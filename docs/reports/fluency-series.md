# Fluency sets: series (brief `docs/briefs/fluency.md`, agent 4)

Six sets, 19 families, in `app/content/courses/series/fluency-*.json`. Every family is a typed answer. Only the two "Write $u_n$" families are expressions; neither needs `form`, because the prompt shows terms, not an expression equal to the key. `geometric-formula` sets `integers: ["n"]` so a negative ratio such as $(-2)^{n-1}$ is compared at whole $n$.

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l2-any-term | term-from-list | 199 | none (numeric) | k-steps, difference-sign |
| | nth-term-formula | 159 | none | n-steps, first-term-times-n |
| | difference-from-two-terms | 200 | none (numeric) | whole-rise, counted-terms |
| | which-term | 200 | none (numeric) | steps-not-position, one-too-many |
| fluency-l3-multiplying-each-time | geometric-term | 135 | none (numeric) | k-factors, added-the-step |
| | common-ratio | 155 | none (numeric) | upside-down, difference |
| | geometric-formula | 97 | none | n-factors, ratio-and-first-swapped, arithmetic-rule |
| fluency-l6-gauss | one-to-n | 129 | none (numeric) | not-halved, one-term-short |
| | first-n-terms | 195 | none (numeric) | not-halved, k-steps |
| | up-to-last-term | 194 | none (numeric) | counted-steps, not-halved |
| fluency-l7-shifted-copy | first-n-terms | 143 | none (numeric) | one-term-short, sign-flipped |
| | up-to-last-term | 71 | none (numeric) | counted-steps, sign-flipped |
| | sigma-powers | 68 | none (numeric) | stopped-early, one-term-extra |
| fluency-l8-adding-forever | from-the-terms | 81 | none (numeric) | sign-of-r, first-term-left-out |
| | from-a-and-r | 169 | none (numeric) | sign-of-r, first-term-left-out |
| | perpetual-bond | 63 | none (numeric, £) | payment-today, per-cent-not-decimal |
| fluency-l11-powers-of-a-bracket | x-plus-b | 101 | none (numeric) | count-only, power-swapped |
| | ax-plus-b | 140 | none (numeric) | a-not-raised, a-left-out |
| | term-with-no-x | 105 | none (numeric) | count-only, powers-only |

Notation and wording follow each lesson: $u_n$, $a$, $d$, $r$, "Write $u_n$ for ...", "Which term ... equals ...?" (l2, l3), $S_n$ and "Find the sum of the first $n$ terms" (l6, l7), $\sum_{k=b}^{t}$ as in the l7 quiz, $S_\infty$, "Give a fraction or a decimal" and the perpetual bond with "a payment in $k$ years is worth ..." (l8), "the number in front of $x^k$" and "the term with no $x$" (l11). Geometric terms with ratio $\frac12$ use a first term that is a multiple of $2^{n-1}$, so every term shown is whole. Sums are capped at 3,000 and coefficients at 3,000.

## Choices and skipped families

- Series that end on a negative term are left out of the "up to the last term" families (l6 needs $l > 0$; l7 uses ratios 2, 3, 4 and $\frac12$ from a positive start), because `+ \dots -92` reads badly and no format chooses the sign of the dots per draw. Negative and alternating series stay in the "first $n$ terms" families, whose prompts end in `+ \dots`.
- Skipped: l8 "write a recurring decimal as a fraction" (the lesson's $0.333\ldots$ item): no answer type refuses the decimal. Raised in `docs/BACKLOG-INBOX.md`.

## Checks

1. `docs/reports/fluency-series-numbers.py` (sympy, 200 draws per family): it sums each series with `summation` (arithmetic and geometric, finite and to infinity), lists terms step by step for $u_k$, solves $u_n = $ value for the position, and expands each bracket with `Poly` to read the coefficient. Each `wrong` is recomputed from the vars and must differ from the key; no two wrongs may coincide; drawn text is scanned for `1x`, `+-`, `--`, `x^{1}`, `+0`, `0x`. Result: 11,600 checks over 19 families, 0 failures, exit 0. A planted +1 on one key was caught (20 of 20 draws).
2. Validator: 0 errors, no warning on any series `fluency-*` file. `test-fluency.mjs --local-cdn` green for all six sets (273 to 277 checks each, no notes).
3. Playthrough `--fluency` for every set, with and without `--mobile`: green. I looked at the 440 px screenshots (item, wrong-answer sheet, end card): no layout faults.
4. `voice-scan.py 35` on `app/content/courses/series`: 0 and 0.
5. I read 20 drawn items of every family as a learner would. The scan found `+0` terms ("$1+0-1+\dots$") and `+ \dots -28` endings, both removed with `where`; a line opening with a numeral and the sigma solution's unexplained $-128$ were reworded. No prompt gives the answer away.
6. Slips that could equal the key or each other are kept apart by `where` (l2 `a != d`, l8 three gaps of 0.02 with wrong `tol` 0.005).
