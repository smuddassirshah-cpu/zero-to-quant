# pytest level 3: performance task

- `homework-3.json`, item `h3-fee-test-first`, index 8 (9 of 9). Added, not converted.
- Kind `code` (Python). Objective (l10): "Write a failing test, then the code that passes it". Chosen over l9 and l11: its product is tests and code, and `h3-lookahead` already asks for l11's.
- Design: the learner writes tests and `broker_fee` in one file. Hidden versions replace their function (by AST) for each pytest run. 15 tests, 1 example: four on their function; three tests collected; green on their code and a correct version, also reversed; every test red on the empty starter function; six broken versions caught. All eleven planted wrong files fail (round numbers only, a penny tolerance, expected values from `broker_fee`, a shared list).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/pytest python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python docs/reports/pytest-3-perf-numbers.py`: 45 checks, exit 0.
4. `node tools/playthrough.mjs --set pytest/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed; shots clean.

Freshness: `broker_fee`, notional, £4.95: only here; `fresh-check --file` no hit on this item.
- Overlapping screens: l10 screens 1 to 4, 7 and 9, l8 screens 4 and 9 and `h2-ma-signal` lay out red, then green, with given tests. New: tests and code from a fee schedule, the minimum, cap and half-penny rounding, zero as an error, every test red first.
