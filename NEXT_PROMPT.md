Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only: work detached at its origin, push `HEAD:` to it, rebase on divergence, never reset. Build the local CDN in the background first: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`. Build the venv (Python 3.12, Pyodide 0.27.7 versions): `uv venv -p /usr/bin/python3.12 <scratchpad>/venv && uv pip install -p <scratchpad>/venv/bin/python numpy==2.0.2 pandas==2.2.3 matplotlib==3.8.4 pytest==8.1.1 scikit-learn==1.6.1 scipy statsmodels sympy mpmath`. Run long jobs with `setsid nohup`, shards in a separate worktree. Six `tools/test-*` need `--local-cdn <pkgs>`.

Expected census: lessons 1,214; levels 279; reviews 279; exams 29 topic, 4 stage, 16 mock; drills 35 (oa 8); bank 200; hours 3,695, gap 0; edges 261; readiness-sums OK; validator 0 errors; perf-pending 0.

Read `docs/reviews/critical-review-fable-5-2.md` and `docs/reviews/critical-review-fable-5-2/self-containment-gaps.md`. Next, in order:
1. Fable audit resumes (user, 9 Nov): re-enable `trig_01FJuNVhosR68kSj3RhYkXrp`, tick PLAN 5b, record in DECISIONS. Order by route use: `mm-games`, `recruiting`, topic 1.5, then other trader and developer closure courses; optional Stage 2 and 3 last. Merge `origin/claude/fable-audit` at start and close.
2. Engine agent: number the session X inbox from 705; then G (generator framework with typed and expression answers, Fluency sets) and C (cumulative review due on Today); in-app hours shown apart from outside hours.
3. Add the gap file's additions (G, R, M, C, A, P, D) to PLAN in its order of work; ask the user.
4. Content: G families for topics 0.2, 0.3 and 1.3; D drills for topic 1.8, then Phase 4 packs (developer first).
5. Re-author `mock-oa-sig-2` and `-3` on new templates; check the trader versions for the same fault.
6. Ask the user for the review-size route. The pilot stays post-completion (user, 9 Nov): do not raise it.

Acceptance: validator 0 errors, readiness-sums OK, all `tools/test-*`, four shards and routes green at the final HEAD, state files, NEXT_PROMPT for session Z.
