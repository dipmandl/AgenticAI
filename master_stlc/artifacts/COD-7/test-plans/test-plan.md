# Test Plan: COD-7 — Edit Existing Release Note

---

## Test Plan ID
**TP-001**

---

## Story and Requirement References

| Reference | Value |
|---|---|
| Story ID | COD-7 |
| Story Title | Edit Existing Release Note |
| Story URL | https://mandlikdipak52.atlassian.net/browse/COD-7 |
| Requirement Analysis | `artifacts/COD-7/requirements/requirement-analysis.md` |
| Impact Analysis | `artifacts/COD-7/impact/impact-analysis.md` |
| Requirements Covered | REQ-001 through REQ-012 (12 total) |
| Acceptance Criteria Covered | AC-1 through AC-4 (4 total) |
| Test Plan Date | 2026-10-30 |
| Risk Level | MEDIUM |

---

## Scope

The following functionality is in scope for this test plan:

1. **Edit button visibility** — Each rendered release card displays an Edit button (REQ-001).
2. **Form pre-fill on Edit** — Clicking Edit opens the existing inline form pre-filled with all seven field values: product, version, teamName, title, description, releaseDate, isBreaking (REQ-002).
3. **Field editability** — All pre-filled fields are editable by the user (REQ-003).
4. **Save action** — Form provides a Save / "Update Release Note" action (REQ-004).
5. **Cancel action** — Form provides a Cancel action to discard changes (REQ-005).
6. **In-place update by id** — Save updates the matching release by id; no new entry created, no other entries modified (REQ-006).
7. **localStorage persistence on Save** — Updated list is persisted to `releaseNotesDashboard.releases` (REQ-007).
8. **List re-render on Save** — Release list re-renders to reflect updated values (REQ-008).
9. **Cancel leaves state unchanged** — Cancelling edit does not modify the list or localStorage (REQ-009).
10. **Filter persistence after Save** — Product filter, breaking-change filter, and keyword search remain applied after Save (REQ-010).
11. **Filter persistence after Cancel** — Same three filters remain applied after Cancel (REQ-011).
12. **Position independence** — Edit operates correctly regardless of card position in the list (REQ-012).
13. **Form state synchronisation** — Editing multiple cards in sequence produces correct pre-fill each time.
14. **Validation on update** — Same mandatory-field validation rules apply to Save in edit mode as in create mode (per impact analysis mitigation for AMB-001).

---

## Out of Scope

The following are explicitly excluded from this test plan:

- Multi-user / concurrent editing scenarios
- Undo / redo after a Save
- Audit trail or history of edits
- Back-end persistence (application is client-side only; no HTTP calls)
- Creating new release notes (covered by a separate story)
- Deleting release notes (separate story) — _except_ regression checks that delete still works after an edit
- CSV export / JSON import functional behaviour — _except_ regression checks that they still function after an edit
- Authentication and authorisation
- Smoke testing (story is a feature, not critical infrastructure)
- Security / XSS / injection testing
- Performance / load / stress testing
- Accessibility beyond functional keyboard navigation
- Edit mode visual indicator (flagged as AMB-002; no requirement confirmed)
- Scroll-into-view behaviour (flagged as AMB-004; cosmetic, not testable as a pass/fail acceptance criterion)

---

## Impacted Areas

Derived from `artifacts/COD-7/impact/impact-analysis.md`.

| Area | File | Change Type | Risk |
|---|---|---|---|
| `startEdit(id)` | script.js | Enhanced — pre-fills all 7 fields, sets edit state | HIGH |
| Form submit handler (update branch) | script.js | New — in-place update by id when `editingReleaseId` is set | HIGH |
| `resetEditMode()` | script.js | Reused unchanged (Cancel, form clear) | MEDIUM |
| `saveReleases()` | script.js | Reused unchanged (localStorage write) | MEDIUM |
| `renderReleaseList()` / `getFilteredReleases()` | script.js | Reused unchanged (filter-aware re-render) | MEDIUM |
| Form markup `#release-form` | index.html | Structure unchanged; reused for edit | LOW |
| Submit button text | index.html / script.js | Text toggled dynamically | LOW |
| Cancel Edit button visibility | index.html / script.js | Show/hide toggled | LOW |
| styles.css | styles.css | Minor button state styling; no breaking changes | LOW |

---

## Test Categories

| Category | Applicable | Automation Suitability | Priority |
|---|---|---|---|
| Functional / UI | YES | BOTH | HIGH |
| E2E (click-to-render) | YES | BOTH | HIGH |
| Integration (form + storage + render chain) | YES | AUTO | HIGH |
| Negative (validation failures, invalid state) | YES | BOTH | HIGH |
| Boundary (edge values, sequential edits) | YES | BOTH | MEDIUM |
| Regression (Create, Delete, Filter, Export, Import) | YES | AUTO | HIGH |
| API | NO | — | — |
| Security | NO | — | — |
| Performance | NO | — | — |
| Smoke | NO | — | — |

---

## Test Scenarios

### Summary Table

| Scenario ID | Category | Title | Linked REQs | Priority |
|---|---|---|---|---|
| TS-P-001 | Positive | Edit button visible on each release card | REQ-001 | HIGH |
| TS-P-002 | Positive | Clicking Edit pre-fills all 7 fields | REQ-002, AC-1 | CRITICAL |
| TS-P-003 | Positive | isBreaking checkbox pre-fills as checked when release is breaking | REQ-002, AC-1 | HIGH |
| TS-P-004 | Positive | isBreaking checkbox pre-fills as unchecked when release is non-breaking | REQ-002, AC-1 | HIGH |
| TS-P-005 | Positive | Save action is available with label "Update Release Note" in edit mode | REQ-004 | HIGH |
| TS-P-006 | Positive | Cancel action is available in edit mode | REQ-005 | HIGH |
| TS-P-007 | Positive | Save updates the specific release by id | REQ-006, AC-2 | CRITICAL |
| TS-P-008 | Positive | Save does not create a duplicate entry | REQ-006, AC-2 | CRITICAL |
| TS-P-009 | Positive | Save does not modify any other release entries | REQ-006, AC-2 | HIGH |
| TS-P-010 | Positive | Updated list is persisted to localStorage after Save | REQ-007 | CRITICAL |
| TS-P-011 | Positive | Release list re-renders with updated values after Save | REQ-008 | HIGH |
| TS-P-012 | Positive | Cancel discards in-progress changes — rendered list unchanged | REQ-009, AC-3 | CRITICAL |
| TS-P-013 | Positive | Cancel leaves localStorage unchanged | REQ-009, AC-3 | HIGH |
| TS-P-014 | Positive | All active filters remain applied after Save | REQ-010, AC-4 | CRITICAL |
| TS-P-015 | Positive | All active filters remain applied after Cancel | REQ-011, AC-4 | HIGH |
| TS-P-016 | Positive | Edit operates correctly on the first card in the list | REQ-012 | MEDIUM |
| TS-P-017 | Positive | Edit operates correctly on the last card in the list | REQ-012 | MEDIUM |
| TS-P-018 | Positive | Edit operates correctly on a middle card in the list | REQ-012 | MEDIUM |
| TS-N-001 | Negative | Cancel without modifying any field — list and localStorage unchanged | REQ-009 | HIGH |
| TS-N-002 | Negative | Save with teamName cleared — validation error, edit state preserved | REQ-004, AMB-001 | HIGH |
| TS-N-003 | Negative | Save with title cleared — validation error shown | REQ-004 | HIGH |
| TS-N-004 | Negative | Save with product cleared — validation error shown | REQ-004 | HIGH |
| TS-N-005 | Negative | Save with version cleared — validation error shown | REQ-004 | HIGH |
| TS-N-006 | Negative | Save with releaseDate cleared — validation error shown | REQ-004 | HIGH |
| TS-N-007 | Negative | startEdit called with non-existent id — no form pre-fill, no crash | REQ-006 | HIGH |
| TS-N-008 | Negative | Clicking Edit on card B while card A is in edit mode — form replaces to card B | AMB-003, REQ-002 | MEDIUM |
| TS-N-009 | Negative | Cancel after a validation failure — edit mode exits cleanly | REQ-005, REQ-009 | HIGH |
| TS-B-001 | Boundary | Edit with all 7 fields modified then Save | REQ-002, REQ-006 | HIGH |
| TS-B-002 | Boundary | Edit with exactly one field changed then Save | REQ-006 | MEDIUM |
| TS-B-003 | Boundary | Edit: set teamName to empty (optional field) and Save | REQ-002, REQ-003 | MEDIUM |
| TS-B-004 | Boundary | Edit with minimum-length valid values in all mandatory fields | REQ-002, REQ-006 | MEDIUM |
| TS-B-005 | Boundary | Edit + Cancel + re-Edit same card — form shows original values | REQ-002, REQ-009 | HIGH |
| TS-B-006 | Boundary | Edit card A, Cancel, Edit card B — form shows B's values only | REQ-002 | HIGH |
| TS-B-007 | Boundary | Edit title/description with maximum-length text | REQ-003 | LOW |
| TS-B-008 | Boundary | Edit text fields with special characters | REQ-003 | LOW |
| TS-B-009 | Boundary | Toggle isBreaking from true to false during edit and Save | REQ-002, REQ-006 | HIGH |
| TS-B-010 | Boundary | Toggle isBreaking from false to true during edit and Save | REQ-002, REQ-006 | HIGH |
| TS-B-011 | Boundary | Edit when list contains exactly one entry | REQ-012 | MEDIUM |
| TS-B-012 | Boundary | Edit with no filters active (baseline state) | REQ-010 | MEDIUM |
| TS-R-001 | Regression | Create new release still works after Edit + Save | REQ-006 | HIGH |
| TS-R-002 | Regression | Create new release still works after Edit + Cancel | REQ-009 | HIGH |
| TS-R-003 | Regression | Delete a different release still works after Edit + Save | REQ-006 | HIGH |
| TS-R-004 | Regression | Deleting the release currently in edit mode resets edit state | REQ-009 | HIGH |
| TS-R-005 | Regression | Product filter still applies correctly after Edit + Save | REQ-010 | HIGH |
| TS-R-006 | Regression | Breaking-change filter still applies correctly after Edit + Save | REQ-010 | HIGH |
| TS-R-007 | Regression | Keyword search filter still applies correctly after Edit + Save | REQ-010 | HIGH |
| TS-R-008 | Regression | Multi-filter combination persists after Edit + Save | REQ-010 | HIGH |
| TS-R-009 | Regression | Edited values persist across page reload (localStorage) | REQ-007 | HIGH |
| TS-R-010 | Regression | Export CSV still works after Edit + Save | REQ-007 | MEDIUM |
| TS-R-011 | Regression | Import JSON while in edit mode resets edit state | REQ-009 | MEDIUM |
| TS-R-012 | Regression | Form in create mode (editingReleaseId = null) still creates new entry | REQ-006 | HIGH |

---

### Positive Scenarios

---

#### TS-P-001
- **Category**: Positive
- **Title**: Edit button visible on each release card
- **Linked Requirements**: REQ-001
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. At least two release notes exist in the list.
- **Steps**:
  1. Inspect every rendered release card in the list.
  2. Verify that each card contains an Edit button (or equivalent action element).
- **Expected Result**: Every rendered release card has a visible Edit button. No card is missing the Edit action.

---

#### TS-P-002
- **Category**: Positive
- **Title**: Clicking Edit pre-fills all 7 fields
- **Linked Requirements**: REQ-002, AC-1
- **Priority**: CRITICAL
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. At least one release note exists with known values for all 7 fields (product, version, teamName, title, description, releaseDate, isBreaking).
- **Steps**:
  1. Record the current values of all 7 fields for a target release card.
  2. Click the Edit button on that card.
  3. Inspect each of the 7 form inputs.
- **Expected Result**: `#product-input` shows the release's product; `#version-input` shows version; `#team-name-input` shows teamName; `#title-input` shows title; `#description-input` shows description; `#release-date-input` shows releaseDate (YYYY-MM-DD); `#is-breaking-input` reflects the isBreaking boolean. All 7 fields match the release data exactly.

---

#### TS-P-003
- **Category**: Positive
- **Title**: isBreaking checkbox pre-fills as checked when release is breaking
- **Linked Requirements**: REQ-002, AC-1
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: A release note with `isBreaking = true` exists in the list.
- **Steps**:
  1. Click Edit on the release with `isBreaking = true`.
  2. Inspect `#is-breaking-input`.
- **Expected Result**: The `#is-breaking-input` checkbox is checked (`.checked === true`).

---

#### TS-P-004
- **Category**: Positive
- **Title**: isBreaking checkbox pre-fills as unchecked when release is non-breaking
- **Linked Requirements**: REQ-002, AC-1
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: A release note with `isBreaking = false` exists in the list.
- **Steps**:
  1. Click Edit on the release with `isBreaking = false`.
  2. Inspect `#is-breaking-input`.
- **Expected Result**: The `#is-breaking-input` checkbox is unchecked (`.checked === false`).

---

#### TS-P-005
- **Category**: Positive
- **Title**: Save action is available with label "Update Release Note" in edit mode
- **Linked Requirements**: REQ-004
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. A release note exists in the list.
- **Steps**:
  1. Click Edit on a release card.
  2. Inspect the form's primary action button.
- **Expected Result**: The submit / primary action button is visible and its text reads "Update Release Note" (not "Add Release Note"). The button is enabled and clickable.

---

#### TS-P-006
- **Category**: Positive
- **Title**: Cancel action is available in edit mode
- **Linked Requirements**: REQ-005
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. A release note exists in the list.
- **Steps**:
  1. Click Edit on a release card.
  2. Inspect the form for a Cancel / "Cancel Edit" button.
- **Expected Result**: A Cancel (or "Cancel Edit") button is visible and clickable. In normal (create) mode this button is hidden; in edit mode it is shown.

---

#### TS-P-007
- **Category**: Positive
- **Title**: Save updates the specific release by id
- **Linked Requirements**: REQ-006, AC-2
- **Priority**: CRITICAL
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. A release note with known id and field values exists. Note the original field values.
- **Steps**:
  1. Click Edit on the target release card.
  2. Change one or more field values (e.g., update the title).
  3. Click Save / "Update Release Note".
  4. Locate the release entry in the rendered list and in `localStorage` by its original id.
- **Expected Result**: The release entry with the original id now shows the updated field values in both the rendered list and in `localStorage`. The id value is unchanged.

---

#### TS-P-008
- **Category**: Positive
- **Title**: Save does not create a duplicate entry
- **Linked Requirements**: REQ-006, AC-2
- **Priority**: CRITICAL
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. Exactly N release notes exist. Note the count N.
- **Steps**:
  1. Click Edit on one release card.
  2. Change a field value.
  3. Click Save.
  4. Count the total number of release entries in the rendered list and in `localStorage`.
- **Expected Result**: The total count remains N (no new entry added). The list contains exactly the same entries as before with one updated.

---

#### TS-P-009
- **Category**: Positive
- **Title**: Save does not modify any other release entries
- **Linked Requirements**: REQ-006, AC-2
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. At least two release notes exist. Record all field values for all entries except the target.
- **Steps**:
  1. Click Edit on the target release card.
  2. Modify several fields.
  3. Click Save.
  4. Inspect the field values of all other (non-target) release entries in the rendered list and `localStorage`.
- **Expected Result**: All non-target release entries have unchanged field values. Only the target entry reflects the edit.

---

#### TS-P-010
- **Category**: Positive
- **Title**: Updated list is persisted to localStorage after Save
- **Linked Requirements**: REQ-007
- **Priority**: CRITICAL
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. A release note exists with known field values.
- **Steps**:
  1. Click Edit on a release card.
  2. Change the title to a distinct test value.
  3. Click Save.
  4. Read `localStorage.getItem('releaseNotesDashboard.releases')` and parse the JSON.
  5. Find the entry by id.
- **Expected Result**: The entry in `localStorage` has the new title value. The entire releases array is present and well-formed JSON.

---

#### TS-P-011
- **Category**: Positive
- **Title**: Release list re-renders with updated values after Save
- **Linked Requirements**: REQ-008
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. A release note exists.
- **Steps**:
  1. Note the current rendered title of a release card.
  2. Click Edit on that card.
  3. Change the title to a new distinct value.
  4. Click Save.
  5. Inspect the rendered release list for the updated card.
- **Expected Result**: The release card in the DOM shows the new title value immediately after Save. No page reload is required.

---

#### TS-P-012
- **Category**: Positive
- **Title**: Cancel discards in-progress changes — rendered list unchanged
- **Linked Requirements**: REQ-009, AC-3
- **Priority**: CRITICAL
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. A release note exists with known field values.
- **Steps**:
  1. Note the current title of a release card.
  2. Click Edit on that card.
  3. Change the title to a different value in the form.
  4. Click Cancel without clicking Save.
  5. Inspect the rendered release list for the target card.
- **Expected Result**: The release card in the DOM still shows the original title. No changes are visible in the list.

---

#### TS-P-013
- **Category**: Positive
- **Title**: Cancel leaves localStorage unchanged
- **Linked Requirements**: REQ-009, AC-3
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. A release note exists. Record the current `localStorage` value for `releaseNotesDashboard.releases`.
- **Steps**:
  1. Click Edit on a release card.
  2. Change multiple field values.
  3. Click Cancel.
  4. Read `localStorage.getItem('releaseNotesDashboard.releases')`.
- **Expected Result**: The `localStorage` value is byte-for-byte identical to the value recorded before the edit was opened.

---

#### TS-P-014
- **Category**: Positive
- **Title**: All active filters remain applied after Save
- **Linked Requirements**: REQ-010, AC-4
- **Priority**: CRITICAL
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded with at least three release notes across two products. Set product filter to a specific product, set breaking-change filter to "Breaking", and enter a keyword in the search filter. Verify the filtered list is correct.
- **Steps**:
  1. With all three filters active, click Edit on a visible (matching) release card.
  2. Modify the description.
  3. Click Save.
  4. Inspect the values of `#product-filter`, `#breaking-filter`, and `#search-filter` DOM elements.
  5. Inspect the rendered release list.
- **Expected Result**: The filter input values are unchanged. The rendered list still applies all three filters. The updated card is shown only if it still matches the active filters.

---

#### TS-P-015
- **Category**: Positive
- **Title**: All active filters remain applied after Cancel
- **Linked Requirements**: REQ-011, AC-4
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. Set product filter to a specific product and enter a keyword in the search filter.
- **Steps**:
  1. With filters active, click Edit on a visible release card.
  2. Modify a field.
  3. Click Cancel.
  4. Inspect the values of `#product-filter` and `#search-filter`.
  5. Inspect the rendered release list.
- **Expected Result**: Filter input values are unchanged. The rendered list continues to apply the same filter criteria.

---

#### TS-P-016
- **Category**: Positive
- **Title**: Edit operates correctly on the first card in the list
- **Linked Requirements**: REQ-012
- **Priority**: MEDIUM
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. At least three release notes exist. Identify the first rendered card.
- **Steps**:
  1. Click Edit on the first card.
  2. Modify the title.
  3. Click Save.
  4. Verify the first card now shows the new title.
- **Expected Result**: First card is updated correctly. No other cards are affected.

---

#### TS-P-017
- **Category**: Positive
- **Title**: Edit operates correctly on the last card in the list
- **Linked Requirements**: REQ-012
- **Priority**: MEDIUM
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. At least three release notes exist. Identify the last rendered card.
- **Steps**:
  1. Click Edit on the last card.
  2. Modify the title.
  3. Click Save.
  4. Verify the last card now shows the new title.
- **Expected Result**: Last card is updated correctly. No other cards are affected.

---

#### TS-P-018
- **Category**: Positive
- **Title**: Edit operates correctly on a middle card in the list
- **Linked Requirements**: REQ-012
- **Priority**: MEDIUM
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. At least three release notes exist. Identify a card that is neither first nor last.
- **Steps**:
  1. Click Edit on the middle card.
  2. Modify the title.
  3. Click Save.
  4. Verify the middle card now shows the new title.
- **Expected Result**: Middle card is updated correctly. Adjacent cards are unaffected.

---

### Negative Scenarios

---

#### TS-N-001
- **Category**: Negative
- **Title**: Cancel without modifying any field — list and localStorage unchanged
- **Linked Requirements**: REQ-009
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. At least one release note exists. Record current `localStorage` value.
- **Steps**:
  1. Click Edit on a release card.
  2. Do not modify any field.
  3. Click Cancel.
  4. Compare rendered list and `localStorage` against the recorded baseline.
- **Expected Result**: No change to either the rendered list or `localStorage`. The edit form reverts to create mode (button text returns to "Add Release Note"; Cancel button hides).

---

#### TS-N-002
- **Category**: Negative
- **Title**: Save with teamName cleared — validation error, edit state preserved
- **Linked Requirements**: REQ-004, AMB-001
- **Priority**: HIGH
- **Automation Suitability**: BOTH
- **Precondition**: A release note with a non-empty teamName exists. Application is in a state where teamName is a required field.
- **Steps**:
  1. Click Edit on a release card that has a teamName.
  2. Clear the `#team-name-input` field.
  3. Click Save / "Update Release Note".
- **Expected Result**: Save is blocked. A validation error is displayed (consistent with the create flow error messaging). The form remains in edit mode. `localStorage` and the rendered list are unchanged.

---

#### TS-N-003
- **Category**: Negative
- **Title**: Save with title cleared — validation error shown
- **Linked Requirements**: REQ-004
- **Priority**: HIGH
- **Automation Suitability**: BOTH
- **Precondition**: Application is loaded. A release note exists.
- **Steps**:
  1. Click Edit on a release card.
  2. Clear the `#title-input` field.
  3. Click Save.
- **Expected Result**: Save is blocked with a validation error. Form remains in edit mode. List and localStorage unchanged.

---

#### TS-N-004
- **Category**: Negative
- **Title**: Save with product cleared — validation error shown
- **Linked Requirements**: REQ-004
- **Priority**: HIGH
- **Automation Suitability**: BOTH
- **Precondition**: Application is loaded. A release note exists.
- **Steps**:
  1. Click Edit on a release card.
  2. Clear or deselect the `#product-input` field.
  3. Click Save.
- **Expected Result**: Save is blocked with a validation error. Form remains in edit mode. List and localStorage unchanged.

---

#### TS-N-005
- **Category**: Negative
- **Title**: Save with version cleared — validation error shown
- **Linked Requirements**: REQ-004
- **Priority**: HIGH
- **Automation Suitability**: BOTH
- **Precondition**: Application is loaded. A release note exists.
- **Steps**:
  1. Click Edit on a release card.
  2. Clear the `#version-input` field.
  3. Click Save.
- **Expected Result**: Save is blocked with a validation error. Form remains in edit mode. List and localStorage unchanged.

---

#### TS-N-006
- **Category**: Negative
- **Title**: Save with releaseDate cleared — validation error shown
- **Linked Requirements**: REQ-004
- **Priority**: HIGH
- **Automation Suitability**: BOTH
- **Precondition**: Application is loaded. A release note exists.
- **Steps**:
  1. Click Edit on a release card.
  2. Clear the `#release-date-input` field.
  3. Click Save.
- **Expected Result**: Save is blocked with a validation error. Form remains in edit mode. List and localStorage unchanged.

---

#### TS-N-007
- **Category**: Negative
- **Title**: startEdit called with non-existent id — no form pre-fill, no crash
- **Linked Requirements**: REQ-006
- **Priority**: HIGH
- **Automation Suitability**: MANUAL
- **Precondition**: Application is loaded. Developer tools accessible.
- **Steps**:
  1. Open the browser console.
  2. Call `startEdit("non-existent-id-xyz")` directly.
  3. Observe form state and console for errors.
- **Expected Result**: The application does not crash (no uncaught exception). The form is not pre-filled with stale or undefined values. The application remains in a usable state. (Exact error handling — silent no-op vs. console warning — is acceptable either way.)

---

#### TS-N-008
- **Category**: Negative
- **Title**: Clicking Edit on card B while card A is in edit mode — form replaces to card B
- **Linked Requirements**: AMB-003, REQ-002
- **Priority**: MEDIUM
- **Automation Suitability**: BOTH
- **Precondition**: Application is loaded. At least two release notes exist (card A and card B) with distinct field values.
- **Steps**:
  1. Click Edit on card A. Verify form is pre-filled with A's values.
  2. Without saving or cancelling, click Edit on card B.
  3. Inspect the form fields.
- **Expected Result**: Form fields now show card B's values (not a mix of A and B). `editingReleaseId` resolves to B's id. If the user now clicks Save, only card B is updated.

---

#### TS-N-009
- **Category**: Negative
- **Title**: Cancel after a validation failure — edit mode exits cleanly
- **Linked Requirements**: REQ-005, REQ-009
- **Priority**: HIGH
- **Automation Suitability**: BOTH
- **Precondition**: Application is loaded. A release note exists.
- **Steps**:
  1. Click Edit on a release card.
  2. Clear a mandatory field (e.g., title).
  3. Click Save — expect validation error.
  4. Without fixing the validation error, click Cancel.
  5. Inspect the form and rendered list.
- **Expected Result**: Edit mode exits. Form returns to create state ("Add Release Note" button; Cancel button hidden). Rendered list and localStorage are unchanged from before the edit.

---

### Boundary Scenarios

---

#### TS-B-001
- **Category**: Boundary
- **Title**: Edit with all 7 fields modified then Save
- **Linked Requirements**: REQ-002, REQ-006
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. A release note exists with known values for all 7 fields.
- **Steps**:
  1. Click Edit on the release card.
  2. Change product, version, teamName, title, description, releaseDate, and toggle isBreaking.
  3. Click Save.
  4. Inspect the rendered card and localStorage entry by id.
- **Expected Result**: All 7 fields reflect the new values. The id is unchanged. No other entries are affected. Total count unchanged.

---

#### TS-B-002
- **Category**: Boundary
- **Title**: Edit with exactly one field changed then Save
- **Linked Requirements**: REQ-006
- **Priority**: MEDIUM
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. A release note exists.
- **Steps**:
  1. Click Edit on a release card.
  2. Change only the description; leave all other 6 fields as pre-filled.
  3. Click Save.
  4. Inspect the rendered card.
- **Expected Result**: Only the description is updated. All other 6 fields (product, version, teamName, title, releaseDate, isBreaking) remain identical to their original values.

---

#### TS-B-003
- **Category**: Boundary
- **Title**: Edit: set teamName to empty (optional field) and Save
- **Linked Requirements**: REQ-002, REQ-003
- **Priority**: MEDIUM
- **Automation Suitability**: BOTH
- **Precondition**: Application is loaded. A release note exists with a non-empty teamName. [NOTE: outcome depends on whether teamName is truly optional in edit mode; flag for clarification against AMB-001.]
- **Steps**:
  1. Click Edit on a release card that has a teamName value.
  2. Clear `#team-name-input` to empty.
  3. Click Save.
  4. Observe outcome: either validation error OR successful save with empty teamName.
- **Expected Result (assumed per impact analysis mitigation)**: If teamName is required, Save is blocked with a validation error. If teamName is optional, the release is saved with an empty teamName and the card reflects the empty value. — **MISSING CLARIFICATION**: Final behaviour depends on AMB-001 resolution; test should record actual outcome.

---

#### TS-B-004
- **Category**: Boundary
- **Title**: Edit with minimum-length valid values in all mandatory fields
- **Linked Requirements**: REQ-002, REQ-006
- **Priority**: MEDIUM
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. A release note exists.
- **Steps**:
  1. Click Edit on a release card.
  2. Set each mandatory text field to a single character (e.g., product = "A", version = "1", title = "T", description = "D").
  3. Set releaseDate to a valid date (e.g., today's date).
  4. Click Save.
- **Expected Result**: Save succeeds. The release is updated with the single-character values. Rendered card shows the new values. localStorage is updated.

---

#### TS-B-005
- **Category**: Boundary
- **Title**: Edit + Cancel + re-Edit same card — form shows original values
- **Linked Requirements**: REQ-002, REQ-009
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. A release note exists with known field values.
- **Steps**:
  1. Click Edit on a release card. Note the pre-filled title.
  2. Change the title to "TEMP_VALUE".
  3. Click Cancel.
  4. Click Edit on the same release card again.
  5. Inspect `#title-input`.
- **Expected Result**: `#title-input` shows the original title (not "TEMP_VALUE"). The form was fully cleared by Cancel and re-filled from the unchanged data source.

---

#### TS-B-006
- **Category**: Boundary
- **Title**: Edit card A, Cancel, Edit card B — form shows B's values only
- **Linked Requirements**: REQ-002
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. At least two release notes (A and B) exist with distinct field values.
- **Steps**:
  1. Click Edit on card A. Note A's title.
  2. Change the title in the form to "CARD_A_TEMP".
  3. Click Cancel.
  4. Click Edit on card B.
  5. Inspect all 7 form fields.
- **Expected Result**: All 7 form fields show card B's values. No residual values from card A are present.

---

#### TS-B-007
- **Category**: Boundary
- **Title**: Edit title/description with maximum-length text
- **Linked Requirements**: REQ-003
- **Priority**: LOW
- **Automation Suitability**: MANUAL
- **Precondition**: Application is loaded. A release note exists. [NOTE: Maximum accepted length is not specified in requirements; flag as MISSING TEST DATA.]
- **Steps**:
  1. Click Edit on a release card.
  2. Paste a very long string (e.g., 500 characters) into `#title-input` and `#description-input`.
  3. Click Save.
- **Expected Result**: Application does not crash or truncate silently. Either the text is saved as-is or a visible truncation/validation message is shown. localStorage entry reflects the saved value. — **MISSING REQUIREMENT**: No max-length constraint defined; document actual behaviour.

---

#### TS-B-008
- **Category**: Boundary
- **Title**: Edit text fields with special characters
- **Linked Requirements**: REQ-003
- **Priority**: LOW
- **Automation Suitability**: MANUAL
- **Precondition**: Application is loaded. A release note exists.
- **Steps**:
  1. Click Edit on a release card.
  2. Enter special characters in title: `<script>alert(1)</script>`, `"quotes"`, `&amp;`, emoji.
  3. Click Save.
  4. Inspect the rendered card and `localStorage`.
- **Expected Result**: Special characters are stored and rendered as literal text (no XSS execution, no JSON parse failure). The rendered card displays the characters visually (HTML-escaped or safely handled).

---

#### TS-B-009
- **Category**: Boundary
- **Title**: Toggle isBreaking from true to false during edit and Save
- **Linked Requirements**: REQ-002, REQ-006
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: A release note with `isBreaking = true` exists.
- **Steps**:
  1. Click Edit on the breaking release card.
  2. Verify `#is-breaking-input` is checked.
  3. Uncheck `#is-breaking-input`.
  4. Click Save.
  5. Inspect the rendered card and `localStorage`.
- **Expected Result**: The release now has `isBreaking = false` in both the rendered list and `localStorage`. Any breaking-change filter that was active may exclude this card after re-render.

---

#### TS-B-010
- **Category**: Boundary
- **Title**: Toggle isBreaking from false to true during edit and Save
- **Linked Requirements**: REQ-002, REQ-006
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: A release note with `isBreaking = false` exists.
- **Steps**:
  1. Click Edit on the non-breaking release card.
  2. Verify `#is-breaking-input` is unchecked.
  3. Check `#is-breaking-input`.
  4. Click Save.
  5. Inspect the rendered card and `localStorage`.
- **Expected Result**: The release now has `isBreaking = true` in both the rendered list and `localStorage`. If a breaking-change filter is active, the card now satisfies that filter.

---

#### TS-B-011
- **Category**: Boundary
- **Title**: Edit when list contains exactly one entry
- **Linked Requirements**: REQ-012
- **Priority**: MEDIUM
- **Automation Suitability**: AUTO
- **Precondition**: localStorage is set so that exactly one release note exists in the list.
- **Steps**:
  1. Verify only one card is rendered.
  2. Click Edit on that card.
  3. Modify the title.
  4. Click Save.
  5. Inspect rendered list and localStorage.
- **Expected Result**: The single card is updated. The list still contains exactly one entry. localStorage is updated. No errors or empty-list rendering bugs.

---

#### TS-B-012
- **Category**: Boundary
- **Title**: Edit with no filters active (baseline state)
- **Linked Requirements**: REQ-010
- **Priority**: MEDIUM
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded with all filters cleared (product filter = "All", breaking filter = "All", search = empty). All releases are visible.
- **Steps**:
  1. Click Edit on any release card.
  2. Modify a field.
  3. Click Save.
  4. Inspect the rendered list and filter control values.
- **Expected Result**: All filter controls remain cleared ("All" / empty). All releases are still rendered (no filter applied). The edited card shows its updated values.

---

### Regression Scenarios

---

#### TS-R-001
- **Category**: Regression
- **Title**: Create new release still works after Edit + Save
- **Linked Requirements**: REQ-006
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded with at least one existing release note. Note total count N.
- **Steps**:
  1. Click Edit on an existing release, modify a field, click Save.
  2. Verify edit flow completed.
  3. Fill in the create form with all required fields for a new release.
  4. Click "Add Release Note".
  5. Inspect the rendered list and `localStorage`.
- **Expected Result**: A new release entry is added (total count = N + 1). The new entry appears in the list and in `localStorage`. The previously edited entry retains its updated values. No duplication or data corruption.

---

#### TS-R-002
- **Category**: Regression
- **Title**: Create new release still works after Edit + Cancel
- **Linked Requirements**: REQ-009
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. At least one existing release note. Note total count N.
- **Steps**:
  1. Click Edit on a release card, modify a field, click Cancel.
  2. Fill in the create form with new release data.
  3. Click "Add Release Note".
  4. Inspect the rendered list and count.
- **Expected Result**: New release is created (count = N + 1). Form is in create mode (editingReleaseId = null). Previously edited card is unchanged.

---

#### TS-R-003
- **Category**: Regression
- **Title**: Delete a different release still works after Edit + Save
- **Linked Requirements**: REQ-006
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. At least three release notes (A, B, C) exist.
- **Steps**:
  1. Click Edit on release A, modify a field, click Save.
  2. Click Delete on release B.
  3. Inspect the rendered list and `localStorage`.
- **Expected Result**: Release B is deleted. Total count decreases by one. Release A shows its updated values. Release C is unaffected.

---

#### TS-R-004
- **Category**: Regression
- **Title**: Deleting the release currently in edit mode resets edit state
- **Linked Requirements**: REQ-009
- **Priority**: HIGH
- **Automation Suitability**: BOTH
- **Precondition**: Application is loaded. At least two release notes exist.
- **Steps**:
  1. Click Edit on release A — form is pre-filled.
  2. Without saving, trigger deletion of release A (via Delete button on the card or programmatically).
  3. Inspect the form and rendered list.
- **Expected Result**: Release A is removed from the list. The form returns to create mode (`editingReleaseId` is cleared; "Add Release Note" button; Cancel button hidden). No orphaned edit state. Attempting to add a new release works correctly.

---

#### TS-R-005
- **Category**: Regression
- **Title**: Product filter still applies correctly after Edit + Save
- **Linked Requirements**: REQ-010
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. Multiple releases across at least two products. Product filter is set to a specific product.
- **Steps**:
  1. With product filter active, click Edit on a visible card, modify description, click Save.
  2. Change the product filter to a different product.
  3. Change it back.
- **Expected Result**: Product filter functions correctly before and after the edit. The edit did not corrupt the product filter logic or the product values in localStorage.

---

#### TS-R-006
- **Category**: Regression
- **Title**: Breaking-change filter still applies correctly after Edit + Save
- **Linked Requirements**: REQ-010
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. At least one breaking and one non-breaking release exist.
- **Steps**:
  1. Set breaking-change filter to "Breaking".
  2. Edit a visible breaking release (modify description), click Save.
  3. Toggle breaking-change filter to "Non-Breaking" then back to "Breaking".
- **Expected Result**: Filter toggles correctly. The breaking/non-breaking classification of each release is correct in the rendered list. The edited release's isBreaking value was not unintentionally changed.

---

#### TS-R-007
- **Category**: Regression
- **Title**: Keyword search filter still applies correctly after Edit + Save
- **Linked Requirements**: REQ-010
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. At least two releases, one containing keyword "alpha" and one not.
- **Steps**:
  1. Enter "alpha" in `#search-filter`.
  2. Edit a visible matching release (change description, not title), click Save.
  3. Clear and re-enter "alpha" in the search.
- **Expected Result**: Search still filters correctly. Only releases containing "alpha" are shown. The edit did not break the search function.

---

#### TS-R-008
- **Category**: Regression
- **Title**: Multi-filter combination persists after Edit + Save
- **Linked Requirements**: REQ-010
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded with multiple releases of varying products and breaking flags. Set all three filters simultaneously: product = "ProductA", breaking = "Breaking", search = "v2".
- **Steps**:
  1. With all three filters active, edit a visible (matching) release's description.
  2. Click Save.
  3. Inspect filter control values and rendered list.
- **Expected Result**: All three filter control values are unchanged. The rendered list applies all three filters correctly (AND logic). The edited card still appears only if it matches all three criteria.

---

#### TS-R-009
- **Category**: Regression
- **Title**: Edited values persist across page reload (localStorage)
- **Linked Requirements**: REQ-007
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded. A release note exists.
- **Steps**:
  1. Click Edit on a release, change the title to a unique string, click Save.
  2. Reload the page (F5 / hard reload).
  3. Inspect the rendered release list for the edited card.
- **Expected Result**: After reload, the edited card shows the updated title. The change survived the page reload via localStorage persistence.

---

#### TS-R-010
- **Category**: Regression
- **Title**: Export CSV still works after Edit + Save
- **Linked Requirements**: REQ-007
- **Priority**: MEDIUM
- **Automation Suitability**: MANUAL
- **Precondition**: Application is loaded. At least two releases exist. Export functionality is available.
- **Steps**:
  1. Edit a release (modify title), click Save.
  2. Click the Export CSV button.
  3. Open/inspect the downloaded CSV file.
- **Expected Result**: CSV is generated successfully. The exported CSV includes the updated field values for the edited release. No other releases are missing or corrupted.

---

#### TS-R-011
- **Category**: Regression
- **Title**: Import JSON while in edit mode resets edit state
- **Linked Requirements**: REQ-009
- **Priority**: MEDIUM
- **Automation Suitability**: MANUAL
- **Precondition**: Application is loaded. Import JSON functionality is available. A valid JSON file with release data is available for import.
- **Steps**:
  1. Click Edit on a release card — form enters edit mode.
  2. Without saving, trigger Import JSON and confirm the import action.
  3. Inspect the form state and rendered list.
- **Expected Result**: Import replaces the releases list. The form returns to create mode (editingReleaseId is cleared). No orphaned edit state. The imported data is rendered correctly.

---

#### TS-R-012
- **Category**: Regression
- **Title**: Form in create mode still creates a new entry (editingReleaseId = null)
- **Linked Requirements**: REQ-006
- **Priority**: HIGH
- **Automation Suitability**: AUTO
- **Precondition**: Application is loaded in a fresh state (no edit mode active, editingReleaseId = null). Note current release count N.
- **Steps**:
  1. Verify the form submit button reads "Add Release Note".
  2. Fill in all required fields for a new release.
  3. Click "Add Release Note".
  4. Inspect the rendered list and `localStorage`.
- **Expected Result**: A new release entry is created (count = N + 1) with a newly generated id. No existing entry is modified. This confirms the create-vs-update branch logic is correct.

---

## Coverage Matrix

### Acceptance Criteria to Test Scenario Mapping

| AC | Description | Test Scenarios |
|---|---|---|
| AC-1 | Edit opens release pre-filled for editing | TS-P-002, TS-P-003, TS-P-004, TS-B-005, TS-B-006 |
| AC-2 | Save updates specific release by id in list and localStorage | TS-P-007, TS-P-008, TS-P-009, TS-P-010, TS-P-011, TS-B-001, TS-B-002 |
| AC-3 | Cancel saves no changes; release list remains unchanged | TS-P-012, TS-P-013, TS-N-001, TS-N-009, TS-B-005 |
| AC-4 | Filters remain applied after Save or Cancel | TS-P-014, TS-P-015, TS-B-012, TS-R-005, TS-R-006, TS-R-007, TS-R-008 |

### Requirements to Test Scenario Mapping

| REQ | Test Scenarios |
|---|---|
| REQ-001 | TS-P-001 |
| REQ-002 | TS-P-002, TS-P-003, TS-P-004, TS-B-001, TS-B-005, TS-B-006, TS-B-009, TS-B-010 |
| REQ-003 | TS-P-002, TS-B-003, TS-B-007, TS-B-008 |
| REQ-004 | TS-P-005, TS-N-002, TS-N-003, TS-N-004, TS-N-005, TS-N-006 |
| REQ-005 | TS-P-006, TS-N-009 |
| REQ-006 | TS-P-007, TS-P-008, TS-P-009, TS-N-007, TS-B-001, TS-B-002, TS-B-009, TS-B-010, TS-R-001, TS-R-003, TS-R-012 |
| REQ-007 | TS-P-010, TS-P-013, TS-R-009, TS-R-010 |
| REQ-008 | TS-P-011 |
| REQ-009 | TS-P-012, TS-P-013, TS-N-001, TS-N-009, TS-B-005, TS-R-002, TS-R-004, TS-R-011 |
| REQ-010 | TS-P-014, TS-B-012, TS-R-005, TS-R-006, TS-R-007, TS-R-008 |
| REQ-011 | TS-P-015 |
| REQ-012 | TS-P-016, TS-P-017, TS-P-018, TS-B-011 |

---

## Test Data Requirements

| Data Item | Description | Status |
|---|---|---|
| Release set — multi-product | At least 3 releases spanning 2+ products for filter tests | REQUIRED — to be created during test setup |
| Release — breaking = true | At least 1 release with `isBreaking = true` | REQUIRED |
| Release — breaking = false | At least 1 release with `isBreaking = false` | REQUIRED |
| Release — non-empty teamName | At least 1 release with a non-empty teamName | REQUIRED |
| Release — keyword-searchable | At least 1 release whose title/description contains a known keyword (e.g., "alpha") | REQUIRED |
| Release — single-entry list | localStorage state with exactly 1 release, for TS-B-011 | REQUIRED |
| JSON import file | Valid JSON array of releases for TS-R-011 | REQUIRED — file must be prepared |
| Long-text value (500+ chars) | For TS-B-007; max-length constraint is UNKNOWN — see MISSING below | FLAGGED MISSING |
| Maximum-length constraint | Required field maximum length not documented in requirements | MISSING — must be specified before TS-B-007 can pass/fail definitively |
| Validation rules per field | Exact validation rules for each mandatory field on update (AMB-001) | MISSING — must clarify before TS-N-002, TS-B-003 are unambiguous |

---

## Environment Requirements

| Requirement | Detail | Status |
|---|---|---|
| Browser | Modern Chromium-based browser (Chrome 120+ or Edge 120+) or Firefox 121+ | REQUIRED |
| JavaScript enabled | Vanilla JS application; JS must be enabled | REQUIRED |
| localStorage accessible | Browser must allow localStorage writes (not in private/incognito mode that blocks it) | REQUIRED |
| Application served | `product_release_dashboard/index.html` served via local file (`file://`) or local HTTP server | REQUIRED |
| Browser DevTools | Required for TS-N-007 (console call), TS-P-013 (localStorage inspection) | REQUIRED for specific scenarios |
| File system access | For TS-R-010 (CSV download inspection) and TS-R-011 (JSON file import) | REQUIRED |
| Test framework | No test framework exists yet (per impact analysis); first test run is manual or requires framework setup | FLAG — framework selection pending |

---

## Dependencies

| Dependency | Type | Impact if Unavailable |
|---|---|---|
| `startEdit(id)` implementation | Code | Blocks TS-P-002 through TS-P-018 and all boundary/regression scenarios |
| Update branch in form submit handler | Code | Blocks TS-P-007, TS-P-008, TS-P-009, TS-P-010, TS-P-011 |
| `resetEditMode()` clearing all 7 fields | Code | Blocks TS-B-005, TS-B-006, TS-N-009 |
| AMB-001 resolved (validation on update) | Requirement | TS-N-002 and TS-B-003 cannot have definitive pass/fail criteria |
| AMB-003 resolved (concurrent edit state) | Requirement | TS-N-008 expected result may be incorrect |
| JSON import file prepared | Test data | Blocks TS-R-011 |
| Max-length specification | Requirement | TS-B-007 result is undefinable without this |

---

## Risks and Mitigations

| Risk ID | Risk | Probability | Impact | Mitigation |
|---|---|---|---|---|
| RISK-001 | In-place update uses array index instead of id lookup — off-by-one errors when list is filtered or sorted | MEDIUM | HIGH | Review `startEdit()` and submit handler to confirm `array.find(r => r.id === id)` is used, not index |
| RISK-002 | `resetEditMode()` does not clear all 7 form fields — stale values appear in next edit | MEDIUM | HIGH | Verify each field is explicitly reset: `.value = ""` and checkbox `.checked = false` |
| RISK-003 | Filter inputs accidentally reset during edit/save — filters appear to disappear after Save | LOW | HIGH | Do not modify `#product-filter`, `#breaking-filter`, or `#search-filter` DOM values during edit flow |
| RISK-004 | Validation not applied on update path (AMB-001) — invalid data can be saved | MEDIUM | MEDIUM | Confirm validation code path is shared between create and update; add TS-N-002 through TS-N-006 as blockers |
| RISK-005 | `editingReleaseId` not cleared on Cancel — orphaned state causes next create to trigger an update | LOW | HIGH | Verify `resetEditMode()` sets `editingReleaseId = null` |
| RISK-006 | No existing test suite — regressions are not caught automatically | HIGH | MEDIUM | Execute TS-R-001 through TS-R-012 manually before merge; plan automation sprint |
| RISK-007 | localStorage quota exceeded on very long field values | LOW | LOW | Note in TS-B-007; handle gracefully (not a blocking risk for story acceptance) |

---

## Assumptions

1. The edit workflow uses the existing inline form `#release-form` in `index.html` (not a modal or separate page).
2. The `id` field is immutable: editing a release does not and cannot change its `id`.
3. "Filters remain applied" means the DOM values of `#product-filter`, `#breaking-filter`, and `#search-filter` are not modified by the edit/save/cancel flow.
4. Validation rules for mandatory fields are the same in edit mode as in create mode (per AMB-001 resolution adopted in impact analysis).
5. `teamName` is treated as a required field for test scenarios TS-N-002; if AMB-001 is resolved differently, TS-N-002 and TS-B-003 must be updated.
6. The Cancel action discards changes without a confirmation dialog (per `resetEditMode()` existing behaviour).
7. Clicking Edit while another card is in edit mode replaces the edit state with the newly clicked card (per AMB-003 mitigation).
8. The application is delivered as a static file; no build step is required before testing.
9. Scroll-into-view behaviour on Edit trigger (AMB-004) is not tested as a pass/fail criterion.

---

## Exit Criteria

### Entry Criteria (before test execution begins)
- Implementation of `startEdit(id)` pre-fill and update branch in form submit handler is code-complete.
- AMB-001 (validation on update) is resolved and communicated to the testing team.
- Test data set (multi-product, breaking/non-breaking releases) is prepared in `localStorage` or via application create flow.
- JSON import file for TS-R-011 is available.

### Exit Criteria (test execution complete when all of the following are satisfied)
- All CRITICAL priority scenarios (TS-P-002, TS-P-007, TS-P-008, TS-P-010, TS-P-012, TS-P-014) pass.
- All HIGH priority scenarios pass or have documented, accepted exceptions.
- Zero CRITICAL or HIGH defects remain open.
- All 12 requirements (REQ-001 through REQ-012) have at least one passing test scenario.
- All 4 acceptance criteria (AC-1 through AC-4) are verified by at least one passing test scenario.
- Regression scenarios TS-R-001, TS-R-003, TS-R-005 through TS-R-009, TS-R-012 all pass.
- MEDIUM and LOW defects are logged with agreed remediation timelines but do not block release.
- Test execution results are recorded against each TS-ID for traceability.

---

## Artifact Metadata

- **Test Plan ID**: TP-001
- **Story**: COD-7 — Edit Existing Release Note
- **Total Scenarios**: 48 (TS-P-001 to TS-P-018: 18; TS-N-001 to TS-N-009: 9; TS-B-001 to TS-B-012: 12; TS-R-001 to TS-R-012: 12; sub-totals exclude TS-B-003 ambiguity note counting)
- **Critical Scenarios**: 6
- **Missing Clarifications**: AMB-001 (validation on update), max-length constraints (TS-B-007)
- **Plan Created**: 2026-10-30
