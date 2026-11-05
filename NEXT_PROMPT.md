Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; `git pull --rebase` first.

Expected census (`node app/tools/census.mjs | tail -20`): lessons 1054 of 1214 (193, 507, 150, 204); reviews 243, none with `pass`; exams 22 topic, 1 stage, 11 mock; drills 35; bank 200; hours 3,265 stored, 3,695 summed. Any difference: fix state files first.

Task: PLAN 2c item 4, met rule rewrite (N02, N03, F05.1 to .4). Freeze in force. Items 1 to 3 are done; item 3 added `how` on result rows and `passedAuto` (DECISIONS "Provenance and the met rule"; AUTHORING section 13).

Context not in state files: the met rule now lives in `prereq.js` `derivedMet` plus `content.js` `examPassedAuto`; any new floor must read `skills[s]` only, never `state.selfMarked`. A review can be sat cold, so the skill floor on the review changes met. Writing per-level `pass` into 243 review files is a content edit: do it with a committed script run by the main session, not by the engine agent. Local CDN: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`, then `--local-cdn <scratchpad>/pkgs`. `--exam mock-superday-research` times out before and after item 3 (KNOWN_ISSUES).

Step: read `docs/reviews/review-course-correction.md` N02, N03 and F05. One engine-dev agent (Sonnet): essential-skill floor per level, revealed-screen cap for `done`, topic pass meets a level only on covered skills, missed quiz items always queue; unit tests for `prereq.js` and `state.js` (a node script under `app/tools/`). Then the `pass` script.

Files: `app/js/prereq.js`, `app/js/state.js`, `app/js/content.js`, `app/js/screens/review.js`, `app/tools/playthrough.mjs`, a new test script, `docs/AUTHORING.md`; review files via script only.

Acceptance: unit tests pass for each rule; a scripted learner who reveals every screen and scores 4 of 5 on quizzes ends with zero levels met; validator 0 errors; `--routes-only --local-cdn` green with and without `--mobile`; readiness-sums exit 0; census shows reviews with `pass` 243. Tick item 4 only then.
