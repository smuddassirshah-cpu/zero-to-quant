Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only: work detached at its origin, push `HEAD:` to it, rebase on divergence, never reset. Build the local CDN in the background first: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`. Build the venv (Python 3.12, Pyodide 0.27.7 versions): `uv venv -p /usr/bin/python3.12 <scratchpad>/venv && uv pip install -p <scratchpad>/venv/bin/python numpy==2.0.2 pandas==2.2.3 matplotlib==3.8.4 pytest==8.1.1 scikit-learn==1.6.1 scipy statsmodels sympy mpmath`. Run long jobs with `setsid nohup`, shards in a separate worktree. `--all` does not play drills or Fluency sets: acceptance also runs `--drills` and `--fluency-all`. One browser job per agent: two at once ran the machine out of memory.

Expected census: lessons 1,214; levels 279; reviews 279 (items 2,519); exams 29 topic, 4 stage, 16 mock; drills 210 (dsa 60, ci 70, py 30, cpp 25, oa 8); Fluency sets 83 (families 257); problem sets 22 (items 88); bank 200; hours 3,695, gap 0; edges 261; readiness-sums OK; validator 0 errors.

Merge `origin/claude/fable-audit` at start and close and replay the files it changed. Agent briefs end "start nothing in the background; hand back once" and "do not commit `manifest.json`"; `engine-dev` and some `test-fixer` agents cannot commit, so the main session commits in their worktrees. At most four agents at once. Next, PLAN 2d in order:
1. Delta reads still owed: fix passes of `docs/reviews/review-drills-cpp.md`, `review-drills-py.md` and `review-problems-1.5-d.md` (pattern `docs/reviews/review-delta-session-z.md`).
2. M chained problems, brief `docs/briefs/chained.md`: topic 1.3 (`limits`, `integrals`, `taylor`, `multivar`), then 0.2, then 0.3; one agent a course, three levels, second read and fix per batch (pattern `review-problems-1.5-c.md`).
3. Engine pass on the drill page limits and the constraints rule (KNOWN_ISSUES session Z; number the inbox bullets first).
4. Syllabus-hole briefs (four new levels); `course.json` edits by the main session.
5. Drill packs 5 to 8 (`docs/briefs/drills-ci-packs.md` pattern, `planted` required).
6. Bank part 2.

Do not raise the pilot. Acceptance: validator 0 errors, readiness-sums OK, all `tools/test-*`, four shards, `--drills`, `--fluency-all`, routes green at the final HEAD, state files, NEXT_PROMPT for session AB.
