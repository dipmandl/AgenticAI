"""
Step definitions for:
  features/json_export/release_notes_stability.feature

Story:   COD-9 — Export Release Notes to JSON File
REQ-IDs: REQ-005

Traceability:
  @TC-023 @REQ-005  — Release list renders correctly after Export feature is added
  @TC-024 @REQ-005  — Add release functionality is unaffected
  @TC-025 @REQ-005  — Edit release functionality is unaffected
  @TC-026 @REQ-005  — Delete release functionality is unaffected
  @TC-027 @REQ-005  — Page navigation and routing are unaffected
  @TC-028 @REQ-005  — localStorage write operations by existing code are unaffected

Skipped (manual_only): TC-029
"""

import json

from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.release_dashboard_page import ReleaseDashboardPage
from utils.helpers import (
    clear_local_storage,
    get_local_storage,
    make_release,
    make_releases,
    read_releases_from_storage,
    set_local_storage,
    STORAGE_KEY,
)


# ---------------------------------------------------------------------------
# Background steps
# ---------------------------------------------------------------------------

@given('the application is loaded with the Export JSON feature present in the UI')
def step_app_loaded_with_export(context):
    """TC-023 … TC-028 background: open app and assert Export JSON button exists."""
    context.page = ReleaseDashboardPage(context.driver)
    context.page.navigate(context.app_url)
    assert context.page.is_export_json_button_visible(), (
        "Export JSON button not visible — feature may not be deployed yet."
    )


# ---------------------------------------------------------------------------
# Given — localStorage state setup (regression)
# ---------------------------------------------------------------------------

@given('the "{key}" key in localStorage contains release notes')
def step_regression_storage_has_releases(context, key):
    releases = make_releases(3)
    set_local_storage(context.driver, releases, key)
    context.seeded_releases = releases
    context.driver.get(context.app_url)


# ---------------------------------------------------------------------------
# When — user actions (regression scenarios)
# ---------------------------------------------------------------------------

@when('the user fills the Add Release Note form with valid values for product, version, title, description, and release date')
def step_fill_add_form(context):
    context.new_release_title = "Regression Test Release"
    context.page.fill_form(
        product="Regression Product",
        version="v9.9.9",
        team_name="Regression Team",
        title=context.new_release_title,
        description="Added by regression test TC-024.",
        release_date="2026-06-01",
        is_breaking=False,
    )


@when('the user submits the form')
def step_submit_form(context):
    context.page.submit_form()


@when('the user edits an existing release and changes the title to "Updated Title"')
def step_edit_release_title(context):
    context.updated_title = "Updated Title"
    context.page.click_edit_first_card()
    title_input = WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "title"))
    )
    title_input.clear()
    title_input.send_keys(context.updated_title)


@when('the user saves the edit')
def step_save_edit(context):
    context.page.submit_form()


@when('the user deletes a release using the delete action')
def step_delete_release(context):
    context.page.click_delete_first_card()


@when('the user navigates through all available application views')
def step_navigate_views(context):
    context.page.navigate_all_views()


@when('the user adds 2 new releases, edits 1 release, and deletes 1 release')
def step_combined_operations(context):
    # Add release 1
    context.page.fill_form(
        product="Op Product 1", version="v1.0.0", team_name="Ops Team",
        title="Op Release 1", description="First op release.",
        release_date="2026-07-01",
    )
    context.page.submit_form()

    # Add release 2
    context.page.fill_form(
        product="Op Product 2", version="v2.0.0", team_name="Ops Team",
        title="Op Release 2", description="Second op release.",
        release_date="2026-07-02",
    )
    context.page.submit_form()

    # Edit the first visible card (most recently added)
    context.page.edit_first_release_title("Op Release 2 — Edited")

    # Delete the first visible card
    context.page.click_delete_first_card()


# ---------------------------------------------------------------------------
# Then — assertions (regression scenarios)
# ---------------------------------------------------------------------------

# TC-023 (part 1)
@then('the release notes list renders with all expected release cards visible')
def step_release_cards_visible(context):
    count = context.page.count_release_cards()
    assert count > 0, "No release cards rendered in the release list."


# TC-023 (part 2)
@then('the rendering matches the pre-Export-feature baseline')
def step_rendering_matches_baseline(context):
    # Baseline: all seeded cards are present and visible
    count = context.page.count_release_cards()
    expected = len(context.seeded_releases)
    assert count == expected, (
        f"Card count mismatch: expected {expected}, found {count}"
    )


# TC-024 (part 1)
@then('the new release card is visible in the release list')
def step_new_card_visible(context):
    assert context.page.is_card_with_title_visible(context.new_release_title), (
        f"New release card with title '{context.new_release_title}' not found."
    )


# TC-024 (part 2)
@then('the new release is persisted to the "{key}" key in localStorage')
def step_new_release_in_storage(context, key):
    releases = read_releases_from_storage(context.driver, key)
    assert releases is not None, "No releases found in localStorage."
    titles = [r["title"] for r in releases]
    assert context.new_release_title in titles, (
        f"New release '{context.new_release_title}' not found in localStorage. Found: {titles}"
    )


# TC-025 (part 1)
@then('the updated release card displays "Updated Title" in the release list')
def step_updated_card_visible(context):
    assert context.page.is_card_with_title_visible("Updated Title"), (
        "Updated release card with title 'Updated Title' not found in list."
    )


# TC-025 (part 2)
@then('the "{key}" key in localStorage reflects the updated title')
def step_updated_title_in_storage(context, key):
    releases = read_releases_from_storage(context.driver, key)
    assert releases is not None, "No releases found in localStorage."
    titles = [r["title"] for r in releases]
    assert "Updated Title" in titles, (
        f"'Updated Title' not persisted to localStorage. Found titles: {titles}"
    )


# TC-026 (part 1)
@then('the deleted release card is no longer visible in the release list')
def step_deleted_card_gone(context):
    count = context.page.count_release_cards()
    expected = len(context.seeded_releases) - 1
    assert count == expected, (
        f"Expected {expected} release cards after delete, found {count}."
    )


# TC-026 (part 2)
@then('the release is removed from the "{key}" key in localStorage')
def step_release_removed_from_storage(context, key):
    releases = read_releases_from_storage(context.driver, key)
    assert releases is not None, "No releases found in localStorage after delete."
    expected = len(context.seeded_releases) - 1
    assert len(releases) == expected, (
        f"Expected {expected} releases in localStorage after delete, found {len(releases)}."
    )


# TC-027 (part 1)
@then('each view loads and displays correctly')
def step_views_load_correctly(context):
    # For a single-page app, verify the release-list section is still present
    from selenium.webdriver.common.by import By
    elements = context.driver.find_elements(By.ID, "release-list")
    assert len(elements) == 1, "Release list section missing after navigation."


# TC-027 (part 2)
@then('navigation behavior matches the pre-Export-feature baseline')
def step_navigation_matches_baseline(context):
    # Export button still visible after scroll/navigation
    assert context.page.is_export_json_button_visible(), (
        "Export JSON button disappeared after navigation."
    )


# TC-028 (part 1)
@then('the "{key}" key in localStorage reflects only the intended operations')
def step_storage_reflects_operations(context, key):
    releases = read_releases_from_storage(context.driver, key)
    assert releases is not None, "localStorage empty — expected persisted releases."
    # 3 seeded + 2 added - 1 deleted = 4 remaining
    expected = len(context.seeded_releases) + 1
    assert len(releases) == expected, (
        f"Expected {expected} releases after add(2)/edit(1)/delete(1), found {len(releases)}."
    )


# TC-028 (part 2)
@then('no residual data from the Export JSON action is present in localStorage')
def step_no_export_residue(context):
    # Export JSON writes no keys to localStorage; verify the storage key structure
    raw = get_local_storage(context.driver, STORAGE_KEY)
    if raw is not None:
        try:
            parsed = json.loads(raw)
            assert isinstance(parsed, list), (
                "localStorage releases key contains non-array data — possible Export residue."
            )
        except json.JSONDecodeError:
            raise AssertionError(
                "localStorage releases key contains invalid JSON — possible Export residue."
            )


# TC-027 additional — application loaded with feature present (for TC-027 background override)
@given('the application is loaded with the Export JSON feature present')
def step_app_loaded_export_present(context):
    context.page = ReleaseDashboardPage(context.driver)
    context.page.navigate(context.app_url)
    assert context.page.is_export_json_button_visible(), (
        "Export JSON button not visible in UI."
    )
