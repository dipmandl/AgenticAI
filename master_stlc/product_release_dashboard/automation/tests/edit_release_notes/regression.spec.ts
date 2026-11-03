import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import { seedLocalStorage, getStoredReleases } from '../../helpers/localStorage';
import {
  PRODUCT_INPUT, VERSION_INPUT, TITLE_INPUT, DESCRIPTION_INPUT,
  RELEASE_DATE_INPUT, TEAM_NAME_INPUT, BREAKING_CHECKBOX,
  SUBMIT_BUTTON,
  RELEASE_CARD, CARD_PRODUCT_VER, EDIT_BTN, DELETE_BTN,
  PRODUCT_FILTER_SELECT, BREAKING_FILTER_SELECT, SEARCH_FILTER_INPUT,
  EXPORT_CSV_BUTTON, STORAGE_KEY
} from '../../helpers/selectors';

async function clickEditOnCard(page: any, productVersion: string) {
  await page
    .locator(RELEASE_CARD)
    .filter({ has: page.locator(CARD_PRODUCT_VER, { hasText: productVersion }) })
    .locator(EDIT_BTN)
    .click();
}

test.describe('Regression Scenarios', () => {

  // ── SD-001 group ──────────────────────────────────────────────────────────

  test.describe('with SD-001', () => {

    test.beforeEach(async ({ page }) => {
      await seedLocalStorage(page, 'SD-001');
      await page.goto('/');
    });

    test('TC-031: Create → Edit → Create: second create adds new entry with blank form', async ({ page }) => {
      // TC-031: Create → Edit → Create: second create adds new entry with blank form

      const initialReleases = await getStoredReleases(page);
      const initialCount = initialReleases.length; // 5

      // Step 1: Edit entry A (test-id-001, ProductA - v1.0.0) → change product
      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await page.locator(PRODUCT_INPUT).fill('EditedProduct');
      await page.locator(SUBMIT_BUTTON).click();

      // Form returns to create mode with blank fields
      await expect(page.locator(SUBMIT_BUTTON)).toHaveText('Add Release Note');
      await expect(page.locator(PRODUCT_INPUT)).toHaveValue('');

      // Step 2: Fill the create form with distinct new values
      await page.locator(PRODUCT_INPUT).fill('NewEntryProduct');
      await page.locator(VERSION_INPUT).fill('1.0.0');
      await page.locator(TITLE_INPUT).fill('New Entry Title');
      await page.locator(DESCRIPTION_INPUT).fill('New description');
      await page.locator(RELEASE_DATE_INPUT).fill('2025-01-01');
      await page.locator(TEAM_NAME_INPUT).fill('NewTeam');
      await page.locator(SUBMIT_BUTTON).click();

      const releases = await getStoredReleases(page);

      // Total count = initial + 1
      expect(releases.length).toBe(initialCount + 1);

      // New entry has the values from the create form — no stale "EditedProduct" leaked
      const newEntry = releases.find((r: any) => r.product === 'NewEntryProduct');
      expect(newEntry).toBeDefined();
      expect(newEntry.title).toBe('New Entry Title');
      expect(newEntry.teamName).toBe('NewTeam');

      // New entry id is distinct from all pre-existing ids
      const preExistingIds = initialReleases.map((r: any) => r.id);
      expect(preExistingIds).not.toContain(newEntry.id);

      // Originally edited entry A still exists
      const editedA = releases.find((r: any) => r.id === 'test-id-001');
      expect(editedA).toBeDefined();
      expect(editedA.product).toBe('EditedProduct');
    });

    test('TC-032: Edit → Save → Delete: delete removes correct entry and list re-renders', async ({ page }) => {
      // TC-032: Edit → Save → Delete: delete removes correct entry and list re-renders

      // Accept the confirm dialog for delete
      page.on('dialog', (dialog: any) => dialog.accept());

      // Edit test-id-001 (ProductA - v1.0.0) → change title
      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await page.locator(TITLE_INPUT).fill('Pre-Delete Title');
      await page.locator(SUBMIT_BUTTON).click();

      // Verify edit persisted
      let releases = await getStoredReleases(page);
      expect(releases.find((r: any) => r.id === 'test-id-001')?.title).toBe('Pre-Delete Title');

      const countBefore = releases.length;

      // Delete the edited entry
      await page
        .locator(RELEASE_CARD)
        .filter({ has: page.locator(CARD_PRODUCT_VER, { hasText: 'ProductA - v1.0.0' }) })
        .locator(DELETE_BTN)
        .click();

      // Wait for list to re-render
      await page.waitForFunction(() => {
        const raw = localStorage.getItem('releaseNotesDashboard.releases');
        if (!raw) return false;
        const arr = JSON.parse(raw);
        return !arr.find((r: any) => r.id === 'test-id-001');
      });

      releases = await getStoredReleases(page);

      // test-id-001 removed from localStorage
      expect(releases.find((r: any) => r.id === 'test-id-001')).toBeUndefined();
      expect(releases.length).toBe(countBefore - 1);

      // test-id-001 card no longer visible
      const remainingCard = page.locator(RELEASE_CARD).filter({
        has: page.locator(CARD_PRODUCT_VER, { hasText: 'ProductA - v1.0.0' })
      });
      await expect(remainingCard).toHaveCount(0);

      // Other entries intact
      expect(releases.find((r: any) => r.id === 'test-id-002')).toBeDefined();
      expect(releases.find((r: any) => r.id === 'test-id-003')).toBeDefined();
    });

    test('TC-033: Edit → Save → Export: CSV export reflects updated values', async ({ page }) => {
      // TC-033: Edit → Save → Export: CSV export reflects updated values

      // Edit entry and save
      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await page.locator(PRODUCT_INPUT).fill('ExportTestProduct');
      await page.locator(TITLE_INPUT).fill('ExportTestTitle');
      await page.locator(SUBMIT_BUTTON).click();

      // Trigger CSV export and capture download
      const [download] = await Promise.all([
        page.waitForEvent('download'),
        page.locator(EXPORT_CSV_BUTTON).click()
      ]);

      const filePath = await download.path();
      expect(filePath).toBeTruthy();

      const csvContent = fs.readFileSync(filePath!, 'utf-8');

      // CSV header matches expected schema
      const lines = csvContent.split('\n').filter(Boolean);
      expect(lines[0]).toBe('"product","version","teamName","title","description","releaseDate","isBreaking"');

      // Updated values present in CSV
      expect(csvContent).toContain('ExportTestProduct');
      expect(csvContent).toContain('ExportTestTitle');

      // Pre-edit values of the modified entry are NOT in CSV
      expect(csvContent).not.toContain('ProductA release notes v1');
    });

    test('TC-034: Edit → Cancel → Create: create form is blank and adds new entry', async ({ page }) => {
      // TC-034: Edit → Cancel → Create: create form is blank and adds new entry

      const before = await getStoredReleases(page);
      const originalEntry = before.find((r: any) => r.id === 'test-id-001')!;

      // Edit and then cancel
      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await page.locator(PRODUCT_INPUT).fill('CancelledProduct');
      await page.locator(TITLE_INPUT).fill('Cancelled Title');
      await page.locator('button#cancel-edit-button').click();

      // Form is blank
      await expect(page.locator(PRODUCT_INPUT)).toHaveValue('');
      await expect(page.locator(TITLE_INPUT)).toHaveValue('');

      // Fill create form with fresh values
      await page.locator(PRODUCT_INPUT).fill('FreshProduct');
      await page.locator(VERSION_INPUT).fill('2.0.0');
      await page.locator(TITLE_INPUT).fill('Fresh Title');
      await page.locator(DESCRIPTION_INPUT).fill('Fresh content');
      await page.locator(RELEASE_DATE_INPUT).fill('2025-06-01');
      await page.locator(TEAM_NAME_INPUT).fill('FreshTeam');
      await page.locator(SUBMIT_BUTTON).click();

      const after = await getStoredReleases(page);

      // New entry has only the fresh values — no stale cancelled values
      const newEntry = after.find((r: any) => r.product === 'FreshProduct');
      expect(newEntry).toBeDefined();
      expect(newEntry.title).toBe('Fresh Title');
      expect(newEntry.product).toBe('FreshProduct');
      expect(newEntry.product).not.toBe('CancelledProduct');

      // New entry has a unique id
      const preExistingIds = before.map((r: any) => r.id);
      expect(preExistingIds).not.toContain(newEntry.id);

      // Original entry (that was cancelled-edited) unchanged
      const unchanged = after.find((r: any) => r.id === 'test-id-001');
      expect(unchanged).toBeDefined();
      expect(unchanged.product).toBe(originalEntry.product);
      expect(unchanged.title).toBe(originalEntry.title);
    });

    test('TC-035: Edit one entry — all other entries remain unchanged in localStorage', async ({ page }) => {
      // TC-035: Edit one entry — all other entries remain unchanged in localStorage

      const before = await getStoredReleases(page);
      const originals = Object.fromEntries(before.map((r: any) => [r.id, { ...r }]));

      // Edit entry 3 (test-id-003: ProductB - v2.0.0)
      await clickEditOnCard(page, 'ProductB - v2.0.0');
      await page.locator(PRODUCT_INPUT).fill('ModifiedProduct');
      await page.locator(VERSION_INPUT).fill('7.7.7');
      await page.locator(TITLE_INPUT).fill('Modified Title');
      await page.locator(SUBMIT_BUTTON).click();

      const after = await getStoredReleases(page);
      expect(after.length).toBe(5);

      // Entry 3 has the changed fields
      const modified = after.find((r: any) => r.id === 'test-id-003');
      expect(modified?.product).toBe('ModifiedProduct');
      expect(modified?.version).toBe('7.7.7');
      expect(modified?.title).toBe('Modified Title');

      // All other entries byte-for-byte identical to pre-edit state
      for (const id of ['test-id-001', 'test-id-002', 'test-id-004', 'test-id-005']) {
        const original = originals[id];
        const current = after.find((r: any) => r.id === id);
        expect(current).toBeDefined();
        expect(current).toEqual(original);
      }
    });

    test('TC-037: Edit same entry twice — second edit pre-fills values from first save', async ({ page }) => {
      // TC-037: Edit same entry twice — second edit pre-fills values from first save

      // First edit: ProductA - v1.0.0 → product = ProductX
      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await page.locator(PRODUCT_INPUT).fill('ProductX');
      await page.locator(SUBMIT_BUTTON).click();

      // Form returns to create mode
      await expect(page.locator(SUBMIT_BUTTON)).toHaveText('Add Release Note');

      // Second edit: click the same entry (now showing ProductX - v1.0.0)
      await clickEditOnCard(page, 'ProductX - v1.0.0');

      // Pre-fill shows ProductX (values from first save), not original ProductA
      await expect(page.locator(PRODUCT_INPUT)).toHaveValue('ProductX');
      await expect(page.locator(VERSION_INPUT)).toHaveValue('v1.0.0');
    });

    test('TC-039: Edit entry to isBreaking=true — breaking filter shows it correctly', async ({ page }) => {
      // TC-039: Edit entry to isBreaking=true — breaking filter shows it correctly
      // test-id-002: ProductA - v1.1.0 / isBreaking=false

      await clickEditOnCard(page, 'ProductA - v1.1.0');
      await page.locator(BREAKING_CHECKBOX).check();
      await page.locator(SUBMIT_BUTTON).click();

      // Verify entry saved with isBreaking=true
      const releases = await getStoredReleases(page);
      const edited = releases.find((r: any) => r.id === 'test-id-002');
      expect(edited?.isBreaking).toBe(true);

      // Set breaking filter to "breaking"
      await page.selectOption(BREAKING_FILTER_SELECT, 'breaking');

      // The just-edited entry appears in the breaking-filtered view
      await expect(
        page.locator(RELEASE_CARD).filter({
          has: page.locator(CARD_PRODUCT_VER, { hasText: 'ProductA - v1.1.0' })
        })
      ).toBeVisible();
    });

    test('TC-040: Edit title to include search keyword — search returns updated entry', async ({ page }) => {
      // TC-040: Edit title to include search keyword — search returns updated entry

      // Confirm "unicornkeyword" is not in any current entry
      await page.locator(SEARCH_FILTER_INPUT).fill('unicornkeyword');
      await expect(page.locator(RELEASE_CARD)).toHaveCount(0);

      // Clear search filter
      await page.locator(SEARCH_FILTER_INPUT).fill('');

      // Edit an entry — include "unicornkeyword" in title
      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await page.locator(TITLE_INPUT).fill('UniqueTitle unicornkeyword');
      await page.locator(SUBMIT_BUTTON).click();

      // Search for unicornkeyword — should now return the edited entry
      await page.locator(SEARCH_FILTER_INPUT).fill('unicornkeyword');

      await expect(page.locator(RELEASE_CARD)).toHaveCount(1);
      await expect(page.locator(RELEASE_CARD).first()).toContainText('unicornkeyword');
    });

    test('TC-041: Two sequential edits on different entries — both updated independently', async ({ page }) => {
      // TC-041: Two sequential edits on different entries — both updated independently

      const before = await getStoredReleases(page);
      const initialCount = before.length;

      // Edit entry A (test-id-001: ProductA - v1.0.0)
      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await page.locator(PRODUCT_INPUT).fill('EntryAProduct');
      await page.locator(SUBMIT_BUTTON).click();

      // Edit entry B (test-id-002: ProductA - v1.1.0)
      await clickEditOnCard(page, 'ProductA - v1.1.0');
      await page.locator(TITLE_INPUT).fill('EntryBTitle');
      await page.locator(SUBMIT_BUTTON).click();

      const after = await getStoredReleases(page);

      // Count unchanged
      expect(after.length).toBe(initialCount);

      const entryA = after.find((r: any) => r.id === 'test-id-001');
      const entryB = after.find((r: any) => r.id === 'test-id-002');

      expect(entryA).toBeDefined();
      expect(entryB).toBeDefined();

      // Entry A has updated product
      expect(entryA.product).toBe('EntryAProduct');

      // Entry B has updated title
      expect(entryB.title).toBe('EntryBTitle');

      // No cross-contamination: entry A title unchanged, entry B product unchanged
      expect(entryA.title).toBe('ProductA release notes v1');
      expect(entryB.product).toBe('ProductA');

      // No id collision
      expect(entryA.id).not.toBe(entryB.id);
    });
  });

  // ── SD-008 group ──────────────────────────────────────────────────────────

  test.describe('with SD-008', () => {

    test.beforeEach(async ({ page }) => {
      await seedLocalStorage(page, 'SD-008');
      await page.goto('/');
    });

    test('TC-036: Edit product value — product filter returns correct results afterward', async ({ page }) => {
      // TC-036: Edit product value — product filter returns correct results afterward
      // SD-008: test-id-001=ProductA, test-id-002=ProductB

      // Edit ProductA entry → change to ProductB
      await clickEditOnCard(page, 'ProductA - v1.0.0');
      await page.locator(PRODUCT_INPUT).fill('ProductB');
      await page.locator(SUBMIT_BUTTON).click();

      // Both entries now have product = ProductB in localStorage
      const releases = await getStoredReleases(page);
      const productBEntries = releases.filter((r: any) => r.product === 'ProductB');
      expect(productBEntries).toHaveLength(2);

      const productAEntries = releases.filter((r: any) => r.product === 'ProductA');
      expect(productAEntries).toHaveLength(0);

      // Filter by ProductB → shows 2 entries
      await page.selectOption(PRODUCT_FILTER_SELECT, 'ProductB');
      await expect(page.locator(RELEASE_CARD)).toHaveCount(2);
    });
  });

  // ── SD-009 group ──────────────────────────────────────────────────────────

  test.describe('with SD-009', () => {

    test.beforeEach(async ({ page }) => {
      await seedLocalStorage(page, 'SD-009');
      await page.goto('/');
    });

    test('TC-038: Seed data: edit one seed record — other seed record unchanged', async ({ page }) => {
      // TC-038: Seed data: edit one seed record — other seed record unchanged
      // SD-009 clears localStorage; app auto-seeds 2 records (r1=Billing API, r2=Auth Service)

      await expect(page.locator(RELEASE_CARD)).toHaveCount(2);

      const seeded = await getStoredReleases(page);
      expect(seeded).toHaveLength(2);
      const record2Original = { ...seeded[1] };

      // Edit seed record 1 (first card rendered)
      await page.locator(RELEASE_CARD).first().locator(EDIT_BTN).click();
      await page.locator(TITLE_INPUT).fill('Edited Seed Title');
      await page.locator(SUBMIT_BUTTON).click();

      const updated = await getStoredReleases(page);

      // Record 1 title updated
      const record1 = updated.find((r: any) => r.id === seeded[0].id);
      expect(record1?.title).toBe('Edited Seed Title');

      // Record 2 byte-for-byte identical to its original auto-seeded state
      const record2After = updated.find((r: any) => r.id === record2Original.id);
      expect(record2After).toEqual(record2Original);
    });
  });

  // TC-042: MANUAL ONLY — CSV import involves window.confirm and file system interaction
});
