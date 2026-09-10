import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { DraftRecord, Matter, PracticeArea } from "./types";

type CounselState = {
  matters: Matter[];
  drafts: DraftRecord[];
  activeMatterId: string | null;
  voiceOn: boolean;
  setVoiceOn: (v: boolean) => void;
  setActiveMatter: (id: string | null) => void;
  upsertMatter: (m: Matter) => void;
  deleteMatter: (id: string) => void;
  addDraft: (d: DraftRecord) => void;
  seedIfEmpty: () => void;
};

function now() {
  return new Date().toISOString();
}

function id(prefix: string) {
  return `${prefix}_${Math.random().toString(36).slice(2, 9)}`;
}

const DEMO_MATTER: Matter = {
  id: "mat_demo607",
  caption: "Avery v. Hale — parenting stipulation",
  practice: "family",
  parties: [
    { role: "Plaintiff / Parent A", name: "Jordan Avery" },
    { role: "Defendant / Parent B", name: "Casey Hale" },
  ],
  facts:
    "Two children, ages 7 and 11, reside in Kings County. Parent A is the current residential parent. Parent B seeks an expanded 2-2-3 schedule and objects to a contemplated move to Albany County. Combined parental income is approximately $180,000. The parties want a so-ordered stipulation rather than a trial.",
  objectives:
    "Joint legal custody, a defined parenting calendar, a Tropea-aware relocation clause, and CSSA child support with statutory add-ons pro-rated.",
  county: "Kings",
  status: "intake",
  createdAt: now(),
  updatedAt: now(),
};

export const useCounsel = create<CounselState>()(
  persist(
    (set, get) => ({
      matters: [DEMO_MATTER],
      drafts: [],
      activeMatterId: DEMO_MATTER.id,
      voiceOn: false,
      setVoiceOn: (v) => set({ voiceOn: v }),
      setActiveMatter: (id) => set({ activeMatterId: id }),
      upsertMatter: (m) =>
        set({
          matters: get().matters.some((x) => x.id === m.id)
            ? get().matters.map((x) => (x.id === m.id ? m : x))
            : [m, ...get().matters],
          activeMatterId: m.id,
        }),
      deleteMatter: (mid) =>
        set({
          matters: get().matters.filter((m) => m.id !== mid),
          drafts: get().drafts.filter((d) => d.matterId !== mid),
          activeMatterId: get().activeMatterId === mid ? null : get().activeMatterId,
        }),
      addDraft: (d) => set({ drafts: [d, ...get().drafts].slice(0, 40) }),
      seedIfEmpty: () => {
        if (get().matters.length === 0) {
          set({ matters: [DEMO_MATTER], activeMatterId: DEMO_MATTER.id });
        }
      },
    }),
    {
      name: "nextlaw607",
      onRehydrateStorage: () => (state) => {
        if (!state) return;
        if (state.matters.length === 0) {
          state.matters = [DEMO_MATTER];
          state.activeMatterId = DEMO_MATTER.id;
        }
      },
    },
  ),
);

export function newMatter(partial: Partial<Matter> & { practice: PracticeArea }): Matter {
  const t = now();
  return {
    id: id("mat"),
    caption: partial.caption ?? "Untitled matter",
    practice: partial.practice,
    parties: partial.parties ?? [],
    facts: partial.facts ?? "",
    objectives: partial.objectives ?? "",
    county: partial.county ?? "New York",
    status: partial.status ?? "intake",
    createdAt: t,
    updatedAt: t,
  };
}

export function newDraftId() {
  return id("dr");
}

export { id as makeId };
