# ensembles level 2: performance task

- `homework-2.json` item 9 of 9, `hw-floor-derive`, appended (8 items before, cap 12). Kind `derivation`: the verb is explain, but the answer is written maths, the variance of an average of correlated predictors, and a derivation beats a spoken explanation as proof.
- Objective (l6): "Explain why only lower correlation, not more trees, lowers the variance floor of an average." The bias step also serves l5's "why bagging helps deep trees, not stumps".
- Rubric 2, 3, 2, 2, 1: assumptions, derivation, limit with the colleague's numbers, second forest with bias (all `required`); checks at the ends (optional). `rubric-passes.mjs`: passes 1-2-3-4 and all five; rows 1 to 4 cannot be left out.
- Overlap: l6 screen 3 orders this derivation; l6 screens 2, 4, 5, quiz q-avgvar, review rv-floor, homework hw-how-many-trees and hw-derive-b-star use the formula. New: blank-page derivation with reasons, spread forecasts in bp², the tenfold claim below the floor, bias kept by linearity and the MSE split, the crossing of two forests at B = 3.5.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/ensembles python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 docs/reports/ensembles-2-perf-numbers.py`: exit 0 (exact fractions, covariance matrix, seeded simulation).
4. `node tools/playthrough.mjs --set ensembles/homework-2 --local-cdn <pkgs>`, with and without `--mobile`, regenerated manifest: All passed. Full-height model shot: 6 displays, none scroll at 440 px.

Freshness: `fresh-check.mjs --file` 0 hits; grep spread, basis point, bp, tenfold, cross, bias, covarian, floor, unchanged, 0.08: hits read, none repeats the task.

Backlog: 0 new bullets.
