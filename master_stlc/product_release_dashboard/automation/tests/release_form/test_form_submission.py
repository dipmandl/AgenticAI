"""
test_form_submission.py — TC-001 through TC-005
Happy-path valid submission scenarios: all fields populated → release card
created, persisted to localStorage, form reset, and entry survives a reload.

Requirement : REQ-001 — Inline Form Validation for Release Notes Dashboard
Feature file: features/release_form/form_submission.feature
Test plan   : TP-001  |  TC range: TC-001 – TC-005

Error-element contract (required by REQ-001 implementation)
-----------------------------------------------------------
Each required field must have an adjacent error element:
    <span class="field-error" data-for="<field-id>">...</span>
The element must be hidden (or absent) when the field is valid.

Card text format
----------------
script.js renders: `${release.product} - ${release.version}`
Example: "Billing API - v1.0.0"
"""

import pytest
from playwright.sync_api import expect

# ── Module-level constants ────────────────────────────────────────────────────

LS_READ = "JSON.parse(localStorage.getItem('releaseNotesDashboard.releases') || '[]')"
FIELDS  = ["product", "version", "title", "description", "releaseDate"]


# ── TC-001 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_001
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.functional
def test_valid_submission_creates_release_card(page):
    """
    TC-001: Valid submission with all fields populated creates a release card
    in the release list — REQ-001, AC-4, FR-1, FR-3.
    """
    page.fill("#product",     "Billing API")
    page.fill("#version",     "v1.0.0")
    page.fill("#title",       "Initial Release")
    page.fill("#description", "First stable release of the product.")
    page.fill("#releaseDate", "2026-09-24")
    page.get_by_role("button", name="Add Release Note").click()

    # Release card must appear with correct product-version text
    expect(
        page.locator(".product-version", has_text="Billing API - v1.0.0")
    ).to_be_visible()

    # No inline error messages must be visible on any field
    for field_id in FIELDS:
        expect(page.locator(f'.field-error[data-for="{field_id}"]')).to_be_hidden()


# ── TC-002 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_002
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.high
@pytest.mark.positive
@pytest.mark.functional
def test_valid_submission_persists_entry_to_localstorage(page):
    """
    TC-002: Valid submission persists the new release entry to localStorage —
    REQ-001, AC-4, FR-3.
    """
    page.fill("#product",     "Payments Gateway")
    page.fill("#version",     "v2.0.0")
    page.fill("#title",       "Payment integration")
    page.fill("#description", "Added Stripe integration to the payments module.")
    page.fill("#releaseDate", "2026-09-24")
    page.get_by_role("button", name="Add Release Note").click()

    # Wait for the card to confirm the JS submit handler ran
    expect(
        page.locator(".product-version", has_text="Payments Gateway - v2.0.0")
    ).to_be_visible()

    # localStorage must now contain 3 entries: 2 seed + 1 new
    releases = page.evaluate(LS_READ)
    assert len(releases) == 3, (
        f"Expected 3 entries in localStorage (2 seed + 1 new), got {len(releases)}"
    )

    # releases.unshift() places the newest entry at index 0
    assert releases[0]["product"] == "Payments Gateway", (
        f"Most recent product should be 'Payments Gateway', got '{releases[0]['product']}'"
    )
    assert releases[0]["version"] == "v2.0.0", (
        f"Most recent version should be 'v2.0.0', got '{releases[0]['version']}'"
    )


# ── TC-003 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_003
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.medium
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.functional
def test_all_form_fields_empty_after_valid_submission(page):
    """
    TC-003: All form fields are empty after a valid submission —
    REQ-001 (derived; verifies form.reset() behaviour).
    """
    page.fill("#product",     "Auth Service")
    page.fill("#version",     "v1.1.0")
    page.fill("#title",       "SSO Support")
    page.fill("#description", "Added SAML SSO support for enterprise customers.")
    page.fill("#releaseDate", "2026-09-24")
    page.get_by_role("button", name="Add Release Note").click()

    # Wait for card to confirm submission completed
    expect(
        page.locator(".product-version", has_text="Auth Service - v1.1.0")
    ).to_be_visible()

    # releaseForm.reset() must clear every required field
    for field_id in FIELDS:
        expect(page.locator(f"#{field_id}")).to_have_value("")


# ── TC-004 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_004
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.smoke
@pytest.mark.high
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.functional
def test_zero_errors_visible_after_valid_submission(page):
    """
    TC-004: Zero inline error messages are visible anywhere on the page after
    a fully valid submission — REQ-001, AC-1, AC-4, FR-1.
    """
    page.fill("#product",     "Notification Service")
    page.fill("#version",     "v3.0.0")
    page.fill("#title",       "Email alerts")
    page.fill("#description", "Introduced configurable email alert thresholds.")
    page.fill("#releaseDate", "2026-09-24")
    page.get_by_role("button", name="Add Release Note").click()

    expect(
        page.locator(".product-version", has_text="Notification Service - v3.0.0")
    ).to_be_visible()

    # Every field's error element must be hidden after a successful submit
    for field_id in FIELDS:
        expect(page.locator(f'.field-error[data-for="{field_id}"]')).to_be_hidden()


# ── TC-005 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_005
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.medium
@pytest.mark.positive
@pytest.mark.functional
def test_submitted_release_visible_after_page_reload(page):
    """
    TC-005: A submitted release entry remains visible in the list after a full
    page reload — REQ-001, AC-4, FR-3 (localStorage persistence).
    """
    page.fill("#product",     "Analytics Engine")
    page.fill("#version",     "v1.2.0")
    page.fill("#title",       "Dashboard widgets")
    page.fill("#description", "Added customisable dashboard widgets for analytics views.")
    page.fill("#releaseDate", "2026-09-24")
    page.get_by_role("button", name="Add Release Note").click()

    expect(
        page.locator(".product-version", has_text="Analytics Engine - v1.2.0")
    ).to_be_visible()

    # Full page reload — entry must be reloaded from localStorage and re-rendered
    page.reload()
    page.wait_for_load_state("networkidle")

    expect(
        page.locator(".product-version", has_text="Analytics Engine - v1.2.0")
    ).to_be_visible()
