# limits-thm level 1: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/limits-thm/homework-1.json`, item `h-prove-capped-wait`, index 9 (item 10 of 10; the homework had 9, nothing converted).
- Kind `derivation` (longform, empty box), difficulty 5, skill `dl-discrete`.
- Matched objective: l2 "Derive its mean $1/p$ by conditioning and by a series". l1 "Derive the binomial distribution from independent trials" also matches; l2's was chosen because its product needs two independent routes to one result.
- Task: a limit order that fills each minute with chance $p$ (same chance, independent minutes) and is cancelled after $m$ minutes. (a) the law of $T = \min(X, m)$, including the atom $q^{m-1}$; (b) $E[T]$ by conditioning, $e_m = 1 + q e_{m-1}$; (c) $E[T]$ by the finite series; (d) $p = 0.15$, $m = 10$: cancel chance 0.1969 (not $0.85^9 = 0.2316$), $E[T] = 5.354$, limit $1/p = 6.667$.
- Rubric 2, 3, 3, 1, 1. Rows 1 to 4 are `required` (9 points), one for each of (a) to (d). `rubric-passes.mjs`: the only minimal pass is rows 1 to 4. Only row 5 (the $m \to \infty$ limit) can be left out.
- Overlapping screens: l2 screens 7 (mean by conditioning, uncapped) and 8 (the series $\sum k q^{k-1}$ by shift and subtract, infinite); l2 screens 3 and 4 and `h-memory-mean` (geometric tails, memorylessness); `h-two-passes` (a mean wait by conditioning). New: the cap, which adds an atom to the law, a recurrence in $m$ in place of a fixed-point equation, a finite series whose shift leaves a boundary term, and the cancel chance as a trap against $P(T = m)$.
- Freshness grep (course folder, every hit read): `cancel`, `capped`, `0.85`, `0.15`, `5.35`, `limit order`, `resting order`, `0.95^`. Only a stock "limit order fills each minute" setup is shared. `fresh-check.mjs --file content/courses/limits-thm/homework-1.json`: 0 hits.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors. Expected warning "limits-thm/L1: has a performance task, remove from perf-pending". Manifest restored before commit.
2. `VOICE_BASE=app/content/courses/limits-thm python3 docs/reviews/voice-scan.py 35`: 0 and 0. One existing 36-word sentence in `homework-2.json` `h-long-exponential` was split to get there.
3. `<venv>/bin/python -I docs/reports/limits-thm-1-perf-numbers.py`: exit 0, 41 checks. Exact rationals for $m = 1$ to 40 (law sums to 1; series = recurrence = closed form). sympy for general $m$ and the limit. A seeded simulation of $10^6$ orders, plus a minute-by-minute Bernoulli simulation. Passing tick sets listed.
4. `node tools/playthrough.mjs --set limits-thm/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed, 2 longform marked by the button. A 356 px KaTeX column check (scratch `eqcheck.mjs`) found one display that scrolled. It was split with `aligned`, and all 8 displays now fit.

No backlog bullets. No course.json change.
