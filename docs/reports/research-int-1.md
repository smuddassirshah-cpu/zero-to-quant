# Report: research-int level 1 (Statistics and linear algebra questions)

Author: content agent, 4 November 2026. Brief: `docs/briefs/research-int.md`, shared sections and `## Level 1`. Followed `docs/LEVEL-BRIEF.md` and `docs/AUTHORING.md` (engine pass C: `parts`, `data`, `draw`, drills). Worktree branch `worktree-agent-a7efeff1c20212ead`.

## Files written

All in `app/content/courses/research-int/`, plus the regenerated `app/content/manifest.json`. Generators, checks and probes are in the scratchpad folder `research-int-1/` (`gen/common.py`, `gen/l1.py` to `gen/l5.py`, `gen/sets.py`, `scripts/my_l1_check.py`, `pyo_check.mjs`, `probe_drag.mjs`).

| File | Screens or items | Quiz | Skills | Notes |
|---|---|---|---|---|
| `l1-two-regressions.json` | 10 (problem, ladder, ladder, trap, ladder, generalise, derive, transfer, 2 follow-up ladders) | 4 | rq-stats | hook: `scatter` with a slope control and live sum of squared residuals (fit hidden until the explanation); `state.lines`; follow-up on a `plane` with a noise slider |
| `l2-correlation-limits.json` | 9 (problem, ladder, ladder, trap, problem, generalise, derive, transfer, follow-up ladder) | 4 | rq-stats, rq-linalg | hook: `plane` with a `heat` layer and implicit edge of $\det R$, a `drag-point` locked to $b = 0.8$, live determinant caption |
| `l3-estimators-on-the-spot.json` | 10 (problem, ladder, ladder, trap, ladder, ladder, generalise, derive, transfer, follow-up ladder) | 4 | rq-stats | hook: `bars` sim `maxn(9, u(0, 10))` with `showMean`; a shrunk-coin MSE chart driven by a slider on $p$; an exponential-rate sim |
| `l4-tests-in-words.json` | 11 (problem, ladder, ladder, ladder, trap, ladder, ladder, problem, generalise, transfer, follow-up ladder) | 4 | rq-stats | hook: `distribution` normal with a heads slider shading both tails; exact binomial; power with an overlay and a shaded region under it; a table of correction bars |
| `l5-matrices-on-the-spot.json` | 11 (problem, 4 ladders, trap, ladder, generalise, derive, transfer, follow-up ladder) | 4 | rq-linalg | hook: `matrix` canvas of the 4 × 4 ones matrix with a `table` widget for its eigenvalues |
| `review-1.json` | 9 items, difficulty 2 to 4, `timed` 540 s with `lockAtZero`; R1.2 has three `parts` | | both | every item has `tags`, `skills`, `pace`; paces add to 540 s |
| `homework-1.json` | 8 items, difficulty 3 to 5 (two at 5); H1.2 has three `parts` | | both | `order` derivation (H1.1), Python `code` (H1.3, 8 hidden tests), `longform` with a 10-point rubric and model answer (H1.4) |

Every lesson: `minutes: 15`, the real time and the pace in the first prose ("This lesson takes about 25 minutes, two minutes a question; say your reasoning aloud first"), an interactive canvas on screen 1, one `trap` with a `byKey` line for the blurt, an edge case, a `transfer` in a desk setting, and closing ladder screens titled "The follow-up: ...". l3 and l4 have no derivation in the brief; l3 has a `derive` (the CDF of the maximum) anyway, l4 has none. No lesson has a non-task screen. Every task screen, quiz, review and homework item carries `tags` (family first) and `pace`.

Pace totals (seconds, screens + quiz): l1 1,200 + 270; l2 1,350 + 360; l3 1,800 + 240; l4 1,320 + 270; l5 990 + 195; review 540 (the clock); homework 2,940. The stated lesson times (25, 30, 35, 25, 20 minutes) are these totals rounded.

## Validator, voice and code

- `node tools/validate.mjs` from `app/`: **0 errors** (425 warnings; for research-int only "a point hint usually highlights the canvas" on some numeric screens, one "ladder reuses canvas kind" on l1's last screen, and course.json's not-yet-written levels 2 to 4).
- `VOICE_BASE=<abs>/app/content/courses/research-int python3 docs/reviews/voice-scan.py`: **0 sentences over 20 words, 0 explanations over three sentences** (2,159 sentences). No exclamation marks, em-dashes or listed American spellings (grep).
- H1.3 in Pyodide 0.27.7 (Node, `pyo_check.mjs`, local package): the solution passes 8 of 8 hidden tests and the starter passes 0 of 8. The homework playthrough also marks the item right through the app's worker.

## Playthrough

All with `--local-cdn <scratchpad>/pkgs`.

| Run | Result |
|---|---|
| `--lesson` l1 to l5 (desktop) | all ok: 14, 13, 14, 15, 15 checks; quizzes 4/4 each |
| `--set research-int/review-1` | ok: timed 540 s locks at zero; timed parts check ok; recorded 9 of 9 |
| `--set research-int/homework-1` | ok: 8 of 8 right, 38 of 38 marks; parts check ok (draft keeps open parts, part credit in marks) |
| the same with `--mobile` (and `--shots`) | all ok |
| `--why` on every lesson and both sets | all ok; explanation sheets inspected |

Probe (`probe_drag.mjs`, keyboard steps on the l2 hook): $c = 0.285$ passes (`ok: true`) and $c = 0.200$ fails with key `outside`, as the brief asks.

Fixes made from the screenshots: the l2 plane with `equal: true` drew at about twice the type size with labels on the ticks (now no `equal`, axis labels `b` and `c`, named in the prose); the hook point label sat on the vline label (point label removed, start at $c = 0.6$); l2 and l3 derive lines with wide KaTeX (a `pmatrix`, a long root identity, an integral with `\dfrac`) pushed the order list past 390 px and hid the remove buttons (lines shortened, the l3 chain split into five lines); the l4 corrections table scrolled at 390 px (now `compact` with short headers, named in the caption); the l3 simulation questions had a tolerance tighter than the 1,000-trial sampling error (a seeded run shows 2.557 for an exact 2.5; tolerance now 0.1 on both sim readings, and the explanations give the exact values).

## Numbers and their sources

Brief numbers were recomputed with the brief's `l1_stats_linalg.py` (ALL AGREE) and the level 1 part of `items_check.py` (ALL AGREE), run with SciPy 1.18.1, statsmodels 0.15.0 and NumPy 2.5.4 installed into the scratchpad (the system Python lacks SciPy). Every number I added or changed is in `research-int-1/scripts/my_l1_check.py`, each by a hand formula and a library call or seeded simulation (ALL AGREE).

- l1: five points: means 3 and 6, $S_{xx} = 10$, $S_{yy} = 40$, $S_{xy} = 16$; slopes 1.6 and 0.4 (drawn 2.5, $y = 2.5x - 1.5$); intercepts 1.2 and 0.6; $r = 0.8$, $r^2 = 0.64$; SSE through the means $40 - 32m + 10m^2$ (18 at $m = 1$, 14.4 at 1.6); $r = 0$ points (1, 4), (2, 8), (3, 6), (4, 8), (5, 4) with $S_{xy} = 0$; beta 1.0 and reverse 0.25; duplicated data (brief's seeded $y$): slope 0.7915, $R^2$ 0.7548, $t$ 4.962 to 7.443, p 0.0011 to $6.7 \times 10^{-7}$; attenuation $8/5 = 1.6$. Quiz: 1.0; $2.1\sqrt{10/4} = 3.32$; $9/12 = 0.75$; $0.25 \times 2 = 0.5$, $|r| = 0.707$. Generalise example 0.3 and 1.2 ($r = 0.6$).
- l2: ranges $[0.28, 1]$, $[-0.02, 1]$ ($a = b = 0.7$), $[-1, -0.62]$, $[0.62, 1]$, $[-0.5, 1]$; equicorrelation floors $-1/2$ ($n = 3$), $-1/4$ ($n = 5$), $-1/5$ ($n = 6$); vendor determinant $-1.68$, smallest eigenvalue $-0.5471$. Quiz: 0.4585 ($0.9, 0.8$), triple determinants $-0.16$, 0.14, 0.19, 0.11; $c = 0.3$ when $a = 1$.
- l3: $E[M] = 9$, Var 0.8182, fix 1.0101, MSE 1.8182, $\operatorname{Var}(2\bar x) = 3.7037$; $7.2 \to 8.0$; divisor table bias 0, $-0.1$, $-0.1818$ and variance 0.2222, 0.18, 0.1488 (MSE 0.2222, 0.19, 0.1818); coin MSE 0.025 and 0.01736 at $p = 0.5$, crossing points $p = 0.1381$ and $0.8619$; $E[1/\bar x] = 2.5$; auction £6.30 to £7.00 (the nine prices average £4.71, so twice the mean is £9.42). Quiz: 10, divisor 31, MSE 0.09, $4/5$. Sim exact values: the max sim converges to 9 and the rate sim to 2.5.
- l4: $z = 2$; normal two-sided 0.0455 (one tail 0.0228); exact 0.0569 (one tail 0.0284); power 0.7054 (cut-off 0.392), $n = 32$ for 80% (31.4, power 0.8074); ten tests 0.4013; Bonferroni 0.005 and 0.0025; Sharpe $t = 2$; corrections 2, 3, 4; best of fifty $p = 0.0027$, $\times 50 = 0.135$, Šidák 0.1264; $p = 0.04$ shading at $\pm 2.054$. Quiz: power 0.516, 0.00125, $t = 2$.
- l5: $J_4$ eigenvalues 4, 0, 0, 0; $uu^\top$ 9; $uv^\top$ 11; equicorrelation 2.2 and 0.7, squares 6.8; reflection $-1, 1, 1$ ($9H$ entries checked); $I + J_3$ 4, 1, 1; rotation $\pm i$; $(2, 1; 1, 2)$ gives 3 and 1; share 44%; det 0.52822. Quiz: 5, 25, trace 2, 0.5.
- Review: R1.1 0.4; R1.2 0.7746, $\sqrt{18/38} = 0.6882$; R1.3 0; R1.4 determinants 0.024, $-0.06$, 0.024, 0.342, $-0.026$; R1.5 9.0; R1.6 16 (MSEs 0.1429, 0.1289, 0.125); R1.7 0.6415; R1.8 counts 1, 3, 4; R1.9 3.0.
- Homework: H1.2 $-0.28$, $-0.3324$, $-1/3$; H1.3 tests as the brief ($n = 10, 15, 20$; 7.0); H1.4 1.5, 0.7854, 0.0017; H1.5 6, 7, 2.5, 1; H1.6 $[-4, 8]$; H1.7 1.5; H1.8 0.0107 (bias $-0.0667$, variance 0.00625).

## Departures from the brief

AUTHORING and the brief agree on `parts` (credit per part, each opening after the previous is checked, unopened parts missed at a timed lock); no conflict to resolve. The departures below keep a review or homework item from repeating a lesson screen's exact numbers, so it tests the method rather than recall:

- R1.2 (c) uses $n = 20$ ($\sqrt{18/38} = 0.6882$); the brief's $n = 10$ ratio 2/3 is stated in the l1 follow-up.
- R1.6 uses $n = 15$ (best divisor 16); $n = 10$ is the l3 trap.
- R1.8 uses new p-values (0.001, 0.011, 0.014, 0.038, 0.3: Bonferroni 1, Holm 3, BH 4); the brief's set is the l4 table.
- R1.9 uses $n = 6$, $\rho = 0.4$ (3.0); $n = 5$, $\rho = 0.3$ appears on four l5 screens.
- H1.1 orders the $r\,s_y/s_x$ route with the equality case; the l1 derive already orders the $S_{xy}$ route.
- H1.2 (a) and (b) use $a = b = 0.6$ and $(0.8, 0.3)$; the brief's $(0.8, 0.8)$ is the l2 hook and $(0.8, 0.6)$ is R1.3.
- l2: the second worked screen uses $a = b = 0.7$ (floor $-0.02$) and the transfer is the vendor matrix alone, since the desks' 0.6 and 0.8 are R1.3; the follow-up asks five assets ($-1/4$) because H1.2 (c) asks four.
- l4: the multiple-testing screen uses ten tests (0.4013) because R1.7 asks twenty; power is drawn on one `distribution` with an overlay and a region shaded under it, not a `pair`, so both curves share one axis.
- l1: the generalise example of a possible pair is 0.3 and 1.2, since R1.2 (a) asks 0.5 and 1.2; the hook hides the fit and adds a slope control so the learner finds 1.6 before it is drawn.
- Homework order: the item with parts is item 1, because the playthrough's homework parts check reads item 1 (backlog bullet).

E3 example draws for the exam author, unchanged from the brief: `{ "from": "bank/research-1", "tags": ["two-regressions"], "difficulty": [2, 3], "n": 2 }` and `{ "from": "bank/research-1", "tags": ["special-eigenvalues"], "difficulty": [2, 4], "n": 2 }`. No level file contains a `draw`.

## Conventions

No seeds or data files in this level (every dataset is an inline list). Canvas sims are seeded: l3 hook seed 31, rate sim seed 32. Families used as first tags: two-regressions, duplicated-data, measurement-error, correlation-bounds, psd-check, max-of-uniform, estimator-bias, variance-divisor, shrinkage-estimator, p-value-meaning, power, multiple-testing, special-eigenvalues, rank-one, equicorrelation.

## Proposed course.json change

None.

## Backlog

Six bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (research-int L1, 4 Nov)".
