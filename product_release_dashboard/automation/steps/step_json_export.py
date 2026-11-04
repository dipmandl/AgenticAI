"""
Step definitions for:
  features/json_export/export_release_note.feature

Story:    COD-9 — Export Release Notes to JSON File
REQ-IDs:  REQ-001, REQ-002, REQ-003, REQ-004, REQ-005

Traceability:
  @TC-001 @REQ-001  — Export JSON button is visible on page load
  @TC-002 @REQ-002  — Clicking Export JSON triggers a file download
  @TC-003 @REQ-002  — Downloaded file has a .json extension
  @TC-004 @REQ-002 @REQ-003  — Downloaded file contains valid parseable JSON
  @TC-005 @REQ-003  — Exported JSON schema matches localStorage releases schema
  @TC-006 @REQ-004  — Export with empty localStorage downloads an empty array
  @TC-007 @REQ-002 @REQ-003  — Export with single release entry
  @TC-008 @REQ-002 @REQ-003  — Export with multiple release entries
  @TC-009 @REQ-004  — Empty localStorage does not skip the download
  @TC-010 @REQ-002 @REQ-005  — Export does not mutate localStorage
  @TC-012 @REQ-004  — Export when localStorage key is absent
  @TC-014 @REQ-001  — Export button not duplicated after page reload
  @TC-015 @REQ-004  — Zero releases — lower bound boundary
  @TC-016 @REQ-002 @REQ-003  — One release — single element boundary
  @TC-017 @REQ-002 @REQ-003  — Large dataset — 100 release notes
  @TC-018 @REQ-002 @REQ-003  — Stress boundary — 1000 release notes
  @TC-019 @REQ-003  — Special characters correctly escaped
  @TC-020 @REQ-003  — Unicode characters preserved

Skipped (manual_only): TC-011, TC-013, TC-021, TC-022
"""

import json
import os

from behave import given, when, then

from pages.release_dashboard_page import ReleaseDashboardPage
from utils.helpers import (
    clear_local_storage,
    get_local_storage,
    make_five_known_releases,
    make_release,
    make_releases,
    make_release_with_special_chars,
    make_release_with_unicode,
    make_single_known_release,
    read_json_file,
    read_raw_file,
    read_releases_from_storage,
    releases_are_equal,
    remove_local_storage_key,
    set_local_storage,
    validate_release_schema,
    wait_for_download,
    STORAGE_KEY,
)


# ---------------------------------------------------------------------------
# Background steps
# ---------------------------------------------------------------------------

@given('the user has opened the application in the browser')
def step_open_app(context):
    """TC-001 … TC-022 background: navigate to the app."""
    context.page = ReleaseDashboardPage(context.driver)
    context.page.navigate(context.app_url)


@given('the application storage key is "{key}"')
def step_verify_storage_key(context, key):
    """Confirm the storage key constant matches what the feature file specifies."""
    assert key == STORAGE_KEY, (
        f"Storage key mismatch: expected '{STORAGE_KEY}', got '{key}'"
    )


# ---------------------------------------------------------------------------
# Given — localStorage state setup
# ---------------------------------------------------------------------------

@given('the "{key}" key in localStorage contains at least 1 release note')
def step_storage_has_at_least_one(context, key):
    set_local_storage(context.driver, [make_release(1)], key)
    context.driver.get(context.app_url)


@given('the "{key}" key in localStorage contains release objects with fields "id", "product", "version", "title", "description", "releaseDate", and "isBreaking"')
def step_storage_has_full_schema_releases(context, key):
    context.seeded_releases = [make_single_known_release()]
    set_local_storage(context.driver, context.seeded_releases, key)
    context.driver.get(context.app_url)


@given('the "{key}" key in localStorage has been cleared')
def step_storage_cleared(context, key):
    clear_local_storage(context.driver)
    context.driver.get(context.app_url)


@given('the "{key}" key in localStorage contains exactly 1 release note with known field values')
def step_storage_exactly_one_known(context, key):
    context.seeded_releases = [make_single_known_release()]
    set_local_storage(context.driver, context.seeded_releases, key)
    context.driver.get(context.app_url)


@given('the "{key}" key in localStorage contains 5 release notes with known field values')
def step_storage_five_known(context, key):
    context.seeded_releases = make_five_known_releases()
    set_local_storage(context.driver, context.seeded_releases, key)
    context.driver.get(context.app_url)


@given('the "{key}" key in localStorage contains 3 release notes')
def step_storage_three(context, key):
    context.seeded_releases = make_releases(3)
    set_local_storage(context.driver, context.seeded_releases, key)
    context.driver.get(context.app_url)


@given('the releases data is recorded before clicking Export')
def step_record_pre_export(context):
    raw = get_local_storage(context.driver, STORAGE_KEY)
    context.pre_export_storage = raw


@given('the "{key}" key has never been set in localStorage')
def step_key_never_set(context, key):
    remove_local_storage_key(context.driver, key)
    context.driver.get(context.app_url)


@given('the application is loaded')
def step_app_loaded(context):
    context.page = ReleaseDashboardPage(context.driver)
    context.page.navigate(context.app_url)


@given('the "{key}" key in localStorage contains exactly 1 release note')
def step_storage_exactly_one(context, key):
    set_local_storage(context.driver, [make_release(1)], key)
    context.driver.get(context.app_url)


@given('the "{key}" key in localStorage contains 100 release notes')
def step_storage_100(context, key):
    set_local_storage(context.driver, make_releases(100), key)
    context.driver.get(context.app_url)


@given('the "{key}" key in localStorage contains 1000 release notes')
def step_storage_1000(context, key):
    set_local_storage(context.driver, make_releases(1000), key)
    context.driver.get(context.app_url)


@given('the "{key}" key in localStorage contains a release note whose title includes double-quote characters, newline characters, and tab characters')
def step_storage_special_chars(context, key):
    context.seeded_releases = [make_release_with_special_chars()]
    set_local_storage(context.driver, context.seeded_releases, key)
    context.driver.get(context.app_url)


@given('the "{key}" key in localStorage contains a release note whose title and description include Chinese, Arabic, and emoji Unicode characters')
def step_storage_unicode(context, key):
    context.seeded_releases = [make_release_with_unicode()]
    set_local_storage(context.driver, context.seeded_releases, key)
    context.driver.get(context.app_url)


# ---------------------------------------------------------------------------
# When — user actions
# ---------------------------------------------------------------------------

@when('the user views the dashboard')
def step_view_dashboard(context):
    # Page is already open; simply ensure release-list is visible
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.ID, "release-list"))
    )


@when('the user clicks the "Export JSON" button')
def step_click_export_json(context):
    context.page.click_export_json()
    # Wait for the download to land
    context.downloaded_file = wait_for_download(context.download_dir, extension=".json")


@when('the user reloads the page')
def step_reload_page(context):
    context.page.reload()


# ---------------------------------------------------------------------------
# Then — assertions
# ---------------------------------------------------------------------------

# TC-001
@then('an "Export JSON" button is visible in the dashboard UI')
def step_export_btn_visible(context):
    assert context.page.is_export_json_button_visible(), (
        "Export JSON button is not visible on the dashboard."
    )


# TC-002
@then('the browser initiates a file download')
def step_download_initiated(context):
    assert context.downloaded_file is not None, (
        "No file was downloaded after clicking Export JSON button."
    )


# TC-003
@then('the downloaded file name ends with ".json"')
def step_file_ends_json(context):
    assert context.downloaded_file is not None, "No file was downloaded."
    assert context.downloaded_file.endswith(".json"), (
        f"Downloaded file does not have .json extension: {context.downloaded_file}"
    )


# TC-004 (part 1)
@then('the downloaded file can be parsed as valid JSON without error')
def step_file_is_valid_json(context):
    assert context.downloaded_file is not None, "No file was downloaded."
    context.parsed_json = read_json_file(context.downloaded_file)


# TC-004 (part 2)
@then('the parsed result is a JSON array')
def step_parsed_is_array(context):
    assert isinstance(context.parsed_json, list), (
        f"Expected a JSON array but got: {type(context.parsed_json)}"
    )


# TC-005
@then('the parsed JSON array from the downloaded file is structurally and content-equal to the releases array in localStorage')
def step_json_matches_storage(context):
    assert context.downloaded_file is not None, "No file was downloaded."
    downloaded = read_json_file(context.downloaded_file)
    assert isinstance(downloaded, list), "Downloaded JSON is not an array."
    validate_release_schema(downloaded)
    assert releases_are_equal(context.seeded_releases, downloaded), (
        "Downloaded JSON content does not match localStorage data.\n"
        f"Expected: {context.seeded_releases}\n"
        f"Actual:   {downloaded}"
    )


# TC-006
@then('the downloaded file contains exactly "[]"')
def step_file_contains_empty_array(context):
    assert context.downloaded_file is not None, "No file was downloaded."
    raw = read_raw_file(context.downloaded_file).strip()
    parsed = json.loads(raw)
    assert parsed == [], f"Expected empty array [], got: {raw}"


# TC-007 (part 1)
@then('the downloaded file contains a JSON array with exactly 1 element')
def step_array_has_one_element(context):
    assert context.downloaded_file is not None, "No file was downloaded."
    context.parsed_json = read_json_file(context.downloaded_file)
    assert isinstance(context.parsed_json, list), "Downloaded JSON is not an array."
    assert len(context.parsed_json) == 1, (
        f"Expected 1 element in downloaded array, found {len(context.parsed_json)}"
    )


# TC-007 (part 2)
@then('that element matches the seeded release note in all fields')
def step_element_matches_seeded(context):
    assert releases_are_equal(context.seeded_releases, context.parsed_json), (
        f"Downloaded release does not match seeded data.\n"
        f"Expected: {context.seeded_releases}\nActual: {context.parsed_json}"
    )


# TC-008 (part 1)
@then('the downloaded file contains a JSON array with exactly 5 elements')
def step_array_has_five_elements(context):
    assert context.downloaded_file is not None, "No file was downloaded."
    context.parsed_json = read_json_file(context.downloaded_file)
    assert isinstance(context.parsed_json, list), "Downloaded JSON is not an array."
    assert len(context.parsed_json) == 5, (
        f"Expected 5 elements, found {len(context.parsed_json)}"
    )


# TC-008 (part 2)
@then('each element matches the corresponding seeded release note in order and content')
def step_all_elements_match(context):
    assert releases_are_equal(context.seeded_releases, context.parsed_json), (
        "One or more downloaded releases do not match the seeded data."
    )


# TC-009 (part 1) — reuses 'the browser initiates a file download'
@then('a file download is triggered')
def step_file_download_triggered(context):
    assert context.downloaded_file is not None, (
        "No file was downloaded after clicking Export JSON."
    )


# TC-009 (part 2)
@then('the downloaded file contains "[]"')
def step_downloaded_contains_empty_array(context):
    assert context.downloaded_file is not None, "No file was downloaded."
    raw = read_raw_file(context.downloaded_file).strip()
    parsed = json.loads(raw)
    assert parsed == [], f"Expected empty array [], got: {raw}"


# TC-010 (part 1)
@then('the "{key}" key in localStorage is identical to the pre-export state')
def step_storage_unchanged(context, key):
    after = get_local_storage(context.driver, key)
    assert context.pre_export_storage == after, (
        "localStorage was mutated by the Export action.\n"
        f"Before: {context.pre_export_storage}\nAfter:  {after}"
    )


# TC-010 (part 2)
@then('no entries have been added, removed, or modified')
def step_no_entries_changed(context):
    after = read_releases_from_storage(context.driver)
    assert releases_are_equal(context.seeded_releases, after), (
        "Release entries changed after export."
    )


# TC-014
@then('exactly one "Export JSON" button is present in the DOM')
def step_exactly_one_export_btn(context):
    count = context.page.count_export_json_buttons()
    assert count == 1, (
        f"Expected exactly 1 Export JSON button, found {count}"
    )


# TC-015
@then('the downloaded JSON file contains an array of length 0')
def step_array_length_zero(context):
    assert context.downloaded_file is not None, "No file was downloaded."
    parsed = read_json_file(context.downloaded_file)
    assert isinstance(parsed, list) and len(parsed) == 0, (
        f"Expected empty array, got: {parsed}"
    )


# TC-016 (part 1)
@then('the downloaded JSON file contains an array of exactly 1 element')
def step_array_length_one(context):
    assert context.downloaded_file is not None, "No file was downloaded."
    context.parsed_json = read_json_file(context.downloaded_file)
    assert isinstance(context.parsed_json, list) and len(context.parsed_json) == 1, (
        f"Expected array with 1 element, got length {len(context.parsed_json)}"
    )


# TC-016 (part 2)
@then('that element conforms to the release object schema')
def step_element_conforms_schema(context):
    validate_release_schema(context.parsed_json)


# TC-017 (part 1)
@then('the downloaded JSON file contains all 100 elements without truncation')
def step_array_length_100(context):
    assert context.downloaded_file is not None, "No file was downloaded."
    context.parsed_json = read_json_file(context.downloaded_file)
    assert isinstance(context.parsed_json, list) and len(context.parsed_json) == 100, (
        f"Expected 100 elements, got {len(context.parsed_json)}"
    )


# TC-017 (part 2) and TC-018 (part 3)
@then('the downloaded file is valid JSON')
def step_downloaded_is_valid_json(context):
    assert context.downloaded_file is not None, "No file was downloaded."
    # If not already parsed, parse now
    if not hasattr(context, "parsed_json") or context.parsed_json is None:
        context.parsed_json = read_json_file(context.downloaded_file)
    assert isinstance(context.parsed_json, list), "Downloaded content is not a JSON array."


# TC-018 (part 1)
@then('the downloaded JSON file contains all 1000 elements')
def step_array_length_1000(context):
    assert context.downloaded_file is not None, "No file was downloaded."
    context.parsed_json = read_json_file(context.downloaded_file)
    assert isinstance(context.parsed_json, list) and len(context.parsed_json) == 1000, (
        f"Expected 1000 elements, got {len(context.parsed_json)}"
    )


# TC-018 (part 2)
@then('the export completes without a browser error')
def step_no_browser_error(context):
    # Verify no JS error dialogs / alerts are present
    try:
        alert = context.driver.switch_to.alert
        text = alert.text
        alert.dismiss()
        raise AssertionError(f"Unexpected browser alert: {text}")
    except Exception as exc:
        if "Unexpected browser alert" in str(exc):
            raise
        # No alert — pass


# TC-019 (part 1) — reuses 'the downloaded file is valid and parseable JSON'
@then('the downloaded file is valid and parseable JSON')
def step_downloaded_valid_parseable(context):
    assert context.downloaded_file is not None, "No file was downloaded."
    context.parsed_json = read_json_file(context.downloaded_file)
    assert isinstance(context.parsed_json, list), "Expected a JSON array."


# TC-019 (part 2)
@then('the special characters are correctly JSON-escaped in the file')
def step_special_chars_escaped(context):
    # If file is parseable (already checked), the characters were correctly escaped
    raw = read_raw_file(context.downloaded_file)
    # The raw bytes must be valid JSON — json.loads will raise if not
    parsed = json.loads(raw)
    assert isinstance(parsed, list) and len(parsed) > 0


# TC-019 (part 3)
@then('parsing the file recovers the original special characters intact')
def step_special_chars_recovered(context):
    parsed = context.parsed_json
    original = context.seeded_releases[0]
    actual_title = parsed[0]["title"]
    expected_title = original["title"]
    assert actual_title == expected_title, (
        f"Special characters not preserved.\nExpected: {repr(expected_title)}\n"
        f"Actual:   {repr(actual_title)}"
    )


# TC-020 (part 1) — reuses 'the downloaded file is valid UTF-8 JSON'
@then('the downloaded file is valid UTF-8 JSON')
def step_downloaded_utf8_json(context):
    assert context.downloaded_file is not None, "No file was downloaded."
    with open(context.downloaded_file, "r", encoding="utf-8") as fh:
        context.parsed_json = json.load(fh)
    assert isinstance(context.parsed_json, list), "Expected a JSON array."


# TC-020 (part 2)
@then('all Unicode characters are preserved intact after parsing the downloaded file')
def step_unicode_preserved(context):
    original_title = context.seeded_releases[0]["title"]
    original_desc  = context.seeded_releases[0]["description"]
    actual_title   = context.parsed_json[0]["title"]
    actual_desc    = context.parsed_json[0]["description"]
    assert actual_title == original_title, (
        f"Unicode title mismatch.\nExpected: {repr(original_title)}\nActual:   {repr(actual_title)}"
    )
    assert actual_desc == original_desc, (
        f"Unicode description mismatch.\nExpected: {repr(original_desc)}\nActual:   {repr(actual_desc)}"
    )
