Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 0, "Triage 3 (session limit, 27 Oct)".

Context: the last session hit its limit with the topic-2.4 exam agent in flight. topic-2.1 to 2.3 are done (green, reported); topic-2.4 did not report. Whatever they wrote is in the last WIP commit: check `app/content/exams/topic-2.*.json` and `docs/reports/exam-2.*.md`; a file may be partial or missing. All Stage 2 content is green and reported. The full `playthrough.mjs --all` had run 137 items green, 0 failures, when stopped.

First, build the local CDN if it is missing: from the repo root, `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`.

Do: one agent (Sonnet) for topic-2.4: a `test-fixer` if the file is on disk, a `content-author` if it is missing or clearly unfinished. Give it `docs/briefs/contests.md` (course context and Level 1 harness rules) and `docs/reports/contests-*.md`. Each reads `docs/AUTHORING.md`, `docs/curriculum.md` (the topic's exit line), the courses' `course.json` maps and level reports, and the patterns `app/content/exams/topic-1.7.json` and `docs/reports/exam-1.8.md`. It covers every skill, ramps difficulty near 20/50/20/10 per cent across d2 to d5, mixes widgets with code items, computes every number twice, checks that starters fail, plays `--exam topic-2.x --local-cdn <pkgs>`, and writes `docs/reports/exam-2.x.md`. Commit each exam as it lands. Then run `node tools/playthrough.mjs --all --local-cdn <pkgs> 2>&1 | tail -30` from `app/` in the background (about 2.5 hours) and commit while it runs.

When triage is green, continue in waves of four: Stage 1 gap levels (PLAN.md task 2, briefs `docs/briefs/gap-<course>.md`, one `content-author` per level). Stop launching at about 85% of the session limit.

Files likely touched: `app/content/exams/topic-2.4.json`, `docs/reports/exam-2.*.md`, `docs/BACKLOG-INBOX.md`, `app/content/manifest.json`, state files.

Acceptance:
- `node tools/validate.mjs` reports 0 errors.
- `playthrough.mjs --all --local-cdn` passes.
- topic-2.4 is green with a report.
- PLAN.md ticks triage 3 and topic-2.4.
- NEXT_PROMPT.md names the next task.
