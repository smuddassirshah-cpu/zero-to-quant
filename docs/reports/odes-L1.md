# odes level 1: First-order equations

Author: content agent (odes L1 to L3 wave). Brief: `docs/briefs/odes.md` `## Level 1`.

## Files

| file | screens / items | quiz | notes |
|---|---|---|---|
| `l1-equations-about-rates.json` | 11 screens | 4 | hook: candidate curves (`exprs` + `options` control) with a tangent against $0.05B$; `code` residual |
| `l2-separable.json` | 10 screens | 4 | `manipulate` separation, logistic `order` derivation with a distractor, `code` logistic |
| `l3-integrating-factor.json` | 10 screens | 4 | product rule backwards on a `table`, trap with wrong curves as option patches, `code` linear_const |
| `l4-slope-fields.json` | 10 screens | 4 | `slopeField` + dragged `trajectory`; phase lines as a one-column `field`; trap on `tap-regions` |
| `l5-mean-reversion.json` | 10 screens | 4 | sliders on $r_0$, $\kappa$; area for the average; `walk` `model: "ou"`; `code` vasicek |
| `review-1.json` | 9 items | | difficulty 2 to 4, every lesson |
| `homework-1.json` | 9 items | | difficulty 3 to 5; `h-fit-kappa` is the performance task (`code`, difficulty 5); `h-derive-vasicek` order derivation; two phase-line items; `h-colleague` longform, 10-point rubric |

Performance task: the level is rule-matched (l1's objective starts "Write"), so `h-fit-kappa` carries `"performance": "code"` (5 hidden tests, 1 example).

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; no warnings on any odes level 1 file (only "not yet written" for later levels).
2. `VOICE_BASE=app/content/courses/odes/ python3 docs/reviews/voice-scan.py`: 0 explanations over three sentences, 0 sentences over 20 words (1,983 scanned).
3. `python3 docs/reports/odes-L1-numbers.py`: 0 failures, exit 0. Each number is computed by its closed form and by an independent route (a 20,000-step RK4 solve of the ODE, a direct log-sum, a finite difference or a trapezoid integral).
4. Playthrough with `--local-cdn`: all 5 lessons, review-1 and homework-1 green with `--mobile` (desktop and 440 px) and without it. Homework: "9 of 9 right, 1 performance starter fail, 1 longform marked by the button".

Screenshots read in `scratchpad/odes-L1/shots`. Fixed after reading them: l4 phase lines (arrows hidden under the y axis; moved the column to $x = 3$ with `spacing: [3, ...]` and drew $f(y)$ sideways on the left), the `walk` level label (KaTeX not rendered; now "θ = 4%"), one prose line in l2 screen 2.

NumPy load time: not timed on its own. A whole lesson with its code screen plays in 25 to 31 s with the local CDN.

## Numbers (source: the script; closed form and RK4 agree in every case)

l1: £1,051.27, £1,648.72, £1,050.00, £1,051.16 (monthly), £1,051.27 (daily), residual 4, $e$ (2.718281828 residual of $e^t$), $C = 2$, $r' = -0.01$, $e^{-0.2} = 0.8187$, $\ln 1.05 = 0.0488$.
l2: £81.87, £82.19 (yearly), £1,083.29, £1,061.84 and £1,105.17 (distractors), 5,505.21, 11,023.18, 2.7465, 5.4931, $y(0.5) = 2$, blow-up at 0.5 from $y(0) = 2$, 0.9231, 73.105858 and 88.079708 (code test).
l3: £15,569.31, £3,569.31, 11.5525 (11.55), £65,014.12, 8.33, 13.8629, 0.6839, 0.4192 and 0.5518 (wrong curves at $t = 1$), £125, £4,100, 0.3679, 3.
l4: 0.3679, 1.0017, $f'(1) = -2$, $f'(K) = -0.8$, market share $f'(0.3) = 0.21$, $f'(0) = -0.3$, $f'(1) = -0.7$, $f'(2) = -2$ for $y(2 - y)$.
l5: 5.2131%, 4.7358%, 1.3863, 2.7726, 4.7343%, 4.1642%, 0.998018, 0.001982, expected rate after 252 days 5.2131%, 0.3466, 0.5493, 1.26, 5% after two half-lives from 8%, doubling time 3.47 for $\kappa = -0.2$.
Review: 5.4366, 1.2642, 0.4621, 2.1972, 4.3944, £60, 28.6. Homework: 2.7183, 4.25, 1.5708, 15.67, 12.5, planted $\kappa$ 0.5, 2 and 1.2.

Conventions: rates as decimals in maths, per cent in prose; `numeric` with `unit: "%"` keys the fraction. The `walk` uses seed 3, 504 daily steps, `theta` $= 1 - e^{-0.5/252}$, `sigma` 0.0006 a day.

## Proposed course.json change

None.

## Backlog

Three bullets in `docs/BACKLOG-INBOX.md` under "Raised later (odes level 1)".
