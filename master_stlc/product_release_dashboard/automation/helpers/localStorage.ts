import { Page } from '@playwright/test';
import { STORAGE_KEY } from './selectors';

// ── Seed datasets ─────────────────────────────────────────────────────────────

/**
 * SD-001: 5 entries — 2×ProductA, 2×ProductB, 1×ProductC; mixed isBreaking; all have teamName.
 * Stable IDs test-id-001 … test-id-005.
 *
 * Design notes for filter-dependent tests:
 *   TC-029  needs: ProductA + isBreaking=true + title contains "release"  → test-id-001 qualifies.
 *   TC-014  needs: at least one entry with "keywordX" in title/description → test-id-002 description.
 *   TC-007  needs: at least one entry with isBreaking=false                → test-id-002 / 003 / 005.
 */
export const SD001_DATA = [
  {
    id: 'test-id-001',
    product: 'ProductA',
    version: 'v1.0.0',
    teamName: 'TeamAlpha',
    title: 'ProductA release notes v1',
    description: 'This is the first release note for ProductA.',
    releaseDate: '2024-01-15',
    isBreaking: true
  },
  {
    id: 'test-id-002',
    product: 'ProductA',
    version: 'v1.1.0',
    teamName: 'TeamBeta',
    title: 'ProductA minor update',
    description: 'Minor update including keywordX improvements and fixes.',
    releaseDate: '2024-02-20',
    isBreaking: false
  },
  {
    id: 'test-id-003',
    product: 'ProductB',
    version: 'v2.0.0',
    teamName: 'TeamGamma',
    title: 'ProductB major release',
    description: 'Major release for ProductB with new features.',
    releaseDate: '2024-03-10',
    isBreaking: false
  },
  {
    id: 'test-id-004',
    product: 'ProductB',
    version: 'v2.1.0',
    teamName: 'TeamDelta',
    title: 'ProductB security patch',
    description: 'Security patch update for ProductB.',
    releaseDate: '2024-04-05',
    isBreaking: true
  },
  {
    id: 'test-id-005',
    product: 'ProductC',
    version: 'v3.0.0',
    teamName: 'TeamEpsilon',
    title: 'ProductC initial release',
    description: 'Initial release of ProductC.',
    releaseDate: '2024-05-01',
    isBreaking: false
  }
];

/** SD-002: single entry, all fields, isBreaking=false */
export const SD002_DATA = [
  {
    id: 'test-id-001',
    product: 'ProductA',
    version: 'v1.0.0',
    teamName: 'TeamAlpha',
    title: 'Single Entry Title',
    description: 'Single entry description for boundary testing.',
    releaseDate: '2024-06-01',
    isBreaking: false
  }
];

/** SD-003: single entry, isBreaking=true */
export const SD003_DATA = [
  {
    id: 'test-id-001',
    product: 'ProductA',
    version: 'v2.0.0',
    teamName: 'TeamAlpha',
    title: 'Breaking Change Entry',
    description: 'Entry with a breaking change flag for boundary testing.',
    releaseDate: '2024-07-01',
    isBreaking: true
  }
];

/** SD-004: single entry, releaseDate="1970-01-01" */
export const SD004_DATA = [
  {
    id: 'test-id-001',
    product: 'ProductA',
    version: 'v1.0.0',
    teamName: 'TeamAlpha',
    title: 'Epoch Date Entry',
    description: 'Entry with Unix epoch release date for boundary testing.',
    releaseDate: '1970-01-01',
    isBreaking: false
  }
];

/**
 * SD-005: single entry, releaseDate = today (computed at runtime in browser context).
 * The actual seed is injected via addInitScript to compute today's date client-side.
 */

/** SD-006: single entry, teamName absent/undefined */
export const SD006_DATA = [
  {
    id: 'test-id-001',
    product: 'ProductA',
    version: 'v1.0.0',
    title: 'Entry Without TeamName',
    description: 'Entry missing the teamName field.',
    releaseDate: '2024-08-01',
    isBreaking: false
    // teamName intentionally omitted
  }
];

/** SD-008: two-product dataset — 1×ProductA, 1×ProductB, both isBreaking=false */
export const SD008_DATA = [
  {
    id: 'test-id-001',
    product: 'ProductA',
    version: 'v1.0.0',
    teamName: 'TeamAlpha',
    title: 'ProductA Entry',
    description: 'ProductA entry for filter regression testing.',
    releaseDate: '2024-09-01',
    isBreaking: false
  },
  {
    id: 'test-id-002',
    product: 'ProductB',
    version: 'v2.0.0',
    teamName: 'TeamBeta',
    title: 'ProductB Entry',
    description: 'ProductB entry for filter regression testing.',
    releaseDate: '2024-09-15',
    isBreaking: false
  }
];

// ── Seed dispatcher ───────────────────────────────────────────────────────────

/**
 * Seeds localStorage BEFORE the page's JavaScript runs by registering an
 * init script on the browser context.  Call this before page.goto('/').
 *
 * SD-007 injects 100 entries at runtime.
 * SD-009 clears the key so the app auto-seeds its two default records.
 */
export async function seedLocalStorage(page: Page, seedId: string): Promise<void> {
  switch (seedId) {

    case 'SD-001':
      await page.addInitScript(({ key, data }) => {
        localStorage.setItem(key, JSON.stringify(data));
      }, { key: STORAGE_KEY, data: SD001_DATA });
      break;

    case 'SD-002':
      await page.addInitScript(({ key, data }) => {
        localStorage.setItem(key, JSON.stringify(data));
      }, { key: STORAGE_KEY, data: SD002_DATA });
      break;

    case 'SD-003':
      await page.addInitScript(({ key, data }) => {
        localStorage.setItem(key, JSON.stringify(data));
      }, { key: STORAGE_KEY, data: SD003_DATA });
      break;

    case 'SD-004':
      await page.addInitScript(({ key, data }) => {
        localStorage.setItem(key, JSON.stringify(data));
      }, { key: STORAGE_KEY, data: SD004_DATA });
      break;

    case 'SD-005':
      // releaseDate is computed at runtime so today's date is always accurate
      await page.addInitScript((key) => {
        const today = new Date().toISOString().split('T')[0];
        localStorage.setItem(key, JSON.stringify([{
          id: 'test-id-001',
          product: 'ProductA',
          version: 'v1.0.0',
          teamName: 'TeamAlpha',
          title: "Today's Release Entry",
          description: 'Entry with today release date for boundary testing.',
          releaseDate: today,
          isBreaking: false
        }]));
      }, STORAGE_KEY);
      break;

    case 'SD-006':
      await page.addInitScript(({ key, data }) => {
        localStorage.setItem(key, JSON.stringify(data));
      }, { key: STORAGE_KEY, data: SD006_DATA });
      break;

    case 'SD-007': {
      // 100 randomised entries; ids test-id-001 … test-id-100
      const entries = Array.from({ length: 100 }, (_, i) => ({
        id: `test-id-${String(i + 1).padStart(3, '0')}`,
        product: `Product${String.fromCharCode(65 + (i % 5))}`,
        version: `v${Math.floor(i / 10) + 1}.${i % 10}.0`,
        teamName: `Team${i + 1}`,
        title: `Release note title ${i + 1}`,
        description: `Description for release note number ${i + 1}.`,
        releaseDate: `2024-${String(Math.floor(i / 30) + 1).padStart(2, '0')}-${String((i % 28) + 1).padStart(2, '0')}`,
        isBreaking: i % 3 === 0
      }));
      await page.addInitScript(({ key, data }) => {
        localStorage.setItem(key, JSON.stringify(data));
      }, { key: STORAGE_KEY, data: entries });
      break;
    }

    case 'SD-008':
      await page.addInitScript(({ key, data }) => {
        localStorage.setItem(key, JSON.stringify(data));
      }, { key: STORAGE_KEY, data: SD008_DATA });
      break;

    case 'SD-009':
      // Clear key so the app's loadReleases() triggers seedData() (2 default records)
      await page.addInitScript((key) => {
        localStorage.removeItem(key);
      }, STORAGE_KEY);
      break;

    default:
      throw new Error(`Unknown seed ID: ${seedId}`);
  }
}

// ── Utility helpers ───────────────────────────────────────────────────────────

/** Read the current releases array from localStorage (evaluated in-page). */
export async function getStoredReleases(page: Page): Promise<any[]> {
  return page.evaluate((key) => {
    const raw = localStorage.getItem(key);
    if (!raw) return [];
    try { return JSON.parse(raw); } catch { return []; }
  }, STORAGE_KEY);
}
