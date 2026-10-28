Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 2b, "analysis L3: Series [Pure maths]". One content level, written by one `content-author` agent from `## Level 3` of `docs/briefs/analysis.md`. The main session plans and reviews only.

Level: course `analysis` (topic 1.10, strand pure), lessons `l11-partial-sums`, `l12-convergence-tests`, `l13-absolute-conditional`, `l14-rearranging`, plus `review-3` and `homework-3`. Use the ids and names in `app/content/courses/analysis/course.json` exactly.

First, before L3: analysis L1 and L2 lessons are committed and green, but `docs/reports/analysis-1.md` and `analysis-2.md` are missing (the agents' writes were refused; see KNOWN_ISSUES). Unless the user has already had them written, run one foreground `content-author` agent to write both reports from the committed files (format in `docs/LEVEL-BRIEF.md`; re-check every stated number twice), then tick analysis L1 and L2 in PLAN.md.

Context not in the state files:
- Proof, markov L5, analysis L1 and L2, linear-maps L1 and L2 are written; read analysis L1 and L2 for notation and voice.
- Proofs are never graded free-form: steps use `order` (with `distractors` and `same`), `choice`/`multi` or fill-ins; whole proofs go to `longform` homework (10-point rubric, model answer).
- Engine limits found: `derive` takes only expression, order or choice (numeric steps go on `problem` screens); `derive` `floor` mis-rounds exact boundaries; tables of 5+ columns scroll at 390 px; table feedback keys by cell id in `byKey`; in `place`, give each chip one slot; `choice` is not shuffled unless `shuffle: true`.
- Scratchpad: give the agent its own subfolder `analysis-3`, and `pkgs` for `--local-cdn` (build with `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs` if missing, about 40 s). Tell it to write its report early and to stop and say so if a write is refused.

Files likely touched: `app/content/courses/analysis/l11-*.json` to `l14-*.json`, `review-3.json`, `homework-3.json`, `docs/reports/analysis-1.md` to `analysis-3.md`, `docs/BACKLOG-INBOX.md`, PLAN.md, PROGRESS.md, NEXT_PROMPT.md.

Acceptance: from `app/`, `node tools/validate.mjs 2>&1 | tail -5` shows 0 errors; `node tools/playthrough.mjs --lesson analysis/<id> --local-cdn <pkgs>` passes for all four lessons, and `--set analysis/review-3` and `--set analysis/homework-3` pass; the reports exist; every stated number computed twice; PLAN.md ticks analysis L3; NEXT_PROMPT.md names "analysis L4: Continuity and the derivative".
