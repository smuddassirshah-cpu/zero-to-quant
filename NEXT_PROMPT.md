Read CLAUDE.md and follow its SESSION PROTOCOL. Branch `claude/amazing-wright-d4mx7i` only; `git pull --rebase` first; on divergence, rebase, never reset.

Expected census: lessons 1,087 of 1,214 (193, 528, 162, 204); levels 251; reviews 251, own pass 251; exams 22 topic, 1 stage, 11 mock; drills 35 (oa 8); bank 200; hours 3,695 stored and summed, gap 0. Trader superday closure (`closure.mjs --target mock-superday-trader`): 96 levels, 32 courses, 422 lessons. `closure.mjs --target pdes/L3`: unwritten only odes L4 and numerics L4.

Tasks, in order. Start the wave only with over half the usage window left.

A. Protocol 6 first (engine-dev, one agent, before any content agent): the two session S inbox items in `docs/BACKLOG-INBOX.md`. (1) [Must] a shared helper so each level's number script asserts its recomputed values against the lesson JSON at named paths, plus a validator warning for a level script that names no JSON path; LEVEL-BRIEF requires it. (2) [Should] validator error on a level review without `pass`. Number them in ENGINE-BACKLOG.

B. Wave of two, worktrees, `merge-wave.sh`: content-author odes L4; content-author numerics L4 ("One option, three ways"). Each uses the A helper. Then per level a second read and a Sonnet fix pass (protocol 4, 5). On merge, `readiness-sums.mjs` fails on LIMITED: empty pdes's list, run `--write`, and drop "Route limited" from `docs/readiness.md` lines 553 and 620.

C. Item 12 pilot prep (user owns the pilot): a one-page observation sheet in `docs/pilot/` (stalls, delayed retention, unseen problem, explanation aloud, out-of-app task) and a learner brief. Do not tick item 12.

Context not in state files: the odes brief's "b = 4 settles fastest" is false (l9 teaches b = 3); numerics L3 requires odes/L4 in course.json (recheck numerics l11, l12 when odes L4 lands). The user still owes the five capstone records (`content/capstones.json`).

Acceptance: validator 0 errors; readiness-sums OK; pdes/L3 closure reaches nothing unwritten; playthroughs green desktop and mobile; four `--all --shard i/4 --local-cdn` runs green.
