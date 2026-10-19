# CLAUDE.md

Reusable, project-agnostic STLC (Software Testing Life Cycle) orchestration system built on Claude. Drop into any repository to run requirement analysis → test planning → automation → execution → failure analysis → self-healing → reporting.

Full architecture, artifact layout, CLI, and configuration reference: `docs/architecture.md` — read it on demand, not preemptively.

## Commands

| Command | Purpose |
|---|---|
| `/1-stlc <story>` | Full pipeline (stops at approval gates) |
| `/setup-mcp` | Install and verify the project Atlassian MCP setup |
| `/2-stlc-plan <story>` | Planning only: discovery → test plan |
| `/3-stlc-automate` | Test generation + automation (requires test plan) |
| `/4-stlc-run [scope]` | Execute + failure analysis + self-healing. Scope: `smoke`, `regression`, `impacted`, `all`, or TC-IDs |
| `/5-stlc-heal` | Re-run self-healing on AUTOMATION_FAILURE items |
| `/6-stlc-report` | Assemble final report from artifacts (read-only) |

## HTML Report

An interactive **HTML report** is automatically generated at the end of the pipeline:
- **Location**: `artifacts/reports/stlc-report.html`
- **Contents**: Combines STLC execution results + agent metrics in a single unified view
- **Tabbed sections**:
  - Test execution summary (pass/fail/xfail counts, pass rate)
  - Test group breakdown (positive, negative, boundary, regression)
  - Defects found
  - **Agent Metrics** with tabs:
    - **Per Phase**: token usage, cache stats, invocation counts by STLC phase
    - **Per Agent**: same metrics aggregated by agent
  - Environment and execution details
- **Features**: Dark/light mode support, responsive layout
- **Token Cost**: **Zero** — runs via hook (deterministic: token-usage → HTML generation)

**Hook sequence** (automatic after `/6-stlc-report`):
1. `python .claude\scripts\token-usage.py` — generates `artifacts\<story_id>\metrics\agent-metrics.json`
2. `python .claude\scripts\html-report-generator.py` — generates `artifacts\<story_id>\reports\stlc-report.html`

**Manual regeneration**:
```bash
python .claude\scripts\token-usage.py
python .claude\scripts\html-report-generator.py
```

See `docs/HOOKS-CONFIGURATION.md` for hook setup details.

## MCP Integrations

Atlassian MCP is configured for Claude Code in the project-scoped `.mcp.json` file:

| Server | Package | Purpose in STLC |
|---|---|---|
| `atlassian` | `mcp-atlassian` (Python) | Create Jira tickets from defects; publish STLC reports to Confluence |

**One-time setup**: either run `/setup-mcp` inside Claude or run `.\scripts\setup-mcp.ps1` from the repo root, provide your credentials interactively, then restart Claude Code.

**First-run flow**:
1. Run `/setup-mcp` or `.\scripts\setup-mcp.ps1`
2. Confirm that `.env` exists in the repo root
3. Restart Claude Code or open a fresh terminal
4. Run `claude` once in this project and approve the `atlassian` MCP server if prompted
5. Run `claude mcp list` and verify `atlassian` is `connected`

Required values stored in the local `.env` file created by the setup script:

| Variable | Value |
|---|---|
| `JIRA_URL` | `https://your-domain.atlassian.net` |
| `JIRA_USERNAME` | Atlassian account email |
| `JIRA_API_TOKEN` | [Atlassian API token](https://id.atlassian.com/manage-profile/security/api-tokens) |
| `CONFLUENCE_URL` | Same as `JIRA_URL` for cloud accounts |
| `CONFLUENCE_USERNAME` | Same as `JIRA_USERNAME` |
| `CONFLUENCE_API_TOKEN` | Same token as Jira for cloud accounts |

**Verification**: after restarting Claude Code, run `claude mcp list`. Atlassian will show `Pending approval` until you open `claude` in this project once and approve the server; after approval it should appear as `connected`.

## Key facts

- State: `artifacts/state/stlc-state.json` — read first; skip completed phases (pipeline is resumable).
- Agents pass artifact **paths**, not content. Delegate every phase to its sub-agent — never do phase work inline in the main session.
- Traceability IDs `REQ-NNN` / `TC-NNN` are preserved end-to-end; matrix at `artifacts/traceability/traceability-matrix.md`.
- Config: `.claude/config/stlc-config.yaml` (permissions, execution limits), `models.yaml`, `frameworks.yaml`.

## Safety rules (non-negotiable without explicit override)

- Never modify existing tests, automation, or application code without permission.
- Never weaken an assertion or skip a failing test to produce a green report.
- Never run destructive commands or install dependencies without approval.
- Self-healing is only allowed for `AUTOMATION_FAILURE` — not `APPLICATION_FAILURE`, `TEST_DATA_FAILURE`, or `ENVIRONMENT_FAILURE`.
- Duplicate artifacts and infinite retry loops are both prohibited.
