# Execution Report: COD-7

## Execution Summary
- Date: 2026-10-30T07:07:41Z (start) — 2026-10-30T07:14:59Z (end)
- Scope: all (46 automated tests + 5 `test.skip()` tests = 51 total)
- Framework: Playwright (chromium, headless, 1 worker)
- Environment: Node v24.15.0, npm v11.12.1, Windows 11
- Command: `npx playwright test --reporter=list,json` (run from `product_release_dashboard/automation`)
- Total: 51
- Passed: 0
- Failed: 46
- Skipped: 5
- Duration: 437.88s (~7m 18s)
- Exit status: all 46 executed tests reported `unexpected` (failed); 0 `expected` (passed); 5 `skipped`

## Pre-execution setup (all succeeded)
1. `cd product_release_dashboard/automation`
2. `npm install` → added 4 packages, 0 vulnerabilities
3. `npx playwright install chromium` → completed, no errors (browser already present/installed cleanly)
4. `npx playwright test --reporter=list,json` → ran to completion, exit observed via stats block (not an ENVIRONMENT_FAILURE — Node/npm/npx all present and functioning)

## Root Cause of Failures (applies to all 46 failed tests)
Every failing test calls the shared helper `clearAndSeedStorage(page, items)` (in `tests/helpers/storage.ts`), which does:
```ts
await page.goto('/');
```
`playwright.config.ts` sets `baseURL` to `file://<...>/product_release_dashboard/index.html` (a direct path to a **file**, not a directory). When Playwright resolves the relative URL `'/'` against a `file://` base URL that points at a specific file, the WHATWG URL algorithm collapses it to the **filesystem root**, not the intended HTML file. Verified independently with Node:
```
$ node -e "console.log(new URL('/', 'file:///C:/.../product_release_dashboard/index.html').toString())"
file:///C:/
```
So every test instead navigates to `file:///C:/` (the root of the C: drive) instead of the Release Notes Dashboard app. The app's DOM (`.release-card`, `#submit-button`, `#product`, etc.) never loads, so every assertion against application elements fails — either immediately (`toBeGreaterThan(0)` on a 0-element locator) or after the default timeout waiting for an element that will never appear.

This is a defect in the **test automation helper code**, not the application under test (`product_release_dashboard/index.html`/`script.js` were never actually exercised). Classification: **AUTOMATION_FAILURE** (test infrastructure bug in `clearAndSeedStorage`'s use of `page.goto('/')` against a file-based `baseURL`). Per project safety rules, no fix was applied — this report only documents findings; a fix requires an explicit approval/self-healing pass (self-healing is permitted for `AUTOMATION_FAILURE`).

No application defects can be confirmed or ruled out from this run, since the application was never reached.

## Passed Tests
None. 0 of 46 executed tests passed.

## Failed Tests (46)
All failures share the same root cause described above. Two underlying error signatures were observed:

**Signature A** — tests that click an Edit button via the `clickEditOnCard` helper:
```
TimeoutError: locator.click: Timeout 10000ms exceeded.
Call log:
  - waiting for locator('.release-card').filter({ hasText: '<product>' }).locator('.edit-btn')
```

**Signature B** — tests that assert card/element presence directly:
```
Error: expect(locator).toHaveCount(expected) failed
Locator:  locator('.release-card')
Expected: <N>
Received: 0
```
(TC-001 failed fastest, 145ms, via `expect(count).toBeGreaterThan(0)`; TC-051 failed via `expect(locator('#submit-button')).toHaveText(...)` — "element(s) not found".)

| TC-ID | Test Title | Error Signature | Duration |
|---|---|---|---|
| TC-001 | Edit button is visible on every rendered release card | B (count 0, `toBeGreaterThan(0)` fails) | 145ms |
| TC-002 | Clicking Edit pre-fills all 7 form fields with the release data | A | 10.2s |
| TC-003 | isBreaking checkbox pre-fills as checked for a breaking release | A | 10.2s |
| TC-004 | isBreaking checkbox pre-fills as unchecked for a non-breaking release | A | 10.1s |
| TC-005 | Submit button label changes to "Update Release Note" in edit mode | A | 10.2s |
| TC-006 | Cancel Edit button becomes visible when edit mode is active | A | 10.2s |
| TC-007 | Save updates the specific release by its id | A | 10.2s |
| TC-008 | Save does not create a duplicate entry | A | 5.1s |
| TC-009 | Save does not modify any other release entries | A | 10.2s |
| TC-010 | Updated release is persisted to localStorage after Save | A | 10.2s |
| TC-011 | Release list re-renders immediately with updated values after Save | A | 10.1s |
| TC-012 | Cancel discards in-progress changes and rendered list is unchanged | A | 10.1s |
| TC-013 | Cancel leaves localStorage unchanged | A | 10.1s |
| TC-014 | All active filters remain applied after Save | A | 10.2s |
| TC-015 | All active filters remain applied after Cancel | A | 10.2s |
| TC-016 | Edit operates correctly on the first card in the list | A | 5.2s |
| TC-017 | Edit operates correctly on the last card in the list | A | 5.2s |
| TC-018 | Edit operates correctly on a middle card in the list | A | 5.1s |
| TC-019 | Cancel without modifying any field leaves list and localStorage unchanged | A | 10.2s |
| TC-020 | Save with teamName cleared shows validation error and preserves edit state | A | 10.2s |
| TC-021 | Save with title cleared shows validation error | A | 10.2s |
| TC-022 | Save with product cleared shows validation error | A | 10.2s |
| TC-023 | Save with version cleared shows validation error | A | 10.2s |
| TC-024 | Save with releaseDate cleared shows validation error | A | 10.2s |
| TC-026 | Clicking Edit on card B while card A is in edit mode replaces form with card B values | A | 10.2s |
| TC-027 | Cancel after a validation failure exits edit mode cleanly | A | 10.2s |
| TC-028 | Edit all 7 fields then Save persists every change | A | 10.4s |
| TC-029 | Edit exactly one field; all others remain intact | A | 10.2s |
| TC-030 | Edit with teamName cleared shows validation error and does not save | A | 10.2s |
| TC-031 | Edit with minimum single-character values in all mandatory fields succeeds | A | 10.2s |
| TC-032 | Edit then Cancel then re-Edit shows original unchanged values | A | 10.1s |
| TC-033 | Edit card A then Cancel then Edit card B shows only card B values | A | 10.1s |
| TC-036 | Toggle isBreaking from true to false and Save persists the change | A | 10.2s |
| TC-037 | Toggle isBreaking from false to true and Save persists the change | A | 10.2s |
| TC-038 | Edit operates correctly when the list contains exactly one entry | B | 5.2s |
| TC-039 | Edit with no filters active leaves filter controls cleared after Save | B | 5.2s |
| TC-040 | Create new release still works after Edit and Save | B | 5.2s |
| TC-041 | Create new release still works after Edit and Cancel | B | 5.2s |
| TC-042 | Delete a different release still works after Edit and Save | B | 5.2s |
| TC-043 | Deleting the release currently in edit mode resets edit state | A | 10.2s |
| TC-044 | Product filter functions correctly before and after Edit and Save | A | 10.2s |
| TC-045 | Breaking-change filter functions correctly after Edit and Save | A | 10.2s |
| TC-046 | Keyword search filter functions correctly after Edit and Save | A | 10.2s |
| TC-047 | Multi-filter combination persists correctly after Edit and Save | A | 10.2s |
| TC-048 | Edited values persist after a full page reload | A | 10.2s |
| TC-051 | Form in create mode creates a new entry and does not trigger an update | B (`#submit-button` not found) | 5.2s |

## Skipped Tests (5)
All five are explicit `test.skip()` placeholders tagged `@manual_only` (deliberately excluded from automation per the test plan — not an execution defect):

| TC-ID | Reason |
|---|---|
| TC-025 | `@manual_only` — Calling `startEdit` with a non-existent id does not crash the application |
| TC-034 | `@manual_only` — Edit title/description with 500-char text does not crash |
| TC-035 | `@manual_only` — Edit text fields with special characters are stored and rendered safely |
| TC-049 | `@manual_only` — Export CSV contains updated values after Edit and Save |
| TC-050 | `@manual_only` — Importing JSON while in edit mode resets edit state |

## Raw Output (key excerpts)

Setup:
```
added 4 packages, and audited 5 packages in 4s
found 0 vulnerabilities
```

List reporter header and final stats block (from Playwright JSON reporter):
```
Running 51 tests using 1 worker
...
"stats": {
  "startTime": "2026-10-30T07:07:41.426Z",
  "duration": 436881.261,
  "expected": 0,
  "skipped": 5,
  "unexpected": 46,
  "flaky": 0
}
```

Representative failure (Signature A):
```
1) [chromium] › tests\boundary\edit-boundary.spec.ts:28:7 › Boundary scenarios (TC-028 to TC-039) › TC-028 ... Edit all 7 fields then Save persists every change

  TimeoutError: locator.click: Timeout 10000ms exceeded.
  Call log:
    - waiting for locator('.release-card').filter({ hasText: 'Billing API' }).locator('.edit-btn')

    17 | async function clickEditOnCard(page: any, productSubstring: string) {
    18 |   const card = page.locator('.release-card').filter({ hasText: productSubstring });
  > 19 |   await card.locator('.edit-btn').click();
       |                                   ^
    at clickEditOnCard (tests\boundary\edit-boundary.spec.ts:19:35)
```

Representative failure (Signature B):
```
Error: expect(locator).toHaveCount(expected) failed
Locator:  locator('.release-card')
Expected: 2
Received: 0
Timeout:  5000ms
  76 |     await expect(page.locator('.release-card')).toHaveCount(2);
     |                                                 ^
    at tests\regression\edit-regression.spec.ts:76:49
```

Full console + JSON reporter output archived at:
`artifacts/COD-7/execution/raw-results/20261030T070741Z/playwright-console-and-json.log`

## Status
**FAIL** — 0/46 executable tests passed; 1 shared root cause (AUTOMATION_FAILURE in `page.goto('/')` helper usage against a `file://` base URL that points at a specific file). No code was modified during this execution run, per safety rules. Recommend routing to self-healing (automation-only) or manual review/approval before any fix to `tests/helpers/storage.ts` or `playwright.config.ts` baseURL handling.
