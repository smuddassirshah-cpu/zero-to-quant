Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; `git pull --rebase` first; on divergence, rebase, never reset. The local ref is the stale unrelated line: work detached at `origin/claude/amazing-wright-d4mx7i` and push `HEAD:claude/amazing-wright-d4mx7i`. Build the local CDN in the background first: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`.

Expected census: lessons 1,214 of 1,214 (193, 560, 202, 259); levels 279 of 279; reviews 279, own pass 279; exams 29 topic, 4 stage, 16 mock; no prep.json mock without a file; drills 35 (oa 8); bank 200; hours 3,695, gap 0. Trader closure 98 levels, 32 courses, 431 lessons, nothing unwritten. readiness-sums OK. Capstone records are PLACEHOLDERS (DECISIONS 6 Nov).

Session V follows `docs/briefs/session-v-plan.md`, phases in order, waves of three or four agents:
1. Engine pass (two agents, disjoint files): shuffle by default; `required` paper items; per-paper `tracks`; cross-exam seen draws; `importHint` reads `setup`; `expression` `form`; `fresh-check` word tokens and code names; validator refinements; `merge-wave.sh` rules for briefs and readiness. Then engine pass 7 alongside Phase 2.
2. Second reads (Opus, one course each) and Sonnet fix passes for the 90 unread levels in `docs/reports/unread-levels-session-u.txt`, in its order, then their unread topic exams. Fix passes clear sentences over 35 words (20 is a target, not a gate) and long explanations.
3. Performance-task retrofit from `app/tools/perf-pending.json` (108 levels), interview and Stage 2 and 3 first, only with over half the window left.
4. Drill packs 1 to 8 and bank part 2, likewise.

Quality gates never move: unfinished work carries to session W. Never merge during a playthrough shard.

Acceptance: validator 0 errors; readiness-sums OK; all `tools/test-*.mjs` pass; four `--all --shard i/4 --local-cdn` runs, staggered, green; `--routes-only --local-cdn` desktop and mobile. Then write NEXT_PROMPT for session W.
