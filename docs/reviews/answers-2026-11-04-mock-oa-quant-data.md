# Answer check, mock-oa-quant-data, 4 November 2026

**Summary.** 13 items checked (10 paper 1 including 2 parts of Q6, 3 code tasks with 26 hidden tests, 5 examples) plus the three CSVs, timing, pass rules and the check part. Wrong keys: 0. Other mismatches: 4 (one test gap that lets a wrong solution pass, one missing `byKey`, one reused concept and number, one wording note). Scripts: scratchpad `answers-mock-qd/` (`p1.py`, `data.py`, `variants.py`, `misc.py`). I read no generator script or author report. The three CSVs match the brief's SHA-256 prefixes (075ba1d7e21c18f1, 31b8bee8e889386e, 9a44408ce52afff1).

Process note: my first script ran the item-2 test setup in the live data folder and overwrote `qd-pair.csv` with the 6-row example. I restored it from `git show HEAD:` (read-only) and the hash and `git status` are clean again. All later runs used copies.

## Paper 1 (keys recomputed independently)

| Item | Key | My computation | Verdict |
|---|---|---|---|
| q1 | 3.92 (abs 0.005) | 1.96 x 12/6 = 3.92. Wrong 2.0 (SE) and 23.52 (no root n) match their `byKey` | ok |
| q2 | option a | No number. Lengths 74/74/72/68. Each distractor names a distinct misreading | ok |
| q3 | 1.8 | 1.8/(5/5) = 1.8; sqrt(25 x 3.24/25) = 1.8. Wrong 9.0 (divide by s/n) and 0.36 (divide by s) correct | ok, but no `byKey` (mismatch 2) |
| q4 | a, b, c | 5-point fit: residual sum 4e-16, line meets means. 2,000 seeded fits: R2 fell 0 times, adjusted R2 fell 1,326 times. d, e, f each unambiguously false | ok |
| q5 | 0.3467 (abs 0.0005) | 1 - 0.6 x 49/45 = 26/75 = 0.34667. n-k wrong: 1 - 0.6 x 49/46 = 0.3609 | ok |
| q6 part 1 | 5.6 | 4 + 0.6 x (2/3) x 4 = 5.6; matrix form 3.6/9 x 4 = 1.6 + 4. Wrong 4.0 and 6.4 (4 + 0.6 x 4) | ok |
| q6 part 2 | 1.6 | 2 x sqrt(0.64) = 1.6; sqrt(4 - 12.96/9) = 1.6. Wrong 2.0 and 1.2 (0.6 x 2) | ok |
| q7 | 0.142 stored, `unit: "%"` (abs 0.0005) | Variance 0.0144 + 0.0144 - 0.00864 = 0.02016, sqrt 0.141986. `accept` says 14.2% within 0.05 points: agrees. Wrong 0.24 (weighted vols) and 0.17 (sqrt 0.0288 = 0.1697, inside abs 0.001) | ok, fraction stored |
| q8 | 0.3448 (abs 0.0005) | (0.04 - 0.015)/(0.0625 + 0.04 - 0.03) = 10/29 = 0.34483. Grid of 1/290: minimum at 100/290. Inverse variance 16/41 = 0.3902, equal 0.5 | ok |
| q9 | a, b, c | No number. Keys avoid leakage, d, e, f each leak. Lengths 45/41/58 against 50/62/48: no key visibly longest | ok |
| q10 | 500 (abs 0) | 4 x (25 + 100) = 500; sum over n from 0 to 79 of the Poisson weights gives 500.0. Wrong 100, 400, 40 correct | ok |

No key band overlaps a wrong band in any numeric field. `shuffle: true` is set on q2, q4 and q9. `unit: "%"` appears only on q7. Every explanation number agrees with its key (q3, q5, q6, q7, q8, q10 re-read line by line). Every explain has at most three sentences.

## Paper 2 (CSVs and hidden tests)

CSV facts: prices 783 rows, 7 blank closes, 3 exact repeats (none share a key with a different close, none of the blank rows repeat), dates 2025-01-02 to 2025-12-31. Pair: 520 rows, date sorted, no repeated dates, exactly 3 rows above 0.25 (asset 0.31, -0.28, 0.35, all in `asset`), no value equal to 0.25, largest legitimate size 0.043. Signal: 800 rows, date sorted, no blanks.

My own solutions, written from the statement, give: d1 773 rows, 258/257/258, volatilities 0.1760834506309832, 0.25816881352482823, 0.3577200967909071 (and a pure-Python pass over the text: 0.17608345, 0.25816881, 0.35772010). d2 458 windows, first 0.80330, last 1.38288, sum 502.378645, full-sample beta 1.0877069411378. d3 coef at split 500 equal to the keyed values and oos R2 0.057702. All 26 hidden tests and all 5 examples pass for my solutions and for the reference, under pandas 3.0.5 with NumPy 2.5.3 and pandas 2.2.3 with NumPy 2.0.2 (Pyodide versions). All three starters fail every hidden test.

Wrong or alternative versions, hidden-test failures (identical under both pandas versions):

| Task | Version | Hidden tests failed |
|---|---|---|
| d1 | no repeat removal | 1, 4, 5, 8, 9, 10 |
| d1 | no blank removal | 1, 2, 5, 8, 9, 10 |
| d1 | `ddof=0`, sqrt 250, simple returns, one return dropped | 8, 9, 10 |
| d1 | return across tickers (stacked diff) | 9, 10 |
| d1 | no sort | 6, 8, 9, 10 |
| d1 | forward-fill blanks | 1, 5, 8, 9, 10 |
| d1 | **sort by date only** | **none: passes all 10** |
| d1 | dedupe on date and ticker | none (legitimate, repeats are exact) |
| d2 | no filter, or divide errors by 100 | 1, 4, 5, 6, 8, 9 |
| d2 | filter `asset` only | 9 (only the ninth test catches it) |
| d2 | one window fewer, extra partial window, shifted window | 1, 3, 4, 8, 9 / 1, 3, 4, 9 / 2, 3, 4, 8, 9 |
| d2 | threshold 0.3 (keeps -0.28) | 1, 4, 8, 9 |
| d2 | strict `<0.25`, threshold 0.2, `np.polyfit`, pandas `rolling().cov()/var()`, closed form, explicit date sort | none (all legitimate: same answer) |
| d2 | rows reordered by `asset` | 2, 3, 4, 5, 6 |
| d3 | unlagged features | 2 to 7 |
| d3 | test-mean baseline | 4, 6, 7 |
| d3 | fit on all rows | 2 to 7 |
| d3 | split off by one either way | 2 to 7 |
| d3 | train baseline 0 | 3 |
| d3 | oos baseline 0, full-sample mean, or squared correlation | 4, 6, 7 |
| d3 | coefficients in reverse order | 2, 5 |

Statement coverage: d2 and d3 fully specify every choice the tests depend on (threshold, drop the row, full windows, date order, lag direction, row range 1 to 799, intercept, baseline, key names and coefficient order). d1 specifies the sort order, but no test enforces it (mismatch 1).

## Timing, pass rules, check part

`pace` sums 2,280 s (40 minutes allows 38) for paper 1 and 4,500 s (75 of 80 minutes) for paper 2, as the brief. Papers are 40 and 80 minutes, 120 in all, 13 items; both have `pass: 0.6` (6 of 10, 2 of 3) and `scoring` right 1, wrong 0, blank 0. The `check` part `no-lookup` has the brief's name and detail. Skills, tags, difficulty ramp (2, 2, 3 x5, 4, 4, 5, then 3, 4, 5) and the `description` match the brief. `models` is 190 characters. Firm names appear only in `models`. Voice scan of all text: no exclamation marks, no em-dashes, no US spellings, no sentence of 20 words or more except `models` (29 words, the brief's own text, a single colon-separated line).

## Duplicates (DECISIONS "Duplicates", 6 Nov)

I scanned every numeric `answer` and `value` in `app/content/` (courses, exams, bank, drills) for the keys and wrong values, plus stem phrases. Matches of a bare number (3.92, 0.3467, 0.3609, 0.3448, 0.142, 5.6) in other files are coincidences in different contexts (series l12, random-vars l11 and so on). One real overlap, one weak overlap:

- `courses/research-int/l4-tests-in-words.json` item `q-p-reading` asks the same thing with the same figure: "A test gives $p = 0.03$. Which sentence is right?" (same tag `p-value-meaning`). The mock's q2 reuses the number and the idea.
- `courses/eigen/l15-matrix-square-root.json` uses vols 20% and 30% and a 60/40 split (correlation 0.5, other answers). `courses/vectors/homework-3.json` uses 20% and 30% with correlation 0.5. Q7 differs in correlation and answer. Low risk.

The data files and function names (`qd-`, `windowed_betas`, `oos_scores`, `tidy_closes`, `vol_by_ticker`) appear nowhere else.

## Mismatches

1. `d1-return-table`, `widget.tests` (and statement): the statement says to sort by ticker, then date, but a version that sorts by `date` only passes all 10 hidden tests (test 6 checks order within each ticker only). It fails visible example 1 only. Fix: add a test such as `tidy_closes().iloc[258].tolist()` expecting `['2025-01-02', 'LAMBDA', 122.15]` (or `list(tidy_closes()['ticker'].unique())` equal to `['KAPPA', 'LAMBDA', 'MU']` plus `tidy_closes()['ticker'].is_monotonic_increasing` equal to `True`), and raise the `how` count to 11 and the feedback text from "ten" to "eleven". Row 0 is `['2025-01-02', 'KAPPA', 50.56]`, row 257 `['2025-12-31', 'KAPPA', 58.62]`, last row `['2025-12-31', 'MU', 11.25]`.
2. `q3-t-statistic`, `feedback.byKey`: missing. The brief asks for a one-clause `byKey` line for each `wrong` id. Add `wrong-se`: "You divided by $s/n$, not $s/\sqrt n$. The standard error is 1, not 0.2." and `s-only`: "You divided by $s$ alone. The mean's own spread is $s/\sqrt n$." Also q2, q4 and q9 correctly have none (no `wrong` ids).
3. `q2-p-value-meaning` (statement and option b, c): reuses the idea and number of `research-int/l4-tests-in-words` `q-p-reading` ($p = 0.03$). Fix: change the figure (for example $p = 0.04$, with options 4% and 96%, and the key "about 4% of the time") and the matching `explain`, feedback and `why` lines.
4. Note only, `models`: one sentence of 29 words, taken verbatim from the brief. Split it at the colon if the voice rule is applied strictly.

## Fix pass

1. Fixed. `d1-return-table` `widget.tests` gains test 11: `[tidy_closes()['ticker'].iloc[258], float(tidy_closes()['close'].iloc[258])]` expecting `['LAMBDA', 122.15]`. The reference gives row 258 = 2025-01-02 LAMBDA 122.15 (first LAMBDA row). A date-only sort gives KAPPA 44.21 there, so it now fails. The starter returns `None` and fails. Count is 11 of 15. `how` now says 11 hidden tests, `feedback.correct` says "All eleven". Playthrough scores 13 of 13. The check ran on pandas 3.0.5, not 2.2.3: it uses only `sort_values`, `iloc` and `float`, which behave the same in 2.2.3.
2. Fixed. `q3-t-statistic` `feedback.byKey` added. `wrong-se` (9.0 = 1.8/(5/25) = 1.8/0.2): "You divided by $s/n$, not $s/\sqrt n$. The standard error is 1, not 0.2." `s-only` (0.36 = 1.8/5): "You divided by $s$ alone. The mean's own spread is $s/\sqrt n$." Both values recomputed twice, by hand and in Python.
3. Fixed. `q2-p-value-meaning` now uses $p = 0.018$ for a trading rule's average daily profit, options 1.8% and 98.2% (100 - 1.8 = 98.2; 1 - 0.018 = 0.982). Changed: `question`, all four option texts, `explain.text`. `feedback` and `why` lines are generic and unchanged. A grep of `app/content/` finds no other 0.018, 98.2% or 1.8% p-value item. Brief table row updated.
4. Fixed. `models` split into two sentences (19 words and 8 words). Changed in the exam JSON, `docs/briefs/mocks.md` and `oa_quant_data_build.py`, which also carries the other edits (it generates the exam). CSVs untouched.

Validator: 0 errors. Playthrough `--exam mock-oa-quant-data`, with and without `--mobile`: all passed.
