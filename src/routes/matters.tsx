import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { Disclaimer } from "@/components/disclaimer";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useCounsel } from "@/lib/store";
import { PRACTICE_LABEL } from "@/lib/types";

export const Route = createFileRoute("/matters")({ component: Matters });

function Matters() {
  const navigate = useNavigate();
  const matters = useCounsel((s) => s.matters);
  const drafts = useCounsel((s) => s.drafts);
  const activeId = useCounsel((s) => s.activeMatterId);
  const setActive = useCounsel((s) => s.setActiveMatter);
  const del = useCounsel((s) => s.deleteMatter);

  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-6 pb-20">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <Badge>Matter files</Badge>
          <h1 className="mt-3 font-display text-3xl tracking-tight">The file room</h1>
          <p className="mt-2 max-w-xl text-sm text-muted">
            Local to this browser. Nothing here is a court filing. Select a
            matter to feed the triad and the instrument desk.
          </p>
        </div>
        <Button onClick={() => navigate({ to: "/intake" })}>New intake</Button>
      </header>

      {matters.length === 0 ? (
        <p className="rounded-xl border border-border bg-surface p-6 text-sm text-muted">
          No matters yet.
        </p>
      ) : (
        <ul className="space-y-3">
          {matters.map((m) => {
            const related = drafts.filter((d) => d.matterId === m.id);
            const last = related[0];
            return (
              <li key={m.id} className="rounded-xl border border-border bg-surface p-5">
                <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                  <div className="min-w-0">
                    <div className="flex flex-wrap items-center gap-2">
                      <h2 className="font-display text-xl">{m.caption}</h2>
                      {m.id === activeId ? <Badge tone="accent">Active</Badge> : null}
                      <Badge>{m.status}</Badge>
                    </div>
                    <p className="mt-1 font-mono text-[11px] uppercase tracking-wider text-subtle">
                      {PRACTICE_LABEL[m.practice]} · {m.county} County
                    </p>
                    <p className="mt-3 text-sm leading-normal text-muted">{m.facts}</p>
                    <ul className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-sm">
                      {m.parties.map((p) => (
                        <li key={p.role + p.name} className="text-fg">
                          <span className="text-subtle">{p.role}:</span> {p.name}
                        </li>
                      ))}
                    </ul>
                    {last ? (
                      <p className="mt-3 font-mono text-xs text-muted">
                        Last draft · {last.title} · score {last.criticScore ?? "—"}
                      </p>
                    ) : null}
                  </div>
                  <div className="flex shrink-0 flex-wrap gap-2">
                    <Button
                      size="sm"
                      variant={m.id === activeId ? "primary" : "secondary"}
                      onClick={() => setActive(m.id)}
                    >
                      Make active
                    </Button>
                    <Button size="sm" variant="secondary" onClick={() => navigate({ to: "/draft" })}>
                      Draft
                    </Button>
                    <Button size="sm" variant="ghost" onClick={() => del(m.id)}>
                      Close file
                    </Button>
                  </div>
                </div>
              </li>
            );
          })}
        </ul>
      )}
      <Disclaimer />
    </div>
  );
}
