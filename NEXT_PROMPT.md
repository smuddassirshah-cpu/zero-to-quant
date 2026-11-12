# NEXT_PROMPT: session AC

Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i`: push every commit there (session AB pushed the harness branch too). Build the local CDN and the venv first: `bash app/tools/fetch-local-cdn.sh <pkgs>`; `uv venv --python 3.12 --seed <venv>` then `uv pip install numpy==2.0.2 pandas==2.2.3 matplotlib==3.8.4 pytest==8.1.1 sympy scipy scikit-learn==1.6.1 statsmodels`. Long jobs with `setsid nohup`; poll result files. Commit an `engine-dev` worktree from the main session at least hourly. Run shards alone: `test-validate-*` files take 25 minutes beside two shards and 10 alone. `test-bank-code`, `test-drill-page`, `test-planted-check` need `--local-cdn <pkgs>` as an argument; `test-answer-forms` needs `ZQ_LOCAL_CDN`; `test-validate-band-rules` needs neither.

Expected census: lessons 1,236; levels 283; reviews 283 (items 2,558); exams 29 topic, 4 stage, 16 mock; drills 270; Fluency sets 100 (families 318); problem sets 87 (items 332); bank 36 files, 400 items; hours 3,695 gap 0; edges 266; validator 0 errors.

Merge `origin/claude/fable-audit` at start and close. Agent brief tail and the acceptance list: DECISIONS, session AB. A re-authored item is grepped for its numbers across `app/content/` (DECISIONS, session AB).

Tasks, in order:
1. Delta reads owed (KNOWN_ISSUES, session AB): fix passes of `review-problems-1.4-b.md`, `-1.4-c.md`, `review-delta-bank-2.md`, `review-delta-holes.md`, `review-delta-problems-ab-1.md`, `review-delta-drills-ci-5-8.md`.
2. Content passes from the new rules: `[percent-form]` 74 parts, `[negative-key]` 240, `[tight-band]` 26, `[near-miss]` 190 drills; `stage-3` `r-t-bar` and `r-best-of-twenty`.
3. M chained problems, PLAN 2d: `eigen` 4, `number-sense` 1 to 3, `ratio`, then 0.6, 1.10, 1.11, 2.1 levels 1 to 3, 2.2, 2.5, 2.6, 3.2, 3.4.
4. Engine: open items 941 to 967, first 944, 945, 951, 955; the two reuse cases `--cross-numbers` misses.
5. 63 drills past the safe recursion depth (`docs/reports/engine-pass-ab.md`): state the limit or resize.

Do not raise the pilot. Acceptance at the final HEAD; NEXT_PROMPT for session AD.
