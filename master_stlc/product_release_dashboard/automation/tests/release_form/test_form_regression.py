"""
test_form_regression.py — TC-019 through TC-024
Regression checks (TC-019–022): verify that REQ-001 validation changes do not
break existing application behaviour — seed data rendering, product filter,
and data integrity after invalid submissions.

End-to-end flows (TC-023–024): complete validation → reactive correction →
successful submission cycles covering all four acceptance criteria (AC-1–AC-4).

Requirement : REQ-001 — Inline Form Validation for Release Notes Dashboard
Feature file: features/release_form/form_regression.feature
Test plan   : TP-001  |  TC range: TC-019 – TC-024

Seed state (guaranteed by conftest page fixture)
------------------------------------------------
After localStorage.clear() + reload the app writes exactly two seed entries:
  [0]  product="Billing API",  version="v1.4.0"
  [1]  product="Auth Service", version="v2.0.0"

E2E acceptance criteria exercised (TC-023, TC-024)
---------------------------------------------------
  AC-1  empty field + submit       → inline error appears adjacent to field
  AC-2  invalid submit             → no entry written to localStorage
  AC-3  field corrected (no resubmit) → error clears reactively
  AC-4  all fields valid + submit  → entry created, persisted, form reset
"""

import pytest
from playwright.sync_api import expect

# ── Module-level constants ────────────────────────────────────────────────────

LS_READ = "JSON.parse(localStorage.getItem('releaseNotesDashboard.releases') || '[]')"
FIELDS  = ["product", "version", "title", "description", "releaseDate"]


# ==============================================================================
# Regression scenarios — TC-019 through TC-022
# ==============================================================================

@pytest.mark.tc_019
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.medium
@pytest.mark.ui
@pytest.mark.functional
def test_seed_entries_rendered_in_release_list_on_page_load(page):
    """
    TC-019: Seed release entries are rendered in the release list on page load —
    REQ-001-regression.
    After localStorage clear + reload the app auto-seeds two known entries.
    """
    # Both seed cards must be visible immediately after the fixture loads
    expect(
        page.locator(".product-version", has_text="Billing API - v1.4.0")
    ).to_be_visible()
    expect(
        page.locator(".product-version", has_text="Auth Service - v2.0.0")
    ).to_be_visible()

    # Total visible release card count must be exactly 2
    expect(page.locator(".release-card")).to_have_count(2)


@pytest.mark.tc_020
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.medium
@pytest.mark.ui
@pytest.mark.functional
def test_product_filter_works_while_validation_errors_visible(page):
    """
    TC-020: The product filter works correctly while inline validation errors
    are visible on the form — REQ-001, FR-4 (regression).
    Form errors must not interfere with filter behaviour.
    """
    # Trigger all five inline validation errors by submitting with empty form
    page.get_by_role("button", name="Add Release Note").click()

    for field_id in FIELDS:
        expect(page.locator(f'.field-error[data-for="{field_id}"]')).to_be_visible()

    # Apply product filter — must filter release list independently of form errors
    page.fill("#product-filter", "Billing")

    # Only "Billing API" card must be visible; "Auth Service" is filtered out
    expect(page.locator(".release-card")).to_have_count(1)
    expect(
        page.locator(".product-version", has_text="Billing API")
    ).to_be_visible()

    # Inline errors must remain visible and unchanged after filtering
    for field_id in FIELDS:
        expect(page.locator(f'.field-error[data-for="{field_id}"]')).to_be_visible()


@pytest.mark.tc_021
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.medium
@pytest.mark.ui
@pytest.mark.functional
def test_product_filter_returns_newly_added_release(page):
    """
    TC-021: The product filter returns the newly added release when filtered by
    its product name — REQ-001-regression.
    """
    # Submit a valid release
    page.fill("#product",     "Inventory Service")
    page.fill("#version",     "v1.0.0")
    page.fill("#title",       "Warehouse sync")
    page.fill("#description", "Syncs warehouse inventory in real time.")
    page.fill("#releaseDate", "2026-09-24")
    page.get_by_role("button", name="Add Release Note").click()

    # Wait for the new card to confirm the submit completed
    expect(
        page.locator(".product-version", has_text="Inventory Service - v1.0.0")
    ).to_be_visible()

    # Filter by the new product — must return exactly 1 card
    page.fill("#product-filter", "Inventory Service")
    expect(page.locator(".release-card")).to_have_count(1)
    expect(
        page.locator(".release-card", has_text="Inventory Service")
    ).to_be_visible()

    # Filter by a non-existent product — must show empty-state and zero cards
    page.fill("#product-filter", "NonExistentProduct")
    expect(page.locator(".empty-state")).to_be_visible()
    expect(page.locator(".release-card")).to_have_count(0)


@pytest.mark.tc_022
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.regression
@pytest.mark.medium
@pytest.mark.ui
@pytest.mark.functional
def test_existing_entries_unchanged_after_invalid_submit(page):
    """
    TC-022: Existing release entries are not removed or altered after an invalid
    form submission — REQ-001, FR-3 (regression).
    Baseline: two seed entries visible before and after the invalid submit.
    """
    # Baseline: verify two seed entries are present
    expect(page.locator(".release-card")).to_have_count(2)
    expect(
        page.locator(".product-version", has_text="Billing API - v1.4.0")
    ).to_be_visible()
    expect(
        page.locator(".product-version", has_text="Auth Service - v2.0.0")
    ).to_be_visible()

    # Trigger an invalid (all-empty) form submission
    page.get_by_role("button", name="Add Release Note").click()
    expect(page.locator('.field-error[data-for="product"]')).to_be_visible()

    # Both seed cards must still be present and unchanged
    expect(page.locator(".release-card")).to_have_count(2)
    expect(
        page.locator(".product-version", has_text="Billing API - v1.4.0")
    ).to_be_visible()
    expect(
        page.locator(".product-version", has_text="Auth Service - v2.0.0")
    ).to_be_visible()


# ==============================================================================
# End-to-end flow scenarios — TC-023 through TC-024
# ==============================================================================

@pytest.mark.tc_023
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.e2e
@pytest.mark.ui
@pytest.mark.functional
def test_full_flow_single_field_error_corrected_then_valid_submit(page):
    """
    TC-023: Full flow — single field triggers an error, is corrected reactively,
    then a valid submission succeeds — REQ-001, AC-1, AC-2, AC-3, AC-4, FR-1–4.
    """
    # ── Phase 1: fill all fields except product and click Submit ──────────────
    page.fill("#version",     "v1.0.0")
    page.fill("#title",       "Initial Release")
    page.fill("#description", "First stable release.")
    page.fill("#releaseDate", "2026-09-24")
    page.get_by_role("button", name="Add Release Note").click()

    # ── Phase 2: product error visible; no release created (AC-1, AC-2) ──────
    expect(page.locator('.field-error[data-for="product"]')).to_be_visible()

    releases = page.evaluate(LS_READ)
    assert len(releases) == 2, (
        f"Expected 2 seed entries on failed submit (no product), got {len(releases)}"
    )

    # ── Phase 3: correct product field — error clears reactively (AC-3) ──────
    page.fill("#product", "Billing API")
    expect(page.locator('.field-error[data-for="product"]')).to_be_hidden()

    # ── Phase 4: all fields now valid — submit and verify full success (AC-4) ─
    page.get_by_role("button", name="Add Release Note").click()

    # Release card must be visible in the list
    expect(
        page.locator(".product-version", has_text="Billing API - v1.0.0")
    ).to_be_visible()

    # localStorage must contain 3 entries: 2 seed + 1 new
    releases = page.evaluate(LS_READ)
    assert len(releases) == 3, (
        f"Expected 3 entries after valid submit, got {len(releases)}"
    )

    # No inline errors must remain visible after a successful submit
    for field_id in FIELDS:
        expect(page.locator(f'.field-error[data-for="{field_id}"]')).to_be_hidden()

    # Form must be fully reset by form.reset()
    for field_id in FIELDS:
        expect(page.locator(f"#{field_id}")).to_have_value("")


@pytest.mark.tc_024
@pytest.mark.req_001
@pytest.mark.story_001
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.e2e
@pytest.mark.ui
@pytest.mark.functional
def test_full_flow_all_five_errors_each_corrected_then_valid_submit(page):
    """
    TC-024: Full flow — all five errors triggered, each corrected individually,
    then a valid submission succeeds — REQ-001, AC-1, AC-2, AC-3, AC-4, FR-1–4.
    """
    # ── Phase 1: submit with all five fields empty ────────────────────────────
    page.get_by_role("button", name="Add Release Note").click()

    # ── Phase 2: all five errors visible; no release created (AC-1, AC-2) ────
    for field_id in FIELDS:
        expect(page.locator(f'.field-error[data-for="{field_id}"]')).to_be_visible()

    releases = page.evaluate(LS_READ)
    assert len(releases) == 2, (
        f"Expected 2 seed entries on all-empty submit, got {len(releases)}"
    )

    # ── Phase 3: correct each field one by one; error clears reactively (AC-3) ─

    page.fill("#product", "Payments Gateway")
    expect(page.locator('.field-error[data-for="product"]')).to_be_hidden()

    page.fill("#version", "v2.0.0")
    expect(page.locator('.field-error[data-for="version"]')).to_be_hidden()

    page.fill("#title", "Payment integration")
    expect(page.locator('.field-error[data-for="title"]')).to_be_hidden()

    page.fill("#description", "Added Stripe integration to the payments module.")
    expect(page.locator('.field-error[data-for="description"]')).to_be_hidden()

    page.fill("#releaseDate", "2026-09-24")
    expect(page.locator('.field-error[data-for="releaseDate"]')).to_be_hidden()

    # ── Phase 4: all fields valid — submit and verify (AC-4) ─────────────────
    page.get_by_role("button", name="Add Release Note").click()

    # Release card must be visible in the list
    expect(
        page.locator(".product-version", has_text="Payments Gateway - v2.0.0")
    ).to_be_visible()

    # localStorage must contain 3 entries: 2 seed + 1 new
    releases = page.evaluate(LS_READ)
    assert len(releases) == 3, (
        f"Expected 3 entries after valid submit, got {len(releases)}"
    )

    # No inline errors must remain visible after a successful submit
    for field_id in FIELDS:
        expect(page.locator(f'.field-error[data-for="{field_id}"]')).to_be_hidden()

    # Form must be fully reset by form.reset()
    for field_id in FIELDS:
        expect(page.locator(f"#{field_id}")).to_have_value("")
