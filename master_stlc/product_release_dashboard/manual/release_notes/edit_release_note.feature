Feature: Edit Release Note

  # Story: COD-7 â€” Edit Existing Release Note
  # Requirements: REQ-001 through REQ-012
  # Acceptance Criteria: AC-1 through AC-4

  Background:
    Given the "releaseNotesDashboard.releases" key in localStorage has been cleared
    And the application is open in the browser at "product_release_dashboard/index.html"
    And the seed data has loaded with "Billing API v1.4.0" (isBreaking: false, teamName: "Platform Team") and "Auth Service v2.0.0" (isBreaking: true, teamName: "Security Team")

  # ---------------------------------------------------------------------------
  # POSITIVE SCENARIOS (TC-001 to TC-018)
  # ---------------------------------------------------------------------------

  @TC-001 @REQ-001 @story_COD-7 @positive @high @functional @ui @regression
  Scenario: TC-001 Edit button is visible on every rendered release card
    When the user inspects every release card in the list
    Then each release card displays an "Edit" button

  @TC-002 @REQ-002 @story_COD-7 @positive @critical @functional @ui @regression
  Scenario: TC-002 Clicking Edit pre-fills all 7 form fields with the release data
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    Then "#product-input" shows "Billing API"
    And "#version-input" shows "v1.4.0"
    And "#team-name-input" shows "Platform Team"
    And "#title-input" shows "Invoice export now supports CSV and XLSX"
    And "#description-input" shows the release description text
    And "#release-date-input" shows "2026-06-08"
    And "#is-breaking-input" checkbox is unchecked

  @TC-003 @REQ-002 @story_COD-7 @positive @high @functional @ui @regression
  Scenario: TC-003 isBreaking checkbox pre-fills as checked for a breaking release
    When the user clicks the "Edit" button on the "Auth Service v2.0.0" release card
    Then "#is-breaking-input" checkbox is checked

  @TC-004 @REQ-002 @story_COD-7 @positive @high @functional @ui @regression
  Scenario: TC-004 isBreaking checkbox pre-fills as unchecked for a non-breaking release
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    Then "#is-breaking-input" checkbox is unchecked

  @TC-005 @REQ-004 @story_COD-7 @positive @high @functional @ui @regression
  Scenario: TC-005 Submit button label changes to "Update Release Note" in edit mode
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    Then the form submit button is visible
    And the form submit button text reads "Update Release Note"
    And the form submit button is enabled and clickable

  @TC-006 @REQ-005 @story_COD-7 @positive @high @functional @ui @regression
  Scenario: TC-006 Cancel Edit button becomes visible when edit mode is active
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    Then a "Cancel Edit" button is visible
    And the "Cancel Edit" button is clickable

  @TC-007 @REQ-006 @story_COD-7 @positive @critical @functional @ui @regression
  Scenario: TC-007 Save updates the specific release by its id
    Given the user has noted the id of the "Billing API v1.4.0" release from localStorage
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears "#title-input" and types "Updated Billing Title"
    And the user clicks "Update Release Note"
    Then the release with the original id shows "Updated Billing Title" in the rendered list
    And the entry for that id in localStorage shows title "Updated Billing Title"
    And the id value of the release is unchanged

  @TC-008 @REQ-006 @story_COD-7 @positive @critical @functional @ui @regression
  Scenario: TC-008 Save does not create a duplicate entry
    Given the rendered list contains exactly 2 release cards
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears "#title-input" and types "No Duplicate Title"
    And the user clicks "Update Release Note"
    Then the rendered list still contains exactly 2 release cards
    And the localStorage "releaseNotesDashboard.releases" array contains exactly 2 entries

  @TC-009 @REQ-006 @story_COD-7 @positive @high @functional @ui @regression
  Scenario: TC-009 Save does not modify any other release entries
    Given the user has noted all field values for the "Auth Service v2.0.0" release
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears "#title-input" and types "Changed Title"
    And the user clicks "Update Release Note"
    Then the "Auth Service v2.0.0" release card shows all its original field values unchanged
    And the "Auth Service v2.0.0" entry in localStorage is byte-for-byte identical to the recorded baseline

  @TC-010 @REQ-007 @story_COD-7 @positive @critical @functional @ui @regression
  Scenario: TC-010 Updated release is persisted to localStorage after Save
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears "#title-input" and types "Persisted Title Test"
    And the user clicks "Update Release Note"
    Then reading localStorage "releaseNotesDashboard.releases" returns a valid JSON array
    And the entry for "Billing API v1.4.0" in that array has title "Persisted Title Test"

  @TC-011 @REQ-008 @story_COD-7 @positive @high @functional @ui @regression
  Scenario: TC-011 Release list re-renders immediately with updated values after Save
    Given the "Billing API v1.4.0" card shows its original title in the rendered list
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears "#title-input" and types "Re-render Title Test"
    And the user clicks "Update Release Note"
    Then the "Billing API" card in the DOM shows "Re-render Title Test" without a page reload

  @TC-012 @REQ-009 @story_COD-7 @positive @critical @functional @ui @regression
  Scenario: TC-012 Cancel discards in-progress changes and the rendered list is unchanged
    Given the "Billing API v1.4.0" card shows its original title
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears "#title-input" and types "DISCARDED_TITLE"
    And the user clicks "Cancel Edit" without clicking "Update Release Note"
    Then the "Billing API v1.4.0" card still shows its original title
    And no card with title "DISCARDED_TITLE" is visible in the rendered list

  @TC-013 @REQ-009 @story_COD-7 @positive @high @functional @ui @regression
  Scenario: TC-013 Cancel leaves localStorage unchanged
    Given the user has recorded the current value of localStorage "releaseNotesDashboard.releases"
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears "#title-input" and types "SHOULD_NOT_PERSIST"
    And the user clears "#version-input" and types "v9.9.9"
    And the user clicks "Cancel Edit"
    Then the value of localStorage "releaseNotesDashboard.releases" is identical to the recorded baseline

  @TC-014 @REQ-010 @story_COD-7 @positive @critical @functional @ui @regression
  Scenario: TC-014 All active filters remain applied after Save
    Given the list contains at least 3 releases including a breaking release for "Billing API" with version "v1"
    And the user has set "#product-filter" to "Billing API"
    And the user has set "#breaking-filter" to "Breaking only"
    And the user has typed "v1" in "#search-filter"
    When the user clicks the "Edit" button on a visible matching release card
    And the user clears "#description-input" and types "Filter Persistence Test"
    And the user clicks "Update Release Note"
    Then "#product-filter" still shows "Billing API"
    And "#breaking-filter" still shows "Breaking only"
    And "#search-filter" still contains "v1"
    And the rendered list still applies all three filter criteria

  @TC-015 @REQ-011 @story_COD-7 @positive @high @functional @ui @regression
  Scenario: TC-015 All active filters remain applied after Cancel
    Given the user has set "#product-filter" to "Billing API"
    And the user has typed "v1" in "#search-filter"
    When the user clicks the "Edit" button on a visible matching release card
    And the user clears "#description-input" and types "Unsaved Description"
    And the user clicks "Cancel Edit"
    Then "#product-filter" still shows "Billing API"
    And "#search-filter" still contains "v1"
    And the rendered list continues to apply the same filter criteria as before

  @TC-016 @REQ-012 @story_COD-7 @positive @medium @functional @ui @regression
  Scenario: TC-016 Edit operates correctly on the first card in the list
    Given the list contains at least 3 release cards
    When the user clicks the "Edit" button on the first release card in the list
    And the user clears "#title-input" and types "First Card Updated"
    And the user clicks "Update Release Note"
    Then the first release card shows "First Card Updated"
    And no other release card is changed

  @TC-017 @REQ-012 @story_COD-7 @positive @medium @functional @ui @regression
  Scenario: TC-017 Edit operates correctly on the last card in the list
    Given the list contains at least 3 release cards
    When the user clicks the "Edit" button on the last release card in the list
    And the user clears "#title-input" and types "Last Card Updated"
    And the user clicks "Update Release Note"
    Then the last release card shows "Last Card Updated"
    And no other release card is changed

  @TC-018 @REQ-012 @story_COD-7 @positive @medium @functional @ui @regression
  Scenario: TC-018 Edit operates correctly on a middle card in the list
    Given the list contains at least 3 release cards
    When the user clicks the "Edit" button on the second release card in the list
    And the user clears "#title-input" and types "Middle Card Updated"
    And the user clicks "Update Release Note"
    Then the second release card shows "Middle Card Updated"
    And the first and last release cards are unaffected

  # ---------------------------------------------------------------------------
  # NEGATIVE SCENARIOS (TC-019 to TC-027)
  # ---------------------------------------------------------------------------

  @TC-019 @REQ-009 @story_COD-7 @negative @high @functional @ui @regression
  Scenario: TC-019 Cancel without modifying any field leaves list and localStorage unchanged
    Given the user has recorded the current value of localStorage "releaseNotesDashboard.releases"
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user does not modify any field
    And the user clicks "Cancel Edit"
    Then the rendered list is identical to its state before "Edit" was clicked
    And localStorage "releaseNotesDashboard.releases" is identical to the recorded baseline
    And the form submit button text reads "Add Release Note"
    And the "Cancel Edit" button is not visible

  @TC-020 @REQ-004 @story_COD-7 @negative @high @functional @ui @regression
  Scenario: TC-020 Save with teamName cleared shows validation error and preserves edit state
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears the "#team-name-input" field
    And the user clicks "Update Release Note"
    Then a validation error message is displayed for the team name field
    And the form remains in edit mode with the submit button reading "Update Release Note"
    And localStorage "releaseNotesDashboard.releases" is unchanged
    And the rendered release list is unchanged

  @TC-021 @REQ-004 @story_COD-7 @negative @high @functional @ui @regression
  Scenario: TC-021 Save with title cleared shows validation error
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears the "#title-input" field
    And the user clicks "Update Release Note"
    Then a validation error message is displayed
    And the form remains in edit mode with submit button reading "Update Release Note"
    And the rendered list and localStorage are unchanged

  @TC-022 @REQ-004 @story_COD-7 @negative @high @functional @ui @regression
  Scenario: TC-022 Save with product cleared shows validation error
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears the "#product-input" field
    And the user clicks "Update Release Note"
    Then a validation error message is displayed
    And the form remains in edit mode with submit button reading "Update Release Note"
    And the rendered list and localStorage are unchanged

  @TC-023 @REQ-004 @story_COD-7 @negative @high @functional @ui @regression
  Scenario: TC-023 Save with version cleared shows validation error
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears the "#version-input" field
    And the user clicks "Update Release Note"
    Then a validation error message is displayed
    And the form remains in edit mode with submit button reading "Update Release Note"
    And the rendered list and localStorage are unchanged

  @TC-024 @REQ-004 @story_COD-7 @negative @high @functional @ui @regression
  Scenario: TC-024 Save with releaseDate cleared shows validation error
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears the "#release-date-input" field
    And the user clicks "Update Release Note"
    Then a validation error message is displayed
    And the form remains in edit mode with submit button reading "Update Release Note"
    And the rendered list and localStorage are unchanged

  @TC-025 @REQ-006 @story_COD-7 @negative @high @functional @manual_only @regression
  Scenario: TC-025 Calling startEdit with a non-existent id does not crash the application
    When the user opens browser DevTools and executes "startEdit('non-existent-id-xyz')" in the console
    Then no uncaught JavaScript exception is thrown in the console
    And the form is not pre-filled with undefined or stale values
    And the application remains in a usable and stable state

  @TC-026 @REQ-002 @story_COD-7 @negative @medium @functional @ui @regression
  Scenario: TC-026 Clicking Edit on card B while card A is in edit mode replaces form with card B's values
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the form is pre-filled with "Billing API" values
    And the user clicks the "Edit" button on the "Auth Service v2.0.0" release card without saving
    Then "#product-input" shows "Auth Service"
    And "#version-input" shows "v2.0.0"
    And "#team-name-input" shows "Security Team"
    And no form field contains any value from the "Billing API v1.4.0" release

  @TC-027 @REQ-005 @REQ-009 @story_COD-7 @negative @high @functional @ui @regression
  Scenario: TC-027 Cancel after a validation failure exits edit mode cleanly
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears the "#title-input" field
    And the user clicks "Update Release Note"
    And a validation error is displayed
    And the user clicks "Cancel Edit" without fixing the validation error
    Then the form submit button text reads "Add Release Note"
    And the "Cancel Edit" button is not visible
    And the "Billing API v1.4.0" card shows its original title in the rendered list
    And localStorage "releaseNotesDashboard.releases" is unchanged from its pre-edit state

  # ---------------------------------------------------------------------------
  # BOUNDARY SCENARIOS (TC-028 to TC-039)
  # ---------------------------------------------------------------------------

  @TC-028 @REQ-002 @REQ-006 @story_COD-7 @boundary @high @functional @ui @regression
  Scenario: TC-028 Edit with all 7 fields modified then Save persists every change
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user sets "#product-input" to "Payments API"
    And the user sets "#version-input" to "v2.0.0"
    And the user sets "#team-name-input" to "Finance Team"
    And the user sets "#title-input" to "All Fields Changed Title"
    And the user sets "#description-input" to "All seven fields have been updated"
    And the user sets "#release-date-input" to "2026-12-01"
    And the user checks "#is-breaking-input"
    And the user clicks "Update Release Note"
    Then the release card shows product "Payments API", version "v2.0.0", team "Finance Team", title "All Fields Changed Title", date "2026-12-01", and isBreaking: true
    And the localStorage entry for the same id reflects all 7 updated field values
    And the total number of release cards in the list is unchanged at 2

  @TC-029 @REQ-006 @story_COD-7 @boundary @medium @functional @ui @regression
  Scenario: TC-029 Edit with exactly one field changed leaves all other fields intact
    Given the user has noted all 7 field values for "Billing API v1.4.0"
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears "#description-input" and types "Only description changed"
    And all other 6 fields are left as pre-filled
    And the user clicks "Update Release Note"
    Then the "Billing API v1.4.0" card shows "Only description changed" for description
    And product, version, teamName, title, releaseDate, and isBreaking remain identical to their original values

  @TC-030 @REQ-002 @REQ-003 @story_COD-7 @boundary @medium @functional @ui @regression
  Scenario: TC-030 Edit with teamName cleared to empty shows a validation error and does not save
    Given the Release Notes Dashboard is open with seed data loaded
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears "#team-name-input" to empty
    And the user clicks "Update Release Note"
    Then the validation error message "Team name is required." is visible in "#team-name-error"
    And the submit button label still reads "Update Release Note"
    And "releaseNotesDashboard.releases" in localStorage is unchanged from its pre-edit state

  @TC-031 @REQ-002 @REQ-006 @story_COD-7 @boundary @medium @functional @ui @regression
  Scenario: TC-031 Edit with minimum single-character values in all mandatory fields succeeds
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user sets "#product-input" to "A"
    And the user sets "#version-input" to "1"
    And the user sets "#team-name-input" to "T"
    And the user sets "#title-input" to "T"
    And the user sets "#description-input" to "D"
    And the user sets "#release-date-input" to "2026-01-01"
    And the user clicks "Update Release Note"
    Then Save succeeds with no validation error
    And the release card shows the single-character values
    And localStorage "releaseNotesDashboard.releases" is updated with the new values

  @TC-032 @REQ-002 @REQ-009 @story_COD-7 @boundary @high @functional @ui @regression
  Scenario: TC-032 Edit then Cancel then re-Edit same card shows original unchanged values
    Given the "Billing API v1.4.0" release card exists with its original title
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears "#title-input" and types "TEMP_VALUE"
    And the user clicks "Cancel Edit"
    And the user clicks the "Edit" button on the "Billing API v1.4.0" release card again
    Then "#title-input" shows the original title of "Billing API v1.4.0"
    And "#title-input" does not contain "TEMP_VALUE"

  @TC-033 @REQ-002 @story_COD-7 @boundary @high @functional @ui @regression
  Scenario: TC-033 Edit card A then Cancel then Edit card B shows only card B's values
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears "#title-input" and types "CARD_A_TEMP"
    And the user clicks "Cancel Edit"
    And the user clicks the "Edit" button on the "Auth Service v2.0.0" release card
    Then "#product-input" shows "Auth Service"
    And "#version-input" shows "v2.0.0"
    And "#team-name-input" shows "Security Team"
    And no form field contains "CARD_A_TEMP" or any value from the "Billing API v1.4.0" release

  @TC-034 @REQ-003 @story_COD-7 @boundary @low @functional @ui @regression @manual_only
  Scenario: TC-034 Edit title and description with 500-character text does not crash the application
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user pastes a 500-character string into "#title-input"
    And the user pastes a 500-character string into "#description-input"
    And the user clicks "Update Release Note"
    Then the application does not crash or throw an uncaught exception
    And the tester records whether the text is saved as-is or truncated with a visible message
    And the localStorage entry reflects the actual saved value without JSON parse errors

  @TC-035 @REQ-003 @story_COD-7 @boundary @low @functional @ui @regression @manual_only
  Scenario: TC-035 Edit text fields with special characters are stored and rendered safely
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user sets "#title-input" to the text: <script>alert(1)</script>
    And the user sets "#description-input" to the text: "quotes" & ampersand
    And the user clicks "Update Release Note"
    Then the release card renders the special characters as literal visible text
    And no script tag or alert is executed in the browser
    And localStorage stores the values without JSON parse errors

  @TC-036 @REQ-002 @REQ-006 @story_COD-7 @boundary @high @functional @ui @regression
  Scenario: TC-036 Toggle isBreaking from true to false and Save persists the change
    When the user clicks the "Edit" button on the "Auth Service v2.0.0" release card
    And "#is-breaking-input" is verified to be checked
    And the user unchecks "#is-breaking-input"
    And the user clicks "Update Release Note"
    Then the "Auth Service v2.0.0" release card displays as non-breaking
    And the localStorage entry for "Auth Service v2.0.0" has isBreaking value of false

  @TC-037 @REQ-002 @REQ-006 @story_COD-7 @boundary @high @functional @ui @regression
  Scenario: TC-037 Toggle isBreaking from false to true and Save persists the change
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And "#is-breaking-input" is verified to be unchecked
    And the user checks "#is-breaking-input"
    And the user clicks "Update Release Note"
    Then the "Billing API v1.4.0" release card displays as breaking
    And the localStorage entry for "Billing API v1.4.0" has isBreaking value of true

  @TC-038 @REQ-012 @story_COD-7 @boundary @medium @functional @ui @regression
  Scenario: TC-038 Edit operates correctly when the list contains exactly one entry
    Given localStorage "releaseNotesDashboard.releases" is set to contain exactly one release "Billing API v1.4.0"
    And the rendered list shows exactly 1 release card
    When the user clicks the "Edit" button on the single release card
    And the user clears "#title-input" and types "Solo Card Updated"
    And the user clicks "Update Release Note"
    Then the list shows exactly 1 release card with title "Solo Card Updated"
    And localStorage contains exactly 1 entry with title "Solo Card Updated"

  @TC-039 @REQ-010 @story_COD-7 @boundary @medium @functional @ui @regression
  Scenario: TC-039 Edit with no filters active leaves all filter controls cleared after Save
    Given "#product-filter" shows "All", "#breaking-filter" shows "All", and "#search-filter" is empty
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the user clears "#title-input" and types "Baseline Filter Test"
    And the user clicks "Update Release Note"
    Then "#product-filter" still shows "All"
    And "#breaking-filter" still shows "All"
    And "#search-filter" is still empty
    And all release cards are rendered with no filter restriction
    And the edited card shows title "Baseline Filter Test"

  # ---------------------------------------------------------------------------
  # REGRESSION SCENARIOS (TC-040 to TC-051)
  # ---------------------------------------------------------------------------

  @TC-040 @REQ-006 @story_COD-7 @regression @high @functional @ui
  Scenario: TC-040 Create new release still works after Edit and Save
    Given the list contains exactly 2 release cards
    When the user clicks "Edit" on "Billing API v1.4.0", changes title to "Edited Billing Title", and clicks "Update Release Note"
    And the user fills "#product-input" with "New Product", "#version-input" with "v3.0.0", "#team-name-input" with "New Team", "#title-input" with "Brand New Release", "#description-input" with "New release description", and "#release-date-input" with "2026-11-01"
    And the user clicks "Add Release Note"
    Then the list contains exactly 3 release cards
    And a card with title "Brand New Release" is visible in the list
    And the "Billing API" card still shows "Edited Billing Title"
    And localStorage "releaseNotesDashboard.releases" contains exactly 3 entries

  @TC-041 @REQ-009 @story_COD-7 @regression @high @functional @ui
  Scenario: TC-041 Create new release still works after Edit and Cancel
    Given the list contains exactly 2 release cards
    When the user clicks "Edit" on "Billing API v1.4.0", changes a field value, and clicks "Cancel Edit"
    And the user fills all required fields for a new release with title "Post-Cancel New Release"
    And the user clicks "Add Release Note"
    Then the list contains exactly 3 release cards
    And a card with title "Post-Cancel New Release" is visible
    And "Billing API v1.4.0" shows its original unchanged title
    And the form submit button reads "Add Release Note"

  @TC-042 @REQ-006 @story_COD-7 @regression @high @functional @ui
  Scenario: TC-042 Delete a different release still works after Edit and Save
    Given the list contains "Billing API v1.4.0" (A), "Auth Service v2.0.0" (B), and a third release "Payments v1.0.0" (C) added via the create form
    When the user clicks "Edit" on release A, changes the title to "A Updated", and clicks "Update Release Note"
    And the user clicks the "Delete" button on release B and confirms the deletion dialog
    Then release B is removed from the rendered list and from localStorage
    And release A shows "A Updated" in the rendered card
    And release C is unaffected with all its original field values

  @TC-043 @REQ-009 @story_COD-7 @regression @high @functional @ui
  Scenario: TC-043 Deleting the release currently in edit mode resets edit state
    When the user clicks the "Edit" button on the "Billing API v1.4.0" release card
    And the form is pre-filled with "Billing API v1.4.0" values
    And the user clicks the "Delete" button on the "Billing API v1.4.0" card and confirms the deletion dialog
    Then "Billing API v1.4.0" is removed from the rendered list
    And the form submit button reads "Add Release Note"
    And the "Cancel Edit" button is not visible
    And the user can successfully fill the create form and add a new release

  @TC-044 @REQ-010 @story_COD-7 @regression @high @functional @ui
  Scenario: TC-044 Product filter functions correctly before and after Edit and Save
    Given the list has releases for "Billing API" and "Auth Service"
    And "#product-filter" is set to "Billing API"
    When the user clicks "Edit" on the visible "Billing API v1.4.0" card, changes description, and clicks "Update Release Note"
    And the user changes "#product-filter" to "Auth Service"
    And the user changes "#product-filter" back to "Billing API"
    Then only "Billing API" releases are shown when filter is set to "Billing API"
    And only "Auth Service" releases are shown when filter is set to "Auth Service"
    And product data in localStorage is not corrupted by the edit

  @TC-045 @REQ-010 @story_COD-7 @regression @high @functional @ui
  Scenario: TC-045 Breaking-change filter functions correctly after Edit and Save
    Given "#breaking-filter" is set to "Breaking only"
    And "Auth Service v2.0.0" (isBreaking: true) is visible in the filtered list
    When the user clicks "Edit" on "Auth Service v2.0.0", changes description without modifying "#is-breaking-input", and clicks "Update Release Note"
    And the user changes "#breaking-filter" to "Non-breaking only"
    And the user changes "#breaking-filter" back to "Breaking only"
    Then "Auth Service v2.0.0" appears under "Breaking only" filter
    And "Billing API v1.4.0" appears under "Non-breaking only" filter
    And the isBreaking value of "Auth Service v2.0.0" was not unintentionally changed by the edit

  @TC-046 @REQ-010 @story_COD-7 @regression @high @functional @ui
  Scenario: TC-046 Keyword search filter functions correctly after Edit and Save
    Given the list has a release whose title contains "alpha" and one that does not
    And the user has typed "alpha" in "#search-filter" and only matching releases are shown
    When the user clicks "Edit" on the visible matching release, changes description (not title), and clicks "Update Release Note"
    And the user clears "#search-filter" and retypes "alpha"
    Then only releases whose title or description contains "alpha" are shown
    And the search filter logic is not broken by the edit

  @TC-047 @REQ-010 @story_COD-7 @regression @high @functional @ui
  Scenario: TC-047 Multi-filter combination persists correctly after Edit and Save
    Given the list has at least one breaking release for "Billing API" with version containing "v1"
    And "#product-filter" is set to "Billing API", "#breaking-filter" to "Breaking only", and "#search-filter" to "v1"
    When the user clicks "Edit" on the visible matching release, changes description, and clicks "Update Release Note"
    Then "#product-filter" still shows "Billing API"
    And "#breaking-filter" still shows "Breaking only"
    And "#search-filter" still contains "v1"
    And only releases matching all three criteria simultaneously are rendered

  @TC-048 @REQ-007 @story_COD-7 @regression @high @functional @ui
  Scenario: TC-048 Edited values persist after a full page reload
    When the user clicks "Edit" on "Billing API v1.4.0", sets title to "Reload Persistence Test", and clicks "Update Release Note"
    And the user reloads the page
    Then the release card for "Billing API" shows "Reload Persistence Test" after reload
    And no release data is lost from localStorage

  @TC-049 @REQ-007 @story_COD-7 @regression @medium @functional @ui @manual_only
  Scenario: TC-049 Export CSV contains updated values after Edit and Save
    When the user clicks "Edit" on "Billing API v1.4.0", sets title to "CSV Export Test", and clicks "Update Release Note"
    And the user clicks the "Export CSV" button
    Then a CSV file is downloaded successfully
    And the downloaded CSV contains a row with the title "CSV Export Test"
    And no other releases are missing or corrupted in the CSV file

  @TC-050 @REQ-009 @story_COD-7 @regression @medium @functional @ui @manual_only
  Scenario: TC-050 Importing JSON while in edit mode resets edit state
    When the user clicks the "Edit" button on "Billing API v1.4.0" and the form enters edit mode
    And the user triggers the JSON import action and selects a valid release JSON file
    And the user confirms the import dialog
    Then the imported releases replace the existing list
    And the form submit button reads "Add Release Note"
    And the "Cancel Edit" button is not visible
    And no orphaned edit state remains active

  @TC-051 @REQ-006 @story_COD-7 @regression @high @functional @ui
  Scenario: TC-051 Form in create mode creates a new entry and does not trigger an update
    Given the form is in create mode with no edit active
    And the form submit button reads "Add Release Note"
    And the list contains exactly 2 release cards
    When the user fills all required fields with title "Confirm Create Mode"
    And the user clicks "Add Release Note"
    Then a new release card with title "Confirm Create Mode" appears in the list
    And the list now contains exactly 3 release cards
    And no existing release entry is modified in localStorage
