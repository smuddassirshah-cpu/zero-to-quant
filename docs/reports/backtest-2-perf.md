# backtest level 2: performance task

- `homework-2.json`, item `h2-never-peeks`, index 9 (10 of 10). Added; nothing converted.
- Kind `code` (Python, difficulty 5). Objective (l8): "Write a test that fails if the engine ever peeks at the future."
- The widget grades the test directly: the prelude's `verdict(engine)` runs the learner's `test_never_peeks(engine)`. No detector workaround needed.
- 9 tests, 2 examples. Three honest engines must pass. Six leaks must fail: next close, a rare peek, full-sample vol, next open, same-close fill, cost read from the close. Nine wrong tests are caught, among them three cuts, every fifth cut, cut form only, too strict on row $t$, 12 bars, Sharpe below 2, and copying `clean_engine`.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/backtest python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python docs/reports/backtest-2-perf-numbers.py`: 33 checks, exit 0; each leak also measured directly.
4. `node tools/playthrough.mjs --set backtest/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed; shots clean.

Freshness: `test_never_peeks`, `daily_bars`, contract, settled, `tanh` hit only this item; `fresh-check --file` 0 hits. Item 7, `h2-same-close`, already explains the cost-from-close leak.
- Overlapping screens: l8 screens 2, 4, 5, 8 and 9 lay out the cut and replace forms and ask about a same-close fill. New: the test from a blank start, every cut, the check on bar $t$'s shares and cash after its open, and the cost-from-close leak.
