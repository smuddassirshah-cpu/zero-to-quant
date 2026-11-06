# topology level 3 (Compact and complete): report

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l9-open-covers.json` | 11 screens | 3 |
| `l10-compact-images.json` | 12 screens | 3 |
| `l11-complete-spaces.json` | 12 screens | 3 |
| `l12-contraction-mapping.json` | 12 screens | 3 |
| `l13-fixed-point-iteration.json` | 12 screens | 3 |
| `review-3.json` | 9 items (difficulty 2 to 4, `pass` 0.8, all five lessons, one recalling level 2's homeomorphisms) | |
| `homework-3.json` | 8 items, one with 4 parts (difficulty 3 to 5, three at 5) | |

The exit line is carried by l12 (the proof in two `order` screens), l13 (using it) and homework-3: the whole proof as a nine-line `order` item at difficulty 4 (two distractors, the `same` pair of uniqueness and the bound), then the exit `longform` `h3-contraction-proof` at difficulty 5, the level's performance task (`derivation`, rubric 2, 2, 2, 2, 2 as the brief suggests).

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; level 3 warnings are only "a problem screen without a canvas before the ladder ends" on proof-only ladders.
2. Voice scan of the whole course folder: 0 sentences over 20 words, 0 explanations over three sentences.
3. `python3 docs/reports/topology-L3-numbers.py`: exits 0, 242 of 242 checks. It caught five wrong figures while being written, all fixed in the content: $125q^{245} \approx 0.0101$ (not 0.0104), $\ln(0.00008)/\ln q \approx 245.2$ (not 245.3), the 7% growth table ($V_{10} \approx 49.2$, $V_{100} \approx 779$), the cosine bound table ($2.9$ and $1.04 \times 10^{-6}$ at $n = 80$ and 86), and the wrong value $\tfrac{1}{32} = 0.03125$. "Check by hand" byKey lines were read and are right.
4. Playthrough with `--local-cdn`: all seven files pass at desktop, with `--mobile` and with `--tablet`; homework-3's parts checks pass too.

## Counts in Pyodide and CPython

Every iteration count in a hidden test (21, 87, 246; 39 and 15; 96 and 48; 39, 87, 15, 17, 246, 246) passed in Pyodide through the playthrough and in CPython through the number script, so no count differed. Margins at the boundaries: the cosine a posteriori bound is $1.07 \times 10^{-6}$ at step 38 and $7.2 \times 10^{-7}$ at 39; the Gordon bound is 0.01009 at 245 and 0.00971 at 246 (tolerance 0.01). No tolerance had to move.

## Proof steps and their widgets

- l9: $[0, 1]$ compact by covers: `order` with the "one member per point" distractor; closed in compact: `order`; compact is closed: `order` with a circular distractor; Heine-Borel: `order` with a `same` pair; the Lebesgue number: `numeric`.
- l10: images of compact sets: `order` with the "images $f(U_\alpha)$ are open" distractor; extreme value theorem: `order`; uniform continuity: `choice` for the Lebesgue step, `expression` $\varepsilon^2$, quiz `numeric` 0.01; compact onto Hausdorff: `order`.
- l11: closed and complete: `order` with a distractor; $C[0, 1]$ in the sup metric: `order`.
- l12: Cauchy step: `order` with the bounded and harmonic distractors; limit, fixed, unique, bound: `order` with a `same` pair; the bound `expression` $\tfrac{q^n}{1-q}d$ (it graded cleanly in the browser; the playthrough types only the authored form); the a priori count: `numeric`.
- l13: the method: `order` with a `same` group of the three hypotheses and a "the picture shrank" distractor.

## Cobwebs

l13's cobweb is a `let` chain of 8 steps of $\cos$ from a control on $x_0$, writing 9 `hidden` points and 16 segments (8 vertical, 8 horizontal); the chain runs on to $x_{40}$ for the caption only, so a learner can read 0.739085 to the screen's tolerance from any start. Screenshots were read at $x_0 = 2.5$ and $x_0 = -3$ (the range end); $x_0 = 3$ follows the same path after one step. l12's matrix iterates use the same pattern: an 8-step chain, 9 points and 8 segments.

## Numbers and sources

All are recomputed in `docs/reports/topology-L3-numbers.py`.

- $I_1, I_2, I_3$: every subset of the six intervals tried on a dense grid, and the greedy cover; the review's cover of 3 likewise.
- Lebesgue number 0.05 by sliding windows and by the overlaps; ball radius 0.025; 41 grid points and the worst gap $\tfrac14\%$ exactly, so £5,000.
- $\tfrac1e \approx 0.3679$ by a dense grid and by $f' = 0$; $f(3) \approx 0.1494$.
- Minimum volatility $w_1 = \tfrac{4}{38} \approx 0.1053$ (exact and by grid search), 9.787%; $-0.0769$ at correlation 0.6 with the long-only minimum at $w_1 = 0$; 0.2 at correlation 0.
- Ramps: 0.0625, 0.05, 0.025 by formula and by a midpoint sum; sup gap 0.5 on a grid.
- Arctan metric: 0.089669; $N$ = 10, 100, 1000 and 20 by search and by $\lfloor\cot\varepsilon\rfloor + 1$; the finite list gives 96 (against 100) and the ramp list 48, each by two routes.
- $0.5x + 1$: iterates, gap 1.25, count 21 by loop and by the log formula; matrix constants 1.2, 0.9, 0.8762 (closed form and power iteration), fixed point $(\tfrac{65}{14}, \tfrac{10}{7})$ in fractions, iterates, 160 and 31.
- Gordon: £125 by formula and bisection, iterates £4.72, £9.26, £13.62, count 246 by the bound and by the true error; $q \approx 0.9623$ and 1.0094.
- Cosine: 0.739085 by bisection and iteration; the five iterates; $\sin 1 \approx 0.8415$, $\sin x^* \approx 0.6736$; counts 87, 39, 32.
- Newton: iterates, errors $2.1 \times 10^{-6}$ and $1.6 \times 10^{-12}$, count 20, $\max|N'| = \tfrac12$ on a grid.
- Picard: $P_3$ by exact integration in fractions and by the Taylor sum, 1.6458333, $e^{1/2} \approx 1.6487213$, error 0.0028879.
- Implied volatility: $M \approx 39.8942$, $T(0.1) \approx 0.200572$, $T(0.5) \approx 0.205690$, $q = 1 - e^{-1/32} \approx 0.0308$ (closed form, and checked as a maximum on a grid), 0.200867 by bisection, three steps within $10^{-8}$.
- $\tfrac{1}{1 + x}$: count 17, iterates, true count 14, a posteriori 15, $\tfrac{\sqrt5 - 1}{2} \approx 0.618034$.
- `fixed_point_report`, computed and reported: cosine (0.739085, 39, 87, $7.2 \times 10^{-7}$); $\tfrac{1}{1 + x}$ (0.618034, 15, 17, $5.1 \times 10^{-7}$); Gordon (124.990, 246, 246, 0.009712).

## Other notes

- `analysis` l10, l17, l19 and l24 exist (l24 has no subcover code screen, so l9's `smallest_subcover` is the course's first); `taylor` l3, `numerics` l5 and `odes` l12 and l14 exist and are cited by id (the Gordon price of £125 matches `odes` l14).
- Code screens: `smallest_subcover` (7 tests, `Fraction` ends), `tail_width`/`first_N` (6), `iterate`/`apriori_steps` (7), `solve_fixed_point`/`implied_vol_atm` (9) and homework `fixed_point_report` (7). Each runs in CPython in the number script (solution passes, starter fails) and in Pyodide in the playthrough.
- No `course.json` change proposed. Backlog: 3 bullets under "Raised later (topology level 3)".
