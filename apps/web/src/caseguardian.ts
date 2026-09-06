import type { CaseGuardianMatter } from "./domain.js";
import { readCases, writeCases } from "./storage.js";

export function createMatter(title: string, jurisdiction = "NY", storage: Storage = localStorage): CaseGuardianMatter {
  const matter: CaseGuardianMatter = {
    id: globalThis.crypto?.randomUUID?.() ?? `matter-${Date.now()}`,
    title: title.trim() || "My case",
    jurisdiction,
    stage: "investigation",
    deadlines: [],
    issues: [],
    nextActions: ["Add the next court date and preserve all case paperwork."],
  };
  const matters = readCases(storage);
  writeCases([...matters, matter], storage);
  return matter;
}

export function updateMatter(matter: CaseGuardianMatter, storage: Storage = localStorage): void {
  const matters = readCases(storage);
  const found = matters.some(item => item.id === matter.id);
  writeCases(found ? matters.map(item => item.id === matter.id ? matter : item) : [...matters, matter], storage);
}

export function matterSummary(matter: CaseGuardianMatter): string {
  const appearance = matter.nextAppearance ? `Next appearance: ${matter.nextAppearance}` : "Next appearance: not entered";
  return `${appearance} · ${matter.issues.length} issue(s) · ${matter.nextActions.length} next action(s)`;
}
