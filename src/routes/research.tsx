import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { Disclaimer } from "@/components/disclaimer";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input, Label, Textarea } from "@/components/ui/input";
import { fetchNyStatute, searchOpinions } from "@/lib/courtlistener";
import { searchCorpus } from "@/lib/corpus";
import type { ResearchHit } from "@/lib/types";

type ResearchSearch = { q?: string };

export const Route = createFileRoute("/research")({
  validateSearch: (s: Record<string, unknown>): ResearchSearch => ({
    q: typeof s.q === "string" ? s.q : undefined,
  }),
  component: Research,
});

function Research() {
  const { q: initial } = Route.useSearch();
  const [q, setQ] = useState(initial ?? "best interests of the child");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hits, setHits] = useState<ResearchHit[]>([]);
  const [count, setCount] = useState<number | null>(null);
  const [paste, setPaste] = useState("");
  const [lawId, setLawId] = useState("DOM");
  const [section, setSection] = useState("70");
  const [statuteText, setStatuteText] = useState("");
  const [statuteErr, setStatuteErr] = useState<string | null>(null);

  const corpus = useMemo(() => searchCorpus(q), [q]);
  const ingest = useMemo(() => parseIngest(paste), [paste]);

  async function runSearch(e?: React.FormEvent) {
    e?.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const res = await searchOpinions({ data: { q } });
      setHits(res.hits);
      setCount(res.count);
      if (!res.ok) setError(res.error);
    } finally {
      setBusy(false);
    }
  }

  async function pullStatute() {
    setStatuteErr(null);
    const res = await fetchNyStatute({ data: { lawId, section } });
    if (!res.ok) {
      setStatuteErr(res.error);
      setStatuteText("");
      return;
    }
    setStatuteText(res.text);
  }

  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-6 pb-20">
      <header>
        <Badge>CourtListener v4 · NY Senate</Badge>
        <h1 className="mt-3 font-display text-3xl tracking-tight">Authority harvest</h1>
        <p className="mt-2 max-w-2xl text-sm leading-normal text-muted">
          Live opinions from the Free Law Project, official statute pages from
          nysenate.gov, and a verified internal bank the Critic is allowed to
          trust. Snippets are not a substitute for the full opinion.
        </p>
      </header>

      <form onSubmit={runSearch} className="flex flex-col gap-3 md:flex-row">
        <Input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Eschbach, Tropea, 30.30, Hooper indemnity…"
          aria-label="Research query"
        />
        <Button type="submit" disabled={busy} className="md:w-40">
          {busy ? "Searching…" : "Search NY"}
        </Button>
      </form>
      {error ? <p className="text-sm text-warn">{error}</p> : null}
      {count != null ? (
        <p className="font-mono text-xs text-subtle">{count.toLocaleString()} hits · NY / AD / Supreme / 2d Cir.</p>
      ) : null}

      <div className="grid gap-6 lg:grid-cols-2">
        <section>
          <h2 className="font-display text-xl">Live opinions</h2>
          <ul className="mt-3 space-y-3">
            {hits.length === 0 ? (
              <li className="rounded-xl border border-border bg-surface p-4 text-sm text-muted">
                Run a search to pull CourtListener clusters. Unauthenticated
                traffic is rate-limited; a token lifts the cap.
              </li>
            ) : (
              hits.map((h) => (
                <li key={h.id} className="rounded-xl border border-border bg-surface p-4">
                  <a
                    href={h.url}
                    target="_blank"
                    rel="noreferrer"
                    className="font-display text-lg leading-snug text-fg hover:text-accent"
                  >
                    {h.caseName}
                  </a>
                  <p className="mt-1 font-mono text-[11px] text-muted">
                    {h.citations[0] ?? "Unreported"} · {h.court} · {h.dateFiled}
                    {h.citeCount ? ` · cited ${h.citeCount}` : ""}
                  </p>
                  <p className="mt-2 text-sm leading-normal text-muted">{h.snippet}</p>
                </li>
              ))
            )}
          </ul>
        </section>

        <section>
          <h2 className="font-display text-xl">Verified bank</h2>
          <ul className="mt-3 space-y-3">
            {corpus.statutes.slice(0, 5).map((s) => (
              <li key={s.id} className="rounded-xl border border-border bg-surface p-4">
                <div className="flex flex-wrap items-center gap-2">
                  <Badge>
                    {s.lawId} § {s.section}
                  </Badge>
                  <span className="text-sm text-fg">{s.title}</span>
                </div>
                <p className="mt-2 text-sm leading-normal text-muted">{s.blackletter}</p>
                <a
                  className="mt-2 inline-block text-xs text-accent underline-offset-4 hover:underline"
                  href={s.officialUrl}
                  target="_blank"
                  rel="noreferrer"
                >
                  nysenate.gov
                </a>
              </li>
            ))}
            {corpus.cases.slice(0, 5).map((c) => (
              <li key={c.id} className="rounded-xl border border-border bg-surface p-4">
                <p className="font-display text-base">{c.name}</p>
                <p className="font-mono text-[11px] text-muted">{c.bluebook}</p>
                <p className="mt-2 text-sm leading-normal text-muted">{c.holding}</p>
              </li>
            ))}
          </ul>
        </section>
      </div>

      <section className="rounded-xl border border-border bg-surface p-5">
        <h2 className="font-display text-xl">NY Senate pull</h2>
        <p className="mt-1 text-sm text-muted">
          Law ids: DOM (DRL), FCT (FCA), CPL, PEN, GOB (GOL), CVP (CPLR), LAB, RPP, LLC, UCC.
        </p>
        <div className="mt-3 grid gap-3 sm:grid-cols-[1fr_1fr_auto]">
          <div>
            <Label htmlFor="law">Law id</Label>
            <Input id="law" className="mt-1" value={lawId} onChange={(e) => setLawId(e.target.value)} />
          </div>
          <div>
            <Label htmlFor="sec">Section</Label>
            <Input id="sec" className="mt-1" value={section} onChange={(e) => setSection(e.target.value)} />
          </div>
          <Button className="self-end" variant="secondary" onClick={() => void pullStatute()}>
            Fetch
          </Button>
        </div>
        {statuteErr ? <p className="mt-3 text-sm text-warn">{statuteErr}</p> : null}
        {statuteText ? (
          <pre className="mt-4 max-h-64 overflow-auto whitespace-pre-wrap font-mono text-xs leading-relaxed text-muted">
            {statuteText}
          </pre>
        ) : null}
      </section>

      <section className="rounded-xl border border-border bg-surface p-5">
        <h2 className="font-display text-xl">Local ingest</h2>
        <p className="mt-1 text-sm text-muted">
          Docling-style local parse. Paste a brief, production letter, or
          multi-column ruling. Headings, tables, and reading order stay on this
          device — nothing is sent until you run the triad.
        </p>
        <Textarea
          className="mt-3 min-h-36"
          value={paste}
          onChange={(e) => setPaste(e.target.value)}
          placeholder="# Heading&#10;Paste the other side's brief…"
        />
        {ingest.headings.length || ingest.tables ? (
          <dl className="mt-4 grid gap-2 text-sm">
            <div>
              <dt className="font-mono text-[11px] uppercase tracking-wider text-subtle">Headings</dt>
              <dd className="text-muted">{ingest.headings.join(" · ") || "—"}</dd>
            </div>
            <div>
              <dt className="font-mono text-[11px] uppercase tracking-wider text-subtle">Words</dt>
              <dd className="tabular-nums text-muted">{ingest.words}</dd>
            </div>
          </dl>
        ) : null}
      </section>
      <Disclaimer />
    </div>
  );
}

function parseIngest(text: string) {
  const headings = text
    .split("\n")
    .filter((l) => /^#{1,3}\s|^(I{1,3}|IV|V|VI{0,3}|ARTICLE)\b/.test(l.trim()))
    .map((l) => l.replace(/^#+\s*/, "").trim())
    .slice(0, 12);
  const tables = /\|.+\|/.test(text);
  const words = text.trim() ? text.trim().split(/\s+/).length : 0;
  return { headings, tables, words };
}
