# Report: trees level 4, "Options at interview"

Author: content agent, 5 Nov. Brief: `## Level 4` of `docs/briefs/trees.md` (second-read and fixed, `docs/reviews/review-brief-trees-4.md`). Nothing outside `app/content/courses/trees/` was edited except the report, `docs/BACKLOG-INBOX.md` and one new script, `docs/briefs/trees-scripts/check_l4_authoring.py`. `course.json`, other levels, exams and engine files are untouched. `tools/validate.mjs` rewrote `app/content/manifest.json`, which I left uncommitted.

## Files written

| File | Screens | Quiz | Notes |
|---|---|---|---|
| `l13-rules-of-thumb.json` | 10 | 4 (`option-estimate`, pace 60 to 90) | explore, problem, 4 ladders, derive, trap, transfer, code |
| `l14-greeks-by-shape.json` | 10 | 4 (`greek-signs`, pace 60) | sketch, drag-point, explore with frames, 3 ladders, sign table, trap, transfer, code |
| `l15-digitals.json` | 10 | 4 (`digital-option`, pace 60 to 75) | explore, table problem, 4 ladders, derive, trap, transfer, code |
| `l16-the-smile.json` | 10 | 4 (`vol-smile`, pace 60 to 75) | 2 problems, explore on the implied density, 3 ladders (one on `distribution`), trap, derive, transfer, code |
| `l17-which-is-cheaper.json` | 10 | 4 (`exotic-ranking`, pace 60) | series canvas throughout; code uses NumPy with `budget` 20,000 |
| `l18-gamma-and-hedging.json` | 10 | 4 (`gamma-pnl`, pace 60 to 75) | two seeded years as frames; code prelude holds both years as 253-price literals |
| `review-4.json` | 9 items (difficulty 2, 3, 3, 3, 3, 2, 3, 4, 4), `timed` 900 s without lock | | items 8 and 9 are 3-part items |
| `homework-4.json` | 8 items (difficulty 4, 5, 4, 4, 4, 3, 5, 4), `dueDays` 7 | | 2 code, 2 order, 1 multi, 1 longform (10 points), 3 parts items |

Every lesson has one trap, one edge case, one follow-up screen pushing the question a step, and an interviewer-voiced transfer with a line to say aloud. Every quiz, review and homework item has `tags` (family first) and `pace`. Hull's and Joshi's books are named once, on the l14 code screen. Φ is used throughout and l15 says once that interviewers write N.

## Validator

`node tools/validate.mjs`: 0 errors. Two level-4 warnings, both "a ladder screen usually reuses the previous canvas kind" (l16 screen 8 changes to a `distribution`, l18 screen 6 to a `plane` after `bars`), both deliberate.

## Playthrough (local CDN, `pkgs` folder named in the task)

| Run | Result |
|---|---|
| 6 lessons, desktop and `--mobile` (440 x 956) | all passed, 14 checks each, quiz 4/4, 27 to 30 s each |
| 6 lessons, desktop and `--tablet` (1032 x 1376 and 1376 x 1032) | all passed, 14 checks each, quiz 4/4, 35 to 40 s each |
| `--set trees/review-4`, desktop, `--mobile`, `--tablet` | passed, 9 of 9 recorded |
| `--set trees/homework-4`, desktop, `--mobile`, `--tablet` | passed, 8 of 8 right, 38 of 38 marks, parts checks passed |

l17 was re-run alone with `--mobile --tablet` after the canvas height cap, and passed. No "Target crashed" occurred.

Screenshots looked at (440, 1032, 1376): l14 screens 1, 2, 3, 6 and 8 (sketch, drag-point, the frames explore, the transposed sign table, the expiry-day curves), l13 screens 1, 3, 6, 8, l15 screens 1, 2, 8, l16 screens 1, 2, 8, 9, l17 screens 1, 4, 5, l18 screens 1, 7, 8, and the review and homework table and order items. Faults found and fixed: a five-column sign table clipped at 440 (now transposed to four columns), an axis title colliding with a caption on the density canvases (captions removed), a long table below a tall series canvas in landscape (l17 `maxHeight` 250), grey versus dashed wording.

Code screens: each `solution` passes every hidden test in Pyodide (the playthrough plays Show solution) and, by my own CPython runner (`run_code_widget` in the scratchpad `trees-4/lib.py`), every starter fails every test (0 of n) while every solution passes (l13 8, l14 7, l15 10, l16 10, l17 9, l18 8, h-rule-rate 7, h-hedge-sim 8).

## Numbers and their sources

Every number is computed twice. The brief's numbers are in `docs/briefs/trees-scripts/check_l4.py` (PASS, 207 checks). Every number I added (rule errors, out-of-the-money prices, ratios, gamma peaks by expiry, the vega and theta identities, theta bleed, digital spread limits, pin deltas, the risk-neutral and skew chances at 110, the up-and-out vanilla key, the one-day gamma and theta, the hedged paths N and F, the review and homework figures) is in the new `docs/briefs/trees-scripts/check_l4_authoring.py`: **PASS, 137 checks**, method A the closed form with `math.erf`, method B numerical integration of the payoff (`scipy.integrate.quad`) or finite differences of those integrals, or `ndtr` against `erf` for the hedged paths.

Simulations and their standard errors:

- l17 `asian_vs_vanilla` (seed 17, n = 52, 20,000 paths, layout `(paths, n)`, log steps with the drift term): 8.0176 and 4.6868 in CPython and the Pyodide solution; se 0.093 and 0.053; formulas 7.9656 and 4.6779. Tests: vanilla within 0.37 (four se) of 7.9656, Asian within 0.21 (four se) of 4.6779, ratio within 0.03 of 0.58, and 12 fixings (seed 5) within 0.21 of 4.8977.
- homework item 2 `hedged_vol_report` (6,000 paths, layout `(paths, 252)`): seed 18 gives mean 2.3700, se 0.0154 for realised 26% and mean −0.7927, se 0.0063 at 18%, against gaps 2.3778 and −0.7943. Tests check the gap to 4 places at 2,000 paths, `se` within 15% of 0.0154, the mean within four se of the gap at (0.2, 0.26), (0.2, 0.18), and zero at (0.2, 0.2), and `within` is a plain `bool`.
- l18 seeded years (`default_rng(18)` with generating vol 26%, `default_rng(21)` with 14%, daily log steps, 253 prices rounded to 6 places in the prelude): exact hedged P&L +2.0682 and −2.4305, gamma sums +2.0795 and −2.4412, a flat path −7.9656 exact and −7.6064 by the gamma sum. The same figures come from the literal lists in two implementations (loop with `erf`, vector with `ndtr`).
- l18 screen 8 paths are deterministic zig-zags, not simulations: N alternates +r and −r every day, F runs up for 22 days then alternates, with r = σ√dt, so both have realised vol exactly 26% by the root-mean-square of daily log returns. Exact hedged P&L at 26%: N +4.82, F +0.38; at 14%: N −4.21, F −1.06 (two implementations agree to 1e-9).

## Decisions and small departures from the brief

- l14 screen 3: the brief's numeric ratio (6.6 tol 0.2) cannot be read off a plane by eye, so the dashed K = 130 curve carries a labelled point at spot £100 that follows the curve as the frames slide (three decimals), and the learner reads two values and divides.
- l14 screen 6: the sign grid is transposed (Greek by row, one column per position) so it fits at 440. The zero cell answer is the text `zero` with `accept` `["0", "~0", "flat", "0.0"]` because a text "0" is read as a number (inbox bullet).
- l16 screen 5 (trap): the prose quotes the colleague's flat-26% chance (10.72%) so the wrong key is something a learner can be tempted by; the honest 0.0813 comes from the put spread of screen 3. l16 `skew_vol` uses 100 as the reference strike (stated in the docstring).
- l17 screen 8 asks for a numeric 0 with `tol` 0 (the brief said "choice ... numeric 0 tol 0"); the wrong key is the vanilla's £3.59.
- Review item 8 key `no-half` 522 is the net when the half is dropped from both the gamma gain and the theta identity (2 × 261.18); the brief gave the figure without the slip.
- Homework item 2: `norm_cdf` in the prelude is a table built on `math.erf` (3,201 points) read with `np.interp`, accurate to about 1e-7, because `np.vectorize(math.erf)` is too slow for 1.5 million evaluations per test. The result is unchanged to four places against the `erf` route.
- Homework item 8 and review item 8 use "S = K = £50 or £320" exactly as the brief; the l18 quiz item 3 (1,000 options at 24% against 20%, answer 1,588 against an exact 1,586) is mine.

## Proposed `course.json` change

Add `opt-dash/L3` to the `requires` of trees level 4 (so `["trees/L3", "markov/L3", "opt-dash/L3"]`), as l16 and l18 build on `opt-dash` l10 and l14. Both lessons restate the idea in one line and do not rely on it, so nothing breaks without the change.

## Inbox

Five bullets under "trees L4 (5 Nov)" in `docs/BACKLOG-INBOX.md`: zero-valued text cells in `table`, a five-column grid clipping at 440, the plane axis title meeting a caption, no light vector normal cdf for Pyodide homework, and validator highlight ids for `distribution`, `bars` and sketch screens.
