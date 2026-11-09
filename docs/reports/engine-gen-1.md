# Engine gen, Agent 1: inbox numbering and in-app hours

Branch `worktree-agent-a1a11dcb55d31d416`. Two commits, one per task. Highest ENGINE-BACKLOG number used: 746 (745 for the inbox, 746 for hours). Agent 2 owns 800 to 829.

## Task 1: inbox numbered, 705 to 745

`docs/BACKLOG-INBOX.md` is never cleared, and the session X triage (7 Nov, items 622 to 697) read everything above it. So "un-numbered" meant the 80 bullets added after that triage (the perf-retrofit bullets, 66 headings). Each is now marked `(numbered n)` in the existing manner, and `docs/ENGINE-BACKLOG.md` carries 41 new items, 705 to 745, all open and none implemented, plus a status block.

- Sightings of items already numbered were marked with that number, not renumbered: 700 (the NaN `isclose` bullets), 701 and 703 (the `-marked` shot bullets), 697 (folded into 718).
- Duplicates were merged, as session X did: for example one `--variant` playthrough item (711) with five sources, one `byKey` item (731) with four.
- Older bullets (before the session X triage) were left as they were. Many carry no mark but were numbered by earlier passes; I did not re-audit them. This is the one judgement call to check.

## Task 2: in-app hours apart from outside hours (item 746)

- `app/js/hours.js`: per lesson, level, course, topic, stage, total and role (`lessonApp` ... `totalApp`, `lessonOut` ... `totalOut`, `roleSums` with `app` and `out`), `splitLabel`, `fmtH`. In-app = authored lesson minutes (14 when not written; workshop and project true minutes), plus each level's review and homework, plus the topic exam shared by lesson weight. Outside = stored less in-app, floored at 0.
- Allowances where files state nothing (none of 280 reviews and 281 homeworks states minutes): review 20 min, homework 45 min, topic exam 60 min if no `examMinutes`. A review or homework with a top-level `minutes` would be used. These are my choice and are stated in AUTHORING 14; they move the in-app figure materially (the trader route is 313 h in the app, not about 150).
- Surfaces: Learn header, stage pills, exit card, topic headings, Paths view; the course page (new `.zc-hours` line); Setup's stage rows; `docs/readiness.md` (tables now "Hours in the app | Hours of outside study", stored columns gone) and `docs/curriculum.md` (map table, topic table, prose and stage headings). `today.js`, `player.js`, `select.js` untouched.
- Validator writes `lessonMinutes` and `setMinutes` to `manifest.json` (about 1,200 lines). `readiness.json` totals gain `hoursInApp` and `hoursOutside`; `readiness-sums.mjs` checks them through its byte comparison and still prints OK. `curriculum-hours.mjs --check` OK.
- `tools/test-hours-split.mjs`: 209 checks (made-up curriculum, real content, the app's `content.js` path against the tools, docs and screens). `playthrough.mjs` routes block now checks Learn's header and each course page read "about N h in the app, about M h of outside study".

Figures: whole path 625 h in the app and 3,111 h of outside study (stored 3,695, topics 3.2 and 3.4 store 0 so the two sum a little over). Trader route: 630 lessons, about 313 h in the app, about 1,492 h of outside study.

## Verification

`validate.mjs` 0 errors; `readiness-sums.mjs` OK; `curriculum-hours.mjs --check` OK; every `tools/test-*` run (see the hand-back for failures); playthrough of three lessons (algebra/l1-symmetries desktop and mobile, conditional/l3-shrinking mobile and desktop) and `--routes-only` desktop and `--mobile` all green.

## Deferred and notes

- Not done: `census.mjs` still prints stored stage hours (a developer consistency check, not a learner surface).
- Quant-only mode keeps the full stage figures, as AUTHORING already said; the split follows the same rule.
- Merge note for Agent 2's branch: `validate.mjs` line writing `manifest.json` (the single long `JSON.stringify` line) and `AUTHORING.md` (my edits are in section 14 only) are the likely conflict spots; `ENGINE-BACKLOG.md` is appended at the end by both (my block ends at 746, theirs starts at 800).
- Slip: one command in this session ran against the main checkout's `docs/curriculum.md`; I reverted it exactly (verified identical to the worktree's committed copy).
