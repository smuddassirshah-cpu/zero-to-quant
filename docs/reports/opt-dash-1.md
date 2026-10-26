# opt-dash level 1 (Data): report

## Files written

All in `app/content/courses/opt-dash/`. Generators and helpers are in the scratchpad folder `opt-dash-1` (`kit.py`, `common.py`, `gen_l1.py` to `gen_l4.py`, `gen_sets.py`, `hwsol.py`, `chain.py`). Each generator computes its numbers from `make_chain()`. It also runs every code widget's solution and starter against its tests in CPython before writing.

| file | screens / items | quiz | code screens |
|---|---|---|---|
| `l1-reading-a-chain.json` | 11 screens (hook, explore, name, 3 ladders, trap, generalise, 2 code, transfer) | 4 | `mid(df)`, `chain_table(df, T, kind)` |
| `l2-cleaning-quotes.json` | 10 screens (hook, explore, name, 2 ladders, trap, generalise, 2 code, transfer) | 4 | `clean_quotes(df, max_age_min=30, max_rel_spread=0.5)`, `drop_report(df, max_age_min=30, max_rel_spread=0.5)` |
| `l3-rates-dividends.json` | 10 screens (hook, explore, name, 2 ladders, trap, derive, 2 code, transfer) | 4 | `implied_forward(df_T, r, T)`, `implied_q(F, S, r, T)` |
| `l4-which-price.json` | 11 screens (hook, explore, name, 2 ladders, edge-case problem, trap, generalise, 2 code, transfer) | 4 | `otm_quotes(df_T, F)`, `iv_from_quotes(df_T, S, r, T, q)` |
| `review-1.json` | 9 items, difficulty 2 to 4, all four lessons interleaved | | |
| `homework-1.json` | 8 items, difficulty 3 to 5 (two at 5) | | code `prepare_chain` (5) and `bounds_violations` (4); `order` pipeline item; longform with a 10-point rubric and model answer |

Skill `od-data` throughout; £ for money.

## Validator

`node app/tools/validate.mjs`: 0 errors overall, and no warnings for these six files. Other warnings belong to other courses and unwritten lessons.

## Playthrough

`node app/tools/playthrough.mjs --lesson ... --set ... --local-cdn <scratchpad>/pkgs`, final run after all edits:

- l1-reading-a-chain: ok, 15 checks, quiz 4/4
- l2-cleaning-quotes: ok, 14 checks, quiz 4/4
- l3-rates-dividends: ok, 14 checks, quiz 4/4
- l4-which-price: ok, 15 checks, quiz 4/4
- review-1: ok, 9 of 9
- homework-1: ok, 8 of 8, 37 of 37 marks

Screenshots, with Why? and wrong-answer sheets, are in scratchpad `opt-dash-1/shots` and `opt-dash-1/shots-sets`. I looked at all the canvas screens. The `Phi`-based price-against-vol curves draw correctly on plane. So do the derive caption on the dragged point, the scatter cut-line control, the parity sliders, and the payoff straddle with its breakevens.

Every code widget ran twice: in CPython (NumPy 2.5, pandas 3.0) in the generators, and in Pyodide 0.27.7 in the browser playthrough. Both passed every test with the authored solution. The untouched starters fail the tests (a few NaN-path tests pass by accident).

Package load: numpy plus pandas took about 19 s to load under node (`pyrun.mjs`), and the first run that imports pandas took about another 19 s. In the browser, the first lesson with code took 37 s against about 10 s for the later ones. Every `how` line that loads pandas says so.

## Numbers and their sources

All of these come from `make_chain()` (seed 2320, verbatim from the brief) with S = 100, r = 5%, q = 1%. They were computed in CPython and confirmed in Pyodide through the code tests.

- Brief checks reproduced: 130 rows; 15 zero bids (rows 62, 111 and 120 planted, the rest deep OTM one- and two-month quotes plus the 3m 130 call); 2 crossed (rows 23, 87); 2 stale (rows 108, 114); 2 planted wide (rows 4, 92); row 64 is 4.37 / 4.64. Cleaning keeps 102.
- `drop_report(chain)` in the order zero bid, crossed, stale, wide gives `{'zero_bid': 15, 'crossed': 2, 'stale': 2, 'wide': 9, 'kept': 102}`. With the wide rule first it drops 24, because every zero bid has relative spread 2. With `max_age_min=300` it keeps 104, and with `max_rel_spread=0.2` it keeps 95.
- Cleaned rows per expiry: 15, 20, 21, 24, 22.
- l1: 3m 100 call mid 4.505, spread 0.27. 3m straddle 4.505 + 3.545 = 8.05, so the implied σ ≈ 8.05 / 40 = 20.1%. The 1y straddle is 17.34, so σ ≈ 21.7%. 100-call mids: 1m 2.31, 3m 4.505, 1y 10.60.
- l2: the 6m 105 call's relative spread is 3.12 / 6.04 = 0.5166. The 3m 95 call's lower bound is 5.93, against a filled mid of 3.99. The hand row (3m 80 call, 18.90 / 19.40) has a lower bound of 20.74. Seven wing quotes have £0.05 spreads and relative spread ≥ 0.5; a £0.10 absolute floor would keep 109 rows. Transfer: the stale 1y 95 call set at S = 102 implies 26.69% against 22.65%, a gap of 4.03 points. With vega £34.57 per contract per point, 500 contracts mark at about £69,700.
- l3: the cleaned 1y C − P line has slope −0.9526 and intercept 99.19 (true −0.9512 and 99.005). It crosses zero at 104.12. Median forwards per expiry: 100.346, 100.650, 101.005, 102.004, 104.123 (true 100.334, 100.669, 101.005, 102.020, 104.081). Implied q per expiry: 0.85%, 1.11%, 1.00%, 1.03%, 0.96%. The 100 strike alone gives F = 104.058. Fitting both r and q from the line: at 1m r = 0.84% and q = −3.24%; at 1y r = 4.86% and q = 0.82%. The brief's "about 5.1% and 1.1%" used a different strike set; the lesson states my values. Dividend transfer: a £2 dividend at 6 months lowers the 1y forward by 2e^{0.025} = 2.0506.
- l4: row 64 implied vols are 19.47%, 20.16% and 20.84%, a band of 1.37 points. The 3m OTM quotes after cleaning are puts 80 to 100 and calls 105 to 120 (9 quotes). Their mid vols are 0.2622, 0.2392, 0.2246, 0.2117, 0.2032, 0.1939, 0.1896, 0.1858, 0.1857. The 3m 120 put's lower bound is 18.76: its bid and mid have no vol, and its ask vol is 22.91%. Trap: the 1m 85 put at 0.01 / 0.06 has a bid vol of 22.47% and an ask vol of 28.39%; their average is 25.43%, but the mid's vol is 26.23%. Bands: the 1m 90 put is 1.83 points (the widest shown) and the 3m 80 put 1.38. The weight ratio between the 3m 90 put and the 3m 80 put is 3.1. "21.5 / 22.5" on the 3m 100 call is £0.197 wide.
- Homework: `prepare_chain(chain, 100, 0.05)` returns 42 rows, with 4, 7, 9, 11 and 11 per expiry. `bounds_violations(chain, 100, 0.05, 0.01)` finds 8 rows, all deep in the money, with mids a few pence below the lower bound from noise. Stale-quote age: 257.4 minutes. A £0.01 error in F moves the 1m q by 0.12 points. A £1.50 dividend at 3 months lowers the 1y forward by 1.5573. The 3m 125 call's mid vol is 18.36%, against a 17.83% average.

## Conventions and decisions for later levels

- Generator: the brief's `make_chain()` verbatim, with two lines added above it: `import numpy as np` and `import pandas as pd`. The code widget's import scan reads the generator's own first line, `import numpy as np, pandas as pd`, as numpy only. Without the extra lines, a screen opened cold would fail with "No module named 'pandas'". Levels 2 to 4 should do the same.
- `mid(df)`: `(bid + ask) / 2` as a Series keeping the index, NaN where `bid <= 0`. A locked quote keeps its mid.
- `chain_table(df, T, kind)` matches T with `np.isclose`, indexes by strike in ascending order, and has columns `bid`, `ask`, `mid`, `spread`.
- `clean_quotes` uses the plain rules: bid > 0, bid ≤ ask, age ≤ max_age_min, (ask − bid)/mid < max_rel_spread. It returns a fresh index. The course chose no absolute spread floor, so the count stays 102 as the brief states; the floor is explained, with its count of 109, on l2's explore screen.
- `drop_report` (an extra helper, not in the dashboard list) returns a dict with keys `zero_bid`, `crossed`, `stale`, `wide`, `kept`, in that order.
- `implied_forward` pivots mids by strike and type, uses `reindex(columns=["call", "put"]).dropna()`, returns NaN under 3 pairs, and otherwise the median of K + e^{rT}(C − P) as a float. `implied_q(F, S, r, T) = r − ln(F/S)/T`. The dashboard fallback is F = S e^{(r − q)T} with a stated q (1%).
- `otm_quotes`: puts with K < F, calls with K ≥ F, sorted by strike, fresh index, same columns.
- `iv_from_quotes` returns one row per input quote, in input order, with columns `strike`, `type`, `iv_bid`, `iv_mid`, `iv_ask`. The mid comes from `mid()`. Its prelude solver is `implied_vol(price, S, K, r, T, kind="call", q=0.0)`: bisection on [1e-4, 5] for 100 steps, returning NaN outside (lower bound, upper bound). That is the l9 signature, so level 3 can swap in the learner's solver.
- Homework `prepare_chain(df, S, r, q_fallback=0.01)` adds an optional argument to the brief's `prepare_chain(df, S, r)`; the old call still works. Its output columns are `T`, `strike`, `type`, `mid`, `F`, `q`.
- Hand-made frames in tests: `quotes(rows)`, `toy_chain(S, r, q, sigma, T, strikes, half=0.05)` (bid and ask ± half around `bs_price`), and `vol_quotes(...)` (bid and ask priced at two known vols). All three are defined in the preludes.

## Proposed course.json change

None.
