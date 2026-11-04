# product_release_dashboard/manual/json_export/export_release_note.feature
Feature: JSON Export — Export Release Note

  Background:
    Given the user has opened the application in the browser
    And the application storage key is "releaseNotesDashboard.releases"

  # ---------------------------------------------------------------------------
  # Positive Scenarios
  # ---------------------------------------------------------------------------

  @TC-001 @REQ-001 @story_9 @positive @smoke @critical @ui
  Scenario: TC-001 Export JSON button is visible on page load
    When the user views the dashboard
    Then an "Export JSON" button is visible in the dashboard UI

  @TC-002 @REQ-002 @story_9 @positive @smoke @critical @ui
  Scenario: TC-002 Clicking Export JSON triggers a file download
    Given the "releaseNotesDashboard.releases" key in localStorage contains at least 1 release note
    When the user clicks the "Export JSON" button
    Then the browser initiates a file download

  @TC-003 @REQ-002 @story_9 @positive @regression @high @ui
  Scenario: TC-003 Downloaded file has a .json extension
    Given the "releaseNotesDashboard.releases" key in localStorage contains at least 1 release note
    When the user clicks the "Export JSON" button
    Then the downloaded file name ends with ".json"

  @TC-004 @REQ-002 @REQ-003 @story_9 @positive @smoke @critical @ui
  Scenario: TC-004 Downloaded file contains valid parseable JSON
    Given the "releaseNotesDashboard.releases" key in localStorage contains at least 1 release note
    When the user clicks the "Export JSON" button
    Then the downloaded file can be parsed as valid JSON without error
    And the parsed result is a JSON array

  @TC-005 @REQ-003 @story_9 @positive @smoke @critical @ui
  Scenario: TC-005 Exported JSON schema matches the localStorage releases schema
    Given the "releaseNotesDashboard.releases" key in localStorage contains release objects with fields "id", "product", "version", "title", "description", "releaseDate", and "isBreaking"
    When the user clicks the "Export JSON" button
    Then the parsed JSON array from the downloaded file is structurally and content-equal to the releases array in localStorage

  @TC-006 @REQ-004 @story_9 @positive @smoke @critical @ui
  Scenario: TC-006 Export with empty localStorage downloads an empty array
    Given the "releaseNotesDashboard.releases" key in localStorage has been cleared
    When the user clicks the "Export JSON" button
    Then the downloaded file contains exactly "[]"

  @TC-007 @REQ-002 @REQ-003 @story_9 @positive @regression @high @ui
  Scenario: TC-007 Export with a single release entry downloads a single-element array
    Given the "releaseNotesDashboard.releases" key in localStorage contains exactly 1 release note with known field values
    When the user clicks the "Export JSON" button
    Then the downloaded file contains a JSON array with exactly 1 element
    And that element matches the seeded release note in all fields

  @TC-008 @REQ-002 @REQ-003 @story_9 @positive @regression @high @ui
  Scenario: TC-008 Export with multiple release entries downloads all entries
    Given the "releaseNotesDashboard.releases" key in localStorage contains 5 release notes with known field values
    When the user clicks the "Export JSON" button
    Then the downloaded file contains a JSON array with exactly 5 elements
    And each element matches the corresponding seeded release note in order and content

  # ---------------------------------------------------------------------------
  # Negative Scenarios
  # ---------------------------------------------------------------------------

  @TC-009 @REQ-004 @story_9 @negative @smoke @critical @ui
  Scenario: TC-009 Export with empty localStorage does not skip the download
    Given the "releaseNotesDashboard.releases" key in localStorage has been cleared
    When the user clicks the "Export JSON" button
    Then a file download is triggered
    And the downloaded file contains "[]"

  @TC-010 @REQ-002 @REQ-005 @story_9 @negative @regression @high @ui
  Scenario: TC-010 Export does not mutate localStorage
    Given the "releaseNotesDashboard.releases" key in localStorage contains 3 release notes
    And the releases data is recorded before clicking Export
    When the user clicks the "Export JSON" button
    Then the "releaseNotesDashboard.releases" key in localStorage is identical to the pre-export state
    And no entries have been added, removed, or modified

  @TC-011 @REQ-002 @REQ-004 @story_9 @negative @regression @high @ui @manual_only
  Scenario: TC-011 Export with corrupted localStorage value produces a valid or graceful result
    Given the "releaseNotesDashboard.releases" key in localStorage is set to the string "not-json"
    When the user clicks the "Export JSON" button
    Then the application does not throw an unhandled JavaScript exception visible to the user
    And the downloaded file either contains "[]" or is otherwise handled gracefully

  @TC-012 @REQ-004 @story_9 @negative @regression @high @ui
  Scenario: TC-012 Export does not break when the localStorage releases key is absent
    Given the "releaseNotesDashboard.releases" key has never been set in localStorage
    When the user clicks the "Export JSON" button
    Then a file download is triggered
    And the downloaded file contains "[]"

  @TC-013 @REQ-005 @story_9 @negative @regression @high @ui @manual_only
  Scenario: TC-013 Export does not interfere with other UI button actions
    Given the application is loaded with Add, Save, and Delete release actions available
    When the user clicks the "Export JSON" button
    And the user clicks the "Add Release Note" button and submits a new release
    And the user saves an edit to an existing release
    And the user deletes a release
    Then all existing actions behave identically to their pre-Export-feature behavior

  @TC-014 @REQ-001 @story_9 @negative @regression @medium @ui
  Scenario: TC-014 Export button is not duplicated after page reload
    Given the application is loaded
    When the user reloads the page
    Then exactly one "Export JSON" button is present in the DOM

  # ---------------------------------------------------------------------------
  # Boundary Scenarios
  # ---------------------------------------------------------------------------

  @TC-015 @REQ-004 @story_9 @boundary @smoke @critical @ui
  Scenario: TC-015 Zero releases — lower bound boundary
    Given the "releaseNotesDashboard.releases" key in localStorage has been cleared
    When the user clicks the "Export JSON" button
    Then the downloaded JSON file contains an array of length 0

  @TC-016 @REQ-002 @REQ-003 @story_9 @boundary @regression @high @ui
  Scenario: TC-016 One release — single element boundary
    Given the "releaseNotesDashboard.releases" key in localStorage contains exactly 1 release note
    When the user clicks the "Export JSON" button
    Then the downloaded JSON file contains an array of exactly 1 element
    And that element conforms to the release object schema

  @TC-017 @REQ-002 @REQ-003 @story_9 @boundary @regression @high @ui
  Scenario: TC-017 Large dataset — 100 release notes
    Given the "releaseNotesDashboard.releases" key in localStorage contains 100 release notes
    When the user clicks the "Export JSON" button
    Then the downloaded JSON file contains all 100 elements without truncation
    And the downloaded file is valid JSON

  @TC-018 @REQ-002 @REQ-003 @story_9 @boundary @regression @medium @ui
  Scenario: TC-018 Stress boundary — 1000 release notes
    Given the "releaseNotesDashboard.releases" key in localStorage contains 1000 release notes
    When the user clicks the "Export JSON" button
    Then the downloaded JSON file contains all 1000 elements
    And the export completes without a browser error
    And the downloaded file is valid JSON

  @TC-019 @REQ-003 @story_9 @boundary @regression @high @ui
  Scenario: TC-019 Special characters in release content are correctly escaped
    Given the "releaseNotesDashboard.releases" key in localStorage contains a release note whose title includes double-quote characters, newline characters, and tab characters
    When the user clicks the "Export JSON" button
    Then the downloaded file is valid and parseable JSON
    And the special characters are correctly JSON-escaped in the file
    And parsing the file recovers the original special characters intact

  @TC-020 @REQ-003 @story_9 @boundary @regression @high @ui
  Scenario: TC-020 Unicode characters in release content are preserved
    Given the "releaseNotesDashboard.releases" key in localStorage contains a release note whose title and description include Chinese, Arabic, and emoji Unicode characters
    When the user clicks the "Export JSON" button
    Then the downloaded file is valid UTF-8 JSON
    And all Unicode characters are preserved intact after parsing the downloaded file

  @TC-021 @REQ-002 @story_9 @boundary @regression @medium @ui @manual_only
  Scenario: TC-021 Multiple rapid clicks each trigger exactly one valid download
    Given the "releaseNotesDashboard.releases" key in localStorage contains 3 release notes
    When the user clicks the "Export JSON" button 5 times in rapid succession
    Then 5 file downloads are triggered
    And each downloaded file is a valid JSON array containing all 3 release elements

  @TC-022 @REQ-002 @REQ-003 @story_9 @boundary @regression @low @ui @manual_only
  Scenario: TC-022 Export succeeds when localStorage is near the 5 MB browser storage limit
    Given the "releaseNotesDashboard.releases" key in localStorage is populated with release notes approaching the 5 MB browser storage limit
    When the user clicks the "Export JSON" button
    Then the export completes successfully
    And the downloaded JSON file is valid with no content truncation
