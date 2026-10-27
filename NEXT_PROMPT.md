Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 0, "Full `playthrough.mjs --all --local-cdn <pkgs>` green", then PLAN.md task 2, the Stage 1 gap levels.

Context: all Stage 2 content and exams topic-2.1 to 2.4 are green and reported. The last full playthrough reached 223 of 1,108 items, all green, when the session limit stopped it. That run started before the topic 2.x exams existed; each passed alone.

First, build the local CDN if it is missing: from the repo root, `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`.

Do:
1. From `app/`, run `node tools/validate.mjs 2>&1 | tail -5`, then start `node tools/playthrough.mjs --all --local-cdn <pkgs> > <scratchpad>/full.log 2>&1` in the background (about 2.5 hours). Never read the full log; count `^ok` lines and grep non-ok lines. A failure goes to one `test-fixer` (Sonnet) with the item id; re-run it alone first, since parallel agents make set mode flaky.
2. While it runs, start the gap levels in waves of four, one `content-author` (Sonnet) per level, in PLAN.md order: limits L5, integrals L4, multivar L5, eigen L4, then random-vars L5, limits-thm L4, markov L4. Each gets its brief `docs/briefs/gap-<course>.md`, `docs/briefs/gaps-plan.md`, `docs/LEVEL-BRIEF.md`, the `--local-cdn` path, and the report pattern `docs/reports/coint-2.md`. Commit each level as it lands.
3. Stop launching at about 85% of the session limit.

Files likely touched: `app/content/courses/{limits,integrals,multivar,eigen,random-vars,limits-thm,markov}/`, `docs/reports/`, `docs/BACKLOG-INBOX.md`, `app/content/manifest.json`, state files.

Acceptance:
- `node tools/validate.mjs` reports 0 errors.
- `playthrough.mjs --all --local-cdn` passes, or its failures are fixed and re-run green.
- Each launched gap level is green with a report, or removed and relisted in PLAN.md.
- PLAN.md ticks the playthrough task and the finished levels.
- NEXT_PROMPT.md names the next task.
