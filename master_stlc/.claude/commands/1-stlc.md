---
description: Step 1 (full pipeline): run the entire STLC workflow. IMPORTANT: Invoke ONLY when the user explicitly types this slash command. NEVER auto-run because a message merely contains a user story or requirement text — in that case, ask the user whether they want to start the STLC pipeline.
---

# STLC Command

Purpose:
Use this command to start the STLC orchestration workflow for a repository or a specific requirement.

Usage:
- Run the pipeline for a story or requirement.
- Proposal mode: analyze without modifying assets.
- Execution mode: run approved automation when available.

Instructions:
1. Review the repository and current state.
2. Analyze the requirement or story.
3. Determine impact and classification.
4. Generate or review a test plan and manual tests.
5. Detect or select the automation framework.
6. Execute approved steps and report results.
7. Stop at approval gates when required.
8. After reporting, run `python .claude\scripts\token-usage.py` to record per-phase token usage in `artifacts/<story_id>/metrics/`.
9. **Pipeline completion check (mandatory before marking status "complete"):**
   After the reporting phase, read `artifacts/state/stlc-state.json` and verify every required phase is in `completed_phases`. The full required sequence is:
   `repository_discovery → requirement_analysis → impact_analysis → test_planning → manual_test_generation → test_review → framework_selection → automation_generation → automation_review → execution → failure_analysis → reporting`
   Plus conditionally:
   - `self_healing` — required if any `AUTOMATION_FAILURE` was found in failure_analysis
   - `pr_generation` — required if `create_pr: true` in `.claude/config/stlc-config.yaml`
   - `defect_analysis` — required if `create_external_defects: true` in `.claude/config/stlc-config.yaml`
   If any required phase is missing from `completed_phases`, run it before setting `status: "complete"`. Never set the pipeline to complete with outstanding required phases.

Token efficiency:
- Delegate every phase to its dedicated sub-agent via the Agent tool; never perform phase work inline in the main session.
- Pass artifact file paths between phases, not file content.

Safety:
- Never modify existing tests, automation, or application code without explicit approval.
- Never weaken assertions or skip failing tests.
- Never expose secrets or credentials.

Workflow:
- analyze
- propose
- ask
- modify
- validate
- execute
- report
