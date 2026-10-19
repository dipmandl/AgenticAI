"""
conftest.py — Shared fixtures and helpers for Release Notes Dashboard automation.

Requirement : REQ-001 — Inline Form Validation for Release Notes Dashboard
Suite       : TC-001 – TC-024

Prerequisites
-------------
The application must be served via HTTP before running the suite:

    python -m http.server 8080 --directory product_release_dashboard

Tests connect to: http://localhost:8080

Fixture design
--------------
page  — self-contained; manages its own Playwright browser lifecycle using
        sync_playwright() so there is no dependency on the pytest-playwright
        plugin's session-scoped playwright fixture.

Setup sequence inside page fixture:
  1. Launch headless Chromium.
  2. Create a fresh BrowserContext and Page.
  3. Navigate to BASE_URL — on a clean context localStorage is empty, so the
     app calls seedData() and writes 2 entries.
  4. Explicitly clear localStorage (guarantees a known clean state even when
     an earlier test in the session left data behind).
  5. Reload — the app detects an empty localStorage key and calls seedData()
     again, writing exactly 2 entries.
  6. Wait for networkidle so that all rendering is complete before yielding.

Seed state at test start (guaranteed by every page fixture invocation)
----------------------------------------------------------------------
  localStorage["releaseNotesDashboard.releases"] contains:
    [0]  product="Billing API",  version="v1.4.0"
    [1]  product="Auth Service", version="v2.0.0"
  Total entries: 2
  Total release cards visible: 2
"""

import pytest
from playwright.sync_api import sync_playwright, expect  # noqa: F401 — expect re-exported for tests

# ── Constants ─────────────────────────────────────────────────────────────────

BASE_URL = "http://localhost:8080"
LS_KEY   = "releaseNotesDashboard.releases"
LS_READ  = f"JSON.parse(localStorage.getItem('{LS_KEY}') || '[]')"
FIELDS   = ["product", "version", "title", "description", "releaseDate"]


# ── Session-scoped fixtures ───────────────────────────────────────────────────

@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL of the running application."""
    return BASE_URL


# ── Function-scoped fixtures ──────────────────────────────────────────────────

@pytest.fixture(scope="function")
def page():
    """
    Provide a fully isolated Page for each test.

    The fixture manages the entire Playwright lifecycle — browser, context, and
    page — so that no state leaks between tests via the browser-level storage.
    Each test starts with exactly 2 seed entries in localStorage.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        pg = context.new_page()
        pg.goto(BASE_URL)
        pg.evaluate("() => localStorage.clear()")
        pg.reload()
        pg.wait_for_load_state("networkidle")
        yield pg
        context.close()
        browser.close()


# ── Plain helper (not a fixture) ──────────────────────────────────────────────

def fill_valid_form(page) -> None:
    """
    Fill all five required form fields with generic valid data.

    Use this helper when the specific field values are not important to the
    test assertion (e.g., to reach a known pre-condition quickly).  Tests
    that assert on specific product/version values should fill fields directly.
    """
    page.fill("#product",     "Test Product")
    page.fill("#version",     "v1.0.0")
    page.fill("#title",       "Test Release Title")
    page.fill("#description", "A valid description for the test release.")
    page.fill("#releaseDate", "2026-09-24")
