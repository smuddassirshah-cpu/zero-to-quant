# CLAUDE.md

## Stack
- Static vanilla JS app in `app/` (no build step). Content is JSON in `app/content/courses/<course>/` and `app/content/exams/`. Engine in `app/js/`, canvases in `app/js/engine/canvas/`, widgets in `app/js/engine/widgets/`.
- Python runs in Pyodide 0.27.7 (NumPy, pandas, SciPy, scikit-learn 1.6.1, statsmodels, matplotlib, pytest); C++ in YoWASP clang 21 (WebAssembly, libc++, `-O1`, no exceptions). Both load from jsDelivr; local copies for sandboxes live in the scratchpad `pkgs` folder named in `docs/LEVEL-BRIEF.md`.
- State files at the repo root: `PLAN.md` (task checklist), `PROGRESS.md`, `DECISIONS.md`, `KNOWN_ISSUES.md`, `NEXT_PROMPT.md`. Design documents: `docs/PLAN.md` (product design), `docs/AUTHORING.md` (content schema and voice, binding), `docs/LEVEL-BRIEF.md` (how a level is authored and reported), `docs/curriculum.md`, `docs/ENGINE-BACKLOG.md`, `docs/BACKLOG-INBOX.md`, `docs/briefs/`, `docs/reports/`, `docs/reviews/`.

## Commands
- Serve: `app/run.sh` then open `http://localhost:8080` in Chrome.
- Validate content (run from `app/`): `node tools/validate.mjs 2>&1 | tail -5` (0 errors required; it rewrites `content/manifest.json`).
- Play through (run from `app/`): `node tools/playthrough.mjs --lesson <course>/<id> | --set <course>/<id> | --exam <id> | --all [--changed] [--mobile] [--why] [--local-cdn <pkgs>] 2>&1 | tail -30`. `--changed` replays only items whose content or engine hash differs from the last green run.
- Grading without a browser (run from `app/`): `node tools/grade-all.mjs [--file <path>] --local-cdn <pkgs>`. Validator tests run on `tools/fixtures/mini-app` and take under five minutes together.
- Number scripts (run from `app/`): `node tools/run-number-scripts.mjs [--only <paths>] [--changed]` with the venv Python; CI job `number-scripts` runs them all. Reuse: `node tools/fresh-check.mjs --file <path>` (same-course mode on problem sets; waivers in `tools/same-course-waivers.json`).
- CI: `.github/workflows/acceptance.yml` runs the full acceptance on every push; see `docs/CI.md`.
- Progress count: see the Python snippet in `PROGRESS.md` history or count `l*.json` against `course.json` maps.

## Conventions
- Git: develop only on `claude/amazing-wright-d4mx7i`; push with `git push -u origin claude/amazing-wright-d4mx7i`; never open a pull request unless asked; commit messages end with the attribution lines the session provides.
- One course per content agent, up to three levels, each from its section in `docs/briefs/<course>.md` (SESSION PROTOCOL 3, DECISIONS "Operating model"); per level the agent follows `docs/LEVEL-BRIEF.md` and reports to `docs/reports/<course>-<level>.md` plus `docs/BACKLOG-INBOX.md`, handing back at most six lines. Content agents never edit engine files, `course.json`, or other levels' files.
- Engine agents never edit content; they number inbox bullets into `docs/ENGINE-BACKLOG.md` and document author-facing changes in `docs/AUTHORING.md` and the canvas READMEs.
- Second readers write `docs/reviews/review-<topic>.md`; fix agents append `## Fix pass` there. Pattern: `docs/reviews/review-1.5.md`.
- Voice: British English, no exclamation marks, no em-dashes, sentences aim for under 20 words (a target, not a gate: never cut a sentence where it would weaken the teaching; the gate is 35 words, `voice-scan.py 35`), explanations of at most three sentences, £ for money. Every stated number computed twice. Every code solution passes its hidden tests and the starter fails them.
- Never rename or remove an existing lesson id (progress data keys on it); add levels instead.
- Models: implementation and test-fixing subagents run on Sonnet, search and exploration on Haiku (see `.claude/agents/`). The main session plans and reviews only.

## SESSION PROTOCOL
1. Start: run `node app/tools/census.mjs | tail -20`, then read NEXT_PROMPT.md, PLAN.md, DECISIONS.md, KNOWN_ISSUES.md. If the census disagrees with PLAN or PROGRESS, fix the state files first and record the drift in KNOWN_ISSUES.
2. Work the next unchecked task in PLAN.md. Course-correction (2c) tasks run before any content expansion until 2c items 1 to 5 are ticked.
3. Waves: three or four agents, each in its own worktree, each owning one course for up to three levels, committing per level with the level in the message. Start a wave only with more than half the usage window left. Merge with `app/tools/merge-wave.sh`; read its tail only.
4. A level is handed to a second reader only with: validator 0 errors, voice scan 0 and 0, a committed number-recompute script that passes, playthrough green with and without `--mobile`. Otherwise it goes back to its author.
5. Check chain per level: author self-check (the author plays its own files), one second read that runs the author's script and `grade-all.mjs --file`, with no browser, one fix pass on Sonnet that plays only the files it edits. Engine agents run the tests they touched. No separate answer-check pass. Nobody replays an unchanged file locally.
6. Any finding class seen three times in docs/reviews becomes a validator rule or script before the next wave; raise it as an engine item.
7. Stay thin: never read large files, logs or full output. Reports under 200 words; detail to files.
8. Acceptance at the final HEAD: validator 0 errors, `playthrough.mjs --changed` on what the session touched, and a green run of `.github/workflows/acceptance.yml` on the pushed HEAD (`docs/CI.md`). No local full `--all`.
9. Before ending: commit, tick PLAN, one PROGRESS line dated from `git log`, record decisions and issues.
10. Last: write NEXT_PROMPT.md (exact next task, context not in state files, files to touch, acceptance check, expected census figures; under 300 words) and print it in full.
