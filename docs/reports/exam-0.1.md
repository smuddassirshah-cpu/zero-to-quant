# Topic 0.1 exam: number

File: `app/content/exams/topic-0.1.json` (id `topic-0.1`, 45 minutes from the topic's 60 hours by `examMinutes` in `learn.js`, pass 0.7).
Generator and checks: `scratchpad/exam-0.1-0.2/` (`gen01.py` builds the file with exact fractions, `check01.py` recomputes every answer by a second method, `lint.py` checks the ramp, skills and copy rules, `course-text.txt` is the course dump used for the freshness search).

## Shape

23 items, interleaving the two courses (number-sense, ratio). Pitched at GCSE Higher; several items say "Work without a calculator".

| Difficulty | Items | Share | Ramp |
|---|---|---|---|
| 2 | 5 | 22% | 20% |
| 3 | 12 | 52% | 50% |
| 4 | 4 | 17% | 20% |
| 5 | 2 | 9% | 10% |

Widgets: 13 numeric, 3 choice, 2 multi, 2 order, 2 table, 1 drag-point (number line).

| # | id | d | skills | widget / canvas |
|---|---|---|---|---|
| 1 | e-mixed-subtract | 2 | ns-fractions | numeric |
| 2 | e-percent-build | 2 | pc-percent | numeric |
| 3 | e-pnl-close | 2 | ns-negatives | drag-point on number-line |
| 4 | e-decimal-order | 2 | ns-decimals | order |
| 5 | e-ratio-units | 2 | pc-ratio | choice |
| 6 | e-tranches | 3 | ns-fractions | numeric |
| 7 | e-terminating | 3 | ns-decimals, ns-fractions | multi |
| 8 | e-tick-count | 3 | ns-powers, ns-decimals | choice |
| 9 | e-fraction-power | 3 | ns-powers | numeric |
| 10 | e-operation-order | 3 | ns-estimate, ns-negatives | numeric |
| 11 | e-estimate | 3 | ns-estimate | choice |
| 12 | e-before-fall | 3 | pc-change | numeric |
| 13 | e-three-moves | 3 | pc-change | numeric |
| 14 | e-ratio-gap | 3 | pc-ratio | numeric |
| 15 | e-two-currencies | 3 | pc-rates | table |
| 16 | e-loss-share | 3 | pc-percent | numeric |
| 17 | e-fill-rate | 3 | pc-rates | numeric |
| 18 | e-depreciation | 4 | pc-change, ns-powers | numeric |
| 19 | e-inverse-square | 4 | pc-ratio, pc-rates | table |
| 20 | e-minus-eight | 4 | ns-negatives, ns-powers | multi |
| 21 | e-chain-ratio | 4 | pc-ratio | numeric |
| 22 | e-fund-fees | 5 | pc-percent, pc-change | numeric |
| 23 | e-recurring-proof | 5 | ns-decimals, ns-fractions | order |

Skills: all 9 of the topic are covered (`skills` map is the union of the two course.json files): ns-fractions 4, ns-decimals 4, ns-negatives 3, ns-powers 4, ns-estimate 2, pc-percent 3, pc-change 4, pc-ratio 4, pc-rates 3.

Quant framing: a desk's P&L below zero, fills of a share, a dividend ratio, fund tranches, futures ticks in standard form, a share's price before a fall, a portfolio's three moves, a desk bonus split, a bond coupon and broker fee in two currencies, losing trades, an algorithm's fill rate, a depreciating server, fund entry and performance fees.

Fresh against the courses: every question, prose line and number was searched in a dump of all five Stage 0 course files (lessons, quizzes, reviews, homework) and in `stage-0.json`. Two near copies were replaced: the ratio item (the course has "two partners split a profit in the ratio 5 : 3") now uses a 7 : 4 bonus and a £960 gap, and the estimate (the course estimates 612 ÷ 0.48) now uses 587. The stage exam's $8^{2/3}$, 15% of 240 and $\tfrac{2}{3} + \tfrac{3}{4}$ are not reused.

## Numbers computed twice

`gen01.py` computes each answer with `Fraction`; `check01.py` recomputes it another way and compares with the JSON: decimals and floats (19/12, 126, 2.25, 0.068), stepping along the line (−8), sorting by padded integers (the price order), repeated addition (12 tranches), long division to 30 digits (which fractions terminate, and 13/55 = 0.2363...), `Decimal` (7.5 × 10⁷ ticks, £400, €460, £1,600), a 1 s.f. rounding function (150), searches over whole amounts (£360, £3,520, the A : B : C shares, C = £600), forward checks (£20,000 × 0.8³ = £10,240; $yx^2 = 48$ in every row), and integer pence for the fund fees (£10,825.60). Numbers in the explanations were checked too: £2,240 and £1,280, 587 × 0.0487 ÷ 0.198 ≈ 144.4, 16,000 and 12,800, 6.25 minutes, the factor 18 in 234/990. No numeric wrong value lies within tolerance of its answer.

## Validation and playthrough

- `node tools/validate.mjs`: 0 errors and no warnings for this file (a concurrent agent's `topic-0.4.json` had one error at the last run; not mine).
- Copy lint (`lint.py`): no `!`, no em or en dashes, no sentence of 20 words or more, no American spellings.
- `playthrough.mjs --exam topic-0.1 --local-cdn <pkgs>`: 23 of 23, passed, desktop and `--mobile`.
- Screenshots reviewed (`scratchpad/exam-0.1-0.2/shots`). Fixes made from them: fractions in the multi options, the negative-power question and the recurring proof changed from `\tfrac` to `\dfrac`, which were too small to read on a phone.

## Engine notes

- The validator rejects a table cell's own `wrong[]` ids as `byKey` keys, though `table.js` returns them (AUTHORING section 3 says so). The two table items key their feedback on cell ids (`r0c1`) instead.
