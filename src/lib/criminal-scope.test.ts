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

describe("criminal-centered scope", () => {
  it("keeps criminal as the primary product practice", () => {
    assert.equal(PRIMARY_PRACTICE, "criminal");
    assert.equal(isPrimaryCriminalPractice("criminal"), true);
    assert.equal(isPrimaryCriminalPractice("civil"), false);
    assert.doesNotThrow(() => requireCriminalCenteredScope("criminal"));
  });

  it("allows intersecting law only with an explicit criminal nexus", () => {
    assert.doesNotThrow(() => requireCriminalCenteredScope("civil", true));
    assert.throws(
      () => requireCriminalCenteredScope("family"),
      /criminal-centered/,
    );
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
