# Fix rule 581: wrong values that could never fire

Values recomputed in Python. Residual hits: 3 (stat-models, other agent). WRONG_FIRE_LEVEL left at 'warning'.

- limits/l1 s0 (b): question now asks a whole number; tol 0.001 to 0.0005, so 1.999 (diff 0.001) falls outside.
- integrals/l2 s4 (a): 5 dp stated; R100 = 101*201/60000 = 0.33835; tol 1.5e-5 to 5e-6; half-term 0.33833 tol 2e-6.
- vectors/l12 s1 (c): removed "printed" (5.000000000000001 vs 5) and its byKey line.
- graphs-dp/l9 s8 (c): removed "sum" (-264.0 vs -264.03, no precision stated); it had no byKey line.
- graphs-dp/hw-4 i6 (b): "Give 4 decimal places"; r=4 0.39869, r=5 0.39825; tol 5e-5, r5 tol 2e-5.
- analysis/l8 s0 (b): whole number asked; tol 0.01 to 0.001; 1.9957 now outside.
- validation/review-2 i6 (a): 4 dp; sqrt(0.002475) = 0.04975; tol 5e-5; "half" 0.05 tol 1e-4.
- arma/l1 q0 (a): ln 0.98 = -0.020203; tol 5e-5; simple -0.02 tol 2e-5; accept text updated.
- coint/review-1 i0 (a): 0.3*sqrt(248/0.91) = 4.9525; n=250 gives 4.9725; tol 0.005; accept text updated.
- backtest/l11 s1 (a): 1 dp; 0.5658/0.16438 = 3.442; tol 0.15 to 0.05; gross 3.33 tol 0.04.
- numerics/l4 s3 (c, question change): answer asked in units of 1e-16; exact det (1+1e-16)^2 - 1 = 2e-16, so slip is 2, tol 0.01.

Graded answers changed: none for correct keys; tighter tolerances only.
