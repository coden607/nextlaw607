# NextLaw607 Project Contract

Active product direction: build NextLaw607 toward **functional day-to-day comparability** with Westlaw + CoCounsel and Lexis+ + Protégé for the selected scope, while preserving NextLaw607's fail-closed legal-verification model.

Read in this order before substantial work:

1. `AGENTS.md`
2. `docs/legal-platform-parity.prd.md`
3. `docs/legal-platform-parity-architecture.md`
4. `docs/anticipated-pr-train-26.md`
5. `docs/anticipated-parity-train-87-136.md`
6. Relevant legal, security, testing, verification, and canonical skill documents.

Scope rule: New York criminal law remains the flagship/deepest vertical. Criminal matters may use ancillary civil/procedural authorities when legally necessary; do not turn family/civil practice into primary product surfaces.

Architecture rule: AI/RAG is an analysis layer over source-controlled legal data. Retrieval never promotes text to citable authority. CitationFirewall remains the sole authority-promotion boundary.

Execution rule: use deterministic/Jev logic before model spend, keep one coherent risk boundary per PR, preserve provenance, and never weaken security/privacy/verification gates to make a change pass.
