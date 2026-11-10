# Fluency sets: limits (brief `docs/briefs/fluency.md`, agent 5)

Seven sets, 23 families, in `app/content/courses/limits/fluency-*.json`. Every family is a typed answer. No family uses `form`: each task is "find a limit", "differentiate" or "find a value", so retyping the prompt never equals the key (AUTHORING 16, "Choosing `form`"). Derivative keys are left to the grader's equivalence, so $-6x^{-4}$, $-\frac{6}{x^4}$ and $\frac{-6}{x^4}$ all pass.

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l2-computing-limits | cancel-linear-bottom | 118 | none (numeric) | zero-over-zero-is-zero, zero-over-zero-is-one, sign-of-factor |
| | cancel-two-quadratics | 187 | none (numeric) | upside-down, zero-over-zero-is-one |
| | difference-quotient | 76 | none (numeric) | square-split, factor-dropped |
| fluency-l7-power-rule | polynomial | 200 | none | power-not-lowered, constant-kept |
| | negative-power | 83 | none | bottom-differentiated, power-raised |
| | fractional-power | 115 | none | power-raised, power-not-brought-down |
| | slope-at-a-point | 200 | none (numeric) | value-not-slope, power-not-lowered |
| fluency-l9-products-quotients | product-rule | 172 | none | product-of-derivatives, one-term-only |
| | quotient-rule | 198 | none | sign-reversed, not-squared |
| | product-at-a-point | 199 | none (numeric) | product-of-derivatives, one-term-only |
| fluency-l10-inside-function | linear-inside | 182 | none | inside-forgotten, power-not-lowered |
| | square-inside | 173 | none | inside-forgotten, x-dropped |
| | root-inside | 73 | none | inside-forgotten, half-dropped |
| fluency-l11-standard-derivatives | exponential-chain | 161 | none | inside-forgotten, power-rule-used |
| | log-chain | 152 | none | inside-forgotten, one-over-x |
| | sine-chain | 116 | none | inside-forgotten, sign-flipped |
| | cosine-chain | 117 | none | sign-lost, inside-forgotten |
| fluency-l12-implicit | ellipse | 192 | none (numeric) | sign-lost, upside-down |
| | extra-y-term | 181 | none (numeric) | y-term-missed, y-term-dropped |
| | product-term | 138 | none (numeric) | xy-as-y-only, xy-as-xy-prime-only |
| fluency-l13-peaks-and-troughs | local-maximum | 188 | none (numeric) | trough-given, sign-slip |
| | local-minimum | 186 | none (numeric) | peak-given, sign-slip |
| | minimum-value | 146 | none (numeric) | x-not-value, peak-value |

Each set keeps to its lesson's notation and wording: $\lim_{x \to a}$ and "Find" (l2), "Differentiate $f(x) = \dots$" and "$f'(k)$" (l7), "Use the product rule / quotient rule" (l9), "Find $\dfrac{dy}{dx}$ when $y = \dots$" (l10, l11, which also uses $t$), "The point $(p, q)$ lies on ... What is $y'$ there? Give a fraction or a decimal." (l12, as in its quiz), "At which $x$ does $f$ have a local maximum?" (l13, as in its quiz). The l12 `product-term` family uses the product rule on $kxy$, which the lesson's derivation and quiz ($xy = 12$) use; $k = \pm 2$ is excluded because those curves are pairs of lines.

## Skipped

- l13 `closed-interval-maximum` (the lesson's trap screen): its real slips equal the key in some draws, and the framework has no choice function nor per-draw switch for a `wrong`. Raised in `docs/BACKLOG-INBOX.md`.
- l9 and l10 draw powers from 3 up, because a power of 2 would print `x^{1}` (no format drops an exponent of 1). Raised.

## Checks

1. `docs/reports/fluency-limits-numbers.py` (sympy, 200 draws per family): it rebuilds each limit with `sympy.limit`, each derivative with `diff`, each implicit slope with `idiff` (after checking the point is on the curve), and each stationary point by solving $f' = 0$ and classifying with $f''$. It checks every `wrong` equals the slip recomputed from the vars and differs from the key (numeric: outside the key's tolerance). Result: 14,000 checks over 23 families, 0 failures, exit 0. A planted error (+1 on one key) was caught.
2. Validator: 0 errors; no warning on any `fluency-*` file (4,103 warnings in all, the same as before the sets apart from the one fixed during authoring). `test-fluency.mjs --local-cdn` green for all seven sets (271 to 275 checks each).
3. Playthrough `--fluency` for every set, with and without `--mobile`: green (see the hand-back).
4. `voice-scan.py 35` on `app/content/courses/limits`: 0 explanations over three sentences, 0 sentences over 35 words.
5. I read 20 drawn items of every family as a learner would, and ran a pattern scan over each drawn prompt, solution, key and `wrong` line for `1x`, `+-`, `x^1`, `0x`, a double minus, `+0` and `-0`. It found `1x^{-3}` in the negative-power solution, now fixed, and nothing else (`u^{1/2}` is a false hit). No prompt gives the answer away. Answers show as reduced fractions (`frac`).
6. Wrong answers that could coincide with each other are kept apart by `where` (l7 slope-at-a-point, l13 minimum-value: test-fluency flagged that one coincidence).

## Widening pass

Formats used: `mono` (power 1 prints no exponent), `when` on a `wrong`, `if`, `max` and `min` in `let`, and a pick of tuples that carries a bracket's exponent text.

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l9-products-quotients | product-rule (now $n \ge 2$, so $x^2(ax+b)$ is drawn) | 176 | none | product-of-derivatives, one-term-only |
| fluency-l10-inside-function | linear-inside (now power 2 and inside $x + b$) | 192 | none | inside-forgotten (`when` $a \ne 1$), power-not-lowered |
| | square-inside (now power 2) | 178 | none | inside-forgotten, x-dropped |
| fluency-l13-peaks-and-troughs | closed-interval-maximum (new, the lesson's trap screen) | 192 | none (numeric) | local-max (`when` it is not also the largest), x-not-value (`when` the $x$ differs from the value), smallest |

The closed-interval family draws a cubic with both stationary points inside $[\text{lo}, \text{hi}]$; the largest value falls at the local maximum, at an end, or at both, so the learner must compare all four values. Unchanged families draw as before.

Entries still blocked: none. One limit raised again: a bracket to a drawn power needs the exponent text in a tuple (inbox, `Raised later (fluency limits integrals multivar, widening pass)`).

Checks: (1) `fluency-limits-numbers.py`, extended with `l13_closed` (sympy solves $f' = 0$ and compares the ends) and an offered-set check for every `when`: 14,655 checks over 24 families, 0 failures, exit 0. (2) Validator 0 errors, no warning on a fluency file; `test-fluency.mjs --local-cdn` 302/302, 301/301, 308/308, no coinciding-wrong notes. (3) Playthrough `--fluency` of the three sets, with and without `--mobile`: green; 440 px screenshots read, no overflow. (4) Voice scan 35 on the course: 0 and 0. (5) I read 20 draws of every changed family and scanned 200 for `1x`, `0x`, `x^1`, `+-`, double minus, `+0`, `-0`, `\frac{n}{1}` and unreduced fractions: none.
