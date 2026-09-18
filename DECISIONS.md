# Architecture Decisions

## ADR-001: Preserve the direct REST research path

The application uses server-side REST adapters for CourtListener and NY Senate
because the UI needs predictable request, retry, caching, and provenance
behavior. An MCP adapter may be added for external agents later, but it must
reuse the same validation and source labels rather than become a second trust
boundary.

## ADR-002: Kysely is an access layer, not a provider

Kysely provides typed SQL access. PostgreSQL is the production database path,
with the existing local fallback retained where supported. A provider change
must not silently change authorization or migration semantics.

## ADR-003: Public sources are linkable without being citable by default

Official court and statute links are useful for verification. Self-help and
secondary sources remain discovery or procedural aids unless a primary source
is independently inspected.

## ADR-004: No unverified MCP server is enabled

No third-party MCP command, URL, credential, or executable is committed until
its provenance, permissions, transport, maintenance, and data handling are
reviewed.