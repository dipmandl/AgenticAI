#!/usr/bin/env python3
"""Post-task artifact validation: checks traceability matrix, state file, and artifact structure."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "artifacts"


def check(label: str, matches: list[Path], warn_msg: str) -> None:
    if matches:
        print(f"[OK] {label}: {matches[0].relative_to(ROOT)}")
    else:
        print(f"[WARN] {label}: {warn_msg}")


def main() -> int:
    if not ARTIFACTS.is_dir():
        print("[SKIP] artifacts/ directory not found — pipeline not started yet")
        return 0

    story_dirs = [p for p in ARTIFACTS.iterdir() if p.is_dir() and p.name != "state"]
    if not story_dirs:
        print("[SKIP] No story artifact folders found yet")
        return 0

    print(f"[STLC Post-Task] Validating artifacts under: {ARTIFACTS.relative_to(ROOT)}")
    for story in sorted(story_dirs):
        print(f"  Story: {story.name}")
        subdirs = [p.name for p in story.iterdir() if p.is_dir()]
        print(f"    Folders: {', '.join(sorted(subdirs)) or '(none)'}")

    check(
        "Traceability matrix",
        list(ARTIFACTS.glob("*/traceability/traceability-matrix.md")),
        "traceability-matrix.md not found — run /3-stlc-automate",
    )

    check(
        "State file",
        list(ARTIFACTS.glob("*/state/stlc-state.json")),
        "stlc-state.json not found — pipeline may need initialization",
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
