Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 2b, third item: briefs for the 0.6, 1.10 and 1.11 courses and the markov gap level. Six courses: `proof`, `analysis`, `linear-maps`, `complex`, `vector-calc`, `odes`, plus markov L5 (martingales and optional stopping; the Poisson process is already markov l16).

Do: launch one brief-writer agent per course (Sonnet, `general-purpose`), in parallel, planning only, no commits. Each reads `docs/briefs/breadth-plan.md` (its course section: levels, lesson ids, titles, objectives, prerequisites, builds-on lessons), the course's `app/content/courses/<course>/course.json`, its item in `docs/curriculum.md`, `docs/briefs/EXAMPLE.md` (the brief pattern) and `docs/AUTHORING.md` as needed. It writes `docs/briefs/<course>.md` with a `## Level n` section per level. Markov L5 goes in a new `docs/briefs/gap-markov-2.md` (do not edit `gap-markov.md`). Every number in a brief is computed twice. Briefs name the current paths: scratchpad `/tmp/claude-0/-home-user-zero-to-quant/<session>/scratchpad` and its `pkgs` folder (built with `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`); give agents this session's scratchpad path. Pure courses (`proof`, `analysis`, `linear-maps`, `vector-calc`) teach proof by guided steps, ordering, and fill-in widgets, since free-form proofs are not gradable; the brief says which widget grades each step. Hand-backs under 200 words each.

Context not in state files: the engine item is done (`docs/reports/engine-breadth.md`); strand badges and "Quant path only" work; stage hours on Learn are stale (item 428).

Files likely touched: `docs/briefs/proof.md`, `analysis.md`, `linear-maps.md`, `complex.md`, `vector-calc.md`, `odes.md`, `gap-markov-2.md`, PLAN.md, state files.

Acceptance:
- Seven brief files exist, each with one `## Level n` section per level in `breadth-plan.md`, every lesson id matching its `course.json`.
- `git diff app/` is empty (briefs only); from `app/`, `node tools/validate.mjs 2>&1 | tail -5` still reports 0 errors.
- PLAN.md ticks the item; NEXT_PROMPT.md names the briefs item for 2.5, 2.6, 3.2 additions and 3.4.
