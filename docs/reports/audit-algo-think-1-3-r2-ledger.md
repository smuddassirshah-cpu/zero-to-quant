# Claim ledger: algo-think L1 to L3, round 2 blind audit (13 Nov 2026)

Stage 1 course, full ledger depth. Files: `l1` to `l14`, `review-1` to `review-3`, `homework-1` to `homework-3` in `app/content/courses/algo-think/`.
Written blind, before any earlier review, audit, report or script for this course was opened.

Basis key. **S** = a named check in `docs/reports/algo-think-L1-3-r2-concepts.py` (CPython 3.13.18 and Pyodide 0.27.7 / Python 3.12.7, same results). **H** = all 41 code widgets run in Pyodide 0.27.7: solution passes every hidden test, starter fails (harness described in the audit file). **D** = derivation given in the row. Sources: CLRS = Cormen, Leiserson, Rivest, Stein, *Introduction to Algorithms* (3rd ed.), by chapter; SW = Sedgewick and Wayne, *Algorithms* (4th ed.); KT = Kleinberg and Tardos, *Algorithm Design*; Hull = *Options, Futures and Other Derivatives*; PyDoc = docs.python.org (3.12) page named; `listsort.txt` and `listobject.c` are in the CPython source.

Verdicts: correct, wrong, imprecise, misleading, unverified.

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l1 | screens[0].widget.answer | scan of 8 prices makes 7 comparisons | correct | S `l1 scan 7` |
| l1 | screens[0].widget.wrong[counted-start] | 8 counts the first price, which is never compared | correct | D: loop is over `prices[1:]` |
| l1 | screens[0].widget.wrong[counted-new-best] | 2 is the number of times the best changed | correct | S (105 and 108) |
| l1 | screens[0].hints, feedback | first price starts as best; one comparison per later price | correct | D |
| l1 | screens[0].explain | counting basic operations measures work; scan makes n - 1 | correct | CLRS 2.2 |
| l1 | screens[1].widget.answer | pair loop on 8 makes 28 = 7 + 6 + ... + 0 | correct | S `l1 pair loop` |
| l1 | screens[1].widget.wrong[] | 64 = 8 x 8; 56 both orders; 8 outer only; 16 loops added | correct | D: 8^2, 8 x 7, 8, 8 + 8 |
| l1 | screens[1].explain | pairs are four times the scan here; gap grows with n | correct | S `28 is four times 7` |
| l1 | screens[2].widget.options | n = 1 and n = 0 both give 0 comparisons; `range(1, 1)` and `range(0)` are empty | correct | S |
| l1 | screens[2].explain | formula gives 1 x 0 / 2 = 0; `prices[0]` raises IndexError on `[]` | correct | S `IndexError` |
| l1 | screens[3].widget.rows | scan 15, 31; pairs 120, 496 | correct | S |
| l1 | screens[3].feedback.byKey | 8 x 15 = 120 and 16 x 31 = 496 by pairing ends | correct | D |
| l1 | screens[3].explain | doubling n roughly doubles the scan, quadruples the pairs | correct | D: 7, 15, 31; 28, 120, 496 |
| l1 | screens[4].prose | Ana 7, Ben 11 (1 + 7 + 2 + 1) | correct | S `Ben counts 11` |
| l1 | screens[4].widget.options, hints | Ben's count at most 2(n - 1) + 2; both grow like n | correct | S |
| l1 | screens[4].explain | a step is any basic operation; choices differ by a constant factor | correct | CLRS 2.2 (RAM model) |
| l1 | screens[5].widget.answer, wrong[] | 1000 x 1000 = 10^6; slips 2000, 1000, 499500 | correct | D |
| l1 | screens[5].explain | nested loop fills an n by n grid: 64 for 8 | correct | D |
| l1 | screens[6].prose, options | (n-1) + ... + 0 = n(n-1)/2; 4950, 10000, 5050, 9900 | correct | S |
| l1 | screens[7].widget.lines | Gauss pairing: n columns each n - 1, so 2S = n(n - 1) | correct | D |
| l1 | screens[8].widget (code) | `count_pairs` solution and 9 tests; test-3, test-4, test-5 feedback | correct | H; D: `[7]` self-pair gives 1, both orders 6, 5 x 3 = 15 not above |
| l1 | screens[8].explain | n(n-1)/2 multiplications; 1,225 for 50 | correct | S |
| l1 | screens[9].widget.answer, wrong[] | 1,999,000; slips 4,000,000, 3,998,000, 4,000 | correct | S |
| l1 | screens[9].explain | about 500 million multiplications; 5 times the stocks is 25 times the work | correct | S |
| l1 | summary | work as a function of n; n - 1, n(n-1)/2, n^2; loops add only in sequence | correct | D |
| l1 | quiz[0] | triangle loop gives 45; slips 100 and 55 | correct | S |
| l1 | quiz[1] | sequential loops add: 1,000 | correct | D |
| l1 | quiz[2].widget, explain (figures) | 25 times; 5 x 10^7 against 2 x 10^6 | correct | S |
| l1 | quiz[2].explain.text (last sentence) | a daily job over 10,000 instruments "cannot afford" a further loop over n | unverified | no source; 5 x 10^11 steps is minutes in compiled code. Finding 8 |
| l1 | quiz[3] | `count_pairs([101.5], 0)` is 0; no IndexError | correct | H |
| l2 | screens[0].widget.answer, wrong[] | 2^n ahead of n^2 for good from n = 5; ties at 2 and 4; 9 > 8 at 3 | correct | S |
| l2 | screens[0].explain | order for large n: 1, log n, n, n log n, n^2, 2^n | correct | CLRS 3.2 |
| l2 | screens[1].widget.answer, wrong[] | 3n^2 + 50n + 7 < 4n^2 from 51; 10,007 v 10,000; 10,360 v 10,404; 17 | correct | S |
| l2 | screens[1].hints[2] | n > 50.14 | correct | S |
| l2 | screens[1].explain | O(n^2): bounded above by a constant times n^2 for large n | correct | CLRS 3.1 |
| l2 | screens[2].widget.rows | A O(1), B O(n), C O(n^2), D O(log n), E O(n log n) | correct | S `snippet D`; D |
| l2 | screens[2].explain | halving or doubling up to n takes about log2 n steps | correct | S |
| l2 | screens[3].widget.rows | 11; 2,048; 22,528; 4,194,304 | correct | S |
| l2 | screens[3].explain | doubling adds 1 to log n, doubles n, 2.2 times n log n, quadruples n^2; ratio test reads the class | correct | S; D (a heuristic: n and n log n differ by 2 against 2.2) |
| l2 | screens[4].widget.options | B 400 against A 1,000 at n = 20; tie at 50; A from 51 | correct | S |
| l2 | screens[4].explain | big O describes growth, not exact cost | correct | CLRS 3.1 |
| l2 | screens[5].widget.options | O(1) means bounded by a constant; scan cheaper until 333,334 | correct | S |
| l2 | screens[6].prose | f = O(g) iff f(n) <= c g(n) for all n >= n0; an upper bound; quote the smallest class | correct | CLRS 3.1 |
| l2 | screens[6].widget.options | 2n log n + 40n + 9 is O(n log n); O(2n log n) right but unsimplified; O(n^2 log n) true but loose | correct | D |
| l2 | screens[6].explain | 2n log n passes 40n once log2 n > 20 | correct | S |
| l2 | screens[7].widget.lines | 50n <= 50n^2, 7 <= 7n^2 for n >= 1; c = 60, n0 = 1 | correct | S `c=60` |
| l2 | screens[7].explain | any working pair (c, n0) proves the bound | correct | CLRS 3.1 |
| l2 | screens[8].widget (code) | `steps_a`, `steps_b`, `cheaper`; test-4, test-6, test-10 feedback | correct | H |
| l2 | screens[9].widget, explain | 2,500,000 calls; 1.25 x 10^9 with a third loop; pandas changes the constant, not the class | correct | S; D |
| l2 | summary | definition, order of classes, doubling rules, 50n v n^2 trap | correct | S |
| l2 | quiz[0] | fixed inner loop of 5: O(n); O(n^2) true but loose; O(5n) = O(n) | correct | D |
| l2 | quiz[1] | vectorising changes the constant only | correct | D: every value still visited |
| l2 | quiz[2] | O(n^2): 4 minutes becomes 16; slips 8, 4, 64 | correct | D |
| l2 | quiz[3] | 20 steps for 10^6, 21 for 2 x 10^6 | correct | S `l9 table` |
| l3 | screens[0] | A holds 1 value, B holds n; extra space O(1) and O(n) | correct | D |
| l3 | screens[0].explain | extra space is memory allocated beyond the input | correct | CLRS 2.1 (in place), standard |
| l3 | screens[1] | dict has 4 entries; grows with distinct keys; O(n) worst case | correct | D |
| l3 | screens[2].widget.answer, wrong[] | 500 swaps for 1,001; 4 for 8; slips 1001, 501, 1000 | correct | S |
| l3 | screens[2].explain | floor(n/2) swaps, in place, O(1); `[::-1]` builds a new list | correct | S; PyDoc sequence types |
| l3 | screens[3].widget (code) | `stream_mean`; peak under 50,000 bytes; test-1, test-3, test-7 feedback | correct | H; S `stream_mean peak` (256 bytes in Pyodide, 2.0 MB for a list) |
| l3 | screens[3].explain | storing 100,000 floats takes megabytes | correct | S |
| l3 | screens[4].canvas | `getsizeof` 8,448,728 and 24 on 64-bit | correct | S (CPython 3.13) |
| l3 | screens[4].widget.answer, wrong[] | 32.4 MB (band 1.5); 8.4, 24, 0.024 | correct | S |
| l3 | screens[4].explain | about 32 bytes a float on 64-bit; about 20 on this page's 32-bit build | correct | S (Pyodide: 4,224,364 and 16) |
| l3 | screens[5].widget (code) | `prefix_sums`, `range_total`; test feedback | correct | H; S |
| l3 | screens[5].explain | n + 1 numbers stored; each range total one subtraction | correct | D |
| l3 | screens[6] | list of intermediates is O(n); append does not copy the list each time; one running value is O(1) | correct | D; L4 |
| l3 | screens[7].widget.answer, wrong[] | 6 open calls for 5 items | correct | S |
| l3 | screens[7].explain | n + 1 calls, O(n) space; about 1,000 open calls allowed | correct | S; PyDoc `sys.getrecursionlimit` |
| l3 | screens[8] | slice copies: O(n); `reverse()`, `prices[-1]`, `len` are O(1) | correct | PyDoc; wiki.python.org TimeComplexity |
| l3 | screens[9].prose, widget, explain | 4,914,000 values a stock; 7.86 GB numpy, 31.45 GB lists; slips 0.98, 0.039 | correct | S |
| l3 | summary | 32 bytes a value in a list of floats, 8 in float64 | correct | S |
| l3 | quiz[0] | generator exhausted; exact `ValueError` text | correct | S |
| l3 | quiz[1] | at most 5 keys: O(1) | correct | D |
| l3 | quiz[2] | count, sum, sum of squares; Var = sum x^2 / n - mean^2; Welford keeps three numbers | correct | S; Welford (1962), Knuth TAOCP 4.2.2 |
| l3 | quiz[3] | 320 MB; 80 MB as float64 | correct | D |
| l4 | screens[0].widget.answer, wrong[] | 9th append copies 8; slips 1, 9, 15 | correct | S |
| l4 | screens[0].explain | copies 1, 2, 4, 8; `list.append` grows by about 1.125 | correct | S; `listobject.c` `list_resize` |
| l4 | screens[1].widget.rows, explain | totals 0, 1, 3, 7, 15; n - 1 at powers of two | correct | S |
| l4 | screens[2].widget.answer, wrong[] | 15/16 = 0.9375; slips 8, 15, 3.75 | correct | S |
| l4 | screens[2].explain | average over the whole run is the amortised cost; amortised O(1) | correct | CLRS 17.1, 17.4 |
| l4 | screens[3].widget.answer, wrong[] | 1.023; 10 resizes; slips 512, 1023, 102.3 | correct | S |
| l4 | screens[3].explain | worst append O(n) but rare; n appends cost O(n) | correct | CLRS 17.4 |
| l4 | screens[4].widget.lines | copies at sizes 1 ... 2^(m-1) < n; sum 2^m - 1 < 2n | correct | S `total < 2n` |
| l4 | screens[5].prose, options | tripling: sum below 3n/2, amortised O(1); not always more copies than doubling | correct | S |
| l4 | screens[5].feedback.correct | any constant factor above 1 gives amortised O(1) | correct | D: total < r/(r-1) n |
| l4 | screens[6].widget (code) | `total_copies`; test-2, test-3, test-10 feedback | correct | H; S |
| l4 | screens[7].widget.answer | grow by 10: 49,500 copies | correct | S |
| l4 | screens[7].widget.wrong[resizes, doubling, ten-each] | 99, 1023, 990 | correct | D |
| l4 | screens[7].feedback.byKey.to-1000 | "The array is never full at 1,000 here" | imprecise | S `FINDING 3 and 4`: size and capacity are both 1,000 after the last append; true only as "no append finds it full". Finding 3 |
| l4 | screens[7].explain | about n^2/20; fixed growth is O(n^2) | correct | S |
| l4 | screens[8] | 499,500 shifts; `pop(0)` O(n); `deque.popleft` O(1) | correct | S; PyDoc `collections.deque` |
| l4 | screens[9].canvas, widget, explain | 2^20 = 1,048,576; 2,097,151 copies; 1.05 a tick; slip 0.52 | correct | S |
| l4 | summary | geometric sum below 2n; fixed growth and `pop(0)` quadratic | correct | S |
| l4 | quiz[0] | `np.append` in a loop is O(n^2): call k copies k - 1 | correct | NumPy docs `numpy.append` (returns a copy) |
| l4 | quiz[1] | worst of 100 appends copies 64, at append 65 | correct | S |
| l4 | quiz[2] | `deque(maxlen=500)`; `pop(0)` and `insert(0, p)` are O(n) | correct | PyDoc |
| l4 | quiz[3] | first append copies nothing | correct | S |
| l5 | screens[0] | only `fact(0)` returns without calling; answers 1, 1, 2, 6, 24 | correct | S |
| l5 | screens[1] | `sum_list` returns 3, 4, 8 | correct | S |
| l5 | screens[2] | base case and recursive case defined; `len(xs) == 1` base fails on `[]` with IndexError | correct | S |
| l5 | screens[3].widget.options | same input never shrinks; last item gives 9; skipping gives 7 | correct | S |
| l5 | screens[4] | dropped recursive answer returns 4 | correct | S |
| l5 | screens[5].widget (code) | `sum_list`, `power`; test feedback | correct | H |
| l5 | screens[6].canvas | traceback text, "repeated 996 more times" | correct | run of the same file on CPython 3.13 |
| l5 | screens[6].widget.options, explain | `fact(0)` with base `n == 1` runs to -1, -2; no limit is enough; limit of 1,000 frames | correct | S |
| l5 | screens[7] | three parts of a recursion; f(3) with step 2 skips 0; `n <= 0` is safe | correct | S |
| l5 | screens[8].widget.lines | induction: base case, inductive step, every n | correct | CLRS 2.1 (loop invariants), standard induction |
| l5 | screens[9].widget (code), explain | `total_pnl`; 395.75; files are base cases | correct | H; S |
| l5 | summary | must move towards and land on the base case | correct | S |
| l5 | quiz[0] | `count([5, 5])` is 3 | correct | S |
| l5 | quiz[1] | 1157.625; slips 1150 and 1102.5 | correct | S |
| l5 | quiz[2] | bond 97.28; par when coupon equals rate | correct | S |
| l5 | quiz[3] | `-1 // 2` is -1 so `f(-1)` never ends; 7, 3, 1, 0; 1000 reaches 0 in ten calls | correct | S; D: ten recursive calls after the first |
| l6 | screens[0], [1] | last call in is first out; push and pop order of `fact(3)` | correct | CLRS 10.1 (stacks) |
| l6 | screens[2] | frame, call stack, push, pop; n + 1 frames for `fact(n)`: 6 | correct | S `frames` |
| l6 | screens[3].prose | `getrecursionlimit()` is 1000; `sum_to(5000)` fails | correct | S (CPython and Pyodide) |
| l6 | screens[3].widget.options[limit].why, feedback.byKey.limit | a huge limit lets the real stack overflow; Python can crash with no traceback | correct | PyDoc `sys.setrecursionlimit`; run: recursion through `max(key=...)` 5,000 deep with the limit raised is a fatal `RangeError` in Pyodide 0.27.7. Note: the pure-Python `sum_to(5000)` itself runs once the limit is raised (S `l6 note`) |
| l6 | screens[3].widget.options[base].why | a second base case saves one frame | correct | D |
| l6 | screens[4] | tail call still keeps every frame; Python does not optimise tail calls | correct | S; van Rossum, "Tail Recursion Elimination" (2009) |
| l6 | screens[5] | each frame has its own `total`; returns 4 | correct | S |
| l6 | screens[6].widget (code) | loop `sum_to`, `depth` of `fib`; 5 frames of 15 calls; test feedback | correct | H; S |
| l6 | screens[6].explain | stack holds one path: depth n | correct | S (n >= 1) |
| l6 | screens[7] | explicit stack loop is depth first; children taken last to first | correct | D: `pop()` takes the last pushed |
| l6 | screens[7].widget.options[limit].why | limit set to 100,000 can crash Python outright | correct | as screens[3] |
| l6 | screens[8] | pushes to the base case, then pops in reverse | correct | D |
| l6 | screens[9].widget (code), explain | `levels`; 4 frames; 10,000 frames need a loop | correct | H; S |
| l6 | summary | about 1,000 frames; no tail-call optimisation; n + 1 frames | correct | S |
| l6 | quiz[0] | RecursionError near day 1,000 | correct | S |
| l6 | quiz[1], [2] | `var_95()` returns first; 7 frames for 6 prices | correct | S |
| l6 | quiz[3] | NameError: a function sees its own and enclosing (module) names, never its caller's | correct | S; Python language reference 4.2 (lexical scoping) |
| l7 | screens[0] | halves return 7 and 9; whole list 9 | correct | D |
| l7 | screens[1] | divide and conquer; `mid = 3`; halves 0 to 3 and 4 to 7 | correct | CLRS 2.3.1 |
| l7 | screens[2].widget, explain | 15 calls for 8; 2n - 1 calls in general | correct | S |
| l7 | screens[3] | inversion defined; `[3, 1, 4, 2]` has 3; slips 2, 6, 1 | correct | S; CLRS problem 2-4 |
| l7 | screens[4] | binary search halves: 11 calls from 1,024; log2 1024 + 1 | correct | S |
| l7 | screens[5].prose | fast power: 1 multiplication for an even step, 2 for an odd one | correct | CLRS 31.6 (repeated squaring) |
| l7 | screens[5].widget (code) | `max_rec`, `power_fast`; (1024, 4), (243, 3), (1, 41), 14, 218626.78; test feedback | correct | H; S |
| l7 | screens[5].explain | 10^9 needs 30 levels and 41 multiplications; calling twice undoes the saving | correct | S; D: T(n) = 2T(n/2) + 1 is O(n) |
| l7 | screens[6] | right half from `mid` never shrinks on two items: RecursionError | correct | S |
| l7 | screens[7] | split, solve, combine; 31 calls for 16 | correct | S |
| l7 | screens[8] | `power_fast(2, 5)` = 4 x 4 x 2 = 32 with 3 multiplications | correct | S |
| l7 | screens[9] | 1.0002^252 = 1.0517; 12 multiplications; slips 8, 251, 252, 14; 16 for 2,520 | correct | S |
| l7 | summary | depth near log2 n; 41 multiplications for 10^9 | correct | S |
| l7 | quiz[0] | `max` runs 7 times; n - 1 like a loop | correct | S |
| l7 | quiz[1] | `max_rec(xs, 1, 1)` returns 99.8 | correct | D |
| l7 | quiz[2] | merge of 3 and 4 makes at most 6 comparisons | correct | S |
| l7 | quiz[3] | 3 additions combine 4 subtotals; 249,999 additions a machine | correct | D |
| l8 | screens[0] | `fib(2)` three times, `fib(3)` twice; 15 calls | correct | S |
| l8 | screens[1] | recurrence defined; T(n) = T(n-1) + 1, T(1) = 1 gives n | correct | S; CLRS 4 |
| l8 | screens[2] | 2T(n/2) + n: 8 per level, 4 levels, 32; T(2) = 4, T(4) = 12 | correct | S |
| l8 | screens[3] | T(n/2) + 1 at 2^20 is 21 | correct | S |
| l8 | screens[4] | 2T(n-1) + 1 = 2^n - 1; 1023; naive fib at most this; ratio 1.618 | correct | S |
| l8 | screens[4].widget.wrong[] | 20, 1024, 19, 512 | correct | D: 2 x 10, 2^10, 1 + 2 x 9, 2^9 |
| l8 | screens[5].widget (code) | `fib_calls`, memoised `fib`; C(80), F(90), F(300) | correct | H; S |
| l8 | screens[5].explain | C(n) = 2F(n+1) - 1; memoised fib is O(n) calls; memoisation defined | correct | S; CLRS 15.3 |
| l8 | screens[6] | two calls on halves give O(n log n), not O(2^n); fib tree doubles through its top half | correct | D: shortest root-to-leaf path of fib is n/2 |
| l8 | screens[7].widget.lines | level k: 2^k calls of size n/2^k; log2 n + 1 levels; n(log2 n + 1) | correct | S; CLRS 4.4 |
| l8 | screens[8] | four recurrences; master theorem packages the halving cases; 2T(n/2) + 1 = 2n - 1 | correct | S; CLRS 4.5 |
| l8 | screens[9] | 2^(n+1) - 1 nodes without recombining; 5,151 with; 2.5 x 10^30; leaves 133.1 to 72.9 | correct | S; Hull ch. 13 |
| l8 | summary | halving gives log2 n + 1 levels; memo makes fib O(n) | correct | S |
| l8 | quiz[0], [1] | chain of log2 n + 1 calls; `sum_list` makes n + 1 calls; slicing copies | correct | S; D |
| l8 | quiz[2] | memoised `fib(30)` makes 59 calls; naive 2,692,537 | correct | S |
| l8 | quiz[3] | T(16) = 80; slips 64, 32, 256 | correct | S |
| l9 | screens[0] | middle cell (index 7 or 8) rules out most; a miss at index 12 can leave 12 cells | correct | D |
| l9 | screens[1] | trace 7, 11, 13, 12; four looks; a scan needs 13 | correct | S |
| l9 | screens[2] | worst case floor(log2 n) + 1: 1, 5, 10, 20 | correct | S (brute force to n = 600); Knuth TAOCP 6.2.1 |
| l9 | screens[3].widget (code) | `binary_search`; at most 45 reads of a million; test-4, test-5, test-11 feedback | correct | H |
| l9 | screens[3].explain | `lo <= hi` checks a single element; both updates shrink the range | correct | D |
| l9 | screens[4] | leftmost 4: `hi = mid` keeps mid, `lo = mid + 1` drops it; ends at index 1 | correct | S |
| l9 | screens[5].widget (code) | `first_at_least` equals `bisect_left`; test feedback | correct | H; S |
| l9 | screens[5].explain | `bisect_right` is the same with `<=`; both O(log n) | correct | PyDoc `bisect` |
| l9 | screens[6] | `lo = mid` stalls when `hi = lo + 1`; `<=` makes it worse; Python ints do not overflow | correct | S; Bloch (2006), "Nearly All Binary Searches and Mergesorts are Broken" |
| l9 | screens[7].prose | invariant; at most ceil(log2(n + 1)) passes | correct | S (exact for n <= 129) |
| l9 | screens[7].widget.options, explain | pairings: `lo < hi` with `hi = mid`; `lo <= hi` with `hi = mid - 1`; `lo + (hi - lo) / 2` in C or Java | correct | S; Bloch (2006) |
| l9 | screens[8] | `bisect_left` 3 counts strictly below; `bisect_right` 6 counts at or below; slips 3, 5, 2 | correct | S |
| l9 | screens[9].widget (code), canvas, explain | `next_trading_day`; 7 and 8 March 2026 a weekend; ISO strings sort by date; 12 looks | correct | H; S |
| l9 | summary | floor(log2 n) + 1; a million needs at most 20 | correct | S |
| l9 | quiz[0] | unsorted list returns -1 after looking at 12 then 8 | correct | S |
| l9 | quiz[1], [2], [3] | 13 looks for 5,000; `1 4`; `first_at_least([5, 5, 5, 5], 5)` is 0 | correct | S |
| l10 | screens[0] | 0.15 sqrt(q) = 1 at q = 44.44 | correct | S |
| l10 | screens[1] | trace 32, 48, 40, 44, 46, 45; six tries among 65 sizes; 65, 32, 16, 8, 4, 2, 1 | correct | S |
| l10 | screens[2] | predicate and monotone defined; savings question is monotone; peak and "below £95" are not | correct | D |
| l10 | screens[3].widget (code) | `smallest_true`; about 40 calls for 10^12; never outside the range; test feedback | correct | H; S |
| l10 | screens[4].widget (code), explain | `isqrt` via smallest false; (n + 1)^2 > n; about 60 steps for 10^18 | correct | H; S |
| l10 | screens[5].prose, canvas | price falls as yield rises; 95.67 at 5%, 91.58 at 6% | correct | S; Hull ch. 4 |
| l10 | screens[5].widget (code) | `yield_for_price`; 120.00 at zero yield; tests stable under the 1p tolerance | correct | H; S |
| l10 | screens[5].feedback.correct, explain | 5.16% in 15 halvings; stop at a tolerance over reals | correct | S |
| l10 | screens[6] | non-monotone test returns 5 not 2; `max(closes[:d + 1]) > 100` is monotone | correct | S |
| l10 | screens[7] | about log2(hi - lo + 2) calls; 30 for 10^9 | correct | S |
| l10 | screens[8].prose | Black-Scholes 10.45, 12.34, 14.23 (S = K = 100, r = 5%, T = 1); price rises with sigma | correct | S; Hull ch. 15 (vega > 0) |
| l10 | screens[8].explain | 20 halvings give 0.2411; Newton is faster, bisection cannot diverge | correct | S; Burden and Faires, *Numerical Analysis* 2.1, 2.3 |
| l10 | screens[9] | bracket 2,500 to 4,000; next test 3,250; 11 tests; slips 1750, 3000 | correct | S |
| l10 | summary | ceil(log2(range size)); `hi + 1` means none | correct | S |
| l10 | quiz[0] to [3] | 26 days; `None`; 20 halvings; n + 1 needed for n = 0 and 1 | correct | S |
| l11 | screens[0], [1] | 7 and 9 shift for the 6; inserting 1 takes 4 comparisons | correct | S |
| l11 | screens[2] | counting rule; 1 + 2 + 1 + 4 + 4 = 12 | correct | S |
| l11 | screens[3].widget (code) | `insertion_sort` with counts 12, 4, 10, 5, 9; test feedback (>, not >=) | correct | H; S |
| l11 | screens[4] | nearly sorted: 9; slips 28, 7, 2; sorted costs n - 1 | correct | S |
| l11 | screens[5] | reversed: n(n-1)/2 = 499,500; 780 at 40; slips | correct | S; CLRS 2.2 |
| l11 | screens[6] | no `break`: 15 comparisons on sorted 6; with it, 5 | correct | S |
| l11 | screens[7] | worst n(n-1)/2, best n - 1, in place, stable with `>`; `sorted` is Timsort, O(n log n) | correct | S; `listsort.txt` |
| l11 | screens[8].widget (code), explain | `sort_trades` stable by time; `sorted(key=...)` gives the same; Timsort stable and fast on runs | correct | H; S; PyDoc Sorting HOWTO |
| l11 | screens[9] | 4 comparisons and 3 shifts; binary search would take 10 looks | correct | S |
| l11 | summary | O(n^2) worst, O(n) nearly sorted, stable | correct | S |
| l11 | quiz[0], [1], [2] | 3 comparisons; sorted is fastest (9,999 against about 50 million); `([42], 0)` | correct | S |
| l11 | quiz[3].widget.options[a], [b], [d] | `sorted` is O(n log n) worst case; no sort beats O(n) | correct | S; `listsort.txt` |
| l11 | quiz[3].widget.options[c].why | O(n) "is only for input already in order" | imprecise | S `FINDING 7`: reversed input costs n - 1 comparisons too. Finding 7 |
| l11 | quiz[3].explain | Timsort stable; insertion sort only on short runs | correct | `listsort.txt` (binary insertion to `minrun`) |
| l12 | screens[0] | merge by smaller front; at most 7 comparisons for 8 values; linear | correct | S; CLRS 2.3.1 |
| l12 | screens[1] | 3 levels of merging for 8; 7 merges | correct | D |
| l12 | screens[2].widget (code), explain | `merge`; at most n - 1 comparisons; tail already sorted | correct | H; S |
| l12 | screens[2].feedback.byKey.test-9 | "Sorting the joined list, or `pop(0)`, is too slow" | wrong | S `FINDING 2`: `sorted(a + b)` takes 2 ms; a `pop(0)` merge 0.9 s in Pyodide, under the 5 s limit. Finding 2 |
| l12 | screens[3].widget (code) | `merge_sort`; 200 million comparisons for insertion sort on 20,000 reversed | correct | H; S |
| l12 | screens[4] | B, A, C; stable with `<=`, not with `<` | correct | S |
| l12 | screens[5] | base case at length 0 only recurses for ever on one value, whichever way the split rounds | correct | S |
| l12 | screens[6].widget.lines | n per level, log2 n levels that merge, O(n log n) | correct | CLRS 2.3.2 |
| l12 | screens[6].explain | 24 against 28; 20 levels of a million against half a trillion; O(n) extra memory | correct | S |
| l12 | screens[7].prose, explain | inversions measure rank disagreement; tau = 1 - 2 x 3/15 = 0.6 | correct | S; Kendall (1938), tau-a without ties |
| l12 | screens[7].widget (code) | `count_inversions`, 99,930,366; test-8, test-9 feedback | correct | H; S |
| l12 | screens[8].widget (code), explain | `merge_logs`; whole tuples would break ties by venue | correct | H |
| l12 | screens[9] | external sort: sorted runs merged from their fronts; 13 runs of about 15 GB | correct | S; Knuth TAOCP 5.4 |
| l12 | summary | stable, O(n log n) on every input, O(n) extra memory | correct | CLRS 2.3 |
| l12 | quiz[0], [1] | missing tail returns `[1, 2, 3]`; 64 comparisons at most | correct | S |
| l12 | quiz[2] | two million takes a little over 2 seconds: ratio 2.1 | correct | S |
| l12 | quiz[3] | faster than insertion sort, O(n) extra memory, stable | correct | CLRS 2.3 |
| l13 | screens[0], [1] | Lomuto partition of `[7, 2, 9, 4, 1, 8, 5]` gives `[2, 4, 1, 5, 9, 8, 7]`, pivot at 3 | correct | S; CLRS 7.1 |
| l13 | screens[2] | recurse on both sides, pivot left out; no merge needed | correct | CLRS 7.1 |
| l13 | screens[3].widget (code) | `partition`; eight tests; test feedback | correct | H; S |
| l13 | screens[4].widget (code) | random-pivot `quicksort`; sorted 3,000 passes | correct | H |
| l13 | screens[4].explain | expected O(n log n) for distinct values whatever the order; in place | correct | S; CLRS 7.4 |
| l13 | screens[5].widget.answer | sorted 7 with last pivot: 21, the most possible | correct | S (all 5,040 orders) |
| l13 | screens[5].widget.wrong[shuffled], [square] | 12 for the example list; 49 = n^2 | correct | S |
| l13 | screens[5].feedback.byKey.nlogn | slip 14: "You assumed even splits" | imprecise | S `FINDING 6`: even splits of 7 cost 6 + 2 + 2 = 10; 14 is 7 x 2. Finding 6 |
| l13 | screens[5].explain | n(n-1)/2, O(n^2), recursion n deep | correct | S |
| l13 | screens[6] | first pivot on sorted 2,000: 1,999,000 comparisons, 2,000 deep, RecursionError | correct | S |
| l13 | screens[6].explain | random pivot or median of three makes even splits likely | correct | SW 2.3 |
| l13 | screens[7] | average O(n log n), worst O(n^2), in place, not stable; no input order is worst for a random pivot | correct | CLRS 7.3, 7.4 |
| l13 | screens[7].explain | many equal values still hurt Lomuto; three-way partition fixes it | correct | S; SW 2.3 |
| l13 | screens[8].widget (code) | `quickselect`; median 5003; no-sort check | correct | H; S |
| l13 | screens[8].feedback.correct, explain | 2n to 4n comparisons; about 3.4n at the median; halving sum 2n | correct | S (Monte Carlo, 400 runs each: 3.39n, 2.40n, 2.0n); CLRS 9.2 |
| l13 | screens[9] | VaR is one order statistic; 230 million against 20 to 40 million; quickselect exact | correct | S |
| l13 | screens[9].widget.options[d], explain | introsort in C++ `std::sort` and .NET caps the worst case at O(n log n) | correct | Musser (1997); .NET `Array.Sort` remarks; ISO C++ [alg.sort] |
| l13 | summary.formula.note | average splits give about 1.39 n log2 n | correct | S (mean matches 2(n+1)H_n - 4n; 1.39 is the leading term); SW 2.3 |
| l13 | quiz[0], [1] | `[2, 1]` gives p = 0, `[1, 2]`; 499,500 | correct | S |
| l13 | quiz[2] | Lomuto reorders equal prices: c, b, a | correct | S |
| l13 | quiz[3] | three-way partition for three distinct values; `<` moves the pile to the other side; two or three levels | correct | S |
| l14 | screens[0] | 87p in 5 coins; greedy always optimal for UK coins | correct | S (DP to 2,000, with and without £1 and £2) |
| l14 | screens[1], [2] | 1, 3, 4: 6 in 2 not 3; greedy beaten at 6 and 10 only, right for 8 of 10 | correct | S |
| l14 | screens[2].explain | greedy defined: best step now, never undone; examples do not prove it | correct | CLRS 16 |
| l14 | screens[3].widget (code), explain | `coins_greedy`; fails for 1, 3, 4 and 1, 10, 25 | correct | H; S |
| l14 | screens[4] | at most 4 of the 7 meetings; A alone gives 1 | correct | S (brute force) |
| l14 | screens[5].widget (code) | earliest finish first; `>=` lets touching meetings share; O(n log n) | correct | H; S |
| l14 | screens[6] | sorting by start gives 1; shortest first fails on (1, 5), (4, 7), (6, 10); earliest finish always optimal | correct | S (1,500 random diaries against brute force) |
| l14 | screens[7].widget.lines | exchange argument: g ends no later than o, swap keeps size | correct | KT 4.1; CLRS 16.1 (theorem 16.1) |
| l14 | screens[8] | fractional 460, whole 400, greedy 300; greedy optimal with parts, not with whole items | correct | S; CLRS 16.2 |
| l14 | screens[9] | cheapest ask first costs 100,031; optimal for one order; slips 100,020 and 100,045 | correct | S; D (exchange) |
| l14 | screens[10] | pair Sharpe (S1 + S2)/sqrt(2 + 2 rho) for equal weights and vols; 1.47, 1.77, 1.70 | correct | S; D from portfolio mean and variance |
| l14 | summary | one counterexample sinks a greedy rule; exchange argument proves one; interval scheduling always optimal | correct | S; KT 4.1 |
| l14 | quiz[0], [1] | 1, 10, 25 at 30: greedy 6, best 3; `0 2` | correct | S |
| l14 | quiz[2].widget.answer, wrong[best] | fractional knapsack 38; 48 adds every value | correct | S |
| l14 | quiz[2].feedback.byKey.whole | slip 30: "You took whole items by value: 20 and 10" | wrong | S `FINDING 1`: whole items by value are 20 then 18, total 38. Finding 1 |
| l14 | quiz[3] | examples can refute a greedy rule, never prove it | correct | D |
| review-1 | items[0] to [4] | 570 calls; O(n^2); 4 times per doubling; `sorted` copies; generator O(1) against list O(n) | correct | S; PyDoc |
| review-1 | items[5] | 127 copies for 65 appends; slips 63, 64, 128 | correct | S |
| review-1 | items[6].widget.answer, wrong[resizes], [hundred-each] | 4,500 copies; 9; 900 | correct | S |
| review-1 | items[6].feedback.byKey.to-thousand | "The array is not full at 1,000 within these appends" | imprecise | S `FINDING 3 and 4`: capacity 1,000 and size 1,000 after append 1,000. Finding 4 |
| review-1 | items[7] | 9 times the pairs: about 90 minutes | correct | S |
| review-2 | items[0], [1] | empty product is 1; the empty-list call returns first | correct | D |
| review-2 | items[2], [5] | 8 multiplications for 100; 6 frames for 50; 30 for 10^9 | correct | S |
| review-2 | items[3], [8] | T(n-1) + 1 = n; `max_rec` is 2T(n/2) + 1 = 2n - 1 | correct | S |
| review-2 | items[4] | 530.604; slips 530 and 520.2 | correct | S |
| review-2 | items[6] | missing odd case returns 9 | correct | D |
| review-2 | items[7] | C(7) = 41 = 2F(8) - 1 | correct | S |
| review-3 | items[0] | `lo <= hi` with `hi = mid` never ends on `[10, 20]`, 15 | correct | S |
| review-3 | items[1] | 7 comparisons on `[4, 3, 2, 1, 5]` | correct | S |
| review-3 | items[2] | 15 years to double at 5%; rule of 72 gives 14.4 | correct | S |
| review-3 | items[3] | Lomuto on `[3, 8, 2, 5, 1, 4]`: p = 3, `[3, 2, 1, 4, 8, 5]` | correct | S |
| review-3 | items[4], [6], [7] (code) | `merge_unique`, `count_between`, `max_size`; test feedback | correct | H |
| review-3 | items[5] | earliest finish always best; 1, 5, 12 fails at 15; whole trades and shortest first fail | correct | S |
| review-3 | items[8] | merge sort or `sorted`: stable and O(n log n); insertion sort risks hours on 2 million | correct | D: 10^12 comparisons |
| homework-1 | items[0], [1], [2] | 31,187,500; tripling loop O(log n); 124 copies from capacity 4 | correct | S |
| homework-1 | items[3] | tripling proof; total below r/(r - 1) n for any r > 1 | correct | S |
| homework-1 | items[4] | rolling mean: O(1) per tick, O(k) space | correct | D |
| homework-1 | items[5], [6] (code) | `best_trade` (one pass equals the pair loop), `copies_fixed` | correct | H; S |
| homework-1 | items[7].model | 8,997,000 calls; 2.25 x 10^9; 64-byte tuple, about 1 GB; heap of k; 80 minutes | correct | S; PyDoc `heapq` |
| homework-2 | items[0], [5], [6], [9] (code) | `flatten`, `sort_count`, `total_value`, `split_feed` (927 and 4,374 splits) | correct | H; S |
| homework-2 | items[1], [2], [7] | `count_calls(5)` is 1; 7 crossing inversions; 11 frames | correct | S |
| homework-2 | items[3], [4] | 2^n - 1; 2T(n/2) + n^2 is O(n^2) | correct | S; CLRS 4.5 case 3 |
| homework-2 | items[5].how | 5-second limit; pair counting on 20,000 exceeds it | correct | run: about 15 s in Pyodide |
| homework-2 | items[8].model | 2^(n+1) - 1 calls; 231 nodes; depth n + 1; backward loop n(n+1)/2 updates, under a second | correct | S; run 0.27 s in Pyodide; Hull ch. 13 |
| homework-2 | items[9].explain | at most 2^(n-1) splits | correct | D: each gap cut or not |
| homework-3 | items[0], [1], [2], [3] | 27 halvings; 1, 5, 12 fails; stable sorts; worst-case quicksort derivation | correct | S |
| homework-3 | items[4], [5], [8] (code) | `min_capacity`, `merge_k` (O(N log k)), `find_trade` (under 100 reads) | correct | H; S |
| homework-3 | items[6].widget (code), explain | `kth_largest` at index n - k; 2n to 4n expected | correct | H; S |
| homework-3 | items[6].feedback.byKey.test-8 | "Test 8 is already sorted. A fixed end pivot makes that O(n^2)" | imprecise | S `FINDING 5`: test 8 asks for k = 1; a fixed last pivot (the taught scheme) finishes in one partition, 4,999 comparisons. Finding 5 |
| homework-3 | items[7].model | 2.3 x 10^8; 24 comparisons a bisection; 5 x 10^9 for scans; 5 x 10^13 worst case; stability not needed | correct | S; Blum et al. (1973) for median of medians |
