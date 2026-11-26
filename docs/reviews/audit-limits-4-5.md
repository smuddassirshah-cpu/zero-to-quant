# Concept audit, round 1 (blind): limits L4 and L5

Auditor: Fable reader, 26 Nov 2026, at commit `6590e79e`. Scope: `app/content/courses/limits/` `l13` to `l20`, `review-4`, `review-5`, `homework-4`, `homework-5`, `problems-4`, `problems-5` and `fluency-l13-peaks-and-troughs` (the only Fluency file of these levels). Stage 1, topic 1.3, full ledger depth. Levels 1 to 3 are closed and were not read, except a grep to confirm that "differentiable implies continuous" is used the same way.

Blind rule kept: the ledger, the findings below and the concepts script were written and committed (WIP commit) before any `docs/reviews/review-*` or `audit-limits-*` file, `docs/reports/limits-*` or `gap-limits*` file was opened. The course's number scripts were run, not opened.

## Result

- Ledger: `docs/reports/audit-limits-4-5-ledger.md`, 1,604 rows: 1,584 correct, 16 imprecise, 4 wrong, 0 misleading, 0 unverified. A slip row covers the `wrong[]` value with its feedback line; a hints row covers every rung of a screen. Every line was read and judged.
- Findings: 15, all `minor`. 4 `wrong`, 11 `imprecise`. 0 `serious`.
- No finding touches a graded key, a definition or a method. The four `wrong` are one hint figure, two slip lines whose named mistake does not give the slip's value, and one feedback word. The theorems are stated correctly where they are stated in full (`l17` `screens[4]`, `l16` `screens[7]`, `l19` `screens[2]`); the `imprecise` findings are places that restate them with a hypothesis dropped.

## Method

- Every number, key, slip value and derivative was recomputed: `docs/reports/limits-L4-5-concepts.py`, 139 checks with sympy 1.14, NumPy 2.5 and SciPy 1.18 (newer than CI's pins; no figure depends on the version). Limits by `sympy.limit`, the bond by repricing, the normal quantile by SciPy.
- Fluency: all four families of `fluency-l13` were enumerated over their whole range (56, 56, 280 and 1,680 admissible cases). Each key was classified independently with $f''$, each closed-interval key against a grid of the interval, and each case checked for a slip equal to the key or to another shown slip. No failure.
- Empirical claims: the Kelly statements in `homework-4` `h-long-kelly` (about 0.5% log growth a bet, a factor near 150 over 1,000 bets, twice Kelly does not grow, Kelly beats other stakes) by Monte Carlo, 20,000 paths of 1,000 bets, paired across stakes, at four standard errors.
- Hypotheses were tested with counterexamples in the script: a continuous P&L that is never at its average rate, a misuse of L'Hôpital that is right by accident, a function with $f''(a) > 0$ whose $f'$ is not increasing near $a$.
- There are no code widgets in these levels, so the code sweep does not apply.

Claims that pass but deserve a note:

- `l16` uses L'Hôpital on $\tfrac{\sin x}{x}$ and $\tfrac{e^{x} - 1}{x}$. As proofs these would be circular, since those limits define the derivatives. The lesson uses them as computations, not proofs. Correct.
- `l20` `screens[5]` and `screens[8]`: an inflection point must be a point of the graph, and may have a vertical tangent. This is Stewart's definition (4.3). Texts that require $f'$ to exist at the point would not count $\sqrt[3]{x}$; the lesson states its convention, so the key is right under it.
- `l15`: modified duration is $-P'/P$ with annual compounding, and Macaulay is $D(1 + y)$. Standard (Hull ch. 4), and said where it first matters.
- `l18` `screens[7]`: "a real ladder would leave the wall long before". With the foot at a steady 0.5 m/s, $y'' = -6.25/y^3$ passes $g$ near $y = 0.86$ m, well above 0.1 m. Correct.
- `homework-4` `h-long-kelly` (c): "grows by a factor of about $e^{5.0}$" is the typical (median) path, which the Monte Carlo confirms. The mean factor is far larger; the model answer says "log growth", so it is correct as worded.

## Findings

1. `l16-both-to-zero.json` | `screens[0].hints[1].text` | wrong, minor | "At $x = \pm 0.01$ both columns are within 0.005 of the same whole number." The table's own entry 1.005017 is 0.005017 from 1. | Script `FINDING 1`; the table row three lines above. | Replace with: `At $x = \pm 0.01$ both columns are within 0.006 of the same whole number.`

2. `l17-somewhere-in-between.json` | `screens[7].widget.wrong[2]` (`double`, value 16) | wrong, minor | The feedback names the mistake "You went the full 3 units from $x = 0$". That gives $5 + 3 \times 3 = 14$, not 16. No reading of the screen gives 16 from that mistake, so a learner who makes it gets the generic line. | Script `FINDING 2`. | Set `"value": 14`. The feedback line stays.

3. `l19-running-backwards.json` | `screens[10].feedback.byKey.wrong-units` (slip 2.5) | wrong, minor | "You took $\tfrac{1}{0.04}$." That is 25. The slip 2.5 is $\tfrac{0.10}{0.04}$, the price change over a vega misread as 0.04 (it is also $\tfrac{1}{0.40}$). | Script `FINDING 3`. | Replace with: `You divided by 0.04. The vega is £0.40 per volatility point, so the rise is $\tfrac{0.10}{0.40}$.`

4. `l17-somewhere-in-between.json` | `screens[2].feedback.byKey.flat` | wrong, minor | "You stopped near the top of the dip". The region $0.8 \le x \le 1$ is the bottom of the dip: $f(1) = -2$ is the local minimum, and `l13` calls it "the bottom of the dip". | $f'(1) = 0$, $f''(1) = 6 > 0$. | Replace with: `You stopped near the bottom of the dip, where the tangent is flat. The line through the ends rises with slope 1, so the tangent must rise too.`

5. `l17-somewhere-in-between.json` | `screens[0].explain.text`, `screens[4].question`, `quiz[2].prose` | imprecise, minor | Each draws the theorem's conclusion from "no gaps" alone, which is continuity. The theorem also needs a slope at every moment inside, as `screens[5]` of the same lesson shows. `quiz[2]` has no picture, so its key 150 rests on the unstated hypothesis. | Spivak ch. 11 Thm 4. Script counterexample: a P&L rising at £100 an hour for 3 hours and £200 for 3 hours is continuous, goes from £2,000 to £2,900, and is never at £150. | `screens[0].explain.text`, second and third sentences: `The stock rose £6 in 3 hours along a smooth path, with no gap and no corner. So at some moment it moved at exactly the average speed.` `screens[4].question`: `The stock rose from £100 to £106 over 3 hours along a smooth path, with no gaps or corners. What does the theorem say about $f'(c)$?` `quiz[2].prose`: `A desk's P&L rises smoothly from £2,000 at 09:00 to £2,900 at 15:00, with no gaps and no corners.`

6. `l17-somewhere-in-between.json` | `screens[9].widget.lines[0]` (id `a`) | imprecise, minor | The proof of Rolle's theorem never states its hypotheses. Line `b` uses $f(a) = f(b)$ ("they are equal") and line `c` uses differentiability inside ("where the tangent is flat"), but line `a` assumes only continuity. | Spivak ch. 11 Thm 3. | Replace line `a` with: `Take $f$ continuous on $[a, b]$ and differentiable inside, with $f(a) = f(b)$. It has a highest and a lowest point (the extreme value theorem)`

7. `l16-both-to-zero.json` | `screens[2].prose` | imprecise, minor | The rule is named and stated with $f(a) = g(a) = 0$ as its only condition. The condition that the limit of $\tfrac{f'}{g'}$ exists comes five screens later. | Spivak ch. 11 Thm 9; Stewart 4.4. | After the display, insert: `It holds whenever the limit on the right exists.`

8. `l16-both-to-zero.json` | `screens[7].explain.text` | imprecise, minor | "The other three are not indeterminate, so you just substitute." For $\tfrac{\cos x}{x}$ substitution gives $\tfrac{1}{0}$: there is nothing to read off and the limit does not exist. | One-sided limits $\pm\infty$ (script). | Replace the last sentence with: `Two of the others you just substitute. $\tfrac{\cos x}{x}$ has the form $\tfrac{1}{0}$: it has no limit, and the rule does not apply.`

9. `l16-both-to-zero.json` | `summary.trap` | imprecise, minor | "the rule gives a wrong answer" is an always-claim that is false: misuse can land on the right value. | $\tfrac{x + 1}{2x + 2}$ at 0 is $\tfrac{1}{2}$, and $\tfrac{f'}{g'} = \tfrac{1}{2}$ too (script). | Replace with: `If the form is not $\tfrac{0}{0}$ or $\tfrac{\infty}{\infty}$, the rule can give a wrong answer. Check the form first.`

10. `l19-running-backwards.json` | `screens[3].prose` | imprecise, minor | "Implicit differentiation proves it for every differentiable, increasing $f$." The chain-rule step assumes $f^{-1}$ has a derivative. It shows what the slope must be, not that there is one, and for $x^3$ at 0 there is none. | Spivak ch. 12 makes exactly this point before Thm 5. | Replace the second sentence with: `Implicit differentiation gives the formula for a differentiable, increasing $f$, taking for granted that $f^{-1}$ has a slope there.`

11. `l20-which-way-it-bends.json` | `screens[7].widget.options[1].why` | imprecise, minor | "It is necessary, but the sign of $f''$ must also change". $f'' = 0$ is necessary only where $f''$ exists. The next screen has an inflection point where $f''$ does not exist. | $\sqrt[3]{x}$ at 0, `screens[8]`. | Replace with: `You treated $f'' = 0$ as enough. The sign of $f''$ must change, and $12x^2 \ge 0$ does not.`

12. `l13-peaks-and-troughs.json` | `screens[8].widget.lines[1]` (id `d2`), `lines[2]` (id `d3`), `screens[8].explain.text` | imprecise, minor | "$f'$ is increasing near $a$" does not follow from $f''(a) > 0$ at one point. What follows is that $f'$ rises through $a$: below $f'(a)$ just left, above it just right. The conclusion is right; the middle step is stronger than the hypothesis gives. | Spivak ch. 11 Thm 5 uses the limit definition of $f''(a)$. Script: $f'(x) = \tfrac{x}{2} + x^2\sin\tfrac{1}{x}$ has $f''(0) = \tfrac{1}{2}$ and $f'' < 0$ arbitrarily near 0. | `d2`: `$f''(a) > 0$ is the slope of $f'$ at $a$, so $f'$ rises through $a$`. `d3`: `An $f'$ that rises through 0 at $a$ is negative just left of $a$ and positive just right`. `explain.text`, first sentence: `$f''(a) > 0$ makes $f'$ rise through $a$, so $f'$ passes 0 from below.`

13. `l17-somewhere-in-between.json` | `screens[6].widget.options[3].why` | imprecise, minor | "That is the argument the theorem makes, and it fails here. The price does not pass through every speed between £1 and £2." The option states the theorem's conclusion, not its argument, and the speed is £1 wherever it exists. The line suggests the theorem works by speeds passing through values in between. | Spivak's proof (Rolle on $f$ minus the chord) uses no such step. | Replace with: `That is the theorem's conclusion, and the theorem needs a path with no jump. Here the speed is £1 an hour wherever it exists.`

14. `l16-both-to-zero.json` | `screens[5].explain.text` | imprecise, minor | "A log grows more slowly than any power of $x$." True for positive powers only. | $\ln x$ outgrows $x^0$ and $x^{-1}$. | Replace the last sentence with: `A log grows more slowly than any positive power of $x$.`

15. `review-5.json` | `items[3].prose` | imprecise, minor | "The distance $x$ along the ground to the point below the station". The station is on the ground; $x$ runs from the point below the plane to the station. | The stated link $s^2 = x^2 + 25$. | Replace the second sentence with: `The distance $x$ along the ground from the point below the plane to the station falls at 300 km/h.`

## Gates

- Validator: `cd app && node tools/validate.mjs`: 0 errors.
- Number scripts: `node tools/run-number-scripts.mjs --only limits`: 9 of 9 passed.
- `node tools/grade-all.mjs --file <file> --local-cdn <pkgs>` on each of the 15 files: 0 failures (217 widgets and 4 Fluency templates).
- Concepts script: `docs/reports/limits-L4-5-concepts.py`, 139 checks, 3 failing (`FINDING 1` to `FINDING 3`), exit 1. It exits 0 once findings 1 to 3 are fixed.
- No playthrough (common rules).

## Overlap table

OVERLAP_PLACEHOLDER

## Inbox

One bullet, added to `docs/BACKLOG-INBOX.md` under "Raised later (audit limits):".
