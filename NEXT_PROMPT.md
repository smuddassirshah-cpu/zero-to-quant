Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 0, "Triage work left in flight on 27 Oct".

Context not in the state files: the previous orchestration ran twenty agents at once and was stopped mid-flight on 27 Oct. Files on disk that no agent reported on may be complete, partial, or unvalidated: `app/content/courses/arma/` level 3 (l9 to l12, review-3, homework-3), `app/content/courses/alpha/` level 3, `app/content/courses/opt-dash/` levels 2 to 4 (reviews, homeworks and l15, l16 missing), and possibly `coint/` and `contests/` level 1 files. Engine pass 7 (`app/js/`, `app/tools/validate.mjs`, `docs/AUTHORING.md`, canvas READMEs) was interrupted; its "Seventh pass" status block in `docs/ENGINE-BACKLOG.md` may be missing or partial. `docs/reviews/review-1.9.md` may be a partial second-reader file.

Do: delegate to a `file-finder` agent for the table of present files against course maps and reports; then, per unreported level, a `test-fixer` agent that runs the validator and the playthrough (`--local-cdn` only if the scratchpad `pkgs` folder named in `docs/LEVEL-BRIEF.md` exists on this machine; otherwise plain, which needs network) and either confirms the level green and writes a short `docs/reports/<course>-<level>.md`, or deletes the partial files. Run `node tools/playthrough.mjs --all 2>&1 | tail -30` from `app/` once; if engine changes broke it and the fix is not obvious, revert `app/js` and `app/tools` to the last commit whose message starts "engine integration pass 6" and record the loss in KNOWN_ISSUES.md.

Files likely touched: the course folders above, `docs/reports/`, `app/js/`, `app/content/manifest.json`, PLAN.md, PROGRESS.md, KNOWN_ISSUES.md.

Acceptance: `node tools/validate.mjs` reports 0 errors; `playthrough.mjs --all` passes; every level on disk is either green with a report or removed; PLAN.md ticks task 0 and lists any level that was removed back under its course; NEXT_PROMPT.md names the next task (garch L2).
