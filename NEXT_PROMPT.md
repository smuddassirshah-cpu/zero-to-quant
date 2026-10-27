Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 0, "Triage 2 (container restart, 27 Oct)".

Context: a container restart stopped four content agents just before they reported. coint L3 and contests L2, L3 and L4 (lessons, reviews, homeworks) are on disk in WIP commits, validator 0 errors. The full `playthrough.mjs --all` had run 663 items green with no failures (Stage 0, Stage 1 and the start of Stage 2) when it was killed.

First, build the local CDN if it is missing: from the repo root, `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`; jsDelivr is blocked here.

Do: for each of the four levels, run one `test-fixer` agent. Give it the brief section in `docs/briefs/<course>.md`, the `--local-cdn` path, and the report pattern `docs/reports/coint-2.md`. It plays every lesson and both sets, checks numbers twice and checks that starters fail. Then it writes `docs/reports/<course>-<level>.md`, or deletes the level's files if they cannot be made green. Run up to four of these agents in parallel. Then run `node tools/playthrough.mjs --all --local-cdn <pkgs> 2>&1 | tail -30` from `app/` in the background. It takes about 2.5 hours, so commit while it runs.

Once triage is green, continue with the next unchecked tasks in this order, one agent per level or exam, in waves of four. Stop launching new work at about 85% of the session limit.
1. Exam topic-2.2.
2. Exams topic-2.3 and topic-2.4.
3. Exam topic-2.1.
4. Stage 1 gap levels.

Files likely touched: `app/content/courses/{coint,contests}/`, `docs/reports/`, `docs/BACKLOG-INBOX.md`, `app/content/manifest.json`, state files.

Acceptance:
- `node tools/validate.mjs` reports 0 errors.
- `playthrough.mjs --all --local-cdn` passes.
- Each of the four levels is green with a report, or removed and relisted in PLAN.md.
- PLAN.md ticks triage 2 and its four levels.
- NEXT_PROMPT.md names the next task.
