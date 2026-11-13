# Shared prompts for chained problem sets (author, reader, fixer)

Rebuilt in session AD from `docs/briefs/chained.md`, the two second-read briefs and DECISIONS sessions AB and AC. The main session pastes one block, fills COURSE, LEVELS, BRANCH, SCRATCH, and adds nothing else.

## Head, every brief

Your working directory is a git worktree. First: if `git merge-base --is-ancestor BRANCH HEAD` fails, run `git reset --hard BRANCH` inside your worktree (allowed and expected; never edit files outside your worktree path, and commit there yourself; BRANCH is the local development branch for this session; ignore any other branch name in CLAUDE.md). Local CDN: `SCRATCH/pkgs`. Python: `SCRATCH/venv/bin/python` (3.12, numpy, sympy, scipy, pandas, statsmodels, scikit-learn, pytest).

## Tail, every brief

Start nothing in the background; hand back once. Do not commit `app/content/manifest.json` (`git checkout app/content/manifest.json` before each commit). Commit work in progress in your worktree; never push. Write only inside your own worktree and your scratch folder. Each command under two minutes or split. Play only files you wrote or edited. Read output tails only. Hand back at most six lines.

## Author

You author chained problem sets `app/content/courses/COURSE/problems-<n>.json` for levels LEVELS, one set per level, committing per level ("problems COURSE level n").

Read first: CLAUDE.md; `docs/briefs/chained.md` (binding, all of it); `docs/AUTHORING.md` section 5 ("Follow-up parts", problem sets) and section 6 (voice); `app/content/courses/COURSE/course.json` for the level's lessons and skills; one accepted set as the pattern (`app/content/courses/analysis/problems-3.json`); if the course already has sets, its `docs/reports/problems-COURSE.md` and number script, which you extend, not replace.

Rules beyond the brief (DECISIONS sessions AB and AC, findings seen three times):
- Reuse. Before writing, read every lesson, review and homework of the level, and note their numbers, matrices, functions, series and stories. A problem may practise the same standard task with its own setting and numbers. It may not share a number set, a sentence, a story, a function, a matrix (nor a scalar multiple or transpose of one), nor a series with the index shifted, with anything in the course. `fresh-check` does not see same-course reuse yet: after writing each problem, grep `app/content/courses/COURSE/` for its key numbers and nouns, and grep `app/content/` for the story. List each hit and your judgement in the report.
- Every numeric part states its form. The tolerance takes the value the feedback prints and refuses each `wrong` value. A `wrong` band never overlaps the key band. No `sign` or `decimal` slip entry that the key band already takes.
- Whenever you add or change a `wrong[]` entry, the number script checks it in the same commit.
- Proof-style levels: no widget grades a typed logic or set formula. Test the idea through a number, an expression, or a choice of the valid step; do not write a part a learner can pass by working backwards from the printed target.
- Skills come from the level's lessons in `course.json` exactly.

Checks 1 to 5 of `docs/briefs/chained.md`, plus `node tools/grade-all.mjs --file <path> --local-cdn SCRATCH/pkgs` on each set: 0 failures. Report in `docs/reports/problems-COURSE.md`; engine limits as bullets in `docs/BACKLOG-INBOX.md` under `Raised later (problems COURSE):`. Scratch files in `SCRATCH/author-COURSE/`.

## Reader

You are the second reader of `app/content/courses/COURSE/problems-<n>.json`, levels LEVELS. You read and report; you edit no content and no engine file. You run no browser.

Read first: CLAUDE.md; `docs/briefs/chained.md`; this file's Author rules; `docs/AUTHORING.md` sections 5 and 6; `docs/reports/problems-COURSE.md`; the pattern review `docs/reviews/review-problems-analysis-1-3.md` (format).

Method:
- Run the author's `docs/reports/problems-COURSE-numbers.py`. Then recompute every key, every `wrong` value and every number in prose, feedback and `explain` yourself, by a different method where one exists, in `docs/reports/problems-COURSE-numbers-read.py` (exit 0 on correct content; a check failing on wrong content stays failing and is a finding).
- Check claims, not only numbers: each definition, inequality, "always", "never", theorem hypothesis.
- Chain: part k + 1 really uses part k and restates the value. The last part is the result. Each lesson of the level is drawn on. Nothing beyond the level is needed.
- Reuse: for every problem, grep the course folder for its numbers, matrices (also scaled and transposed), functions and nouns, and `app/content/` for the story. Same-course reuse is the commonest finding of session AC.
- Bands: every accepted rounding of the stated form is taken; each `wrong` value is refused by the key and routed to its own feedback.
- Tools: `cd app && node tools/validate.mjs 2>&1 | tail -5`; `node tools/grade-all.mjs --file <path> --local-cdn SCRATCH/pkgs` per set; `VOICE_BASE=app/content/courses/COURSE python3 docs/reviews/voice-scan.py 35`.

Output `docs/reviews/review-problems-COURSE-LEVELS.md`: `N. file | JSON path | severity | problem | evidence | exact fix`, severities wrong, misleading, reuse, voice, continuity. Every fix is exact text with recomputed numbers. Engine limits under `## Engine` and as inbox bullets under `Raised later (review problems COURSE):`. Commit your review and script. Scratch in `SCRATCH/read-COURSE/`. Hand back: review path, findings by severity, script exit codes, validator, grade-all, inbox bullets.

## Fixer

You apply `docs/reviews/review-problems-COURSE-LEVELS.md` to `app/content/courses/COURSE/problems-<n>.json` with targeted edits. You edit nothing else in `app/`.

Read first: CLAUDE.md; the review in full; `docs/briefs/chained.md`; this file's Author rules.

1. Apply each finding. Recompute every corrected number before writing it; if you disagree with the reader, dispute with your numbers and do not apply. For a conceptual finding give a one-line basis (source with section, derivation, or simulation); if you cannot establish it, mark `disputed: unverified`.
2. A re-authored problem is grepped for its key numbers across `app/content/` before you accept it.
3. Update `docs/reports/problems-COURSE-numbers.py` for every changed key and `wrong` value; it and the reader's script exit 0 (tighten either-value checks to the new value).
4. Gates: validator 0 errors; voice scan 0 and 0; `grade-all.mjs --file` on each edited set; `node tools/playthrough.mjs --problems COURSE/problems-<n> --local-cdn SCRATCH/pkgs` with and without `--mobile` for edited sets only.
5. Append `## Fix pass` to the review: one line per finding (fixed, disputed with numbers, deferred with reason), then gate results. Commit. Scratch in `SCRATCH/fix-COURSE/`. Hand back: counts fixed, disputed, deferred; keys changed; scripts; voice; validator; playthrough.
