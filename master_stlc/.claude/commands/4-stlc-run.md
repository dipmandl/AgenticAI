---
description: Step 4 (slice): execution, failure analysis, self-healing, defect analysis. IMPORTANT: Invoke ONLY when the user explicitly types this slash command. NEVER auto-run because a message merely contains a user story or requirement text — in that case, ask the user whether they want to start the STLC pipeline.
---

# stlc-run Command

## Purpose
Execute approved automation and capture results. Requires automation to exist from a prior run.

## Prerequisite
`artifacts/automation/framework-selection.md` and automation files must exist.

## Phases executed
1. Execution → `artifacts/execution/execution-summary.md` + `execution-metadata.json`
2. Failure Analysis → `artifacts/execution/failure-analysis.md`
3. Self-Healing (if AUTOMATION_FAILURE found) → `artifacts/self-healing/self-healing-report.md`
4. Defect Analysis (if APPLICATION_FAILURE found) → `artifacts/defects/DEF-NNN.md`

## Usage
```
/4-stlc-run [scope]
```

Scope options: `smoke`, `regression`, `impacted`, `all`, or a comma-separated list of TC-IDs.
If scope is omitted, the user is prompted to confirm before execution starts.

## Output
- Execution summary with pass/fail/skip counts
- Failure classification per failed test
- Self-healing report if applicable
- Defect files for functional failures

## Safety
- Requires explicit scope confirmation when `require_user_scope: true`.
- Never runs destructive commands without approval.
- Never weakens assertions or skips tests.
- Stops after `max_self_healing_iterations` without creating infinite retry loops.
