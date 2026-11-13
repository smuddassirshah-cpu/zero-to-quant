# NEXT_PROMPT: session AE

Read CLAUDE.md and follow its SESSION PROTOCOL. Push to `claude/amazing-wright-d4mx7i` (CI trigger and cache), mirrored to any branch the harness assigns; while agents run, push the CI branch once per batch (DECISIONS, session AD). Setup: KNOWN_ISSUES, session AB last lines. Prompts: `docs/briefs/chained-prompts.md`. Add to every brief: the agent commits itself; number scripts resolve paths from `__file__`; greps for reuse use every variable letter.

Cherry-pick agents' commits, then validator, `readiness-sums.mjs --write`, commit `manifest.json`. CI: `gh api repos/<owner>/<repo>/actions/runs/<id>/jobs`. Last green run: 18 at `ca4ad45` (60 jobs); later commits are docs only.

Expected census: lessons 1,236; levels 283; reviews 283 (items 2,558); exams 29 topic, 4 stage, 16 mock; drills 270; Fluency sets 100 (families 318); problem sets 116 (items 432); bank 36 files, 400 items; hours 3,695 gap 0; edges 266; validator 0 errors. Tags: `[negative-key]` 2, `[percent-form]` 3, `[tight-band]` 17, `[near-miss]` 0, `[same-course-reuse]` 0.

Merge `origin/claude/fable-audit` at start and close (resolve `docs/BACKLOG-INBOX.md` by dropping bullets already numbered).

Tasks, in order:
1. Engine, before any new problem set (protocol 6, fourth sighting): number the 34 inbox bullets from 1028; extend `fresh-check` same-course mode to a function with its interval or factorisation, a key number pair, a shifted or scaled transform, a region with its integrand (true positives: the eight reuse findings in the five `review-problems-*` files of session AD); wire `--changed` into the `number-scripts` job and pin SciPy.
2. Content fixes owed: the six waived items in `app/tools/same-course-waivers.json`; a larger hidden test for `ci-rebuild-from-orders`; "counterclockwise" in 14 files; add `a-spline-columns` to `docs/briefs/exam-stage-2-scripts/build.py`.
3. M chained problems, PLAN 2d: topic 2.1 levels 1 to 3, then 2.2, 2.5, 2.6, 3.2, 3.4. Second read, fix, delta read of re-keyed problems.
4. `acceptance.yml` on `main`: ask the user again (skipped in AD).

Do not raise the pilot. Acceptance: validator 0 errors, a green CI run at the pushed HEAD. Files: engine and docs for 1; `app/content/courses/<course>/problems-<n>.json` for 3.
