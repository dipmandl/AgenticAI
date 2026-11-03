# Test Plan

## Test Plan ID: TP-001

| Field | Value |
|---|---|
| Test Plan ID | TP-001 |
| Story ID | COD-7 |
| Story Title | Edit an existing release note |
| Version | 1.0 |
| Created | 2026-11-03 |
| Artifact | artifacts/COD-7/test-plans/test-plan.md |
| Status | DRAFT — ready for review |

---

## Story and Requirement References

| Reference Type | IDs |
|---|---|
| User Story | COD-7 |
| Functional Requirements | REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009 |
| Non-Functional Requirements | NFR-001, NFR-002, NFR-003, NFR-004 |
| Acceptance Criteria | AC-1, AC-2, AC-3, AC-4 |
| Negative Scenarios (from RA) | N-001, N-002, N-003, N-004, N-005 |
| Boundary Conditions (from RA) | B-001, B-002, B-003, B-004, B-005, B-006 |
| Impact Analysis | artifacts/COD-7/impact/impact-analysis.md |
| Requirement Analysis | artifacts/COD-7/requirements/requirement-analysis.md |

---

## Scope

### In Scope

| # | In-Scope Item |
|---|---|
| 1 | Edit button rendered per release entry row in the list |
| 2 | `startEdit()` behavior: form pre-fill, scroll to form, button text change, Cancel Edit button visibility |
| 3 | Pre-fill correctness for all 7 fields: `product`, `version`, `title`, `description`, `releaseDate`, `teamName`, `breaking` checkbox |
| 4 | `updateRelease()` behavior: id-matched in-place replacement, localStorage write, list re-render |
| 5 | Field validation on Save: `product`, `version`, `title`, `description`, `releaseDate` (HTML required), `teamName` (custom JS validation) |
| 6 | Cancel behavior: immediate discard with no confirmation dialog, form reset, return to create mode |
| 7 | Filter persistence across the edit lifecycle (Save and Cancel): product filter, breaking filter, search filter |
| 8 | Boundary condition B-003: edited entry disappears from filtered view when it no longer matches the active filter |
| 9 | Form mode-switching: submit handler routes to `updateRelease()` in edit mode and `addRelease()` in create mode |
| 10 | localStorage data integrity: array structure, field types, id immutability, unedited entries unchanged |
| 11 | Regression impact on create, delete, filter, search, and export flows |
| 12 | N-005 defect documentation: silent localStorage write failure with no user feedback |
| 13 | Boundary performance test for large dataset re-render (B-006) |
| 14 | Smoke scenario: quick create → edit → save sanity check |

### Out of Scope

| # | Out-of-Scope Item | Reason |
|---|---|---|
| 1 | Multi-user editing and concurrency control | Explicitly excluded in requirements; client-side only |
| 2 | Server-side persistence or API synchronization | NFR-001: localStorage-only; no network requests involved |
| 3 | Undo/redo history for edits | Explicitly excluded in requirements |
| 4 | Bulk editing of multiple release notes simultaneously | Explicitly excluded in requirements |
| 5 | Edit audit trail or change history | Explicitly excluded in requirements |
| 6 | Role-based access control | Explicitly excluded in requirements |
| 7 | Security testing (XSS, CSRF, injection) | Impact analysis concludes no security vulnerabilities introduced; current code uses `textContent` for display |
| 8 | CSV import regression beyond confirming no crash after edit | CSV import is an independent feature; full import regression is out of scope for this story |
| 9 | `styles.css` visual regression testing | NFR-002 confirms no new styling; existing CSS applies unchanged |
| 10 | Cross-device or mobile responsiveness testing | Not part of story requirements |
| 11 | Accessibility (WCAG) automated scanning | Accessibility noted as OPTIONAL in impact analysis; not a story requirement |
| 12 | `id` field editability — it must never be editable | Confirmed as design invariant; covered as assertion within positive tests, not a separate test group |

---

## Impacted Areas

Sourced from `artifacts/COD-7/impact/impact-analysis.md`.

| Module / Function | Risk Level | Key Concern |
|---|---|---|
| `index.html` — `#release-form`, submit button, Cancel Edit button | LOW | Mode clarity (visual distinction between create and edit states) |
| `script.js: startEdit()` | MEDIUM | State-transition logic; mode switch could interfere with create flow if handler swap is buggy |
| `script.js: updateRelease()` | HIGH | Direct localStorage mutation; no try/catch around `localStorage.setItem()` — silent failure on full storage (N-005) |
| `script.js: resetEditMode()` | LOW | Incomplete form reset could leak edit values into subsequent create operations |
| `script.js: renderReleaseList()` | MEDIUM | Must re-apply active filters post-edit; B-003 boundary condition depends on correct filter reapplication |
| `script.js: saveReleases()` | HIGH | No error handling on localStorage write; data loss risk with no user notification |
| `script.js: getFilteredReleases()` | MEDIUM | Filter DOM values must be correctly read after re-render; AC-4 and B-003 depend on this |
| Form submit event handler (mode routing) | MEDIUM | If mode switching is buggy, Save in create mode could trigger `updateRelease()` instead of `addRelease()` |
| localStorage key `"releaseNotesDashboard.releases"` | MEDIUM | Atomic re-write of full array; any structural corruption affects all other features |

---

## Test Categories

### Category Definitions and Entry/Exit Criteria

| Category | Automation | Entry Criteria | Exit Criteria |
|---|---|---|---|
| **Functional** | AUTO | Application deployable locally; localStorage accessible in browser; test data seeds loadable | All positive functional scenarios pass; form pre-fill, save, and cancel behaviors match requirements |
| **Negative** | AUTO / MANUAL | Application deployable; browser validation testable via Playwright | All negative scenarios either blocked at UI or documented as known gaps; N-005 logged as defect candidate |
| **Boundary** | AUTO / MANUAL | Test data with single-entry localStorage, multi-filter states, and large dataset (100+ entries) preparable | All boundary scenarios execute without error; B-003 verified; performance acceptable for B-006 |
| **Regression** | AUTO | Existing create, delete, filter, search, export tests remain green; edit code merged | All regression scenarios pass; no pre-existing feature broken by edit changes |
| **Smoke** | AUTO | Build deployed; localStorage available | TC-001 and TC-002 (edit happy path) pass end-to-end; suite runs in under 2 minutes |

---

## Test Scenarios

### Priority and Automation Legend

| Label | Meaning |
|---|---|
| P1 | CRITICAL — blocks release if failing |
| P2 | HIGH — significant defect if failing |
| P3 | MEDIUM — lower risk; can be deferred if resource-constrained |
| AUTO | Suitable for Playwright automation |
| MANUAL | Requires manual execution (browser storage quota manipulation or visual judgment) |
| BOTH | Automate happy path; validate edge through manual spot-check |

---

### Positive Scenarios

| TC ID | Scenario ID | Title | Steps (Summary) | Expected Outcome | REQ / AC Refs | Priority | Automation |
|---|---|---|---|---|---|---|---|
| TC-001 | TS-P-001 | Edit button present and triggers form pre-fill | 1. Load app with seeded data. 2. Locate a release entry in the list. 3. Click its Edit button. 4. Inspect form fields and UI state. | Form scrolls into view; all 7 fields (`product`, `version`, `title`, `description`, `releaseDate`, `teamName`, `breaking` checkbox) pre-filled with the exact stored values of the clicked entry; submit button text = "Update Release Note"; "Cancel Edit" button is visible. | REQ-001, REQ-002, REQ-003, REQ-004, AC-1 | P1 | AUTO |
| TC-002 | TS-P-002 | Save after modifying product field updates localStorage | 1. Click Edit on entry with `product = "ProductA"`. 2. Change product to "ProductX". 3. Click Save (submit form). 4. Read localStorage. | localStorage entry matching original id now has `product = "ProductX"`; rendered list reflects the new value. | REQ-005, REQ-006, REQ-007, AC-2 | P1 | AUTO |
| TC-003 | TS-P-003 | Save after modifying version field updates localStorage | 1. Click Edit. 2. Change version to "9.9.9". 3. Save. 4. Read localStorage. | Stored entry has `version = "9.9.9"`; UI reflects change. | REQ-005, REQ-006, REQ-007, AC-2 | P2 | AUTO |
| TC-004 | TS-P-004 | Save after modifying title and description updates both fields | 1. Click Edit. 2. Update title and description. 3. Save. 4. Read localStorage. | Stored entry has new title and description; other fields unchanged. | REQ-003, REQ-005, REQ-006, AC-2 | P2 | AUTO |
| TC-005 | TS-P-005 | Save after modifying releaseDate updates date in localStorage | 1. Click Edit. 2. Set releaseDate to "2024-06-15". 3. Save. 4. Read localStorage. | Stored entry has `releaseDate = "2024-06-15"`; date renders correctly in UI. | REQ-003, REQ-005, REQ-006, AC-2 | P2 | AUTO |
| TC-006 | TS-P-006 | Save after modifying teamName updates teamName in localStorage | 1. Click Edit on entry with existing teamName. 2. Change teamName to "AlphaTeam". 3. Save. 4. Read localStorage. | Stored entry has `teamName = "AlphaTeam"`. | REQ-003, REQ-005, REQ-006, AC-2 | P3 | AUTO |
| TC-007 | TS-P-007 | Save with breaking flag toggled from false to true | 1. Click Edit on entry with `isBreaking = false`. 2. Check the breaking checkbox. 3. Save. 4. Read localStorage. | Stored entry has `isBreaking = true`. | REQ-003, REQ-005, REQ-006, AC-2 | P2 | AUTO |
| TC-008 | TS-P-008 | Save with breaking flag toggled from true to false | 1. Click Edit on entry with `isBreaking = true`. 2. Uncheck the breaking checkbox. 3. Save. 4. Read localStorage. | Stored entry has `isBreaking = false`. | REQ-003, REQ-005, REQ-006, AC-2 | P2 | AUTO |
| TC-009 | TS-P-009 | Save after modifying all editable fields; id remains unchanged | 1. Note original `id` of entry. 2. Click Edit. 3. Modify all 7 editable fields. 4. Save. 5. Read localStorage. | All 7 fields updated; original `id` is identical in localStorage; no duplicate entries created. | REQ-003, REQ-005, REQ-006, REQ-007, AC-2 | P1 | AUTO |
| TC-010 | TS-P-010 | Cancel after modifying fields discards all changes | 1. Click Edit. 2. Modify product, title, and description. 3. Click Cancel Edit. 4. Read localStorage and inspect list. | localStorage unchanged; UI shows original values; form returns to create mode. | REQ-008, AC-3 | P1 | AUTO |
| TC-011 | TS-P-011 | Form returns to create mode after Save | 1. Click Edit on any entry. 2. Save successfully. 3. Inspect form state. | Submit button text = "Add Release"; "Cancel Edit" button is hidden; form fields are cleared. | REQ-004 | P2 | AUTO |
| TC-012 | TS-P-012 | Form returns to create mode after Cancel | 1. Click Edit on any entry. 2. Click Cancel Edit. 3. Inspect form state. | Submit button text = "Add Release"; "Cancel Edit" button is hidden; form fields are cleared. | REQ-004 | P2 | AUTO |
| TC-013 | TS-P-013 | Active product filter persists after Save | 1. Apply product filter = "ProductA". 2. Edit a "ProductA" entry (change title only). 3. Save. 4. Inspect product filter DOM value. | Product filter input still shows "ProductA"; rendered list still filtered by "ProductA". | REQ-009, AC-4, NFR-004 | P1 | AUTO |
| TC-014 | TS-P-014 | Active search filter persists after Cancel | 1. Apply search filter = "keywordX". 2. Click Edit on any visible entry. 3. Modify a field. 4. Click Cancel Edit. 5. Inspect search filter DOM value. | Search filter input still contains "keywordX"; rendered list still filtered by "keywordX". | REQ-009, AC-4, NFR-004 | P2 | AUTO |

---

### Negative Scenarios

| TC ID | Scenario ID | Title | Steps (Summary) | Expected Outcome | REQ / RA Refs | Priority | Automation |
|---|---|---|---|---|---|---|---|
| TC-015 | TS-N-001 | Save blocked when required field `product` is cleared | 1. Click Edit. 2. Clear the product field. 3. Submit form. | Browser HTML5 validation fires; form not submitted; localStorage unchanged. | N-001, REQ-003 | P1 | AUTO |
| TC-016 | TS-N-002 | Save blocked when required field `version` is cleared | 1. Click Edit. 2. Clear the version field. 3. Submit form. | Browser HTML5 validation fires; form not submitted; localStorage unchanged. | N-001, REQ-003 | P2 | AUTO |
| TC-017 | TS-N-003 | Save blocked when required field `title` is cleared | 1. Click Edit. 2. Clear the title field. 3. Submit form. | Browser HTML5 validation fires; form not submitted; localStorage unchanged. | N-001, REQ-003 | P2 | AUTO |
| TC-018 | TS-N-004 | Save blocked when required field `description` is cleared | 1. Click Edit. 2. Clear the description field. 3. Submit form. | Browser HTML5 validation fires; form not submitted; localStorage unchanged. | N-001, REQ-003 | P2 | AUTO |
| TC-019 | TS-N-005 | Save blocked when required field `releaseDate` is cleared | 1. Click Edit. 2. Clear the date field. 3. Submit form. | Browser HTML5 validation fires; form not submitted; localStorage unchanged. | N-001, REQ-003 | P2 | AUTO |
| TC-020 | TS-N-006 | Save blocked with custom error when `teamName` is cleared | 1. Click Edit on entry with an existing teamName. 2. Clear the teamName field. 3. Submit form. | Custom JS validation shows inline error message adjacent to the teamName field; teamName field receives focus; form not submitted; localStorage unchanged. | N-001, REQ-003 | P1 | AUTO |
| TC-021 | TS-N-007 | Save without modifying any field succeeds and preserves data | 1. Click Edit on any entry. 2. Do not modify any field. 3. Save. 4. Read localStorage. | Entry re-saved as-is; no error thrown; no data loss; localStorage array structure intact. | N-002 | P2 | AUTO |
| TC-022 | TS-N-008 | localStorage full on Save — silent failure (defect candidate) | 1. Fill localStorage close to quota using auxiliary data. 2. Edit an entry. 3. Save. 4. Observe UI and read localStorage. | **Expected (current behavior):** Application appears to save successfully; no error message shown; localStorage write silently fails. **Defect candidate:** Application should surface an error to the user per N-005 in requirement analysis. Document result for defect logging. | N-005, NFR-003 | P3 | MANUAL |

---

### Boundary Scenarios

| TC ID | Scenario ID | Title | Steps (Summary) | Expected Outcome | REQ / RA Refs | Priority | Automation |
|---|---|---|---|---|---|---|---|
| TC-023 | TS-B-001 | Edit the only release note in the list | 1. Clear localStorage; load exactly 1 release. 2. Click Edit. 3. Modify fields. 4. Save. 5. Inspect list and localStorage. | List re-renders with one updated entry; no duplicate; no empty list state. | B-001, REQ-007 | P1 | AUTO |
| TC-024 | TS-B-002 | Edit with no active filters applied | 1. Ensure no filters are active (all inputs blank / "all"). 2. Edit an entry. 3. Save. 4. Inspect list. | All releases rendered; edited entry shows updated values; no filter restriction applied. | B-002, REQ-007 | P3 | AUTO |
| TC-025 | TS-B-003 | Edited entry disappears when it no longer matches active product filter | 1. Load list with entries for "ProductA" and "ProductB". 2. Apply product filter = "ProductA". 3. Edit a "ProductA" entry; change product to "ProductB". 4. Save. 5. Inspect filtered list. | Edited entry no longer appears in the filtered view; other "ProductA" entries still visible; entry is present in localStorage with new product value. | B-003, REQ-007, REQ-009, AC-4 | P1 | AUTO |
| TC-026 | TS-B-004 | Edit entry with `isBreaking = true` — checkbox pre-fills as checked | 1. Load entry with `isBreaking = true`. 2. Click Edit. 3. Inspect the breaking checkbox. | Breaking checkbox is rendered in checked state before any user interaction. | B-004, REQ-003, AC-1 | P2 | AUTO |
| TC-027 | TS-B-005 | Edit entry with `releaseDate = "1970-01-01"` — date pre-fills correctly | 1. Load entry with `releaseDate = "1970-01-01"`. 2. Click Edit. 3. Inspect date input value. | Date input displays "1970-01-01" (no truncation, no epoch conversion error). | B-005, REQ-003, AC-1 | P2 | AUTO |
| TC-028 | TS-B-006 | Edit entry with `releaseDate = today's date` — date pre-fills correctly | 1. Load entry with today's date as `releaseDate`. 2. Click Edit. 3. Inspect date input value. | Date input matches today's date in YYYY-MM-DD format. | B-005, REQ-003, AC-1 | P3 | AUTO |
| TC-029 | TS-B-007 | All three filters active simultaneously — all persist after Save | 1. Apply: product filter = "ProductA", breaking filter = "breaking", search = "release". 2. Edit a matching entry (change title only). 3. Save. 4. Inspect all three filter DOM input values. | All three filter inputs retain their values; rendered list reflects the combined AND filter. | AC-4, REQ-009, NFR-004 | P2 | AUTO |
| TC-030 | TS-B-008 | Edit one entry from a 100-entry dataset — no visible performance lag | 1. Seed localStorage with 100 test entries. 2. Edit one entry. 3. Save. 4. Observe re-render time. | List re-renders in under 2 seconds (subjective threshold); no browser freeze or visible lag. | B-006 | P3 | MANUAL |

---

### Regression Scenarios

| TC ID | Scenario ID | Title | Steps (Summary) | Expected Outcome | REQ / NFR Refs | Priority | Automation |
|---|---|---|---|---|---|---|---|
| TC-031 | TS-R-001 | Create → Edit → Create: second create adds new entry with blank form | 1. Create entry A. 2. Edit entry A; change product. 3. Save. 4. Fill create form with new entry B data. 5. Submit create. 6. Read localStorage. | Entry B is newly added with new id; no stale fields from edit pre-fill; both entries in localStorage. | NFR-003 (form state leakage) | P1 | AUTO |
| TC-032 | TS-R-002 | Edit → Save → Delete: delete removes correct entry and list re-renders | 1. Edit an entry; save. 2. Delete the same entry via Delete button. 3. Confirm deletion dialog. 4. Inspect list and localStorage. | Deleted entry absent from list and localStorage; other entries intact; no JS errors. | NFR-003 (delete regression) | P2 | AUTO |
| TC-033 | TS-R-003 | Edit → Save → Export: CSV export reflects updated values | 1. Edit an entry; change product and title; save. 2. Click Export CSV. 3. Inspect downloaded CSV content. | CSV contains the updated product and title for the edited entry; CSV schema (`product,version,teamName,title,description,releaseDate,isBreaking`) is intact. | NFR-003 (export regression) | P2 | AUTO |
| TC-034 | TS-R-004 | Edit → Cancel → Create: create form is blank and adds new entry | 1. Click Edit; modify product and title. 2. Click Cancel Edit. 3. Submit create form with distinct new data. 4. Read localStorage. | Create form had no pre-filled values from the cancelled edit; new entry added with provided data; original entry unchanged. | NFR-003 (cancel-then-create) | P1 | AUTO |
| TC-035 | TS-R-005 | Edit one entry — all other entries remain unchanged in localStorage | 1. Seed 5 entries; note all their values. 2. Edit entry 3; change 3 fields; save. 3. Read all 5 entries from localStorage. | Entries 1, 2, 4, 5 have identical values to pre-edit state; entry 3 reflects the 3 changed fields. | REQ-005, NFR-003 | P1 | AUTO |
| TC-036 | TS-R-006 | Edit product value — product filter returns correct results afterward | 1. Edit entry; change product from "ProductA" to "ProductB". 2. Save. 3. Apply product filter = "ProductB". 4. Inspect list. | Edited entry appears in "ProductB" filter results; does not appear in "ProductA" results. | NFR-003 (filter regression) | P2 | AUTO |
| TC-037 | TS-R-007 | Edit same entry twice — second edit pre-fills values from first save | 1. Edit entry; change product to "ProductX"; save. 2. Click Edit on the same entry again. 3. Inspect product field. | Product field shows "ProductX" (the value from the first save, not the original pre-edit value). | REQ-002, REQ-003, AC-1 | P2 | AUTO |
| TC-038 | TS-R-008 | Seed data: edit one seed record — other seed record unchanged | 1. Clear localStorage; reload app (seeds 2 records). 2. Edit seed record 1; change title; save. 3. Read both records from localStorage. | Seed record 2 values are identical to original seeded values; no cross-contamination. | NFR-003 (seed data integrity) | P3 | AUTO |
| TC-039 | TS-R-009 | Edit entry to `isBreaking = true` — breaking filter shows it correctly | 1. Edit entry with `isBreaking = false`; check breaking checkbox; save. 2. Apply breaking filter = "breaking". 3. Inspect list. | Edited entry appears in the "breaking" filtered view. | NFR-003 (breaking filter regression) | P2 | AUTO |
| TC-040 | TS-R-010 | Edit title to include search keyword — search returns updated entry | 1. Apply search filter = "unicornkeyword". 2. Verify no results (keyword not present). 3. Edit an entry; add "unicornkeyword" to title; save. 4. Verify search = "unicornkeyword" now returns the edited entry. | Edited entry appears in search results; search applied to title field. | NFR-003 (search regression) | P2 | AUTO |
| TC-041 | TS-R-011 | Two sequential edits on different entries — both updated independently | 1. Edit entry A; change product; save. 2. Edit entry B; change title; save. 3. Read localStorage. | Entry A has updated product; entry B has updated title; no cross-contamination; no id collision. | REQ-005, REQ-006 | P2 | AUTO |
| TC-042 | TS-R-012 | Edit → Save → Import CSV: import proceeds without crash | 1. Edit an entry; save. 2. Attempt CSV import (confirm prompt). 3. Observe result. | Import completes; localStorage replaced with CSV data; no JS error caused by prior edit state. | NFR-003 (import regression) | P3 | MANUAL |

---

## Test Groups Summary

| Group | Count | TC Range | Priority Distribution | Automation |
|---|---|---|---|---|
| Positive | 14 | TC-001 – TC-014 | P1: 5, P2: 7, P3: 2 | AUTO (all 14) |
| Negative | 8 | TC-015 – TC-022 | P1: 2, P2: 5, P3: 1 | AUTO: 7, MANUAL: 1 |
| Boundary | 8 | TC-023 – TC-030 | P1: 2, P2: 3, P3: 3 | AUTO: 6, MANUAL: 2 |
| Regression | 12 | TC-031 – TC-042 | P1: 3, P2: 7, P3: 2 | AUTO: 10, MANUAL: 2 |
| **Total** | **42** | **TC-001 – TC-042** | **P1: 12, P2: 22, P3: 8** | **AUTO: 37, MANUAL: 5** |

---

## Coverage Matrix

### Requirement → Test Case Mapping

| Requirement ID | Description (Short) | Covered By (TC IDs) | Category |
|---|---|---|---|
| REQ-001 | Edit button per entry | TC-001 | Functional |
| REQ-002 | Edit opens entry in editable state with pre-filled fields | TC-001, TC-037 | Functional, Regression |
| REQ-003 | All 6 fields pre-filled and editable | TC-001, TC-026, TC-027, TC-028, TC-015 – TC-020 | Functional, Boundary, Negative |
| REQ-004 | Save and Cancel actions present | TC-011, TC-012 | Functional |
| REQ-005 | Save updates entry by id in releases array | TC-002 – TC-009, TC-035, TC-041 | Functional, Regression |
| REQ-006 | Save persists updated list to localStorage | TC-002 – TC-009, TC-033, TC-035, TC-041 | Functional, Regression |
| REQ-007 | Save re-renders release list | TC-002, TC-003, TC-009, TC-023, TC-024, TC-025 | Functional, Boundary |
| REQ-008 | Cancel applies no changes | TC-010, TC-034 | Functional, Regression |
| REQ-009 | Active filters persist after Save or Cancel | TC-013, TC-014, TC-025, TC-029 | Functional, Boundary |
| NFR-001 | Client-side only, no network requests | TC-002 – TC-010 (no network assertions) | Functional |
| NFR-002 | No new styling frameworks | Out of scope | N/A |
| NFR-003 | Edit must not corrupt localStorage structure used by other features | TC-031 – TC-042 | Regression |
| NFR-004 | Filter state preserved across edit lifecycle | TC-013, TC-014, TC-029 | Functional, Boundary |

### Acceptance Criteria → Test Case Mapping

| AC ID | Acceptance Criterion | Covered By (TC IDs) |
|---|---|---|
| AC-1 | Click Edit → all fields pre-filled | TC-001, TC-026, TC-027, TC-028 |
| AC-2 | Modify + Save → entry updated by id in list and localStorage | TC-002 – TC-010, TC-023, TC-025 |
| AC-3 | Cancel → no changes saved | TC-010, TC-012, TC-034 |
| AC-4 | Filters remain applied after Save or Cancel | TC-013, TC-014, TC-025, TC-029 |

---

## Test Data Requirements

### Seed States

| State ID | Description | Fields | Used In |
|---|---|---|---|
| SD-001 | Standard 5-entry dataset with varied products | 2 × ProductA, 2 × ProductB, 1 × ProductC; mixed breaking flags; all have teamName | TC-002 – TC-014, TC-031 – TC-041 |
| SD-002 | Single-entry dataset | 1 entry with all fields populated; `isBreaking = false` | TC-023 |
| SD-003 | Entry with `isBreaking = true` | All required fields; `isBreaking = true` | TC-008, TC-026, TC-039 |
| SD-004 | Entry with `releaseDate = "1970-01-01"` | All fields; epoch date | TC-027 |
| SD-005 | Entry with `releaseDate = <today's date>` | All fields; current date in YYYY-MM-DD | TC-028 |
| SD-006 | Entry with empty/undefined `teamName` | All other fields populated; `teamName` absent | TC-020 |
| SD-007 | Large dataset: 100 entries | Randomized product, version, title, description, date, breaking; all with teamName | TC-030 |
| SD-008 | Two-product dataset for B-003 | Exactly 2 entries: one ProductA, one ProductB | TC-025, TC-036 |
| SD-009 | Default app seed (no localStorage) | Application seeds 2 records on first load when localStorage empty | TC-038 |

### localStorage Setup Strategy

Each test must:
1. Before test: Set `localStorage.setItem("releaseNotesDashboard.releases", JSON.stringify([...testData]))` via Playwright's `page.evaluate()` before page load, OR clear localStorage and load page to trigger seed.
2. After test: Call `localStorage.clear()` and reload to isolate state between tests.

### Filter State Setup

| Filter Setup ID | Configuration | Used In |
|---|---|---|
| FS-001 | Product filter = "ProductA" only | TC-013, TC-025, TC-036 |
| FS-002 | Search filter = "keywordX" | TC-014 |
| FS-003 | Breaking filter = "breaking" | TC-039 |
| FS-004 | All three filters active: product="ProductA", breaking="breaking", search="release" | TC-029 |
| FS-005 | No filters active (all blank / "all") | TC-024 |

### Data Constraints

- `id` values must be pre-assigned as stable UUID strings in test data (not auto-generated at test time) so tests can reliably look up entries: e.g., `"test-id-001"`, `"test-id-002"`.
- `releaseDate` values must use YYYY-MM-DD format exactly as stored by the date input element.
- `isBreaking` must be a JSON boolean (`true`/`false`), not a string.
- `teamName` field may be omitted from some seed entries (not always present) to test the undefined-teamName path.

**FLAG**: No test data generator script currently exists. The test automation agent must implement localStorage seeding helpers before TC execution.

---

## Environment Requirements

| Requirement | Detail |
|---|---|
| Browser | Chromium (primary, via Playwright); Firefox and WebKit spot-check recommended for B-004 and B-005 date input behavior |
| localStorage | Must be enabled and accessible; tests must be able to read/write localStorage via `page.evaluate()` |
| Network | No network connection required; application is entirely client-side |
| Application serving | Local file server (e.g., `npx serve .` or `python -m http.server`); file:// protocol may restrict localStorage in some browsers — a local server is required |
| Node.js | Required for Playwright installation and test execution |
| Playwright version | Latest stable; `@playwright/test` package |
| OS | Any (Windows / macOS / Linux); CI must support Playwright Chromium |
| No external dependencies | No backend, no auth service, no CDN resources required |

**FLAG**: A `package.json` with `@playwright/test` and a `playwright.config.ts` with `baseURL` pointing to the local server are prerequisites. Confirm these exist or create them in the automation phase.

---

## Dependencies

| Dependency | Type | Required For | Status |
|---|---|---|---|
| `script.js: startEdit()` implemented and complete | Application code | All TC-001 – TC-030 | UNKNOWN — verify in automation phase |
| `script.js: updateRelease()` implemented and complete | Application code | TC-002 – TC-011, TC-023, TC-025, TC-031 – TC-041 | UNKNOWN — verify in automation phase |
| `script.js: resetEditMode()` implemented | Application code | TC-010 – TC-012, TC-034 | UNKNOWN — verify in automation phase |
| Edit button rendered per list row in `index.html` | Application UI | TC-001 and all others | UNKNOWN — verify in automation phase |
| Playwright installed and configured | Test tooling | All AUTO tests | Automation phase |
| localStorage seeding helper utility | Test helper | All tests requiring SD-001 – SD-009 | Automation phase |
| 100-entry dataset generator | Test data | TC-030 | Automation phase |
| Local HTTP server for app serving | Environment | All tests | Setup step |

---

## Risks and Mitigations

| Risk ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| RISK-001 | N-005: `saveReleases()` has no try/catch; localStorage full causes silent data loss with no user feedback | MEDIUM | HIGH | TC-022 documents current behavior as a defect candidate; raise Jira defect if confirmed. Recommend adding try/catch in code review. |
| RISK-002 | Form mode-switching bug: `addRelease()` called instead of `updateRelease()` on Save during edit mode (or vice versa) | MEDIUM | HIGH | TC-031 and TC-041 explicitly test the create-after-edit and dual-edit sequences to catch handler leakage. |
| RISK-003 | B-003 not implemented: edited entry remains visible in filtered view after its product changes | MEDIUM | MEDIUM | TC-025 explicitly tests this behavior; if it passes, B-003 is confirmed working as designed. |
| RISK-004 | `resetEditMode()` incomplete: stale edit values leak into subsequent create operations | LOW | MEDIUM | TC-031 and TC-034 cover cancel-then-create and save-then-create sequences. |
| RISK-005 | Date input pre-fill broken for edge dates (epoch, today) in specific browsers | LOW | MEDIUM | TC-027 and TC-028 cover date boundaries; run on Chromium, Firefox, and WebKit for B-005. |
| RISK-006 | Automation timing issue: test reads localStorage before re-render completes | LOW | LOW | Use Playwright `waitForFunction` or `waitForSelector` to assert UI state before reading localStorage. |
| RISK-007 | `startEdit()` not yet fully implemented in `script.js` | UNKNOWN | HIGH | Automation phase agent must verify function existence and completeness before writing tests; fail fast if incomplete. |
| RISK-008 | TC-030 performance test is subjective (no hard SLA defined) | LOW | LOW | Flag as manual; record observed render time in test report; establish baseline in first run. |

---

## Assumptions

| ID | Assumption |
|---|---|
| A-001 | `startEdit()`, `updateRelease()`, and `resetEditMode()` functions exist in `script.js` in a callable state at the time automation is written. |
| A-002 | The `id` field in each release entry is a unique, immutable string assigned at creation time and never modified by any operation including edit. |
| A-003 | The edit form reuses the existing `#release-form` at the top of the page — no modal, no inline row form. This is confirmed by source code inspection in the requirement analysis. |
| A-004 | Cancel requires no confirmation dialog; `resetEditMode()` fires immediately. |
| A-005 | Filter state is held in DOM input element values and is naturally preserved across edit without any special handling. |
| A-006 | Playwright can access and manipulate localStorage via `page.evaluate()` within the same origin as the served application. |
| A-007 | The application is served over HTTP (local server), not the `file://` protocol, to avoid localStorage restrictions. |
| A-008 | B-003 is expected and accepted behavior (not a defect): edited entry disappearing from filtered view after product change is intentional. |
| A-009 | CSV import (which fully replaces localStorage data after `window.confirm`) is tested only minimally for regression (TC-042) — full import test coverage is out of scope for this story. |
| A-010 | Two records are seeded automatically on first load when localStorage is empty; tests that require a clean state must clear localStorage before page load. |

---

## Priority Summary (P1 / P2 / P3)

### P1 — CRITICAL (12 test cases — must pass before release)

TC-001, TC-002, TC-009, TC-010, TC-013, TC-015, TC-020, TC-023, TC-025, TC-031, TC-034, TC-035

These cover: core edit + save + cancel happy paths, id immutability, filter persistence, required field validation, single-entry boundary, filter exclusion (B-003), and the two highest-risk regression scenarios (form state leakage, unedited entries unchanged).

### P2 — HIGH (22 test cases — should pass before release; deferral requires documented risk acceptance)

TC-003, TC-004, TC-005, TC-006, TC-007, TC-008, TC-011, TC-012, TC-014, TC-016, TC-017, TC-018, TC-019, TC-021, TC-024, TC-026, TC-027, TC-029, TC-032, TC-033, TC-036, TC-037, TC-039, TC-040, TC-041

These cover: field-by-field modifications, mode-switch UI state, filter combinations, remaining validation cases, B-004/B-005 boundary dates, and core regression flows.

### P3 — MEDIUM (8 test cases — can be deferred to stabilisation cycle)

TC-006 (teamName modify), TC-022 (localStorage full — MANUAL, defect-only), TC-024 (no-filter edit), TC-028 (today's date boundary), TC-030 (performance — MANUAL), TC-038 (seed data isolation), TC-042 (post-edit import — MANUAL)

---

## Automation Approach

### Recommended Framework: Playwright

**Rationale**:
- Playwright provides first-class `page.evaluate()` access to localStorage for both setup (seeding) and assertion (verification independent of rendering).
- Playwright's auto-waiting and locator strategies handle the form scroll-into-view (`startEdit()` scroll behavior) reliably.
- Playwright supports multi-browser runs (Chromium, Firefox, WebKit) which is needed for date input boundary tests (TC-027, TC-028).
- No backend mocking needed — localStorage-only persistence simplifies test setup.
- Playwright's `expect` matchers can assert DOM attribute states (e.g., checkbox `checked`, button text, element visibility) cleanly.

### Automation Coverage

| Category | Total | AUTO | MANUAL | AUTO % |
|---|---|---|---|---|
| Positive | 14 | 14 | 0 | 100% |
| Negative | 8 | 7 | 1 | 88% |
| Boundary | 8 | 6 | 2 | 75% |
| Regression | 12 | 10 | 2 | 83% |
| **Total** | **42** | **37** | **5** | **88%** |

### Manual Test Cases Rationale

| TC ID | Reason for Manual Execution |
|---|---|
| TC-022 | Requires filling localStorage to browser quota limit — not safely automatable without risk of browser instability |
| TC-030 | Performance judgment (visual lag) requires human observation; no hard SLA defined |
| TC-042 | CSV import involves `window.confirm` dialog handling and file system interaction; mark for manual spot-check |

### Recommended Test File Structure

```
tests/
  edit-release/
    positive.spec.ts       # TC-001 – TC-014
    negative.spec.ts       # TC-015 – TC-022
    boundary.spec.ts       # TC-023 – TC-030
    regression.spec.ts     # TC-031 – TC-042
  helpers/
    localStorage.ts        # Seed/read/clear localStorage helpers
    testData.ts            # SD-001 through SD-009 definitions
```

---

## Exclusions (Explicit)

| # | Excluded Item | Reason |
|---|---|---|
| EX-001 | Multi-user concurrency and conflict resolution | Explicitly out of scope in requirements |
| EX-002 | Server-side persistence and API integration | NFR-001: client-side only; no network calls |
| EX-003 | Undo/redo functionality | Not a requirement; explicitly excluded |
| EX-004 | Bulk edit operations | Not a requirement; explicitly excluded |
| EX-005 | Change audit trail | Not a requirement; explicitly excluded |
| EX-006 | Role-based access control | Not a requirement; any user can edit |
| EX-007 | CSS visual regression (pixel diffing) | NFR-002: no styling changes; existing CSS applies |
| EX-008 | XSS, CSRF, and injection security testing | Impact analysis concludes no security surface introduced |
| EX-009 | WCAG / accessibility scanning | Optional per impact analysis; not a story requirement |
| EX-010 | N-003 (page refresh / navigate-away during edit) | Browser behavior (unload discards JS state) is outside application control; no application-level handling exists |
| EX-011 | N-004 (edit a deleted entry from another session tab) | Multi-tab/multi-session behavior is out of scope; no application-level handling defined |
| EX-012 | Full CSV import regression suite | CSV import is a separate feature; only a minimal post-edit crash check (TC-042) is included |
| EX-013 | `id` field format validation (UUID vs. fallback) | `generateId()` implementation is internal; tests assert id immutability, not id format |
| EX-014 | Mobile responsiveness and touch interaction | Not part of story requirements |

---

## Traceability Summary

| Test Group | TC IDs | REQ IDs | AC IDs | Risk Areas from Impact Analysis |
|---|---|---|---|---|
| Positive | TC-001 – TC-014 | REQ-001 to REQ-009, NFR-001, NFR-004 | AC-1, AC-2, AC-3, AC-4 | startEdit(), updateRelease(), resetEditMode() |
| Negative | TC-015 – TC-022 | REQ-003, NFR-003 | AC-2 | saveReleases() (N-005), form validation |
| Boundary | TC-023 – TC-030 | REQ-007, REQ-009, NFR-004 | AC-1, AC-2, AC-4 | renderReleaseList(), getFilteredReleases(), B-003 |
| Regression | TC-031 – TC-042 | NFR-003, REQ-005, REQ-006 | AC-2, AC-3 | Form mode-switching, localStorage integrity, create/delete/filter/export regression |
