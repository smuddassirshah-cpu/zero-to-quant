# Claim ledger: ds levels 1 to 3 (round 1 blind audit)

Course `ds` (Core Data Structures, topic 1.8, Stage 1: full ledger depth). Files: the 13 lessons, three review sets and three homework sets that `course.json` maps to levels 1 to 3.

Basis key: `run` means a check in `docs/reports/ds-L1-3-concepts.py` (CPython 3.13; nothing in it depends on a behaviour newer than the app's Pyodide 0.27.7, which is CPython 3.12). CLRS is Cormen, Leiserson, Rivest and Stein, *Introduction to Algorithms*, 3rd edition. Sources named without a run were cited from memory of the named section, not reopened in this session.

A row may cover one screen's key, its wrong options or slips and its explanation when all were checked together and all hold. Any part that fails has its own row.

Rows: 250. Verdicts: correct 229, wrong 9, imprecise 8, misleading 0, unverified 4.

| # | file | JSON path | claim | verdict | basis |
|---|---|---|---|---|---|
| 1 | l1-arrays-in-memory | `screens[0].widget.answer + explain` | Item i of an array of 8-byte items based at 1000 starts at 1000 + 8i; prices[4] at 1032; no earlier item is visited | correct | derivation (base + i x size); CLRS 3e s10.3; run |
| 2 | l1-arrays-in-memory | `screens[0].widget.wrong[] + feedback.byKey` | 1040 = five steps; 1004 = index added without the width; 1024 = index 3 | correct | 1000+5x8, 1000+4, 1000+3x8 |
| 3 | l1-arrays-in-memory | `screens[1].widget.answer + explain` | Insert at index 2 of five values moves indices 2, 3, 4 one slot right, shifting from the back | correct | derivation; CPython listobject.c ins1 shifts the tail |
| 4 | l1-arrays-in-memory | `screens[1].widget.wrong[] + feedback.byKey` | missed-two leaves 100.40; moved-all moves values before index 2 | correct | matches the two wrong sets |
| 5 | l1-arrays-in-memory | `screens[2].widget.rows + feedback.correct` | Insert at index i of n values moves n - i values: 5, 3, 0 | correct | derivation |
| 6 | l1-arrays-in-memory | `screens[2].explain.text` | That is why append is cheap and insert(0, v) is not | correct | derivation; Python wiki TimeComplexity (list) |
| 7 | l1-arrays-in-memory | `screens[3].widget.options + explain` | Read by index touches 1 value; front insert on 10^6 values shifts 10^6; O(1) against O(n) | correct | derivation |
| 8 | l1-arrays-in-memory | `screens[3].widget.options[1..3].why` | Scan, like-append and averaged options each named correctly | correct | each why matches its option |
| 9 | l1-arrays-in-memory | `screens[4].prose` | A full array cannot grow in place; Python moves it to a bigger block and copies every value | correct | CPython list_resize uses realloc, which may move the block; copy is the worst case, the model the lesson states |
| 10 | l1-arrays-in-memory | `screens[4].widget.answer` | From capacity 1 with doubling, 16 appends make 1+2+4+8 = 15 copies | correct | run (doubling_copies) |
| 11 | l1-arrays-in-memory | `screens[4].widget.wrong[] + feedback.byKey` | 120 = copy all on every append; 16 = one each; 31 = includes the block of 16 | correct | 0+..+15 = 120; 1+2+4+8+16 = 31; run |
| 12 | l1-arrays-in-memory | `screens[4].feedback.correct` | 15 copies for 16 appends: fewer than one per append on average | correct | 15/16 |
| 13 | l1-arrays-in-memory | `screens[4].explain.text (sentence 1)` | The copies are always fewer than the appends | wrong | run: 17 appends make 31 copies; true bound is under twice the appends (CLRS 3e s17.4). Finding 1 |
| 14 | l1-arrays-in-memory | `screens[4].explain.text (sentences 2, 3)` | Append is O(1) amortised; CPython grows lists by about an eighth and the total stays linear | correct | run (ratios 1.125; linear total); CPython listobject.c list_resize: newsize + (newsize >> 3) + 6 |
| 15 | l1-arrays-in-memory | `screens[5].widget.answer + explain` | insert(0, t) for 1,000 ticks shifts 0+1+..+999 = 499,500 = n(n-1)/2; append then reverse is O(n) | correct | run; derivation |
| 16 | l1-arrays-in-memory | `screens[5].widget.wrong[] + feedback.byKey` | 1000 = one each; 10^6 = n^2; 500,500 = sum from 1 to 1000 | correct | run |
| 17 | l1-arrays-in-memory | `screens[5].feedback.correct` | About n^2/2: doubling the ticks quadruples the work | correct | derivation; run (timing ratio) |
| 18 | l1-arrays-in-memory | `screens[6].prose` | A list holds 8-byte pointers side by side; each float is a separate 24-byte object; NumPy stores the 8-byte values | correct | run (sys.getsizeof(float) = 24, 8 bytes per slot); NumPy docs, ndarray float64 itemsize 8 |
| 19 | l1-arrays-in-memory | `screens[6].widget.answer + wrong[]` | A million distinct floats in a list: (8 + 24) MB = 32 MB; 8 = pointers only; 24 = objects only | correct | derivation; assumes distinct float objects, which a list of prices has |
| 20 | l1-arrays-in-memory | `screens[6].explain.text` | xs[i] is still O(1) plus one hop; NumPy uses a quarter of the memory and loops in C | correct | 8/32; NumPy docs |
| 21 | l1-arrays-in-memory | `screens[7].prose` | A str cannot change, so s += piece builds a new string and copies the old one | correct | Python language reference (str immutable); explain adds the CPython in-place caveat |
| 22 | l1-arrays-in-memory | `screens[7].widget.answer + wrong[]` | 1,000 lines of 10 characters: 10+20+..+10,000 = 5,005,000 copied; 10,000 = join; 10^7 = full length every time | correct | run |
| 23 | l1-arrays-in-memory | `screens[7].explain.text` | join sizes the result once and copies each character once; CPython sometimes grows a str in place, with no promise | correct | CPython unicodeobject.c PyUnicode_Append resize path; Python docs (str.join, FAQ on concatenation) |
| 24 | l1-arrays-in-memory | `screens[8].prose (cost table)` | xs[i] O(1); append O(1) amortised; pop() O(1); insert(i, v) O(n - i); pop(0) O(n); v in xs O(n) | correct | Python wiki TimeComplexity; derivation |
| 25 | l1-arrays-in-memory | `screens[8].widget.options[].why` | xs[-1] is one address; append only copies on a full block; len reads a stored number | correct | CPython PyList_GET_SIZE; TimeComplexity |
| 26 | l1-arrays-in-memory | `screens[9] code (to_csv_line)` | join version equals the += version, with no trailing comma and '' for an empty list | correct | run (solution passes 6 tests, starter fails) |
| 27 | l1-arrays-in-memory | `screens[9].feedback.byKey + explain` | test-6 looks for .join(; join of [] is ''; 99.999 formats to 100.00 | correct | run |
| 28 | l1-arrays-in-memory | `screens[10].widget.options[0] + explain` | deque(maxlen=20) drops the oldest in O(1); a deque adds and drops at either end in O(1) | correct | Python docs collections.deque; run |
| 29 | l1-arrays-in-memory | `screens[10].widget.options[1,2].why` | insert(0) with pop() moves the shift to the insert; slicing copies 19 closes each tick | correct | derivation |
| 30 | l1-arrays-in-memory | `screens[10].widget.options[3].why` | remove(window[0]) is 'two linear steps instead of one' | wrong | run: the search ends at index 0 after one comparison; search k plus shift n-k-1 is one linear pass at most. Finding 2 |
| 31 | l1-arrays-in-memory | `summary.ideas + formula + trap` | address = base + i x size; insert shifts n - i; strings recopy on +=; insert(0) loop is O(n^2) | correct | restates rows above |
| 32 | l1-arrays-in-memory | `quiz[0]` | insert(3, v) in 10 values shifts 7; wrongs 3, 6, 10 named correctly | correct | 10 - 3 |
| 33 | l1-arrays-in-memory | `quiz[1]` | [][0] raises IndexError: list index out of range; append(5) would work | correct | run |
| 34 | l1-arrays-in-memory | `quiz[2]` | s[0] = 'B' raises TypeError: 'str' object does not support item assignment | correct | run |
| 35 | l1-arrays-in-memory | `quiz[3]` | 4-byte items from 2000: a[10] at 2040; wrongs 2010, 2044, 2080 named correctly | correct | 2000+40; 2000+10; 2000+11x4; 2000+10x8 |
| 36 | l2-constant-time-lookup | `screens[0] answer + feedback` | Toy hash: VOD 41 bucket 1; BP 18 bucket 3; HSBA 30 bucket 0 | correct | run |
| 37 | l2-constant-time-lookup | `screens[0].explain.text` | The rule is a hash function and the buckets a hash table | correct | CLRS 3e s11.2 |
| 38 | l2-constant-time-lookup | `screens[1] answer + explain` | AZN sums to 41, bucket 1: a collision; the bucket keeps both and a lookup compares keys inside it | correct | run; chaining, CLRS s11.2 |
| 39 | l2-constant-time-lookup | `screens[2].prose` | 'Python hashes it to bucket 1' and compares in arrival order | correct | describes the toy table; the explain says CPython's dict probes instead |
| 40 | l2-constant-time-lookup | `screens[2].widget.answer + wrong[]` | Finding AZN takes 2 comparisons; 4 = every key; 1 = hash step only | correct | derivation |
| 41 | l2-constant-time-lookup | `screens[2].explain.text` | With few keys per bucket, lookup, insert and delete are O(1) on average; CPython's dict probes other slots | correct | CLRS Theorem 11.1 and 11.2 (load factor O(1)); CPython Objects/dictobject.c (open addressing); run |
| 42 | l2-constant-time-lookup | `screens[3] answer + whys` | GSK 37, RIO 42, TSCO 57, BT 22 all leave 2; all n keys in one bucket makes a lookup O(n) | correct | run (all-collide: about n/2 eq calls per hit) |
| 43 | l2-constant-time-lookup | `screens[3].explain.text` | Real hash functions spread keys evenly, so this is rare; O(1) is an average, not a promise | correct | CLRS s11.2 (simple uniform hashing assumption); run |
| 44 | l2-constant-time-lookup | `screens[4] answer + wrong[] + explain` | Nested loop on two lists of 10,000 makes 10^8 comparisons; set version about 20,000 steps | correct | derivation |
| 45 | l2-constant-time-lookup | `screens[5] answer + options` | dedupe with a list on 2x10^6 distinct ids: about n^2/2 = 2x10^12 comparisons; 4x10^7 is n log2 n; 4x10^12 is n^2 | correct | derivation; n log2 n = 4.2x10^7 |
| 46 | l2-constant-time-lookup | `screens[6].prose + explain` | A key's hash must never change; hashable in practice means it cannot change; str, numbers and tuples of them are keys; list and dict raise TypeError: unhashable type | correct | Python glossary 'hashable'; run. Hedge 'in practice' covers user classes |
| 47 | l2-constant-time-lookup | `screens[7].prose + answer + whys` | Scan in a loop is O(nm); set(b) once is O(m), then n checks at O(1) average: O(n + m) | correct | derivation; CLRS s11.2 |
| 48 | l2-constant-time-lookup | `screens[8] code (duplicates)` | One pass with two sets, sorted output; O(n) on average | correct | run (8 tests) |
| 49 | l2-constant-time-lookup | `screens[8].widget.how + feedback.byKey.error` | A list scan on 60,000 distinct tickers runs out of time | correct | run: about 10 s native against the 5 s case limit (AUTHORING, code widget limits) |
| 50 | l2-constant-time-lookup | `screens[9] answer + wrong[]` | Mean (1 + 500)/2 = 250.5 comparisons per row, 250,500,000 in all; 5x10^8 = full scan; 10^6 = dict | correct | run (Monte Carlo 250.5) |
| 51 | l2-constant-time-lookup | `screens[9].explain.text` | dict(ref) costs 500 inserts once, then one O(1) lookup per row | correct | derivation |
| 52 | l2-constant-time-lookup | `summary` | Hash to one bucket; O(nm) to O(n + m); keys must be hashable; all-collide degrades to O(n) | correct | restates rows above |
| 53 | l2-constant-time-lookup | `quiz[0]` | {}['VOD'] raises KeyError: 'VOD'; get returns None or the default; Counter returns 0 | correct | run; Python docs |
| 54 | l2-constant-time-lookup | `quiz[1]` | A list key raises TypeError: unhashable type: 'list', before any bucket is chosen | correct | run (hash() fails first) |
| 55 | l2-constant-time-lookup | `quiz[2]` | BARC sums to 24, bucket 4; 5 is 24/5 rounded | correct | run |
| 56 | l2-constant-time-lookup | `quiz[3]` | set(a) & set(b) is O(n) average; the list versions are O(n^2); sorted(b) inside is worse | correct | Python wiki TimeComplexity (set intersection O(min(len))) |
| 57 | l3-two-sum | `screens[0]` | In [3, 8, 5, 12, 6] only 5 + 12 makes 17; the partner 17 - x is the complement | correct | run (one pair) |
| 58 | l3-two-sum | `screens[1] answer + wrong[]` | Brute force on 5 prices checks 10 pairs = n(n-1)/2; 25, 20, 5 named correctly; 1,000 prices give 499,500 | correct | derivation |
| 59 | l3-two-sum | `screens[2].steps` | One-pass trace on target 17 returns (2, 3) at i = 3 | correct | run |
| 60 | l3-two-sum | `screens[3] answer + whys` | [6, 1, 9, 4, 7] target 13 returns (2, 3), before the pair 6 + 7 | correct | run |
| 61 | l3-two-sum | `screens[4] answer + whys` | At index 3 before its step, seen = {6: 0, 1: 1, 9: 2}; values are keys, indices are values | correct | run |
| 62 | l3-two-sum | `screens[5] answer + whys` | Store-first version returns (0, 0) on [3, 4, 1], 6; a membership test never raises | correct | run |
| 63 | l3-two-sum | `screens[6] prose + answer` | Check then store: O(n) time, O(n) extra memory; [3, 3], 6 returns (0, 1) | correct | run; dict steps O(1) average |
| 64 | l3-two-sum | `screens[7] answer + explain` | Sorted [2, 4, 5, 8, 11, 13] target 16: sum 15 moves lo; walk ends at 5 + 11, indices 2 and 4; O(n), no extra memory | correct | run (walk) |
| 65 | l3-two-sum | `screens[8] code (two_sum)` | Solution, tests, each test has at most one pair; test-3 and test-6 feedback name the store-first slip | correct | run (9 tests; store-first gives (0, 0) on [5], 10) |
| 66 | l3-two-sum | `screens[9] answer + whys` | [1250, 830, 2100, 1670, 420], 2500 returns (1, 3); target 0 finds quantities that net to zero | correct | run |
| 67 | l3-two-sum | `summary` | n(n-1)/2 pairs; check before store; two pointers on sorted data | correct | restates rows above |
| 68 | l3-two-sum | `quiz[0..3]` | 499,500 pairs; [5], 10 gives None; [300, -100, 200, -300], 0 gives (0, 3); returning (need, x) gives (2, 7) | correct | run |
| 69 | l4-frequencies | `screens[0], [1]` | Tally VOD 3, BP 2, AZN 1; the dict holds only keys seen; get(t, 0) + 1 counts in O(n) | correct | run |
| 70 | l4-frequencies | `screens[2] answer + explain` | treads is an anagram of trades; anagrams have equal frequency maps; counting O(n), sorting O(n log n) | correct | derivation |
| 71 | l4-frequencies | `screens[3] answer + whys` | Under the exact-characters rule only '' and '' are anagrams among the four pairs | correct | run (Counter) |
| 72 | l4-frequencies | `screens[4] answer + whys` | counts[t] += 1 on {} raises KeyError: 'VOD'; fixes are get, defaultdict(int), Counter | correct | run |
| 73 | l4-frequencies | `screens[5] answer + explain` | Sorted letters are a canonical key: rate, tear to aert; bat, tab to abt; eat, tea to aet | correct | run |
| 74 | l4-frequencies | `screens[6] prose + answer + whys` | Counter(a) == Counter(b) is O(n); sorted is O(n log n); set compare is wrong; .count in a loop is O(n^2) | correct | derivation; run (set('trades') == set('traders')) |
| 75 | l4-frequencies | `screens[7] code` | is_anagram and group_anagrams; feedback test-2, 4, 5, 6 and the unhashable-list error | correct | run (10 tests) |
| 76 | l4-frequencies | `screens[8] code + how` | fills_per_venue; a Counter or defaultdict compares equal to a dict | correct | run (6 tests; Counter({'a': 1}) == {'a': 1}) |
| 77 | l4-frequencies | `summary` | Frequency map in O(n); anagram test by counts; canonical key; += on a missing key raises | correct | restates rows above |
| 78 | l4-frequencies | `quiz[0..3]` | set compare prints True; most_common(1) is [('a', 3)]; defaultdict read prints 0 2; sorted(w) key is unhashable | correct | run |
| 79 | review-1 | `items[0]` | insert(3, p) in 8 values shifts 5; wrongs 3, 8, 4 | correct | 8 - 3 |
| 80 | review-1 | `items[1]` | SHEL sums to 44, bucket 4; 8 is 44 // 5 | correct | run |
| 81 | review-1 | `items[2]` | [1, 5, 1, 5], 6 returns (0, 1) | correct | run |
| 82 | review-1 | `items[3]` | Tally of 'level' prints 2 3 | correct | l: 2, e: 2, v: 1 |
| 83 | review-1 | `items[4]` | join is O(n); += may copy each time; sum(parts, '') is refused with a pointer to join; front inserts are quadratic | correct | run (TypeError text names join) |
| 84 | review-1 | `items[5]` | x in set(b) inside a comprehension rebuilds the set for every x: O(n^2) | correct | Python reference: the condition is evaluated per iteration |
| 85 | review-1 | `items[6] code` | first_repeat returns the id whose second copy arrives first | correct | run (6 tests) |
| 86 | review-1 | `items[7]` | Sorted-letters key works; frozenset, ord sum and len collide (ad and bc both 197) | correct | run |
| 87 | homework-1 | `items[0] code + feedback` | top_ticker with key (-count, name); most_common(1) keeps the first seen on a tie | correct | run (6 tests; Counter tie order) |
| 88 | homework-1 | `items[1]` | Order of the six two-sum steps | correct | matches l3 screens[6] |
| 89 | homework-1 | `items[2]` | Doubling from capacity 1: 1,000 appends make 1,023 copies; 2,047, 499,500 and 1,000 named correctly | correct | run |
| 90 | homework-1 | `items[3]` | Only snippet A is O(n) on average; B, C, D hide a list scan | correct | derivation |
| 91 | homework-1 | `items[4] code` | pair_count adds the count of earlier complements; [1] x 100,000 gives 4,999,950,000 | correct | run (8 tests); note: seen[target - x] on a defaultdict inserts keys, harmless here |
| 92 | homework-1 | `items[5] code + explain` | longest_run walks only from run starts; each number is stepped over at most twice: O(n) average | correct | run (8 tests); derivation |
| 93 | homework-1 | `items[6]` | 10,000 removes on a 50,000 list: about 25,000 comparisons each, 2.5x10^8; a dict is O(1) per cancel | correct | (1 + 50,000)/2 x 10,000 = 250,005,000, inside the 5% tolerance |
| 94 | homework-1 | `items[7].model (a)` | First loop 2x10^10 to 4x10^10 comparisons; nested loop n(n-1)/2 = 19,999,900,000; 200 times the data is 40,000 times the work; a triple is reported three times | correct | run; C(3,2) = 3 |
| 95 | homework-1 | `items[7].model (b)` | Set plus Counter rewrite is O(n) average plus O(d log d) to sort d duplicates | correct | derivation |
| 96 | homework-1 | `items[7].model (c) + rubric` | O(1) is an average; heavy collisions give O(n^2); Python randomises str hashes; O(n) extra space | correct | Python docs, object.__hash__ note on PYTHONHASHSEED; CLRS s11.2 |
| 97 | l5-both-ends | `screens[0] answer + explain` | Sum 16 over target 10: 15 can pair with nothing, since every partner is at least 1 | correct | derivation (sorted order) |
| 98 | l5-both-ends | `screens[1] states + explain` | Moves j, j, i, j, i; sums 16, 12, 9, 11, 9, 10; dropped 15, 11, 1, 8, 3; every pair is 21 sums | correct | run |
| 99 | l5-both-ends | `screens[2] answer + whys` | Target 20: sums 16, 18, 19, 21, 17, 19, meet on 11; at most n - 1 sums; O(n) against O(n^2) | correct | run (3,000 random lists, at most n - 1 sums) |
| 100 | l5-both-ends | `screens[3] answer + wrong[]` | refer needs 2 comparisons; noon needs 2; 3, 5, 4 named correctly | correct | floor(n/2) |
| 101 | l5-both-ends | `screens[4].prose + answer + explain` | The biggest square is at one end; fill from the back; output [1, 4, 9, 16, 36, 49] | correct | run; derivation (x^2 is monotone in abs(x)) |
| 102 | l5-both-ends | `screens[4].feedback.byKey.c3` | 2 is nearest zero, so its square is the smallest and goes in the first slot | wrong | run: -1 is nearest zero (as byKey.c2 says); 4 is second smallest. Finding 3 |
| 103 | l5-both-ends | `screens[4].feedback.byKey.c1, c2, c4` | 9 loses to 36; -1 squares to the smallest; 4 is not at an end | correct | run |
| 104 | l5-both-ends | `screens[5] answer + whys + explain` | From i on 4 and j on 8 (sum 12), moving i loses 4 + 6 and the pointers meet on 6; moving j was safe | correct | run |
| 105 | l5-both-ends | `screens[6] prose + answer + explain` | O(n) time, O(1) space, needs sorted input; i < j stops a number pairing with itself; [5], 10 with i <= j returns (0, 0) | correct | run |
| 106 | l5-both-ends | `screens[7] code + feedback` | two_sum_sorted and is_palindrome (letters only, case ignored) | correct | run (15 tests) |
| 107 | l5-both-ends | `screens[8] answer + wrong[] + explain` | P&Ls: sums 15, 60, 15, 50; pair -40 and 90; 10,000 trades need at most 9,999 sums, not about 50 million | correct | run; C(10,000, 2) = 49,995,000 |
| 108 | l5-both-ends | `summary` | Drop the number that cannot be in the answer; O(n) time, O(1) space; unsorted input breaks the rule silently | correct | restates rows above |
| 109 | l5-both-ends | `quiz[0]` | [8, 3, 5, 1, 9], 10 prints None: 8 + 9 drops 9 first | correct | run |
| 110 | l5-both-ends | `quiz[1]` | Swapping over all five indices restores the list | correct | run |
| 111 | l5-both-ends | `quiz[2].prose` | 'A strangle's payoff at six strikes' is [10, 5, 0, 0, 5, 10] | imprecise | The six points are prices of the underlying at expiry; the strangle has two strikes, 100 and 105 (run). Hull, Options, Futures and Other Derivatives, ch. 12 (strangles). Finding 4 |
| 112 | l5-both-ends | `quiz[2] answer + wrong[]` | Six values need 3 comparisons; 6 and 2 named correctly | correct | derivation |
| 113 | l5-both-ends | `quiz[3]` | two_sum_sorted([5], 10) prints None; an empty list gives j = -1 | correct | run |
| 114 | l6-sliding-window | `screens[0] answer + wrong[]` | Slide from 13: 13 - 4 + 1 = 10; 14, 9, 3 named correctly | correct | run |
| 115 | l6-sliding-window | `screens[1] answer + feedback` | Sums 13, 10, 16, 12, 17, 14; best window starts on day 4 | correct | run |
| 116 | l6-sliding-window | `screens[2] answer + whys + explain` | Scratch version: 981 x 20 = 19,620 additions, O(nw); sliding 1,980, O(n); at w = 250 the gap is about 100 times | correct | run (107 times) |
| 117 | l6-sliding-window | `screens[3] answer + whys` | At sum 8, record length 4 then shrink from the left; restarting is O(n^2) | correct | derivation |
| 118 | l6-sliding-window | `screens[3].explain.text` | Every day enters once and leaves once, so the scan is O(n) | correct | derivation (two monotone pointers) |
| 119 | l6-sliding-window | `screens[4] answer + explain` | Shortest run reaching 7 in [2, 3, 1, 2, 4, 3] is 2; recorded lengths 4, 4, 3, 3, 2; shrinking is safe because all numbers are positive | correct | run |
| 120 | l6-sliding-window | `screens[5] answer + explain` | On the second b, left = last['b'] + 1 = 2; the window grows to cbdae, length 5 | correct | run |
| 121 | l6-sliding-window | `screens[6].prose` | 'This version passes abcbdae' | wrong | run: the version shown returns 6 on 'abcbdae'; the right answer is 5. Finding 5 |
| 122 | l6-sliding-window | `screens[6] answer + whys + explain` | The version returns 3 on 'abba'; left must never move back: max(left, last[ch] + 1) | correct | run |
| 123 | l6-sliding-window | `screens[7] prose + answer` | Fixed window update total += xs[right] - xs[right - w]; the index that leaves is right - w | correct | derivation |
| 124 | l6-sliding-window | `screens[8] code + feedback` | max_window_sum and longest_unique; test 6 answer 3,799,990,000; scratch is about 3.6 billion additions | correct | run (13 tests) |
| 125 | l6-sliding-window | `screens[9].prose` | vol.rolling(5).sum().max() runs the same loop under the hood | correct | pandas source, _libs/window/aggregations.pyx roll_sum (add_sum and remove_sum per step, with compensation) |
| 126 | l6-sliding-window | `screens[9] answer + wrong[] + explain` | Totals 2370, 2340, 2660, 2800, 2490, 2520; five biggest days sum to 2950; log returns add, so the same loop finds the best 20-day return | correct | run; log returns are additive (Tsay, Analysis of Financial Time Series, s1.1) |
| 127 | l6-sliding-window | `summary` | Fixed width: one add, one drop; free width: grow and shrink; O(n) not O(nw); shrinking on a sum needs positive numbers | correct | restates rows above |
| 128 | l6-sliding-window | `quiz[0]` | Longest run of up days in the eight closes is 3 | correct | moves up, up, down, up, up, up, down |
| 129 | l6-sliding-window | `quiz[1]` | Shrinking window on [5, -4, 6], k = 6 reports 3 and misses [6]; prefix sums handle negatives | correct | run |
| 130 | l6-sliding-window | `quiz[2]` | max_window_sum([12, -3, 40, 7], 1) prints 40 | correct | run |
| 131 | l6-sliding-window | `quiz[3].widget.options[0], [1], [2]` | Subtracting xs[right - w + 1] drops a day still in the window; no IndexError since right - w + 1 is at least 1 | correct | derivation |
| 132 | l6-sliding-window | `quiz[3].widget.options[3].why` | 'Every sum after the first is wrong' | imprecise | run: the error after k steps is x[0] - x[k], so a sum is right whenever x[k] equals x[0]. Finding 6 |
| 133 | l7-prefix-sums | `screens[0] answer + wrong[]` | sum(xs[1:4]) = 5; 8, 0, 9 named correctly | correct | run |
| 134 | l7-prefix-sums | `screens[1] answer + explain` | pre = [0, 3, 2, 6, 8, 3, 9]; n + 1 entries; pre[i] = sum(xs[:i]) | correct | run |
| 135 | l7-prefix-sums | `screens[2] answer + wrong[] + explain` | sum(xs[i:j]) == pre[j] - pre[i]; pre[4] - pre[1] = 5; two lookups, O(1) | correct | run; telescoping sum |
| 136 | l7-prefix-sums | `screens[3] answer + wrong[] + explain` | pre[6] - pre[2] = 7; empty range gives 0; whole list gives 9 | correct | run |
| 137 | l7-prefix-sums | `screens[4] answer + whys + explain` | The n-entry convention reads inc[-1] when i = 0 and prints -3 with no error | correct | run |
| 138 | l7-prefix-sums | `screens[5] prose + answer + explain` | Runs ending at the last day that sum to 3 start where pre[i] = 2: rows 1 and 3; the count over all days is 5 | correct | run |
| 139 | l7-prefix-sums | `screens[6] answer + wrong[] + explain` | [0, 0, 0], k = 0 has 6 runs; without {0: 1} the count is 3 | correct | run |
| 140 | l7-prefix-sums | `screens[7] prose + answer + whys` | 2D prefix table: rectangle = P[r2][c2] - P[r1][c2] - P[r2][c1] + P[r1][c1]; the top-left block is subtracted twice | correct | inclusion-exclusion; run (homework grid) |
| 141 | l7-prefix-sums | `screens[8] code + feedback + explain` | prefix, range_sum, count_subarrays_with_sum; test 13 answer 10,000^2; every subarray is about 200 million sums | correct | run (13 tests; brute-force agreement on 2,000 random lists) |
| 142 | l7-prefix-sums | `screens[9] prose + answer + wrong[] + explain` | Cumulative P&L is a prefix sum; days 4 to 7 make 190 - 240 = -50; the largest fall from a peak is 290 to 140 | correct | run |
| 143 | l7-prefix-sums | `summary` | n + 1 entries; two lookups; dict of prefix counts from {0: 1}; pre[-1] wraps | correct | restates rows above |
| 144 | l7-prefix-sums | `quiz[0..3]` | range_sum(pre, 4, 4) is 0; rebuilding per query is O(qn); [1, 2, 1, 2], k = 3 has 3 runs; a rectangle needs 4 lookups after an O(rc) build | correct | run; derivation |
| 145 | review-2 | `items[0]` | [2, 5, 9, 12, 20] target 21: sum 22 moves j; the walk finds 9 + 12 | correct | run |
| 146 | review-2 | `items[1].widget.answer + wrong[0]` | Two slides of width 2 give 10; 5 is after one slide | correct | run |
| 147 | review-2 | `items[1].widget.wrong[1] + feedback.byKey.kept` | 15 is 'adding the new numbers without dropping the old ones' | wrong | run: that slip gives 6 + 4 + 6 = 16; 15 is 5 + 4 + 6. Finding 7 |
| 148 | review-2 | `items[2].widget.answer + wrong[1]` | sum(xs[1:4]) = pre[4] - pre[1] = 6; 3 is pre[3] - pre[1] | correct | run |
| 149 | review-2 | `items[2].widget.wrong[0] + feedback.byKey.off` | 9 is pre[4] - pre[0] | wrong | run: pre[4] - pre[0] = 10; 9 is pre[4] - pre[2]. Finding 8 |
| 150 | review-2 | `items[3]` | Best trade on the six closes is 39 to 48 = 9; 16 is the range; 7 is the early trade | correct | run |
| 151 | review-2 | `items[4]` | Squares of [-5, -2, 0, 1, 3] from the back: 25 then 9 | correct | run |
| 152 | review-2 | `items[5]` | Shortest run of [1, 4, 2, 3, 5] reaching 8 has length 2 | correct | run |
| 153 | review-2 | `items[6]` | Three prefix pairs differ by 7 | correct | run |
| 154 | review-2 | `items[7]` | Maximum drawdown of the cumulative P&L is 90 to 10 = 80, in pounds | correct | run; pounds are the natural unit for a P&L curve |
| 155 | review-2 | `items[8]` | Prefix sums: 2,500 steps to build, then 10,000 lookups; pre[b + 1] - pre[a] for inclusive days | correct | derivation |
| 156 | homework-2 | `items[0] code + explain` | has_pair_with_difference with two forward pointers; at most 2n steps | correct | run (10 tests) |
| 157 | homework-2 | `items[0].feedback.byKey.test-6` | A failure on [2, 2, 5], 3 means i and j were not kept apart | imprecise | run: with d > 0 the i == j guard never changes the answer (4,000 lists), so the line names no real slip. Finding 9 |
| 158 | homework-2 | `items[1] code + feedback` | longest_k_distinct with a dict of counts | correct | run (10 tests) |
| 159 | homework-2 | `items[2] code + prose + explain` | max_subarray for the non-empty slice; all-negative input returns the largest single value | correct | run (8 tests); Bentley, Programming Pearls, col. 8 |
| 160 | homework-2 | `items[3]` | Proof order: assumption, sorted inequality, sum inequality, x_j ruled out, mirror case | correct | derivation; a valid invariant proof |
| 161 | homework-2 | `items[4].prose (last sentence)` | 'P[r][c] sums rows below r and columns below c' | imprecise | It means rows and columns with smaller index; in a table 'below' reads as larger index, the opposite. l7 says 'above and left'. Finding 10 |
| 162 | homework-2 | `items[4] table + answer + wrong[]` | P as tabulated; rectangle = 14 - 4 - 7 + 2 = 5; 3 forgets the add-back | correct | run |
| 163 | homework-2 | `items[5] answer + wrong[0] + explain` | Fewest minutes reaching 20 lots is 3; no pair beats 19 | correct | run |
| 164 | homework-2 | `items[5].feedback.byKey.four` | '[12, 3, 7, 9] is the first window to reach 20' | wrong | run: [12, 3, 7] = 22 reaches 20 first, as the explain says. Finding 11 |
| 165 | homework-2 | `items[6]` | The shrinking window fails with negatives; a monotonic queue over prefix sums handles them | correct | run (l6 quiz[1]); standard deque method for shortest subarray with sum at least k |
| 166 | homework-2 | `items[7].prompt + model (a), (b)` | Pairwise version is O(n^2), 3,173,940 pairs; one-pass running high is correct and O(n), O(1) space | correct | run; derivation as written |
| 167 | homework-2 | `items[7].prompt + model (c)` | The quantity called 'the maximum drawdown' of ten years of closes is the largest fall in pounds; best trade on negated prices; minus the minimum subarray of changes | imprecise | True for the absolute fall only. For prices the standard measure is the fall as a fraction of the peak (as pytest l3 and py-found l7 define it); the two can pick different episodes (run). Finding 12 |
| 168 | homework-2 | `items[7].model (d), (e) + rubric` | Edge cases; drawdown over ranges is not a difference of prefix values; a segment tree storing (max, min, best drawdown) merges in O(log n) per query | correct | merge: max(L.dd, R.dd, L.max - R.min) |
| 169 | l8-best-day | `screens[0] answer + wrong[] + explain` | Best trade 98 to 107 = 9; max minus min is no trade because the high comes first | correct | run |
| 170 | l8-best-day | `screens[1] answer + wrong[] + explain` | 45 pairs for 10 days; 2,520 days give over 3 million pairs | correct | 3,173,940 |
| 171 | l8-best-day | `screens[2] table + explain` | Running low and best profit; O(n) time, O(1) space | correct | run |
| 172 | l8-best-day | `screens[3] answer + whys + explain` | max - min returns 15, the range; it equals the best trade only when the low comes before the high | correct | run; derivation |
| 173 | l8-best-day | `screens[4] answer + whys + explain` | Starting best at the first pair returns -3 on a falling series; starting at 0 means no trade | correct | run |
| 174 | l8-best-day | `screens[5].prose + question` | 'The maximum drawdown, which you coded in Python Foundations and tested in the pytest course', asked in pounds | imprecise | Those lessons define it as a fraction of the peak; here it is the fall in pounds, with no note of the change. Finding 12 |
| 175 | l8-best-day | `screens[5] answer + wrong[] + explain` | The largest fall from a running high is 110 to 95 = 15 pounds; 12, 13, 9 named correctly | correct | run |
| 176 | l8-best-day | `screens[6] prose + answer + wrong[]` | Profit from day i to j is the sum of the daily changes; best trade = maximum subarray of changes = 3 + 6 | correct | telescoping; run |
| 177 | l8-best-day | `screens[6].explain.text` | Kadane keeps a running sum and resets it to 0 when negative; the reset is the running minimum in disguise | correct | Bentley, Programming Pearls, col. 8; this is the empty-run variant, matching 'no trade'; homework-2 h-max-subarray covers the non-empty variant |
| 178 | l8-best-day | `screens[7] prose + answer` | best starts at 0: a falling series, one price and a flat series all return 0 | correct | run |
| 179 | l8-best-day | `screens[8] code + feedback + explain` | best_trade with strict comparisons gives the stated tie rule | correct | run (11 tests; brute-force agreement on 3,000 random lists) |
| 180 | l8-best-day | `screens[9] answer + whys` | No single long trade on these closes beats 9, so a reported 12 is a bug | correct | run (max over all pairs is 9) |
| 181 | l8-best-day | `screens[9].explain.text (sentences 2, 3)` | A backtest beating the ceiling 'is reading future prices'; 'a look-ahead bug' is a common cause | wrong | The ceiling already assumes perfect foresight: the best buy-before-sell pair is 9 (run). Reading future closes can reach 9, never 12. Finding 13 |
| 182 | l8-best-day | `summary` | Two numbers in one pass; max minus min ignores time; mirror gives drawdown; Kadane on changes | correct | restates rows above |
| 183 | l8-best-day | `quiz[0..3]` | [50, 47] gives (0, 0, 0); flat closes give 0; changes [-2, 5, -1, 4, -6, 3] give 8; drawdown of [100, 120, 90, 130, 80] is 50 | correct | run |
| 184 | l9-last-in-first-out | `screens[0], [1]` | Undo removes the newest edit; a list is a stack with append and pop(); s ends as ['A', 'C'] | correct | derivation; Python tutorial s5.1.1 |
| 185 | l9-last-in-first-out | `screens[2], [3]` | A closer closes the most recent opener; {[()]} balances; ([)] fails though counts match | correct | run |
| 186 | l9-last-in-first-out | `screens[4]` | Balanced means every closer finds its partner on top and the stack ends empty; '', ()[]{} and {[]} pass | correct | run |
| 187 | l9-last-in-first-out | `screens[5] code + feedback + explain` | is_balanced; not stack is tested before pop(); O(n) | correct | run (11 tests) |
| 188 | l9-last-in-first-out | `screens[6] prose + console + whys` | The first attempt passes {[()]} and ([)]; returns True on '(('; raises IndexError: pop from empty list on ')'; or runs left to right | correct | run |
| 189 | l9-last-in-first-out | `screens[7] answer + wrong[] + explain` | 5 1 2 + 4 * + 3 - is 14; the first pop is the right operand; -14 and 17 named correctly | correct | run |
| 190 | l9-last-in-first-out | `screens[8] code + feedback` | eval_postfix; '-3' is a number; 8.0 == 8 | correct | run (9 tests) |
| 191 | l9-last-in-first-out | `screens[9] prose + answer + explain` | Calls wait on the call stack; discount returns first; RecursionError is the stack growing too tall | correct | Python docs (sys.setrecursionlimit); algo-think l6 is 'Watching the call stack' |
| 192 | l9-last-in-first-out | `screens[10] code + table` | first_bad returns -1, 3, 13 for the three formulas; left-over openers sit in reading order | correct | run (10 tests) |
| 193 | l9-last-in-first-out | `summary` | LIFO; append and pop() O(1); stack must end empty | correct | restates rows above (append is amortised O(1), as l1 states) |
| 194 | l9-last-in-first-out | `quiz[0..4]` | [3, 1, 5]; 2 3 4 * + is 14 (20 is left to right); {[]()} balances; append and pop keep undo O(1); tags nest like brackets | correct | run; derivation |
| 195 | l10-next-greater | `screens[0], [1]` | Next greater of day 3 is 5; nested scan on a falling list of 6 makes 15 comparisons, n(n-1)/2; 100,000 closes need about 5 billion | correct | run; 100,000^2 / 2 |
| 196 | l10-next-greater | `screens[2], [3]` | 6 answers days 0 and 1; answers 6, 6, 7, 5, 5, 7, -1; waiting values fall from bottom to top: a monotonic stack | correct | run (agreement with nested scan on 2,000 random lists) |
| 197 | l10-next-greater | `screens[4] answer + whys + explain` | Falling gives all -1; rising gives [5, 6, 8, -1]; either way at most about 2n steps | correct | run |
| 198 | l10-next-greater | `screens[5] answer + whys + explain` | With <= the scan returns [5, 6, -1] on [5, 5, 6]; with < ties wait | correct | run |
| 199 | l10-next-greater | `screens[6] prose + answer + wrong[]` | Each index is pushed once and popped at most once: at most 2n = 2,000 operations; O(n) time, O(n) space | correct | run (ops at most 2n); aggregate analysis, CLRS 3e s17.1 (multipop) |
| 200 | l10-next-greater | `screens[7] code + feedback + explain` | next_greater; 200,000 values take about 400,000 stack operations | correct | run (10 tests) |
| 201 | l10-next-greater | `screens[8] prose + answer + explain` | Largest rectangle needs the next smaller bar; pop while top > x; the 5 spans two bars: area 10; both-side scans give widths in O(n) | correct | run (brute force gives 10) |
| 202 | l10-next-greater | `screens[9].prose (sentences 2, 3)` | 'A long wait means a ceiling held. A short one means momentum.' | unverified | Unsourced reading of market behaviour; no basis found. Finding 15 |
| 203 | l10-next-greater | `screens[9] code + table + explain` | days_until_higher records i - j; table 2, 1, 3, 2, 1, 0, 0; O(n) | correct | run (8 tests) |
| 204 | l10-next-greater | `summary + quiz[0..3]` | [2, 1, 3] gives [3, 3, -1]; stack 6, 5, 2; the while runs at most n times in total; day 0 waits 3 days | correct | run |
| 205 | l11-first-in-first-out | `screens[0].prose (sentence 2)` | 'An exchange fills orders at one price in arrival order' | imprecise | True under price-time priority; some markets allocate pro rata at a price (CME Group, Matching Algorithm Overview). Finding 14 |
| 206 | l11-first-in-first-out | `screens[0] answer + explain` | A 300 then B 100 are filled; a queue is first in, first out | correct | derivation |
| 207 | l11-first-in-first-out | `screens[1]` | deque: append at the back, popleft from the front; q ends as deque(['C', 'D']) | correct | Python docs collections.deque; run |
| 208 | l11-first-in-first-out | `screens[2] answer + explain` | pop(0) on six values moves 5; pop(0) is O(n); popleft only moves a front marker, O(1) | correct | CPython listobject.c (memmove) and _collectionsmodule.c (leftindex); run (timing) |
| 209 | l11-first-in-first-out | `screens[3] answer + wrong[] + explain` | Draining 1,000 values with pop(0) makes 499,500 shifts: O(n^2); a deque is O(n) | correct | run (timing ratios) |
| 210 | l11-first-in-first-out | `screens[4], [5]` | A value with a newer, bigger value behind it can never be a window maximum; deque trace gives 5, 4, 4, 6; O(n) | correct | run |
| 211 | l11-first-in-first-out | `screens[6] code + explain` | max_sliding_window; front check dq[0] <= i - w; pop on <= keeps the newest of equal values | correct | run (11 tests; agreement with slice maxima on 2,000 random lists) |
| 212 | l11-first-in-first-out | `screens[6].widget.how + feedback.byKey.test-11` | 'Slicing each window cannot finish in time' on 200,000 values with w = 2,000 | unverified | Run: max(xs[i:i + w]) over all windows takes 3.2 s in native CPython 3.13, under the 5 s case limit; Pyodide is slower by a machine-dependent factor. Finding 16 |
| 213 | l11-first-in-first-out | `screens[7] answer + whys` | Without the front check the scan returns [5, 5, 5, 6] | correct | run |
| 214 | l11-first-in-first-out | `screens[7].explain.text (last sentence)` | 'Add if dq[0] <= i - w: dq.popleft() before the back pops' | wrong | run: on the first pass the deque is empty and dq[0] raises IndexError; the guard 'dq and' is needed, as in the solution. Finding 17 |
| 215 | l11-first-in-first-out | `screens[8] prose + answer + explain` | deque append, popleft, pop are O(1); pop() instead of popleft() turns breadth-first into depth-first order | correct | Python docs; CLRS 3e s22.2 and s22.3 |
| 216 | l11-first-in-first-out | `screens[9] code + feedback + explain` | RateLimiter with a deque of accepted times; amortised O(1) per call | correct | run (7 tests) |
| 217 | l11-first-in-first-out | `summary + quiz[0..3]` | [3, 4]; 10^6 ticks with pop(0) is about 5x10^11 moves; 231 windows; FIFO basis 1,600, LIFO 1,700, average 1,650 | correct | run |
| 218 | l12-nodes-and-pointers | `screens[0]` | A node knows its value and its successor; reading the k-th value takes k node visits; no O(1) indexing | correct | CLRS 3e s10.2 |
| 219 | l12-nodes-and-pointers | `screens[1], [2]` | Insert after a held node: new.next = a.next, then a.next = new; O(1); list.insert(1, x) on 10^6 values moves 999,999; finding the node is O(n) | correct | derivation |
| 220 | l12-nodes-and-pointers | `screens[3] answer + whys + explain` | a.next = a.next.next removes the next node; rebinding a name changes no arrow; del a.next breaks the walk with AttributeError; removing the head is head = head.next | correct | run |
| 221 | l12-nodes-and-pointers | `screens[4], [5]` | Reverse body order: save, flip, prev, cur; O(n) time, O(1) space; without nxt the function returns [7] | correct | run |
| 222 | l12-nodes-and-pointers | `screens[6] answer + whys` | Insert after a held node is O(1) for a linked list and O(n) for a Python list; indexing and append favour the list | correct | derivation |
| 223 | l12-nodes-and-pointers | `screens[7] code` | reverse re-links the same nodes | correct | run (8 tests) |
| 224 | l12-nodes-and-pointers | `screens[8], [9]` | Dummy node, fast moved n + 1 steps: slow stops before the target; with n steps slow lands on it; head removal needs no special case | correct | run (8 tests; gap of n removes the wrong node) |
| 225 | l12-nodes-and-pointers | `screens[10].prose` | 'An exchange keeps each price level as a queue ... Cancels are frequent, so each node has both prev and next' | unverified | Scenario stated as fact about exchanges; no source given. Finding 15 |
| 226 | l12-nodes-and-pointers | `screens[10] answer + whys + explain` | dict lookup plus two pointer changes cancels in O(1); fixing only the forward arrow leaves C.prev on B | correct | derivation (B is an interior node) |
| 227 | l12-nodes-and-pointers | `summary + quiz[0..3]` | 5,000th node is 4,999 next steps away; [7, 3, 4]; after one pass prev is node 1 and cur node 2; LRU pairs a dict with a doubly linked list | correct | derivation |
| 228 | l13-fast-and-slow | `screens[0], [1]` | 6 points back to 3: a cycle of four; the seen-set method stores 6 nodes, O(n) memory | correct | run |
| 229 | l13-fast-and-slow | `screens[2] states + explain` | Positions (2, 3), (3, 5), (4, 3), (5, 5): meet at 5 after 4 moves; Floyd's cycle detection, O(1) extra space | correct | run; Knuth, TAOCP vol. 2, s3.1 exercise 6 |
| 230 | l13-fast-and-slow | `screens[3] answer + explain` | Gap 2 closes in 2 moves; once slow is in a cycle of length L they meet within L moves; O(n) | correct | run (1,500 random lists) |
| 231 | l13-fast-and-slow | `screens[4] answer + explain` | Middle of six nodes is the second middle, 40; 5 nodes give the 3rd, 2 the 2nd, 1 the only one, empty gives None | correct | run |
| 232 | l13-fast-and-slow | `screens[5] answer + whys + explain` | while fast.next and fast raises AttributeError on [1, 2]; and evaluates left to right | correct | run (solution order passes; trap order raises) |
| 233 | l13-fast-and-slow | `screens[6] prose + answer + explain` | The gap shrinks by exactly one per move; speeds 3 and 1 could skip over 0 | correct | run (gap 1 in a cycle of 4 never closes at speeds 3 and 1) |
| 234 | l13-fast-and-slow | `screens[7] code + explain` | has_cycle and middle; compare nodes with is; O(n) time, O(1) space | correct | run (14 tests, including the two peak-memory tests) |
| 235 | l13-fast-and-slow | `screens[8] lines + explain` | slow has taken a + b steps; fast 2(a + b); a + b = kL; a = kL - b; reset to the head and both meet at the start | correct | run (reset finds the start on 1,500 random lists); Knuth, loc. cit. |
| 236 | l13-fast-and-slow | `screens[9] code + feedback` | has_loop on a dict of fallbacks; missing key plays None | correct | run (9 tests) |
| 237 | l13-fast-and-slow | `summary + quiz[0], [1], [3]` | Self-loop returns True; middle of four is 3; tortoise has run 400 m when first lapped | correct | run; relative speed |
| 238 | l13-fast-and-slow | `quiz[2] answer + whys` | Seen-set needs up to n entries; Floyd needs two names; both O(n) time | correct | derivation |
| 239 | l13-fast-and-slow | `quiz[2].explain.text (last sentence)` | 'That is the reason interviewers ask for it' | unverified | Unsourced remark about interview practice. Finding 15 |
| 240 | review-3 | `items[0..6]` | 4 2 5 * + 1 - is 13; next greater [8, 9, 9, 9, -1]; time priority is FIFO; reverse after two passes; meet after 5 moves (a = 3, b = 2, L = 5); window maxima [7, 7, 3, 5, 5]; 2 indices left | correct | run |
| 241 | review-3 | `items[7].prose (sentence 2)` | 'The deepest nesting tells you how many intermediate results a stack-based evaluator holds at once' | imprecise | run: (1 + (2 * (3 - 4))) has depth 3 and a two-stack evaluator holds 4 operands. Finding 18 |
| 242 | review-3 | `items[7] code + explain` | max_depth as a counter; a counter is the stack's height with one bracket kind | correct | run (6 tests) |
| 243 | homework-3 | `items[0] code + explain` | MinStack with a parallel stack of running minimums; O(1) per call, O(n) extra space | correct | run (7 tests) |
| 244 | homework-3 | `items[1] code + prose + explain` | stock_span is the previous greater element; spans 1, 1, 1, 2, 1, 4, 6; O(n) | correct | run (8 tests) |
| 245 | homework-3 | `items[2]` | FIFO basis 17,650; LIFO 17,300; average cost 17,441.67; 250 shares at 49 remain | correct | run |
| 246 | homework-3 | `items[3]` | Order of the six remove_nth_from_end steps | correct | matches l12 screens[9] |
| 247 | homework-3 | `items[4] code + explain` | LRUCache from a dict and a doubly linked list with two sentinels; OrderedDict.move_to_end is the built-in equivalent | correct | run (8 tests); CPython Objects/odictobject.c (dict plus doubly linked list) |
| 248 | homework-3 | `items[5] code + explain` | cycle_start: meet, reset one pointer to the head, walk both | correct | run (10 tests) |
| 249 | homework-3 | `items[6]` | deque is O(1) at both ends; indexing near the middle and membership are O(n) | correct | Python docs collections.deque ('slows to O(n) in the middle'); run (timing) |
| 250 | homework-3 | `items[7].model + rubric` | Waiting days on a stack; loop; at most 2n pushes and pops; < against <=; worked example 2, 1, 3, 2, 1, 0, 0; edge cases | correct | run |
