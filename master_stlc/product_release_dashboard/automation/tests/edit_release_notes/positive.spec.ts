import { test, expect } from '@playwright/test';
import { seedLocalStorage, getStoredReleases } from '../../helpers/localStorage';
import {
  PRODUCT_INPUT, VERSION_INPUT, TITLE_INPUT, DESCRIPTION_INPUT,
  RELEASE_DATE_INPUT, TEAM_NAME_INPUT, BREAKING_CHECKBOX,
  SUBMIT_BUTTON, CANCEL_EDIT_BUTTON,
  RELEASE_CARD, CARD_PRODUCT_VER, EDIT_BTN,
  PRODUCT_FILTER_SELECT, SEARCH_FILTER_INPUT
} from '../../helpers/selectors';

// Click Edit on the release-card whose product-version text contains the given string
async function clickEditOnCard(page: any, productVersion: string) {
  await page
    .locator(RELEASE_CARD)
    .filter({ has: page.locator(CARD_PRODUCT_VER, { hasText: productVersion }) })
    .locator(EDIT_BTN)
    .click();
}

test.describe('Positive Scenarios', () => {

  // ── SD-001 group (TC-001 to TC-007, TC-009 to TC-014) ────────────────────

  test.describe('with SD-001', () => {

    test.beforeEach(async ({ page }) => {
      await seedLocalStorage(page, 'SD-001');
      await page.goto('/');
    });

    test('TC-001: Edit button present and triggers form pre-fill', async ({ page }) => {
      // TC-001: Edit button present and triggers form pre-fill
      // test-id-001 = ProductA / v1.0.0 / TeamAlpha / isBreaking=true

      await clickEditOnCard(page, 'ProductA - v1.0.0');

      await expect(page.locator(PRODUCT_INPUT)).toHaveValue('ProductA');
      await expect(page.locator(VERSION_INPUT)).toHaveValue('v1.0.0');
      await expect(page.locator(TITLE_INPUT)).toHaveValue('ProductA release notes v1');
      await expect(page.locator(DESCRIPTION_INPUT)).toHaveValue('This is the first release note for ProductA.');
      await expect(page.locator(RELEASE_DATE_INPUT)).toHaveValue('2024-01-15');
      await expect(page.locator(TEAM_NAME_INPUT)).toHaveValue('TeamAlpha');
      await expect(page.locator(BREAKING_CHECKBOX)).toBeChecked();
      await expect(page.locator(SUBMIT_BUTTON)).toHaveText('Update Release Note');
      await expect(page.locator(CANCEL_EDIT_BUTTON)).toBeVisible();
    });

    test('TC-002: Save after modifying product field updates localStorage', async ({ page }) => {
      // TC-002: Save after modifying product field updates localStorage

      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await page.locator(PRODUCT_INPUT).fill('ProductX');
      await page.locator(SUBMIT_BUTTON).click();

      const releases = await getStoredReleases(page);
      const edited = releases.find((r: any) => r.id === 'test-id-001');
      expect(edited).toBeDefined();
      expect(edited.product).toBe('ProductX');
      // Other fields unchanged
      expect(edited.version).toBe('v1.0.0');
      expect(edited.teamName).toBe('TeamAlpha');
      expect(edited.title).toBe('ProductA release notes v1');
      expect(edited.isBreaking).toBe(true);

      await expect(
        page.locator(RELEASE_CARD).filter({
          has: page.locator(CARD_PRODUCT_VER, { hasText: 'ProductX - v1.0.0' })
        })
      ).toBeVisible();
    });

    test('TC-003: Save after modifying version field updates localStorage', async ({ page }) => {
      // TC-003: Save after modifying version field updates localStorage

      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await page.locator(VERSION_INPUT).fill('9.9.9');
      await page.locator(SUBMIT_BUTTON).click();

      const releases = await getStoredReleases(page);
      const edited = releases.find((r: any) => r.id === 'test-id-001');
      expect(edited).toBeDefined();
      expect(edited.version).toBe('9.9.9');

      await expect(
        page.locator(RELEASE_CARD).filter({
          has: page.locator(CARD_PRODUCT_VER, { hasText: 'ProductA - 9.9.9' })
        })
      ).toBeVisible();
    });

    test('TC-004: Save after modifying title and description updates both fields', async ({ page }) => {
      // TC-004: Save after modifying title and description updates both fields

      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await page.locator(TITLE_INPUT).fill('Updated Title Text');
      await page.locator(DESCRIPTION_INPUT).fill('Updated description content.');
      await page.locator(SUBMIT_BUTTON).click();

      const releases = await getStoredReleases(page);
      const edited = releases.find((r: any) => r.id === 'test-id-001');
      expect(edited).toBeDefined();
      expect(edited.title).toBe('Updated Title Text');
      expect(edited.description).toBe('Updated description content.');
      // Other fields unchanged
      expect(edited.product).toBe('ProductA');
      expect(edited.version).toBe('v1.0.0');
      expect(edited.releaseDate).toBe('2024-01-15');
      expect(edited.teamName).toBe('TeamAlpha');
      expect(edited.isBreaking).toBe(true);
    });

    test('TC-005: Save after modifying releaseDate updates date in localStorage', async ({ page }) => {
      // TC-005: Save after modifying releaseDate updates date in localStorage

      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await page.locator(RELEASE_DATE_INPUT).fill('2024-06-15');
      await page.locator(SUBMIT_BUTTON).click();

      const releases = await getStoredReleases(page);
      const edited = releases.find((r: any) => r.id === 'test-id-001');
      expect(edited).toBeDefined();
      expect(edited.releaseDate).toBe('2024-06-15');
    });

    test('TC-006: Save after modifying teamName updates teamName in localStorage', async ({ page }) => {
      // TC-006: Save after modifying teamName updates teamName in localStorage

      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await page.locator(TEAM_NAME_INPUT).fill('AlphaTeam');
      await page.locator(SUBMIT_BUTTON).click();

      const releases = await getStoredReleases(page);
      const edited = releases.find((r: any) => r.id === 'test-id-001');
      expect(edited).toBeDefined();
      expect(edited.teamName).toBe('AlphaTeam');
      // Other fields unchanged
      expect(edited.product).toBe('ProductA');
      expect(edited.version).toBe('v1.0.0');
    });

    test('TC-007: Save with breaking flag toggled from false to true', async ({ page }) => {
      // TC-007: Save with breaking flag toggled from false to true
      // test-id-002 = ProductA / v1.1.0 / isBreaking=false

      await clickEditOnCard(page, 'ProductA - v1.1.0');
      await expect(page.locator(BREAKING_CHECKBOX)).not.toBeChecked();
      await page.locator(BREAKING_CHECKBOX).check();
      await page.locator(SUBMIT_BUTTON).click();

      const releases = await getStoredReleases(page);
      const edited = releases.find((r: any) => r.id === 'test-id-002');
      expect(edited).toBeDefined();
      expect(edited.isBreaking).toBe(true);
    });

    test('TC-009: Save after modifying all editable fields; id remains unchanged', async ({ page }) => {
      // TC-009: Save after modifying all editable fields; id remains unchanged

      const beforeReleases = await getStoredReleases(page);
      const originalCount = beforeReleases.length;

      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await page.locator(PRODUCT_INPUT).fill('NewProduct');
      await page.locator(VERSION_INPUT).fill('8.8.8');
      await page.locator(TITLE_INPUT).fill('New Title');
      await page.locator(DESCRIPTION_INPUT).fill('New description.');
      await page.locator(RELEASE_DATE_INPUT).fill('2025-12-31');
      await page.locator(TEAM_NAME_INPUT).fill('NewTeam');
      await page.locator(BREAKING_CHECKBOX).check();
      await page.locator(SUBMIT_BUTTON).click();

      const releases = await getStoredReleases(page);
      expect(releases.length).toBe(originalCount);

      const matching = releases.filter((r: any) => r.id === 'test-id-001');
      expect(matching).toHaveLength(1);

      const edited = matching[0];
      expect(edited.product).toBe('NewProduct');
      expect(edited.version).toBe('8.8.8');
      expect(edited.title).toBe('New Title');
      expect(edited.description).toBe('New description.');
      expect(edited.releaseDate).toBe('2025-12-31');
      expect(edited.teamName).toBe('NewTeam');
      expect(edited.isBreaking).toBe(true);
    });

    test('TC-010: Cancel after modifying fields discards all changes', async ({ page }) => {
      // TC-010: Cancel after modifying fields discards all changes

      const before = await getStoredReleases(page);

      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await page.locator(PRODUCT_INPUT).fill('DiscardedProduct');
      await page.locator(TITLE_INPUT).fill('Discarded Title');
      await page.locator(DESCRIPTION_INPUT).fill('Discarded description.');

      // No confirm dialog for Cancel — just click
      await page.locator(CANCEL_EDIT_BUTTON).click();

      // Form back to create mode immediately
      await expect(page.locator(SUBMIT_BUTTON)).toHaveText('Add Release Note');
      await expect(page.locator(CANCEL_EDIT_BUTTON)).toBeHidden();
      await expect(page.locator(PRODUCT_INPUT)).toHaveValue('');

      // localStorage unchanged
      const after = await getStoredReleases(page);
      expect(after).toEqual(before);
    });

    test('TC-011: Form returns to create mode after Save', async ({ page }) => {
      // TC-011: Form returns to create mode after Save

      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await expect(page.locator(SUBMIT_BUTTON)).toHaveText('Update Release Note');
      await expect(page.locator(CANCEL_EDIT_BUTTON)).toBeVisible();

      // Save without changes
      await page.locator(SUBMIT_BUTTON).click();

      await expect(page.locator(SUBMIT_BUTTON)).toHaveText('Add Release Note');
      await expect(page.locator(CANCEL_EDIT_BUTTON)).toBeHidden();
      await expect(page.locator(PRODUCT_INPUT)).toHaveValue('');
      await expect(page.locator(VERSION_INPUT)).toHaveValue('');
      await expect(page.locator(TITLE_INPUT)).toHaveValue('');
      await expect(page.locator(DESCRIPTION_INPUT)).toHaveValue('');
      await expect(page.locator(RELEASE_DATE_INPUT)).toHaveValue('');
      await expect(page.locator(TEAM_NAME_INPUT)).toHaveValue('');
      await expect(page.locator(BREAKING_CHECKBOX)).not.toBeChecked();
    });

    test('TC-012: Form returns to create mode after Cancel', async ({ page }) => {
      // TC-012: Form returns to create mode after Cancel

      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await expect(page.locator(SUBMIT_BUTTON)).toHaveText('Update Release Note');
      await expect(page.locator(CANCEL_EDIT_BUTTON)).toBeVisible();

      await page.locator(CANCEL_EDIT_BUTTON).click();

      await expect(page.locator(SUBMIT_BUTTON)).toHaveText('Add Release Note');
      await expect(page.locator(CANCEL_EDIT_BUTTON)).toBeHidden();
      await expect(page.locator(PRODUCT_INPUT)).toHaveValue('');
      await expect(page.locator(VERSION_INPUT)).toHaveValue('');
      await expect(page.locator(TITLE_INPUT)).toHaveValue('');
      await expect(page.locator(DESCRIPTION_INPUT)).toHaveValue('');
      await expect(page.locator(RELEASE_DATE_INPUT)).toHaveValue('');
      await expect(page.locator(TEAM_NAME_INPUT)).toHaveValue('');
      await expect(page.locator(BREAKING_CHECKBOX)).not.toBeChecked();
    });

    test('TC-013: Active product filter persists after Save', async ({ page }) => {
      // TC-013: Active product filter persists after Save
      // SD-001 has 2 ProductA entries (test-id-001, test-id-002)

      await page.selectOption(PRODUCT_FILTER_SELECT, 'ProductA');
      await expect(page.locator(RELEASE_CARD)).toHaveCount(2);

      await page.locator(RELEASE_CARD).first().locator(EDIT_BTN).click();
      await page.locator(TITLE_INPUT).fill('Filter Persistence Test Title');
      await page.locator(SUBMIT_BUTTON).click();

      // Filter still shows ProductA
      await expect(page.locator(PRODUCT_FILTER_SELECT)).toHaveValue('ProductA');

      // List remains filtered — all visible cards have ProductA
      const cards = page.locator(RELEASE_CARD);
      const count = await cards.count();
      expect(count).toBeGreaterThan(0);
      for (let i = 0; i < count; i++) {
        await expect(cards.nth(i).locator(CARD_PRODUCT_VER)).toContainText('ProductA');
      }

      // Updated title visible in the filtered list
      await expect(
        page.locator(RELEASE_CARD).filter({ hasText: 'Filter Persistence Test Title' })
      ).toBeVisible();
    });

    test('TC-014: Active search filter persists after Cancel', async ({ page }) => {
      // TC-014: Active search filter persists after Cancel
      // test-id-002 description contains "keywordX"

      await page.locator(SEARCH_FILTER_INPUT).fill('keywordX');
      const matchedBefore = await page.locator(RELEASE_CARD).count();
      expect(matchedBefore).toBeGreaterThan(0);

      await page.locator(RELEASE_CARD).first().locator(EDIT_BTN).click();
      await page.locator(DESCRIPTION_INPUT).fill('Should be discarded — still has keywordX.');

      await page.locator(CANCEL_EDIT_BUTTON).click();

      // Search filter still active
      await expect(page.locator(SEARCH_FILTER_INPUT)).toHaveValue('keywordX');
      const matchedAfter = await page.locator(RELEASE_CARD).count();
      expect(matchedAfter).toBeGreaterThan(0);

      // localStorage unchanged — original description preserved
      const stored = await getStoredReleases(page);
      const entry = stored.find((r: any) => r.id === 'test-id-002');
      expect(entry).toBeDefined();
      expect(entry.description).toBe('Minor update including keywordX improvements and fixes.');
    });
  });

  // ── SD-003 group (TC-008) ─────────────────────────────────────────────────

  test.describe('with SD-003', () => {

    test.beforeEach(async ({ page }) => {
      await seedLocalStorage(page, 'SD-003');
      await page.goto('/');
    });

    test('TC-008: Save with breaking flag toggled from true to false', async ({ page }) => {
      // TC-008: Save with breaking flag toggled from true to false
      // SD-003 test-id-001 = ProductA / v2.0.0 / isBreaking=true

      await page
        .locator(RELEASE_CARD)
        .filter({ has: page.locator(CARD_PRODUCT_VER, { hasText: 'ProductA - v2.0.0' }) })
        .locator(EDIT_BTN)
        .click();

      await expect(page.locator(BREAKING_CHECKBOX)).toBeChecked();
      await page.locator(BREAKING_CHECKBOX).uncheck();
      await page.locator(SUBMIT_BUTTON).click();

      const releases = await getStoredReleases(page);
      const edited = releases.find((r: any) => r.id === 'test-id-001');
      expect(edited).toBeDefined();
      expect(edited.isBreaking).toBe(false);
    });
  });
});
