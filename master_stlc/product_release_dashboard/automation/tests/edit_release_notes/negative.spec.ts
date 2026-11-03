import { test, expect } from '@playwright/test';
import { seedLocalStorage, getStoredReleases } from '../../helpers/localStorage';
import {
  PRODUCT_INPUT, VERSION_INPUT, TITLE_INPUT, DESCRIPTION_INPUT,
  RELEASE_DATE_INPUT, TEAM_NAME_INPUT,
  SUBMIT_BUTTON, TEAM_NAME_ERROR,
  RELEASE_CARD, CARD_PRODUCT_VER, EDIT_BTN
} from '../../helpers/selectors';

async function clickEditOnCard(page: any, productVersion: string) {
  await page
    .locator(RELEASE_CARD)
    .filter({ has: page.locator(CARD_PRODUCT_VER, { hasText: productVersion }) })
    .locator(EDIT_BTN)
    .click();
}

test.describe('Negative Scenarios', () => {

  test.beforeEach(async ({ page }) => {
    await seedLocalStorage(page, 'SD-001');
    await page.goto('/');
  });

  // ── TC-015 ───────────────────────────────────────────────────────────────

  test('TC-015: Save blocked when required field product is cleared', async ({ page }) => {
    // TC-015: Save blocked when required field product is cleared

    const before = await getStoredReleases(page);

    await clickEditOnCard(page, 'ProductA - v1.0.0');

    // Confirm the field carries the required attribute
    await expect(page.locator(PRODUCT_INPUT)).toHaveAttribute('required', '');

    // Clear the field and attempt to submit
    await page.locator(PRODUCT_INPUT).fill('');
    await page.locator(SUBMIT_BUTTON).click();

    // Browser HTML5 validation prevents submission — localStorage unchanged
    const after = await getStoredReleases(page);
    expect(after).toEqual(before);

    // Form still in edit mode (submit button still reads Update Release Note)
    await expect(page.locator(SUBMIT_BUTTON)).toHaveText('Update Release Note');
  });

  // ── TC-016 ───────────────────────────────────────────────────────────────

  test('TC-016: Save blocked when required field version is cleared', async ({ page }) => {
    // TC-016: Save blocked when required field version is cleared

    const before = await getStoredReleases(page);

    await clickEditOnCard(page, 'ProductA - v1.0.0');
    await expect(page.locator(VERSION_INPUT)).toHaveAttribute('required', '');

    await page.locator(VERSION_INPUT).fill('');
    await page.locator(SUBMIT_BUTTON).click();

    const after = await getStoredReleases(page);
    expect(after).toEqual(before);
    await expect(page.locator(SUBMIT_BUTTON)).toHaveText('Update Release Note');
  });

  // ── TC-017 ───────────────────────────────────────────────────────────────

  test('TC-017: Save blocked when required field title is cleared', async ({ page }) => {
    // TC-017: Save blocked when required field title is cleared

    const before = await getStoredReleases(page);

    await clickEditOnCard(page, 'ProductA - v1.0.0');
    await expect(page.locator(TITLE_INPUT)).toHaveAttribute('required', '');

    await page.locator(TITLE_INPUT).fill('');
    await page.locator(SUBMIT_BUTTON).click();

    const after = await getStoredReleases(page);
    expect(after).toEqual(before);
    await expect(page.locator(SUBMIT_BUTTON)).toHaveText('Update Release Note');
  });

  // ── TC-018 ───────────────────────────────────────────────────────────────

  test('TC-018: Save blocked when required field description is cleared', async ({ page }) => {
    // TC-018: Save blocked when required field description is cleared

    const before = await getStoredReleases(page);

    await clickEditOnCard(page, 'ProductA - v1.0.0');
    await expect(page.locator(DESCRIPTION_INPUT)).toHaveAttribute('required', '');

    await page.locator(DESCRIPTION_INPUT).fill('');
    await page.locator(SUBMIT_BUTTON).click();

    const after = await getStoredReleases(page);
    expect(after).toEqual(before);
    await expect(page.locator(SUBMIT_BUTTON)).toHaveText('Update Release Note');
  });

  // ── TC-019 ───────────────────────────────────────────────────────────────

  test('TC-019: Save blocked when required field releaseDate is cleared', async ({ page }) => {
    // TC-019: Save blocked when required field releaseDate is cleared

    const before = await getStoredReleases(page);

    await clickEditOnCard(page, 'ProductA - v1.0.0');
    await expect(page.locator(RELEASE_DATE_INPUT)).toHaveAttribute('required', '');

    // Clear the date input value via evaluate (fill('') is unreliable for date inputs)
    await page.locator(RELEASE_DATE_INPUT).evaluate((el: HTMLInputElement) => { el.value = ''; });
    await page.locator(SUBMIT_BUTTON).click();

    // Form was NOT submitted — localStorage unchanged
    const after = await getStoredReleases(page);
    expect(after).toEqual(before);
    await expect(page.locator(SUBMIT_BUTTON)).toHaveText('Update Release Note');
  });

  // ── TC-020 ───────────────────────────────────────────────────────────────

  test('TC-020: Save blocked with custom error when teamName is cleared', async ({ page }) => {
    // TC-020: Save blocked with custom error when teamName is cleared
    // teamName uses custom JS validation (NOT HTML5 required attribute)

    const before = await getStoredReleases(page);

    await clickEditOnCard(page, 'ProductA - v1.0.0');

    // teamName does NOT have the required attribute
    await expect(page.locator(TEAM_NAME_INPUT)).not.toHaveAttribute('required', '');

    await page.locator(TEAM_NAME_INPUT).fill('');
    await page.locator(SUBMIT_BUTTON).click();

    // Custom inline error is visible
    await expect(page.locator(TEAM_NAME_ERROR)).toHaveText('Team name is required.');

    // teamName field receives focus
    const focusedId = await page.evaluate(() => (document.activeElement as HTMLElement)?.id);
    expect(focusedId).toBe('teamName');

    // Form was NOT submitted — localStorage unchanged
    const after = await getStoredReleases(page);
    expect(after).toEqual(before);
  });

  // ── TC-021 ───────────────────────────────────────────────────────────────

  test('TC-021: Save without modifying any field succeeds and preserves data', async ({ page }) => {
    // TC-021: Save without modifying any field succeeds and preserves data

    const before = await getStoredReleases(page);
    const target = before.find((r: any) => r.id === 'test-id-001')!;

    // Listen for JS errors
    const jsErrors: string[] = [];
    page.on('pageerror', (err: Error) => jsErrors.push(err.message));

    await clickEditOnCard(page, 'ProductA - v1.0.0');
    // Do NOT modify any field
    await page.locator(SUBMIT_BUTTON).click();

    // No JS errors
    expect(jsErrors).toHaveLength(0);

    // Entry values identical to pre-edit state
    const after = await getStoredReleases(page);
    const saved = after.find((r: any) => r.id === 'test-id-001');
    expect(saved).toBeDefined();
    expect(saved.product).toBe(target.product);
    expect(saved.version).toBe(target.version);
    expect(saved.title).toBe(target.title);
    expect(saved.description).toBe(target.description);
    expect(saved.releaseDate).toBe(target.releaseDate);
    expect(saved.teamName).toBe(target.teamName);
    expect(saved.isBreaking).toBe(target.isBreaking);

    // Total count unchanged
    expect(after.length).toBe(before.length);

    // localStorage is a valid JSON array
    const raw = await page.evaluate((key: string) => localStorage.getItem(key), 'releaseNotesDashboard.releases');
    expect(() => JSON.parse(raw!)).not.toThrow();
    expect(Array.isArray(JSON.parse(raw!))).toBe(true);
  });

  // TC-022: MANUAL ONLY — localStorage full on Save — silent failure
  // Skipped: requires filling localStorage to browser quota (unsafe to automate)
});
