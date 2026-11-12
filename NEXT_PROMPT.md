# NEXT_PROMPT: session AC

Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i`. Local CDN, venv (Python 3.12) and test flags: KNOWN_ISSUES, session AB, last lines. Commit an `engine-dev` worktree from the main session hourly. Brief tail and acceptance list: DECISIONS, session AB.

Expected census: lessons 1,236; levels 283; reviews 283 (items 2,558); exams 29 topic, 4 stage, 16 mock; drills 270; Fluency sets 100 (families 318); problem sets 87 (items 332); bank 36 files, 400 items; hours 3,695 gap 0; edges 266; validator 0 errors.

Merge `origin/claude/fable-audit` at start and close.

Tasks, in order. Tasks 1 to 4 are the user's priority (12 Nov): cut waiting on tests and runs without dropping a check.
1. CI: `.github/workflows/acceptance.yml` on push: validator, readiness-sums, all `tools/test-*`, `--all` in 12 to 16 shards, `--problems all`, `--drills`, `--fluency-all`, routes, desktop and `--mobile`, on real jsDelivr. Confirm one green run and its wall clock.
2. Engine: a green-hash cache (content file hash plus engine hash) so `playthrough.mjs --changed` replays only what changed; a fixtures-only content root for the `test-validate-*` files; a node check of keys, bands and slip routing for all content.
3. CLAUDE.md and the brief tail: readers run no browser; fixers play only files they edit; engine agents run the tests they touched; the session's acceptance is `--changed` plus a green CI run.
4. Delta reads owed (KNOWN_ISSUES, session AB), as script reruns where only a key changed.
5. Content passes from the new rules: `[percent-form]` 74, `[negative-key]` 240, `[tight-band]` 26, `[near-miss]` 190 drills; `stage-3` `r-t-bar`, `r-best-of-twenty`.
6. M chained problems, PLAN 2d: `eigen` 4, `number-sense` 1 to 3, `ratio`, then 0.6, 1.10, 1.11.

Do not raise the pilot. Acceptance at the final HEAD; NEXT_PROMPT for session AD.
