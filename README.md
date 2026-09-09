# NextLaw607

NextLaw607 is a privacy-first, rights-protection and criminal-procedure companion built on ContinuityOS. The user-facing application is TypeScript/PWA-first; Python is isolated behind a FastAPI/legal-processing boundary.

> NextLaw607 is not a law firm and does not create an attorney-client relationship. Important legal conclusions must be verified against current, jurisdiction-appropriate authority. The product must not advise resistance, flight, interference, deception, obstruction, evidence destruction, or witness tampering.

## Architecture

```text
TypeScript PWA
  ├─ Live rights mode
  ├─ Offline rights pack
  ├─ Case Guardian
  └─ Local-first privacy state
        ↓ HTTP API
FastAPI
  ├─ Live encounter safety engine
  ├─ Criminal procedure state
  ├─ Research/citation firewall
  ├─ CourtListener v4 candidate retrieval
  ├─ Temporal verified-rule registry
  └─ Legal adversarial evals
```

## iSH install

From the repository:

```sh
./scripts/ish-bootstrap.sh
```

This installs/reuses Python, pip, Node.js and npm, creates a virtual environment where supported, installs the Python package and web dev dependencies, then runs the verification suite.

## Run

```sh
. .venv/bin/activate 2>/dev/null || true
./scripts/dev.sh
```

Defaults:

- API: `http://127.0.0.1:8000`
- PWA: `http://127.0.0.1:4173`

## Test / verify

```sh
./scripts/verify.sh
```

The current local gate checks Python compilation/tests, strict TypeScript compilation/tests and JSON manifests. The final release gate additionally requires production-equivalent browser E2E, console/network inspection, privacy leakage checks, accessibility, PWA/offline behavior, performance analytics, security scans, and legal evals.

## npm-only web workflow

```sh
npm --prefix apps/web install
npm run build
npm run test:web
npm run dev
```

The web layer is intentionally TypeScript-first. Python remains behind the API boundary for legal processing, retrieval/RAG and other Python-ecosystem capabilities.

## CourtListener

The legal core uses CourtListener v4 search as a research-candidate source. A CourtListener result is **not** automatically treated as good law. It remains unverified until the citation/provenance/validity gates succeed.
