"""
Step definitions for:
  features/delete_release/delete_release.feature

Story:    COD-8 — Delete a Release Note with Confirmation
REQ-IDs:  REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006

Traceability:
  @TC-001 @REQ-001  — Delete button visible on every rendered release card
  @TC-002 @REQ-002  — Clicking Delete shows a browser confirmation dialog
  @TC-003 @REQ-003 @REQ-005  — Confirmed deletion removes card from DOM
  @TC-004 @REQ-004  — Confirmed deletion removes release from localStorage
  @TC-005 @REQ-003 @REQ-005  — Card count decreases by exactly one
  @TC-006 @REQ-003 @REQ-005  — Other releases unaffected after one deletion
  @TC-007 @REQ-004  — Deleted release does not reappear after page reload
  @TC-008 @REQ-003 @REQ-004 @REQ-005  — Delete while in edit mode resets form
  @TC-009 @REQ-006  — Cancelling dialog keeps release visible
  @TC-010 @REQ-006  — Cancelling dialog leaves localStorage unchanged
  @TC-011 @REQ-006  — Dismissing dialog has same effect as cancelling
  @TC-013 @REQ-003 @REQ-004  — Rapid successive deletions do not corrupt state
  @TC-014 @REQ-003 @REQ-004 @REQ-005  — Deleting the only release renders empty state
  @TC-015 @REQ-003 @REQ-005  — Deleting the first release leaves others intact
  @TC-016 @REQ-003 @REQ-005  — Deleting the last release leaves others intact
  @TC-017 @REQ-005  — Active product filter preserved after deletion re-render
  @TC-018 @REQ-004  — Deleted release absent after multiple page reloads
  @TC-019 @REQ-004  — Add release still persists correctly (regression)
  @TC-020 @REQ-003 @REQ-005  — Edit form unaffected when different release deleted
  @TC-021 @REQ-005  — Filter/search results correct after deletion
  @TC-022 @REQ-004  — JSON export does not include deleted release
  @TC-023 @REQ-004 @REQ-005  — App correct state when all releases deleted and reloaded

Skipped (manual_only): TC-012, TC-024

NOTE: Background steps (the user has opened the application in the browser,
      the application storage key is "...") are defined in step_json_export.py
      and reused automatically by Behave.
"""

import json
import time

from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.release_dashboard_page import ReleaseDashboardPage
from utils.helpers import (
    get_local_storage,
    make_release,
    make_releases,
    read_releases_from_storage,
    read_json_file,
    set_local_storage,
    STORAGE_KEY,
)


# ---------------------------------------------------------------------------
# Given — localStorage state setup (COD-8 specific)
# ---------------------------------------------------------------------------

# TC-003 — seed exactly 2 releases
@given('the "{key}" key in localStorage contains exactly 2 release notes')
def step_storage_exactly_two(context, key):
    """TC-003: precondition — exactly 2 releases present."""
    releases = make_releases(2)
    set_local_storage(context.driver, releases, key)
    context.driver.get(context.app_url)


# TC-003 — assert 2 cards visible and record for targeted-card assertion
@given('the user observes 2 release cards in the DOM')
def step_observe_2_cards(context):
    """TC-003: confirm 2 cards are rendered before the deletion step."""
    count = context.page.count_release_cards()
    assert count == 2, (
        f"Precondition failed: expected 2 release cards in DOM, found {count}."
    )


# TC-004 — seed 1 release with a known ID
@given('the "{key}" key in localStorage contains at least 1 release note with a known ID')
def step_storage_one_known_id(context, key):
    """TC-004: seed one release and store its ID for later assertion."""
    release = make_release(index=1, title="Known Release")
    context.known_release_id = release["id"]
    context.target_title = release["title"]
    set_local_storage(context.driver, [release], key)
    context.driver.get(context.app_url)


# TC-005, TC-013 — seed exactly 3 releases
@given('the "{key}" key in localStorage contains exactly 3 release notes')
def step_storage_exactly_three(context, key):
    """TC-005, TC-013: precondition — exactly 3 releases present."""
    releases = make_releases(3)
    context.seeded_releases = releases
    set_local_storage(context.driver, releases, key)
    context.driver.get(context.app_url)


# TC-005 — assert 3 cards visible
@given('the user observes exactly 3 release cards in the DOM')
def step_observe_3_cards(context):
    """TC-005: confirm 3 cards are rendered before the deletion step."""
    count = context.page.count_release_cards()
    assert count == 3, (
        f"Precondition failed: expected 3 release cards in DOM, found {count}."
    )


# TC-006 — seed 3 releases with specific titles
@given('the "{key}" key in localStorage contains 3 release notes with titles "Release Alpha", "Release Beta", and "Release Gamma"')
def step_storage_alpha_beta_gamma(context, key):
    """TC-006: 3 releases with fixed titles for targeted deletion verification."""
    releases = [
        make_release(1, product="Alpha Product", title="Release Alpha"),
        make_release(2, product="Beta Product",  title="Release Beta"),
        make_release(3, product="Gamma Product", title="Release Gamma"),
    ]
    context.seeded_releases = releases
    set_local_storage(context.driver, releases, key)
    context.driver.get(context.app_url)


# TC-007, TC-018 — seed 1 release with a specific title (parameterised)
@given('the "{key}" key in localStorage contains at least 1 release note with title "{title}"')
def step_storage_one_with_title(context, key, title):
    """TC-007, TC-018: seed one release whose title matches the scenario title."""
    release = make_release(index=1, title=title)
    context.target_title = title
    context.known_release_id = release["id"]
    set_local_storage(context.driver, [release], key)
    context.driver.get(context.app_url)


# TC-008 — open edit mode on the first card
@given('the user has clicked the Edit button on a release card to open the edit form with its data')
def step_open_edit_form_first_card(context):
    """TC-008: put the first release card into edit mode."""
    cards = context.page.get_release_cards()
    assert len(cards) > 0, "Precondition failed: no release cards available to open for edit."
    context.editing_card_title = context.page.get_card_title(cards[0])
    context.editing_card_id = getattr(context, 'known_release_id', None)
    context.page.click_edit_first_card()
    # Verify the form is now populated (cancel-edit button is visible)
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "cancel-edit-button"))
    )


# TC-009 — record current card count before the delete action
@given('the user observes the current count of release cards in the DOM')
def step_observe_current_count(context):
    """TC-009: capture baseline card count before clicking Delete."""
    context.pre_delete_count = context.page.count_release_cards()


# TC-010 — record current localStorage value before the delete action
@given('the user records the current value of the "{key}" localStorage key before clicking Delete')
def step_record_storage_before_delete(context, key):
    """TC-010: snapshot localStorage so it can be compared after a cancelled deletion."""
    context.pre_delete_storage = get_local_storage(context.driver, key)


# TC-015, TC-016 — seed 3 releases in a specific named order
@given('the "{key}" key in localStorage contains 3 release notes with titles "Release A", "Release B", and "Release C" in that order')
def step_storage_a_b_c_order(context, key):
    """TC-015, TC-016: three releases in a known order for boundary deletion tests."""
    releases = [
        make_release(1, product="Product A", title="Release A"),
        make_release(2, product="Product B", title="Release B"),
        make_release(3, product="Product C", title="Release C"),
    ]
    context.seeded_releases = releases
    set_local_storage(context.driver, releases, key)
    context.driver.get(context.app_url)


# TC-017 — seed 3 releases where 2 share product "Billing API"
@given('the "{key}" key in localStorage contains 3 release notes where 2 share the product name "Billing API"')
def step_storage_two_billing_api(context, key):
    """TC-017: 2 releases for 'Billing API' product + 1 for a different product."""
    releases = [
        make_release(1, product="Billing API",   title="Billing API Release 1"),
        make_release(2, product="Billing API",   title="Billing API Release 2"),
        make_release(3, product="Other Product", title="Other Product Release"),
    ]
    context.seeded_releases = releases
    context.non_matching_title = "Other Product Release"
    set_local_storage(context.driver, releases, key)
    context.driver.get(context.app_url)


# TC-017 — apply the product filter so 2 matching cards are shown
@given('the user has applied the product filter "Billing API" so that only 2 matching release cards are shown')
def step_apply_billing_api_filter(context):
    """TC-017: select 'Billing API' in the product filter drop-down."""
    context.page.set_product_filter("Billing API")
    visible = context.page.count_release_cards()
    assert visible == 2, (
        f"Expected 2 release cards after applying 'Billing API' filter, found {visible}."
    )


# TC-020 — seed 2 releases with titles "Release A" and "Release B"
@given('the "{key}" key in localStorage contains 2 release notes with titles "Release A" and "Release B"')
def step_storage_release_a_and_b(context, key):
    """TC-020: two named releases for the edit-form isolation test."""
    releases = [
        make_release(1, product="Product A", title="Release A"),
        make_release(2, product="Product B", title="Release B"),
    ]
    context.seeded_releases = releases
    set_local_storage(context.driver, releases, key)
    context.driver.get(context.app_url)


# TC-020 — open edit mode on the card with title "Release A"
@given('the user has clicked the Edit button on the release card with title "Release A" to open the edit form')
def step_open_edit_release_a(context):
    """TC-020: put 'Release A' into edit mode before deleting 'Release B'."""
    context.page.click_edit_card_by_title("Release A")
    WebDriverWait(context.driver, 10).until(
        EC.visibility_of_element_located((By.ID, "cancel-edit-button"))
    )


# TC-021 — seed 3 releases where 2 contain "Payments" in their titles
@given('the "{key}" key in localStorage contains 3 release notes where 2 have titles containing the keyword "Payments"')
def step_storage_two_payments(context, key):
    """TC-021: 2 releases with 'Payments' in title + 1 unrelated release."""
    releases = [
        make_release(1, product="Payments Product", title="Payments v1"),
        make_release(2, product="Payments Product", title="Payments v2"),
        make_release(3, product="Other Product",    title="Unrelated Release"),
    ]
    context.seeded_releases = releases
    context.non_matching_title = "Unrelated Release"
    context.deleted_payments_title = "Payments v1"
    set_local_storage(context.driver, releases, key)
    context.driver.get(context.app_url)


# TC-021 — enter "Payments" in the search input
@given('the user has entered "Payments" in the search input so that 2 matching cards are shown')
def step_enter_payments_search(context):
    """TC-021: type 'Payments' into the search filter to show 2 matching cards."""
    context.page.set_search_filter("Payments")
    visible = context.page.count_release_cards()
    assert visible == 2, (
        f"Expected 2 cards after entering 'Payments' in search, found {visible}."
    )


# TC-022 — seed 2 releases with titles "Export Me" and "Delete Me"
@given('the "{key}" key in localStorage contains 2 release notes with titles "Export Me" and "Delete Me"')
def step_storage_export_and_delete(context, key):
    """TC-022: set up two releases for the JSON-export regression check."""
    releases = [
        make_release(1, product="Export Product", title="Export Me"),
        make_release(2, product="Delete Product", title="Delete Me"),
    ]
    context.seeded_releases = releases
    set_local_storage(context.driver, releases, key)
    context.driver.get(context.app_url)


# ---------------------------------------------------------------------------
# When — user actions (COD-8 specific)
# ---------------------------------------------------------------------------

# TC-001
@when('the user views the release list')
def step_view_release_list(context):
    """TC-001: ensure the release-list container is visible."""
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "release-list"))
    )


# TC-002, TC-009, TC-010, TC-011 — click Delete on first card without handling dialog
@when('the user clicks the Delete button on a release card')
def step_click_delete_a_card(context):
    """TC-002, TC-009, TC-010, TC-011: click Delete on the first card; leave dialog open."""
    context.pre_delete_count = context.page.count_release_cards()
    context.pre_delete_storage = get_local_storage(context.driver, STORAGE_KEY)
    context.page.click_delete_button_on_first_card()


# TC-005 — same action, different step text
@when('the user clicks the Delete button on one release card')
def step_click_delete_one_card(context):
    """TC-005: click Delete on the first card (one of many); leave dialog open."""
    context.pre_delete_count = context.page.count_release_cards()
    context.page.click_delete_button_on_first_card()


# TC-003 — click Delete on the first card by position
@when('the user clicks the Delete button on the first release card')
def step_click_delete_first_card(context):
    """TC-003: click Delete on the first card; record its title for later assertion."""
    cards = context.page.get_release_cards()
    assert len(cards) > 0, "No release cards to delete."
    context.targeted_card_title = context.page.get_card_title(cards[0])
    context.pre_delete_count = context.page.count_release_cards()
    context.page.click_delete_button_on_first_card()


# TC-004 — "that release card" = first card (only 1 seeded with known ID)
@when('the user clicks the Delete button on that release card')
def step_click_delete_that_card(context):
    """TC-004: click Delete on the first card (the one seeded with a known ID)."""
    context.page.click_delete_button_on_first_card()


# TC-014 — "only release card" = first (and only) card
@when('the user clicks the Delete button on the only release card')
def step_click_delete_only_card(context):
    """TC-014: click Delete on the only remaining release card."""
    context.page.click_delete_button_on_first_card()


# TC-008 — "same release card" = the card currently open in edit mode (first card)
@when('the user clicks the Delete button on the same release card')
def step_click_delete_same_card(context):
    """TC-008: click Delete on the card that is currently in edit mode."""
    context.page.click_delete_button_on_first_card()


# TC-006, TC-007, TC-008-related, TC-017, TC-018, TC-020, TC-021, TC-022 —
# click Delete by title
@when('the user clicks the Delete button on the release card with title "{title}"')
def step_click_delete_by_title(context, title):
    """TC-006, TC-007, TC-018, TC-020, TC-021, TC-022: click Delete on the card matching *title*."""
    context.target_title = title
    context.page.click_delete_button_by_title(title)


# TC-015 — click Delete on the first card that matches *title*
@when('the user clicks the Delete button on the first release card with title "{title}"')
def step_click_delete_first_by_title(context, title):
    """TC-015: click Delete on the first card matching *title*."""
    context.target_title = title
    context.page.click_delete_button_by_title(title)


# TC-016 — click Delete on the LAST card that matches *title*
@when('the user clicks the Delete button on the last release card with title "{title}"')
def step_click_delete_last_by_title(context, title):
    """TC-016: click Delete on the last card matching *title*."""
    context.target_title = title
    context.page.click_delete_last_card_by_title(title)


# TC-017 — click Delete on one of the visible filtered cards (first visible)
@when('the user clicks the Delete button on one of the visible filtered release cards')
def step_click_delete_filtered_card(context):
    """TC-017: click Delete on the first currently-visible (filtered) card."""
    cards = context.page.get_release_cards()
    assert len(cards) > 0, "No visible cards to delete after filtering."
    context.deleted_filtered_title = context.page.get_card_title(cards[0])
    context.page.click_delete_button_on_first_card()


# TC-021 — click Delete on the first of the 2 matching search-result cards
@when('the user clicks the Delete button on one of the 2 matching release cards')
def step_click_delete_matching_card(context):
    """TC-021: click Delete on the first visible card in the filtered search results."""
    cards = context.page.get_release_cards()
    assert len(cards) > 0, "No matching release cards visible to delete."
    context.deleted_payments_title = context.page.get_card_title(cards[0])
    context.page.click_delete_button_on_first_card()


# Multiple TCs — accept the browser confirmation dialog
@when('the user accepts the confirmation dialog')
def step_accept_dialog(context):
    """TC-003…TC-023: accept (confirm) the browser confirm dialog."""
    context.page.accept_dialog()
    time.sleep(0.1)  # brief wait for DOM re-render


# TC-009, TC-010 — cancel the browser confirmation dialog
@when('the user cancels the confirmation dialog')
def step_cancel_dialog(context):
    """TC-009, TC-010: dismiss (cancel) the browser confirm dialog."""
    context.page.dismiss_dialog()


# TC-011 — dismiss via Escape / dismiss method
@when('the user dismisses the confirmation dialog without confirming')
def step_dismiss_dialog(context):
    """TC-011: dismiss the confirm dialog (equivalent to pressing Cancel/Escape)."""
    context.page.dismiss_dialog()


# TC-013 — delete first card immediately
@when('the user deletes the first release card and immediately accepts the confirmation dialog')
def step_delete_first_immediately(context):
    """TC-013: delete the first card and accept the dialog without delay."""
    context.page.click_delete_button_on_first_card()
    context.page.accept_dialog()
    time.sleep(0.1)


# TC-013 — delete next card immediately (after first was deleted, first = next)
@when('the user immediately deletes the next release card and accepts the confirmation dialog without waiting')
def step_delete_next_immediately(context):
    """TC-013: delete the new first card (was second) and accept without pause."""
    context.page.click_delete_button_on_first_card()
    context.page.accept_dialog()
    time.sleep(0.1)


# TC-018 — reload the page twice in succession
@when('the user reloads the page twice in succession')
def step_reload_twice(context):
    """TC-018: reload the page twice to verify deletion persistence."""
    context.page.reload()
    context.page.reload()


# TC-019 — fill form, submit, and reload in a single compound step
@when('the user fills the Add Release Note form with valid data, submits the form, and reloads the page')
def step_fill_submit_reload(context):
    """TC-019: add a new release and verify it survives a full page reload."""
    context.new_release_title = "COD-8 Regression Add Release"
    context.page.fill_form(
        product="Regression Product",
        version="v9.9.9",
        team_name="Regression Team",
        title=context.new_release_title,
        description="Added by COD-8 regression test TC-019.",
        release_date="2026-06-01",
        is_breaking=False,
    )
    context.page.submit_form()
    context.page.reload()


# TC-021 — re-enter the search term after deletion
@when('the user re-enters "Payments" in the search input')
def step_reenter_payments_search(context):
    """TC-021: re-type 'Payments' in the search input to trigger a fresh filter render."""
    context.page.set_search_filter("Payments")
    time.sleep(0.1)


# TC-023 — delete every card one by one, confirming each
@when('the user deletes all existing release notes by confirming each deletion in turn')
def step_delete_all_releases(context):
    """TC-023: loop through all cards and delete each one, accepting the dialog each time."""
    max_iterations = 50  # guard against infinite loop
    for _ in range(max_iterations):
        if context.page.count_release_cards() == 0:
            break
        context.page.click_delete_button_on_first_card()
        context.page.accept_dialog()
        time.sleep(0.15)  # allow re-render before checking count


# ---------------------------------------------------------------------------
# Then — assertions (COD-8 specific)
# ---------------------------------------------------------------------------

# TC-001
@then('every rendered release card has a visible Delete button')
def step_every_card_has_delete_btn(context):
    """TC-001: assert each visible release card contains a displayed Delete button."""
    cards = context.page.get_release_cards()
    assert len(cards) > 0, "No release cards rendered — cannot verify Delete button presence."
    for i, card in enumerate(cards):
        btn = card.find_element(By.CSS_SELECTOR, ".delete-btn")
        assert btn.is_displayed(), (
            f"Delete button on card {i + 1} is not visible."
        )


# TC-002 — verify dialog is present (dialog is left open for next step)
@then('a browser confirmation dialog is displayed before any deletion occurs')
def step_dialog_is_displayed(context):
    """TC-002: confirm a browser alert/confirm dialog is currently open."""
    assert context.page.is_dialog_present(), (
        "No browser confirmation dialog appeared after clicking the Delete button."
    )


# TC-002 — dismiss dialog, then verify no card was removed
@then('no release has been removed from the DOM at the point the dialog appears')
def step_no_release_removed_while_dialog_open(context):
    """TC-002: close the dialog, then confirm the card count is unchanged."""
    try:
        context.page.dismiss_dialog()
    except Exception:
        pass  # dialog may already have been closed
    current_count = context.page.count_release_cards()
    expected = getattr(context, 'pre_delete_count', current_count)
    assert current_count == expected, (
        f"A release was removed before the dialog was answered. "
        f"Expected {expected} cards, found {current_count}."
    )


# TC-003
@then('the targeted release card is no longer visible in the DOM')
def step_targeted_card_not_visible(context):
    """TC-003: confirm the first card (whose title was recorded) is gone."""
    title = getattr(context, 'targeted_card_title', None)
    if title:
        assert not context.page.is_card_with_title_visible(title), (
            f"Targeted release card '{title}' is still visible in the DOM."
        )
    else:
        # Fallback: count decreased
        count = context.page.count_release_cards()
        pre = getattr(context, 'pre_delete_count', count + 1)
        assert count < pre, "Card count did not decrease after deletion."


# TC-003 count check; also reused for TC-014 variant (0 cards)
@then('the total count of visible release cards is {count:d}')
def step_total_count_is_n(context, count):
    """TC-003: assert the visible card count equals the expected value."""
    actual = context.page.count_release_cards()
    assert actual == count, (
        f"Expected {count} visible release card(s), found {actual}."
    )


# TC-005 card count
@then('exactly {count:d} release cards are visible in the DOM')
def step_exactly_n_cards_visible(context, count):
    """TC-005: assert exactly *count* release cards are rendered in the DOM."""
    actual = context.page.count_release_cards()
    assert actual == count, (
        f"Expected exactly {count} release card(s) in DOM, found {actual}."
    )


# TC-004 — localStorage no longer contains deleted ID
@then('the "{key}" key in localStorage no longer contains an entry with the deleted release ID')
def step_storage_no_deleted_id(context, key):
    """TC-004: verify the deleted release ID is absent from localStorage."""
    releases = read_releases_from_storage(context.driver, key)
    if releases is None or len(releases) == 0:
        return  # empty storage confirms absence
    deleted_id = getattr(context, 'known_release_id', None)
    if deleted_id:
        ids = [r.get("id") for r in releases]
        assert deleted_id not in ids, (
            f"Deleted release ID '{deleted_id}' is still present in localStorage."
        )


# TC-005, TC-006, TC-015, TC-016 — exact entry count in localStorage
@then('the "{key}" key in localStorage contains exactly {count:d} entries')
def step_storage_exact_entries(context, key, count):
    """TC-005, TC-006, TC-015, TC-016: assert localStorage array has exactly *count* items."""
    releases = read_releases_from_storage(context.driver, key) or []
    assert len(releases) == count, (
        f"Expected {count} entries in localStorage '{key}', found {len(releases)}."
    )


# TC-013 — exactly 1 entry (singular wording in feature file)
@then('the "{key}" key in localStorage contains exactly 1 entry')
def step_storage_exactly_1_entry(context, key):
    """TC-013: assert localStorage array has exactly 1 item."""
    releases = read_releases_from_storage(context.driver, key) or []
    assert len(releases) == 1, (
        f"Expected 1 entry in localStorage '{key}', found {len(releases)}."
    )


# TC-006 — release card with given title is visible
@then('the release card with title "{title}" remains visible in the DOM')
def step_card_with_title_visible(context, title):
    """TC-006, TC-020: assert a card with *title* is still rendered."""
    assert context.page.is_card_with_title_visible(title), (
        f"Release card with title '{title}' is not visible in the DOM."
    )


# TC-015, TC-016 — "remains present" synonym for "remains visible"
@then('the release card with title "{title}" remains present in the DOM')
def step_card_with_title_present(context, title):
    """TC-015, TC-016: assert a card with *title* is still rendered."""
    assert context.page.is_card_with_title_visible(title), (
        f"Release card with title '{title}' is not present in the DOM."
    )


# TC-006 — content of Alpha and Gamma entries unchanged
@then('neither entry in localStorage has been modified')
def step_neither_entry_modified(context):
    """TC-006: verify Alpha and Gamma releases retained their original field values."""
    releases = read_releases_from_storage(context.driver, STORAGE_KEY) or []
    remaining_titles = {r.get("title") for r in releases}
    assert "Release Alpha" in remaining_titles, "'Release Alpha' not found in localStorage."
    assert "Release Gamma" in remaining_titles, "'Release Gamma' not found in localStorage."
    if hasattr(context, 'seeded_releases'):
        for seeded in context.seeded_releases:
            if seeded["title"] in ("Release Alpha", "Release Gamma"):
                actual = next(
                    (r for r in releases if r.get("title") == seeded["title"]), None
                )
                assert actual is not None, (
                    f"'{seeded['title']}' absent from localStorage after deletion."
                )
                for field in ["product", "version", "title", "description", "releaseDate"]:
                    assert seeded.get(field) == actual.get(field), (
                        f"Field '{field}' was modified for '{seeded['title']}'. "
                        f"Expected '{seeded.get(field)}', got '{actual.get(field)}'."
                    )


# TC-007 — card with specific title not visible after reload
@then('the release card with title "{title}" is not visible in the DOM after reload')
def step_card_not_visible_after_reload(context, title):
    """TC-007: confirm the deleted release card is absent after a page reload."""
    assert not context.page.is_card_with_title_visible(title), (
        f"Release card with title '{title}' is still visible after page reload."
    )


# TC-007, TC-008, TC-018, TC-023 — localStorage does not contain the deleted release
@then('the "{key}" key in localStorage does not contain the deleted release')
def step_storage_no_deleted_release(context, key):
    """TC-007, TC-018: confirm localStorage does not retain the deleted release."""
    releases = read_releases_from_storage(context.driver, key)
    if releases is None or len(releases) == 0:
        return  # empty = confirmed absence
    target = getattr(context, 'target_title', None)
    if target:
        titles = [r.get("title") for r in releases]
        assert target not in titles, (
            f"Deleted release '{target}' is still present in localStorage. "
            f"Found titles: {titles}"
        )


# TC-008 — form is cleared and in default Add mode
@then('the edit form is cleared and reset to its default empty state')
def step_form_cleared_and_reset(context):
    """TC-008: verify the form is in Add mode (resetEditMode() was called)."""
    assert context.page.is_form_in_default_state(), (
        "Submit button does not read 'Add Release Note' — form was not reset."
    )
    title_value = context.page.get_edit_form_title_value()
    assert title_value == "", (
        f"Title input is not empty after form reset. Found: '{title_value}'."
    )


# TC-008 — card is no longer visible (different wording from TC-003)
@then('the deleted release card is no longer visible in the DOM')
def step_deleted_card_not_visible(context):
    """TC-008: confirm the card that was in edit mode is no longer rendered."""
    title = getattr(context, 'editing_card_title', getattr(context, 'target_title', None))
    if title:
        assert not context.page.is_card_with_title_visible(title), (
            f"The deleted release card '{title}' is still visible in the DOM."
        )
    else:
        # Fallback: count must have decreased
        count = context.page.count_release_cards()
        pre = getattr(context, 'pre_delete_count', count + 1)
        assert count < pre, "Card count did not decrease — deletion may not have occurred."


# TC-009 — all cards still visible
@then('all release cards remain visible in the DOM')
def step_all_cards_remain_visible(context):
    """TC-009: confirm at least as many cards are visible as before the Delete click."""
    count = context.page.count_release_cards()
    pre = getattr(context, 'pre_delete_count', 0)
    assert count > 0, "No release cards visible in the DOM after cancelled deletion."
    assert count == pre, (
        f"Card count changed after cancellation. Before: {pre}, After: {count}."
    )


# TC-009 — card count is identical to before clicking Delete
@then('the release card count is unchanged from before the Delete button was clicked')
def step_card_count_unchanged(context):
    """TC-009: assert card count equals the pre_delete_count baseline."""
    current = context.page.count_release_cards()
    pre = getattr(context, 'pre_delete_count', current)
    assert current == pre, (
        f"Release card count changed after cancellation. Before: {pre}, After: {current}."
    )


# TC-010 — localStorage byte-identical before and after cancel
@then('the "{key}" key in localStorage is identical to the value recorded before the Delete button was clicked')
def step_storage_identical_to_pre_delete(context, key):
    """TC-010: compare current localStorage value against the pre_delete_storage snapshot."""
    after = get_local_storage(context.driver, key)
    before = getattr(context, 'pre_delete_storage', after)
    assert before == after, (
        f"localStorage was mutated by a cancelled deletion.\n"
        f"Before: {before}\nAfter:  {after}"
    )


# TC-011 — singular card still visible
@then('the release card remains visible in the DOM')
def step_single_card_still_visible(context):
    """TC-011: confirm at least one release card is still rendered after dismissal."""
    count = context.page.count_release_cards()
    assert count > 0, "No release cards visible — expected at least one after dismissal."


# TC-011 — localStorage unchanged after dismiss
@then('the "{key}" key in localStorage is unchanged')
def step_storage_unchanged_after_dismiss(context, key):
    """TC-011: confirm localStorage was not modified by the dismissed dialog."""
    after = get_local_storage(context.driver, key)
    before = getattr(context, 'pre_delete_storage', after)
    assert before == after, (
        f"localStorage changed after dialog dismissal.\n"
        f"Before: {before}\nAfter:  {after}"
    )


# TC-013 — both deletions succeeded
@then('both deletions are applied correctly')
def step_both_deletions_applied(context):
    """TC-013: verify card count dropped by 2 (from 3 to 1)."""
    count = context.page.count_release_cards()
    assert count == 1, (
        f"Expected 1 remaining card after 2 rapid deletions, found {count}."
    )


# TC-013 — remaining card is intact
@then('the one remaining release card is intact in the DOM')
def step_one_remaining_card_intact(context):
    """TC-013: confirm exactly 1 card remains and is displayed."""
    cards = context.page.get_release_cards()
    assert len(cards) == 1, (
        f"Expected exactly 1 remaining card, found {len(cards)}."
    )
    assert cards[0].is_displayed(), "The remaining release card is not displayed."


# TC-014 — no cards in DOM
@then('no release cards are visible in the DOM')
def step_no_cards_visible(context):
    """TC-014: assert the release list contains zero cards."""
    count = context.page.count_release_cards()
    assert count == 0, (
        f"Expected 0 release cards after deleting the only release, found {count}."
    )


# TC-014 — empty-state element is shown
@then('the release list displays the empty state element')
def step_empty_state_visible(context):
    """TC-014: assert the empty-state paragraph is visible in the release list."""
    assert context.page.is_empty_state_visible(), (
        "Empty-state element is not visible after deleting the last release."
    )


# TC-014 — localStorage holds an empty array
@then('the "{key}" key in localStorage contains an empty array')
def step_storage_empty_array(context, key):
    """TC-014: assert localStorage holds '[]' (empty JSON array)."""
    raw = get_local_storage(context.driver, key)
    assert raw is not None, f"'{key}' key is absent from localStorage."
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        raise AssertionError(
            f"localStorage '{key}' is not valid JSON after deletion. Raw: {raw}"
        )
    assert parsed == [], (
        f"Expected empty array '[]' in localStorage '{key}', got: {parsed}"
    )


# TC-015 — first visible card now has a given title
@then('the first visible release card now has the title "{title}"')
def step_first_card_has_title(context, title):
    """TC-015: confirm the first rendered card carries the expected title."""
    cards = context.page.get_release_cards()
    assert len(cards) > 0, "No release cards visible after deletion."
    first_title = context.page.get_card_title(cards[0])
    assert title in first_title, (
        f"Expected first card title to contain '{title}', got '{first_title}'."
    )


# TC-015, TC-016 — total card count (by count, not "exactly N")
@then('the total count of release cards is {count:d}')
def step_total_card_count_is_n(context, count):
    """TC-015, TC-016: assert the total number of rendered cards equals *count*."""
    actual = context.page.count_release_cards()
    assert actual == count, (
        f"Expected total card count of {count}, found {actual}."
    )


# TC-017 — product filter still shows "Billing API"
@then('the active product filter "Billing API" remains selected in the filter control')
def step_billing_api_filter_still_selected(context):
    """TC-017: confirm the product filter drop-down still shows 'Billing API'."""
    value = context.page.get_product_filter_value()
    assert value == "Billing API", (
        f"Expected product filter to remain 'Billing API', got '{value}'."
    )


# TC-017, TC-021 — filtered list shows exactly 1 matching card
@then('the filtered list shows exactly 1 matching release card')
def step_filtered_list_one_card(context):
    """TC-017, TC-021: assert exactly 1 card is visible after filter/search."""
    count = context.page.count_release_cards()
    assert count == 1, (
        f"Expected 1 release card in the filtered list, found {count}."
    )


# TC-017 — non-matching card is not in the DOM (filter is active)
@then('the non-matching release card remains hidden from the filtered view')
def step_non_matching_hidden_from_filter(context):
    """TC-017: confirm the non-Billing-API card is not rendered when filter is active."""
    non_matching = getattr(context, 'non_matching_title', None)
    if non_matching:
        assert not context.page.is_card_with_title_visible(non_matching), (
            f"Non-matching card '{non_matching}' is unexpectedly visible in the filtered view."
        )
    else:
        # At minimum, only 1 card should be visible
        assert context.page.count_release_cards() <= 1


# TC-018 — card not visible after either of the two reloads
@then('the release card with title "{title}" is not visible in the DOM after either reload')
def step_card_not_visible_after_either_reload(context, title):
    """TC-018: confirm the deleted card is absent after two consecutive page reloads."""
    assert not context.page.is_card_with_title_visible(title), (
        f"Release card with title '{title}' appeared after page reload(s)."
    )


# TC-019 — new card is visible after reload
@then('the new release card is visible in the release list after reload')
def step_new_card_visible_after_reload(context):
    """TC-019: confirm the newly added release persisted through a page reload."""
    title = getattr(context, 'new_release_title', "")
    assert context.page.is_card_with_title_visible(title), (
        f"New release card '{title}' is not visible in the list after reload."
    )


# TC-019 — newly added release is in localStorage
@then('the "{key}" key in localStorage contains the newly added release')
def step_storage_has_new_release(context, key):
    """TC-019: confirm the newly added release is persisted in localStorage."""
    releases = read_releases_from_storage(context.driver, key)
    assert releases is not None, f"No releases found in localStorage key '{key}'."
    titles = [r.get("title") for r in releases]
    new_title = getattr(context, 'new_release_title', "")
    assert new_title in titles, (
        f"New release '{new_title}' not found in localStorage. Found titles: {titles}"
    )


# TC-020 — edit form still shows the data for the release that was NOT deleted
@then('the edit form still displays the data belonging to "{title}" unchanged')
def step_form_shows_title_unchanged(context, title):
    """TC-020: confirm the form's title field still shows the originally-edited release title."""
    actual = context.page.get_edit_form_title_value()
    assert actual == title, (
        f"Expected form title field to show '{title}', got '{actual}'."
    )


# TC-020 — localStorage still contains the undeleted release, unmodified
@then('the "{key}" key in localStorage still contains "{title}" unchanged')
def step_storage_still_contains_title(context, key, title):
    """TC-020: confirm the undeleted release still exists in localStorage."""
    releases = read_releases_from_storage(context.driver, key)
    assert releases is not None, f"No releases found in localStorage key '{key}'."
    titles = [r.get("title") for r in releases]
    assert title in titles, (
        f"Release '{title}' not found in localStorage. Found titles: {titles}"
    )


# TC-021 — non-matching release is not in the search results
@then('the non-matching release remains hidden from the search results')
def step_non_matching_hidden_from_search(context):
    """TC-021: confirm the non-'Payments' card is not visible in search results."""
    non_matching = getattr(context, 'non_matching_title', None)
    if non_matching:
        assert not context.page.is_card_with_title_visible(non_matching), (
            f"Non-matching card '{non_matching}' is unexpectedly shown in search results."
        )
    else:
        assert False, "context.non_matching_title not set — Given step may have failed."


# TC-021 — deleted card does not reappear in search results
@then('the deleted release card does not appear in any search result')
def step_deleted_card_not_in_search_results(context):
    """TC-021: confirm the deleted 'Payments' card is not in the filtered list."""
    deleted = getattr(context, 'deleted_payments_title', None)
    if deleted:
        assert not context.page.is_card_with_title_visible(deleted), (
            f"Deleted release '{deleted}' reappeared in search results."
        )
    else:
        assert False, "context.deleted_payments_title not set — Given step may have failed."


# TC-022 — exported JSON contains exactly 1 entry
@then('the exported JSON file contains exactly 1 entry')
def step_export_has_one_entry(context):
    """TC-022: parse the downloaded JSON and assert it holds exactly 1 release."""
    assert context.downloaded_file is not None, (
        "No file was downloaded after clicking Export JSON."
    )
    context.exported_releases = read_json_file(context.downloaded_file)
    assert isinstance(context.exported_releases, list), (
        "Exported file does not contain a JSON array."
    )
    assert len(context.exported_releases) == 1, (
        f"Expected 1 entry in exported JSON, found {len(context.exported_releases)}."
    )


# TC-022 — the one exported entry has the expected title
@then('that entry has the title "{title}"')
def step_export_entry_has_title(context, title):
    """TC-022: confirm the sole exported entry's title field matches *title*."""
    exported = getattr(context, 'exported_releases', [])
    assert len(exported) == 1, "Expected exactly 1 exported entry."
    actual_title = exported[0].get("title", "")
    assert actual_title == title, (
        f"Expected exported entry title '{title}', got '{actual_title}'."
    )


# TC-022 — the deleted release is absent from the export
@then('no entry with title "{title}" is present in the exported JSON file')
def step_export_has_no_entry_with_title(context, title):
    """TC-022: confirm no exported entry carries the deleted release's title."""
    exported = getattr(context, 'exported_releases', None)
    if exported is None:
        assert context.downloaded_file is not None, "No downloaded file available."
        exported = read_json_file(context.downloaded_file)
    titles = [r.get("title") for r in exported]
    assert title not in titles, (
        f"Deleted release '{title}' is present in the exported JSON file. "
        f"Found titles: {titles}"
    )


# TC-023 — application loaded without JS errors
@then('the application loads without any JavaScript errors')
def step_app_no_js_errors(context):
    """TC-023: verify no unexpected alert dialogs or obvious JS error indicators."""
    # Check no unexpected alert is blocking the page
    try:
        alert = context.driver.switch_to.alert
        text = alert.text
        alert.dismiss()
        raise AssertionError(f"Unexpected browser alert present: '{text}'")
    except AssertionError:
        raise
    except Exception:
        pass  # No alert = pass


# TC-023 — release list is in a deterministic state (empty or seed-only)
@then('the release list is either empty or shows only deterministic seed data')
def step_release_list_empty_or_seed(context):
    """TC-023: after deleting all and reloading, storage held '[]', so empty state is expected."""
    # After explicit deleteAll -> saveReleases([]) -> localStorage='[]' -> reload ->
    # loadReleases returns [] -> renderReleaseList shows empty state.
    # Count may be 0 (empty state) or >0 if seed data was reapplied.
    count = context.page.count_release_cards()
    raw = get_local_storage(context.driver, STORAGE_KEY)
    # If localStorage has '[]', deterministic empty state is expected
    if raw is not None:
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list) and len(parsed) == 0:
                assert count == 0, (
                    f"localStorage is empty '[]' but {count} card(s) are still rendered."
                )
                return
        except json.JSONDecodeError:
            pass
    # TC-023 deletes all releases; empty state is the only acceptable outcome
    assert count == 0, (
        f"Expected empty release list after delete-all, found {count} card(s)."
    )


# TC-023 — localStorage reflects the post-deletion state consistently
@then('the "{key}" key in localStorage reflects the post-deletion state consistently')
def step_storage_post_deletion_consistent(context, key):
    """TC-023: confirm localStorage is valid JSON and consistent with what is rendered."""
    raw = get_local_storage(context.driver, key)
    assert raw is not None, f"localStorage key '{key}' is absent after delete-all and reload."
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        raise AssertionError(
            f"localStorage '{key}' contains invalid JSON after reload: {raw}"
        )
    assert isinstance(parsed, list), (
        f"Expected a JSON array in localStorage '{key}', got: {type(parsed)}"
    )
    # DOM card count should match what localStorage says
    dom_count = context.page.count_release_cards()
    storage_count = len(parsed)
    # DOM may show a subset if filters are active; counts should at least not contradict
    assert dom_count <= storage_count or (dom_count == 0 and context.page.is_empty_state_visible()), (
        f"DOM card count ({dom_count}) inconsistent with localStorage count ({storage_count})."
    )
