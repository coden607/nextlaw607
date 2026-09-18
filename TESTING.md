# Testing

## Local gates

Run these in order after installing dependencies:

```bash
npm run lint
npm run typecheck
npm test
npm run build
```

`npm test` covers deterministic scripts and the auth/app-data tests. The build
also runs the repository migration step.

## Browser verification

Start the app with `npm run dev`, then run the repository browser smoke script:

```bash
node scripts/browser-smoke.mjs
```

The smoke run must be checked for visible content, console errors, failed
module or asset loads, and desktop/mobile layout. Playwright is a dependency;
the browser binary must be installed in the execution environment before this
gate can pass.

For interactive flows, use Playwright against the running app and cover the
navigation routes, intake/draft state transitions, research fallback behavior,
triad validation, and keyboard accessibility. Do not use live model or legal
provider calls in deterministic tests.