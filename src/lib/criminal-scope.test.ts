import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { CRIMINAL_CASES, CRIMINAL_STATUTES, corpusPromptBlock } from "./corpus.ts";
import { ACTIVE_PRACTICE, isCriminalPractice, requireCriminalPractice } from "./criminal-scope.ts";
import { CRIMINAL_TEMPLATES } from "./templates.ts";

describe("criminal-only scope", () => {
  it("accepts only criminal practice", () => {
    assert.equal(ACTIVE_PRACTICE, "criminal");
    assert.equal(requireCriminalPractice("criminal"), "criminal");
    assert.equal(isCriminalPractice("criminal"), true);
    assert.equal(isCriminalPractice("civil"), false);
    assert.throws(() => requireCriminalPractice("family"), /restricted to New York criminal-law matters/);
  });

  it("exposes only criminal templates and authority records", () => {
    assert.ok(CRIMINAL_TEMPLATES.length > 0);
    assert.ok(CRIMINAL_TEMPLATES.every((item) => item.practice === "criminal"));
    assert.ok(CRIMINAL_STATUTES.length > 0);
    assert.ok(CRIMINAL_STATUTES.every((item) => item.practice.includes("criminal")));
    assert.ok(CRIMINAL_CASES.length > 0);
    assert.ok(CRIMINAL_CASES.every((item) => item.practice.includes("criminal")));
  });

  it("builds the model authority prompt from criminal authorities only", () => {
    const prompt = corpusPromptBlock();
    assert.match(prompt, /Criminal Procedure Law|Penal Law/);
    assert.doesNotMatch(prompt, /Domestic Relations Law|General Obligations Law/);
  });
});
