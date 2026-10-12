# OG brand-asset pass

The brand-asset pass owns the app's public identity: `public/` brand assets
(`og.jpg`/`og.png`, `x-banner.jpg` for canvas apps, `public/__grok/` icons)
plus `src/lib/og/site.json` (`title`, `card`, `type`, `color`). Everything a
scraper or an install prompt reads about the app flows through those two
surfaces, so they get a dedicated owner instead of whatever QA remembers to
check.

Run it for custom-card apps — games of every kind, whimsical/creative apps,
brand-forward pages. Plain utilities skip it: they get a soft BRAND NOTE, not
a failure, and the `--placeholder-ok` flag exists for exactly that pass.

## Brand-asset pass:

- Launch as a `task` subagent the moment name and palette settle — during
  scaffolding, not at QA time. Generating card art on the critical path is
  pure waiting.
- **No `wait_tasks`, never `get_task_output` on it** — consuming a task's
  output suppresses its completion notification, so the result, failure
  included, would reach nobody. Answer without it; one sentence more when it
  wakes you.
- While it runs it keeps `/workspace/.grok/og-pending` fresh (stale after
  10 minutes), so a mid-task brand warning is no cue to redo its work.
- Self-check before handing back: `node scripts/brand-check.mjs --placeholder-ok`
  (add `--game` for DOM board/word games with no real `<canvas>` to detect;
  `--root <dir>` points the check at another workspace). A custom-card pass
  must come back clean, not warned.
- A live card file wins over every config: drop `public/og.jpg` and the
  checks stamp `card=custom` themselves; `site.json` claiming `card=custom`
  with no file on disk is a warning, not a pass.
