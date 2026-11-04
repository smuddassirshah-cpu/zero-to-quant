# Answer check, research-int level 4 (4 November 2026)

**Summary.** 95 items checked (l16 16, l17 15, l18 16, l19 16, l20 14, review-4 10, homework-4 8) plus 6 `rq-*` drills (51 hidden tests). Wrong keys: 0. Every numeric, choice, order, multi, tap and table key recomputed independently and agrees. Mismatches: 2 `wrong` values or claims that do not match feedback or prose, 3 number or wording slips, 9 code or drill tests that let a wrong solution pass, 4 duplicates, 4 minor voice or balance notes.

Scripts are in `/tmp/claude-0/-home-user-zero-to-quant/024bfe09-7a97-56c3-837c-b47a15727adf/scratchpad/answers-research-4/`: `runw.py` (runs a code widget or drill as the engine does: setup, isclose with 1e-9 default, equal, data files copied into the working folder), `mut.py` (mutated solutions), `cpprun.py` (C++ drills, clang++ -O1 -fno-exceptions), `dump.py`, `voice.py`, `dups.py`.

**Versions.** I ran pandas 2.2.3, NumPy 2.2.6, scikit-learn 1.6.1 (installed in `pkgs223`). Pyodide 0.27.7 ships an older NumPy (2.0.x). Nothing here depends on it except the seeded bootstrap in l20: `default_rng(seed).integers` is a stable stream across 2.x, and the 0.0 float64 results in l18 and `r4-naive-variance` are plain IEEE arithmetic, so no difference is expected. No sklearn call appears in level 4.

## Per item

### l16 Interpolating

| Item | Key | My computation | Verdict |
|---|---|---|---|
| Two gaps | 104 (wrong 106, 100) | 12/3 = 4; two steps gives 6 so 106; carry 100 | ok |
| Formula | 125 (25, 102.5) | 100 + 0.25 x 100; rise only 25; 100 + 2.5 | ok |
| Unsorted | 27.5 (25) | sorted (2,25),(3,30); listed (3,30),(1,10) line gives 25 | ok |
| Beyond ends | 30 (40) | hold 30; extending the (2,25)-(3,30) slope 5 gives 40 | ok |
| Same x twice | 22.5 (25, 20) | mean 15, halfway to 30; last pair gives 25, first pair 20 | ok |
| Uneven times | 103 (106) | 100 + 12/4; by position 106 | ok |
| pandas trap | "by position" | `Series.interpolate()` gives [100, 106, 112]; `method="index"` gives 103; `nearest` gives 100 | ok |
| Empty, derive (order), say-aloud, follow-up | keys | reasoned; order a,b,c,d, x gives 350 at 2.5 as stated | ok |
| Transfer (code, 8 tests) | 286 rows etc. | 312 rows, 15 blank, 297, 11 merged pairs, 286; five interior values recomputed by pure-Python bisection and `np.interp`, all agree | ok, see M7a |
| q16-two-points 20, q16-one-point 42, q16-by-time 16, q16-method | | 10 + 40/4; held; 10 + 0.75 x 8; by position 14 | ok |

### l17 Regression by group

| Item | Key | My computation | Verdict |
|---|---|---|---|
| Reed slope | 0.9 (1.0) | centred products 4.5, Sxx 5; Marsh -0.6, Plain 0 as stated; ends (13-10)/3 = 1 | ok |
| `slope_by_town` (6 tests) | | all 12 slopes recomputed by cov/var; Wick NaN; Ayr -0.0410086, Leith 0.0997918 | ok |
| Negative slopes | 4 (3, 8) | Ayr, Bath, Cork, Deal (-0.000499) | ok |
| SE of a slope | 0.0052 (0.15, 0.015) | Sxx = 83,325 for days 1 to 100 (checked in the data); 1.5/288.66 = 0.005197 | ok |
| Table values | | all 12 slopes to 4 places match; R-squared Deal 0.0001 (8.9e-5), Leith 0.8023 | ok |
| Within two SE of zero | Deal, Elgin | 2 x 0.0104 = 0.0208; Elgin 0.0088 inside, Cork 0.0128 outside | ok |
| Wick trap | | 9.4 - 9.1 = 0.3, 3 x Leith 0.0998 = 0.299 | ok |
| Order (SE derivation) | a,b,c,d | 100 x 9999/12 = 83,325; 1.5/sqrt = 0.0052 | ok |
| Beta | 1.3 (0.7692) | 0.000234/0.000180 | ok |
| q17-hand 0.6 (0.3333), q17-se 0.0104 (0.0052), q17-two-rows 1 | | centred products 3 over 5; 3/288.66 = 0.010393; two points fit exactly | ok |

### l18 Updating a fit

| Item | Key | My computation | Verdict |
|---|---|---|---|
| Running sums (table) | 4, 10, 14, 30, 39 | 2+6+15+16 = 39 | ok |
| Slope from sums | 0.8 (1.3) | (156-140)/(120-100); 39/30 = 1.3; intercept 1.5 | ok |
| Add (5,8) | 1.3 (0.8, 1.6) | sums 5,15,22,55,79: 65/50; intercept 0.5; 8/5 = 1.6 | ok |
| Remove (1,2) | 1.4 (1.3) | sums 4,14,20,54,77: 28/20; intercept 0.1 | ok |
| Sherman-Morrison | 2.5 (1.5, 27) | P = inverse of [[4,10],[10,30]]; Px = (-1, 0.5); x'Px = 1.5; beta moves to (0.5, 1.3) | ok |
| `OnlineLine` (7 tests) | | 200-row polyfit comparison, add, remove | ok, see M7b |
| Float trap | 0 (1) | float64 gives exactly 0.0 for 1e9+1..3; true variance 1 | ok |
| Order (centring) | a,b,c,d | m = 0.5, a' = 1, a = 1 - 0.5e9 = -499,999,999 | ok |
| Rolling beta | 1.24 (1.2419) | sums 250, 25, 37, 585, 726: 180,575/145,625 = 1.24 exactly; add only: 182,950/147,310 = 1.24194 | ok |
| q18-sums 0.5 (1.3571), q18-add 1.7, q18-cost 10000 (5, 2000) | | 3/6; sums 4,10,17,30,51: 34/20; n | ok, see M2 and M11 |

### l19 Timed data task

| Item | Key | My computation | Verdict |
|---|---|---|---|
| Spot five problems | l3, l4, l6, l8, l9 | ids are `l<line number>` with the header as l1 (checked in `console.js`); 397 comma, 322 lower case, 205 -999, 519 blank, second 547 | ok, see M6 |
| drop_duplicates miss | 3 (15, 12) | 15 repeated ids, 12 exact duplicate rows | ok |
| `load_clean` (6 tests) | 570; 230, 206, 134; 1,203,200 | 600, 585, 570; recomputed in plain `csv` | ok, see M7c |
| `vwap_by_symbol` (4 tests) | 50.01524, 120.01457, 8.00046 | recomputed; leaving -999 and repeats gives ALPHA 46.3874 as stated | ok |
| `slippage_model` (4 tests) | 1.242071, 0.337457, 0.534599, 3.795232 | statsmodels OLS; SE 0.04863 as stated; 5-row frame values match | ok |
| 3,200-share cost | 4.642 (40.08, 10.362) | 0.337457 + 1.242071 ln 32 = 4.6421 | ok, see M5 |
| Zero price, order (sign), say-aloud | keys | seller at 49.80 vs mid 50 gives +40 bp | ok |
| Fills VWAP | 31.225 (31.2727, 31.1333) | 124,900/4,000; with repeat 172,000/5,500; overstatement 4.8p | ok |
| Follow-up (multi) | symbol, time, side | cubic terms and dropping large orders are tuning | ok |
| q19-count | 863 | 900-25-12 | key ok; wrong values M1 |
| q19-vwap 10.3 (10.2), q19-dedupe, q19-sign 40 (-40) | | 8,240/800; mean 10.2; (49.80-50)/50 x -1 x 1e4 | ok |

### l20 Writing a take-home

| Item | Key | My computation | Verdict |
|---|---|---|---|
| Order the report | sum, data, meth, res, lim, rerun | | ok |
| `make_report` (8 tests) | 396; 307.2202; 82.89977; seed 0 [77.45197, 88.22498]; seed 1 [77.78532, 88.40591] | 400 rows, 4 above 5000, n = 396; population RMSE; bootstrap with `default_rng`, `integers(0, n, (2000, n))`, percentile 2.5 and 97.5, all match to 1e-9 | ok |
| Reruns that match | again, loop, later | loop form with the same seed gives an array equal to the vectorised draws | ok |
| Interval width | 10.77 (5.39, 2.76) | 88.22497 - 77.45197 = 10.773; draw SD 2.7619; the 2,000 histogram values equal my draws to 1e-3 | ok |
| Checklist (multi), trap, row order, say-aloud, follow-up | keys | sorting by price gives [77.299, 88.295], not [77.452, 88.225] | ok |
| Orders report interval | 1.1468 (1.1935, 1.3374) | 1.2421 - 1.96 x 0.0486 = 1.14684; upper 1.33736 | ok |
| q20-width 11.6 (5.8), q20-tail 50 (25, 100), q20-seed, q20-path | | 52.8 - 41.2; 2.5% of 2,000 | ok |

The l20 interval is computed correctly, with the stated generator and 1e-6 tolerance.

### review-4

| Item | Key | My computation | Verdict |
|---|---|---|---|
| r4-interp-sorted | 38 (42.5) | sorted (3,26),(5,50): 26 + 12; listed (5,50),(1,20) gives 42.5 | ok |
| r4-interp-time | 53 (56) | 50 + 12 x 2/8; by position 56 | ok |
| r4-slope-evidence | 3 (2, 6) | ratios 5.96, -0.77, 0.30, -4.23, 2.16, 1.63: P, S, T pass 2; SEs 0.0052, 0.6708 (4 days), 0.0416 (25 days) check | key ok, see M4 |
| r4-beta-per-stock | ok option | `np.cov` and `.var()` both use n-1; np.var gives n/(n-1) times beta; `rets` instead of `g` pools; loop overwrites | ok |
| r4-add-row | 0.9 (1.1) | sums 5,15,18,55,63: 45/50; before 22/20 = 1.1 | ok |
| r4-remove-row | 1.0 (0.9) | sums 4,14,16,54,61: 20/20 | ok |
| r4-naive-variance | 2.6667 (1.6667, 0) | float64 gives 2.6666666666666665; true 5/3 | ok |
| r4-rows-left | 749 (744, 780) | 780 after repeats; 36-5 = 31 bad prices remain; 800-20-36 = 744 | ok |
| r4-predict-slip | 3.2072 (11.2, 9.424) | 0.4 + 1.35 x 2.07944; 0.4 + 1.35 x 8; 0.4 + 1.35 x 6.68461 | ok |
| r4-rerun-checklist | four correct | | ok, see M8 |

### homework-4

| Item | Key | My computation | Verdict |
|---|---|---|---|
| `value_at` (7 tests) | 100.28438, 101.34113, 101.65240; tiny file 7.5, [6.0, 8.25] | pure-Python recomputation; first quote at second 7, last 23258 | ok |
| `town_slopes` (6 tests) | Bath, Hove, Ince intercept 12.23814, Kelso and Cork R-squared | recomputed by hand-rolled sums | ok, see M7d |
| `OnlineOLS` (6 tests) | [2.0, 2.1], [1.4, 2.4], [1.542857, 2.371429] | closed forms; 20,000-row test runs in 0.18 s here; a refit on every row takes about 1 s per 3,000 rows and fails the budget | ok |
| Long form | 4.02, 0.71 to 1.19, 851 | 900-49; 0.95 +/- 0.2352; 0.30 + 0.95 ln 50 = 4.0166; model text is 115 words | ok |
| VWAP table | 1000, 20.16; 800, 55.2125 | 20,160/1,000; 44,170/800 | ok |
| `clean_orders` (6 tests) | 271 buys, median 2300, 78,732,175.8 | recomputed with `csv`; TINY leaves 3 rows, qty 1,900 | ok, see M7e |
| Normal equations (order) | a,b,c,d | n x eq2 - Sx x eq1 | ok |
| SE of 50 days | 0.0196 (0.2828, 0.04) | 50 x 2499/12 = 10,412.5; 2/102.04 | ok |

### Drills

| Drill | Result | Verdict |
|---|---|---|
| `rq-interp-py` (13 tests) | solution passes, starter fails 13 | ok, see M7f |
| `rq-clean-frame-py` (7) | starter fails 6 (the unchanged-input test passes on the starter) | ok, see M7g |
| `rq-group-slopes-py` (8) | slopes 0.8, 1.6, [1.5, -1.0], cycle 1, 2, 3 recomputed | ok, see M7h |
| `rq-online-ols-py` (7) | l18 sequence and seeded rows pass | ok, see M7i |
| `rq-interp-cpp` (9) | clang++ -O1: all pass; sorting, averaging and end-holding mutants fail | ok |
| `rq-stable-slope-cpp` (7) | all pass; raw sums at 1e9 give num 3, den 0, so inf, as the brief says; at 1e8 raw sums give 0.5 (wrong, not inf) | ok |

Starters fail their tests in every case except where noted (a starter may pass the one test that checks nothing changed).

## Mismatches

### Wrong or contradicting `wrong` values, prose and hints

1. `courses/research-int/l19-timed-data-task.json`, quiz `q19-count`: the two wrong values are swapped against their feedback. `noprice` has value 888 (900-12) but says "You removed the repeats only" (that is 875). `norepeat` has value 875 but says "You removed the blank prices only" (that is 888). Fix: set `noprice` to 875 and `norepeat` to 888, or swap the two feedback lines.
2. `courses/research-int/l18-updating-a-fit.json`, quiz `q18-sums`: prose says "Five points have sums n = 3". Fix: "Three points".
3. `courses/research-int/l18-updating-a-fit.json`, screen "Sums of squares are exact" (index 6), hint 3: "far below the rounding step of 128". The spacing of float64 near 3e18 is 512 (and 1024 for (sum x)^2). Fix: "512".
4. `courses/research-int/review-4.json`, `r4-slope-evidence` explain: ratios "5.97" and "1.64" do not follow from the table (0.031/0.0052 = 5.96, 0.0085/0.0052 = 1.63; they use the unrounded SE 0.005197). Fix: write 5.96 and 1.63, or show the SE as 0.00520.

### Number and wording slips

5. `l19-timed-data-task.json`, screen "What a big order costs" hint 2 and explain: "1.2421 x 3.466 + 0.3375 = 4.642" is 4.6427 with 3.466. Fix: use $\ln 32 = 3.4657$, or write "about 4.642".
6. `l19-timed-data-task.json`, first screen: prose "nine of the 600 rows", but the canvas holds a header and eight data rows (the title also says "nine rows"). Fix: "eight of the 600 rows" and "a header and eight rows".
7. Code tests that let a wrong solution pass (all other mutants I tried fail as they should):
   - a. `l16-interpolating.json` transfer: `.first()`, `.last()` or `.max()` in place of `.mean()` for repeated seconds pass all 8 tests (no queried second lies in a merged segment and the length test does not see values). Fix: add a test on a repeated second, such as `clean_ticks(...)` price at 17718 = 101.7725 or `price_at(c, 17718)`, and one between 6477 and 9682.
   - b. `l18-updating-a-fit.json` `OnlineLine`: returning NaN for two rows (`n < 3`) passes, though the docstring says fewer than 2. Fix: add a two-row case, `m.add(1, 2); m.add(3, 8)` expecting `[-1.0, 3.0]`.
   - c. `l19-timed-data-task.json` `load_clean`: `price >= 0` passes; the file has no zero price although the lesson teaches `> 0`. Fix: add the TINY-style frame with a zero price (as `h4-clean-orders` has).
   - d. `homework-4.json` `town_slopes`: a guard of `n <= 3` passes (no three-row group). Fix: add the small frame used in l17, or a three-row town.
   - e. `homework-4.json` `clean_orders`, `l19` `load_clean` and drill `rq-clean-frame-py`: `drop_duplicates('order_id', keep='last')` passes, because repeats are identical after cleaning, although the statement says "the first". Fix: add a case whose repeats differ in price, or drop "(the first)" from the statements.
   - f. `drills/rq-interp-py.json`: the spec says no points raises `ValueError` and no test checks it (removing the check passes 13 of 13). A linear-scan solution passes the "Long input" test in 0.05 s, so "bisect rather than scan" is not enforced. Fix: add an empty-input `raises` case; reword the `why` or add several thousand queries.
   - g. `drills/rq-group-slopes-py.json`: `groupby('g', sort=False)` passes; "in sorted order" is untested because every test frame lists groups in sorted order. Fix: add a frame with groups `b` before `a`.
   - h. `drills/rq-online-ols-py.json`: a class that stores rows and refits with `lstsq` in `coef()` passes all 7 (the tests call `coef()` once at the end), against "Never refit from stored rows". Fix: call `coef()` after every add in the 5,000-row test, as the homework does.
   - i. See e for `rq-clean-frame-py`.

### Duplicates (DECISIONS "Fresh numbers in reviews and homework" and "Duplicates")

8. `homework-4.json` items `h4-value-at`, `h4-town-slopes`, `h4-clean-orders` use the same data file and the same task as the code screens of l16, l17 and l19 (stage 1), with the same outcomes: 286 clean times, 13 towns and Wick NaN, and the 570-row clean frame. `h4-town-slopes` tests Bath and Hove (the l17 test already checks all twelve slopes to three places). Fix: give each a variant with fresh data (a new file or a different question: for example slope of temperature on day for only the second half, `value_at` for a vector of times, a different cleaning rule), and change the explain lines that repeat "286".
   Smaller overlaps in `review-4.json`: `r4-rerun-checklist` repeats the l20 checklist (seed, relative paths, versions, one command, with the same two traps); `r4-add-row` and `r4-remove-row` use l18's x grid 1 to 5 and the same leaving point (1, 2), with new y values; `r4-slope-evidence` reuses the 0.0052 SE of l17. Fix: change the checklist items (for example data version, run order, a hash of the input), and use a different leaving point such as (2, 3).
   No item shares numbers with any other course, exam, bank file, mock or `oa` drill (checked by a number-set scan of all of `app/content/` plus greps of every key and distinctive value). The drills repeat lesson numbers on purpose (`rq-interp-py` examples are l16's, `rq-online-ols-py` runs l18's sequence); they are practice, not reviews, so I have not counted them.

### Voice and balance (low)

9. `drills/rq-clean-frame-py.json` `brief`: a 22-word sentence ("symbols stripped and in upper case, ..."). `drills/rq-stable-slope-cpp.json` `brief`: a 23-word sentence ("The formula from raw sums ... never 0.5"). Fix: split each.
10. Choice keys that are the longest option, by a few characters: `l19` `q19-dedupe` (57 against 54, 33, 31) and `l18` "Say it aloud" (71 against 66). Not visibly longer. In `l20` "Which reruns match" the correct options are 41, 57 and 33 characters against 16 and 18 for the two wrong ones, so the short ones read as wrong. Fix: lengthen the two wrong options.
11. `l18-updating-a-fit.json` `q18-cost` wrong `p` (5): the feedback "You divided once too often" does not describe a route to 5 (it is $np^2/(np)$). Fix: "You divided by n as well as by $p^2$..." or drop the wrong value.
12. `l16-interpolating.json` transfer explain: "does the sort-free bracket search for you but needs sorted times" reads as a contradiction. Fix: "searches for the bracket for you but needs the times in increasing order".

`unit: "%"`: none used in these files. Em-dashes and exclamation marks: none. British English: no American spellings found. Explanations: none over three sentences.
