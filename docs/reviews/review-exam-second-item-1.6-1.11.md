# Exams topic-1.6 to topic-1.11, second auto item: second-reader findings (session AG)

Scope: the nine new items and eight removals named in `docs/reports/exam-second-item-1.6-1.11.md` (commits dfa666b0 to 495bcc9c), in `app/content/exams/topic-1.6.json`, `topic-1.7.json`, `topic-1.8.json`, `topic-1.9.json`, `topic-1.10.json` and `topic-1.11.json`. No browser, no content edits.

Method: author's script run (172 of 172, exit 0). Own recompute in `docs/reports/exam-second-item-1.6-1.11-numbers-read.py` (169 checks, exit 0, 4 `FINDING` lines, all listed below). Other methods than the author's: Fractions and the weighted-average form for the Beta posteriors; a two-state linear solve and the risk-neutral price for the copy; bisection for the yield and both break-evens; a summed dividend stream; a literal run of the backtracking search beside a $3^6$ enumeration; each of the five C++ tests of `e-swapped-d` run in Python against a correct and a swapped pricer; a moment system for the quadrature weights; `cmath` and the polar route for the square root. Pairs and removals recounted from the exam files, every `course.json` of each topic and the files at 3abacdfe. Reuse read with a text search over the eight courses, the six exams, `stage-1` and the mock exams, plus `fresh-check.mjs --file` at the gate and at triage settings with `--cross-numbers 3`.

Gates: validator 0 errors, no warning on a new item. Voice scan at 35: 0 and 0. `grade-all.mjs --file` on the six exams: 26, 33, 18, 22, 38 and 44 widgets, 0 failures. `fresh-check.mjs --file`: no hit on a new item.

Code items: none of the nine is a code item, and no existing item changed (each file differs from 3abacdfe only by the listed additions and removals, order kept). `e-swapped-d` is a `multi` whose options hold C++ tests; they use `CHECK` and `CHECK_CLOSE`, the kit of `cpp-pricing/l12-testing-a-pricer`. `grade-all.mjs` counts no code widget, so the existing C++ and Python code items were not rerun here; they are unchanged since their last green playthrough.

## Verdict

- Numbers: every key, `wrong` value, option value and printed number of the nine items recomputes. Bands take the printed and the exact value and refuse every `wrong` value. No key or slip sits on a rounding tie. Percentages carry unit "%". One printed route does not reproduce from its own digits (finding 5). No wrong key.
- Pairs: ten pairs before the pass, the same list as the report (1, 5, 1, 1, 1, 1). Each of the ten skills now has exactly two auto items. No skill of any of the six exams is below two auto items. Pairs left: none. Counts 30, 30, 29, 30, 30, 30; minutes unchanged, and 60 × 29 / 28 = 62.1 rounds to 60 for topic-1.8.
- Two-skill item `e-ratio-spread`, strict test: **pass** (see the table below).
- Each item tests its skill: 8 pass, **1 weak on fairness** (`e-swapped-d`: the bounds option needs two normal values the item does not print, finding 4).
- Reuse: 7 clean, **2 reuse** (`s-three-traders` on story and sentence, finding 2; `e-just-paid` on numbers and sentence, finding 3).
- Removals: every count holds (each skill keeps at least two auto items). **One skill is left with only its hardest items**: `rg-inference` in topic-1.6 at 4, 4, 5 (finding 1). Three smaller coverage notes (findings 6, 8, 9).

Format: `N. file | JSON path | severity | problem | evidence | exact fix`. Severity: warning = reuse, a missing source, or a removal that breaks the brief's rule; note = small. No error (no wrong number, no wrong grading).

## Findings

1. topic-1.6.json | removed `s-alpha-beta-table` (`rg-inference`, difficulty 3) | warning (continuity) | The removal leaves `rg-inference` with only its hardest items. | `rg-inference` is essential to `regression` L2 and L3. Before: 3, 4, 4, 5. After: `s-overlap-hac` (4), `s-alpha-years` (4), `s-factor-code` (5, code). The removed item was its only difficulty 3 and the only plain coefficient t-test. The floor moved from two of four to two of three, with one of the three a code item. The report calls it "beside two other alpha t items"; neither `s-overlap-hac` (HAC on overlapping windows) nor `s-alpha-years` (sample size) asks a t-statistic or an interval from an estimate and its standard error. | Put `s-alpha-beta-table` back as it stood at dfa666b0^, and take out `s-p-backtest` (`items[13]`, `ht-pvalue` alone, difficulty 3) in its place, so the exam stays at 30 items and 5, 15, 7, 3. `ht-pvalue` is the most duplicated skill: it keeps `s-sharpe-p` (3), `s-chi-order-mix` (3) and `s-sharpe-code` (4), plus the longform. `rg-inference` returns to 3, 4, 4, 5 (reader script, "fix 1"). `s-p-backtest` is the only item on what a p-value means, so the main session may prefer to remove `s-welch` (`ht-setup` then holds 2, 3) or to accept 4, 4, 5; say which in the fix pass.

2. topic-1.6.json | `items[8]` (`s-three-traders`), `prose` | warning (reuse) | Story and opening sentence shared with the exam's other `es-bayes` item and with a lesson screen. | New: "A desk gives every new trader a $\mathrm{Beta}(22, 18)$ prior for their hit rate: centred on 55%, worth 40 trades." Exam `items[15]` (`s-beta-posterior`): "A desk gives a new trader a $\mathrm{Beta}(12, 8)$ prior for their hit rate: centred on 60%, worth 20 trades." Lesson `courses/estimation/l12-updating-a-belief.json` `screens[10]`: "For a new trader the desk uses a $\mathrm{Beta}(26, 24)$ prior: centred on the desk average, worth 50 trades." `quiz[3]` of that lesson also has a hit-rate posterior $\mathrm{Beta}(22, 18)$. The task (rank three records after shrinkage) is new and good; both `es-bayes` items of the exam now sit on one story. | Keep the id and the task; replace the story and numbers:
   - `title`: "Three sellers, one prior"
   - `prose`: "A marketplace tracks the share of orders each seller sends on time. Every new seller starts from a $\\mathrm{Beta}(27, 3)$ prior: centred on 90%, worth 30 orders. Kiln has sent 20 of 20 on time, Loom 68 of 70 and Moss 252 of 270."
   - `question`: "The marketplace ranks the three by posterior mean. Who comes top?"
   - options, same order: `{"id": "loom", "text": "Loom", "correct": true}`; `{"id": "kiln", "text": "Kiln", "why": "You ranked by the raw rate, 100%. Twenty orders cannot outweigh a prior worth 30, so Kiln's posterior mean is only $47/50 = 0.94$."}`; `{"id": "moss", "text": "Moss", "why": "You trusted the longest record. Moss's 252 of 270 gives $279/300 = 0.93$, below Loom's 0.95."}`; `{"id": "tie", "text": "All three tie, since they share one prior", "why": "The prior is shared, but each record adds its own counts. The posterior means are 0.94, 0.95 and 0.93."}`
   - `feedback.correct`: "Loom's posterior is $\\mathrm{Beta}(95, 5)$, with mean 0.95, the highest of the three."
   - `feedback.generic`: "Add each seller's on-time orders to 27 and late orders to 3, then compare $a/(a + b)$."
   - `explain.text`: "The posteriors are $\\mathrm{Beta}(47, 3)$, $\\mathrm{Beta}(95, 5)$ and $\\mathrm{Beta}(279, 21)$, with means 0.94, 0.95 and 0.93. Kiln's 100% rests on 20 orders, so the prior worth 30 pulls it towards 90%. Loom has enough orders to keep most of its 97%."
   - Recomputed: 47/50, 95/100, 279/300; raw rates 100%, 97.1%, 93.3%; raw top Kiln, longest record Moss, no tie (reader script, "fix 2"). No "seller" or "on time" in `estimation` or in the topic, stage and mock exams on this skill. The fixer runs `fresh-check.mjs --file` on the new story.

3. topic-1.7.json | `items[17]` (`e-just-paid`), `prose` | warning (reuse) | Two of the three numbers and the sentence frame come from the lesson quiz on the same formula. | New: "A company has just paid a dividend of £1.50 a share. Dividends grow 4% a year for ever, and investors require 10% a year." `courses/markets/l7-shares.json` `quiz[2]` (`q-ddm`): "A share will pay a £1.50 dividend next year, growing 4% a year for ever. Investors require 9% a year." The just-paid trap is new (no "just paid" in `markets`), so the task is clean; the number set is not. | Change the numbers only:
   - `prose`: "A company has just paid a dividend of £3.20 a share. Dividends grow 5% a year for ever, and investors require 9% a year."
   - `widget.answer`: `84.0`; `widget.accept`: "£84.00: $3.36/(0.09 - 0.05)$"; `wrong` values: `last-div` 80.0, `no-growth` 37.33, `plus-g` 24.0 (tolerances unchanged).
   - `feedback.correct`: "Next year's dividend is $3.20 \\times 1.05 = 3.36$ pounds, and $3.36/0.04 = 84.00$."
   - `feedback.byKey.last-div`: "You used the £3.20 already paid. The formula needs next year's dividend, £3.36."
   - `feedback.byKey.no-growth`: "You divided by $r$ alone. Growing dividends are worth more: divide by $r - g = 0.04$."
   - `explain.text`: "A share is worth next year's dividend over $r - g$. The £3.20 has been paid, so the first dividend still to come is $3.20 \\times 1.05 = 3.36$ pounds. $3.36/(0.09 - 0.05) = 84.00$ pounds."
   - Recomputed: 3.36/0.04 = 84.00 (summed stream agrees), 3.20/0.04 = 80.00, 3.36/0.09 = 37.33, 3.36/0.14 = 24.00, no tie (reader script, "fix 3"). £3.20, 5% with 9%, £84 and £80 do not meet `markets` l7, `review-2` or `homework-2` (those use £2 at 3%, £2.50 at 2% and £1.80 at 8%).

4. topic-1.9.json | `items[25]` (`e-swapped-d`), `prose` | warning (misleading, source) | The `bounds` option cannot be judged from what the item prints. | To tick `bounds` the learner must know that $100N(0.15) - 95.12N(0.35)$ is negative. The item gives neither $d$ value, no normal value and no table, and the exam has no normal CDF to hand. The other four options need no arithmetic. The course itself prints these values when it asks for this price: `courses/cpp-pricing/l4-normal-cdf.json` `quiz[3]` gives "$d_1 = 0.35$, $d_2 = 0.15$, $\Phi(d_1) = 0.636831$, $\Phi(d_2) = 0.559618$ and $e^{-0.05} = 0.951229$". Author rule 4: a table value names its source. | Append to `prose`: " Here $d_1 = 0.35$ and $d_2 = 0.15$, with $N(0.35) = 0.636831$, $N(0.15) = 0.559618$ and $e^{-0.05} = 0.951229$." Then $55.9618 - 95.1229 \times 0.636831 = -4.62$ (reader script, "fix 4"). These are the course's reference constants, already shared by `l4` and `l12`, so they add no new reuse. The item then tests which tests bite, not recall of $N$.

5. topic-1.9.json | `items[25]` (`e-swapped-d`), `explain.text` | note (wrong digit route, continuity) | The printed route gives −4.61 from its own digits, and it uses a lesson's label. | "$100N(0.15) - 95.12N(0.35) = -4.62$": with 95.12 the value is −4.6136, which rounds to −4.61; the exact −4.6155 needs 95.123. "At the standard inputs" is the phrase of `l12` `screens[5]`; the exam never defines it. | In `explain.text` replace "At the standard inputs $d_1 = 0.35$" with "At these inputs $d_1 = 0.35$", and "95.12N(0.35)" with "95.123N(0.35)" ($100 \times 0.559618 - 95.123 \times 0.636831 = -4.6155$; reader script, "fix 5").

6. topic-1.9.json | pair `cx-testing` | note (continuity) | The pair is filled, but both items are hard. | `cx-testing` is essential to `cpp-pricing` L1, L2 and L3. Its two auto items are `e-swapped-d` (4, a five-option `multi`, all or nothing) and `e-code-digital-tests` (5, code). The floor asks for one of the two. The new item took the removed `e-virtual-dtor`'s difficulty, so the mix is unchanged. Not a removal fault: `cp-classes` keeps 2, 3, 3, 4, 4. | Main session's call. With finding 4 applied the item is nearer a 3 in work. If an easier `cx-testing` item is wanted, it needs a swap at difficulty 2 or 3 in a later pass; no change needed now.

7. topic-1.7.json | `items[14]` (`e-ratio-spread`), `prose` | note (continuity) | Leg sentences and the canvas line follow `items[10]` (`e-bear-spread`). | New: "On one share you buy a call struck at £80.00 for £5.40. You also sell two calls struck at £90.00 for £1.90 each. All three expire on the same day. The bold line is the position's profit at expiry." `e-bear-spread`: "On one share you buy a put struck at £60.00 for £5.20. You also sell a put struck at £52.00 for £1.70. Both expire on the same day. The bold line is the spread's profit at expiry." The position (a ratio spread, loss without limit, upper break-even) and the asks differ, and the course has no ratio spread, so the ruling is clean. | Optional: `prose` to "You hold one call struck at £80.00, bought for £5.40, and you have written two calls struck at £90.00 for £1.90 each. All three are on one share and expire together. The bold line is the position's profit at expiry." No number changes.

8. topic-1.10.json | removed `e-cube-delta` (`an-continuity`, difficulty 3) | note (continuity) | The count rule holds, but no auto item now asks for an $\varepsilon$-$\delta$ argument. | `an-continuity` (essential to `analysis` L4 and L5) keeps `e-halvings-width` (2, a bisection count), `e-uniform-peak` (4) and `e-contraction-proof` (5, also `an-sequences`). Not "only hardest": a 2 remains. The removed item was the only $\delta$ computation. | Main session's call; no change needed if the coverage is accepted.

9. topic-1.11.json and topic-1.7.json | removed `e-integrating-factor`, `e-one-step-q`, `e-parity-put` | note (continuity) | Three removals leave a skill thinner at the easy end; all counts hold. | `de-first` (essential to `odes` L1, L2 and L4) is now at the minimum of two: `e-rate-pull` (2) and `e-separable-slow` (3). `tp-riskneutral` lost its only 2 and keeps 3, 3, 4, 4, 5. `op-parity` keeps 3, 4, 4, 5, and its only 3 is the derivation order `e-parity-order`. None is left with only its hardest items. | None. Recorded so that a later swap does not take a second item from `de-first`.

10. topic-1.7.json | `items[13]` (`e-annualised`), outside this pass | note (reuse, old item) | Seen while reading the `fi-equity` pair. | Exam: "four yearly total returns: +25%, −20%, +10% and +6%". `courses/markets/homework-2.json` `items[6]` (`h-record`): "A fund returned +25%, −20% and +10% in three years." `fresh-check` lists it as an advisory (1.25, 0.8, 1.1). | Not part of this fix pass; raise with the next pass on topic-1.7.

## Skill test for the two-skill item

| item | skills | without `op-payoff` | without `op-strategies` | ruling |
|---|---|---|---|---|
| `e-ratio-spread` | op-strategies, op-payoff | No part can start: both need each call's payoff at a price above both strikes ($15$ and $5$ at £95.00) and the profit as payoff less premium. | A learner who can only value one option gets £9.60 for the long call or −£3.10 for one short call. The key £3.40 needs two short calls netted against one long and a net premium of £1.60; the upper break-even £98.40 needs the combined slope of −1 above £90.00. One short call instead of two gives the keyed slip £8.40. | pass |

The canvas does not give the answers away: `state.breakeven` is false, no `spot` is set, so no value is printed on the line, and the axis cannot be read to a penny (bands ±0.005). The course tags leg-sum profits the same way (`options/homework-1` `h-four-at-85`, `h-profit-code`: both skills). `e-bear-spread` carries `op-strategies` alone for similar work; that is the older, narrower tag, not a fault of the new item.

## Each item against its skill

| item | skill | tests it | can it be passed without it |
|---|---|---|---|
| `s-three-traders` | es-bayes | yes: three conjugate updates and a comparison | no: the raw rate and the longest record are both keyed wrong options |
| `e-capped-copy` | tp-replicate | yes: a copy of a payoff that is not an option | no: three options share 0.6 shares, so the cash leg and its discounting decide |
| `e-zero-yield` | fi-bonds | yes: yield from price, then pull to par | no |
| `e-just-paid` | fi-equity | yes: dividend growth model with the timing trap | no |
| `e-venue-split` | gd-backtrack | yes: part 1 is the search order at a dead end; part 2 counts what the full search records | part 1 no (all four wrong options are valid or tempting ends of a wrong search); part 2 is a count that needs the constraint graph, not the search order |
| `e-swapped-d` | cx-testing | yes: which test families bite on a given bug | no, but see finding 4 |
| `e-integral-weights` | lx-dual | yes: coordinates of a functional in a dual basis, $c_k = I(\ell_k)$ | exactness on $1$, $x$, $x^2$ also gives the weights; that is the same idea in the monomial basis |
| `e-square-root-parts` | cz-arith | yes: expand $(a + bi)^2$, use $i^2 = -1$, match parts | the polar route also works; it is `cz-polar`, harder here |

## Reuse per item

| item | closest exam item | closest lesson screen | closest review / homework | closest problem-set item | ruling |
|---|---|---|---|---|---|
| `s-three-traders` | topic-1.6 `s-beta-posterior` (same desk, same sentence) | `estimation/l12` `screens[10]` (desk prior for a new trader); `quiz[3]` ($\mathrm{Beta}(22, 18)$) | `review-3` `r-shrink` ($\mathrm{Beta}(15, 15)$, 42 of 70); `homework-3` `h-pseudo` | `problems-3` `p-ticket-bot` (bots, $\mathrm{Beta}(8, 12)$) | **reuse** (finding 2) |
| `e-ratio-spread` | topic-1.7 `e-bear-spread` (frame only) | `options/l7` `screens[5]` (a butterfly built with one sold call) and `screens[6]` (profit line, markers hidden) | `review-2` `r-fly-profit` (two sold calls, profit at one price); `homework-2` `h-fly-arb` | none (no problem sets in `options`) | clean (finding 7) |
| `e-capped-copy` | topic-1.7 `e-copy-short-calls` (the exam's one-step frame, also in `e-call-in-k`) | `trees/l2` `screens[5]` (copying a put) and `quiz[2]` (which holding copies the put) | `review-1` `r-copy-80`; `homework-1` `h-replicate-42` (also a £40 share, other tree) | none | clean: a capped note is a new payoff, and the copy holds shares with cash lent, a mix the lessons do not show |
| `e-zero-yield` | topic-1.7 `e-bond-price` (price from yield) | `markets/l5` `screens[5]` (zero's price from its yield); `l6` `screens[2]` (yield by search) | `review-2` `r-ytm`; `homework-2` `h-ytm-97`, `h-bond-hold` (a year on, new yield) | none | clean |
| `e-just-paid` | topic-1.7 `e-annualised` (other task) | `markets/l7` `quiz[2]` `q-ddm` (£1.50, 4%) | `review-2` `r-implied`; `homework-2` `h-implied-g` | none | **reuse** on numbers (finding 3) |
| `e-venue-split` | topic-1.8 `e-prune-tree` (take or skip with a budget) | `graphs-dp/l11` `screens[2]` (four queens: step back at a dead end, count all answers) | `review-3` `r-queen-row2`; `homework-3` `h-legs` (count orders that survive a prune); `homework-1` `h-split-desks` (two groups, by BFS) | none | clean: colouring by backtracking is not in the course |
| `e-swapped-d` | topic-1.9 `e-code-digital-tests` (write tests for three bugs); `e-parity-put` (a wrong $d_1$) | `cpp-pricing/l12` `screens[2]` (parity and limit tests against two planted bugs) and `screens[5]` (one test for a changed `bs_put`) | `review-3` `r-indep`; `homework-3` `h-test-file` | none | clean: the swap is a new bug and the ask (which families bite) is new. The reference case £10.4506 is the course's own constant |
| `e-integral-weights` | topic-1.10 `e-dual-basis-pair` ($\mathbb{R}^2$) | `linear-maps/l10` `screens[4]` (evaluations at 0, 1, 2 and $\ell_1$); `screens[11]` (a functional in a new dual basis, $\mathbb{R}^2$) | `review-3` `r-dual-map`; `homework-3` `h-lagrange-2` (nodes −1, 0, 1) | `problems-3` `p-currency-duals` | clean: new nodes, and an integral as the functional is new |
| `e-square-root-parts` | topic-1.11 `e-divide-conjugate` | `complex/l5` `screens[3]` and `quiz[0]` (roots of $-3 + 4i$, by dragging) | `review-1` `r-sqrt-trap`; `homework-1` `h-quotient` | `problems-1` `p-turning-frames` | clean |

Triage `fresh-check` lines on new items were read: shared-number advisories only (for example `e-ratio-spread` with 1.9, 3.4, 1.6 in unrelated courses), none a shared task.

## Bands, ties, units, sources

| item | check | result |
|---|---|---|
| `e-zero-yield` part 1 | key 0.045593 ± 0.00006, unit "%"; 4.56 typed is in; slips 5.36, 3.75, 4.36 are out and disjoint | ok |
| `e-zero-yield` part 2 | 73.1915; both printed routes ($100/1.0456^7 = 73.188$, $70 \times 1.0456 = 73.192$) land in ±0.006; slips 70.00, 73.75 out | ok |
| `e-ratio-spread` | 3.40 and 98.40 exact; slips 8.40, 5.00, −4.20 and 100.00, 81.60, 101.60 out | ok |
| `e-just-paid` | 26.00 exact; slips 25.00, 15.60, 11.14 (11.1429) out | ok |
| `e-venue-split` part 2 | whole number 24, tolerance 0; slips 729, 4 | ok |
| `e-integral-weights` | 0, 2.25, 0.75 exact, ±0.001; "as decimals" stated | ok |
| `e-capped-copy` | option a is the only holding within a penny in both states (13.6585 lent) | ok |
| `e-swapped-d` | correct 10.4506, swapped −4.6155; all five tests pass on the correct pricer; `known`, `parity`, `bounds` fail on the swap, `limit` and `finite` pass | ok; source missing (finding 4) |

## Handover

- Fix pass (Sonnet): findings 2, 3, 4 and 5 are exact edits. Finding 1 needs the main session's choice of item to remove. Findings 6 to 10 need no edit.
- After the fix pass the author's script needs new values for `s-three-traders` and `e-just-paid`; the reader script's blocks for those two items must be updated with them (its "fix 2" and "fix 3" blocks already hold the new numbers).

## Fix pass

Files edited: `app/content/exams/topic-1.6.json`, `topic-1.7.json`, `topic-1.9.json` only. Scripts: author's `exam-second-item-1.6-1.11-numbers.py` 174 of 174, exit 0; reader's `-numbers-read.py` 164 ok, 0 FINDING, exit 0 (blocks of the rewritten items retargeted to the new numbers; the cx-testing difficulty check is now a printed note; the fix 1 block is switched off because the main session overruled it).

1. Fixed as ruled by the main session (DECISIONS, session AG), not as the reader wrote it: `s-alpha-beta-table` restored to `topic-1.6` exactly as at `dfa666b0^`, at its old position (before `s-three-traders`); nothing else removed. The exam holds 31 items (validator range 20 to 36), `minutes` stays 70. `rg-inference` is back to 3, 4, 4, 5. `s-p-backtest` stays.
2. Fixed: `s-three-traders` re-storied exactly as written (sellers, Beta(27, 3), Kiln 20 of 20, Loom 68 of 70, Moss 252 of 270). Recomputed 47/50, 95/100, 279/300 = 0.94, 0.95, 0.93; no "seller" story in `estimation` or the exams on this skill; `fresh-check --file` gives no hit.
3. Fixed: `e-just-paid` numbers changed exactly as written (£3.20, 5%, 9%; key 84.00; slips 80.00, 37.33, 24.00). Recomputed 3.36/0.04 = 84, 3.20/0.04 = 80, 3.36/0.09 = 37.33, 3.36/0.14 = 24; no hit in `markets` or the exams.
4. Fixed: `e-swapped-d` prose now prints d1, d2, N(0.35), N(0.15) and e^{-0.05}; 100 x 0.559618 - 95.123 x 0.636831 = -4.6155.
5. Fixed: `e-swapped-d` explanation reads "At these inputs" and 95.123N(0.35); gives -4.62.
6. No edit (ruled): `cx-testing` coverage note.
7. No edit (optional wording; verdict clean).
8. No edit (ruled): `an-continuity` coverage note.
9. No edit (ruled): `de-first`, `tp-riskneutral`, `op-parity` coverage note.
10. Deferred: `e-annualised` reuse is outside this pass; raise with the next pass on topic-1.7.

Disputed: none. Deferred replacements: none (no replacement retold course material).

Gates: validator 0 errors; voice scan 0 and 0; `grade-all.mjs --file` 0 failures on topic-1.6 (27 widgets), topic-1.7 (33) and topic-1.9 (22); `playthrough.mjs --exam` with and without `--mobile` all passed on the three. Graded answers changed: `s-three-traders` key (Bea to Loom, new options), `e-just-paid` key (26.00 to 84.00); `e-swapped-d` key unchanged; `s-alpha-beta-table` returns as it was.
