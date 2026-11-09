# Fluency sets: taylor (brief `docs/briefs/fluency.md`, agent 7)

Two sets, 7 families, in `app/content/courses/taylor/fluency-*.json`. Every family is a typed answer. No family uses `form`: each task is "write the tangent line", "estimate" or "find a coefficient", and retyping the prompt's $f$ never equals the key (AUTHORING 16, "Choosing `form`").

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l1-tangent-approx | write-the-line | 200 | none | slope-at-x, swapped |
| | estimate-a-power | 150 | none (numeric) | calculator, no-step, used-x |
| | estimate-a-root | 81 | none (numeric) | calculator, no-step, slope-not-halved |
| fluency-l6-matching-derivatives | exponential-coefficient | 115 | none (numeric) | no-factorial, chain-forgotten |
| | trig-coefficient | 116 | none (numeric) | no-factorial, sign-lost, chain-forgotten |
| | centred-cubic | 200 | none (numeric) | not-halved, at-zero |
| | exponential-about-a | 117 | none | at-x, no-factorial |

Each set keeps to its lesson's notation and wording. l1: "the tangent line approximation $L(x)$ of $f$ at $a$" (its quiz item on $x^3$ at 2), "Use the tangent line at $a = 9$ to estimate $\sqrt{8.9}$" (its base-point screen; the root family draws a perfect square $a$ and a step of 0.05 to 0.9), and the slips the lesson names ($f'(x)$ left in, height and slope swapped, $x$ used for $x - a$, the calculator value, slope $\frac{1}{\sqrt a}$ not halved). l6: "Take $f(x) = e^{3x}$ about 0. What is the coefficient of $x^3$?" (its quiz), extended to $c\,e^{mx}$, $c\sin(mx)$, $c\cos(mx)$, a cubic about $a$ (coefficient of $(x - a)^2$, from l5 and l6) and $c\,e^x$ about $a$ (the lesson's trap: a coefficient is evaluated at the centre, $e/6$ not $e^x/6$). The last family's key is exact, "in terms of $e$", because `let` has no exponential.

Design notes. The sine and cosine family ties the text pick `fn` to the parity of $k$ with `where` (about half the draws rejected) and gets the sign from $(-1)^{\lfloor k/2 \rfloor}$, which serves both. The root family keeps the calculator value more than 0.0003 from the line's value (`where`), so it can be named as a slip at the 0.0001 tolerance. $a = 1$ is left out of the $e^x$ about $a$ family because it would print `e^{1}`.

## Skipped

None of the brief's families for taylor was skipped. One limit raised in `docs/BACKLOG-INBOX.md` under `Raised later (fluency taylor multivar):`: `let` has no `exp` or `ln`, so the lesson's "coefficient of $(x - 2)^2$ for $e^x$, to 4 decimal places" is drilled with an exact key in terms of $e$, and no tangent-line family on $e^x$ or $\ln x$ away from 0 and 1 was attempted.

## Checks

1. `docs/reports/fluency-taylor-numbers.py` (sympy, 200 draws per family): each key is rebuilt from the vars alone: the line from `diff` at $a$, the estimates as $f(a) + f'(a)\,h$, each coefficient as $f^{(k)}(a)/k!$ from sympy's $k$-th derivative and cross-checked against `series` (about 0) or the expansion in $x - a$ (cubic). Each `wrong` is recomputed from the vars and must differ from the key by more than its tolerance. Result: 4,800 checks over 7 families, 0 failures, exit 0. A planted error (+1 on one key) was caught.
2. Validator: 0 errors; 4,110 warnings before and after the sets (none on a `fluency-*` file). `test-fluency.mjs --local-cdn`: 273/273 (l1) and 277/277 (l6).
3. Playthrough `--fluency`, with and without `--mobile`: green for both sets. I looked at the 440 px item and end-card screenshots: no overflow.
4. `voice-scan.py 35` on `app/content/courses/taylor`: 0 explanations over three sentences, 0 sentences over 35 words.
5. I read 20 drawn items of every family as a learner would, and ran a pattern scan over every drawn prompt, key, `accept`, solution, `wrong` tex and line for `1x`, `+-`, `x^1`, `0x`, a double minus, `+0`, `-0`, `1 \times`, float artefacts and unreduced `\frac`. It found `e^{1}` (now excluded), `32^{3}` and `-1 \times 2^{2}` in solutions (reworded); the final scan is clean. No prompt gives the answer away.
