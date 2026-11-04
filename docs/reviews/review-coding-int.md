# Topic 3.5 (coding-int): second-reader findings

Scope: every file in `app/content/courses/coding-int/` (l1 to l19, review-1 to review-4, homework-1 to homework-4; 28 files plus `course.json`), the ten `ci-*` drills in `app/content/drills/` and the link to `app/content/exams/mock-oa-code.json`.
Method: every code widget (54 in lessons and homework, 10 drills) run in a harness against its own solution and starter; mutation testing of every Python solution (1,130 single-edit mutants, `scratchpad/review-coding-int/mut.py`) plus hand-written wrong solutions per item (`wrong.py`); C++ items compiled with `g++ -O1 -fno-exceptions` and run against the hidden tests; mechanical script checks (`mech.py`); voice scan (`docs/reviews/voice-3.5-coding-int.txt`); prose read screen by screen for algorithmic claims. Arithmetic keys were not redone (see `answers-2026-11-04-coding-int-3.md`, `-4.md`).
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong claim or a wrong solution that passes the hidden tests; warning = weak test, explanation or metadata; note = style.

(Findings are appended below as the review proceeds.)

## Test strength: wrong solutions that pass every hidden test

