# Claim ledger: systems L4, concept audit round 2 (blind)

Scope: `l15-no-allocation`, `l16-ring-buffer`, `l17-measuring-latency`, `l18-feed-handler`, `review-4`, `homework-4`. Written before any earlier review, answer check, audit or report of this level was opened. `sim:` names a check in `docs/reports/systems-L4-concepts-r2.py` (exit 0 on this content). Standard clauses are C++17 (N4659) unless said. Williams is *C++ Concurrency in Action*, 2nd ed. Tene is Gil Tene, "How NOT to Measure Latency" (Strange Loop 2015) and the HdrHistogram README.

## l15-no-allocation

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l15 | screens[0].prose | An allocation asks the heap for memory; a 100-char string does not fit inside the string object | correct | libstdc++ SSO holds 15 chars, libc++ 22; `sim: l15-alloc t4, t15` (string(100) allocates, string(15) does not) |
| l15 | screens[0].widget.answer | Lines 3, 4, 5, 6 allocate; 1, 2, 7, 8 do not | correct | `sim: l15-alloc t1 to t7, t14` with an overloaded `operator new` under g++ 13, -O1, c++17 and c++20 |
| l15 | screens[0].hints[1] | A vector that has never held anything owns no memory yet | correct | [vector.cons] default ctor is `noexcept`; `sim: l15-alloc t1` |
| l15 | screens[0].feedback.byKey.l7 | Arithmetic on locals lives in registers and on the stack | correct | no `new` reachable; `sim: l15-alloc t6` |
| l15 | screens[0].explain | Four allocations a message: first push, `new`, 100-char string, map node | correct | `sim: l15-alloc t7` counts 4 |
| l15 | screens[1].prose | 200,000 a second is one every 5 µs | correct | 1/200,000 s = 5 µs; `sim: l15-s1` |
| l15 | screens[1].widget | Each allocation a message adds 10 ms a second (50 ns × 200,000) | correct | model stated on screen; `sim: l15-s1` |
| l15 | screens[1].derive.caption | n allocations: n × 10 ms of every second | correct | linear in n under the stated model |
| l15 | screens[2].prose | Now and then an allocation asks the system for more memory, which takes microseconds | correct | glibc malloc grows the arena with `brk`/`mmap` (a system call) when free chunks run out; glibc manual 3.2.3 |
| l15 | screens[2].widget | 200 ns, 40 ms, 4% of a core | correct | `sim: l15-s2` |
| l15 | screens[2].explain | The rare slow allocation hides inside the 50 ns average | correct | the 50 ns is a mean per call by the screen's model; a mean hides the tail (l17) |
| l15 | screens[3].prose, canvas | Free list threaded through free slots, LIFO; after two allocations and release 0 the cells read 2, used, 3, end | correct | `sim: l15-s3` free-list model |
| l15 | screens[3].widget | Next allocate returns slot 0 | correct | `sim: l15-s3` |
| l15 | screens[3].explain | Both calls are a few instructions and touch no heap | correct | pop and push are two index assignments on the preallocated array (screen 9 solution) |
| l15 | screens[4].widget | 30 ms, 1.2 ms, 25 times | correct | `sim: l15-s4` |
| l15 | screens[4].explain | The pool has no slow path: no system call can hide inside a pop | correct | the pool's memory is taken in the constructor; pop is index arithmetic (screen 9) |
| l15 | screens[5].prose | `alloc_count()` counts every `new`; the tests reset it first | correct | AUTHORING 3, `allocCheck`: global `operator new`/`new[]` replaced and counted |
| l15 | screens[5].widget.solution | Model solution formats every test and makes 0 allocations; the starter allocates (vector growth) | correct | `sim: check_code_item l15-format-price` (solution passes 10/10 under c++17 and c++20; starter fails t10 the count test) |
| l15 | screens[5].explain | A `char tmp[24]` lives on the stack, so building digits there never calls `new` | correct | [basic.stc.auto]; `sim: l15-format-price` count 0 |
| l15 | screens[6].widget | Only the first `push_back` allocates; `std::vector<int> v;`, `std::array<int, 8>`, `int b[8]` do not | correct | `sim: l15-alloc t1, t2, t8, t9` |
| l15 | screens[6].options.array.why | The eight ints are part of the `std::array` object, on the stack here | correct | [array.overview]: aggregate holding `T[N]` |
| l15 | screens[6].explain | Call `reserve` before the first message to avoid the cost | correct | [vector.capacity]/6: no reallocation on insertion after `reserve` until size would exceed capacity |
| l15 | screens[7].widget | A full pool returns -1 and lets the caller decide | correct | design rule consistent with the hot-path contract; `sim: l15-s7` |
| l15 | screens[7].options.wait.why | The one hot thread is the only one that releases, so it would wait for itself | correct | the handler of screen 0 runs on one thread; a blocking wait on the hot path also breaks the budget (l18 screen 2) |
| l15 | screens[7].options.reuse.why | Handing the oldest slot out again makes two users share one slot | correct | by the pool contract (one owner per slot) |
| l15 | screens[7].explain | A slot released twice would link into the free list twice, so a debug build asserts | correct | release pushes `slot` at the head; a second push of a live slot makes a cycle; standard pool practice (e.g. Boost.Pool docs on double free) |
| l15 | screens[8].prose, code | Allocate everything before the first message, then prove it with a count | correct | the standard low-latency pattern (CppCon 2017, Carl Cook, "When a Microsecond Is an Eternity", §allocation) |
| l15 | screens[8].options.fast.why | A fast `new` is still a call that can reach the system | correct | glibc malloc fast bins still fall back to `sysmalloc` when empty (glibc malloc.c) |
| l15 | screens[8].options.stack.why | The stack is one source; a pool covers objects that outlive a call | correct | [basic.stc.auto] lifetime ends at block exit |
| l15 | screens[9].widget.solution | Pool solution: allocate pops the head, release pushes, full returns -1, 0 allocations after the constructor; the starter fails | correct | `sim: check_code_item l15-pool` (solution 10/10 under c++17 and c++20; starter fails t3, t4 and others) |
| l15 | screens[9].widget.how | "The last runs 100 allocate and release rounds, which must add 0 to `alloc_count()`" | correct | `sim: l15-pool` t10; note the starter also passes t10 (it never allocates), it fails on reuse |
| l15 | screens[9].hints[2], explain | allocate returns `head_` and moves it to that slot's next; release points the slot at `head_` then makes it the head; last released is reused first | correct | LIFO free list; `sim: l15-s3` model and the solution's tests |
| l15 | screens[10].widget | Drill answers 1, 2, -1, 1 | correct | `sim: l15-drill rows 1 to 4` |
| l15 | screens[10].explain | Each release pushes at the head, so the free list is a stack | correct | by construction (screen 9 solution) |
| l15 | screens[11].prose | An order is 24 bytes in the layout of level 1, or 32 bytes with padding | correct | l4-object-layout: 24-byte struct, padded to 32 so two fit a line |
| l15 | screens[11].widget | 1,500 slots, 36,000 and 48,000 bytes, 25% saving | correct | `sim: l15-transfer` |
| l15 | screens[11].explain | 36,000 is about 35 KiB and 48,000 about 47 KiB; neither fits a 32 KiB L1 | correct | `sim: l15-transfer explain` |
| l15 | summary.ideas, formula | cost = n_alloc × t_alloc × rate; 4 × 50 ns × 200,000 = 40 ms | correct | `sim: l15-s2` |
| l15 | summary.trap | Thinking an empty container allocates when declared | correct | `sim: l15-alloc t1, t14` (vector and map declarations count 0) |
| l15 | quiz[0] (q15-cost) | 37.5 ms | correct | `sim: q15-cost` |
| l15 | quiz[1] (q15-reserve) | After `reserve(1000)`, pushing 500 and clearing each message never allocates; `clear` keeps the capacity | correct | [vector.capacity]/6 (no reallocation after `reserve` until size would exceed capacity); [sequence.reqmts] `clear` erases only; `sim: l15-alloc t13` |
| l15 | quiz[1].options.every.why | A push allocates only when the size passes the capacity | correct | [vector.capacity]/6 |
| l15 | quiz[2] (q15-pool) | Slot 0 (released last) | correct | `sim: q15-pool` |
| l15 | quiz[3] (q15-size) | 24,000 bytes | correct | `sim: q15-size` |
