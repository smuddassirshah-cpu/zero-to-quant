> Superseded in part: the fix pass in `docs/reviews/review-perf-pilots.md` (C1, C2) replaced the product and all 9 hidden tests; read that section for the current task.

# coding-int level 1: performance task pilot (PLAN 2c item 5)

Kind `code`. One item added to `app/content/courses/coding-int/homework-1.json`: `h1-ticker-book`, item 2 of 10 (was 9; the AUTHORING limit is 12, so nothing was converted).

## Why this objective and this file

- Verb rule match: l2-prefix-trees, "Build a trie and use it for prefix search and word lookups." (the only objective in L1 that starts with a rule verb). The task asks for exactly that: build `TickerBook` on a trie (word lookup `has`, prefix search `count_prefix`) from a stub of `pass` bodies.
- Homework, not review: the task is difficulty 5 (a whole class from blank, `pace` 1200 s), and review items must be 2 to 4. Review items are also short numeric checks that a test-out draws 6 of; a 20-minute build does not fit there. The homework already holds the level's other code items.
- Unseen against the lesson: the lesson's `Trie` screen has insert, search, starts_with and count_prefix with a starter showing a list. The task adds `remove`, no-op rules (repeat add, absent remove), and a timing test, so it is not a copy of a solved screen.

## The item

- Prose: a desk's ticker search box; tickers listed and delisted all day.
- Widget: Python `code`, starter a stub (`class TickerBook` with five `pass` methods), `postlude` with `run_book(ops)` and `big_case(n=100000)` (a seeded 64-bit LCG, so no dependence on `random` across Python versions), 2 examples, 9 tests (examples are tests 1 and 2).
- Hidden tests: repeated add (3), removing an absent ticker and a prefix that is not a ticker (4), removing a ticker that begins another (5), empty book and empty prefix (6), re-adding after removal (7), lookups past the end of a ticker (8), 100,000 random steps within the 5 s case limit (9).
- `feedback.byKey` for tests 3, 4, 5, 7 and 9, each naming the slip.

## Numbers (all recomputed by `docs/reports/coding-int-1-perf-numbers.py`, exit 0)

| Figure | Value | How checked |
|---|---|---|
| Test expectations 1 to 8 | as in the file | three implementations: the item's solution (trie with node counts), a dict of prefix counts plus a set, a set with a scan per query |
| Test 9 | `[90388604, 5169, 18841]` | the solution and the prefix-dict reference |
| Starter fails every test | 9 of 9 | CPython; and in Pyodide (scratch copy, `solution` set to the starter: fails test 1) |
| Tests, examples | 9, 2 | counted from the file; examples equal tests 1 and 2 |
| "100,000 random steps" | `big_case` default `n` | read from the postlude signature |
| Scan work in test 9 | 30,086 count steps, 311,968,622 tickers scanned | counted by instrumenting the reference |
| Slips in byKey | tests 3, 4, 5, 7 | each slip planted in the solution fails first at its named test |
| Homework items | 10, one difficulty 5, one performance item | counted |

Timing: CPython 3.13, solution 0.22 s and scan 13.8 s on test 9. In Pyodide (scratch copy with the scan as `solution`) the scan passes tests 1 to 8 and stops at 5 s on test 9, so the timing test enforces a trie or an equivalent O(L) structure. A prefix-count dict or a sorted list with `bisect` also passes; grading is on behaviour.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors. No warning on `coding-int/homework-1.json`; the expected "coding-int/L1: has a performance task, remove from perf-pending" appears. `perf-pending.json` not edited.
2. `VOICE_BASE=app/content/courses/coding-int/ python3 docs/reviews/voice-scan.py --summary`: 0 explanations over three sentences, 0 sentences over 20 words.
3. `python3 docs/reports/coding-int-1-perf-numbers.py`: 0 failures, exit 0.
4. `node tools/playthrough.mjs --set coding-int/homework-1 --local-cdn <pkgs>`: ok, 10 of 10, 46 of 46 marks; with `--mobile` ok; with `--tablet` ok. Screenshots at 1280 and 440 of item 2 and the result page read cleanly (prose, question, stub and the `how` line fit; no sideways scroll).

Met hook, end to end: a scratch copy of the playthrough printed after submit `state.perf["coding-int/L1"] = { item: "h1-ticker-book", kind: "code", how: "auto" }` and `ZQ.prereq.perfPassed("coding-int", L1)` true.

`app/content/manifest.json` restored before the commit. No `course.json` change proposed. Backlog: 4 bullets under "Raised later (coding-int level 1 perf pilot):".
