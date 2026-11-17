# Re-author brief, older sets (session AF)

Your working directory is a git worktree. First: if `git merge-base --is-ancestor claude/session-ag-route-done-h65un0 HEAD` fails, run `git reset --hard claude/session-ag-route-done-h65un0` inside your worktree (allowed and expected; never edit files outside your worktree path and your scratch folder, and commit there yourself; that branch is BRANCH, this session's development branch; never check it out; ignore any other branch name in CLAUDE.md). SCRATCH = `/tmp/claude-0/-home-user-zero-to-quant/7c3cbe50-6413-5158-822a-1251e413cde0/scratchpad`. Local CDN: `SCRATCH/pkgs`. Python: `SCRATCH/venv/bin/python`. Scratch: `SCRATCH/reauthor-COURSE/`.

You are an author agent. The extended same-course reuse check fired on existing problem sets, and a reader ruled the items named in your task `re-author` in `docs/reviews/review-reuse-af-hits.md`: grep that file for your course and read every line on your items (the lines name the lesson screens, quiz, review and homework items each must not walk).

Read first: CLAUDE.md; `docs/briefs/chained-prompts.md` in full ("Author", "Tail, every brief", "Session AE additions": all binding); `docs/briefs/chained.md`; `docs/reports/problems-COURSE.md` and its number script; the set you edit; every lesson, quiz, review and homework item of the level, and the topic exam that covers the course (`grep -l COURSE app/content/exams/topic-*.json`), which is in the reuse scope.

Work:
1. Replace each named item (or only the named parts, where the review says "parts n and m only") by new work on the same skills, with its own setting, data and chain of steps. It walks none of the named screens and no other screen, quiz, review, homework or exam item of the course at any level, and shares nothing with the other problems of the course's sets. Where only numbers are shared, renumber as the review says. Keep the item id (progress data keys on it) unless the id names the old story so plainly that it misleads; say which you did.
2. Do not touch other items of the set, and add no waiver.
3. Update the author's number script for every new key and `wrong` value; it and every reader script of the course in `docs/reports` exit 0 (retarget reader checks of replaced parts, saying so). Update the report with, for each new item, the closest lesson screen, quiz, review, homework and exam item and why it is not a walk through it.
4. Gates on each edited set: validator 0 errors (run it before any playthrough); voice scan 35, 0 and 0; `node tools/fresh-check.mjs --file <set>` 0 errors, and `node tools/same-course-reuse.mjs --all 2>&1 | grep COURSE` shows no error for your items; `grade-all.mjs --file <set> --local-cdn SCRATCH/pkgs` 0 failures; playthrough `--problems COURSE/problems-<n> --local-cdn SCRATCH/pkgs` with and without `--mobile`. Run heavy commands one at a time; other agents share this machine.
5. Append to `docs/reviews/review-reuse-af-hits.md` nothing (several agents work from it). Write instead `docs/reviews/review-reuse-af-hits-reauthor-COURSE.md`: one line per item (old task, new task, ids, keys), then gate results. A delta reader reads your new parts next.

Commit per set as it passes ("problems COURSE level n: re-author <ids>"), staging by explicit path, `git checkout app/content/manifest.json` before each commit, with a blank line and then:
Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01E26gTPq3dJJ8ftKMHkfKfV
Hand back at most six lines: branch and commit hashes, items re-authored with new keys, gate results, anything open.
