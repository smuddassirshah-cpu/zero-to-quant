Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 2a, phase 0, "mental-pressure L2". One `content-author` agent writes it from `## Level 2` of `docs/briefs/mental-pressure.md`. If there is room, run "puzzles L2" in parallel, then "recruiting L2".

Context not in the state files:
- Task 2a (interview readiness) is the user's priority. Plan: `docs/briefs/interview-plan.md`, with the user's decisions at its end (UK first; trader, then researcher; no audio).
- Read each course's level-1 files for voice. From puzzles L2 on, add follow-up screens, a pace, and `tags` on drill and homework items.
- Name firms only in `recruiting` l4 and in mock exam descriptions.
- `longform` is allowed in homework and exams only.
- Engine limits:
  - `derive` takes expression, order or choice only.
  - `expression` samples six seeded points.
  - 4-column tables scroll at 390 px.
  - `place` allows one slot per chip.
  - Set `shuffle: true` on choices.
- Mock exams (`exams/mock-*.json`, items 450 to 454) support net scoring, forward-only papers, generated arithmetic and timed sets (see AUTHORING sections 5 and 7, and `exams/mock-sample.json`).
- Scratchpad: give each agent a subfolder. The local CDN is `<scratchpad>/pkgs`; build it with `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs` if missing. Agents write their own reports, except for `analysis`.
- If validator errors appear while agents are writing, re-run once before treating them as real.

Files likely touched: `app/content/courses/mental-pressure/` level-2 lessons, `review-2`, `homework-2`; `docs/reports/mental-pressure-2.md`; `docs/BACKLOG-INBOX.md`; the state files.

Acceptance, from `app/`:
- `node tools/validate.mjs 2>&1 | tail -5` shows 0 errors.
- `node tools/playthrough.mjs --lesson mental-pressure/<id> --local-cdn <pkgs>` passes for each level-2 lesson.
- `--set mental-pressure/review-2` and `--set mental-pressure/homework-2` pass.
- The report exists, and every number is computed twice.
- PLAN.md ticks mental-pressure L2 in tasks 2a and 3.
- NEXT_PROMPT.md names the next phase-0 item.
