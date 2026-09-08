import { cp, mkdir, rm } from "node:fs/promises";
import { join } from "node:path";

const root = new URL("../", import.meta.url).pathname;
const out = join(root, "public-dist");

await rm(out, { recursive: true, force: true });
await mkdir(out, { recursive: true });
for (const name of ["index.html", "styles.css", "manifest.webmanifest", "sw.js"]) {
  await cp(join(root, name), join(out, name));
}
await cp(join(root, "dist"), join(out, "dist"), { recursive: true });
