# Claim ledger: contests levels 1 to 3, audit round 3

Blind audit of `app/content/courses/contests/` at commit `64887c8e`: lessons l1 to l12, `review-1` to `review-3`, `homework-1` to `homework-3` (there are no `problems-*` files for these levels). Topic 2.4 is a Stage 2 course, so the ledger is full depth. One row may cover several JSON paths that state the same claim; every `feedback.byKey.test-N` line has its own row in the second table.

Verdicts: `correct`, `wrong`, `imprecise`, `misleading`, `unverified`. Basis "script" is `docs/reports/contests-L1-3-concepts-r3.py`; "sweep" is the code feedback sweep described in `docs/reviews/audit-contests-1-3-r3.md` (Pyodide 0.27.7 through `app/tools/code-runner.mjs`, YoWASP clang 21 for wasm32 under node WASI, real pytest in CPython). Lines marked timing-dependent were measured on this machine, which runs the page's Pyodide about 1.4 times slower than the figures quoted in the content.

Totals: 378 rows. correct 372, wrong 1, imprecise 5, misleading 0, unverified 0.

## Claims by file

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l1 | screens[0].prose | Each hidden test gets up to 5 s; a test over the limit stops the run and later tests do not run | correct | engine: `app/js/engine/widgets/code.js` case plan and `drill-worker.js` limits, read; reproduced with `code-runner.mjs` (slow case reports "Stopped after 5 s", later rows absent) |
| l1 | screens[1].widget.answer | The limits are the two lines with the inequalities (l13, l15) | correct | lines counted from 1 in `canvas.params.lines` |
| l1 | screens[1].feedback.byKey (8 lines) | time and memory lines limit the program, not the input; example is one test | correct | Codeforces statement layout (codeforces.com problem format) |
| l1 | screens[1].explain | example of 6 small positives hides size and negatives | correct | derivation from the statement |
| l1 | screens[2].widget.answer, wrong no-first, byKey c2, c4 | fresh highs of 3 1 4 1 5 9 are days 1, 3, 5, 6 | correct | recomputed in concepts script (prefix maxima) |
| l1 | screens[3].prose, slots | six parts of a Codeforces statement: legend, input, output, constraints, examples, note | correct | Codeforces usage ("legend" is the setters' term, Polygon manual) |
| l1 | screens[3].explain | read constraints, then output, then legend | correct | convention of the course, stated as advice |
| l1 | screens[4].widget.answer 200000; wrong product 2e9, tests 1e4 | sum bound caps the whole input | correct | $10^4 \cdot 2\cdot10^5 = 2\cdot10^9$; script |
| l1 | screens[4].explain | linear work per test is linear overall under a sum bound | correct | $\sum_i c\,n_i = c\sum n_i$ |
| l1 | screens[5] options, hints, explain, caption | sum reaches $2\cdot10^{14}$, int max 2,147,483,647, unsigned about $4.3\cdot10^9$, long long about $9.2\cdot10^{18}$ | correct | C++ standard [basic.fundamental]; wasm32 clang: int 32 bits, long long 64 (compiled `sizeof` probe, see sweep) |
| l1 | screens[5].explain | a C++ int overflows with no error and prints a wrong number | correct | signed overflow is undefined behaviour, in practice wraps silently (ISO C++ [expr.pre]/4) |
| l1 | screens[6] answer 1, wrong 4, 0; explain | strictly greater: ties do not count; n = 1 gives 1 | correct | script |
| l1 | screens[7] answer 2, wrong 0, 1, 3; explain | -5 -3 -4 gives 2; `best = 0` prints 0 | correct | script runs the `best = 0` program: 0 |
| l1 | screens[8] options, explain | restatement = formal task plus what the limits imply | correct | advice; numbers as screens[5] |
| l1 | screens[9].widget solution, how, explain | `text.split()` parse is linear and ignores blank lines | correct | CPython `str.split()` with no argument splits on runs of whitespace (Library Reference, str.split) |
| l1 | screens[10].widget solution, how, explain | running best is O(n); start from None or from xs[0] with count 1 | correct | script |
| l1 | screens[11] options, hints, feedback | totals reach $10^{11}$; first-seen order means an insertion-ordered dict | correct | $10^5\cdot10^6$; dicts keep insertion order since Python 3.7 (Language Reference 3.2) |
| l1 | summary.* | answer bound $2\cdot10^{14} > 2^{31}-1$ | correct | arithmetic |
| l1 | quiz[0] | n = 1 with a loss prints 1; `best = 0` prints 0 | correct | script |
| l1 | quiz[1] answer 290001; slips 300000, 30 | other 9,999 tests take at least one value each | correct | $300000-9999$; script |
| l1 | quiz[2] | product up to $10^{12}$ needs long long and `1LL *` so the multiply is 64-bit | correct | usual arithmetic conversions, ISO C++ [expr.arith.conv] |
| l1 | quiz[3] answer 3; slips 2, 4 | "at least" lets the tie count on 2 2 1 3 | correct | script |
| l2 | screens[0] options, hints, feedback, explain | step counts at $n = 2\cdot10^5$: slices $n^3/6 \approx 1.3\cdot10^{15}$, two loops $n^2/2 = 2\cdot10^{10}$, one pass $n$; a judge does about $10^8$ simple steps a second in C++ | correct | $\sum_{l\le r}(r-l+1) = n(n+1)(n+2)/6$; script; $10^8$ rule: Halim, *Competitive Programming 3*, sec. 1.2.3 |
| l2 | screens[0] option lin | Kadane's pass gives the largest non-empty stretch | correct | Bentley, *Programming Pearls*, column 8; script compares with brute force on 300 random lists |
| l2 | screens[1] answer 10000; slips 3162, $10^8$, 4523071; explain | $n^2 = 10^8$ at $10^4$; $n\log_2 n = 10^8$ near 4.52 million; $2\cdot10^5\log_2(2\cdot10^5) \approx 3.5\cdot10^6$ | correct | script (bisection for $n\log_2 n$) |
| l2 | screens[1].prose, screens[2].canvas | Python about $10^7$ steps a second (roughly $10^6$ to $10^7$); PyPy a few times slower than C++; $10^7$ additions about 1 s in Pyodide | correct | rule of thumb; timing-dependent, measured in sweep (Pyodide in node) |
| l2 | screens[2] table rows 1, 2, 3 and hints | 500 gives $n^3$, 5,000 gives $n^2$, $2\cdot10^5$ gives $n\log n$, with $2^{20}\approx10^6$, $500^3 = 1.25\cdot10^8$, $5000^2 = 2.5\cdot10^7$ | correct | arithmetic; Halim sec. 1.2.3 table |
| l2 | screens[2].feedback.byKey.r0c1 | "Your entry for $n \le 20$ is not the slowest that fits" shown for any entry other than $2^n$ | imprecise | $O(n\,2^n)$ is slower and fits ($20\cdot2^{20}\approx2\cdot10^7$, as screens[3].explain itself says); finding 3 |
| l2 | screens[2].feedback.byKey.r4c1 | "Your entry for $10^{18}$ is too slow" shown for any entry other than $\log n$ | imprecise | an entry of `O(1)` is faster, not too slow; the three lines above it use the two-sided wording; finding 4 |
| l2 | screens[2].explain | a limit on a value, like $10^{18}$, asks for log | correct | Halim sec. 1.2.3 |
| l2 | screens[3] answer $2^{20}$ = 1,048,576; slips 400, 20, 8000; explain $2\cdot10^7$ | subsets of 20 items | correct | arithmetic |
| l2 | screens[4] answer 12,497,500; slips $n^2$, $n(n-1)$; explain | pairs $i<j$ are $n(n-1)/2$; a tenth of a second in C++ | correct | arithmetic; budget rule |
| l2 | screens[5] answer 30; slips $10^9$, 31623, 29; feedback floor | $\lceil\log_2(10^9+1)\rceil = 30$; $2^{29}$ is below $10^9+1$ | correct | script simulates worst-case halving |
| l2 | screens[5].explain | $2\cdot10^5$ queries of 30 halvings is $6\cdot10^6$ steps | correct | arithmetic |
| l2 | screens[6] options, hints, explain | $\sum n_i^2 \le (\sum n_i)^2$, largest when one test holds everything; linear work is safe under a sum bound, quadratic is not | correct | convexity of $x^2$; script |
| l2 | screens[7] options, hints, explain | `x not in seen` on a list scans it: about $n^2/2 = 2\cdot10^{10}$ steps with distinct values; a set is O(1) on average | correct | Python wiki TimeComplexity (list `in` O(n), set `in` O(1) average) |
| l2 | screens[7].explain, summary.ideas[2] | `list.pop(0)` and `s = s + c` hide an O(n) cost | correct | TimeComplexity (pop(0) O(n)); str concatenation copies (Library Reference, "Common Sequence Operations", note 6); CPython's in-place resize is an implementation detail and absent in PyPy |
| l2 | screens[8] prose, table, options | budget rule; $10^6\cdot20 = 2\cdot10^7$ against $2\cdot10^8$ | correct | arithmetic |
| l2 | screens[9] solution, tests, explain | boundaries at 26, 464, $10^4$, about $4.5\cdot10^6$, $10^8$; guard `n <= 60` before `2 ** n` | correct | script: $2^{26}$, $464^3$, $465^3 = 100{,}544{,}625$ |
| l2 | screens[9].hints[1] | Python computes `2 ** n` exactly, so at $n = 10^{18}$ it never finishes | correct | integers are exact (Language Reference 3.2); CPython builds the power by repeated squaring, see sweep |
| l2 | screens[10] solution, hints, explain | sort then two pointers counts pairs with sum at most k in $O(n\log n)$; when `a[i]+a[j] <= k` every partner between also fits | correct | sorted order: $a_m \le a_j$ for $i<m\le j$; script recomputes every expectation, 10,053,378,714 included, with a bisect count |
| l2 | screens[10].how | test 8 counts reads through a list subclass, at most 20,000 pass | correct | prelude read; solution measured at about 1,000 reads (sweep) |
| l2 | screens[11] options, hints, feedback | closest pair sum: sort and two pointers; $5\cdot10^{11}$ pairs is hours; a hash set finds only an exact sum | correct | $5\cdot10^{11}/10^8 = 5{,}000$ s; CLRS exercise 2.3-7 |
| l2 | summary.* | budget rule and constraint table | correct | as above |
| l2 | quiz[0] | $100^3 = 10^6$: write the simple loop | correct | arithmetic |
| l2 | quiz[1] | `pop(0)` shifts the rest: up to $n^2/2$ moves; `deque.popleft()` is O(1) | correct | TimeComplexity; `collections.deque` docs |
| l2 | quiz[2] | $10^6\log_2 10^6 \approx 2\cdot10^7$, $\log_2 10^6 \approx 19.9$ | correct | script |
| l2 | quiz[3] | $400^3 = 6.4\cdot10^7$; setters size limits to the intended solution | correct | arithmetic; convention |
| l3 | screens[0] options, feedback | one read and one split is several times faster than 200,000 `input()` calls | correct | timing-dependent; measured in sweep (CPython and Pyodide ratios both above 2) |
| l3 | screens[0].explain | CPython 0.14 s against 0.04 s; Pyodide 0.19 s against 0.06 s | correct | timing-dependent, recorded as such; ratio reproduced in sweep, absolute values machine-bound |
| l3 | screens[1] answer 6; slips 7, 3; steps | token walk of `3 2 5 7 1 -4 3 1 2 3` | correct | script walks `pos` |
| l3 | screens[2] order | read and split, take t, loop, collect, print once | correct | data dependency |
| l3 | screens[3] answer `data[2 + r]`; explain | `3 4` is two tokens; bytes tokens index to ints, so `row[c] == ord('#')` | correct | Library Reference, "Bytes Objects" (indexing gives an int); script |
| l3 | screens[4] options, explain | one `join` and one `print` beats a call per line; `write` in a loop is between | correct | timing-dependent; ordering reproduced in CPython in sweep |
| l3 | screens[5] prose timings | g++ on $10^6$ numbers: 0.86 s, 0.12 s, 0.54 s with `endl` | correct | timing-dependent, recorded as such; ordering reproduced with g++ in sweep where g++ exists |
| l3 | screens[5] options, hints, explain | `std::endl` is `'\n'` plus a flush; `sync_with_stdio(false)` lets the streams buffer on their own; `cin.tie(nullptr)` stops `cin` flushing `cout` before each read | correct | ISO C++ [ostream.manip], [ios.members.static], [ios.base]/tie; cppreference `std::endl`, `sync_with_stdio` |
| l3 | screens[6] key `5 4`; explain `2 2` | one `input()` reads one line, so the program falls out of step | correct | script runs the program on the input with a StringIO stdin |
| l3 | screens[7] options, explain | `split()` with no argument splits on any run of whitespace | correct | Library Reference, `str.split` |
| l3 | screens[8] solution, hints, explain | `map(int, data.split())` is a lazy iterator; `int(b'12')` is 12 | correct | Library Reference, `map`, `int` (accepts bytes); script |
| l3 | screens[8].widget.how, mutants | tests 6 and 7 tell an iterator from a list; a list fails 6, an `__iter__` that does not return self fails 7 | correct | iterator protocol, Library Reference "Iterator Types"; mutants run in sweep |
| l3 | screens[9].prose | this runner hands the program text, so `sys.stdin.read()`; `buffer` on Codeforces | correct | `sys.stdin.buffer` probed under the runner in sweep |
| l3 | screens[9] solution, how, explain | token program; test 6 sum $5\cdot10^9$ fits a Python int | correct | grade-all; Language Reference 3.2 |
| l3 | screens[10] solution, how, hints, explain | `cin >> x` reads tokens across lines; `long long` for the sum; maximum from the first value | correct | ISO C++ [istream.formatted.arithmetic] (skips leading whitespace); compiled in sweep |
| l3 | screens[10].widget.how | compiler download about 26 MB, first compile 10 to 15 s | correct | the package's wasm and resources gzip to 26.4 MB (sweep); compile times are machine-dependent, recorded as such |
| l3 | screens[11] options, hints, explain | default sync keeps `cin` in step with C stdio so the two can be mixed; off, `cin` buffers; then do not mix `scanf` with `cin` | correct | cppreference `std::ios_base::sync_with_stdio`; Stroustrup, *The C++ Programming Language* 4th ed., 38.4.4 |
| l3 | summary.* | fast template, tokens ignore line structure | correct | as above |
| l3 | quiz[0], quiz[1] | join once; `'\n'` not `endl`; `flush=True` makes each line slower | correct | as screens[4], [5] |
| l3 | quiz[2] answer 3; slip 4 | `"2\n\n5 -3".split()` gives three tokens | correct | script |
| l3 | quiz[2].feedback.byKey.lines (slip 2) | "You counted words on the first line only, or lines with text" | wrong | the first line holds one word, `2`, so that count is 1, not 2; two is the number of lines with text (or the words on the last line); finding 1 |
| l3 | quiz[3] | `b'3' == '3'` is False without error; `int(b'3')` is 3 | correct | Library Reference, "Bytes Objects"; script |
| l4 | screens[0] prose, key, feedback | three verdicts: wrong answer, time limit, runtime error; during a round Codeforces shows the verdict and test number, not the test | correct | Codeforces FAQ / contest rules (tests are opened after the round) |
| l4 | screens[1] frames, answer 5; slips 4, 1; explain | seed 1 cases and counts; trial 5 `[4,10,2,6,1,1]`, k = 2: strict 0, brute 1 | correct | script regenerates the five cases from `random.Random(1)` and both counts |
| l4 | screens[2] prose, order, explain | stress testing: trusted brute force, seeded generator, compare loop; same seed gives same cases | correct | Library Reference, `random` ("reproducible sequences"); Halim sec. 1.2.5 |
| l4 | screens[3] options, hints | `<` for `<=` differs only when a pair sums to exactly k; small values make ties common | correct | derivation: counts differ by the number of pairs with sum = k |
| l4 | screens[3].explain | gen B finds the bug on trial 5 with seed 1; gen A found nothing in 100,000 trials on each of four seeds | correct | Monte Carlo in script: gen B first failure at trial 5; gen A, 4 seeds of 100,000 trials, no failure (expected hits per run about $10^{-3}$) |
| l4 | screens[4] options, explain | `[1,1]`, k = 2 keeps the bug; `[6,1,1]`, k = 3 does not | correct | script |
| l4 | screens[5] options, explain | a brute force sharing a helper agrees with the fast code, bug included | correct | both reduce to the same predicate |
| l4 | screens[6] options, explain | "print any" needs a checker, not equality | correct | Codeforces special checkers (testlib); Halim sec. 1.2.5 |
| l4 | screens[7] solution, tests, how, explain | one seeded rng, `gen` once per trial, deep copies, first differing case; seeds 3 and 5 give `([8,10,7],15)` and `([5,6,9,1,8],9)` | correct | script recomputes all ten expectations in CPython; grade-all |
| l4 | screens[8] solution, how, explain | brute force from the statement; a pytest that passes the right function and fails five planted bugs | correct | real pytest in CPython (sweep): passed, then failed on each of the five swaps |
| l4 | screens[9] options, canvas, explain | reference is a plain loop from the definition; prices 100, 98.50, 98, 99.25, 100.50, last day's move £1.25; pricer checked against Black-Scholes where a closed form exists | correct | $100.50-99.25 = 1.25$; Hull, *Options, Futures and Other Derivatives*, ch. 15 (closed form for European options) |
| l4 | summary.* | stress pattern | correct | as above |
| l4 | quiz[0], quiz[1] | small cases; same seed, same cases | correct | as above |
| l4 | quiz[2] answer 2; slips 3, 0 | `[2,3,3]`, k = 6: sums 5, 5, 6 | correct | script |
| l4 | quiz[3] | indices 2 and 4 both hold the maximum 9 | correct | inspection |
| l5 | screens[0] prose, table, hints, feedback r5c1 | $2^{10^{18}}$ has about $3\cdot10^{17}$ digits; last digits of $7^k$ cycle 7, 9, 3, 1 with period 4; $2031 = 4\cdot507+3$ gives 3 | correct | $10^{18}\log_{10}2$; script (`pow(7, k, 10)`) |
| l5 | screens[0].explain | keeping only the remainder after every step is why the answer mod $10^9+7$ is computable | correct | Hardy and Wright, *An Introduction to the Theory of Numbers*, ch. V, 5.2 (congruences respect sums and products) |
| l5 | screens[1] key seat 2; feedback n1, n3, n4 | $5+4 = 9 \equiv 2 \pmod 7$ | correct | arithmetic |
| l5 | screens[2] answer 2; slips 9, 1710, 6; explain | $38\cdot45 = 1710 = 244\cdot7+2$; definition of $a \equiv b \pmod m$ | correct | Hardy and Wright 5.2; script |
| l5 | screens[3] canvas table, key 4, 5, 2, 3, 6 | products and inverses modulo 7 | correct | script rebuilds the table |
| l5 | screens[3] prose, explain | division does not respect remainders; every non-zero residue has an inverse because 7 is prime; $12/4 \to 5\cdot2 = 10 \equiv 3$ | correct | Hardy and Wright Theorem 57 ($ax \equiv 1$ soluble iff $(a,m)=1$) |
| l5 | screens[4] prose, answer 5; slips 243, 3; explain | Fermat: $a^{p-1}\equiv1 \pmod p$ for $p \nmid a$, so $a^{p-2}$ is the inverse; no inverse when $p \mid a$ | correct | Hardy and Wright Theorem 71; $243 = 34\cdot7+5$ |
| l5 | screens[5] prose, options, explain | $3^8 \equiv 2$, $3^{13} \equiv 3 \pmod 7$; about $\log_2 e$ squarings and at most one multiplication per bit; at most 120 for $e = 10^{18}$ | correct | Knuth, *TAOCP* vol. 2, 4.6.3 (binary method); script |
| l5 | screens[6] solution, how, explain | right-to-left binary power; `1 % m` handles m = 1; 60 turns for $10^{18}$; a linear loop fails the count test | correct | Knuth 4.6.3 Algorithm A; script recomputes 916902199, 719476260, 512064609; count measured in sweep (23) |
| l5 | screens[7] solution, how, explain | `pow(a, p-2, p)` with a zero check; `pow(a, -1, p)` since Python 3.8 raises ValueError when not invertible | correct | Library Reference, `pow` ("Changed in version 3.8"); script |
| l5 | screens[8] prose, canvas, solution, hints, explain | int about $2.1\cdot10^9$, long long about $9.2\cdot10^{18}$; two residues multiply to about $10^{18}$, three do not fit; int times int is 32-bit; C++ `%` keeps the sign of the left side, Python's the divisor's | correct | ISO C++ [expr.mul]/4 (truncation towards zero); Language Reference 6.7; compiled for wasm32 in sweep; script recomputes 259106859, 147, 1000000006, 2401 |
| l5 | screens[9] key, options, explain | $(N/5) \bmod 7$ from $r = 2$ is $2\cdot5^{-1} = 6$; `r // 5` gives 0 | correct | $5^5 = 3125 = 446\cdot7+3$; script |
| l5 | screens[10] prose, options, explain | `(a - b + p) % p` lies in $[1, 2p)$ before `%`; plain gives $-2$ and `abs` gives 2 for 3, 5, 7 | correct | derivation; C++ semantics as above |
| l5 | screens[11] answer 4591; slips 31000004808, 4588; explain | rolling checksum $h \leftarrow (31h+x) \bmod (10^9+7)$; equal checksums are likely, not certainly, the same batch; an LCG is the same arithmetic | correct | script; Knuth vol. 2, 3.2.1 (linear congruential method) |
| l5 | summary.* | rules modulo a prime | correct | as above |
| l5 | quiz[0] | `-3 % 7` is $-3$ in C++ and 4 in Python | correct | as screens[8] |
| l5 | quiz[1] answer 3; slips 0.25, 4; explain $4^9 \bmod 11 = 3$ | inverse of 4 modulo 11 | correct | script |
| l5 | quiz[2] | $2^{59} < 10^{18} < 2^{60}$: 60 squarings and at most 60 multiplications | correct | script |
| l5 | quiz[3] | $2p \equiv 0$ has no inverse; $p+1$, $p-1$ and 2 do, the last being 500,000,004 | correct | script |
| l5 | quiz[4] | $10^9+7$ is prime and below $2^{30}$, so one product fits a signed 64-bit integer; $2^{31}-1$ is a larger prime | correct | script (Miller-Rabin deterministic bases for both) |
| l6 | screens[0] target 252; slips 12, 168, 72; explain | lcm(84, 36) = 252 = 7·36 = 3·84; the product 3024 is the 12th meeting | correct | script; Hardy and Wright 5.1 |
| l6 | screens[1] prose, states, explain | a common divisor of a and b divides a − qb; (84,36) → (36,12) → (12,0); lcm = 84/12·36 | correct | Euclid, *Elements* VII.2; Knuth vol. 2, 4.5.2 |
| l6 | screens[2] table 21, 21, 0; feedback, explain | gcd(1071, 462) = 21; $1071 = 51\cdot21$, $462 = 22\cdot21$; $O(\log\min(a,b))$ steps | correct | script; Knuth 4.5.3 Theorem F (Lamé) |
| l6 | screens[3] options, explain | $d \mid a$, $d \mid b$ gives $d \mid r = a - qb$ and conversely, so gcd(a,b) = gcd(b, a mod b); gcd(g,0) = g since every number divides 0 | correct | Knuth 4.5.2 eq. (4) |
| l6 | screens[4] answer 9; slips 10, 5; explain | `steps(89, 55)` is 9; neighbouring Fibonacci numbers are the worst case; $F_{88} \approx 1.1\cdot10^{18}$ takes 86 steps | correct | Lamé's theorem (Knuth 4.5.3 Theorem F); script counts both |
| l6 | screens[5] solution, how, explain | fold from 0; `math.gcd(*xs)` exists; a subtracting loop needs $10^{18}$ turns on $(10^{18}, 1)$ | correct | Library Reference, `math.gcd` (several arguments since 3.9); script |
| l6 | screens[6] key 49, 77, 91; dim list; explain | after 2, 3, 5 the multiples of 7 still standing are 49, 77, 91; 11 starts at 121; 25 primes up to 100 | correct | script rebuilds the dim set and the `only` set |
| l6 | screens[7] solution, tests, explain | sieve of Eratosthenes from $p^2$, $O(n\log\log n)$; $\pi(10^6) = 78{,}498$, $\pi(2\cdot10^6) = 148{,}933$, prime sum below 1,500,000 is 82,074,443,256 | correct | script recomputes all three; Hardy and Wright Theorem 427 (Mertens) for $\sum 1/p$ |
| l6 | screens[7].explain | Project Euler asks solvers not to share answers beyond its first hundred problems | correct | projecteuler.net/about ("problems 1 to 100") |
| l6 | screens[7].widget.how | per-number trial division is stopped on the last tests | correct | timing-dependent; measured in sweep |
| l6 | screens[8] answer 1000; slips $n-1$, 500001; explain canvas | 1,000,003 is prime; a composite n has a divisor $2 \le d \le \sqrt n$; $\lfloor\sqrt{1000003}\rfloor = 1000$ | correct | script (primality, isqrt) |
| l6 | screens[8].explain | a sieve crossing from 2p is still correct and costs almost the same (0.25 s each in Pyodide at $2\cdot10^6$) | correct | correctness by derivation; timing-dependent, ratio measured in sweep |
| l6 | screens[9] solution, tests, explain | trial division with shrinking n; 999,983, 1,000,003 and 999,999,999,989 are prime; smallest-prime-factor sieve gives $O(\log n)$ divisions a query | correct | script (deterministic Miller-Rabin); Halim sec. 5.5 |
| l6 | screens[9].widget.how | "Trial division up to n instead of $\sqrt n$ is stopped on those [three values near $10^{12}$]" | imprecise | the usual loop without the square-root stop (`while n > 1`) divides n down, so $999983^2$ and $999983\cdot1000003$ finish after about $10^6$ turns; only the prime 999,999,999,989 is stopped (sweep); finding 5 |
| l6 | screens[10] prose, options, explain | lcm = a / gcd · b; dividing first avoids overflow: $a = b = 10^{12}$ | correct | arithmetic; `math.lcm` since 3.9 |
| l6 | screens[11] answer 42; slips 294, 7 | lcm(14, 21) = 42: three equity cycles, two futures cycles | correct | arithmetic |
| l6 | screens[11].explain | the curriculum names Project Euler for maths with code | correct | `docs/curriculum.md` topic 2.4 (grep) |
| l6 | summary.* | Euclid, $\sqrt n$ bound, sieve; 1 is not prime | correct | as above |
| l6 | quiz[0], quiz[1] | gcd(0, 15) = 15; lcm(6, 10) = 30, slips 60 and 2 | correct | script |
| l6 | quiz[2] answer 10; slip 11 | ten primes up to 30; 1 is not prime | correct | script |
| l6 | quiz[3] | at n = 200 the last prime that crosses out is 13: $169 \le 200 < 289$ | correct | arithmetic |
| l7 | screens[0] grid, key 6, 10, 20; feedback r0c1, r1c1, r2c1; explain | routes to a corner = routes to its left + routes below (Pascal's rule); 3 by 3 gives 20; 1,000 by 1,000 needs about a million additions | correct | Feller, *An Introduction to Probability Theory* vol. 1, II.2 and III.1 (lattice paths); script |
| l7 | screens[1] explain | routes are choices of 3 up-steps of 6: $\binom63 = 20$; $\binom{2000}{1000}$ has 601 digits | correct | script (`len(str(math.comb(2000, 1000)))`) |
| l7 | screens[2] key 11, 3, 5; hints, feedback, explain | $n! \bmod 13$ built one multiplication at a time; $720 = 55\cdot13+5$ | correct | script |
| l7 | screens[3] prose, key 1, 1, 7, 11, 6, 9; explain | $(6!)^{-1} \equiv 5^{11} \equiv 8$; $((k-1)!)^{-1} = k\,(k!)^{-1}$; build is $O(n + \log p)$ | correct | derivation from $k! = k(k-1)!$; script |
| l7 | screens[4] answer 7; slips 20, 11, 605; explain | $\binom63 \equiv 5\cdot11\cdot11 = 605 \equiv 7 \pmod{13}$; tables need $n < p$ since $n! \equiv 0$ from $n = p$ | correct | script (the slip 11 is $5\cdot6\cdot6 \bmod 13$) |
| l7 | screens[5] answer 21; slips 243, 10, 35; explain | stars and bars: $\binom{n+k-1}{k-1}$ | correct | Feller vol. 1, II.5 eq. (5.2) |
| l7 | screens[6] solution, how, explain | forward loop, one `pow`, backward loop; $10^6! \bmod (10^9+7) = 641102369$; last test has 10 s | correct | script; `budget` semantics read in `code.js` (sweep) |
| l7 | screens[6].how, explain; screens[9].explain | one `pow` per entry is correct and about ten times slower (0.3 s against 3 s in Pyodide) | correct | timing-dependent; ratio measured in sweep |
| l7 | screens[7] solution, how, explain | guard `k < 0 or k > n`; without it a negative index wraps round silently; $\binom{1000}{500} \equiv 159835829$ | correct | Language Reference 3.2 (negative indices); script |
| l7 | screens[8] solution, tests, how, explain | one build to the largest n, then O(1) a query; 72475738, 996692777, 555553024 | correct | script recomputes all three |
| l7 | screens[9] options, hints, explain | `math.comb(n, k) % p` is exact but builds a 301,027-digit number at $n = 10^6$; about 7 s each in Pyodide | correct | Stirling: $10^6\log_{10}2 - \tfrac12\log_{10}(\pi\cdot5\cdot10^5) = 301026.9$; timing-dependent part measured in sweep |
| l7 | screens[10] prose, options, explain | formula holds for prime p and $0 \le k \le n < p$; Pascal's table needs no inverses, so any modulus; 2 has no inverse modulo $10^9$ | correct | Hardy and Wright Theorem 57 |
| l7 | screens[11] answer 210; slips 1024, 5040; explain | $\binom{10}{6} = 210$; $\binom{252}{126}$ has 75 digits | correct | script; Cox, Ross and Rubinstein (1979) tree: paths to node j of n are $\binom nj$ (Hull ch. 13) |
| l7 | summary.* | method and trap | correct | as above |
| l7 | quiz[0] answer 0; slips 21, 1 | $\binom57 = 0$ | correct | convention $\binom nk = 0$ for $k > n$ (Graham, Knuth, Patashnik, *Concrete Mathematics* 5.1) |
| l7 | quiz[1] | `inv_fact[k] * k % p` | correct | as screens[3] |
| l7 | quiz[2] answer 15; slips 81, 6 | $\binom62$ | correct | script |
| l7 | quiz[3] | one build of about $2\cdot10^6$ multiplications plus $2\cdot10^5$ for the queries | correct | count of loop bodies |
| l8 | screens[0] states, generic route, explain | token game from 3, 2, 1: nine reachable positions, none with six in one box | correct | script: breadth-first search of the move graph gives the same nine states and every listed edge |
| l8 | screens[1] options, hints, explain | $(A-B) \bmod 3 = 1$ in every row and 0 at the target; the total is invariant but shared by the target; $A \bmod 2$ changes | correct | script; Engel, *Problem-Solving Strategies*, ch. 1 (the invariance principle) |
| l8 | screens[2] order | a move adds 1 to every box modulo 3, so differences are fixed; start 1, target 0 | correct | $-2 \equiv 1 \pmod 3$ |
| l8 | screens[3] answer 30; slips 31, 32; shade list; explain | mutilated chessboard: opposite corners share a colour, 30 against 32, each domino covers one of each | correct | Engel ch. 2 (colouring proofs); script counts the shade list |
| l8 | screens[4] options, hints, explain | $x, y \to \lvert x-y\rvert$ changes the sum by $2\min(x,y)$; sum 23 is odd; the last number is 1, 5 or 7 | correct | script plays every order |
| l8 | screens[5] prose, options, explain | $(x,y) \to (x+y,y)$ or $(x,x+y)$ keeps the gcd; (7,5) is reachable by the walk back; the falling sum is a monovariant | correct | $\gcd(x+y,y) = \gcd(x,y)$ (Knuth 4.5.2); script |
| l8 | screens[6] key, options, explain | (2,7) is not reachable from (3,2) though the gcds agree; each pair with $x \ne y$ has one parent | correct | forward moves never shrink a coordinate; script (search with bound) |
| l8 | screens[7] solution, how, explain | Euclid-style walk back with `%`, exact stop at the start; about 90 steps at $10^{18}$; one subtraction at a time needs $10^{18}$ turns on test 11 | correct | script compares an independent walk back with a forward search (starts up to 5, targets up to 14) and runs the fifteen tests |
| l8 | screens[8] solution, how | parity of the sum; empty board 0; seed 3 gives 0 | correct | script |
| l8 | screens[9] prose, options | invariant and monovariant defined; differing invariants rule a target out, agreeing ones prove nothing | correct | Engel ch. 1 |
| l8 | screens[10] key l4; hints, feedback, explain | cash + shares × fill price is unchanged by a fill; buy line holds (10,000 = 8,440 + 30·52); sale gives 10,090 before and 9,540 after, shares should be 20 | correct | arithmetic in script |
| l8 | summary.* | as above | correct | as above |
| l8 | quiz[0] | 1 to 10 sums to 55, odd, so never 0 | correct | script |
| l8 | quiz[1] | corners on one side differ in colour: 31 each, and a tiling does exist | correct | explicit tiling: three horizontal dominoes finish the top row, the other rows tile in pairs |
| l8 | quiz[2] answer 1; slips 0, 2 | $(B-A) \bmod 3 = 2$ | correct | arithmetic |
| l8 | quiz[3] | (10,4) has gcd 2; walk back stalls at (2,2) | correct | script |
| l9 | screens[0] key l2, l4; feedback l1, l3, l5, l6; explain | for n = 4 only 2 4 1 3 and 3 1 4 2 have no neighbours differing by 1; several right answers need a checker | correct | script enumerates all 24 orders; Codeforces checkers (testlib) |
| l9 | screens[1] frames, options, explain | evens then odds fails only at n = 2 and 3; inside a block gaps are 2, the joint gap is at least 3 once $n \ge 4$ | correct | script checks the pattern for n up to 2,000 |
| l9 | screens[2] options, explain | two kinds of neighbouring pair, so checking both is a proof; examples are not | correct | derivation |
| l9 | screens[3] key, explain | n = 3 has no answer: 2 has no allowed neighbour; n = 2 has none either | correct | script (exhaustive) |
| l9 | screens[4] canvas verdicts, multi key | checker tests length, each number once, the gaps, and −1 only when no order exists; it never compares with the jury's order | correct | script validates the six listed outputs |
| l9 | screens[5] solution, prelude checker, how, explain | −1 for n in (2, 3), else evens then odds; O(n) | correct | script; grade-all |
| l9 | screens[6] options, hints, explain | `permutations` yields lexicographic order, so $(n-2)!$ orders starting 1, 2 come first and all fail; memory stays small | correct | Library Reference, `itertools.permutations` ("lexicographic order ... emitted lazily") |
| l9 | screens[7] options, explain | n integers in [1, k] with sum s exist iff $n \le s \le nk$; raising one number by 1 reaches every sum between | correct | discrete intermediate-value argument; script exhaustive for small n, k |
| l9 | screens[8] solution, how, explain | give each number `min(k-1, extra)`; first numbers end at k, at most one between, rest 1; test 9 has extra about $1.5\cdot10^9$ | correct | script; $1500000007 - 200000$ |
| l9 | screens[9] key B, C; options; explain | six children in [100, 250] summing to 1,000; feasible iff $600 \le s \le 1500$ | correct | script sums each row |
| l9 | summary.* | recipe and bounded-sum rule | correct | as above |
| l9 | quiz[0] | 1 3 5 4 2 is invalid; the other three have the gaps listed | correct | script |
| l9 | quiz[1], quiz[2] | any valid order is accepted; `no_adjacent(1)` is `[1]` | correct | as above |
| l9 | quiz[3] answer 10; slips 12, 9 | s from 3 to 12 | correct | script |
| l10 | screens[0] key B, D, F; slips {C,F}, {A}; feedback mA, mC, mE; explain | six meetings: at most three fit, and only B, D, F do | correct | script enumerates all 64 subsets |
| l10 | screens[1] frames, options, explain | shortest first keeps F, C (2); earliest start keeps A (1); earliest finish keeps B, D, F (3) | correct | script runs the three rules |
| l10 | screens[2] prose, options, explain | exchange argument: greedy's first meeting ends no later than OPT's first, so the swap keeps the count and adds no overlap; repeating it gives optimality | correct | Kleinberg and Tardos, *Algorithm Design*, 4.1 (statements 4.2, 4.3); CLRS Theorem 15.1 (3rd ed. 16.1) |
| l10 | screens[3] answer 2; slips 3, 1; explain | touching ends: `s >= end` against `s > end`; the statement decides | correct | script under both rules |
| l10 | screens[4] solution, tests, how, explain | sort by end, keep when `s >= end`; $O(n\log n)$; random test keeps 11,256; test 1 breaks sort-by-start and sort-by-length | correct | script: greedy against exhaustive search on 400 random sets; expectations, 11,256 included, recomputed by a DP |
| l10 | screens[5] answer 3; slips 6, 2; derive caption; explain | fewest rooms = most meetings in progress at once; opening a room only when all are busy never needs more | correct | Kleinberg and Tardos 4.1 (interval partitioning, statement 4.6); script |
| l10 | screens[6] solution, prose, how, explain | sweep over `(s, 1)`, `(e, -1)` events; `(5, -1)` sorts before `(5, 1)`; random peak 144 | correct | tuple ordering (Language Reference 6.10.1); script recomputes every expectation, 144 included, with a heap of end times |
| l10 | screens[6].hints[2] | a min-heap of end times also works (`ds` lesson 17) | correct | Kleinberg and Tardos 4.1; lesson title checked by grep |
| l10 | screens[7] options, canvas, explain | coins 1, 3, 4: largest-first is right for 1 to 5 and wrong first at 6 (4+1+1 against 3+3); 7 and 8 are fine | correct | script (greedy against DP) |
| l10 | screens[8] solution, prelude, tests, how, explain | stress loop keeping the smallest failing amount, first if tied; expectations for seeds 1 to 4; coins 1, 2, 5, 10 never fail | correct | script recomputes the seven expectations and the first failure `([1,5,8],15)` |
| l10 | screens[9] prose, options, explain | greedy shape `sorted(items, key=KEY)`; the swap is safe only if greedy's choice ends no later; A ends at 13 and overlaps D and F | correct | as screens[2] |
| l10 | screens[10] answer 4; slips 3, 8; explain | eight windows: earliest finish fills 2, 3, 5, 8; earliest start fills 3 (order 1 blocks four) | correct | script (greedy and exhaustive) |
| l10 | summary.* | key choice, exchange, proof or stress test | correct | as above |
| l10 | quiz[0] | (3,4) ends first and overlaps both others | correct | inspection |
| l10 | quiz[1] answer 3; slips 2, 4 | touching allowed | correct | script |
| l10 | quiz[2] | coins 1, 5, 10, 20, 25: 40 is paid 25+10+5 by greedy, 20+20 is better; greedy is right up to 30 | correct | script: first failure at 40 |
| l10 | quiz[3] answer 3; slips 4, 2 | peak just after 2 | correct | script |
| l11 | screens[0] key B, D; slips AB, CD, ABC, D; feedback r0, r2; explain | four trades, limit 6: B and D give £11k; 16 subsets | correct | script enumerates the 16 subsets |
| l11 | screens[1] grid, answer 3; slips 6, 2; explain | bit i set means item i is in; subsets of n items are the numbers 0 to $2^n-1$ | correct | Knuth, *TAOCP* vol. 4A, 7.1.3; script |
| l11 | screens[2] prose, canvas, key 1, 14, 2, 2; feedback | `mask >> i & 1` reads, OR with `1 << i` adds, `mask & -mask` isolates the lowest set bit, `bin(mask).count("1")` counts; shifts bind tighter than the bitwise AND and OR | correct | Language Reference 6.17 (precedence); Knuth 7.1.3 eq. (37); script evaluates all four |
| l11 | screens[2].explain | `int.bit_count()` from Python 3.10; `__builtin_popcount` in C++ | correct | What's New in Python 3.10; GCC and Clang built-ins, compiled in sweep |
| l11 | screens[3] solution, tests, how | all masks, all bits: $O(2^n n)$; expectations 5895 and 6848 | correct | script (knapsack DP over risk, independent of masks) |
| l11 | screens[3].explain | $2^{16}\cdot16 \approx 10^6$ bit checks about 0.1 s in the app's Python, n = 20 about 2.5 s; C++ handles $n \le 20$ | correct | timing-dependent; measured in sweep under Pyodide |
| l11 | screens[4] answer 8; slips 15, 16; explain | `1 << n - 1` is `1 << (n - 1)`; in C++ `mask & 1 << i == 0` parses as `mask & ((1 << i) == 0)` | correct | Language Reference 6.17; ISO C++ [expr.eq] above [expr.bit.and]; compiled probe in sweep |
| l11 | screens[5] solution, tests, explain | subsets by position; empty set counts for target 0; `sums[mask ^ low]` makes it $O(2^n)$ | correct | script recomputes the ten expectations by counting ways per sum (independent of masks) |
| l11 | screens[6] solution, tests, explain | `p[m] = p[m >> 1] + (m & 1)`; sum for n = 18 is $18\cdot2^{17} = 2{,}359{,}296$ | correct | script |
| l11 | screens[7] answer 10240; slips 9!, 1024; canvas; explain | Held-Karp: state (mask, end city), $2^n n$ states and $2^n n^2$ steps; $2^{16}\cdot16^2 \approx 1.7\cdot10^7$ | correct | Held and Karp (1962), "A dynamic programming approach to sequencing problems"; arithmetic in script |
| l11 | screens[8] prose, answer $2^{21}$ (6% band); slips $2^{40}$, $2^{20}$; explain | meet in the middle: two halves of $2^{20}$ subsets, one sorted by risk with a running best profit, the other binary searching; $2^{40} \approx 1.1\cdot10^{12}$ | correct | Horowitz and Sahni (1974); script runs the method against the mask loop for n = 16 |
| l11 | screens[8].explain | a sum version for n = 40 took about 2 s in the app's Python | correct | timing-dependent, recorded as such (order of magnitude measured in sweep) |
| l11 | screens[9] prose, canvas, answer 27; slips 64, 8; explain | `sub = (sub - 1) & mask` steps to the next smaller submask; pairs (mask, submask) number $3^n$; $3^{16} \approx 4.3\cdot10^7$ | correct | Knuth 7.1.3 (exercise on submask enumeration); script |
| l11 | screens[10] answer 63; slips 64, 720, 6; explain | $2^6-1$ non-empty combinations; $2^{30} \approx 10^9$; `x > 0 and (x & (x - 1)) == 0` tests a power of two | correct | script; Warren, *Hacker's Delight*, 2-1 |
| l11 | summary.* | $\sum_{\text{mask}} 2^{\text{popcount}} = 3^n$ | correct | binomial theorem, $(1+2)^n$ |
| l11 | quiz[0] | 13 = 1101: A, C, D; the three distractors are 11 read backwards, 14 and 5 | correct | script |
| l11 | quiz[1] | OR adds; XOR flips; `& ~(1 << i)` removes; `>> i & 1` tests | correct | Knuth 7.1.3 |
| l11 | quiz[2] | `range(1 << n)`; `range(2 ** n - 1)` misses the full set | correct | script |
| l11 | quiz[3] answer 8; slips 3, 7 | 10110 has three set bits | correct | script |
| l12 | screens[0] answer $2\cdot10^{10}$; slips $n+q$, q; explain | the range loop makes up to $q\cdot n$ additions | correct | arithmetic |
| l12 | screens[1] steps, answer 3; slips 6, −2; explain | $+v$ at l and $-v$ at $r+1$; running total 0, 3, 5, 5, 5, 3, 3, 1; $O(n+q)$ in place of $O(nq)$ | correct | script replays the three updates both ways |
| l12 | screens[2] prose, key c2, c6; feedback | difference array: cell i is the change from day $i-1$ to day i, the inverse of a prefix sum | correct | Halim sec. 2.4 note on difference arrays; cp-algorithms "Prefix sums and difference arrays"; lesson reference checked by grep |
| l12 | screens[3] options, explain | $n+1$ cells: the largest index written is $r+1 = n$, never read; with $l = r$ the marks are neighbours | correct | derivation; `IndexError` reproduced in script |
| l12 | screens[4] solution, tests, how, explain | two writes an update and one pass; counting test sees 500 reads; test 8's range loop would be about $5\cdot10^9$ additions; checksum 404786420 | correct | script recomputes the checksum with independent reference code (sorted events) and the total range length, $5.0\cdot10^9$ |
| l12 | screens[5] canvas, options, explain | without $-v$ every update runs to the last day; the sample's updates both end on day 7 so it passes; (1,4,+3) shows the bug | correct | script runs the buggy version on both |
| l12 | screens[5].explain | a stress test finds it within ten random cases almost every time | correct | Monte Carlo in script: 20,000 runs of ten cases (n from 1 to 8, 1 to 4 updates, v non-zero), detection above 99.9% |
| l12 | screens[6] answer 3; slips 4, 5; derive; explain | counts by day 1, 2, 3, 3, 3, 3, 3, 3, 2, 1; (0,3) and (4,9) share no day | correct | script |
| l12 | screens[7] solution, tests, how, explain | inclusive ends, $-1$ at $r+1$; peak 49,889; intervals average about 66,500 days, so filling is about $6.6\cdot10^9$ steps | correct | script recomputes the peak and the mean length (expected $n/3$) |
| l12 | screens[8] prose, canvas, options, explain | 2-D update marks four corners: $+v$, $-v$, $-v$, $+v$; a $-v$ at the far corner would leave $-2v$ | correct | inclusion-exclusion; script applies the four marks and two passes on a 5 by 5 grid |
| l12 | screens[9] answer 400; slips 0, 600; explain | position is the running total of fills; an option's exposure has both ends | correct | arithmetic |
| l12 | summary.* | as above | correct | as above |
| l12 | quiz[0] | difference list 5, −2, 0, −5, 2, 0; the three distractors as described | correct | script |
| l12 | quiz[1] answer 3; slips 5, −2 | both updates cover day 2 | correct | script |
| l12 | quiz[2] | marks after the running total are lost | correct | derivation |
| l12 | quiz[3] | all updates then one pass is the difference array's case; interleaved queries need a Fenwick or segment tree; fixed-array range sums are prefix sums | correct | Halim sec. 2.4.3, 2.4.4 |
| l12 | screens[4].widget.how; tests[6] | "at most 2,500 [reads] pass" | imprecise | the test is `0 < update_reads(...) <= 2500`: a correct linear pass that reads through `reversed(updates)` or `updates.copy()` counts 0 reads and fails test 7 with the "far more than 2,500" line (sweep); finding 5 |
| review-1 | items[0] | $10^9\cdot10^9 = 10^{18}$ fits long long if the multiply is 64-bit | correct | arithmetic; [expr.arith.conv] |
| review-1 | items[1] | $n \le 2000$: $n^2\log_2 n \approx 4.4\cdot10^7$ fits, $n^3 = 8\cdot10^9$ is eighty times the budget | correct | script |
| review-1 | items[2] answer 5; slips 3, 4 | token walk: n = 3 at index 1, values at 2 to 4 | correct | script-style walk; slip 3 is the line index, slip 4 the last value's index |
| review-1 | items[3] | `[5,5,1]`, k = 10: sums 10, 6, 6; `[5,5]` keeps the bug | correct | script |
| review-1 | items[4] | clearing a $10^6$ array for each of $10^4$ tests is $10^{10}$; `memset` does not change the count; clear what was used | correct | arithmetic |
| review-1 | items[5] | `a.count(x)` in a loop is $O(n^2)$, $4\cdot10^{10}$; `Counter` makes it $O(n)$ | correct | TimeComplexity (list count O(n)) |
| review-1 | items[6] | `int('\n')` raises ValueError; `read().split()` ignores blank lines | correct | script |
| review-1 | items[7] | a generator must reach the statement's minimum n | correct | derivation |
| review-1 | items[8] answer $2\cdot10^6$ (10% band); slips $10^{11}$, $10^5$ | $10^5$ binary searches of about 20 comparisons | correct | script |
| review-2 | items[0] | C++ `(3 - 5) % 7` is $-2$; `(a - b + p) % p` is 5 | correct | wasm32 probe in sweep |
| review-2 | items[1] answer 18; slips 54, 2 | gcd(252, 198) by Euclid; $252 = 14\cdot18$, $198 = 11\cdot18$ | correct | script |
| review-2 | items[2] answer 333333336 | $3^{-1} = (p+1)/3$ | correct | script |
| review-2 | items[3] answer 4; slips 3, 1; explain | $10^{18} \equiv 4 \pmod 6$, $3^4 = 81 \equiv 4$; exponent reduction modulo $p-1$ needs p prime and not dividing the base | correct | script (`pow(3, 10**18, 7)`; the slip 3 is the exponent taken modulo 7); Hardy and Wright Theorem 71 |
| review-2 | items[4] answer 15; slips 16, 14 | primes up to 50 | correct | script |
| review-2 | items[5] answer 60; slips 240, 2, 12 | lcm(4, 6, 10) | correct | script |
| review-2 | items[6] answer 286; slips $4^{10}$, 120, 715 | $\binom{13}{3}$ | correct | script |
| review-2 | items[7] | tables modulo 7 fail for $\binom81$: $7! \equiv 0$ has no inverse and `pow` returns 0 | correct | script (`pow(0, 5, 7)`) |
| review-2 | items[8] | from 4, 1, 1 the invariants agree with the target, yet (6,0,0) has no parent; 7 reachable positions | correct | script (search) |
| review-2 | items[9] answer 5; slips 6, 0 | walk back from (12, 7) | correct | script |
| review-3 | items[0] | $n = 4$, $k = 5$: answers exist for $4 \le s \le 20$ | correct | as l9 screens[7] |
| review-3 | items[1] solution, checker, explain | ring of n: alternate a, b, add c when n is odd, −1 for n = 1 | correct | script (another valid string through the checker); 3-colouring of an odd cycle (Diestel, *Graph Theory*, 5.1) |
| review-3 | items[2] answer 4; slips 2, 6 | earliest finish keeps B, C, D, E; earliest start keeps 2 because (0,7) blocks four | correct | script |
| review-3 | items[3] answer 10; slips 15, 7 | coins 1, 5, 6: first failure at 10 (five coins against two); 15 is five against three | correct | script |
| review-3 | items[4] | B, C, E is 22; 13, 26, 20 as described | correct | script |
| review-3 | items[5] | C++ `x & (x - 1) == 0` is `x & ((x - 1) == 0)`: false for 8; Python's comparison binds looser than `&` | correct | wasm32 probe in sweep; Language Reference 6.17 |
| review-3 | items[6] answer 1; slips 6, −6, 2 | difference list 2, 0, 5, −6, 0, 0, −1; running total 2, 2, 7, 1, 1, 1 | correct | script |
| review-3 | items[7] | pattern matching: difference array, bitmask, earliest finish, prefix sums, BFS | correct | as the lessons; BFS for unit-cost shortest paths (CLRS 22.2) |
| homework-1 | items[0] solution, tests, how, explain | pairs with sum exactly k by a dictionary of earlier counts, $O(n)$; 9,998,990 and $\binom{200000}{2} = 19{,}999{,}900{,}000$ | correct | script (Counter formula, independent of the pass) |
| homework-1 | items[1] solution, tests, how, explain | sliding window with counts; each fill enters once and leaves at most once; 22 on the random test | correct | script (last-position window, independent) |
| homework-1 | items[2] solution, tests, how, explain | prefix sums, `pre[r] - pre[l - 1]`; expectations of the random test | correct | script |
| homework-1 | items[3] order | read, restate, budget, design, code, test, submit, write up | correct | convention of the level, each step uses the one before |
| homework-1 | items[4] model, rubric | window is correct because a window with more than k tickers stays so when widened, so the left end never moves back; $O(n)$ time, $O(k)$ memory; the never-deleted key crashes on `['C','A','B']`, k = 1 | correct | monotonicity of distinct count; script-style trace of the buggy version (KeyError at left = 2) |
| homework-1 | items[5] | sort once, two binary searches a query; about $1.1\cdot10^7$ steps; `bisect_left` for L and `bisect_right` for U | correct | Library Reference, `bisect`; arithmetic in script |
| homework-1 | items[6] answer $4\cdot10^{10}$; slips $2\cdot10^5$, $4\cdot10^5$ | `set(xs)` inside the loop is rebuilt per query | correct | arithmetic |
| homework-1 | items[7] | small stress cases never reach the overflow: $\binom62 = 15$ against about $2\cdot10^{10}$ | correct | script |
| homework-2 | items[0] prose, solution, tests, explain | $G(n) = \sum_i \gcd(i,n)$ is multiplicative with $G(p^a) = (a+1)p^a - a\,p^{a-1}$; $G(10^{12}) = 74{,}200{,}000{,}000{,}000$ | correct | Pillai's function, $G(n) = \sum_{d\mid n} d\,\varphi(n/d)$ (Hardy and Wright 16.2 for $\varphi$); script evaluates the divisor sum for all ten tests |
| homework-2 | items[1] prose, solution, tests, feedback, explain | Legendre: $Z(k) = \sum \lfloor k/5^i\rfloor$, non-decreasing; $Z(24) = 4$, $Z(25) = 6$; $Z(5m) \ge m$ bounds the search; about 43 halvings of about 18 terms | correct | Hardy and Wright Theorem 416; script (independent search) |
| homework-2 | items[2] order, explain | proof of Fermat by the rearrangement $a, 2a, \dots, (p-1)a$ | correct | Hardy and Wright Theorem 71, first proof (6.1) |
| homework-2 | items[3] model, rubric | gcd invariant, forced walk back, monovariant, `%` with an exact stop, about 90 steps | correct | as l8 screens[5] to [7]; script |
| homework-2 | items[4] answer 9; slips 1, 3 | $3^3 \equiv 1 \pmod{13}$, $200 = 3\cdot66+2$; $200 \bmod 12 = 8$ gives the same | correct | script |
| homework-2 | items[5] answer 28; slips 91, 55 | at least 2 each: $\binom82$ | correct | script; Feller II.5 |
| homework-2 | items[6] | 5, 3, 1: $(A-B) \bmod 3 = 2$, target 0 | correct | arithmetic |
| homework-3 | items[0] solution, tests, explain | fewest points stabbing all closed windows: sort by end, alert at the end of each uncovered window; 35,817 on the random test | correct | CLRS exercise 16.2-5 (points covered by unit intervals, the same greedy); the exchange proof in the model answer, checked line by line; script (mirror-image greedy, independent) |
| homework-3 | items[1] solution, tests, explain | stock span with a falling stack, pop on `<=`, $O(n)$; sums 20,000,100,000 and 18,188,896 | correct | script (value-and-span stack, independent) |
| homework-3 | items[2] solution, tests, how, explain | every $v \ge 1$, so "over after k updates" is monotone; binary search with a difference array, about 17 checks; 36,515, 72,568 and −1 | correct | script (independent bracket search) |
| homework-3 | items[3] order | exchange proof of earliest finish in six lines | correct | Kleinberg and Tardos 4.1 |
| homework-3 | items[4] model, rubric | exchange proof for the alerts: move the alert in the earliest-ending window to its end; every window that held it still does | correct | derivation checked line by line: a window containing $t \le e$ starts by e and ends at or after e |
| homework-3 | items[5] answer 49152; slips 12!, 4096; explain | $2^{12}\cdot12$ pairs, of which $12\cdot2^{11} = 24{,}576$ are a desk inside its mask | correct | script |
| homework-3 | items[6] | shift by one is a derangement for every $n \ge 2$; reverse and neighbour swaps leave a fixed point for odd n | correct | inspection at n = 3 |
| homework-3 | items[7] | all bookings before any output: a difference array; the loop is up to $4\cdot10^{10}$ | correct | as l12 |
| homework-3 | items[8] model: main proof | earliest due date order minimises the worst lateness: swap the greedy's job up to the first difference; every job in positions k to m ends by T and is due no earlier than g | correct | Jackson's rule (Jackson 1955); Kleinberg and Tardos 4.2 (statements 4.7 to 4.10); script: exhaustive check on 300 random instances |
| homework-3 | items[8] model: other route | adjacent inversion swap; orders with no inversion share the worst lateness | correct | Kleinberg and Tardos (4.8), (4.9) |
| homework-3 | items[8] model: assumptions | with ready times due order loses (4 against 0); the never-wait rule loses too (3 against 0); for total lateness due order loses (8 against 5) while the worst is 4 against 5 | correct | script recomputes all six schedules |
| homework-3 | items[1].widget.how; tests[6] | "at most 10,000 [reads] pass" | imprecise | same lower bound, `0 < reads_for(...)`: a correct stack on `closes.copy()` or over `reversed(closes)` fails test 7 (sweep); finding 5 |

## Code feedback sweep: every `feedback.byKey.test-N` line (98 lines)

For each line that names a mistake, two or three natural codings of that mistake were submitted to the page's own grader; the line is `correct` when most of them fail test N first. A line that only describes its test is `correct` when the description is true.

| file | JSON path | claim (short) | verdict | basis: codings and first failing test |
|---|---|---|---|---|
| l1 | screens[9].feedback.byKey.test-2 | no final newline: reading by lines may lose or break the last line | correct | 3 codings (strip last char; drop last split line; `l[:-1]` per line): all first fail test 2 |
| l1 | screens[9].feedback.byKey.test-3 | trailing blank lines: `split()` ignores them, `split('\n')` does not | correct | 2 codings reading line pairs to the end (after `split('\n')` or `splitlines()`): first fail test 3 |
| l1 | screens[9].feedback.byKey.test-4 | blank lines between test cases: read tokens, not lines | correct | line reader that takes t pairs: first fails test 4 |
| l1 | screens[9].feedback.byKey.test-7 | `tokens.pop(0)` shifts the list each call | correct | timing-dependent: `pop(0)` coding stopped after 5 s on test 7 (tests 1 to 6 pass); a re-slicing coding passes in 3 s |
| l1 | screens[10].feedback.byKey.test-3 | all equal: use `>`, not `>=` | correct | 2 codings (`>=` with None, with −inf): first fail test 3 |
| l1 | screens[10].feedback.byKey.test-5 | all losses: best started at 0 | correct | best = 0 and best = −1: first fail test 5 |
| l1 | screens[10].feedback.byKey.test-6 | `if not best` treats 0 as no best | correct | coding first fails test 6 (returns 4) |
| l1 | screens[10].feedback.byKey.test-9 | `max(xs[:i])` each day is $O(n^2)$, about $2\cdot10^{10}$ | correct | timing-dependent: 2 codings stopped on test 9 only |
| l2 | screens[9].feedback.byKey.test-6 | n = 465: compute the step count, the table's 500 is a rule of thumb | correct | 2 of 3 codings that use 500 first fail test 6; a coding with every table threshold fails test 3 (n = 26) first and gets the generic line |
| l2 | screens[9].feedback.byKey.test-7 | n = 500 gives `"n^2"` | correct | describes the test; true ($500^3 > 10^8$) |
| l2 | screens[9].feedback.byKey.test-15 | `2 ** n` at $10^{18}$ never ends; check n first | correct | timing-dependent: 3 unguarded codings pass tests 1 to 14 (test 13 and 14 take 0.5 to 0.7 s) and are stopped on test 15 |
| l2 | screens[10].feedback.byKey.test-1 | a sum equal to k counts: `<=` | correct | strict coding first fails test 1 (returns 2) |
| l2 | screens[10].feedback.byKey.test-3 | do not remove duplicates | correct | `sorted(set(xs))` first fails test 3 |
| l2 | screens[10].feedback.byKey.test-5 | a value above k can pair with a negative one | correct | 2 codings that drop or skip values above k first fail test 5 |
| l2 | screens[10].feedback.byKey.test-8 | far more than 20,000 reads: every pair | correct | 2 double loops on the given list first fail test 8 |
| l2 | screens[10].feedback.byKey.test-9 | every pair is $2\cdot10^{10}$ steps | correct | timing-dependent: 2 double loops on a copy or on slices pass test 8, stopped on test 9 |
| l3 | screens[8].feedback.byKey.test-3 | `\r\n`: `split()` removes them, `split(b'\n')` does not | correct | 2 codings (split on newline then space; newline to space) first fail test 3 with `int(b'\r')` |
| l3 | screens[8].feedback.byKey.test-6 | a list is not an iterator | correct | list coding first fails test 6 (TypeError) |
| l3 | screens[8].feedback.byKey.test-7 | `__iter__` must return self | correct | class coding first fails test 7 |
| l3 | screens[9].feedback.byKey.test-4 | no final newline: reading lines may not handle it | correct | 2 codings (`line[:-1]`; `split('\n')[:-1]`) first fail test 4 |
| l3 | screens[9].feedback.byKey.test-5 | blank line and values over two lines | correct | `input()` per line and `readlines` by index first fail test 5 |
| l3 | screens[9].feedback.byKey.test-7 | one call per test case goes too deep | correct | recursive coding: RecursionError on test 7 only (limit 3000, $10^4$ cases) |
| l3 | screens[10].feedback.byKey.test-1 | maximum started at 0 | correct | YoWASP clang 21, wasm32, run under node WASI: first fails test 1 |
| l3 | screens[10].feedback.byKey.test-3 | sum past an int | correct | same toolchain: `int` sum and `long` sum (4 bytes on wasm32) first fail test 3 |
| l3 | screens[10].feedback.byKey.test-4 | all losses, no final newline: −12 and −3 | correct | describes the test; true |
| l3 | screens[10].feedback.byKey.test-6 | sums $5\cdot10^9$ and $-2\cdot10^9$ | correct | describes the test; true |
| l4 | screens[7].feedback.byKey.test-2 | one `Random(seed)`, `gen` once per trial | correct | rng inside the loop and an unseeded rng first fail test 2; calling `gen` twice fails test 1 (generic line) |
| l4 | screens[7].feedback.byKey.test-4 | run exactly `trials` trials | correct | `range(trials + 1)` first fails test 4 |
| l4 | screens[7].feedback.byKey.test-7 | cases are ints: `list(case)`, `case[:]` fail | correct | both codings first fail test 7 (TypeError) |
| l4 | screens[7].feedback.byKey.test-9 | fast function sorted the case: deep copy | correct | no copy and `copy.copy` first fail test 9 |
| l4 | screens[8].feedback.byKey.test-1 | brute force on `[1,2,3]`, 4 gives 2 | correct | real pytest harness in CPython: `<` and ordered-pair brutes first fail test 1 |
| l4 | screens[8].feedback.byKey.test-5 | test fails on the correct function | correct | assertion reversed: first fails test 5 |
| l4 | screens[8].feedback.byKey.test-6 | passes the `<` version: assert `is None`, brute must not call the fast function | correct | no assert; brute calling the fast function; values too large for ties: all first fail test 6 |
| l4 | screens[8].feedback.byKey.test-10 | bug only for k below 0: let k go negative | correct | k from 0 up; the lesson's generator; positive values with negative k: all first fail test 10 |
| l9 | screens[5].feedback.byKey.test-1 | n = 1: `[1]` is valid | correct | −1 below 4: first fails test 1 |
| l9 | screens[5].feedback.byKey.test-2 | n = 2: return −1 | correct | no special case: first fails test 2 |
| l9 | screens[5].feedback.byKey.test-3 | n = 3: return −1 | correct | only n = 2 special: first fails test 3 |
| l9 | screens[5].feedback.byKey.test-8 | a search over orders already takes seconds for 8 to 12 | correct | timing-dependent: `permutations` search passes tests 1 to 7, stopped on test 8 |
| l9 | screens[5].feedback.byKey.test-9 | a search cannot finish at $10^5$ | correct | recursive backtracking passes 8 to 12, RecursionError on test 9 |
| l9 | screens[8].feedback.byKey.test-4 | k = 1: every number is 1 | correct | describes the test; true |
| l9 | screens[8].feedback.byKey.test-6 | s = 6 above nk = 5 | correct | no upper check: first fails test 6 |
| l9 | screens[8].feedback.byKey.test-7 | s = 3 below n = 4 | correct | no lower check: first fails test 7 |
| l9 | screens[8].feedback.byKey.test-8 | s = 16 above nk = 15 | correct | describes the test; true |
| l9 | screens[8].feedback.byKey.test-9 | about $1.5\cdot10^9$ raises one at a time | correct | timing-dependent: add-one coding stopped on test 9 only |
| l10 | screens[4].feedback.byKey.test-1 | sort by start keeps only A; by length too few | correct | both codings first fail test 1 (1 and 2) |
| l10 | screens[4].feedback.byKey.test-2 | touching is allowed: `>=` | correct | `>` first fails test 2 |
| l10 | screens[4].feedback.byKey.test-6, test-7 | (0,100) contains both others; (4,7) overlaps both others; answers 2 | correct | describe the tests; true (script) |
| l10 | screens[4].feedback.byKey.test-8 | compare with the last kept end only | correct | timing-dependent: check against every kept meeting, and an $O(n^2)$ DP, stopped on test 8 only |
| l10 | screens[6].feedback.byKey.test-2 | end before start at a tie | correct | start-first tie and closed-interval count first fail test 2 |
| l10 | screens[6].feedback.byKey.test-3 | three identical meetings need 3 rooms | correct | `set(intervals)` first fails test 3 |
| l10 | screens[6].feedback.byKey.test-7 | every time point or every pair is too slow | correct | timing-dependent: both codings stopped on test 7 only |
| l10 | screens[8].feedback.byKey.test-1 | returning the first failure gives `([1,5,8],15)` | correct | coding returns exactly that on test 1; script recomputes it |
| l10 | screens[8].feedback.byKey.test-5 | ten trials, none fails: call `gen` ten times | correct | `range(trials + 1)` and one extra call first fail test 5 with `(None, 11)` |
| l10 | screens[8].feedback.byKey.test-7 | coins 1, 2, 5, 10 never fail: run all 300 | correct | early-stop coding first fails test 7 with `(None, 100)` |
| l11 | screens[3].feedback.byKey.test-1 | exactly at the limit: `<=` | correct | `<` first fails test 1 (9); so does `1 << n - 1` |
| l11 | screens[3].feedback.byKey.test-2 | no trades: the empty set, profit 0 | correct | masks from 1 with `max` of a list or best None: first fail test 2 |
| l11 | screens[3].feedback.byKey.test-3 | nothing fits: the empty set, 0 | correct | n = 0 special-cased, masks from 1: first fails test 3 |
| l11 | screens[3].feedback.byKey.test-5 | only trade uses exactly the limit | correct | describes the test; true |
| l11 | screens[5].feedback.byKey.test-2 | empty list, target 0: 1 | correct | masks from 1: first fails test 2 |
| l11 | screens[5].feedback.byKey.test-3 | `[5]`, target 0: only the empty set | correct | empty list special-cased, masks from 1: first fails test 3 |
| l11 | screens[5].feedback.byKey.test-4 | `[2,2,2]`: one subset per pair of positions | correct | distinct value sets: first fails test 4 |
| l11 | screens[5].feedback.byKey.test-5 | a negative value: −1 + 2 counts | correct | knapsack over sums 0 to target first fails test 5; a pruning recursion fails test 10 (generic line) |
| l11 | screens[6].feedback.byKey.test-1 | n = 0 gives `[0]` | correct | list started at `[0, 1]`: first fails test 1 |
| l11 | screens[6].feedback.byKey.test-8 | no `bin` or `bit_count` | correct | both codings pass tests 1 to 7, fail test 8 |
| l12 | screens[4].feedback.byKey.test-1 | last update ends on the last day: $n+1$ cells | correct | n cells: IndexError on test 1 |
| l12 | screens[4].feedback.byKey.test-2 | l = r = 2: +7 at 2, −7 at 3 | correct | describes the test; true |
| l12 | screens[4].feedback.byKey.test-3 | running sum must include day 0 | correct | sum from day 1: first fails test 3 |
| l12 | screens[4].feedback.byKey.test-7 | far more than 2,500 reads: every update for each day | correct | per-day scan first fails test 7 (500,000 reads). The same line is shown to a correct pass that makes no counted read (`reversed(updates)`), see finding 5 |
| l12 | screens[4].feedback.byKey.test-8 | looping over each range is billions of additions | correct | timing-dependent: range loop passes test 7, stopped on test 8; $5.0\cdot10^9$ additions (script) |
| l12 | screens[7].feedback.byKey.test-1 | (0,2) and (2,4) share day 2: −1 at $r+1$ | correct | −1 at r and a half-open sweep first fail test 1 |
| l12 | screens[7].feedback.byKey.test-3 | no intervals: 0 | correct | `max` over an empty list: first fails test 3 |
| l12 | screens[7].feedback.byKey.test-7 | intervals average about 66,500 days: mark the ends | correct | timing-dependent: fill coding stopped on test 7; mean 66,499.6 (script) |
| review-3 | items[1].feedback.byKey.test-1 | n = 1 is its own neighbour: −1 | correct | no n = 1 case: first fails test 1 |
| review-3 | items[1].feedback.byKey.test-3 | alternating a, b puts a beside a for n = 3 | correct | alternate-only coding first fails test 3 |
| review-3 | items[1].feedback.byKey.test-9 | n = 99,999: `ab` 49,999 times then `c` | correct | describes the test; true |
| homework-1 | items[0].feedback.byKey.test-2 | count how many earlier values match, not whether one does | correct | set coding first fails test 2 (3) |
| homework-1 | items[0].feedback.byKey.test-9 | far more than 4,000 reads: every pair | correct | index double loop first fails test 9 |
| homework-1 | items[0].feedback.byKey.test-10 | `xs.count(k - x)` in a loop, unseen by the counter | correct | timing-dependent: coding passes test 9 (24 ms), stopped on test 10 |
| homework-1 | items[0].feedback.byKey.test-11 | counting pairs one by one is too slow | correct | timing-dependent: 2 codings pass test 10 in about 1 s, stopped on test 11 |
| homework-1 | items[1].feedback.byKey.test-1 | count distinct tickers, not fills | correct | `min(k, n)` first fails test 1 |
| homework-1 | items[1].feedback.byKey.test-8 | k = 5, three tickers: whole list | correct | describes the test; true |
| homework-1 | items[1].feedback.byKey.test-9 | far more than 4,000 reads: restart at every day | correct | restart coding on the given list first fails test 9 |
| homework-1 | items[1].feedback.byKey.test-11 | restart costs $2\cdot10^{10}$ when the window is everything | correct | timing-dependent: restart on a copy passes tests 9 and 10, stopped on test 11 |
| homework-1 | items[2].feedback.byKey.test-1 | positions from 1, both ends | correct | 0-based and right-end-out codings first fail test 1 |
| homework-1 | items[2].feedback.byKey.test-6 | `sum(xs[l - 1:r])` a query is about $10^{10}$ steps | correct | timing-dependent: stopped on test 6 only |
| homework-3 | items[0].feedback.byKey.test-2 | an alert at 10 misses (2,3): sort by end | correct | sort by start with a containment check first fails test 2 (returns 2) |
| homework-3 | items[0].feedback.byKey.test-3 | ends are included: `s > last` | correct | `s >= last` first fails test 3 |
| homework-3 | items[0].feedback.byKey.test-7 | sorted by start, (1,20) puts the first alert at 20 and `s > last` skips the rest | correct | that exact coding passes tests 1 to 6 and returns 1 on test 7 |
| homework-3 | items[0].feedback.byKey.test-9 | keep only the last alert time | correct | timing-dependent: checking every alert stopped on test 9 only |
| homework-3 | items[1].feedback.byKey.test-2 | pop on `<=` | correct | `<` first fails test 2 |
| homework-3 | items[1].feedback.byKey.test-7 | walking back on rising prices is about $n^2/2$ reads | correct | walk-back coding first fails test 7 |
| homework-3 | items[1].feedback.byKey.test-8 | $2\cdot10^{10}$ steps on 200,000 rising closes | correct | timing-dependent: walk back on a copy passes test 7, stopped on test 8 |
| homework-3 | items[2].feedback.byKey.test-1 | exactly 5 is not above the cap: `> cap` | correct | `>=` first fails test 1 (returns 2) |
| homework-3 | items[2].feedback.byKey.test-3 | never exceeds: check all updates first | correct | search with no check first fails test 3 (returns 2) |
| homework-3 | items[2].feedback.byKey.test-4 | every day at exactly 5: −1 | correct | describes the test; true |
| homework-3 | items[2].feedback.byKey.test-8 | rebuilding after every update is $O(nq)$ | correct | timing-dependent: 2 codings pass tests 1 to 7, stopped after 25 s on test 8 |
| homework-3 | items[2].feedback.byKey.test-10 | cap $10^9$ is never reached: −1 | correct | describes the test; true |
