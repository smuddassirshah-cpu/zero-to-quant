# Claim ledger: pairs-rep levels 1 to 3 (concept audit, 6 November 2026)

Course `pairs-rep` (topic 3.1), files under `app/content/courses/pairs-rep/`. One row per definition, result, method step, convention, always/never/only claim, interpretation, causal claim, code-behaviour claim, and the reasoning in each `explain`, `why`, hint and feedback line. Pure arithmetic rows (a number divided by another) are covered by the three numbers scripts and are listed only where the reasoning carries a concept.

Sources. GGR = Gatev, Goetzmann and Rouwenhorst, "Pairs Trading: Performance of a Relative-Value Arbitrage Rule", *Review of Financial Studies* 19(3), 2006, 797 to 827: §2.1 pairs formation (p. 802), §2.2 trading (pp. 802 to 803), §2.4 excess return computation (pp. 805 to 806), Table 1 (p. 807), §4 risk and factor regressions, §5 sub-periods and the common factor, abstract. The published text could not be fetched in this session (every paper host is outside the allowed network), so GGR citations are from the auditor's reading of the published version; the fixer should confirm page numbers. DF = Do and Faff, "Does Simple Pairs Trading Still Work?", *Financial Analysts Journal* 66(4), 2010. JT = Jegadeesh and Titman (1993), *Journal of Finance* 48(1). Hamilton = *Time Series Analysis*, ch. 19. MacKinnon (2010), QED working paper 1227 (critical values used by `statsmodels.coint`). NW = Newey and West (1987); HH = Hansen and Hodrick (1980). LdP = Lopez de Prado, *Advances in Financial Machine Learning* (2018), ch. 7 and 11. Vidyamurthy = *Pairs Trading: Quantitative Methods and Analysis* (2004), ch. 5 to 6. Roll (1984), *Journal of Finance* 39(4) (bid-ask bounce). CB = Casella and Berger, *Statistical Inference*, §8.3.4 (p-values). `sim:` rows name a check in `docs/reports/pairs-rep-L<n>-concepts.py`.

Verdicts: correct, wrong, imprecise, misleading, unverified.

## Level 1

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l1-ggr-design | screens[0].prose, options[0] | A pairs desk buys the laggard and sells the leader and waits for convergence | correct | GGR §2.2 p. 803: long the lower-priced, short the higher-priced normalised stock, unwind at the crossing |
| l1-ggr-design | screens[0].options[1].why | Buying the leader is a bet on the gap widening, momentum, the opposite trade | correct | definition; JT (1993) momentum is long the winner |
| l1-ggr-design | screens[0].options[2].why | Buying both is a market bet, not a gap bet | correct | long-long has market exposure 2, no spread exposure |
| l1-ggr-design | screens[0].options[3].why | Once the gap has closed the profit is gone | correct | the payoff is the change in the spread from open to close |
| l1-ggr-design | screens[0].explain.text | Owning A and owing B gains when the gap shrinks whatever the market does | correct | £1 long minus £1 short cancels a common move; sim: L3:l13 screens[2] |
| l1-ggr-design | screens[1].prose | GGR form pairs over 12 months and trade over the next 6; a new portfolio starts every month | correct | GGR §2.1 and §2.2 pp. 802 to 803; abstract |
| l1-ggr-design | screens[1].prose | A month is 21 trading days | correct | convention stated (252 / 12) |
| l1-ggr-design | screens[1].explain.text | 126 / 21 = 6, so six portfolios are live from the sixth month on | correct | sim: L1:l1 calendar |
| l1-ggr-design | screens[1].explain.text | Momentum studies overlap their portfolios in the same way | correct | JT (1993) §II: overlapping K-month holding portfolios |
| l1-ggr-design | screens[1].feedback.byKey.* | Portfolio 6 trades from day 357 so day 360 is inside | correct | calendar arithmetic |
| l1-ggr-design | screens[2].prose | Paraphrase: total-return index set to 1 twelve months back; closest partner; top 20 and top 5 trade six months; open at two standard deviations | correct | GGR §2.1 p. 802 (cumulative total return index, matching partner, top 5 and 20, also pairs 101 to 120), §2.2 p. 803 (two historical standard deviations) |
| l1-ggr-design | screens[2].feedback.byKey.days-f, days-t | 252 and 126 are the periods in trading days, not months | correct | convention |
| l1-ggr-design | screens[2].explain.text | Formation 12 months, trading 6, open at 2 sd, portfolios of 20 or 5 | correct | GGR §2.1 to §2.2 |
| l1-ggr-design | screens[3].prose, slots | Formation rules: scale to 1, measure distance, keep 20 closest, measure spread sd; trading rules: open at 2 sd, close at crossing, close on the last day | correct | GGR §2.1 to §2.2; the sd is "as estimated during the pairs formation period" (p. 803) |
| l1-ggr-design | screens[3].feedback.byKey.t4 | The sd must be known before trading starts, so it comes from formation days | correct | GGR §2.2 p. 803; no look-ahead; sim: L1:l1/l5 trigger sd |
| l1-ggr-design | screens[3].explain.text | Everything that chooses or measures is fixed at the end of formation; that split keeps the backtest honest | correct | LdP ch. 7 (leakage) |
| l1-ggr-design | screens[4].widget | Half-open formation and trading ranges; live portfolios are the last K months | correct | code behaviour; sim: L1:l1 calendar; numbers script runs solution and starter |
| l1-ggr-design | screens[4].explain.text | `max(0, ...)` handles the first months before six portfolios exist | correct | code behaviour |
| l1-ggr-design | screens[5].prose, options[0] | The strategy may use only the formation-period sd on a trading day | correct | GGR §2.2 p. 803 |
| l1-ggr-design | screens[5].options[1].why, options[2].why | A trading-period or full-sample sd uses prices not yet seen: look-ahead | correct | LdP ch. 7 |
| l1-ggr-design | screens[5].explain.text | A threshold computed on trading prices sees the future and flatters the backtest; the paper fixes the sd at the end of formation | correct | GGR §2.2 p. 803 |
| l1-ggr-design | screens[6].prose, options[0] | A delisted share's pair is closed at the last price (or delisting return) | correct | GGR §2.2 p. 803: "we close the position in that pair, using the delisting return, or the last available price" |
| l1-ggr-design | screens[6].options[1].why | Dropping the pair hides a real outcome; the paper keeps every nominated pair | correct | GGR §2.2 p. 803; survivorship bias |
| l1-ggr-design | screens[6].options[2].why | A cash takeover is not a wipe-out; holders received the last price | correct | takeover mechanics; the paper uses the delisting return, which the lesson approximates by the last price |
| l1-ggr-design | screens[6].options[3].why | A replacement partner was never in the formation choice; it would be a new trade | correct | the formation step is closed before trading |
| l1-ggr-design | screens[6].explain.text | The seeded panel has no delistings so the rule never fires; a real replication must code it | correct | generator has no missing prices |
| l1-ggr-design | screens[7].prose | Formation [d, d+252), trading [d+252, d+378); 126 / 21 = 6 | correct | sim: L1:l1 screens[7] |
| l1-ggr-design | screens[8].explain.text | Six overlapping portfolios of 20 pairs give 120 pairs; a share can appear in several | correct | 6 x 20; overlapping portfolios draw from overlapping formation years |
| l1-ggr-design | summary.ideas[1] | Everything that chooses or measures, including the 2 sd trigger, is fixed at the end of formation | correct | GGR §2.2 p. 803 |
| l1-ggr-design | quiz[0] | Computing the sd from the six trading months is look-ahead | correct | as screens[5] |
| l1-ggr-design | quiz[0].options[1].why | The number of days is not the problem, their dates are | correct | 126 days suffice for an sd; the leak is temporal |
| l1-ggr-design | quiz[1] | Portfolios 0, 1, 2 trade in month 2 | correct | sim: L1:l1 quiz[1] |
| l1-ggr-design | quiz[2] | Closing at a crossing is the only trading-period rule among the four | correct | GGR §2.1 to §2.2 |
| l2-normalised-paths | screens[0].explain.text | Dividing by the first price makes a £10 and a £400 share comparable; the paper does this with each share's total-return index | correct | GGR §2.1 p. 802; sim: L1:l2 screens[0] |
| l2-normalised-paths | screens[0].feedback.byKey.pct | 10 is the percentage; as a scaled price it is 1.1 | correct | convention |
| l2-normalised-paths | screens[1].prose | Distance = sum of squared differences between the two normalised paths; GGR rank pairs by it | correct | GGR §2.1 p. 802 |
| l2-normalised-paths | screens[1].explain.text | Every day adds a squared gap so SSD only grows; small SSD means the paths stayed together | correct | non-negative summands |
| l2-normalised-paths | screens[2].feedback.byKey.unsq, absd | Summing unsquared gaps lets signs cancel; the paper squares, not absolute values | correct | GGR §2.1 p. 802; sim: L1:l2 screens[2] |
| l2-normalised-paths | screens[2].explain.text | Squaring stops cancellation and weights big gaps more | correct | convexity of the square |
| l2-normalised-paths | screens[3].prose, explain | The spread is A minus B; its formation sd uses `np.std` dividing by n | correct | convention stated by the course; GGR §2.2 says only "historical standard deviation"; sim: L1:l2 screens[3] |
| l2-normalised-paths | screens[3].widget.wrong[ddof1] | 0.0151 (dividing by n minus 1) is marked wrong | correct | right only because the item states the n convention; a reader of the paper could use either, and over 252 days the two differ by 0.2% |
| l2-normalised-paths | screens[3].feedback.byKey.rms | The root mean square of the spread is not its sd when the mean is not 0 | correct | definition |
| l2-normalised-paths | screens[4].explain.text | Dividing by `P[0]` broadcasts across columns; `float` turns a NumPy scalar into a plain number | correct | NumPy semantics; numbers script runs the code |
| l2-normalised-paths | screens[5].prose, explain | SSD_ij = G_ii + G_jj - 2 G_ij with G = P^T P; the diagonal is exactly 0 | correct | expand (p_i - p_j)^2; sim: L1:l2 screens[5]/[9] |
| l2-normalised-paths | screens[6].prose, options[0] | A dividend drops the price but not the total-return index; on prices a false divergence opens | correct | definition of a total-return index; GGR §2.1 use "price includes reinvested dividends"; sim: L1:l2 screens[6] |
| l2-normalised-paths | screens[6].options[1].why | Holders lost nothing: the 4% arrived as cash; the gap is an accounting artefact | correct | ex-dividend mechanics |
| l2-normalised-paths | screens[6].options[2].why | The sd is fine; the price series leaves out the cash paid | correct | the formation sd is unaffected by one trading-day drop |
| l2-normalised-paths | screens[6].explain.text | On prices a 4% drop is about two formation sds for a close pair | correct | 2 x 0.0210 = 0.042 against a 0.045 drop at level 1.12 |
| l2-normalised-paths | screens[7].options[0], explain | Identical paths give sd 0; the code must guard `sd > 0`; 0 / 0 is NaN and NaN > 2 is False | correct | NumPy semantics; sim: L1:l2 screens[7] |
| l2-normalised-paths | screens[7].options[1].why | A pair whose spread is always 0 never trades and earns 0 | correct | the trigger is never met |
| l2-normalised-paths | screens[8].prose, options[0], explain | Log returns exactly doubled give correlation 1 yet the levels drift apart; distance compares levels | correct | sim: L1:l2 screens[8] |
| l2-normalised-paths | screens[8].options[2].why | Distance and correlation can disagree completely | correct | the same construction |
| l2-normalised-paths | screens[8].explain.text | Cointegration's "Correlation is not cointegration" makes the same point | correct | Hamilton ch. 19 §19.1; Vidyamurthy ch. 5 |
| l2-normalised-paths | screens[9].widget | Derivation of the matrix identity; the distractor squares after summing | correct | algebra; sim: L1:l2 screens[5]/[9] |
| l2-normalised-paths | screens[10].options[0], explain | Distance assumes equal normalised prices, a hedge ratio of 1, so nothing is estimated beyond the spread sd | correct | GGR §2.1 to §2.2: $1 long, $1 short on the normalised series; Vidyamurthy ch. 5 contrasts the estimated ratio |
| l2-normalised-paths | screens[10].options[1].why | Distance uses levels, not correlations | correct | definition |
| l2-normalised-paths | screens[10].options[2].why | Distance can pick spurious pairs too; its gain is simplicity | correct | sim: L1:l3 screens[8] (chance pairs fill the top 20) |
| l2-normalised-paths | screens[10].options[3].why | Cointegration allows any hedge ratio and tests the spread; distance fixes 1 | correct | Hamilton ch. 19 (Engle-Granger); Vidyamurthy ch. 5 |
| l2-normalised-paths | summary.trap | Normalising prices instead of total returns makes a dividend look like a divergence | correct | as screens[6] |
| l2-normalised-paths | quiz[0].feedback.byKey.unsq | Gaps +0.1 and -0.1 cancel unless squared | correct | arithmetic with a concept |
| l2-normalised-paths | quiz[1].options[0], explain | Re-basing the trading period to its own first day puts spread and threshold on different bases and wipes out a gap open on day 0 | correct as a statement about the course's convention; see unverified row below | sim: L2:l2 quiz[1]; GGR §2.2 p. 803 opens on the formation-normalised series (Figure 1 continues one base) |
| l2-normalised-paths | quiz[1].options[1].why | Re-basing resets any open gap to 0 | correct | sim: L2:l2 quiz[1] |
| l2-normalised-paths | quiz[1].options[2].why | The first trading price is known on that day, so re-basing is not look-ahead | correct | timing |
| l2-normalised-paths | quiz[2] | Smaller SSD means the paths stayed closer | correct | definition |
| l3-closest-pairs | screens[0].prose | GGR measure the distance of every possible pair, then trade only the closest | correct | GGR §2.1 p. 802 ("exhaustive matching") |
| l3-closest-pairs | screens[0].feedback.byKey.* | 100 x 99 counts ordered pairs; 100^2 and 5,050 include self-pairs | correct | combinatorics |
| l3-closest-pairs | screens[1].explain.text | The gap between the 20th and 21st SSD hints the first 20 differ from the rest | correct | panel fact; planted pairs share a random walk |
| l3-closest-pairs | screens[2].prose | SSD(i, j) = SSD(j, i) | correct | symmetry |
| l3-closest-pairs | screens[3].prose | Stable sort keeps ties in order; return the k smallest | correct | NumPy semantics |
| l3-closest-pairs | screens[3].explain.text | The first year's top 20 are the 20 planted pairs sharing a random walk | correct | sim: L1:l3 screens[4].explain; numbers script |
| l3-closest-pairs | screens[4].prose | "In the main table each share takes one partner": the paper's rule is a greedy matching in which a share used once is skipped | wrong | GGR §2.1 p. 802 chooses for each stock the partner minimising SSD and then ranks the nominated pairs; nothing excludes a share that is the nearest partner of several others. On the screen's table the paper's rule keeps B-C then A-B; sim: L1:l3 screens[4] EXPECTED_FAIL |
| l3-closest-pairs | screens[4].options[1].why | "You took the two closest pairs overall. B already has a partner, so A-B is skipped" | wrong | A-B is A's nearest partner, so the paper's rule nominates it; the option marked wrong is the paper's answer |
| l3-closest-pairs | screens[4].options[3].why | Greedy order starts from the smallest SSD | correct | under the course's own greedy rule |
| l3-closest-pairs | screens[4].feedback.byKey.all | "That is our closest-overall rule, not the paper's" | wrong | as above |
| l3-closest-pairs | screens[4].explain.text | On the first formation year the two rules agree; in late years they do not | correct | sim: L1:l3 screens[4].explain (no share repeats in year 1) |
| l3-closest-pairs | screens[5].prose, widget | `one_partner_pairs` walks sorted pairs and skips used shares; `same_industry_share` | correct as code; the label "one-partner rule" is attributed to the paper on screens[4] and [6] | numbers script runs solution and starter |
| l3-closest-pairs | screens[5].explain.text | From day 1,512 the closest-overall list reuses shares; the industry share falls from 1.0 to 0.35 | correct | panel fact; numbers script |
| l3-closest-pairs | screens[6].explain.text | "The paper's one-partner rule would drop the repeats" | wrong | GGR §2.1: a share may be the nearest partner of two others and both pairs can rank in the top 20 |
| l3-closest-pairs | screens[7].options[0], explain | Among the 20 closest, rank barely predicts profit; close is necessary, not sufficient; the fifth closest never opened | correct | panel fact; sim: L1:l3 screens[7]; GGR Table 1 shows top 5 and top 20 both profitable without a monotone rank effect |
| l3-closest-pairs | screens[7].options[1].why | A pair that never drifts 2 sd apart never trades | correct | opening rule |
| l3-closest-pairs | screens[8].prose, explain | Two unrelated random walks can stay close for a year by luck; only 3 of 20 are planted at start 2,016 | correct | sim: L1:l3 screens[8]; Hamilton ch. 18 (spurious regression) |
| l3-closest-pairs | screens[8].explain.text | Cointegration's first lesson shows the same trap: unrelated walks that look related | correct | Granger and Newbold (1974) spurious regression |
| l3-closest-pairs | screens[9].prose | N(N-1)/2 pairs; keep the k smallest; with one partner per share skip pairs that reuse a share | correct as a description of the course's rule | combinatorics |
| l3-closest-pairs | screens[9].explain.text | The count grows with the square of the universe | correct | N(N-1)/2 |
| l3-closest-pairs | screens[10].prose | The paper's robustness check trades only same-industry pairs | correct | GGR §3 (Table 3, pairs matched within four industry groups) |
| l3-closest-pairs | screens[10].explain.text | Chance pairs ignore industries, one reason the paper checks same-industry pairs | correct | GGR §3 motivates the industry restriction by economic linkage |
| l3-closest-pairs | summary.ideas[1] | "The paper gives each share one partner; our course keeps the closest pairs overall" | imprecise | true that each stock nominates one partner (GGR §2.1), but the course reads it as exclusive matching; see screens[4] |
| l3-closest-pairs | quiz[1] | Under the one-partner rule (4, 9) then (7, 20) | correct under the course's greedy rule | the item does not attribute the rule to the paper |
| l3-closest-pairs | quiz[2].options[0], explain | The closest pair can earn 0 because its spread never passed 2 sd | correct | opening rule |
| l3-closest-pairs | quiz[2].options[2].why | A pair that never opens is far likelier at exactly 0 than one whose gains and losses cancel exactly | correct | a continuous payoff is 0 with probability 0 if it traded |
| l4-main-results | screens[0].prose | The paper's one dollar a side | correct | GGR §2.2 p. 803 and §2.4 p. 805 |
| l4-main-results | screens[0].explain.text | Return on committed capital divides the total payoff by every nominated pair, traded or not | correct | GGR §2.4 p. 805 |
| l4-main-results | screens[0].feedback.byKey.shares | Returns are per pair, not per share | correct | GGR §2.4: the pair is the unit |
| l4-main-results | screens[1].prose, explain | GGR report two returns: committed divides by all pairs, employed only by pairs that opened; fewer opened pairs make employed larger when the total is positive; equal when all open | correct | GGR §2.4 p. 805 (return on committed capital and on actual employed capital); sim: L1:l4 screens[8] |
| l4-main-results | screens[2].prose | The paper reports monthly figures; the course divides a six-month figure by 6 for now | correct | GGR Table 1 reports monthly excess returns; the course states its own convention |
| l4-main-results | screens[2].explain.text | The paper compounds daily returns within each month; level 2 lists it as a gap source | correct | GGR §2.4 pp. 805 to 806 (positions marked to market daily, daily returns compounded to monthly) |
| l4-main-results | screens[3].prose | Each pair is £1 long and £1 short, so the short sale pays for the long | correct as the paper's convention | GGR §2.4 p. 805 (zero-cost, self-financing payoffs) |
| l4-main-results | screens[3].options[0], explain | A self-financing position needs no cash, so its payoff is an excess return with nothing to beat but zero | correct | GGR §2.4 p. 805 calls the payoffs excess returns because the strategy is self-financing; sim: L1:l4 screens[3] (r_f cancels); the explain adds that margin and fees are real |
| l4-main-results | screens[3].options[1].why | Rates were far from zero in 1962 to 2002 | correct | GGR sample July 1962 to December 2002; T-bill rates 1 to 15% |
| l4-main-results | screens[3].options[2].why | Excess means over the risk-free rate, not over the market | correct | standard convention |
| l4-main-results | screens[3].options[3].why | The figures are before costs | correct | GGR Table 1 is gross; costs are discussed in §4.3 |
| l4-main-results | screens[4].prose, explain | Compound a monthly figure: 1.0075^12 - 1 = 9.38%; the paper reports annualised excess returns of up to 11% | correct | GGR abstract ("up to 11 percent"); sim: L1:l4 screens[4] |
| l4-main-results | screens[4].explain.text | The planted gap size was tuned so the result lands in that range | correct | honest statement of the seeded design |
| l4-main-results | screens[5].options[0], explain | An employed return on a zero-cost position is not comparable with a fund's return on capital | correct | denominators differ; GGR §2.4 call committed the conservative measure |
| l4-main-results | screens[5].options[2].why | Committed is smaller than employed here and still not a return on capital | correct | n < k; capital is not defined without margin |
| l4-main-results | screens[6].options[0], explain | With no opened pair employed is 0 / 0; report 0 by a stated rule and keep the cycle | correct as the course's convention | GGR do not state a rule; the course states its own |
| l4-main-results | screens[6].options[1].why | Dropping quiet cycles inflates the average | correct | selection on the outcome |
| l4-main-results | screens[6].options[2].why | 0 / 0 raises in Python and gives NaN in NumPy; NaN spoils every average | correct | language semantics |
| l4-main-results | screens[7].widget | `committed_and_employed` | correct | numbers script runs solution and starter |
| l4-main-results | screens[8].prose | R_committed = sum / k, R_employed = sum / n; employed at least as large when the total is positive | correct | sim: L1:l4 screens[8] |
| l4-main-results | screens[9].options | Capital, turnover and costs come first; the SSD of the closest pair and the journal do not change the profit | correct | practitioner judgement; GGR §4.3 on costs |
| l4-main-results | screens[9].explain.text | The paper reports that profits survive conservative cost estimates | correct | GGR abstract and §4.3 |
| l4-main-results | summary.ideas[1] | A £1-long, £1-short pair needs no cash, so its payoff is already an excess return | correct | GGR §2.4 p. 805 |
| l4-main-results | quiz[0] | Compound once; multiplying by 12 then compounding counts the year twelve times | correct | arithmetic with a concept |
| l4-main-results | quiz[2] | Employed is below committed only when the total is negative and some pairs never opened | correct | sim: L1:l4 quiz[2] |
| l5-plan | screens[0].prose, explain | A threshold measured on days 252 to 377 is look-ahead | correct | as l1 screens[5] |
| l5-plan | screens[1].prose, explain | The generator plants 20 pairs sharing a random walk; 17 stop co-moving on day 1,512; pairs 4, 7, 16 survive | correct | sim: L1:l5 screens[1].explain |
| l5-plan | screens[1].explain.text | That is our planted version of profits falling in the paper's later years | correct | GGR §5 reports lower profits in the later sub-period; DF (2010) |
| l5-plan | screens[2].prose, explain | Each close sits at the bid or the ask, half a per cent from the mid; a same-day trade on closes earns a bounce that is not real | correct | generator code; Roll (1984); sim: L1:l5 screens[7] |
| l5-plan | screens[3].prose, explain | phi = 0.5^(1/half_life) keeps 91.7% of the gap a day so half remains after 8 days | correct | AR(1) half-life; sim: L1:l5 screens[3] |
| l5-plan | screens[4].prose | Costs and the one-day wait each adjust finished trades, so either may come first | correct | both are post-processing of the trade list |
| l5-plan | screens[4].lines[p6] | Committed <= employed when the total payoff is positive | correct | sim: L1:l4 screens[8] |
| l5-plan | screens[5].explain.text | A comparison with NaN is False, so a NaN price fails the positive check | correct | IEEE 754; sim: L1:l5 screens[5] |
| l5-plan | screens[6].prose | A placebo trades pairs chosen at random; random pairs have no reason to converge | correct | control group; sim: L1:l5 quiz[0] |
| l5-plan | screens[6].explain.text | "Random pairs lose a little, because a pair that never reconverges is closed at a loss" | wrong | for martingale (random-walk) prices the expected payoff of a random pair is 0 by optional stopping, and a forced close can be a gain as easily as a loss; the panel's -1.00% and -1.13% are one cycle's draw. sim: L1:l5 screens[6] EXPECTED_FAIL (mean 0.0011, se 0.0038 over 150 fresh panels) |
| l5-plan | screens[7].options[0], explain | About 0.19 points a month of the same-day result is the bounce; mids have none | correct | 1.004 - 0.816; sim: L2:l9 screens[2] (closes beat mids on fresh panels) |
| l5-plan | screens[7].options[1].why | Size says nothing about the source | correct | logic |
| l5-plan | screens[7].options[2].why | The mid-price run still earns a profit; only the gap is bounce | correct | sim: L2:l9 |
| l5-plan | screens[7].options[3].why | The wait mostly removes a bounce nobody could capture; its real cost is a day of convergence | correct | GGR §2.2 p. 803 (one-day wait to avoid bid-ask bounce); sim: L2:l9 screens[3] and [7] |
| l5-plan | screens[7].explain.text | Even random pairs gain about 0.13 points a cycle from the bounce | correct | sim: L1:l5 screens[7] (closes minus mids positive on random pairs) |
| l5-plan | screens[8].options[0], explain | Keep the delisting step, flag it untested, test it on a planted delisting | correct | GGR §2.2 p. 803 delisting rule; software practice |
| l5-plan | screens[8].options[2].why | Deleting shares at random changes the data the results are reported on | correct | the panel is the fixed object |
| l5-plan | screens[9].prose | With 1 <= n <= k and total > 0, sum/k <= sum/n and employed / committed = k / n | correct | sim: L1:l5 screens[9] |
| l5-plan | screens[10].options | The first commit holds plan, targets and the seeded generator, not a tuned threshold or the results | correct | LdP ch. 11 (backtest overfitting); pre-registration logic |
| l5-plan | summary.ideas[1] | A placebo of random pairs and a run on mid prices separate skill from the bid-ask bounce | correct | sim: L1:l5 and L2:l9 |
| l5-plan | quiz[0].explain.text | A large placebo profit points at a bug or the bounce | correct | sim: L1:l5 quiz[0] |
| l5-plan | quiz[1].options[2].why | 126 days is enough for an sd; the dates are the problem | correct | as l1 quiz[0] |
| review-1 | items[0], items[1] | Calendar: trading starts at start + 252; six portfolios in month 9 | correct | sim: L1:l1 calendar |
| review-1 | items[2].feedback.byKey.* | Summing gaps without squaring, or absolute gaps, is not the SSD | correct | GGR §2.1 |
| review-1 | items[3] | sd dividing by n as `np.std` does; n - 1 gives 0.0245 | correct under the stated convention | as l2 screens[3] |
| review-1 | items[4].prose, options | "Under the paper's one-partner rule" (3, 8), (5, 9), (1, 2); (3, 5) is skipped because share 3 is used | wrong | the paper's rule (GGR §2.1) does not skip a share's second appearance; without the full SSD table the paper's answer is not determined, so the item is right only under the course's greedy rule, which it attributes to the paper |
| review-1 | items[5].options[0], explain | The fall in planted pairs comes from 17 pairs breaking on day 1,512; chance pairs of random walks fill the list | correct | generator; sim: L1:l3 screens[8] |
| review-1 | items[5].options[3].why | The panel has no other traders | correct | generator |
| review-1 | items[6] | Employed divides by opened pairs | correct | GGR §2.4 |
| review-1 | items[7].explain.text | 1.01^12 - 1 = 12.68%; the wait brings it to about 9.4% | correct | sim: L1 compounding |
| review-1 | items[8].explain.text | A shorter half-life means faster convergence, so more round trips per cycle | correct | AR(1) dynamics; sim: L3:l11 ("fast" panels trade more) |
| homework-1 | items[0].prose | "With one_partner=True use the paper's rule" | wrong | as l3 screens[4]; the code implements the greedy variant |
| homework-1 | items[0].explain.text | At starts 0 and 1,134 the two rules give the same 20 pairs because no share repeats | correct | numbers script; sim: L1:l3 screens[4].explain |
| homework-1 | items[1] | Spread stats: SSD, sd dividing by n, largest |spread| in sds; a pair whose spread never passed 2 sd in formation may still trade later | correct | numbers script; the trading period is a new sample |
| homework-1 | items[2].lines[s1] | Keep shares that traded every day of the formation year | correct | GGR §2.1 p. 802 screens out stocks with one or more days with no trade |
| homework-1 | items[2].lines[s2] | Build total-return indices so dividends do not look like divergences | correct | GGR §2.1 p. 802 |
| homework-1 | items[2].lines[s5] | "Rank the pairs and keep the k closest, one partner per share in the paper" | imprecise | each stock nominates one partner (GGR §2.1), but the course reads "one partner per share" as exclusive matching; see l3 screens[4] |
| homework-1 | items[2].lines[x1].why | Re-estimating the sd on the first month of trading is look-ahead | correct | GGR §2.2 p. 803 |
| homework-1 | items[3].model | Distance assumes equal normalised paths and a £1-for-£1 hedge, estimating only the spread sd; Engle-Granger assumes a stationary linear combination of log prices, estimates the hedge ratio and tests the residual | correct | GGR §2.1; Hamilton ch. 19 §19.2 (Engle-Granger two-step) |
| homework-1 | items[3].model | Close pairs are often cointegrated near ratio 1, but distance never tests stationarity; chance pairs enter; distance cannot pick a pair whose fair ratio is far from 1 | correct | sim: L3:l12 (selection bias; hedge ratio 2 invisible to distance) |
| homework-1 | items[3].model | A very quiet spread may never cross 2 formation sds; cointegration can choose a wide but stationary spread that trades often | correct | sim: L1:l3 screens[7]; homework-3 items[0] explain (Engle-Granger's wider spreads earn more at k = 5) |
| homework-1 | items[3].model | The panel knows the true pairs so selection can be checked; it has no delistings, dividends, short costs or real spreads; profits exist because they were planted | correct | generator |
| homework-1 | items[4].explain.text | Employed / committed = k / n, so 14.20 / 11.36 = 5 / 4 means 4 opened | correct | sim: L1:l5 screens[9] |
| homework-1 | items[5].explain.text | The annualised employed figure is a payoff per opened pair on a zero-cost position, not comparable with a fund's return on capital | correct | as l4 screens[5] |
| homework-1 | items[6].options | The log supports: selection found the planted pairs; 19 of 20 opened from the k/n ratio; the bounce lifts random pairs a little; it says nothing about real data or costs | correct | sim: L1:l5 screens[7] (bounce lifts random pairs); the -1.00 against -1.13 reading is the panel's own number |
| homework-1 | items[6].options[3].why | The panel plants the pairs; real data need not have them | correct | generator |
| l10-matching-results | screens[3].options[1] (listed here for the base question) | "We normalise once at formation start and carry it through trading" is a difference from the paper | unverified | GGR §2.2 p. 803 and Figure 1 continue the formation-normalised series into trading as the auditor reads them, which would make this a match, not a gap; the paper text could not be fetched to settle it. l2 quiz[1] treats re-basing as a mistake, so the course is inconsistent either way (finding 4) |
