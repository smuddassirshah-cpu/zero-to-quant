# Claim ledger: cpp levels 4 and 5 (blind concept audit cpp-4-5, round 1)

Files: `app/content/courses/cpp/l14-vector.json` to `l23-own-smart-pointer.json`, `review-4.json`, `review-5.json`, `homework-4.json`, `homework-5.json`, read at commit 6c01af87. Script: `docs/reports/cpp-L4-5-concepts.py` (`sim:` names a job or a check in it; every C++ job is compiled by YoWASP clang 21 for wasm32 with the page's own flags and run in node, and every code widget is graded through the widget's own `unit()`; "base run" is the solution-passes, starter-fails run of every code widget). Sources: N4659 (the C++17 working draft, cited by section; C++17 is the standard the page compiles), Meyers *Effective Modern C++* (by Item), Stroustrup *A Tour of C++*, the Itanium C++ ABI, the CMake and Catch2 documentation, and Hull for the finance formulas.

Rows: 342. Verdicts: correct 306, wrong 7, imprecise 20, misleading 9, unverified 0.

## l14-vector

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l14 | screens[0].prose, widget, explain | `push_back` appends, `size()` counts, `[]` indexes from 0; the snippet prints `3 102`; one fixed element type | correct | N4659 [vector.overview], [ostream.inserters.arithmetic] (`%g` formatting of 102.0); sim: `vec` first=3 102 |
| l14 | screens[0].widget.options[*].why | from-one, last, empty slips | correct | each value follows from the named slip (index 0, size as last index, size 0) |
| l14 | screens[1].prose, explain | Elements sit side by side in one block with spare slots; a full block is replaced by one twice as big; "this library doubles, as libstdc++ does"; room grows 1, 2, 4, 8 | correct | N4659 [vector.overview]/1 (contiguous), [vector.capacity]; growth factor is the library's choice and the text says so; sim: `vec` caps=1,2,4,8 (libc++ under YoWASP) |
| l14 | screens[1].widget.answer, wrong[], feedback.byKey | 5 closes sit in a block of 8; 5 is the size, 6 assumes one spare, 10 doubles the size | correct | sim: `vec` caps5=1,2,4,4,8 |
| l14 | screens[2].prose | `size()` counts elements, `capacity()` slots; `reserve(n)` asks for room up front; a full block doubles here | correct | N4659 [vector.capacity]/3 (`reserve`: capacity >= n) |
| l14 | screens[2].widget.answer | After `reserve(1000)`, 600 pushes move the block 0 times | correct | N4659 [vector.capacity]/6 (no reallocation until size exceeds capacity); sim: `vec` res_same=1 |
| l14 | screens[2].feedback.byKey.ten, eleven, one; explain | Without `reserve`: 10 moves, 11 allocations, 1,023 elements copied; `reserve` allocates once; size stays 0 | correct | 1 + 2 + ... + 512 = 1,023; sim: `vec` moves=10, allocs=11, copied=1023, res_size0=0 |
| l14 | screens[3].prose | n closes give len − n + 1 windows; empty result for n < 1 or n > size | correct | definition; the solution passes the 7 tests (sim: base run) |
| l14 | screens[3].hints[1].text | "Test 4 has 3 closes and n = 4. What is `xs.size() - n + 1` when `size()` is unsigned?" (implied: it wraps) | wrong | 3u − 4 + 1 = 0 modulo 2^32 (N4659 [basic.fundamental]/4); sim: `vec` size_minus_n_plus_1=0; finding 2 |
| l14 | screens[3].feedback.byKey.test-4 | "If the program stopped, `xs.size() - n + 1` wrapped" | wrong | the count is 0 at test 4, so that loop does not stop; the loop `i <= xs.size() - n` does (sim: `l14s3.le_size_minus_n` → test-4, `l14s3.count_wraps_to_zero` → passes all 7); finding 2 |
| l14 | screens[3].widget.tests | The hidden tests reject the unguarded window count | wrong | the loop `i < xs.size() - n + 1` passes all 7 tests and stops for n >= size + 2 (sim: `x.fix_ma_n5`); finding 2 |
| l14 | screens[3].feedback.byKey.test-7 | n = 0 has no windows; dividing by 0 gives nonsense | correct | sim: three codings without `n < 1` fail test 7 first with `{nan, nan, nan}` |
| l14 | screens[3].feedback.byKey.test-2 | The second window is 102, 101, 105, mean 102.67 | correct | 308 / 3 = 102.67; describes its test (a window-start slip fails test 1 first: sim `l14s3.window_one_late`) |
| l14 | screens[3].feedback.byKey.error | "The program stopped. If the message says index out of bounds ..." | correct | the sentence is true (the last start is `xs.size() - n`); the C++ widget gives key `test-N` for a program that stops and `error` only when the runner itself fails (cpp-grade.js, grade()), so the line is not shown for the case it describes: inbox bullet, not a concept finding |
| l14 | screens[3].explain.text | Check n before any `size()` arithmetic because `size()` is unsigned; a running sum costs one step a window | correct | N4659 [basic.fundamental]/4; the solution |
| l14 | screens[4].prose | Simple return p_i / p_{i−1} − 1; n closes give n − 1 returns; `reserve` so the vector never moves | correct | simple-return convention stated; N4659 [vector.capacity] |
| l14 | screens[4].feedback.byKey.test-3 | An empty vector: `px.size() - 1` wraps and `reserve` of that ends the program | correct | sim: `reserve_wrap` (std::length_error, exit 134); codings `l14s4.reserve_no_guard`, `ctor_no_guard`, `loop_to_size_minus_1` all fail test 3 first |
| l14 | screens[4].feedback.byKey.test-5 | Capacity should be 5; 8 means the vector grew by doubling | correct | sim: `l14s4.no_reserve` → test-5 with 8; `reserve_size` → test-5 with 6 |
| l14 | screens[4].feedback.byKey.test-1 | 100 to 110 is 0.1; divide by the earlier close | correct | sim: `l14s4.divide_by_later`, `inverted` → test-1 |
| l14 | screens[4].explain.text | One allocation of the exact size; `size() - 1` of an empty vector is 4.3 billion here, 1.8 × 10^19 on a 64-bit desk; `out(px.size() - 1)` filled by index works too | correct | 2^32 − 1 and 2^64 − 1; "exact" is libc++'s behaviour here (sim: `vec` capr5=5; the standard promises only >= n, which screens[9] states); sim: `l14s4.sized_ctor_ok` passes |
| l14 | screens[5].prose, explain | An iterator marks a place; `[begin, end)`; `*it` reads, `++it` steps; range-for uses the same pair | correct | N4659 [iterator.requirements.general]/7, [stmt.ranged] |
| l14 | screens[5].widget.answer, wrong[] | 303.6; 403.6 adds index 0; 201.3 stops before index 3 | correct | sim: `vec` iter_total=303.6 |
| l14 | screens[6].prose, explain | Read until input ends, sort ascending, print from the back with two limits; `k < prices.size()` compares two unsigned values | correct | N4659 [istream.formatted]; [alg.sort] |
| l14 | screens[6].feedback.byKey.test-2, test-3, test-1 | Two prices; no input; largest first | correct | sim: `l14s6.always_three` → test-2, `three_ifs` → test-3, `from_front` and `no_sort` → test-1 |
| l14 | screens[6].feedback.byKey.error | "The program stopped ..." | correct | the sentence is true; same unreachable `error` key as screens[3] (inbox bullet) |
| l14 | screens[7].prose | `px[i]` does no check: "past the end it reads whatever memory is there"; `at` checks and throws `std::out_of_range`; this app cannot catch | imprecise | undefined behaviour stated as one outcome (N4659 [sequence.reqmts] Table 87: `a[n]` is `*(a.begin() + n)`, undefined out of range); finding 15 |
| l14 | screens[7].feedback.byKey.test-3 | With `[]` this app stops the program with a crash, not `std::out_of_range` | correct | sim: `l14s7.starter` → test-3; `idx_oob` (libc++ hardening assertion, trap) |
| l14 | screens[7].feedback.byKey.test-4, test-5 | `at(-1)` converts to a huge unsigned index and throws; an empty vector has no day 0 | correct | N4659 [conv.integral]/2; sim: `at_neg`; `l14s7.at_to_only`, `manual_upper_only` → test-4 |
| l14 | screens[7].explain.text | `[]` is "undefined past the end"; this app traps it; "a normal release build reads garbage" | imprecise | the first clause is right; the last states one outcome of undefined behaviour as the rule; finding 15 |
| l14 | screens[8].prose, widget (in this app's run) | The loop leaves 101.2, 0, 101.5 | correct | sim: `erase_loop` ticks=101.2,0,101.5 (question says "in this app's run") |
| l14 | screens[8].widget.options[noc], [throw] | It compiles; only `at` throws `std::out_of_range`, `erase` and `++it` do no checks | correct | N4659 [vector.modifiers]/3 to /5 |
| l14 | screens[8].explain.text | `erase` invalidates `it`; using it again is undefined; the fix takes the returned iterator | correct | N4659 [vector.modifiers]/3 ("invalidates iterators and references at or after the point of the erase"); sim: `erase_loop` fixed=101.2,101.5 |
| l14 | screens[9].prose | Summary of the API: `v(5)` five zeros, `reserve` capacity >= n, `erase` returns the next valid iterator, `data()` | correct | N4659 [vector.cons]/3 (value-initialised), [vector.capacity], [vector.modifiers], [vector.data] |
| l14 | screens[9].widget, explain | `for (std::size_t i = v.size() - 1; i >= 0; --i)` never stops; fixes `i-- > 0` or `rbegin()`; an `int i` compares signed with unsigned | correct | N4659 [basic.fundamental]/4, [expr.rel]; clang accepts it without a warning under `-Wall -Wextra` (sim: `size_t_countdown`), GCC's `-Wextra` warns (`-Wtype-limits`), as "some compilers warn" says |
| l14 | screens[10] | Lattice rows of i + 1 nodes; node j went down j times; test values 195.3125, 125, 80, 51.2; 1.25 × 0.8 = 1 | correct | Hull ch. 13 (binomial tree); sim: base run, `l14s10.direct_ok` passes, `steps_rows` and `ups_and_downs_swapped` fail test 1 |
| l14 | summary.ideas, formula, trap | Doubling gives fewer than 2n copies for n pushes, so `push_back` is constant on average; erase then `++it` skips | correct | 1 + 2 + ... + 2^k < 2n; N4659 [vector.overview]/1 (amortised constant) |
| l14 | quiz[0#q-sized-ctor] | `v(3)` holds three zeros; `push_back` makes size 4 | correct | sim: `vec` zsize=4, z0=0 |
| l14 | quiz[1#q-at-end] | `at(3)` on three elements throws `std::out_of_range`, and the program ends here; `px[3]` "might" read what follows in a normal build | correct | sim: `at_oob`; the hedge "might" is right |
| l14 | quiz[2#q-data] | `pv(cf.data(), cf.size())`; `&cf` has the wrong type; a vector does not convert to a pointer; `&v[0]` works when non-empty | correct | sim: `data_ok` compiles; `addr_of_vector`, `vector_as_pointer` do not |
| l14 | quiz[3#q-list] | A vector is faster to sum than a list because 64-byte cache lines bring eight doubles and the CPU prefetches | correct | Drepper, *What Every Programmer Should Know About Memory* §3.3.2 and §6.2.1; Stroustrup, *A Tour of C++* §11.2 (prefer vector) |

## l15-maps

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l15 | screens[0] | A `std::map` iterates in key order: AZN, BARC, VOD; `auto& [sym, qty]` is a structured binding over a `std::pair` | correct | N4659 [associative.reqmts]/9 (ordered by key), [dcl.struct.bind]; sim: `maps` order |
| l15 | screens[0].feedback.byKey.vod | Insertion order is Python's dict, not `std::map` | correct | Python 3.7 language reference (dicts keep insertion order) |
| l15 | screens[1].prose, widget | A `std::map` is a balanced tree; a search for BP goes HSBA, BARC, BP | correct | all three standard libraries use a red-black tree (the standard asks only for logarithmic cost, [associative.reqmts] Table 90); sim: `x.map_depth` depth7_lesson_order=3 |
| l15 | screens[1].feedback.byKey.right, s, b-a | BP sorts before HSBA and after BARC | correct | lexicographic order of `std::string` ([string.ops]) |
| l15 | screens[1].explain.text | "Each comparison throws away half of what is left, so 7 keys need at most 3 steps. A million keys need about 20" | imprecise | a red-black tree is balanced only to height 2 log2(n + 1) (Cormen et al., *Introduction to Algorithms*, Lemma 13.1): 7 keys can sit 4 deep and a million about 20 to 40; sim: `x.map_depth` 4, and 33 for a million sorted inserts, 23 for random ones; finding 20 |
| l15 | screens[1].explain.text | find, insert and erase are O(log n); reading left to right gives the keys in order | correct | N4659 [associative.reqmts] Table 90 |
| l15 | screens[2].prose, widget, explain | `unordered_map` hashes a key to a bucket and compares only the keys there; O(1) on average; no order; buckets grow as keys arrive | correct | N4659 [unord.req]/9 and Table 91 (average constant, worst linear), [unord.req]/15 (rehash keeps the load factor bounded) |
| l15 | screens[2].feedback.byKey.all, tree, one | 7 is a scan, 3 is the tree, 1 forgets AZN in the same bucket | correct | the drawn bucket 3 holds AZN and BP |
| l15 | screens[3] | Sorted output and the highest bid need `map`; lone lookups by id fit `unordered_map` | correct | [associative.reqmts] (ordered, `rbegin()` is the largest key) against [unord.req] |
| l15 | screens[3].explain.text | "When unsure, start with `std::map`: its order makes output repeatable" | correct | advice, consistent with [unord.req] (iteration order unspecified) |
| l15 | screens[4].prose, explain | `pos[sym] += q` works for a new symbol: `[]` inserts it with `int{}` = 0; like `defaultdict(int)` | correct | N4659 [map.access]/1 (value-initialised) |
| l15 | screens[4].feedback.byKey.test-1, test-3, test-4 | `=` overwrites (25); a flat symbol keeps its key (size 1); no fills, size 0 | correct | sim: `l15s4.assign` → test-1 with 25; `erase_flat` → test-3; `maps` flat_key_stays=1 |
| l15 | screens[5].prose, explain | `px[sym]` does not compile on a `const` map because `[]` might insert; `find` returns `end()` for a missing key; `count` needs a second lookup | correct | N4659 [unord.map.elem] (`operator[]` is non-const); sim: `l15s5.index_const` → compile ("no viable overloaded operator[]") |
| l15 | screens[5].feedback.byKey.compile, test-2, test-4 | The compiler names `operator[]`; `at` throws for ZZZ; no prices gives 0 | correct | sim: `l15s5.at` → test-2 (std::out_of_range), `find_unchecked` → test-2 |
| l15 | screens[5].widget.tests | Exposure −330 and 444 | correct | 1000 × 0.72 − 500 × 2.10 = −330; 20 × 118.5 − 300 × 6.42 = 444 |
| l15 | screens[6] | `pos["AZN"] == 0` inserts AZN: prints `flat AZN` then 3; "`[]` never fails" for a map | correct | N4659 [map.access]/1; sim: `maps` flat=1, size_after_read=3 |
| l15 | screens[6].explain.text | To read without inserting use `find`, `count` or `at` | correct | N4659 [map.access], [associative.reqmts] |
| l15 | screens[7].prose, explain | Neither C++ map keeps arrival order; only `std::map` sorts; `unordered_map` order depends on the hash and can change between library versions; `shares[v]` is safe when the key is present | correct | N4659 [unord.req]; sim: `l15s7.unordered` → test-1 (TURQ, CBOE, LSE here), `arrival_order` → test-1 |
| l15 | screens[7].feedback.byKey.test-1, test-4 | Order differs with `unordered_map` or arrival order; AQX 2 25 prints first | correct | sim as above; `l15s7.overwrite_shares` → test-1 |
| l15 | screens[8].prose | `m.count(k)` is 0 or 1; `insert` only if absent; `emplace` the same, built in place | correct | N4659 [associative.reqmts] Table 90 (unique keys) |
| l15 | screens[8].widget, explain | `insert` on an existing key keeps 500 and returns a pair saying it did not insert; `[]` with `=` overwrites; `std::multimap` allows repeats | correct | sim: `maps` after_insert=500, inserted=0, after_emplace=500 |
| l15 | screens[9] | `100.1 + 0.1` is 100.19999999999999, not 100.2, so the `double`-keyed book has 3 levels; key books by integer ticks | correct | IEEE 754 binary64; sim: `maps` levels=3, sum=100.19999999999999 |
| l15 | summary.ideas | Tree: sorted, O(log n); hash: O(1) on average, no order; `[]` inserts a zero value | correct | as the rows above |
| l15 | summary.formula.note | "A million keys: about 20 comparisons in a tree" | imprecise | 20 is the best case; up to about 40 in a red-black tree; finding 20 |
| l15 | summary.trap | `if (pos["AZN"] == 0)` inserts AZN | correct | [map.access]/1 |
| l15 | quiz[0#q-empty-begin] | On an empty map `begin() == end()`; reading `it->second` is undefined; `begin()` never throws | correct | N4659 [container.requirements.general] Table 83 (`begin() == end()` iff empty; `noexcept`); sim: `maps` empty_begin_is_end=1 |
| l15 | quiz[1#q-order] | `unordered_map` order is set by the hash and can differ between libraries, bucket counts or a rehash | correct | N4659 [unord.req]/15; sim: `maps` uorder (not insertion order here) |
| l15 | quiz[2#q-find-missing] | `it == px.end()` is the test; `it == nullptr` does not fit an iterator; `px["BARC"]` inserts; reading through `end()` is not allowed | correct | sim: `find_eq_nullptr` does not compile; [unord.map.elem] |
| l15 | quiz[3#q-cache] | 40,000 ids looked up one at a time fit `unordered_map`; a `map` costs "about 16 comparisons" | correct | log2(40,000) = 15.3 (best case; see finding 20 for the bound) |
| l15 | quiz[3#q-cache].widget.options[v].why, [dk].why | A vector indexed by 64-bit ids would need billions of slots; a `double` key is fragile | correct | 2^64 ids; screens[9] |

## l16-algorithms

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l16 | screens[0] | `std::sort` with `a.sharpe > b.sharpe` puts the largest first; the rule returns true when `a` goes before `b`; `[]() {}` is a lambda | correct | N4659 [alg.sorting]/3, [expr.prim.lambda]; sim: `algos` sorted=mr,mo,tr,va,ca |
| l16 | screens[1] | `std::accumulate(b, e, 0.0)` starts at the third argument and adds each element; the result here is £175.00; the start sets the type | correct | N4659 [accumulate]; sim: `algos` acc_dbl=175 |
| l16 | screens[1].feedback.byKey.first, four | 120.5 is one day, 144.75 four days | correct | canvas sums 120.5, 80.25, 155.25, 144.75, 175 |
| l16 | screens[2] | `[limit]` copies `limit` into the lambda; `count_if` counts 3 of the five returns; `[&limit]`, `[=]`, `[&]` | correct | N4659 [expr.prim.lambda.capture]; sim: `algos` count_snapshot=3 |
| l16 | screens[3].prose, explain | VWAP = Σp·q / Σq; `inner_product` walks two ranges in step; `0.0 / 0.0` is NaN | correct | definition; N4659 [inner.product]; IEEE 754 §7.2; sim: `algos` inner=40300 |
| l16 | screens[3].feedback.byKey.test-3, test-4, test-1 | No fills gives 0/0; zero volume; 101 is the unweighted mean | correct | sim: `l16s3.no_check` → test-3 (nan), `empty_check_only` → test-4, `plain_mean` → test-1 (101) |
| l16 | screens[3].widget.tests | The hidden tests reject totals started at the int `0`, the trap of screens[7] | misleading | sim: `l16s3.int_start` passes all 5 tests (every product in the tests is a whole number); finding 8 |
| l16 | screens[4].prose, explain | Price-time priority: highest bid first, earliest first at one price; like `key=lambda o: (-o.price, o.time)`; the rule must be strict | correct | Harris, *Trading and Exchanges*, ch. 6 (price-time precedence); N4659 [alg.sorting]/3 and /4 (strict weak ordering) |
| l16 | screens[4].feedback.byKey.test-2, test-1 | 7 before 2 means the price tie was not broken; 100.4 means ascending prices | correct | sim: `l16s4.price_only` → test-2 with 9, 7, 2, 4; `ascending` → test-1 with 100.4 |
| l16 | screens[4].feedback.byKey.test-4 | "Six orders at one price. If the program stopped with a strict-weak-ordering message, your rule used `<=` or `>=`" | misleading | six elements never trip libc++'s check (sim: `sort_le_many` n = 6 runs, n = 30 stops); `l16s4.time_le` and `ge_then_le` pass all 5 tests and `price_ge` fails test 2; finding 7 |
| l16 | screens[4].explain.text | Comparing doubles with `!=` is safe here because the prices come from the book unchanged | correct | no arithmetic is done on the keys |
| l16 | screens[5].prose, explain | `adjacent_difference` writes `px[0]` then the differences into a range of the same size; skipping slot 0 is the classic slip | correct | N4659 [adjacent.difference]; sim: `algos` adj=100,4,-3,5,-3 |
| l16 | screens[5].feedback.byKey.test-1, test-2 | Counting `d[0]` gives 3; `d.begin() + 1` on an empty range is past the end | correct | sim: `l16s5.counts_d0` → test-1 with 3; `no_guard` → test-2 |
| l16 | screens[5].feedback.byKey.test-4 | "If you got 1, you counted `d[0]`" as the first failure at test 4 | misleading | that slip fails test 1 first (sim: `l16s5.counts_d0`, `counts_d0_no_guard`); finding 11 |
| l16 | screens[6].prose | `std::transform` writes where its output iterator points and never grows a vector | correct | N4659 [alg.transform]; [iterator.requirements.general] |
| l16 | screens[6].widget.options[ub] (key) | "Nothing: its size is still 0, and three values went to memory it does not own" | imprecise | undefined behaviour given as one outcome with no "in this app"; `pence.begin()` is null, this app writes at address 0 and goes on, a desktop build faults (sim: `transform_empty`); finding 14 |
| l16 | screens[6].widget.options[full], [noc], [throw] | `transform` does not grow `pence`; it compiles; algorithms do not check iterators | correct | [alg.transform] requires only an output iterator |
| l16 | screens[6].explain.text | Algorithms see only iterators; use `std::back_inserter` or `resize` first | correct | N4659 [back.insert.iterator] |
| l16 | screens[7] | `accumulate(b, e, 0)` keeps an `int` total: 120, 79, 154, 143, 173 | correct | N4659 [accumulate]/1 (`acc = acc + *i` in the type of `init`), [conv.fpint]/1 (truncation); sim: `algos` acc_int=173, steps |
| l16 | screens[8].prose | The algorithm list beside its Python | correct | N4659 [alg.sort], [numeric.ops], [alg.min.max], [alg.find], [partial.sum] |
| l16 | screens[8].widget, options | `max_element` of an empty range returns `end()`; it does not throw | correct | N4659 [alg.min.max]/27 ("returns last if first == last") |
| l16 | screens[8].explain.text | Reading through `end()` is undefined; "this app printed nothing at all when we tried it" | correct | sim: `max_empty_deref` (nothing printed for the value; the run then stops) |
| l16 | screens[9].prose, tests | Worst fall of the cumulative P&L from its running peak, counting the £0 start: 150, 80, 0, 50, 11.25 | correct | recomputed by hand in the audit; the solution passes |
| l16 | screens[9].feedback.byKey.test-3, test-1, test-2 | Peak started at the first total gives 30; a by-value `mutable` capture gives 0 | correct | sim: `l16s9.peak_first_guarded`, `peak_minus_inf` → test-3 with 30; `mutable_copies` → test-1 with 0 |
| l16 | screens[9].explain.text | With `[peak, worst]` the assignments do not compile; with `mutable` they change copies; the calls inline so the code is as fast as the hand loop | correct | N4659 [expr.prim.lambda.closure]/4 (call operator is const); sim: `capture_by_value_assign`, `algos` mutable_copy_worst=0; inlining is the usual optimised-build result (Stroustrup, *A Tour of C++* §12) |
| l16 | summary | Algorithms never change a container's size; captures; `accumulate` totals in the type of its start; comparators must be strict | correct | as the rows above |
| l16 | quiz[0#q-le] key, explain | `<=` answers true both ways for equal prices, which breaks `sort`'s rules; `sort` "may run off the end" | correct | N4659 [alg.sorting]/3 and /4 |
| l16 | quiz[0#q-le].widget.options[fine].why | "`sort` can then read past the range; this app's library stops it" | imprecise | on the three prices shown nothing is stopped: they sort to 99.8, 100.5, 100.5 (sim: `sort_le3`); the stop comes on longer ranges (30 and up); finding 7 |
| l16 | quiz[1#q-dangle] | `[&limit]` dangles after `make_filter` returns; capture by value | correct | N4659 [basic.life], [expr.prim.lambda.capture]/12 |
| l16 | quiz[1#q-dangle].explain.text | "Any later call reads freed stack memory" | imprecise | undefined behaviour stated as one outcome; finding 15 |
| l16 | quiz[2#q-sorted-key] | `min_element` with the comparator makes one pass; `find_if` with `f.price` returns the first non-zero price | correct | N4659 [alg.min.max]; [conv.bool] |
| l16 | quiz[3#q-partial] | `partial_sum` of 50, −20, 35 is 50, 30, 65; 50, −70, 55 is `adjacent_difference` | correct | sim: `algos` partial, adjdiff |

## l17-cmake

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l17 | screens[0].prose, widget.answer | The three `.cpp` files become object files; the header and `CMakeLists.txt` do not | correct | N4659 [lex.phases] (a translation unit is a source file with its headers); CMake `add_library`/`add_executable` docs |
| l17 | screens[0].feedback.byKey.hdr, p-i-h, hints[1] | A header is never compiled alone; it is pasted into each `.cpp` that includes it | correct | N4659 [cpp.include]; precompiled headers are a cache of the same text, not a separate object |
| l17 | screens[0].feedback.byKey.p-c | CMake reads `CMakeLists.txt`; the compiler never sees it | correct | cmake(1) |
| l17 | screens[0].explain.text | Each `.cpp` compiles to its own object; the linker joins them; CMake writes the compiler commands | correct | N4659 [lex.phases]/9; cmake-buildsystem(7) |
| l17 | screens[1].canvas, widget.answer | `add_library` (line 7) and `add_executable` (line 10) each create a target | correct | cmake-buildsystem(7) "Binary Targets" |
| l17 | screens[1].feedback.byKey.link, l11, l8, l2, l4 | `target_link_libraries` and `target_include_directories` wire existing targets; `project` names the project; line 4 sets the standard for every target | correct | CMake docs: `CMAKE_CXX_STANDARD` initialises `CXX_STANDARD` of every target created after it |
| l17 | screens[1].explain.text | `PUBLIC include` gives users of `pricing` the include folder; line 11 links `main` against it | correct | CMake `target_include_directories` (PUBLIC populates INTERFACE_INCLUDE_DIRECTORIES) |
| l17 | screens[2].prose | `cmake -S . -B build` configures into `build/`; `cmake --build build` compiles and links; an out-of-source build | correct | cmake(1) "Generate a Project Buildsystem", "Build a Project" (-S/-B since 3.13) |
| l17 | screens[2].canvas | A plain `add_library` makes the static library `libpricing.a` with GNU 13 on Linux | correct | CMake `add_library`: STATIC unless `BUILD_SHARED_LIBS` is on |
| l17 | screens[2].widget.answer, feedback.byKey.lib, l7, l10, l1 | The pricing code joins `main.cpp` at "Linking CXX executable main"; the archive step and the two compile steps join nothing | correct | ld(1); ar(1) packs objects without resolving symbols |
| l17 | screens[2].explain.text | CMake orders the build from `target_link_libraries`; the program is `./build/main` | correct | cmake-buildsystem(7) target dependencies; single-config generators put the executable in the binary dir |
| l17 | screens[3].prose | No second configure is needed; CMake reconfigures itself when `CMakeLists.txt` changes | correct | cmake(1); the generated build system has a regeneration rule |
| l17 | screens[3].widget.answer, wrong[], feedback.byKey.two, zero | After an edit to `main.cpp` one file is compiled, then `main` relinks | correct | make(1)/ninja timestamps; `pricer.cpp.o` is up to date |
| l17 | screens[3].explain.text | The build tool compares file times; 200 files turn minutes into seconds | correct | make(1) (Ninja also uses mtimes); the figure is illustrative |
| l17 | screens[4].prose | Continuous compounding: forward S·e^{rt}, discount e^{-rt}; a namespace groups names as `std` does | correct | Hull, *Options, Futures and Other Derivatives*, ch. 4 (continuous compounding) and ch. 5 (forward price); N4659 [basic.namespace] |
| l17 | screens[4].widget.tests | DF(5%, 2) = 0.9048374180359595; forward 105.12710963760242; PV{5,5,105 at 1,2,3; 4%} = 102.54617478299633; PV{100 at 0.5; 3%} = 98.51119396030627 | correct | sim: `doubles` (df, fwd, pv3, pv1 under YoWASP wasm32) |
| l17 | screens[4].feedback.byKey.compile | A declared function with no matching definition gives an undefined-symbol link error | correct | sim: `l17s4.starter` and `l17s4.wrong_param_types` grade to `compile` with wasm-ld "undefined symbol" |
| l17 | screens[4].feedback.byKey.test-4 | Test 4 is the first present-value test; 5, 5, 105 at 4% is about 102.55 | correct | sim: `l17s4.pv_one_time`, `l17s4.pv_grows` both fail test 4 first |
| l17 | screens[4].explain.text | Other files compile against the header alone; a missing definition passes the compile and fails the link | correct | N4659 [basic.def.odr]/4 (no diagnostic required at compile time), [lex.phases]/9 |
| l17 | screens[5].prose, hints | The definition `year_fraction(int)` does not match the declared `year_fraction(int, int)` | correct | N4659 [over.load] |
| l17 | screens[5].feedback.byKey.compile | A definition with other parameter types is another overload, so the symbol stays undefined | correct | sim: `l17s5.double_params` grades to `compile` |
| l17 | screens[5].feedback.byKey.test-1 | 90/360 = 0.25; 0.2466 means the basis is still 365 | correct | 90/365 = 0.24658; sim: `l17s5.basis_fixed` fails test 1 |
| l17 | screens[5].feedback.byKey.test-2 | "If you got 0, you divided two ints" as the first failure at test 2 | misleading | sim: `l17s5.int_division` fails test 1 first (90/360 is also 0 in ints), so this line is never the first one shown for the slip it names; finding 11 |
| l17 | screens[5].explain.text | Overloading makes `year_fraction(int)` a separate function; the compiler trusts the header and only the linker sees the gap | correct | N4659 [over.load], [basic.link] |
| l17 | screens[6].prose | `-DCMAKE_BUILD_TYPE=Release` gives `-O3` and `NDEBUG`; Debug keeps variables and optimises nothing | correct | CMake `CMAKE_CXX_FLAGS_RELEASE` is `-O3 -DNDEBUG` and `CMAKE_CXX_FLAGS_DEBUG` is `-g` for GCC and Clang (Modules/Compiler/GNU.cmake); `-g` with no `-O` is `-O0`; the screen's session is g++ |
| l17 | screens[6].widget.answer, wrong[], feedback | 1.28 / 0.16 = 8; inverse 0.125; difference 1.12 | correct | arithmetic; sim: the check "l17 screens[6], quiz q-mixed" |
| l17 | screens[6].explain.text | The optimiser keeps values in registers and inlines small functions; time only Release builds | correct | GCC manual §3.11 (`-O0` keeps variables in memory between statements) |
| l17 | screens[7].prose, widget.options[link], explain | The header is found, the code is not linked; `target_link_libraries(main PRIVATE pricing)` fixes it and passes on the PUBLIC include folder, so line 4 can go | correct | CMake `target_link_libraries` (transitive usage requirements) |
| l17 | screens[7].widget.options[hdr].why, feedback.byKey.hdr | `main.cpp` compiled, so the header was found; the error is from `ld` | correct | the canvas shows `collect2: error: ld returned 1 exit status` |
| l17 | screens[7].widget.options[src].why, feedback.byKey.src | Adding `pricer.cpp` to `main` links but compiles the file twice | correct | each target compiles its own sources (cmake-buildsystem(7)) |
| l17 | screens[7].widget.options[std].why | A missing standard shows as compile errors, not at link | correct | diagnostics for language features come from the front end |
| l17 | screens[8].prose | `PUBLIC` passes a setting on to targets that link this one; `PRIVATE` keeps it in; `INTERFACE` library is header-only | correct | cmake-buildsystem(7) "Transitive Usage Requirements", "Interface Libraries" |
| l17 | screens[8].widget.options[chain], explain | `greeks` links `pricing` PUBLIC (its headers mention pricing types); `main` links `greeks` and receives `pricing` through it | correct | CMake `target_link_libraries` |
| l17 | screens[8].widget.options[main].why | Linking both in `main` "often links" but leaves `greeks` without its stated dependency | correct | static archives resolve left to right, so `greeks pricing` links; the dependency is then undeclared |
| l17 | screens[8].widget.options[inc].why, [rev].why | Include directories find headers only; `pricing PUBLIC greeks` is the wrong direction | correct | as above |
| l17 | screens[9].widget.answer, explain | cd, configure (Release), build, run, then build again after an edit; only `pricer.cpp` recompiles (and the targets relink) | correct | cmake(1) |
| l17 | screens[10].widget.options, feedback, explain | `build/` is generated: ignore it; its files are rewritten on configure; `CMakeLists.txt` is the source of every build | correct | cmake(1); gitignore(5) |
| l17 | summary.ideas, formula, trap | Compile per file, link; targets and wiring; configure then build; undefined reference without `target_link_libraries` | correct | as the rows above |
| l17 | quiz[0#q-edit-build] | A flag edited into `build/CMakeFiles/main.dir/flags.make` vanishes at the next generate; use `target_compile_options(main PRIVATE -Wall)` | correct | Makefile generators write `flags.make` on every generate; CMake `target_compile_options` |
| l17 | quiz[1#q-one-file] | One file needs no CMake: `g++ -std=c++17 -O2 vol.cpp -o vol` | correct | g++(1) |
| l17 | quiz[2#q-mixed] | 4.1 / 0.16 ≈ 26; 4.1 / 1.3 ≈ 3; only the Release timing is fair | correct | 25.6 and 3.15; sim: the check "l17 screens[6], quiz q-mixed" |
| l17 | quiz[3#q-interface] | Header-only: `add_library(stats INTERFACE)` with INTERFACE include directories; linking it passes the folder on | correct | cmake-buildsystem(7) "Interface Libraries" |
| l17 | quiz[3#q-interface].widget.options[static].why | A normal library needs source files; a header alone compiles to nothing | correct | CMake reports "Cannot determine link language" for a library with only headers |

## l18-unit-tests

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l18 | screens[0].prose, canvas | C++ tests use a framework such as Catch2 or GoogleTest; the Catch2 v3 file includes `catch_test_macros.hpp` and `catch_approx.hpp` and uses `Catch::Approx` | correct | Catch2 v3 docs, "migrate-v2-to-v3" and "comparing-floating-point" |
| l18 | screens[0].widget, feedback | Line 8, `REQUIRE(price == Approx(10.4506).margin(1e-4));`, does the job of the `assert` line | correct | Catch2 docs "assertions" |
| l18 | screens[0].explain.text | `Approx(10.4506).margin(1e-4)` "is" `pytest.approx(10.4506, abs=1e-4)` | imprecise | Catch2 `Approx` passes when the difference is within the margin OR within its default relative epsilon, 100 × FLT_EPSILON ≈ 1.19e-5 of the value (Catch2 `Approx::equalityComparisonImpl`, read in v2.13.10; unchanged in v3): here 1.245e-4, not 1e-4; pytest takes the larger of abs and rel 1e-6, so 1e-4; finding 19 |
| l18 | screens[1] | On failure Catch2 prints the test name, the line, the check and the check with values ("with expansion"); −10.0 came back; pytest prints `assert -10.0 == 0.0 ± 1.0e-12` | correct | Catch2 console reporter; pytest `approx.__repr__` |
| l18 | screens[2] | A `TEST_CASE` runs from the top once for each leaf `SECTION`, so line 3 runs twice; a failure in one section does not stop the other | correct | Catch2 docs "test-cases-and-sections" |
| l18 | screens[2].feedback.byKey.one, three | One run per section; no extra run | correct | as above (a test case with sections runs once per leaf) |
| l18 | screens[3].prose | The stand-in: `TEST`, `CHECK`, `CHECK_CLOSE(a, b, tol)` passes when \|a − b\| ≤ tol | correct | the prelude macro: `std::fabs((a) - (b)) <= (tol)` |
| l18 | screens[3].widget (planted bugs) | Bug 1 uses σ² for σ²/2, bug 2 pays S − K at expiry, bug 3 does not discount the strike; the solution catches all three | correct | Hull ch. 15 (Black-Scholes-Merton formula); sim: base run; `l18s3.*` |
| l18 | screens[3].hints[1], explain | 10.4506 is rounded to 4 places, so a tolerance of `1e-4` fits | correct | Black-Scholes value 10.450584 (sim: `doubles` bs) |
| l18 | screens[3].feedback.byKey.test-1 | "10.4506 is rounded, so `==` or a tolerance below `1e-4` fails" | wrong | \|10.450584 − 10.4506\| = 1.6e-5, so 2e-5 and 5e-5 pass (sim: `l18s3.tol_2e-5`, `tol_5e-5` pass; `tol_1e-5` and `eq` fail test 1); quiz q-tol says the true value is within 0.00005; finding 3 |
| l18 | screens[3].feedback.byKey.test-2, test-3, test-4 | Empty tests pass; an OTM expiry check catches the missing floor; the ATM value catches the missing discount | correct | sim: `l18s3.starter`, `expiry_only`, `loose_tol` → test-2; `no_otm_expiry` → test-3; `zero_rate_pin` → test-4 |
| l18 | screens[4].prose, explain | The shipped `simple_returns` divides by the later price: 10 / 110 = 0.0909; a failing test documents the bug; flat prices cannot catch it | correct | the prelude; 10/110 = 0.0909 |
| l18 | screens[4].feedback.byKey.test-1 | A new test that passes on the shipped code pins the wrong value or checks nothing | correct | sim: `l18s4.starter`, `pins_shipped_value`, `size_only` → test-1 |
| l18 | screens[4].feedback.byKey.test-2 | "If yours failed, your hand value is wrong: 110 / 100 − 1 = 0.1" | misleading | `CHECK(r[0] == 0.1)` or a zero tolerance, with the right hand value, also fails test 2 first (sim: `l18s4.eq_exact`, `tol_zero`); finding 12 |
| l18 | screens[5] | Two fixes: guard short inputs, divide by the earlier price; the tests define the behaviour | correct | sim: base run |
| l18 | screens[5].hints[1], feedback.byKey.test-1 | `px.size() - 1` on an empty vector wraps and the constructor throws `std::length_error` | correct | N4659 [vector.cons], [vector.capacity] (`length_error` above `max_size()`); sim: `ctor_wrap`; `l18s5.starter`, `divisor_only_fixed`, `guard_only` → test-1 |
| l18 | screens[5].feedback.byKey.error | "The program stopped before printing ..." | correct | the sentence is true; the C++ widget never gives the key `error` for a program that stops (inbox bullet) |
| l18 | screens[6] | `add_test` registers the test program and `ctest` runs it; `REQUIRE_THROWS_AS(expr, type)` tests a throw; GoogleTest has `EXPECT_THROW`; this app cannot catch | correct | CMake `add_test`, ctest(1); Catch2 "assertions"; GoogleTest "Exception Assertions" |
| l18 | screens[7] | `CHECK(r[0] == 0.1)` fails on correct code: 110.0 / 100.0 − 1 is 0.10000000000000009; 1.1 is stored a hair above | correct | IEEE 754; sim: `doubles` rise, rise_eq_01=0 |
| l18 | screens[7].explain.text | Compare within a tolerance: `CHECK_CLOSE(r[0], 0.1, 1e-12)` or `Approx(0.1)` | correct | `Approx(0.1)` allows a relative 1.19e-5, wider than 1e-12 but a tolerance all the same |
| l18 | screens[8] | Arrange, act, assert; a test with no assertion passes whatever the code returns; Catch2 warns only on request | correct | Catch2 command line `-w NoAssertions` |
| l18 | screens[8].widget.options[fail].why | A test fails only when a check fails or the code throws | correct | Catch2 docs "assertions" |
| l18 | screens[9].canvas, tests | CRR binomial call: 100 steps 10.430612, 2,000 steps 10.449584, Black-Scholes 10.450584 | correct | Cox, Ross and Rubinstein (1979); sim: `doubles` crr100, crr2000, bs under the page's compiler |
| l18 | screens[9].hints, feedback.byKey.test-1 | Six decimals allow `1e-6`; a smaller tolerance may not hold | correct | \|10.4306117 − 10.430612\| = 3.4e-7; sim: `l18s9.pin_1e-7`, `pin_1e-9` → test-1 |
| l18 | screens[9].feedback.byKey.test-2, test-3; explain | Bug 1 forgets to discount; bug 2 is one step short and gives 10.4683, which only the pin sees | correct | sim: `doubles` crr99=10.4683, crr1999 within 0.002 of 10.450584; `l18s9.convergence_only`, `pin_loose` → test-3 |
| l18 | summary.ideas, trap | One behaviour per test; doubles need a tolerance; a test with no assertion always passes | correct | as above |
| l18 | summary.formula | \|actual − expected\| ≤ tol; "Catch2: `REQUIRE(x == Approx(e).margin(tol))`" | imprecise | that Catch2 line also passes within a relative 1.19e-5 of e; the absolute-only form is `REQUIRE_THAT(x, Catch::Matchers::WithinAbs(e, tol))`; finding 19 |
| l18 | quiz[0#q-impl] | Pin the hand value 101.5; a test that repeats the implementation checks nothing | correct | (100 × 100 + 102 × 300) / 400 = 101.5; Meszaros, *xUnit Test Patterns* ("calculated values" smell) |
| l18 | quiz[1#q-tol] | For 10.4506 rounded to four places `1e-4` fits; the true value lies within 0.00005 | correct | half a unit in the last place |
| l18 | quiz[2#q-many] | `REQUIRE` stops its test case at the first failure; `CHECK` carries on; other test cases still run | correct | Catch2 docs "assertions" |
| l18 | quiz[3#q-reg] | A failing pin (10.430598 against 10.430612) is a change of 0.000014 to explain before the pin moves | correct | 10.430612 − 10.430598 = 1.4e-5 |

## l19-moving-not-copying

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l19 | screens[0].widget.answer, explain | Lines 2, 5 and 8 copy; 3 and 6 move; 4 and 7 build in place | correct | N4659 [dcl.init]/17.6.1 (a prvalue initialises its target directly), [class.copy.elision]; sim: `tracked` l2 to l8 |
| l19 | screens[0].feedback.byKey.with-make, with-temp, with-move | Since C++17 a returned temporary is built straight into `d`; a temporary argument is built into the parameter; `std::move(a)` moves | correct | as above; Meyers, *Effective Modern C++*, Item 23 |
| l19 | screens[0].feedback.generic | A copy happens when a named object that stays alive is passed or assigned by value | correct | N4659 [over.match.copy]: an lvalue binds to the copy constructor |
| l19 | screens[1].widget, explain | A move copies none of the 1,000,000 doubles; the copy writes 8,000,000 bytes, about 0.8 ms at 10 GB/s; the move writes 8 bytes here and 16 on a desktop | correct | 8e6 / 1e10 s = 0.8 ms; sizeof(Buffer) is 8 here and 16 under both 64-bit ABIs (sim: `virtuals` Buffer=8, `linux64_sizes`) |
| l19 | screens[2].prose | An lvalue has a name and an address; an rvalue is a temporary or a value cast by `std::move`; `Type&&` binds to rvalues; a moved-from object is valid and safe to destroy, with a value nobody promises | correct | N4659 [basic.lval], [lib.types.movedfrom] ("valid but unspecified state") |
| l19 | screens[2].widget, explain | `std::move(a)` does nothing at run time: it is a cast to an rvalue reference | correct | N4659 [forward]/6 (`static_cast<remove_reference_t<T>&&>(t)`); Meyers Item 23; sim: `tracked` cast_only=0,0 |
| l19 | screens[3] | Four `push_back(Tracked(i))` with a `noexcept` move: 0 copies, 7 moves (4 + 1 + 2); capacity 1, 2, 4, 4; the growth factor is a library choice | correct | sim: `tracked` four_pushes=0,7, caps=1,2,4,4 |
| l19 | screens[4].widget.answer | A move that may throw, two pushes: 1 copy and 2 moves | correct | N4659 [vector.modifiers]/1; sim: `tracked_throwing` two_pushes=1,2 |
| l19 | screens[4].widget.options[all-move].why, feedback.byKey.all-move | "It moves only if the move cannot throw; otherwise it copies" | imprecise | true for a copyable type like `Tracked`; a type with no copy constructor is moved even when its move may throw (N4659 [utility] `move_if_noexcept`: `const T&` only if `!is_nothrow_move_constructible_v<T> && is_copy_constructible_v<T>`; sim: `tracked_throwing` move_only_throwing_moves=7); finding 13 |
| l19 | screens[4].explain.text | The library uses `std::move_if_noexcept` to keep the strong guarantee; a move that threw half way would damage the old block | correct | N4659 [vector.modifiers]/1; Meyers Item 14 |
| l19 | screens[5].widget (solution, tests) | A move takes the two fields and nulls the source; the assignment frees its own block behind a guard; neither allocates; both `noexcept` | correct | sim: base run; variants `x.l19s5.*` all rejected (not noexcept → test 11, source keeps size → test 2, no guard → test 8, leak → test 5, copying move → test 4) |
| l19 | screens[5].explain.text | The cost of a move does not depend on the size | correct | two scalar assignments |
| l19 | screens[6].widget.answer, explain | `Order d = std::move(c)` with `const Order c` runs the copy constructor: `const Order&&` binds to `const Order&`, not to `Order&&` | correct | N4659 [dcl.init.ref]/5; Meyers Item 23; sim: `tracked` const_move=1,0 |
| l19 | screens[6].widget.options[move].why | "`std::move` always moves. It yields a `const Order&&` ..." | wrong | the first sentence states the misconception as a fact (feedback.byKey.move has the intended "You believed `std::move` always moves"); finding 4 |
| l19 | screens[6].widget.options[error].why, [ub].why | It compiles; nothing is undefined | correct | as above |
| l19 | screens[7] | A moved-from `std::vector` is valid but unspecified: destroy, assign, `clear()` and `size()` are safe; `v[0]` and `back()` need an element | correct | N4659 [lib.types.movedfrom]; [sequence.reqmts] preconditions; Meyers Item 29 |
| l19 | screens[8].prose, widget | The move pattern; a move must leave a valid object that is safe to destroy; leaving the source unchanged frees the block twice | correct | Stroustrup, *A Tour of C++* §5.2.2; C++ Core Guidelines C.64 |
| l19 | screens[8].explain.text | "Nulling the pointer makes the source destructor a harmless `delete[] nullptr`. That is why the move assignment tests `this != &o` before freeing its own block." | imprecise | the second sentence does not follow from the first: the guard is there because `a = std::move(a)` would free the block and then null its own pointer (sim: `x.l19s5.no_self_guard` → test 8, size 0); finding 21 |
| l19 | screens[9] | Sink argument by value: `keep(history)` copies 1,000,000 doubles once; `keep(std::move(history))` and `keep(load())` copy none; the member assignment is always a move | correct | Meyers Item 41; N4659 [dcl.init] |
| l19 | summary.ideas[0], [1] | A copy duplicates, a move takes and leaves the source empty and destroyable; `std::move` is only a cast; a `const` object copies | correct | as above ("empty" is this lesson's `Buffer`; the library promises only "valid", which screens[7] says) |
| l19 | summary.ideas[2] | "A vector moves its old elements on growth only if their move is `noexcept`. Otherwise it copies" | imprecise | missing "if they can be copied"; finding 13 |
| l19 | summary.formula, trap | Take the pointer, null the source, mark it `noexcept`; `return std::move(t);` blocks elision so a move runs where `return t;` would run none | correct | N4659 [class.copy.elision]/1.1 (NRVO needs the operand to be the name of the local); Meyers Item 25; sim: `tracked` ret_plain=0,0, ret_move=0,1 (NRVO is permitted, not required; the quiz says "on the desk compiler") |
| l19 | quiz[0#q-move-cast] | `std::move` casts and moves nothing; it does not make `a` const | correct | [forward] |
| l19 | quiz[1#q-take-copies] | One of `take(a)`, `take(std::move(a))`, `take(Tracked(3))` copies | correct | sim: `tracked` l5, l6, l7 |
| l19 | quiz[2#q-throwing-growth] | The vector copies because a throw half way through moving would damage the old block; it "chooses not to when a copy is available"; moving is never slower | correct | N4659 [vector.modifiers]/1; the `error` option's why states the copy condition correctly |
| l19 | quiz[3#q-const-move] | A const source falls back to the copy constructor; elision applies to a returned temporary, not to `std::move` of a named object | correct | [dcl.init.ref]; [class.copy.elision] |
| l19 | quiz[4#q-return-move] | `return std::move(t);` blocks copy elision; a returned local is already treated as an rvalue | correct | N4659 [class.copy.elision]/3; sim: `tracked` |

## l20-rule-of-five

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l20 | screens[0] | With only a move constructor declared, `Fill b = std::move(a);` compiles; `Fill b = a;`, `b = a;` and `b = std::move(a);` do not | correct | N4659 [class.copy.ctor]/6 and [class.copy.assign]/2 (copy members deleted), [class.copy.assign]/4 (no implicit move assignment); sim: `fill_move_ctor_only_*` |
| l20 | screens[0].hints[2], feedback, explain | Declaring a move constructor deletes the copy members and writes no move assignment | correct | as above |
| l20 | screens[1].canvas | The 7 × 4 table of what each declaration leaves: nothing; destructor; copy constructor; copy assignment; move constructor; move assignment; all five | correct | N4659 [class.copy.ctor]/6, /8; [class.copy.assign]/2, /4; sim: `special` reproduces all 28 cells with a counting member |
| l20 | screens[1].prose | Copies written after a destructor are deprecated, yet still written | correct | N4659 [depr.impldec] |
| l20 | screens[1].widget.answer, explain | `b = std::move(a)` really moves in 2 of the six declaring rows: a lone move assignment, and all five | correct | sim: `special` |
| l20 | screens[2] | A (nothing) moves; B (destructor) copies; C (copy constructor) copies; D (move constructor) moves; the copy accepts an rvalue, so nothing warns | correct | N4659 [class.copy.ctor]/8; [dcl.init.ref]/5; sim: `special` |
| l20 | screens[2].feedback.generic | "A move is written only if you declared none of the other special members" | correct | [class.copy.ctor]/8 (no user-declared copy constructor, copy assignment, move assignment or destructor) |
| l20 | screens[3].widget, feedback | `Pos(Pos&&) = default` is `noexcept` because the moves of `std::string` and `std::vector` are; the hand-written `Pos3(Pos3&&)` is not | correct | N4659 [except.spec]/7; [string.cons], [vector.cons] (`noexcept` move constructors); sim: `special` pos_nothrow=1, pos3_nothrow=0 |
| l20 | screens[3].explain.text | "The hand-written `Pos3` forgot the keyword, so the vector would copy" | imprecise | as drawn `Pos3` declares only a move constructor, so it has no copy constructor (the prose says the defaulted copy keeps *Pos* copyable) and a vector must move it: sim `special` pos3_copyable=0, growth copies,moves = 0,7; with `Pos3(const Pos3&) = default;` added it is 3,4; finding 13 |
| l20 | screens[3].explain.text | `= default` is the safe way to write a move | correct | C++ Core Guidelines C.80 |
| l20 | screens[4] | Copy assignment order: guard, allocate, copy, free the old block, point, return; freeing first leaves a dangling pointer if `new` throws; copying the address is the shallow-copy bug | correct | Sutter, *Exceptional C++*, Items 12 and 13; Stroustrup *Tour* §5.2.1 |
| l20 | screens[4].feedback.correct, explain | "The guard keeps `a = a` safe"; "the guard handles `a = a`" | imprecise | with allocate, copy, then free, `a = a` is already safe without the guard; see quiz[2]; finding 1 |
| l20 | screens[5].widget (solution, tests) | True copies: one allocation each, old block freed, `a = a` safe | correct | sim: base run; `x.l20s5.assign_leaks_old` → test 6 (leak), `shallow_ctor` → test 1 (double delete) |
| l20 | screens[5].explain.text | Allocating before freeing, behind a guard, is the habit to say in an interview | correct | Sutter Item 13 (the guard is then an optimisation) |
| l20 | screens[6] | `Book` declares a destructor, so `push_back(std::move(b))` copies all 1,000,000 fills; removing the destructor or declaring all five restores the move | correct | [class.copy.ctor]/8; sim: `special` dtor row |
| l20 | screens[7] | `Order` with a `unique_ptr` member and a declared destructor: `Order b = std::move(a);` does not compile, because the implicitly declared copy constructor is deleted and is still chosen | correct | N4659 [class.copy.ctor]/10 (defaulted copy constructor deleted for a non-copyable member), [over.match]/3 (a deleted function takes part in overload resolution); sim: `order_move_deleted` |
| l20 | screens[8] | Declare one of the five and decide all five; rule of zero; `struct Book { std::vector<Fill> fills; ~Book(); };` copies on `b2 = std::move(b1)` | correct | C++ Core Guidelines C.20, C.21; sim: `special` dtor row |
| l20 | screens[9] | Only `FeedHandle { int fd; }` needs hand-written members: delete the copy, write the move | correct | Core Guidelines C.21, R.1 |
| l20 | summary.ideas[0], [1] | A destructor or copy member hides the moves; a move constructor deletes the copies; a deleted function is chosen, not absent | correct | as above |
| l20 | summary.ideas[2] | "A defaulted move is `noexcept` when its members are; a hand-written one is not" | imprecise | a hand-written move is `noexcept` exactly when you write it (screens[3] says so); finding 22 |
| l20 | summary.trap | A class with a destructor still compiles `std::move(a)`: it quietly copies | correct | sim: `special` |
| l20 | quiz[0#q-copy-ctor-only] | With only a copy constructor declared, `b = std::move(a)` copies through the implicit copy assignment | correct | [class.copy.assign]/2, /4; sim: `special` copy_ctor row |
| l20 | quiz[1#q-zero-line] | Rule of zero: own through self-managing members and declare no special members | correct | Core Guidelines C.20 |
| l20 | quiz[2#q-self-guard] key, options[time].why, explain | "For correctness: `a = a` would free the block it is about to copy from", said of the `Samples` copy assignment | wrong | the lesson's `Samples` allocates and copies before it frees (screens[4] rejects the free-first line), so `a = a` is correct without the guard: sim `samples_no_guard` (size 10, data intact) and `l20s5.no_guard_alloc_first` (passes all 13 hidden tests); the explain itself says allocate-then-free prevents it; finding 1 |
| l20 | quiz[3#q-unique-class] | A class holding a `unique_ptr` and declaring nothing is movable, not copyable | correct | [class.copy.ctor]/10; sim: `special` holder=0,1 |

## l21-virtual-dispatch

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l21 | screens[0].prose, canvas | Sizes are for this app's 32-bit WebAssembly compiler: pointers are 4 bytes, 8 on a desktop; `Tick` is 4, `VTick` is 8 here and 16 on a desktop | correct | sim: `virtuals` Tick=4, VTick=8; `linux64_sizes` VTick 16 (MSVC x64 also 16) |
| l21 | screens[0].widget, explain | The extra bytes are a hidden pointer (vptr) to the class's table of functions, one per object; the table is shared by the class | correct | Itanium C++ ABI §2.5 (virtual table layout); Lippman, *Inside the C++ Object Model*, ch. 4; the standard does not name the mechanism, every mainstream ABI uses it |
| l21 | screens[0].widget.options[code], [padding], [name] | Code is stored once; `px` and the pointer are 4 bytes each here, so no padding; type information hangs off the table | correct | Itanium ABI §2.5.2 (RTTI pointer in the vtable) |
| l21 | screens[1] | `p->value(110)` visits the object, then its class's table, then the function; the table comes from the object, not from the pointer's type | correct | Itanium ABI §2.5; N4659 [class.virtual]/2 (final overrider) |
| l21 | screens[2].widget.answer | `sizeof(D)` is 12 here: vptr, `x`, `y` | correct | sim: `virtuals` B=8, D=12 |
| l21 | screens[2].feedback.byKey.sixteen, explain | "That is the desktop answer"; "A desktop gives 16, with an 8-byte pointer" | imprecise | true for the Itanium ABI (Linux, macOS: `y` goes into B's tail padding, sim `linux64_sizes`); MSVC x64 gives 24 (sim: `win64_D_is_24` holds, `win64_D_is_16` fails); finding 16 |
| l21 | screens[3] | `Quote` (vptr and two doubles) is 24 here: 4 + 4 padding + 16; a desktop also gives 24, 8 + 16 with no padding | correct | wasm32 aligns `double` to 8 (tool-conventions BasicCABI); sim: `virtuals` Quote=24, align_double=8; `linux64_sizes` |
| l21 | screens[4] | `Payoff q = c;` slices: `q` is a `Payoff` whose vptr is `Payoff`'s, because each constructor sets its own class's table | correct | N4659 [class.copy.ctor]; [class.cdtor]/4; Stroustrup, *The C++ Programming Language* §17.5.1.4 (slicing); sim: `virtuals` sliced=-1, via_ref=10 |
| l21 | screens[5].widget | The hand-made vtable: `value_of` reads the table and calls through it; one table per kind | correct | sim: base run; `x.l21s5.ignores_table` → test 3 |
| l21 | screens[5].explain.text | The compiler writes the same two steps; the cost per object is one pointer | correct | Itanium ABI §2.5 |
| l21 | screens[6] | `delete p` through a `Base*` whose destructor is not virtual is undefined behaviour; typically `~Derived` never runs and the vector leaks | correct | N4659 [expr.delete]/3 |
| l21 | screens[6].widget.options[defined], [smart], [error] | Not defined-with-leak; `delete` does not find the real type; it compiles | correct | [expr.delete]/3 |
| l21 | screens[6].explain.text | The fix `virtual ~Base() = default;` costs the 4 bytes of a vptr here | correct | sim: `virtuals` (one pointer) |
| l21 | screens[7] | A virtual call in `Base`'s constructor reaches `Base::name`: `d.who` is "Base"; well defined | correct | N4659 [class.cdtor]/4; Meyers, *Effective C++*, Item 9; sim: `virtuals` ctor_call=Base |
| l21 | screens[7].explain.text | Each constructor sets the vptr to its own class's table before its body runs | correct | Itanium ABI §2.6 (construction vtables) |
| l21 | screens[8] | A virtual call: load the vptr, index the table at a slot fixed at compile time, call with `p` as `this`; no search by name; two loads and an indirect jump | correct | Itanium ABI §2.5; Driesen and Hölzle (1996), "The direct cost of virtual function calls in C++" |
| l21 | screens[9] | A virtual destructor, `override`, hold through a pointer or reference; `p->f()` runs the real type's function when `f` is virtual and `p` is a pointer or reference | correct | N4659 [class.virtual]; Core Guidelines C.35, C.128, ES.63 |
| l21 | screens[9].widget.options[always].why, [value].why | A non-virtual `f` is chosen by the pointer's type; a by-value object is a base object | correct | [class.virtual]/9; slicing |
| l21 | screens[10] | A template on the payoff type resolves the call at compile time; `inline` does not; `final` helps only when the compiler sees the exact type; a virtual call usually stops inlining | correct | N4659 [temp.inst]; GCC and Clang devirtualise through `final` only for a static type that is final |
| l21 | summary | One table per class, one vptr per object; slicing keeps the base's vptr; delete through a base only with a virtual destructor; virtual calls in a constructor reach that class | correct | as above |
| l21 | quiz[0#q-sizeof-virtual] | `struct W { virtual void f(); int n; };` is 8 here; a desktop gives 16 | correct | sim: `virtuals` W=8; `linux64_sizes` W 16 (MSVC x64 also 16: 8 + 4 + 4 padding) |
| l21 | quiz[1#q-override] | `override` gives a compile error if nothing in a base is overridden; it changes nothing at run time | correct | N4659 [class.virtual]/5 |
| l21 | quiz[2#q-abstract] key | "An abstract class: it cannot be built, and each derived class must override `value`" | imprecise | a derived class may leave `value` pure and stay abstract; only a class that is built needs the override (N4659 [class.abstract]/4; sim: `abstract_middle_class` compiles); finding 18 |
| l21 | quiz[2#q-abstract].widget.options[static].why, explain | `= 0` means no body is required in the base; the class acts as an interface | correct | [class.abstract]/2 |
| l21 | quiz[3#q-vector-slice] | A `std::vector<Payoff>` given a `Call` holds sliced `Payoff` objects; hold `std::unique_ptr<Payoff>` | correct | sim: `virtuals` vector_slice=-1 |

## l22-undefined-behaviour

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l22 | screens[0].prose | This app never runs undefined behaviour on these screens; whatever happens is allowed, so the answer could differ by build | correct | N4659 [defns.undefined], [intro.execution]/5 |
| l22 | screens[0].canvas, widget, explain | After `int v = *p;` the compiler may assume `p` is not null and delete the later null test; clang for wasm32 at `-O1` emits no test | correct | [intro.execution]/5; Lattner, "What Every C Programmer Should Know About Undefined Behavior" (2011), part 1; sim: `ub_null_check` (first(nullptr) does not return −1) |
| l22 | screens[0].widget.options[drops], [bug], [never] | Not every `if` is dropped; not a compiler bug; `nullptr` is a real value | correct | as above |
| l22 | screens[1].prose | In the standard this app uses (C++17), reading a variable before it is set is undefined | correct | N4659 [dcl.init]/12 (indeterminate value; C++26 changes this to erroneous behaviour, hence "the standard this app uses") |
| l22 | screens[1].widget.answer, feedback, explain | Lines 4 (`a[3]`), 6 (`x + 1` unset) and 8 (`big + 1`) are undefined; line 3 (`u - 1`) wraps to 4,294,967,295 | correct | N4659 [expr.add]/4, [dcl.init]/12, [expr]/4, [basic.fundamental]/4; sim: `ub_misc` u_minus_1 |
| l22 | screens[2].prose, explain | Defined, implementation-defined, unspecified, undefined: what each means | correct | N4659 [defns.impl.defined], [defns.unspecified], [defns.undefined] |
| l22 | screens[2].feedback.byKey.t1, t2 | `UINT_MAX + 1u` is 0; `-7 / 2` is −3 (towards zero since C++11) | correct | [basic.fundamental]/4; [expr.mul]/4; sim: `ub_misc` uint_max_plus_1=0, `doubles` neg7_div_2=-3 |
| l22 | screens[2].feedback.byKey.t3 | "`sizeof(long)` is implementation-defined: 4 here and 8 on a desktop" | imprecise | 8 on 64-bit Linux and macOS (LP64), 4 on 64-bit Windows (LLP64): sim `win64_long_is_4` holds; finding 17 |
| l22 | screens[2].feedback.byKey.t4, t5 | Plain `char` signedness is implementation-defined; the order of evaluating arguments is unspecified | correct | N4659 [basic.fundamental]/1; [expr.call]/5 |
| l22 | screens[2].feedback.byKey.t6, t7, t8, t9 | `INT_MAX + 1`, `v[3]` on three elements, `int x; return x;`, `1 << 32` for an `int` are undefined | correct | [expr]/4; [sequence.reqmts]; [dcl.init]/12; [expr.shift]/1 |
| l22 | screens[3] | `-fsanitize=undefined` turns the run-time reports on; `-Wall` is compile time; `-O0` and `-g` report nothing; `-fsanitize=address` for memory errors; this app's hardening stops an out-of-range vector index but not an overflow or a null read | correct | GCC manual "Instrumentation Options"; sim: `idx_oob`, `ub_null_read`, `ub_misc` |
| l22 | screens[4].widget.solution, hints | `add_overflows`: for b > 0, a > INT_MAX − b; otherwise a < INT_MIN − b; neither subtraction can overflow | correct | CERT C INT32-C (compliant precondition test) |
| l22 | screens[4].feedback.correct, generic, widget.tests | "Your check never overflows, so it stays defined on every input"; "a test that calls `a + b` has already gone wrong" | misleading | the hidden tests accept the classic check made after the sum: `int s = a + b;` then the sign test passes all 13 and gets this feedback (sim: `l22s4.after_sign`); finding 6 |
| l22 | screens[4].explain.text | "This app's compiler removes a check made after the addition. Another build might not" | imprecise | it removes the `s < a` form (sim: `ub_misc` after_check_max=0, `l22s4.after_sum_lt` → test-1) and keeps the sign form, which then works by wrap-around; finding 6 |
| l22 | screens[5] | A null read is undefined: the standard promises neither a crash nor a value; this app reads address 0 without complaint | correct | N4659 [expr.unary.op]/1 with [intro.execution]/5; sim: `ub_null_read` |
| l22 | screens[6] | `v.size() - 1` on an empty vector is 4,294,967,295 here and 18,446,744,073,709,551,615 with an 8-byte `size_t`; defined; `i >= 0` is always true | correct | [basic.fundamental]/4; sim: `ub_misc` size_minus_1 |
| l22 | screens[7] | The defined check: split on the sign of `b`, compare with a shifted limit; adding first leaves nothing defined to compare | correct | CERT INT32-C |
| l22 | screens[8] | A comparator that is not a strict weak ordering makes `std::sort` undefined; `a <= b` is the one; `<`, `>` and `abs(a) < abs(b)` are fine | correct | N4659 [alg.sorting]/3; sim: `sort_le_int` (stopped by the library from 30 elements) |
| l22 | screens[9] | A clean test run and a silent sanitiser cover only the inputs run, on that build | correct | UBSan documentation ("detects only bugs that happen at run time") |
| l22 | screens[10] | 5,000 fills of £5,000 are 2,500,000,000 pence, above `INT_MAX`; use `std::int64_t`; `unsigned` only doubles the range to £42,949,672.95; `double` is exact to 2^53 | correct | arithmetic; IEEE 754 (53-bit significand); sim: `ub_misc` pence, over |
| l22 | summary | Undefined behaviour puts no limit on the run; signed overflow, an index past the end, an unset read and a shift by the width are undefined; check before the operation | correct | as above |
| l22 | quiz[0#q-signed-unsigned] | Unsigned overflow wraps by definition; signed overflow is undefined | correct | [basic.fundamental]/4; [expr]/4 |
| l22 | quiz[1#q-flag] | `-fsanitize=undefined` | correct | GCC manual |
| l22 | quiz[2#q-int-max-pounds] | 2,147,483,647 pence is £21,474,836.47 | correct | arithmetic |
| l22 | quiz[3#q-array-write] | `int a[4]; a[4] = 0;` is undefined | correct | [expr.add]/4, [expr.unary.op] |

## l23-own-smart-pointer

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l23 | screens[0] | Building a shared pointer from `new` allocates twice (object and counter); copies allocate nothing; the last owner frees both | correct | N4659 [util.smartptr.shared.const]; sim: `smart` shared_new=2, copy_allocs=0 |
| l23 | screens[1] | Three owners share one counter on the heap; a count inside each pointer could not be shared | correct | [util.smartptr.shared]/1; Meyers, *Effective Modern C++*, Item 19 |
| l23 | screens[2].widget (solution, tests) | `UniquePtr`: destructor deletes, copy deleted, moves null the source, `release()` gives up without deleting, `reset(p)` stores then deletes the old object; the move assignment takes the source before it lets go | correct | N4659 [unique.ptr.single.asgn], [unique.ptr.single.modifiers]/4 (`reset` order); sim: base run; `x.l23s2.assign_deletes_first` → test 15, `release_deletes` → test 7, `reset_deletes_first` passes (allowed) |
| l23 | screens[2].hints[0], explain | Deleting a null pointer is safe; exactly one destructor frees each object | correct | N4659 [expr.delete]/7 |
| l23 | screens[3] | `sizeof(std::unique_ptr<int>)` is one pointer and `sizeof(std::shared_ptr<int>)` two: 4 and 8 here; the second pointer leads to the counter block; the deleter lives in that block | correct | sim: `virtuals` unique=4, shared=8; Meyers Items 18 and 19 |
| l23 | screens[4] | Copy assignment: read `other` into locals and add one, drop your own share, set from the locals; dropping first breaks `a = a` and `head = head->next` | correct | N4659 [util.smartptr.shared.assign]/1 (equivalent to `shared_ptr(r).swap(*this)`); sim: `x.l23s5.copy_drop_first` → test 6, `copy_drop_first_guarded` → test 14 |
| l23 | screens[5].widget (solution, tests) | `SharedPtr` with a heap `long` count: copy adds, destructor subtracts and frees both at zero, moves take without adding; `use_count()` is 0 when empty | correct | [util.smartptr.shared.obs] (`use_count` 0 for empty); sim: base run; variants `x.l23s5.*` rejected (no increment → test 2, counter never freed → test 1, move drops first → test 15); add-first with no guard passes, as it should |
| l23 | screens[6] | Two `SharedPtr`s built from one raw pointer each start a count at 1, so the object is deleted twice: undefined behaviour | correct | N4659 [util.smartptr.shared.const]/4 and the note at /7; [expr.delete]/2; Meyers Item 19 |
| l23 | screens[6].explain.text | Make a shared owner with `make_shared`, or copy an existing `shared_ptr` | correct | Core Guidelines R.22 |
| l23 | screens[7] | `a` and `b` share one object; after `b = std::move(a)` the count is 1 and `a` is empty | correct | the lesson's move assignment; `std::shared_ptr` agrees (sim: `smart` move_assign_count=1, a_count=0) |
| l23 | screens[8].prose | The count is atomic, the object is not; `weak_ptr` adds nothing to the (use) count; `enable_shared_from_this` lets an object hand out owners of itself; unique has no overhead | correct | N4659 [util.smartptr.shared]/4, [util.smartptr.weak], [util.smartptr.enab]; Meyers Items 18 to 20 |
| l23 | screens[8].widget, explain | Copying a `shared_ptr` costs an atomic add to the count; moving does not touch it | correct | Meyers Item 19 ("moving std::shared_ptrs is faster than copying") |
| l23 | screens[9] | 200,000 messages a second: 400,000 allocations with `shared_ptr(new Message)`, 200,000 with `make_shared`; 200,000 × 50 ns = 10 ms saved | correct | sim: `smart` shared_new=2, make_shared=1; arithmetic |
| l23 | summary | A smart pointer's destructor frees what it owns; shared holds two pointers; add before dropping; never two shared pointers from one raw pointer | correct | as above |
| l23 | quiz[0#q-deleter] | The custom deleter lives in the counter (control) block with the count and the weak count | correct | Meyers Item 19; [util.smartptr.shared.const]/8 to /10 |
| l23 | quiz[1#q-weak-count] | `use_count()` is 2 with `a`, a `weak_ptr` and `b` | correct | sim: `smart` weak_count=2 |
| l23 | quiz[2#q-make-shared] | `std::make_shared<T>()` makes one allocation | correct | N4659 [util.smartptr.shared.create]/7 (a remark: "should perform no more than one memory allocation"; libc++, libstdc++ and MSVC all do); sim: `smart` make_shared=1 |
| l23 | quiz[3#q-release-reset] | `reset()` deletes; `release()` returns the pointer and stops owning it | correct | [unique.ptr.single.modifiers] |

## review-4

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| review-4 | items[0#r4-capacity] | Five pushes: capacity 1, 2, 4, 4, 8; `reserve(5)` first would make it exactly 5 ("this library doubles") | correct | sim: `vec` caps5, capr5=5 |
| review-4 | items[1#r4-erase] | `it = pnl.erase(it)` and step only when keeping; the `++it` and index loops skip the element that slides in; `erase(remove_if(...), end())` does the same | correct | N4659 [vector.modifiers]/3; [alg.remove]; sim: `erase_loop` idx=1,-3,4 |
| review-4 | items[2#r4-count] | `m["VOD"];` inserts, `count` does not: size 1 | correct | sim: `maps` r4count=1 0 0 |
| review-4 | items[3#r4-which-map] | Sorted output: `std::map`; "a few thousand symbols cost about a dozen comparisons each" | correct | log2(4,000) = 12 (best case; see finding 20 for the bound) |
| review-4 | items[4#r4-acc-int] | `accumulate(fees, 0)` over four 2.5s is 8 | correct | sim: `algos` fees=8 |
| review-4 | items[5#r4-comparator] | Asks: lowest price first, then earliest; `<=` is not strict; `>` is the bid order | correct | [alg.sorting]/3; l16 screens[4] |
| review-4 | items[6#r4-linker] | An undefined reference to `vwap` from `tests` is fixed by `target_link_libraries(tests PRIVATE pricing)` | correct | CMake `target_link_libraries` |
| review-4 | items[7#r4-aaa] | Arrange, act, assert; the two checks in either order | correct | Beck, *Test-Driven Development*; the widget's `same` group |
| review-4 | items[8#r4-tol] | `(10.1 + 10.2) / 2` is 10.149999999999999, not the double nearest 10.15; compare with `CHECK_CLOSE(..., 1e-9)` | correct | sim: `doubles` mid, mid_eq=0, vwap_eq=0 |

## review-5

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| review-5 | items[0#r5-take-copies] | With `const Tracked k`: `take(k)` and `take(std::move(k))` copy, `take(Tracked(3))` does not: 2 | correct | sim: `tracked` take_const, take_move_const, take_temp |
| review-5 | items[1#r5-growth-copies] | A `noexcept` move or `reserve(n)` stops the copies on growth; `emplace_back` and a faster copy do not | correct | [vector.modifiers]/1; sim: `tracked_throwing` four_emplace=3,0, four_reserved=0,4 |
| review-5 | items[2#r5-order-compiles] | `struct Order { unique_ptr<Fill> fill; ~Order() {} };`: only `Order d;` compiles | correct | sim: `special` order=1,0,0,0,0 |
| review-5 | items[3#r5-defaulted-nothrow] | `Pos` with a defaulted move is nothrow move constructible; the rule is in the standard | correct | N4659 [except.spec]/7; sim: `special` pos_nothrow=1 |
| review-5 | items[4#r5-sizeof-quote] | `struct S { virtual void f(); char c; };` is 8 here; a desktop gives 16 | correct | sim: `virtuals` S=8; `linux64_sizes` (MSVC x64 also 16) |
| review-5 | items[5#r5-virtual-dtor] | A virtual destructor is needed for `delete` through `Base*` and for `unique_ptr<Base>`; not for `shared_ptr<Base>` from `make_shared<Derived>()` nor for a stack object | correct | [expr.delete]/3; [unique.ptr.dltr.dflt]; [util.smartptr.shared.const] (the deleter is fixed at construction); sim: `shared_base_no_virtual` |
| review-5 | items[6#r5-which-undefined] | `a[4] = 1`, `++x` at `INT_MAX` and reading an unset `int` are undefined; `--u` at 0 and `v.at(5)` are defined | correct | as l22 |
| review-5 | items[7#r5-count-and-money].parts[0] | `a`, `b = a`, `c = std::move(b)`: `a.use_count()` is 2 | correct | sim: `smart` moved_count=2, b_empty=1 |
| review-5 | items[7#r5-count-and-money].parts[1] | 2,500,000,000 − 2,147,483,647 = 352,516,353 | correct | sim: `ub_misc` over |
| review-5 | items[8#r5-unique-move-assign] | Guard, take theirs, null theirs, free your own, keep theirs, return; freeing first breaks `head = std::move(head->next)` | correct | sim: `x.l23s2.assign_deletes_first` → test 15 |
| review-5 | items[9#r5-two-from-raw] | `shared_ptr<T> b(a.get())` starts a second count: the object is deleted twice | correct | Meyers Item 19 |

## homework-4

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| homework-4 | items[0#h4-vwap-book] solution, expects | Group by `std::map`, sort each symbol's trades by price, print count, VWAP, low, high to four places: 72.2600, 210.6667, 4.7700, 27.0900, 6.4250 | correct | recomputed in the script (`h4-vwap-book expects`); sim: base run |
| homework-4 | items[0].widget.tests | The hidden tests enforce alphabetical order | misleading | a program that groups with `std::unordered_map` passes all 5: every test happens to bring its symbols in reverse alphabetical order, which is libc++'s iteration order for a small table (sim: `h4i0.unordered` passes; `x.fix_misc` shows SHEL, BP, AZN for the in-order arrival); finding 9 |
| homework-4 | items[0].feedback.byKey.test-1, test-2 | Key order, weighting, four decimals; no trades, no output | correct | sim: `h4i0.no_sort`, `no_fixed` → test-1 |
| homework-4 | items[0].feedback.byKey.test-4 | "If you got 4.75, you averaged the prices without weights" as the first failure at test 4 | misleading | the unweighted mean fails test 1 first (VOD 72.3000): sim `h4i0.unweighted`; finding 11 |
| homework-4 | items[1#h4-test-drawdown] | 100, 120, 90, 130, 104: worst fall 0.25 (120 to 90), last fall 0.2 (130 to 104); each planted bug is caught by one clause | correct | 30/120 and 26/130; sim: `h4i1.*` (no_new_peak → test-2, peak_of_one → test-3, no_empty_call → test-4, worst_is_last → test-5, wrong_hand_value → test-1) |
| homework-4 | items[2#h4-build-order] | Configure, build, `ctest --test-dir build`, fix in `src/`, build, test | correct | cmake(1), ctest(1) (`--test-dir` needs CMake 3.20; see items[7]) |
| homework-4 | items[3#h4-reserve-grow] | `reserve(100)` then 150 pushes: capacity 200; doubling starts from the current capacity | correct | sim: `vec` h100=100, h150=200 |
| homework-4 | items[4#h4-capture] | A by-value capture is a snapshot: n is 3; `[&limit]` would count none | correct | sim: `algos` count_snapshot=3, count_ref=0 |
| homework-4 | items[5#h4-two-libs].prose | With `report` linked to nothing, "the build of `report` fails with an undefined reference to a `pricing` function" | wrong | `report.o` refers only to what `report.cpp` calls, the `risk` functions, so the linker names those; a `pricing` symbol is first needed once `risk` is linked (sim: `linker_names_caller_symbol`); finding 5 |
| homework-4 | items[5].widget, explain | The missing line is `target_link_libraries(report PRIVATE risk)`; linking `risk` brings `pricing` along because CMake follows the chain of static libraries, PRIVATE or PUBLIC | correct | CMake `target_link_libraries` ("Libraries for a Target and/or its Dependents": a static library's PRIVATE dependencies stay on the link line) |
| homework-4 | items[6#h4-find-or-index] | `px[sym]` on a `const std::map` does not compile; use `find` or `at`; by value compiles but copies the map and inserts into the copy | correct | sim: `const_map_index` fails, `map_by_value_index` compiles |
| homework-4 | items[7#h4-library-plan].model | Layout, one library linked by both tools and the tests, Catch2 v3 through `find_package(Catch2 3 REQUIRED)` and `Catch2::Catch2WithMain`, `add_test`, Release for timing | correct | Catch2 docs "cmake-integration"; CMake docs |
| homework-4 | items[7].model (tests) | Pin 10.430612 within 1e-6; Black-Scholes 10.4506 within 1e-4; 2,000 steps within 0.002; payoff at expiry; put-call parity C − P = S − K·e^{−rT}; bad input throws | correct | sim: `doubles`; Hull ch. 11 (put-call parity) |
| homework-4 | items[7].model (CMake) | `cmake_minimum_required(VERSION 3.16)` beside `ctest --test-dir build-release` | imprecise | `ctest --test-dir` was added in CMake 3.20 (ctest(1), "New in version 3.20"); finding 23 |
| homework-4 | items[8#h4-test-median] | The five planted slips (no sort, integer mean, `int` sum, upper middle, crash on empty) are each caught by one clause of the specification; the solution's values 200, 350.5, 1,999,999,999.5, 5,000, 0 | correct | sim: base run; hand values |

## homework-5

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| homework-5 | items[0#h5-scope-guard] | A scope guard runs its callback once unless dismissed; a `noexcept` move hands the duty over; three guards in a growing vector run exactly 3 times | correct | Alexandrescu and Marginean (2000), "Generic: Change the Way You Write Exception-Safe Code"; sim: base run; `x.h5i0.source_stays_active` → test 3, `move_not_noexcept` → test 11 |
| homework-5 | items[1#h5-vec] solution, how | `Vec<T>` on raw storage: 1,000 pushes allocate 11 times and end at capacity 1,024; 8 pushes of a `noexcept`-move type run 0 copies and 15 moves; build the new element before the old block goes | correct | 1 + 2 + ... + 1,024; 8 + 1 + 2 + 4; sim: base run; `x.h5i1.copy_on_growth` → test 5, `build_after_free` → test 14 |
| homework-5 | items[1].prose, widget.tests | "It must ... move on growth when it is `noexcept`" (and so copy otherwise) is checked | misleading | a `Vec` that always calls `std::move` on growth passes all 15 tests: no hidden type has a throwing move (sim: `x.h5i1.plain_move_on_growth`); finding 10 |
| homework-5 | items[2#h5-sink] | By value then move: an lvalue costs one copy of 1,000,000 doubles, an rvalue none; two overloads avoid the extra move and can reuse capacity | correct | Meyers Item 41 |
| homework-5 | items[3#h5-shared-move-assign] | Guard, read the source into locals, empty the source, drop your own share, set from the locals; adding one leaks; leaving the source's pointers in place double-drops | correct | sim: `x.l23s5.move_drop_first` → test 15 |
| homework-5 | items[4#h5-members-table] | Twelve cells for a lone copy assignment, move assignment, move constructor and destructor | correct | sim: `special` (all 12 match) |
| homework-5 | items[5#h5-six-snippets] | Undefined: `push_back` inside a range-for, `-INT_MIN`, `buf[4] = 0`, double `delete`; defined: `1u << 31` (2,147,483,648) and `7 / 2` | correct | N4659 [vector.modifiers]/1 (reallocation invalidates iterators; `v{1, 2, 3}` has no spare room), [expr]/4, [expr.add]/4, [expr.delete]/2, [expr.shift]/2; sim: `ub_misc` one_shl_31 |
| homework-5 | items[6#h5-virtual-parts] | `struct B { virtual void f(); double x; };` is 16 here; a sliced `Payoff` runs `Payoff`'s version; vectors of `unique_ptr<Payoff>` or of `const Payoff*` avoid the slice; a vector of references cannot exist | correct | sim: `virtuals` BD=16, sliced=-1; `vector_of_refs` does not compile |
| homework-5 | items[7#h5-say-move].model | The spoken answer on `std::move`, when a move happens, `noexcept` and growth, rules of zero and five; 1,000 buffers of 1,000 doubles are 8 MB | correct | as l19 and l20 (the model says "if the move can throw, every element is copied", true for the copyable `Buffer` it names) |
| homework-5 | items[8#h5-say-virtual].model | Dispatch path; delete through a base with a non-virtual destructor is undefined; the fix costs 4 bytes an object here; undefined behaviour and the optimiser; sanitisers | correct | as l21 and l22 |
| homework-5 | items[9#h5-sole-and-counted] | `SolePtr` and `CountedPtr` to the stated specification; an assignment takes its source before it lets go; `CountedPtr(SolePtr&&)` takes the object with `release()` | correct | sim: base run; `x.h5i9.sole_assign_deletes_first` → test 6, `counted_from_sole_no_release` → test 14 |
