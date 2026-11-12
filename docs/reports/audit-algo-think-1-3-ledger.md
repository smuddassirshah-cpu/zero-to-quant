# Claim ledger: algo-think L1 to L3 (round 1 blind audit, 12 Nov 2026)

Scope: `app/content/courses/algo-think/` l1 to l14, review-1 to review-3, homework-1 to homework-3 (Stage 1, full depth). Every row was judged by hand from a derivation, a named source or a run. "script" means a named check in `docs/reports/algo-think-L1-3-concepts.py` (CPython 3.13, 64-bit). "Pyodide" means a value read from the local Pyodide 0.27.7 build (Python 3.12.7, wasm32): `sys.getrecursionlimit()` is 1000, a float is 16 bytes, a list of 10^6 floats is 4,224,364 bytes, `max()` of an empty iterable says `max() iterable argument is empty`. All 41 Python code widgets were run under CPython with the recursion limit at 1000: every solution passes its tests and no starter does. `F n` points to finding n in `docs/reviews/audit-algo-think-1-3.md`.

Paths are shortened: `s3` is `screens[3]`, `q1` is `quiz[1]`, `i4` is `items[4]`; `w` is `widget`, `fb` is `feedback`, `ex` is `explain.text`.

Sources named: CLRS = Cormen, Leiserson, Rivest, Stein, *Introduction to Algorithms* (3rd ed.); Sedgewick and Wayne, *Algorithms* (4th ed.); Knuth, *The Art of Computer Programming* vols 2 and 3; Python docs (library reference, `sys`, `bisect`, `collections`, Sorting HOWTO); CPython `Objects/listobject.c`; Hull, *Options, Futures and Other Derivatives* (9th ed.); Kleinberg and Tardos, *Algorithm Design* ch. 4.

## l1-counting-work

| path | claim | verdict | basis |
|---|---|---|---|
| s0.prose, w.answer, accept | scan of 8 prices makes 7 comparisons | correct | script: l1 scan |
| s0.w.wrong | 8 = counted the first price; 2 = counted new bests (105, 108) | correct | best changes twice on the list; 8 = one per price |
| s0.hints, fb | loop is over `prices[1:]`, first price never compared | correct | reading of the code |
| s0.ex | work = count of basic operations; n prices give n-1 comparisons | correct | script; CLRS 2.2 |
| s1.w.answer | pair loop on 8 makes 28 = 7+6+...+0 | correct | script: l1 pairs |
| s1.w.wrong, fb.byKey | 64 = 8x8, 56 = both orders, 8 = outer only, 16 = added loops | correct | 8·8, 8·7, 8, 8+8 |
| s1.ex | pairs are four times the scan here, gap grows with n | correct | 28/7 = 4; n(n-1)/2 over n-1 = n/2 |
| s2 key, options, hints, fb | n = 1 and n = 0 give 0 comparisons; `range(1, 1)` and `range(0)` are empty | correct | script; Python `range` |
| s2.ex | formula gives 1·0/2 = 0; `prices[0]` raises `IndexError` on an empty list | correct | run |
| s3 table keys, hints, fb | scan 15, 31; pairs 120, 496; 8x15, 16x31 | correct | script |
| s3.ex | doubling n about doubles the scan and about quadruples the pairs | correct | 120/28 = 4.3, 496/120 = 4.1 |
| s4.prose, caption | Ana counts 7, Ben counts 11 (lines 1, 3, 4, 5) | correct | script: Ben counts 11 |
| s4 key, whys, hints | both grow like n; Ben at most 2(n-1)+2 | correct | one comparison and at most one assignment per price, plus two |
| s4.ex | a step is any basic operation; the choice changes the count by a constant factor | correct | CLRS 2.2 (RAM model) |
| s5 key, wrong, fb | full nested loop for n = 1,000 gives 10^6; 2,000, 1,000, 499,500 slips | correct | n·n; n+n; n; n(n-1)/2 |
| s5.ex | 64 cells for n = 8, not 16 | correct | 8·8 |
| s6.prose | forward pair loop n(n-1)/2; full nest n²; scan n-1 | correct | script |
| s6 key, whys | 4,950; 10,000 = 100²; 5,050 = 100+...+1; 9,900 = 100·99 | correct | arithmetic |
| s7 lines, ex | Gauss pairing: n columns each n-1, 2S = n(n-1) | correct | derivation in the lines |
| s8 solution, tests, fb.byKey | `count_pairs` and nine tests; slips 1 (pair with self), 6 (both orders), `>=` | correct | code run; 7·7 > 0 gives 1; 2·2 > 3 six ordered pairs |
| s8.ex | n(n-1)/2 multiplications; 1,225 for 50 | correct | 50·49/2 |
| s9 key, wrong, hints | 2,000 stocks: 1,999,000 pairs; slips 4,000,000, 3,998,000, 4,000 | correct | script |
| s9.ex | x 250 days about 5·10^8 multiplications; 5 times the stocks is 25 times the work | correct | script; (5n)² |
| summary | work as a function of n; n-1, n(n-1)/2, n²; constants do not change growth; nested loops multiply | correct | rows above |
| q0 | `for j in range(i)` gives 45 for n = 10; 100 and 55 slips | correct | 0+1+...+9 |
| q1 | sequential loops add: 1,000; 250,000 = nested | correct | 500+500 |
| q2 | 2,000 to 10,000 instruments: about 25 times the pairs; whys 5, 10, 125 | correct | script |
| q3 | `count_pairs([101.5], 0)` is 0, no `IndexError` | correct | code run |

## l2-big-o

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, wrong, hints, fb | 2^n exceeds n² for good from n = 5; tie at 2 and 4; 9 > 8 at 3 | correct | script |
| s0.ex | order for large n: 1, log n, n, n log n, n², 2^n | correct | CLRS 3.2 |
| s1 key, accept, wrong, hints | 3n²+50n+7 < 4n² from n = 51; 10,007 against 10,000 at 50; root 50.14; 17 is where 3n² passes 50n | correct | script; (50+√2528)/2 = 50.14; 50/3 = 16.7 |
| s1.ex | f = O(n²): bounded above by a constant times n² for large n; keep the fastest term, drop its constant | correct | CLRS 3.1 |
| s2 keys, hints, fb | A O(1), B O(n), C O(n²), D O(log n), E O(n log n) | correct | loop counts; halving and doubling take about log2 n steps |
| s3 keys, hints, fb | at 2,048: 11; 2,048; 22,528; 4,194,304 | correct | script |
| s3.ex | doubling n adds 1 to log n, doubles n, 2.2 times n log n, 4 times n²; the doubling test | correct | script; Sedgewick and Wayne 1.4 (doubling ratio) |
| s4 key, whys, hints, fb | at n = 20, B (400) beats A (1,000); tie at 50; A from 51 | correct | script |
| s4.ex | big O describes growth, not exact cost | correct | CLRS 3.1 |
| s5 key, whys, hints | 10^6 steps is O(1); scan 3n is cheaper below n = 333,334 | correct | script |
| s5.ex | O(1) means bounded, not small | correct | definition with g = 1 |
| s6.prose | f = O(g): constants c, n0 with f(n) <= c g(n) for n >= n0 | correct | CLRS 3.1 (non-negative f, g) |
| s6 key | 2n log n + 40n + 9 is O(n log n) | correct | 40n + 9 <= 49 n log2 n for n >= 2 |
| s6.options[3] product | O(n² log n) graded wrong: "You multiplied the terms" | imprecise | F6: it is a true bound under the screen's own definition; the tightest-class convention is never stated |
| s6.options[1], [2] whys | n log n outgrows any multiple of n; O(2n log n) is right but not simplified | correct | log n unbounded; constants drop |
| s6.ex | 2n log n passes 40n once log2 n > 20 | correct | script |
| s7 lines, ex | 50n <= 50n², 7 <= 7n² for n >= 1; c = 60, n0 = 1; any working pair proves it | correct | script |
| s8 solution, tests, fb | step counters; `cheaper` B below 50, tie at 50 and 0, A from 51 | correct | code run |
| s8.ex | counting steps gives the same answer on every machine | correct | counts are machine independent |
| s9 key, wrong | 5,000 x 500 = 2,500,000 calls; 5,500 and 1.25·10^9 slips | correct | arithmetic |
| s9.ex | a third loop over stocks gives 1.25·10^9, 500 times more; pandas keeps the class and shrinks the constant | correct | 2.5·10^6 · 500; vectorised code still visits every value |
| summary.ideas[0], [1], formula | upper bound on growth; drop constants; definition | correct | CLRS 3.1 |
| summary.ideas[2] | "Doubling n adds a constant to O(log n), doubles O(n), quadruples O(n²)" | imprecise | F6: true of log n, n and n², not of every function that is O(n²) |
| summary.trap | 50n against n²: quadratic wins below 50 | correct | script |
| q0 key, whys [2], [3] | fixed inner loop of 5: O(n); O(5n) is the same class | correct | 5n |
| q0.options[1] n2 | O(n²) graded wrong for 5n | imprecise | F6: 5n <= 5n², so it is a true (loose) bound |
| q1 | vectorising changes the constant, not the class | correct | every value still processed once |
| q2 | O(n²): 4 minutes at 10,000 rows, about 16 at 20,000; whys 8, 4, 64 | correct | (2n)² = 4n² |
| q3 | halving loop: 20 steps at 10^6, 21 at 2·10^6 | correct | script: floor(log2 n)+1 |

## l3-memory

| path | claim | verdict | basis |
|---|---|---|---|
| s0.prose (program A), caption, key, whys, hints, ex | A "holds 1 extra value"; extra space O(1) for A | wrong | F1: `for p in prices[1:]` copies n-1 references; script and Pyodide show the peak growing ten-fold with n |
| s0 (program B), ex | B appends every price: O(n) extra space; extra space = memory beyond the input | correct | list of n; CLRS 2.1 ("in place"), Sedgewick and Wayne 1.4 |
| s1 key, wrong, hints, fb | dict holds one entry per distinct key: 4; 8 and 3 slips | correct | VOD, BARC, AZN, LLOY |
| s1.ex | worst case every trade is a new ticker: O(n) | correct | at most n keys |
| s2 key, wrong, hints, fb | in-place reverse of 1,001 makes 500 swaps; 1,001, 501, 1,000 slips | correct | script: floor(n/2) |
| s2.ex | in place: `lo`, `hi` and one value in flight, O(1); `prices[::-1]` builds a new list | correct | slice semantics, Python docs (sequence types) |
| s3 solution, tests, how, fb | `stream_mean` with two numbers; iterators have no `len` or indexing; empty feed gives `None`; peak under 50,000 bytes | correct | code run; Pyodide peak 256 bytes |
| s3.ex | storing 100,000 floats takes megabytes | correct | 100,000 x 32 bytes = 3.2 MB (2.0 MB on wasm32) |
| s4.prose, console | `getsizeof(xs)` 8,448,728 and a float 24 bytes on 64-bit | correct | script |
| s4 key, wrong, hints, fb | list plus floats about 32.4 MB; 8.4, 24, 0.024 slips | correct | script |
| s4.ex | about 32 bytes per float; the page's Python is a 32-bit build, about 20 bytes a float | correct | Pyodide: 4,224,364 + 16·10^6 bytes = 20.2 bytes each |
| s5.prose, caption | `pre[k]` = sum of the first k values; `[0, 3, 4, 8, 9, 14]`; slice sum is O(n) per question | correct | script |
| s5.hints[1] | "Days 1 to 3 total 8 - 3: `pre[4] - pre[1]`" | wrong | F2: `pre[4]` is 9; 9 - 3 = 6; 8 - 3 = 5 |
| s5 solution, tests, hints[0], [2], fb, ex | `pre[j] - pre[i]`; n+1 numbers, O(n) space, O(1) per query | correct | code run; script |
| s6 key, whys, hints, fb, ex | `final_value` keeps n+1 values: O(n); a running product is O(1); append does not copy the list each time | correct | list length; l4 amortised analysis |
| s7 key, wrong, hints, fb | `total([5,3,8,1,4])` is 21 with 6 calls open | correct | script |
| s7.ex | recursion n deep uses O(n) space; Python allows about 1,000 open calls, so 5,000 raise `RecursionError` | correct | Pyodide: limit 1000, `total(range(5000))` raises |
| s8.prose, key, whys, ex | O(1): running statistics, in-place swap; O(n): copy, intermediates, dict of n keys, recursion n deep; `prices[::-1]` O(n), `reverse()` in place | correct | Python docs (`list.reverse`, slicing) |
| s9.prose, key, wrong, hints, fb, ex | 4,914,000 values per stock; 200 stocks: 7.86 GB as float64, 31.45 GB as lists; 0.98, 0.039 slips | correct | script |
| summary | extra space definition; O(1) and O(n) lists; 32 against 8 bytes; trap | correct | rows above |
| q0 | a generator is used up by `sum`; `max` then raises `ValueError`; message text | correct | script; Pyodide message |
| q1 | weekday dict has at most 5 keys: O(1) | correct | bounded key set |
| q2 key, whys | mean and variance need count, sum, sum of squares; Var = Σx²/n − x̄² | correct | script (population variance) |
| q2.ex | "(Libraries use Welford's update, ...)" | imprecise | F21: NumPy's `var` is two-pass (mean, then squared deviations); Welford is one option, Knuth vol 2 4.2.2 |
| q3 | 10^7 ticks x 32 bytes = 320 MB; 80 MB as float64 | correct | arithmetic |

## l4-cheap-on-average

| path | claim | verdict | basis |
|---|---|---|---|
| s0.prose, caption data, key, wrong, hints, fb | capacity 1, doubling: the 9th append copies 8; totals 0,0,1,3,3,7,7,7,7,15 | correct | script |
| s0.ex | "`list.append` works this way, with a slightly smaller growth factor" | imprecise | F8: CPython grows by about 1.125 (script; `listobject.c` `list_resize`) |
| s1 keys, hints, fb, ex | totals 0, 1, 3, 7, 15 at n = 1, 2, 4, 8, 16; n-1 at powers of two | correct | script |
| s2 key, wrong, hints, fb | 15/16 = 0.9375 copies per append; 8, 15, 3.75 slips | correct | arithmetic |
| s2.ex | amortised cost = average over a whole sequence; append is amortised O(1) | correct | CLRS 17.1 (aggregate method), 17.4 |
| s3 key, wrong, hints, fb | 1,000 appends: 1,023 copies, 1.023 each; 10 resizes; 512, 1,023, 102.3 slips | correct | script |
| s3.ex | worst single append O(n) but rare; n appends cost O(n) | correct | script: total < 2n |
| s4 lines, hints, fb, ex | full at 1, 2, ..., 2^(m-1) < n; sum 2^m - 1 < 2n | correct | script |
| s5.prose, key, whys [1], [2], fb, ex | tripling is still amortised O(1); total under 1.5n; about log3 n resizes | correct | script |
| s5.options[3] why | "Tripling resizes less often, so it copies less in total" | imprecise | F7: false at n = 4, 28 to 32, 244 to 256 (script); true of the bounds 1.5n and 2n |
| s6 solution, tests, canvas, hints, fb, ex | `total_copies`: 7 at 5, 15 at 16, 31 at 17, 127 at 100, 1,023 at 1,000, 2,047 at 1,025; under 2 each | correct | script |
| s7 key, wrong, hints, fb | grow by 10: 49,500 copies for 1,000; 99, 1,023, 990, 50,500 slips | correct | script |
| s7.ex | about n²/20; fixed growth makes n appends O(n²) | correct | script |
| s8 key, wrong, hints, fb | draining 1,000 with `pop(0)`: 499,500 shifts | correct | script |
| s8.ex | `pop(0)` is O(n); `deque.popleft()` is O(1) | correct | Python docs (`collections.deque`; TimeComplexity wiki) |
| s9 table, key, wrong, hints, fb, ex | 2,000,000 ticks: 2,097,151 copies, 1.05 a tick; last resize at 2^20 + 1; 0.52 slip | correct | script |
| summary | geometric sum below 2n; amortised O(1); fixed growth and `pop(0)` are O(n²) | correct | rows above |
| q0 key, whys, ex | `np.append` in a loop is O(n²); call k copies k-1 elements, total n(n-1)/2 | correct | NumPy docs: `append` returns a copy |
| q0.fb.correct, options[2], [3] whys | "1 + 2 + ... + n copies" | imprecise | F9: disagrees with the explain's n(n-1)/2 by n |
| q1 | worst of 100 appends copies 64, at append 65; 99, 127, 128 slips | correct | script |
| q2 key, whys | `deque(maxlen=500)` is O(1) at both ends; `pop(0)`, `insert(0, p)` are O(n) | correct | Python docs |
| q3 | first append to capacity 1 copies 0 | correct | script |

## l5-calls-itself

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, hints, fb, ex | only `fact(0)` returns without calling; answers 1, 1, 2, 6, then 24 | correct | trace |
| s1 keys, hints, fb, ex | `sum_list` returns 0, 3, 4, 8 | correct | trace |
| s2.prose | base case and recursive case defined | correct | CLRS 2.3; Sedgewick and Wayne 1.1 |
| s2 key, whys, hints, fb, ex | base `len(xs) == 1` fails on `[]` with `IndexError` | correct | run |
| s3 key, whys | wrong recursive cases give `RecursionError`, 9, 7 | correct | script |
| s3.ex | each call moves one step towards `[]`; answers 0, 3, 4, 8 | correct | trace |
| s4 key, whys, hints, fb, ex | dropping the recursive answer returns 4 | correct | trace |
| s5 solution, tests, hints, fb, ex | `sum_list`, `power`; x^0 = 1; 0^0 taken as 1 | correct | code run; Python `0 ** 0 == 1` |
| s6 console, key, whys, hints, fb | base `n == 1`: `fact(0)` runs to -1, -2, ... and raises `RecursionError`; no limit would be enough | correct | run |
| s6.ex | limit of 1,000 frames; use `n == 0`, 0! = 1 | correct | Pyodide limit 1000 |
| s7 pattern, key, whys, ex | `f(n - 2)` from 3 skips 0; safe base `n <= 0` | correct | trace 3, 1, -1 |
| s8 lines, hints, fb, ex | induction: base right, step right, so every n | correct | mathematical induction |
| s9 solution, tests, hints, fb, ex | `total_pnl` over nested dicts; 395.75; empty folder gives 0 | correct | code run; script |
| summary | base case, progress towards it and landing on it, combining; fact(0) = 1 | correct | rows above |
| q0 | `count([5, 5])` is 3 because the base returns 1 | correct | trace |
| q1 | `grow(3)` = 1157.625; 1150 and 1102.5 slips | correct | script |
| q2 | bond recursion gives 97.2768; par when coupon equals the rate | correct | script; Hull ch. 4 (bond pricing) |
| q3 key, whys, ex | `-1 // 2 == -1`, so `f(-1)` never ends; 1000 reaches 0 in ten halvings | correct | script; 1000, 500, ..., 1, 0 |

## l6-call-stack

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, hints, fb, ex | last call in is the first out | correct | LIFO; Python execution model |
| s1 states, whys, hints, fb, ex | push 3, 2, 1, 0; pop 0, 1, 2, 3 with values 1, 1, 2, 6 | correct | trace |
| s2.prose | frame = a call's own variables and resume point; push on call, pop on return | correct | Python reference 4.1 (execution frames) |
| s2 key, wrong, hints, fb, ex | `fact(5)` peaks at 6 frames; n+1 in general | correct | trace |
| s3.prose | `sys.getrecursionlimit()` returns 1000; deeper calls raise `RecursionError` | correct | Pyodide; Python docs `sys` |
| s3 key, whys, hints, fb, ex | a loop needs one frame; a second base case saves one frame | correct | trace |
| s3.options[1] why, fb.byKey.limit; s7.options[1] why | a huge limit lets the real stack overflow and Python can crash | correct | Python docs `sys.setrecursionlimit`: "a too-high limit can lead to a crash" |
| s4.prose, key, whys, hints, fb, ex | tail call defined; Python does not reuse frames for tail calls | correct | CPython has no tail-call elimination (van Rossum, "Tail Recursion Elimination", 2009) |
| s5 key, whys, hints, fb, ex | each frame has its own `total`; returns 4 | correct | trace |
| s6 solution, tests, how, hints, fb | `depth(n)` = deepest stack of `fib(n)`: 1, 1, 2, 5, 15, 12 | correct | script |
| s6 caption, ex | `fib(5)`: 5 frames deep out of 15 calls; a local would be fresh in every frame | correct | script |
| s7.prose | frames are LIFO; about 1,000 allowed; no tail-call reuse; explicit stack pattern | correct | rows above |
| s7 key, fb | a list as a stack can grow as deep as memory allows | correct | heap allocated list |
| s7.ex | "it visits in the same last-in, first-out order as the recursion" | imprecise | F12: depth first both, but the loop takes children in reverse (script) |
| s8 lines, hints, fb, ex | `fact(2)`: push 2, 1, 0; pop 0, 1, 2 with 1, 1, 2 | correct | trace |
| s9 solution, tests, hints, fb | `levels` = 1 + deepest child; 4 for the fund; 500-deep chain | correct | code run |
| s9.ex | stack as deep as the levels; a 10,000-day recursive backtest needs 10,000 frames | correct | one frame per day |
| summary | frames, LIFO, depth, limit about 1,000, loops for deep work; n+1 frames | correct | rows above |
| q0 | recursive backtest over 10,000 days raises `RecursionError` near day 1,000 | correct | limit 1000 |
| q1 | `var_95()` returns first | correct | LIFO |
| q2 | `sum_list` on 6 items peaks at 7 frames | correct | lengths 6 to 0 |
| q3 key, options[2], ex | `inner` raises `NameError: name 'n' is not defined` | correct | run |
| q3.options[1] why | "Each frame sees only its own names and the module's" | imprecise | F13: enclosing function scopes and built-ins are also visible (Python reference 4.2.2; script) |

## l7-split-in-half

| path | claim | verdict | basis |
|---|---|---|---|
| s0 keys, hints, fb, ex | halves return 7 and 9, whole 9 | correct | trace |
| s1.prose | divide and conquer: split, solve halves the same way, combine | correct | CLRS 4 |
| s1 key, whys, hints, fb, ex | `mid = 3`; calls on 0..3 and 4..7; no overlap, both smaller | correct | (0+7)//2 |
| s2 key, wrong, hints, fb, ex | 15 calls on 8; n base cases and n-1 splits: 2n-1 | correct | script |
| s3.prose, key, wrong, hints, fb, ex | inversion defined; `[3,1,4,2]` has 3: (3,1), (4,2), (3,2) | correct | script |
| s4 key, wrong, hints, fb, ex | halving 1,024 to 1 takes 11 calls = log2 n + 1 | correct | 2^10 |
| s5.prose | x^n = (x^(n/2))² even, x·(x^((n-1)/2))² odd; costs 1 and 2 | correct | Knuth vol 2 4.6.3 (binary method) |
| s5 solution, tests, how, fb | `power_fast` counts 4, 3, 41, 14; 30 levels for 10^9; missing `* x` gives 81 | correct | script; 9·9 = 81 |
| s5.ex | reusing `h` matters: two calls on `n // 2` undo the saving | correct | T(n) = 2T(n/2)+1 is O(n) (l8 s8) |
| s6 key, whys, hints, fb, ex | right half from `mid` never shrinks on two items: `RecursionError` | correct | mid = 0, call repeats 0..1 |
| s7.prose, key, whys, ex | halves must not overlap and both be smaller; 31 calls on 16 | correct | script |
| s8 lines, hints, fb, ex | `power_fast(2, 5)`: 5 needs 2, 2 needs 1, 4, then 4·4·2 = 32; 3 multiplications | correct | script |
| s9.prose, key, wrong, hints, fb, ex | 1.0002^252 about 1.0517; 12 multiplications (7 squarings, 5 extra); 16 for 2,520; 8, 251, 252, 14 slips | correct | script |
| summary | split, solve, combine; `lo..mid`, `mid+1..hi`; depth near log2 n; 41 multiplications for 10^9 | correct | script |
| q0 | `max` runs n-1 = 7 times on 8 | correct | script |
| q1 | `max_rec(xs, 1, 1)` returns `xs[1]` = 99.8 | correct | base case |
| q2 | recursive merge of 3 and 4 makes at most 6 comparisons | correct | script (all 5,040 interleavings) |
| q3 | four subtotals take 3 additions; each machine 249,999 | correct | k numbers need k-1 additions |

## l8-cost-of-recursion

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, hints, fb, ex | `fib(5)`: `fib(2)` three times, `fib(3)` twice, 15 calls, answer 5 | correct | script |
| s1.prose, key, wrong, hints, fb, ex | recurrence defined; T(n) = T(n-1)+1, T(1) = 1 gives T(n) = n | correct | script; CLRS 4 |
| s2 keys, hints, fb, ex | T(n) = 2T(n/2)+n: each level costs 8, 4 levels, T(8) = 32; T(2) = 4, T(4) = 12 | correct | script |
| s3 key, wrong, hints, fb, ex | T(n) = T(n/2)+1: 21 at 2^20; log2 n + 1 | correct | script |
| s4.prose | naive `fib` costs at most T(n) = 2T(n-1)+1 | correct | script: C(n) <= 2^n - 1 |
| s4 key, wrong, hints, fb | T(10) = 1,023 = 2^10 - 1; 20, 1,024, 19, 512 slips | correct | script; 2·10, 1+2·9 |
| s4.ex | levels 1, 2, ..., 2^(n-1); O(2^n); `fib` grows about 1.618 a step | correct | script |
| s5.prose, solution, tests, how, hints, fb | C(n) = 1+C(n-1)+C(n-2); 15, 177, 75,778,124,746,287,811; memoised `fib` | correct | script |
| s5.ex | C(n) = 2F(n+1) - 1; memoised `fib(n)` is O(n) calls; memoisation defined | correct | script |
| s6 key, whys, hints, fb | T(n) = 2T(n/2)+n is O(n log n), not O(2^n): log2 n + 1 levels of n | correct | script; CLRS 4.4 |
| s6.ex | "`fib`'s ... tree is n levels deep and doubles on each" | imprecise | F10: levels of `fib(5)` hold 1, 2, 4, 6, 2 (script) |
| s7 lines, hints, fb, ex | level k: 2^k calls of size n/2^k; T(n) = n(log2 n + 1) | correct | script |
| s8.prose | four recurrences and their classes; the master theorem packages the halving cases | correct | CLRS 4.5 |
| s8 key, whys, ex | T(n) = 2T(n/2)+1 = 2n-1, O(n); this is `max_rec` | correct | script |
| s8.fb.correct | "1 + 2 + ... + n = 2n - 1" | imprecise | F11: as written that is the arithmetic series, n(n+1)/2; the levels are 1, 2, 4, ..., n |
| s9.prose, key, wrong, hints, fb | non-recombining tree 2^(n+1) - 1 nodes; recombining step k has k+1; 5,151 at 100 steps | correct | script; Hull ch. 13 (binomial trees) |
| s9.ex (first two sentences) | (n+1)(n+2)/2 is O(n²); 2^101 - 1 about 2.5·10^30 | correct | script |
| s9.ex (last sentence) | "So every practical pricer recombines; the course Binomial trees builds one" | imprecise | F19: non-recombining trees are used where the model forces them (Hull ch. 21, cash dividends; ch. 32, HJM); the course is named Pricing with Trees |
| summary | recurrence, tree method, levels, memo makes `fib` O(n) | correct | rows above |
| q0 | T(n) = T(n/2)+1 derivation, O(log n) | correct | script |
| q1 key, whys, ex | `sum_list` makes n+1 calls, O(n) calls; slicing copies as extra work | correct | chain of lengths n to 0 |
| q2 | memoised `fib(30)` makes 59 calls; naive 2,692,537 | correct | script |
| q3 | T(16) = 80; 64, 32, 256 slips | correct | script |

## l9-halving

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, hints, fb, ex | the middle cell (7 or 8) rules out the most whatever its value; index 7 holds 35 | correct | worst side is about half |
| s1 states, whys, hints, fb | lo/hi/mid trace 7, 11, 13, 12; four looks | correct | trace |
| s1.ex | cells in play 16, 8, 4, 1; a scan would take 13 | correct | index 12 |
| s2.prose, table, key, wrong, hints, fb, ex | worst case floor(log2 n)+1 looks: 1, 5, 10, 20 | correct | script |
| s3 solution, tests, how, hints, fb, ex | `binary_search` with `lo <= hi`, `mid ± 1`; -1 when absent; at most 45 reads on 10^6 | correct | code run; 20 passes |
| s4.prose, states, whys, hints, fb, ex | first index with `xs[i] >= 4`: `hi = mid` keeps mid, `lo = mid + 1` drops it; answer 1 | correct | trace |
| s5 solution, tests, how, fb | `first_at_least` equals `bisect_left`; `len(xs)` when all smaller | correct | script |
| s5.ex | `bisect_right` is the same with `<=`; both O(log n) | correct | Python docs `bisect`; CPython `Lib/bisect.py` |
| s6 key, whys [2], [3], hints, fb, ex | `lo = mid` stalls with two cells left; Python integers do not overflow; a correct search returns 3 | correct | trace; Python `int` |
| s6.options[1] why | with `<=` this loop also keeps running at `lo == hi` | correct | both updates leave the range unchanged |
| s7.prose | invariant; at most ceil(log2(n+1)) passes | correct | script |
| s7.options[1] why | "With `<=` ... `hi = mid` changes nothing, so it never ends" | imprecise | F14: it spins only when `xs[mid] >= target`; at `lo == hi == len(xs)` it raises `IndexError` (script) |
| s7 key, options[2], fb | `hi = mid` pairs with `lo < hi`; `hi = mid - 1` with `lo <= hi` | correct | termination argument |
| s7.ex | mixing loops for ever or skips a cell; `lo + (hi - lo) / 2` in C or Java | correct | Bloch, "Nearly All Binary Searches and Mergesorts are Broken" (2006) |
| s8 key, wrong, hints, fb, ex | `bisect_left` 3, `bisect_right` 6; strictly below and at or below; one O(n log n) sort then O(log n) each | correct | script |
| s9 solution, tests, hints, fb | `next_trading_day` by `bisect_left`; `None` past the end; ISO strings sort in date order; 7 March 2026 is a Saturday | correct | code run; `datetime.date(2026, 3, 7).weekday() == 5` |
| s9.ex | 12 looks over ten years of days | correct | script |
| summary | halving, invariant, bisect pair, floor(log2 n)+1, trap | correct | rows above |
| q0 | unsorted `[8,3,12,5,20]`: returns -1 after looking at 12 and 8 | correct | script |
| q1 | 5,000 strikes: 13 looks | correct | script |
| q2 | prints `1 4`; difference 3 counts the 3s | correct | script |
| q3 | `first_at_least([5,5,5,5], 5)` is 0; `hi` goes 2, 1, 0 | correct | trace |

## l10-search-the-answer

| path | claim | verdict | basis |
|---|---|---|---|
| s0.prose, key, hints, fb, ex | impact 0.15√q per cent is the lesson's own model; 1% at q = 44.44; one crossing because it rises | correct | script; stated as "our impact model" |
| s1 states, whys, hints, fb, ex | bisection 32, 48, 40, 44, 46, 45; six tries among 65 sizes; 65, 32, 16, 8, 4, 2, 1 | correct | script |
| s2.prose | predicate; monotone = False then True and never back; binary search finds the first True | correct | definition; CLRS exercise 2.3-5 generalised |
| s2 key, whys, hints, fb, ex | savings 120 + 35d is monotone; peak day and first close below £95 are not | correct | counterexamples in the whys |
| s3 solution, tests, how, hints, fb, ex | `smallest_true` with marker `hi + 1`; `None` when nothing works; about 40 calls for 10^12; never calls outside | correct | script |
| s4.prose, solution, tests, hints, fb, ex | integer square root = one less than the smallest x with x² > n; range to n+1; about 60 steps for 10^18 | correct | script (against `math.isqrt`) |
| s5.prose, caption | 4% five-year annual bond: 95.67 at 5%, 91.58 at 6%; price falls as yield rises | correct | script; Hull ch. 4 |
| s5 solution, tests, hints, fb | yield bisection to a penny; `None` above 120.00 or below the price at 100%; 5.16% in 15 halvings | correct | script |
| s5.ex | over reals stop at a tolerance; each halving halves the bracket | correct | bisection method; Burden and Faires 2.1 |
| s6 key, whys, hints, fb, ex | `closes[d] > 100` is F F T F F T T T; search returns 5; `max(closes[:d+1]) > 100` is monotone | correct | script |
| s7.prose, key, whys, fb, ex | about log2(hi - lo + 2) calls; 30 for 10^9 | correct | script |
| s8.prose, key, whys [1], [2], hints, fb | Black-Scholes call rises with σ; c(0.20) = 10.45, c(0.25) = 12.34, c(0.30) = 14.23; keep [0.20, 0.25] | correct | script; Hull ch. 15, 19 (vega > 0) |
| s8.options[3] why | "The tolerance asks for a penny" | imprecise | F22: this screen states no tolerance |
| s8.ex | twenty halvings give σ about 0.2411; Newton is faster but bisection cannot diverge | correct | script; Burden and Faires 2.1, 2.3 |
| s9.prose, key, wrong, hints, fb | largest passing rate = one less than smallest failing; next test 3,250 | correct | midpoint of 2,500 and 4,000 |
| s9.ex (second sentence) | 11 tests pin the limit to one order a minute | correct | script: 1500/2^11 < 1 |
| s9.ex (last sentence) | "Testing every rate from 1,000 up would take hundreds" | imprecise | F15: at least 1,501 tests (script) |
| summary | first True without a list; marker `hi + 1`; tolerance; ceil(log2(range)); trap | correct | rows above |
| q0 | `smallest_true(1, 100, 120 + 35d >= 1000)` is 26; 25, 29 slips | correct | script; 1000/35 = 28.6 |
| q1 | all False gives `None`, not 50, 51 or 0 | correct | marker |
| q2 | 20 halvings for 10^-6 | correct | script |
| q3 | `n + 1` needed only for n = 0 and 1 | correct | script |

## l11-sorting-by-hand

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, wrong, hints, fb, ex | 7 and 9 shift; 6 drops in after 5 | correct | trace |
| s1 states, whys, hints, fb, ex | inserting 1: four comparisons, four shifts | correct | trace |
| s2.prose, keys, hints, fb, ex | insertion sort; comparisons 1, 2, 1, 4, 4 = 12; a key costs one per value passed plus one stopping test | correct | script |
| s3 solution, tests, how, hints, fb, ex | counts 12, 0, 0, 4, 10, 5, 9, 3; input unchanged; `>` not `>=`; the `break` stops the walk | correct | script; code run |
| s4 key, wrong, hints, fb, ex | nearly sorted list: 9; sorted input n-1, O(n) | correct | script |
| s5.prose, key, wrong, hints, fb, ex | reversed input: key i costs i; 499,500 at 1,000; worst n(n-1)/2, O(n²); best n-1 | correct | script (max over all permutations of 7 is 21); CLRS 2.2 |
| s6 key, whys, hints, fb, ex | no early stop: 15 comparisons on 6 sorted values; with `else: break`, 5 | correct | 1+2+3+4+5 |
| s7.prose | worst n(n-1)/2, sorted n-1, in place; `sorted` is Timsort, O(n log n) | correct | CPython `Objects/listsort.txt` |
| s7 key, whys, fb, ex | stable with `>`; not with `>=` | correct | script; CLRS 8.2 (stable sorting defined) |
| s8 solution, tests, hints, fb | `sort_trades` comparing times only; tuples would order ties by id | correct | code run |
| s8.ex | nearly sorted input is close to O(n); `sorted(key=...)` is stable and fast on runs | correct | Python Sorting HOWTO; `listsort.txt` |
| s9.prose, key, wrong, hints, fb | inserting 99.975: 4 comparisons, 3 shifts; binary search would take 10 looks | correct | script; ceil(log2 1001) = 10 |
| s9.ex | "New levels usually land near the touch" | unverified | U1: unsourced market remark; the sorted-low-to-high list also puts only one side's touch at the end |
| summary | rows above; O(n) when nearly sorted; trap | correct | script |
| q0 | `[3, 1, 2]`: 3 comparisons | correct | script |
| q1 key, whys, ex | fastest on sorted input; random input walks about halfway, still O(n²); reverse about 50 million at 10,000 | correct | script (mean over permutations); 10,000·9,999/2 |
| q2 | `insertion_sort([42])` is `([42], 0)` | correct | code run |
| q3 | `sorted` is O(n log n) in the worst case, O(n) on ordered input, stable; no sort beats O(n) | correct | `listsort.txt`; every value must be read |

## l12-merge-sort

| path | claim | verdict | basis |
|---|---|---|---|
| s0 states, whys, hints, fb, ex | merge takes the smaller front; copy the tail; 8 values, at most 7 comparisons; linear | correct | script |
| s1.prose, key, wrong, hints, fb, ex | merge sort defined; 8 values need 3 levels; 7 merges | correct | log2 8; 4+2+1 |
| s2 solution, tests, hints, fb, ex | `merge` with `<=`, tails by `extend`; at most n-1 comparisons | correct | script; code run |
| s3 solution, tests, fb, ex | `merge_sort`; base `len(xs) <= 1`; 20,000 reversed values would cost insertion sort 2·10^8 | correct | script |
| s4 key, whys, hints, fb, ex | `[A]`, `[B, C]`: B, A, C; stable with `<=`, not with `<` | correct | script |
| s5 key, whys, hints, fb, ex | base only at the empty list: `[7]` splits into `[]` and `[7]` for ever; rounding up moves the problem | correct | 1 // 2 = 0 |
| s6.prose, lines, hints, fb | T(n) = 2T(n/2)+n; level k costs n; log2 n merging levels; O(n log n) | correct | CLRS 2.3.2 |
| s6.ex | 3 levels x 8 = 24 against 28; a million: 20 levels against half a trillion; O(n) extra memory | correct | script |
| s7.prose, caption | inversion = pair ranked in opposite order; 3 of 15; Kendall's rank correlation counts them | correct | Kendall (1938); script |
| s7 solution, tests, how, hints, fb | count during the merge: add `len(left) - i` on a right take; ties are not inversions; 99,930,366 | correct | script (independent count) |
| s7.ex | tau = 1 - 2·3/15 = 0.6; counted in bulk | correct | script (tau-a, no ties) |
| s8 solution, tests, hints, fb, ex | `merge_logs` comparing times with `<=`; whole tuples would break ties by venue name | correct | code run; `'CXE' < 'LSE'` |
| s9 key, whys, hints, fb | external sort: sorted runs, then a merge from the fronts; joining runs end to end is not sorted | correct | Knuth vol 3 5.4 |
| s9.ex | memory holds a buffer per run; databases sort large tables this way | correct | Knuth vol 3 5.4; PostgreSQL docs (`work_mem`, external merge) |
| summary | linear merge; log2 n levels of n; stable, O(n log n) on every input, O(n) extra memory | correct | CLRS 2.3 |
| q0 | merge without tails returns `[1, 2, 3]` | correct | trace |
| q1 | 40 and 25: at most 64 comparisons | correct | script |
| q2 | 1 s at 10^6, a little over 2 s at 2·10^6 (ratio 2.1) | correct | script |
| q3 key, whys, ex | faster than insertion sort, O(n) extra memory, stable | correct | CLRS 2.3 |

## l13-quicksort

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, wrong, hints, fb, ex | pivot 5: 2, 4, 1 go left; pivot ends at index 3 | correct | script |
| s1.prose, states, whys, hints, fb, ex | Lomuto scheme; six comparisons, three swaps, final swap; `[2,4,1,5,9,8,7]` | correct | script; CLRS 7.1 |
| s2.prose, key, whys, hints, fb, ex | recurse on `lo..p-1` and `p+1..hi`; no merge; leaving the pivot out guarantees shrinking | correct | CLRS 7.1 |
| s3 solution, tests, how, hints, fb, ex | `partition` on a sub-range; all-equal values return `hi` | correct | script; code run |
| s4 solution, tests, how, hints, fb | random-pivot `quicksort` in place; fixed last pivot on 3,000 sorted values goes 3,000 deep | correct | code run; script (999 deep at 1,000) |
| s4.ex | "the expected cost is O(n log n) on every input" | imprecise | F4: needs distinct values; all-equal input costs n(n-1)/2 with this partition whatever the draw (script) |
| s4.ex (last sentence) | in place, using only the recursion's stack | correct | CLRS 7 |
| s5.prose, key, wrong, hints, fb, ex | sorted 7 with last pivot: 21 comparisons, the maximum; n(n-1)/2; recursion n deep; 12 on the shuffled example | correct | script |
| s6 key, whys, hints, fb | first pivot on 2,000 sorted prices: 2,000 deep, 1,999,000 comparisons, `RecursionError` | correct | script |
| s6.ex (first sentence) | "Real data often arrives sorted or nearly sorted" | unverified | U2: unsourced empirical remark |
| s6.ex (second sentence) | random pivot or median of three makes even splits likely | correct | Sedgewick and Wayne 2.3 |
| s7.prose | average O(n log n), worst O(n²), in place, not stable | correct | CLRS 7.2, 7.4 |
| s7.w.options[0] (key), question | random pivot: "every input has expected cost O(n log n)" | imprecise | F4: false for inputs with many equal values under Lomuto, as the same screen's explain concedes |
| s7.options[1..3] whys, fb, ex | sorted and reverse-sorted hurt a fixed end pivot only; many equal values are the hard case; three-way partition fixes it | correct | script; Sedgewick and Wayne 2.3 (3-way partitioning) |
| s8.prose, solution, tests, how, hints | `quickselect`: keep the side holding k; exact; 5003 | correct | script; CLRS 9.2 |
| s8.fb.correct, ex | "about 2n comparisons on average"; "about 2 million steps" for the median of a million | imprecise | F17: the median costs about 3.4n = 2(1 + ln 2)n (script, exact recurrence; Knuth, "Mathematical Analysis of Algorithms", 1972) |
| s8.ex (first sentence, class) | quickselect keeps one side; average O(n) | correct | CLRS 9.2 |
| s9.prose | 95% VaR = loss at the 5th percentile of P&L | correct | Hull ch. 22 |
| s9 table, key, whys [1], [2], hints, fb | full sort about 230 million comparisons at 10^7; quickselect 2n to 4n; exact, not approximate | correct | script |
| s9.options[3] why, ex | introsort: quicksort switching to heapsort; used by C++ `std::sort` and .NET; caps the worst case at O(n log n) | correct | Musser (1997); libstdc++ `stl_algo.h`; .NET `Array.Sort` docs |
| summary.ideas, formula | pivot final; fixed end pivot on sorted data O(n²); quickselect O(n) average; n(n-1)/2 | correct | rows above |
| summary.formula.note | average splits give about 1.39 n log2 n | correct | 2n ln n; script (2(n+1)H_n - 4n matches the simulation) |
| q0 | `[2, 1]`: p = 0, `[1, 2]` | correct | script |
| q1 | last pivot on 1,000 sorted values: 499,500 | correct | script |
| q2.prose, key, whys, ex | "Quicksort with Lomuto" on three trades gives c, b, a | imprecise | F5: true with the last value as pivot; the lesson's own random-pivot version also gives c, a, b (script) |
| q3 key, whys, ex | three distinct values in a million: three-way partition; Lomuto puts ties on one side, O(n²); two or three levels | correct | script (all-equal run); Sedgewick and Wayne 2.3 |

## l14-best-step-now

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, wrong, hints, fb | 87p in 5 UK coins | correct | script (dynamic programme) |
| s0.ex | for UK coins largest-first always gives the fewest | correct | script: greedy = optimum for every amount to 1,000, past the Kozen-Zaks bound (largest two coins summed) |
| s1 key, wrong, hints, fb, ex | coins 1, 3, 4: 6 needs 2, greedy uses 3 | correct | script |
| s2.prose, table, key, wrong, fb, ex | greedy defined; counts 1,2,1,1,2,3,2,2,3,4; beaten at 6 and 10 only; right for 8 of 10; a reason is needed, not examples | correct | script |
| s3 solution, tests, how, hints, fb | `coins_greedy`; `None` when stuck; 5,000 coins for 10^6 | correct | code run |
| s3.ex | optimal for UK coins, not for 1, 3, 4 or 1, 10, 25: it depends on the coin system | correct | script (condition stated) |
| s4.prose, key, wrong, hints, fb, ex | seven meetings, at most 4 (B, C, E, F); touching is allowed | correct | script (brute force) |
| s5 solution, tests, how, hints, fb, ex | earliest finish first with `s >= last_end`; O(n log n) sort plus O(n) walk | correct | script |
| s6 key, whys, hints, fb, ex | sorting by start returns 1; shortest first fails on (1,5), (4,7), (6,10); earliest finish is always optimal | correct | script; CLRS 16.1 |
| s7.prose, lines s1, s2, s4, s5, ex | exchange argument: some largest schedule starts with the first to finish; repeat on the rest | correct | CLRS theorem 16.1; Kleinberg and Tardos 4.1 |
| s7.lines[2] | "Every other meeting of O starts after o ends" | imprecise | F18: touching is allowed here, so "when o ends or later" |
| s8.prose, key, wrong, hints, fb | fractional greedy gives £460; whole trades: £400 (B and C) beats greedy's £300 | correct | script |
| s8.ex | fractional knapsack: greedy by ratio is optimal; 0/1 is not; dynamic programming for 0/1 | correct | CLRS 16.2 |
| s9.prose, key, wrong, hints, fb | filling from the cheapest ask costs £100,031; 100,020 and 100,045 slips | correct | script; mean of four levels x 1,000 |
| s9.ex | cheapest first is optimal for one order, by exchange | correct | any other fill swaps a cheaper share for a dearer one |
| s10.prose | S_p = (S1 + S2)/√(2 + 2ρ) for equal weights and equal volatility | correct | derivation: mean σ(S1+S2)/2, sd (σ/2)√(2+2ρ); script simulation |
| s10 key, whys, hints, fb, ex | A and C 1.77 beats A and B 1.47; B and C 1.70 | correct | script |
| summary | greedy defined; a counterexample sinks it; exchange argument; interval scheduling always optimal in O(n log n) | correct | CLRS 16.1 |
| q0 | coins 1, 10, 25, amount 30: greedy 6, fewest 3 | correct | script |
| q1 | `max_meetings([])` 0; touching pair 2 | correct | code run |
| q2 | fractional knapsack: 38; 30 and 48 slips | correct | script |
| q3 | examples can refute a greedy rule, never prove it | correct | logic of universal claims |

## review-1, homework-1

| path | claim | verdict | basis |
|---|---|---|---|
| review-1 i0 | triple loop: 190 pairs x 3 = 570; 1,200, 190, 8,000 slips | correct | 20·19/2·3 |
| review-1 i1 | 5n² + 40n log n + 1,000 is O(n²) | correct | fastest term |
| review-1 i2 key, whys | timings 2, 8, 32 s fit O(n²); exponential would square per doubling | correct | 2^(2n) = (2^n)² |
| review-1 i3 | `sorted` builds a new list: O(n) extra | correct | Python docs `sorted` |
| review-1 i4 | generator O(1) extra, list comprehension O(n); both O(n) time | correct | Python reference 6.2.8 |
| review-1 i5 | 65 appends: 127 copies, below 2n = 130 | correct | script |
| review-1 i6 | capacity 100 growing by 100: 4,500 copies; O(n²) overall | correct | script |
| review-1 i7 | 2,000 to 6,000 stocks: about 90 minutes | correct | 17,997,000/1,999,000 = 9.0 |
| homework-1 i0 | 124,750 pairs x 250 = 31,187,500; slips | correct | arithmetic |
| homework-1 i1 | `i *= 3` loop: ceil(log3 n) steps, O(log n); bases differ by a constant | correct | 3^k >= n |
| homework-1 i2 | start 4, doubling, 100 appends: 124; 127, 252, 64 slips | correct | script |
| homework-1 i3 lines, ex | tripling total below 3n/2; factor r gives below r/(r-1) n | correct | script (integer r) |
| homework-1 i4 | sliding mean: O(1) per tick, O(k) space | correct | deque of k |
| homework-1 i5 solution, tests, how, fb, ex | `best_trade` in one pass; 10, 5, 0, 8, 299,999; pair loop about 2·10^10 | correct | code run; 200,001·200,000/2 |
| homework-1 i6 solution, tests, fb | `copies_fixed`: 49,500; 4,500; 10; 49,999,500,000; n²/(2·step) | correct | script |
| homework-1 i6.ex | "against about 2 × 10^6 with doubling" | wrong | F3: a million appends with doubling make 1,048,575 copies (script) |
| homework-1 i6.ex (last sentence) | fixed growth is O(n²) in total, whatever the step | correct | script |
| homework-1 i7 model, rubric | 8,997,000 calls; 2.25·10^9 day-steps; O(n²d); tuples about 90 to 100 bytes, close to 1 GB; sort O(n² log n); heap of k; 80 minutes | correct | script; 64 + 24 + 8 bytes; Python docs `heapq.nlargest` |

## review-2, homework-2

| path | claim | verdict | basis |
|---|---|---|---|
| review-2 i0 | base returning 0 zeroes every product; the empty product is 1 | correct | convention for empty products |
| review-2 i1 | `sum_list([])` returns first | correct | LIFO |
| review-2 i2 | `power_fast(x, 100)`: 8 multiplications, 7 calls | correct | script |
| review-2 i3 | T(n) = T(n-1)+1 gives n, O(n) | correct | script |
| review-2 i4 | `grow(3)` = 530.604; 530 and 520.2 slips | correct | 500·1.02³ |
| review-2 i5 | 6 frames for n = 50; 30 for 10^9; 51 for plain `power` | correct | script |
| review-2 i6 | missing odd case: `power_fast(3, 3)` returns 9 | correct | 3² |
| review-2 i7 | C(7) = 41 = 2·21 - 1 | correct | script |
| review-2 i8 key, whys, ex | `max_rec`: T(n) = 2T(n/2)+1, O(n); levels 1, 2, 4, ..., n | correct | script |
| review-2 i8.fb.correct | "1 + 2 + ... + n = 2n - 1 units" | imprecise | F11: same notation as l8 s8 |
| homework-2 i0 | `flatten` recursive; 300 lists deep | correct | code run |
| homework-2 i1 | `count_calls(5)` returns 1 | correct | each frame has its own `calls` |
| homework-2 i2 | 7 crossing inversions, 14 in all | correct | script |
| homework-2 i3 | T(n) = 2T(n-1)+1 = 2^n - 1; T(3) = 7 | correct | script |
| homework-2 i4 | T(n) = 2T(n/2)+n² is O(n²), below 2n² | correct | script; CLRS 4.5 case 3 |
| homework-2 i5.prose, solution, tests, how, fb | `sort_count`; 200 million pairs for 20,000; 4,498,500; 99,930,366 | correct | script |
| homework-2 i5.ex (second sentence) | "the merge already compares each pair that matters" | misleading | F16: 64 reversed values have 2,016 inversions counted with 192 comparisons; the count is done in bulk because the left half is sorted |
| homework-2 i5.ex (rest) | T(n) = 2T(n/2)+n, O(n log n); this is merge sort | correct | CLRS 2.3 |
| homework-2 i6 | explicit-stack `total_value`; 340.25; 5,000 deep | correct | code run |
| homework-2 i7 | `max_rec(xs, 0, 999)`: 11 frames, 1,999 calls | correct | script |
| homework-2 i8 model, rubric | C(m) = 2C(m-1)+1, C(0) = 1: 2^(n+1) - 1; 2,097,151 at n = 20; about 1.4·10^76 at 252; (n+1)(n+2)/2 = 231 nodes; depth n+1; loop with n(n+1)/2 updates equals the recursive price | correct | script; Hull ch. 13 |
| homework-2 i9 solution, tests, fb, ex | `split_feed`; `[[]]` for the empty feed; 927 and 4,374 splits; at most 2^(n-1) | correct | script |

## review-3, homework-3

| path | claim | verdict | basis |
|---|---|---|---|
| review-3 i0 | `lo <= hi` with `hi = mid` on `[10, 20]`, 15 loops for ever | correct | trace: lo = hi = 1, xs[1] = 20 >= 15 |
| review-3 i1 | insertion sort on `[4,3,2,1,5]`: 7 | correct | script |
| review-3 i2 | 1.05^n >= 2 first at 15; rule of 72 gives 14.4; 1.05^14 = 1.98 | correct | script |
| review-3 i3 | Lomuto on `[3,8,2,5,1,4]`: p = 3, `[3,2,1,4,8,5]` | correct | script |
| review-3 i4 | `merge_unique` with a third case for equal fronts; one pass | correct | code run |
| review-3 i5 key, whys | earliest finish first is always optimal; 1, 5, 12 fails at 15; whole trades are 0/1 knapsack; shortest first fails | correct | script; CLRS 16.1, 16.2 |
| review-3 i6 | `bisect_right(high) - bisect_left(low)` counts both ends; 0 when `low > high` | correct | script |
| review-3 i7 | `max_size` = smallest breaking size minus one; edge cases `hi` and `None`; 4000, 2316 | correct | script |
| review-3 i8 key, whys, ex | stable and O(n log n): merge sort or `sorted`; quicksort not stable; insertion sort O(n²) | correct | `listsort.txt`; CLRS 2, 7 |
| homework-3 i0 | 27 halvings for 10^-8 | correct | script |
| homework-3 i1 key, whys | 1, 5, 12 fails; 1, 2, 5, 10; powers of 3; 1, 5, 10, 25 are safe for greedy | correct | script (to 2,000, past each Kozen-Zaks bound) |
| homework-3 i2 | stable: insertion with `>`, merge with `<=`, `sorted`; not Lomuto quicksort, not `>=` | correct | script |
| homework-3 i3 | C(n) = (n-1) + C(n-1), C(1) = 0: n(n-1)/2; 1,999,000 at 2,000 | correct | script |
| homework-3 i4 | `min_capacity` by search on the answer between `max` and `sum`; 15, 6, 3, 18, 10, 32, 25,534; O(n log total) | correct | script |
| homework-3 i5 | `merge_k` in rounds: O(N log k); one at a time is O(Nk); ceil(log2 k) rounds | correct | CLRS exercise 6.5-9 bound; code run |
| homework-3 i6 solution, tests, fb | `kth_largest` = index n-k by quickselect on a copy; 8005 | correct | script |
| homework-3 i6.ex | "the expected work is about 2n" | imprecise | F17: about 3n at the 20th percentile, 3.4n at the median (script) |
| homework-3 i7 model (a) | "worst case is O(n²) unless the pivot is random or chosen by median-of-medians" | imprecise | F20: a random pivot makes O(n²) unlikely, not impossible; only median-of-medians rules it out (CLRS 9.2, 9.3) |
| homework-3 i7 model (a) rest, (b), (c), (d), rubric[0], [2..6] | sort about 2.3·10^8; quickselect 2n to 4n; nested selects; sort once then bisect, about 24 comparisons each, 12,000 for 500; 500 scans 5·10^9, twenty times more; first pivot on ordered input 5·10^13 and 10^7 deep; stability not needed | correct | script; CLRS 9 |
| homework-3 i7 rubric[1] | "how a random pivot avoids it" | imprecise | F20 |
| homework-3 i8 solution, tests, fb, ex | rotated sorted ring: one side of `mid` is always in order; `ring[lo] <= ring[mid]`; O(log n) reads; slot values 62,983, 162,983 | correct | code run (exhaustive sweep to 12 slots in the widget's own postlude); arithmetic on the test ring |

## Totals

Rows: 376. correct 346, wrong 3, imprecise 24, misleading 1, unverified 2.
