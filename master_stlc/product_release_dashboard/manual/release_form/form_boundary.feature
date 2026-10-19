# features/release_form/form_boundary.feature
# TC-013 – TC-018 | Boundary value and edge case validation
# Requirement: REQ-001 — Inline Form Validation for Release Notes Dashboard
# Test Plan:   TP-001

Feature: Release Note Form — Boundary and Edge Case Validation

  Background:
    Given the "releaseNotesDashboard.releases" key in localStorage has been cleared
    And the user has opened "product_release_dashboard/index.html" in the browser

  @TC-013 @REQ-001 @REQ-001-FR-1 @REQ-001-FR-2 @REQ-001-FR-3 @AC-1 @AC-2 @story_001 @boundary @high @regression @ui @functional
  Scenario: TC-013 A product field containing only whitespace characters is treated as invalid
    # Test data: product = "   " (three space characters); all other fields contain valid data
    When the user enters "   " in the "product" field
    And the user enters "v1.0.0" in the "version" field
    And the user enters "Initial Release" in the "title" field
    And the user enters "First stable release." in the "description" field
    And the user sets the "releaseDate" field to "2026-09-24"
    And the user clicks the "Add Release Note" button
    Then an inline error message is visible adjacent to the "product" field
    And no new release entry is added to the "releaseNotesDashboard.releases" localStorage key

  # Note: blank cells in the Examples table represent a value of "   " (three space characters).
  # The date field (type="date") is excluded because it is an HTML5 date picker;
  # free-text whitespace entry is not applicable to that field type.
  @TC-014 @REQ-001 @REQ-001-FR-2 @REQ-001-FR-3 @AC-1 @AC-2 @story_001 @boundary @high @regression @ui @functional
  Scenario Outline: TC-014 A whitespace-only value in any required text field is treated as invalid on submission
    When the user enters "<product_val>" in the "product" field
    And the user enters "<version_val>" in the "version" field
    And the user enters "<title_val>" in the "title" field
    And the user enters "<description_val>" in the "description" field
    And the user sets the "releaseDate" field to "2026-09-24"
    And the user clicks the "Add Release Note" button
    Then an inline error message is visible adjacent to the "<invalid_field>" field
    And no new release entry is added to the "releaseNotesDashboard.releases" localStorage key

    Examples: whitespace-only in individual required text fields
      | invalid_field | product_val | version_val | title_val       | description_val       |
      | version       | Billing API |             | Initial Release | First stable release. |
      | title         | Billing API | v1.0.0      |                 | First stable release. |
      | description   | Billing API | v1.0.0      | Initial Release |                       |

  @TC-015 @REQ-001 @REQ-001-FR-4 @AC-3 @story_001 @boundary @high @regression @ui @functional
  Scenario: TC-015 Correcting one errored field clears only that field's error while other errors remain visible
    # Submit with all fields empty to trigger five simultaneous errors
    When the user clicks the "Add Release Note" button without entering any field values
    Then an inline error message is visible adjacent to the "product" field
    And an inline error message is visible adjacent to the "version" field
    # Correct only the product field; no re-submit
    When the user enters "Billing API" in the "product" field
    Then the inline error message adjacent to the "product" field is no longer visible
    And an inline error message is still visible adjacent to the "version" field
    And an inline error message is still visible adjacent to the "title" field
    And an inline error message is still visible adjacent to the "description" field
    And an inline error message is still visible adjacent to the "releaseDate" field

  @TC-016 @REQ-001 @REQ-001-FR-4 @AC-3 @story_001 @boundary @medium @regression @ui @functional
  Scenario: TC-016 An error reappears for a field that was corrected and then cleared again
    # Submit with all fields empty to trigger errors
    When the user clicks the "Add Release Note" button without entering any field values
    Then an inline error message is visible adjacent to the "product" field
    # Correct the product field — error should clear reactively
    When the user enters "Billing API" in the "product" field
    Then the inline error message adjacent to the "product" field is no longer visible
    # Clear the product field again — error must reappear immediately without re-submit
    When the user clears all text from the "product" field
    Then an inline error message is visible adjacent to the "product" field

  @TC-017 @REQ-001 @REQ-001-FR-1 @AC-4 @story_001 @boundary @medium @regression @functional
  Scenario: TC-017 A single character in each required text field is accepted as a valid submission
    # Test data: minimum valid input — one character per text field; one valid date
    When the user enters "A" in the "product" field
    And the user enters "1" in the "version" field
    And the user enters "B" in the "title" field
    And the user enters "C" in the "description" field
    And the user sets the "releaseDate" field to "2026-09-24"
    And the user clicks the "Add Release Note" button
    Then a release card containing "A" and "1" is visible in the release list
    And no inline error messages are visible on the form
    And the "releaseNotesDashboard.releases" localStorage key contains 3 release entries

  @TC-018 @REQ-001 @REQ-001-FR-4 @AC-3 @story_001 @boundary @high @regression @ui @functional
  Scenario: TC-018 Typing a single character into an errored field clears that field's error immediately without re-submitting the form
    # Submit with all fields empty to trigger the product field error
    When the user clicks the "Add Release Note" button without entering any field values
    And an inline error message is visible adjacent to the "product" field
    # Type exactly one character — error must vanish reactively; no second submit is performed
    When the user types the single character "B" into the "product" field
    Then the inline error message adjacent to the "product" field is no longer visible
    And the "Add Release Note" button has not been clicked a second time
