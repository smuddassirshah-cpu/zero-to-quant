# A second auto item for one-item exam skills (session AG, PLAN task 4)

The main session fills EXAMS and NAME. BRANCH = `claude/session-ag-route-done-h65un0`. SCRATCH = `/tmp/claude-0/-home-user-zero-to-quant/7c3cbe50-6413-5158-822a-1251e413cde0/scratchpad`.

Your working directory is a git worktree. First: if `git merge-base --is-ancestor BRANCH HEAD` fails, run `git reset --hard BRANCH` inside your worktree (allowed and expected; never check BRANCH out; never edit outside your worktree path and your scratch folder; commit there yourself; ignore any other branch name in CLAUDE.md). Local CDN: `SCRATCH/pkgs`. Python: `SCRATCH/venv/bin/python`.

## Why

A passing topic exam attempt meets a level unless it scored under half on one of the level's essential skills over the exam's auto (non-longform) items (`app/js/prereq.js`, `EXAM_SKILL_FLOOR`). Where an exam holds one auto item on such a skill, one slip locks the level. `docs/reports/engine-pass-ae-2.md` lists the 109 (exam, level, skill) triples, 62 (exam, skill) pairs. Every pair gets a second auto item.

## Author

For each exam in EXAMS:
1. Recompute the pairs yourself from the exam file, every `course.json` of the topic and the rule in the report (the table is from 16 Nov); list them in your report. Work from your list.
2. Give every listed skill a second auto item that tests that skill, at the difficulty mix the exam already has. In this order of preference: (a) a new item, while the exam has fewer than 30 items (validator: 20 to 30); (b) a new item carrying two listed skills, only where the item cannot be answered without both; (c) a new item in place of an existing one whose skills each keep at least two other auto items after the swap (remove the weakest or most duplicated; list every removed id with its skills in the report); (d) if a pair still cannot be placed, leave it, say so, and name the cap as the reason. Never tag a skill on an item that does not test it. Check afterwards that no skill of the exam fell to one auto item.
3. Reuse: a new item shares no number set, story, function, matrix, data or sentence with any item of the exam, the stage and mock exams that carry the same courses, nor with the lessons, reviews, homework, problem sets and Fluency sets of its course. Read the course's level that teaches the skill and the exam's existing item on the skill first; the new item is a different task on the skill, not the old one with new numbers. Run `cd app && node tools/fresh-check.mjs --file content/exams/<exam>.json` and read its hits on your items.
4. Every item follows `docs/AUTHORING.md` (exam section, section 6 voice) and the shape in `docs/reports/exam-1.8.md`. Numeric items state their form; bands take the printed value and refuse every `wrong` value; no key or slip on a rounding tie; a tail or table value names its source; a percentage carries unit "%". Code items: the solution passes the hidden tests, the starter fails them.
5. Every stated number computed twice: `docs/reports/exam-second-item-NAME-numbers.py` (paths from `__file__`, exit 0) recomputes every key, `wrong` value and printed number of the new items.
6. Exam minutes: unchanged where the item count is unchanged; otherwise scaled pro rata and rounded to 5, with the hours note in your report (the main session runs `readiness-sums.mjs --write`).
7. Gates: validator 0 errors; `VOICE_BASE=app/content/exams python3 docs/reviews/voice-scan.py 35` 0 and 0 on your files; `node tools/grade-all.mjs --file content/exams/<exam>.json --local-cdn SCRATCH/pkgs` 0 failures; `node tools/playthrough.mjs --exam <id> --local-cdn SCRATCH/pkgs` with and without `--mobile`. Heavy commands one at a time, each under two minutes or split.
8. Report `docs/reports/exam-second-item-NAME.md`: per exam, the pairs, the new item ids with skill, difficulty and widget, removed ids, pairs left. Engine limits to `docs/BACKLOG-INBOX.md` under `Raised later (exam second item NAME):`.

Commit per exam ("exam <id>: second auto item for one-item skills"), staging by explicit path, `git checkout app/content/manifest.json` first, a blank line after the subject, then:
Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01E26gTPq3dJJ8ftKMHkfKfV
Start nothing in the background; never push; edit no exam outside EXAMS and no course file. Scratch in `SCRATCH/exam2-NAME/`. Hand back at most six lines: commits, items added and removed per exam, pairs left, gate results.

## Reader

You are the second reader of the new items named in `docs/reports/exam-second-item-NAME.md`. You read and report; you edit no content; no browser. Run the author's script; recompute every key, `wrong` value and printed number yourself by another method in `docs/reports/exam-second-item-NAME-numbers-read.py` (exit 0, a `FINDING` line per failing check). Check that each item tests the skill it is tagged with and cannot be passed without it, that every listed pair now has two auto items, and that no skill fell to one. Reuse: per item, name the closest exam item, lesson screen, review, homework and problem-set item and rule `clean` or `reuse` with both texts. Bands, ties, units and sources as in Author rule 4. Tools: validator, voice scan, `grade-all.mjs --file`. Write `docs/reviews/review-exam-second-item-NAME.md` (`N. file | JSON path | severity | problem | evidence | exact fix`; wrong, misleading, reuse, voice, continuity; every fix exact, recomputed). Commit review and script, same trailers. Hand back at most six lines.

## Fixer (Sonnet)

Apply the review with targeted edits to the exam files only: each exact replacement, recomputed; dispute with numbers; update the author's script; both scripts exit 0; gates of Author rule 7 on edited exams; append `## Fix pass` to the review; commit. Hand back at most six lines.
