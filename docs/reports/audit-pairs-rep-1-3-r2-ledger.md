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

## Level 2

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l6 | screens[0].explain | GGR open a pair on the day its spread first passes 2 formation sds (same-day fill as the base case) | correct | Table 1 Panel A (no wait) is the paper's headline case and Panel B the one-day-wait robustness check (Stony Brook transcription; Quantpedia) |
| l6 | screens[1].prose | Cointegration's z-score thresholds are the same idea, measured in formation sds | correct | both are entry rules on a standardised spread |
| l6 | screens[1].explain | A wider trigger means fewer trades, each from a larger gap; the paper fixes 2 | correct | monotone in the threshold; GGR "two historical standard deviations" |
| l6 | screens[2].options[0] | Negative spread: buy A (cheaper normalised price), sell B | correct | convergence rule |
| l6 | screens[2].options[2].why | Selling both is a bet on the market falling, not on the gap | correct | net short the common factor |
| l6 | screens[3].prose | £1 buys 1/p units of a leg priced p; each leg's gain is units times price change | correct | arithmetic; GGR $1 long $1 short |
| l6 | screens[4].explain | 1.5 sd earns most on this pair; one pair in one cycle is not evidence for a lower trigger; choosing it on the same data overfits | correct | selection on the same sample; l14 |
| l6 | screens[5].explain | Buying the dear leg bets on divergence; the mirror trade loses what the right one gains | correct | r2 L1 (sign) |
| l6 | screens[6].options[0] | Spread already beyond 2 sd on day 0: open at once, the rule is a level test | correct | course convention (no re-basing); under the paper's re-based start the day-0 spread is 0 by construction, so the case cannot arise there; the screen does not claim it is the paper's |
| l6 | screens[6].options[1].why | The rule is a level, not a crossing | correct | GGR "diverge by more than two historical standard deviations" |
| l6 | screens[7].widget | `threshold`, `first_open`, `units` solution passes, starter fails | correct | r2 L2 (code) |
| l6 | screens[7].explain | The `sd > 0` guard handles identical paths; the day-0 test checks the loop starts at 0 | correct | code reading |
| l6 | screens[8].prose | Open on day t if the absolute spread exceeds 2 sigma_form, long the cheaper, 1/p units each side | correct | GGR rule in course notation |
| l6 | screens[9].explain | Equal pounds on each side is the paper's rule, scaled up | correct | GGR $1 long, $1 short |
| l6 | quiz[0] | Spread +0.040 beyond 0.036: short i, buy j | correct | sign convention stated on screens[7] |
| l6 | quiz[2].options[0] | Raising the trigger gives fewer trades, each at a larger gap | correct | threshold monotonicity; numbers (6, 4, 3, 2 opens) |
| l7 | screens[0].prose | The paper closes a pair when the two normalised prices cross | correct | GGR: unwind at the next crossing of the prices |
| l7 | screens[0].feedback.byKey.inside | Re-entering the 2 sd band does not close; the paper waits for the crossing | correct | same |
| l7 | screens[1].prose | GGR let a pair reopen after it closes | correct | GGR Table 2 reports round-trip trades per pair above 1 (Krauss 2017 summary) |
| l7 | screens[2].explain | A round trip pays the long leg's return minus the short leg's on £1 a side | correct | GGR pair payoff: return on long minus return on short, $1 each |
| l7 | screens[3].explain | The side alternates as the spread swings from one band to the other | correct | numbers (sides −1, +1, −1, +1) |
| l7 | screens[4].options[0] | A pair that never converges is booked at the last price of the period, a loss here | correct | GGR: if prices do not cross before the end of the trading interval, gains or losses are computed at the end of the last trading day |
| l7 | screens[4].options[2].why | Each cycle ends its own positions on its last day | correct | same |
| l7 | screens[4].explain | 35% of the top 20's trades end in a forced close; most such losses come from pairs close only by chance | correct | numbers (35%); r2 L2 (forced): losing forced closes come mostly from unplanted or broken pairs |
| l7 | screens[5].prose | A 4 sd stop is not in the paper | correct | GGR have no stop-loss |
| l7 | screens[5].explain | The stop cuts the mean from 6.02% to 4.32%; a planted pair at 4 sd usually comes back; real pairs may differ, so a stop is a risk choice | correct | numbers; hedged |
| l7 | screens[6].options[0] | Exiting when the spread re-enters the band books only part of the convergence | correct | numbers (0.1955 against 0.2218); GGR exit at crossing |
| l7 | screens[6].options[2].why | Band exit trades more often, so pays more costs | correct | numbers (9 trips against 4) |
| l7 | screens[7].explain | With the wait a signal on day 124 would open on day 125 and close at once; the rule t + 1 < 125 forbids it | correct | course code convention, stated |
| l7 | screens[8].widget | `trade_pair`, `holding_days` solution passes, starter fails | correct | r2 L2 (code) |
| l7 | screens[8].prose | After a close, scanning resumes the day after the exit; with wait 1 every open and close fills at the next day's price | correct | code reading; GGR wait-one-day rule applies to opening and closing |
| l7 | screens[9].options[0] | The rule holds an unconverged pair to a crossing or the forced close; the loss stays open | correct | GGR rule |
| l7 | screens[9].options[2].why | Adding doubles a bet the rule never makes | correct | GGR fixed $1 positions |
| l7 | summary.formula | pi = p_L^out/p_L^in − p_S^out/p_S^in | correct | long return minus short return |
| l7 | quiz[1].options[0] | The paper closes at the next crossing or on the last trading day | correct | GGR |
| l7 | quiz[1].options[2].why | The paper has no stop-loss | correct | GGR |
| l8 | screens[0].explain | GGR report both committed and employed returns | correct | GGR §2.3 as quoted |
| l8 | screens[1].explain | Returns are high before cycle 60 and lower after, which level 3 explains | correct | numbers; cycles whose trading crosses day 1,512 start at index 55 and up |
| l8 | screens[2].explain | The committed–employed gap is larger for the top 5 because one of five never opened | correct | k/n = 5/4 against 20/19 |
| l8 | screens[3].prose | The paper marks every pair to market daily, compounds within each calendar month, and averages the six live portfolios | unverified | consistent with secondary descriptions of GGR §2.3 (daily returns, overlapping portfolios as in Jegadeesh and Titman) but the compounding sentence could not be quoted |
| l8 | screens[3].options[0] | Dividing a six-month payoff by 6 spreads it evenly; the paper books it in the months earned, compounded | correct | course convention against the described paper method; the direction is stated as timing, not level |
| l8 | screens[3].options[1].why | The paper never divides by six; it measures each calendar month | unverified | as above |
| l8 | screens[4].prose | Adjacent cycles share five of six trading months, so their returns are correlated; a naive t ignores it; Newey-West with 5 lags allows for it | correct | overlapping 6-period returns sampled monthly have MA(5) errors, so 5 lags is the Hansen-Hodrick lag; r2 L2 (nw) reproduces 13.55 and 8.09 and (nw-mc) shows the naive t over-rejects under H0 |
| l8 | screens[4].options[1].why | The mean is the same in both; only its standard error changes | correct | HAC changes the covariance, not the point estimate |
| l8 | screens[4].options[2].why | Newey-West does not always halve t; it depends on the correlation | correct | r2 L2 (nw) |
| l8 | screens[4].explain | With the wait 11.09 becomes 6.91; Replicating Momentum uses the same correction | correct | r2 L2 (nw) |
| l8 | screens[5].explain | The denominator is pairs; dividing by shares halves the return | correct | each payoff is per pair of £1 a side |
| l8 | screens[6].options[0] | With every pair opened, committed and employed are equal | correct | n = k |
| l8 | screens[6].explain | This happens in 46 of 127 cycles for the top 20 | correct | numbers |
| l8 | screens[7].widget | `cycle_return` solution passes, starter fails | correct | r2 L2 (code) |
| l8 | screens[7].prose | The cycle is normalised once at `start` | correct | course convention, stated |
| l8 | screens[8].explain | 22 cycles at step 126 are a fair sample, not the full result; 1.05% against 1.00% | correct | numbers |
| l8 | screens[9].explain | £904,000 a cycle on £20m long and £20m short; what capital that needs depends on margin rules | correct | arithmetic; margin is outside the course |
| l8 | summary.ideas[2] | Adjacent cycles overlap by five months in six, so a naive t overstates the evidence | correct | r2 L2 (nw-mc) |
| l8 | quiz[1].options[2].why | Overlap leaves the mean unbiased | correct | expectation is linear; dependence affects variance only |
| l9 | screens[0].explain | A backtest that buys at a close printed at the bid pays the full spread less than a real buyer | correct | bid £49.75 against ask £50.25 is 1% of the mid |
| l9 | screens[1].explain | The extra day-to-day noise of the close spread is the bid-ask bounce; a same-day trade on closes buys that bounce | correct | Roll (1984); generator: iid ±0.5% each day |
| l9 | screens[2].explain | Closes 1.00%, mids 0.82%: about 0.19 points is bounce; the wait gives 0.75%, removing the bounce and giving up a day of each move | correct | numbers; r2 L2 (bounce) on fresh panels |
| l9 | screens[3].options[0] | Tomorrow's close is at bid or ask independently of today's, so the trade no longer buys today's bounce | correct | generator draws the side each day independently; r2 L2 (bounce): with the wait the closes-minus-mids gap vanishes |
| l9 | screens[3].options[1].why | The wait still trades at a close, a day later | correct | GGR wait-one-day rule |
| l9 | screens[3].options[2].why | The wait does not add costs; it changes which price is used | correct | same |
| l9 | screens[3].explain | It also gives up a day of convergence, so it is conservative | correct | numbers (mids: 0.82% to 0.75%) |
| l9 | screens[4].prose | Each round trip is four trades of £1 (open and close each leg); cost per pair per cycle = 4c × trips | correct | counting; GGR count round-trip costs on both legs |
| l9 | screens[5].explain | Break-even c* = gross / (4 × trips); the paper reports profits survive conservative cost estimates | correct | algebra; GGR abstract |
| l9 | screens[6].options[1].why | Every buy and every sell pays half the spread and a commission | correct | market microstructure |
| l9 | screens[6].explain | Charged once the cost looks harmless up to 4.52%; per trade it breaks even at 0.67%, about a seventh | correct | 4 × 1.69 = 6.75 trades |
| l9 | screens[7].explain | On mids the wait costs 0.07 points, the lost day; on closes 0.25 because it also removes the bounce; the two parts roughly add | correct | numbers; additivity is stated as "roughly" |
| l9 | screens[8].widget | `bounce_effect`, `net_of_costs`, `breakeven_cost` solution passes, starter fails | correct | r2 L2 (code) |
| l9 | screens[8].explain | On 22 cycles the wait run sits slightly above the mid run; on 127 slightly below; a sample of 22 moves the second decimal | correct | numbers |
| l9 | screens[9].options[0] | The wait-one-day rule addresses only the bounce, a spread effect | correct | GGR introduce the wait for the bid-ask bounce |
| l9 | screens[9].options[2].why | The borrow fee depends on holding time, not the fill price | correct | stock-loan economics |
| l9 | screens[9].explain | Commission, the half-spread on each real fill and the borrow fee must still be charged; a 0.12% stack leaves room under 0.67% | correct | arithmetic |
| l9 | quiz[1].options[0] | A close at the bid makes a share look cheap; buying it books the rebound to the mid | correct | Roll (1984) bounce |
| l10 | screens[0].prose | GGR report annualised excess returns of up to 11% for self-financing pairs portfolios | correct | abstract |
| l10 | screens[0].options[0] | Top 20, committed, one-day wait is the fairest cell to set beside the paper's 11% | misleading | the 11% headline is the fully invested (employed) top-20 one-day-wait figure: 0.895% a month is 10.7% simple and 11.3% compounded, while the committed one-day-wait figure is 0.52% a month, 6.4% a year (Table 1 transcription). The like-for-like cell is the course's employed-with-wait 0.84% (10.6%); setting committed beside an employed headline mixes the denominators l4 screens[5] warns about. r2 L2 (fair-cell). See finding |
| l10 | screens[0].options[1].why | Leading with the best cell flatters the match | correct | reporting practice |
| l10 | screens[0].options[3].why | Choosing the cell by closeness to the target is matching, not checking | correct | l10 screens[5] |
| l10 | screens[0].explain | 0.75% a month, 9.4% a year, sits inside the paper's "up to 11%" | misleading | as above: it sits inside because it is a smaller measure than the headline's |
| l10 | screens[1].explain | Three committed cells exceed 11% a year; each gap needs a reason, not a tweak | correct | numbers; the denominator caveat applies to the comparison |
| l10 | screens[2].options[0] | A match on a tuned, planted panel shows the code reproduces the method, not that the strategy works | correct | the panel's profit is designed in |
| l10 | screens[3].options | Real gap sources: monthly method, normalising once and carrying through, no delistings or dividends, 100-share universe; not the seed or the 2 sd rule | correct | "normalise once" as a difference from the paper agrees with Krauss (2017) and Rad, Low and Faff (2016) on re-normalisation; this is the row l2 quiz[1] contradicts |
| l10 | screens[3].explain | A small universe means fewer and odder pairs | correct | fewer candidates, so the 20th closest is further |
| l10 | screens[4].explain | Sampling one cycle in six moves the second decimal, so quote the full run | correct | numbers |
| l10 | screens[5].options[0] | Settings fitted to the target make the match prove nothing | correct | data snooping |
| l10 | screens[5].options[2].why | Reporting the best of several tries hides how many were tried | correct | multiple comparisons |
| l10 | screens[6].options[0] | State our top-5 over top-20 ordering as ours, without claiming the paper's | correct | GGR Table 1 in fact has top 20 above top 5 fully invested (1.436% against 1.308%), so not claiming is right |
| l10 | screens[6].explain | After the break the three surviving pairs average 2.7 of the top 5 places, so the top 5 hold up better | correct | numbers |
| l10 | screens[7].widget | `results_table` solution passes, starter fails | correct | r2 L2 (code) |
| l10 | screens[8].prose | Gap = ours − paper; compounding (1 + R_month)^12 − 1 is the shared yardstick | correct | course convention, stated |
| l10 | screens[9].options[0] | Lead with the conservative cell and every condition | correct | reporting practice; the sentence states committed and wait, so it is not misleading on its own |
| l10 | screens[9].options[2].why | Matching one range on data we built is not an exact replication | correct | honest |
| l10 | quiz[0] | The cell to set first beside the headline is committed with the wait | misleading | as screens[0] |
| review-2 | items[0] | Spread −0.032 beyond 0.030: buy i, sell j | correct | rule |
| review-2 | items[2] | Long leg −0.0455, short leg price fell 0.1000: payoff 0.0545 | correct | long return minus short return |
| review-2 | items[3].options[0] | Band exit books only part of each convergence, earns less and trades more | correct | numbers |
| review-2 | items[5].options[0] | Quote the Newey-West t | correct | r2 L2 (nw) |
| review-2 | items[5].options[2].why | t statistics apply to returns; they need the overlap correction | correct | standard |
| review-2 | items[8].options[0] | Check the code, list gap sources, report the gap | correct | replication practice |
| homework-2 | items[0] | `full_results` solution passes, starter fails | correct | r2 L2 (code) |
| homework-2 | items[0].explain | Four cells 1.37%, 1.01%, 1.00%, 0.75%; the wait lowers both portfolios | correct | numbers |
| homework-2 | items[1] | `blotter` solution passes, starter fails | correct | r2 L2 (code) |
| homework-2 | items[2].lines | Trade life: sd fixed in formation, signal at 2 sd, fill next day with the wait, hold to sign change or last day, close a day late with the wait, book long minus short | correct | GGR rule with the one-day wait on opening and closing |
| homework-2 | items[3].model | Waiting a day removes the bounce (fresh draw) and loses a day of convergence; the same-day figure answers a question no trader can act on | correct | r2 L2 (bounce) |
| homework-2 | items[3].model | The paper reports that waiting a day cuts returns materially but leaves them positive | correct | Table 1: top 20 1.436% to 0.895% a month |
| homework-2 | items[4] | Net = (4.52% − 4 × 0.2% × 1.69) / 6 = 0.53% a month | correct | arithmetic under the stated cost model |
| homework-2 | items[6].options[1].why | Each leg's return is p_out/p_in so the base cancels on the same trades; re-basing changes which trades open | correct | r2 L2 (rebase): payoff invariant for a fixed trade, trade set changes |
| homework-2 | items[6].options[0] | Dividing by 6 instead of compounding within months changes the figure even on the same trades | correct | different aggregation of the same payoffs |

## Level 3

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l11 | screens[0].explain | The 12-cycle mean drops at the break and never regains its level; 1.50% before, 0.64% after (same day); 1.14% and 0.48% with the wait | correct | numbers |
| l11 | screens[1].prose | GGR report lower profits in the later years of their sample | correct | GGR §4 (Do and Faff 2010 abstract: "continuing decline"; GGR note the 1990s decline) |
| l11 | screens[1].prose | Before = 55 cycles whose trading ends by day 1,512; after = 67 that start trading on it or later; the 5 straddling cycles are left out | correct | start + 378 <= 1512 gives starts 0 to 1,134 (55); start + 252 >= 1512 gives 1,260 to 2,646 (67) |
| l11 | screens[2].explain | Once 17 planted pairs break, chance pairs fill the ranking; the method still picks the closest 20 | correct | numbers; r2 L1 (chance-close) |
| l11 | screens[3].explain | Before the break 77% of trades close at a crossing, after it 54%; chance pairs open as readily but often never come back | correct | numbers; r2 L3 (conv-mc) |
| l11 | screens[4].prose | With `break_frac=0.3` and the same seed, 9 pairs break instead of 17 | correct | the uniform draws for `broken` are the same (same seed, same draws before them); numbers |
| l11 | screens[4].options[0] | Fewer breaks: the return still falls, by less | correct | numbers (1.07% against 0.64% after) |
| l11 | screens[4].options[1].why | The fall comes from the pairs that broke, not from the years | correct | generator: the only change at day 1,512 is the break |
| l11 | screens[5].options[0] | The share of opened trades that close at a crossing tells crowding from broken pairs | correct | r2 L3 (conv-mc): faster reversion leaves the crossing share up, a break cuts it |
| l11 | screens[5].options[1].why | Both stories predict a fall in returns, so the fall cannot choose | correct | logic |
| l11 | screens[5].options[2].why | Pairs are long one share and short another, so the market barely moves them | correct | l13 beta 0.053 |
| l11 | screens[5].explain | Do and Faff (2010) trace the continued decline to fewer pairs converging | unverified | Do and Faff (2010) abstract reachable (decline; strong in turbulence); the convergence attribution is my recollection of their §"Why" and could not be quoted |
| l11 | screens[6].explain | After the break an unbroken pair earns 10.45% a cycle, a chance pair 2.37%; the rule still works on pairs that co-move | correct | numbers |
| l11 | screens[7].widget | `planted_in_top`, `split_means` solution passes, starter fails | correct | r2 L3 (code) |
| l11 | screens[7].explain | A cycle that straddles the break belongs to neither half | correct | code conditions |
| l11 | screens[8].widget | `convergence_share` solution passes, starter fails; per trade, so a pair opening three times counts three times | correct | r2 L3 (code) |
| l11 | screens[9].prose | A fall in the crossing share c says pairs stopped co-moving, not that gaps closed faster | correct | r2 L3 (conv-mc), within the two stories the lesson sets |
| l11 | screens[9].explain | Waiting a day lowers both halves by a similar share (42% either way) | correct | numbers |
| l11 | screens[10].options[0] | Falling hit rate with steady trade count: test each pair's reversion and retire the broken | correct | consistent with screens[5] |
| l11 | screens[10].options[1].why | Broken pairs fail at any threshold | correct | a random-walk spread has no reversion to capture |
| l11 | quiz[1].options[2].why | A drop from 77% to 54% over 2,000 trades is far outside chance variation | correct | binomial se about 1 point; r2 L3 (conv-mc) |
| l11 | quiz[2].explain | The share counts trades, so a pair that opens twice counts twice | correct | definition |
| l12 | screens[0].explain | Pair (38, 39) ranks 2nd by distance with p = 0.2955; chance pair (28, 87) ranks 23rd with p = 0.0009; the two rules measure different things | correct | numbers; Engle-Granger tests residual stationarity, not closeness |
| l12 | screens[1].prose | Cointegration selection runs Engle-Granger on formation log prices and keeps the lowest p-values | correct | course definition; Vidyamurthy (2004) ch. 6 |
| l12 | screens[1].explain | One year of daily prices with a closing bounce is a small sample for the test; a real relationship can fail it | correct | r2 L3 (eg-power): planted pairs reject at 5% in about three quarters of fresh draws |
| l12 | screens[2].prose | GGR use distance alone | correct | GGR matching by SSD; no cointegration test in the paper |
| l12 | screens[2].explain | Before the break Engle-Granger swaps 10 planted pairs for chance pairs; after it both rules find the same 3 survivors | correct | numbers |
| l12 | screens[2].explain | "Over 22 cycles cointegration selection earns 0.63% a month against 1.05% for distance" | misleading | the 0.63% arm trades Engle-Granger picks with a residual z-score rule and a beta-pound hedge (`trade_coint`), the 1.05% arm trades distance picks with `trade_pair`; the number script computes it so. The gap mixes selection with trading rule and capital base, yet the sentence attributes it to selection. r2 L3 (confound): EG picks traded with `trade_pair` earn a different figure. See finding |
| l12 | screens[3].options[0] | Distance assumes equal normalised prices, a 1 to 1 hedge; Engle-Granger does not | correct | Engle and Granger (1987) estimate the cointegrating vector |
| l12 | screens[3].options[1].why | Both rules trade a spread they expect to revert; EG tests it, distance assumes it | correct | definitions |
| l12 | screens[3].options[3].why | Small gaps and rare trades are a consequence of distance, not an assumption | correct | l3 screens[7] |
| l12 | screens[3].explain | Engle-Granger allows any hedge ratio and a wide spread, if the spread is stationary | correct | cointegration definition |
| l12 | screens[4].prose | At 5%, each test of a non-cointegrated pair passes by chance one time in 20 | correct | definition of size, asymptotically; r2 L3 (eg-size) measures the finite-sample size |
| l12 | screens[4].explain | 4,950 × 0.05 = 247.5 expected chance passes | correct | linearity of expectation under the global null |
| l12 | screens[4].explain | The short year and the closing bounce lift the false-alarm rate to about 7%; 4,950 tests sharing 100 shares make one year's count swing widely | correct | r2 L3 (eg-size): size of statsmodels `coint` at n = 252 on random walks with a common market walk is 8% without and 10% with the ±0.5% bounce (600 reps), so "about 7%" is the right order; tests on shared shares are dependent |
| l12 | screens[5].options[0] | A formation p-value describes the formation year; it says nothing direct about the trading period | correct | tests condition on the sample |
| l12 | screens[5].options[2].why | A p-value is not the chance the relationship holds; it is the chance of so small a statistic if it does not | correct | definition (Casella and Berger §8.3.4) |
| l12 | screens[5].explain | The same holds for distance: both rules choose on the past | correct | both are formation-period statistics |
| l12 | screens[6] | ln L = 2 ln A + u: Engle-Granger finds a slope near 2; the SSD ranks far outside the top 20 | correct | r2 L3 (hedge-2); numbers (1.99, rank 177) |
| l12 | screens[6].feedback.byKey.half | Regressing A on L gives 0.5 | correct | reciprocal slope up to noise |
| l12 | screens[7].explain | Scaling a price adds a constant to its log, which the intercept absorbs, so normalised and raw prices give the same p-value | correct | `coint` fits a constant; r2 L3 (eg-scale) |
| l12 | screens[8].explain | At start 0, 18 of the shortlist's 30 chance pairs pass at 5%, not 2.5, because the shortlist was chosen for closeness on the same year | correct | numbers; r2 L3 (eg-select): choosing the closest pairs raises the pass rate of non-cointegrated pairs far above the nominal size |
| l12 | screens[9].prose | Each test of a pair picked blind passes by chance at its level alpha; expected passes = n × alpha | correct | definition |
| l12 | screens[10].options[0] | Shortlist on an economic link, test, confirm on a held-out year | correct | multiple-testing and out-of-sample practice |
| l12 | screens[10].options[2].why | Distance misses ETF pairs with hedges far from 1, such as a leveraged fund on its index | correct | screens[6]; leveraged ETF log price moves about beta times the index's, with volatility drag |
| l12 | screens[10].options[3].why | A low formation p-value is no promise for the trading period | correct | screens[5] |
| l12 | summary.ideas[1] | Over 22 cycles cointegration selection earns 0.63% a month against 1.05% | misleading | as screens[2].explain |
| l12 | quiz[1] | B's log price moves half as far as A's plus a stationary gap: Engle-Granger with hedge near 0.5 can select it; distance cannot ("halved moves make them drift apart") | correct | r2 L3 (hedge-2): slope 0.5 recovered; over 300 constructed years a 0.5-hedge pair sits inside the distance top-20 cut in 4%, a 2-hedge pair in 0%, so the rule holds up to a few quiet years |
| l12 | quiz[2].options[2].why | At start 1,260 Engle-Granger keeps 11 planted pairs that break the next day | correct | numbers |
| l13 | screens[0].explain | The least squares slope on 22 non-overlapping cycles is 0.053: the book's market beta | correct | numbers; r2 L3 (beta) |
| l13 | screens[1].prose | GGR find pairs returns are not explained by standard risk factors | correct | GGR Table 4: small, mostly insignificant factor exposures, alphas remain (Krauss 2017; student summary: "nearly factor-neutral") |
| l13 | screens[1].explain | Alpha 0.0623 a cycle, t = 7.11; beta 0.0529, t = 0.65; the market explains about 2% of the variation | correct | numbers; R^2 = t^2/(t^2 + 20) = 0.02 |
| l13 | screens[2].options[0] | Both legs carry the same market loading, so it cancels in each pair | correct | generator: every log price carries the one market walk; in log returns the market term cancels exactly, in simple returns up to second order; r2 L3 (beta) |
| l13 | screens[2].options[1].why | A rising market lifts both legs; long one and short the other, the rise cancels | correct | same |
| l13 | screens[2].options[2].why | Our pairs are open most of the time | correct | r2 L1 (open-share): 0.533 of pair-days |
| l13 | screens[2].options[3].why | Few points widen the error band; they do not pull the slope to 0 | correct | OLS is unbiased for any n |
| l13 | screens[3].prose | R_p = alpha + beta R_m + e; a small beta says the market moves the book little; alpha is the average return the market does not explain | correct | definitions |
| l13 | screens[3].explain | The prediction is an average; single cycles scatter widely | correct | residual sd is large relative to beta × 0.10 |
| l13 | screens[4].options[0] | Report 7.11 on the 22 non-overlapping cycles or a Newey-West t on all 127 | correct | r2 L2 (nw-mc) |
| l13 | screens[4].options[1].why | Overlapping cycles repeat five months in six, so plain OLS overstates t | correct | same |
| l13 | screens[4].options[2].why | Averaging a sound and an inflated figure is still inflated | correct | logic |
| l13 | screens[5].options[0] | A small beta shows only that the market factor explains little; other risks remain | correct | one regressor; the break is a pair-level risk invisible to it |
| l13 | screens[5].options[3].why | A t of 7.11 on 22 independent cycles is not luck; beta says nothing about that | correct | cycles at step 126 have disjoint trading windows; alpha and beta are separate |
| l13 | screens[5].explain | 24 of 127 waited cycles lost money, the worst −10.8% | correct | numbers |
| l13 | screens[6].prose | The paper also finds that pairs returns share a common latent factor | correct | GGR abstract and §5: profits linked to a common factor in pairs returns (ResearchGate abstract snippet) |
| l13 | screens[6].options[0] | Our panel plants no common factor, so its test cannot speak to the paper's real-data finding | correct | generator: pair gaps are independent across pairs |
| l13 | screens[6].options[2].why | A correlation of −0.12 on 22 cycles is well inside its noise | correct | se about 0.22 |
| l13 | screens[7] | Long £1 of A, short £0.60 of B, both loading 1: net industry exposure £0.40 | correct | linear exposure |
| l13 | screens[7].explain | Distance's 1 to 1 hedge cancels the industry factor; a cointegration hedge may not | correct | same arithmetic |
| l13 | screens[8].widget | `market_by_cycle` solution passes, starter fails; the market return must cover the same days as the pairs return | correct | r2 L3 (code); regression alignment |
| l13 | screens[9].widget | `pairs_alpha` solution passes, starter fails | correct | r2 L3 (code) |
| l13 | screens[9].explain | The wait lowers the alpha, not the market exposure | correct | numbers (betas 0.0529 and 0.0434) |
| l13 | screens[10].options[0] | Factor regressions plus the worst cycles answer the short-volatility and industry questions | correct | a factor loading needs a regression; tail behaviour needs the worst cycles |
| l13 | screens[10].options[2].why | A high Sharpe ratio is what a short-volatility book shows before its loss | correct | negatively skewed payoff profiles |
| l13 | quiz[1].options[2].why | Beta and alpha are separate coefficients | correct | OLS |
| l14 | screens[0] | 10 in-sample cycles end by day 1,512 (starts 0 to 1,134); 12 held-out cycles start trading on or after it (1,260 to 2,646) | correct | arithmetic |
| l14 | screens[1].explain | The best in-sample cell is 1.5 sd with k = 10: 1.97% a month; lower thresholds traded more and earned more in years 1 to 6 | correct | numbers |
| l14 | screens[2].explain | 28% survived; part of the fall is the break, part is having picked the luckiest cell | correct | r2 L3 (best-of): picking the max of noisy cells biases the in-sample figure up |
| l14 | screens[3].explain | The best of many in-sample results is partly the luckiest | correct | r2 L3 (best-of) |
| l14 | screens[4].explain | With the paper's rules unchanged 42% survived; no setting was tuned, so this is the headline | correct | numbers; no selection |
| l14 | screens[5].options[0] | Choosing on the held-out half makes it in sample again; the figure is the best of 12 tries | correct | data snooping |
| l14 | screens[5].options[2].why | More settings make the best one luckier still | correct | r2 L3 (best-of): bias grows with the number of cells |
| l14 | screens[5].options[3].why | Dropping the wait adds the bounce back | correct | l9 |
| l14 | screens[6].options[0] | A rise from 0.43% to 0.45% on 10 and 12 cycles is within chance | correct | cycle sd of several points a cycle; se of a 12-cycle mean is far above 0.02 points a month |
| l14 | screens[7].widget | `sweep` solution passes, starter fails; never touches a cycle that trades after the lock | correct | r2 L3 (code); condition start + 378 <= end_day |
| l14 | screens[8].widget | `held_out` solution passes, starter fails | correct | r2 L3 (code) |
| l14 | screens[9].prose | theta* = argmax of the in-sample mean, fixed before the held-out half is opened; survived = out/in at theta* | correct | protocol definition |
| l14 | screens[9].options[2].why | An average of the halves hides the decline | correct | logic |
| l14 | screens[10].options[2].why | A seeded result cannot speak for real markets | correct | generator |
| l14 | quiz[1].explain | Once held-out data has chosen a setting it no longer tests it; a fresh held-out period would be needed | correct | data snooping |
| l14 | quiz[2] | start + 378 <= 1,008 gives 6 cycles | correct | arithmetic |
| l15 | screens[0].explain | Top 5 with the wait: 69% survived against 42% for the top 20; the three unbroken pairs usually rank in the top 5 | correct | numbers |
| l15 | screens[1].explain | A line that turns planted-panel results into a claim about markets overclaims | correct | generator |
| l15 | screens[2] | 4.52%/6 = 0.753% a month; (1.0075)^12 − 1 = 9.4%; 0.48/1.14 = 42%; 4.52%/(4 × 1.6886) = 0.67% | correct | arithmetic |
| l15 | screens[3].options[0] | "About 42% of the waited top-20 return survived the planted break" names share, rules and data | correct | reporting |
| l15 | screens[4] | Real data adds delistings, dividends, borrow fees and recalls, varying spreads, breaks no seed imitates; the distance formula is the same; the wait still matters | correct | GGR data handling; l9 |
| l15 | screens[4].prose | 5,000 shares make 12,497,500 pairs, about 2,525 times 4,950 | correct | arithmetic |
| l15 | screens[5].options[0] | 1.50% stacks same-day fills, no costs and pre-break years | correct | numbers |
| l15 | screens[5].options[3].why | Committed capital is the conservative return; employed is higher | correct | k/n with positive total |
| l15 | screens[6].options[0] | A negative held-out mean reads "None of the effect survived" with the same prominence | correct | reporting; course convention stated |
| l15 | screens[8].widget | `survival_sentence` solution passes, starter fails; a zero in-sample mean raises | correct | r2 L3 (code) |
| l15 | screens[9].options[1].why | 9.4% is a pairs return, not a margin over the market | correct | self-financing payoff against a long-only return |
| l15 | quiz[1].options[0] | The code reproduces the method; real data is needed to test the strategy | correct | generator |
| review-3 | items[1].options[0] | Fewer pairs reach 2 sd, smaller gains, crossing share steady at 75%: crowding | correct | within the lesson's dichotomy; r2 L3 (conv-mc) |
| review-3 | items[2].explain | Pool the trades: 51/90 = 56.7%; averaging the shares weights the smaller cycle too heavily | correct | weighted against unweighted mean |
| review-3 | items[3] | 190 × 0.05 = 9.5 chance passes | correct | linearity |
| review-3 | items[4].options[1].why | Doubled moves pull the normalised prices apart in any year | correct | r2 L3 (hedge-2) |
| review-3 | items[5].options[0] | The shortlist was chosen on the same noisy year, so its chance pairs already look stationary | correct | r2 L3 (eg-select) |
| review-3 | items[5].options[1].why | The chance pairs are independent random walks by construction | correct | generator |
| review-3 | items[5].options[2].why | Engle-Granger can detect a half-life of 8 days; most planted pairs pass | correct | r2 L3 (eg-power) |
| review-3 | items[6].explain | 0.0623 + 0.0529 × 0.15 = 0.0702; almost all the return is alpha | correct | arithmetic |
| review-3 | items[7] | Long £1, short £1.25, both loading 1: net −£0.25 | correct | linear exposure |
| review-3 | items[8].options[3].why | No single rule earned the average of 12, so it reports no strategy | correct | logic |
| review-3 | items[9] | −0.03/1.20 negative: "None of the effect survived" | correct | course convention |
| homework-3 | items[0] (performance) | `compare_selection` solution passes, starter fails | correct | r2 L3 (code) |
| homework-3 | items[0].prose | "Compare the two selection rules": distance picks traded with `trade_pair`, Engle-Granger picks with `trade_coint` | misleading | the item itself says which rule trades which, but its explain and l12 report the result as a selection comparison; see l12 screens[2] finding |
| homework-3 | items[0].explain | With k = 5 at start 0 Engle-Granger's wider spreads earn 18.19% against 11.36% | misleading | same confound: the 18.19% is a different trading rule on a beta-pound hedge |
| homework-3 | items[1] | `rolling_hit_rate` solution passes, starter fails; a return of exactly 0 is not a hit | correct | r2 L3 (code) |
| homework-3 | items[2].lines | Lock, sweep in sample, choose, run once, report; rerunning on years 7 to 12 or moving the split breaks the protocol | correct | data-snooping logic |
| homework-3 | items[3] | (3 × 10.45% + 17 × 2.37%)/20 = 3.58%; the mix of pairs, not the rule, moved the return | correct | weighted mean; numbers |
| homework-3 | items[4] | 10 industries × 45 pairs × 0.05 = 22.5; restricting to an economic link cuts chance passes elevenfold | correct | 4,950/450 = 11 |
| homework-3 | items[5].options[0] | 22 non-overlapping cycles or 127 with Newey-West errors | correct | r2 L2 (nw-mc) |
| homework-3 | items[5].options[3].why | Choosing the sample after seeing it biases the estimate | correct | selection |
| homework-3 | items[6].model | Method, results, decline, alternatives, out of sample and real-data paragraph as in the lessons | correct | consistent with the ledger above; inherits the l10 and l12 findings ("sits inside the paper's up to 11%", "cointegration selection earns 0.63%") |
| homework-3 | items[6].model | "This matches Do and Faff (2010), who trace the decline to fewer pairs converging" | unverified | as l11 screens[5].explain |

## Verdict counts

Rows: 375. correct: 360, wrong: 0, imprecise: 2, misleading: 8, unverified: 5.
