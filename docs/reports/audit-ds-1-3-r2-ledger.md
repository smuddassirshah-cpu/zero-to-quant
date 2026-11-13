# Claim ledger: ds L1 to L3, round 2 blind audit (13 Nov 2026)

Scope: `app/content/courses/ds/` lessons l1 to l13, review-1 to review-3, homework-1 to homework-3. Stage 1, full depth.

Key to paths: `sN` is `screens[N]`, `qN` is `quiz[N]`, `iN` is `items[N]`, `w` is `widget`, `fb` is `feedback`, `opt` is `widget.options`. A row that names several keys of one screen covers one claim restated in those keys; each was read and checked.

Key to basis: "script X" is a check in `docs/reports/ds-L1-3-r2-concepts.py` (sections A to F; CPython 3.13.18, with Pyodide 0.27.7 values read by node where they differ). "A" means the widget's solution passes every hidden test and its starter fails, in that script and in `grade-all.mjs` under Pyodide. CLRS is Cormen, Leiserson, Rivest and Stein, *Introduction to Algorithms*, 3rd ed. "Py docs" is the Python 3.12 documentation.

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l1 | s0.prose | An array keeps equal-width items side by side; an 8-byte float; base 1000 | correct | CLRS 10.3; IEEE 754 binary64 is 8 bytes |
| l1 | s0.w.answer, accept, hints, fb.correct | `prices[4]` starts at 1000 + 4 × 8 = 1032 | correct | derivation; script B l1 s0 |
| l1 | s0.w.wrong, fb.byKey | 1040 is five steps, 1004 adds the index alone, 1024 is `prices[3]` | correct | 1000 + 40, 1000 + 4, 1000 + 24; script B |
| l1 | s0.explain | item i is at base + i × size; earlier items are never visited | correct | derivation |
| l1 | s1.w.answer, hints, fb, explain | inserting at index 2 of five moves indices 2, 3, 4, shifting from the back | correct | script B shifts(5, 2) = 3; back-first order avoids overwriting |
| l1 | s2.w.rows, fb.correct, explain | insert at i moves n − i values: 5, 3, 0; `append` cheap, `insert(0, v)` not | correct | script B; Py docs TimeComplexity (list insert O(n)) |
| l1 | s3.opt, fb, explain | read touches 1 value, front insert shifts 1,000,000; O(1) against O(n); doubling n doubles the insert | correct | derivation; script F (insert(0) loop quadratic) |
| l1 | s3.opt[3].why | 500,000 is an average over positions; a front insert always shifts all | correct | n − 0 = n |
| l1 | s4.prose | a full block cannot grow in place; the values move to a bigger block | correct | CLRS 17.4 table expansion (worst case of realloc; model stated as a supposition for doubling) |
| l1 | s4.w.answer, hints, fb.correct | capacity 1, doubling, 16 appends: 1 + 2 + 4 + 8 = 15 copies | correct | script B doubling_copies(16) = 15 |
| l1 | s4.w.wrong, fb.byKey | 120 copies on every append; 16 one each; 31 adds a 16th-append copy | correct | 0 + … + 15 = 120; 15 + 16 = 31; script B |
| l1 | s4.explain | with doubling, copies are always under twice the appends; O(1) amortised | correct | CLRS 17.4; script C (k = 1 to 2,999) |
| l1 | s4.explain | Python grows lists by about an eighth; total stays linear | correct | CPython `Objects/listobject.c` list_resize; script C (ratios 1.10 to 1.15, copies < 10n) |
| l1 | s5.prose, w.answer, hints, fb | `insert(0, t)` for 1,000 ticks shifts 0 + … + 999 = 499,500 | correct | script B |
| l1 | s5.w.wrong, fb.byKey | 1,000 one step each; 1,000,000 is n²; 500,500 sums 1 to 1,000 | correct | script B |
| l1 | s5.explain | n(n − 1)/2 shifts; append then one `reverse()` is O(n) and gives the same list | correct | script D, F |
| l1 | s6.prose | a list stores 8-byte pointers; each float is a separate 24-byte object; NumPy stores 8-byte values | imprecise | true on 64-bit CPython (`sys.getsizeof(1.0)` = 24). The app's own Python is Pyodide on wasm32: pointer 4 bytes, float object 16 bytes (measured with node). Finding 2 |
| l1 | s6.w.answer, accept, hints, fb, wrong | (8 + 24) × 10⁶ bytes = 32 MB; 8 MB pointers only; 24 MB objects only | imprecise | arithmetic right under the 64-bit premise; same unstated premise. Finding 2 |
| l1 | s6.w.accept | the list header of a few bytes is too small to matter | correct | 56 bytes on 64-bit, against 32,000,000 |
| l1 | s6.explain | `xs[i]` is O(1) plus one hop; NumPy uses a quarter of the memory; its loops run in C | imprecise | quarter holds only at 8 + 24 against 8 (64-bit); in Pyodide 20 against 8. Finding 2 |
| l1 | s7.prose | a string cannot change; `s += piece` builds a new string and copies the old one | correct | Py docs "Common sequence operations" note 6 (immutable concatenation is quadratic) |
| l1 | s7.w.answer, hints, fb | 1,000 lines of 10 characters: 10 + 20 + … + 10,000 = 5,005,000 | correct | script B |
| l1 | s7.w.wrong, fb.byKey | 10,000 counts each character once; 10,000,000 counts the full report every line | correct | script B |
| l1 | s7.explain | `join` sizes the result once; CPython sometimes grows a string in place, with no promise | correct | Py docs note 6; CPython `unicode_concatenate` in-place case |
| l1 | s8.prose | cost table: index O(1), append O(1) amortised, pop O(1), insert O(n − i), pop(0) O(n), `in` O(n) | correct | Py docs TimeComplexity; script C, F |
| l1 | s8.opt, fb, explain | `pop(0)` is the O(n) one; `xs[-1]`, `len`, `append` are O(1) | correct | same; list stores its length (`ob_size`) |
| l1 | s9.prose, w, hints, fb, explain | `",".join(f"{p:.2f}" for p in prices)`; join of `[]` is `''`; 99.999 formats to 100.00 | correct | A; script D |
| l1 | s10.prose, opt[0], hints, explain | `deque(maxlen=20)` with `append` drops the oldest in O(1); a deque is cheap at both ends | correct | Py docs collections.deque; script D, F |
| l1 | s10.opt[1].why, fb.flip | `insert(0, close)` with `pop()` moves the shift to the insert | correct | Py docs TimeComplexity |
| l1 | s10.opt[2].why, fb.slice | `window[1:] + [close]` is "still about 20 copies per tick" | imprecise | the slice copies 19 pointers and `+` copies 20 more into a third list: 39. Finding 3 |
| l1 | s10.opt[3].why | `remove(window[0])` matches on its first comparison, then shifts the rest | correct | script D; list.remove scans from index 0 |
| l1 | summary.ideas, formula, trap | address(i) = base + i × size; insert shifts n − i; `+=` in a loop recopies; `insert(0, x)` loop is O(n²) | correct | rows above |
| l1 | q0 | `insert(3, v)` on 10 values shifts 7; slips 3, 6, 10 | correct | script B |
| l1 | q1 | `[][0]` raises `IndexError: list index out of range`; `append(5)` works | correct | script D; Pyodide run |
| l1 | q2 | `s[0] = "B"` raises `TypeError: 'str' object does not support item assignment`; `"B" + s[1:]` is `"BOD"` | correct | script D; Pyodide run |
| l1 | q3 | 4-byte ints from 2000: `a[10]` at 2040; slips 2010, 2044, 2080 | correct | script B |
| l2 | s0.prose, w.answer, hints, fb, explain | toy hash: letter-place sum mod 5; VOD 41 → 1, BP 18 → 3, HSBA 30 → 0; hash function, hash table | correct | script B toy(); CLRS 11.2 |
| l2 | s1 | AZN is 41 → bucket 1: a collision; the bucket keeps both and a lookup compares keys | correct | script B; CLRS 11.2 chaining |
| l2 | s2.w.answer, wrong, fb | finding AZN costs 2 comparisons (VOD, then AZN); 4 compares every key; 1 forgets VOD | correct | chaining in arrival order, as the prose states |
| l2 | s2.explain | few keys per bucket gives O(1) on average for lookup, insert, delete; Python's dict probes other slots instead | correct | CLRS Theorems 11.1, 11.2; CPython `Objects/dictobject.c` (open addressing); script C |
| l2 | s3.prose caption | GSK 37, RIO 42, TSCO 57, BT 22 all leave 2 | correct | script B |
| l2 | s3.opt, fb, explain | all n keys in one bucket: a lookup is O(n); O(1) is an average, not a promise | correct | CLRS 11.2 worst case Θ(n); script C (one-bucket keys cost over n/8 comparisons on average) |
| l2 | s3.opt[2].why, opt[3].why | an unsorted bucket cannot be halved; O(n²) would be n such lookups | correct | derivation |
| l2 | s4 | nested loop over two lists of 10,000: 10⁸ comparisons; slips 20,000, 10,000, 5 × 10⁷; `set(b)` gives about 20,000 steps | correct | script B |
| l2 | s5.opt, hints, explain | `not in` on a list over 2,000,000 distinct ids: about n²/2 = 2 × 10¹² comparisons | correct | script B |
| l2 | s5.opt[2].why, opt[3].why | 4 × 10⁷ is n log₂ n; 4 × 10¹² is n² | correct | script B (4.19 × 10⁷) |
| l2 | s6.prose | a key's hash must never change; hashable means, in practice, cannot change | correct | Py docs glossary "hashable"; hedged by "in practice" |
| l2 | s6.opt, hints, explain, q1 | str, int, tuple of them are keys; list and dict raise `TypeError: unhashable type: 'list'` | correct | script D; Pyodide run |
| l2 | s6.fb.correct, summary.ideas[2] | "Strings, numbers and tuples are keys" | imprecise | a tuple that holds a list is unhashable: `{(1, [2]): 0}` raises. The explain says "tuples of them". Finding 11 |
| l2 | s7 | `set(b_list)` costs O(m) once; n checks at O(1) each; O(n + m) replaces O(nm); set, dict, Counter all hash keys | correct | CLRS 11.2; Py docs |
| l2 | s8 | `duplicates`: two sets, `sorted(dups)`; O(n) on average | correct | A |
| l2 | s8.fb.byKey | test 1 expects `['BP', 'VOD']`; test 4 is BARC three times | correct | tests[0], tests[3] read |
| l2 | s9 | 500-pair scan with `break`, uniform ticker: (1 + 500)/2 = 250.5 per row, 250,500,000 in all; slips 5 × 10⁸, 10⁶; `dict(ref)` | correct | script B; expected position of a uniform match |
| l2 | summary.formula, trap | O(n·m) → O(n + m); `x in seen` on a list is a loop | correct | rows above |
| l2 | q0 | `{}["VOD"]` raises `KeyError: 'VOD'`; `get` returns `None` or the default; Counter returns 0 | correct | script D |
| l2 | q1.opt[3].why | the list key fails before any bucket is chosen | correct | hashing precedes lookup; TypeError from `hash()` |
| l2 | q2 | BARC: 24 → bucket 4; slips 24 and 5 (24/5 rounded) | correct | script B |
| l2 | q3 | `set(a) & set(b)` is O(n) on average; list `in` is O(n²); `x in sorted(b)` is worse than O(n²) | correct | n sorts of n log n each; Py docs TimeComplexity (set intersection) |
| l3 | s0.prose, w, fb | prices 3, 8, 5, 12, 6: exactly one pair makes 17, indices 2 and 3; slips 3 + 8 = 11, 5 + 6 = 11 | correct | script B (all 10 pairs) |
| l3 | s0.explain | "Only 5 finds its partner, 12, in the list"; complement defined as 17 − x | imprecise | 12 finds its partner 5 as well. Finding 4 |
| l3 | s1 | brute force checks n(n − 1)/2 pairs: 10 for 5; 499,500 for 1,000; O(n²); slips 25, 20, 5 | correct | script B |
| l3 | s2.steps | one pass with `seen`: 14, 9, 12 absent; at i = 3 need 5, found at 2; return (2, 3) | correct | script D two_sum |
| l3 | s3 | 6, 1, 9, 4, 7 with target 13 returns (2, 3), before 7 is read | correct | script D |
| l3 | s4 | `seen` is `{6: 0, 1: 1, 9: 2}` on reaching index 3; value is the key, index the value | correct | trace |
| l3 | s5 | store-first version returns (0, 0) for `([3, 4, 1], 6)`; the membership test never raises | correct | script D |
| l3 | s6.prose | "One pass of O(1) dict steps: O(n) time, O(n) extra memory" | imprecise | O(1) per dict step is an average (CLRS 11.2); l2 says so, l3 and later lessons drop it. Finding 13 |
| l3 | s6.opt, explain | check-first version returns (0, 1) for `([3, 3], 6)` | correct | script D |
| l3 | s7 | sorted 2, 4, 5, 8, 11, 13 with target 16: sums 15, 17, 15, 16; ends at indices 2 and 4; O(n), no extra memory | correct | script D |
| l3 | s7.explain | a sum below the target means `lo` is too small for any partner left | correct | x_lo + x_k ≤ x_lo + x_hi < t for k ≤ hi |
| l3 | s8 | `two_sum` code; tests; "Tests 5 and 6 have fewer than two numbers"; test 9 is 100,000 numbers | correct | A; tests read |
| l3 | s8.fb.byKey | test 3 `[3, 3]`; test 4 no pair; test 6 `[5]` with target 10 | correct | tests[2], [3], [5] |
| l3 | s9 | costs 1,250, 830, 2,100, 1,670, 420 with target 2,500 return (1, 3); target 0 finds netting trades | correct | script D |
| l3 | summary | n(n − 1)/2; check before store; indices not values; two pointers on sorted data | correct | rows above |
| l3 | q0 to q3 | 499,500 pairs; `two_sum([5], 10)` is `None`; `[300, -100, 200, -300]` gives (0, 3); `(need, x)` returns (2, 7) | correct | script B, D |
| l4 | s0, s1 | tally VOD 3, BP 2, AZN 1; `counts.get(t, 0) + 1`; HSBA never becomes a key; O(n) | correct | script D |
| l4 | s2 | anagrams have equal frequency maps; `treads`; `traders` has two r's; counting O(n), sorting O(n log n) | correct | script D; CLRS 8.2 counting against comparison sorting |
| l4 | s3 | rule: case and spaces count; `""`/`""` are anagrams; `Listen`/`silent` and `dirty room`/`dormitory` are not | correct | stated convention; script D |
| l4 | s4 | `counts[t] += 1` on an empty dict raises `KeyError: 'VOD'`; fixes are `get`, `defaultdict(int)`, `Counter` | correct | script D |
| l4 | s5 | sorted letters as a canonical key: aert, abt, aet | correct | script D |
| l4 | s6.prose | `Counter(fills)` is O(n); `most_common(1)` is `[('VOD', 3)]`; `defaultdict(int)` starts at 0 | correct | script D; Py docs collections |
| l4 | s6.opt[0..2], explain | `Counter(a) == Counter(b)` is O(n); sorting is right but O(n log n); sets are linear but wrong | correct | script D (`set('trades') == set('traders')`) |
| l4 | s6.opt[3].why | `all(a.count(c) == b.count(c) for c in a)` is O(n²) | misleading | true, but the check is also wrong (`'ab'`, `'abc'` pass), and the screen flags only the set version as wrong. Finding 12 |
| l4 | s7 | `is_anagram`, `group_anagrams`; sorted groups in a sorted list; a sorted list cannot be a key | correct | A; script D |
| l4 | s7.fb.byKey | tests 2, 4, 5, 6 as described | correct | tests[1], [3], [4], [5] |
| l4 | s8 | `fills_per_venue`: a set skips resends, a dict counts; LSE 2, CHIX 1, BATS 1; "LSE 3" if resends count | correct | A; o1 twice plus o3 |
| l4 | summary | frequency map; anagram test; canonical key; `+=` trap | correct | rows above |
| l4 | q0 | `set("trades") == set("traders")` is `True` | correct | script D |
| l4 | q1 | `Counter("banana").most_common(1)` is `[('a', 3)]`; always a list of pairs | correct | script D; Py docs |
| l4 | q2 | reading a missing key of `defaultdict(int)` inserts it: prints `0 2` | correct | script D |
| l4 | q3 | `groups[sorted(w)]` raises `TypeError: unhashable type: 'list'`; `tuple(sorted(w))` works | correct | script D |
| l5 | s0 | sorted 1, 3, 4, 6, 8, 11, 15, target 10: 1 + 15 = 16, so 15 has no partner; `j` moves | correct | every pair with 15 is at least 16 |
| l5 | s1.w.states, hints, fb.byKey, explain | walk j, j, i, j, i; sums 16, 12, 9, 11, 9, 10; wrong moves give 18, 14, 7, 12, 7; dropped 15, 11, 1, 8, 3; 21 pairs in all | correct | script B |
| l5 | s2 | no pair for 20: sums 16, 18, 19, 21, 17, 19; at most n − 1 sums; pointers meet on 11; O(n) against O(n²) | correct | script B, D (random sorted lists) |
| l5 | s3 | palindrome check on `refer`: 2 comparisons; `noon` 2; loop `while i < j` | correct | ⌊n/2⌋; script B |
| l5 | s4 | squares of a sorted list: biggest square is at one end; fill from the back; result 1, 4, 9, 16, 36, 49 | correct | x² is convex, so the maximum over an interval is at an end; script D |
| l5 | s5.prose | "We have reached `i` on 4 and `j` on 8" | imprecise | the correct walk passes (1, 8) → (3, 8) → (3, 6) → (4, 6); it never stands on (4, 8). Finding 5 |
| l5 | s5.opt, hints, fb, explain | from (4, 8), moving `i` loses 4 + 6; then 6 + 8 = 14, `j` moves, pointers meet on 6; moving `j` was safe | correct | trace; 8 + x ≥ 12 for x ≥ 4 |
| l5 | s6 | code; O(n) time, O(1) space; needs sorted input; `i < j` so no number is used twice; `[5]` with `<=` returns (0, 0) | correct | A (s7); trace |
| l5 | s7 | `two_sum_sorted`, `is_palindrome` (letters only, case ignored, empty is a palindrome) | correct | A |
| l5 | s7.fb.byKey, how | tests 4, 7, 9, 12; 7 + 8 tests; one test of 100,000 numbers | correct | tests read; `range(0, 200000, 2)` has 100,000 items |
| l5 | s8 | P&Ls −120 … 135, target 50: sums 15, 60, 15, 50; indices 2 and 5; 10,000 trades: 9,999 sums against about 50 million | correct | script B |
| l5 | summary | pointer rule; O(n) time, O(1) space; unsorted input breaks it silently | correct | rows above; q0 |
| l5 | q0 | `two_sum_sorted([8, 3, 5, 1, 9], 10)` prints `None`: sums 17, 9, 4, 6 | correct | script B |
| l5 | q1 | the full-range swap loop restores `[3, 8, 1, 9, 4]` | correct | script D |
| l5 | q2 | palindrome check on six payoffs: 3 comparisons; a strangle's payoff 10, 5, 0, 0, 5, 10 | correct | ⌊6/2⌋; put at 100 and call at 105 on a 90 to 115 grid give those payoffs (Hull ch. 12, strangle) |
| l5 | q3 | `two_sum_sorted([5], 10)` is `None`; an empty list gives `j = -1` | correct | A tests |
| l6 | s0 | window sum 13 slides to 13 − 4 + 1 = 10; slips 14, 9, 3; two operations whatever the width | correct | script B |
| l6 | s1 | six sums 13, 10, 16, 12, 17, 14; best starts on day 4 | correct | script B |
| l6 | s2 | scratch: 981 × 20 = 19,620; sliding: 20 + 2 × 980 = 1,980; with w = 250 about a hundred times | correct | script B (ratio 107) |
| l6 | s3 | shortest run with sum ≥ 7 on positives: record 4, shrink from the left; each day enters and leaves once: O(n) | correct | script E (positive lists against brute force) |
| l6 | s4 | lengths recorded 4, 4, 3, 3, 2; answer 2 (`[4, 3]`); shrinking is safe because numbers are positive | correct | script B |
| l6 | s5 | `last` dict; second `b` moves `left` to `last['b'] + 1 = 2`; longest is `cbdae`, 5 | correct | A (s8 test `abcbdae`) |
| l6 | s6 | version without `max` returns 3 for `abba` (window `bba`) and passes `abcbd` | correct | script D |
| l6 | s7 | fixed window update `total += xs[right] - xs[right - w]`; index `right - w` leaves | correct | A (s8) |
| l6 | s8 | `max_window_sum`, `longest_unique`; `best` starts from the first window | correct | A |
| l6 | s8.fb.byKey, how | tests 4, 5, 6, 8; test 6 is about 3.6 billion additions from scratch; two tests of 200,000 items | correct | 180,001 × 20,000 = 3.6 × 10⁹ |
| l6 | s9.prose | pandas `vol.rolling(5).sum().max()` runs this loop under the hood | correct | pandas `_libs/window/aggregations.pyx` roll_sum (add and remove per step) |
| l6 | s9.w, hints, fb | totals 2370, 2340, 2660, 2800, 2490, 2520; best 2800 (days 4 to 8); slips 2370, 2950 | correct | script B |
| l6 | s9.explain | the same loop over daily log returns finds the best 20-day return | correct | log returns add over time (Tsay, *Analysis of Financial Time Series*, 1.1) |
| l6 | summary.formula | S_r = S_{r−1} + x_r − x_{r−w} | correct | derivation |
| l6 | summary.formula.note | shrinking a window on a sum is safe only when every number is positive | imprecise | zeros are safe too (script E, non-negative lists match brute force); homework-2 i6 says "never negative". Finding 6 |
| l6 | q0 | longest run of up days in 100, 101, 103, 102, 104, 105, 107, 106 is 3; slips 5, 2, 4 | correct | script B |
| l6 | q1 | shrinking window on `[5, -4, 6]`, k = 6 reports 3, missing `[6]`; prefix sums handle negatives | correct | script B |
| l6 | q2 | `max_window_sum([12, -3, 40, 7], 1)` is 40 | correct | A solution run |
| l6 | q3 | update with `xs[right - w + 1]` is off by `xs[0] - xs[k]` after k slides; no IndexError | correct | script D (random lists) |
| l7 | s0 | `xs[1:4]` of 3, −1, 4, 2, −5, 6 sums to 5; slips 8, 0, 9; a slice stops before its end index | correct | script B |
| l7 | s1 | `pre[0] = 0`, `pre[i + 1] = pre[i] + xs[i]`; pre = 0, 3, 2, 6, 8, 3, 9; n + 1 entries | correct | script B |
| l7 | s2 | `sum(xs[i:j]) == pre[j] - pre[i]`; `pre[4] - pre[1] = 5`; slips (p0, p3), (p1, p3), (p2, p4) | correct | telescoping sum; script B |
| l7 | s3 | `xs[2:6]` is 9 − 2 = 7; slips 6, 1, 0; empty range 0; whole list 9 | correct | script B |
| l7 | s4 | inclusive n-entry convention: `inc[2] - inc[-1] = -3`, silently | correct | script D |
| l7 | s5 | pre = 0, 2, 1, 2, 5, 3, 5; runs ending at day 5 with sum 3 need `pre[i] = 2`: rows 1 and 3; 5 runs in all | correct | script B (brute force 5) |
| l7 | s6.w.answer, hints, explain | `[0, 0, 0]`, k = 0: 6 subarrays; adds 1, 2, 3; without `{0: 1}` the count is 3 | correct | script B, D |
| l7 | s6.w.wrong singles, whole | 3 counts single days; 1 counts the whole list | correct | script B |
| l7 | s6.fb.byKey.four | "You forgot one of the runs of two days" for the slip value 4 | wrong | forgetting one of the two pairs leaves 5, not 4; 4 needs two runs missed. Finding 1 |
| l7 | s7 | 2D prefix table; rectangle = P[r2][c2] − P[r1][c2] − P[r2][c1] + P[r1][c1]; the corner block was subtracted twice | correct | inclusion-exclusion; script B (homework-2 grid) |
| l7 | s8 | `prefix`, `range_sum`, `count_subarrays_with_sum` with `{0: 1}`, look up before recording | correct | A; script E (against brute force with negatives and zeros) |
| l7 | s8.fb.byKey, explain | test 13 answer is 10,000²: prefix 0 appears 10,001 times and 1 appears 10,000 times; brute force about 200 million sums | correct | script D |
| l7 | s9 | cumulative P&L: days 4 to 7 are 190 − 240 = −50; slips −100, 190, 50; daily 50, −150, 90, −40; drawdown 290 to 140 | correct | script B; largest peak-to-later-trough fall is 150 |
| l7 | s9.prose | cumulative volume and the VWAP numerator are prefix sums | correct | VWAP = Σ p·v / Σ v (Harris, *Trading and Exchanges*, ch. 21) |
| l7 | summary | rule, formula, trap `pre[-1]` | correct | rows above |
| l7 | q0 to q3 | `range_sum(pre, 4, 4)` is 0; rebuilding per query is O(qn); `[1, 2, 1, 2]`, k = 3 has 3 runs; four lookups per rectangle | correct | script B |
| l8 | s0 | closes 102 … 97: best trade buys 98 on day 3, sells 107 on day 5, £9; slips (110, 95), 95 → 103 = 8, 102 → 110 = 8 | correct | script B brute force |
| l8 | s1 | 45 pairs for 10 days; slips 90, 100, 55; 2,520 days is over 3 million pairs | correct | C(2520, 2) = 3,173,940 |
| l8 | s2 | running low and best profit table; O(n) time, O(1) space | correct | script B |
| l8 | s3 | `max(prices) - min(prices)` returns 15, not a trade; equals the best trade only when the low comes first | correct | high day 1, low day 6 |
| l8 | s4 | convention: no trade, profit 0; colleague's start at the first pair returns −3 on 110, 104, 101, 97 | correct | script B |
| l8 | s5.prose | maximum drawdown is usually quoted as a fraction of the peak | correct | Bacon, *Practical Portfolio Performance Measurement and Attribution*, 2nd ed., ch. 4 (drawdown as a percentage decline from peak) |
| l8 | s5.w, fb, explain | maximum drawdown £15 (110 to 95); slips 12, 13, 9; here max minus min is right because the high comes first | correct | script B |
| l8 | s6.prose, w, fb | profit i to j is the sum of daily changes between them; changes 8, −6, −6, 3, 6, −12, 4, 4, −6; best run 3 + 6 = 9 | correct | telescoping; script B, E |
| l8 | s6.explain | Kadane keeps a running sum and resets to 0 when negative; the reset is the running minimum in disguise | correct | CLRS exercise 4.1-5; script E |
| l8 | s6.explain | "On daily returns, the same loop finds the best stretch of a strategy" | imprecise | sums of simple returns are not compounded returns; exact for log returns or daily P&L (l6 s9 says log returns). Finding 7 |
| l8 | s7 | `best` starts at 0: a falling, flat or single-price series returns 0 | correct | A (s8) |
| l8 | s8 | `best_trade` with ties to the earliest sell day, then the earliest buy day; strict comparisons give both | correct | A; script E (400 random lists against brute force with the tie rule) |
| l8 | s8.fb.byKey | tests 2, 8, 9, 11; about 5 billion pairs for 100,001 prices | correct | tests read; C(100001, 2) = 5.0 × 10⁹ |
| l8 | s9.opt, fb | a single long trade on these closes cannot beat £9; from £95 the best sale is £103 | correct | script B |
| l8 | s9.explain | to beat the bound a backtest must sell before buying, "often via a misaligned index", or fill at other prices | unverified | the bound is proved; how often the cause is a misaligned index is an unsourced empirical remark |
| l8 | summary.formula | max_{i<j}(p_j − p_i) = max_j (p_j − min_{i<j} p_i) | correct | derivation |
| l8 | q0 to q3 | `best_trade([50, 47])` is (0, 0, 0); flat closes give 0; changes −2, 5, −1, 4, −6, 3 give 8 (Kadane 0, 5, 4, 8, 2, 5); drawdown of 100, 120, 90, 130, 80 is 50 | correct | script B |
| l9 | s0, s1 | undo removes the newest edit; a list is a stack with `append` and `pop()`; `s` ends `['A', 'C']` | correct | CLRS 10.1; trace |
| l9 | s2 | bracket check: push openers, a closer pops and compares; `{[()]}` balanced when the stack ends empty | correct | Sedgewick and Wayne, *Algorithms*, 4th ed., 1.3 (Parentheses); A (s5) |
| l9 | s3 | `([)]` passes counting but fails the stack: `)` meets `[` | correct | A (s5 test 2) |
| l9 | s4 | balanced: `""`, `()[]{}`, `{[]}`; not: `(()`, `)(`, `]` | correct | A solution on each |
| l9 | s5 | `is_balanced`; `not stack` before `pop()`; `return not stack`; O(n) | correct | A |
| l9 | s5.fb.byKey | tests 3, 4, 5, 7 as described | correct | tests[2], [3], [4], [6] |
| l9 | s6 | first attempt returns `True` for `"(("` and raises `IndexError: pop from empty list` on `")"`; `or` evaluates left to right; `try` does not fix `"(("` | correct | script D; Py docs "Boolean operations" |
| l9 | s7 | postfix `5 1 2 + 4 * + 3 -` is 14; slips −14, 17; the first pop is the right operand | correct | script B |
| l9 | s8 | `eval_postfix`; `"-3"` is a number, so compare whole tokens; `8.0 == 8` | correct | A; script D |
| l9 | s9 | call stack: `discount` returns first; a `RecursionError` is the stack growing too tall; algo-think lesson 6 | correct | Py docs `sys.setrecursionlimit`; algo-think `l6-call-stack` exists |
| l9 | s10 | `first_bad`: indices on the stack; first failed closer, else `stack[0]`, else −1; table 3, 13 | correct | A |
| l9 | s10.fb.byKey | tests 2, 3, 8 as described | correct | tests[1], [2], [7] |
| l9 | summary | LIFO; `append` and `pop()` O(1); check before pop and at the end | correct | rows above |
| l9 | q0 to q4 | `[3, 1, 5]`; `2 3 4 * +` is 14 (slip 20); `{[]()}` balanced; `append`/`pop()` keep undo O(1); tags nest like brackets | correct | script B, D; A solution |
| l10 | s0 | first later value above day 3's close of 3 is 5 on day 5 | correct | trace |
| l10 | s1 | nested scan on 6 falling values: 15 comparisons; slips 36, 6, 30; n(n − 1)/2; 100,000 closes need about 5 billion | correct | script B |
| l10 | s1.explain | a year of minute bars is about 100,000 closes | correct | 252 days × 390 minutes = 98,280 (a 6.5-hour session) |
| l10 | s2.w, fb | 6 answers the waiting 4 and 2 | correct | trace |
| l10 | s2.explain, summary.ideas[1] | "The waiting values always fall from bottom to top" | imprecise | ties wait (s5), so equal values sit together: they never rise. Homework-3 i7 says "never rise". Finding 8 |
| l10 | s3 | answers 6, 6, 7, 5, 5, 7, −1; each day pushed once, popped at most once | correct | script B |
| l10 | s4 | falling: all −1, stack fills; rising: `[5, 6, 8, -1]`, at most one waits; about 2n steps either way | correct | script B, C (comparisons plus pushes) |
| l10 | s5 | `<=` on `[5, 5, 6]` returns `[5, 6, -1]`; `<` returns `[6, 6, -1]`; state the convention | correct | script B |
| l10 | s6 | at most n pushes plus n pops: 2,000 for n = 1,000; O(n) time and O(n) space; slips 10⁶, 1,000, 499,500 | correct | CLRS 17.1 aggregate analysis (multipop); script C |
| l10 | s7 | `next_greater`; tests; ties wait | correct | A; script C (against the nested scan) |
| l10 | s7.explain | "200,000 values take about 400,000 stack operations" | imprecise | 400,000 is the upper bound; the lesson's own 200,000-value test is falling and makes 200,000 pushes and no pops. Finding 9 |
| l10 | s8 | largest rectangle in a histogram needs the next smaller bar: pop while top > x; 2, 1, 5, 6, 2, 3 gives 5 × 2 = 10 | correct | script B (brute force 10) |
| l10 | s9 | `days_until_higher`; table 2, 1, 3, 2, 1, 0, 0; record `i - j`; daily temperatures problem | correct | A |
| l10 | s9.prose | the desk reads a long wait as a ceiling that held and a short one as momentum | correct | framed as this desk's reading, not a market fact |
| l10 | summary.formula, trap | step rule; `<` for ties waiting, `<=` when equal counts | correct | rows above |
| l10 | q0 to q3 | `[3, 3, -1]`; stack 6, 5, 2; total pops at most n; day 0 waits 3 days | correct | script B |
| l11 | s0 | price-time priority: A 300 and B 100 fill a 400 sell; a queue is FIFO | correct | Harris, *Trading and Exchanges*, ch. 6 (order precedence rules) |
| l11 | s1 | `deque`: `append`, `popleft()`; `q` ends `deque(['C', 'D'])`; `q[0]` front, `q[-1]` back | correct | Py docs collections.deque |
| l11 | s2 | `pop(0)` on six values moves 5; O(n); `popleft()` O(1); `pop()` O(1) | correct | Py docs TimeComplexity; script F |
| l11 | s3 | draining 1,000 with `pop(0)`: 499,500 shifts; slips 10⁶, 1,000, 999, 500,500; O(n²) against O(n) | correct | script B, F |
| l11 | s4 | in the window −1, −3, 5 the two older, smaller values can never be a maximum again | correct | dominance argument; script C |
| l11 | s5 | deque of indices on 5, 3, 4, 1, 2, 6 with w = 3: output 5, 4, 4, 6; each index joins and leaves once | correct | script C |
| l11 | s6 | `max_sliding_window`; front check `dq[0] <= i - w`; pop on `<=` keeps the newest of equals; n − w + 1 results | correct | A; script C (against brute force) |
| l11 | s6.fb.byKey | tests 2, 6, 11; `max(xs[i:i + w])` is O(nw); O(1) per step on average | correct | tests read; amortised by the enter-once argument |
| l11 | s7 | without the front check the list gives `[5, 5, 5, 6]` | correct | script C |
| l11 | s8 | deque `append`, `popleft`, `pop` are O(1); BFS uses a queue; `pop()` instead goes deep first | correct | CLRS 22.2, 22.3; Py docs |
| l11 | s9 | `RateLimiter`: drop times `<= now - t`, accept if fewer than k remain; an order exactly t ms later is outside | correct | A; stated convention |
| l11 | s9.fb.byKey, explain | tests 2, 3, 4; each time appended once and popped at most once | correct | tests read |
| l11 | summary | FIFO; draining a list is O(n²); monotonic deque step | correct | rows above |
| l11 | q0, q1 | `[3, 4]`; 1,000,000 `pop(0)` calls make about 5 × 10¹¹ moves | correct | script D; n²/2 |
| l11 | q2 | 250 closes, window 20: 231 values; pandas `rolling(20).max()` shows the same after 19 blanks | correct | 250 − 20 + 1; pandas `min_periods` defaults to the window |
| l11 | q3 | FIFO cost basis of 150 from 100 at £10 and 100 at £12: £1,600; LIFO 1,700; average 1,650 | correct | script B |
| l12 | s0.w, fb | reading 9 means visiting 7, 3, 9 from `head` | correct | CLRS 10.2 |
| l12 | s0.explain, summary.ideas[0] | "Reading the k-th value takes k steps" | imprecise | k nodes visited but k − 1 `next` steps; quiz 0 grades 4,999 for the 5,000th. Finding 10 |
| l12 | s1 | insert after `a`: `new.next = a.next`, then `a.next = new`; the other order makes `new.next = new` | correct | script D |
| l12 | s2 | `prices.insert(1, x)` on 1,000,000 values moves 999,999; the linked list changes two pointers, if you hold `a` | correct | script B |
| l12 | s3 | `a.next = a.next.next` removes 9; `a.next = None` loses 4; `a = a.next.next` rebinds a name; `del a.next` leads to `AttributeError` | correct | script D |
| l12 | s3.explain | nothing points to 9, so Python frees it; removing the head is `head = head.next` | correct | reference counting (Py docs, "Objects, values and types") |
| l12 | s4 | reverse body order: save `nxt`, flip, `prev = cur`, `cur = nxt`; return `prev`; O(n) time, O(1) space | correct | A (s7) |
| l12 | s5 | version without `nxt` returns `[7]` | correct | script D |
| l12 | s6 | O(1) insert after a held node against O(n) for a Python list; indexing and appending favour the list | correct | CLRS 10.2; Py docs TimeComplexity |
| l12 | s7 | `reverse`; tests 6 and 7 check identity of nodes | correct | A |
| l12 | s8 | remove n-th from end: dummy, `fast` n + 1 steps ahead, `slow` stops before the target (on 3 for n = 2) | correct | A (s9); trace |
| l12 | s8.fb.byKey.n3 | with only n steps `slow` lands on the node to remove | correct | trace: slow reaches 9 |
| l12 | s9 | `remove_nth_from_end`; return `dummy.next`; "if 5 vanished instead of 4" with a gap of n | correct | A; trace gives `[1, 2, 3, 4]` |
| l12 | s10 | doubly linked level plus a dict: cancel B with two pointer changes, O(1) | correct | CLRS 10.2 LIST-DELETE; B has both neighbours here |
| l12 | summary.ideas[1], [2], formula, trap | O(1) insert and delete at a held node; read a pointer before overwriting it | correct | rows above |
| l12 | q0 | 5,000th close: 4,999 `next` steps from `head` | correct | derivation |
| l12 | q1 to q3 | `[7, 3, 4]`; after one pass `prev` is node 1 → None and `cur` is node 2; LRU pairs a dict with a doubly linked list | correct | script D; A (homework-3 i4) |
| l13 | s0, s1 | tail 6 points back to 3; first repeat is 3; a `seen` set holds 6 nodes; O(n) memory | correct | trace |
| l13 | s1.explain | "in an interview it is a fine first answer" | unverified | opinion about interview practice, unsourced |
| l13 | s2 | slow 1 step, fast 2: positions (2, 3), (3, 5), (4, 3), (5, 5); they meet at 5 after 4 moves; Floyd's cycle detection | correct | script B; Knuth, TAOCP vol. 2, 3.1 exercise 6 |
| l13 | s3 | gap of 2 closes at 1 per move: 2 more moves; they meet within L moves of `slow` entering | correct | script B (all tails 0 to 13, cycles 1 to 13) |
| l13 | s4 | `while fast and fast.next` returns the second middle: 40 of six; 3rd of five; 2nd of two | correct | script D |
| l13 | s5 | `while fast.next and fast` raises `AttributeError: 'NoneType' object has no attribute 'next'` on `[1, 2]` | correct | script D; Pyodide message checked |
| l13 | s6 | the gap changes by exactly one per move; a speed of 3 against 1 could skip over 0 | correct | script D (a jump over `slow` exists) |
| l13 | s7 | `has_cycle`, `middle`; compare nodes with `is`; peak-memory tests | correct | A |
| l13 | s7.fb.byKey | tests 3, 4, 5, 9 as described | correct | tests[2], [3], [4], [8] |
| l13 | s8 | a + b = kL, so a steps from the meeting point reach the start; here a = 2, b = 2, L = 4, k = 1 | correct | script B; slow meets before finishing a lap, so it has walked a + b |
| l13 | s9 | `has_loop` on a dict of fallbacks with `.get`; O(1) extra space | correct | A |
| l13 | summary | gap shrinks by one; meet within one lap; reset finds the start; trap order of checks | correct | rows above |
| l13 | q0 to q3 | self-loop is a cycle; middle of 1 → 2 → 3 → 4 is 3; set up to 10,000,000 entries against two names; tortoise runs 400 m | correct | script B, D |
| rev1 | i0, i1 | insert at 3 of 8 shifts 5 (slips 3, 8, 4); SHEL is 44 → bucket 4 with BARC (slips 44, 8) | correct | script B |
| rev1 | i2, i3 | `two_sum([1, 5, 1, 5], 6)` is (0, 1); the `level` tally prints `2 3` | correct | script D; trace |
| rev1 | i4 | `"".join(parts)` is O(n); `sum(parts, "")` is refused with a pointer to `join`; front inserts are quadratic | correct | script D; Pyodide message checked |
| rev1 | i5 | `[x for x in a if x in set(b)]` rebuilds the set for every x: O(n²) | correct | script D (constructor counted 50 times for 50 items) |
| rev1 | i6 | `first_repeat`: first id seen a second time | correct | A |
| rev1 | i7 | sorted-letters key; `frozenset` forgets counts; `ad` and `bc` have equal `ord` sums; `len` groups everything | correct | script B (97 + 100 = 98 + 99) |
| rev2 | i0 | 2, 5, 9, 12, 20 with target 21: `j` moves; walk finds 9 + 12 | correct | script B |
| rev2 | i1, i2 | window slides 6 → 5 → 10 (slips 5, 16); `pre[4] - pre[1] = 6` (slips 10, 3) | correct | script B |
| rev2 | i3 | best profit on 45, 52, 39, 44, 48, 36 is 9; slips 16, 7 | correct | script B |
| rev2 | i4 | squares of −5, −2, 0, 1, 3: 25 then 9 written first | correct | trace |
| rev2 | i5 | shortest run ≥ 8 in 1, 4, 2, 3, 5 is 2 | correct | script B |
| rev2 | i6 | runs summing to 7: 3; prefix sums 0, 3, 7, 0, 3, 4, 7, 8, 4 | correct | script B brute force |
| rev2 | i7 | maximum drawdown of 0, 50, 20, 90, 40, 70, 10, 60 is 80; slips 30, 50, 90 | correct | script B |
| rev2 | i8 | 5,000 range questions on 2,500 values: prefix sums; `pre[b + 1] - pre[a]`; 12.5 million against 2,500 + 10,000 | correct | arithmetic |
| rev3 | i0 | `4 2 5 * + 1 -` is 13; slips −13, 29 | correct | script B |
| rev3 | i1 | next greater of 3, 8, 4, 1, 9 is 8, 9, 9, 9, −1 | correct | script B |
| rev3 | i2, i3 | filling a price level is FIFO, the other three are stacks; after two passes `prev` is 2 → 1 → None, `cur` is 3 | correct | Harris ch. 6; trace |
| rev3 | i4 | `make_cycle(range(8), 3)`: meet after 5 moves at node 5; a = 3, L = 5, b = 2 | correct | script B |
| rev3 | i5 | window maximum, w = 2, on 2, 7, 3, 1, 5, 4: 7, 7, 3, 5, 5 | correct | script C |
| rev3 | i6 | two indices left on the stack (9 and 6); "the stack falls from bottom to top" for this list | correct | script B |
| rev3 | i7 | `max_depth` with a counter | correct | A |
| hw1 | i0 | `top_ticker`; ties to the alphabetically first; `most_common(1)` returns the first seen on a tie; `max`/`min` raise on empty | correct | A; script D; Py docs Counter.most_common |
| hw1 | i1 | order of the one-pass two-sum steps | correct | l3 s6 code |
| hw1 | i2 | capacity 1, doubling, 1,000 appends: 1,023 copies; slips 2,047, 499,500, 1,000 | correct | script B |
| hw1 | i3 | snippet A is O(n) on average; B, C, D hide a scan | correct | Py docs TimeComplexity |
| hw1 | i4 | `pair_count` adds earlier complements before storing; test 8 answer about 5 × 10⁹ | correct | A; C(100000, 2) = 4,999,950,000 |
| hw1 | i5 | `longest_run`: walk only from a run's start; each number stepped over at most twice | correct | A |
| hw1 | i6 | `remove` on 50,000 ids: about 25,000 comparisons each, 2.5 × 10⁸ for 10,000 cancels; slips 5 × 10⁸, 10,000 | correct | (1 + 50,000)/2 × 10,000 |
| hw1 | i7.model (a) | first loop 2 to 4 × 10¹⁰; nested loop 19,999,900,000; 1,000 ids are about 10⁶ and 5 × 10⁵; 200× data is 40,000× work; triple reported three times | correct | script B; C(3, 2) = 3 |
| hw1 | i7.model (b), (c) | set plus Counter rewrite is O(n) plus O(d log d); `1` and `"1"` differ; Python randomises string hashes | correct | Py docs `object.__hash__` (hash randomisation for str and bytes) |
| hw1 | i7.rubric | 2 + 2 + 1 + 3 + 1 + 1 points follow the model | correct | read against the model |
| hw2 | i0 | `has_pair_with_difference` with two forward pointers; at most 2n steps | correct | A |
| hw2 | i1 | `longest_k_distinct` with a dict of counts; `'abaccc'` gives `'accc'` | correct | A |
| hw2 | i2.prose | "The best stretch of a strategy's daily returns is the maximum subarray" | imprecise | as l8 s6: exact for log returns or daily P&L. Finding 7 |
| hw2 | i2.w, fb, explain | `max_subarray` returns a non-empty slice; all-negative gives the largest single value | correct | A; CLRS 4.1 |
| hw2 | i3 | proof order: sorted gives x_k ≥ x_i, so x_k + x_j > t for every k in [i, j) | correct | derivation |
| hw2 | i4 | 2D prefix table 0, 2, 1, 4 / 0, 2, 5, 9 / 0, 7, 8, 14; rectangle 14 − 4 − 7 + 2 = 5; slips 3, 14 | correct | script B |
| hw2 | i5 | fewest consecutive minutes with volume ≥ 20 is 3; best pair is 19 | correct | script B |
| hw2 | i6 | the shrinking window fails on P&Ls with negatives; volumes are never negative; a monotonic queue on prefix sums handles negatives | correct | script E; LeetCode 862 standard solution (deque over prefix sums) |
| hw2 | i7.model (a), (b) | 3,173,940 pairs; one-pass running high is correct | correct | script B, E |
| hw2 | i7.model (c) | drawdown is the best trade on negated prices; minus the minimum sum of consecutive changes | correct | script E |
| hw2 | i7.model (d), (e) | single price and rising prices give 0; drawdown is not a prefix difference; a segment tree of (max, min, drawdown) merges halves | correct | script E (merge rule against brute force) |
| hw3 | i0 | `MinStack` with a second stack of running minimums; 7, 5, 5, 6 gives mins 7, 5, 5, 5 | correct | A |
| hw3 | i1 | `stock_span` with `<=`; spans 1, 1, 1, 2, 1, 4, 6; previous greater element | correct | A; script E (against the definition) |
| hw3 | i2 | FIFO basis of 350 shares: £17,650; LIFO 17,300; average 17,441.67; 250 at £49 remain | correct | script B |
| hw3 | i3 | order of `remove_nth_from_end` steps | correct | l12 s9 solution |
| hw3 | i4 | `LRUCache` with sentinels; `OrderedDict` with `move_to_end` is the same structure built in | correct | A; script E (random operations against OrderedDict); CPython `Lib/collections/__init__.py` |
| hw3 | i5 | `cycle_start`: meet, reset one pointer to the head, step both | correct | A; script B |
| hw3 | i6 | deque is O(1) at the ends; indexing near the middle and searching are O(n) | correct | Py docs collections.deque; script F |
| hw3 | i7.model | waiting closes never rise from bottom to top; loop; at most 2n pushes plus pops; ties; example 2, 1, 3, 2, 1, 0, 0; edge cases | correct | script B, C |
| hw3 | i7.rubric | 2 + 2 + 2 + 1 + 2 + 1 points follow the model | correct | read against the model |
