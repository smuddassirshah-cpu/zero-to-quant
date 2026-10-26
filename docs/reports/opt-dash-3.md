# opt-dash level 3 (Implied volatility): report

## Files written (app/content/courses/opt-dash/)

| File | Screens / items | Quiz | Code screens | Canvases |
|---|---|---|---|---|
| `l9-iv-solver.json` | 11 screens (hook, explore, name, ladder, problem, ladder (edge), trap, generalise, 2 code, transfer) | 4 | `implied_vol`, `iv_frame` | plane (price against σ, live tangent and Newton step), table, number-line (bracket, no-arbitrage band), console |
| `l10-smile.json` | 11 screens (hook, explore, name with sliders fit, 2 ladders, trap, generalise, 3 code, transfer) | 4 | `smile`, `fit_smile`, `plot_smile` | scatter, plane (planted smile with a T control; quadratic fit by sliders), table |
| `l11-term-structure.json` | 10 screens (hook, explore, derive (order), problem, 2 ladders incl. edge, trap, 2 code, transfer) | 4 | `atm_term_structure`, `forward_vol` | plane (ATM vols; total variance with two draggable dots and a chord), series, table, console |
| `l12-surface.json` | 10 screens (hook, explore, name, ladder, trap, generalise, 3 code, transfer) | 4 | `iv_surface`, `interp_iv`, `plot_surface_slices` | plane `heat` + `contour` map (tap, then drag a probe), table, plane (total variance trap), console |
| `review-3.json` | 9 items, difficulty 2 to 4 (three l9, two each l10 to l12) | | | number-line, table |
| `homework-3.json` | 7 items, difficulty 3 to 5 (one at 5) | | `iv_newton_steps` (d4), `svi_fit` (d5, SciPy `least_squares`) | 1 `order` (forward-vol derivation from returns), 1 `longform` (10-point rubric, model answer), 3 numeric |

Skills: l9 `od-iv`; l10 `od-iv`, `od-surface`; l11 and l12 `od-surface`. Builders (one Python script per file, `b9.py` to `b12.py`, `br3.py`, `bh3.py`), the shared preludes (`common.py`), reference solutions and number checks (`lib.py`, `c9*.py` to `c12*.py`, `svi.py`) and a test runner that executes every code widget's tests on its solution (`mkcheck.py`, run in CPython and in Pyodide with `pyrun.mjs`) are in `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/opt-dash-3/`.

## Validator

`node app/tools/validate.mjs`: 0 errors and 0 warnings in my six files. (Errors seen mid-session in `fin-ml/l4-overlapping-labels.json` belonged to another agent and were gone by the end; while they stood the manifest was not rewritten.)

## Playthrough (`--local-cdn .../scratchpad/pkgs`)

- l9-iv-solver: ok, 15 checks, quiz 4/4
- l10-smile: ok, 15 checks, quiz 4/4
- l11-term-structure: ok, 14 checks, quiz 4/4
- l12-surface: ok, 14 checks, quiz 4/4
- review-3: ok, recorded 9 of 9
- homework-3: ok, marked 7 of 7, 33 of 33 marks

Screenshots in `.../scratchpad/opt-dash-3/shots`, checked by eye. Fixes made from them: Newton table's KaTeX powers clipped at the column edge (now Unicode superscripts); l10 caption "1 months" (now "Expiry 1/12 years"); l10 trap curve label on the axis; l11 forward-vol chart gave the answer away and joined dashed partial lines (now months 1 to 6 only, a "?" marker at month 12); l12 point A sat on the 0.3 contour label (moved to £76, 0.18 years). One failure found and fixed: l12's code screens failed in the browser with `ModuleNotFoundError: pandas` (see backlog: imports written `import numpy as np, pandas as pd` load only numpy).

## Function signatures (the brief's list; earlier levels loaded in preludes)

Preludes carry the brief's generator verbatim (plus one extra `import pandas as pd` line, hidden) and the Level 1 functions `mid`, `clean_quotes`, `implied_forward`, `otm_quotes`; I checked them against the written l2 and l4 solutions (same code). `bs_price` in preludes is the generator's; `bs_vega(S, K, r, sigma, T, q=0.0)` is added as an "already loaded" helper.

- `implied_vol(price, S, K, r, T, kind="call", q=0.0)`: bounds `max(Se^{-qT} - Ke^{-rT}, 0) < price < Se^{-qT}` for calls, `max(Ke^{-rT} - Se^{-qT}, 0) < price < Ke^{-rT}` for puts, else `ValueError` (a price at intrinsic value raises: stated on the screen). Bracket `[1e-4, 5]`, start 0.2, Newton step, bisect when the step leaves the bracket, stop when |gap| < 1e-12, at most 50 price calls (a hidden counter on `bs_price` tests it).
- `iv_frame(clean, S, r, q_of_T)`: copy of `clean` plus `iv` (mid's vol, NaN on `ValueError`).
- `smile(clean, T, S, r, q)`: OTM quotes relative to $F = Se^{(r-q)T}$ (from the inputs, not the implied forward), columns `strike`, `m`, `iv`.
- `fit_smile(m, iv, weights=None)`: weighted least squares of `iv = a + b m + c m^2`, weights multiply squared residuals, NaN rows dropped, `ValueError` below three points, tuple rounded to 4 places.
- `plot_smile(smile_df, coeffs)`: `Axes`, line 0 the dots (marker `o`, no line), line 1 the fit over 50 points from min to max $m$; title "Implied volatility smile", x label "m".
- `atm_term_structure(clean, S, r, q)`: Series named `atm_iv`, indexed by float expiry, linear interpolation of the smile at $m = 0$ (`np.interp`, so flat beyond the last quote).
- `forward_vol(s1, T1, s2, T2)`: `ValueError` when $T_2 \le T_1$ or when total variance falls; 0.0 when equal.
- `iv_surface(clean, S, r, q)`: dict float expiry → `fit_smile` tuple.
- `interp_iv(surface, K, T, F_of_T)` → `(iv, outside)`. **Interpretation of the brief:** "linear in $T$ at fixed $m$" is implemented at fixed log-moneyness $k = \ln(K/F(T))$, each node read at $m = k/\sqrt{T_i}$, because the brief's justification (keeps calendar spreads arbitrage-free when the nodes are) holds at fixed $k$ (Gatheral's condition), not at fixed standardised $m$. Outside the nodes: the nearest node's vol at the same $k$ (flat), flag `True`; at a node the flag is `False`.
- `plot_surface_slices(surface, strikes, S=100.0, r=0.05, q=0.01)`: one line per expiry, labels `T = 0.08` etc. Three keyword arguments added (the brief's two-argument call works with the course's inputs) because a slice against strike needs each expiry's forward.
- Homework: `iv_newton_steps(price, S, K, r, T, kind="call", q=0.0, sigma0=0.2, tol=1e-12, max_steps=50)` (plain Newton iterates; gap tested before each step; `ValueError` when vega is exactly 0); `svi_w(k, a, b, rho, m, s)` and `svi_fit(k, w)` (start `[0.5 min w, 0.1, -0.5, 0, 0.1]`, bounds `[-1, 0, -0.999, -1, 1e-4]` to `[1, 5, 0.999, 1, 2]`, `xtol = ftol = gtol = 1e-14`, `ValueError` below five points).

Level 4 note: its brief checks calendar arbitrage "over $m \in [-1, 1]$". On the planted `true_iv`, total variance at fixed standardised $m$ never falls across the five expiries (my check), but at fixed $k$ on a fine $T$ grid from one month it falls for $|k| > 0.42$ (strikes below about £66 or above £153 at one month, outside the quoted range). Worth one sentence in l15 if it checks at fixed $k$.

## Seeds and data conventions

`make_chain()` seed 2320 exactly as in the brief; `clean = clean_quotes(make_chain())` (102 rows); $S = 100$, $r = 5\%$, $q = 1\%$ from the brief (no implied forward is used in level 3; $F = Se^{(r-q)T}$). Hand chains are priced with `bs_price` with bid = ask (locked quotes, kept by cleaning). Synthetic SVI data: $(a, b, \rho, m, s) = (0.02, 0.1, -0.4, 0.05, 0.15)$ on 21 points from −0.5 to 0.5. Tests compare floats rounded to 4 or 6 places with `isclose`. CPython (NumPy 2.5.3, pandas 3.0.5, SciPy 1.18.1) and Pyodide 0.27.7 (under node and in the browser) agreed on every tested value.

Package load (Pyodide under node, `pyrun.mjs`): numpy + pandas about 8 to 10 s; numpy + pandas + matplotlib + SciPy about 20 s. Each heavy screen's `how` says so; `svi_fit` has `budget: 20000`.

## Numbers stated, with sources (CPython, then Pyodide)

l9: £12.00 call vol 0.2411168936821648 (brief 0.2411168936821646, within 1e-15); bisection on [0.0001, 5] needs 43 halvings to a bracket below 1e-12 (47 to a price gap below 1e-12). Newton from 0.2: 0.2 → 0.2412913068 → 0.2411168955 → 0.2411168937; gaps −1.5494, 0.0066, 6.8e-8, 7e-15; errors 4.1e-2, 1.7e-4, 1.8e-9, 2e-16; vega 37.524 at 0.2. First step from σ0 = 0.05 lands at 0.3347 (price £5.28, vega 23.59); from 0.6 at 0.2352. Three-month 100 put mid £3.545 (3.44/3.65): vol 0.203227; parity call £4.5375 (no-q error £4.7872); call mid £4.505 vol 0.2016; the put mid solved as a call 0.1527. One-month 75 put at its ask £0.04: price at 0.2 £2.1e-7, vega 3.0e-5, plain Newton σ1 = 1323.1 then zero vega; safe solver 0.438368 in 10 price calls (first fallback 2.6). One-month 80 put at its ask £0.04: plain Newton 0.2, 8.736, −4.501, 2.113, 0.719, 0.497 (price £0.31 at 0.497); safe 0.351104 in 10 calls. One-year call with q = 1%: bounds £3.882 and £99.005. `iv_frame`: 8 NaN of 102 (deep in-the-money mids below the lower bound; one-month 70 call mid 30.205 vs bound 30.2077); row 44 0.2016, row 60 0.2348, row 101 0.2036. Transfer: 2000 × 20 × 43 × 2 µs = 3.44 s, Newton 0.64 s. Quiz: quick guess $\sqrt{2\pi}\,12/100 = 0.3008$; forward value $S - Ke^{-rT} = 4.877$.

l10 (three-month OTM smile, 9 quotes 80 to 120): vols 0.2622 … 0.1857 with $m$ −0.4663 … 0.3446; fit (0.2001, −0.0805, 0.109); with $a$ fixed, least squares b = −0.0805, c = 0.1089, RMS 0.086 vol points (2.73 flat). Fits by expiry: 1M (4 quotes) (0.1854, −0.0767, 0.0903), 2M (7) (0.1943, −0.0787, 0.0954), 3M (9) (0.2001, −0.0805, 0.1090), 6M (11) (0.2115, −0.0815, 0.1020), 1Y (11) (0.2185, −0.0799, 0.0978); planted $a(T)$ 0.1859, 0.1942, 0.2004, 0.2115, 0.2184. Planted IV(90) − IV(110): 0.0596, 0.0421, 0.0345, 0.0247, 0.0179 (ratio 3.33; √12 = 3.46). Planted IV(70), IV(100), IV(130): one month 0.4412, 0.1869, 0.1946; one year 0.2659, 0.2218, 0.2056. ITM vs OTM mid-vol error at three months: 1.42 vs 0.08 vol points. Bid-ask vol bands at three months: 80 put 1.38, 90 put 0.45 vol points. Risk reversal 90 put 0.2246 − 110 call 0.1896 = 3.50 points. Hand fits: weighted example (0.2005, −0.0437, 0.3452), three points (0.2, −0.1, 0.2222). Quiz: $m(110, 3M) = 0.1706$.

l11: ATM vols from the chain 0.1850, 0.1948, 0.2013, 0.2123, 0.2196 (planted 0.1859, 0.1942, 0.2004, 0.2115, 0.2184); forward vols 0.2043, 0.2137, 0.2227, 0.2267 (from the 4-place vols; 0.2266 unrounded; planted 0.2021, 0.2124, 0.2220, 0.2251). Planted ATM total variance 0.01004 (3M), 0.02237 (6M), 0.0477 (1Y). Crisis 45/35/28%: forward vols 0.2872 and 0.2524. 40% 1M / 26% 2M: w 0.01333 vs 0.01127. Trap 40% 1M / 20% 1Y: 0.1706 (vol-additive 0.1818). 40% 3M / 20% 1Y: 0. Earnings 24%/34% at 20/27 days: 6.55%. One-year at strike 100 0.2218 vs at the forward 104.08 0.2184.

l12: planted vols at the hook points A (76, 0.18) 0.2925, B (125, 0.12) 0.1791, C (75, 0.9) 0.2567, D (100, 0.5) 0.2138; 75 strike 0.3682 (1M) to 0.2553 (1Y). Interpolated $K = 100$, $T = 0.75$: $k = -0.0300$, node m −0.0424 and −0.0300, vols 0.2151 and 0.2210, w 0.02314 and 0.04883, w(0.75) 0.035989, vol 0.21905 (planted 0.2192; vol-linear 0.21805). Fit − planted errors (vol points) at one month −1.97 at £70 … −0.02 at £105 … −0.54 at £130; at one year within 0.03. Crisis trap 60%/30%: linear vols give 46.4% at six months, w 0.1075 > 0.09; linear w gives 33.8%. Surface grid (80 to 120 by expiry) in the screen; `interp_iv(surface, 100, 1.5, F)` 0.22365 flagged; `interp_iv(surface, 70, 1/12)` 0.4215. Planted two-node surface: K = 100, T = 0.75 0.216369; K = 90 0.228191; K = 110, T = 0.25 0.191804 (flag); K = 100, T = 2 0.22704 (flag). Quizzes: weekly node 20.0% / 19.9% gives 0.1855; $m(100, 6M) = -0.0283$; 20%/25% at 1M/3M gives 0.2385 at 2M.

Review and homework: Newton 0.25; bracket fallback 0.10005; $m(90, 6M) = -0.1773$; strike-skew ratio 2; forward vol 22%/24% = 0.2585; 2M 30% / 3M 24%: w 0.0150 vs 0.0144; interpolated 0.2129; SVI on the one-year smile $(a, b, \rho, m, s) = (0.0311, 0.0578, -0.999, -0.2018, 0.4454)$, max residual 6.1e-4 in total variance, ATM vol 0.2185; earnings 30%/45% at 7/14 days 6.57%; predicted one-year skew 0.0172 (planted 0.0179); crisis 50%/25%: 0.3371 (vol-linear 0.4545).

## Departures from the brief

- l10's hook uses the three-month smile, not the one-month: after cleaning, the one-month expiry has only four OTM quotes (90 to 105), too few to show the shape. The one-month thinness is used instead in l10's coefficient ladder and l12's extrapolation ladder.
- The planted smile's "slight rise on the right" is not visible in the cleaned quotes (its minimum is at $m = 0.4$, beyond most clean calls); the hook describes it as "falling, then flattening".
- `interp_iv` holds $k = \ln(K/F)$ fixed, not standardised $m$ (reason above).
- Weighting by the bid-ask vol band is taught (l10 generalise) and supported by `fit_smile(weights=...)`, but the level fits with unit weights, as the brief's l4 line says level 3 uses mids.
- No `course.json` change proposed.
