# Post-task Hook

**Status:** ✅ ACTIVE - Configured in `hooks.json`

## Implementation

This hook is now active via the following configured hooks:
- `stlc-post-task-artifact-validation` — Validate generated artifacts
- `stlc-token-metrics-generation` — Generate token metrics (after /6-stlc-report)
- `stlc-html-report-generation` — Generate HTML report (after /6-stlc-report)
- `stlc-traceability-validation` — Validate requirement-test-execution linkage
- `stlc-state-persistence` — Persist state for resumability

See `docs/HOOKS-ACTIVE-CONFIGURATION.md` for complete hook configuration.

## Purpose
Validate generated artifacts after each phase and trigger deterministic post-processing.

## Checks
- Markdown output exists
- JSON output is valid when required
- Traceability references are consistent
- Files are not duplicates of existing artifacts
- No secrets are exposed

## Post-processing

### Metrics & Report Generation (after reporting phase)
If the completed phase is `reporting` or command is `/6-stlc-report`:

1. **Generate token metrics** (populates agent-metrics.json):
```bash
python .claude\scripts\token-usage.py
```
- Reads session transcripts from Claude Code
- Writes `artifacts/<story_id>/metrics/agent-metrics.md` + `.json`
- **Token cost**: Zero (deterministic transcript analysis)

2. **Generate HTML report** (combines final report + metrics):
```bash
python .claude\scripts\html-report-generator.py
```
- Reads `artifacts/reports/final-stlc-report.json` + `artifacts/<story_id>/metrics/agent-metrics.json`
- Generates `artifacts/<story_id>/reports/stlc-report.html`
- **Token cost**: Zero (deterministic JSON processing)

Both run sequentially in ~2-3 seconds total.

## Output
- Summary of created or modified files
- Validation status
- HTML report generation status (if applicable)
