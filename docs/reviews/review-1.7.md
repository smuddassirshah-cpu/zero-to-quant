# Topic 1.7 (finance basics): second-reader findings

Scope: every lesson, review and homework file in `markets`, `options`, `trees` and `micro`, plus `app/content/exams/topic-1.7.json`.

Method:
- Every stated number was recomputed in Python, including explanations, captions, feedback, hints, model answers and rubrics.
- Black-Scholes and the Greeks came from an independent `bs.py`. Every tree figure was checked against an independent numpy CRR pricer (`crr.py`), European and American.
- Seeded `random.Random` claims were re-run. Hedging simulations were rerun with 40,000 paths (`hedge.py`, `hedgesim.py`).
- Every code item's tests were run against an independent implementation.
- Each distractor value was re-derived from its `why`.
- Tolerance overlaps were scanned (`tolcheck.py`), and style was scanned (`style.py`, `sentcount.py`).
- Scripts are in the session scratchpad, `review-1.7/`.

Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation or teaching issue; note = style.

## markets

- app/content/courses/markets/l1-interest-on-interest.json | quiz q-simple-vs-compound option b-small | warning | The why says the gap is "1% over 10 years", but the question's horizon is 20 years (a £200 gap). | Say "over 20 years", with the £200 gap.
- app/content/courses/markets/l2-present-value.json | screens[9] explain | note | "The headline overstates the prize by about a third" is ambiguous. The headline is 47% above the value; the value is about a third below the headline. | "The value is about a third below the headline."
- app/content/courses/markets/l4-npv.json | screens[3] explain | note | "Solving for it exactly needs Newton's method": any root-finder works (bisection is used in l6), and Newton gives an approximation. | "We solve for it numerically, for example by Newton's method."
- app/content/courses/markets/l5-pricing-a-bond.json | screens[1] wrong coupons-only (17.32) | warning | The why says "the four coupons alone, and part of year 5", but 17.32 is all five £4 coupons discounted, with no face. | "That is the five £4 coupons alone. Add the £100 face at year 5."
- app/content/courses/markets/l6-yield.json | screens[2] hints[2] and explain | error | The bisection prices are wrong. The text gives £92.15 at 5.85% and £91.95 at 5.90%; the bond prices are 92.1752 and 91.9747. | £92.18 and £91.97.
- app/content/courses/markets/l6-yield.json | screens[4] prose | warning | The prose says the 4.40 modified duration was found "in the Series and Approximation course". It was found in Limits and Derivatives l15, and taylor l4 says so itself. | "In Limits and Derivatives you found..."
- app/content/courses/markets/l6-yield.json | screens[5] table | note | The 10-year answer cell is −7.59, but the hint, feedback and explain say −7.58 (true −7.584). | Answer −7.58.
- app/content/courses/markets/l6-yield.json | screens[8] wrong inverse (0.0433) | warning | The why says "the £4.33 pull to £100 over the price", which gives 4.33/95.67 = 0.0453. 0.0433 is 4.33/100. | Value 0.0453, or a why that says "over the £100 face".
- app/content/courses/markets/l6-yield.json | screens[11] explain | note | "A rise of a couple of points" understates 2022. The US aggregate index yield rose about three points (1.75% to 4.68%). | "about three points"
- app/content/courses/markets/l8-measuring-returns.json | screens[6] | warning | It repeats l1 screens[8]: 1% a month gives 12.68%, with the same 12% distractor. | New numbers, e.g. 0.75% a month gives 9.38%.
- app/content/courses/markets/l11-margin.json | screens[7] explain | note | The third sentence (limit-down halts) has nothing to do with the basis task and is not introduced anywhere. | Drop it or move it to a margin screen.
- app/content/courses/markets/l12-selling-what-you-do-not-own.json | summary.ideas[2] | note | It says "a profit of P0", but the generalise screen gives P0 − C. | "a profit of at most P0, less costs"
- app/content/courses/markets/l13-leverage.json | quiz q-recover explain | warning | It shows an internal id: "(the taylor course, lesson 12)". | "(Series and Approximation, lesson 12)"
- app/content/courses/markets/l13-leverage.json | screens[5] explain vs summary.ideas[1] | note | "Leverage magnifies losses more than gains" contradicts the summary's "Gains and losses scale alike". | "...so the interest drags on both outcomes."
- app/content/courses/markets/homework-2.json | h-bond-hold wrong five-year (−0.0013) | error | The slip in its why gives (91.5753 + 4 − 95.6705)/95.6705 = −0.0010. −0.0013 is outside that value's tolerance, so the key never fires. | −0.0010
- app/content/courses/markets/review-3.json | r-margin-loan wrong orig (21000) | warning | The why ("took 30% of the original £30,000 as the trigger") gives 18,000 + 9,000 = 27,000. 21,000 is a 30% fall in the position. | Value 27000, or rewrite the why for a 30% fall.
- app/content/courses/markets/l1-interest-on-interest.json, l6-yield.json, l8-measuring-returns.json, homework-2.json | screens[3] explain, quiz[1], screens[3], quiz[2], screens[2], screens[9], items[1] | note | "percent" is the American spelling. | "per cent"
- app/content/courses/markets/l4-npv.json, homework-1.json, homework-3.json | widget.how | note | "math.isclose" is in prose without code formatting. | `math.isclose`
- app/content/courses/markets/l6-yield.json | screens[3] and screens[8] explain | note | Four sentences each (the limit is 3). | Merge two.
- app/content/courses/markets (18 sentences) | e.g. l10 screens[0] prose (27 words), l11 screens[6] prose (29), l12 screens[7] prose (29), homework-3 items[4] how (26) and explain (25) | note | These sentences are over 20 words. | Split them.

## options

- app/content/courses/options/l1-right-to-buy.json | screens[10] explain | note | "The cash would be untouched ... misses only the first £5.00 of the rise" leaves out the calls' premium, and the prose never says to ignore it. | Add "Ignore what the calls cost" to the prose, or "less the premium".
- app/content/courses/options/l4-buying-or-writing.json | screens[10] prose and explain | warning | "As in 2008, the index crashes to 60": no major index fell 40% in a month in 2008 (the S&P 500's worst month, October 2008, was −16.9%). | Drop "as in 2008", or crash to 80.
- app/content/courses/options/l6-straddles.json | screens[8], summary.formula | note | Premiums are written C and P, while l3, l9 and l10 use c and p. | c + p
- app/content/courses/options/l6-straddles.json | quiz q-strangle explain | note | "Cheaper protection buys a wider band of loss": a strangle is not protection. | "The cheaper bet needs a wider move."
- app/content/courses/options/l7-butterfly.json | screens[8] explain | error | It says many scaled-up butterflies tend to a digital payoff. That is false: a call spread scaled by 1/h tends to a digital, and a butterfly scaled by 1/h² tends to a spike at one price (an Arrow-Debreu payoff). | "Scale a narrow call spread by 1/h and it becomes a digital. A butterfly scaled by 1/h² pays only at £100.00."
- app/content/courses/options/l7-butterfly.json | screens[10] explain | warning | "Pricing with Trees builds that map into a risk-neutral density": trees never builds a density, only the risk-neutral q on a tree. The explain is also four sentences. | "Pricing with Trees turns such chances into risk-neutral probabilities." Cut to three sentences.
- app/content/courses/options/l7-butterfly.json | screens[5] option d (£34.00) | note | The why says "You counted the £95.00 call alone", but the lower wing alone gives 35 − 7.50 = £27.50. £34 is 35 less the butterfly's £1.00. | Value £27.50, or why "You kept the lower wing's payoff and took off the £1.00 cost."
- app/content/courses/options/l9-put-call-parity.json | screens[2], screens[4], screens[8], quiz q-price-put, q-call-dear | error | A literal `{P}` sits inside maths in five places ("$p = {P}7.14$", "{P}0.86", "{P}8.57", "{P}3.28", "{P}0.60"). It renders as an italic P before each number. | `\text{£}`
- app/content/courses/options/l9-put-call-parity.json | screens[2] prose and feedback | warning | "its one-step tree price from trees" uses an internal id. It also refers forward: Pricing with Trees comes after Options. | "the price a one-step tree gives (you build it in Pricing with Trees)"
- app/content/courses/options/l9-put-call-parity.json | screens[6] feedback.correct | note | "The £4.76 gap is a year's interest on £100.00": at 5% that is £5.00. 4.76 is a year's interest on £95.24. | "...a year's interest on £95.24."
- app/content/courses/options/l9-put-call-parity.json | screens[9] explain | note | "with the forward F = 105 from markets" uses an internal id. The explain is also four sentences. | "from Markets and Instruments". Trim to three sentences.
- app/content/courses/options/l10-bounds.json | screens[9] prose, screens[11] prose | note | They use internal lesson ids: "(level 2, l7)" and "as in l7". | Use the lesson name, "A bet on staying put".
- app/content/courses/options/l11-exercise-early.json | screens[0] question, screens[8], screens[6] explain | note | They use internal ids: "from l10", and "The trees course ... in l7". | Use lesson and course names.
- app/content/courses/options/l11-exercise-early.json | screens[9] transfer | warning | The prose gives no rate, but the canvas floor of £28.55 and the explain use 5% for four years. | Add "Rates are 5% a year."
- app/content/courses/options/l12-how-price-responds.json | screens[7] trap option inverse | note | The why says "0.47 happens to be the pricing chance here, but not because of 1 − Delta". With r = 0 and S = K, d2 = −d1, so N(d2) = 1 − N(d1) exactly. | "It equals 1 − Delta only because r = 0 and S = K here."
- app/content/courses/options/l12-how-price-responds.json | screens[8] table, summary.ideas[2] | warning | It states generally that "long options have negative theta". A deep in-the-money European put with r > 0 has positive theta (+1.58 a year at S = 80, K = 100, r = 5%, σ = 20%, T = 1). l11 screens[6] shows such a put below its payoff. | "With rates at 0, long options have..." or name the exception.
- app/content/courses/options/review-2.json | r-short-strangle wrong centre (−15) | warning | The slip in the why ("You measured the move from £100.00") gives 5 − 15 = −10, the same value as noprem. −15 also drops the premium. | Why "You measured from £100.00 and forgot the £5.00 collected."
- app/content/courses/options/review-2.json | r-cc-put | note | The wrong ids premium, gap and diff have no byKey lines. | Add one line each.
- app/content/courses/options/homework-2.json | h-long-spread (longform) | warning | It repeats l5 screens[10] and quiz q-why: the same £100/£110 spread at £3.50 against the call at £6.00, the same £106 view and the same £112.50 crossover. | New strikes and premiums.
- app/content/courses/options/l8-with-the-stock.json, l9-put-call-parity.json, l12-how-price-responds.json, homework-1.json, homework-2.json, homework-3.json | widget.how | note | "math.isclose" is in prose without code formatting. | `math.isclose`
- app/content/courses/options (37 sentences) | e.g. l11 screens[8] prose (30 words), l7 screens[7] prose (29), review-2 items[5] prose (29), l7 screens[9] prose (27), homework-2 items[4] prose (27) | note | These sentences are over 20 words. | Split them; break before display formulas.

## trees

- app/content/courses/trees/l2-copying-the-option.json | screens[7] prose | note | "as in the vectors course" uses an internal id. | "as in Vectors and Matrices"
- app/content/courses/trees/l2-copying-the-option.json | quiz q-call-13 option reverse why | note | "That pays £11.90 for the copy's mirror and £13 for the call" is muddled: selling the copy brings in £11.90. | "You pay £13 for the call and get only £11.90 for the copy: you lose £1.10."
- app/content/courses/trees/l4-hedge-ratio.json | screens[7] prose | note | "as in limits ... as in multivar" uses internal ids. | Limits and Derivatives; Multivariable Calculus.
- app/content/courses/trees/l5-two-steps.json | quiz q-new-tree wrong middle (3.15) | warning | The why says "You counted the middle node as paying", but the £49.50 node cannot pay a £50 call. Counting −0.50 there gives 3.40. 3.15 matches no slip. | Value 3.40 with why "You let the middle node pay 49.50 − 50", or drop it.
- app/content/courses/trees/l6-calibrating.json | screens[3] feedback.correct | note | With the rounded inputs shown, 0.1078/0.2004 = 0.5379, not 0.5378. | "0.1077/0.2003 = 0.5378" or "about 0.5378".
- app/content/courses/trees/l6-calibrating.json | screens[3] prose | note | The rate convention changes in one clause. Level 1's "5% a year" grows by 1.05; here "5%" is continuous and grows by e^{0.05} = 1.0513. The rate keeps its name but changes meaning. | "From here, r is a continuously compounded rate: £1 grows to e^{rΔt} over a step."
- app/content/courses/trees/l7-american-on-a-tree.json | screens[7] | warning | The prose ("the four-step tree from the last lesson ... r = 5%") silently switches to e^{rΔt} per step. Hold values 5.88 and 10.58 and the European 5.09 need e^{0.0125}; 1.05 a year or 1.0125 a step give 5.92 and 5.89. Screens[5] (generalise) and summary.formula in the same lesson divide by (1 + r). | Add "each step now grows cash by e^{rΔt}, as in the last lesson" to screens[7]. Write the summary formula with a one-step growth factor R.
- app/content/courses/trees/l9-tiny-steps.json | screens[2] table, 8-step row | note | The error is shown as −0.24 (10.21 − 10.45). The true error is −0.2455, which rounds to −0.25. | −0.25
- app/content/courses/trees/l9-tiny-steps.json | screens[5] explain | note | "(limits-thm, Why sums look normal)" uses an internal id. | "(Distributions and Limit Theorems, Why sums look normal)"
- app/content/courses/trees/l9-tiny-steps.json | quiz q-real | note | £15.53 and £16.32 need 12% compounded continuously (annual 12% gives £14.99 and £15.76). The prose says only "grow 12% a year". | "12% a year, continuously compounded"
- app/content/courses/trees/l10-black-scholes.json | screens[8] prose | note | "(options, How the price responds)" uses an internal id. | "(Options and Payoffs, How the price responds)"
- app/content/courses/trees/l11-implied-vol.json | screens[2] prose | note | "Newton's method (taylor, Newton's method)" uses an internal id. | "(Series and Approximation, Newton's method)"
- app/content/courses/trees/l11-implied-vol.json | screens[7] smile table | note | The prices match the stated vols only at r = 5% (r = 0 gives 0.53, 1.45, 4.19 ...). The prose gives no rate or dividend yield. | Add "r = 5%, no dividends".
- app/content/courses/trees/l11-implied-vol.json | quiz q-otm explain | warning | "At the 200 strike vega is about 0.3 per unit of σ" is wrong. Black-Scholes vega there is 0.55 at 21.2% and 0.95 at 22.6%; the 1p move over 1.4 vol points is a slope of 0.7. | "about 0.7"
- app/content/courses/trees/l12-delta-hedging.json | screens[4] | note | The 3,000-path figures give no seed, generator or real-world drift, so they cannot be reproduced. The figures are unhedged 15.21, then 5.87, 2.82, 1.53, 0.76 and 0.40. My 40,000-path runs (μ = r) give 15.4, 5.9, 2.9, 1.5, 0.77 and 0.39, which agree. | State the seed and drift.
- app/content/courses/trees/l12-delta-hedging.json | screens[6] explain | note | "it returns £-1.19" puts the sign in the wrong place. | "−£1.19"
- app/content/courses/trees/l12-delta-hedging.json | screens[9] | warning | The day counts disagree, and neither is stated. Here theta "earns the book £25.45" overnight, which is 1,000 × 6.414/252, a 252-trading-day year. l10 screens[8] gives theta per day as "about −£0.018", which is 6.414/365. | State "per trading day (252 a year)" here and "per calendar day" in l10, or use one convention.
- app/content/courses/trees/l12-delta-hedging.json | quiz q-zero | warning | "A share had zero volatility ... the hedging error is zero" contradicts screens[7]. There, a share that never moves gives the seller, hedged at 20% vol, +£7.97. The claim holds only if the hedge also uses σ = 0. | "...and you price and hedge with σ = 0"
- app/content/courses/trees/review-2.json | r-crr-q explain | note | The working is inconsistent: 1.0905 − 0.9170 is 0.1735, not 0.1734, and 0.0863/0.1734 = 0.4977. The answer 0.4976 comes from unrounded inputs. | "q = 0.08634/0.17351 = 0.4976"
- app/content/courses/trees/review-3.json | r-freq option 1800 | warning | The why says "You cubed the factor", but 20 × 3.06³ = 573. 1,800 is about 20 × 3.06⁴. | Value "about 570" with that why, or why "You raised the factor to the fourth power".
- app/content/courses/trees/homework-1.json | h-digital-100 canvas | error | The branch labels read ×1.2 and ×0.8 on a £50 share that ends at £55 or £45. The factors are 1.1 and 0.9, which the explain uses. | ×1.1 and ×0.9
- app/content/courses/trees/homework-2.json | h-calibrate wrong one-step | note | It duplicates linear (both 128.4, same tolerance), so one-step never fires and has no byKey. | Drop it.
- app/content/courses/trees/homework-1.json items[8] model, homework-3.json items[2] explain, l12-delta-hedging.json screens[9] explain | maths | note | A bare £ sits inside maths ("£11.904762", "= £8.00", "= £938"). | `\text{£}` or move the £ outside the maths.
- app/content/courses/trees/homework-2.json items[1], items[4]; homework-3.json items[3] | explain | note | Four sentences each. | Trim to three.
- app/content/courses/trees/l8-python-pricer.json, l10-black-scholes.json, l12-delta-hedging.json, homework-1.json | widget.how | note | "math.isclose" is in prose without code formatting. l11 quiz[3] option 2 also uses "percent". | `math.isclose`; "per cent"
- app/content/courses/trees (12 sentences) | e.g. l11 screens[4] how (26 words), l12 summary.trap (25), homework-3 items[0] how (25) | note | These sentences are over 20 words. | Split them.

## micro

- app/content/courses/micro/l2-walking-the-book.json | quiz q-slip | note | The wrong ids level-gap and total have no byKey lines. | Add one line each.
- app/content/courses/micro/l4-market-or-limit.json | quiz q-urgent explain | note | It uses "the half-spread ... 2p a share, £40 in all", but the prose gives no spread. | Add the 4p spread to the prose.
- app/content/courses/micro/l6-impact.json | quiz q-walk wrong all-third (20.0333) | error | 20.0333 matches no slip. The slip its why names (weighting the third level by its full 1,000 shares) gives (10,000 + 10,010 + 20,050)/2,000 = £20.030, which is the correct answer, so the item cannot catch it. | Make the third level 800 shares (whole-level average £20.0278) and set all-third to that.
- app/content/courses/micro/l7-where-is-the-price.json | screens throughout | note | "Microprice" here is the size-weighted mid. Stoikov's micro-price is a different, model-based estimator. | One clause: "(also called the weighted mid)".
- app/content/courses/micro/l9-both-sides.json | screens[5] explain | note | "$2 \times 10 \times 0.067 = 1.35$": the product shown is 1.34 (exact 1.3476). | "$2 \times 10 \times 0.0674 = 1.35$"
- app/content/courses/micro/l9-both-sides.json, l10-inventory.json, l11-adverse-selection.json, l12-venues.json | objectives[1] and [2] | note | Objectives 2 and 3 have no final full stop. Objective 1 has one. | Add full stops.
- app/content/courses/micro/l10-inventory.json | screens[5] explain | note | "Inventory is a random walk and drifts to 18 lots", but the question uses the end value, 14. 18 is the peak (trade 84). | "drifts as far as 18 lots"
- app/content/courses/micro/l11-adverse-selection.json | screens[5] explain | note | It says l9 called the £100,000 day "before adverse selection". l9 screens[10] says "before exchange fees, technology and staff" and only promises the bigger cost. | "That is the bigger cost l9 promised after the £100,000 day."
- app/content/courses/micro/l12-venues.json | screens[2] explain | warning | "The 300-share surplus stays unfilled, filled by time priority among the buyers at the margin" contradicts itself. | "Buyers above 501p fill in full; the 500 shares bid at exactly 501p share the last 200 by time priority, and 300 stay unfilled."
- app/content/courses/micro/l12-venues.json | screens[8] prose, screens[10] row 4; homework-3.json h-pfof | warning | The UK course describes an internaliser "often paying brokers for the flow" and grades a "wholesaler that pays the broker" as normal. Payment for order flow is banned in the UK (FCA) and is being phased out in the EU; this is the US retail model. Screens[7] says UK and EU dark pools run "with caps on dark volume", but the UK removed the double volume cap. | Say "in the US" for payment for order flow. Say "in the EU, with caps on dark volume" for screens[7].
- app/content/courses/micro/l12-venues.json | screens[10] explain | note | Four sentences. | Merge two.
- app/content/courses/micro/l8-liquidity.json quiz q-flash, l12-venues.json quiz q-flash | quiz | note | Both quizzes test the 6 May 2010 flash crash with the same correct reading. | Replace one, e.g. with a closing-auction imbalance.
- app/content/courses/micro/review-1.json | r-marketable wrong market (300) | warning | The why says "You took the size of the bid at £19.99", which is 600. 300 is the size at £20.02. | Why "You took the size of the bid at £20.02."
- app/content/courses/micro/homework-1.json | h-bp | error | The wrong bid value is 32.2, but 0.04/12.46 × 10,000 = 32.10. Dividing by the bid is therefore graded correct (answer 32.1 ± 0.1), and its why never fires. Dividing by the ask gives 32.00, also accepted. | Ask for two decimal places: answer 32.05, tol 0.005, bid 32.10, ask 32.00.
- app/content/courses/micro/homework-1.json | h-sell-walk wrong all-levels (255) | warning | The slip in the why (selling all 1,200 at £250.30, i.e. 3,000 shares) gives £260. 255 matches no slip. | Value 260.
- app/content/courses/micro/homework-2.json | hw2-longform part (e) | note | The prompt gives day-2 sizes but no prices. The model assumes the mid is still £25.00 with a 2p spread. | Add "with bid £24.99 and ask £25.01".
- app/content/courses/micro/homework-3.json | h-best-s wrongs one-side and old-k | warning | Both are 29.43, so old-k never fires, and it has no byKey. A learner who keeps s = 2 in this λ gets 2 × 2 × 20e^{−0.5} = 48.52. | old-k = 48.52 with why "You kept s = 2 from k = 0.5; here s* = 4".
- app/content/courses/micro/l5-crossing-the-spread.json screens[1], [2], [3], [9] hints[2], quiz[1]; l6-impact.json screens[9], quiz[2]; review-2.json items[0], items[8]; homework-2.json items[3], items[8] model and rubric[8] | maths | note | A bare £ sits inside maths (e.g. "$100 \times £0.04 = £4.00$", "$= £360$", "$-£200$", "$£24.994$"). | `\text{£}` or move the amount outside the maths.
- app/content/courses/micro/l2-walking-the-book.json, l11-adverse-selection.json, homework-1.json | widget.how | note | "math.isclose" is in prose without code formatting. | `math.isclose`
- app/content/courses/micro (63 sentences) | e.g. l6 screens[4] prose (37 words), l12 screens[8] prose (36), homework-3 items[4] explain (33), l6 screens[11] explain (33), homework-1 items[2] explain (32), l12 screens[9] explain (32) | note | These sentences are over 20 words. Micro has the most in the topic. | Split them.

## exam (app/content/exams/topic-1.7.json)

- app/content/exams/topic-1.7.json | e-crr-q | warning | It is identical to trees/review-2 r-crr-q (σ = 30%, monthly steps, r = 4% continuous, q = 0.4976), so it tests recall. | New numbers, e.g. σ = 25%, weekly steps, r = 5%.
- app/content/exams/topic-1.7.json | whole exam | note | All 16 skills are mapped, and every exit line is tested (book, limit against market, parity derivation, Python tree pricer). Even so, tp-bs, fi-bonds, fi-equity, op-payoff and op-strategies get one item each. Gamma, vega and theta signs, implied vol, futures margin and the square-root impact model never appear. | Add one Greeks-sign item and one impact or margin item.
- app/content/exams/topic-1.7.json | items[20] and items[25] widget.how | note | "math.isclose" is in prose without code formatting. | `math.isclose`

## Automated checks (no finding)

- Reference values reproduced:
  - Black-Scholes £10.4506.
  - CRR 12.1623, 9.9705, 10.3267, 10.4194, 10.4428 and 10.4467 at n = 1, 4, 16, 64, 256 and 512.
  - Implied vol 0.241117 for £12.00, with Newton steps 0.2413 and 0.2411.
  - Two-step American put £7.99 against European £6.29; three-step American 8.904.
  - l7's four-step American 5.88 against European 5.09 (with e^{0.0125}).
- Code tests reproduced:
  - All trees and markets code tests: the l8 pricer, `hedge_pnl`, `exercise_nodes` (514), `margin_calls`, `irr`, `ytm` and `bond_price`.
  - l12's 20-step path hedge: P&L −1.19, cash −101.19 and the full delta series.
  - micro `expected_profit` (9 tests), `cost_vs_mid` (9), `estimate_cost` and `days_to_exit` (10), and `uncross` (9, against an independent implementation that includes both tie rules: smallest surplus, then lowest price).
  - micro `maker_pnl` (8 seeded tests, including 0.9988 for seed 1).
  - Exam `make_market` (8) and `put_prices` (8, against the independent numpy CRR pricer).
- micro l10's seed-3 inventory paths were reproduced exactly with `random.seed(3)`, a sale when u < 1/(1 + e^{−q}).
- Market-maker derivations hold:
  - π(s) = 2sλ₀e^{−ks} peaks at s* = 1/k.
  - Glosten-Milgrom gives E[V | buy] = V + αδ, with P(510 | buy) = 0.6, E = 502 and E[V | sell] = 498. The two-buy (503.85) and three-buy (505.43) posteriors check.
  - s* = αδ + 1/k in homework-3 checks.
  - Avellaneda-Stoikov's γ = Aσ²τ is stated correctly. Microprice = mid + I·s/2 is an identity.
  - The course makes no Kyle-model claims.
- Order-book arithmetic checks: every VWAP, bp slippage, implementation shortfall, Amihud ratio, days-to-exit figure, auction uncross price and volume. The auction examples have no ties.
- All exam numbers were recomputed, distractors included. They check apart from the findings above.
- The exam ramp runs 2 → 5 (6, 14, 5 and 3 items). The 16 exam skills are exactly the set the four courses use.
- All 13 longform rubrics sum to 10. There is no "!" outside LaTeX `\!` and no "$" used as currency; the DOLLAR hits are the words "US dollars" in the FX screens.
- The tolerance scan raised three flags, all reported above: trees homework-2 h-calibrate, micro homework-1 h-bp and micro homework-3 h-best-s.
- Rate conventions are stated wherever they matter:
  - Markets and options use annual compounding.
  - Trees uses 1 + r up to l5 and e^{rΔt} from l6 on. The handover is noted above, and l7 screens[7] is the one silent case.
  - The exam states its convention in each item.

## Coverage against the curriculum (Use, Add and Exit lines)

- Covered:
  - Shares and returns, bonds, interest and compounding, present value, NPV and IRR (markets l1–l8).
  - Forwards, cost of carry with dividends and FX, futures and margin, shorting and leverage (markets l9–l13).
  - Option payoffs, strategies, butterflies, covered calls, put-call parity, bounds and early exercise. Greeks: delta, gamma, vega and theta in options l12; rho in trees l10.
  - One-step replication, risk-neutral pricing, multi-step and American trees, calibration, CRR convergence, Black-Scholes, implied vol and delta hedging (trees).
  - Microstructure: the book, spread, market against limit orders, queues, impact, liquidity, market making, inventory, adverse selection, venues and auctions (micro).
- Exit lines:
  - The limit order book, spread and market against limit orders are covered in micro l1–l5 and the exam (e-sell-into-book, e-limit-breakeven).
  - Parity is derived in options l9 and the exam (e-parity-order).
  - The Python binomial pricer is built in trees l8 and the exam (e-code-put-pricer).
- Thin or missing against Hull and Varsity: interest-rate futures and hedging with futures beyond one basis screen; swaps; options on futures; dividend effects on option bounds and parity, which are stated as "no dividends" throughout options; and the Greeks of portfolios beyond delta (gamma or vega hedging appears only in prose).

## Fix pass

I recomputed every corrected number before writing it. Bond prices, CRR trees, Black-Scholes values, vega and theta came from Python, using the review's `crr.py` and closed-form checks. After the edits, `tolcheck.py` finds no answer or misconception overlap in any topic 1.7 file. `sentcount.py` finds no explanation over three sentences. A sentence scan that also breaks at display maths and skips derive captions finds no sentence over 20 words; the 38 hits left in the original `style.py` are derive formulas and display-maths artefacts. `node tools/validate.mjs`: 0 errors in topic 1.7 files (the 8 errors are all in fin-ml l4). All 62 touched files pass the playthrough (42 lessons, 19 sets and the exam).

Status: fixed 88, fixed in part 2, disputed 0, deferred 0. Where a fix differs from the proposal, the line says why.

### markets (20 fixed)

1. l1 q-simple-vs-compound `b-small`: fixed. The option now reads £200.00, and the why gives the 1% gap as simple interest over 20 years.
2. l2 s9: fixed, "The value is about a third below the headline" (679,516/1,000,000 = 0.68).
3. l4 s3: fixed, "We solve for it numerically, for example by Newton's method".
4. l5 s1 `coupons-only`: fixed, wording as proposed (five £4 coupons at 5% = 17.32).
5. l6 s2: fixed, £92.18 at 5.85% and £91.97 at 5.90% (92.1752, 91.9747). The yield stays 5.89% (5.8937%).
6. l6 s4: fixed, "In Limits and Derivatives you found...".
7. l6 s5: fixed, answer −7.58 (−7.584%).
8. l6 s8 `inverse`: fixed, value 0.0453 (4.33/95.67). The why is unchanged.
9. l6 s11: fixed, "about three points".
10. l8 s6: fixed with 0.75% a month. The answer is 9.38% (1.0075¹² − 1 = 0.09381), `times12` is 9% and `simple` is 0.0075. The series, marker, caption, hints and explain were updated.
11. l11 s7: fixed, the limit-down sentence is dropped.
12. l12 summary.ideas[2]: fixed, "a profit of $P_0 - C$", as the generalise screen has it.
13. l13 q-recover: fixed, "(Series and Approximation, lesson 12)".
14. l13 s5: fixed, "The interest is due either way, so it drags on both outcomes."
15. homework-2 h-bond-hold `five-year`: fixed, −0.0010 ((91.5753 + 4 − 95.6705)/95.6705 = −0.000995).
16. review-3 r-margin-loan `orig`: fixed, value 27,000 (18,000 + 0.3 × 30,000).
17. "percent": fixed, "per cent" in prose. The engine's `"format": "percent"` keyword is left unchanged. homework-2 now asks for the yield "as a percentage, to two decimal places".
18. `math.isclose`: fixed, in code formatting.
19. l6 s3 and s8: fixed, three sentences each.
20. Long sentences: fixed, split. Three of the cited examples were scan artefacts: l10 s0, l11 s6 and l12 s7 already break at bold text or display maths. A missing full stop after display maths was added in l1 s6.

### options (21 fixed)

21. l1 s10: fixed. The explain now says the cash is untouched "less the premium", and that apart from the premium the fund misses only the first £5.00.
22. l4 s10: fixed. The crash is to 80 in one month, without "as in 2008", so the answer is −9. `no-prem` is now −10 and `from-100` −19; `premium` stays −1. Hints, feedback and explain were updated ("9 months of premium").
23. l6: fixed, c + p in all seven places.
24. l6 q-strangle: fixed, "The cheaper bet needs a wider move."
25. l7 s8: fixed. A call spread scaled by one over its gap tends to a digital, and a butterfly scaled by one over the gap squared tends to a spike at £100.00. The first sentence now says the narrow tent is £1.00 high on a £2.00 base, because "tall, thin spike" was also wrong. h is not defined until s9, so the screen says "gap".
26. l7 s10: fixed, "turns such chances into risk-neutral probabilities", in three sentences.
27. l7 s5 option d: fixed, value £27.50 (35 − 7.50), with the why showing it.
28. l9: fixed, `\text{£}` in all five places.
29. l9 s2: fixed. The prose and the feedback now say a one-step tree gives the price, which you build in Pricing with Trees.
30. l9 s6: fixed, "a year's interest on £95.24" (0.05 × 95.24 = 4.76).
31. l9 s9: fixed, "from Markets and Instruments", in three sentences.
32. l10 s9 and s11: fixed, "A bet on staying put".
33. l11: fixed, "the last lesson" for l10 in four places, and "Pricing with Trees ... in Exercising early on a tree".
34. l11 s9: fixed, "Rates are 5% a year." (45 − 20/1.05⁴ = 28.55).
35. l12 s7 `inverse`: fixed, "It equals 1 − Δ only because r = 0 and S = K here."
36. l12 theta: fixed. The s8 prose, feedback.correct and summary.ideas[2] now state rates at 0, as on the lesson's curves.
37. review-2 r-short-strangle `centre`: fixed, wording as proposed.
38. review-2 r-cc-put: fixed, byKey lines for `premium`, `gap` and `diff`.
39. homework-2 h-long-spread: fixed with new numbers. The share is £80.00 and the view £84.00, with the cap at £88.00. Calls cost £4.80 and £1.60, so the spread costs £3.20, the cap is £8.00, maximum profit £4.80 and break-even £83.20. The crossover is £89.60. At £84.00 the call loses £0.80 and the spread makes £0.80. Rubric points are unchanged (10).
40. `math.isclose`: fixed.
41. Long sentences: fixed, split. Breaks were added before display formulas where needed.

### trees (26: 25 fixed, 1 fixed in part)

42. l2 s7: fixed, "as in Vectors and Matrices".
43. l2 q-call-13 `reverse`: fixed, wording as proposed.
44. l4 s7: fixed, Limits and Derivatives and Multivariable Calculus.
45. l5 q-new-tree `middle`: fixed, value 3.40 ((3.78 − 0.48 × 0.50)/1.0404). The byKey line names the slip.
46. l6 s3 feedback: fixed differently, "$0.10778/0.2004 = 0.5378$". The given u and d make u − d exactly 0.2004, so only the numerator needed more places (1.012578 − 0.9048).
47. l6 s3 prose: fixed, "From here, r is a continuously compounded rate".
48. l7: fixed. s7 now says each step grows cash by e^{rΔt}, as in the last lesson. The s5 generalise and summary.formula now divide by R, one step's growth of £1. The note gives 1 + r, or e^{rΔt} on a calibrated tree. s0 to s6 still use 1.05 a step, which is consistent with R.
49. l9 s2 table: fixed, −0.25 (10.2051 − 10.4506 = −0.2455).
50. l9 s5: fixed, "(Distributions and Limit Theorems, Why sums look normal)".
51. l9 q-real: fixed, "12% a year, continuously compounded" (£15.53 checked).
52. l10 s8: fixed, "(Options and Payoffs, How the price responds)".
53. l11 s2: fixed, "(Series and Approximation, Newton's method)".
54. l11 s7: fixed, "r = 5% and no dividends".
55. l11 q-otm: fixed, "about 0.7". Black-Scholes vega is 0.55 at 21.2%, 0.73 at 21.9% and 0.95 at 22.6%.
56. l12 s4: fixed in part. The prose now states the drift: each path drifts at the 5% risk-free rate. No seed is stated, because the generator and seed behind the 3,000-path figures are not recorded. The review's 40,000-path rerun with μ = r agrees to within sampling error.
57. l12 s6: fixed, "−£1.19".
58. l12 s9 and l10 s8: fixed. l12 now says "one trading day of theta (252 a year)" (1,000 × 6.414/252 = 25.45). l10 says "per calendar day" (6.414/365 = 0.0176).
59. l12 q-zero: fixed, "...and you price and hedge with σ = 0".
60. review-2 r-crr-q: fixed, "$e^{0.04/12} = 1.00334$, so $q = 0.08634/0.1735 = 0.4976$". The given u − d is exactly 0.1735.
61. review-3 r-freq `1800`: fixed with a new why, "You raised the factor to the fourth power: 20 × 3.06⁴ ≈ 1,750". The value is kept.
62. homework-1 h-digital-100: fixed, ×1.1 and ×0.9.
63. homework-2 h-calibrate: fixed, `one-step` dropped.
64. Bare £ in maths: fixed, `\text{£}`.
65. homework-2 items[1] and [4] and homework-3 items[3]: fixed, three sentences each.
66. `math.isclose` and "per cent": fixed.
67. Long sentences: fixed, split.

### micro (20 fixed)

68. l2 q-slip: fixed, byKey lines for `level-gap` (the 2p gap between the bid levels) and `total` (£12 on all 1,000 shares).
69. l4 q-urgent: fixed. The prose now gives the 4p spread (half-spread 2p × 2,000 = £40).
70. l6 q-walk: fixed as proposed. The third level is now 800 shares and `all-third` is 20.0278 (36,050/1,800), with tolerance 0.0005. The answer stays £20.030, and the explain says "500 of the 800".
71. l7: fixed, "the microprice, also called the weighted mid".
72. l9 s5: fixed, "2 × 10 × 0.0674 = 1.35".
73. l9 to l12 objectives: fixed, full stops added.
74. l10 s5: fixed, "drifts as far as 18 lots".
75. l11 s5: fixed, "the bigger cost promised in Quoting both sides, after the £100,000 day". The lesson is named rather than "l9".
76. l12 s2: fixed. 300 stay unfilled, bids above 501p fill in full, and the 500 shares bid at exactly 501p share the last 200 by time priority. It is split across two sentences to stay within 20 words and three sentences.
77. l12 venues: fixed. The internaliser line, the s10 row 4 and the s10 explain now say US, and the explain notes that UK rules ban payment for order flow. homework-3 h-pfof is now "A US retail app". The s7 option now reads "in the UK and EU they run under MiFID II rules. The EU also caps dark volume."
78. l12 s10 explain: fixed, three sentences.
79. Duplicate flash-crash quiz: fixed. l12 q-flash is replaced with q-imbalance, a closing-auction item: 900,000 to buy against 300,000 to sell at the indicative 2,000p. The answer is that publishing the imbalance draws in sellers. Each distractor names one slip: the excess is cancelled, the indicative price is final, or the order goes to a dark pool. l8 keeps the flash crash.
80. review-1 r-marketable `market`: fixed, "the bid at £20.02".
81. homework-1 h-bp: fixed as proposed. The item now asks for two decimal places: answer 32.05 with tolerance 0.005, `bid` 32.10. A new `ask` misconception at 32.00 has a byKey line (0.04/12.48 × 10⁴ = 32.051).
82. homework-1 h-sell-walk `all-levels`: fixed, 260 (3,000 shares at the mid less £751,030).
83. homework-2 hw2-longform (e): fixed, "the best bid is £24.99 for 2,000 shares and the best ask £25.01 for 8,000" (microprice £24.994 checked).
84. homework-3 h-best-s `old-k`: fixed, 48.52 (2 × 2 × 20e^{−0.5}), with a byKey line.
85. Bare £ in maths: fixed, `\text{£}` in every place listed.
86. `math.isclose`: fixed.
87. Long sentences: fixed, split. l4 quiz[1] was a scan artefact (a quoted sentence); it now reads as indirect speech.

### exam (3: 2 fixed, 1 fixed in part)

88. e-crr-q: fixed with σ = 25%, weekly steps and r = 5% continuous. u = 1.035277, d = 0.965925 and q = 0.5052. The wrong values are `annual-growth` 1.2306, `annual-simple` 1.2123 and `no-growth` 0.4913; the byKey lines point out that the first two give a q above 1.
89. Whole exam: fixed in part. I added e-greek-signs (difficulty 3, signs of a short put at r = 0) and e-split-impact (difficulty 4). The impact item uses the square-root model: £6m against £24m a day at 2% vol saves £40,000 over nine days, £60,000 against £20,000. The exam now has 30 items at 6/15/6/3, which is the 8.4 ramp. Implied vol and futures margin still have no exam item; the exam is at its 30-item ceiling.
90. Items[20] and [25] how: fixed, `math.isclose`.

Course files were out of scope for this pass, and none needs a change for these fixes.
