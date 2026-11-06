Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; `git pull --rebase` first; on divergence, rebase, never reset.

Expected census: lessons 1,087 of 1,214 (193, 528, 162, 204); levels 251 of 279; reviews 251, own pass 251; exams 22 topic, 1 stage, 11 mock; drills 35 (oa 8); bank 200; hours 3,695 stored and summed, gap 0. Trader superday closure: 96 levels, 32 courses, 422 lessons. `closure.mjs --target pdes/L3`: unwritten only odes L4 and numerics L4.

Long session (6 to 7 hours, autonomous). Follow `docs/briefs/session-T-plan.md` in order:

0. engine-dev alone: the three session S inbox items (number-check helper that reads the lesson JSON, validator error on a review without `pass`, playthrough port retry). Protocol 6: no content agent before it merges.
1. Wave 1: odes L4, numerics L4, convex L1 to L3, stat-models L1 to L3. On merge, clear pdes's LIMITED list in `readiness-sums.mjs` and `docs/readiness.md`.
2. Wave 2: momentum-rep L2 to L3, pairs-rep L1 to L3, complex L3, analysis L5.
3. Wave 3, only with over half the usage window left: convex L4, stat-models L4, vector-calc L1 to L3, exam `topic-3.1`.

Every level gets a second read and a Sonnet fix pass (protocol 4, 5), overlapped with the next wave. Do not stop between steps to ask; record open questions in KNOWN_ISSUES and carry on. Commit and push after every merge and fix pass.

Context: the odes brief's "b = 4 settles fastest" is false (l9 teaches b = 3). Item 12 (pilot) is post-completion. Capstone records await the user's review (DECISIONS "Completion scope").

Acceptance: validator 0 errors; readiness-sums OK; pdes/L3 closure reaches nothing unwritten; each level's playthrough green desktop and mobile; four `--all --shard i/4 --local-cdn` runs, started a few seconds apart, green. Write NEXT_PROMPT for session U from the plan's "Left for session U".
