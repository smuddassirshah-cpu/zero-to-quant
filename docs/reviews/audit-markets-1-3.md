# Concept audit: markets (topic 1.7), levels 1 to 3, round 1

Scope: `app/content/courses/markets/` l1 to l13, review-1 to review-3, homework-1 to homework-3, at commit 6c01af87. No problems-* file exists for these levels. Blind read: no review, audit or author report on this course was opened until the ledger and the findings below were written. Stage 1 course, full ledger.

Ledger: `docs/reports/audit-markets-1-3-ledger.md`, 2,798 rows: 2,781 correct, 4 wrong, 12 imprecise, 1 misleading, 0 unverified. The 17 rows that are not correct belong to the 11 findings below (finding 1 covers 6 rows, finding 3 covers 2).

Script: `docs/reports/markets-L1-3-concepts.py` (venv Python 3 with NumPy; nothing depends on a library version). 138 checks: every graded key and every named slip value recomputed from its own method, every figure in the explanations and model answers, the closed forms against their series, Monte Carlo for the three empirical claims, and every code widget's solution, starter and wrong programs. 130 pass. 8 fail, and each failing check is a finding (1, 3 twice, 4, 6, 8, 10, 11); exit code 1 until those are fixed. The five wording checks search the text for the missing idea (the pattern is in the script beside each check); the fixer should adjust the pattern if a correct fix uses other words.

Sources: Hull, *Options, Futures and Other Derivatives* (ch. 2, 4, 5, 6); Fabozzi, *Bond Markets, Analysis and Strategies* (ch. 2 to 4); Bodie, Kane and Marcus (BKM), *Investments* (ch. 3, 5, 14, 16, 18); Brealey, Myers and Allen (BMA), *Principles of Corporate Finance* (ch. 5).

Conventions on the watch list, where each first matters and whether it is said there:

| Convention | Where | Verdict |
|---|---|---|
| Annual compounding as the default; "compounded yearly" | l1 screens[5], l2 screens[6] | stated |
| Nominal against effective, continuous limit | l3 screens[2], screens[4] | stated |
| Day count 360 or 365 | l3 screens[9] | stated, but the 360 basis is given without its currency (finding 2) |
| Half-yearly bond yield is twice the six-month rate | l5 screens[3] | stated ("compounded half-yearly: 2.5% per six months") |
| Clean against dirty price, accrued interest | l5 screens[10] | stated and correct |
| Yield to maturity against coupon rate and current yield | l6 screens[0], screens[8] | stated and correct, both orders (discount and premium) |
| Macaulay against modified duration; convexity sign | l6 screens[4], screens[6] | stated; modified = Macaulay / (1 + y) for annual compounding; curve bends up |
| Simple against log returns | l8 screens[4], screens[7] | stated |
| Forward price with income and storage | l10 screens[7], quiz[2], homework-3 items[8] | correct for shares and gold; stated as an equality for jet fuel (finding 11) |
| Forward against futures | l11 screens[0], screens[6] | daily settlement and credit stated; no claim that the two prices are equal, and none about convexity bias |
| Short-sale costs | l12 screens[2] to screens[4] | fee and dividend cash flows correct; the dividend is called a cost with no ex-dividend offset (finding 8) |
| Margin on leveraged longs and shorts | l13 screens[7], homework-3 items[6], items[7] | arithmetic correct (BKM 3.8, 3.9) |
| £ for money | throughout | kept; dollars appear only as a foreign currency and for Metallgesellschaft |

Format: `N. file | JSON path | severity, tag | problem | evidence and basis | exact fix`.

## Level 1

1. l4-npv.json | summary.ideas[2]; quiz[1].widget.options[0].why and [1].why; quiz[3].widget.options[0].why and [2].why; quiz[3].explain.text | imprecise, serious | "NPV falls as the rate rises" is stated as a general rule, and two quiz items grade on it ("A lower rate simply raises every NPV", "Below 8% the NPV is even higher than £40.00, so it cannot be zero there") without saying what the cash flows look like. It holds only for an outlay followed by inflows. A learner carries away a rule that fails for a loan, and never meets the standard interview point that an IRR need not be unique. | A loan-shaped stream +1000, −550, −550 has NPV −£22.68 at 5% and +£45.45 at 10%: it rises with the rate. The stream −100, +230, −132 has NPV zero at both 10% and 20% (script note under finding 1). BMA ch. 5, "Pitfall 1: lending or borrowing" and "Pitfall 2: multiple rates of return". The course knows the hypothesis: homework-1 items[5].prose states it ("Assume `flows[0]` is negative and the rest are not, so the NPV falls as the rate rises"). In quiz[3] the key "Between 8% and 10%" is right for any stream by the sign change; only the reasons for the wrong options need the hypothesis. | summary.ideas[2]: "For an outlay followed by inflows, NPV falls as the rate rises, and two streams can rank differently at different rates. At 0% the NPV is the plain sum." quiz[1].prose: "An analyst reports project A's NPV as £50.00 at 6%, and project B's as £70.00 at 9%. Each is an outlay today followed by inflows, and both are risky in the same way." quiz[3].prose: "A project pays out today and brings cash in later. Its NPV is £40.00 at 8% and −£25.00 at 10%." quiz[3].explain.text, first sentence: "For an outlay followed by inflows, NPV falls as the rate rises: here from £40.00 at 8% to −£25.00 at 10%."

2. l3-comparing-rates.json | screens[9].prose; screens[9].canvas.params.rows[1][0] | imprecise, minor | "Money-market desks often quote on a 360-day basis instead" in a lesson priced in pounds. Sterling money markets use actual/365; actual/360 is the dollar and euro convention. A learner will take 360 as the sterling rule. | Hull 6.1 (day counts: actual/360 for US money-market instruments); sterling deposits and SONIA accrue on actual/365 (Bank of England, SONIA key features and policies). The arithmetic on the screen (key £920.50, 365 credits) is right. | screens[9].prose, last sentence: "Dollar and euro money-market desks quote on a 360-day basis instead, while sterling uses 365; we meet day counts later." Table row label: "360-day (dollar and euro money markets)".

## Level 2

3. l5-pricing-a-bond.json | screens[9].feedback.byKey.test-2; screens[9].feedback.byKey.test-3 | wrong, minor | Both lines name a mistake that cannot reach them. test-2 says "Check you discount at `yld`, not `coupon`", but test 2 is the par case, `bond_price(100, 0.04, 5, 0.04)`: a program that discounts at `coupon` returns 100 there and passes it. test-3 says "Check the face value is discounted over `years`", but every natural coding of that mistake has already failed test 1. | Run under the page's Pyodide through `app/tools/code-runner.mjs` and again in CPython: discounting coupons and face at `coupon`, coupons only at `coupon`, face only at `coupon` all give `test-1`; face not discounted, discounted one year, discounted `years - 1` and left out all give `test-1` (script checks "code l5 bond_price byKey test-2" and "test-3", both failing). The key shown is the first failing test (`widgets/code.js`, `test-${first + 1}`). | Remove `test-2`. Add `"test-1": "The 5-year 4% bond at a 5% yield should give 95.67. Check that every coupon and the face value are discounted at `yld`, and that the face is discounted over `years`."` Reword `test-3` as a description: "A zero-coupon bond should give $100/1.05^{10} = 61.39$. With `coupon = 0` only the discounted face value is left."

4. l5-pricing-a-bond.json | screens[3].explain.text | imprecise, minor | "It is a little below £95.67 because 2.5% a half compounds to 5.06% a year." The reason gives the right direction here by half the argument. The same reason applied to the lesson's own quiz[3] predicts a lower price for the half-yearly premium bond, which is in fact higher (£103.81 against £103.77). | Half-yearly pricing moves a bond away from par, not down: $P - 100 = (c - y) \times 100 \times$ annuity factor, and the half-yearly factor is the larger. Script check "L2.l5 half-yearly pricing moves away from par" (discount lower, premium higher, par unchanged); Fabozzi ch. 2. | Last sentence: "It is a little further below par than £95.67: half-yearly, the 4% coupon compounds to 4.04% a year and the 5% yield to 5.06%, a slightly wider gap."

5. l6-yield.json | screens[7].explain.text | imprecise, minor | "If you hold to maturity you still earn your 5%" drops the condition that the coupons are reinvested at 5%. In the screen's own story yields are now 6%, so reinvested coupons earn more and the realised return is about 5.08% a year. | Fabozzi ch. 3 (yield to maturity as a promised yield; reinvestment risk); BKM 14.4 (realised compound return against yield to maturity). Script note under finding 5: 5.077% with coupons reinvested at 6%, 5.000% at 5%. | Third sentence: "Held to maturity, the bond still pays every promised pound, about 5% a year on your £95.67; the 6% belongs to the new buyer."

6. l8-measuring-returns.json | screens[10].feedback.byKey.test-2 | wrong, minor | "Compound rather than average" is keyed to test 2, but an averaging program fails test 1 first (0.0633 against 0.0582), so the learner who averages never sees the line. | Under the page's Pyodide and in CPython: arithmetic mean, total return divided by T, and mean of growth factors all return `test-1` (script check "code l8 annualised byKey test-2", failing). A program that passes test 1 and fails test 2 is one with the root hard-coded as 3. | `"test-1": "For 12%, −8% and 15% the answer is $1.18496^{1/3} - 1 = 0.0582$, not the 6.33% average. Compound, then take the root."` and `"test-2": "For +50% then −50% the answer is $0.75^{1/2} - 1 = -0.134$. Check that the root uses `len(returns)`, here 2."`

7. l8-measuring-returns.json | screens[10].widget.tests[5]; screens[10].feedback.byKey | imprecise, minor | The lesson teaches that log returns add (screens[4]), and a solution that averages log returns is a valid method. It stops on the hidden test with a −100% year (`math.log(0)`), and the page returns `test-6`, which has no line. The learner is told only which test failed. | Run under the page's Pyodide: `math.exp(sum(math.log(1 + r) for r in returns) / len(returns)) - 1` passes tests 1 to 5 and returns key `test-6`. The expected value there, −1.0, is right (growth 0). | Add `"test-6": "A −100% year makes the growth 0, so the answer is −1. `math.log(0)` fails there: multiply the growth factors instead of adding logs."`

## Level 3

8. l12-selling-what-you-do-not-own.json | screens[2].explain.text | misleading, serious | "So a dividend is a cost of being short, on top of the fee." The cash flow is right: the short pays the lender each dividend. But the share goes ex-dividend by about the same amount, which the short gains, so the dividend is not a net cost in the way the fee is. The course says so itself in l8 screens[0] ("the price dropped as the cash left the company"). A learner would answer the common interview question ("does a dividend hurt a short seller?") wrongly. | Short one share at £50.00, dividend £0.60, nothing else changes: the share opens ex-dividend near £49.40, so the profit is 50 − 49.40 − 0.60 = 0 (script note under finding 8). Hull 5.2 (the short pays dividends to the lender; the forward-price argument of 5.5 nets them against the price); BKM 3.9. The graded items that take the cover price as given (screens[3], screens[4], quiz[2], homework-3 items[5]) are arithmetically right and need no change. | Third sentence: "So you must pay each dividend, although the share usually falls by about that much on the day, so it drains cash more than it adds a loss."

9. l13-leverage.json | screens[7].prose; screens[7].explain.text | imprecise, minor | "Below that it sells your shares." A broker first makes a margin call; it sells only if the cash is not paid. The lesson before (l11) defined a margin call as a demand to top up, so the learner now has two different pictures under one name. The trigger arithmetic (£13,333.33) is right. | BKM 3.8: below the maintenance margin "the broker will issue a margin call"; if the investor does not act, the broker may sell. | screens[7].prose, last sentence: "Below that it makes a margin call: you add cash at once, or it sells your shares." screens[7].explain.text, last sentence: "Below it the broker calls for cash and sells if you cannot pay, often at the worst moment, so your loss is locked in."

10. homework-3.json | items[3].feedback.byKey.end | wrong, minor | The slip value is 0 and the line says "You settled the week at once." Settling the week at once gives a balance of 12,000 − 7,200 = £4,800.00, below the £9,000.00 maintenance level, so a call of £7,200.00: the key itself, not 0. The named mistake does not give the slip's value. | Script check "L3.hw.3 slip `end`" (failing): settling once gives a call of 7200, the slip value is 0. (In l11 screens[5] the same line is right, because there the week's net loss leaves £4,800.00 above a £4,500.00 maintenance level.) | `"end": "No call would need every evening's balance to stay at or above £9,000.00. Day 2 closes at £8,400.00, and so does day 5."`

11. homework-3.json | items[8].model, part 1 (and the prompt's "Derive the no-arbitrage one-year forward price") | imprecise, serious | "Two ways to own fuel in a year must cost the same", giving F = £642.00 as an equality for jet fuel. For a commodity that firms hold in order to use, buy-and-store gives only an upper limit: nobody lends fuel cheaply to be sold short, so nothing stops the forward trading below the carry price. A learner would carry away spot plus interest plus storage as the forward price of oil, and could not explain backwardation. | Hull 5.11: for consumption assets $F_0 \le (S_0 + U)e^{rT}$, with equality only for investment assets such as gold; 5.12 (convenience yield). l10 quiz[2] uses gold, where the equality is right. Part 4 (a quote above £642.00, cash and carry) is the direction that does hold. Script check "L3.hw.8 model says the carry price is an upper limit" (failing). | In the model, after "Storage is a cost of holding, so it raises $F$; a dividend would have lowered it." add: "For a commodity that firms hold in order to use, such as fuel, £642.00 is strictly the highest forward price that no arbitrage allows: nobody lends fuel to be sold short, so the forward can trade below it. We take £642.00 as the price here." No rubric change.

## Checked and found sound (the items most likely to be wrong)

- Every graded key, slip value, table cell, model figure and worked number in the three levels recomputed twice (once by the item's method, once by a second route where one exists: closed form against series, forward against backward, cash accounting against formula). No numerical error found.
- l3: effective rates rise with the number of credits and stay under $e^r - 1$ (checked for m = 1 to 400); AER and UK APR described as effective rates, which is the UK usage.
- l5: gilt clean price, accrued interest for half a period and dirty price; half-yearly convention stated.
- l6: modified duration 4.40 and convexity 24.47 for the 5-year 4% bond at 5%; zero-coupon Macaulay duration equal to maturity; the 2022 claim (a broad US investment-grade index lost about 13%, its worst year on record) matches the Bloomberg US Aggregate; "Newton gets there in three steps" holds from 4%, 6% and 8%.
- l7: the dividend discount model with its condition g < r, and the correct reading at g = r (no answer, not zero or infinity); rights issue and split arithmetic.
- l8: "a few years of data could not tell them apart": with true Sharpe ratios 0.42 and 0.40, the worse fund ranks first in 48.9% of 5-year samples and 48.6% of 10-year samples (200,000 each), and the standard deviation of a 5-year estimate is 0.69.
- l10: the forward price is not the expected price; dividend handled by present value and by reinvestment, both £102.95; covered interest parity quoted the right way up; the index forward's tolerance band takes the linear, exact and continuous forms.
- l11: top-up to the initial margin, strict "below maintenance" trigger, convergence, basis as spot minus futures; Metallgesellschaft about 1.3 billion dollars.
- l13: $R_E = L R_A - (L - 1) r$ against the cash accounting for 1,000 random cases; volatility at L = 3 is three times the asset's (Monte Carlo 0.150 to 0.450) and a 50% loss goes from 7 in 100,000 to 8.8 in 100.
- homework-3 items[9] (performance task): both bounds, the two dearer alternatives, the one-rate price and the optional profit all recompute.
- Code widgets: six solutions pass every hidden test and every starter fails, under the page's Pyodide (`grade-all.mjs --code`); 27 wrong programs across the six widgets each fail at least one hidden test, so no wrong program passes. homework-2 items[3] `test-1` ("check the direction") is correct: all three reversed codings fail test 1 first.

## Tool results

- Validator: `cd app && node tools/validate.mjs`: 0 errors, 4,610 warnings (repository-wide).
- Number scripts: `node tools/run-number-scripts.mjs --only markets`: 1 of 436 scripts, 1 passed (the only committed markets number script is `docs/reports/markets-3-perf-numbers.py`; lessons 1 to 13 have no committed author number script, which is itself worth a line in the state files).
- `node tools/grade-all.mjs --file <each of the 19 files> --local-cdn <pkgs>`: 219 widgets, 0 failures. With `--code` on the six files that hold code widgets: 6 Python widgets run, 0 failures.
- Concepts script: exit 1, 130 ok, 8 failing (the findings listed above).
- No playthrough, as the common rules say.

## Overlap with the earlier reads

Read after the commit of the ledger and findings above (c242507c): `docs/reviews/review-1.7.md` (the second read of topic 1.7, markets section of 20 findings, and its fix pass, all 20 fixed), `docs/reports/markets-3-perf.md` and `docs/reviews/review-perf-retrofit-12.md` (the performance task homework-3 items[9]: no finding on markets). The other review files that name markets cite it only as a source for reuse or prerequisite checks and raise nothing on these lessons. All earlier findings were applied before this audit, so "both" can only count a defect that survived its fix, and none did.

| Conceptual findings | Count | Items |
|---|---:|---|
| Audit only | 11 | 1 to 11 above |
| Earlier review only | 13 | listed below; all fixed before this audit, and the fixed text is verified in the ledger |
| Both | 0 | |

New `wrong` that no earlier read found: 3 findings (3, 6 and 10; four ledger rows), all minor feedback lines whose named mistake cannot reach them. One is in level 3 and two are in level 2, so the round is above the convergence rule's one new `wrong` per three levels.

The earlier review's conceptual findings (its other seven were spelling, code formatting, sentence counts, sentence length and a repeated item):

- l1 quiz b-small "1% over 10 years" on a 20-year item: fixed; the why now gives £200.00 over 20 years (ledger: correct).
- l2 screens[9] "overstates by about a third": fixed to "about a third below the headline" (679,516 / 1,000,000 = 0.68).
- l4 screens[3] "exactly needs Newton's method": fixed to "numerically, for example by Newton's method".
- l5 screens[1] `coupons-only` why (four coupons): fixed; 17.32 is five coupons, recomputed.
- l6 screens[2] bisection prices: fixed; £92.18 and £91.97 recomputed (script check L2.l6.s2).
- l6 screens[4] cross-reference to the wrong course: fixed; Limits and Derivatives l15 does hold the 4.40 (checked by search).
- l6 screens[5] cell −7.59: fixed to −7.58 (−7.584%).
- l6 screens[8] `inverse` value: fixed to 0.0453.
- l6 screens[11] "a couple of points": fixed to "about three points".
- l12 summary "a profit of P0": fixed to $P_0 - C$.
- l13 screens[5] "magnifies losses more than gains": fixed; the line now says the interest drags on both outcomes.
- homework-2 `five-year` value: fixed to −0.0010, recomputed.
- review-3 `orig` value: fixed to 27,000, recomputed.

Why the earlier read missed the audit's findings: it checked each number against its own why and each cross-reference, which is where its 13 hits are. It did not submit wrong programs to the code widgets (findings 3, 6, 7), did not test rules for their hypotheses (1, 4, 5, 11) and did not read conventions against market practice (2, 8, 9). Finding 10 is the one of its own kind it missed: a slip value that does not match the mistake its line names.

## Inbox

Two bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (audit markets):".

## Fix pass

Opus fixer, round 1, on cb8e1702. Every basis below is my own derivation, run or source; the auditor's text was used only to locate the item.

1. l4 summary.ideas[2], quiz[1], quiz[3] | fixed | $NPV'(r) = -\sum t C_t (1+r)^{-t-1}$ is negative for every $r$ only when $C_0 < 0$ and every later $C_t \ge 0$ (BMA ch. 5, pitfalls 1 and 2); +1000, −550, −550 gives −£22.68 at 5% and +£45.45 at 10%. The hypothesis is now in the summary, both quiz prompts, quiz[1] option `a` and quiz[3] explain; keys unchanged (quiz[3]'s key follows from the sign change alone).
2. l3 screens[9] | fixed | USD (SOFR, US money-market instruments) and EUR (€STR, EURIBOR) accrue actual/360, sterling (SONIA, deposits) actual/365 (Hull 6.1, day count conventions; Bank of England, SONIA key features); prose and table label now name the currencies; key £920.50 unchanged.
3. l5 screens[9] byKey | fixed differently | Under Pyodide, discount-at-coupon and wrong-face-period codings all fail test 1, so a new `test-1` line names them; but the example's 5% hard-coded as `1.05` or `0.05` (three codings) passes test 1 and first fails test 2, and the face discounted over a fixed `** 5` (three codings) passes tests 1 and 2 and first fails test 3. So `test-2` and `test-3` were kept and reworded to name those mistakes. 12 `mutants` added (6 on test 1, 3 on test 2, 3 on test 3), all confirmed by `grade-all --code`. No test changed.
4. l5 screens[3] explain | fixed differently | Exact identity: two £2 coupons a year valued at year end at 2.5% a half are £4.05, and $1.025^2 - 1 = 5.0625\%$, so the half-yearly bond is an annual one paying £4.05 at 5.06% (price 95.6240 both ways). Generally $P - F = (c - y)F(1 - u^{-2T})/y$ with $u^2 = 1 + y + y^2/4 > 1 + y$, so half-yearly pricing moves away from par in either direction. I did not use the audit's "coupon compounds to 4.04%", which has the coupons reinvested at the coupon rate, not the yield.
5. l6 screens[7] explain | fixed | Realised return on £95.67 with coupons reinvested at 6% is $((4 \cdot s_{5|6\%} + 100)/95.67)^{1/5} - 1 = 5.08\%$, at 5% exactly 5.00% (Fabozzi ch. 3, reinvestment risk); text now says "about 5% a year", true for either reinvestment rate.
6. l8 screens[10] byKey test-2 | fixed | Arithmetic mean, total return over $T$ and mean growth factor all first fail test 1 under Pyodide; a root fixed at 3 (three codings) passes test 1 and first fails test 2. New `test-1` (average) and `test-2` (`len(returns)`) lines; $1.12 \times 0.92 \times 1.15 = 1.18496$, $1.18496^{1/3} - 1 = 0.0582$; $0.75^{1/2} - 1 = -0.134$. Six `mutants` added.
7. l8 screens[10] byKey test-6 | fixed | Mean log return via `math.log(1 + r)`, `math.log1p(r)` and a summing loop each pass tests 1 to 5 and raise in test 6, which the page keys `test-6` (code.js; AUTHORING engine pass 7, item 2). Line added; three `mutants` added. Expected −1.0 rechecked (growth 0).
8. l12 screens[2] explain | fixed | Hull 5.2 (the short pays the lender any income) with the ex-dividend price fall (Hull 5.5's $F = (S_0 - I)e^{rT}$ nets the income against the price): short at £50.00, £0.60 dividend, ex-dividend £49.40, profit $50 - 49.40 - 0.60 = 0$. Third sentence now says the dividend is paid but the share usually falls by about as much, so unlike the fee it leaves the profit about the same. Graded items take the cover price as given and are unchanged.
9. l13 screens[7] | fixed, extended | BKM 3.8: below maintenance the broker issues a margin call and sells only if it is not met. Prose and explain as the audit proposed; also the question, widget label and canvas label ("margin call £13,333.33"), and the same wording in review-3 `r-margin-loan` (question, label, `zero` line), which said "the broker sell(s)". Keys £13,333.33 and £25,714.29 unchanged ($10{,}000/0.75$, $18{,}000/0.7$).
10. homework-3 items[3] slip `end` | fixed differently | Settling the week at once gives $12{,}000 - 2 \times 10 \times 360 = 4{,}800 < 9{,}000$, a call of £7,200.00 (the key), so the old line was wrong. Instead of a description, the line now names a mistake that gives 0: the 2-contract balance checked against one contract's £4,500.00 (balances 10,000, 8,400, 9,000, 6,000, 4,800, never below 4,500; computed by hand and by the script). Slip value 0 unchanged; band clear of the key.
11. homework-3 items[8] | fixed | Hull 5.11: for consumption commodities $F_0 \le (S_0 + U)e^{rT}$, because holders will not sell the physical good and buy forward; 5.12 convenience yield. Prompt part 1 now asks for the price "that buying and storing fuel implies"; model part 1 frames buy-and-store as one route, says a forward above £642.00 is an arbitrage (part 4), that £642.00 is only an upper limit for fuel, and that the item takes it as the price. Rubric unchanged.

Concepts script `docs/reports/markets-L1-3-concepts.py`: re-pointed, as its docstring now records: the hw.3 `end` check recomputes the newly named mistake; the l5 test-2 and test-3 checks submit the newly named codings, with a new test-1 check for the old ones; the l8 test-2 check is now a test-1 check for averaging plus a fixed-root test-2 check and a mean-log test-6 check; `run_tests` returns N for an exception in test N, as the page does; one new check for the £4.05 at 5.06% identity. Regex checks for findings 1, 4, 8 and 11 match the new wording unchanged. Exit 0, 143 checks.

Gates: validator 0 errors; voice scan 35 on the nine files, 0 and 0; concepts script exit 0; `run-number-scripts --only markets` 1 passed; `grade-all --code --file` on the nine files 0 failures (mutants enforced: a probe with a wrong test number failed as expected); playthrough of the seven lessons and two sets, desktop and `--mobile`, all passed.

## Fix-pass read

Fresh reader, blind to the audit above until these rows were written. Read: `git show ead4b0b6 -- app/content/courses` (markets l3, l4, l5, l6, l8, l12, l13, review-3, homework-3). Script: `docs/reports/markets-L1-3-fixread.py` (every changed number two ways; exits 1 while row 4 stands, 0 after its fix). Code lines: 23 codings of my own plus the 21 committed mutants graded through `tools/code-runner.mjs` under the local Pyodide; every one first fails the test its line names, both solutions pass and both starters fail test 1.

| # | file | JSON path | claim | verdict | basis |
|---|---|---|---|---|---|
| 1 | l3-comparing-rates | screens/9/prose | Dollar and euro money markets quote on 360 days, sterling on 365 | correct | Hull ch. 6.1 (day counts: actual/360 for US money-market instruments); market convention ACT/360 for USD and EUR, ACT/365 for GBP. Key £920.50 recomputed |
| 2 | l3-comparing-rates | screens/9/canvas rows[1][0] | "360-day (dollar and euro money markets)" | correct | as row 1 |
| 3 | l4-npv | summary ideas[2] | For an outlay followed by inflows, NPV falls as the rate rises | correct | Derivation: each inflow's PV falls in r, the outlay is fixed. Brealey-Myers-Allen ch. 5 (IRR pitfalls 1 and 2: the rule fails for borrowing and mixed-sign streams). Grid check on two streams; counter-stream [+1000, −1100] rises |
| 4 | l4-npv | quiz/q-different-rates/prose (with the key `right`) | A is £50.00 at 6%, B is £70.00 at 9%, both conventional; keyed "Nothing yet: compute both at the same rate" | **wrong** | The new premise makes NPV fall with the rate for both. So B(r) ≥ 70 > 50 ≥ A(r) at every shared rate from 6% to 9%, including both rates the analyst used. The key is no longer true and option `b` ("B is better") is. The item's own `why` on `b` ("B's NPV at 6% would be higher than £70.00") hands the learner the proof |
| 5 | l4-npv | quiz/q-different-rates/options a/why | For an outlay followed by inflows, a lower rate raises the NPV | correct | as row 3 (reworded by the fix in row 4) |
| 6 | l4-npv | quiz/q-irr-bracket/prose | Outlay today, inflows later; NPV £40.00 at 8%, −£25.00 at 10% | correct | Monotone NPV gives one root, between 8% and 10%; exactly one option true; the `below` and `above` reasons now follow from the premise |
| 7 | l4-npv | quiz/q-irr-bracket/explain | NPV falls as the rate rises for such a stream; interpolation 9.23% | correct | 0.08 + 0.02 × 40/65 = 0.0923, two ways |
| 8 | l5-pricing-a-bond | screens/3/explain | £95.62 sits further below par than £95.67; it works like an annual bond paying £4.05 at 5.06% | correct | Two coupons are worth 2 × 1.025 + 2 = 4.05 at each year end, and 1.025² − 1 = 5.0625%. Annual bond, £4.05, 5 years, 5.0625%: 95.623968, equal to the half-yearly price to 1e-9. Shortfall 1.0125 points against 1.00. (At the rounded 5.06% it prices at 95.63; "works like" covers it) |
| 9 | l5-pricing-a-bond | screens/9/feedback test-1 | 5-year 4% bond at 5% gives 95.67; discount coupons and face at `yld` | correct | 95.6705 two ways. My codings (coupon undiscounted; coupon over `years`; rate used as the amount; discount at `coupon`; face over `years − 1`) all return test-1 |
| 10 | l5-pricing-a-bond | screens/9/feedback test-2 | Yield equal to coupon prices at 100; fault is the fixed 5% | correct | Tests 1 and 2 differ only in `yld`, so passing 1 and failing 2 means the yield is not used. My codings (`r = 0.05` variable; closed form with 1.05 and 0.05) return test-2 |
| 11 | l5-pricing-a-bond | screens/9/feedback test-3 | 100/1.05^10 = 61.39; face over `years`, not a fixed 5 | correct | 61.3913. My codings (`n = 5` for the face; list `[1..5]` with power 5) return test-3. A loop fixed at 5 with the face right first fails test 4 and gets the generic line, which fits |
| 12 | l5-pricing-a-bond | screens/9/widget mutants, test 1 (6) | each first fails test 1 | correct | run: all test-1 |
| 13 | l5-pricing-a-bond | screens/9/widget mutants, test 2 (3) | each first fails test 2 | correct | run: all test-2 |
| 14 | l5-pricing-a-bond | screens/9/widget mutants, test 3 (3) | each first fails test 3 | correct | run: all test-3 |
| 15 | l6-yield | screens/7/explain | Held to maturity it pays every promised pound, about 5% a year on £95.67 | correct | IRR of the flows on 95.67 is 5.00% by bisection; with coupons reinvested at 6% the realised rate is 5.08%. "About" is right. £91.58 and £4.10 recomputed (exact difference 4.095) |
| 16 | l8-measuring-returns | screens/10/feedback test-1 | 1.18496^(1/3) − 1 = 0.0582, not the 6.33% mean | correct | 1.12 × 0.92 × 1.15 = 1.18496; root 0.05820 by power and by exp-log; mean 0.0633. My codings (mean; no "− 1"; product of returns; total not annualised; growth × 1/T) all return test-1. Note: the line names the mean, and a learner who only forgot "− 1" reads it too; optional tail "then subtract 1" |
| 17 | l8-measuring-returns | screens/10/feedback test-2 | 0.75^(1/2) − 1 = −0.134; the root must use `len(returns)`, here 2 | correct | −0.13397. Test 1 has three returns, so a fixed cube root passes it. My codings (`n = 3`; literal 0.3333333333333333) return test-2 |
| 18 | l8-measuring-returns | screens/10/feedback test-6 | A −100% year gives growth 0 and answer −1; `math.log(0)` fails | correct | 0^(1/2) − 1 = −1.0 exactly (compare `equal`). `math.log(0)` raises ValueError. My codings (log of the product; list of logs) return test-6, as does `statistics.geometric_mean`. NumPy logs give −inf and pass |
| 19 | l8-measuring-returns | screens/10/widget mutants, test 1 (3) | each first fails test 1 | correct | run |
| 20 | l8-measuring-returns | screens/10/widget mutants, test 2 (3) | each first fails test 2 | correct | run |
| 21 | l8-measuring-returns | screens/10/widget mutants, test 6 (3) | each first fails test 6, by raising | correct | run: key test-6, not `error` |
| 22 | l12-selling-what-you-do-not-own | screens/2/explain | You pay each dividend, but the share falls by about as much ex-dividend, so unlike the fee your profit is about the same | correct | Hull ch. 5.2 (the short pays the broker any income on the borrowed shares); Hull, chapter on dividends and options (the price falls on the ex-dividend date by about the dividend, a little less for tax). Consistent with the lesson's profit = P0 − P1 − C, where P1 is the ex-dividend price. Key "You do" still the one true option |
| 23 | l13-leverage | screens/7/prose | Below 25% equity the broker makes a margin call: add cash at once, or it sells | correct | Hull ch. 5.2 and ch. 2 (maintenance margin, margin call, close-out if not met) |
| 24 | l13-leverage | screens/7/question | "Below what position value does the broker make a margin call?" key 13,333.33 | correct | V − 10,000 ≥ 0.25V gives V ≥ 10,000/0.75; bisection agrees; at exactly 13,333.33 the rule holds, so "below" is the right word. One keyed value |
| 25 | l13-leverage | screens/7/widget/label | "Position value at the margin call" | correct | as row 24 |
| 26 | l13-leverage | screens/7/explain/text | Below it the broker calls for cash and sells if you cannot pay | correct | as row 23; a fall of a third checked |
| 27 | l13-leverage | screens/7/explain/canvas points.call.label | "margin call £13,333.33" | correct | as row 24 |
| 28 | review-3 | items/r-margin-loan/question | margin call below 25,714.29 | correct | 18,000/0.7 two ways |
| 29 | review-3 | items/r-margin-loan/widget/label | "Position value at the margin call" | correct | as row 28 |
| 30 | review-3 | items/r-margin-loan/feedback zero | "The broker calls earlier, at 30%" | correct | equity is zero at V = 18,000 < 25,714.29 |
| 31 | homework-3 | items/h-two-calls/feedback end (slip value 0) | Checking against £4,500.00, one contract's maintenance, gives no call; the 2-contract level is £9,000.00 and day 2 closes at £8,400.00 | correct | Simulated with level 4,500: closes 10,000, 8,400, 9,000, 6,000, 4,800, no call, paid 0. Second way: low is 12,000 + 20 × (7,640 − 8,000) = 4,800 > 4,500. Key 7,200 and slips 3,600, 4,200 recomputed |
| 32 | homework-3 | items/h-airline-hedge/prompt part 1 | "the forward price that buying and storing fuel implies" | correct | Hull ch. 5.11: F0 = (S0 + U) grown at r for an investment asset; 600 × 1.05 + 12 = 642 with storage paid at the end |
| 33 | homework-3 | items/h-airline-hedge/model part 1, derivation | One way to own fuel in a year is to buy and store; this way costs £642.00 | correct | as row 32 |
| 34 | homework-3 | items/h-airline-hedge/model part 1, limit | Above £642.00 is an arbitrage; for fuel, held for use, £642.00 is only an upper limit, since holders will not sell and buy forward | correct | Hull ch. 5.11, consumption commodities: F0 ≤ (S0 + U)e^{rT}, the reverse trade failing because owners keep the commodity for use (convenience yield). Part 4 uses the valid side, 660 > 642, profit 18. Rubric matches |

Counts: 34 rows. correct 33, wrong 1, imprecise 0, misleading 0, unverified 0.

### Finding

1. l4-npv.json | quiz/q-different-rates | wrong, serious | The fix added "Each is an outlay today followed by inflows". With that premise B's NPV is above £70.00 at any rate under 9% and A's is below £50.00 at any rate over 6%. So B beats A at every shared rate from 6% to 9%, and the keyed "Nothing yet" is false while option `b` is true. | Monotone NPV for conventional streams (row 3; Brealey-Myers-Allen ch. 5); script check "l4 q-different-rates" fails. | Swap the two rates, so the known values bound the wrong way and either ranking is possible (script: "swapped rates: A can win at 6%", "B can win at 6%"). Paste-ready:
   - `prose`: "An analyst reports project A's NPV as £50.00 at 9%, and project B's as £70.00 at 6%. Each is an outlay today followed by inflows, and both are risky in the same way."
   - option `b` `why`: "You compared NPVs taken at different rates. B's NPV at 9% would be lower than £70.00."
   - option `a` `text`: "A is better: it was tested at the higher rate"
   - option `a` `why`: "The rate is not a score. For an outlay followed by inflows, a higher rate simply lowers the NPV."
   - key, `feedback` and `explain` unchanged.

Optional, not a finding (row 16): l8 `test-1` could end "Compound, take the root, then subtract 1."

## Fix-pass follow-up (Opus)

| finding | status | basis (own) |
|---|---|---|
| Fix-pass read 1, l4-npv quiz/q-different-rates | fixed | NPV of an outlay then inflows falls strictly in r (each inflow's PV falls, the outlay is fixed). With A £50.00 at 9% and B £70.00 at 6%: at 9%, B < 70 but may sit above or below 50; at 6%, A > 50 but may sit above or below 70. Own simulation (scratch `fix-mkts-l4/check.py`, one-cash-flow projects fitted to the two quotes): A wins at 6%, 7.5% and 9% when A's cash is late (A 763.64 v B 70.00 at 6%; B −59.83 at 9%); B wins at all three when both pay £300 in one year (57.79 v 70.00 at 6%; 50.00 v 62.21 at 9%). So no ranking follows and "Nothing yet" is true; key unchanged |

Edits, all in `quiz/q-different-rates`: `prose` rates swapped (A at 9%, B at 6%); option `a` text "A is better: it was tested at the higher rate"; `a` why "The rate is not a score. A higher rate lowers the NPV of an outlay followed by inflows, so A's at 6% would exceed £50.00, but not necessarily £70.00."; option `b` why "... B's NPV at 9% would be lower than £70.00, perhaps below £50.00." (the first case above takes it to −£59.83). `feedback` and `explain` re-read under the new prose and left as they are: both still true, and "rankings can flip at another rate" holds for crossing conventional streams. No key, slip or test changed.

Gates: `markets-L1-3-fixread.py` exit 0 (was 1); `markets-L1-3-concepts.py` exit 0; validator 0 errors; voice-scan 35 on l4 0 and 0; `run-number-scripts --only markets` 1 passed; `grade-all --file l4-npv.json` 0 failures; playthrough `markets/l4-npv` green desktop and `--mobile` (quiz 4/4).
