Read CLAUDE.md and the four state files; follow the SESSION PROTOCOL. Full standards apply (DECISIONS "Standards restored").

Task: PLAN.md 2a order item 5 (topic 3.5), part one: briefs for `research-int`, `coding-int` and `systems`, all levels.

Steps (own scratchpad subfolder each; checkpoint-commit as each brief lands):
1. In parallel, three agents (Sonnet), one brief each: `docs/briefs/research-int.md`, `coding-int.md`, `systems.md`. Sources, binding: `docs/briefs/interview-plan.md` section (b) for that course (levels, lessons, engine needs), `docs/briefs/interview-gaps.md`, the course map `app/content/courses/<course>/course.json`, `docs/LEVEL-BRIEF.md`, `docs/AUTHORING.md`. Pattern: `docs/briefs/game-theory.md` (section per level `## Level n`, lesson ids from course.json, objectives, numbers computed twice, the existing lessons each builds on, review and homework items). Each brief names the engine features its levels need (pass C: E3, E8, E11, E14; E13 for systems), with no fallbacks.
2. A second reader checks the three briefs against interview-plan (b), the course maps and LEVEL-BRIEF. A fixer applies the findings.
3. From the briefs, write the engine pass C scope into PLAN.md 2a item 5 (which E items, in what order, before which levels), splitting the item if needed.
4. Tick the phase 2 briefs line for research-int, coding-int and systems.

Context: firm-neutral content; UK first; trader and researcher tracks first; no audio. `playthrough.mjs --bank <file>|all` now exists (ENGINE-BACKLOG 462). Build the local CDN (`bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`) only if an author checks code.

Files likely touched: `docs/briefs/research-int.md`, `coding-int.md`, `systems.md`, `docs/reviews/review-briefs-3.5.md`, `docs/BACKLOG-INBOX.md`, `PLAN.md`, state files.

Acceptance: three briefs exist, one section per course.json level, every lesson id matches its course map; every number in them is computed twice; review file with a fix pass; from `app/`, `node tools/validate.mjs 2>&1 | tail -5` still 0 errors; PLAN ticks. Next after that: engine pass C, then the topic 3.5 levels.
