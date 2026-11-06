Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; `git pull --rebase` first; on divergence, rebase, never reset. The local ref is the stale unrelated line (KNOWN_ISSUES, session T): work detached at `origin/claude/amazing-wright-d4mx7i` and push `HEAD:claude/amazing-wright-d4mx7i`. Build the local CDN first: `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`.

Expected census: lessons 1,214 of 1,214 (193, 560, 202, 259); levels 279 of 279; reviews 279, own pass 279; exams 29 topic, 4 stage, 16 mock; no prep.json mock without a file; drills 35 (oa 8); bank 200; hours 3,695 stored and summed, gap 0. Trader closure 98 levels, 32 courses, 431 lessons, nothing unwritten. readiness-sums OK.

Session V, in order:
1. Engine pass (protocol 6; inbox "session U" bullets): `fresh-check.mjs` counts word tokens only and compares code function and class names (Must, four sightings); a `required` flag on paper items (Must: stage and mock code exits can be skipped); `expression` `form` for constant answers; per-paper `tracks`; draws seen in any exam count as seen; `importHint` reads test `setup`; float `example` warning; 584 refinement; libc++ hardening. Then engine pass 7.
2. Second reads and Sonnet fix passes for levels never read under the current standard: arma, garch, coint, backtest, alpha, opt-dash, contests, proof, analysis L1 to L4, linear-maps L1 to L3, momentum-rep L1. Each fix pass also clears its course's voice debt (`docs/reports/voice-census-session-u.txt`: 47 courses, 1,479 long sentences).
3. Drill packs 1 to 8 and bank part 2, only with over half the usage window left.

Open for the user: default choice shuffling (3,373 of 6,605 lesson choices show the key first); the `[key-length]` threshold (1,658 hits); capstone records.

Acceptance: validator 0 errors; readiness-sums OK; all `tools/test-*.mjs` pass; four `--all --shard i/4 --local-cdn` runs, staggered, green, with no merge during a shard. Then write NEXT_PROMPT for session W.
