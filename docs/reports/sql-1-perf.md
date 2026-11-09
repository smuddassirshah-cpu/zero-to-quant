# sql level 1: performance task

- `homework-1.json` item 9 of 9, `h-cash-bonds`, appended (cap 12, nothing converted). Kind `code`, difficulty 5.
- Matched objective (l3-top-ten): "Write clauses in their fixed order, and spot ties at the cut."
- Product: `query()` from a stub on a new `bonds` table,, through `sqlite3` as every sql code item runs. The four AAA or AA bonds maturing soonest, perpetuals out, date ties broken by yield, highest first.
- 6 tests, 1 example. 16 planted bugs fail: missing rating test, `<> NULL`, no `IS NOT NULL`, bracketless `OR`, wrong directions, no tie-break (either stored order), `LIMIT 3` and `5`.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/sql python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 docs/reports/sql-1-perf-numbers.py`: numbers script exits 0.
4. `node tools/playthrough.mjs --set sql/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed; starter fails; no item too wide.

Freshness: `fresh-check.mjs --file` 0 hits; bonds, rating, maturity, yield, perpetual, AAA appear nowhere else.

Overlapping screens: l3-top-ten screens 3, 6 and 9, review-1 `r-two-keys`, l4 screen 8, `h-quiet-days`, l2 screen 5. New: the table, a tie straddling the cut, a mixed-direction tie-break, brackets beside a `NULL` test.

Backlog: 0 bullets.
