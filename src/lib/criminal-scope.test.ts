import assert from "node:assert/strict";
import { describe, it } from "node:test";
import {
  CRIMINAL_CASES,
  CRIMINAL_STATUTES,
  corpusPromptBlock,
  searchCriminalCenteredCorpus,
} from "./corpus.ts";
import {
  PRIMARY_PRACTICE,
  isPrimaryCriminalPractice,
  requireCriminalCenteredScope,
} from "./criminal-scope.ts";
import { CRIMINAL_TEMPLATES } from "./templates.ts";
import type { PracticeArea } from "./types.ts";

describe("criminal-centered scope", () => {
  it("keeps criminal as the primary product practice", () => {
    assert.equal(PRIMARY_PRACTICE, "criminal");
    assert.equal(isPrimaryCriminalPractice("criminal"), true);
    assert.equal(isPrimaryCriminalPractice("civil"), false);
    assert.doesNotThrow(() => requireCriminalCenteredScope("criminal"));
  });

  it("allows every modeled ancillary practice area with an explicit criminal nexus", () => {
    const ancillary: PracticeArea[] = [
      "civil",
      "family",
      "contracts",
      "real-property",
      "employment",
    ];

    for (const practice of ancillary) {
      assert.doesNotThrow(() => requireCriminalCenteredScope(practice, true));
    }
  });

  it("does not promote standalone non-criminal practice", () => {
    const ancillary: PracticeArea[] = [
      "civil",
      "family",
      "contracts",
      "real-property",
      "employment",
    ];

    for (const practice of ancillary) {
      assert.throws(
        () => requireCriminalCenteredScope(practice),
        /criminal-centered.*materially intersects a criminal matter/i,
      );
    }
  });

  it("keeps primary templates and base authority criminal", () => {
    assert.ok(CRIMINAL_TEMPLATES.length > 0);
    assert.ok(CRIMINAL_TEMPLATES.every((item) => item.practice === "criminal"));
    assert.ok(CRIMINAL_STATUTES.length > 0);
    assert.ok(CRIMINAL_CASES.length > 0);
  });

  it("includes CPLR habeas authority when the criminal context calls for it", () => {
    const prompt = corpusPromptBlock("criminal detention habeas corpus CPLR Article 70");
    assert.match(prompt, /Criminal Procedure Law|Penal Law/);
    assert.match(prompt, /Civil Practice Law and Rules § Article 70/);
    assert.match(prompt, /Habeas corpus/);
  });

  it("finds matching collateral authority without making it the base corpus", () => {
    const result = searchCriminalCenteredCorpus("CPLR habeas Article 70");
    assert.ok(result.statutes.some((item) => item.id === "cplr-art-70"));
  });
});
