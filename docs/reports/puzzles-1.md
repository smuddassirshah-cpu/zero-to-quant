# puzzles level 1 (Expected value): report

## Files written

All in `app/content/courses/puzzles/`. Ids, names, objectives and skills are the level 1 entries of `course.json` (each lesson's `objectives` is the course objective, unchanged). Skills: `pz-expectation` on every lesson, plus `pz-recursion` on l3 and l6 and `pz-symmetry` on l5; the sets also use `pz-recursion` and `pz-symmetry`.

| File | Screens / items | Interactive canvas early | Code |
|---|---|---|---|
| `l1-dice-games.json` | 9 screens (title, 3 problem, ladder, derive, trap, generalise, transfer), 4 quiz | 6 × 6 `grid` of the larger face, tap the cells where it is 6 | none |
| `l2-every-coupon.json` | 10 screens, 4 quiz | `graph` (markov) of faces seen; `table` widget filling the six stage waits; `bars` of the exact distribution of rolls | `coupon_expectation`, `coupon_sim` |
| `l3-waiting-for-hh.json` | 10 screens, 4 quiz | `graph` (markov) pattern states; `table` widget solving the HH and HHH first-step equations | `wait_time` (with `next_state` and `solve` in the prelude) |
| `l4-indicator-tricks.json` | 9 screens, 4 quiz | `grid` of 10 flips, tap the run starts; ring `graph` of pairs; `grid` of boxes; `bars` of record chances | none |
| `l5-hats.json` | 8 screens, 4 quiz | `boxes` of four people's hats, tap the matches; `table` of the 24 orderings | none |
| `l6-when-to-stop.json` | 10 screens, 4 quiz | hand-placed `graph` lattice of the 2-and-2 card game with backward values; `number-line` drag to the pig thresholds; `table` of the secretary orders | `card_game_value` |
| `review-1.json` | 9 items, difficulty 2 to 4, every lesson interleaved, all unseen puzzles | | |
| `homework-1.json` | 10 items, difficulty 3 to 5 (two at 5): 2 `code`, 1 `order`, 1 `longform` (10-point rubric, full model answer), 6 `numeric`/`choice` | | `pattern_wait` (5), `stopping_value` (4) |

Per lesson: worked puzzles of rising difficulty (canvas discovery, apply, twist), a trap on the blurted answer, generalise, an `order` derive with a distractor line, a quant transfer, and a quiz that is the brief's drill. Books (Mosteller, Zhou's green book, Crack, Joshi and co-authors, Jane Street's guide) are named once, in l1's title screen, with the families each is rich in, in general terms. l6 quotes Graphs and DP's £4.25 and £14/3 on its generalise screen.

Edge cases: l1 product of two dice (independence makes the product of means right); l2 one coupon type; l3 a one-flip pattern; l4 a variance needs pairs; l5 $n = 1$ and the impossible "exactly three of four"; l6 a game where going on always loses (stop at once).

Traps: l1 $3.5^2$ for the square of a die; l2 "about 6" or 36 rolls; l3 HH and HT take equally long; l4 refusing to add dependent indicators; l5 "with 1,000 people someone surely matches"; l6 stopping as soon as you are ahead (3 red, 1 black, first card red).

Builders and checkers are in `/tmp/claude-0/-home-user-zero-to-quant/9fb26fd5-8508-5986-8a3a-66bc5f67acde/scratchpad/puzzles-1/`: `common.py`, `build_l1.py` to `build_l6.py`, `build_sets.py`, `lint.py` (sentence length, punctuation, spelling), `codecheck.py` (solution passes and starter fails every hidden test, in CPython), `check_numbers.py` (output `numbers.out`) and `check_extra.py`. Every code `expect` in the homework is computed by a reference function in `build_sets.py` and cross-checked against Conway's overlap formula (patterns) or an iterated fixed point (reroll game).

## Validator

`node tools/validate.mjs` from `app/`: 0 errors, and no warnings for any puzzles level 1 file. The only puzzles warning is the course-level "not yet written" line for later levels.

## Playthrough

`node tools/playthrough.mjs --lesson puzzles/<id> ... --set puzzles/review-1 --set puzzles/homework-1 --local-cdn <scratchpad>/pkgs --shots <scratchpad>/puzzles-1/shots --mobile --why`: all passed.

- l1: 12 checks, quiz 4/4
- l2: 14 checks, quiz 4/4
- l3: 14 checks, quiz 4/4
- l4: 13 checks, quiz 4/4
- l5: 12 checks, quiz 4/4
- l6: 14 checks, quiz 4/4
- review-1: 9 of 9 recorded
- homework-1: 10 of 10 marked right, 47 of 47 marks

`codecheck.py`: every solution passes all its tests and every starter passes none (l2's same-seed test was tightened to `... == ... > 0` after the starter's `None == None` passed it).

Screenshots at 1280 and 390 px, with Why? sheets, were read screen by screen. Fixed from them: the l1 title screen does not draw a canvas (the books table became a list in the prose); the six-branch reroll tree's $\tfrac16$ labels collided (hidden, with a caption); the seven-node coupon chain overlapped at 390 px (zigzag layout, loops above and below); the l2 table screen's canvas gave the answers away (now the chance chain, with waits only in the Why? patch); the trap's caption gave the mean away; the HHH chain was cramped (hand positions); the HH equations overflowed at 390 px (stacked with `aligned`); the card-game lattice pills were shortened; the race item's correct option was the only short one.

## Numbers and their sources

Every number below was computed exactly (Fractions or exact enumeration) and again by a second method: simulation with `random.Random`, a closed form, or a different exact argument. Values to 4 places.

| Where | Number | Exact | Second method |
|---|---|---|---|
| l1 | one die | 7/2 | simulation 3.494 |
| l1, l1 transfer | larger of two dice | 161/36 = 4.4722 | $\sum k(2k-1)/36$; simulation 4.4718 |
| l1 quiz | smaller of two dice | 91/36 = 2.5278 | $7 - 161/36$ |
| l1 quiz | absolute difference | 35/18 = 1.9444 | simulation 1.9408 |
| l1 quiz | product | 49/4 | $3.5^2$ by independence |
| l1 trap | square of a die | 91/6 = 15.1667 | $3.5^2 + 35/12$ |
| l1 | £1 reroll game | 4 | best threshold policy; fixed-point iteration |
| l1 generalise, review | 50p reroll game | 9/2 | both methods; keep 5 and 6, tie at 4 |
| l1 quiz | sum of rolls to the first six | 21 | Wald $6 \times 3.5$; $5 \times 3 + 6$; simulation 20.96 |
| l2 | H and T | 3 | simulation 3.003 |
| l2 | three different faces | 37/10 | simulation 3.702 |
| l2 | every face | 147/10 | simulation 14.680; mode 11, $P(T = 6) = 5/324 \approx 1.5\%$ |
| l2 | last three faces | 11 | $14.7 - 3.7$ |
| l2 code | `coupon_sim(6, 20000, 1)` = 14.6871, `coupon_sim(4, 20000, 7)` = 8.3508 | 14.7, 25/3 | within 3 SE (0.13 and 0.08; sd 6.244 and 3.801) |
| l2 transfer | five weekdays | 137/12 = 11.4167 | simulation 11.42 |
| l2 quiz | four suits, ten toys | 25/3, 7381/252 = 29.2897 | simulation 8.326, 29.15 |
| l2 quiz | distinct faces in six rolls | 31031/7776 = 3.9906 | simulation 3.9903 |
| l3 | H, HT, HH, HHH, TT, HTH, HHT | 2, 4, 6, 14, 6, 10, 8 | Gauss-Jordan on first-step equations; Conway's formula; simulation |
| l3 | HH with $p = 2/3$ | 15/4 | $(1+p)/p^2$; simulation 3.746 |
| l3 transfer | two losses in a row, $p = 0.4$ | 35/4 = 8.75 | $(1+p)/p^2$; simulation 8.756 |
| l3 code | HTTH; TT at $p = 3/5$ | 18; 35/4 | Conway; simulation |
| l4 | runs in 10 flips | 11/2 | enumeration of all 1,024 sequences |
| l4 | shared-birthday pairs, 30 people | 87/73 = 1.1918 | 435/365; "at least one" 0.7063 as distractor |
| l4 | empty boxes | $10 \times 0.9^{10}$ = 3.4868 | simulation 3.4878 |
| l4 derive | aces before the first king | 4/5 | simulation 0.7945 |
| l4 transfer | records in 21 days | $H_{21}$ = 3.6454 | simulation 3.634 |
| l4 quiz | HH places in 10 flips, local maxima of 1 to 10, distinct faces of three dice, adjacent red pairs | 9/4, 11/3, 91/36, 25/2 | enumeration or simulation (2.25, 3.668, 2.5278, 12.49) |
| l5 | match counts for $n = 4$ | 9, 8, 6, 0, 1 of 24 | enumeration; inclusion and exclusion $24 - 24 + 12 - 4 + 1 = 9$ |
| l5 | $P(\text{no match})$, $n = 1$ to 8 | 0, 1/2, 1/3, 3/8, 11/30, 53/144, 103/280, 2119/5760 | $\sum (-1)^k/k!$; enumeration |
| l5 | mean and variance of matches | 1 and 1 | exact for $n = 2$ to 8 by enumeration |
| l5 quiz | five hats, no match | 44/120 = 0.3667 | simulation 0.3651 |
| l6 | card game values $V(1,1), V(2,1), V(1,2), V(2,2), V(3,3), V(3,1), V(2,3)$ | 1/2, 4/3, 0, 2/3, 17/20, 9/4, 1/5 | memoised recursion; simulation of the optimal rule (0.8527, 0.6674) |
| l6 trap | stop-when-ahead rule, 3 and 3 | 3/4 | enumeration of the 20 orders |
| l6 code | full deck $V(26, 26)$ | 41984711742427/15997372030584 = 2.6245 | memoised recursion; float 2.624476 |
| l6 | pig thresholds (1 wipes; 1 or 2 wipe; 6 wipes) | 20, 9, 15 | one-step gain against risk; exact DP over hold-at-$T$ policies (8.1418, 4.0926, 6.1537 maxima, ties at $T + 1$) |
| l6 | secretary, 3 and 4 candidates | 1/2, 11/24 | enumeration of all orders |
| l6 quiz | secretary, 100 candidates | about 1/e | exact 0.3710 for skipping 37; simulation 0.3701 |
| l6 transfer | take-profit threshold | £18,000 | $0.9 \times 2000 / 0.1$; day change 0 at £18,000 |
| review | largest of three dice | 119/24 = 4.9583 | tail sum; count by largest face |
| review | twelve months | 86021/2310 = 37.2385 | simulation 37.23 |
| review | 6 then 5 | 36 | first-step; Conway; simulation 36.02 |
| review | HH against HT race | 1/2 | simulation 0.502 |
| review | colour changes, 26 and 26 | 26 | simulation 25.96 |
| review | exactly one of six matches | 264/720 = 0.3667 | enumeration |
| review | secretary, 4 candidates | 11/24 = 0.4583 | enumeration |
| homework | `pattern_wait` expects (HTHT 20, HHTT 16, HTHTH 42, HHHHH 62, HTH at 1/3 is 33/2, HHT at 3/5 is 125/18, THTTHHTHTTHH 4160, twelve H at 9/10) | exact Fractions | Gauss-Jordan and Conway agree on all; simulation for the short ones |
| homework | `stopping_value` expects (4, 18/5, 9/2, 6, 7/2, 7, 8/3, 5, 5, 7) | exact | max over threshold policies; fixed-point iteration |
| homework | two sixes in a row | 42 | $(1+p)/p^2$; simulation 42.0 |
| homework | HHH or TTT | 7 | run-length chain; simulation 7.008 |
| homework | two toys at 0.8 and 0.2 | 21/4 | split on the first toy; $E[\max] = E[T_A] + E[T_B] - E[\min]$; simulation 5.246 |
| homework | loops in a random draw of 10 names | $H_{10}$ = 2.9290 | simulation 2.935 |
| homework | HT against TT race | 3/4 | simulation 0.752 |
| homework | birthday triples, 50 people | 784/5329 = 0.1471 | simulation 0.1488 (200,000 trials) |

Seeds: `random.Random(2026)` in `check_numbers.py`, `random.Random(11)` in `check_extra.py`; the l2 code tests use seeds 1, 7 and 3, whose solution values are given above (Pyodide 0.27.7's `random` is the same Mersenne Twister and `randrange` as CPython's).

## Proposed course.json changes

None. The map was taught as named. (`course.json` now lists a fifth level; that is the planning agent's, and this level does not touch it.)

## Backlog

Six bullets added to `docs/BACKLOG-INBOX.md` under `Raised later (puzzles level 1):`.
