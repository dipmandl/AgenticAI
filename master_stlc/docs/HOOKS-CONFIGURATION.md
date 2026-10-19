# Hook Configuration for HTML Report Generation

## Problem
Generating the HTML report at the end of `/6-stlc-report` adds extra steps that consume Claude tokens, even though the report is purely deterministic (read JSON, generate HTML).

## Solution
Use **hooks** — deterministic shell commands that run without consuming Claude tokens.

## Current Setup

**File:** `.claude/settings.json`

```json
{
  "hooks": [
    {
      "trigger": "after-task",
      "condition": "task.command.includes('stlc-report') || task.command.includes('/6-stlc')",
      "action": "shell",
      "script": "python .claude\\scripts\\html-report-generator.py",
      "description": "Auto-generate combined HTML report after reporting phase"
    }
  ]
}
```

## How It Works

1. **Trigger**: After `/6-stlc-report` completes
2. **Condition**: Matches commands containing "stlc-report" or "/6-stlc"
3. **Action**: Runs `python .claude\scripts\html-report-generator.py` in the shell
4. **Result**: `artifacts/<story_id>/reports/stlc-report.html` is generated
5. **Token Cost**: **ZERO** — no Claude agent invocation

## Benefits

| Approach | Token Cost | Execution Time |
|---|---|---|
| Inside Claude agent | ~5,000-10,000 tokens | ~30-60s |
| Via shell hook | **0 tokens** | ~1-2s |
| **Savings** | **100% reduction** | **95% faster** |

## Manual Trigger (if needed)

Even with the hook, you can manually regenerate the HTML anytime:
```bash
python .claude\scripts\html-report-generator.py
```

## Other Hooks You Can Add

Examples of other efficient deterministic tasks to offload to hooks:

```json
{
  "hooks": [
    {
      "trigger": "after-task",
      "condition": "task.command.includes('stlc-run')",
      "action": "shell",
      "script": "python .claude\\scripts\\token-usage.py",
      "description": "Update token metrics after execution"
    },
    {
      "trigger": "after-task",
      "condition": "task.command.includes('stlc')",
      "action": "shell",
      "script": "echo 'Pipeline phase complete' && ls -la artifacts/reports/",
      "description": "Log phase completion status"
    }
  ]
}
```

## Hook Syntax Reference

- **trigger**: `before-task`, `after-task`, `on-error`
- **condition**: JavaScript expression matching task properties (optional)
- **action**: `shell` (only type supported currently)
- **script**: Shell command to execute
- **description**: Human-readable label

For more hook options, see: https://docs.anthropic.com/claude-code/hooks
