#!/usr/bin/env python3
"""
jira-story-pickup.py
Called by the STLC orchestrator at pipeline start (Step 0).
  1. Gets the authenticated user's Jira account ID via /rest/api/3/myself
  2. Fetches story details
  3. Assigns story to the authenticated user
  4. Transitions story to In Progress
  5. Writes/updates the entry in story_registry.json
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("[jira-story-pickup] 'requests' not installed — skipping Jira pickup", file=sys.stderr)
    sys.exit(0)

SCRIPT_DIR = Path(__file__).parent
MASTER_STLC_DIR = SCRIPT_DIR.parent.parent
ENV_PATH = MASTER_STLC_DIR / ".env"
REGISTRY_PATH = MASTER_STLC_DIR / "artifacts" / "story_registry.json"


def load_env():
    if ENV_PATH.exists():
        with open(ENV_PATH) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip())


def jira_get(base, auth, path):
    r = requests.get(f"{base}/rest/api/3/{path}", auth=auth,
                     headers={"Accept": "application/json"}, timeout=10)
    r.raise_for_status()
    return r.json()


def jira_put(base, auth, path, payload):
    r = requests.put(f"{base}/rest/api/3/{path}", json=payload, auth=auth,
                     headers={"Content-Type": "application/json"}, timeout=10)
    r.raise_for_status()


def jira_post(base, auth, path, payload):
    r = requests.post(f"{base}/rest/api/3/{path}", json=payload, auth=auth,
                      headers={"Content-Type": "application/json"}, timeout=10)
    r.raise_for_status()
    return r.json()


def find_in_progress_transition(transitions):
    keywords = ["in progress", "in-progress", "inprogress", "start", "begin"]
    for t in transitions:
        if any(kw in t.get("name", "").lower() for kw in keywords):
            return t["id"]
    return None


def load_registry():
    if REGISTRY_PATH.exists():
        try:
            return json.loads(REGISTRY_PATH.read_text())
        except Exception:
            pass
    return {"version": "1.0", "stories": {}}


def save_registry(registry):
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--story-id", required=True, help="Jira story key e.g. COD-9")
    parser.add_argument("--branch", default="", help="Current git branch name")
    args = parser.parse_args()

    story_id = args.story_id.upper()

    load_env()
    jira_url  = os.environ.get("JIRA_URL",       "").rstrip("/")
    username  = os.environ.get("JIRA_USERNAME",  "")
    api_token = os.environ.get("JIRA_API_TOKEN", "")
    auth      = (username, api_token)

    if not all([jira_url, username, api_token]):
        print("[jira-story-pickup] Missing Jira credentials — writing registry only", file=sys.stderr)
        registry = load_registry()
        story = registry["stories"].setdefault(story_id, {})
        story.update({
            "status":       "in_progress",
            "branch":       args.branch,
            "started_at":   datetime.now(timezone.utc).isoformat(),
            "jira_subtasks": story.get("jira_subtasks", {}),
            "artifacts":    story.get("artifacts", []),
        })
        save_registry(registry)
        return

    display_name = username
    account_id   = None

    # 1. Get authenticated user's account ID
    try:
        myself       = jira_get(jira_url, auth, "myself")
        account_id   = myself["accountId"]
        display_name = myself.get("displayName", username)
        print(f"[jira-story-pickup] Authenticated as: {display_name} ({account_id})")
    except Exception as e:
        print(f"[jira-story-pickup] Could not get account ID: {e}", file=sys.stderr)

    # 2. Fetch story details
    title          = story_id
    current_status = "unknown"
    try:
        issue          = jira_get(jira_url, auth, f"issue/{story_id}")
        title          = issue["fields"]["summary"]
        current_status = issue["fields"]["status"]["name"]
        print(f"[jira-story-pickup] Story: {story_id} — {title} (status: {current_status})")
    except Exception as e:
        print(f"[jira-story-pickup] Could not fetch story {story_id}: {e}", file=sys.stderr)

    # 3. Assign to current user
    if account_id:
        try:
            jira_put(jira_url, auth, f"issue/{story_id}/assignee", {"accountId": account_id})
            print(f"[jira-story-pickup] Assigned {story_id} to {display_name}")
        except Exception as e:
            print(f"[jira-story-pickup] Could not assign: {e}", file=sys.stderr)

    # 4. Transition to In Progress
    try:
        data        = jira_get(jira_url, auth, f"issue/{story_id}/transitions")
        transitions = data.get("transitions", [])
        tid         = find_in_progress_transition(transitions)
        if tid:
            jira_post(jira_url, auth, f"issue/{story_id}/transitions",
                      {"transition": {"id": tid}})
            print(f"[jira-story-pickup] Transitioned {story_id} to In Progress")
        else:
            available = [t["name"] for t in transitions]
            print(f"[jira-story-pickup] No 'In Progress' transition found. Available: {available}",
                  file=sys.stderr)
    except Exception as e:
        print(f"[jira-story-pickup] Could not transition: {e}", file=sys.stderr)

    # 5. Update story_registry.json
    registry = load_registry()
    story    = registry["stories"].setdefault(story_id, {})
    story.update({
        "title":          title,
        "branch":         args.branch,
        "assignee":       username,
        "assignee_name":  display_name,
        "status":         "in_progress",
        "started_at":     datetime.now(timezone.utc).isoformat(),
        "completed_at":   story.get("completed_at"),
        "merged_at":      story.get("merged_at"),
        "pr_number":      story.get("pr_number"),
        "jira_url":       f"{jira_url}/browse/{story_id}",
        "jira_subtasks":  story.get("jira_subtasks", {}),
        "artifacts":      story.get("artifacts", []),
    })
    save_registry(registry)
    print(f"[jira-story-pickup] Registry updated: {story_id} → in_progress")


if __name__ == "__main__":
    main()
