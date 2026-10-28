Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 2b, "proof L2: Sets and functions [Pure maths]". One content level, written by one `content-author` agent from `## Level 2` of `docs/briefs/proof.md`. The main session plans and reviews only.

Level: course `proof` (topic 0.6, strand pure), lessons `l6-sets`, `l7-combining-sets`, `l8-functions-as-sets`, `l9-one-to-one-onto`, plus `review-2` and `homework-2`. Use the ids and names in `app/content/courses/proof/course.json` exactly.

Context not in the state files:
- Proof L1 is written (`l1` to `l5`, `review-1`, `homework-1`); the agent reads `l2` to `l5` for notation and voice, as the brief says. Its report is `docs/reports/proof-1.md`.
- Proofs are never graded free-form: each step is graded with `order` (with `distractors` and `same`), `choice`/`multi` or fill-ins; whole proofs go to `longform` homework with a 10-point rubric and model answer.
- Table-widget misconception feedback is keyed by cell id in `byKey`; the validator rejects the widget's own `wrong[]` ids (L1 finding, in the inbox).
- Briefs name an older session's scratchpad. Give the agent this session's scratchpad: its own subfolder `proof-2`, and `pkgs` for `--local-cdn` (build it with `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs` if missing, about 40 s). CPython lacks SciPy and SymPy; install with `pip install --target <scratchpad>/pylib scipy sympy` if a number check needs them.

Files likely touched: `app/content/courses/proof/l6-*.json` to `l9-*.json`, `review-2.json`, `homework-2.json`, `docs/reports/proof-2.md`, `docs/BACKLOG-INBOX.md`, plus PLAN.md, PROGRESS.md, NEXT_PROMPT.md.

Acceptance: from `app/`, `node tools/validate.mjs 2>&1 | tail -5` shows 0 errors; `node tools/playthrough.mjs --lesson proof/<id>` passes for all four lessons and `--set proof/review-2` and `--set proof/homework-2` pass (with `--local-cdn <pkgs>`); the report exists; every stated number is computed twice; PLAN.md ticks proof L2; NEXT_PROMPT.md names "proof L3: Proof methods".
