# Topic 2.4 exam: contest practice

File: `app/content/exams/topic-2.4.json` (id `topic-2.4`, 60 minutes, pass 0.7). Minutes follow `examMinutes` in `learn.js`: topic 2.4 is 140 h, so 60 (see the backlog bullet).
Generator and checks: `scratchpad/exam-2.4/` (`items_a.py`, `items_b.py`, `items_c.py` and `common.py` build the file through `build.py`; `lib.py` holds the reference solutions and independent brute forces; `harness.py` (CPython), `pyo.mjs` with `pyo_run.py` (Pyodide 0.27.7 under Node), `variants.py` (wrong and slow versions), `search4.py`, `search25.py`, `check_*.py`, `lint.py`).

## Exit line

`docs/curriculum.md` 2.4 has no Exit line, only the Cover line: weekly contests once 100 problems are behind you, 1400 as a first-year target. The exam tests that: reading a statement into limits and a complexity, writing a correct fast solution, the contest maths and patterns a 1400 round asks for, and how to run a round (order, time caps, debugging, upsolving).

## Shape

26 items across levels 1 to 4 (all four levels, all five skills).

| Difficulty | Items | Share | Ramp |
|---|---|---|---|
| 2 | 5 | 19% | 20% |
| 3 | 13 | 50% | 50% |
| 4 | 5 | 19% | 20% |
| 5 | 3 | 12% | 10% |

Widgets: 8 numeric, 6 code (pure Python, one in script mode), 4 tap-regions (number-line, table rows, two grids), 3 multi, 2 choice, 1 table, 1 order, 1 longform.

| # | id | d | skills | widget / canvas |
|---|---|---|---|---|
| 1 | e-file-values | 2 | cn-reading | numeric, console statement (sum of n) |
| 2 | e-fast-read | 2 | cn-impl | choice with code options |
| 3 | e-lcm-rebalance | 2 | cn-maths | numeric |
| 4 | e-greedy-tap | 2 | cn-patterns | tap-regions, number-line intervals |
| 5 | e-upsolve-pick | 2 | cn-strategy | multi |
| 6 | e-next-problem | 3 | cn-strategy | tap-regions, table rows (scoreboard) |
| 7 | e-pop-front | 3 | cn-reading | numeric |
| 8 | e-budget-table | 3 | cn-reading | table |
| 9 | e-code-pairs | 3 | cn-impl, cn-reading | code, script mode (stdin and stdout) |
| 10 | e-inverse-solve | 3 | cn-maths | numeric |
| 11 | e-sieve-tap | 3 | cn-maths | tap-regions, grid |
| 12 | e-coin-parity | 3 | cn-maths | multi |
| 13 | e-fact-order | 3 | cn-maths | order |
| 14 | e-swap-cost | 3 | cn-patterns | numeric |
| 15 | e-submask-tap | 3 | cn-patterns | tap-regions, grid of masks |
| 16 | e-code-quiet | 3 | cn-patterns | code (difference array) |
| 17 | e-stress-gen | 3 | cn-impl | choice |
| 18 | e-penalty-order | 3 | cn-strategy | numeric |
| 19 | e-code-geom | 4 | cn-maths | code (geometric sum modulo p, n up to 10^18) |
| 20 | e-code-vans | 4 | cn-patterns | code (greedy, sort and two pointers) |
| 21 | e-code-conflicts | 4 | cn-patterns | code (bitmask subsets, n up to 16) |
| 22 | e-moves-back | 4 | cn-maths | numeric (walk back with Euclid) |
| 23 | e-hand-cases | 4 | cn-impl, cn-reading | multi, console code |
| 24 | e-code-book | 5 | cn-patterns | code (constructive, hidden checker) |
| 25 | e-best-plan | 5 | cn-strategy | numeric, table |
| 26 | e-round-review | 5 | cn-strategy, cn-reading, cn-impl | longform, 10-point rubric, full model answer |

Skill counts (items naming it): cn-reading 6, cn-impl 5, cn-maths 7, cn-patterns 7, cn-strategy 5. Lessons: l1 (1, 9, 23), l2 (1, 7, 8), l3 (2, 9), l4 (17), l5 (10, 13, 19), l6 (3, 11, 22), l7 (13), l8 (12, 22), l9 (24), l10 (4, 14, 20), l11 (15, 21), l12 (16), l13 (26), l14 (6, 18, 25), l15 (23), l16 (5, 26).

All statements are original. Quant framing: order batches, rebalancing cycles, replay drains, fund holdings, delta-neutral books, strategy conflicts, job completion times, round scoreboards.

## Code items

Run in CPython (`harness.py`) and in Pyodide 0.27.7 under Node (`pyo_run.py`), and through the app's own grader by the playthrough.

| item | tests | solution (CPython / Pyodide) | starter | wrong versions (each fails) |
|---|---|---|---|---|
| e-code-pairs | 7 | 7/7, 0.01 s / 0.02 s | fails all 7 | `input()` per line (3, 4, 7), split on newlines (3, 4, 7), double loop (7, stopped), `list.count` per value (7, stopped), string tokens with `/` (all) |
| e-code-quiet | 8 | 8/8, 0.2 s / 0.6 s | fails all 8 | range loop (7, 8 stopped), no spare cell (1 to 3, 5 to 8), `>=` (1, 5, 8), no `-v` (1, 4, 6 to 8), numpy slices (8, by the source check) |
| e-code-geom | 11 | 11/11, under 0.01 s | fails all 11 | no `g = 1` case (4, 8), loop over n (8 to 11, stopped), floor division (7, 11), no reduction (2, 3, 6, 7, 9 to 11), `n` without `% p` (8) |
| e-code-vans | 8 | 8/8, 0.1 s / 0.3 s | fails all 8 | neighbours in sorted order (1, 2, 6, 7), input order (1, 2, 7), heaviest with next heaviest (1, 2, 6, 7), partner scan (7, 8, stopped), missing last van (1, 3, 5) |
| e-code-conflicts | 10 | 10/10, 0.02 s / 0.06 s | fails all 10 | permutations (8 to 10, stopped), least-conflicted greedy (7), first fit (7 to 9), masks to `n - 1` bits (2, 3, 7, 8) |
| e-code-book | 8 | 8/8, 0.03 s / 0.2 s | fails all 8 | a zero for odd n (1, 3, 4, 6, 7), a wrong odd pattern (1, 4, 6, 7), search over combinations (6 to 8, stopped), running sum (4 to 8) |

Slow versions measured in Pyodide: the double loop on test 7 took 69 s and `list.count` 19.5 s, against the 5 s limit (two runs in parallel). The partner scan on 200,000 orders was still running after 120 s. The loop over $10^{18}$ terms, the permutation search at $n = 16$ and the combination search at $n = 199{,}999$ cannot finish. Every size case sits at least 4 times over the limit for its slow version and every correct solution at under 1 s.

Constructive item: `check_book` accepts any valid book (distinct, non-zero, absolute value at most n, sum 0, a list of ints) and demands `None` only for n = 1, which a search up to n = 7 confirmed is the only impossible size.

## Numbers computed twice

Each by a second method in `scratchpad/exam-2.4/` (CPython), and again in Pyodide through the playthrough.

- 1: sum of n, 200,000; the product trap is $10^4 \cdot 2 \cdot 10^5 = 2 \cdot 10^9$.
- 3: lcm(84, 90) = 1260 by `math.lcm` and by $84 \cdot 90 / 6$; gcd 6, product 7560.
- 4: all subsets of seven intervals searched (unique optimum B, D, G); the earliest-start greedy gives A, E and the shortest-first greedy B, F (2 each).
- 7: $\sum (m - 1) = n(n-1)/2 = 4{,}999{,}950{,}000$, and a simulated `pop(0)` count matches the formula for n = 1, 2, 5, 10.
- 8: $5000^2 = 2.5 \cdot 10^7$; $10^{10}$; $10^6 \log_2 10^6 = 19{,}931{,}568.6$; $2^{30} = 1{,}073{,}741{,}824$.
- 10: $x$ with $5x \equiv 3 \pmod{17}$ is 4 by search, by `pow(5, -1, 17)` and by $5^{15}$.
- 11: after crossing out multiples of 2, 3 and 5 up to 60 the only composite left is 49 (checked by trial division).
- 12: tails parity and heads parity are invariant; the other three change under one move (checked by enumeration).
- 14: completion totals 54 and 47, a fall of 7 (and $9 - 2$).
- 15: submasks of 1011 are 0, 1, 2, 3, 8, 9, 10, 11 (`v & 11 == v`), eight $= 2^3$.
- 17: with n from 1 to 6 and values to $10^9$ a pair sums to exactly k about 2.9 times per billion trials (pairs on average 5.83 over $2 \cdot 10^9$).
- 18: P then Q 1,938, Q then P 1,896, a gap of 42; losses 462 and 504.
- 22: BFS from (1, 1) gives 9 moves to (47, 30); walking back and the quotients 1, 1, 1, 3, 4 (sum 10, minus 1) agree.
- 25: all 4-problem subsets and orders by exact fractions: D, B, C scores 4,044 (1,632 + 1,196 + 1,216); rate greedy D, B, A 3,708; value D, C, B 3,900; letters A, B, C 3,372; the optimum is unique.
- 26 and 5: C opened at 41, ended at 120, so 79 minutes; 1,300 is 50 above 1,250.
- Code items: expected values come from the reference solutions and were checked against brute forces (`lib.py`): doubling and loops for the geometric sum, a bitmask DP for vans, subset search for conflicts, a combination search for the book, `numpy` for the 200,000-update count; `Counter` against the double loop for the pairs.

## Validation and playthrough

- `node tools/validate.mjs`: 0 errors overall, no warning for this file; the manifest lists `exams/topic-2.4.json`.
- Copy lint (`lint.py`: no `!` outside maths, no em-dashes, no sentence of 20 words or more, explanations of at most three sentences, no American spellings): clean. The word "program" is flagged by the American-spelling pattern and is the right word here.
- `playthrough.mjs --exam topic-2.4 --local-cdn`: 26 of 26, passed, desktop and `--mobile`.
- Screenshots reviewed (desktop and 390 px). Fixes made: code starters and docstrings rewrapped to at most 56 characters so the editor does not scroll sideways; the stress-test choice no longer puts the right answer first.
- Item 6's table and the number-line fit at 390 px. The 6 by 10 sieve grid is small on a phone but legible and tappable.

## Notes

- Time: 6 code items and a longform in 60 minutes is tight. The file follows `examMinutes`.
- The `--why` result screenshot is one page about 171,000 px tall, so it was not inspected as an image.
- Engine bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (exam 2.4)": large stdin inline, no import ban, exam minutes, small grid cells on a phone.
