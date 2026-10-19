---
name: Cypress Browser Automation Skill
description: JavaScript E2E automation with feature-based structure, POM, and 2-category tag strategy
trigger: "when selecting cypress for E2E testing or modern JavaScript test automation"
category: automation
frameworks: [cypress]
languages: [javascript, typescript]
applies_to_phases: [automation-generation, automation-review, execution]
---

# Cypress Browser Automation Skill

See [README.md](./README.md) for full patterns, examples, and conventions.

## Quick Reference

- **Framework**: Cypress + cypress-grep (for tag filtering)
- **Languages**: JavaScript, TypeScript
- **Best for**: E2E testing, JS/TS projects, real-time feedback
- **Browser**: Chromium-based (Chrome, Edge, Electron)

## Folder structure

```
automation/
├── cypress/
│   ├── e2e/
│   │   └── <feature>/          # feature folders (login/, release_form/)
│   │       └── <scenario>.cy.js
│   ├── pages/                  # Page Object Model
│   │   └── <Feature>Page.js
│   ├── fixtures/
│   ├── support/
│   │   ├── commands.js
│   │   └── e2e.js
│   └── utils/
│       └── helpers.js
├── cypress.config.js
└── package.json
```

## Tag strategy — 2 categories

**Category 1 — Test type**: `smoke` · `regression` · `positive` · `negative` · `boundary` · `e2e` · `critical` · `high` · `medium` · `low` · `ui` · `manual_only`

**Category 2 — Story tag**: `story_002` · `story_NNN`

**Traceability**: embedded in test title — `'TC-001 REQ-001: <description>'`

## Test tag template

```javascript
it('TC-001 REQ-001: Successful form submission', {
  tags: ['story_002', 'smoke', 'critical', 'positive']
}, () => { ... })
```

## Key run commands

```bash
npx cypress run --env grepTags=story_002
npx cypress run --env grepTags="story_002|story_003"
npx cypress run --env grepTags=smoke
npx cypress run --env grepTags="negative+critical"
npx cypress run --spec "cypress/e2e/release_form/**"
```
