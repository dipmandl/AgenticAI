/**
 * Centralised DOM selectors for the Release Notes Dashboard.
 * Derived from product_release_dashboard/index.html and script.js.
 */

export const STORAGE_KEY = 'releaseNotesDashboard.releases';

// ── Form fields ──────────────────────────────────────────────────────────────
export const PRODUCT_INPUT      = '#product';
export const VERSION_INPUT      = '#version';
export const TITLE_INPUT        = '#title';
export const DESCRIPTION_INPUT  = '#description';
export const RELEASE_DATE_INPUT = '#releaseDate';
export const TEAM_NAME_INPUT    = '#teamName';
export const BREAKING_CHECKBOX  = '#breaking';
export const TEAM_NAME_ERROR    = '#team-name-error';

// ── Form buttons ─────────────────────────────────────────────────────────────
/** Initial text: "Add Release Note"; edit mode text: "Update Release Note" */
export const SUBMIT_BUTTON      = '#submit-button';
export const CANCEL_EDIT_BUTTON = '#cancel-edit-button';

// ── Filter controls ──────────────────────────────────────────────────────────
/** <select> — options built dynamically; "all" = All products */
export const PRODUCT_FILTER_SELECT   = '#product-filter';
/** <select> — values: "all" | "breaking" | "non-breaking" */
export const BREAKING_FILTER_SELECT  = '#breaking-filter';
/** <input type="text"> — searches title + description */
export const SEARCH_FILTER_INPUT     = '#search-filter';

// ── Transfer actions ─────────────────────────────────────────────────────────
export const EXPORT_CSV_BUTTON  = '#export-csv-button';
export const IMPORT_JSON_BUTTON = '#import-json-button';
export const TRANSFER_STATUS    = '#transfer-status';

// ── Release list ─────────────────────────────────────────────────────────────
export const RELEASE_LIST      = '#release-list';
/** Every rendered release entry */
export const RELEASE_CARD      = '.release-card';
/** Text element showing "<product> - <version>" inside a card */
export const CARD_PRODUCT_VER  = '.product-version';
/** <h3> inside a card */
export const CARD_TITLE        = '.release-title';
/** Paragraph showing "Team: <teamName>" inside a card */
export const CARD_TEAM         = '.release-team';
/** Empty-state paragraph shown when no entries match filters */
export const EMPTY_STATE       = '.empty-state';

// ── Card action buttons ───────────────────────────────────────────────────────
export const EDIT_BTN   = '.edit-btn';
export const DELETE_BTN = '.delete-btn';
