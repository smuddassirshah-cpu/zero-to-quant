# NEXT_PROMPT: session AF

Read CLAUDE.md and follow its SESSION PROTOCOL. Push to the branch the harness assigns and, once per batch, to `claude/amazing-wright-d4mx7i` (CI). A push there cancels the run in progress: wait for the run first. Setup: KNOWN_ISSUES, session AB last lines. Prompts: `docs/briefs/chained-prompts.md`, with its "Session AE additions" in every brief.

Cherry-pick agents' commits, then validator, `readiness-sums.mjs --write`, commit `manifest.json`. CI status: GitHub MCP `actions_list`, `actions_get`, `get_job_logs`. Last green run: see PROGRESS, last line.

Expected census: lessons 1,236; levels 283; reviews 283 (items 2,558); exams 29 topic, 4 stage, 16 mock; drills 270; Fluency sets 100 (families 318); problem sets 128 (items 480); bank 36 files, 400 items; hours 3,695 gap 0; edges 266; validator 0 errors. Tags: `[negative-key]` 2, `[percent-form]` 3, `[tight-band]` 17, `[near-miss]` 0, `[same-course-reuse]` 0. Waivers 5, all "stands".

Merge `origin/claude/fable-audit` at start and close.

Tasks, in order:
1. Content, small: apply the 10 open findings of `docs/reviews/review-delta-ae-4.md` with its exact text (one Sonnet fixer; rule `p-futures-study` part 5 first).
2. Engine, before any new problem set (protocol 6): number the inbox from 1060; make `fresh-check` read `feedback`, `explain` and `why`; detect a retold screen (shared chain of steps or sentence skeleton with other nouns or numbers) and a rate as decimal against per cent; true positives: the reuse findings of the four `review-problems-*-1-3.md` files of session AE and `review-delta-ae-2.md` to `-ae-4.md`. If run 19's C++ compiler timeout in `test-planted-check` recurs, fix it.
3. M chained problems, PLAN 2d: 2.2 (`arma`, `coint`, `garch`), then 2.5, 2.6, 3.2, 3.4; 39 sets. Authors, not fixers, re-author a problem ruled reuse. At most two fix rounds.
4. Content, later: a second auto item for the 109 one-item skills (`docs/reports/engine-pass-ae-2.md`).

Do not raise the pilot or `acceptance.yml` on `main`. Acceptance: validator 0 errors, a green CI run at the pushed HEAD.
