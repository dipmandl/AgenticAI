# Safety Hook

**Status:** ✅ ACTIVE - Configured in `hooks.json`

## Implementation

This hook is now active via:
- `stlc-pre-task-safety-check` — Verify permissions before execution
- `stlc-safety-violation-check` — Enforce safety constraints on errors

See `docs/HOOKS-ACTIVE-CONFIGURATION.md` for complete hook configuration.

## Purpose
Prevent unsafe operations and policy violations.

## Rules
- Never modify existing tests or automation without user approval.
- Never modify application code without approval.
- Never install dependencies without permission.
- Never weaken assertions.
- Never create external defects without approval.
- Never overwrite unrelated user changes.

## Permissions Enforced

The following paths are protected:
- ✅ Can read/write: `artifacts/**`, `.claude/config/**`
- ❌ Cannot write: `application/**`, `src/**`, `node_modules/**`

## Failures
- Stop the workflow and request approval or clarification.
