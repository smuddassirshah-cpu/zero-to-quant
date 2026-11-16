# NEXT_PROMPT: session AF (1 of 4 to DONE)

Read CLAUDE.md and follow its SESSION PROTOCOL, with these overrides from the user (16 Nov), which hold until DONE:
- Scope is larger than one PLAN task: work every task below in order and start the next wave while the last one's readers run. Waves may hold up to six agents; one course per author, up to three levels; a course with four levels gets a second author for level 4 in the next wave.
- Ignore the "half the usage window" rule; stop a wave only if agents fail to start.
- This file may exceed 300 words.

Push to the branch the harness assigns and to `claude/amazing-wright-d4mx7i` (CI). A push there cancels the run in progress: push it only when no run is in progress, at most once per wave. Setup: KNOWN_ISSUES, session AB last lines. Prompts: `docs/briefs/chained-prompts.md` with its "Session AE additions" in every brief. Cherry-pick agents' commits, then validator, `readiness-sums.mjs --write`, commit `manifest.json`. CI status: GitHub MCP `actions_list`, `actions_get`, `get_job_logs`. Last green run: 24 at `3c39d0c` (30 jobs); later commits are docs only. Merge `origin/claude/fable-audit` at start and close.

Expected census: lessons 1,236; levels 283; reviews 283 (items 2,558); exams 29 topic, 4 stage, 16 mock; drills 270; Fluency sets 100 (families 318); problem sets 128 (items 480); bank 36 files, 400 items; hours 3,695 gap 0; edges 266; validator 0 errors. Tags: `[negative-key]` 2, `[percent-form]` 3, `[tight-band]` 17, `[near-miss]` 0, `[same-course-reuse]` 0. Waivers 5, all "stands".

## Session map (PLAN "Route to DONE"; DECISIONS session AE close)

- AF: tasks 1 to 4 below. Target at close: 149 sets.
- AG: chained sets for 3.2 (`ito`, `measure-prob`, `pdes`) and 3.4 (`algebra`, `topology`), 18 sets, 167 in all, PLAN 2d ticked; a second auto item for the 109 one-item exam skills; engine pass 8 on the inbox.
- AH: engine pass 7 remainder ([Must] and [Should] of 340 to 422 and the deferred list; every [Could], E13 and E15 to E19 moved to a post-completion list, not built); full acceptance by manual dispatch `mode: full`; System gallery in both themes; fix what it finds.
- AI: Getting started in both READMEs; `docs/PLAN.md` section 13 item by item; final report; `DONE`. Spare session if AH overruns.
- Not in DONE (user, 16 Nov): the Fable concept audit (PLAN 5b) and the pilot. Both run after release.

## Tasks for AF, in order

1. Start together. (a) One Sonnet fixer applies the 10 open findings of `docs/reviews/review-delta-ae-4.md` with its exact text; rule `p-futures-study` part 5 first. (b) Engine agent, before any new set (protocol 6): number the 22 inbox bullets from 1060; `fresh-check` reads `feedback`, `explain` and `why`; it detects a retold screen (shared chain of steps or sentence skeleton with other nouns or numbers, any level of the course) and a rate written as a decimal against a per cent; true positives are the reuse findings of the four `review-problems-*-1-3.md` files of session AE and `review-delta-ae-2.md` to `-ae-4.md`; the new kinds are errors; hits on the 128 existing sets are listed, triaged by one reader, then fixed or waived as "stands".
2. Wave A, when 1(b) is merged, six authors: `arma` 1 to 3, `coint` 1 to 3, `garch` 1 to 3, `stat-models` 1 to 3, `convex` 1 to 3, `numerics` 1 to 3 (18 sets).
3. Wave B, three authors, started as soon as wave A's authors hand back: `stat-models` 4, `convex` 4, `numerics` 4 (3 sets).
4. Per course: second read, one fix pass, one delta read of re-keyed or re-authored problems, one more fix pass at most. A problem ruled reuse goes back to an author agent, never a fixer, with the lesson screens it must not walk named in the brief. What is still open after two rounds goes to KNOWN_ISSUES with exact fix text and is fixed first thing in AG.

If run 19's C++ compiler timeout in `test-planted-check` or the two flaky `stat-learning` level 4 number scripts fail again, read the `FAIL` lines and fix the cause in this session.

Do not raise the pilot, the audit's place in DONE, or `acceptance.yml` on `main`. Acceptance: validator 0 errors, `same-course-reuse --all` 0 errors, a green CI run at the pushed HEAD. At close write NEXT_PROMPT for AG from the session map, corrected for what slipped.
