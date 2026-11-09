# fin-ml level 2: performance task

- `homework-2.json` item 8 of 8, `h-return-rank`, appended. `code`, difficulty 4, `fm-features`.
- Objective: l7 "Build cross-sectional rank features", over l5: a time-series rank or a stale close leaks or mis-trades silently, in range. The task builds l5's return too.
- Product: `return_rank(df, k)`, unsorted long panel with NaN closes; $k$-date return, ranked per date, ties averaged, $-1$ to 1, lone share 0.
- 13 tests, 1 example. 24 planted bugs fail (time-series rank, tie methods, `pct_change` padding, ffill, $n_t$ miscounts, wrong scales, inverted return, price level, unsorted, $k \pm 1$, lone share), each with a byKey line on its first failure. Loop, log and difference routes pass.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/fin-ml python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python -I docs/reports/fin-ml-2-perf-numbers.py`: exit 0.
4. `node tools/playthrough.mjs --set fin-ml/homework-2 --local-cdn <pkgs>`, with and without `--mobile`, new manifest: All passed.

Freshness: `fresh-check --file` hits only item 1. Grep: return_rank, fill_method, linearly, lowest first, n_t, alone, shuffl, no close.
Overlapping screens: l7 screens 4 and 6, `h-builder` mom_rank. New: NaN closes, unsorted rows, the $-1$ to 1 scale, index alignment.

Backlog: 1 bullet.
