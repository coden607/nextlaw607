import { createFileRoute } from "@tanstack/react-router";
import { useRef, useState } from "react";
import { toast } from "sonner";
import { ContractPaper, TriadColumns } from "@/components/contract-view";
import { Disclaimer } from "@/components/disclaimer";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Label, Textarea } from "@/components/ui/input";
import { runTriad, speakCounsel } from "@/lib/ai";
import { searchOpinions } from "@/lib/courtlistener";
import { newDraftId, useCounsel } from "@/lib/store";
import type { TriadResult } from "@/lib/types";

type DictationEngine = {
  lang: string;
  continuous: boolean;
  interimResults: boolean;
  onresult: ((ev: { results: ArrayLike<ArrayLike<{ transcript: string }>> }) => void) | null;
  onend: (() => void) | null;
  start: () => void;
  stop: () => void;
};

type DictationCtor = new () => DictationEngine;

function getDictationCtor(): DictationCtor | undefined {
  if (typeof window === "undefined") return undefined;
  const w = window as unknown as {
    SpeechRecognition?: DictationCtor;
    webkitSpeechRecognition?: DictationCtor;
  };
  return w.SpeechRecognition ?? w.webkitSpeechRecognition;
}

export const Route = createFileRoute("/triad")({ component: TriadPage });

function TriadPage() {
  const matter = useCounsel((s) => s.matters.find((m) => m.id === s.activeMatterId) ?? s.matters[0]);
  const addDraft = useCounsel((s) => s.addDraft);
  const voiceOn = useCounsel((s) => s.voiceOn);
  const [prompt, setPrompt] = useState(
    "Attack and then rebuild the pending instrument. Identify every missing DRL, FCA, GOL, or CPL hook.",
  );
  const [busy, setBusy] = useState(false);
  const [listening, setListening] = useState(false);
  const [result, setResult] = useState<TriadResult | null>(null);
  const recRef = useRef<DictationEngine | null>(null);

  function startDictation() {
    const SR = getDictationCtor();
    if (!SR) {
      toast.error("This browser has no speech recognition.");
      return;
    }
    const rec = new SR();
    rec.lang = "en-US";
    rec.continuous = true;
    rec.interimResults = true;
    rec.onresult = (ev) => {
      let t = "";
      for (let i = 0; i < ev.results.length; i++) t += ev.results[i][0].transcript;
      setPrompt(t);
    };
    rec.onend = () => setListening(false);
    recRef.current = rec;
    rec.start();
    setListening(true);
  }

  function stopDictation() {
    recRef.current?.stop();
    setListening(false);
  }

  async function run() {
    if (!matter) return;
    setBusy(true);
    try {
      const live = await searchOpinions({
        data: { q: `${matter.caption} ${matter.objectives}`.slice(0, 160) },
      });
      const liveAuthorities = live.ok
        ? live.hits.map((h) => `${h.caseName} — ${h.citations[0] ?? h.court} — ${h.url}`).join("\n")
        : "";
      const payload = await runTriad({
        data: {
          mode: "triad",
          practice: matter.practice,
          caption: matter.caption,
          county: matter.county,
          parties: matter.parties,
          facts: matter.facts,
          objectives: matter.objectives,
          extra: prompt,
          liveAuthorities,
        },
      });
      if (!payload.result) {
        toast.error(payload.error ?? "Triad failed");
        return;
      }
      setResult(payload.result);
      addDraft({
        id: newDraftId(),
        matterId: matter.id,
        templateId: "custom",
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
      if (voiceOn && payload.result.critic.memo) {
        const spoken = await speakCounsel({
          data: { text: payload.result.critic.memo },
        });
        if (spoken.ok) {
          const audio = new Audio(`data:${spoken.mime};base64,${spoken.audio}`);
          void audio.play();
        }
      }
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Triad failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-6 pb-20">
      <header>
        <Badge tone="critic">Adversarial session</Badge>
        <h1 className="mt-3 font-display text-3xl tracking-tight">Planner · Executor · Critic</h1>
        <p className="mt-2 max-w-2xl text-sm leading-normal text-muted">
          One user-initiated run. The Lead Partner frames the matrix, the
          Associate drafts against the verified bank, Opposing Counsel scores
          the paper. Dictate walking into the courtroom; arm Voice on the rail
          to hear the critic aloud.
        </p>
      </header>

      <section className="rounded-xl border border-border bg-surface p-5">
        <p className="font-mono text-[11px] uppercase tracking-wider text-subtle">
          {matter ? `${matter.caption} · ${matter.county} County` : "No matter loaded"}
        </p>
        <Label htmlFor="brief" className="mt-4 block">
          Session brief
        </Label>
        <Textarea
          id="brief"
          className="mt-2 min-h-32"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
        <div className="mt-4 flex flex-wrap gap-2">
          <Button disabled={busy || !matter} onClick={() => void run()}>
            {busy ? "Agents in conference…" : "Open the session"}
          </Button>
          <Button
            variant="secondary"
            onClick={() => (listening ? stopDictation() : startDictation())}
          >
            {listening ? "Stop dictation" : "Dictate"}
          </Button>
        </div>
        {busy ? (
          <p className="shimmer mt-4 rounded-md px-3 py-2 font-mono text-sm text-muted">
            Hierarchical triad running — no silent citations.
          </p>
        ) : null}
      </section>

      {result ? (
        <>
          <TriadColumns result={result} />
          {result.critic.rewriteDirectives.length ? (
            <section className="rounded-xl border border-border bg-surface p-5">
              <h2 className="font-display text-xl">Rewrite directives</h2>
              <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-muted">
                {result.critic.rewriteDirectives.map((d) => (
                  <li key={d}>{d}</li>
                ))}
              </ul>
            </section>
          ) : null}
          <ContractPaper title={result.draft.title} body={result.draft.body} />
        </>
      ) : (
        <div className="grid gap-4 md:grid-cols-3">
          {[
            ["01", "Lead Partner", "Decompose standing, forum, SOF, elements, and the worst opposing argument."],
            ["02", "Associate", "Harvest Court of Appeals and the relevant Appellate Division. Fill the instrument."],
            ["03", "Opposing Counsel", "Reject unverified cites. Score below 85 forces rewrite."],
          ].map(([n, t, d]) => (
            <article key={n} className="rounded-xl border border-border bg-surface p-5">
              <p className="font-mono text-xs text-subtle">{n}</p>
              <h2 className="mt-2 font-display text-xl">{t}</h2>
              <p className="mt-2 text-sm text-muted">{d}</p>
            </article>
          ))}
        </div>
      )}
      <Disclaimer />
    </div>
  );
}
