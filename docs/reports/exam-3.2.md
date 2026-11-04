# Topic 3.2 exam: stochastic calculus

## Brief (written before the items)

The brief is `docs/briefs/exam-3.2.md`: topic 3.2 (optional, desk quant and derivatives pricing), courses `ito` (l1 to l17), `measure-prob` (l1 to l17) and `pdes` (l1 to l12); 30 items, 90 minutes, pass 0.7, 14 skills, ramp 6, 15, 6, 3, no `requires`. Its keys were computed twice by `check_ito.py`, `check_mp.py`, `check_pdes.py` and `check_fix.py` (re-run at the start: all assertions pass).

## Result

File: `app/content/exams/topic-3.2.json` (id `topic-3.2`, 90 minutes, pass 0.7, 30 items, 37 sittable questions with the 13 sub-asks of the six `parts` items, pace sum 4,875 s = 81.25 minutes).
Scripts in `docs/briefs/exam-3.2-scripts/`: `build.py` (with `build_ito.py`, `build_mp.py`, `build_pdes.py`, `helpers.py`) writes the file; `check_final.py` recomputes every stated number by a second route; `exprcheck.cjs` grades the three expression items through the app's real `exprEqual`; `codecheck.mjs` runs the code item in Pyodide 0.27.7; `fresh.py` is the freshness grep.

Ramp 6, 15, 6, 3 at difficulty 2, 3, 4, 5, in that order in the file, courses interleaved. Kinds: 15 numeric, 6 parts (13 sub-asks: 12 numeric and 1 choice), 3 expression, 3 multi, 1 table, 1 order, 1 code. By course: `ito` 11, `measure-prob` 11, `pdes` 8. Every `choice` and `multi` has `shuffle: true` and a `why` on every distractor, and no correct option is the longest. Every numeric lists two named wrong values with `byKey` lines.

### Coverage by level

`measure-prob` level 4 was confirmed from the written files: `mt-change` is on l14 to l17 and first met on l14 (l1 to l13 carry none), `mt-martingale` also on l16 and l17 (first met on l11). So level 4 counts as covered by M9, M10, M11. Result: **11 of 11 levels covered**.

| Course | Level | Skill first met | Items |
| --- | --- | --- | --- |
| ito | 1 Brownian motion | it-bm (l1), it-calculus (l3) | `e-var-two-times`, `e-gbm-below`, `e-qv-drift` |
| ito | 2 Itô calculus | it-martingale (l8) | `e-pick-martingales`; `e-drift-t2w2` tests l6 through the shared it-calculus |
| ito | 3 Pricing | it-pricing (l9) | `e-theta-from-pde`, `e-daily-touch` |
| ito | 4 Interview | none (shared) | `e-exit-drift` (l14), `e-sixth-repair` (l13), `e-moment-and-isometry` (l15), `e-cubed-claim` (l16) |
| measure-prob | 1 Measures | mt-sigma | `e-atoms-three-sets`, `e-sigma-families` |
| measure-prob | 2 Integration | mt-integral | `e-tail-integral`, `e-swap-limits` |
| measure-prob | 3 Information and martingales | mt-condexp (l9), mt-martingale (l11) | `e-var-of-condexp`, `e-variance-split`, `e-adapted-predictable`, `e-ruin-by-martingale` |
| measure-prob | 4 Changing measure | mt-change (l14) | `e-is-weight`, `e-die-reweight`, `e-tree-price` |
| pdes | 1 The heat equation | pe-heat | `e-kernel-peak`, `e-slab-heat` |
| pdes | 2 Separation and Fourier | pe-fourier | `e-coefficient-k`, `e-jump-gibbs`, `e-rod-centre` |
| pdes | 3 Pricing equations | pe-bs (l9), pe-fk (l11), pe-fd (l12) | `e-heat-change`, `e-fk-square`, `e-explicit-code` |

`ito` level 4 has no skill of its own and is covered only through shared skills, by four items each built on one of its lessons (as `coding-int` level 3 for exam 3.5). `ito` level 2 counts through `it-martingale`; `e-drift-t2w2` does not count for it.

Skill counts, asserted by `build.py`: it-bm 4, it-calculus 5, it-martingale 3, it-pricing 3, mt-sigma 2, mt-integral 2, mt-condexp 3, mt-martingale 3, mt-change 3, pe-heat 3, pe-fourier 3, pe-bs 1, pe-fk 1, pe-fd 1. All 14 are in the `skills` map and tested.

### Timing

Pace sum 4,875 s = 81.25 minutes of the 90, about 9 minutes for reading and review. Paces are the brief's. The playthrough clock run left 1:29:15 at question 30 (it answers at once).

### Revisions to the brief's item plan, and why

Read from the written files and the freshness greps (`fresh.py`, then by eye):

1. **File order** is by difficulty, courses interleaved; item numbers in the brief are plan numbers.
2. **I4** (`ito` l6, drift): the brief's $d(tW^2)$ is already asked in `ito` l13 (a drift at $t=2$, $W=3$, and "add $f_t$ and $\tfrac12 f_{xx}$ for $f=tx^2$"). New process $t^2W_t^2$, key `2tw^2+t^2`, slips `2tw^2` and `2tw^2+2t^2`. Id `e-drift-t2w2`.
3. **I5** (martingale picks): the brief's options $e^{3W-4.5t}$, $W^4-6tW^2+3t^2$ and $tW-\int W\,ds$ are in `ito` homework-2 and l13, and $e^{t/2}\cos W$ is in homework-2; review-4 has $e^{1.5W+ct}$. New six: A $e^{0.8W_t-0.32t}$ (yes), B $e^{0.8W_t-0.64t}$ (no), C $e^{-t/2}\cosh W_t$ (yes), D $W_t^2-2t+\int W\,dW$ (no, drift $-1$), E $W_t^3-3\int W\,ds$ (yes), F $W^4-6tW^2+6t^2$ (no, drift $6t$). Key A, C, E; the longest option (D) is wrong.
4. **M4** (limit swap): `U^n`, `nU^n`, a squared-index spike and `n 1{U<1/n^2}` are in l7, homework-2 and review-2. New five: A $U^{1/n}$ (yes, mean $n/(n+1)\to1$, limit 1), B $n^2\mathbf 1_{\{U<1/n^2\}}$ (no), C $\sqrt n\,U^n$ (yes), D $ne^{-nU}$ (no, mean $1-e^{-n}$, limit 0), E $\min(n,1/U)$ (yes, monotone). Key A, C, E.
5. **M6** (table): the fifth rule, $\mathbf 1_{\{S_n>0\}}$, is an option in `measure-prob` l11. Replaced by $S_{n-1}\xi_n$ (adapted, not predictable).
6. **M9**: the brief's $x=3.6$ equals homework-4's $\theta=3.6$. Moved to $\theta=2.5$, $x=3.2$: weight $e^{-4.875}=0.0076$ (0.007635; slips $e^{+4.875}=130.97$ and $e^{-8}=0.000335$). `tol` abs 0.0001; the upside-down slip has abs 0.5.
7. **M11**: after the level 4 fix pass, homework-4 has a tree with $u=1.25$, $d=0.75$ at 4%. New tree $S_0=60$, $u=1.24$, $d=0.84$, $1+r=1.05$, $p=0.6$, $K=60$: $q=0.525$; payoffs 32.256, 2.496, 0; price 9.193 (9.19314). Slips for $q$: 0.600 and 0.475; for the price: 11.619 (weights $p$) and 10.135 (no discounting). Replicating cost and backward induction agree to 1e-9.
8. **I7**: the second slip (forgot the factor 2) is 0.348 (shift applied, one tail) in place of the brief's 0.367 (no shift and one tail), since an author who applies the shift and forgets the 2 lands on 0.348. Key 0.6956, `tol` 0.004.
9. **I8**: the "no $\sigma^2$" slip is $c=2\mu$ (gives 0.4595), not $2\mu/\sigma$; text corrected.
10. **I6**: the gamma term is 4.2018 from the rounded inputs (the brief rounded it to 4.2019); $\Theta=-5.73$ unchanged.
11. **P8**: the brief's wide-bump case (T=1.7, 170 steps) does not trigger a float `ceil` error in IEEE arithmetic (170.0 exactly). The wide case is $D=0.08$, $\Delta x=0.04$, $T=1.12$, where $T/\Delta t_{\max}=112.00000000000001$ and an unguarded `ceil` takes 113 steps and fails. A further case ($D=0.2$, $\Delta x=0.1$, $T=0.3$, ratio 11.999999999999996) fails a floor. The starter (floor steps) passes 3 of 8 tests; the solution passes 8 of 8.
12. **M8**: the line texts were shortened so that no display-maths span runs past 440 px (see Backlog); same seven lines, `same` on lines 5 and 6, two distractors with `why`. No line text appears in `l10`, `review-3` or `homework-3`.
13. **I3 and I1** keep the brief's numbers. **I2** answer 0.34995 with `tol` 0.0005.

### Numbers computed twice

`check_final.py` asserts each key, each slip and each figure an `explain` or `feedback` quotes (36 checks). Route A is the closed form; route B is independent:

- I1: 7 (quadratic form; 2,000,000-draw simulation to 0.05); 19, 31. I3: 45 (200,000-step squared increments within 0.5); 65, 15.
- I2: 0.34995 (lognormal quadrature; 3,000,000 draws to 0.002); 0.2751, 0.2928; $z=-0.3855$, sd 0.4243.
- I4: SymPy $f_t+\tfrac12f_{xx}=2tx^2+t^2$; exact one-step mean change. I5: SymPy drifts of all six options; simulation of A, C (mean 1) and E (mean 0) at $T=2$.
- I6: $-5.7326$ (formula), $-5.7327$ (PDE balance), $-5.7326$ (central difference in $T$); $-9.93$, $-1.80$.
- I7: 0.6956 (BGK), 0.6953 (exact 126-step grid Markov chain), 0.6957 (200,000 paths); continuous 0.7343; 0.348.
- I8: 0.41317 and 2.5350 (formulae and a 200,001-point tridiagonal finite-difference solve to 1e-5 and 1e-4); 0.6667, 0.4595, 2.0, $-0.7605$.
- I9: SymPy solve $a=-15$, $b=45$, $c=-15$ and the drift factorisation; no-constant drift $45t^2$.
- I10: 30 (split $W_5$; 4,000,000 draws to 0.5); 11.1825 ($e^{2.5}-1$; quadrature, $E[e^{2W_t-t}]=e^t$ by quadrature and simulation).
- I11: 23.5574 ($8e^{1.08}$; quadrature to 1e-6, 4,000,000 draws); $-0.375$ (SymPy roots $-0.375$ and 1); 25.0141, 5.5814, 0.375, $-0.15$.
- M1: 64 (atoms; brute-force closure under complement and union); 8, 512. M2: brute-force closure test, F1 and F5. M3: 3 (formula, density quadrature, inverse-CDF simulation); 1, 4.
- M4: exact means at $n=2000$ by quadrature for A, C, D, E; limits checked at two $U$ values. M5: $\tfrac{25}{12}$ in exact `Fraction`, $\tfrac56+\tfrac{25}{12}=\tfrac{35}{12}$, 3,000,000-roll simulation to 0.01. M6: measurability against the atoms of the first $n-1$ and $n$ tosses on three tosses. M7: 0.189573 (formula and a six-state linear solve to 1e-12); 0.4, 0.6398.
- M9: $e^{-4.875}=0.007635$ (and the density ratio to 1e-15); M10: 8.6 (exact `Fraction`, both routes); 15.17, 6.25. M11: see revision 7.
- P1: 0.26596 (spectral solve on a 16,384-point grid to 1e-4); 0.3761, 0.4205. P2: 0.87866 (quadrature of the kernel); 0.9715, 0.9545. P3: SymPy integral and `quad` at $k=1$ to 7; 2.5465, 0, 0.0943. P4: 0.08949 ($\mathrm{Si}(\pi)/\pi-\tfrac12$), 7.5369 (4,000-harmonic partial sum to 0.005). P5: 2.93822 (modes) and the matrix exponential of a 599-point Laplacian to 1e-3; 1.697, 3.848. P6: SymPy substitution gives $\alpha=-0.46$, $\beta=-2.1316$. P7: 9.72652 (normal quadrature; PDE residual 0 at a test point; 4,000,000 draws to 0.05).
- P8: loop against the eigen-decomposition solution to 1e-12 on all five named grids (sine mix centre 0.52642 with 52 steps and $\lambda=0.49615$; spike centre 0.07647; 112, 1,200 and 12 step cases).

### Code item and starter

`codecheck.mjs` (Pyodide 0.27.7): `e-explicit-code` solution 8 of 8 (slowest 0.007 s), example 1 of 1, starter passes 3 of 8 (wide bump, zero start and 1,200 steps). The unguarded `ceil` fails 1 test and a floor fails 3 (`check_final.py`). The playthrough also ran the solution in the app.

### Freshness

`fresh.py` greps every item's keys and parameters (number boundaries) over `app/content` (courses, exams, bank, drills, data) and was re-run after merging the `measure-prob` level 4 fix pass (review-4 and homework-4 with $u=1.3$, $d=0.7$, $p=0.4$, $q=0.55$; $q=0.58$, $p=0.65$, $u=1.25$, $d=0.75$ at 4%; $\theta=0.4$). Real clashes became revisions 2 to 7. Remaining hits are decimals inside simulated series (`coint`, `arma`, `garch`, `markov`, `ensembles`), an unrelated context (`conditional` l14 0.2660; `puzzles` $\tfrac{125}{12}$), a shared fact (the plain-die $\tfrac{91}{6}$ in `mock-oa-sig`, here a named slip), `ito` l16's different cubed claim, and `measure-prob` l2's $\{3,4,5,6\}$ inside a different space. No firm names. M10's die $(0.35, 0.25, \dots)$ and the tree are not in l14 to l17, review-4 or homework-4.

## Validation and playthrough

- `node tools/validate.mjs`: 0 errors, no warning for `topic-3.2.json`; it adds one line to `content/manifest.json` (kept).
- Voice scan on `app/content/exams` (`VOICE_BASE=<worktree>/app/content/exams`): 0 sentences over 20 words and 0 explanations over three sentences for `topic-3.2.json` (the other exams' lines are not mine).
- `playthrough.mjs --exam topic-3.2 --local-cdn <pkgs>`: 37 questions, scored 30 of 30, passed. Again with `--mobile --tablet --why` (440, 1032, 1376 and 1280 px, with the results page and explanations): passed, no sideways scroll.
- Screenshots looked at (440 px: table, multi, order, code; results page). Fixes: the order lines of M8 were clipped at 440 px (shortened into short maths spans); two starter lines ran off the editor (shortened).
- `prep.json`: no topic exams listed there, not edited. `course.json`: no change proposed; the exam carries no `requires`.

## Backlog

One bullet under "Raised later (exam topic-3.2):" in `docs/BACKLOG-INBOX.md` (long display maths in an `order` line does not wrap).
