Read CLAUDE.md, then PLAN.md, PROGRESS.md, DECISIONS.md and KNOWN_ISSUES.md. Follow the SESSION PROTOCOL in CLAUDE.md.

Task: PLAN.md task 3, first item: momentum-rep L1 ("The paper"), course `momentum-rep` (topic 3.1).

Context: tasks 0 to 2 are done (Stage 1 and Stage 2 complete; exams topic-1.3 to 1.5 extended to the 30-item cap and green). Stage 3 starts here. The brief is `docs/briefs/momentum-rep.md`: the course context at the top (paper figures, generator, reference values) plus section `## Level 1`. That brief names stale scratchpad and pkgs paths; give the agent this session's paths instead.

First, build the local CDN if it is missing: from the repo root, `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`.

Do:
1. Launch one `content-author` agent with the course context and the Level 1 section of `docs/briefs/momentum-rep.md`, `docs/LEVEL-BRIEF.md`, `docs/AUTHORING.md`, this session's scratchpad subfolder `momentum-rep-1` and the `--local-cdn` path. It writes `l1-reading-a-paper` to `l5-replication-plan`, `review-1.json`, `homework-1.json` in `app/content/courses/momentum-rep/`, reports to `docs/reports/momentum-rep-1.md`, appends engine limits to `docs/BACKLOG-INBOX.md`, and does not commit.
2. If time remains after it lands and is committed, run momentum-rep L2 the same way (it reads L1's files, so not in parallel).

Files likely touched: `app/content/courses/momentum-rep/l1-*.json` to `l5-*.json`, `review-1.json`, `homework-1.json`, `docs/reports/momentum-rep-1.md`, `docs/BACKLOG-INBOX.md`, `app/content/manifest.json`, state files.

Acceptance:
- From `app/`, `node tools/validate.mjs 2>&1 | tail -5` reports 0 errors.
- `node tools/playthrough.mjs --lesson momentum-rep/<id>` for each of the five lessons and `--set momentum-rep/review-1`, `--set momentum-rep/homework-1`, all with `--local-cdn <pkgs>`, pass.
- Every code solution passes its hidden tests and every starter fails them; every number computed twice (report says how).
- PLAN.md ticks momentum-rep L1; NEXT_PROMPT.md names the next task (momentum-rep L2, or L3 if L2 also landed).
