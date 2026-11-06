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

## l16-ring-buffer

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l16 | objectives[0] | A fixed-size SPSC ring buffer can be built with two counters | correct | Williams §7.2 (lock-free queue, one producer and one consumer); sim: SPSC ring program (200,000 items in order) |
| l16 | screens[0].prose | Items come out at the head and go in at the tail (convention) | correct | the lesson's convention, used consistently through l16 and homework-4 items[4] |
| l16 | screens[0].canvas frames | Four pushes fill the ring, the fifth is refused, pops return 1 to 4, empty is head == tail | correct | derivation from full = tail − head == N, empty = head == tail |
| l16 | screens[0].hints[1..2], feedback.byKey.r1c1, explain.text | Pops return items in push order; full is a tail four ahead, empty is equal counters | correct | FIFO by construction; sim: SPSC in-order delivery |
| l16 | screens[1].prose | The counters only ever grow; the slot is the counter reduced to the ring size | correct | the growing-counter design (Williams §7.2; LMAX Disruptor sequence numbers) |
| l16 | screens[1].widget.rows, hints[2].text | 5 mod 4 = 1; 20 − 13 = 7; 20 mod 8 = 4 | correct | sim: l16 screens[1] |
| l16 | screens[1].explain.text | For a power of two, counter mod N is `counter & (N − 1)`; size is tail − head; the next push goes to slot 4 before the head's slot 5 | correct | N − 1 has the low log2 N bits set, so the AND keeps the remainder; sim |
| l16 | screens[2].prose | An `unsigned` counter wraps to 0 after 4,294,967,295; `size_t` is 4 bytes in this app and 8 on a desktop | correct | N4659 [basic.fundamental]/2 (unsigned arithmetic mod 2^N); wasm32 `size_t` is 32-bit, x86-64 64-bit |
| l16 | screens[2].hints[0].text | A power of two divides 2^32 evenly, so the low bits carry on across the wrap | correct | 2^k divides 2^32 for k ≤ 32; sim: slot order 2, 3, 0, 1 |
| l16 | screens[2].hints[1].text, feedback.byKey.r1c1 | 2^32 mod 3 = 1, so a ring of 3 breaks at the wrap; 4,294,967,295 = 3 × 1,431,655,765 | correct | sim: l16 screens[2] hints[1] |
| l16 | screens[2].explain.text | A power-of-two ring keeps slot order across the wrap and tail − head stays 2; a ring of 3 puts 4,294,967,295 and 0 in one slot; at 10 million pushes a second the wrap comes after 429.5 s | correct | sim: l16 screens[2] explain (both tables), row 3 |
| l16 | screens[3].prose | A cache line is 64 bytes; a core that writes a word takes the whole line from the other core | correct | MESI: a write needs the line in Modified state, invalidating the other core's copy (Drepper §3.3.4) |
| l16 | screens[3].widget.answer, hints[2], explain.text (first two sentences) | All eight words of the line move, including `head`; the consumer's store to `head_` pulls it back | correct | Drepper §3.3.4, §6.4.1 |
| l16 | screens[3].explain.text | "Neither counter is shared, yet the line ping-pongs: false sharing" | imprecise | both counters are shared in the ring's own design: the producer loads `head_` (screens[5] s2) and the consumer loads `tail_` (homework items[4] s2). Each counter has one writer and one reader on the other core, which is true sharing of each counter. False sharing is the extra traffic from the two counters sitting in one line (Drepper §6.4.1; Williams §8.2.3) |
| l16 | screens[4].prose | A store that steals the line costs about 60 ns, 1 ns when the line stays put (stated assumption) | correct as an assumption | cross-core line transfer is tens of ns (Drepper §3.3.2 figures; l1-latency-numbers) |
| l16 | screens[4].explain.text | With `alignas(64)` each counter keeps its own line and the cost falls to 10 ms | misleading | `alignas(64)` removes the false sharing but not the true sharing: the producer's store to `tail_` still invalidates the consumer's copy of the `tail_` line, which the consumer re-reads on every pop (and the same for `head_`), so neither line "stays put" at 1 ns a push. The standard remedy that makes most pushes touch no shared line is a cached copy of the other side's counter, re-read only when the ring looks full or empty (Rigtorp SPSCQueue; LMAX Disruptor 2011 §3.3; Williams §8.2.3 on keeping shared data apart) |
| l16 | screens[5].prose | A `release` store publishes everything written before it, and an `acquire` load that reads it sees it | correct | N4659 [atomics.order]/2, [intro.races]/9 to 12 (synchronizes-with, happens-before); Williams §5.3.3 |
| l16 | screens[5].widget.answer (s1 to s5) | push: relaxed load of own `tail_`; `if (t − head_.load(acquire) == N) return false`; write slot; `tail_.store(t + 1, release)`; return true | correct | Williams §7.2 and §5.3.3: the acquire on `head_` orders the consumer's reads of the slot before the producer's overwrite; the release on `tail_` publishes the slot write; sim: SPSC ring, 200,000 items, in order, TSan clean |
| l16 | screens[5].widget.lines[5].why (d1) | A relaxed store can become visible before the slot write, so the consumer could read a stale slot | correct | no happens-before from a relaxed store, N4659 [atomics.order]/1 (relaxed), Williams §5.3.3 |
| l16 | screens[5].widget.lines[6].why (d2) | Only the consumer writes `head_`; a second writer would race | correct | SPSC ownership; a second writer of an atomic does not "race" in the UB sense but breaks the single-writer invariant; acceptable |
| l16 | screens[5].widget.lines[7].why (d3) | Each counter has one writer, so no lock is needed | correct | Williams §7.2 (lock-free SPSC) |
| l16 | screens[5].feedback.byKey.s3, .s4, explain.text | The slot write must precede the tail store; a relaxed store would not order the two | correct | as above |
| l16 | screens[6].prose, options[0] | One producer and one consumer: no mutex needed, each counter has one writer | correct (with the atomics and orders of screens[5]) | Williams §7.2 |
| l16 | screens[6].widget.options[1].why, feedback.byKey.yes | The threads write different slots; the counters hand each slot across | correct | the acquire/release pair orders slot access (Williams §5.3.3) |
| l16 | screens[6].widget.options[2].why, feedback.byKey.vector | A vector is not thread safe | correct | N4659 [res.on.data.races]/3 (library functions may be called concurrently only when no object is modified) |
| l16 | screens[6].widget.options[3].why, feedback.byKey.pop | The consumer alone writes `head_`, so `pop` needs no lock either | correct | as above |
| l16 | screens[6].explain.text | "A race needs two writers of one variable." | wrong | N4659 [intro.races]/21: a data race is two conflicting actions in different threads, at least one not atomic, neither happening before the other; conflicting means one modifies and the other accesses ([intro.races]/2). One writer and one reader of a plain variable is a data race and undefined behaviour. l7-data-races teaches it correctly ("at least one writes"). sim: l16 screens[6] explain (ThreadSanitizer reports one writer plus one reader) |
| l16 | screens[6].explain.text (third sentence) | A release and acquire pair makes each slot visible before its counter moves | correct | Williams §5.3.3 |
| l16 | screens[7].prose | Some rings keep wrapped indexes and give up one slot to tell full from empty | correct | classic circular buffer with N − 1 capacity (Knuth TAOCP 1 §2.2.2 queue in a circular array keeps one cell empty) |
| l16 | screens[7].widget.accept, explain.text | Head 7, tail 11 in a ring of 4: 4 items, both slots 3; counters let a ring of N hold N items | correct | sim: l16 screens[7] |
| l16 | screens[7].feedback.byKey.zero, .three | Equal slots but counters differ by 4 is full; only wrapped indexes stop at three | correct | derivation |
| l16 | screens[8].prose | slot = counter & (N − 1); empty = head == tail; full = tail − head == N | correct | derivation; sim |
| l16 | screens[8].widget.options[1].why, options[2].why | Equal counters mean empty; equal slots happen when empty and when full | correct | derivation |
| l16 | screens[8].explain.text | "Unsigned subtraction stays right across the wrap, because 2^32 is a multiple of N" | wrong (right conclusion, wrong reason) | unsigned subtraction is exact modulo 2^32 for any N (N4659 [basic.fundamental]/2): with N = 3, tail 1 and head 4,294,967,295 still give 2. What needs N to divide 2^32 is the slot mapping counter mod N, as screens[2] shows. sim: l16 screens[8] explain (EXPECTED_FAIL) |
| l16 | screens[9].prose | push false when full, pop false when empty; keep `head_` and `tail_` on separate cache lines for two cores | correct as a contract | sim: l16 screens[9] Ring tests |
| l16 | screens[9].widget.solution | Full is `tail_ − head_ == buf_.size()`; `alignas(64)` on each counter puts them 64 bytes apart; all 10 tests pass | correct for the single-threaded tests | sim: l16 screens[9] Ring (c++17, c++20); solution offsets ≥ 64, `alignof(Ring)` 64 |
| l16 | screens[9].widget.solution and prose together | The code is presented as the two-core ring (separate lines "so two cores do not share a cache line") | misleading | the counters are plain `std::size_t` with no atomics and no release/acquire, which screens[5] just taught are what makes the two-thread ring correct; driven by two threads this `Ring` is a data race (N4659 [intro.races]/21). sim: l16 screens[9] widget.solution (ThreadSanitizer reports the race; EXPECTED_FAIL). A learner may carry the alignas-only version away as the SPSC queue |
| l16 | screens[9].widget.starter | `>= buf_.size() − 1` refuses a push one slot early and fails | correct | sim: starter fails tests 0, 3 (capacity 1 refuses every push) |
| l16 | screens[9].hints[0..2], explain.text | The ring may hold N items; full test is equality with the capacity; `alignas(64)` before each counter | correct | sim |
| l16 | screens[10].hints[2].text, explain.text | A mask costs one instruction, a division tens of cycles on many CPUs | correct (for a runtime N) | Agner Fog instruction tables: `div r32` 26 cycles latency on Skylake, `div r64` 35 to 88; for a compile-time N the compiler strength-reduces `%` itself, which the lesson does not say but its `Ring` has a runtime capacity |
| l16 | screens[10].explain.text | Items stored is always the tail minus the head | correct | growing counters; unsigned subtraction exact mod 2^32 |
| l16 | screens[10].widget.rows | Ring of 1: second push 0, pop 7; 45 & 15 = 13; 103 − 100 = 3 | correct | sim: l16 screens[10] |
| l16 | screens[11].explain.text | 256 slots × 24 = 6,144 bytes sits in L1; 5,000 messages round up to 8,192 slots, 192 KiB, in L2 | correct | 8,192 × 24 = 196,608 = 192 KiB; L2 is 256 KiB to 2 MiB on current cores |
| l16 | screens[11].prose | A 1 ms stall at 200,000 a second must lose nothing: 200 messages (assumes the ring is empty when the stall starts) | correct (stated setup) | 200,000 × 0.001 = 200; sizing from an empty ring is the interview convention |
| l16 | summary.ideas[1] | Powers of two keep slot order across a 32-bit wrap; a ring of 3 puts two counters in one slot | correct | sim: l16 screens[2] explain |
| l16 | summary.ideas[2], summary.trap | One writer per counter needs no lock; give head and tail lines of their own | correct (with atomics) | Williams §7.2, §8.2.3 |
| l16 | quiz[0] | Head 37, tail 50 in a ring of 16: 13 items, next slot 2 | correct | sim: l16 quiz[0] |
| l16 | quiz[1].widget.options[0], explain.text | `N − 1` is all one bits, so `&` acts as `% N`; for N = 6 the mask 101 keeps the wrong bits | correct | binary 5 = 101; sim: l16 quiz[1] explain |
| l16 | quiz[1].widget.options[1].why | Speed comes from the mask replacing a division; other sizes break the mask | correct | as screens[10] |
| l16 | quiz[1].widget.options[2].why | The ring is far larger than a line | correct | 16 ints already exceed 64 bytes |
| l16 | quiz[1].widget.options[3].why | "They meet when empty and when full" | imprecise | with growing counters the counters are equal only when empty; it is the slots that coincide when full as well (screens[7]). "They" reads as the counters in an item about counters |
| l16 | quiz[2] | 5 ms at 400,000 a second is 2,000 messages, next power of two 2,048 | correct | sim: l16 quiz[2] |
| l16 | quiz[3] | The consumer alone writes `head_`; the producer reads it | correct | Williams §7.2 |
