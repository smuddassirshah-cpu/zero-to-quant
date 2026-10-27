# contests level 1 (How contests work): report

## Files written

All in `app/content/courses/contests/`. `l1-reading-statements.json` was kept as triaged (not edited). Skills: `cn-reading` for l2, `cn-impl` for l3 and l4; the sets also use `cn-strategy` (homework routine and write-up).

| File | Screens / items | Code screens |
|---|---|---|
| `l1-reading-statements.json` | 12 screens, 4 quiz items (unchanged) | `parse`, `new_highs` |
| `l2-limits-to-complexity.json` | 12 screens, 4 quiz items | `budget_class`, `pair_sums_at_most` |
| `l3-fast-io.json` | 12 screens, 4 quiz items | `read_tokens`, problem S as a Python script, problem S in C++ |
| `l4-stress-testing.json` | 10 screens, 4 quiz items | `stress`, `brute_pair_sums` plus `test_against_brute` under real pytest |
| `review-1.json` | 9 items, difficulty 2 to 4, all four lessons interleaved | none |
| `homework-1.json` | 8 items, difficulty 3 to 5 (one 5) | `count_pairs` (4), `longest_window` (5), `range_sums` (4); `order` routine; `longform` write-up with a 10-point rubric |

Shape per lesson: hook, explore (l2 a log-log `plane` with a log slider and `derive` caption; l3 an `array` stepper over the tokens; l4 a `console` with a `frames` control through stress trials), name, ladder, trap, generalise, code, transfer, summary, quiz.

- l2 hook is Laaksonen chapter 2's maximum-subarray example with three solutions. Its third solution is $O(n)$ (Kadane), not $O(n \log n)$ as the brief says, because no natural $n \log n$ version exists. Ladders: $n \le 20$, $n \le 5{,}000$, a value up to $10^{18}$ with many queries, and the sum-of-$n$ bound. Trap: `x not in seen` on a list. Edge case: quiz 1, where $n \le 100$ allows brute force. Transfer: "what are the constraints?" in an interview. PyPy 3 is named on the name screen and on ladder E.
- l3: the name screen orders the fast template. Ladders: a grid of strings (bytes tokens), printing many lines, and the C++ `std::endl`. Trap: values spread over several lines, read with `input().split()`. Edge cases: no final newline and blank lines (code tests, quiz 3), and bytes tokens (quiz 4). Transfer: `sync_with_stdio` in a C++ interview, plus market-data replays.
- l4: hook is a verdict list to tap. Ladders: generator range and shrinking. Trap: a brute force that shares the fast code's helper. Edge case: many valid answers need a checker (generalise screen, quiz 4). Transfer: a vectorised backtest against a slow loop.

Generators and checkers are in `/tmp/claude-0/-home-user-zero-to-quant/3e0ee4d9-5633-56bc-b89e-00d7263b2d42/scratchpad/contests-1/`:
- builders: `common.py`, `build_l2.py`, `build_l3.py`, `build_l4.py`, `build_sets.py`
- solutions: `lib.py`; l4's hidden prelude is `l4pre.py`
- test harness: `harness.py` (CPython), `pyo.sh` with `pyrun.mjs` (Pyodide 0.27.7 under node)
- other checks: `variants.py` (wrong solutions), `cppcheck.py` (clang++ locally), `speed.py` (timings), `bt.py` (backtest trace), `counter_check.py`

Every test `expect` is computed by running the solution in `lib.py`, not typed by hand.

## Validator

`node tools/validate.mjs` (from `app/`): 0 errors. The only contests warning is the existing l1 ladder canvas-kind warning (screen 7 switches from `array` to `console`). That file is triaged and was left unchanged.

## Playthrough

Command: `node tools/playthrough.mjs --lesson ... --set contests/review-1 --set contests/homework-1 --local-cdn <scratchpad>/pkgs --shots ... --mobile --why`. Everything passed.

- l1: 15 checks, quiz 4/4
- l2: 16 checks, quiz 4/4
- l3: 16 checks, quiz 4/4 (includes the C++ compile)
- l4: 14 checks, quiz 4/4
- review-1: 9 of 9 recorded
- homework-1: 8 of 8 right, 37 of 37 marks

l2, l3 and l4 were replayed alone after the last edits, and all passed.

I checked the screenshots (desktop, 390 px, and the Why? sheets). Fixes made:
- l2 plane: x range cut to $2 \cdot 10^5$, so the Python line's label no longer collides with the $n \log_2 n$ curve.
- Statement subscripts written with Unicode rather than `a_l`.
- Hook option code re-indented to two spaces, so every line is at most 25 characters (the inbox notes clipping past about 33 at 390 px).
- l4 stress table: case column widened and `compact` set.
- Why? states fixed for the l3 stepper and the l4 explore.

Code checks, CPython 3.13 and Pyodide 0.27.7 under node:
- Every solution passes all its tests in both.
- Every starter fails.
- Wrong versions fail the intended tests:
  - l2: brute force fails 8 (count) and 9 (size); `<` fails 1, 3, 5 to 7 and 9; sort-then-brute fails 9; `budget_class` without the guard stops on test 15; the table-row version fails 3, 6, 7 and 9.
  - l3 C++ (clang++ locally): an `int` sum fails 3 and 6; a maximum started at 0 fails 1 and 4 to 7.
  - l4 `stress`: without a copy it fails 9; reseeding every trial fails 2, 3, 5 and 9.
  - l4 pytest screen: a brute force that calls `pair_sums_at_most`, or a missing assert, fails 6 to 10. Four different generators all catch every planted bug, except that a positive-only generator misses test 10's negative-$k$ bug, which the prose rules out.
  - Homework: brute force fails 9 to 11; `xs[i+1:].count` fails 10 and 11; a set instead of counts fails 2, 7, 10 and 11; restart windows fail 9 and 11; slice sums fail 6.

## Harness and complexity enforcement

`code.js` gives each case its own 5 s limit, not a pooled budget, contrary to the brief's course context. l1's title screen says so, and l2 to l4 rely on it: a size case stops on its own row.

Each `how` line says which way a test enforces complexity: by size (200,000 values), by counting (`_Counted`), or both.

What the counter sees, checked in both CPython and Pyodide on a 100-item list:
- Counted: `__getitem__` and `__iter__`. A `for` loop, `sorted`, `enumerate`, `sum`, `max`, `set` and an index loop each count 100.
- Counted as 1: a slice.
- Not counted: `in`, `index`, `count`, `sort()` and `len`.

So every counting test is paired with a size test. Homework P's `xs[i+1:].count(k - x)` and Q's `sum(xs[l-1:r])` pass the counter and are stopped only by size.

## Numbers stated, with sources

All computed in CPython (`lib.py` and inline scripts) and again in Pyodide through `pyo.sh` or the playthrough. Timings are measured, quoted as "about", and no test depends on a time.

**Speeds, measured in this sandbox.** The brief's figures were 1.6 s and 4.3 s for $10^7$ additions on a busier machine.

| Measurement | CPython | Pyodide (node) |
|---|---|---|
| $10^7$ additions | 0.32 s | 1.08 s |
| `sorted` of $2 \cdot 10^5$ ints | 0.039 s | 0.061 s |
| $10^6$ dict insertions | 0.10 s | 0.096 s |

Reading $2 \cdot 10^5$ lines:
- CPython, real stdin, best of 7, twice: `input()` per line 0.14 s, `sys.stdin.buffer.read().split()` 0.04 s.
- In the app's harness style (StringIO), CPython: 0.053 s and 0.026 s.
- The same in Pyodide: 0.19 s and 0.06 s.

Printing $10^5$ lines:
- CPython to a pipe: `print` loop 0.17 s, `sys.stdout.write` loop 0.08 s, `join` 0.01 s.
- Pyodide with StringIO: 0.066 s and 0.024 s.

C++ (g++ -O2, $10^6$ numbers in and out, to a file): 0.86 s with neither fast line, 0.12 s with both, 0.54 s with both plus `std::endl`, and 0.90 s with `endl` alone.

Lesson code runs in the browser:
- Pyodide: largest l2 case about 0.4 s; homework cases up to 1.6 s (mostly generating 600,000 random ints).
- Whole lessons in the playthrough: 30 to 92 s.

**l2**
- Hook: $n^3/6 \approx 1.33 \cdot 10^{15}$; $n(n+1)/2 = 2.00001 \cdot 10^{10}$.
- Explore: $(10^4)^2 = 10^8$; $\sqrt{10^7} = 3{,}162$; $n \log_2 n$ reaches $10^8$ at $n = 4{,}523{,}071$; at $2 \cdot 10^5$ it is $3.52 \cdot 10^6$.
- Table: $2^{20} = 1{,}048{,}576$; $500^3 = 1.25 \cdot 10^8$; $5{,}000^2 = 2.5 \cdot 10^7$.
- Problem D: $2^{20} \cdot 20 = 20{,}971{,}520$.
- Problem E: $5{,}000 \cdot 4{,}999 / 2 = 12{,}497{,}500$.
- Problem F: $\lceil \log_2(10^9 + 1) \rceil = 30$ ($2^{30} = 1{,}073{,}741{,}824$); $2 \cdot 10^5 \cdot 30 = 6 \cdot 10^6$.
- Problem G: $(2 \cdot 10^5)^2 = 4 \cdot 10^{10}$; $10^4 \cdot 20^2 = 4 \cdot 10^6$; $10^4 \cdot (2 \cdot 10^5)^2 = 4 \cdot 10^{14}$.
- Trap: $n^2/2 = 2 \cdot 10^{10}$.
- Generalise: $10^6 \log_2 10^6 = 1.99 \cdot 10^7$.
- `budget_class` boundaries:
  - $2^n$ fits up to 26 ($2^{26} = 67{,}108{,}864$; $27^3 = 19{,}683$).
  - $464^3 = 99{,}897{,}344$ fits; $465^3 = 100{,}544{,}625$ does not.
  - $n = 500$ gives `"n^2"`; the lesson explains why that differs from the table.
  - $n^2$ fits up to $10^4$, $n \log n$ up to $4{,}523{,}071$, and $n$ up to $10^8$.
- `pair_sums_at_most`: size case (seed 5, $n = 2 \cdot 10^5$, $k = 0$) gives 10,053,378,714. Counting case (seed 11, 1,000 values): the solution makes 1,000 reads, the brute force 999,000, and the answer is 259,120. 20,000 random small cases agree with the brute force.
- Transfer: $5 \cdot 10^{11}$ pairs. Quiz: $100^3 = 10^6$; $400^3 = 6.4 \cdot 10^7$; $\log_2 10^6 = 19.93$.

**l3**
- Explore: the third test case's $n$ is at index 6.
- Problem S tests:
  - test 3 sums to $3 \cdot 10^9$ (past `int`)
  - test 6 sums to $5 \cdot 10^9$ and $-2 \cdot 10^9$
  - test 7 is seed 3: $10^4$ cases with $n$ from 1 to 3 and values from −9 to 9 (69,521 characters in, 49,258 out)
- `read_tokens`: 200,000 tokens sum to 19,999,900,000.

**l4**
- Generator `gen_pairs` with seed 1: the `<` bug first fails on trial 5, `[4, 10, 2, 6, 1, 1]` with $k = 2$ (fast 0, brute 1).
- First failures for other seeds:

  | Seed | Trial | Case | Fast | Brute |
  |---|---|---|---|---|
  | 2 | 2 | `[3, 5, 5]`, $k = 8$ | 0 | 2 |
  | 3 | 7 | `[8, 10, 7]`, $k = 15$ | 0 | 1 |
  | 4 | 3 | `[5, 1, 4, 9, 9]`, $k = 13$ | 5 | 7 |
  | 5 | 1 | `[5, 6, 9, 1, 8]`, $k = 9$ | 2 | 3 |

- Values up to $10^9$ found nothing in 100,000 trials on seeds 1, 2, 3 and 7. Values from 1 to 3 found the bug within 7 trials on the same seeds.
- Without a copy, the in-place version returns `[1, 1, 2, 4, 6, 10]`.
- Backtest trace (`bt.py`, seed 4): the vectorised P&L drops the last day. It gives −£1.50 and £0.00 on trials 1 and 2, then £0.00 against £1.25 on the path £100, £98.50, £98, £99.25, £100.50.
- Quiz: `[2, 3, 3]` with $k = 6$ gives 3, or 2 with `<`.

**Review**
- $10^{18}$; $2{,}000^2 \log_2 2{,}000 = 4.39 \cdot 10^7$ against $8 \cdot 10^9$.
- `pos` = 5.
- `[5, 5, 1]` with $k = 10$ gives 3, or 2 with `<`.
- $10^4 \cdot 10^6 = 10^{10}$; $4 \cdot 10^{10}$; $10^5 \cdot 20 = 2 \cdot 10^6$.

**Homework**
- `count_pairs`: counting case (seed 21) is 1,000 reads against the brute force's 999,000; size case (seed 22) gives 9,998,990; 200,000 sevens give $\binom{200000}{2} = 19{,}999{,}900{,}000$.
- `longest_window`: counting case is 1,000 reads against 500,500; seed 31 (8 tickers, $k = 4$) gives 22; alternating tickers give 200,000.
- `range_sums`: seed 41, checked by length, first, last and sum.
- Other items: rebuilt set $4 \cdot 10^{10}$; count-in-range about $7 \cdot 10^6$.
- Model write-up: its mistake (a count that reaches 0 but is never deleted) was verified. A stress run on seed 1 crashed it on trial 1, `['C', 'A', 'B']` with $k = 1$.
- 5,000 random small cases each for `count_pairs` and `longest_window` agree with the brute forces.

## Conventions

- Problems are original Codeforces-style statements in `console` canvases, lettered A to W across the level, with Mira's P&L as the running legend. Money is in £.
- l4's hidden prelude (`gen_pairs`, `brute_pairs`, `fast_ok`, `fast_strict`, `fast_in_place`) is shared by the explore trace and the `stress` tests, so seed 1 tells the same story on both screens.
- The pytest screen copies the postlude from `pytest/l5-empty-one-many.json` verbatim, and its planted wrong functions live in the prelude.
- This app's runner gives the program text input. So l3's script reads `sys.stdin.read()`, and the prose says to use `sys.stdin.buffer.read()` on Codeforces (see backlog).

## Proposed change to course.json

None.

## Backlog

Seven bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (contests level 1)":
- `sys.stdin.buffer` is missing in script mode.
- Output costs too little in the harness to show the print-loop gap.
- The validator rejects table `wrong[]` text ids.
- Log-scale plane tick labels clip.
- The array stepper's `step` patch keeps the opening caption.
- The read counter misses `count`, `in` and slices.
- Large stdin and expected output must be inline.
