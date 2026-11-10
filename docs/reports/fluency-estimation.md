# Fluency sets: estimation (brief `docs/briefs/fluency.md`, second wave, agent 3, topics 1.5 and 1.6)

## Lessons chosen

- `l9-how-precise`: $s/\sqrt n$, $\sqrt{\hat p(1 - \hat p)/n}$, and the $1/\sqrt n$ rule for the data needed.
- `l10-catching-the-truth`: $\bar x \pm z\,\mathrm{SE}$ with the lesson's multipliers 1.645, 1.96 and 2.576. The interval is typed as a set answer, both ends in any order.

Considered and left out:

- `l5` to `l8`: likelihood and MLE derivations, whose answers are formulas and whose numbers need logs.
- `l1` to `l4`: sampling, bias and variance as ideas.
- `l11-bootstrap`, `l12-updating-a-belief`: simulation, and a Bayesian update the conditional set already drills.

## Sets

Two sets, 5 families, in `app/content/courses/estimation/fluency-l9-how-precise.json` and `fluency-l10-catching-the-truth.json`. Sample sizes are squares whose roots have only the factors 2 and 5 (or tuples that make the root exact), so standard errors are exact decimals; interval ends and half-widths are asked to 3 decimal places (`tol` 0.0005) because the multipliers carry three or four figures.

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l9-how-precise | se-of-mean | 103 | none (numeric) | divided-by-n, gave-sd |
|  | se-of-proportion | 92 | none (numeric) | no-root, root-over-n |
|  | data-needed | 86 | none (numeric) | linear, extra-only |
| fluency-l10-catching-the-truth | interval-from-se | 191 | none (numeric) | no-multiplier, used-1-96 (only when the level is not 95%) |
|  | half-width-from-s | 109 | none (numeric) | no-root-n, divided-by-n |

`se-of-proportion` keeps $\hat p n$ whole (`where`), so 36% of 25 trades is 9 trades. A slip of the set family is the whole wrong interval, as AUTHORING 16 asks.

## Checks

1. `docs/reports/fluency-estimation-numbers.py` (200 draws a family, shared checker `docs/reports/fluency_check.py`): roots are taken by sympy from $n$ itself and each tuple root is asserted equal to it; the multipliers are checked against `statistics.NormalDist().inv_cdf` to 0.0005; the data-needed key solves $\mathrm{SE}(n_2) = \mathrm{SE}(n)/k$ for $n_2$ with sympy. Each `wrong` is recomputed from the vars, must sit outside the key's tolerance plus its own, and must differ from the other slips; the expected slip ids per draw mirror each `when`. The drawn text is scanned for `+-`, `--`, `+ -`, `^{1}`, `+0`, `1x`, `0x` and any `\frac{n}{d}` not in lowest terms. Result: 2,935 checks over 5 families, 0 failures, exit 0. A planted 0.01 on one slip (markov, run once) failed every draw, so the checker bites.
2. From `app/`: validator 0 errors and no warning naming a `fluency-` file; `node tools/test-fluency.mjs --local-cdn <pkgs> --set` green for both sets (304 and 301 checks).
3. `node tools/playthrough.mjs --fluency <set> --local-cdn <pkgs>`, with and without `--mobile`: green for every set. Screenshots at 440 px looked at for markov and estimation l10 (the widest prompts): no overflow; the matrix sits inline and the set answer's feedback wraps cleanly.
4. `VOICE_BASE=app/content/courses/estimation/ python3 docs/reviews/voice-scan.py 35`: 0 explanations over three sentences, 0 sentences over 35 words.
5. I read 20 drawn items of every family as a learner would (`fluency-sample.mjs --n 20` a family; reworded "hit rate" to "that share" so the fill-rate context reads right, and kept the counts whole). No `1x`, `+-`, `x^1`, `0x`, double minus or unreduced final fraction, and no prompt that gives the answer away. Working steps keep the lesson's unreduced branch fractions (such as $\tfrac{6}{9} \times \tfrac{5}{8}$) before the reduced result.
6. This report; engine limits in `docs/BACKLOG-INBOX.md` under `Raised later (fluency estimation):` where there are any.
