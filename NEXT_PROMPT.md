Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md. Full standards apply (DECISIONS "Standards restored").

Task: PLAN.md task 2a, order item 2 (topic 0.7), plus the game-theory brief from item 4.

Another session is finishing the prep tags engine pass (ENGINE-BACKLOG 455) and will then write `app/content/prep.json`. Do not touch `app/js/`, `app/css/`, `app/tools/`, `app/index.html`, `app/content/prep.json`, `docs/briefs/prep-tags.md` or `docs/ENGINE-BACKLOG.md`. Before every push run `git pull --rebase origin claude/amazing-wright-d4mx7i`; on a `manifest.json` conflict take either side and re-run the validator.

Steps, each agent with its own scratchpad subfolder:
1. In parallel: a `content-author` writes recruiting L3 from `## Level 3` of `docs/briefs/recruiting.md`; a brief agent writes `docs/briefs/game-theory.md`, every level, in the pattern of `docs/briefs/brainteasers.md`, from `course.json`, `docs/briefs/interview-plan.md` and `interview-gaps.md`.
2. After recruiting L3 is green and committed: exam topic-0.7 (pattern `exams/topic-1.7.json`, brief pattern `docs/reports/exam-1.8.md`).
3. A second reader writes `docs/reviews/review-0.7.md` (pattern `review-1.5.md`): answers, grading of alternative correct forms and wrong answers, layout. A `test-fixer` appends `## Fix pass`.
4. An answer-check agent recomputes every keyed answer in the session's new files; mismatches go to a fix agent.

Context: from puzzles L2 on, follow-up screens, a pace, `tags` on drill and homework items. Firms only in recruiting l4, mock descriptions and `prep.json`. `longform` in homework and exams only. `derive` takes expression, order or choice; `expression` samples six seeded points; 4-column tables scroll at 390 px; `place` allows one slot per chip; `shuffle: true` on choices. Local CDN: `<scratchpad>/pkgs`, built with `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`.

Acceptance, from `app/`: validate 0 errors; playthrough passes for every new recruiting lesson (`--local-cdn`, and `--mobile`), `--set` for review-3 and homework-3, `--exam topic-0.7`; report, brief and review exist; PLAN ticks recruiting L3 and topic 0.7; NEXT_PROMPT.md names order item 3 (second reads of 0.5, 1.8, 2.1) with topic 3.3's first levels.
