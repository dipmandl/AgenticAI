# Repository Analysis Skill

## Purpose
Provide a reusable repository scanning pattern for the STLC pipeline.

## Use when
- The orchestrator needs repo discovery before planning and automation.
- The system must determine existing frameworks, tools, and test conventions.

## Inputs
- Repository contents
- Existing config files
- Build and dependency manifests

## Outputs
- Repository capabilities summary
- Candidate frameworks and test directions
- Risk or blind spots to note in planning

## Rules
- Use evidence from the repository, not assumptions.
- Keep analysis non-destructive.
- Record findings in artifacts/repository/repository-discovery.md.
