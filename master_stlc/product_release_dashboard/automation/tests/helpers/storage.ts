import { Page } from '@playwright/test';
import { ReleaseNote } from '../fixtures/seed-data';

const STORAGE_KEY = 'releaseNotesDashboard.releases';

/**
 * Returns the full parsed releases array from localStorage.
 */
export async function getLocalStorage(page: Page): Promise<ReleaseNote[]> {
  return page.evaluate((key: string) => {
    const raw = localStorage.getItem(key);
    if (!raw) return [];
    try {
      const parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  }, STORAGE_KEY);
}

/**
 * Clears the storage key and writes fresh seed items, then navigates to the app.
 * Call this before page.goto() so the page loads with the seeded data.
 */
export async function clearAndSeedStorage(page: Page, items: ReleaseNote[]): Promise<void> {
  // Navigate to the page first so we have an origin to write localStorage against
  await page.goto('');
  await page.evaluate(
    ({ key, data }: { key: string; data: ReleaseNote[] }) => {
      localStorage.setItem(key, JSON.stringify(data));
    },
    { key: STORAGE_KEY, data: items }
  );
  // Reload so the app reads the freshly seeded data
  await page.reload();
}

/**
 * Finds a single release by its id in localStorage. Returns undefined if not found.
 */
export async function getRelease(page: Page, id: string): Promise<ReleaseNote | undefined> {
  const all = await getLocalStorage(page);
  return all.find((r) => r.id === id);
}

/**
 * Returns the raw JSON string stored under the releases key.
 */
export async function getRawStorage(page: Page): Promise<string> {
  return page.evaluate((key: string) => localStorage.getItem(key) ?? '', STORAGE_KEY);
}
