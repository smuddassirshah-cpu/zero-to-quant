# research-int level 4 report: Data tasks and take-homes

Author: content agent, 4 November 2026 (worktree branch `worktree-agent-a8859a2b6006bfb36`). Brief: `docs/briefs/research-int.md` `## Level 4` plus its shared sections. Files in `app/content/courses/research-int/` and `app/content/drills/`. `course.json`, the data files, the engine and other levels are untouched. The six data files in `app/content/data/` were only read; their SHA-256 prefixes were checked against the brief first (all six match).

## Files

| File | Screens | Quiz / items | Canvases and widgets | Notes |
| --- | --- | --- | --- | --- |
| `l16-interpolating.json` | 12 | 4 | `series` with `null` gaps and `markers` (two screens), `table`, `console`; `numeric`, `choice`, `order` with distractor, `code` (with `data`) | hook (gaps 100, 112), formula on two points, unsorted, ends held, repeated x, missing y by time against by position, trap (`interpolate()` is by position), edge (nothing left), derive, say it aloud, transfer code on `ticks-gaps.csv`, "The follow-up" (ten million rows) |
| `l17-regression-by-group.json` | 11 | 4 | `table` (hook, 12 slopes), `bars` (trap), widgets `numeric`, `code`, `choice`, `order` | hook (Reed's slope by hand), code `slope_by_town` on `towns-temp.csv`, read the table (4 negative), SE 0.0052, three routes agree, trap (Wick 0.3), edge (one day), derive (SE), say it aloud, transfer (beta 1.3), "The follow-up" (5,000 groups) |
| `l18-updating-a-fit.json` | 12 | 4 | `table` canvases of running sums, `matrix` (P and x); `table` widget (five sums), `numeric`, `code` (`OnlineLine`), `choice`, `order` | hook, slope 0.8, add (5, 8) gives 1.3, remove (1, 2) gives 1.4, Sherman-Morrison denominator 2.5, code, trap (variance 0.0), edge (removing a row never added), derive (centring), say it aloud, transfer (rolling beta 1.24), "The follow-up" (forgetting factor) |
| `l19-timed-data-task.json` | 12 | 4 | `console` with `tap-regions` (hook), `bars` (row counts 600, 585, 570); three `code` screens with `data` and a shared hidden `prelude` | hook (tap five problems), repeats missed by `drop_duplicates()` (3), stage one clean (6 min), stage two VWAP (8 min), stage three slippage model (11 min), 3,200-share cost 4.642, trap, edge (price zero), derive (sign), say it aloud (names the drill), transfer (VWAP 31.225), "The follow-up" (`multi`) |
| `l20-writing-a-take-home.json` | 10 | 4 | `bars` histogram of the 2,000 draws with `cut`; `order` with distractor (hook), `code` with `data`, `multi` (two) | hook (order the sections), `make_report`, which reruns match, interval width, checklist, trap (it ran once), edge (row order), say it aloud (names the free resources), transfer (interval 1.147 to 1.337), "The follow-up" |
| `review-4.json` | | 10 items, difficulty 2 to 4 | untimed; every item has `skills`, `tags`, `pace` | `numeric` ×7, `choice`, `multi`; the item list is below |
| `homework-4.json` | | 8 items, difficulty 3 to 5, two at 5 | four `code` items (all with `data` or none), `longform` with a 10-point rubric and model answer, `table`, `order` derivation, `numeric` | every item has `skills`, `tags`, `pace` |
| `app/content/drills/rq-*.json` ×6 and 6 rows in `drills/index.json` | | | see Drills | |

Every lesson has `minutes: 15`, the objective and skills from `course.json` (`rq-data` on l16 and l17; `rq-data` with `rq-linalg` on l18; `rq-data` with `rq-case` on l19; `rq-case` on l20), one `trap` with a `byKey` line naming the blurt, one edge case, a "Say it aloud" `generalise` screen with a `choice` over spoken answers, a quant `transfer`, and a closing `ladder` titled "The follow-up". l20 has no `derive` (the brief names none for it); the others have one, each with a distractor line. Each lesson's first prose states a pace ("About two minutes a question; say your reasoning aloud first", "About ten minutes with the code").

### Tags and pace

Families: `interpolation` (l16); `group-regression` (l17); `rank-one-update` and `numerical-stability` (l18); `data-cleaning`, `vwap`, `slippage-model` (l19); `take-home-writeup` and `reproducibility` (l20).

| File | Paced screens (sum) | Quiz (sum) |
| --- | --- | --- |
| l16 | 12: 11 at 150 s and the code screen at 600 s (2,250 s) | 4 at 150 s (600 s) |
| l17 | 11: 10 at 150 s and the code screen at 600 s (2,100 s) | 4 at 150 s (600 s) |
| l18 | 12: 11 at 150 s and the code screen at 600 s (2,250 s) | 4 at 150 s (600 s) |
| l19 | 12: 9 at 150 s, code screens at 360, 480 and 660 s, that is 6, 8 and 11 minutes, the 25-minute plan (2,850 s) | 4 at 150 s (600 s) |
| l20 | 10: 9 at 150 s and the code screen at 600 s (1,950 s) | 4 at 150 s (600 s) |
| review-4 | 10 items, 1,005 s (untimed, pace shown) | |
| homework-4 | 3,930 s: code 600, 600, 900, 600; longform 600; table 240; order 240; numeric 150 | |

### E3 example draw (for the exam author; no level file holds a `draw`)

- `{ "from": "bank/research-4", "tags": ["interpolation", "group-regression"], "difficulty": [3, 4], "n": 2 }` (as the brief gives it). The numeric and choice review items carry the tags `interpolation`, `group-regression`, `rank-one-update`, `numerical-stability`, `data-cleaning`, `slippage-model`, `reproducibility` for the bank author to copy.

## Review and homework items

Review (all fresh numbers, see the next section): R4.1 `r4-interp-sorted` (d2, interpolation, 38; wrong 42.5 first two listed points); R4.2 `r4-interp-time` (d3, 53 by time, wrong 56 by position); R4.3 `r4-slope-evidence` (d3, group-regression, six slopes with standard errors, 3 beyond two standard errors); R4.4 `r4-beta-per-stock` (d4, `choice`, the guarded `groupby(...).apply` of cov over var; distractors mix `np.var` with `np.cov`, read the whole frame, and a loop that keeps the last); R4.5 `r4-add-row` (0.9, wrong 1.1); R4.6 `r4-remove-row` (1.0, wrong 0.9); R4.7 `r4-naive-variance` (d4, numerical-stability, 2.6667 against the true 1.6667); R4.8 `r4-rows-left` (749, wrong 744 and 780); R4.9 `r4-predict-slip` (3.2072, wrong 11.2 and 9.424); R4.10 `r4-rerun-checklist` (`multi`, reproducibility).

Homework: H4.1 `h4-value-at` (d4, `code`, `ticks-gaps.csv`); H4.2 `h4-town-slopes` (d4, `code`, `towns-temp.csv`); H4.3 `h4-online-ols` (d5, `code`, Sherman-Morrison, 20,000 rows inside a per-case `budget`); H4.4 `h4-writeup-longform` (d5, 10-point rubric, model answer); H4.5 `h4-vwap-table` (d4, `table` with edit cells); H4.6 `h4-clean-orders` (d4, `code`, `orders-messy.csv`); H4.7 `h4-normal-equations` (d4, `order` with the distractor "divide Σxy by Σxx"); H4.8 `h4-se-fifty` (d3, `numeric`, tolerance 0.00005).

## Departures from the brief, and why

1. **Fresh numbers (DECISIONS "Fresh numbers in reviews and homework", and "Duplicates").** The brief's review and homework items repeat the lessons' own numbers (R4.1 and R4.2 use the l16 cases, R4.3 the l17 table, R4.5 and R4.6 the l18 sums, R4.8 and R4.9 the l19 results, H4.1 to H4.6 and H4.8 the lessons' file values). The orchestrator's rule overrules, so every review and homework item has numbers that appear in no lesson of this course. Still the brief's skills and shapes: R4.1 sorted pairing, R4.2 by time against by position, R4.3 a slope evidence count (now from a table of six groups with standard errors, since the 12-town table is in l17), R4.4 the guarded group-by (stock betas, with a `np.var` against `np.cov` distractor in place of the brief's `.slope()`), R4.5 and R4.6 add then remove a row, R4.7 a float64 variance, R4.8 the rows left, R4.9 a slippage prediction, R4.10 the rerun checklist. H4.1 queries seconds 3,333, 16,000 and 20,000 and a small hand-made file; H4.2 tests Bath, Hove, Ince and Cork (not the lessons' Ayr and Leith) and returns four columns; H4.3 uses its own sequence; H4.4 is on a fills file with new counts (900 to 851, slope 0.95, standard error 0.12, 4.02 bp); H4.5 uses a six-row frame; H4.6 tests the buy count, median quantity and total value on the file and a seven-row case; H4.8 uses sigma 2.0 over 50 days. The lessons keep the brief's numbers.
2. **l18 code screen is `OnlineLine` (running sums), not `OnlineOLS(p)`.** The lesson teaches the sums method for a straight line (the brief's Method), and the Sherman-Morrison class `OnlineOLS(p)` is the drill `rq-online-ols-py` and H4.3 as the brief lists them. This keeps the class from appearing three times with the same sequence.
3. **Interval end.** The brief writes £88.23k for the upper end of the l20 bootstrap interval. The exact value is 88.22498, so every text says £88.22k (lower end 77.45196, £77.45k). Seed 0, `default_rng(0).integers(0, 396, (2000, 396))`.
4. **Sort by id inside `make_report`.** The brief's edge case "a draw that depends on row order" needed a rule that removes it, so the function sorts by `id` before drawing (the file is already in id order, so the brief's numbers are unchanged), and a hidden test shuffles the rows.
5. **R4.7.** The brief's float64 variance of 10^9 + 1 to + 3 is the l18 trap. The review item uses 10^8 + 1 to + 4, where float64 returns 2.6667 (true 1.6667); the plain loop, `sum()` and NumPy sums agree on it, in Python 3.12 (Pyodide) and 3.13.

No `course.json` change is proposed.

## Drills (E8)

Six files in `app/content/drills/`, each with `pattern`, `pace`, `tags`, `skills`, hidden tests (each with a `why`), a model solution, and a row in `drills/index.json` (`id`, `name`, `course: "research-int"`, `difficulty`; the file already held 8 rows, now 14).

| Drill | Pattern | Difficulty | Pace | Tests | Notes |
| --- | --- | --- | --- | --- | --- |
| `rq-interp-py` | `interpolation` | 3 | 900 | 13 | the l16 cases, `None` and NaN as missing, `raises ValueError` when nothing is left, 100,000 points |
| `rq-group-slopes-py` | `group-regression` | 3 | 900 | 8 | six-row `DF` in the prelude (groups `u` and `v`), small group NaN, 1,000 groups |
| `rq-online-ols-py` | `rank-one-update` | 4 | 1500 | 7 | l18 sequence [1.5, 0.8], [0.5, 1.3], [0.1, 1.4]; 200 rows, 50 removals, 5,000 rows against `np.linalg.lstsq`; skills `rq-data` and `rq-linalg` |
| `rq-clean-frame-py` | `data-cleaning` | 3 | 900 | 7 | the brief's six-row frame: 3 rows left, ALPHA VWAP 13,100/1,300 = 10.0769, input unchanged |
| `rq-interp-cpp` | `interpolation` | 3 | 900 | 9 | `language: "cpp"`, `types` given, the l16 cases |
| `rq-stable-slope-cpp` | `rank-one-update` | 4 | 1200 | 7 | centred slope 0.5 and intercept -499,999,999 on 10^9 + 1 to + 3, `tol` rel 1e-9, no `try`; skills `rq-data` and `rq-linalg` |

`rq-stable-slope-cpp` carries the tag `numerical-stability` (its pattern is `rank-one-update`, the only fit among the four level patterns).

## Validator, voice, playthrough

- `node tools/validate.mjs` (from `app/`): **0 errors** (475 warnings in all, none an error). The warnings in this level's files are "a point hint usually highlights the canvas" and "a problem screen without a canvas before the ladder ends" (code, order, choice and table screens with no diagram), as in level 3.
- Voice: `VOICE_BASE=<abs>/app/content/courses/research-int python3 docs/reviews/voice-scan.py` (all of research-int, which includes this level and its `how` lines and model answers): **0 sentences over 20 words, 0 explanations over three sentences**. No `!`, no em-dash, no emoji, no American spelling (grep). Choice keys: no key is more than 8% longer than its longest distractor (22 options were rebalanced after a script flagged them; `keys.py`), every `choice` and `multi` has `shuffle: true`. A numeric `unit: "%"` is not used in this level.
- Playthrough with `--local-cdn <scratchpad>/pkgs`, from `app/`: five lessons, `review-4` and `homework-4` with `--mobile` (390 px) and without it, and the six drills with `--drill` ×6, with and without `--mobile`: **all passed**.

| Lesson or set | Desktop | 390 px |
| --- | --- | --- |
| l16-interpolating | 16 checks, quiz 4/4 | 16 checks, quiz 4/4 |
| l17-regression-by-group | 15 checks, quiz 4/4 | 15 checks, quiz 4/4 |
| l18-updating-a-fit | 16 checks, quiz 4/4 | 16 checks, quiz 4/4 |
| l19-timed-data-task | 16 checks, quiz 4/4 | 16 checks, quiz 4/4 |
| l20-writing-a-take-home | 14 checks, quiz 4/4 | 14 checks, quiz 4/4 |
| review-4 | 10 items, recorded 10 of 10 | same |
| homework-4 | 8 items, marked 8 of 8 right, 38 of 38 marks | same |
| `rq-interp-py`, `rq-group-slopes-py`, `rq-online-ols-py`, `rq-clean-frame-py` | 13, 8, 7 and 7 of the hidden tests with the model solution, starter fails | same |
| `rq-interp-cpp`, `rq-stable-slope-cpp` | 9 and 7 of 9 and 7 (compiled in the browser), starter fails | same |

Two things the drill playthrough found, both fixed: `rq-interp-py` had a `raises` case and `rq-online-ols-py` a test `tol`, and the Python drill harness supports neither (12 of 13 and 4 of 7 passed); the raises case became a missing y at the left end and the helper in the prelude rounds to six places (backlog). One 390 px run of the six drills showed `rq-clean-frame-py` at 0 of 7 once (a package load that had not finished); it passed alone and in two further full runs, so it is recorded as a flake, not a content fault.

Screenshots (desktop and 390 px, every lesson screen, review and homework item) were looked at. Fixed from them: the l16 `series` screens showed only the last known point because a point beside a gap draws no mark (known values now carry `markers`); the l17 slopes bar chart thinned its town labels and showed Deal's -0.0005 as 0.000, so the "how many are negative" question had no honest chart (now a four-column `table` of slopes to four places); 22 sentences over 20 words in `how` lines, explanations and summaries; 22 over-long choice keys.

### Code in Pyodide

Every Python `code` widget (eight in lessons and homework) and the four Python drills were run in Pyodide 0.27.7 under Node with `l4_codecheck.mjs`: the model solution passes every hidden test and example, and the untouched starter fails them. The only starter passes are tests that a do-nothing starter meets by construction: l16 the column-name test (1 of 8), H4.6 the "input frame unchanged" test (1 of 6) and `rq-clean-frame-py` the same (1 of 7). The playthrough runs each solution again in the app's worker. A learner who refits after every row in H4.3 takes about 3 s for 3,000 rows (quadratic), so the 20,000-row test stops at its 7 s limit; the model solution takes under 1 s.

| Widget | Solution | Starter passes |
| --- | --- | --- |
| l16 `clean_ticks`, `price_at`, `price_at_np` | 8 of 8 | 1 of 8 |
| l17 `slope_by_town` | 6 of 6 | 0 of 6 |
| l18 `OnlineLine` | 7 of 7 | 0 of 7 |
| l19 `load_clean`, `vwap_by_symbol`, `slippage_model` | 6, 4 and 4 | 0, 0 and 0 |
| l20 `make_report` | 8 of 8 | 0 of 8 |
| H4.1 `value_at`, H4.2 `town_slopes`, H4.3 `OnlineOLS`, H4.6 `clean_orders` | 7, 6, 6 and 6 | 0, 0, 0 and 1 |
| four Python drills | 13, 8, 7 and 7 | 0, 0, 0 and 1 |

## Dataset and seed conventions

The six CSV files are read as they are (no regeneration; SHA-256 prefixes checked). l20 and H4.3 use `numpy.random.default_rng(seed)`: seed 0 for the report (`rng.integers(0, n, (n_boot, n))` on the errors, sorted by `id`), seeds 5, 11, 3 and 21 for the checks on random rows in the l18 code screen, H4.3 and `rq-online-ols-py`. The l20 histogram holds the 2,000 draws of seed 0 rounded to three places as `bars` `data`, so no canvas depends on a random stream.


## Numbers, with sources

Every number was computed twice. Method A is a hand formula (pure Python, `fractions` or `math`; `refs.py` reads the CSV with the `csv` module); method B is pandas, NumPy or statsmodels in Pyodide 0.27.7 (numpy 2.0.2, pandas 2.2.3). The brief's scripts were re-run first: `l4_data_tasks.py` (ALL AGREE) and `stable_slope.py` (ALL AGREE). My own checks are in `docs/briefs/research-int-scripts/` as new files (nothing existing was edited): `l4_aux.py` (the fresh review, homework and lesson numbers), `l4_boot.py` (the l20 bootstrap), `l4_refs.py` (pure-Python references read from the CSV files), `l4_sm_test.py` (Sherman-Morrison against `lstsq`) and `l4_codecheck.mjs` (every Python code widget and drill in Pyodide). The values are repeated here.

**Lessons (brief numbers).** l16: gaps 100, 104, 108, 112; cases 125, 27.5, 13.0, 10, 30, 15, 22.5, 103 against 106; `ticks-gaps.csv` 312 rows, 15 blank prices, 12 repeated seconds, 286 clean times, values 100.5572 (12,000), 99.95228476821192 (100), 101.33592086330935 (23,000), 99.98 at 5, 101.295 at 23,400 (method A bisection against method B `numpy.interp`, 1e-9). l17: 13 towns, 1,202 rows, slopes Ayr -0.0410086 to Leith 0.0997918, four negative, Deal -0.0005, R² from 0.0001 (Deal) to 0.8023 (Leith), Wick 0.3 unguarded, SE $1.5/\sqrt{83{,}325} = 0.0052$ (cov/var, `polyfit` and statsmodels agree to 1e-10). l18: sums 4, 10, 14, 30, 39, slope 0.8, intercept 1.5; add (5, 8) 5, 15, 22, 55, 79, 1.3 and 0.5; remove (1, 2) 4, 14, 20, 54, 77, 1.4 and 0.1; Sherman-Morrison 1 + xᵀPx = 2.5, innovation 2.5, new P [[1.1, -0.3], [-0.3, 0.1]]; naive variance of 10^9 + 1 to + 3 is 0.0; the stable slope 0.5 and intercept -499,999,999. l19: 600 rows, 15 repeats of which 12 exact (3 missed), 570 clean, ALPHA 230 and 50.0152, BRAVO 206 and 120.0146, CHARLIE 134 and 8.0005, total quantity 1,203,200, 46.3874 with the -999 and repeats left in, slope 1.2421 (SE 0.0486), intercept 0.3375, R² 0.5346, mean 3.795, 3,200 shares 4.642. l20: 396 clean rows, mean £307.22k, RMSE £82.8998k (82.90), draws 2.5th and 97.5th percentiles 77.4520 and 88.2250, 2,000 draws from seed 0, loop and vectorised draws identical (difference 0.0), same seed identical, seed 1 differs (77.7853, 88.4059), shuffled rows after sorting by id identical, 50 draws below the lower end, draws' standard deviation 2.7613.

**Mine.** l16 quiz: (0, 10), (4, 50) at 1 is 20; one point 42; times 0, 3, 4 with 10, gap, 18 give 16 against 14. l17: Reed 0.9 (endpoints 1.0), Marsh -0.6, Plain 0; quiz 0.6 (endpoints 0.3333), SE with sigma 3.0 is 0.0104, two rows give R² 1; transfer beta 0.000234/0.000180 = 1.3 (inverted 0.7692). l18: quiz sums 3, 6, 9, 14, 19 give 0.5 (and 19/14 = 1.3571 wrong); add (4, 8) gives 1.7; cost ratio n = 10,000; transfer window 250, 20, 30, 580, 720 with (3, 4) in and (-2, -3) out: sums 25, 37, 585, 726, slope 180,575/145,625 = 1.24 exactly (add-only 1.2419). l19: quiz 863; VWAP £10.30 (£10.20 simple mean); seller at 49.80 against mid 50.00 is +40 bp; transfer £31.225 (repeat left in £31.2727, simple mean £31.1333); mis-answers 40.09 (no log) and 10.363 (ln 3,200). l20: interval lower end 1.2421 - 1.96 × 0.0486 = 1.1468 (method A hand; the unrounded fit 1.14676); quiz 52.8 - 41.2 = 11.6, 50 of 2,000.
Review: R4.1 38 (42.5 by the first two listed), R4.2 53 (56 by position), R4.3 standard errors 0.0052 (100 days), 0.0416 (25 days, $1.5/\sqrt{1300}$), 0.6708 (4 days, $1.5/\sqrt{5}$) and the ratios 5.97, -0.77, 0.30, -4.23, 2.16, 1.64 give 3, R4.5 and R4.6 from sums 4, 10, 13, 30, 38 (slope 1.1), add (5, 5) sums 5, 15, 18, 55, 63 (0.9), remove (1, 2) sums 4, 14, 16, 54, 61 (1.0), checked by `fractions` against `np.polyfit`; R4.7 2.6666666666666665 (exact 1.6667), R4.8 800 - 20 - (36 - 5) = 749 (744 double count), R4.9 0.4 + 1.35 ln 8 = 3.2072.
Homework: ticks at 3,333, 16,000 and 20,000 are 100.28438461538461, 101.34113043478261 and 101.6523970856102 (A bisection, B `np.interp`); small file points (10, 6.0) and (30, 9.0) give 7.5 at 20 and 8.25 at 25; Bath -0.0236696, Hove 0.0300376, Ince intercept 12.2381394, Kelso R² 0.7432052, Cork R² 0.0558597 (cov/var against statsmodels, 1e-10); online sequence points (1, 4), (2, 6), (3, 9), (4, 10): 2.0 and 2.1; add (5, 14): 1.4 and 2.4; then remove (2, 6) by `fractions`; Sherman-Morrison from $P = 10^8 I$ matches `lstsq` to 1.4e-10 at 200 rows and 5e-12 at 20,000 (start 1e8 times the identity; 1e10 loses accuracy); H4.4 900 - 24 - 18 - 7 = 851, interval 0.95 ± 1.96 × 0.12 = 0.7148 to 1.1852, 0.30 + 0.95 ln 50 = 4.0164; H4.5 X 1,000 shares VWAP 20.16 and Z 800 shares 55.2125 (fractions against `np.average`); H4.6 271 buys, median quantity 2,300, total value £78,732,175.8 (A pure Python, B pandas) and the seven-row case 3 rows, 1,900 shares; H4.8 $2.0/\sqrt{10{,}412.5} = 0.0196$ (formula against $\sqrt{[(X^TX)^{-1}]_{11}}$).
