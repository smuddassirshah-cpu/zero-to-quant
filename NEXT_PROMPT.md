Read CLAUDE.md and the four state files; follow the SESSION PROTOCOL. Full standards apply (DECISIONS "Standards restored").

Task: PLAN.md 2a order item 4 (topic 3.3), first part, plus fix pass 1.9 left from task 5.

Steps (own scratchpad subfolder per agent; checkpoint-commit as items turn green):
1. In parallel:
   - `engine-dev`: engine pass B, E7 (question bank with item spacing) and E9 (per-item timing), from their bullets in `docs/BACKLOG-INBOX.md`; number them from 456 in `docs/ENGINE-BACKLOG.md`, document in AUTHORING, report to `docs/reports/engine-pass-b.md`.
   - Four `content-author`s: mental-pressure L4, puzzles L4, brainteasers L1, mm-games L2, each from its brief's `## Level n`.
   - A `test-fixer`: fix pass 1.9 from `docs/reviews/review-1.9.md` (append `## Fix pass`), then a voice pass on cpp and cpp-pricing with `docs/reviews/voice-scan.py` (0 and 0).
2. After pass B is green: `engine-dev` engine pass D, E12 (trading-game widget); then revise the `## Level 3` and `## Level 4` sections of `docs/briefs/mm-games.md` to use the widget instead of scripts.
3. An answer-check agent recomputes every keyed answer in this session's new files (pattern `docs/reviews/answers-2026-11-03.md`); a fixer fixes mismatches.

Context: follow-up screens, a pace, `tags` on drill and homework items; firms only in recruiting l4, mocks and `prep.json`; `longform` in homework and exams only; `derive` takes expression, order or choice; `expression` samples six points; 4-column tables scroll at 390 px; `place` allows one slot per chip; `shuffle: true` on choices. Every new file passes `voice-scan.py`; re-run a validator error once during engine work. Local CDN: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`.

Acceptance, from `app/`: validate 0 errors; new lessons green with and without `--mobile`, new sets with `--set`; topic 1.9 courses and exam green after the fixes; `--routes-only` and the full `--all` run green after both engine passes; reports exist; PLAN ticks each item. NEXT_PROMPT names mental-pressure's close (mock-oa-arith), puzzles L5 and the next 3.3 levels.
