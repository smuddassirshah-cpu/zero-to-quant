# options level 2: performance task

`homework-2.json`, `h-strategy-card`, item 10 of 10 (appended; nothing converted). Kind `code` (Python, standard library).

Objective: l5 "Build a spread from two strikes and read its capped payoff." l6 and l7 "Build..." also match; the task covers all three.

Task: `strategy_card(legs)` returns cost today, best and worst profit at expiry (`inf` where unlimited) and every break-even once, for any position of calls, puts and shares.

Tests: 12 hidden, 2 examples, isclose within 1e-9. Twelve planted bugs each fail (no £0 point, no slope, `abs(qty)`, share left out, unsorted strikes, kink root twice, 1p grid, and more).

Overlapping screens: l8 screen 10 (`payoff(legs, S)`), `h-code-profit` (same leg format), l5 screen 8, l6 screen 8, l7 screen 9 (one strategy's formulas). New: any position, limits from the slope, the £0 extreme, kink and touch roots once, ratio positions.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/options python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/options-2-perf-numbers.py`: exit 0.
4. `node tools/playthrough.mjs --set options/homework-2 --local-cdn <pkgs>`, with and without `--mobile`, regenerated manifest: All passed, starter fails.

Freshness: `fresh-check --file` 0 hits; grep `strategy_card`, `breakevens`, `float('inf')`, `unlimited`, `ratio`.
