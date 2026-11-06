# Claim ledger: systems level 4 (blind concept audit)

Files: `app/content/courses/systems/l15-no-allocation.json`, `l16-ring-buffer.json`, `l17-measuring-latency.json`, `l18-feed-handler.json`, `review-4.json`, `homework-4.json`. Script: `docs/reports/systems-L4-concepts.py` (`sim:` rows name its check by the ledger row named in the check's message). Sources are cited as `N4659 [section]` (C++17 working draft), Williams (*C++ Concurrency in Action*, 2nd ed.), Drepper (*What Every Programmer Should Know About Memory*, 2007), Tene (*How NOT to Measure Latency*, Strange Loop 2015), Knuth (TAOCP vol. 1), Hyndman and Fan (1996), Agner Fog (instruction tables), Paoloni (Intel white paper 324264, 2010). Verdicts: correct, wrong, imprecise, misleading, unverified.

## l15-no-allocation

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l15 | objectives[0] | A hot path can be made allocation-free with a pool allocator | correct | Knuth TAOCP 1 §2.2.3 (available-space list); sim: l15 screens[9] Pool |
| l15 | screens[0].prose | An allocation asks the heap for memory; a 100-char string does not fit inside `std::string` | correct | libstdc++ `_S_local_capacity` = 15, libc++ 22 (64-bit); sim: l15 screens[0] prose SSO |
| l15 | screens[0].widget.answer | Lines 3 (first `push_back`), 4 (`new`), 5 (`std::string(100)`), 6 (`std::map` insert) allocate; 2 and 7 do not | correct | N4659 [vector.capacity] (no storage until needed), [associative.reqmts] node-based; sim: l15 screens[0] widget.answer |
| l15 | screens[0].hints[0].text | An allocation happens when a container grows or `new` runs | correct | N4659 [expr.new]/10, [vector.modifiers] reallocation; sim as above |
| l15 | screens[0].hints[1].text, feedback.byKey.l2, explain.text | A default-constructed vector owns no memory until the first push | correct | libstdc++/libc++ default ctor noexcept and allocate nothing; sim: l15 screens[6] trap |
| l15 | screens[0].feedback.byKey.l7 | Arithmetic on locals lives in registers and the stack | correct | no `operator new` involved; sim: line 7 counts 0 |
| l15 | screens[0].hints[2].text, explain.text | Line 6 allocates a map node | correct | N4659 [associative.reqmts]/9 (node handles, nodes are allocated); sim counts 1 |
| l15 | screens[1].prose | A `malloc` or `new` costs about 50 ns (stated assumption) | correct | stated as an assumption; glibc malloc fast path is tens of ns (Drepper §7 and glibc malloc docs); not graded as fact |
| l15 | screens[1].widget.accept, explain.text | 50 ns × 200,000 a second = 10 ms a second, each extra allocation adds the same | correct | derivation: 50 × 2e5 = 1e7 ns = 10 ms |
| l15 | screens[1].feedback.byKey.us, .ns | 10,000 is the microsecond figure; 50 ns is one call | correct | unit conversion |
| l15 | screens[2].prose | Now and then an allocation asks the system for more memory, which takes microseconds | correct | glibc malloc grows the arena with `brk`/`mmap` (M_MMAP_THRESHOLD) and the first touch page-faults; a syscall plus page fault is microseconds (Drepper §7.3, §4) |
| l15 | screens[2].explain.text | 200 ns a message, 40 ms a second, 4% of a core; the rare slow allocation hides inside the average | correct | derivation 4 × 50 = 200, × 2e5 = 4e7 ns; a mean hides a tail (Tene) |
| l15 | screens[3].prose | A pool keeps slots in a fixed array with a free list threaded through free slots; `allocate` takes the head, `release` pushes at the head | correct | Knuth TAOCP 1 §2.2.3 (AVAIL stack); Bonwick (1994) slab free lists |
| l15 | screens[3].canvas, widget.answer | After two allocations and release(0): cells [2, used, 3, end], next allocate returns 0 | correct | sim: l15 screens[3] |
| l15 | screens[3].hints[0].text | `allocate` always takes the head of the free list | correct | LIFO free list by construction (the pool contract of screens[9]) |
| l15 | screens[3].feedback.byKey.c2, .c1, .c3 | Slot 2 follows 0; slot 1 is in use; slot 3 is the end | correct | sim: l15 screens[3] |
| l15 | screens[3].explain.text | Releasing 0 made it the head pointing at 2; allocate pops it; both calls touch no heap | correct | sim: l15 screens[9] Pool (alloc_count 0 over 100 rounds) |
| l15 | screens[4].prose | A pool allocation takes 2 ns against 50 ns for `malloc` (stated assumption) | correct | assumption; a free-list pop is a few instructions (L1 hit about 1 ns, l1-latency-numbers) |
| l15 | screens[4].explain.text | 600,000 calls a second: 30 ms versus 1.2 ms, 25 times cheaper | correct | derivation |
| l15 | screens[4].explain.text | "its cost never varies" | imprecise | a free-list pop has no system-call slow path, but its latency still varies with the cache state of the slot (an L1 hit is about 1 ns, a DRAM miss about 100 ns: Drepper §3.3, l1-latency-numbers); "never varies" overstates a bounded cost as a constant one |
| l15 | screens[5].prose | A test can prove a hot path never allocates by counting every `new` | correct | replaceable global `operator new`, N4659 [new.delete.single]/1; cpp-grade.js ALLOC_CNT; sim: ALLOC harness |
| l15 | screens[5].widget.solution | Stack `char tmp[24]`, sign, pounds digits, dot, two pence digits; all tests pass, no allocation | correct | sim: l15 screens[5] format_price (c++17, c++20) |
| l15 | screens[5].widget.starter | The starter builds digits in a `std::vector<char>` and fails the tests | correct | sim: starter fails; starter alloc_count > 0 |
| l15 | screens[5].widget.how | The first Check downloads the compiler, about 26 MB, 10 to 15 s | unverified | engine behaviour, not a concept; outside this audit |
| l15 | screens[5].hints[0..2].text | Digits can be built in a stack array; peel with `% 10` and `/ 10`; pad pence below 10 | correct | the solution does this; sim passes tests 1, 6 (5 and -5) |
| l15 | screens[5].explain.text | `char tmp[24]` on the stack never calls `new`; the `alloc_count()` test would fail with the starter | correct | sim: starter alloc_count > 0 at -O1 -fno-builtin (the app's flags); solution count 0 |
| l15 | screens[6].prose | A colleague says every container allocates when declared (the trap) | correct as a trap | resolved below |
| l15 | screens[6].widget.options[0] | The first `v.push_back(1)` allocates | correct | sim: l15 screens[6] trap |
| l15 | screens[6].widget.options[1].why, feedback.byKey.decl | A default vector owns no memory yet; it allocates on the first push | correct | libstdc++ `_Vector_base` default ctor sets null pointers; sim |
| l15 | screens[6].widget.options[2].why, options[3].why | `std::array<int, 8>` and `int b[8]` carry their storage inside the object, no heap call | correct | N4659 [array.overview]/2 (aggregate holding `T[N]`); sim counts 0 |
| l15 | screens[6].explain.text | To avoid the cost, call `reserve` before the first message | correct | N4659 [vector.capacity]/6 (no reallocation after `reserve` until size would exceed capacity) |
| l15 | screens[7].prose | On the hot path the pool may not grow; a slot released twice would corrupt the free list | correct | pushing one slot twice makes the list point at itself (Knuth §2.2.3 exercise on AVAIL corruption) |
| l15 | screens[7].widget.options[0] | A full pool returns -1 and lets the caller decide | correct | design convention stated by the contract; matches screens[9] tests[2], [8] |
| l15 | screens[7].widget.options[1].why, feedback.byKey.grow | Growing allocates on the hot path | correct | by definition |
| l15 | screens[7].widget.options[2].why, feedback.byKey.wait | The one hot thread is the only one that releases, so waiting would deadlock | correct (single-thread hypothesis stated in the why) | the lesson's handler is one thread; with a second releasing thread waiting is a design choice |
| l15 | screens[7].widget.options[3].why, feedback.byKey.reuse | Handing one slot to two users corrupts both | correct | aliasing |
| l15 | screens[7].explain.text | Size the pool for the worst case; a debug build asserts on a double release | correct | standard practice (Bonwick 1994 §4, debug free-list checks) |
| l15 | screens[8].prose | Allocate everything before the first message, then prove it with a count | correct | the lesson's method; sim: alloc harness |
| l15 | screens[8].widget.options[1].why, feedback.byKey.fast | A fast `new` is still a call that can reach the system | correct | glibc malloc may `brk`/`mmap` on any call that finds no free chunk (Drepper §7) |
| l15 | screens[8].widget.options[2].why, feedback.byKey.stack | The stack is one source; a pool covers objects that outlive a call | correct | automatic storage duration ends with the block, N4659 [basic.stc.auto] |
| l15 | screens[8].explain.text | Take the memory once; after that every call pops or pushes a slot; the count test proves it | correct | sim: l15 screens[9] Pool tests[9] |
| l15 | screens[9].prose | `allocate` returns the most recently released slot, or -1 when none is free | correct | LIFO free list; sim |
| l15 | screens[9].widget.solution | Free list threaded through `next_free_`, head pop and push, `in_use_` count; no allocation after the constructor | correct | sim: l15 screens[9] Pool (c++17, c++20), all 10 tests |
| l15 | screens[9].widget.starter | `next_++` never reuses a slot and never reports full, so it fails | correct | sim: starter fails tests 2, 3, 4, 5, 8 |
| l15 | screens[9].hints[1..2].text | Build the list so slot s points at s + 1, head 0; allocate pops, release pushes | correct | matches the solution; sim |
| l15 | screens[9].explain.text | Last released is reused first; all of it is index arithmetic on reserved memory | correct | sim: alloc_count 0 over 100 rounds |
| l15 | screens[10].widget.rows | Sequences give 1, 2, -1 and 1 | correct | sim: l15 screens[10] rows 1 to 4 |
| l15 | screens[10].hints[1].text, feedback.byKey.r1c1, explain.text | Release 0 then 2 makes 2 the head with 0 after it; the free list is a stack | correct | sim: l15 screens[10] row 2 |
| l15 | screens[10].feedback.byKey.r3c1, hints[2].text | Released 3, 1, 2 means head order 2, 1, 3 | correct | sim: row 4 |
| l15 | screens[11].prose | An order is 24 bytes in the level 1 layout or 32 with padding; L1 data is 32 KiB | correct | l4-object-layout (24-byte struct, padded to 32); 32 KiB L1d is the common size (Intel Skylake to Comet Lake; 48 KiB from Ice Lake, so "a core's L1" is a typical figure) |
| l15 | screens[11].explain.text | 36,000 bytes is about 35 KiB, 48,000 about 47 KiB, neither fits a 32 KiB L1; the tighter layout is 25% smaller | correct | 36,000 / 1,024 = 35.2; 48,000 / 1,024 = 46.9; 1 − 24/32 = 0.25 |
| l15 | summary.ideas[0..2], summary.formula | cost = n_alloc × t_alloc × rate; pool semantics; allocate first, count after | correct | derivations above |
| l15 | summary.trap | Thinking an empty container allocates when declared | correct | sim: l15 screens[6] trap |
| l15 | quiz[0] | 5 × 50 ns × 150,000 = 37.5 ms | correct | derivation |
| l15 | quiz[1].widget.options[0], explain.text | After `reserve(1000)`, pushing 500 and `clear` each message allocates nothing; `clear` keeps the capacity | correct | N4659 [vector.capacity]/6 guarantee holds until an insertion would exceed `capacity()`, and `clear()` is not an insertion; capacity shrinks only by `shrink_to_fit` or swap/move ([vector.capacity]/9); sim: l15 quiz[1] (0 allocations over 50 messages) |
| l15 | quiz[1].widget.options[1].why, options[2].why, options[3].why | A push allocates only past the capacity; `clear` keeps the capacity; `reserve` did the work | correct | as above |
| l15 | quiz[2] | Release 3 then 0: allocate returns 0 | correct | sim: l15 quiz[2] |
| l15 | quiz[3] | 800 × 1.5 = 1,200 slots × 20 = 24,000 bytes | correct | derivation |
