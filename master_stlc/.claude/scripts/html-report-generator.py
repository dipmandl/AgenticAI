#!/usr/bin/env python3
"""Generate combined HTML report from final-stlc-report.json and agent-metrics.json.

Moved to .claude/scripts to centralize utility scripts.
"""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
REPORT_JSON = ROOT / "artifacts" / "reports" / "final-stlc-report.json"


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

    # Status & Summary
    status = report.get("status", "UNKNOWN")
    status_class = "pass" if "PASS" in status else "fail" if "FAIL" in status else "warn"

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
    <div class="stat-value">{report.get("test_cases_total", 0)}</div>
    <div class="stat-label">Total Test Cases</div>
  </div>
  <div class="stat">
    <div class="stat-value">{report.get("test_cases_automated", 0)}</div>
    <div class="stat-label">Automated Tests</div>
  </div>
</div>
"""

    # Execution Results
    passed = report.get("passed", 0)
    failed = report.get("failed", 0)
    xfailed = report.get("xfailed", 0)
    total_executed = report.get("tests_executed", 0)
    pass_rate = report.get("pass_rate_percent", 0)

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

    # Test Groups
    test_groups = report.get("test_groups", {})
    if test_groups:
        html += """
<h3>Test Groups Breakdown</h3>
<table>
<thead><tr>
  <th>Category</th>
  <th>Total</th>
  <th>Passed</th>
  <th>Failed</th>
  <th>Expected Fail</th>
  <th>Status</th>
</tr></thead>
<tbody>
"""
        for category, data in test_groups.items():
            status_badge = data.get("status", "UNKNOWN")
            badge_class = "pass" if "PASS" in status_badge else "fail" if "FAIL" in status_badge else "xfail"
            html += f"""<tr>
  <td><strong>{category.title()}</strong></td>
  <td>{data.get("total", 0)}</td>
  <td class="pass"><strong>{data.get("passed", 0)}</strong></td>
  <td class="fail"><strong>{data.get("failed", 0)}</strong></td>
  <td class="xfail">{data.get("xfailed", 0)}</td>
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
        if per_phase:
            html += """
<div id="metrics-phase" class="tab-content active">
<table>
<thead><tr>
  <th>Phase</th>
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

                total_input += input_tokens
                total_output += output_tokens
                total_cache_creation += cache_creation
                total_cache_read += cache_read
                total_messages += messages
                total_invocations += invocations

                html += f"""<tr>
  <td><strong>{phase}</strong></td>
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

    # Environment
    environment = report.get("environment", "N/A")
    framework = report.get("framework", "N/A")
    browser = report.get("browser", "N/A")
    execution_start = report.get("execution_start_time", "N/A")
    execution_end = report.get("execution_end_time", "N/A")
    duration = report.get("duration_seconds", 0)

    html += f"""
<h2>Environment & Execution</h2>
<table>
<tr><td><strong>Environment</strong></td><td>{environment}</td></tr>
<tr><td><strong>Framework</strong></td><td>{framework}</td></tr>
<tr><td><strong>Browser</strong></td><td>{browser}</td></tr>
<tr><td><strong>Execution Start</strong></td><td>{execution_start}</td></tr>
<tr><td><strong>Execution End</strong></td><td>{execution_end}</td></tr>
<tr><td><strong>Duration</strong></td><td>{duration:.2f} seconds</td></tr>
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
    report = load_json(REPORT_JSON)

    if not report:
        print(f"[ERROR] {REPORT_JSON} not found or empty")
        return 1

    story_id = str(report.get("story_id") or "general")
    metrics_json = metrics_json_for_story(story_id)
    metrics = load_json(metrics_json)

    if not metrics:
        print(f"[WARN] {metrics_json} not found or empty")

    html = generate_html(report, metrics)

    # Write into a per-story folder under artifacts/reports/<story_id>/stlc-report.html
    output_html = ROOT / "artifacts" / story_id / "reports" / "stlc-report.html"

    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_html.write_text(html, encoding="utf-8")

    print(f"[OK] HTML report generated: {output_html}")
    return 0


if __name__ == "__main__":
    exit(main())