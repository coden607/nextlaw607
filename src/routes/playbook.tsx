import { createFileRoute } from "@tanstack/react-router";
import { Disclaimer } from "@/components/disclaimer";
import { Badge } from "@/components/ui/badge";
import { PERSONA, SKILLS, WORKFLOW } from "@/lib/skills";

export const Route = createFileRoute("/playbook")({ component: Playbook });

export function Playbook() {
  return (
    <div className="mx-auto flex max-w-4xl flex-col gap-8 pb-20">
      <header>
        <Badge tone="partner">Persona · skills · MCP · workflow</Badge>
        <h1 className="mt-3 font-display text-3xl tracking-tight">Counsel operating system</h1>
        <p className="mt-2 text-sm leading-normal text-muted">
          The rules the triad cannot waive. Every Grok call is prepended with
          this persona, the skill cards, and the verified New York bank.
        </p>
      </header>

      <section className="rounded-xl border border-border bg-surface p-5">
        <h2 className="font-display text-xl">Persona</h2>
        <pre className="mt-4 whitespace-pre-wrap font-mono text-xs leading-relaxed text-muted">
          {PERSONA}
        </pre>
      </section>

      <section>
        <h2 className="font-display text-xl">Skills</h2>
        <div className="mt-4 grid gap-4">
          {SKILLS.map((s) => (
            <article key={s.id} className="rounded-xl border border-border bg-surface p-5">
              <div className="flex flex-wrap items-center gap-2">
                <h3 className="font-display text-lg">{s.name}</h3>
                <Badge>{s.id}</Badge>
              </div>
              <p className="mt-2 font-mono text-[11px] text-subtle">Trigger · {s.trigger}</p>
              <p className="mt-3 text-sm leading-normal text-muted">{s.mandate}</p>
              <ol className="mt-3 list-decimal space-y-1 pl-5 text-sm text-fg">
                {s.steps.map((st) => (
                  <li key={st}>{st}</li>
                ))}
              </ol>
            </article>
          ))}
        </div>
      </section>

      <section>
        <h2 className="font-display text-xl">Workflow</h2>
        <ol className="mt-4 space-y-3">
          {WORKFLOW.map((w, i) => (
            <li key={w.id} className="flex gap-4 rounded-xl border border-border bg-surface p-4">
              <span className="font-mono text-sm text-subtle">{String(i + 1).padStart(2, "0")}</span>
              <div>
                <p className="font-medium">{w.title}</p>
                <p className="mt-1 text-sm leading-normal text-muted">{w.detail}</p>
              </div>
            </li>
          ))}
        </ol>
      </section>

      <section className="rounded-xl border border-border bg-surface p-5">
        <h2 className="font-display text-xl">MCP gateway</h2>
        <p className="mt-2 text-sm leading-normal text-muted">
          CourtListener v4 is the Westlaw/Lexis bypass: opinions, dockets, oral
          arguments, and citation networks over Streamable HTTP at
          mcp.courtlistener.com, with REST fallback on
          courtlistener.com/api/rest/v4/. Tokens stay on the server. NY Senate
          Open Legislation supplies blackletter text. Internal tools:
        </p>
        <ul className="mt-3 space-y-2 font-mono text-xs text-muted">
          <li>search_opinions(q, court=ny,nyappdiv,nysupct,ca2)</li>
          <li>get_statute(lawId, section) → legislation.nysenate.gov</li>
          <li>run_triad(mode, matter, template) → planner / draft / critic JSON</li>
          <li>speak_counsel(text) → on-call voice</li>
        </ul>
        <p className="mt-4 font-mono text-xs text-subtle">
          CLI surface · ./nextlaw draft ica · ./nextlaw research "Tropea" · ./nextlaw
          cite DOM/70 · ./nextlaw critic
        </p>
      </section>
      <Disclaimer />
    </div>
  );
}
