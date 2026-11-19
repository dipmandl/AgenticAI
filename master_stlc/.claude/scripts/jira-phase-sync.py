#!/usr/bin/env python3
"""
jira-phase-sync.py
PostToolUse hook — fires after every Write tool call.
When the written file is a recognized phase artifact under artifacts/COD-*/,
creates a Jira subtask on the parent story and updates story_registry.json.

Claude Code passes hook data via stdin as JSON:
  {
    "tool_name": "Write",
    "tool_input": {"file_path": "...", "content": "..."},
    "tool_response": {...}
  }
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit(0)

SCRIPT_DIR      = Path(__file__).parent
MASTER_STLC_DIR = SCRIPT_DIR.parent.parent
ENV_PATH        = MASTER_STLC_DIR / ".env"
REGISTRY_PATH   = MASTER_STLC_DIR / "artifacts" / "story_registry.json"

# Phase folder → (exact trigger filename or None for any .md, label prefix)
PHASE_MAP = {
    "discovery":    ("repository-discovery.md",  "[DISCOVERY]"),
    "requirements": ("requirement-analysis.md",  "[REQ]"),
    "impact":       ("impact-analysis.md",        "[IMPACT]"),
    "test-plans":   ("test-plan.md",              "[TEST PLAN]"),
    "test-cases":   ("test-case-inventory.md",    "[TEST CASES]"),
    "execution":    ("execution-summary.md",      "[EXECUTION]"),
    "defects":      (None,                        "[DEFECT]"),   # any DEF-NNN.md
    "reports":      ("final-stlc-report.md",      "[REPORT]"),
}

# Matches: ...artifacts/COD-9/requirements/requirement-analysis.md
ARTIFACT_RE = re.compile(
    r"artifacts[/\\](COD-\d+)[/\\]([^/\\]+)[/\\]([^/\\]+)$",
    re.IGNORECASE,
)


def load_env():
    if ENV_PATH.exists():
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip())


def extract_title(content, fallback):
    for line in (content or "").splitlines():
        line = line.strip()
        if line.startswith("#"):
            return line.lstrip("#").strip()[:120]
    return fallback


def get_account_id(base, auth):
    r = requests.get(f"{base}/rest/api/3/myself", auth=auth, timeout=10)
    r.raise_for_status()
    return r.json()["accountId"]


def create_subtask(base, auth, parent_key, summary, description, account_id):
    project_key = parent_key.split("-")[0]
    payload = {
        "fields": {
            "project":     {"key": project_key},
            "parent":      {"key": parent_key},
            "issuetype":   {"name": "Subtask"},
            "summary":     summary[:255],
            "description": {
                "type": "doc", "version": 1,
                "content": [{
                    "type": "paragraph",
                    "content": [{"type": "text", "text": description}]
                }],
            },
            "assignee":    {"accountId": account_id},
            "labels":      ["stlc-generated"],
        }
    }
    r = requests.post(
        f"{base}/rest/api/3/issue",
        json=payload, auth=auth,
        headers={"Content-Type": "application/json"},
        timeout=15,
    )
    r.raise_for_status()
    data = r.json()
    return data["key"], f"{base}/browse/{data['key']}"


def update_registry(story_id, phase_folder, file_name, subtask_key, subtask_url):
    registry = {}
    if REGISTRY_PATH.exists():
        try:
            registry = json.loads(REGISTRY_PATH.read_text())
        except Exception:
            pass

    story    = registry.setdefault("stories", {}).setdefault(story_id, {})
    subtasks = story.setdefault("jira_subtasks", {})
    label    = file_name if phase_folder == "defects" else phase_folder
    subtasks[label] = {
        "key":        subtask_key,
        "url":        subtask_url,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    artifacts = story.setdefault("artifacts", [])
    if phase_folder not in artifacts:
        artifacts.append(phase_folder)

    REGISTRY_PATH.write_text(json.dumps(registry, indent=2))


def main():
    # Read hook input
    try:
        hook_data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if hook_data.get("tool_name") != "Write":
        sys.exit(0)

    file_path = hook_data.get("tool_input", {}).get("file_path", "")
    content   = hook_data.get("tool_input", {}).get("content", "")

    match = ARTIFACT_RE.search(file_path.replace("\\", "/"))
    if not match:
        sys.exit(0)

    story_id     = match.group(1).upper()
    phase_folder = match.group(2)
    file_name    = match.group(3)

    if phase_folder not in PHASE_MAP:
        sys.exit(0)

    expected_file, prefix = PHASE_MAP[phase_folder]
    if expected_file and file_name != expected_file:
        sys.exit(0)

    # Credentials
    load_env()
    jira_url  = os.environ.get("JIRA_URL",       "").rstrip("/")
    username  = os.environ.get("JIRA_USERNAME",  "")
    api_token = os.environ.get("JIRA_API_TOKEN", "")
    auth      = (username, api_token)

    if not all([jira_url, username, api_token]):
        print("[jira-phase-sync] Missing credentials — skipping", file=sys.stderr)
        sys.exit(0)

    try:
        account_id = get_account_id(jira_url, auth)
    except Exception as e:
        print(f"[jira-phase-sync] account ID lookup failed: {e}", file=sys.stderr)
        sys.exit(0)

    artifact_title = extract_title(content, f"{phase_folder} artifact")
    summary        = f"{prefix} {story_id} — {artifact_title}"
    description    = (
        f"STLC pipeline artifact\n"
        f"Story:     {story_id}\n"
        f"Phase:     {phase_folder}\n"
        f"File:      {file_path}\n"
        f"Generated: {datetime.now(timezone.utc).isoformat()}"
    )

    try:
        key, url = create_subtask(jira_url, auth, story_id, summary, description, account_id)
        print(f"[jira-phase-sync] Created {key}: {summary}")
    except Exception as e:
        print(f"[jira-phase-sync] subtask creation failed: {e}", file=sys.stderr)
        sys.exit(0)

    try:
        update_registry(story_id, phase_folder, file_name, key, url)
    except Exception as e:
        print(f"[jira-phase-sync] registry update failed: {e}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
