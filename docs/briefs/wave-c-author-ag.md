# Wave C author (session AG): chained problem sets for 3.2 and 3.4

The main session fills COURSE and LEVELS. BRANCH = `claude/session-ag-route-done-h65un0`. SCRATCH = `/tmp/claude-0/-home-user-zero-to-quant/7c3cbe50-6413-5158-822a-1251e413cde0/scratchpad`.

Your working directory is a git worktree. First: if `git merge-base --is-ancestor BRANCH HEAD` fails, run `git reset --hard BRANCH` inside your worktree, or `git merge --ff-only BRANCH` if the reset is refused (never check BRANCH out; never edit outside your worktree path and your scratch folder; commit there yourself; ignore any other branch name in CLAUDE.md). Local CDN: `SCRATCH/pkgs`. Python: `SCRATCH/venv/bin/python`.

Your brief is `docs/briefs/chained-prompts.md`: "Author", "Tail, every brief" and "Session AE additions", all binding, with `docs/briefs/chained.md`. Added for this wave:

1. Exams are in the reuse scope. Before writing, read every item of the topic, stage and mock exams that carries one of the course's skills (exam items name skills, not courses: take the skill ids from `course.json` and search `app/content/exams/*.json` for them). Since engine pass 8 `fresh-check --file` reads those items too and reports a hit as an error for a new set.
2. Per problem, the report names the closest lesson screen, quiz item, review item, homework item and exam item, with one line on how the problem differs from each.
3. No problem walks through several quiz, review or exam items in a row, and none retells a lesson screen with other nouns or numbers. A problem is a new chain on the level's skills.
4. New validator rules (AUTHORING section 5, engine pass 8): `[working-band]` the key band takes the value the part's printed working gives; `[rounding-tie]` no key or slip on a rounding tie at the asked places; `[table-source]` a part that needs a tail, quantile or table value gives it or names its source; `[percent-unit]` (error) a percentage part carries unit "%"; `[wide-wrong-tol]` a slip band no wider than its value warrants. Your sets carry none of these warnings.
5. `[slip-line]`: a slip feedback line identical to one in the course, or differing in one number, is a hit. Write each slip line for its own part.
6. Proof-heavy levels: test the idea through a number, an expression or a choice of the valid step; no part passable by working backwards from a printed target.
7. Gates per set, in this order: validator 0 errors (before any playthrough); voice scan 35, 0 and 0; `node tools/fresh-check.mjs --file <set>` 0 errors (use `--pairs` to see every matched pair; `--files a,b,c` for several sets); the number script exits 0; `node tools/grade-all.mjs --file <set> --local-cdn SCRATCH/pkgs` 0 failures; `node tools/playthrough.mjs --problems COURSE/problems-<n> --local-cdn SCRATCH/pkgs` with and without `--mobile`. Heavy commands one at a time; other agents share the machine.

Commit per level ("problems COURSE level n"), staging by explicit path, `git checkout app/content/manifest.json` first, a blank line after the subject, then:
Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01E26gTPq3dJJ8ftKMHkfKfV
Report `docs/reports/problems-COURSE.md`, number script `docs/reports/problems-COURSE-numbers.py`. Scratch in `SCRATCH/author-COURSE/`. Hand back at most six lines: commits per level, problems and parts per set, gate results, inbox bullets.
