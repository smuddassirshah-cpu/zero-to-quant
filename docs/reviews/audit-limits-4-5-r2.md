# Blind concept audit, round 2: limits levels 4 and 5

Auditor name `limits-4-5-r2`. Commit audited: d85c9279. Scope: `l13` to `l20`, `review-4`, `review-5`, `homework-4`, `homework-5`, `problems-4`, `problems-5`, `fluency-l13-peaks-and-troughs`. Stage 1, full ledger.

Ledger: `docs/reports/audit-limits-4-5-r2-ledger.md` (2,625 rows: 2,615 correct, 4 wrong, 6 imprecise, 0 misleading, 0 unverified).
Script: `docs/reports/limits-L4-5-concepts-r2.py` (34,819 checks; exits 1 on three checks that fail because the content is wrong: findings 1, 2 and 3).

## What was checked

- Every printed figure in prose, hints, feedback, explains, captions and tables, recomputed (sympy, NumPy, SciPy).
- Every numeric slip: the value its named mistake gives, against the stored value. No slip sits inside a key's tolerance and no two slips overlap.
- Every expression widget: each `accept` form equals the key and each `wrong` form differs from it.
- Mean value theorem and Rolle: both hypotheses are stated (`l17` screens 4 to 6), the proof order is the standard one (Spivak ch. 11, Thms 3 and 4), and each applied use names continuity and differentiability.
- L’Hôpital: the form is checked before the rule on every item; the two trap items give the wrong value the misapplied rule produces (1 and 2).
- First and second derivative tests, closed intervals, the Kelly fraction, duration and convexity, the inverse-function rule, inflection points: all agree with the sources named in the ledger.
- Taylor remainder claims (`l15` summary, `review-4` item 8, `homework-4` items 6 and 7, `l17` screen 10): correct.
- Empirical claims by simulation: Kelly growth per bet (one binomial draw of 1e9 bets at p = 0.6; 4e10 bets at p = 0.55, which separates G(0.2) = −0.00014 from 0), minimum variance at 9/13 (2e6 draws), Jensen for log utility (4e6 flips).
- Fluency: all four families over their whole range, 4,088 admissible variants. Every key, table value, solution line and slip is right, and keys and active slips never collide.

## Findings

1. `l17-somewhere-in-between.json` | `screens[2].hints[1].text`, `screens[2].feedback.generic`, `screens[2].feedback.correct` | wrong, minor | The hint and the generic line tell the learner to find a tangent label that reads 1.00. The label can never read 1.00. | P snaps to 0.05 in $x$ (`snapX`), and $f'(x) = 3x^2 - 3$ gives labels 0.63, 0.97, 1.32 at $x = 1.10$, 1.15, 1.20. The correct line says "At $x = 1.15$ the tangent has slope 1", but $f'(1.15) = 0.9675$, and it shows for any accepted $x$ from 1.10 to 1.25 (labels 0.63 to 1.69, `tol` 0.1). Script check `l17 s2 hint and feedback ask for a label of 1.00`. | Hint: "The solid line has slope 1, so look for the tangent whose label is closest to 1. It reads 0.97 at $x = 1.15$." Generic: "Not quite right. Move P until the tangent's label is as close to 1 as it gets." Correct: "Near $x = 1.15$ the tangent has slope close to 1, almost parallel to the line through the ends." Set `widget.points[0].tol` to 0.06, so only $x = 1.10$, 1.15 and 1.20 pass.

2. `l14-best-value.json` | `screens[9].feedback.byKey.p` | wrong, minor | "At $f = 0.6$ the growth rate is negative: drag P there and see." P cannot be dragged there. | The curve's `domain` and the plane's $x$ range both stop at 0.5, and `plane.js` clamps a dragged point to them. The figure itself is right: $G(0.6) = 0.6\ln 1.6 + 0.4\ln 0.4 = -0.0845$. Script check `l14 s9 feedback.byKey.p`. | "You staked the chance of winning. At $f = 0.6$ the growth rate is $-0.085$ a bet. Drag P to 0.5: it is already negative there."

3. `homework-5.json` | `items[6].feedback.byKey.flipped` | wrong, minor | The line names the mistake "used $\tfrac{w_2}{w_1}$ where the formula has $\tfrac{w_1}{w_2}$ and the variance ratio 4". That mistake does not give the slip's value. | With $\tfrac{w_2}{w_1}$ and the 4 kept: $-4 \times \tfrac{0.4}{0.3} \times 0.01 = -0.0533$. The slip value $-0.0033$ is the whole fraction inverted: $-\tfrac{0.02 \times 0.4}{0.08 \times 0.3} \times 0.01$. Script check `h5 risk flipped: the named mistake`. | "You turned the whole fraction upside down: $\tfrac{0.02w_2}{0.08w_1}$. Solving for $w_2'$ gives $-\tfrac{0.08w_1}{0.02w_2}\,w_1'$."

4. `review-5.json` | `items[0].feedback.byKey.quarter` | imprecise, minor | "That is $c^2$ with the wrong power." 4 is $c^2$ itself; no power is wrong. | The slip is stopping at $c^2 = 4$. | "That is $c^2$, not $c$. Take the square root: $c = 2$."

5. `l18-rates-in-step.json` | `screens[10].prose` | imprecise, minor | "From the sensitivity level". No level has that name. | The rule is from lesson `l15` (Sensitivity of a price) in level 4, "Using derivatives" (`course.json`). `l19` uses "the rules level" correctly for level 3. | "From the lesson on sensitivity, $\dfrac{\Delta P}{P} \approx -D\,\Delta y$."

6. `l13-peaks-and-troughs.json` | `screens[5].feedback.correct` | imprecise, minor | "Same second derivative, different verdicts." The second derivatives are $6x$ and $12x^2$; only their values at 0 agree. | The prose on the same screen states both. | "Both second derivatives are 0 at 0, yet the verdicts differ."

7. `l17-somewhere-in-between.json` | `screens[10].prose` | imprecise, minor | "The option's value changes by delta times the move" is true only if delta is constant. | The explain gives the correct statement, $\Delta C = \delta(c) \times 10$ for some $c$ (mean value theorem, Spivak ch. 11 Thm 4). | "Over a small move the option's value changes by about delta times the move. The theorem makes this exact at some price in between, so it bounds the change over a £10 move."

8. `l14-best-value.json` | `summary.formula.note` | imprecise, minor | $f^* = p - \tfrac{q}{b}$ maximises $G$ on $0 \le f < 1$ only when it is positive. The lesson never says what to do when it is not. | $G'(0) = pb - q$ and $G'' < 0$, so for $pb \le q$ the maximum on the interval is at $f = 0$ (`homework-4` item 9 part (e) proves it). `review-4` item 7's slip $-0.4$ shows a negative value arises. | Append to the note: "If this is 0 or negative, stake nothing."

Serious: 0. Minor: 8 (3 wrong, 5 imprecise; finding 1 covers three ledger rows, two wrong and one imprecise).

## Tool results

- `node tools/validate.mjs`: 0 errors, 4,622 warnings.
- `node tools/run-number-scripts.mjs --only limits`: 9 of 9 passed.
- `node tools/grade-all.mjs --file <file> --local-cdn <pkgs>`: 0 failures on each of the 15 files.
- `limits-L4-5-concepts-r2.py`: exit 1; 34,819 checks, 3 failed (findings 1 to 3). Venv Python 3.13 with newer NumPy, SciPy and sympy than CI pins; no figure depends on the version.
- No playthrough, as the common rules set. No code widgets in scope.

## Overlap table

Earlier reads, opened after the ledger and the findings above were written: `docs/reviews/audit-limits-4-5.md` (round 1, 15 findings, all fixed in its fix pass), `docs/reviews/review-1.3.md` (one content finding on `homework-4`), `docs/reviews/review-problems-1.3-c.md` and the other problem-set reviews (four conceptual findings on `problems-4`, `problems-5` and `homework-4`, as round 1 lists them), and the author report `docs/reports/limits-5.md`. None of them names any of the eight findings here.

| | Count |
|---|---|
| Found by this audit only | 8 (3 wrong, 5 imprecise) |
| Found by the earlier reads only | 19 (15 in round 1, 4 before it; all fixed before this round) |
| Found by both | 0 |

New `wrong` that no earlier read found: 3 findings (four ledger rows), all minor. None changes a key, a theorem, a method or a convention. Findings 1 and 2 are lines that ask for a canvas state the canvas cannot show; finding 3 is a slip line that names the wrong mistake. Round 1's fixes all hold: each of its 15 was re-read and recomputed in this round's ledger and is `correct`.

Convergence: round 1 gave 4 new `wrong` on these two levels, this round 3, all minor and of a narrower kind (no figure, key or slip value is wrong now). That is still above one per three levels, so a further blind round is due after the fix pass, unless the session accepts that the remaining class is covered by the validator rule asked for in the inbox.

## Inbox

One bullet added to `docs/BACKLOG-INBOX.md` under "Raised later (audit limits):": a validator warning for hint or feedback lines that quote a label value no snapped position renders, or an $x$ outside a dragged point's domain.
