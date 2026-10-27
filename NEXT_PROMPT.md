Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 2, last item: extend exams topic-1.3, topic-1.4 and topic-1.5 with items for the seven new gap levels.

Context: task 0 is done (all 739 lessons, 354 sets, 19 exams and every route green with `--local-cdn`). All seven gap levels are written, green and reported (`docs/reports/limits-5.md`, `integrals-4.md`, `multivar-5.md`, `eigen-4.md`, `random-vars-5.md`, `limits-thm-4.md`, `markov-4.md`). The items each exam needs are listed in `docs/briefs/gaps-plan.md`, section "For the exam extension". Gap briefs name stale scratchpad paths; give agents this session's paths.

First, build the local CDN if it is missing: from the repo root, `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`.

Do:
1. Launch three `content-author` agents (Sonnet) in parallel, one per exam. Each gets: its exam file `app/content/exams/topic-1.<n>.json` (append items only, never rename or remove existing item ids), its bullet in `docs/briefs/gaps-plan.md`, the matching gap reports, `docs/LEVEL-BRIEF.md`, `docs/AUTHORING.md`, the `--local-cdn` path, and the report pattern `docs/reports/exam-2.2.md`. Reports go to `docs/reports/exam-1.<n>-gap.md`. Each agent checks every new number twice and plays its exam alone.
2. Commit each exam as it lands.
3. Optional if time remains: a `test-fixer` adds the limits-thm l18 cite to markov l16 (KNOWN_ISSUES).

Files likely touched: `app/content/exams/topic-1.3.json`, `topic-1.4.json`, `topic-1.5.json`, `docs/reports/`, `docs/BACKLOG-INBOX.md`, `app/content/manifest.json`, state files.

Acceptance:
- From `app/`, `node tools/validate.mjs` reports 0 errors.
- `node tools/playthrough.mjs --exam topic-1.3 --exam topic-1.4 --exam topic-1.5 --local-cdn <pkgs>` passes.
- Each exam covers every bullet in its gaps-plan list, or the report names what was left out and why.
- PLAN.md ticks the exam extension; NEXT_PROMPT.md names the next task (Stage 3 content, momentum-rep L1).
