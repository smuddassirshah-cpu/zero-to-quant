Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; work detached at `origin/claude/amazing-wright-d4mx7i`, push `HEAD:claude/amazing-wright-d4mx7i`, rebase on divergence, never reset. Build the local CDN in the background first: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`. Build the number-check venv with Python 3.12 and the Pyodide 0.27.7 versions: `uv venv -p /usr/bin/python3.12 <scratchpad>/venv && uv pip install -p <scratchpad>/venv/bin/python numpy==2.0.2 pandas==2.2.3 matplotlib==3.8.4 pytest==8.1.1 scikit-learn==1.6.1 scipy statsmodels sympy mpmath`. Launch long runs with `setsid nohup`; run playthrough shards in a separate worktree. Tests that need the CDN take `--local-cdn <pkgs>` (test-check-first, test-engine-runtime, test-expr-equations, test-playthrough-overflow, test-playthrough-tall, test-today-tested-out).

Expected census: lessons 1,214 of 1,214; levels 279 of 279; reviews 279, own pass 279; exams 29 topic, 4 stage, 16 mock; drills 35 (oa 8); bank 200; hours 3,695, gap 0; cross-course edges 261, none without why; readiness-sums OK; validator 0 errors; `perf-pending.mjs` lists 0, 132 of 132 rule-matched levels with a task; `[perf-optional-row]` 0.

Session X finished Phase 3: every performance task written, second-read and fixed (`docs/reviews/review-perf-retrofit-1.md` to `-14.md`). Engine 698 to 704 done. Gates green at 1d9de3e: four shards at 18defcb, the seven later files replayed, routes desktop and mobile, all `tools/test-*` (PROGRESS, session X close).

Next, in order:
1. Phase 4 of `docs/briefs/session-v-plan.md`: drill packs 1 to 8 and bank part 2 (PLAN 2a), with the freshness gate; one content agent per pack, each second-read.
2. One engine agent beside it numbers the session X inbox bullets (`docs/BACKLOG-INBOX.md`, "Raised later" sections after "orchestrator, session W"; about 60) from 705.
3. Ask the user for the review-size route (`docs/reports/review-size-audit.md`) before any review authoring.

The Fable audit stays paused (trigger `trig_01FJuNVhosR68kSj3RhYkXrp` disabled). Merge with merge-wave; amend a merge only after it prints OK.

Acceptance: validator 0 errors; readiness-sums OK; all `tools/test-*` pass; four shards and routes green at the final HEAD; state files; NEXT_PROMPT for session Z.
