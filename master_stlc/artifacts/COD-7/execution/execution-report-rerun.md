# COD-7 — Playwright Automation Re-run Report (Post Self-Healing)

## Re-run Execution Summary

| Field | Value |
|---|---|
| Timestamp (UTC) | 2026-10-30T09:52:21Z |
| Command | `npx playwright test --reporter=list,json` |
| Working directory | `product_release_dashboard/automation` |
| Framework | Playwright (chromium, headless) |
| Total tests | 51 |
| Passed | 46 |
| Failed | 0 |
| Skipped | 5 (`@manual_only`) |
| Duration | 24.5s (reporter) / 27s (wall clock) |
| Exit code | 0 |

Fixes applied prior to this run (not re-applied here, execution only):
1. `tests/helpers/storage.ts` — `page.goto('/')` → `page.goto('')` (file:// URL resolution fix)
2. `tests/positive/edit-positive.spec.ts` TC-015 — search term `'v1'` → `'export'` (matches `DEFAULT_SEED`)

## Passed Tests (46)

| TC-ID | Title |
|---|---|
| TC-001 | Edit button is visible on every rendered release card |
| TC-002 | Clicking Edit pre-fills all 7 form fields with the release data |
| TC-003 | isBreaking checkbox pre-fills as checked for a breaking release |
| TC-004 | isBreaking checkbox pre-fills as unchecked for a non-breaking release |
| TC-005 | Submit button label changes to "Update Release Note" in edit mode |
| TC-006 | Cancel Edit button becomes visible when edit mode is active |
| TC-007 | Save updates the specific release by its id |
| TC-008 | Save does not create a duplicate entry |
| TC-009 | Save does not modify any other release entries |
| TC-010 | Updated release is persisted to localStorage after Save |
| TC-011 | Release list re-renders immediately with updated values after Save |
| TC-012 | Cancel discards in-progress changes and rendered list is unchanged |
| TC-013 | Cancel leaves localStorage unchanged |
| TC-014 | All active filters remain applied after Save |
| TC-015 | All active filters remain applied after Cancel (self-healed: search term fix) |
| TC-016 | Edit operates correctly on the first card in the list |
| TC-017 | Edit operates correctly on the last card in the list |
| TC-018 | Edit operates correctly on a middle card in the list |
| TC-019 | Cancel without modifying any field leaves list and localStorage unchanged |
| TC-020 | Save with teamName cleared shows validation error and preserves edit state |
| TC-021 | Save with title cleared shows validation error |
| TC-022 | Save with product cleared shows validation error |
| TC-023 | Save with version cleared shows validation error |
| TC-024 | Save with releaseDate cleared shows validation error |
| TC-026 | Clicking Edit on card B while card A is in edit mode replaces form with card B values |
| TC-027 | Cancel after a validation failure exits edit mode cleanly |
| TC-028 | Edit all 7 fields then Save persists every change |
| TC-029 | Edit exactly one field; all others remain intact |
| TC-030 | Edit with teamName cleared shows validation error and does not save |
| TC-031 | Edit with minimum single-character values in all mandatory fields succeeds |
| TC-032 | Edit then Cancel then re-Edit shows original unchanged values |
| TC-033 | Edit card A then Cancel then Edit card B shows only card B values |
| TC-036 | Toggle isBreaking from true to false and Save persists the change |
| TC-037 | Toggle isBreaking from false to true and Save persists the change |
| TC-038 | Edit operates correctly when the list contains exactly one entry |
| TC-039 | Edit with no filters active leaves filter controls cleared after Save |
| TC-040 | Create new release still works after Edit and Save |
| TC-041 | Create new release still works after Edit and Cancel |
| TC-042 | Delete a different release still works after Edit and Save |
| TC-043 | Deleting the release currently in edit mode resets edit state |
| TC-044 | Product filter functions correctly before and after Edit and Save |
| TC-045 | Breaking-change filter functions correctly after Edit and Save |
| TC-046 | Keyword search filter functions correctly after Edit and Save |
| TC-047 | Multi-filter combination persists correctly after Edit and Save |
| TC-048 | Edited values persist after a full page reload |
| TC-051 | Form in create mode creates a new entry and does not trigger an update |

## Failed Tests

None. All 46 executed tests passed.

## Skipped Tests (5, `@manual_only`)

| TC-ID | Reason |
|---|---|
| TC-025 | Calling startEdit with a non-existent id does not crash the application — `@manual_only` |
| TC-034 | Edit title/description with 500-char text does not crash — `@manual_only` |
| TC-035 | Edit text fields with special characters are stored and rendered safely — `@manual_only` |
| TC-049 | Export CSV contains updated values after Edit and Save — `@manual_only` |
| TC-050 | Importing JSON while in edit mode resets edit state — `@manual_only` |

## Comparison to Previous Run

| Metric | Before self-healing (2026-10-30T07:07:41Z) | After self-healing (2026-10-30T09:52:21Z) |
|---|---|---|
| Passed | 0 | 46 |
| Failed | 46 | 0 |
| Skipped | 5 | 5 |
| Total | 51 | 51 |
| Duration | 437.88s | ~24.5s (reporter) |

Root cause of the prior 46 failures: `tests/helpers/storage.ts` used `page.goto('/')`, which failed to resolve against the `file://` base URL used by this static dashboard, causing every test that relied on the shared storage/navigation helper to fail at setup. TC-015 additionally had an unrelated `AUTOMATION_FAILURE` (wrong search term in the test itself, not the app). Both fixes have fully resolved the failures with zero regressions introduced.

## Raw Output (key sections)

```
Running 51 tests using 1 worker

  ✓   1 [chromium] › tests\boundary\edit-boundary.spec.ts:28:7 › ... TC-028 ... (457ms)
  ...
  -   7 [chromium] › tests\boundary\edit-boundary.spec.ts:160:8 › ... TC-034 @manual_only ...
  -   8 [chromium] › tests\boundary\edit-boundary.spec.ts:166:8 › ... TC-035 @manual_only ...
  ...
  -  19 [chromium] › tests\negative\edit-negative.spec.ts:138:8 › ... TC-025 @manual_only ...
  ...
  ✓  36 [chromium] › tests\positive\edit-positive.spec.ts:241:7 › ... TC-015 @REQ-011 @positive @high All active filters remain applied after Cancel (880ms)
  ...
  -  49 [chromium] › tests\regression\edit-regression.spec.ts:311:8 › ... TC-049 @manual_only ...
  -  50 [chromium] › tests\regression\edit-regression.spec.ts:317:8 › ... TC-050 @manual_only ...
  ✓  51 [chromium] › tests\regression\edit-regression.spec.ts:322:7 › ... TC-051 ... (325ms)

  5 skipped
  46 passed (24.5s)
```

JSON reporter stats block:
```json
"stats": {
  "startTime": "2026-10-30T09:53:36.575Z",
  "duration": 24466.927,
  "expected": 46,
  "skipped": 5,
  "unexpected": 0,
  "flaky": 0
}
```

Full raw console output and stderr are stored at:
`artifacts/COD-7/execution/raw-results/20261030T095221Z/console-output.log`
`artifacts/COD-7/execution/raw-results/20261030T095221Z/stderr.log` (empty)
`artifacts/COD-7/execution/raw-results/20261030T095221Z/exit-code.txt`
