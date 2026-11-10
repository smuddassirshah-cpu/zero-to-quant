# Fluency sets: random-vars (brief `docs/briefs/fluency.md`, second wave, agent 3, topics 1.5 and 1.6)

## Lessons chosen

- `l9-measuring-spread`: variance and standard deviation of a small distribution, through $E[X^2] - \mu^2$; each family first finds the mean, so expectation (l5) is drilled on the way.

Considered and left out:

- `l5-long-run-average`, `l6-fair-price`: expectation alone is the first step of every family here.
- `l10-scaling-and-adding`: procedural ($\operatorname{Var}(aX + b)$, sums), left within the six-set budget.
- `l1` to `l4`, `l7`, `l8`, `l11` to `l20`: pmfs and CDFs read from a table, linearity and indicators, covariance, joint tables, conditional expectation, Jensen: ideas or multi-step set-ups rather than one technique.

## Sets

One set, 3 families, in `app/content/courses/random-vars/fluency-l9-measuring-spread.json`. Answers are exact decimals (numeric, `tol` 0).

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l9-measuring-spread | two-outcome-variance | 181 | none (numeric) | no-mean, mean-not-squared |
|  | three-value-variance | 179 | none (numeric) | no-mean, mean-not-squared |
|  | standard-deviation | 173 | none (numeric) | gave-variance, no-mean |

Slips are offered only where they are slips: `no-mean` when $\mu \ne 0$, `mean-not-squared` when $\mu$ is neither 0 nor 1, `gave-variance` when the variance is not its own root. The standard-deviation family draws chances 0.5, 0.2, 0.8, 0.1 and 0.9, whose $p(1-p)$ is a perfect square, so every sd is exact. Values of $X$ are written in maths so a negative value shows a true minus.

## Checks

1. `docs/reports/fluency-random-vars-numbers.py` (200 draws a family, shared checker `docs/reports/fluency_check.py`): the variance is worked from its definition $E[(X - \mu)^2]$ over the pmf built from the vars (the set's solutions use the shortcut), and the sd is the exact sympy root. Each `wrong` is recomputed from the vars, must sit outside the key's tolerance plus its own, and must differ from the other slips; the expected slip ids per draw mirror each `when`. The drawn text is scanned for `+-`, `--`, `+ -`, `^{1}`, `+0`, `1x`, `0x` and any `\frac{n}{d}` not in lowest terms. Result: 1,767 checks over 3 families, 0 failures, exit 0. A planted 0.01 on one slip (markov, run once) failed every draw, so the checker bites.
2. From `app/`: validator 0 errors and no warning naming a `fluency-` file; `node tools/test-fluency.mjs --local-cdn <pkgs> --set` green for the set (304 checks).
3. `node tools/playthrough.mjs --fluency <set> --local-cdn <pkgs>`, with and without `--mobile`: green for every set. Screenshots at 440 px looked at for markov and estimation l10 (the widest prompts): no overflow; the matrix sits inline and the set answer's feedback wraps cleanly.
4. `VOICE_BASE=app/content/courses/random-vars/ python3 docs/reviews/voice-scan.py 35`: 0 explanations over three sentences, 0 sentences over 35 words.
5. I read 20 drawn items of every family as a learner would (`fluency-sample.mjs --n 20` a family; moved the drawn values into maths). No `1x`, `+-`, `x^1`, `0x`, double minus or unreduced final fraction, and no prompt that gives the answer away. Working steps keep the lesson's unreduced branch fractions (such as $\tfrac{6}{9} \times \tfrac{5}{8}$) before the reduced result.
6. This report; engine limits in `docs/BACKLOG-INBOX.md` under `Raised later (fluency random-vars):` where there are any.
