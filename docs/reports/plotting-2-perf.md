# plotting level 2: performance task

- `homework-2.json` item 9 of 9, `h-wealth-peak`, appended. Kind `code`, difficulty 4.
- Objective: l7 "Build the wealth curve with cumprod and plot its running peak" (the only verb-rule match).
- Grading: the learner's Axes is read through its artists, as the course's other chart items do. A prelude helper finds each line by its label; tests read x and y data, line style, legend texts, y scale and y label. 10 tests, 1 example. 15 planted slips fail: years unsorted, no opening point, capital ignored, peak taken before the opening point, linear axis, legend before the peak, no legend, flat peak, caller sorted in place, added returns, axes swapped, solid peak, no £, logs on a linear axis, capital fixed.

Gates:
1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. Voice, `VOICE_BASE=app/content/courses/plotting python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `<venv>/bin/python -I docs/reports/plotting-2-perf-numbers.py`: exit 0.
4. Playthrough, `node tools/playthrough.mjs --set plotting/homework-2 --local-cdn <pkgs>`, with and without `--mobile`, new manifest: All passed.

Freshness: `fresh-check --file` no hit. Grep: cumprod, running peak, capital, legend, set_yscale, client, yearly, sort_index, Wealth.
Overlapping screens: l7 screens 4, 8 and 9 (cumprod wealth, the pattern, wealth of £1 with a dashed peak), l7 screen 7 and quiz q3, l9 screen 6 (log axis), l2 screens 5 and 7 (legend), homework-2 `h2` (yearly log chart), review-2 `r7`, l13 quiz `q-sort-first`. New: yearly returns out of order, wealth in £ from an opening year, a peak that starts at the capital, a named two-line legend, inputs unchanged.

Backlog: 2 bullets.
