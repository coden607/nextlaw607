import type { CaseGuardianMatter, PrivacySettings } from "./domain.js";
import { DEFAULT_PRIVACY } from "./domain.js";

const PRIVACY_KEY = "nextlaw607.privacy.v1";
const CASES_KEY = "nextlaw607.cases.v1";

export function readPrivacy(storage: Storage = localStorage): PrivacySettings {
  const raw = storage.getItem(PRIVACY_KEY);
  if (!raw) return DEFAULT_PRIVACY;
  try { return { ...DEFAULT_PRIVACY, ...JSON.parse(raw) as Partial<PrivacySettings> }; }
  catch { return DEFAULT_PRIVACY; }
}

export function writePrivacy(settings: PrivacySettings, storage: Storage = localStorage): void {
  storage.setItem(PRIVACY_KEY, JSON.stringify(settings));
}

export function readCases(storage: Storage = localStorage): CaseGuardianMatter[] {
  const raw = storage.getItem(CASES_KEY);
  if (!raw) return [];
  try { return JSON.parse(raw) as CaseGuardianMatter[]; }
  catch { return []; }
}

export function writeCases(cases: readonly CaseGuardianMatter[], storage: Storage = localStorage): void {
  storage.setItem(CASES_KEY, JSON.stringify(cases));
}
