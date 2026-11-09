# Fluency sets: counting (brief `docs/briefs/fluency.md`, agent 4)

Two sets, 7 families, in `app/content/courses/counting/fluency-*.json`. Every family is a `numeric` whole-number answer with `tol` 0, so no `form` is needed.

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l3-choosing-in-order | evaluate-p | 69 | none (numeric) | repeats-allowed, one-factor-short |
| | awards | 78 | none (numeric) | repeats-allowed, times-places |
| | factorial-quotient | 71 | none (numeric) | subtracted, divided-the-numbers |
| fluency-l4-choosing-without-order | pairs | 133 | none (numeric) | order-counted, n-plus-one |
| | evaluate-binomial | 64 | none (numeric) | not-divided, divided-by-s |
| | committee | 158 | none (numeric) | order-counted, divided-by-r |
| | up-down-patterns | 119 | none (numeric) | all-patterns, order-counted |

Wording follows the lessons: $P(n, r)$, "nobody can win twice", $\dfrac{n!}{m!}$ (l3); $\binom{n}{r}$, "Both go as equals", "All ... have equal votes", the up-down pattern quiz item, and the symmetry $\binom{n}{r} = \binom{n}{n-r}$ (l4). The l3 set uses no idea from l4: its slips are repeats allowed, one factor short and the factorial misread, never "divide by $r!$". Counts are capped at 10,000 ($P(n, r)$), 5,040 (factorial quotients) and 3,003 (choices), so no draw needs a calculator; the widest ranges are two factors, up to $50 \times 49$ and $60 \times 59$.

## Choices and skipped families

- `evaluate-binomial` draws the smaller bottom number $s$ from 3 to 6 and shows $\binom{n}{s}$ or $\binom{n}{n-s}$. At $s = 2$ the real slip "divided by $r$, not $r!$" equals the key, and a `wrong` cannot be switched off per draw (already raised). $\binom{n}{2}$ is drilled by the `pairs` family instead, and by `up-down-patterns`.
- No family skipped. The solutions write $\frac{n!}{(n-r)!}$ rather than the lesson's "$7 \times 6 \times 5$", because no format writes a drawn number of factors. Raised in `docs/BACKLOG-INBOX.md`.

## Checks

1. `docs/reports/fluency-counting-numbers.py` (200 draws per family): it counts by brute-force enumeration with `itertools.permutations`, `combinations` and `product('UD', repeat=n)` whenever the count is at most 20,000, and by sympy `ff` and `binomial` above that. Each `wrong` is recomputed from the vars and must differ from the key and from the other wrong; drawn text is scanned for `1x`, `+-`, `--`, `x^{1}`, `+0`, `0x`. Result: 4,200 checks over 7 families, 0 failures, exit 0. A planted +1 on one wrong was caught (20 of 20 draws).
2. Validator: 0 errors, no warning on either counting `fluency-*` file. `test-fluency.mjs --local-cdn` green for both sets (274 and 278 checks).
3. Playthrough `--fluency` for both sets, with and without `--mobile`: green; 440 px screenshots looked at, no layout faults.
4. `voice-scan.py 35` on `app/content/courses/counting`: 0 and 0.
5. I read 20 drawn items of every family as a learner would. Fixed: "You stopped after 1 factors" (now "one factor early") and a symmetry step that read oddly when $r$ was already the smaller side. No prompt gives the answer away.
