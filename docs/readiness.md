# Readiness contract

Signed off by the user, 5 Nov (PLAN 2c item 2; DECISIONS "Readiness contract sign-off"). Answers in DECISIONS "Readiness contract answers (user, 5 Nov)" are binding here.

## What this contract says

- The app is not a credential. It builds skill; it does not certify it.
- No total in this file is evidence of readiness. Hours and lesson counts measure work offered, not skill shown.
- A role reads "ready" only when all three hold: every mock listed for the role exists, the learner has passed each one, and an external capstone record exists. The reviewer is the user. A learner's own review never counts.
- A role with a gap mock below cannot read "ready" yet, however much else is done.
- Learn header: one total per role, required plus recommended, with written and unwritten lessons stated separately. Undecided shows the shared foundation.
- Employer formats change and differ by office. Treat the tasks below as planning targets, not hiring requirements.

Status words: **required** is shown as next work in order. **Recommended** is shown after required. **Optional** is never shown as next work for the role; it stays reachable from Learn.

<!-- generated:catalogue -->
Catalogue: 79 courses, 1214 lessons mapped (1214 written, 0 unwritten). Hours are shown as hours in the app and hours of outside study: the stored topic hours, shared across a topic's courses by lesson weight (js/hours.js; a short lesson weighs 1), split into the minutes counted in the app (lessons, level reviews and homework, topic exams) and the rest; topics 3.2 and 3.4 store 0.
<!-- /generated -->

Hours come from `app/js/hours.js` (AUTHORING section 14): a short lesson weighs 1 and a workshop or project `minutes / 14`. Each table gives hours in the app (lesson minutes, level reviews and homework, topic exams) and hours of outside study (stored hours less the in-app figure, never below 0), in that order; no table shows the stored total alone. Hours in each table are rounded per cell, and the header is the sum of the cells. Run `node app/tools/readiness-sums.mjs` from the repo root to check every figure here. It exits non-zero on any mismatch.

Derivatives and desk quant is a sub-route of Strats, not its own track. Its table sits inside the Strats section.

## Trader

Plan: probability, numeracy, uncertainty, communication and games first. Machine learning, PDEs and abstract algebra can wait.

**Independent tasks that count** (each done alone, on material the learner has not seen)

1. Price an unseen expected-value or betting game aloud in 3 minutes, with no paper. Evidence: drill in `mm-games` and `puzzles`, then a spoken mock with a stranger (external).
2. Score 50 or more on Zetamac default settings and clear the timed arithmetic mock. Evidence: `mock-oa-arith` and a dated Zetamac screenshot (external).
3. Make a two-sided market on an unknown quantity and update it as trades arrive, aloud with a partner. Evidence: external mock with written feedback.
4. Solve an unseen conditional-probability problem cold in 5 minutes and defend the assumptions. Evidence: `mock-oa-trader` versions 2 and 3, which are unseen until sat.
5. Pass the timed trader and SIG batteries at their marks. Evidence: `mock-oa-trader` and `mock-oa-sig`.
6. Complete three mock interviews with a stranger, each marked on reasoning as well as answers. Evidence: external record; `mock-superday-trader` for rehearsal.

**Course classification**

| Course | Stage | Status | Reason |
| --- | --- | --- | --- |
| `algebra` | 3 | optional | Abstract algebra. Not asked in trader screens; can wait. |
| `algo-think` | 1 | recommended | Complexity, recursion and sorting. User decision: recommended. |
| `alpha` | 2 | optional | Alpha research project. Not asked in trader screens; can wait. |
| `analysis` | 1 | optional | Real analysis. Not asked in trader screens; can wait. |
| `arma` | 2 | optional | ARMA time series. Not asked in trader screens; can wait. |
| `backtest` | 2 | optional | Backtesting project. Not asked in trader screens; can wait. |
| `brainteasers` | 3 | required | Logic puzzles and brainteasers. Reported in most trader screens. |
| `coding-int` | 3 | optional | Coding interview patterns. Not asked in trader screens; can wait. |
| `coint` | 2 | optional | Cointegration. Not asked in trader screens; can wait. |
| `complex` | 1 | optional | Complex numbers. Not asked in trader screens; can wait. |
| `conditional` | 1 | required | Conditioning, Bayes and independence. Core trader screen content. |
| `contests` | 2 | optional | Contest-style problem solving. User decision: optional. |
| `convex` | 2 | optional | Convex optimisation. Not asked in trader screens; can wait. |
| `counting` | 0 | required | Permutations, combinations and sums. Core trader screen content. |
| `counting-chance` | 1 | required | Counting arguments in probability. Core trader screen content. |
| `cpp` | 1 | optional | C++ memory, the standard library and tests. Not asked in trader screens; can wait. |
| `cpp-pricing` | 1 | optional | Pricing and low-latency C++. Not asked in trader screens; can wait. |
| `ds` | 1 | recommended | Hash maps, trees, heaps and stacks. User decision: recommended. |
| `eigen` | 1 | optional | Eigenvalues, SVD and PCA. Not asked in trader screens; can wait. |
| `elimination` | 1 | recommended | Elimination and solving systems. Helps a trader screen; not a first gate. |
| `ensembles` | 2 | optional | Trees, boosting and ensembles. Not asked in trader screens; can wait. |
| `equations` | 0 | required | Solving equations and inequalities. Core trader screen content. |
| `estimation` | 1 | recommended | Estimators and confidence intervals. Helps a trader screen; not a first gate. |
| `exp-log` | 0 | required | Exponentials and logarithms. Core trader screen content. |
| `fin-ml` | 2 | optional | Machine learning on financial data. Not asked in trader screens; can wait. |
| `first-python` | 0 | required | First programs in Python. Core trader screen content. |
| `functions` | 0 | required | Functions and graphs. Core trader screen content. |
| `game-theory` | 3 | required | Games, auctions and poker. Core trader screen content. |
| `garch` | 2 | optional | Volatility models. Not asked in trader screens; can wait. |
| `git` | 1 | optional | Version control. Not asked in trader screens; can wait. |
| `graphs-dp` | 1 | optional | Graph search and dynamic programming. User decision: optional. |
| `integrals` | 1 | required | Integration techniques. User decision: required. |
| `ito` | 3 | optional | Brownian motion and Itô calculus. Not asked in trader screens; can wait. |
| `least-squares` | 1 | recommended | Projections and least squares. Helps a trader screen; not a first gate. |
| `limits` | 1 | required | Limits and derivatives. Core trader screen content. |
| `limits-thm` | 1 | required | Named distributions, LLN and CLT. Core trader screen content. |
| `linear-maps` | 1 | optional | Proof-based linear algebra. Not asked in trader screens; can wait. |
| `markets` | 1 | recommended | How markets and orders work. Finance basics: recommended for traders. |
| `markov` | 1 | required | Markov chains, random walks and martingales. Ruin, walks and martingale questions. |
| `measure-prob` | 3 | optional | Measure-theoretic probability. Not asked in trader screens; can wait. |
| `mental` | 0 | required | Daily mental arithmetic. Core trader screen content. |
| `mental-pressure` | 3 | required | Speed and accuracy under pressure. Timed arithmetic and speed drills for the OA. |
| `micro` | 1 | recommended | Market microstructure and the order book. Finance basics: recommended for traders. |
| `mm-games` | 3 | required | Market-making and betting games. Market-making games are the trader final round. |
| `momentum-rep` | 3 | optional | Replication of a momentum paper. Not asked in trader screens; can wait. |
| `multivar` | 1 | required | Partial derivatives and constrained optimisation. User decision: required. |
| `number-sense` | 0 | required | Fractions, decimals, negatives and powers. Core trader screen content. |
| `numerics` | 2 | optional | Numerical methods. Not asked in trader screens; can wait. |
| `numpy-pandas` | 1 | recommended | Arrays and DataFrames. Helps a trader screen; not a first gate. |
| `odes` | 1 | optional | Ordinary differential equations. Not asked in trader screens; can wait. |
| `opt-dash` | 2 | optional | Optimiser and dashboard project. Not asked in trader screens; can wait. |
| `options` | 1 | recommended | Options, payoffs and parity. Finance basics: recommended for traders. |
| `pairs-rep` | 3 | optional | Replication of a pairs-trading paper. Not asked in trader screens; can wait. |
| `pdes` | 3 | optional | PDEs and the Black-Scholes equation. Not asked in trader screens; can wait. |
| `plotting` | 1 | optional | Plotting with matplotlib. Not asked in trader screens; can wait. |
| `proof` | 0 | optional | Reasoning and proof. Pure maths; not tested at interview. |
| `puzzles` | 3 | required | Interview probability problems. Trader interview probability: the core of the screen. |
| `py-found` | 1 | recommended | Fluent Python: lists, classes, sorting. Helps a trader screen; not a first gate. |
| `pytest` | 1 | optional | Testing code. Not asked in trader screens; can wait. |
| `quadratics` | 0 | required | Quadratics and factorising. Core trader screen content. |
| `random-vars` | 1 | required | Expectation, variance and distributions. Core trader screen content. |
| `ratio` | 0 | required | Ratio, percentages and rates. Core trader screen content. |
| `recruiting` | 0 | required | Roles, firms and the hiring calendar. Core trader screen content. |
| `regression` | 1 | recommended | Linear regression and its failures. Helps a trader screen; not a first gate. |
| `research-int` | 3 | optional | Research interview cases and take-homes. Not asked in trader screens; can wait. |
| `series` | 0 | required | Sequences, series and the binomial theorem. Core trader screen content. |
| `sql` | 1 | optional | SQL for data tasks. Not asked in trader screens; can wait. |
| `stat-learning` | 2 | optional | Supervised learning and ISLR methods. Not asked in trader screens; can wait. |
| `stat-models` | 2 | optional | Generalised linear models and Bayesian inference. Not asked in trader screens; can wait. |
| `systems` | 3 | optional | Caches, threads, sockets and design. Not asked in trader screens; can wait. |
| `taylor` | 1 | recommended | Taylor series and approximation. Helps a trader screen; not a first gate. |
| `terminal` | 0 | required | The terminal and files. Core trader screen content. |
| `testing` | 1 | recommended | Hypothesis tests and multiple testing. Helps a trader screen; not a first gate. |
| `topology` | 3 | optional | Metric and topological spaces. Not asked in trader screens; can wait. |
| `trees` | 1 | recommended | Binomial trees and Black-Scholes. Finance basics: recommended for traders. |
| `trig` | 0 | required | Trigonometry. Core trader screen content. |
| `validation` | 2 | optional | Cross-validation and leakage. Not asked in trader screens; can wait. |
| `vector-calc` | 1 | optional | Vector calculus. Not asked in trader screens; can wait. |
| `vectors` | 1 | required | Vectors and matrices. Core trader screen content. |

**Mocks**

| Mock | Status | Note |
| --- | --- | --- |
| `mock-oa-arith` | exists |  |
| `mock-oa-trader` | exists |  |
| `mock-oa-trader-2` | exists | version of mock-oa-trader |
| `mock-oa-trader-3` | exists | version of mock-oa-trader |
| `mock-oa-sig` | exists |  |
| `mock-oa-sig-2` | exists | version of mock-oa-sig |
| `mock-oa-sig-3` | exists | version of mock-oa-sig |
| `mock-superday-trader` | exists |  |

**Capstone:** a spoken mock-interview record with a named human reviewer (the user), date, format, and written notes on the reasoning shown. Not yet built (PLAN 2c item 8).

**Totals**

<!-- generated:totals:trader -->
| Set | Lessons written | Lessons unwritten | Lessons total | Hours in the app | Hours of outside study |
| --- | --- | --- | --- | --- | --- |
| Required | 442 | 0 | 442 | 247 | 967 |
| Recommended | 188 | 0 | 188 | 99 | 491 |
| Learn header (required plus recommended) | 630 | 0 | 630 | 346 | 1458 |
<!-- /generated -->

**Dependency conflicts**

Acceptance check: a fresh trader profile is never shown `graphs-dp` as next work. It is optional here, so Today must skip it. The conflicts below are the edges that still pull it in; PLAN 2c item 7 must cut or replace each one.

<!-- generated:conflicts:trader -->
| From (required or recommended) | Optional course reached | Edge or route |
| --- | --- | --- |
| `brainteasers` | `contests` | L3 needs contests/L2 |
| `brainteasers` | `graphs-dp` | via `contests` |

Required courses that need a recommended course: `game-theory` needs `micro`; `mm-games` needs `micro`, `options`; `puzzles` needs `estimation`.
<!-- /generated -->

## Researcher

Plan: probability, statistics, linear algebra, Python, validation and independent data analysis. Low-latency C++ and contest work can wait.

**Independent tasks that count** (each done alone, on material the learner has not seen)

1. Analyse an unfamiliar dataset in 60 minutes and state a defensible conclusion with its limits. Evidence: `mock-oa-quant-data`.
2. Solve an unseen probability or statistics question and explain every assumption aloud. Evidence: `mock-superday-research` and an external spoken mock.
3. Fit and validate a model out of sample on data you have not seen, and report what failed. Evidence: external take-home reviewed by the user.
4. Work an open prediction case aloud in 45 minutes. Evidence: `mock-superday-research` and an external spoken mock.
5. Solve two medium coding problems in 60 minutes. Evidence: `mock-oa-code`.
6. Replicate a published result from a clean checkout, with an out-of-sample extension and defence notes. Evidence: external capstone.

**Course classification**

| Course | Stage | Status | Reason |
| --- | --- | --- | --- |
| `algebra` | 3 | optional | Abstract algebra. Not needed for research screens; can wait. |
| `algo-think` | 1 | recommended | Complexity, recursion and sorting. Strengthens a research profile; not a first gate. |
| `alpha` | 2 | recommended | Alpha research project. Strengthens a research profile; not a first gate. |
| `analysis` | 1 | optional | Real analysis. Not needed for research screens; can wait. |
| `arma` | 2 | recommended | ARMA time series. Strengthens a research profile; not a first gate. |
| `backtest` | 2 | recommended | Backtesting project. Strengthens a research profile; not a first gate. |
| `brainteasers` | 3 | optional | Logic puzzles and brainteasers. Not needed for research screens; can wait. |
| `coding-int` | 3 | recommended | Coding interview patterns. Coding part of every research screen. |
| `coint` | 2 | recommended | Cointegration. Strengthens a research profile; not a first gate. |
| `complex` | 1 | optional | Complex numbers. Not needed for research screens; can wait. |
| `conditional` | 1 | required | Conditioning, Bayes and independence. Core researcher content. |
| `contests` | 2 | optional | Contest-style problem solving. Not needed for research screens; can wait. |
| `convex` | 2 | recommended | Convex optimisation. Strengthens a research profile; not a first gate. |
| `counting` | 0 | required | Permutations, combinations and sums. Core researcher content. |
| `counting-chance` | 1 | required | Counting arguments in probability. Core researcher content. |
| `cpp` | 1 | optional | C++ memory, the standard library and tests. Not needed for research screens; can wait. |
| `cpp-pricing` | 1 | optional | Pricing and low-latency C++. Not needed for research screens; can wait. |
| `ds` | 1 | recommended | Hash maps, trees, heaps and stacks. Strengthens a research profile; not a first gate. |
| `eigen` | 1 | required | Eigenvalues, SVD and PCA. Core researcher content. |
| `elimination` | 1 | required | Elimination and solving systems. Core researcher content. |
| `ensembles` | 2 | required | Trees, boosting and ensembles. Core researcher content. |
| `equations` | 0 | required | Solving equations and inequalities. Core researcher content. |
| `estimation` | 1 | required | Estimators and confidence intervals. Core researcher content. |
| `exp-log` | 0 | required | Exponentials and logarithms. Core researcher content. |
| `fin-ml` | 2 | required | Machine learning on financial data. Core researcher content. |
| `first-python` | 0 | required | First programs in Python. Core researcher content. |
| `functions` | 0 | required | Functions and graphs. Core researcher content. |
| `game-theory` | 3 | optional | Games, auctions and poker. Not needed for research screens; can wait. |
| `garch` | 2 | optional | Volatility models. Not needed for research screens; can wait. |
| `git` | 1 | recommended | Version control. Strengthens a research profile; not a first gate. |
| `graphs-dp` | 1 | recommended | Graph search and dynamic programming. Coding screens draw on it; contests stay optional. |
| `integrals` | 1 | required | Integration techniques. Core researcher content. |
| `ito` | 3 | optional | Brownian motion and Itô calculus. Not needed for research screens; can wait. |
| `least-squares` | 1 | required | Projections and least squares. Core researcher content. |
| `limits` | 1 | required | Limits and derivatives. Core researcher content. |
| `limits-thm` | 1 | required | Named distributions, LLN and CLT. Core researcher content. |
| `linear-maps` | 1 | optional | Proof-based linear algebra. Not needed for research screens; can wait. |
| `markets` | 1 | recommended | How markets and orders work. Finance basics: recommended for researchers. |
| `markov` | 1 | required | Markov chains, random walks and martingales. Core researcher content. |
| `measure-prob` | 3 | optional | Measure-theoretic probability. Not needed for research screens; can wait. |
| `mental` | 0 | recommended | Daily mental arithmetic. Strengthens a research profile; not a first gate. |
| `mental-pressure` | 3 | optional | Speed and accuracy under pressure. Not needed for research screens; can wait. |
| `micro` | 1 | recommended | Market microstructure and the order book. Finance basics: recommended for researchers. |
| `mm-games` | 3 | optional | Market-making and betting games. Not needed for research screens; can wait. |
| `momentum-rep` | 3 | required | Replication of a momentum paper. Replication capstone route. |
| `multivar` | 1 | required | Partial derivatives and constrained optimisation. Core researcher content. |
| `number-sense` | 0 | required | Fractions, decimals, negatives and powers. Core researcher content. |
| `numerics` | 2 | recommended | Numerical methods. Strengthens a research profile; not a first gate. |
| `numpy-pandas` | 1 | required | Arrays and DataFrames. Core researcher content. |
| `odes` | 1 | optional | Ordinary differential equations. Not needed for research screens; can wait. |
| `opt-dash` | 2 | optional | Optimiser and dashboard project. Not needed for research screens; can wait. |
| `options` | 1 | recommended | Options, payoffs and parity. Finance basics: recommended for researchers. |
| `pairs-rep` | 3 | recommended | Replication of a pairs-trading paper. Second replication option; needs backtesting. |
| `pdes` | 3 | optional | PDEs and the Black-Scholes equation. Not needed for research screens; can wait. |
| `plotting` | 1 | recommended | Plotting with matplotlib. Strengthens a research profile; not a first gate. |
| `proof` | 0 | optional | Reasoning and proof. Pure maths; not tested at interview. |
| `puzzles` | 3 | recommended | Interview probability problems. Strengthens a research profile; not a first gate. |
| `py-found` | 1 | required | Fluent Python: lists, classes, sorting. Core researcher content. |
| `pytest` | 1 | recommended | Testing code. Strengthens a research profile; not a first gate. |
| `quadratics` | 0 | required | Quadratics and factorising. Core researcher content. |
| `random-vars` | 1 | required | Expectation, variance and distributions. Core researcher content. |
| `ratio` | 0 | required | Ratio, percentages and rates. Core researcher content. |
| `recruiting` | 0 | recommended | Roles, firms and the hiring calendar. Strengthens a research profile; not a first gate. |
| `regression` | 1 | required | Linear regression and its failures. Core researcher content. |
| `research-int` | 3 | required | Research interview cases and take-homes. Open cases, data tasks and take-homes. |
| `series` | 0 | required | Sequences, series and the binomial theorem. Core researcher content. |
| `sql` | 1 | required | SQL for data tasks. Core researcher content. |
| `stat-learning` | 2 | required | Supervised learning and ISLR methods. Core researcher content. |
| `stat-models` | 2 | recommended | Generalised linear models and Bayesian inference. Strengthens a research profile; not a first gate. |
| `systems` | 3 | optional | Caches, threads, sockets and design. Not needed for research screens; can wait. |
| `taylor` | 1 | required | Taylor series and approximation. Core researcher content. |
| `terminal` | 0 | required | The terminal and files. Core researcher content. |
| `testing` | 1 | required | Hypothesis tests and multiple testing. Core researcher content. |
| `topology` | 3 | optional | Metric and topological spaces. Not needed for research screens; can wait. |
| `trees` | 1 | recommended | Binomial trees and Black-Scholes. Finance basics: recommended for researchers. |
| `trig` | 0 | required | Trigonometry. Core researcher content. |
| `validation` | 2 | required | Cross-validation and leakage. Core researcher content. |
| `vector-calc` | 1 | optional | Vector calculus. Not needed for research screens; can wait. |
| `vectors` | 1 | required | Vectors and matrices. Core researcher content. |

**Mocks**

| Mock | Status | Note |
| --- | --- | --- |
| `mock-oa-code` | exists |  |
| `mock-oa-quant-data` | exists |  |
| `mock-superday-research` | exists |  |
| `mock-video` | exists | behavioural and spoken video mock |

**Capstone:** one replication (`momentum-rep` or an equivalent external project) with repo link, rerun-from-clean result and defence notes, reviewed by the user.

**Totals**

<!-- generated:totals:researcher -->
| Set | Lessons written | Lessons unwritten | Lessons total | Hours in the app | Hours of outside study |
| --- | --- | --- | --- | --- | --- |
| Required | 534 | 0 | 534 | 305 | 1348 |
| Recommended | 340 | 0 | 340 | 175 | 932 |
| Learn header (required plus recommended) | 874 | 0 | 874 | 480 | 2280 |
<!-- /generated -->

**Dependency conflicts**

<!-- generated:conflicts:researcher -->
| From (required or recommended) | Optional course reached | Edge or route |
| --- | --- | --- |
| `numerics` | `cpp-pricing` | L1 needs cpp-pricing/L1 |
| `numerics` | `odes` | L3 needs odes/L4 |
| `numerics` | `opt-dash` | L4 needs opt-dash/L2 |
| `numerics` | `complex` | via `odes` |
| `numerics` | `cpp` | via `cpp-pricing` |

Required courses that need a recommended course: `momentum-rep` needs `backtest`.
<!-- /generated -->

## Developer

Plan: programming, algorithms, C++, systems and debugging. Broad stochastic calculus and paper replication can wait.

**Independent tasks that count** (each done alone, on material the learner has not seen)

1. Solve two to four unseen algorithm problems against the clock, in Python or C++. Evidence: `mock-oa-code` and `mock-oa-code-hard`.
2. Debug and profile a native C++ program you did not write. Evidence: external exercise reviewed by the user.
3. Extend existing code live while requirements change. Evidence: `mock-superday-developer` and an external live session.
4. Defend a feed handler design aloud, including memory and threading choices. Evidence: external spoken review.
5. Implement a C++ class with moves and a rule of five against hidden tests. Evidence: `cpp` level 5 drill and review.
6. Ship an independent systems project that builds and passes tests from a clean clone. Evidence: external capstone.

**Course classification**

| Course | Stage | Status | Reason |
| --- | --- | --- | --- |
| `algebra` | 3 | optional | Abstract algebra. Not needed for developer rounds; can wait. |
| `algo-think` | 1 | required | Complexity, recursion and sorting. Core developer content. |
| `alpha` | 2 | optional | Alpha research project. Not needed for developer rounds; can wait. |
| `analysis` | 1 | optional | Real analysis. Not needed for developer rounds; can wait. |
| `arma` | 2 | optional | ARMA time series. Not needed for developer rounds; can wait. |
| `backtest` | 2 | optional | Backtesting project. Not needed for developer rounds; can wait. |
| `brainteasers` | 3 | optional | Logic puzzles and brainteasers. Not needed for developer rounds; can wait. |
| `coding-int` | 3 | required | Coding interview patterns. Core developer content. |
| `coint` | 2 | optional | Cointegration. Not needed for developer rounds; can wait. |
| `complex` | 1 | optional | Complex numbers. Not needed for developer rounds; can wait. |
| `conditional` | 1 | recommended | Conditioning, Bayes and independence. Supports developer rounds; not a first gate. |
| `contests` | 2 | recommended | Contest-style problem solving. Contest practice counts most for developers. |
| `convex` | 2 | optional | Convex optimisation. Not needed for developer rounds; can wait. |
| `counting` | 0 | recommended | Permutations, combinations and sums. Supports developer rounds; not a first gate. |
| `counting-chance` | 1 | recommended | Counting arguments in probability. Supports developer rounds; not a first gate. |
| `cpp` | 1 | required | C++ memory, the standard library and tests. Core developer content. |
| `cpp-pricing` | 1 | recommended | Pricing and low-latency C++. Needed for systems; pulls in trees (see conflicts). |
| `ds` | 1 | required | Hash maps, trees, heaps and stacks. Core developer content. |
| `eigen` | 1 | optional | Eigenvalues, SVD and PCA. Not needed for developer rounds; can wait. |
| `elimination` | 1 | optional | Elimination and solving systems. Not needed for developer rounds; can wait. |
| `ensembles` | 2 | optional | Trees, boosting and ensembles. Not needed for developer rounds; can wait. |
| `equations` | 0 | recommended | Solving equations and inequalities. Supports developer rounds; not a first gate. |
| `estimation` | 1 | optional | Estimators and confidence intervals. Not needed for developer rounds; can wait. |
| `exp-log` | 0 | required | Exponentials and logarithms. Core developer content. |
| `fin-ml` | 2 | optional | Machine learning on financial data. Not needed for developer rounds; can wait. |
| `first-python` | 0 | required | First programs in Python. Core developer content. |
| `functions` | 0 | recommended | Functions and graphs. Supports developer rounds; not a first gate. |
| `game-theory` | 3 | optional | Games, auctions and poker. Not needed for developer rounds; can wait. |
| `garch` | 2 | optional | Volatility models. Not needed for developer rounds; can wait. |
| `git` | 1 | required | Version control. Core developer content. |
| `graphs-dp` | 1 | required | Graph search and dynamic programming. Reported often in live coding rounds. |
| `integrals` | 1 | optional | Integration techniques. Not needed for developer rounds; can wait. |
| `ito` | 3 | optional | Brownian motion and Itô calculus. Not needed for developer rounds; can wait. |
| `least-squares` | 1 | optional | Projections and least squares. Not needed for developer rounds; can wait. |
| `limits` | 1 | optional | Limits and derivatives. Not needed for developer rounds; can wait. |
| `limits-thm` | 1 | optional | Named distributions, LLN and CLT. Not needed for developer rounds; can wait. |
| `linear-maps` | 1 | optional | Proof-based linear algebra. Not needed for developer rounds; can wait. |
| `markets` | 1 | recommended | How markets and orders work. Supports developer rounds; not a first gate. |
| `markov` | 1 | optional | Markov chains, random walks and martingales. Not needed for developer rounds; can wait. |
| `measure-prob` | 3 | optional | Measure-theoretic probability. Not needed for developer rounds; can wait. |
| `mental` | 0 | recommended | Daily mental arithmetic. Supports developer rounds; not a first gate. |
| `mental-pressure` | 3 | optional | Speed and accuracy under pressure. Not needed for developer rounds; can wait. |
| `micro` | 1 | recommended | Market microstructure and the order book. Supports developer rounds; not a first gate. |
| `mm-games` | 3 | optional | Market-making and betting games. Not needed for developer rounds; can wait. |
| `momentum-rep` | 3 | optional | Replication of a momentum paper. Not needed for developer rounds; can wait. |
| `multivar` | 1 | optional | Partial derivatives and constrained optimisation. Not needed for developer rounds; can wait. |
| `number-sense` | 0 | required | Fractions, decimals, negatives and powers. Core developer content. |
| `numerics` | 2 | optional | Numerical methods. Not needed for developer rounds; can wait. |
| `numpy-pandas` | 1 | recommended | Arrays and DataFrames. Supports developer rounds; not a first gate. |
| `odes` | 1 | optional | Ordinary differential equations. Not needed for developer rounds; can wait. |
| `opt-dash` | 2 | optional | Optimiser and dashboard project. Not needed for developer rounds; can wait. |
| `options` | 1 | optional | Options, payoffs and parity. Not needed for developer rounds; can wait. |
| `pairs-rep` | 3 | optional | Replication of a pairs-trading paper. Not needed for developer rounds; can wait. |
| `pdes` | 3 | optional | PDEs and the Black-Scholes equation. Not needed for developer rounds; can wait. |
| `plotting` | 1 | recommended | Plotting with matplotlib. Supports developer rounds; not a first gate. |
| `proof` | 0 | optional | Reasoning and proof. Not needed for developer rounds; can wait. |
| `puzzles` | 3 | optional | Interview probability problems. Not needed for developer rounds; can wait. |
| `py-found` | 1 | required | Fluent Python: lists, classes, sorting. Core developer content. |
| `pytest` | 1 | required | Testing code. Core developer content. |
| `quadratics` | 0 | recommended | Quadratics and factorising. Supports developer rounds; not a first gate. |
| `random-vars` | 1 | recommended | Expectation, variance and distributions. Supports developer rounds; not a first gate. |
| `ratio` | 0 | required | Ratio, percentages and rates. Core developer content. |
| `recruiting` | 0 | required | Roles, firms and the hiring calendar. Core developer content. |
| `regression` | 1 | optional | Linear regression and its failures. Not needed for developer rounds; can wait. |
| `research-int` | 3 | optional | Research interview cases and take-homes. Not needed for developer rounds; can wait. |
| `series` | 0 | recommended | Sequences, series and the binomial theorem. Supports developer rounds; not a first gate. |
| `sql` | 1 | recommended | SQL for data tasks. Supports developer rounds; not a first gate. |
| `stat-learning` | 2 | optional | Supervised learning and ISLR methods. Not needed for developer rounds; can wait. |
| `stat-models` | 2 | optional | Generalised linear models and Bayesian inference. Not needed for developer rounds; can wait. |
| `systems` | 3 | required | Caches, threads, sockets and design. Systems design and debugging round. |
| `taylor` | 1 | optional | Taylor series and approximation. Not needed for developer rounds; can wait. |
| `terminal` | 0 | required | The terminal and files. Core developer content. |
| `testing` | 1 | optional | Hypothesis tests and multiple testing. Not needed for developer rounds; can wait. |
| `topology` | 3 | optional | Metric and topological spaces. Not needed for developer rounds; can wait. |
| `trees` | 1 | optional | Binomial trees and Black-Scholes. Not needed for developer rounds; can wait. |
| `trig` | 0 | recommended | Trigonometry. Supports developer rounds; not a first gate. |
| `validation` | 2 | optional | Cross-validation and leakage. Not needed for developer rounds; can wait. |
| `vector-calc` | 1 | optional | Vector calculus. Not needed for developer rounds; can wait. |
| `vectors` | 1 | optional | Vectors and matrices. Not needed for developer rounds; can wait. |

**Mocks**

| Mock | Status | Note |
| --- | --- | --- |
| `mock-oa-code` | exists |  |
| `mock-oa-code-hard` | exists |  |
| `mock-superday-developer` | exists |  |

**Capstone:** an independent systems project, such as a feed handler or matching engine. The record holds repo link, rerun-from-clean result and defence notes. The user reviews it.

**Totals**

<!-- generated:totals:developer -->
| Set | Lessons written | Lessons unwritten | Lessons total | Hours in the app | Hours of outside study |
| --- | --- | --- | --- | --- | --- |
| Required | 228 | 0 | 228 | 116 | 564 |
| Recommended | 248 | 0 | 248 | 142 | 695 |
| Learn header (required plus recommended) | 476 | 0 | 476 | 258 | 1259 |
<!-- /generated -->

**Dependency conflicts**

<!-- generated:conflicts:developer -->
| From (required or recommended) | Optional course reached | Edge or route |
| --- | --- | --- |
| `cpp-pricing` | `trees` | L2 needs trees/L3 |
| `cpp-pricing` | `integrals` | via `trees` > `limits-thm` |
| `cpp-pricing` | `limits` | via `trees` > `limits-thm` > `integrals` |
| `cpp-pricing` | `limits-thm` | via `trees` |
| `cpp-pricing` | `multivar` | via `trees` > `limits-thm` |
| `random-vars` | `limits` | L5 needs limits/L5 |

Required courses that need a recommended course: `coding-int` needs `micro`; `exp-log` needs `functions`; `pytest` needs `plotting`.
<!-- /generated -->

## Strats

Plan: calculus, linear algebra, probability, options and pricing, with solid Python and C++. Finance basics are required here.

**Independent tasks that count** (each done alone, on material the learner has not seen)

1. Sit a timed maths paper on calculus, linear algebra and probability. Evidence: `mock-oa-strats`.
2. Derive put-call parity and one Greek from first principles, aloud. Evidence: external spoken mock.
3. Solve an unseen probability tree or martingale question cold. Evidence: drill in `markov` and `trees`, then `mock-superday-strats` (gap).
4. Complete a coding challenge in Python or C++. Evidence: `mock-oa-code`.
5. Price one option by a tree and a closed form, and explain the difference. Evidence: external capstone.
6. Pass a strats technical superday with C++ questions. Evidence: `mock-superday-strats` (gap) and an external mock.

**Course classification**

| Course | Stage | Status | Reason |
| --- | --- | --- | --- |
| `algebra` | 3 | optional | Abstract algebra. Not needed for strats screens; can wait. |
| `algo-think` | 1 | required | Complexity, recursion and sorting. Core strats content. |
| `alpha` | 2 | optional | Alpha research project. Not needed for strats screens; can wait. |
| `analysis` | 1 | optional | Real analysis. Not needed for strats screens; can wait. |
| `arma` | 2 | optional | ARMA time series. Not needed for strats screens; can wait. |
| `backtest` | 2 | optional | Backtesting project. Not needed for strats screens; can wait. |
| `brainteasers` | 3 | optional | Logic puzzles and brainteasers. Not needed for strats screens; can wait. |
| `coding-int` | 3 | required | Coding interview patterns. Coding part of the strats loop. |
| `coint` | 2 | optional | Cointegration. Not needed for strats screens; can wait. |
| `complex` | 1 | recommended | Complex numbers. Helps a strats profile; not a first gate. |
| `conditional` | 1 | required | Conditioning, Bayes and independence. Core strats content. |
| `contests` | 2 | optional | Contest-style problem solving. Not needed for strats screens; can wait. |
| `convex` | 2 | optional | Convex optimisation. Not needed for strats screens; can wait. |
| `counting` | 0 | required | Permutations, combinations and sums. Core strats content. |
| `counting-chance` | 1 | required | Counting arguments in probability. Core strats content. |
| `cpp` | 1 | required | C++ memory, the standard library and tests. Core strats content. |
| `cpp-pricing` | 1 | recommended | Pricing and low-latency C++. Helps a strats profile; not a first gate. |
| `ds` | 1 | required | Hash maps, trees, heaps and stacks. Core strats content. |
| `eigen` | 1 | required | Eigenvalues, SVD and PCA. Core strats content. |
| `elimination` | 1 | required | Elimination and solving systems. Core strats content. |
| `ensembles` | 2 | optional | Trees, boosting and ensembles. Not needed for strats screens; can wait. |
| `equations` | 0 | required | Solving equations and inequalities. Core strats content. |
| `estimation` | 1 | required | Estimators and confidence intervals. Core strats content. |
| `exp-log` | 0 | required | Exponentials and logarithms. Core strats content. |
| `fin-ml` | 2 | optional | Machine learning on financial data. Not needed for strats screens; can wait. |
| `first-python` | 0 | required | First programs in Python. Core strats content. |
| `functions` | 0 | required | Functions and graphs. Core strats content. |
| `game-theory` | 3 | optional | Games, auctions and poker. Not needed for strats screens; can wait. |
| `garch` | 2 | optional | Volatility models. Not needed for strats screens; can wait. |
| `git` | 1 | recommended | Version control. Helps a strats profile; not a first gate. |
| `graphs-dp` | 1 | recommended | Graph search and dynamic programming. Helps a strats profile; not a first gate. |
| `integrals` | 1 | required | Integration techniques. Core strats content. |
| `ito` | 3 | recommended | Brownian motion and Itô calculus. Asked in strats final rounds. |
| `least-squares` | 1 | required | Projections and least squares. Core strats content. |
| `limits` | 1 | required | Limits and derivatives. Core strats content. |
| `limits-thm` | 1 | required | Named distributions, LLN and CLT. Core strats content. |
| `linear-maps` | 1 | optional | Proof-based linear algebra. Not needed for strats screens; can wait. |
| `markets` | 1 | required | How markets and orders work. Finance basics: required for strats. |
| `markov` | 1 | required | Markov chains, random walks and martingales. Core strats content. |
| `measure-prob` | 3 | optional | Measure-theoretic probability. Not needed for strats screens; can wait. |
| `mental` | 0 | recommended | Daily mental arithmetic. Helps a strats profile; not a first gate. |
| `mental-pressure` | 3 | optional | Speed and accuracy under pressure. Not needed for strats screens; can wait. |
| `micro` | 1 | required | Market microstructure and the order book. Finance basics: required for strats. |
| `mm-games` | 3 | optional | Market-making and betting games. Not needed for strats screens; can wait. |
| `momentum-rep` | 3 | optional | Replication of a momentum paper. Not needed for strats screens; can wait. |
| `multivar` | 1 | required | Partial derivatives and constrained optimisation. Core strats content. |
| `number-sense` | 0 | required | Fractions, decimals, negatives and powers. Core strats content. |
| `numerics` | 2 | recommended | Numerical methods. Helps a strats profile; not a first gate. |
| `numpy-pandas` | 1 | required | Arrays and DataFrames. Core strats content. |
| `odes` | 1 | recommended | Ordinary differential equations. Strats maths paper names differential equations. |
| `opt-dash` | 2 | optional | Optimiser and dashboard project. Not needed for strats screens; can wait. |
| `options` | 1 | required | Options, payoffs and parity. Finance basics: required for strats. |
| `pairs-rep` | 3 | optional | Replication of a pairs-trading paper. Not needed for strats screens; can wait. |
| `pdes` | 3 | optional | PDEs and the Black-Scholes equation. Desk quant sub-route only. |
| `plotting` | 1 | recommended | Plotting with matplotlib. Helps a strats profile; not a first gate. |
| `proof` | 0 | optional | Reasoning and proof. Not needed for strats screens; can wait. |
| `puzzles` | 3 | recommended | Interview probability problems. Helps a strats profile; not a first gate. |
| `py-found` | 1 | required | Fluent Python: lists, classes, sorting. Core strats content. |
| `pytest` | 1 | recommended | Testing code. Helps a strats profile; not a first gate. |
| `quadratics` | 0 | required | Quadratics and factorising. Core strats content. |
| `random-vars` | 1 | required | Expectation, variance and distributions. Core strats content. |
| `ratio` | 0 | required | Ratio, percentages and rates. Core strats content. |
| `recruiting` | 0 | required | Roles, firms and the hiring calendar. Core strats content. |
| `regression` | 1 | required | Linear regression and its failures. Core strats content. |
| `research-int` | 3 | optional | Research interview cases and take-homes. Not needed for strats screens; can wait. |
| `series` | 0 | required | Sequences, series and the binomial theorem. Core strats content. |
| `sql` | 1 | recommended | SQL for data tasks. Helps a strats profile; not a first gate. |
| `stat-learning` | 2 | recommended | Supervised learning and ISLR methods. Helps a strats profile; not a first gate. |
| `stat-models` | 2 | optional | Generalised linear models and Bayesian inference. Not needed for strats screens; can wait. |
| `systems` | 3 | optional | Caches, threads, sockets and design. Not needed for strats screens; can wait. |
| `taylor` | 1 | required | Taylor series and approximation. Core strats content. |
| `terminal` | 0 | required | The terminal and files. Core strats content. |
| `testing` | 1 | recommended | Hypothesis tests and multiple testing. Helps a strats profile; not a first gate. |
| `topology` | 3 | optional | Metric and topological spaces. Not needed for strats screens; can wait. |
| `trees` | 1 | required | Binomial trees and Black-Scholes. Finance basics: required for strats. |
| `trig` | 0 | required | Trigonometry. Core strats content. |
| `validation` | 2 | recommended | Cross-validation and leakage. Helps a strats profile; not a first gate. |
| `vector-calc` | 1 | optional | Vector calculus. Not needed for strats screens; can wait. |
| `vectors` | 1 | required | Vectors and matrices. Core strats content. |

**Mocks**

| Mock | Status | Note |
| --- | --- | --- |
| `mock-oa-strats` | exists |  |
| `mock-oa-code` | exists |  |
| `mock-video` | exists | behavioural and spoken video mock |
| `mock-superday-strats` | exists |  |

**Capstone:** a small pricer or risk tool in C++ or Python with tests and a written error note. The record holds repo link, rerun-from-clean result and defence notes. The user reviews it.

**Totals**

<!-- generated:totals:strats -->
| Set | Lessons written | Lessons unwritten | Lessons total | Hours in the app | Hours of outside study |
| --- | --- | --- | --- | --- | --- |
| Required | 569 | 0 | 569 | 320 | 1363 |
| Recommended | 223 | 0 | 223 | 114 | 489 |
| Learn header (required plus recommended) | 792 | 0 | 792 | 434 | 1852 |
<!-- /generated -->

**Dependency conflicts**

<!-- generated:conflicts:strats -->
| From (required or recommended) | Optional course reached | Edge or route |
| --- | --- | --- |
| `numerics` | `opt-dash` | L4 needs opt-dash/L2 |

Required courses that need a recommended course: `coding-int` needs `graphs-dp`; `regression` needs `testing`.
<!-- /generated -->

### Derivatives and desk quant sub-route

Same learner as Strats, plus the pricing mathematics.

**Independent tasks that count** (each done alone, on material the learner has not seen)

1. Derive the Black-Scholes equation with Itô lemma and solve it through the heat equation. Evidence: `ito` and `pdes` reviews plus external derivation check.
2. Match a finite-difference price to the closed form to four decimal places. Evidence: external capstone code, rerun from clean.
3. Price one option three numerical ways and explain the error of each method. Evidence: `numerics` (unwritten) plus external review.
4. Solve a first-order and a second-order ODE, and state when each method fails. Evidence: `odes` (unwritten) topic exam (none yet).
5. Do an independent derivation of a change of measure on an unseen problem. Evidence: `measure-prob` exam `topic-3.2` plus external check.

**Course classification**

| Course | Stage | Status | Reason |
| --- | --- | --- | --- |
| `algebra` | 3 | optional | Abstract algebra. Not needed for derivatives roles; can wait. |
| `algo-think` | 1 | required | Complexity, recursion and sorting. Core desk quant content. |
| `alpha` | 2 | optional | Alpha research project. Not needed for derivatives roles; can wait. |
| `analysis` | 1 | optional | Real analysis. Not needed for derivatives roles; can wait. |
| `arma` | 2 | recommended | ARMA time series. Helps a pricing profile; not a first gate. |
| `backtest` | 2 | optional | Backtesting project. Not needed for derivatives roles; can wait. |
| `brainteasers` | 3 | optional | Logic puzzles and brainteasers. Not needed for derivatives roles; can wait. |
| `coding-int` | 3 | required | Coding interview patterns. Core desk quant content. |
| `coint` | 2 | optional | Cointegration. Not needed for derivatives roles; can wait. |
| `complex` | 1 | required | Complex numbers. Core desk quant content. |
| `conditional` | 1 | required | Conditioning, Bayes and independence. Core desk quant content. |
| `contests` | 2 | optional | Contest-style problem solving. Not needed for derivatives roles; can wait. |
| `convex` | 2 | recommended | Convex optimisation. Optimisation for calibration and portfolios. |
| `counting` | 0 | required | Permutations, combinations and sums. Core desk quant content. |
| `counting-chance` | 1 | required | Counting arguments in probability. Core desk quant content. |
| `cpp` | 1 | required | C++ memory, the standard library and tests. Core desk quant content. |
| `cpp-pricing` | 1 | required | Pricing and low-latency C++. Core desk quant content. |
| `ds` | 1 | required | Hash maps, trees, heaps and stacks. Core desk quant content. |
| `eigen` | 1 | required | Eigenvalues, SVD and PCA. Core desk quant content. |
| `elimination` | 1 | required | Elimination and solving systems. Core desk quant content. |
| `ensembles` | 2 | optional | Trees, boosting and ensembles. Not needed for derivatives roles; can wait. |
| `equations` | 0 | required | Solving equations and inequalities. Core desk quant content. |
| `estimation` | 1 | required | Estimators and confidence intervals. Core desk quant content. |
| `exp-log` | 0 | required | Exponentials and logarithms. Core desk quant content. |
| `fin-ml` | 2 | optional | Machine learning on financial data. Not needed for derivatives roles; can wait. |
| `first-python` | 0 | required | First programs in Python. Core desk quant content. |
| `functions` | 0 | required | Functions and graphs. Core desk quant content. |
| `game-theory` | 3 | optional | Games, auctions and poker. Not needed for derivatives roles; can wait. |
| `garch` | 2 | recommended | Volatility models. Helps a pricing profile; not a first gate. |
| `git` | 1 | recommended | Version control. Helps a pricing profile; not a first gate. |
| `graphs-dp` | 1 | recommended | Graph search and dynamic programming. Helps a pricing profile; not a first gate. |
| `integrals` | 1 | required | Integration techniques. Core desk quant content. |
| `ito` | 3 | required | Brownian motion and Itô calculus. Itô calculus is the core of pricing. |
| `least-squares` | 1 | required | Projections and least squares. Core desk quant content. |
| `limits` | 1 | required | Limits and derivatives. Core desk quant content. |
| `limits-thm` | 1 | required | Named distributions, LLN and CLT. Core desk quant content. |
| `linear-maps` | 1 | optional | Proof-based linear algebra. Not needed for derivatives roles; can wait. |
| `markets` | 1 | required | How markets and orders work. Core desk quant content. |
| `markov` | 1 | required | Markov chains, random walks and martingales. Core desk quant content. |
| `measure-prob` | 3 | recommended | Measure-theoretic probability. Change of measure and martingale pricing. |
| `mental` | 0 | recommended | Daily mental arithmetic. Helps a pricing profile; not a first gate. |
| `mental-pressure` | 3 | optional | Speed and accuracy under pressure. Not needed for derivatives roles; can wait. |
| `micro` | 1 | required | Market microstructure and the order book. Core desk quant content. |
| `mm-games` | 3 | optional | Market-making and betting games. Not needed for derivatives roles; can wait. |
| `momentum-rep` | 3 | optional | Replication of a momentum paper. Not needed for derivatives roles; can wait. |
| `multivar` | 1 | required | Partial derivatives and constrained optimisation. Core desk quant content. |
| `number-sense` | 0 | required | Fractions, decimals, negatives and powers. Core desk quant content. |
| `numerics` | 2 | required | Numerical methods. Prerequisite of pdes. Unwritten. |
| `numpy-pandas` | 1 | required | Arrays and DataFrames. Core desk quant content. |
| `odes` | 1 | required | Ordinary differential equations. Prerequisite of pdes. Unwritten. |
| `opt-dash` | 2 | optional | Optimiser and dashboard project. Not needed for derivatives roles; can wait. |
| `options` | 1 | required | Options, payoffs and parity. Core desk quant content. |
| `pairs-rep` | 3 | optional | Replication of a pairs-trading paper. Not needed for derivatives roles; can wait. |
| `pdes` | 3 | recommended | PDEs and the Black-Scholes equation. Black-Scholes as a PDE. |
| `plotting` | 1 | recommended | Plotting with matplotlib. Helps a pricing profile; not a first gate. |
| `proof` | 0 | optional | Reasoning and proof. Not needed for derivatives roles; can wait. |
| `puzzles` | 3 | recommended | Interview probability problems. Helps a pricing profile; not a first gate. |
| `py-found` | 1 | required | Fluent Python: lists, classes, sorting. Core desk quant content. |
| `pytest` | 1 | recommended | Testing code. Helps a pricing profile; not a first gate. |
| `quadratics` | 0 | required | Quadratics and factorising. Core desk quant content. |
| `random-vars` | 1 | required | Expectation, variance and distributions. Core desk quant content. |
| `ratio` | 0 | required | Ratio, percentages and rates. Core desk quant content. |
| `recruiting` | 0 | required | Roles, firms and the hiring calendar. Core desk quant content. |
| `regression` | 1 | required | Linear regression and its failures. Core desk quant content. |
| `research-int` | 3 | optional | Research interview cases and take-homes. Not needed for derivatives roles; can wait. |
| `series` | 0 | required | Sequences, series and the binomial theorem. Core desk quant content. |
| `sql` | 1 | recommended | SQL for data tasks. Helps a pricing profile; not a first gate. |
| `stat-learning` | 2 | recommended | Supervised learning and ISLR methods. Helps a pricing profile; not a first gate. |
| `stat-models` | 2 | optional | Generalised linear models and Bayesian inference. Not needed for derivatives roles; can wait. |
| `systems` | 3 | optional | Caches, threads, sockets and design. Not needed for derivatives roles; can wait. |
| `taylor` | 1 | required | Taylor series and approximation. Core desk quant content. |
| `terminal` | 0 | required | The terminal and files. Core desk quant content. |
| `testing` | 1 | recommended | Hypothesis tests and multiple testing. Helps a pricing profile; not a first gate. |
| `topology` | 3 | optional | Metric and topological spaces. Not needed for derivatives roles; can wait. |
| `trees` | 1 | required | Binomial trees and Black-Scholes. Core desk quant content. |
| `trig` | 0 | required | Trigonometry. Core desk quant content. |
| `validation` | 2 | recommended | Cross-validation and leakage. Helps a pricing profile; not a first gate. |
| `vector-calc` | 1 | recommended | Vector calculus. Helps a pricing profile; not a first gate. |
| `vectors` | 1 | required | Vectors and matrices. Core desk quant content. |

**Mocks**

| Mock | Status | Note |
| --- | --- | --- |
| `mock-oa-strats` | exists | shared with Strats |
| `mock-oa-code` | exists |  |
| `mock-video` | exists | shared with Strats |
| `mock-superday-strats` | exists |  |

**Capstone:** a priced-and-validated option project with a derivation note. The record holds repo link, rerun-from-clean result and defence notes. The user reviews it.

**Totals**

<!-- generated:totals:strats-deriv -->
| Set | Lessons written | Lessons unwritten | Lessons total | Hours in the app | Hours of outside study |
| --- | --- | --- | --- | --- | --- |
| Required | 646 | 0 | 646 | 361 | 1511 |
| Recommended | 228 | 0 | 228 | 118 | 431 |
| Learn header (required plus recommended) | 874 | 0 | 874 | 479 | 1942 |
<!-- /generated -->

**Dependency conflicts**

<!-- generated:conflicts:strats-deriv -->
| From (required or recommended) | Optional course reached | Edge or route |
| --- | --- | --- |
| `numerics` | `opt-dash` | L4 needs opt-dash/L2 |

Required courses that need a recommended course: `coding-int` needs `graphs-dp`; `regression` needs `testing`.
<!-- /generated -->

## Undecided

Plan: build the shared foundation, then choose a role. The app prompts the choice when the foundation is done.

**Shared foundation:** all of Stage 0 except `proof` (pure maths), then `py-found` as the first Stage 1 Python course and three core probability courses: `counting-chance`, `conditional`, `random-vars`.

**Independent tasks that count**

1. Pass a GCSE Higher non-calculator paper timed at 80% or better. Evidence: external paper marked by someone else.
2. Score 25 or more on Zetamac default settings. Evidence: `mock-oa-arith` and a dated screenshot (external).
3. Write and run a ten-line Python script from the terminal, alone. Evidence: `stage-0` exam and the drill in `first-python`.
4. Solve an unseen counting or conditional-probability problem in 5 minutes. Evidence: `topic-1.5` exam.
5. Read the role descriptions in `recruiting` and record a role choice with a reason. Evidence: in-app role prompt.

**Course classification**

| Course | Stage | Status | Reason |
| --- | --- | --- | --- |
| `algebra` | 3 | optional | Abstract algebra. Wait until a role is chosen. |
| `algo-think` | 1 | optional | Complexity, recursion and sorting. Wait until a role is chosen. |
| `alpha` | 2 | optional | Alpha research project. Wait until a role is chosen. |
| `analysis` | 1 | optional | Real analysis. Wait until a role is chosen. |
| `arma` | 2 | optional | ARMA time series. Wait until a role is chosen. |
| `backtest` | 2 | optional | Backtesting project. Wait until a role is chosen. |
| `brainteasers` | 3 | optional | Logic puzzles and brainteasers. Wait until a role is chosen. |
| `coding-int` | 3 | optional | Coding interview patterns. Wait until a role is chosen. |
| `coint` | 2 | optional | Cointegration. Wait until a role is chosen. |
| `complex` | 1 | optional | Complex numbers. Wait until a role is chosen. |
| `conditional` | 1 | required | Conditioning, Bayes and independence. Core probability. |
| `contests` | 2 | optional | Contest-style problem solving. Wait until a role is chosen. |
| `convex` | 2 | optional | Convex optimisation. Wait until a role is chosen. |
| `counting` | 0 | required | Permutations, combinations and sums. Shared foundation before a role choice. |
| `counting-chance` | 1 | required | Counting arguments in probability. Core probability. |
| `cpp` | 1 | optional | C++ memory, the standard library and tests. Wait until a role is chosen. |
| `cpp-pricing` | 1 | optional | Pricing and low-latency C++. Wait until a role is chosen. |
| `ds` | 1 | optional | Hash maps, trees, heaps and stacks. Wait until a role is chosen. |
| `eigen` | 1 | optional | Eigenvalues, SVD and PCA. Wait until a role is chosen. |
| `elimination` | 1 | optional | Elimination and solving systems. Wait until a role is chosen. |
| `ensembles` | 2 | optional | Trees, boosting and ensembles. Wait until a role is chosen. |
| `equations` | 0 | required | Solving equations and inequalities. Shared foundation before a role choice. |
| `estimation` | 1 | optional | Estimators and confidence intervals. Wait until a role is chosen. |
| `exp-log` | 0 | required | Exponentials and logarithms. Shared foundation before a role choice. |
| `fin-ml` | 2 | optional | Machine learning on financial data. Wait until a role is chosen. |
| `first-python` | 0 | required | First programs in Python. Shared foundation before a role choice. |
| `functions` | 0 | required | Functions and graphs. Shared foundation before a role choice. |
| `game-theory` | 3 | optional | Games, auctions and poker. Wait until a role is chosen. |
| `garch` | 2 | optional | Volatility models. Wait until a role is chosen. |
| `git` | 1 | optional | Version control. Wait until a role is chosen. |
| `graphs-dp` | 1 | optional | Graph search and dynamic programming. Wait until a role is chosen. |
| `integrals` | 1 | optional | Integration techniques. Wait until a role is chosen. |
| `ito` | 3 | optional | Brownian motion and Itô calculus. Wait until a role is chosen. |
| `least-squares` | 1 | optional | Projections and least squares. Wait until a role is chosen. |
| `limits` | 1 | optional | Limits and derivatives. Wait until a role is chosen. |
| `limits-thm` | 1 | optional | Named distributions, LLN and CLT. Wait until a role is chosen. |
| `linear-maps` | 1 | optional | Proof-based linear algebra. Wait until a role is chosen. |
| `markets` | 1 | optional | How markets and orders work. Wait until a role is chosen. |
| `markov` | 1 | optional | Markov chains, random walks and martingales. Wait until a role is chosen. |
| `measure-prob` | 3 | optional | Measure-theoretic probability. Wait until a role is chosen. |
| `mental` | 0 | required | Daily mental arithmetic. Shared foundation before a role choice. |
| `mental-pressure` | 3 | optional | Speed and accuracy under pressure. Wait until a role is chosen. |
| `micro` | 1 | optional | Market microstructure and the order book. Wait until a role is chosen. |
| `mm-games` | 3 | optional | Market-making and betting games. Wait until a role is chosen. |
| `momentum-rep` | 3 | optional | Replication of a momentum paper. Wait until a role is chosen. |
| `multivar` | 1 | optional | Partial derivatives and constrained optimisation. Wait until a role is chosen. |
| `number-sense` | 0 | required | Fractions, decimals, negatives and powers. Shared foundation before a role choice. |
| `numerics` | 2 | optional | Numerical methods. Wait until a role is chosen. |
| `numpy-pandas` | 1 | optional | Arrays and DataFrames. Wait until a role is chosen. |
| `odes` | 1 | optional | Ordinary differential equations. Wait until a role is chosen. |
| `opt-dash` | 2 | optional | Optimiser and dashboard project. Wait until a role is chosen. |
| `options` | 1 | optional | Options, payoffs and parity. Wait until a role is chosen. |
| `pairs-rep` | 3 | optional | Replication of a pairs-trading paper. Wait until a role is chosen. |
| `pdes` | 3 | optional | PDEs and the Black-Scholes equation. Wait until a role is chosen. |
| `plotting` | 1 | optional | Plotting with matplotlib. Wait until a role is chosen. |
| `proof` | 0 | optional | Reasoning and proof. Pure maths; skipped on the quant path. |
| `puzzles` | 3 | optional | Interview probability problems. Wait until a role is chosen. |
| `py-found` | 1 | required | Fluent Python: lists, classes, sorting. First Python after Stage 0: lists, classes, sorting. |
| `pytest` | 1 | optional | Testing code. Wait until a role is chosen. |
| `quadratics` | 0 | required | Quadratics and factorising. Shared foundation before a role choice. |
| `random-vars` | 1 | required | Expectation, variance and distributions. Core probability. |
| `ratio` | 0 | required | Ratio, percentages and rates. Shared foundation before a role choice. |
| `recruiting` | 0 | required | Roles, firms and the hiring calendar. Shows the roles before the choice. |
| `regression` | 1 | optional | Linear regression and its failures. Wait until a role is chosen. |
| `research-int` | 3 | optional | Research interview cases and take-homes. Wait until a role is chosen. |
| `series` | 0 | required | Sequences, series and the binomial theorem. Shared foundation before a role choice. |
| `sql` | 1 | optional | SQL for data tasks. Wait until a role is chosen. |
| `stat-learning` | 2 | optional | Supervised learning and ISLR methods. Wait until a role is chosen. |
| `stat-models` | 2 | optional | Generalised linear models and Bayesian inference. Wait until a role is chosen. |
| `systems` | 3 | optional | Caches, threads, sockets and design. Wait until a role is chosen. |
| `taylor` | 1 | optional | Taylor series and approximation. Wait until a role is chosen. |
| `terminal` | 0 | required | The terminal and files. Shared foundation before a role choice. |
| `testing` | 1 | optional | Hypothesis tests and multiple testing. Wait until a role is chosen. |
| `topology` | 3 | optional | Metric and topological spaces. Wait until a role is chosen. |
| `trees` | 1 | optional | Binomial trees and Black-Scholes. Wait until a role is chosen. |
| `trig` | 0 | required | Trigonometry. Shared foundation before a role choice. |
| `validation` | 2 | optional | Cross-validation and leakage. Wait until a role is chosen. |
| `vector-calc` | 1 | optional | Vector calculus. Wait until a role is chosen. |
| `vectors` | 1 | optional | Vectors and matrices. Wait until a role is chosen. |

**Mocks**

| Mock | Status | Note |
| --- | --- | --- |
| `mock-oa-arith` | exists | used for task 2 |
| `mock-video` | exists | general path; shared with Researcher and Strats |

Undecided never reads "ready". It reads "foundation done" once the required courses are met.

**Totals**

<!-- generated:totals:undecided -->
| Set | Lessons written | Lessons unwritten | Lessons total | Hours in the app | Hours of outside study |
| --- | --- | --- | --- | --- | --- |
| Required | 252 | 0 | 252 | 140 | 578 |
| Recommended | 0 | 0 | 0 | 0 | 0 |
| Learn header (required plus recommended) | 252 | 0 | 252 | 140 | 578 |
<!-- /generated -->

**Dependency conflicts**

<!-- generated:conflicts:undecided -->
| From (required or recommended) | Optional course reached | Edge or route |
| --- | --- | --- |
| `random-vars` | `limits` | L5 needs limits/L5 |

Required courses that need a recommended course: none.
<!-- /generated -->

## Notes for sign-off

- Judgement calls, not binding answers: `numerics` and `convex` as recommended for researchers; `coding-int` as required for strats and recommended-with-graphs-dp for researchers; `puzzles` as recommended for developers; `contests` as recommended for developers only.
- Stored hours for topics 3.2 and 3.4 are 0, so `ito`, `measure-prob` and `pdes` add lessons but no hours to the derivatives route. The true figure is higher.
- The conflict lists are conservative. They follow every `requires` edge at course level, so a conflict may disappear when item 7 cuts an edge.
- `mock-video` is named only by the Researcher and Strats paths and the general path. The Trader and Developer routes do not gate on it.
- Pure-maths courses (`proof`, `analysis`, `linear-maps`, `vector-calc`, `algebra`, `topology`) are optional for every role.
