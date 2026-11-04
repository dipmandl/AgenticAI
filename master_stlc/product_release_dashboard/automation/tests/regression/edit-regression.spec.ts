/**
 * Regression test cases: TC-040 to TC-051
 * Story: COD-7 — Edit Existing Release Note
 * REQ: REQ-006, REQ-007, REQ-009, REQ-010
 */

import { test, expect } from '@playwright/test';
import { clearAndSeedStorage, getLocalStorage, getRelease, getRawStorage } from '../helpers/storage';
import {
  DEFAULT_SEED,
  THREE_ITEM_SEED,
  SEED_BILLING,
  SEED_AUTH,
  SEED_PAYMENTS,
  type ReleaseNote,
} from '../fixtures/seed-data';

async function clickEditOnCard(page: any, productSubstring: string) {
  const card = page.locator('.release-card').filter({ hasText: productSubstring });
  await card.locator('.edit-btn').click();
}

async function fillCreateForm(
  page: any,
  data: { product: string; version: string; teamName: string; title: string; description: string; releaseDate: string }
) {
  await page.locator('#product').fill(data.product);
  await page.locator('#version').fill(data.version);
  await page.locator('#teamName').fill(data.teamName);
  await page.locator('#title').fill(data.title);
  await page.locator('#description').fill(data.description);
  await page.locator('#releaseDate').fill(data.releaseDate);
}

test.describe('Regression scenarios (TC-040 to TC-051)', () => {
  test.beforeEach(async ({ page }) => {
    await clearAndSeedStorage(page, DEFAULT_SEED);
  });

  // -------------------------------------------------------------------------
  test('TC-040 @REQ-006 @regression @high Create new release still works after Edit and Save', async ({ page }) => {
    await expect(page.locator('.release-card')).toHaveCount(2);

    // Edit Billing
    await clickEditOnCard(page, 'Billing API');
    await page.locator('#title').fill('Edited Billing Title');
    await page.locator('#submit-button').click();

    await expect(page.locator('#submit-button')).toHaveText('Add Release Note');

    // Now create a new release
    await fillCreateForm(page, {
      product: 'New Product',
      version: 'v3.0.0',
      teamName: 'New Team',
      title: 'Brand New Release',
      description: 'New release description',
      releaseDate: '2026-11-01',
    });
    await page.locator('#submit-button').click();

    await expect(page.locator('.release-card')).toHaveCount(3);

    const newCard = page.locator('.release-card').filter({ hasText: 'Brand New Release' });
    await expect(newCard).toBeVisible();

    const billingCard = page.locator('.release-card').filter({ hasText: 'Edited Billing Title' });
    await expect(billingCard).toBeVisible();

    const all = await getLocalStorage(page);
    expect(all.length).toBe(3);
  });

  // -------------------------------------------------------------------------
  test('TC-041 @REQ-009 @regression @high Create new release still works after Edit and Cancel', async ({ page }) => {
    await expect(page.locator('.release-card')).toHaveCount(2);

    // Edit then cancel
    await clickEditOnCard(page, 'Billing API');
    await page.locator('#title').fill('CANCELLED_CHANGE');
    await page.locator('#cancel-edit-button').click();

    await expect(page.locator('#submit-button')).toHaveText('Add Release Note');

    // Create new release
    await fillCreateForm(page, {
      product: 'Post Cancel Product',
      version: 'v1.0.0',
      teamName: 'Test Team',
      title: 'Post-Cancel New Release',
      description: 'Created after a cancelled edit',
      releaseDate: '2026-09-01',
    });
    await page.locator('#submit-button').click();

    await expect(page.locator('.release-card')).toHaveCount(3);

    const newCard = page.locator('.release-card').filter({ hasText: 'Post-Cancel New Release' });
    await expect(newCard).toBeVisible();

    // Billing API shows original title
    const billingCard = page.locator('.release-card').filter({ hasText: SEED_BILLING.title });
    await expect(billingCard).toBeVisible();

    await expect(page.locator('#submit-button')).toHaveText('Add Release Note');
  });

  // -------------------------------------------------------------------------
  test('TC-042 @REQ-006 @regression @high Delete a different release still works after Edit and Save', async ({ page }) => {
    await clearAndSeedStorage(page, THREE_ITEM_SEED);
    await expect(page.locator('.release-card')).toHaveCount(3);

    // Edit Billing API (r1), update title
    await clickEditOnCard(page, 'Billing API');
    await page.locator('#title').fill('A Updated');
    await page.locator('#submit-button').click();

    // Delete Auth Service (r2) — handle confirm dialog
    page.once('dialog', (dialog) => dialog.accept());
    const authCard = page.locator('.release-card').filter({ hasText: 'Auth Service' });
    await authCard.locator('.delete-btn').click();

    await expect(page.locator('.release-card')).toHaveCount(2);

    // Auth Service gone
    await expect(page.locator('.release-card').filter({ hasText: 'Auth Service' })).toHaveCount(0);

    // Billing API shows updated title
    const billingCard = page.locator('.release-card').filter({ hasText: 'A Updated' });
    await expect(billingCard).toBeVisible();

    // Payments still there
    const paymentsCard = page.locator('.release-card').filter({ hasText: 'Payments API' });
    await expect(paymentsCard).toBeVisible();
  });

  // -------------------------------------------------------------------------
  test('TC-043 @REQ-009 @regression @high Deleting the release currently in edit mode resets edit state', async ({ page }) => {
    await clickEditOnCard(page, 'Billing API');
    await expect(page.locator('#submit-button')).toHaveText('Update Release Note');

    // Delete the card currently being edited
    page.once('dialog', (dialog) => dialog.accept());
    const billingCard = page.locator('.release-card').filter({ hasText: 'Billing API' });
    await billingCard.locator('.delete-btn').click();

    // Billing API gone
    await expect(page.locator('.release-card').filter({ hasText: 'Billing API' })).toHaveCount(0);

    // Edit mode reset
    await expect(page.locator('#submit-button')).toHaveText('Add Release Note');
    await expect(page.locator('#cancel-edit-button')).toBeHidden();

    // Can still add a new release
    await fillCreateForm(page, {
      product: 'New Entry',
      version: 'v1.0.0',
      teamName: 'Test Team',
      title: 'Post-Delete New Entry',
      description: 'Added after deleting the edit target',
      releaseDate: '2026-10-01',
    });
    await page.locator('#submit-button').click();

    const newCard = page.locator('.release-card').filter({ hasText: 'Post-Delete New Entry' });
    await expect(newCard).toBeVisible();
  });

  // -------------------------------------------------------------------------
  test('TC-044 @REQ-010 @regression @high Product filter functions correctly before and after Edit and Save', async ({ page }) => {
    // Set product filter to Billing API
    await page.locator('#product-filter').selectOption('Billing API');

    // Edit visible Billing card
    await clickEditOnCard(page, 'Billing API');
    await page.locator('#description').fill('Filter regression test description');
    await page.locator('#submit-button').click();

    // Still filtered to Billing API
    await expect(page.locator('#product-filter')).toHaveValue('Billing API');
    await expect(page.locator('.release-card')).toHaveCount(1);

    // Switch to Auth Service
    await page.locator('#product-filter').selectOption('Auth Service');
    const authCards = page.locator('.release-card').filter({ hasText: 'Auth Service' });
    await expect(authCards).toHaveCount(1);

    // Switch back to Billing API
    await page.locator('#product-filter').selectOption('Billing API');
    const billingCards = page.locator('.release-card').filter({ hasText: 'Billing API' });
    await expect(billingCards).toHaveCount(1);

    // Data not corrupted
    const stored = await getRelease(page, SEED_BILLING.id);
    expect(stored!.product).toBe('Billing API');
  });

  // -------------------------------------------------------------------------
  test('TC-045 @REQ-010 @regression @high Breaking-change filter functions correctly after Edit and Save', async ({ page }) => {
    // Set filter to breaking only
    await page.locator('#breaking-filter').selectOption('breaking');

    // Auth Service (isBreaking: true) should be visible
    await expect(page.locator('.release-card').filter({ hasText: 'Auth Service' })).toBeVisible();

    // Edit Auth Service, change description only
    await clickEditOnCard(page, 'Auth Service');
    await page.locator('#description').fill('Breaking filter regression test');
    await page.locator('#submit-button').click();

    // Switch to non-breaking
    await page.locator('#breaking-filter').selectOption('non-breaking');
    await expect(page.locator('.release-card').filter({ hasText: 'Billing API' })).toBeVisible();
    await expect(page.locator('.release-card').filter({ hasText: 'Auth Service' })).toHaveCount(0);

    // Switch back to breaking
    await page.locator('#breaking-filter').selectOption('breaking');
    await expect(page.locator('.release-card').filter({ hasText: 'Auth Service' })).toBeVisible();
    await expect(page.locator('.release-card').filter({ hasText: 'Billing API' })).toHaveCount(0);

    // isBreaking not accidentally changed
    const stored = await getRelease(page, SEED_AUTH.id);
    expect(stored!.isBreaking).toBe(true);
  });

  // -------------------------------------------------------------------------
  test('TC-046 @REQ-010 @regression @high Keyword search filter functions correctly after Edit and Save', async ({ page }) => {
    // Seed one release with 'alpha' in title and one without
    const alphaRelease: ReleaseNote = {
      id: 'r5',
      product: 'Alpha Product',
      version: 'v0.1.0',
      teamName: 'Alpha Team',
      title: 'Alpha feature release',
      description: 'Initial alpha feature drop',
      releaseDate: '2026-08-01',
      isBreaking: false,
    };
    await clearAndSeedStorage(page, [alphaRelease, ...DEFAULT_SEED]);

    // Search for alpha
    await page.locator('#search-filter').fill('alpha');
    const alphaCard = page.locator('.release-card').filter({ hasText: 'Alpha feature release' });
    await expect(alphaCard).toBeVisible();
    // Billing and Auth should not show (no 'alpha' in title/description)
    await expect(page.locator('.release-card').filter({ hasText: 'Billing API' })).toHaveCount(0);

    // Edit the alpha release description (not title)
    await alphaCard.locator('.edit-btn').click();
    await page.locator('#description').fill('Updated alpha description with alpha keyword');
    await page.locator('#submit-button').click();

    // Clear and retype search
    await page.locator('#search-filter').fill('');
    await page.locator('#search-filter').fill('alpha');

    // Alpha card still matches
    await expect(page.locator('.release-card').filter({ hasText: 'Alpha feature release' })).toBeVisible();
  });

  // -------------------------------------------------------------------------
  test('TC-047 @REQ-010 @regression @high Multi-filter combination persists correctly after Edit and Save', async ({ page }) => {
    // Seed a breaking Billing API release with v1 in title
    const breakingBilling: ReleaseNote = {
      id: 'r6',
      product: 'Billing API',
      version: 'v1.9.0',
      teamName: 'Platform Team',
      title: 'Breaking billing v1 change',
      description: 'Breaking change for v1 billing customers',
      releaseDate: '2026-07-15',
      isBreaking: true,
    };
    await clearAndSeedStorage(page, [...DEFAULT_SEED, breakingBilling]);

    // Apply three filters
    await page.locator('#product-filter').selectOption('Billing API');
    await page.locator('#breaking-filter').selectOption('breaking');
    await page.locator('#search-filter').fill('v1');

    const visibleCard = page.locator('.release-card').first();
    await visibleCard.locator('.edit-btn').click();
    await page.locator('#description').fill('Multi-filter regression test description');
    await page.locator('#submit-button').click();

    // All three filters still set
    await expect(page.locator('#product-filter')).toHaveValue('Billing API');
    await expect(page.locator('#breaking-filter')).toHaveValue('breaking');
    await expect(page.locator('#search-filter')).toHaveValue('v1');
  });

  // -------------------------------------------------------------------------
  test('TC-048 @REQ-007 @regression @high Edited values persist after a full page reload', async ({ page }) => {
    await clickEditOnCard(page, 'Billing API');
    await page.locator('#title').fill('Reload Persistence Test');
    await page.locator('#submit-button').click();

    // Reload the page
    await page.reload();

    // App loads from localStorage — edited title must appear
    const billingCard = page.locator('.release-card').filter({ hasText: 'Reload Persistence Test' });
    await expect(billingCard).toBeVisible();

    // Count unchanged
    await expect(page.locator('.release-card')).toHaveCount(2);
  });

  // -------------------------------------------------------------------------
  // TC-049: @manual_only — file download (CSV) cannot be reliably automated
  test.skip('TC-049 @REQ-007 @regression @medium @manual_only Export CSV contains updated values after Edit and Save', async () => {
    // Manual: edit title to "CSV Export Test", click Export CSV, verify downloaded CSV
  });

  // -------------------------------------------------------------------------
  // TC-050: @manual_only — file input (JSON import) is handled manually
  test.skip('TC-050 @REQ-009 @regression @medium @manual_only Importing JSON while in edit mode resets edit state', async () => {
    // Manual: enter edit mode, trigger JSON import, confirm dialog, verify edit state reset
  });

  // -------------------------------------------------------------------------
  test('TC-051 @REQ-006 @regression @high Form in create mode creates a new entry and does not trigger an update', async ({ page }) => {
    // Verify create mode
    await expect(page.locator('#submit-button')).toHaveText('Add Release Note');
    await expect(page.locator('.release-card')).toHaveCount(2);

    await fillCreateForm(page, {
      product: 'Confirm Product',
      version: 'v1.0.0',
      teamName: 'Confirm Team',
      title: 'Confirm Create Mode',
      description: 'This should be a new entry, not an update',
      releaseDate: '2026-12-15',
    });
    await page.locator('#submit-button').click();

    // New card visible
    const newCard = page.locator('.release-card').filter({ hasText: 'Confirm Create Mode' });
    await expect(newCard).toBeVisible();

    // Total is now 3
    await expect(page.locator('.release-card')).toHaveCount(3);

    // No existing entry was modified
    const storedBilling = await getRelease(page, SEED_BILLING.id);
    expect(storedBilling!.title).toBe(SEED_BILLING.title);

    const storedAuth = await getRelease(page, SEED_AUTH.id);
    expect(storedAuth!.title).toBe(SEED_AUTH.title);

    const all = await getLocalStorage(page);
    expect(all.length).toBe(3);
  });
});
