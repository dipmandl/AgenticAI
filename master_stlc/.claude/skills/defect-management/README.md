# Defect Management Skill

## Purpose
Guide structured defect creation from APPLICATION_FAILURE evidence.

## When to create a defect
- Failure is classified as `APPLICATION_FAILURE` by the failure analysis agent.
- Evidence confirms the application does not meet an acceptance criterion.

## Defect severity classification
| Severity | Criteria |
|----------|----------|
| CRITICAL | Blocks core functionality; no workaround |
| HIGH | Major feature broken; workaround exists but poor UX |
| MEDIUM | Feature partially works; workaround available |
| LOW | Minor UI or cosmetic issue |

## Required defect fields
| Field | Source |
|-------|--------|
| Defect ID | Sequential DEF-NNN |
| TC-ID | From failure analysis |
| REQ-ID | From requirement analysis |
| Severity | Assessed from business impact |
| Steps to reproduce | From test scenario Given/When steps |
| Expected result | From acceptance criteria |
| Actual result | From assertion error and logs |
| Evidence | Log snippet, screenshot path |
| Environment | From execution metadata |
| Detected timestamp | From execution metadata |

## Defect ID assignment
Read existing files in `artifacts/defects/` to find the next available DEF-NNN.
Never overwrite existing defect files.

## External defect system integration
If `create_external_defects: true` in `stlc-config.yaml`:
1. Ask the user to confirm before creating in the external system.
2. Record the external issue reference (e.g., Jira ticket ID) in the local defect file.
3. Supported external systems are configured separately — this skill is system-agnostic.

## What a defect is NOT
- A defect is not a self-healing report.
- A defect is not an automation code fix.
- A defect should document a business behavior violation, not a test code problem.
