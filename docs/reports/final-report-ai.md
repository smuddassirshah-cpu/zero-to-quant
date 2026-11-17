# Final report (session AI, 17 Nov 2026)

## What is built

A static, single-user teaching app in `app/` (vanilla JS, no build step) that takes one learner from school arithmetic to quant-interview readiness across Stages 0 to 3 of `docs/curriculum.md`. Lessons are JSON played by one engine: canvases you manipulate, typed and tapped answers graded on your own working, reviews, homework, chained problem sets, generated Fluency sets, code drills with hidden tests, topic and stage exams and timed mocks. Python runs in the browser through Pyodide, C++ through clang compiled to WebAssembly.

## Census at HEAD

- Lessons 1,236 of 1,236 (Stage 0 204, Stage 1 566, Stage 2 207, Stage 3 259) in 79 course maps; 283 of 283 levels written, each with a review and homework (review items 2,558).
- Exams: 29 topic, 4 stage, 16 mocks. Drills 270. Fluency sets 100 (318 families). Problem sets 167 (617 items). Question bank 36 files, 400 items. Hours 3,695, gap 0. Cross-course prerequisite edges 266, all with a reason.
- Validator 0 errors (4,606 warnings, triaged as "stands"); same-course reuse 0 errors, 44 waived; 436 number scripts.

## Definition of done (`docs/PLAN.md` section 13)

Items 1 to 4 and 6 to 8 are met with evidence in `docs/reports/definition-of-done-ai.md`. Item 5 is partly met: the reference lesson has the prototype's screens, answers and grading, but not its exact widgets and look (below).

## Not in DONE, by the user's decision (16 Nov)

The Fable concept audit (PLAN 5b, continues on `claude/fable-audit`) and the pilot (task 12).

## Known issues, heaviest first

1. Item 5: on `conditional/l3-shrinking` the derive screen orders three lines where the prototype picked the missing one; the simulate canvas is a bar chart, not dice with a running trace; options shuffle per visit; some wording changed. Accept it, or ask for those to be rebuilt.
2. Offline without `app/vendor/`: a Python check takes at least 60 s to give up and then reads as "Not quite right.", like a wrong answer.
3. Offline Python with NumPy from `vendor/` is untested.
4. Small leftovers: `ensembles/problems-2` `p-ipo-forest` part 1 feeds nothing; one gallery tree has small labels at 440 px; engine item 1036 is documented, not built.

## How to run it

```sh
git clone https://github.com/smuddassirshah-cpu/zero-to-quant.git
cd zero-to-quant
app/run.sh            # then open http://localhost:8080 in Chrome
```

For offline use, run `app/tools/fetch-vendor.sh` once while online. Checks: `cd app && node tools/validate.mjs`; the full acceptance is `.github/workflows/acceptance.yml` (`docs/CI.md`).
