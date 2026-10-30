# Automation Suite: COD-7 — Edit Existing Release Note

**Framework**: Playwright (TypeScript)
**Story**: COD-7
**Total automated**: 46 of 51 TCs
**Skipped (manual_only)**: TC-025, TC-034, TC-035, TC-049, TC-050

---

## Generated Files

| File | Purpose | TC Range |
|------|---------|----------|
| `product_release_dashboard/automation/package.json` | npm config and run scripts | — |
| `product_release_dashboard/automation/playwright.config.ts` | Playwright configuration with `file://` baseURL | — |
| `product_release_dashboard/automation/tests/fixtures/seed-data.ts` | Typed seed objects matching `script.js:seedData()` | — |
| `product_release_dashboard/automation/tests/helpers/storage.ts` | localStorage read/write helpers | — |
| `product_release_dashboard/automation/tests/positive/edit-positive.spec.ts` | Positive scenarios | TC-001 to TC-018 |
| `product_release_dashboard/automation/tests/negative/edit-negative.spec.ts` | Negative scenarios | TC-019 to TC-027 |
| `product_release_dashboard/automation/tests/boundary/edit-boundary.spec.ts` | Boundary scenarios | TC-028 to TC-039 |
| `product_release_dashboard/automation/tests/regression/edit-regression.spec.ts` | Regression scenarios | TC-040 to TC-051 |

---

## TC-NNN to Spec File Mapping

| TC-ID | Spec File | Test Title | Status |
|-------|-----------|------------|--------|
| TC-001 | positive/edit-positive.spec.ts | TC-001 @REQ-001 @positive @high Edit button is visible on every rendered release card | AUTOMATED |
| TC-002 | positive/edit-positive.spec.ts | TC-002 @REQ-002 @positive @critical Clicking Edit pre-fills all 7 form fields with the release data | AUTOMATED |
| TC-003 | positive/edit-positive.spec.ts | TC-003 @REQ-002 @positive @high isBreaking checkbox pre-fills as checked for a breaking release | AUTOMATED |
| TC-004 | positive/edit-positive.spec.ts | TC-004 @REQ-002 @positive @high isBreaking checkbox pre-fills as unchecked for a non-breaking release | AUTOMATED |
| TC-005 | positive/edit-positive.spec.ts | TC-005 @REQ-004 @positive @high Submit button label changes to "Update Release Note" in edit mode | AUTOMATED |
| TC-006 | positive/edit-positive.spec.ts | TC-006 @REQ-005 @positive @high Cancel Edit button becomes visible when edit mode is active | AUTOMATED |
| TC-007 | positive/edit-positive.spec.ts | TC-007 @REQ-006 @positive @critical Save updates the specific release by its id | AUTOMATED |
| TC-008 | positive/edit-positive.spec.ts | TC-008 @REQ-006 @positive @critical Save does not create a duplicate entry | AUTOMATED |
| TC-009 | positive/edit-positive.spec.ts | TC-009 @REQ-006 @positive @high Save does not modify any other release entries | AUTOMATED |
| TC-010 | positive/edit-positive.spec.ts | TC-010 @REQ-007 @positive @critical Updated release is persisted to localStorage after Save | AUTOMATED |
| TC-011 | positive/edit-positive.spec.ts | TC-011 @REQ-008 @positive @high Release list re-renders immediately with updated values after Save | AUTOMATED |
| TC-012 | positive/edit-positive.spec.ts | TC-012 @REQ-009 @positive @critical Cancel discards in-progress changes and rendered list is unchanged | AUTOMATED |
| TC-013 | positive/edit-positive.spec.ts | TC-013 @REQ-009 @positive @high Cancel leaves localStorage unchanged | AUTOMATED |
| TC-014 | positive/edit-positive.spec.ts | TC-014 @REQ-010 @positive @critical All active filters remain applied after Save | AUTOMATED |
| TC-015 | positive/edit-positive.spec.ts | TC-015 @REQ-011 @positive @high All active filters remain applied after Cancel | AUTOMATED |
| TC-016 | positive/edit-positive.spec.ts | TC-016 @REQ-012 @positive @medium Edit operates correctly on the first card in the list | AUTOMATED |
| TC-017 | positive/edit-positive.spec.ts | TC-017 @REQ-012 @positive @medium Edit operates correctly on the last card in the list | AUTOMATED |
| TC-018 | positive/edit-positive.spec.ts | TC-018 @REQ-012 @positive @medium Edit operates correctly on a middle card in the list | AUTOMATED |
| TC-019 | negative/edit-negative.spec.ts | TC-019 @REQ-009 @negative @high Cancel without modifying any field leaves list and localStorage unchanged | AUTOMATED |
| TC-020 | negative/edit-negative.spec.ts | TC-020 @REQ-004 @negative @high Save with teamName cleared shows validation error and preserves edit state | AUTOMATED |
| TC-021 | negative/edit-negative.spec.ts | TC-021 @REQ-004 @negative @high Save with title cleared shows validation error | AUTOMATED |
| TC-022 | negative/edit-negative.spec.ts | TC-022 @REQ-004 @negative @high Save with product cleared shows validation error | AUTOMATED |
| TC-023 | negative/edit-negative.spec.ts | TC-023 @REQ-004 @negative @high Save with version cleared shows validation error | AUTOMATED |
| TC-024 | negative/edit-negative.spec.ts | TC-024 @REQ-004 @negative @high Save with releaseDate cleared shows validation error | AUTOMATED |
| TC-025 | negative/edit-negative.spec.ts | TC-025 @REQ-006 @negative @high @manual_only Calling startEdit with non-existent id | SKIPPED — manual_only |
| TC-026 | negative/edit-negative.spec.ts | TC-026 @REQ-002 @negative @medium Clicking Edit on card B while card A is in edit mode replaces form with card B values | AUTOMATED |
| TC-027 | negative/edit-negative.spec.ts | TC-027 @REQ-005 @REQ-009 @negative @high Cancel after a validation failure exits edit mode cleanly | AUTOMATED |
| TC-028 | boundary/edit-boundary.spec.ts | TC-028 @REQ-002 @REQ-006 @boundary @high Edit all 7 fields then Save persists every change | AUTOMATED |
| TC-029 | boundary/edit-boundary.spec.ts | TC-029 @REQ-006 @boundary @medium Edit exactly one field; all others remain intact | AUTOMATED |
| TC-030 | boundary/edit-boundary.spec.ts | TC-030 @REQ-002 @REQ-003 @boundary @medium @regression Edit with teamName cleared shows validation error | AUTOMATED |
| TC-031 | boundary/edit-boundary.spec.ts | TC-031 @REQ-002 @boundary @medium Edit with minimum single-character values in all mandatory fields succeeds | AUTOMATED |
| TC-032 | boundary/edit-boundary.spec.ts | TC-032 @REQ-002 @REQ-009 @boundary @high Edit then Cancel then re-Edit shows original unchanged values | AUTOMATED |
| TC-033 | boundary/edit-boundary.spec.ts | TC-033 @REQ-002 @boundary @high Edit card A then Cancel then Edit card B shows only card B values | AUTOMATED |
| TC-034 | boundary/edit-boundary.spec.ts | TC-034 @REQ-003 @boundary @low @manual_only Edit title/description with 500-char text | SKIPPED — manual_only |
| TC-035 | boundary/edit-boundary.spec.ts | TC-035 @REQ-003 @boundary @low @manual_only Edit text fields with special characters | SKIPPED — manual_only |
| TC-036 | boundary/edit-boundary.spec.ts | TC-036 @REQ-002 @REQ-006 @boundary @high Toggle isBreaking from true to false and Save persists the change | AUTOMATED |
| TC-037 | boundary/edit-boundary.spec.ts | TC-037 @REQ-002 @REQ-006 @boundary @high Toggle isBreaking from false to true and Save persists the change | AUTOMATED |
| TC-038 | boundary/edit-boundary.spec.ts | TC-038 @REQ-012 @boundary @medium Edit operates correctly when the list contains exactly one entry | AUTOMATED |
| TC-039 | boundary/edit-boundary.spec.ts | TC-039 @REQ-010 @boundary @medium Edit with no filters active leaves filter controls cleared after Save | AUTOMATED |
| TC-040 | regression/edit-regression.spec.ts | TC-040 @REQ-006 @regression @high Create new release still works after Edit and Save | AUTOMATED |
| TC-041 | regression/edit-regression.spec.ts | TC-041 @REQ-009 @regression @high Create new release still works after Edit and Cancel | AUTOMATED |
| TC-042 | regression/edit-regression.spec.ts | TC-042 @REQ-006 @regression @high Delete a different release still works after Edit and Save | AUTOMATED |
| TC-043 | regression/edit-regression.spec.ts | TC-043 @REQ-009 @regression @high Deleting the release currently in edit mode resets edit state | AUTOMATED |
| TC-044 | regression/edit-regression.spec.ts | TC-044 @REQ-010 @regression @high Product filter functions correctly before and after Edit and Save | AUTOMATED |
| TC-045 | regression/edit-regression.spec.ts | TC-045 @REQ-010 @regression @high Breaking-change filter functions correctly after Edit and Save | AUTOMATED |
| TC-046 | regression/edit-regression.spec.ts | TC-046 @REQ-010 @regression @high Keyword search filter functions correctly after Edit and Save | AUTOMATED |
| TC-047 | regression/edit-regression.spec.ts | TC-047 @REQ-010 @regression @high Multi-filter combination persists correctly after Edit and Save | AUTOMATED |
| TC-048 | regression/edit-regression.spec.ts | TC-048 @REQ-007 @regression @high Edited values persist after a full page reload | AUTOMATED |
| TC-049 | regression/edit-regression.spec.ts | TC-049 @REQ-007 @regression @medium @manual_only Export CSV contains updated values | SKIPPED — manual_only |
| TC-050 | regression/edit-regression.spec.ts | TC-050 @REQ-009 @regression @medium @manual_only Importing JSON while in edit mode resets edit state | SKIPPED — manual_only |
| TC-051 | regression/edit-regression.spec.ts | TC-051 @REQ-006 @regression @high Form in create mode creates a new entry and does not trigger an update | AUTOMATED |

---

## Skipped Tests (manual_only)

| TC-ID | Reason |
|-------|--------|
| TC-025 | Requires DevTools console — browser automation cannot execute `startEdit()` directly without page evaluation rewriting global state |
| TC-034 | Requires visual observation of crash/truncation behaviour with 500-char strings |
| TC-035 | Requires human verification that `<script>` tag is NOT executed in the browser |
| TC-049 | Requires file download verification — CSV file path is non-deterministic across OS/browser combinations |
| TC-050 | Requires file input trigger (`<input type="file">`) with a real JSON file on disk and dialog confirmation |

---

## Setup Instructions

### Prerequisites
- Node.js 18+
- npm 9+

### Install

```bash
cd product_release_dashboard/automation
npm install
npx playwright install chromium
```

### Run All Tests

```bash
npx playwright test
```

### Run by Suite

```bash
# Positive only
npx playwright test tests/positive/

# Negative only
npx playwright test tests/negative/

# Boundary only
npx playwright test tests/boundary/

# Regression suite (by @regression marker)
npx playwright test --grep @regression

# Single TC by ID
npx playwright test --grep "TC-007"
```

### Run Headed (visible browser)

```bash
npx playwright test --headed
```

### View HTML Report

```bash
npx playwright show-report playwright-report
```

---

## Notes

- `baseURL` is set to `file://<abs-path-to>/product_release_dashboard/index.html` — no HTTP server required.
- Each `beforeEach` calls `clearAndSeedStorage()` which navigates to the page, writes seed data to localStorage, then reloads — ensuring test isolation.
- TC-021 to TC-024 rely on the browser's native `required` attribute validation on `<input>` fields (product, version, title, description, releaseDate). The app also guards these with an explicit early-return check in the submit handler.
- TC-042 and TC-043 use `page.once('dialog', ...)` to auto-accept the `window.confirm` delete dialog.
