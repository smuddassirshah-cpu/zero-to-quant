NEXT_PROMPT: after session AJ (concept audit, session 13)

The build is complete (`DONE`). Read CLAUDE.md, `docs/reports/concept-audit-next.md`, audit notes session 13 and DECISIONS "Session AJ". If the census disagrees with the figures below, fix the state files first.

Push to the branch the harness assigns and to `claude/amazing-wright-d4mx7i` (CI), only when no run is in progress there. `claude/fable-audit` is stale and fully merged: do not use it. Lesson ids are never renamed.

Default track: the concept audit (PLAN 5b), run from the content session with the rules of `docs/briefs/concept-audit.md` and the procedure of `docs/briefs/fable-audit-session-prompt.md`.

1. ds L4 round 2 (round 1: 5 `wrong`, all fixed and read).
2. graphs-dp L4, cpp L4 and L5, markets (check scope rule (a) first).
3. Problem sets added since close in conditional, ito, limits-thm, markov, measure-prob, numerics, odes, pdes, random-vars: one course per read.
4. Fluency sets: number-sense L1 to L3, markov fluency-l2.

Agent worktrees start on the repository's three-commit initial history: every agent prompt begins with `git checkout -B <own branch> <commit>`. Code courses: sweep every `test-N` line by submission and add `mutants`. Local number scripts need the pinned versions (`.github/actions/zq-setup/requirements.txt`); unpinned scikit-learn 1.9 and pandas 3.1 fail 6 scripts in untouched courses. Local `playthrough --changed` has no green cache here and replays everything: play edited files only.

Other track (user's choice): post-completion engine work, `docs/ENGINE-BACKLOG.md` and `docs/BACKLOG-INBOX.md`.

Acceptance: validator 0 errors; edited files played desktop and mobile; a green `acceptance.yml` run on the pushed HEAD.

Expected census: lessons 1,236; levels 283; reviews 283 (items 2,558); exams 29 topic, 4 stage, 16 mock; drills 270; Fluency 100 (families 318); problem sets 167 (items 617); bank 36 files, 400 items; hours 3,695, gap 0; edges 266; validator 0 errors (4,610 warnings); same-course reuse 0 errors, 44 waived; number scripts 436.
