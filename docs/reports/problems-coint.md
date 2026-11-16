# Problem sets: coint, levels 1 to 3 (brief `docs/briefs/chained-prompts.md`, Author)

Files: `app/content/courses/coint/problems-1.json` (4 problems, 17 parts), `problems-2.json` (4, 18), `problems-3.json` (4, 20). Numbers: `docs/reports/problems-coint-numbers.py` (770 checks, 0 failures, exit 0). Commits: 18d5669d (level 1), 62b9517e (level 2), then level 3 with this report.

This is a resumed pass. The first author's drafts were judged against the brief. Three problems walked a course setting and were replaced: `p-designed-tie` (level 1, the design $y = x + u$ with $\text{Var}(\Delta u) = 2\text{Var}(u)(1 - \phi)$ and the correlation of daily changes, which is l2 screens[3] and [4] and homework-1 items[3] run backwards), `p-false-alarms` (level 3, l11's rolling ADF every 125 days on 250, two checks above 0.5 against the first above 0.10, and an option paraphrasing l11 screens[9] "a known price") and `p-insurer-trading-years` (level 3, homework-3's report: 2,520 days split at 1,260, costs, Sharpe, $1/\sqrt 5$). The other nine drafts stand, each recomputed.

## Sets

| set | item | parts (numeric / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-paper-mill-multiple | 4 (3 / 1) | l2, l3, l4 | 4 |
| problems-1 | p-cocoa-chip-levels | 4 (3 / 1) | l1, l4 | 3 |
| problems-1 | p-cable-sample-length (new) | 4 (4 / 0) | l3, l4 | 5 |
| problems-1 | p-screen-real-share (fix pass, for p-utility-step-two) | 5 (5 / 0) | l2, l4 | 4 |
| problems-2 | p-smelter-tls (fix pass, for p-cement-three-ratios) | 4 (4 / 0) | l5, l6 | 4 |
| problems-2 | p-lessor-window | 4 (4 / 0) | l6, l7 | 4 |
| problems-2 | p-three-distributors | 5 (4 / 1) | l8, l6 | 4 |
| problems-2 | p-tyre-vecm | 4 (3 / 1) | l8, l7 | 5 |
| problems-3 | p-glassmaker-borrow (fix pass, for p-packaging-stop-reopen) | 5 (4 / 1) | l9, l10 | 4 |
| problems-3 | p-stop-edge | 5 (5 / 0) | l9, l11 | 5 |
| problems-3 | p-half-life-alarms (new) | 5 (5 / 0) | l11, l12 | 4 |
| problems-3 | p-housebuilder-trading-years (new) | 5 (5 / 0) | l10, l12 | 4 |

Typed parts after the fix pass: 15 of 17, 15 of 17, 19 of 20. Choice parts are judgements (which multiple least squares finds, the verdict against MacKinnon's values, whether a pair can hide inside a rank-1 triple, what a zero speed does, what leaving borrowing fees out does to a backtest).

New chains: $\gamma = 0.96 - 1 = -0.04$; rough guide $t_\gamma = -0.04/\sqrt{0.0784/250} = -2.26$; 547 days to reach −3.34; 1,105 days at $\phi = 0.98$ (prose calls it a rough guide: the script's simulation shows the real Engle-Granger statistic usually misses at 250 days and usually rejects at the guide's days). Alarms: $1 - 0.86^4 = 0.4530$; $0.0196 \times 2.72 = 0.0533$; 15.99 more false stops of 40; £12.98 cheaper; break-even £9.33. Housebuilders: £0.0375 a day; Sharpe 1.08; 1.53 standard errors; 3.43 years; 361 more days.

## Gates

- Validator: 0 errors; no warnings on the three files (4,571 in all, as before).
- Voice scan (`VOICE_BASE=app/content/courses/coint`, 35): 0 and 0.
- Number script: exit 0. Every key twice (exact or sympy, then simulation, enumeration, statsmodels on built data, eigen solver or a day-by-day loop), every `wrong` value matched to its slip and outside the key band, printed numbers checked.
- `fresh-check.mjs --file`: 0 hits on each set. Advisories, judged clean: set 1 shares MacKinnon's −3.04 and the ADF −2.86 with l4 (course constants), 750 and 1,500 with l9 (sample lengths), the step-two equation with l4 screens[10] (the test itself, quoted), 0.55 and 0.08 with review-3 (a p-value list; ours are a residual sd and $\hat\gamma$). Set 2 shares Johansen's 95% values 29.80, 15.49, 3.84 with l8 and homework-2 (tables).
- `grade-all.mjs --file`: 0 failures on each (17, 18, 20 widgets).
- Playthrough with and without `--mobile`: green on all three sets. Shots at 440 px read: no overflow or clipping.

## Reuse, by hand (closest lesson screen, review item, homework item)

- p-paper-mill-multiple: l2 screens[8] (gap of two correlated walks spreads), review-1 items[3] (sd of $y - 0.5x$ at day 100), homework-1 items[2]. Here the gap holds a stationary AR(1) plus a wrong multiple's walk; the chain is long-run sd, sd at day 500, the day the sd doubles, then where least squares lands. None of the three asks any of those.
- p-cocoa-chip-levels: l1 quiz[0] and review-1 items[0] ($|t|$ from $r$, one step), homework-1 items[5]. Our part 1 is that standard task with its own numbers; parts 2 to 4 (smallest $|r|$ passing 1.96, the doubled sample, the residual verdict) are not in the course.
- p-cable-sample-length: l4 quiz[1] (power from a count), l4 screens[10], review-1 items[6]. No item turns $\phi$ into $\gamma$, a guide statistic, or a sample length.
- p-utility-step-two: removed in the fix pass (it walked stage-2 `b-df-hand`); see p-screen-real-share below.
- p-cement-three-ratios: removed in the fix pass (it walked topic-2.2 `e-hedge-flip`); see p-smelter-tls below.
- p-lessor-window: l7 screens[2] and [7] (half-life, expected path to 0), review-2 items[2] and [7], homework-2 items[2]. New: the window from five half-lives and decay towards $\mu = -a/b$, not 0 or the window mean.
- p-three-distributors: l8 screens[4] and [6], quiz[3], homework-2 items[3]. New: pricing the normalised spread, its z, and why rank 1 with three non-zero weights leaves no pair.
- p-tyre-vecm: l8 screens[7], review-2 items[6] (one expected change). New: the gap's change from both legs, its half-life and the zero-speed case.
- p-packaging-stop-reopen: removed in the fix pass (it walked topic-2.2 `e-pair-positions`, l9's ladder and stage-2 `b-pair-pnl`); see p-glassmaker-borrow below.
- p-stop-edge: l9 screens[2], l11 screens[8] (names gambler's ruin, computes nothing), review-3 items[3]. Break-even hit rate, first-passage chance and the fair-bet result are not in the course.
- p-half-life-alarms: l11 screens[3] and [9], review-3 items[5], homework-3 items[6]. Those read a path of p-values or count fires in a simulation; ours is a monthly half-life check, the chance of each rule firing, and a cost comparison with break-even.
- p-housebuilder-trading-years: l10 screens[9] and quiz[2], l12 screens[7], homework-3 items[3] and its report. Own split (four years, then 504 days); the new step is inverting $S\sqrt T = 2$ for the years and days still needed.

Nothing waived. Open: none.

## Re-author and fix pass (session AF, `docs/briefs/reauthor-fix-af.md`)

Review: `docs/reviews/review-problems-coint-1-3.md` (16 findings). Three problems ruled re-author were replaced; the other findings were applied as the reader wrote them (line by line in the review's `## Fix pass`).

New problems, with the closest course and exam items (both texts read; verdict clean for each):

- p-screen-real-share (set 1, l2 and l4). 1,200 pairs, 36 truly tied, power 0.40 on two years: 14.4 real passes, 72.6 in all, 19.8% real; four years at power 0.85: 34.5%; the 1% level at power 0.65: 66.8%. Closest: l2 screens[11] ("If none of the 2,000 were truly cointegrated, about how many would still pass at 5%?"), l2 quiz[3] (pairs from 300 shares), l4 quiz[1] (power from 29 of 100), review-1 items[7] (false pairs under the ADF and Engle-Granger values), homework-1 items[6] (screen code); topic-2.2 items[7] (low power on 400 days); stage-2 none. No item mixes tied and untied pairs or asks what share of the passes is real; the count of false passes among the untied is the standard step, inside a new chain. No $t_\gamma$, no table verdict, no sums.
- p-smelter-tls (set 2, l5 and l6). From a covariance matrix ($s_{xx} = 6.25$, $s_{yy} = 4.00$, $s_{xy} = 4.60$, correlation 0.92): larger eigenvalue 9.86, TLS ratio 0.785, spread sd £0.793 (least squares minimum £0.784), today's z 2.29. Closest: l5 screens[6] (TLS in code by the eigenvector), screens[9] and review-2 items[0] (the inverted slope), review-2 items[8] (TLS and units); l6 screens[3], review-2 items[1] (a z from a mean and sd); topic-2.2 items[10] `e-hedge-flip`. It never inverts a slope or starts from two sds and a correlation; the review freed the TLS number, the spread sd and its z from another start.
- p-glassmaker-borrow (set 3, l9 and l10). Borrowing fees on the sold leg: a long borrows $1.15 \times £36.00 = £41.40$ of $x$ at 6% a year, £0.207 over 21 of 252 days; a short borrows £48.00 of $y$ at 0.5%, £0.020; the gap £0.187 moves the long entry to $-2 - 0.187/0.50 = -2.37$; a choice on what leaving fees out does to a backtest. Closest: l9 screens[2], [4], quiz[1] (the legs of each side), l10 screens[4], quiz[1], homework-3 items[1] (bid-ask or bp costs on both legs), l10 screens[11]; topic-2.2 items[13], stage-2 `b-pair-pnl`. No z path, no leg P&L, no bp on fills; borrowing fees are not in the course.

Gates after the pass: validator 0 errors (two O2-long-sentence warnings, both on the reader's replacement text, kept exact: problems-1 items[0].parts[1].question, problems-2 items[2].parts[0].feedback.correct); voice scan 35 on the course folder 0 and 0; `fresh-check --file` 0 hits on each set (advisories: set 1 three, set 2 two, as before; set 3 one, topic-2.2 items[9], a VaR chart sharing 48, 21 and 0.98, judged clean); `grade-all --file` 0 failures (17, 17, 20 widgets); number script 826 checks, 0 failures; reader's script 641 checks, 0 FINDING lines; playthrough green on all three sets with and without `--mobile` (440 px shots of sets 2 and 3 read: no overflow).

