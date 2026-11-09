# py-found level 4: performance task

- `homework-4.json` item 9 of 9, `h4-sweep-offers`, appended. Kind `code`.
- Matched objective (l13): "Write a generator and use it in a loop".
- Product: generator `sweep_offers(qty, offers)` (cheapest first, ties in book order, `ValueError`) and `average_price` looping over it.
- Tests: 15 hidden, 2 examples. 22 planted slips fail: no `key`, `.sort()` on the caller's book (6), `len` on a generator (5), fills read twice (10), empty book divides by zero (11), `assert` (8, 9, 14), a list returned (7).

Gates:
1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, expected perf-pending warning.
2. Voice, `VOICE_BASE=app/content/courses/py-found python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `python3 -I docs/reports/py-found-4-perf-numbers.py`: exit 0.
4. Playthrough, `node tools/playthrough.mjs --set py-found/homework-4 --local-cdn <pkgs>`, with and without `--mobile`, regenerated manifest: All passed; shots clean.

Freshness: `fresh-check.mjs --file` no hit on the item. Grep: offer, fill, `yield`, `next(`, `sorted(`, `.sort(`, `raise ValueError`, `average_price`.

- Overlapping screens: l13 screens 4 to 7, l14 screens 4 and 7, l8 screens 5 to 7, l11 screens 5 and 6, l15 screens 2 to 4, `h4-reuse`, `r4-resume`. New: an order book, stable ties, partial fills, any iterable.

Backlog: 0 bullets.
