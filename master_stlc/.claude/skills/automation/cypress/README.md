# Cypress Automation Skill — Full Reference

## When to use
- Repository is JavaScript or TypeScript.
- Test plan includes UI / E2E / browser testing.

## Dependencies

```json
{
  "devDependencies": {
    "cypress": "^13.0.0",
    "@cypress/grep": "^4.0.0",
    "mochawesome": "^7.0.0",
    "mochawesome-merge": "^4.0.0"
  }
}
```

`@cypress/grep` is required for tag-based filtering.

## Folder structure

```
automation/
├── cypress/
│   ├── e2e/
│   │   ├── release_form/              # feature folder
│   │   │   ├── form_submission.cy.js
│   │   │   ├── form_validation.cy.js
│   │   │   └── form_boundary.cy.js
│   │   ├── release_list/
│   │   │   └── release_list.cy.js
│   │   └── regression/
│   │       └── end_to_end.cy.js
│   ├── pages/                         # Page Object Model
│   │   ├── BasePage.js
│   │   └── ReleaseFormPage.js
│   ├── fixtures/
│   │   └── test_data.json
│   ├── support/
│   │   ├── commands.js                # custom Cypress commands
│   │   └── e2e.js                     # global before/after hooks
│   └── utils/
│       └── helpers.js                 # shared constants
├── cypress.config.js
└── package.json
```

**Rule**: `e2e/` folders = features. Test type = tags.

## Tag strategy

```
story_002      — story ownership (always present)
smoke          — fast build sanity
regression     — full pre-release suite
positive       — happy path
negative       — invalid input / error paths
boundary       — edge cases
e2e            — multi-step flows
critical       — must-pass gate
high / medium / low — priority
manual_only    — excluded from automated run
```

TC and REQ go in the **test title** (Cypress has no parametrized marker system):
```javascript
it('TC-007 REQ-002: Submit empty product shows inline error', ...)
```

## Page Object pattern

```javascript
// cypress/pages/ReleaseFormPage.js
class ReleaseFormPage {
  visit()                { cy.visit('/') }
  fillProduct(val)       { cy.get('#product').type(val) }
  fillVersion(val)       { cy.get('#version').type(val) }
  fillTitle(val)         { cy.get('#title').type(val) }
  fillDescription(val)   { cy.get('#description').type(val) }
  fillDate(val)          { cy.get('#releaseDate').type(val) }
  submit()               { cy.get("button[type='submit']").click() }
  getError(field)        { return cy.get(`.field-error[data-for="${field}"]`) }
  assertErrorVisible(f)  { this.getError(f).should('be.visible') }
  assertErrorHidden(f)   { this.getError(f).should('not.be.visible') }

  fillAll({ product, version, title, description, date }) {
    this.fillProduct(product)
    this.fillVersion(version)
    this.fillTitle(title)
    this.fillDescription(description)
    this.fillDate(date)
  }
}
export default new ReleaseFormPage()
```

## Test file pattern

```javascript
// cypress/e2e/release_form/form_validation.cy.js
import form from '../../pages/ReleaseFormPage'

describe('Release Form — Inline Validation', () => {

  beforeEach(() => {
    cy.clearLocalStorage()
    form.visit()
  })

  it('TC-007 REQ-002: Submit empty product shows inline error', {
    tags: ['story_002', 'negative', 'critical', 'smoke']
  }, () => {
    form.submit()
    form.assertErrorVisible('product')
  })

  it('TC-001 REQ-001: Successful submission with all fields valid', {
    tags: ['story_002', 'positive', 'critical', 'smoke']
  }, () => {
    form.fillAll({
      product: 'Product Alpha', version: '1.0.0',
      title: 'Initial Release', description: 'First release.', date: '2026-09-23'
    })
    form.submit()
    cy.get('#release-list .product-version').first().should('contain', 'Product Alpha')
  })
})
```

## cypress.config.js

```javascript
const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    baseUrl: process.env.BASE_URL || 'http://localhost:3000',
    screenshotsFolder: 'cypress/screenshots',
    videosFolder:      'cypress/videos',
    reporter:          'mochawesome',
    setupNodeEvents(on, config) {
      require('@cypress/grep/src/plugin')(config)
      return config
    },
  },
})
```

## support/e2e.js

```javascript
import '@cypress/grep'        // enables tag filtering
```

## Execution commands

```bash
# By story
npx cypress run --env grepTags=story_002
npx cypress run --env grepTags="story_002|story_003"   # OR

# By type
npx cypress run --env grepTags=smoke
npx cypress run --env grepTags="negative+critical"     # AND

# By feature folder
npx cypress run --spec "cypress/e2e/release_form/**"

# All tests headless
npx cypress run

# Headed for debugging
npx cypress open
```

## Safety
- Use `Cypress.env()` for credentials — never hardcode.
- Use `data-testid` attributes as preferred locators.
- Classify failures with failure-analysis-agent before modifying assertions.
- Exclude `manual_only` in CI: `--env grepTags="not+manual_only"` (requires cypress-grep v4+).
