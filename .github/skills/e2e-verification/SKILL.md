---
name: e2e-verification
description: Use when validating a NextLaw607 browser flow, Playwright smoke run, responsive layout, console errors, or release gate.
---

Read `TESTING.md` and `VERIFICATION-GATES.md`. Start the app through the
documented npm script, use Playwright when its browser runtime is available,
capture desktop and mobile results, inspect console and network failures, and
report unavailable browser prerequisites rather than converting them into a
passing result.