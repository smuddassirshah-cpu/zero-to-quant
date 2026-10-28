Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 2b, "proof L1: Statements and logic [Pure maths]". One content level, written by one `content-author` agent from `## Level 1` of `docs/briefs/proof.md`. The main session plans and reviews only.

Level: course `proof` (topic 0.6, strand pure), lessons `l1-true-or-false`, `l2-and-or-not`, `l3-if-then`, `l4-for-all-there-exists`, `l5-saying-the-opposite`, plus `review-1` and `homework-1`. Use the ids and names in `app/content/courses/proof/course.json` exactly.

Context not in the state files:
- Proofs are never graded free-form: each step is graded with `order` (with `distractors` and `same`), `choice`/`multi` or fill-ins; whole proofs go to `longform` homework with a 10-point rubric and model answer.
- Briefs name an older session's scratchpad. Give the agent this session's scratchpad: its own subfolder `proof-1`, and `pkgs` for `--local-cdn` (build it with `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs` if missing, about 40 s). CPython lacks SciPy and SymPy; install with `pip install --target <scratchpad>/pylib scipy sympy` if a number check needs them.
- Item 449 (tested out) is new: nothing in this level depends on it.
- Seven new breadth briefs exist (`numerics`, `convex`, `stat-models`, `measure-prob`, `pdes`, `algebra`, `topology`); later levels use them.

Files likely touched: `app/content/courses/proof/l1-*.json` to `l5-*.json`, `review-1.json`, `homework-1.json`, `docs/reports/proof-1.md`, `docs/BACKLOG-INBOX.md`, plus PLAN.md, PROGRESS.md, NEXT_PROMPT.md.

Acceptance: from `app/`, `node tools/validate.mjs 2>&1 | tail -5` shows 0 errors; `node tools/playthrough.mjs --lesson proof/<id>` passes for all five lessons and `--set proof/review-1` and `--set proof/homework-1` pass (with `--local-cdn <pkgs>`); the report exists; every stated number is computed twice; PLAN.md ticks proof L1; NEXT_PROMPT.md names "proof L2: Sets and functions".
