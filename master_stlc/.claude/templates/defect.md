# Defect Template

Use this template for `artifacts/defects/DEF-NNN.md`.

---

# DEF-NNN: <Short descriptive title>

| Field | Value |
|-------|-------|
| Defect ID | DEF-NNN |
| TC-ID | TC-NNN |
| REQ-ID | REQ-NNN |
| Severity | CRITICAL / HIGH / MEDIUM / LOW |
| Status | OPEN |
| Environment | |
| Detected | <ISO timestamp> |
| Pipeline ID | |
| Story ID | |

## Summary
One sentence describing the defect.

## Steps to Reproduce
1. <Step 1>
2. <Step 2>
3. <Step 3>

## Expected Result
<Derived from acceptance criteria — quote the criterion>

## Actual Result
<What the application actually does — from log or screenshot evidence>

## Evidence
- Log excerpt:
  ```
  <≤10 lines from execution log>
  ```
- Screenshot: `artifacts/execution/raw-results/<timestamp>/screenshots/<name>.png`
- API response (if applicable):
  ```json
  {}
  ```

## Impacted Area
<Module, service, or component name>

## External Issue Reference
<Jira / GitHub Issue / ADO ticket ID — if created>

## Notes
<Any additional context — regression risk, related requirements>
