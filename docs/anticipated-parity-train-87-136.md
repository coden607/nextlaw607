# Anticipated parity train — actions/PRs 87–136

These follow the existing 1–86 Continuity train. They target the remaining Westlaw/Lexis-style content, search, citator, document, knowledge, and trust gaps. Keep each independently reviewable.

87. Corpus coverage manifest + completeness SLO — machine-readable expected/available coverage by jurisdiction/source/date.
88. Corpus coverage dashboard — expose measured gaps/freshness without implying completeness.
89. Canonical case/opinion entity graph — clusters, opinions, aliases, parallel citations, court/date lineage.
90. Canonical statute/rule entity graph — sections, versions, effective ranges, amendment lineage.
91. Citation alias resolver — normalize reporter/neutral/vendor/public aliases to canonical IDs.
92. Full-text lexical index v1 — legal-field-aware tsvector/BM25-equivalent query path.
93. Terms-and-connectors parser — AND/OR/NOT, phrase, proximity, field constraints with deterministic validation.
94. Citation lookup search — exact and normalized citation-to-entity resolution.
95. Party-name/case-name search — normalized names, aliases, typo-tolerant matching.
96. Faceted search API — court, department, jurisdiction, date, source type, precedential status.
97. Search-within-results — deterministic secondary filtering over stable result sets.
98. Saved-search model — scoped saved queries, filters, alert policy, provenance.
99. Search result pin/folder model — matter-scoped organization with auditability.
100. Hybrid rank benchmark v2 — lexical/vector/metadata/citation-fusion evaluation on gold legal queries.
101. Search explanation payload — ranking factors/provenance without chain-of-thought.
102. Citator graph persistence — normalized citation edges with evidence and timestamps.
103. Subsequent-history resolver — appeal/reversal/affirmance/remand lineage.
104. Treatment taxonomy v2 — followed/distinguished/limited/questioned/criticized/overruled/superseded.
105. Treatment evidence extractor — exact text spans supporting treatment candidates.
106. Treatment adjudication workflow — human-review/approval state for uncertain or high-impact treatment.
107. Citator negative-treatment benchmark — recall/precision gold set and release threshold.
108. Depth-of-discussion score — deterministic evidence-backed discussion strength signal.
109. Citator filters — court/date/jurisdiction/treatment/depth.
110. Citation alert engine — authority treatment/version changes trigger matter-scoped revalidation tasks.
111. Deep Research planner v2 — issue tree, source plan, adverse-law requirement, stop conditions.
112. Deep Research research-log schema — every query/result/selection/rejection with safe provenance.
113. Research completeness gate — blocks “complete” when required issue/source/adverse passes are missing.
114. Rule/proposition graph — synthesized propositions linked to supporting/contrary verified authorities.
115. Fact-to-record graph — matter propositions linked to exhibits/transcript/page-line anchors.
116. Proposition-to-authority verifier — detect unsupported, weakly supported, or contrary propositions.
117. Quote/pinpoint verifier v2 — source span, pin cite, quotation drift, omitted-context checks.
118. Draft citation formatter — deterministic citation formatting profiles; no authority invention.
119. Table-of-authorities generator — deterministic authority extraction/classification/page references.
120. Draft redline/version service — structured revisions, attribution, rollback, comparison.
121. Draft review packet — argument matrix, support map, adverse authority, unresolved gaps in one artifact.
122. Secure Matter Vault v2 — document classes, retention, legal hold, export/delete, audit events.
123. OCR/document normalization pipeline — page-stable text + layout anchors + parser confidence.
124. Batch document question matrix — source-traceable tabular analysis across bounded collections.
125. Evidence contradiction detector — conflicting statements with exact source anchors.
126. Matter chronology v2 — dedupe/conflict resolution and source-weighted event graph.
127. Deposition/hearing prep workspace — issue/fact/exhibit/authority-linked preparation.
128. Discovery review matrix — requests/responses/obligations/deficiencies/provenance.
129. NY criminal practical-guidance schema — original checklists/notes/forms tied to verified primary law.
130. Practical-guidance publishing workflow — author/reviewer/version/effective-date controls.
131. Docket/event ingestion abstraction — normalized public docket events/filings with source rights.
132. Procedural deadline rule engine v2 — rule version, trigger event, exclusions, assumptions, verification.
133. Public ruling analytics foundation — aggregate court/judge/opinion statistics with sample coverage disclosure.
134. Firm knowledge vault — permissioned briefs/motions/memos/templates with dedupe/provenance.
135. Knowledge-aware drafting — approved exemplars + verified law with strict matter/tenant isolation.
136. Parity acceptance harness — end-to-end benchmarks proving declared-scope comparability and blocking unsupported marketing claims.

## Execution order

- 87–101: corpus/search.
- 102–110: citator.
- 111–121: deep research/drafting.
- 122–128: matter/document analysis.
- 129–136: guidance/dockets/knowledge/acceptance.

## Promotion rule

A PR may move toward merge only after its exact head revision satisfies applicable unit/integration/security/privacy/legal/CI/browser/eval gates. Do not merge from this planning branch merely because the backlog exists.
