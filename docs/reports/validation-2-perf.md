# validation level 2: performance task

- `homework-2.json` item 9 of 9, `h-label-purge`, appended. Kind `code`, difficulty 5.
- Objective (l7): "Build a forward label with the right alignment". Product: `label_table(px, h)` on dates by shares with halts, and `train_dates(px, h, test_start, test_end)`, the purge.
- 12 tests, 1 example. 17 planted bugs fail, each first where its byKey fits: wrong-way shift, horizon off by one (test 1); h closes not h rows, back-fill, `pct_change` padding (test 3); purge by h or h - 2, one side, none (test 7); unlabelled dates (test 10).
- Overlap: l7 screens 4 (`forward_label`), 5 (`purged_train_idx`), 9; `h-pks`, `h-count`, `r-purge`. New: missing closes give NaN, purge by dates with an inclusive end, unlabelled dates dropped.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/validation python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python docs/reports/validation-2-perf-numbers.py`: exit 0; a pure-Python loop agrees; starter fails 12 of 12.
4. `node tools/playthrough.mjs --set validation/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed; shots clean.

Freshness: `fresh-check.mjs --file` 0 hits; grep label_table, train_dates, desk(, tape(, not yet listed, both included: item only.

Backlog: 1 bullet.
