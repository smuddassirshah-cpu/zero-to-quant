# Fluency sets: markov (brief `docs/briefs/fluency.md`, second wave, agent 3, topics 1.5 and 1.6)

## Lessons chosen

- `l2-transition-matrix`: a two-step chance as a row times a column, and a distribution moved one step by $\boldsymbol{\pi}_0\mathbf{P}$, on the lesson's bull-bear and Sunny-Cloudy-Rain chains.

Considered and left out:

- `l5-where-it-settles`, `l7-how-long`, `l8-which-end`, `l10-gamblers-ruin`: procedural but each a small linear system with one or two shapes; left within the six-set budget.
- `l1`, `l3`, `l4`, `l6`, `l9`, `l11` to `l22`: ideas (the Markov property, absorbing states, convergence, martingales, stopping) or simulation.

## Sets

One set, 3 families, in `app/content/courses/markov/fluency-l2-transition-matrix.json`. Entries are tenths, so every answer is an exact decimal (numeric, `tol` 0).

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l2-transition-matrix | two-state-two-step | 148 | none (numeric) | squared-entry, one-step |
|  | three-state-two-step | 172 | none (numeric) | squared-entry, one-step |
|  | distribution-forward | 184 | none (numeric) | bull-row-only, unweighted-column |

The matrix is in the prompt as a `pmatrix`; at 440 px it sits inline beside the sentence without overflow (screenshot looked at). Each slip carries `when` so it is offered only where it differs from the key (a chain whose two-step chance equals its one-step chance).

## Checks

1. `docs/reports/fluency-markov-numbers.py` (200 draws a family, shared checker `docs/reports/fluency_check.py`): the matrix is rebuilt as an exact sympy Matrix (rows checked to add to 1), two-step chances are entries of `P**2`, and the moved distribution is the row vector times `P`. Each `wrong` is recomputed from the vars, must sit outside the key's tolerance plus its own, and must differ from the other slips; the expected slip ids per draw mirror each `when`. The drawn text is scanned for `+-`, `--`, `+ -`, `^{1}`, `+0`, `1x`, `0x` and any `\frac{n}{d}` not in lowest terms. Result: 1,788 checks over 3 families, 0 failures, exit 0. A planted 0.01 on one slip (markov, run once) failed every draw, so the checker bites.
2. From `app/`: validator 0 errors and no warning naming a `fluency-` file; `node tools/test-fluency.mjs --local-cdn <pkgs> --set` green for the set (304 checks).
3. `node tools/playthrough.mjs --fluency <set> --local-cdn <pkgs>`, with and without `--mobile`: green for every set. Screenshots at 440 px looked at for markov and estimation l10 (the widest prompts): no overflow; the matrix sits inline and the set answer's feedback wraps cleanly.
4. `VOICE_BASE=app/content/courses/markov/ python3 docs/reviews/voice-scan.py 35`: 0 explanations over three sentences, 0 sentences over 35 words.
5. I read 20 drawn items of every family as a learner would (`fluency-sample.mjs --n 20` a family; nothing to fix). No `1x`, `+-`, `x^1`, `0x`, double minus or unreduced final fraction, and no prompt that gives the answer away. Working steps keep the lesson's unreduced branch fractions (such as $\tfrac{6}{9} \times \tfrac{5}{8}$) before the reduced result.
6. This report; engine limits in `docs/BACKLOG-INBOX.md` under `Raised later (fluency markov):` where there are any.
