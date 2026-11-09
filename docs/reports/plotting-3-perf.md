# plotting level 3: performance task

- `homework-3.json` item 11 of 11, `h-price-file-report`, appended (the homework had 10 items). Kind `code`, difficulty 5.
- Objective: l13 "Build the 1.1 exit project: one script from a price file to three charts". l10 "Build and save a four-panel backtest results figure" also matches; l13's is the level's end-to-end product, and `h-backtest-figure` already asks for l10's.
- Grading: the returned figure is read through its artists, as the course's chart items do. Prelude helpers read each panel's longest line point by point (date, value), the "Max drawdown" annotation, the suptitle and the saved PNG's dpi. 10 tests, 1 example. 16 planted slips fail: file order kept, repeated day kept, both copies dropped, duplicates judged by close, returns on the earlier date, population sd, times 252, overall top, arrow at the lowest close, no sharex, dates as text, default dpi, not saved, title from the population sd, title from the last rolling value, unsigned label. A csv-and-loops route passes.

Gates:
1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. Voice, `VOICE_BASE=app/content/courses/plotting python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `<venv>/bin/python -I docs/reports/plotting-3-perf-numbers.py`: exit 0.
4. Playthrough, `node tools/playthrough.mjs --set plotting/homework-3 --local-cdn <pkgs>`, with and without `--mobile`, new manifest: All passed.

Freshness: `fresh-check --file` no hit. Grep: read_csv, StringIO, drop_duplicates, suptitle, savefig, dpi, running peak, idxmin, newest first, sort.
Overlapping screens: l13 screens 1, 2, 3, 4, 5, 6 and 8 and quiz `q-sort-first`, `q-mdd`; l10 screens 4 and 6; homework-2 `h1`, `h3`, `h4`; homework-3 `h-backtest-figure`; review-3 `r-dpi`, `r-mdd-order`. New: the exit figure on a date axis parsed from the file (l13 screen 8 plots day numbers; `h4` shows a date arrow), a repeated day beside two days that share a close, both figures in a suptitle, the save path as an argument.

Backlog: 2 bullets.
