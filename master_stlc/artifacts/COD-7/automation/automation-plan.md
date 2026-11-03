# Automation Plan

## Metadata

| Field | Value |
|---|---|
| Story ID | COD-7 |
| Story Title | Edit an existing release note |
| Framework | Playwright TypeScript |
| Generated | 2026-11-03 |
| Automation Root | `product_release_dashboard/automation/` |

---

## What Was Generated

### File Structure

```
product_release_dashboard/automation/
  package.json                                          ← project manifest
  playwright.config.ts                                  ← multi-browser config (Chromium, Firefox, WebKit)
  helpers/
    selectors.ts                                        ← centralised DOM selector constants
    localStorage.ts                                     ← typed seed functions SD-001 … SD-009
  tests/
    edit_release_notes/
      positive.spec.ts                                  ← TC-001 to TC-014 (14 automated)
      negative.spec.ts                                  ← TC-015 to TC-021 (7 automated)
      boundary.spec.ts                                  ← TC-023 to TC-029 (7 automated)
      regression.spec.ts                                ← TC-031 to TC-041 (11 automated) *
```

`* TC-042 is MANUAL — not included.`

Total automated test functions: **37**

---

## TC → File Mapping

### positive.spec.ts

| TC ID | Describe Block | Test Title |
|-------|---------------|------------|
| TC-001 | Positive Scenarios / with SD-001 | Edit button present and triggers form pre-fill |
| TC-002 | Positive Scenarios / with SD-001 | Save after modifying product field updates localStorage |
| TC-003 | Positive Scenarios / with SD-001 | Save after modifying version field updates localStorage |
| TC-004 | Positive Scenarios / with SD-001 | Save after modifying title and description updates both fields |
| TC-005 | Positive Scenarios / with SD-001 | Save after modifying releaseDate updates date in localStorage |
| TC-006 | Positive Scenarios / with SD-001 | Save after modifying teamName updates teamName in localStorage |
| TC-007 | Positive Scenarios / with SD-001 | Save with breaking flag toggled from false to true |
| TC-008 | Positive Scenarios / with SD-003 | Save with breaking flag toggled from true to false |
| TC-009 | Positive Scenarios / with SD-001 | Save after modifying all editable fields; id remains unchanged |
| TC-010 | Positive Scenarios / with SD-001 | Cancel after modifying fields discards all changes |
| TC-011 | Positive Scenarios / with SD-001 | Form returns to create mode after Save |
| TC-012 | Positive Scenarios / with SD-001 | Form returns to create mode after Cancel |
| TC-013 | Positive Scenarios / with SD-001 | Active product filter persists after Save |
| TC-014 | Positive Scenarios / with SD-001 | Active search filter persists after Cancel |

### negative.spec.ts

| TC ID | Test Title |
|-------|------------|
| TC-015 | Save blocked when required field product is cleared |
| TC-016 | Save blocked when required field version is cleared |
| TC-017 | Save blocked when required field title is cleared |
| TC-018 | Save blocked when required field description is cleared |
| TC-019 | Save blocked when required field releaseDate is cleared |
| TC-020 | Save blocked with custom error when teamName is cleared |
| TC-021 | Save without modifying any field succeeds and preserves data |

### boundary.spec.ts

| TC ID | Describe Block | Test Title |
|-------|---------------|------------|
| TC-023 | Boundary Scenarios / with SD-002 | Edit the only release note in the list |
| TC-024 | Boundary Scenarios / with SD-001 | Edit with no active filters applied |
| TC-025 | Boundary Scenarios / with SD-008 | Edited entry disappears when it no longer matches active product filter |
| TC-026 | Boundary Scenarios / with SD-003 | Edit entry with isBreaking=true — checkbox pre-fills as checked |
| TC-027 | Boundary Scenarios / with SD-004 | Edit entry with releaseDate "1970-01-01" — date pre-fills correctly |
| TC-028 | Boundary Scenarios / with SD-005 | Edit entry with releaseDate = today's date — date pre-fills correctly |
| TC-029 | Boundary Scenarios / with SD-001 | All three filters active simultaneously — all persist after Save |

### regression.spec.ts

| TC ID | Describe Block | Test Title |
|-------|---------------|------------|
| TC-031 | Regression Scenarios / with SD-001 | Create → Edit → Create: second create adds new entry with blank form |
| TC-032 | Regression Scenarios / with SD-001 | Edit → Save → Delete: delete removes correct entry and list re-renders |
| TC-033 | Regression Scenarios / with SD-001 | Edit → Save → Export: CSV export reflects updated values |
| TC-034 | Regression Scenarios / with SD-001 | Edit → Cancel → Create: create form is blank and adds new entry |
| TC-035 | Regression Scenarios / with SD-001 | Edit one entry — all other entries remain unchanged in localStorage |
| TC-036 | Regression Scenarios / with SD-008 | Edit product value — product filter returns correct results afterward |
| TC-037 | Regression Scenarios / with SD-001 | Edit same entry twice — second edit pre-fills values from first save |
| TC-038 | Regression Scenarios / with SD-009 | Seed data: edit one seed record — other seed record unchanged |
| TC-039 | Regression Scenarios / with SD-001 | Edit entry to isBreaking=true — breaking filter shows it correctly |
| TC-040 | Regression Scenarios / with SD-001 | Edit title to include search keyword — search returns updated entry |
| TC-041 | Regression Scenarios / with SD-001 | Two sequential edits on different entries — both updated independently |

---

## Skipped / Manual-Only

| TC ID | Reason |
|-------|--------|
| TC-022 | MANUAL — filling localStorage to browser quota is unsafe to automate |
| TC-030 | MANUAL — performance judgment requires human observation |
| TC-042 | MANUAL — CSV import uses `window.confirm` + OS file picker |

---

## Key Design Decisions

### Seed Strategy
- All seeds use `page.addInitScript()` which fires before the page's own JavaScript on the first navigation, preventing the app from auto-seeding over the test data.
- SD-005 (`releaseDate = today`) computes the date inside the browser context so there is no timezone mismatch between the Node.js process and the browser.
- SD-009 removes the localStorage key; the app's `loadReleases()` then calls `seedData()` and creates the two default entries (Billing API, Auth Service).

### Entry Selection
- Cards are selected by the `.product-version` text (e.g., `ProductA - v1.0.0`) using Playwright's `filter({ has: locator })` pattern since no `data-id` attribute is present in the rendered HTML.
- All seed entries have deterministic IDs (`test-id-001` … `test-id-005`) so assertions can target specific entries in localStorage without relying on UUID values.

### HTML5 vs Custom Validation (TC-015–TC-020)
- TC-015–TC-019: assert the `required` attribute is present on the field and that localStorage is unchanged after clicking submit (browser validation blocks the JS handler).
- TC-020: assert the custom `#team-name-error` element has the expected message text and that `document.activeElement.id === 'teamName'` (custom JS validation, not HTML5 `required`).

### CSV Export (TC-033)
- Uses `page.waitForEvent('download')` combined with `Promise.all()` to capture the programmatic download triggered by `exportReleasesCsv()`.
- The download file is read with Node.js `fs.readFileSync` after `download.path()`.

### Delete Confirmation (TC-032)
- Uses `page.on('dialog', d => d.accept())` to accept the `window.confirm("Delete this release note?")` dialog.

### Product Filter Behaviour (TC-025, TC-036)
- `updateProductFilterOptions()` rebuilds the `<select>` dropdown on every `renderReleaseList()` call. When an entry is edited so that a product no longer has any entries, the corresponding option is removed from the dropdown and the filter resets to `"all"`. Tests assert the localStorage state directly rather than attempting to select a no-longer-existing option.

### Submit Button Text
- In create mode the button text is `"Add Release Note"` (as set in `resetEditMode()` and in the HTML).
- In edit mode the text changes to `"Update Release Note"` (set by `startEdit()`).
- Test case descriptions that say `"Add Release"` refer to the same button; the automation uses the actual DOM text `"Add Release Note"`.

---

## How to Run

```bash
# Prerequisite: start the application server from the repo root
npx serve product_release_dashboard -l 3000

# From the automation directory
cd product_release_dashboard/automation
npm install
npx playwright install

# Run all 37 automated tests across all 3 browsers
npx playwright test

# Run by group
npm run test:positive
npm run test:negative
npm run test:boundary
npm run test:regression
```

HTML report is written to: `artifacts/COD-7/automation/playwright-report/`
