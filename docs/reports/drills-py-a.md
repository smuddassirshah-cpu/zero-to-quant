# Drills pack `py`, agent A (`py-found` 12, `plotting` 6)

Brief: `docs/briefs/drills-1.1-1.9.md` (pack `py`, agent A), on top of `docs/briefs/drills-1.8.md` and `docs/briefs/drills-ci-packs.md`. 18 Python drills, `"pack": "py"`, no `pattern` (the idea is in `tags`), rows appended to `app/content/drills/index.json`. All data in briefs, examples and tests is my own.

| id | course | lesson drawn on | idea | difficulty | pace (s) | hidden tests | planted |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `py-trimmed-fill-mean` | py-found | l2-slicing, l8-who-changes-the-list | sort, slice off `k` each end (`k = 0` trap), caller's list kept | 1 | 420 | 12 | 3 |
| `py-holdings-change` | py-found | l6-membership | set difference and intersection over repeated tickers; one large test | 1 | 480 | 11 | 3 |
| `py-format-pence` | py-found | l16-returns-from-a-file | `£` formatting with commas and a leading minus, whole-number pence past $2^{53}$ | 2 | 600 | 12 | 3 |
| `py-cross-up-days` | py-found | l4-one-line-lists | one comprehension over `i` and `i - 1`, equal-then-above counts | 1 | 540 | 14 | 5 |
| `py-split-pence` | py-found | l1-why-not-0-3 | `round(fee * 100)` not `int`, `divmod` shares, spare pence first | 2 | 660 | 13 | 4 |
| `py-fill-summary` | py-found | l5-lookup-by-name | two dicts of running totals, quantity-weighted average | 2 | 660 | 11 | 3 |
| `py-quote-ladder` | py-found | l7-arguments | defaults in a stated order, keywords, no shared default list, rounded prices | 2 | 720 | 11 | 3 |
| `py-wide-to-long` | py-found | l10-reading-a-csv | `csv.reader`, stripped headers, blank and space cells, `\r\n`, sort | 3 | 960 | 13 | 3 |
| `py-batches` | py-found | l13-one-at-a-time | a generator that reads a feed lazily, new list per batch, `ValueError` | 2 | 660 | 14 | 4 |
| `py-split-adjusted` | py-found | l8-who-changes-the-list | a new list, backward running factor, split day itself unchanged | 3 | 900 | 12 | 3 |
| `py-guarded-returns` | py-found | l11-when-things-go-wrong | two narrow `except`s, `TypeError` let through | 3 | 960 | 12 | 3 |
| `py-cost-basis` | py-found | l12-data-with-behaviour | a class with an invariant: average cost, realised P&L, refused trades change nothing | 3 | 1080 | 15 | 5 |
| `py-growth-curve` | plotting | l7-drawing-drawdown ("From returns to wealth") | compounded growth of £100, start point included | 1 | 420 | 12 | 4 |
| `py-bar-limits` | plotting | l12-charts-that-mislead | y limits that keep zero, padded by the span | 1 | 480 | 11 | 3 |
| `py-bin-counts` | plotting | l6-shape-of-returns | histogram counts with `ax.hist`'s edge rule | 2 | 660 | 11 | 3 |
| `py-paired-returns` | plotting | l11-two-variables | scatter points from shared dates only, in date order | 2 | 780 | 11 | 3 |
| `py-underwater-series` | plotting | l7-drawing-drawdown | drawdown and days-since-peak series, equal-to-peak resets | 3 | 900 | 10 | 3 |
| `py-month-grid` | plotting | l10-panels ("A heat map of months") | tidy month by ticker table for grouped bars, compounded, `None` for gaps | 3 | 1140 | 15 | 4 |

Mix (after the fix pass): `py-found` 3 / 5 / 4 and `plotting` 2 / 2 / 2 at difficulty 1 / 2 / 3, so 5 / 7 / 6 for these 18 (first draft 4 / 5 / 3 and 6 / 7 / 5). For the pack's 30 to be 9 / 12 / 9, agent B's 12 would be 3 / 5 / 4. Skills are the named lesson's own (the check script reads them from the lesson file). Large tests only where the lesson teaches cost: `py-holdings-change` (60,000 tickers each side, so `in` on a list is too slow). The other large tests are length or sum checks of correctness.

## Checks

1. `docs/reports/drills-py-a-check.py` (scratchpad venv): `18 drills, 54 planted, errors: 0`, exit 0. It runs the model and an independent method on every example and test under the drill page's own comparison: removal by `list.remove`, `dict.fromkeys`, string grouping of digits, a boolean list, a ceiling formula, `Fraction` sums, `Decimal` quantising, a hand line parser, `itertools.islice`, a product over later splits, a type-checked reader, a `Fraction` cost-basis class with properties, prefix products, `np.histogram`, a pandas inner join with `shift`, `np.maximum.accumulate` index arithmetic, a pandas `groupby().prod().unstack()`. It recomputes each brief's worked example against a hand value, checks starters fail, every planted solution fails a test, skills, `how` counts, paces, the mix and the index rows.
2. `node tools/validate.mjs`: 0 errors, and no warning on any of the 18 files.
3. `node tools/playthrough.mjs --drill <18 ids> --local-cdn <pkgs>`: 18 ok, All passed; with `--mobile`: All passed. Screenshots of three drills at 440 px and desktop read cleanly.
4. `planted-check.mjs --drill <18 ids> --require --local-cdn <pkgs>`: 18 drills, 54 planted solutions, 0 failures.
5. Voice: `voice-scan.py 35` on the 18 files: 0 sentences over 35 words, 0 explanations over three sentences (36 of 524 sentences over 20). No em-dashes; the only `!` are `!=` in code.

## Planted solutions

No planted solution passed every test on its first run, so no test was added for that reason. Three tests were added where a slip was caught by one case only, so each such slip meets a second readable case: `cross_up_days([4.0, 5.0, 6.0], [5.0, 5.0, 5.0])` (the strict `<`), a header with a trailing space and a cell of spaces in `py-wide-to-long`, and a second unsorted pair of dicts in `py-paired-returns`.

## Drafting faults found and fixed

- My first tests used `setup` and `compare: "raises"`, and `isclose` on dicts and strings. The validator accepted them, but the drill page's own harness (`js/screens/drill.js`) runs neither and fails a dict or string under `isclose`. The model then failed most tests in the playthrough. Every case is now a single `call`; errors are tested through a `prelude` helper `_raised(f)` (named in `how`), and dicts and labels through `equal` tests. The check script now mirrors the drill harness, so it would catch this.
- The `py-quote-ladder` hint first quoted `5.0 + 3 * 0.05` as 5.1499..., which is false (it is 5.15); the check script's arithmetic asserts caught it. It now quotes `4.85 - 4 * 0.05` = 4.6499999999999995, which a test uses.

## Freshness

`node tools/fresh-check.mjs --drill <id>`: 0 hits for all 18. At `--min-run 8 --min-share 0` the hits are the shared tolerance and time-limit constraint lines between these drills and one `index.json` name row: stock phrasing, kept. Setups judged against the courses by hand: `homework-3` `Account` (deposits and withdrawals refused over the balance), so the class drill is average cost and realised P&L; `homework-2` P&L per ticker and `latest_prices`, so the dict drill is a weighted average per order; `l11` `load_orders`, so the exceptions drill separates two expected errors and lets a third through; `l13` `drawdowns`, `homework-4` `drawdown_period` and `backtest` `longest_underwater`, so the drawdown drill returns both chart series; `stat-models` `trimmed_mean(x, prop)`, so the slicing drill counts `k` and keeps the caller's list. No function name of a lesson code widget is reused. The existing `py-found` drills (daily and log returns, annualised volatility, maximum drawdown) and the `numpy-pandas` ones (cumulative P&L, rolling mean, Sharpe) are not repeated.

## Inbox

Two bullets under "Raised later (drills py a):" in `docs/BACKLOG-INBOX.md`.

Fix pass: tests, planted solutions, starters and four difficulty labels changed after the second read; the counts above are the first draft's. See `docs/reviews/review-drills-py.md`, `## Fix pass`.
