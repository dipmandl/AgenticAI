# product_release_dashboard/manual/json_export/release_notes_stability.feature
Feature: JSON Export — Release Notes Stability After Export Feature

  Background:
    Given the application is loaded with the Export JSON feature present in the UI
    And the application storage key is "releaseNotesDashboard.releases"

  # ---------------------------------------------------------------------------
  # Regression Scenarios — Verifying existing features are unaffected
  # ---------------------------------------------------------------------------

  @TC-023 @REQ-005 @story_9 @regression @high @ui
  Scenario: TC-023 Release notes list renders correctly after Export feature is added
    Given the "releaseNotesDashboard.releases" key in localStorage contains release notes
    When the user views the dashboard
    Then the release notes list renders with all expected release cards visible
    And the rendering matches the pre-Export-feature baseline

  @TC-024 @REQ-005 @story_9 @regression @high @ui
  Scenario: TC-024 Add release functionality is unaffected by the Export feature
    Given the "releaseNotesDashboard.releases" key in localStorage has been cleared
    When the user fills the Add Release Note form with valid values for product, version, title, description, and release date
    And the user submits the form
    Then the new release card is visible in the release list
    And the new release is persisted to the "releaseNotesDashboard.releases" key in localStorage

  @TC-025 @REQ-005 @story_9 @regression @high @ui
  Scenario: TC-025 Edit release functionality is unaffected by the Export feature
    Given the "releaseNotesDashboard.releases" key in localStorage contains at least 1 release note
    When the user edits an existing release and changes the title to "Updated Title"
    And the user saves the edit
    Then the updated release card displays "Updated Title" in the release list
    And the "releaseNotesDashboard.releases" key in localStorage reflects the updated title

  @TC-026 @REQ-005 @story_9 @regression @high @ui
  Scenario: TC-026 Delete release functionality is unaffected by the Export feature
    Given the "releaseNotesDashboard.releases" key in localStorage contains at least 1 release note
    When the user deletes a release using the delete action
    Then the deleted release card is no longer visible in the release list
    And the release is removed from the "releaseNotesDashboard.releases" key in localStorage

  @TC-027 @REQ-005 @story_9 @regression @medium @ui
  Scenario: TC-027 Page navigation and routing are unaffected by the Export feature
    Given the application is loaded with the Export JSON feature present
    When the user navigates through all available application views
    Then each view loads and displays correctly
    And navigation behavior matches the pre-Export-feature baseline

  @TC-028 @REQ-005 @story_9 @regression @high @ui
  Scenario: TC-028 localStorage write operations by existing code are unaffected
    Given the "releaseNotesDashboard.releases" key in localStorage has been cleared
    When the user adds 2 new releases, edits 1 release, and deletes 1 release
    Then the "releaseNotesDashboard.releases" key in localStorage reflects only the intended operations
    And no residual data from the Export JSON action is present in localStorage

  @TC-029 @REQ-005 @story_9 @regression @high @ui @manual_only
  Scenario: TC-029 No new JavaScript console errors are introduced by the Export feature
    Given the browser developer tools console is open
    When the user loads the application
    And the user clicks the "Export JSON" button
    And the user performs normal operations including add, edit, and delete
    Then no new JavaScript errors or warnings appear in the browser console that were not present before the Export feature was added
