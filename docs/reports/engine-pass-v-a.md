# Engine pass V-A (runtime and exams), items 591 to 599

Scope: `app/js/**`, `app/css/screens/exam.css`, `app/tools/playthrough.mjs`, the new `app/tools/test-engine-runtime.mjs`, and the AUTHORING.md sections for choice and multi, expression, code (and the C++ addendum), exam papers and drawn items. Nothing under `app/content/**`, `validate.mjs`, `fresh-check.mjs` or `merge-wave.sh` was touched.

## Items

| Item | What changed | Where |
|---|---|---|
| 591 shuffle | `choice` and `multi` shuffle unless `shuffle: false`. The order is seeded from the draft key, the screen key, the item id, the option ids and `ZQ.attempt`. `ZQ.attempt` is new at every route change (`core.js`); an exam sets it to its seed, so `#exam/<id>/<seed>` fixes the order. | `widgets/_base.js` `orderOptions`, `choice.js`, `multi.js`, `player.js` `buildScreen`, `core.js`, `exam.js` |
| 592 required | `required: true` on a paper item fails the paper when wrong, whatever the share. Start card rule, per-paper count, an in-paper tag, a result line and per-paper question numbers. `passedAuto` reads the same rule. | `mock.js` `requiredMissed`, `passed`; `exam.js`; `css/screens/exam.css` |
| 593 tracks | `tracks` on a mock paper. Off-track learners (including Undecided) do not sit it; the start card names it and links `#exam/<id>/all`. With `all` it is optional and never gates; `as-<role>` sits as that role. The playthrough sits tracked exams through `all`. | `mock.js` `roleOf`, `paperFor`; `exam.js`; `playthrough.mjs` `xr()` |
| 594 seen | A draw sat in any other exam or mock counts as seen (rank 0.75, below a sitting of this exam, above a library solve). Label "Previously seen: sat in another exam". | `mock.js` `seenInfo`, `seenLabel` |
| 595 importHint | A code test's `setup` is read for imports (function and script mode). | `widgets/code.js` `harness`, `scriptHarness`; exports `Z.widgets.codeImports` for the test |
| 596 expression form | `form: "rectangular"` and, on a constant answer, `simplified` also refuses what is left undone. Works on Compute Engine canonical MathJSON (`iota` is the imaginary unit after `prep`). Without the engine the text fallback is unchanged. | `widgets/expression.js` `exprForms` |
| 597 Skip test | Automated test of the 589 Skip marking path, plus Finish marking. | `tools/test-engine-runtime.mjs` |
| 598 written part | A `longform` part inside `parts` is worth ticks over points. The item's credit is the sum over parts; "right" still needs every part right. | `player.js` `renderParts` `gradeAll`; `mock.tally`; `exam.js`; `review.js` (homework marks, timed-set total) |
| 599 libc++ | Extensive hardening with the enforce semantic: bounds messages kept, internal checks off. | `screens/cpp-worker.js`; AUTHORING C++ addendum |

## Decisions worth a second look

- **Shuffle seed.** "Per attempt" is a page visit (route change) for lessons, reviews, homework and drills, and the attempt seed for exams and mocks. A Retry inside one visit keeps the order, which is what makes the layout stable under Try again.
- **Tracks, off-track default.** Left out, not optional-and-sat, so a trader is not made to sit a research prompt. The link on the start card is the opt-in. Undecided is treated as off-track; if the orchestrator prefers "Undecided sits everything, ungated", change `role` handling in `exam.js` (one line).
- **Role ids.** `trader`, `research`, `strats`, `developer` as in `prep.json`; `researcher` is accepted as `research`.
- **Expression form scope.** `rectangular` and constant-`simplified` are structural checks on MathJSON, not a re-evaluation: `1+\sqrt{2}` passes, `2+3` fails, `\frac{1}{2}+\frac{1}{3}` fails (two plain fractions added), `e^{i\pi/3}` fails `rectangular`.
- **libc++.** `_LIBCPP_ENABLE_EXPERIMENTAL` is needed only because libc++ refuses a hand-set assertion semantic without it. It declares experimental headers and links nothing. Measured with the packaged clang in node (WASI): 20,000 map inserts and erases 1,730 ms (debug), 11 ms (extensive), 7 ms (extensive with messages). Lost: the comparator strict-weak-order check and the pedantic checks.

## Tests

- `node tools/test-engine-runtime.mjs --local-cdn <pkgs>` (desktop and `--mobile`): unit (30 expression cases on real Compute Engine output, 3 importHint cases) and browser (shuffle 6, required 6, tracks 8, Skip marking 4, written part 2, seen 3, no page errors).
- All existing `app/tools/test-*` files, validator and playthroughs: see "Results" below.

## Content edits needed (for a Sonnet fixer)

1. `required: true` on the stage code exits named in `review-exam-stage-1`, `-stage-2`, `-stage-3`, `-mock-oa-code-hard` and `-mock-superday-strats` (the items, not the papers).
2. `form: "rectangular"` (or `"simplified"`) on constant `expression` answers named in `review-exam-1.11` (complex division and the like).
3. `shuffle: false` on any `choice` or `multi` whose options are ordered or refer to each other; agent B's `O2-unshuffled-numeric` (73 hits at the start of this pass) and `[shuffled-position]` rules list them. Nothing changes in the meantime except that the order moves.
4. Optional: drop an unused `import pandas as pd` that a starter carried only so a hidden `setup` would run (595).
5. Optional: a `tracks` list on the research or strats technical prompt papers of `mock-video`, `mock-superday-research` and `mock-superday-strats`, as `review-exam-mock-video` asked.

## Results

- `node tools/validate.mjs` from `app/`: 0 errors (3,978 warnings, unchanged class mix).
- `test-engine-runtime.mjs`: 63 of 63, desktop and `--mobile`.
- Every other `app/tools/test-*.mjs` and `test-numbers-lib.py`: pass. `test-merge-wave.sh` fails in this worktree on `error: Could not read <sha>` from its own temporary git repositories (agent B's file, untouched by this pass; it does not load any file under `app/js`); re-run once, same result.
- Playthrough `--all --shard i/4 --local-cdn`, staggered 75 s apart: shard 1/4 (458 items and the routes), 2/4 (458), 3/4 (458), 4/4 (457) all passed, 0 browser relaunches. A first attempt was stopped at the 30-minute background limit (two "threw" lines were the killed browser; both lessons passed on their own).
- `--routes-only --local-cdn` desktop and `--mobile`: all passed.
- Targeted before the shards: `cpp/l22-undefined-behaviour`, `conditional/l3-shrinking`, `mock-video`, `topic-1.5`.
