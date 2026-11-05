# Answer check: cpp level 5 (l19 to l23, review-5, homework-5), 2026-11-05

Scope: `app/content/courses/cpp/` l19-moving-not-copying, l20-rule-of-five, l21-virtual-dispatch, l22-undefined-behaviour, l23-own-smart-pointer, review-5, homework-5. Branch merged from `origin/claude/amazing-wright-d4mx7i` (already up to date). Nothing edited except this report.

## Result

**No mismatch.** Every keyed answer was derived from the question text alone and agrees with the key, its explanation, its `wrong[]` feedback and the prose figures.

Widgets checked: **96** (8 code, 45 choice, 19 numeric, 6 multi, 6 table, 5 order, 4 tap-regions, 2 longform, 1 place). By file: l19 15, l20 14, l21 15, l22 15, l23 14, review-5 10, homework-5 13 (the two `parts` items count 3 widgets each). Longform rubrics sum to 10 points each (two items).

## Mismatch table

| file | path | stated | my result | method |
|---|---|---|---|---|
| (none) | | | | |

## Method

- C++ snippets: scratch programs compiled with `clang++ -std=c++17 -O1 -fno-exceptions` (clang 18, libstdc++), `g++ -std=c++17 -O1 -fno-exceptions` (libstdc++), and the app toolchain (YoWASP clang 21, libc++, debug hardening, wasm32, c++17) through `docs/briefs/cpp-scripts/app_toolchain/` runners. All three agreed on every count, trait and print; they differ only in pointer width (sizes), as the lessons say.
- Compile-error claims by `static_assert` on the type traits plus a direct compile of the failing line.
- UB claims: reproduced where a tool shows it (g++ `-fsanitize=undefined`, g++ `-fsanitize=address`, `_GLIBCXX_DEBUG`, libc++ hardening) and cited to the standard below.
- Numeric widgets: `parseNum` and `within` from `app/js/engine/grade.js` run on the typed forms (`4,294,967,295`, `£21,474,836.47`, `1,000,000`, `2,500,000,000`). All parse to the key; the pounds tolerance (abs 0.005) accepts 21474836.47 and rejects 21474836.5.
- Code widgets: the app's own `unit()` builder (prelude, postlude, `leakCheck`, `allocCheck`, `compiles` probes), each test in its own WASI process, c++17 and c++20.

## Facts confirmed (stated = result)

| Claim | Result | Rule or note |
|---|---|---|
| l19 s0: lines 2, 5, 8 copy; 3, 6 move; 4, 7 neither | 1 copy, 1 move, 0 on 4 and 7, 1 copy on 5 and 8 | C++17 guaranteed elision, [dcl.init]/17.6.1 |
| l19 s3: 4 pushes, noexcept move, capacity 1, 2, 4, 8: 0 copies, 7 moves | 0 / 7 | growth 1, 2, 4, 8, 16, 32 in libstdc++ and libc++ |
| l19 s4: throwing move, 2 pushes: 1 copy, 2 moves | 1 / 2 (4 pushes: 3 / 4) | `std::move_if_noexcept`, [vector.modifiers] |
| l19 s6 and quiz 3: `std::move` of a `const Order` runs the copy constructor | 1 copy, 0 moves | `const Order&&` binds to `const Order&` |
| l19 s9: `set_prices` copies 1,000,000 / 0 / 0 doubles | 1 allocation, 0, 0 | counting `operator new` |
| l19 quiz 4: `return std::move(t)` runs 1 move, `return t` 0 | 1 / 0 | all three toolchains |
| l19 s1: 8 bytes here, 16 on a desktop for `int` + `double*` | 8 / 16 | wasm32 against LP64 layout |
| l20 s1, homework item 4: the full special-member table (7 rows x 4 operations) | identical in clang and g++ | each cell compiled and run separately with a counting member |
| l20 s0: only `Fill b = std::move(a);` compiles | traits agree | move ctor declared deletes copies, no move assign: [class.copy.ctor]/7, [class.copy.assign]/2 |
| l20 s2: A move, B copy, C copy, D move | agree | |
| l20 s3: `Pos` noexcept, `Pos3` not | agree | `static_assert` on `is_nothrow_move_constructible_v` |
| l20 s6, s8, review item 2: destructor stops the move; `Order` with `unique_ptr` and `~Order(){}` rejects the move line | copy of all fills; "call to implicitly-deleted copy constructor" | deleted functions take part in overload resolution, [dcl.fct.def.delete]/2 |
| l21 sizes: VTick 8 (16), D 12 (16), Quote 24 (24), W 8 (16), B 16 (16), Q 24, empty virtual base 4 | all match in wasm32; desktop figures match x86-64 | |
| l21 s4, homework part 2, quiz 3: slicing gives `Payoff`'s version (-1 in my test) | `q.value` and `vector<Payoff>[0].value` return the base result, the reference returns the derived | |
| l21 s7: virtual call in a base constructor reaches `Base::name` | "Base" | well defined, [class.cdtor]/4 |
| l21 s6, review item 5: `delete` through `Base*` with non-virtual destructor | `~Derived` never runs (only `~Base` printed in all three); g++ ASan: new-delete-type-mismatch | UB, [expr.delete]/3; `shared_ptr<Base>` from `make_shared<Derived>` or `new Derived` runs both; `unique_ptr<Base>` does not |
| l22 s0: wasm output for `first(int*)` has no null test | app clang 21 `-O1 -S`: `local.get 0`, `i32.load 0` | read before test lets the compiler assume non-null |
| l22 s1, review item 6, homework item 5: lines 4, 6, 8 undefined; line 3 defined | UBSan reports index, null, overflow, shift, negation; unsigned wrap defined | see rules below |
| l22 s2: nine snippets sorted | defined: `UINT_MAX + 1u` is 0, `-7 / 2` is -3; implementation-defined: `sizeof(long)`, char signedness; unspecified: argument order; UB: the other four | see rules below |
| l22 s3 report texts | match g++ UBSan wording (`signed integer overflow`, `index 3 out of bounds for type 'int [3]'`, `load of null pointer of type 'volatile int'`) | |
| l22 s6: `v.size() - 1` is 4,294,967,295 here, 18,446,744,073,709,551,615 on a desktop | agree | `size_t` is 4 bytes in wasm32 |
| l22 s8: `<=` comparator makes `std::sort` undefined | 100 equal elements: g++ reads out of bounds (`v[0]` came back 0, not 7); `_GLIBCXX_DEBUG` aborts; app libc++ hardening aborts "does your comparator satisfy the strict-weak ordering requirement?" | Compare requirement [alg.sorting]/3, violating it is UB |
| l22 s10, quiz 2: INT_MAX pence = £21,474,836.47; `unsigned` max = £42,949,672.95; 5,000 x £5,000 = 2,500,000,000 pence | agree | computed in two ways |
| l22 s1 app note: libc++ hardening stops `v[3]`, not null read or overflow | app run: assertion trap for the index; null read and overflow run to "done" | |
| l23 s0, s1, s9, quiz 1, 2: allocations and counts | `shared_ptr(new T)` 2, `make_shared` 1, six steps 2, `use_count` 3 inside and 2 after, 200,000 x 50 ns = 10 ms | |
| l23 s3: `unique_ptr` one pointer, `shared_ptr` two (4 and 8 here) | agree | |
| l23 quiz 3: `release()` keeps the object, `reset()` deletes | live count 2 to 1 on `reset` | |
| homework item 5: iterator invalidation, `-INT_MIN`, `buf[4]`, double delete undefined; `1u << 31` and `7 / 2` defined | ASan heap-use-after-free on the range-for; UBSan negation report | [vector.modifiers], [expr.pre]/4, [expr.add]/4, [expr.delete]/2 |
| homework item 6: `sizeof(B)` 16 with a `double` after a vptr | 16 | 4 + 4 padding + 8 |
| review item 6: `v.at(5)` is defined | native throws `std::out_of_range`; app's `__cxa_throw` stub exits 134 | defined, [vector.capacity] |

Rules for the UB, unspecified and implementation-defined calls (C++17 numbering, same text in C++20):
signed overflow [expr]/4 (UB); index one past the end [expr.add]/4 (UB); unset read [dcl.init]/12 (UB); shift by the width [expr.shift]/1 (UB); unsigned wrap [basic.fundamental]/4 (defined); division towards zero [expr.mul]/4 (defined); `sizeof(long)` and plain `char` signedness [basic.fundamental] (implementation-defined); order of argument evaluation [expr.call]/8 (unspecified); `delete` through a base without a virtual destructor [expr.delete]/3 (UB); double `delete` [expr.delete]/2 and [new.delete.single] (UB); comparator that is not a strict weak ordering [alg.sorting]/3 (UB); iterator use after reallocation [vector.modifiers]/1 (UB); moved-from standard objects [lib.types.movedfrom] (valid, unspecified).

## Code widgets (hidden tests in the app toolchain)

All eight: model solution passes every hidden test (c++17 and c++20), starter fails, and my own wrong solutions are caught.

| Widget | Solution | Starter fails | My wrong solutions (tests failing) |
|---|---|---|---|
| l19 s5 `Buffer` moves | 0 of 15 | 9 | move assignment without self-check 1; move ctor leaves source 7; moves not `noexcept` 2 |
| l20 s5 `Samples` copies | 0 of 13 | 11 | shallow copy ctor 6; delete-first assignment with no guard 1 (`a = a`) |
| l21 s5 hand-made vtable | 0 of 11 | 6 | `value_of` always calls `call_value` 3; `make_put` uses the call table 4 |
| l22 s4 `add_overflows` | 0 of 13 | 7 | one-sided check 3; `>=` off by one 1; add-then-compare 7 |
| l23 s2 `UniquePtr` | 0 of 15 (+2 compile checks) | 14 | copied pointer in move ctor 3; no self-move guard 1; `reset` leaks 2; `release` keeps pointer 2 |
| l23 s5 `SharedPtr` | 0 of 15 | 14 | drop-then-add assignment 1; copy ctor never increments 5; counter never freed 13 |
| homework 0 `ScopeGuard` | 0 of 12 (+2 compile checks) | 8 | move ctor leaves source active 3; defined copy ctor 1 (compile check); defined move assignment 1 (compile check); move not `noexcept` 1 |
| homework 1 `Vec<T>` | 0 of 15 | 11 | grow before building argument 1 (`bad`); always copy on growth 1; capacity +1 3; destroy-first assignment 1 |

## Notes

1. **Test gap, l23 s5 `SharedPtr`.** A move assignment that takes the pointers but does not null the source passes all 15 tests (0 failed). Only the move constructor has a source check (`a.use_count()` after `b = std::move(a)`); the assignment tests read `b` only, and the source's later `--*count_` hits the poisoned freed counter without deleting again. One more test, `b = std::move(a)` then `a.use_count()` expecting 0, would catch it. Homework item 3 (order) does teach "empty the source", so the key is right; only the grader is loose.
2. **l23 s0 slip value.** The numeric `wrong` value 3 carries "You counted a new counter for each copy". A new counter per pointer (object plus three counters) would be 4, not 3. The feedback fires on 3 either way, so nothing is graded wrongly, but the explanation of the slip does not add up. Frame 5 ("b ends") of the same canvas also labels the object "Tracked(1) new", copied from frame 1, while the question counts `new`.
3. **Equivalent mutants.** In homework 0, deleting `ScopeGuard(const ScopeGuard&) = delete;` or the deleted move assignment changes nothing (0 of 12 fail), because the declared move constructor already deletes the copy members. That is the lesson's own rule, not a test gap; real copy and assignment definitions are caught by the compile checks. Likewise l20 s5 delete-first assignment with the `this != &other` guard is safe on `a = a`, so it passes.
4. **Alternative solutions accepted.** l22 s4 accepts a `long long` widening check (0 of 13 fail). It never overflows, so it is correct, though the prose says "so the addition never happens". l20 s5 accepts allocate-then-copy-then-free with no guard.
5. **Homework item 4 accepts exact words only.** Cells take `copy`, `move`, `error` (case-insensitive). l20 s2 also accepts `copies`, `moves`, `mv`; homework item 4 has no `accept` lists, so `copies` is marked wrong there. The prompt names the three words, so this is consistency only.
6. **C++26.** Reading an uninitialised automatic variable (l22 s1 line 6, s2 `int x; return x;`, review item 6, quiz 3) is undefined in C++17 and C++20, which the lesson says it uses. C++26 (P2795R5) makes it erroneous behaviour. No change needed while the toolchain stays at c++17 or c++20.
7. **Platform wording.** "`sizeof(long)` is 8 on a desktop" holds for Linux and macOS (LP64); on Windows it is 4. Fine for the intended reader.
8. **Homework item 7 model answer.** "Each growth copies 8 MB" is true only for growths made when the vector already holds 1,000 `Buffer`s of 1,000 doubles; earlier growths copy less. Round and acceptable as a spoken figure.
9. **Homework item 2 part 3.** The key "by value, then move" is the best of the four options, but the explanation says two overloads are faster. The overloads are not offered, so the key stands.
10. **Pointer widths.** Every size claim is stated for wasm32 with the desktop figure beside it; none disagrees with the app toolchain (4-byte pointers) or with x86-64 (8-byte).

## Recheck

Merged origin/claude/amazing-wright-d4mx7i (fix pass ecb7f19, cd1452d). Checked independently: my own runner built from the content JSON (not the problems_*.py), the app's own `unit()` and the app's real flags (`-std=c++17 -O1 -D_LIBCPP_HARDENING_MODE=DEBUG`, no `-fno-exceptions`), plus native g++ 13 and clang++ (libstdc++).

### Widgets

- Code items (l19 to l23, homework-5, exam 23, 26, 28): every solution passes all hidden tests and every starter fails (l19 9/15, l20 11/13, l21 6/11, l22 7/13, l23 SharedPtr 14/15, homework 8/12 and 11/15, clone-basket 10/12). The exam items that use `raises` and list compare (17, 24, 27) show spurious failures only because my runner does not model those compare modes; they are unchanged by the fix.
- New SharedPtr tests (l23 screen 5), five wrong move assignments (no drop of the old share, source count not cleared, move that adds a count, move written as a copy, no drop before taking): each fails 2 of 15. The `b = a; b = std::move(a)` test (expect 10) and the `live*100 + b*10 + a` test (expect 110) catch them.
- New clone-basket test (`c = b.clone(); b.cost(2.0)` expect 500): a clone that steals the source children via `const_cast` fails exactly that test. Empty clone, sliced Limit clone and Market-for-everything clone fail 2 to 3 tests.
- Facts, all as keyed, same in the app, g++ and clang++ unless noted: review-5 item 1 (`take` with const: 2 copies, 0 moves); item 2 (noexcept and reserve stop copies; `emplace_back` does not); item 5 (sizeof is 8 here, 16 on a desktop); item 8 (`use_count` 2; 352,516,353 pence); item 9 (order); item 10 (`shared_ptr(a.get())`: counts 1 and 1, two destructor runs in the app, ASan double-free natively); l23 s0 (4 and 3 slips match their text); l23 s7 and quiz (`b.use_count()` is 1 after a move-assign; `weak_ptr` leaves `use_count` at 2); l22 s5 (null read: the app prints v = 0 and runs on; g++ segfaults; clang++ -O1 reads garbage and exits 0); l21 s2 and s3 (12, 24); Order with a user destructor (default compiles; move, copy and move-assign all fail with a deleted copy).
- Homework members table: all 12 cells match g++, clang++ and the app (row 1 copy, error, move; row 2 move, error, error; row 3 copy x3 and row 0 copy x3). Slip texts agree with each cell.
- No mismatch found in key, accept list, slip or stated fact.

### Vector growth (l19 and e-vector-growth)

Verdict: correct. With the app's real flags a `Tracked` whose move is `noexcept(false)` gives 1 copy and 2 moves for two pushes and 3 copies and 4 moves for four. A `noexcept` move gives 0 and 7 in the app, g++ and clang++. g++ and clang++ with libstdc++ give 3 and 4 even with `-fno-exceptions`. libc++ in the app with `-fno-exceptions` added gives 0 copies and 7 moves, which confirms the fixer's dispute of the reviewer's 0 and 7. The text names `std::move_if_noexcept` and the strong guarantee correctly.

One minor flag: the added sentence "a build with exceptions off, such as libc++ with `-fno-exceptions`, moves anyway" (l19 screen 4 explain, exam e-vector-growth explain) is true but a learner cannot observe it: the app has no flag control and never passes `-fno-exceptions`. It is also library-specific (libstdc++ still copies). Optional: drop it or label it as a desktop note.

### Old values

Grepped the cpp folder, exam and manifest for `q-copy-unique`, `q-use-count`, `r5-use-count`, `r5-int-max-pounds`, "Add before you drop", "What value is y", and the old l19 `set_prices` setter: none remains in the files the diff changed. `set_prices` still appears in homework-5 h5-sink, which the diff did not touch (a different item, still correct).

### Layout

`playthrough --lesson cpp/l21-virtual-dispatch --exam topic-1.9 --mobile --tablet`: l21 15 checks ok, exam 30 of 30 passed. l21 screens 7 and 9 at 440, 1032 and 1376: no clipped code (both `return` bodies wrapped). Clone-basket starter (exam item 27): clean at 1032 and 1376. At 440 the editor still cuts the right end of lines 4, 8, 9, 14, 15, 17 and 18 (the first columns show; the editor scrolls sideways). The starter comments were shortened but the signatures are longer than 440 allows. Minor: wrap them as the fixer did for the other items, or accept editor scrolling.

### Voice

`voice-scan.py --summary` on the cpp folder: 0 explanations over three sentences, 0 sentences over 20 words (10,403 scanned). A scratch copy of topic-1.9.json: 0 and 0 (639 scanned).
