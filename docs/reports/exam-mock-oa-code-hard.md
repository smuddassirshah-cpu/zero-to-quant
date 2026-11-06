# mock-oa-code-hard: report

Brief: `docs/briefs/mocks.md`, section `## mock-oa-code-hard` (written for this mock, from the `oa-developer` path in `prep.json`, `interview-plan.md` (d) and `interview-gaps.md`; no web search). Build: `docs/briefs/mocks-scripts/mock-oa-code-hard_build.py`. Second route: `docs/briefs/mocks-scripts/mock-oa-code-hard_check.py` (CPython 3.13, NumPy 2.5.3, g++ for the C++). Both run with `python3 -I`.

## Files
- `app/content/exams/mock-oa-code-hard.json` (one file, three fixed items; nothing drawn from the pack `oa`, so no item is shared with `mock-oa-code`).
- `docs/briefs/mocks.md` (section appended), the two scripts, this report, `docs/BACKLOG-INBOX.md`.
- `docs/readiness.md`: the developer row for `mock-oa-code-hard` changed from "gap: not yet written" to "exists"; `readiness-sums.mjs --write` then moved it from `missing` to `present` in `app/content/readiness.json` (4 lines). Nothing else changed.

## Items
One paper, 90 minutes, `pass: 0.6` (2 of 3), scoring 1, 0, 0, free navigation; checks `read-all` and `no-lookup`.

| Item | Diff | Language | Family | Pace | Tests |
| --- | --- | --- | --- | --- | --- |
| H1 `busiest_worker(k, jobs)`: two heaps, interval rule | 4 | Python | `job-scheduling` | 1,500 s | 12 |
| H2 `cheapest_with_voucher(n, links)`: Dijkstra on (site, voucher) | 4 | Python | `voucher-route` | 1,800 s | 12 |
| H3 `best_cash(prices, cap)`: DP over shares held | 5 | C++ | `inventory-dp` | 1,800 s | 13 |

Pace sums to 5,100 s of 5,400 s.

## Numbers (every expected value computed twice; all agree)
- H1: heap reference against a scan of every worker (build) and a NumPy scan (check) on all 12 cases and both examples. Keys `[1, 10]`, `[0, 0]`, `[0, 7]`, `[0, 6]`, `[0, 9]`, `[0, 7]`, `[0, 9]`, `[0, 21]`, `[1, 150]`, `[182, 308657]`, `[1845, 466369]`, `[0, 200000]` (the last also by closed form: job $i$ runs from $2i$ to $2i + 2$).
- H2: state Dijkstra against Bellman-Ford with each link freed in turn (build, small cases) and against $\min(d_0[n-1], \min_{(u,v)} d_0[u] + d_n[v])$ from two plain Dijkstras (check, every case). Keys 0, 0, −1, −1, 20, 0, 2, 0, 2, 99,990 (closed form $19{,}998 \times 5$), 1,213, 72.
- H3: a Python port of the recurrence (build), the C++ compiled with g++ (check), a $3^n$ brute force on the 10 small cases and a NumPy DP on the 3 large. Keys 7, 0, 0, 4, 3, 0, 0, 18, 13, 16, 99,999,900,000 (closed form $10^5 \times 999{,}999$), 49,503,711,056, 49,667,371,055. The last three pass $2^{31} - 1$ and stay under $2^{53}$.
- Starters fail 11 of 12, 10 of 12 and at least one of 13. Planted wrong versions each fail at least one test: H1 strict `<` (3), end from arrival (4), waits for the lowest number (2), unsorted input (1); H2 plain route minus its dearest link (5), voucher on every link (3), links both ways (3); H3 `int` total (3), no cap (2), sum of rises (5), cap of 1 (5).
- Slowest Python test 121 ms in CPython; all 15 C++ cases run in 0.04 s natively.
- Every number in every learner-visible string is a stated input, a test count or an answer. `check_wrongs()` then `report()`: 120 of 120 checks passed, exit 0.

## Gates
- Validator: 0 errors, no warning on this file (a first draft had a `pace` over 1,800 s and three sentences of 20 words or more; all fixed).
- Voice scan on a copy: 0 explanations over three sentences, 0 sentences over 20 words (84 scanned).
- `fresh-check --exam mock-oa-code-hard --min-run 10`: 0 hits. A literal search finds no function name or setup elsewhere; `graphs-dp` homework 2 `cheapest_within` (a step limit) and `topic-1.8` (a fee, two trades) set other states.
- Playthrough with `--local-cdn`: green (3 of 3, passed; clang compiled H3 in the browser; mock checks ok), and green with `--mobile`.
- Screenshots (1280 and 440): start card, each code item, results. The C++ signature is broken over two lines so it fits the phone editor.
- `readiness-sums.mjs`: OK after the `readiness.md` row above.

## Proposals
- `prep.json`: none.

## Backlog
2 bullets under `Raised later (mock mock-oa-code-hard):` in `docs/BACKLOG-INBOX.md`.
