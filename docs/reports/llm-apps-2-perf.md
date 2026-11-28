# llm-apps level 2: performance task

- `homework-2.json`, item `h-text-signal`, index 0. Kind `code` (Python, difficulty 5).
- Matched objective: l8 "Design a text-signal backtest that survives a cut-off check and the number of models tried." (also l6 "Build a daily text feature stamped with when each document became known.").
- Task: from a stub holding only the signature, `text_signal_report(panel, docs, cutoff, buffer_days, folds, n_trials)` keeps dates later than the cut-off plus a calendar buffer, builds the feature by a backward as-of join at the 16:30 close, cuts the kept days into walk-forward folds (bounds `round(i * n / folds)`), trades folds 2 on with the sign of the feature minus the earlier folds' mean, and returns the annualised Sharpe and its haircut $s - \sqrt{2\ln N}/\sqrt T$ with $T$ the traded days over 252.
- 7 hidden tests, 1 example: five ten-day hand cases (within relative $10^{-9}$) each built so that one leak or slip changes the answer (no buffer, a document published at 17:10, a threshold fitted on later days, the years in the haircut, a cut-off before every date), and the seeded market from `llm_apps_ops_l2.make_market` at seed 0 (no buffer, 5 folds, 12 trials) and seed 3 (60-day buffer, 4 folds, 8 trials), within 0.0005. Four mutants, each first failing its own test with a `byKey` line: no buffer, date join, full-window threshold, haircut over all clean days.
- Overlapping screens: l5 screens 9 and 10 code `clean_window`, `share_after_cutoff` and `sharpe_by_period`; l6 screen 9 codes `known_by` and `asof_feature`; l8 screens 9 and 10 code `haircut` and `honest_backtest` (screens counted from 0). The task adds the buffer and the haircut over the traded days to l8's backtest, from nothing, and is tested on hand cases and seeds no screen uses (seed 3 with a buffer).

Gates:
1. `node tools/validate.mjs`: 0 errors.
2. `VOICE_BASE=app/content/courses/llm-apps python3 docs/reviews/voice-scan.py 35`: 0 over 35 words and 0 lesson ids in code spans.
3. Numbers script `docs/reports/llm-apps-L2-numbers.py` (venv, strict, through `tools/run-number-scripts.mjs`): exit 0; it reruns the solution and a pandas twin against every test and checks every mutant's first failing test.
4. Playthrough `--set llm-apps/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: all passed, the starter fails. `grade-all.mjs --code --strict-feedback`: 0 failures (also with parallel jobs, after the pandas prelude noted in the report).
