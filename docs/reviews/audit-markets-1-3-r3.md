# Concept audit: markets levels 1 to 3, round 3

Blind read of commit `0bf8e2e2` by a fresh reader. Scope: `app/content/courses/markets/` l1 to l13, review-1 to review-3, homework-1 to homework-3 (the course has no `problems-*` file). Stage 1 course, so the full ledger.

- Ledger: `docs/reports/audit-markets-1-3-r3-ledger.md`, 3,221 rows: correct 3,216, imprecise 5, wrong 0, misleading 0, unverified 0.
- Concepts script: `docs/reports/markets-L1-3-concepts-r3.py`, 665 checks read from the JSON (every numeric key, every slip whose feedback names a mistake, every table cell, the true option of every choice item, the hidden tests of the six code widgets, the stated figures) and five Monte Carlo or sweep checks for the empirical claims.
- Sources: Hull, *Options, Futures and Other Derivatives* (10th edition section numbers); Brealey, Myers and Allen (BMA); Bodie, Kane and Marcus (BKM); Fabozzi, *Bond Markets, Analysis and Strategies*.

## Verdict

No `wrong` found. Four findings, all `imprecise` and all `minor`: two wordings a learner could over-generalise, one hint whose printed arithmetic is a penny-level rounding slip, and one stored slip value a penny from what its named mistake gives. Nothing changes a graded answer.

## Findings

1. `l6-yield.json` | `screens[5].hints[2].text` | imprecise, minor | The step hint prints "10-year: $-7.00/92.28 = -7.58\%$". That quotient is −7.586%, which is −7.59% to two places. | The key −7.58 is right from the unrounded prices: $(85.2798 - 92.2783)/92.2783 = -7.584\%$ (concepts script; Hull 4.4 pricing). A learner who divides the table's figures gets −7.59, which the 0.02 tolerance accepts, so only the hint's equation is off. | Replace the hint text with: `2-year: $-1.81/98.14 = -1.84\\%$. 10-year: $-7.00/92.28 = -7.59\\%$, or $-7.58\\%$ from the unrounded prices. Both are accepted.`

2. `review-2.json` | `items[0].widget.wrong[1].value` (`full-coupon`) | imprecise, minor | The feedback names "You paid £5 every six months". That mistake gives £110.83, and the file stores 110.84. | $5 \times \tfrac{1 - 1.03^{-6}}{0.03} + \tfrac{100}{1.03^6} = 27.0860 + 83.7484 = 110.8344$ (concepts script, failing check). The slip's tolerance is 0.05, so 110.83 still gets the line: no learner sees a difference. | Set `"value": 110.83`.

3. `l3-comparing-rates.json` | `screens[6].explain.text` (third sentence) and `summary.trap` | imprecise, minor | "Dividing by 12 gives a nominal monthly rate, not an effective one." and "Dividing an annual rate by 12 gives a nominal monthly rate." For a nominal rate credited monthly, $r/12$ is exactly the growth each month, as screens 0 to 2 teach; 1% a month is itself an effective monthly rate. The error on the trap screen is dividing an *effective* annual rate. "Nominal monthly rate" is not a standard term. | Hull 4.2: with a rate $R$ compounded $m$ times a year, each period grows by $R/m$. BMA ch. 2: APR divided by 12 is the monthly rate. A learner could carry away that $r/12$ is never the true monthly rate. | `screens[6].explain.text`, third sentence: `Dividing by 12 suits a nominal rate credited monthly; an effective annual rate needs the twelfth root.` `summary.trap`: `Dividing by 12 converts only a nominal rate credited monthly. From an effective annual rate, the monthly rate is $(1 + r_{\\text{eff}})^{1/12} - 1$.`

4. `l1-interest-on-interest.json` | `screens[8].explain.text` (second sentence) | imprecise, minor | "Adding up monthly returns understates compounded growth." True when every month gains, as here. With mixed signs the sum overstates: lesson 8 screen 1 has +20%, −10%, +5% adding to 15% against 13.4% compounded. | Derivation: $(1+a)(1+b) - 1 = a + b + ab$, and $ab < 0$ when the signs differ. BKM ch. 5 (arithmetic against geometric). Lesson 8 states the general rule correctly, so the risk is a short-lived over-generalisation. | Replace the sentence with: `Adding up monthly gains understates compounded growth.`

## Checks that passed and deserve a line

- Slips: every numeric slip whose feedback names a mistake was recomputed from the mistake (about 230 values). All match except finding 2. One needs its convention stated: `l2-present-value` screen 4 `once` is 1590.87 from the £1,352.77 the prose gives (1590.86 from unrounded present values); the tolerance of 0.05 covers both.
- Choice items: all 60 were read for a single true option under the stated premises. Two carry the right label with a wrong reason or wrong figures (`l8` screen 11 "Fund A: 0.75 against 0.60"; `review-2` item 2 "Y, because £3.00 is less than £12.00"); each is false as a statement and its `why` says so.
- Conventions: annual compounding unless stated; half-yearly bond yields stated on first use (`l5` screen 3); 365 against 360 days stated (`l3` screen 9); simple against log returns stated (`l8` screen 4); basis as spot minus future (`l11` screen 7, Hull 3.3); margin calls restore the initial margin and trigger strictly below maintenance (Hull 2.4), with the boundary case tested in `homework-3` item 4; modified against Macaulay duration distinguished (`l6` screen 6).
- Hypotheses kept: $g < r$ for the dividend discount model; "outlay followed by inflows" for a falling NPV curve and a single IRR; no dividends in the base cost-of-carry formula; the forward price for a consumption commodity given as an upper bound (`homework-3` item 8, Hull 5.11); "ignoring interest" on the $1/L$ wipe-out.
- Empirical or approximate claims, each checked in the concepts script: Newton reaches the bisection's 20-step precision in three steps from 4%, 5%, 6% or 8% (errors under $6 \times 10^{-9}$ percentage points); averaging yearly returns never understates the annualised return (200,000 draws); Sharpe ratios of 0.42 and 0.40 cannot be told apart in five years (A ahead in 50.9% of 20,000 pairs); three times leverage makes a 50% loss about 140 times likelier (13.3% against 0.096% of 1,000,000 draws); the rule of 72 runs short at 20% and long at 5%.
- Facts: the 2022 fall of about 13% in the US aggregate bond index, its worst year; GameStop short interest of about 140% of float in January 2021; Metallgesellschaft's loss of about 1.3 billion dollars (Hull, Business Snapshot 3.2); gilts quoted clean per £100 nominal with half-yearly coupons. All as stated.

## Code widgets (rule 6)

Run under the page's Pyodide 0.27.7 through `app/tools/code-runner.mjs` (scratch script `scratchpad/mkts13-r3/sweep.mjs`, 43 submissions).

| Widget | Line | Natural codings of the mistake | First failing test | Verdict |
|---|---|---|---|---|
| `l5` screen 9 | `test-1` (describes its test) | face not discounted; coupons not discounted; coupon rate not times face; face dropped | test 1, all four | correct |
| `l5` screen 9 | `test-2` (fixed 5%) | `1.05` in both lines; coupons at `0.05`; face at `1.05` | test 2, all three | correct |
| `l5` screen 9 | `test-3` (fixed 5 years) | face over 5 years; loop and face fixed at 5; loop alone fixed at 5 | test 3, test 3, test 4 | correct (two of three; the third gets the generic line, since test 3 is a zero-coupon bond) |
| `l8` screen 10 | `test-1` (average, not compounded) | arithmetic mean; total over years; root without the −1 | test 1, all three | correct |
| `l8` screen 10 | `test-2` (root not `len`) | `1/3`; `0.3333`; `math.cbrt` | test 2, all three | correct |
| `l8` screen 10 | `test-6` (`math.log(0)`) | sum of `math.log`; `math.log1p`; a log loop | test 6, all three | correct |
| `homework-2` item 3 | `test-1` (direction) | `<` for `>`; operands swapped; compared with `face` | test 1, all three | correct |

Wrong programs against the hidden tests: simple discounting, a loop one coupon short (`l5`); simple discounting, the outlay discounted a year, compounding forward, the rate as a per cent (`l4` screen 7); a reversed bracket and a test on the sign of `mid` (`homework-1` item 5); a call at or below maintenance, a top-up to maintenance, a call not added back, one contract's margins, a short treated as long, a call whenever below initial (`homework-3` item 4). Every one fails; every starter fails; no wrong program passed. A NumPy version of the log method in `l8` passes test 6, correctly, because `np.log(0)` is `-inf` and `np.exp(-inf)` is 0. None of the lines depends on timing.

## Overlap with earlier reads

Read after the ledger and findings above were written: `docs/reviews/review-1.7.md`, `docs/reviews/audit-markets-1-3.md`, `docs/reviews/audit-markets-1-3-r2.md` and their ledgers.

All 30 earlier conceptual findings were fixed before this commit (review-1.7: 13; audit round 1: 11, and 1 from its fix-pass read; audit round 2: 5). Each fixed text has a ledger row here and all read correct, so "both" can only count a defect that survived its fix. None did.

| Conceptual findings | Count | Items |
|---|---:|---|
| This audit only | 4 | 1 to 4 above, all `imprecise`, minor |
| Earlier reads only | 30 | review-1.7: 13; round 1: 11; its fix-pass read: 1; round 2: 5. All fixed and verified in the ledger |
| Both | 0 | |

New `wrong` that no earlier read found: **0**. That is within the convergence rule's one new `wrong` per three levels.

Notes on the overlap:

- Finding 1 is a remnant of a review-1.7 fix, not the same defect. That review found the 10-year cell keyed −7.59 against text saying −7.58, and the key was moved to the exact −7.58. The hint's quotient of rounded prices then no longer equals what it prints. Both earlier ledgers mark the hint `correct`.
- Finding 2 was marked `correct` in both earlier ledgers ("the named mistake recomputed to this value"). To the penny it is 110.83; the 0.05 tolerance hides the difference.
- Findings 3 and 4 were marked `correct` in both earlier ledgers.
- Round 2's two `wrong` (the `homework-1` `simple` equation and the `l8` screen 5 `up` option) are sound now: $1000(1 + 1.5r) = 1100$ gives 6.67%, and halving only the £50 gain leaves £125.
- Round 1's serious findings (the NPV premise, the short's dividend, the fuel forward as an upper bound) remain sound, as does `q-different-rates`.

## Inbox

No engine limit met; no bullet added to `docs/BACKLOG-INBOX.md`.

## Runs

- `cd app && node tools/validate.mjs`: 0 errors, 4,614 warnings (whole repository).
- `node tools/run-number-scripts.mjs --only markets` (venv Python first on `PATH`): 1 script, 1 passed.
- `node tools/grade-all.mjs --file <each of the 19 files> --code --local-cdn <pkgs>`: 219 widgets and 6 Python code widgets, 0 failures.
- `python docs/reports/markets-L1-3-concepts-r3.py`: 665 checks, 2 failed, exit 1. The two failures are findings 1 and 2 and stay failing until fixed. Venv NumPy is newer than CI's pin; no figure depends on the version.
- `node scratchpad/mkts13-r3/sweep.mjs app <pkgs>`: 43 submissions, all as the table above.
- No playthrough (auditor rule 7).

## Fix pass

Opus fixer, from commit `8d0dd3dc`. Each basis below was derived afresh, not copied from the finding.

1. Fixed (auditor's text). Basis: $-7.00/92.28 = -0.075856$, so −7.59% from the table's rounded prices; the unrounded prices (92.27827 and 85.27983, recomputed by summing discounted coupons) give −7.584%, so −7.58. The key −7.58 stays; both values sit inside its 0.02 tolerance, so the hint now says so.
2. Fixed. Basis: £5 a period for 6 periods at 3% plus £100 at $1.03^{-6}$ is 110.83438, once by summing the six discounted coupons in exact fractions and once by the annuity formula. Slip set to 110.83; it stays clear of the key 97.29 and the other slips (97.33, 82.79). No key changed.
3. Fixed differently (own wording, same substance). Basis: Hull 4.2, a rate $R$ compounded $m$ times a year grows by $R/m$ each period, so $r/12$ is the true monthly rate for a nominal rate credited monthly; the trap's error is dividing an effective rate. Explain, third sentence: "Dividing by 12 works only for a nominal rate credited monthly, not for an effective rate." Trap: "Dividing by 12 gives the monthly rate only for a nominal rate credited monthly. From an effective annual rate, the monthly rate is $(1 + r_{\text{eff}})^{1/12} - 1$."
4. Fixed (auditor's text). Basis: $(1+a)(1+b) - 1 = a + b + ab$; the sum understates only when $ab > 0$. Lesson 8's +20%, −10%, +5% gives $1.2 \times 0.9 \times 1.05 - 1 = 13.4\%$ against a 15% sum. Sentence now reads "Adding up monthly gains understates compounded growth."

Runs: validator 0 errors; voice scan 35 on the four files 0 and 0 (0 explanations over three sentences); `markets-L1-3-concepts-r3.py` 665 checks, 0 failed, exit 0 (no re-pointing needed: the finding 1 check looks for the old text, the finding 2 check recomputes the slip); r2, r1 and fixread scripts exit 0; `run-number-scripts --only markets` 1 passed; `grade-all --file` on the four files 0 failures; playthrough of l1, l3, l6 and review-2, desktop and `--mobile`, all passed. No key, slip band, hidden test or solution changed beyond the slip value in finding 2.
