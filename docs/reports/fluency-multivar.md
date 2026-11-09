# Fluency sets: multivar (brief `docs/briefs/fluency.md`, agent 7)

Two sets, 6 families, in `app/content/courses/multivar/fluency-*.json`. Every family is a typed answer. No family uses `form`: each task is "find a level", "find a value" or "find a partial derivative", and retyping the prompt's $f$ never equals the key.

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l1-two-inputs | contour-through-a-point | 198 | none (numeric) | negative-square, swapped |
| | walk-along-a-contour | 166 | none (numeric) | sign-lost, upside-down |
| | point-on-a-contour | 196 | none (numeric) | signs-not-changed, one-term-moved |
| fluency-l3-second-partials | first-partial | 200 | none | x-term-differentiated, x-factor-dropped |
| | bend-at-a-point | 200 | none (numeric) | stopped-at-first, mixed-instead |
| | mixed-partial | 200 | none | product-of-partials, pure-term-kept, power-not-lowered |

## A departure from the brief's table

The table gives `l1-two-inputs` "first partial derivatives". That lesson teaches functions of two inputs and contour maps only; partial derivatives start in `l2-slicing` (its objective: "Compute partial derivatives by holding one variable fixed"). The brief's first rule (only ideas taught up to that lesson) wins, so:

- `fluency-l1-two-inputs` drills what l1 teaches, in its wording: "Which level $c$ is the contour that passes through $(3, 4)$?" (its quiz), a walk along a contour of a linear function (its P&L screen: "What change in B's price keeps your P&L at exactly £0?"), and the missing coordinate of a point on a contour of $f = y - x^2 + \dots$ (its screens on $y - x^2$).
- First partials are drilled as the `first-partial` family of `fluency-l3-second-partials`, where they are the first step of every second partial. One partial per item ($f_y$), never a gradient vector.
- Proposal for the main session: a `fluency-l2-slicing` set would be the natural home for first partials ($f_x$ and $f_y$ of products of powers, and a partial at a point). It is outside row 7, so I did not write it.

`fluency-l3-second-partials` uses the lesson's notation ($f_y$, $f_{xx}$, $f_{xy}$, "the mixed partial") and its trap ($f_{xy}$ is not $f_x \times f_y$) as a named slip. The bend family fixes the powers ($c\,x^3y^n + b\,x^4 + e\,y^q$) so that $f_{xx} = 6c\,xy^n + 12b\,x^2$ prints with no `x^{1}`; the expression families draw every power from 3 up for the same reason (a known limit, not re-raised).

## Skipped

No family skipped. One limit raised in `docs/BACKLOG-INBOX.md` under `Raised later (fluency taylor multivar):` (an exponential in `let`, met in the taylor set).

## Checks

1. `docs/reports/fluency-multivar-numbers.py` (sympy, 200 draws per family): levels by substituting the point, the contour walk by solving $a\,\Delta x + b\,\Delta y = 0$ (and checking $f$ is unchanged), the missing coordinate by `solve`, partials by `diff` (and $f_{xy} = f_{yx}$ checked). Each `wrong` is recomputed from the vars and must differ from the key. Result: 3,800 checks over 6 families, 0 failures, exit 0. A planted error (+1 on one key) was caught.
2. Validator: 0 errors; 4,110 warnings before and after (none on a `fluency-*` file). `test-fluency.mjs --local-cdn`: 274/274 (l1), 272/272 (l3), and the default run 529/529.
3. Playthrough `--fluency`, with and without `--mobile`: green for both sets. I looked at the 440 px item, wrong-answer and end-card screenshots: no overflow.
4. `voice-scan.py 35` on `app/content/courses/multivar`: 0 and 0.
5. I read 20 drawn items of every family as a learner would and ran a pattern scan (`1x`, `+-`, `x^1`, `0x`, double minus, `+0`, `-0`, `1 \times`, float artefacts, unreduced `\frac`). It found `-1 \times 3` in a solution (reworded), `y^{1}` in a slip's tex (powers now from 3) and one draw where the two point-on-a-contour slips coincided (now excluded by `where`). Final scan clean; no prompt gives the answer away.
