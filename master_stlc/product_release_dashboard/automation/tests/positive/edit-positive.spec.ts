/**
 * Positive test cases: TC-001 to TC-018
 * Story: COD-7 — Edit Existing Release Note
 * REQ: REQ-001, REQ-002, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-010, REQ-011, REQ-012
 */

import { test, expect } from '@playwright/test';
import { clearAndSeedStorage, getLocalStorage, getRelease, getRawStorage } from '../helpers/storage';
import {
  DEFAULT_SEED,
  THREE_ITEM_SEED,
  SEED_BILLING,
  SEED_AUTH,
  SEED_PAYMENTS,
} from '../fixtures/seed-data';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

async function clickEditOnCard(page: any, productVersion: string) {
  const card = page.locator('.release-card').filter({ hasText: productVersion });
  await card.locator('.edit-btn').click();
}

// ---------------------------------------------------------------------------
// TC-001 to TC-006 — Edit button visibility and edit-mode activation
// ---------------------------------------------------------------------------

test.describe('Edit button and edit-mode UI (TC-001 to TC-006)', () => {
  test.beforeEach(async ({ page }) => {
    await clearAndSeedStorage(page, DEFAULT_SEED);
  });

  test('TC-001 @REQ-001 @positive @high Edit button is visible on every rendered release card', async ({ page }) => {
    const cards = page.locator('.release-card');
    const count = await cards.count();
    expect(count).toBeGreaterThan(0);
    for (let i = 0; i < count; i++) {
      await expect(cards.nth(i).locator('.edit-btn')).toBeVisible();
    }
  });

  test('TC-002 @REQ-002 @positive @critical Clicking Edit pre-fills all 7 form fields with the release data', async ({ page }) => {
    await clickEditOnCard(page, 'Billing API');

    await expect(page.locator('#product')).toHaveValue(SEED_BILLING.product);
    await expect(page.locator('#version')).toHaveValue(SEED_BILLING.version);
    await expect(page.locator('#teamName')).toHaveValue(SEED_BILLING.teamName);
    await expect(page.locator('#title')).toHaveValue(SEED_BILLING.title);
    await expect(page.locator('#description')).toHaveValue(SEED_BILLING.description);
    await expect(page.locator('#releaseDate')).toHaveValue(SEED_BILLING.releaseDate);
    await expect(page.locator('#breaking')).not.toBeChecked();
  });

  test('TC-003 @REQ-002 @positive @high isBreaking checkbox pre-fills as checked for a breaking release', async ({ page }) => {
    await clickEditOnCard(page, 'Auth Service');
    await expect(page.locator('#breaking')).toBeChecked();
  });

  test('TC-004 @REQ-002 @positive @high isBreaking checkbox pre-fills as unchecked for a non-breaking release', async ({ page }) => {
    await clickEditOnCard(page, 'Billing API');
    await expect(page.locator('#breaking')).not.toBeChecked();
  });

  test('TC-005 @REQ-004 @positive @high Submit button label changes to "Update Release Note" in edit mode', async ({ page }) => {
    await clickEditOnCard(page, 'Billing API');
    const submitBtn = page.locator('#submit-button');
    await expect(submitBtn).toBeVisible();
    await expect(submitBtn).toHaveText('Update Release Note');
    await expect(submitBtn).toBeEnabled();
  });

  test('TC-006 @REQ-005 @positive @high Cancel Edit button becomes visible when edit mode is active', async ({ page }) => {
    const cancelBtn = page.locator('#cancel-edit-button');
    // Before edit mode it should be hidden
    await expect(cancelBtn).toBeHidden();
    await clickEditOnCard(page, 'Billing API');
    await expect(cancelBtn).toBeVisible();
    await expect(cancelBtn).toBeEnabled();
  });
});

// ---------------------------------------------------------------------------
// TC-007 to TC-011 — Save behaviour
// ---------------------------------------------------------------------------

test.describe('Save updates the correct entry (TC-007 to TC-011)', () => {
  test.beforeEach(async ({ page }) => {
    await clearAndSeedStorage(page, DEFAULT_SEED);
  });

  test('TC-007 @REQ-006 @positive @critical Save updates the specific release by its id', async ({ page }) => {
    await clickEditOnCard(page, 'Billing API');
    await page.locator('#title').fill('Updated Billing Title');
    await page.locator('#submit-button').click();

    // Card in DOM
    const card = page.locator('.release-card').filter({ hasText: 'Updated Billing Title' });
    await expect(card).toBeVisible();

    // localStorage
    const stored = await getRelease(page, SEED_BILLING.id);
    expect(stored).toBeDefined();
    expect(stored!.title).toBe('Updated Billing Title');
    expect(stored!.id).toBe(SEED_BILLING.id);
  });

  test('TC-008 @REQ-006 @positive @critical Save does not create a duplicate entry', async ({ page }) => {
    // Initial count
    await expect(page.locator('.release-card')).toHaveCount(2);

    await clickEditOnCard(page, 'Billing API');
    await page.locator('#title').fill('No Duplicate Title');
    await page.locator('#submit-button').click();

    await expect(page.locator('.release-card')).toHaveCount(2);
    const all = await getLocalStorage(page);
    expect(all.length).toBe(2);
  });

  test('TC-009 @REQ-006 @positive @high Save does not modify any other release entries', async ({ page }) => {
    // Record Auth baseline from localStorage before edit
    const authBefore = await getRelease(page, SEED_AUTH.id);

    await clickEditOnCard(page, 'Billing API');
    await page.locator('#title').fill('Changed Title');
    await page.locator('#submit-button').click();

    const authAfter = await getRelease(page, SEED_AUTH.id);
    expect(JSON.stringify(authAfter)).toBe(JSON.stringify(authBefore));
  });

  test('TC-010 @REQ-007 @positive @critical Updated release is persisted to localStorage after Save', async ({ page }) => {
    await clickEditOnCard(page, 'Billing API');
    await page.locator('#title').fill('Persisted Title Test');
    await page.locator('#submit-button').click();

    const all = await getLocalStorage(page);
    expect(Array.isArray(all)).toBe(true);
    const entry = all.find((r) => r.id === SEED_BILLING.id);
    expect(entry).toBeDefined();
    expect(entry!.title).toBe('Persisted Title Test');
  });

  test('TC-011 @REQ-008 @positive @high Release list re-renders immediately with updated values after Save', async ({ page }) => {
    await clickEditOnCard(page, 'Billing API');
    await page.locator('#title').fill('Re-render Title Test');
    await page.locator('#submit-button').click();

    // No page reload — check DOM directly
    const card = page.locator('.release-card').filter({ hasText: 'Re-render Title Test' });
    await expect(card).toBeVisible();
  });
});

// ---------------------------------------------------------------------------
// TC-012 to TC-013 — Cancel behaviour
// ---------------------------------------------------------------------------

test.describe('Cancel discards changes (TC-012 to TC-013)', () => {
  test.beforeEach(async ({ page }) => {
    await clearAndSeedStorage(page, DEFAULT_SEED);
  });

  test('TC-012 @REQ-009 @positive @critical Cancel discards in-progress changes and rendered list is unchanged', async ({ page }) => {
    const baselineRaw = await getRawStorage(page);

    await clickEditOnCard(page, 'Billing API');
    await page.locator('#title').fill('DISCARDED_TITLE');
    await page.locator('#cancel-edit-button').click();

    // Original title still visible
    const originalCard = page.locator('.release-card').filter({ hasText: SEED_BILLING.title });
    await expect(originalCard).toBeVisible();

    // Discarded title not present
    const discardedCard = page.locator('.release-card').filter({ hasText: 'DISCARDED_TITLE' });
    await expect(discardedCard).toHaveCount(0);

    // localStorage must be byte-for-byte identical — Cancel must not write anything
    const afterRaw = await getRawStorage(page);
    expect(afterRaw).toBe(baselineRaw);
  });

  test('TC-013 @REQ-009 @positive @high Cancel leaves localStorage unchanged', async ({ page }) => {
    const baselineRaw = await getRawStorage(page);

    await clickEditOnCard(page, 'Billing API');
    await page.locator('#title').fill('SHOULD_NOT_PERSIST');
    await page.locator('#version').fill('v9.9.9');
    await page.locator('#cancel-edit-button').click();

    const afterRaw = await getRawStorage(page);
    expect(afterRaw).toBe(baselineRaw);
  });
});

// ---------------------------------------------------------------------------
// TC-014 to TC-015 — Filter persistence
// ---------------------------------------------------------------------------

test.describe('Filters remain applied after Save and Cancel (TC-014 to TC-015)', () => {
  test.beforeEach(async ({ page }) => {
    await clearAndSeedStorage(page, DEFAULT_SEED);
  });

  test('TC-014 @REQ-010 @positive @critical All active filters remain applied after Save', async ({ page }) => {
    // Need at least one breaking Billing API release. Seed a breaking Billing v1 entry.
    const breakingBilling = {
      id: 'r4',
      product: 'Billing API',
      version: 'v1.5.0',
      teamName: 'Platform Team',
      title: 'Breaking billing change v1',
      description: 'This is a breaking change for billing v1',
      releaseDate: '2026-07-01',
      isBreaking: true,
    };
    await clearAndSeedStorage(page, [...DEFAULT_SEED, breakingBilling]);

    // Apply three filters
    await page.locator('#product-filter').selectOption('Billing API');
    await page.locator('#breaking-filter').selectOption('breaking');
    await page.locator('#search-filter').fill('v1');

    // Click Edit on the visible matching card
    const visibleCard = page.locator('.release-card').first();
    await visibleCard.locator('.edit-btn').click();

    // Change description
    await page.locator('#description').fill('Filter Persistence Test');
    await page.locator('#submit-button').click();

    // Filters must still be set
    await expect(page.locator('#product-filter')).toHaveValue('Billing API');
    await expect(page.locator('#breaking-filter')).toHaveValue('breaking');
    await expect(page.locator('#search-filter')).toHaveValue('v1');
  });

  test('TC-015 @REQ-011 @positive @high All active filters remain applied after Cancel', async ({ page }) => {
    await clearAndSeedStorage(page, DEFAULT_SEED);

    await page.locator('#product-filter').selectOption('Billing API');
    // 'export' appears in SEED_BILLING title — search only matches title+description, not product/version
    await page.locator('#search-filter').fill('export');

    await clickEditOnCard(page, 'Billing API');
    await page.locator('#description').fill('Unsaved Description');
    await page.locator('#cancel-edit-button').click();

    await expect(page.locator('#product-filter')).toHaveValue('Billing API');
    await expect(page.locator('#search-filter')).toHaveValue('export');
  });
});

// ---------------------------------------------------------------------------
// TC-016 to TC-018 — Position-based editing
// ---------------------------------------------------------------------------

test.describe('Edit operates correctly at any list position (TC-016 to TC-018)', () => {
  test.beforeEach(async ({ page }) => {
    await clearAndSeedStorage(page, THREE_ITEM_SEED);
  });

  test('TC-016 @REQ-012 @positive @medium Edit operates correctly on the first card in the list', async ({ page }) => {
    const cards = page.locator('.release-card');
    await expect(cards).toHaveCount(3);

    await cards.first().locator('.edit-btn').click();
    await page.locator('#title').fill('First Card Updated');
    await page.locator('#submit-button').click();

    await expect(page.locator('.release-card').first().locator('.release-title')).toHaveText('First Card Updated');
    // Other cards unchanged
    const secondTitle = await page.locator('.release-card').nth(1).locator('.release-title').textContent();
    const thirdTitle = await page.locator('.release-card').nth(2).locator('.release-title').textContent();
    expect(secondTitle).not.toBe('First Card Updated');
    expect(thirdTitle).not.toBe('First Card Updated');
  });

  test('TC-017 @REQ-012 @positive @medium Edit operates correctly on the last card in the list', async ({ page }) => {
    const cards = page.locator('.release-card');
    await expect(cards).toHaveCount(3);

    await cards.last().locator('.edit-btn').click();
    await page.locator('#title').fill('Last Card Updated');
    await page.locator('#submit-button').click();

    await expect(page.locator('.release-card').last().locator('.release-title')).toHaveText('Last Card Updated');
    const firstTitle = await page.locator('.release-card').first().locator('.release-title').textContent();
    const secondTitle = await page.locator('.release-card').nth(1).locator('.release-title').textContent();
    expect(firstTitle).not.toBe('Last Card Updated');
    expect(secondTitle).not.toBe('Last Card Updated');
  });

  test('TC-018 @REQ-012 @positive @medium Edit operates correctly on a middle card in the list', async ({ page }) => {
    const cards = page.locator('.release-card');
    await expect(cards).toHaveCount(3);

    await cards.nth(1).locator('.edit-btn').click();
    await page.locator('#title').fill('Middle Card Updated');
    await page.locator('#submit-button').click();

    await expect(page.locator('.release-card').nth(1).locator('.release-title')).toHaveText('Middle Card Updated');
    const firstTitle = await page.locator('.release-card').first().locator('.release-title').textContent();
    const lastTitle = await page.locator('.release-card').last().locator('.release-title').textContent();
    expect(firstTitle).not.toBe('Middle Card Updated');
    expect(lastTitle).not.toBe('Middle Card Updated');
  });
});
