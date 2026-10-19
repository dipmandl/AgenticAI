# STLC Hooks Configuration

**Status:** Active hooks via `.claude/settings.json`  
**Last Updated:** 2026-09-23

## Overview

All STLC hooks are now configured in `.claude/settings.json` following Claude's official hook syntax. These hooks automatically execute during pipeline phases without consuming Claude tokens.

---

## Hook Execution Flow

```
User runs: /1-stlc "story"
           ↓
[PRE-TASK HOOKS]
  ├─ stlc-pre-task-validation
  └─ stlc-pre-task-safety-check
           ↓
[PHASE EXECUTION]
  └─ Repository discovery → Requirement analysis → ... → Reporting
           ↓
[POST-TASK HOOKS]
  ├─ stlc-post-task-artifact-validation
  ├─ stlc-token-metrics-generation
  ├─ stlc-html-report-generation
  ├─ stlc-traceability-validation
  └─ stlc-state-persistence
           ↓
[ON-ERROR HOOKS] (if failures)
  └─ stlc-safety-violation-check
```

---

## Hooks Configured

### 1. **stlc-pre-task-validation**
- **Trigger:** Before any STLC task
- **Action:** Validate repository structure and state
- **Checks:** `.claude/config/` exists, `artifacts/state/stlc-state.json` present
- **Token Cost:** Zero

### 2. **stlc-pre-task-safety-check**
- **Trigger:** Before execution (`/4-stlc-run`)
- **Action:** Verify execution permissions and safety constraints
- **Checks:** User approval needed, no destructive commands, no dependency install without permission
- **Token Cost:** Zero

### 3. **stlc-post-task-artifact-validation**
- **Trigger:** After any STLC phase completes
- **Action:** Validate all generated artifacts
- **Checks:** Artifacts exist, no duplicates
- **Token Cost:** Zero

### 4. **stlc-token-metrics-generation**
- **Trigger:** After `/6-stlc-report` completes
- **Action:** Run `python .claude\scripts\token-usage.py`
- **Output:** `artifacts/<story_id>/metrics/agent-metrics.json`
- **Token Cost:** Zero (deterministic analysis)

### 5. **stlc-html-report-generation**
- **Trigger:** After `/6-stlc-report` completes
- **Action:** Run `python .claude\scripts\html-report-generator.py`
- **Output:** `artifacts/<story_id>/reports/stlc-report.html`
- **Token Cost:** Zero (deterministic generation)
- **Sequence:** Runs AFTER token-usage (depends on metrics.json)

### 6. **stlc-traceability-validation**
- **Trigger:** After automation or execution phases
- **Action:** Validate requirement → test → execution traceability
- **Checks:** `traceability-matrix.md` exists
- **Token Cost:** Zero

### 7. **stlc-safety-violation-check**
- **Trigger:** On any error during STLC tasks
- **Action:** Classify failure type and enforce constraints
- **Rules:** 
  - No assertion weakening
  - No app code changes without approval
  - Self-healing only for AUTOMATION_FAILURE
- **Token Cost:** Zero

### 8. **stlc-state-persistence**
- **Trigger:** After any STLC phase
- **Action:** Ensure state is persisted
- **Purpose:** Enable pipeline resumability
- **Token Cost:** Zero

---

## Hook Syntax Reference

Each hook follows Claude's standard structure:

```json
{
  "name": "hook-identifier",
  "trigger": "before-task | after-task | on-error",
  "condition": "JavaScript expression matching task properties",
  "action": "shell",
  "script": "shell command to execute",
  "description": "Human-readable description",
  "severity": "info | warning | error",
  "continue_on_error": true | false
}
```

### Trigger Types
- **before-task**: Runs before phase execution starts
- **after-task**: Runs after phase completes successfully
- **on-error**: Runs if phase fails

### Condition Examples
```javascript
// Match specific commands
task.command.includes('stlc-report')
task.command.includes('/6-stlc')

// Match task status
task.status === 'success'
task.status === 'failed'

// Match error types
error.message.includes('APPLICATION_FAILURE')
```

### Available task Properties
- `task.command`: The command being executed
- `task.type`: Type of task (e.g., 'code-execution')
- `task.status`: Current status ('success', 'failed', etc.)
- `error`: Error object (on-error hooks only)

---

## Permissions Configuration

Hooks respect the permissions block:

```json
"permissions": {
  "allow_shell_execution": true,
  "allow_file_read": ["artifacts/**", ".claude/config/**"],
  "allow_file_write": ["artifacts/**"],
  "deny": ["application/**", "src/**", "node_modules/**"]
}
```

**Protection:** Hooks cannot modify:
- Application source code (`application/**`, `src/**`)
- Dependencies (`node_modules/**`)
- Test automation without approval
- Existing configuration files

---

## Execution Sequence Example

### Running `/6-stlc-report`:

```
1. Pre-task: stlc-pre-task-validation
   └─ Check state.json exists ✓

2. Phase: Reporting agent runs
   └─ Generates final-stlc-report.json ✓

3. Post-task: stlc-post-task-artifact-validation
   └─ Verify artifacts exist ✓

4. Post-task: stlc-token-metrics-generation
   └─ Run .claude\scripts\token-usage.py → agent-metrics.json ✓

5. Post-task: stlc-html-report-generation
   └─ Run .claude\scripts\html-report-generator.py → stlc-report.html ✓

6. Post-task: stlc-traceability-validation
   └─ Check traceability-matrix.md ✓

7. Post-task: stlc-state-persistence
   └─ Verify state.json updated ✓

[RESULT] HTML report ready at artifacts/reports/stlc-report.html
```

---

## Token Cost Analysis

| Hook | Execution | Cost |
|---|---|---|
| pre-task-validation | shell check | 0 tokens |
| pre-task-safety-check | shell echo | 0 tokens |
| post-task-artifact-validation | shell ls | 0 tokens |
| token-metrics-generation | Python script (deterministic) | 0 tokens |
| html-report-generation | Python script (deterministic) | 0 tokens |
| traceability-validation | shell check | 0 tokens |
| safety-violation-check | shell echo | 0 tokens |
| state-persistence | shell check | 0 tokens |
| **TOTAL** | **All deterministic** | **0 tokens** |

---

## How to Modify Hooks

Edit `.claude/settings.json` and:
1. Add/remove/modify hook objects
2. Update `trigger`, `condition`, `script` as needed
3. Restart Claude session (hooks reload on session start)

Example: Add a new pre-execution hook:
```json
{
  "name": "my-custom-hook",
  "trigger": "before-task",
  "condition": "task.command.includes('pytest')",
  "action": "shell",
  "script": "echo 'Running custom pre-test setup...'",
  "description": "Custom pre-test initialization",
  "severity": "info"
}
```

---

## Debugging Hooks

Check hook execution by:
1. Running a phase: `/6-stlc-report`
2. Observing shell output in Claude Code terminal
3. Verifying artifacts were generated
4. Checking `artifacts/reports/stlc-report.html` exists

---

## References

- Claude Hooks Documentation: https://docs.anthropic.com/claude-code/hooks
- STLC Pipeline: See `CLAUDE.md`
- State Management: `artifacts/state/stlc-state.json`
