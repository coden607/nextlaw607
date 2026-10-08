import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { TEMPLATES, templateById } from "./templates.ts";
import { PRACTICE_LABEL } from "./types.ts";
import { STATUTES, CASES, statuteById, caseById } from "./corpus.ts";

/** Mirrors the replacement map in ai.ts fallbackTriad. */
function renderSkeleton(skeleton: string, vars: Record<string, string>): string {
  let out = skeleton;
  for (const [k, v] of Object.entries(vars)) {
    out = out.replaceAll(`{{${k}}}`, v);
  }
  return out;
}

const TEST_VARS: Record<string, string> = {
  partyA: "Test Firm LLP",
  partyB: "John Doe",
  county: "Kings",
  effectiveDate: "2026-10-08",
  services: "full-scope representation",
  fees: "$25,000 flat fee",
  term: "through disposition",
  purpose: "defense of one count of PL 155.25",
  children: "[none]",
  parentingSchedule: "[n/a]",
  miles: "50",
  proRata: "50/50",
  indexNo: "12345/2026",
  dispute: "the defendant was stopped and searched on Main Street",
  paymentMethod: "wire",
  premises: "[n/a]",
  management: "[n/a]",
  vote: "[n/a]",
  signatureBlock: "\nTest Firm LLP\nBy: ____________________\n\nJohn Doe\nBy: ____________________\n",
};

const CRIMINAL_TEMPLATE_IDS = ["criminal-retention", "mitigation-memo", "suppression-brief"];

describe("criminal practice area union", () => {
  it("includes 'criminal' in PRACTICE_LABEL", () => {
    assert.ok("criminal" in PRACTICE_LABEL, "criminal must appear in PRACTICE_LABEL");
    assert.equal(PRACTICE_LABEL["criminal"], "Criminal — PL / CPL");
  });
});

describe("criminal instrument templates", () => {
  for (const id of CRIMINAL_TEMPLATE_IDS) {
    it(`template '${id}' exists with practice=criminal`, () => {
      const t = templateById(id);
      assert.ok(t, `template ${id} must exist`);
      assert.equal(t!.practice, "criminal");
      assert.ok(t!.skeleton.length > 400, `${id} skeleton must be substantive`);
      assert.ok(t!.summary.length > 20, `${id} must have a summary`);
    });
  }

  it("renders all three templates with zero leftover standard mustache placeholders", () => {
    for (const id of CRIMINAL_TEMPLATE_IDS) {
      const t = templateById(id)!;
      const rendered = renderSkeleton(t.skeleton, TEST_VARS);
      const leftover = rendered.match(/\{\{(partyA|partyB|county|effectiveDate|services|fees|term|purpose|children|parentingSchedule|miles|proRata|indexNo|dispute|paymentMethod|premises|management|vote|signatureBlock)\}\}/g);
      assert.equal(leftover, null, `${id} must render all standard placeholders (leftover: ${JSON.stringify(leftover)})`);
      assert.ok(!rendered.includes("{{partyA}}"), `${id} must replace partyA`);
      assert.ok(!rendered.includes("{{partyB}}"), `${id} must replace partyB`);
      assert.ok(!rendered.includes("{{county}}"), `${id} must replace county`);
      assert.ok(rendered.includes("Kings"), `${id} must contain replaced county value`);
    }
  });

  it("every requiredStatutes / requiredCases id resolves in the corpus", () => {
    for (const id of CRIMINAL_TEMPLATE_IDS) {
      const t = templateById(id)!;
      for (const sid of t.requiredStatutes) {
        assert.ok(statuteById(sid), `${id}.requiredStatutes references missing statute '${sid}'`);
      }
      for (const cid of t.requiredCases) {
        assert.ok(caseById(cid), `${id}.requiredCases references missing case '${cid}'`);
      }
    }
  });

  it("suppression-brief cites real landmark authorities", () => {
    const t = templateById("suppression-brief")!;
    const sk = t.skeleton;
    assert.match(sk, /Mapp v\. Ohio, 367 U\.S\. 643 \(1961\)/);
    assert.match(sk, /Terry v\. Ohio, 392 U\.S\. 1 \(1968\)/);
    assert.match(sk, /Miranda v\. Arizona, 384 U\.S\. 436 \(1966\)/);
    assert.match(sk, /Dunaway v\. New York, 442 U\.S\. 200 \(1979\)/);
    assert.match(sk, /Wong Sun v\. United States, 371 U\.S\. 471 \(1963\)/);
    assert.match(sk, /People v\. Huntley \(N\.Y\.\)/);
  });

  it("criminal-retention is a defense engagement letter with fee + investigation budget placeholders", () => {
    const t = templateById("criminal-retention")!;
    assert.match(t.skeleton, /SCOPE OF REPRESENTATION/);
    assert.match(t.skeleton, /\{\{fees\}\}/);
    assert.match(t.skeleton, /Investigation budget/);
    assert.match(t.skeleton, /CLIENT DUTIES/);
    assert.match(t.skeleton, /no promise or prediction about the outcome/i);
  });

  it("mitigation-memo has sentencing mitigation sections + YO placeholder", () => {
    const t = templateById("mitigation-memo")!;
    assert.match(t.skeleton, /MITIGATION/i);
    assert.match(t.skeleton, /restitution/i);
    assert.match(t.skeleton, /CPL ART\. 720/i);
  });
});

describe("criminal corpus expansion", () => {
  it("adds Penal Law articles 120, 125, 130, 140, 155, 160, 220, 265", () => {
    const expected = ["pl-120-00", "pl-125-00", "pl-130-00", "pl-140-00", "pl-155-00", "pl-160-00", "pl-220-00", "pl-265-00"];
    for (const id of expected) {
      assert.ok(statuteById(id), `corpus must include ${id}`);
      assert.ok(statuteById(id)!.practice.includes("criminal"), `${id} must be tagged criminal`);
    }
  });

  it("adds CPL 140.20, 710.20, 710.40, 450.10, 470.05", () => {
    for (const id of ["cpl-140-20", "cpl-710-20", "cpl-710-40", "cpl-450-10", "cpl-470-05"]) {
      assert.ok(statuteById(id), `corpus must include ${id}`);
    }
  });

  it("adds landmark SCOTUS + NY criminal cases", () => {
    const expected = ["mapp-ohio", "miranda-arizona", "terry-ohio", "dunaway-ny", "wong-sun", "brady-maryland", "batson-kentucky", "crawford-washington", "people-huntley"];
    for (const id of expected) {
      assert.ok(caseById(id), `corpus must include ${id}`);
      assert.equal(caseById(id)!.court, id === "people-huntley" ? "N.Y. Court of Appeals" : "U.S. Supreme Court");
    }
  });

  it("corpus has no duplicate ids", () => {
    const statuteIds = STATUTES.map((s) => s.id);
    const caseIds = CASES.map((c) => c.id);
    assert.equal(new Set(statuteIds).size, statuteIds.length, "statute ids must be unique");
    assert.equal(new Set(caseIds).size, caseIds.length, "case ids must be unique");
  });
});
