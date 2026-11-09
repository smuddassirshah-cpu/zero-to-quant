# backtest level 1: performance task

- `homework-1.json`, item `h-breakout-twice`, index 8 (9 of 9). Added; nothing converted.
- Kind `code` (Python, difficulty 5). Objective (l1): "Write the loop and a vectorised version, and test that they agree."
- Task: a channel-breakout rule that holds inside the channel, new to the course. The learner writes `breakout_loop`, `breakout_vector` (no Python loop) and `agree` from stubs.
- 13 tests, 2 examples: hand closes, channel ties, random walks against a hidden reference, a short series, every data prefix for both functions, an AST loop scan, and `agree` on matching, same-bar, short and nudged pairs. 13 planted bugs all caught (same-bar returns, channel including today, no hold, `shift(-1)`, vector calling the loop, `zip` or `==` in `agree`).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/backtest python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python docs/reports/backtest-1-perf-numbers.py`: 35 checks, exit 0; hand values also as exact fractions.
4. `node tools/playthrough.mjs --set backtest/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed; shots clean.

Freshness: breakout, channel, `agree(`, `walk(`, `HAND`, `ffill`, `rolling(n)` hit only this item; `fresh-check --file` 0 hits.
- Overlapping screens: l1 screens 4, 6 and 9 lay out an event loop, a vectorised signal and the agreement idea; the objective's product needs them. New: the channel with a held target, returns with the lag, and `agree` checked on pairs that differ in timing, length and by $10^{-12}$ (and, from the fix pass, by $5 \times 10^{-9}$).
- Fix pass: 15 tests (was 13). Test 14 rejects a default `np.allclose` in `agree`; test 15 rejects code that calls the prelude's helpers.
