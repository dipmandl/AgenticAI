#!/usr/bin/env python3
"""Generate combined HTML report from final-stlc-report.json and agent-metrics.json.

Moved to .claude/scripts to centralize utility scripts.
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
_FLAT_REPORT_JSON = ROOT / "artifacts" / "reports" / "final-stlc-report.json"


def resolve_state_json(story_id: str) -> Path:
    """Return per-story state path, falling back to legacy flat path."""
    per_story = ROOT / "artifacts" / story_id / "state" / "stlc-state.json"
    if per_story.exists():
        return per_story
    return ROOT / "artifacts" / "state" / "stlc-state.json"


def extract_phase_models(state: dict) -> dict[str, str]:
    """Return {metrics_phase_name: model_id} from stlc-state.json artifacts section.

    stlc-state.json uses snake_case phase keys; the metrics table uses the names
    produced by token-usage.py AGENT_TO_PHASE. This mapping aligns them.
    """
    # state key → metrics phase name (only where they differ)
    STATE_TO_METRICS = {
        "test_planning":       "test-plan",
        "test_review_fixes":   "test-review",   # merged into test-review phase
        "framework_selection": "automation-generation",  # framework-selection-agent maps here
        "automation_fixes":    "automation-review",      # merged into automation-review phase
        "failure_analysis":    "execution",              # failure-analysis-agent maps to execution
    }

    models: dict[str, str] = {}
    for phase, data in state.get("artifacts", {}).items():
        model = data.get("model_id", "")
        if not model:
            continue
        metrics_key = STATE_TO_METRICS.get(phase, phase.replace("_", "-"))
        # Keep the first (earliest) model seen for a merged phase
        models.setdefault(metrics_key, model)

    # orchestrator is not a tracked artifact phase in state — derive its model
    # from the agent definition frontmatter if not already found
    if "orchestrator" not in models:
        agent_def = ROOT / ".claude" / "agents" / "1-stlc-orchestrator.md"
        try:
            for line in agent_def.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("model:"):
                    models["orchestrator"] = line.split(":", 1)[1].strip()
                    break
        except OSError:
            pass

    return models


def find_state_json() -> Path:
    """Find stlc-state.json — per-story path first, legacy flat path as fallback."""
    matches = sorted(
        ROOT.glob("artifacts/*/state/stlc-state.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if matches:
        return matches[0]
    return ROOT / "artifacts" / "state" / "stlc-state.json"


def resolve_report_json() -> Path:
    """Return the per-story report JSON path, falling back to the legacy flat path."""
    try:
        state = json.loads(find_state_json().read_text(encoding="utf-8"))
        story_id = state.get("story_id")
        if story_id:
            candidate = ROOT / "artifacts" / story_id / "reports" / "final-stlc-report.json"
            if candidate.exists():
                return candidate
    except (OSError, json.JSONDecodeError):
        pass
    return _FLAT_REPORT_JSON


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def format_number(num: int | float) -> str:
    if isinstance(num, float):
        return f"{num:,.2f}"
    return f"{num:,}"


def metrics_json_for_story(story_id: str) -> Path:
    return ROOT / "artifacts" / story_id / "metrics" / "agent-metrics.json"


def generate_html(report: dict, metrics: dict) -> str:
    """Generate combined HTML report."""

    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>STLC Report</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;500;600;700;800&family=Source+Sans+3:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
:root {
  --bg:        #EEF2F7;
  --surface:   #FFFFFF;
  --surface-2: #F5F8FC;
  --border:    #CDD7E3;
  --text:      #1C2B3A;
  --muted:     #546E8A;
  --accent:    #2B5EA7;
  --accent-bg: #EAF0FA;
  --pass:      #0E7A55;
  --pass-bg:   #E5F5EF;
  --fail:      #C4362A;
  --fail-bg:   #FAEAE8;
  --xfail:     #8B6200;
  --xfail-bg:  #FDF3DC;
  --warn:      #9A4E00;
  --warn-bg:   #FEF0E0;
  --shadow:    0 4px 12px rgba(28,43,58,.08);
  --radius:    8px;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg:        #111D2C;
    --surface:   #192435;
    --surface-2: #1F2E42;
    --border:    #253650;
    --text:      #DCE8F5;
    --muted:     #7A90A8;
    --accent:    #5B8FD8;
    --accent-bg: #1A2F50;
    --pass:      #34C68A;
    --pass-bg:   #0C2D20;
    --fail:      #E8685E;
    --fail-bg:   #2D1210;
    --xfail:     #D4A830;
    --xfail-bg:  #2B2000;
    --warn:      #E09050;
    --warn-bg:   #2A1800;
  }
}

* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: "Source Sans 3", system-ui, sans-serif;
  font-size: 14px;
  line-height: 1.6;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

h1, h2, h3 {
  font-family: "Figtree", sans-serif;
  margin: 1.5rem 0 0.75rem 0;
}

h1 { font-size: 2rem; margin-top: 0; }
h2 { font-size: 1.5rem; border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; }
h3 { font-size: 1.1rem; }

table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  overflow: hidden;
}

th {
  background: var(--surface-2);
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid var(--border);
  color: var(--accent);
}

td {
  padding: 0.75rem;
  border-bottom: 1px solid var(--border);
}

tr:last-child td { border-bottom: none; }
tr:hover { background: var(--surface-2); }

.stat-box {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
}

.stat {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1rem;
  box-shadow: var(--shadow);
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--accent);
  font-family: "JetBrains Mono";
}

.stat-label {
  font-size: 0.85rem;
  color: var(--muted);
  margin-top: 0.25rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.pass { color: var(--pass); }
.fail { color: var(--fail); }
.xfail { color: var(--xfail); }
.warn { color: var(--warn); }

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.85rem;
  font-weight: 500;
}

.badge-pass { background: var(--pass-bg); color: var(--pass); }
.badge-fail { background: var(--fail-bg); color: var(--fail); }
.badge-xfail { background: var(--xfail-bg); color: var(--xfail); }
.badge-warn { background: var(--warn-bg); color: var(--warn); }

.tabs {
  display: flex;
  gap: 0;
  border-bottom: 2px solid var(--border);
  margin: 1.5rem 0 1rem 0;
}

.tab-btn {
  padding: 0.75rem 1.5rem;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  color: var(--muted);
  transition: all 0.2s;
}

.tab-btn:hover { color: var(--accent); }
.tab-btn.active {
  color: var(--accent);
  border-bottom-color: var(--accent);
}

.tab-content {
  display: none;
}

.tab-content.active {
  display: block;
}

.metric-row {
  display: grid;
  grid-template-columns: 2fr 1.5fr 1fr 1fr 1fr;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid var(--border);
}

.metric-row.header {
  font-weight: 600;
  background: var(--surface-2);
  border-bottom: 2px solid var(--border);
}

.metric-cell {
  font-family: "JetBrains Mono";
  font-size: 0.9rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.summary-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.5rem;
  box-shadow: var(--shadow);
}

.summary-card h3 {
  margin-top: 0;
}

.footer {
  text-align: center;
  color: var(--muted);
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid var(--border);
  font-size: 0.9rem;
}

code {
  background: var(--surface-2);
  padding: 0.2rem 0.5rem;
  border-radius: 3px;
  font-family: "JetBrains Mono";
  font-size: 0.9rem;
}
</style>
</head>
<body>
<div class="container">
"""

    # Header
    pipeline_id = report.get("pipeline_id", "N/A")
    story_id = report.get("story_id", "N/A")
    story_title = report.get("story_title", "N/A")
    report_date = report.get("report_date", "N/A")

    html += f"""
<h1>STLC Report: {pipeline_id}</h1>
<div style="color: var(--muted); margin-bottom: 2rem;">
  <strong>Story:</strong> {story_id} — {story_title}<br>
  <strong>Report Date:</strong> {report_date}
</div>
"""

    # Status & Summary — handle both new flat-field format and legacy nested format
    status = (report.get("release_readiness_verdict")
              or report.get("status", "UNKNOWN"))
    status_class = "pass" if "PASS" in status or "APPROVED" in status else "fail" if "FAIL" in status else "warn"
    test_cases_total = (report.get("test_cases_planned")
                        or report.get("test_cases_total", 0))

    html += f"""
<div class="stat-box">
  <div class="stat">
    <div class="stat-value {status_class}">{status}</div>
    <div class="stat-label">Pipeline Status</div>
  </div>
  <div class="stat">
    <div class="stat-value">{report.get("requirements", 0)}</div>
    <div class="stat-label">Requirements</div>
  </div>
  <div class="stat">
    <div class="stat-value">{test_cases_total}</div>
    <div class="stat-label">Total Test Cases</div>
  </div>
  <div class="stat">
    <div class="stat-value">{report.get("test_cases_automated", 0)}</div>
    <div class="stat-label">Automated Tests</div>
  </div>
</div>
"""

    # Execution Results — new JSON uses tests_passed/tests_failed; legacy uses passed/failed
    passed = report.get("tests_passed") if report.get("tests_passed") is not None else report.get("passed", 0)
    failed = report.get("tests_failed") if report.get("tests_failed") is not None else report.get("failed", 0)
    xfailed = (report.get("tests_skipped")
               if report.get("tests_skipped") is not None
               else report.get("xfailed", 0))
    total_executed = report.get("tests_executed", 0)
    pass_rate = (report.get("pass_rate_percentage")
                 or report.get("pass_rate_percent", 0))

    html += f"""
<h2>Execution Results</h2>
<div class="stat-box">
  <div class="stat">
    <div class="stat-value pass">{passed}</div>
    <div class="stat-label">Passed</div>
  </div>
  <div class="stat">
    <div class="stat-value fail">{failed}</div>
    <div class="stat-label">Failed</div>
  </div>
  <div class="stat">
    <div class="stat-value xfail">{xfailed}</div>
    <div class="stat-label">Expected Failures</div>
  </div>
  <div class="stat">
    <div class="stat-value">{total_executed}</div>
    <div class="stat-label">Total Executed</div>
  </div>
  <div class="stat">
    <div class="stat-value pass">{pass_rate}%</div>
    <div class="stat-label">Pass Rate</div>
  </div>
</div>
"""

    # Test Groups — support both nested dict format and flat test_group_<name>_<field> format
    test_groups = report.get("test_groups", {})
    if not test_groups:
        # Build from flat fields: test_group_positive_passed, test_group_positive_failed, etc.
        for grp in ("positive", "negative", "boundary", "regression", "filter_persistence"):
            p = report.get(f"test_group_{grp}_passed", 0)
            f = report.get(f"test_group_{grp}_failed", 0)
            s = report.get(f"test_group_{grp}_skipped", 0)
            if p or f or s:
                test_groups[grp] = {"passed": p, "failed": f, "skipped": s,
                                    "total": p + f + s,
                                    "status": "PASS" if f == 0 else "FAIL"}
    if test_groups:
        html += """
<h3>Test Groups Breakdown</h3>
<table>
<thead><tr>
  <th>Category</th>
  <th>Total</th>
  <th>Passed</th>
  <th>Failed</th>
  <th>Skipped</th>
  <th>Status</th>
</tr></thead>
<tbody>
"""
        for category, data in test_groups.items():
            status_badge = data.get("status", "UNKNOWN")
            badge_class = "pass" if "PASS" in status_badge else "fail" if "FAIL" in status_badge else "xfail"
            skipped = data.get("skipped", data.get("xfailed", 0))
            html += f"""<tr>
  <td><strong>{category.replace("_", " ").title()}</strong></td>
  <td>{data.get("total", 0)}</td>
  <td class="pass"><strong>{data.get("passed", 0)}</strong></td>
  <td class="fail"><strong>{data.get("failed", 0)}</strong></td>
  <td class="xfail">{skipped}</td>
  <td><span class="badge badge-{badge_class}">{status_badge}</span></td>
</tr>
"""
        html += """</tbody>
</table>
"""

    # Defects
    defects = report.get("defects", [])
    if defects:
        html += """
<h2>Defects Found</h2>
<table>
<thead><tr>
  <th>ID</th>
  <th>Title</th>
  <th>Severity</th>
  <th>Status</th>
  <th>Failed Tests</th>
</tr></thead>
<tbody>
"""
        for defect in defects:
            defect_id = defect.get("defect_id", "N/A")
            title = defect.get("title", "N/A")
            severity = defect.get("severity", "UNKNOWN")
            status = defect.get("status", "UNKNOWN")
            failed_count = defect.get("failed_test_count", 0)
            severity_class = "fail" if severity == "HIGH" else "warn"
            html += f"""<tr>
  <td><strong>{defect_id}</strong></td>
  <td>{title}</td>
  <td><span class="badge badge-{severity_class}">{severity}</span></td>
  <td>{status}</td>
  <td>{failed_count}</td>
</tr>
"""
        html += """</tbody>
</table>
"""

    # Metrics Section
    per_phase = metrics.get("per_phase", {})
    per_agent = metrics.get("per_agent", {})

    if per_phase or per_agent:
        html += """
<h2>Agent Metrics</h2>
<div class="tabs">
  <button class="tab-btn active" onclick="switchTab(event, 'metrics-phase')">Per Phase</button>
  <button class="tab-btn" onclick="switchTab(event, 'metrics-agent')">Per Agent</button>
</div>
"""

        # Per Phase Metrics
        phase_models = metrics.get("phase_models", {})
        if per_phase:
            html += """
<div id="metrics-phase" class="tab-content active">
<table>
<thead><tr>
  <th>Phase</th>
  <th>Model</th>
  <th>Input Tokens</th>
  <th>Output Tokens</th>
  <th>Cache Creation</th>
  <th>Cache Read</th>
  <th>Messages</th>
  <th>Invocations</th>
</tr></thead>
<tbody>
"""
            total_input = total_output = total_cache_creation = total_cache_read = 0
            total_messages = total_invocations = 0

            for phase, data in sorted(per_phase.items()):
                input_tokens = data.get("input_tokens", 0)
                output_tokens = data.get("output_tokens", 0)
                cache_creation = data.get("cache_creation_input_tokens", 0)
                cache_read = data.get("cache_read_input_tokens", 0)
                messages = data.get("messages", 0)
                invocations = data.get("invocations", 0)
                model = phase_models.get(phase, "n/a")

                total_input += input_tokens
                total_output += output_tokens
                total_cache_creation += cache_creation
                total_cache_read += cache_read
                total_messages += messages
                total_invocations += invocations

                html += f"""<tr>
  <td><strong>{phase}</strong></td>
  <td><code>{model}</code></td>
  <td>{format_number(input_tokens)}</td>
  <td>{format_number(output_tokens)}</td>
  <td>{format_number(cache_creation)}</td>
  <td>{format_number(cache_read)}</td>
  <td>{messages}</td>
  <td>{invocations}</td>
</tr>
"""

            html += f"""<tr style="background: var(--surface-2); font-weight: 600; border-top: 2px solid var(--border);">
  <td>TOTAL</td>
  <td></td>
  <td>{format_number(total_input)}</td>
  <td>{format_number(total_output)}</td>
  <td>{format_number(total_cache_creation)}</td>
  <td>{format_number(total_cache_read)}</td>
  <td>{total_messages}</td>
  <td>{total_invocations}</td>
</tr>
</tbody>
</table>
</div>
"""

        # Per Agent Metrics
        if per_agent:
            html += """
<div id="metrics-agent" class="tab-content">
<table>
<thead><tr>
  <th>Agent</th>
  <th>Input Tokens</th>
  <th>Output Tokens</th>
  <th>Cache Creation</th>
  <th>Cache Read</th>
  <th>Messages</th>
  <th>Invocations</th>
</tr></thead>
<tbody>
"""
            total_input = total_output = total_cache_creation = total_cache_read = 0
            total_messages = total_invocations = 0

            for agent, data in sorted(per_agent.items()):
                input_tokens = data.get("input_tokens", 0)
                output_tokens = data.get("output_tokens", 0)
                cache_creation = data.get("cache_creation_input_tokens", 0)
                cache_read = data.get("cache_read_input_tokens", 0)
                messages = data.get("messages", 0)
                invocations = data.get("invocations", 0)

                total_input += input_tokens
                total_output += output_tokens
                total_cache_creation += cache_creation
                total_cache_read += cache_read
                total_messages += messages
                total_invocations += invocations

                html += f"""<tr>
  <td><strong>{agent}</strong></td>
  <td>{format_number(input_tokens)}</td>
  <td>{format_number(output_tokens)}</td>
  <td>{format_number(cache_creation)}</td>
  <td>{format_number(cache_read)}</td>
  <td>{messages}</td>
  <td>{invocations}</td>
</tr>
"""

            html += f"""<tr style="background: var(--surface-2); font-weight: 600; border-top: 2px solid var(--border);">
  <td>TOTAL</td>
  <td>{format_number(total_input)}</td>
  <td>{format_number(total_output)}</td>
  <td>{format_number(total_cache_creation)}</td>
  <td>{format_number(total_cache_read)}</td>
  <td>{total_messages}</td>
  <td>{total_invocations}</td>
</tr>
</tbody>
</table>
</div>
"""

    # Environment — new JSON uses test_framework / primary_browser / execution_timestamp
    framework = (report.get("test_framework")
                 or report.get("framework", "N/A"))
    browser = (report.get("primary_browser")
               or report.get("browser", "N/A"))
    execution_start = (report.get("execution_timestamp")
                       or report.get("execution_start_time")
                       or report.get("execution_date", "N/A"))
    execution_end = report.get("execution_end_time", "N/A")
    duration = report.get("duration_seconds", 0)
    app_path = report.get("application_path", "N/A")
    test_root = report.get("test_root", "N/A")
    healed = report.get("healed", report.get("defects_automation_healed", 0))
    app_defects = report.get("defects_application", 0)

    html += f"""
<h2>Environment & Execution</h2>
<table>
<tr><td><strong>Framework</strong></td><td>{framework}</td></tr>
<tr><td><strong>Browser</strong></td><td>{browser}</td></tr>
<tr><td><strong>Application</strong></td><td>{app_path}</td></tr>
<tr><td><strong>Test Root</strong></td><td>{test_root}</td></tr>
<tr><td><strong>Execution Date</strong></td><td>{execution_start}</td></tr>
<tr><td><strong>Duration</strong></td><td>{f"{duration:.2f} seconds" if duration else "N/A"}</td></tr>
<tr><td><strong>Application Defects</strong></td><td>{app_defects}</td></tr>
<tr><td><strong>Self-Healed</strong></td><td>{healed}</td></tr>
</table>
"""

    # Footer
    html += f"""
<div class="footer">
  <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
</div>
</div>

<script>
function switchTab(event, tabId) {{
  // Hide all tabs
  const tabs = document.querySelectorAll('.tab-content');
  tabs.forEach(t => t.classList.remove('active'));

  // Remove active class from all buttons
  const buttons = document.querySelectorAll('.tab-btn');
  buttons.forEach(b => b.classList.remove('active'));

  // Show selected tab and mark button active
  document.getElementById(tabId).classList.add('active');
  event.target.classList.add('active');
}}
</script>
</body>
</html>
"""

    return html


def main():
    report_json = resolve_report_json()
    report = load_json(report_json)

    if not report:
        print(f"[ERROR] {report_json} not found or empty")
        return 1

    story_id = str(report.get("story_id") or "general")
    metrics_json = metrics_json_for_story(story_id)
    metrics = load_json(metrics_json)

    if not metrics:
        print(f"[WARN] {metrics_json} not found or empty")

    state = load_json(resolve_state_json(story_id))
    phase_models = extract_phase_models(state)
    metrics["phase_models"] = phase_models

    html = generate_html(report, metrics)

    # Write into a per-story folder under artifacts/reports/<story_id>/stlc-report.html
    output_html = ROOT / "artifacts" / story_id / "reports" / "stlc-report.html"

    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(html, encoding="utf-8")

    print(f"[OK] HTML report generated: {output_html}")
    return 0


if __name__ == "__main__":
    exit(main())