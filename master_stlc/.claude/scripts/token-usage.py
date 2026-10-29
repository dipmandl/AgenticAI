#!/usr/bin/env python3
r"""Calculate token usage per STLC phase from Claude Code transcript files.

Reads session transcripts (JSONL) from ~/.claude/projects/<project>/ and the
subagent transcripts under <session-id>/subagents/. Each subagent has a
meta.json with its agentType, which is mapped to an STLC phase.

Usage:
    python .claude\scripts\token-usage.py                 # print report + write artifacts/<story_id>/metrics/
    python .claude\scripts\token-usage.py --no-write      # print only
    python .claude\scripts\token-usage.py --project-dir <path-to-transcript-dir>
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

AGENT_TO_PHASE = {
    "repository-discovery-agent": "repository-discovery",
    "requirement-analysis-agent": "requirement-analysis",
    "impact-analysis-agent": "impact-analysis",
    "test-planning-agent": "test-plan",
    "manual-test-generation-agent": "manual-test-generation",
    "test-review-agent": "test-review",
    "framework-selection-agent": "automation-generation",
    "automation-generation-agent": "automation-generation",
    "automation-review-agent": "automation-review",
    "execution-agent": "execution",
    "failure-analysis-agent": "execution",
    "defect-analysis-agent": "execution",
    "self-healing-agent": "self-healing",
    "reporting-agent": "reporting",
    "stlc-orchestrator": "orchestrator",
}

USAGE_FIELDS = (
    "input_tokens",
    "output_tokens",
    "cache_creation_input_tokens",
    "cache_read_input_tokens",
)

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REPORT_JSON = ROOT / "artifacts" / "reports" / "final-stlc-report.json"


def find_state_json() -> Path:
    """Find stlc-state.json — per-story path first, legacy flat path as fallback."""
    # Scan for artifacts/*/state/stlc-state.json (per-story pattern)
    matches = sorted(
        ROOT.glob("artifacts/*/state/stlc-state.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if matches:
        return matches[0]
    return ROOT / "artifacts" / "state" / "stlc-state.json"


def default_project_dir() -> Path:
    cwd = Path.cwd().resolve()
    sanitized = str(cwd).replace("\\", "-").replace("/", "-").replace(":", "").replace(".", "-").replace("_", "-")
    if not sanitized.startswith("-"):
        sanitized = sanitized[0].lower() + sanitized[1:]
    candidate = Path.home() / ".claude" / "projects" / sanitized
    if candidate.is_dir():
        return candidate
    # fallback: pick the projects dir whose name ends with the cwd folder name
    projects = Path.home() / ".claude" / "projects"
    tail = cwd.name.replace("_", "-").lower()
    matches = [p for p in projects.iterdir() if p.is_dir() and p.name.lower().endswith(tail)]
    if len(matches) == 1:
        return matches[0]
    sys.exit(
        f"Could not locate transcript dir (tried {candidate}). "
        "Pass it explicitly with --project-dir."
    )


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def resolve_story_id() -> str:
    state = load_json(find_state_json())
    if state.get("story_id"):
        return str(state["story_id"])
    report = load_json(DEFAULT_REPORT_JSON)
    return str(report.get("story_id") or "general")


def sum_usage(jsonl_path: Path) -> dict:
    """Sum token usage across assistant messages, deduplicated by message id."""
    seen: dict[str, dict] = {}
    with open(jsonl_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("type") != "assistant":
                continue
            msg = entry.get("message") or {}
            usage = msg.get("usage")
            if not usage:
                continue
            key = msg.get("id") or entry.get("requestId") or str(len(seen))
            seen[key] = usage  # last entry for a message id wins

    totals = {k: 0 for k in USAGE_FIELDS}
    totals["messages"] = len(seen)
    for usage in seen.values():
        for k in USAGE_FIELDS:
            totals[k] += usage.get(k) or 0
    return totals


def collect(project_dir: Path) -> tuple[dict, dict]:
    per_agent: dict[str, dict] = defaultdict(lambda: {k: 0 for k in (*USAGE_FIELDS, "messages", "invocations")})

    def add(bucket: dict, usage: dict):
        for k in (*USAGE_FIELDS, "messages"):
            bucket[k] += usage[k]

    for session_file in sorted(project_dir.glob("*.jsonl")):
        usage = sum_usage(session_file)
        if usage["messages"]:
            bucket = per_agent["main-session (orchestrator)"]
            add(bucket, usage)
            bucket["invocations"] += 1

        subagents_dir = project_dir / session_file.stem / "subagents"
        if not subagents_dir.is_dir():
            continue
        for meta_file in sorted(subagents_dir.glob("agent-*.meta.json")):
            try:
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            agent_type = meta.get("agentType", "unknown")
            transcript = meta_file.with_name(meta_file.name.replace(".meta.json", ".jsonl"))
            if not transcript.exists():
                continue
            usage = sum_usage(transcript)
            bucket = per_agent[agent_type]
            add(bucket, usage)
            bucket["invocations"] += 1

    per_phase: dict[str, dict] = defaultdict(lambda: {k: 0 for k in (*USAGE_FIELDS, "messages", "invocations")})
    for agent, usage in per_agent.items():
        phase = AGENT_TO_PHASE.get(agent, "orchestrator" if agent.startswith("main-session") else "other")
        for k in (*USAGE_FIELDS, "messages", "invocations"):
            per_phase[phase][k] += usage[k]

    return dict(per_agent), dict(per_phase)


def total_of(usage: dict) -> int:
    return sum(usage[k] for k in USAGE_FIELDS)


def fmt_table(title: str, rows: dict) -> str:
    header = f"| {title} | Input | Output | Cache Write | Cache Read | Total | Msgs | Runs |"
    sep = "|" + "---|" * 8
    lines = [header, sep]
    grand = {k: 0 for k in (*USAGE_FIELDS, "messages", "invocations")}
    for name, u in sorted(rows.items(), key=lambda x: -total_of(x[1])):
        lines.append(
            f"| {name} | {u['input_tokens']:,} | {u['output_tokens']:,} | "
            f"{u['cache_creation_input_tokens']:,} | {u['cache_read_input_tokens']:,} | "
            f"{total_of(u):,} | {u['messages']} | {u['invocations']} |"
        )
        for k in grand:
            grand[k] += u[k]
    lines.append(
        f"| **TOTAL** | **{grand['input_tokens']:,}** | **{grand['output_tokens']:,}** | "
        f"**{grand['cache_creation_input_tokens']:,}** | **{grand['cache_read_input_tokens']:,}** | "
        f"**{total_of(grand):,}** | **{grand['messages']}** | **{grand['invocations']}** |"
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Per-phase token usage from Claude Code transcripts")
    parser.add_argument("--project-dir", type=Path, help="Claude Code transcript dir for this project")
    parser.add_argument("--no-write", action="store_true", help="Print only; do not write artifacts/<story_id>/metrics/")
    args = parser.parse_args()

    project_dir = args.project_dir or default_project_dir()
    per_agent, per_phase = collect(project_dir)

    if not per_agent:
        sys.exit(f"No transcripts with usage data found in {project_dir}")

    phase_table = fmt_table("Phase", per_phase)
    agent_table = fmt_table("Agent", per_agent)
    report = (
        f"# STLC Token Usage\n\nSource: `{project_dir}`\n\n"
        f"## Per Phase\n\n{phase_table}\n\n## Per Agent\n\n{agent_table}\n"
    )
    print(report)

    if not args.no_write:
        story_id = resolve_story_id()
        metrics_dir = ROOT / "artifacts" / story_id / "metrics"
        metrics_dir.mkdir(parents=True, exist_ok=True)
        (metrics_dir / "agent-metrics.md").write_text(report, encoding="utf-8")
        (metrics_dir / "agent-metrics.json").write_text(
            json.dumps({"source": str(project_dir), "per_phase": per_phase, "per_agent": per_agent}, indent=2),
            encoding="utf-8",
        )
        print(f"Written: {metrics_dir / 'agent-metrics.md'} and .json")


if __name__ == "__main__":
    main()
