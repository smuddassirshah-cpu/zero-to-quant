# py-found level 2: performance task

- `homework-2.json` item 9 of 9, `h-book-weights`, appended. Kind `code`, difficulty 4.
- Matched objective (l8): "Write pure functions that return new values, and use `None` and an early `return` on purpose." It also builds a dictionary and takes `cash` by keyword.
- Product: `book_weights(book, prices, cash=0.0)`, a new dictionary of weights, `None` at a missing price or a zero total.
- Tests: 10 hidden, 1 example; each `None` case is paired with a priced one. Fifteen planted slips fail, among them a missing price as 0, `abs(qty)`, `//`, the book changed in place.

Gates (exact commands; `<pkgs>` is the scratchpad folder):
1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, plus the expected perf-pending warning.
2. Voice, `VOICE_BASE=app/content/courses/py-found python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `python3 -I docs/reports/py-found-2-perf-numbers.py`: exit 0.
4. Playthrough, `node tools/playthrough.mjs --set py-found/homework-2 --local-cdn <pkgs>`, with and without `--mobile`, regenerated manifest: All passed, starter fails; shots clean.

Freshness: `fresh-check.mjs --file` 0 hits. Grep: weight, total, cash, `None`, `book_value`.

- Overlapping screens: l8 screens 9 and 11 (`apply_trade`, `book_value`), homework-2 `h-net-value`. New: weights as a second dictionary, cash, the zero-total `None`, shorts.

Backlog: 1 bullet.
