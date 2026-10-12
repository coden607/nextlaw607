
export const PROCEDURE_STAGES = [
  "investigation", "arrest", "appearance_ticket", "arraignment",
  "release_bail_remand", "grand_jury", "plea", "pretrial", "discovery",
  "motions", "hearings", "trial", "sentencing", "appeal", "post_conviction"
] as const;

export type ProcedureStage = typeof PROCEDURE_STAGES[number];

export type EncounterMode = "street_stop" | "traffic_stop" | "search" | "home_entry" | "interrogation" | "arrest";

export interface RightsCard {
  mode: EncounterMode;
  title: string;
  actions: readonly string[];
  never: readonly string[];
}

export interface PrivacySettings {
  diagnostics: boolean;
  cloudSync: boolean;
  cloudAI: boolean;
  localOnly: boolean;
}

export interface CaseGuardianMatter {
  id: string;
  title: string;
  jurisdiction: string;
  stage?: ProcedureStage;
  nextAppearance?: string;
  deadlines: readonly string[];
  issues: readonly string[];
  nextActions: readonly string[];
}

export const DEFAULT_PRIVACY: PrivacySettings = {
  diagnostics: false,
  cloudSync: false,
  cloudAI: false,
  localOnly: true
};

export const RIGHTS_PACK: Record<EncounterMode, RightsCard> = {
  street_stop: {
    mode: "street_stop",
    title: "Street stop",
    actions: ["Stay calm.", "Ask: Am I free to leave?", "Do not consent to a search."],
    never: ["Do not resist, flee, interfere, lie, obstruct, or destroy evidence."]
  },
  traffic_stop: {
    mode: "traffic_stop",
    title: "Traffic stop",
    actions: ["Keep your hands visible.", "Do not consent to a search.", "Ask whether you are free to leave when appropriate."],
    never: ["Do not physically resist or interfere."]
  },
  search: {
    mode: "search",
    title: "Search",
    actions: ["Say: I do not consent to this search.", "Do not physically interfere.", "Preserve what happened for later review."],
    never: ["Do not hide, alter, or destroy evidence."]
  },
  home_entry: {
    mode: "home_entry",
    title: "Police at the door / home entry",
    actions: ["Stay calm.", "Do not consent to entry or a search unless you choose to.", "Do not physically block officers."],
    never: ["Do not resist execution of a warrant or destroy evidence."]
  },
  interrogation: {
    mode: "interrogation",
    title: "Questioning / interrogation",
    actions: ["Say: I am invoking my right to remain silent.", "Say: I want a lawyer before answering questions."],
    never: ["Do not lie or fabricate information."]
  },
  arrest: {
    mode: "arrest",
    title: "Arrest",
    actions: ["Do not resist.", "Say: I want a lawyer and I am choosing to remain silent.", "Preserve paperwork and release conditions."],
    never: ["Do not flee, fight, threaten, or obstruct."]
  }
};

export function rightsFor(mode: EncounterMode): RightsCard {
  return RIGHTS_PACK[mode];
}
