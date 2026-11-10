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
