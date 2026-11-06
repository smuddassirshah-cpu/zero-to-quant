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

## l17-measuring-latency

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l17 | objectives[0] | Latency is reported as percentiles; the mean misleads | correct | Tene (2015); Dean and Barroso, *The Tail at Scale* (CACM 2013) |
| l17 | screens[0].explain.text | Mean 19.9 µs; not one request took that long; "the mean describes a request that never happened" | correct | derivation; sim: l17 screens[0] |
| l17 | screens[1].prose | Out of 1,000 sorted requests the p99 is the value at position 990 (nearest-rank convention, stated once where it first matters) | correct (convention stated) | nearest-rank method, rank ⌈p n / 100⌉ (Hyndman and Fan 1996 Type 1, inverted CDF); NumPy's default linear interpolation would read 19.9 here; the lesson says which it uses |
| l17 | screens[1].widget.accept, hints[2], explain.text | The p99 first reads 1,000 µs at 11 slow requests; the mean moves from 19.9 to 20.9 | correct | sim: l17 screens[1] and explain |
| l17 | screens[1].feedback.byKey.ten, .one | With 10 slow position 990 is fast; one slow sits at position 1,000 | correct | derivation |
| l17 | screens[2].prose, widget.rows, explain.text | p50 10, p99 10, p99.9 1,000; with one slow only the maximum shows it | correct | sim: l17 screens[2] |
| l17 | screens[3].prose | A closed-loop client (send, wait, send) delays the requests due during a stall; two reports of one run | correct | Tene (2015), coordinated omission; HdrHistogram `recordValueWithExpectedInterval` |
| l17 | screens[3].canvas | done − sent: p50 40, p99 50, p99.9 248; done − intended: 49, 48,821, 49,911; 875 of 2,000 sent late | correct | sim: l17 screens[3] canvas (recomputed from latencies.csv) |
| l17 | screens[3].widget.options[0], explain.text | Done minus intended shows what a queued request felt; waiting for each reply hides the delay: coordinated omission | correct | Tene (2015) |
| l17 | screens[3].widget.options[1].why, feedback.byKey.sent | The client sent late because it was waiting; that wait is missing | correct | derivation: sent − intended is the wait |
| l17 | screens[3].widget.options[2].why | They differ by exactly the time each request waited to be sent | correct | (done − intended) − (done − sent) = sent − intended; sim: l17 screens[3] options[2].why |
| l17 | screens[3].widget.options[3].why | 875 of 2,000 were delayed, not one outlier | correct | sim: 875 rows have sent > intended |
| l17 | screens[4].widget.starter docstring | rank = ceil(p n / 100) nearest rank; closed-loop client sent each request when the previous reply arrived | correct | method statement; CSV consistent (one intended every 100 µs) |
| l17 | screens[4].widget.solution | Integer ceiling `-(-permille * n // 1000)`, both lists, true mean 10,584.622 | correct | sim: l17 screens[4] solution passes 11 tests; starter fails |
| l17 | screens[4].widget.tests[7..10] | 77 rows: p99 and p99.9 both rank 77 (86); 1,000 rows p99.9 rank 999 (1008); 78 rows p50 rank 39 (48) | correct | sim: l17 screens[4] tests[7..10] (37 is coprime to 77, 1000 and 78, so the values are permutations) |
| l17 | screens[4].hints[1].text, hints[2].text | Rank ⌈p n / 100⌉ counting from 1; use integers for the rank | correct | avoids the float boundary of screens[6] |
| l17 | screens[4].explain.text | The true list has the 50 ms stall inside it, which is why its p99 is 48,821 µs | correct | sim: one reply about 50 ms; about 500 requests due during it plus the catch-up backlog push 875 past rank 1,980 |
| l17 | screens[5].widget.options[0], explain.text | Quote both, tail first; the mean is a total over a count and a few slow requests move it little; the mean still helps for sizing capacity | correct | Tene (2015); the mean × arrival rate is the average concurrency (Little's law), which is the capacity use |
| l17 | screens[5].widget.options[1].why, options[2].why, options[3].why | The mean describes no request; the median ignores the tail; one maximum can be a fluke, percentiles show how often | correct | derivation; Dean and Barroso (2013) |
| l17 | screens[6].prose, canvas | 0.999 × 1,000 = 999 exactly; 99.9 / 100 × 1,000 in a double is 999.0000000000001 and `ceil` gives 1,000 | correct | IEEE 754 binary64; sim: l17 screens[6] (Python and C++ doubles agree) |
| l17 | screens[6].widget.accept, explain.text | The correct p99.9 of 999 fast and one slow is 10 µs (rank 999); the float reads rank 1,000 | correct | sim: l17 screens[2] row 3 and screens[6] |
| l17 | screens[6].explain.text | NumPy 2.0.2 with `inverted_cdf` does the same | correct (checked on NumPy 2.5.3, the same code path) | sim: l17 screens[6] explain (NumPy inverted_cdf gives 1000.0); NumPy computes `q / 100 * n` in floating point |
| l17 | screens[6].explain.text | Work in integers, or subtract 1e-9 before the `ceil` | correct | the integer form is exact; the 1e-9 guard is a convention safe while p n / 100 has no fractional part below 1e-9 (true for p with few decimals and n below 1e6) |
| l17 | screens[7].prose | Nearest rank r = ⌈p n / 100⌉ counted from 1, rank 1 for p = 0; report the tail first; measure from the intended send time | correct | nearest-rank method (Hyndman and Fan Type 1); Tene |
| l17 | screens[7].widget.options[0], explain.text | p95 of 40 samples is rank 38, an exact integer so no rounding up; rank counts from the smallest | correct | 0.95 × 40 = 38; sim |
| l17 | screens[7].widget.options[1..3].why | Rank 39 added one; rank 2 used the 5% left over; 95 is a percentage not a rank | correct | each names the learner's error |
| l17 | screens[8].prose | 64.4 × 250 / 100 is 161.00000000000003 in doubles, so an unguarded `ceil` gives 162 | correct | sim: l17 screens[8] (Python and C++) |
| l17 | screens[8].widget.solution | Sort a copy, rank = ceil(p n / 100 − 1e-9) clamped to [1, n], return `samples[rank − 1]` | correct | sim: l17 screens[8] percentile passes 15 tests (c++17, c++20); starter fails |
| l17 | screens[8].explain.text | The 1e-9 guard keeps a rank that is exactly whole from creeping up | correct | as screens[6] |
| l17 | screens[9].prose | A clock read costs about 20 ns; in this app the clock ticks in 100 µs steps | correct | `clock_gettime` via the vDSO is about 20 to 25 ns on Linux x86-64; browsers coarsen `performance.now()` to 100 µs without cross-origin isolation (W3C HR-Time, Chrome) |
| l17 | screens[9].prose, hints[0], feedback.byKey.r0c1, explain.text | "Timing one 10 ns call alone adds two reads to it": the call reads as 50 ns and the clock is 80% of it | imprecise | the bracket `t0 = now(); f(); t1 = now();` measures from the instant the first read captures its timestamp to the instant the second does, which contains the tail of the first read and the head of the second: about one read's cost, not two (Paoloni 2010 §3.1 measures the overhead as the delta of two back-to-back reads, about one read; Agner Fog, *Optimizing software in C++* §16.1). The screen's model is stated and the table keys follow it, but a learner carries away "two reads inside the measurement" |
| l17 | screens[9].explain.text | In a batch of 1,000 the two reads add 0.04 ns a call; warm up first, time batches, take the median | correct (the batch conclusion holds under either overhead model) | derivation 40 / 1,000; warm-up and batching are standard (Paoloni 2010 §3.2; Google Benchmark) |
| l17 | screens[10].widget.rows, explain.text | Sorted 1 to 5: p20 rank 1, p50 rank 3 (2.5 rounds up), p80 rank 4, p100 rank 5 | correct | sim: l17 screens[10] |
| l17 | screens[11].widget.rows, explain.text | Host B p99 1,000; average of the two p99 values 505, a number no request had; pooled p99 is position 1,980 of 2,000, slow, 1,000 µs | correct | sim: l17 screens[11] |
| l17 | screens[11].hints[1].text | Averaging two percentiles is not a percentile of anything | correct | Tene (2015): percentiles do not average; sim: l17 screens[11] hints[1] |
| l17 | screens[11].explain.text | On a desk, ship the histograms, not the percentiles | correct | HdrHistogram merge; Tene |
| l17 | summary.ideas[0..2], formula | Tail first; r = ⌈p n / 100⌉ and integers at a boundary; measure from the intended send | correct | as above |
| l17 | summary.trap | Quoting the mean, or timing from the late send | correct | Tene |
| l17 | quiz[0] | p75 of 1 to 10 is rank ⌈7.5⌉ = 8, the value 8 | correct | sim: l17 quiz[0] |
| l17 | quiz[1].widget.options[0], explain.text | A closed-loop client records almost nothing about the requests due during a stall; the stall appears as one slow request | correct | Tene (2015) |
| l17 | quiz[1].widget.options[1..3].why | It never timed their wait; none of the waiting is recorded; percentiles are unaffected too | correct | as above |
| l17 | quiz[2] | Mean (95 × 20 + 5 × 400) / 100 = 39 µs; 210 is the unweighted average of the two values | correct | derivation |
| l17 | quiz[3].widget.options[0], explain.text | Time a batch of many calls with two reads after a warm-up; the warm-up fills the caches | correct | Paoloni 2010; Agner Fog §16 |
| l17 | quiz[3].widget.options[1].why | Two reads cost 40 ns, four times the function | imprecise | same two-read model as screens[9]; the ranking of the options is unaffected |
| l17 | quiz[3].widget.options[2].why | One call includes cold caches and the clock reads | correct | first-touch cache and TLB misses (Drepper §3, §4) |
| l17 | quiz[3].widget.options[3].why, feedback.byKey.sleep | An idle CPU runs slower; warm it up instead | correct | C-state exit latency and frequency ramp after idle (Intel SDM vol. 3 §14, C-states; the usual "spin before measuring" advice) |

## l18-feed-handler

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l18 | screens[0].widget.answer | Packet in to order out: NIC to a user-space ring, decode, sequence check, book, strategy, encode and send | correct | the standard handler pipeline (kernel bypass with a user-space ring, e.g. DPDK/OpenOnload; sequence check before the book so a stale frame never changes it) |
| l18 | screens[0].widget.lines[6].why (d1) | A file write is a system call that can take microseconds; log from another thread | correct | `write(2)` is a syscall (hundreds of ns to µs with the page cache; more on a flush); l11-processes |
| l18 | screens[0].widget.lines[7].why (d2) | An allocation on every message adds cost and a rare slow case | correct | l15; glibc malloc slow path |
| l18 | screens[0].hints[1], feedback.byKey.s3, explain.text | The sequence is checked before the book changes, so a stale frame never changes it | correct | design rule; matches the solution of screens[8] (`frame()` checks seq first) |
| l18 | screens[1].canvas | Stages 1,000, 200, 0, 300, 500, 500 ns: total 2,500 (stated budget) | correct | stated figures; sum 2,500 |
| l18 | screens[1].widget.accept, explain.text | The card-to-ring stage is 40% of the total | correct | 1,000 / 2,500 |
| l18 | screens[1].explain.text | "The network card to user buffer is the biggest share, which is why handlers bypass the kernel" | imprecise | the 1,000 ns stage is already the kernel-bypass path (stage 1 is "network card to a ring in user space"); through the kernel socket stack the same hop is several microseconds (l12-files-and-sockets; DPDK and OpenOnload figures). The size of the bypassed hop is the reason to bypass, which the sentence inverts |
| l18 | screens[2].prose | Allocations cost 50 ns each; a stall such as a page fault or a context switch can take 5 µs | correct | a context switch is 1 to 5 µs, a minor page fault about 1 µs, a major one far more (l3-virtual-memory, l11-processes); stated as "can" |
| l18 | screens[2].widget.rows, explain.text | 2,500; 500 slack; 2,700 with four allocations; 7,500 with a 5 µs stall; the budget must hold for the worst message | correct | sim: l18 screens[2]; Dean and Barroso (2013) on tails |
| l18 | screens[3].widget.rows, explain.text | 201 levels; 1,608 bytes; 16,384 bytes; 18,032 bytes in all; fits a 32 KiB L1; a cached best price removes the scan | correct | sim: l18 screens[3] and sizeof(Handler) == 18,032 |
| l18 | screens[4].prose | Policy: apply a frame at or above the expected number, count skipped numbers as a gap, drop a frame below it | correct (stated policy) | one common arbitration policy; others hold frames briefly (the explain says so) |
| l18 | screens[4].widget.answer, feedback.byKey.c1..c8, explain.text | Applied 1A, 2A, 4A, 5A with a gap of 1; 3B is stale after 4A; a better handler would hold 4A briefly | correct | sim: l18 screens[4] |
| l18 | screens[5].widget.options[0], explain.text | `std::unordered_map` allocates nodes and rehashes at unpredictable times; both can land on one message | correct | N4659 [unord.req]/9 (node-based, rehash when `size() > max_load_factor() * bucket_count()`) |
| l18 | screens[5].widget.options[1].why | Its average is fine; the worst case is the problem | correct | amortised O(1) per insert, O(n) on a rehash |
| l18 | screens[5].widget.options[2].why | An `unordered_map` does not sort | correct | N4659 [unord.req]/1 |
| l18 | screens[5].widget.options[3].why | One thread can use it | correct | N4659 [res.on.data.races] |
| l18 | screens[5].explain.text | An array indexed by order id, or a preallocated table, has neither | correct | fixed storage; sim: l18 screens[8] alloc_count 0 |
| l18 | screens[6].prose | A stream read can end mid-frame and one read can hold several; a gap is judged only on a whole frame | correct | TCP is a byte stream (l13-tcp-and-udp; RFC 793 §1.5) |
| l18 | screens[6].widget.rows, explain.text | Reads of 50, 40, 80 bytes complete 2, 1, 4 frames with 2 bytes waiting | correct | sim: l18 screens[6] |
| l18 | screens[7].prose | Pipeline with a budget; keep stages free of allocation; handle loss and partial reads on purpose | correct | the lesson's method |
| l18 | screens[7].widget.options[0], explain.text | A number above the expected one counts the gap and applies the frame; a smaller number is dropped | correct | policy of screens[4]; sim: l18 quiz[1], quiz[3] |
| l18 | screens[7].widget.options[1].why, options[2].why | Dropping is for a number below; waiting stalls every later message | correct | policy; latency argument |
| l18 | screens[8].prose, starter comments | Frames are 24 bytes in the l14 layout, big-endian; 'A' add, 'X' cancel the rest, 'T' trade qty; seq below expected is ignored, above adds the difference to gaps; partial frames wait; after construction no heap | correct | l14-messages-on-the-wire (seq at offsets 4 to 7, MSB first); sim: l18 screens[8] prelude frame layout |
| l18 | screens[8].widget.solution | Byte-at-a-time assembly into a 24-byte buffer; sequence check first; arrays by price (201 levels) and by id (1,024); cancel and trade subtract from the order's level; out-of-range id or price ignored; no allocation in `feed` | correct | sim: l18 screens[8] Handler passes 15 tests (c++17, c++20); alloc_count 0 |
| l18 | screens[8].widget.solution `frame()` | `expected_` and `applied_` advance before the id and price range checks, so an out-of-range frame still counts as applied | correct (consistent with tests[6], [11]; a design choice not stated) | sim: tests pass; no test contradicts it |
| l18 | screens[8].widget.starter | `std::map` book, adds only, ignores sequence numbers: fails | correct | sim: starter fails (alloc test and gap tests) |
| l18 | screens[8].explain.text | The map allocates a node per price level, so the starter fails the count; a 24-byte buffer carries a partial frame | correct | N4659 [associative.reqmts]; sim: starter alloc_count > 0 |
| l18 | screens[9].widget.rows, explain.text | 2,000 ns; 2,150 ns; 150,000 × 24 = 3.6 MB a second; 37 frames and 12 bytes | correct | sim: l18 screens[9]; MB as 10^6 bytes |
| l18 | screens[10].widget.rows, explain.text | 50 × 18,032 = 901,600 bytes, 880.5 KiB, 28 caches of 32 KiB; fits a large L2; each message touches one instrument's slice | correct | 901,600 / 1,024 = 880.47; / 32,768 = 27.5; L2 of 1 to 2 MiB on current cores; working set argument (Drepper §6) |
| l18 | summary.ideas[0..2], formula, trap | Pipeline with a budget; arrays, no hash map; gaps above, drops below, partial waits; plan for the worst message | correct | as above |
| l18 | quiz[0] | 600 + 100 + 200 + 300 + 300 = 1,500 ns, 500 ns slack against 2 µs | correct | derivation |
| l18 | quiz[1] | Expecting 10, a 14 adds 4 to the gap count and expects 15 next | correct | sim: l18 quiz[1] |
| l18 | quiz[2] | 2,048 × 16 = 32,768 bytes, exactly 32 KiB, a typical L1 | correct | derivation; 32 KiB L1d (48 KiB on Ice Lake and later, still "typical") |
| l18 | quiz[3].widget.options[0], explain.text | Expecting 9, a 7 is dropped as a duplicate or late arrival | correct | policy; sim: l18 quiz[3] |
| l18 | quiz[3].widget.options[1..3].why | A gap counts numbers above; nothing is held for a number below; moving back would replay old data | correct | policy |

## review-4

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| review-4 | items[0] (r4-allocating-lines) options and explain | `emplace_back` on an empty vector, `new double[3]` and `std::string(64)` allocate; `double a[3]`, `std::array<double, 3>` and an empty `std::vector<double> w` do not | correct | libstdc++ SSO 15 (libc++ 22), so 64 allocates; sim: review-4 items[0] |
| review-4 | items[0].feedback.byKey.decl | An empty vector allocates on its first push, not when declared | correct | sim: l15 screens[6] trap |
| review-4 | items[1] (r4-pool-order) | Release 2, 3, 1: the list reads 1, 3, 2, next allocate returns 1 | correct | sim: review-4 items[1] |
| review-4 | items[2] (r4-alloc-bill) | 3 × 50 ns × 120,000 = 18 ms | correct | derivation |
| review-4 | items[3] (r4-ring-counters) | Head 70, tail 85, ring of 32: 15 items, next slot 85 & 31 = 21 | correct | sim: review-4 items[3] |
| review-4 | items[4] (r4-ring-order) | Ring of 2: 10, 20 in, 30 refused, pop 10, push 40, pops 20 then 40: the third pop is 40 | correct | FIFO derivation |
| review-4 | items[5] (r4-mean-p99) | Mean 38.1 µs; p99 at position 990 is 400 µs since only 940 are fast | correct | sim: review-4 items[5] (nearest rank, the convention l17 states) |
| review-4 | items[6] (r4-p60) | p60 of 8 by nearest rank: ⌈4.8⌉ = 5, value 6; rounding down gives 5, rank 6 gives 7 | correct | sim: review-4 items[6] |
| review-4 | items[7] (r4-budget) | 2,600 + 6 × 50 = 2,900 ns | correct | derivation |
| review-4 | items[8] (r4-two-reads) | 31 then 41 bytes: 1 frame plus 7 held, then 48 bytes = 2 frames, 3 in all | correct | sim: review-4 items[8] |

## homework-4

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| homework-4 | items[0].prose (h4-latency-hist) | Keeping every sample would allocate; a histogram with a bucket per power of two does not; sample ns goes in bucket ⌊log2 ns⌋ | correct | a growing container allocates; a fixed `std::array<int, 40>` does not; HdrHistogram uses the same log-scale bucketing idea |
| homework-4 | items[0].widget.starter comment | `percentile_upper(p)` finds the bucket holding the nearest-rank sample (rank ⌈p n / 100 − 1e-9⌉, at least 1) and returns its upper bound 2^(bucket + 1) | correct | the bucket b holds [2^b, 2^(b+1)), so 2^(b+1) is an exclusive upper bound: a conservative report |
| homework-4 | items[0].widget.solution | Shift loop for ⌊log2⌋, clamp at 39, cumulative walk to the rank | correct | sim: homework-4 items[0] LatencyHist passes 15 tests (c++17, c++20); starter fails; alloc_count 0 over 1,000 records |
| homework-4 | items[0].widget.tests[8] | 2^45 clamps to bucket 39 and reports 2^40 | correct | sim: homework-4 items[0] explain |
| homework-4 | items[0].explain.text | 10 ns is bucket 3 (8 to 15), upper bound 16; the array was sized at construction so `record` never allocates | correct | sim |
| homework-4 | items[1].parts[0..3] (h4-sizing) | 3,000 slots; 60,000 bytes (58.6 KiB); 300 messages in 2 ms, 512 slots; 12,288 bytes | correct | sim: homework-4 items[1] |
| homework-4 | items[1].parts[4] options and explain | Only the 12,288-byte ring fits a 32,768-byte L1; the pool is 27,232 over, the pair 39,520 over | correct | sim: homework-4 items[1] parts[4] |
| homework-4 | items[1].parts[4].widget.options[3].why | "The question is about the whole pool, and it is 27,232 bytes over" (against "only the slots in use are touched") | imprecise | the distractor raises the right idea (residency depends on the working set, not the allocation: Drepper §6) and the why dismisses it by fiat; the sound reason is that even the 2,400 live slots are 48,000 bytes, over L1. sim: homework-4 items[1] parts[4] |
| homework-4 | items[2].model §1 (h4-handler-aloud) | Pipeline: user-space ring, decode, sequence, book, strategy, send; 4 µs target, stages 1,200 + 250 + 350 + 600 + 600 = 3,000 ns, 1,000 ns slack | correct | sim: homework-4 items[2] model budget |
| homework-4 | items[2].model §2 | Every allocation is about 50 ns and a rare slow case; take memory before the first message; prove it by resetting a `new` counter and asserting 0 | correct | l15; sim: ALLOC harness |
| homework-4 | items[2].model §3 | Below expected: dropped; above: skipped numbers to a gap count; the gap is repaired from a snapshot; partial frames wait in a small buffer | correct | l18 policy; snapshot recovery is the standard gap repair (exchange snapshot and incremental feeds, e.g. ITCH/MoldUDP64 recovery) |
| homework-4 | items[2].model §4 | A £4 range in pennies is 401 levels a side | correct | 400 steps, both ends included |
| homework-4 | items[2].model §4 | "Both are sized at start, so they fit in L1, and neither can rehash" | imprecise | being sized at start makes the size fixed and removes rehashing; fitting in L1 follows from the size (401 × 4 × 2 = 3,208 bytes plus 1,024 × 16 = 16,384, under 32 KiB), not from when it was taken. The rubric asks "why they stay in cache", so the reason given should be the size |
| homework-4 | items[2].model §4 | A `std::unordered_map` allocates and rehashes at unpredictable moments | correct | N4659 [unord.req]/9 |
| homework-4 | items[2].model §5 | Time from the intended send time; quote p99 and p99.9 first, the mean after; time batches after a warm-up | correct | Tene (2015); Paoloni (2010) |
| homework-4 | items[2].model §6 | Counting and moving on keeps delay low but loses frames the other feed may hold; a short hold recovers some at a latency cost | correct | A/B arbitration trade-off (l18 screens[4] explain) |
| homework-4 | items[2].rubric | Pipeline with figures; allocation avoided and proved; loss handling; arrays and why they stay in cache; percentiles from intended time; a trade-off | correct | matches the lesson's method |
| homework-4 | items[3].parts[0..2] (h4-two-hosts) | Average of 20 and 800 is 410, a number no request had; pooled p99 with 40 slow of 2,000 is 800; with 15 slow it is 20 | correct | sim: homework-4 items[3] |
| homework-4 | items[3].parts[1].feedback.byKey.avg, parts[2].feedback.byKey.avg | 410 averages two percentiles, which is not a percentile | correct | Tene (2015) |
| homework-4 | items[3].parts[2].explain.text | Host B alone still has a p99 of 800 µs (15 slow of 1,000, position 990 slow) | correct | 985 fast, rank 990 slow |
| homework-4 | items[3].parts[3].widget.options[0], explain.text | Pool the samples (or merge histograms with the same buckets) and read the percentile once | correct | HdrHistogram merge; Tene |
| homework-4 | items[3].parts[3].widget.options[1].why | The average is a number no request had, "and it moves the wrong way as hosts differ in size" | correct (vague) | an unweighted average ignores request counts; with 15 slow the honest fleet p99 is 20 while the average says 410 |
| homework-4 | items[3].parts[3].widget.options[2].why, options[3].why | The larger p99 says 800 when only 0.75% were slow; medians say nothing about the tail | correct | derivation |
| homework-4 | items[4].widget.answer (h4-pop-order) | pop: relaxed load of own `head_`; `if (h == tail_.load(acquire)) return false`; read slot; `head_.store(h + 1, release)`; return true | correct | Williams §7.2, §5.3.3; sim: SPSC ring program (TSan clean, in order) |
| homework-4 | items[4].widget.lines[5].why (d1) | A relaxed `head_` store can become visible before the slot read, so the producer could overwrite it first | correct | the release on `head_` orders the slot read before the producer's acquire of `head_` and its overwrite (N4659 [intro.races]/9 to 12) |
| homework-4 | items[4].widget.lines[6].why (d2) | Only the producer writes `tail_` | correct | SPSC ownership |
| homework-4 | items[4].widget.lines[7].why (d3) | A relaxed load of `tail_` does not pair with the producer's release, so the slot may not be visible yet | correct | N4659 [atomics.order]/2 (synchronizes-with needs an acquire load) |
| homework-4 | items[4].feedback.byKey.s3, .s4, explain.text | Read the slot before the head moves; the release store tells the producer the slot is free | correct | as above |
| homework-4 | items[5] (h4-stall-count) | 40 ms / 250 µs = 160 requests due; the closed-loop client sent none on time, so its own timing hides all 160 | correct | sim: homework-4 items[5]; Tene (2015) |

## Verdict counts

231 rows: correct 218, wrong 2, imprecise 8, misleading 2, unverified 1 (the compiler download size and time in l15 screens[5].widget.how, an engine figure outside this audit).

The `wrong` rows: l16 screens[6].explain.text (a race needs two writers) and l16 screens[8].explain.text (the reason unsigned subtraction survives the wrap). The `misleading` rows: l16 screens[4].explain.text (alignas makes the line stay put) and l16 screens[9] (a plain-counter ring presented as the two-core ring). Each is a finding in `docs/reviews/audit-systems-4.md`, as is every imprecise row; l17 quiz[3].options[1].why is folded into the l17 screens[9] finding.
