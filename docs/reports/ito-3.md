# Report: ito (Brownian Motion and Itô, topic 3.2), level 3 "Pricing"

Branch: the agent worktree `agent-a68abf0c241f76c73`. Scratch folder: the scratchpad's `ito-3` (generators `gen_l9.py` to `gen_l12.py`, `gen_sets3.py`, the shared `lib.py`, number scripts `nums*.py`, `check2.py`, `checkcode.mjs`, `dbg.mjs`).

## Files written

All in `app/content/courses/ito/`. Ids, names, objectives and skills are those of `course.json` (`it-pricing` on l9, l11 and l12; `it-martingale` and `it-pricing` on l10).

| File | Screens / items | Quiz | Code widgets |
|---|---|---|---|
| `l9-bs-pde.json` | 9 screens (hook slider, four-term table, 7-line `order`, trap, edge, code, generalise, two transfers) | 4 | 1: `greeks` and `pde_residual` (10 tests) |
| `l10-changing-measure.json` | 9 screens (hook slider, theta, `order`, `expression` density, weights table, generalise, trap, code, transfer) | 4 | 1: `market_price_of_risk`, `weight_mean`, `girsanov_price` (10 tests) |
| `l11-prices-as-expectations.json` | 10 screens | 4 | 2: `mc_call` (7 tests); `crr_price` and `mc_digital` (8 tests) |
| `l12-barrier-option.json` | 11 screens | 4 | 3: `touch_prob_mc` (6); `down_and_out_mc` (7); `down_and_out_formula` and `bgk_barrier` (8) |
| `review-3.json` | 10 items, difficulty 2 to 4 (l9 2, l10 2, l11 3, l12 3) | | |
| `homework-3.json` | 7 items, difficulty 4 and 5 (three at 5) | | `barrier_report` (d5, `budget` 15000), `pde_check` (d4); `order` (replication route); 10-point `longform` with `pace: 300` |

Every lesson is 8 to 12 screens with no non-task screen. l9 names Shreve once (last screen) and opens, in its first prose, with the one sentence that topic 3.2 is optional (strats and desk quant interviews at banks, trading firms rarely).

## Brief corrections applied

- R5 (spoken derivation). The last screen of l9 is a `transfer` with a graded `order` of the five-minute plan (model and lemma, hedge, no-arbitrage step, equation, check, with one distractor), and its explanation sends the learner to the homework item "Derivation". The spoken answer is the `longform` item `h-derivation` in `homework-3.json` with `pace: 300`. No timer, no watch fallback. Nothing in the files says "E6" or "timed-set".
- R6 (two-letter subscripts). Every Itô-lemma and Black-Scholes line is an `order` line with `$V_{SS}$` in KaTeX. No `expression` screen contains `V_{SS}`. The one `expression` screen (l10, the density) is `e^{-\theta w-\frac{\theta^2T}{2}}`, keyed in the `e^{...}` form, with no `\exp` and no workaround. The four terms at S = 100 are four `numeric` cells in a `table` (rSΔ = 3.1842, ½σ²S²Γ = 3.7524, rV = 0.5225 and the sum 0, with Θ = −6.4140 given), bound to a `bars` canvas.
- Stale facts: scratchpad paths, the E6 timer sentence, "ito is not written", the `--local-cdn` folder: none of the stale text was carried into the files. Level 1 and 2 files were read for voice and numbers.
- R14 does not apply to this level (no `area`).

## Lesson size: what moved

- l9: the second `order` ("a riskless book earns r") is merged into line 6 of the 7-line derivation, its distractor and the trap screen (a hedged book earns r, not 0 and not μ). The trap "forgetting the ½σ²S² term" moved to quiz `q-vt`. The put's theta moved to quiz `q-put`. `greeks` and `pde_residual` share one code screen. The brief's plane with σ and T controls is replaced by a slider on Δ (the hook); the theta-gamma balance is on `bars`.
- l10: the edge case θ = 0 moved to quiz `q-edge`. `market_price_of_risk`, `weight_mean` and `girsanov_price` share one code screen. E_P[Z_T] = 1 is checked in the weights table (average of the two paths 0.9988) and in `weight_mean` (0.9999 on seed 14).
- l11: `crr_price` and `mc_digital` share one code screen. "Averaging undiscounted payoffs" is in quiz `q-disc` and `q-recipe` and in the trap's explanation, not a screen.
- l12: the BGK shift number is merged with the corrected-price screen (9). The trap "forgetting the barrier on paths that end above it" is quiz `q-path`. In-out parity is one table screen on the same 20,000 paths. `down_and_out_formula` and `bgk_barrier` share one code screen. The reflection check and its continuity correction are taught first on driftless Brownian motion (screens 1 to 3), then on the option.
- Review-3 holds a power-payoff item (`r-power`, S_T² priced at 10,941.74); l16 (level 4) covers general powers, so it is a preview of n = 2 only.

## Validator and playthrough

- `node tools/validate.mjs`: 0 errors; no warning in the level 3 files (the only ito warning is the existing "not yet written" line for level 4).
- Playthrough with `--local-cdn`, desktop and `--mobile` (390 px): l9 (13 checks, quiz 4/4), l10 (13, 4/4), l11 (14, 4/4), l12 (15, 4/4), `review-3` (recorded 10 of 10) and `homework-3` (marked 7 of 7 right, 36 of 36 marks): all passed, both ways.
- `checkcode.mjs` (Pyodide 0.27.7 under node, NumPy 2.0.2): every code widget's solution passes all its tests and examples, and every untouched starter fails (l9 10 of 10 starters fail, l10 10 of 10, l11 7 of 7 and 8 of 8, l12 6 of 6 and 7 of 7, l12 formula screen 7 of 8 because the dead-barrier test returns 0 in the starter, homework 5 of 5 and 7 of 7).
- Screenshots viewed (scratchpad `ito-3/sl`, `fin`, `ss`, `l12`). Faults found and fixed: a typo in the plane formula (d2 sign) that emptied the l9 hook curve; a caption overlapping the long x label on the l10 hook; a display formula too wide on a phone (l12); order lines clipped at 390 px by unbreakable inline maths (fixed by splitting long inline maths into `$` spans, see the inbox); the l12 edge screen showed a barrier at 90 for a barrier at 100 (now shows all 40 paths hit at time 0); a table byKey on cell wrong ids the validator refuses (removed).
- Voice: `VOICE_BASE=<worktree>/app/content/courses/ito python3 docs/reviews/voice-scan.py` reports 0 over-20-word sentences and 0 explanations over three sentences in the level 3 files (its remaining 2 long sentences are in earlier levels).

## Numbers stated, with sources (each computed by two routes)

Option: S = K = 100, r = 5%, σ = 20%, T = 1. Routes: (A) CPython NumPy 2.5.3 script, (B) Pyodide 0.27.7 (the code widgets' tests, expected from A and passing in B), (C) an independent method named below.

- Black-Scholes: d₁ = 0.35, d₂ = 0.15, Φ = 0.636831, 0.559618 (A; quadrature of the normal density, 0.636831 and 0.559618 and Φ(1) = 0.841345); call £10.4506 (A; quadrature of the Q-expectation 10.450584, and with P-draws reweighted by Z_T 10.450584).
- l9: Δ = 0.636831, Γ = φ(d₁)/(Sσ√T) = 0.018762, Θ = −6.4140 (analytic, and by finite differences of the formula: Γ 0.018762017, Θ −6.41402755, Δ 0.63683064); rSΔ = 3.1842, ½σ²S²Γ = 3.7524 (= 10φ(0.35)), rV = 0.5225, sum 2×10⁻¹⁶. The hedged book Π = −V + SΔ = £53.2325; −Θ − ½σ²S²Γ = 2.6616 = rΠ (two routes); 12% of Π = 6.3879. The residual of `pde_residual(100, 100, 0.05, 0.2, 1)` at h = 0.01, dt = 10⁻⁴ is **−1.0154 × 10⁻⁷** in CPython and −1.01539 × 10⁻⁷ in Pyodide; at (110, 100, 3%, 25%, 0.5) −2.15 × 10⁻⁸; at (50, 48, 4%, 30%, 0.25) −7.16 × 10⁻⁷; at the coarse step h = 1, dt = 0.01: −9.3876 × 10⁻⁴ and −6.3414 × 10⁻⁴. Forward V = 4.8771, V_t = −4.7561, rV = 0.2439, residual 0 at any σ. Put: V = 5.5735, Δ = −0.3632, Θ = −1.6579 (equation, and by parity Θ_c + rKe^{−rT}). Market maker: Γ-term 37.524, Θ −25.452, interest +10.562, net 22.634 per 1,000 calls at a £2 move; break-even move σS/√252 = 1.2599 (gamma 14.890 = 25.452 − 10.562). Quiz: −3.25, 318.4, −1.6579.
- l10: θ = 0.35 (also 0.2 for 8%, 3%, 25%); Z₁ = 0.6628 at W = 1, 1.3348 at W = −1, average 0.9988 (= e^{−θ²/2}cosh θ); E_P[S₁] = 112.7497, E_Q[S₁] = 105.1271, P(S₁ > 100) = Φ(0.5) = 0.691462; weighted P-draws on seed 14: 10.4692 (standard error 0.0305), mean weight 0.999933 (A, B); P-quadrature with weights 10.450584 and E[Z] = 1.0000000000 (C); without the weights 15.526 exactly (quadrature) against the simulated 15.534 (se 0.056) and 15.540 on seed 14; `girsanov_price` with μ = r on seed 11 equals the plain Monte Carlo price 10.4534 (0.0465). Discounted-mean hook: e^{−0.05}·100e^{m} = 100 only at m = 5% (107.25 at 12%, 95.12 at 0). Quiz: 1, 0.2, 103.05, 1.8941.
- l11: seed 11, 100,000 draws: 10.4534 (se 0.0465), antithetic 10.4590 (0.0232), 1,000 draws 10.7168 (0.4661), 10,000 draws 10.6368 (0.1478); scaling 0.4661/√10 = 0.1474 (A, B); four-draw hand table 84.37, 93.24, 113.88, 125.86, payoffs 13.88 and 25.86, average 9.9357, discounted 9.4511 (hand, and code); CRR tree 12.1623 (1 step), 9.5405 (2), 10.4306 (100), 10.4466 (500); gaps −0.0200, −0.0040 (the 500-step gap is 5.0 times smaller than the 100-step gap), +0.0028, +0.0084; wrong drift: exact 15.5261 (closed form with d = 0.7 and 0.5) and simulated 15.5343 (0.0562); undiscounted 10.99; digital e^{−0.05}Φ(0.15) = 0.5323 (formula; quadrature 0.53233; simulation 0.5320 with se 0.0015); S_T² claim 10,941.74 (10⁴e^{0.09}; quadrature of E_Q[S²] = 11,502.74 times e^{−0.05}). Desk paths (7.10/0.01)² = 504,100.
- l12: reflection 2(1 − Φ(1)) = 0.3173 (A; and 5,000-step simulation 0.3186 with se 0.0033); 5,000 paths of 1,000 steps on seed 13: 0.3102 (shape (paths, steps); 0.3072 with the other shape per the brief check), 100 steps 0.2852, 10 steps 0.2496; BGK shifted level 1 + 0.5826/√1000 = 1.0184 and 2(1 − Φ) = 0.3085. Down-and-out: λ = 1.75, y = −0.7036, (B/S)^{2λ} = 0.6916, c_di = 1.7851, c_do = 8.6655 (A, and a Brownian-bridge simulation of the continuous contract, 400,000 paths of 50 steps: 8.6566 with se 0.0229, 0.4 se away); daily 20,000 paths seed 12: 8.8510 (0.1034), weekly 9.0885, monthly 9.5712; vanilla on the same paths 10.4128 (0.1039), knock-in by parity 1.5617; shift 0.5826σ√(1/252) = 0.00734, B* = 89.3418, c_do(B*) = 8.9139 (c_di(B*) = 1.5367). **Caveat found while checking:** a daily simulation with 400,000 paths gives 8.8632 (se 0.0231), so the shifted formula is about five pence (2.2 standard errors) above the true daily price. The lessons say so (l12 screen 9 and the transfer explanation) and give the true gap to the continuous price as about £200 per 1,000 notes against £248 by the shifted formula. Quiz: 78.40, 0.0455, 7.30.
- review-3: −16.38, 0.9449, 1.1972, 52.04, 225,000, 10,941.74, 0.4117, 90.33, 0.1243 (Φ(1.5368) = 0.93783 by A).
- homework-3: `barrier_report` seeds 12, 3, 7: [8.6655, 8.8510, 0.1034, 8.9139, −0.6081, 0], [.., 8.8282, 0.1029, .., −0.8336, 0], [.., 8.8483, 0.1024, .., −0.6406, 0]; ratio Φ(0.15)/Φ(0.5) = 0.8093; antithetic worth (0.0465/0.0232)² × 100,000 = 400,000; corrected touch 0.2202 at level 1.2261.

## Proposals

- `course.json`: none for the map. The course card line to add (proposed in every level's report until the main session adds it): "Needed for strats and desk quant interviews (banks), rarely for trading firms".
- Prerequisites beyond `course.json` `requires` (level 3 has none and takes `ito/L2`): none needed. The lessons use trees l10 and l12 (the formula, delta hedging, vega), options l12 (gamma, theta), markov l11 (reflection) and ito l8 (the exponential martingale); all are in the closure of `ito/L1` and `ito/L2`.
- Level 4: l17's spoken derivation should follow the same pattern as `h-derivation` (a graded `order` of the plan on the last lesson screen, a `longform` with `pace: 300` in `homework-4.json`). Level 4's power payoff (l16) builds on `r-power` of review-3 for n = 2.

## Seed and shape conventions

NumPy `default_rng(seed)`, `standard_normal` with shape `(paths, steps)` (row per path) everywhere; Q-draws use `S_T = S₀exp((r − σ²/2)T + σ√T z)`; the Girsanov draws use `W_T = √T z`. Series pictures on l10 and l11 are precomputed running means (40 log-spaced points) of the seed 14 and seed 11 draws.
