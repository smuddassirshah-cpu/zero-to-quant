# Answer check, pdes level 2 (3.2)

Independent recomputation of every keyed answer, tolerance, slip value, stated number and code test in `app/content/courses/pdes/` for `l5-separation-of-variables`, `l6-fourier-series`, `l7-when-fourier-converges`, `l8-heat-on-a-rod`, `review-2` and `homework-2`. Each value was worked from the question text alone. The author's scripts and `docs/reports/pdes-2.md` were not read. Scripts are in the scratchpad folder `ac-pdes2` (`calc.py`, `calc2.py`, `calc3.py`, `code_check.py`, `expr.cjs`, `expr2.cjs`, `scan.py`, `scan2.py`, `reuse.py`, `simpson.py`).

Second routes used:

- SciPy quadrature (`quad`) of every Fourier coefficient quoted: square wave `b_k` and the energy `E(b)`, `|x|` coefficients `a_0` and `a_3`, `x` coefficients `b_k` and the complex `c_1`, `c_2`, `x^3` (all `a_k` 0), the rod coefficients for ends 20 and 50, and the squared-sine areas. A Simpson readout that copies the engine's `integral()` (400 intervals) reproduces the l6 screen 0 caption: 1.424778 at `b = 1`, 1.190227 at `4/pi`.
- Partial sums by a dense grid (2,000,000 points) for the Gibbs peak (`M` = 5, 10, 50, 100: 1.182328, 1.179814, 1.179013, 1.178988, each at `x = pi/(2M)`) and `(2/pi) Si(pi) = 1.178980` by `scipy.special.sici`.
- Rod series with 2,001 terms against a root find (centre reaches 50 at `t = 0.934523`), against a stiff BDF solve of the 99-point system (46.834596) and against the exact eigen-solution of the grid (46.834596, and 47.435706 for nine points).
- The explicit scheme run in CPython for every quoted case: 200 intervals with ends 20 and 50 gives 65.441014 at `lambda = 0.4`; the 9-point matrix gives 46.519673 (`lambda = 0.4`, 25 steps) and 1,160.980670 (`lambda = 0.6`, 20 steps); 50, 100 and 200 intervals give 46.797890, 46.825437 and 46.832329.
- Corridor option by series (2,001 terms) and by the method of images (61 images): 37.077743 for `sigma = 0.2`, 54.035775 for `sigma = 0.25`. A 200,000-path daily-monitored simulation (252 steps) survives with frequency 0.4029.
- Every code solution run in CPython with NumPy under the engine's rules (prelude, solution, `setup` in the shared namespace, `isclose` with the item's `rel` and `abs`, `raises` by class name). Starters run the same way.
- Every expression widget graded by the repo's own `grade.js` (`exprEqual`) with Compute Engine 0.30.2 from the scratchpad `pkgs`: the key, ten to fourteen forms a learner would type (fraction, `\frac`, `\cdot`, `\left(` brackets, `\mathrm{i}`, `\imaginaryI`, implicit products such as `2D` and `kπ`) and every `wrong` expression.
- A structural scan of all 77 widgets: wrong values inside the answer tolerance, answer inside a wrong tolerance, wrong values overlapping each other, `byKey` keys naming nothing, wrong ids without feedback text, choice and multi correct counts, order ids against lines, table cell ids against `byKey`, literal backslash-n in every string, and a grep of every numeric key and slip value against the eight pdes lessons.

**Summary.** All 77 widgets were recomputed (45 numeric, 11 choice, 5 expression, 5 order, 5 code with 38 hidden tests, 3 slider, 1 table with 3 editable cells, 1 multi, 1 longform; 114 slip entries). Every key is right. Every code solution passes all its tests and every starter fails them. No choice or multi distractor is also correct, no numeric slip lies inside an answer tolerance, and no two slips overlap. Five items need a fix (errors 1 to 5): a slip value that no slip produces, an equivalent form the grader rejects, literal `\n` in a model answer, a false "right to two places", and three wrong numbers in l8's explanation. Thirteen items need a decision or a small edit (warnings 6 to 18), most of them in-course repeats of lesson numbers (DECISIONS "Fresh numbers in reviews and homework"). Nine are notes (19 to 27).

## Widgets checked

Numeric rows give the key and tolerance, then my value and my value for each named slip. `ok` means my value lies inside the key's tolerance and each slip value lies inside its stated value's tolerance. Slips not shown are 0 or the quoted number.

| File | Screen or item | Key | My value | Verdict |
|---|---|---|---|---|
| l5 | screen[0] | numeric 1.8085, abs 0.0006 | 3e^-0.5 - e^-4.5 = 1.808483 (slips: one-mode 1.819592; start 2) | ok |
| l5 | screen[1] | order a1..a5; d1, d2 | chain is strict; d1 and d2 false as `why` says | ok |
| l5 | screen[2] | numeric 0.1353, abs 0.0006 | e^-2 = 0.135335 (slips: no-lam 0.367879; straight -1) | ok |
| l5 | screen[3] | slider lambda = 4, tol 0.05 | X(pi) = sin(sqrt(lambda) pi)/sqrt(lambda) has one zero in [2, 5.5], at 4 | ok |
| l5 | screen[4] | choice cancel | sinh(2 pi)/2 = 133.87 (canvas "about 134"; hint 535 c1 = 535.49); X(0) = 0 then X(pi) = 0 forces c1 = 0; three distractors false | ok; key 1.69 times the distractors (warning 16) |
| l5 | screen[5] | expression (k pi / L)^2 | Compute Engine: 9 typed forms equal (`\frac{k^2\pi^2}{L^2}`, `(k\pi/L)^2`, `\pi^2k^2L^{-2}` and others); 4 slips differ | ok |
| l5 | screen[6] | numeric 0.077, abs 0.0005 | ln 2/9 = 0.0770164 (slips: three 0.231049; same 0.693147); explain 0.006105 = e^-4/3 | ok |
| l5 | screen[7] | numeric 1.3679, abs 0.0006 | 1 + e^-1 = 1.367879 (slips: decayed 0.367879; flat 1) | ok |
| l5 | screen[8] | code: eigenvalues, separated; 7 tests + example | solution 8/8; starter 0/8; 2.467401, 9.869604, 22.206610; 1.808483; 0.220302, 0.191535 | ok (warning 18) |
| l5 | screen[9] | numeric 8, abs 0 | D k^2 = 2 x 4 = 8 (slips: no-D 4; dk-squared 16) | ok |
| l5 | screen[10] | numeric 0.2231, abs 0.0006 | e^-1.5 = 0.223130 (slips: k-gap 0.740818; alone 0.201897; inverse-k 0.25); explain e^-0.1 = 0.904837 | ok |
| l5 | quiz[0] q-lambda2 | numeric 9.8696, abs 0.0006 | pi^2 = 9.869604 (slips: no-square 3.141593; no-L 39.478418); explain 2.4674, 9.8696, 22.2066 | ok |
| l5 | quiz[1] q-ratio | numeric 0.0183, abs 0.0004 | e^-4 = 0.0183156 (slips: linear 0.367879; alone 0.011109) | ok |
| l5 | quiz[2] q-insulated | choice const | lambda = 0 only; cos x and sin x decay | ok |
| l5 | quiz[3] q-fade | numeric 2, abs 0.01 | 1/0.5 = 2 (slips: no-D 1; times-D 0.5) | ok |
| l6 | screen[0] | slider b = 1.27, tol 0.04; wrong 0.95 to 1.05 | E(b) = 2 pi - 8b + pi b^2, minimum at 4/pi = 1.2732 (E = 1.190227); E(1) = 1.424778 (quad and engine Simpson) | ok |
| l6 | screen[1] | numeric 3.1416, abs 0.001 | int sin^2 3x = 3.141593 (slips: zero 0; two-pi 6.2832; half-range 1.570796); j = 2, k = 3 gives -3e-18 | ok |
| l6 | screen[2] | order s1..s4; d1, d2 | strict chain; d1 false (E = 0 is not the minimum); d2 false (int sin^2 = pi) | ok |
| l6 | screen[3] | expression 2(1-(-1)^k)/(k pi) | key = 4/(k pi) odd, 0 even (quad: 1.273240, 0, 0.424413, 0, 0.254648); the `\cos k\pi` form is rejected | error 2 |
| l6 | screen[4] | numeric 1.1035, abs 0.0006 | 4/pi (1 - 1/3 + 1/5) = 1.103474 (slips: first-only 1.273240; stopped-at-3 0.848826; no-signs 1.952301) | key ok; no-signs 1.9576 wrong (error 1) |
| l6 | screen[5] | numeric -0.1415, abs 0.0006 | a_3 = -4/(9 pi) = -0.141471 (quad -0.141471; slips: a1 -1.273240; no-square -0.424413; sign 0.141471) | ok |
| l6 | screen[6] | numeric 1.5708, abs 0.001 | a_0/2 = pi/2 = 1.570796 (slips: a0 3.141593; zero 0) | ok |
| l6 | screen[7] | expression i/2 | c_2 = (0 - i b_2)/2 with b_2 = -1: i/2 (quad: re 0, im 0.5); 13 typed forms equal; -i/2, -i, 1/2 differ | ok |
| l6 | screen[8] | code: fourier_coeffs, partial_sum; 8 tests + example | solution 9/9; starter 0/9; 1.273238 (key 1.273240), 0.666662 (0.666667, diff 5.3e-6 of 1e-5), -0.141472, 3.141593, 1.103471 (key 1.103474) | ok (note 22) |
| l6 | screen[9] | choice a | x^3 odd: x^3 cos kx odd, all a_k 0 (quad 0, 0, 0, 0) | ok |
| l6 | screen[10] | table: 60, 15, 4 (abs 0.01) | 12 prices match to 2 places; sums 720, 90.000000, 24.000000; each square sums to 6 | ok |
| l6 | quiz[0] q-x-b3 | numeric 0.6667, abs 0.0006 | 2/3 = 0.666667 (slips: b2 -1; neg -0.666667; two 2) | ok |
| l6 | quiz[1] q-leibniz | numeric 0.7854, abs 0.0006 | pi/4 = 0.785398 (slips: half 1.570796; one 1) | ok |
| l6 | quiz[2] q-two-pi | numeric 1.2732, abs 0.0006 | 4/pi = 1.273240 (slips: two-pi 0.636620; no-divide 4; times-pi 12.566371) | ok |
| l6 | quiz[3] q-finite | choice b13 | b_1 = 3, b_3 = 1 | ok |
| l7 | screen[0] | numeric 1.1798, abs 0.0006 | M = 10 peak 1.179814 at x = 0.157080 (slips: M = 5 1.182328; wave 1); explain 1.1790 at M = 50 (1.179013) | ok |
| l7 | screen[1] | numeric 8.95, abs 0.02 | (2/pi) Si(pi) = 1.178980; overshoot 8.949% of the jump (slips: of-height 17.898; peak 117.898) | ok |
| l7 | screen[2] | numeric -2, abs 0 | |a_k| = 4/(pi k^2): log slope -2 (slips -1, 2) | ok |
| l7 | screen[3] | numeric 0.0635, abs 0.0006 | pi/2 - (4/pi) sum to k = 9 = 0.063453 (slips: one-term 0.297557; n99 0.006366); explain values match | ok |
| l7 | screen[4] | expression 1/N | integral from N of x^-2 = 1/N; `N^{-1}`, `\frac1N` equal; 1/N^2, 1/(2N^2), ln N differ; tail at N = 10 is 0.095166 | ok |
| l7 | screen[5] | order p1..p4; same [p1, p2]; d1, d2 | energy 2 pi^2/3 = 6.579736; sum 1/k^2 = pi^2/6 = 1.644934 (numeric Parseval agrees to 1e-12); d1, d2 false | ok (note 25) |
| l7 | screen[6] | choice stays | peak height 1.182328, 1.179814, 1.179013 for M = 5, 10, 50; limit 1.17898 | ok |
| l7 | screen[7] | numeric 0, abs 0.001 | sin k pi = 0 for every k (slips: f 3.1416; minus -3.1416) | ok |
| l7 | screen[8] | code: gibbs_peak, decay_slope; 7 tests + example | solution 8/8; starter 0/8; 1.182328, 1.179814, 1.179013, 1.273240; slopes -1, -2, -1.5 to 1e-15 | ok |
| l7 | screen[9] | choice mid | midpoint of -1 and 1 is 0 | ok |
| l7 | screen[10] | numeric 200, abs 0 | 4/N^2 = 0.0001 gives N = 200 (slips: digital-rule 2000; hundred 100, where the call is 0.0004) | ok |
| l7 | quiz[0] q-odd-sum | numeric 1.2337, abs 0.0006 | pi^2/8 = 1.233701 (slips: even 0.411234; all 1.644934) | ok |
| l7 | quiz[1] q-midpoint | numeric 5, abs 0.001 | (2 + 8)/2 = 5 (slips 2, 8); 8.95% of 6 is not quoted | ok |
| l7 | quiz[2] q-smooth | choice smooth | e^{sin x} analytic; jump 1/k; kink 1/k^2 | ok (note 20) |
| l7 | quiz[3] q-peak-place | numeric 0.0157, abs 0.0003 | pi/200 = 0.015708 (slips: m50 0.031416; height 1.179); M = 100 peak at 0.015708 (1.178988) | ok |
| l8 | screen[0] | slider t = 0.93, tol 0.03; wrong 0.3 to 0.6 | centre 50 at t = 0.934523; ln(8/pi) = 0.934712; centre at t = 0.3 and 0.6 is 91.49 and 69.69 (prose "above 60") | ok |
| l8 | screen[1] | order m1..m4; d1, d2 | method is sound in this order; d1, d2 false | ok (warning 15) |
| l8 | screen[2] | numeric 9.5493, abs 0.0006 | b_2 = 30/pi = 9.549297 (quad 9.549297; slips: b1 82.760570; no-k 19.098593; neg -9.549297); u(pi/2, 1) = 65.442508; explicit 200 intervals 65.441014 | ok (note 19) |
| l8 | screen[3] | numeric -8.3532, abs 0.0006 | -(4/dx^2) sin^2(3 dx/2) = -8.353217 (slips: exact -9; no-half -26.526230); N = 100: -0.999918, -3.998684, -8.993340; stiff solve 46.834596 | ok (note 21) |
| l8 | screen[4] | expression h^2/(2D) | `\frac{h^{2}}{2\cdot D}`, `\frac12\frac{h^2}{D}`, `0.5h^2/D` equal; h^2/D, h/(2D), h^2/2 differ | ok (warning 17) |
| l8 | screen[5] | numeric -1.3413, abs 0.0006 | 1 - 4(0.6) sin^2(9 pi/20) = -1.341268 (slips: lam04 -0.560845; centre -0.2; lam05 -0.951057); 1,160.98 and 46.5197 recomputed; series 47.4487; nine points exact 47.4357 | ok |
| l8 | screen[6] | numeric 99.9112, abs 0.0006 | 99.911187 (slips: one-term 115.207478; start 100); four terms 99.906956, diff 0.004230 | ok |
| l8 | screen[7] | numeric 117.9, abs 0.15 | 100 x 1.178980 = 117.898 (slips: none 100; of-start 108.95 inside 108.9 +/- 0.2) | ok |
| l8 | screen[8] | code: rod_series, rod_explicit; 9 tests + example | solution 10/10; starter 0/10; 46.834628, 99.911187, 115.207478, 23.417314; scheme 46.797890, 46.825437; raises ValueError at 0.6; 200 intervals within 0.0023 | ok (warning 14) |
| l8 | screen[9] | choice decay | term k is 400/(k pi) e^{-k^2 t}; k = 3 over k = 1 at t = 1 is 0.000112 | ok; key 87 against 80 and 29 characters (note 26) |
| l8 | screen[10] | numeric 37.08, abs 0.02 | series 0.370777 and images agree; 37.0777 (slips: daily 40.29 simulated; no-amp 29.121) | key ok; explain numbers wrong (error 5); note 23 |
| l8 | quiz[0] q-centre | numeric 46.8346, abs 0.0006 | 46.839865 - 0.005238 = 46.834628 (slips: one-term 46.839865; sign 46.845103) | ok |
| l8 | quiz[1] q-dt | numeric 0.0493, abs 0.0002 | (pi/10)^2/2 = 0.049348 (slips: no-half 0.098696; h-only 0.157080) | ok (warning 17) |
| l8 | quiz[2] q-blow | choice top | 1 - 4(0.6)(0.975528) = -1.341268; others false | ok; key 2.33 times (warning 16) |
| l8 | quiz[3] q-max | choice max | maximum principle | ok; key 2.03 times (warning 16) |
| review-2 | item[0] r-lambda-len4 | numeric 2.4674, abs 0.0006 | (pi/2)^2 = 2.467401 (slips: no-square 1.570796; one-L 9.869604) | ok; repeats l5 (warning 10) |
| review-2 | item[1] r-decay-ratio | numeric 0.1225, abs 0.0006 | e^-2.1 = 0.122456 (slips: k-gap 0.740818; alone 0.082085) | ok (note 27) |
| review-2 | item[2] r-b4 | numeric 0.6366, abs 0.0006 | 2/pi = 0.636620 (slips: two-pi 0.318310; raw 2) | ok; repeats l6 (warning 11) |
| review-2 | item[3] r-mean-x2 | numeric 3.2899, abs 0.0006 | pi^2/3 = 3.289868 (slips: a0 6.579736; zero 0) | ok |
| review-2 | item[4] r-coefficient-decay | choice kink | slope -2 is a kink | ok; key 39 against 6 and 51 characters |
| review-2 | item[5] r-parseval | numeric 1.0147, abs 0.0006 | pi^4/96 = 1.014678 (numeric Parseval agrees to 1e-12; slips: no-constant 4.058712; no-factor 0.0625) | key ok; no-factor feedback names no slip (warning 13) |
| review-2 | item[6] r-stable-step | numeric 0.0247, abs 0.0002 | (pi/20)^2/(2 x 0.5) = 0.024674 (slips: no-D 0.012337; h-only 0.078540) | ok (warning 17) |
| review-2 | item[7] r-linearity | numeric 49.9556, abs 0.0006 | 99.911187/2 = 49.955593 (slips: one-term 57.603739; same 99.9112) | ok; repeats l8 (warning 8) |
| review-2 | item[8] r-kernel-peak | numeric 0.2821, abs 0.0006 | 1/sqrt(4 pi) = 0.282095 (slips: t1 0.398942; no-root 0.079577) | ok; repeats l3 (warning 9) |
| homework-2 | item[0] h-heat-rod | code: sine_coeffs, heat_rod; 7 tests + example | solution 8/8; starter 0/8; [127.324, 0, 42.4413]; 46.834625 (key 46.834628, tol 1e-3); 1.808483; PARAB [0.393918, 0.556788] (computed 0.393918, 0.556788) | ok; tests repeat lessons (warning 12) |
| homework-2 | item[1] h-no-lambda | order s1..s5; d1, d2 | energy argument sound in this order; d1 false (X = 0 at the ends); d2 false (a square) | ok |
| homework-2 | item[2] h-centre-nonzero | numeric 65.4425, abs 0.0006 | 35 + 30.445912 - 0.003404 = 65.442508 (slips: one-term 65.4459; sign 65.4493; steady 35); b_1 = 82.760570, b_3 = 27.586857 | key ok; verbatim copy of l8 screen 2 (warning 6) |
| homework-2 | item[3] h-gibbs-true | multi mid, peak, slow | 0 at the jump; peak 1.17898 rounds to 1.1790; coefficients 4/(k pi); uniform and gone are false | ok (note 26) |
| homework-2 | item[4] h-parseval-x2 | numeric 1.0823, abs 0.0006 | pi^4/90 = 1.082323 (slips: no-constant 2.435227; no-sixteen 17.317172); energy 2 pi^4/5 = 38.963636 (numeric Parseval 38.963636) | ok |
| homework-2 | item[5] h-step-count | numeric 2534, abs 0 | 1/(0.4 (pi/100)^2) = 2533.0296, ceiling 2534 (slips: floor 2533; wrong-dx 25000); lambda used 0.399847 | ok |
| homework-2 | item[6] h-corridor-wide | numeric 54.04, abs 0.02 | series and images 54.0358 (slips: d-sigma-sq 22.949; no-amp 42.4545); k = 1 0.540548, k = 3 -0.000190 | ok (note 24) |
| homework-2 | item[7] h-colleague-terms | longform, 5 rubric lines of 2 points | rubric sums to 10; -17.26 (17.2554), 97.95 (97.9521), 2.09 (2.0903), 99.9070, 0.0042, 6.4e-5 for k = 11 all recompute | numbers ok; literal `\n` (error 3); "right to two places" false (error 4); repeats l8 (warning 7) |

## Mismatches

### Errors

1. **`l6-fourier-series.json`, screen 4, `wrong` `no-signs`: the value is not the slip it names.** Adding the three sizes without signs gives $\tfrac4\pi(1 + \tfrac13 + \tfrac15) = 1.9523$ (1.2732 + 0.4244 + 0.2546 = 1.9522). The file has 1.9576, so a learner who makes this slip and types 1.9523 gets the generic line. Fix: set `value` to 1.9523 and keep `tol.abs` 0.001 (it also accepts 1.9522 from the rounded sizes). The `byKey` text is right.

2. **`l6-fourier-series.json`, screen 3, expression: the form the prose invites is graded wrong.** The prose gives $\int f\sin kx\,dx = 2(1 - \cos k\pi)/k$, so the natural answer is `\frac{2(1-\cos k\pi)}{k\pi}`. The grader returns false for it (and for `\frac{2(1-\cos(k\pi))}{k\pi}` and `\frac{2(1+(-1)^{k+1})}{k\pi}`). Cause: the engine tests at six non-integer points between 0.3 and 3, where Compute Engine evaluates the key's $(-1)^k$ as NaN while $\cos k\pi$ is finite, so the numeric test fails and the symbolic test cannot join the two. Only forms that keep $(-1)^k$ pass. Fix: add to `widget.accept` the two LaTeX forms `"\\frac{2(1-\\cos(k\\pi))}{k\\pi}"` and `"\\frac{2(1-\\cos k\\pi)}{k\\pi}"`. Tested: a cosine form then equals either, and the `(-1)^k` forms still equal the key. Consider asking for odd $k$ in the question instead if more forms (such as `4/(k\pi)` for odd $k$) are wanted.

3. **`homework-2.json`, item `h-colleague-terms`, `model` holds literal backslash-n sequences, not line breaks.** The string has 0 real newlines and 6 two-character `\n` sequences (three paragraph breaks, written `\\n\\n` in the file). `prose()` splits on real blank lines, so the four numbered sections render as one block with `\n\n` visible. This is the same slip as `answers-3.2-pdes-1.md` error 2. Fix: in the `model` string replace the three `\\n\\n` (as written in the file) with `\n\n`. A scan of every string in the six files found no other literal `\n`.

4. **`homework-2.json`, item `h-colleague-terms`, `model` section 3 and rubric line 3: "46.84 is right to two places" is false.** The true value is 46.8346, which rounds to 46.83. The one-term value 46.8399 rounds to 46.84. The report is 0.0054 high, not right to two places. Fix in `model`: replace "The one-term value 46.8399 is only 0.0052 too high, so 46.84 is right to two places." with "The one-term value 46.8399 is only 0.0052 too high, so 46.84 is close, but the true value rounds to 46.83." Fix rubric line 3: "Says the 46.84 report is close but not exact: the true value is 46.8346, which rounds to 46.83." (If warning 7 is taken, this item is rewritten anyway.)

5. **`l8-heat-on-a-rod.json`, screen 10, `explain.text`: three stated numbers are wrong.** The text says "The first term is $1.2732 \times 0.29116 = 0.37073$ and the $k = 3$ term is about $-10^{-6}$". Computed twice: $e^{-1.2337} = 0.29121$, so the first term is $1.2732 \times 0.29121 = 0.37078$; the $k = 3$ term is $-\tfrac{4}{3\pi}e^{-11.103} = -6.4 \times 10^{-6}$. The final $P = 0.370777$ and £37.08 are right (it is 0.37078 minus 0.0000064). The `byKey` line for `no-amp` ($100e^{-1.2337} = 29.12$) is right. Fix: "The first term is $1.2732 \times 0.29121 = 0.37078$ and the $k = 3$ term is about $-6 \times 10^{-6}$, so $P = 0.370777$ and the value is £37.08." The hint "1.2732 × 0.2912 = 0.3707" is right.

### Warnings

6. **`homework-2.json`, item `h-centre-nonzero`, repeats `l8-heat-on-a-rod.json` screen 2 verbatim.** Same ends (20 and 50), same start (100), same $D$, same question point and time, so the key 65.4425, $b_1 = 82.7606$, $b_3$, the slips 65.4459 and 65.4493, and the sentence "explicit scheme on 200 intervals gives 65.4410" are the lesson's (DECISIONS "Fresh numbers in reviews and homework"). Fix with ends held at 10 and 70, start 100, $D = 1$: $u = 10 + \tfrac{60x}{\pi} + \sum_kb_ke^{-k^2t}\sin kx$ with $b_k = \tfrac2\pi\cdot\tfrac{90(1-(-1)^k) + 60(-1)^k}{k}$, so $b_1 = 240/\pi = 76.3944$ and $b_3 = 80/\pi = 25.4648$ (both by quadrature). $u(\pi/2, 1) = 40 + 76.3944e^{-1} - 25.4648e^{-9} = 40 + 28.1039 - 0.0031 = 68.1008$. `answer` 68.1008 with `tol.abs` 0.0006; `wrong` `one-term` 68.1039 (tol 0.0004), `sign` 68.1071 (tol 0.0004), `steady` 40 (tol 0.01). None of these numbers occurs in the course. Drop the explicit-scheme sentence or compute it again.

7. **`homework-2.json`, item `h-colleague-terms`, repeats the scenario and numbers of `l8-heat-on-a-rod.json` screen 6 and `q-centre`.** Same colleague, same rod ($L = \pi$, $D = 1$, start 100), same reports (115.21 at $t = 0.1$, 46.84 at $t = 1$), same values 99.9112, 46.8346, 99.9070, 0.0042, 0.0052. Fix with a start of 60, same rod: first term at $t = 0.1$ is $\tfrac{240}{\pi}e^{-0.1} = 69.12$ (above 60, so wrong); the full series gives 59.9467 there; $k = 3$ term $-\tfrac{80}{\pi}e^{-0.9} = -10.35$. At $t = 1$ the first term is 28.1039, the full series 28.1008, the $k = 3$ term $-0.0031$, and 28.10 is right to two places (both round to 28.10, so error 4's wording becomes true). The colleague's reports become 69.12 and 28.10. Recompute the four-term value and the rule's example cutoffs for the new amplitude, and update the rubric numbers. This also removes error 4.

8. **`review-2.json`, item `r-linearity`, repeats `l8-heat-on-a-rod.json` screen 6.** The prose gives the lesson's 99.9112 and 115.2075 at $t = 0.1$, and the same-id slip `same` is 99.9112. Fix: use $t = 0.3$ and a start of 40. Prose: "For the start of 100, the centre at $t = 0.3$ is 91.4857, and the first term alone gives 94.3239." Question: "What is the true centre at $t = 0.3$ for the start of 40?" `answer` 36.5943 (91.4857 x 0.4 = 36.59428), `accept` "36.5943: 0.4 times 91.4857, since the equation is linear", `wrong` `one-term` 37.7296 (0.4 x 94.3239, tol 0.0006), `same` 91.4857 (tol 0.001). Update `byKey` and `explain` ("36.59 is below 40"). None of these numbers occurs in the course.

9. **`review-2.json`, item `r-kernel-peak`, repeats `l3-heat-kernel.json` `q-peak`.** The key 0.2821 ($1/\sqrt{4\pi}$) is the l3 quiz key, and the slip `t1` 0.3989 is the slip there and in l2; `no-root` 0.0796 is an l2 value. Fix: $D = 0.25$, $t = 3$, so $4\pi Dt = 3\pi$. `answer` 0.3257 ($1/\sqrt{3\pi} = 0.325735$); `wrong` `t1` 0.5642 ($1/\sqrt{\pi}$, the peak at $t = 1$) and `no-root` 0.1061 ($1/(3\pi)$). Update the prose ("Take $D = 0.25$ and $t = 3$"), `accept`, `byKey` and `explain` ($3\pi = 9.4248$, $1/\sqrt{9.4248} = 0.3257$). None of these numbers occurs in pdes.

10. **`review-2.json`, item `r-lambda-len4`, repeats `l5-separation-of-variables.json`.** The key 2.4674 is $\lambda_1$ for $L = 2$ in the l5 code test and the `q-lambda2` explain, and the slip `one-L` 9.8696 is the `q-lambda2` key. Fix: $L = 3$, $k = 2$: `answer` 4.3865 ($(2\pi/3)^2 = 4.386491$), `no-square` 2.0944 ($2\pi/3$), `one-L` 13.1595 ($(2\pi)^2/3$). Update the prose, `accept` ("$(2\pi/3)^2 = 4\pi^2/9$"), `byKey` and `explain`.

11. **`review-2.json`, item `r-b4`, key repeats an `l6-fourier-series.json` number.** $2/\pi = 0.6366$ is the l6 `q-two-pi` slip `two-pi` and appears in its explain. The item is the same skill with 2 for 4. Fix: set the integral to 3: `answer` 0.9549 ($3/\pi = 0.954930$), `two-pi` 0.4775 ($3/(2\pi)$), `raw` 3. Update `accept`, `byKey` and `explain`.

12. **`homework-2.json`, item `h-heat-rod`, three hidden tests repeat lesson values.** `heat_rod(CONST, [pi/2], 1)` is l8's 46.834628, `heat_rod(MODES, [pi/2], 0.5)` is l5's 1.808483, and `sine_coeffs(CONST, 3, pi)` expects l8's [127.324, 0, 42.4413]. The explain also quotes 46.834628 and 1.808483. Fix: replace with `heat_rod(CONST, np.array([np.pi / 3]), 0.2)` expecting [90.13026] (series 90.130265, tol 1e-3), `heat_rod(CONST, np.array([np.pi / 4]), 0.3)` expecting [68.70398] (68.703983, tol 1e-3), `heat_rod(MODES, np.array([np.pi / 6]), 0.25)` expecting [1.273600] (3 e^-0.25/2 + e^-2.25 = 1.2736004, tol 1e-4), and `sine_coeffs(PARAB, 3, 2).tolist()` expecting [1.03205, 0.0, 0.038224] (quad, tol 1e-4). Keep the PARAB heat test and the maximum-principle test. Update the explain.

13. **`review-2.json`, item `r-parseval`, `wrong` `no-factor`: 0.0625 is not produced by any slip.** The feedback says "0.0625 is 1/16", which is a number, not an error. The slip it describes (forgetting that $a_k^2$ carries $1/\pi^2$, so dividing the remainder by 16 alone) gives $\tfrac{\pi^2}{6}/16 = 0.1028$. Fix: `value` 0.1028 (tol 0.0006) and text: "0.1028 divides the remainder $\pi^2/6$ by 16 alone. Each $a_k^2$ is $16/(\pi^2k^4)$, so the factor is $16/\pi^2$."

14. **`l8-heat-on-a-rod.json`, screen 8: a hidden test needs a guard the problem never states.** The test `rod_explicit(100, 0.6, 1)` expects `ValueError`. The prose, the starter docstring and `how` do not say the function must raise; only the third hint rung and the feedback line mention it. A learner who implements the scheme as described returns a number and fails one of nine tests with no way to know why. Fix: add to the prose "It raises `ValueError` if `lam` is above 0.5." and to the starter docstring of `rod_explicit` "Raise ValueError if lam > 0.5."

15. **`l8-heat-on-a-rod.json`, screen 1, order: a valid order is rejected.** Line m1 (each $e^{-k^2t}\sin kx$ solves the equation and meets the ends) and line m2 (expand the start in sines) do not depend on each other; m3 needs both. A learner who expands the start first is marked wrong. Fix: add `"same": [["m1", "m2"]]`.

16. **Choice keys visibly longer than their distractors** (characters without `$`; key against each distractor): `l5` screen 4 (93 against 62, 46, 57), `l8` `q-blow` (85 against 37, 36), `l8` `q-max` (69 against 42, 26). Suggested keys with the distractors padded to match:
    - `l5` screen 4: "$X(0) = 0$ gives $c_2 = -c_1$; then $X(\pi) = 0$ forces $c_1 = 0$" (62).
    - `l8` `q-blow`: key "The top mode is multiplied by $-1.34$ a step, so it grows" (56); distractors "Too few terms of the series were kept for it to settle" (54) and "The grid is too fine for the heat to show in the answer" (55).
    - `l8` `q-max`: key "The maximum principle: $u$ never exceeds the start or end values" (62); distractors "Energy decay: $\int u^2\,dx$ falls as time passes, but not point by point" (68) and "Orthogonality of the sines, which gives the coefficients $b_k$" (60).

17. **Stability wording is stricter than the maths in `l8-heat-on-a-rod.json` screens 4 and 5 and `q-dt`, and in `review-2.json` `r-stable-step`.** "Largest stable time step" and "the top mode has factor $1 - 4\lambda$" hold only as the bound for a fine grid. On the 9-interior-point grid the top mode factor is $1 - 3.902\lambda$ and the scheme stays stable up to $\lambda = 1/(2\cos^2(\pi/20)) = 0.5125$ ($\Delta t = 0.0506$ for $q$-dt, not 0.0493). Screen 5's feedback calls $-0.9511$ at $\lambda = 0.5$ "the edge of stability", though it lies inside $(-1, 1)$. The keys are right for the stated bound $\Delta t \le h^2/(2D)$. Fix: in screen 4 ask for "the step that keeps $\lambda \le \tfrac12$" in place of "the largest stable time step" and write "The highest mode has a factor close to $1 - 4\lambda$" in its explain; in screen 5 `lam05` write "$-0.9511$ is the factor for $\lambda = 0.5$, just inside the safe bound"; in `q-dt` and `r-stable-step` write "the largest step the bound guarantees" (both already state the rule).

18. **Code tests call `.tolist()` on the return value, so a function that returns a list fails.** `l5` screen 8 `eigenvalues` is the clear case: the natural list comprehension `[D * (k * pi / L) ** 2 for k in range(1, N + 1)]` passes the example (it runs `np.round` first) and fails hidden tests 1 and 2 with an `AttributeError`. The starter says only "Decay rates ... for k = 1..N". The same holds for `separated`, `partial_sum`, `rod_series`, `sine_coeffs` and `heat_rod`. Fix: in each test wrap the call, for example `np.asarray(eigenvalues(2, 3)).tolist()`, or state "returns a NumPy array" in the docstring. The wrap is the safer fix because the loop forms are valid.

### Notes

19. **`l8-heat-on-a-rod.json` screen 2 `explain` and `homework-2.json` `h-centre-nonzero` `explain`: "an explicit scheme on 200 intervals gives 65.4410" does not say which $\lambda$.** It is 65.441014 at $\lambda = 0.4$, 65.439623 at 0.5 and 65.441572 at 0.25. Fix: add "with $\lambda = 0.4$".

20. **`l7-when-fourier-converges.json` `q-smooth`, `square` `why`: "the slowest decay of the four" lists three options.** The prose says "Three periodic functions". Fix: "of the three".

21. **`l8-heat-on-a-rod.json` screen 3, `feedback.correct`: "$-40.528 \times 0.2061 = -8.3532$".** The product of the rounded factors is 8.3528. The exact value is 8.3532 (40.52847 x 0.2061074). Fix: "$-40.528 \times 0.20611 = -8.3532$" and "$\sin^2(0.4712) = 0.2061$" can stay in the explain.

22. **`l6-fourier-series.json` screen 8 `explain`: "matches $4/\pi$, $2/3$ and $\pi$ to five places".** The trapezium values are 1.273238, 0.666662 and 3.141593, so $2/3$ differs in the fifth place (0.66666 against 0.66667). The tests allow $10^{-5}$, and 0.666662 uses 53 percent of it. Fix: "to within 0.00001".

23. **`l8-heat-on-a-rod.json` screen 10, `wrong` `daily`: value 40 with `tol.abs` 0.1 sits below the simulated survival.** 200,000 paths over 252 daily steps survive with frequency 0.4029, so a learner who simulates gets 40.3 and misses the slip. The feedback says "0.400". Fix: `value` 40.3, `tol.abs` 0.4, text "£40 is about the frequency from daily monitoring, 0.40."

24. **`homework-2.json` `h-corridor-wide`:** the generic line and the explain give $D(\pi/L)^2 = 0.8568$; the value is 0.856736, so 0.8567. The `d-sigma-sq` slip is 22.949 (22.95), not 22.96; it lies inside its tolerance 0.05, so grading is unaffected. Fix: 0.8567 in both places and `value` 22.95.

25. **`l7-when-fourier-converges.json` screen 5, order:** `same [p1, p2]` is right, but p2, p3, p1, p4 is also a valid order (p3 needs only p2's notation, p1 is independent) and is rejected. `same` cannot express it. Leave, or reword p3 to restate "$\sum b_k^2$" and move p1 into a `same` pair with p3. No change needed for the key.

26. **`homework-2.json` `h-gibbs-true` restates sentences of `l7-when-fourier-converges.json` (1.179, 8.95%, "converges to the midpoint").** The three correct options are 60, 62 and 73 characters against 45 and 42 for the distractors. This is a recall item. If a fresh test is wanted, ask for the value at the jump of $f = x$ at $x = \pi$ (0) or the overshoot for a jump of 6 (0.537), but the item is acceptable. Likewise `l8` screen 9: key 87 characters against 80 and 29, only one distractor is short.

27. **Engine items 501 and 502 and P32-expr-exp.** Level 2 has no expression key containing `\exp`, so item 501 does not reach it. Item 502 (a letter before a bracket) is exercised by `(k\pi/L)^2`, `2D`, `(-1)^k` and `(1-(-1)^k)`: all grade as products. Slip values that coincide with a lesson's slip in another question: `r-decay-ratio` `k-gap` 0.7408 equals l5 screen 10 `k-gap` (both $e^{-0.3}$ from a different gap). Harmless, but a fresh gap (modes 2 and 6) would remove it.

## Commands to reproduce

Run from the scratchpad folder `ac-pdes2` (needs `pip install --target pylib scipy sympy mpmath numpy`): `python3 calc.py`, `python3 calc2.py`, `python3 calc3.py`, `python3 code_check.py`, `node expr.cjs`, `node expr2.cjs`, `python3 scan.py`, `python3 scan2.py`, `python3 reuse.py`.
