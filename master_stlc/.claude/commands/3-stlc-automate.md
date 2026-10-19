---
description: Step 3 (slice): manual test generation through automation review. IMPORTANT: Invoke ONLY when the user explicitly types this slash command. NEVER auto-run because a message merely contains a user story or requirement text — in that case, ask the user whether they want to start the STLC pipeline.
---

# stlc-automate Command

## Purpose
Run test generation and automation phases. Requires an approved test plan to exist.
Stops before execution and awaits user confirmation of scope.

## Prerequisite
`artifacts/test-planning/test-plan.md` must exist from a prior `stlc-plan` or `stlc` run.

## Phases executed
1. Manual Test Generation → `artifacts/test-cases/test-case-inventory.md`
2. Test Case Review → `artifacts/reviews/test-case-review.md`
3. Framework Selection → `artifacts/automation/framework-selection.md`
4. Automation Generation → automation files + `artifacts/traceability/traceability-matrix.md`
5. Automation Review → `artifacts/reviews/automation-review.md`

## Stops after
Automation review. Awaits user confirmation of execution scope before running tests.

## Usage
```
/3-stlc-automate
```

## Output
- Manual test cases and Gherkin scenarios
- Automation code in the selected framework
- Review report with approval status
- Traceability matrix

## Safety
- Requires test plan artifact to exist.
- Does not modify existing tests or automation without permission.
- Does not execute tests.
- Asks for user confirmation before creating dependency files.
