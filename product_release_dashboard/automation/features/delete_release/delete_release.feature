# automation/features/delete_release/delete_release.feature
# Story:  COD-8 — Delete a Release Note with Confirmation
# Source: product_release_dashboard/manual/delete_release/delete_release.feature
#
# Excluded (manual_only):
#   TC-012 — requires direct browser-console JS injection
#   TC-024 — requires a second browser tab / driver instance

Feature: Delete Release Note — Delete a Release Note with Confirmation

  Background:
    Given the user has opened the application in the browser
    And the application storage key is "releaseNotesDashboard.releases"

  # ---------------------------------------------------------------------------
  # Positive Scenarios — TC-001 to TC-008
  # ---------------------------------------------------------------------------

  @TC-001 @REQ-001 @story_8 @positive @smoke @critical @ui
  Scenario: TC-001 Delete button is visible on every rendered release card
    Given the "releaseNotesDashboard.releases" key in localStorage contains at least 1 release note
    When the user views the release list
    Then every rendered release card has a visible Delete button

  @TC-002 @REQ-002 @story_8 @positive @smoke @critical @ui
  Scenario: TC-002 Clicking Delete shows a browser confirmation dialog
    Given the "releaseNotesDashboard.releases" key in localStorage contains at least 1 release note
    When the user clicks the Delete button on a release card
    Then a browser confirmation dialog is displayed before any deletion occurs
    And no release has been removed from the DOM at the point the dialog appears

  @TC-003 @REQ-003 @REQ-005 @story_8 @positive @smoke @critical @ui
  Scenario: TC-003 Confirmed deletion removes the targeted release card from the DOM
    Given the "releaseNotesDashboard.releases" key in localStorage contains exactly 2 release notes
    And the user observes 2 release cards in the DOM
    When the user clicks the Delete button on the first release card
    And the user accepts the confirmation dialog
    Then the targeted release card is no longer visible in the DOM
    And the total count of visible release cards is 1

  @TC-004 @REQ-004 @story_8 @positive @smoke @critical @ui
  Scenario: TC-004 Confirmed deletion removes the release from localStorage
    Given the "releaseNotesDashboard.releases" key in localStorage contains at least 1 release note with a known ID
    When the user clicks the Delete button on that release card
    And the user accepts the confirmation dialog
    Then the "releaseNotesDashboard.releases" key in localStorage no longer contains an entry with the deleted release ID

  @TC-005 @REQ-003 @REQ-005 @story_8 @positive @smoke @critical @ui
  Scenario: TC-005 Release card count decreases by exactly one after a confirmed deletion
    Given the "releaseNotesDashboard.releases" key in localStorage contains exactly 3 release notes
    And the user observes exactly 3 release cards in the DOM
    When the user clicks the Delete button on one release card
    And the user accepts the confirmation dialog
    Then exactly 2 release cards are visible in the DOM
    And the "releaseNotesDashboard.releases" key in localStorage contains exactly 2 entries

  @TC-006 @REQ-003 @REQ-005 @story_8 @positive @regression @high @ui
  Scenario: TC-006 Other releases are unaffected after a single confirmed deletion
    Given the "releaseNotesDashboard.releases" key in localStorage contains 3 release notes with titles "Release Alpha", "Release Beta", and "Release Gamma"
    When the user clicks the Delete button on the release card with title "Release Beta"
    And the user accepts the confirmation dialog
    Then the release card with title "Release Alpha" remains visible in the DOM
    And the release card with title "Release Gamma" remains visible in the DOM
    And the "releaseNotesDashboard.releases" key in localStorage contains exactly 2 entries
    And neither entry in localStorage has been modified

  @TC-007 @REQ-004 @story_8 @positive @regression @high @ui
  Scenario: TC-007 Deleted release does not reappear after a page reload
    Given the "releaseNotesDashboard.releases" key in localStorage contains at least 1 release note with title "Release To Delete"
    When the user clicks the Delete button on the release card with title "Release To Delete"
    And the user accepts the confirmation dialog
    And the user reloads the page
    Then the release card with title "Release To Delete" is not visible in the DOM after reload
    And the "releaseNotesDashboard.releases" key in localStorage does not contain the deleted release

  @TC-008 @REQ-003 @REQ-004 @REQ-005 @story_8 @positive @regression @high @ui
  Scenario: TC-008 Deleting a release that is open in edit mode resets the form and removes the card
    Given the "releaseNotesDashboard.releases" key in localStorage contains at least 1 release note
    And the user has clicked the Edit button on a release card to open the edit form with its data
    When the user clicks the Delete button on the same release card
    And the user accepts the confirmation dialog
    Then the edit form is cleared and reset to its default empty state
    And the deleted release card is no longer visible in the DOM
    And the "releaseNotesDashboard.releases" key in localStorage does not contain the deleted release

  # ---------------------------------------------------------------------------
  # Negative Scenarios — TC-009 to TC-013
  # ---------------------------------------------------------------------------

  @TC-009 @REQ-006 @story_8 @negative @smoke @high @ui
  Scenario: TC-009 Cancelling the confirmation dialog keeps the release visible in the UI
    Given the "releaseNotesDashboard.releases" key in localStorage contains at least 1 release note
    And the user observes the current count of release cards in the DOM
    When the user clicks the Delete button on a release card
    And the user cancels the confirmation dialog
    Then all release cards remain visible in the DOM
    And the release card count is unchanged from before the Delete button was clicked

  @TC-010 @REQ-006 @story_8 @negative @regression @high @ui
  Scenario: TC-010 Cancelling the confirmation dialog leaves localStorage unchanged
    Given the "releaseNotesDashboard.releases" key in localStorage contains at least 1 release note
    And the user records the current value of the "releaseNotesDashboard.releases" localStorage key before clicking Delete
    When the user clicks the Delete button on a release card
    And the user cancels the confirmation dialog
    Then the "releaseNotesDashboard.releases" key in localStorage is identical to the value recorded before the Delete button was clicked

  @TC-011 @REQ-006 @story_8 @negative @regression @high @ui
  Scenario: TC-011 Dismissing the confirmation dialog without confirming has the same effect as cancelling
    Given the "releaseNotesDashboard.releases" key in localStorage contains at least 1 release note
    When the user clicks the Delete button on a release card
    And the user dismisses the confirmation dialog without confirming
    Then the release card remains visible in the DOM
    And the "releaseNotesDashboard.releases" key in localStorage is unchanged

  @TC-013 @REQ-003 @REQ-004 @story_8 @negative @regression @low @ui
  Scenario: TC-013 Rapid successive deletions do not corrupt the releases state
    Given the "releaseNotesDashboard.releases" key in localStorage contains exactly 3 release notes
    When the user deletes the first release card and immediately accepts the confirmation dialog
    And the user immediately deletes the next release card and accepts the confirmation dialog without waiting
    Then both deletions are applied correctly
    And the one remaining release card is intact in the DOM
    And the "releaseNotesDashboard.releases" key in localStorage contains exactly 1 entry

  # ---------------------------------------------------------------------------
  # Boundary Scenarios — TC-014 to TC-018
  # ---------------------------------------------------------------------------

  @TC-014 @REQ-003 @REQ-004 @REQ-005 @story_8 @boundary @smoke @high @ui
  Scenario: TC-014 Deleting the only remaining release renders the empty state
    Given the "releaseNotesDashboard.releases" key in localStorage contains exactly 1 release note
    When the user clicks the Delete button on the only release card
    And the user accepts the confirmation dialog
    Then no release cards are visible in the DOM
    And the release list displays the empty state element
    And the "releaseNotesDashboard.releases" key in localStorage contains an empty array

  @TC-015 @REQ-003 @REQ-005 @story_8 @boundary @regression @high @ui
  Scenario: TC-015 Deleting the first release in the list leaves the remaining releases intact
    Given the "releaseNotesDashboard.releases" key in localStorage contains 3 release notes with titles "Release A", "Release B", and "Release C" in that order
    When the user clicks the Delete button on the first release card with title "Release A"
    And the user accepts the confirmation dialog
    Then the first visible release card now has the title "Release B"
    And the release card with title "Release C" remains present in the DOM
    And the total count of release cards is 2
    And the "releaseNotesDashboard.releases" key in localStorage contains exactly 2 entries

  @TC-016 @REQ-003 @REQ-005 @story_8 @boundary @regression @high @ui
  Scenario: TC-016 Deleting the last release in the list leaves the remaining releases intact
    Given the "releaseNotesDashboard.releases" key in localStorage contains 3 release notes with titles "Release A", "Release B", and "Release C" in that order
    When the user clicks the Delete button on the last release card with title "Release C"
    And the user accepts the confirmation dialog
    Then the release card with title "Release A" remains present in the DOM
    And the release card with title "Release B" remains present in the DOM
    And the total count of release cards is 2
    And the "releaseNotesDashboard.releases" key in localStorage contains exactly 2 entries

  @TC-017 @REQ-005 @story_8 @boundary @regression @medium @ui
  Scenario: TC-017 Active product filter is preserved after a deletion triggers re-render
    Given the "releaseNotesDashboard.releases" key in localStorage contains 3 release notes where 2 share the product name "Billing API"
    And the user has applied the product filter "Billing API" so that only 2 matching release cards are shown
    When the user clicks the Delete button on one of the visible filtered release cards
    And the user accepts the confirmation dialog
    Then the active product filter "Billing API" remains selected in the filter control
    And the filtered list shows exactly 1 matching release card
    And the non-matching release card remains hidden from the filtered view

  @TC-018 @REQ-004 @story_8 @boundary @regression @high @ui
  Scenario: TC-018 Deleted release remains absent after multiple consecutive page reloads
    Given the "releaseNotesDashboard.releases" key in localStorage contains at least 1 release note with title "Persistent Release"
    When the user clicks the Delete button on the release card with title "Persistent Release"
    And the user accepts the confirmation dialog
    And the user reloads the page twice in succession
    Then the release card with title "Persistent Release" is not visible in the DOM after either reload
    And the "releaseNotesDashboard.releases" key in localStorage does not contain the deleted release

  # ---------------------------------------------------------------------------
  # Regression Scenarios — TC-019 to TC-023
  # ---------------------------------------------------------------------------

  @TC-019 @REQ-004 @story_8 @regression @high @ui
  Scenario: TC-019 Add release still persists correctly after delete code changes
    Given the "releaseNotesDashboard.releases" key in localStorage has been cleared
    When the user fills the Add Release Note form with valid data, submits the form, and reloads the page
    Then the new release card is visible in the release list after reload
    And the "releaseNotesDashboard.releases" key in localStorage contains the newly added release

  @TC-020 @REQ-003 @REQ-005 @story_8 @regression @medium @ui
  Scenario: TC-020 Edit form for release A is unaffected when a different release B is deleted
    Given the "releaseNotesDashboard.releases" key in localStorage contains 2 release notes with titles "Release A" and "Release B"
    And the user has clicked the Edit button on the release card with title "Release A" to open the edit form
    When the user clicks the Delete button on the release card with title "Release B"
    And the user accepts the confirmation dialog
    Then the edit form still displays the data belonging to "Release A" unchanged
    And the release card with title "Release A" remains visible in the DOM
    And the "releaseNotesDashboard.releases" key in localStorage still contains "Release A" unchanged

  @TC-021 @REQ-005 @story_8 @regression @high @ui
  Scenario: TC-021 Filter and search results are correct after a release is deleted
    Given the "releaseNotesDashboard.releases" key in localStorage contains 3 release notes where 2 have titles containing the keyword "Payments"
    And the user has entered "Payments" in the search input so that 2 matching cards are shown
    When the user clicks the Delete button on one of the 2 matching release cards
    And the user accepts the confirmation dialog
    And the user re-enters "Payments" in the search input
    Then the filtered list shows exactly 1 matching release card
    And the non-matching release remains hidden from the search results
    And the deleted release card does not appear in any search result

  @TC-022 @REQ-004 @story_8 @regression @high @ui
  Scenario: TC-022 JSON export does not include a release that has been deleted
    Given the "releaseNotesDashboard.releases" key in localStorage contains 2 release notes with titles "Export Me" and "Delete Me"
    When the user clicks the Delete button on the release card with title "Delete Me"
    And the user accepts the confirmation dialog
    And the user clicks the "Export JSON" button
    Then the exported JSON file contains exactly 1 entry
    And that entry has the title "Export Me"
    And no entry with title "Delete Me" is present in the exported JSON file

  @TC-023 @REQ-004 @REQ-005 @story_8 @regression @medium @ui
  Scenario: TC-023 Application shows correct state when all releases are deleted and page is reloaded
    Given the "releaseNotesDashboard.releases" key in localStorage contains at least 1 release note
    When the user deletes all existing release notes by confirming each deletion in turn
    And the user reloads the page
    Then the application loads without any JavaScript errors
    And the release list is either empty or shows only deterministic seed data
    And the "releaseNotesDashboard.releases" key in localStorage reflects the post-deletion state consistently
