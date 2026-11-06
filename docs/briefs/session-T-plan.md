# Session T plan (written at the close of session S, 6 Nov)

Budget: 6 to 7 hours autonomous. The main session plans, merges and reviews; agents do the work (CLAUDE.md "Models"). Usage rule unchanged: start a wave only with more than half the usage window left; past half, finish the step in flight, close the state files and stop.

Closure facts at session S close (`closure.mjs --target <course>/<level>`): convex, stat-models, momentum-rep, pairs-rep L1, complex L3, vector-calc L1, algebra L1, analysis L5, linear-maps L4 and odes L4 reach nothing unwritten outside their own course. numerics L4 reaches odes L4; topology reaches analysis L5. Authors may write a level whose prerequisites are unwritten; playthrough does not need them.

## Step 0, engine-dev alone (about 45 min; protocol 6 before any content)

The three session S inbox items in `docs/BACKLOG-INBOX.md`, numbered into `docs/ENGINE-BACKLOG.md`:
1. [Must] Shared number-check helper: a level script loads the level's JSON and asserts each recomputed value appears at a named path (prose, `wrong[]` value, `why`, `explain`); validator warning for a level whose script names no JSON path. Update `docs/LEVEL-BRIEF.md` so authors use it.
2. [Should] Validator error on a level review without `pass`.
3. [Should] Playthrough static server retries on a new port when the bind fails (the four-shard start race).
While it runs, the main session drafts the per-agent prompts for wave 1. No content agent starts before step 0 merges.

## Wave 1 (four content-authors, worktrees)
- odes L4 (Transforms and numerical solution).
- numerics L4 (One option, three ways). Then recheck numerics l11, l12 against odes L4 (numerics L3 requires odes/L4).
- convex L1 to L3.
- stat-models L1 to L3.
On merge: `readiness-sums.mjs` fails on LIMITED once odes L4 and numerics L4 exist: empty pdes's list, `--write`, drop "Route limited" from `docs/readiness.md` lines 553 and 620. `closure.mjs --target pdes/L3` must reach nothing unwritten.

## Wave 2 (four agents)
- momentum-rep L2 and L3.
- pairs-rep L1 to L3.
- complex L3 (Integrals and Fourier).
- analysis L5 (Integration and metric spaces).

## Wave 3 (four agents, only with over half the window left)
- convex L4 and stat-models L4 (two agents; one course each).
- vector-calc L1 to L3.
- Exam author: `topic-3.1` (momentum-rep, pairs-rep; pattern `app/content/exams/topic-3.3.json`, brief section in `docs/briefs/` if present, else PLAN 2b line 246).

Left for session U: algebra L1 to L4, topology L1 to L3, linear-maps L4, the breadth and stage exams, the five missing mocks, drill packs, bank part 2.

## Per level (protocol 4 and 5)
Author gates, then one second read (writes `docs/reviews/review-<course>-<levels>.md`, runs the author's script, checks JSON-stated values) and one Sonnet fix pass. Overlap reads and fixes with the next wave. Before each merge run `node app/tools/write-review-pass.mjs --dry` (should report 0 to write once step 0 lands).

## Close
Validator 0 errors; readiness-sums OK; `test-met-rule`, `test-capstone`, `test-check-first` green; four `--all --shard i/4 --local-cdn` runs started a few seconds apart, all green; PLAN ticks, one PROGRESS line, DECISIONS, KNOWN_ISSUES; NEXT_PROMPT for session U from "Left for session U".
