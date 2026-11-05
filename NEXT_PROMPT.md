Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; `git pull --rebase` first.

Expected census (`node app/tools/census.mjs | tail -20`): lessons 1054 of 1214 (193, 507, 150, 204); reviews 243, none with `pass`; exams 22 topic, 1 stage, 11 mock; drills 35; bank 200; hours 3,265 stored, 3,695 summed. Any difference: fix state files first.

Task: PLAN 2c item 2, readiness contract per role (F01, N04). Freeze in force. Do not write the contract until the user has answered:

1. Roles: trader, researcher, developer, strats, derivatives? `state.js:20` has only Trader, Researcher, Developer, Undecided. Add strats and derivatives as tracks, or map them onto existing ones?
2. Trader: are ds, graphs-dp, algo-think, contests, integrals and multivar required, recommended or optional? Today the trader superday closure pulls them in (107 levels, 470 lessons).
3. Finance basics: required for traders and researchers (`docs/curriculum.md:292`) or recommended?
4. Undecided: shared foundation to which stage before the role fork?
5. Missing mocks (mock-video, mock-oa-strats, mock-superday-strats, mock-superday-developer, mock-oa-code-hard): listed as gaps, or dropped from prep.json?
6. Learn header: one total for the chosen role only?

Also pending: item 7 (odes and numerics before 2b: write them, or mark pdes route-limited) and item 8 (who reviews capstones).

With answers: agent drafts `docs/readiness.md` (independent tasks, required, recommended, optional courses, existing and missing mocks per role) from `docs/curriculum.md`, `content/prep.json` and `docs/reviews/review-curriculum-first.md` section 5; user signs off; then an engine agent makes Today read the role. Without answers: draft options only and stop.

Files: `docs/readiness.md`, `app/js/screens/today.js`, `app/js/state.js`, `app/js/screens/learn.js`.

Acceptance: a fresh trader profile is never shown `graphs-dp` as next work unless the contract makes it required; Learn shows one total equal to the contract's sum for that role; `--routes-only` green.
