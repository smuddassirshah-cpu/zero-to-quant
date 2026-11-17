# Engine pass 7 triage (read only, at 90bd03bc)

Marks: DONE-ALREADY (built, status never updated), BUILD (S under an hour, M a few hours, L a day), DROP, UNSURE, POST-COMPLETION (every [Could], E13, E15 to E19: user decision). Evidence paths are under `app/` unless they start with `docs/`. Nothing was run: every mark rests on reading code, tests and reports.

## 0. Counts

| Set | Items | DONE-ALREADY | BUILD | DROP | UNSURE | POST-COMPLETION |
|---|---|---|---|---|---|---|
| "status: open", [Must] | 9 | 9 | 0 | 0 | 0 | 0 |
| "status: open", [Should] | 38 | 15 | 19 | 1 | 3 | 0 |
| "status: open", [Could] | 70 | 4 | 0 | 0 | 0 | 66 |
| 340 to 422 (83 items, none tagged, none with a status line) | 83 | 79 | 0 | 3 | 1 | 0 (3 leftovers proposed) |
| Deferred inbox list of `engine-pass-7.md` | 10 | 0 | 0 | 1 | 1 | 8 (proposed, untagged) |
| E13, E15 to E19 | 6 | 1 (E13) | 0 | 0 | 0 | 5 |

The 87 "status: open" lines hold 117 items (ranges such as "1028 to 1051").

Surprises:
1. Items 340 to 422 carry no [Must]/[Should]/[Could] tag at all, and 79 of the 83 are built: the code comments name the item numbers ("Pass 7", "item 363"), from the old integration pass 7 (commit ec706cad). Session V's report called them "all others still open" in error.
2. Engine pass 8 part B was built and merged (d2b3a442, `docs/reports/engine-pass-8-reuse.md`), yet its 47 status lines still read "open: engine pass 8 part B". All 9 open [Must] items are in that group and are done.
3. No BUILD item touches a canvas or a CSS file. The System gallery check is not triggered by this work.
4. Outside the 87 lines, 46 more [Must]/[Should] items have no "Done" and no status line (section 7; "705 to 745 (41), all open" at backlog line 1854). They are not in the PLAN wording of pass 7. The coordinator must rule whether they are in scope.
5. The nine untagged inbox bullets deferred by pass 7 were never numbered; their text left the inbox when pass AD cleared it (fc24bf10). Only the names in the report remain.

## 1. Open [Must] (9)

| No | Gist | Mark | Evidence |
|---|---|---|---|
| 1086 | Print every matched pair of a reuse hit | DONE-ALREADY | `tools/same-course-reuse.mjs` `--pairs`, `fmtPairs` (line 380); `tools/reuse-hits-report.mjs` |
| 1087 | Waiver with `source` or `text` | DONE-ALREADY | `same-course-reuse.mjs` waiver match (line 352); `text` is 1152 |
| 1097 | Same-course check missed topic exam near-copies (stat-models) | DONE-ALREADY | exam sources, tag `[exam-reuse]` (line 338); `tools/test-fresh-check-pass8.mjs` |
| 1103, 1107, 1109, 1114, 1118, 1126 | Same-course reuse reads no exam (arma, coint, garch, numerics, convex) | DONE-ALREADY | same; skill-to-course map from `course.json`; CI step "Same-course reuse" in `.github/workflows/acceptance.yml` line 93 |

## 2. Open [Should] (38)

| No | Gist | Mark | Evidence, or files and size |
|---|---|---|---|
| 944 | `form` for a surd in simplest form ($\sqrt{72}$ passes for $6\sqrt2$) | BUILD M | `js/engine/grade.js` `simplestVerdict` (line 792) has no surd branch; test in `tools/test-grade-ab3.mjs` |
| 945 | `form` for a cancelled algebraic fraction | BUILD M | `grade.js` `simplestVerdict`: only a sum over a whole number is judged |
| 951 | A typed % in a field with no `%` unit reads as a hundredth, generic line | BUILD S | `grade.js` `parseNum` line 48 (`if (pct \|\| percent) n /= 100`); `js/engine/widgets/numeric.js`; fix covers 955 and 1077 ([Could]) at no extra cost |
| 1028 | `mutants` list on a code widget, first failing test asserted | BUILD L | no `mutants` in `tools/`; new tool or `tools/planted-check.mjs`; needs the runner of 1031 |
| 1029 | `slip` expression on a `wrong[]` entry, checked against `value` | BUILD M | none in `tools/validate.mjs`; `tools/numbers_lib.py` has `check_wrongs` only |
| 1031 | `grade-all.mjs --code` (node Pyodide runner; also 1008) | BUILD M | `tools/grade-all.mjs` header line 16: code not covered; no `loadPyodide` |
| 1032 | "Times out" tests must fail the naive version by a stated factor | BUILD M | nothing in `tools/perf-rules.mjs` or validator; build on 1031 |
| 1036 | Key `error` fires only on load failure (also 681) | BUILD S | `widgets/code.js` line 576, `widgets/cpp-grade.js` line 736; either key a raise inside a test or document and warn |
| 1037 | Shared no-sort postlude snippet | BUILD S | no snippet in `widgets/code.js`; a helper in the Python prelude library avoids a schema change |
| 1062 | Shared-formula advisory fires on the course's own standard formula | BUILD S | no allowlist in `tools/fresh-check.mjs` or `same-course-reuse.mjs` |
| 1063 | `--problems --mobile` green while inline KaTeX overflows 440 px (also 709, 987) | UNSURE | `tools/playthrough.mjs` line 443 prints only a `note` in the shots loop; line 51 says every width gets the "wider than the window" check. Not run. If it is a note, BUILD S |
| 1079 | Validator advisory `[no-chain]` | BUILD S | no `no-chain` in `validate.mjs` |
| 1081 | A `wrong` value reached from the printed rounded values | BUILD M | `[working-band]` covers the key only; add slip routes to `numbers_lib.py` |
| 1082 to 1085 | `retold` too loose; three false-positive classes | DONE-ALREADY | `tools/retold-reuse.mjs`; `test-fresh-check-pass8.mjs`; stands 50 to 22 |
| 1088 | `rate`: eighths, and a ratio of two stated amounts missed by `numbers` | BUILD S (remainder) | eighths done; the ratio is under "Not built" in `engine-pass-8-reuse.md` |
| 1090 | Identical short feedback line missed | DONE-ALREADY | `[slip-line]`, `retold-reuse.mjs` `slipFires`; paraphrases dropped by the 1148 ruling |
| 1098, 1108, 1116 | `retold` missed slip skeletons in new numbers | DONE-ALREADY (part) | one-number lines fire; the rest is DROP by the 1148 ruling (a slip line in other numbers is stock unless numbers are shared) |
| 1102 | Two short sentences that differ in one number | DONE-ALREADY | closed in `engine-pass-8-reuse.md` |
| 1105 | Chain test against exam parts | DONE-ALREADY | exam sources; closed in the same report |
| 1106 | Chain test reads one source at a time | BUILD M | `retold-reuse.mjs` line 9: "steps of one source" |
| 1110 | Generic line repeated with one clause added | DROP | overtaken by 1147 and 1148; widening `retold` would reverse the triage of 189 warnings |
| 1113 | Gate: check every set of a course when one changes | DONE-ALREADY | CI runs `same-course-reuse.mjs --all` on every push (acceptance.yml line 93) |
| 1115, 1125 | Word-for-word slip line in two course files | DONE-ALREADY | `[slip-line]` |
| 1121 | Question retold with one phrase added (numerics 4) | UNSURE | not in the closed list; needs a run on the named pair at its old commit |
| 1128 | Story reused in its own nouns, task changed | BUILD M | "a story test on rare nouns" is under "Not built"; `retold-reuse.mjs` |
| 1130 | "Using x from part k": slip band narrower than the key band | BUILD S | pass 8 A "Not built: the carry check"; `validate.mjs` `pass8Rules` |
| 1131, 1139 | Stage exams not read | DONE-ALREADY | exam sources |
| 1138 | Printed quotient of restated values against the band | BUILD S | pass 8 A "Not built"; `validate.mjs` |
| 1142 | `[shown-arithmetic]` misses "x is $a \times b$" and a quotient in `\Phi\big(...\big)` | BUILD S | pass 8 A "Not built"; `validate.mjs` line 118 |
| 1144 | 0 hits on stat-models sets: ranks and statistics are not compared | UNSURE | exam part done; the rest names no rule to build |
| 1153 | Shared parameter, problem against exam item ("x over n years") | BUILD S | `engine-pass-8.md` part C: "gone until 1153 is built" |

## 3. Open [Could] (70)

DONE-ALREADY, status only (4): 1091 (`fresh-check.mjs --files`, line 353), 1096 (normal quantiles are stock, line 261), 1101 (`rate` skips a decimal on a variable), 1124 (corpus loaded once; 54 s to 34 s).

POST-COMPLETION (66):

| No | Gist |
|---|---|
| 930 | fresh-check: shared model parameter and answer kind |
| 941 | Fluency: thousands separator format |
| 942 | `form` for a product of primes |
| 943 | `fluency-sample --json` omits a `wrong` entry's `tol` |
| 946 | fresh-check: story reused with new numbers and words |
| 947 | Rules: `expanded` with no cue in the prompt; "Type the top" with no `whole` slip |
| 948 | Fluency: `pick` text var holding a placeholder |
| 949 | `[wrong-band]` on a whole-number part with a non-whole slip |
| 950 | `--shots`: feedback sheet covers options at 440 px |
| 952 | fresh-check does not read a longform `model` |
| 953 | Rule: k places, half-unit band, `\ln` or $X^2$ in the prompt |
| 954 | Census: lessons whose key term no exam holds |
| 955 | Built-in `decimal` key on a `%` part (falls out of 951) |
| 956 | Accepted line prints the band at full decimals |
| 957 | On-screen hint for typing a matrix |
| 958 | `grade-regression.mjs --file` |
| 959 | fresh-check lists standard constants as parameters |
| 960 | Advisory: one-letter unit named, no `unit` |
| 962 | Number scripts: slip from exact inputs where the input is rounded |
| 963 | fresh-check: task repeated with new numbers |
| 964 | Three band rule candidates (testing read) |
| 965 | fresh-check: two vectors reused under other names |
| 966 | Inline `pmatrix` at full height at 440 px |
| 967 | fresh-check: two-term linear equation as a shared formula |
| 1030 | Warn on a `byKey` line with neither the slip value nor a formula |
| 1033 | "Timed out" line must name a failing naive version |
| 1034 | graphs-dp has no number script (content) |
| 1035 | `tools/grade-cpp.mjs` |
| 1038 | algo-think homework-3 test 8 is weak (content) |
| 1039 to 1042 | AUTHORING notes: 64-bit sizes, shared test namespace, compiler flags on transcripts, `order` byKey choice |
| 1043 | `planted-check`: flip each comparison |
| 1044 | Read-count cap checked against the solution only |
| 1045 | Recursion depth check for lesson code screens |
| 1046 | Caption and prose disagree on canvas labels |
| 1047 | `console` `lN` keys unchecked against their line (the pass 7 "console line-number citations") |
| 1048 | `byKey` keys on the test number only |
| 1049 | Warn on `tol.abs >= 1` for a whole-number answer |
| 1050 | Drag-point region feedback cannot quote the dropped value |
| 1051 | More universal-wording phrases |
| 1060, 1073 | Over-100 warning fires on a `wrong[]` entry (one item, numbered twice; also 651) |
| 1061, 1074 | Shared-formula advisory misses an equivalent rewrite (one item, numbered twice) |
| 1070 | fresh-check: story miss across courses |
| 1071 | fresh-check: numbers miss (eigen) |
| 1072 | `reuse-shapes` `transform`: mirrored factor pair |
| 1077 | Hint when 100 times the typed value fits a `%` key (falls out of 951) |
| 1089 | Regenerate the AF hits report |
| 1093 | A reader's replacement raises `[key-length]` |
| 1094, 1095 | `--problems` on a stale manifest gives a bare error |
| 1099 | A chain held in one explain line |
| 1104 | One distinctive parameter on the same task |
| 1111 | Compare the problems of one set with each other |
| 1119 | Story held in a few rare nouns |
| 1120 | Parts that are each a different quiz item |
| 1129 | A hit rate no whole count of rows gives |
| 1132 | Slip line differing by one word and a tail clause (partly done) |
| 1133 | fresh-check reads no canvas table or number run |
| 1134 | `feedback.correct` prints the key at other places |
| 1135 | One key number, up to sign, in two problems of a set |
| 1136 | Glossary of taught terms |
| 1146 | Sentence frame that is mostly maths |

## 4. Items 340 to 422 (untagged, no status)

DONE-ALREADY (79). Evidence is a code comment naming the item unless stated.

| File | Items |
|---|---|
| `js/engine/canvas/plane.js` | 340 (line 854), 345 (1198), 346 (`state.ci`, 1290), 361 (884), 366 (README-B line 125), 372 (1371), 375 (1363), 388 (1388) |
| `js/engine/canvas/_base.js` | 341 and 380 (`qnorm`, `normcdf`, `erf`, line 107), 355 (642), 367 (`randn`, `ar1`, 565), 386 (`pair` `split`, 677), 389 (`obj()`, 554) |
| `js/engine/canvas/bars.js`, `js/engine/sim.js` | 342 (`maxn`, catch-all `"4+"`), 382 (`state.categories`) |
| `js/engine/canvas/distribution.js` | 344 (`beta`, line 63) |
| `js/engine/canvas/console.js` | 349 (`compact`, `fontSize`) |
| `js/engine/canvas/scatter.js` | 350, 358, 365 (header and line 82) |
| `js/engine/canvas/orderbook.js` | 352, 353, 370, 376, 421 (header line 4) |
| `js/engine/canvas/boxes.js` | 354, 392 (header) |
| `js/engine/canvas/tree.js` | 359, 396, 409, 417, 420 (header; `state.labels`, `values`, `dim`, `arrows`, `params.binary`) |
| `js/engine/canvas/graph.js` | 374 (`lattice`, line 20), 398 (ordered badges in `_base.js` 361), 399 (item 609), 406, 415, 416 (KaTeX edge labels, radius; side panel not built) |
| `js/engine/canvas/payoff.js` | 362 (`labelAt`), 363, 371, 379 |
| `js/engine/canvas/series.js` | 373 (line 197), 385 (229) |
| `js/engine/canvas/array.js` | 384, 387, 393, 397, 405 (header; the Why? copy of `state.active` in 387 is still unconfirmed) |
| `js/engine/canvas/grid.js` | 410 (line 129), 418 (255) |
| `js/engine/canvas/number-line.js` | 348, 413 (line 170; validator line 667) |
| `js/engine/widgets/table.js` | 356, 360 (`wrong`, header line 7), 390 (`compare: "bigO"`), 408 (as a table-widget `deps` highlight on the grid, line 72, not `params.edit`) |
| `js/engine/widgets/place.js` | 364 (`onPlace`, line 142) |
| `js/engine/widgets/code.js`, `cpp-grade.js` | 378 (`tol`), 394 and 419 (per-case limit), 395, 402 (`flags`), 403 (hidden `files` linked, "in part"), 369 (output before a timeout; C++ section at AUTHORING line 425) |
| `js/engine/widgets/manipulate.js` | 407 (`reject: true`) |
| `js/engine/widgets/tap-regions.js` | 411 (`ordered: true`; no widget for an `array` drag-reorder) |
| `js/engine/widgets/choice.js` | 391 (fenced block, line 15) |
| `js/engine/player.js` | 357 (`stops`, line 237), 404 (line 559) |
| `js/engine/grade.js` | 381 (Markdown tables, line 1127) |
| `css/screens/lesson.css` | 377 (line 320: `.has-maxh > .cv-table` scrolls) |
| `tools/validate.mjs` | 351 (line 701) |
| `tools/playthrough.mjs` | 400 (line 439: past the enter patch, then settled) |
| `docs/AUTHORING.md` | 343, 347 (README-B), 414, 368 (line 434: no unwinder, do not set `try`/`catch` exercises) |

| No | Gist | Mark | Reason |
|---|---|---|---|
| 383 | Calculus coverage against MIT 18.01 and 18.02 | DROP | content, not engine; `course.json` maps now hold improper integrals, partial fractions, trig substitution, arc length, related rates, revolution |
| 401 | Linear algebra coverage against MIT 18.06 | DROP | content; maps hold matrix exponential, similar matrices, pseudoinverse, Cholesky |
| 422 | No `build(values)` tree helper; remove the claim from briefs | DROP | no brief or AUTHORING line makes the claim now (grep of `docs/briefs`, `docs/AUTHORING.md`) |
| 412 | `tree`: stacked rows or a minimum font under `maxHeight` | UNSURE | no minimum-font or stacking code found in `tree.js`; labels "shrink a little" (line 209). Cosmetic: propose POST-COMPLETION |

Leftovers of done items, proposed POST-COMPLETION: 403 (learner-edited second source file), 411 (order after an `array` drag-reorder), 416 (side panel for a heap).

## 5. Deferred inbox list of `engine-pass-7.md` (untagged, never numbered)

| Bullet | Mark | Checked |
|---|---|---|
| `series` marker tap snapping | POST-COMPLETION (proposed) | no `snap` in `canvas/series.js` |
| `number-line` six-label collisions | UNSURE | `number-line.js` stacks overlapping labels in tiers (lines 4, 92); the six-label case was not run |
| `drag-point` pixel tolerance warning | POST-COMPLETION (proposed) | no such warning in `validate.mjs` case `drag-point` (line 869) |
| `[prelude-drift]` | POST-COMPLETION (proposed) | tag absent from `tools/` |
| `[canvas-above]` | POST-COMPLETION (proposed) | tag absent |
| Console line-number citations | POST-COMPLETION | same ask as 1047 [Could] |
| Lo standard-error advisory | POST-COMPLETION (proposed) | nothing in `validate.mjs` |
| Longform homework "this" advisory | POST-COMPLETION (proposed) | only the prose-plus-prompt warning exists (line 1639) |
| Playthrough check for off-screen answer cells | POST-COMPLETION (proposed) | `playthrough.mjs` checks width and marked-shot height only (701, 703) |
| Backtest fill-cap | DROP | a content item by the report's own words |

"Proposed" because no bullet ever carried a tag and the text is gone; if the coordinator holds a bullet that was [Must] or [Should], it becomes BUILD S in package 2 (validator rules) or package 1 (playthrough).

## 6. E items

| Item | Gist | Mark |
|---|---|---|
| E13 | Concurrency canvas | DONE-ALREADY (backlog 471, `canvas/interleave.js`, `css/interleave.css`); nothing left to build |
| E15 | Calculator panel on a paper | POST-COMPLETION |
| E16 | Application tracker on You | POST-COMPLETION |
| E17 | Role filter | POST-COMPLETION |
| E18 | Readiness view | POST-COMPLETION |
| E19 | `asOf` and `sources` freshness fields | POST-COMPLETION |

## 7. Not in the 87 lines: [Must]/[Should] with no "Done" and no status line (46, all [Should])

One grep each, not a triage. "nf" means the probe found nothing in the named file.

| No | Gist | Probe |
|---|---|---|
| 623 | Warn on protocol-dependent puzzles (Monty Hall) | nf `validate.mjs` |
| 624 | List levels with a report and no number script | part: `validate.mjs` line 2387 (573) checks a script that exists |
| 628 | Check cross-course lesson references in prose | nf |
| 630 | LEVEL-BRIEF: scratchpad per branch | nf `docs/LEVEL-BRIEF.md` |
| 635 | `research-int/review-1` timed checks time out | open in KNOWN_ISSUES line 244 |
| 643 | `[shuffled-position]` refinements | UNSURE (601 may cover) |
| 645 | `[float-artefact]` opt-out | nf |
| 646 | Playthrough `"verify": "stdout"` | nf |
| 651 | `unit "%"` above-1 rule on `answer` only | not done (`validate.mjs` line 810; see 1060) |
| 652 | `[float-example]` skips a rounding `call` | UNSURE (line 1112) |
| 659 | Rerun SQL solutions with reversed rows | nf |
| 660 | `numeric` `"places": n` | nf `numeric.js` |
| 667 | `drag-point` `wrong[]` regions and on-target points | nf |
| 668 | Error on `=` in an expression answer | nf (618 to 620 may overtake) |
| 676 | Built-in key for a correct decimal of an exact answer | nf `grade.js` |
| 677 | Copy button on shell blocks | nf |
| 681 | `byKey.error` (same as 1036) | not done |
| 687 | fresh-check setup signature | nf |
| 692 | `formOk` judges the right-hand side after a label | nf by number; UNSURE |
| 693 | Label strip counts a composite | nf by number; UNSURE |
| 696 | Exam item needs only taught constructs | nf |
| 697 | Longform: "prose or prompt" rule | nf |
| 705 | Homework wording on an `aloud` item | UNSURE (`longform.js` line 39) |
| 707 | `aloud` `reveal` list | nf (`reveal()` there is the mark step) |
| 709 | Width check on inline `.katex` (with 1063, 987) | nf |
| 710 | Rubric row cut at 440 px | UNSURE (`css/widgets.css` line 216 has `min-width: 0`) |
| 716 | `data` path inside the course folder | nf |
| 717 | Headings in `grade.prose` | nf |
| 737 | Render a returned Figure in the code widget | nf |
| 879 | `form: "standard"` | nf |
| 880 | `form: "ratio"` | nf |
| 883 | Whole matrix as a typed Fluency answer | UNSURE (931 reads the typing forms) |
| 888 | `rectangular` accepts a number times a surd times $i$ | UNSURE (`grade.js` line 739) |
| 890 | `--problems --shots` shoots the Problem set row | UNSURE |
| 899 | `trade` one-sided quote | nf `trade.js` |
| 974 | Python test limit under 5 s | UNSURE (394 gives a per-case limit; `budget` only adds) |
| 976 | `compare: "fraction"` evaluated in the learner's namespace | likely done (`code.js` line 211 imports `Fraction as _F`) |
| 979 | Rule for "In 2,000 seeded fits" | nf |
| 980 | `fresh-check --bank` near copies | UNSURE (970, 929 cover part) |
| 983 | `numText` unit forms (bp, per cent, 55p) | UNSURE (`unitCanon`, line 959) |
| 987 | `--problems --mobile` and a wide display in prose | with 1063 |
| 990 | A number in front of a vector | likely done (`scaledLiteral`, item 932) |
| 1006 | `numbers_lib` `require_coverage()` | nf |
| 1008 | `grade-all --file` runs no code widget | not done (same as 1031) |
| 1010 | `numbers_lib` code runner ignores `setup`, `prelude` | nf |
| 1024 | "One fraction" parts accept the retyped question | UNSURE (945 family) |

## 8. Work packages (19 BUILD items, disjoint files)

| Package | Files owned | Items | Size |
|---|---|---|---|
| 1. Grader, code widgets and code tooling | `js/engine/grade.js`, `js/engine/widgets/numeric.js`, `widgets/code.js`, `widgets/cpp-grade.js`, `js/screens/drill-worker.js`, `tools/grade-all.mjs`, `tools/planted-check.mjs`, `tools/playthrough.mjs`, `tools/test-grade-ab3.mjs`, `tools/test-grade-all.mjs` | 944, 945, 951, 1036, 1037, 1028, 1031, 1032 (8), plus 1063 if confirmed | 3 S, 4 M, 1 L, order 1031 then 1032 then 1028 |
| 2. Validator rules and number scripts | `tools/validate.mjs`, `tools/numbers_lib.py`, `tools/test-validate-pass8.mjs`, `tools/test-validate-shown-arithmetic.mjs`, `tools/test-numbers-lib.py` | 1029, 1079, 1081, 1130, 1138, 1142 (6) | 4 S, 2 M |
| 3. Reuse checkers | `tools/same-course-reuse.mjs`, `tools/retold-reuse.mjs`, `tools/reuse-shapes.mjs`, `tools/fresh-check.mjs`, `tools/same-course-waivers.json`, `tools/test-fresh-check-pass8.mjs` | 1062, 1088 (ratio), 1106, 1128, 1153 (5) | 3 S, 2 M |

Shared files: `docs/AUTHORING.md` and `.github/workflows/acceptance.yml` (a new test file needs a CI line). Give each package its own AUTHORING paragraph and let one agent, or the coordinator, add the CI lines. `docs/ENGINE-BACKLOG.md` status lines: one writer, after the numbering agent finishes.

Seams: 1028 (`mutants`) and 1037 need the validator to accept a new widget field only if `validate.mjs` rejects unknown fields on `code`; package 1 should ask package 2 for that line, not edit the file. New validator warnings in package 2 will raise hits in content: report counts, change no content.

Gallery: no package touches a canvas, a canvas README or CSS. Package 1 changes the logic of the `numeric` and `code` widgets (no markup or style change intended). The gallery check in both themes stays a task 6 acceptance step, not a consequence of these packages.

## 9. PLAN.md lines that would close

| Line | Text | Closes when |
|---|---|---|
| 305 (section 6) | "Engine pass 7 ... the rest of 340 to 422 and the deferred list" | 340 to 422 are built now (section 4); the line closes once the status lines are written, the three packages land and the coordinator rules on section 5 (untagged bullets) and section 7 |
| 192 (2a) | "Engine: E13 concurrency canvas ...; [Could] items E15 to E19" | now: E13 is built (471) and E15 to E19 move to the post-completion list |
| 17 (Route to DONE, AH) | "engine pass 7 remainder ([Must] and [Should] only ...)" | with line 305; its acceptance and gallery clauses belong to line 309 |

Not closed by this: line 309 (full acceptance, gallery in both themes).

## 10. The 46 extras, 412 and number-line labels (second triage)

Read at 9827e437. Marks: DONE-ALREADY, BUILD-CORRECTNESS (a learner is marked wrong when right, right when wrong, shown a wrong number, or blocked), POST-COMPLETION, DROP. Unlike the first triage, the grader items were run: `grade.js` was loaded with the local Compute Engine (as `tools/test-answer-forms.mjs` does) and the typings below were graded; two Python scans read all 2,529 content files. "Probe" names such a run. Nothing was built and no engine or content file was edited.

| Set | Items | DONE-ALREADY | BUILD-CORRECTNESS | POST-COMPLETION | DROP |
|---|---|---|---|---|---|
| The 46 of section 7 | 46 | 8 | 3 | 32 | 3 |
| 412 | 1 | 0 | 0 | 1 | 0 |
| Number-line labels (section 5) | 1 | 0 | 0 | 1 | 0 |
| Total | 48 | 8 | 3 | 34 | 3 |

### BUILD-CORRECTNESS (3)

| No | What goes wrong for a learner | Evidence | Files | Size |
|---|---|---|---|---|
| 888 | Wrong when right. Under `form: "rectangular"` a correct $a + bi$ whose imaginary part is a number times a surd is refused with the key `form`. | Probe on the real key of `complex/problems-1` `items[2].parts[3]` ($\frac{3}{2}-\frac{3\sqrt{3}}{2}i$): `\frac{3}{2}-\frac{3}{2}\sqrt{3}i`, `\frac{3}{2}-\frac{3\sqrt{3}i}{2}`, `\frac{3}{2}-\frac{3i\sqrt{3}}{2}` and `1.5-1.5\sqrt{3}i` all return `ok: false, key: "form"`. `9\sqrt{3}i` is refused even as its own key. Cause: `imagTerm` (`js/engine/grade.js` line 735) accepts a product of exactly two factors. 21 items carry the form, 5 with a surd key; no stored key is refused today, so only the learner's other spellings fail. | `js/engine/grade.js` (`imagTerm`), `tools/test-grade-ab3.mjs` | S |
| 976 | Wrong when right. A `compare: "fraction"` expect is evaluated in the learner's namespace, so a learner who writes `import fractions` (or `from fractions import Fraction as F`) and returns a correct `Fraction` fails every case with a `NameError`. | `js/engine/widgets/code.js` line 206: `eval(_exp, _ns)`; `_F` is imported only inside `__zq_judge` (line 211). Read, not run in Pyodide. Scan: 42 code widgets use the compare, 17 have no `Fraction` in a prelude or setup (markov l17, l18, l20, l21 and homework-5, measure-prob l1 and l3, bank `coding-1` `items[5]` and others). The drill worker is safe (`drill-worker.js` line 30). | `js/engine/widgets/code.js` (`__zq_cmp`, both harnesses), `tools/test-engine-runtime.mjs` | S |
| 1024 | Right when wrong. A part that asks for "one fraction" grades the retyped question correct. | Probe: `\frac{2}{x+1}+\frac{3}{x+2}` against the key `\frac{5x+7}{(x+1)(x+2)}` returns `ok: true` with no form and with `form: "simplified"`. Live in `analysis/problems-1` `items[1].parts[1]` (the question shows $5 - \tfrac{5n-4}{n+1}$, the key is $\frac{9}{n+1}$, no `form`). Scan: 11 expression parts ask for one or a single fraction and 8 carry no `form`; in most the retyped question is not available (a derivative, an unnamed $a_n$). | Same function as 945 (BUILD M, package 1): `js/engine/grade.js` (`simplestVerdict` refuses a sum of fractions), `tools/test-grade-ab3.mjs`; then `"form": "simplified"` on `analysis/problems-1.json` and `problems-2.json` (content, two lines) | S on top of 945 |

All three sit in package 1 of section 8 (`grade.js`, `widgets/code.js` and their tests), so they add no new file owner.

### DONE-ALREADY (8)

| No | Gist | Evidence |
|---|---|---|
| 630 | Scratchpad folder per agent | `docs/LEVEL-BRIEF.md` line 40: "your own subfolder of the scratchpad named `<course>-<level>` ... never touch another folder" |
| 635 | `research-int/review-1` timed checks time out | `docs/reports/engine-pass-ac-4.md` section 4: a harness fault, fixed (`timedChecks` calls `unlockRoute` first); "passes all three lines". `KNOWN_ISSUES.md` line 244 is stale |
| 687 | fresh-check setup signature | Built as 970 (`--cross-numbers`), 972 and 993 (numbers, matrices, shapes; `tools/same-course-reuse.mjs`, `tools/fresh-check.mjs` header lines 4 to 7), 1075 to 1080 (retold screens). Leftover (test `call` strings, ids): post-completion |
| 692 | `formOk` judges the right-hand side after a label | Item 904: `dropLabel` (`grade.js` line 748) runs before the shape check (line 845); `tools/test-answer-forms.mjs` line 112 (`y=2.5t-2` passes `simplified`) |
| 693 | Label strip counts a composite | Item 904: `CALLLABEL` (`grade.js` line 511) reads `m(e(x))`, `gf(x)`, `f^{-1}(x)` |
| 883 | Whole matrix as a typed answer | Item 931 (Done, [Must]): `[[a, b], [c, d]]`, `((a, b), (c, d))` and MathLive spellings; `tools/test-grade-ab3.mjs` part 1; `docs/AUTHORING.md` line 194 |
| 983 | `numText` unit forms | Probe: "10 basis points", "10 per cent", "10 percent", "55p", "4h" and "20 degrees" all grade right (`unitCanon`, `grade.js` line 959). Unread still: "£1.732m" and "20°C" on a "degrees" field; the field then stays unready (`numeric.js` line 55), so no mark is lost. Leftover: post-completion |
| 990 | A number in front of a vector | Item 932: probe `5(0.8,0.6,0)` against `(4,3,0)` is right. `16(3,1)+(2,1)` still returns the key `length`: an unfinished sum, refused. Leftover: post-completion |

### DROP (3)

| No | Gist | Reason |
|---|---|---|
| 668 | Error on `=` in an expression answer | Overtaken by 618: an equation is graded as a relation. Probe: the key `y=2x+1` refuses `x=1` and `3=3`; `tools/test-expr-equations.mjs` |
| 681 | `byKey.error` | Same ask as 1036 (BUILD S, package 1); build once under 1036 |
| 1008 | `grade-all --file` runs no code widget | Same ask as 1031 (BUILD M, package 1) |

### POST-COMPLETION (34)

| No | Gist | Checked | Why not correctness |
|---|---|---|---|
| 412 | `tree` minimum font or stacked rows | `canvas/tree.js` line 209: labels scale to 0.82 at least | cosmetic |
| Number line | Six labelled points collide at 440 px | Original bullet (da756dd9, removed at fc24bf10) was tagged [Could]; `number-line.js` line 92 already stacks overlapping labels in tiers. The six-label screen was not rendered | cosmetic, [Could] |
| 623 | Warn on protocol-dependent puzzles | not in `validate.mjs` | validator advisory |
| 624 | List levels with no number script | `validate.mjs` line 2387 checks only a script that exists | process check |
| 628 | Cross-course lesson references in prose | not built | validator advisory; the 15 known were checked by hand |
| 643 | `[shuffled-position]` refinements | `validate.mjs` lines 1488 to 1525 | lint precision |
| 645 | `[float-artefact]` opt-out | line 126, no opt-out | false alarms only |
| 646 | Playthrough `"verify": "stdout"` | not built | audit tool. One run would check every "What does it print?" key, so it is the nearest of these to correctness |
| 651 | `unit "%"` above-1 rule on `answer` only | line 807 exempts a `wrong` value at or below 1 only | false alarms; same ask as 1060 [Could] |
| 652 | `[float-example]` skips a rounding `call` | line 1112, no skip | false alarms |
| 659 | Rerun SQL solutions with reversed rows | not built | audit tool; second nearest to correctness |
| 660 | `numeric` `"places": n` | probe: `4` is right for 4.0 | marking style, the value is right |
| 667 | `drag-point` `wrong[]` regions and on-target points | `drag-point.js` line 86: all regions tested against all points | the mark is unaffected (a fully right answer returns before the loop); only the slip line can be the wrong one. S if wanted |
| 676 | Built-in key for a decimal of an exact answer | probe: `1.414` for $\sqrt{2}$ is wrong with no key | the mark is right; feedback wording |
| 677 | Copy button strips shell prompts | `grade.js` line 1164 copies the whole block | convenience |
| 696 | Exam item needs only taught constructs | not built | audit tool |
| 697 | Longform "prose or prompt" rule | `validate.mjs` line 1639 warns on both | rule wording; with 718 |
| 705 | Homework wording on an `aloud` item | `longform.js` line 47 with `review.js` line 1030 (homework runs in mode `exam`): "The paper clock ends the sitting" | wording |
| 707 | `aloud` `reveal` list | not built | new feature |
| 709 | Width check on inline `.katex` | `playthrough.mjs` line 445 measures `.katex-display` only | tooling; decide with 1063 |
| 710 | Rubric row cut at 440 px | `css/widgets.css` lines 222 and 223: the text column has no `min-width: 0` | cosmetic; the row still ticks |
| 716 | `data` path inside the course folder | `validate.mjs` line 480 | authoring rule |
| 717 | Headings in `grade.prose` | scan: two models show a `# ` line literally (`backtest/homework-4` and `alpha/homework-4`, `items[7]`) | cosmetic; a two-line content edit also closes it |
| 737 | Render a returned Figure | not in `widgets/code.js` | convenience; the tests grade the chart |
| 879 | `form: "standard"` | not built; scan finds no item that asks for it | new form |
| 880 | `form: "ratio"` | not built | new form |
| 890 | `--problems --shots` shoots the Problem set row | not built | tooling |
| 899 | `trade` one-sided quote | not in `widgets/trade.js` | new feature |
| 974 | Python test limit under 5 s | `code.js` line 493: `budget` only adds | authoring aid |
| 979 | Rule for "In 2,000 seeded fits" | not built | validator advisory |
| 980 | `fresh-check --bank` near copies | 970 covers shared numbers in another order | tooling |
| 987 | `--problems --mobile` and a wide display in prose | line 1164 checks page width only | tooling; decide with 1063 |
| 1006 | `numbers_lib` `require_coverage()` | not built | tooling |
| 1010 | `numbers_lib` code runner ignores `setup`, `prelude` | not built | tooling; 1031 would replace it |

Notes for the coordinator:
1. The section 5 bullets are not lost: `git show fc24bf10^:docs/BACKLOG-INBOX.md` holds their text and tags. The number-line bullet reads "[Could] `number-line` with six labelled points ... (coint l4 `screens[5]`)".
2. 709 and 987 stand or fall with 1063 (UNSURE in section 2). An over-wide formula shifts the page; it blocks nobody, so by the strict test all three are post-completion.
3. `KNOWN_ISSUES.md` line 244 (635) can be struck.
