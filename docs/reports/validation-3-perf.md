# validation level 3: performance task

- `homework-3.json` item 10 of 10, `h-dead-firms`, appended. Kind `code`.
- Objective (l11): "Build a point-in-time universe and keep dead firms with their delisting returns." Product: `survivor_free_returns(rets, listings, delist)`, monthly equal-weight `held` and `ret` from listing records over a back-filled vendor file.
- 8 tests, 1 example. 14 planted bugs fail, each first where its byKey fits: today's listing or back-filled returns (test 1); dead firm dropped early (tests 1, 2); delisting return ignored, replacing, added or late (test 3); a record ending before the file (test 5).
- Overlap: l11 screens 3 (`survivor_bias`), 5 (`universe_as_of`), 7, 8 (the pipeline as an order); `h-delist`, `h-order`, `h-audit`; `r-top100`. New: back-fill, the delisting return compounded with the regular return, records outside the file.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/validation python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python docs/reports/validation-3-perf-numbers.py`: exit 0; a month-by-month loop agrees; starter fails 8 of 8.
4. `node tools/playthrough.mjs --set validation/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed; shots clean.

Freshness: `fresh-check.mjs --file` 0 hits; grep survivor_free_returns, back-fill, vendor, compound: item and l11 screen 8 only.

Backlog: 0 bullets.
