import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { ArrowRight, Scale, Shield, PenLine } from "lucide-react";
import { useMemo, useState } from "react";
import { Disclaimer } from "@/components/disclaimer";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { CASES, STATUTES } from "@/lib/corpus";
import { useCounsel } from "@/lib/store";
import { TEMPLATES } from "@/lib/templates";
import { PRACTICE_LABEL } from "@/lib/types";

export const Route = createFileRoute("/")({ component: Deck });

function Deck() {
  const navigate = useNavigate();
  const [cmd, setCmd] = useState("");
  const matters = useCounsel((s) => s.matters);
  const drafts = useCounsel((s) => s.drafts);
  const activeId = useCounsel((s) => s.activeMatterId);
  const setActive = useCounsel((s) => s.setActiveMatter);
  const latest = drafts[0];
  const authority = useMemo(() => {
    const i = new Date().getDate() % CASES.length;
    return CASES[i];
  }, []);

  function runCommand(raw: string) {
    const q = raw.trim();
    if (!q) return;
    const lower = q.toLowerCase();
    if (lower.startsWith("draft")) {
      void navigate({ to: "/draft" });
      return;
    }
    if (lower.startsWith("research") || lower.startsWith("cite")) {
      const rest = q.replace(/^(research|cite)\s+/i, "");
      void navigate({ to: "/research", search: { q: rest } });
      return;
    }
    if (lower.startsWith("intake") || lower.startsWith("matter")) {
      void navigate({ to: "/intake" });
      return;
    }
    if (lower.startsWith("triad") || lower.startsWith("critic")) {
      void navigate({ to: "/triad" });
      return;
    }
    void navigate({ to: "/research", search: { q } });
  }

  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-8 pb-16">
      <section className="grid gap-8 lg:grid-cols-[1.4fr_0.9fr] lg:items-end">
        <div>
          <Badge tone="accent">Zero-hallucination mandate</Badge>
          <h1 className="mt-4 font-display text-4xl leading-tight tracking-tight md:text-5xl">
            The counsel terminal that will not invent a citation.
          </h1>
          <p className="mt-4 max-w-xl text-base leading-normal text-muted">
            NextLaw607 drafts New York instruments, harvests binding Court of
            Appeals and Appellate Division authority, and then attacks its own
            work as opposing counsel. Built for DRL §§ 70/240, FCA Article 6,
            CPL, the Penal Law, and the General Obligations Law.
          </p>
        </div>
        <Disclaimer />
      </section>

      <form
        className="flex flex-col gap-3 rounded-xl border border-border bg-surface p-3 md:flex-row md:items-center"
        onSubmit={(e) => {
          e.preventDefault();
          runCommand(cmd);
        }}
      >
        <span className="hidden px-3 font-mono text-xs text-subtle md:inline">
          ./nextlaw
        </span>
        <Input
          value={cmd}
          onChange={(e) => setCmd(e.target.value)}
          placeholder="draft ica · research best interests · cite DRL 70 · triad"
          className="border-0 bg-transparent font-mono"
          aria-label="Counsel command"
        />
        <Button type="submit" className="shrink-0">
          Run
          <ArrowRight />
        </Button>
      </form>

      <section className="grid gap-4 md:grid-cols-3">
        {[
          {
            role: "Lead Partner",
            tone: "partner" as const,
            icon: Scale,
            copy: "Ingests the matter, decomposes the legal matrix, and maps the tactical framework before a word of operative text is written.",
          },
          {
            role: "Associate",
            tone: "associate" as const,
            icon: PenLine,
            copy: "Bound to the verified NY bank and the CourtListener v4 gateway. Pulls Appellate Division and Court of Appeals authority only.",
          },
          {
            role: "Opposing Counsel",
            tone: "critic" as const,
            icon: Shield,
            copy: "Red-team filter. Missing DRL/FCA hooks, unverified cites, and Hooper-unclear fee clauses force an automated rewrite.",
          },
        ].map((a) => (
          <article key={a.role} className="rounded-xl border border-border bg-surface p-5">
            <Badge tone={a.tone}>{a.role}</Badge>
            <a.icon className="mt-4 size-5 text-fg" />
            <p className="mt-3 text-sm leading-normal text-muted">{a.copy}</p>
          </article>
        ))}
      </section>

      <section className="grid gap-4 lg:grid-cols-[1fr_1fr]">
        <article className="rounded-xl border border-border bg-surface p-5">
          <div className="flex items-center justify-between gap-3">
            <h2 className="font-display text-xl">Open matters</h2>
            <Button size="sm" variant="ghost" onClick={() => navigate({ to: "/matters" })}>
              All
            </Button>
          </div>
          <ul className="mt-4 divide-y divide-border">
            {matters.slice(0, 4).map((m) => (
              <li key={m.id}>
                <button
                  type="button"
                  onClick={() => {
                    setActive(m.id);
                    void navigate({ to: "/matters" });
                  }}
                  className="flex w-full items-start justify-between gap-3 py-3 text-left"
                >
                  <span>
                    <span className="block text-sm text-fg">{m.caption}</span>
                    <span className="mt-1 block font-mono text-[11px] uppercase tracking-wider text-subtle">
                      {PRACTICE_LABEL[m.practice]} · {m.county} County
                    </span>
                  </span>
                  {m.id === activeId ? <Badge tone="accent">Active</Badge> : null}
                </button>
              </li>
            ))}
          </ul>
        </article>

        <article className="rounded-xl border border-border bg-surface p-5">
          <h2 className="font-display text-xl">Authority of the day</h2>
          <p className="mt-3 font-display text-lg leading-snug">{authority.name}</p>
          <p className="mt-1 font-mono text-xs text-muted">{authority.bluebook}</p>
          <p className="mt-3 text-sm leading-normal text-muted">{authority.holding}</p>
          <a
            href={authority.officialUrl}
            className="mt-4 inline-flex h-11 items-center text-sm text-accent underline-offset-4 hover:underline"
            target="_blank"
            rel="noreferrer"
          >
            Open source
          </a>
        </article>
      </section>

      <section>
        <div className="flex items-end justify-between gap-3">
          <h2 className="font-display text-xl">Instrument desk</h2>
          <p className="font-mono text-[11px] uppercase tracking-wider text-subtle">
            {STATUTES.length} statutes · {CASES.length} binding cases
          </p>
        </div>
        <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {TEMPLATES.map((t) => (
            <button
              key={t.id}
              type="button"
              onClick={() => navigate({ to: "/draft", search: { template: t.id } })}
              className="rounded-xl border border-border bg-surface p-4 text-left transition-colors duration-[var(--motion-quick)] hover:bg-elevated"
            >
              <p className="text-sm font-medium text-fg">{t.name}</p>
              <p className="mt-2 text-xs leading-normal text-muted">{t.summary}</p>
            </button>
          ))}
        </div>
      </section>

      {latest ? (
        <article className="rounded-xl border border-border bg-elevated p-5">
          <Badge tone={latest.criticScore && latest.criticScore >= 85 ? "ok" : "warn"}>
            Last triad {latest.criticScore ?? "—"}
          </Badge>
          <p className="mt-3 font-display text-lg">{latest.title}</p>
          <p className="mt-1 text-sm text-muted">
            {new Date(latest.createdAt).toLocaleString()} · {latest.criticNotes[0] ?? "Awaiting critique"}
          </p>
        </article>
      ) : null}
    </div>
  );
}
