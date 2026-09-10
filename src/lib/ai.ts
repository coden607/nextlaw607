import { createServerFn } from "@tanstack/react-start";
import { CASES, STATUTES, corpusPromptBlock } from "./corpus";
import { PERSONA, skillsPromptBlock } from "./skills";
import { TEMPLATES } from "./templates";
import type { PracticeArea, TriadResult } from "./types";

type CounselInput = {
  mode: "triad" | "rewrite" | "research-memo";
  practice: PracticeArea;
  templateId?: string;
  caption: string;
  county: string;
  parties: { role: string; name: string }[];
  facts: string;
  objectives: string;
  extra?: string;
  liveAuthorities?: string;
  priorDraft?: string;
  criticNotes?: string[];
};

function extractJson(text: string): unknown {
  const fence = text.match(/```json\s*([\s\S]*?)```/i);
  const raw = fence?.[1] ?? text;
  const start = raw.indexOf("{");
  const end = raw.lastIndexOf("}");
  if (start < 0 || end <= start) throw new Error("Model did not return JSON");
  return JSON.parse(raw.slice(start, end + 1));
}

function fallbackTriad(input: CounselInput): TriadResult {
  const tmpl = TEMPLATES.find((t) => t.id === input.templateId) ?? TEMPLATES[0];
  const partyA = input.parties[0]?.name ?? "Party A";
  const partyB = input.parties[1]?.name ?? "Party B";
  let body = tmpl.skeleton
    .replaceAll("{{partyA}}", partyA)
    .replaceAll("{{partyB}}", partyB)
    .replaceAll("{{county}}", input.county || "New York")
    .replaceAll("{{effectiveDate}}", new Date().toLocaleDateString("en-US"))
    .replaceAll("{{services}}", input.objectives || "the services described by the parties")
    .replaceAll("{{fees}}", "[AMOUNT]")
    .replaceAll("{{term}}", "one (1) year")
    .replaceAll("{{purpose}}", input.objectives || "a potential transaction")
    .replaceAll("{{children}}", "[CHILD NAMES AND DATES OF BIRTH]")
    .replaceAll("{{parentingSchedule}}", "2-2-3 rotating, exchanges at school")
    .replaceAll("{{miles}}", "50")
    .replaceAll("{{proRata}}", "in proportion to CSSA income")
    .replaceAll("{{indexNo}}", "[INDEX]")
    .replaceAll("{{dispute}}", input.facts.slice(0, 240) || "the disputed claims")
    .replaceAll("{{paymentMethod}}", "wire")
    .replaceAll("{{premises}}", "[PREMISES ADDRESS]")
    .replaceAll("{{management}}", "member-managed")
    .replaceAll("{{vote}}", "Majority-in-Interest")
    .replaceAll(
      "{{signatureBlock}}",
      `\n${partyA}\nBy: ________________________    Date: __________\n\n${partyB}\nBy: ________________________    Date: __________\n`,
    );
  const authorities = [
    ...tmpl.requiredStatutes.map((id) => STATUTES.find((s) => s.id === id)?.title ?? id),
    ...tmpl.requiredCases.map((id) => CASES.find((c) => c.id === id)?.bluebook ?? id),
  ];
  return {
    planner: {
      issues: [
        `Instrument type: ${tmpl.name}`,
        `Forum: ${input.county || "New York"} County, State of New York`,
        "Human attorney review required before execution or filing.",
      ],
      authorities,
      framework:
        "Offline template fill — live counsel is unavailable. Authorities below are from the verified New York bank only.",
      risks: [
        "AI features were unavailable, so this is a skeleton, not a negotiated instrument.",
        "Fill every bracketed placeholder before circulation.",
      ],
    },
    draft: { title: tmpl.name, body },
    critic: {
      score: 62,
      flaws: [
        "Skeleton fill only — no live adversary pass.",
        "Placeholders remain. An incomplete instrument is not binding.",
      ],
      missingStatutes: [],
      unverifiedCitations: [],
      rewriteDirectives: ["Enable counsel AI and re-run the triad for a full red-team pass."],
      memo: "Critic score capped because the language model was offline. Do not treat this as airtight.",
    },
  };
}

function parseTriad(raw: unknown): TriadResult {
  const r = raw as TriadResult;
  if (!r?.draft?.body || !r?.critic || !r?.planner) {
    throw new Error("Incomplete triad payload");
  }
  return {
    planner: {
      issues: r.planner.issues ?? [],
      authorities: r.planner.authorities ?? [],
      framework: r.planner.framework ?? "",
      risks: r.planner.risks ?? [],
    },
    draft: {
      title: r.draft.title ?? "Draft",
      body: r.draft.body,
    },
    critic: {
      score: Math.max(0, Math.min(100, Number(r.critic.score) || 0)),
      flaws: r.critic.flaws ?? [],
      missingStatutes: r.critic.missingStatutes ?? [],
      unverifiedCitations: r.critic.unverifiedCitations ?? [],
      rewriteDirectives: r.critic.rewriteDirectives ?? [],
      memo: r.critic.memo ?? "",
    },
  };
}

async function grokJson(system: string, user: string): Promise<string> {
  const apiKey = process.env.XAI_API_KEY;
  if (!apiKey) throw new Error("NO_AI");
  const res = await fetch("https://api.x.ai/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: "grok-4.5",
      temperature: 0.2,
      max_tokens: 3200,
      messages: [
        { role: "system", content: system },
        { role: "user", content: user },
      ],
    }),
  });
  if (!res.ok) {
    const t = await res.text().catch(() => "");
    throw new Error(`xAI API error ${res.status} ${t.slice(0, 200)}`);
  }
  const body = (await res.json()) as {
    choices: { message: { content: string } }[];
  };
  return body.choices[0]?.message.content ?? "";
}

function systemPrompt(): string {
  return `${PERSONA}

${skillsPromptBlock()}

${corpusPromptBlock()}

OUTPUT CONTRACT
Return ONLY a JSON object with this shape:
{
  "planner": {
    "issues": string[],
    "authorities": string[],
    "framework": string,
    "risks": string[]
  },
  "draft": {
    "title": string,
    "body": string
  },
  "critic": {
    "score": number,
    "flaws": string[],
    "missingStatutes": string[],
    "unverifiedCitations": string[],
    "rewriteDirectives": string[],
    "memo": string
  }
}
The draft.body is the full instrument in plain text, suitable for execution after human review. Use NY citation form. Score < 85 if any citation is unverified or a required statute is missing.`;
}

export const runTriad = createServerFn({ method: "POST" })
  .validator((input: CounselInput) => input)
  .handler(async ({ data }) => {
    const tmpl = TEMPLATES.find((t) => t.id === data.templateId);
    const user = [
      `MODE: ${data.mode}`,
      `PRACTICE: ${data.practice}`,
      `TEMPLATE: ${tmpl ? `${tmpl.name} (${tmpl.id})` : "none — choose structure from practice"}`,
      tmpl ? `SKELETON (adapt, do not omit required articles):\n${tmpl.skeleton}` : "",
      `CAPTION: ${data.caption}`,
      `COUNTY: ${data.county}`,
      `PARTIES:\n${data.parties.map((p) => `- ${p.role}: ${p.name}`).join("\n")}`,
      `FACTS:\n${data.facts}`,
      `OBJECTIVES:\n${data.objectives}`,
      data.liveAuthorities ? `LIVE AUTHORITIES:\n${data.liveAuthorities}` : "",
      data.priorDraft ? `PRIOR DRAFT TO REWRITE:\n${data.priorDraft}` : "",
      data.criticNotes?.length ? `CRITIC NOTES TO SATISFY:\n${data.criticNotes.join("\n")}` : "",
      data.extra ? `ADDITIONAL INSTRUCTIONS:\n${data.extra}` : "",
    ]
      .filter(Boolean)
      .join("\n\n");

    try {
      const text = await grokJson(systemPrompt(), user);
      const parsed = parseTriad(extractJson(text));
      return { ok: true as const, result: parsed, offline: false };
    } catch (err) {
      const message = err instanceof Error ? err.message : "unknown";
      if (message === "NO_AI" || message.startsWith("xAI API error")) {
        return {
          ok: true as const,
          result: fallbackTriad(data),
          offline: true,
          error: message === "NO_AI" ? "Counsel AI is not configured in this environment." : message,
        };
      }
      return {
        ok: false as const,
        error: message,
        result: fallbackTriad(data),
        offline: true,
      };
    }
  });

export const speakCounsel = createServerFn({ method: "POST" })
  .validator((input: { text: string }) => input)
  .handler(async ({ data }) => {
    const apiKey = process.env.XAI_API_KEY;
    if (!apiKey) return { ok: false as const, error: "Voice is unavailable." };
    const clipped = data.text.slice(0, 1200);
    const res = await fetch("https://api.x.ai/v1/tts", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${apiKey}`,
      },
      body: JSON.stringify({ text: clipped, voice_id: "eve" }),
    });
    if (!res.ok) return { ok: false as const, error: `TTS ${res.status}` };
    const buf = Buffer.from(await res.arrayBuffer());
    return { ok: true as const, audio: buf.toString("base64"), mime: "audio/mpeg" };
  });
