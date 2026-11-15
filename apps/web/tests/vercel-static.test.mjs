import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { test } from "node:test";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");

test("Vercel deploys the static public-dist output, not a Node entrypoint", () => {
  const config = JSON.parse(readFileSync(join(root, "vercel.json"), "utf8"));
  assert.equal(config.outputDirectory, "public-dist");
  assert.equal(config.buildCommand, "npm run build");
  assert.equal(config.framework, null);
  // A Node framework would treat dist/main.js (browser ESM) as a serverless
  // function and throw "Cannot use import statement outside a module".
  assert.notEqual(config.framework, "node");
});

test("the static build stages ESM main.js under public-dist/dist", async () => {
  const { spawnSync } = await import("node:child_process");
  const result = spawnSync("npm", ["run", "build"], { cwd: root, encoding: "utf8" });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  const main = readFileSync(join(root, "public-dist/dist/main.js"), "utf8");
  assert.match(main, /\bimport\b/);
  const html = readFileSync(join(root, "public-dist/index.html"), "utf8");
  assert.match(html, /<script type="module" src="\/dist\/main\.js">/);
});
