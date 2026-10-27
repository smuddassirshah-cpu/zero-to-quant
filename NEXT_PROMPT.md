Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 2b, first item: the breadth plan. The user asked (27 Oct) for the maths breadth pass to run before the rest of Stage 3; momentum-rep L1 is done, and L2 waits until task 2b is complete.

Context: `docs/curriculum.md` now has new items 0.6 (proof), 1.10 (analysis, proof-based linear algebra), 1.11 (complex numbers, vector calculus, ODEs), 2.5 (numerical methods, optimisation), 2.6 (statistical modelling), additions to 3.2 (measure theory, PDEs), 3.4 (algebra, topology), and a 1.5 gap level for markov (Poisson process, martingales, optional stopping). Each item is tagged [Quant] or [Pure maths]. The previous gap pass is the pattern: `docs/briefs/gaps-plan.md`. Topics shown in the app: `app/content/curriculum.json`.

Do:
1. Launch one Sonnet agent (`general-purpose` or `content-author`, planning only). It writes `docs/briefs/breadth-plan.md`: for each course, the levels, lesson ids, titles, objectives, prerequisites and the existing lessons each one builds on. It writes the new `course.json` maps, each with `strand` ("quant" or "pure") and `strandNote`, plus the topic entries in `app/content/curriculum.json`, and appends the markov gap level to `markov/course.json` without renaming any id. It writes no lessons and does not commit.
2. Replace the "Levels: placeholder" line in PLAN.md task 2b with one line per level, each marked [Quant] or [Pure maths], ordered Stage 0, then 1, 2, 3.

Files likely touched: `docs/briefs/breadth-plan.md`, `app/content/courses/<new>/course.json`, `app/content/courses/markov/course.json`, `app/content/curriculum.json`, `app/content/manifest.json`, PLAN.md, state files.

Acceptance:
- From `app/`, `node tools/validate.mjs 2>&1 | tail -5` reports 0 errors. New lessons show as "not yet written". If it rejects `strand`, note it for the engine item and keep the field.
- No existing lesson id changes (`git diff` on existing course.json files shows additions only).
- PLAN.md ticks the breadth plan and lists every level; NEXT_PROMPT.md names the engine item of task 2b.
