import { RIGHTS_PACK, type EncounterMode } from "./domain.js";
import { readCases, readPrivacy, writePrivacy } from "./storage.js";
import { createMatter, matterSummary } from "./caseguardian.js";

const appNode = document.querySelector<HTMLElement>("#app");
if (!appNode) throw new Error("#app missing");
const app: HTMLElement = appNode;

function renderHome(): void {
  const privacy = readPrivacy();
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
          ${Object.values(RIGHTS_PACK).map(card => `<button class="card" data-mode="${card.mode}"><strong>${card.title}</strong><span>Open rights guide</span></button>`).join("")}
        </div>
      </section>
      <section aria-labelledby="case-heading">
        <h2 id="case-heading">Case Guardian</h2>
        <div id="case-list">${readCases().map(matter => `<article class="card"><strong>${matter.title}</strong><span>${matterSummary(matter)}</span></article>`).join("") || "<p>No local case created yet.</p>"}</div>
        <button id="create-case" class="card"><strong>Create local case</strong><span>Stored on this device by default</span></button>
      </section>
      <section class="privacy" aria-labelledby="privacy-heading">
        <h2 id="privacy-heading">Privacy</h2>
        <label><input id="diagnostics" type="checkbox" ${privacy.diagnostics ? "checked" : ""}> Share privacy-safe diagnostics</label>
        <p>Legal questions, case documents, conversations, evidence and precise location are excluded from ordinary diagnostics.</p>
      </section>
    </main>`;

  app.querySelectorAll<HTMLButtonElement>("[data-mode]").forEach(button => {
    button.addEventListener("click", () => renderRights(button.dataset.mode as EncounterMode));
  });
  app.querySelector<HTMLButtonElement>("#create-case")?.addEventListener("click", () => {
    createMatter("My case");
    renderHome();
  });
  app.querySelector<HTMLInputElement>("#diagnostics")?.addEventListener("change", event => {
    const checked = (event.currentTarget as HTMLInputElement).checked;
    writePrivacy({ ...readPrivacy(), diagnostics: checked });
  });
}

function renderRights(mode: EncounterMode): void {
  const card = RIGHTS_PACK[mode];
  app.innerHTML = `
    <main class="rights">
      <button id="back" class="back">← Back</button>
      <p class="eyebrow">Live rights mode</p>
      <h1>${card.title}</h1>
      <section><h2>Do now</h2><ol>${card.actions.map(item => `<li>${item}</li>`).join("")}</ol></section>
      <section class="warning"><h2>Safety</h2><ul>${card.never.map(item => `<li>${item}</li>`).join("")}</ul></section>
      <p class="source-note">Offline rights pack. Verify current jurisdiction-specific law when connectivity is available.</p>
    </main>`;
  app.querySelector<HTMLButtonElement>("#back")?.addEventListener("click", renderHome);
}

renderHome();

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => navigator.serviceWorker.register("/sw.js").catch(() => undefined));
}
