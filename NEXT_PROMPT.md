Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 2a, phase 0, "mental-pressure L2". One content level, written by one `content-author` agent from `## Level 2` of `docs/briefs/mental-pressure.md`. If the session has room, run "puzzles L2" (`## Level 2` of `docs/briefs/puzzles.md`) in parallel, then "recruiting L2".

Context not in the state files:
- Task 2a (interview readiness) is the user's priority. Its plan is `docs/briefs/interview-plan.md`; the user's decisions are at its end (UK first, trader then researcher tracks, no audio recording). Pure maths levels in 2b wait.
- Read the level-1 files of each course for notation and voice. For puzzles from L2 on, add follow-up screens, a pace, and `tags` per drill and homework item, as the brief says.
- Firm names appear only in `recruiting` l4 and mock exam descriptions; elsewhere write "some trading firms" or "banks".
- `longform` is allowed only in homework and exams.
- Engine limits: `derive` takes only expression, order or choice; `expression` samples six seeded points; tables of 4 or more columns scroll at 390 px; in `place`, one slot per chip; set `shuffle: true`; `playthrough --mobile` shows only the viewport.
- Mock exams (`exams/mock-*.json`, items 450 to 454) now support net scoring, forward-only papers, generated arithmetic items and timed sets. See AUTHORING sections 5 and 7, and `exams/mock-sample.json`.
- Scratchpad: give each agent its own subfolder. The local CDN is `<scratchpad>/pkgs`; build it with `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs` if it is missing. Agents write their own reports, except for the `analysis` course.
- Main-session acceptance script pattern: validate, then every lesson and both sets with `--local-cdn`. Re-run once if validator errors appear while other agents are writing.

Files likely touched: `app/content/courses/mental-pressure/l5-*` onwards, `review-2`, `homework-2` (and the puzzles and recruiting equivalents), `docs/reports/mental-pressure-2.md`, `docs/BACKLOG-INBOX.md`, state files.

Acceptance: from `app/`, `node tools/validate.mjs 2>&1 | tail -5` shows 0 errors. `node tools/playthrough.mjs --lesson mental-pressure/<id> --local-cdn <pkgs>` passes for every level-2 lesson, and `--set mental-pressure/review-2` and `--set mental-pressure/homework-2` pass. The report exists, and every stated number is computed twice. PLAN.md ticks mental-pressure L2 in task 2a and task 3. NEXT_PROMPT.md names the next unchecked phase 0 item.
