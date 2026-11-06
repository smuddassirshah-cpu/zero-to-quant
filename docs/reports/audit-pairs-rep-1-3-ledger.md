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
| homework-1 | items[1] | Spread stats: SSD, sd dividing by n, largest absolute spread in sds; a pair whose spread never passed 2 sd in formation may still trade later | correct | numbers script; the trading period is a new sample |
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

## Level 2

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l6-two-standard-deviations | screens[0].prose, explain | The formation sd fixes the dashed lines at +-2 sd; GGR open a pair on the first day the spread moves beyond them | correct | GGR §2.2 p. 803 |
| l6-two-standard-deviations | screens[0].feedback.byKey.cross | Day 43 is the zero crossing, which closes the trade | correct | GGR §2.2: unwind at the next crossing |
| l6-two-standard-deviations | screens[1].prose | Cointegration's z-score thresholds are the same idea measured in formation sds | correct | Vidyamurthy ch. 6; the z-score is spread / sd |
| l6-two-standard-deviations | screens[1].explain.text | A wider trigger means fewer trades, each from a larger gap; the paper fixes 2 | correct | GGR §2.2; sim: L2:l6 quiz[2] |
| l6-two-standard-deviations | screens[2].options[0], explain | Buy the cheaper normalised price and sell the dearer: the opening rule | correct | GGR §2.2 p. 803; sim: L2:l6 screens[2] |
| l6-two-standard-deviations | screens[2].options[1].why | Buying the dearer share bets on the gap widening | correct | sign of the payoff; sim: L2:l6 screens[5] |
| l6-two-standard-deviations | screens[2].options[2].why | Selling both is a bet on the market falling | correct | net short exposure |
| l6-two-standard-deviations | screens[3].prose, explain | £1 buys 1/p units; equal pounds, unequal units; each leg's gain is units times price change | correct | GGR §2.4 p. 805 ($1 a side); sim: L2:l6 screens[3] |
| l6-two-standard-deviations | screens[4].explain.text | 1.5 sd earns most on this pair, but one pair in one cycle is not evidence for a lower trigger; choosing it on the same data overfits | correct | LdP ch. 11; sim: L3:l14 (winner's curse) |
| l6-two-standard-deviations | screens[5].prose, explain | The flipped trade earns minus the correct payoff; a sign error turns a profitable book into a loser | correct | sim: L2:l6 screens[5] |
| l6-two-standard-deviations | screens[6].options[0], explain | The opening rule is a level test, met on day 0; code that waits for a crossing from inside or starts on day 1 misses trades | correct as the course's reading of the rule | GGR §2.2 states a level ("diverge by more than two historical standard deviations"); sim: L2:l6 screens[6] |
| l6-two-standard-deviations | screens[6].options[2].why | Nothing in the rule excludes a day-0 open | correct | GGR §2.2 |
| l6-two-standard-deviations | screens[7].widget | `threshold`, `first_open` (level test with `sd > 0` guard), `units` | correct | numbers script runs solution and starter |
| l6-two-standard-deviations | screens[8].prose, explain | Open when the gap exceeds 2 sigma_form; +0.06 shorts i and buys j, -0.06 the reverse | correct | GGR §2.2 |
| l6-two-standard-deviations | screens[9].explain.text | Equal pounds on each side is the paper's rule, scaled up | correct | GGR §2.4 p. 805 |
| l6-two-standard-deviations | quiz[0].options[2].why | 2 x 0.018 = 0.036 and 0.040 is beyond it | correct | arithmetic with the rule |
| l6-two-standard-deviations | quiz[2].options[2].why | The rule is fixed in the paper, but the code can change it, with fewer trades | correct | sim: L2:l6 quiz[2] |
| l7-closing | screens[0].prose, explain | The paper closes a pair when the two normalised prices cross; the pair may then reopen | correct | GGR §2.2 p. 803 (unwind at the next crossing; a pair can open again) |
| l7-closing | screens[0].feedback.byKey.inside | Coming back inside 2 sd does not close; the paper waits for the crossing | correct | GGR §2.2 |
| l7-closing | screens[0].feedback.byKey.end | Day 125 is the forced close | correct | GGR §2.2 p. 803 (end of the trading interval) |
| l7-closing | screens[1].explain.text | Reopening lets a quiet pair earn several times; a crossing on the final day counts as a close | correct | GGR §2.2; sim: L2:l7 screens[1]/[3] |
| l7-closing | screens[2].prose, explain | A round trip pays the long leg's return minus the short leg's, £1 a side | correct | GGR §2.4; sim: L2:l7 screens[2] |
| l7-closing | screens[2].feedback.byKey.add | A short loses when its price rises | correct | definition |
| l7-closing | screens[3].explain.text | The side alternates as the spread swings from one band to the other | correct | panel fact; sim: L2:l7 screens[1]/[3] |
| l7-closing | screens[4].options[0], explain | A non-converging pair is booked at the last price, here a loss; most such losses come from pairs close only by chance | correct | GGR §2.2 p. 803; sim: L2:l7 screens[4]; sim: L3:l11 (broken pairs converge less) |
| l7-closing | screens[4].options[1].why | The position existed and lost money; the forced close books it | correct | accounting |
| l7-closing | screens[4].options[2].why | Each cycle ends its own positions on its last day | correct | GGR §2.2 |
| l7-closing | screens[5].prose | A 4 sd stop is not in the paper | correct | GGR describe no stop-loss |
| l7-closing | screens[5].options[0], explain | On the panel the stop costs money because a planted pair at 4 sd usually comes back; a stop is a risk choice, not a free gain | correct | sim: L2:l7 screens[5] (236 of 298 trades that reached 4 sd still crossed; the stop cuts cycle 1 to 10.68%) |
| l7-closing | screens[5].options[1].why | Cutting losses does not raise the average when it also cuts winners about to converge | correct | sim: L2:l7 screens[5] |
| l7-closing | screens[6].options[0], explain | Exiting when the spread re-enters the band books only part of the move and trades more often | correct | sim: L2:l7 screens[6] (0.1955 in 9 trips against 0.2218 in 4) |
| l7-closing | screens[6].options[2].why | It trades more often, so it pays more costs | correct | 9 trips against 4 |
| l7-closing | screens[7].prose, explain | With the wait a signal on day t opens on t + 1 and needs t + 1 < 125, so day 123 is the last signal; without the wait day 124 | correct | code convention; sim: L2:l7 screens[7] |
| l7-closing | screens[8].prose | With wait = 1 every open and close is done at the next day's price; scanning resumes the day after the exit | correct | GGR §2.2 p. 803 and Table 1 Panel B ("wait one day") delay both the opening and the closing signal |
| l7-closing | screens[8].widget | `trade_pair` and `holding_days` | correct | numbers script; sim: L2 trips reproduce the blotter |
| l7-closing | screens[9].options[0], explain | The rule has no stop, so an unconverged pair runs to the period's end; the note flags the open loss and the forced-close date | correct | GGR §2.2 |
| l7-closing | screens[9].options[1].why | Pairs do not always converge; the loss can be large | correct | sim: L3:l11 convergence share |
| l7-closing | quiz[1] | The paper closes at the next crossing or on the last trading day; no band exit, no stop | correct | GGR §2.2 p. 803 |
| l8-committed-capital | screens[0].explain.text | GGR report both committed and employed returns | correct | GGR §2.4 p. 805 and Table 1 |
| l8-committed-capital | screens[0].feedback.byKey.shares, legs | Returns are per pair, not per share or per leg | correct | GGR §2.4 |
| l8-committed-capital | screens[1].explain.text | Returns are high before cycle 60 and lower after, which level 3 explains | correct | panel fact (the break at day 1,512) |
| l8-committed-capital | screens[2].explain.text | The gap between committed and employed is larger for the top 5 because one of five never opened | correct | k / n = 5 / 4 against 20 / 19 |
| l8-committed-capital | screens[3].prose | The paper marks every pair to market daily, compounds within each calendar month, and averages the six live portfolios | correct | GGR §2.4 pp. 805 to 806 (daily marking to market, returns compounded to monthly; six overlapping portfolios whose returns are averaged) |
| l8-committed-capital | screens[3].options[0], explain | Dividing a cycle's payoff by 6 spreads it evenly; the paper books it in the months earned and compounds; a known gap source | correct | GGR §2.4 |
| l8-committed-capital | screens[3].options[1].why | The paper never divides by six; it measures each calendar month | correct | GGR Table 1 (monthly) |
| l8-committed-capital | screens[4].prose | Adjacent cycles share five of six trading months, so their returns are correlated; Newey-West with 5 lags allows for it | correct | overlapping six-month windows at monthly starts are MA(5); HH (1980), NW (1987); sim: L2:l8 screens[4] |
| l8-committed-capital | screens[4].options[0], explain | Overlapping cycles are not independent, so there is less information than 127 points suggest; the naive standard error is too small | correct | sim: L2:l8 screens[4] (naive t sd 2.57 under the null, NW(5) 1.33) |
| l8-committed-capital | screens[4].options[1].why | Newey-West changes the standard error, not the mean | correct | NW (1987); sim: L2:l8 screens[4] byKey.bias |
| l8-committed-capital | screens[4].options[2].why | The correction depends on the correlation; it does not always halve t | correct | NW formula |
| l8-committed-capital | screens[4].explain.text | Replicating Momentum's overlapping-returns correction is the same | correct | JT (1993) use the same overlap; HH (1980) |
| l8-committed-capital | screens[5].explain.text | The denominator is pairs; dividing by shares halves it, by legs counts the cycle as one pair | correct | GGR §2.4 |
| l8-committed-capital | screens[6].options[0], explain | When every pair opens committed equals employed; 46 of 127 cycles for the top 20 | correct | n = k; numbers script |
| l8-committed-capital | screens[6].options[1].why | Employed is larger only when some pair stays shut | correct | n < k |
| l8-committed-capital | screens[7].prose | The cycle is normalised once at `start` and the trading period keeps that base | correct as the course's convention | see the unverified row on the paper's base |
| l8-committed-capital | screens[7], screens[8].widget | `cycle_return`, `run`, `monthly` | correct | numbers script runs solution and starter |
| l8-committed-capital | screens[8].explain.text | One cycle in six is a fair sample, not the full result; its mean sits near the full run's | correct | 1.05% against 1.00%; sampling |
| l8-committed-capital | screens[9].explain.text | £904,000 a cycle on £20m long and £20m short; the capital needed depends on margin rules | correct | GGR §2.4 note that in practice capital is tied up as margin |
| l8-committed-capital | summary.ideas[2] | Adjacent cycles overlap by five months in six, so a naive t statistic overstates the evidence | correct | sim: L2:l8 screens[4] |
| l8-committed-capital | quiz[1].options[2].why | Overlap leaves the mean unbiased | correct | sim: L2:l8 screens[4] byKey.bias |
| l9-bid-ask-bounce | screens[0].prose, explain | A close printed at the bid; a real buyer pays the ask; a backtest buying at the printed bid pays 1% less, the full spread | correct | market microstructure; sim: L2:l9 screens[0] |
| l9-bid-ask-bounce | screens[0].feedback.byKey.mid | The mid is a reference price; nobody trades at it by crossing | correct | definition |
| l9-bid-ask-bounce | screens[1].explain.text | The extra day-to-day noise on closes is the bid-ask bounce: a close at the bid looks cheap, then bounces back; a same-day trade on closes buys that bounce | correct | Roll (1984); sim: L2:l9 screens[2] |
| l9-bid-ask-bounce | screens[2].prose | GGR worry that same-day returns include the bounce | correct | GGR §2.2 p. 803 and §4.3 (the one-day wait as a conservative check against bid-ask bounce) |
| l9-bid-ask-bounce | screens[2].explain.text | Closes minus mids is bounce; the wait removes it and also gives up a day of each move | correct | sim: L2:l9 screens[2], [3], [7] |
| l9-bid-ask-bounce | screens[3].prose | The paper's wait-one-day rule opens and closes each trade a day after the signal, at that day's close | correct | GGR §2.2 p. 803, Table 1 Panel B |
| l9-bid-ask-bounce | screens[3].options[0], explain | Tomorrow's close is at the bid or the ask independently of today's, so the trade no longer buys today's bounce; the wait is conservative | correct in the panel's model (a fresh coin each day) and as GGR's rationale | generator; GGR §2.2; sim: L2:l9 screens[3] |
| l9-bid-ask-bounce | screens[3].options[1].why | The wait still trades at a close, a day later | correct | GGR §2.2 |
| l9-bid-ask-bounce | screens[3].options[2].why | The wait does not add costs; it changes which price is used | correct | definition |
| l9-bid-ask-bounce | screens[4].prose, explain | Each round trip is four trades of £1; cost per pair per cycle = 4 c x round trips | correct | each leg opens and closes once; sim: L2:l9 screens[4]/[5] |
| l9-bid-ask-bounce | screens[5].prose, explain | Break-even c* = gross / (4 x trips); the paper reports that profits survive conservative cost estimates | correct | algebra; GGR abstract and §4.3 |
| l9-bid-ask-bounce | screens[6].options[0], explain | Charging the cost once per pair overstates the break-even about sevenfold; the cost count matters as much as the level | correct | sim: L2:l9 screens[6] |
| l9-bid-ask-bounce | screens[6].options[1].why | "Every buy and every sell pays the spread and commission" | imprecise | each trade pays half the quoted spread (the course's own screens[9] says so); a round trip pays the full spread. A learner carries away a doubled cost |
| l9-bid-ask-bounce | screens[6].options[2].why | Using the close as the fill price is the bounce itself, not a cost model | correct | as screens[1] |
| l9-bid-ask-bounce | screens[6].feedback.byKey.right | A pair trades about 6.8 times a cycle and each trade pays | correct | 4 x 1.69 |
| l9-bid-ask-bounce | screens[7].prose, explain | On mids the wait costs only the day of convergence; on closes it also removes the bounce; the two parts roughly add | correct | sim: L2:l9 screens[7] and [3] |
| l9-bid-ask-bounce | screens[8].widget | `bounce_effect`, `net_of_costs`, `breakeven_cost` | correct | numbers script |
| l9-bid-ask-bounce | screens[8].explain.text | On 22 cycles the wait run sits slightly above the mid run, on 127 slightly below; a sample of 22 moves the second decimal | correct | numbers script; sampling |
| l9-bid-ask-bounce | screens[9].options[0], explain | The wait addresses the bounce, a spread effect; commission, the half-spread on each real fill and the borrow fee must be charged separately | correct | GGR §2.2 and §4.3 |
| l9-bid-ask-bounce | screens[9].options[2].why | The borrow fee depends on how long the short is held, not on the fill price | correct | securities lending convention (fee accrues daily) |
| l9-bid-ask-bounce | summary.ideas[2] | Break-even cost = gross / (4 x trips) | correct | sim: L2:l9 |
| l9-bid-ask-bounce | quiz[1].options[0], explain | A close at the bid makes a share look cheap; buying it books the rebound to the mid | correct | Roll (1984) |
| l9-bid-ask-bounce | quiz[1].options[1].why | Closes and mids share the same mid path; only the bounce differs | correct | generator |
| l10-matching-results | screens[0].prose, table | GGR report annualised excess returns of up to 11%; profits survive conservative cost estimates; waiting a day cuts returns but leaves them positive; profits were lower in later years | correct | GGR abstract; Table 1 Panel B (one-day wait); §5 sub-periods |
| l10-matching-results | screens[0].options[0], explain | Lead with top 20, committed, with the wait: conservative on capital and on the bounce | correct | GGR §2.4 call committed the conservative measure; the wait is their conservative fill |
| l10-matching-results | screens[0].options[3].why | Choosing the cell by closeness to the target is matching, not checking | correct | LdP ch. 11 |
| l10-matching-results | screens[1].explain.text | Each gap needs a reason, not a tweak | correct | replication practice |
| l10-matching-results | screens[2].options[0], explain | On a panel tuned to the paper's range a match checks the code, not the strategy or the paper | correct | the profit was planted |
| l10-matching-results | screens[3].options[0] | Our monthly figure is a cycle's return over 6, not a daily compounded calendar month | correct | GGR §2.4 |
| l10-matching-results | screens[3].options[1] | We normalise once at formation start and carry it through trading, a difference from the paper | unverified | see the Level 1 row; GGR §2.2 and Figure 1 continue one base as the auditor reads them. Either this option or l2 quiz[1] misstates the paper (finding 4) |
| l10-matching-results | screens[3].options[2] | "No delistings, no dividends and no industry restriction" is a difference from the paper | imprecise | the paper's main table (Table 1) is unrestricted; the within-industry results are a separate robustness table (§3). No delistings and no dividends are data differences, not method differences, and the course's own l3 screens[10] calls the industry restriction a robustness check |
| l10-matching-results | screens[3].options[3] | A universe of 100 shares, not thousands | correct | GGR use all liquid CRSP stocks |
| l10-matching-results | screens[3].options[4].why, [5].why | The seed is not a design difference; 2 sd is the paper's own rule | correct | GGR §2.2 |
| l10-matching-results | screens[4].explain.text | Sampling one cycle in six moves the second decimal, so quote the full run | correct | sampling |
| l10-matching-results | screens[5].options[0], explain | Settings tuned to hit the target prove nothing; run the stated rules and explain the gap; test other settings only out of sample | correct | LdP ch. 11 |
| l10-matching-results | screens[5].options[2].why | Reporting the best of several tries hides how many were tried | correct | multiple testing |
| l10-matching-results | screens[6].options[0], explain | Report our ordering as ours without claiming the paper's; after the break the three unbroken pairs usually sit in the top 5 | correct | the course quotes only five paper facts; panel fact |
| l10-matching-results | screens[7].widget | `results_table` | correct | numbers script |
| l10-matching-results | screens[8].prose | gap = ours - paper; R_year = (1 + R_month)^12 - 1 | correct | definitions |
| l10-matching-results | screens[9].options[0], explain | Lead with the conservative cell and every condition: data, wait, costs | correct | reporting practice |
| l10-matching-results | screens[9].options[2].why | Matching one range on data we built is not an exact replication | correct | logic |
| l10-matching-results | quiz[0].explain.text | Committed counts idle pairs and the wait removes the bounce: the hardest cell to flatter | correct | GGR §2.4 |
| review-2 | items[0] | A negative spread means i is cheaper: buy i, sell j; 0.032 > 0.030 | correct | GGR §2.2 |
| review-2 | items[2].feedback.byKey.* | A short gains when its price falls; flipping the sign is the mirror trade | correct | sim: L2:l6 screens[5] |
| review-2 | items[3].options[0], explain | Closing when the spread re-enters the band books part of each convergence, earns less and trades more | correct | sim: L2:l7 screens[6] |
| review-2 | items[3].options[1].why | On pair (2, 3) the band exit earns 0.1955 against 0.2218 | correct | sim: L2:l7 screens[6] |
| review-2 | items[5].options[0], explain | Quote the Newey-West t: overlapping cycles are correlated and the naive t overstates the evidence | correct | sim: L2:l8 screens[4] |
| review-2 | items[5].options[2].why | t statistics apply to returns, with the overlap correction | correct | NW (1987) |
| review-2 | items[6], items[7] | Break-even = gross / (4 x trips); bounce = closes minus mids | correct | sim: L2:l9 |
| review-2 | items[8].options[0], explain | Check the code, list the known gap sources, report the gap; tuning to the target makes the match meaningless | correct | LdP ch. 11 |
| homework-2 | items[0].explain.text | The four cells: 1.37%, 1.01%, 1.00%, 0.75%; the wait lowers both portfolios | correct | numbers script; sim: L2:l9 (the wait lowers planted-pair payoffs) |
| homework-2 | items[1].prose, widget | Blotter: open beyond 2 formation sds, close at the first sign change or the last day, resume after the exit, fill a day late with the wait | correct | GGR §2.2; numbers script |
| homework-2 | items[2].lines | Trigger fixed in formation, signal, fill (a day late with the wait), hold to the sign change or last day, close and book long minus short; the band exit is the distractor | correct | GGR §2.2 |
| homework-2 | items[3].model | The bounce: closes at bid or ask, a same-day fill books a rebound nobody could buy; the wait fills at a fresh close; two effects (bounce and a lost day of convergence); the same-day figure overstates what a trader could earn | correct | GGR §2.2; sim: L2:l9 |
| homework-2 | items[3].model | The paper reports that waiting a day cuts returns materially but leaves them positive | correct | GGR Table 1 Panel B |
| homework-2 | items[4].explain.text | Costs per pair per cycle = 4 x c x trips; net = gross minus that, over 6 for a month | correct | sim: L2 homework-2 items[4] |
| homework-2 | items[6].options[0] | Dividing by 6 instead of compounding daily returns within each month changes the figure on the same trades | correct | GGR §2.4 |
| homework-2 | items[6].options[1].why | The normalisation base cancels in p_out / p_in on the same trades; it changes which trades open | correct | sim: L2 homework-2 items[6] |
| homework-2 | items[6].options[2].why | The seed picks the data; on the paper's own trades it plays no part | correct | logic |

## Level 3

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l11-why-profits-fell | screens[0].options, explain | The 12-cycle mean drops at the break and never regains its level; the dip of the straddling cycles is not a recovery | correct | panel fact (series in the file) |
| l11-why-profits-fell | screens[1].prose | GGR report lower profits in the later years of their sample | correct | GGR §5 (sub-period results: lower excess returns in the later period); DF (2010) |
| l11-why-profits-fell | screens[1].prose, explain | Before = cycles whose trading ends by day 1,512; after = cycles starting trading on it or later; straddling cycles are left out of both | correct | clean split; sim: L1/L3 calendar |
| l11-why-profits-fell | screens[1].explain.text | Survived = after / before; less than half survived | correct | definition; sim: L3:l11 screens[1]/[9] |
| l11-why-profits-fell | screens[1].feedback.byKey.* | Share lost against share survived; points against a ratio | correct | definitions |
| l11-why-profits-fell | screens[2].prose, explain | After 17 planted pairs break, chance pairs (random walks that tracked each other by luck) fill the top 20; the method still picks the closest 20 | correct | sim: L1:l3 screens[8] |
| l11-why-profits-fell | screens[3].prose, explain | A trade ends at a crossing or at the forced close; after the break only 54% of trades cross against 77% before; chance pairs open as readily but often never come back | correct | sim: L3:l11 (broken pairs converge far less often than planted ones) |
| l11-why-profits-fell | screens[4].options[0], explain | With fewer breaks the fall is smaller; the decline scales with how many pairs broke | correct | numbers script (break_frac 0.3 panel); mechanism |
| l11-why-profits-fell | screens[4].options[1].why | The fall comes from the pairs that broke, not from the years | correct | generator |
| l11-why-profits-fell | screens[5].options[0], explain | Crowding would close gaps sooner but leave convergence intact; broken pairs cut the convergence share; the share tells the stories apart | correct | DF (2010) attribute the decline to a worsening of arbitrage risk (pairs that diverge and do not converge) rather than to crowding; sim: L3:l11 (faster reversion keeps the crossing share, broken pairs cut it) |
| l11-why-profits-fell | screens[5].options[1].why | Both stories predict a fall in returns, so the fall cannot choose | correct | logic |
| l11-why-profits-fell | screens[5].options[2].why | The market barely moves a long-short pair under either story | correct | sim: L3:l13 screens[2] |
| l11-why-profits-fell | screens[5].options[3].why | A wider 20th-closest distance says fewer close pairs exist, not why trades fail | correct | logic |
| l11-why-profits-fell | screens[5].explain.text | "Do and Faff (2010) trace the continued decline to fewer pairs converging" | correct | DF (2010) §"Why has profitability declined?": the decline reflects worsening arbitrage risk, measured by the share of pairs that diverge without converging |
| l11-why-profits-fell | screens[6].explain.text | The rule still works on pairs that co-move; there are fewer of them | correct | panel decomposition; sim: L3:l11 |
| l11-why-profits-fell | screens[7].widget | `planted_in_top`, `split_means` (before: start + 378 <= break; after: start + 252 >= break) | correct | numbers script |
| l11-why-profits-fell | screens[7].explain.text | A cycle that straddles the break belongs to neither half, so it cannot blur the comparison | correct | definition of the split |
| l11-why-profits-fell | screens[8].explain.text | The convergence share is per trade, so a pair that opens three times counts three times | correct | definition stated |
| l11-why-profits-fell | screens[9].prose | survived = r_after / r_before; c = crossings / trades opened; a fall in c says pairs stopped co-moving, not that gaps closed faster | correct | sim: L3:l11 |
| l11-why-profits-fell | screens[9].explain.text | Waiting a day lowers both halves by a similar share | correct | 42% against 42%; panel fact |
| l11-why-profits-fell | screens[10].options[0], explain | A steady trade count with fewer crossings is the pattern of broken pairs; test each pair and retire those that drift | correct | sim: L3:l11 |
| l11-why-profits-fell | screens[10].options[1].why | Broken pairs fail at any threshold | correct | a random-walk spread has no level to revert to |
| l11-why-profits-fell | screens[10].options[2].why | Crowding predicts gaps that close sooner, not trades that stop closing | correct | DF (2010) |
| l11-why-profits-fell | quiz[1].options[2].why | A drop from 77% to 54% over 2,000 trades is far outside chance variation | correct | binomial se about 1.5 points |
| l11-why-profits-fell | quiz[2].feedback.byKey.pairs | The share counts trades, not pairs | correct | definition |
| l12-cointegration-selection | screens[0].prose, explain | The two rules measure different things: a planted pair ranks 2nd by distance with p = 0.2955; a chance pair ranks 23rd with p = 0.0009 | correct | numbers script; sim: L3:l12 (power about 70%, selection bias among close chance pairs) |
| l12-cointegration-selection | screens[0].options[1].why | Engle-Granger asks whether a weighted gap reverts; closeness is the distance test | correct | Hamilton ch. 19 §19.2 |
| l12-cointegration-selection | screens[1].prose | Cointegration selection runs Engle-Granger on each candidate's formation log prices and keeps the lowest p-values | correct as the course's definition | Vidyamurthy ch. 5 to 6 describes the cointegration approach; the ranking by p-value is the course's rule |
| l12-cointegration-selection | screens[1].explain.text | One year of daily prices with a closing bounce is a small sample for this test; a real relationship can fail it | correct | sim: L3:l12 power 0.71 on planted pairs over 252 days |
| l12-cointegration-selection | screens[2].prose | GGR use distance alone | correct | GGR §2.1 |
| l12-cointegration-selection | screens[2].explain.text | Before the break Engle-Granger swaps 10 planted pairs for chance pairs with tiny p-values; after it both rules find the same 3 survivors | correct | numbers script; sim: L3:l12 selection bias |
| l12-cointegration-selection | screens[3].prose | Engle-Granger regresses one log price on the other, with any slope, and tests whether the residual reverts | correct | Hamilton ch. 19 §19.2 (two-step); MacKinnon (2010) critical values |
| l12-cointegration-selection | screens[3].options[0], explain | Distance assumes equal normalised prices, a 1 to 1 hedge; Engle-Granger allows any hedge ratio and a wide spread if stationary | correct | GGR §2.2; Hamilton ch. 19 |
| l12-cointegration-selection | screens[3].options[1].why | Both rules trade a spread they expect to revert: Engle-Granger tests it, distance assumes it | correct | definitions |
| l12-cointegration-selection | screens[3].options[2].why | Neither rule uses industry | correct | GGR §2.1 (unrestricted); the course's EG rule |
| l12-cointegration-selection | screens[3].options[3].why | Small gaps and rare trades are a consequence of distance, not an assumption | correct | sim: L1:l3 screens[7] |
| l12-cointegration-selection | screens[4].prose | At 5% each test of a non-cointegrated pair passes by chance one time in 20 | correct | definition of size; MacKinnon (2010) p-values; sim: L3:l12 size 0.063 on mids |
| l12-cointegration-selection | screens[4].question, explain | Expected chance passes = 4,950 x 0.05 = 247.5 if no pair were cointegrated | correct | linearity of expectation (holds under dependence); sim: L3:l12 |
| l12-cointegration-selection | screens[4].explain.text | "The 392 chance passes exceed 248, because on this panel's short, noisy year the test over-rejects" | imprecise | the bounce raises the rejection rate only to about 7% (sim: L3:l12 size on closes 0.072 against 0.063 on mids), which explains about 100 of the extra 144; the rest is that the 4,950 tests share 100 shares and are dependent, so one year's count swings from 3% to 15% across fresh panels (sim: L3:l12 per-panel range). The explanation names one cause and omits the larger one |
| l12-cointegration-selection | screens[4].feedback.byKey.twenty | The question asks about chance passes, not planted pairs | correct | definition |
| l12-cointegration-selection | screens[5].options[0], explain | A formation p-value describes the formation year; the relationship can break the day trading begins; both rules choose on the past | correct | sim: L3:l12 screens[5] (planted pairs with p < 0.05 at 1,260 break at 1,512); LdP ch. 7 |
| l12-cointegration-selection | screens[5].options[1].why | The test covers days that are over | correct | logic |
| l12-cointegration-selection | screens[5].options[2].why | A p-value is not the chance the relationship holds; it is the chance of so small a statistic if it does not | correct | CB §8.3.4 (p-value definition); the EG null is no cointegration |
| l12-cointegration-selection | screens[5].options[3].why | Nothing bounds the trading z-score | correct | the formation sd does not constrain future residuals |
| l12-cointegration-selection | screens[6].prose, explain | ln L = 2 ln A + u gives an Engle-Granger slope of 2 with a small p-value, yet a large SSD; a hedge far from 1 is invisible to distance | correct | sim: L3:l12 screens[6] (slope 1.92, rank 92 of 4,950 in the auditor's construction; 177 in the course's) |
| l12-cointegration-selection | screens[6].options[1].why | A slope of 1 is what distance assumes | correct | GGR §2.2 |
| l12-cointegration-selection | screens[6].options[2].why | Regressing A on L gives the reciprocal slope | correct | OLS of the reverse regression: about 1 / 2 when the fit is tight |
| l12-cointegration-selection | screens[7].explain.text | Scaling a price adds a constant to its log, absorbed by the intercept, so normalised and raw prices give the same p-value | correct | `coint` includes a constant (trend "c"); sim: L3:l12 screens[7] |
| l12-cointegration-selection | screens[8].widget | `coint_pairs` (stable argsort of p-values), `false_positive_count` = n x alpha | correct | numbers script |
| l12-cointegration-selection | screens[8].explain.text | At start 0, 18 of the shortlist's 30 chance pairs pass at 5%, not 2.5 | correct | numbers script; sim: L3:l12 selection bias (28% of the 30 closest chance pairs pass on fresh panels, far above 5%) |
| l12-cointegration-selection | screens[9].prose | Distance fixes beta = 1 and wants small gaps; Engle-Granger estimates beta and wants a stationary u_t; each test of a pair picked blind passes by chance at its level | correct | Hamilton ch. 19; definition of size |
| l12-cointegration-selection | screens[9].explain.text | Distance picks on the same year, which biases pairs towards passing | correct | sim: L3:l12 selection bias |
| l12-cointegration-selection | screens[10].options[0], explain | Shortlist on an economic link, test, confirm on a held-out year | correct | Vidyamurthy ch. 5 (economic rationale); LdP ch. 7 and 11 |
| l12-cointegration-selection | screens[10].options[1].why | About 2,240 chance passes would swamp the real ones | correct | 44,850 x 0.05 |
| l12-cointegration-selection | screens[10].options[2].why | Distance misses pairs with hedges far from 1, such as a leveraged fund on its index | correct | sim: L3:l12 screens[6] |
| l12-cointegration-selection | screens[10].options[3].why | A low formation p-value is no promise for the trading period | correct | sim: L3:l12 screens[5] |
| l12-cointegration-selection | summary.ideas[2] | Many tests mean many chance passes: tests times level; a formation p-value says nothing certain about the trading period | correct | as above |
| l12-cointegration-selection | quiz[0].explain.text | Lowering the level cuts chance passes but also fails more real pairs | correct | size against power |
| l12-cointegration-selection | quiz[1].options[0], explain | Log price moving half as far plus a stationary gap: Engle-Granger with a hedge near 0.5 can select it; distance cannot | correct | the mirror of screens[6] |
| l12-cointegration-selection | quiz[2].options[0], explain | The p-value describes the formation sample only; planted pairs scored near zero and still broke | correct | sim: L3:l12 screens[5] |
| l12-cointegration-selection | quiz[2].options[2].why | At start 1,260 Engle-Granger keeps 11 planted pairs that break the next day | correct | numbers script; sim: L3:l12 screens[5] (at least 8 kept pairs are broken ones) |
| l13-just-a-factor | screens[0].prose | One cycle in six, so no two overlap | correct | step 126 = trading length; trading windows are disjoint |
| l13-just-a-factor | screens[0].explain.text | The least-squares slope of the book on the market is its market beta; the cloud is close to flat | correct | definition (CAPM beta as a regression slope); numbers script |
| l13-just-a-factor | screens[1].prose | GGR find pairs returns are not explained by standard risk factors; the constant is the alpha | correct | GGR §4.1 (Table 5: regressions on market, SMB, HML, momentum and reversal factors leave a significant intercept) |
| l13-just-a-factor | screens[1].explain.text | The market explains about 2% of the variation (R^2 0.021) | correct | definition of R^2 |
| l13-just-a-factor | screens[2].options[0], explain | The two legs carry the same market loading, so it cancels in each pair; what is left is the gap | correct | generator (one market factor for every share); sim: L3:l13 screens[2] (mean beta 0.07 across fresh panels) |
| l13-just-a-factor | screens[2].options[1].why | A rising market lifts both legs and cancels | correct | same |
| l13-just-a-factor | screens[2].options[3].why | Few points widen the error band; they do not pull the slope to 0 | correct | OLS: n affects the standard error, not the expectation of the slope |
| l13-just-a-factor | screens[3].prose, explain | R = alpha + beta R_m + e; alpha is the average return the market does not explain; the prediction is an average with wide scatter | correct | regression definitions |
| l13-just-a-factor | screens[4].options[0], explain | Report 7.11 on non-overlapping cycles or a Newey-West t on all 127; plain OLS on overlapping cycles inflates t | correct | HH (1980), NW (1987); sim: L2:l8 screens[4] |
| l13-just-a-factor | screens[4].options[1].why | Overlapping cycles repeat five months in six, so they are not new data | correct | MA(5) overlap |
| l13-just-a-factor | screens[4].options[2].why | Averaging a sound and an inflated figure is still inflated | correct | logic |
| l13-just-a-factor | screens[5].options[0], explain | A small beta rules out market risk only; the break was a pair-level risk the regressor cannot see; 24 of 127 cycles lose with the wait | correct | sim: L3:l13 screens[5] |
| l13-just-a-factor | screens[5].options[3].why | A t of 7.11 on 22 independent cycles is not luck; beta says nothing about that | correct | the 22 trading windows are disjoint; alpha and beta are separate coefficients |
| l13-just-a-factor | screens[6].prose | The paper also finds that pairs returns share a common latent factor | correct | GGR §5 (returns of the top pairs are correlated with those of pairs 101 to 120 after controlling for factors; abstract links the profits to a common factor) |
| l13-just-a-factor | screens[6].options[0], explain | On a panel built with independent pair gaps the correlation is near 0; it cannot test the paper's real-data finding | correct | generator (independent OU gaps); logic |
| l13-just-a-factor | screens[6].options[2].why | A correlation of -0.12 on 22 cycles is well inside its noise | correct | se about 1 / sqrt(22) = 0.21 |
| l13-just-a-factor | screens[7].prose, explain | With equal loadings, £1 long and £0.60 short leave £0.40 of industry exposure; a 1 to 1 hedge cancels it | correct | linear exposure; sim: L3:l13 screens[7] |
| l13-just-a-factor | screens[8].explain.text | The market return must cover the same days as the pairs return | correct | regression alignment |
| l13-just-a-factor | screens[9].explain.text | The wait lowers the alpha, not the market exposure | correct | numbers script (betas 0.053 and 0.043) |
| l13-just-a-factor | screens[10].options[0], explain | Industry regressions show whether the hedges leave a factor behind; the worst cycles show whether losses cluster when spreads widen; a small market beta settles neither | correct | GGR §4.1 run multi-factor regressions; short-volatility books show in tail cycles |
| l13-just-a-factor | screens[10].options[2].why | A high Sharpe ratio is what a short-volatility book shows before its loss | correct | the Sharpe ratio ignores tail risk |
| l13-just-a-factor | summary.formula.note | Use non-overlapping cycles or Newey-West errors | correct | sim: L2:l8 |
| l13-just-a-factor | quiz[1].options[2].why | Beta and alpha are separate coefficients | correct | OLS |
| l14-out-of-sample | screens[0].prose | Lock years 7 to 12 away; years 1 to 6 stand for the paper's sample | correct | LdP ch. 7 and 11 (hold-out); the course's convention |
| l14-out-of-sample | screens[0].explain.text | 10 in-sample cycles, 12 held out; every setting is chosen on the first 10 alone | correct | sim: L3:l14 screens[0] |
| l14-out-of-sample | screens[1].explain.text | Lower thresholds trade more often and earned more in years 1 to 6; now run the chosen setting once | correct | panel fact; protocol |
| l14-out-of-sample | screens[2].explain.text | Part of the fall is the break; part is having picked the luckiest cell | correct | sim: L3:l14 (winner's curse: the best of 12 equal settings falls back out of sample) |
| l14-out-of-sample | screens[3].explain.text | The best of many in-sample results is partly the luckiest | correct | sim: L3:l14; LdP ch. 11 |
| l14-out-of-sample | screens[4].prose, explain | The fairest extension runs the paper's rules unchanged; no setting was tuned, so this is the headline | correct | protocol |
| l14-out-of-sample | screens[5].options[0], explain | Choosing on the held-out half makes it in sample again; the figure is a best-of-12 | correct | LdP ch. 11 |
| l14-out-of-sample | screens[5].options[2].why | More settings make the best one luckier still | correct | order statistics of a maximum |
| l14-out-of-sample | screens[5].options[3].why | The wait is the conservative fill; dropping it adds the bounce back | correct | sim: L2:l9 |
| l14-out-of-sample | screens[6].options[0], explain | One setting of 12 rising on a dozen cycles is within chance; reporting it as robust would be choosing on the held-out half | correct | sim: L3:l14; multiple comparisons |
| l14-out-of-sample | screens[7].widget, explain | `sweep` keeps cycles with start + 378 <= end_day, so the sweep never touches a cycle that trades after the lock | correct | numbers script; code inspection |
| l14-out-of-sample | screens[8].widget, explain | `held_out` keeps cycles with start + 252 >= start_day; run once on the setting chosen in sample | correct | numbers script |
| l14-out-of-sample | screens[9].prose | survived = r_out(theta*) / r_in(theta*), theta* = argmax of the in-sample mean, fixed before the held-out half opens | correct | protocol definition |
| l14-out-of-sample | screens[9].options[2].why | An average of the halves hides the decline | correct | logic |
| l14-out-of-sample | screens[9].options[3].why | The best in-sample figure was chosen to be the largest, so it flatters the rule | correct | sim: L3:l14 |
| l14-out-of-sample | screens[10].options[0], explain | Lead with the untuned rules, the held-out years, the share that survived and the data | correct | reporting practice |
| l14-out-of-sample | quiz[1].options[0], explain | After choosing on the held-out data it no longer tests that setting; a fresh held-out period would be needed | correct | LdP ch. 11 |
| l14-out-of-sample | quiz[2] | start + 378 <= 1,008 gives 6 cycles | correct | arithmetic with the rule |
| l15-pairs-note | screens[0].explain.text | The top 5 keep 69% against 42% for the top 20 because the three unbroken pairs usually rank in the top 5 after the break | correct | panel fact; numbers script |
| l15-pairs-note | screens[1].options, explain | "Pairs trading still works on real markets today" overclaims: a seeded panel proves only that the code works | correct | logic |
| l15-pairs-note | screens[2].explain.text | Per month = cycle / 6; year = (1 + m)^12 - 1; survived = after / before; break-even = gross / (4 x trips) | correct | course conventions; sim: L1 and L2 |
| l15-pairs-note | screens[3].options[0], explain | The survival sentence gives the share, the untuned rules and the planted cause | correct | reporting practice |
| l15-pairs-note | screens[3].options[1].why | 42% survived, on planted data: "died" overclaims twice | correct | logic |
| l15-pairs-note | screens[4].options | What changes on real data: delistings, dividends, short fees and recalls, varying spreads, pairs that break for other reasons and no list of true pairs; not a different distance formula; the wait still matters | correct | GGR §2.1 (total returns, delistings), §4.3 (costs); generator limits |
| l15-pairs-note | screens[4].options[6].why | Real closes sit at the bid or the ask too, so the wait still matters | correct | Roll (1984) |
| l15-pairs-note | screens[5].options[0], explain | 1.50% stacks same-day fills, no costs and the pre-break years; the conservative lead is 0.75% with the wait over all years | correct | reporting practice |
| l15-pairs-note | screens[5].options[3].why | Committed capital is the conservative return; employed is higher | correct | GGR §2.4 |
| l15-pairs-note | screens[6].options[0], explain | A negative held-out mean reads "None of the effect survived", with the same prominence | correct | reporting practice; sim: L3:l15 screens[8] |
| l15-pairs-note | screens[7].widget | Note order: question, data, method, results, costs, decline, cointegration and factors (either order), out of sample, real data | correct | document structure |
| l15-pairs-note | screens[8].widget, explain | A ratio at or below 0 reads none; a rise reads over 100%; a zero in-sample mean raises because a share of nothing is undefined | correct | sim: L3:l15 screens[8]; numbers script |
| l15-pairs-note | screens[9].options[1].why | A seeded panel proves nothing about markets, and 9.4% is a pairs return, not a margin over the market | correct | the figure is an excess return over zero (GGR §2.4), not over the market |
| l15-pairs-note | quiz[1].options[2].why | We could only match the facts we quoted, on data we built | correct | logic |
| review-3 | items[1].options[0], explain | Fewer opens and smaller gains with convergence held at 75% fits crowding; broken pairs would cut the crossing share | correct | DF (2010); sim: L3:l11 |
| review-3 | items[2].explain.text | Pool the trades: averaging the two cycle shares weights the smaller cycle too heavily | correct | sim: L3 review-3 items[2] |
| review-3 | items[3].explain.text | 190 x 0.05 = 9.5 chance passes even with no real pair | correct | definition of size |
| review-3 | items[4].options[0], explain | Engle-Granger with a hedge near 2 can select L and A; distance cannot | correct | sim: L3:l12 screens[6] |
| review-3 | items[4].options[2].why | Only the rule that estimates the slope sees the stationary gap | correct | Hamilton ch. 19 |
| review-3 | items[5].options[0], explain | The shortlist was chosen on the same noisy year, so its chance pairs already look stationary; five planted pairs fail at 5% while some chance pairs score near zero; a low one-year p-value is weak evidence | correct | sim: L3:l12 (selection bias 0.28; power 0.71) |
| review-3 | items[5].options[1].why | The chance pairs are independent random walks by construction | correct | generator |
| review-3 | items[5].options[2].why | Engle-Granger can detect a half-life of 8 days: most planted pairs pass | correct | sim: L3:l12 power 0.71 |
| review-3 | items[6].explain.text | The market adds under a point; almost all the return is alpha | correct | 0.0529 x 0.15 against 0.0623 |
| review-3 | items[7].feedback.byKey.* | A larger short leg makes the net exposure negative; only a 1 to 1 hedge cancels | correct | linear exposure |
| review-3 | items[8].options, explain | Only a setting fixed before the held-out years gives an out-of-sample figure; the best held-out cell is a best-of-12 | correct | LdP ch. 11; sim: L3:l14 |
| review-3 | items[8].options[3].why | No single rule earned the average of all 12, so it reports no strategy | correct | logic |
| review-3 | items[9].options, explain | A negative ratio reads "None of the effect survived" with the same prominence | correct | course convention; sim: L3:l15 |
| homework-3 | items[0].prose, widget | Distance keeps the closest k of the n candidates; Engle-Granger keeps the k lowest p-values; each traded with its own rule | correct | numbers script runs solution and starter; `trade_coint` estimates beta, alpha and sd on formation only (no look-ahead) |
| homework-3 | items[0].explain.text | With k = 5 at start 0 Engle-Granger's wider spreads earn 18.19% against 11.36% | correct | numbers script; consistent with l12 screens[3] (wide but stationary spreads trade more) |
| homework-3 | items[1].prose, widget | Hit rate = share of cycles with a positive committed return over a trailing window; a return of exactly 0 is not a hit | correct | definition stated; numbers script |
| homework-3 | items[1].explain.text | A falling hit rate is the alarm of l11's transfer screen | correct | consistent with l11 screens[10] |
| homework-3 | items[2].lines | Fix the split first; sweep on cycles that end by day 1,512; choose on the in-sample grid; run once on the held-out cycles; report out over in; the two distractors choose on the held-out years or move the split | correct | LdP ch. 7 and 11 |
| homework-3 | items[2].explain.text | Our chosen setting kept 28% of its return, the paper's own 42% | correct | numbers script |
| homework-3 | items[3].explain.text | (3 x 10.45% + 17 x 2.37%) / 20 = 3.58%; the mix of pairs, not the rule, moved the return | correct | weighted mean; sim: L3:l11 |
| homework-3 | items[3].feedback.byKey.emp3 | Committed capital divides by all 20 | correct | GGR §2.4 |
| homework-3 | items[4].explain.text | 10 industries of 45 pairs give 450 tests and 22.5 chance passes; restricting to an economic link cuts the chance passes elevenfold | correct | combinatorics; 4,950 / 450 = 11 |
| homework-3 | items[5].options[0], explain | Regress 22 non-overlapping cycles or all 127 with Newey-West errors; plain OLS on 127 inflates t | correct | sim: L2:l8 |
| homework-3 | items[5].options[2].why | Regressing the market on the pairs returns reverses the question | correct | regression direction |
| homework-3 | items[5].options[3].why | Choosing the sample after seeing it biases the estimate | correct | LdP ch. 11 |
| homework-3 | items[6].model | Method: normalise to 1 at the formation start, rank all pairs by SSD, trade the closest 20 for six months, open beyond 2 formation sds £1 a side, close at the crossing or the last day, may reopen; committed and employed; same day and with the wait | correct | GGR §2.1 to §2.4 |
| homework-3 | items[6].model | The conservative cell sits inside the paper's "up to 11%" by design; the decline matches Do and Faff (2010); Engle-Granger selection earns less and passes many chance pairs; beta 0.053 with alpha t 7.11; 42% survived with the paper's rules, 28% for the tuned setting | correct | GGR abstract; DF (2010); numbers script; sim: L3 |
| homework-3 | items[6].model | Real data: millions of pairs, delistings, corporate actions, dividends, short fees and recalls, varying spreads, pairs that break for reasons no seed imitates | correct | GGR §2.1 and §4.3; generator limits |

## Verdict counts

Rows: 424. correct 410, wrong 7, imprecise 5, misleading 0, unverified 2 (the two rows on whether the paper re-bases the normalised series at the trading start, l10 screens[3].options[1] and the Level 1 cross-reference row; the paper text could not be fetched in this session).
