# Engine pass 7 (session V), items 604 to 615

Section "Session V engine pass 7" at the end of `docs/ENGINE-BACKLOG.md` holds each item and its status. 29 inbox bullets were moved out of `docs/BACKLOG-INBOX.md` (taken or already landed); the rest stay.

## Done
- 604 `fresh-check.mjs --file content/courses/<c>/<set>.json`: no ENOENT, no self-match, code items read from their own path, about 13 s. 614: advisory lines (exit 0) for three or more shared non-trivial numbers with a lesson screen of the same course.
- 605 validator `[shown-arithmetic]` (warning): recomputes `a op b = c` and `\approx c` inside a maths span. 197 hits in existing content (a miss over 2% is skipped as a deliberate wrong claim).
- 606 `numbers_lib`: hyphenated keys, `lv.claim`, `lv.claim_text`, `lv.stated`.
- 607 table fade cue (canvas and widget); 608 control label cap and stacking at 520 px; 609 `graph` rect and pill cap below 440 px.
- 610 `[wrong-band]` judged at the learner's rounding (122 to 86 hits); 611 signed zero in `[float-artefact]`, including `table` canvas cells.
- 612 compact start card for one-item mock papers; 613 `longform` `think` and `lockAtZero`, exam wording.
- 616 `order` `after` precedence rules (every valid proof order accepted); 2 runtime and 3 validator tests.
- 615 `O2-unshuffled-numeric` retired (it fired on correct `shuffle: false`; the coordinator's request). Regression case in `test-validate-o2.mjs`: the old bad fixture now raises nothing.
- Checked as already done: 343, 347, 348, 390, 395, 414, 415 (343 and 414 got a documentation sentence).

## Deferred
Inbox: `series` marker tap snapping, `number-line` six-label collisions, `drag-point` pixel tolerance warning, `[prelude-drift]`, `[canvas-above]`, console line-number citations, Lo standard-error advisory, longform homework "this" advisory, a playthrough viewport check for off-screen answer cells, backtest fill-cap (content item). Backlog 340 to 422: all others still open (`plane`, `orderbook`, `tree`, `payoff`, `array`, `boxes`, C++ items and so on).

## Tests added
`test-validate-shown-arithmetic.mjs` (new), `test-fresh-check.mjs` (+4), `test-numbers-lib.py` (+1), `test-validate-session-v-b.mjs` (+3), `test-engine-runtime.mjs` (+5: one-item start card, think and lock clock), `test-validate-o2.mjs` (+1).

## Content edits needed (not made)
Run the validator and read `[shown-arithmetic]` warnings (arma l3, l5, l8, l11, l12, review-1, homework-1; garch l2, l3, l7; trig l12; exp-log; functions homework-3; opt-dash and coint ones as listed). Authors of mocks with recorded prompts may now use `think` and `lockAtZero` (mock-video). Alpha l16 and backtest l4 and l8 need no change for 607 and 609 but tables with answer columns past column 4 still rely on scrolling.

## Verification
See the handback and `results.txt` in the scratch folder `engine-v-7`: validator, every `test-*`, four shards, routes desktop and mobile.
