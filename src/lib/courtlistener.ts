import { createServerFn } from "@tanstack/react-start";
import type { ResearchHit } from "./types";

const NY_COURTS = "ny,nyappdiv,nysupct,ca2";

type CLSearch = {
  q: string;
  courts?: string;
  type?: "o" | "r" | "oa";
};

type CLRaw = {
  count?: number;
  results?: Array<{
    absolute_url?: string;
    caseName?: string;
    citation?: string[];
    court?: string;
    dateFiled?: string;
    snippet?: string;
    citeCount?: number;
    cluster_id?: number;
    docketNumber?: string;
  }>;
};

export const searchOpinions = createServerFn({ method: "POST" })
  .validator((input: CLSearch) => input)
  .handler(async ({ data }) => {
    const q = data.q.trim();
    if (!q) return { ok: false as const, error: "Enter a query.", hits: [] as ResearchHit[], count: 0 };

    const url = new URL("https://www.courtlistener.com/api/rest/v4/search/");
    url.searchParams.set("q", q);
    url.searchParams.set("type", data.type ?? "o");
    url.searchParams.set("court", data.courts ?? NY_COURTS);
    url.searchParams.set("order_by", "score desc");
    url.searchParams.set("page_size", "8");

    const headers: Record<string, string> = {
      Accept: "application/json",
      "User-Agent": "NextLaw607/1.0 (General Counsel terminal; educational research)",
    };
    const token = process.env.COURTLISTENER_API_TOKEN;
    if (token) headers.Authorization = `Token ${token}`;

    try {
      const res = await fetch(url.toString(), { headers });
      if (!res.ok) {
        return {
          ok: false as const,
          error: `CourtListener ${res.status}. ${
            res.status === 401 || res.status === 403
              ? "A Free Law Project token raises the rate limit; unauthenticated search is throttled."
              : "The research gateway is busy."
          }`,
          hits: [] as ResearchHit[],
          count: 0,
        };
      }
      const body = (await res.json()) as CLRaw;
      const hits: ResearchHit[] = (body.results ?? []).map((r, i) => ({
        id: String(r.cluster_id ?? i),
        caseName: r.caseName ?? "Untitled",
        citations: r.citation ?? [],
        court: r.court ?? "",
        dateFiled: r.dateFiled ?? "",
        snippet: (r.snippet ?? "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim(),
        url: r.absolute_url
          ? `https://www.courtlistener.com${r.absolute_url}`
          : "https://www.courtlistener.com/",
        citeCount: r.citeCount ?? 0,
      }));
      return { ok: true as const, hits, count: body.count ?? hits.length };
    } catch {
      return {
        ok: false as const,
        error: "Could not reach CourtListener. Using the verified bank only.",
        hits: [] as ResearchHit[],
        count: 0,
      };
    }
  });

export const fetchNyStatute = createServerFn({ method: "POST" })
  .validator((input: { lawId: string; section: string }) => input)
  .handler(async ({ data }) => {
    const lawId = data.lawId.toUpperCase();
    const section = data.section.replace(/^§\s*/, "");
    const url = `https://legislation.nysenate.gov/api/3/laws/${encodeURIComponent(lawId)}/${encodeURIComponent(section)}?key=DEMO`;
    try {
      const res = await fetch(url, {
        headers: { Accept: "application/json" },
      });
      if (!res.ok) {
        return {
          ok: false as const,
          error: `NY Senate Open Legislation ${res.status}. Use the verified bank and nysenate.gov links.`,
          text: "",
          url: `https://www.nysenate.gov/legislation/laws/${lawId}/${section}`,
        };
      }
      const body = (await res.json()) as {
        result?: { text?: string; title?: string; lawId?: string; locationId?: string };
        message?: string;
        success?: boolean;
      };
      const text = body.result?.text ?? "";
      if (!text) {
        return {
          ok: false as const,
          error: "No text in the Senate response. Open the official page.",
          text: "",
          url: `https://www.nysenate.gov/legislation/laws/${lawId}/${section}`,
        };
      }
      return {
        ok: true as const,
        text: text.slice(0, 8000),
        title: body.result?.title ?? `${lawId} § ${section}`,
        url: `https://www.nysenate.gov/legislation/laws/${lawId}/${section}`,
      };
    } catch {
      return {
        ok: false as const,
        error: "NY Senate API unreachable.",
        text: "",
        url: `https://www.nysenate.gov/legislation/laws/${lawId}/${section}`,
      };
    }
  });
