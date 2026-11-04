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

## Fix pass

Fix pass of 4 November 2026 (worktree branch `worktree-agent-a8bfbfc44066489c6`). Targeted edits only; no lesson id, `course.json` or item id changed. Every changed number was computed twice (method A and B named per entry). Checks: pandas 2.2.3 and NumPy 2.2.6 from `pkgs223` through `runw.py` (with `__learner_source__` defined and the data files copied from the worktree), then the real playthrough in Pyodide 0.27.7 with `--local-cdn`.

**Counts.** Fixed 12 of 12 numbered findings (1 to 12, with 7a to 7i and the two overlap notes of 8). Disputed 0. Deferred 1 part: the "bisect rather than scan" constraint of `rq-interp-py` cannot be tested (see 7f). Graded answers changed: 6 (`q19-count` two wrong values; `r4-slope-evidence` 3 to 4; `r4-add-row` 0.9 to 2.1; `r4-remove-row` 1.0 to 2.0; homework items 0, 1 and 5 replaced by new tasks with new answers).

### Contradictions and slips (1 to 6)

1. `q19-count` (l19): `noprice` value 888 to 875 (900 - 25 = 875, method A: repeats removed only, matches "You removed the repeats only"; method B: 900 - 12 = 888 is the other). `norepeat` value 875 to 888 (900 - 12 = 888, matches "You removed the blank prices only"). Feedback text unchanged.
2. `q18-sums` (l18) prose: "Five points have sums $n = 3$" to "Three points have sums $n = 3$".
3. l18 screen "Sums of squares are exact", hint 3: "rounding step of 128" to "rounding step of 512" (float64 spacing just above $2^{61}$ is $2^{61-52} = 512$; method B: `np.spacing(3e18)` = 512).
4. `r4-slope-evidence` explain: "5.97 ... 1.64" to "5.96 ... 1.63" in the old table. The item has since been replaced (see 8), so the final explain reads "The ratios are 2.7, -0.5, 1.7, -2.3, 2.3 and 2.1", each rounded to one place so that the displayed and unrounded standard errors give the same figure.
5. l19 screen "What a big order costs": $\ln 32 = 3.466$ to $3.4657$ in hint 2, hint 3 and explain. $0.3375 + 1.2421 \times 3.4657 = 4.6422$ (method A, by hand: 3.4657 x 0.2421 = 0.83905, so 4.30475 + 0.3375); method B with the unrounded fit, $0.337457 + 1.242071 \ln 32 = 4.64215$. Both give 4.642.
6. l19 first screen: "nine of the 600 rows" to "eight of the 600 rows"; canvas title "orders-messy.csv, nine rows" to "orders-messy.csv, a header and eight rows" (the console holds 9 lines: 1 header and 8 data rows).

### Weak tests (7)

Old and new tests; the "mutants" are the wrong solutions the checker listed, run through `runw.py` (14 to 15 tests each, solution passes, starter fails).

- 7a `l16` transfer (8 to 11 tests, how text updated). Added: `[price_at(c, t) for t in (2648, 6477, 17718, 22418)]` expect `[100.202, 100.238, 101.7725, 101.474]`; the same list from `price_at_np`; `price_at(c, 15650)` expect `101.39480952380953`. All rel 1e-9. Values: method A pure-Python bisection on the merged series (means of [100.189, 100.215], [100.239, 100.237], [101.778, 101.767], [101.485, 101.463]; 15650 lies 31/63 of the way from 101.383 to 101.407); method B `np.interp` on the pandas frame. Both agree. Mutants now failing: `.first()`, `.last()`, `.max()`, `.min()` (8 of 11 pass, 3 fail). `.median()` equals the mean for pairs, so it is not a wrong solution.
- 7b `OnlineLine` (l18, 7 to 8 tests). Added `m.add(1, 2); m.add(3, 8)` expect `[-1.0, 3.0]` (slope 6/2 = 3, intercept 2 - 3 = -1; method B `np.polyfit([1, 3], [2, 8], 1)`). Mutant `n < 3` now fails.
- 7c and 7e `load_clean` (l19, 6 to 8 tests). Added a prelude that writes `tiny-orders.csv` (7 rows: a price of 0.0, a NaN, a -999, id 2 twice with prices 5.0 then 6.0, symbols ' x ' and 'y', quantities '1,000' and '4,500') and two tests: `[len, order_id list, price list]` = `[3, [1, 2, 6], [10.0, 5.0, 12.0]]`, and `[symbols, qty]` = `[['X', 'Y', 'X'], [1000, 200, 700]]`. Mutants now failing: `price >= 0` (6 of 8 pass) and `keep='last'` (6 of 8 pass).
- 7d and 7e homework `town_slopes` and `clean_orders`: replaced by new items (see 8), whose tests carry the guard and repeat cases. `trend_table`: a five-row lake is fitted and a four-row lake is not, so `n <= 5` and `n < 3` fail (see the table below). `clean_fills`: a repeated id whose copies differ (`keep='first'` fails).
- 7e `rq-clean-frame-py` (7 to 8 tests): added "Repeats that differ", ids [1, 1, 2] with prices [5.0, 9.0, 4.0], expect `[5.0, 4.0]`. Mutant `keep='last'` now fails; `price >= 0` already failed on "A price of zero".
- 7f `rq-interp-py` (13 to 14 tests, prelude added): "Every y missing", `_raises_value_error([1, 2], [None, float('nan')], 1)` expect True (the drill harness has no `raises` compare, so a prelude helper catches `ValueError`). Mutant without the check now fails. Deferred: a linear-scan solution still passes. Every call rebuilds and sorts a dict, so a scan cannot be told from bisection by timing, and the drill harness cannot read the source. The first constraint now says "The tests check results and speed, not the method", and the "Long input" `why` no longer claims to test bisection.
- 7g `rq-group-slopes-py` (8 to 9 tests): "Groups listed out of order", groups b, b, b, a, a, a with y [1, 2, 4, 4, 3, 2], expect `[['a', 'b'], [-1.0, 1.5]]` (b: centred products 3 over 2 = 1.5; a: -2 over 2 = -1; method B `np.polyfit`). Mutant `groupby('g', sort=False)` now fails.
- 7h `rq-online-ols-py` (7 to 8 tests, prelude helper `_run_calls`): "Coefficients after every row", 20,000 seeded rows with `coef()` called after each add, maximum error against `lstsq` at every 1,000th row below 1e-6. The model solution takes 0.19 s here; a class that stores rows and refits in `coef()` took 43.5 s (limit 5 s per test, so the engine stops it). It is stopped by the engine's limit, not by `runw.py`, which has no clock.

### Duplicates (8): fresh numbers, data and tasks

New data from the seeded script `docs/briefs/research-int-scripts/gen_hw4_data.py` (numpy `default_rng`, standard library; seeds 2041, 2042, 2043), written to `app/content/data/research-int/`: `rates-gaps.csv` (2.1 KB), `lakes-level.csv` (5.3 KB), `fills-messy.csv` (14.5 KB). All far below 256 KB. No number set of the new items occurs elsewhere in `app/content/` (greps of the distinctive values 381950, 52350.5, 34271, 16818536, 0.84193; shared small numbers only).

- `h4-value-at` (was: value_at on `ticks-gaps.csv`, 286 times). Now `regrid(path, step)` and `longest_gap(path)` on `rates-gaps.csv`: 200 quotes, 14 written NA, 186 valid, minutes 5 to 479. Values: 30-minute grid 16 points (5, 35, ..., 455), rates at rows 0, 3, 7 = 0.8497, 0.8442, 0.8408416666666667; one-minute grid 475 points with mean 0.8419341052631579; longest gap 14 (12 if the NA rows were counted). Method A pure-Python bracket search; method B `np.interp` (mean 0.8419341052631578). Tiny file `20,2.0 / 0,1.0 / 10,NA / 40,4.0`: step 15 gives [[0, 1.0], [15, 1.75], [30, 3.0]], step 20 gives [[0, 1.0], [20, 2.0], [40, 4.0]], step 100 one row, gap 20. 8 tests (was 7). Mutants failing: interpolating by position (5 of 8 fail), grid stopping before the last minute (`+ 1` removed, 2 fail), not dropping NA (4 fail), forward fill (4 fail).
- `h4-town-slopes` (was: slope, intercept and R-squared for 13 towns, Wick NaN). Now `trend_table(path)` and `trending(path)` on `lakes-level.csv`: 9 lakes of 40 years and Tarn with 4 years; columns slope, se, t, n; NaN below 5 rows; `trending` lists the lakes with |t| above 2, largest first. Values (method A raw sums from `csv`, method B centred sums with `numpy`, equal to 1e-9): slopes Ard -0.013390056285178205, Gill 0.01314502814258912, Isla -0.008340431519699798; se Dee 0.0018137026547917082, Fyne 0.0020575279234840245; t Bala -1.5872, Hawes 1.6806, Ard -9.2752; list [Ard, Gill, Isla, Esk, Fyne, Dee] with t = -9.28, 8.58, -4.24, 3.51, 3.37, 3.06. Tiny file: V (x 1 to 5, y 10.0, 10.2, 9.9, 10.4, 10.3) slope 0.08, se 0.06, t 1.3333 (Sxy 0.8, Sxx 10, RSS 0.108); W has 4 rows and is NaN. 8 tests (was 6). Mutants failing: `n < 3` (3 fail), `n <= 5` (1 fails), divisor `n` or `n - 1` for `n - 2` (3 fail), threshold 1.5 (1 fails), ascending order (1 fails).
- `h4-clean-orders` (was: `clean_orders`, 570-row frame). Now `clean_fills(df)` on `fills-messy.csv` (402 rows, 380 ids, 10 final CANCELLED rows, 12 corrections, side in mixed case, qty such as '2k', price such as '£11.99'): a later row replaces an earlier one, a CANCELLED last row removes the id. Values (method A `csv` and plain Python, method B pandas, frames equal row by row): 370 rows, 193 buys, quantity total 381,950, signed value -52,350.5, seconds total 16,818,536. TINY (7 rows) leaves 4 rows: [[1, 34200, 1, 1000, 10.0], [2, 34271, -1, 250, 5.5], [4, 34380, -1, 50, 7.0], [5, 36005, 1, 2000, 9.5]]. 7 tests. Mutants failing: `keep='first'` (5 of 7 fail), dedupe before dropping cancelled in the wrong order (5 fail), no strip (4 fail), 'k' read as 00 (4 fail), time seconds dropped (2 fail).
- `r4-slope-evidence` (reused l17's 0.0052). New table: P, Q, S, U 60 days with standard error 0.0075 and slopes 0.020, -0.004, -0.017, 0.016; R 5 days, slope 0.550, se 0.3162; T 20 days, slope 0.090, se 0.0388 (all with sigma 1: $1/\sqrt{60 \cdot 3599/12} = 0.00746$, $1/\sqrt{10} = 0.3162$, $1/\sqrt{665} = 0.0388$). Ratios 2.7, -0.5, 1.7, -2.3, 2.3, 2.1 (displayed and unrounded standard errors agree to one place). Answer 3 to 4 (P, S, T, U). `wrong`: `big` 2 to 3 (60-day groups only: P, S, U), `all` 6 unchanged. Feedback `correct`, `byKey.big` and explain updated to match.
- `r4-add-row` (x grid 1 to 5, new point (5, 5), answer 0.9). Now sums 4, 14, 20, 54, 81 and the point (6, 10): new sums 5, 20, 30, 90, 141, slope $(705 - 600)/(450 - 400) = 2.1$. Method B centred: points (2,2), (3,4), (4,5), (5,9), (6,10), Sxy 21 over Sxx 10 = 2.1. `old` wrong 1.1 to 2.2 (before: Sxy 11 over Sxx 5 = 2.2). Answer 0.9 to 2.1.
- `r4-remove-row` (leaving point (1, 2), answer 1.0). Now sums 5, 25, 40, 135, 215 and the point (3, 6) leaves: new sums 4, 22, 34, 126, 197, slope $(788 - 748)/(504 - 484) = 2.0$. Method B centred on the four remaining points (4,5), (5,9), (6,8), (7,12): Sxy 10 over Sxx 5 = 2.0. `kept` wrong 0.9 to 1.5 (all five points: Sxy 15 over Sxx 10). Answer 1.0 to 2.0.
- `r4-rerun-checklist` (repeated l20's seed, paths, versions, one command). Now about repeating the cleaning: correct options `input` (a saved copy of the input, with its date or a hash), `code` (cleaning in code, never by editing the spreadsheet), `counts` (row counts printed after each step), `order` (the run order, written in one place); wrong `fresh` (the newest data downloaded on every run) and `hand` (odd rows fixed by hand). Old ids seed, rel, req, one, once, hand are replaced; `byKey` and explain rewritten.

### Voice and balance (9 to 12)

- 9: `rq-clean-frame-py` brief split into three sentences ("It returns a cleaned copy. Symbols are stripped and in upper case. Quantities are whole numbers. Keep one row per order id (the first), and only prices above zero."). `rq-stable-slope-cpp` brief: "..., has a zero denominator over a non-zero numerator there, so it returns inf or NaN, never 0.5." to "... there. It returns inf or NaN, never 0.5."
- 10: `q19-dedupe` key "They differ in text, so they are not exact duplicates yet" (57) to "The text differs, so they are not exact duplicates" (50). l18 "Say it aloud" key (71) to "An update costs p squared a row; a refit costs n times p squared." (65). l20 "Which reruns match" wrong options "A different seed" (16) and "No seed set at all" (18) to "The same code, run with a different seed" (40) and "The same code, run with no seed set at all" (42).
- 11: `q18-cost` wrong `p` (5) feedback: "You divided once too often. The $p^2$ cancels, leaving $n$." to "You divided $np^2$ by $np$, not by $p^2$. That leaves $p$." ($np^2/(np) = p = 5$.)
- 12: l16 transfer explain: "does the sort-free bracket search for you but needs sorted times" to "searches for the bracket for you but needs the times in increasing order".

### Wrong solutions, before and after

| Item | Wrong solution | Before | After |
|---|---|---|---|
| l16 transfer | `.first()`, `.last()`, `.max()`, `.min()` for `.mean()` | pass 8 of 8 | fail 3 of 11 |
| l18 `OnlineLine` | NaN when n < 3 | pass 7 of 7 | fails 1 of 8 |
| l19 `load_clean` | `price >= 0`; `keep='last'` | pass 6 of 6 | fail 2 of 8 each |
| `rq-interp-py` | no empty-input check | pass 13 of 13 | fails 1 of 14 |
| `rq-interp-py` | linear scan | pass | still passes (deferred, not testable) |
| `rq-group-slopes-py` | `sort=False` | pass 8 of 8 | fails 1 of 9 |
| `rq-online-ols-py` | stores rows, refits in `coef()` | pass 7 of 7 | stopped at 5 s (43.5 s here) |
| `rq-clean-frame-py` | `keep='last'` | pass 7 of 7 | fails 1 of 8 |
| homework `town_slopes` | guard `n <= 3` | pass | replaced; `n <= 5` and `n < 3` fail |
| homework `clean_orders` | `keep='last'` | pass | replaced; `keep='first'` for the new rule fails |

### Verification

- `node tools/validate.mjs`: 0 errors (539 warnings, all earlier ones).
- `playthrough --lesson research-int/l16-interpolating`, `l18-updating-a-fit`, `l19-timed-data-task`, `l20-writing-a-take-home`: all pass, with and without `--mobile`.
- `playthrough --set research-int/review-4` and `homework-4`: all pass (10 of 10; 8 of 8, 38 of 38 marks), with and without `--mobile`.
- `playthrough --drill` for the six `rq-*` drills: all pass (14, 9, 8, 8, 9 and 7 hidden tests, starters fail), with and without `--mobile`.
