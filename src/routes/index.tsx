import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { ArrowRight, Scale, Shield, PenLine } from "lucide-react";
import { useMemo, useState } from "react";
import { Disclaimer } from "@/components/disclaimer";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { CRIMINAL_CASES, CRIMINAL_STATUTES } from "@/lib/corpus";
import { useCounsel } from "@/lib/store";
import { CRIMINAL_TEMPLATES } from "@/lib/templates";
import { PRACTICE_LABEL } from "@/lib/types";
import { cn } from "@/lib/cn";

export const Route = createFileRoute("/")({ component: Deck });

function Deck() {
  const navigate = useNavigate();
  const [cmd, setCmd] = useState("");
  const matters = useCounsel((s) => s.matters);
  const drafts = useCounsel((s) => s.drafts);
  const activeId = useCounsel((s) => s.activeMatterId);
  const setActive = useCounsel((s) => s.setActiveMatter);
  const holoMode = useCounsel((s) => s.holoMode);
  const latest = drafts[0];
  const authority = useMemo(() => {
    const i = new Date().getDate() % CRIMINAL_CASES.length;
    return CRIMINAL_CASES[i];
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
          <Badge tone={holoMode ? "holo" : "accent"}>Zero-hallucination mandate</Badge>
          <h1 className={cn("mt-4 font-display text-4xl leading-tight tracking-tight md:text-5xl", holoMode && "holo-flicker")}>
            New York criminal law, verified before it speaks.
          </h1>
          <p className="mt-4 max-w-xl text-base leading-normal text-muted">
            NextLaw607 centers New York criminal law and criminal procedure: CPL and Penal Law, suppression, discovery, speedy trial, pleas, sentencing, preservation, appeals, and post-conviction work. Intersecting law remains available when it materially affects the criminal matter or remedy.
          </p>
        </div>
        <Disclaimer />
      </section>

      <form
        className={cn(
          "flex flex-col gap-3 rounded-xl border border-border bg-surface p-3 md:flex-row md:items-center relative transition-all",
          holoMode && "holo-card holo-corner-brackets",
        )}
        onSubmit={(e) => {
          e.preventDefault();
          runCommand(cmd);
        }}
      >
        <span
          className={cn(
            "hidden px-3 font-mono text-xs text-subtle md:inline",
            holoMode && "text-cyan-400 font-semibold drop-shadow-[0_0_6px_rgba(0,240,255,0.4)]",
          )}
        >
          ./nextlaw
        </span>
        <Input
          value={cmd}
          onChange={(e) => setCmd(e.target.value)}
          placeholder="research CPL 30.30 · draft suppression motion · cite CPL 245 · triad"
          className={cn("border-0 bg-transparent font-mono", holoMode && "placeholder:text-cyan-400/40 text-cyan-100")}
          aria-label="Counsel command"
        />
        <Button type="submit" variant={holoMode ? "holo" : "primary"} className="shrink-0">
          Run
          <ArrowRight />
        </Button>
      </form>

      <section className="grid gap-4 md:grid-cols-3">
        {[
          {
            role: "Lead Partner",
            tone: holoMode ? ("holo" as const) : ("partner" as const),
            icon: Scale,
            copy: "Ingests the matter, decomposes the legal matrix, and maps the tactical framework before a word of operative text is written.",
          },
          {
            role: "Associate",
            tone: holoMode ? ("holo" as const) : ("associate" as const),
            icon: PenLine,
            copy: "Bound to the verified NY bank and the CourtListener v4 gateway. Pulls Appellate Division and Court of Appeals authority only.",
          },
          {
            role: "Opposing Counsel",
            tone: holoMode ? ("holo" as const) : ("critic" as const),
            icon: Shield,
            copy: "Red-team filter. Missing CPL/PL hooks, suppression gaps, preservation defects, and unverified citations force an automated rewrite.",
          },
        ].map((a) => (
          <article
            key={a.role}
            className={cn(
              "rounded-xl border border-border bg-surface p-5 relative transition-all",
              holoMode && "holo-card holo-corner-brackets",
            )}
          >
            <Badge tone={a.tone}>{a.role}</Badge>
            <a.icon className={cn("mt-4 size-5 text-fg", holoMode && "text-cyan-300 drop-shadow-[0_0_6px_#00f0ff]")} />
            <p className="mt-3 text-sm leading-normal text-muted">{a.copy}</p>
          </article>
        ))}
      </section>

      <section className="grid gap-4 lg:grid-cols-[1fr_1fr]">
        <article
          className={cn(
            "rounded-xl border border-border bg-surface p-5 relative transition-all",
            holoMode && "holo-card holo-corner-brackets",
          )}
        >
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

        <article
          className={cn(
            "rounded-xl border border-border bg-surface p-5 relative transition-all",
            holoMode && "holo-card holo-corner-brackets",
          )}
        >
          <div className="flex items-center justify-between gap-3">
            <h2 className="font-display text-xl">Authority of the day</h2>
            {holoMode ? <Badge tone="holo">Verified NY</Badge> : null}
          </div>
          <p className={cn("mt-3 font-display text-lg leading-snug", holoMode && "text-cyan-100")}>{authority.name}</p>
          <p className="mt-1 font-mono text-xs text-muted">{authority.bluebook}</p>
          <p className="mt-3 text-sm leading-normal text-muted">{authority.holding}</p>
          <a
            href={authority.officialUrl}
            className={cn(
              "mt-4 inline-flex h-11 items-center text-sm text-accent underline-offset-4 hover:underline",
              holoMode && "text-cyan-300 hover:text-cyan-200 drop-shadow-[0_0_6px_rgba(0,240,255,0.4)]",
            )}
            target="_blank"
            rel="noreferrer"
          >
            Open source ↗
          </a>
        </article>
      </section>

      <section>
        <div className="flex items-end justify-between gap-3">
          <h2 className="font-display text-xl">Instrument desk</h2>
          <p className={cn("font-mono text-[11px] uppercase tracking-wider text-subtle", holoMode && "text-cyan-400/60")}>
            {CRIMINAL_STATUTES.length} statutes · {CRIMINAL_CASES.length} criminal-law cases
          </p>
        </div>
        <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {CRIMINAL_TEMPLATES.map((t) => (
            <button
              key={t.id}
              type="button"
              onClick={() => navigate({ to: "/draft", search: { template: t.id } })}
              className={cn(
                "rounded-xl border border-border bg-surface p-4 text-left transition-all duration-[var(--motion-quick)] hover:bg-elevated",
                holoMode && "border-cyan-500/20 hover:border-cyan-400/50 hover:shadow-[0_0_15px_rgba(0,240,255,0.15)]",
              )}
            >
              <p className={cn("text-sm font-medium text-fg", holoMode && "group-hover:text-cyan-200")}>{t.name}</p>
              <p className="mt-2 text-xs leading-normal text-muted">{t.summary}</p>
            </button>
          ))}
        </div>
      </section>

      {latest ? (
        <article
          className={cn(
            "rounded-xl border border-border bg-elevated p-5 relative transition-all",
            holoMode && "holo-card holo-corner-brackets",
          )}
        >
          <Badge tone={latest.criticScore && latest.criticScore >= 85 ? (holoMode ? "holo" : "ok") : "warn"}>
            Last triad {latest.criticScore ?? "—"}
          </Badge>
          <p className={cn("mt-3 font-display text-lg", holoMode && "holo-text")}>{latest.title}</p>
          <p className="mt-1 text-sm text-muted">
            {new Date(latest.createdAt).toLocaleString()} · {latest.criticNotes[0] ?? "Awaiting critique"}
          </p>
        </article>
      ) : null}
    </div>
  );
}
