# NEXT_PROMPT: session AG (2 of 4 to DONE)

Read CLAUDE.md and follow its SESSION PROTOCOL, with these overrides from the user (16 Nov), which hold until DONE:
- Scope is larger than one PLAN task: work every task below in order and start the next wave while the last one's readers run. Waves may hold up to six authors; one course per author, up to three levels; a course with four or more levels gets further authors in the next wave.
- Ignore the "half the usage window" rule; stop a wave only if agents fail to start.
- This file may exceed 300 words.

Push to the branch the harness assigns and to `claude/amazing-wright-d4mx7i` (CI). A push there cancels the run in progress: push it only when no run is in progress, at most once per wave. Setup: KNOWN_ISSUES, session AB last lines (the clone is shallow: `git fetch --unshallow origin claude/amazing-wright-d4mx7i claude/fable-audit` before merging the audit branch). Briefs, all in `docs/briefs/`: `chained-prompts.md` (author, reader), `reauthor-fix-af.md` (re-author and fix pass after a second read, one author agent per course), `delta-read-af.md`, `round2-fix-af.md` (last Sonnet fix pass), `reauthor-af.md`. Rename nothing; fill COURSE, SETS, REVIEW, NAME. Cherry-pick agents' commits (inbox conflicts: keep both sides), then validator, `readiness-sums.mjs --write`, commit `manifest.json` and the readiness files. A container restart stops every agent: worktrees survive, resume with a brief that names the worktree path and forbids a reset; agents commit per set. CI status: GitHub MCP `actions_list`, `actions_get`, `get_job_logs`. Merge `origin/claude/fable-audit` at start and close.

Expected census: lessons 1,236; levels 283; reviews 283 (items 2,558); exams 29 topic, 4 stage, 16 mock; drills 270; Fluency sets 100 (families 318); problem sets 149 (items 555); bank 36 files, 400 items; hours 3,695 gap 0; edges 266; validator 0 errors. Tags: `[negative-key]` 2, `[percent-form]` 3, `[tight-band]` 17, `[near-miss]` 0, `[wrong-band]` 98. Waivers 41, all "stands". `same-course-reuse --all` 0 errors.

## Session map (PLAN "Route to DONE")

- AG: tasks below. Target at close: 167 sets, PLAN 2d ticked.
- AH: engine pass 7 remainder ([Must] and [Should] of 340 to 422 and the deferred list; every [Could], E13 and E15 to E19 moved to a post-completion list, not built); full acceptance by manual dispatch `mode: full`; System gallery in both themes; fix what it finds.
- AI: Getting started in both READMEs; `docs/PLAN.md` section 13 item by item; final report; `DONE`. Spare session if AH overruns.
- Not in DONE (user, 16 Nov): the Fable concept audit (PLAN 5b) and the pilot.

## Tasks for AG, in order

1. Start together. (a) One author agent closes KNOWN_ISSUES "session AF close", `p-hedge-ranks` (n and data changed, every part recomputed, gates, then one reader on that problem only). (b) Engine pass 8, before any new set (protocol 6): number the inbox bullets from 1082; build as validator or `fresh-check` rules, with tests on `tools/fixtures/mini-app`: a band that must take the value the part's printed working gives; no key or slip on a rounding tie; a tail or table value must name its source; a percentage part carries unit "%"; `[wrong-band]` skips a slip that rounds to 0 at the asked places; same-course reuse reads the exams that hold the course's items; `retold` skips short stock lines and prints every matched pair; waivers carry a `source`. List hits on the 149 sets, one reader triages, fix or waive as "stands".
2. Wave C, when 1(b) is merged, five authors: 3.2 `ito`, `measure-prob`, `pdes`; 3.4 `algebra`, `topology` (18 sets: check each course's level count in `course.json` and split authors so none writes more than three). Every author brief adds: read the topic, stage and mock exams with the course's items before writing; name the closest lesson screen, quiz, review, homework and exam item per problem; no walk through several quiz or exam items in a row.
3. Per course, the AF chain: second read; one author agent re-authors and fixes; delta read; one Sonnet fix pass. What stays open after that goes to KNOWN_ISSUES with exact fix text. Expect about a quarter of new problems ruled re-author.
4. A second auto item for the 109 one-item exam skills (PLAN; brief pattern in `docs/reports/exam-1.8.md`), second-read and fixed.
5. Tick PLAN 2d when 167 sets are in and read.

If `test-planted-check` (C++ compiler timeout) or the two `stat-learning` level 4 number scripts fail in CI, read the `FAIL` lines; `stat-learning-L4-numbers.py` takes four minutes locally, so check the job's time limit first.

Do not raise the pilot, the audit's place in DONE, or `acceptance.yml` on `main`. Acceptance: validator 0 errors, `same-course-reuse --all` 0 errors, a green CI run at the pushed HEAD. At close write NEXT_PROMPT for AH from the session map, corrected for what slipped.
