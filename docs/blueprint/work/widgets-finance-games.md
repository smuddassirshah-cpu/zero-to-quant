# Widget catalogue: finance, projects and interview formats

Blueprint work file, Stage 2 Phase 1. Draft 1, 6 October 2026.

**Scope.** Every interactive widget needed to teach curriculum items 1.7 Finance basics (100 h), 2.3 Projects (400 h) and 3.3 Interview preparation (250 h), Brilliant-style (act before you read, the diagram explains, direct manipulation, one idea per screen) and at the depth a top quant programme expects. That means shares, bonds, interest and compounding, the limit order book, the bid-ask spread, market against limit orders, forwards and futures, option payoffs, put-call parity, binomial trees, Black-Scholes, the Greeks and market microstructure in 1.7; the five projects in 2.3 (backtesting engine, alpha signal research, options analytics, live market data, paper trading bot); and the live interview formats in 3.3 (mental arithmetic including 80 questions in 8 minutes, market-making games, betting games and Kelly sizing, probability brainteasers, and mock interviews spoken aloud).

**Read for this file.** `docs/curriculum.md`; `docs/design-research.md` sections 2, 4, 5, 6, 8, 9 and 10; the Stage 1 prototype (`css/tokens.css`, `js/screens/lesson.js`, `drill.js`, `drill-worker.js`, `exam.js`, `review.js`); the sibling work files `widgets-stage0.md`, `widgets-calc-linalg.md`, `widgets-prob-stats-ts.md` and `widgets-programming.md`; the owner's lesson-creator, maths-teaching, code-craft and project-forge skills with `engineering-floor.md` and `blueprint.md`; the Artifact `sample`, `db`, `room`, `permissions` and `downloads` contracts (version 0.2.69).

**Sources the lessons follow.** Khan Academy Finance and Capital Markets (interest, shares, bonds); Zerodha Varsity modules on stock markets, futures and options; Hull, Options, Futures, and Other Derivatives (forwards, futures, option properties, binomial trees, Black-Scholes-Merton, the Greeks, interest rates); Larry Harris, Trading and Exchanges (microstructure); Natenberg, Option Volatility and Pricing (optional depth for the options track); López de Prado, Advances in Financial Machine Learning, and Bailey and López de Prado on the deflated Sharpe ratio (backtesting); Grinold and Kahn, Active Portfolio Management (information coefficient and the fundamental law); Gatheral, The Volatility Surface (SVI and no-arbitrage checks); Avellaneda and Stoikov (2008) and Glosten and Milgrom (1985) for market making; Thorp and MacLean, Thorp and Ziemba on Kelly sizing; Mosteller, Zhou (the green book), Crack (Heard on the Street) and Joshi for interview problems; Jane Street's Probability and Markets guide. Content is recreated from general knowledge of these works; no text is copied, and interview problems are re-parameterised recreations with original solutions (decision 9).

**How to read it.** Section 1 walks every lesson and names what the learner must manipulate, see, build or predict. Every widget below exists because a row in section 1 needs it. Section 2 states what this cluster adds to the shared widget contract. Section 3 specifies new primitives, section 4 additions to shared primitives, section 5 extensions to widgets the sibling catalogues own. Sections 6 to 8 specify the composites. Sections 9 to 13 cover generators, the misconception register, rejected alternatives and open questions, the full widget table and cross-cluster needs.

**Numbering.** Course and lesson numbers (1.7.1 to 1.7.9, 2.3.0 to 2.3.5, 3.3.1 to 3.3.5, and L1, L2 inside them) are this catalogue's working outline, written to test coverage. The course-architecture blueprint owns the final outline; renumbering it changes no widget.

**Evidence tags**, as in the design research: [sourced] for facts from a cited source, [recalled] for facts from general knowledge not re-checked here, [inferred] for deductions, [our choice] for decisions, and [unverified] for anything not yet measured.

**Currency in prose.** A dollar sign opens inline maths in these documents, so prose writes "USD 100" or "100 dollars". Code blocks and configuration use plain numbers.

---

## 0. Summary and decisions

- **49 new widgets:** 7 primitives and 42 composites. Section 12 lists them all.
  - **P0:** 2 (`puzzle-workbench` core and `scratch-pad`), because the curriculum's habit of three interview-style probability problems a week starts at item 1.5 (finding 2).
  - **P1:** 31 (all of 1.7: 6 primitives and 25 composites).
  - **P2:** 16 (11 project composites for 2.3 and 5 interview composites for 3.3).
- **23 widgets from the sibling catalogues gain a mode or preset** (section 5), and 9 shared primitives gain additions (section 4). Three priorities move: `gbm-lab` gains a P1 mode for 1.7, `hedging-sim` gains a P1 one-path mode, and `binomial-tree` passes to this catalogue's ownership because 1.7 is its first and heaviest user.
- **Generators.** 40 of the 42 composites need seeded generators for practice, homework and exams (section 9). `results-note` needs none, `mock-interview` selects seeded items from other widgets' generators, and the 7 primitives need none.
- **Build waves:** G1 (1.7.1 to 1.7.4: time value, shares, bonds, the order book; Stage 0 maths only), G2 (1.7.5 and 1.7.6: forwards, futures, option payoffs and parity), G3 (1.7.7 to 1.7.9: binomial trees, Black-Scholes, Greeks, microstructure), H (2.3 projects) and J (3.3 interviews). `puzzle-workbench` core and `scratch-pad` ship in the probability cluster's wave D4.
- **Three services carry most of the risk:** `exchange-sim` (one matching engine for every book, game and bot), `finance-core` (pricing, bonds, rates, Greeks, implied volatility) and `interview-engine` (Bertie as interviewer). Section 2.12 states their acceptance tests.

### 0.1 Decisions

| # | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| 1 | Reuse | Extend sibling widgets (`binomial-tree`, `gbm-lab`, `hedging-sim`, `drawdown-lab`, `game-lab`, `speed-drill`, `multiple-testing`, `time-series-lab` and others, section 5); build a composite only where no sibling can carry the idea | A self-contained finance widget set | The Stage 1 lesson's 23 defects were mostly machinery. Two binomial trees means two sets of node arithmetic to get wrong |
| 2 | Order matching | One deterministic `exchange-sim` service: price-time priority over integer ticks and integer lots, shared by `order-book`, `auction-lab`, `tape-lab`, `dealer-sim`, `feed-sim`, `order-lifecycle`, `paper-trader` and `mm-game` | Fill logic inside each widget; a third-party JavaScript matching engine | Fill rules (partial fills, priority after an amend, self-trades) are the commonest source of subtle bugs. One engine is property-tested once. No maintained, licence-clear JavaScript engine with call auctions was found [unverified: not searched exhaustively] |
| 3 | Money arithmetic | Integers in minor units (ticks, lots, cents) inside `exchange-sim` and `ledger`; formatting only at the display edge. Model values (prices from formulas, rates, Greeks) are float64 with stated tolerances | Floats for cash; a decimal library such as decimal.js | Exact reconciliation of cash, position and P&L. A trade blotter that drifts by 0.000001 erodes trust in every answer. Integers cost nothing; a decimal library adds size for no gain |
| 4 | Compounding convention | Annual and periodic compounding in 1.7.1 to 1.7.3 (bonds are quoted that way); continuous compounding from 1.7.5 on for derivatives (Hull's convention). Every rate on screen carries a convention chip ("5%, continuous") | One convention everywhere | Bond yields are periodic by market practice; derivative formulas are cleanest continuous. The chip prevents silent switching, the same lesson as the probability cluster's geometric-distribution decision 13 |
| 5 | Game counterparties | Seeded deterministic bots decide every trade in `mm-game`, `dealer-sim`, `order-book` flow and `bet-lab`. Bertie only narrates and debriefs | Bertie (an LLM) as the trading counterparty | Reproducible and gradeable games; `sample` on the default tier takes 5 to 60 s before first text [sourced, `sample.d.ts`], too slow for a quote cycle; no cost per trade |
| 6 | What games and simulations grade | Decisions against exact expectations: a quote against the posterior mean, a fraction against the Kelly fraction, a hedge against the minimum-variance ratio. Realised P&L is shown and scored on a leaderboard, never used for a pass or a fail | Grading realised P&L | Realised P&L is a random outcome. The probability cluster's rule 1 (never grade a random estimate) applies with more force here, because good quoting loses money on some seeds |
| 7 | Where the 2.3 projects are built | On the learner's machine, in Git, as the curriculum requires. In-app composites teach and rehearse each component on synthetic data; milestones verify by pasted output (`setup-checklist` project mode) and by downloadable starter test suites | Building the projects inside the app; live market connections from the browser | The deliverable is a public repository with tests and a results note. The Artifact blocks all network requests; free data feeds have usage terms that forbid redistribution [recalled] |
| 8 | Market data in the app | Synthetic only, from the `market-gen` service, with known truths (true IC, true volatility, planted arbitrage). Real data appear only in the learner's own project code (yfinance, Deribit's public API, Nasdaq Data Link) | Bundling price or option-chain snapshots | Redistribution rights for free market data are unclear [recalled]. Known truths make items gradeable. Same choice as the probability cluster's decision 11 |
| 9 | Interview problem banks | Recreated, re-parameterised problems with our own solutions, cited by source and chapter ("after Zhou, chapter 4"); never verbatim. A `book-log` mode tracks the learner's progress through their own copy of each book for the 3.3 exit test | Transcribing the books; LLM-generated problems at runtime | Copyright, and the owner's instruction to recreate from expertise. Generated problems can be unsolvable (design research section 10); ours ship with solver tests |
| 10 | Speech | Browser speech: `SpeechRecognition` for capture where the browser has it, `speechSynthesis` for the interviewer's voice; a typed path is always equivalent; audio is never stored by the app | Sending audio to Claude; on-device Whisper in version 1 | The Messages API reference describes no audio input [inferred from the bundled API reference]; a Whisper model is tens of megabytes [unverified size] and cannot run in the Artifact without the archive-free packaging question being solved |
| 11 | Mock interviewer | Bertie in an interviewer mode (a neutral expression set, no hint ladder, terse), driven by `interview-engine` from our banks with private solutions and rubrics | A separate interviewer character; questions recalled by the model | One face for the AI, as the owner asked. Our solutions stop the model from accepting a wrong answer it half-remembers |
| 12 | Partner sessions (a stranger interviewing you; market-making aloud with a partner) | Pass-and-play on one device on both targets; two-device sessions through the `room` capability in the Artifact only, where the platform admits the partner [unverified for invited guests] | A signalling server on the proxy for WebRTC | Keeps the proxy a key-holding relay with one route (threat class B to C boundary stays small); `room` already exists in the Artifact |
| 13 | Weekly interview problems | `puzzle-workbench` core is P0 and ships with probability (wave D4), although its home topic is 3.3 | Deferring to P2; serving weekly problems through scattered probability widgets | The curriculum starts three problems a week at 1.5, inside the depth-first build |
| 14 | 1.7 timing | 1.7 stays P1, as the priority rule says. Wave G1 (1.7.1 to 1.7.4) needs only Stage 0 maths, so it ships first in P1 and the course map unlocks it from 1.3, matching "alongside 1.3 to 1.6" | Pulling all of 1.7 into P0 | 1.7.6 to 1.7.8 need 1.3 (derivatives, Taylor) and 1.5 (expectation, the normal and lognormal) anyway. G1 is cheap and independent |
| 15 | Order book and quote colours | Bids `--s6` violet, asks `--s2` orange, each with a text label and fixed side (bids left, asks right); P&L on the diverging ramp with "+" and "−" glyphs | Trading-screen green and red | Green and amber belong to grading. Red against green fails for the commonest colour-vision deficiencies |
| 16 | Pricing accuracy | `finance-core` in JavaScript, tested against golden fixtures generated in CI with CPython and SciPy, and QuantLib for day counts and bond analytics [QuantLib version pin unverified] | Pyodide for widget numbers; trusting textbook tables | Widgets must redraw within a frame on a phone, and the Artifact may have no Python. Fixtures make the JavaScript provably equal to the references |
| 17 | Kelly | One `kelly-lab`; the probability cluster's `game-lab` `kelly-coin` mode becomes an embed of it | Two Kelly implementations | One growth-curve implementation, one set of misconceptions |
| 18 | Order book rendering | A new `price-ladder` primitive (a host whose rows are focusable price levels) | Building the ladder from `marks` on `plot-2d`, as Stage 0's table suggested | Order entry happens on the ladder: rows need focus, keyboard entry, hit areas and a grid table view, which passive marks do not have |

### 0.2 Findings that shape the widgets

1. **The 1.7 exit test asks for three kinds of evidence.** "Explain a limit order book, the bid-ask spread, and market against limit orders" is an explanation, best given aloud and marked against a rubric. "Derive put-call parity" is a derivation. "Price a European option on a binomial tree in Python" is code with tests. The exit therefore needs `free-response` with voice and rubric marking (section 5), `parity-lab` with `derivation-steps`, and `code-cell` linked to `binomial-tree`.
2. **The weekly probability habit begins at 1.5.** The curriculum's "three interview-style probability problems a week from item 1.5 onwards" falls inside P0. No sibling catalogue specifies a workbench for it, so `puzzle-workbench` core and `scratch-pad` are P0 here, and the 3.3 interview features (cold mode, think-aloud, book log) are P2 modes of the same widget.
3. **"Alongside 1.3 to 1.6" conflicts with the priority rule.** P0 ends at 1.5, so a learner following the curriculum's schedule would reach 1.7 before it is built. Decision 14 resolves it.
4. **The 2.3 deliverables live outside the app.** Tests, a README, a results note and a GitHub repository cannot be produced inside a browser lesson. The app can teach each component, rehearse it on synthetic data, verify milestones by pasted output and by starter test suites the learner downloads and runs, and review the results note. `results-note` and the `setup-checklist` project mode (programming cluster) carry this.
5. **The 3.3 exit cannot be fully machine-verified.** "Ten mock interviews, at least three with a stranger" is self-declared in the `mock-interview` log. "80% of the probability chapter in Zhou solved cold" uses the learner's own book through `puzzle-workbench` `book-log` mode, alongside our recreated equivalents.
6. **Market-making and betting games are applied probability under a clock.** Grading needs exact posterior means and variances for card and dice quantities, so this cluster depends on the probability cluster's `rational`, `dist` and enumeration services.
7. **Microstructure needs a fuller exchange than the exit test implies.** Harris's chapters, the 3.1 Avellaneda and Stoikov replication and the 2.3.4 feed handler need call auctions, stop and iceberg orders, amend rules, fees and a message feed. `exchange-sim` includes them from the start, because retrofitting order types into a matching engine breaks its invariants.
8. **Some interview facts are firm-specific and unverified.** Whether a given firm's 80-in-8 test marks wrong answers negatively, or offers multiple choice, is [unverified]. Such details are configuration in `speed-drill`, never code.
9. **The 1.1 exit already computes finance numbers.** Returns, annualised volatility and maximum drawdown are taught in 1.1 by `drawdown-lab` (programming cluster). 1.7 builds on that widget rather than re-teaching returns.

### 0.3 Names against the sibling catalogues

This file uses the names the programming catalogue adopted from the calculus and linear algebra catalogue. The engine blueprint picks the final names; the mapping is mechanical.

| Used here | Stage 0 file | Probability file | Notes |
|---|---|---|---|
| `plot-2d` | `plot-axes` | `plot-axes` | Host for every chart here |
| `marks` | `curve-layer`, `geo-layer`, `bar-layer` | `marks` | Section 4.1 adds candles, depth steps, payoff kinks, cash-flow arrows and bands |
| `drag-point` | `draggable-point` | `draggable-point` | |
| `region-select` | `region-selector` | `region-selector` | |
| `value-table` | `data-table` | `data-table` | Section 4 adds blotter and chain presets |
| `live-formula` | `tex-terms` | `tex-terms` | |
| `slider`, `stepper`, `token-tray`, `number-line`, `sim-runner` | same | same | |
| `choice`, `numeric-input`, `expression-input`, `free-response`, `derivation-steps` | `choice-cards`, `numeric-entry`, `expression-entry`, `free-response`, `derivation` | Stage 0 names | |
| `speed-timer`, `keypad`, `card-sort`, `speed-drill`, `strategy-trainer`, `fermi-estimator`, `multiplier-chain` | same | same | Stage 0 owns them |
| `code-cell`, `code-surface`, `node-link`, `array-strip`, `cell-grid`, `json-explorer`, `schema-builder`, `setup-checklist`, `drawdown-lab`, `time-series-lab`, `bench-lab` | | | Programming cluster owns them |
| `mass-editor`, `chance-object`, `node-graph`, `game-lab`, `first-step-solver`, `multiple-testing`, `dist-explorer`, `gaussian-2d`, `regression-lab` | | | Probability cluster owns them |
| `sketch-pad`, `plot-3d`, `matrix`, `gbm-lab`, `hedging-sim`, `measure-change`, `path-simulator`, `series-explorer`, `lagrange-explorer`, `convexity-chord` | | | Calculus and linear algebra cluster owns them |
| `binomial-tree` | | | Moves to this catalogue (section 5.1) |
| Element ids `kind:name` | `kind-name` | `kind:name` | `level:10005`, `order:o7`, `leg:2`, `flow:3`, `handle:K1` |

### 0.4 Priority and waves

| Wave | Priority | Content | Widgets |
|---|---|---|---|
| D4 (probability cluster's wave) | P0 | Weekly interview problems from 1.5 | `puzzle-workbench` (weekly, practice and book-log modes), `scratch-pad`; services `problem-bank` |
| G1 | P1 | 1.7.1 to 1.7.4: time value, shares, bonds, the order book | `cashflow-timeline`, `price-ladder`, `order-ticket`, `voice-capture`, `compounding-lab`, `tvm-timeline`, `share-lab`, `margin-lab`, `portfolio-lab`, `bond-lab`, `yield-curve-lab`, `duration-lab`, `order-book`, `auction-lab`; services `finance-core` (rates and bonds), `exchange-sim`, `ledger` |
| G2 | P1 | 1.7.5 and 1.7.6: forwards, futures, payoffs, bounds, parity | `position-editor`, `carry-arb`, `futures-mtm`, `hedge-lab`, `payoff-builder`, `option-bounds`, `parity-lab`, `option-chain` |
| G3 | P1 | 1.7.7 to 1.7.9: binomial trees, Black-Scholes, Greeks, microstructure | `quote-entry`, `binomial-tree` (owned now), `bs-explorer`, `greeks-lab`, `pnl-attribution`, `iv-solver`, `tape-lab`, `adverse-selection`, `dealer-sim`, `execution-lab`; services `finance-core` (options), `market-gen` (flow) |
| H | P2 | 2.3 projects | `backtest-lab`, `sharpe-lab`, `signal-lab`, `vol-surface`, `pricer-compare`, `feed-sim`, `candle-builder`, `latency-lab`, `order-lifecycle`, `paper-trader`, `results-note`; services `backtest-core`, `market-gen` (cross-sections, chains, ticks) |
| J | P2 | 3.3 interviews | `bet-lab`, `kelly-lab`, `mm-game`, `calibration-lab`, `mock-interview`, `puzzle-workbench` (cold and aloud modes); services `speech`, `interview-engine` |

Inside each wave, primitives ship before the composites that use them. Features of P1 widgets that only 2.3 or 3.3 need are marked P2 in their entries.

---

## 1. Lesson map: what the learner does to get each idea

Each table row is one lesson idea in depth-first order: the action that makes the idea land, the widgets that provide it, and how the screen is checked. Every lesson follows design research section 8.3 (hook, explore, name, ladder, trap, generalise and derive, transfer, summary, quiz); the "Act" column names the hook or the central action.

### 1.1 Finance basics (1.7, 100 h)

**1.7.1 Interest, compounding and the time value of money** (12 lessons; Khan Academy interest and debt; Hull chapter 4 on compounding). Currency: pounds sterling, because the course frames money personally (savings, loans, mortgages) before markets.

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Interest is rent on money; simple interest | Predict the balance after 5 years at 10% simple, then drag the years slider to see it | compounding-lab (simple) | numeric |
| 2 | Compound interest: interest earns interest | Stack each year's interest block on the balance; predict year 10 before it appears | compounding-lab (blocks), multiplier-chain | numeric |
| 3 | Doubling time and the rule of 72 | Drag the rate and read the doubling time; compare with $72/(100r)$ and the exact $\ln 2/\ln(1+r)$ | compounding-lab (doubling) | numeric |
| 4 | Compounding frequency; APR against the effective annual rate | Split the year into $m$ periods and watch the effective rate climb towards a ceiling | compounding-lab (frequency) | numeric |
| 5 | Continuous compounding and $e$; converting between conventions | Push $m$ towards infinity; convert 5% continuous into an annual rate | compounding-lab (continuous) | numeric, expression |
| 6 | Present value: discounting | Slide a £1,000 cash flow back along the timeline and watch it shrink | tvm-timeline (pv) | numeric |
| 7 | Net present value and the decision rule | Place a project's cash flows; find the rate where NPV crosses zero (the IRR) | tvm-timeline (npv, irr) | numeric |
| 8 | Perpetuities and annuities | Collapse an endless stream with the shift trick; an annuity is the difference of two perpetuities | tvm-timeline (annuity), series-explorer | expression, numeric |
| 9 | Loans and amortisation | Drag the monthly payment until a mortgage balance reaches zero in year 25; watch interest and principal trade places | tvm-timeline (amortise) | numeric |
| 10 | Real against nominal; inflation | Deflate a future cash flow; derive $(1 + n) = (1 + r)(1 + \pi)$ | compounding-lab (real) | numeric, expression |
| 11 | Trap: rates quoted under different conventions | Rank 12% APR compounded monthly against 12.5% compounded annually | compounding-lab (compare) | ordering |
| 12 | Transfer: the discount factor as the price today of £1 at a later date | Drag discount-factor knots to price a three-flow stream (bridge to bonds) | tvm-timeline (discount factors) | numeric |

**1.7.2 Shares, returns and portfolios** (15 lessons; Khan stocks and ownership; Varsity "Introduction to Stock Markets"; Hull chapter 1; portfolio theory at an introductory level). Currency from here on: US dollars, written "USD" in prose.

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | A share is a slice of a company; market capitalisation | Cut the company into shares; set the price; read the market cap | share-lab (ownership) | numeric |
| 2 | How shares come to exist: primary and secondary markets, IPOs, issuance dilutes | Issue new shares and watch each slice shrink while cash grows | share-lab (issue), card-sort | numeric, mapping |
| 3 | Dividends and the ex-dividend price drop | Step through the ex-date: cash leaves the company; predict the opening price | share-lab (dividend) | numeric |
| 4 | Splits, buybacks and adjusted prices | Apply a 2-for-1 split; repair the chart's fake crash with an adjustment factor | share-lab (split) | numeric, set |
| 5 | Total return | Reinvest dividends and compare total return with price return | share-lab (total-return), drawdown-lab (returns) | numeric |
| 6 | Arithmetic against geometric mean; volatility drag | +50% then −50%: predict the end value first | multiplier-chain (returns preset), gbm-lab (1.7 mode) | numeric, choice |
| 7 | Long and short: asymmetric P&L | Drag the price and compare the long and short P&L lines; where is the loss unbounded? | margin-lab (long-short) | choice, numeric |
| 8 | Margin, gearing and the margin call | Buy on margin; drag the price down until the account hits maintenance; find that price | margin-lab (margin) | numeric |
| 9 | Short-sale accounts, borrow fees and squeezes | Run a short through a rally; the fee accrues and equity drains | margin-lab (short) | numeric |
| 10 | Indices: price-weighted against capitalisation-weighted | Build both from four stocks; a split changes one index's divisor | share-lab (index) | numeric |
| 11 | Risk and return; two-asset diversification | Slide the weight between two stocks and trace the portfolio's path in $(\sigma, \mu)$ | portfolio-lab (two-asset) | point, numeric |
| 12 | Correlation and the minimum-variance portfolio | Drag $\rho$ from 1 to −1; find the weight with the least risk | portfolio-lab (two-asset), lagrange-explorer (optional) | point, numeric |
| 13 | The efficient frontier, the risk-free asset and the Sharpe ratio | Rotate a line from the risk-free rate until it touches the frontier | portfolio-lab (frontier, cml) | point |
| 14 | Beta and systematic risk | Fit the line through stock-against-market returns; split variance into systematic and idiosyncratic | portfolio-lab (beta), regression-lab | numeric |
| 15 | Trap: "more stocks always remove risk" | Add stocks with $\rho = 0.3$ and watch risk floor at $\sqrt{\rho}\,\sigma$ | portfolio-lab (n-asset) | numeric |

**1.7.3 Bonds and the yield curve** (17 lessons, one optional; Khan bonds; Hull chapter 4).

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | A bond is a stream of cash flows | Build a 5-year 4% annual-coupon bond on the timeline | bond-lab (cashflows) | state |
| 2 | Price is the present value; price and yield move inversely | Drag the yield and watch every discounted arrow and the price respond | bond-lab (price-yield) | numeric, choice |
| 3 | Par, premium and discount | Predict which of three bonds trades above 100 | bond-lab (price-yield) | choice |
| 4 | Yield to maturity by root-finding | Drag the yield until the present value meets the quoted price | bond-lab (ytm) | numeric |
| 5 | Pull to par | Hold the yield and move the valuation date towards maturity | bond-lab (pull-to-par) | curve |
| 6 | Zero-coupon bonds and discount factors | Price a strip from a discount factor, then the reverse | yield-curve-lab (discount-factors) | numeric |
| 7 | Bootstrapping zero rates | Peel each maturity's zero rate off a coupon bond, shortest first | yield-curve-lab (bootstrap) | numeric per maturity |
| 8 | Forward rates | Two routes to year 2 must cost the same; solve for the forward | yield-curve-lab (forwards) | numeric |
| 9 | Curve shapes and moves: shift, steepen, twist | Drag curve knots; predict which bond loses most | yield-curve-lab (shapes) | choice |
| 10 | Duration as a balance point | Balance the seesaw of present-value blocks on the timeline | duration-lab (fulcrum) | numeric |
| 11 | Modified duration and DV01 | Read the tangent's slope on the price-yield curve; predict the price after +1 basis point | duration-lab (tangent) | numeric |
| 12 | Convexity | Add the curvature term; compare errors for ±200 basis points | duration-lab (convexity) | numeric |
| 13 | Immunisation | Match a liability's value and duration with two bonds | duration-lab (immunise) | numeric |
| 14 | Clean and dirty prices, accrued interest, day counts | Slide the settlement date through a coupon period and watch the sawtooth | bond-lab (accrued) | numeric |
| 15 | Credit spreads | Discount with survival probabilities; read the spread a hazard rate implies | bond-lab (credit) | numeric |
| 16 | Interest rate swaps (optional; Hull chapter 7) | Value a swap as a fixed bond minus a floating bond; find the par swap rate | yield-curve-lab (swap) | numeric |
| 17 | Trap: "a higher coupon means a longer duration" | Compare two bonds' balance points | duration-lab (compare) | choice |

**1.7.4 Exchanges and the limit order book** (13 lessons; Varsity "Introduction to Stock Markets"; Harris on orders and order-driven markets). This course carries the first part of the 1.7 exit.

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Why exchanges exist: a continuous double auction | Post a bid and an offer; watch them meet when they cross | order-book (explore) | state |
| 2 | Limit orders rest; the book is two queues | Place limit orders on the ladder; read the best bid and best ask | order-book (place) | numeric |
| 3 | The spread and the mid; tick size | Read the spread in ticks and basis points; change the tick size and watch the queue lengthen | order-book (spread) | numeric |
| 4 | Market orders cross the spread and walk the book | Predict the average fill price of a 500-share market buy before sending it | order-book (walk) | numeric |
| 5 | Price-time priority and queue position | Predict which resting order fills first | order-book (queue) | ordering |
| 6 | Market against limit: price against certainty | Race a limit order at the bid against a market order on a seeded flow; the limit may never fill | order-book (race) | choice |
| 7 | Order types and instructions: stop, stop-limit, IOC, FOK, post-only, iceberg; amending loses priority | Predict the book after each instruction | order-book (types), order-ticket | state, choice |
| 8 | Depth and slippage | Drag the order size and watch the cost curve rise | order-book (depth) | curve, numeric |
| 9 | Order book imbalance and the microprice | Predict the next mid move from queue sizes | order-book (imbalance) | numeric, choice |
| 10 | Opening and closing auctions | Find the uncrossing price that maximises traded volume | auction-lab | numeric |
| 11 | Maker-taker fees and rebates | Compute the all-in cost of taking against making | order-book (fees) | numeric |
| 12 | After the trade: clearing, the central counterparty, settlement | Order the post-trade steps | card-sort | ordering |
| 13 | Exit rehearsal: explain the book, the spread, and market against limit orders aloud | Speak or type an explanation; Bertie drafts marks against the rubric; you confirm | free-response (voice, rubric), order-book | text (rubric) |

**1.7.5 Forwards and futures** (14 lessons; Varsity "Futures Trading"; Hull chapters 2, 3 and 5).

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | A forward contract; payoff $S_T - K$ | Drag the delivery price and watch the payoff line slide | payoff-builder (forward) | curve |
| 2 | Pricing by no-arbitrage: cash and carry | Borrow, buy and agree to deliver; make the cash flows today net to zero | carry-arb (build) | numeric |
| 3 | When the quote is wrong: reverse cash and carry | Build the trade that profits from a forward quoted too low | carry-arb (arbitrage) | predicate |
| 4 | Income and costs: dividends, storage, convenience yield | Add each to the carry and derive $F_0 = S_0 e^{(r - q)T}$ | carry-arb (income), derivation-steps | expression |
| 5 | Foreign exchange forwards: covered interest parity | Two routes from pounds today to dollars in a year must agree | carry-arb (fx) | numeric |
| 6 | Valuing an existing forward | Value a contract struck last month after the forward price moved | carry-arb (value) | numeric |
| 7 | Futures: exchange-traded, standardised, settled daily | Step through a week of settlement prices; fill the variation margin column | futures-mtm (daily) | numeric |
| 8 | Margin accounts and margin calls | Drag the price path down until the account needs topping up | futures-mtm (margin) | numeric |
| 9 | Notional against margin: the gearing of futures | Compare return on margin with return on notional | futures-mtm (gearing) | numeric |
| 10 | Basis and convergence; contango and backwardation | Watch spot and futures meet at expiry; read the term structure | futures-mtm (basis, term) | choice |
| 11 | Hedging with futures: short and long hedges, basis risk | Hedge a cargo; the residual basis is what is left | hedge-lab (basic) | numeric |
| 12 | The minimum-variance hedge ratio | Drag the hedge ratio to minimise the hedged variance | hedge-lab (min-var) | point, numeric |
| 13 | Beta hedging a portfolio with index futures | Compute the contracts needed to take beta to zero | hedge-lab (beta) | numeric |
| 14 | Trap: "the futures price is the market's forecast of the spot price" | Change the interest rate and watch the fair futures price move with no change in forecasts | carry-arb (trap) | choice |

**1.7.6 Options: payoffs, strategies, bounds and put-call parity** (17 lessons; Varsity "Options Theory for Professional Trading"; Hull chapters 10 to 12).

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | A call is the right to buy; payoff $\max(S_T - K, 0)$ | Drag the stock's final price and watch the call's payoff | payoff-builder (single leg) | curve |
| 2 | Puts; long and short; who bears which risk | Flip a leg's side and predict the new diagram | payoff-builder | curve, choice |
| 3 | Payoff against profit; the premium; break-even | Subtract the premium; find the break-even | payoff-builder (profit) | numeric |
| 4 | Moneyness, intrinsic value and time value | Split a quoted price into intrinsic and time value | payoff-builder (value today), option-chain (read) | numeric |
| 5 | Reading an option chain | Find the mid, the spread and the most liquid strike | option-chain (read) | numeric, set |
| 6 | Vertical spreads | Build a bull call spread; read its maximum profit and loss | payoff-builder | curve, numeric |
| 7 | Straddles and strangles: positions on volatility | Build a straddle; predict when it pays | payoff-builder | curve, choice |
| 8 | Butterflies and condors | Build a butterfly; see it as a bet that the price lands near one strike | payoff-builder | curve |
| 9 | Covered calls, protective puts and collars | Build each from stock plus options | payoff-builder | curve |
| 10 | Any piecewise-linear payoff is a sum of calls | Match a target payoff with the fewest legs | payoff-builder (match) | payoff |
| 11 | No-arbitrage bounds | Drag a quoted call price outside the shaded region; build the arbitrage | option-bounds | region, predicate |
| 12 | Early exercise of American calls on non-dividend stocks | Show the call is worth more alive than exercised | option-bounds (american) | choice |
| 13 | Put-call parity: two portfolios, one payoff | Slide $S_T$ and watch call plus bond equal put plus share at every price | parity-lab (overlay) | state |
| 14 | Deriving parity; conversion and reversal arbitrage | Complete the derivation; trade a parity violation | parity-lab (derive, arbitrage), derivation-steps | expression, predicate |
| 15 | Synthetic positions and the box spread | Build a synthetic long stock; price a box as a loan | parity-lab (synthetic, box) | numeric |
| 16 | Strike convexity: the butterfly cannot cost less than zero | Drag three call quotes until a butterfly becomes free money | option-bounds (strikes) | predicate |
| 17 | Exit rehearsal: derive put-call parity cold | Order and complete the derivation with no hints | derivation-steps | ordering, expression |

**1.7.7 Binomial trees** (11 lessons; Hull chapter 13). This course carries the coding part of the 1.7 exit and feeds the 1.9 C++ exit.

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | One step: replicate a call with shares and a bond | Solve for $\Delta$ and the bond holding that copy the call in both states | binomial-tree (replicate) | numeric |
| 2 | No arbitrage needs $d < e^{r \Delta t} < u$ | Push $u$ below the growth factor; build the free lunch | binomial-tree (arbitrage) | predicate |
| 3 | Risk-neutral probability; the real probability does not matter | Change $p$ and watch the price stay put; derive $q$ | binomial-tree (q derive) | numeric, choice |
| 4 | Two steps and backward induction | Fill the tree from the leaves back | binomial-tree (price) | numeric per node |
| 5 | Delta changes through the tree | Read the hedge at each node; rebalance after a move | binomial-tree (delta) | numeric |
| 6 | Calibrating the tree: Cox-Ross-Rubinstein | Set $u = e^{\sigma \sqrt{\Delta t}}$ from a volatility | binomial-tree (crr) | numeric |
| 7 | American puts and early exercise | Mark the nodes where exercising beats waiting | binomial-tree (american) | set |
| 8 | Dividend yield in the tree | Change the growth rate to $r - q$ | binomial-tree (dividend) | numeric |
| 9 | Convergence and the odd-even wobble | Raise $N$; watch the price oscillate onto the Black-Scholes value | binomial-tree (converge) | choice, numeric |
| 10 | Code: one array, backward induction | Write the pricer; the tree lights each layer your array holds | code-cell, binomial-tree (vector) | code |
| 11 | Exit: price a European option on a binomial tree in Python | Hidden tests, no hints | code-cell | code |

**1.7.8 Black-Scholes and the Greeks** (17 lessons; Hull chapters 15 and 19; Natenberg optional).

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Prices as lognormal | Predict whether the median path ends above the start when $\mu = 5\%$, $\sigma = 40\%$ | gbm-lab (1.7 mode), dist-explorer (lognormal) | choice, numeric |
| 2 | From the tree to the formula | Raise $N$ in the tree until it agrees with the formula | binomial-tree (converge), bs-explorer | numeric |
| 3 | Reading the formula: an asset-or-nothing minus a cash-or-nothing claim | Split the call price into its two pieces | bs-explorer (decompose) | numeric |
| 4 | $N(d_2)$ is the risk-neutral chance of finishing in the money | Shade the lognormal density above $K$ | bs-explorer (density) | numeric |
| 5 | How each input moves the price | Predict the sign table, then test each slider | bs-explorer (inputs) | choice |
| 6 | The price curve against the stock at several expiries; time value collapses | Sketch the curve a week before expiry, then reveal | bs-explorer (slices), sketch-pad | curve |
| 7 | The at-the-money shortcut $C \approx 0.4\,\sigma\sqrt{T}\,S$ | Price five at-the-money calls in your head; compare | bs-explorer (atm), speed-drill (options deck) | numeric |
| 8 | Delta: slope and hedge ratio | Drag the tangent along the price curve; read $N(d_1)$ | greeks-lab (delta) | numeric, point |
| 9 | Gamma: curvature; the at-the-money spike near expiry | Find where gamma peaks; watch it sharpen as expiry nears | greeks-lab (gamma) | point, choice |
| 10 | Theta: time decay | Compare yesterday's and today's curves | greeks-lab (theta) | numeric |
| 11 | Vega and rho | Shift volatility by one point; read the change | greeks-lab (vega, rho) | numeric |
| 12 | Greeks of a position | Build a straddle; read its Greeks; make it delta-neutral | greeks-lab (portfolio), position-editor | numeric, predicate |
| 13 | P&L explained by the Greeks | Split a day's P&L into delta, gamma, theta and vega pieces | pnl-attribution | numeric |
| 14 | Delta hedging one path; gamma pays for theta | Hedge daily and compare realised with implied volatility | hedging-sim (one-path) | choice, numeric |
| 15 | Implied volatility | Drag $\sigma$ until the model price meets the market price | iv-solver | numeric |
| 16 | The smile: Black-Scholes assumptions fail | Solve five strikes; the implied volatilities are not equal | iv-solver (smile), option-chain | choice |
| 17 | Trap: "higher volatility makes a put cheaper, because the stock might rise" | Test it with the vega slider | bs-explorer | choice |

**1.7.9 Market microstructure** (13 lessons; Harris, Trading and Exchanges; Glosten and Milgrom; Roll).

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Who trades and why: Harris's taxonomy | Sort traders into utilitarian, profit-motivated, informed, uninformed, dealers | card-sort | mapping |
| 2 | Liquidity: width, depth, immediacy, resilience | Replay a large order and watch the book refill | order-book (resilience) | choice |
| 3 | The tape: classify each trade as buyer- or seller-initiated | Tag trades by the quote rule, then the tick rule | tape-lab (classify) | set |
| 4 | Quoted, effective and realised spreads; price impact | Compute each for five trades | tape-lab (spreads) | numeric |
| 5 | Bid-ask bounce and Roll's estimator | Read the negative autocovariance in the scatter; recover the spread | tape-lab (roll) | numeric |
| 6 | Why spreads exist, part 1: costs and inventory | Quote against noise traders; widen and skew to control inventory | dealer-sim (inventory) | numeric, choice |
| 7 | Why spreads exist, part 2: adverse selection | Set the bid and ask that break even against informed traders | adverse-selection (glosten-milgrom) | numeric |
| 8 | Price discovery: beliefs converge as trades arrive | Update the quote after each trade; watch the spread narrow | adverse-selection (sequence) | numeric, curve |
| 9 | Market impact: temporary, permanent, the square-root law | Split a parent order and compare costs | execution-lab (impact) | numeric |
| 10 | Execution benchmarks: TWAP, VWAP, implementation shortfall | Choose a schedule and score it against arrival price | execution-lab (schedule) | numeric |
| 11 | Market-making economics: earn the spread, pay adverse selection | Decompose a dealer's P&L | dealer-sim (decompose) | numeric |
| 12 | Market structure: fragmentation, dark pools, latency races | Match each venue feature to the trader it serves | card-sort, free-response | mapping, text |
| 13 | Tick size, queue priority and who wins | Halve the tick; predict the change in spread and queue length | order-book (tick) | choice |

**Coverage of the 1.7 exit.** Limit order book, spread, market against limit: 1.7.4 L1 to L6 and L13. Derive put-call parity: 1.7.6 L13, L14 and L17. Price a European option on a binomial tree in Python: 1.7.7 L10 and L11.

### 1.2 Projects (2.3, 400 h)

Projects are built on the learner's machine (decision 7). Each project has a short concept course in the app, then a project hub: milestones, starter test suites to download, verification by pasted output, and a results note reviewed against a rubric.

**2.3.0 Project method** (shared by all five; 5 lessons)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | What a professional reader looks for | Rank five results notes from most to least credible | card-sort | ordering |
| 2 | Tests for numerical code: invariants, tolerances, golden files | Write the invariant tests for a toy pricer | code-cell (pytest) | code |
| 3 | The results note, including what failed | Fill a note's skeleton from pasted metrics | results-note (guided) | predicate, text |
| 4 | Treat a Sharpe above 2 as a bug | Find the bug in three too-good backtests | backtest-lab (hunt) | set |
| 5 | Repository hygiene: README, licence, CI, caching data to disk | Complete the project checklist | setup-checklist (project) | state |

**2.3.1 Backtesting engine** (13 lessons; López de Prado; Bailey and López de Prado)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | A backtest replays history using only what was known then | Step the event loop one bar at a time; the future is locked | backtest-lab (step) | ordering |
| 2 | Signal at the close, trade at the next open | Predict the fill price under each timing rule | backtest-lab (timing) | choice |
| 3 | Look-ahead bias | Toggle `shift(-1)`; predict the effect first; the equity curve becomes too good | backtest-lab (bias), time-series-lab (shift) | choice, set |
| 4 | Survivorship bias | Switch from today's universe to the point-in-time universe | backtest-lab (bias) | numeric |
| 5 | Transaction costs and slippage | Sweep the cost per trade; find the break-even cost | backtest-lab (costs), execution-lab | numeric |
| 6 | Position sizing and volatility targeting | Compare fixed size with volatility-targeted size | backtest-lab (sizing) | numeric |
| 7 | Metrics: Sharpe, Calmar, maximum drawdown | Compute each from a returns series | sharpe-lab, drawdown-lab (Sharpe, Calmar modes) | numeric |
| 8 | How noisy is a Sharpe ratio? | Run null strategies; read the spread of their Sharpe ratios for 3 years of data | sharpe-lab (null) | numeric |
| 9 | The held-out period and walk-forward testing | Bracket the in-sample and held-out periods; never touch the held-out until the end | backtest-lab (holdout) | choice |
| 10 | Backtest overfitting and the deflated Sharpe ratio | Pick the best of 200 noise strategies; deflate its Sharpe | multiple-testing (strategy zoo), sharpe-lab (deflated) | numeric, choice |
| 11 | Engine architecture: data, strategy, portfolio, execution | Connect the components and name what crosses each boundary | backtest-lab (architecture), node-link | mapping |
| 12 | Testing a backtester: cash plus positions equals equity; no fill before its signal | Write the invariants against our starter suite | code-cell (pytest), setup-checklist (project) | code |
| 13 | Project: build it, test it, write the results note | Milestones, pasted outputs, note review | setup-checklist (project), results-note | state, text |

**2.3.2 Alpha signal research** (12 lessons; Jegadeesh and Titman; Grinold and Kahn)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Cross-sectional against time-series signals | Sort the same data both ways and say what each bets on | signal-lab (universe) | choice |
| 2 | Momentum (12 months, skipping the last) and short-term reversal | Build the signal from return windows; rank the stocks | signal-lab (construct) | ordering, numeric |
| 3 | Normalising: ranks, z-scores, winsorising | Drag an outlier and watch each normalisation react | signal-lab (normalise) | choice |
| 4 | Neutralising sectors and the market | Demean within sectors; watch the sector bet vanish | signal-lab (neutralise) | numeric |
| 5 | The information coefficient | Read the rank correlation between signal and next month's return on one date | signal-lab (ic) | numeric |
| 6 | IC over time: mean, IC information ratio, t-statistic | Read the IC series; is a mean IC of 0.03 real over 10 years? | signal-lab (ic-series) | numeric |
| 7 | The fundamental law: information ratio about $\mathrm{IC}\sqrt{\text{breadth}}$ | Change the universe size and watch the ratio | signal-lab (breadth) | numeric |
| 8 | IC decay by horizon | Predict which horizon carries the most IC | signal-lab (decay) | choice |
| 9 | Quantile portfolios and the long-short spread | Check that the quantile bars rise in order | signal-lab (quantiles) | ordering, choice |
| 10 | Turnover and its cost | Smooth the signal; trade off IC against turnover | signal-lab (turnover) | numeric |
| 11 | Sharpe after costs; capacity | Add costs; find the cost at which the signal dies | signal-lab (net), backtest-lab (costs) | numeric |
| 12 | Project: momentum and reversal across a few hundred shares | Milestones, pasted outputs, note review | setup-checklist (project), results-note | state, text |

**2.3.3 Options analytics dashboard** (11 lessons; Hull; Gatheral)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Cleaning an option chain: mids, stale quotes, crossed markets | Tap every quote you would discard | option-chain (clean) | set |
| 2 | Implied volatility by root-finding | Step Newton's method; switch to bisection when vega is tiny | iv-solver (algorithm) | ordering, numeric |
| 3 | The implied forward from put-call parity | Read the forward from call minus put across strikes | option-chain (parity), parity-lab | numeric |
| 4 | Smile and skew | Plot implied volatility against strike for one expiry; say why puts are dearer | vol-surface (smile) | choice |
| 5 | Term structure and total variance | Plot $\sigma^2 T$ against log-moneyness for each expiry | vol-surface (total-variance) | curve, choice |
| 6 | No-arbitrage checks: calendar and butterfly | Find the strikes where the implied density turns negative | vol-surface (arbitrage) | set |
| 7 | Fitting a smile (SVI) | Drag five parameters until the curve fits the dots | vol-surface (svi) | predicate |
| 8 | Greeks across strikes and expiries | Read where gamma and vega concentrate | greeks-lab (surface) | point |
| 9 | Three pricers compared: formula, tree, Monte Carlo | Plot error against compute for each | pricer-compare | numeric |
| 10 | Monte Carlo error and variance reduction | Add antithetic paths and a control variate; read the standard error | pricer-compare (mc) | numeric |
| 11 | Project: the dashboard on yfinance or Deribit data | Milestones, pasted outputs, note review | setup-checklist (project), results-note | state, text |

**2.3.4 Live market data handler** (12 lessons)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Ticks: trades and quotes; message anatomy | Pick out the fields a candle needs from a raw message | feed-sim (messages), json-explorer | set |
| 2 | Websockets: subscribe, heartbeat, reconnect with backoff | Put the reconnect steps in order; fill the backoff delays | feed-sim (connection) | ordering, numeric |
| 3 | Sequence numbers, gaps, snapshot plus deltas | Rebuild the book from messages; find the gap; resynchronise | feed-sim (book) | set, state |
| 4 | Candles: open, high, low, close, volume | Fill one minute's candle from its ticks | candle-builder (aggregate) | numeric |
| 5 | Bar boundaries and labels | Drag the boundary; decide which bar a tick at exactly 10:01:00 belongs to | candle-builder (boundaries) | mapping |
| 6 | Multi-timeframe roll-ups | Build a 5-minute bar from five 1-minute bars, not from the ticks | candle-builder (rollup) | numeric |
| 7 | Late and out-of-order ticks; finalising bars | A tick arrives 3 seconds late: amend or drop? | candle-builder (late) | choice |
| 8 | Clocks and timestamps | Separate exchange time from receive time; measure a one-way delay | latency-lab (clocks) | numeric |
| 9 | Latency percentiles and tails; coordinated omission | Place the p50, p99 and p99.9 handles on the histogram | latency-lab (percentiles) | point, numeric |
| 10 | Queues and bursts; backpressure | Raise the arrival rate towards capacity and watch the queue | latency-lab (queue) | choice |
| 11 | Storage: PostgreSQL tables or Redis streams; idempotent writes | Design the candle table; write the upsert | schema-builder, code-cell (sql) | state, code |
| 12 | Project: ticks to multi-timeframe candles with latency measured | Milestones, pasted outputs, note review | setup-checklist (project), results-note | state, text |

**2.3.5 Paper trading bot** (9 lessons)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Architecture: data, strategy, risk, orders, paper broker | Connect the components | order-lifecycle (architecture) | mapping |
| 2 | Indicators: EMA, RSI, Supertrend | Compute one value of each by hand from a short series | paper-trader (indicators) | numeric |
| 3 | Rules as a state machine | Build "flat, long, short" from rule tokens | paper-trader (rules) | state |
| 4 | Order lifecycle | Apply acks, fills and cancels to an order's state | order-lifecycle (states) | ordering, state |
| 5 | Idempotency and reconciliation after a crash | Reconcile the bot's records with the broker's | order-lifecycle (recovery) | set, choice |
| 6 | Risk limits and the kill switch | Mark which orders the risk layer must reject | order-lifecycle (risk) | set |
| 7 | Does it beat chance? | Compare the strategy with random entries of the same turnover | paper-trader (null) | numeric, choice |
| 8 | Logging and observability | Choose what to log and what never to log | card-sort, free-response | mapping, text |
| 9 | Project: paper trading only, built on projects 1 and 4 | Milestones, pasted outputs, note review | setup-checklist (project), results-note | state, text |

### 1.3 Interview preparation (3.3, 250 h)

**3.3.1 Mental arithmetic for trading tests** (6 lessons, then daily drills; Stage 0's `speed-drill` and `strategy-trainer` carry it)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | The formats: Zetamac at 50, 80 in 8 | Sit a baseline of each | speed-drill (zetamac, eighty-in-eight) | state (score) |
| 2 | Decimals and fractions at speed | Drill the fraction-to-decimal anchors | speed-drill (deck), strategy-trainer | numeric |
| 3 | Percentages and multiplying decimals | Strategy drills, then timed sets | strategy-trainer, speed-drill | numeric |
| 4 | Estimation under a clock | Answer within 5% in 10 seconds | speed-drill (estimation deck) | numeric (factor tolerance) |
| 5 | Trading arithmetic: expected values, odds, quick option values | Timed decks of EV, odds conversion and at-the-money option prices | speed-drill (ev, odds, options decks) | numeric |
| 6 | Pacing: skip, return, guess policy | Run 80-in-8 with your skip rule; compare scores | speed-drill (eighty-in-eight) | state |

**3.3.2 Probability and brainteasers** (14 lessons, then the books in order: Mosteller, Zhou, Crack, Joshi)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Clarify, restate, choose notation | Rewrite a vague problem precisely before solving | puzzle-workbench (practice) | text (rubric) |
| 2 | Small cases and patterns | Solve $n = 1, 2, 3$ and guess the rule | puzzle-workbench, value-table | numeric |
| 3 | Symmetry | Find the symmetric event that halves the work | puzzle-workbench, outcome-grid | numeric |
| 4 | Complements | Count the opposite event | puzzle-workbench, counting-slots | numeric |
| 5 | Linearity of expectation and indicators | Write the indicator sum; ignore dependence | puzzle-workbench, indicator-board | expression |
| 6 | Conditioning and first-step analysis | Write one equation per state | puzzle-workbench, first-step-solver | numeric |
| 7 | Waiting times for patterns (HH against HT) | Build the state chain for each pattern | puzzle-workbench, first-step-solver | numeric |
| 8 | Geometric probability | Shade the region and take its area | puzzle-workbench, geo-prob | numeric |
| 9 | Optimal stopping and dynamic programming | Fill the value table backwards | puzzle-workbench, game-lab (dice-stop) | numeric |
| 10 | Random walks and martingales | Use the optional stopping argument | puzzle-workbench, path-simulator, lattice-walk | numeric |
| 11 | Sanity checks and bounds | Reject three answers by bounds alone | puzzle-workbench | choice |
| 12 | Order statistics and continuous puzzles | Break a stick; find the expected shortest piece | puzzle-workbench, order-statistics | expression |
| 13 | Speaking while solving | Solve aloud; read back your transcript against the rubric | puzzle-workbench (aloud), voice-capture | text (rubric) |
| 14 | Cold solving under time | Ten problems, no hints, 10 minutes each | puzzle-workbench (cold) | numeric, expression |

**3.3.3 Expected value, betting games and Kelly sizing** (12 lessons)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | The expected value of a bet; the fair price to play | Price a die game before seeing the outcomes table | bet-lab (ev) | numeric |
| 2 | Odds formats, implied probability, the bookmaker's margin | Convert decimal, fractional and American odds; sum implied probabilities | bet-lab (odds) | numeric |
| 3 | Variance and the risk of ruin | Bet everything every time on a favourable coin; watch ruin | kelly-lab (paths) | choice |
| 4 | When to hedge: locking in a profit | Prices moved in your favour; size the hedge that equalises outcomes | bet-lab (hedge) | numeric |
| 5 | Arbitrage across bookmakers | Spread stakes so every outcome pays the same | bet-lab (arbitrage) | predicate |
| 6 | Kelly: maximise the expected log of wealth | Drag $f$ along the growth curve to its peak | kelly-lab (curve) | point, numeric |
| 7 | Over-betting: twice Kelly grows at about zero | Run paths at $f^*$, $2f^*$ and $3f^*$ | kelly-lab (compare) | choice |
| 8 | Fractional Kelly: give up a little growth for a lot less pain | Read growth and drawdown at half Kelly | kelly-lab (fractional) | numeric |
| 9 | Several outcomes; several bets at once | Allocate stakes over outcomes with the mass editor | kelly-lab (multi) | numeric |
| 10 | Uncertain edge | Shrink the fraction when $p$ is estimated | kelly-lab (uncertain) | choice, numeric |
| 11 | Continuous Kelly: $f^* = (\mu - r)/\sigma^2$ | Size a position in a stock | kelly-lab (continuous) | numeric |
| 12 | Interview betting games | Play "pay to roll", "double or nothing" and card bets; price before playing | bet-lab (game), game-lab | numeric |

**3.3.4 Market-making games** (11 lessons; Jane Street's Probability and Markets guide)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Anatomy of a market: "30 at 35, 10 up" | Enter a two-sided quote; read its width and centre | mm-game (anatomy), quote-entry | quote |
| 2 | Centre on the expected value | Make a market on the sum of two dice | mm-game (dice) | quote |
| 3 | Width from uncertainty | Set a 90% interval for five quantities, then quote | calibration-lab, mm-game (width) | interval, quote |
| 4 | What a trade tells you | The interviewer lifts your offer; update | mm-game (update) | quote, numeric |
| 5 | Inventory and skew | Long 30 contracts: move your market so you sell more than you buy | mm-game (inventory) | quote |
| 6 | Information arrives: re-quote as cards are revealed | Quote before and after each reveal | mm-game (sequential) | quote |
| 7 | Markets on estimates (Fermi) | Quote on the number of piano tuners in London | mm-game (fermi), fermi-estimator | quote |
| 8 | Several counterparties; stale quotes get picked off | Re-quote fast after news | mm-game (multi-bot) | state (score) |
| 9 | Pricing correlated products: the sum and the parts | Quote on two dice and on their sum; keep them consistent | mm-game (linked) | predicate |
| 10 | Spoken market-making | Quote aloud; Bertie plays the interviewer | mm-game (interview), voice-capture | quote, text (rubric) |
| 11 | Partner play | One person quotes, one trades; swap roles | mm-game (partner) | state |

**3.3.5 Mock interviews spoken aloud** (8 lessons, then ten logged mocks)

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | What interviewers mark | Mark an annotated transcript with the rubric | mock-interview (review) | text (rubric) |
| 2 | Thinking aloud | Re-solve a known problem aloud; compare transcripts | puzzle-workbench (aloud) | text (rubric) |
| 3 | Probability round | A 30-minute mock | mock-interview (probability) | rubric |
| 4 | Market-making round | A 30-minute mock with an embedded game | mock-interview (markets) | rubric |
| 5 | Mental maths and betting round | A 20-minute mock | mock-interview (speed) | rubric |
| 6 | Project walk-through and motivation | Present a 2.3 project; take follow-ups | mock-interview (project) | rubric |
| 7 | Be the interviewer | Run a mock for a partner from the interviewer sheet | mock-interview (partner) | state |
| 8 | The exit log: ten mocks, three with a stranger | Log mocks and review the trend | mock-interview (log) | state |

### 1.4 Coverage check against the task list

| Topic | Lessons |
|---|---|
| Shares | 1.7.2 L1 to L10 |
| Bonds | 1.7.3 |
| Interest and compounding | 1.7.1 |
| Limit order book | 1.7.4 L1 to L9, 1.7.9 L2 and L13 |
| Bid-ask spread | 1.7.4 L3, 1.7.9 L3 to L8 and L11 |
| Market against limit orders | 1.7.4 L4 and L6, 1.7.9 L9 and L10 |
| Forwards and futures | 1.7.5 |
| Option payoffs | 1.7.6 L1 to L10 |
| Put-call parity | 1.7.6 L13 to L15 and L17 |
| Binomial trees | 1.7.7 |
| Black-Scholes | 1.7.8 L1 to L7 |
| Greeks | 1.7.8 L8 to L14 |
| Microstructure | 1.7.9 |
| Backtesting engine | 2.3.1 |
| Alpha research with IC and turnover | 2.3.2 |
| Options analytics with an implied volatility surface | 2.3.3 |
| Live market data candles | 2.3.4 |
| Paper trading bot | 2.3.5 |
| Mental arithmetic, 80 in 8 | 3.3.1 |
| Market-making games | 3.3.4 |
| Betting games and Kelly sizing | 3.3.3 |
| Probability brainteasers | 3.3.2, and weekly from 1.5 |
| Mock interviews spoken aloud | 3.3.5 |

**Not covered, by decision.** Fundamental analysis of financial statements (Varsity's module) is not in the curriculum's cover list and rarely appears in quant interviews; value at risk and credit derivatives are outside 1.7's stated scope. Each would reuse `tvm-timeline`, `portfolio-lab` or `sim-runner` if the owner adds it.

---
## 2. What this cluster adds to the shared contract

The shared widget contract is proposed in `widgets-stage0.md` section 1 and `widgets-calc-linalg.md` section 2, with additions in `widgets-prob-stats-ts.md` section 2 (`secret()`, the distribution and policy checks, the seed rules) and `widgets-programming.md` section 2 (the `code` check, the `table` answer). This file assumes all of it. Where the drafts differ, the engine blueprint decides; this section states only what finance, projects and interview formats add.

### 2.1 Answer and check additions

```ts
// Additions to the shared Answer union
type Answer =
  | { type: 'position'; legs: Leg[] }                                    // position-editor hosts
  | { type: 'quote'; bid: number; ask: number; bidSize?: number; askSize?: number }   // quote-entry
  | { type: 'order'; order: OrderSpec }                                  // order-ticket
  | { type: 'cashflows'; flows: { t: number; amount: number; lane?: string }[] }      // cashflow-timeline
  | { type: 'game'; log: GameEvent[]; summary: Record<string, number> }  // mm-game, dealer-sim, bet-lab games
  | { type: 'transcript'; segments: { t0: number; t1: number; text: string;
        speaker: 'learner' | 'interviewer' | 'partner' }[] };            // voice-capture, mock-interview

interface Leg {
  id: string;
  instrument: 'stock' | 'bond' | 'cash' | 'call' | 'put' | 'forward' | 'future' | 'digital-call' | 'digital-put';
  qty: number;              // signed: + long, - short
  K?: number;               // strike or delivery price
  T?: number;               // expiry or maturity in years
  face?: number;            // bond: amount repaid at T
  premium?: number;         // price per unit today; the long pays it
}

interface OrderSpec {
  side: 'buy' | 'sell';
  type: 'limit' | 'market' | 'stop' | 'stop-limit';
  qty: number;              // integer lots
  px?: number; stopPx?: number;
  tif: 'day' | 'ioc' | 'fok' | 'gtc';
  postOnly?: boolean; displayQty?: number;
}

// Additions to the shared Check union
type Check =
  | { kind: 'payoff'; target: Leg[] | PayoffSpec; basis: 'payoff' | 'profit';
      range: [number, number]; tol: number; minimalLegs?: number }
  | { kind: 'replicates'; target: Leg[] | PayoffSpec; cost: 'equal' | 'ignore'; tol: number }
  | { kind: 'arbitrage'; prices: Record<string, Entry>; rates?: { r: Entry; q?: Entry }; tol: number }
  | { kind: 'quote'; fair: Entry; mustContainFair?: boolean; centreTol?: number;
      maxWidth?: number; minWidth?: number; skew?: { dir: 'up' | 'down'; minTicks: number } }
  | { kind: 'book'; expect: BookSnapshot; compare: 'top' | 'levels' | 'orders' }
  | { kind: 'fills'; expect: { qty: number; px: number }[]; order: 'exact' | 'vwap'; vwapTol?: number }
  | { kind: 'cashflows'; expect: { t: number; amount: Entry }[]; tol: number; netByDate?: boolean }
  | { kind: 'rubric'; rubric: RubricItem[]; model: string;
      marking: 'self' | 'tutor-draft' | 'partner'; passMark: number };

type PayoffSpec = { kinks: [number, number][]; slopeLeft: number; slopeRight: number };   // (S, payoff) points
interface RubricItem { id: string; point: string; marks: number; evidence?: 'quote-required' }
```

**How the new checks grade.**

- **`payoff`.** Two continuous piecewise-linear functions on $[0, \infty)$ are equal when they agree at $S = 0$, at every kink of either function, and in their right-tail slope. The checker evaluates exactly there, so the check is exact for strikes on the authored grid; no sampling band is needed. Digital legs add jumps, compared from the left and the right of each jump. `minimalLegs` turns "match the target" into "match it with the fewest legs".
- **`replicates`.** The learner's position and the target have equal payoffs in every terminal state (as `payoff`) and, when `cost: 'equal'`, the same price today under the screen's prices.
- **`arbitrage`.** The position costs at most zero today and pays at least zero in every state, with strict inequality somewhere. For payoffs over $S_T \in [0, \infty)$ the checker tests $S_T = 0$, every kink and the right-tail slope; for trees it tests every terminal node; for cash-flow positions it discounts every date with the screen's rates. This generalises the calculus catalogue's `arbitrage-profitable` predicate, which becomes an alias.
- **`quote`.** `fair` is the exact posterior mean given the information public at the moment of quoting, computed by the item (rationals for dice and cards). A quote passes when it contains `fair` (if required), its centre lies within `centreTol` of `fair` (or is skewed the required way for inventory tasks), and its width respects the bounds.
- **`book` and `fills`.** Predicted book states and fills are compared with `exchange-sim`'s result on the same events, in integer ticks and lots, so equality is exact.
- **`rubric`.** The shared free-text check extended with a `partner` marking mode for human interviewers and an evidence rule: Bertie's draft mark for an item must quote the learner's own words, or the mark is shown as unsupported.

**Accepted-answer rule shown after grading**, as the design research requires: "Accepted: any position with the same payoff at every price, costing 3.20 ± 0.01", "Accepted: a market containing 7 with width at most 2", "Accepted: 100.02 ± 0.0005".

**Linked mode** (contract addition). Any composite can be opened from `puzzle-workbench` with `{ linkedFrom: { problemId, params } }`: it mounts in a compact layout beside the problem, takes its parameters from the problem, and grades nothing; the problem's own check stands. It applies unchanged to `first-step-solver`, `indicator-board`, `geo-prob`, `lattice-walk`, `order-statistics`, `markov-chain`, `game-lab`, `outcome-grid`, `counting-slots` and `path-simulator`, and to this catalogue's `bet-lab` and `kelly-lab`.

### 2.2 Predicates this cluster registers

Named, pure, unit-tested; content names them and passes arguments, never code.

| Predicate | Tests | Used by |
|---|---|---|
| `is-arbitrage` | as the `arbitrage` check, for positions built inside composite state | `option-bounds`, `parity-lab`, `carry-arb`, `binomial-tree`, `bet-lab` |
| `self-financing` | the position's net cash flow today is zero within tolerance | `carry-arb`, `binomial-tree` (replicate) |
| `delta-neutral`, `gamma-neutral`, `vega-neutral` | the position's Greek is within tolerance of zero | `greeks-lab`, `hedging-sim` |
| `min-variance-hedge` | $\lvert h - h^* \rvert \le$ tol | `hedge-lab` |
| `on-frontier` | the portfolio point lies within tolerance of the efficient frontier | `portfolio-lab` |
| `balanced` | the seesaw's torque $\sum_i (t_i - D)\,PV_i$ is within tolerance of zero | `duration-lab` |
| `immunised` | value and duration of assets match the liability's within tolerance | `duration-lab` |
| `book-valid` | no crossed book; first-in-first-out within each level | `order-book`, `feed-sim` |
| `no-lookahead` | the learner's strategy, re-run with every future bar poisoned to NaN, gives identical decisions | `backtest-lab`, `code-cell` (2.3.1 drills) |
| `bars-equal` | learner bars equal the reference OHLCV exactly | `candle-builder` |
| `gap-found` | the learner flagged the first message whose sequence number skips | `feed-sim` |
| `order-state-valid` | every state transition the learner applied is legal and the final states match | `order-lifecycle` |
| `risk-gate` | exactly the orders that breach the limits are marked for rejection | `order-lifecycle` |
| `kelly-near` | $\lvert f - f^* \rvert \le$ tol, with $f^*$ computed exactly for binary bets and numerically for several outcomes | `kelly-lab` |
| `calibrated` | the session's hit rate lies inside the binomial 90% band for the nominal coverage | `calibration-lab` |
| `mm-score` | game summary thresholds: edge captured at or above $x$, every quote within the width limit, re-quoted after every informative event | `mm-game`, `dealer-sim` |
| `svi-fits` | fit error below tolerance and no butterfly or calendar violation | `vol-surface` |
| `sections-complete`, `metrics-consistent` | the note has every required section; every metric quoted in the text equals the pasted metrics | `results-note` |

### 2.3 Money, rates and conventions

- **Signs.** Cash flows are positive when received and negative when paid. Quantities are positive long and negative short. P&L is positive for a profit. Widgets always print the word ("receive", "pay", "long", "short", "profit", "loss") beside the sign.
- **Rates.** Decimals in maths, percentages in prose (design research 9.4). Every rate shows a convention chip: "simple", "annual", "semi-annual", "monthly", "continuous" (decision 4). A basis point is $10^{-4}$ and prints as "bp".
- **Time.** Years as decimals with a label ("0.5 years, 6 months"). Option expiries use ACT/365F. Annualising returns uses 252 trading days, as `drawdown-lab` does. Bond accrued interest uses the convention the item names: 30/360 for US corporate bonds, ACT/ACT for government bonds [recalled market practice], always shown.
- **Greek units.** Delta per unit of the underlying (also shown as "share-equivalent"); gamma per unit; vega per volatility point (0.01); theta per calendar day ($\Theta_{\text{year}}/365$); rho per percentage point. The unit chip sits beside every Greek, because unit confusion is the commonest Greek error in practice.
- **Parsing.** `num-parse` gains `bp` and `bps`, the suffixes `k`, `m`, `bn`, accounting negatives "(120)" in cash-flow fields, and percentages with or without the sign. `quote-entry` owns the quote shorthand.
- **Display precision.** Prices to the tick; money to the minor unit; rates to 2 decimal places of a percent; Greeks to 3 significant figures.

### 2.4 Markets, seeds and grading

1. **Never grade a random outcome** (decision 6, probability rule 1).
2. **Streams.** `data` (fixed item data: books, chains, histories), `flow:<widget>` (order flow), `bot:<name>` (each counterparty's private randomness) and `sim:<widget>` (Monte Carlo, null strategies). "New seed" changes `flow` and `sim` only.
3. **Exact posteriors.** Hidden quantities built from dice, cards and coins are enumerated exactly with BigInt rationals (up to $10^6$ outcomes; above that, by convolution of exact distributions). Fermi quantities carry an authored log-normal prior and a sourced true value.
4. **Bots are honest.** After a game, every counterparty's policy is shown: "Trader B knew the answer 30% of the time and traded only when your quote was at least 2 away from it."
5. **Exchange determinism.** Integer ticks, integer lots, sequence-numbered events. A game or lesson replays exactly from its seed and the learner's action log.
6. **Two-way verification in CI.** Every generated answer is checked by an independent implementation: Python references (SciPy, QuantLib) for pricing and bond analytics; a Python reference matching engine for books and fills (differential testing on $10^5$ random order streams per release); exact enumeration against $10^6$-trial simulation within 4 standard errors for game posteriors.
7. **Data shared with code drills** travel as literals or CSV files, as in the probability cluster's decision 7. Drills that need fresh synthetic data import `zq_market`, a pure-Python port of the relevant `market-gen` generators built on `zq_rng`.

### 2.5 Example screen as data

A Problem screen from 1.7.4 L4. The widget, the check, the misconceptions and their show-why are all data.

```json
{
  "id": "1.7.4.L4.s3",
  "type": "problem",
  "prose": "You send a market order to buy 500 shares into this book. Predict the average price you pay.",
  "widgets": [{
    "type": "order-book", "id": "ob", "label": "Order book for XYZ",
    "mode": "walk", "tick": 0.01, "lot": 100,
    "book": { "bids": [[99.98, 300], [99.97, 500], [99.95, 800]],
              "asks": [[100.01, 200], [100.02, 200], [100.04, 400]] },
    "order": { "side": "buy", "type": "market", "qty": 500, "tif": "ioc" },
    "predictFirst": true, "show": { "fills": "after-check" }
  }],
  "answer": { "type": "numeric-input", "id": "vwap",
              "fields": [{ "id": "px", "label": "Average price paid", "unit": "USD" }] },
  "check": { "kind": "numeric", "value": "100.02", "tol": { "abs": 0.0005 } },
  "misconceptions": [
    { "when": { "kind": "numeric", "value": "100.01", "tol": { "abs": 0.0005 } },
      "id": "fills-at-best-ask",
      "line": "Only 200 shares rest at 100.01. The rest comes from higher levels.",
      "showWhy": { "key": "eat-levels" } },
    { "when": { "kind": "numeric", "value": "99.995", "tol": { "abs": 0.0005 } },
      "id": "trades-at-mid",
      "line": "The mid is not a price anyone offered. A buyer pays the ask.",
      "showWhy": { "key": "cross-spread" } }]
}
```

The fills are 200 at 100.01, 200 at 100.02 and 100 at 100.04, so the average is $50{,}010 / 500 = 100.02$.

### 2.6 Visual roles for this cluster

All tokens are from `prototype/css/tokens.css`. Slot `--s1` is skipped in any view with a handle, as the sibling catalogues decided.

| Role | Style | Examples |
|---|---|---|
| Learner-controlled | `--manip` handles (20px disc, 2px white ring, 1px ink outline); the learner's resting orders as `--manip` outlined chips with a side word; the learner's quote as a `--manip` bracket; learner-built totals as 2.5px `--manip` curves | strikes, yields, hedge ratios, Kelly fraction, quotes, orders, the total payoff |
| Bid side | `--s6` violet bars at 35% fill with a 1px edge; the word "Bid"; always the left column | ladder sizes, depth, bid step lines |
| Ask side | `--s2` orange bars at 35% fill; the word "Ask"; always the right column | ladder sizes, depth, ask step lines |
| Trades | ink dots sized by quantity; a triangle pointing up for buyer-initiated, down for seller-initiated | tapes, fills on charts |
| Model or theory | `--s3` aqua, 2px; dashed for a value before expiry | Black-Scholes value curve, fair forward, efficient frontier, growth curve |
| Given market data and primary series | ink, 2px | price paths, given payoffs, equity curves |
| Benchmark or comparison | 2px dashed ink with a direct label inside book widgets; `--s6` dashed elsewhere | buy and hold, the null band, the target payoff |
| Simulated distributions | `--s2` fills at 35% (the probability cluster's "empirical" role), never inside a book widget | Monte Carlo prices, null Sharpe ratios, Kelly wealth outcomes |
| Profit and loss | `--div-pos` and `--div-neg` fills at 18% with "+" and "−" glyphs and the words "profit" and "loss"; strokes stay ink | payoff shading, P&L bars, waterfalls |
| Truth revealed after a game | 1.5px dashed ink with a label ("True sum: 23") | `mm-game`, `signal-lab` true IC |
| Cash flows | received: arrow up; paid: arrow down; ink 2px with 6px heads; present-value ghosts `--s3` at 60%; editable arrows `--manip` | timelines |
| Option legs | 1.5px lines in `--s2`, `--s6`, `--s4`, `--s5` order with direct labels ("long C100"); `--s3` is reserved for the model curve | `payoff-builder` |
| Candles | up: hollow body, 1.5px ink outline; down: filled ink body; no colour carries direction | charts in 2.3 |
| Track accent | `--fin` and `--speed` only in chrome (course cards, track buttons), never inside a canvas | |

Grading recolours answer objects only: the learner's orders, quote, total payoff, placed arrows, handles and entered fields. Book data, legs, model curves and market data never change colour.

### 2.7 Motion and show-why

- **Direct manipulation is never tweened.** Strike handles, yield handles, the $\sigma$ slider and every curve that depends on them redraw on the pointer's frame.
- **Market events are content.** When an order executes, each consumed level's bar shrinks over 160ms with an 80ms stagger, so the eye can follow the walk through the book; a resting order springs into its queue slot (`spring-snap`). Replayed flow runs at 0.5× to 8×; above 4× events cut without interpolation (the programming cluster's rule).
- **Consequence animations** play only after a learner action: discounting slides each cash flow to $t = 0$ over 480ms (`ease-morph`, 80ms stagger); the legs of a strategy translate into their sum over 600ms; the seesaw tilts with `spring-physical`.
- **Show-why** follows the declarative recipe in the calculus catalogue's section 2.6 (tween non-answer variables, highlight, annotate, 480 to 800ms). Each widget lists its keys.
- **Games** show counterparty actions with a 200ms fade and rise; there is no flash or shake on a loss.
- **Reduced motion.** Fills appear at once with a fill list; discounting shows a before-and-after pair with a Play button; springs land at once; replays step without interpolation.

### 2.8 Accessibility additions

- **Order books are grids.** Each row reads "Price 100.02. Ask 200 shares. Your order 100 shares, second in queue." The table view is one keypress away (T).
- **Prices and quotes are spoken plainly:** "one hundred point zero two"; "bid 30, ask 35, width 5".
- **Timed formats.** Every timed game and drill has an untimed practice mode. A "more time" setting multiplies limits by 1.5 and marks the score as adjusted; adjusted scores never count towards an exit test, and the screen says so (Stage 0's rule for `speed-drill`, extended).
- **Speech is never required.** Every voice path has a typed equivalent that counts the same, including towards the mock-interview log. Everything the interviewer says is captioned.
- **Charts.** Candle charts have a table view (date, open, high, low, close, volume); payoffs a table at each kink; Greeks a table by underlying price; surfaces a strike-by-expiry grid.
- **Colour.** Bids and asks carry words and fixed columns; candle direction is carried by fill; P&L carries glyphs.

### 2.9 Tutor hooks for Brainy Bertie

- **`describe('brief')`** at most 300 characters and **`describe('full')`** at most 1,500, numbers as displayed.
- **`secret()`** (the probability cluster's decision 9): true values hidden from the learner, passed to Bertie only in lesson and explore modes under a never-reveal instruction. Here: the hidden quantity in a game, the informed fraction, the true IC of a synthetic signal, the planted bias in a backtest, whether an arbitrage exists, the solution of a puzzle.
- **Element ids** use `kind:name`: `level:10002` (prices in integer ticks), `order:o7`, `leg:2`, `flow:3`, `handle:K1`, `node:2,1`, `bar:2024-03-01T10:05`.
- **Suggestion chips** change views or non-answer parameters only ("Show each leg", "Try $\sigma = 40\%$", "Step one bar", "Slow the replay"). Bertie never edits answer state, orders or quotes.
- **Computed numbers.** On complex-tier calls the engine may give Bertie a `fin_eval` tool: `{ fn: 'bs' | 'greeks' | 'bond-price' | 'ytm' | 'forward' | 'npv' | 'irr' | 'kelly' | 'posterior', args }`, returning under 1 KB, so any number Bertie quotes is computed, as with the probability cluster's `dist_eval`.
- **Timed play.** Bertie is off during a timed game or drill (Stage 0's rule). Afterwards the debrief reads the game log summary (at most 4 KB) and `secret()`.

**2.9.1 Interviewer mode.** Used by `mock-interview` and by `mm-game` in interview mode.

- **Persona.** Bertie with the interviewer expression set (neutral and attentive, no celebration), terse, British. Asks, listens, probes, and gives a hint only when the candidate asks or has been silent and stuck for 60 seconds. Every hint is logged with its level.
- **Prompt.** A frozen prefix (interviewer rules; the round plan; each item with its private solution, common wrong paths and hint ladder; the rubric; the output format) and a volatile suffix (the transcript, trimmed to the last 12 turns plus a running summary; elapsed time; flags).
- **Output per turn:** `{ "say": string, "action": "ask" | "probe" | "hint" | "accept" | "next" | "end", "hintLevel"?: 1 | 2 | 3, "notes": string[] }`. `notes` are private evidence for the rubric, shown only in the debrief.
- **Transport, Artifact.** `sample.json` with the turns list (the instructions as a leading user turn), `cache: false`, `modelTier: 'quick'` for turns, because the quick tier does not think first and answers in a second or two [sourced: `sample.d.ts`]. The debrief uses `modelTier: 'complex'`, streamed.
- **Transport, web.** The proxy calls `claude-opus-5-5` with streaming, effort `low` for turns and `high` for the debrief [turn latency unverified; measured in the wave J spike]. Prompt caching covers the frozen prefix (tools, system, then the round's items), with the transcript last. Structured turns use a strict tool `interviewer_turn` with `tool_choice: auto` and prompt steering, because forced tool choice returns 400; the server-side refusal fallback header is set.
- **Leak guard.** Before `accept`, the engine scans `say` for the solution's value in its common forms (exact rational, decimal to 3 significant figures, percentage) and replaces a leaking turn with a neutral probe. It is a heuristic and is tested against a red-team set (section 2.12).
- **Voice.** `say` is spoken by `speechSynthesis` once parsed; captions show it at the same time.

### 2.10 Performance

The reference phone is the engine blueprint's (the sibling files name a Pixel 4a or Galaxy A53 class device). Shared budgets apply: 8ms of widget work per pointer frame for a composite, of which script at most 4ms; mount within 100ms excluding lazy dependencies; 1,500 SVG nodes per screen before a layer moves to Canvas 2D.

| Work | Budget or cap |
|---|---|
| `exchange-sim` event (add, cancel, match) | at most 50 microseconds [our choice target; measured in G1] |
| Ladder redraw after an event | at most 2ms; events coalesced to one redraw per frame |
| Payoff curves | exact at kinks; up to 20 legs; redraw under 1ms |
| Black-Scholes curves | 200 points by 5 expiries in closed form, under 1ms |
| Binomial trees | up to $N = 8$ drawn (45 nodes); up to $N = 2{,}000$ priced in a worker for convergence plots (about $2 \times 10^6$ operations) |
| Monte Carlo | in the worker: $10^5$ terminal draws under 50ms; $10^4$ paths of 252 steps under 150ms [estimates, unverified on the reference phone] |
| Cross-sections | 500 stocks by 240 months; rank IC per date in a worker, debounced 50ms on slider drags |
| Candles | up to 2,000 in SVG; Canvas 2D above |
| Latency histograms | $10^5$ samples binned on a log scale into `Uint32Array` |
| Speech | interim transcript updates at most 4 times a second |
| Saved state | at most 32 KB per widget instance; game logs at most 32 KB; mock-interview transcripts as separate documents of at most 64 KB |

### 2.11 Artifact and web

| Concern | Artifact | Web |
|---|---|---|
| All 1.7 widgets, the concept parts of 2.3, the 3.3 games | identical | identical |
| Pure-Python drills (the binomial pricer, Kelly simulations) | MicroPython if the WebAssembly probe passes [unverified]; otherwise handoff | Pyodide |
| Drills needing NumPy, pandas or SciPy (implied volatility with `scipy.optimize`, signal research, backtests) | ulab for drills CI tags compatible; others hand off | Pyodide |
| Starter test suites for projects | `downloads` capability; each suite is a single `.py` file, so no archive is needed | Blob link |
| Speech capture | `SpeechRecognition` inside the Artifact frame depends on the frame's microphone permission [unverified]; typed path always | Chrome, Edge and Safari have `SpeechRecognition`; Firefox does not [recalled] |
| Speech output | `speechSynthesis` [unverified inside the frame] | `speechSynthesis` |
| Partner sessions on two devices | `room` where the platform admits the partner [unverified for invited guests] | not offered; pass-and-play only |
| Tutor and interviewer | `sample` | proxy |
| Exporting a results note or a game log | `downloads` (Markdown, CSV) | Blob link |

### 2.12 Services this cluster needs (not widgets)

These are requirements on shared modules, written as acceptance tests. The engine blueprint owns their design.

| Module | Must provide | Accuracy acceptance | Used by |
|---|---|---|---|
| `finance-core` | Rate conversions; PV, NPV, IRR (Brent inside a bracket found by a sign-change scan, reporting every root when cash flows change sign more than once); annuities, perpetuities, amortisation; bond price, accrued interest (ACT/365F, ACT/360, 30/360 US, ACT/ACT ICMA), yield to maturity, Macaulay and modified duration, convexity, DV01; zero curves by bootstrapping, discount factors, forward rates, par swap rates; forward prices with income, yield, storage and foreign rates; Black-Scholes-Merton prices and Greeks ($\Delta, \Gamma, \Theta, \nu, \rho$) with dividend yield; digitals; implied volatility (Brent on $[10^{-6}, 5]$ with Newton steps while vega exceeds $10^{-8}$, returning a reason when the price violates the no-arbitrage bounds); binomial trees (CRR), European and American; option bounds; SVI evaluation and fitting; implied densities by finite differences | Prices and Greeks to $10^{-10}$ relative against SciPy fixtures on a grid from 1 day to 5 years and moneyness from 0.2 to 5; implied volatility round trip to $10^{-8}$ where vega exceeds $10^{-8}$; bond analytics and day counts to $10^{-10}$ against QuantLib fixtures; IRR to $10^{-10}$ | most of section 6 and 7 |
| `exchange-sim` | Continuous double auction with price-time priority; limit, market, stop, stop-limit; IOC, FOK, day, GTC; post-only (rejected if it would cross); iceberg (display quantity replenished to the back of the queue); cancel; amend (a price change or a quantity increase loses priority, a decrease keeps it) [recalled as common practice; venue rules vary, so it is configuration]; call auctions (maximum executable volume, then minimum imbalance, then nearest to a reference price) [recalled; venues differ]; maker and taker fees; tick and lot sizes; self-trade prevention (cancel the newest); a sequence-numbered event log, snapshots and incremental feeds | Differential testing against a Python reference engine on $10^5$ random order streams per release (identical fills, books and logs); invariants after every event (no crossed book; quantity conserved; first-in-first-out within a level) | `order-book`, `auction-lab`, `tape-lab`, `dealer-sim`, `feed-sim`, `order-lifecycle`, `paper-trader`, `mm-game` |
| `market-gen` | Order flow: Poisson arrivals of limit, market and cancel orders by distance from the mid (the zero-intelligence model of Cont, Stoikov and Talreja [recalled]); informed and noise traders; news jumps; trade and quote tapes; option chains from an SVI surface with bid-ask noise, stale and crossed quotes; cross-sections of returns from a factor model (market and sectors) with a planted signal of chosen IC and decay, and delistings; latency samples (log-normal body, Pareto tail, periodic pauses); daily prices through the programming cluster's `price-series` | Statistics of $10^6$-sample runs within 4 standard errors of the planted parameters in CI | sections 6 to 8 |
| `ledger` | Positions per instrument; average-cost and first-in-first-out lots; realised and unrealised P&L; cash; fees; mark-to-market; margin requirements; integer minor units | Cash plus marked positions minus starting cash equals realised plus unrealised P&L minus fees, exactly, on random trade streams | every widget with a blotter |
| `backtest-core` | Bar-driven event loop; a point-in-time data handle that throws on future access unless a lesson disables the guard on purpose; signals to target weights to orders to fills (next open, close with slippage, a VWAP proxy); cost models (basis points, half-spread, square-root impact); metrics (annual return, volatility, Sharpe with its standard error, Sortino, Calmar, maximum drawdown and its length, turnover, exposure); the deflated Sharpe ratio; walk-forward splits | Metrics equal pandas and NumPy fixtures to $10^{-10}$; a planted look-ahead strategy trips the guard | `backtest-lab`, `sharpe-lab`, `paper-trader`, `signal-lab` |
| `signal-core` | Ranks with average ties, z-scores, winsorising, sector demeaning, rank and Pearson IC, IC $t$-statistics, decay curves, quantile portfolios, one-way turnover | Against pandas and SciPy fixtures to $10^{-10}$ | `signal-lab` |
| `speech` | `SpeechRecognition` wrapper (continuous, interim results, en-GB, restart on `end`, errors mapped to plain messages) and `speechSynthesis` wrapper (voice choice, rate, sentence queue, cancel when the learner starts speaking); `available()`; the first-use disclosure: browsers may send audio to their maker's speech service [recalled for Chrome]; the app keeps text only | Manual test matrix per browser in wave J | `voice-capture`, `mock-interview`, `mm-game` |
| `interview-engine` | Round plans; seeded item selection; prompt assembly (section 2.9.1); the turn loop; timers; silence prompts after 20 seconds without speech or typing; hint accounting; the leak guard; transcripts; the debrief request; rubric storage | Scripted conversations replayed against a stub model; the leak guard catches at least 95% of a 200-turn red-team set [our choice target] | `mock-interview`, `mm-game` |
| `problem-bank` | Problems with source citation, pattern tags, difficulty, answer type, exact answer, worked solution, wrong-answer diagnoses and a linked-widget configuration; parametrised families with solvers; held-out sets for cold mode | Every family's solver agrees with a $10^6$-trial simulation within 4 standard errors; every authored problem has a second reviewer | `puzzle-workbench`, `mock-interview` |
| `rubric-marker` | Rubric items with required evidence quotes; tutor-draft marks; learner or partner confirmation; per-item history | Unit tests on mark arithmetic and evidence matching | `free-response`, `results-note`, `mock-interview`, `puzzle-workbench` |

### 2.13 Data held and data policy

- **Learner data.** Progress, answers, game logs, mock-interview transcripts (text) and results notes, all in the learner's own `db` space in the Artifact or IndexedDB on the web. None leaves except to Bertie, on the learner's own action, through `sample` or the proxy.
- **Audio** is never stored or sent by the app.
- **Market data** in the app is synthetic. No third-party data are stored or redistributed.
- **Pasted outputs** are redacted for home-directory paths before they reach Bertie, as in Stage 0.

---

## 3. New primitives

Each is cluster-neutral and proposed for the engine's primitive set.

### 3.1 `price-ladder`: Price ladder

**Primitive (host) · P1 · G1.** A vertical ladder of price levels: bid sizes on the left, prices in the centre, ask sizes on the right, with the learner's own orders, the last trade and volume at each price.

- **Purpose.** The canvas for every order-book idea, and for any widget that shows or takes orders at prices. A ladder makes queues, the spread and walking the book visible in one glance.
- **Serves.** 1.7.4, 1.7.9; 2.3.4 L3; 2.3.5; 3.3.4 (ladder view).
- **Hosts.** `order-book`, `auction-lab`, `dealer-sim`, `feed-sim`, `order-lifecycle`, `mm-game`.
- **Interactions.**
  - Pointer: tap a row to select its price; tap a bid or ask cell to stage a buy or sell there (it prefills `order-ticket`, or places at once in quick mode); drag one of your resting orders up or down to amend its price (a ghost shows the new place; release commits; the loss of priority is labelled); drag the price column to scroll; double-tap to centre on the mid.
  - Keyboard: a grid with a roving tab stop. Up and Down move one tick; PageUp and PageDown ten; Home and End jump to the best ask and best bid; B and S stage a buy or sell at the focused price; Enter sends; Delete cancels your order at the focused level (asking which when there are several); C centres; Escape cancels staging.
- **State.** `{ window: { topTick: number; rows: number }; selected?: number; staged?: { side: 'buy' | 'sell'; tick: number; qty: number } }`. The book itself is input (an `exchange-sim` snapshot), not state.
- **Answers.** `set` (selected levels) and `order` (the staged order); hosts add others.
- **Config.**

```ts
interface PriceLadderConfig extends BaseConfig {
  tick: number; lot: number;
  columns: Array<'my-bid' | 'bid' | 'price' | 'ask' | 'my-ask' | 'volume' | 'cum-bid' | 'cum-ask' | 'supply' | 'demand'>;
  rows: { min: number; max: number };          // visible levels, 9 to 41
  entry: 'none' | 'ticket' | 'quick';          // how a tap on a size cell turns into an order
  amendByDrag: boolean;
  showQueuePosition: boolean;
  showLast: boolean;
}
```

- **Visual.** Prices in the centre column in ink, tabular figures; the best bid and best ask prices bold; rows between them shaded `--bg-sunken` with a label ("spread 3 ticks"); bid sizes as `--s6` bars growing leftwards with their numbers, ask sizes as `--s2` bars growing rightwards; your orders as `--manip` outlined chips ("You 100, 3rd"); the last trade as a small ink triangle (up or down) beside its price; volume at price as thin ink bars. Rows are 44px on coarse pointers and 32px on fine pointers, so every hit area meets the 44px rule where touch is used.
- **Motion.** Size bars change over 120ms (`ease-standard`) when the market moves them; new levels fade in over 120ms; emptied levels collapse over 160ms; an amended order springs into place (`spring-snap`). Your own drag is direct.
- **Reduced motion.** Widths and rows change at once.
- **Accessibility.** `role="grid"`; each row reads "Price 100.02. Ask 200 shares. Your order: none." The table view lists every level. Fills are announced on commit ("Bought 200 at 100.01, 200 at 100.02, 100 at 100.04"); during a replay, one summary every 2 seconds.
- **Tutor.** Describe: "Best bid 99.98 (300), best ask 100.01 (200), spread 3 ticks. Your orders: buy 100 at 99.97, 2nd in queue." Ids: `level:<ticks>`, `bid:<ticks>`, `ask:<ticks>`, `order:<id>`, `spread`, `mid`, `last`.
- **Performance.** At most 41 rows rendered (virtualised); keyed updates; under 2ms per event; one redraw per frame.
- **Artifact and web.** No difference.
- **Generators.** None of its own; books come from `market-gen` or content.

### 3.2 `cashflow-timeline`: Cash-flow timeline

**Primitive (host) · P1 · G1.** A time axis with cash flows drawn as arrows (up when received, down when paid), lanes for separate legs, present-value ghosts, grouping brackets and an optional fulcrum.

- **Purpose.** Every time-value idea: discounting, NPV, annuities and loans, bond cash flows, duration as a balance point, the replicating trades behind forwards, swap legs, the bond in put-call parity.
- **Serves.** 1.7.1, 1.7.3, 1.7.5, 1.7.6 L13 to L15; cross-cluster: 0.3 annuities and 1.3 series (optional).
- **Hosts.** `tvm-timeline`, `bond-lab`, `yield-curve-lab`, `duration-lab`, `carry-arb`, `parity-lab`.
- **Interactions.**
  - Pointer: drag an arrow's head vertically to set its amount (snapping to the step); drag its foot along the period grid to change its date; tap the axis to add a flow where editing is allowed; long-press or Delete to remove; drag a bracket's ends to group flows; drag the fulcrum; tap "Discount" (or one flow) to send present-value ghosts to $t = 0$.
  - Keyboard: Left and Right select flows in time order; Up and Down change the amount by one step (Shift ten steps, Alt a tenth); [ and ] move the date by one period; N adds a flow at the focused date; Delete removes; E opens the exact editor, which accepts expressions such as `1000*1.05^-3`; F focuses the fulcrum, whose Left and Right move it.
- **State.** `{ flows: { id: string; t: number; amount: number; lane: string }[]; selected?: string; fulcrum?: number; brackets?: { id: string; from: number; to: number }[]; discounted: boolean }`.
- **Answers.** `cashflows`, `point` (the fulcrum), `set` (selected flows).
- **Config.**

```ts
interface CashflowTimelineConfig extends BaseConfig {
  horizon: number; period: number;            // years; e.g. 10 and 0.5
  lanes: { id: string; label: string; editable: boolean }[];
  flows: { id: string; t: number; amount: Entry; lane: string; locked?: boolean }[];
  amountStep: number; amountRange: [number, number];
  scale: 'linear' | 'sqrt';                   // sqrt when amounts span more than 20x
  discount?: { rate: Entry; convention: 'annual' | 'semi-annual' | 'monthly' | 'continuous' } | { curve: [number, number][] };
  show: { pv: boolean; net: boolean; growthArcs: boolean; fulcrum: boolean };
}
```

- **Visual.** The axis in ink at 1.5px with period ticks and a "years" label; arrows 2px with 6px heads, ink when given and `--manip` when editable, each labelled with its amount; present-value ghosts in `--s3` at 60%, stacked at $t = 0$ with their total; lanes separated by 1px `--line` rules with labels on the left ("Borrow", "Stock", "Forward"); an optional net row in bold ink; brackets dashed `--s4` with a label ("annuity, 5 payments"); the fulcrum a `--manip` triangle under the axis; growth arcs between dates labelled "×1.05³". Beyond 60 flows, arrows thin to 1px and labels show on focus.
- **Motion.** Discounting slides ghosts to $t = 0$ while shrinking them, 480ms `ease-morph`, 80ms stagger. Drags are direct.
- **Reduced motion.** Ghosts appear at $t = 0$.
- **Accessibility.** Each flow is a control reading "Year 3, receive 50 pounds, present value 43.19." The table view lists $t$, amount, discount factor and present value. Lanes are groups with names.
- **Tutor.** Describe: "3 lanes. Net today 0.00. Borrow lane: receive 100 at t=0, pay 105.13 at t=1." Ids: `flow:<id>`, `lane:<id>`, `pv:<id>`, `net:<t>`, `fulcrum`, `bracket:<id>`.
- **Performance.** SVG up to 400 flows (a 30-year monthly mortgage is 360); Canvas 2D above.
- **Artifact and web.** No difference.
- **Generators.** None of its own.

### 3.3 `position-editor`: Position editor

**Primitive (control) · P1 · G2.** A list of legs (instrument, side and quantity, strike, expiry, price) with an instrument palette, linked to handles in a host plot.

- **Purpose.** Build positions: option strategies, replicating portfolios, arbitrage trades, hedges.
- **Serves.** 1.7.5, 1.7.6, 1.7.7 L1, 1.7.8 L12 and L13; 2.3.3.
- **Hosts.** `payoff-builder`, `parity-lab`, `option-bounds`, `carry-arb`, `hedge-lab`, `greeks-lab`, `pnl-attribution`.
- **Interactions.**
  - Pointer: tap a palette chip (Stock, Bond, Call, Put, Forward, Digital) to add a leg; steppers for quantity; a Long and Short segmented control; a strike field that is linked both ways to the host's kink handle; remove; drag to reorder.
  - Keyboard: a grid with a roving tab stop; + and − change quantity; L and S set the side; K focuses the strike; Delete removes; A opens the palette, whose arrows choose an instrument and Enter adds it.
- **State.** `{ legs: Leg[] }`.
- **Answers.** `position`.
- **Config.**

```ts
interface PositionEditorConfig extends BaseConfig {
  instruments: Leg['instrument'][];
  maxLegs: number;
  qty: { min: number; max: number; integer: boolean };
  strikeGrid: { min: number; max: number; step: number };
  pricing: 'none' | 'given' | { model: 'bs'; S: number; sigma: Entry; r: Entry; q?: Entry; T: number };
  locked?: string[];                           // leg ids the learner cannot edit
  showCost: boolean;
}
```

- **Visual.** Each leg is a lipped card with a letter badge (C, P, S, B, F, D), the side in words ("Long 2"), editable fields with `--manip` focus, and a colour swatch matching its line in the host plot; a premium column reads "pays 4.20" or "receives 4.20"; the net cost row is bold.
- **Motion.** A new leg slides in over 200ms; a removed leg collapses over 160ms.
- **Reduced motion.** Instant.
- **Accessibility.** A list; each row reads "Long 2 calls, strike 100, expiry 0.5 years, premium 4.20 each." The net cost is announced on commit.
- **Tutor.** Ids: `leg:<id>`, `leg:<id>:qty`, `leg:<id>:K`, `palette:<instrument>`, `net-cost`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** None of its own.

### 3.4 `order-ticket`: Order ticket

**Primitive (input) · P1 · G1.** Side, order type, price, quantity, time in force and display quantity, with validation in plain words and an optional dry-run preview.

- **Purpose.** Every order the learner sends.
- **Serves.** 1.7.4, 1.7.9; 2.3.5.
- **Hosts.** `order-book`, `auction-lab`, `order-lifecycle`, `paper-trader` (manual trades), `dealer-sim` (manual mode).
- **Interactions.**
  - Pointer: Buy and Sell as a segmented control with text labels; order-type chips (Limit, Market, Stop, Stop-limit) and toggles (IOC, FOK, Post-only, Iceberg) where the config enables them; a price stepper in ticks (linked to the ladder's selection); a quantity stepper in lots with quick sizes; Send.
  - Keyboard: B and S choose the side; T cycles the type; P focuses price (Up and Down step a tick); Q focuses quantity; Enter sends; Escape clears.
- **State.** `OrderSpec` plus `{ dirty: boolean }`.
- **Answers.** `order`.
- **Validation.** Plain messages, costing no attempt: "Price must be a multiple of the 0.01 tick." "Quantity must be a multiple of the 100-share lot." "A post-only buy at 100.01 would cross the ask, so it is rejected."
- **Preview.** Optional: "Would fill 200 at 100.01 and rest 300 at 100.01", from an `exchange-sim` dry run. Content turns it off on predict screens.
- **Config.**

```ts
interface OrderTicketConfig extends BaseConfig {
  tick: number; lot: number;
  types: OrderSpec['type'][];
  tifs: OrderSpec['tif'][];
  allowPostOnly: boolean; allowIceberg: boolean;
  quickSizes?: number[];
  preview: boolean;
  fixed?: Partial<OrderSpec>;                  // fields the screen fixes
}
```

- **Visual.** The side shows as text and a 4px left edge in the side colour (`--s6` buy, `--s2` sell); Send uses the engine's neutral action style, never green or red; fields take the `--manip` focus ring.
- **Motion.** None beyond button presses.
- **Reduced motion.** Not applicable.
- **Accessibility.** Form semantics; errors linked by `aria-describedby`; the preview in the polite live region.
- **Tutor.** Ids: `ticket:side`, `ticket:type`, `ticket:px`, `ticket:qty`, `ticket:tif`, `ticket:preview`.
- **Performance.** Trivial; a dry run costs one simulated match.
- **Artifact and web.** No difference.
- **Generators.** None.

### 3.5 `quote-entry`: Two-sided quote

**Primitive (input) · P1 · G3.** A bid and an ask with sizes, a width and centre readout, nudges, and shorthand parsing ("30 at 35", "30-35", "30 bid, 35 offered, 10 up").

- **Purpose.** Making markets: `dealer-sim` in manual mode, `mm-game`, and the quote mode of `order-book`.
- **Serves.** 1.7.9 L6 and L11; 3.3.4.
- **Interactions.**
  - Pointer: two fields; a shorthand box; nudges for Up and Down (shift both by one tick), Wider and Tighter (symmetric), and Skew (move the centre, keep the width); on a host axis, drag the bid handle, the ask handle or the centre handle (which moves both).
  - Keyboard: inside the widget, Up and Down shift the quote, W and T widen and tighten, Tab moves between fields, Enter sends; inside a field, Up and Down step one tick.
  - Voice: through `voice-capture` with the quote grammar (section 3.6).
- **State.** `{ bid?: number; ask?: number; bidSize?: number; askSize?: number; text?: string }`.
- **Answers.** `quote`.
- **Validation.** Bid below ask; tick multiples; width within the limits, shown before sending ("Width 6 is wider than the 4 the interviewer allows").
- **Config.**

```ts
interface QuoteEntryConfig extends BaseConfig {
  tick: number;
  width?: { min?: number; max?: number };
  sizes?: { show: boolean; lot: number; max: number };
  shorthand: boolean; voice: boolean;
  host?: { kind: 'number-line' | 'price-ladder'; id: string };
}
```

- **Visual.** "Bid" field on the left with an `--s6` label, "Ask" on the right with an `--s2` label; width and centre in caption figures between them; on a host, the quote is a `--manip` bracket with a centre tick.
- **Motion.** The bracket is direct; nudges move it at once.
- **Reduced motion.** Not applicable.
- **Accessibility.** "Your market: bid 30, ask 35, width 5, centre 32.5", announced on send.
- **Tutor.** Ids: `quote:bid`, `quote:ask`, `quote:width`, `quote:centre`, `quote:text`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** None.

### 3.6 `voice-capture`: Voice capture

**Primitive (control) · P1 · G1.** Speech captured as an editable, timestamped transcript, with a typed path that always counts the same, and an optional command grammar for quotes and trades.

- **Purpose.** Explanations aloud (the 1.7 exit rehearsal), thinking aloud in puzzles, spoken market-making, mock interviews. Interviewers mark reasoning as it is spoken; practising that needs the words captured.
- **Serves.** 1.7.4 L13; 3.3.2 L13; 3.3.4 L10 and L11; 3.3.5.
- **Hosts.** `free-response` (voice mode), `puzzle-workbench` (aloud), `mm-game` (interview, partner), `mock-interview`.
- **Interactions.**
  - Pointer: a mic button toggles listening (off, listening, paused, unavailable); a level meter; interim text in `--text-muted`, final text in ink; tap any segment to edit; "Type instead" switches to a textarea with the same output.
  - Keyboard: M toggles the mic when focus is in the widget but not in a text field; Escape stops; the transcript is a plain textarea.
- **Command grammar** (`grammar: 'quotes'`): numbers spoken in words or digits ("thirty-two and a half", "thirty two point five"), "at", "bid", "offer" or "offered", "for", "size", "up", "mine" (I buy), "yours" (I sell), "done", "out" (pull my quotes). An ambiguous parse is shown for one-tap confirmation; nothing trades on a parse the learner has not seen.
- **State.** `{ status: 'off' | 'listening' | 'paused' | 'unavailable'; segments: { t0: number; t1: number; text: string; final: boolean }[]; typed: boolean }`.
- **Answers.** `transcript`, `text`; parsed commands go to the host as events.
- **Config.**

```ts
interface VoiceCaptureConfig extends BaseConfig {
  lang: 'en-GB' | 'en-US';
  mode: 'dictation' | 'think-aloud' | 'commands';
  grammar?: 'quotes' | 'none';
  maxMinutes?: number;
  showInterim: boolean;
}
```

- **Visual.** The mic button is a secondary pill with a mic icon and the word "Listening" while on; the level meter is five ink bars; transcript in body text with caption timestamps.
- **Motion.** The meter follows the input level (data, not decoration).
- **Reduced motion.** The meter becomes a static "sound detected" dot.
- **Accessibility.** The typed path is equivalent and says so; the host captions the other speaker; lessons set no time limit on speaking.
- **Privacy.** First use shows the `speech` service's disclosure; audio is never stored; transcripts stay in the learner's own space.
- **Tutor.** Describe: "Transcript 412 words over 6 min 10 s; last segment: 'so the expected sum is seven'." Ids: `segment:<n>`, `mic`.
- **Performance.** Recognition runs in the browser; interim updates at most 4 times a second; transcripts at most 64 KB a session.
- **Artifact and web.** As section 2.11: availability inside the Artifact frame is [unverified]; when `SpeechRecognition` is missing, the widget opens in typed mode and says why.
- **Generators.** None.

### 3.7 `scratch-pad`: Scratch pad

**Primitive (control) · P0 · D4.** Free working space: typed notes with inline maths, and optional ink, saved per problem, which the learner can show Bertie.

- **Purpose.** Where the learner works a puzzle or a long-form problem. It never grades.
- **Serves.** The weekly problems from 1.5; 3.3.2; 3.3.5; long-form homework items in any topic.
- **Hosts.** `puzzle-workbench`, `mock-interview`, `mm-game` (notes).
- **Interactions.**
  - Pointer: text blocks with `$...$` maths rendered on blur; an ink layer with pen and eraser, using pressure where the device reports it; undo and redo; pages.
  - Keyboard: the text is fully keyboard-operable; Ctrl+Z and Ctrl+Y undo and redo. Ink has no keyboard equivalent and is never required.
- **State.** `{ blocks: { id: string; text: string }[]; ink?: { strokes: string[] }; page: number }` (strokes delta-encoded).
- **Answers.** None. "Show Bertie" sends the text, and a PNG of the ink page where `sample.limits()` reports images.
- **Config.** `{ ink: boolean; pages: number; template?: 'blank' | 'clarify-plan-solve-check' }`. The template seeds four headed blocks that mirror the interview method of 3.3.2.
- **Visual.** A `--bg-sunken` page; ink 2px in ink colour; text in body type; maths in KaTeX.
- **Motion.** None.
- **Reduced motion.** Not applicable.
- **Accessibility.** Text blocks are real textareas; the ink layer is described as "Ink page 1, 34 strokes" and is readable by Bertie only through the image.
- **Tutor.** Ids: `block:<id>`, `ink:page:<n>`.
- **Performance.** Strokes simplified (Ramer-Douglas-Peucker at 0.75px) and delta-encoded; at most 64 KB a page; drawn on Canvas 2D.
- **Artifact and web.** No difference, except that images reach Bertie only where the view allows them.
- **Generators.** None.

---

## 4. Additions to shared primitives

### 4.1 `marks`: new mark types

| Mark | What it draws | Style | First use |
|---|---|---|---|
| `candles` | Open, high, low and close bodies with wicks; optional volume bars in a linked lower panel | up: hollow body, 1.5px ink outline; down: filled ink; wicks 1px ink; volume `--line` fill | 2.3.4, 2.3.5; requested by the programming cluster's `time-series-lab` |
| `ohlc-bars` | The tick-mark variant of candles | ink | 2.3.4 |
| `depth` | Cumulative bid and ask step areas meeting at the spread | bids `--s6` at 25%, asks `--s2` at 25%, 1.5px edges, labels | 1.7.4 L8 |
| `payoff` | A piecewise-linear curve with kink dots, slope labels between kinks, and an arrow on an unbounded tail | by role (section 2.6) | 1.7.5, 1.7.6 |
| `signed-fill` | The area between a curve and zero, split into profit and loss | `--div-pos` and `--div-neg` at 18% with "+" and "−" glyphs | payoffs, P&L |
| `waterfall` | Additive bars from a start value to an end value | signed fills; totals ink | `pnl-attribution`, `execution-lab`, `backtest-lab` |
| `quote-band` | A band from bid to ask over time with the mid line | band `--bg-sunken`, edges `--s6` and `--s2`, mid ink dashed | `tape-lab`, `adverse-selection`, `dealer-sim`, `mm-game` |
| `trade-glyphs` | Trades as dots sized by quantity, triangles for initiator side | ink | `tape-lab`, `paper-trader` |
| `event-rug` | Ticks on the time axis for discrete events, each with a small icon and label | ink | dividends and splits in `share-lab`; reconnects in `feed-sim`; fills in `backtest-lab` |

### 4.2 Other primitives

| Primitive | Addition | Priority | First use |
|---|---|---|---|
| `plot-2d` | A trading-time axis that compresses weekends and holidays (shared with the programming cluster); linked crosshairs across stacked panels (`link: { group, axis: 'x' }`); a log price axis | P1 | `share-lab`, `backtest-lab`, `paper-trader` |
| `slider` | Logarithmic scales (volatility, $N$, costs in basis points); value lists (rebalancing frequencies); unit suffixes (%, bp, years) | P1 | `bs-explorer`, `pricer-compare` |
| `number-line` | Log mode with interval brackets; a quote bracket with bid, ask and centre handles | P1 (quote), P2 (log intervals) | `mm-game`, `calibration-lab` |
| `value-table` | Presets: `blotter` (time, side, quantity, price, position, cash, P&L, with running totals from `ledger`), `chain` (calls, strike, puts, with a sticky strike column and selectable cells), `book` (the price ladder's table view) | P1 | `order-book`, `option-chain`, `dealer-sim` |
| `sim-runner` | Models: `order-flow` (from `market-gen`), `bet-sequence` (multiplicative wealth), `null-strategy` (random entries with a fixed trade count), `latency` | P1 (flow), P2 (others) | `order-book` race, `kelly-lab`, `paper-trader`, `latency-lab` |
| `region-select` | Chain cell selection; time brushes for held-out periods (already added by the probability cluster) | P1 | `option-chain`, `backtest-lab` |
| `stepper` | A replay speed control (0.5× to 8×) | P1 | `order-book` replays, `feed-sim` |
| `speed-timer` | A count-up mode with a soft target ("about 10 minutes in an interview") that never ends the attempt | P0 | `puzzle-workbench` |

---

## 5. Extensions to widgets owned by sibling catalogues

23 composites and inputs from the sibling catalogues gain a mode or preset here. Linked mode (section 2.1) applies to 10 more without per-widget changes.

| # | Widget | Owner | Change | Priority | Serves |
|---|---|---|---|---|---|
| 1 | `binomial-tree` | calc-linalg, **moving here** | Modes `crr`, `delta`, `dividend`, `vector`, `state-prices`; specified in full in section 5.1 | P1, G3 | 1.7.7, 1.7.8 L2, 1.9 exit |
| 2 | `gbm-lab` | calc-linalg | A 1.7 mode, promoted from P2: lognormal terminal distribution, median against mean, $\mu - \frac{1}{2}\sigma^2$ as the median growth rate; no Itô notation | P1, G3 | 1.7.2 L6, 1.7.8 L1 |
| 3 | `hedging-sim` | calc-linalg | The `one-path` mode promoted to P1 with a daily-rebalance default and a gamma-theta split per day; distribution mode stays P2 | P1, G3 | 1.7.8 L14; 2.3.3 |
| 4 | `drawdown-lab` | programming | Compare mode adds Sharpe, Sortino and Calmar readouts and a rolling Sharpe panel | P2, H | 2.3.1 L7 |
| 5 | `time-series-lab` | programming | Resample mode accepts irregular tick data from `market-gen`, so `candle-builder` can hand over to the pandas idiom | P2, H | 2.3.4 L4 to L6 |
| 6 | `json-explorer` | programming | Feed-message presets (trade, quote, book delta, heartbeat, error) | P2, H | 2.3.4 L1 |
| 7 | `schema-builder` | programming | Trades and candles items: time-partitioned tables, a composite primary key (symbol, interval, start), idempotent upserts | P2, H | 2.3.4 L11 |
| 8 | `setup-checklist` | programming | Project mode for 2.3: milestones per project, starter-suite download, parsing of pasted `pytest -q` output and of a metrics JSON whose schema we publish | P2, H | 2.3 all |
| 9 | `code-cell` | programming | A finance prelude `zq_fin` (reference pricers for test comparisons, `price_close(a, b)` with absolute $10^{-6}$ and relative $10^{-8}$ tolerance); `zq_market` for synthetic data | P1, G3 | 1.7.7 L10 and L11; 2.3 drills |
| 10 | `free-response` | Stage 0 | Voice input through `voice-capture`; `tutor-draft` and `partner` rubric marking; evidence quotes highlighted in the answer | P1, G1 | 1.7.4 L13 (exit); 3.3 |
| 11 | `multiplier-chain` | Stage 0 | A returns preset: successive returns as multipliers, with arithmetic and geometric means side by side | P1, G1 | 1.7.2 L6 |
| 12 | `series-explorer` | calc-linalg | Annuity and perpetuity presets linked to a `cashflow-timeline` | P1, G1 | 1.7.1 L8 |
| 13 | `lagrange-explorer` | calc-linalg | A minimum-variance portfolio preset (the budget constraint as the line) | P1, G1 | 1.7.2 L12 (optional) |
| 14 | `convexity-chord` | calc-linalg | Presets for volatility drag ($E[\ln(1+R)] < \ln(1 + E[R])$) and for the concave Kelly growth curve | P1 (drag), P2 (Kelly) | 1.7.2 L6; 3.3.3 L6 |
| 15 | `sketch-pad` | calc-linalg | A piecewise-linear snapping mode for sketching payoffs (kinks snap to the strike grid) | P1, G2 | 1.7.6 predict-first screens; 1.7.8 L6 |
| 16 | `dist-explorer` | prob-stats | A lognormal preset parametrised by $S_0$, drift, $\sigma$ and $T$, with $P(S_T > K)$ shaded and $N(d_2)$ shown | P1, G3 | 1.7.8 L1 and L4 |
| 17 | `regression-lab` | prob-stats | A beta preset: stock against market returns, the variance split into systematic and idiosyncratic parts | P1, G1 | 1.7.2 L14 |
| 18 | `game-lab` | prob-stats | The `kelly-coin` mode embeds `kelly-lab` (decision 17); interview betting presets ("pay to roll", "double or nothing") link to `bet-lab` | P2, J | 3.3.3 |
| 19 | `multiple-testing` | prob-stats | The strategy zoo draws its noise strategies from `backtest-core` and links to `sharpe-lab`'s deflated Sharpe | P2, H | 2.3.1 L10 |
| 20 | `speed-drill` | Stage 0 | Decks `ev` (expected value of a simple bet), `odds` (conversions), `options` (at-the-money values by $0.4\,\sigma\sqrt{T}\,S$), `sequences` (next term; relevance to firm tests [unverified]); 80-in-8 options: negative marking and a skip rule as configuration [firm practice unverified] | P2, J (the `options` deck P1) | 3.3.1; 1.7.8 L7 |
| 21 | `strategy-trainer` | Stage 0 | Strategies for decimals by decimals, percentage of a percentage, eighths and sixteenths as decimals, and quick division by 7, 9, 11 and 13 | P2, J | 3.3.1 |
| 22 | `fermi-estimator` | Stage 0 | Exports an estimate with a log-normal uncertainty to `mm-game` and `calibration-lab` | P2, J | 3.3.4 L7 |
| 23 | `node-link` | programming | Fixed-layout state machines with labelled transitions and the active transition highlighted | P2, H | `order-lifecycle`, `feed-sim` |

### 5.1 `binomial-tree`: Binomial pricing tree (ownership moves here)

**Composite · P1 · G3.** The calculus and linear algebra catalogue specified this widget (its section 7.8) for 1.7 and Shreve I. 1.7 is its first and heaviest user, and the 1.9 C++ exit checks against it, so this catalogue takes ownership. Everything in the original spec stands; the additions follow.

- **Purpose.** Build an $N$-step tree; replicate with $\Delta$ shares and a bond; derive the risk-neutral probability $q = \frac{e^{r\Delta t} - d}{u - d}$; price by backward induction; American early exercise; arbitrage when $d < e^{r\Delta t} < u$ fails; calibration by Cox-Ross-Rubinstein; convergence to Black-Scholes; the one-array implementation behind the 1.7 and 1.9 exits.
- **Serves.** 1.7.7 L1 to L11; 1.7.8 L2; 1.9 C++ exit (cross-cluster); 3.2.1 L1 to L3 and L6 (cross-cluster, P2).
- **Uses.** `marks` (tree nodes and edges), `slider`, `stepper`, `numeric-input`, `value-table`, `plot-2d` (convergence), `region-select` (exercise nodes), `position-editor` (replicate mode), `cashflow-timeline` (replicate mode's bond leg), `array-strip` (vector mode), `live-formula`.
- **New modes.**
  - `crr`: the learner sets $\sigma$ and $N$; the widget shows $u = e^{\sigma\sqrt{\Delta t}}$, $d = 1/u$ and the resulting tree. Checks: numeric $u$, $d$, $q$.
  - `delta`: each internal node shows $\Delta = \frac{V_u - V_d}{S_u - S_d}$ and the bond holding; a path through the tree replays the hedge's rebalancing. Check: numeric $\Delta$ at named nodes.
  - `dividend`: a continuous dividend yield replaces $r$ with $r - q$ in $q$'s numerator.
  - `vector`: one row of `array-strip` holds the terminal payoffs; each backward step overwrites it, and the tree lights the layer the array currently represents. Linked to a `code-cell`, the array follows the learner's own Python by recorded trace (web) or by the reference trace with the learner's printed values (Artifact). This is how 1.7.7 L10 makes the code's single array visible.
  - `state-prices`: each terminal node shows its state price $e^{-rT}\binom{N}{j} q^j (1-q)^{N-j}$; the option price is their payoff-weighted sum.
- **Interactions.** As the original: sliders for $S_0$, $u$, $d$, $r$, $K$, $N$; node fields; tap to mark early exercise; the stepper runs backward induction a layer at a time; arbitrage mode builds a portfolio with `position-editor`. Keyboard: Up and Down follow the up and down moves; Left steps back in time; nodes are fields; E opens the exact editor.
- **State.** `{ params: { S0: number; u: number; d: number; r: number; q?: number; K: number; N: number; sigma?: number }; entries: Record<string, number>; exercise: string[]; step: number; legs?: Leg[] }`.
- **Answers and checks.** `numeric` per node through `multi`; `numeric` for $q$, $\Delta$ and the bond holding; `set` for early-exercise nodes; `arbitrage`; `code` (with `code-cell`).
- **Config.**

```ts
interface BinomialTreeConfig extends BaseConfig {
  S0: number; K: number; r: number; T: number; N: number; NMax: number;
  move: { u: number; d: number } | { crr: { sigma: number } };
  q?: number;                                   // dividend yield
  payoff: { type: 'call' | 'put' | 'digital-call' | 'custom'; expr?: Expr };
  style: 'european' | 'american';
  mode: 'build' | 'replicate' | 'price' | 'arbitrage' | 'converge' | 'crr' | 'delta' | 'dividend' | 'vector' | 'state-prices';
  fill: 'none' | 'terminal' | 'all';
  qMode: 'given' | 'derive';
  link?: { codeCell: string };                  // vector mode
}
```

- **Visual.** As the original: nodes as small rounded rectangles with $S$ above and $V$ below; edges 1.5px ink; learner fields underlined in `--manip`; early-exercise nodes carry a flag glyph; the convergence plot shows tree prices against $N$ as `--s2` dots around the Black-Scholes value in dashed ink. Delta values show in caption type under each node; the vector strip sits under the leaves with each cell aligned to its node.
- **Motion.** Backward induction fills one layer every 320ms (a demonstration the learner starts). In vector mode each overwrite slides the new value down into its cell over 200ms.
- **Show-why.** `q-is-not-p` (the real-world probability slider moves; the price does not), `exercise-beats-holding` (at a flagged node, the exercise value and the continuation value appear side by side), `odd-even` (the convergence dots alternate above and below the line).
- **Reduced motion.** Layers and overwrites appear at once.
- **Accessibility.** The tree also renders as a table by time step and state; arrow keys follow the tree; delta values are read with each node.
- **Tutor.** Ids: `node:<n>,<j>`, `edge:<n>,<j>,up`, `edge:<n>,<j>,down`, `q`, `delta:<n>,<j>`, `bond:<n>,<j>`, `cell:<j>`, `plot:converge`, `slider:<param>`. Secret: the full solved tree.
- **Performance.** Up to $N = 8$ drawn in full on phones; up to $N = 2{,}000$ priced in a worker for convergence plots.
- **Artifact and web.** The vector mode's live trace of learner code needs Pyodide; in the Artifact it uses the reference trace plus the learner's printed array values.
- **Generators.** $(u, d, r)$ with rational $q$ (for example $S_0 = 4$, $u = 2$, $d = \frac{1}{2}$, $r = \frac{1}{4}$ per period gives $q = \frac{1}{2}$); CRR parameter sets; strikes and styles; American puts where early exercise occurs at a known set of nodes.
- **Misconceptions.** `real-probability-prices`, `delta-is-constant`, `american-call-early`, `q-from-sigma-directly`, `discount-once-at-end` (discounting the expected payoff with the wrong number of periods).

---

## 6. Finance composites (1.7)

Every composite below follows the shared contract and section 2. A field that says "base" means the shared rule applies unchanged.

### 6.1 Time value of money

#### 6.1.1 `compounding-lab`: Compounding lab

**Composite · P1 · G1.** Growth of money under simple, compound and continuous interest; conventions; doubling; real against nominal.

- **Purpose.** Make "interest on interest" a visible layer, show that compounding more often has a ceiling ($e^r - 1$), and make conventions explicit before any market quotes a rate.
- **Serves.** 1.7.1 L1 to L5, L10, L11; cross-cluster: 0.1 percentages (Stage 0's `multiplier-chain` covers the arithmetic).
- **Uses.** `plot-2d` (balance against time; effective rate against $m$ on a log axis), `marks` (stacked bars, curves, the asymptote), `slider` (rate, years, $m$ from the list 1, 2, 4, 12, 52, 365, continuous), `drag-point` (prediction handle), `token-tray` (compare mode), `live-formula`, `numeric-input`, `expression-input`; links to `multiplier-chain`.
- **Modes.** `simple`, `blocks`, `doubling`, `frequency`, `continuous`, `real`, `compare`.
- **Interactions.**
  - Pointer: drag the rate, years and $m$; tap a year's bar to split it into principal, interest on principal and interest on interest; before a reveal, drag the prediction handle to where year 10 will be; in compare mode, drag rate cards into order of effective rate.
  - Keyboard: slider keys (base); bars are focusable and Enter splits one; P focuses the prediction handle; compare cards use the token keys.
- **State.** `{ mode: string; rate: number; years: number; m: number | 'cont'; inflation?: number; prediction?: number; split: number[]; order?: string[] }`.
- **Answers and checks.** `numeric` (balance, effective rate, doubling time, real rate); `expression` (conversions such as $r_{\text{annual}} = e^{r_c} - 1$); `ordering` (compare); `point` (the prediction, graded before the reveal).
- **Config.**

```ts
interface CompoundingLabConfig extends BaseConfig {
  mode: 'simple' | 'blocks' | 'doubling' | 'frequency' | 'continuous' | 'real' | 'compare';
  principal: number; currency: 'GBP' | 'USD';
  rate: { init: number; range: [number, number]; step: number };
  years: { init: number; max: number };
  mValues?: Array<number | 'cont'>;
  inflation?: number;
  compare?: { id: string; rate: number; convention: 'simple' | 'annual' | 'monthly' | 'continuous' | 'apr-monthly' }[];
  predictFirst?: boolean;
}
```

- **Visual.** Stacked bars per year: principal outlined in ink, interest on principal `--s3` at 25%, interest on interest `--s2` at 35%, each labelled once; the simple-interest line dashed ink; the continuous curve $e^{rt}$ in `--s3`; in frequency mode, the effective rate against $m$ with the asymptote $e^r - 1$ as dashed ink; convention chips on every rate.
- **Motion.** Bars follow the sliders directly; splitting a bar separates its layers over 300ms.
- **Show-why.** `interest-on-interest` (the `--s2` layer is highlighted growing year by year), `ceiling` (the effective-rate points crowd under the asymptote), `apr-not-ear` (the two rates of a compare pair are drawn as growth over one year).
- **Reduced motion.** Splits appear at once.
- **Accessibility.** Table view by year (principal, simple interest, compound interest, balance); slider values announced on commit ("5%, annual, 10 years: balance 1,628.89 pounds").
- **Tutor.** Describe: "Rate 5% annual, 10 years: 1,000 grows to 1,628.89; interest on interest 128.89." Ids: `slider:rate`, `slider:years`, `slider:m`, `bar:<year>`, `layer:principal`, `layer:simple`, `layer:compound`, `curve:continuous`, `asymptote`, `handle:prediction`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Conversions with tidy answers; doubling times (exact and rule of 72); real rates; compare sets in which the highest APR is not the highest effective rate.
- **Misconceptions.** `simple-for-compound`, `apr-is-ear`, `rule-72-exact`, `frequency-unbounded`, `real-is-difference` (only when inflation is large enough for the approximation to fail the tolerance).

#### 6.1.2 `tvm-timeline`: Time-value timeline

**Composite · P1 · G1.** Present value, NPV, IRR, annuities, perpetuities, loans and discount factors on one timeline.

- **Purpose.** One picture for every discounting idea: a cash flow shrinks as it slides back in time; NPV is the sum of the ghosts; the IRR is where the NPV curve crosses zero.
- **Serves.** 1.7.1 L6 to L9, L12; 2.3.0 (valuation of strategies, optional).
- **Uses.** `cashflow-timeline`, `plot-2d` (NPV against rate; amortisation), `drag-point` (rate on the NPV curve; discount-factor knots), `slider` (rate, payment), `value-table` (schedules), `live-formula`, `numeric-input`, `expression-input`; links to `series-explorer`.
- **Modes.** `pv`, `npv`, `irr`, `annuity`, `perpetuity`, `amortise`, `discount-factors`.
- **Interactions.**
  - Pointer: build or edit flows on the timeline; drag the rate handle along the NPV curve to its zero crossing; in perpetuity mode, the Shift control copies the stream one period later so the learner sees $PV - PV/(1+r) = C/(1+r)$; in amortise mode, drag the payment until the final balance reaches zero; in discount-factor mode, drag knots on a curve under the timeline.
  - Keyboard: `cashflow-timeline` keys; the NPV handle moves along the curve with Left and Right; S applies the shift.
- **State.** `{ mode: string; flows: Flow[]; rate: number; payment?: number; dfKnots?: [number, number][] }`.
- **Answers and checks.** `numeric` (PV, NPV, IRR, payment); `expression` (the annuity formula); `cashflows` (build a described stream); `point` (the IRR on the curve).
- **Config.**

```ts
interface TvmTimelineConfig extends BaseConfig {
  mode: 'pv' | 'npv' | 'irr' | 'annuity' | 'perpetuity' | 'amortise' | 'discount-factors';
  timeline: CashflowTimelineConfig;
  rate: { init: number; range: [number, number]; convention: 'annual' | 'monthly' | 'continuous' };
  loan?: { principal: number; years: number; periodsPerYear: number };
  growth?: number;                              // growing perpetuity
  showNpvCurve: boolean;
}
```

- **Visual.** The timeline above; the NPV curve below in ink with a zero line, the rate handle in `--manip`, crossings marked after grading; amortisation as stacked bars per payment (interest `--s2`, principal `--s3`) with the remaining balance as an ink line.
- **Motion.** Base; discounting slides ghosts (section 2.7).
- **Show-why.** `discount-slide`; `two-irrs` (a stream with two sign changes crosses zero twice); `shift-subtract` (the perpetuity trick animates the copy and the subtraction); `front-loaded-interest`.
- **Reduced motion.** Base.
- **Accessibility.** Table view: $t$, flow, discount factor, present value, cumulative; the NPV curve's table by rate.
- **Tutor.** Describe: "5 flows: pay 1,000 at 0, receive 300 at years 1 to 4. At 8%: NPV −6.36; IRR 7.71%." Ids: `flow:<id>`, `curve:npv`, `handle:rate`, `irr:<n>`, `bar:<k>`, `knot:<t>`, `control:shift`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Streams built from a chosen IRR (the last flow solves the NPV equation), loans with tidy payments, perpetuities and growing perpetuities, streams with two IRRs for the Trap.
- **Misconceptions.** `discount-multiplies`, `sum-without-discounting`, `irr-unique`, `annuity-due-off-by-one`, `growing-perpetuity-sign`.

### 6.2 Shares, returns and portfolios

#### 6.2.1 `share-lab`: Share lab

**Composite · P1 · G1.** What a share is; market capitalisation; issuance and dilution; dividends and the ex-dividend drop; splits and buybacks; adjusted prices; total return; indices.

- **Purpose.** Ground equity in a company's balance: a share is a slice; paying a dividend moves cash from the company to its owners without creating wealth; a split relabels slices.
- **Serves.** 1.7.2 L1 to L5, L10; 1.1 exit data hygiene (cross-cluster: why adjusted closes exist).
- **Uses.** `marks` (company bar divided into share tiles; `event-rug`; price series), `plot-2d` (trading-time axis), `slider` (share count, price, dividend, split ratio, adjustment factor), `stepper` (cum-date, ex-date, pay-date), `region-select` (tap suspicious days), `value-table`, `numeric-input`; links to `drawdown-lab` (returns).
- **Modes.** `ownership`, `issue`, `dividend`, `split`, `buyback`, `total-return`, `index`.
- **Interactions.**
  - Pointer: drag the share count and watch the company bar re-divide; issue shares and watch your slice shrink as cash grows; step through a dividend's dates while your wallet (cash plus shares) stays level; tap days in a price history that look like crashes; drag the adjustment factor until the series is continuous; in index mode, drag four stocks' prices and read a price-weighted and a capitalisation-weighted index side by side, then apply a split and fix the divisor.
  - Keyboard: slider and stepper keys; history days are cells (Space toggles); I switches index views.
- **State.** `{ mode: string; shares: number; price: number; cash: number; step: number; flagged: string[]; adjust: number; prices?: number[]; divisor?: number }`.
- **Answers and checks.** `numeric` (market cap, ex-dividend price, adjusted price, index level, new divisor); `set` (split days); `choice`.
- **Config.**

```ts
interface ShareLabConfig extends BaseConfig {
  mode: 'ownership' | 'issue' | 'dividend' | 'split' | 'buyback' | 'total-return' | 'index';
  company: { cash: number; operating: number; shares: number };
  holder?: { shares: number; cash: number };
  events?: { date: string; kind: 'dividend' | 'split' | 'buyback' | 'issue'; value: number }[];
  history?: { generator: 'price-series'; seed: number; days: number } | number[];
  index?: { stocks: { id: string; price: number; shares: number }[] };
}
```

- **Visual.** The company as a tall bar (a cash band and an operating band) cut into share tiles; the holder's wallet beside it; the price chart with the `event-rug`; the adjusted series dashed `--s3` against the raw series in ink.
- **Motion.** Tiles re-divide directly with the slider; on the ex-date, the dividend's cash slides from the company bar to the wallet over 400ms (a consequence of the learner's step).
- **Show-why.** `wealth-unchanged` (the wallet's total line stays flat across the ex-date), `split-not-crash`, `dilution`.
- **Reduced motion.** Cash moves at once.
- **Accessibility.** "Company value 500 million: cash 50 million, operations 450 million; 10 million shares at 50." Table view of history with raw, factor and adjusted columns.
- **Tutor.** Ids: `tile:<k>`, `band:cash`, `band:ops`, `wallet`, `event:<date>`, `series:raw`, `series:adjusted`, `index:price-weighted`, `index:cap-weighted`, `divisor`.
- **Performance.** Tiles collapse into a proportional bar above 200 shares.
- **Artifact and web.** No difference.
- **Generators.** Corporate-action sequences on `price-series` histories; ex-dividend items; index and divisor items.
- **Misconceptions.** `dividend-is-free-money`, `split-changes-value`, `raw-close-returns`, `index-weights-confused`.

#### 6.2.2 `margin-lab`: Margin and short-selling lab

**Composite · P1 · G1.** Long against short P&L; buying on margin; gearing; maintenance margin and the margin call; short-sale accounts, borrow fees and squeezes.

- **Purpose.** Show, as a balance sheet that moves with the price, why borrowing scales returns in both directions and exactly where the broker calls.
- **Serves.** 1.7.2 L7 to L9; 1.7.5 L9 (futures gearing, by comparison).
- **Uses.** `plot-2d` (P&L against price; equity over time), `marks` (balance-sheet bars, signed fills, the maintenance line), `drag-point` (price handle on the axis), `slider` (initial margin, maintenance margin, borrow fee), `sim-runner` (`gbm` path for the squeeze), `value-table`, `numeric-input`, `choice`.
- **Modes.** `long-short`, `margin`, `short`, `squeeze`.
- **Interactions.**
  - Pointer: drag the price; read equity, return on equity and the margin ratio; drag until the ratio touches maintenance; in short mode, run a path and watch the fee accrue; in squeeze mode, step through a rally.
  - Keyboard: the price handle is a slider; R runs; stepper keys.
- **State.** `{ mode: string; qty: number; entry: number; price: number; initialMargin: number; maintenance: number; feeRate?: number; t?: number }`.
- **Answers and checks.** `numeric` (margin-call price, equity, return on equity); `choice` (bounded or unbounded loss).
- **Formulas shown live.** Long with loan $L$ on $Q$ shares: equity $E = QP - L$; call when $E/(QP) < m$, so $P^* = \frac{L}{Q(1 - m)}$. Short with proceeds and margin $M$ held: $E = (\text{proceeds} + M) - QP$; call when $E/(QP) < m$, so $P^* = \frac{\text{proceeds} + M}{Q(1 + m)}$.
- **Config.**

```ts
interface MarginLabConfig extends BaseConfig {
  mode: 'long-short' | 'margin' | 'short' | 'squeeze';
  qty: number; entry: number;
  initialMargin: number; maintenance: number;   // fractions
  feeRate?: number;                              // annual borrow fee on short value
  path?: { model: 'gbm'; mu: number; sigma: number; days: number; seed: number };
}
```

- **Visual.** Assets, loan and equity bars (the loan hatched and labelled), equity as a signed fill; the maintenance threshold dashed ink ("maintenance 25%"); long and short P&L lines (ink, and dashed ink) with an arrow on the short's unbounded tail.
- **Motion.** Direct.
- **Show-why.** `call-price` (the handle glides to $P^*$ and the ratio meter turns to its threshold), `unbounded-short`, `geared-returns`.
- **Reduced motion.** Base.
- **Accessibility.** "Price 80: assets 8,000, loan 5,000, equity 3,000, margin ratio 37.5%, maintenance 25%."
- **Tutor.** Ids: `handle:price`, `bar:assets`, `bar:loan`, `bar:equity`, `line:maintenance`, `line:long`, `line:short`, `meter:ratio`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Margin-call prices with tidy values; short-account items; fee accruals.
- **Misconceptions.** `short-loss-bounded`, `call-at-zero-equity`, `gearing-adds-return-not-risk`.

#### 6.2.3 `portfolio-lab`: Portfolio lab

**Composite · P1 · G1.** Two-asset diversification, correlation, the minimum-variance portfolio, the efficient frontier, the risk-free asset and the Sharpe ratio, beta, and the diversification floor.

- **Purpose.** The mean-variance picture in the $(\sigma, \mu)$ plane, manipulated directly: correlation bends the curve; a risk-free asset turns the frontier into a line; beta is a slope.
- **Serves.** 1.7.2 L11 to L15; 2.3.2 L7 (breadth, by analogy); cross-cluster: 1.4 quadratic forms (portfolio variance $\mathbf{w}^\top \Sigma \mathbf{w}$).
- **Uses.** `plot-2d` ($(\sigma, \mu)$ plane; return scatter), `drag-point` (portfolio point constrained to the curve; the far end of the capital-market line; a fitted beta line), `slider` ($w$, $\rho$, $n$), `mass-editor` (weights for three or four assets), `marks` (curve, cloud of random portfolios, lines), `live-formula`, `numeric-input`; links to `regression-lab` and `lagrange-explorer`.
- **Modes.** `two-asset`, `n-asset`, `frontier`, `cml`, `beta`.
- **Interactions.**
  - Pointer: drag the portfolio along the two-asset curve (or the $w$ slider); drag $\rho$ from 1 to −1 and watch the curve bend to a point on the $\mu$ axis; in frontier mode, reshape weights with the mass editor and watch the point move among the cloud; in CML mode, rotate a line from the risk-free rate until it just touches the frontier; in beta mode, drag a line through the scatter, then compare with least squares.
  - Keyboard: slider keys; handles move along their constraint; the mass editor's keys.
- **State.** `{ mode: string; w: number[]; rho?: number; n?: number; cmlSlope?: number; betaLine?: { slope: number; intercept: number } }`.
- **Answers and checks.** `point` (minimum-variance and tangency portfolios); `numeric` ($\sigma_p$, weights, Sharpe ratio, beta); `predicate: on-frontier`; `choice`.
- **Formulas shown live.** $\mu_p = w\mu_1 + (1 - w)\mu_2$; $\sigma_p^2 = w^2\sigma_1^2 + (1-w)^2\sigma_2^2 + 2w(1-w)\rho\sigma_1\sigma_2$; $w^* = \frac{\sigma_2^2 - \rho\sigma_1\sigma_2}{\sigma_1^2 + \sigma_2^2 - 2\rho\sigma_1\sigma_2}$; equal weights over $n$ assets with common $\sigma$ and $\rho$: $\sigma_p^2 = \frac{\sigma^2}{n} + \left(1 - \frac{1}{n}\right)\rho\sigma^2$; $\beta = \frac{\mathrm{Cov}(R_i, R_m)}{\mathrm{Var}(R_m)}$.
- **Config.**

```ts
interface PortfolioLabConfig extends BaseConfig {
  mode: 'two-asset' | 'n-asset' | 'frontier' | 'cml' | 'beta';
  assets: { id: string; mu: number; sigma: number }[];
  corr: number[][] | { rho: number; editable: boolean };
  rf?: number;
  shortSelling: boolean;
  cloud?: { n: number; seed: number };
  beta?: { generator: 'market-gen/beta'; seed: number; beta: number; idio: number; n: number };
}
```

- **Visual.** $\sigma$ on $x$, $\mu$ on $y$; assets as labelled ink points; the frontier curve in `--s3`; the learner's portfolio a `--manip` handle; the cloud as ink dots at 20%; the learner's capital-market line in `--manip`; after grading, the tangency point and minimum-variance point as dashed ink markers; in n-asset mode, $\sigma_p$ against $n$ with the floor $\sqrt{\rho}\,\sigma$ as a dashed labelled line.
- **Motion.** Direct; the curve redraws on the $\rho$ slider's frame.
- **Show-why.** `rho-bends-curve`, `min-variance-left-of-both` (the curve's leftmost point is less risky than either asset), `tangent-max-slope`, `floor`.
- **Reduced motion.** Base.
- **Accessibility.** "Weight in A 0.62: volatility 13.1%, expected return 7.2%, Sharpe 0.40." Table view of the curve by weight.
- **Tutor.** Ids: `asset:<id>`, `handle:portfolio`, `curve:frontier`, `line:cml`, `point:tangency`, `point:min-var`, `slider:rho`, `line:beta`, `cloud`.
- **Performance.** At most four assets; the cloud of 2,000 portfolios on Canvas 2D.
- **Artifact and web.** No difference.
- **Generators.** $(\sigma_1, \sigma_2, \rho, \mu_1, \mu_2)$ with tidy minimum-variance weights; tangency items; beta datasets from `market-gen` with a planted beta.
- **Misconceptions.** `diversify-needs-negative-corr`, `min-var-is-safer-asset`, `max-sharpe-is-max-return`, `beta-is-correlation`, `n-stocks-zero-risk`.

### 6.3 Bonds and the yield curve

#### 6.3.1 `bond-lab`: Bond lab

**Composite · P1 · G1.** A bond as cash flows; price as present value; the price-yield curve; par, premium and discount; yield to maturity; pull to par; accrued interest; credit spreads.

- **Purpose.** Tie every bond number to arrows on a timeline, so "price falls when yields rise" is seen as every arrow's present value shrinking at once.
- **Serves.** 1.7.3 L1 to L5, L14, L15.
- **Uses.** `cashflow-timeline`, `plot-2d` (price against yield; price against time to maturity), `drag-point` (yield handle on the curve; settlement date), `slider` (coupon, maturity, hazard rate, recovery), `live-formula`, `numeric-input`, `value-table`.
- **Modes.** `cashflows`, `price-yield`, `ytm`, `pull-to-par`, `accrued`, `credit`.
- **Interactions.**
  - Pointer: set coupon and maturity and watch the arrows appear; drag the yield along the price-yield curve while the timeline's ghosts shrink or grow; in YTM mode, drag until the present value meets the quoted price line; in pull-to-par mode, drag the valuation date towards maturity; in accrued mode, drag the settlement date through a coupon period; in credit mode, raise the hazard rate and watch each arrow's survival weighting.
  - Keyboard: slider and handle keys; D focuses the date handle.
- **State.** `{ mode: string; face: number; coupon: number; freq: 1 | 2 | 4; maturity: number; yield: number; settle?: string; hazard?: number; recovery?: number }`.
- **Answers and checks.** `cashflows` (build the bond); `numeric` (price, YTM, accrued, spread); `choice` (premium or discount); `curve` (a predicted pull-to-par path).
- **Formulas shown live.** $P = \sum_{k=1}^{n} \frac{c/m}{(1 + y/m)^k} + \frac{F}{(1 + y/m)^n}$; accrued $= \frac{c}{m} \times \frac{\text{days since last coupon}}{\text{days in period}}$ under the stated day count; risky price $\approx \sum CF_t \, DF_t \, S(t)$ plus recovery, with spread $\approx \lambda(1 - R)$.
- **Config.**

```ts
interface BondLabConfig extends BaseConfig {
  mode: 'cashflows' | 'price-yield' | 'ytm' | 'pull-to-par' | 'accrued' | 'credit';
  face: number; coupon: number; freq: 1 | 2 | 4; maturity: number;
  yield: { init: number; range: [number, number] };
  quote?: number;                               // clean price for ytm mode
  dayCount?: 'ACT/365F' | 'ACT/360' | '30/360' | 'ACT/ACT-ICMA';
  dates?: { issue: string; settle: string };
  credit?: { hazard: number; recovery: number };
}
```

- **Visual.** The timeline above (coupon arrows in ink, the final principal tall); the price-yield curve in ink, convex, with the par line (100) dashed and the quote line labelled; the yield handle `--manip`; the dirty price as an ink sawtooth and the clean price as dashed `--s3`; survival-weighted ghosts in `--s3`.
- **Motion.** Ghosts follow the yield handle directly.
- **Show-why.** `inverse` (raising the yield shrinks every ghost at once), `coupon-vs-yield` (premium when the coupon exceeds the yield), `sawtooth`.
- **Reduced motion.** Base.
- **Accessibility.** "5-year 4% annual bond at 5% yield: price 95.67, discount." Table of flows with discount factors.
- **Tutor.** Ids: `flow:<k>`, `curve:price-yield`, `handle:yield`, `line:quote`, `line:par`, `series:dirty`, `series:clean`, `slider:hazard`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Bonds priced from a chosen yield, the price rounded to the quoting precision, the YTM answer recomputed from the rounded price; accrued-interest items under each day count; credit items.
- **Misconceptions.** `price-yield-same-direction`, `ytm-is-coupon`, `clean-includes-accrued`, `spread-is-default-probability`.

#### 6.3.2 `yield-curve-lab`: Yield curve lab

**Composite · P1 · G1.** Discount factors, zero rates, bootstrapping, forward rates, curve shapes and moves, and swaps.

- **Purpose.** One curve prices every safe cash flow; bootstrapping recovers it from bonds one maturity at a time; forwards are what today's curve locks in.
- **Serves.** 1.7.3 L6 to L9, L16; 2.3.3 (rates for option pricing).
- **Uses.** `plot-2d` (zero rates and discount factors against maturity), `drag-point` (curve knots), `cashflow-timeline` (bond flows being peeled; swap legs in two lanes), `slider` (parallel shift, twist), `value-table` (bond quotes and the learner's entries), `live-formula`, `numeric-input`.
- **Modes.** `discount-factors`, `bootstrap`, `forwards`, `shapes`, `swap`.
- **Interactions.**
  - Pointer: in bootstrap mode, each bond row lights its earlier coupons already discounted by known factors, and the learner enters the remaining factor; in forwards mode, two route diagrams (1 year then a 1-year forward, against a 2-year zero) are equalised by dragging the forward; in shapes mode, drag knots or apply shift and twist and read each bond's price change; in swap mode, set the fixed rate until the swap's value is zero.
  - Keyboard: table cells; knots move with Up and Down; S and W focus the shift and twist sliders.
- **State.** `{ mode: string; knots: [number, number][]; entries: Record<string, number>; shift?: number; twist?: number; swapRate?: number }`.
- **Answers and checks.** `numeric` per maturity through `multi`; `numeric` (forward rate, par swap rate); `choice` (which bond loses most).
- **Formulas shown live.** $DF(t) = (1 + z_t)^{-t}$ (annual) or $e^{-z_t t}$ (continuous); $f_{t_1, t_2} = \left(\frac{DF(t_1)}{DF(t_2)}\right)^{1/(t_2 - t_1)} - 1$; par swap rate with annual fixed payments $s = \frac{1 - DF(n)}{\sum_{i=1}^{n} DF(i)}$.
- **Config.**

```ts
interface YieldCurveLabConfig extends BaseConfig {
  mode: 'discount-factors' | 'bootstrap' | 'forwards' | 'shapes' | 'swap';
  convention: 'annual' | 'continuous';
  curve: { knots: [number, number][]; editable: boolean; interp: 'linear-zero' | 'log-linear-df' };
  bonds?: { id: string; coupon: number; maturity: number; price: Entry }[];
  swap?: { maturity: number; notional: number };
  portfolio?: { bondId: string; qty: number }[];
}
```

- **Visual.** The zero curve in ink through its knots (`--manip` when editable); forwards as an `--s3` step line; discount factors in a second panel; swap lanes labelled "fixed" and "floating".
- **Motion.** Direct; peeling a bond fades its known coupons into ghosts over 300ms after the learner confirms each row.
- **Show-why.** `peel`, `two-routes`, `float-at-par` (the floating leg's value collapses to par at each reset).
- **Reduced motion.** Base.
- **Accessibility.** Table of maturity, discount factor, zero rate and forward rate.
- **Tutor.** Ids: `knot:<t>`, `row:<bond>`, `entry:<t>`, `route:a`, `route:b`, `lane:fixed`, `lane:float`, `slider:shift`, `slider:twist`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Bonds generated from chosen rational discount factors so bootstrapped answers are exact; forward items; par swap rates.
- **Misconceptions.** `forward-is-average`, `zero-equals-par-yield`, `floating-leg-unknowable`.

#### 6.3.3 `duration-lab`: Duration and convexity lab

**Composite · P1 · G1.** Macaulay duration as the balance point of present values; modified duration and DV01; convexity; immunisation; the effect of coupon and maturity.

- **Purpose.** Make duration a physical balance point before it becomes a derivative, then show the tangent and the curvature on the price-yield curve.
- **Serves.** 1.7.3 L10 to L13, L17; 2.3.3 (rate risk of option books, by analogy).
- **Uses.** `cashflow-timeline` (with fulcrum), `plot-2d` (price against yield with tangent and quadratic), `drag-point` (fulcrum; yield), `slider` (coupon, maturity, yield shock, bond weights), `live-formula`, `numeric-input`, `choice`.
- **Modes.** `fulcrum`, `tangent`, `convexity`, `immunise`, `compare`.
- **Interactions.**
  - Pointer: in fulcrum mode, present-value blocks stand at each date and the learner drags the fulcrum until the beam balances (the beam tilts by its torque); in tangent mode, drag the yield and predict the price after +1 basis point from the tangent; in convexity mode, add the second-order term and slide a ±300 basis point shock to compare errors; in immunise mode, set holdings of two bonds so value and duration match a liability; in compare mode, two bonds side by side.
  - Keyboard: F focuses the fulcrum (Left and Right move it by 0.05 years); slider keys.
- **State.** `{ mode: string; fulcrum?: number; yield: number; shock?: number; weights?: [number, number] }`.
- **Answers and checks.** `numeric` (Macaulay and modified duration, DV01, convexity, estimated price); `predicate: balanced`, `predicate: immunised`; `choice`.
- **Formulas shown live.** $D = \frac{\sum_t t \, PV_t}{P}$; $D_{\text{mod}} = \frac{D}{1 + y/m}$; $\text{DV01} = D_{\text{mod}} \, P \times 10^{-4}$; $\frac{\Delta P}{P} \approx -D_{\text{mod}}\,\Delta y + \frac{1}{2} C\,(\Delta y)^2$.
- **Config.**

```ts
interface DurationLabConfig extends BaseConfig {
  mode: 'fulcrum' | 'tangent' | 'convexity' | 'immunise' | 'compare';
  bonds: { id: string; coupon: number; maturity: number; freq: 1 | 2 }[];
  yield: number;
  liability?: { t: number; amount: number };
  shockRange?: [number, number];                // basis points
}
```

- **Visual.** The beam as an ink line on the axis; present-value blocks in `--s3` stacked at each date; the fulcrum a `--manip` triangle; the beam tilts; the price-yield curve in ink, the tangent in `--s2`, the quadratic approximation dashed `--s6`, the error between them shaded.
- **Motion.** The beam tilts with `spring-physical` on each fulcrum release (a consequence of the drag); the curves are direct.
- **Show-why.** `tilt`, `tangent-under` (the convex curve lies above its tangent on both sides), `coupon-pulls-early`.
- **Reduced motion.** The beam shows its final angle at once.
- **Accessibility.** "Fulcrum at 4.40 years; beam tips right; balance point is later." Table of $t$, PV and $t \times PV$.
- **Tutor.** Ids: `fulcrum`, `block:<t>`, `beam`, `curve:price-yield`, `line:tangent`, `curve:quadratic`, `slider:shock`, `bond:<id>`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Bonds with tidy durations; DV01 items; immunisation items with a unique solution.
- **Misconceptions.** `duration-is-maturity`, `higher-coupon-longer`, `linear-is-enough`, `convexity-hurts-holder`.

### 6.4 The order book

#### 6.4.1 `order-book`: Limit order book

**Composite · P1 · G1.** Resting limit orders; best bid and ask; spread and mid; market orders walking the book; price-time priority and queue position; order types; depth and slippage; imbalance and the microprice; fees; tick size; resilience. It carries the order-book part of the 1.7 exit.

- **Purpose.** Let the learner be a participant: place orders, watch them rest in queues, send orders that cross the spread, and see exactly which resting orders fill at what prices.
- **Serves.** 1.7.4 L1 to L11, L13; 1.7.9 L2, L13; 3.3.4 (quote mode, optional).
- **Uses.** `price-ladder`, `order-ticket`, `quote-entry` (quote mode), `plot-2d` with `marks` `depth` (depth chart), `value-table` (`blotter`), `stepper` (replay speed), `sim-runner` (`order-flow`), `token-tray` (queue predictions), `numeric-input`, `choice`.
- **Modes.** `explore`, `place`, `spread`, `walk`, `queue`, `race`, `types`, `depth`, `imbalance`, `fees`, `tick`, `resilience`, `quote`.
- **Interactions.**
  - Pointer: ladder and ticket interactions (sections 3.1 and 3.4); in predict-first screens, the learner enters the prediction (fills, queue order or the book after) before Send unlocks; in race mode, the learner chooses a limit price or a market order and presses Run, and a seeded flow plays until fill or timeout; across 20 seeds the screen shows fill rate and average cost, never graded; in resilience mode, a large market order hits and the book refills over replayed time; in tick mode, a tick-size slider regroups the same orders into fewer, longer queues.
  - Keyboard: ladder and ticket keys; R runs a race; replay with the stepper keys and speed control.
- **State.** `{ mode: string; book: BookSnapshot; myOrders: OrderSpec[]; staged?: OrderSpec; prediction?: unknown; log: Event[]; replay?: { t: number; speed: number } }`. The book is derived by `exchange-sim` from the config and the learner's actions, so the persisted state is the action log.
- **Answers and checks.** `numeric` (spread, mid, average fill price, microprice, all-in cost with fees); `fills`; `book`; `ordering` (queue); `order`; `set`; `choice`.
- **Formulas shown live.** Spread $= a - b$; mid $= \frac{a + b}{2}$; microprice $= \frac{a\,Q_b + b\,Q_a}{Q_a + Q_b}$; imbalance $I = \frac{Q_b - Q_a}{Q_b + Q_a}$; average fill price $= \frac{\sum_i q_i p_i}{\sum_i q_i}$.
- **Config.**

```ts
interface OrderBookConfig extends BaseConfig {
  mode: 'explore' | 'place' | 'spread' | 'walk' | 'queue' | 'race' | 'types' | 'depth'
      | 'imbalance' | 'fees' | 'tick' | 'resilience' | 'quote';
  tick: number; lot: number;
  book: { bids: [number, number][]; asks: [number, number][] }
      | { generator: 'market-gen/book'; seed: number; levels: number; sizeScale: number };
  queues?: Record<string, { id: string; owner: 'you' | string; qty: number; t: number }[]>;
  order?: Partial<OrderSpec>;
  flow?: { model: 'zero-intelligence' | 'informed-mix'; seed: number; ratePerSec: number; durationS: number };
  fees?: { maker: number; taker: number };       // per share; negative is a rebate
  amendRule: 'lose-on-price-or-increase' | 'always-lose';
  predictFirst?: boolean;
  show: { depth: boolean; blotter: boolean; microprice: boolean; queuePositions: boolean;
          fills: 'live' | 'after-check' };
}
```

- **Visual.** The ladder at the centre; the ticket below on phones and beside on desktop; the depth chart optional on the right; the blotter collapsible; the microprice a small `--s3` tick on the price column between bid and ask.
- **Motion.** Fills walk the levels (section 2.7); resting orders spring into their queue slot; replays at the chosen speed.
- **Show-why.** `eat-levels` (the market order consumes levels one by one with running quantity and cost), `cross-spread` (a buyer meets the ask, not the mid), `queue-ahead` (orders ahead of yours light in priority order), `limit-not-filled` (the replay shows the price moving away from a resting order), `amend-to-back`.
- **Reduced motion.** Fills appear at once with a fill list; replays step.
- **Accessibility.** Ladder grid semantics; fills announced; the depth chart has a table view; race results as a table.
- **Tutor.** Describe: "Best bid 99.98 (300), best ask 100.01 (200), spread 0.03. Staged: market buy 500. No fills yet." Ids: the ladder's, plus `ticket:*`, `depth`, `microprice`, `fill:<n>`, `queue:<tick>:<k>`, `race:result`. Secret: in race mode, the future flow and the fill outcome.
- **Performance.** Section 2.10; races of 20 seeds run in under 200ms in a worker.
- **Artifact and web.** No difference.
- **Generators.** Seeded books; market orders sized to consume a chosen number of levels with tidy averages; queue items with mixed arrival times; order-type items (post-only rejections, stop triggers, IOC partial fills, FOK kills); imbalance and fee items.
- **Misconceptions.** `fills-at-best-ask`, `trades-at-mid`, `limit-always-better`, `market-order-free`, `queue-by-size`, `amend-keeps-priority`, `stop-is-limit`, `ioc-rests`.

#### 6.4.2 `auction-lab`: Call auction lab

**Composite · P1 · G1.** Opening and closing auctions: aggregate demand and supply, the uncrossing price that maximises executed volume, tie-breaks, imbalance, and the indicative price during the call.

- **Purpose.** Show that a call auction is one price for everyone, chosen where the cumulative demand and supply curves cross, and that your own order moves the indicative price.
- **Serves.** 1.7.4 L10; 2.3.4 (closing prices in candles, by reference).
- **Uses.** `price-ladder` (supply and demand columns), `plot-2d` (cumulative curves), `marks` (step curves; executable-volume bars), `drag-point` (candidate price), `order-ticket` (your order), `value-table`, `numeric-input`, `choice`.
- **Interactions.**
  - Pointer: drag a candidate price and read executable volume $\min(D(p), S(p))$, where $D(p)$ is the buy quantity willing to pay at least $p$ and $S(p)$ the sell quantity willing to accept at most $p$; find the maximum; add your own order and watch the indicative price move.
  - Keyboard: the candidate handle steps by ticks; ticket keys.
- **State.** `{ orders: OrderSpec[]; candidate: number; myOrder?: OrderSpec }`.
- **Answers and checks.** `numeric` (uncrossing price, volume, imbalance); `choice` (which tie-break applies).
- **Config.**

```ts
interface AuctionLabConfig extends BaseConfig {
  tick: number; lot: number;
  orders: { side: 'buy' | 'sell'; px: number | 'market'; qty: number }[] | { generator: 'market-gen/auction'; seed: number };
  tieBreak: ('max-volume' | 'min-imbalance' | 'market-pressure' | 'reference-price')[];
  referencePrice?: number;
  allowOwnOrder: boolean;
}
```

- **Visual.** Cumulative demand as an `--s6` step curve, supply as an `--s2` step curve; executable volume as ink bars by price; the candidate a `--manip` handle; the uncrossing price after grading as a dashed ink line.
- **Motion.** Direct.
- **Show-why.** `max-volume`, `tie-break`.
- **Reduced motion.** Base.
- **Accessibility.** Table by price: cumulative demand, cumulative supply, executable volume, imbalance.
- **Tutor.** Ids: `handle:candidate`, `curve:demand`, `curve:supply`, `bar:<tick>`, `order:<id>`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Order sets with a unique maximum-volume price; sets that need the second or third tie-break.
- **Misconceptions.** `auction-at-midpoint`, `max-volume-is-most-orders`.

### 6.5 Forwards and futures

#### 6.5.1 `carry-arb`: Cash-and-carry lab

**Composite · P1 · G2.** Forward pricing by no-arbitrage: cash and carry, reverse cash and carry, income and yields, storage and convenience yield, covered interest parity, valuing an existing forward, and the forecast Trap.

- **Purpose.** Derive the forward price by building the trade that would profit if it were wrong. The learner sees the replication as lanes of cash flows whose net today is zero.
- **Serves.** 1.7.5 L2 to L6, L14; 1.7.6 L13 to L15 (the same replication logic, extended to options); cross-cluster: 3.2.1 L1 (no-arbitrage in discrete time).
- **Uses.** `cashflow-timeline` (lanes: Cash, Asset, Forward, and Income where present), `position-editor` (legs: stock, bond or cash, forward), `slider` ($r$, $q$, $T$, the quoted forward), `live-formula`, `derivation-steps` (L4), `numeric-input`, `choice`.
- **Modes.** `build`, `arbitrage`, `income`, `fx`, `value`, `trap`.
- **Interactions.**
  - Pointer: add legs (borrow $S_0$, buy the asset, sell the forward at the quoted $F$); the timeline fills each lane's flows at $0$ and $T$; the net row at $0$ must be zero (self-financing); the net at $T$ is $F - S_0 e^{rT}$; drag the quoted $F$ and watch the profit at $T$ cross zero at the fair forward; income mode adds dividend flows that reduce the carry; FX mode swaps the asset for a foreign deposit.
  - Keyboard: `position-editor` and `cashflow-timeline` keys; F focuses the quoted-forward handle.
- **State.** `{ mode: string; legs: Leg[]; quoteF: number; r: number; q?: number; income?: { t: number; amount: number }[]; storage?: number; rf?: number }`.
- **Answers and checks.** `numeric` (fair forward; value of an existing forward $f = (F_0 - K)e^{-rT}$); `predicate: is-arbitrage`, `predicate: self-financing`; `expression` ($F_0 = S_0 e^{(r - q)T}$, $F_0 = (S_0 - I)e^{rT}$, $F_0 = S_0 e^{(r_d - r_f)T}$); `choice`.
- **Config.**

```ts
interface CarryArbConfig extends BaseConfig {
  mode: 'build' | 'arbitrage' | 'income' | 'fx' | 'value' | 'trap';
  S0: number; T: number;
  r: Entry; q?: Entry; rf?: Entry;              // continuous rates
  income?: { t: number; amount: number }[];
  storage?: Entry; convenience?: Entry;
  quoteF: { init: number; range: [number, number]; editable: boolean };
  K?: number;                                    // value mode: the existing contract's delivery price
  lockedLegs?: string[];
}
```

- **Visual.** Lanes with labels; the net row in bold; the profit at $T$ as a signed fill on the net arrow; the quoted-forward handle in `--manip` on a short price axis; the fair forward as an `--s3` marker; convention chips on every rate ("continuous").
- **Motion.** Direct; when a leg is added, its flows draw in over 200ms.
- **Show-why.** `net-zero-today`, `profit-at-T`, `rate-moves-forward` (the Trap: the rate slider moves the fair forward while a "forecast" marker stays still).
- **Reduced motion.** Base.
- **Accessibility.** "Borrow lane: receive 100 today, pay 105.13 at 1 year. Asset lane: pay 100 today, deliver the asset. Forward lane: receive 107 at 1 year. Net today 0; net at 1 year +1.87."
- **Tutor.** Ids: `lane:<id>`, `flow:<id>`, `net:0`, `net:T`, `handle:F`, `marker:fair`, `leg:<id>`. Secret: the fair forward.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** $(S_0, r, q, T)$ with mispricings of either sign; FX items with domestic and foreign rates; existing-forward valuations; income schedules.
- **Misconceptions.** `forward-is-forecast`, `forget-income`, `fx-forward-wrong-way`, `existing-forward-undiscounted`.

#### 6.5.2 `futures-mtm`: Futures settlement lab

**Composite · P1 · G2.** Daily settlement, variation margin, initial and maintenance margin, margin calls, notional against margin, basis and convergence, contango and backwardation.

- **Purpose.** Futures P&L arrives every day; the learner keeps the margin account by hand until the pattern is obvious, then sees basis converge at expiry.
- **Serves.** 1.7.5 L7 to L10.
- **Uses.** `plot-2d` (futures path with settlement dots; the account balance; spot and futures; a term structure), `value-table` (settlement ledger: day, settlement price, daily gain, cumulative gain, balance, call), `drag-point` (day cursor; path points in margin mode), `slider` (contracts, margins), `numeric-input`, `choice`.
- **Modes.** `daily`, `margin`, `gearing`, `basis`, `term`.
- **Interactions.**
  - Pointer: step day by day, filling the daily gain and balance cells; in margin mode, drag a path point down until the balance falls below maintenance and the call appears; in basis mode, drag the time cursor to expiry; in term mode, switch between a carry market and a convenience-yield market.
  - Keyboard: ledger cells as a grid; Left and Right move the day cursor; Enter confirms a row.
- **State.** `{ mode: string; day: number; path: number[]; entries: Record<string, number>; position: 'long' | 'short'; contracts: number }`.
- **Answers and checks.** `numeric` per cell through `multi`; `numeric` (call amount, return on margin, basis); `choice` (contango or backwardation; which side pays).
- **Config.**

```ts
interface FuturesMtmConfig extends BaseConfig {
  mode: 'daily' | 'margin' | 'gearing' | 'basis' | 'term';
  contract: { multiplier: number; tick: number };
  initialMargin: number; maintenanceMargin: number;   // per contract
  path: number[] | { generator: 'price-series'; seed: number; days: number };
  spot?: number[];
  term?: { expiries: number[]; prices: number[] };
  position: 'long' | 'short'; contracts: number;
  fill: 'none' | 'first-row' | 'all';
}
```

- **Visual.** The ledger beside the charts; the balance in ink with the maintenance line dashed and the initial line dotted, both labelled; call markers with the amount; spot in ink and futures in `--s3` meeting at expiry.
- **Motion.** Rows appear as the learner steps; nothing moves on its own.
- **Show-why.** `variation-flows` (each day's gain moves between the two accounts), `call-restores-initial` (the top-up goes back to the initial margin, not to maintenance), `convergence`.
- **Reduced motion.** Base.
- **Accessibility.** The ledger is the table view; calls announced ("Day 4: balance 3,400 below maintenance 4,000; call 2,600 to restore 6,000").
- **Tutor.** Ids: `cell:<day>:<col>`, `line:balance`, `line:maintenance`, `line:initial`, `marker:call:<day>`, `cursor:day`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Paths with calls on known days and tidy amounts; contract specifications; term structures of both shapes.
- **Misconceptions.** `call-tops-to-maintenance`, `futures-pnl-at-expiry-only`, `contango-means-expected-rise`.

#### 6.5.3 `hedge-lab`: Hedging lab

**Composite · P1 · G2.** Hedging with futures; basis risk; the minimum-variance hedge ratio; the number of contracts; beta hedging.

- **Purpose.** The best hedge ratio is a regression slope, not 1; what remains after hedging is the part of the risk the future cannot explain.
- **Serves.** 1.7.5 L11 to L13; 2.3.2 L4 (market neutralising, by analogy).
- **Uses.** `plot-2d` (scatter of spot changes against futures changes; hedged variance against the hedge ratio), `drag-point` (slope handle; a point on the variance parabola), `slider` ($\rho$, $\sigma_S$, $\sigma_F$), `marks` (scatter, line, parabola, histogram), `position-editor` (contracts), `live-formula`, `numeric-input`, `choice`.
- **Modes.** `basic`, `min-var`, `beta`.
- **Interactions.**
  - Pointer: drag the hedge-ratio line through the scatter while the hedged P&L histogram narrows or widens; drag along the variance parabola to its minimum; enter the number of contracts; in beta mode, size an index-futures hedge for a portfolio.
  - Keyboard: the slope handle and parabola handle step by 0.01; slider keys.
- **State.** `{ mode: string; h: number; contracts?: number }`.
- **Answers and checks.** `numeric` ($h^*$, contracts); `point`; `predicate: min-variance-hedge`; `choice`.
- **Formulas shown live.** Hedged variance $\sigma_S^2 - 2h\rho\sigma_S\sigma_F + h^2\sigma_F^2$; $h^* = \rho\frac{\sigma_S}{\sigma_F}$; residual variance $\sigma_S^2(1 - \rho^2)$; contracts $N^* = \frac{h^* Q_A}{Q_F}$; beta hedge $N = \beta\frac{V_A}{F \times \text{multiplier}}$.
- **Config.**

```ts
interface HedgeLabConfig extends BaseConfig {
  mode: 'basic' | 'min-var' | 'beta';
  sigmaS: number; sigmaF: number; rho: number;
  sample?: { generator: 'market-gen/pair'; seed: number; n: number };
  exposure?: { qty: number; contractSize: number };
  beta?: { value: number; portfolio: number; futures: number; multiplier: number };
}
```

- **Visual.** The scatter in ink dots; the learner's line through the origin with slope $h$ in `--manip`; the variance parabola in ink; after grading, the minimum as a dashed marker; the hedged P&L histogram in `--s2`.
- **Motion.** Direct.
- **Show-why.** `residual-is-basis`, `one-to-one-not-optimal`.
- **Reduced motion.** Base.
- **Accessibility.** "Hedge ratio 0.80 with correlation 0.9: hedged standard deviation 0.87% against 2.00% unhedged."
- **Tutor.** Ids: `handle:h`, `scatter`, `curve:variance`, `hist:hedged`, `slider:rho`. Secret: $h^*$.
- **Performance.** Scatter up to 1,500 points in SVG.
- **Artifact and web.** No difference.
- **Generators.** $(\sigma_S, \sigma_F, \rho)$ with tidy $h^*$; contract sizes; beta hedges.
- **Misconceptions.** `hedge-ratio-one`, `hedge-removes-all-risk`, `beta-with-correlation`.

### 6.6 Options: payoffs, bounds and parity

#### 6.6.1 `payoff-builder`: Payoff builder

**Composite · P1 · G2.** Build positions from calls, puts, stock, bonds and forwards; see payoff and profit at expiry and value today; drag strikes; find break-evens; match target payoffs.

- **Purpose.** The central options canvas. Every strategy is a sum of simple lines; every kink is a strike; every slope change is a count of options.
- **Serves.** 1.7.5 L1; 1.7.6 L1 to L10; 1.7.8 L12 (with `greeks-lab`); 2.3.3; 3.3.3 L12 (option-style bets).
- **Uses.** `plot-2d`, `marks` (`payoff`, `signed-fill`, leg lines, value-today curve), `position-editor`, `drag-point` (strike handles on the $S_T$ axis; probe cursor), `slider` ($\sigma$ and time to expiry for value-today), `sketch-pad` (piecewise-linear mode), `live-formula`, `numeric-input`, `choice`.
- **Modes.** `single`, `legs`, `profit`, `value-today`, `match`, `sketch-first`, `forward`, `name`.
- **Interactions.**
  - Pointer: add legs from the palette; drag a strike handle and its kink moves; drag the probe along $S_T$ and read each leg's contribution and the total; toggle payoff, profit and value today; in match mode, the target is a dashed curve; in sketch-first mode, the learner sketches the payoff before the legs appear.
  - Keyboard: `position-editor` keys; strike handles step along the strike grid; P focuses the probe; V cycles views.
- **State.** `{ mode: string; legs: Leg[]; view: 'payoff' | 'profit' | 'value'; probe?: number; sketch?: unknown; tau?: number }`.
- **Answers and checks.** `position`; `payoff` (with `minimalLegs` for "fewest legs"); `numeric` (break-evens, maximum profit, maximum loss, value at a price; "unbounded" is a special value); `choice` (strategy name); `curve` (the sketch, graded by the kink features).
- **Config.**

```ts
interface PayoffBuilderConfig extends BaseConfig {
  mode: 'single' | 'legs' | 'profit' | 'value-today' | 'match' | 'sketch-first' | 'forward' | 'name';
  editor: PositionEditorConfig;
  initial?: Leg[];
  target?: Leg[] | PayoffSpec;
  range: [number, number];
  model?: { S0: number; sigma: number; r: number; q?: number; T: number };   // premiums and value-today
  show: { legs: boolean; probe: boolean; breakevens: boolean; slopes: boolean; signedFill: boolean };
}
```

- **Visual.** Leg lines at 1.5px in `--s2`, `--s6`, `--s4`, `--s5` with direct labels; the total as a 2.5px `--manip` curve; profit and loss as a signed fill; kink dots; slope labels between kinks ("slope +1"); break-evens as ink ticks with values; arrows on unbounded tails; value today as a dashed `--s3` curve; the target as dashed ink.
- **Motion.** Direct for strikes and the probe.
- **Show-why.** `sum-legs` (each leg's line translates into the total, 600ms), `kink-slopes` (the slope change at each strike equals the number of calls struck there), `premium-shift` (profit is payoff shifted down by the net premium).
- **Reduced motion.** A before-and-after pair for `sum-legs`.
- **Accessibility.** "Long call 95, short 2 calls 100, long call 105: payoff 0 below 95, rising to 5 at 100, back to 0 at 105 and above. Net premium 0.62 paid. Break-evens 95.62 and 104.38." Table view at each kink.
- **Tutor.** Ids: `leg:<id>`, `handle:K:<id>`, `curve:total`, `curve:leg:<id>`, `kink:<K>`, `breakeven:<n>`, `probe`, `target`. Secret: in match mode, one minimal solution.
- **Performance.** Exact at kinks; up to 20 legs.
- **Artifact and web.** No difference.
- **Generators.** Targets from random leg sets (one to four legs, strikes on the grid); break-even items; strategy-name items; sketch items.
- **Misconceptions.** `payoff-includes-premium`, `short-put-unbounded`, `straddle-profits-at-strike`, `butterfly-bets-on-move`.

#### 6.6.2 `option-bounds`: No-arbitrage bounds

**Composite · P1 · G2.** Bounds on European call and put prices; American calls on non-dividend stocks; monotonicity, slope and convexity across strikes.

- **Purpose.** Before any model, prices must lie in a region; outside it, a trade makes money in every state. The learner finds the trade.
- **Serves.** 1.7.6 L11, L12, L16; 2.3.3 L6 (strike convexity is the butterfly check on the surface).
- **Uses.** `plot-2d` (bounds region against $S$; prices against $K$), `drag-point` (quote points), `position-editor` (the arbitrage), `marks` (region, bounds, chords), `live-formula`, `numeric-input`, `choice`.
- **Modes.** `spot`, `strikes`, `american`.
- **Interactions.**
  - Pointer: drag a quote point and commit a judgement (inside or outside) before the region is revealed; if outside, build the arbitrage with the position editor and confirm it pays in every state; in strikes mode, drag three call quotes and read the butterfly's cost; in American mode, compare the exercise value with the lower bound.
  - Keyboard: quote handles step by 0.01; `position-editor` keys.
- **State.** `{ mode: string; quotes: Record<string, number>; judgement?: 'inside' | 'outside'; legs: Leg[] }`.
- **Answers and checks.** `choice`; `predicate: is-arbitrage`; `numeric` (bound values); `set` (violating quotes).
- **Formulas shown live.** $\max(S_0 - Ke^{-rT}, 0) \le c \le S_0$; $\max(Ke^{-rT} - S_0, 0) \le p \le Ke^{-rT}$; across strikes $c(K)$ is decreasing, with slope between $-e^{-rT}$ and 0, and convex.
- **Config.**

```ts
interface OptionBoundsConfig extends BaseConfig {
  mode: 'spot' | 'strikes' | 'american';
  S0: number; r: number; T: number;
  K?: number;
  quotes: { id: string; type: 'call' | 'put'; K: number; price: number; editable: boolean }[];
  predictFirst: boolean;
}
```

- **Visual.** The region between the lower bound and the upper bound filled `--bg-sunken` with both bounds in ink and labelled; intrinsic value dashed; quote points `--manip`; in strikes mode, chords between quotes in `--s3`, and a chord below a middle quote marks a convexity violation after grading.
- **Motion.** Direct.
- **Show-why.** `below-lower-bound` (the arbitrage's flows appear on a mini timeline), `chord-above`, `alive-worth-more`.
- **Reduced motion.** Base.
- **Accessibility.** "Call quoted 3.00; lower bound 4.88; outside the region by 1.88."
- **Tutor.** Ids: `handle:quote:<id>`, `bound:lower`, `bound:upper`, `intrinsic`, `chord:<K1>-<K3>`, `leg:<id>`. Secret: whether each quote is admissible.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Quotes inside and outside each bound; strike triples that break convexity or monotonicity; American items.
- **Misconceptions.** `lower-bound-is-intrinsic`, `call-above-stock`, `exercise-american-call-early`, `convexity-optional`.

#### 6.6.3 `parity-lab`: Put-call parity lab

**Composite · P1 · G2.** Two portfolios with one payoff; the derivation; conversion and reversal arbitrage; synthetic positions; the box spread; the implied forward; dividends; the American inequality. It carries the derivation part of the 1.7 exit.

- **Purpose.** Parity is not a formula to memorise; it is the observation that a call plus a bond and a put plus a share pay the same in every state, so they cost the same.
- **Serves.** 1.7.6 L13 to L15, L17; 2.3.3 L3; cross-cluster: 1.9 (a parity test in the C++ pricer's suite).
- **Uses.** `payoff-builder` (two portfolios, as two layers), `position-editor`, `cashflow-timeline` (the bond leg), `derivation-steps`, `slider` (the $S_T$ probe), `value-table` (quotes), `live-formula`, `numeric-input`.
- **Modes.** `overlay`, `derive`, `arbitrage`, `synthetic`, `box`, `forward`, `dividends`, `american`.
- **Interactions.**
  - Pointer: in overlay mode, slide $S_T$ and watch portfolio A (call plus bond paying $K$) and portfolio B (put plus share) report equal values, case by case; in derive mode, complete the derivation's lines; in arbitrage mode, read quotes, decide conversion or reversal, and build it; in synthetic mode, build a synthetic long stock; in box mode, price a box as a loan; in forward mode, read $c - p$ across strikes and fit the line whose intercept is the forward's present value and whose slope is $-e^{-rT}$.
  - Keyboard: probe slider keys; `derivation-steps` and `position-editor` keys.
- **State.** `{ mode: string; probe: number; legsA: Leg[]; legsB: Leg[]; steps?: unknown; trade?: Leg[] }`.
- **Answers and checks.** `replicates`; `expression` ($c + Ke^{-rT} = p + S_0$, and with a dividend yield $c + Ke^{-rT} = p + S_0e^{-qT}$); `predicate: is-arbitrage`; `numeric` (implied forward, implied rate, box value $(K_2 - K_1)e^{-rT}$); `ordering` (derivation steps).
- **Config.**

```ts
interface ParityLabConfig extends BaseConfig {
  mode: 'overlay' | 'derive' | 'arbitrage' | 'synthetic' | 'box' | 'forward' | 'dividends' | 'american';
  S0: number; K: number; r: number; T: number; q?: number;
  quotes?: { type: 'call' | 'put'; K: number; bid: number; ask: number }[];
  derivation?: DerivationStepsConfig;
  style: 'european' | 'american';
}
```

- **Visual.** Portfolio A's total in ink and B's as dashed `--s3`, coinciding when equal; each labelled ("A: call + bond", "B: put + share"); the probe's table shows both values per case ($S_T < K$, $S_T \ge K$); the parity gap, when quotes violate it, appears as a riskless flow at $t = 0$.
- **Motion.** Direct for the probe.
- **Show-why.** `cases` (the two cases light in turn with each leg's value), `parity-gap`.
- **Reduced motion.** Base.
- **Accessibility.** "At S_T 120: A pays 20 from the call plus 100 from the bond, 120 in all; B pays 0 from the put plus 120 from the share, 120 in all."
- **Tutor.** Ids: `portfolio:A`, `portfolio:B`, `probe`, `case:below`, `case:above`, `quote:<id>`, `step:<n>`, `line:fit`. Secret: the violation's direction and size.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Quotes violating parity in each direction (with bid-ask spreads that sometimes absorb the violation); dividend yields; box spreads; implied-forward items from several strikes with exact answers.
- **Misconceptions.** `parity-needs-model`, `parity-for-american`, `strike-undiscounted`, `synthetic-without-bond`.

#### 6.6.4 `option-chain`: Option chain

**Composite · P1 (read, parity) · G2; P2 (clean, smile) · H.** Reading and cleaning a chain: bid, ask, mid, last, volume, open interest, implied volatility and delta; stale and crossed quotes; liquidity; the parity-implied forward; a smile preview.

- **Purpose.** Real option data arrive as a table with traps: the last price can be hours old, wide quotes are not prices, and illiquid strikes distort a surface. The learner reads, then cleans.
- **Serves.** 1.7.6 L4, L5; 1.7.8 L16; 2.3.3 L1, L3.
- **Uses.** `value-table` (`chain` preset), `region-select` (cell selection), `plot-2d` (mini smile; $c - p$ against $K$), `marks`, `numeric-input`, `choice`.
- **Modes.** `read`, `clean`, `parity`, `smile`.
- **Interactions.**
  - Pointer: tap cells to answer; filter strikes and expiries; flag quotes to discard; in parity mode, tap strikes to include in the line fit.
  - Keyboard: grid navigation; Space selects; F flags; E switches expiry.
- **State.** `{ mode: string; expiry: string; selected: string[]; flagged: string[]; fitStrikes?: number[] }`.
- **Answers and checks.** `numeric` (mid, spread, forward, implied rate); `set` (bad quotes; the most liquid strike); `choice`.
- **Config.**

```ts
interface OptionChainConfig extends BaseConfig {
  mode: 'read' | 'clean' | 'parity' | 'smile';
  chain: { generator: 'market-gen/chain'; seed: number; expiries: number; strikes: number;
           defects: ('stale-last' | 'crossed' | 'wide' | 'zero-bid' | 'parity-break')[] } | ChainData;
  columns: ('bid' | 'ask' | 'mid' | 'last' | 'volume' | 'oi' | 'iv' | 'delta')[];
}
```

- **Visual.** Calls left, a sticky strike column in the centre, puts right; in-the-money cells shaded `--bg-sunken` and labelled "ITM" for screen readers; flagged cells with a cross icon and a word ("stale"); the parity plot as ink dots with the fitted line in `--s3`.
- **Motion.** None.
- **Show-why.** `stale-last` (the last trade's time appears beside its price), `crossed`, `parity-line`.
- **Reduced motion.** Not applicable.
- **Accessibility.** The chain is a grid; each cell reads "Call, strike 105, bid 2.10, ask 2.30, last 1.85 at 10:02."
- **Tutor.** Ids: `cell:<K>:<call|put>:<field>`, `strike:<K>`, `expiry:<id>`, `plot:parity`, `line:fit`. Secret: the planted defects.
- **Performance.** Virtualised above 60 strikes.
- **Artifact and web.** No difference.
- **Generators.** Synthetic chains from `market-gen` with seeded defects; forward and rate items.
- **Misconceptions.** `last-is-price`, `wide-spread-fine`, `iv-same-all-strikes`.

### 6.7 Black-Scholes and the Greeks

#### 6.7.1 `bs-explorer`: Black-Scholes explorer

**Composite · P1 · G3.** The Black-Scholes-Merton formula as a picture: price curves against the stock at several expiries; the decomposition into two digital claims; $N(d_2)$ as a probability; the effect of each input; the at-the-money shortcut.

- **Purpose.** Read the formula rather than memorise it: $c = S_0 e^{-qT} N(d_1) - K e^{-rT} N(d_2)$ is an asset-or-nothing claim minus a cash-or-nothing claim; $N(d_2)$ is the risk-neutral chance of exercise; the real drift does not appear.
- **Serves.** 1.7.8 L2 to L7, L17; 2.3.3 L9; 3.3.1 L5 (the at-the-money deck).
- **Uses.** `plot-2d` (price against $S$; density panel), `slider` ($S$, $K$, $T$, $\sigma$, $r$, $q$; log scales where useful), `marks` (curves, signed fill, density, tail), `live-formula` ($d_1$ and $d_2$ live), `sketch-pad` (predict a curve), `numeric-input`, `choice`; links to `dist-explorer` (lognormal) and `binomial-tree` (convergence).
- **Modes.** `slices`, `decompose`, `density`, `inputs`, `atm`, `put`.
- **Interactions.**
  - Pointer: sliders; sweep $T$ towards zero and watch the curve collapse onto the payoff; in decompose mode, read the two component curves and their difference; in density mode, read the shaded tail beyond $K$; in inputs mode, fill a sign table (does the call rise or fall with each input?) before testing each slider; in atm mode, estimate with $0.4\,\sigma\sqrt{T}\,S$ and compare.
  - Keyboard: slider keys; T toggles the table view.
- **State.** `{ mode: string; S: number; K: number; T: number; sigma: number; r: number; q: number; slices: number[]; signTable?: Record<string, -1 | 0 | 1>; sketch?: unknown }`.
- **Answers and checks.** `numeric` (price, $N(d_2)$, each component); `choice` (sign-table cells); `curve` (a predicted price curve); `point`.
- **Config.**

```ts
interface BsExplorerConfig extends BaseConfig {
  mode: 'slices' | 'decompose' | 'density' | 'inputs' | 'atm' | 'put';
  type: 'call' | 'put';
  params: { S: number; K: number; T: number; sigma: number; r: number; q?: number };
  editable: ('S' | 'K' | 'T' | 'sigma' | 'r' | 'q')[];
  slices?: number[];                            // times to expiry drawn together
  predictFirst?: boolean;
}
```

- **Visual.** The payoff in ink; price curves in `--s3`, older slices fading; the lower bound dashed ink; in decompose mode, the asset part in `--s6` and the cash part in `--s2` with their difference shaded; the density in `--s3` with the tail beyond $K$ patterned and labelled $N(d_2)$; the formula with live numbers.
- **Motion.** Direct.
- **Show-why.** `collapse-to-payoff`, `vol-raises-both` (the volatility slider lifts both the call and the put), `tail-area`.
- **Reduced motion.** Base.
- **Accessibility.** "S 100, K 100, T 0.5 years, volatility 20%, r 3% continuous: call 6.37, put 4.88; d1 0.177, d2 0.035." Table by $S$.
- **Tutor.** Ids: `slider:<param>`, `curve:T=<t>`, `component:asset`, `component:cash`, `density`, `tail`, `formula:d1`, `formula:d2`, `table:signs`.
- **Performance.** Section 2.10.
- **Artifact and web.** No difference.
- **Generators.** Parameter sets with answers from `finance-core`; sign tables; at-the-money estimates.
- **Misconceptions.** `vol-lowers-put`, `n-d1-is-probability`, `price-depends-on-mu`, `theta-always-negative` (a deep in-the-money European put can gain value as time passes), `atm-approx-uses-variance`.

#### 6.7.2 `greeks-lab`: Greeks lab

**Composite · P1 · G3 (surface mode P2 · H).** Delta, gamma, theta, vega and rho as slopes and curvatures of the price; how they change with the stock price and time; position Greeks; delta-neutral hedging.

- **Purpose.** Each Greek is a shape on the price curve before it is a formula: delta is the tangent's slope, gamma its rate of turning, theta the gap between today's and tomorrow's curves.
- **Serves.** 1.7.8 L8 to L12; 2.3.3 L7 (surface).
- **Uses.** `plot-2d` (price curve with tangent; Greek against $S$ in a linked panel), `drag-point` ($S$ on the curve), `slider` ($T$, $\sigma$), `position-editor` (portfolio mode), `plot-3d` (surface mode), `marks`, `value-table` (Greeks by leg), `live-formula`, `numeric-input`, `choice`.
- **Modes.** `delta`, `gamma`, `theta`, `vega`, `rho`, `portfolio`, `surface`.
- **Interactions.**
  - Pointer: drag $S$ along the price curve; the tangent and the lower panel's cursor follow; in gamma mode an osculating parabola shows curvature; drag $T$ towards expiry and watch the gamma spike sharpen at the strike; in portfolio mode, read each leg's Greeks and the total, then add stock until delta is zero.
  - Keyboard: the $S$ handle moves along the curve; G cycles the Greek shown.
- **State.** `{ mode: string; S: number; T: number; sigma: number; legs?: Leg[]; greek: string }`.
- **Answers and checks.** `numeric` (a Greek at a price, with units); `point` (where gamma peaks); `choice` (signs, where a Greek is largest); `predicate: delta-neutral`.
- **Config.**

```ts
interface GreeksLabConfig extends BaseConfig {
  mode: 'delta' | 'gamma' | 'theta' | 'vega' | 'rho' | 'portfolio' | 'surface';
  base: { K: number; r: number; q?: number; sigma: number; T: number; type: 'call' | 'put' };
  Srange: [number, number];
  tSlices?: number[];
  editor?: PositionEditorConfig;
  units: { theta: 'per-day' | 'per-year'; vega: 'per-point' | 'per-unit' };
}
```

- **Visual.** The price curve in `--s3`, the tangent in `--s2`, the $S$ handle in `--manip`; the lower panel draws the Greek against $S$ for several expiries (ink, fading with time); unit chips on every number; in surface mode, the Greek over $(S, T)$ shaded with the sequential ramp.
- **Motion.** Direct.
- **Show-why.** `tangent-is-delta`, `gamma-spike`, `theta-gamma-mirror` (for an at-the-money option, the theta panel mirrors the gamma panel).
- **Reduced motion.** Base.
- **Accessibility.** "At S 100: delta 0.570 per share, gamma 0.028 per unit, theta −0.019 per day, vega 0.28 per volatility point." Table of Greeks by $S$.
- **Tutor.** Ids: `handle:S`, `line:tangent`, `curve:price`, `curve:<greek>:T=<t>`, `table:portfolio`, `cell:<leg>:<greek>`.
- **Performance.** Closed forms; the surface on a 40 by 40 grid.
- **Artifact and web.** No difference.
- **Generators.** Positions with given Greek signs; delta-neutral hedges with integer share counts; where-is-it-largest items.
- **Misconceptions.** `delta-is-probability`, `gamma-highest-deep-itm`, `long-option-positive-theta`, `vega-highest-near-expiry`, `delta-neutral-is-riskless`.

#### 6.7.3 `pnl-attribution`: P&L attribution

**Composite · P1 · G3.** A position's P&L explained by its Greeks: $\Delta V \approx \Delta\,dS + \frac{1}{2}\Gamma\,dS^2 + \Theta\,dt + \nu\,d\sigma$, with the residual; the delta-hedged daily P&L $\approx \frac{1}{2}\Gamma S^2(\sigma_{\text{realised}}^2 - \sigma_{\text{implied}}^2)\,dt$; the break-even move.

- **Purpose.** The desk's daily question, "why did we make or lose money?", answered with a waterfall. It is also the bridge from Greeks to hedging.
- **Serves.** 1.7.8 L13, L14; 3.3.5 (options-desk interview questions).
- **Uses.** `marks` (`waterfall`), `plot-2d` (path view: cumulative gamma P&L against theta), `slider` ($dS$, $d\sigma$, $dt$), `position-editor` (the position), `value-table`, `numeric-input`, `choice`.
- **Modes.** `one-day`, `path`, `breakeven`.
- **Interactions.**
  - Pointer: set a move with the sliders; fill each bar's value; compare the sum with full revaluation; in path mode, replay a path and watch daily gamma gains against theta; in break-even mode, find the move at which a long-gamma position breaks even, $\lvert dS \rvert = \sigma S\sqrt{dt}$.
  - Keyboard: slider keys; bars are focusable fields.
- **State.** `{ mode: string; legs: Leg[]; dS: number; dSigma: number; dt: number; entries: Record<string, number> }`.
- **Answers and checks.** `numeric` per term through `multi`; `choice` (signs); `numeric` (break-even move).
- **Config.**

```ts
interface PnlAttributionConfig extends BaseConfig {
  mode: 'one-day' | 'path' | 'breakeven';
  position: Leg[];
  market: { S: number; sigma: number; r: number; q?: number };
  move?: { dS: number; dSigma: number; dtDays: number };
  path?: { generator: 'market-gen/path'; seed: number; days: number; sigmaRealised: number };
}
```

- **Visual.** A waterfall from yesterday's value to today's (delta, gamma, theta, vega bars as signed fills, the residual hatched); full revaluation as a dashed ink marker; in path mode, cumulative gamma P&L and cumulative theta as two ink lines with labels.
- **Motion.** Direct.
- **Show-why.** `quadratic-term` (doubling $dS$ quadruples the gamma bar), `residual-grows-with-move`.
- **Reduced motion.** Base.
- **Accessibility.** "Move +2.00: delta +1.14, gamma +0.06, theta −0.02, vega 0; explained +1.18; actual +1.19; residual +0.01."
- **Tutor.** Ids: `bar:delta`, `bar:gamma`, `bar:theta`, `bar:vega`, `bar:residual`, `marker:full`, `slider:dS`, `slider:dSigma`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Positions and moves with answers from `finance-core`.
- **Misconceptions.** `gamma-term-linear`, `theta-negligible`, `attribution-is-exact`.

#### 6.7.4 `iv-solver`: Implied volatility solver

**Composite · P1 (drag, bounds, smile) · G3; P2 (algorithm) · H.** Inverting the price formula: by hand with a slider, by Newton's method with vega as the slope, by bisection when Newton fails; prices with no solution; the smile across strikes.

- **Purpose.** Implied volatility is the one number the market quotes options in. The learner first finds it by dragging, then learns why the textbook algorithm needs a safeguard.
- **Serves.** 1.7.8 L15, L16; 2.3.3 L2.
- **Uses.** `plot-2d` (model price against $\sigma$ with the market price line; the smile panel), `drag-point` ($\sigma$ on the curve), `stepper` (iterations), `token-tray` (order the algorithm's steps), `live-formula`, `numeric-input`, `choice`; links to `code-cell` for the 2.3.3 drill.
- **Modes.** `drag`, `algorithm`, `bounds`, `smile`.
- **Interactions.**
  - Pointer: drag $\sigma$ until the curve meets the market line; in algorithm mode, press Step to draw Newton's tangent and the next iterate, or switch to bisection and watch the bracket halve; in bounds mode, enter a price below intrinsic value and see that the line never meets the curve; in smile mode, solve five strikes and plot them.
  - Keyboard: the $\sigma$ handle steps by 0.1 volatility points (Shift by 1); N steps Newton; B steps bisection.
- **State.** `{ mode: string; sigma: number; market: number; iterates: number[]; bracket?: [number, number]; solved: Record<string, number> }`.
- **Answers and checks.** `numeric` (implied volatility); `ordering` (algorithm steps); `choice` (why there is no solution); `point`.
- **Formulas shown live.** $\sigma_{n+1} = \sigma_n - \frac{C(\sigma_n) - C_{\text{mkt}}}{\nu(\sigma_n)}$; bisection keeps $C(\sigma_{\text{lo}}) < C_{\text{mkt}} < C(\sigma_{\text{hi}})$.
- **Config.**

```ts
interface IvSolverConfig extends BaseConfig {
  mode: 'drag' | 'algorithm' | 'bounds' | 'smile';
  option: { type: 'call' | 'put'; S: number; K: number; T: number; r: number; q?: number };
  market: number | { strikes: number[]; prices: number[] };
  sigmaRange: [number, number];
  start?: number;                               // initial guess for Newton
}
```

- **Visual.** The price-against-volatility curve in `--s3` (increasing); the market price as dashed ink; the $\sigma$ handle in `--manip`; Newton tangents in `--s2` with numbered iterate dots; the bisection bracket as an `--s6` band.
- **Motion.** Each Step draws its tangent over 300ms (a consequence of the learner's press).
- **Show-why.** `newton-overshoot` (a far out-of-the-money option with tiny vega sends the iterate off the chart), `below-intrinsic`.
- **Reduced motion.** Tangents appear at once.
- **Accessibility.** "Market 4.20; at volatility 22.0% the model gives 4.05; increase volatility." Iterates as a table.
- **Tutor.** Ids: `handle:sigma`, `curve:price`, `line:market`, `iterate:<n>`, `bracket`, `smile:<K>`. Secret: the true volatility used to generate the quote.
- **Performance.** Closed-form evaluations only.
- **Artifact and web.** No difference; the code drill follows section 2.11.
- **Generators.** Quotes generated from a chosen volatility, so the implied volatility is exact; tiny-vega items; prices outside the bounds.
- **Misconceptions.** `iv-is-historical`, `iv-always-exists`, `newton-always-converges`.

### 6.8 Market microstructure

#### 6.8.1 `tape-lab`: Tape lab

**Composite · P1 · G3.** Reading time and sales against the quotes: classifying trades (quote rule, tick rule, Lee-Ready); quoted, effective and realised spreads; price impact; the bid-ask bounce and Roll's estimator.

- **Purpose.** The spread a trader really pays is measured from trades, and trades bounce between bid and ask; Roll turns that bounce into a spread estimate from prices alone.
- **Serves.** 1.7.9 L3 to L5; 2.3.4 L1 (trade messages).
- **Uses.** `plot-2d` with `marks` (`quote-band`, `trade-glyphs`), `value-table` (tape: time, price, size, bid, ask), `region-select` (tag trades), `plot-2d` (scatter of $\Delta p_t$ against $\Delta p_{t-1}$), `numeric-input`, `choice`.
- **Modes.** `classify`, `spreads`, `roll`.
- **Interactions.**
  - Pointer: tap each trade and tag it buyer- or seller-initiated; fill spread columns for selected trades; in Roll mode, read the scatter's covariance and compute the estimate.
  - Keyboard: rows as a grid; B and S tag the focused trade; Enter confirms.
- **State.** `{ mode: string; tags: Record<string, 'B' | 'S'>; entries: Record<string, number> }`.
- **Answers and checks.** `set` (buyer-initiated trades); `numeric` (spreads, impact, Roll estimate); `choice`.
- **Formulas shown live.** With $D = +1$ for a buy and $-1$ for a sell and mid $m$: effective spread $2D(p - m_t)$; realised spread $2D(p - m_{t+\Delta})$; price impact $2D(m_{t+\Delta} - m_t)$; Roll $s = 2\sqrt{-\mathrm{Cov}(\Delta p_t, \Delta p_{t-1})}$.
- **Config.**

```ts
interface TapeLabConfig extends BaseConfig {
  mode: 'classify' | 'spreads' | 'roll';
  tape: { generator: 'market-gen/tape'; seed: number; n: number; spread: number; informed: number } | TapeData;
  rule: 'quote' | 'tick' | 'lee-ready';
  horizon?: number;                              // seconds for realised spread
}
```

- **Visual.** The quote band with the mid dashed; trades as triangles (up for buys, down for sells, once tagged; circles before); tagged trades outlined `--manip`; the scatter in ink with the fitted line in `--s3`.
- **Motion.** None beyond tagging.
- **Show-why.** `bounce` (trades alternate between the band's edges while the mid stays flat), `midpoint-trade` (a trade at the mid needs the tick rule).
- **Reduced motion.** Not applicable.
- **Accessibility.** The tape is the table view; each row reads "10:00:03, 100.02, 300 shares; bid 100.00, ask 100.02."
- **Tutor.** Ids: `trade:<n>`, `row:<n>`, `band`, `scatter`, `line:roll`. Secret: the true initiator of every trade.
- **Performance.** Tapes up to 2,000 trades.
- **Artifact and web.** No difference.
- **Generators.** Tapes with known initiators and planted spreads; Roll series with independent bounce; impact items.
- **Misconceptions.** `price-up-means-buyer`, `effective-equals-quoted`, `roll-works-with-trend`.

#### 6.8.2 `adverse-selection`: Adverse selection (Glosten-Milgrom)

**Composite · P1 · G3.** The dealer's zero-profit bid and ask when some traders know the value; Bayesian updating after each trade; the spread against the informed fraction; price discovery.

- **Purpose.** The spread exists even for a dealer with no costs, because every trade might come from someone who knows more. This is the idea behind every market-making game in 3.3.
- **Serves.** 1.7.9 L7, L8; 3.3.4 L4 (what a trade tells you); cross-cluster: 1.5 Bayes' rule in a market setting.
- **Uses.** `number-line` (value axis with $V_L$, $V_H$, and bid and ask handles), `slider` ($\mu$, prior $\pi$), `stepper` (trades in sequence), `plot-2d` with `marks` (belief path and `quote-band` over trades), `value-table` (Bayes table: trade, $P(V_H)$, bid, ask), `live-formula`, `numeric-input`.
- **Modes.** `single`, `sequence`, `compare`.
- **Interactions.**
  - Pointer: drag the bid and ask to where the dealer breaks even; read the expected profit per side after committing; in sequence mode, after each trade re-quote; the true value is revealed at the end; in compare mode, vary $\mu$ and watch the spread scale.
  - Keyboard: handles step by one tick; N steps to the next trade.
- **State.** `{ mode: string; bid: number; ask: number; pi: number; trade: number; history: { side: 'buy' | 'sell'; bid: number; ask: number; pi: number }[] }`.
- **Answers and checks.** `numeric` (bid and ask, exact rationals); `quote` (contains the conditional expectations); `curve` (a predicted belief path).
- **Formulas shown live.** A trader is informed with probability $\mu$ (buys if $V = V_H$, sells if $V = V_L$) and otherwise buys or sells with probability $\frac{1}{2}$. $\text{ask} = E[V \mid \text{buy}]$, $\text{bid} = E[V \mid \text{sell}]$. With $\pi = \frac{1}{2}$: $\text{ask} = V_L + (V_H - V_L)\frac{1 + \mu}{2}$ and the spread is $\mu(V_H - V_L)$.
- **Config.**

```ts
interface AdverseSelectionConfig extends BaseConfig {
  mode: 'single' | 'sequence' | 'compare';
  VL: number; VH: number; prior: Entry; mu: Entry;
  trades?: ('buy' | 'sell')[] | { seed: number; n: number; trueV: 'L' | 'H' };
  tick: number;
}
```

- **Visual.** The value axis with $V_L$ and $V_H$ as ink ticks; the belief $\pi$ as a bar; bid and ask handles in `--manip`; $E[V]$ as an ink tick; after grading, the break-even quotes dashed ink; in sequence mode, the quote band narrowing over trades.
- **Motion.** Direct; the belief bar moves after each trade over 300ms.
- **Show-why.** `lose-to-informed` (with quotes at the prior mean, every informed trade's loss is drawn), `spread-equals-mu-range`.
- **Reduced motion.** Base.
- **Accessibility.** "Values 90 or 110, belief 0.50, informed share 20%: break-even ask 102, bid 98."
- **Tutor.** Ids: `handle:bid`, `handle:ask`, `slider:mu`, `bar:belief`, `trade:<n>`, `row:<n>`. Secret: the true value.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** $(V_L, V_H, \pi, \mu)$ with rational answers; trade sequences.
- **Misconceptions.** `spread-is-greed`, `quote-at-prior-mean`, `noise-traders-lose-nothing`.

#### 6.8.3 `dealer-sim`: Dealer simulator

**Composite · P1 · G3 (Avellaneda-Stoikov mode P2 · H).** A market maker's session: earn the spread from noise flow, pay adverse selection to informed flow, manage inventory by skewing; decompose P&L; the Avellaneda-Stoikov reservation price and spread.

- **Purpose.** Turn the two spread theories into one running business with inventory risk, and prepare the 3.1 replication of Avellaneda and Stoikov.
- **Serves.** 1.7.9 L6, L11; 3.3.4 L5 (inventory); cross-cluster: 3.1 (Avellaneda and Stoikov, 2008).
- **Uses.** `plot-2d` (mid with `quote-band`; inventory; P&L), `slider` (half-spread, skew per unit of inventory, $\gamma$, $k$), `quote-entry` (manual mode), `price-ladder` (optional view), `sim-runner` (`order-flow`), `marks` (`waterfall` for decomposition), `value-table` (`blotter`), `numeric-input`, `choice`.
- **Modes.** `inventory`, `adverse`, `decompose`, `manual`, `avellaneda-stoikov`.
- **Interactions.**
  - Pointer: set the quoting policy with sliders and Run a seeded session; watch inventory and P&L; open the decomposition; in manual mode, quote live at slow replay speed; in the Avellaneda-Stoikov mode, compare the reservation price with the mid as inventory grows.
  - Keyboard: slider keys; R runs; replay keys.
- **State.** `{ mode: string; policy: { half: number; skew: number; gamma?: number; k?: number }; seed: number; log: Event[] }`.
- **Answers and checks.** `numeric` (decomposition terms on a fixed replay, which are deterministic computations); `choice` (which policy controls inventory; which way to skew); `quote` (manual quotes against the posterior when the replay is informative). Realised P&L across seeds is shown, never graded (decision 6).
- **Formulas shown live** (Avellaneda-Stoikov mode). Reservation price $r = s - q\gamma\sigma^2(T - t)$; total spread $\delta^a + \delta^b = \gamma\sigma^2(T - t) + \frac{2}{\gamma}\ln\left(1 + \frac{\gamma}{k}\right)$.
- **Config.**

```ts
interface DealerSimConfig extends BaseConfig {
  mode: 'inventory' | 'adverse' | 'decompose' | 'manual' | 'avellaneda-stoikov';
  flow: { seed: number; noiseRate: number; informedShare: number; sigma: number; durationS: number };
  policy: { half: [number, number]; skew: [number, number]; gamma?: [number, number]; k?: number };
  tick: number;
  showLadder: boolean;
}
```

- **Visual.** The mid in ink with the learner's quote band; fills as triangles; inventory and P&L in their own panels in ink, P&L with a signed fill; the decomposition as a waterfall (spread captured, adverse selection, inventory mark-to-market, fees).
- **Motion.** Replay as content; at most 8×.
- **Show-why.** `inventory-drift` (without skew, inventory wanders like a random walk), `adverse-cost` (informed fills are drawn with the mid's later move).
- **Reduced motion.** The replay steps without interpolation.
- **Accessibility.** "Session 10 minutes: 214 fills; spread captured +312; adverse selection −198; inventory −41; fees −22; net +51." The blotter is the table view.
- **Tutor.** Ids: `slider:<param>`, `panel:mid`, `panel:inventory`, `panel:pnl`, `bar:<component>`, `fill:<n>`. Secret: the informed share and the value path.
- **Performance.** Sessions of up to 5,000 events in a worker; panels decimated per pixel column.
- **Artifact and web.** No difference.
- **Generators.** Flow parameters; fixed replays for decomposition arithmetic; skew-direction items.
- **Misconceptions.** `wider-always-better`, `inventory-is-free`, `skew-wrong-way`.

#### 6.8.4 `execution-lab`: Execution lab

**Composite · P1 · G3 (frontier mode P2 · H).** The cost of trading size: spread, temporary and permanent impact, the square-root law, splitting over time, TWAP and VWAP schedules, implementation shortfall, timing risk; the Almgren-Chriss frontier.

- **Purpose.** Market against limit, scaled up: the faster you trade, the more you pay in impact; the slower, the more the price can wander.
- **Serves.** 1.7.9 L9, L10; 2.3.1 L5 (cost models for the backtester); 2.3.2 L11 (capacity).
- **Uses.** `plot-2d` (cost against size; schedule bars over the day with the volume curve; price path), `mass-editor` (allocation across time buckets, summing to 100%), `slider` (order size as a share of daily volume; risk aversion $\lambda$), `marks` (`waterfall`), `sim-runner` (price paths for timing risk), `numeric-input`, `choice`, `drag-point` (a point on the frontier).
- **Modes.** `impact`, `schedule`, `shortfall`, `children`, `frontier`.
- **Interactions.**
  - Pointer: drag the order size and read the cost in basis points; reshape the schedule with the mass editor; run price paths to see timing risk; in children mode, choose market or limit for each child order; in frontier mode, slide $\lambda$ along the expected-cost against risk curve.
  - Keyboard: slider and mass-editor keys; R runs.
- **State.** `{ mode: string; size: number; schedule: number[]; lambda?: number; childTypes?: ('market' | 'limit')[] }`.
- **Answers and checks.** `numeric` (cost in basis points, shortfall); `choice` (schedule for a given urgency); `point` (a frontier choice).
- **Formulas shown live.** Square-root rule: impact $\approx Y\sigma\sqrt{Q/V}$ with $Y$ of order 1 [sourced: empirical studies of metaorders, recalled]; implementation shortfall $= $ side $\times (\bar{p}_{\text{exec}} - p_{\text{arrival}}) \times Q$ plus fees plus the opportunity cost of unfilled shares.
- **Config.**

```ts
interface ExecutionLabConfig extends BaseConfig {
  mode: 'impact' | 'schedule' | 'shortfall' | 'children' | 'frontier';
  market: { price: number; sigmaDaily: number; adv: number; spread: number; volumeCurve: number[] };
  order: { side: 'buy' | 'sell'; qty: number; horizonBuckets: number };
  impact: { model: 'sqrt' | 'linear'; Y: number; permanentShare: number };
  seed?: number;
}
```

- **Visual.** The U-shaped volume curve outlined in ink; schedule bars in `--manip`; the price path in ink with the arrival price dashed; the cost waterfall (spread, impact, timing, fees).
- **Motion.** Direct; runs draw paths over 600ms.
- **Show-why.** `sqrt-not-linear`, `rush-costs-impact`, `slow-costs-risk`.
- **Reduced motion.** Paths appear at once.
- **Accessibility.** "Buying 5% of daily volume over 1 hour: expected cost 18 bp (spread 2, impact 16)."
- **Tutor.** Ids: `slider:size`, `bucket:<k>`, `curve:volume`, `line:arrival`, `bar:<cost>`, `frontier`, `handle:lambda`.
- **Performance.** Path runs in the worker.
- **Artifact and web.** No difference.
- **Generators.** Orders and market parameters; shortfall arithmetic; schedule-choice items.
- **Misconceptions.** `impact-linear`, `beat-vwap-means-good`, `splitting-always-cheaper`.

---

## 7. Project composites (2.3)

These widgets teach and rehearse the components of the five projects on synthetic data (decision 7). The learner's real project runs on their own machine; `setup-checklist` (project mode) and `results-note` connect the two.

### 7.1 `backtest-lab`: Backtest lab

**Composite · P2 · H.** An event-driven backtest the learner steps through, with biases that can be switched on and seen: look-ahead, survivorship, missing costs, wrong fill timing; sizing; held-out periods and walk-forward; a bug hunt; the engine's architecture.

- **Purpose.** Most backtests that look good are wrong in one of a few known ways. The learner builds the habit of asking "what could the strategy see at this moment?" by watching the event loop and by breaking it on purpose.
- **Serves.** 2.3.0 L4; 2.3.1 L1 to L6, L9, L11; 2.3.2 L11; 2.3.5 L7; cross-cluster: 2.1 time-ordered validation, 3.1 replications.
- **Uses.** `stepper`, `plot-2d` (price with signals; equity; drawdown; linked x axes), `marks` (`event-rug` for fills, `signed-fill`), `region-select` (in-sample and held-out brackets; walk-forward windows), `slider` (cost in basis points, volatility target), `value-table` (data window; `blotter`), `code-surface` (read-addressable code in hunt mode), `node-link` and `card-sort` (architecture mode), `live-formula`, `numeric-input`, `choice`; services `backtest-core`, `price-series`, `market-gen` (universes with delistings).
- **Modes.** `step`, `timing`, `bias`, `costs`, `sizing`, `holdout`, `hunt`, `architecture`.
- **Interactions.**
  - Pointer: in step mode, press Step and a bar arrives: the data window shows only the past (future rows greyed with a lock icon), then the signal, target position, orders, fills at the next open, and the portfolio update; in bias mode, predict the effect of a toggle (look-ahead, today's universe, costs off, fill at the signal's close) before the biased equity curve appears; in costs mode, sweep the cost and read the break-even; in holdout mode, drag the brackets, and the held-out region stays locked until "Final test" is pressed, once; in hunt mode, tap the line that causes a too-good equity curve; in architecture mode, connect components and label what crosses each boundary.
  - Keyboard: N steps a bar; stepper keys; Space toggles a bias; bracket handles step by a month; code lines are selectable with Up, Down and Space.
- **State.** `{ mode: string; step: number; toggles: Record<string, boolean>; cost: number; sizing: 'fixed' | 'vol-target'; brackets?: [number, number][]; holdoutRevealed: boolean; flaggedLines: number[]; graph?: { edges: [string, string, string][] } }`.
- **Answers and checks.** `ordering` (event-loop steps); `choice` (predicted effects); `numeric` (metrics; break-even cost); `set` (bug lines; delisted names); `mapping` (architecture); `predicate: no-lookahead` (for the companion code drill).
- **Config.**

```ts
interface BacktestLabConfig extends BaseConfig {
  mode: 'step' | 'timing' | 'bias' | 'costs' | 'sizing' | 'holdout' | 'hunt' | 'architecture';
  data: { generator: 'price-series' | 'market-gen/universe'; seed: number; assets: number; days: number; delistings?: number };
  strategy: { kind: 'ma-cross' | 'momentum' | 'mean-reversion' | 'buy-hold'; params: Record<string, number> };
  fill: 'next-open' | 'close' | 'close-with-slippage';
  costs: { bps: number; halfSpread?: boolean; impact?: 'none' | 'sqrt' };
  biases?: ('look-ahead' | 'survivorship' | 'no-costs' | 'same-bar-fill')[];
  holdout?: { from: string; to: string };
  code?: { source: string; bugLines: number[] };   // hunt mode; bugLines stay in secret()
}
```

- **Visual.** Price in ink with signal markers on an `event-rug`; equity in ink, the benchmark dashed and labelled; a biased run in `--s2` labelled "with look-ahead"; the held-out region hatched with a lock icon until revealed; the data window's future rows greyed with "not yet known".
- **Motion.** Step animations are consequences (a row moves from "future" to "known" over 200ms); full runs draw over 600ms.
- **Show-why.** `peek` (the biased run highlights the bar where it used the next day's price), `graveyard` (delisted names reappear in the universe), `cost-drag` (the equity curve sinks as costs rise, turnover annotated).
- **Reduced motion.** Steps cut; runs appear at once.
- **Accessibility.** "Bar 2023-05-04: signal long; target 100 shares; order filled at the next open, 101.20; equity 10,412." Metrics table; the data window is a table.
- **Tutor.** Ids: `step:<n>`, `window`, `row:<date>`, `toggle:<bias>`, `curve:equity`, `curve:biased`, `bracket:<id>`, `line:<n>`, `metric:<name>`, `component:<id>`. Secret: the planted bias and the bug lines.
- **Performance.** Ten years of daily bars for 50 assets (about 126,000 bars) run in under 100ms in a worker; step mode is trivial.
- **Artifact and web.** No difference; the companion code drills follow section 2.11.
- **Generators.** Strategies with planted bugs (a negative shift, today's universe, fills at the signal's close, adjusted prices misused around dividends, costs omitted); cost and metric items; held-out designs.
- **Misconceptions.** `high-sharpe-is-skill`, `same-bar-fill`, `survivors-only`, `costs-negligible`, `peek-at-holdout`.

### 7.2 `sharpe-lab`: Sharpe lab

**Composite · P2 · H.** Performance metrics and their noise: the Sharpe ratio and its annualisation, its standard error and $t$-statistic, Sortino, Calmar, the distribution of maximum drawdown, the best of many null strategies, and the deflated Sharpe ratio.

- **Purpose.** A Sharpe ratio is an estimate with a wide error bar. Three years of data cannot tell 0.5 from 1.0, and the best of 200 tries looks like skill.
- **Serves.** 2.3.1 L7, L8, L10; 2.3.2 L6, L11; cross-cluster: 3.1 (Harvey, Liu and Zhu).
- **Uses.** `sim-runner` (`null-strategy`, `gbm`), `plot-2d` (histogram of null Sharpe ratios; equity fan; years needed against true Sharpe), `marks`, `slider` (true Sharpe, years, number of trials, autocorrelation), `value-table`, `live-formula`, `numeric-input`, `choice`; links to `drawdown-lab` and `multiple-testing`.
- **Modes.** `compute`, `annualise`, `null`, `years`, `deflated`, `drawdown`.
- **Interactions.**
  - Pointer: compute metrics from a fixed returns table; choose the annualisation factor for daily, weekly and monthly data; run 1,000 strategies with true Sharpe 0 over $T$ years and read the 95th percentile; slide the true Sharpe and read the years needed for $t = 2$; slide the number of trials and watch the deflation threshold rise; read the drawdown distribution for a given Sharpe.
  - Keyboard: slider keys; R runs.
- **State.** `{ mode: string; trueSR: number; years: number; trials: number; rho1?: number; seed: number }`.
- **Answers and checks.** `numeric` (Sharpe, standard error, $t$, threshold, deflated Sharpe probability, Calmar); `choice`.
- **Formulas shown live.** $\mathrm{SR}_{\text{ann}} = \frac{\bar{r}}{s}\sqrt{k}$ with $k = 252$, 52 or 12; for independent returns, $\mathrm{SE}(\widehat{\mathrm{SR}}) \approx \sqrt{(1 + \frac{1}{2}\mathrm{SR}^2)/T}$ per period (Lo, 2002); $t \approx \mathrm{SR}_{\text{ann}}\sqrt{\text{years}}$; the expected maximum of $N$ independent null Sharpe ratios $\approx \sqrt{V}\left[(1 - \gamma)\Phi^{-1}(1 - \tfrac{1}{N}) + \gamma\Phi^{-1}(1 - \tfrac{1}{Ne})\right]$ with $\gamma \approx 0.5772$ (Bailey and López de Prado).
- **Config.**

```ts
interface SharpeLabConfig extends BaseConfig {
  mode: 'compute' | 'annualise' | 'null' | 'years' | 'deflated' | 'drawdown';
  returns?: number[] | { generator: 'market-gen/returns'; seed: number; n: number; sr: number; freq: 'daily' | 'monthly' };
  sim?: { seed: number; strategies: number; years: [number, number]; trials: [number, number] };
  autocorrelation?: number;
}
```

- **Visual.** The null histogram in `--s2` with the learner's Sharpe as a `--manip` marker and the 95th percentile dashed ink; equity fans in ink at 15%; the years-needed curve in `--s3`.
- **Motion.** Histograms fill as runs arrive (content).
- **Show-why.** `null-spread`, `best-of-n`, `wrong-root` (annualising monthly data with $\sqrt{252}$).
- **Reduced motion.** Final histograms at once.
- **Accessibility.** "1,000 null strategies over 3 years: 95th percentile Sharpe 0.95; your strategy 0.90." Histogram table view.
- **Tutor.** Ids: `hist:null`, `marker:learner`, `line:p95`, `slider:<param>`, `curve:years`.
- **Performance.** Null runs are vectorised in the worker ($10^3$ strategies by 756 days in under 100ms [estimate]).
- **Artifact and web.** No difference.
- **Generators.** Returns with planted mean and volatility; annualisation items; trial counts; deflation items.
- **Misconceptions.** `annualise-wrong-root`, `sharpe-is-precise`, `best-of-n-is-skill`, `autocorrelation-ignored`.

### 7.3 `signal-lab`: Signal lab

**Composite · P2 · H.** Cross-sectional signal research: build a signal from return windows, normalise and neutralise it, measure its information coefficient on each date and over time, its decay, its quantile spreads, its turnover and its Sharpe ratio after costs.

- **Purpose.** Research is measuring a weak relationship across many stocks: an IC of 0.03 is invisible on any one date and valuable across hundreds of names and years. Turnover decides whether it survives costs.
- **Serves.** 2.3.2 L1 to L11; cross-cluster: 3.1 (Jegadeesh and Titman; Fama and French).
- **Uses.** `plot-2d` (one date's scatter of signal rank against forward return; IC series; decay bars; quantile bars; turnover), `marks` (heat cells for the universe, bars, bands), `slider` (lookback, skip, horizon, smoothing half-life, cost, universe size), `region-select` (date brush), `token-tray` (signal recipe: window, skip, normalise, neutralise), `value-table`, `numeric-input`, `choice`; services `signal-core`, `market-gen`.
- **Modes.** `universe`, `construct`, `normalise`, `neutralise`, `ic`, `ic-series`, `breadth`, `decay`, `quantiles`, `turnover`, `net`.
- **Interactions.**
  - Pointer: assemble the recipe from tokens; drag the lookback and skip; tap a date to see its scatter and rank IC; brush a period for the IC statistics; drag an outlier to compare rank and Pearson IC; toggle sector neutralisation; drag the smoothing half-life and watch IC and turnover trade off; drag the cost and read the net Sharpe.
  - Keyboard: slider keys; Left and Right move the date; token keys for the recipe.
- **State.** `{ mode: string; recipe: string[]; lookback: number; skip: number; horizon: number; halfLife: number; cost: number; date: string; brush?: [string, string]; neutral: boolean }`.
- **Answers and checks.** `numeric` (IC on a date, mean IC, IC $t$, turnover, net Sharpe); `ordering` (quantile monotonicity); `choice`; `code` (web drills compute IC and turnover in pandas against the same synthetic panel).
- **Formulas shown live.** Rank IC on date $t$: Spearman correlation between the signal and the next period's return across stocks; $\mathrm{ICIR} = \overline{\mathrm{IC}} / s_{\mathrm{IC}}$ and $t = \mathrm{ICIR}\sqrt{n_{\text{dates}}}$; the fundamental law $\mathrm{IR} \approx \mathrm{IC}\sqrt{\text{breadth}}$ (Grinold); one-way turnover $\frac{1}{2}\sum_i \lvert w_{i,t} - w_{i,t-1} \rvert$.
- **Config.**

```ts
interface SignalLabConfig extends BaseConfig {
  mode: 'universe' | 'construct' | 'normalise' | 'neutralise' | 'ic' | 'ic-series' | 'breadth'
      | 'decay' | 'quantiles' | 'turnover' | 'net';
  panel: { generator: 'market-gen/cross-section'; seed: number; stocks: number; months: number;
           sectors: number; trueIC: number; decay: number; crash?: boolean };
  recipe?: string[];
  quantiles: number;
  cost: number;                                  // basis points per unit of one-way turnover
}
```

- **Visual.** The universe as heat cells (stocks by months, sequential ramp); one date's scatter in ink dots with the rank IC printed; the IC series as signed bars with the mean line and a ±2 standard error band; decay bars in `--s3`; quantile bars in ink with the long-short bar labelled; turnover as an ink line.
- **Motion.** Recomputations land after the debounce; nothing animates on its own.
- **Show-why.** `noise-dominates` (a single date with IC 0.05 looks like noise; the 120-date average does not), `breadth`, `turnover-eats`.
- **Reduced motion.** Base.
- **Accessibility.** "Momentum 12-1, sector neutral: mean rank IC 0.031 over 120 months, t 2.4; quantile spread 0.42% a month; one-way turnover 38% a month; net Sharpe 0.41 at 10 bp." Tables for every panel.
- **Tutor.** Ids: `token:<k>`, `slider:<param>`, `date:<d>`, `scatter`, `series:ic`, `band:se`, `bar:q<k>`, `bar:long-short`, `line:turnover`. Secret: the planted IC and decay.
- **Performance.** 500 stocks by 240 months in a worker; slider drags debounced to 50ms; the scatter of one date (500 points) in SVG.
- **Artifact and web.** No difference; pandas drills follow section 2.11.
- **Generators.** Panels with planted IC, decay, sector exposure and a momentum crash; computation items on small panels with exact answers.
- **Misconceptions.** `ic-too-small-to-matter`, `pearson-on-outliers`, `sector-bet-as-alpha`, `ignore-turnover`, `quantiles-not-checked`.

### 7.4 `vol-surface`: Volatility surface

**Composite · P2 · H.** The implied volatility surface: smiles and skews by expiry, the term structure, total variance, the implied density, no-arbitrage checks (calendar and butterfly), and an SVI fit.

- **Purpose.** The surface is where Black-Scholes is used as a quoting language. The learner sees its shape, the two conditions that keep it free of arbitrage, and how a parametric fit enforces them.
- **Serves.** 2.3.3 L4 to L7; 1.7.8 L16 (via `iv-solver`'s smile).
- **Uses.** `plot-2d` (smile against strike, log-moneyness or delta; total variance against log-moneyness; implied density), `plot-3d` (surface), `slider` (SVI parameters $a, b, \rho, m, \sigma$), `region-select` (flag strikes and expiries), `value-table`, `numeric-input`, `choice`; links to `option-chain` for its data.
- **Modes.** `smile`, `term`, `total-variance`, `density`, `arbitrage`, `svi`, `surface`.
- **Interactions.**
  - Pointer: switch the x axis between strike, log-moneyness and delta; in total-variance mode, find where two expiries' lines cross; in density mode, find where the implied density dips below zero; flag violations; in SVI mode, drag the five sliders until the fit passes; orbit the 3D surface.
  - Keyboard: slider keys; `plot-3d` keys; Space flags the focused strike.
- **State.** `{ mode: string; xAxis: 'strike' | 'log-moneyness' | 'delta'; expiry: string; flagged: string[]; svi?: { a: number; b: number; rho: number; m: number; sigma: number } }`.
- **Answers and checks.** `set` (violating strikes or expiries); `predicate: svi-fits`; `choice`; `numeric`.
- **Formulas shown live.** Total variance $w(k, T) = \sigma_{\text{imp}}^2 T$; calendar condition: $w$ does not decrease in $T$ at fixed $k$; butterfly condition: call prices are convex in $K$, so the implied density $q(K) = e^{rT}\frac{\partial^2 C}{\partial K^2}$ is non-negative (Breeden and Litzenberger); SVI: $w(k) = a + b\left(\rho(k - m) + \sqrt{(k - m)^2 + \sigma^2}\right)$ (Gatheral).
- **Config.**

```ts
interface VolSurfaceConfig extends BaseConfig {
  mode: 'smile' | 'term' | 'total-variance' | 'density' | 'arbitrage' | 'svi' | 'surface';
  surface: { generator: 'market-gen/surface'; seed: number; expiries: number[]; strikes: number;
             arbitrage?: ('calendar' | 'butterfly')[]; noise: number } | SurfaceData;
  forward: number; r: number;
}
```

- **Visual.** Smiles per expiry in slot order with direct labels; total-variance lines that must not cross, a crossing marked after grading; the density in `--s3` with any negative region patterned and labelled; the surface with the sequential ramp; SVI fit in `--manip` over the market dots.
- **Motion.** Direct.
- **Show-why.** `crossing-lines`, `negative-density`.
- **Reduced motion.** Base.
- **Accessibility.** Strike-by-expiry grid as the table view; "Expiry 3 months: total variance crosses the 6-month line at log-moneyness −0.35."
- **Tutor.** Ids: `smile:<expiry>`, `point:<expiry>:<K>`, `line:w:<expiry>`, `density`, `slider:<param>`, `surface`. Secret: the planted violations.
- **Performance.** At most 12 expiries by 40 strikes; the density by finite differences on a 200-point grid.
- **Artifact and web.** No difference.
- **Generators.** Surfaces from SVI parameters with planted calendar or butterfly arbitrage; fit targets.
- **Misconceptions.** `smile-means-mispricing`, `crossing-variance-ok`, `moneyness-axes-confused`.

### 7.5 `pricer-compare`: Pricer comparison

**Composite · P2 · H.** One option priced three ways (closed form, binomial tree, Monte Carlo): error against compute, orders of convergence, variance reduction, and which method suits which product.

- **Purpose.** The options dashboard compares pricers; the learner should know before coding that a tree's error falls like $1/N$ with an odd-even wobble, Monte Carlo's like $1/\sqrt{N}$, and that only one of them handles early exercise and only one handles path dependence cheaply.
- **Serves.** 2.3.3 L9, L10; cross-cluster: 1.9 exit (timing, with `bench-lab`).
- **Uses.** `plot-2d` (log-log error against steps or paths; against time), `slider` ($N$; paths), `sim-runner` (Monte Carlo in the worker), `value-table`, `numeric-input`, `choice`; links to `binomial-tree` (converge) and `gbm-lab` (price mode).
- **Modes.** `european`, `american`, `path-dependent`, `mc`.
- **Interactions.**
  - Pointer: slide $N$ and the number of paths; toggle antithetic paths and a control variate; read the standard error; the plot accumulates points as runs finish.
  - Keyboard: slider keys; R runs.
- **State.** `{ mode: string; N: number; paths: number; antithetic: boolean; control: boolean; points: { method: string; n: number; err: number; ms: number }[] }`.
- **Answers and checks.** `numeric` (slopes of about −1 for the tree and −½ for Monte Carlo; standard errors); `choice` (method for a product).
- **Config.**

```ts
interface PricerCompareConfig extends BaseConfig {
  mode: 'european' | 'american' | 'path-dependent' | 'mc';
  option: { type: 'call' | 'put'; style: 'european' | 'american' | 'asian' | 'barrier';
            S: number; K: number; T: number; r: number; sigma: number; barrier?: number };
  NRange: [number, number]; pathsRange: [number, number];
  seed: number;
}
```

- **Visual.** Binomial points in `--s2`, Monte Carlo in `--s6` with error bars; the closed-form value as dashed ink; reference slopes as thin dotted guides labelled "slope −1" and "slope −½".
- **Motion.** Points appear as runs finish (content).
- **Show-why.** `odd-even`, `quarter-error-needs-16x`.
- **Reduced motion.** Base.
- **Accessibility.** Table of method, $N$, price, error and time.
- **Tutor.** Ids: `series:tree`, `series:mc`, `line:exact`, `slider:N`, `slider:paths`, `toggle:antithetic`, `toggle:control`.
- **Performance.** Trees up to $N = 2{,}000$ and Monte Carlo up to $10^6$ paths in batches, in the worker; timings labelled with the device.
- **Artifact and web.** No difference.
- **Generators.** Option parameter sets; method-choice items.
- **Misconceptions.** `mc-converges-like-tree`, `more-steps-always-better`, `antithetic-free-lunch`.

### 7.6 `feed-sim`: Market data feed

**Composite · P2 · H.** Market data messages: their anatomy; the websocket lifecycle (connect, subscribe, heartbeat, disconnect, reconnect with backoff); sequence numbers and gaps; snapshot plus deltas; rebuilding the book; duplicates and idempotency.

- **Purpose.** A feed handler is correct only if it notices when it has missed something. The learner rebuilds a book from messages and has to catch the gap.
- **Serves.** 2.3.4 L1 to L3; cross-cluster: 2.4 trading competitions.
- **Uses.** `price-ladder` (the rebuilt book), `code-surface` (read-addressable raw messages), `stepper` (message by message, speed control), `node-link` (connection state machine), `token-tray` (recovery steps), `value-table`, `numeric-input`, `choice`; links to `json-explorer`; service `exchange-sim` (feed output).
- **Modes.** `messages`, `connection`, `book`, `recovery`.
- **Interactions.**
  - Pointer: step through messages and watch (or apply) each delta on the ladder; flag the message where the sequence skips; order the recovery steps (buffer, request snapshot, discard deltas older than the snapshot, replay the rest); in connection mode, fill the backoff delays and walk the state machine through a disconnect.
  - Keyboard: N steps; F flags the focused message; token keys for ordering.
- **State.** `{ mode: string; cursor: number; applied: number[]; flagged?: number; recovery?: string[]; delays?: number[] }`.
- **Answers and checks.** `set` (the gap message); `book` (the rebuilt book equals the reference); `ordering` (recovery); `numeric` (backoff delays, for example 1, 2, 4, 8 and 16 seconds capped at 30, with jitter shown separately); `predicate: gap-found`.
- **Config.**

```ts
interface FeedSimConfig extends BaseConfig {
  mode: 'messages' | 'connection' | 'book' | 'recovery';
  stream: { seed: number; messages: number; gaps: number; duplicates: number; outOfOrder: number;
            format: 'json-generic' };
  backoff?: { base: number; factor: number; cap: number; jitter: boolean };
}
```

- **Visual.** Messages in the code token with sequence numbers in a gutter; the flagged message marked with a cross icon and "gap" after grading; the ladder beside; the state machine with the current state ringed in `--manip`.
- **Motion.** Each applied delta updates the ladder as content (section 3.1).
- **Show-why.** `wrong-book` (after the gap, the learner's book and the true book diverge level by level), `stale-delta`.
- **Reduced motion.** Base.
- **Accessibility.** Messages are text; "Message 1043 follows 1041: one message missing."
- **Tutor.** Ids: `msg:<seq>`, `level:<tick>`, `state:<name>`, `step:<k>`, `delay:<k>`. Secret: gap positions.
- **Performance.** Up to 5,000 messages; the list virtualised.
- **Artifact and web.** No difference.
- **Generators.** Streams with gaps, duplicates and reordering at chosen places.
- **Misconceptions.** `ignore-sequence`, `deltas-before-snapshot`, `reconnect-without-backoff`.

### 7.7 `candle-builder`: Candle builder

**Composite · P2 · H.** Ticks into candles: open, high, low, close and volume; bar boundaries and labels; roll-ups from fine to coarse bars; late ticks; empty intervals; VWAP; time zones.

- **Purpose.** Candles look trivial and hide conventions: which bar owns a tick at exactly 10:01:00, what to do with a tick that arrives late, and why a 5-minute bar must be built from 1-minute bars rather than ticks once the ticks are gone.
- **Serves.** 2.3.4 L4 to L7; cross-cluster: 1.1.3 resampling (`time-series-lab`).
- **Uses.** `plot-2d` (ticks as dots on a time axis; candles), `marks` (`candles`, `trade-glyphs`), `array-strip` (the tick tape), `region-select` (bar windows), `drag-point` (a boundary), `value-table`, `numeric-input`, `card-sort` (late-tick policy), `choice`.
- **Modes.** `aggregate`, `boundaries`, `rollup`, `late`, `empty`, `tz`.
- **Interactions.**
  - Pointer: select the ticks inside a window and fill the candle's five numbers; drag a boundary and assign edge ticks; roll five 1-minute bars into a 5-minute bar; when a late tick arrives, choose amend, drop or carry; choose an empty-bar policy; convert a session's bars across a daylight-saving change.
  - Keyboard: tape cells with Left and Right, Space selects; fields; card keys.
- **State.** `{ mode: string; window: [number, number]; selected: number[]; entries: { o?: number; h?: number; l?: number; c?: number; v?: number }; policy?: string }`.
- **Answers and checks.** `numeric` (OHLCV and VWAP); `mapping` (tick to bar); `predicate: bars-equal`; `choice`.
- **Config.**

```ts
interface CandleBuilderConfig extends BaseConfig {
  mode: 'aggregate' | 'boundaries' | 'rollup' | 'late' | 'empty' | 'tz';
  ticks: { generator: 'market-gen/ticks'; seed: number; minutes: number; edgeTicks: number; lateTicks: number } | TickData;
  interval: '1m' | '5m' | '1h';
  closed: 'left'; label: 'left' | 'right';
  tz?: { exchange: string; display: string };
}
```

- **Visual.** Ticks as ink dots sized by quantity; the window bracket in `--manip`; the learner's candle outlined `--manip` until graded; reference candles after grading; boundary ticks marked with a small diamond.
- **Motion.** Direct.
- **Show-why.** `boundary-owner` (the tick at the boundary jumps into the later bar under left-closed intervals), `rollup-equals`.
- **Reduced motion.** Base.
- **Accessibility.** "Bar 10:00 to 10:01: 14 ticks; open 100.02, high 100.09, low 99.98, close 100.05, volume 3,200."
- **Tutor.** Ids: `tick:<n>`, `bar:<start>`, `window`, `boundary:<t>`, `field:<o|h|l|c|v>`.
- **Performance.** Up to 50,000 ticks; dots on Canvas 2D above 1,500.
- **Artifact and web.** No difference.
- **Generators.** Tick streams with ticks on exact boundaries, late ticks and empty minutes.
- **Misconceptions.** `close-is-max`, `boundary-tick-earlier-bar`, `rollup-from-ticks-only`, `local-time-bars`.

### 7.8 `latency-lab`: Latency lab

**Composite · P2 · H.** Timestamps through a pipeline; clock offsets; percentiles and tails; histograms on log axes; coordinated omission; queues near capacity; Little's law.

- **Purpose.** Latency is a distribution, not a number; its tail is what hurts; measuring it honestly takes synchronised clocks and a load generator that does not wait for slow replies.
- **Serves.** 2.3.4 L8 to L10; cross-cluster: 1.9 performance.
- **Uses.** `node-link` (pipeline stages with timestamps), `plot-2d` (log-x histogram; queue length over time; latency against utilisation), `marks`, `drag-point` (percentile handles), `slider` (arrival rate, service rate, burst size), `sim-runner` (`latency` model, queue), `value-table`, `numeric-input`, `choice`.
- **Modes.** `clocks`, `percentiles`, `omission`, `queue`.
- **Interactions.**
  - Pointer: read timestamps at each stage and compute a one-way delay with a known clock offset; place p50, p99 and p99.9 handles on the histogram; compare the "wait for each reply" measurement with the fixed-schedule one; raise the arrival rate towards capacity and watch the queue.
  - Keyboard: handles step by histogram bin; slider keys.
- **State.** `{ mode: string; handles: Record<'p50' | 'p99' | 'p999', number>; rate?: number; service?: number }`.
- **Answers and checks.** `numeric` (delays, percentiles); `point` (handles within a bin); `choice`.
- **Formulas shown live.** Little's law $L = \lambda W$; for a single server with Poisson arrivals and exponential service, $W = \frac{1}{\mu - \lambda}$.
- **Config.**

```ts
interface LatencyLabConfig extends BaseConfig {
  mode: 'clocks' | 'percentiles' | 'omission' | 'queue';
  samples?: { generator: 'market-gen/latency'; seed: number; n: number; p50: number; tailIndex: number; pauses?: number };
  pipeline?: { stage: string; t: number; clock: string }[];
  queue?: { lambda: [number, number]; mu: number; burst?: number };
}
```

- **Visual.** The histogram in ink on a log x axis; percentile handles in `--manip`; true percentiles dashed after grading; the two measurement methods as two outlines labelled; the queue as an ink line.
- **Motion.** Queue runs draw over 600ms.
- **Show-why.** `mean-hides-tail`, `omission-gap`, `hockey-stick` (waiting time rising without bound as utilisation nears 1).
- **Reduced motion.** At once.
- **Accessibility.** "p50 180 microseconds, p99 2.1 milliseconds, p99.9 9.8 milliseconds; mean 310 microseconds." Histogram table.
- **Tutor.** Ids: `stage:<name>`, `hist`, `handle:<p>`, `line:true:<p>`, `slider:rate`, `curve:wait`.
- **Performance.** $10^5$ samples binned in a typed array.
- **Artifact and web.** No difference.
- **Generators.** Samples with set percentiles and tails; clock-offset items; queue items.
- **Misconceptions.** `mean-is-enough`, `clocks-agree`, `full-utilisation-fine`.

### 7.9 `order-lifecycle`: Order lifecycle

**Composite · P2 · H.** The order state machine; idempotent client order ids; reconciliation after a crash; pre-trade risk checks and the kill switch; the architecture of a trading bot.

- **Purpose.** A bot is mostly bookkeeping under uncertainty: an order can be filled while your cancel is in flight, a fill message can arrive twice, and after a crash your own records are the least trustworthy thing you have.
- **Serves.** 2.3.5 L1, L4 to L6; 2.3.1 L11 (architecture).
- **Uses.** `node-link` (state diagram; architecture), `order-ticket`, `value-table` (`blotter`; the broker's report), `token-tray` (apply events to orders), `stepper` (event stream), `card-sort`, `numeric-input`, `choice`; services `exchange-sim` (paper broker), `ledger`.
- **Modes.** `architecture`, `states`, `recovery`, `risk`.
- **States.** Pending new, new (acknowledged), partially filled, filled; pending cancel, cancelled; pending replace, replaced; rejected. Fills may arrive while a cancel is pending.
- **Interactions.**
  - Pointer: drag each event onto the order it belongs to (matched by client order id) and the order's state updates, with illegal transitions refused and explained; in recovery mode, compare the bot's records with the broker's and mark the orders to cancel or resynchronise; in risk mode, mark the orders the risk layer must reject (maximum position, maximum notional, a price collar, an order-rate limit), then press the kill switch and check what it must do.
  - Keyboard: token keys; Enter applies; grid keys in tables.
- **State.** `{ mode: string; orders: Record<string, { state: string; filled: number }>; applied: string[]; marks: string[] }`.
- **Answers and checks.** `predicate: order-state-valid`; `predicate: risk-gate`; `set`; `ordering`; `mapping` (architecture).
- **Config.**

```ts
interface OrderLifecycleConfig extends BaseConfig {
  mode: 'architecture' | 'states' | 'recovery' | 'risk';
  events?: { seed: number; orders: number; duplicates: number; races: number; crashAt?: number };
  limits?: { maxPosition: number; maxNotional: number; collarPct: number; maxOrdersPerSec: number };
}
```

- **Visual.** The state diagram with the current state ringed in `--manip`; events as lipped tokens; refused transitions with a cross icon and a reason; broker and local tables side by side with mismatches marked by a glyph after grading.
- **Motion.** A token snaps onto its order (`spring-snap`); the state ring moves along the edge over 200ms.
- **Show-why.** `fill-after-cancel` (the race drawn on a timeline), `double-count`.
- **Reduced motion.** Instant.
- **Accessibility.** "Order C-17: new, then partially filled 200 of 500, then pending cancel; a fill of 300 arrives." Tables are the table view.
- **Tutor.** Ids: `order:<clOrdId>`, `event:<n>`, `state:<name>`, `row:local:<id>`, `row:broker:<id>`, `limit:<name>`, `kill`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Event streams with duplicates, late acknowledgements, fill-after-cancel races and crash points; risk items.
- **Misconceptions.** `cancel-is-instant`, `duplicate-fill-counted`, `trust-local-state`, `risk-after-send`.

### 7.10 `paper-trader`: Paper trader

**Composite · P2 · H.** Indicators (EMA, RSI, Supertrend), rule-based strategies as state machines, paper runs on candles with costs, and the honest comparison with chance.

- **Purpose.** Build the curriculum's fifth project's strategy logic, then test it against random entries with the same number of trades. The curriculum ranks this project last because such rules rarely beat chance; the widget shows the learner how to find out.
- **Serves.** 2.3.5 L2, L3, L7.
- **Uses.** `plot-2d` (candles with overlays; an RSI panel; equity), `marks` (`candles`, bands, `trade-glyphs`), `token-tray` (rule tokens), `slider` (EMA spans, RSI period, ATR multiple, cost), `sim-runner` (`null-strategy`), `value-table`, `numeric-input`, `choice`; service `backtest-core`.
- **Modes.** `indicators`, `rules`, `run`, `null`.
- **Interactions.**
  - Pointer: compute one EMA and one RSI value by hand from a short series; build the rule ("when EMA(12) crosses above EMA(26), go long; exit when it crosses back") from tokens; run it on a seeded series with costs; press "Compare with chance" to run 1,000 random-entry strategies with the same trade count and holding periods.
  - Keyboard: token keys; slider keys; R runs.
- **State.** `{ mode: string; rule: string[]; params: Record<string, number>; entries: Record<string, number>; seed: number }`.
- **Answers and checks.** `numeric` (EMA, RSI, ATR values; the share of random strategies that beat the rule); `state` (the rule); `choice`.
- **Formulas shown live.** $\mathrm{EMA}_t = \alpha x_t + (1 - \alpha)\mathrm{EMA}_{t-1}$ with $\alpha = \frac{2}{N + 1}$; $\mathrm{RSI} = 100 - \frac{100}{1 + \mathrm{RS}}$, with RS the ratio of Wilder-smoothed gains to losses; Supertrend bands $\frac{H + L}{2} \pm m \cdot \mathrm{ATR}$ with the trailing rule.
- **Config.**

```ts
interface PaperTraderConfig extends BaseConfig {
  mode: 'indicators' | 'rules' | 'run' | 'null';
  series: { generator: 'price-series'; seed: number; days: number; interval: '1d' | '1h' } | CandleData;
  indicators: ('ema' | 'rsi' | 'atr' | 'supertrend')[];
  rule?: string[];
  cost: number;
  nullRuns?: number;
}
```

- **Visual.** Monochrome candles; EMAs in `--s2` and `--s6` with labels; Supertrend as a dashed ink line; trades as triangles; equity in ink against the null band in `--s2` at 35% with its median.
- **Motion.** Runs draw over 600ms.
- **Show-why.** `lag` (the EMA turns after the price does), `chance-band`.
- **Reduced motion.** At once.
- **Accessibility.** "Rule: 23 trades, net return 6.1% after costs; 41% of random strategies did better." Tables of indicator values and trades.
- **Tutor.** Ids: `token:<k>`, `slider:<param>`, `series:ema:<n>`, `panel:rsi`, `trade:<n>`, `curve:equity`, `band:null`.
- **Performance.** Null runs in the worker.
- **Artifact and web.** No difference.
- **Generators.** Series; indicator computations with tidy numbers; rule-construction items.
- **Misconceptions.** `indicator-predicts`, `backtest-without-costs`, `one-path-proves`.

### 7.11 `results-note`: Results note

**Composite · P2 · H.** The one-page results note every project ships with: question, data, method, results, what failed, limitations, next steps; consistency checks against pasted metrics; Bertie's review against a rubric; export.

- **Purpose.** The curriculum asks for a note that includes what failed. The widget makes that section mandatory and checks that the numbers in the prose match the numbers the code produced.
- **Serves.** 2.3.0 L3; every 2.3 project; cross-cluster: 3.1 replication notes, 2.1 project write-ups; 3.3.5 L6 (the project walk-through draws on it).
- **Uses.** `free-response` (sectioned), `value-table` (metrics from pasted JSON), `setup-checklist` (project link); service `rubric-marker`.
- **Interactions.**
  - Pointer: paste the metrics JSON (schema published with each project); write each section; live checks show missing sections, a length above one page (about 500 words), any number in the text that does not match the metrics, and a Sharpe ratio above 2 with no explanation; "Ask Bertie to review" returns draft marks with quotes; the learner confirms or changes each mark; Export produces Markdown.
  - Keyboard: textareas; Tab between sections; R requests review.
- **State.** `{ sections: Record<string, string>; metrics?: Record<string, number>; marks?: Record<string, { mark: number; evidence: string; confirmed: boolean }> }`.
- **Answers and checks.** `rubric` (`tutor-draft`); `predicate: sections-complete`; `predicate: metrics-consistent`.
- **Config.**

```ts
interface ResultsNoteConfig extends BaseConfig {
  project: 'backtester' | 'alpha' | 'options' | 'market-data' | 'bot' | 'replication';
  sections: { id: string; title: string; required: boolean; maxWords?: number }[];
  metricsSchema: Record<string, 'number' | 'string'>;
  rubric: RubricItem[];
  flags: { sharpeAbove?: number };
}
```

- **Visual.** Sections as stacked text areas with word counts; failed checks as neutral inline notes with an icon and text (they are not grades); the metrics table beside.
- **Motion.** None.
- **Show-why.** Not applicable.
- **Reduced motion.** Not applicable.
- **Accessibility.** Real text areas; each check is announced on blur.
- **Tutor.** Ids: `section:<id>`, `metric:<name>`, `check:<id>`, `mark:<item>`. Bertie reviews only on the learner's request.
- **Performance.** Trivial.
- **Artifact and web.** Export through `downloads` in the Artifact, a Blob link on the web.
- **Generators.** None; rubrics are authored per project.
- **Misconceptions.** `hide-failures`, `metrics-without-costs`, `in-sample-only`.

---

## 8. Interview composites (3.3, and the weekly problems from 1.5)

### 8.1 `puzzle-workbench`: Puzzle workbench

**Composite · P0 core (weekly, practice, book-log) · D4; P2 interview modes (cold, aloud) · J.** One place to solve a word problem: statement, working, answer, hints, a worked solution, the linked picture, self-rating and spaced redo.

- **Purpose.** Interview problems are solved on paper and aloud, not on a canvas. The workbench gives that setting a structure (clarify, plan, solve, check), keeps the learner's working, and opens the matching visual widget only after an attempt, so the picture explains rather than solves.
- **Serves.** The weekly three problems from 1.5 onwards; 3.3.2 L1 to L14; 3.3.5 L2; homework long-form items in 1.5, 1.6 and 1.7.
- **Uses.** `scratch-pad`, `speed-timer` (count-up with a soft target), `numeric-input`, `expression-input`, `choice`, `free-response`, `derivation-steps` (the solution view), `voice-capture` (aloud mode), `live-formula`; linked mode (section 2.1) for `first-step-solver`, `indicator-board`, `geo-prob`, `lattice-walk`, `order-statistics`, `markov-chain`, `game-lab`, `outcome-grid`, `counting-slots`, `path-simulator`, `bet-lab` and `kelly-lab`; services `problem-bank`, `rubric-marker`.
- **Modes.**
  - `weekly` (P0): one problem at a time from the week's three; hints after the first attempt; Bertie available.
  - `practice` (P0): sets by pattern (symmetry, linearity, first-step analysis and so on), with the pattern hidden until after the attempt, because naming the pattern is half the solution.
  - `book-log` (P0): the learner logs problems from their own copy of a book by reference ("Zhou 4.2, problem 7"), with outcome (solved cold, solved with a hint, failed) and time. No problem text is stored.
  - `cold` (P2): interview conditions: a visible clock, no hints, one attempt, then the solution.
  - `aloud` (P2): the learner speaks while solving; the transcript is marked against the communication rubric.
- **Interactions.**
  - Pointer: read the problem; work in the scratch pad (the "clarify, plan, solve, check" template is optional); enter the answer; Check; after a not-yet verdict, Get help opens Bertie's three rungs (weekly and practice only); after solving or after the third rung, "See the picture" opens the linked widget with the problem's parameters; the solution view walks the worked steps, alternative solutions and common wrong answers with their diagnoses; rate the problem (easy, hard, failed) to schedule redo.
  - Keyboard: the scratch pad is text; Tab reaches the answer field; Enter checks; H opens help; P opens the picture; 1, 2 and 3 rate.
- **State.** `{ problemId: string; seed?: string; mode: string; notes: string; answer?: string; attempts: number; hints: number; ms: number; rating?: 'easy' | 'hard' | 'failed'; transcriptRef?: string; log?: { ref: string; outcome: string; ms: number }[] }`.
- **Answers and checks.** `numeric` (with exact rational support and the probability forms of the probability cluster), `expression`, `choice`, `rubric` (proofs, explanations, aloud mode), `state` (book-log entries).
- **Config.**

```ts
interface PuzzleWorkbenchConfig extends BaseConfig {
  mode: 'weekly' | 'practice' | 'book-log' | 'cold' | 'aloud';
  problem: { bank: string; id: string } | { family: string; seed: string; difficulty: 1 | 2 | 3 | 4 | 5 };
  answer: { type: 'numeric' | 'expression' | 'choice' | 'free-text'; check: Check };
  linked?: { widget: string; params: Record<string, unknown> };
  timer: { show: boolean; softTargetS?: number };
  template?: 'clarify-plan-solve-check' | 'blank';
  source?: { book: 'mosteller' | 'zhou' | 'crack' | 'joshi' | 'jane-street-guide' | 'original'; chapter?: string };
}
```

- **Visual.** The problem card at the top in body type with KaTeX; the scratch pad below on `--bg-sunken`; the answer row above the button group; the timer quiet (caption, `--text-muted`) except in cold mode; pattern tags hidden until after the attempt; the source citation in caption type ("After Mosteller, problem 1").
- **Motion.** None of its own; linked widgets bring their own.
- **Show-why.** Per problem: the linked widget's own recipes (for example `first-step-solver`'s equation highlight).
- **Reduced motion.** Base.
- **Accessibility.** The problem is text; the timer can be hidden; cold mode offers the "more time" setting with adjusted marking (section 2.8).
- **Tutor.** Describe: "Problem: expected rolls of a fair die until two sixes in a row. Attempt 1: 36 (not yet). Notes: 3 lines, defines states 0, 1." Ids: `problem`, `notes`, `answer`, `timer`, `picture`, `step:<n>`. Secret: the answer and the solution outline. Bertie may read the notes text; the ink only as an image on request.
- **Performance.** Trivial; linked widgets load lazily.
- **Artifact and web.** No difference.
- **Generators.** `problem-bank` families: waiting times for patterns, gambler's ruin variants, dice and card expectations, geometric probability on shapes, order statistics, coupon collecting, optimal stopping with costs; each family has an exact solver and a simulation check in CI. Authored problems are recreations with original solutions, cited by source.
- **Misconceptions.** Per problem, stored in the bank with each wrong answer's diagnosis.

### 8.2 `bet-lab`: Betting lab

**Composite · P2 · J.** The expected value and fair price of a bet; odds formats and implied probability; the bookmaker's margin; hedging a position after prices move; arbitrage across books; interview betting games.

- **Purpose.** Interviewers ask "would you play this game, and for how much?" The answer is an expected value, a variance and a bankroll consideration, in that order.
- **Serves.** 3.3.3 L1, L2, L4, L5, L12.
- **Uses.** `value-table` (outcomes, probabilities, payoffs), `mass-editor` (probabilities; stakes across outcomes), `chance-object` (dice, cards, coins), `slider` (stake; price to play), `plot-2d` (payoff by outcome; P&L distribution), `numeric-input`, `choice`; links to `game-lab` and `kelly-lab`.
- **Modes.** `ev`, `odds`, `hedge`, `arbitrage`, `game`.
- **Interactions.**
  - Pointer: fill or read the outcome table and compute the fair price; convert between decimal, fractional and American odds; sum implied probabilities to find the margin; in hedge mode, size the opposing bet that makes every outcome pay the same; in arbitrage mode, spread stakes across books so every outcome pays the same and more than the total stake; in game mode, price the game, then play rounds (outcomes shown, never graded).
  - Keyboard: table cells; mass-editor keys; slider keys; P plays a round.
- **State.** `{ mode: string; outcomes: { id: string; p: Entry; payoff: number }[]; stakes?: number[]; price?: number; played: number[] }`.
- **Answers and checks.** `numeric` (EV, fair price, implied probability, margin, hedge stake); `predicate: is-arbitrage`; `choice`.
- **Formulas shown live.** $E[X] = \sum_i p_i x_i$; implied probability from decimal odds $d$: $1/d$; from fractional odds $a/b$: $\frac{b}{a + b}$; from American $+A$: $\frac{100}{A + 100}$, and $-A$: $\frac{A}{A + 100}$; margin $\sum_i 1/d_i - 1$; when $\sum_i 1/d_i < 1$, stakes proportional to $1/d_i$ lock in a profit.
- **Config.**

```ts
interface BetLabConfig extends BaseConfig {
  mode: 'ev' | 'odds' | 'hedge' | 'arbitrage' | 'game';
  outcomes?: { id: string; label: string; p: Entry; payoff: number }[];
  books?: { id: string; odds: Record<string, number> }[];
  game?: { preset: 'pay-to-roll' | 'double-or-nothing' | 'card-high' | 'two-dice-max' | 'custom'; params?: Record<string, number> };
  format: 'decimal' | 'fractional' | 'american';
  seed?: number;
}
```

- **Visual.** The outcome table with probabilities as fractions and decimals; payoff bars by outcome with a signed fill; stakes in `--manip`; chance devices from `chance-object`.
- **Motion.** Chance devices animate for the first ten rounds only (the probability cluster's rule).
- **Show-why.** `stake-included` (decimal odds return the stake), `margin-is-overround`.
- **Reduced motion.** Devices show results with a cross-fade.
- **Accessibility.** "Game: pay 3.50 to roll a die and receive the face value. Expected value 3.50; fair."
- **Tutor.** Ids: `row:<outcome>`, `stake:<k>`, `slider:price`, `book:<id>`, `device`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Games with exact expected values; odds sets with and without arbitrage; hedge items.
- **Misconceptions.** `odds-are-probabilities`, `decimal-odds-exclude-stake`, `hedge-loses-ev`, `doubling-system-wins`.

### 8.3 `kelly-lab`: Kelly lab

**Composite · P2 · J.** Sizing bets to maximise long-run growth: the growth curve and its peak, over-betting, fractional Kelly, several outcomes, simultaneous bets, an uncertain edge, and the continuous version.

- **Purpose.** A favourable bet can still ruin you if you bet too much. The growth curve shows why the best fraction is interior, why twice that fraction grows at about zero, and why practitioners bet less than full Kelly.
- **Serves.** 3.3.3 L3, L6 to L11; cross-cluster: 1.5 (preview via `game-lab`), 2.3.1 L6 (sizing).
- **Uses.** `plot-2d` (growth curve $g(f)$; wealth fan on a log scale; drawdown distribution), `drag-point` ($f$ on the curve), `slider` ($p$, $b$, $f$, fraction of Kelly $\lambda$), `sim-runner` (`bet-sequence`), `mass-editor` (stakes across outcomes), `marks`, `live-formula`, `numeric-input`, `choice`; links to `convexity-chord`.
- **Modes.** `curve`, `paths`, `compare`, `fractional`, `multi`, `simultaneous`, `uncertain`, `continuous`.
- **Interactions.**
  - Pointer: drag $f$ along the growth curve; run paths for the chosen $f$; compare $f^*$, $\frac{1}{2}f^*$, $2f^*$ and $3f^*$ side by side; in multi mode, spread stakes over outcomes with the mass editor; in uncertain mode, set a range for $p$ and compare the growth of the plug-in Kelly fraction with a shrunk one.
  - Keyboard: the $f$ handle steps by 0.01; slider keys; R runs.
- **State.** `{ mode: string; p: number; b: number; f: number; lambda?: number; stakes?: number[]; seed: number }`.
- **Answers and checks.** `numeric` ($f^*$, growth rate); `point` (the peak); `predicate: kelly-near`; `choice`.
- **Formulas shown live.** $g(f) = p\ln(1 + bf) + (1 - p)\ln(1 - f)$; $f^* = p - \frac{1 - p}{b}$; continuous $f^* = \frac{\mu - r}{\sigma^2}$ with growth $r + \frac{(\mu - r)^2}{2\sigma^2}$ at $f^*$; with fraction $\lambda$ of Kelly, growth $\approx (2\lambda - \lambda^2)$ times the full-Kelly excess growth, and the chance of ever falling to a fraction $x$ of starting wealth $\approx x^{2/\lambda - 1}$ [recalled from Thorp's continuous approximation].
- **Config.**

```ts
interface KellyLabConfig extends BaseConfig {
  mode: 'curve' | 'paths' | 'compare' | 'fractional' | 'multi' | 'simultaneous' | 'uncertain' | 'continuous';
  bet?: { p: Entry; b: Entry };
  outcomes?: { p: Entry; payoff: number }[];
  bets?: { p: Entry; b: Entry }[];
  continuous?: { mu: number; r: number; sigma: number };
  sim: { seed: number; paths: number; rounds: number };
  pRange?: [number, number];
}
```

- **Visual.** The growth curve in ink with the zero line; the $f$ handle in `--manip`; the peak dashed after the learner commits; wealth paths in ink at 15% on a log axis with the median in `--s2`; a ruin threshold dashed and labelled.
- **Motion.** Paths draw over 600ms.
- **Show-why.** `overbet` (paths at $2f^*$ drift sideways and at $3f^*$ downwards, while the mean still rises), `half-kelly-tradeoff`.
- **Reduced motion.** Paths at once.
- **Accessibility.** "p 0.55, even odds: Kelly fraction 0.10; at 0.10 the growth rate is 0.50% a bet; at 0.20 it is about zero (−0.01%)." Path quantiles as a table.
- **Tutor.** Ids: `handle:f`, `curve:growth`, `peak`, `fan`, `line:median`, `line:ruin`, `slider:<param>`, `stake:<k>`.
- **Performance.** 200 paths of 1,000 bets drawn on Canvas 2D; up to $10^4$ paths summarised in the worker.
- **Artifact and web.** No difference.
- **Generators.** $(p, b)$ with tidy $f^*$; multi-outcome items solved numerically in CI; continuous items.
- **Misconceptions.** `bet-to-max-ev`, `kelly-is-safe`, `kelly-on-estimated-edge`, `sum-individual-kellys`.

### 8.4 `mm-game`: Market-making game

**Composite · P2 · J.** The interview market-making game: make a two-sided market on an unknown quantity, trade with counterparties, update after each trade and each reveal, manage inventory, settle, and review every quote against what could have been known.

- **Purpose.** Trader interviews test whether you can turn a probability into a price, set a width that reflects uncertainty and adverse selection, move when you are hit, and stay consistent across related markets, all aloud and quickly.
- **Serves.** 3.3.4 L1 to L11; 3.3.5 L4; cross-cluster: 1.7.9 (adverse selection in practice).
- **Uses.** `quote-entry`, `number-line` (the value axis with the quote bracket and, in review, the posterior distribution), `chance-object` (dice and cards), `price-ladder` (ladder view and multi-counterparty mode), `value-table` (`blotter`), `speed-timer`, `voice-capture` (interview and partner modes), `scratch-pad` (notes), `plot-2d` (posterior and the post-game timeline); links to `fermi-estimator` and `calibration-lab`; services `exchange-sim` (multi-counterparty mode), `ledger`, `interview-engine` (interview mode); `room` capability for two-device partner play.
- **Modes.** `anatomy`, `dice`, `width`, `update`, `inventory`, `sequential`, `fermi`, `multi-bot`, `linked`, `interview`, `partner`.
- **Hidden quantities.** The sum, maximum or product of $k$ dice (6, 10 or 20 faces); the sum, maximum or count of a suit in $n$ cards dealt from a standard deck without replacement; counts of heads; a Fermi quantity from the sourced fact bank; for `linked`, two quantities and their sum.
- **Counterparties** (seeded, policy shown after the game). `noise` (trades at random); `informed` (knows the value, trades when your quote is off by more than a threshold); `mixed` (informed with probability $\mu$); `sharp` (knows the public posterior and picks off quotes left stale after a reveal); `interviewer` (a scripted pattern: lifts once, then checks whether you move).
- **Interactions.**
  - Pointer: enter a market (fields, shorthand, or the bracket on the value axis); the counterparty buys at your ask, sells at your bid, or passes; re-quote; reveals arrive in sequential mode; at the end the value is revealed and positions settle.
  - Keyboard: `quote-entry` keys; Enter sends; N requests the next event in untimed play.
  - Voice: in interview and partner modes, quotes are spoken ("seven at eight") through the quote grammar and confirmed with one tap.
- **State.** `{ mode: string; seed: string; round: number; quotes: { t: number; bid: number; ask: number }[]; trades: { t: number; side: 'buy' | 'sell'; px: number; qty: number }[]; reveals: string[]; settled?: number }`.
- **Answers and checks.** `quote` (each scored quote against the exact posterior mean given public information, with the width rule); `game` (the log); `predicate: mm-score`; `numeric` (the posterior mean after a reveal); `rubric` (interview mode).
- **Review.** A timeline of every quote against the posterior mean and a ±1 standard deviation band; each trade's edge, $\text{side} \times (\text{price} - \text{posterior mean at the time})$ from the market maker's view; inventory; and, for informed counterparties, the update a trade should have caused. Settlement P&L is shown and never graded (decision 6).
- **Config.**

```ts
interface MmGameConfig extends BaseConfig {
  mode: 'anatomy' | 'dice' | 'width' | 'update' | 'inventory' | 'sequential' | 'fermi'
      | 'multi-bot' | 'linked' | 'interview' | 'partner';
  quantity: { kind: 'dice'; k: number; faces: 6 | 10 | 20; stat: 'sum' | 'max' | 'product' }
          | { kind: 'cards'; n: number; stat: 'sum' | 'max' | 'count-suit'; suit?: string }
          | { kind: 'coins'; n: number }
          | { kind: 'fermi'; factId: string };
  reveals?: { after: number; what: string }[];
  counterparties: { name: string; policy: 'noise' | 'informed' | 'mixed' | 'sharp' | 'interviewer';
                    mu?: number; threshold?: number }[];
  rules: { tick: number; maxWidth?: number; size: number; rounds: number; timeLimitS?: number };
  scoring: { minEdge?: number; requireRequoteAfterEvent: boolean };
  seed: string;
}
```

- **Visual.** The value axis with your bracket in `--manip`; dice and cards from `chance-object`, revealed cards face up; trades as triangles on the axis with the counterparty's name; inventory and cash in the blotter; in review, the posterior as `--s3` bars or a curve with the true value as dashed ink.
- **Motion.** Counterparty actions fade and rise over 200ms; reveals flip over 300ms; nothing animates during a timed quote except the timer.
- **Show-why.** `adverse-selection` (in review, the trades that hit you are drawn against the true value), `stale-quote` (after a reveal, the posterior jumps and your old quote stays behind).
- **Reduced motion.** Reveals cross-fade; actions appear at once.
- **Accessibility.** "Round 3. Two dice, one shows 5. Your market 8 at 10. Trader B buys 1 at 10. Position short 1." Untimed mode is always offered; timed scores carry their mode.
- **Tutor.** Off during timed play. Interview mode: Bertie voices the interviewer through `interview-engine`; the trading decisions remain the seeded bots'. Debrief ids: `quote:<n>`, `trade:<n>`, `reveal:<n>`, `posterior:<n>`, `band`, `inventory`. Secret: the hidden value and every bot's policy.
- **Performance.** Exact posteriors by enumeration (at most $10^6$ outcomes, or by convolution); everything else trivial.
- **Artifact and web.** Partner play on two devices only in the Artifact through `room` [unverified for guests]; pass-and-play on both.
- **Generators.** Quantities by kind and difficulty; reveal schedules; counterparty mixes; Fermi facts drawn from the sourced bank; linked pairs.
- **Misconceptions.** `quote-on-guess-not-ev`, `width-from-nothing`, `ignore-being-lifted`, `skew-wrong-way`, `too-tight-under-adverse`, `inconsistent-linked-markets`.

### 8.5 `calibration-lab`: Calibration lab

**Composite · P2 · J.** Honest uncertainty: 90% and 50% intervals on quantities, the hit rate, the interval score, and the link between an interval and a market's width.

- **Purpose.** A market's width is a confidence interval with a price on it. Most people's 90% intervals contain the truth about half the time [recalled from the calibration literature]; practice fixes that.
- **Serves.** 3.3.4 L3, L7; cross-cluster: 1.6 confidence intervals (intuition), 0.1 estimation.
- **Uses.** `number-line` (log mode with interval brackets), `numeric-input`, `value-table` (session history), `plot-2d` (calibration chart: nominal against realised coverage across sessions); links to `fermi-estimator`.
- **Interactions.**
  - Pointer: drag the two ends of an interval on a log number line (or type them); submit ten items; see the hit rate and score; review misses.
  - Keyboard: handles step by a tenth of a decade; fields.
- **State.** `{ items: { id: string; lo: number; hi: number }[]; coverage: 0.5 | 0.9; submitted: boolean }`.
- **Answers and checks.** `interval` per item (scored, not pass or fail); `predicate: calibrated` over a session (hit rate inside the binomial band: for 10 items at 90%, 7 to 10 hits); `numeric`.
- **Formulas shown live.** Interval score for nominal coverage $1 - \alpha$: $(u - l) + \frac{2}{\alpha}(l - x)\mathbf{1}\{x < l\} + \frac{2}{\alpha}(x - u)\mathbf{1}\{x > u\}$ (Gneiting and Raftery), computed on $\log_{10}$ values for magnitudes.
- **Config.**

```ts
interface CalibrationLabConfig extends BaseConfig {
  items: { factId: string }[] | { bank: 'fermi' | 'computed'; n: number; seed: string };
  coverage: 0.5 | 0.9;
  scale: 'log' | 'linear';
}
```

- **Visual.** Intervals as `--manip` brackets on a log line; after submission, the truth as an ink tick with "inside" or "outside" in words; the calibration chart with the diagonal dashed.
- **Motion.** None.
- **Show-why.** `too-narrow` (misses drawn with how far outside they fell).
- **Reduced motion.** Not applicable.
- **Accessibility.** "Item 4: your interval 2,000 to 20,000; true 8,400; inside."
- **Tutor.** Ids: `item:<id>`, `bracket:<id>`, `truth:<id>`, `chart`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Selection from the sourced fact bank (each fact with a citation and a date); computed quantities (counts and probabilities with exact values).
- **Misconceptions.** `overconfident-narrow`, `fixed-percent-interval`, `linear-scale-for-magnitudes`.

### 8.6 `mock-interview`: Mock interview

**Composite · P2 · J.** A spoken mock interview with Bertie as the interviewer, or with a human partner using the interviewer sheet: rounds, follow-ups, hints, a transcript, rubric marks with evidence, and the exit log.

- **Purpose.** Interviewers mark the reasoning as it happens. The learner needs repetitions of the whole format, including silence, hints and follow-ups, and a record of improvement towards the exit test (ten mocks, three with a stranger).
- **Serves.** 3.3.5 L1 to L8; 3.3 exit.
- **Uses.** `voice-capture`, `scratch-pad`, `speed-timer`, `puzzle-workbench` (embedded item view), `mm-game` (embedded, interview mode), `speed-drill` (embedded), `free-response` (debrief notes), `value-table` (rubric, log), `plot-2d` (the interview timeline with markers); services `interview-engine`, `speech`, `problem-bank`, `rubric-marker`; `room` capability for two-device partner sessions.
- **Rounds.** `probability`, `markets`, `speed` (mental maths and betting), `project` (a 2.3 project walk-through, using the learner's results notes as Bertie's context), `technical` (statistics and machine-learning questions from those clusters' banks), `motivation` (why trading or research; a mistake and what you learned).
- **Modes.** `review` (mark an annotated transcript), `bertie`, `partner`, `log`.
- **Flow.**
  1. Setup: track (trader, researcher, developer), rounds, length (20, 30 or 45 minutes), style (friendly, neutral, pressured), voice on or off.
  2. Run: Bertie asks; the learner answers aloud or by typing; after 20 seconds of silence Bertie prompts ("Talk me through what you are thinking"); hints come when asked or after 60 seconds stuck, and are logged; follow-ups probe ("Why is that independent?"); time is kept.
  3. Debrief: the timeline with markers (question asked, first clarifying question, plan stated, first number, hint, answer, sanity check); rubric marks with evidence quotes; model answers; three things to fix; items added to the Redo queue.
- **Rubric** (default, 10 marks, matching the owner's 10-point scale): clarifies and plans (2); reasons aloud in order (2); method correct (2); answer correct and checked (2); uses hints and handles pressure and time (2). Every mark needs a quote from the transcript as evidence (section 2.1).
- **Partner mode.** The interviewer's sheet shows the question, the solution, the hint ladder, the rubric checkboxes and the clock; the candidate's view shows the question only. One device uses a cover screen between turns; two devices use `room` in the Artifact. The partner's marks are stored as `partner` marks.
- **Log.** Every mock records date, rounds, partner type (Bertie, friend, stranger; self-declared), score and transcript reference; the exit tracker shows "7 of 10 mocks, 2 of 3 with a stranger".
- **Interactions.**
  - Pointer: setup choices; mic toggle; scratch pad; "I need a hint"; "Repeat the question"; End.
  - Keyboard: M toggles the mic; H asks for a hint; R repeats; Escape ends after confirmation.
- **State.** `{ mode: string; setup: Record<string, unknown>; round: number; transcriptRef: string; markers: { t: number; kind: string }[]; marks?: Record<string, { mark: number; evidence: string; by: 'bertie' | 'self' | 'partner' }>; logEntry?: unknown }`.
- **Answers and checks.** `rubric` (`tutor-draft` with Bertie, `partner` with a human); `state` (the log).
- **Config.**

```ts
interface MockInterviewConfig extends BaseConfig {
  mode: 'review' | 'bertie' | 'partner' | 'log';
  track: 'trader' | 'researcher' | 'developer';
  rounds: { kind: 'probability' | 'markets' | 'speed' | 'project' | 'technical' | 'motivation'; minutes: number }[];
  style: 'friendly' | 'neutral' | 'pressured';
  voice: boolean;
  rubric: RubricItem[];
  banks: string[];
  silencePromptS: number; hintAfterS: number;
}
```

- **Visual.** Bertie in the interviewer expression set at the top; captions under Bertie; the learner's transcript below; the scratch pad beside on desktop and in a sheet on phones; the clock in caption type; in the debrief, the timeline as a horizontal axis with marker glyphs and labels.
- **Motion.** Bertie's idle and speaking states follow the engine's mascot state machine; no celebration at the end of a mock.
- **Show-why.** Not applicable; the debrief carries the explanation.
- **Reduced motion.** Bertie's speaking animation becomes a static "speaking" label.
- **Accessibility.** Captions always on; typed answers count the same; timing can be relaxed and is recorded as adjusted.
- **Tutor.** Bertie is the interviewer (section 2.9.1), then returns to tutor mode for the debrief. Ids for the debrief: `marker:<n>`, `segment:<n>`, `mark:<item>`, `item:<n>`.
- **Performance.** Turn latency is the binding constraint: the quick tier in the Artifact; effort `low` on the web [unverified]; the spike in wave J measures both, and a P50 above 3 seconds triggers a faster model on the web proxy.
- **Artifact and web.** Section 2.11 for speech and partner sessions.
- **Generators.** None of its own; it selects seeded items from `problem-bank`, `mm-game` and `speed-drill` generators.
- **Misconceptions.** `silent-solving`, `answer-without-check`, `refuse-hints`, `unstructured-answer`.

---

## 9. Generators

Practice, quizzes, homework and exams need many instances of each item, and every instance must be solvable and unambiguous. Generators are code, never model output (Stage 0, section 12).

### 9.1 Contract additions

The shared `Generator` contract stands (Stage 0 section 12.1; calc-linalg section 2.12; the probability cluster's two-way verification in its section 2.2). This cluster adds three rules [our choice]:

1. **Answer first.** Finance items fix the answer before the data: choose the yield, then price the bond and round the price to its quoting precision, then recompute the yield from the rounded price as the stored answer; choose the implied volatility, then quote the option; choose the IRR, then solve for the last cash flow; choose the posterior, then the reveal. Rejection loops are a last resort.
2. **Reference implementation per family.** Each family names a CI reference: SciPy for pricing and root-finding, QuantLib for day counts and bond analytics, the Python reference matching engine for books and fills, exact enumeration plus a $10^6$-trial simulation for game posteriors.
3. **Market realism bounds.** Generated markets stay inside plausible ranges unless the item is about an anomaly: volatilities from 5% to 120%, rates from −1% to 15%, spreads of at least one tick, positive prices. Items about negative rates or zero bids say so in their prompt.

### 9.2 Families by widget

| Widget | Families | Difficulty | Answer built and verified by |
|---|---|---|---|
| `compounding-lab` | simple and compound balances; conversions between conventions; doubling times; real rates; compare sets | 1 to 4 | closed forms; CI against Python |
| `tvm-timeline` | PV; NPV; IRR from a chosen rate; annuities, perpetuities, growing perpetuities; loan payments; two-IRR traps | 1 to 5 | answer first; Brent in CI |
| `share-lab` | market cap; dilution; ex-dividend prices; split adjustment factors; index levels and divisors | 1 to 3 | exact arithmetic |
| `margin-lab` | margin-call prices (long and short); returns on equity; fee accruals | 2 to 4 | closed forms |
| `portfolio-lab` | two-asset risk and return; minimum-variance weights; tangency; beta from data | 2 to 5 | closed forms; OLS fixture for beta |
| `bond-lab` | prices from yields; YTM from rounded prices; accrued interest by day count; credit spreads | 2 to 5 | QuantLib fixtures |
| `yield-curve-lab` | discount factors; bootstrapping from rational discount factors; forwards; par swap rates | 2 to 5 | exact rationals |
| `duration-lab` | Macaulay and modified duration; DV01; convexity; immunisation with a unique solution | 2 to 5 | QuantLib fixtures |
| `order-book` | spreads and mids; walk-the-book averages; queue order; order-type outcomes; imbalance and microprice; fees | 1 to 5 | Python reference engine |
| `auction-lab` | uncrossing prices with unique maximum volume; tie-break cases | 2 to 4 | Python reference engine |
| `carry-arb` | fair forwards with income, yield, storage, foreign rates; mispricings of either sign; existing-forward values | 2 to 5 | closed forms |
| `futures-mtm` | settlement ledgers with calls on known days | 1 to 3 | exact arithmetic |
| `hedge-lab` | minimum-variance ratios; contract counts; beta hedges | 2 to 4 | closed forms |
| `payoff-builder` | targets from random leg sets; break-evens; maximum profit and loss; strategy names; sketches | 1 to 5 | exact piecewise-linear evaluation |
| `option-bounds` | quotes inside and outside each bound; convexity and monotonicity violations; American items | 2 to 5 | closed forms |
| `parity-lab` | parity violations with spreads; synthetics; boxes; implied forwards and rates | 2 to 5 | exact arithmetic |
| `option-chain` | chains with planted defects; mids and spreads; implied forwards | 1 to 4 | `market-gen` truth |
| `bs-explorer` | prices; components; $N(d_2)$; sign tables; at-the-money estimates | 1 to 4 | SciPy fixtures |
| `greeks-lab` | Greeks at a price; signs; where-largest; delta-neutral hedges | 2 to 5 | SciPy fixtures |
| `pnl-attribution` | term-by-term attribution; break-even moves | 3 to 5 | SciPy fixtures |
| `iv-solver` | quotes from chosen volatilities; tiny-vega cases; bound violations; algorithm-order items | 2 to 5 | answer first |
| `binomial-tree` | rational $q$ trees; CRR trees; American exercise sets; replication; convergence | 1 to 5 | exact rationals; Python reference |
| `tape-lab` | tapes with known initiators; spread measures; Roll series | 2 to 4 | `market-gen` truth |
| `adverse-selection` | Glosten-Milgrom quotes with rational answers; trade sequences | 2 to 5 | exact rationals |
| `dealer-sim` | fixed replays for decomposition; skew-direction items | 2 to 4 | deterministic replay |
| `execution-lab` | impact costs; shortfall arithmetic; schedule choice | 2 to 4 | closed forms |
| `backtest-lab` | planted-bug strategies; event-loop ordering; metric items; cost sweeps | 2 to 5 | `backtest-core` against pandas fixtures |
| `sharpe-lab` | metrics from fixed returns; annualisation; null thresholds; deflation | 2 to 5 | closed forms; pandas fixtures |
| `signal-lab` | small panels with exact IC and turnover; planted-IC panels for exploration | 2 to 5 | pandas and SciPy fixtures |
| `vol-surface` | SVI surfaces with planted calendar or butterfly arbitrage; fit targets | 3 to 5 | `market-gen` truth |
| `pricer-compare` | parameter sets; method-choice items; slope items | 2 to 4 | SciPy and reference pricers |
| `feed-sim` | streams with gaps, duplicates and reordering; backoff schedules | 2 to 4 | reference handler |
| `candle-builder` | tick streams with boundary and late ticks; roll-ups; time-zone items | 1 to 4 | pandas resample fixtures |
| `latency-lab` | samples with set percentiles; clock offsets; queue items | 2 to 4 | closed forms; NumPy fixtures |
| `order-lifecycle` | event streams with duplicates, races and crashes; risk-limit items | 2 to 5 | reference state machine |
| `paper-trader` | indicator values; rule construction; null comparisons on fixed seeds | 1 to 4 | pandas fixtures |
| `puzzle-workbench` | `problem-bank` families (section 8.1) | 1 to 5 | exact solvers plus simulation |
| `bet-lab` | game EVs; odds conversions; margins; hedges; arbitrage sets | 1 to 4 | exact rationals |
| `kelly-lab` | binary Kelly; multi-outcome (numerical); continuous; fractional trade-offs | 2 to 5 | closed forms; SciPy optimiser in CI |
| `mm-game` | quantities by kind; reveal schedules; counterparty mixes; Fermi facts; linked pairs | 1 to 5 | exact enumeration plus simulation |
| `calibration-lab` | fact selection; computed quantities | 1 to 3 | sourced facts; exact computation |

`results-note` and `mock-interview` have no generators of their own; the seven primitives have none.

---

## 10. Misconception register

Each misconception has an id, the verdict-chip line (at most 20 words) and the widgets whose show-why recipes answer it. Content authors attach them to distractors (design research section 5.6).

| Id | Line | Widgets |
|---|---|---|
| `simple-for-compound` | You added the same interest every year. Each year's interest also earns interest. | `compounding-lab` |
| `apr-is-ear` | A 12% rate paid monthly grows to more than 12% in a year. | `compounding-lab` |
| `rule-72-exact` | The rule of 72 is an approximation; the exact time is $\ln 2 / \ln(1 + r)$. | `compounding-lab` |
| `frequency-unbounded` | Compounding more often helps less and less; the limit is $e^r - 1$. | `compounding-lab` |
| `real-is-difference` | Real growth divides by inflation; subtracting is only close when both rates are small. | `compounding-lab` |
| `discount-multiplies` | Money later is worth less now. Divide by the growth factor; do not multiply. | `tvm-timeline` |
| `sum-without-discounting` | You added amounts paid at different dates as if they were paid today. | `tvm-timeline` |
| `irr-unique` | These cash flows change sign twice, so the NPV can cross zero twice. | `tvm-timeline` |
| `annuity-due-off-by-one` | The first payment is today, so it is not discounted. | `tvm-timeline` |
| `growing-perpetuity-sign` | Growth shrinks the denominator: $C / (r - g)$, not $C / (r + g)$. | `tvm-timeline` |
| `dividend-is-free-money` | The cash left the company, so each share is worth less by about the dividend. | `share-lab` |
| `split-changes-value` | Twice as many shares at half the price. Nothing was created. | `share-lab` |
| `raw-close-returns` | That fall is a split, not a crash. Use adjusted prices for returns. | `share-lab` |
| `index-weights-confused` | A price-weighted index gives the highest-priced stock the most weight, whatever the company's size. | `share-lab` |
| `short-loss-bounded` | A price can rise without limit, so a short can lose without limit. | `margin-lab` |
| `call-at-zero-equity` | The broker calls at the maintenance ratio, long before your equity reaches zero. | `margin-lab` |
| `gearing-adds-return-not-risk` | Borrowing scales losses by the same factor as gains. | `margin-lab`, `futures-mtm` |
| `diversify-needs-negative-corr` | Any correlation below 1 reduces risk. Negative correlation is not required. | `portfolio-lab` |
| `min-var-is-safer-asset` | The mix can be less risky than the safer asset alone. | `portfolio-lab` |
| `max-sharpe-is-max-return` | The best Sharpe ratio is the steepest line from the risk-free rate, not the highest point. | `portfolio-lab` |
| `beta-is-correlation` | Beta is correlation times the ratio of volatilities. | `portfolio-lab` |
| `n-stocks-zero-risk` | With correlated stocks, risk falls towards $\sqrt{\rho}\,\sigma$, not zero. | `portfolio-lab` |
| `price-yield-same-direction` | A higher yield discounts every cash flow more, so the price falls. | `bond-lab` |
| `ytm-is-coupon` | The coupon is fixed; the yield depends on the price you pay. | `bond-lab` |
| `clean-includes-accrued` | The clean price leaves out accrued interest; the buyer pays the dirty price. | `bond-lab` |
| `spread-is-default-probability` | A spread is roughly default intensity times the loss given default. | `bond-lab` |
| `forward-is-average` | The forward is what makes the two routes cost the same, not their average. | `yield-curve-lab` |
| `zero-equals-par-yield` | Zero rates and par yields agree only when the curve is flat. | `yield-curve-lab` |
| `floating-leg-unknowable` | A floating leg is worth par at each reset, so you can value it today. | `yield-curve-lab` |
| `duration-is-maturity` | Coupons pull the balance point earlier than maturity. | `duration-lab` |
| `higher-coupon-longer` | A higher coupon puts more value early, so duration falls. | `duration-lab` |
| `linear-is-enough` | For large moves the tangent misses; add the convexity term. | `duration-lab` |
| `convexity-hurts-holder` | The curve lies above its tangent: convexity helps the holder both ways. | `duration-lab` |
| `fills-at-best-ask` | Only the quantity at the best ask fills there; the rest comes from higher levels. | `order-book` |
| `trades-at-mid` | The mid is not a price anyone offered. A buyer pays the ask. | `order-book` |
| `limit-always-better` | A limit order saves the spread only if it fills. Sometimes the price runs away. | `order-book` |
| `market-order-free` | A market order pays half the spread, and more if it walks the book. | `order-book`, `execution-lab` |
| `queue-by-size` | At one price, orders fill in time order, not by size. | `order-book` |
| `amend-keeps-priority` | Changing the price, or raising the size, sends the order to the back of the queue. | `order-book` |
| `stop-is-limit` | A stop order rests unseen until triggered, then becomes a market order. | `order-book` |
| `ioc-rests` | Immediate-or-cancel never rests; the unfilled part is cancelled. | `order-book` |
| `auction-at-midpoint` | The auction price maximises the volume that can trade, not the midpoint of bids. | `auction-lab` |
| `max-volume-is-most-orders` | Volume counts shares, not orders. | `auction-lab` |
| `forward-is-forecast` | The forward follows from the carry. Change the rate and it moves with no change in forecasts. | `carry-arb` |
| `forget-income` | The holder of the asset receives its dividends, which reduces the cost of carry. | `carry-arb` |
| `fx-forward-wrong-way` | The higher-rate currency trades at a forward discount. | `carry-arb` |
| `existing-forward-undiscounted` | The difference in forward prices is paid at expiry, so discount it to today. | `carry-arb` |
| `call-tops-to-maintenance` | A margin call restores the initial margin, not the maintenance level. | `futures-mtm` |
| `futures-pnl-at-expiry-only` | Futures settle every day; gains and losses move daily. | `futures-mtm` |
| `contango-means-expected-rise` | Contango reflects carry costs, not a forecast that prices will rise. | `futures-mtm` |
| `hedge-ratio-one` | The best ratio is the regression slope, $\rho\sigma_S/\sigma_F$. | `hedge-lab` |
| `hedge-removes-all-risk` | What remains is basis risk: $\sigma_S^2(1 - \rho^2)$. | `hedge-lab` |
| `beta-with-correlation` | Size an index hedge with beta, not with correlation. | `hedge-lab` |
| `payoff-includes-premium` | Payoff ignores the premium; profit subtracts it. | `payoff-builder` |
| `short-put-unbounded` | A short put loses at most the strike less the premium, because prices stop at zero. | `payoff-builder` |
| `straddle-profits-at-strike` | At the strike both legs pay nothing; a long straddle loses its premium there. | `payoff-builder` |
| `butterfly-bets-on-move` | A long butterfly pays most when the price ends near the middle strike. | `payoff-builder` |
| `lower-bound-is-intrinsic` | For a European call the bound is $S_0 - Ke^{-rT}$, above intrinsic value. | `option-bounds` |
| `call-above-stock` | A call can never cost more than the share it lets you buy. | `option-bounds` |
| `exercise-american-call-early` | Without dividends, an American call is worth more alive than exercised. | `option-bounds`, `binomial-tree` |
| `convexity-optional` | Call prices must be convex in the strike, or a butterfly is free money. | `option-bounds`, `vol-surface` |
| `parity-needs-model` | Parity follows from payoffs alone. No model is needed. | `parity-lab` |
| `parity-for-american` | For American options parity becomes a pair of inequalities. | `parity-lab` |
| `strike-undiscounted` | The bond pays $K$ at expiry, so today it costs $Ke^{-rT}$. | `parity-lab` |
| `synthetic-without-bond` | Long call minus put equals the share minus a bond, not the share alone. | `parity-lab` |
| `last-is-price` | The last trade may be hours old. Use the current bid and ask. | `option-chain` |
| `wide-spread-fine` | A mid inside a very wide market is not a price you can trade. | `option-chain` |
| `iv-same-all-strikes` | Implied volatility varies by strike: that is the smile. | `option-chain`, `iv-solver` |
| `vol-lowers-put` | More volatility raises both calls and puts: their payoffs are convex. | `bs-explorer` |
| `n-d1-is-probability` | $N(d_2)$ is the risk-neutral exercise probability; $N(d_1)$ is delta. | `bs-explorer` |
| `price-depends-on-mu` | The stock's expected return does not appear in the formula. | `bs-explorer`, `binomial-tree` |
| `theta-always-negative` | A deep in-the-money European put can gain value as time passes. | `bs-explorer` |
| `atm-approx-uses-variance` | The shortcut uses volatility times root time: $0.4\,\sigma\sqrt{T}\,S$. | `bs-explorer` |
| `delta-is-probability` | Delta is a hedge ratio; it is close to, but not equal to, the exercise probability. | `greeks-lab` |
| `gamma-highest-deep-itm` | Gamma peaks near the strike, where the delta changes fastest. | `greeks-lab` |
| `long-option-positive-theta` | A long option loses time value; theta is the rent for gamma. | `greeks-lab` |
| `vega-highest-near-expiry` | Vega grows with the square root of time to expiry. | `greeks-lab` |
| `delta-neutral-is-riskless` | Delta-neutral still carries gamma and vega risk. | `greeks-lab` |
| `gamma-term-linear` | The gamma term grows with the square of the move. | `pnl-attribution` |
| `theta-negligible` | Theta is paid every day whether or not the stock moves. | `pnl-attribution` |
| `attribution-is-exact` | The Greeks approximate; the residual grows with the size of the move. | `pnl-attribution` |
| `iv-is-historical` | Implied volatility comes from today's option price, not past returns. | `iv-solver` |
| `iv-always-exists` | Below the no-arbitrage bound no volatility matches the price. | `iv-solver` |
| `newton-always-converges` | With tiny vega, Newton's step overshoots. Bracket and bisect. | `iv-solver` |
| `real-probability-prices` | Change the real probability: the price does not move. Only $q$ matters. | `binomial-tree` |
| `delta-is-constant` | The hedge changes at every node as the option's moneyness changes. | `binomial-tree` |
| `q-from-sigma-directly` | $q$ comes from $u$, $d$ and $r$; volatility enters through $u$ and $d$. | `binomial-tree` |
| `discount-once-at-end` | Discount one period per step, or the whole horizon once, never a mixture. | `binomial-tree` |
| `price-up-means-buyer` | Classify by where the trade printed against the quotes, then by the tick. | `tape-lab` |
| `effective-equals-quoted` | Trades inside the spread pay less than the quoted spread. | `tape-lab` |
| `roll-works-with-trend` | Roll's estimator assumes no drift or momentum in the true price. | `tape-lab` |
| `spread-is-greed` | Even a zero-cost dealer needs a spread to break even against informed traders. | `adverse-selection` |
| `quote-at-prior-mean` | A buy is evidence the value is high. Quote the ask above the prior mean. | `adverse-selection` |
| `noise-traders-lose-nothing` | Uninformed traders pay the spread; that is what funds the dealer. | `adverse-selection` |
| `wider-always-better` | Wider quotes trade less; the spread earned can fall. | `dealer-sim` |
| `inventory-is-free` | Inventory exposes the dealer to price moves; skew to shed it. | `dealer-sim` |
| `skew-wrong-way` | When long, lower both quotes so you sell more than you buy. | `dealer-sim`, `mm-game` |
| `impact-linear` | Impact grows roughly with the square root of size, not in proportion. | `execution-lab` |
| `beat-vwap-means-good` | Beating VWAP can still lose against the arrival price. | `execution-lab` |
| `splitting-always-cheaper` | Trading slowly saves impact but adds the risk of the price moving away. | `execution-lab` |
| `high-sharpe-is-skill` | A Sharpe above 2 from a simple rule is usually a bug. Look for the leak. | `backtest-lab` |
| `same-bar-fill` | You cannot trade at the close that produced your signal. | `backtest-lab` |
| `survivors-only` | Today's universe leaves out the companies that failed. | `backtest-lab` |
| `costs-negligible` | High turnover times small costs can erase the edge. | `backtest-lab`, `signal-lab` |
| `peek-at-holdout` | Every look at the held-out period makes it less held out. | `backtest-lab` |
| `annualise-wrong-root` | Monthly returns annualise with $\sqrt{12}$, not $\sqrt{252}$. | `sharpe-lab` |
| `sharpe-is-precise` | Three years of data leave a standard error near 0.6 on an annual Sharpe. | `sharpe-lab` |
| `best-of-n-is-skill` | The best of many null strategies always looks good in sample. | `sharpe-lab` |
| `autocorrelation-ignored` | Serially correlated returns make the square-root-of-time rule wrong. | `sharpe-lab` |
| `ic-too-small-to-matter` | Across hundreds of stocks and years, a small IC adds up. | `signal-lab` |
| `pearson-on-outliers` | One extreme return can drive a Pearson IC; ranks are steadier. | `signal-lab` |
| `sector-bet-as-alpha` | Part of that IC was a sector bet. Neutralise and measure again. | `signal-lab` |
| `ignore-turnover` | A signal that reshuffles every month pays costs every month. | `signal-lab` |
| `quantiles-not-checked` | A real signal's quantile returns should rise in order, not just at the ends. | `signal-lab` |
| `smile-means-mispricing` | The smile is the market's correction to the model, not an arbitrage. | `vol-surface` |
| `crossing-variance-ok` | Total variance must not fall with expiry; crossing lines are an arbitrage. | `vol-surface` |
| `moneyness-axes-confused` | A smile against strike and against delta look different; label the axis. | `vol-surface` |
| `mc-converges-like-tree` | Monte Carlo error falls like $1/\sqrt{N}$: four times the paths halves it. | `pricer-compare` |
| `more-steps-always-better` | Tree prices wobble between odd and even step counts. | `pricer-compare`, `binomial-tree` |
| `antithetic-free-lunch` | Antithetic paths help when the payoff is monotone; they can do little otherwise. | `pricer-compare` |
| `ignore-sequence` | A skipped sequence number means a missed update. Your book is now wrong. | `feed-sim` |
| `deltas-before-snapshot` | Discard updates older than the snapshot, then apply the rest in order. | `feed-sim` |
| `reconnect-without-backoff` | Reconnecting in a tight loop overloads both sides. Back off and cap. | `feed-sim` |
| `close-is-max` | The close is the last price in the bar, not the highest. | `candle-builder` |
| `boundary-tick-earlier-bar` | With left-closed bars, a tick at exactly 10:01:00 starts the next bar. | `candle-builder` |
| `rollup-from-ticks-only` | Five 1-minute bars make one 5-minute bar exactly; you do not need the ticks. | `candle-builder` |
| `local-time-bars` | Bars in local time break at daylight-saving changes. Store UTC. | `candle-builder` |
| `mean-is-enough` | The mean hides the tail. Quote p99 and p99.9. | `latency-lab` |
| `clocks-agree` | Two machines' clocks differ; one-way delay needs their offset. | `latency-lab` |
| `full-utilisation-fine` | Near full utilisation, waiting time grows without bound. | `latency-lab` |
| `cancel-is-instant` | A fill can arrive while your cancel is in flight. | `order-lifecycle` |
| `duplicate-fill-counted` | The same fill can arrive twice. Deduplicate by its id. | `order-lifecycle` |
| `trust-local-state` | After a crash, the broker's records are the truth. Reconcile. | `order-lifecycle` |
| `risk-after-send` | Risk checks run before an order leaves, not after it fills. | `order-lifecycle` |
| `indicator-predicts` | An indicator summarises past prices. Test whether it beats chance. | `paper-trader` |
| `backtest-without-costs` | Every crossing pays the spread and fees. Include them. | `paper-trader` |
| `one-path-proves` | One price path is one draw. Compare with many random strategies. | `paper-trader` |
| `hide-failures` | A results note without what failed is less credible, not more. | `results-note` |
| `metrics-without-costs` | Report metrics after costs, with the cost assumption stated. | `results-note` |
| `in-sample-only` | Report the held-out period separately. | `results-note` |
| `odds-are-probabilities` | Bookmaker odds include a margin; implied probabilities sum to more than 1. | `bet-lab` |
| `decimal-odds-exclude-stake` | Decimal odds include the returned stake. | `bet-lab` |
| `hedge-loses-ev` | At fair prices a hedge costs no expected value; at a bookmaker's it costs the margin. | `bet-lab` |
| `doubling-system-wins` | Doubling after losses does not change the expected value; it raises the risk of ruin. | `bet-lab` |
| `bet-to-max-ev` | Betting everything maximises the mean and guarantees eventual ruin. | `kelly-lab` |
| `kelly-is-safe` | Full Kelly still halves your wealth with probability about one half at some point. | `kelly-lab` |
| `kelly-on-estimated-edge` | An overestimated edge makes Kelly over-bet. Shrink the fraction. | `kelly-lab` |
| `sum-individual-kellys` | Simultaneous bets share one bankroll; optimise them together. | `kelly-lab` |
| `quote-on-guess-not-ev` | Centre the market on the expected value, not on the most likely outcome. | `mm-game` |
| `width-from-nothing` | The width should reflect the uncertainty and the risk of informed traders. | `mm-game` |
| `ignore-being-lifted` | Someone bought at your ask. Ask what they might know, and move. | `mm-game` |
| `too-tight-under-adverse` | Against informed traders, a tight market gets picked off. | `mm-game` |
| `inconsistent-linked-markets` | Your market on the sum must agree with your markets on the parts. | `mm-game` |
| `overconfident-narrow` | Your 90% intervals caught the truth 5 times in 10. Widen them. | `calibration-lab` |
| `fixed-percent-interval` | A fixed ±10% ignores how uncertain each quantity is. | `calibration-lab` |
| `linear-scale-for-magnitudes` | For quantities spanning powers of ten, set the interval on a log scale. | `calibration-lab` |
| `silent-solving` | The interviewer marks reasoning they can hear. Talk through each step. | `mock-interview`, `puzzle-workbench` |
| `answer-without-check` | Check the answer against a bound or a special case before stating it. | `mock-interview`, `puzzle-workbench` |
| `refuse-hints` | Using a hint well scores better than staying stuck. | `mock-interview` |
| `unstructured-answer` | State the plan first, then compute. | `mock-interview` |

---

## 11. Rejected alternatives and open questions

### 11.1 Rejected

| Alternative | Why not |
|---|---|
| QuantLib compiled to WebAssembly in the browser | Megabytes of WebAssembly for functions `finance-core` covers in a few hundred lines; may not run in the Artifact; CI fixtures give the same assurance |
| A third-party charting library for candles (for example TradingView's Lightweight Charts) or for depth (ECharts, Plotly) | A second rendering path without our keyboard model, ids, grading recolours or table views; the `candles` and `depth` marks are small |
| Fermi facts generated by the model at runtime | Unsourced numbers cannot grade a calibration item; the fact bank is curated with citations and dates |
| A real-time multiplayer server on the web proxy | Turns a key-holding relay into a stateful service with its own threat surface (decision 12) |
| Red and green for bids and asks, or for up and down candles | Clashes with grading colours and fails colour-blind learners (decision 15) |
| Sonifying order flow | No evidence it helps learning here; adds sound to a product whose sound is off by default |
| A volatility-trading game in Natenberg's style | Valuable for the options track, but `hedging-sim` and `pnl-attribution` cover the mechanism; deferred to a later catalogue if the owner adds options-trading depth |
| A four-suit card trading game modelled on a firm's published game | It trains inference from order flow, but it is a firm's named game; an original design would need its own rules and testing. `mm-game` multi-bot and linked modes cover the core skills |
| A Kyle (1985) model widget | Covered in text with `execution-lab`'s linear-impact setting; a dedicated widget is P2-optional if 3.1 adds the paper |
| Full FIX message syntax in `order-lifecycle` | The states teach the ideas; FIX tags would be memorisation |
| Grading mock interviews automatically | Spoken reasoning needs a human or a reviewed draft; Bertie drafts, the learner or partner confirms |

### 11.2 Open questions

| # | Question | Effect and fallback |
|---|---|---|
| 1 | Does the Artifact CSP allow WebAssembly? [unverified, probe running] | Decides whether the binomial-pricer exit drill runs in the Artifact (MicroPython) or hands off |
| 2 | Are `SpeechRecognition`, `speechSynthesis` and the microphone available inside the Artifact frame? [unverified] | If not, voice is web-only and the Artifact opens `voice-capture` in typed mode |
| 3 | Does `room` admit an invited stranger (a guest from outside the owner's organisation)? [unverified] | If not, stranger mocks use pass-and-play or the web app |
| 4 | Web interviewer turn latency at effort `low` [unverified] | A P50 above 3 seconds switches the proxy to a faster model from the current list |
| 5 | Firm-specific 80-in-8 details (negative marking, multiple choice, sequences) [unverified] | Configuration in `speed-drill`; the owner may supply first-hand reports |
| 6 | Pinned versions of SciPy and QuantLib for CI fixtures [unverified] | Fixtures regenerate when a pin moves; a content review follows |
| 7 | Default exchange rules for amends and auction tie-breaks | Proposed: a generic, labelled rule set ("typical continuous market"); the owner may prefer to model a named venue |
| 8 | Citation style for recreated interview problems | Proposed: "After Mosteller, problem 1"; owner sign-off needed |
| 9 | Who curates the Fermi and calibration fact bank, and how often it is refreshed | Proposed: 300 facts at launch, each with a source and date, reviewed yearly |
| 10 | Does the `downloads` capability accept `.py` files for starter suites? [unverified] | Fallback: offer the suite as `.txt` with instructions to rename |
| 11 | Will `sample.limits().tools.maxCount` allow `fin_eval` beside the five shared tutor tools? [unverified] | If not, `fin_eval` folds into `read_screen` results for finance screens |
| 12 | Should 1.7 unlock alongside 1.3 in the course map (decision 14)? | Owner decision; widgets are unaffected |

---

## 12. All widgets

Kinds: **primitive** (a building block, also usable alone; host, control or input) and **composite**.

| # | Id | Kind | Priority | Wave | Curriculum items |
|---|---|---|---|---|---|
| 1 | `price-ladder` | primitive (host) | P1 | G1 | 1.7.4, 1.7.9; 2.3.4, 2.3.5; 3.3.4 |
| 2 | `cashflow-timeline` | primitive (host) | P1 | G1 | 1.7.1, 1.7.3, 1.7.5, 1.7.6 |
| 3 | `position-editor` | primitive (control) | P1 | G2 | 1.7.5 to 1.7.8; 2.3.3 |
| 4 | `order-ticket` | primitive (input) | P1 | G1 | 1.7.4, 1.7.9; 2.3.5 |
| 5 | `quote-entry` | primitive (input) | P1 | G3 | 1.7.9; 3.3.4 |
| 6 | `voice-capture` | primitive (control) | P1 | G1 | 1.7.4 (exit rehearsal); 3.3.2, 3.3.4, 3.3.5 |
| 7 | `scratch-pad` | primitive (control) | P0 | D4 | weekly problems from 1.5; 3.3.2, 3.3.5; long-form homework |
| 8 | `compounding-lab` | composite | P1 | G1 | 1.7.1 |
| 9 | `tvm-timeline` | composite | P1 | G1 | 1.7.1 |
| 10 | `share-lab` | composite | P1 | G1 | 1.7.2 |
| 11 | `margin-lab` | composite | P1 | G1 | 1.7.2, 1.7.5 |
| 12 | `portfolio-lab` | composite | P1 | G1 | 1.7.2 |
| 13 | `bond-lab` | composite | P1 | G1 | 1.7.3 |
| 14 | `yield-curve-lab` | composite | P1 | G1 | 1.7.3; 2.3.3 |
| 15 | `duration-lab` | composite | P1 | G1 | 1.7.3 |
| 16 | `order-book` | composite | P1 | G1 | 1.7.4 (exit), 1.7.9; 3.3.4 |
| 17 | `auction-lab` | composite | P1 | G1 | 1.7.4 |
| 18 | `carry-arb` | composite | P1 | G2 | 1.7.5, 1.7.6 |
| 19 | `futures-mtm` | composite | P1 | G2 | 1.7.5 |
| 20 | `hedge-lab` | composite | P1 | G2 | 1.7.5 |
| 21 | `payoff-builder` | composite | P1 | G2 | 1.7.5, 1.7.6, 1.7.8; 2.3.3; 3.3.3 |
| 22 | `option-bounds` | composite | P1 | G2 | 1.7.6; 2.3.3 |
| 23 | `parity-lab` | composite | P1 | G2 | 1.7.6 (exit); 2.3.3 |
| 24 | `option-chain` | composite | P1 (P2 modes) | G2 | 1.7.6, 1.7.8; 2.3.3 |
| 25 | `bs-explorer` | composite | P1 | G3 | 1.7.8; 2.3.3; 3.3.1 |
| 26 | `greeks-lab` | composite | P1 (P2 surface) | G3 | 1.7.8; 2.3.3 |
| 27 | `pnl-attribution` | composite | P1 | G3 | 1.7.8; 3.3.5 |
| 28 | `iv-solver` | composite | P1 (P2 algorithm) | G3 | 1.7.8; 2.3.3 |
| 29 | `tape-lab` | composite | P1 | G3 | 1.7.9; 2.3.4 |
| 30 | `adverse-selection` | composite | P1 | G3 | 1.7.9; 3.3.4 |
| 31 | `dealer-sim` | composite | P1 (P2 Avellaneda-Stoikov) | G3 | 1.7.9; 3.3.4; 3.1 |
| 32 | `execution-lab` | composite | P1 (P2 frontier) | G3 | 1.7.9; 2.3.1, 2.3.2 |
| 33 | `backtest-lab` | composite | P2 | H | 2.3.0, 2.3.1, 2.3.2, 2.3.5 |
| 34 | `sharpe-lab` | composite | P2 | H | 2.3.1, 2.3.2; 3.1 |
| 35 | `signal-lab` | composite | P2 | H | 2.3.2; 3.1 |
| 36 | `vol-surface` | composite | P2 | H | 2.3.3 |
| 37 | `pricer-compare` | composite | P2 | H | 2.3.3; 1.9 |
| 38 | `feed-sim` | composite | P2 | H | 2.3.4; 2.4 |
| 39 | `candle-builder` | composite | P2 | H | 2.3.4 |
| 40 | `latency-lab` | composite | P2 | H | 2.3.4; 1.9 |
| 41 | `order-lifecycle` | composite | P2 | H | 2.3.5, 2.3.1 |
| 42 | `paper-trader` | composite | P2 | H | 2.3.5 |
| 43 | `results-note` | composite | P2 | H | 2.3 all; 3.1 |
| 44 | `puzzle-workbench` | composite | P0 core (P2 cold and aloud) | D4, J | 1.5 onwards (weekly); 3.3.2, 3.3.5 |
| 45 | `bet-lab` | composite | P2 | J | 3.3.3 |
| 46 | `kelly-lab` | composite | P2 | J | 3.3.3; 2.3.1 |
| 47 | `mm-game` | composite | P2 | J | 3.3.4, 3.3.5 |
| 48 | `calibration-lab` | composite | P2 | J | 3.3.4 |
| 49 | `mock-interview` | composite | P2 | J | 3.3.5 (exit) |

**Counts:** 7 primitives and 42 composites, 49 in all. P0: 2 (`scratch-pad`, `puzzle-workbench` core). P1: 31 (6 primitives, 25 composites). P2: 16 (11 project composites, 5 interview composites). 40 composites need seeded generators.

**Owned elsewhere, extended here (section 5):** 23 widgets, among them `binomial-tree`, whose ownership moves to this catalogue (P1, G3). Shared primitives with additions (section 4): `marks`, `plot-2d`, `slider`, `number-line`, `value-table`, `sim-runner`, `region-select`, `stepper`, `speed-timer`.

---

## 13. Cross-cluster needs

### 13.1 Primitives from this catalogue that other clusters will need

1. **`scratch-pad`**: every long-form homework item in every topic; derivations worked by hand before `derivation-steps` checks them; probability problems from 1.5.
2. **`voice-capture`**: any "explain aloud" item (the 1.6 exit asks the learner to explain every number in a statsmodels table; the 2.1 exit asks for leakage and the bias-variance trade-off without notes); oral items in topic exams.
3. **`cashflow-timeline`**: 0.3 annuities and geometric series, 1.3 series (`series-explorer`'s annuity preset).
4. **`order-ticket` and `price-ladder`**: 2.4 trading competitions (IMC Prosperity style) on the trader track; 3.1 Avellaneda and Stoikov.
5. **`quote-entry`**: any interval or two-sided estimate (1.6 confidence intervals as markets, in an optional ladder step).
6. **`position-editor`**: portfolio construction items in 2.1 (weights with constraints) if the machine-learning cluster wants a discrete-leg editor beside `mass-editor`.
7. **The `waterfall` and `signed-fill` marks**: feature attribution in 2.1 (contributions summing to a prediction); variance decompositions in 1.6.
8. **The `blotter` and `chain` presets of `value-table`**: 2.4 and 3.1 replications.

### 13.2 Composites from this catalogue that other clusters should reuse rather than rebuild

| Composite | Other uses |
|---|---|
| `puzzle-workbench` | the weekly probability problems (1.5, probability cluster); 1.8 maths-flavoured problems before coding; 2.4 Project Euler reasoning before code |
| `results-note` | 3.1 replication notes; 2.1 end-to-end project write-up |
| `backtest-lab` | 2.1 time-ordered validation (held-out and walk-forward modes); 3.1 out-of-sample extensions |
| `sharpe-lab` | 3.1 Harvey, Liu and Zhu (multiple testing in factor research); 1.6 standard errors of estimators |
| `signal-lab` | 3.1 Jegadeesh and Titman, Fama and French replications |
| `adverse-selection` | 1.5 Bayes' rule transfer screens |
| `kelly-lab` | 1.5 betting preview through `game-lab` |
| `calibration-lab` | 1.6 what a confidence interval promises; 0.1 estimation |
| `latency-lab` | 1.9 performance measurement beyond `bench-lab` |
| `mock-interview` | the developer track's coding rounds, with the programming cluster's `problem-workbench` embedded |
| `dealer-sim` | 3.1 Avellaneda and Stoikov replication |

### 13.3 What this catalogue needs from other clusters

| Need | Owner | Used in |
|---|---|---|
| `rational`, `dist`, exact enumeration services; `mass-editor`; `chance-object`; linked mode in ten probability composites | probability cluster | `mm-game`, `bet-lab`, `kelly-lab`, `puzzle-workbench`, `execution-lab`, `portfolio-lab` |
| `price-series` service; `code-cell` with the finance prelude; `setup-checklist` project mode; `node-link` state machines; `json-explorer`; `schema-builder`; the trace recorder (for `binomial-tree` vector mode) | programming cluster | 1.7.7, all of 2.3 |
| `sketch-pad` piecewise-linear mode; `plot-3d`; `gbm-lab` 1.7 mode; `hedging-sim` one-path mode | calculus and linear algebra cluster | 1.7.6, 1.7.8, 2.3.3 |
| `speed-drill` decks and 80-in-8 options; `fermi-estimator` export; `free-response` voice and rubric modes | Stage 0 | 3.3.1, 3.3.4, 1.7.4 exit |
| Bertie's interviewer expression set; the mascot's speaking state; `room` integration; the `speech` service; `downloads` for suites and notes; the five tutor tools plus `fin_eval` | engine and tutor blueprint | 3.3.5, 3.3.4, 2.3 |
| A purged, time-ordered cross-validation splitter | machine-learning cluster (2.1) | `backtest-lab` walk-forward mode |
