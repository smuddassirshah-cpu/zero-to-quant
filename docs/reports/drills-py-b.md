# Drills pack `py`, agent B (`numpy-pandas`, 12 drills)

Brief: `docs/briefs/drills-1.1-1.9.md` (pack `py`, agent B), on top of `docs/briefs/drills-1.8.md` and `docs/briefs/drills-ci-packs.md`. Files `app/content/drills/py-*.json`, `"pack": "py"`, `"course": "numpy-pandas"`, no `pattern` (the idea is in `tags`), rows appended to `drills/index.json`. One data file: `app/content/data/numpy-pandas/volumes.csv` (own numbers). The three untagged drills of the course (`rolling-mean`, `sharpe-ratio`, `cumulative-pnl`) and every lesson and homework code task were read first and are not repeated.

| id | lesson drawn on | idea | difficulty | pace (s) | returns | hidden tests | planted |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `py-big-move-days` | l3-masks | two conditions in one mask, `np.abs`, `&` | 1 | 420 | list of int | 10 | 3 |
| `py-best-desk-each-day` | l2-shapes-and-axes | `argmax` along `axis=1`, first desk wins a tie | 1 | 420 | list of str | 10 | 3 |
| `py-carry-forward-limit` | l7-gaps | `ffill(limit=k)`, limit 0, leading gap | 1 | 480 | Series | 10 | 4 |
| `py-volume-surge` | l6-loading-prices, l9-returns-with-shift | read a CSV by column name, compare with `shift(1)` | 1 | 480 | list of str | 10 | 4 |
| `py-fx-to-pounds` | l4-broadcasting | a per-day rate as a column, `rates[:, None]` | 2 | 600 | 2-D array | 10 | 3 |
| `py-day-fills` | l12-split-apply-combine | named `agg`: signed net, VWAP, count | 2 | 720 | DataFrame | 11 | 4 |
| `py-weekly-range` | l11-daily-to-monthly | `resample("W-FRI")`, empty weeks dropped | 2 | 720 | Series | 11 | 3 |
| `py-gap-aware-returns` | l7-gaps, l9-returns-with-shift | a return across a missing close stays NaN | 2 | 660 | Series | 11 | 3 |
| `py-combined-desk-pnl` | l13-joining-on-dates | outer join on the date, 0 for a silent desk | 2 | 720 | Series | 11 | 3 |
| `py-prior-zscore` | l10-rolling, l9-returns-with-shift | rolling window ending yesterday, flat window NaN | 3 | 960 | Series | 10 | 4 |
| `py-excess-vs-benchmark` | l12-split-apply-combine, l13-joining-on-dates | returns inside each ticker, index return before the merge | 3 | 1140 | Series | 10 | 4 |
| `py-month-hit-rate` | l11-daily-to-monthly, l12-split-apply-combine | month-end returns, drop the first NaN, group by calendar month | 3 | 1080 | Series | 11 | 4 |

Mix 4 / 5 / 3 at difficulty 1 / 2 / 3 (the brief's 3 : 4 : 3 for 12, rounded as its 25-drill row is). Each brief says what the function returns and how the tests read it.

## How the tests compare

The drill page judges with its own `__zq_eq` in `js/screens/drill.js`, not the code widget's comparison: in `isclose` NaN never matches, and a dict, string or Series fails. So every pandas result reaches the tests as a plain list (`tolist()`, `index.tolist()`, `to_numpy().tolist()`), and the three drills whose answers hold NaN call a prelude helper `_plain`, which shows NaN as `None`; each such test carries a `show` of the plain `.tolist()` call and the brief says so. Text and whole-number results use `equal`, floats `isclose` (rel `1e-9`). Found in the real runtime (below); inbox bullet 1.

## Checks

1. `docs/reports/drills-py-b-check.py` (scratchpad venv: NumPy 2.0.2, pandas 2.2.3, the Pyodide versions): exit 0, "12 drills, 42 planted, 0 errors". It runs the model and an independent plain-loop method (no pandas shift, rolling, resample, groupby or merge) on all 149 examples and tests against each `expect` with a copy of the drill page's rule, learner code before the prelude as the page does. It also checks that the starter and each planted solution fail a hidden test, recomputes the brief numbers by hand (VWAP 72.546, ranges 0.048, z of 3 and -1.528, 197.1 bp), and checks the mix, paces, test counts in `how` and index rows.
2. `node tools/validate.mjs`: 0 errors; no warning on these files.
3. `node tools/playthrough.mjs --drill <12 ids> --local-cdn <pkgs>`: All passed; with `--mobile`: All passed. Screenshots at 440 px and desktop (`carry-forward-limit`, `excess-vs-benchmark`, `month-hit-rate`) read cleanly, with no sideways scroll.
4. `node tools/planted-check.mjs --drill <id> ... --require --local-cdn <pkgs>` on all 12: 42 planted solutions, 0 failures.
5. Voice: `voice-scan.py 35` on the 12 files: 0 sentences over 35 words, 0 explanations over three sentences; no em-dashes, no exclamation marks.
6. `node tools/fresh-check.mjs --drill <id>`: 0 hits on the 12 shipped. A first draft, `py-overnight-gaps`, hit `py-found/homework-1` item 9 (the same overnight-gap setup and function name); I replaced it with `py-volume-surge` before any commit.

## Planted solutions

None of the 42 passed every hidden test at first, so no test was added for that reason. A planted solution caught by only one test: `carry-forward-limit` (limit 0 raising; in-place fill), `volume-surge` (columns by position), `month-hit-rate` (a flat month counted as a rise). Four extra wrong solutions I did not plant (a pooled index mean, grouping by year, a zero-filled first volume, ISO-week labels) each fail one or more tests.

Two faults were found in the real runtime and fixed before commit. First, the NaN and dict comparison above: model passes of 5/10, 9/10 and 0/11 on the first planted-check. Second, a drill missing from the manifest timed out (inbox bullet 3).

## Engine limits

Four bullets in `docs/BACKLOG-INBOX.md` under `Raised later (drills py b):`. The first commit's `index.json` already lists the six drills of the second commit.
