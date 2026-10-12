import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { toast } from "sonner";
import { ContractPaper, ScoreMeter } from "@/components/contract-view";
import { Disclaimer } from "@/components/disclaimer";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useCounsel } from "@/lib/store";
import { templateById } from "@/lib/templates";
import { PRACTICE_LABEL } from "@/lib/types";
export const Route = createFileRoute("/drafts")({ component: Drafts });

function Drafts() {
  const navigate = useNavigate();
  const matters = useCounsel((s) => s.matters);
  const drafts = useCounsel((s) => s.drafts);
  const del = useCounsel((s) => s.deleteDraft);
  const [openId, setOpenId] = useState<string | null>(null);

  const open = drafts.find((d) => d.id === openId) ?? null;
  const matterFor = (id: string) => matters.find((m) => m.id === id);

  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-6 pb-20">
      <header className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <Badge tone="associate">Work product</Badge>
          <h1 className="mt-3 font-display text-3xl tracking-tight">The drafts drawer</h1>
          <p className="mt-2 max-w-xl text-sm text-muted">
            Every instrument the triad has closed, newest first. Local to this
            browser. Review the critic before circulating anything — nothing
            here is a court filing.
          </p>
        </div>
        <Button onClick={() => navigate({ to: "/draft" })}>New draft</Button>
      </header>

      {drafts.length === 0 ? (
        <p className="rounded-xl border border-border bg-surface p-6 text-sm text-muted">
          No drafts yet. Run the instrument desk or open a triad session to create work product.
        </p>
      ) : open ? (
        <DraftDetail
          draft={open}
          caption={matterFor(open.matterId)?.caption ?? "Closed matter"}
          onClose={() => setOpenId(null)}
          onDelete={() => {
            del(open.id);
            toast.success("Draft discarded.");
            setOpenId(null);
          }}
        />
      ) : (
        <ul className="space-y-3">
          {drafts.map((d) => {
            const matter = matterFor(d.matterId);
            const tmpl = templateById(d.templateId);
            return (
              <li key={d.id} className="rounded-xl border border-border bg-surface p-5">
                <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
                  <div className="min-w-0">
                    <div className="flex flex-wrap items-center gap-2">
                      <h2 className="font-display text-xl">{d.title}</h2>
                      <Badge tone={d.criticScore && d.criticScore >= 85 ? "ok" : "warn"}>
                        Critic {d.criticScore ?? "—"}
                      </Badge>
                      {d.missingAuthorities.length ? (
                        <Badge tone="critic">{d.missingAuthorities.length} gaps</Badge>
                      ) : null}
                    </div>
                    <p className="mt-1 font-mono text-[11px] uppercase tracking-wider text-subtle">
                      {tmpl?.name ?? d.templateId}
                      {matter ? ` · ${matter.caption}` : ""} ·{" "}
                      {matter ? PRACTICE_LABEL[matter.practice] : ""}
                    </p>
                    <p className="mt-3 text-sm leading-normal text-muted">
                      {(d.criticNotes[0] ?? d.plannerMemo.slice(0, 160)) || "Awaiting critique"}
                    </p>
                    <p className="mt-2 font-mono text-xs text-subtle">
                      {new Date(d.createdAt).toLocaleString()} · {d.citations.length} verified
                      citations on file
                    </p>
                  </div>
                  <div className="flex shrink-0 flex-wrap gap-2">
                    <Button size="sm" onClick={() => setOpenId(d.id)}>
                      Review
                    </Button>
                    <Button
                      size="sm"
                      variant="ghost"
                      onClick={() => {
                        del(d.id);
                        toast.success("Draft discarded.");
                      }}
                    >
                      Discard
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

function DraftDetail({
  draft,
  caption,
  onClose,
  onDelete,
}: {
  draft: (ReturnType<typeof useCounsel.getState>["drafts"])[number];
  caption: string;
  onClose: () => void;
  onDelete: () => void;
}) {
  const navigate = useNavigate();
  const matterId = draft.matterId;
  return (
    <div className="flex flex-col gap-5">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-2">
          <Button size="sm" variant="secondary" onClick={onClose}>
            All drafts
          </Button>
          <Badge tone={draft.criticScore && draft.criticScore >= 85 ? "ok" : "warn"}>
            Critic {draft.criticScore ?? "—"}
          </Badge>
        </div>
        <div className="flex flex-wrap gap-2">
          <Button
            size="sm"
            variant="secondary"
            onClick={() => navigate({ to: "/matters" })}
            disabled={!matterId}
          >
            Matter file
          </Button>
          <Button size="sm" variant="ghost" onClick={onDelete}>
            Discard
          </Button>
        </div>
      </div>

      <div>
        <h2 className="font-display text-2xl tracking-tight">{draft.title}</h2>
        <p className="mt-1 font-mono text-[11px] uppercase tracking-wider text-subtle">
          {caption} · {new Date(draft.createdAt).toLocaleString()}
        </p>
      </div>

      <div className="rounded-xl border border-border bg-surface p-4">
        <p className="font-mono text-[11px] uppercase tracking-wider text-subtle">
          Enforceability
        </p>
        <div className="mt-2">
          <ScoreMeter score={draft.criticScore ?? 0} />
        </div>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <section className="rounded-xl border border-border bg-surface p-4">
          <Badge tone="partner">Lead Partner</Badge>
          <p className="mt-3 whitespace-pre-wrap text-sm leading-normal text-muted">
            {draft.plannerMemo || "No planner memo recorded."}
          </p>
        </section>
        <section className="rounded-xl border border-border bg-surface p-4">
          <Badge tone="critic">Opposing Counsel</Badge>
          <p className="mt-3 whitespace-pre-wrap text-sm leading-normal text-muted">
            {draft.criticMemo || "No critic memo recorded."}
          </p>
          {draft.criticNotes.length ? (
            <ul className="mt-3 space-y-1.5 text-sm">
              {draft.criticNotes.map((f) => (
                <li key={f} className="border-l border-critic pl-3 text-fg">
                  {f}
                </li>
              ))}
            </ul>
          ) : null}
          {draft.missingAuthorities.length ? (
            <div className="mt-3">
              <p className="font-mono text-[11px] uppercase tracking-wider text-subtle">
                Missing authority
              </p>
              <ul className="mt-1 space-y-1 text-sm text-warn">
                {draft.missingAuthorities.map((m) => (
                  <li key={m}>{m}</li>
                ))}
              </ul>
            </div>
          ) : null}
        </section>
      </div>

      {draft.citations.length ? (
        <section className="rounded-xl border border-border bg-surface p-4">
          <Badge>Verified citations on file</Badge>
          <ul className="mt-3 space-y-2">
            {draft.citations.map((c) => (
              <li key={c.id} className="text-sm">
                <a
                  href={c.url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-accent underline-offset-4 hover:underline"
                >
                  {c.bluebook}
                </a>
                <span className="text-subtle"> · {c.source} · verified</span>
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      <ContractPaper
        title={draft.title}
        body={draft.body}
        onCopy={() => toast.success("Draft copied. Attorney review still required.")}
      />
    </div>
  );
}
