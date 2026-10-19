# Pre-task Hook

**Status:** ✅ ACTIVE - Configured in `hooks.json`

## Implementation

This hook is now active via the following configured hooks:
- `stlc-pre-task-validation` — Repository and state validation
- `stlc-pre-task-safety-check` — Execution safety constraints

See `docs/HOOKS-ACTIVE-CONFIGURATION.md` for complete hook configuration.

## Purpose
Validate that the repository and STLC context are ready before work begins.

## Checks
- Repository exists
- Configuration loads
- Required directories exist
- No destructive actions without approval
- No secret leakage in logs or reports

## Output
- Block or continue with explicit reasoning.
