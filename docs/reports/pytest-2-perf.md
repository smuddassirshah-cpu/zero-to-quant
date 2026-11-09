# pytest level 2: performance task

- `homework-2.json`, item `h2-curve-properties`, index 8 (9 of 9). Added, not converted.
- Kind `code` (Python). Objective (l5): "Write property checks that hold for every input", the only match at this level.
- Design: `equity_curve(start, returns)` sits in a hidden `curve.py`, tested from a description; pytest runs once per version written there. 14 tests, 1 example: three tests collected; three correct versions pass, also reversed; seven broken are caught; each test fails on one and makes five calls or more. All eleven planted wrong files fail (hand answers only, no flat day, end value only, a module-scoped fixture one test extends).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/pytest python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python docs/reports/pytest-2-perf-numbers.py`: 38 checks, exit 0; fixture builds counted in real pytest 8.1.1.
4. `node tools/playthrough.mjs --set pytest/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed; shots clean.

Freshness: `equity_curve`, `curve.py`: only here; `fresh-check --file` no hit on this item.
- Overlapping screens: l5 screens 5 and 8, l6 screens 4 and 8, l7 screen 6 and `h2-drawdowns` lay out rules over every input, parametrised tables and a shared list. New: rules chosen from a description, five inputs per rule, the input-unchanged rule, a flat day, reverse order.
