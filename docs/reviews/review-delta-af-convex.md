# Delta read AF, convex: the three re-authored problems and the parts the two fix passes changed

Counts: `wrong` 0, `misleading` 0, `reuse` 2, `re-author` 0, `continuity` 1, `voice` 0, `other` 0. No key, no `wrong` value and no printed number in scope is mistaken. None of the three new problems is a retelling. All 27 findings of the two second reads are closed as their fix passes say.

Scope, at commit 962ba05f (fix passes e55a0144, c921270e, 42c17099 and 962ba05f against 6173fdf0):

- New, whole: `problems-1` `p-account-target`, `problems-3` `p-style-fit`, `problems-4` `p-curve-fit-backtrack` (parts 1 and 2 kept, with findings 1 and 2 of the level 4 read; parts 3 to 5 new).
- Changed lines, found by a JSON-path diff against 6173fdf0: `p-shortfall-and-fee` 15, `p-two-futures-hedge` 14, `p-parking-cash` 4, `p-whole-blocks` 3, `p-three-strategies` 6, `p-capital-price` 2, `p-variance-limit` 2, `p-sale-horizon` 7, `p-variance-log` 12. The counts match the findings one for one, and no other path changed.
- Exams read for reuse: `exams/topic-2.5.json` (the 14 convex items) and `exams/stage-2.json` (`c-kkt-hand`, `c-kkt-code`, `c-dedication-lp`, `c-convex-functions`, `c-projected-step`). `topic-1.3`, `topic-1.5`, `topic-1.7` and `topic-3.2` use the word convex but hold no item of this course; no mock exam holds a backtracking, style-fit or square-root item.

Method. Each part in scope was solved from its text before its key was read. No browser, no content or engine edit.

- `docs/reports/delta-review-delta-af-convex-numbers.py` imports no earlier script. Routes: a central second difference; 20,000 random chords for the convex set; SLSQP from four starts and a 600,001-point grid in the original variables $x, y$ at targets 12, 30, 45 and 60; exact fractions for $T^2/45$; 12 months of data built from the symmetric square root of the Gram matrix (the author used its Cholesky factor), then SLSQP with bounds on the data and on the quadratic form from three starts, and the three active sets by hand; a real backtracking loop on the two-variable quadratic that records every trial; a fixed-step loop on both errors; `linprog` on each level 2 programme; exact fractions for the logged variances. Each band is rebuilt with the engine's rule (a bare number divided by 100 under `unit` "%", $10^{-9}$ of slack) and fed 57 typed strings.
- Expression parts: 21 typed forms were run through the real widget code (`grade-all.mjs` on a copy with the forms as `wrong[]` entries). Taken: $-\tfrac{3}{2x\sqrt{x}}$, $-\tfrac{3}{2\sqrt{x^3}}$, $-1.5x^{-3/2}$, $-\tfrac{3}{2x^{1.5}}$, $\tfrac{5T^2}{225}$, $(\tfrac{2T}{15})^2 + (\tfrac{T}{15})^2$, $\tfrac{2T^2}{90}$, $\tfrac{t^2}{45}$ and nine more. Refused: the key plus 0.001, $\tfrac{T^2}{44}$, $0.0222T^2$.
- Fixes applied: each replacement text of the two reviews was searched for in the sets by a script (65 lines found word for word; the 13 not found belong to the replaced problems), and each changed number was recomputed.
- Reuse: the screens, quiz, review, homework and exam items named in the table below were read in full with their slip, hint and `why` lines. A scratch script listed every run of six words (maths and numbers masked) that a string of a new problem shares with the course, its exams, the other sets, or another new problem.

## Tool results

| check | result |
|---|---|
| author's `problems-convex-numbers.py` | 818 of 818, `numbers_lib` failures 0, exit 0 |
| readers' scripts | `problems-convex-numbers-read.py` 683 checks, 0 FINDING; `problems-convex-4-numbers-read.py` 118 checks, 0 failed; both exit 0 |
| this read's script | 331 checks, 0 failed, 3 FINDING rows, exit 0 (a row prints `resolved` once fixed) |
| validator | 0 errors, 4585 warnings; on these sets four `O2-long-sentence` (the three keeps of set 3 and finding 14(b) of set 4) and two `[wrong-band]` (ruling a); `manifest.json` restored |
| voice scan 35, course folder | 0 and 0 |
| `fresh-check.mjs --file` | 0 hits on each of the four sets; advisories as the fix passes list (set 3: 0.01, 0.04, 0.005; set 4: 0.05 and 0.06, and the Armijo formula of l14 screen 8) |
| `grade-all.mjs --file` | 15, 14, 15 and 13 widgets, 0 failures |
| scratch copy with findings 1 to 3 applied | `fresh-check --content` 0 hits on sets 3 and 4, the same advisories; `grade-all` 0 failures; voice 0 and 0; this script 331 checks, 3 rows `resolved`; copy dropped |

## Rulings asked for

**(a) The two `[wrong-band]` warnings on set 4: the bands are right and the rule is wrong here.** `times-s` (0.075, $\pm 0.0005$, under "Give a whole number") and `thousands` (0.0793, $\pm 0.005$, under "to the nearest pound") are slips in another unit. A learner who makes them types the value as it stands; rounded "as asked" each is 0, which nobody types. The band the rule wants, $\pm 0.5$, is the one the level 4 read removed: it took 0.5, 0.04 and 0.3 for `times-s`, and 0.311 and 0.568 (two other slips given in £k) for `thousands`. As narrowed, `times-s` takes 0.075 only and `thousands` takes 0.08, 0.079 and 0.0793 and refuses 0, 0.311 and 0.568 (script, C2 and D8). Keep both bands. The rule should skip a slip whose value rounds to 0 at the asked places while the slip itself is not 0. The fix pass's inbox bullet says so already; one line is added under this read's heading with the exact condition.

**(b) `p-capital-price` part 5 and `p-variance-limit` part 5: the parts stay; one explain line changes (finding 3).** Both multiply a multiplier by a small change, which is l13's one standard task, and l13 is drawn on by these two parts only. They are not the same step told twice. The first takes a price from a minimised dual function and returns a total in £k, with a band that also takes the re-solved 42.04; its slips are the trial price and a per-desk double count. The second takes $\mu$ from a KKT row and returns a rise in basis points; its slips are a division and the bare step. Since `p-no-borrowing` became `p-style-fit`, which ends on a fit figure, one problem in three no longer ends this way, which is what finding 20 asked for. No key, question or slip needs to change. What a learner would notice is the wording: both explain lines run estimate, "adds about", "Re-solving", reason, which is the frame of l13 screen 3's explain, and the second shares a six-word run with it. Finding 3 rewrites that one line; `p-capital-price` keeps its own.

## Verdict per problem

| problem | closest lesson screens | closest quiz, review, homework, other set, exam | verdict |
|---|---|---|---|
| p-account-target | l2 S3 ($f''$ of $-\ln x$, slips `sign` and `first`), l4 S1 (a $\ge$ moved across), l4 S4 (logs turn $xy \ge 1$ into a convex function at most 0), l3 S5 | `q4-disguise`, `r1-floor`, `r1-compose`, `h1-sublevel`, `h1-sharpe`; `p-two-futures-hedge` part 5 (a limit held, then one variable); `e-convex-sets`, `e-projection-kkt` and `e-solver-certificate` (a bowl over a half-plane), `c-convex-functions` | `clean`. Part 2 is l4 S4's move on another function: l4 S4 key "$-\ln x - \ln y \le 0$, a convex function at most 0", set key "$30 - 6\sqrt{x} - 3\sqrt{y}$ is a sum of convex functions, and the plans are where it is at most 0". That is the level's standard task, and here the sign comes from part 1. The square-root change of variables, the plan along the active limit and $T^2/45$ are in no file. `e-projection-kkt` reaches a nearest point by KKT rows and a normal; this problem substitutes, and shares no line with it. One line shared with `p-style-fit` (finding 2). |
| p-style-fit | l12 S2 and `q12-qp` ($\mathbf{Q} = 2\boldsymbol{\Sigma}$), l12 S3 (active limits at a solver's answer), l12 S9 (a tracking QP), l11 S0 (a quadratic along the target line), l11 S9 (a floor that does not bind) | `q10-slack`, `r3-kkt`, `h3-frontier`, `h3-cap-kkt`; `p-account-target` part 3; `c-kkt-hand`, `e-long-only-kkt`, `e-slsqp-sign` | `clean`. A QP built from regression sums is new to the course, no multiplier is solved, and the end is a fit figure. `q12-qp` asks for $\mathbf{Q}$ and $\mathbf{q}$ of $\mathbf{w}^T\boldsymbol{\Sigma}\mathbf{w} - 2\mathbf{m}^T\mathbf{w}$ as a choice; part 1 asks for one entry from six sums, with its own two slips. One line shared with `p-account-target` (finding 2). |
| p-curve-fit-backtrack | l14 S0 and S2 (factor $1 - s\lambda$), l14 S8 (backtracking in order; "the test passes once $s \le 1/L$"), l15 S2 (a count from a rate) | `q14-armijo` ($2x^2$ at $x = 1$, accepts 0.25), `r4-factor`, `r4-count`, `h4-rho`; `p-variance-log` part 3 (a count, in the same set); `e-step-limit`, `e-rate-from-kappa` | `clean`; `continuity` (finding 1). `q14-armijo`: "tries $s = 1$ and halves on failure ... Which step does it accept?" Set: "trial step 1, halved until ... which step does the test accept at step 40?" The rule and the question are the quiz's, as they must be; the quiz runs it once in one variable. Here it runs twice in two variables, accepts a step 7.5 times the fixed-step limit and then a sixteenth of it, and is priced in fixed steps. No balanced step, no $\rho$ from $\kappa$, no count to a power of ten: the walk of the old parts 3 to 5 is gone. |

The three compared with each other. `p-curve-fit-backtrack` shares only house frames with the other two ("Using ... from part n", "steps of parts 3 and 4"). `p-account-target` and `p-style-fit`, by one author, share one step (a linear equality substituted, then a parabola in one variable) and the frame of its `correct` line (finding 2). Their stories, numbers, chains and last parts are different, and the step is l11 screen 0's standard one.

## Findings

1. `problems-4.json` | `items[0].prose`, `items[0].parts[2].question`, `items[0].parts[3].feedback.byKey.keep`, `items[0].parts[4].question` | continuity | The stem's step number does not agree with its own factor. The log has the level error halving each step, and "At step 40" the level gradient is 0.06, an error of 0.002. Forty halvings back, that error was $0.002 \times 2^{40} \approx 2.2 \times 10^{9}$, beside a decay-rate error of 2.56. A learner who checks the log against the gradient finds a level error that should have been gone thirty steps earlier. No key or printed number depends on the step number. | Script, FINDING 1. At step 4 the start errors are $0.5/0.96^4 = 0.589$ and $0.002 \times 16 = 0.032$. | Replace "step 40" by "step 4" in all four strings, and nothing else. `prose`: "... a factor of $-0.5$. At step 4 the gradient is $(0.4, 0.06)$, decay rate first. ..."; `parts[2].question`: "Using curvatures 0.8 and 30 from parts 1 and 2, which step does the test accept at step 4? Give a decimal."; `parts[3].feedback.byKey.keep`: "0.5 suited step 4, not this point. From errors 0.3 and $-0.028$ it multiplies the level error by $-14$ again, and the excess rises to about 2.32."; `parts[4].question`: "The two backtracking steps of parts 3 and 4 take the excess from 0.10006 to about 0.0343. From step 4, how many steps of the fixed $s = 0.05$ would bring it as low? Give a whole number." Tested in a copy: 0 hits, 0 failures, voice 0 and 0. The author's script should be searched for "step 40".

2. `problems-3.json` | `items[1].parts[1].feedback.correct` | reuse | Two new problems of one author give the same step the same sentence. | `p-account-target` part 3: "Along the line the spend is $u^2 + (10 - 2u)^2$, with slope $2u - 4(10 - 2u) = 10u - 40$. It is 0 at $u = 4$, so $x = u^2 = 16$ and $v = 2$." `p-style-fit` part 2: "Along the budget $S = 100\beta_G^2 - 140\beta_G + 60$, with slope $200\beta_G - 140$. It is 0 at $\beta_G = 0.70$, so $\boldsymbol{\beta} = (0.3, 0.7)$." The checker reports neither (Engine 2). Script, FINDING 2. | `problems-3` `items[1].parts[1].feedback.correct`: "With $\beta_V = 1 - \beta_G$ the sum is $S = 100\beta_G^2 - 140\beta_G + 60$. Its derivative $200\beta_G - 140$ vanishes at $\beta_G = 0.70$, so $\boldsymbol{\beta} = (0.3, 0.7)$." Tested in a copy: 0 hits, 0 failures, voice 0 and 0. Set 1 stays.

3. `problems-3.json` | `items[2].parts[4].explain.text` | reuse | The explain keeps the frame of l13 screen 3's, and `p-capital-price` part 5 in the same set has it too (ruling b). The first read replaced this part's generic line (finding 19) and left the explain. | l13 S3 explain: "The multiplier is the slope $dV^*/dr$ at 8%, so a step of 0.002 adds about 0.002571. Re-solving gives $\tfrac{2749}{78750} \approx 0.034908$, a rise of 0.002765". Set: "$\mu$ is the return gained per unit of extra variance, so 0.0002 more variance adds about 0.0003. Re-solving gives $w \approx 0.405$ and a rise of 2.98 basis points. The estimate is close because the step is small." `p-capital-price` part 5: "... so £0.3m adds about 1.4. Re-solving at £6.3m gives a price of 4.47 and a profit of £42.04k." Script, FINDING 3. | `items[2].parts[4].explain.text`: "The loosened limit $V(w) = 0.0162$ is met at $w \approx 0.405$, where the return is 2.98 basis points higher. The multiplier's 3 is within 0.03 of that, with no quadratic to solve. Over so small a step $\mu$ barely moves, from 1.5 to 1.48." Checked: $w = 0.40496$, rise 2.977 basis points, $\mu = 0.06/V'(0.40496) = 1.477$. Tested in a copy: 0 hits, 0 failures, voice 0 and 0.

## Verified with no finding

`p-account-target`.
- $\tfrac{d^2}{dx^2}6\sqrt{x} = -\tfrac32x^{-3/2}$ by a second difference at five points. $N$ is concave and $\{N \ge 30\}$ convex on 20,000 random chords. The counterexamples hold: $\max(x, y) \ge 1$ with $(1, 0)$, $(0, 1)$ and their midpoint; $x^2 \ge 1$ with the gap. ($\max$ rises only weakly in each variable; the line's point, that rising does not give a convex set, stands.)
- SLSQP in $x, y$ and the boundary grid both give $(16, 4)$ and £20k. The slope $10u - 40$ is right. Slips: 4 is $u$, 25 is $(30/6)^2$, 100 is $u = 10$ from $2u + 2(10 - 2u) = 0$; 16, 6 and 25 in part 4.
- $T^2/45$: exact with $u = \tfrac{2T}{15}$, $v = \tfrac{T}{15}$, and SLSQP at $T = 12, 30, 45, 60$. 20 at 30 and 80 at 60. $\tfrac{2T}{3}$, $\tfrac{T^2}{36}$ and $\tfrac{T^2}{9}$ are the three slips their lines name, and $\tfrac1{45} < \tfrac1{36} < \tfrac19$.

`p-style-fit`.
- The six sums are possible: the Gram matrix of $(r, v, g)$ is positive definite. $\mathbf{Q} = \begin{pmatrix}120 & 40\\ 40 & 160\end{pmatrix}$, $\mathbf{q} = (-60, -120)$, and the expanded $S$ agrees with the sum over 12 built months at five points.
- Along the budget $S = 100\beta_G^2 - 140\beta_G + 60$ exactly; minimum at 0.7 (fractions and a grid). No budget: $(\tfrac{3}{11}, \tfrac{15}{22})$, sum $\tfrac{21}{22} = 0.95$, $S = \tfrac{120}{11} = 10.91$. No cross term: $\tfrac{9}{14}$. The bands of 0.70, 0.68 and 0.64 do not meet.
- Long-only: SLSQP with bounds $[0, 1]$ and the budget returns $(0.3, 0.7)$ to within $5 \times 10^{-7}$ from three starts, on the data and on the quadratic form; the two ends of the budget give 20 and 60. Stationarity holds with the budget multiplier alone.
- $S = 11$ ($60 - 102 + 53$); slips 6.8 and 62; $\tfrac{49}{60}$. Part 5: $\sqrt{11/12} = 0.95743$, no tie at 3 places, `unit` "%". Taken: "0.957", "0.957%", "0.9574". Refused: "0.958", "0.956", "0.96", "0.00957". Routed: "3.317", "0.917", "2.236".

`p-curve-fit-backtrack`.
- Curvatures 0.8 and 30. Errors 0.5 and 0.002, excess 0.10006.
- First test, by the loop: $s = 1$ gives 0.05446 against a wanted drop of 0.0818 and fails; $s = 0.5$ gives 0.04776 under the bar 0.05916 and passes, with errors 0.3 and $-0.028$. $\lVert\nabla f\rVert^2 = 0.1636$, $\nabla f^T\mathbf{H}\nabla f = 0.236$, ratio 0.693. The fall formula of the explain is exact at four steps. 0.0625 and 0.03125 are the first halvings under $2/30$ and $1/30$.
- Second test: gradient $(0.24, -0.84)$, 0.7632 and 21.2141, ratio 0.036; trials 1, 0.5, 0.25, 0.125 and 0.0625 fail and 0.03125 passes. At 0.5 the excess is 2.32; at 1 it grows by 9.8; at 0.0625 it drops by 0.0063 against 0.02385.
- The count: the excess after the two steps is 0.034268. The fixed-step loop on both errors first gets under it, and under the printed 0.0343, at step 14; step 13 leaves 0.0346. $\ln(0.10006/0.0343)/\ln(1/0.9216) = 13.1$. Slips 13, 27 and 12 as their lines say.
- Bands: 0.03125 $\pm 0.0001$ takes 0.0313 and 0.0312 and refuses 0.031 ("Give the exact decimal"). `one-over-l` takes 0.0333 and 0.03333 and not 0.033, which gets the generic line; left.

Kept problems, changed lines.
- Set 1: chord gap 13; $C(-1) = 37$; minimiser 1.75 and 11.875; $C(0) = 18$, $C(3) = 15$; $C'(1.2) = -2.2$, $C(1.2) = 12.48$, the limit costs 0.605. $V(a, b)$ is $\operatorname{Var}(P - aF_1 - bF_2)$ at five points; minimiser $(7, -2)$ with $V = 1$; determinant 4, and $-9$ with $7ab$; with $b \ge 0$ SLSQP gives 5 at $(1, 0)$. The story now sells $a$ and $b$ and bans a purchase, which agrees with the signs.
- Set 2: `linprog` gives $(12, 2)$ and $-92$; 84, 1 £m-year unused, $2 \times 4 = 8$, 80; floor 5 gives 886 at $(6, 5)$; status 0 at a floor of 8 and 2 at 8.01. Blocks: $\tfrac{263}{9}$ at $(\tfrac{11}{3}, \tfrac{13}{9})$, 28.5 and 13.33 on the axes, 3.25 units unused, the swap adds 2; $(4, 1)$ alone earns 29. Strategies: dual 30 at $(1, 2)$, corners 40 and 70, primal $(0, 2, 4)$; one more of $u$ for two fewer of $v$ saves 10.
- Set 3: $g(3) = 42.75$; $\tfrac{14}{3}$ and $\tfrac{122}{3}$; estimate 42.07, re-solve 42.04 at a price of 4.47. $V(w)$, $w^* = 0.4$, $\mu = 1.5$, 3 basis points, re-solve 2.98 at 0.405. The dual function is named apart from the Lagrangian, "in £k" is there, the endowment holds corporate bonds.
- Set 4: 0.125, 0.0625, $2/f''(2) = 1$, eight times; 1.375; $f(0.625) = 14.05$; 1.7375, 2.2314, 6.15, 0.3625, 0.1395, 1.5145, 1.0125; $4.6043 + 3.4750 = 8.0793$ and £79. Variance log: ratio $\tfrac{49}{64}$, $1 - 0.765625 = 0.234375$, $V^* = 200$, 30 more steps, $1.04 \times 10^{-4}$ and $7.96 \times 10^{-5}$, 0.2901, 0.0735. The `extrapolated` option no longer contradicts the stem.

Read and not flagged (below what a learner would recognise).
- `p-account-target` part 1 `first`: "That is the first derivative. Differentiate $3x^{-1/2}$ once more." beside l2 S3 `first`: "That is $f'(x)$. Differentiate once more." A stock line on the problem's own function.
- `p-style-fit` part 3 generic: "Compare each weight with 0 and with 1, then ask what complementary slackness says about the bound multipliers." beside l12 S3's first hint: "Compare each weight with 0 and with 0.4." Its explain ends "so this KKT point is the global answer", beside `e-long-only-kkt`: "so this KKT point is the global minimum." Both are the taught fact in six words.
- "set the slope to 0" in `p-capital-price` part 1, `p-account-target` parts 3 and 5 and `p-style-fit` part 2: the author's stock phrase for a one-variable minimum.

## Engine

1. `[wrong-band]` (ruling a): skip a slip whose value rounds to 0 at the asked places while the slip is not 0. The two warnings on `convex/problems-4` are of this kind, and the band the rule asks for is the fault the second read removed.
2. `fresh-check` `retold` does not report `problems-1` `p-account-target` part 3 against `problems-3` `p-style-fit` part 2, although with maths and numbers masked the two `correct` lines share the run "with slope M it is N at M so" (finding 2). A run of six masked tokens between two sets of one course would catch it.

Inbox: two bullets under `Raised later (delta read AF convex):` in `docs/BACKLOG-INBOX.md`.

## Counts

3 findings: wrong 0, misleading 0, reuse 2 (2, 3), re-author 0, continuity 1 (1), voice 0, other 0. Six replacement strings, no key, no `wrong` value and no band changed. No problem is ruled `reuse` or `re-author`. Rulings: (a) keep the two narrowed bands, the rule is at fault; (b) the two shadow-price parts of set 3 stay, with one explain line reworded.

## Fix pass

1. Finding 1: fixed. "step 40" became "step 4" in the four strings of `problems-4` `items[0]` (prose, part 3 question, part 4 `keep`, part 5 question); recomputed 0.5/0.96^4 = 0.589 and 0.002 x 16 = 0.032. The author's script label updated to step 4.
2. Finding 2: fixed. `problems-3` `items[1].parts[1].feedback.correct` replaced with the reader's text (S = 100b^2 - 140b + 60, derivative 200b - 140 zero at 0.70).
3. Finding 3: fixed. `problems-3` `items[2].parts[4].explain.text` replaced with the reader's text; recomputed w = 0.40496, rise 2.977 basis points, mu = 0.06/V'(0.40496) = 1.477.

Ruling (a): the two `[wrong-band]` warnings on set 4 left as ruled.

Gates: validator 0 errors; voice scan 35: 0 and 0; fresh-check on sets 3 and 4: 0 hits (same advisories); grade-all 0 failures on both; all four convex scripts exit 0, delta script 331 checks, 0 FINDING (three `resolved`); playthrough sets 3 and 4, with and without `--mobile`: all passed. No keys, `wrong` values or bands changed.
