# STLC Orchestrator

## Purpose
This document defines the orchestrator for the Generic Claude STLC project.

## Pipeline
1. Repository discovery
2. Requirement clarification
3. Existing functionality and test detection
4. Classification and impact analysis
5. Test plan generation
6. Manual test generation
7. Test review
8. Automation framework detection
9. Automation generation
10. Automation review
11. User-approved execution scope selection
12. Test execution
13. Failure analysis
14. Self-healing if safe
15. Rerun affected tests
16. Defect analysis
17. Optional defect creation
18. Final report and metrics

## Rules
- Keep the orchestrator generic and repository-agnostic.
- Keep framework-specific logic inside skills, not in the orchestrator.
- Stop at approval gates whenever testing or code changes are required.
- Record all phases in state and artifacts.
- Maintain traceability between story, requirement, test, automation, execution, and defect.

## State handling
- Persist state under `artifacts/state/stlc-state.json`.
- Resume by reading completed phases and continuing from the next phase.
- Prevent duplicate artifacts and repeated expensive work.

## Safety
- No unapproved modification of existing tests or automation.
- No application code changes without approval.
- No dependency installation without permission.
- No destructive commands unless explicitly approved.
- No weakening of assertions or skipping failing tests.
