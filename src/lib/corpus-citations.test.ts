import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { corpusCitationsForTemplate } from "./corpus.ts";
import { TEMPLATES } from "./templates.ts";

describe("corpusCitationsForTemplate", () => {
  it("returns only resolved, verified corpus citations for every template", () => {
    for (const tmpl of TEMPLATES) {
      const citations = corpusCitationsForTemplate(tmpl);
      const expected = tmpl.requiredStatutes.length + tmpl.requiredCases.length;
      assert.equal(
        citations.length,
        expected,
        `${tmpl.id}: expected ${expected} citations, got ${citations.length}`,
      );
      for (const c of citations) {
        assert.equal(c.verified, true, `${tmpl.id}:${c.id} must be verified`);
        assert.equal(c.source, "corpus", `${tmpl.id}:${c.id} must come from the corpus`);
        assert.ok(c.url.startsWith("https://"), `${tmpl.id}:${c.id} must carry a source URL`);
        assert.ok(c.bluebook.length > 0, `${tmpl.id}:${c.id} must have a bluebook line`);
      }
    }
  });

  it("orders statutes before cases, matching requiredStatutes then requiredCases", () => {
    for (const tmpl of TEMPLATES) {
      const citations = corpusCitationsForTemplate(tmpl);
      const statuteIds = citations.filter((c) => c.kind === "statute").map((c) => c.id);
      const caseIds = citations.filter((c) => c.kind === "case").map((c) => c.id);
      assert.deepEqual(statuteIds, tmpl.requiredStatutes, `${tmpl.id}: statute order mismatch`);
      assert.deepEqual(caseIds, tmpl.requiredCases, `${tmpl.id}: case order mismatch`);
    }
  });

  it("statute citations point at nysenate.gov official pages", () => {
    for (const tmpl of TEMPLATES) {
      for (const c of corpusCitationsForTemplate(tmpl)) {
        if (c.kind === "statute") {
          assert.ok(
            c.url.includes("nysenate.gov"),
            `${tmpl.id}:${c.id} statute URL must be the official NY Senate page`,
          );
        }
      }
    }
  });
});
