import { defineConfig } from '@playwright/test';
import path from 'path';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  retries: 0,
  workers: 1,
  use: {
    baseURL: `file://${path.resolve(__dirname, '../index.html')}`,
    headless: true,
    storageState: undefined,
    actionTimeout: 10_000,
    navigationTimeout: 15_000,
  },
  reporter: [
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['json', { outputFile: 'results.json' }],
    ['list'],
  ],
  projects: [
    {
      name: 'chromium',
      use: { browserName: 'chromium' },
    },
  ],
});
