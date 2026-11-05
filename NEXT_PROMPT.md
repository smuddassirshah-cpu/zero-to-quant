Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; `git pull --rebase` first.

Expected census (`node app/tools/census.mjs | tail -20`): lessons 1054 of 1214 (193, 507, 150, 204); reviews 243, none with `pass`; exams 22 topic, 1 stage, 11 mock; drills 35; bank 200; hours 3,265 stored, 3,695 summed. Any difference: fix state files first.

Task: PLAN 2c item 3, result provenance (N01). Freeze in force. Item 2 is done (readiness contract signed off; engine reads `app/content/readiness.json`).

Context not in state files: 259 homework widgets are self-ticked longform, and mock checks count as mastery and as `ok` today (KNOWN_ISSUES N01). The sandbox needs the local CDN for playthroughs: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs` (870 MB, about a minute), then pass `--local-cdn <scratchpad>/pkgs`. Without it `#drill (filters)` fails on a 404, before and after item 2.

Step: one engine-dev agent (Sonnet). `results[]` rows carry `how: auto | self | external`; `rate()` stores Elo per provenance or excludes `self`; You shows self-marked work separately; prerequisite met (`prereq.js`) ignores `self`. Old saves load, with missing `how` read as `auto` except longform and mock checks, read as `self`. Document in `docs/AUTHORING.md`. No content edits.

Files: `app/js/state.js`, `app/js/prereq.js`, `app/js/screens/you.js`, the homework and longform widget under `app/js/engine/widgets/`, `app/tools/playthrough.mjs`, `docs/AUTHORING.md`.

Acceptance: a scripted homework with only longform items cannot change a prerequisite or a mastery-map cell, and the You screen labels it self-marked; an old save without `how` imports clean; validator 0 errors; `--routes-only --local-cdn` green with and without `--mobile`; readiness-sums exit 0. Tick item 3 only then.
