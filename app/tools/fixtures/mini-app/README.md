# mini-app: the small content root the test-validate-* tests run on

A cut-down copy of `app/content`, laid out like `app/` so that `node tools/validate.mjs --root tools/fixtures/mini-app/content`
checks it (the folder above `--root` plays the part of `app/`; its `tools/` would hold perf-pending.json and the problem-set and
Fluency fixtures, and the harness adds those only when a case asks). It validates with 0 errors in about 0.4 s. It is used only
through `tools/lib/validate-harness.mjs`, which copies it to a temp folder per test. `census`, `fresh-check`, `grade-regression`
and the playthrough read `app/content`, never `tools/fixtures`, so nothing counts these files as content.

What is in it
- Courses `algo-think`, `first-python`, `equations`, `odes`, `recruiting`: the real `course.json` maps (every level and lesson id), but only
  the lessons, reviews and homework the scratch cases plant into (algo-think l1 and l11, first-python l8, equations l1, l3 and all of
  level 3, odes review-1, and the sets that go with them). The rest are "not yet written" warnings, as in the real tree.
- Equations also holds a Fluency set (`fluency-l3-opening-brackets`) and a problem set (`problems-3`); level 3 is fully written so the
  problem-set skill rule still has a level to compare against.
- Exams `topic-0.7`, `mock-oa-strats`, the `mock-oa-sig` and `mock-oa-trader` families with their -2 and -3 versions; a bank file; two drill
  files and their `drills/index.json` rows; `warmup.json`, `capstones.json`, `readiness.json`, `curriculum.json` and an invented `prep.json`.

Where it differs from the real files (edits, all in this folder only)
- `requires` entries that named a course outside the mini set were dropped; algo-think level 1 requires `first-python/L2` with a why.
- Exam `skills` and exam `requires` that named courses outside the set were mapped to `at-complexity`, `first-python/L2` and `equations/L1`.
- The two drills' `course` is `algo-think` where it named another course; `readiness.json` lists only the five courses and says it is a fixture.
- `curriculum.json` keeps the topics of the five courses, and `prep.json` is a two-path invention that names the three mock families.

It carries the real lessons' own warnings (about 64: not-yet-written lines, O2 voice notes, key-length and so on). A case asserts on the tag
or message of its own planted fault, never on "no warnings at all". Keep any edit here small, and run `node tools/test-validate-harness.mjs`
and the 16 other test-validate-* files afterwards: several plant into specific screens (algo-think l1 screens 2, 3 and 7, equations
problems-3) and expect them where they are.
