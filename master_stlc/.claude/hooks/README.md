# STLC Hooks Configuration

**Location:** `.claude/hooks/`  
**Active Configuration:** `hooks.json`  
**Status:** ✅ All hooks active and executable

---

## File Structure

```
.claude/hooks/
├── hooks.json              ← ACTIVE hook configuration (JSON)
├── README.md               ← This file
├── pre-task.md             ← Pre-task hook documentation
├── post-task.md            ← Post-task hook documentation
├── execution.md            ← Execution hook documentation
└── safety.md               ← Safety hook documentation
```

---

## Active Hooks (from hooks.json)

All hooks execute automatically during STLC pipeline phases.

| # | Hook Name | Trigger | Action | Token Cost |
|---|---|---|---|---|
| 1 | `stlc-pre-task-validation` | before-task | Validate repo structure | 0 |
| 2 | `stlc-pre-task-safety-check` | before-task (execution) | Verify permissions | 0 |
| 3 | `stlc-post-task-artifact-validation` | after-task | Validate artifacts | 0 |
| 4 | `stlc-token-metrics-generation` | after-task (report) | Run token-usage.py | 0 |
| 5 | `stlc-html-report-generation` | after-task (report) | Run html-report-generator.py | 0 |
| 6 | `stlc-traceability-validation` | after-task (auto/run) | Validate traceability matrix | 0 |
| 7 | `stlc-safety-violation-check` | on-error | Enforce safety rules | 0 |
| 8 | `stlc-state-persistence` | after-task | Persist state.json | 0 |

---

## Hook Execution Flow

```
/1-stlc "story"
    ↓
[PRE-TASK]
├─ stlc-pre-task-validation ✓
└─ stlc-pre-task-safety-check (if /4-stlc-run)
    ↓
[PHASE EXECUTION]
└─ Repository → Requirements → Impact → Plan → Tests → Review → Automation → Exec → Report
    ↓
[POST-TASK]
├─ stlc-post-task-artifact-validation ✓
├─ stlc-token-metrics-generation (if /6-stlc-report) ✓
├─ stlc-html-report-generation (if /6-stlc-report) ✓
├─ stlc-traceability-validation ✓
└─ stlc-state-persistence ✓
    ↓
[ON-ERROR] (if failures occur)
└─ stlc-safety-violation-check ✓
```

---

## Hook Configuration Format

Each hook in `hooks.json` follows Claude's standard structure:

```json
{
  "name": "unique-hook-identifier",
  "trigger": "before-task | after-task | on-error",
  "condition": "JavaScript expression",
  "action": "shell",
  "script": "shell command to execute",
  "description": "What this hook does",
  "severity": "info | warning | error",
  "continue_on_error": true | false
}
```

### Trigger Types
- **before-task** — Runs before phase starts
- **after-task** — Runs after phase completes successfully
- **on-error** — Runs if phase fails

### Condition Examples
```javascript
// Match commands
task.command.includes('stlc-report')
task.command.includes('/6-stlc')

// Match status
task.status === 'success'
error.message.includes('APPLICATION_FAILURE')
```

---

## Modifying Hooks

To add, modify, or delete hooks:

1. **Edit** `.claude/hooks/hooks.json`
2. **Update** the hooks array (add/remove/modify hook objects)
3. **Restart** Claude Code session (hooks reload on startup)

### Example: Add Custom Hook

```json
{
  "name": "my-custom-hook",
  "trigger": "before-task",
  "condition": "task.command.includes('pytest')",
  "action": "shell",
  "script": "echo 'Running pre-test setup...'",
  "description": "Custom pre-test initialization",
  "severity": "info",
  "continue_on_error": true
}
```

---

## Hook Execution Examples

### Example 1: Running `/6-stlc-report`

```
1. pre-task-validation
   └─ Validates .claude/config/ and artifacts/state/stlc-state.json ✓

2. [Reporting Agent Executes]
   └─ Generates final-stlc-report.json ✓

3. post-task-artifact-validation
   └─ Verifies artifacts/ directory structure ✓

4. token-metrics-generation
   └─ Runs: python .claude\scripts\token-usage.py
   └─ Output: artifacts/<story_id>/metrics/agent-metrics.json ✓

5. html-report-generation
   └─ Runs: python .claude\scripts\html-report-generator.py
   └─ Output: artifacts/<story_id>/reports/stlc-report.html ✓

6. traceability-validation
   └─ Checks artifacts/traceability/traceability-matrix.md ✓

7. state-persistence
   └─ Verifies artifacts/state/stlc-state.json updated ✓

[RESULT] Complete HTML report at artifacts/reports/stlc-report.html
```

### Example 2: Running `/4-stlc-run` with Failure

```
1. pre-task-validation ✓
2. pre-task-safety-check ✓
3. [Execution Agent Runs Tests] → 16 failures
4. post-task-artifact-validation ✓
5. safety-violation-check (ON-ERROR triggered)
   └─ Message: "16 failures classified as APPLICATION_FAILURE"
   └─ Action: "Review defect analysis before proceeding"
```

---

## Documentation Files

The `.md` files in this folder provide detailed documentation:

| File | Purpose |
|---|---|
| `pre-task.md` | Pre-task hook specifications and checks |
| `post-task.md` | Post-task hook specifications and metrics generation |
| `execution.md` | Execution validation and artifact collection |
| `safety.md` | Safety constraints and permission enforcement |

**Note:** These `.md` files are documentation only. The actual hook execution is defined in `hooks.json`.

---

## Debugging Hooks

To debug hook execution:

1. Run a phase: `/6-stlc-report`
2. Watch terminal output for `[STLC ...]` messages
3. Verify expected artifacts are generated
4. Check `artifacts/reports/stlc-report.html` exists
5. Verify `artifacts/metrics/agent-metrics.json` exists

---

## Token Cost Analysis

All hooks are **deterministic** (no Claude agent calls):

| Hook | Script | Execution Time | Token Cost |
|---|---|---|---|
| pre-task-validation | shell check | <100ms | 0 |
| pre-task-safety-check | shell echo | <50ms | 0 |
| post-task-artifact-validation | shell ls | <100ms | 0 |
| token-metrics-generation | Python script | ~500ms | 0 |
| html-report-generation | Python script | ~1s | 0 |
| traceability-validation | shell check | <100ms | 0 |
| safety-violation-check | shell echo | <50ms | 0 |
| state-persistence | shell check | <100ms | 0 |
| **TOTAL** | **All deterministic** | **~2-3 seconds** | **0 tokens** |

---

## References

- **Claude Hooks Docs:** https://docs.anthropic.com/claude-code/hooks
- **STLC Pipeline:** See `CLAUDE.md`
- **Complete Hooks Guide:** See `docs/HOOKS-ACTIVE-CONFIGURATION.md`
