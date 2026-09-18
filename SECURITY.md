# Security Baseline

- Secrets are server-only and supplied through environment variables. Never
  commit `.env`, tokens, API keys, or captured secret-bearing logs.
- Validate and constrain all user, network, and model output before rendering,
  persisting, or using it in a command or query.
- Keep authentication and authorization checks at server boundaries; do not
  trust client-supplied user or matter identifiers.
- Treat CourtListener, NY Senate, model output, and uploaded matter content as
  untrusted data. Escape rendered text and reject unsupported authority.
- Review dependency changes with `npm audit` when network access is available;
  do not resolve findings by weakening validation or silently suppressing
  errors.

The application is a drafting aid, not a court filing system. Security review
does not establish legal sufficiency or attorney-client privilege.