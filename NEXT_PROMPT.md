# NEXT_PROMPT: session AI (4 of 4 to DONE)

Read CLAUDE.md and follow its SESSION PROTOCOL, with these overrides from the user (16 Nov), which hold until DONE:
- Scope is larger than one PLAN task: work every task below in order. Waves may hold up to six agents.
- Ignore the "half the usage window" rule; stop a wave only if agents fail to start.
- This file may exceed 300 words.

Push to the branch the harness assigns and to `claude/amazing-wright-d4mx7i` (CI). A push there cancels the run in progress: push it only when no run is in progress. Setup: KNOWN_ISSUES, session AB last lines (the clone is shallow: `git fetch --unshallow origin claude/amazing-wright-d4mx7i claude/fable-audit` before merging the audit branch; it had no new commits on 17 Nov at session AH close). CI status: GitHub MCP `actions_list`, `actions_get`, `get_job_logs` (the job list is large: read it with `jq '.jobs.jobs[]'` from the saved file). A push that touches only `docs/` or root state files starts no run. A dispatch straight after a push leaves the push run queued: cancel the push run with `actions_run_trigger` `cancel_workflow_run`. Last green full run: 35 at 5b651e21 (full, by dispatch; later commits are docs and state files only). Before any push to the CI branch run, from `app/`, `node tools/run-number-scripts.mjs --python <venv>/bin/python --changed <last green sha>`. Tell `engine-dev` in the brief: "you must commit your own work; the coordinator authorises it". Tell every agent to leave no background process and to hand back once. Sub-agents sign commits with their own model's line; leave it.

Expected census: lessons 1,236; levels 283; reviews 283 (items 2,558); exams 29 topic (21 to 36 items), 4 stage, 16 mock; drills 270; Fluency sets 100 (families 318); problem sets 167 (items 617); bank 36 files, 400 items; hours 3,695 gap 0; edges 266; validator 0 errors (4,607 warnings). Tags: `[negative-key]` 2, `[percent-form]` 3, `[tight-band]` 17, `[wrong-band]` 68, `[rounding-tie]` 5, `[key-in-question]` 3, `[carry-band]` 11, `[band-edge]` 3, `[later-key]` 10, `[no-chain]` 7, `[slip-in-key-band]` 2; `[near-miss]`, `[working-band]`, `[table-source]`, `[wide-wrong-tol]` 0. Waivers 60, all "stands" (59 with a source). `same-course-reuse --all`: 0 errors, 0 warnings, 44 waived. `docs/ENGINE-BACKLOG.md`: 0 lines "status: open"; inbox holds two post-completion bullets.

## Session map (PLAN "Route to DONE")
- AH (done): engine pass 9 and its tightening, engine pass 7 closed, AG-close items, gallery in both themes, full acceptance.
- AI: PLAN section 7. Nothing slipped from AH.
- Not in DONE (user, 16 Nov): the Fable concept audit (PLAN 5b) and the pilot (task 12).

## Tasks for AI, in order
1. Getting started (PLAN section 7, line 1): `README.md` (23 lines) and `app/README.md` (88 lines) describe clone, `app/run.sh`, first load (jsDelivr for Pyodide, MathLive, Compute Engine, YoWASP clang) and the self-host fallback in `app/vendor/`. One agent writes; a second follows the text literally on a fresh clone in a scratch folder (serve, open in Chromium, run one Python and one C++ item, then with jsDelivr blocked and the vendor fallback) and lists what fails; one fix pass.
2. `docs/PLAN.md` section 13 (definition of done, line 308) item by item: one reader marks each item met (with the evidence: file, test, CI job, census line) or not met; gaps go to KNOWN_ISSUES. Fix what is small; anything large goes to the user in the final report, not into a new wave.
3. Small open items of KNOWN_ISSUES "session AH close", only if section 13 needs them: `topology/problems-2` `p-right-rays` (four questions under a lede that promises a chain: reword the lede or re-author, then one delta read); `grade-all --code` over all content (new runner, tried on three files); confirm `test-fresh-check-pkg3.mjs` fails without its fix.
4. Final report to the user (what is built, census, what is not in DONE, known issues in order of weight, how to run it), then create `DONE`. Tick PLAN section 7.

Do not raise the pilot, the audit's place in DONE, or `acceptance.yml` on `main`. Acceptance: validator 0 errors, `same-course-reuse --all` 0 errors, a green run of `acceptance.yml` at the last commit that touches `app/` (dispatch suite full, mode full if anything under `app/` changed other than a README). Merge `origin/claude/fable-audit` at start and close.
