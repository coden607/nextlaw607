# Legal War Room and MCP integrations

The legal-analysis methodology is vendored from `coden607/skills` under `.agents/skills/`. Load only the skills relevant to the case. Never cite unverified law, treat case data as confidential, and require attorney review before filing.

## Configured MCP
- **CourtListener**: `.mcp.json` declares Free Law Project's official remote MCP endpoint. Authenticate through the MCP client's OAuth flow. The declaration alone does **not** prove the server is connected or operational.

## Additional available integrations (not automatically enabled)
- **CourtListener REST API**: existing server-side `COURTLISTENER_API_TOKEN` integration; no token in source.
- **NY Senate Open Legislation**: existing authority-harvest integration.
- **GitHub**: development and PR workflows only; requires an authorized GitHub MCP connection.
- **Google Drive / Gmail / Calendar / Slack**: optional evidence, matter communications, and scheduling; must be separately authenticated and explicitly authorized for each matter. Do not give them blanket access to privileged data.
- **Adobe Acrobat**: optional PDF/exhibit processing, with redaction and attorney review.
- **Vercel / Supabase / Stripe**: deployment, data, and payment administration only; do not connect to legal reasoning or case files by default.
- **CourtListener judicial and docket search**: use the CourtListener MCP and existing REST adapter; do not assume all endpoints have been tested.

## Security gates
1. All remote services are opt-in, scoped, and read-only by default.
2. No secrets, tokens, personal case files, or privileged material in committed configuration.
3. Do not send, file, pay, modify production, or share data without explicit approval.
4. CitationFirewall remains fail-closed: external hits are leads until verified against primary authority.
5. MCP clients differ in configuration format; adapt this catalog per client, verify connectivity and permissions before claiming operational support.

## Installation verification
- Confirm the five skill files are present.
- Inspect `.mcp.json` in an MCP client supporting remote HTTP transport.
- Complete CourtListener OAuth if prompted, then run a read-only case search.
- Validate source and citation provenance; do not treat an MCP search result as a verified holding.
