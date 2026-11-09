# stat-learning level 2: performance task

- File: `app/content/courses/stat-learning/homework-2.json`, item 9 of 9, `h-ridge-formula`, kind `code` (Python), difficulty 5. Appended; nothing converted (8 items before).
- Objective (l9, verb rule "Build"): "Build a scaler and a penalised model into one pipeline fitted on training rows only."
- Task: from a blank stub, `ridge_formula(X, y, n_train, alpha)` fits scaler and ridge on the first `n_train` rows and returns the model in raw units plus the test MSE. 1 example (one feature, hand-checkable: 1.95, 0.35, 1.5625), 6 hidden tests, isclose. Test 5 has a dummy constant on training rows.
- Planted slips, all failing a test (script): scaler on all rows, penalty on unscaled features, pipeline on all rows, test rows scaled by their own statistics, scaled coefficients, intercept not converted, ddof 1, penalised intercept, no constant-column guard (test 5 only), mean-error objective.
- Fresh: new over l9 screens 5 and 9 and `h-end-to-end` are the raw-unit formula and the split inside the function. The constant column repeats l9 screen 8 on purpose (test 5). Grep terms: ridge_formula, raw unit, per unit, intercept, scale_, mean_, Ridge(, constant, dummy. `fresh-check --file`: 0 hits.

Gates: `node tools/validate.mjs` 0 errors (expected perf-pending warning); `VOICE_BASE=app/content/courses/stat-learning python3 docs/reviews/voice-scan.py 35` 0 and 0; `venv/bin/python docs/reports/stat-learning-2-perf-numbers.py` exit 0; `node tools/playthrough.mjs --set stat-learning/homework-2 --local-cdn <pkgs>` All passed, with and without `--mobile`.
- Overlapping screens: l9 screens 5, 8 and 9 and `h-end-to-end` (scaler, penalised model, constants), as above.
