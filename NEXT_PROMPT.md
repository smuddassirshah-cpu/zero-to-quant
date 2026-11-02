Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 2a, phase 0, "mental-pressure L3" ("Test formats": l9-eighty-in-eight, l10-next-in-sequence, l11-word-problems, l12-mock-test, review-3, homework-3). One `content-author` agent writes it from `## Level 3` of `docs/briefs/mental-pressure.md`. Room permitting, run "mental-pressure L4: Assessment batteries" after it (same course, so not in parallel: L4 reads L3's files). The phase-0 mock exams (mock-oa-arith, mock-oa-trader, mock-oa-sig) come after L4; mock-oa-arith reuses l12's seeded generator script.

Context not in the state files:
- Task 2a (interview readiness) is the user's priority. Plan: `docs/briefs/interview-plan.md`, user decisions at its end (UK first; trader, then researcher; no audio).
- Read level-1 and level-2 files for voice. Keep follow-up screens, a pace, and `tags` on drill and homework items.
- Name firms only in `recruiting` l4 and mock exam descriptions; cite a firm's resource by title and firm type.
- `longform` in homework and exams only.
- Engine limits: `derive` takes expression, order or choice only; `expression` samples six seeded points; 4-column tables scroll at 390 px; `place` allows one slot per chip; `shuffle: true` on choices.
- Net scoring, forward-only papers, generated arithmetic and timed sets exist for mock exams only (AUTHORING sections 5 and 7, `exams/mock-sample.json`). Where the L3 brief says E1 or E4 are unbuilt, follow AUTHORING; lessons still cannot net-score the learner's answers.
- The brief's scratchpad subfolder is `mental-pressure-3` under the scratchpad you name. Local CDN: `<scratchpad>/pkgs`; build with `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs` if missing.
- If validator errors appear while agents write, re-run once before treating them as real.

Files likely touched: `app/content/courses/mental-pressure/` level-3 lessons, `review-3`, `homework-3`; `docs/reports/mental-pressure-3.md`; `docs/BACKLOG-INBOX.md`; the state files.

Acceptance, from `app/`:
- `node tools/validate.mjs 2>&1 | tail -5` shows 0 errors.
- `node tools/playthrough.mjs --lesson mental-pressure/<id> --local-cdn <pkgs>` passes for each level-3 lesson; `--set mental-pressure/review-3` and `--set mental-pressure/homework-3` pass.
- The report exists, records l12's generator script and output, and every number is computed twice.
- PLAN.md ticks mental-pressure L3 in tasks 2a and 3.
- NEXT_PROMPT.md names the next phase-0 item.
