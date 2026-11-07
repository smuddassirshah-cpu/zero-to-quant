# opt-dash level 1: performance task

`homework-1.json`, `h-parity-fit`, item 9 of 9 (added; cap 12). Kind `code` (Python, pandas).

Objective: l3 "Write `implied_forward` and `implied_q` for the dashboard." Chosen over l1 and l2 (`mid`, `chain_table`, `clean_quotes`, `drop_report`) because the forward and yield feed every later level.

Task: `parity_fit(df_T, S, T)` returns `(F, r, q)` from a least-squares line of $C - P$ against $K$, with NaNs under three pairs or for a non-positive discount factor. The lessons code only the one-strike median forward with $r$ given; the regression is shown as a table, never coded. No level function is loaded.

Tests: 11 hidden, 2 examples. Ten planted bugs each fail, first at their named test: put-call sign, discounting omitted, rate not divided by $T$, zero-bid quote kept, pairing by position, four-pair minimum, no pair minimum, no slope guard, yield sign, rate as $1 - D$.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; only the expected perf-pending warning.
2. `VOICE_BASE=app/content/courses/opt-dash python3 docs/reviews/voice-scan.py 35`: 0 and 0 (also 0 and 0 before).
3. `<venv>/bin/python -I docs/reports/opt-dash-1-perf-numbers.py`: exit 0.
4. `node tools/playthrough.mjs --set opt-dash/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed, starter fails. Shots clean.

Freshness grep: `parity_fit`, `least squares`, `polyfit`, `lstsq`, `intercept`, `slope`, `seed=58`, `S=96`, `zero_bid`.
