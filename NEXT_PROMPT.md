Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; `git pull --rebase` first.

Expected census (`node app/tools/census.mjs | tail -20`): lessons 1054 of 1214 (193, 507, 150, 204); reviews 243, none with `pass`; exams 22 topic, 1 stage, 11 mock; drills 35; bank 200; hours 3,265 stored, 3,695 summed.

Goal: lift the freeze. Close PLAN 2c O1, 4, O2 and 5 in that order; stop when under half the usage window is left.

Context not in state files: met lives in `prereq.js` `derivedMet` and `content.js` `examPassedAuto`; new floors read `skills[s]`, never `state.selfMarked`. Writing `pass` into 243 review files is content: a committed script run by the main session. Build the local CDN with `app/tools/fetch-local-cdn.sh`. `--exam mock-superday-research` times out (KNOWN_ISSUES).

Steps:
1. O1, one engine-dev in place: `app/tools/merge-wave.sh`. Acceptance per PLAN O1.
2. Wave of two engine-dev worktrees, merged with `merge-wave.sh`:
   - A, item 4 (N02, N03, F05): skill floor, revealed-screen cap, covered-skill topic pass, missed items always queue; node unit tests under `app/tools/`. Files: `prereq.js`, `state.js`, `content.js`, `screens/review.js`, `playthrough.mjs`.
   - B, O2: the five validator rules in `validate.mjs` only.
   Then run the `pass` script.
3. Item 5: engine-dev adds the performance task kind (AUTHORING 5 and 11, DECISIONS "Performance tasks"), the verb rule, and a met-rule hook. Then four content-author agents, one each in `coding-int`, `ito`, `proof`, `research-int`, author one pilot each. Protocol 4 and 5 apply.

Acceptance: item 4's scripted learner (all screens revealed, 4 of 5 on quizzes) meets zero levels; census reviews with `pass` 243; O2 rules fire on scratch cases; item 5 validator errors on a rule-matched level without a task; validator 0 errors; readiness-sums exit 0; `--routes-only --local-cdn` green with and without `--mobile`. Tick each item only on its own evidence; when 5 ticks, record the freeze lifted. Next prompt: item 6.
