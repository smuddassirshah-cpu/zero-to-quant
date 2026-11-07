# alpha level 2: performance task

- `homework-2.json` item 8 of 8, `h-momentum-pct`, appended (cap 12, nothing converted). Kind `code`, difficulty 4, pace 900 s, skill `al-signal`.
- Objective (l5): "Build a cross-sectional momentum signal." Preferred to l6's reversal: tests can catch an unskipped month and a time-series rank.
- Product: `momentum_pct(px, lookback=12, skip=1)` from a stub, on month-end total-return prices: return from `lookback` to `skip` months back, scored only when listed at $t$, ranked across shares per month as rank over count, ties averaged.
- 12 tests, 1 example. Ten planted bugs all fail: no skip (tests 2 to 4), time-series rank, shift the wrong way (test 7 spy), no listed check (test 5), window a month early (test 6), raw rank, unscored shares ranked as 0, descending, ties by order (test 8), l7-style (r - 1)/(n - 1).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors (expected perf-pending warning).
2. `VOICE_BASE=app/content/courses/alpha python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python docs/reports/alpha-2-perf-numbers.py`: exit 0; solution and a plain loop with a hand average rank agree; starter fails 12 of 12.
4. `node tools/playthrough.mjs --set alpha/homework-2 --local-cdn <pkgs>` with and without `--mobile`: All passed; shots read cleanly.

Freshness: `fresh-check.mjs --file` 1 hit, on the existing item 1 (`rolling_beta`, momentum-rep), not this item. Grep of momentum_pct, month end, pct=True, jumped, refreshes: l7 has `rank(pct=True)` only as its pooled-rank trap.

Backlog: 0 bullets.
