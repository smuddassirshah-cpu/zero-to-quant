# Fluency sets: testing (brief `docs/briefs/fluency.md`, second wave, agent 3, topics 1.5 and 1.6)

## Lessons chosen

- `l2-measuring-surprise`: $z = (\bar x - \mu_0)/(\sigma/\sqrt n)$, with a null of 0 (returns) and a null that is not 0 (the lesson's slippage in bp).
- `l4-t-test`: $t = \bar x/(s/\sqrt n)$, and the lesson's Sharpe ratio times $\sqrt T$.

Considered and left out:

- `l3-p-value`, `l6-power`, `l8-two-groups`, `l10-correcting`: procedural, left within the five-set budget for topic 1.6 (l3 and l6 would need tail areas given in the prompt, as the bell-curve set does).
- `l1`, `l5`, `l7`, `l9`, `l11`, `l12`: ideas and judgements (luck, two errors, what a p-value is not, snooping).

## Sets

Two sets, 4 families, in `app/content/courses/testing/fluency-l2-measuring-surprise.json` and `fluency-l4-t-test.json`. $z$ is asked to 2 decimal places (`tol` 0.005) and $t$ to 3 (`tol` 0.0005), as the lessons do.

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l2-measuring-surprise | z-null-zero | 193 | none (numeric) | divided-by-sigma, divided-by-n |
|  | z-null-nonzero | 198 | none (numeric) | centred-on-zero, divided-by-sigma |
| fluency-l4-t-test | t-statistic | 200 | none (numeric) | no-root-n, root-of-df |
|  | sharpe-t | 173 | none (numeric) | times-t, over-root |

Every decimal slip carries the key's tolerance, so a learner who rounds the slip is still named. `root-of-df` ($\sqrt{n - 1}$ for $\sqrt n$) is kept 0.002 clear of the key by `where`. `sharpe-t` rejects about half its draws (213 of 413) because a var's range cannot depend on another var: the period, years 2 to 10 or months 6 to 60, is filtered from one shared range. Raised in the inbox.

## Checks

1. `docs/reports/fluency-testing-numbers.py` (200 draws a family, shared checker `docs/reports/fluency_check.py`): each statistic is rebuilt as (estimate minus null) over a standard error with sympy's root of $n$ (tuple roots asserted equal); the Sharpe family rebuilds a mean and sd with that ratio and forms $t$ from them. Each `wrong` is recomputed from the vars, must sit outside the key's tolerance plus its own, and must differ from the other slips; the expected slip ids per draw mirror each `when`. The drawn text is scanned for `+-`, `--`, `+ -`, `^{1}`, `+0`, `1x`, `0x` and any `\frac{n}{d}` not in lowest terms. Result: 2,400 checks over 4 families, 0 failures, exit 0. A planted 0.01 on one slip (markov, run once) failed every draw, so the checker bites.
2. From `app/`: validator 0 errors and no warning naming a `fluency-` file; `node tools/test-fluency.mjs --local-cdn <pkgs> --set` green for both sets (300 checks each).
3. `node tools/playthrough.mjs --fluency <set> --local-cdn <pkgs>`, with and without `--mobile`: green for every set. Screenshots at 440 px looked at for markov and estimation l10 (the widest prompts): no overflow; the matrix sits inline and the set answer's feedback wraps cleanly.
4. `VOICE_BASE=app/content/courses/testing/ python3 docs/reviews/voice-scan.py 35`: 0 explanations over three sentences; 1 sentence over 35 words, in `homework-3.json` `items.8.widget.prompt` (45 words), which is not a Fluency file and was there before this wave (left for the course owner).
5. I read 20 drawn items of every family as a learner would (`fluency-sample.mjs --n 20` a family; dropped a rounded standard error that read $1/5 \approx 0.2000\%$). No `1x`, `+-`, `x^1`, `0x`, double minus or unreduced final fraction, and no prompt that gives the answer away. Working steps keep the lesson's unreduced branch fractions (such as $\tfrac{6}{9} \times \tfrac{5}{8}$) before the reduced result.
6. This report; engine limits in `docs/BACKLOG-INBOX.md` under `Raised later (fluency testing):` where there are any.
