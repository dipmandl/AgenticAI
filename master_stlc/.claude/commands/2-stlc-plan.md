---
description: Step 2 (slice): planning phases only — discovery through test plan. IMPORTANT: Invoke ONLY when the user explicitly types this slash command. NEVER auto-run because a message merely contains a user story or requirement text — in that case, ask the user whether they want to start the STLC pipeline.
---

# stlc-plan Command

## Purpose
Run only the planning phases of the STLC pipeline and stop before test generation.
Use this to review and approve the test plan before committing to test and automation creation.

## Phases executed
1. Repository Discovery → `artifacts/repository/repository-discovery.md`
2. Requirement Analysis → `artifacts/requirements/requirement-analysis.md`
3. Impact Analysis → `artifacts/test-planning/impact-analysis.md`
4. Test Plan → `artifacts/test-planning/test-plan.md`

## Stops after
Test plan generation. Awaits user approval before proceeding.

## Usage
```
/2-stlc-plan <story or requirement text>
```

## Output
- Planning artifacts in `artifacts/`
- Summary of proposed test scenarios (positive, negative, boundary, regression)
- Prompt: "Approve this plan to continue with test generation?"

## Safety
- No test files created.
- No automation generated.
- No existing files modified.
