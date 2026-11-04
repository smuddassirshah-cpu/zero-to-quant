# Report: systems level 4 (Low-latency C++)

Author: content agent, 4 November 2026. Brief: `docs/briefs/systems.md` `## Level 4`, shared sections, P-pool, P-format-price, P-ring, P-percentile, P-latency-hist, P-handler, D-lru, D-token-bucket, D-bits, P-latency-report. Builders and checks are in the scratchpad `systems-4` folder (`l15.py` to `l18.py`, `rh4.py`, `hw4.py`, `drills.py`, `code_parse.py`, `voice.py`, `chk.py`, `starters.py`).

## Files

| File | Screens or items | Quiz | Notes |
|---|---:|---:|---|
| `l15-no-allocation` | 12 | 4 | tap hook (console, l3 to l6), explore (console, frames of 0 to 4 allocations), cost table, pool tap (array), pool cost table, P-format-price (`allocCheck`), trap, full-pool edge, generalise (names the conference talks once), P-pool (`allocCheck`), drill, 1,000-order transfer |
| `l16-ring-buffer` | 12 | 4 | explore (array stepper over 11 frames, table of two cells), counter-to-slot table, wrap listing and table, false-sharing grid tap, stall cost table, producer `order` (3 distractors), trap, full-ring edge, generalise, P-ring, drill, ring-size transfer |
| `l17-measuring-latency` | 12 | 4 | bars hook (`showMean`), explore (slow-request slider), percentile table, coordinated-omission choice on a console, Python report (E14 `latencies.csv`), trap, float-edge numeric, generalise, P-percentile, timing table, drill, fleet p99 transfer |
| `l18-feed-handler` | 11 | 4 | `order` hook (2 distractors), explore (directed `graph`, pill nodes, frames), budget table, structure table, A/B tap (array), unordered_map trap, split-read table, generalise, P-handler (`allocCheck`, prelude), drill, 50-instrument transfer |
| `review-4` | 9 items, difficulty 2 to 3 | | 1 multi, 6 numeric, 2 tables (items 4 and 6), as the brief says |
| `homework-4` | 6 items, difficulty 4, 5, 5, 4, 4, 3 | | 1 code (P-latency-hist, `allocCheck`), 2 `parts` (4 numeric, 1 choice), 3 longform (rubric 10), 4 `parts` (3 numeric, 1 choice), 5 `order` with 3 distractors, 6 numeric |
| `drills/sy-lru-cache`, `sy-token-bucket`, `sy-bits` | 7, 7, 15 tests | | C++, patterns `cache`, `rate-limiter`, `bits`, paces 1500, 900, 600; three rows appended to `drills/index.json` |
| `content/data/systems/latencies.csv` | 2,000 rows, 47,587 bytes | | copied from `docs/briefs/systems-scripts/level4/latencies.csv`; unchanged |

Skills follow the brief: l15 `sy-latency` and `sy-memory`, l16 `sy-latency` and `sy-concurrency`, l17 `sy-latency`, l18 `sy-latency` and `sy-os`. Every skill appears in review and homework. No `course.json` change proposed.

## Results
- Validator: 0 errors. Voice scan over every prose, question, feedback, explanation, hint, `how` and drill brief: 0 sentences over 20 words, 0 explanations over three sentences, no exclamation marks, no em-dashes. Choice keys are not visibly longer than distractors (script `chk.py`, every `choice` has `shuffle: true`).
- Playthrough with `--local-cdn`, desktop and `--mobile` (390 px): l15, l16, l17, l18 (16, 16, 16, 15 checks, quiz 4 of 4 each), review-4 (9 of 9), homework-4 (6 of 6, 30 of 30 marks, parts checks), and the three drills (7, 7 and 15 of 15 tests with the model solution, starter fails) all passed. I looked at the screenshots of every lesson screen at 390 px (contact sheets) and of the desktop explore screens. Fixes made after looking: the pool tap no longer shows the head pointer before the answer; the wrap listing was narrowed so it fits 390 px; the bars hook lost its value labels (they collided with the mean label); the pipeline graph uses one-word pill labels so nodes no longer overlap.
- Starters fail: with each code `solution` replaced by its starter, the app's clang 21 and Pyodide failed l15 (format-price test 2 and pool test 3), l16 (ring test 1), l17 (Python test 2 and percentile test 1), l18 (handler test 3) and homework-4 item 1 (histogram test 1). The real solutions pass all tests. Files were rebuilt afterwards.

## Numbers (computed twice; asserted in the builders)
- l15: 4 x 50 ns = 200 ns, 200 ns x 200,000 = 40 ms, 4%; one allocation 10 ms (Fractions agree); 3 x 2 ns x 200,000 = 1.2 ms against 30 ms, 25 times; pool traces by a stack model and by the linked-list model of the solution (all drill, review and quiz answers agree); 1,000 x 1.5 = 1,500 slots, 36,000 and 48,000 bytes, 25% saved; quiz 37.5 ms, 24,000 bytes.
- l16: ring traces by counters and by a deque (all P-ring `drive` expectations re-derived by both); 5 and 3 = slot 1 and 20 and 7 = slot 4; 4,294,967,293 and 3 = 1, 4,294,967,295 mod 3 = 0, 0 mod 3 = 0, 2^32 / 10^7 = 429.5 s; 10^7 x 60 ns = 600 ms, 10 ms; 200, 256, 6,144, 5,000, 8,192, 196,608 (192 KiB); quiz 13, 2,048.
- l17: 19.9 (Fractions and float); nearest rank by Fraction ranks and by integer permille ranks (p50 10, p99 10, p99.9 1,000, p99 jumps at 11 slow requests, checked for every k from 0 to 30); `latencies.csv`: 40, 50, 248 and 49, 38,308, 48,821, 49,911, 875 late, mean 10,584.622 (Fractions and floats, and by `level4/latencies_answers.py`); clock 40/50 = 80% and 0.04 ns; fleet 1,000, 505, 1,000; quiz p75 8, mean 39.
- l18: 1,000 + 200 + 300 + 500 + 500 = 2,500, slack 500, 2,700, 7,500; 40%; 201 levels, 1,608, 16,384, 18,032 (g++ and clang wasm32 `static_assert`, `sz.cpp`); A/B arrivals by two models (applied 1A, 2A, 4A, 5A, gap 1); reads 50, 40, 80 carry 2, 1, 4 with 2 left; 50 x 18,032 = 901,600 = 880.5 KiB, 28 caches; quiz 1,500, 4, 32,768.
- Review (fresh, none in a lesson): 18 ms; pool of 4 gives slot 1; ring of 32 with head 70 and tail 85 gives 15 and 21; ring of 2 third pop 40; 970 at 12 and 30 at 500 give mean 26.64 and p99 500; p60 of eight samples 6; 2,900 ns; 31 and 41 bytes give 3 frames.
- Homework (fresh): 2,400 x 1.25 = 3,000 slots, 60,000 bytes, 300 messages, 512 slots, 12,288 bytes; 60,000 is 27,232 over 32,768 and 72,288 is 39,520 over; hosts at 20 and 800 us give 410, 800 and, with 15 slow, 20 (host B alone stays 800); 40 ms at 250 us gives 160; histogram tests by a `bit_length` model and a `log2` loop model.

## Deviations from the brief
- Difficulty: the validator caps lesson screens at 3, so P-ring and P-handler (brief: 4) are difficulty 3.
- Fresh numbers (DECISIONS): brief review items 2 to 9 and homework 2, 4, 5 and 6 repeated lesson numbers or answers, so they have new ones (above); item 1 changes the lines. Homework 1 keeps the brief's tests except the first three, which use 970 at 10 ns and 30 at 1,000 ns instead of 990 and 10 (lesson 17). Homework 5 asks for the consumer's `pop`, not the push the lesson ordered. The l15 quiz and l18 drill also use new figures.
- Float edge (l17): the brief says 0.999 x 1,000 comes out as 999.0000000000001. In a double `0.999 * 1000` is exactly 999.0; the slip is `99.9 / 100 * 1000` (999.0000000000001). The lesson says so. NumPy `inverted_cdf` gives 1,000 for 999 samples at 10 and one at 1,000 on NumPy 2.0.2 (the Pyodide 0.27.7 version, checked in a venv) and on 2.5.3.
- l18 A/B policy is the brief's (apply at or above the expected number, count the gap, drop below it), so frame 3 on feed B is lost when 4 on feed A arrives first. The explanation says this and names the better handler.
- Drill extras: `constraints`, `hint` and `notes` are authored for the three drills; their `how` text states the test counts. Drill tests use the `drive` postlude of the brief (`args` with `types` for D-lru and D-token-bucket, the brief's expression calls for D-bits).
- P-handler needs `frame()` and `cat()`: they are in the widget `prelude`, which includes `<vector>` itself.

## Backlog
Four bullets under "Raised later (systems level 4)" in `docs/BACKLOG-INBOX.md` (bars value axis and mean label, no percentile marker, graph pills on a phone, grid text size).
