import { run } from "./harness.mjs";
await import("./domain.test.mjs");
await import("./cloudflare.test.mjs");
await run();
