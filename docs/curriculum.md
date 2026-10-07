# Zero to Quant Curriculum

Oct 5, 2026 · @Muddassir Shah · revised Oct 7, 2026: numerical methods, optimisation, deep learning, research method, continuous-time probability and, for two tracks, real analysis added

## Start here

The full path is about 3,390 hours of deliberate work, 3,450 on the researcher and ML research tracks and 3,470 on the developer track: roughly 4.3 years at 15 hours a week, or about 2.6 years at 25. It follows the three tiers of Priyanshu Priyank's Quant Roadmap (Quant Memo, 16 slides), with a Stage 0 added underneath, because the post's Tier 1 already assumes school maths and a working computer setup. The October 2026 additions cover what university quant and machine-learning programmes teach and the post leaves out.

Zero means: you can read English, use a web browser and do arithmetic with a calculator. Nothing else is assumed, including school algebra or ever having written a line of code.

Three things to know before starting:

- **Sit each stage's exit test first.** Pass it and you skip the stage. Fail it and you have a list of what to study.
- **Order matters.** Stages run in sequence, and inside a stage each numbered item uses the one before it.
- **This builds skill, not a credential.** Trading firms and funds hire researchers and traders mostly from maths, physics, statistics and computer science degrees, and a self-taught CV rarely clears the screen at the top names. Run this alongside a quantitative degree, or aim first at roles where projects carry more weight: quant developer, data, risk, smaller firms.

## The map

Four stages, 3,390 hours (3,450 on the researcher and ML research tracks, 3,470 on the developer track), each closed by a test you can mark yourself.

| Stage | Hours | At 15 h/week | You leave when |
| --- | --- | --- | --- |
| 0. From nothing (not in the post) | 500 | 8 months | A GCSE Higher paper at 80%, a precalculus test at 85%, and a Python script you wrote runs |
| 1. Foundations (post's Tier 1) | 1,415; 1,475 on the researcher and ML research tracks | 22 months; 23 | University finals at 70% in calculus, linear algebra and probability; 150 algorithm problems solved; on two tracks, the main theorems of analysis proved without notes |
| 2. Intermediate (post's Tier 2) | 1,075; 1,155 on the developer track | 17 months; 18 | A call priced four ways with its errors measured; a portfolio's dual values explained; your own transformer matches a reference; three finished projects, each with tests and a written results note that passes the research checklist |
| 3. Advanced (post's Tier 3) | 400 | 6 months | One paper replicated out of sample; the interview books solved cold |

Two habits run through every stage and are not on the map: 10 minutes of mental arithmetic a day from the first week, and three interview-style probability problems a week from item 1.5 onwards.

## Stage 0: From nothing (500 hours)

This stage is everything the post takes for granted: school maths up to the edge of calculus, and enough computer skill to install and run things.

| # | Topic | Hours | Cover | Use |
| --- | --- | --- | --- | --- |
| 0.1 | Number | 60 | Fractions, decimals, percentages, ratio, negatives, powers, roots, estimation | Khan Academy: Arithmetic, then Pre-algebra |
| 0.2 | Algebra | 180 | Expressions, linear equations, inequalities, simultaneous equations, quadratics, functions, graphs | Khan Academy: Algebra 1 and 2. UK route: Corbettmaths GCSE videos and worksheets |
| 0.3 | Precalculus | 200 | Exponentials and logarithms, trigonometry, sequences and series, binomial expansion, vectors, counting with permutations and combinations | Khan Academy: Precalculus. UK route: TLMaths A-level videos. One-book option: Basic Mathematics, Serge Lang |
| 0.4 | Computer basics | 40 | Touch typing, files and folders, installing software, the terminal, a code editor | keybr.com for typing. Install Python and VS Code. First three chapters of Automate the Boring Stuff (free online) |
| 0.5 | Mental arithmetic | 20 | Times tables to 12, two-digit addition, subtraction and multiplication, fractions to decimals | Zetamac arithmetic game, 10 minutes a day |

All of it is free. Do 0.1 to 0.3 in order; run 0.4 and 0.5 alongside from the first week.

**Exit test**

- [ ] A GCSE Higher non-calculator past paper, timed, at 80% or better (exam boards publish them free)
- [ ] Khan Academy Precalculus course challenge at 85% or better
- [ ] Zetamac score of 25 or more on default settings
- [ ] You can make a folder, write a ten-line Python script in it and run it from the terminal

## Stage 1: Foundations (1,415 hours; 1,475 on the researcher and ML research tracks)

This is the post's Tier 1 put into a fixed order, with one resource chosen per topic. Python comes first so that every maths topic after it can be checked in code; C++ comes last. On the researcher and ML research tracks, real analysis (A1) comes straight after calculus.

### 1.1 Python (150 h)

- **Use:** CS50P (Harvard, free) or the post's Automate the Boring Stuff. Then Python for Data Analysis by Wes McKinney (free online) for NumPy, pandas and matplotlib.
- **Not yet:** the post's Fluent Python and Python for Finance both assume fluency. Fluent Python belongs in Stage 2.
- **Exit:** from a CSV of daily prices, compute returns, annualised volatility and maximum drawdown, and plot them.

### 1.2 Tools (40 h)

- **Cover:** Git and GitHub, the Linux command line, SQL basics, testing with pytest. The post lists none of these and every quant job uses all four.
- **Use:** The Missing Semester (MIT, free) and SQLBolt.
- **Exit:** the 1.1 project is in a Git repository with at least one test. Everything you build from here on is too.

### 1.3 Calculus (200 h)

- **Use:** the post's Stewart, or OpenStax Calculus volumes 1 to 3 (free), with MIT 18.01 lectures. Watch 3Blue1Brown's Essence of Calculus first for intuition.
- **Cover:** limits, derivatives, optimisation, integrals, Taylor series, partial derivatives, gradients, multiple integrals, Lagrange multipliers.
- **Exit:** the MIT 18.01 final exam at 70%, plus the 18.02 problem sets on partial derivatives and Lagrange multipliers.

### A1 Real analysis (60 h): researcher and ML research tracks only

Research interviews ask for proofs, and machine-learning theory is written in them. 1.3 uses the theorems; this proves them.

- **Use:** Abbott, Understanding Analysis, 2nd edition, chapters 1 to 6, with MIT 18.100A Real Analysis (Fall 2020, free) for lectures and problem sets. Lebl's Basic Analysis I (free, the course's textbook) is the second explanation when a section does not land.
- **Not yet:** Rudin is the reference and too terse for a first course. Tao's Analysis I builds the reals from axioms, a course of its own longer than these 60 hours. Both are stretch reading.
- **Cover:** completeness and suprema, countable and uncountable sets, limits of sequences with an explicit $N(\varepsilon)$, subsequences, Cauchy sequences, series and rearrangements, open, closed and compact sets, continuity and uniform continuity, the derivative and the mean value theorems, uniform convergence, power series, Taylor's theorem, Weierstrass approximation. No proof course comes first, so A1 teaches its own proof writing.
- **Exit:** prove the main theorems of real analysis on the line without notes, two or more from each of Abbott's chapters 1 to 6 at 7 of 10, and pass the MIT 18.100A Final Assignment at 70%, timed.
- **By track:** traders and developers can take it as an elective; it is not in their hours.

### 1.4 Linear algebra (150 h)

- **Use:** the post's Strang, Introduction to Linear Algebra, with his MIT 18.06 lectures (free). Watch 3Blue1Brown's Essence of Linear Algebra first.
- **Not yet:** Axler is a proof-based second course and the wrong first book. Horn and Johnson is a reference; skip it.
- **Cover:** elimination, vector spaces, rank, orthogonality, projections, least squares, determinants, eigenvalues, the singular value decomposition, positive definite matrices.
- **Exit:** the 18.06 final at 70%, and least squares and principal component analysis written in NumPy from the matrix operations.

### 1.5 Probability (265 h): the priority

The post is right that this is where most of the effort goes. It is the subject interviews test hardest.

- **Use:** Introduction to Probability by Blitzstein and Hwang (free online) with the Harvard Stat 110 lectures. It is driven by problems and is the closest textbook to interview style. The post's Toronto text (Evans and Rosenthal, free) is a sound alternative. For continuous time: Durrett, Essentials of Stochastic Processes, chapters 4 and 5, and Grimmett and Stirzaker, Probability and Random Processes, chapter 13.
- **Cover:** counting, conditional probability, Bayes' rule, random variables, expectation and its linearity, indicator variables, variance and covariance, the named distributions, joint and conditional distributions, conditional expectation, the law of large numbers, the central limit theorem, Markov chains, random walks, martingales and optional stopping. Then continuous time: Markov chains with holding times and queues, Brownian motion, its martingales, exit problems with and without drift, the reflection principle.
- **Exit:** two Stat 110 past finals at 70%, and a continuous-time paper at 70%: a chain's stationary distribution and hitting time, an exit with drift by optional stopping, and the running maximum by reflection.

### 1.6 Statistics (120 h)

- **Use:** the post's DeGroot and Schervish, for its chapters on estimation, hypothesis testing and linear models. If it is too steep, do OpenIntro Statistics (free) first.
- **Cover:** estimators, bias and variance, maximum likelihood, confidence intervals, hypothesis tests, p-values, multiple testing, linear regression and its assumptions, Bayesian updating.
- **Exit:** fit a linear regression in NumPy, match the statsmodels output, and explain every number in its summary table.

### 1.7 Finance basics (100 h, alongside 1.3 to 1.6)

The post calls this optional. For trader and researcher interviews it is not: you will be asked about markets.

- **Use, in order:** Khan Academy Finance and Capital Markets for shares, bonds, interest and compounding. Then the post's Zerodha Varsity (free): its modules on stock markets, futures and options transfer to any market, though the examples are Indian. Then Hull, for forwards, futures, option properties, binomial trees, Black-Scholes and the Greeks.
- **Add:** Trading and Exchanges by Larry Harris for market microstructure. The post names microstructure as important and lists nothing for it.
- **Later or never:** Natenberg only if you aim at options trading. Skip Kratter; the post itself says Varsity covers it.
- **Exit:** explain a limit order book, the bid-ask spread, and market against limit orders; derive put-call parity; price a European option on a binomial tree in Python.

### 1.8 Data structures and algorithms (250 h)

- **Use:** Grokking Algorithms by Aditya Bhargava as a first read. Then one problem list: NeetCode 150 (works well in Python, video solutions) or the post's Striver A2Z sheet (larger, built around C++ and Java). CLRS is a reference only, as the post says.
- **Cover:** complexity, arrays, hashing, two pointers, stacks, queues, linked lists, binary search, trees, heaps, graphs, recursion, dynamic programming, greedy methods.
- **Exit:** 150 problems solved, and a fresh LeetCode medium finished in 30 minutes more often than not.

### 1.9 C++ (140 h)

- **Use:** learncpp.com (free, kept current) or the post's Stroustrup, Programming: Principles and Practice. Skip Sams Teach Yourself C++ in 21 Days; it is dated. Meyers comes after a first book. Williams matters only for developer roles.
- **Exit:** rewrite the 1.7 binomial pricer in C++ with tests and time it against the Python version.
- **By track:** traders and researchers can let C++ slip into Stage 2. For developers it is the core skill and needs at least double these hours.

## Stage 2: Intermediate (1,075 hours; 1,155 on the developer track)

This is the post's Tier 2, with four items the post leaves out: numerical methods and optimisation first, because pricing, risk and training all run on them; deep learning after machine learning; and research method just before the projects. Choose a track before starting, because the four roles are interviewed differently and the post treats them as one.

| Track | Interviews test | Weight in Stages 2 and 3 |
| --- | --- | --- |
| Trader | Probability, mental arithmetic, market-making and betting games | Probability drills, options, one project |
| Researcher | Probability, statistics, regression, machine learning, a data take-home | 2.1, 2.2, 2.2c, projects 1 and 2, paper replication |
| ML research | Probability, linear algebra, proofs, machine learning and deep learning built from first principles, a research take-home | A1, 2.1, 2.1b, 2.2c, project 2, paper replication |
| Developer | Algorithms, C++, systems design | C++, 2.0a, contests, projects 1 and 4 |

The ML research track takes the researcher track's items and hours; it differs in where the weight goes, not in what is studied. Every track takes 2.0a, 2.0b, 2.1b and 2.2c in full. The order is 2.0a, 2.0b, 2.1, 2.1b, 2.2, 2.2c, 2.3, with 2.4 alongside; developers build projects 1 and 4 before 2.1 and take 2.2c before the alpha project.

### 2.0a Numerical methods, floating point and Monte Carlo (120 h): missing from the post

Prices, risk numbers and trained models are all numerical answers. A desk that cannot say which error dominates cannot say whether a price is right.

- **Use:** Süli and Mayers, An Introduction to Numerical Analysis, for error, equations, interpolation and integrals; Trefethen and Bau, Numerical Linear Algebra; Wilmott, Howison and Dewynne, The Mathematics of Financial Derivatives, for finite differences; Glasserman, Monte Carlo Methods in Financial Engineering. MIT 18.335J (free, with solutions) for lectures and problem sets. Read Goldberg's "What Every Computer Scientist Should Know About Floating-Point Arithmetic" (its sections on rounding error and the IEEE standard) at the start.
- **Cover:** floating point as a number system, conditioning and stability, cancellation, root finding that never fails, interpolation and splines, quadrature, solving linear systems well, iterative solvers, the heat and Black-Scholes equations on a grid and their stability, random number generators, Monte Carlo error, variance reduction, quasi-Monte Carlo, Greeks by simulation, early exercise by Longstaff and Schwartz.
- **No differential-equations course first:** 2.0a teaches the heat equation, Fourier modes and stiff equations it needs, and derives Black-Scholes from a binomial tree without Itô calculus.
- **Exit:** price a European call four ways (closed form, binomial tree, Crank-Nicolson, Monte Carlo with a control variate) and plot error against work on log-log axes, reading off the orders; compute implied volatility across a strike grid with no failures; explain one cancellation failure and its fix.

### 2.0b Optimisation (80 h): missing from the post

Portfolios are optimisation problems, prices are duals, and training is descent. Knowing whether a problem is convex is most of the job.

- **Use:** Boyd and Vandenberghe, Convex Optimization (free PDF), with the Stanford EE364A lectures; for linear programming, Vanderbei, Linear Programming: Foundations and Extensions, because Boyd and Vandenberghe do not teach the simplex method. Nocedal and Wright is the reference for algorithms.
- **Cover:** linear programmes, the simplex method, duality and shadow prices, no-arbitrage from Farkas' lemma, convex sets and functions, Lagrangian duality and the KKT conditions, gradient descent, Newton, quasi-Newton, accelerated, stochastic and proximal methods with their rates, constrained mean-variance portfolios, execution schedules as quadratic programmes, the lasso and the support vector machine as convex programmes.
- **Exit:** derive the dual of a linear programme and confirm strong duality numerically; prove the convexity of three functions; show gradient descent converging linearly against Newton's quadratic rate; build a long-only mean-variance portfolio with a turnover limit and explain each constraint's dual value.

### 2.1 Machine learning (200 h)

- **Use:** An Introduction to Statistical Learning with Python (free PDF) as the core text. The post marks it optional; for quant work it is the reverse, because most models in use are linear, regularised or tree-based and the hard part is validation.
- **Alongside, for code:** the post's Géron. A [PyTorch edition](https://www.oreilly.com/library/view/-/9798341607972) came out in October 2025; the post lists the older Keras and TensorFlow one.
- **Videos:** the post's CampusX series is, to my knowledge, taught largely in Hindi, so check before committing. Andrew Ng's Machine Learning Specialization and StatQuest cover the same ground in English.
- **Then one applied book:** Advances in Financial Machine Learning (López de Prado) for method: labelling, purged cross-validation, backtest overfitting. Or the post's Jansen for breadth and a code repository. Isichenko is dense and worth the time only on the researcher track.
- **Exit:** one tabular prediction problem done end to end with time-ordered cross-validation, and you can explain leakage, regularisation and the bias-variance trade-off without notes.

### 2.1b Deep learning core (120 h)

2.1 gives a first pass at neural networks. This builds them by hand, which is what machine-learning labs test and what every framework hides.

- **Use:** Prince, Understanding Deep Learning (free PDF), chapters 1 to 12, with Karpathy's Neural Networks: Zero to Hero rebuilt in NumPy instead of PyTorch, and the MIT 6.7960 Deep Learning problem sets (Fall 2024, free).
- **Why NumPy, not PyTorch:** building the engine is the understanding. Someone who has written backpropagation reads any framework in an afternoon; the reverse is not true.
- **Skip:** Goodfellow, Bengio and Courville, which predates transformers. Bishop and Bishop is stretch reading.
- **Cover:** what deep networks compute, losses from likelihood, learning-rate schedules, AdamW and clipping, reverse-mode automatic differentiation, an autodiff engine of your own, initialisation and normalisation, reading training curves, generalisation and double descent, convolution, residual networks, attention and the transformer, tokenisation, scaling laws.
- **Scale:** toy models that train in a browser or on a laptop. Everything that matters at this scale (correctness, the loss at initialisation, curves, overfitting, sampling) is visible at 100,000 parameters.
- **Exit:** your own NumPy autodiff engine trains an MLP and a small CNN; your character-level transformer's validation loss is within 0.05 nats of a reference implementation; you can derive and explain backpropagation, normalisation and attention without notes.

### 2.2 Time series (60 h): missing from the post

- **Use:** [Forecasting: Principles and Practice, the Pythonic Way](https://otexts.com/fpppy) (Hyndman and co-authors, free online) for the core. Analysis of Financial Time Series by Ruey Tsay for volatility models and cointegration.
- **Cover:** stationarity, autocorrelation, ARMA models, volatility clustering and GARCH, cointegration.
- **Exit:** test a pair of price series for cointegration, and explain why models are fitted to returns and not prices.

### 2.2c Research method (35 h): missing from the post

A researcher's value is the false discoveries they do not ship. No university teaches this as a named course, so the app has to be the supervisor.

- **Use:** López de Prado, Advances in Financial Machine Learning, chapters 11 to 14 (you own it from 2.1), with Arnott, Harvey and Markowitz (2019), "A Backtesting Protocol in the Era of Machine Learning", as the checklist. Then a short pack of method papers by section: Harvey, Liu and Zhu (2016), Bailey and López de Prado on the deflated Sharpe ratio, Ioannidis (2005), McLean and Pontiff (2016), and Kapoor and Narayanan (2023) for the same failures in machine learning.
- **Cover:** the uncertainty of one Sharpe ratio, autocorrelation and the block bootstrap, trial counts and the deflated Sharpe ratio, backtest overfitting, auditing someone else's backtest (look-ahead, survivorship, splits, costs, choices made in sample), what survives publication, benchmark reuse and seed-picking in machine learning, writing a results note, pre-registration.
- **Exit:** audit a supplied backtest with five planted defects (look-ahead, survivorship, unadjusted splits, in-sample parameter choice, missing costs) and find at least four; write a one-page pre-registration for project 2 before touching its data; report a deflated Sharpe ratio and a block-bootstrap interval for a strategy's Sharpe ratio.
- **From here on:** every results note that reports a Sharpe ratio passes the same checklist.

### 2.3 Projects (400 h)

Do three properly, not five thinly. These are the post's five, re-ranked by how much they prove to someone reading your CV.

1. **Backtesting engine** (post's no. 1). Add what the post leaves out: transaction costs, slippage, a check against look-ahead, and a held-out period. Report Sharpe, Calmar and maximum drawdown.
2. **Alpha signal research** (post's no. 4). Cross-sectional momentum and mean reversion across a few hundred shares. Report information coefficient, turnover and Sharpe after costs. This is the closest of the five to real research work.
3. **Options analytics dashboard** (post's no. 3). Implied volatility surface and Greeks, with Black-Scholes, binomial and Monte Carlo pricers compared. For data, yfinance option chains on US shares or Deribit's public API work in place of NSE.
4. **Live market data handler** (post's no. 5). Websocket ticks into multi-timeframe candles, stored in PostgreSQL or Redis, with latency measured. On the developer track, write it in C++.
5. **Trading bot** (post's no. 2). Paper trading only, built on projects 1 and 4. It ranks last because EMA, RSI and Supertrend rules are retail technical analysis and carry no weight with a professional reader.

Every project ships with a README, tests, and a one-page results note that includes what failed. A note that reports a Sharpe ratio also passes the 2.2c checklist: a pre-registration locked before the data was opened, a bias audit, a deflated Sharpe ratio and a bootstrap interval. Treat any simple rule that backtests to a Sharpe above 2 as a bug until you have proved otherwise.

Library notes on the post's list: Quandl is now Nasdaq Data Link; zipline is no longer maintained, so use zipline-reloaded or your own engine; yfinance breaks often, so cache data to disk.

### 2.4 Contests (140 h on the developer track, 60 h on the others, spread across the stage)

- **Use:** Codeforces, the post's first pick. Start once you have 100 problems behind you and aim for one contest a week. A rating of 1400 is a fair first-year target on the developer track.
- **How much it counts:** rating-based shortlisting is mainly a feature of Indian campus hiring. Elsewhere a rating helps developer applications and counts for little in trader or researcher interviews.
- **By track:** developers do it all: 30 rated contests, each upsolved, and three practice rounds. The other tracks take the contest-craft course, number theory and modular arithmetic, 12 contests and two practice rounds, and set no rating target; the hours go to 2.0a, 2.0b, 2.1b and 2.2c.
- **Add:** Kaggle competitions on the researcher track, firm-run trading competitions such as IMC Prosperity on the trader track, and Project Euler for maths with code.

## Stage 3: Advanced (400 hours)

This is the post's Tier 3: papers, then interview preparation. Interview drilling starts here in earnest, but the weekly probability problems since 1.5 mean you are not starting cold.

### 3.1 Research papers (150 h)

- **Where:** the post's three sources: SSRN, arXiv Quantitative Finance and WorldQuant BRAIN.
- **Method:** replicate before you read widely. Pick one classic, reproduce its main table, then extend it to data from after publication.
- **Starting list:** Jegadeesh and Titman (1993) on momentum. Fama and French (1993) on the three-factor model. Gatev, Goetzmann and Rouwenhorst (2006) on pairs trading. Avellaneda and Stoikov (2008) on market making. Harvey, Liu and Zhu (2016) on multiple testing in factor research.
- **Machine-learning option:** a toy replication of double descent (Belkin and co-authors, 2019; Nakkiran and co-authors, 2020), built on your 2.1b engine, can stand in for the finance paper. Researchers should do a finance paper first and this one second.
- **Exit:** one replication on GitHub with an out-of-sample extension and a plain note on how much of the effect survived.

### 3.2 Stochastic calculus (optional, hours not counted): missing from the post

- **Who needs it:** derivatives pricing and desk quant roles. It is rarely tested for trading or statistical research roles.
- **Use:** Stochastic Calculus for Finance, volumes I and II, by Steven Shreve.

### 3.3 Interview preparation (250 h)

Work the books in this order, easiest first:

1. Fifty Challenging Problems in Probability, Mosteller (post).
2. A Practical Guide to Quantitative Finance Interviews, Xinfeng Zhou, known as the green book. The post lists Zhou under the wrong title; see the last section.
3. Heard on the Street, Timothy Crack (post).
4. Quant Job Interview Questions and Answers, Mark Joshi and co-authors. Developer and desk quant roles only.

The books do not train the live formats, so add:

- **Mental arithmetic:** Zetamac at 50 or more on default settings, plus timed drills in the 80-questions-in-8-minutes format some firms use.
- **Market-making games:** quote a two-sided price on an unknown quantity and update it as trades come in. Practise aloud with a partner.
- **Betting games:** expected value, when to hedge, Kelly sizing.
- **Jane Street's Probability and Markets guide:** free, short, and written by the firm about its own interviews.
- **Mock interviews, spoken aloud:** interviewers mark the reasoning as it happens, not only the answer.

**Exit test**

- [ ] 80% of the probability chapter in Zhou solved cold
- [ ] Zetamac at 50 or more
- [ ] Ten mock interviews done, at least three with a stranger

## Weekly rhythm and rules

A 15-hour week splits four ways, with most of it on the one numbered item you are currently working through.

| Block | Hours | What |
| --- | --- | --- |
| Main subject | 9 | Three 3-hour sessions on the current item |
| Build | 3 | Code. From Stage 1, something is committed every week |
| Review | 2 | Redo every problem you got wrong, one week later and one month later |
| Mental arithmetic | 1 | 10 minutes a day |

Rules:

1. **One resource per topic.** The post says the same. Pick it and finish it.
2. **Problems over reading.** At least 60% of study time goes on solving, not on text or video.
3. **No exit test, no next stage.** Marks under the bar mean more problems, not a new book.
4. **Everything goes on GitHub** from item 1.2 onwards.
5. **Know the hiring calendar.** Internship and graduate applications run on fixed annual windows, often opening about a year ahead. Check each target firm's dates early.

## Where this departs from the post

The post is a sound resource list but not a curriculum: it has no order, no hours and no tests, and it starts above zero. Its framing is also Indian campus hiring, which shows in the resources and in the weight on contest ratings.

| The post | This curriculum | Why |
| --- | --- | --- |
| Starts at Tier 1 | Stage 0 added | Tier 1 assumes school maths and a working setup |
| No order, hours or tests | Fixed order, hours and an exit test per stage | Without them there is no way to know when to move on |
| Axler listed first for linear algebra | Strang first, Axler dropped | Axler is a proof-based second course |
| Toronto text or DeGroot for probability | Blitzstein and Stat 110, the post's picks as alternatives | Closer to interview problems |
| Finance basics optional | Required | Traders and researchers are asked about markets |
| ISLR optional | Core text | Validation and linear models are most of quant machine learning |
| Géron, Keras and TensorFlow edition | PyTorch edition | Newer edition, October 2025 |
| CampusX videos | English alternatives named | Teaching language, to my knowledge Hindi |
| NSE and Indian broker data | US shares and Deribit options data | Free, no broker account needed |
| Indicator bots as a headline project | Ranked last, paper only | Retail technical analysis proves nothing to a professional |
| Codeforces rating as a hiring filter | Demoted outside the developer track, where 2.4 drops to 60 h | Mainly an Indian campus-hiring practice |
| Zhou credited with Quant Job Interview Questions and Answers | Two separate books, both listed | That title is Joshi's; Zhou wrote A Practical Guide to Quantitative Finance Interviews ([comparison](https://quantvault.org/best-quant-interview-books.html)) |
| The Puzzle Palace | Left out | I could not identify the resource |
| Nothing on tools, time series, stochastic calculus, mental arithmetic or market-making games | All added | Used daily on the job or tested at interview |
| Nothing on numerical methods, optimisation or research method; deep learning only as part of Géron | 2.0a, 2.0b, 2.2c and 2.1b added; continuous-time processes inside 1.5 | Core in the university quant programmes surveyed (Princeton ORFE, CMU MSCF, Baruch, Cambridge), and what machine-learning labs test |
| No proofs | Real analysis (A1) on the researcher and ML research tracks | Research interviews and ML theory assume it |

## Sources

- Quant Roadmap, Priyanshu Priyank, Quant Memo: the 16-slide post this is built on
- [Hands-On Machine Learning with Scikit-Learn and PyTorch, O'Reilly](https://www.oreilly.com/library/view/-/9798341607972)
- [Forecasting: Principles and Practice, the Pythonic Way](https://otexts.com/fpppy)
- [The Best Quant Interview Books, Compared, QuantVault](https://quantvault.org/best-quant-interview-books.html)
- [Convex Optimization, Boyd and Vandenberghe, free PDF](https://web.stanford.edu/~boyd/cvxbook/)
- [MIT 18.335J Introduction to Numerical Methods, Spring 2019](https://ocw.mit.edu/courses/18-335j-introduction-to-numerical-methods-spring-2019/)
- [MIT 18.100A Real Analysis, Fall 2020](https://ocw.mit.edu/courses/18-100a-real-analysis-fall-2020)
- [MIT 6.7960 Deep Learning, Fall 2024](https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/)
- [Understanding Deep Learning, Simon Prince, book repository](https://github.com/udlbook/udlbook)
- [Neural Networks: Zero to Hero, Andrej Karpathy](https://karpathy.ai/zero-to-hero.html)
- [A Backtesting Protocol in the Era of Machine Learning, Arnott, Harvey and Markowitz, SSRN 3275654](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3275654)

Hours are my estimates for a learner starting from zero, not sourced figures. The hours of the October 2026 additions are net of what the earlier items already teach.
