# Delta read AF, garch: the re-authored problems and the parts the fix pass changed

Counts: `wrong` 0, `misleading` 1, `reuse` 1, `re-author` 0, `continuity` 0, `voice` 0, `other` 1. No key and no `wrong` value is mistaken. Every band in scope takes both the value its printed working gives and the unrounded carry. The four `wrong` and four `misleading` findings of the second read are all closed.

Scope, at commit 409f8214 (fix pass commits 012b5453, fbf463c1, 409f8214 against e09c4825, 990151ba, b23d81d3), from `docs/reviews/review-problems-garch-1-3.md` and its `## Fix pass`:

- `garch/problems-1`: `p-stale-alarm` (new, all four parts); `p-stale-prices-scaling` parts 1 and 4 (lines); `p-eight-day-window` part 3 (key, band, lines); `p-big-day-indicator` part 4 (question).
- `garch/problems-2`: `p-two-filters-one-score` part 3 (key); `p-weekly-gas-arch` parts 1, 3 and 5 (lines, question); `p-silver-moment-fit` parts 2 and 4 (lines; question, key, slips); `p-crash-then-quiet` prose and parts 1, 3 and 4.
- `garch/problems-3`: `p-forecasts-to-parameters` parts 1, 3 and 4 (lines, question); `p-bank-index-flat-var` parts 1 to 4 (lines; part 4 question and key); `p-recalibrate-short-var` prose and parts 1, 3 and 4 (lines, bands); `p-monthly-sleeve` (new, all four parts).
- Exams read for reuse: `exams/topic-2.2.json` (7 garch items) and `exams/stage-2.json` (`b-arch-lm`, `b-garch-target`, `b-ewma-update`, `b-es-normal`). No mock exam holds a garch item (grep of `exams/mock-*.json` for GARCH, EWMA, Kupiec, kurtosis, VaR, expected shortfall: no file).

Method. Each part in scope was solved from its text before its key was read. No browser, no content or engine edit.

- `docs/reports/delta-review-delta-af-garch-numbers.py` (scratchpad venv Python) imports no earlier script. Routes: the storm day's tail by `scipy` and again by integrating its density beyond the alarm level; the kurtosis of the rescaled day by integration and by 2,000,000 draws; 312.24 from the banded covariance matrix of 252 days; a loop over every count from 0 to 75 for the LM part; exact fractions for the tied key; the lag-1 ACF formula solved for $\alpha$ by a root find, then a 1,500,000-day simulation of the fitted model; the EWMA stepped day by day for the crossing day; `binom.logpmf` for Kupiec; the ES multiplier by integrating the tail; the 84 daily forecasts of the sleeve stepped by the recursion and summed month by month. Each band is rebuilt with the engine's rule and fed what a learner types from the part's rounded working and from the unrounded carry.
- Reuse. The learner-facing text of all 12 lessons, three reviews, three homework sets and the topic exam was printed with the second reader's `taught.py`. Lessons 1, 3, 9 and 12 were read in full against the two new problems, with the reviews, homework and exam stems of levels 1 and 3. `stage-2.json` was walked for every item with a `gv-` skill. Greps of `app/content` for cocoa, crop failure, alarm, risk screen, screen sd, sleeve, pension scheme, airline index.
- Fixes. Each of the 25 applied findings was read in the file against the review's replacement text. The three fixes below were applied to a scratch copy and tested, then the copy was dropped.

## Tool results

| check | result |
|---|---|
| author's `problems-garch-numbers.py` | 835 of 835 direct, 163 of 163 `numbers_lib`, exit 0 (the fix pass reports 419 `numbers_lib` checks; the run here prints 163) |
| second reader's `problems-garch-numbers-read.py` | 556 checks, 0 FINDING lines, exit 0 |
| `delta-review-delta-af-garch-numbers.py` | 216 checks, 0 failed, 3 FINDING rows, exit 0 |
| validator | 0 errors, 4588 warnings, none on `garch/problems-*`; `manifest.json` restored |
| voice scan 35, course folder | 0 and 0 |
| `grade-all.mjs --file`, three sets | 0 failures each |
| `fresh-check.mjs --file`, three sets | 0 hits each; problems-3 has the 4 advisories the fix pass lists |
| scratch copy with findings 1 to 3 applied | `fresh-check --content` 0 hits on problems-1 and problems-3, `grade-all --file` 0 failures on both, voice 0 and 0 |

## The eight wrong and misleading findings of the second read

| Second read | Fix | Checked here | Verdict |
|---|---|---|---|
| 5, wrong: band refused 28.34 from the printed $s$ | key 0.28336, tol 0.00011 | $\sqrt{252} \times 1.785 = 28.3360$; 28.34 and 28.33 taken, 28.32 and 28.35 refused; slips at 26.55 and 34.10 routed | closed |
| 7, wrong: "smallest count" was 0 | question limited to counts above 3.75 | loop over 0 to 75: 0 rejects ($LM = 4.15$), 1 to 7 do not, 8 does ($LM = 5.33$); 8 is the smallest above 3.75 | closed |
| 8, wrong: key on an exact tie | key 1.65365 | day 3 is exactly 165365/100000 in fractions; 1.6536 and 1.6537 taken, 1.6535 and 1.6538 refused | closed |
| 26, wrong: bands refused the unrounded $c$ | tol 5 in parts 3 and 4 | rounded $c$: £76,945 and £91,770; unrounded: £76,948 and £91,774; all four taken | closed; one slip band left narrow (finding 2) |
| 14, misleading: $\alpha$ against the ACF | $\alpha = 0.13$, $\beta = 0.83$ | the stem's lag-3 value 0.25 with $\phi = 0.96$ needs $\alpha = 0.1278$; $\alpha = 0.13$ gives lag 3 of 0.2555 and lag 4 of 0.2453; simulation agrees; $3\alpha^2 + 2\alpha\beta + \beta^2 = 0.955 < 1$, so the ACF exists; key $\sqrt{5.1468} = 2.2687\%$ | closed |
| 22, misleading: forecast below the model's floor | a refitted model, 0.50% | the first fit's floor is $\sqrt{0.06/0.09} = 0.8165\%$, above the cap point 0.5543%, so the 0.50% cannot be its forecast; the question now names a new fit, and states no parameters for it to contradict; key £218,090.63, slips £241,796 and £174,472.50 | closed |
| 3, misleading: "understates by about 11%" | "about 11% above the reported one" | $\sqrt{312.24/252} = 1.1131$ | closed |
| 18, misleading: "expect to report" | "does that day-30 forecast give" | wording only; £133,474 from 0.7172%, £133,474 from the unrounded vol | closed |

## Verdict per item

| Item | Changed | Numbers and bands | Reuse | Chain |
|---|---|---|---|---|
| `p-stale-alarm` | new | clean | clean chain; two lines of part 4 (finding 1) | holds |
| `p-stale-prices-scaling` | parts 1, 4 lines | clean | clean | holds |
| `p-eight-day-window` | part 3 | clean | clean | holds |
| `p-big-day-indicator` | part 4 question | clean | clean | holds |
| `p-two-filters-one-score` | part 3 key | clean | clean | holds |
| `p-weekly-gas-arch` | parts 1, 3, 5 | clean | clean | holds; part 3 now restates $V = 9.23$ |
| `p-silver-moment-fit` | parts 2, 4 | clean | clean | holds |
| `p-crash-then-quiet` | prose, parts 1, 3, 4 | clean | clean | holds |
| `p-forecasts-to-parameters` | parts 1, 3, 4 | clean | clean | holds |
| `p-bank-index-flat-var` | parts 1 to 4 | clean | clean | holds |
| `p-recalibrate-short-var` | prose, parts 1, 3, 4 | clean; one slip band (finding 2) | clean, one likeness below | holds |
| `p-monthly-sleeve` | new | clean; one printed number (finding 3) | clean, likenesses below | holds |

### `p-stale-alarm`: clean, with one line group

The stem is consistent: 14.5% a year is 0.9134% a day, the alarm sits at 2.74%, and a storm day with sd 2.1% is 1.305 sds from it. Part 2's key, 19.1974%, follows the 2.74 the question restates; the unrounded carry gives 19.1935% and both type as 19.2. Part 3 takes 71.1 from 19.2/0.27, from the unrounded chance and from the exact normal rate. Part 4's key is 3 by integration and by simulation.

Closest material, with texts.

- l1 screen 11, a stale window in a storm: "The desk sizes its positions from the 250-day figure ... It treats a 44% storm as a 19% day, so its positions carry more than twice the risk it intends." The problem shares the idea of a trailing figure held into a storm. Its chain (an alarm level, a tail chance under the wrong sd, a ratio of rates, a kurtosis) is on no screen, and no sentence is shared. Clean.
- l4 quiz 1, part 1's step: "A fund's risk limit is 10% annual volatility. What daily sd does that allow", slips "You divided by 252. The sd scales by $\sqrt{252}$." and "You used calendar days. Use 252 trading days." Problem: "You divided 14.5% by 252. The screen multiplied the daily sd by $\sqrt{252}$, so undo that." and "You divided by $\sqrt{365}$. The screen annualises with 252 trading days." The standard task with its standard slips, in other sentences. Clean.
- l3 screen 0 and review-1 item 6, part 3's rate: "A normal puts 0.0027 of its mass beyond ±3 sds", "30 observed is more than four times that". The problem divides its own 19.2% by the same constant. Clean.
- l3 screen 10 and l3 quiz 0, part 4: reuse of two lines, finding 1. The task itself, a kurtosis that a change of scale leaves alone, is l3 screen 10's on a new setting, and the point it makes (the alarms are clustering, not fat tails) is the level's own, as in l3 screen 8: "Fat tails here are clustering seen through a histogram." No sentence of that screen is used.
- Exams: `e-mixed-window` is no longer walked (no shares, no mixture, no window sd). Nothing in `stage-2` is close.
- Story: cocoa appears once elsewhere, in `coint/problems-1` (cocoa futures regressed on a chip index); no alarm rule or risk screen of this kind anywhere in `app/content`.

### `p-monthly-sleeve`: clean

The stem is consistent: $2.56 - 0.81 = 1.75$, and the 84 daily forecasts stepped by the recursion match the closed form. Month 1 is 43.3484, month 2 is 29.4741, month 4 is 19.8013, and the weights rise 0.3946, 0.4786, 0.5428, 0.5839. Part 2 takes 0.3946 from 43.35, from the unrounded sum, from the printed $2.598/6.584$ and from $9/\sqrt{12 \times 43.35}$. Part 4 takes 0.189 from every carry.

Closest material, with texts.

- l9 screens 4, 6 and 11 and quiz 1, a horizon variance as a sum of daily forecasts: "Add the five daily variances, then take the square root of the total."; "Sum the 63 daily variance forecasts, scale by 252/63 and take the root". There the sum is read from a table or code. Here it is a geometric series in closed form, and the slips are the problem's own (`powers-from-one`). The `flat` slip is the lesson's $\sqrt{h}$ trap in other words: lesson "That assumes all five days are as stormy as tomorrow, but the forecast is already fading."; problem "53.76 is 21 days at tomorrow's 2.56 %². The gap shrinks by 0.965 a day, so later days are calmer." Clean.
- l12 screen 2, quiz 0, review-3 item 3 and, in the set, `p-bank-index-flat-var` part 2, a weight as target over forecast. Part 2 is that step on a monthly footing with no cap. It shares the slip id `times-252` and the word "footing" with the set's other sizing part, and nothing else. The second read asked that the new problem not walk that part; it does not, since the forecast is a month's and the scaling is $\sqrt{12}$. Clean, noted.
- homework-1 item 1, an annual limit scaled to a week: one step of part 2 with other numbers. Clean.
- Parts 3 and 4, the monthly factor $0.965^{21}$ and the telescoping buys, are on no screen. The second read let the telescoping step stand.
- Exams: `e-vol-ahead` and `e-breach-days` (the advisory's 21, 1.75 and 42 are a day number, a return and a day number there). Nothing close in `stage-2`.
- Story: a pension scheme appears twice in `convex` (asset splits under constraints), an airline index nowhere.

### Likeness noted, not raised

- `p-recalibrate-short-var` part 4 and `stage-2` `b-es-normal`: both ask a 97.5% normal ES on a £3m position. Stage: "A GARCH model forecasts tomorrow's volatility at 0.014 for a £3,000,000 position ... one-day 97.5% expected shortfall", slip "You forgot to divide by the tail mass 0.025." Problem: "Using the recalibrated vol $1.1379 \times 1.15\%$ from part 3, what is the ES?", slip (as fixed) "£2,294 is the density times the vol and the position. The mean loss in the tail divides that by the tail's size, 0.025." The level and its constants are the standard ones; the one free number shared is the £3m. The vols, answers and sentences differ, and the stage test comes after the set. The second read did not open `stage-2`. Left as it is.

## Findings

Format: `N. file | JSON path | class | problem | evidence | exact fix`.

1. `garch/problems-1.json` | `items[0].parts[3].feedback.byKey.excess`, `.feedback.generic` | **reuse** | two lines of the new part retell l3 quiz 0 and l3 screen 10 | l3 quiz 0: "That is the excess kurtosis. The question asks for the raw value." Problem: "0 is the excess kurtosis. The question asks for the raw figure, which adds 3." l3 screen 10: "Kurtosis has no units: top and bottom both carry the fourth power of the scale." Problem: "Kurtosis is the fourth moment over the squared variance, and both carry the same scale." The checker reports neither | `excess`: `0 is what is left once the normal's 3 is taken off. This part keeps the 3 in.` `generic`: `Not quite. $x$ is a normal draw with sd 2.299, not 1. Work out its kurtosis from that.` Tested on a scratch copy: fresh-check 0 hits, grade-all 0 failures, voice 0 and 0.

2. `garch/problems-3.json` | `items[2].parts[2].widget.wrong[1].tol` (`inverted`) | **other** | the fix to finding 26 widened the key band for a learner who keeps $c$ in the calculator, and left this slip's band at 1.5 | the slip with the rounded $c$ is $67620/1.1379 = £59{,}425$; with $c = 1.96/1.7224$ it is £59,423, which the band refuses, so that learner gets the generic line | `tol.abs`: `5` (takes £59,423 and £59,425; the key is £17,500 away). Part 4's `no-divide` needs no change: £2,294 from both carries. Tested on the scratch copy with finding 3.

3. `garch/problems-3.json` | `items[3].parts[3].explain.text` | **misleading** | the first of the three buys is printed as 0.0839 | the part works from the 0.3946 it restates: $2.598/\sqrt{29.47} = 0.4786$, and $0.4786 - 0.3946 = 0.0840$ (0.08395 unrounded). 0.0839 comes only from the unrounded weight 0.394608. As printed, $0.0839 + 0.0643 + 0.0410 = 0.1892$, beside a line that says the sum is $0.5839 - 0.3946 = 0.1893$ | replace `The three buys are 0.0839, 0.0643 and 0.0410` with `The three buys are 0.0840, 0.0643 and 0.0410`. The three then sum to 0.1893. The key and every band stand.

## Verified with no finding

- Every fix of findings 2 to 26 is in the file as the review gave it; finding 22 carries the one sentence split the fix pass records.
- `p-stale-prices-scaling`: 0.0566; $1.96/1200 = 0.0016$ routed; 312.24 by the covariance matrix; the pairs add 23.9%.
- `p-eight-day-window` part 3: $\sqrt{365} \times 1.785 = 34.10$, as the new `calendar` line prints.
- `p-big-day-indicator` part 4: 0.0456 and 3.12 at 7 days; 0.0506 from both routes.
- `p-weekly-gas-arch`: 9.23, 56.4, 25.74, the gap 16.51, $\omega = 0.7385$, 25.40 from the rounded and the unrounded $\omega$; "6.0 is the variance after a week with no move at all" is true of the rule.
- `p-silver-moment-fit` part 2: 16.98 days, 3.4 trading weeks; slips 25 and 12.5. Part 4: slips 5.1468, 1.7605% and 36.01%; 33% above 1.70%.
- `p-crash-then-quiet`: 2.9495, 30 times, 2.4 times; 2.8100 with slips 2.8020 and 2.8220; ARCH 0.872; the closed form matches the stepped filter; first day below 0.872 is 27; 0.895 after 26 days; 24 with no floor.
- `p-forecasts-to-parameters`: 0.0244, 0.5144, 0.7172%; £133,474, £94,378, £154,590, down 14%.
- `p-bank-index-flat-var`: 1.7514%, 27.803%, 0.3956, 6.28, 441%, £170,951; part 4 as in the table above. The 1.44 that raised finding 9 is gone and `fresh-check` on problems-2 has 0 hits.
- `p-recalibrate-short-var`: $\Phi^{-1}(0.9575) = 1.7224$ and $\varphi(1.96) = 0.058441$; scores $-72.408$ and $-70.324$, gap 2.084, LR 4.168, p-value 0.041; the ES multiplier 2.3376 by integration.
- No `wrong` band in scope overlaps its key band. Percentage parts carry the unit "%".

## Engine

1. A `wrong` value built from a carried value can keep a narrower tolerance than the key of its own part (finding 2). The validator could flag a slip band narrower than the key band in a part whose question says "Using x from part k".
2. `fresh-check.mjs --file` reads the topic exam only as an advisory and does not read the stage exams: `stage-2` `b-es-normal` shares the level and the £3m of `p-recalibrate-short-var` part 4 and drew nothing.
3. `retold` still misses a line that differs by one word and a tail clause: "That is the excess kurtosis. The question asks for the raw value." against "0 is the excess kurtosis. The question asks for the raw figure, which adds 3." (finding 1).

Inbox bullets: `docs/BACKLOG-INBOX.md`, `Raised later (delta read AF garch):`.

## Fix pass

1. fixed: `p-stale-alarm` part 4 `excess` and `generic` lines replaced with the review's text.
2. fixed: `p-recalibrate-short-var` part 3 slip `inverted` tol.abs 1.5 to 5 (59,425.26 and 59,423 both taken; key £17,500 away).
3. fixed: `p-monthly-sleeve` part 4 explain now prints 0.0840 (the three buys sum to 0.1893). Author script lines 579 and 587 updated to 0.0840, with the 0.08395 unrounded buy given tolerance 6e-5.

Gates: validator 0 errors; voice scan 35 0 and 0; fresh-check 0 hits on problems-1 and problems-3 (problems-3 keeps its 4 advisories); grade-all 0 failures on both; playthrough with and without `--mobile` passed on both; scripts exit 0 (author 835 and 163, reader 556, delta 216 with 0 FINDING rows). Graded answers changed: none.
