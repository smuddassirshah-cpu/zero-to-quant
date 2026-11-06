# Engine pass T: items 581 and 582

Rule 581 (`wrongCannotFire` in app/tools/validate.mjs) runs as a warning (`WRONG_FIRE_LEVEL`) because it found true hits in existing content. No content was edited. Route the 14 below to fix agents, then set the level to 'error'. The 19 overlaps between wrong entries stay warnings by design (the earlier entry takes the key).

## Wrong value cannot fire (14)

- content/courses/limits/l1-getting-closer.json  screens[0].widget.wrong[2]: wrong value 1.999 lies inside the answer 2 tolerance (+-0.001), so it is graded correct and "last-row" can never fire
- content/courses/integrals/l2-thinner.json  screens[4].widget.wrong[2]: wrong "half-term" (0.33833 +-0.000005001) overlaps the answer 0.33835 tolerance (+-0.000015001); the overlap is graded correct
- content/courses/vectors/l12-numpy-matrices.json  screens[1].widget.wrong[0]: wrong value 5.000000000000001 lies inside the answer 5 tolerance (+-1e-9), so it is graded correct and "printed" can never fire
- content/courses/graphs-dp/l9-arbitrage-cycle.json  screens[8].widget.wrong[1]: wrong value -264 lies inside the answer -264.03 tolerance (+-1), so it is graded correct and "sum" can never fire
- content/courses/graphs-dp/homework-4.json  items[6].widget.wrong[1]: wrong value 0.3983 lies inside the answer 0.3987 tolerance (+-0.000500001), so it is graded correct and "r5" can never fire
- content/courses/analysis/l8-bounded-and-monotone.json  screens[0].widget.wrong[0]: wrong value 1.9957 lies inside the answer 2 tolerance (+-0.01), so it is graded correct and "last" can never fire
- content/courses/validation/review-2.json  items[6].widget.wrong[1]: wrong "half" (0.05 +-0.000200001) overlaps the answer 0.0497 tolerance (+-0.000200001); the overlap is graded correct
- content/courses/arma/l1-returns-not-prices.json  quiz[0].widget.wrong[0]: wrong value -0.02 lies inside the answer -0.0202 tolerance (+-0.000200001), so it is graded correct and "simple" can never fire
- content/courses/coint/review-1.json  items[0].widget.wrong[1]: wrong value 4.97 lies inside the answer 4.95 tolerance (+-0.02), so it is graded correct and "n" can never fire
- content/courses/backtest/l11-turnover.json  screens[1].widget.wrong[0]: wrong value 3.33 lies inside the answer 3.439 tolerance (+-0.15), so it is graded correct and "gross" can never fire
- content/courses/numerics/l4-stability.json  screens[3].widget.wrong[0]: wrong value 2e-16 lies inside the answer 0 tolerance (+-1e-9), so it is graded correct and "exact" can never fire
- content/courses/stat-models/l11-permutation-tests.json  screens[2].widget.wrong[0]: wrong value 0.20916 lies inside the answer 0.2092 tolerance (+-0.000200001), so it is graded correct and "plain" can never fire
- content/courses/stat-models/l11-permutation-tests.json  screens[7].widget.wrong[0]: wrong value 0.0101 lies inside the answer 0.01 tolerance (+-0.000100001), so it is graded correct and "b" can never fire
- content/courses/stat-models/review-3.json  items[1].widget.wrong[0]: wrong value 0.002004 lies inside the answer 0.002 tolerance (+-0.000010001), so it is graded correct and "b" can never fire

## Wrong entries overlapping each other (19)

- content/courses/ratio/l13-currencies.json  screens[3].widget.wrong[2]: wrong "one-rate" overlaps wrong[0] "same"; the earlier entry takes the key where they overlap
- content/courses/trig/l1-squares-on-sides.json  screens[10].widget.wrong[1]: wrong "no-root" overlaps wrong[0] "added"; the earlier entry takes the key where they overlap
- content/courses/taylor/l2-how-wrong.json  screens[10].widget.wrong[3]: wrong "per-contract" overlaps wrong[2] "zero"; the earlier entry takes the key where they overlap
- content/courses/taylor/homework-3.json  items[4].widget.wrong[1]: wrong "pair" overlaps wrong[0] "add"; the earlier entry takes the key where they overlap
- content/courses/multivar/l4-chain-two-inputs.json  screens[8].widget.wrong[4]: wrong "per-option" overlaps wrong[3] "rates"; the earlier entry takes the key where they overlap
- content/courses/multivar/homework-5.json  items[0].widget.wrong[1]: wrong "area" overlaps wrong[0] "noJ"; the earlier entry takes the key where they overlap
- content/courses/conditional/l8-base-rates.json  screens[3].widget.wrong[2]: wrong "base" overlaps wrong[1] "joint"; the earlier entry takes the key where they overlap
- content/courses/conditional/l9-natural-frequencies.json  screens[4].widget.wrong[2]: wrong "base" overlaps wrong[1] "everyone"; the earlier entry takes the key where they overlap
- content/courses/markov/l2-transition-matrix.json  screens[8].widget.wrong[1]: wrong "no-migration" overlaps wrong[0] "three-times"; the earlier entry takes the key where they overlap
- content/courses/markov/l10-gamblers-ruin.json  screens[7].widget.wrong[1]: wrong "p" overlaps wrong[0] "fair"; the earlier entry takes the key where they overlap
- content/courses/markov/l20-when-stopping-fails.json  screens[5].widget.wrong[1]: wrong "most" overlaps wrong[0] "win"; the earlier entry takes the key where they overlap
- content/courses/trees/l13-rules-of-thumb.json  screens[7].widget.wrong[1]: wrong "atm" overlaps wrong[0] "rule"; the earlier entry takes the key where they overlap
- content/courses/ds/review-4.json  items[2].widget.wrong[1]: wrong "none0" overlaps wrong[0] "nodes"; the earlier entry takes the key where they overlap
- content/courses/analysis/l19-uniform-convergence.json  screens[4].widget.wrong[2]: wrong "edge" overlaps wrong[1] "tenth"; the earlier entry takes the key where they overlap
- content/courses/complex/l8-exp-and-log.json  screens[5].widget.wrong[1]: wrong "pi" overlaps wrong[0] "above"; the earlier entry takes the key where they overlap
- content/courses/stat-learning/review-2.json  items[0].widget.wrong[1]: wrong "flip" overlaps wrong[0] "pos"; the earlier entry takes the key where they overlap
- content/courses/arma/review-1.json  items[3].widget.wrong[1]: wrong "times" overlaps wrong[0] "a"; the earlier entry takes the key where they overlap
- content/courses/opt-dash/homework-1.json  items[4].widget.wrong[1]: wrong "1y" overlaps wrong[0] "no-T"; the earlier entry takes the key where they overlap
- content/courses/numerics/l12-stiff-equations.json  screens[0].widget.wrong[1]: wrong "small" overlaps wrong[0] "exact"; the earlier entry takes the key where they overlap

## Tests

- node app/tools/test-validate-wrong-fire.mjs: 5 of 5 (clean value, equal to answer, wrong tol reaching answer, two overlapping wrongs, two separate wrongs)
- python3 app/tools/test-numbers-lib.py: pass (check_wrongs on a synthetic file and the real odes L3)
- validator: 0 errors
