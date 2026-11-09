Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only: work detached at its origin, push `HEAD:` to it, rebase on divergence, never reset. Build the local CDN in the background first: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`. Build the venv (Python 3.12, Pyodide 0.27.7 versions): `uv venv -p /usr/bin/python3.12 <scratchpad>/venv && uv pip install -p <scratchpad>/venv/bin/python numpy==2.0.2 pandas==2.2.3 matplotlib==3.8.4 pytest==8.1.1 scikit-learn==1.6.1 scipy statsmodels sympy mpmath`. Run long jobs with `setsid nohup`, shards in a separate worktree. Six `tools/test-*` need `--local-cdn <pkgs>`.

Expected census: lessons 1,214; levels 279; reviews 279; exams 29 topic, 4 stage, 16 mock; drills 35 (oa 8); bank 200; hours 3,695, gap 0; edges 261, none without why; readiness-sums OK; validator 0 errors; perf-pending 0, 132 of 132 tasks.

Session X finished Phase 3 (`docs/reviews/review-perf-retrofit-*.md`). Engine 698 to 704 done. Gates green at 1d9de3e (PROGRESS).

Next, in order:
1. Phase 4 of `docs/briefs/session-v-plan.md`: drill packs 1 to 8 and bank part 2 (PLAN 2a), one content agent per pack, each second-read.
2. One engine agent beside it numbers the session X inbox bullets (`docs/BACKLOG-INBOX.md` after "orchestrator, session W") from 705.
3. Ask the user for the review-size route (`docs/reports/review-size-audit.md`).

Fable audit resumes (user, 9 Nov): at session start re-enable the scheduled task `trig_01FJuNVhosR68kSj3RhYkXrp`, tick the PLAN 5b pause line, and record it in DECISIONS. The audit follows `docs/briefs/fable-audit-session-prompt.md` and DECISIONS "Correctness first": interview courses and Stages 2 and 3 first (open: ito L4, measure-prob L4, pairs-rep finding 3), then Stages 1 and 0, then exams; session X performance tasks included. Merge `origin/claude/fable-audit` with merge-wave at start and close. Content work avoids courses the audit has open. Merge with merge-wave; amend a merge only after it prints OK.

Acceptance: validator 0 errors, readiness-sums OK, all `tools/test-*`, four shards and routes green at the final HEAD, state files, NEXT_PROMPT for session Z.
