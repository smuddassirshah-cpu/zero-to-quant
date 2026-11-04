Read CLAUDE.md and the four state files; follow the SESSION PROTOCOL. Full standards apply (DECISIONS "Standards restored"). Branch `claude/amazing-wright-d4mx7i` only; if the local ref is behind origin, check out origin's commit (shallow clone: compare trees; back up before moving a ref).

Task: PLAN 2a item 5a (prerequisite gating, user request) beside item 5 (remaining topic 3.5 levels and the mock-oa-code brief). Engine pass C is done (items 467 to 480 in `docs/AUTHORING.md`); coding-int, research-int and systems L1 and L2 are written and answer-checked.

Wave 1, parallel (Sonnet, `isolation: "worktree"`, distinct files; merge each branch, grep every file for conflict markers, re-validate):
- engine-dev: engine pass E from `docs/briefs/prereq-gating.md` sections 1 to 7 (number from 481), with a sample, routes checks and AUTHORING section 11.
- content-authors, one level each: research-int L3, systems L3 (`feed.hex` under `content/data/systems/`), coding-int L3.
- brief writer: the mock-oa-code section of `docs/briefs/mocks.md` (draws from `drills/<pack>`).
Wave 2: the `requires` mapping agent (brief section 8; may edit `course.json` for that field only), then its second reader and fix; research-int L4 and systems L4 (they write their drill files); then mock-oa-code, then coding-int L4.

Close: an answer check per new level (DECISIONS "Fresh numbers in reviews and homework") and a fix agent; a second reader on engine pass E; build the local CDN (`bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`); full split playthrough (four lesson shards from the manifest, then `--sets`, `--exams`, `--bank all`, `--drills`, `--routes-only`) with and without `--mobile`; PLAN ticks; state files.

Files likely touched: `app/js/` (content, learn, today, course, lesson, prepare screens), `app/tools/`, every `course.json` (wave 2), `app/content/courses/{research-int,systems,coding-int}/`, `app/content/drills/`, `docs/briefs/mocks.md`, `docs/AUTHORING.md`, reports and reviews.

Acceptance: validate 0 errors with no `requires` cycles; a fresh profile sees a correct locked card on a Stage 3 lesson, test-out unlocks it, Strict mode hides "Open anyway"; new levels green with and without `--mobile`; answer checks clean after fixes; full split runs green.
