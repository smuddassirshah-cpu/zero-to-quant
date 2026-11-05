Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; `git pull --rebase` first. Another session pushed to this branch during session R; if `git status -sb` shows a divergence, rebase, never reset.

Expected census (`node app/tools/census.mjs | tail -20`): lessons 1054 of 1214 (193, 507, 150, 204); reviews 243, with own pass 243; exams 22 topic, 1 stage, 11 mock; drills 35 (oa 8); bank 200; hours 3,695 stored, 3,695 summed, gap 0. Trader superday closure (`node app/tools/closure.mjs --target mock-superday-trader`): 96 levels, 32 courses, 422 lessons.

Task: PLAN 2c item 9, precision read (F08, N05). The user is the maths second reader; the item never closes on an agent alone. Past half the usage window, finish the step in flight and record the stop.

1. Main session, by script committed as `app/tools/precision-candidates.mjs`: list every `summary` line in ito, measure-prob, pdes, markov, limits-thm, random-vars and research-int that holds "only", "exactly when", "any", "always", "never", "all" or "iff" (expect about 69; the method is `docs/reviews/review-course-correction.md` lines 78 to 84). Write `docs/reviews/review-precision-3.2.md` with one row per candidate: file, line, text, counterexample attempt, verdict blank.
2. One Sonnet agent drafts the counterexample attempts only; the user judges each row. Do not fix before the user's verdicts.
3. Fixes by the fix-pass rule (grep the old value); the five known lines (`ito/l1:904`, `pdes/l1:1194` and the three in N05) fixed.

Then: odes L1 to L4, numerics L1 to L4 and complex L1 from `docs/briefs/`, one content-author per course (wave of three, `merge-wave.sh`), so pdes loses "Route limited".

Open from R: capstone records empty (user fills `app/content/capstones.json`); `mock-sample-draw` intermittent (KNOWN_ISSUES, engine item).

Acceptance: review file with one row per candidate and user verdicts; validator 0 errors; playthrough of changed lessons green with and without `--mobile`.

After each merge: `node app/tools/perf-pending.mjs --prune`. Local CDN: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`.
