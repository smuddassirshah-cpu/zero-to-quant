# analysis level 3: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/analysis/homework-3.json`, item `h-prove-integral-test`, index 9 (item 10 of 10; the homework had 9, nothing converted).
- Kind `derivation` (longform, empty box), difficulty 5, skill `an-series`.
- Matched objective: l12 "Prove and use the comparison, ratio and integral tests." It is the only objective of the level that starts with prove (l11 define, l13 tell, l14 see).
- Task: (a) the integral test for a positive, continuous, decreasing $f$, with the tail bound $\sum_{n > K} a_n \le \int_K^\infty f$; (b) $\sum_{n \ge 2} 1/(n(\ln n)^2)$ converges, and its ratios tend to 1, so the ratio test is silent; (c) the bound promises a tail below 0.1 from $K = 22027$, and the lower bound $1/\ln(K + 1)$ puts the true smallest $K$ at 22,026 or 22,027.
- Rubric 3, 2, 3, 1, 1. Rows 1 to 4 `required` (9 points): both rows of (a), (b), and (c)'s $K$. `rubric-passes.mjs`: the only minimal pass is rows 1 to 4; row 5 (the lower bound) can be left out.
- Overlapping screens: l12 screens 1 to 3 (comparison by increasing, bounded partial sums), screen 8 (rectangles under $1/x^2$), screen 10 (tails between $\tfrac1{n+1}$ and $\tfrac1n$), quiz `q-ratio-one` (ratio limit 1 decides nothing) and `q-p-series`; `h-tail-m`, `r-integral-mid`, `r-harmonic-ten`; l13 screen 9 (a bound's $n$ against the true one); integrals l9 quiz 3 (the substitution for $(\ln x)^2$). New: the integral test proved in general with its tail bound, a series no screen uses, the ratio limit justified through $\ln(1 + t) \le t$, and a two-sided tail that pins $K$ to within one.
- Freshness grep (course folder, every hit read): `ln n)^2`, `\ln n`, `(\ln x)^2` (all courses), `e^{10}`, `22026`, `integral test`, `0.1`; `fresh-check.mjs --file`: 1 hit, `rearrange_to` in the existing `h-rearrange-minus-one`, which reuses l14's function by design; none on the new item.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "analysis/L3: has a performance task, remove from perf-pending". Manifest restored before commit.
2. `VOICE_BASE=app/content/courses/analysis python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python -I docs/reports/analysis-3-perf-numbers.py` (sympy, mpmath): exit 0, 58 checks. The antiderivative and limit in sympy against quadrature; the term bounds for $k < 3000$; the ratio squeeze for $n < 10^5$; $K$ by search and by $e^{10}$; the true tails by Euler-Maclaurin and by a 200,000-term direct sum, which agree ($S \approx 2.1097428$; the tail at 22,026 is 0.09999998); passing tick sets listed.
4. `node tools/playthrough.mjs --set analysis/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed, 2 longform marked by the button. 440 px shots read: no display equations, nothing past the gutter.

No backlog bullets. No course.json change.
