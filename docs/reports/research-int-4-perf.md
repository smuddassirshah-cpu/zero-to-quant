# research-int level 4: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/research-int/homework-4.json`, item `h4-quote-at`, index 8 (item 9 of 9; nothing converted).
- Kind `code` (Python, standard library `bisect`), difficulty 5, skill `rq-data`, pace 1200.
- Objective matched: l16 "Write a linear interpolator that handles gaps, edges and unsorted input." l20 "Write a take-home report" also matches, but a longform self-mark is weaker evidence than an auto-graded product, and the l20 passages carry open audit notes (pound-typed rows), so `code` was chosen. The task stays clear of l14 and l20.
- Fresh: l16 holds the end for ever and `h4-value-at` regrids with `np.interp`. This task adds a trust window `max_gap` inside and at the ends, cancelled `None` prices, answers in the asked order, and a log-cost requirement.
- Tests: 2 examples, 10 hidden (isclose, `None` must be `None`). Test 10 runs 40,000 quotes and 40,000 seconds: the solution takes 0.08 s in CPython, a linear scan about 28 s (limit 5 s). Ten planted bugs are each caught (the last two are the repeated-second slips, caught by value test 9): no sort, last repeat wins, `None` read as 0, no inside gap rule, ends held for ever, `>=` at `max_gap`, sorted output, linear scan. The starter fails all 10.
- Freshness grep: `max_gap`, `stale`, `quote_at`, `cancel`, `bisect`, `interp`.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "research-int/L4: has a performance task, remove from perf-pending".
2. `VOICE_BASE=app/content/courses/research-int python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 docs/reports/research-int-4-perf-numbers.py` (venv, numpy): exit 0. Each expectation is checked three ways: worked by hand, by the solution, and by a numpy route (`unique`, `bincount`, `interp`). The script also runs 400 random cross-checks, the starter and the bugs.
4. `node tools/playthrough.mjs --set research-int/homework-4 --local-cdn <pkgs>`, with and without `--mobile`: All passed, with one performance starter failing as required. Shots at 440 px read.

No backlog bullets. No course.json change.

Fix pass notes:
- Fresh part: the objective is l16's own product (blank prices, repeated seconds averaged, sort then bisect, held ends appear on l16 screen 10, `price_at` and `clean_ticks`). What is new here is the `max_gap` trust window inside and at the ends, a list of asked seconds answered in order, and the log-cost demand.
- `fresh-check --file`: one hit, `big_case`, a hidden postlude helper shared with coding-int homework-1 and homework-3.

Overlapping screens: l16-interpolating screens[2] (points in any order), [3] (beyond the ends, hold the nearest value), [4] (the same x twice, merged), [5] (a missing value on uneven times), [7] (nothing left to interpolate), [8] and [9] (the formula and the sorted, merged, bracketed procedure), [11] (ten million rows), homework-4 `h4-value-at` (regridding with `np.interp`), review-4 `r4-interp-sorted`; new parts: a trust window `max_gap` between quotes and at both ends, cancelled `None` prices, answers in the order asked, and a log-cost requirement per asked second.
