# numerics level 1 (Errors): report

Author: content agent, 5 Nov 2026. Brief: `docs/briefs/numerics.md` section "Level 1".

## Files

| File | Screens or items | Canvases and widgets of note |
|---|---|---|
| `l1-floating-point.json` | 10 screens, quiz 4 | console hook (52 halvings), toy-format number-line with a drag-point, 4 by 16 bit grid (tap the exponent, decode −6.5 and 100.25), spacing staircase, limits table trap, code `decode` + `machine_epsilon` |
| `l2-cancellation.json` | 10 screens, quiz 4 | root table hook, live plane of the textbook root's error against b (slider on k, derive in browser doubles), expm1 and one-pass variance ladders, forward-difference V (tap the best h, slider on the model), delta trap, `derive` expression for h*, code `stable_small_root` + `welford_var` + `best_bump`, gamma transfer |
| `l3-conditioning.json` | 10 screens, quiz 4 | two nearly parallel lines with a slider on b2 and a derived meeting point, amplification table (28,285), kappa of four functions, matrix kappa 40,002, digits lost, residual trap, `order` derivation of the bound with a distractor, code `cond2` + `digits_lost` + `predicted_error`, implied-vol transfer |
| `l4-stability.json` | 10 screens, quiz 4 | e^-20 series console, plane of term sizes with a slider on m, backward stability, Läuchli matrix (det 0, 16.3 digits), `order` SVD derivation with two distractors, Trefethen lecture 19 table, algorithm-for-problem trap, code `lstsq_normal` + `lstsq_qr`, yield-curve transfer |
| `review-1.json` | 10 items, difficulty 2 to 4 | interleaves all four lessons; skills `nm-float` (5) and `nm-stability` (5) |
| `homework-1.json` | 9 items, difficulty 3 to 5 | two 5s: code `stable_stats` + `kahan_total` (8 tests, float32 pennies), longform book variance (10-point rubric, full model); derivations: expression (kappa of e^x − 1) and `order` (forward error ≤ kappa × backward error) |

No performance task: the lesson objectives start with Read, Spot, Compute and Compare, so the verb rule does not match (AUTHORING sections 5 and 11), and the validator agrees.

## Gates (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors overall; no warning on any numerics level 1 file.
2. `VOICE_BASE=app/content/courses/numerics/ python3 docs/reviews/voice-scan.py`: 0 sentences over 20 words, 0 explanations over three sentences.
3. `python3 docs/reports/numerics-L1-numbers.py`: exits 0 (about 190 checks, plus every code widget's solution passing and starter failing its hidden tests in CPython). Needs numpy, scipy and mpmath.
4. Playthrough with `--local-cdn <scratchpad>/pkgs`: all six files pass without flags, with `--mobile`, and with `--mobile --tablet` (lessons 14 checks each and quiz 4/4; review 10 of 10; homework 9 of 9, 41 of 41 marks, longform marked by the button). Screenshots at 1280 and 440 were read; two layout faults were fixed (see Backlog).

## Numbers and their sources

Every number was computed in CPython (NumPy 2.5.3) and recomputed by a second route in the numbers script: mpmath at 50 digits for exp, roots, Black-Scholes and the series; exact `Fraction` arithmetic for 0.1 and the variances; `math.frexp` against `struct` decoding; eigenvalues against the SVD; float32 loops in NumPy scalars.

- l1: 52 halvings, eps 2^-52 = 2.220446e-16; −6.5 = sign 1, field 1025, power 2, fraction 0.625, `0xa000000000000`; 100.25 = field 1029, power 6, fraction 0.56640625; 0.1 stored as 0.1000000000000000055511151231257827, error 5.55e-18 (relative 5.55e-17); spacing 1.42e-14 at 100, 1.16e-10 at 10^6; 2^53 = 9,007,199,254,740,992; max 1.797693e308, exp(709) = 8.218407e307, exp(710) raises or returns inf; tiny 2.225074e-308, subnormal 2^-1074 ≈ 5e-324; u = 1.11e-16; eps/tiny ≈ 10^292; float32 eps 1.19e-7, gap 0.001953125 at 20,000, 20,000.01 stored as 20,000.009765625; timestamps 1.7e18 ns between 2^60 and 2^61, gap 256 ns.
- l2: textbook root 7.450581e-9 against 1.0e-8 (25.5%); log10 relative error −14.4 at b = 10, −6.5 at 10^5, −0.6 at 10^8 (two digits per decade); expm1 relative error 8.27e-8; one-pass variance 0.0 (offset 10^9), 29.33 (10^8), two-pass and Welford 30.0, population 22.5; forward errors 0.1406 (h = 0.1), 6.6e-9 (10^-8, the lowest), 0.39 (10^-15); central 4.5e-9 (10^-4), 5.9e-11 (10^-5); h* = 2√eps = 2.98e-8, eps^(1/3) ≈ 6e-6; standard call £10.4506, delta 0.636831, gamma 0.0187620, vega 37.52; forward delta errors 9.3e-3 (£1, estimate 0.6461), 9.4e-5 (£0.01), 4.4e-3 (10^-12, estimate 0.6324); central 8.6e-5 (£1), 8.6e-9 (£0.01); best forward delta bump ≈ 7e-7; gamma estimates 0.01875972, 0.01876202 (error 2.7e-10), 0.01876188 (1.4e-7), 0.02842171 (51% too big); £1 gamma error 2.3e-6; log(1 + 1e-12) = 1.000089e-12.
- l3: sigma 2.00005 and 4.999875e-5, kappa 40,002; meeting points (1, 1) and (0, 2); relative input change 3.536e-5, amplification 28,285; digits lost 4.6; Hilbert 8 kappa 1.53e10, 10.2 digits; kappa 1/2, 20, 10,001, 10,000.5; residual of (0, 2) is (0, −0.0001) (the brief wrote +0.0001: b − Ax is negative); vol moves 0.027 (call, vega 37.52) and 1.70 vol points (60 put, price £0.0113, vega 0.588), ratio 64; £0.05 gives 0.133 and 8.5; correlation kappa 39 at r = 0.95, VIF 10.26, 199 at 0.99; bound 4.0002e-4.
- l4: series 6.147561828914626e-9 against 2.061153622438558e-9 (198.3%); largest term 4.31e7, 16.3 powers of ten above the answer; 1/sum(e^20) = 2.061153622438557e-9; Läuchli: stored det 0, exact 2e-16, kappa 1.41e8, 8.15 and 16.3 digits; at eps = 10^-7 the normal equations return (1, 1), kappa^2 u ≈ 0.02, 1 + 10^-14 is 45 gaps above 1; Trefethen: kappa 2.27e10, kappa u ≈ 2.5e-6, kappa^2 ≈ 5e20; yield curve on maturities 1, 2, 3, 5, 7, 10, 15, 20, 30 years: kappa 2.98e4, kappa(AᵀA) 8.88e8 (8.95 digits), centred and scaled 13.3. The brief did not name the maturities; these nine are the set that reproduces all three stated figures.
- Pyodide differs from CPython (NumPy 2.0.2 against 2.5.3) in Trefethen's fit, as the brief expected. Pyodide, run with the local CDN in node: lstsq and QR 0.9999999654 (relative error 3.5e-8), normal equations −0.2654. CPython: 0.9999999847 (1.5e-8) and −0.1623. The lesson states Pyodide's figures (0.99999997, −0.27) and names −0.16 as the desktop figure; the code test asks QR for an error under 1e-6, which both meet.
- Review and homework: 0.01 has field 1016, power −7; √(x+1) − √x ≈ 5e-7 at 10^12; float32 gap £0.0625 at 10^6; h* = 2.98e-7 for |f| = 100; e^-30 = 9.4e-14, largest term 7.8e11, 25 powers of ten; spread kappa 10,001; `0x4024000000000000` = 10; float32 integers exact to 2^24 = 16,777,216; kappa 3e5 leaves 5.0 digits by the normal equations, 10.5 by QR; gamma bump (48 eps)^(1/4) = 3.21e-4; a million float32 pennies: naive £9,865.22, Kahan £10,000.00.

Tolerances in code tests: exact equality for decodings and eps; relative 1e-12 for roots; absolute 1e-9 for variances and central derivatives; relative 1e-6 for condition numbers; absolute 1e-9 (QR) and 1e-6 (normal, eps = 1e-7) on the Läuchli solves; absolute £0.005 on the float32 pennies, which take about 2 s in Pyodide (`caseBudget` 20,000 ms).

## Choices that differ from the brief

- The spacing pictures (l1 screens 6 and 10) use a plane in log10 coordinates, not `number-line` or plane log scales: the log-scale plane printed overlapping full-digit tick labels and "0" for small ticks (Backlog).
- Homework longform: the brief's book moves by "a few thousand pounds a day", which gives a one-pass error near 2e-5 relative, never negative. The scenario is a hedged £1bn book that moves by a few pounds a day; a seeded simulation of 200 years (seed 7, sd £3) gave 0 in 100 and values from −263 to 263 otherwise, against about 9 by two passes.
- The homework code item imports NumPy in the starter, because the float32 tests need it and packages load only from the learner's imports.

## Proposed course.json change

None.

## Seeds and conventions

Simulation seed 7 (Python `random`), numbers script only. Standard call S = K = 100, r = 5%, sigma = 20%, T = 1 throughout. £ for money. Generators and helpers are in the scratchpad folder `numerics-L1` (not committed).
