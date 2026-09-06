import { writeFile } from "node:fs/promises";
import process from "node:process";
import { chromium } from "playwright";
import AxeBuilder from "@axe-core/playwright";

const baseURL = process.env.NEXTLAW_BROWSER_URL || "http://127.0.0.1:4173/";
const revision = process.env.GITHUB_SHA || process.env.NEXTLAW_REVISION;
if (!revision) throw new Error("browser evidence requires an exact revision");

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext();
const page = await context.newPage();
await page.addInitScript(() => {
  window.__nextlawVitals = { lcp_ms: 0, cls: 0, inp_ms: 0 };
  new PerformanceObserver(list => {
    for (const entry of list.getEntries()) window.__nextlawVitals.lcp_ms = Math.max(window.__nextlawVitals.lcp_ms, entry.startTime || 0);
  }).observe({ type: "largest-contentful-paint", buffered: true });
  new PerformanceObserver(list => {
    for (const entry of list.getEntries()) {
      if (!entry.hadRecentInput) window.__nextlawVitals.cls += entry.value || 0;
    }
  }).observe({ type: "layout-shift", buffered: true });
  try {
    new PerformanceObserver(list => {
      for (const entry of list.getEntries()) window.__nextlawVitals.inp_ms = Math.max(window.__nextlawVitals.inp_ms, entry.duration || 0);
    }).observe({ type: "event", buffered: true, durationThreshold: 0 });
  } catch {}
});

const consoleErrors = [];
const requestFailures = [];
page.on("console", message => { if (message.type() === "error") consoleErrors.push(message.text()); });
page.on("requestfailed", request => requestFailures.push(`${request.method()} ${request.url()} ${request.failure()?.errorText || "failed"}`));

await page.goto(baseURL, { waitUntil: "networkidle" });
await page.locator("button[data-mode]").first().click();
await page.locator("#back").click();
await page.waitForTimeout(250);

const axe = await new AxeBuilder({ page }).analyze();
const seriousA11y = axe.violations.filter(v => ["serious", "critical"].includes(v.impact));

const ready = await page.evaluate(async () => {
  if (!("serviceWorker" in navigator)) return false;
  await navigator.serviceWorker.ready;
  return Boolean(navigator.serviceWorker.controller || (await navigator.serviceWorker.getRegistration()));
});
if (!ready) throw new Error("service worker did not become ready");

await context.setOffline(true);
let offlinePassed = true;
try {
  await page.reload({ waitUntil: "domcontentloaded", timeout: 15000 });
  await page.locator("button[data-mode]").first().waitFor({ state: "visible" });
} catch {
  offlinePassed = false;
}
await context.setOffline(false);

const performance = await page.evaluate(() => ({ ...window.__nextlawVitals }));
for (const key of ["lcp_ms", "cls", "inp_ms"]) {
  if (!Number.isFinite(performance[key])) performance[key] = 0;
}

const evidence = {
  revision,
  captured_at: new Date().toISOString(),
  tool: "playwright+axe-core+performance-observer",
  e2e_passed: consoleErrors.length === 0 && requestFailures.length === 0,
  accessibility_passed: seriousA11y.length === 0,
  pwa_passed: ready && offlinePassed,
  performance,
  details: {
    accessibility_violations: seriousA11y.map(v => ({ id: v.id, impact: v.impact, help: v.help })),
    console_errors: consoleErrors,
    request_failures: requestFailures,
    offline_reload_passed: offlinePassed,
  },
};
await writeFile(new URL("../../../.continuity/browser-evidence.json", import.meta.url), `${JSON.stringify(evidence, null, 2)}\n`, "utf8");
await browser.close();

if (!evidence.e2e_passed || !evidence.accessibility_passed || !evidence.pwa_passed) process.exitCode = 1;
