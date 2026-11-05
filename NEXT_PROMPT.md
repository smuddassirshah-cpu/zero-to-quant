Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; `git pull --rebase` first.

Expected census (`node app/tools/census.mjs | tail -20`): lessons 1054 of 1214 (193, 507, 150, 204); reviews 243, with own pass 243; exams 22 topic, 1 stage, 11 mock; drills 35 (oa 8); bank 200; hours 3,265 stored, 3,695 summed.

Task: PLAN 2c items 7, 10 and 11, plus the playthrough shard fix. Work in this order; if usage passes half the window, finish the step in flight and record where you stopped.

Ask the user once, at the start, in one question set: (a) are `odes` and `numerics` written before 2b (item 7); (b) who reviews capstones (item 8); (c) who is the maths second reader (item 9). Do not act on them unasked.

1. Wave 1, two engine-devs in worktrees, merged with `app/tools/merge-wave.sh`:
   - Playthrough: `--shard i/n` and a browser relaunch on close (`app/tools/playthrough.mjs` only; inbox bullet "main session P").
   - Item 7 engine: a `why` schema that keeps plain strings valid, a validator rule (error after the fill), "route limited: X unwritten" on Learn and Prepare, a closure tool.
2. Item 7 content: one Sonnet agent drafts `why` for the 248 cross-course edges into a proposal JSON. The main session reviews it, applies it by script, and cuts or converts indefensible edges. Report: `docs/reports/closure-item7.md`, with the trader closure before and after.
3. Wave 2, one engine-dev (both items touch hours and Learn): item 10 `session` field and a validator warning with the matching pattern written down; item 11 one hours function from `readiness.json`, stage `hours` derived, `docs/curriculum.md` quoting it. The main session runs the content scripts.
4. Close: `--all --shard i/4 --local-cdn` as four background runs, then `--routes-only --local-cdn --mobile`.

Acceptance: each item's line in PLAN 2c; validator 0 errors; readiness-sums exits 0. After item 11, stored hours equal summed hours; lesson figures are unchanged.

Local CDN: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`. Prune with `node app/tools/perf-pending.mjs --prune` after each merge; renumber clashing ENGINE-BACKLOG items by hand.

Next prompt: item 8 if a reviewer is named, else item 9's candidate list.
