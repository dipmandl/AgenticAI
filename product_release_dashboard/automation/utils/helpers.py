"""
Shared test helpers for COD-9 automation.

Covers:
- localStorage read/write via Selenium execute_script
- Download directory polling
- Release object schema validation
- Test data factories
"""

import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional

from jsonschema import validate, ValidationError
from selenium.webdriver.remote.webdriver import WebDriver

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

STORAGE_KEY = "releaseNotesDashboard.releases"

RELEASE_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["id", "product", "version", "title", "description", "releaseDate", "isBreaking"],
        "properties": {
            "id":          {"type": "string"},
            "product":     {"type": "string"},
            "version":     {"type": "string"},
            "teamName":    {"type": ["string", "null"]},
            "title":       {"type": "string"},
            "description": {"type": "string"},
            "releaseDate": {"type": "string"},
            "isBreaking":  {"type": "boolean"},
        },
        "additionalProperties": True,
    },
}

# ---------------------------------------------------------------------------
# localStorage helpers
# ---------------------------------------------------------------------------

def get_local_storage(driver: WebDriver, key: str = STORAGE_KEY) -> Optional[str]:
    """Return the raw string value stored at *key*, or None if absent."""
    return driver.execute_script(
        "return localStorage.getItem(arguments[0]);", key
    )


def set_local_storage(driver: WebDriver, releases: List[Dict], key: str = STORAGE_KEY) -> None:
    """Serialise *releases* and write to localStorage at *key*."""
    driver.execute_script(
        "localStorage.setItem(arguments[0], arguments[1]);",
        key,
        json.dumps(releases),
    )


def set_local_storage_raw(driver: WebDriver, raw: str, key: str = STORAGE_KEY) -> None:
    """Write a raw string to localStorage (used for corrupted-value tests)."""
    driver.execute_script(
        "localStorage.setItem(arguments[0], arguments[1]);", key, raw
    )


def clear_local_storage(driver: WebDriver) -> None:
    """Remove all localStorage entries."""
    driver.execute_script("localStorage.clear();")


def remove_local_storage_key(driver: WebDriver, key: str = STORAGE_KEY) -> None:
    """Remove a specific key from localStorage."""
    driver.execute_script("localStorage.removeItem(arguments[0]);", key)


def read_releases_from_storage(driver: WebDriver, key: str = STORAGE_KEY) -> Optional[List[Dict]]:
    """Return the parsed JSON array from localStorage, or None if absent/invalid."""
    raw = get_local_storage(driver, key)
    if raw is None:
        return None
    try:
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, list) else None
    except json.JSONDecodeError:
        return None


# ---------------------------------------------------------------------------
# Download helpers
# ---------------------------------------------------------------------------

def wait_for_download(download_dir: str, extension: str = ".json", timeout: int = 15) -> Optional[str]:
    """
    Poll *download_dir* until a file with *extension* appears (or *timeout* elapses).

    Returns the absolute path of the first matching file, or None on timeout.
    Chrome writes a .crdownload temporary file while downloading; we wait
    until that is gone before returning.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        candidates = [
            f for f in os.listdir(download_dir)
            if f.endswith(extension) and not f.endswith(".crdownload")
        ]
        if candidates:
            return os.path.join(download_dir, candidates[0])
        time.sleep(0.4)
    return None


def get_latest_download(download_dir: str) -> Optional[str]:
    """Return the most-recently-modified file in *download_dir*, or None."""
    try:
        files = [
            os.path.join(download_dir, f)
            for f in os.listdir(download_dir)
            if os.path.isfile(os.path.join(download_dir, f))
        ]
        if not files:
            return None
        return max(files, key=os.path.getmtime)
    except OSError:
        return None


def read_json_file(path: str) -> Any:
    """Read and parse a JSON file; raises ValueError on decode errors."""
    with open(path, "r", encoding="utf-8") as fh:
        try:
            return json.load(fh)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Downloaded file is not valid JSON: {exc}") from exc


def read_raw_file(path: str) -> str:
    """Read the raw text content of a file."""
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Schema validation
# ---------------------------------------------------------------------------

def validate_release_schema(releases: Any) -> None:
    """Raise AssertionError if *releases* does not conform to RELEASE_SCHEMA."""
    try:
        validate(instance=releases, schema=RELEASE_SCHEMA)
    except ValidationError as exc:
        raise AssertionError(f"Schema validation failed: {exc.message}") from exc


def releases_are_equal(expected: List[Dict], actual: List[Dict]) -> bool:
    """
    Compare two release lists for structural and content equality.
    Order-sensitive; ignores extra keys that may be added by the app.
    """
    if len(expected) != len(actual):
        return False
    for exp, act in zip(expected, actual):
        for field in ["id", "product", "version", "title", "description", "releaseDate", "isBreaking"]:
            if exp.get(field) != act.get(field):
                return False
    return True


# ---------------------------------------------------------------------------
# Test data factories
# ---------------------------------------------------------------------------

def make_release(
    index: int = 1,
    product: str = "Test Product",
    version: str = "v1.0.0",
    team_name: str = "Test Team",
    title: str = "Test Release",
    description: str = "Test description.",
    release_date: str = "2026-01-01",
    is_breaking: bool = False,
) -> Dict:
    """Return a single release object with a deterministic id."""
    return {
        "id": f"test-{index:04d}",
        "product": product,
        "version": version,
        "teamName": team_name,
        "title": title,
        "description": description,
        "releaseDate": release_date,
        "isBreaking": is_breaking,
    }


def make_releases(count: int) -> List[Dict]:
    """Generate *count* distinct release objects."""
    return [
        make_release(
            index=i + 1,
            product=f"Product {i + 1}",
            version=f"v{i + 1}.0.0",
            title=f"Release {i + 1}",
            description=f"Description for release {i + 1}.",
            release_date="2026-01-01",
        )
        for i in range(count)
    ]


def make_single_known_release() -> Dict:
    """Return the canonical single-release object used in TC-007."""
    return make_release(
        index=1,
        product="Alpha Product",
        version="v1.0.0",
        team_name="Alpha Team",
        title="Alpha Release",
        description="First release of Alpha Product.",
        release_date="2026-03-15",
        is_breaking=False,
    )


def make_five_known_releases() -> List[Dict]:
    """Return the canonical 5-release list used in TC-008."""
    return [
        make_release(i + 1, product=f"Prod{i + 1}", version=f"v{i + 1}.0.0",
                     title=f"Title {i + 1}", description=f"Desc {i + 1}.",
                     release_date=f"2026-0{i + 1}-01")
        for i in range(5)
    ]


def make_release_with_special_chars() -> Dict:
    """Return a release whose title/description contain special characters (TC-019)."""
    return make_release(
        index=1,
        title='Title with "quotes", newline\nand\ttab',
        description='Description with "quotes" and special chars.',
    )


def make_release_with_unicode() -> Dict:
    """Return a release whose fields include Chinese, Arabic, and emoji (TC-020)."""
    return make_release(
        index=1,
        title="中文标题 عنوان \U0001f680",
        description="中文描述 وصف \U0001f4e6",
    )
