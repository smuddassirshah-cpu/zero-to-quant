# Claim ledger: pairs-rep L1 to L3, concept audit round 2 (blind)

Auditor: Fable, 6 November 2026. Blind to review-pairs-rep*, audit-pairs-rep-1-3 and the round-1 concepts scripts until this file was committed.

Paper access. `WebFetch` on the Wharton PDF, the NBER PDF and a lecture copy all failed (host not resolvable from this session). Every "paper" basis below rests on secondary quotations found with `WebSearch`: the SSRN and RFS abstracts; a Lund thesis quoting p. 803 on the two-stage matching; a student summary of section 2.3 on committed and employed capital; a replication paper and Krauss (2017, Journal of Economic Surveys) on re-normalisation at the trading start; a working-paper excerpt on delisting; a Stony Brook lecture transcription of Table 1 (top 5 1.308%, top 20 1.436% fully invested, 0.745% and 0.895% with one-day wait; committed 0.784% and 0.805%, 0.463% and 0.520% with the wait); Table 2 figures (trigger 0.0476 and 0.0528, 4.81 and 19.30 pairs traded, 3.75 and 3.76 months open); Do and Faff (2010) abstract. Where only the course's own panel is claimed, the basis is the number script (`docs/reports/pairs-rep-L<n>-numbers.py`, all three exit 0) or my concepts script (`docs/reports/pairs-rep-L<n>-concepts-r2.py`, check name in brackets).

Abbreviations: GGR = Gatev, Goetzmann and Rouwenhorst (2006). "numbers" = recomputed by the level's number script. "r2 Lk" = check k in my concepts script for that level. "course convention, stated" = the text presents it as the course's own choice.

Verdicts: correct, wrong, imprecise, misleading, unverified.

## Level 1

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l1 | screens[0].options[0] | Convergence trade: buy the laggard, sell the leader, wait for them to meet | correct | GGR trading rule: long the loser, short the winner on divergence (Krauss 2017 §2.1 description) |
| l1 | screens[0].options[1].why | Buy B sell A bets on the gap widening: momentum, the opposite trade | correct | sign of payoff flips with the sides; r2 L1 (sign) |
| l1 | screens[0].options[2].why | Buying both is a bet on the market, not the gap | correct | long-long has market loading 2, no gap exposure |
| l1 | screens[0].explain | Owning A and owing B gains when the gap shrinks whatever the market does | correct | equal £ long and short cancel a common factor; l13 s2 derivation |
| l1 | screens[1].prose | GGR form pairs over a year, trade over the next six months, a new portfolio every month | correct | GGR §2 as quoted in Lund thesis and Krauss 2017; 12-month formation, 6-month trading, monthly overlapping |
| l1 | screens[1].explain | 126 / 21 = 6 portfolios always live from the sixth month | correct | arithmetic; r2 L1 (live) |
| l1 | screens[1].explain | Momentum studies overlap their portfolios in the same way | correct | Jegadeesh and Titman (1993) overlapping-portfolio design, which GGR cite |
| l1 | screens[2].prose | Paraphrase: total-return index set to 1 twelve months back, each share matched to its closest partner, top 20 and top 5 traded, open at two sd | correct | GGR §2.1 and 2.2 (Lund thesis quote of p. 803; Quantpedia summary); the paper also reports pairs 101 to 120, which the course omits |
| l1 | screens[2].feedback.byKey.days-f | 252 is the formation period in trading days | correct | 12 months of 21 days; course calendar |
| l1 | screens[3].slots | Scaling, distance, selection, sd belong to formation; open, close at cross, close on last day to trading | correct | GGR: sd "estimated during the pairs formation period"; closing at next crossing or end of period |
| l1 | screens[3].explain | Everything that chooses or measures is fixed at the end of formation; that split makes the backtest honest | correct | no trading-period data used in selection or threshold; look-ahead avoided |
| l1 | screens[4].widget | `cycle_windows` and `live_portfolios` solution passes, starter fails | correct | r2 L1 (code) and numbers check_code |
| l1 | screens[4].explain | `max(0, ...)` handles the first months before six portfolios exist | correct | code reading |
| l1 | screens[5].options[0] | Only the formation-period sd may be used on a trading day | correct | GGR: historical sd from the formation period; trading-period sd needs future prices |
| l1 | screens[5].options[1].why | Trading-period sd uses prices from days not yet happened: look-ahead | correct | definition of look-ahead |
| l1 | screens[5].options[2].why | Twelve-year sd: eleven years lie in the future of most trades | correct | the panel is 12 years; look-ahead |
| l1 | screens[5].explain | A threshold computed on trading prices sees the future, "and it flatters the backtest" | imprecise | the look-ahead part is right; the flattering is not a law: r2 L1 (lookahead), 30 fresh first cycles, trading-sd thresholds earn +0.6 points a cycle more than formation-sd thresholds with se 0.5, consistent with no effect. The honest claim is that it uses prices the desk does not have |
| l1 | screens[6].options[0] | Delisted share: close both legs at the last price | correct | GGR (working-paper excerpt): "close the position ... using the delisting return, or the last available price"; for a cash takeover these coincide |
| l1 | screens[6].options[1].why | Dropping the pair hides a real outcome; the paper keeps every nominated pair | correct | GGR keep delisted pairs with the delisting return |
| l1 | screens[6].options[2].why | B was bought out for cash, not wiped out | correct | scenario statement |
| l1 | screens[6].options[3].why | A replacement partner was never in the formation choice | correct | selection fixed at formation end |
| l1 | screens[7].prose | formation [d, d+252), trading [d+252, d+378), new cycle every 21 days, six at once | correct | course calendar; r2 L1 (live) |
| l1 | screens[8].explain | Six overlapping portfolios of 20 pairs give 120; a share can appear in several of them | correct | portfolios are chosen independently each month |
| l1 | screens[8].explain | "Most will be waiting for a 2 sd gap" (most of the 120 pairs idle) | imprecise | r2 L1 (open-share): the top-20 pairs are open on about half of pair-days on this panel and l13 s2 says "our pairs are open most of the time"; one of the two is wrong, see finding |
| l1 | quiz[0].options[0] | sd from the six trading months uses future prices to set today's threshold | correct | look-ahead |
| l1 | quiz[0].options[1].why | The number of days is not the problem, their dates are | correct | 126 days suffice for an sd |
| l1 | quiz[0].options[2].why | It differs, 0.0300 against 0.0210, and uses the future | correct | numbers |
| l1 | quiz[1].explain | Months 0, 1, 2 have each started one portfolio so 3 trade | correct | arithmetic |
| l1 | quiz[2].options | Closing at a crossing is the only trading-period rule of the four | correct | as screens[3] |
| l1 | summary.trap | Measuring the sd on the trading period uses prices the desk has not seen | correct | look-ahead |
| l2 | screens[0].explain | Dividing by the first price makes a £10 and a £400 share comparable; the paper does this with each total-return index | correct | GGR normalised cumulative total-return index starting at 1 (Quantpedia; Lund thesis) |
| l2 | screens[1].prose | Distance = sum of squared differences between the two normalised paths; GGR rank pairs by it | correct | GGR p. 803 as quoted: "minimizes the sum of squared deviations between the two normalized price series" |
| l2 | screens[1].explain | Every day adds a squared gap so SSD only grows | correct | sum of non-negative terms |
| l2 | screens[2].feedback.byKey.unsq | Adding unsquared gaps lets signs cancel | correct | r2 L1 (ssd-toy) |
| l2 | screens[2].feedback.byKey.absd | The paper squares the gaps, not absolute values | correct | SSD definition |
| l2 | screens[2].explain | Squaring weights big gaps more than small ones | correct | convexity of the square |
| l2 | screens[3].prose | The trigger uses the spread's sd over formation, `np.std` default dividing by n | correct | course convention, stated once where it first matters; paper does not say n or n-1; with n = 252 the two differ by 0.2% |
| l2 | screens[3].feedback.byKey.ddof1 | `np.std` divides by n unless told otherwise | correct | NumPy documentation; r2 L1 (sd-toy) |
| l2 | screens[3].feedback.byKey.rms | Root mean square of the spread is not its sd when the mean is not 0 | correct | r2 L1 (sd-toy) |
| l2 | screens[4].widget | `normalise`, `ssd` solution passes, starter fails | correct | r2 L1 (code) |
| l2 | screens[4].explain | Dividing by `P[0]` broadcasts across columns | correct | NumPy broadcasting |
| l2 | screens[5].prose | SSD_ij = G_ii + G_jj − 2 G_ij with G = P^T P | correct | expansion of (p_i − p_j)^2; r2 L1 (gram) |
| l2 | screens[5].explain | The diagonal is exactly 0 | correct | 2 d_i − 2 G_ii with G_ii = d_i is exactly 0 in floating point; r2 L1 (gram) |
| l2 | screens[6].options[0] | A dividend drop in a price series looks like a divergence; on total returns there is no gap | correct | total-return index reinvests the dividend; GGR use total-return indices |
| l2 | screens[6].options[1].why | Holders of B lost nothing: the 4% arrived as cash | correct | ex-dividend accounting |
| l2 | screens[6].explain | A 4% drop is about two formation sds for a close pair | correct | 2 × 0.021 = 0.042; numbers |
| l2 | screens[7].options[0] | Identical paths: sd 0, never opens, guard against dividing by 0 | correct | 0 > 2 × 0 is false; code guard `sd > 0` |
| l2 | screens[7].options[2].why | 0 / 0 is NaN in NumPy and NaN > 2 is False, hiding the case | correct | IEEE 754; r2 L1 (nan) |
| l2 | screens[8].prose | G's log return is always twice A's, so their returns have correlation 1 | correct | r_G = 2 r_A is a linear map, correlation 1 |
| l2 | screens[8].options[0] | The levels drift apart and the SSD is large | correct | p_G = p_A^2 in normalised terms; r2 L1 (corr-vs-dist) |
| l2 | screens[8].options[2].why | Distance and correlation can disagree completely | correct | same check |
| l2 | screens[8].explain | Cointegration's "Correlation is not cointegration" makes the same point | correct | standard distinction |
| l2 | screens[9].lines | Derivation of the Gram identity; the distractor squares the sum of gaps | correct | algebra; r2 L1 (gram) |
| l2 | screens[10].options[0] | Distance assumes equal normalised prices, a hedge ratio of 1, nothing to estimate beyond the sd | correct | £1 long £1 short in GGR; no regression in the distance method |
| l2 | screens[10].options[2].why | Distance can pick spurious pairs too | correct | l3 s8: chance pairs of random walks |
| l2 | screens[10].options[3].why | Cointegration allows any hedge ratio and tests the spread; distance fixes the ratio at 1 | correct | Engle and Granger (1987) |
| l2 | summary.trap | Normalising prices instead of total returns makes a dividend look like a divergence | correct | as screens[6] |
| l2 | quiz[1].options[0] | Re-basing at the trading start puts spread and threshold on different bases, so the gap is mismeasured; "what goes wrong" | misleading | Krauss (2017, §2.1) and Rad, Low and Faff (2016) both describe GGR as re-normalising prices at the start of the trading period; l10 screens[3] itself lists "normalise once and carry through" as a difference from the paper. Re-basing is a convention the paper (per those sources) uses, not an error; see finding |
| l2 | quiz[1].options[1].why | Re-basing resets any gap open at the end of formation to 0 | correct | spread at t0 becomes 1 − 1 = 0 |
| l2 | quiz[1].options[2].why | Re-basing is not look-ahead since the first trading price is known that day | correct | uses day-0 price only |
| l2 | quiz[2] | The pair with gaps 0, 0.01, −0.01 has the smallest SSD | correct | arithmetic |
| l2 | summary.ideas[2] | Correlated returns can still drift apart in level | correct | r2 L1 (corr-vs-dist) |
| l3 | screens[0].explain | 100 shares make 100 × 99 / 2 = 4,950 pairs | correct | binomial coefficient |
| l3 | screens[1].explain | The 20 closest stop at 0.6717 and the 21st is 0.9989; a hint the first 20 are different | correct | numbers; interpretation hedged as "a hint" |
| l3 | screens[2].explain | Ranking all 4,950 cells this way is the selection step | correct | GGR rank by SSD |
| l3 | screens[3].widget | `top_pairs` solution passes, starter fails; stable sort keeps ties in order | correct | r2 L1 (code); NumPy `kind="stable"` |
| l3 | screens[3].explain | The first year's top 20 are the 20 planted pairs, each sharing a random walk | correct | numbers; generator reading (common[:, k]) |
| l3 | screens[4].prose | In the paper each share nominates its closest partner, and one share may be nearest to several others | correct | GGR p. 803 "for each stock a matching partner"; nothing in the quoted method forbids a shared partner |
| l3 | screens[4].prose | Our course keeps the closest pairs overall, so a share may appear twice | correct | course convention, stated as the course's own; note that a top-k-overall list can also hold a pair neither member nominated, so it is not the paper's list either, which the course does not claim |
| l3 | screens[4].options[1].why | The two closest overall are also allowed by the paper's rule (toy) | correct | in the toy A–B is A's nearest partner, so nominated; r2 L1 (nominate-toy) |
| l3 | screens[4].options[2].why | After B–C, C already has a partner | correct | greedy rule |
| l3 | screens[4].explain | On the first year the two course rules agree; in late years they do not | correct | numbers (tests at 0, 1134, 2016) |
| l3 | screens[5].widget | `one_partner_pairs`, `same_industry_share` solution passes, starter fails | correct | r2 L1 (code) |
| l3 | screens[6].explain | The paper lets a share be the nearest partner of two others; the one-pair variant drops repeats; the course keeps them | correct | as screens[4] |
| l3 | screens[7].options[0] | Among the 20 closest, rank barely predicts profit (rank correlation 0.04); the fifth closest never opened | correct | numbers (Spearman 0.04; pair never opens) |
| l3 | screens[7].options[1].why | A pair that never drifts 2 sd apart never trades | correct | opening rule |
| l3 | screens[7].feedback.correct | Close is necessary, not sufficient | correct | within the method, closeness selects; profit needs a divergence |
| l3 | screens[8].prose | Two unrelated random walks can stay close for a year by luck | correct | r2 L1 (chance-close): on fresh panels unplanted pairs enter the top 20 after the break |
| l3 | screens[8].explain | Cointegration's first lesson shows the same trap: unrelated walks that look related | correct | spurious regression (Granger and Newbold 1974) |
| l3 | screens[9].prose | N(N−1)/2 pairs; the paper itself only gives each share its closest partner | correct | binomial; GGR matching |
| l3 | screens[10].prose | The paper's robustness check trades only same-industry pairs | correct | GGR restrict pairs within industry groups as a robustness check (Table 5 of the paper per Krauss 2017 summary) |
| l3 | screens[10].explain | Chance pairs ignore industries, which is one reason the paper checks same-industry pairs | correct | numbers: same-industry share 1.0 then 0.35 |
| l3 | quiz[1] | One-pair variant keeps (4, 9) then (7, 20) | correct | greedy rule |
| l3 | quiz[2].options[2].why | A pair that never opens is far likelier to earn exactly 0 than one that gained and lost the same | correct | exact 0 from a continuous payoff has probability 0 |
| l4 | screens[0].explain | Dividing by every nominated pair, traded or not, is the return on committed capital; an unopened pair counts as 0 | correct | GGR §2.3 as quoted: committed divides payoffs by the number of pairs selected |
| l4 | screens[1].prose | Employed divides only by the pairs that opened | correct | GGR "fully invested" return divides by the number of pairs that open |
| l4 | screens[1].explain | Fewer opened pairs make employed larger, never smaller, when the total is positive | correct | Π/n ≥ Π/k for n ≤ k, Π > 0 |
| l4 | screens[2].prose | The paper reports monthly figures; for now divide by 6 | correct | course convention, stated; GGR Table 1 is monthly |
| l4 | screens[2].explain | The paper compounds daily returns within each month instead | unverified | GGR §2.3 not reachable; secondary sources describe daily marked-to-market portfolio returns but do not quote the monthly compounding |
| l4 | screens[3].options[0] | A self-financing position has no risk-free return to subtract, so its payoff is an excess return | correct | GGR call them excess returns on self-financing portfolios (abstract) |
| l4 | screens[3].options[2].why | Excess means over the risk-free rate, not over the market | correct | standard definition |
| l4 | screens[3].explain | Margin and borrowing fees are real, which level 2 adds | correct | later lessons charge costs; margin is not in fact modelled, see l8 s9 |
| l4 | screens[4].explain | 1.0075^12 − 1 = 9.38%; the paper reports annualised excess returns of up to 11% | correct | abstract: "up to 11 percent"; compounding is the course's stated yardstick |
| l4 | screens[4].explain | "We tuned the planted gap size so that our result lands in that range" | correct | honest statement of design; l10 repeats it |
| l4 | screens[5].options[0] | Employed on a zero-cost position is not comparable with a fund's return on capital | correct | different denominators; GGR themselves add a committed measure for this reason |
| l4 | screens[5].options[2].why | Committed is smaller than employed here and still not a return on capital | correct | n < k here; no margin modelled |
| l4 | screens[6].options[0] | With nothing opened, employed is 0/0; report 0 by a stated rule and keep the cycle | correct | course convention, stated; the paper's fully invested measure is undefined there too |
| l4 | screens[6].options[1].why | Dropping quiet cycles inflates the average | correct | selection on outcome |
| l4 | screens[6].options[2].why | 0/0 raises in Python and gives NaN in NumPy | correct | r2 L1 (nan) |
| l4 | screens[7].widget | `committed_and_employed` solution passes, starter fails | correct | r2 L1 (code) |
| l4 | screens[8].prose | R_committed = Σπ/k, R_employed = Σπ/n, employed at least as large when the total is positive | correct | algebra |
| l4 | screens[9].options | Capital, trades and costs come before reading the returns; SSD and journal do not | correct | judgement consistent with l4 s5 and l9 |
| l4 | screens[9].explain | The paper reports that profits survive conservative cost estimates | correct | abstract: "profits typically exceed conservative transaction costs estimates" |
| l4 | quiz[0].explain | Multiplying then compounding again counts the year twelve times | correct | 1.09^12 is a 12-year compound |
| l4 | quiz[2].options[0] | Employed is smaller than committed when the total is negative and some pairs never opened | correct | Π/n < Π/k for Π < 0, n < k |
| l5 | screens[0].explain | A trigger from days 252 to 377 uses future prices; a check after each step catches it | correct | look-ahead |
| l5 | screens[1].explain | With seed 2006 pairs 4, 7, 16 never break; the other 17 split at day 1,512 | correct | numbers |
| l5 | screens[2].prose | Each close sits at bid or ask half a per cent from mid, a coin each day; a same-day trade on closes earns a bounce that is not real | correct | generator reading; Roll (1984) bid-ask bounce; r2 L1 (placebo) |
| l5 | screens[3].explain | φ^8 = 0.5 gives φ = 0.9170; each day keeps 91.7% of the gap | correct | AR(1) half-life |
| l5 | screens[4].lines | Plan order: panel, normalise, distance, select, trade, returns, costs and wait in either order, extension last | correct | data dependencies |
| l5 | screens[5].explain | A comparison with NaN is False, so a NaN price fails the positive check | correct | IEEE 754; r2 L1 (nan) |
| l5 | screens[6].prose | Random pairs have no reason to converge | correct | generator: unplanted shares are independent random walks |
| l5 | screens[6].explain | On fresh panels random pairs average within noise of 0 on mids, since no open or close rule beats a random walk | correct | r2 L1 (placebo): 40 fresh seeds, mean payoff on mids within 2 se of 0; on closes positive (bounce) |
| l5 | screens[7].options[0] | About 0.19 points a month of the same-day result is bounce | correct | numbers: closes 1.004%, mids 0.816% |
| l5 | screens[7].options[2].why | The mid-price run still earns a profit; only the gap is bounce | correct | numbers |
| l5 | screens[7].options[3].why | The wait mostly removes a bounce nobody could capture; its real cost is a day of convergence | correct | l9 s7 split; r2 L1 (placebo) |
| l5 | screens[7].explain | Even random pairs gain about 0.13 points a cycle from the bounce | correct | numbers: −1.00% on closes against −1.13% on mids over 200 seeds |
| l5 | screens[8].prose | The paper closes a pair at the last price when a share delists; the seeded panel has none | correct | GGR delisting rule (excerpt) |
| l5 | screens[8].options[0] | Keep the untested step, flag it, test it on a planted delisting | correct | software practice |
| l5 | screens[9].prose | Π/k ≤ Π/n and employed/committed = k/n for Π > 0 | correct | algebra |
| l5 | screens[10].options | First commit: plan, targets with tolerance, seeded generator; not a tuned threshold or results | correct | pre-registration logic; l10 s5 |
| l5 | quiz[0].explain | A large placebo profit points at a bug or the bounce | correct | r2 L1 (placebo) |
| l5 | quiz[1] | Days 252 to 377 are the trading period, so a trigger from them is look-ahead | correct | calendar |
| review-1 | items[1].explain | Portfolios 4 to 9 trade in month 9; from month 5 on always six | correct | arithmetic |
| review-1 | items[3] | sd dividing by n of 0, 0.03, −0.03, 0 is 0.0212 | correct | course convention; numbers |
| review-1 | items[4].options[1].why | The closest pairs overall, which the paper's rule allows | correct | in the item (3, 5) is nominated by share 5 and (5, 9) by share 9; r2 L1 (nominate-toy) |
| review-1 | items[5].options[0] | 17 planted pairs stopped co-moving on day 1,512 so chance pairs fill the list | correct | generator; numbers |
| review-1 | items[5].options[3].why | The panel has no other traders | correct | generator |
| review-1 | items[7].explain | 1.01^12 − 1 = 12.68%; the wait brings it to about 9.4% | correct | arithmetic; numbers |
| review-1 | items[8].explain | A shorter half-life means faster convergence, so more round trips per cycle | correct | AR(1) with smaller φ crosses 0 sooner; r2 L1 (halflife) |
| homework-1 | items[0] (performance) | `form_pairs` solution passes 8 tests, starter fails | correct | r2 L1 (code) |
| homework-1 | items[0].explain | At starts 0 and 1,134 the rules agree because no share repeats; at 2,016 they part | correct | numbers |
| homework-1 | items[1].explain | A pair whose spread never passed 2 sd in formation may still trade later | correct | formation max/sd is not a bound on trading days |
| homework-1 | items[2].lines | Keep shares that traded every day of the formation year | correct | GGR screen out stocks with one or more days of no trade (Krauss 2017 summary) |
| homework-1 | items[2].lines | Build total-return indices, divide by first value, SSD, rank, record formation sd | correct | GGR method |
| homework-1 | items[2].lines[6].why | Re-estimating the sd on the first trading month is look-ahead | correct | uses trading prices for the threshold |
| homework-1 | items[3].model | Cointegration (Engle-Granger) assumes a stationary linear combination of log prices, estimates the hedge ratio, tests the residual for a unit root | correct | Engle and Granger (1987); Hamilton ch. 19 |
| homework-1 | items[3].model | Close pairs are often cointegrated with a ratio near 1, but distance never tests stationarity | correct | hedged "often"; l12 s0 shows disagreement |
| homework-1 | items[3].model | Distance cannot pick a pair whose fair ratio is far from 1 | correct | l12 s6: hedge 2 pair ranks 177th |
| homework-1 | items[3].model | Profits here exist because we planted them | correct | generator |
| homework-1 | items[4] | 14.20 / 11.36 = 1.25 = 5/4 so 4 of 5 opened | correct | k/n identity |
| homework-1 | items[5].explain | 1.0084^12 − 1 = 10.56%, a payoff per opened pair on a zero-cost position, not comparable with a fund | correct | as l4 s5 |
| homework-1 | items[6].options | The log supports selection, the k/n consistency and the bounce lift; not real-data or cost claims | correct | numbers; placebo |
