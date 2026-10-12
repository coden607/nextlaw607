import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import type { TriadResult } from "@/lib/types";

export function ScoreMeter({ score }: { score: number }) {
  const tone = score >= 85 ? "ok" : score >= 70 ? "warn" : "danger";
  return (
    <div className="flex items-center gap-3">
      <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-elevated">
        <div
          className={
            tone === "ok" ? "h-full bg-ok" : tone === "warn" ? "h-full bg-warn" : "h-full bg-danger"
          }
          style={{ width: `${Math.max(4, Math.min(100, score))}%` }}
        />
      </div>
      <span className="font-mono text-sm tabular-nums text-fg">{score}</span>
    </div>
  );
}

export function TriadColumns({ result }: { result: TriadResult }) {
  return (
    <div className="grid gap-4 lg:grid-cols-3">
      <section className="rounded-xl border border-border bg-surface p-4">
        <Badge tone="partner">Lead Partner</Badge>
        <h3 className="mt-3 font-display text-lg">Planner</h3>
        <p className="mt-2 text-sm leading-normal text-muted">{result.planner.framework}</p>
        <ul className="mt-3 space-y-1.5 text-sm text-fg">
          {result.planner.issues.map((i) => (
            <li key={i} className="border-l border-partner pl-3">
              {i}
            </li>
          ))}
        </ul>
        {result.planner.authorities.length ? (
          <div className="mt-4 space-y-1">
            {result.planner.authorities.map((a) => (
              <p key={a} className="font-mono text-[11px] leading-snug text-muted">
                {a}
              </p>
            ))}
          </div>
        ) : null}
      </section>

      <section className="rounded-xl border border-border bg-surface p-4">
        <Badge tone="associate">Associate</Badge>
        <h3 className="mt-3 font-display text-lg">Executor</h3>
        <p className="mt-2 text-sm text-muted">{result.draft.title}</p>
        <p className="mt-3 line-clamp-8 whitespace-pre-wrap font-display text-sm leading-relaxed text-fg">
          {result.draft.body.slice(0, 700)}
          {result.draft.body.length > 700 ? "…" : ""}
        </p>
      </section>

      <section className="rounded-xl border border-border bg-surface p-4">
        <Badge tone="critic">Opposing Counsel</Badge>
        <h3 className="mt-3 font-display text-lg">Critic</h3>
        <div className="mt-3">
          <ScoreMeter score={result.critic.score} />
        </div>
        <p className="mt-3 text-sm leading-normal text-muted">{result.critic.memo}</p>
        <ul className="mt-3 space-y-1.5 text-sm">
          {result.critic.flaws.map((f) => (
            <li key={f} className="border-l border-critic pl-3 text-fg">
              {f}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}

export function ContractPaper({
  title,
  body,
  onCopy,
}: {
  title: string;
  body: string;
  onCopy?: () => void;
}) {
  return (
    <article className="overflow-hidden rounded-xl border border-border">
      <div className="no-print flex items-center justify-between gap-3 border-b border-border bg-surface px-4 py-3">
        <h3 className="truncate font-display text-lg">{title}</h3>
        <div className="flex gap-2">
          <Button
            size="sm"
            variant="secondary"
            onClick={() => {
              void navigator.clipboard.writeText(body);
              onCopy?.();
            }}
          >
            Copy
          </Button>
          <Button size="sm" variant="secondary" onClick={() => window.print()}>
            Print
          </Button>
        </div>
      </div>
      <pre className="contract-paper max-h-[70vh] overflow-auto whitespace-pre-wrap px-6 py-8 font-display text-[15px] leading-relaxed md:px-10">
        {body}
      </pre>
    </article>
  );
}
