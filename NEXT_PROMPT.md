Read CLAUDE.md and the four state files; follow the SESSION PROTOCOL. Full standards apply (DECISIONS "Standards restored").

First: if `claude/recruiting-l3-game-theory-nvxp1s` (topic 0.7 and the game-theory brief) is not yet in `claude/amazing-wright-d4mx7i`, run `git pull --rebase origin claude/recruiting-l3-game-theory-nvxp1s` before anything else.

Task: PLAN.md task 2a, order item 3 (second reads and fix passes for topics 0.5, 1.8 and 2.1), plus the first levels of topic 3.3: mental-pressure L3 and puzzles L3.

If the prep tags session is still running, do not touch `app/js/`, `app/css/`, `app/tools/`, `app/index.html`, `app/content/prep.json`, `docs/briefs/prep-tags.md` or `docs/ENGINE-BACKLOG.md`.

Steps, each agent with its own scratchpad subfolder:
1. In parallel: three second readers write `docs/reviews/review-0.5.md` (course `mental` plus exam topic-0.5), `review-1.8.md` (algo-think, ds, graphs-dp plus topic-1.8) and `review-2.1.md` (stat-learning, validation, fin-ml, ensembles plus topic-2.1), pattern `review-0.7.md`: answers, grading of alternative correct forms and of wrong answers, layout, voice. Code screens: the solution passes its hidden tests and the starter fails them. Two `content-author` agents write mental-pressure L3 and puzzles L3 from `## Level 3` of their briefs (where a brief says E1 or E4 is unbuilt, follow AUTHORING: engine pass A built them for mocks only).
2. A `test-fixer` per review appends `## Fix pass`.
3. An answer-check agent recomputes every keyed answer in this session's new files (pattern `docs/reviews/answers-2026-11-02.md`); mismatches go to a fix agent.

Local CDN: build `<scratchpad>/pkgs` with `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`.

Acceptance, from `app/`: validate 0 errors; playthrough green for every course in 0.5, 1.8 and 2.1 after the fixes (lessons, `--sets`, the three exams; split runs, `--local-cdn`); every new lesson green with and without `--mobile`, its review and homework green with `--set`; three reviews with fix passes and two reports exist; PLAN ticks order item 3, mental-pressure L3 and puzzles L3. NEXT_PROMPT names engine pass B (E7, E9) and the next 3.3 levels.
