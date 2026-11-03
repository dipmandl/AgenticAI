#!/usr/bin/env python3
"""PreToolUse hook — runs before every Agent tool call.

Fast path: if artifacts/.mcp-validated exists and is < 1 hour old, exit 0 immediately.
Slow path: run full MCP validation (validate-mcp.py), write the flag on success,
           exit 1 on failure so the harness blocks the Agent tool call.

This script never blocks on re-validation within the same session.
"""

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FLAG = ROOT / "artifacts" / ".mcp-validated"
MAX_AGE_SECONDS = 3600  # re-validate after 1 hour


def flag_is_fresh() -> bool:
    if not FLAG.exists():
        return False
    age = time.time() - FLAG.stat().st_mtime
    return age < MAX_AGE_SECONDS


def main():
    if flag_is_fresh():
        sys.exit(0)

    # Run full validation
    result = subprocess.run(
        [sys.executable, str(ROOT / ".claude" / "scripts" / "validate-mcp.py")],
        capture_output=False,   # let output print to terminal
    )

    if result.returncode == 0:
        FLAG.parent.mkdir(parents=True, exist_ok=True)
        FLAG.write_text(str(time.time()), encoding="utf-8")
        sys.exit(0)
    else:
        print("\n  [PIPELINE BLOCKED] MCP validation failed. Fix the issues above and retry.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
