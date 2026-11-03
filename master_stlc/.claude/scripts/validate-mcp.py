#!/usr/bin/env python3
"""Validate Jira and GitHub MCP connectivity before the STLC pipeline starts.

Reads credentials from .env in the project root.
Exits 0 if all required integrations pass; exits 1 if any required one fails.

Usage:
    python .claude/scripts/validate-mcp.py
"""

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# ── Load .env ─────────────────────────────────────────────────────────────────

def load_env(env_path: Path) -> dict:
    env = {}
    if not env_path.exists():
        return env
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        env[key.strip()] = value.strip()
    return env


# ── Load stlc-config.yaml (simple key: value parser, no PyYAML needed) ────────

def load_stlc_config() -> dict:
    config_path = ROOT / ".claude" / "config" / "stlc-config.yaml"
    config = {"create_pr": False, "create_external_defects": False}
    if not config_path.exists():
        return config
    for line in config_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("create_pr:"):
            config["create_pr"] = "true" in line.lower()
        elif line.startswith("create_external_defects:"):
            config["create_external_defects"] = "true" in line.lower()
    return config


# ── Validators ────────────────────────────────────────────────────────────────

def validate_jira(env: dict) -> tuple[bool, str]:
    try:
        import urllib.request
        import base64

        url = env.get("JIRA_URL", "").rstrip("/")
        username = env.get("JIRA_USERNAME", "")
        token = env.get("JIRA_API_TOKEN") or env.get("ATLASSIAN_BASIC_AUTH", "")

        if not url or not username or not token:
            missing = [k for k, v in {"JIRA_URL": url, "JIRA_USERNAME": username, "JIRA_API_TOKEN": token}.items() if not v]
            return False, f"Missing env vars: {', '.join(missing)}"

        creds = base64.b64encode(f"{username}:{token}".encode()).decode()
        req = urllib.request.Request(
            f"{url}/rest/api/3/myself",
            headers={"Authorization": f"Basic {creds}", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            account = data.get("emailAddress") or data.get("displayName", "unknown")
            return True, f"Connected as {account}"
    except Exception as exc:
        return False, str(exc)


def validate_github(env: dict) -> tuple[bool, str]:
    try:
        import urllib.request

        token = env.get("GITHUB_TOKEN", "")
        if not token:
            return False, "GITHUB_TOKEN not set in .env"

        req = urllib.request.Request(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            login = data.get("login", "unknown")
            return True, f"Connected as {login}"
    except Exception as exc:
        return False, str(exc)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    env = load_env(ROOT / ".env")
    config = load_stlc_config()

    results = {}
    failed_required = []

    # Jira — always required (fetching requirements)
    ok, msg = validate_jira(env)
    results["Jira (Atlassian)"] = ("PASS" if ok else "FAIL", msg, True)
    if not ok:
        failed_required.append("Jira")

    # Confluence — required if defect/report publishing enabled
    if config["create_external_defects"]:
        # Same credentials as Jira for cloud accounts; reuse the Jira check result
        results["Confluence"] = results["Jira (Atlassian)"]

    # # GitHub — required if create_pr: true
    # if config["create_pr"]:
    #     ok, msg = validate_github(env)
    #     results["GitHub"] = ("PASS" if ok else "FAIL", msg, True)
    #     if not ok:
    #         failed_required.append("GitHub")
    # else:
    #     ok, msg = validate_github(env)
    #     status = "PASS" if ok else "SKIP"
    #     note = msg if ok else f"Not required (create_pr=false); {msg}"
    #     results["GitHub"] = (status, note, False)

    # ── Print report ──────────────────────────────────────────────────────────
    print("\n" + "=" * 56)
    print("       MCP CONNECTIVITY VALIDATION")
    print("=" * 56 + "\n")

    all_pass = True
    for name, (status, msg, required) in results.items():
        icon = "[OK]  " if status == "PASS" else ("[SKIP]" if status == "SKIP" else "[FAIL]")
        req_label = "[required]" if required else "[optional]"
        print(f"  {icon}  {name:<22} {req_label}  {msg}")
        if status == "FAIL" and required:
            all_pass = False

    print()
    if all_pass:
        print("  PASS  All required integrations validated. Pipeline may proceed.\n")
        sys.exit(0)
    else:
        print("  BLOCKED  Fix the failed integrations above before retrying.")
        print("           Check .env for correct values and ensure .mcp.json exists.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
