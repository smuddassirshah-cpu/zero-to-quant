# representations level 2: performance task

- `homework-2.json`, item `h-detector`, index 0. Kind `code` (Python, difficulty 5).
- Matched objective: l5 "Build an autoencoder with a bottleneck, and read its reconstruction error." (also l8 "Use reconstruction error to flag unusual days, and choose a threshold on held-out data.").
- Task: from a one-line stub, `anomaly_detector(R_train, R_val, R_test, k, q)` fits a linear autoencoder with `k` codes to the training days centred by their mean (500 Adam steps, or the closed form of l6, which spans the same subspace), scores every day by its squared rebuild distance, sets the threshold at the `q` quantile of the validation errors (`np.quantile`) and returns the positions in `R_test` strictly above it.
- 9 hidden tests, 2 examples: an exact list on a two-stock toy (points on the line $(1, 2)$ plus noise, five test points) and the same toy shifted by $(5, -3)$, which catches a missing centring; on `odd_day_panel(3)` and `odd_day_panel(7)` every planted odd day flagged, the market-wide fall on day 700 not flagged, at most 18 flags; an all-normal block of `odd_day_panel(4)` with at most 4 alarms; $q = 1$ on two toy days; a sorted list of integer positions inside the test block. Four mutants: the threshold taken on the test days (the level's trap), positions counted from the start of training, scored days not centred, one code whatever `k`. The number script checks that the trained solution and an SVD twin both pass with margin (at most 14 flags on the two panels, at most 2 alarms on the normal block).
- Overlapping screens: l5 screens 8 and 9 code `encode_decode`, `recon_error` and `train_autoencoder`; l8 screens 8 and 9 code `day_errors`, `threshold_from_val` and `flag_days` against a shipped model (screens counted from 0). The task joins training, centring, calibration and scoring from nothing, on panels and a shifted toy that no screen uses.

Gates:
1. `node tools/validate.mjs`: 0 errors.
2. `VOICE_BASE=app/content/courses/representations python3 docs/reviews/voice-scan.py 35`: 0 over 35 words and 0 lesson ids in code spans.
3. Numbers script `docs/reports/representations-L2-numbers.py` through `node tools/run-number-scripts.mjs --only representations-L2` (strict): 297 of 297 checks, exit 0; it reruns the solution and an SVD twin against every test.
4. Playthrough `--set representations/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: all passed, the starter fails. Desktop time per hidden test in Pyodide: 107 to 281 ms (budget 4,000 ms a case).
