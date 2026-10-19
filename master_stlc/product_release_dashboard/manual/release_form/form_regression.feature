# features/release_form/form_regression.feature
# TC-019 – TC-024 | Regression checks for existing functionality + End-to-End submission flows
# Requirement: REQ-001 — Inline Form Validation for Release Notes Dashboard
# Test Plan:   TP-001

Feature: Release Note Form — Regression and End-to-End Flows

  Background:
    Given the "releaseNotesDashboard.releases" key in localStorage has been cleared
    And the user has opened "product_release_dashboard/index.html" in the browser

  # ---------------------------------------------------------------------------
  # Regression scenarios (TC-019 – TC-022)
  # Verify existing functionality is not broken by the REQ-001 validation changes
  # ---------------------------------------------------------------------------

  @TC-019 @REQ-001 @REQ-001-regression @story_001 @regression @medium @functional @ui
  Scenario: TC-019 Seed release entries are rendered in the release list on page load
    # After localStorage is cleared the app auto-seeds two known entries on first load
    Then the release list displays a card for product "Billing API" version "v1.4.0"
    And the release list displays a card for product "Auth Service" version "v2.0.0"
    And the total number of release cards visible is 2

  @TC-020 @REQ-001 @REQ-001-regression @REQ-001-FR-4 @story_001 @regression @medium @functional @ui
  Scenario: TC-020 The product filter works correctly while inline validation errors are visible on the form
    # Trigger validation errors first
    When the user clicks the "Add Release Note" button without entering any field values
    And inline error messages are visible on the form
    # Apply the product filter — form errors must not interfere with filter behaviour
    When the user enters "Billing" in the "product-filter" field
    Then the release list shows only cards for products whose name contains "Billing"
    And the inline error messages on the form remain visible and are unchanged

  @TC-021 @REQ-001 @REQ-001-regression @story_001 @regression @medium @functional @ui
  Scenario: TC-021 The product filter returns the newly added release when filtered by its product name
    # Submit a valid release
    When the user enters "Inventory Service" in the "product" field
    And the user enters "v1.0.0" in the "version" field
    And the user enters "Warehouse sync" in the "title" field
    And the user enters "Syncs warehouse inventory in real time." in the "description" field
    And the user sets the "releaseDate" field to "2026-09-24"
    And the user clicks the "Add Release Note" button
    # Filter by the newly added product — should return exactly 1 card
    When the user enters "Inventory Service" in the "product-filter" field
    Then the release list shows exactly 1 card
    And that card contains the text "Inventory Service"
    # Filter by a value that matches no product — should return no cards
    When the user enters "NonExistentProduct" in the "product-filter" field
    Then the release list shows the empty-state message and no release cards

  @TC-022 @REQ-001 @REQ-001-regression @REQ-001-FR-3 @story_001 @regression @medium @functional @ui
  Scenario: TC-022 Existing release entries are not removed or altered after an invalid form submission
    # Baseline: two seed entries are visible after the Background step runs
    Given the release list shows 2 existing release cards
    And a card for product "Billing API" version "v1.4.0" is visible
    And a card for product "Auth Service" version "v2.0.0" is visible
    # Trigger a failed submission (all fields empty)
    When the user clicks the "Add Release Note" button without entering any field values
    # The two existing seed cards must be unchanged
    Then the release list still shows exactly 2 release cards
    And the card for product "Billing API" version "v1.4.0" is still visible
    And the card for product "Auth Service" version "v2.0.0" is still visible

  # ---------------------------------------------------------------------------
  # End-to-End scenarios (TC-023 – TC-024)
  # Full error → correct → valid-submit flow covering AC-1 through AC-4
  # ---------------------------------------------------------------------------

  @TC-023 @REQ-001 @REQ-001-FR-1 @REQ-001-FR-2 @REQ-001-FR-3 @REQ-001-FR-4 @AC-1 @AC-2 @AC-3 @AC-4 @story_001 @e2e @critical @smoke @ui @functional
  Scenario: TC-023 Full flow — single field triggers an error, is corrected reactively, then a valid submission succeeds
    # Phase 1 — fill all fields except product; click Submit to trigger the product error
    When the user enters "v1.0.0" in the "version" field
    And the user enters "Initial Release" in the "title" field
    And the user enters "First stable release." in the "description" field
    And the user sets the "releaseDate" field to "2026-09-24"
    And the user clicks the "Add Release Note" button
    # Phase 2 — error is visible on product; no release was created
    Then an inline error message is visible adjacent to the "product" field
    And no new release entry is added to the "releaseNotesDashboard.releases" localStorage key
    # Phase 3 — correct the product field; error must clear without a second submit
    When the user enters "Billing API" in the "product" field
    Then the inline error message adjacent to the "product" field is no longer visible
    # Phase 4 — all fields are now valid; submit and verify full success
    When the user clicks the "Add Release Note" button
    Then a release card containing "Billing API" and "v1.0.0" is visible in the release list
    And the "releaseNotesDashboard.releases" localStorage key contains 3 release entries
    And no inline error messages are visible on the form
    And the "product" field value is empty
    And the "version" field value is empty
    And the "title" field value is empty
    And the "description" field value is empty
    And the "releaseDate" field value is empty

  @TC-024 @REQ-001 @REQ-001-FR-1 @REQ-001-FR-2 @REQ-001-FR-3 @REQ-001-FR-4 @AC-1 @AC-2 @AC-3 @AC-4 @story_001 @e2e @critical @smoke @ui @functional
  Scenario: TC-024 Full flow — all five errors triggered, each corrected individually, then a valid submission succeeds
    # Phase 1 — submit with all five fields empty
    When the user clicks the "Add Release Note" button without entering any field values
    # Phase 2 — verify five simultaneous inline errors and no release created
    Then an inline error message is visible adjacent to the "product" field
    And an inline error message is visible adjacent to the "version" field
    And an inline error message is visible adjacent to the "title" field
    And an inline error message is visible adjacent to the "description" field
    And an inline error message is visible adjacent to the "releaseDate" field
    And no new release entry is added to the "releaseNotesDashboard.releases" localStorage key
    # Phase 3 — fill each field one by one; verify each error clears reactively on input
    When the user enters "Payments Gateway" in the "product" field
    Then the inline error message adjacent to the "product" field is no longer visible
    When the user enters "v2.0.0" in the "version" field
    Then the inline error message adjacent to the "version" field is no longer visible
    When the user enters "Payment integration" in the "title" field
    Then the inline error message adjacent to the "title" field is no longer visible
    When the user enters "Added Stripe integration to the payments module." in the "description" field
    Then the inline error message adjacent to the "description" field is no longer visible
    When the user sets the "releaseDate" field to "2026-09-24"
    Then the inline error message adjacent to the "releaseDate" field is no longer visible
    # Phase 4 — all fields now valid; submit and verify release is created, persisted, form reset
    When the user clicks the "Add Release Note" button
    Then a release card containing "Payments Gateway" and "v2.0.0" is visible in the release list
    And the "releaseNotesDashboard.releases" localStorage key contains 3 release entries
    And no inline error messages are visible on the form
    And the "product" field value is empty
    And the "version" field value is empty
    And the "title" field value is empty
    And the "description" field value is empty
    And the "releaseDate" field value is empty
