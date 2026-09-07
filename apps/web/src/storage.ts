import type { CaseGuardianMatter, PrivacySettings, ProcedureStage } from "./domain.js";
import { DEFAULT_PRIVACY, PROCEDURE_STAGES } from "./domain.js";

const PRIVACY_KEY = "nextlaw607.privacy.v1";
const CASES_KEY = "nextlaw607.cases.v1";
export const LOCAL_DATA_SCHEMA_VERSION = 1 as const;

export interface LocalDataSnapshot {
  schemaVersion: typeof LOCAL_DATA_SCHEMA_VERSION;
  exportedAt: string;
  privacy: PrivacySettings;
  cases: CaseGuardianMatter[];
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every(item => typeof item === "string");
}

function isPrivacySettings(value: unknown): value is PrivacySettings {
  if (!isRecord(value)) return false;
  return ["diagnostics", "cloudSync", "cloudAI", "localOnly"].every(key => typeof value[key] === "boolean");
}

function isProcedureStage(value: unknown): value is ProcedureStage {
  return typeof value === "string" && (PROCEDURE_STAGES as readonly string[]).includes(value);
}

function isCaseMatter(value: unknown): value is CaseGuardianMatter {
  if (!isRecord(value)) return false;
  if (typeof value.id !== "string" || typeof value.title !== "string" || typeof value.jurisdiction !== "string") return false;
  if (value.stage !== undefined && !isProcedureStage(value.stage)) return false;
  if (value.nextAppearance !== undefined && typeof value.nextAppearance !== "string") return false;
  return isStringArray(value.deadlines) && isStringArray(value.issues) && isStringArray(value.nextActions);
}

export function readPrivacy(storage: Storage = localStorage): PrivacySettings {
  const raw = storage.getItem(PRIVACY_KEY);
  if (!raw) return DEFAULT_PRIVACY;
  try {
    const parsed = JSON.parse(raw) as unknown;
    return isRecord(parsed) ? { ...DEFAULT_PRIVACY, ...parsed } as PrivacySettings : DEFAULT_PRIVACY;
  } catch {
    return DEFAULT_PRIVACY;
  }
}

export function writePrivacy(settings: PrivacySettings, storage: Storage = localStorage): void {
  storage.setItem(PRIVACY_KEY, JSON.stringify(settings));
}

export function readCases(storage: Storage = localStorage): CaseGuardianMatter[] {
  const raw = storage.getItem(CASES_KEY);
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw) as unknown;
    return Array.isArray(parsed) && parsed.every(isCaseMatter) ? parsed : [];
  } catch {
    return [];
  }
}

export function writeCases(cases: readonly CaseGuardianMatter[], storage: Storage = localStorage): void {
  storage.setItem(CASES_KEY, JSON.stringify(cases));
}

export function exportLocalData(storage: Storage = localStorage): LocalDataSnapshot {
  return {
    schemaVersion: LOCAL_DATA_SCHEMA_VERSION,
    exportedAt: new Date().toISOString(),
    privacy: { ...readPrivacy(storage) },
    cases: readCases(storage).map(matter => ({
      ...matter,
      deadlines: [...matter.deadlines],
      issues: [...matter.issues],
      nextActions: [...matter.nextActions],
    })),
  };
}

export function clearLocalData(storage: Storage = localStorage): void {
  storage.removeItem(PRIVACY_KEY);
  storage.removeItem(CASES_KEY);
}

export function importLocalData(snapshot: unknown, storage: Storage = localStorage): void {
  if (!isRecord(snapshot) || snapshot.schemaVersion !== LOCAL_DATA_SCHEMA_VERSION) {
    throw new Error("Unsupported local data schema");
  }
  if (!isPrivacySettings(snapshot.privacy)) throw new Error("Invalid privacy settings in local data snapshot");
  if (!Array.isArray(snapshot.cases) || !snapshot.cases.every(isCaseMatter)) {
    throw new Error("Invalid case data in local data snapshot");
  }
  writePrivacy(snapshot.privacy, storage);
  writeCases(snapshot.cases, storage);
}
