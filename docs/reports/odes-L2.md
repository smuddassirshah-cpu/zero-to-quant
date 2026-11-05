# odes level 2: Second-order equations

Author: content agent (odes L1 to L3 wave). Brief: `docs/briefs/odes.md` `## Level 2`.

## Files

| file | screens / items | quiz | notes |
|---|---|---|---|
| `l6-second-order.json` | 10 screens | 4 | hook: `sliders` on $y(0)$, $y'(0)$ to hit a target; superposition with controls on $c_1, c_2$; boundary value edge case ($c\sin t$); `code` residual and `as_system` |
| `l7-characteristic-equation.json` | 10 screens | 4 | dragged $r$ on $r^2 - 3r + 2$; repeated-root `order` proof; complex root as one `expression` ($-1 + 2i$); roots moving in the complex plane with a `slider` on $b$; perpetual put transfer |
| `l8-forcing.json` | 11 screens | 4 | slider guess of a constant; `table` widget for $A$, $B$; trap on fitting too early (wrong curve as option patch); resonant guess `order`; singular `matrix`; smoother lag on a `series` |
| `l9-damping-and-resonance.json` | 11 screens | 4 | one curve for all $b$ (`exprs` switched by a derived index); settling table; overshoot; resonance `order`; `drag-point` on the amplitude response |
| `review-2.json` | 9 items | | difficulty 2 to 4, every lesson, one level 1 recall (`r-recall`) |
| `homework-2.json` | 8 items | | difficulty 3 to 5; `h-step` `code` (difficulty 5, all three regimes); `h-repeated` order derivation; `h-smoother` longform with a 10-point rubric |

Performance task: none. No level 2 objective starts with a verb of the rule (Recognise, Solve, Find, Read), and the validator agrees.

Euler's formula: stated in l7 screen 5 myself, with a pointer to `complex` l3, since `complex` is unwritten. Only the real and imaginary parts of $e^{(\alpha + i\beta)t}$ are used.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; no warnings on any level 2 file.
2. Voice scan over `app/content/courses/odes/`: 0 explanations over three sentences, 0 sentences over 20 words.
3. `python3 docs/reports/odes-L2-numbers.py`: 0 failures, exit 0. Route 2 is a 40,000-step RK4 solve of each equation as a system, a root finder, or a 400,001-point grid for the amplitude peak.
4. Playthrough with `--local-cdn`: l6 to l9, review-2 and homework-2 green with `--mobile` and without; level 1 replayed green in the same runs after the pound-sign fix below.

Screens read at 440 px and desktop. Fixed after reading: the l8 `matrix` cells (plain strings printed raw; now `$...$`), l7 axis titles cut off at 440 px (now "Re" and "Im", with the circle $|r| = 2$ dashed).

Also fixed in level 1 files during this level: a pound sign inside `$...$` rendered in italic maths type (AUTHORING section 4). The generator now writes `\text{£}` inside maths in every odes file; validator and playthrough re-run green on level 1.

## Numbers (source: the script; both routes agree)

l6: $y(\pi) = -1$, $c_2 = 1$, $W(0) = 1$, residual $2e^3$. l7: 4.6708 (4.670774), 0.4060 (0.406006), 0.014164, 0.18142 (distractor), roots 1 and $-2.5$, £71.43, £12.32, 1.270671 (code test). l8: $A = \tfrac{1}{20}$, $(-3, 1)$, $(0, 1)$, $(-0.5, 0)$, $(-1.5, -1)$, 0.7893, $y_p(1) = -0.7794$, $y_p = te^{-t}$, $b = -1.5$, lag 4, $A = \tfrac16$. l9: 1.9365, 3.2446, settling 5.39, 1.56, 2.37, 3.28, 5.73 (b = 1, 3, 4, 5, 8, fine-step solve, step 0.0001), overshoot 44.43% and 2.84% ($\zeta = 0.75$), peak time 1.62, amplitudes 0.25, 0.3162, 0.5, peak 0.5164 at 1.8708, $\ln 2 = 0.6931$, undamped period 3.1416. Review: 16.30%, 3.7622, $b = 6$, $b = -1$. Homework: 1.070645, 0.593994, 0.515599, 0.849426, 0.998922, 0.2079, $A = -1$, 1.2563, $b = 8.5$, lags 1 and 4 days, peak at 6.49 days.

Note for the second reader: the brief's l9 hook says the learner finds the $b$ "that returns to rest fastest without overshooting"; that is $b = 4$. Into a 5% band, $b = 3$ settles sooner (1.56) with a 2.8% overshoot. l9 screen 5 says so plainly and the trap still uses $b = 5$ against $b = 4$.

## Proposed course.json change

None.

## Backlog

One bullet in `docs/BACKLOG-INBOX.md` under "Raised later (odes level 2)".
