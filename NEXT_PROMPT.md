Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only: work detached at its origin, push `HEAD:` to it, rebase on divergence, never reset. Build the local CDN in the background first: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`. Build the venv (Python 3.12, Pyodide 0.27.7 versions): `uv venv -p /usr/bin/python3.12 <scratchpad>/venv && uv pip install -p <scratchpad>/venv/bin/python numpy==2.0.2 pandas==2.2.3 matplotlib==3.8.4 pytest==8.1.1 scikit-learn==1.6.1 scipy statsmodels sympy mpmath`. Run long jobs with `setsid nohup`, shards in a separate worktree. Six `tools/test-*` need `--local-cdn <pkgs>`.

Expected census: lessons 1,214; levels 279; reviews 279; exams 29 topic, 4 stage, 16 mock; drills 35 (oa 8); bank 200; hours 3,695, gap 0; edges 261; readiness-sums OK; validator 0 errors; perf-pending 0.

Read `docs/reviews/critical-review-fable-5-2.md` (verdict and the ten changes). Next, in order:
1. Fable audit resumes (user, 9 Nov): re-enable `trig_01FJuNVhosR68kSj3RhYkXrp`, tick the PLAN 5b pause line, record in DECISIONS. Order changes to route use (review 6.4): `mm-games`, `recruiting`, topic 1.5 courses, then the other trader and developer closure courses; optional Stage 2 and 3 courses last. Merge `origin/claude/fable-audit` with merge-wave at start and close; content avoids open courses.
2. Engine agent: number the session X inbox from 705; Learn, stage cards and `readiness.md` show in-app hours (from `minutes`) apart from outside-study hours (review 4.1); local record and playback on `aloud` items (5.1).
3. Phase 4 (`docs/briefs/session-v-plan.md`), developer first: drill packs for OA and coding-interview patterns, each second-read.
4. Re-author `mock-oa-sig-2`, `-3`, `mock-oa-trader-2`, `-3` on new templates (review 3.1), second-read; then bank part 2.
5. Ask the user for the review-size route. The pilot stays post-completion (user, 9 Nov; PLAN 2c item 12): do not raise or schedule it.

Acceptance: validator 0 errors, readiness-sums OK, all `tools/test-*`, four shards and routes green at the final HEAD, state files, NEXT_PROMPT for session Z.
