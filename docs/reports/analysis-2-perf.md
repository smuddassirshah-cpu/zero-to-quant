# analysis level 2: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/analysis/homework-2.json`, item `h-prove-falling-recursion`, index 8 (item 9 of 9; the homework had 8, nothing converted).
- Kind `derivation` (longform, empty box), difficulty 5, skill `an-sequences`.
- Matched objective: l8 "Prove that a bounded monotone sequence converges, and use it on a recursive sequence." All five objectives start with prove; l8's product (a theorem with an epsilon and N proof, used on a recursion, then an explicit $N$) covers the level best, and `h-prove-limit-product` already asks for l6 and l7's.
- Task: (a) a decreasing sequence bounded below tends to its infimum, from completeness, with the infimum's existence shown; (b) $a_1 = 2$, $a_{n+1} = (a_n^2 + 4)/5$ converges to 1, not the other root 4; (c) $0 < a_n - 1 \le (3/5)^{n-1}$, so $N = 15$ for 0.001, against the true first $n = 10$.
- Rubric 3, 2, 2, 2, 1. Rows 1 to 4 `required` (9 points): (a), both rows of (b), and (c)'s bound and $N$. `rubric-passes.mjs`: the only minimal pass is rows 1 to 4; row 5 (the comparison with $n = 10$) can be left out.
- Overlapping screens: l8 screens 3 and 4 (the theorem for increasing sequences, $L - \varepsilon$), screen 1 (an induction that a map keeps order), screen 5 (two roots, one ruled out by a bound), screen 6 (a falling sequence bounded below), screen 10 (a geometric gap and the first day within it), l8's summary note (the decreasing case stated), l3 screen 9 ($\inf A = -\sup(-A)$), `r-recursive-6`, `r-limit-4`, `h-square-trap`. New: the decreasing case proved through the infimum, a quadratic recursion with fixed points 1 and 4, a gap bounded by an inequality rather than known exactly, and the bound's $N$ against the true one.
- Freshness grep (course folder, every hit read): `a_n^2 + 4`, `tfrac35`, `(3/5)`, `bounded below`, `\inf`, `0.001`; `fresh-check.mjs --file` 0 hits.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "analysis/L2: has a performance task, remove from perf-pending". Manifest restored before commit.
2. `VOICE_BASE=app/content/courses/analysis python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/analysis-2-perf-numbers.py`: exit 0, 44 checks. The terms as exact Fractions (14), at 80 digits (200) and as floats; both inductions on every computed term; both factorisations as identities; the roots by formula and substitution; $N = 15$ by search and by logarithms; $n = 10$ by three routes; passing tick sets listed.
4. `node tools/playthrough.mjs --set analysis/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed, 2 longform marked by the button. 440 px shots read: no display equations, nothing past the gutter.

No backlog bullets. No course.json change.
