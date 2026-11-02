Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 2a, order items 1 and 2. Full standards apply (DECISIONS "Standards restored"): no lean rules.
- If ENGINE-BACKLOG 455 (prep tags) is not ticked, an `engine-dev` agent finishes it from `docs/briefs/prep-tags.md` and `docs/reports/engine-prep-tags.md` first.
- Then, in parallel, each agent with its own scratchpad subfolder:
  - `content-author`: prep tags mapping, `docs/briefs/prep-tags.md` section "Mapping" (edits only `app/content/prep.json`).
  - `content-author`: recruiting L3 from `## Level 3` of `docs/briefs/recruiting.md`.
  - A brief agent: the game-theory brief, every level, in the pattern of `docs/briefs/brainteasers.md`, from `course.json`, `docs/briefs/interview-plan.md` and `interview-gaps.md`.
- After recruiting L3 is green: exam topic-0.7 (pattern `exams/topic-1.7.json`, brief pattern `docs/reports/exam-1.8.md`), then a second reader (`docs/reviews/review-0.7.md`, pattern `review-1.5.md`) and a fix pass.
- End with an answer-check agent that recomputes every keyed answer in the session's new files.

Context not in the state files:
- From puzzles L2 on: follow-up screens, a pace, `tags` on drill and homework items. Name firms only in recruiting l4, mock descriptions and `prep.json`. `longform` in homework and exams only.
- Engine limits: `derive` takes expression, order or choice only; `expression` samples six seeded points; 4-column tables scroll at 390 px; `place` allows one slot per chip; `shuffle: true` on choices.
- Local CDN: `<scratchpad>/pkgs`; build with `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs` if missing. Re-run a validator error once while agents write.

Acceptance, from `app/`: `node tools/validate.mjs 2>&1 | tail -5` 0 errors; playthrough passes for every new lesson (`--lesson`, `--local-cdn`, and `--mobile`), each new set (`--set`), `--exam topic-0.7` and `--routes-only`; reports and review exist; PLAN ticks each item; NEXT_PROMPT.md names the next order item.
