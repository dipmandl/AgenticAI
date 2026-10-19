# product_release_dashboard/manual/features/REQ-002-happy-path-submission.feature
# TC-REQ002-001 through TC-REQ002-006 | Happy path submission scenarios
# Requirement: REQ-002 — Release Form Happy Path Submission Testing (Jira CS-50)
# Test Plan:   TP-001
# Automation:  test_happy_path_submission.py (tc_req002_001–tc_req002_006)
#
# Ambiguity resolutions applied:
#   AMB-001 (badge selector)    : .badge.breaking with text "Breaking Change";
#                                  .badge.safe with text "Non-Breaking";
#                                  card element gets class "breaking" when isBreaking=true
#   AMB-002 (form reset)        : native releaseForm.reset() confirmed in script.js line 33
#   AMB-003 (date display)      : toLocaleDateString(undefined,{year:'numeric',month:'short',day:'numeric'})
#                                  locale-dependent; assertions use partial/contains match on year "2026"
#   AMB-005 (error indicators)  : no explicit error DOM elements exist; error suppression validated
#                                  by confirming card is created and release-list count is 3
#   AMB-006 (storage schema)    : confirmed field is "isBreaking" (boolean) from script.js line 24;
#                                  full schema: {id, product, version, title, description, releaseDate, isBreaking}

Feature: Release Note Form — Happy Path Submission (REQ-002)

  Background:
    Given the "releaseNotesDashboard.releases" key in localStorage has been cleared
    And the page has been reloaded so that exactly 2 seed entries are present in localStorage
    And the user has opened "http://localhost:8080" in the browser
    And the release list displays exactly 2 cards

  # ---------------------------------------------------------------------------
  # TC-REQ002-001 | Core happy path: card rendered after valid submission
  # FRs: REQ-002-FR-01, REQ-002-FR-02 | AC: AC-001 | Priority: CRITICAL
  # ---------------------------------------------------------------------------
  @TC-REQ002-001 @REQ-002 @REQ-002-FR-01 @REQ-002-FR-02 @AC-001 @story_002 @positive @critical @smoke @ui @functional @e2e
  Scenario: TC-REQ002-001 Valid form submission renders a release card in the release list
    When the user enters "Billing API" in the "product" field
    And the user enters "v1.0.0" in the "version" field
    And the user enters "Initial Stable Release" in the "title" field
    And the user enters "First stable release of the Billing API." in the "description" field
    And the user sets the "releaseDate" field to "2026-10-01"
    And the user clicks the "Add Release Note" button
    Then a release card containing "Billing API" and "v1.0.0" is visible in "#release-list"
    And the ".product-version" text of that card reads "Billing API - v1.0.0"
    And the ".release-title" text of that card reads "Initial Stable Release"
    And the ".release-date" text of that card contains "2026"
    And the release list displays exactly 3 cards

  # ---------------------------------------------------------------------------
  # TC-REQ002-002 | localStorage persistence after valid submission
  # FRs: REQ-002-FR-01, REQ-002-FR-03 | AC: AC-002 | Priority: CRITICAL
  # ---------------------------------------------------------------------------
  @TC-REQ002-002 @REQ-002 @REQ-002-FR-01 @REQ-002-FR-03 @AC-002 @story_002 @positive @critical @smoke @ui @functional @e2e
  Scenario: TC-REQ002-002 Valid form submission persists the entry to localStorage
    When the user enters "Billing API" in the "product" field
    And the user enters "v1.0.0" in the "version" field
    And the user enters "Initial Stable Release" in the "title" field
    And the user enters "First stable release of the Billing API." in the "description" field
    And the user sets the "releaseDate" field to "2026-10-01"
    And the user clicks the "Add Release Note" button
    Then the "releaseNotesDashboard.releases" localStorage key contains exactly 3 entries
    And the first entry in the localStorage array has product "Billing API"
    And the first entry in the localStorage array has version "v1.0.0"
    And the first entry in the localStorage array has title "Initial Stable Release"
    And the first entry in the localStorage array has releaseDate "2026-10-01"
    And the first entry in the localStorage array has isBreaking "false"

  # ---------------------------------------------------------------------------
  # TC-REQ002-003 | Form fields reset to empty after valid submission
  # FRs: REQ-002-FR-01, REQ-002-FR-04 | AC: AC-003 | Priority: CRITICAL
  # ---------------------------------------------------------------------------
  @TC-REQ002-003 @REQ-002 @REQ-002-FR-01 @REQ-002-FR-04 @AC-003 @story_002 @positive @critical @regression @ui @functional
  Scenario: TC-REQ002-003 Valid form submission resets all form fields to empty or unchecked
    When the user enters "Billing API" in the "product" field
    And the user enters "v1.0.0" in the "version" field
    And the user enters "Initial Stable Release" in the "title" field
    And the user enters "First stable release of the Billing API." in the "description" field
    And the user sets the "releaseDate" field to "2026-10-01"
    And the user clicks the "Add Release Note" button
    Then the "product" field value is empty
    And the "version" field value is empty
    And the "title" field value is empty
    And the "description" field value is empty
    And the "releaseDate" field value is empty
    And the "breaking" checkbox is unchecked

  # ---------------------------------------------------------------------------
  # TC-REQ002-004 | No validation error indicators after valid submission
  # FRs: REQ-002-FR-01, REQ-002-FR-05 | AC: AC-004 | Priority: CRITICAL
  # Note: The application (script.js) does not render explicit error DOM elements;
  #       error suppression is confirmed by successful card creation (list count = 3).
  # ---------------------------------------------------------------------------
  @TC-REQ002-004 @REQ-002 @REQ-002-FR-01 @REQ-002-FR-05 @AC-004 @story_002 @positive @critical @smoke @ui @functional
  Scenario: TC-REQ002-004 Valid form submission shows no validation error indicators in the DOM
    When the user enters "Billing API" in the "product" field
    And the user enters "v1.0.0" in the "version" field
    And the user enters "Initial Stable Release" in the "title" field
    And the user enters "First stable release of the Billing API." in the "description" field
    And the user sets the "releaseDate" field to "2026-10-01"
    And the user clicks the "Add Release Note" button
    Then zero elements with class "error" are visible anywhere on the page
    And zero elements with class "error-message" are visible anywhere on the page
    And the release list displays exactly 3 cards
    And a release card containing "Billing API" and "v1.0.0" is visible in "#release-list"

  # ---------------------------------------------------------------------------
  # TC-REQ002-005 | Persisted entry re-renders correctly after full page reload
  # FRs: REQ-002-FR-01, REQ-002-FR-02, REQ-002-FR-03, REQ-002-FR-06 | AC: AC-005
  # Priority: CRITICAL
  # ---------------------------------------------------------------------------
  @TC-REQ002-005 @REQ-002 @REQ-002-FR-01 @REQ-002-FR-02 @REQ-002-FR-03 @REQ-002-FR-06 @AC-005 @story_002 @positive @critical @regression @ui @functional @e2e
  Scenario: TC-REQ002-005 Persisted entry re-renders correctly after a full page reload
    When the user enters "Billing API" in the "product" field
    And the user enters "v1.0.0" in the "version" field
    And the user enters "Initial Stable Release" in the "title" field
    And the user enters "First stable release of the Billing API." in the "description" field
    And the user sets the "releaseDate" field to "2026-10-01"
    And the user clicks the "Add Release Note" button
    And the user reloads the page
    Then the release list displays exactly 3 cards
    And a release card containing "Billing API" and "v1.0.0" is visible in "#release-list"
    And the ".release-title" text of the "Billing API" card reads "Initial Stable Release"
    And the ".release-date" text of the "Billing API" card contains "2026"

  # ---------------------------------------------------------------------------
  # TC-REQ002-006 | Breaking-change checkbox checked → isBreaking=true and badge shown
  # FRs: REQ-002-FR-01, REQ-002-FR-07 | AC: AC-006 | Priority: CRITICAL
  # Badge resolution (AMB-001): .badge.breaking element with text "Breaking Change";
  #   the release card article also receives class "breaking" via classList.toggle()
  # ---------------------------------------------------------------------------
  @TC-REQ002-006 @REQ-002 @REQ-002-FR-01 @REQ-002-FR-07 @AC-006 @story_002 @positive @critical @smoke @ui @functional
  Scenario: TC-REQ002-006 Breaking-change checkbox checked results in isBreaking true and badge displayed on the card
    When the user enters "Auth Service" in the "product" field
    And the user enters "v3.0.0" in the "version" field
    And the user enters "Major Auth Overhaul" in the "title" field
    And the user enters "Deprecated legacy token endpoint; client migration required." in the "description" field
    And the user sets the "releaseDate" field to "2026-10-01"
    And the user checks the "breaking" checkbox
    And the user clicks the "Add Release Note" button
    Then the first entry in the localStorage array has isBreaking "true"
    And the release card for "Auth Service - v3.0.0" has CSS class "breaking" on the article element
    And the ".badge" element inside that card has CSS class "breaking"
    And the ".badge" element inside that card has text content "Breaking Change"
    And the release list displays exactly 3 cards
