# Review top-up: 13 interview-course reviews to 10 items

Decision (user, 9 November): a test-out draws 5 review items, so a 10-item review gives two papers with no repeated item. One new item was appended to each review below; no existing item was edited or reordered.

| Review | New item | Skill (lesson) | Kind | Why that skill |
|---|---|---|---|---|
| recruiting review-1 | `r10-dev-plan` | rk-landscape (l1 three roles) | choice | l1 had one item (r1); every other lesson had two. Tests reading a posting's tasks into the tests to prepare. |
| recruiting review-2 | `r2-one-take` | rk-assess, rk-behave (l10 recorded video) | choice | l10 had one item (r2-first-line). Tests the one-take format and the close. |
| recruiting review-3 | `r3-refuse-check` | rk-behave, rk-assess (l12 reasoning aloud) | choice | l12 had one item (r3-missing-move). Tests choosing the check that catches a wrong value (the refusal check, not the range check). |
| brainteasers review-1 | `r10-jugs-7-11` | bz-search (l5 ropes and jugs) | numeric | l5 had one item (hourglasses) and no jug item. Fewest steps to 8 litres with jugs of 7 and 11: 6. |
| research-int review-1 | `r1-det-rank-one` | rq-linalg (l5 matrices) | numeric | l5 had one item (equicorrelation). $\det(I + uu^\top)$ for $u = (2, 1, 2, 4)$: 26. |
| puzzles review-1 | `r1-five-of-eight` | pz-expectation (l2 every coupon) | numeric | l1, l2 and l4 had one item each; l2's only item was a full collection. Partial collection, 5 of 8: 7.0762. |
| puzzles review-4 | `r4-thh-price` | pz-games, pz-recursion (l20 betting on sequences) | numeric | l20 had one item (a chance, not a price). Fair price of a £16 ticket on THH before HHH: £14. |
| game-theory review-1 | `rv1-mixed-value` | gm-mixed (l4 mixing) | numeric | l4 had one item, asking for a mix. Ana's value at the mixed equilibrium: £2.20. |
| game-theory review-2 | `rv2-half-rounds` | gm-sequential, gm-normal (l7 guess two thirds) | numeric | l7 had one item (level-k), none on iterated deletion. Rounds until the bound for half the average falls below 1: 7. |
| systems review-1 | `r1-branch-budget` | sy-memory, sy-latency (l5 branches) | numeric | l4 and l5 had one item each; l5's was a counter trace, not the cost. Mispredicts as a share of a 5 µs budget: 10%. |
| systems review-2 | `r2-queue-fills` | sy-concurrency (l10 producer and consumer) | numeric | l10 had one item (lost wakeup). Time until a 600-item bounded queue blocks the producer: 12 ms. |
| systems review-3 | `r3-offset` | sy-os, sy-latency (l14 messages on the wire) | numeric | l11, l12 and l14 had two each; l14's two were both byte values, none on the fixed layout. Packed offset of the price: 13. |
| systems review-4 | `r4-burst` | sy-latency, sy-os (l18 feed handler) | numeric | Coverage was even (two per lesson); l18's objective (design and defend a handler) had no capacity item. Backlog after a 2 ms burst: 200. |

## Checks

- Numbers: `docs/reports/review-topup-numbers.py` recomputes every key by two methods (for example BFS and iterative deepening for the jugs, a first-step chain and Conway's leading numbers for THH, `numpy.linalg.det` and the determinant lemma), checks each key against the file, each numeric distractor against its slip and against the key, and each choice distractor for a `why`. Exit 0.
- Validator (from `app/`): 0 errors. The new items raise no warning (three long-sentence warnings and two explain-answer warnings on drafts were fixed).
- Voice scan (`voice-scan.py 35`, `VOICE_BASE` per course) on recruiting, brainteasers, research-int, puzzles, game-theory and systems: 0 and 0.
- Freshness (`fresh-check.mjs --file`, also at `--min-run 8 --min-share 0` for triage): the only hits on a new item are the game-theory stock sentence "Ana chooses the row and Ben the column; each cell is ...", shared with every payoff-table item in the course (the table and the question differ; homework-1 item 4 asks Ben's mix in another game), and "and nothing otherwise ... fair price" against random-vars review-2 (a die ticket, a different problem). Both are stock phrasing. Other hits in these files are on existing items and were not touched.
- Playthrough `--set` with `--local-cdn`, desktop and `--mobile`: 12 of 13 green. `research-int/review-1` plays all 10 items and records 10 of 10, but its `(timed)` and `(timed parts)` checks throw a 20 s `waitForFunction` timeout. The same failure occurs with the file restored to HEAD, and it is already in `docs/BACKLOG-INBOX.md` (line about 1468), so it is not caused by this change.

## Pass fields and clocks

- Every review has `pass: 0.8`, a share, so 8 of 10 is the new pass line. Left unchanged; the validator does not object.
- `research-int/review-1` has `timed: { seconds: 540, lockAtZero: true }`, exactly the sum of the nine paces. The new item has `pace: 45`, so paces now sum to 585 against a 540 s locking clock. Left unchanged (the task allows no edit beyond the new item, and the course brief names 540); raising it to 585 is a one-line decision for the main session.
- `puzzles/review-4` has `timed: { seconds: 1260 }` without a lock; paces now sum to 1200, inside it.
