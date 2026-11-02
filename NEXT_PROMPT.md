Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md, with the sprint override below.

Task: PLAN.md task 2a, Part S, session S1. The user has superdays coming and wants a learnable app fast. Run these in parallel, one agent each, each with its own scratchpad subfolder:
- `content-author`: recruiting L3 (`docs/briefs/recruiting.md`).
- `content-author`: mental-pressure L3 (`docs/briefs/mental-pressure.md`).
- `content-author`: puzzles L3 (`docs/briefs/puzzles.md`).
- `content-author`: brainteasers L1 (`docs/briefs/brainteasers.md`).
- Then a `content-author` for the prep tags mapping (`docs/briefs/prep-tags.md`, section "Mapping"), only if ENGINE-BACKLOG 455 is ticked; if not, an `engine-dev` agent finishes 455 first from `docs/reports/engine-prep-tags.md`.

Context not in the state files:
- Lean rules (PLAN 2a Part S): no second reads, short reports, one `--mobile` spot check per level; numbers still computed twice, code still passes its tests.
- From puzzles L2 on: follow-up screens, a pace, `tags` on drill and homework items. Name firms only in recruiting l4, mock descriptions and `prep.json`. `longform` in homework and exams only.
- Engine limits: `derive` takes expression, order or choice only; `expression` samples six seeded points; 4-column tables scroll at 390 px; `place` allows one slot per chip; `shuffle: true` on choices. Net scoring and timed papers exist for mock exams only (AUTHORING 5 and 7); where a brief says E1 or E4 are unbuilt, follow AUTHORING.
- Local CDN: `<scratchpad>/pkgs`; build with `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs` if missing. Re-run a validator error once before treating it as real while agents write.
- Commit each level as it turns green.

Acceptance, from `app/`: `node tools/validate.mjs 2>&1 | tail -5` 0 errors; `node tools/playthrough.mjs --lesson <course>/<id> --local-cdn <pkgs>` passes for every new lesson, and `--set` for each new review and homework; four reports exist; PLAN ticks each level (in tasks 2a and 3 where listed); NEXT_PROMPT.md names session S2.
