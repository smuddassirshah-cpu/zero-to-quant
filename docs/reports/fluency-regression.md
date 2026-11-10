# Fluency sets: regression (brief `docs/briefs/fluency.md`, second wave, agent 3, topics 1.5 and 1.6)

## Lessons chosen

- `l2-slope-formula`: $b = S_{xy}/S_{xx}$, $a = \bar y - b\bar x$, and $b = r\,s_y/s_x$ (beta and hedge ratio).

Considered and left out:

- `l3-how-much-explained` ($R^2$), `l5-how-sure` and `l6-is-slope-zero` (slope SE and $t$): procedural, left within the five-set budget for topic 1.6.
- `l1`, `l4`, `l7` to `l12`: reading plots, residuals, summary tables, collinearity and failed assumptions: judgements.

## Sets

One set, 3 families, in `app/content/courses/regression/fluency-l2-slope-formula.json`. Slopes from sums and intercepts are exact decimals (`tol` 0); the slope from $r$ is asked to 3 decimal places.

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l2-slope-formula | slope-from-sums | 199 | none (numeric) | upside-down, x-on-y |
|  | intercept | 200 | none (numeric) | added, means-swapped |
|  | slope-from-r | 191 | none (numeric) | sds-upside-down, forgot-r |

`slope-from-sums` draws $S_{xx}$ from divisors of a power of ten, so the key terminates, and requires $S_{xy}^2 < S_{xx}S_{yy}$ so the sums could come from real data. The numbers script found a draw where the two intercept slips coincided; `means-swapped` now carries `when` to skip it.

## Checks

1. `docs/reports/fluency-regression-numbers.py` (200 draws a family, shared checker `docs/reports/fluency_check.py`): the slope minimises $S(b) = S_{yy} - 2bS_{xy} + b^2S_{xx}$ with sympy (the $x$-on-$y$ slip swaps the squared sums), the intercept solves $\bar y = a + b\bar x$, and the $r$ slope is $\operatorname{Cov}/\operatorname{Var}$ with $\operatorname{Cov} = r\,s_xs_y$. Each `wrong` is recomputed from the vars, must sit outside the key's tolerance plus its own, and must differ from the other slips; the expected slip ids per draw mirror each `when`. The drawn text is scanned for `+-`, `--`, `+ -`, `^{1}`, `+0`, `1x`, `0x` and any `\frac{n}{d}` not in lowest terms. Result: 1,798 checks over 3 families, 0 failures, exit 0. A planted 0.01 on one slip (markov, run once) failed every draw, so the checker bites.
2. From `app/`: validator 0 errors and no warning naming a `fluency-` file; `node tools/test-fluency.mjs --local-cdn <pkgs> --set` green for the set (304 checks).
3. `node tools/playthrough.mjs --fluency <set> --local-cdn <pkgs>`, with and without `--mobile`: green for every set. Screenshots at 440 px looked at for markov and estimation l10 (the widest prompts): no overflow; the matrix sits inline and the set answer's feedback wraps cleanly.
4. `VOICE_BASE=app/content/courses/regression/ python3 docs/reviews/voice-scan.py 35`: 0 explanations over three sentences, 0 sentences over 35 words.
5. I read 20 drawn items of every family as a learner would (`fluency-sample.mjs --n 20` a family; nothing to fix beyond the coinciding slips). No `1x`, `+-`, `x^1`, `0x`, double minus or unreduced final fraction, and no prompt that gives the answer away. Working steps keep the lesson's unreduced branch fractions (such as $\tfrac{6}{9} \times \tfrac{5}{8}$) before the reduced result.
6. This report; engine limits in `docs/BACKLOG-INBOX.md` under `Raised later (fluency regression):` where there are any.
