// Seed data matching the application's seedData() in script.js
// Used by clearAndSeedStorage() in storage helpers

export interface ReleaseNote {
  id: string;
  product: string;
  version: string;
  teamName: string;
  title: string;
  description: string;
  releaseDate: string;
  isBreaking: boolean;
}

export const SEED_BILLING: ReleaseNote = {
  id: 'r1',
  product: 'Billing API',
  version: 'v1.4.0',
  teamName: 'Platform Team',
  title: 'Invoice export now supports CSV and XLSX',
  description: 'Added dual-format export and improved export speed for large accounts.',
  releaseDate: '2026-06-08',
  isBreaking: false,
};

export const SEED_AUTH: ReleaseNote = {
  id: 'r2',
  product: 'Auth Service',
  version: 'v2.0.0',
  teamName: 'Identity Team',
  title: 'Token introspection endpoint updated',
  description: 'Old response shape is deprecated. Clients should migrate to the new claims object format.',
  releaseDate: '2026-06-10',
  isBreaking: true,
};

export const SEED_PAYMENTS: ReleaseNote = {
  id: 'r3',
  product: 'Payments API',
  version: 'v1.0.0',
  teamName: 'Finance Team',
  title: 'Payments service initial release',
  description: 'First stable release of the Payments API with basic transaction support.',
  releaseDate: '2026-07-01',
  isBreaking: false,
};

/** Default two-item seed used in most beforeEach hooks */
export const DEFAULT_SEED: ReleaseNote[] = [SEED_BILLING, SEED_AUTH];

/** Three-item seed for position-based tests (TC-016, TC-017, TC-018) */
export const THREE_ITEM_SEED: ReleaseNote[] = [SEED_BILLING, SEED_AUTH, SEED_PAYMENTS];

/** Single-item seed for TC-038 */
export const SINGLE_ITEM_SEED: ReleaseNote[] = [SEED_BILLING];
