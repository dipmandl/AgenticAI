#!/usr/bin/env python3
"""Log agent invocation metadata (agentType, model) from PostToolUse hook.

Called by the PostToolUse:Agent hook after each Agent tool call.
Reads the hook payload from stdin and appends a record to
artifacts/<story_id>/metrics/agent-invocations.jsonl.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def find_story_id() -> str:
    matches = sorted(
        ROOT.glob("artifacts/*/state/stlc-state.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if matches:
        try:
            data = json.loads(matches[0].read_text(encoding="utf-8"))
            return str(data.get("story_id", "general"))
        except Exception:
            pass
    return "general"


def main():
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        payload = {}

    tool_input = payload.get("tool_input", {})
    tool_result = payload.get("tool_result", {})

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent_type": tool_input.get("subagent_type", "unknown"),
        "agent_name": tool_input.get("name", ""),
        "description": tool_input.get("description", ""),
        "model": tool_input.get("model", "default"),
        "result_summary": str(tool_result)[:200] if tool_result else "",
    }

    story_id = find_story_id()
    metrics_dir = ROOT / "artifacts" / story_id / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    log_path = metrics_dir / "agent-invocations.jsonl"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


if __name__ == "__main__":
    main()
