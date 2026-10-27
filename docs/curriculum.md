# Zero to Quant Curriculum

Oct 5, 2026 · @Muddassir Shah

## Start here

The full path is about 3,530 hours of deliberate work: roughly 4.5 years at 15 hours a week, or about 2.7 years at 25. Without the pure maths items it is 3,330 hours, about 4.3 years at 15 hours a week. It follows the three tiers of Priyanshu Priyank's Quant Roadmap (Quant Memo, 16 slides), with a Stage 0 added underneath, because the post's Tier 1 already assumes school maths and a working computer setup.

Zero means: you can read English, use a web browser and do arithmetic with a calculator. Nothing else is assumed, including school algebra or ever having written a line of code.

Four things to know before starting:

- **Sit each stage's exit test first.** Pass it and you skip the stage. Fail it and you have a list of what to study.
- **Order matters.** Stages run in sequence, and inside a stage each numbered item uses the one before it.
- **This builds skill, not a credential.** Trading firms and funds hire researchers and traders mostly from maths, physics, statistics and computer science degrees, and a self-taught CV rarely clears the screen at the top names. Run this alongside a quantitative degree, or aim first at roles where projects carry more weight: quant developer, data, risk, smaller firms.
- **Two tags mark the items added for breadth.** **[Quant]** marks material a quant career needs, with the roles that use it. **[Pure maths]** marks what a maths degree teaches for its own sake: it deepens proof and rounds out the education, but it is not needed to be hired. Untagged items are the core quant path. Pure maths items never gate the next stage on the quant path; they do if you want a degree-level education.

## The map

Four stages, 3,530 hours (3,330 on the quant path, without the pure maths items), each closed by a test you can mark yourself.

| Stage | Hours | Quant path | At 15 h/week | You leave when |
| --- | --- | --- | --- | --- |
| 0. From nothing (not in the post) | 540 | 500 | 8 months | A GCSE Higher paper at 80%, a precalculus test at 85%, and a Python script you wrote runs; five short proofs a stranger can check **[Pure maths]** |
| 1. Foundations (post's Tier 1) | 1,650 | 1,490 | 25 months | University finals at 70% in calculus, linear algebra, probability and differential equations; 150 algorithm problems solved; a proof-based analysis paper at 60% **[Pure maths]** |
| 2. Intermediate (post's Tier 2) | 940 | 940 | 14 months | Three finished projects, each with tests and a written results note; one option priced three numerical ways with each error explained |
| 3. Advanced (post's Tier 3) | 400 | 400 | 6 months | One paper replicated out of sample; the interview books solved cold |

Two habits run through every stage and are not on the map: 10 minutes of mental arithmetic a day from the first week, and three interview-style probability problems a week from item 1.5 onwards.

## Stage 0: From nothing (540 hours)

This stage is everything the post takes for granted: school maths up to the edge of calculus, and enough computer skill to install and run things.

| # | Topic | Hours | Cover | Use |
| --- | --- | --- | --- | --- |
| 0.1 | Number | 60 | Fractions, decimals, percentages, ratio, negatives, powers, roots, estimation | Khan Academy: Arithmetic, then Pre-algebra |
| 0.2 | Algebra | 180 | Expressions, linear equations, inequalities, simultaneous equations, quadratics, functions, graphs | Khan Academy: Algebra 1 and 2. UK route: Corbettmaths GCSE videos and worksheets |
| 0.3 | Precalculus | 200 | Exponentials and logarithms, trigonometry, sequences and series, binomial expansion, vectors, counting with permutations and combinations | Khan Academy: Precalculus. UK route: TLMaths A-level videos. One-book option: Basic Mathematics, Serge Lang |
| 0.4 | Computer basics | 40 | Touch typing, files and folders, installing software, the terminal, a code editor | keybr.com for typing. Install Python and VS Code. First three chapters of Automate the Boring Stuff (free online) |
| 0.5 | Mental arithmetic | 20 | Times tables to 12, two-digit addition, subtraction and multiplication, fractions to decimals | Zetamac arithmetic game, 10 minutes a day |
| 0.6 | Reasoning and proof **[Pure maths]** | 40 | Statements, and, or, not, implication, quantifiers, sets, functions as sets, direct proof, the contrapositive, contradiction, induction, counterexamples, writing a proof another person can check | How to Prove It, Daniel Velleman. Lighter option: How to Think Like a Mathematician, Kevin Houston |

All of it is free except the 0.6 books. Do 0.1 to 0.3 in order; run 0.4 and 0.5 alongside from the first week; start 0.6 after 0.2 and run it alongside 0.3.

**Exit test**

- [ ] A GCSE Higher non-calculator past paper, timed, at 80% or better (exam boards publish them free)
- [ ] Khan Academy Precalculus course challenge at 85% or better
- [ ] Zetamac score of 25 or more on default settings
- [ ] Five short statements proved, one each by direct proof, contrapositive, contradiction, induction and counterexample, written so a stranger can check every step **[Pure maths]**
- [ ] You can make a folder, write a ten-line Python script in it and run it from the terminal

## Stage 1: Foundations (1,650 hours)

This is the post's Tier 1 put into a fixed order, with one resource chosen per topic. Python comes first so that every maths topic after it can be checked in code; C++ comes last of the original nine. Items 1.10 and 1.11 add what a maths degree teaches and the post leaves out: proof-based analysis and linear algebra, complex numbers, vector calculus and differential equations. Start 1.10 after 1.4 and 1.11 after 1.10; finish both before Stage 2.

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

### 1.4 Linear algebra (150 h)

- **Use:** the post's Strang, Introduction to Linear Algebra, with his MIT 18.06 lectures (free). Watch 3Blue1Brown's Essence of Linear Algebra first.
- **Not yet:** Axler is a proof-based second course and the wrong first book; it is the text for 1.10. Horn and Johnson is a reference; skip it.
- **Cover:** elimination, vector spaces, rank, orthogonality, projections, least squares, determinants, eigenvalues, the singular value decomposition, positive definite matrices.
- **Exit:** the 18.06 final at 70%, and least squares and principal component analysis written in NumPy from the matrix operations.

### 1.5 Probability (250 h): the priority

The post is right that this is where most of the effort goes. It is the subject interviews test hardest.

- **Use:** Introduction to Probability by Blitzstein and Hwang (free online) with the Harvard Stat 110 lectures. It is driven by problems and is the closest textbook to interview style. The post's Toronto text (Evans and Rosenthal, free) is a sound alternative.
- **Cover:** counting, conditional probability, Bayes' rule, random variables, expectation and its linearity, indicator variables, variance and covariance, the named distributions, joint and conditional distributions, conditional expectation, the law of large numbers, the central limit theorem, Markov chains, random walks, the Poisson process, a first look at martingales and optional stopping. The last three are an added level **[Quant: all roles; optional stopping is a common interview question]**.
- **Exit:** two Stat 110 past finals at 70%.

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

### 1.10 Analysis and proof-based linear algebra (130 h, after 1.4) **[Pure maths]**: missing from the post

Calculus and linear algebra so far have been computational. This item proves why they work, which is how a maths degree teaches them and how research papers argue. It is not needed to be hired, but research roles that hire maths PhDs will notice its absence.

- **Use:** Understanding Analysis by Stephen Abbott for analysis. Then the post's Axler, Linear Algebra Done Right (the fourth edition is free online), now in its proper place as the second course.
- **Cover, analysis:** the real numbers and completeness, sequences and their limits with epsilon and N, series and convergence tests, continuity with epsilon and delta, the derivative and the mean value theorem proved, uniform convergence, the Riemann integral defined, metric spaces, open and closed sets, compactness.
- **Cover, linear algebra:** abstract vector spaces, linear maps, kernel and image, rank-nullity proved, dual spaces, inner product spaces, the spectral theorem proved, the Jordan form.
- **Exit:** a proof-based analysis final (MIT 18.100A past papers are free) at 60%; prove rank-nullity and the spectral theorem for symmetric matrices without notes.

### 1.11 Complex numbers, vector calculus and differential equations (120 h, after 1.10): missing from the post

Complex numbers 30 h **[Quant]**, vector calculus 30 h **[Pure maths]**, differential equations 60 h **[Quant]**.

Pricing models are differential equations, and Fourier methods for option pricing run on complex numbers. A degree covers both in the first two years.

- **Use:** MIT 18.03 Differential Equations (free lectures and problem sets) as the core, with the second half of 18.02 for vector calculus. For complex numbers, Visual Complex Analysis by Tristan Needham, its chapters on the geometry, differentiation and integration.
- **Cover, complex numbers [Quant: desk quant, Fourier option pricing]:** arithmetic and the complex plane, Euler's formula, roots of unity, complex functions, differentiability, contour integrals and residues, enough to invert a Fourier transform.
- **Cover, vector calculus [Pure maths]:** line integrals, surface integrals, Green's theorem, Stokes' theorem, the divergence theorem.
- **Cover, differential equations [Quant: desk quant and rates]:** first-order equations, linear second-order equations, systems and phase planes, stability, the Laplace transform, numerical solution with Euler and Runge-Kutta, a mean-reverting equation as the drift of an interest rate model.
- **Exit:** the 18.03 final at 70%; solve one equation numerically in NumPy and match its closed form to four decimal places.

## Stage 2: Intermediate (940 hours)

This is the post's Tier 2. Choose a track before starting, because the three roles are interviewed differently and the post treats them as one.

| Track | Interviews test | Weight in Stages 2 and 3 |
| --- | --- | --- |
| Trader | Probability, mental arithmetic, market-making and betting games | Probability drills, options, one project |
| Researcher | Probability, statistics, regression, machine learning, a data take-home | 2.1, 2.2, projects 1 and 2, paper replication |
| Developer | Algorithms, C++, systems design | C++, contests, projects 1 and 4 |

### 2.1 Machine learning (200 h)

- **Use:** An Introduction to Statistical Learning with Python (free PDF) as the core text. The post marks it optional; for quant work it is the reverse, because most models in use are linear, regularised or tree-based and the hard part is validation.
- **Alongside, for code:** the post's Géron. A [PyTorch edition](https://www.oreilly.com/library/view/-/9798341607972) came out in October 2025; the post lists the older Keras and TensorFlow one.
- **Videos:** the post's CampusX series is, to my knowledge, taught largely in Hindi, so check before committing. Andrew Ng's Machine Learning Specialization and StatQuest cover the same ground in English.
- **Then one applied book:** Advances in Financial Machine Learning (López de Prado) for method: labelling, purged cross-validation, backtest overfitting. Or the post's Jansen for breadth and a code repository. Isichenko is dense and worth the time only on the researcher track.
- **Exit:** one tabular prediction problem done end to end with time-ordered cross-validation, and you can explain leakage, regularisation and the bias-variance trade-off without notes.

### 2.2 Time series (60 h): missing from the post

- **Use:** [Forecasting: Principles and Practice, the Pythonic Way](https://otexts.com/fpppy) (Hyndman and co-authors, free online) for the core. Analysis of Financial Time Series by Ruey Tsay for volatility models and cointegration.
- **Cover:** stationarity, autocorrelation, ARMA models, volatility clustering and GARCH, cointegration.
- **Exit:** test a pair of price series for cointegration, and explain why models are fitted to returns and not prices.

### 2.3 Projects (400 h)

Do three properly, not five thinly. These are the post's five, re-ranked by how much they prove to someone reading your CV.

1. **Backtesting engine** (post's no. 1). Add what the post leaves out: transaction costs, slippage, a check against look-ahead, and a held-out period. Report Sharpe, Calmar and maximum drawdown.
2. **Alpha signal research** (post's no. 4). Cross-sectional momentum and mean reversion across a few hundred shares. Report information coefficient, turnover and Sharpe after costs. This is the closest of the five to real research work.
3. **Options analytics dashboard** (post's no. 3). Implied volatility surface and Greeks, with Black-Scholes, binomial and Monte Carlo pricers compared. For data, yfinance option chains on US shares or Deribit's public API work in place of NSE.
4. **Live market data handler** (post's no. 5). Websocket ticks into multi-timeframe candles, stored in PostgreSQL or Redis, with latency measured. On the developer track, write it in C++.
5. **Trading bot** (post's no. 2). Paper trading only, built on projects 1 and 4. It ranks last because EMA, RSI and Supertrend rules are retail technical analysis and carry no weight with a professional reader.

Every project ships with a README, tests, and a one-page results note that includes what failed. Treat any simple rule that backtests to a Sharpe above 2 as a bug until you have proved otherwise.

Library notes on the post's list: Quandl is now Nasdaq Data Link; zipline is no longer maintained, so use zipline-reloaded or your own engine; yfinance breaks often, so cache data to disk.

### 2.4 Contests (140 h, spread across the stage)

- **Use:** Codeforces, the post's first pick. Start once you have 100 problems behind you and enter one contest a week. A rating of 1400 is a fair first-year target.
- **How much it counts:** rating-based shortlisting is mainly a feature of Indian campus hiring. Elsewhere a rating helps developer applications and counts for little in trader or researcher interviews.
- **Add:** Kaggle competitions on the researcher track, firm-run trading competitions such as IMC Prosperity on the trader track, and Project Euler for maths with code.

### 2.5 Numerical methods and optimisation (90 h, alongside 2.3) **[Quant: all roles]**: missing from the post

Every pricer, fit and portfolio in the projects is a numerical method. This item says when each one is accurate and when it fails.

- **Use:** Numerical Linear Algebra by Trefethen and Bau, lectures 12 to 17 on conditioning and stability. Convex Optimization by Boyd and Vandenberghe (free PDF), chapters 1 to 5, with the Stanford EE364A lectures.
- **Cover, numerical methods:** floating point and rounding error, conditioning and stability, root finding, interpolation, quadrature, ODE solvers and their step size, finite differences for a pricing equation, Monte Carlo and variance reduction.
- **Cover, optimisation:** convex sets and functions, linear programming, duality, the KKT conditions, quadratic programmes for portfolios, gradient descent and Newton's method and their convergence.
- **Exit:** price one European option by finite differences, quadrature and Monte Carlo with a control variate, and explain each method's error; solve a constrained mean-variance problem through the KKT conditions by hand and match a solver.

### 2.6 Statistical modelling (50 h, after 2.1) **[Quant: researcher track]**: missing from the post

Regression in 1.6 assumed normal errors. This item covers the models a statistics degree adds next.

- **Use:** Regression and Other Stories by Gelman, Hill and Vehtari (free PDF). All of Statistics by Larry Wasserman, chapters on nonparametric methods.
- **Cover:** generalised linear models (logistic and Poisson), analysis of variance, design of experiments, nonparametric and rank tests, Bayesian inference with conjugate priors, Markov chain Monte Carlo, hierarchical models.
- **Exit:** fit a logistic and a Poisson model by your own iteratively reweighted least squares and match statsmodels; fit a Bayesian model by Markov chain Monte Carlo and check that the chains have converged.

## Stage 3: Advanced (400 hours)

This is the post's Tier 3: papers, then interview preparation. Interview drilling starts here in earnest, but the weekly probability problems since 1.5 mean you are not starting cold.

### 3.1 Research papers (150 h)

- **Where:** the post's three sources: SSRN, arXiv Quantitative Finance and WorldQuant BRAIN.
- **Method:** replicate before you read widely. Pick one classic, reproduce its main table, then extend it to data from after publication.
- **Starting list:** Jegadeesh and Titman (1993) on momentum. Fama and French (1993) on the three-factor model. Gatev, Goetzmann and Rouwenhorst (2006) on pairs trading. Avellaneda and Stoikov (2008) on market making. Harvey, Liu and Zhu (2016) on multiple testing in factor research.
- **Exit:** one replication on GitHub with an out-of-sample extension and a plain note on how much of the effect survived.

### 3.2 Stochastic calculus (optional, hours not counted) **[Quant: desk quant and derivatives pricing]**: missing from the post

- **Who needs it:** derivatives pricing and desk quant roles. It is rarely tested for trading or statistical research roles.
- **Use:** Stochastic Calculus for Finance, volumes I and II, by Steven Shreve. Probability with Martingales by David Williams for the measure theory. Partial Differential Equations: An Introduction by Walter Strauss, chapters 1 to 4.
- **Cover, measure-theoretic probability:** sigma-algebras, measures, the Lebesgue integral, conditional expectation as a projection, filtrations, martingales, stopping times, the Radon-Nikodym derivative and change of measure.
- **Cover, stochastic calculus:** Brownian motion, the Itô integral, Itô's lemma, stochastic differential equations, Girsanov's theorem, risk-neutral pricing.
- **Cover, partial differential equations:** the heat equation, separation of variables, Fourier series, the Black-Scholes equation turned into the heat equation, Feynman-Kac, finite-difference solution.
- **Exit:** derive the Black-Scholes equation with Itô's lemma, solve it through the heat equation, and match a finite-difference price to the closed form to four decimal places.

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

### 3.4 Pure mathematics (optional, hours not counted) **[Pure maths]**: missing from the post

- **Who needs it:** anyone aiming at research roles that hire maths PhDs, or who wants to read proofs in papers without stalling. It is rarely tested at interview beyond modular arithmetic and permutations.
- **Use:** A Book of Abstract Algebra by Charles Pinter. Introduction to Metric and Topological Spaces by Wilson Sutherland.
- **Cover, algebra:** groups, subgroups and cosets, permutations, modular arithmetic, homomorphisms, rings, fields, polynomials over a field.
- **Cover, topology:** metric spaces revisited, topological spaces, continuity, connectedness, compactness, completeness and the contraction mapping theorem.
- **Exit:** a sample of Pinter's end-of-chapter exercises across groups, rings and fields at 70%; prove the contraction mapping theorem and use it to show a fixed-point iteration converges.

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
| Axler listed first for linear algebra | Strang first, Axler in 1.10 | Axler is a proof-based second course |
| Toronto text or DeGroot for probability | Blitzstein and Stat 110, the post's picks as alternatives | Closer to interview problems |
| Finance basics optional | Required | Traders and researchers are asked about markets |
| ISLR optional | Core text | Validation and linear models are most of quant machine learning |
| Géron, Keras and TensorFlow edition | PyTorch edition | Newer edition, October 2025 |
| CampusX videos | English alternatives named | Teaching language, to my knowledge Hindi |
| NSE and Indian broker data | US shares and Deribit options data | Free, no broker account needed |
| Indicator bots as a headline project | Ranked last, paper only | Retail technical analysis proves nothing to a professional |
| Codeforces rating as a hiring filter | Demoted outside the developer track | Mainly an Indian campus-hiring practice |
| Zhou credited with Quant Job Interview Questions and Answers | Two separate books, both listed | That title is Joshi's; Zhou wrote A Practical Guide to Quantitative Finance Interviews ([comparison](https://quantvault.org/best-quant-interview-books.html)) |
| The Puzzle Palace | Left out | I could not identify the resource |
| Nothing on tools, time series, stochastic calculus, mental arithmetic or market-making games | All added | Used daily on the job or tested at interview |
| Nothing on proof, analysis, differential equations, numerical methods, optimisation or statistical models beyond regression | Items 0.6, 1.10, 1.11, 2.5, 2.6 added; measure theory and PDEs in 3.2; optional pure mathematics in 3.4 | A maths degree teaches them, desk quant roles use them, and research papers assume them |

## Sources

- Quant Roadmap, Priyanshu Priyank, Quant Memo: the 16-slide post this is built on
- [Hands-On Machine Learning with Scikit-Learn and PyTorch, O'Reilly](https://www.oreilly.com/library/view/-/9798341607972)
- [Forecasting: Principles and Practice, the Pythonic Way](https://otexts.com/fpppy)
- [The Best Quant Interview Books, Compared, QuantVault](https://quantvault.org/best-quant-interview-books.html)

Hours are my estimates for a learner starting from zero, not sourced figures.
