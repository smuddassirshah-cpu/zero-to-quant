# Concept audit, round 2: odes level 4 (Transforms and numerical solution)

Blind read of `l14-laplace-transform`, `l15-solving-with-laplace`, `l16-euler-method`, `l17-runge-kutta`, `l18-four-decimal-places`, `review-4` and `homework-4` (with its two performance tasks) in `app/content/courses/odes/`. No earlier review, audit, ledger, concepts script, author report or git history of the course folder was opened before the blind commit.

- Ledger: `docs/reports/audit-odes-4-r2-ledger.md`. 244 rows: 240 correct, 1 wrong, 3 imprecise, 0 misleading, 0 unverified.
- Script: `docs/reports/odes-L4-concepts-r2.py`. 116 checks. It exits 1 on the four FINDING checks below and passes the other 112.
- Environment for code and console lines: CPython 3.13, NumPy 2.2.6, SciPy 1.14.1 (the app runs Pyodide 0.27.7 with NumPy 2.0.2 and SciPy 1.14.1).

## What was run

Every code widget's solution was run against its hidden tests, and its starter was run to confirm it fails. Every console canvas line with a `>>>` prompt was executed against the taught solution and compared digit for digit. All 15 console outputs match, including the two SciPy lines. The slipped `rk4_step` in l17 was run separately: 2.71613 and order 1.979 both hold.

Stated error sizes, orders and step counts were recomputed: Euler's errors and fitted slope 0.964, RK4's ratio 15.35, the stability roots 2 and 2.7853, the 63-step radii, 163 as Euler's true minimum, and 4 as RK4's true minimum on the lesson's system (three steps err by $52.8 \times 10^{-6}$). The Vasicek convexity factor $4.643\sigma^2$ was derived from the variance of the integrated rate and confirmed by a Monte Carlo of 200,000 paths. The Laplace rules were read against their conditions: every table row carries its region, the derivative rule states its limit hypothesis on the line that uses it, and the residue formula states distinct poles and a proper fraction.

## Findings

1. `l17-runge-kutta.json` | `screens[5].canvas.state.caption` | **wrong, minor** | The caption says "Orange: Euler's 63 steps." Euler's path is drawn green. | The Euler polyline has `colour: 3`. The plane canvas maps a colour slot to `var(--s<n>)`, and `app/css/tokens.css` sets `--s3` to #1BAF7A (green; #199E70 in the dark theme). Orange is slot 2. No orange curve is on the chart, so the caption names a curve that is not there. The curve labels still identify the paths, so no concept is lost. | Replace the caption with: `Green: Euler's 63 steps. Blue: RK4's 63 steps.`

2. `l18-four-decimal-places.json` | `screens[6].explain.text` and `screens[6].feedback.correct` | **imprecise, minor** | Both argue the failure from the printed digits: "0.789080 prints as 0.7891 against 0.7892, so the fourth decimal is wrong." The lesson's own test is the band, and screen 3 says printed digits can differ inside it. | Screen 3: "0.789255 is inside the band and prints 0.7893." By that screen a differing print does not show a failure. The failure here is the error, $1.35 \times 10^{-4}$, against a band of $5 \times 10^{-5}$. | `explain.text`: `The error is $1.35 \times 10^{-4}$, 2.7 times the band, so monthly Euler fails. Here the print differs too: 0.7891 against 0.7892. Euler is first order, so it takes 163 steps, not 60, to meet the band.` `feedback.correct`: `The error in $D$ is $1.35 \times 10^{-4}$, outside the band of $5 \times 10^{-5}$.`

3. `l16-euler-method.json` | `screens[7].prose` | **imprecise, minor** | "At $h = 0.05$ the factor is 0.5; at $h = 0.1$ it is 0" follows two sentences about a general $\lambda$ and $\mu$. It holds only for $\lambda = 10$, which the prose does not say. | $1 - h\lambda$ is 0.5 at $h = 0.05$ only when $\lambda = 10$. The canvas label and the question do use 10, so a careful reader recovers it. | Replace the sentence with: `With $\lambda = 10$, the factor is 0.5 at $h = 0.05$ and 0 at $h = 0.1$.`

4. `l18-four-decimal-places.json` | `screens[7].prose` | **imprecise, minor** | "Then the price gains a factor $e^{\frac12\mathrm{Var}(I)}$, because $e^{-I}$ is convex." Convexity gives the direction only. The exact factor holds because $I$ is normal in Vasicek. | For normal $I$, $E[e^{-I}] = e^{-E[I] + \frac12\mathrm{Var}(I)}$. Jensen's inequality alone gives $E[e^{-I}] \ge e^{-E[I]}$ with no formula for the gap. Brigo and Mercurio, *Interest Rate Models*, 3.2.1. The number $4.643\sigma^2$ is right (script, with Monte Carlo). | Replace the sentence with: `Then $I$ is normal, so the price gains a factor $e^{\frac12\mathrm{Var}(I)}$; here it is $e^{4.643\sigma^2}$. The factor is above 1 because $e^{-I}$ is convex.`

No finding needs more than a sentence or two; no screen needs a rewrite.

## Read and found sound (points the task asked for)

- Console lines: all printed digits match the taught code (list in the script output).
- Orders and halving: "close to 2" (1.92) and "close to 16" (15.35) are stated as measured ratios, and the keys grade the measured value. Summaries say "about 16".
- Agreement to four decimals: defined once as a band on $D$, with the rounding-edge caveat. Step counts 163, 256 and 4 are each said with their meaning (true minimum, doubling sequence, true minimum).
- Stability: $h < 2/\lambda$ and $h\lambda < 2.7853$; $|R| < 1$ holds on the whole open interval, so "below" is exact.
- Laplace: regions of convergence on every table row and in the trap; starting values in both derivative rules; the transfer screens use only $s$ inside the region.
- Homework `h-match-4dp` uses the system $(r, D)$ where the lesson uses $(r, I)$. Its stated counts (8, 16, 16, `None`) are right for its own system.

## Overlap with earlier reads

Read after the blind commit (`2a75a37c`): `docs/reviews/review-odes-4.md` (second read and its fix pass: 13 findings, 8 of them conceptual), `docs/reviews/audit-odes-4.md` (round 1: 10 findings, 3 wrong, 6 imprecise, 1 misleading, with its fix pass), and that file's fix-pass read (2 imprecise, both fixed).

| | count |
|---|---|
| Conceptual findings by this audit only | 4 |
| Conceptual findings by earlier reads only | 20 (review 8, audit round 1 10, fix-pass read 2; all fixed before this read) |
| Found by both | 0 |

`wrong` in this round: 1 (finding 1, minor). It is new: no earlier read mentions the caption's colours.

Notes on the four:

- Finding 1 (colour caption): original text, not fix-pass text. Three reads passed it. No read before this one compared a colour word with the slot drawn.
- Finding 2 (l18 `screens[6]`): round 1's finding 1 looked at `screens[6].feedback.correct` while fixing `screens[3]` and left it, "because it is true of that value". That is right as a fact. This audit's point is narrower: after the fix to `screens[3]`, the explain's "so" argues the failure from the print, which the new `screens[3]` text says is not the test. It is a judgement call and the lowest priority of the four.
- Finding 3 (l16 `screens[7]`): the review and round 1 both edited this prose (stiffness, "shrink", the eigenvalue sentence). The eigenvalue sentence the review added now sits between the general rule and the two numbers, which is what detaches them from $\lambda = 10$.
- Finding 4 (l18 `screens[7]`): round 1 noted the Vasicek pricing drift here and checked the number by Monte Carlo, but did not raise the "because convex" wording.

All earlier fixes were re-read in place and hold: the rounding-edge caveat, the `solve_ivp` prefix `0.0141640489531...`, the corrected console digits, $R(3)$, the six "Below what step" questions, "piecewise continuous", "of lower degree than den", the `steps_to_4dp` caveat, "In these tests", the content-named feedback in `h-which-exist`, the `f"{d:.2e}"` console and the three `2.718279744135166` keys. This read found no `wrong` in fix-pass text.

## Gates

- Validator: 0 errors (4,666 warnings; manifest unchanged).
- Playthrough with `--local-cdn`, desktop and `--mobile`: all five lessons, `review-4` and `homework-4` report "All passed".
- `docs/reports/odes-L4-concepts-r2.py`: exit 1 (4 FINDING checks fail by design, 112 pass).
- `docs/reports/odes-L4-numbers.py`: exit 0.
- `docs/reports/odes-L4-concepts.py` (round 1): exit 0.
- Inbox: two bullets under "Raised later (audit odes):" in `docs/BACKLOG-INBOX.md`.
