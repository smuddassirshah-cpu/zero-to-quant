# Fluency: exp-log (brief `docs/briefs/fluency.md`, agent 3)

Four sets, 16 families. Each set uses its lesson's notation and wording: $a^{-n}$ and $a^{m/n}$ as "Work out", $p = \log_b x$ and $q = \log_b y$ as in l6, "take $\log$ of both sides" with base-10 `log` as in l8, and $\ln$ with $e^{kt}$ as in l10. No set uses an idea from a later lesson.

| Set | Family | Distinct prompts in 200 | `form` | Slips (`wrong` ids) |
| --- | --- | --- | --- | --- |
| fluency-l3-strange-powers | negative-power (numeric) | 65 | none | dropped-minus, times-the-power |
| | fractional-power (numeric) | 68 | none | times-the-power, flipped |
| | laws-then-evaluate (numeric; zero and negative results) | 187 | none | added-the-bottom, multiplied-the-top |
| | power-of-a-power (numeric $k$) | 192 | none | added-the-powers, sign-of-divide |
| fluency-l6-products-into-sums | split-a-product (in $p$, $q$) | 91 | none (prompt has no $p$ or $q$) | powers-left-behind, multiplied-the-logs |
| | split-a-quotient (in $p$, $q$) | 118 | none | added-for-divide, divided-the-logs |
| | combine-a-sum (numeric) | 62 | none | log-of-the-sum, multiplied-the-logs |
| | combine-a-difference (numeric) | 82 | none | divided-the-logs, subtracted-inside |
| fluency-l8-solving-for-the-power | exact-power ($\frac{\log b}{\log a}$) | 195 | none (prompt is an equation) | upside-down, divided-the-numbers |
| | power-to-3-sf (numeric) | 193 | none | upside-down, divided-the-numbers |
| | power-alone-first (numeric) | 149 | none | stopped-early, joined-the-base |
| | money-target (numeric, 3 sf) | 164 | none | joined-the-base, logs-too-soon |
| fluency-l10-natural-log | exact-with-ln ($\frac{\ln b}{k}$) | 168 | none | multiplied-by-k, divided-inside |
| | continuous-growth (numeric, 2 dp) | 143 | none | logs-too-soon, rate-as-whole-number |
| | ln-from-two-values (numeric, 4 dp) | 95 | none | powers-left-behind, swapped-the-values |
| | any-base-as-e (numeric, 4 dp) | 101 | none | used-log, one-over |

"Combine" is asked as a value ("Work out $\log_6 4 + \log_6 9$"), not as "write as a single log": a single-log key is a constant, graded by value, so the prompt typed back would score.

## Logs in `let`

The evaluator has no `ln`. Each log is computed as `50000*(y^(1/100000) - y^(-1/100000))`, which is $10^5 \sinh(\ln y / 10^5)$, so $\ln y$ to about $10^{-11}$. Keys are then rounded to 6 dp (`round(r, 6)`). The number script checks every such key against sympy's own `log` to $10^{-6}$. Raised as an engine item.

## Checks

1. `docs/reports/fluency-exp-log-numbers.py` (sympy venv), 200 draws of every family. It rebuilds each key from the vars alone: exact powers, `expand_log` in $p$ and $q$, `sympy.solve` for $a^x = b$, $c a^x = d$ and $Pe^{kt} = T$, and sympy `log`. It checks each `wrong` is the named slip and lies outside the key's tolerance, each 3 sf `accept` string, and that the true $\ln$ lies inside the ln-from-two-values tolerance. Result: 18,800 of 18,800 checks pass, exit 0.
2. Validator: 0 errors, no warning on these files. `test-fluency.mjs --local-cdn` per set: 278, 276, 277 and 277 of each, all pass.
3. Playthrough `--fluency` for all 4 sets, with and without `--mobile`: all green. Screenshots of l6 (wrong answer) and l10 at 440 px looked right, with no overflow.
4. Voice scan 35 on exp-log: 0 and 0.
5. I read 20 draws of every family as a learner would (320 items), with a pattern scan for `1x`, `+-`, `x^1`, `0x`, double minus, unreduced fractions and float artefacts. I fixed what I found: $\left(t^{-1}\right)^{-1} = t^{1}$ in a wrong line (now `m*n != 1`), and two steps of the fractional-power working that read badly for a power of $1/n$. No prompt gives the answer away.

## Found while testing

- An `accept` entry in plain text with a function name, such as `ln(97)/ln(4)`, is read as the letters $l \cdot n$, so it equals $\frac{97}{4}$ and made the wrong `\frac{97}{4}` grade correct. The accept list now holds LaTeX forms only (`\frac{\ln b}{\ln a}`, `\log_{a} b`). Raised.
- There is no significant-figures format. The 3 sf families keep the answer between 1 and 10 (`dp2`) or between 10 and 100 (`dp1`) with `where`. Raised.

Nothing was skipped.

## Widening pass

Entries worked: every `ln` work-round in `let` now uses the evaluator's `ln`, and the two 3 sf families use the `sf3` format instead of a `where` that held the answer in one decade.

| Set | Family | Distinct prompts in 200 | `form` | Slips (`wrong` ids) |
| --- | --- | --- | --- | --- |
| fluency-l6-products-into-sums | combine-a-sum, combine-a-difference (changed `let`) | 62, 82 | none | as before |
| fluency-l8-solving-for-the-power | exact-power, power-alone-first (changed `let`) | 195, 149 | none | as before |
| | power-to-3-sf (widened: `sf3`, answers 0.56 to 13.1) | 192 | none | upside-down, divided-the-numbers |
| | money-target (widened: `sf3`, answers 5.27 to 70.0) | 170 | none | joined-the-base, logs-too-soon |
| fluency-l10-natural-log | all four (changed `let`) | 168, 143, 95, 101 | none | as before |

Each `50000*(y^(1/100000) - y^(-1/100000))` became `ln(y)`. I drew 200 items of every exp-log set on seed 1 before the change and after it (before the `sf3` widening): the same vars, prompts, solutions and wrong values in all 800, and keys equal to within 1e-8, so every drawn answer is unchanged at its stated precision. The widened families set `"accept": "{r:sf3}"`, state `{r:sf3}` in the solution, and take a tolerance of 0.51 of a unit in the third figure as a template (`"abs": "{0.51*10^e}"` with `e = floor(log10(r)) - 2`), for the key and each slip. A `where` keeps $r$ off an exact 3 sf value, and the upside-down slip off the key near $r = 1$. Rejected draws fell from 41 to 9 (power-to-3-sf) and from 34 to 6 (money-target) per 200 kept.

Checks: (1) `fluency-exp-log-numbers.py`: a new `sf3` check works the 3 sf text with Python `Decimal` at 40 digits from sympy's `log`, and checks the tolerance and the figure the solution states; 20,000 of 20,000 checks, exit 0. (2) Validator 0 errors, no warning on exp-log fluency files; `test-fluency.mjs --local-cdn`: l6 306, l8 307, l10 307, all pass. (3) Playthrough `--fluency` of l6, l8 and l10 with and without `--mobile`: green. (4) `voice-scan.py 35` on exp-log: 0 and 0. (5) I read 20 draws each of power-to-3-sf and money-target as a learner would (for example $n = \frac{\log 2}{\log 1.08} = 9.01$ and $t = \frac{\log 4}{\log 1.02} = 70.0$): no float artefacts, `+-` or double minus, and no prompt gives the answer away. (6) This section.

Still blocked: nothing in this course.
