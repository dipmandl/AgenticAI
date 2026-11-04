/**
 * Boundary test cases: TC-028 to TC-039
 * Story: COD-7 — Edit Existing Release Note
 * REQ: REQ-002, REQ-003, REQ-006, REQ-010, REQ-012
 */

import { test, expect } from '@playwright/test';
import { clearAndSeedStorage, getLocalStorage, getRelease, getRawStorage } from '../helpers/storage';
import {
  DEFAULT_SEED,
  SINGLE_ITEM_SEED,
  SEED_BILLING,
  SEED_AUTH,
  type ReleaseNote,
} from '../fixtures/seed-data';

async function clickEditOnCard(page: any, productSubstring: string) {
  const card = page.locator('.release-card').filter({ hasText: productSubstring });
  await card.locator('.edit-btn').click();
}

test.describe('Boundary scenarios (TC-028 to TC-039)', () => {
  test.beforeEach(async ({ page }) => {
    await clearAndSeedStorage(page, DEFAULT_SEED);
  });

  // -------------------------------------------------------------------------
  test('TC-028 @REQ-002 @REQ-006 @boundary @high Edit all 7 fields then Save persists every change', async ({ page }) => {
    await clickEditOnCard(page, 'Billing API');

    await page.locator('#product').fill('Payments API');
    await page.locator('#version').fill('v2.0.0');
    await page.locator('#teamName').fill('Finance Team');
    await page.locator('#title').fill('All Fields Changed Title');
    await page.locator('#description').fill('All seven fields have been updated');
    await page.locator('#releaseDate').fill('2026-12-01');
    // Billing is non-breaking; check the box to make it breaking
    await page.locator('#breaking').check();

    await page.locator('#submit-button').click();

    // DOM assertions
    const card = page.locator('.release-card').filter({ hasText: 'All Fields Changed Title' });
    await expect(card).toBeVisible();
    await expect(card.locator('.product-version')).toHaveText('Payments API - v2.0.0');
    // script.js renders team as "Team: <name>" — toContainText is intentionally used here, not toHaveText
    await expect(card.locator('.release-team')).toContainText('Finance Team');

    // localStorage assertions
    const stored = await getRelease(page, SEED_BILLING.id);
    expect(stored!.product).toBe('Payments API');
    expect(stored!.version).toBe('v2.0.0');
    expect(stored!.teamName).toBe('Finance Team');
    expect(stored!.title).toBe('All Fields Changed Title');
    expect(stored!.description).toBe('All seven fields have been updated');
    expect(stored!.releaseDate).toBe('2026-12-01');
    expect(stored!.isBreaking).toBe(true);

    // No extra entries
    const all = await getLocalStorage(page);
    expect(all.length).toBe(2);
  });

  // -------------------------------------------------------------------------
  test('TC-029 @REQ-006 @boundary @medium Edit exactly one field; all others remain intact', async ({ page }) => {
    await clickEditOnCard(page, 'Billing API');

    await page.locator('#description').fill('Only description changed');
    await page.locator('#submit-button').click();

    const stored = await getRelease(page, SEED_BILLING.id);
    expect(stored!.description).toBe('Only description changed');
    // All other fields unchanged
    expect(stored!.product).toBe(SEED_BILLING.product);
    expect(stored!.version).toBe(SEED_BILLING.version);
    expect(stored!.teamName).toBe(SEED_BILLING.teamName);
    expect(stored!.title).toBe(SEED_BILLING.title);
    expect(stored!.releaseDate).toBe(SEED_BILLING.releaseDate);
    expect(stored!.isBreaking).toBe(SEED_BILLING.isBreaking);
  });

  // -------------------------------------------------------------------------
  test('TC-030 @REQ-002 @REQ-003 @boundary @medium Edit with teamName cleared shows validation error and does not save', async ({ page }) => {
    const baselineRaw = await getRawStorage(page);

    await clickEditOnCard(page, 'Billing API');
    await page.locator('#teamName').fill('');
    await page.locator('#submit-button').click();

    // Specific error text per the app's showTeamNameError call
    const errorEl = page.locator('#team-name-error');
    await expect(errorEl).toBeVisible();
    await expect(errorEl).toHaveText('Team name is required.');

    // Still in edit mode
    await expect(page.locator('#submit-button')).toHaveText('Update Release Note');

    // localStorage unchanged
    const afterRaw = await getRawStorage(page);
    expect(afterRaw).toBe(baselineRaw);
  });

  // -------------------------------------------------------------------------
  test('TC-031 @REQ-002 @boundary @medium Edit with minimum single-character values in all mandatory fields succeeds', async ({ page }) => {
    await clickEditOnCard(page, 'Billing API');

    await page.locator('#product').fill('A');
    await page.locator('#version').fill('1');
    await page.locator('#teamName').fill('T');
    await page.locator('#title').fill('T');
    await page.locator('#description').fill('D');
    await page.locator('#releaseDate').fill('2026-01-01');
    await page.locator('#submit-button').click();

    // No validation error — edit mode exited
    await expect(page.locator('#submit-button')).toHaveText('Add Release Note');

    const stored = await getRelease(page, SEED_BILLING.id);
    expect(stored!.product).toBe('A');
    expect(stored!.version).toBe('1');
    expect(stored!.teamName).toBe('T');
    expect(stored!.title).toBe('T');
    expect(stored!.description).toBe('D');
  });

  // -------------------------------------------------------------------------
  test('TC-032 @REQ-002 @REQ-009 @boundary @high Edit then Cancel then re-Edit shows original unchanged values', async ({ page }) => {
    await clickEditOnCard(page, 'Billing API');
    await page.locator('#title').fill('TEMP_VALUE');
    await page.locator('#cancel-edit-button').click();

    // Re-open edit on Billing API
    await clickEditOnCard(page, 'Billing API');
    const titleValue = await page.locator('#title').inputValue();
    expect(titleValue).toBe(SEED_BILLING.title);
    expect(titleValue).not.toBe('TEMP_VALUE');
  });

  // -------------------------------------------------------------------------
  test('TC-033 @REQ-002 @boundary @high Edit card A then Cancel then Edit card B shows only card B values', async ({ page }) => {
    await clickEditOnCard(page, 'Billing API');
    await page.locator('#title').fill('CARD_A_TEMP');
    await page.locator('#cancel-edit-button').click();

    // Now edit Auth Service
    await clickEditOnCard(page, 'Auth Service');

    await expect(page.locator('#product')).toHaveValue('Auth Service');
    await expect(page.locator('#version')).toHaveValue('v2.0.0');
    await expect(page.locator('#teamName')).toHaveValue('Identity Team');

    const titleVal = await page.locator('#title').inputValue();
    expect(titleVal).not.toContain('CARD_A_TEMP');
    expect(titleVal).not.toContain('Billing API');
    expect(titleVal).not.toBe(SEED_BILLING.title);
  });

  // -------------------------------------------------------------------------
  // TC-034: @manual_only — requires manual 500-char paste and crash observation
  test.skip('TC-034 @REQ-003 @boundary @low @manual_only Edit title/description with 500-char text does not crash', async () => {
    // Manual: paste 500-char strings into #title and #description, verify no crash
  });

  // -------------------------------------------------------------------------
  // TC-035: @manual_only — requires XSS observation in the browser
  test.skip('TC-035 @REQ-003 @boundary @low @manual_only Edit text fields with special characters are stored and rendered safely', async () => {
    // Manual: set title to <script>alert(1)</script>, verify no script execution
  });

  // -------------------------------------------------------------------------
  test('TC-036 @REQ-002 @REQ-006 @boundary @high Toggle isBreaking from true to false and Save persists the change', async ({ page }) => {
    await clickEditOnCard(page, 'Auth Service');

    // Verify it starts checked (breaking)
    await expect(page.locator('#breaking')).toBeChecked();

    // Uncheck
    await page.locator('#breaking').uncheck();
    await page.locator('#submit-button').click();

    // Card should not show breaking badge
    const card = page.locator('.release-card').filter({ hasText: 'Auth Service' });
    const badge = card.locator('.badge');
    await expect(badge).not.toHaveText('Breaking Change');

    // localStorage
    const stored = await getRelease(page, SEED_AUTH.id);
    expect(stored!.isBreaking).toBe(false);
  });

  // -------------------------------------------------------------------------
  test('TC-037 @REQ-002 @REQ-006 @boundary @high Toggle isBreaking from false to true and Save persists the change', async ({ page }) => {
    await clickEditOnCard(page, 'Billing API');

    // Verify it starts unchecked
    await expect(page.locator('#breaking')).not.toBeChecked();

    // Check it
    await page.locator('#breaking').check();
    await page.locator('#submit-button').click();

    const card = page.locator('.release-card').filter({ hasText: 'Billing API' });
    const badge = card.locator('.badge');
    await expect(badge).toHaveText('Breaking Change');

    const stored = await getRelease(page, SEED_BILLING.id);
    expect(stored!.isBreaking).toBe(true);
  });

  // -------------------------------------------------------------------------
  test('TC-038 @REQ-012 @boundary @medium Edit operates correctly when the list contains exactly one entry', async ({ page }) => {
    await clearAndSeedStorage(page, SINGLE_ITEM_SEED);

    await expect(page.locator('.release-card')).toHaveCount(1);

    await page.locator('.release-card').first().locator('.edit-btn').click();
    await page.locator('#title').fill('Solo Card Updated');
    await page.locator('#submit-button').click();

    await expect(page.locator('.release-card')).toHaveCount(1);
    await expect(page.locator('.release-card').first().locator('.release-title')).toHaveText('Solo Card Updated');

    const all = await getLocalStorage(page);
    expect(all.length).toBe(1);
    expect(all[0].title).toBe('Solo Card Updated');
  });

  // -------------------------------------------------------------------------
  test('TC-039 @REQ-010 @boundary @medium Edit with no filters active leaves filter controls cleared after Save', async ({ page }) => {
    // Verify filters start in default state
    await expect(page.locator('#product-filter')).toHaveValue('all');
    await expect(page.locator('#breaking-filter')).toHaveValue('all');
    await expect(page.locator('#search-filter')).toHaveValue('');

    await clickEditOnCard(page, 'Billing API');
    await page.locator('#title').fill('Baseline Filter Test');
    await page.locator('#submit-button').click();

    // Filters still in default state
    await expect(page.locator('#product-filter')).toHaveValue('all');
    await expect(page.locator('#breaking-filter')).toHaveValue('all');
    await expect(page.locator('#search-filter')).toHaveValue('');

    // All cards rendered (no filter restriction)
    await expect(page.locator('.release-card')).toHaveCount(2);

    // Edited card shows new title
    const editedCard = page.locator('.release-card').filter({ hasText: 'Baseline Filter Test' });
    await expect(editedCard).toBeVisible();
  });
});
