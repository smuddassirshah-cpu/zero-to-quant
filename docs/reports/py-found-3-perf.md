# py-found level 3: performance task

- `homework-3.json` item 9 of 9, `h-cash-account`, appended (cap 12, nothing converted). Kind `code`, difficulty 5, pace 1200 s, skill `pf-classes`.
- Matched objective (l12): "Write a small class with an initialiser and methods." The only verb-rule objective in the level.
- Product: `Account` from a one-line stub: `__init__(self, opening=0.0)`, `deposit`, `withdraw`, `balance`, `history`, exact to the penny, refusing with `ValueError` and changing nothing. A hidden prelude defines `refused(move, amount)`.
- Tests: 10 hidden, 1 example, all exact `==` or raises. Starter fails 10 of 10. Sixteen planted slips each fail: pounds as floats (test 2), `int` truncation (3), `>=` refuses the whole balance (4), no overdraft check (5), change then check (6), `< 0` lets 0 in (7), no deposit check, no check on a negative withdrawal (9), `return False`, `raise Exception`, list in the class body (10), history in pence, opening as a move, balance in pence, print not return, opening ignored. Pounds rounded to 2 places each move passes: exact by another route.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; the expected "py-found/L3: has a performance task, remove from perf-pending" warning.
2. `VOICE_BASE=app/content/courses/py-found python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script `python3 -I docs/reports/py-found-3-perf-numbers.py`: exit 0, 0 failures. Route A the solution, route B Fractions of a pound, route C integer pence.
4. Playthrough `node tools/playthrough.mjs --set py-found/homework-3 --local-cdn <pkgs>`, with and without `--mobile`, regenerated manifest: All passed, performance starter fails. Shots read cleanly.

Freshness: `fresh-check.mjs --file` no hit on item 9. Grep: account, deposit, withdraw, balance, pence, `round(`, `ValueError`.

- Overlapping screens: l12 screens 3 and 9 (`Position`, `Trade` and `Book`, a list per instance), l12 screen 7 (the class-body list), l11 screen 6 (`parse_qty` raises), l1 screens 7 and 8 (float deposits, `total_pence`), review-3 `r-buy`, homework-3 `h-book-dates`. New: pence kept inside an object, check-before-change, the whole-balance edge, negative withdrawals.

Backlog: 0 bullets.
