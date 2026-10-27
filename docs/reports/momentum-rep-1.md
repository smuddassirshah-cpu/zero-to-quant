# momentum-rep level 1 (The paper): report

## Files written

All in `app/content/courses/momentum-rep/`, £ for money, ids and titles from `course.json`.

| File | Screens / items | Skills | Canvases | Code |
|---|---|---|---|---|
| `l1-reading-a-paper.json` | 9 screens, 4 quiz | `rm-paper` | table (claims tap, sections ordered tap, zero-cost position, abstract, Paper Q, margin notes) | none (as the brief says) |
| `l2-jt-design.json` | 10 screens, 4 quiz | `rm-paper` | series timeline (J and K sliders driving `shade` ends through `derive`), grid staircase of live cohorts | `live_cohorts(t, J, K, skip=0)` |
| `l3-main-table.json` | 9 screens, 4 quiz | `rm-paper` | table (JT layout mock-up, 4 × 4 grid), number-line (t against 1.96 and 2.58; annual), bars (ten decile means) | `annualise`, `t_stat` (pure Python) |
| `l4-what-to-replicate.json` | 9 screens, 3 quiz | `rm-paper`, `rm-data` | table, number-line with a k slider driving the tolerance band | `within_tolerance`, `matches` (pure Python) |
| `l5-replication-plan.json` | 10 screens, 4 quiz | `rm-paper`, `rm-stats` | console (buggy log, placebo logs), graph (plan steps, ordered tap, arrows in the Why? copy) | `weights_ok` (pure Python), `placebo_spread` (NumPy, generator in the prelude) |
| `review-1.json` | 9 items, difficulty 2 to 4, two per lesson (one for l4 plus one shared l4/l5) | as each item | console tap item | none |
| `homework-1.json` | 8 items, difficulty 3 to 5 (two at 5) | `rm-paper`, `rm-stats` | | `jt_layout` (5), `cohort_calendar` (4); `order` item (reading order); `longform` (5, 10-point rubric, full model answer) |

Lesson shapes. l1: hook (testable claims), explore (reading order), name (zero-cost), three ladders (design, signal, edge case raw against adjusted), trap (12.01% as return on capital), generalise, transfer (first hour with an SSRN paper). l2: explore (J/K sliders), name (cohort), skip ladder, live-cohort staircase, month 20 ladder, weight ladder, trap (non-overlapping), generalise with the K = 1 edge case, code, transfer (12 sleeves). l3: hook (read the layout), explore (largest and smallest cell), name (t), ladders (edge case 12/12 high mean low t, monthly to yearly), trap (Sell row on decile bars), generalise, code, transfer (after costs). l4: hook (sort targets), explore (tolerance band), name (match), ladders (apply the rule, edge case a misprinted cell), trap (best of sixteen), generalise, code, transfer (what exactly did you reproduce). l5: hook (log with a look-ahead bug), explore (plan steps), name (check), ladders (weights check, reading the placebo), trap (no placebo), derive (`order` with a `same` group for the two robustness steps), two code screens, transfer (first commit); edge case (data the free sources lack) in the quiz.

Build scripts, helpers and checks are in `/tmp/claude-0/-home-user-zero-to-quant/98c5513d-912f-5001-9d0f-5e8b213473d3/scratchpad/momentum-rep-1/`: `gen.py` (the generator verbatim and loop reference functions), `gen_prelude.py` (the generator verbatim plus a vectorised `formation_returns`, used as the l5 prelude), `ref.py` to `ref5.py` (first computation), `twice.py` (second, independent computation), `build_l1.py` to `build_l5.py`, `build_sets.py`, `checkcode.py` (runs every code widget's solution and starter against its hidden tests in CPython), `voice.py` (sentence length, dashes, exclamation marks).

## Validator

`node tools/validate.mjs` from `app/`: 0 errors. One warning in these files: `l3-main-table.json screens[4].hints[1]` (the annualise ladder's point hint has nothing to highlight, because its number-line starts empty and the answer is drawn only in the Why? copy). The course-level warning lists the ten level 2 and 3 lessons not yet written.

## Playthrough

All with `--local-cdn /tmp/claude-0/-home-user-zero-to-quant/98c5513d-912f-5001-9d0f-5e8b213473d3/scratchpad/pkgs`:

- l1-reading-a-paper: ok, 13 checks, quiz 4/4.
- l2-jt-design: ok, 14 checks, quiz 4/4.
- l3-main-table: ok, 13 checks, quiz 4/4.
- l4-what-to-replicate: ok, 12 checks, quiz 3/3.
- l5-replication-plan: ok, 14 checks, quiz 4/4 (the NumPy placebo screen passes in Pyodide with the CPython expected values to 1e-6 relative).
- review-1: ok, 9 of 9 recorded.
- homework-1: ok, 8 of 8 marked right, 37 of 37 marks.

Screenshots at 1280 px with `--why` and at 390 px with `--mobile` (folders `shots/` and `mshots/` in the scratchpad) were inspected. Fixes made: number-line labels "12/12" and "3/12" rendered as fractions (now "12/12 cell"); the l3 layout table scrolled sideways on a phone (now compact with short K headers); the l5 plan graph overlapped on both widths (nodes moved to the frame edges, labels shortened, and the Why? copy rearranges them into a snake with arrows); the l4 band label sat on the bar; starter comments ran past the editor edge (moved onto their own lines); the skip month is now a separate red band on the l2 timeline.

Starters: `checkcode.py` runs every code widget in CPython. Every solution passes all its tests; no starter passes all of its tests (most pass none; `t_stat`/`annualise` passes 1 of 8, `within_tolerance` 1 of 10, `cohort_calendar` 2 of 8, each on a trivial case such as an empty list).

## Numbers and how each was computed twice

First computation: `ref.py` to `ref5.py` with `gen.py` (loop formation returns, `cohort_weights` with the double stable argsort and `rank * q // n`, `wml` averaging the K cohorts' weights). Second computation: `twice.py` with `gen_prelude.py` (vectorised formation returns, weights from one argsort, the composite as the mean of each live cohort's own spread, an index-based shuffle). Code-test values were checked a third time in Pyodide by the playthrough.

| Number (where) | First | Second |
|---|---|---|
| 4 × 4 table no skip, all 16 means and t (l3, l4) | `ref.py`: identical to the course context to 2 places | `twice.py` spot cells 6/6, 12/3, 12/12, 3/12, 3/3 |
| 6/6: 0.96% (0.009639), sd 5.98%, 289 months, t 2.74 | `ref.py`, `ref3.py` | `twice.py` |
| 12/3 1.31% t 3.18; 12/12 0.66% t 1.77, sd 6.21%, 277 months; 3/12 0.63% t 2.98 | `ref3.py` | `twice.py` |
| Layout mock-up Sell and Buy legs for J = 6 and 12 (l3) | `ref3.py` decile composites (Buy − Sell equals `wml` to 4 places) | `twice.py` decile loop |
| Ten decile means of the 6/6 composite 1.04 to 2.01 (l3 bars) | `ref2.py` | `twice.py` |
| t from rounded inputs 0.96 / (5.98 / 17) = 2.73 | Python | by hand: 5.98 / 17 = 0.352, 0.96 / 0.352 = 2.73 |
| (1.0095)^12 − 1 = 12.01%, (1.0131)^12 − 1 = 16.90%, (1.0077)^12 − 1 = 9.64%, (1.005)^12 − 1 = 6.17%; ×12 gives 11.40%, 15.72%, 9.24%, 6.00% | `**` power | `expm1(12 log1p(m))` |
| Net of costs: 1.00 − 0.577 × 0.25 = 0.856%; 0.9639 − 0.577 × 0.25 = 0.82%; 0.96 − 0.577 × 0.50 = 0.6715% | Python | by hand; 0.577 is the course context's two-sided 6/6 turnover |
| Months for 12/12 to reach t 1.96: (1.96 × 6.21 / 0.66)² = 340.1, so 341 | Python | (1.96 / 1.766)² × 277 = 341.2 from unrounded values; the item accepts 340 to 342 |
| Look-ahead bug (window t − 5 to t): 17.06% a month, t 41.20 (l5, base panel) | `ref2.py` | `twice.py` (the formation return known at t + 1) |
| Same bug on the shuffled base panel (seed 0): 17.86%, t 137.79; correct code there 0.04%, t 0.25; correct 6/1 on the base panel 0.52%, t 1.14 | `ref5.py` | `twice.py` |
| `placebo_spread` on `momentum_panel(n=200, T=120)`: seed 0 J 6 −0.004169197 (t −1.17, 114 months), seed 1 0.001131606, J 3 seed 0 −0.004339038, J 12 seed 5 −0.003021951; flat panel 0.018 | `ref2.py`, `ref4.py` | `twice.py`, then Pyodide (playthrough) |
| Gaps in standard errors: 0.33 / 0.30 = 1.10, 0.79 / 0.33 = 2.39, 0.61 / 0.30 = 2.03, 0.54 / 0.30 = 1.8; band ends 0.95 ± 0.6 = 0.35; 6.0 / 17 = 0.353 | Python | by hand |
| Code-test `expect` values (`live_cohorts`, `annualise`, `t_stat`, `within_tolerance`, `matches`, `weights_ok`, `jt_layout`, `cohort_calendar`) | the solution run in CPython (`checkcode.py`) | the hand cases worked on paper (for example `t_stat([1, 3]) = 2.0`, `cohort_calendar(300, 6, 6)` has 289 full months = 300 − 11); Pyodide in the playthrough |

Hypothetical numbers that are labelled as made up on screen: the colleague's free-data cells (0.41, 0.62, 0.52, 0.70 with their standard errors), Paper Q's 0.6% alpha and 0.9% raw spread, the misprinted row (1.20, 1.71, 0.59), the l1 and quiz £ positions, the review log with winners at +1/45.

Paper figures quoted, always as "the paper reports" or from the abstract paraphrase, and only from the course context's list: 6/6 about 0.95% a month and 12.01% a year compounded; 12/3 about 1.31%, the most profitable cell; skipping a week raises every cell a little; t statistics of about 3 to 4; part of the first-year gain reverses in years two and three; the losers' returns are concentrated in January; NYSE and AMEX, 1965 to 1989. No other cell of the paper is stated anywhere. No later papers are named in level 1.

## Seeds and conventions

- Generator: `momentum_panel` verbatim from the brief, seed 2 (`n = 500, T = 300`) for the base panel and `momentum_panel(n=200, T=120)` for the code tests. Shuffle: `np.random.default_rng(seed).permutation` of each share's column in turn, seed 0 unless a test says otherwise.
- `formation_returns` in the l5 prelude is the course context's reference definition (months t − skip − J to t − skip − 1, `np.expm1` of a difference of cumulative log returns, NaN before J + skip), written vectorised; it matches the loop version exactly on three (J, skip) cases.
- Weights: +1/size on the top decile and −1/size on the bottom, deciles `rank * 10 // n` with a double stable argsort. Live cohorts in month t: `max(J + skip, t − K + 1)` to t.
- Two-sided turnover (both legs, gross 2) for costs, named as "counting buys and sells" on screen; costs charged per £1 traded.
- Plain t statistic: mean over (sd with ddof 1 / √n).

## Departures from the brief

- Reference scripts `momfinal.py` and `momext2.py` were absent, as the orchestrator said; every value was recomputed from the generator printed in the brief. All the course-context values I used agree with my computation.
- l5's look-ahead bug: the brief says "gets 15% a month"; with a window of months t − 5 to t on the base panel the bug gives 17.06% (t 41.20), so the lesson quotes 17%.
- l1's reading-order explore uses an ordered `tap-regions` on a table, not a `place` in order mode, because an explore screen needs a canvas-bound widget. The plan steps in l5 likewise use an ordered tap on a `graph` for the explore, and an `order` widget for the derive.
- l3's decile `bars` show the full-sample means of the 6/6 decile composites rather than one formation's: one formation (month 100) is too noisy to show the pattern (its ten deciles do not rise in order).
- l4's three buckets are labelled "Match the number", "Match sign and pattern" and "Out of reach with our data" (the brief's "reproduce exactly" would claim our seeded panel reproduces the paper's digits).
- The l3 layout mock-up shows only J = 6 and J = 12 (six rows) to fit a phone; the explore screen carries all sixteen Buy − Sell cells.

## Proposed course.json change

None.

## Backlog

Five bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (momentum-rep level 1):".
