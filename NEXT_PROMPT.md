Read CLAUDE.md and the four state files; follow the SESSION PROTOCOL. Full standards apply (DECISIONS "Standards restored"). Prep tags and topic 0.7 are merged; work only on `claude/amazing-wright-d4mx7i`.

Task: PLAN.md 2a order item 3 (second reads and fixes for topics 0.5, 1.8, 2.1), plus mental-pressure L3 and puzzles L3.

Steps (own scratchpad subfolder per agent; checkpoint-commit as items turn green):
1. In parallel:
   - Three second readers write `docs/reviews/review-0.5.md` (`mental`, exam topic-0.5), `review-1.8.md` (algo-think, ds, graphs-dp, topic-1.8) and `review-2.1.md` (stat-learning, validation, fin-ml, ensembles, topic-2.1), pattern `review-0.7.md`: answers, grading of alternative correct forms and wrong answers, layout, voice; code solutions pass hidden tests, starters fail them.
   - Two `content-author` agents write mental-pressure L3 and puzzles L3 from `## Level 3` of their briefs. Where a brief says E1 or E4 is unbuilt, follow AUTHORING (built for mocks only).
2. A `test-fixer` per review appends `## Fix pass`.
3. An answer-check agent recomputes every keyed answer in this session's new files (pattern `docs/reviews/answers-2026-11-02.md`); mismatches go to a fix agent.

Context: follow-up screens, a pace, `tags` on drill and homework items; firms only in recruiting l4, mocks and `prep.json`; `longform` in homework and exams only; `derive` takes expression, order or choice; `expression` samples six points; 4-column tables scroll at 390 px; `place` allows one slot per chip; `shuffle: true` on choices. Local CDN: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`.

Acceptance, from `app/`: validate 0 errors; after the fixes, playthrough green for every course in 0.5, 1.8, 2.1 and their exams (split runs, `--local-cdn`); new lessons green with and without `--mobile`, new sets green with `--set`; `--routes-only` green; three reviews with fix passes and two reports; PLAN ticks order item 3, mental-pressure L3 and puzzles L3. NEXT_PROMPT names engine passes B (E7, E9) and D (E12) with the next 3.3 levels: mental-pressure L4, puzzles L4, brainteasers L1, mm-games L2.
