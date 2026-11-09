# opt-dash level 1: performance task

`homework-1.json`, `h-parity-fit`, item 9 of 9 (added; cap 12). Kind `code` (Python, pandas).

Objective: l3 "Write `implied_forward` and `implied_q` for the dashboard." Chosen because the forward and yield feed every later level.

Task: `parity_fit(df_T, S, T)` returns `(F, r, q)` from a least-squares line of $C - P$ against $K$, with NaNs under three pairs or for a non-positive discount factor. The lessons code only the one-strike median forward with $r$ given; the regression is shown as a table, never coded.

Tests: 11 hidden, 2 examples. Ten planted bugs each fail, first at their named test: put-call sign, discounting omitted, rate not divided by $T$, zero-bid quote kept, pairing by position, pair minimums, slope guard, yield sign, rate as $1 - D$.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; only the expected perf-pending warning.
2. `VOICE_BASE=app/content/courses/opt-dash python3 docs/reviews/voice-scan.py 35`: 0 and 0 (also 0 and 0 before).
3. `<venv>/bin/python -I docs/reports/opt-dash-1-perf-numbers.py`: exit 0.
4. `node tools/playthrough.mjs --set opt-dash/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed, starter fails. Shots clean.

Freshness grep: `parity_fit`, `least squares`, `polyfit`, `lstsq`, `intercept`, `seed=58`, `zero_bid`.

Overlapping screens: l3-rates-dividends screens[0] and [1] (call minus put against strike and the parity line), [2] (the one-strike median forward, $r$ given), [4] (fitting both $r$ and $q$ from a line, shown as a table, never coded), [6] (parity to the forward), [7] `implied_forward` and [8] `implied_q` (coded); new parts: `parity_fit` as a least-squares regression of $C - P$ on $K$ returning $(F, r, q)$, NaN under three pairs or for a non-positive discount factor, zero-bid quotes dropped, pairing by strike.
