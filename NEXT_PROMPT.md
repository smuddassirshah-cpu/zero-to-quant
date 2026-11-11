# NEXT_PROMPT: session AB

Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only: work detached at its origin, push `HEAD:` to it, rebase on divergence, never reset. Build the local CDN and venv in the background first (commands in `docs/LEVEL-BRIEF.md`). Long jobs with `setsid nohup`, shards in a separate worktree, one browser job per agent, at most four agents. A shard takes about 80 minutes: run two runners in parallel from the start.

Expected census: lessons 1,236; levels 283; reviews 283 (items 2,558); exams 29 topic, 4 stage, 16 mock; drills 270; Fluency sets 83 (families 257); problem sets 62 (items 237); bank 200; hours 3,695 gap 0; edges 266; validator 0 errors.

Merge `origin/claude/fable-audit` at start and close; replay the files it changed. Agent briefs end "start nothing in the background; hand back once", "do not commit `manifest.json`", "commit work in progress", "write only inside your own worktree". The main session commits for `engine-dev`.

Tasks, in order:
1. Delta read of the fix passes in `docs/reviews/review-drills-ci-5.md` to `-8.md`.
2. Engine pass: the [Must] silent stop on deep recursion on the drill page (KNOWN_ISSUES, session AA), with a check across all 270 drills; ENGINE-BACKLOG 914; a protocol 6 rule for "method one step short of the target passes".
3. Bank part 2 (200 items), PLAN 2d.
4. Four new levels (`number-sense`, `quadratics`, `testing`, `stat-learning` level 4): topic exam items, Option B skills, Fluency, problem sets.
5. M chained problems for the remaining maths, probability and statistics levels.
6. Triage: 149 `[tight-band]`, 37 `[wide-wrong-band]`, 198 answers noted by `grade-regression.mjs`.

Do not raise the pilot. Acceptance: validator 0 errors, readiness-sums OK, all `tools/test-*`, four shards, `--problems all`, `--drills`, `--fluency-all`, routes green at the final HEAD, state files, NEXT_PROMPT for session AC.
