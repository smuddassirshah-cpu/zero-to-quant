# contests level 2 (Contest maths): report

A container restart stopped the content agent before it reported, and its generators were lost. This report comes from a triage pass: every file was read in full, every stated number was recomputed independently, every code widget was run in CPython against both starter and solution, and the fixes below were made as targeted string edits (the JSON files round-trip byte for byte through a loader and writer, so nothing else moved). The level is kept.

## Files

All in `app/content/courses/contests/`.

| File | Screens or items | Quiz | Code screens | Notes |
|---|---|---|---|---|
| `l5-modulo.json` | 12 screens (difficulty 1 to 3) | 5 | 3: `power_mod` (with a multiplication counter), `inverse_mod`, C++ `mul_mod` | skill `cn-maths` |
| `l6-gcd-and-primes.json` | 12 screens | 4 | 3: `gcd` and `gcd_all`, `sieve`, `factorise` | skill `cn-maths` |
| `l7-counting-mod.json` | 12 screens | 4 | 3: `build_tables`, `n_choose_k`, `count_queries` | skill `cn-maths` |
| `l8-invariants.json` | 11 screens | 4 | 2: `can_reach`, `final_parity` | skill `cn-maths`; one `order` derive |
| `review-2.json` | 10 items: 2 at difficulty 2, 4 at 3, 4 at 4 | | | three items on l5, three on l6, two on l7, two on l8 |
| `homework-2.json` | 7 items: 2 at difficulty 3, 4 at 4, 1 at 5 | | 2: `gcd_sum` (d5), `smallest_k` (d4) | one `order` (Fermat's little theorem, d4); one `longform` (d4, 10-point rubric, full model answer) |

Interactive canvases: l5 a ring graph (seats mod 7), tables for last digits and the multiplication table mod 7; l6 a draggable point on a number-line (gear wheels), a `manipulate` Euclid step, a 10 by 10 sieve grid; l7 a lattice grid with editable counts bound to cells, an array for choosing up-steps, factorial tables; l8 a `manipulate` token game on `boxes`, a chessboard grid, an `order` proof.

Edge cases present: l5 $a \equiv 0$ (no inverse, `ValueError`), $e = 0$, $m = 1$, negative inputs in C++; l6 $\gcd(0, a)$, 1 is not prime, $n < 2$, a prime left after the loop; l7 $k > n$, $k < 0$, $n = 0$, $n \ge p$ (review); l8 the target equal to the start, an empty board, the walk-back shortcut stopping exactly at the start.

## Validator

`node tools/validate.mjs`: 0 errors, 328 warnings overall. Warnings on these six files: nine "a ladder screen usually reuses the previous canvas kind" (code ladders move between console, table, array and grid) and one "a point hint usually highlights the canvas" (l6 screen 7). None is an error.

## Playthrough

`node tools/playthrough.mjs --lesson ... --set ... --why --local-cdn <scratchpad>/pkgs`, run before and after the fixes, all green both times:

- l5-modulo: ok, 17 checks, quiz 5/5
- l6-gcd-and-primes: ok, 16 checks, quiz 4/4
- l7-counting-mod: ok, 16 checks, quiz 4/4
- l8-invariants: ok, 15 checks, quiz 4/4
- review-2: ok, 10 of 10 recorded
- homework-2: ok, 7 of 7 items, 33 of 33 marks
- l7 and l8 also played with `--mobile` (390 px): ok. Screenshots looked at: l5 explore, l6 gears and sieve, l7 lattice grid and binomial tree, l8 boxes, chessboard and the nine-row table on a phone. No empty canvas, overlap or console error.

## Numbers checked

Each number was recomputed in CPython by a different method from the solution (scratchpad `contests-2/verify.py`, `v2.py`), and the playthrough is the second, Pyodide computation against the same literals. All agree, except the corrections listed under fixes.

- l5: last digits of powers of 7 (7, 9, 3, 1, 7; $7^{2031}$ ends in 3); $38 \cdot 45 = 1710 \equiv 2 \pmod 7$; the full mod-7 multiplication table and every inverse; $3^5 \equiv 5$; $3^{13} \equiv 3$; $3^{100000} \bmod p = 916{,}902{,}199$; $2^{10^{18}} \bmod p = 719{,}476{,}260$; $(10^{18})^{10^{18}+3} \bmod p = 512{,}064{,}609$; $2^{-1} = 500{,}000{,}004$; $123456789 \cdot 987654321 \bmod p = 259{,}106{,}859$; $10^{18} \equiv 49$, so 147 and 2,401; the checksum 4,591 (and 4,588 and 31,000,004,808 for the two slips); $10^{18}$ has 60 bits, so at most 120 multiplications.
- l6: $\operatorname{lcm}(84, 36) = 252$; Euclid on 1071 and 462 gives 21; `steps(89, 55)` is 9; $F_{88} = 1{,}100{,}087{,}778{,}366{,}101{,}931$ and $F_{87}$ take 86 steps and have gcd 1; 78,498 primes up to $10^6$; 148,933 up to $2 \cdot 10^6$; the sum of primes below 1,500,000 is 82,074,443,256; 25 primes up to 100 and 10 up to 30 and 15 up to 50; 1,000,003 is prime and $\lfloor\sqrt{1{,}000{,}003}\rfloor = 1000$; 999,983, 1,000,003 and 999,999,999,989 are prime (Miller-Rabin); the sieve grid's dimmed set and tappable set match multiples of 2, 3, 5 exactly; $\operatorname{lcm}(14, 21) = 42$.
- l7: all counts on the 4 by 4 lattice; $\binom63 = 20$; $\binom{2000}{1000}$ has 601 digits and is 72,475,738 mod $p$; mod 13 tables ($n! = 1, 1, 2, 6, 11, 3, 5$; inverses 1, 1, 7, 11, 6, 9, 8) and $\binom63 \equiv 7$; $1{,}000{,}000! \bmod p = 641{,}102{,}369$; $\binom{1000}{500} \equiv 159{,}835{,}829$; $\binom{10^6}{5 \cdot 10^5} \equiv 996{,}692{,}777$ (also by `math.comb`) and has 301,027 digits; the seed-7 random query sum 555,553,024 (by a different table construction); $\binom{7}{2} = 21$, $\binom62 = 15$, $\binom{10}{6} = 210$, $5040$, $1024$; $\binom{252}{126}$ has 75 digits.
- l8: BFS over the token game gives exactly 9 reachable positions, none is $(6, 0, 0)$, and $(A - B) \bmod 3 = 1$ on all nine; from $(4, 1, 1)$ there are 7; the difference game from 3, 5, 6, 9 gives only 1, 5 or 7; random-order play confirms the parity invariant; `can_reach` agrees with a BFS on every start from 1 to 8 and every target to 60 (0 mismatches), and the large cases follow from gcd 1 and arithmetic progressions; the seed-3 parity is 0; the backtest line values 10,090, 9,540, 10,000.
- Review: $\gcd(252, 198) = 18$; $3^{-1} = 333{,}333{,}336$; $3^{10^{18}} \equiv 4 \pmod 7$; $\operatorname{lcm}(4, 6, 10) = 60$; $\binom{13}{3} = 286$, $4^{10} = 1{,}048{,}576$, $\binom{10}{3} = 120$, $\binom{13}{4} = 715$; $(12, 7)$ is 5 moves from $(1, 1)$.
- Homework: $G(n) = \sum_i \gcd(i, n)$ for $n \le 1000$ and 720,720 by direct sum; $G(2^{40}) = 23{,}089{,}744{,}183{,}296$, $G(10^{12}) = 74{,}200{,}000{,}000{,}000$, $G(999983 \cdot 1000003) = 3{,}999{,}939{,}999{,}825$, $G(999999999989) = 1{,}999{,}999{,}999{,}977$ (also as $\sum_{d \mid n} d\varphi(n/d)$); `smallest_k` for $m \le 25$ against a factorial brute force, and $m = 10^{12} - 1$ and $10^{12}$ (4,000,000,000,005 and 4,000,000,000,010) by Legendre's digit-sum form; $3^{200} \equiv 9 \pmod{13}$; $\binom82 = 28$, 91, 55.

Pyodide 0.27.7 under Node in this sandbox (CPython 3.13 in brackets; quoted as "about"):
- $10^7$ additions: 1.4 s (0.5 s).
- `build_tables` to $10^6$: 0.27 s; one `pow` per entry: 2.9 s (0.29 s and 1.1 s).
- `math.comb(10**6, 5 * 10**5)`: 6.8 s (4.1 s).
- Trial division of every number to $\sqrt n$ up to $10^6$: 6.0 to 6.7 s (2.1 to 3.4 s). Trial division by primes only: 1.1 s.
- Sieve to $2 \cdot 10^6$: 0.25 s, with the inner loop starting at $p^2$ or $2p$ alike.
- `count_queries` on $10^5$ queries: 0.4 s.

## Starters, solutions and slow solutions

CPython harness (`contests-2/harness.py`) runs prelude, code, postlude and each case as the widget describes.

- All 12 Python solutions pass every hidden case. All 12 are also green in the Pyodide playthrough (every code widget is checked against its `solution`).
- Every Python starter fails every value case. Two starters pass exactly one case, which checks the source and not a value: `power_mod` test 8 (`'pow(' not in __learner_source__`) and `gcd` test 11 (`'math' not in __learner_source__`). Recorded in the inbox.
- C++ `mul_mod` was compiled with g++ -std=c++17 -O1 and driven with the eight cases: the solution passes all 8; the starter (int variables) passes 4 and fails the negative-input, $10^9 + 6$ and $10^{18}$ cases, as intended.
- Slow solutions rejected:
  - Loops of $e$ or $a$ turns (`power_mod`, `gcd`, `can_reach`, `smallest_k`, `factorise` to $n$, `gcd_sum` by direct sum) need $10^{12}$ to $10^{18}$ steps and cannot finish.
  - `power_mod`'s multiplication counter fails a loop at test 7, before the $10^{18}$ case.
  - Trial division of every number takes 6 s or more at $10^6$ and about 18 s at $2 \cdot 10^6$ in Pyodide, over the 5 s case limit.
  - `math.comb` per query takes 6.8 s for one query at $\binom{10^6}{5 \cdot 10^5}$ and far longer for $10^5$ random ones. On a fast machine test 6 could pass, test 7 cannot, so the `how` now says "test 6 or 7".
  - One `pow` per inverse factorial (a correct but slower solution) passes inside the 10 s budget on purpose; the `how` says so.
  - `final_parity` simulated with a list scan per move is $O(n^2)$ at $n = 2 \cdot 10^5$ and is stopped; a heap or stack simulation is correct and fast, which is acceptable.

## Fixes made

Wrong numbers or claims:
1. l6 screen 8 explanation said a sieve starting at $2p$ took "about 0.7 s against 0.45 s" in Pyodide. Measured: both about 0.25 s at $n = 2 \cdot 10^6$. Rewritten to say it is correct and costs almost nothing.
2. l7 screen 9 hint: $\binom{10^6}{5 \cdot 10^5}$ has 301,027 digits, not 301,028.
3. l7: "about 10 s" for one `math.comb` at $n = 10^6$ is about 7 s (screen 9 option, lesson summary trap).
4. l7 screen 6: the build took about 0.3 s and one `pow` per entry about 3 s in Pyodide (was 0.4 s and 4 s); still ten times.
5. l7 quiz item 3: the queries cost $2 \cdot 10^5$ multiplications (two per query), not $3 \cdot 10^5$.
6. l5 screen 8: two residues multiply to "at most about $1.0 \cdot 10^{18}$", since $(10^9 + 6)^2$ is slightly above $10^{18}$ (was "under").
7. Homework item 1: "$Z(k) \ge k/5$" is false for non-multiples of 5; now "$Z(5m) \ge m$", which gives the same bound. The feedback's "about 45 halvings" is about 43 ($\log_2(5 \cdot 10^{12}) = 42.2$).
8. l7 `how` for `count_queries`: `math.comb` is "stopped at test 6 or 7".

Graded-answer routing (the only change to anything graded):
9. Review item 3 ($3^{10^{18}} \bmod 7$): the two `wrong[]` values were swapped. Reducing the exponent modulo 7 gives 3 (key `mod7`), and an exponent that is a multiple of 6 gives 1 (key `e0`); the file had 1 and 3. The correct answer, 4, is unchanged.
10. Review item 2 ($3^{-1} \bmod p$): the `decimal` wrong value 0.3333 had tolerance 0, so 0.333 never matched; tolerance is now 0.001.

Voice (sentences under 20 words, three-sentence explanations): about 25 long sentences split or shortened in `explain`, prose, hints, `how` lines, the l8 summary idea, the homework longform prompt and model answer. No wording that states a number changed beyond the items above. Checked clean: no exclamation marks (the `!` in `n!` and `k!` is maths), no em-dashes, no American spellings, no emoji, £ in the l8 backtest and no other money.

Graded answers changed: none of the correct answers; two wrong-answer routing values (item 9) and one tolerance (item 10).

## Brief must-haves

- l5: last-digit table hook; ring graph; inverse table mod 7; Fermat's inverse; repeated squaring derive; `power_mod` with a multiplication counter; `inverse_mod` with `ValueError`; C++ `mul_mod` with the compile-time note; traps for dividing a remainder and for C++ negative `%`; $a \equiv 0$ and $e = 0$; the checksum transfer; why $10^9 + 7$ (quiz).
- l6: gear wheels and lcm; Euclid by hand and as `manipulate`; the Fibonacci worst case; the 10 by 10 sieve; a sieve for the course's own Project Euler-style problem (primes below 1,500,000, not Project Euler's); trial division to $\sqrt n$ trap; $\gcd(0, a)$, 1 not prime, $n < 2$; `gcd`, `sieve`, `factorise` with size and near-$10^{12}$ prime cases; rebalance-calendar transfer.
- l7: lattice routes; factorial and inverse-factorial tables; stars and bars; `build_tables`, `n_choose_k`, `count_queries` with $10^6$ and $10^5$-query size cases; `math.comb` trap; per-entry `pow` explained; Pascal's rule when the modulus is not prime; binomial-tree transfer.
- l8: the token game; chessboard dominoes; the difference game; a gcd invariant with a walk back; the trap that an invariant is not a route; `can_reach` to $10^{18}$; `final_parity` at $2 \cdot 10^5$; monovariant named; backtest conservation transfer.
- Homework: two `code` items (difficulty 5 `gcd_sum`, a Project Euler-style problem of the course's own; difficulty 4 binary search on the answer to $m = 10^{12}$), an `order` item (Fermat's little theorem), a `longform` with a 10-point rubric and a full model answer. No Project Euler problem or answer is used.

## Open issues

- The playthrough runs solutions only. Starters were checked by the CPython harness (and g++ for C++), not in the browser.
- l5 and l6 each have a source-check case that the starter passes; see the inbox.
- l8 screen 1's nine-row table scrolls inside 300 px, so two rows are hidden on a phone; see the inbox.
- l7 screen 0 says "1,000 by 1,000 grid of streets" and uses 3 by 3 for a 4 by 4 lattice of corners. Both mean blocks, so the 1,000 case is $\binom{2000}{1000}$; the wording is consistent but a learner could read "streets" as lines.
- The timing figures are from Pyodide under Node on this machine, and a browser will differ. No test depends on a time except through the 5 s case limit; the slow methods listed are far over it, apart from the single `math.comb` case noted above.

## Proposed course.json change

None.

## Engine limits

Three bullets appended to `docs/BACKLOG-INBOX.md` under "Raised later (contests level 2)": source-check cases pass on the starter; table canvas row count on a phone; operation counting sees only overridden operators.
