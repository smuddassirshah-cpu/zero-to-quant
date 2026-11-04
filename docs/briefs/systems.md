# Level briefs: systems (Systems for Developer Interviews, topic 3.5)

Course context. `systems` is a course of topic 3.5, Interviews by role (track `speed`, strand `quant`, strandNote "Developer and low-latency roles", about 40 hours, 4 levels and 18 lessons; plan in `docs/briefs/interview-plan.md` section (b), priority [Should], [Must] for the developer track). Its promise is the `course.json` description: "Explain memory, concurrency, the kernel and the network, then write low-latency C++ for developer rounds." The gap analysis (`docs/briefs/interview-gaps.md`) lists developer rounds that ask about caches, threads and locks, sockets and protocols, and "design a market data handler" at an intern level. User decisions of 29 October 2026 apply: UK and Europe first (£, London distances), trader and researcher tracks first, so this course runs in the final phase, no audio, firm-neutral. Lessons never name a firm, an exchange or a person: say "an exchange", "a trading firm", "a bank". Our wire format is invented (24 bytes, defined in l14); no real feed protocol is quoted. Latency figures are round figures for a modern desktop-class core, stated as such; real values vary by machine. Free resources are named once per level, in its first lesson, by title and kind only: level 1 "What Every Programmer Should Know About Memory" (a free long paper); level 2 the thread-support pages of cppreference.com (a free reference); level 3 "Beej's Guide to Network Programming" (a free guide) and the Linux manual pages for `read`, `recv` and `epoll`; level 4 free conference talk recordings on low-latency C++ for trading systems. Never quote any of them.

Prerequisites (the plan): `cpp` levels 1 to 4 and level 5 (course.json lists `l19-moving-not-copying` to `l23-own-smart-pointer`; those files are unwritten, so depend on their titles only), `cpp-pricing` level 3. Builds on, by lesson: `cpp` l7-addresses, l8-stack-and-heap, l9-owning-memory, l14-vector, l15-maps; `cpp-pricing` l9-timing (batch timing and the median: l17 here does not repeat it), l10-memory-layout (cache lines of 8 doubles and flat storage: l2 here uses different numbers and does not repeat array-of-structs against struct-of-arrays), l11-optimisation-flags (this app compiles at `-O1` with asserts on: l5 and l15 rely on it); `ds` l1-arrays-in-memory, l11-first-in-first-out; `algo-think` l3-memory; `micro` l1-bids-and-asks and l3-the-queue (l18); `py-found` l10-reading-a-csv and `first-python` l11-numbers-from-a-file (the two Python items); `terminal` l7-looking-inside (reading output). `cpp` l22-undefined-behaviour (unwritten) will own undefined behaviour in general; l7 here teaches only that a data race is undefined behaviour.

Lesson shape: the `puzzles` and `game-theory` shape. The method is stated after the learner has used it; three worked examples of rising difficulty (the first tried on a canvas before any rule is named); a `trap` screen built on the answer candidates blurt; one edge case; a drill of three to five new cases with a pace in the prose ("about two minutes each; say the reasoning aloud first"; lessons have no clock); and a `transfer` screen that is the follow-up: the same idea extended the way an interviewer extends it, with one sentence on a desk use. Every case ends with the general principle in one sentence. Each lesson file meets `docs/LEVEL-BRIEF.md`: 8 to 12 screens, at most two non-task screens, difficulty 1 to 3 across the screens, 3 to 5 quiz items at difficulty 2 to 3 with static canvases or none. A drill whose answers are all numbers shares one `table` screen and one Check.

Grading. An argument is never graded free-form. Use `order` with `distractors` (a plausible flawed step, each with a `why`) for pipelines and for lines of code; `choice` (with `shuffle: true`) or `multi` for "which", "can this happen", "is it safe"; `numeric` for counts, bytes, nanoseconds and sizes (`accept` states the form); `table` for offsets, byte maps and tallies; `tap-regions` on a `console` (lines `l1`, `l2`), an `array` (cells `c0`, `c1`) or a `grid` for "tap the line, the byte, the step"; the `interleave` canvas for races. Whole arguments go to `longform` homework items with a 10-point rubric and a full model answer: the prose tells the learner to say the answer aloud, timing themselves, then open the model and tick the rubric. No audio is recorded.

Tags. Every drill screen, review item and homework item carries `"tags": ["<family>"]` (kebab-case, family first, as listed per lesson) and a `pace` in seconds where the item is a quick check, so the interview bank (E7, built) and the E3 exam draws can use them. Review and homework items carry `skills` (course.json ids: `sy-memory`, `sy-concurrency`, `sy-os`, `sy-latency`); the topic 3.5 exam must cover all four. Skills rule: an item's `skills` are those of its lesson (l1, l2, l4: `sy-memory`; l3: `sy-memory`, `sy-os`; l5: `sy-memory`, `sy-latency`; l6 to l10: `sy-concurrency`; l11, l12: `sy-os`; l13, l14: `sy-os`, `sy-latency`; l15: `sy-latency`, `sy-memory`; l16: `sy-latency`, `sy-concurrency`; l17: `sy-latency`; l18: `sy-latency`, `sy-os`); a mixed item carries both lessons' skills; a homework item carries the skills of its named lesson or, for a whole-level item, of the lessons it draws on. Coverage check for the author: review-1 items 5 and 6 (l3) carry `sy-os` and item 8 (l5) `sy-latency`; every skill appears at least once in each level that teaches it.

Shared runtime facts (checked against `docs/AUTHORING.md` section 3 and the C++ notes).
- C++ runs as `-std=c++17 -O1` under libc++ in debug hardening, in WebAssembly (wasm32). Pointers, `size_t` and `long` are 4 bytes there and 8 on a desktop: every layout exercise here uses only `uint8_t`, `uint16_t`, `uint32_t`, `int32_t`, `uint64_t`, `double` and `char`, whose sizes and alignments agree on both (checked with a wasm32 `static_assert`; see `systems/level1/l4_layout.py`). Say once, in l4, that pointers differ.
- No threads, sockets, files or clocks that count in nanoseconds (`steady_clock` ticks in about 100 µs). Concurrency and OS lessons use listings, the `interleave` canvas and single-threaded code that models the behaviour; level 4 code runs.
- No `try`/`catch`. A `compiles` case can check a snippet (AUTHORING "Compile checks"); see inbox bullet 1 on `<mutex>` and `<atomic>`.
- Functions return `int`, `long long`, `double`, `bool`, `std::string`, `std::vector<int>`, `std::vector<double>`, `std::vector<std::string>`; a struct is built in `setup` and read by member in `call`. Every C++ problem below uses only these shapes and keeps at most 15 tests. Each test below is written as one string "setup; call": the author splits it into `setup`, `call` and a JSON `expect`, splitting after the closing brace where a `for` loop precedes the call (P-pool test 10).
- Python items run in Pyodide 0.27.7 (pure standard library: `csv`, `struct`); data files arrive through E14.

Engine limits to write around (every level): a `derive` screen takes only `expression`, `order` or `choice`; `table` canvases and widgets of five or more columns turn compact at 390 px, so keep tables to 4 columns; `longform` is accepted only in homework and exams; set `shuffle: true` on every `choice` and `multi` except ordered options; grid and array cell text is plain text (no KaTeX); grid ids are one-based (`r1c1`), table ids zero-based (`r0c0`), array ids `c{i}` by displayed index; console line ids `l1`, `l2`; a `pair` stacks two canvases below 480 px; `numeric` accepts decimal, not `0x` hex (inbox bullet 6), so hex answers are asked as decimal bytes.

Canvases that suit this course (checked against `app/js/engine/canvas/README.md` and `README-B.md`): `console` for listings, traces and tool output (`tone`, `shade`, line taps); `array` for memory (`wrap: 8` puts bytes in rows of eight, `pointers` for head and tail, `highlight.ranges` with a `label` for byte fields, `mode: "queue"`); `number-line` with `scale: "log"` for latencies; `bars` with `yScale: "log"`, `showMean` and `hlines` for histograms; `table` for page tables and layouts; `grid` for cache lines and byte maps; `graph` with `directed: true`, `tapEdges` and pill nodes for lock-order graphs and pipelines; `pair` for a listing beside a picture; and the E13 `interleave` canvas for races. Every lesson has a real interactive canvas early.

E items, all as built before these levels are authored (specs in interview-plan section (f) and `docs/BACKLOG-INBOX.md`): E3 exam item banks, E8 C++ drills (timed, filtered), E11 `parts` follow-ups on an item, E13 `interleave`, E14 data files for `code` items. No fallback or workaround is written for any of them. Per level, the "Engine" paragraph says where each is used. The brief assumes the `interleave` canvas supports these steps: load, add, store, fetch-add, lock, unlock, wait (sleeps until a notify that comes after it began) and notify, with a lane that cannot step while it waits on a held lock, a "deadlock" or "asleep" end state, tap-to-mark on a step, and a `derive` of final values; inbox bullet 4 asks the builder to confirm blocked lanes. E13 requirement for the engine pass (stated as acceptance criteria; the level 2 author must not start until the engine pass meets them): (a) the `interleave` step set is load, add, store, fetch-add, lock, unlock, wait and notify, plus conditional steps (U4 "if ok: store, cash out"; U11 `c2` waits only if `c1` saw an empty queue); (b) a lane whose next step is a lock held by another lane is disabled, and a schedule in which no lane can step ends "deadlock"; (c) a wait step sleeps until a notify that begins after it, otherwise the lane ends "asleep forever"; (d) steps can be marked by tapping, and `values.outcomes` gives each reachable final, including the end states "deadlock" and "asleep", with its schedule count, counting only the schedules the rules allow (U6 is 4 complete and 2 deadlock of 6, U7 is 162 complete and 6 deadlock of 168, U11 is 5 awake and 1 asleep of 6; a plain interleaving count of the U7 ring would be 34,650); (e) up to 3 lanes of 4 steps (the U7 ring is 12 steps) with the enumeration cached. A level author states a count such as "of 168" only after the canvas reproduces it. E11 requirement for the engine pass: each part of a `parts` item may be any widget kind (`numeric`, `choice`, `multi`, `table`), graded and revealed in turn; the homework items that mix kinds are hw-1 item 2, hw-2 items 2, 3 and 6, and hw-4 items 2 and 4, each labelled `parts` below without a leading item kind.

Code problems are specified in "Code problems" at the end of this file (starter, solution, hidden tests, checks), one per name `P-...`; drills `D-...`. Python items are in "Python items". Number checks per level are in "Number checks".

## Level 1

You are a content agent on the Zero to Quant build in /home/user/zero-to-quant. Author course `systems` ("Systems for Developer Interviews", topic 3.5), level 1 ("Memory and the machine"): lessons `l1-latency-numbers`, `l2-caches`, `l3-virtual-memory`, `l4-object-layout`, `l5-branches`, plus `review-1.json` and `homework-1.json`, in `app/content/courses/systems/`. Follow `docs/LEVEL-BRIEF.md` exactly and read `docs/AUTHORING.md` in full; use the lesson names, objectives and skill ids in `course.json` exactly (`sy-memory` on all five, plus `sy-os` on l3 and `sy-latency` on l5). Use £ for money and London for distances.

- Context: read the course context above. The learner has `cpp` l7-addresses and l8-stack-and-heap, `cpp-pricing` l9-timing and l10-memory-layout, `ds` l1-arrays-in-memory. Name the free paper once, in l1. Every lesson states its round figures as round, and that the learner should know them to a power of ten, not to the digit.
- l1 (`l1-latency-numbers`, "Numbers every programmer should know"; tags `latency-ladder`, `time-budget`, `light-speed`). Objective (course.json): "Order the costs of a register, cache, memory, disk and network access by powers of ten." Method: know each cost to a power of ten, then divide a time budget by it. Round figures used everywhere in this course: register 0.3 ns (one cycle at 3 GHz); L1 cache 1 ns; L2 4 ns; L3 20 ns; main memory (DRAM) 100 ns; NVMe solid-state read 100 µs; same-data-centre round trip 500 µs; spinning-disk seek 10 ms; London to New York round trip 60 ms. Hook (`order`, no numbers shown): "Order these from fastest to slowest": a register read, an L1 read, a main-memory read, an NVMe read, a disk seek, a London to New York round trip (answer in that order; `distractors` none). Then an `explore` on a `number-line` with `scale: "log"` from 0.1 ns to 100 ms, the six points placed: "How many powers of ten separate an L1 read from a disk seek?" 7 (`numeric`; 1 ns to 10 ms is 10^7). Worked: (1) scale to human time, 1 ns as 1 second, in a `table` widget (columns access, real time, human seconds): DRAM 100 s, NVMe 100,000 s (1 day 3 h 46 min 40 s), disk seek 10,000,000 s (115.7 days), London to New York 60,000,000 s (694.4 days, 1.9 years). (2) a budget: a handler gets 200,000 messages a second, so 1 s / 200,000 = 5 µs each, which is 50 main-memory reads or 5,000 L1 reads (`numeric` 50). (3) light sets a floor: London to Frankfurt is 640 km in a straight line and light in fibre covers about 200,000 km/s, so the round trip is 2 × 640 / 200,000 = 6.4 ms; at the speed of light in air or vacuum (299,792 km/s) it is 4.27 ms, saving 2.13 ms (`numeric` 6.4, then 2.13). Trap (`choice`): "An NVMe read against a main-memory read: how many times slower?" 1,000 (`why` for 10: "You counted one step on the ladder; NVMe is three steps beyond DRAM"; for 100: "That is DRAM against L1"). Edge: the floor is physics, the real figure is higher: London to New York is 5,570 km, so the fibre floor is 55.7 ms against the 60 ms round figure (`numeric` 55.7). Drill (one `table`, pace "about 90 seconds each"; tags `time-budget`): DRAM reads in 5 µs, 50; L1 reads in 1 µs, 1,000; powers of ten from L1 to NVMe, 5; same-data-centre round trips in 60 ms, 120; NVMe reads in one disk seek, 100. Transfer (follow-up): "A London strategy trades on a New York price. What is the least time before that price can reach it?" One way is 5,570 / 200,000 = 27.85 ms in fibre (`numeric`), so the strategy can predict that price but never react to it first (`choice`); one sentence: firms buy shorter paths and faster media because the floor is the whole game. Canvas: `number-line` log, `table`, `console` for nothing.
- l2 (`l2-caches`, "How caches work"; tags `cache-lines`, `stride`, `conflict-misses`, `loop-order`). Objective (course.json): "Predict cache misses from an access pattern and a line size." Method: memory moves in 64-byte lines (8 doubles, 16 ints); an access that finds its line in the cache is a hit, otherwise a miss that loads the line and may evict another (least recently used first). A cache of `n` lines in sets of `w` ways puts line `L` (address / 64) in set `L mod (n / w)`. The hook doubles as the recap: its prose cites `cpp-pricing` l10-memory-layout in one sentence (lines of 64 bytes, 8 doubles, stride) and does not teach it again; the lesson spends its screens on what l10 does not cover: eviction, sets, ways and conflict misses. Hook (`array`, 64 doubles with `wrap: 8` so each row is one line, `tap-regions`): "The cache starts empty. A loop adds a[0] to a[31] in order. Tap every access that misses." Answer c0, c8, c16, c24 (4 misses, 28 hits, 87.5%). Worked: (1) eviction: a cache of 4 lines (fully associative, least recently used out first) and a loop that sweeps 32 doubles (4 lines) three times: 96 reads, 4 misses, all hits after the first sweep; sweep 40 doubles (5 lines) three times and it is 120 reads and 15 misses, because each miss evicts the line the loop needs next (`numeric` 15). (2) two arrays `a` and `b` 256 bytes apart, a loop `a[i] + b[i]` for i = 0 to 7, 16 accesses, a cache of 4 lines: direct-mapped (1 way) misses 16 (both arrays land in the same set and evict each other), 2-way misses 2, and moving `b` 64 bytes further (gap 320) fixes the direct-mapped cache too, 2 misses (`table` widget, 4 columns: gap, ways, misses, hit rate). (3) sets and ways: a cache of 8 lines reading lines 0, 4, 8, 0 (line L goes to set L mod the number of sets): 1 way (8 sets) 4 misses, 2 ways (4 sets) 4, 4 ways (2 sets) 3, 8 ways 3, because lines 0, 4 and 8 share a set until the set is wide enough to hold two of them and the reuse of line 0 (`table` widget, 3 columns: ways, sets, misses). Trap (`choice`): "A loop sweeps 5 lines over and over in a 4-line cache with least recently used eviction. How many line fetches in the second sweep hit?" None (`why` for 4: "You kept four of the five lines, but each miss evicts the line the loop needs next"). Edge: when the data fits the cache the order does not matter: a 64 × 64 matrix is 32 KiB, exactly an L1 cache of 512 lines (32 KiB, 8-way, 64 sets), and both orders miss 512 times. Drill (`table`): stride 4 over 64 doubles, 16 reads, 8 misses; stride 3 over 96 doubles, 32 reads, 12 misses; 5 lines swept three times in a 4-line cache, 15 misses; 4 lines swept three times, 4; lines 0, 4, 8, 0 in a cache of 8 lines with 2 ways, 4 misses, with 4 ways, 3 (`numeric` for each). Transfer (follow-up): the interviewer asks why a lattice stored row by row is slow when walked by column (cpp-pricing l10): a 1,000 × 1,000 matrix of doubles gives 125,000 misses by rows and 1,000,000 by columns, 8 times as many, so 12.5 ms against 100 ms at 100 ns a miss, and no difference at N = 64; one sentence on loop order in a pricer. Canvas: `array`, `grid` for the 4-line cache picture, `table`.
- l3 (`l3-virtual-memory`, "Virtual memory"; tags `page-table`, `tlb`, `page-fault`, `huge-pages`). Objective (course.json): "Explain pages, the TLB and a page fault, and what each costs." Method: a program uses virtual addresses; the hardware splits one into a page number and an offset, looks the page up in a page table to get a frame, and keeps recent lookups in the TLB. Hook (`table` canvas, columns page, frame, present; pages 0 to 2 map to frames 7, none, 9; page size 4,096 bytes): "Translate virtual address 0x2A7C (10,876)." Page 2, offset 2,684, frame 9: 9 × 4,096 + 2,684 = 39,548 (`numeric`). Worked: (1) address 0x1000 is page 1, which is not present: a page fault, which the kernel handles by finding or loading a frame (minor fault about 1 µs; from an SSD a major fault about 100 µs, as in l1). (2) x86-64 uses 48-bit addresses: a 12-bit offset and four 9-bit indexes, so 0x00007F3A1C2D5E48 has offset 0xE48 = 3,656 and indexes 254, 232, 225, 213 (`table` widget, 5 rows); a walk is up to four extra reads, 4 × 100 = 400 ns if none is cached. (3) the TLB: 64 entries cover 64 × 4 KiB = 256 KiB; random reads over a 64 MiB table touch 16,384 pages, so 64 / 16,384 = 0.39% hit the TLB; with 2 MiB pages the table is 32 pages and all fit (reach 128 MiB). Trap (`choice`): "`new double[134217728]` (1 GiB): when does it cost 262 ms?" On first write, one fault per 4 KiB page (262,144 × 1 µs = 262.144 ms), not at the call (`why` for "at the call": "The kernel only reserves addresses; frames arrive when a page is first touched"). Edge: virtual space is larger than RAM and per process: 2^48 bytes is 256 TiB, and two processes may use the same virtual address for different frames. Drill (`table`): 0x3B10 with pages [5, 2, none, 8] gives frame 8, address 35,600 (0x8B10); 0x2000 faults; pages in 64 MiB, 16,384; a 1,536-entry second-level TLB reaches 6 MiB; touching 3 GiB first costs 786,432 faults, 786.4 ms. Transfer (follow-up): "Why does a trading process touch and lock all its memory at start-up?" It moves 786 ms of faults out of the session and removes 1 µs jitter from the hot path; huge pages cut 3 GiB to 1,536 pages. Code: P-translate. Canvas: `table`, `array`, `console`.
- l4 (`l4-object-layout`, "Alignment and object layout"; tags `struct-size`, `padding`, `field-order`, `cache-line-straddle`). Objective (course.json): "Work out a struct's size and padding, and reorder its fields to shrink it." Method: each field sits at the next multiple of its alignment (here equal to its size); the struct's size is rounded up to its largest alignment; sort fields largest first to waste least. Say once that pointers are 4 bytes in this app and 8 on a desktop, so every struct here uses fixed-width fields. Hook (`grid`, 3 rows of 8 cells for 24 bytes, `tap-regions`): `struct { uint8_t a; double b; uint8_t c; }`: "Tap every byte that is padding." r1c2 to r1c8 and r3c2 to r3c8: 14 of 24 bytes (58%). Worked: (1) offsets 0, 8, 16 and size 24 (`table` widget: field, offset, size). (2) reorder `double, char, char`: offsets 0, 8, 9, size 16. (3) the order message `{type u8, seq u32, side u8, id u32, instrument u16, qty u32, price i32, time u32}`: offsets 0, 4, 8, 12, 16, 20, 24, 28, size 32; sorted largest first (`seq, id, qty, price, time, instrument, type, side`) offsets 0, 4, 8, 12, 16, 20, 22, 23, size 24: 25% smaller, 1,000,000 orders 32 MB against 24 MB. Trap (`choice`): "`struct { char; double; char; }`: sizeof?" 24, not 10 (`why` for 10: "You summed the fields; padding is part of the size"). Edge: reordering does not always help: `{1, 2, 4, 8, 1, 2, 4, 8}` bytes is 32 either way, and `{u16, u8}` is 4, not 3. Drill (`table`): `{u8, u16, u8, u32, u8}` 16, best 12; `{1, 8, 1, 8, 1, 8}` 48, best 32; `{u16, u8}` 4; `{double, int}` 16. Transfer (follow-up): "Can I `memcpy` this struct onto the wire?" No: padding and byte order differ by platform, so write the bytes by hand (l14); an array of 24-byte structs also puts 2 of every 8 across a 64-byte line boundary, where 32-byte structs never straddle (`numeric` 2); a `u16` flag appended to the 24-byte message makes the host struct 28 bytes. Code: P-struct-size. Canvas: `grid`, `table`.
- l5 (`l5-branches`, "Branches and prediction"; tags `branch-predictor`, `mispredict-cost`, `branchless`, `data-dependent-branch`). Objective (course.json): "Explain branch prediction and remove a branch from a hot loop." Method: the CPU guesses each branch before it knows the answer; a wrong guess throws away about 15 to 20 cycles of work (we use 5 ns). Model the guess as a two-bit counter 0 to 3, starting at 1, guessing taken at 2 or 3, moving up on taken and down on not taken. Hook (`array` of `T T T N N N`, `tap-regions`): "The counter starts at 1. Tap every step where it guesses wrong." c0, c3, c4 (3 misses). Worked: (1) cost: 3 misses × 5 ns. (2) a branch on random data (`if (x >= 128)`) is wrong about half the time: 1,000,000 elements × 0.5 × 5 ns = 2.5 ms extra, while sorted data is wrong almost never (a seeded run of 10,000 random outcomes gives 5,064 misses, 50.6%; the same sorted gives 2; generator in `systems/level1/l5_branch.py`: x starts at 12345, each step x = (1103515245 × x + 12345) mod 2^31, an outcome is taken when bit 16 of x is set, and "sorted" puts every not-taken before every taken). (3) branchless form `sum += x & -(x >= 128)`; a `console` of a desk run (see below). Trap (`choice`): "When is the branchless loop slower?" On sorted, predictable data (`why` for "never": "The mask does extra work on every element, so it loses when the branch is well predicted"). Edge: at `-O1` the compiler already turned the branch into a conditional move, so sorted and unsorted run the same: this app compiles at `-O1`, so learners cannot see the effect here, which is why the lesson shows a desk run. Desk run (one 2.3 GHz server core, 32,768 random bytes summed 20,000 times, `systems/level1/bench.cpp`, g++ 13.3 and clang++ 18.1; the figures are quoted from that run and are not recomputed in the app or by the level agent; state as one machine, rounded to two figures, never as a promise): `-O0` branch loop 6.3 ns per element unsorted and 1.5 to 1.8 sorted; mask loop 2.2 to 2.5 either way; `-O1` branch loop 0.53 (g++) or 0.32 (clang++) either way. A history `TNTN...` is wrong every time for a two-bit counter (8 of 8) although it is regular; real predictors keep history and learn it. Drill (`table`): `TTTTTTTN` twice, 3 misses; `TTN` ten times, 11; `NTTT`, 2; `TNTNTNTN`, 8; `TTN` three times with a one-bit predictor that starts at not taken 6 against two-bit 4. Transfer (follow-up): a handler branches on message type with 70% adds, 15% cancels, 15% trades in random order: the best guess is wrong 30% of the time, 0.3 × 5 ns = 1.5 ns a message, 200,000 × 1.5 ns = 0.3 ms a second (0.03% of a core): measure before you optimise (`numeric` 1.5). Code: P-mispredicts. Canvas: `array`, `console`.

Level 1 review (`review-1.json`, 9 items, difficulty 2 to 4, interleaving l1 to l5, every item tagged and paced; `longform` is refused in a review):
1. (l1, `order`, tags `latency-ladder`, pace 45) order a register read, an L2 read, a disk seek, a main-memory read, a same-data-centre round trip, an NVMe read: register, L2, DRAM, NVMe, same-data-centre round trip, disk seek.
2. (l1, `numeric`, `time-budget`, 40) one main-memory read (100 ns) per message in a 5 µs budget is what percentage? 2.
3. (l2, `numeric`, `cache-lines`, 60) stride 3 over 96 doubles, cold cache, 64-byte lines: misses? 12 (32 reads).
4. (l2, `choice`, `loop-order`, 40) a row-major 1,000 × 1,000 matrix: which loop nest is fast? Row index outer, column index inner.
5. (l3, `numeric`, `page-table`, 60) page table [5, 2, none, 8], address 0x3B10 (15,120): physical address? 35,600.
6. (l3, `numeric`, `page-fault`, 60) first touch of 2 GiB with 4 KiB pages at 1 µs a fault: milliseconds? 524.288 (524,288 pages).
7. (l4, `numeric`, `struct-size`, 60) `{u8, u16, u8, u32, u8}` sorted largest first: size? 12 (unsorted is 16).
8. (l5, `numeric`, `branch-predictor`, 60) two-bit predictor from 1 on `TTTN` four times: misses? 5.
9. (mixed l4 and l2, `numeric`, `cache-line-straddle`, 45) 24-byte structs from a 64-byte-aligned array: how many of the first 8 cross a line boundary? 2 (indexes 2 and 5).

Level 1 homework (`homework-1.json`, 7 items, difficulty 3 to 5 with a 5, one `longform` with a 10-point rubric and model answer, one `code`; E11 `parts` on items 2, 4 and 6):
1. (d4, `code`, P-cache-sim, tags `cache-lines`) a cache simulator.
2. (d3, E11 `parts`: a to c `numeric`, d `choice`; `latency-ladder`) follow-ups: (a) main-memory reads in one NVMe read, 1,000; (b) in one London to New York round trip (60 ms), 600,000; (c) a handler does 3 main-memory reads a message and one NVMe read per 1,000 messages: average ns a message, 300 + 100,000 / 1,000 = 400; (d) how many times the NVMe share (100 ns) is the DRAM share (300 ns)? One third (`choice`).
3. (d4, `longform`, `latency-ladder`) "Say aloud, in two minutes, what happens from `a[i]` in your code to the value arriving": the model covers virtual address, TLB, page walk, L1 to L3, DRAM, with the round figures; rubric 10 points (virtual to physical 2, TLB hit or walk with cost 2, cache lines of 64 bytes 2, the three cache levels and DRAM with figures 2, a fault or a miss to disk with its cost 1, a closing sentence on why layout matters 1).
4. (d4, `numeric` with `parts`, `loop-order`) 1,000 × 1,000 row order 125,000 misses; column order 1,000,000; the cost at 100 ns a miss 12.5 ms and 100 ms; at 64 × 64 both orders 512.
5. (d4, `table`, `struct-size`) `{u8, u64, u8, u16}`: offsets 0, 8, 16, 18, size 24; sorted `{u64, u16, u8, u8}`: offsets 0, 8, 10, 11, size 16.
6. (d5, `numeric` with `parts`, `tlb`) a handler reads a 256 MiB table at random; each read costs 100 ns plus, on a TLB miss, a 30 ns walk (stated as an assumption); 64 TLB entries. (a) TLB hit rate with 4 KiB pages, 64 / 65,536 = 0.098%; (b) average read cost, 100 + 0.999 × 30 = 129.97 ns; (c) with 2 MiB pages (128 pages, hit rate 50%) 115 ns, 11.5% faster.
7. (d3, `choice`, `mispredict-cost`) a handler's `if (type == 'A')` on a 70/15/15 mix: should you rewrite it branchless? No, 1.5 ns of 5,000 ns is 0.03%; measure first.

Engine (level 1). E3: the review and homework `tags` above are the draw keys; `bank/systems-1.json` (written by a later bank session, `role: ["developer"]`, `style: "coding"`, `requires` the named lessons, no `code` items) has these families: `latency-ladder` (l1), `cache-lines` and `loop-order` (l2), `page-table` (l3), `struct-size` (l4), `branch-predictor` (l5), six items from the numbers above; `topic-3.5` and `mock-superday-developer` draw from it. E8: none in this level (its code problems stay lesson screens; the `sy-bits` drill, below, suits l4 afterwards). E11: homework items 2, 4 and 6. E13: none. E14: none. Existing features used: `order`, `numeric`, `table`, `tap-regions` on `array`, `grid` and `console`, `choice`, `multi`, `code` (C++), `longform`, `number-line` log scale, `tags`, `pace`.

## Level 2

You are a content agent on the Zero to Quant build in /home/user/zero-to-quant. Author course `systems`, level 2 ("Concurrency"): lessons `l6-threads`, `l7-data-races`, `l8-locks-and-deadlock`, `l9-atomics`, `l10-producer-consumer`, plus `review-2.json` and `homework-2.json`, in `app/content/courses/systems/`. Follow `docs/LEVEL-BRIEF.md` and `docs/AUTHORING.md`; skill id `sy-concurrency` on all five. Do not start this level until the engine pass has met the E13 requirement stated in the shared "E items" paragraph above (conditional steps, lock, wait and notify steps, blocked lanes and their end states, `values.outcomes` counts). Read the E13 `interleave` entry in `app/js/engine/canvas/README-B.md` (or wherever the builder documented it) for its exact parameter names; this brief gives lanes, shared variables, marks and outcomes in words, and every set of outcomes below was enumerated twice (below).

- Context: the learner has `cpp` l7 to l9, `ds` l11-first-in-first-out, level 1 of this course (cache lines, l2; the 60 ns cost of a line that moves between cores is introduced here, not there). The C++ runtime has no threads: every race is shown on the `interleave` canvas or in a listing, and every code problem models the behaviour on one thread. Name the cppreference thread pages once, in l6. Round figures for this level, stated as assumptions: create a thread 15 µs; thread stack 8 MiB of address space; uncontended mutex lock and unlock 25 ns; uncontended atomic add 5 ns; an atomic add whose cache line moves between cores 60 ns; a mutex acquisition that has to sleep and wake 5 µs; a plain add in L1 1 ns.
- E13 uses (each is an `interleave` canvas; "lanes" are the threads; a step is one numbered operation; the final-value `derive` and the answer sets are keyed by the enumeration in `systems/level2/interleave.py`, run as `python3 -I interleave.py`; `more.py` adds the last two):

| Use | Where | Lanes (steps) | Shared | Reachable finals (interleavings) | Mark to tap |
| --- | --- | --- | --- | --- | --- |
| U1 | l6 worked 3 | A: load r from total, add r 10, store total from r; B: the same with 26 | total = 0 | 10 (9), 26 (9), 36 (2) of 20 | the three steps on `total` of either lane |
| U2 | l7 hook | A and B each: a1 load r from x, a2 add r 1, a3 store x from r (b1 to b3) | x = 0 | 1 (18), 2 (2) of 20 | a1 and b1, the loads that both read 0 |
| U3 | l7 worked 2 | three lanes of the U2 program | x = 0 | 1 (1,404), 2 (270), 3 (6) of 1,680 | the last load that read a stale value |
| U4 | l7 worked 3 | each lane: check (load r from bal, ok = r at least 80), act (if ok: store bal = r - 80 and cash out 80) | bal = 100 | (bal 20, cash 80) 2, (bal 20, cash 160) 4 of 6 | the check of the lane that acts second |
| U5 | l8 hook | each lane: lock m, load, add 1, store, unlock m | x = 0, m free | 2 only (2 schedules: whichever lane takes m first) | none (the lane waiting on m is the lesson) |
| U6 | l8 worked 2 | T1: lock A, lock B, unlock B, unlock A; T2: lock B, lock A, unlock A, unlock B | A and B free | complete 4, deadlock 2 of 6 | the second lock step of each lane |
| U7 | l8 worked 3 | same order (T1 and T2 both A then B) 2 complete; a ring (A,B), (B,C), (C,A) 162 complete and 6 deadlock of 168; the ring broken (third lane takes A then C) 142 complete, 0 deadlock | | as listed | the lane step to reorder |
| U8 | l9 hook | each lane: fetch-add x 1 (one step); then three lanes | x = 0 | 2 (2 schedules); 3 (6) | none |
| U9 | l9 worked 2 | A: x = 1, then r1 = y; B: y = 1, then r2 = x (the store-buffering test) | x = 0, y = 0 | (r1, r2) = (0, 1) 1, (1, 0) 1, (1, 1) 4 of 6; (0, 0) 0 | the step that reads a value written later |
| U10 | l9 worked 3 | writer: data = 42, ready = 1; reader: r1 = ready, r2 = data | both 0 | (0, 0) 1, (0, 42) 4, (1, 42) 1; with the writer's two stores swapped (0, 0) 2, (0, 42) 1, (1, 0) 1, (1, 42) 2 | the reader's step that sees ready = 1 |
| U11 | l10 hook | consumer: c1 check queue empty, c2 wait if it was empty; producer: p1 push, p2 notify | q = 0 | consumer ends awake 5, asleep forever 1 of 6 (order c1 p1 p2 c2) | p2, the notify that nobody hears |

Other enumerated sets used in text: a position of 500 changed by +100 on one lane and -300 on the other (the U2 program with different amounts) ends 200 (9), 300 (2) or 600 (9) of 20; two lanes each doing `if flag is 0 then set it to 1 and enter` as separate check and set: both enter in 4 of 6, one in 2; `x = x + 1` written as a load step and a store step on an atomic ends 1 in 4 of 6 and 2 in 2; the condition-variable fix (lock held across the check and the wait, which releases it as it sleeps) has 5 schedules and 0 end asleep.

- l6 (`l6-threads`, "Threads and what they share"; tags `thread-shared-state`, `thread-cost`, `stack-per-thread`). Objective (course.json): "Say what threads share and what each one owns." Method: threads of one process share code, globals, the heap and open files; each owns a stack, registers and `thread_local` variables. Hook (`console` listing, `tap-regions`): lines `int total = 0;` (l1), `std::vector<int> data(1000);` (l2), `void worker(int id) {` (l3), `int local = 0;` (l4), `static int calls = 0;` (l5), `thread_local int mine = 0;` (l6), `int* p = new int(id);` (l7): "Tap every variable that two threads running `worker` both reach." l1, l2, l5 (the block `p` points to is private unless `p` is shared). Worked: (1) the hook. (2) a thread per message: 15 µs × 200,000 a second = 3.0 cores a second, so use a pool; the stacks alone would be 8 MiB × 1,000 threads = 7.8 GiB of address space (reserved, not touched: level 1 l3). (3) U1: each thread sums its own half in a local, only the final merge touches `total`: 1 + 2 + 3 + 4 = 10, 5 + 6 + 7 + 8 = 26, and the merge can end at 10, 26 or 36. Trap (`choice`): "`static int calls` inside a function: how many copies?" One for the whole process (`why` for "one per thread": "That is `thread_local`; `static` is shared"). Edge: a lambda that captures a local by reference and runs on another thread shares it, and it may be gone by then. Drill (`table`, tags `thread-shared-state`): snippet 2 (`static std::atomic<int> hits;`, `thread_local std::vector<int> scratch;`, `std::mutex m;`, `int n = 8; auto f = [&n] { ++n; };`) shared 3 (hits, m, n); snippet 3 (`const int kLimit = 100;`, `char buffer[64];` global, a loop `int i`) shared 2 (kLimit is shared but read-only, so safe). Transfer (follow-up): "Sum a million doubles with four threads": a shared atomic per element, serialised at 60 ns, is 1,000,000 × 60 ns = 60 ms; four local sums of 250,000 at 1 ns are 0.25 ms each, in parallel, then 3 adds: 240 times faster (`numeric` 240). Canvas: `console` with `tap-regions`, `interleave` U1.
- l7 (`l7-data-races`, "Data races"; tags `lost-update`, `check-then-act`, `race-outcomes`, `ub-race`). Objective (course.json): "Find a data race by stepping two threads through an interleaving." Method: two threads that touch the same variable with no ordering between them, at least one writing, are a data race; to find what can happen, list every interleaving of the steps. Hook (U2, tap-to-mark): "Step the lanes in any order so that x ends at 1. Tap the two steps that read the old value." a1 and b1 (both read 0). Worked: (1) U2 counted: 20 interleavings, 18 end at 1 and only 2 (one lane entirely before the other) end at 2 (`numeric` 18). (2) U3: three lanes, 1,680 interleavings (9 factorial over 3 factorial cubed), 1,404 end at 1, 270 at 2, 6 at 3 (the 6 serial orders, 3 factorial) (`multi`: which finals are possible: 1, 2, 3, not 0 or 4). (3) U4 check-then-act: balance £100, two withdrawals of £80: in 4 of 6 interleavings both check before either acts, so £160 comes out of an account of £100 and the balance still ends at £20. Trap (`choice`): "`x++` compiles to one instruction, so two threads cannot interleave inside it": false (`why` names a load-add-store on most machines, and that the language says a race is undefined behaviour either way). Edge: both lanes read, yet the final can still be 2 (2 of 20), so a test that passes is not a proof; and a race on a plain `bool done` flag may let the compiler read it once and spin forever. Drill (`table`, tags `race-outcomes`, pace "two minutes each"): two lanes, two increments each (12 steps): 924 interleavings (12 factorial over 6 factorial squared), of which 702 end at 2, 216 at 3 and 6 at 4 (`numeric` for 924, 702, 6). Transfer (follow-up): a position of 500 shares with a fill of +100 on one thread and a sale of 300 on another (the U2 program): finals 200, 300, 600 with counts 9, 2, 9; "so which fix?" an atomic add (l9) or a mutex (l8) (`choice`). Code: P-final-counts. Canvas: `interleave` U2, U3, U4; `table`.
- l8 (`l8-locks-and-deadlock`, "Mutexes and deadlock"; tags `mutex-critical-section`, `lock-order`, `deadlock-conditions`, `scoped-lock`). Objective (course.json): "Protect shared data with a mutex and avoid deadlock by fixing the lock order." Method: a mutex lets one thread at a time into a critical section; two threads that each hold a lock the other wants wait forever, so every thread takes locks in one fixed order. Hook (U5): "Try to make x end at 1." Impossible: the second lane cannot step while the first holds the mutex; 2 schedules, both end at 2. Worked: (1) cost: 4,000,000 locked increments cost 4,000,000 × 25 ns = 0.1 s uncontended, and if every acquisition had to sleep, 4,000,000 × 5 µs = 20 s: keep critical sections short. (2) U6: two locks in opposite orders, 6 schedules, 4 finish and 2 deadlock (each lane holds one lock and waits for the other); the four conditions for deadlock (mutual exclusion, hold and wait, no pre-emption, circular wait), and the cure by removing the cycle. (3) the lock-order graph (`graph`, `directed: true`, nodes A, B, C, edges A to B, B to C, C to A, `tapEdges`): "The third thread takes C then A. Tap the edge that, reversed, removes the cycle." e-C-A (the third thread takes A then C, U7: 142 schedules, 0 deadlock). Trap (`choice`): "Which can deadlock: `lock(a); lock(b);` in two functions with the arguments swapped, or `std::scoped_lock lk(a, b);` in both?" The first (`why` for the second: "scoped_lock takes both with a deadlock-avoiding algorithm, whatever the argument order"). Edge: locking the same non-recursive mutex twice deadlocks one thread alone (a lock-order graph with an edge from A to A). Drill (`table`, tags `lock-order`; 1 means a cycle, 0 none): threads {AB, BA} 1; {AB, BC, AC} 0; {AB, BC, CD, DA} 1; {ABC, BCD, ACD} 0. Transfer (follow-up): a `transfer(from, to, amount)` that locks `from` then `to` deadlocks when two transfers go in opposite directions; fix by locking the lower account id first or with `scoped_lock`; with correct locking, accounts of £100 and £100, £10 moved one way and £5 the other, end at £95 and £105 (`numeric` 95, 105). Code: P-lock-cycle. Canvas: `interleave` U5 to U7, `graph`.
- l9 (`l9-atomics`, "Atomics and memory order"; tags `atomic-counter`, `memory-order`, `litmus`, `lock-free`). Objective (course.json): "Use an atomic counter and say what each memory order guarantees." Method: an atomic operation is one indivisible step; a memory order says which other writes and reads it orders around itself: `relaxed` only atomicity, `acquire` and `release` a hand-off (everything written before a release store is visible to a thread that acquire-loads it), `seq_cst` one global order (the default). Hook (U8): "Two lanes each fetch-add 1. Can an update be lost?" No: 2 schedules, both end at 2; three lanes, 6 schedules, all end at 3. Worked: (1) cost: 4,000,000 atomic adds at 5 ns uncontended is 0.02 s, but if the line moves between cores at 60 ns each it is 0.24 s, and per-thread counters at 1 ns are 4 ms: shard hot counters. (2) U9, the store-buffering test: in any interleaving the outcomes are (0, 1), (1, 0) or (1, 1), never (0, 0); but real hardware, and `relaxed` atomics, can give (0, 0) because a store waits in a buffer (`multi`: which pairs are possible in an interleaving; then `choice`: with `seq_cst` can (0, 0) occur? no). (3) U10: with `data` written before `ready` the reader never sees (1, 0) in an interleaving, and with release on the `ready` store and acquire on its load that holds on every machine; with `relaxed` on both, (1, 0) is allowed. Trap (`choice`): "`if (x.load() == 0) x.store(1);` on an atomic: safe?" No, a check-then-act: both lanes enter in 4 of 6 schedules (use `compare_exchange`). Edge: `x++` on a `std::atomic<int>` is one atomic add, while `x = x + 1` is a load and a store: it ends at 1 in 4 of 6 and at 2 in 2. Drill (`table`): U9's three outcomes with counts 1, 1, 4 (`numeric`: the chance of (1, 1) if the 6 interleavings are equally likely, 0.667); which orders forbid (0, 0): `seq_cst` on all four accesses. Transfer (follow-up): a one-producer one-consumer flag: the producer writes an order then sets `ready` with release, the consumer reads it with acquire; `relaxed` is not enough, and on x86 a `seq_cst` store compiles to an exchange (about 20 cycles) where a release store is a plain move (1 cycle). Canvas: `interleave` U8, U9, U10; `table`; listings in `console`.
- l10 (`l10-producer-consumer`, "A producer and a consumer"; tags `condition-variable`, `lost-wakeup`, `spurious-wakeup`, `bounded-queue`). Objective (course.json): "Pass work between threads with a queue and a condition variable." Method: a queue guarded by a mutex, with a condition variable the consumer waits on while the queue is empty and the producer notifies after a push; the check and the wait must happen under the same lock, and the check is a `while`. Hook (U11): "Find the order in which the consumer sleeps forever." c1 p1 p2 c2 (tap p2, the notify nobody hears); 1 of 6. Worked: (1) the fix, lock held across check and wait: 5 schedules, 0 asleep. (2) `if` against `while`: two consumers, one item, `notify_all`: the second pops an empty queue unless it re-checks (`order` with `distractors` for a consumer loop: lock, while empty wait, pop, unlock; distractors `if` instead of `while`, and wait without the lock). (3) bounded queue: a full queue blocks the producer, an empty one the consumer (`table`: `blocked_counts`-style tallies by hand). Trap (`choice`): "A consumer polls with `sleep(1 ms)` instead of a condition variable: how long can an item wait?" Up to 1 ms (average 0.5 ms, 5,000 main-memory reads). Edge: shutdown: the producer sets `done` and notifies all, and the wait predicate must test `done` too, or the consumer sleeps forever. Drill (`table`): `blocked_counts(2, "PPPPCC")` gives {2, 0, 0}; `(1, "PPCCPC")` {1, 1, 0}; wake from sleep 5 µs against a spin 0.1 µs, 50 times; a spinning consumer holds 1 of 8 cores, 12.5%. Transfer (follow-up): why hot threads spin instead of waiting: a wake costs 5 µs, the whole per-message budget of level 1; spin first, then sleep. Canvas: `interleave` U11, `console` listing.

Level 2 review (`review-2.json`, 9 items):
1. (l6, `multi`, `thread-shared-state`, pace 60) which of `static std::atomic<int> hits`, `thread_local std::vector<int> scratch`, `std::mutex m`, a local `int n` captured by reference are shared? hits, m, n.
2. (l6, `numeric`, `thread-cost`, 45) a thread per message at 15 µs and 100,000 messages a second: cores? 1.5.
3. (l7, `numeric`, `race-outcomes`, 45) two lanes of load, add, store: how many of the 20 interleavings end at 2? 2.
4. (l7, `multi`, `race-outcomes`, 45) three such lanes: which finals are possible? 1, 2, 3.
5. (l8, `choice`, `lock-order`, 60) threads {AB, BC, CA}: can they deadlock? Yes (a cycle); reverse one thread's order.
6. (l8, `numeric`, `deadlock-conditions`, 45) two locks in opposite orders: how many of the 6 schedules deadlock? 2.
7. (l9, `multi`, `litmus`, 60) the store-buffering test, if the four steps run one at a time in some order (no store buffer): which pairs (r1, r2) can occur? (0, 1), (1, 0), (1, 1); not (0, 0). The real-hardware (0, 0) is homework item 6.
8. (l10, `choice`, `lost-wakeup`, 60) why a consumer can sleep forever: check and wait not under one lock; the notify arrived in between.
9. (mixed l9 and l2, `numeric`, `atomic-counter`, 45) two counters on one 64-byte line, each incremented by its own thread: cost per add 60 ns against 1 ns on separate lines: how many times slower? 60.

Level 2 homework (`homework-2.json`, 7 items, difficulty 3 to 5; E11 `parts` on 2, 3 and 6):
1. (d3, `code`, P-blocked-counts, `bounded-queue`).
2. (d4, E11 `parts`: a, c, d `numeric`, b `multi`; `race-outcomes`) position 500, +100 and -300: (a) interleavings, 20; (b) possible finals (`multi`), 200, 300, 600; (c) how many end at 600, 9; (d) after an atomic add on each lane the final is always 300.
3. (d4, E11 `parts`: a, c, d `choice`, b `numeric`; `lock-order`) a transfer deadlock: (a) does {AB, BA} have a cycle, yes; (b) schedules that deadlock, 2 of 6; (c) does locking the lower id first give {AB, AB}, no cycle; (d) which standard-library lock takes both at once, `std::scoped_lock`.
4. (d5, `longform`, `lost-wakeup`) "Say aloud, in three minutes, the lost wakeup and how a consumer loop avoids it": model answer with the 1-in-6 schedule, check and wait under one lock, the `while`, the notify after the push; rubric 10 (the failing order 3, why the lock fixes it 2, the `while` and spurious wakeups 2, shutdown 1, a cost comparison with polling and spinning 2).
5. (d4, `order`, `condition-variable`) order the lines of a correct consumer (lock, while empty wait, pop, unlock) among distractors.
6. (d5, E11 `parts`: a `multi`, b and d `choice`, c `numeric`; `litmus`) the store-buffering test: (a) outcomes in an interleaving, 3; (b) (0, 0) with relaxed atomics, possible; (c) chance of (1, 1) with 6 equally likely interleavings, 0.667; (d) the order that forbids (0, 0), `seq_cst`.
7. (d3, `numeric`, `atomic-counter`) 8 threads each add 500,000 times: a contended atomic at 60 ns serialised takes 0.24 s; per-thread counters at 1 ns take 0.5 ms; 480 times faster.

Engine (level 2). E13: the requirement stated in the shared "E items" paragraph above must be met first, then U1 to U11 above, 11 uses in 5 lessons (l6 1, l7 3, l8 3, l9 3, l10 1), each with its lanes, shared variables and reachable finals listed. E3: tags `thread-shared-state`, `race-outcomes`, `lock-order`, `litmus`, `lost-wakeup` for `bank/systems-2.json`. E11: homework 2, 3, 6 (kinds mixed, see the E11 requirement above). E8, E14: none. Existing features used: `console` with `tap-regions`, `graph` directed with `tapEdges`, `table`, `order` with `distractors`, `multi`, `choice`, `numeric`, `code` (C++), `longform`.

## Level 3

You are a content agent on the Zero to Quant build in /home/user/zero-to-quant. Author course `systems`, level 3 ("Operating systems and networks"): lessons `l11-processes`, `l12-files-and-sockets`, `l13-tcp-and-udp`, `l14-messages-on-the-wire`, plus `review-3.json` and `homework-3.json`, in `app/content/courses/systems/`. Follow `docs/LEVEL-BRIEF.md` and `docs/AUTHORING.md`; skills `sy-os` on l11 and l12, `sy-os` and `sy-latency` on l13 and l14.

- Context: the learner has level 1 (virtual memory and the latency ladder), level 2 (threads, l6), `terminal` l7-looking-inside, and `cpp` l7. The runtime has no sockets or files, so this level is `console` traces, `order` pipelines, `array` byte pictures and arithmetic; the only running code is P-find-gaps and P-wire (C++) and one Python item (E14). Name Beej's guide and the manual pages once, in l11. Round figures, stated as assumptions: a system call (user to kernel and back) 0.2 µs; a thread context switch 2 µs; a wake-up from a blocking read about 5 µs; the kernel receive path for one packet about 10 µs, a kernel-bypass path about 1 µs; `clock_gettime` through the shared-page shortcut about 20 ns; a UDP datagram of 1,500 bytes carries 1,472 bytes of payload. Straight-line London to New York 5,570 km, fibre 200,000 km/s. Traces in `console` are abbreviated and invented in our own words (never a real log); say so.
- l11 (`l11-processes`, "Processes and system calls"; tags `syscall-cost`, `context-switch`, `process-vs-thread`, `fd-table`). Objective (course.json): "Explain a process, a system call and a context switch, and what each costs." Method: a process is a program with its own address space and file-descriptor table; a system call asks the kernel to act and returns to the same thread; a context switch changes which thread runs. Hook (`console` of an invented `strace -T` run, `tap-regions`): lines `socket(AF_INET, SOCK_DGRAM, 0) = 3 <0.000012>`, `bind(3, ...) = 0 <0.000008>`, `recvfrom(3, ..., 1500, 0, ...) = 24 <0.012340>`, `write(1, "24 bytes\n", 9) = 9 <0.000010>`: "Tap the call where the program waits." The `recvfrom` line (the thread slept until a packet arrived). Worked: (1) read 1 MiB: with 64-byte reads 16,384 calls, 3,276.8 µs of call overhead at 0.2 µs; with 4 KiB reads 256 calls, 51.2 µs; with 64 KiB reads 16 calls, 3.2 µs: batch your reads (1,024 times fewer calls than 64 bytes). (2) a thread that sleeps on a socket and is woken per message costs two context switches, 2 × 2 = 4 µs, which at 100,000 messages a second is 40% of a core. (3) threads share an address space, processes do not: switching process changes the page table, which costs more (state it qualitatively, no figure beyond the 2 µs for threads), and a child made with `fork` shares frames copy-on-write until either writes. Trap (`choice`): "Is a system call a context switch?" No: the thread does not change, only its privilege level does (`why` for "yes": "The kernel runs on your thread's behalf; no other thread was scheduled"). Edge: some calls need no kernel entry: reading the clock through the shared-page shortcut costs about 20 ns, not 200. Drill (`table`, tags `syscall-cost`): 4 MiB read in 4 KiB chunks, 1,024 calls, 204.8 µs; 8 MiB in 4 KiB chunks 2,048 calls, 409.6 µs; in 64 KiB chunks 128 calls, 25.6 µs; one wake per message at 100,000 a second, 0.4 of a core. Transfer (follow-up): "Your handler calls `recv` for every 24-byte message at 200,000 a second": 200,000 × 0.2 µs = 40 ms a second, 4% of a core; if the sender packs 61 frames to a datagram (1,472 / 24 = 61 remainder 8) that is 3,279 calls a second. Canvas: `console`, `table`.
- l12 (`l12-files-and-sockets`, "Files and sockets"; tags `read-path`, `partial-read`, `blocking-vs-polling`, `copy-count`). Objective (course.json): "Follow a read from a socket through the kernel into user space." Method: a file, a pipe and a socket are all file descriptors read with `read` or `recv`; `recv(fd, buf, n)` returns between 0 and `n` bytes, never promising `n`. Hook (`order`, no distractors): "Put a received packet's journey in order": the network card writes the frame to memory; the card signals the kernel; the kernel's network stack checks the packet and finds the socket by port; the data joins the socket's buffer and the sleeping thread is woken; the scheduler runs that thread; the kernel copies the data into the thread's buffer; `recvfrom` returns the byte count. Worked: (1) two copies (card to kernel memory, kernel to your buffer) and one wake-up: about 10 µs against the 5 µs budget of level 1; a kernel-bypass path puts the frame straight into a user-space ring in about 1 µs. (2) partial reads: a TCP stream carrying 24-byte frames is read in chunks: 100 bytes is 4 frames and 4 bytes left over, 1,000 bytes is 41 frames and 16 left; the leftover waits for the next read (`table`). (3) blocking, non-blocking and busy-polling: blocking sleeps and costs a 5 µs wake; a non-blocking loop returns at once with "would block" each call (0.2 µs per call, one core at 100%). Trap (`choice` with a `console` of returns 24, 100, 0): "`read(fd, buf, 1000)` returned 100. What happened?" Only 100 bytes were ready; call again (`why` for "an error": "A short read is normal; an error returns -1"). Edge: on a TCP socket `recv` returning 0 means the peer closed, not "no data yet". Drill (`table`, tags `partial-read`): reads of [100, 50, 24, 23, 1] bytes with 24-byte frames: whole frames per read 4, 2, 1, 1, 0 and 6 bytes left over at the end, 8 frames in all; reads of [50, 50, 50]: 2, 2, 2 and 6 left. Transfer (follow-up): "Blocking, epoll or busy poll for a 5 µs budget?" Busy poll on a pinned core for the hot path (0.2 µs per empty call, no 5 µs wake), blocking for everything else, and say what the spinning core costs. Canvas: `order`, `console`, `table`.
- l13 (`l13-tcp-and-udp`, "TCP, UDP and multicast"; tags `tcp-handshake`, `head-of-line`, `udp-multicast`, `ab-feeds`). Objective (course.json): "Choose between TCP, UDP and multicast for orders and for market data." Method: TCP gives one ordered, reliable stream (it retransmits and holds later data behind a gap); UDP sends independent datagrams with no promise; multicast sends one datagram to every subscriber; so orders usually use a reliable ordered session and market data usually uses UDP multicast with sequence numbers. Hook (`array`, `indexFrom: 1`, ten messages with message 3 shaded lost, `tap-regions`): "TCP delivers in order. Tap every message it holds back until message 3 is resent." c4 to c10 (7 messages; UDP would deliver all but message 3). Worked: (1) handshake: with a 60 ms round trip, TCP's first data reaches the server at 90 ms (SYN out 30, SYN-ACK back at 60, data out with the ACK, arrives at 90), UDP's at 30 ms (`numeric`). (2) head-of-line blocking: at 100,000 messages a second, a lost packet repaired in one data-centre round trip (0.5 ms) delays 50 messages; if the retransmission timer (about 200 ms on Linux) has to fire, 20,000. (3) multicast: 50 subscribers, 1,000 messages of 100 bytes a second: unicast 5,000,000 bytes a second (40 Mbit/s) against 100,000 (0.8 Mbit/s), 50 times; two feeds A and B each lose 1% of 1,000,000 messages independently, so one feed misses 10,000 and both miss 1,000,000 × 0.01 × 0.01 = 100 (a seeded simulation gave 87, within its error). Trap (`choice`): "Why can UDP deliver a price sooner than TCP?" It skips the handshake and never waits behind a retransmission (`why` for "its packets travel faster": "The wire is the same; the saving is waiting, not speed"). Edge: arrival order is not send order: `{1, 3, 2}` has no gap, and duplicates from the second feed must be dropped. Drill (`table`, tags `ab-feeds`): missing counts for `{1, 2, 4, 5}` 1, `{1, 5}` 3, `{3, 1, 2, 6, 5}` 1, `{1, 2, 3, 7, 8, 10}` 4. Transfer (follow-up): "Why set `TCP_NODELAY` on an order connection?" Small writes are held back by a rule that waits for an acknowledgement, and a delayed acknowledgement can hold a 24-byte order for tens of milliseconds (about 40 ms on Linux) (`choice`). Code: P-find-gaps. Canvas: `array`, `table`, `console`.
- l14 (`l14-messages-on-the-wire`, "Messages on the wire"; tags `wire-layout`, `endianness`, `fixed-point-price`, `partial-frame`). Objective (course.json): "Encode a market data message in a fixed binary layout and parse it back." Method: a wire format fixes every field's offset, size and byte order, and is written and read byte by byte, never by copying a struct. The format in this course (invented, 24 bytes, big-endian, most significant byte first): offset 0 type (1 byte, 65 add, 88 cancel, 84 trade), 1 side (66 buy, 83 sell), 2 instrument (2), 4 sequence (4), 8 order id (4), 12 quantity (4), 16 price (4, signed, in pence), 20 time (4, milliseconds since midnight). Hook (`array`, `wrap: 8`, hex bytes `41 42 01 02 00 01 11 70 07 5b cd 15 00 00 00 64 00 00 28 23 02 25 51 00`, `highlight.ranges` labelled by field once the layout is shown, `tap-regions`): "The sequence number is 70,000. Tap the four bytes that hold it." c4 to c7 (`00 01 11 70`); then `numeric`: 0x00011170 is 70,000. Worked: (1) byte order: 258 as a 2-byte big-endian field is `01 02`, little-endian `02 01`; a little-endian machine's `memcpy` writes the second. (2) fixed point: £102.75 is 10,275 pence, `00 00 28 23`; never a double on the wire; -25 pence is `ff ff ff e7` (2^32 - 25); 36,000,000 ms is 10:00:00, `02 25 51 00`. (3) a stream of frames: 200,000 messages a second is 4,800,000 bytes (38.4 Mbit/s); a datagram holds 61 frames (1,472 / 24, remainder 8). Trap (`choice`): "Can I `memcpy` the struct onto the socket?" No: padding, field order and byte order are the compiler's and the CPU's, not the protocol's. Edge: `80 00 00 00` is -2,147,483,648 as a signed price, and `ff ff ff ff` is 4,294,967,295 as a sequence number. Drill (`table`, tags `endianness`): `00 00 28 23` is 10,275; `ff ff ff e7` is -25; `00 00 01 00` is 256 big-endian and 65,536 little-endian; a 1,000-byte read holds 41 frames and 16 bytes. Transfer (follow-up): "Add a 2-byte flags field": the wire frame becomes 26 bytes and the host struct 28 (padding to 4), so a parser must not assume the frame size is the struct size. Code: P-wire. Canvas: `array`, `table`.

Level 3 review (`review-3.json`, 9 items):
1. (l11, `numeric`, `syscall-cost`, 45) 4 MiB read in 4 KiB chunks at 0.2 µs a call: microseconds? 204.8 (1,024 calls).
2. (l11, `choice`, `context-switch`, 40) is a system call a context switch? No.
3. (l12, `table` of two rows with one `numeric` cell each, `partial-read`, 60) reads of 50, 50 and 60 bytes of 24-byte frames (160 bytes in all): whole frames, then bytes left over? 6 frames (144 bytes), 16 bytes.
4. (l12, `choice`, `partial-read`, 40) `recv` returned 0 on a TCP socket: the peer closed the connection.
5. (l13, `numeric`, `tcp-handshake`, 45) round trip 40 ms: TCP's first data reaches the server after? 60 ms (UDP 20 ms).
6. (l13, `numeric`, `ab-feeds`, 45) `{1, 2, 3, 7, 8, 10}` arrived: missing numbers? 4 (4, 5, 6, 9).
7. (l14, `numeric`, `endianness`, 45) bytes `00 00 01 00` read as big-endian: 256.
8. (l14, `numeric`, `fixed-point-price`, 60) -100 pence as 4 big-endian bytes: the last byte as a decimal? 156 (`ff ff ff 9c`).
9. (mixed l13 and l12, `numeric`, `ab-feeds`, 60) two feeds each lose 2% of 1,000,000 messages independently: messages lost by both? 400.

Level 3 homework (`homework-3.json`, 7 items; E11 `parts` on 2 and 5; E14 on 1):
1. (d3, `code` Python, P-feed-summary with E14 `data: { "feed.hex": "content/data/systems/feed.hex" }`, tags `wire-layout`) parse a hex capture of 201 frames: unique sequence numbers 200, missing `[17, 18, 90, 150, 151, 152]`, trades 31, volume-weighted trade price 10,001.4128 pence. See "Python items".
2. (d3, `numeric` with `parts`, `tcp-handshake`) (a) round trip 80 ms: TCP first data at 120 ms, UDP 40 ms; (b) one loss at 50,000 messages a second repaired in 1 ms: 50 messages held; (c) with a 200 ms timer, 10,000; (d) 20 subscribers, 2,000 messages of 150 bytes a second: unicast 6,000,000 bytes a second, multicast 300,000.
3. (d4, `longform`, `udp-multicast`) "Say aloud, in two minutes, why market data uses multicast with two feeds and orders use a reliable session": rubric 10 (what TCP guarantees and its cost 2, head-of-line blocking with a figure 2, multicast scaling with a figure 2, sequence numbers and gaps 2, A/B arbitration with the 100-against-10,000 figure 1, one risk or caveat 1).
4. (d4, `table`, `wire-layout`) hand-encode type 84, side 83, instrument 12, sequence 300, id 99, quantity 1,000, price -5, time 43,200,000 (12:00:00): the last byte of each field in decimal: instrument 12, sequence 44, id 99, quantity 232, price 251, time 0 (the frame is `54 53 00 0c 00 00 01 2c 00 00 00 63 00 00 03 e8 ff ff ff fb 02 93 2e 00`).
5. (d5, `numeric` with `parts`, `read-path`) a single thread on the kernel path takes 10 µs a message: (a) messages a second, 100,000; (b) on the bypass path at 1 µs, 1,000,000; (c) cores for 200,000 a second on the kernel path, 2.0; (d) reads a second if the sender packs 61 frames to a datagram and you take one datagram a read, 3,279.
6. (d3, `order`, `read-path`) order the steps of a `recv` among distractors ("the program copies the frame itself", "the kernel asks the disk").
7. (d4, `numeric`, `syscall-cost`) 8 MiB read in 4 KiB chunks: 2,048 calls, 409.6 µs; in 64 KiB chunks 128 calls, 25.6 µs.

Engine (level 3). E14: homework item 1 (a Python `code` item whose `data` file is `feed.hex`, 9,849 bytes, 201 lines; spec in "Python items"). E11: homework items 2 and 5. E3: tags `syscall-cost`, `partial-read`, `tcp-handshake`, `ab-feeds`, `wire-layout`, `endianness` for `bank/systems-3.json`. E13, E8: none. Existing features used: `console` (`tap-regions`, `tone`), `order`, `array` with `wrap` and `highlight.ranges`, `table`, `choice`, `numeric`, `code` (C++ and Python), `longform`.

## Level 4

You are a content agent on the Zero to Quant build in /home/user/zero-to-quant. Author course `systems`, level 4 ("Low-latency C++"): lessons `l15-no-allocation`, `l16-ring-buffer`, `l17-measuring-latency`, `l18-feed-handler`, plus `review-4.json` and `homework-4.json`, in `app/content/courses/systems/`. Follow `docs/LEVEL-BRIEF.md` and `docs/AUTHORING.md`; skills `sy-latency` and `sy-memory` on l15, `sy-latency` and `sy-concurrency` on l16, `sy-latency` on l17, `sy-latency` and `sy-os` on l18. This level runs real code.

- Context: the learner has levels 1 to 3 here, `cpp` l8, l9, l14, l15, `cpp-pricing` l9-timing (batch timing, the median) and l11 (`-O1`). Name the conference talks once, in l15. Round figures, as assumptions: a `malloc` or `new` 50 ns (and sometimes microseconds when it asks the system for memory); a pool allocation 2 ns; a message rate of 200,000 a second, 5 µs each; a 24-byte message (l14). Every code screen below is verified; copy starters and tests from "Code problems" exactly, and have the app's own checker confirm each (`node tools/playthrough.mjs --lesson systems/<id>`). Levels 1 to 3 gave the budget (5 µs a message), the line (64 bytes), the wire format and the sequence gaps; this level builds the parts of a handler.
- l15 (`l15-no-allocation`, "No allocation on the hot path"; tags `allocation-cost`, `pool-allocator`, `preallocate`, `alloc-counter`). Objective (course.json): "Remove allocations from a hot path and write a pool allocator." Method: on a hot path every allocation is a cost and a risk, so allocate everything before the first message, from a pool or a fixed array, and count `new` calls in a test to prove it. Hook (`console` listing, `tap-regions`): `void on_message(const Msg& m) {` (l1), `std::vector<int> levels;` (l2), `levels.push_back(m.price);` (l3), `auto* ev = new Event(m);` (l4), `std::string s(100, 'x');` (l5), `std::map<int, int> book; book[m.price] = 1;` (l6), `int x = m.qty * 2;` (l7): "Tap every line that allocates." l3, l4, l5, l6 (an empty vector does not allocate until its first push; four allocations a message). Worked: (1) cost: 4 allocations × 50 ns × 200,000 a second = 40 ms a second, 4% of a core, plus the rare slow one. (2) a pool: slots in a fixed array, a free list threaded through them, `allocate` pops, `release` pushes, 2 ns each, so 3 a message is 1.2 ms a second against 30 (25 times less). (3) count the heap: the hidden `prelude` replaces `operator new` with a counter and the test asserts the count stays 0 across a call (P-format-price, then P-pool). Trap (`choice`): "Which of these allocates: `std::vector<int> v;`, the first `v.push_back(1)`, `std::array<int, 8> a;`, `int b[8];`?" The first `push_back` (`why` for the empty vector: "A default vector owns no memory yet"). Edge: a pool that runs out must not grow on the hot path: `allocate` returns -1 and the caller drops or fails loudly; size it for the worst case. A slot released twice corrupts the free list (a debug build asserts). Drill (`table`, tags `pool-allocator`): a pool of 3: allocate three, release 1, allocate gives 1; allocate three, release 0, release 2, allocate gives 2 (last released, first reused); a fourth allocate on a full pool gives -1. Transfer (follow-up): "How big a pool for 1,000 live orders?" 1,000 × 1.5 safety = 1,500 slots; at 24 bytes that is 36,000 bytes (35.2 KiB), at 32 bytes 48,000 (46.9 KiB): neither fits a 32 KiB L1, but the 24-byte layout of l4 is 25% smaller (`numeric` 36,000). Code: P-format-price, P-pool. Canvas: `console`, `table`.
- l16 (`l16-ring-buffer`, "A ring buffer"; tags `ring-buffer`, `power-of-two-mask`, `false-sharing`, `spsc-order`). Objective (course.json): "Build a fixed-size single-producer, single-consumer ring buffer." Method: a ring of `N` slots (a power of two) with two counters that only grow: the producer owns the tail counter and the consumer the head; the slot is `counter & (N - 1)`; it is empty when head equals tail and full when `tail - head == N`. Hook (`array`, `mode: "queue"`, capacity 4, `pointers` for head and tail): "Push 1, 2, 3, 4, 5 into an empty ring of 4, then pop until empty. Which push fails, and what do the pops return?" The fifth push; 1, 2, 3, 4 (`numeric` for the failing push, 5, then for the third pop, 3). Worked: (1) indices: counter 5 is slot 5 & 3 = 1; with head 13 and tail 20 in a ring of 8 the size is 7 and the next slot is 20 & 7 = 4. (2) counters wrap: an unsigned 32-bit counter wraps at 2^32, and because 2^32 divides evenly by a power of two, `tail - head` and the mask stay right (a `console` listing, not a hidden test, shows `tail - head` staying 2 as the tail goes 4,294,967,294, 4,294,967,295, 0; `size_t` is 4 bytes in this app and 8 on a desktop, so say so and use `unsigned` in the listing), but with capacity 3 and `%`, the counters 4,294,967,295 and 0 both map to slot 0 (2^32 mod 3 is 1): at 10 million operations a second the wrap comes after 429.5 s, so it will happen (`numeric`). (3) false sharing: put the head and tail counters on one 64-byte line and each producer store steals the line from the consumer's core (about 60 ns against 1 ns): `alignas(64)` gives each its own line (a test compares the two addresses). A listing (not run) of the producer's side with `std::atomic` is an `order` task: load tail relaxed, check space against head loaded acquire, write the slot, store tail + 1 with release; distractors: store the tail before writing the slot, store tail relaxed. Trap (`choice`): "Two threads share the ring: does it need a mutex?" Not with one producer and one consumer: each counter has one writer (`why` for "yes, both write the buffer": "They write different slots; the counters hand slots over"). Edge: counters rather than wrapped indexes use all `N` slots, because full and empty are told apart by the difference. Drill (`table`, tags `ring-buffer`): the hidden-driver cases of P-ring by hand (capacity 4, pushes 1 to 5 then five pops: the pushes answer 1, 1, 1, 1, 0 and the pops 1, 2, 3, 4, -1); modulo against mask: a division costs tens of cycles on many CPUs, a mask one. Transfer (follow-up): "Size the ring for a 1 ms consumer stall at 200,000 messages a second": 200 messages, round up to 256 slots, 256 × 24 = 6,144 bytes (in L1); for 5 ms at 1,000,000 a second, 5,000, so 8,192 slots, 196,608 bytes (192 KiB, in L2). Code: P-ring. Canvas: `array`, `console`, `table`.
- l17 (`l17-measuring-latency`, "Measuring latency"; tags `percentile`, `tail-latency`, `coordinated-omission`, `mean-vs-p99`). Objective (course.json): "Measure latency percentiles and say why the mean misleads." Method: report percentiles, not the mean: the p-th percentile of n sorted samples is the value at rank ceil(p × n / 100), counting from 1; the mean hides the tail, and a test client that waits for each reply hides it again. Hook (`bars` with `showMean`, two bars: 990 requests at 10 µs and 10 at 1,000 µs): "What is the mean? How many requests took about that long?" 19.9 µs; none (`numeric` 19.9, then 0). Worked: (1) nearest rank: for the 1,000 samples p50 is 10, p99 is 10 (rank 990), p99.9 is 1,000 (rank 999), max 1,000; with 11 outliers in 1,000 p99 jumps to 1,000 (rank 990 is now an outlier); with 1 outlier p99.9 is still 10 and only the max shows it. (2) `latencies.csv` (E14; 2,000 requests, one every 100 µs, a client that sends the next request when the previous reply arrives, one 50 ms stall at request 1,000): measured as reply minus actual send time, p50 is 40 µs, p99 50 µs, p99.9 248 µs; measured from the time each request should have been sent, p50 is 49 µs, p90 38,308, p99 48,821 and p99.9 49,911, and 875 of the 2,000 requests were late by more than 100 µs: the stall delayed everything queued behind it and the first measure never saw them (this is coordinated omission); see "Python items". (3) timing in code: a clock read costs about 20 ns, so time batches and warm up (`cpp-pricing` l9), and in this app the clock ticks in about 100 µs, so tests here use supplied samples. Trap (`choice`): "Mean 19.9 µs, p99.9 1,000 µs: which do you quote to a trader?" Both, with the tail first (`why` for "the mean, it is the typical case": "No request took 19.9 µs; the mean describes none of them"). Edge: floating point at a rank boundary: p99.9 of 999 samples at 10 and one at 1,000 is rank 999, value 10, but `numpy.percentile(..., 99.9, method="inverted_cdf")` returns 1,000 because 0.999 × 1,000 comes out as 999.0000000000001 and rounds up (checked with NumPy 2.5.3 on a desktop; recheck with the NumPy that Pyodide 0.27.7 ships before stating it): use integer rank arithmetic, as P-percentile (a 1e-9 guard) and the Python solution do. Drill (`table`, tags `percentile`): five samples {5, 1, 4, 2, 3}: p20 1, p50 3, p80 4, p100 5. Transfer (follow-up): "Two hosts report p99 of 10 µs and 1,000 µs: what is the fleet p99?" Not the average, 505: pool the samples. With host A at 1,000 requests of 10 µs and host B at 970 of 10 µs and 30 of 1,000 µs, B's p99 is 1,000, the pooled p99 over 2,000 is 1,000 and the average of the two is 505 (`numeric` 1,000). Code: P-percentile (C++), the latency report (Python, E14). Canvas: `bars`, `table`.
- l18 (`l18-feed-handler`, "Designing a feed handler"; tags `feed-handler-design`, `latency-budget`, `a-b-arbitration`, `book-structure`). Objective (course.json): "Design a market data handler end to end and defend each choice aloud." Method: a handler is a pipeline with a time budget; give each stage a share, make each stage allocation-free and cache-friendly, and handle loss and partial reads explicitly. Hook (`order` with `distractors`): "Order the stages from packet in to order out": network card to a user-space ring; decode the 24-byte frame; check the sequence number; update the book; strategy; encode and send the order; distractors "write the frame to a log file", "allocate an `Event` with `new`". Worked: (1) budget: card to user 1,000 ns, decode 200, book 300, strategy 500, encode and send 500: 2,500 ns against a 3 µs target leaves 500 ns of slack; four allocations at 50 ns add 200 (2,700); one 5 µs stall makes 7,500 (`table` widget, 3 columns). (2) structures: the book as arrays indexed by price tick (201 levels from £99.00 to £101.00 in pence, 9,900 to 10,100) holding quantity per side, and orders in an array indexed by id (below 1,024): `sizeof` the whole handler is 18,032 bytes (1,608 for levels, 16,384 for orders), which fits a 32 KiB L1; best bid by scanning 201 levels is fine at this size (cache the best price if it is not). (3) loss: a sequence number above the expected one counts the gap (policy: apply the frame, count the missing), one below it is a duplicate from the second feed or a late arrival and is dropped; a partial frame waits for its remaining bytes. Trap (`choice`): "Orders in a `std::unordered_map`: why not?" It allocates nodes and rehashes at unpredictable times; an array by id or a preallocated table does not (`why` for "it is slow on average": "Its average is fine; its worst case is the problem"). Edge: a gap while a frame is split across two reads, and two frames in one read. Drill (`table`, tags `latency-budget`): the budget sum 2,500 ns and with four allocations 2,700; 200,000 messages a second is 4.8 MB a second; frames in a 1,000-byte read 41 with 16 left; a datagram of 1,472 bytes 61 frames. Transfer (follow-up): "Now 50 instruments": 50 × 18,032 = 901,600 bytes (880.5 KiB), so the book no longer fits L1 but fits L2; only the touched instrument's slice moves per message. Code: P-handler. Canvas: `graph` with `directed: true` and pill nodes for the pipeline picture, `order`, `table`.

Level 4 review (`review-4.json`, 9 items):
1. (l15, `multi`, `allocation-cost`, 60) which lines allocate: `std::vector<int> v;`, `v.push_back(1);`, `int* p = new int(5);`, `std::string s(100, 'x');`, `int a[4] = {1, 2, 3, 4};`, `std::array<int, 4> b{};`? The `push_back`, the `new` and the long string (three).
2. (l15, `numeric`, `pool-allocator`, 45) pool of 3: allocate three, release 0, release 2, allocate: slot? 2.
3. (l15, `numeric`, `allocation-cost`, 45) 4 allocations at 50 ns, 200,000 messages a second: milliseconds a second? 40.
4. (l16, `table` of two rows with one `numeric` cell each, `power-of-two-mask`, 45) ring of 8, head 13, tail 20: items stored, then the slot of the next push? 7 (20 - 13) and 4 (20 & 7).
5. (l16, `numeric`, `ring-buffer`, 45) pushes 1 to 5 into a ring of 4 then pops: the third pop returns? 3.
6. (l17, `table` of two rows with one `numeric` cell each, `mean-vs-p99`, 60) 990 requests of 10 µs and 10 of 1,000 µs: mean and p99 in µs? 19.9 (19,900 / 1,000) and 10 (the 990th of 1,000 sorted).
7. (l17, `numeric`, `percentile`, 45) samples {5, 1, 4, 2, 3}: p80? 4.
8. (l18, `numeric`, `latency-budget`, 45) stages 1,000, 200, 300, 500, 500 ns plus four 50 ns allocations: total? 2,700.
9. (l18, `numeric`, `partial-frame`, 45) frames of 24 bytes in a 1,472-byte datagram? 61.

Level 4 homework (`homework-4.json`, 6 items; E11 `parts` on 2 and 4):
1. (d4, `code`, P-latency-hist, `percentile`) a fixed-bucket latency histogram with no allocation in `record`.
2. (d5, E11 `parts`: a to d `numeric`, e `choice`; `feed-handler-design`) sizing: (a) pool slots for 1,000 live orders with 1.5 safety, 1,500; (b) bytes at 24 per order, 36,000; (c) ring slots for a 1 ms stall at 200,000 messages a second, rounded to a power of two, 256; (d) bytes at 24 per message, 6,144; (e) does it fit a 32 KiB L1, yes.
3. (d5, `longform`, `feed-handler-design`) "Say aloud, in three minutes, how you would build a handler for one instrument's feed, defending each choice": model answer covers the ring from the network, the decode, the sequence check and A/B arbitration, array-indexed book and orders, no allocation and its proof, a latency budget with figures, how to measure (percentiles, open-loop), what to do on a gap; rubric 10 (pipeline and budget 2, no allocation and a pool or fixed arrays 2, loss and A/B 2, book structure and cache 2, measurement 1, a trade-off named 1).
4. (d4, E11 `parts`: a to c `numeric`, d `choice`; `tail-latency`) two hosts: (a) host A p99 10 µs, host B p99 1,000 µs: the average, 505; (b) pooled p99 of A (1,000 at 10 µs) and B (970 at 10, 30 at 1,000), 1,000; (c) the pooled p99 if B had only 20 slow requests, 10; (d) so which is honest, pool the samples (`choice`).
5. (d4, `order`, `spsc-order`) the SPSC push as lines of C++ with distractors (store the tail before writing the slot; a relaxed store of the tail).
6. (d3, `numeric`, `coordinated-omission`) from the l17 numbers: measured p99.9 248 µs against 49,911 µs from intended send time: how many times larger, to the nearest whole number? 201 (49,911 / 248 = 201.25).

Drills for the E8 library (C++, timed, `drills/<id>.json` with `language: "cpp"`; fields as AUTHORING "Drill": `id`, `name`, `course: "systems"`, `skills`, `difficulty`, `brief`, `starter`, `examples`, `tests`, `how`, `solution`; filters by pattern and difficulty; a "session" is two drills in 60 minutes): `sy-lru-cache` (D-lru; skills `sy-latency`, `sy-memory`; pattern `cache`; difficulty 3; pace 1500 seconds), `sy-token-bucket` (D-token-bucket; `sy-latency`; pattern `rate-limiter`; 2; 900 seconds), `sy-bits` (D-bits; `sy-memory`; pattern `bits`; 2; 600 seconds). Suggested session: `sy-lru-cache` with `sy-token-bucket` (2,400 seconds of work in a 3,600-second session). The `brief` is the comment at the top of each starter; `how` states the number of hidden tests; `examples` are the first two tests.

Engine (level 4). E8: the three drills above (screen: the drill library, not a lesson; pace, filter and session fields as built). E3: tags `ring-buffer`, `power-of-two-mask`, `percentile`, `tail-latency`, `coordinated-omission`, `latency-budget`, `feed-handler-design`, `allocation-cost` for `bank/systems-4.json`; `mock-superday-developer` and `topic-3.5` draw from all four banks. E11: homework items 2 and 4. E13: none new (the ring's memory orders reuse l9's litmus ideas in an `order` task, not the canvas). E14: l17 (screen: the Python "report" `code` item, data file `latencies.csv`, 47,587 bytes, 2,000 rows). Existing features used: `console`, `array` queue mode with pointers, `bars` with `showMean`, `graph` directed pills, `order` with `distractors`, `table`, `numeric`, `choice`, `multi`, `code` (C++ and Python), `longform`.

## Code problems

Each problem below was compiled and run under g++ 13.3 and clang++ 18.1 with the harness in `cpp/harness.py`, which mimics the app: it runs every case in function mode as `setup`, then `call`, then compares to `expect`. The starter compiles and fails; the reference solution passes every test. Hidden `prelude` and `postlude` are placed around the learner's code as AUTHORING describes. `isclose` is used for doubles and `equal` otherwise. Copy the code exactly, then run the app's own checker.

### P-translate: l3-virtual-memory: translate

Where: `l3-virtual-memory`, a `code` screen after the worked examples, difficulty 2. Widget `code`, `language: "cpp"`, 10 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// frames[p] is the physical frame of virtual page p, or -1 if p is not mapped.
// Pages are 4096 bytes. Return the physical address, or -1 for a page fault.
long long translate(const std::vector<int>& frames, long long vaddr) {
    long long page = vaddr / 4096;
    if (page >= static_cast<long long>(frames.size())) return -1;
    return static_cast<long long>(frames[page]) * 4096;
}
```

Reference solution:

```cpp
#include <vector>

long long translate(const std::vector<int>& frames, long long vaddr) {
    long long page = vaddr / 4096;
    long long offset = vaddr % 4096;
    if (page >= static_cast<long long>(frames.size())) return -1;
    if (frames[page] < 0) return -1;
    return static_cast<long long>(frames[page]) * 4096 + offset;
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `translate({7,-1,9}, 10876)` expects `39548`
- `translate({7,-1,9}, 0)` expects `28672`
- `translate({7,-1,9}, 4095)` expects `32767`
- `translate({7,-1,9}, 8192)` expects `36864`
- `translate({7,-1,9}, 12287)` expects `40959`
- `translate({7,-1,9}, 4096)` expects `-1`
- `translate({7,-1,9}, 20480)` expects `-1`
- `translate({3,5}, 4113)` expects `20497`
- `translate({}, 0)` expects `-1`
- `translate({0}, 4095)` expects `4095`

Checked by `cpp/build_md.py`: the solution passes all 10 tests and the starter fails 6 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-struct-size: l4-object-layout: struct size

Where: `l4-object-layout`, a `code` screen after the layout table, difficulty 3. Widget `code`, `language: "cpp"`, 15 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// sizes: the size in bytes of each field, in declaration order.
// Each field is aligned to its own size (1, 2, 4 or 8).
int struct_size(const std::vector<int>& sizes) {
    int total = 0;
    for (int s : sizes) total += s;
    return total;
}

// The size after sorting the fields from largest to smallest.
int best_size(const std::vector<int>& sizes) {
    return struct_size(sizes);
}
```

Reference solution:

```cpp
#include <algorithm>
#include <functional>
#include <vector>

int struct_size(const std::vector<int>& sizes) {
    int offset = 0, widest = 1;
    for (int s : sizes) {
        offset = (offset + s - 1) / s * s;   // round up to a multiple of s
        offset += s;
        widest = std::max(widest, s);
    }
    return (offset + widest - 1) / widest * widest;   // tail padding
}

int best_size(const std::vector<int>& sizes) {
    std::vector<int> sorted = sizes;
    std::sort(sorted.begin(), sorted.end(), std::greater<int>());
    return struct_size(sorted);
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `struct_size({1,8,1})` expects `24`
- `best_size({1,8,1})` expects `16`
- `struct_size({1,4,1,4,2,4,4,4})` expects `32`
- `best_size({1,4,1,4,2,4,4,4})` expects `24`
- `struct_size({})` expects `0`
- `struct_size({1})` expects `1`
- `best_size({1})` expects `1`
- `struct_size({2,1})` expects `4`
- `best_size({2,1})` expects `4`
- `struct_size({8,1})` expects `16`
- `best_size({8,1})` expects `16`
- `struct_size({4,1,2,1,8})` expects `24`
- `best_size({4,1,2,1,8})` expects `16`
- `struct_size({1,2,4,8,1,2,4,8})` expects `32`
- `best_size({1,2,4,8,1,2,4,8})` expects `32`

Checked by `cpp/build_md.py`: the solution passes all 15 tests and the starter fails 10 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-mispredicts: l5-branches: two-bit predictor

Where: `l5-branches`, a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 10 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <string>

// Count the mispredictions of a two-bit saturating counter on a branch history.
// 'T' is taken, 'N' is not taken. The counter runs 0..3, starts at 1,
// predicts taken at 2 or 3, moves up on T and down on N, and stops at 0 and 3.
int mispredicts(const std::string& history) {
    int taken = 0, misses = 0;   // one bit: remember the last outcome
    for (char c : history) {
        int actual = (c == 'T');
        if (taken != actual) ++misses;
        taken = actual;
    }
    return misses;
}
```

Reference solution:

```cpp
#include <string>

int mispredicts(const std::string& history) {
    int counter = 1, misses = 0;
    for (char c : history) {
        bool predicted_taken = counter >= 2;
        bool actual_taken = (c == 'T');
        if (predicted_taken != actual_taken) ++misses;
        if (actual_taken) { if (counter < 3) ++counter; }
        else { if (counter > 0) --counter; }
    }
    return misses;
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `mispredicts("TTTTTTTT")` expects `1`
- `mispredicts("NNNN")` expects `0`
- `mispredicts("TNTNTNTN")` expects `8`
- `mispredicts("TTNTTNTTN")` expects `4`
- `mispredicts("TTTNNN")` expects `3`
- `mispredicts("TTTTTTTNTTTTTTTNTTTTTTTN")` expects `4`
- `mispredicts("")` expects `0`
- `mispredicts("T")` expects `1`
- `mispredicts("TTNTTNTTNTTNTTNTTNTTNTTNTTNTTN")` expects `11`
- `mispredicts("NTTT")` expects `2`

Checked by `cpp/build_md.py`: the solution passes all 10 tests and the starter fails 5 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-cache-sim: homework-1: a cache simulator

Where: `homework-1`, the homework `code` item, difficulty 4. Widget `code`, `language: "cpp"`, 10 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// A cache of num_lines lines of 64 bytes, in sets of `ways` lines each (num_lines is a multiple of ways).
// The line holding byte address a is a / 64 and it lives in set (a / 64) % (num_lines / ways).
// A full set drops its least recently used line. Start empty. Return the number of misses.
int count_misses(int num_lines, int ways, const std::vector<int>& addresses) {
    int misses = 0;
    for (int a : addresses) {
        (void)a;
        ++misses;     // TODO: an access whose line is already in its set is a hit
    }
    return misses;
}
```

Reference solution:

```cpp
#include <list>
#include <vector>

int count_misses(int num_lines, int ways, const std::vector<int>& addresses) {
    int sets = num_lines / ways;
    std::vector<std::list<int>> cache(sets);      // front = most recently used
    int misses = 0;
    for (int a : addresses) {
        int line = a / 64;
        std::list<int>& set = cache[line % sets];
        bool hit = false;
        for (auto it = set.begin(); it != set.end(); ++it) {
            if (*it == line) { set.erase(it); hit = true; break; }
        }
        if (!hit) {
            ++misses;
            if (static_cast<int>(set.size()) == ways) set.pop_back();
        }
        set.push_front(line);
    }
    return misses;
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `count_misses(4, 1, {0, 256, 8, 264, 16, 272, 24, 280, 32, 288, 40, 296, 48, 304, 56, 312})` expects `16`
- `count_misses(4, 2, {0, 256, 8, 264, 16, 272, 24, 280, 32, 288, 40, 296, 48, 304, 56, 312})` expects `2`
- `count_misses(4, 1, {0, 320, 8, 328, 16, 336, 24, 344, 32, 352, 40, 360, 48, 368, 56, 376})` expects `2`
- `count_misses(4, 4, {0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200, 208, 216, 224, 232, 240, 248, 256, 264, 272, 280, 288, 296, 304, 312, 320, 328, 336, 344, 352, 360, 368, 376, 384, 392, 400, 408, 416, 424, 432, 440, 448, 456, 464, 472, 480, 488, 496, 504})` expects `8`
- `count_misses(4, 4, {0, 64, 128, 192, 256, 320, 384, 448, 8, 72, 136, 200, 264, 328, 392, 456, 16, 80, 144, 208, 272, 336, 400, 464, 24, 88, 152, 216, 280, 344, 408, 472, 32, 96, 160, 224, 288, 352, 416, 480, 40, 104, 168, 232, 296, 360, 424, 488, 48, 112, 176, 240, 304, 368, 432, 496, 56, 120, 184, 248, 312, 376, 440, 504})` expects `64`
- `count_misses(8, 8, {0, 64, 128, 192, 256, 320, 384, 448, 8, 72, 136, 200, 264, 328, 392, 456, 16, 80, 144, 208, 272, 336, 400, 464, 24, 88, 152, 216, 280, 344, 408, 472, 32, 96, 160, 224, 288, 352, 416, 480, 40, 104, 168, 232, 296, 360, 424, 488, 48, 112, 176, 240, 304, 368, 432, 496, 56, 120, 184, 248, 312, 376, 440, 504})` expects `8`
- `count_misses(512, 8, {0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 256, 272, 288, 304, 320, 336, 352, 368, 384, 400, 416, 432, 448, 464, 480, 496})` expects `8`
- `count_misses(512, 8, {0, 24, 48, 72, 96, 120, 144, 168, 192, 216, 240, 264, 288, 312, 336, 360, 384, 408, 432, 456, 480, 504, 528, 552, 576, 600, 624, 648, 672, 696, 720, 744})` expects `12`
- `count_misses(4, 4, {})` expects `0`
- `count_misses(2, 2, {0, 64, 128, 0, 64, 128})` expects `6`

Checked by `cpp/build_md.py`: the solution passes all 10 tests and the starter fails 6 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-final-counts: l7-data-races: count every outcome

Where: `l7-data-races`, a `code` screen after the interleaving drill, difficulty 4. Widget `code`, `language: "cpp"`, 7 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// threads threads each run `increments` times: load x, add 1, store x (three steps).
// Try every interleaving of all the steps. result[v] is how many interleavings end with x == v.
std::vector<int> final_counts(int threads, int increments) {
    // Wrong model: an increment is one indivisible step.
    std::vector<int> done(threads, 0);
    std::vector<int> result(threads * increments + 1, 0);
    // count schedules of whole increments: every one ends with the full total
    std::vector<int> fact(threads * increments + 1, 1);
    for (int i = 1; i <= threads * increments; ++i) fact[i] = fact[i - 1] * i;
    long long ways = fact[threads * increments];
    for (int t = 0; t < threads; ++t) ways /= fact[increments];
    result[threads * increments] = static_cast<int>(ways);
    return result;
}
```

Reference solution:

```cpp
#include <vector>

namespace {
struct Walker {
    int threads, steps;                  // steps = 3 * increments, per thread
    std::vector<int> pc, reg;            // next step and register of each thread
    int x = 0;
    std::vector<int> result;
    void go() {
        bool any = false;
        for (int t = 0; t < threads; ++t) {
            if (pc[t] == steps) continue;
            any = true;
            int old_x = x, old_reg = reg[t];
            int phase = pc[t] % 3;
            if (phase == 0) reg[t] = x;            // load
            else if (phase == 1) reg[t] += 1;      // add
            else x = reg[t];                       // store
            ++pc[t];
            go();
            --pc[t];
            x = old_x;
            reg[t] = old_reg;
        }
        if (!any) ++result[x];
    }
};
}

std::vector<int> final_counts(int threads, int increments) {
    Walker w;
    w.threads = threads;
    w.steps = 3 * increments;
    w.pc.assign(threads, 0);
    w.reg.assign(threads, 0);
    w.result.assign(threads * increments + 1, 0);
    w.go();
    return w.result;
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `final_counts(1, 1)` expects `[0, 1]`
- `final_counts(1, 3)` expects `[0, 0, 0, 1]`
- `final_counts(2, 1)` expects `[0, 18, 2]`
- `final_counts(3, 1)` expects `[0, 1404, 270, 6]`
- `final_counts(2, 2)` expects `[0, 0, 702, 216, 6]`
- `final_counts(2, 3)` expects `[0, 0, 648, 30780, 15714, 1458, 20]`
- `final_counts(4, 1)` expects `[0, 291600, 74952, 3024, 24]`

Checked by `cpp/build_md.py`: the solution passes all 7 tests and the starter fails 5 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-lock-cycle: l8-locks-and-deadlock: lock-order cycle

Where: `l8-locks-and-deadlock`, a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 12 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <string>
#include <vector>

// Each string is one thread: the locks it takes, in order, each held while it takes the next ("AB" takes A, then B).
// Return true if the lock-order graph (an edge from each held lock to each lock taken after it) has a cycle.
bool has_lock_cycle(const std::vector<std::string>& threads) {
    // Only checks whether two threads share a lock, which is not the same as a cycle.
    for (size_t a = 0; a < threads.size(); ++a)
        for (size_t b = a + 1; b < threads.size(); ++b)
            for (char c : threads[a])
                if (threads[b].find(c) != std::string::npos) return true;
    return false;
}
```

Reference solution:

```cpp
#include <string>
#include <vector>

namespace {
bool visit(int n, const bool edge[26][26], int state[26]) {   // 0 new, 1 on the path, 2 finished
    state[n] = 1;
    for (int m = 0; m < 26; ++m) {
        if (!edge[n][m]) continue;
        if (state[m] == 1) return true;
        if (state[m] == 0 && visit(m, edge, state)) return true;
    }
    state[n] = 2;
    return false;
}
}

bool has_lock_cycle(const std::vector<std::string>& threads) {
    bool edge[26][26] = {};
    for (const auto& s : threads)
        for (size_t i = 0; i < s.size(); ++i)
            for (size_t j = i + 1; j < s.size(); ++j)
                edge[s[i] - 'A'][s[j] - 'A'] = true;
    int state[26] = {};
    for (int n = 0; n < 26; ++n)
        if (state[n] == 0 && visit(n, edge, state)) return true;
    return false;
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `has_lock_cycle({"AB", "BA"})` expects `true`
- `has_lock_cycle({"AB", "AB"})` expects `false`
- `has_lock_cycle({"AB", "BC", "CA"})` expects `true`
- `has_lock_cycle({"AB", "BC", "AC"})` expects `false`
- `has_lock_cycle({"A", "A"})` expects `false`
- `has_lock_cycle({"ABC", "CBA"})` expects `true`
- `has_lock_cycle({"AB", "CD"})` expects `false`
- `has_lock_cycle({})` expects `false`
- `has_lock_cycle({"AA"})` expects `true`
- `has_lock_cycle({"AB", "BC", "CD", "DA"})` expects `true`
- `has_lock_cycle({"ABC", "BCD", "ACD"})` expects `false`
- `has_lock_cycle({"AC", "BD", "CB"})` expects `false`

Checked by `cpp/build_md.py`: the solution passes all 12 tests and the starter fails 6 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-blocked-counts: homework-2: bounded buffer

Where: `homework-2`, the homework `code` item, difficulty 3. Widget `code`, `language: "cpp"`, 7 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <string>
#include <vector>

// A queue holds at most `capacity` items. The events run in order on one thread:
// 'P' pushes an item, 'C' pops one. A push on a full queue and a pop on an empty queue each
// would block, so skip the event and count it. Return {blocked pushes, blocked pops, items left}.
std::vector<int> blocked_counts(int capacity, const std::string& events) {
    int items = 0, blocked_push = 0, blocked_pop = 0;
    for (char e : events) {
        if (e == 'P') ++items;
        else --items;
    }
    return {blocked_push, blocked_pop, items};
}
```

Reference solution:

```cpp
#include <string>
#include <vector>

std::vector<int> blocked_counts(int capacity, const std::string& events) {
    int items = 0, blocked_push = 0, blocked_pop = 0;
    for (char e : events) {
        if (e == 'P') {
            if (items == capacity) ++blocked_push;
            else ++items;
        } else {
            if (items == 0) ++blocked_pop;
            else --items;
        }
    }
    return {blocked_push, blocked_pop, items};
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `blocked_counts(2, "PPPCCC")` expects `[1, 1, 0]`
- `blocked_counts(2, "CCPP")` expects `[0, 2, 2]`
- `blocked_counts(1, "PPCCPC")` expects `[1, 1, 0]`
- `blocked_counts(3, "PPPPPPCCC")` expects `[3, 0, 0]`
- `blocked_counts(4, "")` expects `[0, 0, 0]`
- `blocked_counts(2, "PCPCPC")` expects `[0, 0, 0]`
- `blocked_counts(2, "PPPPCC")` expects `[2, 0, 0]`

Checked by `cpp/build_md.py`: the solution passes all 7 tests and the starter fails 5 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-find-gaps: l13-tcp-and-udp: find the missing sequence numbers

Where: `l13-tcp-and-udp`, a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 13 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// A UDP feed numbers its messages 1, 2, 3, ... Messages may arrive late or twice.
// Given the sequence numbers in arrival order, return every number from 1 up to the largest seen
// that has not arrived, smallest first.
std::vector<int> find_gaps(const std::vector<int>& seqs) {
    std::vector<int> missing;
    int expected = 1;
    for (int s : seqs) {
        while (expected < s) missing.push_back(expected++);   // a jump means a gap
        if (s == expected) ++expected;
    }
    return missing;
}
```

Reference solution:

```cpp
#include <algorithm>
#include <vector>

std::vector<int> find_gaps(const std::vector<int>& seqs) {
    if (seqs.empty()) return {};
    int largest = *std::max_element(seqs.begin(), seqs.end());
    std::vector<bool> seen(largest + 1, false);
    for (int s : seqs) seen[s] = true;
    std::vector<int> missing;
    for (int n = 1; n <= largest; ++n)
        if (!seen[n]) missing.push_back(n);
    return missing;
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `find_gaps({1, 2, 4, 5})` expects `[3]`
- `find_gaps({1, 3, 2})` expects `[]`
- `find_gaps({2, 3})` expects `[1]`
- `find_gaps({1, 5})` expects `[2, 3, 4]`
- `find_gaps({1, 2, 2, 4, 4})` expects `[3]`
- `find_gaps({})` expects `[]`
- `find_gaps({3, 1, 2, 6, 5})` expects `[4]`
- `find_gaps({1, 2, 3, 7, 8, 10})` expects `[4, 5, 6, 9]`
- `find_gaps({5, 4, 3, 2, 1})` expects `[]`
- `find_gaps({2, 1, 4, 3, 6})` expects `[5]`
- `find_gaps({4, 2, 3})` expects `[1]`
- `find_gaps({1, 4, 2, 3})` expects `[]`
- `find_gaps({3, 3, 1})` expects `[2]`

Checked by `cpp/build_md.py`: the solution passes all 13 tests and the starter fails 7 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-wire: l14-messages-on-the-wire: encode and decode

Where: `l14-messages-on-the-wire`, a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 12 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Hidden `prelude`:

```cpp
struct Msg {
    int type;            // 'A' add, 'X' cancel, 'T' trade
    int side;            // 'B' or 'S'
    int instrument;      // 0..65535
    unsigned seq;
    unsigned id;
    unsigned qty;
    int price;           // pence, may be negative
    unsigned time;       // milliseconds since midnight
};
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// Wire layout, 24 bytes, big-endian (most significant byte first):
//   0 type (1)   1 side (1)   2 instrument (2)   4 seq (4)
//   8 id (4)    12 qty (4)   16 price (4, signed)  20 time (4)
std::vector<int> encode(const Msg& m) {
    std::vector<int> out(24, 0);
    out[0] = m.type;
    out[1] = m.side;
    // TODO: the other fields, most significant byte first
    return out;
}

Msg decode(const std::vector<int>& b) {
    Msg m{};
    m.type = b[0];
    m.side = b[1];
    // TODO: the other fields
    return m;
}
```

Reference solution:

```cpp
#include <vector>

namespace {
void put(std::vector<int>& out, int at, unsigned v, int bytes) {
    for (int k = 0; k < bytes; ++k)
        out[at + k] = (v >> (8 * (bytes - 1 - k))) & 0xFF;
}
unsigned get(const std::vector<int>& b, int at, int bytes) {
    unsigned v = 0;
    for (int k = 0; k < bytes; ++k) v = (v << 8) | static_cast<unsigned>(b[at + k] & 0xFF);
    return v;
}
}

std::vector<int> encode(const Msg& m) {
    std::vector<int> out(24, 0);
    out[0] = m.type;
    out[1] = m.side;
    put(out, 2, static_cast<unsigned>(m.instrument), 2);
    put(out, 4, m.seq, 4);
    put(out, 8, m.id, 4);
    put(out, 12, m.qty, 4);
    put(out, 16, static_cast<unsigned>(m.price), 4);
    put(out, 20, m.time, 4);
    return out;
}

Msg decode(const std::vector<int>& b) {
    Msg m{};
    m.type = b[0];
    m.side = b[1];
    m.instrument = static_cast<int>(get(b, 2, 2));
    m.seq = get(b, 4, 4);
    m.id = get(b, 8, 4);
    m.qty = get(b, 12, 4);
    m.price = static_cast<int>(get(b, 16, 4));
    m.time = get(b, 20, 4);
    return m;
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `Msg m{65, 66, 258, 70000u, 123456789u, 100u, 10275, 36000000u}; encode(m)` expects `[65, 66, 1, 2, 0, 1, 17, 112, 7, 91, 205, 21, 0, 0, 0, 100, 0, 0, 40, 35, 2, 37, 81, 0]`
- `Msg m{88, 83, 1, 1u, 2u, 0u, -25, 0u}; encode(m)` expects `[88, 83, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 255, 255, 255, 231, 0, 0, 0, 0]`
- `Msg m{84, 66, 65535, 4294967295u, 4294967295u, 4294967295u, 2147483647, 86399999u}; encode(m)` expects `[84, 66, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127, 255, 255, 255, 5, 38, 91, 255]`
- `Msg m{65, 83, 0, 0u, 0u, 1u, (-2147483647 - 1), 1u}; encode(m)` expects `[65, 83, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 128, 0, 0, 0, 0, 0, 0, 1]`
- `decode(std::vector<int>{65, 66, 1, 2, 0, 1, 17, 112, 7, 91, 205, 21, 0, 0, 0, 100, 0, 0, 40, 35, 2, 37, 81, 0}).instrument` expects `258`
- `decode(std::vector<int>{65, 66, 1, 2, 0, 1, 17, 112, 7, 91, 205, 21, 0, 0, 0, 100, 0, 0, 40, 35, 2, 37, 81, 0}).price` expects `10275`
- `decode(std::vector<int>{88, 83, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 255, 255, 255, 231, 0, 0, 0, 0}).price` expects `-25`
- `(long long)decode(std::vector<int>{84, 66, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127, 255, 255, 255, 5, 38, 91, 255}).seq` expects `4294967295`
- `(long long)decode(std::vector<int>{84, 66, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127, 255, 255, 255, 5, 38, 91, 255}).time` expects `86399999`
- `decode(std::vector<int>{65, 83, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 128, 0, 0, 0, 0, 0, 0, 1}).price` expects `-2147483648`
- `Msg m{65, 66, 258, 70000u, 123456789u, 100u, 10275, 36000000u}; Msg d = decode(encode(m)); (long long)d.id` expects `123456789`
- `Msg m{84, 66, 65535, 4294967295u, 4294967295u, 4294967295u, 2147483647, 86399999u}; Msg d = decode(encode(m)); (long long)d.qty` expects `4294967295`

Checked by `cpp/build_md.py`: the solution passes all 12 tests and the starter fails 12 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-pool: l15-no-allocation: a pool of slots

Where: `l15-no-allocation`, a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 10 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Hidden `prelude`:

```cpp
#include <cstdlib>
#include <new>
static int g_allocs = 0;   // counts every call to operator new
static void* volatile g_last = nullptr;   // the last block, kept so the call stays visible
void* operator new(std::size_t n) { ++g_allocs; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); g_last = p; return p; }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// A pool of `slots` fixed slots, numbered 0 .. slots-1.
// allocate() returns a free slot, or -1 if none is free. release(s) makes slot s free again.
// The most recently released slot is the next one allocated. No call may use the heap after the constructor.
class Pool {
public:
    explicit Pool(int slots) : slots_(slots) {}
    int allocate() { return next_++; }          // never reuses a slot
    void release(int slot) { (void)slot; }
    int in_use() const { return next_; }
private:
    int slots_;
    int next_ = 0;
};
```

Reference solution:

```cpp
#include <vector>

class Pool {
public:
    explicit Pool(int slots) : next_free_(slots, -1), in_use_(0) {
        for (int s = 0; s + 1 < slots; ++s) next_free_[s] = s + 1;   // slot s points at slot s+1
        head_ = slots > 0 ? 0 : -1;
    }
    int allocate() {
        if (head_ < 0) return -1;
        int slot = head_;
        head_ = next_free_[slot];
        ++in_use_;
        return slot;
    }
    void release(int slot) {
        next_free_[slot] = head_;
        head_ = slot;
        --in_use_;
    }
    int in_use() const { return in_use_; }
private:
    std::vector<int> next_free_;   // the free list, stored inside the slots' own indices
    int head_;
    int in_use_;
};
```

Hidden tests (`setup` then `call` and its `expect`):

- `Pool p(3); p.allocate()` expects `0`
- `Pool p(3); p.allocate(); p.allocate(); p.allocate()` expects `2`
- `Pool p(3); p.allocate(); p.allocate(); p.allocate(); p.allocate()` expects `-1`
- `Pool p(3); int a = p.allocate(); int b = p.allocate(); p.allocate(); p.release(b); p.allocate()` expects `1`
- `Pool p(3); int a = p.allocate(); int b = p.allocate(); p.release(a); p.release(b); p.allocate()` expects `1`
- `Pool p(3); int a = p.allocate(); int b = p.allocate(); p.release(a); p.release(b); p.allocate(); p.allocate()` expects `0`
- `Pool p(2); p.allocate(); p.allocate(); p.release(0); p.allocate(); p.in_use()` expects `2`
- `Pool p(2); p.allocate(); p.allocate(); p.release(0); p.release(1); p.in_use()` expects `0`
- `Pool p(0); p.allocate()` expects `-1`
- `Pool p(8); g_allocs = 0; for (int r = 0; r < 100; ++r) { int s = p.allocate(); p.release(s); } g_allocs` expects `0`

Checked by `cpp/build_md.py`: the solution passes all 10 tests and the starter fails 7 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-format-price: l15-no-allocation: format a price in place

Where: `l15-no-allocation`, a second `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 9 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Hidden `prelude`:

```cpp
#include <cstdlib>
#include <new>
static int g_allocs = 0;   // counts every call to operator new
static void* volatile g_last = nullptr;   // the last block, kept so the call stays visible
void* operator new(std::size_t n) { ++g_allocs; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); g_last = p; return p; }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// Write a price given in pence as pounds and pence into out, for example 10275 -> "102.75", -25 -> "-0.25".
// Put a '\0' after the text and return its length (not counting the '\0'). out has room for 32 characters.
// The hot path may not use the heap.
int format_price(char* out, int pence) {
    std::vector<char> digits;                 // allocates
    bool negative = pence < 0;
    long long a = negative ? -(long long)pence : pence;
    (void)negative;
    do { digits.push_back(static_cast<char>('0' + a % 10)); a /= 10; } while (a > 0);
    int n = 0;      // TODO: the '-' sign, and pence below 10 need a leading '0'
    for (int i = static_cast<int>(digits.size()) - 1; i >= 0; --i) {
        out[n++] = digits[i];
        if (i == 2) out[n++] = '.';
    }
    out[n] = '\0';
    return n;
}
```

Reference solution:

```cpp
int format_price(char* out, int pence) {
    int n = 0;
    long long a = pence;
    if (a < 0) { out[n++] = '-'; a = -a; }
    long long pounds = a / 100;
    int pennies = static_cast<int>(a % 100);
    char tmp[24];
    int t = 0;
    do { tmp[t++] = static_cast<char>('0' + pounds % 10); pounds /= 10; } while (pounds > 0);
    while (t > 0) out[n++] = tmp[--t];
    out[n++] = '.';
    out[n++] = static_cast<char>('0' + pennies / 10);
    out[n++] = static_cast<char>('0' + pennies % 10);
    out[n] = '\0';
    return n;
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `char buf[32]; int n = format_price(buf, 10275); std::string(buf, n)` expects `"102.75"`
- `char buf[32]; int n = format_price(buf, 5); std::string(buf, n)` expects `"0.05"`
- `char buf[32]; int n = format_price(buf, 0); std::string(buf, n)` expects `"0.00"`
- `char buf[32]; int n = format_price(buf, -25); std::string(buf, n)` expects `"-0.25"`
- `char buf[32]; int n = format_price(buf, 100000); std::string(buf, n)` expects `"1000.00"`
- `char buf[32]; int n = format_price(buf, 1999); std::string(buf, n)` expects `"19.99"`
- `char buf[32]; int n = format_price(buf, -5); std::string(buf, n)` expects `"-0.05"`
- `char buf[32]; int n = format_price(buf, 99); std::string(buf, n)` expects `"0.99"`
- `char buf[32]; g_allocs = 0; format_price(buf, 10275); format_price(buf, -25); g_allocs` expects `0`

Checked by `cpp/build_md.py`: the solution passes all 9 tests and the starter fails 6 of them: five on the text (no sign, no padding) whatever the optimiser does, and the `g_allocs` test only if the compiler keeps the `std::vector` allocation, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-ring: l16-ring-buffer: a single-producer ring

Where: `l16-ring-buffer`, a `code` screen, difficulty 4. Widget `code`, `language: "cpp"`, 10 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Hidden `postlude`:

```cpp

// hidden driver: ops > 0 push that value (1 if accepted, 0 if full); ops == 0 pop (the value, or -1 if empty)
std::vector<int> drive(int capacity, const std::vector<int>& ops) {
    Ring r(capacity);
    std::vector<int> out;
    for (int op : ops) {
        if (op > 0) out.push_back(r.push(op) ? 1 : 0);
        else { int v = 0; out.push_back(r.pop(v) ? v : -1); }
    }
    return out;
}
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <cstddef>
#include <vector>

// A fixed-size ring of ints. capacity is a power of two. push returns false when full,
// pop returns false when empty. head_ counts pops and tail_ counts pushes: both only ever grow.
// Keep head_ and tail_ at least 64 bytes apart so two cores do not share a cache line.
struct Ring {
    explicit Ring(std::size_t capacity) : buf_(capacity), mask_(capacity - 1) {}
    bool push(int v) {
        if (tail_ - head_ >= buf_.size() - 1) return false;   // one slot too early
        buf_[tail_ & mask_] = v;
        ++tail_;
        return true;
    }
    bool pop(int& out) {
        if (head_ == tail_) return false;
        out = buf_[head_ & mask_];
        ++head_;
        return true;
    }
    std::vector<int> buf_;
    std::size_t mask_;
    std::size_t head_ = 0;
    std::size_t tail_ = 0;
};
```

Reference solution:

```cpp
#include <cstddef>
#include <vector>

struct Ring {
    explicit Ring(std::size_t capacity) : buf_(capacity), mask_(capacity - 1) {}
    bool push(int v) {
        if (tail_ - head_ == buf_.size()) return false;     // full
        buf_[tail_ & mask_] = v;
        ++tail_;
        return true;
    }
    bool pop(int& out) {
        if (head_ == tail_) return false;                   // empty
        out = buf_[head_ & mask_];
        ++head_;
        return true;
    }
    std::vector<int> buf_;
    std::size_t mask_;
    alignas(64) std::size_t head_ = 0;
    alignas(64) std::size_t tail_ = 0;
};
```

Hidden tests (`setup` then `call` and its `expect`):

- `drive(4, {1, 2, 3, 4, 5, 0, 0, 0, 0, 0})` expects `[1, 1, 1, 1, 0, 1, 2, 3, 4, -1]`
- `drive(4, {1, 2, 3, 0, 0, 4, 5, 6, 0, 0, 0, 0})` expects `[1, 1, 1, 1, 2, 1, 1, 1, 3, 4, 5, 6]`
- `drive(2, {0})` expects `[-1]`
- `drive(1, {7, 8, 0, 9, 0, 0})` expects `[1, 0, 7, 1, 9, -1]`
- `drive(8, {})` expects `[]`
- `drive(4, {1, 2, 3, 4, 0, 5, 0, 6, 0, 7, 0, 8, 0, 0, 0, 0, 0})` expects `[1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 6, 7, 8, -1]`
- `drive(2, {1, 2, 3, 0, 3, 0, 0, 0})` expects `[1, 1, 0, 1, 1, 2, 3, -1]`
- `drive(4, {1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 0, 7, 0, 8, 0, 9, 0, 10, 0})` expects `[1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 1, 6, 1, 7, 1, 8, 1, 9, 1, 10]`
- `drive(4, {1, 2, 3, 4, 0, 5, 0, 6, 0, 7, 0, 8, 0, 9, 0, 10, 0, 11, 0, 12, 0, 13, 0, 14, 0, 15, 0, 16, 0, 17, 0, 18, 0, 19, 0, 20, 0, 21, 0, 22, 0, 23, 0, 0, 0, 0, 0})` expects `[1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 4, 1, 5, 1, 6, 1, 7, 1, 8, 1, 9, 1, 10, 1, 11, 1, 12, 1, 13, 1, 14, 1, 15, 1, 16, 1, 17, 1, 18, 1, 19, 1, 20, 21, 22, 23, -1]`
- `Ring r(8); (long long)((const char*)&r.tail_ - (const char*)&r.head_) >= 64` expects `true`

Checked by `cpp/build_md.py`: the solution passes all 10 tests and the starter fails 7 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-percentile: l17-measuring-latency: percentile and mean

Where: `l17-measuring-latency`, a `code` screen, difficulty 3. Widget `code`, `language: "cpp"`, 13 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <vector>

// Nearest-rank percentile: sort the samples; the p-th percentile is the value at rank ceil(p * n / 100),
// counting from 1 (rank 1 at p = 0). Subtract 1e-9 before ceil so 99 * 1000 / 100 does not round up.
double percentile(std::vector<double> samples, double p) {
    return samples.empty() ? 0.0 : samples.back();     // the last sample, unsorted
}

double mean(const std::vector<double>& samples) {
    double total = 0.0;
    for (double s : samples) total += s;
    return samples.empty() ? 0.0 : total / samples.size();
}
```

Reference solution:

```cpp
#include <algorithm>
#include <cmath>
#include <vector>

double percentile(std::vector<double> samples, double p) {
    if (samples.empty()) return 0.0;
    std::sort(samples.begin(), samples.end());
    double n = static_cast<double>(samples.size());
    long long rank = static_cast<long long>(std::ceil(p * n / 100.0 - 1e-9));
    if (rank < 1) rank = 1;
    if (rank > static_cast<long long>(samples.size())) rank = static_cast<long long>(samples.size());
    return samples[rank - 1];
}

double mean(const std::vector<double>& samples) {
    double total = 0.0;
    for (double s : samples) total += s;
    return samples.empty() ? 0.0 : total / samples.size();
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `std::vector<double> v(990, 10.0); v.insert(v.end(), 10, 1000.0); percentile(v, 50)` expects `10.0`
- `std::vector<double> v(990, 10.0); v.insert(v.end(), 10, 1000.0); percentile(v, 99)` expects `10.0`
- `std::vector<double> v(990, 10.0); v.insert(v.end(), 10, 1000.0); percentile(v, 99.9)` expects `1000.0`
- `std::vector<double> v(990, 10.0); v.insert(v.end(), 10, 1000.0); percentile(v, 100)` expects `1000.0`
- `std::vector<double> v(989, 10.0); v.insert(v.end(), 11, 1000.0); percentile(v, 99)` expects `1000.0`
- `std::vector<double> v(999, 10.0); v.push_back(1000.0); percentile(v, 99.9)` expects `10.0`
- `std::vector<double> v(999, 10.0); v.push_back(1000.0); percentile(v, 100)` expects `1000.0`
- `std::vector<double> v = {5.0, 1.0, 4.0, 2.0, 3.0}; percentile(v, 20)` expects `1.0`
- `std::vector<double> v = {5.0, 1.0, 4.0, 2.0, 3.0}; percentile(v, 50)` expects `3.0`
- `std::vector<double> v = {5.0, 1.0, 4.0, 2.0, 3.0}; percentile(v, 80)` expects `4.0`
- `std::vector<double> v = {5.0, 1.0, 4.0, 2.0, 3.0}; percentile(v, 100)` expects `5.0`
- `std::vector<double> v = {5.0, 1.0, 4.0, 2.0, 3.0}; percentile(v, 0)` expects `1.0`
- `std::vector<double> v(990, 10.0); v.insert(v.end(), 10, 1000.0); mean(v)` expects `19.9`

Checked by `cpp/build_md.py`: the solution passes all 13 tests and the starter fails 7 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-latency-hist: homework-4: a fixed-bucket latency histogram

Where: `homework-4`, the homework `code` item, difficulty 4. Widget `code`, `language: "cpp"`, 12 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Hidden `prelude`:

```cpp
#include <cstdlib>
#include <new>
static int g_allocs = 0;   // counts every call to operator new
static void* volatile g_last = nullptr;   // the last block, kept so the call stays visible
void* operator new(std::size_t n) { ++g_allocs; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); g_last = p; return p; }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <array>

// Buckets by powers of two: a sample of ns nanoseconds goes in bucket floor(log2(max(ns, 1))), 0..39.
// percentile_upper(p) finds the bucket holding the nearest-rank p-th percentile sample
// (rank ceil(p * n / 100 - 1e-9), at least 1) and returns that bucket's upper bound, 2^(bucket + 1).
// record() must not use the heap.
class LatencyHist {
public:
    void record(long long ns) { ++total_; (void)ns; }
    long long percentile_upper(double p) const { (void)p; return 0; }
    int count() const { return total_; }
private:
    std::array<int, 40> buckets_{};
    int total_ = 0;
};
```

Reference solution:

```cpp
#include <array>
#include <cmath>

class LatencyHist {
public:
    void record(long long ns) {
        int b = 0;
        long long v = ns < 1 ? 1 : ns;
        while (v > 1) { v >>= 1; ++b; }
        if (b > 39) b = 39;
        ++buckets_[b];
        ++total_;
    }
    long long percentile_upper(double p) const {
        if (total_ == 0) return 0;
        long long rank = static_cast<long long>(std::ceil(p * total_ / 100.0 - 1e-9));
        if (rank < 1) rank = 1;
        long long seen = 0;
        for (int b = 0; b < 40; ++b) {
            seen += buckets_[b];
            if (seen >= rank) return 1LL << (b + 1);
        }
        return 1LL << 40;
    }
    int count() const { return total_; }
private:
    std::array<int, 40> buckets_{};
    int total_ = 0;
};
```

Hidden tests (`setup` then `call` and its `expect`):

- `LatencyHist h; for (int i = 0; i < 990; ++i) h.record(10); for (int i = 0; i < 10; ++i) h.record(1000); h.percentile_upper(50)` expects `16`
- `LatencyHist h; for (int i = 0; i < 990; ++i) h.record(10); for (int i = 0; i < 10; ++i) h.record(1000); h.percentile_upper(99)` expects `16`
- `LatencyHist h; for (int i = 0; i < 990; ++i) h.record(10); for (int i = 0; i < 10; ++i) h.record(1000); h.percentile_upper(99.9)` expects `1024`
- `LatencyHist h; for (int i = 0; i < 1; ++i) h.record(1); for (int i = 0; i < 1; ++i) h.record(2); for (int i = 0; i < 1; ++i) h.record(3); for (int i = 0; i < 1; ++i) h.record(4); for (int i = 0; i < 1; ++i) h.record(5); for (int i = 0; i < 1; ++i) h.record(6); for (int i = 0; i < 1; ++i) h.record(7); for (int i = 0; i < 1; ++i) h.record(8); for (int i = 0; i < 1; ++i) h.record(9); for (int i = 0; i < 1; ++i) h.record(10); h.percentile_upper(50)` expects `8`
- `LatencyHist h; for (int i = 0; i < 1; ++i) h.record(1); for (int i = 0; i < 1; ++i) h.record(2); for (int i = 0; i < 1; ++i) h.record(3); for (int i = 0; i < 1; ++i) h.record(4); for (int i = 0; i < 1; ++i) h.record(5); for (int i = 0; i < 1; ++i) h.record(6); for (int i = 0; i < 1; ++i) h.record(7); for (int i = 0; i < 1; ++i) h.record(8); for (int i = 0; i < 1; ++i) h.record(9); for (int i = 0; i < 1; ++i) h.record(10); h.percentile_upper(90)` expects `16`
- `LatencyHist h; for (int i = 0; i < 1; ++i) h.record(1); for (int i = 0; i < 1; ++i) h.record(2); for (int i = 0; i < 1; ++i) h.record(3); for (int i = 0; i < 1; ++i) h.record(4); for (int i = 0; i < 1; ++i) h.record(5); for (int i = 0; i < 1; ++i) h.record(6); for (int i = 0; i < 1; ++i) h.record(7); for (int i = 0; i < 1; ++i) h.record(8); for (int i = 0; i < 1; ++i) h.record(9); for (int i = 0; i < 1; ++i) h.record(10); h.percentile_upper(100)` expects `16`
- `LatencyHist h; for (int i = 0; i < 1; ++i) h.record(0); for (int i = 0; i < 1; ++i) h.record(1); for (int i = 0; i < 1; ++i) h.record(2); for (int i = 0; i < 1; ++i) h.record(3); h.percentile_upper(50)` expects `2`
- `LatencyHist h; for (int i = 0; i < 1; ++i) h.record(0); for (int i = 0; i < 1; ++i) h.record(1); for (int i = 0; i < 1; ++i) h.record(2); for (int i = 0; i < 1; ++i) h.record(3); h.percentile_upper(100)` expects `4`
- `LatencyHist h; for (int i = 0; i < 5; ++i) h.record(1000000); for (int i = 0; i < 95; ++i) h.record(100); h.percentile_upper(90)` expects `128`
- `LatencyHist h; for (int i = 0; i < 5; ++i) h.record(1000000); for (int i = 0; i < 95; ++i) h.record(100); h.percentile_upper(99)` expects `1048576`
- `LatencyHist h; h.record(1000); h.record(2000); h.count()` expects `2`
- `LatencyHist h; g_allocs = 0; for (int i = 0; i < 1000; ++i) h.record(i * 37); g_allocs` expects `0`

Checked by `cpp/build_md.py`: the solution passes all 12 tests and the starter fails 10 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### P-handler: l18-feed-handler: a book with no allocation

Where: `l18-feed-handler`, the capstone `code` screen, difficulty 4 (the lesson's last task screen). Widget `code`, `language: "cpp"`, 14 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Hidden `prelude`:

```cpp
#include <cstdlib>
#include <new>
static int g_allocs = 0;   // counts every call to operator new
static void* volatile g_last = nullptr;   // the last block, kept so the call stays visible
void* operator new(std::size_t n) { ++g_allocs; void* p = std::malloc(n ? n : 1); if (!p) std::abort(); g_last = p; return p; }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

#include <vector>
std::vector<int> frame(char type, char side, unsigned seq, unsigned id, unsigned qty, int price) {
    std::vector<int> b(24, 0);
    auto put = [&](int at, unsigned v, int n) { for (int k = 0; k < n; ++k) b[at + k] = (v >> (8 * (n - 1 - k))) & 0xFF; };
    b[0] = type; b[1] = side; put(2, 7, 2); put(4, seq, 4); put(8, id, 4); put(12, qty, 4); put(16, static_cast<unsigned>(price), 4); put(20, 36000000u + seq, 4);
    return b;
}
std::vector<int> cat(std::vector<std::vector<int>> parts) {
    std::vector<int> all;
    for (auto& p : parts) all.insert(all.end(), p.begin(), p.end());
    return all;
}
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <map>
#include <vector>

// Frames are 24 bytes (the l14 layout, big-endian). One instrument, prices 9900..10100 pence, order ids below 1024.
// 'A' adds an order (side B or S, price, qty), 'X' cancels the rest of order id, 'T' trades qty against order id.
// A frame with seq < the next expected is stale: ignore it. A larger seq adds (seq - expected) to gaps().
// Partial frames wait for their remaining bytes. After construction, feed() may not use the heap.
class Handler {
public:
    void feed(const std::vector<int>& bytes) {
        for (std::size_t at = 0; at + 24 <= bytes.size(); at += 24) {
            int type = bytes[at];
            unsigned id = (bytes[at + 8] << 24) | (bytes[at + 9] << 16) | (bytes[at + 10] << 8) | bytes[at + 11];
            unsigned qty = (bytes[at + 12] << 24) | (bytes[at + 13] << 16) | (bytes[at + 14] << 8) | bytes[at + 15];
            int price = (bytes[at + 16] << 24) | (bytes[at + 17] << 16) | (bytes[at + 18] << 8) | bytes[at + 19];
            bool bid = bytes[at + 1] == 'B';
            if (type == 'A') { (bid ? bids_ : asks_)[price] += qty; ++applied_; }
        }
    }
    int best_bid() const { return bids_.empty() ? 0 : bids_.rbegin()->first; }
    int best_ask() const { return asks_.empty() ? 0 : asks_.begin()->first; }
    int bid_qty(int price) const { auto it = bids_.find(price); return it == bids_.end() ? 0 : static_cast<int>(it->second); }
    int ask_qty(int price) const { auto it = asks_.find(price); return it == asks_.end() ? 0 : static_cast<int>(it->second); }
    int gaps() const { return 0; }
    int applied() const { return applied_; }
private:
    std::map<int, unsigned> bids_, asks_;
    int applied_ = 0;
};
```

Reference solution:

```cpp
#include <array>
#include <cstdint>
#include <vector>

class Handler {
public:
    void feed(const std::vector<int>& bytes) {
        for (int b : bytes) {
            pending_[pending_len_++] = static_cast<std::uint8_t>(b);
            if (pending_len_ == kFrame) { frame(); pending_len_ = 0; }
        }
    }
    int best_bid() const {
        for (int i = kLevels - 1; i >= 0; --i) if (qty_[0][i] > 0) return kMinPrice + i;
        return 0;
    }
    int best_ask() const {
        for (int i = 0; i < kLevels; ++i) if (qty_[1][i] > 0) return kMinPrice + i;
        return 0;
    }
    int bid_qty(int price) const { return level(0, price); }
    int ask_qty(int price) const { return level(1, price); }
    int gaps() const { return gaps_; }
    int applied() const { return applied_; }
private:
    static constexpr int kFrame = 24, kMinPrice = 9900, kLevels = 201, kOrders = 1024;
    struct Order { int side = 0; int price = 0; unsigned qty = 0; bool live = false; };

    unsigned u32(int at) const {
        return (unsigned(pending_[at]) << 24) | (unsigned(pending_[at + 1]) << 16) | (unsigned(pending_[at + 2]) << 8) | unsigned(pending_[at + 3]);
    }
    int level(int side, int price) const {
        int i = price - kMinPrice;
        return (i >= 0 && i < kLevels) ? static_cast<int>(qty_[side][i]) : 0;
    }
    void frame() {
        unsigned seq = u32(4);
        if (seq < expected_) return;                 // stale or duplicate
        if (seq > expected_) gaps_ += static_cast<int>(seq - expected_);
        expected_ = seq + 1;
        ++applied_;
        int type = pending_[0];
        int side = pending_[1] == 'B' ? 0 : (pending_[1] == 'S' ? 1 : -1);
        unsigned id = u32(8), qty = u32(12);
        int price = static_cast<int>(u32(16));
        if (id >= kOrders) return;
        Order& o = orders_[id];
        if (type == 'A') {
            int i = price - kMinPrice;
            if (side < 0 || i < 0 || i >= kLevels || o.live) return;
            o = Order{side, price, qty, true};
            qty_[side][i] += qty;
        } else if (type == 'X') {
            if (!o.live) return;
            qty_[o.side][o.price - kMinPrice] -= o.qty;
            o.live = false;
        } else if (type == 'T') {
            if (!o.live) return;
            unsigned done = qty < o.qty ? qty : o.qty;
            o.qty -= done;
            qty_[o.side][o.price - kMinPrice] -= done;
            if (o.qty == 0) o.live = false;
        }
    }

    std::array<std::array<unsigned, kLevels>, 2> qty_{};
    std::array<Order, kOrders> orders_{};
    std::array<std::uint8_t, kFrame> pending_{};
    int pending_len_ = 0;
    unsigned expected_ = 1;
    int gaps_ = 0, applied_ = 0;
};
```

Hidden tests (`setup` then `call` and its `expect`):

- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005)}); h.feed(s); h.best_bid()` expects `10005`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005)}); h.feed(s); h.best_ask()` expects `10010`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005), frame('X', 'B', 4, 3, 0, 0)}); h.feed(s); h.best_bid()` expects `10000`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005), frame('T', 'B', 4, 1, 30, 10000)}); h.feed(s); h.bid_qty(10000)` expects `70`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('T', 'B', 2, 1, 100, 10000)}); h.feed(s); h.best_bid()` expects `0`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 10, 10000), frame('A', 'B', 2, 2, 10, 10001), frame('A', 'B', 5, 3, 10, 10002)}); h.feed(s); h.gaps()` expects `2`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 10, 10000), frame('A', 'B', 2, 2, 10, 10001), frame('A', 'B', 2, 3, 99, 10050)}); h.feed(s); h.applied()` expects `2`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 10, 10000), frame('A', 'B', 2, 2, 10, 10001), frame('A', 'B', 4, 3, 10, 10002), frame('A', 'B', 3, 4, 500, 10050)}); h.feed(s); h.best_bid()` expects `10002`
- `Handler h; auto s = cat({frame('A', 'B', 3, 1, 10, 10000)}); h.feed(s); h.gaps()` expects `2`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005)}); h.feed(std::vector<int>(s.begin(), s.begin() + 30)); h.feed(std::vector<int>(s.begin() + 30, s.end())); h.best_bid()` expects `10005`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005), frame('T', 'S', 4, 2, 50, 10010)}); for (int b : s) h.feed(std::vector<int>{b}); h.best_ask()` expects `0`
- `Handler h; auto s = cat({frame('X', 'B', 1, 9, 0, 0), frame('A', 'B', 2, 4000, 10, 10000), frame('A', 'B', 3, 5, 10, 12000), frame('A', 'B', 4, 6, 10, 9999)}); h.feed(s); h.best_bid()` expects `9999`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'S', 2, 2, 50, 10010), frame('A', 'B', 3, 3, 40, 10005)}); g_allocs = 0; h.feed(s); g_allocs` expects `0`
- `Handler h; auto s = cat({frame('A', 'B', 1, 1, 100, 10000), frame('A', 'B', 2, 1, 70, 10003)}); h.feed(s); h.bid_qty(10003)` expects `0`

Checked by `cpp/build_md.py`: the solution passes all 14 tests and the starter fails 11 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### D-lru: drill sy-lru-cache: least recently used cache

Where: `drill sy-lru-cache (E8)`, a drill, pattern `cache`, difficulty 3, pace 1500 seconds. Widget `code`, `language: "cpp"`, 7 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Hidden `postlude`:

```cpp
#include <cstdio>
#include <string>
#include <vector>

// hidden driver: "p k v" puts, "g k" gets; the result lists every get (value or -1)
std::vector<int> drive(int capacity, const std::vector<std::string>& ops) {
    LRU cache(capacity);
    std::vector<int> out;
    for (const auto& op : ops) {
        int k = 0, v = 0;
        if (op[0] == 'p') { std::sscanf(op.c_str(), "p %d %d", &k, &v); cache.put(k, v); }
        else { std::sscanf(op.c_str(), "g %d", &k); out.push_back(cache.get(k)); }
    }
    return out;
}
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
#include <list>
#include <unordered_map>

// A cache of at most `capacity` keys. get(k) returns the value or -1, and counts as a use.
// put(k, v) stores or updates k (also a use); when over capacity, drop the least recently used key.
// Both calls take constant time on average.
class LRU {
public:
    explicit LRU(int capacity) : capacity_(capacity) {}
    int get(int key) {
        auto it = values_.find(key);
        return it == values_.end() ? -1 : it->second;      // does not count as a use yet
    }
    void put(int key, int value) {
        values_[key] = value;
        if (static_cast<int>(values_.size()) > capacity_) values_.erase(values_.begin());   // not the oldest
    }
private:
    int capacity_;
    std::unordered_map<int, int> values_;
};
```

Reference solution:

```cpp
#include <list>
#include <unordered_map>

class LRU {
public:
    explicit LRU(int capacity) : capacity_(capacity) {}
    int get(int key) {
        auto it = where_.find(key);
        if (it == where_.end()) return -1;
        order_.splice(order_.begin(), order_, it->second);   // move to the front: most recent
        return it->second->second;
    }
    void put(int key, int value) {
        if (capacity_ <= 0) return;
        auto it = where_.find(key);
        if (it != where_.end()) {
            it->second->second = value;
            order_.splice(order_.begin(), order_, it->second);
            return;
        }
        order_.emplace_front(key, value);
        where_[key] = order_.begin();
        if (static_cast<int>(order_.size()) > capacity_) {
            where_.erase(order_.back().first);
            order_.pop_back();
        }
    }
private:
    int capacity_;
    std::list<std::pair<int, int>> order_;                       // front = most recent
    std::unordered_map<int, std::list<std::pair<int, int>>::iterator> where_;
};
```

Hidden tests (`setup` then `call` and its `expect`):

- `drive(2, {"p 1 10", "p 2 20", "g 1", "p 3 30", "g 2", "g 3", "g 1"})` expects `[10, -1, 30, 10]`
- `drive(1, {"p 1 5", "p 2 6", "g 1", "g 2"})` expects `[-1, 6]`
- `drive(2, {"p 1 1", "p 2 2", "p 1 9", "p 3 3", "g 1", "g 2", "g 3"})` expects `[9, -1, 3]`
- `drive(3, {"g 7"})` expects `[-1]`
- `drive(2, {"p 1 1", "p 2 2", "g 1", "g 1", "p 3 3", "g 2", "g 1"})` expects `[1, 1, -1, 1]`
- `drive(0, {"p 1 1", "g 1"})` expects `[-1]`
- `drive(3, {"p 1 1", "p 2 2", "p 3 3", "p 4 4", "g 1", "g 2", "g 3", "g 4", "p 5 5", "g 2", "g 3", "g 4", "g 5"})` expects `[-1, 2, 3, 4, -1, 3, 4, 5]`

Checked by `cpp/build_md.py`: the solution passes all 7 tests and the starter fails 5 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### D-token-bucket: drill sy-token-bucket: a rate limiter

Where: `drill sy-token-bucket (E8)`, a drill, pattern `rate-limiter`, difficulty 2, pace 900 seconds. Widget `code`, `language: "cpp"`, 7 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Hidden `postlude`:

```cpp
#include <vector>

std::vector<int> drive(long long rate, long long burst, const std::vector<long long>& times) {
    TokenBucket b(rate, burst);
    std::vector<int> out;
    for (long long t : times) out.push_back(b.allow(t) ? 1 : 0);
    return out;
}
```

Starter (the learner sees this; it compiles and fails the tests):

```cpp
// rate tokens a second refill continuously, up to burst tokens. The bucket starts full.
// allow(now_ns) is called with non-decreasing times in nanoseconds. It returns true and spends one token
// if a whole token is available, else false. Use integers only: no floating point.
class TokenBucket {
public:
    TokenBucket(long long rate, long long burst) : rate_(rate), burst_(burst), tokens_(burst) {}
    bool allow(long long now_ns) {
        (void)now_ns;
        if (tokens_ < 1) return false;     // never refills
        --tokens_;
        return true;
    }
private:
    long long rate_, burst_, tokens_;
};
```

Reference solution:

```cpp
// Tokens are counted in billionths of a token, so a nanosecond at `rate` per second adds exactly `rate` units.
class TokenBucket {
public:
    TokenBucket(long long rate, long long burst)
        : rate_(rate), cap_(burst * kUnit), units_(burst * kUnit) {}
    bool allow(long long now_ns) {
        units_ += (now_ns - last_) * rate_;
        if (units_ > cap_) units_ = cap_;
        last_ = now_ns;
        if (units_ < kUnit) return false;
        units_ -= kUnit;
        return true;
    }
private:
    static constexpr long long kUnit = 1000000000LL;
    long long rate_, cap_, units_;
    long long last_ = 0;
};
```

Hidden tests (`setup` then `call` and its `expect`):

- `drive(1000, 3, std::vector<long long>{0, 0, 0, 0})` expects `[1, 1, 1, 0]`
- `drive(1000, 3, std::vector<long long>{0, 0, 0, 0, 1000000, 1000000})` expects `[1, 1, 1, 0, 1, 0]`
- `drive(1000, 1, std::vector<long long>{0, 500000, 1000000, 1500000, 2000000})` expects `[1, 0, 1, 0, 1]`
- `drive(2, 2, std::vector<long long>{0, 0, 0, 250000000, 500000000, 1000000000})` expects `[1, 1, 0, 0, 1, 1]`
- `drive(10, 5, std::vector<long long>{0, 1000000000, 1000000001})` expects `[1, 1, 1]`
- `drive(1000000000, 2, std::vector<long long>{0, 0, 0, 1, 2, 3})` expects `[1, 1, 0, 1, 1, 1]`
- `drive(100, 3, std::vector<long long>{1000000000000, 1000000000000, 1000000000000, 1000000000000})` expects `[1, 1, 1, 0]`

Checked by `cpp/build_md.py`: the solution passes all 7 tests and the starter fails 4 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

### D-bits: drill sy-bits: powers of two and byte order

Where: `drill sy-bits (E8)`, a drill, pattern `bits`, difficulty 2, pace 600 seconds. Widget `code`, `language: "cpp"`, 15 hidden tests (function mode, `compare: "equal"` unless a number is a double). Checked below.

Starter (the learner sees this; it compiles and fails the tests):

```cpp
// next_pow2(x): the smallest power of two >= x (1 for x = 0 or 1). x is at most 2^30.
// is_pow2(x): true for 1, 2, 4, 8, ... and false for 0.
// popcount(x): the number of 1 bits. bswap32(x): reverse the four bytes of x.
unsigned next_pow2(unsigned x) { return x; }
bool is_pow2(unsigned x) { return x % 2 == 0; }
int popcount(unsigned x) { return static_cast<int>(x); }
unsigned bswap32(unsigned x) { return x; }
```

Reference solution:

```cpp
unsigned next_pow2(unsigned x) {
    unsigned p = 1;
    while (p < x) p <<= 1;
    return p;
}
bool is_pow2(unsigned x) { return x != 0 && (x & (x - 1)) == 0; }
int popcount(unsigned x) {
    int n = 0;
    while (x) { x &= x - 1; ++n; }      // clears the lowest set bit
    return n;
}
unsigned bswap32(unsigned x) {
    return (x >> 24) | ((x >> 8) & 0x0000FF00u) | ((x << 8) & 0x00FF0000u) | (x << 24);
}
```

Hidden tests (`setup` then `call` and its `expect`):

- `(long long)next_pow2(0u)` expects `1`
- `(long long)next_pow2(5u)` expects `8`
- `(long long)next_pow2(8u)` expects `8`
- `(long long)next_pow2(1000u)` expects `1024`
- `(long long)next_pow2(1073741824u)` expects `1073741824`
- `is_pow2(0u)` expects `false`
- `is_pow2(6u)` expects `false`
- `is_pow2(64u)` expects `true`
- `is_pow2(4294967295u)` expects `false`
- `popcount(0u)` expects `0`
- `popcount(4294967295u)` expects `32`
- `popcount(2147483648u)` expects `1`
- `(long long)bswap32(1u)` expects `16777216`
- `(long long)bswap32(305419896u)` expects `2018915346`
- `(long long)bswap32(65280u)` expects `16711680`

Checked by `cpp/build_md.py`: the solution passes all 15 tests and the starter fails 10 of them, with g++ 13.3 and clang++ 18.1, `-std=c++17` and `-std=c++20`, `-O1 -fno-exceptions`; the solution is also clean under `-fsanitize=undefined` (and address where no `operator new` is replaced). Expected values come from an independent Python model in the same file.

## Python items

Both items use the E14 `data` field of the `code` widget. Pure standard library (`csv`, `struct`), `language: "python"`, `compare: "equal"` unless noted. The data files are generated by the scripts below, deterministic (own linear congruential generator, no `random` module), so the level agent can regenerate and compare the checksums of the lines quoted. Files go in `app/content/data/systems/`. Both were checked with the solutions and starters in `systems/level4/pytest_run/` (solution passes every test, starter fails 6 of 7 and 4 of 4) and the expected values were computed by a second program (`level4/latencies_answers.py`, `level3/feed_answers.py`).

### P-latency-report: l17-measuring-latency (Python, E14)

Screen: the `code` screen after the coordinated-omission worked example, difficulty 3. `data: { "latencies.csv": "content/data/systems/latencies.csv" }`; file 47,587 bytes, header `seq,intended_us,sent_us,done_us`, 2,000 rows, regenerated by:

```python
# Generates latencies.csv for l17 (E14 data file): a closed-loop client sending 10,000 requests a second.
# Deterministic: own LCG. Run: python3 -I make_latencies_csv.py   (writes latencies.csv next to this file)
class Lcg:
    def __init__(self, s): self.s = s
    def next(self, n):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) & (2**64 - 1)
        return (self.s >> 33) % n
g = Lcg(11)
rows = []
done_prev = 0
for seq in range(2000):
    intended = seq * 100                      # one request every 100 us
    sent = max(intended, done_prev)           # closed loop: wait for the previous reply
    service = 30 + g.next(21)                 # 30..50 us
    if g.next(100) == 0: service += 200       # 1% slow replies
    if seq == 1000: service += 50000          # one 50 ms stall
    done = sent + service
    rows.append((seq, intended, sent, done)); done_prev = done
with open('latencies.csv', 'w') as f:
    f.write("seq,intended_us,sent_us,done_us\n")
    for r in rows: f.write("%d,%d,%d,%d\n" % r)
```

Starter:

```python
import csv

def report(path):
    """Read latencies.csv (seq, intended_us, sent_us, done_us). A closed-loop client sent each request
    when the previous reply arrived. Return nearest-rank percentiles (rank = ceil(p * n / 100)) of
    done - sent ("sent") and of done - intended ("true"), and the mean of the true latency."""
    with open(path) as f:
        rows = list(csv.DictReader(f))
    sent = sorted(int(r["done_us"]) - int(r["sent_us"]) for r in rows)
    mid = sent[len(sent) // 2]
    return {"p50_sent": mid, "p99_sent": mid, "p999_sent": mid,
            "p50_true": mid, "p99_true": mid, "p999_true": mid,
            "mean_true": sum(sent) / len(sent)}
```

Reference solution:

```python
import csv

def nearest_rank(values, permille):
    s = sorted(values)
    rank = max(1, -(-permille * len(s) // 1000))      # ceil(permille * n / 1000) in integers
    return s[rank - 1]

def report(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    sent = [int(r["done_us"]) - int(r["sent_us"]) for r in rows]
    true = [int(r["done_us"]) - int(r["intended_us"]) for r in rows]
    return {
        "p50_sent": nearest_rank(sent, 500), "p99_sent": nearest_rank(sent, 990), "p999_sent": nearest_rank(sent, 999),
        "p50_true": nearest_rank(true, 500), "p99_true": nearest_rank(true, 990), "p999_true": nearest_rank(true, 999),
        "mean_true": sum(true) / len(true),
    }
```

Hidden tests: `report('latencies.csv')['p50_sent']` expects 40; `['p99_sent']` 50; `['p999_sent']` 248; `['p50_true']` 49; `['p99_true']` 48821; `['p999_true']` 49911; `['mean_true']` 10584.622 (`compare: "isclose"`, `tol: { "abs": 0.001 }`). The other statistics quoted in l17 (p90 true 38,308; 875 late requests) are exact too: p90 by the same function with `permille = 900`, late requests `sum(1 for r in true if r > 100)`.

### P-feed-summary: homework-3 item 1 (Python, E14)

Difficulty 3. `data: { "feed.hex": "content/data/systems/feed.hex" }`; file 9,849 bytes, 201 lines of 48 hex characters (one 24-byte frame each, the l14 layout), regenerated by:

```python
# Generates feed.hex for homework-3 (E14 data file). Deterministic: own LCG, no random module.
import struct
class Lcg:
    def __init__(self, s): self.s = s
    def next(self, n):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) & (2**64 - 1)
        return (self.s >> 33) % n
g = Lcg(2027)
dropped = {17, 18, 90, 150, 151, 152}
frames = []
for seq in range(1, 207):
    r = g.next(100)
    t = ord('A') if r < 70 else (ord('X') if r < 85 else ord('T'))
    side = ord('B') if g.next(2) == 0 else ord('S')
    price = 10000 + g.next(41) - 20
    qty = 10 * (1 + g.next(20))
    frames.append((seq, struct.pack('>BBHIIIiI', t, side, 7, seq, 1000 + seq, qty, price, 36000000 + seq * 5)))
frames = [f for f in frames if f[0] not in dropped]
order = [f for f in frames]
i = [k for k, f in enumerate(order) if f[0] == 40][0]; order[i], order[i + 1] = order[i + 1], order[i]   # 41 arrives before 40
j = [k for k, f in enumerate(order) if f[0] == 100][0]; order.insert(j + 1, order[j])                     # 100 arrives twice
open('feed.hex', 'w').write("\n".join(f[1].hex() for f in order) + "\n")
print(len(order), "lines")
```

Starter:

```python
import struct

def summarise(path):
    """Each line of feed.hex is one 24-byte frame in hex (>BBHIIIiI: type, side, instrument, seq, id, qty, price, time).
    Return the number of unique sequence numbers, the sorted list of missing ones (1 up to the largest),
    the number of trades (type 84, 'T') and their volume-weighted average price in pence."""
    frames = [struct.unpack(">BBHIIIiI", bytes.fromhex(l.strip())) for l in open(path) if l.strip()]
    return {"unique": len(frames), "missing": [], "trades": 0, "vwap": 0.0}
```

Reference solution:

```python
import struct

def summarise(path):
    seen, rows = set(), []
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        kind, side, instrument, seq, order_id, qty, price, time = struct.unpack(">BBHIIIiI", bytes.fromhex(line))
        if seq in seen:
            continue                      # a duplicate from the second feed
        seen.add(seq)
        rows.append((kind, qty, price))
    trades = [(q, p) for k, q, p in rows if k == ord("T")]
    return {
        "unique": len(seen),
        "missing": sorted(set(range(1, max(seen) + 1)) - seen),
        "trades": len(trades),
        "vwap": sum(q * p for q, p in trades) / sum(q for q, _ in trades),
    }
```

Hidden tests: `summarise('feed.hex')['unique']` expects 200; `['missing']` `[17, 18, 90, 150, 151, 152]`; `['trades']` 31; `['vwap']` 10001.412844036697 (`isclose`, relative 1e-9). Frame 41 arrives before frame 40, and frame 100 arrives twice, which is why the first line count is 201 and the unique count 200.


## Number checks

Every number in this brief was computed twice by independent methods. The scripts are committed in `docs/briefs/systems-scripts/` (`brief`, `cpp`, `level1` to `level4`); `systems/levelN/...` and `cpp/...` paths in this brief mean `docs/briefs/systems-scripts/levelN/...` and `docs/briefs/systems-scripts/cpp/...`. The level agent recomputes each number itself before stating it.

| Level | Quantity | Method A | Method B | Script |
| --- | --- | --- | --- | --- |
| 1 | Human-scale times (100 s, 1 d 3 h 46 min 40 s, 115.7 d, 694.4 d), budget 5 µs, 50 reads, fibre round trips 55.7, 6.4, 4.27, 2.13 ms | floats | integer picoseconds and Fractions | `level1/l1_latency.py` |
| 1 | Cache misses: 4, 8, 8, 16, 2, 2; matrix 8, 64, 8 (homework and review only); LRU sweeps 4 and 15 of 96 and 120 reads, sets and ways 4, 4, 3, 3; L1 512, 2,048, 16,384, 125,000, 1,000,000 | OrderedDict LRU per set | list with recency stamps, then a closed form | `level1/l2_cache.py` |
| 1 | Page walk: 39,548; indexes 254, 232, 225, 213, offset 3,656; 35,600; TLB 0.39%; 262.144 ms; 786.4 ms | shifts and masks | divmod and bit strings | `level1/l3_vm.py` |
| 1 | Struct offsets and sizes (24, 16, 32, 24, 48, 32, 28), straddles 2 of 8 | hand algorithm | ctypes (x86-64), and clang wasm32 `static_assert` | `level1/l4_layout.py` |
| 1 | Two-bit and one-bit mispredicts (1, 0, 8, 4, 3, 5, 11, 6); random 5,064 of 10,000, sorted 2 | state machine | transition-table lookup | `level1/l5_branch.py` |
| 1 | Desk run, branch against mask at `-O0` and `-O1` | g++ 13.3 | clang++ 18.1 (two runs each) | `level1/bench.cpp` |
| 1 | Review and homework values (12, 35,600, 524.288 ms, 12, 5, 129.97 ns, 115 ns) | formulas | Fractions | `review_numbers.py`, `level1/l1_review_homework.py` |
| 2 | Interleavings and final values (20, 1,680, 924; 18/2; 1,404/270/6; 9/9/2; 4/2 of 6; SB 1/1/4; publication; lost wakeup 1 of 6; deadlock 2 of 6, 6 of 168, 0 of 142) | recursive enumeration over a mutable state | memoised dynamic programme over immutable states (and, for `final_counts`, the C++ solution) | `level2/interleave.py`, `level2/more.py` |
| 2 | Costs (3.0 cores, 7.8 GiB, 0.1 s, 20 s, 0.24 s, 240 times, 480 times, 60 times) | floats | Fractions | `level2/l2_numbers.py` |
| 3 | Syscall counts and times, partial reads (4+4, 41+16, 8 frames and 6 left), handshake 90 ms against 30, held back 50 and 20,000, 50 times multicast, A/B 100 against 10,000 | formulas | event-time model, seeded simulation (87 against 100, within error), `divmod` | `level3/l3_numbers.py`, `review_numbers.py` |
| 3 | Wire bytes (`41 42 01 02 ...`, `ff ff ff e7`, `54 53 00 0c ...`) and decode | `struct.pack` | manual shifts and the C++ solution | `cpp/problems_l3.py` |
| 3 | `feed.hex` answers: 200 unique, 6 missing, 31 trades, VWAP 10,001.4128 | `struct.unpack` with Fractions | `int.from_bytes` with floats | `level3/feed_answers.py` |
| 4 | Costs (40 ms, 1.2 ms, 2,500 and 2,700 ns, 36,000, 48,000, 256, 6,144, 8,192, 196,608, 429.5 s) and `sizeof(Handler)` 18,032 | floats | Fractions; g++ `sizeof`; wasm32 `static_assert` | `level4/l4_numbers.py`, `review_numbers.py`, `cpp/problems_l4b.py` |
| 4 | Percentiles (10, 10, 1,000, 1,000; 5-sample set) and pooled p99 (1,000 against 505) | sort and rank with `ceil` and a 1e-9 guard | exact rational rank (the NumPy `inverted_cdf` discrepancy at p99.9 is recorded in the l17 edge case) | `cpp/problems_l4.py`, `review_numbers.py` |
| 4 | `latencies.csv` percentiles (40, 50, 248; 49, 38,308, 48,821, 49,911), mean 10,584.622, 875 late | pure Python and Fractions | NumPy sort with integer ranks | `level4/latencies_answers.py` |
| 4 | Ring wrap at 2^32 (slots 1, 2, 3, 0; capacity 3 maps two counters to slot 0) | C++ run | Python modular arithmetic | `level4/wrap.cpp` |
| all | Every hidden test's `expect` | an independent Python model | the C++ solution under g++ and clang++, `-std=c++17` and `c++20`, `-O1 -fno-exceptions`, plus UBSan | `cpp/harness.py`, `cpp/build_md.py` (summary in `cpp/summary.json`) |

The handler was also fuzzed: 400 random streams (drops, swaps, duplicates, out-of-range prices and ids, random read sizes) matched the Python model on best bid, best ask, gaps and applied frames, with the solution built under AddressSanitizer and UBSan (`cpp/problems_l4b.py`, run as `python3 -I problems_l4b.py`).

Unresolved for the level agents (not blockers): (1) `std::atomic`, `<mutex>` and `<thread>` are not verified to compile under YoWASP libc++ (no pthreads); no code problem here needs them, and inbox bullet 1 asks for a check; (2) the allocation counter replaces global `operator new` in a `prelude`; if the app's `leakCheck` wrapper conflicts, ask for an `allocCheck` harness flag (inbox bullet 2); (3) the starters were checked with g++ 13.3 and clang++ 18.1, not with the app's clang 21, so run the app's checker on every starter and solution once; the starter of P-format-price fails five tests on its text whatever the optimiser does, so its failing no longer depends on the `std::vector` allocation surviving `-O1` (the `g_allocs` test is a bonus check on solutions that allocate); (4) the `interleave` canvas parameter names are the builder's, not this brief's.
