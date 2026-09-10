import { createFileRoute } from "@tanstack/react-router";
import { Disclaimer } from "@/components/disclaimer";
import { Badge } from "@/components/ui/badge";
import { LAYER_LABEL, MEDIN_VIDEO, STACK, type StackNode } from "@/lib/medin-stack";

export const Route = createFileRoute("/stack")({ component: StackPage });

const LAYERS = Object.keys(LAYER_LABEL) as StackNode["layer"][];

export function StackPage() {
  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-8 pb-20">
      <header>
        <Badge>Captions scraped</Badge>
        <h1 className="mt-3 font-display text-3xl tracking-tight">{MEDIN_VIDEO.title}</h1>
        <p className="mt-2 text-sm leading-normal text-muted">
          Cole Medin · {MEDIN_VIDEO.duration} · published {MEDIN_VIDEO.published}. NextLaw607
          is the legal mapping of that AI-first stack: Postgres memory, Pydantic-style
          typed agents, LangGraph triad, Docling ingest, Arcade-style MCP auth, and a
          $0/month self-host path.
        </p>
        <p className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-sm">
          <a
            className="text-accent underline-offset-4 hover:underline"
            href={MEDIN_VIDEO.url}
            target="_blank"
            rel="noreferrer"
          >
            Full video
          </a>
          <a
            className="text-accent underline-offset-4 hover:underline"
            href={MEDIN_VIDEO.shortUrl}
            target="_blank"
            rel="noreferrer"
          >
            Short
          </a>
        </p>
      </header>

      <section className="rounded-xl border border-border bg-surface p-5">
        <h2 className="font-display text-xl">From the captions</h2>
        <ul className="mt-4 space-y-3">
          {MEDIN_VIDEO.captions.map((c) => (
            <li key={c} className="border-l border-border pl-4 text-sm leading-normal text-muted">
              {c}
            </li>
          ))}
        </ul>
        <ol className="mt-6 grid gap-2 sm:grid-cols-2">
          {MEDIN_VIDEO.chapters.map((ch) => (
            <li key={ch.t} className="font-mono text-xs text-subtle">
              {ch.t} · {ch.title}
            </li>
          ))}
        </ol>
      </section>

      {LAYERS.map((layer) => (
        <section key={layer}>
          <h2 className="font-display text-xl">{LAYER_LABEL[layer]}</h2>
          <div className="mt-4 grid gap-3">
            {STACK.filter((n) => n.layer === layer).map((n) => (
              <article key={n.id} className="rounded-xl border border-border bg-surface p-5">
                <div className="flex flex-wrap items-center gap-2">
                  <h3 className="font-display text-lg">{n.name}</h3>
                  {n.oss ? <Badge tone="ok">OSS</Badge> : <Badge>Hosted</Badge>}
                </div>
                <p className="mt-1 text-xs uppercase tracking-wider text-subtle">{n.role}</p>
                <p className="mt-3 text-sm leading-normal text-muted">{n.why}</p>
                {n.alts.length ? (
                  <p className="mt-2 font-mono text-[11px] text-subtle">
                    Alternatives · {n.alts.join(" · ")}
                  </p>
                ) : null}
                <p className="mt-3 text-sm text-fg">
                  <span className="text-subtle">NextLaw map · </span>
                  {n.nextlaw}
                </p>
              </article>
            ))}
          </div>
        </section>
      ))}
      <Disclaimer />
    </div>
  );
}
