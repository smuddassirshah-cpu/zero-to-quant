# Review: the 74 new reuse hits of engine pass 7 remainder, package 3

Read at `c2845d4f` (`claude/session-ah-engine-pass-1nzn58`). Source list: `docs/reports/engine-pass-7r-pkg3-hits.md`. No content, waiver or engine file was edited. Both items of each of the 41 unwaived hits were opened and read side by side; the 33 hits that existing waivers clear were skimmed the same way.

Standard applied: a part is a FAULT when a learner could answer it by recalling a lesson screen, homework item or exam item (same structure with the same or scaled numbers, or the same deciding step in the same guise). A shared stock phrase, a shared standard number, a well-known object asked a different question, or new numbers through a taught method STANDS.

## Counts

| Tag | Hits | Cleared by existing waivers | Read in full | FAULT | STANDS |
|---|---|---|---|---|---|
| ratio (gate) | 7 | 0 | 7 | 1 | 6 |
| chain-union (gate) | 1 | 0 | 1 | 1 | 0 |
| question (gate) | 1 | 0 | 1 | 0 | 1 |
| all-exams (not gated) | 65 | 33 | 32 | 0 | 32 |
| Total | 74 | 33 | 41 | 2 | 39 |

The 32 unwaived all-exams hits by kind: ratio 16, rate 11, and one each of pair, numbers, transform, function and question. All 32 stand. One of them (the question hit) is the gate hit again, against a homework file and not an exam.

Skim of the 33 waived all-exams hits: no waiver hides a fault. 32 of the 33 are same-course hits printed a second time under the `[all-exams]` tag (their sources are lessons, reviews and other sets); only `p-tail-bound` against `exams/topic-1.3.json` is an exam hit. Each pair shares a taught rule in its natural words or a slip line, with its own numbers. The closest is `markov/problems-5.json` `p-signal-trial` part 2 against `review-5.json` `r-base`: the same question on the mirrored walk ($p = 0.45$ against 0.55). Recalling the review's $\tfrac{9}{11}$ gives the set's `p-over-q` slip, not its key, so the learner must still apply $r = q/p$. It stands.

## FAULT list

### Fault 1 (ratio, gate). `courses/trig/problems-3.json` `p-daylight-model`, all five parts. Change the problem set.

The source is `courses/trig/homework-3.json` `h3-demand-model`. Both fit $a\sin\big(b(t - c)\big) + d$ to a yearly cycle from its peak and trough, then find when the curve is above a level. The set's 16.4 and 7.6 hours are the homework's 820 and 380 GWh divided by 50, so $a = 4.4$ and $d = 12$ are the homework's 220 and 600 on another scale. Two earlier reads (`review-delta-problems-aa-3.md` c2 and its first read, finding 20) moved the level of parts 4 and 5 and left the peak and trough alone.

Fix: new peak and trough, 17.6 and 6.4 hours. The midline stays 12, the months stay 6 and 12, the level stays 10 hours. With new numbers in a new setting the fit is the taught method, which stands.

Apply it with the committed script (it computes every number twice and refuses to write if a check fails):

```
/tmp/claude-0/-home-user-zero-to-quant/03f41800-e92e-529a-9172-f90ee010591f/scratchpad/venv/bin/python docs/reviews/review-pkg3-reuse-hits-scripts/trig_daylight_fix.py app/content/courses/trig/problems-3.json --apply
```

It changes 27 fields of `items[2]` and nothing else. One pass over every string of the item replaces these printed numbers:

| Old | New | Where |
|---|---|---|
| 16.4, 7.6 | 17.6, 6.4 | `prose`; part 1 `feedback.correct`, `byKey.midline`, `explain.text`; part 5 `explain.text` |
| 8.8 | 11.2 | part 1 `byKey.range`, `explain.text` |
| 4.4 | 5.6 | part 1 `accept`, `feedback`, `explain`; part 3 `explain.text`; part 4 `question`, `feedback.correct`, `explain.text` |
| $\tfrac{5}{11}$ | $\tfrac{5}{14}$ | part 4 `feedback.correct`, `byKey.no-shift`, `byKey.above`, `explain.text` |
| 0.4719, 3.6135 | 0.3652, 3.5068 | part 4 `feedback.correct`, `explain.text` |
| $-0.90$, 6.90 | $-0.70$, 6.70 | part 4 `explain.text` |
| 2.10, 9.90 | 2.30, 9.70 | part 4 `feedback.correct`, `explain.text`; part 5 `question`, `feedback.correct`, `byKey.whole-months`, `explain.text` |
| 7.8, 4.2 | 7.4, 4.6 | part 5 `accept`, `feedback.correct`, `byKey.whole-months`, `explain.text` |

Keys, bands and slips (bands unchanged):

| Part | Field | Old | New | Exact value |
|---|---|---|---|---|
| 1 | `widget.answer`, `accept` (tol 0.001) | 4.4 | 5.6 | 5.6 |
| 1 | `wrong` `range` | 8.8 | 11.2 | 11.2 |
| 1 | `wrong` `longest` | 16.4 | 17.6 | 17.6 |
| 1 | `wrong` `midline` | 12 | 12 | 12 |
| 2 | all fields | | unchanged | $\tfrac{\pi}{6}$ |
| 3 | all but `explain.text` | | unchanged | 3 |
| 4 | `widget.answers` (tol 0.01) | [2.1, 9.9] | [2.3, 9.7] | 2.3025, 9.6975 |
| 4 | `wrong` `no-shift` | "6.9, 11.1" | "6.7, 11.3" | 6.6975, 11.3025 |
| 4 | `wrong` `above` | "3.9, 8.1" | "3.7, 8.3" | 3.6975, 8.3025 (14 hours, as the feedback says) |
| 5 | `widget.answer`, `accept` (tol 0.05) | 7.8 | 7.4 | 7.3950 |
| 5 | `wrong` `outside` | 4.2 | 4.6 | 4.6050 |
| 5 | `wrong` `whole-months` | 8 | 8 | 10 − 2 |

Checked on a scratch copy of `app/content` with the fix applied: `validate.mjs --root` 0 errors and no warning on the file, `grade-all.mjs --file` 18 widgets and 0 failures, `same-course-reuse.mjs --file ... --all-exams` 0 warnings. In the trig course 17.6 appears nowhere else, and 6.4 and 5.6 only in the triangle lessons l3 and l1.

The fixer must also re-key the item's block in `docs/reports/problems-trig-numbers.py` (lines 482 to 512), or the `number-scripts` job fails:

- `F(164, 10)` to `F(176, 10)`, `F(76, 10)` to `F(64, 10)`, every `4.4` to `5.6`, `16.4` to `17.6`, `7.6` to `6.4`, `printed='4.4'` to `'5.6'`.
- `sp.Rational(22, 5)` to `sp.Rational(28, 5)`; every `Rational(5, 11)` and `5 / 11` to `Rational(5, 14)` and `5 / 14`; the messages `-5/11` to `-5/14`.
- Roots `2.0988` and `9.9012` to `2.3025` and `9.6975`; `0.4719` to `0.3652`; `3.6135` to `3.5068`; slips `6.9012` and `11.0988` to `6.6975` and `11.3025`.
- `[6.9, 11.1]` to `[6.7, 11.3]`, `[3.9, 8.1]` to `[3.7, 8.3]` (also `Lm(3.9)`, `Lm(8.1)` and the tuple `(6.9, 11.1)`), `asked=[2.1, 9.9]` to `[2.3, 9.7]`.
- Line 504: the tolerance `1e-3` becomes `2e-3` (6.7 is 0.0025 months from 6.6975, a sine gap of 0.0012).
- Part 5: `7.8` to `7.4`, `7.8024` to `7.3950`, `4.1976` to `4.6050`, `asked=9.90 - 2.10` to `9.70 - 2.30`, band edges `7.7` and `7.9` to `7.3` and `7.5`.

Then the usual chain on the one file: validator, voice scan, number script, `grade-all --file`, playthrough `--problems trig/problems-3` with and without `--mobile`.

### Fault 2 (chain-union, gate). `courses/validation/problems-2.json` `p-spread-blocks`, parts 1 to 4. Re-author the whole problem.

Every part is one course step on a 24-day calendar, in the lesson's order and guise, and no part feeds the next beyond naming fold 2:

| Part | Asks | Source it walks |
|---|---|---|
| 1 | test days of a shuffled fold with a training day on both sides | `l5-shuffling-lies.json` screens[1], the same count on 15 days; the same `all` slip |
| 2 | training days after an unshuffled test block | `l5-shuffling-lies.json` screens[7], the same question; the slip line "18 counts every training day" is the lesson's "12 counts every training day" |
| 3 | training days left after the purge and the embargo | `homework-2.json` `h-count` ($1000 - 100 - 19 - 19 - 10$ against $24 - 6 - 3 - 3 - 2$), with the same `h` and no-embargo slips; also `review-2.json` `r-purge`, `l7-purging.json` screens[1] and [2], the set's own `p-forward-label`, and exam `stage-2.json` `a-purged-fold` |
| 4 | the percentage by which purging raises the error | `l7-purging.json` screens[5], the same question in the same words (not flagged by the tool) |

No change of numbers mends this: the deciding step of each part is the one its source delivers. A fixer cannot settle it. The main session should brief a re-author of `p-spread-blocks` (four parts, the skills `vl-time`, `vl-leakage`, `vl-cv`), and the new problem must not walk:

- the sandwich count of a shuffled fold (l5 screens[0] and [1]) or the later-training-days count of a block (l5 screens[7], [8]);
- the count of rows left, or removed, by a purge and an embargo round one block (l7 screens[1], [2], quiz[1]; `r-purge`; `h-count`; `p-forward-label`; exam `a-purged-fold`);
- the percentage rise of the error under purging (l7 screens[5]), the shuffled-to-ordered error ratio (l5 screens[2]), the pooled MSE of joined folds (l6 screens[5], `r-pool`, `p-gas-demand` part 3), and the fold standard error flag (l8, `h-z`, `p-signal-break`).

## STANDS

39 hit lines stand, in 35 waiver entries: 7 that clear gate warnings (the first 7 below; the `question` entry also clears its all-exams copy) and 28 for all-exams lines, which never gate and may be left out if the main session prefers a short file. Built by `docs/reviews/review-pkg3-reuse-hits-scripts/waivers.mjs` from the checker's own JSON, in the format of `app/tools/same-course-waivers.json` (file, item, kind, source file or list, reason). Trial with the merged file as `ZQ_WAIVERS`: `--all --all-exams` prints 0 errors, 2 warnings (the two faults) and 0 all-exams warnings.

Two stands that are not chance matches:

- `conditional/problems-5.json` `p-two-houses` part 2 against `homework-5.json` `h-gap` (question). Both ask by how much the survivors' average overstates the average of all funds, and both use 8% for survivors. The data differ (25 of 50 funds and −2%, against 60% and −5%; answers 5.0 and 5.2), the share that closed must be found from counts, and the part feeds a comparison of two houses that the homework lacks. New numbers through the taught formula: stands.
- `limits-thm/problems-3.json` `p-fund-months` against `exams/topic-1.6.json` `s-sharpe-p` (numbers). Both reach $t = 1.8$ and are told $\Phi(1.8) = 0.9641$. The set gets $t$ from a monthly mean and $\sigma/\sqrt n$ and asks a two-sided tail (0.0718); the exam gets it from a Sharpe ratio and $1/\sqrt T$ and asks a one-sided $p$ (0.0359). Each key is the other's slip, so recall alone answers neither. Stands; if a later pass touches the set, moving it off $t = 1.8$ would end the likeness.

The other 37 lines are chance matches of two numbers (a table size against a percentage sum, a variance against a squared autocorrelation, and so on); each reason names both sides.

```json
[
  {
    "file": "courses/conditional/problems-5.json",
    "item": "p-two-houses",
    "kind": "question",
    "source": "courses/conditional/homework-5.json",
    "reason": "stands: the survivorship gap asked in its natural words; own data (25 of 50 funds, 8% and −2%, against 60%, 8% and −5%), and the part feeds a Simpson comparison of two houses that the homework lacks (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/equations/problems-2.json",
    "item": "p-interest-split",
    "kind": "ratio",
    "source": "courses/equations/l15-swapping-in.json",
    "reason": "stands: £660 of interest and the multiplier 1000 against share prices of £8.25 and £12.50; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/numerics/problems-1.json",
    "item": "p-float32-overnight",
    "kind": "ratio",
    "source": "courses/numerics/l8-splines.json",
    "reason": "stands: a relative error of 3.16e-8 against a quote of 3.95% moved 10 bp; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/numerics/problems-4.json",
    "item": "p-pilot-control",
    "kind": "ratio",
    "source": "courses/numerics/l1-floating-point.json",
    "reason": "stands: a covariance of 77 from 2,000 paths against 2.31e18 and the exponent 60; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/regression/problems-1.json",
    "item": "p-stopping-distances",
    "kind": "ratio",
    "source": "courses/regression/l3-how-much-explained.json",
    "reason": "stands: stopping distances of 23 m and 36 m against fitted values 2.3 and 3.6 of an SSR screen; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/stat-learning/problems-1.json",
    "item": "p-heat-demand",
    "kind": "ratio",
    "source": "courses/stat-learning/review-2.json",
    "reason": "stands: a training MSE of 3.10 and degree 6 against 31 May and a 60-day volatility; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/vectors/problems-1.json",
    "item": "p-charging-robot",
    "kind": "ratio",
    "source": "courses/vectors/l4-portfolio-return.json",
    "reason": "stands: a dot product of 42 and a squared length of 68 against price moves of £2.10 and £3.40; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/algebra/problems-1.json",
    "item": "p-probe-stride",
    "kind": "ratio",
    "source": "exams/mock-oa-arith.json",
    "reason": "stands: slot 13 of a 56-slot table against 65% of 280 in a mental arithmetic mock; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/analysis/problems-2.json",
    "item": "p-sum-law-band",
    "kind": "rate",
    "source": "exams/topic-2.1.json",
    "reason": "stands: 4/311 is a term of a limit gap and 0.04 its epsilon, against a Kelly growth of 1.29% and a stake of 0.04; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/arma/problems-3.json",
    "item": "p-smoothed-fund",
    "kind": "rate",
    "source": "exams/topic-2.1.json",
    "reason": "stands: a root-12 volatility of 10.0% and a variance weight 0.52, against 1,000 labels worth 100 and a base rate of 52%; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/coint/problems-1.json",
    "item": "p-screen-real-share",
    "kind": "rate",
    "source": [
      "exams/topic-3.3.json",
      "exams/mock-oa-trader.json"
    ],
    "reason": "stands: a slip value of 19.4% (36 of 186) against 7/36 in a meeting-time item and a dice item; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/conditional/problems-2.json",
    "item": "p-takeover-rumour",
    "kind": "ratio",
    "source": "exams/topic-0.5.json",
    "reason": "stands: 180 of 456 rumoured stocks against trades of £15 and £38 in a mental sum; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/eigen/problems-3.json",
    "item": "p-crab-sizes",
    "kind": "ratio",
    "source": "exams/mock-oa-trader.json",
    "reason": "stands: claw lengths 88 and 118 against terms 44 and 59 of a digit-sum sequence; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/eigen/problems-3.json",
    "item": "p-site-anomalies",
    "kind": "rate",
    "source": "exams/topic-2.6.json",
    "reason": "stands: a variance share 0.769 against a logistic slip of 76.85%; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/elimination/problems-1.json",
    "item": "p-florist-prices",
    "kind": "ratio",
    "source": "exams/mock-superday-trader.json",
    "reason": "stands: matrix entries 13 and 19 against the product 38 × 26; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/functions/problems-1.json",
    "item": "p-sapling-log",
    "kind": "ratio",
    "source": "exams/topic-3.3.json",
    "reason": "stands: heights 29 and 32 cm against the product 58 × 64; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/garch/problems-2.json",
    "item": "p-two-filters-one-score",
    "kind": "rate",
    "source": "exams/stage-2.json",
    "reason": "stands: a starting variance of 1.44 %² against 0.12 squared inside a Ljung-Box sum; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/garch/problems-3.json",
    "item": "p-bank-index-flat-var",
    "kind": "rate",
    "source": [
      "exams/topic-2.5.json",
      "exams/stage-2.json"
    ],
    "reason": "stands: a starting variance of 2.25 %² and a leverage cap of 1.25 against a KKT multiplier and a covariance entry; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/least-squares/problems-3.json",
    "item": "p-runner-heart",
    "kind": "ratio",
    "source": "exams/mock-oa-trader.json",
    "reason": "stands: a slope of 5.9 against terms 40 and 59 of a digit-sum sequence; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/limits-thm/problems-3.json",
    "item": "p-fund-months",
    "kind": "numbers",
    "source": "exams/topic-1.6.json",
    "reason": "stands: both reach t = 1.8 and are told Φ(1.8) = 0.9641; the set asks a two-sided tail from a monthly mean and σ/√n, the exam a one-sided p from a Sharpe ratio and 1/√T, so neither deciding step gives the other (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/limits/problems-3.json",
    "item": "p-relative-strength",
    "kind": "pair",
    "source": "exams/topic-1.6.json",
    "reason": "stands: 0.0004 and 0.02 are a ratio's slope and level, against a variance and its root in a standard error; different quantities (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/markov/problems-3.json",
    "item": "p-maker-edge",
    "kind": "ratio",
    "source": "exams/topic-3.5.json",
    "reason": "stands: a standard deviation of £39.80 over 400 trades against 10 units and a limit of 100.5; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/number-sense/problems-4.json",
    "item": "p-cycle-commute",
    "kind": "transform",
    "source": "exams/topic-2.3.json",
    "reason": "stands: four commute times against four returns inside a code task; a chance affine match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/numerics/problems-4.json",
    "item": "p-grid-node-budget",
    "kind": "ratio",
    "source": "exams/topic-0.5.json",
    "reason": "stands: a volatility of 30% and a spot of 76 against trades of £15 and £38 in a mental sum; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/random-vars/problems-1.json",
    "item": "p-tightest-quote",
    "kind": "rate",
    "source": "exams/topic-2.3.json",
    "reason": "stands: 0.6 to the 9th, 0.0101, against a trading cost of 1.01% and £0.60 traded; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/random-vars/problems-4.json",
    "item": "p-file-retry",
    "kind": "ratio",
    "source": "exams/mock-oa-trader-3.json",
    "reason": "stands: waits of 3.2 and 7.4 seconds against terms 16 and 37 of a digit-square sequence; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/ratio/problems-3.json",
    "item": "p-partners-profit",
    "kind": "ratio",
    "source": "exams/topic-1.6.json",
    "reason": "stands: £2,850 of £12,000 against a 95% interval on 400 days; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/regression/problems-1.json",
    "item": "p-car-prices",
    "kind": "ratio",
    "source": "exams/topic-1.1.json",
    "reason": "stands: prices of £15,400 and £18,000 against closes of 77.0 and 90.0 in a drawdown assert; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/series/problems-2.json",
    "item": "p-bouncing-ball",
    "kind": "rate",
    "source": "exams/topic-2.3.json",
    "reason": "stands: 0.6 to the 9th, 0.010078, against a trading cost of 1.01%; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/stat-learning/problems-1.json",
    "item": "p-loaves-k",
    "kind": "ratio",
    "source": "exams/mock-oa-trader.json",
    "reason": "stands: expected errors of 5.8 and 10.4 against terms 29 and 52 of a digit-sum sequence; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/stat-models/problems-2.json",
    "item": "p-two-looks",
    "kind": "rate",
    "source": "exams/topic-2.2.json",
    "reason": "stands: a planned level of 0.0107 and 37 patterns against a VaR line of a breach chart; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/stat-models/problems-3.json",
    "item": "p-spread-day-tail",
    "kind": "ratio",
    "source": "exams/topic-0.5.json",
    "reason": "stands: normal arguments 2.003 and 2.819 against trades of £27 and £38 in a mental sum; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/validation/problems-2.json",
    "item": "p-gas-demand",
    "kind": "ratio",
    "source": [
      "exams/mock-oa-trader-2.json",
      "exams/mock-oa-trader-3.json"
    ],
    "reason": "stands: block errors of 5.2 and 6.1 against terms of two number sequences; a chance match (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/validation/problems-2.json",
    "item": "p-spread-blocks",
    "kind": "ratio",
    "source": "exams/topic-1.1.json",
    "reason": "stands: errors of 3.85 and 4.62 against closes of 77.0 and 100.0 in a drawdown assert; a chance match (moot once the item is re-authored, fault 2) (review-pkg3-reuse-hits)"
  },
  {
    "file": "courses/vector-calc/problems-2.json",
    "item": "p-rectangle-edges",
    "kind": "function",
    "source": "exams/topic-1.3.json",
    "reason": "stands: y³ − 4y is one component of a field whose curl is asked, against f′(x) = x³ − 4x read off a graph for its maxima; a small cubic, different questions (review-pkg3-reuse-hits)"
  }
]

```

## Verdict on each new rule

- **`chain-union`: keep.** One hit, one fault, and a fault the single-source chain test and the earlier reads of the set missed. It also undercounted: part 4 walks a fourth screen. Best value of the package.
- **`ratio`, same course: keep as a warning.** One fault in seven, and that fault (a homework on another scale) is exactly what the rule was built for and what no other kind saw. The six chance hits pair amounts of different kinds (pounds against a multiplier of 1000, metres against fitted values). A test that the two amounts carry the same unit, or that the two items share a skill, should drop most of the six and keep the fault; that is untested.
- **`ratio` and `rate` under `--all-exams`: not worth their lines.** 27 hits, 27 chance. About a dozen of the 31 exam-source hits are against mental-arithmetic and sequence items, which have numbers and no setting. Leave these two kinds out of the mode, or require a shared skill.
- **`question`: keep as a warning.** One hit, a true near neighbour that deserved the read, ruled stands on its numbers. No noise.
- **`story`, `xparam`: no evidence.** Neither fires on current content.
- **`--all-exams` as a mode: keep it off the gate and out of routine runs.** 0 faults in 32. Its number kinds (ratio, rate, pair, numbers, transform) are noise across unrelated courses; only the text kinds (retold, text, question, function) are worth reading there. The same holds for the open decision on reading the 23 `parts[]` exam files by default: do it for the text kinds only.
- **Tool defect.** `--all-exams` prints every same-course hit a second time under its tag: 33 of the 65 lines have a course file as source, not an exam. The true count of new exam hits is 32 (31 unwaived, 1 waived). The mode should list only hits whose source is an exam.

## Scripts

`docs/reviews/review-pkg3-reuse-hits-scripts/`: `dump.mjs` (both items of each hit side by side; `WAIVED=1` for the waived ones), `waivers.mjs` (verdict table to waiver entries, with a merged trial file), `trig_daylight_fix.py` (fault 1: computes, checks and applies).

## Fix pass

- Fault 1 (`trig/problems-3` `p-daylight-model`): FIXED with `trig_daylight_fix.py --apply` (27 fields, 17.6 and 6.4 hours); `docs/reports/problems-trig-numbers.py` lines 482 to 512 re-keyed as listed (tolerance 2e-3, roots 2.3025 and 9.6975, 5/14). Whole problem re-read: sentences, explanations and slip lines agree; 6.4 to 17.6 hours of daylight is plausible for a northern town. Validator 0 errors, no warning tag on the file; voice scan 0 and 0; number script passes; `grade-all --file` 18 widgets, 0 failures; playthrough green with and without `--mobile`. Graded answers changed: part 1 (5.6), part 4 (2.3, 9.7), part 5 (7.4).
- Fault 2 (`validation/problems-2` `p-spread-blocks`): DEFERRED to an author, not touched.
- Waivers: the 7 gate-clearing entries added to `app/tools/same-course-waivers.json`; the 28 all-exams-only entries left out. Reuse gate `--all`: 0 errors, 1 warning (`p-spread-blocks`, chain-union).
