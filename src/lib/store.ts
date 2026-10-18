import { create } from "zustand";
import { persist } from "zustand/middleware";
import { isPrimaryCriminalPractice, requireCriminalCenteredScope } from "./criminal-scope";
import type { DraftRecord, Matter, PracticeArea } from "./types";

type CounselState = {
  matters: Matter[];
  drafts: DraftRecord[];
  activeMatterId: string | null;
  voiceOn: boolean;
  setVoiceOn: (v: boolean) => void;
  holoMode: boolean;
  setHoloMode: (v: boolean) => void;
  setActiveMatter: (id: string | null) => void;
  upsertMatter: (m: Matter) => void;
  deleteMatter: (id: string) => void;
  addDraft: (d: DraftRecord) => void;
  deleteDraft: (id: string) => void;
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
  caption: "People v. Rivera — suppression workup",
  practice: "criminal",
  parties: [
    { role: "Defendant", name: "Alex Rivera" },
    { role: "Prosecution", name: "People of the State of New York" },
  ],
  facts:
    "Demo criminal matter involving a street stop, search, arrest, and custodial questioning. Dates, charges, discovery status, and hearing posture must be confirmed from the record before use.",
  objectives:
    "Map suppression issues, CPL Article 245 discovery, CPL 30.30 timing, preservation, and verified controlling authority.",
  county: "New York",
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
      holoMode: true,
      setHoloMode: (v) => set({ holoMode: v }),
      setActiveMatter: (id) => set({ activeMatterId: id }),
      upsertMatter: (m) => {
        requireCriminalCenteredScope(m.practice);
        set({
          matters: get().matters.some((x) => x.id === m.id)
            ? get().matters.map((x) => (x.id === m.id ? m : x))
            : [m, ...get().matters],
          activeMatterId: m.id,
        });
      },
      deleteMatter: (mid) =>
        set({
          matters: get().matters.filter((m) => m.id !== mid),
          drafts: get().drafts.filter((d) => d.matterId !== mid),
          activeMatterId: get().activeMatterId === mid ? null : get().activeMatterId,
        }),
      addDraft: (d) => set({ drafts: [d, ...get().drafts].slice(0, 40) }),
      deleteDraft: (draftId) => set({ drafts: get().drafts.filter((d) => d.id !== draftId) }),
      seedIfEmpty: () => {
        const criminalMatters = get().matters.filter((m) => isPrimaryCriminalPractice(m.practice));
        if (criminalMatters.length === 0) {
          set({ matters: [DEMO_MATTER], activeMatterId: DEMO_MATTER.id });
        } else if (criminalMatters.length !== get().matters.length) {
          const allowedIds = new Set(criminalMatters.map((m) => m.id));
          set({
            matters: criminalMatters,
            drafts: get().drafts.filter((d) => allowedIds.has(d.matterId)),
            activeMatterId: allowedIds.has(get().activeMatterId ?? "")
              ? get().activeMatterId
              : criminalMatters[0].id,
          });
        }
      },
    }),
    {
      name: "nextlaw607",
      onRehydrateStorage: () => (state) => {
        if (!state) return;
        state.matters = state.matters.filter((m) => isPrimaryCriminalPractice(m.practice));
        const allowedIds = new Set(state.matters.map((m) => m.id));
        state.drafts = state.drafts.filter((d) => allowedIds.has(d.matterId));
        if (state.matters.length === 0) {
          state.matters = [DEMO_MATTER];
          state.activeMatterId = DEMO_MATTER.id;
        } else if (!state.matters.some((m) => m.id === state.activeMatterId)) {
          state.activeMatterId = state.matters[0].id;
        }
      },
    },
  ),
);

export function newMatter(partial: Partial<Matter> & { practice: PracticeArea }): Matter {
  requireCriminalCenteredScope(partial.practice);
  const t = now();
  return {
    id: id("mat"),
    caption: partial.caption ?? "Untitled criminal matter",
    practice: "criminal",
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
