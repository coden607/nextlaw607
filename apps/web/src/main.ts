import { PROCEDURE_STAGES, RIGHTS_PACK, type CaseGuardianMatter, type EncounterMode, type ProcedureStage } from "./domain.js";
import { clearLocalData, exportLocalData, importLocalData, readCases, readPrivacy, writePrivacy } from "./storage.js";
import { addMatterIssue, createMatter, matterSummary, setMatterStage, setNextAppearance, updateMatter } from "./caseguardian.js";
import { escapeHtml } from "./html.js";
import { requestCaseNextActions } from "./api.js";

const appNode = document.querySelector<HTMLElement>("#app");
if (!appNode) throw new Error("#app missing");
const app: HTMLElement = appNode;

const stageLabel = (stage: ProcedureStage): string => stage.replaceAll("_", " ").replace(/\b\w/g, char => char.toUpperCase());

function downloadLocalData(): void {
  const snapshot = exportLocalData();
  const blob = new Blob([`${JSON.stringify(snapshot, null, 2)}\n`], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `nextlaw607-local-data-${new Date().toISOString().slice(0, 10)}.json`;
  document.body.append(anchor);
  anchor.click();
  anchor.remove();
  setTimeout(() => URL.revokeObjectURL(url), 0);
}

function deleteLocalData(): void {
  const confirmed = window.confirm("Delete all NextLaw607 case and privacy data stored on this device? This cannot be undone.");
  if (!confirmed) return;
  clearLocalData();
  renderHome();
}

async function restoreLocalData(file: File): Promise<void> {
  const status = app.querySelector<HTMLElement>("#data-status");
  try {
    const text = await file.text();
    const snapshot = JSON.parse(text) as unknown;
    importLocalData(snapshot);
    renderHome();
    const restoredStatus = app.querySelector<HTMLElement>("#data-status");
    if (restoredStatus) restoredStatus.textContent = "Local data backup restored on this device.";
  } catch {
    if (status) status.textContent = "Backup could not be restored. Existing local data was not replaced.";
  }
}

function renderHome(): void {
  const privacy = readPrivacy();
  const matters = readCases();
  app.innerHTML = `
    <header class="hero">
      <p class="eyebrow">NextLaw607</p>
      <h1>Protect your rights. Know the next lawful step.</h1>
      <p>Live rights guidance and case organization. Important legal conclusions must be source-verified; this app is not a substitute for a licensed attorney.</p>
    </header>
    <main>
      <section aria-labelledby="live-heading">
        <h2 id="live-heading">Live encounter</h2>
        <div class="grid">
          ${Object.values(RIGHTS_PACK).map(card => `<button class="card" data-mode="${card.mode}"><strong>${escapeHtml(card.title)}</strong><span>Open rights guide</span></button>`).join("")}
        </div>
      </section>
      <section aria-labelledby="case-heading">
        <h2 id="case-heading">Case Guardian</h2>
        <div id="case-list" class="grid">${matters.map(matter => `<button class="card" data-matter="${escapeHtml(matter.id)}"><strong>${escapeHtml(matter.title)}</strong><span>${escapeHtml(matterSummary(matter))}</span></button>`).join("") || "<p>No local case created yet.</p>"}</div>
        <button id="create-case" class="card"><strong>Create local case</strong><span>Stored on this device by default</span></button>
      </section>
      <section class="privacy" aria-labelledby="privacy-heading">
        <h2 id="privacy-heading">Privacy Center</h2>
        <p><strong>Local/guest mode.</strong> Your Case Guardian data stays on this device unless you explicitly export or enable a future sync feature.</p>
        <label><input id="diagnostics" type="checkbox" ${privacy.diagnostics ? "checked" : ""}> Share privacy-safe diagnostics</label>
        <p>Legal questions, case documents, conversations, evidence and precise location are excluded from ordinary diagnostics.</p>
        <div class="row wrap privacy-actions">
          <button id="export-data" type="button">Export my local data</button>
          <button id="delete-data" type="button">Delete local data</button>
        </div>
        <label for="import-data">Restore a NextLaw607 JSON backup</label>
        <input id="import-data" type="file" accept="application/json,.json">
        <p id="data-status" class="source-note" role="status" aria-live="polite">Export creates a JSON backup you control. Restore validates the backup before replacing NextLaw607 local records.</p>
      </section>
    </main>`;

  app.querySelectorAll<HTMLButtonElement>("[data-mode]").forEach(button => {
    button.addEventListener("click", () => renderRights(button.dataset.mode as EncounterMode));
  });
  app.querySelectorAll<HTMLButtonElement>("[data-matter]").forEach(button => {
    button.addEventListener("click", () => renderMatter(button.dataset.matter || ""));
  });
  app.querySelector<HTMLButtonElement>("#create-case")?.addEventListener("click", () => {
    const matter = createMatter("My case");
    renderMatter(matter.id);
  });
  app.querySelector<HTMLInputElement>("#diagnostics")?.addEventListener("change", event => {
    const checked = (event.currentTarget as HTMLInputElement).checked;
    writePrivacy({ ...readPrivacy(), diagnostics: checked });
  });
  app.querySelector<HTMLButtonElement>("#export-data")?.addEventListener("click", downloadLocalData);
  app.querySelector<HTMLButtonElement>("#delete-data")?.addEventListener("click", deleteLocalData);
  app.querySelector<HTMLInputElement>("#import-data")?.addEventListener("change", event => {
    const input = event.currentTarget as HTMLInputElement;
    const file = input.files?.[0];
    if (file) void restoreLocalData(file);
  });
}

function renderRights(mode: EncounterMode): void {
  const card = RIGHTS_PACK[mode];
  app.innerHTML = `
    <main class="rights">
      <button id="back" class="back">← Back</button>
      <p class="eyebrow">Live rights mode</p>
      <h1>${escapeHtml(card.title)}</h1>
      <section><h2>Do now</h2><ol>${card.actions.map(item => `<li>${escapeHtml(item)}</li>`).join("")}</ol></section>
      <section class="warning"><h2>Safety</h2><ul>${card.never.map(item => `<li>${escapeHtml(item)}</li>`).join("")}</ul></section>
      <p class="source-note">Offline rights pack. Verify current jurisdiction-specific law when connectivity is available.</p>
    </main>`;
  app.querySelector<HTMLButtonElement>("#back")?.addEventListener("click", renderHome);
}

function findMatter(matterId: string): CaseGuardianMatter | undefined {
  return readCases().find(matter => matter.id === matterId);
}

function renderMatter(matterId: string): void {
  const matter = findMatter(matterId);
  if (!matter) { renderHome(); return; }
  const stage = matter.stage || "investigation";
  app.innerHTML = `
    <main class="case-editor">
      <button id="back" class="back">← Cases</button>
      <p class="eyebrow">Case Guardian · Local first</p>
      <h1>${escapeHtml(matter.title)}</h1>
      <p class="source-note">This organizer does not calculate legal deadlines. Enter dates from your actual court papers or verified counsel guidance.</p>
      <section>
        <h2>Case posture</h2>
        <label for="stage">Procedural stage</label>
        <select id="stage">${PROCEDURE_STAGES.map(item => `<option value="${item}" ${item === stage ? "selected" : ""}>${escapeHtml(stageLabel(item))}</option>`).join("")}</select>
        <label for="appearance">Next appearance from your paperwork</label>
        <input id="appearance" type="datetime-local" value="${escapeHtml(matter.nextAppearance || "")}">
      </section>
      <section>
        <h2>Issues to preserve</h2>
        <ul>${matter.issues.map(issue => `<li>${escapeHtml(issue)}</li>`).join("") || "<li>No issues entered yet.</li>"}</ul>
        <form id="issue-form">
          <label for="issue">Add an issue or fact to review</label>
          <div class="row wrap"><input id="issue" autocomplete="off" placeholder="Example: Search consent disputed"><button type="submit">Add</button></div>
        </form>
      </section>
      <section>
        <div class="row between wrap"><h2>Next lawful steps</h2><button id="refresh-guidance" type="button">Refresh guidance</button></div>
        <ul id="next-actions">${matter.nextActions.map(item => `<li>${escapeHtml(item)}</li>`).join("")}</ul>
        <p id="guidance-status" class="source-note" role="status" aria-live="polite">Local guidance shown. Remote/current-law verification is separate.</p>
      </section>
    </main>`;

  app.querySelector<HTMLButtonElement>("#back")?.addEventListener("click", renderHome);
  app.querySelector<HTMLSelectElement>("#stage")?.addEventListener("change", event => {
    setMatterStage(matter, (event.currentTarget as HTMLSelectElement).value as ProcedureStage);
    renderMatter(matter.id);
  });
  app.querySelector<HTMLInputElement>("#appearance")?.addEventListener("change", event => {
    setNextAppearance(matter, (event.currentTarget as HTMLInputElement).value);
    renderMatter(matter.id);
  });
  app.querySelector<HTMLFormElement>("#issue-form")?.addEventListener("submit", event => {
    event.preventDefault();
    const input = app.querySelector<HTMLInputElement>("#issue");
    if (input) addMatterIssue(matter, input.value);
    renderMatter(matter.id);
  });
  app.querySelector<HTMLButtonElement>("#refresh-guidance")?.addEventListener("click", () => refreshCaseGuidance(matter.id));
}

async function refreshCaseGuidance(matterId: string): Promise<void> {
  const matter = findMatter(matterId);
  const status = app.querySelector<HTMLElement>("#guidance-status");
  if (!matter) return;
  if (status) status.textContent = "Refreshing procedural guidance…";
  try {
    const response = await requestCaseNextActions({
      matterId: matter.id,
      jurisdiction: matter.jurisdiction,
      stage: matter.stage || "investigation",
      nextAppearance: matter.nextAppearance,
      unresolvedIssues: matter.issues,
    });
    updateMatter({ ...matter, nextActions: response.next_actions });
    renderMatter(matter.id);
    const nextStatus = app.querySelector<HTMLElement>("#guidance-status");
    if (nextStatus) nextStatus.textContent = response.deadline_source_verified
      ? "Guidance refreshed with verified deadline source metadata."
      : "Guidance refreshed. No legal deadline was automatically asserted.";
  } catch {
    if (status) status.textContent = "Guidance could not refresh. Your local case data is unchanged and remains available offline.";
  }
}

renderHome();

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => navigator.serviceWorker.register("/sw.js").catch(() => undefined));
}
