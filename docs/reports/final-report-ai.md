# Final report (session AI, 17 Nov 2026)

## What is built

A static, single-user teaching app in `app/` (vanilla JS, no build step) that takes one learner from school arithmetic to quant-interview readiness across Stages 0 to 3 of `docs/curriculum.md`. Lessons are JSON played by one engine: canvases you manipulate, typed and tapped answers graded on your own working, reviews, homework, chained problem sets, generated Fluency sets, code drills with hidden tests, topic and stage exams and timed mocks. Python runs in the browser through Pyodide, C++ through clang compiled to WebAssembly.

## Census at HEAD

- Lessons 1,236 of 1,236 (Stage 0 204, Stage 1 566, Stage 2 207, Stage 3 259) in 79 course maps; 283 of 283 levels written, each with a review and homework (review items 2,558).
- Exams: 29 topic, 4 stage, 16 mocks. Drills 270. Fluency sets 100 (318 families). Problem sets 167 (617 items). Question bank 36 files, 400 items. Hours 3,695, gap 0. Cross-course prerequisite edges 266, all with a reason.
- Validator 0 errors (4,606 warnings, triaged as "stands"); same-course reuse 0 errors, 44 waived; 436 number scripts, all passing on both CPU paths.
- Acceptance: CI run 43 at 529f3c3a (full suite, full mode) green, 30 jobs.

## Definition of done (`docs/PLAN.md` section 13)

All eight items are met, with evidence in `docs/reports/definition-of-done-ai.md`. Item 5 by your decision of 17 Nov: the reference lesson has the prototype's screens, answers, grading and simulation visual (dice, counters, the share of total 10 among kept rolls against 1/11); its derive screen stays an ordering task, which you judged better than the prototype's pick-a-line.

## Not in DONE, by the user's decision (16 Nov)

The Fable concept audit (PLAN 5b, continues on `claude/fable-audit`) and the pilot (task 12), both run independently after `DONE`.

## Known issues, heaviest first

1. The gated Run buttons on a predict-first screen are disabled before the check but do not look dimmed; the note "Answer first, then run it." is the only cue.
2. The first CI run after a change to `fetch-vendor.sh` downloads the 389 MB Pyodide release again (later runs use the cache).
3. Small leftovers from session AH: `ensembles/problems-2` `p-ipo-forest` part 1 feeds nothing; one gallery tree has small labels at 440 px; engine item 1036 is documented, not built.
4. 4,606 validator warnings remain, each class triaged as "stands".
5. One review script (`stat-learning-4-scripts/read-numbers.py`) passes on widened tolerances, not on the Pyodide values the learner sees.

## How to run it

```sh
git clone https://github.com/smuddassirshah-cpu/zero-to-quant.git
cd zero-to-quant
app/run.sh            # then open http://localhost:8080 in Chrome
```

For offline use, run `app/tools/fetch-vendor.sh` once while online; with no copy and no network, a code check now says within seconds that Python or C++ could not load, not that the answer is wrong. Checks: `cd app && node tools/validate.mjs`; the full acceptance is `.github/workflows/acceptance.yml` (`docs/CI.md`).
