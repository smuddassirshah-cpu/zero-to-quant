# py-found level 2: performance task

- `homework-2.json` item 9 of 9, `h-book-weights`, appended (cap 12, nothing converted). Kind `code`, difficulty 4, pace 900 s, skills `pf-functions`, `pf-collections`.
- Matched objective (l8): "Write pure functions that return new values, and use `None` and an early `return` on purpose." Chosen over l5 "Build a dictionary ..." and l7 "Write functions with default arguments ...": the product also builds a dictionary and takes a default `cash` by keyword, so it proves the whole level.
- Product: `book_weights(book, prices, cash=0.0)` from a one-line stub: a new dictionary of value over total, `None` at a missing price or a zero total, both arguments unchanged.
- Tests: 10 hidden, 1 example; each `None` case is paired with a priced one, so the starter fails 10 of 10. Fifteen planted slips each fail: a missing price priced at 0 or skipped (test 4), no zero check (5, 6), `None` for a cash-only book (5), zero check before cash (6), cash ignored, cash as a ticker, `abs(qty)` (7), weights by shares, `//` (8), book changed in place (9, 10), loop over `prices`, `return` inside the loop, print not return.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; the expected "py-found/L2: has a performance task, remove from perf-pending" warning.
2. `VOICE_BASE=app/content/courses/py-found python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script `python3 -I docs/reports/py-found-2-perf-numbers.py`: exit 0, 0 failures. Route A the solution, route B a value list divided at the end, route C exact fractions for every weight.
4. Playthrough `node tools/playthrough.mjs --set py-found/homework-2 --local-cdn <pkgs>`, with and without `--mobile`, regenerated manifest: All passed, performance starter fails. Shots read cleanly at both widths.

Freshness: `fresh-check.mjs --file` 0 hits. Grep: weight, total, cash, `None`, `book_weights`, `book_value`.

- Overlapping screens: l8 screen 11 (`book_value`, `None` at a missing price), l8 screen 9 (`apply_trade`, a new book), homework-2 `h-net-value` (value or `None`). New: the weights as a second dictionary, cash in the total, the zero-total `None` (empty or hedged book), shorts.

Backlog: 1 bullet.
