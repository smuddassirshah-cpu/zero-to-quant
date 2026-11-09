# pytest level 1: performance task

- `homework-1.json`, item `h-average-cost-tests`, index 7 (8 of 8). Added, not converted.
- Kind `code` (Python). Objective (l2): "Write a test function in arrange, act, assert order". Chosen over l1's: its product is a whole pytest file.
- Design: `average_cost(fills, fee)` sits in a hidden `costs.py`, tested from a description; pytest runs once per version written there. 12 tests, 1 example: three tests collected; three correct versions pass, also reversed; six broken are caught; each test fails on one. All twelve planted wrong files fail (self-comparison, early `return`, 5p tolerance, shared list).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/pytest python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python docs/reports/pytest-1-perf-numbers.py`: 33 checks, exit 0.
4. `node tools/playthrough.mjs --set pytest/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed; shots clean.

Freshness: `average_cost`, `costs.py`, fill: only here; `fresh-check --file` 0 hits.
- Overlapping screens: l2 screens 4, 5 and 9 and l4 screens 7 and 9 lay out arrange, act, assert tests with `pytest.approx` against broken versions; `h-drawdown-tests` and `r-total-return` too. New: a blank file, a black-box function, per-fill fees and size weights, every test catching a bug, collection and order checks.
