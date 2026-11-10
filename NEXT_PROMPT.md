Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only: work detached at its origin, push `HEAD:` to it, rebase on divergence, never reset. Build the local CDN in the background first: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`. Build the venv (Python 3.12, Pyodide 0.27.7 versions): `uv venv -p /usr/bin/python3.12 <scratchpad>/venv && uv pip install -p <scratchpad>/venv/bin/python numpy==2.0.2 pandas==2.2.3 matplotlib==3.8.4 pytest==8.1.1 scikit-learn==1.6.1 scipy statsmodels sympy mpmath`. Run long jobs with `setsid nohup`, shards in a separate worktree (a full four-shard run takes about an hour). `tools/test-*` take `--local-cdn <pkgs>`; run them in batches.

Expected census: lessons 1,214; levels 279; reviews 279 (items 2,519); exams 29 topic, 4 stage, 16 mock; drills 95 (dsa 60, oa 8); Fluency sets 46 (families 141); bank 200; hours 3,695, gap 0; edges 261; readiness-sums OK; validator 0 errors.

Merge `origin/claude/fable-audit` at start and close, and replay the files it changed. Agent briefs end "start nothing in the background; hand back once". Next, PLAN 2d in order:
1. Fluency widening pass (list in PLAN 2d; formats now exist, AUTHORING 16): skipped and narrowed families, the `ln` and `sin` approximations in exp-log and trig, `multivar/fluency-l2-slicing`. Then the second wave: topics 0.1, 1.4, 1.5, 1.6, 1.11 (brief pattern `docs/briefs/fluency.md`).
2. Content edit: the 18 text-mode `accept` entries that still do not parse (`docs/reports/engine-835.md`).
3. D drills: Phase 4 packs, developer first (`docs/briefs/interview-plan.md` line 202; pattern `docs/briefs/drills-1.8.md`), then 1.1 and 1.9. Add the planted-wrong-solution check as a tool before the wave (KNOWN_ISSUES, protocol 6).
4. M chained problems: brief first, then topics 1.5, 1.3, 0.2, 0.3.
5. Syllabus-hole briefs (four new levels); `course.json` edits by the main session.
6. Bank part 2.

Do not raise the pilot. Acceptance: validator 0 errors, readiness-sums OK, all `tools/test-*`, four shards and routes green at the final HEAD, state files, NEXT_PROMPT for session AA.
