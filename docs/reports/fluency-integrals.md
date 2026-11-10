# Fluency sets: integrals (brief `docs/briefs/fluency.md`, agent 6)

Five sets, 17 families, all typed (`expression` with `upToConstant` for antiderivatives, `numeric` for definite integrals and coefficients). Definite integrals are whole numbers or exact fractions ("Give a fraction or a decimal", tolerance 0.0005, `accept` shows the reduced fraction). No family uses `form`: every task is "Find", "Evaluate" or "Work out", and no prompt shows an expression equal to its key.

| Set | Family | Distinct prompts in 200 | `form` | Slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l6-working-backwards | power | 140 | none, `upToConstant` | old-power, no-divide, differentiated |
| | polynomial | 182 | none, `upToConstant` | no-divide, constant-left |
| | negative-power | 90 | none, `upToConstant` | power-lowered, sign-lost |
| | fix-constant (numeric) | 195 | none | no-constant, no-divide |
| fluency-l7-evaluating | power (limits in either order) | 134 | none | limits-swapped, no-divide |
| | quadratic (exact fraction) | 199 | none | limits-swapped, no-divide |
| | reciprocal-square (exact fraction) | 121 | none | sign-lost, power-lowered |
| fluency-l9-undo-chain | power-inside | 186 | none, `upToConstant` | half-missed, no-divide |
| | exp-inside | 142 | none, `upToConstant` | half-missed, multiplied |
| | log-inside | 134 | none, `upToConstant` | half-missed, multiplied |
| | definite-power (change the limits, exact) | 88 | none | limits-kept |
| fluency-l10-undo-product | parts-exp | 124 | none, `upToConstant` | sign-slip, missing-term |
| | parts-cos | 101 | none, `upToConstant` | sign-slip, missing-term |
| | parts-sin | 94 | none, `upToConstant` | sign-slip, missing-term |
| | parts-log | 83 | none, `upToConstant` | sign-slip, second-divide |
| fluency-l14-splitting-fractions | cover-up (numeric $A$) | 196 | none | other-factor, no-divide |
| | split-integrate ($A\ln\lvert x-a\rvert + B\ln\lvert x-b\rvert$) | 195 | none, `upToConstant` | swapped, sign-flip |

Rejected draws stay under 54% for every family (definite-power the highest, 230 of 430).

## Checks

1. `docs/reports/fluency-integrals-numbers.py` (sympy, 200 draws per family, from the vars only): 22,400 checks, 0 failures, exit 0. Antiderivative keys differ from sympy's by a constant at five points; every `wrong` does not, and no two wrongs coincide. Numeric keys equal sympy's exact value; each wrong value is recomputed and lies outside tolerance. For cover-up the prompt's numerator is read back and split with `apart`.
2. Validator 0 errors; no warning names an integrals fluency file. `node tools/test-fluency.mjs --local-cdn <pkgs>`: 338/338 passed, no coinciding-wrong notes on these sets.
3. Playthrough `--fluency` of all five sets, with and without `--mobile`: green. The 440 px screenshots were read; inline fractions were too small, so the prompts with a fraction now use `\displaystyle`.
4. Voice scan 35 on the course folder: 0 and 0.
5. I read 20 drawn items of every family (and scanned 200 draws of every text for `1x`, `0x`, `x^1`, `+-`, double minus, `\frac{n}{1}` and unreduced fractions): none found, and no prompt gives its answer away.

## Families skipped and limits

- Definite integrals to stated decimals (l9 with $e^{x^2}$, l10 by parts, l14 between limits, l7 with $e^{kx}$): `let` has no `ln`, `exp`, `sin`, `cos` or `pi`. Raised in the inbox.
- No coefficient-fraction format, so draws whose coefficient is 1 are excluded ($\int xe^x\,dx$, $\int x\cos x\,dx$, $\int 2x(x^2+b)^n\,dx$, $\int \frac{2x}{x^2+b}\,dx$). Raised.
- No monomial with a var power, so l7 power, l9 definite-power and l10 parts-log start at power 2. Raised.
- l6 holds four families; the brief caps a set at four, so the single-power family covers whole and fraction coefficients together.

## Widening pass

Formats used: `cfrac` and `+cfrac` (coefficient 1 writes nothing), `mono` (power 1), `exp` and `ln` in `let`, `when` on a `wrong`, and a pick of tuples for a bracket's exponent.

| Set | Family | Distinct prompts in 200 | `form` | Slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l7-evaluating | power (now $\int_p^q cx\,dx$ too) | 149 | none | limits-swapped, no-divide |
| | exponential (new: $\int_0^q ce^{kx}\,dx$ to 3 dp, as the lesson's quiz) | 137 | none | lower-limit-zero, no-divide (`when` $k \ne \pm 1$), sign-lost (`when` $k < 0$) |
| fluency-l9-undo-chain | power-inside (coefficient 1 allowed: $\int 2x(x^2+b)^n\,dx$) | 191 | none, `upToConstant` | half-missed, no-divide |
| | exp-inside ($\int 2xe^{x^2}\,dx$ now drawn) | 149 | none, `upToConstant` | half-missed, multiplied |
| | log-inside ($\int \frac{2x}{x^2+b}\,dx$ now drawn) | 128 | none, `upToConstant` | half-missed, multiplied |
| | definite-power (now from $(x^2+b)^1$) | 127 | none | limits-kept |
| fluency-l10-undo-product | parts-exp ($\int xe^x\,dx$ now drawn) | 137 | none, `upToConstant` | sign-slip, missing-term |
| | parts-cos ($\int x\cos x\,dx$ now drawn) | 113 | none, `upToConstant` | sign-slip, missing-term |
| | parts-sin (coefficient 1 now drawn) | 106 | none, `upToConstant` | sign-slip, missing-term |
| | parts-log (now from $\int ax\ln x\,dx$, the lesson's example) | 108 | none, `upToConstant` | sign-slip, second-divide |
| fluency-l14-splitting-fractions | cover-up (draws no longer narrowed; slips use `when`) | 199 | none | other-factor (`when` $B \ne A$), no-divide (`when` it differs from $A$ and $B$) |
| | split-between-limits (new: between limits to 4 dp, as the lesson's quiz) | 194 | none | swapped (`when` it differs from $\pm$ the key), sign-flip |

Entries still blocked: the decimal definite integrals by substitution (l9) and by parts (l10). The functions now exist, but both sets already hold four families, the brief's cap; raised in the inbox as a brief decision, not an engine item.

Checks: (1) `fluency-integrals-numbers.py`, extended with the exponential and split-between-limits families (sympy integrates exactly; the prompt's numerator is read back and split with `apart`) and an offered-set check for every `when`: 27,025 checks, 0 failures, exit 0. (2) Validator 0 errors, no warning on a fluency file; `test-fluency.mjs --local-cdn` 308/308, 305/305, 304/304, 303/303, no coinciding-wrong notes. (3) Playthrough `--fluency` of the four sets, with and without `--mobile`: green; 440 px screenshots read, no overflow. (4) Voice scan 35: 0 and 0. (5) I read 20 draws of every changed family and scanned 200 for `1x`, `0x`, `x^1`, `+-`, double minus and unreduced fractions; the scan caught `-1e^{x}` from a missed `+frac`, now `+cfrac`, and is clean.
