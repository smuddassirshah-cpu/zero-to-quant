# Drills, pack `dsa`, sub-pack A (hashing, prefix sums, simulation)

Brief: `docs/briefs/drills-1.8.md`, sub-pack A. Fifteen Python drills in `app/content/drills/`, each with a row appended to `drills/index.json`.

## Drills

| id | pattern | course | difficulty | pace (s) | stdin | hidden tests |
| --- | --- | --- | --- | --- | --- | --- |
| `dsa-majority-reading` | hashing | ds | 1 | 480 | no | 12 |
| `dsa-silent-sensors` | hashing | ds | 1 | 600 | no | 11 |
| `dsa-kth-repeat` | hashing | ds | 2 | 900 | yes | 12 |
| `dsa-traders-by-ticker` | hashing | ds | 2 | 900 | no | 11 |
| `dsa-trace-shapes` | hashing | ds | 3 | 1200 | no | 12 |
| `dsa-first-overdrawn` | prefix-sums | ds | 1 | 480 | no | 11 |
| `dsa-range-volumes` | prefix-sums | ds | 2 | 900 | yes | 12 |
| `dsa-staff-per-hour` | prefix-sums | ds | 2 | 900 | no | 12 |
| `dsa-flattest-stretch` | prefix-sums | ds | 3 | 1500 | no | 13 |
| `dsa-winning-stretch` | prefix-sums | ds | 3 | 1500 | no | 13 |
| `dsa-empty-orders-back` | simulation | ds | 1 | 600 | no | 11 |
| `dsa-trailing-stop` | simulation | ds | 1 | 600 | no | 12 |
| `dsa-stock-ledger` | simulation | ds | 2 | 1200 | yes | 11 |
| `dsa-rotate-rota` | simulation | ds | 2 | 900 | no | 11 |
| `dsa-looping-route` | simulation | algo-think | 3 | 1200 | no | 12 |

Difficulty split 5 / 6 / 4; three stdin drills (`solve_<slug>(text)`, tagged `stdin`, tests with trailing newlines, blank lines and extra spaces). Skills are `ds-hashing`, `ds-arrays`, `ds-pointers` (declared by `ds` lessons) and `at-complexity` (`algo-think`).

Each drill's last one or two tests are large inputs. A naive version of every drill (count per element, `in` on a list, slice sums, per-slot loops, step-by-step walking, one-at-a-time rotation) was timed natively in `<scratchpad>/dsa-a/naive.py`: all ran past 8 s except the rota (7.2 s natively, so well past 5 s in Pyodide). The model solutions take at most 0.13 s natively.

## Checks

1. `docs/reports/drills-dsa-a-check.py` (venv Python): model solution and an independent slow method (sort and group, bisect, numpy slices and all-pairs scans, per-item replay, literal walking, pairwise comparison for small trace sets) agree with every example and hidden `expect`; the starter fails at least one hidden test in all 15. Exit 0, `errors: 0`.
2. `node tools/validate.mjs`: 0 errors, no warnings on the `dsa-` files.
3. Playthrough `--drill` x15 `--local-cdn`: all passed (model solution passes every hidden test, starter fails), and all passed again with `--mobile`. Browser relaunches 0.
4. Voice: `voice-scan.py 35` on a copy of the 15 files: 0 over three sentences, 0 sentences over 35 words of 432. No exclamation marks, no em or en dashes; British spelling.
5. Fresh: `node tools/fresh-check.mjs --drill <id>` gives 0 hits for all 15. Triage at `--min-run 8 --min-share 0`: the only hits are the stock constraint sentence "... is too slow. All tests share a 5-second time limit." shared with `ci-` drills and each other, the stdin sentence "Lines may carry extra spaces, and the text may end with blank lines" (three stdin drills here and py-found `homework-1` item 5), and "are case-sensitive strings"; all house phrasing, not a setup. No function name is shared with a lesson code widget.

## Fresh-setup notes

Lesson `ds/l7` teaches counting runs with sum `k`, and `coding-int` has the longest zero-sum run, so the prefix-sum d3 drill is instead the closest-to-zero stretch (sorted prefix totals). Lesson `ds/l4` has the ticker tally and anagram grouping, so the counting drill is a strict-majority reading and the grouping drills key on a ticker and on step shapes.

A first draft had a two-dimensional block-sum drill. The loose triage paired it with `ci-cpp-range-sums` (grid rectangle sums, same setup in C++), so it was replaced by `dsa-winning-stretch` (longest run with strictly more winning days: running score and the first position of score minus one). Its neighbour `ci-balanced-run` asks for equal counts, a lookup of the same score; the strict version needs the one-below lookup and the argument in its second note, so it was judged a different task. `dsa-first-overdrawn` and `dsa-trailing-stop` share running totals and running maxima with `cumulative-pnl` and `max-drawdown`, but ask a different question (first crossing of a level), so they stand.
