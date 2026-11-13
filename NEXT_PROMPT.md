# NEXT_PROMPT: session AD

Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i`. Setup (CDN with fonts, venv 3.12): KNOWN_ISSUES, session AB last lines. Brief tail: DECISIONS, "Test and run time". Shared prompts used in AC (chained author, reader, fixer) are not in the repo: rebuild them from `docs/briefs/chained.md`, both second-read briefs and DECISIONS session AC.

Every brief opens with: if HEAD is not a descendant of the local branch, `git reset --hard claude/amazing-wright-d4mx7i`. Bring agents' commits in with `git cherry-pick`, then run the validator, `readiness-sums.mjs --write`, commit `manifest.json` (KNOWN_ISSUES, session AC). Read CI with `gh api repos/<owner>/<repo>/actions/runs/<id>/jobs`.

Expected census: lessons 1,236; levels 283; reviews 283 (items 2,558); exams 29 topic, 4 stage, 16 mock; drills 270; Fluency sets 100 (families 318); problem sets 106 (items 399); bank 36 files, 400 items; hours 3,695 gap 0; edges 266; validator 0 errors. Tags: `[negative-key]` 3, `[percent-form]` 3, `[tight-band]` 17, `[near-miss]` 0.

Merge `origin/claude/fable-audit` at start and close.

Tasks, in order:
1. Engine: number the AC items and all inbox bullets into `docs/ENGINE-BACKLOG.md` (from 971), clear the inbox. Then build: a CI job running every `*-numbers.py` (first triage the 28 that already fail, `docs/reports/number-scripts-ac.md`); `fresh-check` same-course mode (numbers, matrices up to scale and transpose, 8-word shingles), gated; why changed-only `extras problems` jobs took 18 minutes.
2. Put `acceptance.yml` on `main` so the weekly full run fires (ask the user: it needs a pull request or a push to `main`).
3. M chained problems, PLAN 2d: `analysis` 4 and 5, `linear-maps` 4, `odes` 1 to 4, `vector-calc` 1 to 3. Authors grep their own course first.
4. Open items in KNOWN_ISSUES session AC: `complex/l13` screens[10], `limits-thm/l7` screens[9], the near-miss re-read of 106 marked plants, `unit: "%"`.

Do not raise the pilot. Acceptance: validator 0 errors, a green CI run at the pushed HEAD. Files: engine and docs for 1; `app/content/courses/<course>/problems-<n>.json` for 3.
