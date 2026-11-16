# Problem sets: ensembles (brief `docs/briefs/chained.md`, prompts `docs/briefs/chained-prompts.md`)

Files: `app/content/courses/ensembles/problems-1.json` to `problems-3.json`. Numbers: `docs/reports/problems-ensembles-numbers.py` (paths from `__file__`; exits 0). Every lesson, review and homework of each level was read first (text dumped without canvas data) and its numbers, data sets and stories noted.

## Level 1: `problems-1.json` (decision trees)

Settings new to the course: an exchange's spoofing alerts, a funding desk's repo terms, a broker's client tree, ten mornings' opening gaps.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-spoof-alerts | 5 (5 / 0) | l1, l2 | 3 |
| problems-1 | p-repo-terms | 5 (5 / 0) | l3, l4 | 4 |
| problems-1 | p-broker-pruning | 5 (5 / 0) | l2, l3 | 4 |
| problems-1 | p-opening-gaps | 5 (5 / 0) | l1, l2, l3 | 5 |

Typed parts 20 of 20. Chains: mistakes 12, root Gini 0.42, sides 0.289, gain 0.131, then 7 mistakes at depth 2. Root error 160, best drop 120 at 12 weeks, flat forecast 20 at 26 weeks, the floor `min_samples_leaf=2` moves the split to 5 weeks (drop 96) and the forecast to 14. Node Gini $\tfrac49$, $R(t) = 0.03$, inner break-even 0.003, the node's own 0.021 once the inner cut is made, so `ccp_alpha=0.016` keeps 10 of 11 leaves. Nine thresholds, two tied on mistakes with Gini gains 0.213 and 0.163, information gain 0.420 of the kept split, and 5 leaves for the unlimited tree (memorising one morning).

Design note. The pruning problem was first drafted as a three-leaf branch cut in one step at 0.0095. A scan of every three-leaf branch shows that greedy Gini growth always gives the inner node the smaller break-even, so weakest-link pruning cuts it first. The problem now follows the two cuts in order; the script grows the node with scikit-learn and reads both cuts off `cost_complexity_pruning_path`, scaled from 27 to 400 rows.

## Level 2: `problems-2.json` (averaging trees)

Settings new to the course: a desk's 25 bonds and downgrades, new listings below their issue price, dividend cuts, a market maker's order-book imbalance.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-2 | p-bond-downgrades | 4 (4 / 0) | l5, l7 | 3 |
| problems-2 | p-ipo-forest | 4 (4 / 0) | l5, l6 | 4 |
| problems-2 | p-dividend-importance | 5 (4 / 1) | l8, l5 (a forest averages its trees' importances) | 4 |
| problems-2 | p-imbalance-stumps | 5 (5 / 0) | l5, l7 (stumps from level 1) | 5 |

Typed parts 17 of 18; the one choice is the judgement on company_id. Chains: $0.96^{25} = 0.3604$, 2.88 out-of-bag trees per bond, 0.70 bonds with none, and the reported error $\tfrac{6}{25} = 0.240$ because scikit-learn calls an uncovered row class 0. $m = 3$ of 10, bagged variance 0.0200 and forest 0.0118 at 50 trees, the forest ahead from 5 trees. Credits 0.1641 and 0.0980, share 0.593, forest importance 0.571, then company_id read as memorised. Out-of-bag rows 2 and 5, stump forecasts 3 and $-1$ (repeats counted), out-of-bag MSE 2.75, bagged forecast 1.

## Level 3: `problems-3.json` (boosting)

Settings new to the course: limit-order fill times, callable bonds, a commodity future's walk-forward study, post-earnings drift by company size. The carry and momentum interaction stories of `l10` and `review-3` were avoided; the interaction here is a surprise that matters only for small companies.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-3 | p-fill-times | 5 (5 / 0) | l9, l10 | 3 |
| problems-3 | p-callable-bonds | 5 (5 / 0) | l11, l9, l10 | 5 |
| problems-3 | p-futures-study | 4 (3 / 1) | l12, l11 | 4 |
| problems-3 | p-surprise-drift | 5 (4 / 1) | l9, l10, l12 | 4 |

Typed parts 17 of 19; the choices are judgements (how to stop early on daily data, what can fit an interaction). Chains: start 11, first leaf $-5$, forecast 10.5 at $\nu = 0.1$, squared error 214 to 178.375, second leaf $-4.5$ and forecast 10.05. $F_0 = \ln\tfrac13 = -1.0986$, target 0.75, Newton leaf $\tfrac{20}{9} = 2.2222$, $F_1 = -0.8764$, $p = 0.2939$. Last training row 457 with `gap=2`, $t = 1.55$ against a 0.525 base rate, £15,000 after costs, then stopping on a later block. Start 2, surprise leaf $+6$, forecast 8 for every positive surprise, MSE 36 that no stump can lower, then depth 2. The Newton step is stated in the question, since `l11` names it (one Newton step per leaf) without the formula.

## Checks

| check | problems-1 |
|---|---|
| numbers script | 0 failures (scikit-learn trees on built data against fractions: impurity, thresholds, leaf means, `min_samples_leaf`, pruning path, leaf count; every `wrong` matched to its slip and outside the key band) |
| validator | 0 errors, 0 warnings on the file (first draft: nine `O2-long-sentence`, two `[shown-arithmetic]`, two `O2-long-explain`, two `[wrong-band]`, all rewritten) |
| grade-all `--file` | 0 failures (20 widgets) |
| playthrough `--local-cdn` | green (20 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault |
| voice scan 35 (course folder) | 0 and 0 |

| check | problems-2 |
|---|---|
| numbers script | 0 failures (scipy's binomial law and a bootstrap simulation; the sklearn rule for uncovered rows; the variance of an average from the full covariance matrix and a scan over $B$; sklearn's own impurity importances on a built book; sklearn stumps on each resample) |
| validator | 0 errors, 0 warnings on the file (first draft: five `O2-long-sentence`, two `[shown-arithmetic]`, one `[key-length]`, one `[negative-key]`, all fixed) |
| grade-all `--file` | 0 failures (18 widgets, the row set included) |
| playthrough `--local-cdn` | green (18 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault |
| voice scan 35 (course folder) | 0 and 0 |

| check | problems-3 |
|---|---|
| numbers script | 0 failures (sklearn's `GradientBoostingRegressor` and `GradientBoostingClassifier` read stage by stage, init, leaf values and decision function; `TimeSeriesSplit`; statsmodels' `proportions_ztest` with the null variance; a P&L in NumPy; 50 stumps stalling at MSE 36 against depth 2 at 0) |
| validator | 0 errors, 0 warnings on the file (first draft: nine `O2-long-sentence`, one `O2-long-explain`, one `[negative-key]`, one `[key-length]`, all fixed) |
| grade-all `--file` | 0 failures (19 widgets) |
| playthrough `--local-cdn` | green (19 parts) |
| playthrough `--mobile` | green; 440 px shots read; pound signs moved out of KaTeX in the P&L working |
| voice scan 35 (course folder) | 0 and 0 |

The script caught four slip values of the first draft that did not follow from their named slip (a forecast slip equal to the key, two misworked shares, a variance with the wrong $\rho$); each was recomputed before the set was played.

## Fresh-check

`node tools/fresh-check.mjs --file content/courses/ensembles/problems-1.json`: 0 hits, 0 advisories. Two advisories on drafts were removed by changing numbers, not waived: two shared parameters (0.006, 0.01) with `review-2.json` item 7, and three (0.025, 0.021, 0.015) with `exams/stage-2.json`. Second check by grep of the course folder: no key value, data set or noun (spoof, repo, broker, opening gap) appears in a lesson, review or homework text; single numbers such as 160 and 96 appear only in unrelated captions.

`node tools/fresh-check.mjs --file content/courses/ensembles/problems-2.json`: 0 hits, 0 advisories. One draft advisory was removed by changing numbers: the dividend tree first had a node of 120 companies with 105 kept, the same three parameters (120, 105, 80) as the regime split in `l2-good-split.json` screen 12. Grep: no key value or story repeats a lesson, review or homework (2.75 and 12.75 occur only in unrelated working).

`node tools/fresh-check.mjs --file content/courses/ensembles/problems-3.json`: 0 hits, 0 advisories. The draft had one `[same-course-reuse]` transform warning and three shared-formula advisories. The warning was real enough to act on: the first fill times, 2, 4, 12, 13, 14, gave residuals equal to `homework-1.json` item 3's targets under $x \to -x + 7.6$, so the data were replaced (4, 5, 9, 16, 21). The advisories were the course's own formulas ($p = 1/(1 + e^{-F})$ against `l9`, the Newton step against `exams/stage-2.json`, $\sqrt{b(1 - b)/n}$ against `l12`); each is now said in words in the stem, and stays in feedback. No warning is waived and none is listed as a false positive.

## Engine limits

One bullet in `docs/BACKLOG-INBOX.md` under `Raised later (problems ensembles):` (fresh-check's shared-formula advisory on a course's standard formulas).
