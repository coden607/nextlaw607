export type PracticeArea =
  | "contracts"
  | "family"
  | "criminal"
  | "civil"
  | "real-property"
  | "employment";

export type AgentRole = "planner" | "executor" | "critic";

export type MatterStatus =
  | "intake"
  | "research"
  | "draft"
  | "critique"
  | "ready";

export type Party = {
  role: string;
  name: string;
  entity?: string;
};

export type Citation = {
  id: string;
  kind: "statute" | "case" | "rule" | "reg";
  bluebook: string;
  court?: string;
  year?: number;
  pinpoint?: string;
  url: string;
  verified: boolean;
  source: "corpus" | "courtlistener" | "nysenate" | "unverified";
  holding?: string;
};

export type Matter = {
  id: string;
  caption: string;
  practice: PracticeArea;
  parties: Party[];
  facts: string;
  objectives: string;
  county: string;
  status: MatterStatus;
  createdAt: string;
  updatedAt: string;
};

export type DraftRecord = {
  id: string;
  matterId: string;
  templateId: string;
  title: string;
  body: string;
  criticScore: number | null;
  criticNotes: string[];
  missingAuthorities: string[];
  citations: Citation[];
  plannerMemo: string;
  criticMemo: string;
  createdAt: string;
};

export type ResearchHit = {
  id: string;
  caseName: string;
  citations: string[];
  court: string;
  dateFiled: string;
  snippet: string;
  url: string;
  citeCount: number;
};

export type StatuteDoc = {
  id: string;
  lawId: string;
  section: string;
  title: string;
  chapter: string;
  blackletter: string;
  practiceNotes: string;
  officialUrl: string;
  practice: PracticeArea[];
};

export type CaseDoc = {
  id: string;
  name: string;
  bluebook: string;
  court: string;
  year: number;
  holding: string;
  officialUrl: string;
  statutes: string[];
  practice: PracticeArea[];
};

export type ContractTemplate = {
  id: string;
  name: string;
  practice: PracticeArea;
  summary: string;
  requiredStatutes: string[];
  requiredCases: string[];
  skeleton: string;
};

export type TriadResult = {
  planner: {
    issues: string[];
    authorities: string[];
    framework: string;
    risks: string[];
  };
  draft: {
    title: string;
    body: string;
  };
  critic: {
    score: number;
    flaws: string[];
    missingStatutes: string[];
    unverifiedCitations: string[];
    rewriteDirectives: string[];
    memo: string;
  };
};

export type SkillCard = {
  id: string;
  name: string;
  trigger: string;
  mandate: string;
  steps: string[];
  authorities: string[];
};

export const PRACTICE_LABEL: Record<PracticeArea, string> = {
  contracts: "Contracts / GOL / UCC",
  family: "Family — DRL / FCA",
  criminal: "Criminal — PL / CPL",
  civil: "Civil — CPLR",
  "real-property": "Real Property",
  employment: "Employment / Labor",
};
