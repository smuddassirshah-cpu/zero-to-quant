Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; `git pull --rebase` first.

Expected census (`node app/tools/census.mjs | tail -20`): lessons 1054 of 1214 (193, 507, 150, 204); reviews 243, none with `pass`; exams 22 topic, 1 stage, 11 mock; drills 35; bank 200; hours 3,265 stored, 3,695 summed. Any difference: fix state files first.

Task: PLAN 2c item 2, second half. Freeze in force.

Context not in state files: the user answered all eight questions (DECISIONS "Readiness contract answers"). `docs/readiness.md` is drafted and `node app/tools/readiness-sums.mjs` exits 0. The user has not signed it off. Open sign-off points: judgement calls in its "Notes for sign-off"; the trader required set is 442 lessons against the old 470-lesson closure (KNOWN_ISSUES); `brainteasers` and `game-theory` require graphs-dp and contests.

Step 1: ask the user to sign off `docs/readiness.md`, or take edits. Ask whether the brainteasers and game-theory edges into graphs-dp and contests are cut now (pulled forward from item 7) or Today filters optional courses regardless of edges. Re-run the script after any edit.

Step 2, only after sign-off: an engine-dev agent (Sonnet) adds the Strats track to `state.js:20`; makes Today read the role from the contract (required first, then recommended, never optional); makes the Learn header one total from the contract; shows "route limited: odes, numerics unwritten" on pdes. The contract may need a JSON form under `app/content/` for the engine; generate it from the script, never by hand.

Files: `docs/readiness.md`, `app/tools/readiness-sums.mjs`, `app/js/state.js`, `app/js/screens/today.js`, `app/js/screens/learn.js`, `docs/AUTHORING.md`.

Acceptance: a fresh trader profile is never shown `graphs-dp` as next work; the Learn header for trader reads 630 lessons, 1,804 h (or the signed-off figure); `--routes-only` green; validator 0 errors. Tick item 2 only then.
