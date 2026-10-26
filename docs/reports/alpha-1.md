# alpha level 1 (Universe): report

## Files written

All in `app/content/courses/alpha/`, skill `al-universe` throughout, £ for money.

| File | Screens / items | Code screens |
|---|---|---|
| `l1-choosing-a-universe.json` | 11 screens, 4 quiz items | `universe_on`, `universe_mask` |
| `l2-splits-and-dividends.json` | 11 screens, 4 quiz items | `split_adjust`, `total_return` |
| `l3-including-the-dead.json` | 11 screens, 4 quiz items | `survivorship_gap`, `delisting_return_kept` |
| `l4-returns-panel.json` | 11 screens, 4 quiz items | `forward_returns`, `to_long` |
| `review-1.json` | 9 items, difficulty 2 to 4, all four lessons interleaved | none |
| `homework-1.json` | 7 items, difficulty 3 to 5 (two at 5) | `clean_panel` (5), `universe_turnover` (4); `order` item; `longform` with a 10-point rubric |

Each lesson: hook, explore (a real control-driven canvas), name, ladder, two code screens, trap, generalise or derive, transfer(s), summary, quiz. Edge cases: l1 the 59 empty days before a full 60-day window; l2 a split and a dividend on the same day (hand case; the seed has none) and a share's first day (NaN); l3 a late listing is not a death (boxes screen, code test, quiz); l4 a death inside the forward window and the NaN tail.

Generators (all in `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/alpha-1/`): `common.py`, `l1.py` to `l4.py`, `sets.py`, `lib.py` (the solutions), `hwlib.py`. Every test `expect` is computed by evaluating the call against the solutions, not typed by hand.

## Validator

`node app/tools/validate.mjs`: 0 errors and 0 warnings for these six files. (At the time of the run the validator reported 8 errors elsewhere, all in `cpp/` files, "tolCase is not defined", from another agent's in-progress work.)

## Playthrough

`node app/tools/playthrough.mjs --lesson ... --set alpha/review-1 --set alpha/homework-1 --local-cdn .../scratchpad/pkgs --shots ...`: all passed.

- l1: 15 checks, quiz 4/4. l2: 15 checks, quiz 4/4. l3: 15 checks, quiz 4/4. l4: 15 checks, quiz 4/4.
- review-1: 9 of 9 recorded. homework-1: 7 of 7, 33 of 33 marks.
- Every screen was screenshotted (plus the Why? sheets for l3 and l4) and inspected; fixes made: y ranges (explore lines clipped, prices drawn below £0), the forward-return tables moved into the widget with a bars canvas, arrowheads on the pipeline graph (`directed: true`), bar highlight ids.
- Every code test was also run directly in Pyodide 0.27.7 under node (`pyrun.mjs`): all matched. NumPy plus pandas load took 13 to 18 s under node; whole lessons took 20 to 55 s in the browser playthrough.

## Conventions and signatures

- Data: the brief's `make_panel()` verbatim, seed 2310; tests use `small = make_panel(30, 300, 5)` and a few full-panel cases. Every prelude puts `import numpy as np` and `import pandas as pd` on separate lines above the generator (see backlog: the import scan misses `import numpy as np, pandas as pd`).
- `daily_volume_gbp(p)` (hidden helper, "already defined"): `p["volume_gbp"]` if the panel has a daily £ volume, else `p["listed"] * p["adv_gbp"]`, NaN where not listed. `make_panel` has one volume per share, so its trailing mean is `adv_gbp` once 60 days exist; the l1 hand panel `toy` (120 days, shares A to E) has a daily figure so the trailing-versus-whole-sample trap and the look-ahead spies bite.
- `universe_on(p, date, min_adv_gbp=5e6, window=60)` and `universe_mask(p, min_adv_gbp=5e6, window=60)`: listed on the date and a trailing 60-day mean £ volume, today included, of at least £5m (inclusive), NaN until a full window. The `window` keyword is an addition; the brief's signatures still work.
- `split_adjust`: close divided by the product of split ratios strictly after its date. `total_return`: `split * (raw_close + dividend) / raw_close.shift(1) - 1`, dividend per new share; NaN on each share's first listed day (where `make_panel`'s `ret` has a value: 30 such cells on `small`).
- `forward_returns(ret, h)`: row t is prod(1 + r) - 1 over t+1..t+h, compounding the days that exist, NaN if none, NaN on the last h rows, `ValueError` for h < 1; checked against a slow loop and a spy that rewrites returns up to row t.
- `to_long(panel)`: columns `date`, `name`, `value`, NaN dropped, sorted, index from 0 (via `melt`, so it behaves the same in pandas 2.2 and 3).
- `survivorship_gap(ret, listed)` -> (everyone, survivors), 252 x mean daily equal-weighted return, 4 places. `delisting_return_kept(ret, listed)` -> sorted (name, ISO last listed date, last return to 4 places) for shares listed at some point and not on the last day.
- Homework `clean_panel(raw_close, split, dividend, listed, min_adv_gbp, adv_gbp, window=60)`: total returns kept only where the share was in the universe at the previous close (`universe_mask(...).shift(1, fill_value=False)`), so delisting returns stay and a share's first day in the universe is dropped. `universe_turnover(mask)`: mean over consecutive month ends of (entering + leaving) / names at the earlier month end, empty months skipped, 4 places.

## Numbers stated, with sources

All computed in CPython (NumPy 2.5.3, pandas 3.0.5) and in Pyodide 0.27.7 (NumPy 2.0.2, pandas 2.2.3); identical.

- Brief checks reproduced: 235,497 listed cells, 16,503 NaN; 15 split days; rebuild error 5.2e-16; half spread median 7.31 bp; 0.1128 and 0.1301; momentum IC 0.0325, t 2.64, 47 dates (log-sum method).
- l1: 180 listed on day 0; today's list 180, of which 160 listed on day 0 (20 not yet listed, 20 listed then but dead later); universe empty for 59 days, first date 26 March 2019 with 165 shares, then 165 to 180 (169 on the last day); 16 shares below £5m; S046 lists 7 April 2021 (£11.7m), joins 29 June 2021; S012 (£35.6m) dies 18 January 2022 at -82.89%. `toy`: E's 60-day mean on 3 May 2019 £5.15m (2 May £4.975m), whole-sample mean £6.375m; universe [A, D] from 26 March, E from 3 May, C from 7 May, D out from 22 May. `small` universe counts [0, 0, 26, 25, 25] at rows 0, 58, 59, 100, 299. Max listed count in a week 196.
- l2: S089 split 27 August 2021, raw 528.61 -> 260.09 (-50.80%), true return -1.59%, 100 shares worth £52,860.52 then 200 worth £52,018.32; S000 dividend £0.5183 on 1 April 2019 (104.39 -> 103.66; total -0.21%, -0.20% from the rounded numbers shown). Raw-close returns below -40%: 34 (20 deaths, 14 splits; the 15th split, S111's, falls after it died). No split and dividend on the same day in the seed. 110 dividend payers.
- l3: EW index of £100: everyone £164.17, today's 180 £179.06 (gap £14.89). Momentum study, 47 monthly dates, signal sum of log returns over 231 days shifted 21, fwd = `forward_returns(ret, 21)`: everyone mean IC 0.0334 (t 2.76), top fifth 18.66%, bottom 6.78%, spread 11.88% (mean monthly x 12); today's 180: 0.0317 (t 2.30), 20.68%, 9.66%, 11.02%. Dropping the 20 delisting returns: 12.79% (87% of the 1.73-point gap). Filling dead shares with 0 after death: 10.72%. Mean delisting return -70.9%, mean listed count 186.9, rule-of-thumb bias 1.52% a year. `small`: (0.0826, 0.1654), deaths S007, S012, S029. Delisting returns on the full panel from -54.87% to -93.52%. Shumway (1997), about -30% for performance delistings, cited for a missing delisting return.
- l4: past five-day return signal against five-day forward returns on 249 weekly dates: rank IC -0.0243 (t -4.54) correct, +0.1697 (t 32.44) with the off-by-one `shift(-4)`; momentum 0.0334 against 0.0366 with the same leak.
- homework: `clean_panel` on `make_panel()` keeps 207,419 returns, mean 9.58% a year; `universe_turnover` 0.0036 on `make_panel()` (only listings and deaths change it, since volume is constant per share) and 0.0178 on `small`. Hand-made numbers in quiz, review and homework items were each computed in Python.

## Proposed change to course.json

None.

## Backlog

Two bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (alpha level 1)": the bars validator accepting `x`-prefixed ids for object categories, and the import scan missing `import numpy as np, pandas as pd` (already raised by backtest level 1; hit again here, with the workaround later alpha levels need).
