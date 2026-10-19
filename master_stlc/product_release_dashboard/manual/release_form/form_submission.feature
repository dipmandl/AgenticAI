# features/release_form/form_submission.feature
# TC-001 – TC-005 | Happy path / valid submission scenarios
# Requirement: REQ-001 — Inline Form Validation for Release Notes Dashboard
# Test Plan:   TP-001

Feature: Release Note Form — Successful Submission

  Background:
    Given the "releaseNotesDashboard.releases" key in localStorage has been cleared
    And the user has opened "product_release_dashboard/index.html" in the browser

  @TC-001 @REQ-001 @REQ-001-FR-1 @REQ-001-FR-3 @AC-4 @story_001 @positive @critical @smoke @ui @functional
  Scenario: TC-001 Valid submission with all fields populated creates a release card in the release list
    When the user enters "Billing API" in the "product" field
    And the user enters "v1.0.0" in the "version" field
    And the user enters "Initial Release" in the "title" field
    And the user enters "First stable release of the product." in the "description" field
    And the user sets the "releaseDate" field to "2026-09-24"
    And the user clicks the "Add Release Note" button
    Then a release card containing "Billing API" and "v1.0.0" is visible in the release list
    And no inline error messages are visible on the form

  @TC-002 @REQ-001 @REQ-001-FR-3 @AC-4 @story_001 @positive @high @regression @functional
  Scenario: TC-002 Valid submission persists the new release entry to localStorage
    When the user enters "Payments Gateway" in the "product" field
    And the user enters "v2.0.0" in the "version" field
    And the user enters "Payment integration" in the "title" field
    And the user enters "Added Stripe integration to the payments module." in the "description" field
    And the user sets the "releaseDate" field to "2026-09-24"
    And the user clicks the "Add Release Note" button
    Then the "releaseNotesDashboard.releases" localStorage key contains 3 release entries
    And the most recently stored entry has product "Payments Gateway" and version "v2.0.0"

  @TC-003 @REQ-001 @derived @story_001 @positive @medium @regression @functional @ui
  Scenario: TC-003 All form fields are empty after a valid submission
    When the user enters "Auth Service" in the "product" field
    And the user enters "v1.1.0" in the "version" field
    And the user enters "SSO Support" in the "title" field
    And the user enters "Added SAML SSO support for enterprise customers." in the "description" field
    And the user sets the "releaseDate" field to "2026-09-24"
    And the user clicks the "Add Release Note" button
    Then the "product" field value is empty
    And the "version" field value is empty
    And the "title" field value is empty
    And the "description" field value is empty
    And the "releaseDate" field value is empty

  @TC-004 @REQ-001 @REQ-001-FR-1 @AC-1 @AC-4 @story_001 @positive @high @smoke @ui @functional
  Scenario: TC-004 Zero inline error messages are visible after a fully valid submission
    When the user enters "Notification Service" in the "product" field
    And the user enters "v3.0.0" in the "version" field
    And the user enters "Email alerts" in the "title" field
    And the user enters "Introduced configurable email alert thresholds." in the "description" field
    And the user sets the "releaseDate" field to "2026-09-24"
    And the user clicks the "Add Release Note" button
    Then zero inline error messages are visible anywhere on the page

  @TC-005 @REQ-001 @REQ-001-FR-3 @AC-4 @story_001 @positive @medium @regression @functional
  Scenario: TC-005 A submitted release entry remains visible in the list after a full page reload
    When the user enters "Analytics Engine" in the "product" field
    And the user enters "v1.2.0" in the "version" field
    And the user enters "Dashboard widgets" in the "title" field
    And the user enters "Added customisable dashboard widgets for analytics views." in the "description" field
    And the user sets the "releaseDate" field to "2026-09-24"
    And the user clicks the "Add Release Note" button
    When the user reloads the page
    Then a release card containing "Analytics Engine" and "v1.2.0" is visible in the release list
