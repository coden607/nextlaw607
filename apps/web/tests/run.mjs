import { run } from "./harness.mjs";
await import("./domain.test.mjs");
await import("./cloudflare.test.mjs");
await import("./frontend-quality.test.mjs");
await run();
