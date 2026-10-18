import assert from "node:assert/strict";
import { describe, it } from "node:test";
import { ACTIVE_PRACTICE, isCriminalPractice, requireCriminalPractice } from "./criminal-scope.ts";

describe("criminal-only scope", () => {
  it("accepts only criminal practice", () => {
    assert.equal(ACTIVE_PRACTICE, "criminal");
    assert.equal(requireCriminalPractice("criminal"), "criminal");
    assert.equal(isCriminalPractice("criminal"), true);
    assert.equal(isCriminalPractice("civil"), false);
    assert.throws(() => requireCriminalPractice("family"), /restricted to New York criminal-law matters/);
  });
});
