#!/usr/bin/env node
/**
 * Fail loudly when the running dev server and the next build disagree about
 * `VITE_AUTH_ENABLED`.
 *
 * `npm run dev`, `npm run build` and `npm run preview` all get the flag from
 * `scripts/with-app-env.mjs`, so they agree by construction — but a dev server
 * started outside npm (`npx vite dev`) does not, and the result is sign-in
 * visible in the live preview and absent from the built output, or the reverse.
 *
 * The two sides compared:
 *  - **dev**: what the running server resolved, read from the `/__app-env`
 *    endpoint the template's dev-only `appEnvPlugin` serves.
 *  - **build**: what the wrapper hands `vite build` / `vite preview`.
 *
 * The built bundle is not read: Vite inlines the flag and the minifier folds
 * `"false" !== "false"` away, so the built client JS carries no marker to
 * compare against unless the app is made to emit one.
 *
 * `scripts/browser-smoke.mjs` runs the comparison on every smoke; run it
 * standalone with `npm run check:auth` (exit 0 agree, 1 diverged,
 * 2 could not observe). When no dev server answers the probe, the command
 * boots one, waits for `/__app-env`, and tears it down afterwards — so the
 * gate also works where nothing is listening yet (a fresh CI job). Callers
 * comparing the flag should use `compareAuthInvariant()` rather than
 * re-deriving it.
 */
import { APP_ENV_ROUTE } from "./app-env-plugin.mjs";
import { isMainModule, mergeAppEnv, projectRoot, readAppEnv } from "./with-app-env.mjs";

const DEFAULT_DEV_URL = "http://127.0.0.1:8080";

/** The predicate `src/lib/auth/{client,server}.ts` apply to the flag. */
export function authEnabledFromEnvValue(value) {
  return value !== "false";
}

/**
 * Compare the two resolved values. `null` means "could not observe" — reported
 * as indeterminate rather than as agreement.
 */
export function compareAuthInvariant({ devAuthEnabled, buildAuthEnabled }) {
  const label = (value) => (value ? "on" : "off");
  if (devAuthEnabled === null || devAuthEnabled === undefined) {
    return {
      status: "indeterminate",
      message: "[auth-invariant] could not read the dev server's resolved VITE_AUTH_ENABLED",
    };
  }
  if (devAuthEnabled === buildAuthEnabled) {
    return {
      status: "ok",
      message: `[auth-invariant] dev and build agree: sign-in ${label(devAuthEnabled)}`,
    };
  }
  return {
    status: "diverged",
    message:
      `[auth-invariant] dev server has sign-in ${label(devAuthEnabled)} but the next ` +
      `build has it ${label(buildAuthEnabled)}. Start the app with \`npm run dev\` — ` +
      "invoking vite directly skips scripts/with-app-env.mjs, so the dev server and " +
      "the built output resolve .grok/app-env.json differently.",
  };
}

/**
 * Ask the dev server which env it resolved. Anything but a JSON object from
 * `/__app-env` (no server, a built-output preview, an older workspace without
 * the plugin) is "could not observe".
 */
export async function probeDevAuthEnabled(devUrl, fetchImpl = fetch) {
  let env;
  try {
    const response = await fetchImpl(new URL(APP_ENV_ROUTE, devUrl).href);
    if (!response.ok) return null;
    env = JSON.parse(await response.text());
  } catch {
    return null;
  }
  if (env === null || typeof env !== "object") return null;
  return authEnabledFromEnvValue(env.VITE_AUTH_ENABLED);
}

/** The smoke-verdict warnings for a comparison: a real divergence only. */
export function authInvariantWarnings(result) {
  return result.status === "diverged" ? [result.message] : [];
}

/** What `vite build` / `vite preview` will resolve, via the same wrapper. */
export function buildAuthEnabled(root = projectRoot(), processEnv = process.env) {
  const env = mergeAppEnv(readAppEnv(root), processEnv);
  return authEnabledFromEnvValue(env.VITE_AUTH_ENABLED);
}

/**
 * Probe the dev server, booting a short-lived one when nothing answers. CI
 * runs this command on a fresh checkout where no server is listening; the
 * gate's whole point is comparing resolutions, so it brings its own dev
 * server up rather than declaring the run unobservable.
 */
async function probeWithFallbackServer(devUrl) {
  const running = await probeDevAuthEnabled(devUrl);
  if (running !== null) return { devAuthEnabled: running, booted: false };

  const { spawn } = await import("node:child_process");
  const child = spawn("npm", ["run", "dev"], {
    cwd: projectRoot(),
    stdio: "ignore",
    // Own process group so the kill below takes the vite grandchild too.
    detached: process.platform !== "win32",
  });
  try {
    const deadline = Date.now() + 120_000;
    while (Date.now() < deadline && child.exitCode === null) {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      const observed = await probeDevAuthEnabled(devUrl);
      if (observed !== null) return { devAuthEnabled: observed, booted: true };
    }
    return { devAuthEnabled: null, booted: true };
  } finally {
    try {
      if (process.platform !== "win32") process.kill(-child.pid, "SIGTERM");
      else child.kill("SIGTERM");
    } catch {
      /* already gone */
    }
  }
}

async function main(argv) {
  const devUrlFlag = argv.indexOf("--dev-url");
  const devUrl = devUrlFlag === -1 ? DEFAULT_DEV_URL : argv[devUrlFlag + 1];
  const probe = await probeWithFallbackServer(devUrl);
  if (probe.booted) {
    console.error(
      probe.devAuthEnabled === null
        ? "[auth-invariant] started a dev server for the probe but it never became ready"
        : "[auth-invariant] no dev server was running; started one for the probe",
    );
  }
  const result = compareAuthInvariant({
    devAuthEnabled: probe.devAuthEnabled,
    buildAuthEnabled: buildAuthEnabled(),
  });
  if (result.status === "ok") {
    console.log(result.message);
    process.exit(0);
  }
  console.error(result.message);
  process.exit(result.status === "diverged" ? 1 : 2);
}

if (isMainModule(import.meta.url)) {
  await main(process.argv.slice(2));
}
