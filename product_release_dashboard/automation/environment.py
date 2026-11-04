"""
Behave environment hooks — browser lifecycle management for COD-9 automation.

Story: COD-9 — Export Release Notes to JSON File
App:   file:///C:/Users/DipakMandlik/Desktop/AgenticAI/Final_implementation/AgenticAI/
       product_release_dashboard/index.html
"""

import os

from selenium import webdriver
from selenium.webdriver.edge.options import Options

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

APP_URL = (
    "file:///C:/Users/DipakMandlik/Desktop/AgenticAI/Final_implementation/"
    "AgenticAI/product_release_dashboard/index.html"
)
STORAGE_KEY = "releaseNotesDashboard.releases"


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------

def before_all(context):
    """Create a shared temp download directory; instantiate the Edge driver."""
    context.download_dir = os.path.join(
        os.path.dirname(__file__), "reports", "downloads"
    )
    os.makedirs(context.download_dir, exist_ok=True)

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    # Allow file:// access to localStorage
    options.add_argument("--allow-file-access-from-files")

    prefs = {
        "download.default_directory": os.path.abspath(context.download_dir),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,
        "safebrowsing.disable_download_protection": True,
    }
    options.add_experimental_option("prefs", prefs)

    # Use selenium-manager (bundled with selenium 4.15) to resolve msedgedriver from cache
    context.driver = webdriver.Edge(options=options)
    context.driver.set_window_size(1280, 900)

    # Expose constants on context for step definitions
    context.app_url = APP_URL
    context.storage_key = STORAGE_KEY


def before_scenario(context, scenario):
    """Open the application and clear localStorage before each scenario."""
    context.driver.get(context.app_url)
    context.driver.execute_script("localStorage.clear();")
    # Allow the page to settle after clearing storage
    context.driver.get(context.app_url)

    # Clean up any leftover downloads from a previous scenario
    _clean_download_dir(context.download_dir)

    # Reset per-scenario state
    context.downloaded_file = None
    context.pre_export_storage = None


def after_step(context, step):
    """Capture a screenshot on step failure for debugging."""
    if step.status == "failed":
        screenshots_dir = os.path.join(os.path.dirname(__file__), "reports", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        safe_name = context.scenario.name.replace(" ", "_").replace("/", "_")[:80]
        path = os.path.join(screenshots_dir, f"{safe_name}.png")
        context.driver.save_screenshot(path)


def after_all(context):
    """Quit the browser after the full test run."""
    if hasattr(context, "driver") and context.driver:
        context.driver.quit()


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _clean_download_dir(download_dir: str) -> None:
    """Remove all files from the download directory."""
    if not os.path.isdir(download_dir):
        return
    for fname in os.listdir(download_dir):
        fpath = os.path.join(download_dir, fname)
        try:
            os.remove(fpath)
        except OSError:
            pass
