# Report: complex level 1 (The complex plane)

## Files written

All in `app/content/courses/complex/`, generated from scripts kept in the scratchpad folder `complex-L1`.

| File | Screens or items | Code screens | Skills |
|---|---|---|---|
| `l1-square-root-of-minus-one.json` | 12 screens, 4 quiz | `cmul` and `cdiv` on pairs; `i_power` (cycle) and `quad_roots` (`cmath.sqrt`, starter uses `math.sqrt`) | cz-arith |
| `l2-points-in-a-plane.json` | 12 screens, 4 quiz | `to_polar` (starter has the `atan(b/a)` trap) and `from_polar`; `ar2_cycle` | cz-arith, cz-polar |
| `l3-euler.json` | 12 screens, 4 quiz | `exp_series`; `rotate` (degrees bug) and `power_polar` (angle not multiplied by n) | cz-polar |
| `l4-roots-of-unity.json` | 11 screens, 4 quiz | `nth_roots`; `dft` (hidden test against `np.fft.fft`); `dominant_period` | cz-polar |
| `review-1.json` | 10 items, difficulty 2 to 4 (one two-part modulus and argument item, one drag-point product) | | cz-arith, cz-polar |
| `homework-1.json` | 9 items, difficulty 3 to 5 (two at 5) | `is_stationary_ar2` (4), `fft` radix-2 (5) | cz-arith, cz-polar |

Homework also has two `expression` items, a numeric argument, a choice of the roots of $z^4 = -4$, an `order` proof of De Moivre by induction (two distractor lines), the AR(2) colleague `longform` (10-point rubric, one required row) and the performance task.

**Performance task.** l3's objective starts "Derive", so the level is rule-matched. `h-euler-derive` is `performance: "derivation"`: a blank longform, Euler's formula from the series, then $e^{i\pi} + 1 = 0$, $|e^{i\theta}| = 1$ and De Moivre; six rubric rows summing to 10, two required. The validator accepts it.

Traps: $\sqrt{-4}\sqrt{-9} = 6$ (l1); $\operatorname{Arg}(-1 - i)$ by $\arctan(b/a)$ (l2); $|e^{2 + 3i}| = e^5$ (l3); one root only, as `(8j) ** (1/3)` returns (l4). Edge cases: a real number has imaginary part 0 and a zero discriminant (l1 quiz); $z = 0$ has no argument and $\operatorname{Arg}(-2) = \pi$ with the signed-zero note (l2 code screen and quiz); $\theta + 2\pi$ (l3 quiz); $w^4 = 0$ and $n = 1$ (l4 quiz and code tests).

## Gates (SESSION PROTOCOL 4)

1. Validator: `node tools/validate.mjs` reports 0 errors. Level 1 files carry 5 warnings, all "a ladder screen usually reuses the previous canvas kind" (l2 screens 5 and 6, l3 screens 4 to 6), where the brief asks for `vectors` beside the Argand `plane`.
2. Voice scan (`VOICE_BASE=app/content/courses/complex/`): 0 sentences over 20 words, 0 explanations over three sentences.
3. Numbers: `python3 docs/reports/complex-L1-numbers.py` exits 0, 175 checks. Each figure is computed by exact arithmetic (fractions, closed forms, hand recurrences) and in floating point (complex, `cmath`, NumPy), then compared with the stated value. It also runs all 13 code widgets of the level in CPython: every solution passes, every starter fails.
4. Playthrough (`--local-cdn .../scratchpad/pkgs`), without and with `--mobile`: all six files green both times. l1 16 checks, l2 16, l3 16, l4 15, quizzes 4/4; review-1 10 of 10 recorded; homework-1 9 of 9 right, 47 of 47 marks, both longform items marked by the button. Screenshots at 1280 and 440 px were read; fixes made from them: order lines clipped at 440 px (formulas split), the vectors sum parallelogram hiding $z - w$ (sum moved to the explanation), overlapping labels.

## Numbers and sources

Every number is in the script with its two methods. The ones measured in Pyodide 0.27.7 (run in node from the local copy, and confirmed by the playthrough):

- `1j ** 2026` is $-1 + 1.2050400707482638 \times 10^{-13}i$ in CPython 3.13 and in Pyodide (l1 screen 10).
- `(8j) ** (1/3)` is `1.7320508075688774+0.9999999999999999j`; `cmath.phase(complex(-1, -0.0))` is $-\pi$ (l4, l2).
- Homework FFT budget: FFT of 4,096 points 0.035 s in Pyodide (CPython 0.011 s); the $N^2$ DFT 0.93 s at 1,024 points, so about 15 s at 4,096 (CPython about 5 s). The 4,096 case has `budget: 1000`, a 6 s limit.
- Every code `expect` was produced by running the solution in CPython and in Pyodide; they agreed to the last digit.

Seeds: `np.random.default_rng(3)` (l4 `dft` test, 16 points); `default_rng(1)`, `(2)`, `(4)`, `(5)` and `(6)` for the homework FFT tests (lengths 8, 1,024, 4,096 and a 64-point complex input).

## Conventions kept

AR(2) $x_t = \phi_1 x_{t-1} + \phi_2 x_{t-2} + \varepsilon_t$ with characteristic equation $z^2 - \phi_1 z - \phi_2 = 0$, stationary when both roots have $|z| < 1$; the lag-polynomial convention is stated once (l2 screen 12). Python's `1j` is named once (l1 screen 10). Complex answers are one `expression`, code returns complex values tested with complex `isclose`.

## course.json

No change proposed.

## Backlog

Four bullets under "Raised later (complex level 1):" in `docs/BACKLOG-INBOX.md`: the validator refusing table-cell `wrong` ids as keys, clipped `order` lines at 440 px, no `tol` on `expression`, overlapping labels on a transformed `vectors` canvas.
