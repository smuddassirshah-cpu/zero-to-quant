Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; `git pull --rebase` first.

Expected census (`node app/tools/census.mjs | tail -20`): lessons 1054 of 1214 (193, 507, 150, 204); reviews 243, with own pass 243; exams 22 topic, 1 stage, 11 mock; drills 35 (oa 8); bank 200; hours 3,265 stored, 3,695 summed.

Task: PLAN 2c items 7, 10 and 11, plus the playthrough shard fix. In order; past half the usage window, finish the step in flight and record the stop.

Ask the user once, at the start: (a) are `odes` and `numerics` written before 2b; (b) who reviews capstones (item 8); (c) who is the maths second reader (item 9).

1. Wave 1, two engine-devs in worktrees, merged with `app/tools/merge-wave.sh`:
   - Playthrough: `--shard i/n` and a browser relaunch on close (playthrough.mjs only; inbox "session P").
   - Item 7 engine: `why` schema (plain strings stay valid), validator rule, "route limited: X unwritten" on Learn and Prepare, closure tool.
2. Item 7 content: one Sonnet agent drafts `why` for the 248 cross-course edges into a proposal JSON. The main session reviews and applies it by script; indefensible edges are cut or become diagnostics. Report `docs/reports/closure-item7.md`: trader closure before and after.
3. Wave 2, one engine-dev (both touch hours and Learn): item 10 `session` field and validator warning, pattern written down; item 11 one hours function from `readiness.json`, stage `hours` derived. Main session runs content scripts.
4. Close: `--all --shard i/4 --local-cdn` as four background runs; then `--routes-only --mobile`.

Acceptance: each item's line in PLAN 2c; validator 0 errors; readiness-sums exits 0. After item 11, stored hours equal summed hours; lessons unchanged.

After each merge: `node app/tools/perf-pending.mjs --prune`; renumber clashing ENGINE-BACKLOG items by hand. Local CDN: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`.

Next prompt: item 8 if a reviewer is named, else item 9's candidate list.
