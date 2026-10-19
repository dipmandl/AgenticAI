# Execution Hook

**Status:** ✅ ACTIVE - Configured in `hooks.json`

## Implementation

This hook is implemented via:
- `stlc-pre-task-safety-check` — Safety validation before execution
- `stlc-post-task-artifact-validation` — Artifact validation after execution

See `docs/HOOKS-ACTIVE-CONFIGURATION.md` for complete hook configuration.

## Purpose
Prepare execution validation, environment checks, and artifact collection.

## Checks
- Environment is known
- Command is valid
- Scope is explicit
- Reports and logs directories exist
- Exit codes and artifacts are captured

## Output
- Execution summary and metadata
