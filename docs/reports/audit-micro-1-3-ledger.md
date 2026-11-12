# Claim ledger: micro (topic 1.7) L1 to L3 (concept audit, blind)

Scope: `app/content/courses/micro/` l1 to l12, review-1 to review-3, homework-1 to homework-3. One row per definition, result, method step, convention, always/never/every/only claim, causal claim, real-market claim, code-behaviour claim and the reasoning in each explain, why, hint and feedback line. Verdicts: correct, wrong, imprecise, misleading, unverified. `sim:` and `script:` point at checks in `docs/reports/micro-L1-3-concepts.py`; "KEYS" is its registry, which recomputes every numeric key, every numeric `wrong[]` value by the route its feedback names, and every table cell, and fails on any widget it does not cover.

Paths are JSON paths inside the named file; `s3` abbreviates `screens[3]`, `q1` `quiz[1]`, `i4` `items[4]`, `o2` `widget.options[2]`, `w.x` the `wrong[]` entry with id `x` and its `feedback.byKey.x` line, `fb` feedback, `ex` `explain.text`. `F n` is finding n of `docs/reviews/audit-micro-1-3.md`.

Sources: Harris, *Trading and Exchanges* (2003), cited as Harris with chapter: 4 orders, 6 order-driven markets, 11 order anticipators, 13 dealers, 14 bid/ask spreads, 19 liquidity, 21 transaction cost measurement. Hasbrouck, *Empirical Market Microstructure* (2007), cited as Hasbrouck: 5 sequential trade models, 14 trading costs. GM: Glosten and Milgrom (1985). AS: Avellaneda and Stoikov (2008). GK: Grinold and Kahn, *Active Portfolio Management*, ch. 16. Perold (1988). Amihud (2002). Bangia et al. (1999). Easley, Kiefer, O'Hara and Paperman (1996). Gould and Bonart (2016); Stoikov (2018). CFTC-SEC, *Findings Regarding the Market Events of May 6, 2010*. LSE, *Guide to the Trading System* (MIT201). MiFIR Art. 4 and 5; FCA COBS 11.2A; FCA FG12/13.

## Level 1

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l1 | s1 key, hints, fb, ex | A buy now trades with the cheapest waiting seller, the best ask, £100.14 | correct | Harris 4 (market orders take the best opposite quote) |
| l1 | s1.fb.byKey bid0..ask2 | Bids are buyers' prices; a buyer takes the cheapest ask first | correct | Harris 6 (price priority) |
| l1 | s2 key, ex | A sell now gets the best bid, £100.10 | correct | Harris 4 |
| l1 | s3.prose | Definitions: bid, ask, best bid, best ask, spread | correct | Harris 4, 14 |
| l1 | s3 key, w.lowest-bid, w.widest, w.pounds | Quoted spread = best ask minus best bid = 4p; 6, 8 and 0.04 by the named routes | correct | KEYS; Harris 14 |
| l1 | s3.ex | Levels further out do not set the spread | correct | definition |
| l1 | s4.prose | Mid is halfway between best bid and best ask, the usual one-number price | correct | Hasbrouck 14 (quote midpoint as benchmark) |
| l1 | s4 key, wrongs, ex | Mid £100.12; a buy pays 2p above it, a sell 2p below: half the spread each way | correct | KEYS; half-spread convention, Hasbrouck 14 |
| l1 | s5.prose | One basis point is 0.01%, 1/10,000; spreads are compared as a fraction of the mid | correct | definition |
| l1 | s5 key, w.percent, w.fraction, w.ten-times | 0.04/100.12 x 10,000 = 3.995; 0.04, 0.0004, 40 by the named routes | correct | KEYS |
| l1 | s5.ex | Near £100 a penny is about one basis point, only because of the price | correct | arithmetic |
| l1 | s6.prose | A book showing a bid resting above the ask would be crossed | correct | Harris 6 |
| l1 | s6 key, o.rests, o.rejected, o.own-price | A bid at £100.15 trades at once at the resting seller's £100.14; the limit is only a cap | correct | Harris 4 (marketable limit order), 6 (discriminatory pricing at standing prices) |
| l1 | s6.ex (first sentence) | On one exchange the best bid always sits below the best ask | imprecise | F 1. True in continuous trading only; an auction call shows a crossed book (LSE MIT201; l12 s0) |
| l1 | s6.ex | Locked means spread 0; a crossed screen is stale or merges venues | correct | Harris 6; consolidated quotes can lock or cross |
| l1 | s6.ex.canvas.caption | 300 trade at £100.14; 500 remain | correct | 800 - 300 |
| l1 | s7 key, whys, ex | A quote of £100.10 is the bid; a buyer of 200 pays £100.14 | correct | 800 shares at the ask cover 200 |
| l1 | s7.ex | A quote without a side is only half the story | correct | Harris 4 |
| l1 | s8.prose, key, ex | s = a - b, m = (a + b)/2, s_bp = 10,000 s/m; £50.05; about 20 bp | correct | script: l1 s8 |
| l1 | s9 key | Waiting traders hold out for a better price; who trades now pays the gap to who waited | correct | Harris 14 (spread as the price of immediacy; Demsetz 1968) |
| l1 | s9.o.fee.why | Exchange fees are separate and far smaller than the spread | unverified | F 4. Holds for the 4 bp spread shown; not for one-tick spreads (a 30 mil US access fee against a half-cent half-spread). Stated as general fact |
| l1 | s9.o.tick.why | The smallest step here is 1p, a tick; the spread is 4 ticks | correct | book shown |
| l1 | s9.hints, fb | The patient seller earned 4p more than selling now; immediacy has a price | correct | 100.14 - 100.10 |
| l1 | s9.ex | Firms that post both sides all day are market makers | correct | Harris 13 |
| l1 | s9.ex (last sentence) | The spread pays makers for the risk of trading with someone who knows more | imprecise | F 2. One of three components: order processing, inventory, adverse selection (Harris 14; Stoll 1978); l11 q0 says so itself |
| l1 | s10 key, wrongs, ex | 60 bp on £10,000 is £60; large-cap £2; £600, £2, £6 by the named routes | correct | KEYS; script: l1 s10 |
| l1 | summary.ideas, formula | Bids best (highest) first, asks best (lowest) first; buy pays ask, sell gets bid | correct | Harris 6 |
| l1 | summary.trap | A quoted price is usually the bid or the mid | unverified | F 3. Headline quotes are most often the last trade, or the mid; not established as stated |
| l1 | q0, q1, q2 | Mid £54.23; 20 bp; spread 6p, with 11p, 15p, 3p by the named routes | correct | KEYS; 54.26 - 54.15, 54.30 - 54.15 |
| l1 | q3 key, whys, ex | A crossed display on one exchange means stale or wrong data | imprecise | F 1. Right in continuous trading; in an auction call a crossed book is normal and the item does not say which |
| l2 | s0 key, slips, ex | A 1,500 buy takes 500, 600 and 400 of 700; the next best ask is £100.18 | correct | walk; 300 left at 100.18 |
| l2 | s1 key, whys, ex | Past 500 shares the average creeps up; £100.1622 at 1,800 | correct | script: l2 s1 |
| l2 | s1.ex | The more you buy at once, the worse your average | correct | monotone walk of an upward-sloping book |
| l2 | s2.prose | Market order walks the book; each trade is a fill | correct | Harris 4 |
| l2 | s2 table, fb, ex | 500, 600, 400; £50,070, £60,096, £40,072; £150,238 | correct | TABLES |
| l2 | s3 key, wrongs, ex | Average = cost / shares = £100.1587; plain mean £100.16 | correct | KEYS (volume-weighted average price) |
| l2 | s4.prose, key, wrongs | Slippage = average price minus a reference; 1.87p against the best ask; 4p, 0.0187, £28 by route | correct | KEYS; Harris 21 |
| l2 | s5 key, wrongs, ex | £58 against the mid = £30 half-spread + £28 walk; 3.9 bp | correct | KEYS; script: l2 s5 |
| l2 | s5.ex | The mid is the fairer benchmark: it does not ignore the spread | correct | Hasbrouck 14 (effective cost against the midpoint) |
| l2 | s6 key, whys | 1,800 fill; the last 200 wait, are cancelled or fill worse, by exchange | correct | Harris 4; venue rules differ |
| l2 | s6.ex | Never send a market order bigger than the book you can see | correct | advice, not a theorem; follows from the walk |
| l2 | s7 key, whys, ex | 600 shares average £100.1433; unweighted £100.15 overstates by 0.67p | correct | script: l2 s7 |
| l2 | s8.prose, key, whys | Weights q_i are the shares filled, not the size shown | correct | definition of VWAP |
| l2 | s9 code, hints, ex | `min(left, shares)` walks; raise before dividing when the book runs out | correct | script: code l2 s9 (solution passes 9, starter fails) |
| l2 | s10 key, wrongs, ex | Thin share: £1,800, 18 bp against 1 bp; £500, £100, £4,000 by route | correct | KEYS; script: l2 s10 |
| l2 | s10.ex | In a thin share the order's size sets the cost; large orders are split over time | correct | Harris 15, 19 |
| l2 | summary | Slippage against the mid is half the spread plus the walk | correct | s5 |
| l2 | q0..q2 | £100.14; £49.988; 1.2p; wrongs by route | correct | KEYS |
| l2 | q2.ex | For a sell, slippage is how far below the reference you sold | correct | sign convention, Harris 21 |
| l2 | q3 key, whys, ex | With a refilling book the three small buys pay £100.14 and save £28; real books do not refill free | correct | script: l2 q3 |
| l3 | s0 key, slips, ex | At one price the earliest order fills first; A and B fill, C nothing | correct | Harris 6 (time precedence) |
| l3 | s1.prose, key, ex | A limit buy below the ask rests; a new order joins the back of its price | correct | Harris 4, 6 |
| l3 | s2.prose | Price-time priority: better prices first, then earlier orders | correct | Harris 6 (primary and secondary precedence) |
| l3 | s2 key, wrongs | 1,300 shares must trade first | correct | KEYS |
| l3 | s3 key, wrongs | A cancel ahead moves you up: 700 | correct | KEYS |
| l3 | s3.ex | Cancels and fills ahead are the only things that move you forward | correct | time precedence; a size cut ahead is a partial cancel |
| l3 | s4 key, whys, hints | Raising the size sends the order to the back; size buys no priority | correct | LSE MIT201 (an increase in size loses time priority); CME, Nasdaq alike |
| l3 | s4.ex | Changing the price resets your place; cutting the size keeps it on most exchanges | correct | LSE MIT201; hedged "most" |
| l3 | s5 key, whys, ex | A 300 print fills A only; a trade at your price is not your fill | correct | time precedence |
| l3 | s6 key, wrongs, ex | A limit buy at or above the best ask is marketable and trades at the resting price | correct | Harris 4 |
| l3 | s7.prose | A resting buy fills after every better bid and every earlier bid at its price | correct | Harris 6 (displayed orders, price-time) |
| l3 | s7.prose, summary.formula | First fill after about n = Q/v trades; cancels shrink Q | correct | sim: l3 s7/s8 (mean 10.0 for Q/v = 10) |
| l3 | s7 key, whys, ex | Cutting size keeps the place; raising it or a new price starts at the back | correct | as s4 |
| l3 | s8 key, wrongs, ex | 20,000/2,000 = 10 trades; may never fill if the price lifts | correct | KEYS; non-execution risk, Harris 4 |
| l3 | s9.prose | Makers earn the spread when both sides fill; many pay for speed to be first at a new level | correct | Harris 13; Aquilina, Budish and O'Neill (2022) |
| l3 | s9 key, whys | The front fills first at the same price; no better price, no right to cancel others | correct | time precedence |
| l3 | s9.ex | Back orders often fill only when a big seller sweeps the level before a drop | correct | adverse selection of queue position, Harris 14; Glosten (1994) |
| l3 | s9.ex | Some futures venues match pro-rata, splitting each trade by size | correct | CME allocation algorithms; Harris 6 |
| l3 | summary, q0..q3 | 200 of Y fill (pro-rata 171); cut keeps place; sell limit £100.05 trades at £100.10; 4 trades | correct | KEYS |
| l4 | s0 key, whys, ex | Waiting saves 4p if it fills and may never fill: price against certainty | correct | Harris 4 (execution price uncertainty against execution uncertainty) |
| l4 | s1.prose, key, ex | Model: fill chance falls 0.1 a tick below the ask, a miss buys at £100.15; cost is lowest, 0p, at £100.10 and £100.09 | correct | script: l4 s1 (grid minimum at 4 and 5 ticks) |
| l4 | s1.ex | A limit far from the market rarely fills, so it is not free | correct | model; Harris 4 |
| l4 | s2.prose, table, ex | Market order buys now at the ask; limit names a price and waits; costs 2p and 0p | correct | TABLES; sim: l4 p = 0.6 |
| l4 | s3 key, wrongs, ex | p = 0.3 gives 1.5p; lower fill chance moves the cost towards the miss cost | correct | KEYS; sim: l4 p = 0.3 |
| l4 | s4 key, wrongs, ex | Break-even p = 0.2; above it the limit is cheaper on average | correct | KEYS; sim: l4 p = 0.2 gives 2.0p |
| l4 | s5 key, whys | With a miss of 8p and p = 0.5 the limit costs 3p against 2p | correct | sim: l4 p = 0.5, miss 8 |
| l4 | s5.ex | A bid tends to fill just as the price falls through it: adverse selection | correct | Harris 4, 14 (limit orders give a free option) |
| l4 | s6 key, fb.correct, ex | In a wide spread the mid is "the natural" limit | misleading | F 5. Not a standard result: any bid above £4.90 stands first (the item's own hint), and the best price is a fill-chance trade-off as in s1 (Harris 11 on quote matching) |
| l4 | s6.o.bid.why, o.market.why | Behind 2,000 shares you may wait all day; a market buy pays 2% for speed | correct | 10p on £5.00 |
| l4 | s6.ex | Some venues offer mid-point orders | correct | mid-point peg orders (LSE, Cboe) |
| l4 | s7.prose, key, whys | E[market] = h; E[limit] = -ph + (1 - p)(h + c); higher p favours the limit, higher c or smaller h does not | correct | derivative of the difference 2ph - (1 - p)c |
| l4 | s7.ex | Urgency, size and volatility raise c | correct | Harris 4 |
| l4 | s8 order, fb, ex | Limit cheaper when p > c/(2h + c); a big c pushes the threshold towards 1 | correct | script: l4 s8 (sympy) |
| l4 | s9.prose | The close is set in the 4.30 pm closing auction | correct | LSE closing auction call 16:30 to 16:35 |
| l4 | s9 key, whys, ex | Fund: closing auction or market orders; maker: passive quotes | correct | large c against small c in the model |
| l4 | summary | The limit wins when p > c/(2h + c); a far-away limit almost always misses | correct | s8 |
| l4 | q0, q2 | -1p; 1/6; wrongs by route; a wider spread lowers the bar | correct | KEYS |
| l4 | q1 key, whys, ex | A miss has a cost; resting orders are usually free to post | correct | Harris 4; "usually" hedges order-to-trade fees |
| l4 | q3.prose, o.limit.why, ex | A 2,000-share hedge of a position that loses £500 per 1p; "a single penny costs £500" against £40 of half-spread | imprecise | F 6. 2,000 shares offset £20 per 1p; £500 per 1p needs 50,000 shares. The comparison mixes two sizes |
| l4 | q3 key | Urgency: the market order fits | correct | large c in the model |
| r1 | i0 | A sell now gets the best bid, £20.00 | correct | 900 cover 100 |
| r1 | i1 | 53.3 bp; dividing by the bid gives 53.5 | correct | KEYS |
| r1 | i2, i3 | £20.0125; £18 = £8 half-spread + £10 walk | correct | KEYS |
| r1 | i4, i5 | 900 ahead after a 600 print; a 1,500 print leaves you behind 500 | correct | KEYS; time precedence |
| r1 | i6 | Expected cost -0.9p against 3p | correct | KEYS |
| r1 | i7 key, wrongs, ex | A sell limit at £20.00 sells 400 and 300, rests 200 as the new best ask | correct | KEYS; marketable limit, Harris 4 |
| h1 | i0 | 32.05 bp; 32.10 by the bid, 32.00 by the ask | correct | KEYS |
| h1 | i1 | £195 = £75 + £120; average £250.352; £260 if all 1,200 are sold | correct | KEYS; script: h1 i1 |
| h1 | i2 code, ex | Cost against the mid, positive when worse, both sides | correct | script: code h1 i2 |
| h1 | i3 key, w.old, w.walked, ex | 500 fill, 500 rest at £100.15 as best bid; spread 1p | correct | KEYS |
| h1 | i3.w.no-rest | "You dropped the unfilled 500 shares" for the value 2p | wrong | F 7. That route leaves bid 100.10, ask 100.16: 6p, the `walked` value. 2p comes from resting the remainder at the fill price, 100.14 |
| h1 | i4, i5 | 5 trades; raise and re-price go to the back, a cut does not | correct | KEYS; LSE MIT201 |
| h1 | i6 | E[limit] = h + c - 2ph - pc | correct | script: h1 i6 (sympy) |
| h1 | i7 order, ex | With a post-fill drift a, limit cheaper when p > c/(2h + c - a); 1/3 at h = 2, c = 1, a = 2 | correct | script: h1 i7; realised-spread idea, Hasbrouck 14 |
| h1 | i8 model (a) to (c) | £1,202,850, £20.0475, £2,850, 23.75 bp; £1,200; E = 0, range -£1,200 to +£1,800 | correct | script: h1 i8 |
| h1 | i8 model (d), rubric | Avoid one market order; passive early, cross before the deadline; optimism from adverse selection and impact | correct | Harris 4, 15 |

## Level 2

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l5 | s0, s1 | A round trip at the touch buys at the ask and sells at the bid: £4.00 on 100 shares | correct | KEYS |
| l5 | s2.prose, key, ex | Each side costs half the spread against the mid: 2.0 bp; round trip 4.0 bp | correct | KEYS; effective half-spread, Hasbrouck 14 |
| l5 | s3 key, wrongs, ex | £50,000 in and out costs about £19.98; about 499 shares | correct | KEYS |
| l5 | s4.prose | With 1p ticks no spread on this book can be narrower than one tick | correct | tick grid, Harris 4 |
| l5 | s4 key, whys, ex | A dark mid fill pays 0 bp against the mid; the ask is 1.0 bp above | correct | definition |
| l5 | s5 table, ex | A 4.0 bp, B 40 bp, C 8 bp; £1 per bp on £10,000 | correct | TABLES |
| l5 | s6 key, whys | A fill at the quoted ask costs 2p against the mid | correct | half-spread convention |
| l5 | s6.ex | A report that benchmarks against the quote you crossed always shows zero | correct | for a fill at that quote, by definition |
| l5 | s7 order, ex | Turnover T means selling TV and buying TV; annual cost TV s/m; 300% at 10 bp a trade is 60 bp | correct | derivation; standard turnover definition |
| l5 | s8 key, wrongs, ex | A 3 bp mid-price edge nets -1 bp after a 4 bp round trip | correct | KEYS |
| l5 | s8.ex | Resting orders that fill earn the spread | correct | Harris 14 |
| l5 | s9 key, wrongs, ex | £50,000 a day at 5 bp for 252 days: £6,300, 0.63% | correct | KEYS; 252-day convention stated |
| l5 | summary | Per side s/2m, round trip s/m, per year T s/m; measure from the mid | correct | s7 |
| l5 | q0..q3 | 0.6%; £160; 5 bp; 2.5 bp at one tick | correct | KEYS; script: l5 q1, q3 |
| l6 | s0, s1 | £10.016; 10 bp at 1,000 shares rising to 35 bp at 10,000 | correct | KEYS; script: l6 s1 |
| l6 | s2.prose | Slippage is the excess over the arrival mid: half-spread plus market impact | correct | Harris 21; Perold (1988) |
| l6 | s2 key, wrongs, ex | £100, 22 bp: 10 bp half-spread, 12 bp impact | correct | KEYS |
| l6 | s3 | A 200-share order pays the half-spread alone, 10 bp | correct | KEYS |
| l6 | s4.prose | Square-root model: impact = c sigma sqrt(Q/V), c near 1, fitted to many trades | correct | GK 16 (cost of a day's volume is a day's volatility); Almgren et al. (2005); Toth et al. (2011). Used as average cost per share |
| l6 | s4 key, wrongs, ex | 0.02 x sqrt(0.01) = 20 bp; 2, 200, 0.2 by route | correct | KEYS |
| l6 | s5 key, whys, ex | 4% costs 40 bp, not 80; total £ cost is eight times | correct | sqrt scaling; Q^(3/2) |
| l6 | s6.prose, key, ex | The part of the move that fades is temporary impact, the part that stays permanent: 3p and 3p | correct | KEYS; Almgren and Chriss (2000) |
| l6 | s6.ex | The permanent part is the market reading the buying as information | correct | Hasbrouck 5; Kyle (1985) |
| l6 | s7.prose | Impact costs 50/n bp "since smaller slices push less"; an hour of exposure is priced at 2 bp | imprecise | F 10. Declared a simple model, but the square-root rule taught at s4 gives 50/sqrt(n). The prose does not say the model has changed |
| l6 | s7 key, slips, ex | 50/n + 2n is smallest at n = 5: 20 bp; 52 bp for one block | correct | script: l6 s7 |
| l6 | s7.ex | Splitting trades impact for timing risk | correct | Almgren and Chriss (2000) |
| l6 | s8 order, ex | Implementation shortfall = execution cost + opportunity cost = paper P&L minus real P&L | correct | Perold (1988) |
| l6 | s9 key, wrongs, ex | £230 + £360 = £590, 59 bp; fills alone 33 bp | correct | KEYS; script: l6 s9 |
| l6 | s10 key, wrongs, ex | £5m at 10% of volume: 63 bp, about £31,600 | correct | KEYS |
| l6 | s11 code, ex | `impact_bps`, `shortfall`; shortfall can be negative | correct | script: code l6 s11 |
| l6 | summary | Impact grows like the square root of size; part fades, part stays | correct | s4 to s6 |
| l6 | q0.widget.answer, accept, fb.correct, ex | 500 at £20.00, £20.02 and £20.05 average "£20.030"; "£30,035 for 1,500 shares, £20.030 each" | wrong | F 8. 30,035/1,500 = 20.0233. The key marks the right answer wrong |
| l6 | q0.w.top, w.all-third | £20.00; £20.0278 when the third level is weighted by 800 | correct | KEYS (36,050/1,800) |
| l6 | q1 | 2% to 8% doubles impact: 60 bp; 42 bp is the sqrt(2) slip | correct | 30 x 1.414 = 42.4 |
| l6 | q2 key, whys, ex | Shortfall £50 + £3,000 is the honest cost | correct | Perold (1988) |
| l6 | q2.fb.correct | "£3,050 in all, 30.5 bp of £100,000" | wrong | F 9. 3,050/100,000 = 3.05% = 305 bp |
| l6 | q3 | 5 bp: half-spread, no impact | correct | KEYS |
| l7 | s0 key, whys, ex | With equal market-order flow the 1,000 ask empties before the 5,000 bid, so the mid most likely ticks up | correct | sim: l7 s0 (over 99%) |
| l7 | s1 key, whys, ex | The size-aware price leans towards the thin side | correct | definition below |
| l7 | s2.prose | Microprice (weighted mid) = (P_a Q_b + P_b Q_a)/(Q_a + Q_b): each price weighted by the other side's size | correct | Gatheral and Oomen (2010); Stoikov (2018) "weighted mid"; Cartea, Jaimungal and Penalva (2015) |
| l7 | s2 key, wrongs, ex | £100.1333, two thirds of the way from the mid to the ask | correct | KEYS |
| l7 | s3 key, wrongs | The ask lasts 2 s, the bid 10 s | correct | KEYS |
| l7 | s3.ex | The mid then rises to £100.125 | correct | (100.10 + 100.15)/2 |
| l7 | s3.ex (last sentence) | "The microprice prices that in ahead of time" | imprecise | F 11. The microprice is £100.1333, above the new mid £100.125: right direction, wrong size |
| l7 | s4 | Equal sizes give the mid | correct | KEYS |
| l7 | s5.prose, key, wrongs | Order imbalance I = (Q_b - Q_a)/(Q_b + Q_a), from -1 to +1; 0.667 | correct | KEYS; Gould and Bonart (2016) (queue imbalance) |
| l7 | s5.ex | Positive imbalance: the next mid move is more likely up | correct | sim: l7 s0; Gould and Bonart (2016) |
| l7 | s6 key, whys, ex | Own-side weights lean towards the heavy side, the wrong way | correct | sign of I |
| l7 | s7 order, ex | P_mu = m + I s/2; ask or bid at I = +1 or -1 | correct | script: l7 s7 (sympy) |
| l7 | s8 key, o.far, o.back, ex | The 100.11/100.15 quote is centred closest to £100.133 | correct | script: l7 s8 |
| l7 | s8.o.mid.why | "when fair value is £100.133" | imprecise | F 11. The microprice is a direction signal, not an established fair value (Stoikov 2018, sec. 2) |
| l7 | s9 code, ex | Both signals from the best level; None on a one-sided book | correct | script: code l7 s9 |
| l7 | s10 key, whys, ex | I = -0.8, microprice £100.104: a buyer with time waits | correct | script: l7 s10; follows from s5 |
| l7 | summary.ideas[1] | "so the microprice predicts the next mid better than the mid does" | imprecise | F 11. sim: true in a one-tick book (MSE 0.16 against 0.25), false in this lesson's 4p book (0.38 against 0.25; 0.83p miss against 0.50p) |
| l7 | summary.formula, trap | One-sided book has neither mid nor microprice; own-side weights reverse the lean | correct | definition |
| l7 | q0, q1, q2 | £50.01; £20.005; neither exists without an ask | correct | KEYS |
| l7 | q3 key, whys, ex | Across a day of quotes the microprice predicts the mid one second on better | imprecise | F 11. Supported for one-tick books (Gould and Bonart 2016); the item states no such condition |
| l8 | s0, s1 | Book B fills 2,000 at £100.02 (£30, 1.5 bp); book A costs £143, 7.1 bp | correct | KEYS; script: l8 s1 |
| l8 | s2.prose, key, wrongs, ex | Spread is the cost of a small trade; depth, the size near the touch, sets the cost of a large one; 700 against 7,000 | correct | KEYS; Harris 19 (width, depth, immediacy) |
| l8 | s3.prose | Volume refills the book quickly, so impact fades fast | correct | resiliency, Harris 19 |
| l8 | s3 key, whys, ex | X about 90 bp, Y about 17 bp | correct | script: l8 s3 |
| l8 | s4.prose, key, wrongs, ex | Amihud ratio = abs(r)/£ volume, averaged over days; bigger is less liquid; 0.04% per £1m | correct | KEYS; Amihud (2002) |
| l8 | s5 key, whys, ex | Q 0.025 beats P 0.05; volume alone misleads | correct | script: l8 s5 |
| l8 | s6.prose, ex, summary.ideas[2] | Spreads are wide after the open and tightest before the close; makers are unsure of the price at the open | correct | McInish and Wood (1992) for the open; declining intraday spreads on modern order books (LSE, Euronext) |
| l8 | s6 key, wrongs | £600 against £160: £440 | correct | KEYS |
| l8 | s7.prose, key, ex | In a crisis makers widen or step away; £4,000 against £400 | correct | KEYS; CFTC-SEC (2010) |
| l8 | s8.prose (second and third sentences) | A common rule caps trading at a fraction p of volume, often 10%; "Then the order adds little impact" | imprecise | F 12. The 10% rule is common; "little impact" contradicts l6 s10, where 10% of a day costs 63 bp |
| l8 | s8 order, ex | D = X/(pV); a cap of D_max days bounds X | correct | algebra; £20m at 10% of £50m is 4 days |
| l8 | s9 key, wrongs, ex | £2.4m; a £20m position would take 25 days | correct | KEYS |
| l8 | s10 key, whys, ex | Liquidity-adjusted VaR adds half the stressed spread plus impact and uses the exit horizon | correct | Bangia et al. (1999) |
| l8 | q0 | With no ask the spread is unbounded; a market buy cannot fill | correct | convention: a missing ask as plus infinity |
| l8 | q1, q2 | 0.04; 4 days | correct | KEYS |
| l8 | q3.prose | On 6 May 2010 US share prices "fell about 9% within minutes" | imprecise | F 13. CFTC-SEC (2010): indices already down over 4%, then a further 5% to 6% in minutes; 9% is the day's low against the prior close |
| l8 | q3.prose, key, whys, ex | Most of the fall was recovered within the half hour; some shares traded at a penny; volume was huge; depth vanished | correct | CFTC-SEC (2010), secs. I and II |
| r2 | i0..i4 | £50; £20.004; 6 bp; £6,000; 40 bp | correct | KEYS |
| r2 | i5.canvas.params.columns[2] | Column "Shares at the best bid" holds £ amounts (£15,000, £250,000) | imprecise | F 14. The explain reads them as £ depth ("200 times the depth") |
| r2 | i5 key, whys, ex | L: 2.5% of volume against 75% of K's | correct | script: r2 i5 |
| r2 | i6, i7, i8 | £9.995 and down; 3 days; shortfall -£20 | correct | KEYS |
| h2 | i0 | £600 + £8,000 = £8,600, 43 bp; impact thirteen times the spread cost | correct | TABLES; script: h2 i0 |
| h2 | i1 | Total sqrt-model cost grows like Q^(3/2); doubling costs 2.83 times | correct | script: h2 i1 |
| h2 | i2 | With Q_b = 3Q_a the microprice is (3a + b)/4 | correct | script: h2 i2 (sympy) |
| h2 | i3 | 42 bp; fills alone 19.2 bp | correct | KEYS |
| h2 | i4 | 72/n + 2n: n = 6, 24 bp; 24.4 and 24.3 either side | correct | script: h2 i4 |
| h2 | i5 | Amihud ranks R, S, T | correct | script: h2 i5 |
| h2 | i6 code, ex | Half the spread plus sqrt impact on the notional; £94,000; 2.5 days | correct | script: code h2 i6 |
| h2 | i7 | A market sell walks an emptied book; a limit caps the damage at the cost of not selling | correct | CFTC-SEC (2010); Harris 4 |
| h2 | i8 model (a), (b), (d) | £4,000; 90 bp, £90,000; 2.5 days | correct | script: h2 i8 |
| h2 | i8 model (c) | Three days: 52 bp each day, £52,000 in all, if each day's impact is temporary and fades overnight | correct | script: h2 i8; the hypothesis is stated |
| h2 | i8 model (c) | Timing-risk sd about £134,000 | correct | sim: h2 i8 (134k) |
| h2 | i8 model (e), (f), rubric | I = -0.6, £24.994, wait; measure by implementation shortfall | correct | script: h2 i8; Perold (1988) |

## Level 3

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l9 | s1 key, wrongs, ex | Selling at £5.02 and buying at £4.98 keeps the 4p spread: £4.00; each trade earns 2p against £5.00 | correct | KEYS |
| l9 | s2 key, whys, ex | Profit per minute peaks at 2p: £12.13, £14.72, £10.83, £1.35 | correct | script: l9 s2 |
| l9 | s3.prose | Half-spread s; arrivals lambda(s) = 10 e^(-0.5 s) a minute a side | correct | AS (2008), intensity A e^(-k delta) |
| l9 | s3.prose | The letter s, the whole spread in l1, l5 and l7, now means the half-spread | imprecise | F 15. Defined here, but the change from s = a - b is not flagged; l7's m + I s/2 and this level's V - s sit side by side |
| l9 | s3 key, wrongs, ex | £13.39 at 3p | correct | KEYS |
| l9 | s4 | A zero spread earns nothing however much it trades | correct | KEYS |
| l9 | s5 key, whys, ex | 10p earns £1.35 a minute against £14.72 | correct | script: l9 s2 |
| l9 | s6 | pi(s) = 2 s lambda(s); the 2 counts the two sides | correct | sim: l9 (Poisson) |
| l9 | s7 order, ex | pi'(s) = 2 lambda_0 e^(-ks)(1 - ks); peak at s* = 1/k; bigger k needs a tighter quote | correct | script: l9 s7 (sympy); AS (2008) as risk aversion tends to 0 |
| l9 | s8 code, ex | `expected_profit`; with k = 0 profit grows without limit | correct | script: code l9 s8 |
| l9 | s9.prose | Designated makers get lower fees for showing two-sided quotes for 90% of the day at a minimum size and maximum spread | correct | LSE registered market maker obligations (MIT201) |
| l9 | s9 key, whys, ex | A sell-only quote is not market making; every fill moves you from flat | correct | obligation as stated |
| l9 | s10 | 10,000 round trips of 1,000 shares at 1p: £100,000 gross | correct | KEYS |
| l9 | summary, q0..q3 | A round trip keeps 2s, one trade s; s* = 1/k; £30; £4; 4p; £12.13 | correct | KEYS |
| l10 | s0 key, whys, ex | Long 300: move both quotes down; a lower ask draws buyers, a lower bid deters sellers | correct | AS (2008) reservation price; Harris 13 |
| l10 | s1 key, whys, ex | Moving down d pence makes a sale e^d times as likely: 7.39 at 2p, about 55 at 4p | correct | script: l10 s1 |
| l10 | s2.prose | Skew: centre on m = V - gamma q | correct | AS (2008), r = s - q gamma sigma^2 (T - t) |
| l10 | s2, s3 keys, wrongs, ex | Ask 499p at q = +3; bid 500p at q = -2 | correct | KEYS |
| l10 | s4 key, whys, ex | At a position limit only the reducing side stays | correct | follows from the limit |
| l10 | s5.prose, chart | No-skew path ends at 14 and reaches 18; skewed path ends at 0, within 3 lots | correct | script: l10 s5 (series data) |
| l10 | s5 key, wrongs | 1,400 shares x 5p = £70 | correct | KEYS |
| l10 | s5.ex | Without a skew inventory is a random walk; with one it is pulled back | correct | sim: l10 s5 (sd 10 against about 1.1 after 100 trades) |
| l10 | s6 key, whys, ex | Short 3: quotes go up to 501p and 505p; skew against inventory | correct | m = 503 |
| l10 | s7.prose | Holding q for time tau adds variance q^2 sigma^2 tau; gamma = A sigma^2 tau in Avellaneda-Stoikov | correct | AS (2008), eq. for the reservation price |
| l10 | s7 key, whys, ex | Doubling sigma multiplies gamma by 4 | correct | sigma squared |
| l10 | s8 key, whys, ex | Short 2,000 calls: raise both call quotes; desks also hedge with the share | correct | same rule; Harris 13 |
| l10 | s9 table, ex | q runs 1, 2, 1, 0, -1; centre 499, 498, 499, 500, 501 | correct | TABLES |
| l10 | s10.prose | "Market makers cut such positions to zero before the 16:30 close" | imprecise | F 16. True of electronic makers (SEC Concept Release 2010; Menkveld 2013); stated of all makers |
| l10 | s10.prose | "Overnight the price often moves 2%" | unverified | F 16. A 2% close-to-open gap is a large move for a single share (overnight sd near 1%: French and Roll 1986; Lou, Polk and Skouras 2019), not a frequent one |
| l10 | s10 key, whys, ex | Flat before the close: overnight variance with no spread to earn; no rule forces it; a 2% gap on £10,000 is £200 | correct | script: l10 s10 |
| l10 | summary, q0..q3 | 799p; no skew at q = 0; a rebound is no more likely than a further fall; factor 9 | correct | KEYS; martingale fair value |
| l11 | s0 key, wrongs, ex | Selling at 502p a share worth 510p loses 8p: -£8.00; the half-spread is an edge only against the uninformed | correct | KEYS; GM (1985) |
| l11 | s1.prose, key, whys, ex | A share alpha informed, the rest random: average profit per buy s - alpha x 10; break-even 2p at alpha = 0.2 | correct | sim: l11 s5 |
| l11 | s2.prose | Adverse selection: losing to traders who know more | correct | Harris 14; Hasbrouck 5 |
| l11 | s2 key, slips, ex | Buy paths 1/10, 1/5, 1/5; one buy in five is informed | correct | sim: l11 s2 |
| l11 | s3 key, wrongs, ex | P(510p given buy) = 0.6 | correct | KEYS; sim: l11 s3; Bayes, GM (1985) |
| l11 | s4 key, wrongs | E[V given buy] = 502p | correct | KEYS; sim: l11 s4 |
| l11 | s4.prose, ex | A maker who sells at E[V given buy] makes nothing on average; fair value moves to 502p after the trade | correct | GM (1985): ask = E[V given buy], prices a martingale |
| l11 | s5 key, whys, ex | A buy at 502p earns £0.00 on average; in this model the whole spread pays for the informed | correct | sim: l11 s5 |
| l11 | s6 key, whys, ex | At alpha = 1 the break-even quotes are 490p and 510p and no one gains from trading | correct | GM (1985) market breakdown |
| l11 | s7.prose | ask = V + alpha delta, bid = V - alpha delta, s = alpha delta: the Glosten-Milgrom idea | correct | derivation s8; Hasbrouck 5 |
| l11 | s7 key, wrongs | 0.2 x 30 = 6p | correct | KEYS |
| l11 | s7.ex | Spreads widen before announcements (delta) and are wide in thin shares (alpha) | correct | Easley et al. (1996); Lee, Mucklow and Ready (1993) |
| l11 | s8 order, ex | P(informed given buy) = alpha; E[profit given buy] = s - alpha delta | correct | sim: l11 s2, s5 |
| l11 | s9.prose, key, whys | A multi-venue sweep is toxic flow: cancel, quote higher and wider; a fill then is the winner's curse | correct | Hasbrouck 5; Harris 14 |
| l11 | s9.ex | Makers pull quotes within microseconds | correct | Aquilina, Budish and O'Neill (2022): races last 5 to 10 millionths of a second |
| l11 | s9.ex, summary.trap | Waiting does not help; the informed trade when you do quote | correct | GM (1985): anonymous flow; read with s9's key (acting on a signal is not waiting) |
| l11 | s10 code, fb, ex | `maker_pnl` tends to s - alpha delta = 1p; seed 1 gives 0.9988 | correct | script: code l11 s10; sim: l11 s10 |
| l11 | q0 | At alpha = 0 the zero-profit spread is 0; real spreads stay positive from costs and inventory risk | correct | KEYS; Stoll (1978) |
| l11 | q1, q2 | 2p; E[V given sell] = 498p | correct | KEYS; sim: l11 q2 |
| l11 | q3 | In this model a thin share's wider spread means a larger alpha | correct | Easley et al. (1996); hedged "in this lesson's model" |
| l12 | s0.prose | At 16:30 continuous trading stops; orders are collected for five minutes; all matched shares trade at one price | correct | LSE MIT201 closing auction |
| l12 | s0 key, slips, ex | Volume at a price is the smaller side; 501p matches 1,200 | correct | script: l12 s0 |
| l12 | s1 key, whys, ex | Sellers limit volume at low prices, buyers at high; the peak is at the crossing | correct | min(D, S) |
| l12 | s2 key, wrongs | 300 buy shares unfilled | correct | KEYS |
| l12 | s2.ex | Bids above 501p fill in full; the 500 at 501p share 200 by time priority; the uncross maximises volume | correct | script: l12 s2; LSE MIT201 uncrossing |
| l12 | s3 table, s4 key, wrongs | Cumulative demand and supply; uncross 250p for 1,000 | correct | TABLES; script: l12 s4 |
| l12 | s5 key, whys, ex | No overlap: no price; orders stay in the book | correct | script: l12 s5 |
| l12 | s6.prose, s8.prose (dark pool line) | A dark pool's hidden orders "match at the lit market's mid" | imprecise | F 18. True of UK and EU reference-price pools (MiFIR Art. 4(1)(a)); US pools also match at other prices inside the quote |
| l12 | s6 key, wrongs, ex | Saving 1p a share, £200; a lit order this size would walk past £5.01; dark pools hide size | correct | KEYS |
| l12 | s7 key, whys, ex | A mid fill saves the half-spread; a missed fill can cost more; dark pools are regulated under MiFID II and the EU caps dark volume | correct | MiFIR Art. 4 and 5 (volume cap) |
| l12 | s8.prose | Lit: visible book, price-time; auction: p* = argmax min(D, S); internaliser fills clients itself, US payment for order flow; brokers owe best execution | correct | FCA COBS 11.2A; SEC Rule 606 |
| l12 | s8 key, whys | A smart order router splits a buy across venues | correct | Harris 6; routing practice |
| l12 | s8.ex (last sentence) | Reading every venue and splitting each order "is what best execution requires" | imprecise | F 19. The duty is all sufficient steps for the best possible result on price, cost, speed and likelihood (COBS 11.2A.2R); it does not require splitting |
| l12 | s9.prose, key, whys, ex | £20m is 10% of the day and 40% of the close; slice most of it, put a modest share in the close; index funds use the close | correct | script: l12 s9 |
| l12 | s10 table, ex | L, D, A, I; UK rules ban payment for order flow | correct | FCA FG12/13 |
| l12 | summary, q0 | The official close is the auction's uncross price, not the last trade | correct | LSE MIT201 |
| l12 | q1, q3 | 101p; £12.42 | correct | KEYS |
| l12 | q2 key, whys, ex | Publishing an auction imbalance draws in offsetting orders | correct | Nasdaq and NYSE imbalance feeds; stated as this exchange's practice |
| r3 | i0, i1 | £40; bid 1,199p | correct | KEYS |
| r3 | i2 key, o.b.why, ex | "Informed traders cannot be told apart from the rest"; "an informed order looks like any other until the price moves" | imprecise | F 17. Absolute; l11 s9 teaches that a sweep marks likely informed flow and that pulling quotes is right |
| r3 | i3, i4 | Opens at 102p; s* = 3p | correct | KEYS |
| r3 | i5 key, wrongs, ex | Two independent buys: P(510) = 9/13, E[V] = 503.85p | correct | KEYS; sim: r3 i5 |
| r3 | i6, i7, i8 | £150; factor 2; -1p a trade, widen to 3p | correct | KEYS; sim: r3 i8 |
| h3 | i0 | 58.86p at s* = 4p | correct | KEYS |
| h3 | i1 order, ex | pi = 2 lambda_0 e^(-ks)(s - alpha delta); s* = alpha delta + 1/k = 4p | correct | script: h3 i1 (sympy) |
| h3 | i2 | At the limit only the ask, 1,995p | correct | KEYS |
| h3 | i3 | Three buys: 27/35, 505.43p; steps 2p, 1.85p, 1.58p | correct | KEYS; sim: h3 i3 |
| h3 | i4.prose, code | Uncross: most volume, then smallest surplus, then lowest price | correct | script: code h3 i4; agrees with an independent reference on 3,000 random books |
| h3 | i4.fb.correct | The function "breaks ties the exchange's way" | imprecise | F 20. After volume and surplus, exchanges use market pressure and a reference price (LSE MIT201), not the lowest price |
| h3 | i5 | A 300-share market buy moves the uncross to 502p | correct | script: h3 i5 |
| h3 | i6 key, whys, ex | A wholesaler internalises and pays for retail flow because it is rarely informed; brokers still owe best execution | correct | Harris 14; SEC Rule 606; Easley, Kiefer and O'Hara (1996) |
| h3 | i7 model, rubric | Half-spread 8p before results, 6p a trade lost at 2p; skew to flat, closing auction; sweep is toxic; spread is not pure profit | correct | script: h3 i7; l10, l11 |
| h3 | i8 model (a) | a = alpha delta/(alpha + 2(1 - alpha) beta), b with 1 - beta | correct | script: h3 i8 (sympy); sim: h3 i8 |
| h3 | i8 model (b), (c) | At beta = 1/2 both are alpha delta; a = 3p, b = 7p; P(informed given sell) = 1/3, given buy 1/7 | correct | sim: h3 i8; `micro-3-perf-numbers.py` |
| h3 | i8 model (d), rubric | Symmetric quotes earn 1.2p on a buy, lose 2.8p on a sell, 0 overall; a rival undercuts the ask | correct | sim: h3 i8 (d); GM (1985) zero profit per side |
