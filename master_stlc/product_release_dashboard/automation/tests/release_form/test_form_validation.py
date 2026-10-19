"""
test_form_validation.py — TC-006 through TC-012
Inline error / negative scenarios: validation errors appear for each required
field when that field is empty at submission time, and invalid submissions
never write to localStorage.

Requirement : REQ-001 — Inline Form Validation for Release Notes Dashboard
Feature file: features/release_form/form_validation.feature
Test plan   : TP-001  |  TC range: TC-006 – TC-012

Error-element contract (required by REQ-001 implementation)
-----------------------------------------------------------
Each required field must have an adjacent error element:
    <span class="field-error" data-for="<field-id>">...</span>
The element must be visible when the field is invalid and hidden when valid.
"""

import pytest
from playwright.sync_api import expect

# ── Module-level constants ────────────────────────────────────────────────────

LS_READ = "JSON.parse(localStorage.getItem('releaseNotesDashboard.releases') || '[]')"
FIELDS  = ["product", "version", "title", "description", "releaseDate"]


# ── Private helper ────────────────────────────────────────────────────────────

def _assert_single_field_error(page, error_field: str) -> None:
    """
    Assert that exactly one field has a visible inline error.

    - The field named ``error_field`` must have a visible .field-error element.
    - All other required fields must have a hidden .field-error element.
    """
    for field_id in FIELDS:
        locator = page.locator(f'.field-error[data-for="{field_id}"]')
        if field_id == error_field:
            expect(locator).to_be_visible()
        else:
            expect(locator).to_be_hidden()


# ── TC-006 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_006
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.negative
@pytest.mark.ui
@pytest.mark.functional
def test_submit_all_empty_fields_shows_five_simultaneous_errors(page):
    """
    TC-006: Submitting with all five required fields empty shows five
    simultaneous inline errors — REQ-001, AC-1, AC-2, FR-1, FR-2, FR-3.
    """
    page.get_by_role("button", name="Add Release Note").click()

    # All five field errors must be visible simultaneously
    for field_id in FIELDS:
        expect(page.locator(f'.field-error[data-for="{field_id}"]')).to_be_visible()

    # No new entry must be written to localStorage
    releases = page.evaluate(LS_READ)
    assert len(releases) == 2, (
        f"Expected 2 seed entries (invalid submit must not write to localStorage), "
        f"got {len(releases)}"
    )


# ── TC-007 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_007
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.smoke
@pytest.mark.high
@pytest.mark.negative
@pytest.mark.ui
@pytest.mark.functional
def test_submit_empty_product_shows_inline_error(page):
    """
    TC-007: Submitting with only the product field empty shows an error for
    product only — REQ-001, AC-1, AC-2, FR-2, FR-3.
    """
    # Fill all fields except product
    page.fill("#version",     "v1.0.0")
    page.fill("#title",       "Initial Release")
    page.fill("#description", "First stable release.")
    page.fill("#releaseDate", "2026-09-24")
    page.get_by_role("button", name="Add Release Note").click()

    _assert_single_field_error(page, "product")

    releases = page.evaluate(LS_READ)
    assert len(releases) == 2, (
        f"Expected 2 seed entries (missing product must not write to localStorage), "
        f"got {len(releases)}"
    )


# ── TC-008 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_008
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.high
@pytest.mark.negative
@pytest.mark.ui
@pytest.mark.functional
def test_submit_empty_version_shows_inline_error(page):
    """
    TC-008: Submitting with only the version field empty shows an error for
    version only — REQ-001, AC-1, AC-2, FR-2, FR-3.
    """
    page.fill("#product",     "Billing API")
    # version intentionally left empty
    page.fill("#title",       "Initial Release")
    page.fill("#description", "First stable release.")
    page.fill("#releaseDate", "2026-09-24")
    page.get_by_role("button", name="Add Release Note").click()

    _assert_single_field_error(page, "version")

    releases = page.evaluate(LS_READ)
    assert len(releases) == 2, (
        f"Expected 2 seed entries (missing version must not write to localStorage), "
        f"got {len(releases)}"
    )


# ── TC-009 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_009
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.high
@pytest.mark.negative
@pytest.mark.ui
@pytest.mark.functional
def test_submit_empty_title_shows_inline_error(page):
    """
    TC-009: Submitting with only the title field empty shows an error for
    title only — REQ-001, AC-1, AC-2, FR-2, FR-3.
    """
    page.fill("#product",     "Billing API")
    page.fill("#version",     "v1.0.0")
    # title intentionally left empty
    page.fill("#description", "First stable release.")
    page.fill("#releaseDate", "2026-09-24")
    page.get_by_role("button", name="Add Release Note").click()

    _assert_single_field_error(page, "title")

    releases = page.evaluate(LS_READ)
    assert len(releases) == 2, (
        f"Expected 2 seed entries (missing title must not write to localStorage), "
        f"got {len(releases)}"
    )


# ── TC-010 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_010
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.high
@pytest.mark.negative
@pytest.mark.ui
@pytest.mark.functional
def test_submit_empty_description_shows_inline_error(page):
    """
    TC-010: Submitting with only the description field empty shows an error for
    description only — REQ-001, AC-1, AC-2, FR-2, FR-3.
    """
    page.fill("#product",  "Billing API")
    page.fill("#version",  "v1.0.0")
    page.fill("#title",    "Initial Release")
    # description intentionally left empty
    page.fill("#releaseDate", "2026-09-24")
    page.get_by_role("button", name="Add Release Note").click()

    _assert_single_field_error(page, "description")

    releases = page.evaluate(LS_READ)
    assert len(releases) == 2, (
        f"Expected 2 seed entries (missing description must not write to localStorage), "
        f"got {len(releases)}"
    )


# ── TC-011 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_011
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.high
@pytest.mark.negative
@pytest.mark.ui
@pytest.mark.functional
def test_submit_empty_release_date_shows_inline_error(page):
    """
    TC-011: Submitting with only the releaseDate field empty shows an error for
    date only — REQ-001, AC-1, AC-2, FR-2, FR-3.
    """
    page.fill("#product",     "Billing API")
    page.fill("#version",     "v1.0.0")
    page.fill("#title",       "Initial Release")
    page.fill("#description", "First stable release.")
    # releaseDate intentionally left empty (default state after fixture reload)
    page.get_by_role("button", name="Add Release Note").click()

    _assert_single_field_error(page, "releaseDate")

    releases = page.evaluate(LS_READ)
    assert len(releases) == 2, (
        f"Expected 2 seed entries (missing releaseDate must not write to localStorage), "
        f"got {len(releases)}"
    )


# ── TC-012 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_012
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.negative
@pytest.mark.functional
def test_invalid_submit_does_not_write_to_localstorage(page):
    """
    TC-012: An invalid form submission does not write any new entry to
    localStorage — REQ-001, AC-2, FR-3.
    Baseline: conftest fixture guarantees exactly 2 seed entries.
    """
    page.get_by_role("button", name="Add Release Note").click()

    # Wait for at least the product error to confirm the submit handler ran
    expect(page.locator('.field-error[data-for="product"]')).to_be_visible()

    # localStorage count must still be exactly 2
    releases = page.evaluate(LS_READ)
    assert len(releases) == 2, (
        f"Expected exactly 2 entries (seed data only — invalid submit must not persist), "
        f"got {len(releases)}"
    )
