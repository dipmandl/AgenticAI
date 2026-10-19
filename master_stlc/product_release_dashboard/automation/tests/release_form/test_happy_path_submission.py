"""
test_happy_path_submission.py — TC-001 through TC-006
Happy-path valid form submission scenarios for REQ-002: release card creation,
localStorage persistence, form reset, error absence, post-reload persistence,
and breaking-change checkbox storage.

Requirement : REQ-002 — Release Form Happy Path Submission Testing
Feature file: product_release_dashboard/manual/features/REQ-002-happy-path-submission.feature
Test plan   : TP-002  |  TC range: TC-001 – TC-006
Jira        : COD-20

Test review issues addressed
----------------------------
ISS-001 : Canonical test data used throughout (not "Initial Release" from plan)
ISS-002 : TC-006 uses distinct Auth Service data with isBreaking: True
ISS-006 : TC-006 asserts ALL 7 localStorage fields (not just isBreaking)

Card text format
----------------
script.js renders: `${release.product} - ${release.version}`
Example:           "Billing API - v1.0.0"

Seed state (managed by conftest.py page fixture)
------------------------------------------------
Each test function starts with exactly 2 seed entries in localStorage:
  [0]  product="Billing API",  version="v1.4.0"
  [1]  product="Auth Service", version="v2.0.0"
After submitting a new release the total grows to 3; new entry at index 0
(script.js uses Array.unshift).
"""

import pytest
from playwright.sync_api import expect

# ── Module-level constants ────────────────────────────────────────────────────

LS_KEY  = "releaseNotesDashboard.releases"
LS_READ = f"JSON.parse(localStorage.getItem('{LS_KEY}') || '[]')"

# Canonical test data — REQ-002 TC-001 through TC-005 (addresses ISS-001)
PRODUCT      = "Billing API"
VERSION      = "v1.0.0"
TITLE        = "Payment Gateway Integration"
DESCRIPTION  = "Integrates Stripe payment gateway for subscription billing"
RELEASE_DATE = "2026-10-01"

# TC-006 distinct test data — breaking-change variant (addresses ISS-002)
TC006_PRODUCT      = "Auth Service"
TC006_VERSION      = "v3.0.0"
TC006_TITLE        = "Breaking Auth Refactor"
TC006_DESCRIPTION  = "Authentication service refactored with breaking API changes"
TC006_RELEASE_DATE = "2026-10-15"


# ── Module-level helper ───────────────────────────────────────────────────────

def _fill_canonical_form(page) -> None:
    """
    Fill all five required form fields with canonical REQ-002 test data.
    The breaking-change checkbox is intentionally left unchecked (TC-001–TC-005
    default state; breaking=False).
    """
    page.fill("#product",     PRODUCT)
    page.fill("#version",     VERSION)
    page.fill("#title",       TITLE)
    page.fill("#description", DESCRIPTION)
    page.fill("#releaseDate", RELEASE_DATE)


# ── TC-001 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_req002_001
@pytest.mark.req_002
@pytest.mark.story_002
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.functional
def test_valid_submission_creates_release_card(page):
    """
    TC-001 (REQ-002, AC-1, FR-001/FR-002): Valid form submission with all five
    required fields populated creates a new release card in #release-list.
    The card's product-version label must read exactly "Billing API - v1.0.0".
    """
    _fill_canonical_form(page)
    page.get_by_role("button", name="Add Release Note").click()

    # New release card must appear inside #release-list with the correct label
    expect(
        page.locator("#release-list .product-version", has_text=f"{PRODUCT} - {VERSION}")
    ).to_be_visible()


# ── TC-002 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_req002_002
@pytest.mark.req_002
@pytest.mark.story_002
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.positive
@pytest.mark.functional
def test_valid_submission_persists_to_localstorage(page):
    """
    TC-002 (REQ-002, AC-2, FR-001/FR-003/FR-004/FR-008): Valid submission
    persists a complete release entry to localStorage.  The array grows from
    2 seed entries to 3; the newest entry is at index 0 (unshift semantics)
    and must carry all 7 required fields with correct values.
    """
    _fill_canonical_form(page)
    page.get_by_role("button", name="Add Release Note").click()

    # Wait for the card to confirm the JS submit handler ran before reading storage
    expect(
        page.locator(".product-version", has_text=f"{PRODUCT} - {VERSION}")
    ).to_be_visible()

    releases = page.evaluate(LS_READ)

    assert len(releases) == 3, (
        f"Expected 3 entries in localStorage (2 seed + 1 new), got {len(releases)}"
    )

    entry = releases[0]  # unshift() places the newest entry at index 0

    assert entry["product"] == PRODUCT, (
        f"Expected product '{PRODUCT}', got '{entry['product']}'"
    )
    assert entry["version"] == VERSION, (
        f"Expected version '{VERSION}', got '{entry['version']}'"
    )
    assert entry["title"] == TITLE, (
        f"Expected title '{TITLE}', got '{entry['title']}'"
    )
    assert entry["description"] == DESCRIPTION, (
        f"Expected description '{DESCRIPTION}', got '{entry['description']}'"
    )
    assert entry["releaseDate"] == RELEASE_DATE, (
        f"Expected releaseDate '{RELEASE_DATE}', got '{entry['releaseDate']}'"
    )
    assert entry["isBreaking"] is False, (
        f"Expected isBreaking False (checkbox unchecked), got '{entry['isBreaking']}'"
    )
    assert entry.get("id"), (
        f"Expected a non-empty id field (UUID), got '{entry.get('id')}'"
    )


# ── TC-003 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_req002_003
@pytest.mark.req_002
@pytest.mark.story_002
@pytest.mark.regression
@pytest.mark.high
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.functional
def test_form_fields_reset_after_submission(page):
    """
    TC-003 (REQ-002, AC-3, FR-001/FR-005): All six form fields — the five
    required text/date inputs (#product, #version, #title, #description,
    #releaseDate) and the breaking-change checkbox (#breaking) — must be reset
    to their empty/unchecked default state immediately after a valid submission.
    """
    _fill_canonical_form(page)
    page.get_by_role("button", name="Add Release Note").click()

    # Wait for the card to confirm that form.reset() was called by the handler
    expect(
        page.locator(".product-version", has_text=f"{PRODUCT} - {VERSION}")
    ).to_be_visible()

    # All text and date inputs must be cleared to empty string
    for field_id in ["product", "version", "title", "description", "releaseDate"]:
        expect(page.locator(f"#{field_id}")).to_have_value("")

    # Breaking-change checkbox must be unchecked
    expect(page.locator("#breaking")).not_to_be_checked()


# ── TC-004 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_req002_004
@pytest.mark.req_002
@pytest.mark.story_002
@pytest.mark.regression
@pytest.mark.high
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.functional
def test_no_errors_visible_after_valid_submission(page):
    """
    TC-004 (REQ-002, AC-4, FR-001/FR-006): Zero .field-error elements are
    visible anywhere in the DOM after a fully valid form submission.  The happy
    path must produce a completely clean page with no validation feedback.
    """
    _fill_canonical_form(page)
    page.get_by_role("button", name="Add Release Note").click()

    # Wait for card to confirm submission completed
    expect(
        page.locator(".product-version", has_text=f"{PRODUCT} - {VERSION}")
    ).to_be_visible()

    # Count .field-error elements whose offsetParent is non-null (i.e. visible)
    visible_errors = page.evaluate(
        "() => Array.from(document.querySelectorAll('.field-error'))"
        ".filter(el => el.offsetParent !== null).length"
    )
    assert visible_errors == 0, (
        f"Expected 0 visible .field-error elements after valid submission, got {visible_errors}"
    )


# ── TC-005 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_req002_005
@pytest.mark.req_002
@pytest.mark.story_002
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.regression
@pytest.mark.e2e
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.functional
def test_submitted_release_visible_after_reload(page):
    """
    TC-005 (REQ-002, AC-5, FR-001/FR-003/FR-004/FR-007): Submitted release card
    survives a full page reload and remains at position 0 in #release-list.
    After reload the list must contain exactly 3 cards (2 seed + 1 submitted).
    """
    _fill_canonical_form(page)
    page.get_by_role("button", name="Add Release Note").click()

    # Confirm submission before triggering the reload
    expect(
        page.locator(".product-version", has_text=f"{PRODUCT} - {VERSION}")
    ).to_be_visible()

    # Full page reload — data must be re-hydrated from localStorage
    page.reload()
    page.wait_for_load_state("networkidle")

    # #release-list must contain exactly 3 cards (2 seed + 1 submitted)
    cards = page.locator("#release-list .release-card")
    expect(cards).to_have_count(3)

    # The submitted card must be at position 0 (most recent first)
    expect(
        cards.first.locator(".product-version")
    ).to_have_text(f"{PRODUCT} - {VERSION}")


# ── TC-006 ────────────────────────────────────────────────────────────────────

@pytest.mark.tc_req002_006
@pytest.mark.req_002
@pytest.mark.story_002
@pytest.mark.regression
@pytest.mark.medium
@pytest.mark.positive
@pytest.mark.ui
@pytest.mark.functional
def test_breaking_checkbox_stored_as_true(page):
    """
    TC-006 (REQ-002, AC-2 extension, FR-001/FR-003/FR-008): Valid submission
    with the breaking-change checkbox checked stores isBreaking as boolean true
    in localStorage.  All 7 fields on the persisted entry are verified (ISS-006).
    Distinct test data used to prevent interference with TC-001–TC-005 (ISS-002).
    """
    page.fill("#product",     TC006_PRODUCT)
    page.fill("#version",     TC006_VERSION)
    page.fill("#title",       TC006_TITLE)
    page.fill("#description", TC006_DESCRIPTION)
    page.fill("#releaseDate", TC006_RELEASE_DATE)
    page.check("#breaking")
    page.get_by_role("button", name="Add Release Note").click()

    # Wait for card to confirm the submission ran
    expect(
        page.locator(".product-version", has_text=f"{TC006_PRODUCT} - {TC006_VERSION}")
    ).to_be_visible()

    releases = page.evaluate(LS_READ)

    assert len(releases) == 3, (
        f"Expected 3 entries (2 seed + 1 new), got {len(releases)}"
    )

    entry = releases[0]  # unshift() places newest entry at index 0

    # ISS-006: assert ALL 7 required fields — not just isBreaking
    assert entry["product"] == TC006_PRODUCT, (
        f"Expected product '{TC006_PRODUCT}', got '{entry['product']}'"
    )
    assert entry["version"] == TC006_VERSION, (
        f"Expected version '{TC006_VERSION}', got '{entry['version']}'"
    )
    assert entry["title"] == TC006_TITLE, (
        f"Expected title '{TC006_TITLE}', got '{entry['title']}'"
    )
    assert entry["description"] == TC006_DESCRIPTION, (
        f"Expected description '{TC006_DESCRIPTION}', got '{entry['description']}'"
    )
    assert entry["releaseDate"] == TC006_RELEASE_DATE, (
        f"Expected releaseDate '{TC006_RELEASE_DATE}', got '{entry['releaseDate']}'"
    )
    assert entry["isBreaking"] is True, (
        f"Expected isBreaking True (checkbox checked), got '{entry['isBreaking']}'"
    )
    assert entry.get("id"), (
        f"Expected a non-empty id field (UUID), got '{entry.get('id')}'"
    )
