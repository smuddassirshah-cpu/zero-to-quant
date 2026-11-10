# Claim ledger: mm-games L1 to L3 (concept audit)

Blind audit of `app/content/courses/mm-games/` levels 1 to 3 (l1 to l13, review-1 to review-3, homework-1 to homework-3). ROWCOUNT_LINE

One row per definition, result, method step, convention, always/never/every/only claim, code-behaviour claim and the reasoning of each explain, why, hint, feedback, rubric and model line. Lines on one screen that restate the same reasoning share a row, and the path column then names every key covered. Paths are JSON paths inside the file (`s[n]` is `screens[n]`, `q[n]` is `quiz[n]`, `i[n]` is `items[n]`). Verdicts: correct, wrong, imprecise, misleading, unverified. `sim:` names a check in `docs/reports/mm-games-L<n>-concepts.py`; `enum` means exact enumeration there.

Sources: Zhou, *A Practical Guide to Quantitative Finance Interviews* (ch. 2 brain teasers, ch. 4 probability); Joshi, Denson and Downes, *Quant Job Interview Questions and Answers* (ch. 3 probability); Crack, *Heard on the Street*; Jane Street, *Probability and Markets* (market-making games, confidence intervals, adverse selection); Harris, *Trading and Exchanges* (ch. 13 dealers, ch. 14 bid/ask spreads, ch. 19 liquidity); Glosten and Milgrom (1985), "Bid, ask and transaction prices in a specialist market with heterogeneously informed traders", JFE 14; Avellaneda and Stoikov (2008), "High-frequency trading in a limit order book", Quant. Finance 8 (reservation price); Casella and Berger, *Statistical Inference* (ch. 2 expectations, ch. 4 covariance, sec. 5.5 CLT, ch. 8 tests); Cochran, *Sampling Techniques* (ch. 2, finite-population correction); Hull, *Options, Futures and Other Derivatives* (ch. 3 minimum-variance hedge ratio); Clopper and Pearson (1934) exact binomial test as in R `binom.test`.

## Level 1

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l1-unknown-quantity | s[0] options, hints, feedback, explain | A 90% range claims that about 9 in 10 ranges made this way hold the truth; it is not certainty; the point estimate is the centre, the range the spread | correct | Frequency reading of a subjective interval; *Probability and Markets*, confidence intervals |
| l1-unknown-quantity | s[0].options[2].why | The count is most likely near the guess in the middle; the ends mark where surprise begins | correct | One-peaked belief; convention of the lesson |
| l1-unknown-quantity | s[1] table, hints, feedback, explain | Pages 1 to 300 use 9 + 180 + 603 = 792 digits; 100 to 300 is 201 pages; slips 600 and 900 | correct | enum (L1 script) |
| l1-unknown-quantity | s[2] prose, table, hints, feedback | A k by k square starts in (9−k)² places; 64, 49, ..., 1 add to 204; slips 9, 64, 65 | correct | enum; Zhou ch. 2 |
| l1-unknown-quantity | s[2].explain.text | "Most first guesses say 64 or 65" | imprecise | Empirical "most" with no source; the standard wrong answer is 64 (Zhou ch. 2). Finding 2 |
| l1-unknown-quantity | s[3] table rows | Ten truths: 792, 204, 31,536,000, 10,080, 8,784, 2,598,960, 40,320, 2,893, 435, 1,296 | correct | enum: C(52,5), 8!, C(30,2), C(9,2)² |
| l1-unknown-quantity | s[3] answer, wrong sets, hints, feedback, explain | Rows 2, 6, 10 miss, each above its high end; the other seven hold | correct | enum |
| l1-unknown-quantity | s[4].prose, widget, hints, feedback | Hit rate is the share of ranges that hold the truth; here 7/10 = 0.7; slips 0.3 and 7 | correct | Definition; enum |
| l1-unknown-quantity | s[4].explain.text | A calibrated forecaster scores 7 or fewer of 10 about 7% of the time | correct | Binomial(10, 0.9): 0.0702; sim |
| l1-unknown-quantity | s[4].explain.text | "These ranges were too narrow: the candidate was overconfident" (from 7 of 10) | imprecise | p = 0.070 is above 0.05; homework-1 i[1] returns `calibrated` for the same data and review-1 says ten is too few. Finding 1 |
| l1-unknown-quantity | s[5] options, hints, feedback, explain | A 10-hour range on a guess is overconfident and misses 8,784; 0 to 100,000 cannot miss and says nothing; C is centred on 365 × 24 with room; a leap year has 366 × 24 = 8,784 hours | correct | Arithmetic; *Probability and Markets* on useless wide intervals |
| l1-unknown-quantity | s[6] options, hints, feedback, explain | A number worked out exactly gets zero width; padding or a habit 10% width is wrong; "there is no usual width" | correct | Width follows uncertainty; convention of the lesson (the maker may say the value is known) |
| l1-unknown-quantity | s[7].prose, summary.formula | Calibrated at level p: ranges hold the truth a share p of the time; hit rate formula with closed ends | correct | Definition of calibration |
| l1-unknown-quantity | s[7] widget, feedback, explain | 20 calibrated 90% ranges: about 2 miss; zero misses in 20 has chance about 12%; never missing means too wide | correct | 0.9^20 = 0.1216 |
| l1-unknown-quantity | s[8] prose, answer, wrong, hints, feedback, explain | Digits for pages 1 to n, 100 ≤ n ≤ 999: 189 + 3(n − 99) = 3n − 108; slips 3n − 111 and 3n | correct | enum over n = 100..999 |
| l1-unknown-quantity | s[9] code, tests, hints, explain | `digits_to_number` by blocks; `calibration` counts lo ≤ t ≤ hi, ends included; 10,000 pages need 38,894 digits | correct | CPython: 12/12 cases pass, starter fails |
| l1-unknown-quantity | s[10] widget, hints, feedback | Sold at 850, settles at 792: seller's P&L is price minus value, +58; slips −58, 850 | correct | Cash 850 in, 792 out |
| l1-unknown-quantity | s[10].explain.text | "A price far from your fair value invites the interviewer to trade against you" | imprecise | False as stated: an offer far above fair deters trade; what invites trade is a price on the wrong side of the true value. Finding 3 |
| l1-unknown-quantity | s[11] options, hints, feedback, explain | Best opening says a number, a range and a reason aloud before exact working; silence, a useless range and false precision lose marks | correct | *Probability and Markets*; Crack; Zhou ch. 2 |
| l1-unknown-quantity | s[11].prose, explain | *Probability and Markets* is a free guide by a trading firm; Zhou and Crack collect such openers | correct | Jane Street guide; the two books exist as described |
| l1-unknown-quantity | summary.ideas, trap | Fair value is the centre, range the spread; calibrated 90% ranges hold about 9 in 10; a known number gets zero width | correct | As rows above |
| l1-unknown-quantity | q[0] | 500 pages: 1,392 digits; slips 1,389 and 1,500 | correct | enum |
| l1-unknown-quantity | q[1] | 12 of 20 at 90%: overconfident, widen; hit rate tells about width, not direction | correct | P(≤12 of 20) < 0.001; a hit rate carries no sign |
| l1-unknown-quantity | q[2] | 4 by 4 board: 30 squares; slips 16, 17 | correct | enum |
| l1-unknown-quantity | q[3] | 365 × 24 × 3,600 = 31,536,000; slips 31,622,400 and 525,600 | correct | Arithmetic |
| l2-dice-sum | s[0] widget, hints, feedback, explain | One die pays 21/6 = 3.5 on average; paying more loses on average; no roll pays 3.5 | correct | E[X] by enumeration; Zhou ch. 4 |
| l2-dice-sum | s[1] options, hints, explain | Two dice average 7; bars symmetric about 7; a finite batch wanders; 12 has chance 1/36 | correct | Linearity; law of large numbers |
| l2-dice-sum | s[2].prose | Fair value is the long-run average payout, the expectation E[X]; pay less and gain on average | correct | Definition (risk-neutral game value); Zhou ch. 4 |
| l2-dice-sum | s[2] bars, widget, feedback, explain | Three dice: 10.5; 10 and 11 each have 27 of 216; a fair value need not be attainable | correct | enum |
| l2-dice-sum | s[3] bars, widget, feedback, explain | £10 a six on three dice is worth £5; at least one six is 91/216; (10×75 + 20×15 + 30)/216 = 5 | correct | enum; linearity of expectation |
| l2-dice-sum | s[4] prose, widget, hints, feedback, explain | Larger of two dice is k in 2k − 1 rolls; fair value 161/36 ≈ 4.4722; mode 6 is above it | correct | enum; Zhou ch. 4 |
| l2-dice-sum | s[5] widget, hints | One die squared pays 91/6 ≈ 15.17; product of two different dice 12.25 | correct | enum |
| l2-dice-sum | s[5].feedback.byKey.product-of-means, s[5].explain.text, summary.ideas[2] | "Multiplying fair values works only for independent dice" | imprecise | E[XY] = E[X]E[Y] iff Cov = 0; independence is sufficient, not necessary (Casella and Berger Thm 4.5.5 and Example 4.5.9). sim (counterexample). Finding 4 |
| l2-dice-sum | s[5].explain.text | The gap 91/6 − 49/4 = 35/12 is one die's variance | correct | Var X = E[X²] − (E X)² |
| l2-dice-sum | s[6] prose, table, hints, feedback, explain | One die has variance 35/12; variances of independent dice add; sds 2.4152 and 2.9580; adding sds gives 3.4157, 5.1235 | correct | enum; Casella and Berger Thm 4.5.6 |
| l2-dice-sum | s[7] lines, why, explain | Var(X₁+X₂) = Var + Var + 2Cov; Cov = 0 for independent dice; root last; √(a+b) < √a + √b | correct | Casella and Berger Thm 4.5.6; true for a, b > 0 |
| l2-dice-sum | s[8].prose, summary.formula | E[Sₙ] = 3.5n, sd(Sₙ) = √(35n/12) for independent fair dice | correct | Linearity and additivity of variance |
| l2-dice-sum | s[8] options, explain | 100 dice: fair 350, sd 17.08; slips 170.8, 291.67, 300 | correct | Arithmetic |
| l2-dice-sum | s[8].explain.text | The total of 100 dice is very close to normal; 350 ± 17 holds about two thirds | correct | Exact convolution: 0.6945 (sim); CLT |
| l2-dice-sum | s[9] code, tests, hints, explain | `fair_value` averages a payout over all 6ⁿ rolls exactly; `sd_of_sum` is √(35n/12) | correct | CPython: 13/13 cases pass, starter fails |
| l2-dice-sum | s[10] widget, hints, feedback, explain | Sold 2 at 11.50 against fair 10.50: +£2 at fair value; if the dice come 14 the day loses £5; that loss is luck, the trade was worth +£2 | correct | Expected P&L against realised P&L |
| l2-dice-sum | s[11] options, hints | Centre the quote on 10.5; dice have no memory; halfway between 3 and 18 is 10.5 | correct | Independence of rolls |
| l2-dice-sum | s[11].explain.text | "perhaps 9.5 to sell to you and 11.5 to buy from you" | imprecise | Direction reads either way: the maker buys at 9.5 and sells at 11.5, but "to sell to you" can be heard as the maker selling at 9.5. Harris ch. 13 convention. Finding 5 |
| l2-dice-sum | summary.ideas[0..1], trap | Fair value is expected payout; fair values add; variances add so sd grows like √n; the mode is not the price | correct | As rows above |
| l2-dice-sum | q[0] | Sum of three dice with a 6 shown: 6 + 7 = 13 | correct | Conditional expectation with independent dice |
| l2-dice-sum | q[1] | Smaller of two dice: weights 13 − 2k, fair 91/36; larger plus smaller is the total, 161/36 + 91/36 = 7 | correct | enum |
| l2-dice-sum | q[2] | Four dice: sd √(35/3) ≈ 3.42, twice one die's sd; slips 6.83, 11.67, 1.71 | correct | Arithmetic |
| l3-how-wide | s[0] options, hints, feedback, explain | Two dice: 6 to 8 holds 16/36, 5 to 9 holds 24/36 = 2/3, 4 to 10 holds 30/36; the gain per step shrinks | correct | enum |
| l3-how-wide | s[1] prose, widget, feedback, explain | Width is high end minus low end; 6 to 8 has width 2 and holds 4/9; slips 3/11 and 3/36 | correct | Definition; enum |
| l3-how-wide | s[2] widget, hints, feedback, explain | 4 to 10 holds 30/36 = 5/6; six rolls outside; slip 7/11 | correct | enum |
| l3-how-wide | s[3] prose, options, hints | Under "width at most 2", 6 to 8 holds 16 rolls, 5 to 7 and 7 to 9 hold 15 | correct | enum |
| l3-how-wide | s[3].explain.text | "A range should sit on the fair value, where the chance is densest" | imprecise | True for a symmetric one-peaked total only; the larger of two dice has fair value 4.47 and its densest range is 5 to 6 (sim). l2 taught mode ≠ fair value. Finding 6 |
| l3-how-wide | s[4].prose | A range doubles as a quote: you buy at the low end and sell at the high end | correct | Bid below ask; Harris ch. 13 |
| l3-how-wide | s[4] check, wrong, hints, feedback, explain | Width 2 centred on 10.5 is 9.5 to 11.5; it holds totals 10 and 11, a quarter of rolls; a crossed quote buys higher than it sells; zero width has no edge | correct | enum (54/216) |
| l3-how-wide | s[5] prose, functions, options, hints, feedback, explain | Toy game: profit(h) = ½h(1 − h/4) − ½E[(|S−7| − h)⁺]; −0.97 at h = 0, −0.18 at 1, 0.27 at 2.5, peak about 0.28 near h = 2.7, 0 at h = 5 | correct | Derivation (peak at h = 8/3) and Monte Carlo of the stated game (sim) |
| l3-how-wide | s[5].explain.text, summary.ideas[1] | Tight quotes trade more but are picked off by the informed; wide quotes are safe but do not trade | correct | Glosten and Milgrom (1985); Harris ch. 14 |
| l3-how-wide | s[6] options, hints, feedback, explain | "Tight market, width at most 1" on one die: 3 to 4; the full range ignores the question; zero width ignores the uncertainty | correct | Interview convention; *Probability and Markets* |
| l3-how-wide | s[7] widget, hints, feedback, explain | Buy at 9.50, sell at 11.50: £2 locked in whatever the dice show; each trade earns half the width against fair value | correct | Flat position; cash 11.50 − 9.50 |
| l3-how-wide | s[8].prose, summary.formula | For a near-normal total, μ ± kσ holds a share fixed by k; P(|X − μ| ≤ σ) ≈ 0.68; two dice 7 ± 2.42 holds 5 to 9, 2/3 | correct | Normal table; enum |
| l3-how-wide | s[8] widget, feedback, explain | A contract that always pays £6 has σ = 0, so zero width: 6 at 6, or say it is known | correct | Convention of the lesson (width from uncertainty only), stated |
| l3-how-wide | s[9] prose, answer, wrong, hints, explain | Two dice: share inside 7 − k to 7 + k is 1 − (6−k)(5−k)/36 for whole k from 0 to 5 | correct | enum for k = 0..5 |
| l3-how-wide | s[10] code, tests, explain | `coverage` counts lo ≤ total ≤ hi exactly; three dice 8 to 13 holds 73/108, the first symmetric range past one half | correct | CPython: 10/10 cases pass, starter fails; enum |
| l3-how-wide | s[11] widget, hints, feedback | To hold the same share, the half-width scales with the sd (3 times), not the variance (9 times): ±60p | correct | Scale family: P(|X| ≤ kσ) fixed by k |
| l3-how-wide | s[11].prose, s[11].explain.text | A desk quotes a £20 share at fair value ±20p, one daily sd, and ±60p on results day | misleading | A quoted half-spread of one daily sd (1% of price) is about a hundred times a real spread in a liquid share; only the proportional widening is realistic (Harris ch. 14). Finding 7 |
| l3-how-wide | summary.ideas, trap | ± k sd holds a share set by k; width zero for a known payout, wider when the sd rises | correct | As rows above |
| l3-how-wide | q[0] | Three dice, 9 to 12: 104/216 = 13/27; slip 4/16 | correct | enum |
| l3-how-wide | q[1] | One die, 2 to 5: four faces, 2/3; slip 0.5 | correct | enum |
| l3-how-wide | q[2] | Two dice, width at most 4: 5 to 9 holds 24; 4 to 8 holds 23; 6 to 8 holds 16 | correct | enum |
| l4-fermi | s[0] | Pool 50 × 25 × 2 = 2,500 m³ = 2,500,000 litres; slip 250,000 | correct | 1 m³ = 1,000 L |
| l4-fermi | s[1] options, hints, explain | Doubling any one factor doubles a product; on a log axis each doubling is the same step | correct | Homogeneity of a product |
| l4-fermi | s[2] prose, widget, feedback, explain | A Fermi estimate breaks a quantity into factors you can guess; 500 × 20 × 8 = 80,000; slips 10,000 and 528 | correct | Definition; Zhou ch. 2; Crack |
| l4-fermi | s[3] options, hints, explain | 5 × 2 × 8 = 80 and 10² × 10¹ = 10³, so 8 × 10⁴, closest to 10⁵; say the magnitude first | correct | log₁₀ 80,000 = 4.90 |
| l4-fermi | s[4] table, hints, feedback | Lows multiply to 10,000, highs to 640,000: a factor of 8 each way from 80,000 | correct | Arithmetic (interval bound for positive factors) |
| l4-fermi | s[4].explain.text, s[5].options[0], s[5].hints[2], s[5].explain.text | The total is "good to a factor of 8"; "a factor of 8 either way is honest" | imprecise | 8 is the worst-case bound. With independent errors the 90% factor is 2^√3 ≈ 3.3 and ×8 holds over 99% (sim), an over-wide range by l1's own calibration standard. The worst case is named only two screens later. Finding 8 |
| l4-fermi | s[5] options[1..3] why, feedback | 95,209 from three guesses is false precision; "between 1 and 10 million" throws the estimate away | correct | 487 × 23 × 8.5 = 95,208.5 |
| l4-fermi | s[6] | One zero factor makes the product zero; ask whether a factor can vanish; then zero width | correct | Arithmetic |
| l4-fermi | s[7] prose, widget, feedback, explain | ln Q is a sum of logs; four factors of 2 compound to 16 in the worst case; errors that cancel give less | correct | Triangle inequality in logs; worst case stated |
| l4-fermi | s[8] lines, why, explain | Each ln fᵢ within ln rᵢ of ln cᵢ; bounds add; Q within a factor r₁r₂r₃; adding the rᵢ is false | correct | Derivation as written |
| l4-fermi | s[9] code, tests, prose, explain | Products of lows, centres and highs; "the product of the lows is the lowest total" | correct | CPython: 8/8 cases pass, starter fails; true for non-negative factors, which counts are |
| l4-fermi | s[10] widget, hints, feedback | Sold 3 at 90 against own fair value 80: +£30 on your numbers; slips −30, 10, 270 | correct | 3 × (90 − 80) |
| l4-fermi | s[10].explain.text | Someone keen to buy 3 at 90 may think the count is above 90 | correct | Adverse selection; Glosten and Milgrom (1985) |
| l4-fermi | s[11] | 40 × 5 × 2 = 400 contracts; quote a size of a few, not 100 | correct | Arithmetic; sizing judgement, stated as such |
| l4-fermi | summary.ideas, formula, trap | Say the power of ten first; doubts add in logs; the formula note names the worst case; one significant figure with its uncertainty | correct | As rows above |
| l4-fermi | q[0] | 252 × 8.5 × 60 = 128,520 trading minutes; slips 2,142 and 186,150 | correct | Arithmetic; 252-day convention stated in the item |
| l4-fermi | q[1] | Factors 2, 2, 3 and 1 compound to 12; ln 2 + ln 2 + ln 3 = ln 12 | correct | Worst-case product |
| l4-fermi | q[2] | 70 × 60 × 24 × 365 × 80 = 2,943,360,000, say about 3 × 10⁹ | correct | Arithmetic |
| review-1 | i[0] | The digit 7 appears 20 times in 1 to 100; 77 counts twice; slips 19, 10 | correct | enum |
| review-1 | i[1] | 38 of 50 at 90%: about 45 expected; P(≤ 38) ≈ 0.0032; overconfident, widen; fifty is plenty, ten too few | correct | Binomial(50, 0.9): 0.0032 |
| review-1 | i[2] | Gap of two dice: d ≥ 1 in 2(6 − d) rolls; fair value 35/18; slips 0 and 35/36; simulation 1.945 | correct | enum; sim with `random.Random(1)` gives 1.9447 |
| review-1 | i[3] | Largest of three dice: P(M ≤ k) = (k/6)³, E[M] = 6 − 225/216 = 119/24; six is largest in 91 of 216; simulation 4.958 | correct | Tail-sum formula; enum; sim |
| review-1 | i[4] | sd of £10 × (S₂ − 7) is 10 × 2.4152 = 24.15; shifting leaves the sd, scaling by 10 scales it by 10; ±£24 holds two thirds | correct | sd(aX + b) = |a| sd(X); enum 24/36 |
| review-1 | i[5] | Three dice 8 to 13 holds 146/216 = 73/108; acts like 10.5 ± 3, about one sd (2.96) each side | correct | enum; continuity correction |
| review-1 | i[6] | sd doubles, so the half-width doubles to £2: £48 at £52 | correct | Scale family (same toy desk as l3 s[11], see finding 7) |
| review-1 | i[7] options, why | 160,000 cm / 2.3 cm ≈ 70,000 coins; slips 700, 69,565.2, 7 million | correct | Arithmetic |
| review-1 | i[7].explain.text | "With the exact figures, 1,609.344 m and 2.25 cm, it is 71,526" | wrong | 22.5 mm was the round pound, withdrawn in 2017. The pound coin now in use is 23.43 mm corner to corner (Royal Mint), which gives 68,687. The prose itself says 2.3 cm. Finding 9 |
| review-1 | i[8] | Worst case 2 × 2 × 1.5 × 3 = 18; pin down the factor of 3 first | correct | Worst case named in the question |
| review-1 | i[9] | Sold 2 at 220 and bought 1 at 200, value 204: +32 + 4 = +36, short 1; slips 16, 28 | correct | Mark to the settlement value |
| homework-1 | i[0] prose, code, tests | Centre ⌊2μ + ½⌋/2; widen an integer quote until it holds half the rolls or passes the limit; population sd | correct | CPython: 17/17 cases pass, starter fails; enum of each test |
| homework-1 | i[0].explain.text | The product of two dice has no such quote under width 10 "because its payouts are too lumpy" | imprecise | The cause is spread: sd 8.94, so half the mass needs a width above 10 whatever the lumps (sim). Finding 10 |
| homework-1 | i[1] prose, code, tests | Two-sided exact binomial p-value: add every count no more likely than the observed one; 7 of 10 gives 0.070, 14 of 20 gives 0.011, 50 of 50 gives 0.008 | correct | Minimum-likelihood exact test as in R `binom.test`; CPython: 12/12 pass, starter fails |
| homework-1 | i[1].prose, i[1].explain.text | Below 0.05 call it over- or underconfident, "else calibrated" | imprecise | Failing to reject is not evidence of calibration (Casella and Berger sec. 8.3); 7 of 10 is labelled calibrated here and overconfident in l1. Finding 1 |
| homework-1 | i[2] | Order: clarify, estimate, range, quote, update; silent exact working loses marks | correct | *Probability and Markets*; interview practice |
| homework-1 | i[3] | 204 = 8 × 9 × 17 / 6; 1,296 counts rectangles, C(9,2)² | correct | Sum of squares formula |
| homework-1 | i[4].model | Clarify; "about 200, 90% sure of 150 to 300"; quote 180 at 230, width 50 around 205; running totals to 204; then 204 at 204; a sale at 230 marks +£26 | correct | Arithmetic checked (L1 script); consistent with the lesson's conventions |
| homework-1 | i[4].rubric[0..4] | Marks for clarifying, a range that holds 204 before calculating, the (9 − k)² count with a check, quotes before and after, +£26, speaking in order | correct | Matches the model and the lessons |
| homework-1 | i[5] | Digit sums of 1 to 100 add to 901: fair value 9.01; slips 9 and 4.5 | correct | enum |
| homework-1 | i[6] | Distinct faces on three dice: 6 × 91/216 = 91/36; three distinct in 120 of 216; simulation 2.528 | correct | Indicator sum; enum; sim |
| homework-1 | i[7] | Low end 1,000 × 1,000 = 1,000,000; high 36,000,000; a factor of 6 each way | correct | Worst-case bound, as taught |
| homework-1 | i[8] | Bought 3 at 6, sold 1 at 8: +£4 at fair 7; +£8 at the roll of 9; £4 is edge and £4 is luck from being long 2 | correct | 3 × 1 + 1; 3 × 3 − 1; 2 × (9 − 7) |

## Level 2

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l5-two-sided | s[0] options, hints, feedback, explain | With fair value 10.5, buying at 9.5 and selling at 11.5 each earn 1 on average; a crossed pair around 10.5 loses 1 either way; one price at 10.5 earns nothing; 3 at 18 never trades | correct | Edge against fair value; Harris ch. 13 |
| l5-two-sided | s[0].prose | *Probability and Markets* opens with "make me a market" | correct | Jane Street guide, market-making section |
| l5-two-sided | s[1] options, explain | Every trade earns on average exactly when the fair value sits strictly between the two prices; a wider gap earns more a trade and trades less often | correct | 10.5 − b > 0 and a − 10.5 > 0 |
| l5-two-sided | s[2].prose | Bid is your buying price, ask your selling price; said "9.5 at 11.5", bid first; width is ask minus bid; size "3 up" | correct | Dealer convention; Harris ch. 13; *Probability and Markets* |
| l5-two-sided | s[2] widget, hints, feedback, explain | The interviewer buys at your ask, 11.5; you are short 3; "a buyer always pays the ask and a seller always gets the bid"; nobody trades at 10.5 | correct | True for the party who trades on a maker's quote, which is the only case in the game (Harris ch. 4 and 13) |
| l5-two-sided | s[3] | Sold 3 at 11.50 against fair 10.50: +£3 at fair, short 3; slips −3, 1, 34.5 | correct | 3 × (11.50 − 10.50) |
| l5-two-sided | s[4] | Larger of two dice, width at most 1: 4 at 5 holds 4.47; 4.47 outside the quote trades one side at a loss | correct | 161/36 between 4 and 5 |
| l5-two-sided | s[5] prose, check, feedback | Heads before the first tail pay £1 each: fair value £1; quote £0.50 at £1.50; centring on 2 confuses flips with heads | correct | Geometric: Σ k/2^(k+1) = 1; mean flips 2; sim |
| l5-two-sided | s[5].explain.text | "The payout is often 0, so the bid should stay well under £1" | imprecise | The bid sits under £1 because a bid at or above fair has no edge, not because the payout is often 0; the next sentence says the centre is still the mean. Finding 11 |
| l5-two-sided | s[6] | Product of two independent dice: 3.5 × 3.5 = 12.25; width 2 gives 11.25 at 13.25; centring on 7 prices the sum | correct | E[XY] = E[X]E[Y] under independence |
| l5-two-sided | s[7] | 5.5 at 6.5 is centred on the mode 6; a sale to you at 5.5 loses about 1.03; centre on the mean, 4 at 5 | correct | 5.5 − 161/36 = 1.03 |
| l5-two-sided | s[8].prose | "a crossed quote, bid above ask, loses on every trade" | imprecise | False when the fair value lies outside the crossed quote (bid 12, ask 11, fair 13: the purchase earns 1). What always loses is the round trip. sim. Finding 12 |
| l5-two-sided | s[8] formula, widget, explain; summary.formula | bid = μ − h, ask = μ + h, width 2h; four dice, h = 1.5: 12.5 at 15.5 | correct | Definition |
| l5-two-sided | s[9] | Buying q at μ − h and selling q at μ + h earns 2qh, the width times the size; one trade earns qh | correct | Algebra |
| l5-two-sided | s[10] code, prose, explain | `quote` centres on fair; a valid quote holds fair and respects the width cap; a known payout may have zero width | correct | CPython: 14/14 cases pass, starter fails |
| l5-two-sided | s[11] | Model value £4.20, width at most 10p: £4.15 at £4.25, the best quote on both sides of the shown book | correct | 4.15 > 4.10 and 4.25 < 4.30 |
| l5-two-sided | summary.ideas, trap | Centre on the mean, not the mode; never let the bid pass the ask | correct | As rows above |
| l5-two-sided | q[0] | "I only want to sell": answer with a bid below 7; a bid at 7 earns nothing, at 8 loses 1 | correct | One-sided market convention |
| l5-two-sided | q[1] | Crossed "12 at 10" around 10.5: buy at 12 loses 1.5, sell at 10 loses 0.5, −£2 | correct | Arithmetic; here fair lies inside the crossed quote |
| l5-two-sided | q[2] | "8 at 12" suggests fair value 10 and width 4 | correct | Mid of an unskewed quote; the item says "suggests" |
| l5-two-sided | q[3] | Two dice, width at most 2: 6 at 8 | correct | Fair 7 |
| l6-edge | s[0], s[1] | Pay £3 for a die's face: +£0.50 a play; single plays run −£2 to +£3; the average of many settles near £0.50 | correct | E = 3.5 − 3; law of large numbers |
| l6-edge | s[2].prose, s[8].prose, summary.formula | Edge is what a trade earns on average at its price: sale p − μ, purchase μ − p; a game E[payout] − stake | correct | Standard interview usage (expected value per unit against fair) |
| l6-edge | s[2].explain.text | "Each unit earns 1.5 on average, whatever the dice show" | imprecise | The position is open: single rolls pay from +9 to −6. "Whatever the dice show" was used correctly for a flat position in l3. sim. Finding 13 |
| l6-edge | s[3] | Coin game worth £1 at a £1.20 charge: edge −£0.20; decline or sell the game; slips 0.2, 0.8, −1.2 | correct | E = 1 |
| l6-edge | s[4] | £2 on heads for £1.10: edge −£0.10 | correct | ½ × 2 − 1.10 |
| l6-edge | s[5]; summary.ideas[2]; q[2] | Against random flow each trade earns the half-width; four trades at 9.5 or 11.5 earn £4, long 2 | correct | Each trade is h from fair |
| l6-edge | s[6] options, feedback, explain | A sale at 12 against 10.5 had edge +1.5; the 14 was bad luck; about 26% of rolls land above 12; a thousand repeats earn about £1,500 | correct | 56/216 = 0.259 |
| l6-edge | s[6].hints[1].text | "Most rolls land at 12 or below, where the sale wins" | imprecise | At 12 the sale breaks even; it wins below 12, on 135 of 216 rolls. Finding 14 |
| l6-edge | s[7] | One play has variance 35/12; 100 plays have sd £17.08, so £70 is about one sd above £50; one play at 100 times the size has sd £170.78 | correct | Additivity of variance; path steps checked (L2 script) |
| l6-edge | s[8] widget, explain | A trade at fair value has zero edge; it is worth doing only to change your position | correct | Edge definition; inventory motive (Harris ch. 13) |
| l6-edge | s[9] | E = ½ × 0 + ½(1 + E) gives E = 1; stopping after one flip gives ½ and is wrong | correct | First-step analysis (Zhou ch. 4); E is finite |
| l6-edge | s[10] code, explain | `edge` flips sign with the side; `game_edge` is exact; larger of two dice for £4 gives 17/36 | correct | CPython: 13/13 cases pass, starter fails |
| l6-edge | s[11] | 2,000 trades × 100 shares × 0.5p = £1,000 expected a day; one day's −£300 is noise | correct | Arithmetic |
| l6-edge | summary.ideas[0..1], trap | Edge is fixed at the price; one outcome says little about it | correct | As rows above |
| l6-edge | q[0], q[1], q[3] | 161/36 − 4 = 17/36; buying 2 at 9 earns 3; a purchase at 9.5 has edge +1 though a 7 lost 2.5 | correct | Arithmetic |
| l7-skewing | s[0] options, hints, feedback, explain | Lifted for 2 you are short and lose if the total is high; move both prices up: a higher bid attracts sellers, a higher ask slows buyers; widening only trades less | correct | Inventory control; Harris ch. 13; Avellaneda and Stoikov (2008) reservation price |
| l7-skewing | s[1], s[2] prose, s[8] formula, summary.formula | Skew: centre m = V − γq with q positive long; bid m − h, ask m + h; width unchanged | correct | Linear form of the Avellaneda and Stoikov reservation price r = s − qγσ²(T − t) |
| l7-skewing | s[2] widget, feedback | q = −2, γ = 0.25: centre 11, quote 10 at 12 | correct | Arithmetic |
| l7-skewing | s[3] | Lifted, lifted, hit, lifted: positions −1, −2, −1, −2; bids 9.75, 10, 9.75, 10; "lifted means you sold"; each trade happens at the quote shown before it | correct | Rule applied step by step (L2 script); lift/hit convention (Harris ch. 4) |
| l7-skewing | s[4] | Bought at 9.50 and 9.25, sold at 11.00: +£2.75 at fair, long 1; without skew it would be 3; the skew gives up a little edge to cut the position | correct | 1 + 1.25 + 0.5 |
| l7-skewing | s[5] | Short 3: quote 10.25 at 12.25; lowering the quote to sell more grows the short; "skew against your inventory, never with it" | correct | m = 10.5 + 0.75; sim (skewing sheds inventory faster) |
| l7-skewing | s[6] | Two reasons to raise the quote after a lift on an unknown number: information (the buyer may know it is higher) and inventory (you are short); a lift says nothing about width | correct | Glosten and Milgrom (1985) for information; Avellaneda and Stoikov for inventory |
| l7-skewing | s[7], q[3] | A declared random buyer moves the position, not the fair value: new quote 9.75 at 11.75 | correct | No information in the trade, so E[V given a buy] = V |
| l7-skewing | s[8].prose, hints | "News moves V; trades move q" | correct | Rule of the lesson; s[6] has already said an informed trade is news |
| l7-skewing | s[8] widget, explain | Long 4: quote 8.5 at 10.5; the ask at fair value is the zero-edge trade that sheds risk | correct | m = 9.5 |
| l7-skewing | s[9] | Ask = 11.5 − 0.25q; slips 11.5 + 0.25q and 9.5 − 0.25q | correct | Algebra |
| l7-skewing | s[10] code | `skewed_quote` and `quote_path` (+1 hit, −1 lifted) | correct | CPython: 12/12 cases pass, starter fails |
| l7-skewing | s[11] | Short 2,000 calls is 20 lots; at £0.005 a lot the centre rises £0.10: £2.50 at £2.60; short calls lose if the share jumps | correct | Arithmetic; short calls are short delta |
| l7-skewing | summary.ideas, trap | Up after being lifted, down after being hit; two reasons to move | correct | As rows above |
| l7-skewing | q[0], q[2] | Long 3: ask 10.75; sold 2 at 12 and bought 1 at 10: +£3.50, short 1 | correct | Arithmetic |
| l7-skewing | q[1] | Fair 50, long 5: "47.5 at 49.5" is the quote that fits a skew | imprecise | The keyed ask is below the stated fair value: by the previous lesson its edge is −0.5 a unit. The explain does not say the skew is paying to shed risk. Finding 15 |
| l8-informed-flow | s[0] widget, hints, feedback | An interviewer who has seen the die buys above the ask and sells below the bid; 2.5 at 4.5 loses (1.5 + 0.5 + 0.5 + 1.5)/6 = 2/3 a game | correct | enum; sim |
| l8-informed-flow | s[0].explain.text | "You lose 2/3 a game, however the die is centred" | imprecise | Garbled: a die is not centred. The point is that the quote is centred on fair value and still loses. Finding 16 |
| l8-informed-flow | s[1] options | 0.5 at 6.5 loses nothing; 1.5 at 5.5 loses 1/6; 3 at 4 loses 1; 3.5 at 3.5 trades on every face the wrong way | correct | enum |
| l8-informed-flow | s[1].feedback.correct, s[1].explain.text | "Only the whole range, 0.5 at 6.5, is safe"; "every narrower quote leaves a face that trades against you" | wrong | 1 at 6 is narrower, is reachable on the sliders and loses nothing: no face is above 6 or below 1. enum. Finding 17 |
| l8-informed-flow | s[2].prose | Adverse selection: losing to someone who trades only when you are wrong | correct | Glosten and Milgrom (1985); Harris ch. 14 |
| l8-informed-flow | s[2] table, feedback, explain | Loss is the distance outside the quote, summed over faces, over 6: 1/6 and 1; the tighter the quote, the more the informed take | correct | enum |
| l8-informed-flow | s[3] | Half informed, half random at any width, quote 1.5 at 5.5: ½ × 2 − ½ × 1/6 = 11/12 | correct | enum; sim |
| l8-informed-flow | s[4] | 2 at 5 earns 7/12, 2.5 at 4.5 earns 1/6; the widest earns most in this toy because the random half trades at any width; real flow thins as you widen | correct | enum; the toy's hypothesis is stated |
| l8-informed-flow | s[5] | Against an interviewer who sees the die, tightening from 2 at 5 to 3 at 4 triples the loss, 1/3 to 1; widen; a loss taken is gone | correct | enum |
| l8-informed-flow | s[6] | Dice 2, 3, 1, 6 at 2 at 5: no trade, no trade, −1, −1: −£2; expected 4/3 | correct | A die on the bid is not below it; enum |
| l8-informed-flow | s[7] prose, widget, explain; summary.formula | Zero-profit half-spread s = αδ for a share α informed about ±δ; α = 0.2, δ = 30p gives 6p | correct | Glosten and Milgrom (1985) one-period case: ask = E[V given a buy] = V + αδ when the uninformed buy or sell with equal chance; sim |
| l8-informed-flow | s[8] | Average a game (1 − α)h − αL(h); break-even where (1 − α)h = αL(h); L falls as h grows, so larger α needs larger h; an informed trader does not cost h | correct | Derivation; consistent with s = αδ when L(h) = δ − h |
| l8-informed-flow | s[9] code | `informed_loss` uses strict inequalities; `mixed_pnl` weights the random half-width against it; α = 0.2 at 1.5 at 5.5 earns 47/30 | correct | CPython: 13/13 cases pass, starter fails |
| l8-informed-flow | s[10] | 500p share, α = 0.2: 498 at 502 on a normal day, 494 at 506 before results; informed flow is called toxic | correct | s = αδ; usage as in Easley, López de Prado and O'Hara (flow toxicity) |
| l8-informed-flow | summary.ideas, trap | Every trade an informed player chooses loses; widen until random earning and informed loss balance | correct | As rows above |
| l8-informed-flow | q[0] | "I have not looked at it": 3 at 4, the plain two-sided game; zero width earns nothing | correct | No information asymmetry |
| l8-informed-flow | q[1], q[3] | 2.5 at 5.5 loses 5/12; two dice at 5 at 9 lose 20/36 = 5/9; chance of a trade 12/36 | correct | enum |
| l8-informed-flow | q[2] | α from 0.2 to 0.4 with δ = 10p: 4p | correct | s = αδ |
| l9-cards-revealed | s[0] | Three cards from one deck, ace 1 to king 13: each averages 364/52 = 7, sum 21; slips 19.5 and 364 | correct | Linearity; holds without replacement |
| l9-cards-revealed | s[1], s[2].prose | After a king, 351 points sit in 51 cards, 6.88 a card; each unseen card has the remaining mean | correct | Exchangeability of the undealt cards; enum |
| l9-cards-revealed | s[2] widget, feedback, explain | Fair value 13 + 2 × 351/51 = 455/17 ≈ 26.7647, up 5.76, not 6; slips 27, 13, 19.88 | correct | enum over the remaining pairs; sim |
| l9-cards-revealed | s[3] | Sold 1 at 23 before the king: +2 at 21, then −£3.76 at 26.76; a ledger marked at fair moves with every reveal | correct | Mark to market |
| l9-cards-revealed | s[4] | New quote: centre within 0.5 of 26.76, width at most 4, e.g. 25 at 28.5; short 1 you might lean higher | correct | Rule of the screen; skew direction as taught |
| l9-cards-revealed | s[5] | K and 2 shown: 15 + 349/50 = 21.98; the short at 23 is +£1.02; fair value fell 4.78 | correct | enum |
| l9-cards-revealed | s[6], q[2] | Fresh deck for each card: the king tells nothing, 13 + 7 + 7 = 27; ace gives 15 | correct | Independence |
| l9-cards-revealed | s[7] | Two kings: 26 + 338/50 = 32.76, not 33; a third king is less likely, 2 of 50 | correct | enum |
| l9-cards-revealed | s[8] | Change in fair value when the first card shows c: 49(c − 7)/51; a king gives 5.76 | correct | Algebra; enum for c = 1..13 |
| l9-cards-revealed | s[9].prose, summary.formula | F = S + (n − k)(T − S)/(N − k); F = S when k = n | correct | Conditional expectation of a sample without replacement (Cochran ch. 2); enum |
| l9-cards-revealed | s[9] widget, explain | Ace first: 1 + 2 × 363/51 = 259/17 ≈ 15.2353; remaining mean 7.12 | correct | enum |
| l9-cards-revealed | s[10] code | `card_sum_fair` and `quote_after_reveals`, exact | correct | CPython: 13/13 cases pass, starter fails |
| l9-cards-revealed | s[11] | Two of five companies report £2.60 and £1.80, the rest unaffected: £10.40; linked results would move the others too | correct | Independence stated in the item |
| l9-cards-revealed | summary.ideas, trap; q[0] | When the last card turns the market collapses to the known sum: 21 at 21, or decline | correct | Convention of the course for a known value |
| l9-cards-revealed | q[1], q[3] | Queen first of four: 12 + 3 × 352/51 = 556/17; long 1 at 20 marks −£4.76 after an ace | correct | enum |
| review-2 | i[0], i[1] | Four dice, width 2: 13 at 15; smaller of two dice for £2.50: edge 1/36, swamped by variance over a few plays | correct | Arithmetic |
| review-2 | i[2], i[6] | Long 2 at γ = 0.5: quote 8.5 at 10.5, ask at fair; hit four times means long 4, move both prices down | correct | Skew rule |
| review-2 | i[3] | Informed interviewer, quote 2 at 4: faces 1, 5, 6 cost 1, 1, 2: 2/3 a game; counting trades gives 3/6 | correct | enum |
| review-2 | i[4], i[9] | Queen and 5 shown: 17 + 347/50 = 23.94; one king of two cards: fresh decks are higher by 2/17 | correct | enum |
| review-2 | i[5] | Sold 2 at 8, bought 1 at the skewed bid 6.5, fair 7: +£2.50, short 1 | correct | Arithmetic |
| review-2 | i[7] | Share 400p, α = ¼, δ = 12p: ask 403p, bid 397p | correct | s = αδ |
| review-2 | i[8] | Sold at 9 on two dice: edge +2; only 10 to 12 lose, 1 roll in 6 | correct | 6/36 |
| homework-2 | i[0] code, tests, explain | Scripted card game: each trade at the rule's quote for the fair value and position of the moment; P&L is cash plus position times the true sum; the mock round settles at +3 | correct | CPython: 10/10 cases pass, starter fails |
| homework-2 | i[1] code, tests, explain | Break-even half-width is the smallest h with (1 − α)h ≥ αL(h); the gap rises with h and is piecewise linear; die α = ½ gives 4/5, α = 1 gives 5/2 | correct | CPython: 11/11 pass, starter fails; bisection (L2 script) |
| homework-2 | i[2] | After a lift: update fair value, skew for the position, check the limit, requote; lowering the ask loses marks | correct | Order follows the lessons; the limit check before the quote is the course's convention |
| homework-2 | i[3].model | Mock round: 21 and 19 at 23; long 2 skews to 18 at 22; 3 shown gives 17.16, −£3.69, 14 at 18; sale at 18 gives −£2.84, 14.5 at 18.5; jack gives 21, +£1, 18.5 at 22.5; 9 gives 23 and +£3 | correct | Every number recomputed (L2 script) |
| homework-2 | i[3].rubric[0..5] | Marks for 21 from 364/52, the updates 17.16, 21, 23, width with a reason, moves named as information or inventory, ledger −£3.69, +£1, +£3, speaking in order | correct | Matches the model |
| homework-2 | i[4], i[5], i[6] | 3 shown: 875/51; 3 and jack shown: exactly 21 because they average 7; final P&L −20 + 23 = +£3 | correct | enum |
| homework-2 | i[7] | Two dice, half informed, 5 at 9: ½ × 2 − ½ × 5/9 = 13/18 | correct | enum |
| homework-2 | i[8] | Six pays £6, five pays £1, stake £1: edge 1/6; play in small size | correct | 7/6 − 1 |
