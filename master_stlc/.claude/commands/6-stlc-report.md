---
description: Step 6 (slice): assemble final report and metrics from artifacts. IMPORTANT: Invoke ONLY when the user explicitly types this slash command. NEVER auto-run because a message merely contains a user story or requirement text — in that case, ask the user whether they want to start the STLC pipeline.
---

# stlc-report Command

## Purpose
Assemble the final STLC report from all completed phase artifacts without re-running any pipeline phases.

## Prerequisite
At least the following artifacts must exist:
- `artifacts/requirements/requirement-analysis.md`
- `artifacts/test-planning/test-plan.md`
- `artifacts/test-cases/test-case-inventory.md`

Execution and self-healing artifacts are included if present; missing ones are noted in the report.

## Phases executed
1. Reporting → `artifacts/reports/final-stlc-report.md`
2. JSON summary → `artifacts/reports/final-stlc-report.json`
3. Metrics → run `python .claude\scripts\token-usage.py` to compute per-phase and per-agent token usage from Claude Code transcripts → `artifacts/<story_id>/metrics/agent-metrics.md` + `agent-metrics.json`

## Usage
```
/6-stlc-report
```

## Output
- `artifacts/reports/final-stlc-report.md` — full STLC narrative report
- `artifacts/reports/final-stlc-report.json` — machine-readable summary
- `artifacts/<story_id>/metrics/agent-metrics.md` — per-agent metrics
- `artifacts/<story_id>/metrics/agent-metrics.json` — machine-readable metrics
- `artifacts/<story_id>/reports/stlc-report.html` — interactive HTML report

## Safety
- Read-only across all existing artifacts.
- Does not re-run any pipeline phase.
- Does not modify test files, automation, or application code.
- Masks secrets detected in log excerpts.
