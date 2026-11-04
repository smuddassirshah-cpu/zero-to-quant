Read CLAUDE.md and the four state files; follow the SESSION PROTOCOL. Full standards apply (DECISIONS "Standards restored"). Branch `claude/amazing-wright-d4mx7i` only; if the local ref is behind origin, check out origin (shallow clone; back up before moving a ref). User (4 Nov): long session; close topic 3.5 and ship prerequisite gating.

Task: PLAN 2a items 5 and 5a in full. Engine pass C is done; L1 and L2 of coding-int, research-int and systems are written and checked.

Parallel agents (Sonnet, `isolation: "worktree"`, distinct files); merge each branch, grep every file for conflict markers, re-validate.
- Wave 1: engine pass E (`docs/briefs/prereq-gating.md` sections 1 to 7, from item 481, AUTHORING section 11); research-int L3, systems L3, coding-int L3; a brief writer for mock-oa-code, mock-superday-research, mock-oa-quant-data (`docs/briefs/mocks.md`) and exam topic-3.5 (pattern `docs/reports/exam-3.3.md`).
- Wave 2: `requires` mapping (brief section 8; `course.json` field only), second reader and fix; research-int L4, systems L4 with their drills; mock-oa-code; mock-superday-research.
- Wave 3: coding-int L4; mock-oa-quant-data; exam topic-3.5.
- Wave 4: second reads and fix passes for the three courses (voice 0 and 0) and engine pass E; topic 3.5 closing commit.
- If limits allow: ito L2 (topic 3.2).

After each wave: an answer check per new level, mock and exam (DECISIONS "Fresh numbers in reviews and homework"), a fix agent, changed keys rechecked.

Close: local CDN (`bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`); split playthrough (four lesson shards, then `--sets`, `--exams`, `--bank all`, `--drills`, `--routes-only`) with and without `--mobile`; PLAN ticks; state files; NEXT_PROMPT.

Files: `app/js/`, `app/tools/`, every `course.json`, the three course folders, `app/content/{drills,exams,data}/`, `docs/briefs/mocks.md`, `docs/AUTHORING.md`.

Acceptance: validate 0 errors, no `requires` cycles; a locked Stage 3 lesson shows a correct card, test-out unlocks it, Strict mode hides "Open anyway"; all topic 3.5 levels, mocks and topic-3.5 green with and without `--mobile`; answer checks clean; split runs green.
