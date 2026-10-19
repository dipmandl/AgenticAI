# Execution Report Template

Use this template for `artifacts/execution/execution-summary.md`.

---

# Execution Summary

| Field | Value |
|-------|-------|
| Pipeline ID | |
| Story ID | |
| Execution ID | |
| Start Time | |
| End Time | |
| Duration | |
| Framework | |
| Environment | |
| Scope | |
| Command | |

## Results

| Status | Count |
|--------|-------|
| Total | |
| Passed | |
| Failed | |
| Skipped | |
| Blocked | |
| Retried | |
| Exit Code | |

## Test Results

| TC-ID | Scenario | Status | Duration | Notes |
|-------|----------|--------|----------|-------|

## Failed Tests

| TC-ID | Scenario | Error Summary |
|-------|----------|---------------|

## Evidence
- Raw results: `artifacts/execution/raw-results/<timestamp>/`
- Screenshots: `artifacts/execution/raw-results/<timestamp>/screenshots/`
- Logs: `artifacts/execution/raw-results/<timestamp>/logs/`

## Next Step
- If all passed: proceed to reporting.
- If failures exist: invoke failure analysis agent.
