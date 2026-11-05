Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; `git pull --rebase` first.

Expected census (`node app/tools/census.mjs | tail -20`): lessons 1054 of 1214 (193, 507, 150, 204); reviews 243, with own pass 243; exams 22 topic, 1 stage, 11 mock; drills 35 (oa 8); bank 200; hours 3,695 stored, 3,695 summed, gap 0.

Task: PLAN 2c item 8, independent capstone (F06, N08). The user is the reviewer. Past half the usage window, finish the step in flight and record the stop.

Ask the user once, at the start: (a) does `complex` L1 join `odes` and `numerics` before 2b (the pdes route reaches it); (b) take the trader lever in `docs/reports/closure-item7.md` (two graphs-dp edges as diagnostics, 465 to 422 lessons) or not; (c) which external capstone each role uses, and whether verified `oa` drills count toward coding-int levels.

1. One engine-dev in a worktree, merged with `app/tools/merge-wave.sh`: a capstone record per role in `content/capstones.json` (repo link, reviewer, date, rerun-from-clean result, defence notes, `external: true`); research route's capstone is `momentum-rep` or an equivalent external project; a validator rule; Today and the readiness summary never show "ready" without an `external` record; a You card to view records (the user fills them). Drill verification feeds the coding met rule if the user says so.
2. Main session writes empty records for the five roles by script.

Acceptance: PLAN 2c item 8 line; a test where a role with every level met but no external record is not "ready"; validator 0 errors; readiness-sums 0; `--routes-only --local-cdn` green with and without `--mobile`.

After each merge: `node app/tools/perf-pending.mjs --prune`. Local CDN: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`. Full runs: `--all --shard i/4 --local-cdn`, four background runs.

Next prompt: item 9's candidate list (user is the maths reader), then the odes and numerics levels.
