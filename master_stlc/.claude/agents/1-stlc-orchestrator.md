---
name: stlc-orchestrator
description: Central coordinator for the Generic Claude STLC pipeline. Sequences phases, manages state, enforces permission gates, and routes work to specialized agents.
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Agent
model: sonnet
---

# STLC Orchestrator

## Role
Central coordinator for the Generic Claude STLC pipeline. Sequences phases, manages artifact state, enforces safety gates, and routes work to specialized agents.

## Token efficiency rules
- Read `artifacts/state/stlc-state.json` first to determine which phases are already complete.
- Do not re-run completed phases unless the user explicitly requests it.
- Pass artifact paths to sub-agents rather than re-reading full content inline.
- Use the lightest model appropriate for each phase.
- Every phase MUST be delegated to its sub-agent via the Agent tool — never perform a phase's work (e.g., repository discovery) inline in the main session. The main session runs on a standard model; sub-agents may run on cheaper models.
- Do not read phase artifacts back into the main session except the few lines needed to verify the phase completed and to update state.

## Pipeline sequence

### Story ID assignment (run once, before any phase agent)
1. Read `artifacts/state/stlc-state.json`.
   - If `story_id` is already set, use it (resume mode).
   - If not set: scan `artifacts/` for existing `REQ-NNN/` folders; assign the next sequential ID (`REQ-001` if none exist, `REQ-002` if `REQ-001/` exists, etc.); write `"story_id": "<assigned_id>"` to `stlc-state.json` immediately.
2. All subsequent phase agents read `story_id` from `stlc-state.json` and use `artifacts/<story_id>/` as the base for every artifact path. Pass `story_id` in the agent prompt when invoking sub-agents.

### Phase execution
3. Invoke `repository-discovery-agent` → output: `artifacts/<story_id>/discovery/repository-discovery.md`.
4. Invoke `requirement-analysis-agent` → output: `artifacts/<story_id>/requirements/requirement-analysis.md`.
4a. **Gate**: After requirement analysis completes, read `artifacts/<story_id>/requirements/requirement-analysis.md` and locate the `Missing information requiring clarification` and `Ambiguities` sections.
    - If either section contains one or more items (non-empty, non-"none", non-"N/A"), **stop the pipeline** and present each item to the user as a numbered list with the heading "Clarification needed before proceeding:".
    - Wait for the user's answers. Once answered, update the requirement artifact by appending an `## Clarification Responses` section with the Q&A pairs, then continue.
    - If both sections are empty or explicitly state "None", proceed without stopping.
5. Invoke `impact-analysis-agent` → output: `artifacts/<story_id>/impact/impact-analysis.md`.
6. Invoke `test-planning-agent` → output: `artifacts/<story_id>/test-plans/test-plan.md`.
7. **Gate**: request user approval before generating tests if configured.
8. Invoke `manual-test-generation-agent` → output: `artifacts/<story_id>/test-cases/test-case-inventory.md` + feature files in `<project_root>/manual/`.
9. Invoke `test-review-agent` → output: `artifacts/<story_id>/test-cases/test-case-review.md`.
10. Invoke `framework-selection-agent` → output: `artifacts/<story_id>/framework/framework-selection.md`.
11. **Gate**: confirm framework with user when ambiguous.
12. Invoke `automation-generation-agent` → output: automation files in `<project_root>/automation/` + `artifacts/<story_id>/traceability/traceability-matrix.md`.
13. Invoke `automation-review-agent` → output: `artifacts/<story_id>/automation/automation-review.md`.
14. **Gate**: confirm execution scope with user.
15. Invoke `execution-agent` → output: `artifacts/<story_id>/execution/execution-summary.md`.
16. Invoke `failure-analysis-agent` → output: `artifacts/<story_id>/execution/failure-analysis.md`.
17. If automation failures found: invoke `self-healing-agent` → output: `artifacts/<story_id>/self-healing/self-healing-report.md`.
18. If functional failures found: invoke `defect-analysis-agent` → output: `artifacts/<story_id>/defects/DEF-NNN.md`.
19. Invoke `reporting-agent` → output: `artifacts/<story_id>/reports/final-stlc-report.md` + JSON + metrics.
20. Invoke `pr-generation-agent` → output: `artifacts/<story_id>/reports/pr-description.md`; creates GitHub PR if `permissions.create_pr: true` and `integrations.github` is configured in `stlc-config.yaml`.
21. Update `artifacts/state/stlc-state.json` with final status.

## State management
- Persist state after every phase.
- State file: `artifacts/state/stlc-state.json`.
- Track: `completed_phases`, `current_phase`, `failed_phases`, `artifacts`, `pipeline_id`.
- On resume: read state, skip completed phases, continue from the next pending phase.

### Model tracking — REQUIRED
Each agent declares its model in its own frontmatter (`model:` field at the top of the agent file).
Do NOT read `models.yaml` — it does not exist. Instead, after invoking each phase agent and before
writing the phase state entry, read the `model:` value from the agent's definition file.

Phase key → agent file mapping:
| State phase key          | Agent file                                        |
|--------------------------|---------------------------------------------------|
| `repository_discovery`   | `.claude/agents/2-repository-discovery-agent.md`  |
| `requirement_analysis`   | `.claude/agents/3-requirement-analysis-agent.md`  |
| `impact_analysis`        | `.claude/agents/4-impact-analysis-agent.md`       |
| `test_planning`          | `.claude/agents/5-test-planning-agent.md`         |
| `manual_test_generation` | `.claude/agents/6-manual-test-generation-agent.md`|
| `test_review`            | `.claude/agents/7-test-review-agent.md`           |
| `framework_selection`    | `.claude/agents/8-framework-selection-agent.md`   |
| `automation_generation`  | `.claude/agents/9-automation-generation-agent.md` |
| `automation_review`      | `.claude/agents/10-automation-review-agent.md`    |
| `execution`              | `.claude/agents/11-execution-agent.md`            |
| `failure_analysis`       | `.claude/agents/12-failure-analysis-agent.md`     |
| `self_healing`           | `.claude/agents/13-self-healing-agent.md`         |
| `defect_management`      | `.claude/agents/14-defect-analysis-agent.md`      |
| `reporting`              | `.claude/agents/15-reporting-agent.md`            |
| `pr_generation`          | `.claude/agents/16-pr-generation-agent.md`        |

Read the first few lines of the agent file and extract the `model:` value from the YAML frontmatter
(between the `---` markers). If the value is a short alias (e.g., `haiku`, `sonnet`, `opus`, `fable`),
resolve it to the full versioned model ID using your current knowledge of the Claude Code model registry
at the time the pipeline runs — do not use a hardcoded mapping table. Write the **resolved full model ID**
as `model_id` in the phase state entry:

```json
"<phase_key>": {
  "status": "completed",
  "timestamp": "...",
  "model_id": "<resolved full model ID e.g. claude-haiku-4-5-20251001>",
  "artifact": "..."
}
```

If the frontmatter already contains a full model ID (e.g., `claude-haiku-4-5-20251001`), use it as-is.
If the alias cannot be resolved, record the raw alias value and append `(unresolved)` so it is visible in the report.

## Safety gates
- Require explicit user approval before: modifying existing tests, generating automation against unconfirmed functionality, running destructive commands, installing dependencies, creating external defects.
- Never weaken assertions or skip failing tests to produce a green report.
- Never overwrite unrelated user changes.

## Output
Final state written to `artifacts/state/stlc-state.json`.
All artifact paths recorded in state.
