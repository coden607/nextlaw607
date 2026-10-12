export type PublicSourceKind = "primary" | "self-help" | "secondary";

export type PublicLegalSource = {
  id: string;
  name: string;
  kind: PublicSourceKind;
  description: string;
  url: string;
  searchUrl?: (query: string) => string;
  mayCite: boolean;
};

export const PUBLIC_LEGAL_SOURCES: PublicLegalSource[] = [
  {
    id: "nys-ucs-decisions",
    name: "New York State Unified Court System",
    kind: "primary",
    description: "Official court decisions, opinions, and court-system resources.",
    url: "https://www.nycourts.gov/reporter/",
    searchUrl: (query) =>
      `https://www.google.com/search?q=site%3Anycourts.gov%2Freporter+${encodeURIComponent(query)}`,
    mayCite: false,
  },
  {
    id: "nys-law-reporting-bureau",
    name: "NYS Law Reporting Bureau",
    kind: "primary",
    description: "Official New York reports, slip opinions, and citation information.",
    url: "https://www.nycourts.gov/reporter/",
    searchUrl: (query) =>
      `https://www.google.com/search?q=site%3Anycourts.gov%2Freporter+${encodeURIComponent(query)}`,
    mayCite: false,
  },
  {
    id: "nys-ucs-forms",
    name: "NYS UCS Court Forms",
    kind: "self-help",
    description: "Official court forms and filing instructions for the public.",
    url: "https://www.nycourts.gov/forms/",
    searchUrl: (query) =>
      `https://www.google.com/search?q=site%3Anycourts.gov%2Fforms+${encodeURIComponent(query)}`,
    mayCite: false,
  },
  {
    id: "nys-court-help",
    name: "NYS CourtHelp",
    kind: "self-help",
    description: "Plain-language court procedure and legal-help information.",
    url: "https://www.nycourts.gov/courthelp/",
    searchUrl: (query) =>
      `https://www.google.com/search?q=site%3Anycourts.gov%2Fcourthelp+${encodeURIComponent(query)}`,
    mayCite: false,
  },
  {
    id: "findlaw-caselaw",
    name: "FindLaw Case Law",
    kind: "secondary",
    description: "Public case-law and legal-information index; verify against the opinion.",
    url: "https://caselaw.findlaw.com/",
    searchUrl: (query) =>
      `https://caselaw.findlaw.com/search.html?search_type=party&court=ny&text=${encodeURIComponent(query)}`,
    mayCite: false,
  },
  {
    id: "courtlistener",
    name: "CourtListener / Free Law Project",
    kind: "primary",
    description: "Searchable public opinions and dockets; inspect the full source before relying on it.",
    url: "https://www.courtlistener.com/",
    mayCite: true,
  },
  {
    id: "supreme-court-opinions",
    name: "U.S. Supreme Court Opinions",
    kind: "primary",
    description: "Official Supreme Court opinions and orders for federal constitutional authority.",
    url: "https://www.supremecourt.gov/opinions/opinions.aspx",
    searchUrl: (query) =>
      `https://www.google.com/search?q=site%3Asupremecourt.gov%2Fopinions+${encodeURIComponent(query)}`,
    mayCite: false,
  },
  {
    id: "nys-senate",
    name: "New York Senate Open Legislation",
    kind: "primary",
    description: "Official public New York statute text and legislative metadata.",
    url: "https://www.nysenate.gov/legislation",
    mayCite: true,
  },
  {
    id: "cornell-lii",
    name: "Cornell Legal Information Institute",
    kind: "secondary",
    description: "Public constitutional, federal, and legal reference material; confirm current primary text.",
    url: "https://www.law.cornell.edu/",
    searchUrl: (query) =>
      `https://www.google.com/search?q=site%3Alaw.cornell.edu+${encodeURIComponent(query)}`,
    mayCite: false,
  },
  {
    id: "justia-law",
    name: "Justia Law",
    kind: "secondary",
    description: "Public case and statute index useful for discovery; verify every authority against a primary source.",
    url: "https://law.justia.com/",
    searchUrl: (query) =>
      `https://www.google.com/search?q=site%3Alaw.justia.com+${encodeURIComponent(query)}`,
    mayCite: false,
  },
];

export const PUBLIC_SOURCE_KIND_LABEL: Record<PublicSourceKind, string> = {
  primary: "Primary source",
  "self-help": "Self-help / procedure",
  secondary: "Secondary index",
};