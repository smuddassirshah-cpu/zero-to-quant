# Report: systems level 3 (Operating systems and networks)

Author: content agent, 4 November 2026. Brief: `docs/briefs/systems.md` `## Level 3`, shared sections, P-find-gaps, P-wire, P-feed-summary.

## Files (all in `app/content/courses/systems/`, plus `app/content/data/systems/feed.hex`, 9,849 bytes, copied from `docs/briefs/systems-scripts/level3/feed.hex`)

| File | Screens or items | Quiz | Notes |
|---|---:|---:|---|
| l11-processes | 10 | 4 | strace tap hook, slider, three tables, fork choice, trap, clock edge, generalise (names Beej's guide and manual pages once), drill (pace 450), transfer table |
| l12-files-and-sockets | 9 | 4 | order hook, kernel/bypass explore, short-read table, wait/spin table, trap, recv-0 edge, generalise, drill (450), transfer choice |
| l13-tcp-and-udp | 11 | 4 | array tap hook, repair-time slider, handshake, multicast, A/B, trap, late-and-twice edge, generalise, drill (360), P-find-gaps (13 tests), TCP_NODELAY transfer |
| l14-messages-on-the-wire | 10 | 4 | hex array tap hook, byte-order frames slider, fixed point, stream, struct trap, signed edge, generalise, P-wire (12 tests), drill (450), flags transfer |
| review-3 | 9 items, difficulty 2 to 4 | | |
| homework-3 | 7 items, difficulty 3 to 5 | | 1 parts (5 numeric, d3), 2 Python code with E14 `data` (d3), 3 longform (rubric 10), 4 table, 5 parts (5 numeric, d5), 6 order with 3 distractors, 7 numeric |

Skills: l11, l12 `sy-os`; l13, l14 `sy-os` and `sy-latency`; review and homework follow the brief's rule. No `course.json` change proposed.

## Results
- Validator: 0 errors. Voice scan: 0 sentences over 20 words, 0 explanations over three sentences, no exclamation marks in prose, no em-dashes.
- Playthrough with `--local-cdn`, desktop and `--mobile` (390 px): l11, l12, l13, l14, review-3 (9 of 9) and homework-3 (7 of 7, 32 of 32 marks, parts checks) all passed. I looked at the screenshots of every lesson screen at 390 px (hex array, struct console, tables, sliders); no overlaps.
- Starters: with each code `solution` replaced by its starter, the app's clang 21 and Pyodide failed l13 (test 2), l14 (test 1) and the Python item (test 1); the real solutions pass all 13, 12 and 4 tests. Files were rebuilt afterwards.

## Numbers (computed twice: formulas or floats against Fractions, divmod carry simulation, bitmap versus set, `struct` against manual shifts and `ctypes` layout; asserted in the builders)
- l11: 16,384 / 256 / 16 calls, 3,276.8 / 51.2 / 3.2 µs, 1,024 times; 2 x 2 = 4 µs, 40% at 100,000 a second; drill 1,024 and 204.8, 128 and 25.6, 250,000 x 4 µs = 1 core; clock 500,000 x 20 ns = 10 ms (100 ms as calls); 200,000 x 0.2 µs = 40 ms, 4%, 3,279 calls (0.066%); quiz 64 calls and 12.8 µs, 20%.
- l12: 100 = 4x24+4, 1,000 = 41x24+16; 250 empty calls in 50 µs; carry runs [100,50,24,23,1] gives 4,2,1,1,0 (8 frames, 6 left, the 24-byte read parses 1) and [50,50,50] gives 6 and 6; quiz 10 frames, 5,000 calls.
- l13: 90 against 30 ms; 50, 500, 2,000, 20,000 held; 5,000,000 against 100,000 bytes (40 and 0.8 Mbit/s); 100 of 1,000,000 (simulation 87, sd 10.0); `find_gaps` tests against a set model and a bitmap model; quiz 150 ms, 2 missing, 2,000,000.
- l14: hook frame equals `struct.pack`; 70,000 = 0x11170; 10,275 = 40x256+35; -25 ends e7 (231); 36,000,000 = 02 25 51 00; 4,800,000 B/s = 38.4 Mbit/s; 61 frames and 8 spare; `ctypes` sizes 24 and 28 (flags field); 1,472/26 = 56 and 16; drill 256, 65,536, -200, 12,000 pence, 125; quiz 3,000, 24, 58.
- Review (fresh, not in any lesson): 768 calls and 153.6 µs; 6 frames and 16 left; 60 ms; 3 missing; 2,000; 156; 400.
- Homework (fresh): 80 ms gap, 100 and 8,000 held, 300,000 and 6,000,000 B/s; 12 µs and 3 µs per message gives 83,333 and 333,333 a second, 3.6 cores, 7,500 receives, 0.675 of a core (computed per datagram and per message); hand-encoded frame `54 53 00 0c ...` last bytes 12, 44, 99, 232, 251, 0; 5 MiB gives 2,560 and 64 calls, 499.2 µs saved; `feed.hex` answers 200, six gaps, 31 trades, 10,001.4128 (`feed_answers.py`).

## Deviations from the brief
- Fresh numbers (DECISIONS): the brief's review item 1 and 2, 4, 6, 7 and homework 2, 5, 6, 7 repeated lesson numbers or answers, so they have new ones (above). Item 2 asks which event forces a switch; item 4 asks what to do on a 0 from `recv` (the lesson edge is the spin loop); homework 3's model uses 30,000 a second, 0.5% loss and 100 subscribers; homework 6 is a blocking `recv` from an empty socket.
- l11 drill last row is 250,000 a second (1 core) so it does not repeat worked example 2. l14 drill and l14 reading of `-25` differ from the brief for the same reason (-200, `00 00 2e e0`, a 3,000-byte read).
- Homework item order: the parts item is first and the code item second.
- Struct in the l14 trap uses fixed-width fields (24 bytes), so the catch is byte order, not size; the 28-byte struct appears only in the flags transfer. The `P-wire` prelude uses plain `int` and `unsigned` fields as the brief gives.

## Backlog
Two bullets under "Raised later (systems level 3)" in `docs/BACKLOG-INBOX.md`.
