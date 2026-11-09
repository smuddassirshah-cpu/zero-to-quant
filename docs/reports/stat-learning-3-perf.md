# stat-learning level 3: performance task

- File: `app/content/courses/stat-learning/homework-3.json`, item 10 of 10, `h-lag-split`, kind `code` (Python, standard library), difficulty 5. Appended; nothing converted (9 items before).
- Objective (l14, verb rule "Build"): "Build lagged features without look-ahead and split in time order." Chosen over l10's "Explain ..." as a code product.
- Task: from a blank stub, `lag_split(prices, lags, horizon, split)` builds lagged returns and an $h$-day direction label, then splits at day `split` so no training row reads a test-period price, label included. 1 example, 6 hidden tests (isclose); test 6 has an empty training set.
- Planted slips, each failing a hidden test (script): forward shift, backward label, shuffled split, no purge, next-day purge only, dropped days put in test, tie counted as a rise, lags sorted, wrap-round first row, price difference, test features from the test block alone.
- Fresh: l14 screens 3 and 4 and `h-pipeline` use fixed features, a one-day label and a row-count split. New here: arbitrary lags from prices, the $h$-day label and the purge it forces. Grep terms: lag_split, lag, horizon, purge, shift(, roll, pct_change, look-ahead, shuffle. `fresh-check --file`: 0 hits.

Gates: `node tools/validate.mjs` 0 errors (expected perf-pending warning); `VOICE_BASE=app/content/courses/stat-learning python3 docs/reviews/voice-scan.py 35` 0 and 0; `venv/bin/python docs/reports/stat-learning-3-perf-numbers.py` exit 0; `node tools/playthrough.mjs --set stat-learning/homework-3 --local-cdn <pkgs>` All passed, with and without `--mobile`.

Overlapping screens: l14-up-or-down screens[1] (a row of features for day $t$, the label is day $t + 1$), [2] (`make_features` coded with a 20-day window), [3] (train on the first rows and test on the last, in time order) and quiz q-align (a slice that reaches day $t + 1$), homework-3 `h-pipeline` (the same features and split); new parts: `lag_split` from a blank stub with arbitrary lags, an $h$-day direction label, the purge so that no training label reads the test period, ties not counted as a rise, and an empty training set (test 6).
