# Fluency sets: limits-thm (brief `docs/briefs/fluency.md`, second wave, agent 3, topics 1.5 and 1.6)

## Lessons chosen

- `l1-counting-successes`: $\binom{n}{k}p^k(1-p)^{n-k}$ and $np(1-p)$ with fresh $n$, $k$ and $p$.
- `l7-bell-curve`: standardising and reading $\Phi$ with symmetry, the step every later normal calculation uses. Each prompt states $\Phi$ at the needed $z$, as the brief asks.

Considered and left out:

- `l2-first-success`, `l4-without-replacement`, `l13-approximating-binomial`: procedural, left within the six-set budget (l13 would reuse the l7 families with a continuity correction).
- `l3-rare-events`, `l6-uniform-exponential`, `l8-lognormal`: need $e^{-\lambda}$ or a log, so a calculator the lessons do not assume.
- `l5`, `l9` to `l12`, `l14` to `l19`: ideas (area, laws of large numbers, bounds, the CLT) or derivations.

## Sets

Two sets, 6 families, in `app/content/courses/limits-thm/fluency-l1-counting-successes.json` and `fluency-l7-bell-curve.json`. The lessons work in decimals: binomial chances to 4 decimal places (`tol` 0.00005; the exact value also passes), the binomial variance exactly, and normal chances from the table value the prompt gives.

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l1-counting-successes | exactly-k | 127 | none (numeric) | one-path, swapped (each only when 0.0002 clear of the key) |
|  | binomial-variance | 158 | none (numeric) | gave-mean, one-trial |
|  | none-succeed | 76 | none (numeric) | used-p, complement-of-all |
| fluency-l7-bell-curve | standardise | 190 | none (numeric) | divided-by-variance, sign-flipped |
|  | normal-probability | 199 | none (numeric) | other-tail, gave-z |
|  | within-band | 191 | none (numeric) | one-cut, half-band |

`exactly-k` draws $2 \le k \le n - 2$ so no power of 1 appears in the working, and keeps the key at least 0.001. `normal-probability` writes the variance as a number, $N(12, 9)$, as the lesson's trap does; `standardise` and `within-band` write it as $5^2$. The ten table values (0.4 to 3) are the standard four-figure ones.

## Checks

1. `docs/reports/fluency-limits-thm-numbers.py` (200 draws a family, shared checker `docs/reports/fluency_check.py`): binomial chances are summed over all $2^n$ enumerated win-loss paths; every table value is checked against $\Phi$ from `math.erf` to 0.00005, and each normal key is rebuilt from the event (standardise, then $\Phi(z)$ or $1 - \Phi(z)$ by symmetry) and checked against erf too. Each `wrong` is recomputed from the vars, must sit outside the key's tolerance plus its own, and must differ from the other slips; the expected slip ids per draw mirror each `when`. The drawn text is scanned for `+-`, `--`, `+ -`, `^{1}`, `+0`, `1x`, `0x` and any `\frac{n}{d}` not in lowest terms. Result: 3,537 checks over 6 families, 0 failures, exit 0. A planted 0.01 on one slip (markov, run once) failed every draw, so the checker bites.
2. From `app/`: validator 0 errors and no warning naming a `fluency-` file; `node tools/test-fluency.mjs --local-cdn <pkgs> --set` green for both sets (304 checks each).
3. `node tools/playthrough.mjs --fluency <set> --local-cdn <pkgs>`, with and without `--mobile`: green for every set. Screenshots at 440 px looked at for markov and estimation l10 (the widest prompts): no overflow; the matrix sits inline and the set answer's feedback wraps cleanly.
4. `VOICE_BASE=app/content/courses/limits-thm/ python3 docs/reviews/voice-scan.py 35`: 0 explanations over three sentences, 0 sentences over 35 words.
5. I read 20 drawn items of every family as a learner would (`fluency-sample.mjs --n 20` a family; loans now repay rather than default with chance 0.9, "1 sds" became "1 sd", and `none-succeed` keeps the key at least 0.001). No `1x`, `+-`, `x^1`, `0x`, double minus or unreduced final fraction, and no prompt that gives the answer away. Working steps keep the lesson's unreduced branch fractions (such as $\tfrac{6}{9} \times \tfrac{5}{8}$) before the reduced result.
6. This report; engine limits in `docs/BACKLOG-INBOX.md` under `Raised later (fluency limits-thm):` where there are any.
