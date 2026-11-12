# Delta read: the three problems fix passes of session AB (estimation and regression, testing, vectors)

Scope: every entry of the three "changed graded answers, bands and items" lists, read as the files stand at commit 16b0554.

- Fix pass of `review-problems-1.6-a.md` (681ffcb estimation, 01de5a2 regression): `estimation/problems-1` to `-3`, `regression/problems-1` to `-3`.
- Fix pass of `review-problems-1.6-b.md` (6bf48c8): `testing/problems-1` to `-3`.
- Fix pass of `review-problems-1.4-a.md` (26ebd3d): `vectors/problems-1` to `-3`.

Method. `difflist.py` compares each fix commit with its parent, part by part, and I held the result against the three lists: the lists are complete (no part changed that is not on them). Each listed part was then read whole (`show.py`). `recompute_a.py` and `recompute_b.py` recompute every changed answer, band and `wrong` value by my own routes (the raw readings, fractions, numpy least squares, scipy tails, enumeration of the 27 bootstrap resamples and of the 4,096 tasting sequences, a BH routine run on the full lists, the noncentral $t$ for the shoe trial), and sweep the ten re-authored items and parts for printed numbers: every number written anywhere in them, feedback and `wrong` lines included, must be one I derived. `overlap-sim.py` is my own simulation of the overlap claims of `p-overlap-signal` (2,000 runs, a hand-coded Newey-West). `grade.mjs` runs the engine's own graders (`numGrade`, and `exprGrade` with the local Compute Engine) on every answer, `accept` form and `wrong` entry of the changed parts and on 714 typed strings over 71 parts: other right forms, the value the feedback prints, a typed % and the decimal on the `%` parts, a typed unit, the answer one step short, and wrong methods against each widened band. `find.py` searches the course files and exams for each re-authored item's words, numbers and formulae; I read what it pointed at. `proposed.py` computes the numbers of every fix proposed below, twice.

Scripts: `docs/reviews/review-delta-problems-ab-1-scripts/`, run from the repo root: `recompute_a.py`, `recompute_b.py`, `overlap-sim.py`, `proposed.py` (scratchpad venv Python; `lib.py` is their shared helper); `grade.mjs --local-cdn <pkgs> [--show]`; `difflist.py <commit> [--values]`; `show.py <course> <item>[:parts]`; `find.py '<glob>' '<regex>'`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = a statement reads two ways; `minor` = otherwise.

## Tool results

- `recompute_a.py`: 341 checks, 0 failures, 0 FINDING rows. `recompute_b.py`: 336 checks, 0 failures, 1 FINDING row (finding 4). `overlap-sim.py`: 4 of 4. `proposed.py`: 23 of 23.
- `grade.mjs`: 1,327 checks, 0 failures, 24 FINDING rows (findings 1, 2, 7 and 8, and the engine notes). Every stored answer and `accept` form grades correct; every `wrong` entry typed at its stored value lands on its own id and has a line (12 wrong matrices not typed: the known engine fault, not reported).
- Authors' scripts, scratchpad venv, all exit 0: `problems-estimation-numbers.py` 1,080 checks, 0 failures; `-regression-` 1,202, 0; `-testing-` 1,120, 0; `-vectors-` 935, 0. All four pass with findings 1 to 5 in the files: none of them reads a line against what lands on it, or an option against the prose.
- `node tools/validate.mjs`: 0 errors, 4,850 warnings. On the twelve sets: three `O2-long-sentence` advisories, all in questions the passes did not touch (`p-sulphur-labs` part 3, `p-currency-vol` part 5, `p-ticket-bot` part 2). `manifest.json` unchanged.
- `fresh-check.mjs --file` on the seven sets with a re-authored item or part: 0 hits; advisories are shared formulae and small numbers only. It does not see finding 6.
- `voice-scan.py 35`: 0 and 0 on `estimation`, `regression`, `vectors`; `testing` 1 sentence, in `homework-3.json`, out of scope.
- No browser run, as asked.

## Findings

### A. Vectors

1. `wrong` | `courses/vectors/problems-1.json` `p-active-bets` `parts[1]`, `p-stress-hedge` `parts[0]`, `parts[2]`, `parts[3]`; `problems-2.json` `p-factor-risk` `parts[4]` | `feedback.byKey.decimal`.
   Each new `decimal` entry sits at the decimal rounded to the asked places, with a band wide enough to reach the real decimal. Three parts share the value $-0.0001$ with band 0.000049, so in a `%` field anything typed from $-0.0149$ to $-0.0051$ lands on the line. The line then names one decimal: "That is the decimal, $-0.0073$. ... so type $-0.73$."
   Evidence (`grade.mjs`, FINDING rows): `p-stress-hedge` part 4, typed $-0.0146$ (the `no-half` slip, $0 - 0.0146$, as a decimal) is told "That is the decimal, $-0.0073$". Part 3, typed $-0.008$ (the `old` slip, $\mathbf{w} \cdot \mathbf{s}$, as a decimal) is told "That is the decimal, $-0.0146$". In both the learner made two slips, is told a number they did not type, and is handed the answer. `p-active-bets` part 2 does the same for $-0.01$ and $-0.0095$; `p-factor-risk` part 5 for anything from 0.75 to 0.85; `p-stress-hedge` part 1 for $-0.025$ to $-0.015$.
   Fix (text only, all five parts; the bands stay, so the validator's `[wrong-band]` rule still passes): `feedback.byKey.decimal` = "That looks like a decimal. The part asks for per cent: multiply your decimal by 100." The working in per cent is already in each `feedback.correct`.

2. `minor` | `courses/vectors/problems-3.json` `p-colour-sensor` `parts[2].widget.accept` (and `p-goat-feed` `parts[2]`) | the fix of finding 6 of the first read holds for exact spellings only.
   A number in front of a bracket matrix is matched as text against the `accept` list, not computed. `1.25[[0.6,-0.4],[-0.1,1.4]]` and `\frac{1}{0.8}[[...]]` pass. `\frac{5}{4}[[0.6,-0.4],[-0.1,1.4]]` is refused with the generic line, though $\tfrac{1}{0.8} = \tfrac{5}{4}$ is the form a learner who clears the decimal writes. So are `1.25\cdot[[...]]`, `1.25\times[[...]]` and `1.25[[0.60,-0.40],[-0.10,1.40]]`; for the goat feed, `10\cdot[[...]]`. A number in front of a vector is computed (`0.2(3,4)` and `\frac15(3,4)` pass in `p-drone-crosswind`), so that part is sound.
   Fix: add `"\\frac{5}{4}[[0.6, -0.4], [-0.1, 1.4]]"` to the sensor's `accept` (tested in the grader with the entry added: accepted). The other spellings are the engine's (see Engine).

### B. Testing

3. `unclear` | `courses/testing/problems-3.json` `p-checkout-designs` `parts[4]` | the keyed answer contradicts the item's own supposition.
   The prose says "suppose no page truly differs", and parts 1 to 4 rest on it. Part 5 then keys "Pages that do improve checkout must also clear the stricter bar, so fewer of them are found" and marks wrong "Nothing: a stricter bar only removes useless launches". In the world the prose sets up there are no pages that improve checkout, so the second option is the true one: the stricter bar costs this shop nothing.
   Fix: `question` = "Under the bar from part 3, the expected waste is $18 \\times 0.002778 \\times$ £4,000 = £200. Now suppose a few pages really are better. Using parts 2 to 4, what does the stricter bar cost the shop?" No number changes.

4. `unclear` | `courses/testing/problems-3.json` `p-gene-screen` `parts[4]` | option `q-same`, its `why` and `feedback.byKey.q-same`: "so BH rejects 6".
   The prose fixes the other 52 p-values only as "all above 0.1". At $q = 0.15$ the bar for rank 60 is 0.15, so if those 52 are at 0.12 BH rejects all 60, not 6 (`recompute_b.py` FINDING row; `proposed.py`). The option is still wrong (the list grows either way) and parts 3 and 4 are safe: at $q = 0.10$ nothing above 0.1 can pass, and I checked the count 5 with the 52 at 0.1001, 0.5 and 1.
   Fix: both strings = "At $q = 0.15$ the bar for rank 6 is 0.015, and 0.0125 is under it, so the list grows."

5. `unclear` | `courses/testing/problems-3.json` `p-gene-screen` `parts[4]` | keyed option `right`: "BH keeps the share of false links at most 10%".
   BH bounds the expected share, not the share: a list of 5 with one false link has a share of 20%. The course says so itself (l10 screen 5: "the share of rejections that are false, on average"; `homework-3` `h-fdr-count`: "On average, at most how many"), and this part's own `explain` has "on average at most 10% of its list". The keyed option drops the two words that matter. The first read's finding 7 asked for "at most 10%"; it got that, without the average.
   Fix: `text` = "Bonferroni keeps the chance of any false link at most 10%; BH keeps the average share of false links at most 10%". Rerun the validator for `[key-length]`.

6. `minor` | `courses/testing/problems-3.json` `p-gene-screen` `parts[2]` | freshness: the BH step is the sibling item's, with the same answer.
   The re-authored part 3: ranks 1 to 3 pass, rank 4 fails, rank 5 passes, BH rejects 5, slip `first-fail` 3. `p-fund-managers` part 3 in the same set: "Ranks 1 to 3 pass, and rank 4 fails ... Rank 5 passes ... so BH rejects 5", slip `first-fail` 3. `homework-3` `h-bh-ten` is the same step again (rank 3 fails, ranks 4 and 5 pass, "Five"). A learner who has done either meets the same pattern and the same number. Part 4 (the smallest $q$) is new work, and the story and numbers are new.
   Fix, if the set should not ask one step twice: gene p-values 0.0004, 0.0021, 0.0055, 0.0058, 0.0090, 0.0096, 0.0190, 0.034, the other 52 above 0.2. Then Bonferroni still rejects 1; ranks 3 and 5 fail inside the list and rank 6 passes (0.0096 against 0.01), so BH rejects 6 with `first-fail` 2; part 4 becomes $\tfrac{60 \times 0.0096}{6} = 0.096$ (slips 0.576, 0.108 for rank 5 alone, 0.01 for the bar; BH rejects 4 just below 0.096); and `q-same` must use $q = 0.20$, where rank 7 passes (0.0190 against 0.0233) and BH rejects 7, since at 0.15 the list would not change. All in `proposed.py`. Or accept it as it stands.

7. `minor` | `courses/testing/problems-3.json` `p-biomarker-field` `parts[2].widget.wrong` | the slip from part 2's nearest wrong bar has no line.
   Part 2 offers the bars 2.5, 2.8 and 3.5 as wrong choices. Part 3 has `old-bar` 18 (2.5) and `next-bar` 12 (3.5) but nothing for 2.8: 16.8, or 17 as the whole number asked for, gets the generic line (`grade.mjs`). `chained.md` asks for the answer that follows from the slip in the part before.
   Fix: add `{"id": "lower-bar", "value": 17, "tol": {"abs": 0.5}}` with the line "That uses 0.84, the pass chance at 2.8. The bar chosen in part 2 is 3.1, with chance 0.75." The band takes 16.8 and 17 and is clear of 15, 18 and 20.

8. `minor` | `courses/testing/problems-3.json` `p-checkout-designs` `parts[3].feedback.byKey.bound` | a carried slip lands on a line that describes another.
   Part 3 has a `sidak` entry, 0.002846. A learner who carries it into part 4 and works correctly gets $1 - (1 - 0.002846)^{18} = 0.0500$, which lands on `bound`: "0.05 is the union bound, which Bonferroni guarantees." They did not use the bound.
   Fix: `bound` = "0.05 is the union bound, which Bonferroni guarantees, and what the Šidák bar gives. With the bar 0.002778 the exact chance is a little lower."

9. `minor` | `courses/testing/problems-3.json` | coverage and chain after the re-authoring.
   - l12 now rests on one step. The old `p-checkout-designs` carried l12's main idea (part 3, the honest next step: a hold-out) and the report row said "l9, l10, l12"; the new item is l9 and l10 only, and the row says so. What is left of l12 in the set is the biomarker's choice of a bar above 3 (l12's second idea). No problem now asks about a choice made on the same data, a hold-out or the count of things tried. The rule "every lesson of the level appears in at least one problem" is met only in that thin sense. Accept, or give `p-checkout-designs` part 5 a hold-out distractor pair again.
   - In `p-checkout-designs` part 3 (the Bonferroni bar) uses nothing from parts 1 and 2; the chain restarts there. Its four numeric parts are each one step of a lesson with 18 for 20 (l9 screen 0, l10 screens 0 and 1), which fits its new label of difficulty 3.
   - `p-gene-screen` parts 2 and 3 ask for a count with no form sentence. Add "Give a whole number." to both, as the estimation pass did for the same class (its finding 7).

### C. Regression

10. `minor` | `courses/regression/problems-1.json` `p-car-prices` `parts[3].widget.wrong` | the uncorrected line's own price has no line.
    The re-authored part 4 has `old-slope` 6,600 and `old-mean` 7,517, each with one old figure. A learner who misses the word "corrected" uses both and types 6,267 ($13{,}667 - 1{,}480 \times 5$, also the first fit's value at 9 years): generic line (`grade.mjs`).
    Fix: add `{"id": "both-old", "value": 6267, "tol": {"abs": 1}}` with the line "That is the first line's price, from the old slope and the old mean. Use the corrected slope, $-£1{,}230$, and the corrected mean, £14,000."

No finding on estimation.

## The re-authored items and parts

Each was recomputed whole and swept for stale numbers; none holds a number of its old version.

- `p-ping-latency` part 4: 28 (root 27.5; 2.02 at 27, 1.98 at 28). Slips 22, 55, 27 and 5.24 land; 27.5 gets the generic line, which says to round up. Fresh: no lesson or set of `estimation` asks for a sample size from a target standard error on a mean (l10 screen 7 halves an interval's width). Chain holds.
- `p-reference-mass` part 5: 0.513, by the formula and from the raw readings; 0.51 and 0.513 pass, 0.5 and 0.52 are refused. The idea (a mean measured in standard errors) is l2's, in a new setting. Part 1 now tests l1's sampling error, so `problems-1` covers l1 to l4.
- `p-car-prices` part 4: 7,850, by the mean point and by a fit of the corrected prices; the £350 in the explanation is right. Finding 10.
- `p-power-price` part 4: 0.04. The claim behind it holds exactly: with the same spreads, $n$ and noise, the gas slope's standard error at $r = 0.6$ is 1.25 times its value at $r = 0$ (inverse of the centred $\mathbf{X}^T\mathbf{X}$). It is l10's root-of-VIF factor run backwards; no item of the course or of exam `topic-1.6` asks it that way.
- `p-gene-screen`: 0.001667, 1, 5, 0.0948 (5 just above, 3 just below), all right. Findings 4, 5, 6 and 9.
- `p-checkout-designs`: 0.9, £3,600, 0.002778, 0.0488 (from the exact bar and the 6-place bar), £200, 0.6028, all right. Findings 3, 8 and 9.
- `p-biomarker-field`: the table is right at a real centre of 3.78 (0.0124 and 0.90, 0.0051 and 0.84, 0.0019 and 0.75, 0.00047 and 0.61); 0.002632, 3.1, 15, 0.0459, 0.51 all right. The tails are no longer l12's. Finding 7.
- `p-charging-robot`: $(2, 3)$, 42, $57.53°$, 2.177 m, all right. The band 0.015 on 2.18 takes 2.17, 2.177, 2.18 and 2.19 and none of seven wrong methods tried (nearest: 1.14 and 3.59). No file of the course or of exams `topic-1.4` and `stage-1` holds the pair $(4, 1)$, $(1, 3)$ or the point $(11, 11)$. Covers l1, l2, l3.
- `p-factor-risk`: $(1.105, 0.2)$, 0.605, $(0.5, 0.04875)$, 0.0037579, 80.3% (80.31 from the rounded figures, 80.33 exact, both inside the band), all right; $\mathbf{F}$ is positive definite; the cross term is 3.9% of the total. The hedge with a future is in no lesson, set or exam of the course. Finding 1.
- `p-colour-sensor`: $\mathbf{C}$, 0.8, $\mathbf{C}^{-1}$, $(120, 80)$ and the stage-by-stage check, all right; the two orders of the inverses do differ. Part 5 is l10 screen 5's idea (the last move is undone first) in a new setting. With its code line gone, l12 is covered by `p-paint-tints` part 2 only. Finding 2.

Every set still has a 5, and typed parts are 14 of 18 or more in each.

## Widened bands

- `p-currency-vol` part 3: each of the four slip bands takes the slip from the exact sd, from 1.0874 and from the 2-place value part 2 accepts (8.36 from 1.16 is on the edge of `carried` and lands); all are clear of the key and of each other. The key band takes 7.83 to 7.86.
- `p-three-month-fund` part 4: `inverted` takes 1.224 and 1.225, `squared` takes 0.667 and 0.668; 0.816 and 0.817 pass; 0.815, 0.818 and 0.82 are refused.
- `p-ticket-bot` part 4 `no-root`: takes 27.6 and 27.62. `p-ping-latency`, `p-reference-mass`, `p-tank-sensor` part 1: each whole-number band takes the exact slip and its rounding (387.5 and 388, 2.5 and 3, 8.4 and 8, 52.5 and 53).
- The three doubled tails (band 0.00015): each takes twice the 4-place tail and the calculator's value (0.0801 and 0.0802, 0.0718 and 0.0719, 0.0069 and 0.0070). Half the tail, one less two tails, the lower tail and the density at $z$ land in no band of the part.
- `p-running-shoes` parts 2 and 3 (0.005): the 2-place and 3-place slips land on their own lines; $-4.01$ and $-3.99$ are refused; no two bands meet.
- `p-stopping-distances` part 1: 0.66 and 0.658 land on `reverse`, 0.65 and 0.648 on `other-way`; the bands do not meet.
- The `decimal` bands of the vectors pass are the one place where a widened band misleads: finding 1.

## Original findings: closed or not

Closed as the passes say, each checked in the file and by script: 1.6-a findings 1 to 8 and 10 to 20; 1.6-b findings 1 to 11; 1.4-a findings 2, 3, 4, 5, 7, 8, 9 and 10. The claims of 1.6-a findings 14 and 15 hold in my simulation: with rolling-average signals the naive $t$ has sd 1.842 (formula 1.844); with independent daily signals 1.014; HAC with 4 and 8 lags still rejects a true zero in 9.2% and 7.4% of runs ("about one time in ten"). 1.4-a finding 6 is closed for the spellings it lists only (finding 2 here). 1.4-a finding 5 is closed and opens finding 1 here.

Deferred or decided without a change, as the passes record:
- 1.6-a finding 9: `p-route-delays` parts 1 to 3, `p-ticket-bot`, `p-currency-vol` part 4 and `p-ride-waits` parts 1 and 2 keep their overlap with a lesson or exam item, because the last part of each is new. Finding 20: `p-overlap-signal` parts 2 to 4, `p-bond-fund-weeks` parts 3 and 4, `p-sunny-cones` part 4 and `p-raw-intercept` part 4 accepted.
- 1.6-b finding 11: `p-running-shoes` part 5 accepted. `p-wine-taster` part 2: 0.019 still lands on `carried`, by design, with a line that now names both causes.
- 1.4-a finding 1 (nine matrix parts, now ten with the new sensor parts 1 and 3): waits for the engine. `p-paint-tints` part 2 accepted.
- Engine, in the inbox: a unit typed in full after a number stops the field ("1.52 m per mph", "1.96 percentage points": both still not read, `grade.mjs`); a plus sign before a positive number; `\ell(\lambda) =` before an expression; a number in front of a typed `pmatrix`.

## Engine

Not content findings; for the engine pass that is fixing the matrix fault.

- A number times a bracket matrix is matched as text against `accept`, never computed (finding 2). Wanted: the product computed entry by entry, as it already is for a vector.
- A wrong multiple of a vector, such as `5(3,4)` or `\frac{1}{4}(3,4)` in `p-drone-crosswind` part 1, returns the key `length` with the line "That is a single value. The answer has 2 components." It is two values with a number in front. This looks like the same list reading as the known fault; check it when that fix lands.

## Verified clean

- Estimation: `p-robot-deliveries` part 3 (0.9 by a grid search; $L$ falls all the way; 0.9, 0.90, 9/10 and 90% pass, 0.95, 0.75 and 1 land on their lines); `p-currency-vol` parts 1 to 5 from the eight returns (0.25, 1.0874, 7.84, 1.96, 123; each key typed with and without %, and each slip with and without %, behaves as stored); `p-three-month-fund` (2.08, 1.70 by enumerating the 27 resamples, 0.8165); `p-tank-sensor` (51, 3.08, 55.29); `p-ticket-bot` part 4 (0.5255); `p-routing-test` part 3 ($-0.1035$; 0.10 lands on `no-sign`).
- A decimal typed in an estimation or regression `%` field (0.0025 for 0.25) gets the generic line. That is sound here: the data and every feedback line are in per cent, unlike the vectors parts, whose working is in decimals.
- Regression: `p-stopping-distances` ($S_{xx}$ 1,000, $S_{xy}$ 1,520, $S_{yy}$ 2,345.2; `other-way` is numpy's slope of speed on distance; the five residuals and $R^2$ 0.985; 85 m at 70 mph); `p-freight-summary` part 1 (10; SSR is the course's word for the explained sum, l3 screen 1; no ESS left); `p-solar-output` part 2; `p-raw-intercept` part 4 (205; 105 lands on `extra`); `p-bond-fund-weeks` (week 8's residual is $-0.30$, $d = 0.2222$, lag-1 correlation 0.728); `p-overlap-signal` part 4 (1.8981; 1.57 lands on `root-h`).
- Testing: `p-fertiliser-trials` (0.7274, 0.9379, and both `centre-only` values); `p-phone-battery` ("18 h", "18h", "18 hours", "18 hrs" and "19.34 h" pass); `p-wine-taster` (79 of 4,096; 0.0730); `p-fund-managers` part 3 (5; the slips 2, 2 and 6); `p-running-shoes` part 5 (a paired $t$ test has power 0.783 at 25 and first reaches 0.8 at 27, so "a couple more" is right).
- Vectors: `p-site-plan` part 4 (126.87°; 53.1 lands on `clockwise`); `p-engraver-dial` part 1 (every mix of the two spellings of each entry passes, the keyboard's `\left(` form too) and part 3 ($-2$ and $-2.44$ land on `added`); `p-drone-crosswind` part 1 (all fifteen right forms tried pass); `p-goat-feed` part 3; `p-stress-hedge` part 1 at 2 places ($-2.2$, $-2.20$ and both with % pass).

## Counts

10 findings: 1 `wrong` (1), 3 `unclear` (3, 4, 5), 6 `minor` (2, 6, 7, 8, 9, 10). No changed key, band or `wrong` value is wrong, and no re-authored item holds a stale number. Two engine notes.
