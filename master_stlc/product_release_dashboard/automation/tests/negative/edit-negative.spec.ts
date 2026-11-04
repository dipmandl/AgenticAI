/**
 * Negative test cases: TC-019 to TC-027
 * Story: COD-7 — Edit Existing Release Note
 * REQ: REQ-002, REQ-004, REQ-005, REQ-006, REQ-009
 */

import { test, expect } from '@playwright/test';
import { clearAndSeedStorage, getLocalStorage, getRawStorage } from '../helpers/storage';
import { DEFAULT_SEED, SEED_BILLING, SEED_AUTH } from '../fixtures/seed-data';

async function clickEditOnCard(page: any, productVersion: string) {
  const card = page.locator('.release-card').filter({ hasText: productVersion });
  await card.locator('.edit-btn').click();
}

test.describe('Negative scenarios (TC-019 to TC-027)', () => {
  test.beforeEach(async ({ page }) => {
    await clearAndSeedStorage(page, DEFAULT_SEED);
  });

  // -------------------------------------------------------------------------
  test('TC-019 @REQ-009 @negative @high Cancel without modifying any field leaves list and localStorage unchanged', async ({ page }) => {
    const baselineRaw = await getRawStorage(page);
    const cardsBefore = await page.locator('.release-card').count();

    await clickEditOnCard(page, 'Billing API');
    // Do NOT modify any field
    await page.locator('#cancel-edit-button').click();

    // localStorage unchanged
    const afterRaw = await getRawStorage(page);
    expect(afterRaw).toBe(baselineRaw);

    // Same card count
    await expect(page.locator('.release-card')).toHaveCount(cardsBefore);

    // Submit button back to create mode
    await expect(page.locator('#submit-button')).toHaveText('Add Release Note');

    // Cancel button hidden
    await expect(page.locator('#cancel-edit-button')).toBeHidden();
  });

  // -------------------------------------------------------------------------
  test('TC-020 @REQ-004 @negative @high Save with teamName cleared shows validation error and preserves edit state', async ({ page }) => {
    const baselineRaw = await getRawStorage(page);

    await clickEditOnCard(page, 'Billing API');
    await page.locator('#teamName').fill('');
    await page.locator('#submit-button').click();

    // Validation error visible
    const errorEl = page.locator('#team-name-error');
    await expect(errorEl).toBeVisible();
    await expect(errorEl).toHaveText('Team name is required.');

    // Still in edit mode
    await expect(page.locator('#submit-button')).toHaveText('Update Release Note');

    // localStorage unchanged
    const afterRaw = await getRawStorage(page);
    expect(afterRaw).toBe(baselineRaw);

    // Rendered list unchanged (still 2 cards)
    await expect(page.locator('.release-card')).toHaveCount(2);
  });

  // -------------------------------------------------------------------------
  test('TC-021 @REQ-004 @negative @high Save with title cleared shows validation error', async ({ page }) => {
    const baselineRaw = await getRawStorage(page);

    await clickEditOnCard(page, 'Billing API');
    await page.locator('#title').fill('');
    await page.locator('#submit-button').click();

    // The browser required attribute or app validation prevents save
    // The submit button must still read "Update Release Note" (edit mode preserved)
    await expect(page.locator('#submit-button')).toHaveText('Update Release Note');

    // localStorage must be unchanged
    const afterRaw = await getRawStorage(page);
    expect(afterRaw).toBe(baselineRaw);

    await expect(page.locator('.release-card')).toHaveCount(2);
  });

  // -------------------------------------------------------------------------
  test('TC-022 @REQ-004 @negative @high Save with product cleared shows validation error', async ({ page }) => {
    const baselineRaw = await getRawStorage(page);

    await clickEditOnCard(page, 'Billing API');
    await page.locator('#product').fill('');
    await page.locator('#submit-button').click();

    await expect(page.locator('#submit-button')).toHaveText('Update Release Note');

    const afterRaw = await getRawStorage(page);
    expect(afterRaw).toBe(baselineRaw);

    await expect(page.locator('.release-card')).toHaveCount(2);
  });

  // -------------------------------------------------------------------------
  test('TC-023 @REQ-004 @negative @high Save with version cleared shows validation error', async ({ page }) => {
    const baselineRaw = await getRawStorage(page);

    await clickEditOnCard(page, 'Billing API');
    await page.locator('#version').fill('');
    await page.locator('#submit-button').click();

    await expect(page.locator('#submit-button')).toHaveText('Update Release Note');

    const afterRaw = await getRawStorage(page);
    expect(afterRaw).toBe(baselineRaw);

    await expect(page.locator('.release-card')).toHaveCount(2);
  });

  // -------------------------------------------------------------------------
  test('TC-024 @REQ-004 @negative @high Save with releaseDate cleared shows validation error', async ({ page }) => {
    const baselineRaw = await getRawStorage(page);

    await clickEditOnCard(page, 'Billing API');
    // Clear the date input via evaluate since fill('') may not clear date inputs in all browsers
    await page.locator('#releaseDate').evaluate((el: HTMLInputElement) => { el.value = ''; });
    await page.locator('#submit-button').click();

    await expect(page.locator('#submit-button')).toHaveText('Update Release Note');

    const afterRaw = await getRawStorage(page);
    expect(afterRaw).toBe(baselineRaw);

    await expect(page.locator('.release-card')).toHaveCount(2);
  });

  // -------------------------------------------------------------------------
  // TC-025 is @manual_only — DevTools console interaction cannot be automated
  test.skip('TC-025 @REQ-006 @negative @high @manual_only Calling startEdit with a non-existent id does not crash the application', async () => {
    // Manual: open DevTools, execute startEdit('non-existent-id-xyz'), observe no JS exception
  });

  // -------------------------------------------------------------------------
  test('TC-026 @REQ-002 @negative @medium Clicking Edit on card B while card A is in edit mode replaces form with card B values', async ({ page }) => {
    // Put Billing API into edit mode first
    await clickEditOnCard(page, 'Billing API');
    await expect(page.locator('#product')).toHaveValue('Billing API');

    // Now click Edit on Auth Service without saving
    await clickEditOnCard(page, 'Auth Service');

    await expect(page.locator('#product')).toHaveValue('Auth Service');
    await expect(page.locator('#version')).toHaveValue('v2.0.0');
    await expect(page.locator('#teamName')).toHaveValue('Identity Team');

    // No Billing API values should remain
    const productValue = await page.locator('#product').inputValue();
    const versionValue = await page.locator('#version').inputValue();
    expect(productValue).not.toBe('Billing API');
    expect(versionValue).not.toBe('v1.4.0');
  });

  // -------------------------------------------------------------------------
  test('TC-027 @REQ-005 @REQ-009 @negative @high Cancel after a validation failure exits edit mode cleanly', async ({ page }) => {
    const baselineRaw = await getRawStorage(page);

    await clickEditOnCard(page, 'Billing API');
    // Trigger validation failure by clearing title
    await page.locator('#title').fill('');
    await page.locator('#submit-button').click();

    // Validation error should be present (still in edit mode)
    await expect(page.locator('#submit-button')).toHaveText('Update Release Note');

    // Now cancel
    await page.locator('#cancel-edit-button').click();

    // Edit mode exited
    await expect(page.locator('#submit-button')).toHaveText('Add Release Note');
    await expect(page.locator('#cancel-edit-button')).toBeHidden();

    // Original card still shows original title
    const billingCard = page.locator('.release-card').filter({ hasText: SEED_BILLING.title });
    await expect(billingCard).toBeVisible();

    // localStorage unchanged
    const afterRaw = await getRawStorage(page);
    expect(afterRaw).toBe(baselineRaw);
  });
});
