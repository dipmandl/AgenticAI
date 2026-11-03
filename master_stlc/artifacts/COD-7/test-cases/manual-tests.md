# Manual Test Cases

## Metadata

| Field | Value |
|---|---|
| Story ID | COD-7 |
| Story Title | Edit an existing release note |
| Test Plan Reference | artifacts/COD-7/test-plans/test-plan.md |
| Total Test Cases | 42 |
| Generated | 2026-11-03 |
| Artifact | artifacts/COD-7/test-cases/manual-tests.md |

---

## Application Context

- **SPA location**: `product_release_dashboard/` (`index.html`, `script.js`, `styles.css`)
- **Edit mechanism**: Reuses the top-of-page `#release-form`; `startEdit(id)` pre-fills all 7 fields and changes submit button text to "Update Release Note"; shows "Cancel Edit" button
- **Required fields**: `product`, `version`, `title`, `description`, `releaseDate` (HTML `required` attribute) + `teamName` (custom JS validation: `if (!payload.teamName)` → inline error + focus)
- **Breaking flag**: `<input type="checkbox">` — boolean; unchecked = `false`
- **Cancel**: Calls `releaseForm.reset()` immediately — no confirmation dialog
- **Delete**: `window.confirm("Delete this release note?")` required before removal
- **Filters**: AND-combined; read from DOM values; persist naturally across re-renders
- **After Save**: `renderReleaseList()` re-applies active filters; edited entry disappears from view if it no longer matches filters (B-003 — expected behavior)
- **localStorage key**: `"releaseNotesDashboard.releases"` (JSON array)
- **ID generation**: `crypto.randomUUID()` (UUID v4)
- **Silent failure**: `saveReleases()` calls `localStorage.setItem()` with no `try/catch` — quota exceeded causes silent failure with no user feedback

---

## Test Data Seeds Reference

| Seed ID | Description |
|---|---|
| SD-001 | Standard 5-entry dataset: 2 × ProductA, 2 × ProductB, 1 × ProductC; mixed `isBreaking` flags; all have `teamName` |
| SD-002 | Single-entry dataset: 1 entry with all fields populated; `isBreaking = false` |
| SD-003 | Entry with `isBreaking = true`; all required fields populated |
| SD-004 | Entry with `releaseDate = "1970-01-01"`; all other fields populated |
| SD-005 | Entry with `releaseDate = <today's date in YYYY-MM-DD>`; all other fields populated |
| SD-006 | Entry without `teamName` (field absent or undefined); all other fields populated |
| SD-007 | Large dataset: 100 entries with randomized values; all have `teamName` |
| SD-008 | Two-product dataset: exactly 1 entry with `product = "ProductA"`, 1 entry with `product = "ProductB"` |
| SD-009 | Default app seed: clear localStorage; reload page triggers auto-seed of 2 records |

---

## Group 1 — Positive Scenarios (TC-001 to TC-014)

---

### TC-001

| Field | Value |
|---|---|
| ID | TC-001 |
| Scenario ID | TS-P-001 |
| Title | Edit button present and triggers form pre-fill |
| Linked Requirements | REQ-001, REQ-002, REQ-003, REQ-004, AC-1 |
| Priority | P1 — Critical |
| Type | Positive |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: localStorage key `"releaseNotesDashboard.releases"` is seeded with SD-001. Application is loaded and the release list is rendered.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001 (5 entries)
And the application is open and the release list displays all 5 entries
When the user clicks the "Edit" button on any release entry in the list
Then the page scrolls to the top-of-page "#release-form"
And the "product" input is pre-filled with the exact stored product value of that entry
And the "version" input is pre-filled with the exact stored version value of that entry
And the "title" input is pre-filled with the exact stored title value of that entry
And the "description" textarea is pre-filled with the exact stored description value of that entry
And the "releaseDate" date input is pre-filled with the exact stored releaseDate value of that entry
And the "teamName" input is pre-filled with the exact stored teamName value of that entry
And the "breaking" checkbox reflects the exact stored isBreaking boolean value of that entry
And the submit button text reads "Update Release Note"
And the "Cancel Edit" button is visible on the form
```

**Expected Result**: All 7 fields (product, version, title, description, releaseDate, teamName, breaking checkbox) are pre-filled with the exact values of the selected entry. Submit button reads "Update Release Note". "Cancel Edit" button is visible. Form has scrolled into view.

---

### TC-002

| Field | Value |
|---|---|
| ID | TC-002 |
| Scenario ID | TS-P-002 |
| Title | Save after modifying product field updates localStorage |
| Linked Requirements | REQ-005, REQ-006, REQ-007, AC-2 |
| Priority | P1 — Critical |
| Type | Positive |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: Entry with `product = "ProductA"` exists in localStorage (SD-001). Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on the entry with product "ProductA"
And the user clears the "product" field and types "ProductX"
And the user clicks the "Update Release Note" submit button
Then the form is submitted successfully with no validation error
And the entry matching the original "id" in localStorage now has product equal to "ProductX"
And the release list re-renders and displays the entry with product "ProductX"
And all other fields of that entry remain unchanged in localStorage
```

**Expected Result**: localStorage entry identified by the original `id` has `product = "ProductX"`. The rendered list reflects the new value. No duplicate entries are created.

---

### TC-003

| Field | Value |
|---|---|
| ID | TC-003 |
| Scenario ID | TS-P-003 |
| Title | Save after modifying version field updates localStorage |
| Linked Requirements | REQ-005, REQ-006, REQ-007, AC-2 |
| Priority | P2 — High |
| Type | Positive |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: An entry with an existing version exists in SD-001. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on any release entry
And the user clears the "version" field and types "9.9.9"
And the user clicks the "Update Release Note" submit button
Then the form is submitted successfully with no validation error
And the entry matching the original "id" in localStorage now has version equal to "9.9.9"
And the release list re-renders and displays the entry with version "9.9.9"
```

**Expected Result**: Stored entry has `version = "9.9.9"`. UI reflects the change. No other entries are affected.

---

### TC-004

| Field | Value |
|---|---|
| ID | TC-004 |
| Scenario ID | TS-P-004 |
| Title | Save after modifying title and description updates both fields |
| Linked Requirements | REQ-003, REQ-005, REQ-006, AC-2 |
| Priority | P2 — High |
| Type | Positive |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: An entry with existing title and description exists in SD-001. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on any release entry
And the user clears the "title" field and types "Updated Title Text"
And the user clears the "description" field and types "Updated description content."
And the user clicks the "Update Release Note" submit button
Then the form is submitted successfully with no validation error
And the entry matching the original "id" in localStorage has title equal to "Updated Title Text"
And the entry matching the original "id" in localStorage has description equal to "Updated description content."
And all other fields (product, version, releaseDate, teamName, isBreaking) remain unchanged in localStorage
```

**Expected Result**: Stored entry has the new title and new description. All other fields of that entry are unchanged.

---

### TC-005

| Field | Value |
|---|---|
| ID | TC-005 |
| Scenario ID | TS-P-005 |
| Title | Save after modifying releaseDate updates date in localStorage |
| Linked Requirements | REQ-003, REQ-005, REQ-006, AC-2 |
| Priority | P2 — High |
| Type | Positive |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: An entry with an existing releaseDate exists in SD-001. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on any release entry
And the user sets the "releaseDate" date input to "2024-06-15"
And the user clicks the "Update Release Note" submit button
Then the form is submitted successfully with no validation error
And the entry matching the original "id" in localStorage has releaseDate equal to "2024-06-15"
And the release list re-renders and displays the updated date correctly
```

**Expected Result**: Stored entry has `releaseDate = "2024-06-15"`. The date renders correctly in the UI list.

---

### TC-006

| Field | Value |
|---|---|
| ID | TC-006 |
| Scenario ID | TS-P-006 |
| Title | Save after modifying teamName updates teamName in localStorage |
| Linked Requirements | REQ-003, REQ-005, REQ-006, AC-2 |
| Priority | P3 — Medium |
| Type | Positive |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: An entry with an existing teamName exists in SD-001. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on an entry that has a teamName value
And the user clears the "teamName" field and types "AlphaTeam"
And the user clicks the "Update Release Note" submit button
Then the form is submitted successfully with no validation error
And the entry matching the original "id" in localStorage has teamName equal to "AlphaTeam"
```

**Expected Result**: Stored entry has `teamName = "AlphaTeam"`. All other fields remain unchanged.

---

### TC-007

| Field | Value |
|---|---|
| ID | TC-007 |
| Scenario ID | TS-P-007 |
| Title | Save with breaking flag toggled from false to true |
| Linked Requirements | REQ-003, REQ-005, REQ-006, AC-2 |
| Priority | P2 — High |
| Type | Positive |
| Automation | AUTO |
| Test Data | SD-001 (entry with `isBreaking = false`) |

**Preconditions**: An entry with `isBreaking = false` exists in SD-001. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on an entry with isBreaking equal to false
And the "breaking" checkbox on the form is in an unchecked state
And the user checks the "breaking" checkbox
And the user clicks the "Update Release Note" submit button
Then the form is submitted successfully with no validation error
And the entry matching the original "id" in localStorage has isBreaking equal to true
```

**Expected Result**: Stored entry has `isBreaking = true`. All other fields remain unchanged.

---

### TC-008

| Field | Value |
|---|---|
| ID | TC-008 |
| Scenario ID | TS-P-008 |
| Title | Save with breaking flag toggled from true to false |
| Linked Requirements | REQ-003, REQ-005, REQ-006, AC-2 |
| Priority | P2 — High |
| Type | Positive |
| Automation | AUTO |
| Test Data | SD-003 (entry with `isBreaking = true`) |

**Preconditions**: An entry with `isBreaking = true` exists (SD-003). Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-003
And the application is open and the release list is rendered
When the user clicks the "Edit" button on the entry with isBreaking equal to true
And the "breaking" checkbox on the form is in a checked state
And the user unchecks the "breaking" checkbox
And the user clicks the "Update Release Note" submit button
Then the form is submitted successfully with no validation error
And the entry matching the original "id" in localStorage has isBreaking equal to false
```

**Expected Result**: Stored entry has `isBreaking = false`. All other fields remain unchanged.

---

### TC-009

| Field | Value |
|---|---|
| ID | TC-009 |
| Scenario ID | TS-P-009 |
| Title | Save after modifying all editable fields; id remains unchanged |
| Linked Requirements | REQ-003, REQ-005, REQ-006, REQ-007, AC-2 |
| Priority | P1 — Critical |
| Type | Positive |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: An entry with a known stable `id` (e.g., "test-id-001") exists in SD-001. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And one entry has id "test-id-001"
And the application is open and the release list is rendered
When the user clicks the "Edit" button on the entry with id "test-id-001"
And the user updates the "product" field to "NewProduct"
And the user updates the "version" field to "8.8.8"
And the user updates the "title" field to "New Title"
And the user updates the "description" field to "New description."
And the user sets the "releaseDate" to "2025-12-31"
And the user updates the "teamName" field to "NewTeam"
And the user checks the "breaking" checkbox
And the user clicks the "Update Release Note" submit button
Then the form is submitted successfully with no validation error
And the entry with id "test-id-001" exists exactly once in localStorage
And that entry has product equal to "NewProduct"
And that entry has version equal to "8.8.8"
And that entry has title equal to "New Title"
And that entry has description equal to "New description."
And that entry has releaseDate equal to "2025-12-31"
And that entry has teamName equal to "NewTeam"
And that entry has isBreaking equal to true
And the total number of entries in localStorage is the same as before editing
```

**Expected Result**: All 7 editable fields are updated. The original `id = "test-id-001"` is preserved identically. No duplicate entries are created. Total entry count is unchanged.

---

### TC-010

| Field | Value |
|---|---|
| ID | TC-010 |
| Scenario ID | TS-P-010 |
| Title | Cancel after modifying fields discards all changes |
| Linked Requirements | REQ-008, AC-3 |
| Priority | P1 — Critical |
| Type | Positive |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded. Application is loaded. Entry values are recorded before the test.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
And the original values of all entries in localStorage are noted
When the user clicks the "Edit" button on any release entry
And the user changes the "product" field to "DiscardedProduct"
And the user changes the "title" field to "Discarded Title"
And the user changes the "description" field to "Discarded description."
And the user clicks the "Cancel Edit" button
Then no confirmation dialog appears
And the form is immediately reset to empty/default state
And localStorage still contains the original values for all entries (no changes persisted)
And the release list displays the original values of the edited entry
And the form returns to create mode (submit button reads "Add Release", "Cancel Edit" button is hidden)
```

**Expected Result**: localStorage is unchanged. The UI shows original values. The form is cleared and back in create mode. No confirmation dialog appeared.

---

### TC-011

| Field | Value |
|---|---|
| ID | TC-011 |
| Scenario ID | TS-P-011 |
| Title | Form returns to create mode after Save |
| Linked Requirements | REQ-004 |
| Priority | P2 — High |
| Type | Positive |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on any release entry
And the form is in edit mode (submit button reads "Update Release Note", "Cancel Edit" is visible)
And the user makes no changes to any field
And the user clicks the "Update Release Note" submit button
Then the form is submitted successfully
And the submit button text reads "Add Release"
And the "Cancel Edit" button is no longer visible (hidden)
And all form fields are cleared (empty or default values)
```

**Expected Result**: After a successful Save, the form reverts to create mode. Submit button reads "Add Release". "Cancel Edit" button is hidden. All form fields are empty.

---

### TC-012

| Field | Value |
|---|---|
| ID | TC-012 |
| Scenario ID | TS-P-012 |
| Title | Form returns to create mode after Cancel |
| Linked Requirements | REQ-004 |
| Priority | P2 — High |
| Type | Positive |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on any release entry
And the form is in edit mode (submit button reads "Update Release Note", "Cancel Edit" is visible)
And the user clicks the "Cancel Edit" button
Then no confirmation dialog appears
And the submit button text reads "Add Release"
And the "Cancel Edit" button is no longer visible (hidden)
And all form fields are cleared (empty or default values)
```

**Expected Result**: After Cancel, the form reverts to create mode. Submit button reads "Add Release". "Cancel Edit" button is hidden. All form fields are empty.

---

### TC-013

| Field | Value |
|---|---|
| ID | TC-013 |
| Scenario ID | TS-P-013 |
| Title | Active product filter persists after Save |
| Linked Requirements | REQ-009, AC-4, NFR-004 |
| Priority | P1 — Critical |
| Type | Positive |
| Automation | AUTO |
| Test Data | SD-001, Filter Setup FS-001 |

**Preconditions**: SD-001 is seeded. Application is loaded. Product filter is set to "ProductA".

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
And the user sets the product filter input to "ProductA"
And the release list is filtered showing only "ProductA" entries
When the user clicks the "Edit" button on a visible "ProductA" entry
And the user changes the "title" field to "Filter Persistence Test Title"
And the user clicks the "Update Release Note" submit button
Then the form is submitted successfully
And the product filter input still displays "ProductA"
And the rendered release list still shows only entries matching product "ProductA"
And the edited entry appears in the list with the updated title "Filter Persistence Test Title"
```

**Expected Result**: Product filter input retains "ProductA". The list remains filtered by "ProductA". The edit is visible within the filtered view.

---

### TC-014

| Field | Value |
|---|---|
| ID | TC-014 |
| Scenario ID | TS-P-014 |
| Title | Active search filter persists after Cancel |
| Linked Requirements | REQ-009, AC-4, NFR-004 |
| Priority | P2 — High |
| Type | Positive |
| Automation | AUTO |
| Test Data | SD-001, Filter Setup FS-002 |

**Preconditions**: SD-001 is seeded. Application is loaded. Search filter is set to "keywordX" (a term that matches at least one entry in SD-001).

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
And the user sets the search filter input to "keywordX"
And the release list is filtered showing only entries matching "keywordX"
When the user clicks the "Edit" button on any visible entry
And the user modifies the "description" field
And the user clicks the "Cancel Edit" button
Then no changes are saved to localStorage
And the search filter input still contains "keywordX"
And the rendered release list still shows only entries matching "keywordX"
```

**Expected Result**: Search filter input retains "keywordX". The list remains filtered by "keywordX" after Cancel. No changes were saved.

---

## Group 2 — Negative Scenarios (TC-015 to TC-022)

---

### TC-015

| Field | Value |
|---|---|
| ID | TC-015 |
| Scenario ID | TS-N-001 |
| Title | Save blocked when required field `product` is cleared |
| Linked Requirements | N-001, REQ-003 |
| Priority | P1 — Critical |
| Type | Negative |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
And the original localStorage values are noted
When the user clicks the "Edit" button on any release entry
And the user clears the "product" field completely (leaving it empty)
And the user clicks the "Update Release Note" submit button
Then the browser HTML5 required field validation fires on the "product" field
And the form is NOT submitted
And localStorage remains unchanged (no update persisted)
```

**Expected Result**: Browser native validation prevents form submission. The "product" field shows a required-field validation message. localStorage is unchanged.

---

### TC-016

| Field | Value |
|---|---|
| ID | TC-016 |
| Scenario ID | TS-N-002 |
| Title | Save blocked when required field `version` is cleared |
| Linked Requirements | N-001, REQ-003 |
| Priority | P2 — High |
| Type | Negative |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on any release entry
And the user clears the "version" field completely (leaving it empty)
And the user clicks the "Update Release Note" submit button
Then the browser HTML5 required field validation fires on the "version" field
And the form is NOT submitted
And localStorage remains unchanged (no update persisted)
```

**Expected Result**: Browser native validation prevents form submission. The "version" field shows a required-field validation message. localStorage is unchanged.

---

### TC-017

| Field | Value |
|---|---|
| ID | TC-017 |
| Scenario ID | TS-N-003 |
| Title | Save blocked when required field `title` is cleared |
| Linked Requirements | N-001, REQ-003 |
| Priority | P2 — High |
| Type | Negative |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on any release entry
And the user clears the "title" field completely (leaving it empty)
And the user clicks the "Update Release Note" submit button
Then the browser HTML5 required field validation fires on the "title" field
And the form is NOT submitted
And localStorage remains unchanged (no update persisted)
```

**Expected Result**: Browser native validation prevents form submission. The "title" field shows a required-field validation message. localStorage is unchanged.

---

### TC-018

| Field | Value |
|---|---|
| ID | TC-018 |
| Scenario ID | TS-N-004 |
| Title | Save blocked when required field `description` is cleared |
| Linked Requirements | N-001, REQ-003 |
| Priority | P2 — High |
| Type | Negative |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on any release entry
And the user clears the "description" field completely (leaving it empty)
And the user clicks the "Update Release Note" submit button
Then the browser HTML5 required field validation fires on the "description" field
And the form is NOT submitted
And localStorage remains unchanged (no update persisted)
```

**Expected Result**: Browser native validation prevents form submission. The "description" field shows a required-field validation message. localStorage is unchanged.

---

### TC-019

| Field | Value |
|---|---|
| ID | TC-019 |
| Scenario ID | TS-N-005 |
| Title | Save blocked when required field `releaseDate` is cleared |
| Linked Requirements | N-001, REQ-003 |
| Priority | P2 — High |
| Type | Negative |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on any release entry
And the user clears the "releaseDate" date input (leaving it empty)
And the user clicks the "Update Release Note" submit button
Then the browser HTML5 required field validation fires on the "releaseDate" field
And the form is NOT submitted
And localStorage remains unchanged (no update persisted)
```

**Expected Result**: Browser native validation prevents form submission. The "releaseDate" field shows a required-field validation message. localStorage is unchanged.

---

### TC-020

| Field | Value |
|---|---|
| ID | TC-020 |
| Scenario ID | TS-N-006 |
| Title | Save blocked with custom error when `teamName` is cleared |
| Linked Requirements | N-001, REQ-003 |
| Priority | P1 — Critical |
| Type | Negative |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded (all entries have `teamName`). Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on any release entry that has a teamName value
And the user clears the "teamName" field completely (leaving it empty)
And the user clicks the "Update Release Note" submit button
Then a custom JS inline error message is displayed adjacent to the "teamName" field
And the "teamName" field receives focus
And the form is NOT submitted
And localStorage remains unchanged (no update persisted)
```

**Expected Result**: Custom JavaScript validation fires (not browser HTML5 validation). An inline error message is visible next to the `teamName` field. The field is focused. localStorage is unchanged.

---

### TC-021

| Field | Value |
|---|---|
| ID | TC-021 |
| Scenario ID | TS-N-007 |
| Title | Save without modifying any field succeeds and preserves data |
| Linked Requirements | N-002 |
| Priority | P2 — High |
| Type | Negative |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded. Application is loaded. Original entry values are noted.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
And the original values of all entries are noted
When the user clicks the "Edit" button on any release entry
And the user does not modify any form field
And the user clicks the "Update Release Note" submit button
Then the form is submitted successfully with no error
And the entry matching the original "id" in localStorage has identical field values to the pre-edit state
And no JavaScript error is thrown
And the localStorage array structure remains intact (valid JSON array)
And the total number of entries in localStorage is unchanged
```

**Expected Result**: The release note is re-saved with identical values. No error is thrown. No data loss occurs. localStorage array structure remains intact.

---

### TC-022

| Field | Value |
|---|---|
| ID | TC-022 |
| Scenario ID | TS-N-008 |
| Title | localStorage full on Save — silent failure (defect candidate) |
| Linked Requirements | N-005, NFR-003 |
| Priority | P3 — Medium |
| Type | Negative |
| Automation | MANUAL |
| Test Data | Large auxiliary data to fill localStorage close to browser quota |

**Preconditions**: localStorage must be filled close to its browser quota limit using auxiliary data (outside the `"releaseNotesDashboard.releases"` key). Application is loaded with at least one valid entry.

> **Manual execution required**: Filling localStorage to browser quota limit is not safely automatable without risk of browser instability. Execute this test manually in a controlled browser session.

```gherkin
Given the browser's localStorage is filled close to its quota limit with auxiliary data
And the localStorage key "releaseNotesDashboard.releases" contains at least one valid entry
And the application is open and the release list is rendered
When the user clicks the "Edit" button on an existing entry
And the user modifies the "title" field
And the user clicks the "Update Release Note" submit button
Then the application visually appears to save successfully (no error message shown to the user)
And the localStorage write silently fails (the "releaseNotesDashboard.releases" data is NOT updated)
And the user receives no error notification or feedback about the failure
```

**Expected Result (current behavior — defect candidate)**:
- Application gives no indication that the save failed.
- localStorage write fails silently because `saveReleases()` has no `try/catch` around `localStorage.setItem()`.
- User believes the change was saved but data is lost.

**Defect Note**: This behavior is a known gap (N-005). If confirmed, raise a Jira defect: "Application should surface an error message when localStorage write fails due to quota exceeded." The defect should recommend adding `try/catch` around `localStorage.setItem()` in `saveReleases()`.

---

## Group 3 — Boundary Scenarios (TC-023 to TC-030)

---

### TC-023

| Field | Value |
|---|---|
| ID | TC-023 |
| Scenario ID | TS-B-001 |
| Title | Edit the only release note in the list |
| Linked Requirements | B-001, REQ-007 |
| Priority | P1 — Critical |
| Type | Boundary |
| Automation | AUTO |
| Test Data | SD-002 (single entry) |

**Preconditions**: localStorage is cleared and seeded with exactly 1 entry (SD-002). Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" contains exactly 1 entry (SD-002)
And the application is open and the release list displays exactly 1 entry
When the user clicks the "Edit" button on the single release entry
And the user modifies the "title" field to "Only Entry Updated"
And the user clicks the "Update Release Note" submit button
Then the form is submitted successfully with no validation error
And the release list re-renders and displays exactly 1 entry with title "Only Entry Updated"
And no duplicate entry is created
And the release list does not display an empty-list state
And localStorage contains exactly 1 entry with the updated title
```

**Expected Result**: List re-renders with exactly one updated entry. No duplicate. No empty-list state shown. localStorage has exactly 1 entry.

---

### TC-024

| Field | Value |
|---|---|
| ID | TC-024 |
| Scenario ID | TS-B-002 |
| Title | Edit with no active filters applied |
| Linked Requirements | B-002, REQ-007 |
| Priority | P3 — Medium |
| Type | Boundary |
| Automation | AUTO |
| Test Data | SD-001, Filter Setup FS-005 |

**Preconditions**: SD-001 is seeded. Application is loaded with no filters active (all filter inputs are blank or set to "all").

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
And no filters are active (product filter is blank, breaking filter is "all", search filter is blank)
And all 5 entries are visible in the release list
When the user clicks the "Edit" button on any release entry
And the user modifies the "version" field to "0.0.1"
And the user clicks the "Update Release Note" submit button
Then the form is submitted successfully with no validation error
And the release list re-renders and displays all 5 entries (no filter restriction applied)
And the edited entry appears in the list with version "0.0.1"
And no other entries are removed or duplicated
```

**Expected Result**: All 5 entries are rendered after the edit. The edited entry shows the new version. No filter restriction is applied.

---

### TC-025

| Field | Value |
|---|---|
| ID | TC-025 |
| Scenario ID | TS-B-003 |
| Title | Edited entry disappears when it no longer matches active product filter |
| Linked Requirements | B-003, REQ-007, REQ-009, AC-4 |
| Priority | P1 — Critical |
| Type | Boundary |
| Automation | AUTO |
| Test Data | SD-008, Filter Setup FS-001 |

**Preconditions**: SD-008 is seeded (1 entry with `product = "ProductA"`, 1 entry with `product = "ProductB"`). Application is loaded. Product filter is set to "ProductA".

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-008
And the application is open
And the product filter is set to "ProductA"
And the release list shows only the "ProductA" entry
When the user clicks the "Edit" button on the "ProductA" entry
And the user changes the "product" field to "ProductB"
And the user clicks the "Update Release Note" submit button
Then the form is submitted successfully with no validation error
And the edited entry is NO LONGER visible in the filtered list (because it no longer matches product "ProductA")
And the product filter input still displays "ProductA"
And the release list shows zero entries matching the "ProductA" filter
And the edited entry exists in localStorage with product equal to "ProductB"
```

**Expected Result**: The edited entry disappears from the filtered view because it no longer matches the active "ProductA" filter. The entry is present in localStorage with `product = "ProductB"`. The product filter remains set to "ProductA". This is expected behavior (B-003 confirmed).

---

### TC-026

| Field | Value |
|---|---|
| ID | TC-026 |
| Scenario ID | TS-B-004 |
| Title | Edit entry with `isBreaking = true` — checkbox pre-fills as checked |
| Linked Requirements | B-004, REQ-003, AC-1 |
| Priority | P2 — High |
| Type | Boundary |
| Automation | AUTO |
| Test Data | SD-003 (entry with `isBreaking = true`) |

**Preconditions**: SD-003 is seeded (entry with `isBreaking = true`). Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-003
And the application is open and the release list is rendered
When the user clicks the "Edit" button on the entry with isBreaking equal to true
Then the form scrolls into view and populates with the entry's values
And the "breaking" checkbox on the form is in a checked (ticked) state before any user interaction
```

**Expected Result**: The "breaking" checkbox renders in a checked state immediately on form pre-fill, before any user interaction. This confirms `releaseForm.breaking.checked = Boolean(release.isBreaking)` works correctly for `true` values.

---

### TC-027

| Field | Value |
|---|---|
| ID | TC-027 |
| Scenario ID | TS-B-005 |
| Title | Edit entry with `releaseDate = "1970-01-01"` — date pre-fills correctly |
| Linked Requirements | B-005, REQ-003, AC-1 |
| Priority | P2 — High |
| Type | Boundary |
| Automation | AUTO |
| Test Data | SD-004 (entry with `releaseDate = "1970-01-01"`) |

**Preconditions**: SD-004 is seeded (entry with `releaseDate = "1970-01-01"`). Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-004
And the application is open and the release list is rendered
When the user clicks the "Edit" button on the entry with releaseDate "1970-01-01"
Then the form scrolls into view and populates with the entry's values
And the "releaseDate" date input displays "1970-01-01"
And no truncation, epoch conversion error, or incorrect date offset occurs
```

**Expected Result**: The date input shows "1970-01-01" exactly as stored. No epoch/timestamp conversion errors. Cross-browser spot-check recommended (Chromium, Firefox, WebKit).

---

### TC-028

| Field | Value |
|---|---|
| ID | TC-028 |
| Scenario ID | TS-B-005b |
| Title | Edit entry with `releaseDate = today's date` — date pre-fills correctly |
| Linked Requirements | B-005, REQ-003, AC-1 |
| Priority | P3 — Medium |
| Type | Boundary |
| Automation | AUTO |
| Test Data | SD-005 (entry with `releaseDate = <today in YYYY-MM-DD>`) |

**Preconditions**: SD-005 is seeded (entry with `releaseDate` set to today's date in `YYYY-MM-DD` format). Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-005
And SD-005 has an entry with releaseDate equal to today's date in YYYY-MM-DD format
And the application is open and the release list is rendered
When the user clicks the "Edit" button on the entry with today's releaseDate
Then the form scrolls into view and populates with the entry's values
And the "releaseDate" date input displays today's date in YYYY-MM-DD format
And no date offset, timezone shift, or incorrect value is shown
```

**Expected Result**: The date input shows today's date in `YYYY-MM-DD` format exactly as stored. No timezone-related discrepancy occurs.

---

### TC-029

| Field | Value |
|---|---|
| ID | TC-029 |
| Scenario ID | TS-B-007 |
| Title | All three filters active simultaneously — all persist after Save |
| Linked Requirements | AC-4, REQ-009, NFR-004 |
| Priority | P2 — High |
| Type | Boundary |
| Automation | AUTO |
| Test Data | SD-001, Filter Setup FS-004 |

**Preconditions**: SD-001 is seeded. Application is loaded. All three filters are active: product filter = "ProductA", breaking filter = "breaking", search filter = "release". At least one entry must match all three filters simultaneously.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
And the product filter is set to "ProductA"
And the breaking filter is set to "breaking"
And the search filter is set to "release"
And the release list shows only entries matching all three filters simultaneously
When the user clicks the "Edit" button on a visible entry that matches all three filters
And the user changes the "title" field to include the word "release" (preserving search match)
And the user clicks the "Update Release Note" submit button
Then the form is submitted successfully with no validation error
And the product filter input still displays "ProductA"
And the breaking filter select still shows "breaking"
And the search filter input still contains "release"
And the rendered release list reflects the combined AND filter of all three active filters
```

**Expected Result**: All three filter inputs retain their values after Save. The rendered list reflects the combined AND-filter. The edit is visible if the entry still matches all three filters.

---

### TC-030

| Field | Value |
|---|---|
| ID | TC-030 |
| Scenario ID | TS-B-008 |
| Title | Edit one entry from a 100-entry dataset — no visible performance lag |
| Linked Requirements | B-006 |
| Priority | P3 — Medium |
| Type | Boundary |
| Automation | MANUAL |
| Test Data | SD-007 (100-entry dataset) |

**Preconditions**: SD-007 is seeded (100 entries with randomized values). Application is loaded. Tester observes browser rendering performance visually.

> **Manual execution required**: Performance judgment (visible lag) requires human observation. No hard SLA is defined. Record observed render time in the test report and establish a baseline on first run.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-007 (100 entries)
And the application is open and the release list is rendered with all 100 entries visible
When the user clicks the "Edit" button on any one of the 100 entries
And the user modifies the "title" field
And the user clicks the "Update Release Note" submit button
Then the form is submitted successfully
And the release list re-renders within 2 seconds (as observed by the tester)
And no browser freeze, unresponsive tab, or visible rendering lag occurs
And all 100 entries are displayed after re-render (or the filtered subset if filters are active)
```

**Expected Result**: List re-renders in under 2 seconds (subjective threshold). No browser freeze or visible lag. All 100 entries are displayed correctly after re-render.

**Performance Note**: Record actual observed re-render time in test execution results. If lag is noticeable, raise a performance defect with benchmark data.

---

## Group 4 — Regression Scenarios (TC-031 to TC-042)

---

### TC-031

| Field | Value |
|---|---|
| ID | TC-031 |
| Scenario ID | TS-R-001 |
| Title | Create → Edit → Create: second create adds new entry with blank form |
| Linked Requirements | NFR-003 (form state leakage) |
| Priority | P1 — Critical |
| Type | Regression |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on entry A
And the user changes the "product" field to "EditedProduct"
And the user clicks the "Update Release Note" submit button
And the form returns to create mode
And the user fills the create form with new distinct values:
  | product     | NewEntryProduct  |
  | version     | 1.0.0            |
  | title       | New Entry Title  |
  | description | New description  |
  | releaseDate | 2025-01-01       |
  | teamName    | NewTeam          |
And the user clicks the "Add Release" submit button
Then a new entry is created in localStorage with id different from all pre-existing ids
And the new entry has product equal to "NewEntryProduct" (no stale edit value "EditedProduct" leaked)
And the new entry has all fields matching the values entered in the create form
And both the originally edited entry A and the new entry B exist in localStorage
And the total entry count in localStorage equals the SD-001 count plus 1
```

**Expected Result**: The second create adds a brand-new entry with a new `id`. No stale values from the prior edit session are leaked into the new entry. Both the edited entry A and the new entry B exist in localStorage.

---

### TC-032

| Field | Value |
|---|---|
| ID | TC-032 |
| Scenario ID | TS-R-002 |
| Title | Edit → Save → Delete: delete removes correct entry and list re-renders |
| Linked Requirements | NFR-003 (delete regression) |
| Priority | P2 — High |
| Type | Regression |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on entry A (with a known stable id "test-id-001")
And the user changes the "title" field to "Pre-Delete Title"
And the user clicks the "Update Release Note" submit button
And the entry "test-id-001" is updated in localStorage with title "Pre-Delete Title"
And the user clicks the "Delete" button on the entry with id "test-id-001"
And the browser confirmation dialog "Delete this release note?" appears
And the user confirms the deletion
Then the entry with id "test-id-001" is removed from localStorage
And the release list re-renders without the deleted entry
And all other entries remain present in localStorage with their original values
And no JavaScript error is thrown during or after the delete
```

**Expected Result**: The deleted entry is absent from both the list and localStorage. All other entries are intact. No JS errors occur.

---

### TC-033

| Field | Value |
|---|---|
| ID | TC-033 |
| Scenario ID | TS-R-003 |
| Title | Edit → Save → Export: CSV export reflects updated values |
| Linked Requirements | NFR-003 (export regression) |
| Priority | P2 — High |
| Type | Regression |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on any release entry
And the user changes the "product" field to "ExportTestProduct"
And the user changes the "title" field to "ExportTestTitle"
And the user clicks the "Update Release Note" submit button
And the entry is updated in localStorage
And the user clicks the "Export CSV" button
Then a CSV file is downloaded
And the CSV file contains a row with product "ExportTestProduct" and title "ExportTestTitle"
And the CSV schema columns are exactly: product, version, teamName, title, description, releaseDate, isBreaking
And the CSV contains no data from the pre-edit values of the modified entry
```

**Expected Result**: The downloaded CSV reflects the updated `product` and `title`. The CSV schema is intact (`product,version,teamName,title,description,releaseDate,isBreaking`). No old values are exported.

---

### TC-034

| Field | Value |
|---|---|
| ID | TC-034 |
| Scenario ID | TS-R-004 |
| Title | Edit → Cancel → Create: create form is blank and adds new entry |
| Linked Requirements | NFR-003 (cancel-then-create) |
| Priority | P1 — Critical |
| Type | Regression |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on any release entry
And the user changes the "product" field to "CancelledProduct"
And the user changes the "title" field to "Cancelled Title"
And the user clicks the "Cancel Edit" button
And the form returns to create mode with all fields cleared
And the user fills the create form with distinct new values:
  | product     | FreshProduct   |
  | version     | 2.0.0          |
  | title       | Fresh Title    |
  | description | Fresh content  |
  | releaseDate | 2025-06-01     |
  | teamName    | FreshTeam      |
And the user clicks the "Add Release" submit button
Then the create form contained no pre-filled values from the cancelled edit (form was blank before new values were entered)
And a new entry is created in localStorage with product "FreshProduct" and title "Fresh Title"
And the new entry id is unique (not matching any pre-existing id)
And the original entry that was "cancelled-edited" still has its original unchanged values in localStorage
```

**Expected Result**: The create form shows no stale values from the cancelled edit. The new entry is created with only the values entered in the create form. The original (un-edited) entry remains unchanged in localStorage.

---

### TC-035

| Field | Value |
|---|---|
| ID | TC-035 |
| Scenario ID | TS-R-005 |
| Title | Edit one entry — all other entries remain unchanged in localStorage |
| Linked Requirements | REQ-005, NFR-003 |
| Priority | P1 — Critical |
| Type | Regression |
| Automation | AUTO |
| Test Data | SD-001 (5 entries) |

**Preconditions**: SD-001 is seeded with exactly 5 entries having known stable ids. All field values are noted before the test. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001 (5 entries)
And the original field values of all 5 entries are recorded before the test begins
And the application is open and the release list is rendered
When the user clicks the "Edit" button on entry 3 (id "test-id-003")
And the user changes the "product" to "ModifiedProduct"
And the user changes the "version" to "7.7.7"
And the user changes the "title" to "Modified Title"
And the user clicks the "Update Release Note" submit button
Then the entry with id "test-id-003" in localStorage has the 3 changed field values
And the entry with id "test-id-001" in localStorage has field values identical to its original pre-edit state
And the entry with id "test-id-002" in localStorage has field values identical to its original pre-edit state
And the entry with id "test-id-004" in localStorage has field values identical to its original pre-edit state
And the entry with id "test-id-005" in localStorage has field values identical to its original pre-edit state
And the total number of entries in localStorage remains 5
```

**Expected Result**: Entries 1, 2, 4, and 5 are byte-for-byte identical to their pre-edit state. Entry 3 reflects exactly the 3 changed fields. Total count is still 5.

---

### TC-036

| Field | Value |
|---|---|
| ID | TC-036 |
| Scenario ID | TS-R-006 |
| Title | Edit product value — product filter returns correct results afterward |
| Linked Requirements | NFR-003 (filter regression) |
| Priority | P2 — High |
| Type | Regression |
| Automation | AUTO |
| Test Data | SD-008, Filter Setup FS-001 |

**Preconditions**: SD-008 is seeded (1 entry with `product = "ProductA"`, 1 entry with `product = "ProductB"`). Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-008
And the application is open and the release list is rendered with 2 entries
When the user clicks the "Edit" button on the "ProductA" entry
And the user changes the "product" field to "ProductB"
And the user clicks the "Update Release Note" submit button
And the entry is saved with product "ProductB" in localStorage
And the user sets the product filter to "ProductB"
Then the release list shows 2 entries matching product "ProductB" (the original ProductB entry and the just-edited one)
When the user sets the product filter to "ProductA"
Then the release list shows 0 entries matching product "ProductA"
```

**Expected Result**: After the edit, the product filter correctly reflects the change. The edited entry appears in "ProductB" filter results and does not appear in "ProductA" filter results.

---

### TC-037

| Field | Value |
|---|---|
| ID | TC-037 |
| Scenario ID | TS-R-007 |
| Title | Edit same entry twice — second edit pre-fills values from first save |
| Linked Requirements | REQ-002, REQ-003, AC-1 |
| Priority | P2 — High |
| Type | Regression |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on any entry (with original product "ProductA")
And the user changes the "product" field to "ProductX"
And the user clicks the "Update Release Note" submit button
And the entry is saved with product "ProductX" in localStorage
And the form returns to create mode
And the user clicks the "Edit" button on the same entry again
Then the form populates with the values from the first save
And the "product" field displays "ProductX" (not the original "ProductA")
And all other fields display the values as they were after the first save
```

**Expected Result**: The second edit form pre-fills using the values saved by the first edit (`product = "ProductX"`), not the original pre-first-edit values. This confirms that `startEdit()` reads from the current localStorage state.

---

### TC-038

| Field | Value |
|---|---|
| ID | TC-038 |
| Scenario ID | TS-R-008 |
| Title | Seed data: edit one seed record — other seed record unchanged |
| Linked Requirements | NFR-003 (seed data integrity) |
| Priority | P3 — Medium |
| Type | Regression |
| Automation | AUTO |
| Test Data | SD-009 (default app auto-seed of 2 records) |

**Preconditions**: localStorage is cleared. Application is loaded (auto-seeds 2 records). Both seed record values are noted.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is cleared before page load
And the application is opened (triggering the auto-seed of 2 default records)
And the release list displays exactly 2 auto-seeded entries
And the original field values of both seed records are noted
When the user clicks the "Edit" button on seed record 1
And the user changes the "title" field to "Edited Seed Title"
And the user clicks the "Update Release Note" submit button
Then seed record 1 in localStorage has title equal to "Edited Seed Title"
And seed record 2 in localStorage has field values identical to its original auto-seeded values
And no cross-contamination between seed records has occurred
```

**Expected Result**: Seed record 2 is byte-for-byte identical to its original auto-seeded values. No cross-contamination between seed records.

---

### TC-039

| Field | Value |
|---|---|
| ID | TC-039 |
| Scenario ID | TS-R-009 |
| Title | Edit entry to `isBreaking = true` — breaking filter shows it correctly |
| Linked Requirements | NFR-003 (breaking filter regression) |
| Priority | P2 — High |
| Type | Regression |
| Automation | AUTO |
| Test Data | SD-001 (entry with `isBreaking = false`), Filter Setup FS-003 |

**Preconditions**: SD-001 is seeded (contains an entry with `isBreaking = false`). Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on an entry with isBreaking equal to false
And the user checks the "breaking" checkbox
And the user clicks the "Update Release Note" submit button
And the entry is saved with isBreaking equal to true in localStorage
And the user sets the breaking filter select to "breaking"
Then the release list shows the just-edited entry (because it now has isBreaking = true)
And the entry appears correctly in the "breaking" filtered view
```

**Expected Result**: The edited entry (now `isBreaking = true`) appears when the breaking filter is set to "breaking". The breaking filter regression is confirmed as working correctly.

---

### TC-040

| Field | Value |
|---|---|
| ID | TC-040 |
| Scenario ID | TS-R-010 |
| Title | Edit title to include search keyword — search returns updated entry |
| Linked Requirements | NFR-003 (search regression) |
| Priority | P2 — High |
| Type | Regression |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded. No entry initially contains the keyword "unicornkeyword". Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And no entry in SD-001 has "unicornkeyword" in any field
And the application is open and the release list is rendered
And the user sets the search filter to "unicornkeyword"
And the release list shows zero entries (no match)
When the user clears the search filter
And the user clicks the "Edit" button on any entry
And the user changes the "title" field to include "unicornkeyword"
And the user clicks the "Update Release Note" submit button
And the entry is saved in localStorage with "unicornkeyword" in the title
And the user sets the search filter to "unicornkeyword"
Then the release list shows the just-edited entry in the search results
And the search filter is correctly applied to the updated title field
```

**Expected Result**: After the edit, the search filter "unicornkeyword" correctly returns the edited entry. This confirms that the search filter is applied against the updated localStorage data after re-render.

---

### TC-041

| Field | Value |
|---|---|
| ID | TC-041 |
| Scenario ID | TS-R-011 |
| Title | Two sequential edits on different entries — both updated independently |
| Linked Requirements | REQ-005, REQ-006 |
| Priority | P2 — High |
| Type | Regression |
| Automation | AUTO |
| Test Data | SD-001 |

**Preconditions**: SD-001 is seeded with at least 2 entries having stable known ids. Application is loaded.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on entry A (id "test-id-001")
And the user changes the "product" field to "EntryAProduct"
And the user clicks the "Update Release Note" submit button
And the form returns to create mode
And the user clicks the "Edit" button on entry B (id "test-id-002")
And the user changes the "title" field to "EntryBTitle"
And the user clicks the "Update Release Note" submit button
Then the entry with id "test-id-001" in localStorage has product equal to "EntryAProduct"
And the entry with id "test-id-002" in localStorage has title equal to "EntryBTitle"
And no id collision exists (both entries have their original distinct ids)
And no cross-contamination occurred (entry A title is unchanged; entry B product is unchanged)
And the total number of entries in localStorage is the same as before both edits
```

**Expected Result**: Entry A has updated product. Entry B has updated title. No cross-contamination between the two edits. No id collision. Total entry count is unchanged.

---

### TC-042

| Field | Value |
|---|---|
| ID | TC-042 |
| Scenario ID | TS-R-012 |
| Title | Edit → Save → Import CSV: import proceeds without crash |
| Linked Requirements | NFR-003 (import regression) |
| Priority | P3 — Medium |
| Type | Regression |
| Automation | MANUAL |
| Test Data | SD-001 + a valid CSV file conforming to the expected import schema |

**Preconditions**: SD-001 is seeded. Application is loaded. A valid CSV import file is prepared conforming to the schema: `product,version,teamName,title,description,releaseDate,isBreaking`.

> **Manual execution required**: CSV import involves `window.confirm` dialog handling and file system interaction. Execute manually as a spot-check.

```gherkin
Given the localStorage key "releaseNotesDashboard.releases" is seeded with SD-001
And the application is open and the release list is rendered
When the user clicks the "Edit" button on any release entry
And the user changes the "title" field to "Pre-Import Edit Title"
And the user clicks the "Update Release Note" submit button
And the entry is saved to localStorage with title "Pre-Import Edit Title"
And the user clicks the "Import CSV" button
And the browser confirmation dialog appears asking to confirm the import
And the user confirms the import
And the user selects a valid CSV import file
Then the import completes without any JavaScript error
And localStorage is replaced with the data from the imported CSV
And the release list re-renders showing the imported data
And no residual edit state from the prior edit session causes any error or unexpected behavior
```

**Expected Result**: Import completes successfully after a prior edit. No JavaScript error is thrown. localStorage is replaced with CSV data. The prior edit state does not interfere with the import flow.

---

## Summary

| Group | TC Range | Count | P1 | P2 | P3 | AUTO | MANUAL |
|---|---|---|---|---|---|---|---|
| Positive | TC-001 – TC-014 | 14 | 5 | 7 | 2 | 14 | 0 |
| Negative | TC-015 – TC-022 | 8 | 2 | 5 | 1 | 7 | 1 |
| Boundary | TC-023 – TC-030 | 8 | 2 | 3 | 3 | 6 | 2 |
| Regression | TC-031 – TC-042 | 12 | 3 | 7 | 2 | 10 | 2 |
| **Total** | **TC-001 – TC-042** | **42** | **12** | **22** | **8** | **37** | **5** |

### Manual-Only Test Cases

| TC ID | Reason |
|---|---|
| TC-022 | Requires filling localStorage to browser quota limit — unsafe to automate |
| TC-030 | Performance judgment (visual rendering lag) requires human observation |
| TC-042 | CSV import involves `window.confirm` and file system interaction |

### Requirement Coverage Summary

| Requirement | Covered By |
|---|---|
| REQ-001 | TC-001 |
| REQ-002 | TC-001, TC-037 |
| REQ-003 | TC-001, TC-004, TC-005, TC-006, TC-007, TC-008, TC-015–TC-020, TC-026, TC-027, TC-028 |
| REQ-004 | TC-011, TC-012 |
| REQ-005 | TC-002–TC-009, TC-035, TC-041 |
| REQ-006 | TC-002–TC-009, TC-033, TC-035, TC-041 |
| REQ-007 | TC-002, TC-003, TC-009, TC-023, TC-024, TC-025 |
| REQ-008 | TC-010, TC-034 |
| REQ-009 | TC-013, TC-014, TC-025, TC-029 |
| NFR-001 | TC-002–TC-010 |
| NFR-003 | TC-031–TC-042 |
| NFR-004 | TC-013, TC-014, TC-029 |

### Acceptance Criteria Coverage

| AC | Criterion | Covered By |
|---|---|---|
| AC-1 | Click Edit → all fields pre-filled | TC-001, TC-026, TC-027, TC-028 |
| AC-2 | Modify + Save → entry updated by id | TC-002–TC-010, TC-023, TC-025 |
| AC-3 | Cancel → no changes saved | TC-010, TC-012, TC-034 |
| AC-4 | Filters remain applied after Save or Cancel | TC-013, TC-014, TC-025, TC-029 |
