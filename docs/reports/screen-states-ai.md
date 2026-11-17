# Screen states test (definition of done items 3, 4, 6), session AI

`app/tools/test-screen-states.mjs [--local-cdn <pkgs>]`, run in the CI `tests-browser` ui leg. Green, 124 s locally.

- Item 3: 27 routes (every id from `ZQ.screens` plus real params: course, lesson, review, homework, exam topic and mock, problems, testout, fluency, drill, prepare paths, practice, weekly, warmup, redo, bank, system, setup) on an empty state, a populated state, and a truly empty profile (all but #system must land on #setup), at 1280 and 440 px. Asserts text, no render-failed card, no page or console error except blocked jsDelivr. The populated state comes from playing a lesson, a level review and a problem set through the `ZQ.test` hooks, plus an exam attempt with a miss, a fluency result and a redo item; the test checks it holds progress, XP, MP, streak, skills, redo, problems, exams, hours, fluency.
- Item 4: the mini fixture is validated into a temp folder (manifest written) and served as the app's content. Course map shows "Not yet written"; the unwritten lesson, review and homework routes show a card; Learn and Today render. No new fixture files were needed (algo-think already has unwritten lessons).
- Item 6: export, import into a fresh context, deep-equal of every key; again after reload; a wrong version and non-JSON are refused with state untouched.
- Mutation check: a `you` screen throwing on empty state and an import that zeroed `mp` both failed the test (5 failures); reverted.
- Engine faults found: none.
