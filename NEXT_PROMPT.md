Read CLAUDE.md and the four state files; follow the SESSION PROTOCOL. Full standards apply (DECISIONS "Standards restored"). Branch `claude/amazing-wright-d4mx7i` only; if the local ref is behind origin, check out origin (back up before moving a ref).

Task: PLAN 2a item 6, topic 3.2: ito L2 to L4, measure-prob L1 to L4, pdes L1 to L3, exam topic-3.2, second reads and fix. Topic 3.5 and gating closed 4 Nov.

Context not in the state files:
- Briefs `docs/briefs/ito.md`, `measure-prob.md`, `pdes.md` predate engine passes C and E and name an old scratchpad. Give agents the current `pkgs` path. Check each brief's canvas and widget needs against `docs/AUTHORING.md` first; per DECISIONS "Topic 3.5 briefs", raise [Must] items for an engine pass, never workarounds.
- Gating is live (AUTHORING section 11): a level needs `requires` only where its brief names more than the previous level; only a mapping agent edits `course.json`.
- Worktree agents commit as they go; merge per DECISIONS "Parallel worktree merges".
- Pyodide ships SciPy 1.14.1 (KNOWN_ISSUES).

Waves (parallel Sonnet agents, `isolation: "worktree"`):
1. Brief check and engine gaps; ito L2, measure-prob L1, pdes L1.
2. ito L3, measure-prob L2, pdes L2.
3. ito L4, measure-prob L3 and L4, pdes L3.
4. Exam topic-3.2 (brief first, pattern `docs/reports/exam-3.5.md`); second reads and fix passes, voice 0 and 0.
After each wave: an answer check per level, a fix agent, changed keys rechecked.

Close: local CDN (`bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs`); split playthrough (four lesson shards in parallel, then `--sets`, `--exams`, `--bank all`, `--drills`, `--routes-only`) with and without `--mobile`; PLAN ticks; state files; NEXT_PROMPT.

Files: `app/content/courses/{ito,measure-prob,pdes}/`, `app/content/exams/topic-3.2.json`, `docs/reports/`, `docs/reviews/`, `app/js/` if an engine pass is needed.

Acceptance: validate 0 errors; all topic 3.2 levels and exam green with and without `--mobile`; answer checks clean; voice 0 and 0; split runs green.
