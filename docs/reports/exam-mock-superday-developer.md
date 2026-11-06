# Report: mock-superday-developer

Written from `## mock-superday-developer` in `docs/briefs/mocks.md` (the brief was written first, in the shape of the other superday sections).

## Files

- `app/content/exams/mock-superday-developer.json`: 6 papers and 2 checks, 17 items, 215 minutes.
- `docs/briefs/mocks-scripts/superday_developer_build.py` (route A, writes the file), `superday_developer_check.py` (route B), with `superday_lib.py` from the strats mock.
- `docs/readiness.md`: the `mock-superday-developer` status row now reads `exists`; `readiness-sums.mjs --write` then changed `app/content/readiness.json` only in the developer `mocks.present` and `mocks.missing` lists (checked with `git diff`).

| Paper | Minutes | Items | Kinds | Difficulty | Pass |
| --- | --- | --- | --- | --- | --- |
| Coding round one | 45 | 1 | Python code (14 tests) | 4 | 1 |
| Coding round two | 45 | 1 | `parts`: C++ code (7 tests), C++ code (7 more, 14 merged), choice | 5 | 1 |
| C++ | 40 | 6 | 1 `parts` (2 numeric), 4 choice, 1 C++ code with `allocCheck` (13 tests) | 3, 4, 3, 4, 3, 4 | 0.6 |
| Concurrency and systems | 25 | 5 | 3 choice, 1 numeric, 1 `parts` (2 numeric) | 3, 4, 3, 4, 4 | 0.6 |
| System design | 45 | 2 | `longform` | 5, 4 | 0.5 |
| Fit and motivation | 15 | 2 | `longform` | 3, 3 | 0.5 |

Families (first tags), all new to the mocks: `scheduled-arrival`, `asof-store`, `struct-padding`, `copy-or-move`, `shallow-copy`, `dispatch-during-construction`, `template-deduction`, `slot-pool`, `lost-updates`, `release-acquire`, `lock-ordering`, `cache-line-stride`, `queue-sizing`, `risk-gateway-design`, `tail-latency-regression`, `why-trading-systems`, `review-disagreement`.

## Results

- Validator: 0 errors; no warning names this file (the total stays at 3,983).
- Voice scan on a copy (`VOICE_BASE=<scratchpad>/vsfix/dev/`): 0 sentences over 20 words of 411, 0 explanations over three sentences.
- `python3 docs/briefs/mocks-scripts/superday_developer_check.py`: `numbers_lib: 174 of 174 checks passed`, exit 0. The fix pass added planted wrong versions (six for A1, five for B1, six for K6). `check_wrongs()` lists 6 "check by hand" lines; each `byKey` line names the slip's arithmetic (such as "1 + 8 + 4 + 1") rather than its value, and all were read and are right.
- `fresh-check --exam mock-superday-developer --min-run 10`: 0 hits. The first draft had 5: a `larger` template identical to `topic-1.9` (rewritten as `clamp_to` with new calls) and the longform opening line shared with the strats mock (reworded).
- Playthrough with `--local-cdn <pkgs>`: ok, 21 items (parts counted), scored 17 of 17, passed; mock checks ok. With `--mobile`: ok, the same. The first draft's window test (50,000 ticks, 5,000 kept) ran past 5 s in the browser because libc++ debug hardening checks the whole tree at every `std::map::erase`. The fix pass keeps 1,000 ticks in that window and restores the large insert-and-query test to 200,000 ticks, which the reference passes in the browser; a sorted vector takes 8.2 s there and fails.
- `readiness-sums`: OK after the status row above.
- Screenshots (1280 and 390 px, `<scratchpad>/exam-superday/shd/`): the start card, the Python round, the C++ `parts` round, the padding `parts` item, a choice with a code block, the pool item, the queue-sizing `parts` item, the design longform and the results page. Nothing overlaps; long starter lines scroll inside the editor at 390 px, as in other C++ items. The results page at 390 px is wider than the window, the engine matter raised for the strats mock.

## Every number and its source

| Item | Key | Route A | Route B |
| --- | --- | --- | --- |
| A1 | 14 test values (50, 50, -1, -1, 2, 20, 8, 23, 15, 7, 7,229, -1, 5,990, 9,000) | sort by departure, keep the earliest time per site, in CPython | label-setting search with bisection over each site's runs; six planted wrong versions |
| B1 | 14 test values | reference compiled by g++ | a Python model on sorted lists with `bisect`; the large total is $\sum_{t < 200000}(100 + t \bmod 97) = 29{,}599{,}419$; five planted wrong versions |
| K1 | 24, 16 | the layout by hand | g++ `sizeof`; minimum over the 24 member orders |
| K2 | 1 copy | by hand | g++ `-O0`, `-O1`, `-fno-elide-constructors`, clang++ |
| K3 | a double delete | by hand | a counting `operator delete[]` |
| K4 | `base tree tree base` | by hand | g++ output |
| K5 | `clamp_to(101.5, 0, 100)` fails | by hand | `g++ -fsyntax-only` on each option |
| K6 | 13 test values, ending 12,499,900,000 | reference compiled by g++ with a counting `operator new` | a Python model of the pool with generations; six planted wrong versions |
| Y1 | 2,000,000 with `std::atomic<int>` | by hand | native threads, three runs |
| Y3 | `std::scoped_lock` | by hand | native threads, 400,000 opposite transfers |
| Y4 | 8 | 8 doubles to a 64-byte line | an LRU simulation: 65,536 against 8,192 misses |
| Y5 | 6, 32 | $150{,}000 \times 40 \times 10^{-6}$; next power of two above 24 | a replay of arrivals in nanoseconds; `bit_length` |
| G1 | one order every 5 µs | $1/200{,}000$ s | $200{,}000 \times 5\,\mu s = 1$ in flight |

The last pass of the check matches every number in every learner-visible string of each item to a route-B or given value; code in fences and spans is checked by compiling it instead.

## Prerequisites cited (gated by `requires`)

graphs-dp L2 (`l7-dijkstra`), coding-int L4 (`l13-requirements-change`, `l16-edge-cases-first`, `l18-talking-while-coding`), cpp L5 (`l13-templates`, `l15-maps`, `l19` to `l23`), systems L4 (`l2-caches`, `l4-object-layout`, `l7` to `l10`, `l11-processes`, `l15` to `l18`), recruiting L3 for the fit paper.

## Proposals

- No `prep.json` change. A developer firm path (Hudson River Trading, Two Sigma quant developer) does not exist yet; when one is added it could name this mock.

## Changes in the fix pass

See `docs/reviews/review-exam-mock-superday-developer.md`, `## Fix pass`. A1 is now `earliest_arrival` over timed runs (the first draft repeated `graphs-dp/homework-2`), K6 asks for generation handles (the first draft repeated the `systems/l15` pool), `round-two` has `pass: 1`, `models` no longer lists concurrency, and K6's pace is cut to 1,080 s so the C++ paper keeps 160 s of slack.
