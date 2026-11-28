# ai-basics level 2 (Learning by nudging): report

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l5-how-wrong.json` | 9 screens (explore scatter with $w$, $b$ sliders, problem table widget, ladder, trap, problem table widget, 2 ladder, generalise, transfer), 13 min, skills `ab-nudge`, `ab-models` | 3 |
| `l6-mean-squared-error.json` | 11 screens (problem, problem `sliders` "MSE at most 0.5", problem, 2 ladder, trap, ladder outlier, code `predict`, code `mse`, generalise, transfer), 14 min | 3 |
| `l7-nudge-and-keep.json` | 10 screens (problem, explore, 2 ladder incl. a table widget for round 1, problem bars of 16 MSEs, trap, ladder step sizes, code `nudge_once`, generalise, transfer), 14 min | 3 |
| `l8-a-script-that-learns.json` | 9 screens (order, code `fit_by_nudging`, ladder console, trap, 2 ladder, script-mode code on stdin, generalise, transfer), 15 min | 3 |
| `review-2.json` | 10 items, difficulty 2 to 4, `pass: 0.8`; skills `ab-nudge`, plus `ab-models` on the three l5 items | |
| `homework-2.json` | 7 items, difficulty 3 to 5: code `mse` + `nudge_once` + `fit_by_nudging` on a fresh table (4), code `fit_with_pairs` (5), order with a distractor (3), numeric MSE (3), numeric one round (4), choice (4), longform "did it find the best line?" (5) | |
| `problems-2.json` | 3 chained problems, 14 parts: shop line (3; l5, l6, l7), stuck line (5; l5 to l8), test script (4; l6, l7, l8) | |

Stage 0, so no performance task. No "gradient", "derivative" or "descent" anywhere; l8's generalise names `multivar` l8 once.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors. Warnings left on level 2 files: five "point hint usually highlights the canvas" and three "problem screen without a canvas" (code and order screens). None on review, homework or problems.
2. `voice-scan.py 35 --summary` on the course folder: 0 over 35 words, 0 lesson ids in code spans, 0 doubled words, 0 explanations over three sentences.
3. `docs/reports/ai-basics-L2-numbers.py` (venv): exit 0, 280 of 280 checks. The 28 "check by hand" lines were read; each byKey names its slip.
4. Playthrough with `--local-cdn`, desktop and `--mobile`, with `--why`: l5 12 checks, l6 14, l7 13, l8 12 (quizzes 3/3); review-2 10 of 10; homework-2 7 of 7, longform marked by the button; problems-2 14 parts, 26 typed slips routed. `grade-all.mjs --code`: 71 widgets and 7 code widgets, 0 failures. `fresh-check.mjs --file problems-2.json`: 0 hits, 1 advisory (the line $y = 1.5x + 1.5$ appears in l6 and as the least squares line of the stuck problem's new data: a coincidence of different data, kept).

Screenshots read at 1280 and 440: the `sliders` widget opened mid-range and moved the line on entry until `start` was set; the derive caption now writes $y = 2.0x - 1.0$ rather than "+ −1.0".

## Numbers (each computed in floats and in exact fractions in the script; the nudging runs twice: exact rule and the widgets' own solutions)

- Course data as the brief: MSE 38.2, 2, 0.1, 0.06; flat line 5.8 errors add to 0, squares 22.8, MSE 4.56. Best line on the 0.1 grid by brute force (1.5, 1.3), equal to least squares.
- Nudging, step 0.1: 34.23, 42.39, 33.14 (and 35.34 for $b$ − 0.1); 16 rounds counting the last that changes nothing; the bars are the 16 MSEs from 38.2 to 0.06 (round 13 is the first below 1). Step 0.5: (1.5, 1.5), 0.1, 4 rounds. Step 0.01: (1.48, 1.36), 0.0608, 155 rounds; single nudges 0.0611, 0.0627, 0.0609, 0.0609; the paired move (1.49, 1.35) gives 0.0606.
- At (1.5, 1.3): $w \pm 0.1$ give 0.17, $b \pm 0.1$ give 0.07. Outlier (5, 15): 7.74. Desk forecasts 3.8 (root about £1.95) and 5. Price line 0.22x + 19.84 (least squares of the five prices), day 35 gives £27.54.
- Code: `nudge_once` tests include a case where only $b$ moves ((2, 0) on $y = 2x + 1$ data, step 1, to (2, 1)); `fit_by_nudging` tests the course data at 0.1 and 0.5, the planted $y = 3x - 2$ and $y = -x + 2$, points on $y = 0$ (1 round) and a single point.
- Homework fresh table (1,2), (2,2), (3,4), (4,5), (5,6): step 0.1 stops at (1.0, 0.8) with 0.16 after 11 rounds while $y = 1.1x + 0.5$ scores 0.14. Problems: shop 0.4, 0.55, round to (1.1, 0.9) at 0.34; stuck 0, 6, 1.52, trials 1.67, 1.59, 1.53, 1.53, while $y = 1.5x + 1.5$ scores 1.5; script 9, (1, 0) after round 1 (a tie at 1.5 does not move $b$), 3 rounds.

## Two brief figures that did not hold, and what the level does instead

- "A planted line $y = 3x - 2$ on four points that it must recover exactly at step 1": on $x = 0, 1, 2, 3$ the rule stops at (2, 0) with MSE 1.5. It recovers (3, −2) in 4 rounds on $x = -1, 0, 1, 2$, which the test uses.
- "A nudger that also tries (w ± step, b ∓ step) reaches 0.06 from where the plain rule stopped at 0.0608": it does not. Run from (0, 0) (or from (1.48, 1.36)) with step 0.01 it stops at (1.51, 1.27) with MSE 0.0602, and with step 0.1 it stops at (1.6, 1.0) with 0.08, worse than plain nudging; an eight-neighbour version also stops at 0.0602. The homework code item keeps the paired rule with these true results, and the longform uses them to show that each rule only promises that none of its own moves helps.

## Conventions

Error is prediction minus actual. The nudge rule: keep the lower trial only if strictly lower; on a tie between $+s$ and $-s$ take $+s$; $w$ first, then $b$ from the new $w$. `fit_by_nudging` counts every round, including the last, and rounds $w$, $b$ and the error to 6 places.

## Proposed course.json change

None.
