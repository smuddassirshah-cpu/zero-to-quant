# Claim ledger: micro L1 to L3, round 2 blind audit

Auditor: Fable, blind (no earlier review, audit, report or ledger for this course opened before the WIP commit). Stage 1, full ledger depth. Date 12 Nov 2026.

Path shorthand: `sN` is `screens[N]`, `qN` is `quiz[N]`, `iN` is `items[N]`, `opt.x` is `widget.options[id=x]`, `wrong.x` is `widget.wrong[id=x]` with its `feedback.byKey.x`. A row that names several paths covers lines that state the same step; each was read and checked against the same derivation. "Derivation" means I recomputed the figure by hand from the item's own data; "script" means `docs/reports/micro-L1-3-r2-concepts.py` (exit 0, CPython 3.13.18).

Verdicts: `correct`, `wrong`, `imprecise`, `misleading`, `unverified`.

Named sources used: Harris, *Trading and Exchanges* (2003), ch. 4 (orders), 6 (order-driven markets), 13 to 14 (dealers, bid/ask spreads), 21 (transaction cost measurement); Perold (1988), "The implementation shortfall"; Grinold and Kahn, *Active Portfolio Management*, ch. 16 (square-root cost); Tóth et al. (2011), "Anomalous price impact", Phys. Rev. X; Amihud (2002), "Illiquidity and stock returns"; Kyle (1985); Glosten and Milgrom (1985); Avellaneda and Stoikov (2008), "High-frequency trading in a limit order book"; Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (2015), ch. 3, 4 and 10; Gould and Bonart (2016), "Queue imbalance as a one-tick-ahead price predictor"; Easley, Kiefer, O'Hara and Paperman (1996); Lee, Mucklow and Ready (1993); Bangia et al. (1999), "Liquidity on the outside"; CFTC-SEC (30 Sep 2010), *Findings regarding the market events of May 6, 2010*; LSE *Guide to the Trading System* (MIT201); MiFID II Art. 27 and MiFIR; FCA FG12/13 (payment for order flow).

## l1-bids-and-asks

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l1 | s1 prose, hints, explain | Buyers name a size and the most they pay; a buy now trades with the cheapest waiting seller, £100.14 | correct | Harris ch. 4; book data: lowest ask 100.14 × 800 |
| l1 | s1 feedback.byKey bid0..ask2 | Bids are buyers' prices; dearer asks fill only after cheaper ones | correct | Price priority, Harris ch. 6 |
| l1 | s2 answer bid0, explain, byKey | A sell now gets the highest bid, £100.10 | correct | Book data |
| l1 | s3 prose | Definitions of bid, ask, best bid, best ask, spread | correct | Harris ch. 4 |
| l1 | s3 answer 4, explain | Spread = best ask − best bid = 4p; outer levels do not set it | correct | 100.14 − 100.10 |
| l1 | s3 wrong.lowest-bid 6, wrong.widest 8, wrong.pounds 0.04 | Slip values and their named mistakes | correct | 100.14 − 100.08 = 0.06; 100.16 − 100.08 = 0.08; £0.04 |
| l1 | s4 prose | Mid is halfway between best bid and best ask; "the usual one-number answer" | correct | Definition; the summary trap notes a quote may also be bid or last trade |
| l1 | s4 answer 100.12, wrongs half-spread, sum, bid, ask | (100.10 + 100.14)/2; slips 0.02, 200.24, 100.10, 100.14 | correct | Derivation |
| l1 | s4 explain | A buy now pays 2p over the mid, a sell gets 2p under: half the spread each way | correct | Derivation |
| l1 | s5 prose | Spread is quoted relative to the mid in basis points; 1 bp = 0.01% = 1/10,000 | correct | Convention; Harris ch. 14 (relative spread) |
| l1 | s5 answer 4.0, hints, explain | 0.04/100.12 × 10,000 = 3.995 | correct | Script; derivation |
| l1 | s5 wrong.percent 0.04, fraction 0.0004, ten-times 40 | 0.03995% (and £0.04); 0.0003995; ×100,000 | correct | Derivation; tolerances do not overlap the key |
| l1 | s5 explain | "Near £100 a penny is about one basis point, but only because of where the price is" | correct | 0.01/100 = 1 bp |
| l1 | s6 prose, opt.match, hints | A bid at or above the best ask trades at once at the resting seller's price | correct | Marketable limit order, Harris ch. 4 |
| l1 | s6 opt.rests, opt.rejected, opt.own-price why | Exchange matches at once; such a bid is allowed; trade price is the resting price, not the limit | correct | Harris ch. 6 (discriminatory pricing rule of continuous books) |
| l1 | s6 explain; q3 explain, opts | In continuous trading on one exchange best bid < best ask; locked = spread 0, crossed = bid above ask; a crossed display is stale or consolidated | correct | Definitions; holds for continuous trading, which the text states |
| l1 | s6 explain caption | 300 trade at £100.14; 500 remain | correct | 800 − 300 |
| l1 | s7 all | Quote of £100.10 is the bid; a buyer pays £100.14; nobody sells at the mid | correct | Book data |
| l1 | s8 prose | s = a − b, m = (a + b)/2, s_bp = 10,000 s/m | correct | Definitions |
| l1 | s8 answer, opts, explain | Mid £50.05; half-spread £0.05; spread about 20 bp | correct | 0.10/50.05 × 10,000 = 19.98 |
| l1 | s9 opt.patience, hints, feedback | Patient traders hold out for a better price; the impatient pay the gap to them | correct | Harris ch. 14 (price of immediacy; Demsetz 1968) |
| l1 | s9 opt.fee why | Exchange fees are separate; the gap goes to whoever posted the order | correct | Harris ch. 14 |
| l1 | s9 opt.tick why | Tick here is 1p; this spread is 4 ticks | correct | Book prices move in 0.01 |
| l1 | s9 explain | Market makers post both sides; the spread pays for costs and risks including adverse selection | correct | Harris ch. 14 (spread components) |
| l1 | s10 prose | 2p on £100.00 is 2 bp; 6p on £10.00 is 60 bp | correct | Derivation |
| l1 | s10 answer 60, wrongs per-pound 600, large 2, pence 6 | 1,000 shares × 6p; 10,000 × 6p; 100 × 2p; 100 × 6p | correct | Derivation |
| l1 | s10 explain, feedback.correct | £60 against £2, thirty times | correct | 60/2 |
| l1 | summary ideas, formula, trap | Restate the above | correct | As above |
| l1 | q0 answer, wrongs, explain | Mid £54.23; half 0.03; spread 0.06 | correct | Derivation |
| l1 | q1 answer 20, wrongs pence 4, percent 0.2 | 0.04/20.00 = 20 bp = 0.2% | correct | Derivation |
| l1 | q2 opts | 6p; 11p = 54.26 − 54.15; 15p = 54.30 − 54.15; 3p half | correct | Derivation |

## l2-walking-the-book

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l2 | s0 answer, hints, wrong sets, explain | 1,500 needs 500 + 600 + 400 of 700; next best ask is £100.18 | correct | Book data; 300 remain at 100.18 |
| l2 | s1 canvas caption, opts, explain | Average rises a little with each extra 100 past 500; £100.1622 at 1,800 | correct | 180,292/1,800 = 100.16222 |
| l2 | s2 prose | Market order walks the book; each trade is a fill | correct | Harris ch. 4 |
| l2 | s2 table keys, byKey | 500, 600, 400; £50,070, £60,096, £40,072 | correct | Derivation; total £150,238 |
| l2 | s3 answer 100.1587, wrongs unweighted 100.16, best, last | 150,238/1,500 = 100.15867; plain mean of three prices is 100.16 | correct | Script |
| l2 | s3 explain | Each price counts in proportion to the shares bought there | correct | Volume-weighted average definition |
| l2 | s4 prose | Slippage = average price minus a reference price | correct | Harris ch. 21 |
| l2 | s4 answer 1.87, wrongs last-level 4, pounds 0.0187, total 28 | 100.15867 − 100.14 = 1.867p; 4p; £0.0187; £28 | correct | Script; 0.018667 × 1,500 = 28.0 |
| l2 | s5 answer 58, wrongs best-ask 28, half-only 30, per-share 0.0387 | 150,238 − 150,180; splits £30 + £28 | correct | Script |
| l2 | s5 explain | About 3.9 bp; the mid is the fairer benchmark because it does not ignore the spread | correct | 58/150,180 = 3.86 bp; Harris ch. 21 (quote midpoint benchmark) |
| l2 | s6 opts, explain | 1,800 fill; the rest waits, is cancelled or fills worse, depending on the venue | correct | Venue rules differ (LSE MIT201 market order handling); hedged in text |
| l2 | s6 explain | "Never send a market order bigger than the book you can see" | correct | Advice, follows from the screen |
| l2 | s7 answer, opts, hints, explain | 60,086/600 = 100.1433; a sixth of the way up; unweighted overstates by 0.67p | correct | Derivation |
| l2 | s8 prose, opts, explain | p̄ = Σq_i p_i / Σq_i with q_i the shares filled, not the size shown | correct | Definition |
| l2 | s9 code solution, tests, how, feedback | `min(left, shares)` walk; raises when the book is short; 9 tests | correct | Ran in CPython: solution 9/9, starter 0/9 |
| l2 | s9 explain | Dividing by `size` is valid only once every share is filled | correct | Code reading |
| l2 | s10 prose | Liquid share: 10,000 at £100.01 costs £100 over a £100.00 mid | correct | 10,000 × 0.01 |
| l2 | s10 answer 1800, hints, wrongs half-spread 500, liquid 100, worst 4000 | Fills cost £1,001,800 | correct | Script |
| l2 | s10 explain | 18 bp against 1 bp; this is why large orders are split over time | correct | Derivation; Harris ch. 15 |
| l2 | summary | Restates | correct | As above |
| l2 | q0 | 300 fit in 500 at £100.14; slip 100.15 | correct | Derivation |
| l2 | q1 answer 49.988, wrongs | (400 × 50.00 + 600 × 49.98)/1,000 | correct | Derivation |
| l2 | q2 answer 1.2, wrongs level-gap 2, total 12 | 50.00 − 49.988 = 1.2p; sell-side sign convention stated | correct | Derivation |
| l2 | q3 opts, explain | Y pays £100.14 if the book refills; saves £28; real books do not refill for free | correct | Derivation; hedge stated |

## l3-the-queue

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l3 | s0 answer, wrong sets, explain | 900 shares fill A (300) then B (600); C gets nothing | correct | Time priority, Harris ch. 6 |
| l3 | s1 prose, answer, explain | A limit order names a worst price and waits; a new order joins the back; 1,300 ahead | correct | Harris ch. 4, 6 |
| l3 | s2 prose | Price-time priority; queue position | correct | Harris ch. 6 |
| l3 | s2 answer 1300, wrongs 0, 200, 1500 | 300 + 600 + 400 | correct | Derivation |
| l3 | s3 answer 700, wrongs | 300 + 400 after B cancels | correct | Derivation |
| l3 | s3 explain | "Cancels ahead of you, and fills, are the only things that move you forward" | correct | Under price-time priority; a size cut ahead is a partial cancel |
| l3 | s4 opts, hints, explain; s7 opts, explain; q1 | Raising size or changing price loses time priority; cutting size keeps it on most exchanges | correct | LSE MIT201 (order modification), CME and Nasdaq rules; hedged "most exchanges" |
| l3 | s5 opts, explain | A 300-share print fills A only; 1,000 still ahead | correct | Derivation |
| l3 | s6 answer 100.14, wrongs limit, bid, explain | A buy limit at or above the best ask is marketable and trades at the resting price | correct | Harris ch. 4 |
| l3 | s7 prose | n ≈ Q/v trades to the first fill; cancels shrink Q | correct | Derivation; stated as approximate |
| l3 | s7 opt.price why | At £100.11 you would be first but pay a penny more and lose your old place | correct | No bid at 100.11 in this book |
| l3 | s8 answer 10, wrongs inverse 0.1, next 1, explain | 20,000/2,000; may never fill if the price moves away | correct | Derivation |
| l3 | s9 prose | Market makers earn the spread when both sides fill; many spend heavily on speed to be first in line | correct | Budish, Cramton and Shim (2015); Yao and Ye (2018) on queue priority |
| l3 | s9 opts, explain | The front gets earlier fills, not better prices; back orders often fill only on sweeps before a drop; some futures venues match pro-rata | correct | Moallemi and Yuan (2017), value of queue position; CME pro-rata algorithms |
| l3 | summary | Restates | correct | As above |
| l3 | q0 answer 200, wrongs all 500, none 0, prorata 171 | 1,200 − 1,000; pro-rata share 1,200 × 500/3,500 = 171.4 | correct | Derivation |
| l3 | q2 | Sell limit at £100.05 trades at the £100.10 bid | correct | Marketable limit |
| l3 | q3 answer 4, wrong no-cancel 6 | (9,000 − 3,000)/1,500 | correct | Derivation |

## l4-market-or-limit

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l4 | s0 opts, hints, explain | Waiting saves 4p if it fills but may not fill; price against certainty | correct | Harris ch. 4 (execution uncertainty); 100.14 − 100.10 |
| l4 | s1 prose, canvas, opts, explain | Model: fill chance falls 0.1 per tick below the ask, a miss costs 3p; expected cost 2.0p at the ask, 0.0p at £100.10 and £100.09, 1.2p at £100.06, 3.0p at £100.04 | correct | Script reproduces the canvas expression |
| l4 | s2 prose, table keys, byKey, explain | Market 2p; limit 0.6 × (−2) + 0.4 × 3 = 0; saves 2p on average | correct | Derivation; the model's numbers are stated as a model |
| l4 | s3 answer 1.5, wrongs old 0, fill-only −0.6, miss-only 2.1 | 0.3 × (−2) + 0.7 × 3 | correct | Derivation |
| l4 | s4 answer 0.2, wrongs half, bid-chance, third | −2p + 3(1 − p) = 2 gives p = 0.2; dropping −2p gives 1/3 | correct | Derivation |
| l4 | s5 prose, opts, hints | Six ticks to £100.20, 8p over the mid; 0.5 × (−2) + 0.5 × 8 = 3p against 2p | correct | Derivation |
| l4 | s5 explain | A bid tends to fill just as the price falls through it: adverse selection | correct | Harris ch. 4 and 14; Glosten (1994) |
| l4 | s6 prose | 10p over a £5.00 mid is 2% | correct | Derivation |
| l4 | s6 opts, hints, explain | In a wide spread a patient buyer bids inside the gap; any bid above £4.90 is first in a new line; the mid is a natural choice; some venues offer mid-point peg orders | correct | Price priority; peg orders exist (for example Nasdaq midpoint peg). "Natural" is advice, hedged in the explain |
| l4 | s7 prose, opts, explain | E[market] = h; E[limit] = −ph + (1 − p)(h + c); h = 2, c = 1; higher p helps the limit, higher c and smaller h hurt it | correct | Advantage of the limit is 2ph − (1 − p)c, rising in p and h, falling in c |
| l4 | s7 explain | Urgency, size and volatility all raise c | correct | Reasoned from the model; Harris ch. 4 |
| l4 | s8 lines, hints, feedback, explain | p > c/(2h + c); 1/5 with h = 2, c = 1; a big miss cost pushes the threshold towards 1 | correct | Script; algebra checked line by line |
| l4 | s9 prose, opts, explain | An index fund benchmarked to the close has a large miss cost and uses the closing auction; a market maker posts passive quotes | correct | LSE closing auction 16:30 to 16:35 (MIT201); Harris ch. 13 |
| l4 | summary | Restates | correct | As above |
| l4 | q0 answer −1, wrongs | 0.8 × (−2) + 0.2 × 3 | correct | Derivation |
| l4 | q1 opts, explain | A miss has a cost when the shares are needed; resting orders are usually free to post | correct | Exchange tariffs charge on execution (LSE Trading Services Price List); "usually" is hedged |
| l4 | q2 answer 0.1667, wrongs h-c 0.2857, over-h 0.4, explain | 2/12; 2/7; 2/5; a wider spread lowers the bar | correct | Derivation |
| l4 | q3 opts, explain | Half-spread £40 on 2,000 shares; a minute risks about £200; break-even 10/14, about 0.7 | correct | Derivation |

## review-1

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| review-1 | i0 | A sell now gets the best bid £20.00; 900 shares cover 100 | correct | Book data |
| review-1 | i1 answer 53.3, wrongs pence, bid 53.5, percent | 0.04/7.50; 0.04/7.48 = 53.48; 0.533%; "more than 13 times" 4 bp | correct | Derivation; slip tolerance [53.46, 53.54] clear of the key's [53.2, 53.4] |
| review-1 | i2 answer 20.0125, wrongs | 16,010/800; five-eighths of the way | correct | Derivation |
| review-1 | i3 answer 18, wrongs best-ask 10, half 8 | 16,010 − 800 × 19.99 | correct | Derivation |
| review-1 | i4 answer 900, wrongs | 1,500 − 600 | correct | Derivation |
| review-1 | i5 opts, explain | Front order takes all 1,500 and keeps 500 | correct | Time priority |
| review-1 | i6 answer −0.9, wrongs | 0.7 × (−3) + 0.3 × 4 | correct | Derivation |
| review-1 | i7 answer 200, wrongs, explain | 400 + 300 trade; £19.99 is below the limit; 200 rest as best ask | correct | Derivation; asks start at 20.08 |

## homework-1

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| homework-1 | i0 answer 32.05, wrongs bid 32.1, ask 32.0, percent, pence | 0.04/12.48 = 32.051; /12.46 = 32.103; /12.50 = 32.000 | correct | Derivation; tolerance windows do not overlap |
| homework-1 | i1 answer 195, wrongs best-bid 120, half 75, all-levels 260, explain | £625,880 received; mid £250.43; average £250.352 | correct | Derivation: 200,320 + 250,350 + 175,210; 3,000-share variant gives 751,290 − 751,030 = 260 |
| homework-1 | i2 code, tests, feedback test-2, test-6, explain | Cost against the mid for either side; sell 1,500 costs £37 | correct | Ran in CPython: solution 9/9, starter 0/9; 150,180 − 150,143 |
| homework-1 | i3 answer 1, wrongs old 4, walked 6, no-rest 2, explain | 500 fill at £100.14; 500 rest at £100.15; ask £100.16 | correct | Derivation |
| homework-1 | i4 answer 5, wrongs 7.5, 10 | (12,000 − 4,000)/1,600 | correct | Derivation |
| homework-1 | i5 multi keys, whys | Raise size and change price go to the back; cut and a cancel ahead do not | correct | As l3 s4 |
| homework-1 | i6 answer, accepts, wrongs | h + c − 2ph − pc | correct | Algebra |
| homework-1 | i6 explain | "Each extra point of fill chance cuts the cost by 2h + c" | imprecise | dE/dp = −(2h + c) per unit of p; a "point" of chance reads as 0.01, which cuts the cost by 0.01(2h + c). Finding 5 |
| homework-1 | i7 lines, explain | p > c/(2h + c − a); 1/3 with h = 2, c = 1, a = 2; no fill chance suffices if a ≥ 2h + c | correct | Script; algebra |
| homework-1 | i8 model (a) | 200,200 + 300,450 + 401,000 + 301,200 = 1,202,850; £20.0475; £2,850; 23.75 bp | correct | Derivation |
| homework-1 | i8 model (b), (c) | £1,200, 10 bp, assumes the book refills; limit plan 0p expected, range +£1,200 to −£1,800 | correct | Derivation |
| homework-1 | i8 model (d), rubric | More than twice the sliced cost (2.375 times); break-even 1/5; adverse selection and impact as caveats | correct | Derivation; l4 model |

## l5-crossing-the-spread

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l5 | s0 answer, byKey, explain | A buy lifts the ask (£100.14), a sell hits the bid (£100.10) | correct | Book data; Harris ch. 4 |
| l5 | s1 answer 4.0, wrongs half 2, per-share 0.04, zero, pence 400, explain | Round trip loses the whole spread: 100 × £0.04 | correct | Derivation |
| l5 | s2 prose | Each side costs half the spread against the mid: the half-spread | correct | Harris ch. 21 (effective half-spread) |
| l5 | s2 answer 2.0, wrongs full 4.0, percent 0.02, explain | 0.02/100.12 × 10,000 = 1.998 | correct | Derivation |
| l5 | s3 answer 19.98, accept window, wrongs once 9.99, percent 2000, per-share 0.04, explain | 50,000 × 0.04/100.12 = 19.976; about 499 shares | correct | Derivation |
| l5 | s4 prose | 1p ticks, so no quoted spread narrower than £50.00/£50.01; mid £50.005; 2.0 bp | correct | 0.01/50.005 = 1.9998 bp |
| l5 | s4 opts, explain | A fill at the mid costs 0 bp against the mid; the cheapest lit buy is 1.0 bp over; mid-point venues go under the tick floor | correct | Derivation; midpoint dark pools (l12) |
| l5 | s5 table keys, hints, explain | A 4.0 bp/£4; B 40 bp/£40; C 8 bp/£8; £1 per bp on £10,000 | correct | 0.04/100.12, 0.04/10.00, 0.20/250.00 |
| l5 | s6 opts, feedback, explain | A buy at the ask costs 2p against the mid; a report benchmarked on the crossed quote shows zero | correct | Harris ch. 21 |
| l5 | s7 lines, explain | Turnover T means selling TV and buying TV; annual cost 2TV × s/(2m) = TV s/m; 300% at 10 bp a trade is 60 bp | correct | Turnover as the lesser of purchases and sales over assets (SEC Form N-1A convention); derivation |
| l5 | s8 prose caption | 1p on £25.005 is 4.0 bp | correct | 3.9992 bp |
| l5 | s8 answer −1, wrongs ignored 3, half 1, double −5, added 7, explain | 3 − 4; resting orders that fill earn the spread | correct | Derivation |
| l5 | s9 answer 6300, wrongs once 3150, full 12600, day 25, explain | 50,000 × 0.0005 × 252; 0.63% of £1m | correct | Derivation; 252 trading days stated |
| l5 | summary | per side s/(2m), round trip s/m, per year T s/m | correct | As s7 |
| l5 | q0 opts | 3 × 2 × 10 = 60 bp; 0.3%, 0.1%, 6% slips | correct | Derivation |
| l5 | q1 answer 160, wrongs once 80, pence 800 | 80 bp of £20,000; 4,000 shares × 4p; 20,000 × 4p = £800 | correct | Derivation |
| l5 | q2 answer 5, wrongs | 10p/£200 | correct | Derivation |
| l5 | q3 opts, explain | Half a tick is 2.5 bp of £20.005; quotes sit on the tick grid | correct | 0.005/20.005 = 2.4994 bp |

## l6-impact

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l6 | s0 answer 10.016, wrongs top, simple 10.015, last, explain | 25,040/2,500; 1.6p over the mid | correct | Script |
| l6 | s1 canvas, opts, explain | Cost over the mid rises from 10 bp at 1,000 to 35 bp at 10,000; slower than the order grows | correct | Script (walk gives 35 bp) |
| l6 | s2 prose | Slippage is the extra over the arrival mid; half-spread plus market impact (own order pushing the price paid) | correct | Harris ch. 21; consistent with l2's "reference price" |
| l6 | s2 answer 100, wrongs top 45, last 135, pence 10000, explain | 1,000 + 3,000 + 6,000 pence; 22 bp = 10 bp half-spread + 12 bp impact | correct | Script; 100/45,000 = 22.2 bp |
| l6 | s3 answer 10, wrongs none, full 20, pence 1, explain | 1p on £10.00; no impact inside the touch | correct | Derivation |
| l6 | s4 prose | Square-root model: impact ≈ c σ √(Q/V), σ daily volatility, V daily volume, c near 1, fitted to many trades | correct | Grinold and Kahn ch. 16; Tóth et al. (2011) (prefactor of order one). Used here as the average cost per share, the Grinold-Kahn convention |
| l6 | s4 answer 20, wrongs no-root 2, root-of-one 200, percent 0.2, explain | 0.02 × √0.01 = 0.002 | correct | Script |
| l6 | s5 opts, explain | Four times the size is twice the impact per share (40 bp); 320 bp squares the ratio; total £ cost is eight times | correct | √4 = 2; 20 × 16 = 320; 4 × 2 = 8 |
| l6 | s6 prose, answer 3, wrongs, explain | Temporary impact fades, permanent stays; 6p rise, settles 3p up; permanent part read as information | correct | Script (series); Almgren and Chriss (2000); Kyle (1985) |
| l6 | s7 prose, slider key 5, wrong ranges, hints, explain | Toy model 50/n + 2n, flagged as not the square-root rule; minimum at n = 5, 20 bp; 52 bp at n = 1 | correct | Script; AM-GM: minimum where 50/n = 2n |
| l6 | s8 prose, lines, explain | Implementation shortfall = Σq_i(p_i − p_d) + (N − Σq_i)(p_c − p_d) = paper P&L − real P&L | correct | Perold (1988); N(p_c − p_d) − Σq_i(p_c − p_i) expands to the two terms |
| l6 | s9 answer 590, wrongs filled-only 230, missed-only 360, all-close 1200, explain | 80 + 150 + 360; 59 bp of £100,000; 33 bp on fills alone | correct | 230/70,000 = 32.9 bp |
| l6 | s10 answer 31623, wrongs linear 100000, no-root 10000, bp 63.2, explain | 0.02 × √0.1 = 0.0063246 of £5m | correct | Script |
| l6 | s10 explain | "This is why large funds split orders over days" | correct | Smaller Q/V per day in the same model; Harris ch. 15 |
| l6 | s11 code, tests, explain | `impact_bps`, `shortfall`; shortfall can be negative when the price falls | correct | Ran in CPython: 12/12, starter 0/12 |
| l6 | summary | Restates | correct | As above |
| l6 | q0 answer 20.0233, wrongs top, all-third 20.0278 | 30,035/1,500; 36,050/1,800 | correct | Derivation |
| l6 | q1 opts | 30 × √4 = 60; 42 is 30 × √2 | correct | Derivation |
| l6 | q2 opts, explain | £50 + 15,000 × 20p = £3,050, 305 bp of £100,000 | correct | Derivation |
| l6 | q3 answer 5, wrongs | 2p/£40.00 | correct | Derivation |

## l7-where-is-the-price

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l7 | s0 opts, hints, explain | With equal market-order flow the thin ask (1,000) empties before the bid (5,000), so the mid most likely moves up | correct | Script (hit rate 0.87 and 0.83 in two queue models); Gould and Bonart (2016) |
| l7 | s1 canvas, opts, explain | The size-weighted dot leans towards the thin side | correct | Formula in the canvas |
| l7 | s2 prose | Microprice, also called the weighted mid: (P_a Q_b + P_b Q_a)/(Q_a + Q_b) | correct | Cartea, Jaimungal and Penalva ch. 3 (microprice); Gatheral and Oomen (2010) (weighted mid) |
| l7 | s2 answer 100.1333, wrongs mid, same-side 100.1067, explain | 600,800/6,000; two thirds of the way from mid to ask | correct | Derivation |
| l7 | s3 answer 2, wrongs bid 10, both 12 | 1,000/500 | correct | Derivation |
| l7 | s3 explain | Next ask £100.15, mid rises to £100.125; the microprice £100.133 overshoots that move | correct | (100.10 + 100.15)/2; overshoot stated |
| l7 | s4 answer, wrongs, explain | Equal sizes give the mid | correct | Formula |
| l7 | s5 prose, answer 0.6667, wrongs reversed, no-divide 4000, ratio 5 | I = (Q_b − Q_a)/(Q_b + Q_a) in [−1, 1] | correct | Cartea, Jaimungal and Penalva (order imbalance); derivation |
| l7 | s5 explain | Positive imbalance: next mid move more likely up | correct | Script; Gould and Bonart (2016) |
| l7 | s6 opts, explain | Own-side weights give £100.107 and get the lean backwards | correct | Derivation; script on direction |
| l7 | s7 lines, explain | P_μ = m + I s/2; equals the ask or bid at I = ±1 | correct | Algebra |
| l7 | s8 opts, explain | Quote centres 100.13, 100.12, 100.14, 100.11; closest to 100.133 is £100.11/£100.15 | correct | Derivation |
| l7 | s9 code, tests | `microprice`, `imbalance`, `None` for a one-sided book | correct | Ran in CPython: 10/10; starter passes only the two `None` tests |
| l7 | s9 explain | "Dividing would then crash or mislead" on an empty side | imprecise | Without the guard the failure is `IndexError` at `asks[0]`; nothing is divided (script INFO line). Finding 1 |
| l7 | s10 opts, explain | I = −0.8, P_μ = 100.104; a buyer waits for the likely down-tick; saves a fraction of the spread over many slices | correct | Derivation; Cartea, Donnelly and Jaimungal (2018), "Enhancing trading strategies with order book signals" |
| l7 | summary ideas[1]; q3 opts, explain | In a one-tick book the microprice predicts the mid after its next move better than the mid; the shift I s/2 never exceeds the half-tick move | correct | Script: MSE 0.55 and 0.59 against 1.00 (half-ticks squared); |I| ≤ 1 |
| l7 | q0 answer 50.01, wrongs mid 50.02, own 50.03 | (50.04 × 2,000 + 50.00 × 6,000)/8,000 | correct | Derivation |
| l7 | q1 opts | 20.00 + 0.5 × 0.01 | correct | Derivation |
| l7 | q2 opts, explain | A one-sided book has no mid and no microprice | correct | Both formulas need P_a |

## l8-liquidity

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l8 | s0 prose, answer, explain | Both mids £100.005; book B fills 2,000 at £100.02; book A walks to £100.10 | correct | Script |
| l8 | s1 answer 143, wrongs spread 10, top-level 1.5, pence 14300, explain | 150 + 1,800 + 12,350 pence; 7.1 bp against 1.5 bp | correct | Script; 143/200,010 = 7.15 bp |
| l8 | s2 prose | Spread is the cost of a small trade; depth is the size offered near the touch | correct | Kyle (1985) tightness and depth; Harris ch. 19 |
| l8 | s2 answer 700, wrongs 300, 2700, 1200, explain | 300 + 400; book B offers 7,000 within 5p | correct | Derivation |
| l8 | s3 prose | "Heavy trading refills the book quickly, so impact fades fast" | correct | Foucault, Kadan and Kandel (2005): resiliency rises with order arrival rates |
| l8 | s3 opts, hints, explain | X about 90 bp, Y about 17 bp | correct | Script |
| l8 | s4 prose, answer 0.04, wrongs negative, inverse 25, times 36, decimal 0.0004, explain | Amihud ratio |r|/volume, bigger is less liquid; averaged over many days in practice | correct | Amihud (2002), eq. 1 (daily average of |r|/volume) |
| l8 | s5 opts, explain | P 0.05, Q 0.025 % per £1m | correct | Derivation |
| l8 | s6 prose, answer 440, wrongs half 220, open-only 600, bp 8.8 | 500,000 × 8.8 bp; £600 against £160 | correct | Derivation; the prose describes the chart shown |
| l8 | s6 explain | After the open makers are unsure of the price and quote wide; later the price is known | unverified | Plausible price-discovery account; the general intraday pattern differs by market (McInish and Wood (1992) found NYSE spreads widen again at the close). No source for London is cited |
| l8 | s7 prose, answer 4000, wrongs calm 400, half 2000, explain | 40 bp of £1m; makers widen or step away in a crisis | correct | Derivation; CFTC-SEC (2010) report |
| l8 | s8 prose | "A common rule is to trade at most a fraction p of daily volume, often 10%" | unverified | Participation caps are standard; the "often 10%" figure is unsourced |
| l8 | s8 lines, explain | D = X/(pV); cap X ≤ D_max pV; 20/5 = 4 days | correct | Derivation |
| l8 | s9 answer 2.4, wrongs one-day 0.8, no-p 24, divide 0.267, explain | 3 × 0.1 × 8; £20m would take 25 days | correct | Derivation |
| l8 | s10 opts, explain | Liquidity-adjusted VaR adds half the stressed spread plus impact and uses the exit horizon | correct | Bangia et al. (1999) |
| l8 | summary ideas[0] | Three dimensions: spread, depth, "volume (how fast the book refills)" | imprecise | The standard third dimension is resiliency (Kyle 1985); volume is a proxy for it, and the lesson's own trap shows volume alone misleads. Finding 8 |
| l8 | summary ideas[2] | "wide after the open, tight before the close" as a general pattern | unverified | As s6: true of the chart; unsourced as a general statement |
| l8 | q0 opts, explain | No ask: no finite spread | correct | Definition |
| l8 | q1 answer 0.04, wrongs | 0.6/15 | correct | Derivation |
| l8 | q2 answer 4, wrongs no-p 0.4, times 100 | 20/(0.1 × 50) | correct | Derivation |
| l8 | q3 prose, opts, explain | 6 May 2010: indices already down about 4%, fell a further 5% to 6% in minutes, recovered most within the half hour; some shares traded at a penny; volume was huge; depth vanished | correct | CFTC-SEC (2010), executive summary |

## review-2

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| review-2 | i0 answer 50, wrongs once 25, percent 5000 | 6p/£30.00 = 20 bp of £25,000 | correct | Derivation |
| review-2 | i1 answer 20.004, wrongs mid, own 20.016, explain | (20.02 × 800 + 20.00 × 3,200)/4,000; I = −0.6 | correct | Derivation |
| review-2 | i2 answer 6, wrongs top 4, last 10, simple 6.67, explain | 18,000p/6,000 = 3p on £50.00; 4 bp is half-spread | correct | Derivation |
| review-2 | i3 answer 6000, wrongs no-root 1200, bp 30 | 0.015 × √0.04 = 0.003 of £2m | correct | Derivation |
| review-2 | i4 answer 40, wrongs once 20, double 80 | 5 turnovers × 8 bp | correct | l5 s7 |
| review-2 | i5 opts, explain | 75% of K's volume against 2.5% of L's; 200 times K's depth | correct | 3/4, 3/120, 3,000,000/15,000 |
| review-2 | i6 opts | 10.00 − 0.5 × 0.01 = 9.995 | correct | Derivation |
| review-2 | i7 answer 3, wrongs no-p 0.6, ten 6 | 12/(0.2 × 20) | correct | Derivation |
| review-2 | i8 answer −20, wrongs filled-only 180, sign 380, sign2 20, explain | 3,000 × 6p − 2,000 × 10p | correct | Perold (1988); derivation |

## homework-2

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| homework-2 | i0 table keys, explain | £600 + £8,000 = £8,600, 43 bp; impact thirteen times the spread cost | correct | 3 bp and 0.02 × √0.04 of £2m; 8,000/600 = 13.3 |
| homework-2 | i1 lines, explain | Total impact cost = (cσ/√V) Q^{3/2}; doubling Q multiplies it by 2.83 | correct | Algebra |
| homework-2 | i2 answer, accepts, wrongs, explain | (3a + b)/4; I = 1/2 | correct | Algebra |
| homework-2 | i3 answer 42, wrongs filled-only 19.2, fills-on-paper 12, explain | (1,200 + 3,000)/1,000,000 | correct | 1,200/625,000 = 19.2 bp; 1,200/1,000,000 = 12 bp |
| homework-2 | i4 table keys, explain | n = 6, 24 bp; 24.4 at five, 24.3 at seven | correct | Script |
| homework-2 | i5 opts, explain | R 0.020, S 0.030, T 0.060 | correct | Derivation |
| homework-2 | i6 code, tests, explain | `estimate_cost`, `days_to_exit`; £94,000; 2.5 days | correct | Ran in CPython: 10/10, starter 0/10 |
| homework-2 | i7 opts, explain | A market sell walks far down an emptied book; a limit caps the damage at the cost of not selling | correct | l2, l8; CFTC-SEC (2010) |
| homework-2 | i8 model (a), (b) | £4,000; 0.018 × 0.5 = 90 bp, £90,000 | correct | Derivation |
| homework-2 | i8 model (c) | 0.018 × √(1/12) = 52 bp, about £52,000, if each day's impact fades overnight; risk sd about £134,000 | correct | Script (134,024 simulated against 134,164 exact) |
| homework-2 | i8 model (d), (e), (f), rubric | 2.5 days; I = −0.6, P_μ = £24.994; implementation shortfall against £25.00 | correct | Derivation |

## l9-both-sides

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l9 | s1 answer 4.0, wrongs one-side 2.0, per-share 0.04, half 0.02, explain | Sell 100 at £5.02, buy 100 at £4.98: £4.00; each trade earns 2p a share against fair value | correct | Derivation |
| l9 | s2 canvas, opts, explain | Profit 20x e^{−0.5x} £ a minute: £12.13 at 1p, £14.72 at 2p, £10.83 at 4p (1.35 trades), £1.35 at 10p (0.07 trades) | correct | 20e^{−0.5}, 40e^{−1}, 80e^{−2}, 200e^{−5} |
| l9 | s3 prose | λ(s) = 10e^{−0.5s} a side; s is now the half-spread, a change from earlier lessons, said in the text | correct | Avellaneda and Stoikov (2008), exponential arrival intensity |
| l9 | s3 answer 13.39, wrongs one-side 6.69, full-spread 26.78, per-share 0.1339, no-fall 60, explain | 2 × 2.2313 × £3 | correct | Derivation |
| l9 | s4 answer 0, wrongs trades 20, ten 10, explain | Quoting at fair value earns nothing however busy | correct | 2 × 0 × 10 |
| l9 | s5 opts, hints, explain | 2 × 10 × 0.0674 = £1.35 against £14.72 | correct | Derivation |
| l9 | s6 prose, opts, explain | π(s) = 2sλ_0 e^{−ks}; the 2 counts the two sides | correct | Definition of the model |
| l9 | s7 lines, explain | π'(s) = 2λ_0 e^{−ks}(1 − ks); unique peak at s* = 1/k; bigger k needs a tighter quote | correct | Calculus; script grid search |
| l9 | s8 code, tests, explain | `expected_profit`; with k = 0 profit grows without limit (60p at 3p) | correct | Ran in CPython: 9/9, starter 0/9 |
| l9 | s9 prose, opts, explain | A designated market maker owes a bid and an ask; a one-sided quote is a directional position; the other bid is 12p below the ask | correct | LSE market maker obligations (MIT201; MiFID II RTS 8); 5.02 − 4.90 |
| l9 | s9 explain | "Exchanges pay market makers to stay two-sided precisely when it is uncomfortable" | correct | MiFID II RTS 8 Art. 6 (incentives in stressed market conditions) |
| l9 | s10 answer 100000, wrongs half 50000, no-shares 100, pence 10000000, explain | 10,000 × 1,000 × 1p, before fees, technology and staff | correct | Derivation |
| l9 | summary | Restates | correct | As above |
| l9 | q0 answer 30, wrongs | 6p × 500 | correct | Derivation |
| l9 | q1 answer 4, wrongs spread 8, zero, explain | One trade earns s against fair value; the short carries price risk | correct | 2p × 200 |
| l9 | q2 opts | s* = 1/0.25 = 4p | correct | s7 |
| l9 | q3 answer 12.13, wrongs one-side 6.07, no-fall 20 | 2 × 1 × 6.065 | correct | Derivation |

## l10-inventory

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l10 | s0 opts, hints, explain | Long inventory: move both quotes down; widening does not tilt the next trade | correct | Ho and Stoll (1981); Avellaneda and Stoikov (2008) |
| l10 | s1 prose, canvas, opts, explain | With rates 10e^{−0.5x}, a shift down of d makes a sale e^d times as likely: 7.39 at 2p, about 55 at 4p (ask 498p) | correct | e^{−0.5(2−d)}/e^{−0.5(2+d)} = e^d; e^4 = 54.6 |
| l10 | s2 prose | Skew; centre m = V − γq, q in lots | correct | Avellaneda and Stoikov reservation price, linear in q |
| l10 | s2 answer 499, wrongs wrong-way 505, no-skew 502, mid 497, bid 495, explain | m = 497; gives up 1p a share on the sale | correct | Derivation |
| l10 | s3 answer 500, wrongs wrong-way 496, no-skew 498, mid 502, explain | m = 502 | correct | Derivation |
| l10 | s4 opts, explain | At the position limit only the reducing side is quoted; at q = 0 there is no skew | correct | Follows from the limit; Cartea, Jaimungal and Penalva ch. 10 (inventory bounds) |
| l10 | s5 prose, chart | With γ = 1p a lot a sale is e^q times as likely; no-skew path ends at 14 and reaches 18; skew path stays within 3 and ends at 0 | correct | Script reads the series |
| l10 | s5 answer 70, wrongs lots 0.7, pence 7000, skewed 0 | 1,400 × 5p | correct | Derivation |
| l10 | s5 explain | Without a skew inventory is a random walk; with one it keeps returning to zero | correct | Script: sd after 100 trades 9.9 lots against 1.1; 92% of skewed paths stay within 3 lots |
| l10 | s6 opts, hints, explain | Short 3 lots: m = 503, bid 501p, ask 505p; skew against inventory | correct | Derivation |
| l10 | s7 prose | Holding q for time τ adds variance q²σ²τ; Avellaneda-Stoikov gives m = V − γq with γ = Aσ²τ | imprecise | Avellaneda and Stoikov (2008), eq. for the reservation price: r = s − qγσ²(T − t). There τ is the time left to the end of the session, not an arbitrary holding time. Finding 2 |
| l10 | s7 opts, explain; q3; review-3 i7 | γ scales with σ², so doubling σ multiplies it by 4; 3 times gives 9; σ doubled and τ halved gives 2 | correct | Algebra on γ = Aσ²τ |
| l10 | s8 prose, opts | Short calls after a client buy: raise both quotes | correct | Same skew logic applied to the option |
| l10 | s8 explain | "Options desks skew this way after every large client trade" | unverified | Industry practice stated as "every"; no source |
| l10 | s9 table keys, explain | q: 1, 2, 1, 0, −1; quotes 497/501, 496/500, 497/501, 498/502, 499/503 | correct | Derivation |
| l10 | s10 opts | No exchange rule forces flat books in shares; overnight moves go both ways; 2% of £10,000 is about £200 | correct | Derivation; LSE rules have no such requirement |
| l10 | s10 explain | "The skew rule says the same: a long τ makes γ large, so you shed inventory hard into the close" | imprecise | True with the night counted in τ. In Avellaneda-Stoikov τ = T − t shrinks to zero at the close and the skew fades. Finding 2 |
| l10 | summary | Restates | correct | As above |
| l10 | q0 answer 799, wrongs 807, 803, 801 | m = 796 | correct | Derivation |
| l10 | q1 opts | q = 0: 498p and 502p | correct | Derivation |
| l10 | q2 opts, explain | At a fair value of 490p a rebound is no more likely than a further fall; purchase price is no anchor | correct | Fair value as conditional expectation (martingale property) |

## l11-adverse-selection

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l11 | s0 answer −8, wrongs spread 2, loss-sign 8, per-share −0.08, explain | (502 − 510) × 100 = −800p | correct | Derivation |
| l11 | s1 prose, canvas, opts, explain | Share α informed about 510p or 490p; average profit per buy s − 10α; break-even 2p at α = 0.2 | correct | Glosten and Milgrom (1985); 0.2 × (2 − 10) + 0.8 × 2 = 0 |
| l11 | s2 prose, answer, wrong sets, byKey, explain | Adverse selection; buy paths 1/10 + 1/5 + 1/5 = 1/2; one buy in five informed | correct | Tree arithmetic |
| l11 | s3 answer 0.6, wrongs prior, alpha, joint 0.3, explain | P(510 \| buy) = (3/10)/(1/2) | correct | Bayes; script |
| l11 | s4 answer 502, wrongs prior 500, high 510, swapped 498, explain | E[V \| buy] = 502p equals the ask; fair value moves to 502p after the trade | correct | Glosten and Milgrom (1985); script |
| l11 | s5 opt.zero, opt.two, opt.minus8, hints, explain | 0.2 × (−8) + 0.8 × 2 = 0; the whole spread is a fee for this risk in the model | correct | Derivation |
| l11 | s5 opt.four why; review-3 i8 byKey.full | "One trade earns at most the half-spread" | imprecise | False per trade against the true value this lesson uses (a sale at 502p of a share worth 490p earns 12p); true on average (E = s − αδ ≤ s). Finding 6 |
| l11 | s6 opts, hints, explain | α = 1: break-even quotes 490p and 510p, nobody gains, the market breaks down; α = 0 gives a zero spread | correct | Glosten and Milgrom (1985), market breakdown |
| l11 | s7 prose | ask = E[V \| buy] = V + αδ, bid = V − αδ, s = αδ | correct | E[V \| buy] = V + δ(2 × (1 + α)/2 − 1); script |
| l11 | s7 answer 6, wrongs old 2, delta 30 | 0.2 × 30 | correct | Derivation |
| l11 | s7 explain; summary formula note; q3 | Spreads widen before announcements (δ grows) and are wide in thin shares (α larger) | correct | Lee, Mucklow and Ready (1993); Easley, Kiefer, O'Hara and Paperman (1996). q3 scopes it to "this lesson's model" |
| l11 | s8 lines, explain | P(informed \| buy) = α; profits s − δ and s; E = s − αδ; s = αδ | correct | Algebra; script |
| l11 | s9 prose, opts, hints | A multi-venue sweep is likely informed (toxic): raise fair value and widen; winner's curse | correct | Glosten and Milgrom logic; Cartea, Jaimungal and Penalva ch. 10 |
| l11 | s9 explain | "Makers watch for sweeps and pull or move their quotes within microseconds" | unverified | Order of magnitude plausible; no source for the timescale |
| l11 | s10 code, tests, how, explain | Seeded simulation; seed 1 gives 0.9988; long-run s − αδ = 1p; two tests exact | correct | Script: all eight expected values reproduce in CPython; long-run mean 1.0 |
| l11 | summary | Restates | correct | As above |
| l11 | q0 answer 0, wrong, explain | α = 0 gives s = 0; real spreads stay positive for costs and inventory risk | correct | Harris ch. 14 |
| l11 | q1 answer 2, wrongs delta 20, half 1 | 0.1 × 20 | correct | Derivation |
| l11 | q2 answer 498, wrongs | 0.4 × 510 + 0.6 × 490 | correct | Script |

## l12-venues

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l12 | s0 prose | Continuous trading stops at 16:30; orders are collected for five minutes; all matched shares trade at one price | correct | LSE closing auction call 16:30 to 16:35 (MIT201) |
| l12 | s0 answer r2, hints, byKey, explain | Matched volume is the smaller side: 600, 1,000, 1,200, 700, 300; uncross at 501p | correct | Script; volume-maximising rule (MIT201 uncrossing algorithm, first criterion) |
| l12 | s1 opts | Sellers limit at low prices, buyers at high; the traded amount follows the lower line | correct | min(D, S) |
| l12 | s1 explain | "it peaks where they cross, at 501p" | imprecise | The plotted lines cross between 501p and 502p (at about 501.3p); 501p is the best whole tick beside the crossing. Finding 7 |
| l12 | s2 answer 300, wrongs 1500, 1200, 0, explain | 1,500 − 1,200; bids above 501p fill in full, the 500 at 501p share 200 by time priority | correct | 1,000 + 200 = 1,200; MIT201 (price then time in the uncrossing) |
| l12 | s3 table keys, explain | Cumulative buyers 500, 800, 1,200, 1,800, 2,000; sellers 2,000, 1,400, 1,000, 500, 200 | correct | Script |
| l12 | s4 answer 250, wrongs 251, 249, 252, explain | Matched 500, 800, 1,000, 500, 200 | correct | Script |
| l12 | s5 opts | No overlap: no shares match at any price, so no uncross price | correct | Definition |
| l12 | s5 explain | "the orders simply stay in the book" | imprecise | Unmatched orders stay only until they expire, and the exchange still sets a closing price from earlier trades (MIT201, closing price hierarchy). Finding 4 |
| l12 | s6 prose, answer 200, wrongs full 400, per-share 0.01, pence 20000, explain | Mid fill saves the half-spread: 20,000 × 1p; a lit order would walk past 2,000 shares | correct | Derivation |
| l12 | s7 opts right, cheaper, same; explain | A dark mid fill saves the half-spread on what fills; a missed fill can cost more | correct | Reasoned; Harris ch. 15 |
| l12 | s7 opt.unreg why | Dark pools are regulated; in the UK and EU under MiFID II rules; the EU caps dark volume | correct | MiFID II/MiFIR (UK: onshored version); EU volume cap under MiFIR Art. 5 |
| l12 | s7 feedback.byKey.unreg | "regulated venues with their own rules and volume caps" | imprecise | Volume caps are an EU rule; the UK removed its double volume cap (FSMA 2023) and the US has none. Finding 3 |
| l12 | s8 prose | Lit exchange, dark pool, auction p* = argmax min(D, S), internaliser (US payment for order flow); best execution; smart order router | correct | Harris ch. 5, 6; MiFID II Art. 27 |
| l12 | s8 opts, explain | A router splits across venues; best execution means "all sufficient steps" for the best possible result | correct | MiFID II Art. 27(1) wording |
| l12 | s9 prose, opts, hints, explain | Chart sums to £200m; £20m is 10% of the day and 40% of the £50m close; £5m is 10% of the auction; index funds use the close | correct | 4 + 30 + 24 + 20 + 42 + 30 + 50 = 200 |
| l12 | s10 table keys, accepts, explain | L, D, A, I; payment for order flow is banned by UK rules | correct | FCA FG12/13 |
| l12 | summary | Restates; "the closing price is the auction's uncross price, not the last trade" | correct | MIT201 (first rung of the closing price hierarchy) |
| l12 | q0 opts, explain | Official close is the uncross price, 501p | correct | MIT201 |
| l12 | q1 answer 101, wrongs | Matched 300, 600, 400 | correct | Derivation |
| l12 | q2 opts, explain | Publishing the imbalance draws in offsetting orders and damps the price move | correct | NYSE and Nasdaq closing imbalance feeds; reasoned |
| l12 | q3 answer 12.42, wrongs | (12.40 + 12.44)/2 | correct | Derivation |

## review-3

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| review-3 | i0 answer 40, wrongs | 2p × 2,000 | correct | Derivation |
| review-3 | i1 answer 1199, wrongs 1195, 1197, 1201, explain | m = 1,202 | correct | Derivation |
| review-3 | i2 opts, explain | She cannot spot all informed flow; still needs s ≥ αδ with α the informed share of the orders she fills | correct | Glosten and Milgrom logic |
| review-3 | i3 answer 102, wrongs | Matched 400, 700, 900, 500, 200 | correct | Derivation |
| review-3 | i4 answer 3, wrongs k, lam | s* = 1/k with k = 1/3 | correct | l9 s7; script |
| review-3 | i5 answer 503.85, wrongs one-buy 502, added 504, prior 500, explain | P(510 \| two buys) = 0.36/0.52 = 9/13 | correct | Script (503.856 simulated) |
| review-3 | i6 answer 150, wrongs | 3p × 5,000 | correct | Derivation |
| review-3 | i8 answer −1, wrongs spread 2, sign 1, explain | s − αδ = 2 − 3 | correct | l11 s8 |

## homework-3

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| homework-3 | i0 answer 58.86, wrongs one-side 29.43, no-fall 160, old-k 48.52 | 2 × 4 × 20e^{−1}; 80e^{−0.5} = 48.52 | correct | Derivation |
| homework-3 | i1 lines, explain | π(s) = 2λ_0 e^{−ks}(s − αδ); s* = αδ + 1/k = 4p | correct | Calculus; script grid search |
| homework-3 | i2 answer 1995, wrongs bid 1987, no-skew 2004, wrong-way 2013, mid 1991 | m = 1,991; ask only at the limit | correct | Derivation |
| homework-3 | i3 answer 505.43, wrongs linear 506, two, one, explain | P = 0.216/0.280 = 27/35; steps 2p, 1.85p, 1.58p | correct | Script (505.457 simulated) |
| homework-3 | i4 code, tests, explain | Volume-maximising uncross; ties by surplus then lowest price, flagged as this task's rules | correct | Ran in CPython: 9/9, starter 0/9; script |
| homework-3 | i5 answer 502, wrongs same 501, p503, explain | Buyers +300: matched 900, 1,300, 1,200, 700, 300 | correct | Script |
| homework-3 | i6 opts, explain | A wholesaler internalises and pays for retail flow because it is rarely informed; best execution still applies | correct | Easley, Kiefer and O'Hara (1996), "Cream-skimming or profit-sharing?"; SEC Rule 606 |
| homework-3 | i7 model, rubric | s = αδ rises from 2p to 8p; keeping 2p loses 6p a trade; skew down and be flat by the close; treat the sweep as toxic; the spread is not pure profit | correct | l10, l11 formulas |
| homework-3 | i8 model, zero-profit step | a = E[D \| buy], b = −E[D \| sell] | correct | Glosten and Milgrom (1985) |
| homework-3 | i8 model, formulas | P(buy | +δ) = α + (1 − α)β; a = αδ/(α + 2(1 − α)β); b = αδ/(α + 2(1 − α)(1 − β)) | correct | Bayes, rederived by hand; script |
| homework-3 | i8 model (b), (c), rubric | β = 1/2 gives a = b = αδ; a = 3p, b = 7p; P(informed \| sell) = 1/3, P(informed \| buy) = 1/7 | correct | Script (3.02 and 7.06 simulated) |
| homework-3 | i8 model (d) | Symmetric ±4.2p: +1.2p on a buy, −2.8p on a sell, 0 overall; a rival undercuts the ask | correct | 0.7 × 1.2 − 0.3 × 2.8 = 0 |

## Counts

308 rows: 294 `correct`, 0 `wrong`, 9 `imprecise`, 0 `misleading`, 5 `unverified`.

The nine `imprecise` rows map to findings 1 to 8 in `docs/reviews/audit-micro-1-3-r2.md` (finding 2 covers two rows). The five `unverified` rows are listed there under "Unverified market remarks".
