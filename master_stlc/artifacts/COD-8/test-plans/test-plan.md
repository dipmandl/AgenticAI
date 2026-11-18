# Test Plan — COD-8

**Test Plan ID**: TP-001
**Story ID**: COD-8
**Story Title**: Delete a release note with confirmation
**Author**: Test Planning Agent
**Date**: 2026-11-05
**Status**: DRAFT — Pending Review

---

## 1. Story and Requirement References

| Reference ID | Description |
|---|---|
| COD-8 | Story: Delete a release note with confirmation |
| REQ-001 | Delete button present on each release card |
| REQ-002 | Confirmation prompt shown before deletion |
| REQ-003 | In-memory state updated on confirm |
| REQ-004 | localStorage updated on confirm |
| REQ-005 | UI re-rendered after deletion |
| REQ-006 | No changes on cancellation |
| AC-1 | Clicking Delete shows confirmation prompt |
| AC-2 | Confirmed deletion removes release from UI and localStorage |
| AC-3 | Cancelled deletion leaves release unchanged |
| BC-001..BC-006 | Boundary conditions from requirement analysis |
| NEG-001..NEG-004 | Negative conditions from requirement analysis |

---

## 2. Test Objectives

1. Verify the Delete button is present and visible on every rendered release card.
2. Verify a confirmation prompt is presented before any deletion occurs.
3. Verify confirmed deletion removes the release from in-memory state, localStorage, and the DOM.
4. Verify cancelled/dismissed confirmation produces no change in state, storage, or UI.
5. Verify edge positions (first, last, only release) are handled correctly.
6. Verify cross-reload persistence: deleted releases do not reappear after a page reload.
7. Verify that delete-flow changes to `saveReleases()` and `renderReleaseList()` do not break create, edit, filter/search, or JSON-export (COD-9) functionality.

---

## 3. Scope

The following areas are in scope for this test plan:

- Visibility and accessibility of the Delete button (`.delete-btn`, `.danger-btn`) on release cards.
- Confirmation dialog appearance and behaviour (`window.confirm()`).
- In-memory `releases` array state after confirmed deletion.
- localStorage key `releaseNotesDashboard.releases` state after confirmed deletion.
- DOM re-render: deleted card removed; remaining cards unaffected.
- Cancellation / dismissal of the confirmation dialog.
- Deletion while a release is open in edit mode (`resetEditMode()` call path).
- Empty-state display when the last release is deleted.
- Cross-reload persistence of the deletion.
- Filter/search state preservation after deletion triggers `renderReleaseList()`.
- Regression coverage of create, edit, filter/search, and JSON-export operations affected by shared `saveReleases()` and `renderReleaseList()` calls.

---

## 4. Out of Scope

| OOS ID | Description |
|---|---|
| OOS-001 | Undo / restore functionality after deletion |
| OOS-002 | Bulk deletion of multiple release notes in a single operation |
| OOS-003 | Server-side persistence (application is client-side only) |
| OOS-004 | Replacing native browser confirm with a custom modal dialog UI |
| OOS-005 | Browser compatibility testing beyond Microsoft Edge |
| OOS-006 | Accessibility enhancements to the confirmation dialog |
| OOS-007 | Performance or stress testing with large datasets (100+ releases) |
| OOS-008 | Security / authorization testing (no auth layer; no security impact identified) |
| OOS-009 | Parallel or concurrent tab testing beyond the single cross-tab regression scenario noted below |

---

## 5. Impacted Areas

Derived from `artifacts/COD-8/impact/impact-analysis.md`.

| File / Component | Risk Level | Reason |
|---|---|---|
| `script.js` — `deleteRelease(id)` (lines 188–201) | HIGH | Core deletion logic: confirm dialog, array filter, saveReleases, renderReleaseList |
| `script.js` — `saveReleases()` | HIGH | Shared by create/delete; corruption here breaks all persistence |
| `script.js` — `renderReleaseList()` | HIGH | Shared by all CRUD; broken render breaks filters and card display |
| `script.js` — `resetEditMode()` | MEDIUM | Called on delete-during-edit path; must clear form cleanly |
| `index.html` — release card template | LOW | Button markup already exists; no structural change expected |
| `styles.css` — `.delete-btn`, `.danger-btn` | LOW | Styling already present; no functional change expected |
| `automation/pages/release_dashboard_page.py` | LOW | May need minor additions for delete-specific POM methods |
| `automation/environment.py` | LOW | Existing alert handling and localStorage hooks cover requirements |

---

## 6. Test Categories

| Category | Applicable | Automation Suitability | Notes |
|---|---|---|---|
| Positive / Functional | YES | AUTO | Core happy-path flows; full Selenium automation feasible |
| Negative | YES | AUTO | Cancel/dismiss flows; Selenium alert dismiss already supported in POM |
| Boundary | YES | AUTO | Edge positions and cross-reload covered by Selenium + page reload |
| Regression | YES | BOTH | Create/edit/filter/export regression; AUTO where existing steps cover; MANUAL for cross-tab |
| E2E | YES | AUTO | Click → confirm → reload → verify is a natural Selenium E2E flow |
| UI | YES | AUTO | DOM assertions, card count, empty state — all automatable |
| Integration | YES | AUTO | In-memory ↔ localStorage ↔ DOM consistency checks via JS executor |
| Security | NO | N/A | Out of scope per impact analysis |
| Performance | NO | N/A | Out of scope per OOS-007 |
| Accessibility | OPTIONAL | MANUAL | Low priority; flagged only; not included in this plan |

---

## 7. Test Scenarios

Scenario IDs follow the pattern `TS-{group}-{NNN}`. Each scenario is also assigned a sequential `TC-NNN` ID used for end-to-end traceability. IDs are stable and must not be renumbered.

---

### 7.1 Positive Scenarios

**Priority**: CRITICAL (TC-001 to TC-005), HIGH (TC-006 to TC-008)
**Automation Suitability**: AUTO

---

#### TS-P-001 | TC-001 — Delete button visible on every release card

| Field | Value |
|---|---|
| TC ID | TC-001 |
| Scenario ID | TS-P-001 |
| Priority | CRITICAL |
| Requirement(s) | REQ-001 |
| Acceptance Criteria | AC-1 |
| Precondition | At least one release exists in the list |
| Steps | 1. Load application. 2. Observe all rendered release cards. |
| Expected Result | Every release card has a visible Delete button (`.delete-btn` / `.danger-btn`). |
| Automation | AUTO — assert element presence and visibility via POM |

---

#### TS-P-002 | TC-002 — Clicking Delete shows confirmation prompt

| Field | Value |
|---|---|
| TC ID | TC-002 |
| Scenario ID | TS-P-002 |
| Priority | CRITICAL |
| Requirement(s) | REQ-002 |
| Acceptance Criteria | AC-1 |
| Precondition | At least one release card is rendered |
| Steps | 1. Load application. 2. Click the Delete button on any release card. |
| Expected Result | A browser confirmation dialog appears before any deletion occurs. No state change occurs before user response. |
| Automation | AUTO — `driver.switch_to.alert` detects the dialog |

---

#### TS-P-003 | TC-003 — Confirmed deletion removes card from DOM

| Field | Value |
|---|---|
| TC ID | TC-003 |
| Scenario ID | TS-P-003 |
| Priority | CRITICAL |
| Requirement(s) | REQ-003, REQ-005 |
| Acceptance Criteria | AC-2 |
| Precondition | At least two releases exist so list is not empty after deletion |
| Steps | 1. Load application with 2+ releases. 2. Record count of release cards. 3. Click Delete on a specific release. 4. Accept the confirmation dialog. |
| Expected Result | The targeted release card is removed from the DOM. Total card count decreases by 1. |
| Automation | AUTO — compare card count before and after; assert target card absent |

---

#### TS-P-004 | TC-004 — Confirmed deletion removes release from localStorage

| Field | Value |
|---|---|
| TC ID | TC-004 |
| Scenario ID | TS-P-004 |
| Priority | CRITICAL |
| Requirement(s) | REQ-004 |
| Acceptance Criteria | AC-2 |
| Precondition | At least one release exists; localStorage contains the release |
| Steps | 1. Load application. 2. Record release IDs in localStorage. 3. Click Delete on a specific release. 4. Accept confirmation. 5. Read localStorage key `releaseNotesDashboard.releases`. |
| Expected Result | The deleted release's ID is absent from the localStorage JSON array. |
| Automation | AUTO — `driver.execute_script("return localStorage.getItem(...)")` post-deletion |

---

#### TS-P-005 | TC-005 — Release count decreases by exactly one after deletion

| Field | Value |
|---|---|
| TC ID | TC-005 |
| Scenario ID | TS-P-005 |
| Priority | CRITICAL |
| Requirement(s) | REQ-003, REQ-005 |
| Acceptance Criteria | AC-2 |
| Precondition | 3 releases exist |
| Steps | 1. Load application with 3 releases. 2. Count cards (expect 3). 3. Delete one release and confirm. 4. Count cards again. |
| Expected Result | Card count is exactly 2. In-memory and localStorage count is 2. |
| Automation | AUTO — count DOM cards; count localStorage array length |

---

#### TS-P-006 | TC-006 — Other releases are unaffected after a single deletion

| Field | Value |
|---|---|
| TC ID | TC-006 |
| Scenario ID | TS-P-006 |
| Priority | HIGH |
| Requirement(s) | REQ-003, REQ-005 |
| Acceptance Criteria | AC-2 |
| Precondition | 3 releases with known IDs/titles exist |
| Steps | 1. Load application. 2. Delete release B (middle). 3. Confirm deletion. 4. Verify releases A and C remain in DOM and localStorage. |
| Expected Result | Releases A and C remain fully intact in DOM and localStorage. Their content is unchanged. |
| Automation | AUTO — assert by release title/ID presence |

---

#### TS-P-007 | TC-007 — Deleted release does not reappear after page reload

| Field | Value |
|---|---|
| TC ID | TC-007 |
| Scenario ID | TS-P-007 |
| Priority | HIGH |
| Requirement(s) | REQ-004 |
| Acceptance Criteria | AC-2 |
| Precondition | At least one release exists |
| Steps | 1. Load application. 2. Delete a release and confirm. 3. Reload the page (`driver.refresh()`). 4. Verify the deleted release is absent. |
| Expected Result | The deleted release does not appear in the UI or localStorage after reload. |
| Automation | AUTO — reload and assert card absence; read localStorage post-reload |

---

#### TS-P-008 | TC-008 — Delete while in edit mode resets form and removes release

| Field | Value |
|---|---|
| TC ID | TC-008 |
| Scenario ID | TS-P-008 |
| Priority | HIGH |
| Requirement(s) | REQ-003, REQ-004, REQ-005 (BC-004) |
| Acceptance Criteria | AC-2 |
| Precondition | At least one release is open in edit mode |
| Steps | 1. Load application. 2. Click Edit on release A to open edit form. 3. Click Delete on release A. 4. Accept confirmation. |
| Expected Result | Edit form is cleared (`resetEditMode()` called). Release A is removed from DOM and localStorage. No form data persists. |
| Automation | AUTO — assert form fields empty; assert card absent |

---

### 7.2 Negative Scenarios

**Priority**: HIGH
**Automation Suitability**: AUTO

---

#### TS-N-001 | TC-009 — Cancelling confirmation keeps release in UI

| Field | Value |
|---|---|
| TC ID | TC-009 |
| Scenario ID | TS-N-001 |
| Priority | HIGH |
| Requirement(s) | REQ-006 |
| Acceptance Criteria | AC-3 |
| Precondition | At least one release exists |
| Steps | 1. Load application. 2. Record card count. 3. Click Delete on a release. 4. Dismiss the confirmation dialog (Cancel). 5. Count cards. |
| Expected Result | Card count is unchanged. The release remains visible in the DOM. |
| Automation | AUTO — `alert.dismiss()` then assert card still present |

---

#### TS-N-002 | TC-010 — Cancelling confirmation leaves localStorage unchanged

| Field | Value |
|---|---|
| TC ID | TC-010 |
| Scenario ID | TS-N-002 |
| Priority | HIGH |
| Requirement(s) | REQ-006 |
| Acceptance Criteria | AC-3 |
| Precondition | At least one release exists; localStorage contains the release |
| Steps | 1. Load application. 2. Read localStorage snapshot. 3. Click Delete on a release. 4. Cancel the confirmation dialog. 5. Read localStorage again. |
| Expected Result | localStorage content is byte-for-byte identical before and after the cancelled operation. |
| Automation | AUTO — compare localStorage JSON before and after |

---

#### TS-N-003 | TC-011 — Dismissing dialog via Escape key has same effect as Cancel

| Field | Value |
|---|---|
| TC ID | TC-011 |
| Scenario ID | TS-N-003 |
| Priority | HIGH |
| Requirement(s) | REQ-006 |
| Acceptance Criteria | AC-3 |
| Precondition | At least one release exists |
| Steps | 1. Load application. 2. Click Delete on a release. 3. Press Escape (dismiss dialog, equivalent to Cancel). 4. Assert release remains. |
| Expected Result | Release remains in UI and localStorage. No state change occurred. |
| Automation | AUTO — Selenium `alert.dismiss()` (same path as TC-009); cover NEG-002 |

---

#### TS-N-004 | TC-012 — Deletion attempt with non-existent release ID is handled safely

| Field | Value |
|---|---|
| TC ID | TC-012 |
| Scenario ID | TS-N-004 |
| Priority | MEDIUM |
| Requirement(s) | REQ-003, REQ-004 (data validation impact) |
| Acceptance Criteria | AC-2 (verify safe no-op) |
| Precondition | Application is loaded; a stale/invalid ID is constructed in test |
| Steps | 1. Load application with known releases. 2. Inject a `deleteRelease("non-existent-id")` call via JS executor. 3. Assert releases array is unchanged. |
| Expected Result | `releases` array length is unchanged. localStorage is unchanged. No UI error. `deleteRelease()` silently no-ops (filter produces same array). |
| Automation | MANUAL — requires direct JS injection; not a standard UI path; verify via browser console in first run |

---

#### TS-N-005 | TC-013 — Rapid successive deletes do not corrupt state

| Field | Value |
|---|---|
| TC ID | TC-013 |
| Scenario ID | TS-N-005 |
| Priority | LOW |
| Requirement(s) | REQ-003, REQ-004 |
| Acceptance Criteria | AC-2 |
| Precondition | 3+ releases exist |
| Steps | 1. Load application with 3 releases. 2. Delete release 1 and confirm. 3. Immediately delete release 2 and confirm (no wait). 4. Assert state. |
| Expected Result | Both deletions succeed. Remaining releases are intact. localStorage reflects correct reduced array. No corruption. |
| Automation | AUTO — sequential confirm accepts with minimal wait |

---

### 7.3 Boundary Scenarios

**Priority**: HIGH (TC-014 to TC-016, TC-018), MEDIUM (TC-017)
**Automation Suitability**: AUTO

---

#### TS-B-001 | TC-014 — Delete the only remaining release renders empty state

| Field | Value |
|---|---|
| TC ID | TC-014 |
| Scenario ID | TS-B-001 |
| Priority | HIGH |
| Requirement(s) | REQ-003, REQ-004, REQ-005 (BC-001) |
| Acceptance Criteria | AC-2 |
| Precondition | Exactly one release exists in the list |
| Steps | 1. Load application with exactly 1 release. 2. Delete the release and confirm. 3. Observe list area. |
| Expected Result | Release list is empty. Empty-state UI element is displayed (or container is empty). localStorage array is `[]`. |
| Automation | AUTO — assert card count = 0; assert empty-state element visible; read localStorage |

---

#### TS-B-002 | TC-015 — Delete the first release in the list

| Field | Value |
|---|---|
| TC ID | TC-015 |
| Scenario ID | TS-B-002 |
| Priority | HIGH |
| Requirement(s) | REQ-003, REQ-005 (BC-002) |
| Acceptance Criteria | AC-2 |
| Precondition | 3 releases exist; first is identified by position |
| Steps | 1. Load application with 3 releases (A, B, C in order). 2. Delete release A (first card). 3. Accept confirmation. 4. Verify remaining list. |
| Expected Result | Release A is removed. Releases B and C remain in DOM and localStorage in correct order. |
| Automation | AUTO — assert first card is now B; assert count = 2 |

---

#### TS-B-003 | TC-016 — Delete the last release in the list

| Field | Value |
|---|---|
| TC ID | TC-016 |
| Scenario ID | TS-B-003 |
| Priority | HIGH |
| Requirement(s) | REQ-003, REQ-005 (BC-003) |
| Acceptance Criteria | AC-2 |
| Precondition | 3 releases exist |
| Steps | 1. Load application with 3 releases (A, B, C in order). 2. Delete release C (last card). 3. Accept confirmation. 4. Verify remaining list. |
| Expected Result | Release C is removed. Releases A and B remain in DOM and localStorage. Order is unchanged. |
| Automation | AUTO — assert last card is now B; assert count = 2 |

---

#### TS-B-004 | TC-017 — Active filter is preserved after deletion triggers re-render

| Field | Value |
|---|---|
| TC ID | TC-017 |
| Scenario ID | TS-B-004 |
| Priority | MEDIUM |
| Requirement(s) | REQ-005 (BC-006, regression filter risk) |
| Acceptance Criteria | AC-2 |
| Precondition | 3 releases exist; at least 2 match a filter value |
| Steps | 1. Load application. 2. Apply a product/team filter so only 2 releases are shown. 3. Delete one of the visible (matching) releases and confirm. 4. Observe the filtered list. |
| Expected Result | Active filter remains applied. Only matching non-deleted releases are shown. Non-matching releases remain hidden. |
| Automation | AUTO — assert filter value still selected; assert hidden cards are still hidden |

---

#### TS-B-005 | TC-018 — Deleted release absent after multiple page reloads

| Field | Value |
|---|---|
| TC ID | TC-018 |
| Scenario ID | TS-B-005 |
| Priority | HIGH |
| Requirement(s) | REQ-004 (BC-005) |
| Acceptance Criteria | AC-2 |
| Precondition | At least one release exists |
| Steps | 1. Load application. 2. Delete a release and confirm. 3. Reload once — assert deleted release absent. 4. Reload again — assert deleted release still absent. |
| Expected Result | Deleted release does not reappear after 2 consecutive page reloads. localStorage remains consistent. |
| Automation | AUTO — two sequential `driver.refresh()` calls with assertions after each |

---

### 7.4 Regression Scenarios

**Priority**: HIGH (TC-019, TC-021, TC-022), MEDIUM (TC-020, TC-023, TC-024)
**Automation Suitability**: BOTH (AUTO where existing POM steps cover; MANUAL for cross-tab)

---

#### TS-R-001 | TC-019 — Create/add release still persists after delete code changes

| Field | Value |
|---|---|
| TC ID | TC-019 |
| Scenario ID | TS-R-001 |
| Priority | HIGH |
| Requirement(s) | REQ-004 (regression: `saveReleases()`) |
| Acceptance Criteria | AC-2 |
| Precondition | Application is loaded with no pre-existing releases |
| Steps | 1. Create a new release via the Add form. 2. Reload the page. 3. Verify the release is present. 4. Delete the release. 5. Create another new release. 6. Reload and verify it persists. |
| Expected Result | Created releases persist to localStorage correctly. `saveReleases()` is not broken by the delete feature. |
| Automation | AUTO — reuse existing create/reload steps from COD-9 suite |

---

#### TS-R-002 | TC-020 — Edit release is unaffected when a different release is deleted

| Field | Value |
|---|---|
| TC ID | TC-020 |
| Scenario ID | TS-R-002 |
| Priority | MEDIUM |
| Requirement(s) | REQ-003, REQ-005 (regression: `resetEditMode()`) |
| Acceptance Criteria | AC-2 |
| Precondition | 2+ releases exist |
| Steps | 1. Load application with releases A and B. 2. Click Edit on release A (open edit form with A's data). 3. Delete release B and confirm. 4. Verify edit form still shows A's data. 5. Verify release A is unchanged in DOM and localStorage. |
| Expected Result | Edit form retains release A's data. `resetEditMode()` is NOT called when deleting a different release. Release A is unmodified. |
| Automation | AUTO — assert form field values match release A's data after delete of B |

---

#### TS-R-003 | TC-021 — Filter/search results are correct after a deletion

| Field | Value |
|---|---|
| TC ID | TC-021 |
| Scenario ID | TS-R-003 |
| Priority | HIGH |
| Requirement(s) | REQ-005 (regression: `renderReleaseList()` with filter) |
| Acceptance Criteria | AC-2 |
| Precondition | 3+ releases; search/filter input is available |
| Steps | 1. Load application. 2. Enter a search term that matches 2 out of 3 releases. 3. Verify filter shows 2 cards. 4. Delete one matching release and confirm. 5. Re-enter the same search term. |
| Expected Result | Filter correctly shows 1 matching card (deleted card is gone). Non-matching release remains hidden. `renderReleaseList()` correctly re-applies filter state. |
| Automation | AUTO — reuse filter steps; assert count and card identity |

---

#### TS-R-004 | TC-022 — JSON export (COD-9) does not include deleted release

| Field | Value |
|---|---|
| TC ID | TC-022 |
| Scenario ID | TS-R-004 |
| Priority | HIGH |
| Requirement(s) | REQ-004 (regression: COD-9 export reads `releases` array) |
| Acceptance Criteria | AC-2 |
| Precondition | 2+ releases exist; JSON export button is present |
| Steps | 1. Load application with releases A and B. 2. Delete release A and confirm. 3. Trigger JSON export. 4. Inspect exported data. |
| Expected Result | Exported JSON contains only release B. Release A is absent. Export file/download reflects the post-deletion state. |
| Automation | AUTO — reuse COD-9 export step; parse exported content to assert release A absent |

---

#### TS-R-005 | TC-023 — App shows correct state when all releases are deleted and page is reloaded

| Field | Value |
|---|---|
| TC ID | TC-023 |
| Scenario ID | TS-R-005 |
| Priority | MEDIUM |
| Requirement(s) | REQ-004, REQ-005 (regression: seed data / empty state on reload) |
| Acceptance Criteria | AC-2 |
| Precondition | Exactly 1 release exists (or test deletes all releases sequentially) |
| Steps | 1. Load application. 2. Delete all existing releases (confirm each). 3. Reload the page. 4. Observe application state. |
| Expected Result | Application loads without errors. Either: (a) empty state is shown and localStorage is `[]`, or (b) seed data is re-applied consistently. Behaviour is deterministic and error-free. |
| Automation | AUTO — delete all; reload; assert no JS errors; assert deterministic empty/seed state |

---

#### TS-R-006 | TC-024 — Cross-tab: deletion in one tab is reflected after reload of a second tab

| Field | Value |
|---|---|
| TC ID | TC-024 |
| Scenario ID | TS-R-006 |
| Priority | MEDIUM |
| Requirement(s) | REQ-004 (regression: localStorage cross-tab consistency) |
| Acceptance Criteria | AC-2 |
| Precondition | Application is open in two browser windows/tabs |
| Steps | 1. Open app in tab 1. 2. Open app in tab 2 (same file:// URL). 3. Delete a release in tab 1 and confirm. 4. Reload tab 2. 5. Verify the deleted release is absent in tab 2. |
| Expected Result | After reload, tab 2 reads the updated localStorage and does not show the deleted release. |
| Automation | MANUAL — multi-window Selenium requires additional test harness setup not currently in POM; automate in future sprint |

---

## 8. Traceability Matrix

| TC ID | Scenario ID | REQ(s) | AC | Boundary/Negative Ref |
|---|---|---|---|---|
| TC-001 | TS-P-001 | REQ-001 | AC-1 | — |
| TC-002 | TS-P-002 | REQ-002 | AC-1 | — |
| TC-003 | TS-P-003 | REQ-003, REQ-005 | AC-2 | — |
| TC-004 | TS-P-004 | REQ-004 | AC-2 | — |
| TC-005 | TS-P-005 | REQ-003, REQ-005 | AC-2 | — |
| TC-006 | TS-P-006 | REQ-003, REQ-005 | AC-2 | — |
| TC-007 | TS-P-007 | REQ-004 | AC-2 | BC-005 |
| TC-008 | TS-P-008 | REQ-003, REQ-004, REQ-005 | AC-2 | BC-004 |
| TC-009 | TS-N-001 | REQ-006 | AC-3 | NEG-001 |
| TC-010 | TS-N-002 | REQ-006 | AC-3 | NEG-004 |
| TC-011 | TS-N-003 | REQ-006 | AC-3 | NEG-002 |
| TC-012 | TS-N-004 | REQ-003, REQ-004 | AC-2 | NEG-003 |
| TC-013 | TS-N-005 | REQ-003, REQ-004 | AC-2 | — |
| TC-014 | TS-B-001 | REQ-003, REQ-004, REQ-005 | AC-2 | BC-001 |
| TC-015 | TS-B-002 | REQ-003, REQ-005 | AC-2 | BC-002 |
| TC-016 | TS-B-003 | REQ-003, REQ-005 | AC-2 | BC-003 |
| TC-017 | TS-B-004 | REQ-005 | AC-2 | BC-006 |
| TC-018 | TS-B-005 | REQ-004 | AC-2 | BC-005 |
| TC-019 | TS-R-001 | REQ-004 | AC-2 | — |
| TC-020 | TS-R-002 | REQ-003, REQ-005 | AC-2 | BC-004 |
| TC-021 | TS-R-003 | REQ-005 | AC-2 | — |
| TC-022 | TS-R-004 | REQ-004 | AC-2 | — |
| TC-023 | TS-R-005 | REQ-004, REQ-005 | AC-2 | BC-001 |
| TC-024 | TS-R-006 | REQ-004 | AC-2 | — |

**Coverage summary**: REQ-001 (1 TC), REQ-002 (1 TC), REQ-003 (8 TC), REQ-004 (10 TC), REQ-005 (8 TC), REQ-006 (3 TC).

---

## 9. Test Data Requirements

| Data Item | Value / Description | Source | Status |
|---|---|---|---|
| Release record (standard) | `{id, product, version, teamName, title, description, releaseDate, isBreaking}` | Test setup via `before_scenario()` or direct localStorage injection | AVAILABLE — structure known from discovery |
| Release record — minimum valid | All required fields populated; `isBreaking: false` | Test setup | AVAILABLE |
| Release record — breaking change | `isBreaking: true` | Test setup | AVAILABLE |
| Multi-release dataset (3 records) | Three releases with distinct IDs, products, and titles | Test setup | AVAILABLE — can be generated programmatically |
| Single-release dataset (1 record) | Used for TC-014 (delete-only-release) | Test setup | AVAILABLE |
| Empty localStorage state | `releaseNotesDashboard.releases` absent or `[]` | `before_scenario()` hook clears localStorage | AVAILABLE — hook exists |
| Pre-populated localStorage state | Used for reload persistence tests (TC-007, TC-018, TC-023) | Written by `saveReleases()` in earlier test steps | AVAILABLE |
| Non-existent release ID | Any UUID not present in `releases` array | Constructed in test (TC-012) | AVAILABLE — generated at runtime |
| Filter/search term | A string matching a subset of test releases | Hardcoded in test data definition | **FLAG: specific filter term must be agreed with automation agent; filter field name/selector to be confirmed from POM** |

---

## 10. Environment Requirements

| Requirement | Detail | Status |
|---|---|---|
| Browser | Microsoft Edge (Chromium-based) | AVAILABLE — existing test infrastructure |
| WebDriver | Microsoft Edge WebDriver (msedgedriver) | AVAILABLE — configured in automation suite |
| WebDriver flag | `--allow-file-access-from-files` (required for file:// localStorage) | AVAILABLE — confirmed in discovery |
| Application access | `file://<absolute-path>/product_release_dashboard/index.html` | AVAILABLE — existing `BASE_URL` in POM |
| Test framework | Behave (Python) with Selenium | AVAILABLE — established in COD-9 |
| Page Object Model | `automation/pages/release_dashboard_page.py` | AVAILABLE — minor additions may be needed for delete-specific methods |
| localStorage helpers | `automation/utils/helpers.py` — `clear_local_storage()`, `remove_local_storage_key()` | AVAILABLE — confirmed in discovery |
| Alert handling | `driver.switch_to.alert` + `alert.accept()` / `alert.dismiss()` | AVAILABLE — POM lines 184–187 |
| `before_scenario()` hook | Clears localStorage and reloads app before each scenario | AVAILABLE — `automation/environment.py` |
| `after_step()` hook | Captures screenshot on failure | AVAILABLE — `automation/environment.py` |
| Selenium explicit waits | `WebDriverWait` + `expected_conditions` for post-deletion DOM assertions | AVAILABLE — standard Selenium; **FLAG: wait timeout values must be confirmed or set in POM config** |

---

## 11. Entry Criteria

1. `artifacts/COD-8/requirements/requirement-analysis.md` and `artifacts/COD-8/impact/impact-analysis.md` are approved (or accepted for automation).
2. Application code (`index.html`, `script.js`, `styles.css`) reflects the COD-8 feature implementation (delete button and `deleteRelease()` function present and functional).
3. Automation infrastructure is operational: Behave, Edge WebDriver, and POM are executable without errors.
4. `before_scenario()` hook correctly clears localStorage before each test.
5. Alert handling (`alert.accept()` / `alert.dismiss()`) has been smoke-tested against the file:// URL.

---

## 12. Exit Criteria

1. All CRITICAL and HIGH priority test cases (TC-001 to TC-011, TC-014 to TC-019, TC-021, TC-022) are executed.
2. Pass rate for CRITICAL scenarios (TC-001 to TC-005): 100%.
3. Pass rate for HIGH scenarios: >= 95% (at most 1 non-blocker failure).
4. All MEDIUM and LOW priority scenarios executed or explicitly deferred with documented justification.
5. No open P1 / P2 defects against REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006.
6. Traceability matrix (`artifacts/COD-8/traceability/traceability-matrix.md`) is complete and each REQ is covered by at least one passing TC.
7. TC-024 (cross-tab, MANUAL) either executed manually or explicitly deferred to a future sprint with a Jira ticket.

---

## 13. Dependencies

| Dependency | Type | Owner | Risk if Absent |
|---|---|---|---|
| COD-8 feature implementation in `script.js` | Application code | Development team | Tests cannot execute — blocking |
| Edge WebDriver compatible with installed Edge version | Infrastructure | Test environment owner | Tests cannot launch — blocking |
| `before_scenario()` localStorage clear hook | Test framework | Automation engineer | Test isolation breaks; false positives/negatives |
| Alert handling already working on file:// URL | POM capability | Automation engineer | TC-002 to TC-008, TC-009 to TC-011 cannot auto-pass — HIGH risk |
| COD-9 export feature and its automation steps | Regression dependency | COD-9 story | TC-022 cannot run without export functionality — HIGH |
| Filter/search UI selectors confirmed in POM | POM configuration | Automation engineer | TC-017, TC-021 cannot run — MEDIUM |

---

## 14. Risks and Mitigations

| Risk ID | Risk Description | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| RISK-001 | `window.confirm()` alert not interceptable by Selenium on file:// URL | MEDIUM | HIGH | POM already has `switch_to.alert` logic; run TC-002 first as a canary; fail fast if unsupported |
| RISK-002 | localStorage file:// scoping differs from HTTP; data not isolated per-test | LOW | HIGH | `before_scenario()` clears localStorage; `--allow-file-access-from-files` flag set |
| RISK-003 | DOM not updated before Selenium assertion (timing / flakiness) | MEDIUM | MEDIUM | Use `WebDriverWait` for card staleness / invisibility; tune timeout in POM config |
| RISK-004 | Seed data reapply after delete-all creates non-deterministic state (TC-023) | MEDIUM | MEDIUM | Assert either empty state OR seeded state; document expected behaviour before automating |
| RISK-005 | `saveReleases()` silent failure causes in-memory/localStorage divergence | LOW | HIGH | Always assert both DOM count and localStorage array length together |
| RISK-006 | Filter field selector not present in current POM (TC-017, TC-021 blocked) | MEDIUM | MEDIUM | Automation agent must add POM method before implementing these TCs |
| RISK-007 | TC-012 (non-existent ID) not automatable via standard UI flow | HIGH | LOW | Mark as MANUAL; document JS executor approach; deprioritise |
| RISK-008 | TC-024 (cross-tab) not supported by current single-driver setup | HIGH | LOW | Mark as MANUAL; open Jira for future sprint |

---

## 15. Assumptions

| Assumption ID | Description |
|---|---|
| ASS-001 | The confirmation mechanism is `window.confirm()` (native browser dialog); no custom modal dialog is required. |
| ASS-002 | The `releases` array in `script.js` is the sole in-memory source of truth for all release data. |
| ASS-003 | localStorage key `releaseNotesDashboard.releases` holds the full JSON-serialised releases array. |
| ASS-004 | `before_scenario()` in `environment.py` clears localStorage and reloads the app before every scenario; no residual state leaks between tests. |
| ASS-005 | Test execution is serial (not parallel); shared localStorage is safe under serial execution. |
| ASS-006 | Automation uses the Behave + Selenium + Edge WebDriver stack established for COD-9; no framework changes required. |
| ASS-007 | The POM (`release_dashboard_page.py`) will be extended by the Automation Agent to add delete-specific methods (`click_delete_button(release_id)`, `accept_delete_confirmation()`, `dismiss_delete_confirmation()`). |
| ASS-008 | COD-9 JSON export automation steps are available and reusable for TC-022. |
| ASS-009 | Seed data behaviour on reload after delete-all (TC-023) will be clarified before that scenario is automated; deterministic expected result must be documented. |

---

## 16. Priority Summary

| Group | TC IDs | Priority | Scenarios | Automation |
|---|---|---|---|---|
| Positive (smoke + core) | TC-001 to TC-005 | CRITICAL | TS-P-001 to TS-P-005 | AUTO |
| Positive (extended) | TC-006 to TC-008 | HIGH | TS-P-006 to TS-P-008 | AUTO |
| Negative | TC-009 to TC-011 | HIGH | TS-N-001 to TS-N-003 | AUTO |
| Negative | TC-012 | MEDIUM | TS-N-004 | MANUAL |
| Negative | TC-013 | LOW | TS-N-005 | AUTO |
| Boundary | TC-014 to TC-016, TC-018 | HIGH | TS-B-001 to TS-B-003, TS-B-005 | AUTO |
| Boundary | TC-017 | MEDIUM | TS-B-004 | AUTO |
| Regression | TC-019, TC-021, TC-022 | HIGH | TS-R-001, TS-R-003, TS-R-004 | AUTO |
| Regression | TC-020, TC-023 | MEDIUM | TS-R-002, TS-R-005 | AUTO |
| Regression | TC-024 | MEDIUM | TS-R-006 | MANUAL |

**Total test cases: 24** (TC-001 to TC-024)
- CRITICAL: 5
- HIGH: 13
- MEDIUM: 5
- LOW: 1
- AUTO: 21 | MANUAL: 3 (TC-012, TC-024; TC-023 deferred pending seed-data clarification)
