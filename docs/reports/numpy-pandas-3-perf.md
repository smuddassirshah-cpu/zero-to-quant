# numpy-pandas level 3: performance task

- `homework-3.json` item 9 of 9, `h-trend-shares`. Kind `code`, difficulty 5, appended.
- Objective: l10 "Build a moving average signal that trades only on what it knew." (only match).
- Tests: 11, 1 example. 18 planted slips fail: no lag, `shift(-1)`, forward return on the decision row, three no-groupby routes, ungrouped `shift` or `pct_change`, no sort, `min_periods=1`, `>=`, fast and slow swapped, one average, centred windows, first row 0, wide pivot on table dates, `df` changed in place, index lost. A loop route passes.

Gates:
1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. Voice, `VOICE_BASE=app/content/courses/numpy-pandas python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `<venv>/bin/python -I docs/reports/numpy-pandas-3-perf-numbers.py`: exit 0.
4. Playthrough, `node tools/playthrough.mjs --set numpy-pandas/homework-3 --local-cdn <pkgs>`, with and without `--mobile`, new manifest: All passed.

Freshness: `fresh-check --file` no hit. Grep: crossover, fast, slow, transform, trend, rolling.
Overlapping screens: l10 screens 6, 7 and 10 (`ma_strategy`), l9 screen 11, l12 screens 7 and 9, `h-backtest-review`, `h-vol-target`, review-3 `r-centred` and `r-interleaved`. New: a long table of several shares in any order, two averages, ties out, a share's own rows across a missing day, `df` unchanged.

Backlog: 1 bullet.
