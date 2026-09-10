import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { toast } from "sonner";
import { ContractPaper, ScoreMeter, TriadColumns } from "@/components/contract-view";
import { Disclaimer } from "@/components/disclaimer";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Label, Textarea } from "@/components/ui/input";
import { runTriad } from "@/lib/ai";
import { searchOpinions } from "@/lib/courtlistener";
import { CASES, STATUTES } from "@/lib/corpus";
import { newDraftId, useCounsel } from "@/lib/store";
import { TEMPLATES, templateById } from "@/lib/templates";
import type { TriadResult } from "@/lib/types";

type DraftSearch = { template?: string };

export const Route = createFileRoute("/draft")({
  validateSearch: (s: Record<string, unknown>): DraftSearch => ({
    template: typeof s.template === "string" ? s.template : undefined,
  }),
  component: DraftDesk,
});

function DraftDesk() {
  const { template: initial } = Route.useSearch();
  const matters = useCounsel((s) => s.matters);
  const activeId = useCounsel((s) => s.activeMatterId);
  const addDraft = useCounsel((s) => s.addDraft);
  const upsert = useCounsel((s) => s.upsertMatter);
  const matter = matters.find((m) => m.id === activeId) ?? matters[0];

  const [templateId, setTemplateId] = useState(initial ?? "ica");
  const [extra, setExtra] = useState("");
  const [busy, setBusy] = useState(false);
  const [offline, setOffline] = useState(false);
  const [result, setResult] = useState<TriadResult | null>(null);
  const tmpl = templateById(templateId) ?? TEMPLATES[0];

  const required = useMemo(
    () => ({
      statutes: tmpl.requiredStatutes
        .map((id) => STATUTES.find((s) => s.id === id))
        .filter(Boolean),
      cases: tmpl.requiredCases.map((id) => CASES.find((c) => c.id === id)).filter(Boolean),
    }),
    [tmpl],
  );

  async function generate(mode: "triad" | "rewrite") {
    if (!matter) {
      toast.error("Open or create a matter first.");
      return;
    }
    setBusy(true);
    try {
      const live = await searchOpinions({
        data: { q: `${tmpl.name} ${matter.objectives || matter.facts}`.slice(0, 180) },
      });
      const liveAuthorities = live.ok
        ? live.hits
            .map(
              (h) =>
                `${h.caseName} (${h.citations[0] ?? h.court}, ${h.dateFiled}) ${h.url} — ${h.snippet.slice(0, 220)}`,
            )
            .join("\n")
        : "";
      const payload = await runTriad({
        data: {
          mode,
          practice: tmpl.practice,
          templateId: tmpl.id,
          caption: matter.caption,
          county: matter.county,
          parties: matter.parties,
          facts: matter.facts,
          objectives: matter.objectives,
          extra,
          liveAuthorities,
          priorDraft: mode === "rewrite" ? result?.draft.body : undefined,
          criticNotes: mode === "rewrite" ? result?.critic.rewriteDirectives : undefined,
        },
      });
      if (!payload.result) {
        toast.error(payload.error ?? "Counsel failed.");
        return;
      }
      setResult(payload.result);
      setOffline(Boolean(payload.offline));
      addDraft({
        id: newDraftId(),
        matterId: matter.id,
        templateId: tmpl.id,
        title: payload.result.draft.title,
        body: payload.result.draft.body,
        criticScore: payload.result.critic.score,
        criticNotes: payload.result.critic.flaws,
        missingAuthorities: payload.result.critic.missingStatutes,
        citations: [],
        plannerMemo: payload.result.planner.framework,
        criticMemo: payload.result.critic.memo,
        createdAt: new Date().toISOString(),
      });
      upsert({ ...matter, status: "draft", updatedAt: new Date().toISOString() });
      if (payload.offline) toast.message("Offline skeleton — live counsel was unavailable.");
      else toast.success("Triad closed. Read the critic before circulating.");
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Counsel failed.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-6 pb-20">
      <header className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <Badge tone="associate">Instrument desk</Badge>
          <h1 className="mt-3 font-display text-3xl tracking-tight">Draft a New York instrument</h1>
          <p className="mt-2 max-w-2xl text-sm leading-normal text-muted">
            The Associate fills a verified template. The Critic will not let a
            missing GOL, DRL, or Hooper clause leave the building.
          </p>
        </div>
        <Disclaimer compact />
      </header>

      <div className="grid gap-6 lg:grid-cols-[280px_1fr]">
        <aside className="rounded-xl border border-border bg-surface p-4">
          <Label>Template</Label>
          <div className="mt-2 flex flex-col gap-1">
            {TEMPLATES.map((t) => (
              <button
                key={t.id}
                type="button"
                onClick={() => setTemplateId(t.id)}
                className={
                  t.id === templateId
                    ? "rounded-md bg-elevated px-3 py-2 text-left text-sm"
                    : "rounded-md px-3 py-2 text-left text-sm text-muted hover:bg-elevated hover:text-fg"
                }
              >
                {t.name}
              </button>
            ))}
          </div>
        </aside>

        <div className="flex flex-col gap-5">
          <section className="rounded-xl border border-border bg-surface p-5">
            <p className="font-display text-xl">{tmpl.name}</p>
            <p className="mt-2 text-sm text-muted">{tmpl.summary}</p>
            <p className="mt-4 font-mono text-[11px] uppercase tracking-wider text-subtle">
              Matter · {matter?.caption ?? "None selected"}
            </p>
            <div className="mt-4 flex flex-wrap gap-2">
              {required.statutes.map((s) =>
                s ? (
                  <a key={s.id} href={s.officialUrl} target="_blank" rel="noreferrer">
                    <Badge>
                      {s.lawId} § {s.section}
                    </Badge>
                  </a>
                ) : null,
              )}
              {required.cases.map((c) =>
                c ? (
                  <Badge key={c.id} tone="accent">
                    {c.name}
                  </Badge>
                ) : null,
              )}
            </div>
            <div className="mt-4">
              <Label htmlFor="extra">Additional instructions</Label>
              <Textarea
                id="extra"
                className="mt-2"
                value={extra}
                onChange={(e) => setExtra(e.target.value)}
                placeholder="Deal points, numbers, parenting calendar, carve-outs…"
              />
            </div>
            <div className="mt-4 flex flex-wrap gap-2">
              <Button disabled={busy} onClick={() => void generate("triad")}>
                {busy ? "Triad in session…" : "Run planner · executor · critic"}
              </Button>
              <Button
                variant="secondary"
                disabled={busy || !result}
                onClick={() => void generate("rewrite")}
              >
                Force rewrite
              </Button>
            </div>
            {offline ? (
              <p className="mt-3 text-xs text-warn">
                Live model offline — skeleton filled from the verified template bank.
              </p>
            ) : null}
          </section>

          {busy ? (
            <p className="shimmer rounded-md px-3 py-2 font-mono text-sm text-muted">
              Lead Partner issue-spotting · Associate harvesting · Critic loading the brief…
            </p>
          ) : null}

          {result ? (
            <>
              <div className="rounded-xl border border-border bg-surface p-4">
                <Label>Enforceability score</Label>
                <div className="mt-2">
                  <ScoreMeter score={result.critic.score} />
                </div>
              </div>
              <TriadColumns result={result} />
              <ContractPaper title={result.draft.title} body={result.draft.body} />
            </>
          ) : (
            <pre className="max-h-80 overflow-auto whitespace-pre-wrap rounded-xl border border-border bg-elevated p-5 font-mono text-xs leading-relaxed text-muted">
              {tmpl.skeleton.slice(0, 1800)}
              {tmpl.skeleton.length > 1800 ? "\n…" : ""}
            </pre>
          )}
        </div>
      </div>
    </div>
  );
}
