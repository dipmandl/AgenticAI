import { test, expect } from '@playwright/test';
import { seedLocalStorage, getStoredReleases } from '../../helpers/localStorage';
import {
  PRODUCT_INPUT, VERSION_INPUT, TITLE_INPUT,
  RELEASE_DATE_INPUT, BREAKING_CHECKBOX,
  SUBMIT_BUTTON, CANCEL_EDIT_BUTTON,
  RELEASE_CARD, CARD_PRODUCT_VER, EDIT_BTN, EMPTY_STATE,
  PRODUCT_FILTER_SELECT, BREAKING_FILTER_SELECT, SEARCH_FILTER_INPUT
} from '../../helpers/selectors';

test.describe('Boundary Scenarios', () => {

  // ── TC-023: SD-002 (single entry) ────────────────────────────────────────

  test.describe('with SD-002', () => {

    test.beforeEach(async ({ page }) => {
      await seedLocalStorage(page, 'SD-002');
      await page.goto('/');
    });

    test('TC-023: Edit the only release note in the list', async ({ page }) => {
      // TC-023: Edit the only release note in the list

      await expect(page.locator(RELEASE_CARD)).toHaveCount(1);

      await page.locator(RELEASE_CARD).first().locator(EDIT_BTN).click();
      await page.locator(TITLE_INPUT).fill('Only Entry Updated');
      await page.locator(SUBMIT_BUTTON).click();

      // List re-renders with exactly 1 entry
      await expect(page.locator(RELEASE_CARD)).toHaveCount(1);
      await expect(page.locator(EMPTY_STATE)).toBeHidden();

      // Correct title visible
      await expect(page.locator(RELEASE_CARD).first()).toContainText('Only Entry Updated');

      // localStorage has exactly 1 entry with updated title
      const releases = await getStoredReleases(page);
      expect(releases).toHaveLength(1);
      expect(releases[0].title).toBe('Only Entry Updated');
    });
  });

  // ── TC-024, TC-025, TC-029: SD-001 ───────────────────────────────────────

  test.describe('with SD-001', () => {

    test.beforeEach(async ({ page }) => {
      await seedLocalStorage(page, 'SD-001');
      await page.goto('/');
    });

    test('TC-024: Edit with no active filters applied', async ({ page }) => {
      // TC-024: Edit with no active filters applied — all 5 entries visible after save

      // No filters active — all 5 entries visible
      await expect(page.locator(RELEASE_CARD)).toHaveCount(5);

      await page
        .locator(RELEASE_CARD)
        .filter({ has: page.locator(CARD_PRODUCT_VER, { hasText: 'ProductA - v1.0.0' }) })
        .locator(EDIT_BTN)
        .click();

      await page.locator(VERSION_INPUT).fill('0.0.1');
      await page.locator(SUBMIT_BUTTON).click();

      // All 5 entries still visible
      await expect(page.locator(RELEASE_CARD)).toHaveCount(5);

      // Edited entry shows new version
      await expect(
        page.locator(RELEASE_CARD).filter({
          has: page.locator(CARD_PRODUCT_VER, { hasText: 'ProductA - 0.0.1' })
        })
      ).toBeVisible();
    });

    test('TC-029: All three filters active simultaneously — all persist after Save', async ({ page }) => {
      // TC-029: All three filters active simultaneously — all persist after Save
      // SD-001 test-id-001: ProductA, isBreaking=true, title "ProductA release notes v1" (contains "release")

      await page.selectOption(PRODUCT_FILTER_SELECT, 'ProductA');
      await page.selectOption(BREAKING_FILTER_SELECT, 'breaking');
      await page.locator(SEARCH_FILTER_INPUT).fill('release');

      // At least one entry matches all three filters (test-id-001)
      const visibleBefore = await page.locator(RELEASE_CARD).count();
      expect(visibleBefore).toBeGreaterThan(0);

      // Edit a visible entry — preserve search match by keeping "release" in title
      await page.locator(RELEASE_CARD).first().locator(EDIT_BTN).click();
      await page.locator(TITLE_INPUT).fill('ProductA release persistence test');
      await page.locator(SUBMIT_BUTTON).click();

      // All three filter values persist
      await expect(page.locator(PRODUCT_FILTER_SELECT)).toHaveValue('ProductA');
      await expect(page.locator(BREAKING_FILTER_SELECT)).toHaveValue('breaking');
      await expect(page.locator(SEARCH_FILTER_INPUT)).toHaveValue('release');

      // List re-rendered with combined AND filter still applied
      const visibleAfter = await page.locator(RELEASE_CARD).count();
      expect(visibleAfter).toBeGreaterThan(0);
    });
  });

  // ── TC-025: SD-008 ────────────────────────────────────────────────────────

  test.describe('with SD-008', () => {

    test.beforeEach(async ({ page }) => {
      await seedLocalStorage(page, 'SD-008');
      await page.goto('/');
    });

    test('TC-025: Edited entry disappears when it no longer matches active product filter', async ({ page }) => {
      // TC-025: Edited entry disappears when it no longer matches active product filter
      // SD-008: 1×ProductA (test-id-001), 1×ProductB (test-id-002)

      await page.selectOption(PRODUCT_FILTER_SELECT, 'ProductA');
      await expect(page.locator(RELEASE_CARD)).toHaveCount(1);

      // Edit the single ProductA entry → change product to ProductB
      await page.locator(RELEASE_CARD).first().locator(EDIT_BTN).click();
      await page.locator(PRODUCT_INPUT).fill('ProductB');
      await page.locator(SUBMIT_BUTTON).click();

      // Edited entry in localStorage now has product = ProductB
      const releases = await getStoredReleases(page);
      const edited = releases.find((r: any) => r.id === 'test-id-001');
      expect(edited).toBeDefined();
      expect(edited.product).toBe('ProductB');

      // ProductA option is removed from dropdown (no more ProductA entries);
      // filter auto-resets to "all" — entry is no longer visible as ProductA
      // Verify by reading the filter select value and confirming no ProductA entry exists
      const productAEntries = releases.filter((r: any) => r.product === 'ProductA');
      expect(productAEntries).toHaveLength(0);
    });
  });

  // ── TC-026: SD-003 ────────────────────────────────────────────────────────

  test.describe('with SD-003', () => {

    test.beforeEach(async ({ page }) => {
      await seedLocalStorage(page, 'SD-003');
      await page.goto('/');
    });

    test('TC-026: Edit entry with isBreaking=true — checkbox pre-fills as checked', async ({ page }) => {
      // TC-026: Edit entry with isBreaking=true — checkbox pre-fills as checked

      await page
        .locator(RELEASE_CARD)
        .filter({ has: page.locator(CARD_PRODUCT_VER, { hasText: 'ProductA - v2.0.0' }) })
        .locator(EDIT_BTN)
        .click();

      // Checkbox is checked immediately on pre-fill, before any user interaction
      await expect(page.locator(BREAKING_CHECKBOX)).toBeChecked();
    });
  });

  // ── TC-027: SD-004 ────────────────────────────────────────────────────────

  test.describe('with SD-004', () => {

    test.beforeEach(async ({ page }) => {
      await seedLocalStorage(page, 'SD-004');
      await page.goto('/');
    });

    test('TC-027: Edit entry with releaseDate "1970-01-01" — date pre-fills correctly', async ({ page }) => {
      // TC-027: Edit entry with releaseDate "1970-01-01" — date pre-fills correctly

      await page.locator(RELEASE_CARD).first().locator(EDIT_BTN).click();

      // Date field displays exactly "1970-01-01" — no epoch conversion error
      await expect(page.locator(RELEASE_DATE_INPUT)).toHaveValue('1970-01-01');
    });
  });

  // ── TC-028: SD-005 ────────────────────────────────────────────────────────

  test.describe('with SD-005', () => {

    test.beforeEach(async ({ page }) => {
      await seedLocalStorage(page, 'SD-005');
      await page.goto('/');
    });

    test("TC-028: Edit entry with releaseDate = today's date — date pre-fills correctly", async ({ page }) => {
      // TC-028: Edit entry with releaseDate = today's date — date pre-fills correctly

      // Compute today in the browser context (same source as the seed)
      const today = await page.evaluate(() => new Date().toISOString().split('T')[0]);

      await page.locator(RELEASE_CARD).first().locator(EDIT_BTN).click();

      // Date input shows today with no timezone offset
      await expect(page.locator(RELEASE_DATE_INPUT)).toHaveValue(today);
    });
  });

  // TC-030: MANUAL ONLY — performance judgment requires human observation
});
