# Engine pass V-B: validator and tools (items 600 to 603)

Agent B, session V. Files touched: `app/tools/fresh-check.mjs`, `app/tools/validate.mjs`, `app/tools/o2-rules.mjs` (one exported helper, no behaviour change), `app/tools/merge-wave.sh`, new `app/tools/union-table-rows.mjs`, tests, `docs/AUTHORING.md` (section 5 "Exam freshness" and section 7 validator rules only), `docs/ENGINE-BACKLOG.md` (pass B section). No `app/js`, `app/css`, `playthrough.mjs` or content edits.

## Results

- `node tools/validate.mjs`: 0 errors, 4,277 warnings (was 3,978 before this pass: +299).
- Every `app/tools/test-*.mjs` passes, plus the new `test-validate-session-v-b.mjs` (26 cases), `test-fresh-check.mjs` (11 cases, 4 new) and `test-merge-wave.sh` (PASS merge-wave).
- `node tools/fresh-check.mjs --all-exams`: 25 hits in 56 exam files (see below). The six session U topic exams give 0.

## Item 600: fresh-check

- Word tokens only. A maths span, a LaTeX command and a number each become one `#` placeholder; a run counts only its words, and `share` is run words over the item's words.
- Stop list (`STOPLIST` in the tool): "Put the lines/steps/proof/derivation/argument in order", "Leave out the (two) line(s)/step(s) that do(es) not belong", "Move the flawed line(s) to Left out", "one/two line(s) is/are flawed", "Each line carries its reason", "Give a reason for every line", "Select all that apply", "Give N decimal places", "a fraction or a decimal", "Say the reasoning aloud first", "Complete/Fill in the ... functions/answers/table", "Which statement is true/right?", "What does it print/return?". Each becomes a break that no run crosses.
- Code names: `def` and `class` names (Python), class/struct and function definitions (C++), `fn` of a drill and the head of each test `call`, from starter and solution, for every code widget of an exam, drill or bank item, against every code widget of every lesson, review and homework. Ignored: names under six characters without an underscore, `_x`, `test_x`, a generic list, and a name used in three or more courses (`--idiom n`). `--no-code` switches it off. One line per target widget and name, with "(+N more)" for further sources.
- Mock versions (`versionOf`) are not compared with each other (they were 140 of the 164 raw hits).
- Gate: `--min-run 12 --min-share 0.6`, Jaccard 0.5 (the 588 default). Calibration on the six session U exams (0.6, 1.10, 1.11, 2.5, 2.6, 3.4): at the old settings (`--min-run 8 --min-share 0`) 5, 6, 3, 4, 10 and 8 hits, all definitions or stock questions, none a copied setup; at `--min-run 12` alone 2.6 still shows two (shares 0.42 and 0.41) and 3.4 one (a field definition, share 0.50); at share 0.6 all six are clean. The stage-2 reuse is caught by the code-name check (test fixture with `walk_forward_mse`; `irls_logistic` and `metropolis` pass the same name filter).
- Documented in AUTHORING section 5 "Exam freshness".

### `--all-exams` hits for a content pass (not fixed here)

Prose (8): `topic-1.2` item 9 (SQL join, run 24, share 0.86, `sql/l10`); `topic-3.3` item 5 (balance weighings, `bank/brainteasers-3`); `mock-oa-sig`, `-2`, `-3` item 3 (expected count of HHH, `puzzles/l4` quiz 0, run 18); `mock-sample-parts` (deliberate sample copies of py-found sample homework and review).
Code names (17): `mock-sample-data` (`best_day`, `allocate`, `release`, `in_use`, `alloc_count`, `Buffer`: the sample is meant to copy cpp and systems helpers); `mock-superday-developer` part 2 item 5 (`release`, `in_use`, `alloc_count`); `stage-1` (`worst_drawdown`, `crr_price`); `topic-1.1` items 18 and 20 (`month_end_closes`, `rebased_chart`); `topic-1.9` item 27 (`Straddle`); `topic-2.2` item 18 (`garch_variance`, `neg_loglik`). Several are an exam item that tests the same function as the topic's own lesson, which may be intended; a reader decides.

## Item 601: validator refinements (warning counts)

| Rule | Before | After |
| --- | --- | --- |
| `[table-slip-key]` (584 refined) | 3 | 0 (odes l1 s10, odes l12 s1, topic-2.3 item 15 carry a generic cell line beside wrong-id lines) |
| `[shuffled-position]` (585, now every choice without `shuffle: false`, with exclusions) | 8 | 8 (see below) |
| `[float-example]` | 0 | 42 |
| `[wrong-band]` | 0 | 122 |
| `[float-artefact]` | 0 | 88 |
| `[math-thousands-comma]` | 0 | 7 |

`[shuffled-position]`: of the earlier eight false positives, five are now excluded (recruiting l8 and l9 table labels, py-found l9, git l3, convex l4, coding-int homework-4 part). The eight now are seven real hits that were hidden while the rule needed `shuffle: true` (numpy-pandas l8 quiz 2, integrals l16 s5, multivar l18 s7 twice, trees review-2 item 7, validation l8 s7, alpha l16 s5) and one false positive (`puzzles/homework-5` item 4, "last answer" of an earlier puzzle; needs `noPosCheck: true` in content). algo-think l6 s4 (code stack) is excluded by the code-block rule.

`[wrong-band]` is the loudest; it fires only when the wrong value has more decimals than the asked rounding and its band is under half a rounding step. Some of the 122 are deliberate "unrounded" slips; a reader decides. `[float-artefact]` includes deliberate floating-point teaching in py-found l1 (put the number in backticks to silence it).

Rules: thousands comma house form is `10{,}000` (1,352 uses in content against 78 plain commas outside maths); a list with comma and space and a bracketed pair such as `(1,000)` are not flagged.

## Item 602: schema

- `shuffle` is now boolean-checked (error otherwise). `[shuffle-false]`: 43 warnings on `shuffle: false` with plain-text options.
- `required` (exam paper items): error if not boolean. `tracks` (mock paper): error on an unknown role; accepted ids are the `prep.json` tracks (`trader`, `research`, `strats`, `developer`) plus the roles in `capstones.json` (`researcher`, `strats-deriv`).
- `form` on `expression`: the validator already accepted `expanded`, `factorised` and `simplified` (about nine items use them, so "rectangular or simplified only" would have broken content); `rectangular` is added and any other value stays an error.
- Not done (not in the item list): the inbox's warning for a symbol-free `expression` answer with no `form`.
- Follow-up for the orchestrator: once pass A's default shuffle lands, `O2-unshuffled-numeric` (73 warnings, "without shuffle: true: the key sits at a fixed place") is obsolete and should be retired in `o2-rules.mjs` and its fixture.

## Item 603: merge-wave

- `docs/briefs/*.md`: keep both sides.
- `docs/readiness.md`: keep both sides (`git merge-file --union`), then `union-table-rows.mjs` reduces each repeated row key (per heading) to one row, ours when ours changed it from the base, otherwise theirs. Tested with six adjacent-row conflicts (one in each role table).
- After the validator: `node tools/readiness-sums.mjs --write` from `app/`; `content/readiness.json` and `docs/readiness.md` are staged before the commit; the tail prints `readiness: OK`, `readiness: regenerated` or `readiness: FAIL (...)` (which also fails the run).
- `test-merge-wave.sh` was extended (briefs, readiness rows, a stale `readiness.json` that must be regenerated). It now builds a scratch repository from a snapshot of the working tree, because `git clone` of a shallow checkout fails ("unrelated histories").

## Content fixes needed (none done here)

1. The seven real `[shuffled-position]` hits above, and `noPosCheck: true` on `puzzles/homework-5` item 4.
2. The `--all-exams` hits above (SQL join in topic-1.2, balance puzzle in topic-3.3, HHH count in the three `mock-oa-sig` papers, and the code-name reuses).
3. Optional advisory passes by a reader, not a bulk edit: the 42 `[float-example]` examples (add `"compare": "isclose"`), the 122 `[wrong-band]` lines, the 43 `[shuffle-false]` fields, the 7 thousands commas, the 88 float artefacts that are not deliberate teaching.
