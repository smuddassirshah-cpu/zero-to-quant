# opt-dash level 2 (Pricers): report

## Files written (app/content/courses/opt-dash/)

| File | Screens / items | Quiz | Code screens | Notes |
|---|---|---|---|---|
| `l5-bs-pricer.json` | 10 screens (hook, explore, name, 4 ladders incl. trap, generalise, transfer) | 4 | 3 (`bs_price`, `bs_price_vec`, pytest `test_parity`/`test_limits`) | plane value curve with `Phi`, controls on σ, T, q |
| `l6-tree-pricer.json` | 10 screens | 4 | 2 (`crr_price`, `exercise_boundary`) | graph four-step tree, series convergence and boundary |
| `l7-mc-pricer.json` | 10 screens | 4 | 2 (`mc_price`, `mc_control_variate`) | table, series funnel, bars coverage, distribution |
| `l8-three-pricers.json` | 10 screens | 3 | 2 (`compare_grid`, `flag_differences`) | table grid, grouped bars with an expiry control |
| `review-2.json` | 8 items, difficulty 2 to 4, two per lesson | | | |
| `homework-2.json` | 7 items, difficulty 3 to 5 (two at 5) | | 2 (`richardson_tree` d5, `mc_greek_delta` d4) | 2 `order` items, 1 `longform` (10-point rubric, model answer) |

All skills `od-pricers`. Generators (Python, one per file) and the reference solutions live in `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/opt-dash-2/` (`common.py`, `sol2.py`, `gen_l5.py` to `gen_l8.py`, `gen_sets.py`).

## Validator

`node app/tools/validate.mjs`: 0 errors overall. My files carry two warnings, both on l6 (screens 3 and 4: a ladder changes canvas kind, table → array → table), kept on purpose: the code screen shows the NumPy slices on an `array`, the timing screen a table.

## Playthrough (`--local-cdn .../scratchpad/pkgs`)

- l5-bs-pricer: ok, 14 checks, quiz 4/4 (pytest screen passes: right pricer passes, three planted pricers fail)
- l6-tree-pricer: ok, 14 checks, quiz 4/4
- l7-mc-pricer: ok, 14 checks, quiz 4/4
- l8-three-pricers: ok, 13 checks, quiz 3/3
- review-2: ok, recorded 8 of 8
- homework-2: ok, marked 7 of 7, 34 of 34 marks

Screenshots (with `--why`) in `.../scratchpad/opt-dash-2/shots`, `shots6`, `shots7`, `shots8`, `shotsS`; checked by eye. One fix made from them: l6's `exercise_boundary` had a zero-rate test that failed in the browser because at $r = 0$ hold and exercise values tie to the last bit at deep nodes (floating noise decides); replaced by the last two steps of a 50-step tree.

## Function signatures (as in the brief's list, plus optional trailing keywords)

- `bs_price(S, K, r, sigma, T, kind="call", q=0.0)`: `ValueError` for another `kind`; $T \le 0$ returns intrinsic value; $\sigma \le 0$ returns $e^{-rT}\max(\pm(F-K),0)$.
- `bs_price_vec(S, K, r, sigma, T, kind="call", q=0.0)`: NumPy arrays, `scipy.special.ndtr`; assumes $T, \sigma > 0$.
- `crr_price(S, K, r, sigma, T, n, kind="call", american=False, q=0.0)`: NumPy backward induction; `ValueError` when $p \notin [0,1]$.
- `exercise_boundary(S, K, r, sigma, T, n, q=0.0)`: list of length $n+1$, highest exercised node price per step (strict `K - s > hold`), `nan` where none; at expiry the highest leaf below $K$.
- `mc_price(S, K, r, sigma, T, kind="call", n_paths=100_000, seed=0, antithetic=True, q=0.0)` → `(price, se)`. Convention: `n_paths` counts payoffs; antithetic draws `n_paths // 2` normals in one `rng.standard_normal` call and the error uses the pair averages; `ValueError` with fewer than two independent samples.
- `mc_control_variate(S, K, r, sigma, T, n_paths, seed, q=0.0)` → `(price, se)`, calls only, control $X = e^{-rT}S_T$ with $E[X] = Se^{-qT}$, $b$ from the same sample.
- `compare_grid(S, r, q, sigma, strikes, expiries, n_steps, n_paths, seed)`: **puts** (the brief's column `tree_am_put` implies puts); rows expiries outer, strikes inner; columns `K, T, bs, tree_eu, tree_am_put, mc, mc_se`; the same seed in every cell (common random numbers, stated).
- `flag_differences(grid, tree_tol=0.01, n_se=3.0)`: frame `K, T, check, diff, reason`; checks `mc` (beyond `n_se` errors), `tree_eu` (beyond `tree_tol`), `american` (below `-tree_tol` is `pricer-error`, above `tree_tol` is `american-premium`). Two keyword arguments added; the brief's one-argument call works.
- Homework: `bbs_price` and `richardson_tree(S, K, r, sigma, T, n, kind="call", american=False, q=0.0)` (Black-Scholes last step, then $2P_{2n} - P_n$); `mc_greek_delta(S, K, r, sigma, T, n_paths, seed, h, q=0.0)` (call, common random numbers).

Later levels can load these exactly from `common.py` (`BS_SRC`, `CRR_SRC`, `MC_SRC`) or the lesson files' `solution` fields.

## Seeds and data conventions

- No chain data are needed in this level; inputs are the course's: $S = 100$, $r = 5\%$, $q = 1\%$ (chain) or $q = 0$ (to match `trees`), $\sigma = 20\%$.
- Monte Carlo: `np.random.default_rng(seed)`, all normals in one call; seed 0 for lesson numbers, seed 1 for the l8 test grid, seed 7 and 3 for tolerance tests, seeds 0 to 199 (and 0 to 1999) for coverage.
- Tests compare seeded floats rounded to 6 places with ==; CPython (NumPy 2.5.3) and Pyodide 0.27.7 (NumPy 2.0.2, under node with `pyrun.mjs`, and in the browser playthrough) agreed at that precision everywhere.

## Numbers stated, with sources (all computed in CPython, then in Pyodide)

l5: call £10.450583572185565, put £5.573526022256971, `bs_call(110,100,0.03,0.25,0.5)` 14.466961084155471 (trees l10, reproduced); with $q = 1\%$ call £9.8263, put £5.9443, $C - P = 3.8820$; $d_1 = 0.30$, $d_2 = 0.10$; $\sigma \to 0$ limit £4.88 (4.877057549928611); swapped order `bs_price(100,100,1,0.2,0.05)` = 5.1658; percent rate `r=5` gives 99.3262; `bs_price_vec` grid values in the screen (CPython = Pyodide to 6 places); one-year call at σ 0.22 to 0.26: 11.2028, 11.5800, 11.9578, 12.3360, 12.7146; quiz: $C - P = 10.787$ for $S=100, K=90, r=4\%, q=2\%, T=0.5$.

l6: four-step tree of the six-month 95 put ($u = 1.092412$, $p = 0.506236$): only node £76.71 exercises (18.29 vs hold 17.82); 4-step American £4.1769, European £4.1207. 500 steps: European £3.9057, American £4.0053, BS £3.9043 (the brief's values confirmed). One-year call 500 steps £10.4466, 501 £10.4541, average £10.4503; 1 step £12.1623; tree prices for 1 to 200 steps in the series. $p$ with $q = 1\%$, four steps: 0.5252 (0.5378 with $r$). American call, $S = 130$, $K = 100$, $q = 5\%$: £30.39 vs European £29.50 (q = 1% gives no premium to 1e-13 on this grid). Bug "r in p instead of r − q", q = 1%: £10.4466 vs right £9.8224. $p = 3.061$ for σ = 1%, one step of a year. Timings (Pyodide under node, American put): pure Python 0.16 s / 2.42 s at 500 / 2,000 steps, NumPy 0.050 s / 0.158 s. Black-Scholes vol of the American £4.0053: 0.2540. Boundary from 500 steps (every 10th step) rises from £74.05 to £93.87.

l7: eight draws (seed 0) average payoff £12.18, discounted £11.59. 100,000 paths seed 0: plain 10.4362 ± 0.0465 ($s = 14.71$), antithetic 10.4721 ± 0.0329 (ratio 0.708; pair correlation −0.50), control variate 10.4484 ± 0.0178 (ratio 0.382; $b = 0.673$, correlation 0.924; plain paths to match: 686,000); put plain SE 0.0274, CV call and put SE both 0.017764 (parity). Coverage of 1.96-SE intervals, 2,000 antithetic paths: 190 of 200 runs (seeds 0 to 199), 1,893 of 2,000. Wrong antithetic SE over 100,000 payoffs 0.0466 vs right 0.0329; for a straddle 0.0419 vs right 0.0537 (pair correlation +0.64). Asian call, 12 monthly fixings, 100,000 paths seed 0: £6.1722 ± 0.0269; paths for SE 0.01 about 725,000. Running-estimate band at 2,500 / 10,000 paths ±£0.59 / ±£0.29.

l8 (puts, $S = 100$, $r = 5\%$, $q = 1\%$, σ = 20%, 500 steps, 100,000 antithetic paths, seed 0): tree − BS under 0.4p in all 15 cells; MC − BS within 1.27 SE everywhere; American premium from 0.03p (K = 80, 3 months) to £2.18 (K = 120, 1 year); K = 120, 3 months American £20.0000 exactly; one-year 100 put MC 5.9609 ± 0.0210 vs BS 5.9443 (0.79 SE); one-year 110 row MC +0.95p (0.5 SE), American +104.7p; three-month 80 put relative SE 4.1% vs 0.34% at the money. Timings (Pyodide): `bs_price` 3.7 µs, 500-step American tree 50 ms, `mc_price` 100,000 antithetic 18 ms, 15-cell grid 0.39 s.

Homework: plain CRR on the 95 put, 20 / 40 steps £3.9697 / £3.8889, naive Richardson £3.8081 (−9.6p); `richardson_tree` at 50 steps within 0.05p (European) and £4.0045 vs 5,000-step £4.0038 (American 95 put), ATM American put within 0.11p of £6.0902; `mc_greek_delta` 0.635973 (h = 1) and 0.636373 (h = 0.01) vs closed form 0.636831; separate seeds at h = 0.01 give −2.42. Longform: "exercise at the first in-the-money monthly date" Monte Carlo rule gives £3.20 ± £0.01 vs European £5.57 and tree American £6.09; 50-step call error −3.99p, 51 +3.4p, 100 −2.0p.

## Package load times (Pyodide 0.27.7 from the local CDN under node)

Base Pyodide about 2.8 s; plus NumPy about 1.5 s; NumPy and pandas import about 3.7 s more; SciPy (for `bs_price_vec`) adds about 2 s to download and 2 s to import. The `how` lines say so (NumPy 10 to 20 s, NumPy and SciPy 20 to 40 s, NumPy and pandas 10 to 30 s on a real connection, as level 1 measured).

## Departures from the brief, and proposed changes

- l6 hook uses a `graph` canvas for the recombining four-step tree (as trees l7 does) instead of `tree`, which draws non-recombining paths.
- l6 trap: the brief's second option, "r instead of r − q in p (the American call premium appears with q = 0)", does not happen: with q = 0 the bug changes nothing, and with q > 0 it hides the yield. The trap is "max only at the leaves"; the r-versus-r − q bug is a quiz item with its real effect (£10.4466 vs £9.8224).
- l5 explore and hook use a `plane` with the closed form in `Phi` (so the curve can carry q) rather than `payoff` with `value`, which has no dividend yield.
- Homework `richardson_tree`: plain-CRR Richardson makes the off-strike error worse (−9.6p), so the item uses the Broadie-Detemple smoothed tree (Black-Scholes last step) before extrapolating; homework item h-naive-rich shows why.
- No `course.json` change proposed.
