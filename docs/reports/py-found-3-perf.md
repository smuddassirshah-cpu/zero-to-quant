# py-found level 3: performance task

- `homework-3.json` item 9 of 9, `h-cash-account`, appended. Kind `code`, difficulty 5.
- Matched objective (l12): "Write a small class with an initialiser and methods."
- Product: `Account` with `deposit`, `withdraw`, `balance` and `history`, exact to the penny, refusing with `ValueError` and changing nothing.
- Tests: 10 hidden, 1 example, exact `==` or raises. Sixteen planted slips fail, among them float pounds, `int` truncation, `>=` on the whole balance, change then check, a class-body list.

Gates (exact commands; `<pkgs>` is the scratchpad folder):
1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, plus the expected perf-pending warning.
2. Voice, `VOICE_BASE=app/content/courses/py-found python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `python3 -I docs/reports/py-found-3-perf-numbers.py`: exit 0.
4. Playthrough, `node tools/playthrough.mjs --set py-found/homework-3 --local-cdn <pkgs>`, with and without `--mobile`, regenerated manifest: All passed, starter fails; shots clean.

Freshness: `fresh-check.mjs --file` no hit. Grep: account, deposit, withdraw, balance, pence.

- Overlapping screens: l12 screens 3, 7 and 9, l11 screen 6, l1 screens 7 and 8, review-3 `r-buy`, homework-3 `h-book-dates`. New: pence inside an object, check before change, the whole-balance edge, negative withdrawals.

Backlog: 0 bullets.
