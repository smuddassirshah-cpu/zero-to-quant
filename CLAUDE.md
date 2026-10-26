# CLAUDE.md

## Stack
- Static vanilla JS app in `app/` (no build step). Content is JSON in `app/content/courses/<course>/` and `app/content/exams/`. Engine in `app/js/`, canvases in `app/js/engine/canvas/`, widgets in `app/js/engine/widgets/`.
- Python runs in Pyodide 0.27.7 (NumPy, pandas, SciPy, scikit-learn 1.6.1, statsmodels, matplotlib, pytest); C++ in YoWASP clang 21 (WebAssembly, libc++, `-O1`, no exceptions). Both load from jsDelivr; local copies for sandboxes live in the scratchpad `pkgs` folder named in `docs/LEVEL-BRIEF.md`.
- State files at the repo root: `PLAN.md` (task checklist), `PROGRESS.md`, `DECISIONS.md`, `KNOWN_ISSUES.md`, `NEXT_PROMPT.md`. Design documents: `docs/PLAN.md` (product design), `docs/AUTHORING.md` (content schema and voice, binding), `docs/LEVEL-BRIEF.md` (how a level is authored and reported), `docs/curriculum.md`, `docs/ENGINE-BACKLOG.md`, `docs/BACKLOG-INBOX.md`, `docs/briefs/`, `docs/reports/`, `docs/reviews/`.

## Commands
- Serve: `app/run.sh` then open `http://localhost:8080` in Chrome.
- Validate content (run from `app/`): `node tools/validate.mjs 2>&1 | tail -5` (0 errors required; it rewrites `content/manifest.json`).
- Play through (run from `app/`): `node tools/playthrough.mjs --lesson <course>/<id> | --set <course>/<id> | --exam <id> | --all [--mobile] [--why] [--local-cdn <pkgs>] 2>&1 | tail -30`.
- Progress count: see the Python snippet in `PROGRESS.md` history or count `l*.json` against `course.json` maps.

## Conventions
- Git: develop only on `claude/amazing-wright-d4mx7i`; push with `git push -u origin claude/amazing-wright-d4mx7i`; never open a pull request unless asked; commit messages end with the attribution lines the session provides.
- One level per content agent, from its section in `docs/briefs/<course>.md`; the agent follows `docs/LEVEL-BRIEF.md` and reports to `docs/reports/<course>-<level>.md` plus `docs/BACKLOG-INBOX.md`, handing back at most six lines. Content agents never edit engine files, `course.json`, or other levels' files.
- Engine agents never edit content; they number inbox bullets into `docs/ENGINE-BACKLOG.md` and document author-facing changes in `docs/AUTHORING.md` and the canvas READMEs.
- Second readers write `docs/reviews/review-<topic>.md`; fix agents append `## Fix pass` there. Pattern: `docs/reviews/review-1.5.md`.
- Voice: British English, no exclamation marks, no em-dashes, sentences under 20 words, explanations of at most three sentences, £ for money. Every stated number computed twice. Every code solution passes its hidden tests and the starter fails them.
- Never rename or remove an existing lesson id (progress data keys on it); add levels instead.
- Models: implementation and test-fixing subagents run on Sonnet, search and exploration on Haiku (see `.claude/agents/`). The main session plans and reviews only.

## SESSION PROTOCOL
1. Start: read only PLAN.md, PROGRESS.md, DECISIONS.md, KNOWN_ISSUES.md. Do not read the whole codebase.
2. Work on the next unchecked task in PLAN.md, one task per session. If a task is too big, split it in PLAN.md and do the first part.
3. Stay thin as orchestrator: never read large files, logs or full test output yourself. Delegate to subagents and require their reports to be under 200 words, with detail written to files if needed.
4. Run tests and builds with quiet flags or pipe through tail -50. Never dump full output into context.
5. Before ending: commit the work, tick the task in PLAN.md, add one line to PROGRESS.md, record any new decisions or issues. If all tasks are done, create a file named DONE.
6. Final step every session: write NEXT_PROMPT.md, a self-contained prompt for the next fresh session. It must name the exact next task, any context it needs that is not in the state files, files likely to be touched, and the acceptance check. Under 300 words. Then print the full contents of NEXT_PROMPT.md as your last message so I can paste it manually if needed.
