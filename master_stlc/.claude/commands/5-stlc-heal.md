---
description: Step 5 (optional): re-run self-healing on remaining AUTOMATION_FAILURE items. IMPORTANT: Invoke ONLY when the user explicitly types this slash command. NEVER auto-run because a message merely contains a user story or requirement text — in that case, ask the user whether they want to start the STLC pipeline.
---

# stlc-heal Command

## Purpose
Run or re-run self-healing on failures classified as AUTOMATION_FAILURE from the most recent execution.

## Prerequisite
`artifacts/execution/failure-analysis.md` must exist with at least one AUTOMATION_FAILURE record.

## Phases executed
1. Read failure analysis → identify AUTOMATION_FAILURE items only
2. Self-Healing → apply bounded repairs, record changes
3. Rerun → execute repaired tests, record HEALED / STILL_FAILING
4. Update `artifacts/self-healing/self-healing-report.md`

## Usage
```
/5-stlc-heal
```

## Output
- Updated self-healing report
- Rerun results per healed test

## Limits
- Runs at most `max_self_healing_iterations` times (from `stlc-config.yaml`).
- Does not attempt to heal APPLICATION_FAILURE, TEST_DATA_FAILURE, or ENVIRONMENT_FAILURE.
- Stops and reports if no safe fix can be found.

## Safety
- Never weakens an assertion to make a test pass.
- Never changes expected business behavior.
- Records every change before applying it.
- Stops if the change would alter application source code.
