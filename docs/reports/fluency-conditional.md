# Fluency sets: conditional (brief `docs/briefs/fluency.md`, second wave, agent 3, topics 1.5 and 1.6)

## Lessons chosen

- `l7-turning-around`: Bayes' rule as a procedure, from a two-way count and from three rates; the learner needs fresh numbers to stop swapping the condition.

Considered and left out:

- `l6-adding-branches`: total probability is the denominator here, so it is drilled as the family `every-positive-path` rather than a set of its own.
- `l8-base-rates`, `l9-natural-frequencies`, `l10-odds-form`, `l11-updating-twice`: the same calculation in other dress, or a second pass of it; left within the six-set budget.
- `l1` to `l5`: shrinking the space and the multiplication rule, mostly reading a diagram or tree.
- `l12` to `l26`: many hypotheses, independence ideas, puzzles (Monty Hall, Bertrand, two children) and fallacies, whose point is a judgement or a set-up.

## Sets

One set, 3 families, in `app/content/courses/conditional/fluency-l7-turning-around.json`. The count family answers in exact fractions; the rate families work in decimals as the lesson does (its rate screens give 0.3077 and "Give a decimal"): $P(+)$ exactly, $P(B \mid +)$ to 3 decimal places.

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l7-turning-around | from-counts | 199 | none (numeric) | inverse, joint |
|  | from-rates | 178 | none (numeric) | inverse, no-division, unweighted-others |
|  | every-positive-path | 182 | none (numeric) | one-path, unweighted-others |

The notation is the lesson's $P(\text{ill} \mid +)$, with three contexts (people and ill, parts and faulty, payments and fraudulent). The 3 dp slip `unweighted-others` carries `tol` 0.0005 so a learner who rounds it is still caught; `where` keeps it 0.002 clear of the key and of the other two slips (the numbers script found one draw where it equalled `inverse` before that guard).

## Checks

1. `docs/reports/fluency-conditional-numbers.py` (200 draws a family, shared checker `docs/reports/fluency_check.py`): the count family builds the population person by person and counts inside the positives; the rate families turn the percentages into natural frequencies over 1,000,000 cases and count, so Bayes' rule is never evaluated. Each `wrong` is recomputed from the vars, must sit outside the key's tolerance plus its own, and must differ from the other slips; the expected slip ids per draw mirror each `when`. The drawn text is scanned for `+-`, `--`, `+ -`, `^{1}`, `+0`, `1x`, `0x` and any `\frac{n}{d}` not in lowest terms. Result: 2,000 checks over 3 families, 0 failures, exit 0. A planted 0.01 on one slip (markov, run once) failed every draw, so the checker bites.
2. From `app/`: validator 0 errors and no warning naming a `fluency-` file; `node tools/test-fluency.mjs --local-cdn <pkgs> --set` green for the set (304 checks).
3. `node tools/playthrough.mjs --fluency <set> --local-cdn <pkgs>`, with and without `--mobile`: green for every set. Screenshots at 440 px looked at for markov and estimation l10 (the widest prompts): no overflow; the matrix sits inline and the set answer's feedback wraps cleanly.
4. `VOICE_BASE=app/content/courses/conditional/ python3 docs/reviews/voice-scan.py 35`: 0 explanations over three sentences, 0 sentences over 35 words.
5. I read 20 drawn items of every family as a learner would (`fluency-sample.mjs --n 20` a family; capped the prior at 40% in `every-positive-path` and fixed a solution step that began with a lower-case word). No `1x`, `+-`, `x^1`, `0x`, double minus or unreduced final fraction, and no prompt that gives the answer away. Working steps keep the lesson's unreduced branch fractions (such as $\tfrac{6}{9} \times \tfrac{5}{8}$) before the reduced result.
6. This report; engine limits in `docs/BACKLOG-INBOX.md` under `Raised later (fluency conditional):` where there are any.
