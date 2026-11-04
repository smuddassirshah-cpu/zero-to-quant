Read CLAUDE.md and the four state files; follow the SESSION PROTOCOL. Full standards apply (DECISIONS "Standards restored"). Branch `claude/amazing-wright-d4mx7i` only; if the local branch ref is behind origin, check out origin's commit (the clone is shallow; compare trees, never reset away local work without a backup branch).

Task: PLAN 2a item 5, the remaining topic 3.5 levels, plus the mock-oa-code brief. Engine pass C is done (items 467 to 480, documented in `docs/AUTHORING.md`: `parts`, `data`, `draw`, C++ drills and sessions, `allocCheck`, `interleave`, `"sample": true`); levels L1 and L2 of coding-int, research-int and systems are written, answer-checked and fixed.

Wave 1, parallel content-author agents (Sonnet, `isolation: "worktree"`, one level each; merge each branch, grep every file for conflict markers, re-validate):
- research-int L3 (uses `parts`, `data`; the six CSVs are in `app/content/data/`)
- systems L3 (uses `parts`, `data` for `feed.hex`)
- coding-int L3 (uses `parts`)
- a brief writer: `exams/mock-oa-code` section in `docs/briefs/mocks.md` (draws coding tasks from `drills/<pack>` per AUTHORING `draw`; coding-int l15 links to it)
Wave 2: research-int L4 and systems L4 (drills, `allocCheck`); then mock-oa-code itself, then coding-int L4 (needs the mock file).

Authors write the drill files their brief section names (vocabulary: AUTHORING section 5).

Close: an answer-check agent per level (fresh-numbers rule: DECISIONS "Fresh numbers in reviews and homework") and a fix agent; full split playthrough (four lesson shards from the manifest, then `--sets`, `--exams`, `--bank all`, `--drills`, `--routes-only`) with and without `--mobile`, `--local-cdn <scratchpad>/pkgs` (build it first with `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`); PLAN ticks per level; state files; NEXT_PROMPT.

Files likely touched: `app/content/courses/{research-int,systems,coding-int}/`, `app/content/drills/`, `app/content/data/systems/`, `docs/briefs/mocks.md`, `docs/reports/`, `docs/reviews/answers-*.md`, `docs/BACKLOG-INBOX.md`.

Acceptance: validate 0 errors; each new level green with and without `--mobile`; answer checks clean after fixes; full split runs green. Next after that: mock-superday-research, mock-oa-quant-data, topic-3.5 exam, second reads of the three courses.
