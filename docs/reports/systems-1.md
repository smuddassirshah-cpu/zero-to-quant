# Report: systems level 1 (Memory and the machine)

Author: content agent, 4 November 2026. Brief: `docs/briefs/systems.md` `## Level 1`, with the course context, shared runtime facts, engine limits, E items, code problems P-translate, P-struct-size, P-mispredicts, P-cache-sim and the number checks. Followed `docs/LEVEL-BRIEF.md` and `docs/AUTHORING.md` (engine pass C: `parts` with mixed kinds, section 5).

## Files written

All in `app/content/courses/systems/` (plus `app/content/manifest.json`, rewritten by the validator).

| File | Screens or items | Quiz | Canvases and widgets |
|---|---:|---:|---|
| `l1-latency-numbers.json` | 11 screens (difficulty 1 to 3) | 4 | `order` hook; log `number-line` with a log control and a derive caption; `table` widgets; `table` canvas of distances; trap `choice`; drill `table` (tag `time-budget`, pace 450) |
| `l2-caches.json` | 9 screens | 4 | `array` (64 doubles, `wrap: 8`) with `tap-regions`; `grid` cache slots with a 16-frame LRU stepper; `grid` sets; `table` widgets (4 columns at most); drill `table` (tags `stride`, `cache-lines`, pace 540); transfer on a matrix `grid` (tag `loop-order`) |
| `l3-virtual-memory.json` | 11 screens | 4 | page-table `table` canvas; `number-line` explore with an address slider and a live translation caption; `console` bit groups; `code` P-translate; `order` derive with one distractor; drill `table` (tags `page-table`, `page-fault`, pace 540); transfer (tag `huge-pages`) |
| `l4-object-layout.json` | 11 screens | 4 | 3 × 8 byte `grid` with `tap-regions`; `grid` explore with a field-order frames control; `console` listings; `table` widgets; `code` P-struct-size; drill `table` (tags `struct-size`, `padding`, pace 360); straddle `grid` transfer (tag `cache-line-straddle`) |
| `l5-branches.json` | 10 screens | 4 | `array` history with `tap-regions`; `array` explore with a 9-frame counter stepper; `console` seeded run, mask listing and desk run; `code` P-mispredicts; drill `table` (tag `branch-predictor`, pace 540); transfer (tag `mispredict-cost`) |
| `review-1.json` | 9 items, difficulty 2 to 4 | | the brief's nine items in order, every one tagged and paced, skills as the brief's rule (items 5 and 6 `sy-os`, item 8 `sy-latency`) |
| `homework-1.json` | 7 items, difficulty 3 to 5 | | 1 `parts` numeric, numeric, numeric, choice (d3); 2 `code` P-cache-sim (d4); 3 `longform`, 10-point rubric and model (d4); 4 `parts`, five numeric (d4); 5 `table` (d4); 6 `parts`, four numeric (d5); 7 `choice` (d3) |

Every lesson: skills as `course.json` (`sy-memory`; l3 adds `sy-os`, l5 adds `sy-latency`), one trap, one edge case, a drill screen with a pace in the prose, a follow-up transfer, no more than two non-task screens (all five have none). The free paper is named once, in l1 screen 3. Round figures are called round, to be known to a power of ten, in l1 screens 1 and 8 and in every lesson's drill prose; l4 says once that pointers are 4 bytes here and 8 on a desktop.

## Validator

`node tools/validate.mjs`: 0 errors. One warning for these files: l1 screen 1 (the `order` hook, as the brief specifies) has no canvas.

## Voice

`VOICE_BASE=<repo>/app/content/courses/systems python3 docs/reviews/voice-scan.py`: 0 explanations over three sentences, 0 sentences over 20 words (2,767 scanned). No exclamation marks, em-dashes or American spellings (`center` appears only as a table `align` value).

## Playthrough

From `app/`, with `--local-cdn <scratchpad>/pkgs`, all files in one run, then again with `--mobile` (390 px, with screenshots):

| File | Desktop | Mobile |
|---|---|---|
| l1-latency-numbers | ok, 15 checks, quiz 4/4 | ok |
| l2-caches | ok, 13 checks, quiz 4/4 | ok |
| l3-virtual-memory | ok, 15 checks (C++ compiled), quiz 4/4 | ok |
| l4-object-layout | ok, 15 checks (C++ compiled), quiz 4/4 | ok |
| l5-branches | ok, 14 checks (C++ compiled), quiz 4/4 | ok |
| review-1 | ok, recorded 9 of 9 | ok |
| homework-1 | ok, marked 7 of 7, 33 of 33 marks; parts checks ok | ok |

"All passed" both times; homework-1 was replayed at both widths after its last prose change. I looked at the screenshots (desktop with `--why`, and 390 px) and fixed what I saw: the array index row under the l2 cells (now hidden), an l2 explanation whose range washes did not show (now one range plus bold misses), and a struct in homework item 5 that wrapped badly inline (now a code block). The first full run failed only the playthrough's homework parts check, which assumes the parts item is the paper's first item; the four-part item now comes first (backlog bullet).

## C++ in the app (YoWASP clang 21, `-O1`, no exceptions)

The brief's C++ was checked with g++ 13.3 and clang++ 18.1 natively. I copied `app/` into my scratchpad, wrapped each of the four problems as a sample drill there (tests rebuilt as `call` plus JSON `args`, `types` and `expect`), and ran `node tools/playthrough.mjs --drill ... --local-cdn <pkgs>` in that copy, patched to print how many tests the starter passes:

| Problem | Model solution | Starter |
|---|---|---|
| P-translate (l3) | 10 of 10 | passes 4 of 10 (fails 6, as the brief) |
| P-struct-size (l4) | 15 of 15 | passes 5 of 15 (fails 10, as the brief) |
| P-mispredicts (l5) | 10 of 10 | passes 5 of 10 (fails 5, as the brief) |
| P-cache-sim (homework) | 10 of 10 | passes 4 of 10 (fails 6, as the brief) |

No difference from the native results. The lesson and homework playthroughs then ran each model solution through the real widgets again. Code is copied exactly from the brief; P-struct-size and P-cache-sim solutions include headers the starters do not (`<algorithm>`, `<functional>`, `<list>`), so the precompiled header built for the starter is not used for those solutions. That only costs compile time.

## Numbers

Every number stated was computed twice by my own script (`<scratchpad>/systems-1/numbers.py`: method A floats or a direct LRU simulation, method B Fractions, bit strings or a second simulation) and checked against the brief's scripts in `docs/briefs/systems-scripts/level1/`, which I also ran. Every hidden-test `expect` was recomputed by an independent Python model (`<scratchpad>/systems-1/code_problems.py`) and asserted equal to the brief's value.

- l1: human time 100 s, 100,000 s (1 d 3 h 46 min 40 s), 10,000,000 s (115.7 days), 60,000,000 s (694.4 days, 1.9 years); L1 to disk 7 powers; 5 µs budget, 50 DRAM or 5,000 L1 reads; Frankfurt 6.4 ms fibre, 4.27 ms air, 2.13 ms saved, 3.2 ms one way; New York floor 55.7 ms, one way 27.85 ms (18.58 ms through air); NVMe/DRAM 1,000; drill 50, 1,000, 5, 120, 100; 2 µs / 20 ns = 100; quiz 250, 3.2, 10/50/4/100 µs.
- l2: hook 4 misses, 28 hits, 87.5%; LRU 4 of 96 and 15 of 120; gap 256 one way 16, two ways 2, gap 320 2 (87.5%); lines 0, 4, 8, 0: 4, 4, 3, 3 with 8, 4, 2, 1 sets; L1 512 lines, 64 sets; 64 × 64 both orders 512; address 4,160 in set 1; drill 8, 12, 15, 4, 4, 3; 1,000 × 1,000: 125,000 and 1,000,000 misses (both also simulated through a 512-line 8-way LRU), 12.5 and 100 ms; quiz 4, set 3, 3.
- l3: 0x2A7C = 10,876 → 39,548; indexes 254, 232, 225, 213, offset 3,656; walk 400 ns; reach 256 KiB, 16,384 pages, 0.39%, 32 huge pages, reach 128 MiB; 1 GiB = 262,144 pages, 262.144 ms; 256 TiB; 8,195 → 36,867; drill 35,600 (0x8B10), −1, 16,384, 6 MiB, 786,432, 786.4 ms; 1,536 huge pages; quiz 24,580, 128 KiB, 131.072 ms.
- l4: 14 of 24 padding (58%); offsets 0, 8, 16, size 24; reordered 16; order message 0, 4, 8, 12, 16, 20, 24, 28 (32) and sorted 0, 4, 8, 12, 16, 20, 22, 23 (24), 32 MB against 24 MB; edge 32 both ways (sorted data 30); `{u16, u8}` 4; `{u32, u16, double}` 16; drill 16/12, 48/32, 4/4, 16/16; straddlers 2 (structs 2 and 5), none at 32 bytes; flag gives 28; quiz 12, 8, 28.
- l5: hook misses at steps 0, 3, 4 (15 ns); `TTTNTTTN` 3; random 2.5 ms; seeded run 5,064 of 10,000 and 2 sorted (generator of `level1/l5_branch.py`, reproduced); mask saving 3.8 to 4.1 ns at `-O0`; 0.5 ms at 10%; drill 3, 11, 2, 8, 6, 4; switch 1.5 ns, 0.3 ms a second, 0.03%; quiz 1, 25 ms, 0.005 ns. Desk-run figures are quoted from the brief (`level1/bench.cpp`), not recomputed, as the brief says.
- review: 2%, 12, 35,600, 524.288 ms (distractor 488.28 for decimal GiB), 12, 5 (one-bit 8), 2.
- homework: 1,000; 600,000; 400 ns; one third; 125,000, 1,000,000, 12.5 ms, 100 ms, 512; offsets 0, 8, 16, 18 (24) and 0, 8, 10, 11 (16); TLB 0.098%, 129.97 ns, 115 ns, 11.5% (distractor 13.0% over the new cost); 1.5 ns of 5,000 ns is 0.03%.

## Where the files differ from the brief

- `parts`: used exactly as AUTHORING section 5 states (no item `widget` or `feedback`, each part with its own `question`, `widget`, `feedback`, `explain`). The brief's shapes match; homework item 6 has four parts instead of three, because part (c) asked for two numbers (115 ns and 11.5%).
- l1: the follow-up is two screens, a numeric problem (27.85 ms) then the transfer `choice` (predict, never react first), as the brief's two widgets.
- l2: worked example 1 (eviction) is the explore, a frames stepper through the 15 line fetches; the 4-line case is stated in its prose.
- l3: the transfer asks the 1,536 huge pages; "why touch and lock at start-up" is quiz item 1. A derive `order` screen (translation steps with one distractor) was added.
- l4: the trap uses the brief's `{char, double, char}`, which is the hook's struct quick-fire. The edge screen asks `{1, 2, 4, 8} × 2`; `{u16, u8}` is in the drill and the edge explanation. "Can I `memcpy` this?" is in the transfer prose and quiz item 1; the 28-byte flag is in the transfer explanation and quiz item 4.
- l5: worked example 1 (3 × 5 ns) is the hook explanation. The desk run is the trap's canvas, and the `-O1` edge reuses it.
- Table cells: the slips the brief names sit on cell-id keys (`r0c1`), because the validator refuses a cell's `wrong[].id` as a key (backlog bullet).
- Review item 2 uses `unit: "%"`.
- Homework item order: the brief's item 2 (four-part latency follow-ups) is first and the code item second, for the playthrough check above; the other items keep the brief's order.

## Conventions

Seeded data: only the brief's branch generator (x0 = 12345, x = (1103515245x + 12345) mod 2^31, taken when bit 16 is set), quoted as its result. Addresses are shown in hex with decimal beside them; every answer is decimal. No dataset files.

## course.json

No change proposed.

## Backlog

Six bullets under "Raised later (systems L1, 4 Nov)" in `docs/BACKLOG-INBOX.md`: the validator and table-cell `wrong` ids; a starter check for lesson and set code widgets in the playthrough; thousands separators and hex in `derive`; hex input for `numeric`; documenting `stopLabels` for control readouts; the playthrough homework parts check that assumes the parts item comes first.
