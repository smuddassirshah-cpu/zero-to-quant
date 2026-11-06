Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; `git pull --rebase` first; on divergence, rebase, never reset. If the local ref is the stale unrelated line (KNOWN_ISSUES, session T), work detached at `origin/claude/amazing-wright-d4mx7i` and push `HEAD:claude/amazing-wright-d4mx7i`.

Expected census: lessons 1,179 of 1,214 (193, 555, 202, 229); levels 271 of 279; reviews 271, own pass 271; exams 23 topic, 1 stage, 11 mock; drills 35 (oa 8); bank 200; hours 3,695 stored and summed, gap 0. Trader superday closure: 96 levels, 32 courses, 422 lessons, nothing unwritten. `closure.mjs --target` linear-maps/L4, topology/L1 and algebra/L1 each reach nothing unwritten.

Session U, in order (session T plan, "Left for session U"):
1. Content wave: algebra L1 to L2 and L3 to L4 (two agents), topology L1 to L3, linear-maps L4. One second read and one Sonnet fix pass per level.
2. Exam wave: topic exams 0.6, 1.10, 1.11, 2.5, 2.6, 3.4; stage-1, stage-2, stage-3 (PLAN line 249); the five mocks prep.json names with no file. Pattern: `topic-3.1` and `docs/briefs/exam-3.1-scripts/check_numbers.py` (never name a script `numbers.py`: it shadows the stdlib module).
3. Drill packs 1 to 8 and bank part 2, only with over half the usage window left.

New since T: level scripts must import `app/tools/numbers_lib.py` directly and call `check_wrongs()`; rule 581 (wrong value that can never fire) and a review without `pass` are validator errors. An author low on context hands back finished levels; start a fresh author for the rest. Launch a fix agent only after its review merges. Voice-scan whole course folders.

Acceptance: validator 0 errors; readiness-sums OK; each level green desktop and mobile; four `--all --shard i/4 --local-cdn` runs, staggered, green. Then write NEXT_PROMPT for session V.
