# stat-models level 2 (Experiments): author report

Session T, content wave 1. Brief: `docs/briefs/stat-models.md`, preamble and `## Level 2`.

## Files written

| File | Screens / items | Quiz | Notes |
|---|---|---|---|
| `l6-anova.json` | 10 | 3 | hook: twelve draggable orders with live group means, grand mean and a derive caption for SSB, SSW, SST; SSB 24 and SSW 26 by hand; SST = SSB + SSW derivation (distractor: the wrong zero); ANOVA `table`; raw-sum trap; D5 SSB; code `anova_table` (8 tests) |
| `l7-f-test.json` | 10 | 3 | hook: $F(2, 9)$ density (lgamma) with a cut slider on `area.from`; drag one order past the 5% cut; $F(2, 87)$ on D5; ANOVA as regression on dummies (console); $F = t^2$; pairwise trap (14.26%); Bonferroni; code `f_test` + `anova_by_regression`; five-broker transfer |
| `l8-designing-an-experiment.json` | 10 | 3 | confounded choice table; `place` boxes mode (coin per stock-day); power `distribution` with an overlay whose mean follows a slider on $n$ and a hatched `under` region; 1,005 per arm, 24% at 200, SD(D) 5.06, 201 pairs; blocked-then-unpaired trap; sample-size derivation; code `n_per_arm` + `randomise_within_blocks` (10 tests, prelude helper) |
| `l9-execution-experiment.json` | 11 | 3 | D6 `scatter` (compact points); Welch, paired $t$, interval, block fixed effect, sign test (binomial `distribution` with two shaded tails); unpaired trap; peeking `bars` `sim` with ten `let` bindings (seed 3); SPRT `walk` (seed 17) with a frames toggle between no effect and the effect; code `analyse_paired` + `sign_test`; £ transfer |
| `review-2.json` | 9 items, difficulty 2 to 4, `pass: 0.8` | | interleaves all four lessons; `r2-link` recalls level 1's logit link |
| `homework-2.json` | 7 items, difficulty 3 to 5 (two at 5) | | `h-design-sim` code (difficulty 5, `performance: "code"`, 7 tests: `design_and_analyse` and vectorised `false_positive_rate`), `h-var-diff` order derivation, `h-monday-friday` longform (10-point rubric, full model answer) |

Skills: l6 to l8 `sm-anova`; l9 `sm-anova` and `sm-nonpar`. l9's objective starts with "Design" and the course is Stage 2, so the level is rule-matched; the homework's code item is its one performance task (gating).

## Gates

1. Validator: **0 errors** (only "ladder reuses the previous canvas kind" and "point hint" warnings on these files).
2. Voice scan over the course folder: **0 and 0**.
3. Numbers: `python3 docs/reports/stat-models-L2-numbers.py`: **164 of 164 passed**, exit 0. L1's script still passes 266 of 266.
4. Playthrough: four lessons, `--set stat-models/review-2`, `--set stat-models/homework-2`, with `--mobile --tablet --local-cdn <pkgs>`: **all passed** (homework performance starter fails as required; longform marked by the button). Screenshots looked at: the ANOVA hook, the F density with cut, the power canvas, the boxes assignment at 440 (fixed: `cols: 2`), the peeking bars, the SPRT walk (fixed: y range).

## Numbers and their sources

Every planner value was reproduced in Pyodide 0.27.7 (SciPy 1.14.1, statsmodels 0.14.4) run in Node from the local wheels; datasets D5 (seed 41) and D6 (seed 53) are byte-identical between local NumPy and Pyodide. Reproduced exactly: 4, 24, 26, 50, 0.48, 12, 2.889, 4.1538, 0.0527, 4.2565, 2.1402, 2.3032, 6.2310, 321.886, 2,570.214, 5.4478, 0.00590, 2.140226, 4.090789, 0.163008, 0.1113, $-2.1213$, 4.5, 14.26%, 0.911, 0.0041, 0.0064, 1004.66, 1,006 ($t$ version, `TTestIndPower` 1005.62), 5.06, 201, 79.8%, 0.808, 5.4734, 4.3819, $-1.2221$, 0.222, $-1.0915$, 5.5334, $-2.7895$, 0.00579, $(-1.8630, -0.3199)$, 1.9720, 117 of 200, 0.0194, 0.0196, 8.3%, 14.2%, 19.4%, $-1.5581$, 2.7726, 42.9, 61.0, 99.

Differences and choices:
- Power at 200 per arm is 0.23953, so the lessons say **24%** (the brief's 23.9% truncates 23.95%).
- $z_{0.975} + z_{0.8} = 2.801585$, written 2.80159 in the accept line.
- OLS with block fixed effects reproduces the paired estimate and $t$ exactly ($-1.091465$, $-2.789550$); the brief's warning held in practice: a Python variable named `C` broke `smf.ols('... C(algo) ...')` in my own Pyodide check, so l9 says so.
- Peeking `sim` (engine stream, seed 3): **190 of 1,000** false alarms at 10 looks (19.0%); the same stream gives 50, 79 and 139 at 1, 2 and 5 looks. Exact rates by 400,000 NumPy simulations: 5.04%, 8.35%, 14.19%, 19.34% (planner: 0.1935 and 0.1936).
- SPRT `walk` (seed 17, 300 paths, 300 steps): under no effect **14 stop at the top, 286 at the bottom** (4.7% false positives); under the effect **246 top, 53 bottom, 1 undecided** (82.0% power). Read off the rendered canvas; the mean stopping times are in the live caption.
- Added values, each computed twice (hand formula and SciPy in Pyodide, or two seeds): $F$ at $a_4 = 3$ is 9.61 with SSW 14.75; $F(2, 87)$ cut 3.1013; $p(F_{4,55} > 1.8) = 0.142$, cut 2.5397; $P(F_{2,9} > 3) = 0.100$; 252, 1,345, 1,495 per arm; power 50.7% at 500 per arm; homework $F = 7.778$ ($p = 0.0022$); review $F = 2.667$ ($p = 0.062$), 393 per arm, 0.00833; 30 looks about 28%; £218,293 a month (interval £63,980 to £372,606); paired small case $p = 0.0917$; sign test 15 of 19 $p = 0.0192$; the homework code's $p$-values for seeds 1, 2 and 5, and `false_positive_rate` 0.1911, 0.0506, 0.0833, 0.1407 for 10, 1, 2, 5 looks (tests use simulation tolerances of 0.01, 0.003, 0.005, 0.005 round the exact rates).

## Runtime

No L2 code screen imports statsmodels (NumPy and SciPy only, about 10 s on first load, stated in each `how`); the regression and block-effect results are shown in `console` canvases with values computed by statsmodels in Pyodide. Setup lines avoid comprehensions; screens whose setup uses NumPy import it in the starter so Pyodide loads it.

## Proposed course.json change

None.

## Backlog

Four bullets under `Raised later (stat-models level 2):` (boxes cards on a phone; no tool reads canvas `values`; `stops` with `options`; overlay and shade labels colliding).
