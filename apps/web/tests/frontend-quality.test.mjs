import fs from "node:fs";
import { assert, test } from "./harness.mjs";

const indexHtml = fs.readFileSync(new URL("../index.html", import.meta.url), "utf8");
const styles = fs.readFileSync(new URL("../styles.css", import.meta.url), "utf8");

test("frontend exposes a keyboard skip link to the main application", () => {
  assert.match(indexHtml, /class="skip-link"/);
  assert.match(indexHtml, /href="#app"/);
});

test("interactive controls preserve visible keyboard focus and touch target sizing", () => {
  assert.match(styles, /:focus-visible/);
  assert.match(styles, /min-height:\s*44px/);
});

test("motion honors reduced-motion preferences", () => {
  assert.match(styles, /prefers-reduced-motion:\s*reduce/);
  assert.match(styles, /animation-duration:\s*0\.01ms/);
});

test("premium visual treatment remains responsive and readable", () => {
  assert.match(styles, /color-scheme:\s*light dark/);
  assert.match(styles, /clamp\(/);
  assert.match(styles, /@media\s*\(max-width:\s*640px\)/);
});
