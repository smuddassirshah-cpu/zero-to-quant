Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; `git pull --rebase` first.

Expected census (`node app/tools/census.mjs | tail -20`): lessons 1054 of 1214 (193, 507, 150, 204); reviews 243, with own pass 243; exams 22 topic, 1 stage, 11 mock; drills 35 (oa 8); bank 200; hours 3,265 stored, 3,695 summed.

Task: PLAN 2c item 6, holdout and resit integrity (F05.6, .7). The freeze is lifted (items 1 to 5 ticked), but 2c items still run before 2a expansion.

Context not in state files:
- `mock-oa-code` passes at 0.5 and draws one difficulty-3 and one difficulty-4 problem from the 8 `oa` drills the library lists. Either hide a holdout pack until sat, or draw unseen-first by solved state, with a "previously seen" label.
- Mocks with fixed versions: check every version is named in `prep.json`.
- The pass mark must match the curriculum's criterion (two problems in 60 minutes). The file must say whether the mark is illustrative.
- The mock engine is `app/js/screens/exam.js`. The drill solved state lives in `state.js`.
- Open user decision before more pilots: review-perf-pilots Q1, the proof L3 task gating met (DECISIONS "Performance tasks in force"). Ask once; do not act on it unasked.
- New levels need a performance task where the verb rule matches. Prune with `node app/tools/perf-pending.mjs --prune` after each merge.
- Local CDN: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`. Merge with `app/tools/merge-wave.sh`. Renumber clashing ENGINE-BACKLOG items by hand: the script leaves that file unresolved.

Steps: one engine-dev in place for the engine part; the main session runs any content script, for example `pass` or `prep.json` edits.

Files: `app/js/screens/exam.js`, `app/js/state.js`, `app/tools/playthrough.mjs`, a node test under `app/tools/`, `app/content/exams/mock-oa-code*.json` and `app/content/prep.json` (by script), `docs/AUTHORING.md` section 5.

Acceptance:
- A learner who has verified all 8 `oa` drills sees "previously seen" on the mock.
- Sitting it twice never repeats a problem while the pool allows.
- Validator shows 0 errors; readiness-sums exits 0.
- `--exam mock-oa-code --local-cdn` and `--routes-only --local-cdn` are green with and without `--mobile`.
- Next prompt: item 7.
