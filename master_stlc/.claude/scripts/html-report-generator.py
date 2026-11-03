#!/usr/bin/env python3
"""Generate HTML report by reading stable raw artifacts directly.

Primary sources (machine-written, stable schemas):
  - stlc-state.json          → pipeline status, phase summaries, model IDs
  - execution-results.json   → pass/fail counts, browsers, duration, per-TC results
  - framework-selection.json → framework name, language
  - agent-metrics.json       → token usage per phase / per agent

Fallback source (freeform, used only for fields not available above):
  - final-stlc-report.json   → requirements count, test case totals, story title
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# Artifact finders
# ---------------------------------------------------------------------------

def find_story_dir() -> Path | None:
    """Return the most recently modified per-story artifacts directory."""
    candidates = sorted(
        ROOT.glob("artifacts/*/state/stlc-state.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if candidates:
        return candidates[0].parent.parent  # artifacts/<story_id>/
    return None


def load_json(path: Path) -> dict:
    if path and path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def format_number(n) -> str:
    if isinstance(n, float):
        return f"{n:,.2f}"
    try:
        return f"{int(n):,}"
    except (TypeError, ValueError):
        return str(n)


# ---------------------------------------------------------------------------
# Data extraction from stable sources
# ---------------------------------------------------------------------------

def extract_from_state(state: dict) -> dict:
    """Pull all usable fields from stlc-state.json."""
    phases = state.get("phases", {})
    exec_summary = phases.get("execution", {}).get("summary", {})
    fail_summary = phases.get("failure_analysis", {}).get("summary", {})
    review_totals = phases.get("automation_review", {}).get("totals", {})

    completed = state.get("completed_phases", [])
    required = [
        "repository_discovery", "requirement_analysis", "impact_analysis",
        "test_planning", "manual_test_generation", "test_review",
        "framework_selection", "automation_generation", "automation_review",
        "execution", "failure_analysis", "reporting",
    ]
    all_done = all(p in completed for p in required)
    has_failures = fail_summary.get("automation_failures", 0) + fail_summary.get("application_failures", 0) > 0
    status = "PASS" if (all_done and not has_failures) else ("FAIL" if has_failures else "IN PROGRESS")

    # Phase model IDs
    phase_models = {}
    for phase_key, phase_data in phases.items():
        if isinstance(phase_data, dict):
            model = phase_data.get("model_id", "")
            if model:
                metrics_key = phase_key.replace("_", "-")
                phase_models.setdefault(metrics_key, model)

    return {
        "story_id": state.get("story_id", ""),
        "pipeline_id": state.get("pipeline_id", ""),
        "status": status,
        "completed_phases": completed,
        "exec_total": exec_summary.get("total_tests", 0),
        "exec_passed": exec_summary.get("passed", 0),
        "exec_failed": exec_summary.get("failed", 0),
        "exec_skipped": exec_summary.get("skipped", 0),
        "exec_pass_rate": exec_summary.get("pass_rate", ""),
        "exec_unique_tc": exec_summary.get("unique_tc_count", 0),
        "exec_browsers": exec_summary.get("browsers", 0),
        "automation_failures": fail_summary.get("automation_failures", 0),
        "application_failures": fail_summary.get("application_failures", 0),
        "environment_failures": fail_summary.get("environment_failures", 0),
        "data_failures": fail_summary.get("data_failures", 0),
        "self_healing_required": fail_summary.get("self_healing_required", False),
        "review_pass": review_totals.get("pass", 0),
        "review_fail": review_totals.get("fail", 0),
        "review_warn": review_totals.get("warn", 0),
        "phase_models": phase_models,
        "config": state.get("config", {}),
    }


def extract_from_execution(exec_results: dict) -> dict:
    """Pull execution details from execution-results.json."""
    if not exec_results:
        return {}

    results = exec_results.get("test_results", [])

    # Build per-TC breakdown from test_results
    tc_map: dict[str, dict] = {}
    for r in results:
        tc_id = r.get("tc_id", "")
        spec = r.get("spec_file", "")
        status = r.get("status", "")
        if tc_id not in tc_map:
            tc_map[tc_id] = {"title": r.get("title", tc_id), "spec": spec, "browsers": [], "statuses": []}
        tc_map[tc_id]["browsers"].append(r.get("browser", ""))
        tc_map[tc_id]["statuses"].append(status)

    # Group TCs by spec file → derive category from spec name
    spec_groups: dict[str, list] = {}
    for tc_id, tc in tc_map.items():
        spec = tc["spec"]
        group = "other"
        for cat in ("positive", "negative", "boundary", "regression"):
            if cat in spec:
                group = cat
                break
        spec_groups.setdefault(group, []).append(tc_id)

    group_stats: dict[str, dict] = {}
    for group, tc_ids in spec_groups.items():
        g_pass = g_fail = 0
        for tc_id in tc_ids:
            statuses = tc_map[tc_id]["statuses"]
            if all(s == "PASS" for s in statuses):
                g_pass += 1
            else:
                g_fail += 1
        group_stats[group] = {
            "total": len(tc_ids),
            "passed": g_pass,
            "failed": g_fail,
            "status": "PASS" if g_fail == 0 else "FAIL",
        }

    browsers = exec_results.get("browsers", [])
    browser_str = ", ".join(browsers) if isinstance(browsers, list) else str(browsers)

    return {
        "total": exec_results.get("total_tests", 0),
        "passed": exec_results.get("passed", 0),
        "failed": exec_results.get("failed", 0),
        "skipped": exec_results.get("skipped", 0),
        "pass_rate": exec_results.get("pass_rate", 0),
        "unique_tc": exec_results.get("unique_test_cases", 0),
        "browsers": browser_str,
        "duration_ms": exec_results.get("suite_duration_ms", 0),
        "timestamp": exec_results.get("execution_timestamp", ""),
        "group_stats": group_stats,
        "tc_map": tc_map,
        "known_warnings": exec_results.get("known_warnings", []),
    }


def extract_from_framework(fw: dict) -> dict:
    """Pull framework details from framework-selection.json."""
    return {
        "framework": fw.get("framework", "N/A"),
        "language": fw.get("language", ""),
        "automation_root": fw.get("automation_root", ""),
        "test_root": fw.get("test_root", ""),
    }


def extract_fallback(report: dict) -> dict:
    """Extract fields from final-stlc-report.json that have no other source."""
    req_raw = report.get("requirements", {})
    if isinstance(req_raw, dict):
        req_total = req_raw.get("total", 0)
    else:
        req_total = int(req_raw) if req_raw else 0

    tc_raw = report.get("test_cases", {})
    if isinstance(tc_raw, dict):
        tc_total = tc_raw.get("total", 0)
        tc_auto = tc_raw.get("automated", 0)
        tc_manual = tc_raw.get("manual", 0)
    else:
        tc_total = tc_auto = tc_manual = 0

    # Try flat fields if nested not found
    tc_total = tc_total or report.get("test_cases_planned") or report.get("test_cases_total", 0)
    tc_auto = tc_auto or report.get("test_cases_automated", 0)

    return {
        "story_title": report.get("story_title", report.get("summary", "")),
        "req_total": req_total,
        "tc_total": tc_total,
        "tc_auto": tc_auto,
        "tc_manual": tc_manual,
    }


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

def generate_html(s: dict, e: dict, fw: dict, fb: dict, metrics: dict) -> str:
    story_id = s.get("story_id", "N/A")
    pipeline_id = s.get("pipeline_id", story_id)
    story_title = fb.get("story_title") or ""
    status = s.get("status", "UNKNOWN")
    status_class = "pass" if status == "PASS" else "fail" if "FAIL" in status else "warn"

    # Execution numbers — prefer execution-results.json, fall back to state summary
    total = e.get("total") or s.get("exec_total", 0)
    passed = e.get("passed") or s.get("exec_passed", 0)
    failed = e.get("failed") or s.get("exec_failed", 0)
    skipped = e.get("skipped") or s.get("exec_skipped", 0)
    pass_rate = e.get("pass_rate") or s.get("exec_pass_rate", 0)
    unique_tc = e.get("unique_tc") or s.get("exec_unique_tc", 0)
    browsers_str = e.get("browsers", "")
    duration_ms = e.get("duration_ms", 0)
    exec_ts = e.get("timestamp", "")

    # Test counts — execution-results unique_tc is most accurate, fallback to plan
    tc_total = fb.get("tc_total") or unique_tc or 0
    tc_auto = fb.get("tc_auto") or unique_tc or 0
    tc_manual = fb.get("tc_manual", 0)
    req_total = fb.get("req_total", 0)

    framework = fw.get("framework", "N/A")
    language = fw.get("language", "")
    framework_str = f"{framework} ({language})" if language else framework

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>STLC Report — {story_id}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&family=Source+Sans+3:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
:root {{
  --bg: #EEF2F7; --surface: #FFFFFF; --surface-2: #F5F8FC;
  --border: #CDD7E3; --text: #1C2B3A; --muted: #546E8A;
  --accent: #2B5EA7; --accent-bg: #EAF0FA;
  --pass: #0E7A55; --pass-bg: #E5F5EF;
  --fail: #C4362A; --fail-bg: #FAEAE8;
  --xfail: #8B6200; --xfail-bg: #FDF3DC;
  --warn: #9A4E00; --warn-bg: #FEF0E0;
  --shadow: 0 4px 12px rgba(28,43,58,.08); --radius: 8px;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --bg: #111D2C; --surface: #192435; --surface-2: #1F2E42;
    --border: #253650; --text: #DCE8F5; --muted: #7A90A8;
    --accent: #5B8FD8; --accent-bg: #1A2F50;
    --pass: #34C68A; --pass-bg: #0C2D20;
    --fail: #E8685E; --fail-bg: #2D1210;
    --xfail: #D4A830; --xfail-bg: #2B2000;
    --warn: #E09050; --warn-bg: #2A1800;
  }}
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--bg); color: var(--text);
  font-family: "Source Sans 3", system-ui, sans-serif; font-size: 14px; line-height: 1.6; }}
.container {{ max-width: 1400px; margin: 0 auto; padding: 2rem; }}
h1, h2, h3 {{ font-family: "Figtree", sans-serif; margin: 1.5rem 0 0.75rem 0; }}
h1 {{ font-size: 2rem; margin-top: 0; }}
h2 {{ font-size: 1.5rem; border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; }}
h3 {{ font-size: 1.1rem; }}
table {{ width: 100%; border-collapse: collapse; margin: 1rem 0;
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); overflow: hidden; }}
th {{ background: var(--surface-2); padding: 0.75rem; text-align: left;
  font-weight: 600; border-bottom: 2px solid var(--border); color: var(--accent); }}
td {{ padding: 0.75rem; border-bottom: 1px solid var(--border); }}
tr:last-child td {{ border-bottom: none; }}
tr:hover {{ background: var(--surface-2); }}
.stat-box {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem; margin: 1rem 0; }}
.stat {{ background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 1rem; box-shadow: var(--shadow); }}
.stat-value {{ font-size: 1.75rem; font-weight: 700; color: var(--accent);
  font-family: "JetBrains Mono"; }}
.stat-label {{ font-size: 0.85rem; color: var(--muted); margin-top: 0.25rem;
  text-transform: uppercase; letter-spacing: 0.5px; }}
.pass {{ color: var(--pass); }} .fail {{ color: var(--fail); }}
.xfail {{ color: var(--xfail); }} .warn {{ color: var(--warn); }}
.badge {{ display: inline-block; padding: 0.25rem 0.75rem;
  border-radius: 1rem; font-size: 0.85rem; font-weight: 500; }}
.badge-pass {{ background: var(--pass-bg); color: var(--pass); }}
.badge-fail {{ background: var(--fail-bg); color: var(--fail); }}
.badge-xfail {{ background: var(--xfail-bg); color: var(--xfail); }}
.badge-warn {{ background: var(--warn-bg); color: var(--warn); }}
.tabs {{ display: flex; border-bottom: 2px solid var(--border); margin: 1.5rem 0 1rem 0; }}
.tab-btn {{ padding: 0.75rem 1.5rem; background: none; border: none;
  border-bottom: 3px solid transparent; cursor: pointer; font-size: 0.95rem;
  font-weight: 500; color: var(--muted); transition: all 0.2s; }}
.tab-btn:hover {{ color: var(--accent); }}
.tab-btn.active {{ color: var(--accent); border-bottom-color: var(--accent); }}
.tab-content {{ display: none; }} .tab-content.active {{ display: block; }}
code {{ background: var(--surface-2); padding: 0.2rem 0.5rem;
  border-radius: 3px; font-family: "JetBrains Mono"; font-size: 0.9rem; }}
.footer {{ text-align: center; color: var(--muted); margin-top: 3rem;
  padding-top: 2rem; border-top: 1px solid var(--border); font-size: 0.9rem; }}
</style>
</head>
<body>
<div class="container">

<h1>STLC Report: {pipeline_id}</h1>
<div style="color: var(--muted); margin-bottom: 2rem;">
  <strong>Story:</strong> {story_id}{(' — ' + story_title) if story_title else ''}<br>
  <strong>Report Date:</strong> {datetime.now().strftime('%Y-%m-%d')}
</div>

<div class="stat-box">
  <div class="stat">
    <div class="stat-value {status_class}">{status}</div>
    <div class="stat-label">Pipeline Status</div>
  </div>
  <div class="stat">
    <div class="stat-value">{req_total or '—'}</div>
    <div class="stat-label">Requirements</div>
  </div>
  <div class="stat">
    <div class="stat-value">{tc_total}</div>
    <div class="stat-label">Total Test Cases</div>
  </div>
  <div class="stat">
    <div class="stat-value">{tc_auto}</div>
    <div class="stat-label">Automated</div>
  </div>
  <div class="stat">
    <div class="stat-value">{tc_manual}</div>
    <div class="stat-label">Manual</div>
  </div>
</div>

<h2>Execution Results</h2>
<div class="stat-box">
  <div class="stat">
    <div class="stat-value pass">{format_number(passed)}</div>
    <div class="stat-label">Passed</div>
  </div>
  <div class="stat">
    <div class="stat-value fail">{format_number(failed)}</div>
    <div class="stat-label">Failed</div>
  </div>
  <div class="stat">
    <div class="stat-value xfail">{format_number(skipped)}</div>
    <div class="stat-label">Skipped</div>
  </div>
  <div class="stat">
    <div class="stat-value">{format_number(total)}</div>
    <div class="stat-label">Total Runs</div>
  </div>
  <div class="stat">
    <div class="stat-value pass">{pass_rate}%</div>
    <div class="stat-label">Pass Rate</div>
  </div>
</div>
"""

    # Test group breakdown (from execution-results)
    group_stats = e.get("group_stats", {})
    if group_stats:
        html += """
<h3>Test Group Breakdown</h3>
<table>
<thead><tr>
  <th>Group</th><th>Total</th><th>Passed</th><th>Failed</th><th>Status</th>
</tr></thead>
<tbody>
"""
        order = ["positive", "negative", "boundary", "regression"]
        for grp in order + [g for g in group_stats if g not in order]:
            if grp not in group_stats:
                continue
            d = group_stats[grp]
            badge = "pass" if d["status"] == "PASS" else "fail"
            html += f"""<tr>
  <td><strong>{grp.title()}</strong></td>
  <td>{d['total']}</td>
  <td class="pass"><strong>{d['passed']}</strong></td>
  <td class="fail"><strong>{d['failed']}</strong></td>
  <td><span class="badge badge-{badge}">{d['status']}</span></td>
</tr>
"""
        html += "</tbody></table>\n"

    # Failure breakdown
    auto_f = s.get("automation_failures", 0)
    app_f = s.get("application_failures", 0)
    env_f = s.get("environment_failures", 0)
    data_f = s.get("data_failures", 0)
    total_f = auto_f + app_f + env_f + data_f
    html += f"""
<h2>Failure Analysis</h2>
"""
    if total_f == 0:
        html += '<p style="color: var(--pass);">No failures found. All test executions passed.</p>\n'
    else:
        html += f"""<table>
<thead><tr><th>Category</th><th>Count</th></tr></thead>
<tbody>
<tr><td>Application Failures</td><td class="fail"><strong>{app_f}</strong></td></tr>
<tr><td>Automation Failures</td><td class="warn"><strong>{auto_f}</strong></td></tr>
<tr><td>Environment Failures</td><td><strong>{env_f}</strong></td></tr>
<tr><td>Data Failures</td><td><strong>{data_f}</strong></td></tr>
</tbody></table>
"""

    # Known warnings
    warnings = e.get("known_warnings", [])
    if warnings:
        html += """
<h2>Known Warnings</h2>
<table>
<thead><tr><th>ID</th><th>Description</th></tr></thead>
<tbody>
"""
        for w in warnings:
            w_id = w.get("id", "") if isinstance(w, dict) else ""
            w_desc = w.get("description", str(w)) if isinstance(w, dict) else str(w)
            html += f"<tr><td><strong>{w_id}</strong></td><td>{w_desc}</td></tr>\n"
        html += "</tbody></table>\n"

    # Agent Metrics
    per_phase = metrics.get("per_phase", {})
    per_agent = metrics.get("per_agent", {})
    phase_models = s.get("phase_models", {})

    if per_phase or per_agent:
        html += """
<h2>Agent Metrics</h2>
<div class="tabs">
  <button class="tab-btn active" onclick="switchTab(event,'metrics-phase')">Per Phase</button>
  <button class="tab-btn" onclick="switchTab(event,'metrics-agent')">Per Agent</button>
</div>
"""
        if per_phase:
            html += """<div id="metrics-phase" class="tab-content active">
<table>
<thead><tr>
  <th>Phase</th><th>Model</th><th>Input Tokens</th><th>Output Tokens</th>
  <th>Cache Creation</th><th>Cache Read</th><th>Messages</th><th>Invocations</th>
</tr></thead>
<tbody>
"""
            t_in = t_out = t_cc = t_cr = t_msg = t_inv = 0
            for phase, d in sorted(per_phase.items()):
                i = d.get("input_tokens", 0); o = d.get("output_tokens", 0)
                cc = d.get("cache_creation_input_tokens", 0); cr = d.get("cache_read_input_tokens", 0)
                msg = d.get("messages", 0); inv = d.get("invocations", 0)
                model = phase_models.get(phase, metrics.get("phase_models", {}).get(phase, "n/a"))
                t_in += i; t_out += o; t_cc += cc; t_cr += cr; t_msg += msg; t_inv += inv
                html += f"""<tr>
  <td><strong>{phase}</strong></td><td><code>{model}</code></td>
  <td>{format_number(i)}</td><td>{format_number(o)}</td>
  <td>{format_number(cc)}</td><td>{format_number(cr)}</td>
  <td>{msg}</td><td>{inv}</td>
</tr>
"""
            html += f"""<tr style="background:var(--surface-2);font-weight:600;border-top:2px solid var(--border);">
  <td>TOTAL</td><td></td>
  <td>{format_number(t_in)}</td><td>{format_number(t_out)}</td>
  <td>{format_number(t_cc)}</td><td>{format_number(t_cr)}</td>
  <td>{t_msg}</td><td>{t_inv}</td>
</tr>
</tbody></table></div>
"""

        if per_agent:
            html += """<div id="metrics-agent" class="tab-content">
<table>
<thead><tr>
  <th>Agent</th><th>Input Tokens</th><th>Output Tokens</th>
  <th>Cache Creation</th><th>Cache Read</th><th>Messages</th><th>Invocations</th>
</tr></thead>
<tbody>
"""
            t_in = t_out = t_cc = t_cr = t_msg = t_inv = 0
            for agent, d in sorted(per_agent.items()):
                i = d.get("input_tokens", 0); o = d.get("output_tokens", 0)
                cc = d.get("cache_creation_input_tokens", 0); cr = d.get("cache_read_input_tokens", 0)
                msg = d.get("messages", 0); inv = d.get("invocations", 0)
                t_in += i; t_out += o; t_cc += cc; t_cr += cr; t_msg += msg; t_inv += inv
                html += f"""<tr>
  <td><strong>{agent}</strong></td>
  <td>{format_number(i)}</td><td>{format_number(o)}</td>
  <td>{format_number(cc)}</td><td>{format_number(cr)}</td>
  <td>{msg}</td><td>{inv}</td>
</tr>
"""
            html += f"""<tr style="background:var(--surface-2);font-weight:600;border-top:2px solid var(--border);">
  <td>TOTAL</td>
  <td>{format_number(t_in)}</td><td>{format_number(t_out)}</td>
  <td>{format_number(t_cc)}</td><td>{format_number(t_cr)}</td>
  <td>{t_msg}</td><td>{t_inv}</td>
</tr>
</tbody></table></div>
"""

    # Environment
    duration_s = duration_ms / 1000 if duration_ms else 0
    html += f"""
<h2>Environment &amp; Execution</h2>
<table>
<tr><td><strong>Framework</strong></td><td>{framework_str}</td></tr>
<tr><td><strong>Browsers</strong></td><td>{browsers_str or '—'}</td></tr>
<tr><td><strong>Execution Timestamp</strong></td><td>{exec_ts or '—'}</td></tr>
<tr><td><strong>Duration</strong></td><td>{f'{duration_s:.1f}s' if duration_s else '—'}</td></tr>
<tr><td><strong>Unique Test Cases</strong></td><td>{unique_tc}</td></tr>
<tr><td><strong>Total Executions</strong></td><td>{format_number(total)}</td></tr>
<tr><td><strong>Self-Healing Required</strong></td><td>{'Yes' if s.get('self_healing_required') else 'No'}</td></tr>
<tr><td><strong>Completed Phases</strong></td><td>{len(s.get('completed_phases', []))}</td></tr>
</table>

<div class="footer">
  <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
</div>
</div>

<script>
function switchTab(event, tabId) {{
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
  event.target.classList.add('active');
}}
</script>
</body>
</html>
"""
    return html


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    story_dir = find_story_dir()
    if not story_dir:
        print("[SKIP] No stlc-state.json found — pipeline not started yet.")
        return 0

    # Only generate when reporting phase is complete — skip silently otherwise
    state_check = load_json(story_dir / "state" / "stlc-state.json")
    if "reporting" not in state_check.get("completed_phases", []):
        print("[SKIP] Reporting phase not complete yet — skipping HTML generation.")
        return 0

    story_id = story_dir.name

    state     = load_json(story_dir / "state"     / "stlc-state.json")
    exec_res  = load_json(story_dir / "execution" / "execution-results.json")
    fw        = load_json(story_dir / "framework" / "framework-selection.json")
    metrics   = load_json(story_dir / "metrics"   / "agent-metrics.json")
    fallback  = load_json(story_dir / "reports"   / "final-stlc-report.json")

    if not state:
        print(f"[ERROR] stlc-state.json is empty at {story_dir}/state/")
        return 1

    s  = extract_from_state(state)
    e  = extract_from_execution(exec_res)
    fw = extract_from_framework(fw)
    fb = extract_fallback(fallback)

    # Inject phase_models into metrics for the template
    metrics["phase_models"] = s.get("phase_models", {})

    html = generate_html(s, e, fw, fb, metrics)

    out = story_dir / "reports" / "stlc-report.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"[OK] HTML report → {out}")
    return 0


if __name__ == "__main__":
    exit(main())
