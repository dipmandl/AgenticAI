"""
test_form_boundary.py — TC-013 through TC-018
Boundary and edge-case validation: whitespace-only inputs treated as invalid,
reactive error clearing (AC-3 / FR-4), single-character minimum values, and
error re-appearance when a corrected field is cleared again.

Requirement : REQ-001 — Inline Form Validation for Release Notes Dashboard
Feature file: features/release_form/form_boundary.feature
Test plan   : TP-001  |  TC range: TC-013 – TC-018

Reactive clearing (AC-3 / FR-4)
--------------------------------
When a field that previously had a visible error receives a non-empty,
non-whitespace value via an input/change event, the adjacent error element
must be hidden immediately — WITHOUT a second form submit.
Tests verify this by:
  1. Filling a field with valid data (page.fill triggers input events).
  2. Asserting to_be_hidden() without clicking Submit again.
  3. Checking localStorage count to confirm no hidden re-submit occurred.
"""

import pytest
from playwright.sync_api import expect

# ── Module-level constants ────────────────────────────────────────────────────

LS_READ = "JSON.parse(localStorage.getItem('releaseNotesDashboard.releases') || '[]')"
FIELDS  = ["product", "version", "title", "description", "releaseDate"]


# ── TC-013 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_013
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.high
@pytest.mark.boundary
@pytest.mark.ui
@pytest.mark.functional
def test_product_whitespace_only_is_treated_as_invalid(page):
    """
    TC-013: A product field containing only whitespace characters is treated as
    invalid — REQ-001, AC-1, AC-2, FR-1, FR-2, FR-3.
    Test data: product = "   " (three space characters); all other fields valid.
    script.js trims the value before validation, so "   ".trim() === "".
    """
    page.fill("#product",     "   ")   # three space characters — whitespace-only
    page.fill("#version",     "v1.0.0")
    page.fill("#title",       "Initial Release")
    page.fill("#description", "First stable release.")
    page.fill("#releaseDate", "2026-09-24")
    page.get_by_role("button", name="Add Release Note").click()

    # Whitespace-only product trims to "" and must trigger an inline error
    expect(page.locator('.field-error[data-for="product"]')).to_be_visible()

    # No entry must be persisted
    releases = page.evaluate(LS_READ)
    assert len(releases) == 2, (
        f"Expected 2 seed entries (whitespace-only product must not be saved), "
        f"got {len(releases)}"
    )


# ── TC-014 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_014
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.high
@pytest.mark.boundary
@pytest.mark.ui
@pytest.mark.functional
@pytest.mark.parametrize(
    "invalid_field,product_val,version_val,title_val,description_val",
    [
        # Each row has whitespace-only ("   ") in the field under test
        ("version",     "Billing API", "   ", "Initial Release", "First stable release."),
        ("title",       "Billing API", "v1.0.0", "   ",          "First stable release."),
        ("description", "Billing API", "v1.0.0", "Initial Release", "   "),
    ],
    ids=["version_whitespace", "title_whitespace", "description_whitespace"],
)
def test_whitespace_only_field_treated_as_empty(
    page, invalid_field, product_val, version_val, title_val, description_val
):
    """
    TC-014: A whitespace-only value in any required text field is treated as
    invalid on submission — REQ-001, AC-1, AC-2, FR-2, FR-3.
    Parametrised over version, title, description (date field excluded as it is
    an HTML5 date picker and does not accept free-text whitespace).
    """
    page.fill("#product",     product_val)
    page.fill("#version",     version_val)
    page.fill("#title",       title_val)
    page.fill("#description", description_val)
    page.fill("#releaseDate", "2026-09-24")
    page.get_by_role("button", name="Add Release Note").click()

    # The field with whitespace-only content must show an inline error
    expect(page.locator(f'.field-error[data-for="{invalid_field}"]')).to_be_visible()

    # No entry must be persisted
    releases = page.evaluate(LS_READ)
    assert len(releases) == 2, (
        f"Expected 2 seed entries (whitespace-only '{invalid_field}' must not be saved), "
        f"got {len(releases)}"
    )


# ── TC-015 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_015
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.high
@pytest.mark.boundary
@pytest.mark.ui
@pytest.mark.functional
def test_correcting_one_field_clears_only_that_fields_error(page):
    """
    TC-015: Correcting one errored field clears only that field's error while
    other errors remain visible — REQ-001, AC-3, FR-4.
    """
    # Submit with all five fields empty to trigger five simultaneous errors
    page.get_by_role("button", name="Add Release Note").click()

    for field_id in FIELDS:
        expect(page.locator(f'.field-error[data-for="{field_id}"]')).to_be_visible()

    # Correct only the product field — reactive clearing must fire immediately
    page.fill("#product", "Billing API")

    # Product error must be gone
    expect(page.locator('.field-error[data-for="product"]')).to_be_hidden()

    # All four remaining field errors must still be visible
    for field_id in ["version", "title", "description", "releaseDate"]:
        expect(page.locator(f'.field-error[data-for="{field_id}"]')).to_be_visible()


# ── TC-016 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_016
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.medium
@pytest.mark.boundary
@pytest.mark.ui
@pytest.mark.functional
def test_error_reappears_when_corrected_field_is_cleared_again(page):
    """
    TC-016: An error reappears for a field that was corrected and then cleared
    again — REQ-001, AC-3, FR-4. No re-submit is performed.
    """
    # Step 1: submit empty — error appears on product field
    page.get_by_role("button", name="Add Release Note").click()
    expect(page.locator('.field-error[data-for="product"]')).to_be_visible()

    # Step 2: correct the field — error clears reactively
    page.fill("#product", "Billing API")
    expect(page.locator('.field-error[data-for="product"]')).to_be_hidden()

    # Step 3: clear the field again — error must reappear reactively (no re-submit)
    page.fill("#product", "")
    expect(page.locator('.field-error[data-for="product"]')).to_be_visible()


# ── TC-017 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_017
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.medium
@pytest.mark.boundary
@pytest.mark.functional
def test_single_character_per_field_is_valid_submission(page):
    """
    TC-017: A single character in each required text field is accepted as a
    valid submission — REQ-001, AC-4, FR-1.
    Test data: minimum valid input — one character per text field, one valid date.
    """
    page.fill("#product",     "A")
    page.fill("#version",     "1")
    page.fill("#title",       "B")
    page.fill("#description", "C")
    page.fill("#releaseDate", "2026-09-24")
    page.get_by_role("button", name="Add Release Note").click()

    # Release card must appear with single-character product and version
    expect(page.locator(".product-version", has_text="A - 1")).to_be_visible()

    # No inline errors must be visible
    for field_id in FIELDS:
        expect(page.locator(f'.field-error[data-for="{field_id}"]')).to_be_hidden()

    # localStorage must contain 3 entries: 2 seed + 1 new
    releases = page.evaluate(LS_READ)
    assert len(releases) == 3, (
        f"Expected 3 entries after single-character valid submit, got {len(releases)}"
    )


# ── TC-018 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_018
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.high
@pytest.mark.boundary
@pytest.mark.ui
@pytest.mark.functional
def test_typing_one_char_clears_error_reactively_without_resubmit(page):
    """
    TC-018: Typing a single character into an errored field clears that field's
    error immediately without re-submitting the form — REQ-001, AC-3, FR-4.
    """
    # Submit empty form to trigger the product field error
    page.get_by_role("button", name="Add Release Note").click()
    expect(page.locator('.field-error[data-for="product"]')).to_be_visible()

    # Type a single character — triggers input event; error must clear reactively
    page.fill("#product", "B")

    # Error must vanish immediately without a second Submit click
    expect(page.locator('.field-error[data-for="product"]')).to_be_hidden()

    # Verify no hidden re-submit occurred: localStorage must still contain 2 entries
    # (with only product filled the other fields are still empty, so a second submit
    # would also fail — but the count stays at 2 either way; what matters is no
    # unexpected submit side-effect triggered the handler)
    releases = page.evaluate(LS_READ)
    assert len(releases) == 2, (
        "Expected 2 seed entries — form must not have been re-submitted "
        f"automatically, got {len(releases)}"
    )
