# features/release_form/form_validation.feature
# TC-006 – TC-012 | Inline error / negative / empty field scenarios
# Requirement: REQ-001 — Inline Form Validation for Release Notes Dashboard
# Test Plan:   TP-001

Feature: Release Note Form — Inline Validation Errors

  Background:
    Given the "releaseNotesDashboard.releases" key in localStorage has been cleared
    And the user has opened "product_release_dashboard/index.html" in the browser

  @TC-006 @REQ-001 @REQ-001-FR-1 @REQ-001-FR-2 @REQ-001-FR-3 @AC-1 @AC-2 @story_001 @negative @critical @smoke @ui @functional
  Scenario: TC-006 Submitting with all five required fields empty shows five simultaneous inline errors
    When the user clicks the "Add Release Note" button without entering any field values
    Then an inline error message is visible adjacent to the "product" field
    And an inline error message is visible adjacent to the "version" field
    And an inline error message is visible adjacent to the "title" field
    And an inline error message is visible adjacent to the "description" field
    And an inline error message is visible adjacent to the "releaseDate" field
    And no new release entry is added to the "releaseNotesDashboard.releases" localStorage key

  @TC-007 @REQ-001 @REQ-001-FR-2 @REQ-001-FR-3 @AC-1 @AC-2 @story_001 @negative @high @smoke @ui @functional
  Scenario: TC-007 Submitting with only the product field empty shows an error for product only
    When the user enters "v1.0.0" in the "version" field
    And the user enters "Initial Release" in the "title" field
    And the user enters "First stable release." in the "description" field
    And the user sets the "releaseDate" field to "2026-09-24"
    And the user clicks the "Add Release Note" button
    Then an inline error message is visible adjacent to the "product" field
    And no inline error message is visible adjacent to the "version" field
    And no inline error message is visible adjacent to the "title" field
    And no inline error message is visible adjacent to the "description" field
    And no inline error message is visible adjacent to the "releaseDate" field
    And no new release entry is added to the "releaseNotesDashboard.releases" localStorage key

  @TC-008 @REQ-001 @REQ-001-FR-2 @REQ-001-FR-3 @AC-1 @AC-2 @story_001 @negative @high @regression @ui @functional
  Scenario: TC-008 Submitting with only the version field empty shows an error for version only
    When the user enters "Billing API" in the "product" field
    And the user enters "Initial Release" in the "title" field
    And the user enters "First stable release." in the "description" field
    And the user sets the "releaseDate" field to "2026-09-24"
    And the user clicks the "Add Release Note" button
    Then an inline error message is visible adjacent to the "version" field
    And no inline error message is visible adjacent to the "product" field
    And no inline error message is visible adjacent to the "title" field
    And no inline error message is visible adjacent to the "description" field
    And no inline error message is visible adjacent to the "releaseDate" field
    And no new release entry is added to the "releaseNotesDashboard.releases" localStorage key

  @TC-009 @REQ-001 @REQ-001-FR-2 @REQ-001-FR-3 @AC-1 @AC-2 @story_001 @negative @high @regression @ui @functional
  Scenario: TC-009 Submitting with only the title field empty shows an error for title only
    When the user enters "Billing API" in the "product" field
    And the user enters "v1.0.0" in the "version" field
    And the user enters "First stable release." in the "description" field
    And the user sets the "releaseDate" field to "2026-09-24"
    And the user clicks the "Add Release Note" button
    Then an inline error message is visible adjacent to the "title" field
    And no inline error message is visible adjacent to the "product" field
    And no inline error message is visible adjacent to the "version" field
    And no inline error message is visible adjacent to the "description" field
    And no inline error message is visible adjacent to the "releaseDate" field
    And no new release entry is added to the "releaseNotesDashboard.releases" localStorage key

  @TC-010 @REQ-001 @REQ-001-FR-2 @REQ-001-FR-3 @AC-1 @AC-2 @story_001 @negative @high @regression @ui @functional
  Scenario: TC-010 Submitting with only the description field empty shows an error for description only
    When the user enters "Billing API" in the "product" field
    And the user enters "v1.0.0" in the "version" field
    And the user enters "Initial Release" in the "title" field
    And the user sets the "releaseDate" field to "2026-09-24"
    And the user clicks the "Add Release Note" button
    Then an inline error message is visible adjacent to the "description" field
    And no inline error message is visible adjacent to the "product" field
    And no inline error message is visible adjacent to the "version" field
    And no inline error message is visible adjacent to the "title" field
    And no inline error message is visible adjacent to the "releaseDate" field
    And no new release entry is added to the "releaseNotesDashboard.releases" localStorage key

  @TC-011 @REQ-001 @REQ-001-FR-2 @REQ-001-FR-3 @AC-1 @AC-2 @story_001 @negative @high @regression @ui @functional
  Scenario: TC-011 Submitting with only the releaseDate field empty shows an error for date only
    When the user enters "Billing API" in the "product" field
    And the user enters "v1.0.0" in the "version" field
    And the user enters "Initial Release" in the "title" field
    And the user enters "First stable release." in the "description" field
    And the user clicks the "Add Release Note" button without setting the "releaseDate" field
    Then an inline error message is visible adjacent to the "releaseDate" field
    And no inline error message is visible adjacent to the "product" field
    And no inline error message is visible adjacent to the "version" field
    And no inline error message is visible adjacent to the "title" field
    And no inline error message is visible adjacent to the "description" field
    And no new release entry is added to the "releaseNotesDashboard.releases" localStorage key

  @TC-012 @REQ-001 @REQ-001-FR-3 @AC-2 @story_001 @negative @critical @smoke @functional
  Scenario: TC-012 An invalid form submission does not write any new entry to localStorage
    # Baseline: Background clears localStorage; app seeds 2 entries on page load
    When the user clicks the "Add Release Note" button without entering any field values
    Then the "releaseNotesDashboard.releases" localStorage key still contains exactly 2 entries
