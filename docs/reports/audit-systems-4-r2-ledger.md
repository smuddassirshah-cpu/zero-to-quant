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

## l16-ring-buffer

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l16 | screens[0].prose, frames | Items come out at the head and go in at the tail; four slots take pushes 1 to 4, push 5 is refused, pops return 1, 2, 3, 4, then empty | correct | `sim: l16-s0` growing-counter ring model |
| l16 | screens[0].frames[4].pointers | After push 4 the tail counter is 4 and its slot is 0 | correct | 4 & 3 = 0 |
| l16 | screens[0].explain | Full is a tail four ahead of the head; empty is equal counters | correct | definition of the counter ring (screen 8 generalise); `sim: l16-s0` |
| l16 | screens[1].prose | The counters only ever grow; the slot is the counter reduced to the ring size | correct | design convention stated; slot = counter mod N |
| l16 | screens[1].widget | Slot 1, 7 items, slot 4 | correct | `sim: l16-s1` |
| l16 | screens[1].explain | counter mod N is `counter & (N - 1)` for a power of two; head 13 sits in slot 5, so slot 4 is just before it and one slot is free | correct | N = 2^k: low k bits are the remainder; `sim: l16-s1` (13 & 7 = 5, 20 & 7 = 4, 20 - 13 = 7 of 8) |
| l16 | screens[2].prose | An `unsigned` wraps to 0 after 4,294,967,295; `size_t` is 4 bytes in this app and 8 on a desktop | correct | [basic.fundamental]/2 unsigned arithmetic mod 2^n; wasm32 has 32-bit `size_t`, x86-64 64-bit |
| l16 | screens[2].canvas table | Across the wrap the slots run 2, 3, 0, 1 and tail - head stays 2 | correct | `sim: l16-s2 console` (mod 2^32 arithmetic) |
| l16 | screens[2].widget | 1; 0; 0; 429.5 s | correct | `sim: l16-s2 rows 1 to 4` |
| l16 | screens[2].hints[0], [1] | A power of two divides 2^32 evenly so the low bits carry on; 2^32 mod 3 = 1 so a ring of 3 breaks at the wrap | correct | 2^32 = 4 × 2^30; 2^32 ≡ (-1)^32 = 1 (mod 3); `sim: l16-s2` |
| l16 | screens[2].feedback.byKey.r1c1 | 4,294,967,295 = 3 × 1,431,655,765 | correct | arithmetic; `sim: l16-s2 rows` |
| l16 | screens[2].explain | A ring of 3 puts counters 4,294,967,295 and 0 in the same slot; at 10 million pushes a second the wrap comes after 429.5 s | correct | `sim: l16-s2 explain`; 2^32 / 10^7 = 429.5 |
| l16 | screens[3].prose | A cache line is 64 bytes; a core that writes a word takes the whole line from the other core | correct | MESI/MOESI write-invalidate: a store needs the line in Modified, invalidating other copies (Hennessy and Patterson, CA:AQA 6th ed., 5.2); 64-byte lines on x86 |
| l16 | screens[3].widget, explain | All eight words of the line move, `head` included; each store drags the other counter's word along: false sharing | correct | same source; Intel Optimization Reference Manual, "false sharing" |
| l16 | screens[4].widget | 600 ms a second against 10 ms (60 ns and 1 ns a push at 10^7 a second) | correct | model stated on screen; `sim: l16-s4` |
| l16 | screens[4].explain | 600 ms is 60% of a core; `alignas(64)` stops a store to one counter evicting the other; real rings cache the other counter and re-read it only when the ring looks full or empty | correct | `sim: l16-s4`; [dcl.align]; the cached-index SPSC design (folly `ProducerConsumerQueue`, rigtorp `SPSCQueue`) |
| l16 | screens[5].prose | A `release` store publishes everything written before it, and an `acquire` load sees it | imprecise | [atomics.order]/2: the acquire load must read the value the release store wrote (or a later one in its release sequence) to synchronize with it; as written any acquire load "sees it" |
| l16 | screens[5].widget.answer | push: load tail relaxed; return false if tail - head(acquire) == N; write slot; store tail release; return true | correct | Williams 2nd ed. 5.3.3 (release-acquire pairing) and 7.2; `sim: spsc-ok` (200,000 items in order, no TSan report) |
| l16 | screens[5].lines.d1.why | A relaxed tail store can become visible before the slot write, so the consumer could read a stale slot | correct | [intro.races]/21 and [atomics.order]: no happens-before from a relaxed store; `sim: spsc-l16-s5-d1` (TSan reports the slot access as a data race) |
| l16 | screens[5].lines.d2.why | Only the consumer writes `head_`; a second writer would race | correct | SPSC ownership; two unsynchronised writers of one atomic are not a data race in the standard sense but break the single-writer invariant the counter arithmetic relies on |
| l16 | screens[5].lines.d3.why | Each counter has one writer, so no lock is needed | correct | Williams 7.2 (lock-free SPSC queue) |
| l16 | screens[5].explain | The release store of tail + 1 publishes the slot write, so the consumer's acquire load of the tail sees it; a relaxed store would not order the two | correct | [atomics.order]/2, [intro.races]/9 to 12; `sim: spsc-ok`, `spsc-l16-s5-d1` |
| l16 | screens[6].widget | No mutex is needed: each counter has one writer | correct | Williams 7.2; `sim: spsc-ok` |
| l16 | screens[6].options.yes.why | The two threads write different slots; the counters hand each slot from one thread to the other | correct | release/acquire on the counters orders slot write before slot read and slot read before the next slot write |
| l16 | screens[6].options.vector.why | A vector is not thread safe | correct | [res.on.data.races]/3: concurrent modification of one object is a data race unless the library says otherwise |
| l16 | screens[6].explain | A data race is two threads touching one variable, at least one writing, with nothing ordering them | imprecise | [intro.races]/21 adds "at least one of which is not atomic"; as written, two unordered relaxed atomic accesses would be a data race, which they are not |
| l16 | screens[6].explain | Each counter is an atomic with one writer, and the release/acquire pair orders each slot write before the other thread reads it | correct | Williams 5.3.3; `sim: spsc-ok` |
| l16 | screens[7].widget, explain | head 7, tail 11, ring of 4: 4 items, both slots 3; wrapped indexes would make full look like empty, so a counter ring of N holds N items | correct | `sim: l16-full-ring`; the classic N-1 limitation of index-only rings (Knuth TAOCP vol. 1, 2.2.2 exercise on circular queues) |
| l16 | screens[8].prose, code | slot = counter & (N - 1); empty = head == tail; full = tail - head == N | correct | `sim: l16-generalise`, `l16-s0` |
| l16 | screens[8].options.slot.why | Equal slots happen when empty and when full | correct | `sim: l16-full-ring` (7 & 3 = 11 & 3 = 3 while the ring is full) |
| l16 | screens[8].explain | Unsigned subtraction is exact modulo 2^32, so tail - head is right across the wrap for any N; only the slot needs N to divide 2^32 | correct | [basic.fundamental]/2; `sim: l16-generalise` (any N; 4 and 8 keep slot order, 3 does not) |
| l16 | screens[9].prose | This one-thread version keeps plain `size_t` counters; the two-thread ring makes them atomic with the push screen's orders | correct | consistent with screens 5 and 6 |
| l16 | screens[9].widget.solution | Ring solution passes the ten drives and keeps the counters 64 bytes apart; the starter holds N - 1 and fails | correct | `sim: check_code_item l16-ring` (solution 10/10 under c++17 and c++20; starter fails t1 and t10); test expectations recomputed by the counter model |
| l16 | screens[9].explain | The starter refuses a push one slot early; the exact test is tail - head == capacity; `alignas(64)` puts each counter at the start of its own line | correct | `sim: l16-ring`; [dcl.align]/5 and [basic.align]: an `alignas(64)` member sits at a 64-byte boundary of a correctly aligned object |
| l16 | screens[10].widget | 0, 7, 13, 3 | correct | `sim: l16-drill` |
| l16 | screens[10].hints[2], explain | A mask costs one instruction, a division tens of cycles on many CPUs; items stored is always tail minus head | correct | Agner Fog, instruction tables: `DIV r64` 35 to 88 cycles latency on Skylake, 10 to 18 on Ice Lake and later; `AND` 1 cycle; the second claim is the counter-ring definition |
| l16 | screens[11].widget | 200, 256, 6,144, 8,192 | correct | `sim: l16-transfer` |
| l16 | screens[11].explain | 6,144 bytes sits in L1; 8,192 slots are 192 KiB, in L2 | correct | `sim: l16-transfer explain`; 6 KiB < 32 KiB; 192 KiB < a 256 KiB to 2 MiB L2 |
| l16 | summary.ideas[1] | Powers of two keep slot order across a 32-bit wrap; a ring of 3 puts two counters in one slot | correct | `sim: l16-s2`, `l16-generalise` |
| l16 | summary.ideas[2], trap | One writer per counter needs no lock; give head and tail lines of their own | correct | Williams 7.2; Intel Optimization Reference Manual on false sharing |
| l16 | quiz[0] (q16-slot) | 13 items; next slot 2 | correct | `sim: q16-slot` |
| l16 | quiz[1] (q16-pow2) | `N - 1` is all one bits so `&` acts like `% N`; for N = 6 the mask 101 keeps the wrong bits | correct | binary arithmetic; `sim: q16-pow2 explain` |
| l16 | quiz[1].options.even.why | The counters meet only when empty; the slots coincide when full as well | correct | `sim: l16-full-ring` |
| l16 | quiz[2] (q16-stall) | 2,048 slots | correct | `sim: q16-stall` |
| l16 | quiz[3] (q16-owner) | The consumer alone writes `head_`; the producer reads it and writes `tail_` | correct | screen 5 and 6 design; Williams 7.2 |
