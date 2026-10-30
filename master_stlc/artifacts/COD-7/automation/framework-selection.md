# Framework Selection: COD-7

## Selected Framework
**Playwright** (Node.js / TypeScript)

## Rationale
| Criterion | Playwright Fit |
|---|---|
| `file://` protocol support | Native — no HTTP server required |
| `localStorage` access | `page.evaluate(() => localStorage.getItem(...))` — direct |
| DOM interactions | Excellent — `locator()`, `getByRole()`, `fill()`, `click()`, `check()` |
| Speed | Fast headless execution; 51 scenarios complete in under 60 s |
| Assertions | Built-in `expect()` with auto-retry and meaningful diffs |
| BDD integration | Optional — `@cucumber/cucumber` + `@playwright/test` can consume `.feature` files; plain POM spec files are used here for direct traceability |
| CI readiness | `npx playwright test` works in any Node.js CI pipeline |

## Alternatives Considered
| Framework | Reason Not Selected |
|---|---|
| Cypress | Requires HTTP server for `file://`; larger install footprint |
| Selenium (Python) | Verbose API; no native localStorage helper; slower than Playwright |
| Behave (Python BDD) | Python ecosystem mismatch; needs Playwright/Selenium plugin; extra config overhead |

## Test Structure
```
product_release_dashboard/
├── automation/
│   ├── playwright.config.ts        # Playwright configuration
│   ├── package.json                # npm dependencies
│   ├── tests/
│   │   ├── helpers/
│   │   │   └── storage.ts          # localStorage utilities
│   │   ├── positive/
│   │   │   └── edit-positive.spec.ts
│   │   ├── negative/
│   │   │   └── edit-negative.spec.ts
│   │   ├── boundary/
│   │   │   └── edit-boundary.spec.ts
│   │   └── regression/
│   │       └── edit-regression.spec.ts
│   └── fixtures/
│       └── seed-data.ts            # seed release notes fixture
```

## Setup Requirements
```json
{
  "devDependencies": {
    "@playwright/test": "^1.44.0",
    "typescript": "^5.4.0"
  }
}
```
Install: `npm install && npx playwright install chromium`

## Configuration (playwright.config.ts)
```typescript
import { defineConfig } from '@playwright/test';
import path from 'path';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  use: {
    baseURL: `file://${path.resolve(__dirname, '../index.html')}`,
    headless: true,
    storageState: undefined,
  },
  reporter: [['html', { outputFolder: 'playwright-report' }], ['json', { outputFile: 'results.json' }]],
});
```

## Traceability to Feature File
The `.feature` file at `product_release_dashboard/manual/release_notes/edit_release_note.feature` is the human-readable specification. Each Playwright spec maps TC-NNN identifiers to test titles so traceability is preserved end-to-end:
```typescript
test('TC-002 Edit button pre-fills all 7 fields', async ({ page }) => { ... });
```

## Run Commands
```bash
# All tests
npx playwright test

# Regression suite only
npx playwright test --grep @regression

# Single TC
npx playwright test --grep "TC-007"

# Headed (debug)
npx playwright test --headed
```
