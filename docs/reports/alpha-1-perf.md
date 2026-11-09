# alpha level 1: performance task

- `homework-1.json` item 8 of 8, `h-review-universe`, appended (cap 12, nothing converted). Kind `code`, difficulty 5, pace 1200 s.
- Objective (l1): "Build the universe from listing and trailing £ volume, with no look-ahead." Preferred to l4's panel because tests can catch look-ahead.
- Product: `review_universe(close, shares, listed, n, window)` from a stub: monthly review, top `n` by trailing mean £ volume, held from the next day, a dead share leaves at once.
- 11 tests, 1 example. Nine planted bugs all fail: same-month list, traded on review day, full-sample volume, window a day ahead, partial window, dead share kept, shares not £, `rank <= n` ties, ascending sort. Test 7 changes February volume; nothing to 29 February may move.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors (expected perf-pending warning).
2. `VOICE_BASE=app/content/courses/alpha python3 docs/reviews/voice-scan.py 35`: 0 and 0 (0 and 0 before).
3. `<venv>/bin/python docs/reports/alpha-1-perf-numbers.py`: exit 0; solution and an independent day loop agree; starter fails 11 of 11.
4. `node tools/playthrough.mjs --set alpha/homework-1 --local-cdn <pkgs>` with and without `--mobile`: All passed; shots read cleanly.

Freshness: `fresh-check.mjs --file` 0 hits; grep of review_universe, shares traded, once a month, highest mean, 200 largest, members, sorts first finds nothing outside the item but l1's "today's 200 largest".

Backlog: 0 bullets (the toast in the 440 shot is BACKLOG-INBOX line 1581).
- Overlapping screens: l1 screens 6, 7 and 9 lay out the trailing-volume filter. New: £ volume from close and shares, monthly reviews, the top $n$ with ties, the list held from the next day.
