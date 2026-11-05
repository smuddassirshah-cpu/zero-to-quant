# Engine pass O2: recurring finding classes as validator warnings

PLAN 2c item O2; source `docs/reviews/session-operating-model.md` 2.2. Backlog items 523 to 527.

## What changed
- `app/tools/o2-rules.mjs` (new): `scanO2(json, emit)` walks one content file. Kept apart from `validate.mjs` so the runner can call it on fixtures. The validator imports it, scans every JSON file under `content/` and files each hit as a warning tagged `[O2-...]`, then prints `O2 warnings: code n, ...` just above the error line.
- `app/tools/test-validate-o2.mjs` and `app/tools/fixtures/o2/<code>.json` (`{ bad, ok }` each): prints PASS or FAIL per code and `O2 rules: 6 passed, 0 failed`.
- `docs/AUTHORING.md` (validator section), `docs/ENGINE-BACKLOG.md` items 523 to 527.
- No `app/js` or `app/content` file touched. Validator: 0 errors; manifest unchanged.

## Counts on current content
Before: the rules were absent (0). Warnings overall went from 610 to 2094.

| Code | After | Top three files |
|---|---|---|
| O2-long-sentence | 677 | alpha/l14-turnover-and-costs 8; alpha/l9-information-coefficient 8; garch/l1-calm-and-storms 8 |
| O2-long-explain | 63 | arma/l3-unit-root 4; arma/l4-differencing 3; equations/homework-4 3 |
| O2-unshuffled-numeric | 73 | brainteasers/l5-ropes-and-jugs 2; markets/l2-present-value 2; multivar/l1-two-inputs 2 |
| O2-no-slip | 46 | algo-think/l8-cost-of-recursion 3; graphs-dp/l12-remembering 3; graphs-dp/l13-climbing-stairs 3 |
| O2-prose-prompt | 8 | one each in mental-pressure l14, l15, l5 (also trees l15 to l18) |
| O2-explain-answer | 617 | ito/l16-pricing-in-a-minute 6; integrals/l17-solids-of-revolution 5; research-int/l16-interpolating 5 |

To list one code: `node tools/validate.mjs | grep O2-no-slip`.

## Sampled precision (10 hits per rule, by eye, after tightening)
- long-sentence: 10 of 10 real (a few sit at exactly 20 words; maths spans are not counted).
- long-explain: 9 of 10 real (a bare formula line counts as a sentence).
- unshuffled-numeric: 9 of 10 real; the tenth is an ordered parameter menu (0.80, 0.90, 0.94) where order may help.
- no-slip: about 7 of 10. Most hits are `numeric` `wrong` entries with an id but no `byKey` note (the note is genuinely missing). A few choice hits describe a real slip in words that the detector cannot read.
- prose-prompt: 8 of 8 are the question repeated in the prose ("Put the lines in order."); true but cosmetic. No item has `prompt` beside prose beyond the existing longform check (item 297).
- explain-answer: about 7 of 10. Residual false positives: answers given in words ("nearly ten billion"), symbolic answers (`\sqrt{2}` is handled, other closed forms are not), and a rounded figure outside the 0.6 per cent band. Different-final-value is not detected, only absence of the key.

## Tightening done
Fractions in `\tfrac`, `\dfrac` and `\frac1{17}` forms, `\pi`, `\sqrt n`, sign-blind comparison for £ losses, key 0 skipped, vectors and "a and b" pairs no longer counted as intervals (only `to`, dashes, `[a, b]` or `between a and b`), ranges must be ordered by lower bound, explanations counted by `.?!` only (not colons), choice distractors with a note of 9 words or more are accepted.

## Notes
- Rule 4 mostly already existed (item 297, longform); O2-prose-prompt widens it.
- The repo has no voice-scan script (only per-review scratch scans), so the 20-word rule is implemented fresh; it splits on `.?!:;` and newlines after stripping maths and code.
- Choice `why` is already an error when absent, so O2-no-slip for choices only fires on unreachable values with a thin note.
