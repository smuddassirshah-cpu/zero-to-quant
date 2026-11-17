# NEXT_PROMPT: session AH (3 of 4 to DONE)

Read CLAUDE.md and follow its SESSION PROTOCOL, with these overrides from the user (16 Nov), which hold until DONE:
- Scope is larger than one PLAN task: work every task below in order. Waves may hold up to six agents.
- Ignore the "half the usage window" rule; stop a wave only if agents fail to start.
- This file may exceed 300 words.

Push to the branch the harness assigns and to `claude/amazing-wright-d4mx7i` (CI). A push there cancels the run in progress: push it only when no run is in progress. Setup: KNOWN_ISSUES, session AB last lines (the clone is shallow: `git fetch --unshallow origin claude/amazing-wright-d4mx7i claude/fable-audit` before merging the audit branch; it had no new commits on 17 Nov). CI status: GitHub MCP `actions_list`, `actions_get`, `get_job_logs` (the job list is large: read it with `jq` from the saved file). A push that touches only `docs/` starts no run: dispatch `acceptance.yml` on the CI branch with `actions_run_trigger`. Last green run: 29 at `86e0d611`; run 30 at `90bd03bc` (the closing content HEAD) was queued when this was written: check it first. Before any push to the CI branch run, from `app/`, `node tools/run-number-scripts.mjs --python <venv>/bin/python --changed <last green sha>` (under two minutes) and `--only exam` after any exam edit. Cherry-pick agents' commits; on an inbox conflict keep the cleared inbox and append only the commit's added bullets; on a report conflict keep both sections. `engine-dev` commits nothing unless told: tell it to commit per item, and commit its worktree from the main session hourly. Briefs must say `git merge --ff-only <branch>` as the fallback when `git reset --hard` is refused in a worktree. Sub-agents sign commits with their own model's attribution line; leave it.

Expected census: lessons 1,236; levels 283; reviews 283 (items 2,558); exams 29 topic (21 to 36 items), 4 stage, 16 mock; drills 270; Fluency sets 100 (families 318); problem sets 167 (items 617); bank 36 files, 400 items; hours 3,695 gap 0; edges 266; validator 0 errors (4,569 warnings). Tags: `[negative-key]` 2, `[percent-form]` 3, `[tight-band]` 17, `[near-miss]` 0, `[wrong-band]` 68; `[working-band]`, `[rounding-tie]`, `[table-source]`, `[wide-wrong-tol]` 0. Waivers 53, all "stands". `same-course-reuse --all`: 0 errors, 1 warning (`regression/problems-2` `p-grocer-beta`), 37 waived.

## Session map (PLAN "Route to DONE")

- AG (done): 167 sets, PLAN 2d ticked, exam second items, engine pass 8.
- AH: tasks below.
- AI: Getting started in both READMEs; `docs/PLAN.md` section 13 item by item; final report; `DONE`. Spare session if AH overruns.
- Not in DONE (user, 16 Nov): the Fable concept audit (PLAN 5b) and the pilot.

## Tasks for AH, in order

1. Engine pass 9, first, one `engine-dev` agent: number the 57 inbox bullets from 1154 and clear the inbox. Build only what content correctness needs (KNOWN_ISSUES "session AG close", rule gaps): `[rounding-tie]` for a slip on a tie at any asked places, a key within half a unit of the last place of a tie, and a printed product that lands on a tie; `[working-band]` carrying each printed rounded value forward through the next part; a warning for a numeric key printed in its own part's question; the mobile playthrough fails when text runs past the page at 440 px; the voice scan flags a lesson id in a code span in learner text; `playthrough --problems` says "run the validator first" when the manifest lacks the set. Tests on `tools/fixtures/mini-app`. List the hits on the 167 sets and the exams; one reader triages; one Sonnet fix pass.
2. Engine pass 7 remainder: [Must] and [Should] of 340 to 422 and the deferred list in `docs/reports/engine-pass-7.md` (87 backlog lines read "status: open" in all; triage first, two or three `engine-dev` agents on disjoint files). Move every [Could], E13 and E15 to E19 to a post-completion list in `docs/ENGINE-BACKLOG.md`; build none of them. Tick PLAN section 6 lines as they close.
3. The small open items of KNOWN_ISSUES "session AG close", one Sonnet fixer with exact text: `p-grid-budget` part 3 `tol.abs` 0.007; `topic-2.3` `e-honest-bar` pace 90; waive or reword `p-grocer-beta`; split the 45-word prompt in `testing/homework-3.json`. One author agent for `topology/problems-2` `p-signal-bands` and `pdes/problems-3` `p-grid-budget` parts 1 and 2, then one delta read of those two problems plus the thinly checked keys listed there.
4. Full acceptance by manual dispatch of `acceptance.yml` on the CI branch (`suite: full`, `mode: full`); read the failing jobs' `FAIL` lines and fix what it finds. If `test-planted-check` (C++ compiler timeout) or the two `stat-learning` level 4 number scripts fail, read the lines before touching a tolerance; `stat-learning-L4-numbers.py` takes four minutes locally.
5. System gallery renders in both themes (PLAN section 6, last line): one agent screenshots every gallery entry in light and dark at 440 and 1376 px, lists faults, one fix pass.

Do not raise the pilot, the audit's place in DONE, or `acceptance.yml` on `main`. Acceptance: validator 0 errors, `same-course-reuse --all` 0 errors, a green full run at the pushed HEAD. At close write NEXT_PROMPT for AI from the session map, corrected for what slipped; merge `origin/claude/fable-audit` at start and close.
