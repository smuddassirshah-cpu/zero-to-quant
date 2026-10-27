Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 2b, fourth item: briefs for the 2.5, 2.6, 3.2 additions and 3.4 courses. Seven courses: `numerics`, `convex` (2.5), `stat-models` (2.6), `measure-prob`, `pdes` (3.2), `algebra`, `topology` (3.4, optional).

Do: launch one brief-writer agent per course (Opus, `general-purpose`), in parallel, planning only, no commits. Each reads its course section of `docs/briefs/breadth-plan.md` (levels, lesson ids, titles, objectives, builds-on lessons), `app/content/courses/<course>/course.json`, its item in `docs/curriculum.md`, `docs/briefs/EXAMPLE.md`, one finished breadth brief as a model (`docs/briefs/odes.md` for quant courses, `docs/briefs/linear-maps.md` for pure), and `docs/AUTHORING.md` as needed. It writes `docs/briefs/<course>.md` with one `## Level n` section per level. Every number is computed twice (hand or closed form plus Python in its own scratchpad subfolder `brief-<course>`). Each level section names this session's scratchpad, a `<course>-<n>` subfolder, and `--local-cdn <scratchpad>/pkgs` (built with `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`). Pure courses (`algebra`, `topology`) grade proofs step by step (`order`, `choice`, fill-ins, `longform`); the brief says which widget grades each step. `numerics` l13 states the Black-Scholes equation, cites `trees` l10, and defers the derivation to `ito` l9. Hand-backs under 200 words; add their engine limits to `docs/BACKLOG-INBOX.md` yourself.

Context not in state files: an acceptance script from the last session checked ids, `## Level n` sections and em-dashes; rewrite it (about 25 lines of Python over `course.json` `levels[].n` and `levels[].lessons`). Sandbox CPython lacks SciPy; agents install it with `pip --target` into their scratchpad.

Files likely touched: `docs/briefs/numerics.md`, `convex.md`, `stat-models.md`, `measure-prob.md`, `pdes.md`, `algebra.md`, `topology.md`, `docs/BACKLOG-INBOX.md`, PLAN.md, state files.

Acceptance:
- Seven brief files exist, each with one `## Level n` section per level in `breadth-plan.md`, every lesson id matching its `course.json`, no em-dashes.
- `git diff app/` is empty; from `app/`, `node tools/validate.mjs 2>&1 | tail -5` reports 0 errors.
- PLAN.md ticks the item; NEXT_PROMPT.md names proof L1 as the next task.
