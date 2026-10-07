# Canon and gap analysis

Working paper for the Stage 2 Blueprint, 6 October 2026, **revision 2**. Scope: what the programmes that produce the strongest quants and ML-lab researchers treat as core, set against `docs/curriculum.md`; which gaps to propose to the owner, with hours and slots; and the resource canon, the university-grade texts, lecture series and problem sets that each curriculum item will cite. Input to `docs/PLAN.md` (curriculum proposals, content order) and to `content/sources.yaml` (`content-format.md` 3.2 `Source`, 9.4).

**Revision 2** (same day) keeps every section number, every proposal number (P1 to P16, O1), every gap number (G1 to G18) and every `src.*` id of revision 1 but one (`src.kurose-ross-8e`, renamed for a new edition and cited nowhere else), because `content-format.md`, `assessment.md`, `ai-tutor.md` and the curriculum files in `docs/curriculum/` cite them. It reconciles this paper with what was written after it: the curriculum files, which moved part of several proposals inside the existing hours; `content-format.md` revision 2; `arch-decision.md`; and the platform spikes (`spikes/README.md`). It also re-runs the survey searches for the items revision 1 left [recalled] or [unverified]. Section 0.5 lists every change and its reason; section 8 holds the reconciliation tables.

**The curriculum is the owner's.** Sections 3 and 4 are proposals. Nothing here edits `docs/curriculum.md`. The owner accepts, trims or rejects each line, and only accepted lines enter the content plan.

**How to read it.**

- Section 0 is the summary: every proposal with hours, slot and verdict, the canon decisions, and what revision 2 changed.
- Section 1 says how the survey was done and what could not be checked.
- Section 2 is the survey: each programme's core, the pattern across them, and a coverage matrix.
- Section 3 is the gap analysis, one entry per gap.
- Section 4 is the recommendation: priorities, hours per track, a minimum set, exit tests, and what is not worth adding.
- Section 5 says what the proposals ask of the engine, the widget library and the Python runtimes, which are built first.
- Section 6 is the resource canon, item by item, with `src.*` ids and a table of where solutions exist.
- Section 7 lists the decisions the owner needs to make.
- Section 8 reconciles this paper with the curriculum files: id map, hours already absorbed, spine and licence changes, follow-ups for other files.

**Evidence tags.** [searched] confirmed by a web search on 6 October 2026 (results listed under Sources). [measured] read from a file on this machine (the Pyodide 314.0.7 lock file, section 5.3). [recalled] from memory and confident; a person should confirm before a lesson relies on it. [unverified] not confident (an edition, a year, a chapter number, or whether solutions are public); check before citing. [our estimate] hours I estimated. [our choice] a decision without outside evidence. [inferred] a deduction from tagged facts.

---

## 0. Summary

### 0.1 Proposals

| # | Proposal | Hours (rev. 2) | Rev. 1 | Slot (working label) | Tracks | Priority |
|---|---|---|---|---|---|---|
| P1 | Research method and statistical honesty | 35 | 40 | New Stage 2 item before 2.3 Projects (2.2c) | All | 1 |
| P2 | Stochastic processes, continuous time | +15 | +40 | Extension of 1.5 Probability (250 to 265 h) | All | 1 |
| P3 | Numerical methods and Monte Carlo | 120 | 120 | New first item of Stage 2 (2.0a) | All | 1 |
| P4 | Optimisation | 80 | 80 | New Stage 2 item after P3 (2.0b) | All | 1 |
| P5 | Statistical inference, second pass (dependent data, heavy tails, GLMs, covariance) | +25 | +40 | Extension of 1.6 Statistics (120 to 145 h) | All | 2 |
| P6 | Portfolio theory, risk and fixed income | 75 | 80 | New Stage 2 item after P4 (2.0c) | Trader, Researcher | 2 |
| P7 | Proof and discrete mathematics | 70 | 90 | New Stage 1 item between 1.4 and 1.5 (1.4b) | All | 2 |
| P8 | Differential equations, second order and systems | 45 | 50 | New Stage 1 item after 1.6 (1.6b) | All | 3 |
| P9 | Information theory essentials | +20 | +25 | Opening of 2.1 Machine learning | All | 3 |
| P10 | Matrix calculus for learning (the part 1.4 does not hold) | +10 | +20 | Opening of 2.1, beside P9 (was: extension of 1.4) | All | 3 |
| P11 | Financial econometrics and empirical asset pricing, plus a time-series extension | 80 + 15 | 80 + 20 | New Stage 2 item after 2.2 (2.2b); 2.2 from 60 to 75 h | Researcher | 2 |
| P12 | Market microstructure and execution | 50 | 50 | New Stage 2 item after P6 (2.0d) | Trader | 2 |
| P13 | Computer systems, concurrency and performance | 150 | 150 | New Stage 2 item after 1.9 (2.0e) | Developer | 1 (developer) |
| P14 | ML research track: deep learning 150, language models from scratch 120, learning theory 60, reinforcement learning 50 | 380 | 380 | A fourth Stage 2 track | ML research | 2 |
| P15 | Bayesian computation | 40 | 50 | Elective | Researcher, ML research | 3 |
| P16 | Derivatives add-on: real analysis 120, measure-theoretic probability 100, stochastic calculus 150 (3.2, now counted) | 370 | 370 | Optional, after Stage 2 | Desk quant, theory-minded | 3 |
| O1 | Offset: 2.4 Contests from 140 to 60 h outside the developer track | -80 | -80 | 2.4 | Trader, Researcher, ML research | 1 |

**Why ten proposals shrank.** The curriculum files written after revision 1 put first passes of several proposals inside the existing hours: martingales, optional stopping, Wald's identity, the pattern martingale, Poisson thinning and the reflection principle in 1.5 (levels Z3 and Z4); Fisher information, the delta method, the bootstrap, permutation tests, the false discovery rate and logistic regression in 1.6; first-order differential equations in 1.3 (level I6); gradients of quadratic forms, Eckart-Young, covariance shrinkage and gradient descent in 1.4; backpropagation and automatic differentiation in 1.3; proof by contrapositive, contradiction and induction in 0.3 (levels R1 and R2). Counting those hours twice would overstate the cost. Section 8.2 itemises every reduction.

Working labels only. The engine computes display numbers from position (`content-format.md` decision 4), so inserting an item renumbers nothing a learner has stored.

### 0.2 Hours if every proposal is accepted

| Track | Today | With proposals | Change | At 15 h a week | At 25 h a week |
|---|---|---|---|---|---|
| Trader | 3,100 | 3,565 | +465 | 4.6 years | 2.7 years |
| Researcher | 3,100 | 3,610 (3,650 with P15) | +510 | 4.6 years | 2.8 years |
| Developer | 3,100 | 3,670 | +570 | 4.7 years | 2.8 years |
| ML research (new) | none | 3,820 (3,860 with P15) | | 4.9 years | 2.9 years |
| Derivatives add-on (P16) | 0 (3.2 uncounted) | +370 on any track | | +0.5 years | +0.3 years |

Years assume 52 working weeks, as the curriculum's own "roughly 4 years at 15 hours a week" for 3,100 hours does. Revision 1's totals were 3,655 to 3,905 hours; `assessment.md` 6.5 and 8.7 quote them and need the new figures (section 8.4).

**Minimum set** if the owner wants to cap the growth: P1, P2, P3 and P4 with offset O1. That is +170 h net (3,270 h) outside the developer track and +250 h (3,350 h) on it. These four have the most value per hour: P3 is core in nearly every financial-engineering master's (section 2.2); P4 is core in the operations-research route and underlies both portfolio construction and ML training; P2 completes the stochastic-process material interviews test, at 15 hours now that 1.5 holds the discrete part; P1 prevents the most common failure in the projects the curriculum already sets.

### 0.3 Not proposed

Abstract algebra, geometry and topology; complex analysis and Fourier methods as a separate course; corporate finance and accounting; macroeconomics; credit, XVA and term-structure models; kdb+/q; a distributed-systems course; graduate probability (Durrett's *Probability: Theory and Examples* level) outside P16; stochastic control as a course; quantum and blockchain topics; contest ratings above the curriculum's 1400 target. Reasons in section 4.5.

### 0.4 Decisions about the canon

| # | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| 1 | How many resources per item | **One spine plus up to three in fixed roles**: lectures, problems, stretch | Two or three equal texts | Keeps the curriculum's rule 1 ("one resource per topic") for reading, while giving homework a problem source and lessons a lecture to parallel |
| 2 | Whose spine | **The owner's pick stays the spine.** Where the curriculum offers two (1.1 "CS50P or Automate the Boring Stuff"; 1.3 "Stewart, or OpenStax"), the curriculum file for that item chooses, and this paper follows it. University-grade alternatives go into the other roles | Replacing Stewart with Apostol, DeGroot with Casella and Berger, and so on | The curriculum is the owner's; its picks are sound for a learner from zero. Revision 2 follows `stage1-calculus.md` decision 2: OpenStax is the 1.3 spine because it is free on every device; Stewart becomes the alternative |
| 3 | Role names | Map to `Citation.use` (`content-format.md` 3.2): spine = `basis`, lectures = `parallel-reading`, problems = `problem-inspired`, stretch = `further` | New role names | One vocabulary across papers |
| 4 | Editions | **Pin the edition in `sources.yaml`** and cite chapter and section by that edition; `checked: false` until a person with the book confirms; cite by chapter title where the number is [unverified] | Citing titles without editions | Chapter numbers move between editions: Strang's 6th edition reorganised its opening chapters to introduce rank and column space early [searched]; Luenberger's 2nd edition added chapters on risk management, credit risk, and data and statistics [searched] |
| 5 | Problem sets | **Homework mirrors problem types, never wording** (`problem-inspired`); MIT OpenCourseWare and the OpenStax calculus volumes stay `problem-inspired` only | Adapting OCW or OpenStax Calculus problems | `content-format.md` 9.4: CC BY-NC-SA adaptation would bind our content to its terms. OpenStax Calculus volumes 1 to 3 are CC BY-NC-SA 4.0 [searched], not CC BY as revision 1 said |
| 6 | Id rule (new) | **Books** `src.<author or short title>[-<n>e]`; **courses** `src.<school>-<number>[-<year>]`; **papers** `src.<surnames or the field's standard acronym>-<year>`. Revision 1 ids stand; a duplicate proposed by a curriculum file maps to the revision 1 id (section 8.1) | Renaming revision 1's acronym ids (`src.hlz-2016`) to surname ids | Other papers already cite revision 1 ids (`content-format.md`, `ai-tutor.md`, two curriculum files). `sources.yaml` does not exist yet, so the map costs nothing now and an id is immutable once it is written there |
| 7 | Solutions (new) | **Every item names at least one problem source whose solutions are public**, or says that none exists and the app must write and verify its own worked solutions (section 6, "Where the solutions are") | Problem sources chosen by reputation alone | Homework that mirrors a problem set is only checkable by the learner when the set's solutions exist; where they do not, the verifier (`content-format.md` decision 7) carries the load |

### 0.5 What revision 2 changed, and why

| # | Change | Sections | Source |
|---|---|---|---|
| 1 | Ten proposals shrink (P1, P2, P5, P6, P7, P8, P9, P10, P11's extension, P15), by 105 h in all; P10 moves from 1.4 to the opening of 2.1 | 0.1, 0.2, 3, 4, 8.2 | The curriculum files put first passes inside existing hours (section 8.2) |
| 2 | Track totals 3,565 to 3,820 h (were 3,655 to 3,905); minimum set +170 h net (was +200) | 0.2, 4.2, 4.3 | Change 1 |
| 3 | 1.3 spine becomes OpenStax Calculus; its licence is CC BY-NC-SA 4.0, so its exercises are `problem-inspired` only | 0.4, 6 (1.3) | `stage1-calculus.md` decision 2 and open item 5; [searched] |
| 4 | P2 spine becomes Durrett, *Essentials of Stochastic Processes*, 3rd ed; Grimmett and Stirzaker move to problems and stretch; MIT 6.262 (Spring 2011) added as lectures; 18.445's scope corrected | 3 (G3), 6 (1.5) | 1.5 now holds the discrete material; Durrett's six chapters match what is left [searched] |
| 5 | Python package facts per proposal, from the Pyodide 314.0.7 lock file: cvxpy-base, clarabel, highspy and statsmodels exist; PyMC, NumPyro, PyTorch, JAX, linearmodels and arch do not. P15's exit no longer compares against PyMC in the browser | 3 (G2, G11, G15), 5.3 | [measured]; `spikes/README.md`; `arch-decision.md` 6.3.3 |
| 6 | Runtime notes follow the spike: NumPy and pandas run inside the Artifact; SciPy, statsmodels and scikit-learn there depend on the 120 MB budget measured at stage E8 | 5.1, 5.3 | `spikes/README.md`; `arch-decision.md` decision 16 and its risk table |
| 7 | 51 ids added (23 the curriculum files requested, 12 more they use or `curriculum.md` names, 16 from this revision's searches and gaps); 7 duplicates mapped; `src.kurose-ross-8e` becomes `src.kurose-ross-9e`; `src.islr-2e` maps to `src.islp-2023` | 6, 8.1 | `stage1-linear-algebra.md` and `stage1-statistics-ts.md` request tables; [searched] |
| 8 | Editions and facts confirmed: Sweigart 3rd ed (2025), Bhargava 2nd ed (2024), Foucault, Pagano and Röell 2nd ed (2023), Crack 24th ed (2023), Stefanica and co-authors 3rd ed, Kurose and Ross 9th ed (2025), Tuckman and Serrat 4th ed (2022), Grimmett and Stirzaker's *One Thousand Exercises* 3rd ed (2020), Hull 11th ed chapter list, Grinold and Kahn chapter list, Strang's heat equation in chapter 8, the PBO paper (J. Computational Finance 20(4), 2017), Almgren and Chriss (Journal of Risk 3(2), winter 2000/01), Ghosh (Packt 2023) | 6 | [searched] |
| 9 | Survey additions: Cambridge Part IA titles; Stanford CS106A and CS106B; CS231n Spring 2025 videos; CS336 Spring 2026; MIT 6.036 (Fall 2020), 18.600 (Fall 2019), 15.433 (Spring 2003), 6.262 (Spring 2011), 18.445 (Spring 2015), 18.175 (Spring 2014), 14.384 (Fall 2013); Harvard Stat 110's practice materials | 2.1, 6 | [searched] |
| 10 | Missing Semester 2026 is the 0.4 and 1.2 lecture parallel; 2020 kept for the lectures 2026 dropped | 6 (0.4, 1.2) | [searched] |
| 11 | P1's reading pack gains Arnott, Harvey and Markowitz's backtesting protocol (2019) and three method papers; P13 gains a free spine alternative (OSTEP) | 6 (2.2c, 2.0e) | [searched] for Arnott and OSTEP; the rest [recalled] |
| 12 | Coverage matrix and gap texts describe the curriculum as the curriculum files now teach it, not only as `curriculum.md` lists it | 2.3, 3 | Change 1 |
| 13 | Section 6 gains "Where the solutions are"; section 8 is new | 6, 8 | Decision 7 |

---

## 1. Method and limits

- **Searches.** About 30 web searches for revision 1 and about 40 more for revision 2 on 6 October 2026, one or more per programme, plus edition, licence and table-of-contents checks for books whose details matter. Results are under Sources.
- **Blocked pages.** Direct fetches of `maths.cam.ac.uk`, `courses.maths.ox.ac.uk`, `cmu.edu` and `imperial.ac.uk` were blocked by this environment's egress proxy, and still were for revision 2 (the Cambridge Part IA lecture list PDF). Course lists tagged [searched] therefore come from search-result summaries of those pages, not from reading the pages. Course titles are reliable at that depth; lecture-by-lecture syllabi are mostly [recalled].
- **Measured.** The Pyodide 314.0.7 package lock (`pyodide-lock.json`, 357 packages, Python 3.14.2) from the spike's scratch install was read directly for section 5.3. It says which packages exist, not whether each imports and runs on an iPhone; only NumPy and pandas were run there (`spikes/README.md`).
- **What "core" means here.** Required in a programme, or required in the undergraduate degree that feeds it. Cambridge Part IA is compulsory; Part IB and Part II courses are chosen, so they count as "taught", not "required" [recalled].
- **Hours.** An MIT 12-unit course is about 12 hours a week for 14 weeks, roughly 170 hours [recalled]. Oxford MCF core courses are 16 lectures and 4 classes of 1.5 hours [searched], about 80 to 100 hours with private study [our estimate]. Proposed hours assume an adult who has finished the items before the slot, cover the subset of a course that the quant or ML use needs, and now exclude what the curriculum files already teach (section 8.2). All proposed hours are [our estimate].
- **What was not surveyed.** Firm-internal training, PhD programmes, and the "ML lab" side as a hiring process. The ML research track (P14) is built from the courses that frontier-lab researchers commonly cite (MIT 6.7960, Stanford CS229, CS231n, CS336), not from lab job descriptions.

---

## 2. Survey

### 2.1 What each programme treats as core

**Cambridge Mathematical Tripos.**

- Part IA, compulsory: Numbers and Sets (proof), Groups, Vectors and Matrices, Differential Equations, Analysis I, Probability, Vector Calculus [searched: titles in the 2025-26 lecture list], Dynamics and Relativity [recalled].
- Part IB, chosen: Linear Algebra, Analysis and Topology, Complex Analysis or Complex Methods, Methods (Fourier series, PDEs), Numerical Analysis, Statistics, Markov Chains, Optimisation (12 lectures), plus pure and applied courses not relevant here [searched for Markov Chains, Statistics and Optimisation in the 2025-26 lecture lists; the rest recalled. A revision 2 search summary placed Optimisation in the Part IA list; I could not open the PDF to check, and keep it in Part IB as in earlier years [unverified]].
- Part II, chosen: Probability and Measure, Applied Probability, Principles of Statistics, Stochastic Financial Models (example sheets for 2025-26 are posted), Mathematics of Machine Learning, Statistical Modelling, Numerical Analysis, Optimisation and Control, Coding and Cryptography [searched for Probability and Measure, Principles of Statistics and Stochastic Financial Models; the rest recalled].
- The shape: proof and analysis from the first term; probability in year one, then Markov chains, statistics, optimisation and numerical analysis in year two; measure and stochastic finance in year three.

**Oxford.**

- Undergraduate Mathematics: Prelims analysis, linear algebra, probability, statistics and an introduction to proof; Part A Integration (Lebesgue), Probability, Statistics, Numerical Analysis, Differential Equations; Part B Probability, Measure and Martingales, and B8.2 Continuous Martingales and Stochastic Calculus (16 lectures) [searched for B8.2; the rest recalled].
- MSc in Mathematical and Computational Finance [searched]: an introductory week on partial differential equations, probability and statistics, financial markets and instruments, and Python. First-term core: Stochastic Calculus, Financial Derivatives, Numerical Methods, Statistics and Financial Data Analysis, Financial Computing with C++ I. Second-term core: Deep Learning, Quantitative Risk Management, Stochastic Control, Fixed Income. Electives: Advanced Volatility Modelling, Advanced Monte Carlo Methods, Advanced Numerical Methods. A dissertation closes the year.

**Imperial MSc Mathematics and Finance** [searched]: seven compulsory modules: Fundamentals of Option Pricing, Statistical Methods for Finance, Stochastic Processes, Quantitative Risk Management, Interest Rates Models, Computing for Finance (Python and C++), Simulation Methods for Finance. Electives include Numerical Methods in Finance, Deep Learning, Optimization in Machine Learning, Reinforcement Learning. A research project.

**Carnegie Mellon.**

- Undergraduate [searched]: 21-127 Concepts of Mathematics (proof; prerequisite for every theoretical course), 21-355 Real Analysis I, and for the Computational Finance minor 21-241 Matrices and Linear Transformations, 21-259 Calculus in Three Dimensions, 21-260 Differential Equations, 21-370 Discrete-Time Finance, 21-420 Continuous-Time Finance. Also 36-225 and 36-226 probability and inference, 15-213 Introduction to Computer Systems and 10-301/601 Introduction to Machine Learning [recalled].
- MSCF [searched]: Stochastic Calculus I and II, Probability and Statistical Inference, Regression Analysis and Time Series Analysis, Financial Computing I to IV, Multi-Period Asset Pricing, Statistical Arbitrage, Monte Carlo Simulation, Quantitative Asset Management, Credit Derivatives. The programme names Monte Carlo simulation, optimisation and the numerical solution of PDEs in C++ and Python, a sequence of data-science, machine-learning and time-series courses, and applications in asset management, statistical arbitrage, risk management and market microstructure.

**Baruch MFE** [searched]: required MTH 9814 Financial Markets and Securities, MTH 9815 Software Engineering for Finance, MTH 9821 Numerical Methods for Finance, MTH 9831 Probability and Stochastic Processes for Finance I, MTH 9903 Capstone. Electives include MTH 9875 The Volatility Surface. The Pre-MFE seminars, which the programme recommends before entry: Advanced Calculus with Financial Engineering Applications, Probability Theory for Financial Applications, Numerical Linear Algebra for Financial Engineering, C++ Programming for Financial Engineering, and from Spring 2026 Machine Learning for Financial Engineering Applications. Baruch faculty also write the interview book in 3.3 (Stefanica, Radoičić and Wang, now in a 3rd edition that adds statistics and machine learning [searched]).

**Princeton ORFE** [searched]: four core courses: ORF 245 Fundamentals of Statistics (estimation, intervals, tests, regression, classification), ORF 307 Optimization (linear optimisation, duality, simplex and interior-point methods, network flows, integer programming), ORF 309 Probability and Stochastic Systems (Poisson processes, random walks, Brownian motion, branching processes, Markov chains), ORF 335 Introduction to Financial Mathematics (discrete-time risk-neutral pricing, Black-Scholes, Heston).

**MIT.**

- 18.01, 18.02, 18.03, 18.06 (calculus, multivariable calculus, differential equations, linear algebra) [recalled]; the OCW 18.01SC (Fall 2010) final and the 18.06 (Spring 2010) final are posted with solutions [searched].
- 18.05 and 18.600 (probability; 18.05 adds statistics) [recalled]; 18.600 Fall 2019 (Sheffield, on Ross's *A First Course in Probability*, with exams and solutions on OCW) [searched]; 18.650 Statistics for Applications, Fall 2016 (parametric inference, maximum likelihood, method of moments, tests, goodness of fit, regression, Bayesian statistics, PCA, generalised linear models) [searched].
- 18.065 Matrix Methods in Data Analysis, Signal Processing, and Machine Learning, Spring 2018 (SVD, weighted least squares, PCA, covariance matrices, graphs, neural nets; Strang's *Linear Algebra and Learning from Data*) [searched]; 18.S096 Matrix Calculus for Machine Learning and Beyond, IAP 2023 (Edelman and Johnson; videos, notes, problem sets and solutions) [searched].
- 18.S096 Topics in Mathematics with Applications in Finance, Fall 2013: linear algebra, probability, statistics, stochastic processes and numerical methods, each followed by an industry lecture (yield-curve bootstrapping, value at risk, volatility estimation, Black-Scholes, PCA) [searched].
- Stochastic processes: 6.262 Discrete Stochastic Processes, Spring 2011 (Gallager; 25 video lectures: Poisson, renewal and Markov processes, random walks, martingales) [searched]; 18.445 Introduction to Stochastic Processes, Spring 2015 (Markov chains, random walks, martingales, Galton-Watson trees; homework with solutions) [searched]; 18.175 Theory of Probability, Spring 2014 (Sheffield, on Durrett's *Probability: Theory and Examples*) [searched].
- 18.100A Real Analysis, Fall 2020; 18.335J Introduction to Numerical Methods, Spring 2019 (floating point, backward error, conditioning, stability, dense and iterative linear algebra) [searched].
- 6.0001 (Fall 2016) and 6.100L (the OpenCourseWare form of 6.100A, Fall 2022) [searched for 6.100L; 6.0001 recalled]; 6.006 Spring 2020; 6.046J Spring 2015 [searched]; 6.036 Introduction to Machine Learning, Fall 2020, free on the Open Learning Library with auto-checked exercises (now numbered 6.390) [searched]; 6.7960 Deep Learning, Fall 2024 (architectures, backpropagation and autodiff, generalisation in high dimensions) [searched]; 6.172 Performance Engineering of Software Systems, Fall 2018 [searched].
- 15.401 Finance Theory I (Lo, Fall 2008) [recalled]; 15.433 Investments, Spring 2003 (portfolio theory, CAPM and APT, the cross-section and time series of returns, fixed income and credit, market efficiency, active management; 23 lectures of notes and assignments with solutions) [searched]; 14.384 Time Series Analysis, Fall 2013 (Mikusheva; stationary and non-stationary models, VARs, persistent series, structural breaks; five problem sets) [searched].

**Harvard** [searched]: Stat 110 (probability, Blitzstein): lecture videos, about 250 strategic-practice problems with detailed solutions, and practice finals; Stat 111 Introduction to Statistical Inference (Blitzstein and Shephard): frequentist and Bayesian model building, learning from data and decisions under uncertainty, taught through theory, simulation and data. Stat 111 has no public textbook or course archive that I could find [inferred from search results].

**Stanford.**

- CS106A (now taught in Python) and CS106B Programming Abstractions (C++; recursion, algorithm analysis, data abstraction, classic data structures; Roberts, *Programming Abstractions in C++*) [searched].
- STATS 116 Theory of Probability (text: Ross, *A First Course in Probability*, 10th edition) ran for the last time in autumn 2023 and is replaced by STATS 117 and STATS 118 (STATS 117 uses the online text *The Art of Chance* by Sun, Kim and Sood) [searched].
- STATS 200 Introduction to Statistical Inference: decision theory, point and interval estimation, Neyman-Pearson, Bayesian analysis, maximum likelihood, large-sample theory; text Rice, *Mathematical Statistics and Data Analysis*; the Autumn 2016 lecture page (Zhou Fan) is public [searched; whether every set of notes is open, check].
- MS&E 245A Investment Science: interest rates, bond valuation, portfolio design, risk measurement, CAPM; Luenberger's *Investment Science* is the field's standard text [searched].
- CS229 Machine Learning: Fall 2025 offering (supervised and unsupervised learning, learning theory, reinforcement learning) [searched]; Ng's Autumn 2018 lectures are on YouTube with four public problem sets [searched]. CS231n Deep Learning for Computer Vision: Spring 2025 lecture videos public, assignment starter code and notes public [searched]. CS336 Language Modeling from Scratch: Spring 2025 and Spring 2026 offerings, five assignments with public materials (tokenisation, a transformer, FlashAttention2 in Triton, scaling laws, data, reinforcement-learning fine-tuning) [searched]. EE364A [recalled].

**NYU Courant MS in Mathematics in Finance** [searched]: first-semester core MATH-GA.2791 Derivative Securities, MATH-GA.2751 Risk and Portfolio Management with Econometrics, MATH-GA.2902 Stochastic Calculus, MATH-GA.2041 Computing in Finance. Electives include Scientific Computing in Finance, Time Series Analysis and Statistical Arbitrage, Advanced Statistical Inference and Machine Learning. A capstone.

**Berkeley MFE** [searched]: required MFE 230A Investments and Derivatives, 230D Derivatives: Quantitative Methods, 230E Empirical Methods (maximum likelihood, GMM, GARCH, non-parametric methods), 230H Financial Risk Measurement and Management, 230I Fixed Income, 230P Financial Data Science, 230Q Stochastic Calculus with Asset Pricing Applications, 230O Applied Finance Project, and an internship.

**ETH Zurich and UZH MSc Quantitative Finance** [searched]: mathematical core: Mathematical Foundations for Finance, Statistical Foundations for Finance, Mathematics for New Technologies in Finance, Numerical Methods for Finance, Quantitative Risk Management; finance core: Asset Management, Intermediate Corporate Finance, Economic Foundations for Finance, Asset Pricing, Financial Engineering.

### 2.2 The pattern

1. **Nearly every financial-engineering master's teaches numerical methods as core.** Oxford (Numerical Methods), Imperial (Simulation Methods; Numerical Methods elective), CMU (Monte Carlo, PDE solvers), Baruch (MTH 9821, plus a pre-entry seminar on numerical linear algebra) and ETH (Numerical Methods for Finance) require it; NYU offers Scientific Computing in Finance as an elective; Berkeley's required list does not name it [searched]. Cambridge IB and MIT 18.335J teach it to undergraduates. The curriculum touches it in three lessons (binary floating point in 0.1, finite-difference error in 1.3, a quadrature preview in 1.3) and has no course.
2. **Every master's surveyed teaches stochastic processes and stochastic calculus as core** [searched, except ETH, where I take it to sit inside Mathematical Foundations for Finance [recalled]]. The curriculum files now teach the discrete-time half inside 1.5 (Markov chains, random walks, the reflection principle, Poisson processes, martingales and optional stopping). Continuous time is absent, and stochastic calculus is an optional, uncounted 3.2.
3. **Statistics is taught twice**: a first inference course (ORF 245, 18.650, STATS 200, Cambridge IB Statistics) and then econometrics or financial data analysis inside the master's (Berkeley 230E, NYU's Risk and Portfolio Management with Econometrics, Oxford's Statistics and Financial Data Analysis, CMU's Regression and Time Series, ETH's Statistical Foundations) [searched]. The curriculum has the first pass (1.6, which now reaches Fisher information, the bootstrap and HAC errors) and time series (2.2), not the second.
4. **Risk and fixed income are core in most masters**: Oxford (QRM, Fixed Income), Imperial (QRM, Interest Rates Models), Berkeley (230H, 230I), ETH (QRM), NYU (Risk and Portfolio Management) [searched]. The curriculum covers bonds only through Khan Academy in 1.7; the files add a minimum-variance lesson (1.3), covariance shrinkage (1.4) and a VaR backtest (2.2), but no course on portfolio construction or risk measures, although project 2 reports an information coefficient.
5. **Optimisation is core in the operations-research route** (Princeton ORF 307, Cambridge IB) and named in CMU's MSCF [searched]. The curriculum stops at Lagrange multipliers and the multiplier as a shadow price (1.3), with gradient descent on a quadratic in 1.4.
6. **Proof comes first in every undergraduate pipeline** (Cambridge Numbers and Sets, Oxford Prelims, CMU 21-127) [searched for Cambridge and CMU; recalled for Oxford]. `curriculum.md` never asks for a proof; the curriculum files add a proof thread at school-to-first-year level (0.3 levels R1 and R2; long-form proofs in 1.3, 1.5 and 1.6), but no course in proof as a subject.
7. **Deep learning has entered the core**: core at Oxford MCF, elective at Imperial, a new Baruch seminar, a required data-science course at Berkeley [searched]. The curriculum's 2.1 is classical machine learning, which is right for quant work, but it does not reach what an ML lab expects.
8. **C++ is core in every master's** (Oxford C++ I, Imperial Computing for Finance, CMU Financial Computing I to IV, Baruch MTH 9815, NYU Computing in Finance) [searched]. The curriculum has it (1.9). What the finance masters' course lists do not name, and the developer track needs, is computer systems: CMU 15-213 and MIT 6.172 are where that lives.
9. **Research method is never a named course.** It is taught inside dissertations and capstones (Oxford dissertation, Imperial research project, Baruch MTH 9903, NYU capstone) [searched for their existence; that method is taught there is inferred]. A self-taught learner has no supervisor, so the app must teach it explicitly. The 1.6 file has made a start (forking paths and backtest overfitting, one lesson each).

### 2.3 Coverage matrix

R = required in the programme or its feeder degree; T = taught as a named course or elective; · = not found in the course lists I could see (weak evidence of absence). **Bold** cells rest on a course title confirmed by search; plain cells are [recalled]. The last column describes the curriculum as the curriculum files teach it.

| Topic | Cam | Ox | Imp | CMU | Bar | Pri | MIT | Hvd | Stan | NYU | Berk | ETH | Curriculum (with the files) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Proof, real analysis | **R** | R | · | **R** | · | · | **T** | · | T | · | · | · | Proof methods in 0.3 (R1, R2); $\varepsilon$-$\delta$ in 1.3; no analysis course |
| ODEs and PDEs | **R** | **R** | **R** | **R** | T | · | T | · | · | T | · | · | First-order ODEs in 1.3 (I6) |
| Numerical methods, floating point | T | **R** | **R** | **R** | **R** | · | **T** | · | T | **T** | · | **R** | Three lessons (0.1, 1.3) |
| Optimisation (LP, convex, duality) | **T** | · | **T** | **R** | · | **R** | T | · | T | · | · | · | Lagrange multipliers, shadow prices (1.3); gradient descent (1.3, 1.4) |
| Elementary probability | **R** | R | R | R | **R** | **R** | **T** | **T** | **T** | R | R | R | 1.5, 250 h |
| Stochastic processes, martingales | **T** | **T** | **R** | **R** | **R** | **R** | **T** | · | T | **R** | **R** | R | Discrete time in 1.5 (Z3, Z4); no continuous time |
| Measure-theoretic probability | **T** | T | · | T | · | · | **T** | · | T | · | · | R | Named once in 1.5 |
| Stochastic calculus | **T** | **R** | **R** | **R** | **R** | **T** | **T** | · | T | **R** | **R** | R | 3.2 optional, uncounted |
| Statistical inference | **T** | R | **R** | **R** | · | **R** | **T** | **T** | **T** | · | **R** | **R** | 1.6, 120 h, to Fisher information and the bootstrap |
| Econometrics, empirical finance | · | **R** | **R** | **R** | · | · | T | · | T | **R** | **R** | **R** | HC and HAC errors (1.6); Newey-West (2.2) |
| Time series | · | R | T | **R** | T | · | **T** | · | T | **T** | **R** | R | 2.2, 60 h |
| Classical machine learning | T | **R** | **T** | **R** | **T** | T | **T** | · | **T** | **T** | **R** | T | 2.1, 200 h |
| Deep learning | · | **R** | **T** | T | · | · | **T** | · | **T** | · | · | · | Backpropagation lesson (1.3); a few chapters of 2.1 |
| Information theory | T | T | · | · | · | · | T | · | T | · | · | · | Maximum entropy (1.3); cross-entropy as likelihood (1.6) |
| Bayesian inference and MCMC | T | · | · | · | · | · | **T** | **T** | **T** | · | · | · | 1.6 course BY (11 lessons, Metropolis); Metropolis in 1.5 |
| Portfolio theory, risk measures | · | **R** | **R** | **R** | T | · | **T** | · | **T** | **R** | **R** | **R** | Minimum variance (1.3), shrinkage (1.4), VaR backtest (2.2) |
| Fixed income | · | **R** | **R** | T | T | · | **T** | · | **T** | T | **R** | T | Khan Academy in 1.7 |
| Market microstructure | · | · | · | **T** | T | · | · | · | · | **T** | · | · | Harris in 1.7; the Roll model (2.2) |
| C++ and software engineering | T | **R** | **R** | **R** | **R** | · | T | · | **T** | **R** | · | · | 1.9, 140 h |
| Computer systems, performance | T | · | · | T | · | · | **T** | · | T | · | · | · | Measured timing (1.1); none beyond |
| Research method (inside a dissertation, project or capstone) | · | **R** | **R** | **R** | **R** | R | · | · | · | **R** | **R** | R | Two 1.6 lessons; implicit in 2.3 and 3.1 |

---

## 3. Gap analysis

Each entry gives what is missing, why it matters for quant and ML-lab work, which programmes teach it, the canonical university resource (full canon in section 6), hours, slot, a proposed exit test and the verdict. Revision 2 adds, where it applies, **Already in the curriculum files**: what the item files written after revision 1 teach inside existing hours, which the proposal now builds on rather than repeats. Gaps are ordered by priority, not by curriculum position.

### G1. Numerical methods, floating point and Monte Carlo (P3, 120 h, priority 1)

**Missing.** Floating-point arithmetic and rounding error as a theory (machine epsilon, ulps, backward error); conditioning and stability; root finding with safeguards; interpolation and quadrature; numerical linear algebra as algorithms (LU with pivoting, Cholesky, QR, the SVD, iterative solvers); finite differences for parabolic PDEs (explicit, implicit, Crank-Nicolson, stability); Monte Carlo with variance reduction (antithetic variates, control variates, importance sampling), quasi-random sequences, random-number generation.

**Already in the curriculum files.** Why $0.1 + 0.2 \ne 0.3$ (0.1 lesson 42, binary floating point); a cancellation-safe quadratic formula in a 0.2 drill; the balance of truncation and rounding error in finite differences (1.3 lesson 27); a quadrature preview (1.3 lesson 75); bisection with a step count (0.2 drill). These are the right first contacts. None reaches conditioning, a factorisation algorithm, a PDE solver or variance reduction.

**Why it matters.**

- *Pricing.* Implied volatility has no closed form: it is a root-finding problem, and plain Newton diverges for far out-of-the-money options unless bracketed. American and exotic options are priced by PDE solvers, trees or Monte Carlo. Monte Carlo error falls as $N^{-1/2}$, so variance reduction is the difference between ten thousand and a million paths. Project 3 already asks for Black-Scholes, binomial and Monte Carlo pricers compared: that is this course without the theory.
- *Statistics.* The one-pass variance formula $\frac{1}{n}\sum x_i^2 - \bar{x}^2$ loses about eight of double precision's sixteen significant digits when prices sit near 10,000 and move by about 1, and all of them in single precision; Welford's update loses none of note. A sample covariance matrix of 500 stocks from 250 days has rank at most 249, so it cannot be inverted for a mean-variance portfolio. Both are numerical linear algebra.
- *Developer.* Summation order, equality tests on prices, binary floating point for money: pricing libraries break here.
- *ML lab.* Mixed-precision training, loss scaling and the stable log-sum-exp in every softmax are the same ideas.

**Programmes.** Core at Oxford MCF, Baruch (MTH 9821 and a pre-entry seminar on numerical linear algebra), ETH, CMU MSCF and Imperial (Simulation Methods) [searched]; Cambridge IB Numerical Analysis [recalled]; MIT 18.335J [searched].

**Canonical resource.** Two courses, one spine each: Süli and Mayers, *An Introduction to Numerical Analysis* (CUP 2003) with Trefethen and Bau for the linear algebra; Glasserman, *Monte Carlo Methods in Financial Engineering* (Springer 2003). Lectures and solved problem sets: MIT 18.335J, Spring 2019 [searched]. For the PDE half in finance: Wilmott, Howison and Dewynne, *The Mathematics of Financial Derivatives* (CUP 1995) [recalled].

**Hours.** Floating point and error 12, equations, interpolation and quadrature 18, numerical linear algebra 30, finite differences 25, Monte Carlo 35 [our estimate; floating point is 3 h lighter and Monte Carlo 5 h heavier than revision 1 because 0.1 and 1.3 now hold the first contact].

**Slot.** First item of Stage 2 (2.0a), all tracks. Needs 1.3, 1.4, 1.5 and P8.

**Exit.** Price a European call four ways (closed form, binomial tree, Crank-Nicolson, Monte Carlo with a control variate) and plot error against work on log-log axes, reading off the orders: $O(n^{-1})$ for the tree, $O(\Delta t^2 + \Delta S^2)$ for Crank-Nicolson, $O(N^{-1/2})$ for Monte Carlo. Compute implied volatility across a strike grid with a safeguarded Newton method and no failures. Explain one cancellation failure and its fix.

**Verdict.** Propose. It is the largest gap against every master's surveyed.

### G2. Optimisation (P4, 80 h, priority 1)

**Missing.** Linear programming and duality; convex sets and functions; the Karush-Kuhn-Tucker conditions; Lagrangian duality; quadratic programming; gradient descent, Newton and quasi-Newton methods with their convergence rates; stochastic gradient methods; modelling with cvxpy.

**Already in the curriculum files.** Lagrange multipliers with the multiplier read as a shadow price (1.3 lessons 126 and 128, including the minimum-variance portfolio of uncorrelated assets); gradient descent in two dimensions (1.3 lesson 117) and on a quadratic in the eigenbasis, showing why conditioning sets the speed (1.4 lesson 96). Inequality constraints and KKT are left to P4 by `stage1-calculus.md`'s coverage check.

**Why it matters.**

- *Portfolios.* Portfolio construction is $\min_w \; w^\top \Sigma w - \lambda\, \mu^\top w$ subject to budget, position, sector and turnover constraints. Project 2 turns a signal into positions; without constraints and costs a mean-variance optimiser maximises estimation error (Michaud, "The Markowitz Optimization Enigma", FAJ 1989).
- *Prices.* Duality gives shadow prices, and the one-period fundamental theorem of asset pricing is LP duality (Farkas' lemma) in finance clothing.
- *ML.* Training is optimisation. The LASSO and support vector machines are convex optimisation problems, and the SVM dual is where kernels come from. SGD, momentum and Adam are every lab's working tools.
- *Execution.* Almgren-Chriss in discrete time is a quadratic programme.

**Programmes.** Princeton ORF 307 (core), Cambridge IB Optimisation, CMU MSCF, Imperial (elective) [searched]; Stanford EE364A [recalled].

**Canonical resource.** Boyd and Vandenberghe, *Convex Optimization* (CUP 2004, free PDF), with Stanford EE364A lectures [recalled]. Finance applications: Cornuéjols, Peña and Tütüncü, *Optimization Methods in Finance*, 2nd ed (CUP 2018).

**Runtime.** cvxpy-base 1.8.2 with the Clarabel solver, and HiGHS (`highspy`), are in Pyodide 314.0.7's package set [measured: lock file], so modelling drills can run in the browser; cvxpy depends on SciPy, so in the Artifact they need the SciPy load group to fit the budget (section 5.3).

**Hours.** LP and duality 20, convexity and KKT 25, algorithms 20, portfolio and ML applications 15 [our estimate].

**Slot.** Stage 2 after P3 (2.0b), before 2.1, which uses it.

**Exit.** Derive the dual of a given LP and confirm strong duality numerically; decide and prove the convexity of three functions; implement gradient descent and Newton's method and show linear against quadratic convergence; build a long-only mean-variance portfolio with a turnover limit and explain each constraint's dual value.

**Verdict.** Propose.

### G3. Stochastic processes in continuous time (P2, +15 h to 1.5, priority 1)

**Missing.** Revision 1 proposed 40 hours of discrete martingales, ruin, patterns, Poisson processes and Brownian motion. `stage1-probability.md` now teaches the discrete half inside 1.5's 250 hours: Poisson processes with merging and thinning and the inspection paradox (lessons 74 and 75), patterns as Markov chains (133), the reflection principle, the ballot theorem and Catalan numbers (136 to 138), a Brownian preview with the arcsine law (140), and a whole level on martingales (Z4: the martingale property, optional stopping and the doubling strategy, ruin by martingales, Wald's identity, the ABRACADABRA martingale). What is still missing: continuous-time Markov chains (generators, holding times, stationary distributions, birth-death chains); Brownian motion as an object (independent increments, quadratic variation stated, hitting times, the running maximum by reflection, $B_t$ and $B_t^2 - t$ as martingales, exit from an interval); and enough problem volume to solve the green book's chapter 5 cold.

**Why it matters.**

- *Interviews.* Martingale and Brownian arguments are the standard tool for a large family of interview problems: the probability that a Brownian motion with drift hits $+a$ before $-b$, the expected exit time, the distribution of the maximum. Zhou's green book, which 3.3 names, has a chapter on stochastic processes and stochastic calculus (ch. 5) after its probability chapter (ch. 4) [recalled]; the curriculum's exit asks only for ch. 4.
- *Markets.* Order arrivals in queue models are continuous-time chains; Avellaneda and Stoikov (2008), on 3.1's reading list, assumes fills arrive as a Poisson process with intensity $\lambda(\delta) = A e^{-k\delta}$ and prices move as Brownian motion.
- *Foundation.* Shreve volume II and every continuous-time model start from Brownian motion, so P16 needs this.

**Programmes.** Princeton ORF 309 (Poisson processes, random walks, Brownian motion, Markov chains), Cambridge IB Markov Chains, Imperial Stochastic Processes, Baruch MTH 9831 [searched]; MIT 6.262 and 18.445 [searched].

**Canonical resource.** Durrett, *Essentials of Stochastic Processes*, 3rd ed (Springer 2016), ch. 4 (continuous-time Markov chains) and ch. 5 (martingales) [searched for the chapter list], written for a learner who has finished a first probability course. Durrett treats Brownian motion only inside his finance chapter [unverified depth], so the Brownian part reads Grimmett and Stirzaker, *Probability and Random Processes*, 4th ed (OUP 2020), ch. 13 (diffusion processes: Brownian motion, first passage times, barriers) [recalled section titles]. Its ch. 12 (martingales) and the companion *One Thousand Exercises in Probability*, 3rd ed (OUP 2020) are the problems and stretch [searched]. Lectures: MIT 6.262 Discrete Stochastic Processes (Gallager, Spring 2011, 25 videos) for the Markov and martingale material [searched]; MIT 18.S096 Fall 2013 lectures on stochastic processes for Brownian motion [searched for topics].

**Hours.** Continuous-time chains 4, Brownian motion and its martingales 6, problem volume at green-book level 5 [our estimate].

**Exit.** Solve cold: the stationary distribution and an expected hitting time of a three-state continuous-time chain; for Brownian motion with drift, $X_t = \mu t + \sigma B_t$, the probability of hitting $+a$ before $-b$ and the expected exit time, by optional stopping applied to the martingales $e^{-2\mu X_t/\sigma^2}$ and $X_t - \mu t$; the distribution of the running maximum by reflection; eight green-book chapter 5 style problems at 70%.

**Verdict.** Propose. Still the highest interview value per hour of any gap, and now 15 hours.

### G4. Research method and statistical honesty (P1, 35 h, priority 1)

**Missing.** The curriculum has the right instincts in fragments: multiple testing in 1.6, purged cross-validation in 2.1, "treat any simple rule that backtests to a Sharpe above 2 as a bug", "report what failed". No item teaches the method: stating a hypothesis before looking; pre-registration; data-snooping corrections (White's reality check, the deflated Sharpe ratio, the probability of backtest overfitting); survivorship, look-ahead and point-in-time data; corporate actions; how often published anomalies replicate; reproducible pipelines (pinned environments, seeds, data versions); a results note a sceptic would accept.

**Already in the curriculum files.** The false discovery rate (1.6 lesson 40), the garden of forking paths (41) and backtest overfitting (42), one lesson each; the delta-method standard error of a Sharpe ratio (1.6 lesson 19); point-in-time joins and look-ahead bias in pandas (1.1 course on financial data); pairs trading without look-ahead (2.2 lesson 42). P1 starts from these and spends its hours on the audit, the protocol and the writing.

**Why it matters.**

- *Quant.* This is the job: a researcher's value is the false discoveries they do not ship. Harvey, Liu and Zhu (2016) argue a new factor needs a $t$-statistic above about 3.0, not 2.0. McLean and Pontiff (2016) find anomaly returns fall substantially after publication. Bailey and López de Prado's deflated Sharpe ratio adjusts for the number of trials. For $T$ independent, normally distributed returns, an estimated Sharpe ratio has standard error about $\sqrt{(1 + \mathrm{SR}^2/2)/T}$ in the units of the sampling period (Lo 2002). Annualised, a Sharpe of 1 measured over 3 years carries a standard error between about 0.58 (daily data) and 0.71 (annual data).
- *ML lab.* The same failures under other names: test-set reuse, benchmark contamination, seed cherry-picking, missing error bars, leakage (Kapoor and Narayanan, Patterns 2023; Henderson et al., "Deep Reinforcement Learning That Matters", AAAI 2018; Recht et al., "Do ImageNet Classifiers Generalize to ImageNet?", ICML 2019 [recalled]).
- *The curriculum's own exits depend on it.* 2.3 asks for a results note with failures; 3.1 asks how much of a published effect survived.

**Programmes.** No programme names a course. It is taught through supervised dissertations and capstones [inferred]. A self-taught learner has no supervisor, so the app has to be one.

**Canonical resource.** No textbook owns the topic. Spine: López de Prado, *Advances in Financial Machine Learning* (Wiley 2018) ch. 11 to 14, already in 2.1, with Arnott, Harvey and Markowitz, "A Backtesting Protocol in the Era of Machine Learning" (Journal of Financial Data Science 1(1), 2019) [searched] as the checklist, plus a reading pack of papers (section 6, item 2.2c).

**Hours.** Honest inference 6, backtest pathologies 14, replication and reproducibility 10, writing 5 [our estimate; honest inference is 4 h lighter than revision 1 because 1.6 now holds FDR, forking paths and backtest overfitting].

**Slot.** Stage 2, immediately before 2.3 Projects (2.2c). It uses 2.1's cross-validation and 2.2's time series.

**Exit.** Audit a supplied backtest with five planted defects (look-ahead, survivorship, unadjusted splits, in-sample parameter choice, missing costs) and find at least four; write a one-page pre-registration for project 2 before touching its data; report a deflated Sharpe ratio and a block-bootstrap interval for the project's Sharpe.

**Verdict.** Propose. Cheapest addition with the largest effect on the quality of everything after it.

### G5. Statistical inference, second pass (P5, +25 h to 1.6, priority 2)

**Missing.** Revision 1's list was Fisher information, the delta method, the bootstrap, permutation tests, FDR, GLMs, heavy tails and covariance shrinkage. `stage1-statistics-ts.md` decision S5 puts the core of it inside 1.6's 120 hours, one lesson each: Fisher information (16), Cramér-Rao (17), MLE asymptotics (18), the delta method with the Sharpe ratio's standard error (19), the bootstrap (25), permutation tests (35), FDR (40), logistic regression by iteratively reweighted least squares (65), resistant estimators (8). 1.4 lesson 95 introduces linear shrinkage. What is still missing, and what a one-lesson treatment cannot give: inference for dependent data (block and stationary bootstrap, against HAC errors); generalised linear models beyond logistic (Poisson regression, deviance, overdispersion); heavy tails (tail index, the Hill estimator, extreme value theory in outline); covariance estimation done properly (the Ledoit-Wolf optimal intensity, factor-model covariance, out-of-sample evaluation).

**Why it matters.** Returns are heavy-tailed and autocorrelated, so normal-theory intervals are often wrong and the block bootstrap is the working tool. Covariance estimation is how risk models make $\Sigma$ invertible and stable. Tail estimates drive expected shortfall. MIT 18.650 teaches GLMs and Stanford STATS 200 large-sample theory as part of the first serious inference course [searched].

**Canonical resource.** DeGroot and Schervish stays the spine (its §12.6 is the bootstrap); Wasserman, *All of Statistics* (Springer 2004) ch. 8 to 10 and 13 for this extension; MIT 18.650 Fall 2016 lectures [searched]; McNeil, Frey and Embrechts, *Quantitative Risk Management*, revised ed (Princeton 2015), chapter on extreme value theory [recalled] for tails.

**Hours.** Dependent-data inference 7, GLMs beyond logistic 6, heavy tails 6, covariance estimation 6 [our estimate].

**Exit.** The standard error of a Sharpe ratio by the delta method and by block bootstrap on the same autocorrelated series, with the difference explained; Ledoit-Wolf against the sample covariance, compared out of sample on minimum-variance portfolio volatility; a Poisson regression fitted by iteratively reweighted least squares and matched to statsmodels; a Hill estimate of the tail index of daily returns with the threshold choice defended.

**Verdict.** Propose.

### G6. Portfolio theory, risk and fixed income (P6, 75 h, priority 2, trader and researcher)

**Missing.** Mean-variance and the efficient frontier; CAPM, APT and factor models; the fundamental law of active management, $\mathrm{IR} \approx \mathrm{IC}\sqrt{\mathrm{breadth}}$; risk decomposition; risk measures (volatility, value at risk, expected shortfall, coherence); bond pricing, yield curves and bootstrapping, duration and convexity, swaps. 1.7 covers instruments and options. Project 2 reports an information coefficient without the theory that gives it meaning.

**Already in the curriculum files.** The minimum-variance portfolio of uncorrelated assets (1.3 lesson 128); portfolio variance (1.5 lesson 96); covariance shrinkage (1.4 lesson 95); VaR backtesting and volatility targeting (2.2 lessons 30 and 31); PCA of yield curves as a 1.4 transfer (Litterman and Scheinkman is on 1.4's reading list).

**Why it matters.** Researchers turn signals into portfolios and are judged on risk-adjusted return; the fundamental law is the standard lens of systematic equity [recalled]. Traders on rates desks are asked about duration and curves. Risk measurement is core in Oxford, Imperial, Berkeley, ETH and NYU [searched].

**Canonical resource.** Luenberger, *Investment Science*, 2nd ed (OUP 2013), the field's standard text and the basis of Stanford MS&E 245A's scope [searched for the course and the edition]; lectures MIT 15.401 Finance Theory I (Lo, Fall 2008) [recalled] and 15.433 Investments (Spring 2003, notes and assignments with solutions) [searched]; the 18.S096 Fall 2013 lectures on portfolio theory, factor models, VaR and yield curves [searched for topics].

**Hours.** Fixed income 25, mean-variance and CAPM 15, factor models and the fundamental law 20, risk measures 15 [our estimate; risk 5 h lighter because 2.2 now holds the VaR backtest].

**Slot.** Stage 2 after P4 (2.0c).

**Exit.** Bootstrap a zero curve from par yields and price a bond off it; hedge a position's DV01; compute 99% VaR and ES three ways (historical, parametric, Monte Carlo) and backtest with Kupiec's test; predict an information ratio from IC and breadth and compare it with a simulated strategy.

**Verdict.** Propose for trader and researcher; optional for developer. The finance widget catalogue already designs bonds and the yield curve (`widgets-finance-games.md` 6.3), so part of the engine work exists.

### G7. Proof and discrete mathematics (P7, 70 h, priority 2)

**Missing.** `curriculum.md` never asks for a proof. The curriculum files have added a proof thread at school-to-first-year level, and P7 now builds on it. Still missing: proof as a subject rather than a technique (quantifiers handled fluently, proofs about sets, functions and relations, bijective and double-counting proofs); elementary number theory (divisibility, modular arithmetic, gcd and the Euclidean algorithm with proof); graphs (trees, connectivity, matchings, colouring, with proofs); invariants and the extremal principle; recurrences and asymptotic notation with proofs; and enough volume that writing a correct proof is routine.

**Already in the curriculum files.** Logic, implication, contrapositive and contradiction (0.3 level R1, 5 lessons); induction for sums, divisibility, inequalities and recurrences (0.3 level R2, 4 lessons); the pigeonhole principle (0.3 lesson 104); $\varepsilon$-$\delta$ and proofs of the differentiation rules, the mean value theorem and the fundamental theorem (1.3); long-form proofs with rubrics in every 1.5 and 1.6 level.

**Why it matters.**

- *Interviews* ask for arguments: "show the expected number of fixed points of a random permutation is 1", "prove this strategy is optimal", invariant puzzles (hats, prisoners, chessboard tilings). Indicator variables, a 1.5 topic, are a proof technique.
- *Research* means reading an appendix and catching a wrong lemma. ML-lab research is written in theorems.
- *Every undergraduate pipeline surveyed starts here*: Cambridge Numbers and Sets, Oxford Prelims, CMU 21-127 as the prerequisite for all theory [searched for Cambridge and CMU].
- *Prerequisite* for P16 and for learning theory in P14; it also strengthens 1.8, where correctness arguments matter.

**Canonical resource.** Velleman, *How to Prove It*, 3rd ed (CUP 2019); Lehman, Leighton and Meyer, *Mathematics for Computer Science* (MIT, 2017 revision, free) with MIT 6.042J lectures and problem sets [recalled].

**Hours.** Proof writing beyond R1 and R2 15, sets, functions, relations and bijective counting 15, number theory 10, graphs 12, invariants and combinatorial proof 10, recurrences and asymptotics 8 [our estimate; 20 h lighter than revision 1 because 0.3 now teaches the methods].

**Slot.** Between 1.4 and 1.5 (1.4b). Proof makes probability easier; placing it before calculus would delay 1.3 for a learner fresh from Stage 0. The weekly interview problems that start at 1.5 start 70 hours later.

**Exit.** Fifteen proofs, at least three each by induction, contradiction, bijection, invariant and pigeonhole, self-marked against a 10-point rubric with tutor suggestions, at 70%; one 6.042J-style final at 70%.

**Verdict.** Propose. It also makes the long-form rubric items (`content-format.md` decision 15, genre `proof`) load-bearing from Stage 1.

### G8. Differential equations, second order and systems (P8, 45 h, priority 3)

**Missing.** Second-order constant-coefficient equations; linear systems $x' = Ax$ solved through eigenvalues and $e^{At}$; stability and phase portraits; Runge-Kutta methods and stiffness; the heat equation by separation of variables, with the idea of Fourier series.

**Already in the curriculum files.** One level of four lessons in 1.3 (I6): slope fields, separable equations, Euler's method, and linear first-order equations with an integrating factor, including continuous compounding at a varying rate and mean reversion. Fourier series as orthogonal functions appear in 1.4 lesson 53.

**Why it matters.** The Black-Scholes PDE becomes the heat equation after a change of variables. Mean reversion (the Ornstein-Uhlenbeck process, the Vasicek short rate, a pairs-trading spread) has a mean that solves $m'(t) = \theta(\mu - m(t))$ and a variance that solves a second linear equation. Finite-difference pricing (P3) must know what equation it solves. Gradient descent is a discretised gradient flow, and diffusion models are SDEs with an ODE counterpart. Taught in Cambridge IA, CMU 21-260 and the Oxford MCF induction week [searched].

**Canonical resource.** Strang, *Differential Equations and Linear Algebra* (Wellesley-Cambridge 2014), with MIT 18.03SC (Fall 2011) problem sets and exams [recalled] and the Strang and Moler video series RES.18-009 (Fall 2015) [searched]. The heat equation is in Strang's chapter 8, Fourier and Laplace Transforms [searched].

**Hours.** Second-order equations 10, linear systems and $e^{At}$ 15, stability and phase portraits 6, numerical methods 6, the heat equation 8 [our estimate; 5 h lighter because 1.3 now teaches first-order equations].

**Slot.** After 1.6 (1.6b). It needs 1.4's eigenvalues; after 1.6 it delays nothing in probability. Before P3.

**Exit.** One 18.03SC-style unit exam on second-order equations and one on linear systems at 70%; derive and solve the OU mean and variance equations; transform the Black-Scholes PDE to the heat equation and verify the transformation symbolically.

**Verdict.** Propose. The calculus catalogue already has `slope-field` (Euler's method).

### G9. Information theory essentials (P9, +20 h to 2.1, priority 3)

**Missing.** Entropy, cross-entropy, KL divergence, mutual information; source coding (Huffman codes, the source-coding theorem stated); log-loss as likelihood across models; Kelly's criterion as maximising expected log growth.

**Already in the curriculum files.** The maximum-entropy distribution under a constraint (1.3 lesson 128); cross-entropy loss as a negative log-likelihood (1.6 lesson 65); a Kelly growth preview (1.5 level Z6).

**Why it matters.** Cross-entropy is the loss every classifier and language model minimises. KL divergence appears in variational inference, in the KL penalties of policy optimisation and in model comparison. Mutual information measures dependence that correlation misses. For traders, the Kelly sizing already in 3.3's betting games is information theory: Cover and Thomas derive it (ch. 6 and 16). Taught at Cambridge, Oxford, MIT and Stanford [recalled].

**Canonical resource.** MacKay, *Information Theory, Inference, and Learning Algorithms* (CUP 2003, free), ch. 1, 2, 4 and 5, with his recorded Cambridge lectures [recalled].

**Hours.** 20 (entropy, KL and mutual information 8, coding 5, log-loss and Kelly 7). **Slot.** Opening of 2.1.

**Exit.** Entropies and KL divergences by hand; a Huffman code built and its expected length compared with the entropy; a proof that cross-entropy loss is the negative log-likelihood of a categorical model; the Kelly fraction $f^* = p - (1-p)/b$ derived, and a simulation showing that betting $2f^*$ grows wealth at a rate near zero for small edges.

**Verdict.** Propose.

### G10. Matrix calculus for learning (P10, +10 h, opening of 2.1, priority 3)

**Missing.** Revision 1 proposed 20 hours inside 1.4. `stage1-linear-algebra.md` decision 6 and `stage1-calculus.md` now hold most of it inside existing hours: gradients of linear and quadratic forms, least squares and ridge by calculus with finite-difference checks (1.4 lesson 82), Eckart-Young low-rank approximation (1.4 lesson 86), gradient descent and conditioning (1.4 lesson 96), finite differences and dual-number automatic differentiation (1.3 lessons 27 and 28), backpropagation on a small computation graph (1.3 lesson 116). Still missing: Jacobians and the chain rule in matrix form; the softmax and logistic gradients in matrix form; backpropagation through a two-layer network written with matrices; the identities $\nabla_X \operatorname{tr}(AX) = A^\top$ and $\nabla_X \log\det X = X^{-\top}$.

**Why it matters.** 2.1 derives every fitted model's gradient silently; P14 starts from backpropagation in matrix form. `stage1-linear-algebra.md` places the remainder "with 2.1, where its use is", and this revision agrees, so P10 moves from 1.4 to the opening of 2.1. MIT built 18.065 and the 18.S096 matrix-calculus course around this bridge [searched].

**Canonical resource.** MIT 18.S096 Matrix Calculus for Machine Learning and Beyond (IAP 2023; videos, notes, problem sets with solutions) [searched]; Deisenroth, Faisal and Ong, *Mathematics for Machine Learning* (CUP 2020, free) ch. 5 [recalled].

**Hours.** 10. **Exit.** Derive and check by finite differences the gradients of logistic loss, softmax cross-entropy and a two-layer network, all in matrix form.

**Verdict.** Propose.

### G11. Financial econometrics and empirical asset pricing (P11, 80 h + 15 h to 2.2, priority 2, researcher)

**Missing.** Panel data with fixed effects and clustered errors; Fama-MacBeth cross-sectional regressions; portfolio sorts and their $t$-statistics; time-series tests of factor models (GRS); event studies; GMM in outline; instrumental variables in outline. Time-series extension: state-space models and the Kalman filter, regime switching in outline, VAR estimation beyond 2.2's preview.

**Already in the curriculum files.** Heteroskedasticity-consistent and HAC standard errors (1.6 lessons 55 and 56), Newey-West in depth (2.2), the Roll model as MA(1), realised volatility, VAR, Granger causality and Johansen as a preview (2.2 lessons 12, 29 and 41).

**Why it matters.** The factor papers on 3.1's list (Jegadeesh and Titman, Fama and French, Harvey, Liu and Zhu) rest on portfolio sorts, time-series factor regressions and cross-sectional tests, and the literature that extends them uses Fama-MacBeth regressions with Newey-West errors; the replication exit cannot be passed honestly without these tools. Overlapping returns make ordinary standard errors too small: a classic way to find significance that is not there. The Kalman filter is a common estimator of a time-varying hedge ratio, the natural extension of Gatev, Goetzmann and Rouwenhorst's fixed-ratio distance method. Core at Berkeley (230E), NYU, Oxford, CMU and ETH [searched].

**Canonical resource.** Bali, Engle and Murray, *Empirical Asset Pricing: The Cross Section of Stock Returns* (Wiley 2016); Campbell, Lo and MacKinlay, *The Econometrics of Financial Markets* (Princeton 1997) as reference; Wooldridge, *Introductory Econometrics*, 8th ed (Cengage 2025) [searched for edition] for exercises; Cochrane's free online Asset Pricing class with problem sets and exams [searched].

**Runtime.** statsmodels 0.14.6 is in Pyodide's package set; `linearmodels` (panel and Fama-MacBeth estimators) and `arch` (GARCH) are not [measured: lock file]. Fama-MacBeth, clustered errors and the Kalman filter are therefore written from NumPy and statsmodels pieces, which is also the better lesson.

**Hours.** 80, plus 15 on 2.2 (state space and Kalman 8, regime switching 4, VAR estimation 3) [our estimate; the 2.2 extension is 5 h lighter because 2.2 now previews VARs].

**Slot.** After 2.2 (2.2b). Researcher core; elective for others.

**Exit.** Replicate a momentum Fama-MacBeth regression with Newey-West errors and show how the $t$-statistic moves with the lag choice; run a GRS test of the CAPM on the 25 size and value portfolios from Kenneth French's data library; estimate a Kalman-filter hedge ratio for a pair and compare it with a rolling regression.

**Verdict.** Propose for the researcher track.

### G12. Market microstructure and execution (P12, 50 h, priority 2, trader)

**Missing.** The theory behind the order book that 1.7 describes: the Roll model of the spread in depth; Glosten-Milgrom (the spread as protection against informed traders); Kyle (informed trading and price impact $\lambda$); dealer inventory models; Avellaneda-Stoikov market making; Almgren-Chriss optimal execution; empirical facts of order flow (persistent order signs, square-root impact); Hawkes processes in outline.

**Already in the curriculum files.** The Roll model as an MA(1) (2.2 lesson 12), and Harris for description (1.7). P12 starts from them.

**Why it matters.** Market-making firms hire traders to reason about adverse selection and inventory. 3.3's market-making games are Glosten-Milgrom played live. Project 4 records exactly the data this theory explains, and Avellaneda and Stoikov sits on 3.1's list with no background to read it. CMU MSCF and NYU name microstructure [searched].

**Canonical resource.** Foucault, Pagano and Röell, *Market Liquidity: Theory, Evidence, and Policy*, 2nd ed (OUP 2023), which adds chapters on algorithmic and high-frequency trading and on liquidity and financial stability [searched]; the original papers (section 6, item 2.0d). I could not identify a public university lecture series on the topic [unverified].

**Hours.** 50. **Slot.** Stage 2 after P6 (2.0d). Trader core; researcher elective.

**Exit.** Simulate Glosten-Milgrom and show the spread narrowing as the informed share falls; implement Avellaneda-Stoikov quotes and report inventory and P&L against a symmetric quoter; compute an Almgren-Chriss trajectory and its cost-risk frontier.

**Verdict.** Propose for the trader track.

### G13. Computer systems, concurrency and performance (P13, 150 h, priority 1 for developers)

**Missing.** How a computer runs code: data representation (two's complement, IEEE 754); reading machine code; the memory hierarchy and caches; virtual memory; processes and threads; synchronisation (mutexes, condition variables, atomics, the C++ memory model); lock-free single-producer single-consumer queues; false sharing; networking (TCP against UDP, multicast market data, sockets); profiling and performance engineering; kernel bypass in outline. The curriculum says developers need double the C++ hours; but C++ the language is not systems knowledge. `stage1-python-tools.md` lesson 68 teaches measurement, not parallelism, and leaves concurrency to Stage 2.

**Why it matters.** Quant-developer interviews at latency-sensitive firms ask why a vector beats a linked list, what false sharing is, how to build a lock-free queue, and what happens between a packet arriving and an order leaving [recalled from widely reported interview content; varies by firm]. Project 4 asks for measured latency on the developer track and cannot be done well without this. CMU 15-213 and MIT 6.172 are the canonical courses [searched for 6.172; recalled for 15-213].

**Canonical resource.** Bryant and O'Hallaron, *Computer Systems: A Programmer's Perspective*, 3rd ed (Pearson 2015) with CMU 15-213 labs; MIT 6.172 Fall 2018 [searched]; Williams, *C++ Concurrency in Action*, 2nd ed (Manning 2019). Free alternative for processes, virtual memory and concurrency: Arpaci-Dusseau and Arpaci-Dusseau, *Operating Systems: Three Easy Pieces*, version 1.10 (free) [searched].

**Hours.** Representation and machine code 30, memory and performance 40, threads and concurrency 45, networking 25, capstone 10 [our estimate].

**Slot.** Stage 2 after 1.9 (2.0e), developer core. All drills run on the learner's machine or the web app, since neither target compiles C++ in the browser (`widgets-programming.md` decision 9).

**Exit.** The CS:APP data, bomb, cache and proxy labs [recalled lab names]; a lock-free SPSC ring buffer benchmarked against a mutex queue, with the result explained; a UDP multicast feed handler with measured p50, p99 and p99.9 latency.

**Verdict.** Propose for the developer track.

### G14. Deep learning, language models, learning theory and reinforcement learning (P14, 380 h, priority 2, new track)

**Missing.** The owner's goal includes ML-lab calibre thinking. 2.1 is correct for quant work and the right first ML course: linear, regularised and tree models with careful validation. It does not reach what ML labs expect, judging by the courses their researchers cite: backpropagation and automatic differentiation built from scratch at scale; modern architectures (residual networks, attention, transformers); initialisation, normalisation and optimisers in practice; training at scale (GPU memory, parallelism, mixed precision, scaling laws); evaluation; learning theory as a way to think about generalisation; and reinforcement learning, on which language-model post-training now depends. 1.3 lesson 116 (backpropagation on a small graph) is the first contact.

**Programmes.** Deep learning is core at Oxford MCF and elective at Imperial [searched]; MIT 6.7960, Stanford CS229, CS231n and CS336 are the reference courses [searched for all four].

**Four courses.**

| Course | Hours | Spine | Lectures and problems | Exit |
|---|---|---|---|---|
| Deep learning foundations | 150 | Prince, *Understanding Deep Learning* (MIT Press 2023, free PDF, CC BY-NC-ND [searched]) ch. 1 to 12 and 18 | MIT 6.7960 Fall 2024 (lectures, problem sets with solutions) [searched]; Stanford CS231n Spring 2025 (public videos, notes and assignment starter code) [searched]; Karpathy's *Neural Networks: Zero to Hero* as the code companion (not a university course) [recalled] | An autodiff engine in NumPy that trains an MLP; a small CNN; a character-level transformer whose validation loss matches a reference implementation within a stated tolerance |
| Language models from scratch | 120 | Stanford CS336 Language Modeling from Scratch (Spring 2025, with the Spring 2026 offering also public; lectures and five assignments) [searched] | Austin et al., "How to Scale Your Model" (Google DeepMind 2025, free) [recalled]; Vaswani et al. (2017), Kaplan et al. (2020), Hoffmann et al. (2022) | The CS336 first assignment's scope: a byte-pair tokeniser, a transformer, AdamW and a training loop, with a three-size scaling sweep [recalled assignment scope] |
| Learning theory | 60 | Shalev-Shwartz and Ben-David, *Understanding Machine Learning* (CUP 2014, free) ch. 2 to 7, 12 to 14 | Bach, *Learning Theory from First Principles* (MIT Press 2024) [recalled]; Hardt and Recht, *Patterns, Predictions, and Actions* (Princeton 2022, free) [recalled] | PAC and VC exercises; a written account of double descent backed by a simulation |
| Reinforcement learning | 50 | Sutton and Barto, *Reinforcement Learning: An Introduction*, 2nd ed (MIT Press 2018, free) ch. 2 to 6, 9, 13 | David Silver's UCL course (2015) [recalled]; Berkeley CS285 [recalled] | Bandit algorithms with regret curves; tabular Q-learning; REINFORCE with a baseline |

**Slot.** A fourth Stage 2 track after 2.1, with P15 as an elective. On this track two of 2.3's three projects become ML projects and the 3.1 replication may be an ML paper [our choice]. 3.3 stays: probability and estimation transfer, and the owner may still interview with quant firms.

**Runtime.** Neither PyTorch nor JAX is in Pyodide's package set [measured: lock file], so in-browser drills build networks in NumPy, which covers the first course and most of the third and fourth. The second course trains on the learner's machine or a free cloud notebook [inferred].

**Verdict.** Propose as a new track. Without it the curriculum produces a strong quant who has used a neural network but never built one.

### G15. Bayesian computation (P15, 40 h, elective)

**Missing.** Hierarchical models and partial pooling; Gibbs sampling and Metropolis-Hastings beyond a first sampler; Hamiltonian Monte Carlo; convergence diagnostics ($\hat{R}$, effective sample size, divergences); variational inference in outline; probabilistic programming.

**Already in the curriculum files.** A first Metropolis sampler with detailed balance (1.5 lesson 134); the 1.6 Bayesian course BY (11 lessons: posterior predictive, normal-normal, empirical-Bayes shrinkage, Bayesian ridge, Bayes factors, Metropolis).

**Why it matters.** Partial pooling is the principled form of the shrinkage quants apply to noisy per-asset estimates; Black-Litterman is a Bayesian update [recalled]; ML labs use variational methods and Langevin-type samplers. Harvard Stat 111 and MIT 18.650 teach Bayesian inference [searched]; the 1.5 spine has an MCMC chapter (Blitzstein and Hwang ch. 12).

**Canonical resource.** Gelman et al., *Bayesian Data Analysis*, 3rd ed (CRC 2013, free PDF from the authors); McElreath, *Statistical Rethinking*, 2nd ed (CRC 2020) with his recorded lecture series [recalled].

**Runtime.** PyMC, ArviZ and NumPyro are not in Pyodide's package set [measured: lock file]. Samplers are written from scratch in NumPy on both targets, which is the point of the course; a probabilistic-programming comparison runs on the learner's machine.

**Hours.** Hierarchical models 10, Gibbs and Metropolis-Hastings 8, HMC 8, diagnostics 6, variational inference 4, probabilistic programming off-device 4 [our estimate; 10 h lighter because 1.5 and 1.6 now hold the first sampler and conjugate updating]. **Slot.** Elective on the researcher and ML research tracks.

**Exit.** Metropolis-Hastings and HMC written from scratch for a hierarchical model of per-stock betas, checked in the browser against a grid posterior on a two-parameter slice and on the learner's machine against PyMC or NumPyro; $\hat{R}$ and effective sample size explained.

**Verdict.** Propose as an elective.

### G16. Real analysis, measure-theoretic probability and stochastic calculus (P16, 370 h, optional)

**Missing.** The rigorous route: sequences, series, continuity, uniform convergence and the Riemann integral; sigma-algebras, Lebesgue integration, conditional expectation as a projection, martingale convergence; Brownian motion, the Itô integral, Itô's formula, Girsanov's theorem, Feynman-Kac and continuous-time risk-neutral pricing (the curriculum's 3.2).

**Why it matters.** Required for derivatives pricing and desk-quant roles; every financial-engineering master's surveyed teaches stochastic calculus as core [searched for all but ETH]. Useful for ML theory and diffusion models. The curriculum is right that it is rarely tested for trading or statistical research roles, so it stays optional. What changes is that its hours are counted and its prerequisites stated: Shreve volume II opens with measure theory (ch. 1 and 2), which a learner with no analysis meets cold. 1.3's two $\varepsilon$-$\delta$ lessons and 1.5's statement of the strong law are previews, not the course.

**Canonical resource.** Abbott, *Understanding Analysis*, 2nd ed (Springer 2015) with MIT 18.100A Fall 2020 [searched]; Williams, *Probability with Martingales* (CUP 1991); Shreve, *Stochastic Calculus for Finance* I and II (Springer 2004), with Cambridge Part II Stochastic Financial Models example sheets [searched] and Chin, Nel and Ólafsson, *Problems and Solutions in Mathematical Finance*, vol. 1 (Wiley 2014), for worked solutions [searched].

**Hours.** Real analysis 120, measure-theoretic probability 100, stochastic calculus 150 [our estimate].

**Slot.** Optional add-on after Stage 2; real analysis needs P7.

**Verdict.** Propose as optional, with hours counted.

### G17 and G18. Minor: no new hours

- **G17, algorithms with proofs.** 1.8 is an interview problem list. MIT 6.006 and 6.046J teach correctness proofs, amortised analysis and randomised algorithms. Proposal: inside 1.8's 250 hours, use the 6.006 Spring 2020 problem sets as a theory thread of about 40 hours [our estimate]. On the developer track, Stanford CS106B's C++ treatment of the same structures (Roberts, *Programming Abstractions in C++*) [searched] joins 1.9 as a second explanation.
- **G18, software construction.** Baruch MTH 9815 and Oxford's C++ courses teach design and testing [searched for titles]. Proposal: 1.2 and 1.9 lessons cite MIT's Software Construction readings (free; course 6.102, formerly 6.031 and 6.005) [searched] for specifications, testing and abstraction.

**Considered and folded in.** Game theory goes inside P12 (Glosten-Milgrom and Kyle are games). Stochastic control (Oxford MCF core) goes inside P12 (Avellaneda-Stoikov and Almgren-Chriss are control problems), P14's reinforcement-learning course (Bellman equations) and P16 (the Merton problem as a stretch reading), not a course. Causal inference gets one lesson inside P1 on confounding, not a course. SQL depth and data engineering go inside P1 (point-in-time data) and project 4.

---

## 4. Recommendation

### 4.1 Priorities

| Priority | Proposals | Reason |
|---|---|---|
| 1 | P1, P2, P3, P4, O1; P13 for developers | Core in nearly every master's (P3) or in the operations-research route and under every portfolio and training loop (P4); the stochastic-process material interviews test, now 15 hours (P2); the failure that sinks projects (P1). O1 pays for part of it. P13 is the developer track's equivalent of P3 |
| 2 | P5, P6, P7, P11, P12, P14 | Core in most programmes or needed by the curriculum's own exits (P6 for project 2, P11 for 3.1) or by the owner's ML-lab goal (P14) |
| 3 | P8, P9, P10, P15, P16 | Valuable and cheap (P8 to P10) or optional by nature (P15, P16) |

### 4.2 Resulting order by track

**Stage 1, all tracks (1,555 h).** 1.1 Python, 1.2 Tools, 1.3 Calculus, 1.4 Linear algebra, **1.4b Proof and discrete mathematics (P7, 70 h)**, 1.5 Probability with P2 (265 h), 1.6 Statistics with P5 (145 h), **1.6b Differential equations (P8, 45 h)**, 1.7 Finance basics (alongside 1.3 to 1.6, as now), 1.8 Data structures and algorithms, 1.9 C++.

**Stage 2.**

| Order | Item | Trader | Researcher | Developer | ML research |
|---|---|---|---|---|---|
| 2.0a | Numerical methods and Monte Carlo (P3) | 120 | 120 | 120 | 120 |
| 2.0b | Optimisation (P4) | 80 | 80 | 80 | 80 |
| 2.0c | Portfolio theory, risk and fixed income (P6) | 75 | 75 | optional | optional |
| 2.0d | Market microstructure and execution (P12) | 50 | elective | optional | · |
| 2.0e | Systems, concurrency and performance (P13) | · | · | 150 | optional |
| 2.1 | Machine learning, opening with information theory (P9) and matrix calculus (P10) | 230 | 230 | 230 | 230 |
| 2.1x | ML research track (P14) | · | · | · | 380 |
| 2.2 | Time series | 60 | 75 | 60 | 60 |
| 2.2b | Financial econometrics (P11) | elective | 80 | · | · |
| 2.2c | Research method and statistical honesty (P1) | 35 | 35 | 35 | 35 |
| 2.3 | Projects | 400 | 400 | 400 | 400 |
| 2.4 | Contests (O1) | 60 | 60 | 140 | 60 |
| | Bayesian computation (P15) | · | elective 40 | · | elective 40 |
| | **Stage 2 total** | **1,110** | **1,155** | **1,215** | **1,365** |

Stage 0 (500 h) and Stage 3 (400 h) are unchanged. P16 (370 h) can follow Stage 2 on any track. Totals: 500 + 1,555 + Stage 2 + 400, giving 3,565 (trader), 3,610 (researcher), 3,670 (developer) and 3,820 (ML research) hours, as in section 0.2.

### 4.3 The minimum set

If the owner wants the smallest change with the largest effect: **P1, P2, P3, P4 and O1**. Net +170 h (3,270 h) outside the developer track, +250 h (3,350 h) on it. Everything else can be added later without disturbing learners, because ids are immutable and display numbers come from position.

### 4.4 Exit-test changes that follow

These are proposals too. `assessment.md` 2.9 already shows each fits the exit instrument union without new machinery.

- **Stage 1 exit** adds a proof portfolio (P7) and a differential-equations unit exam (P8). 1.5's exit adds the P2 problems; 1.6's adds the P5 tasks.
- **Stage 2 exit** keeps "three finished projects, each with tests and a written results note", and adds that each note passes the P1 checklist (pre-registration, bias audit, deflated Sharpe ratio, bootstrap interval).
- **Stage 3 exit** extends "80% of the probability chapter in Zhou solved cold" to "80% of ch. 4 and 70% of ch. 5", if P2 is accepted.

### 4.5 Not worth adding

| Topic | Where it is taught | Why not |
|---|---|---|
| Abstract algebra, geometry, topology beyond the real line | Cambridge and Oxford cores [recalled] | Neither quant nor ML work at this level uses them |
| Complex analysis and Fourier methods as a course | Cambridge IB [recalled] | Needed only for characteristic-function pricing (Carr-Madan, Heston). 1.4 lesson 53 gives Fourier series; if P16 is taken, a 10-hour appendix inside stochastic calculus covers the rest |
| Corporate finance and accounting | ETH and CMU cores [searched] | Matters for fundamental equity research; trading firms do not test it [recalled from common interview reports] |
| Macroeconomics | ETH (Economic Foundations) [searched] | Firm-specific (macro funds, rates desks); a reading list at most |
| Credit, XVA, term-structure models (HJM, LMM) | CMU MSCF, Imperial, Oxford [searched] | Sell-side specialisms learnt on the desk; Shreve II ch. 10 inside P16 gives the idea |
| Stochastic control as a course | Oxford MCF core [searched] | The pieces a trader or researcher uses are inside P12, P14 and P16 (section 3, "Considered and folded in") |
| kdb+/q | Used at many banks and funds [recalled] | Vendor-specific and learnt on the job; name it in the developer notes |
| Distributed systems (MIT 6.5840) | MIT [recalled] | Beyond a first quant-developer role; Kleppmann's book as a project-4 reference is enough |
| Graduate probability (Durrett's *Probability: Theory and Examples*, Kallenberg), high-dimensional probability | Graduate programmes (MIT 18.175 uses Durrett [searched]) | PhD-track theory |
| Quantum computing, quantum ML, blockchain | Imperial elective (quantum ML) [searched] | Low hiring weight for the hours |
| Contest ratings above 1400 | | The curriculum's own reasoning stands |

---

## 5. What the proposals ask of the engine, the widget library and the runtimes

The owner's priority is the engine and widget library first. This section is so the library is designed for the curriculum as it may become, not only as it is. Widget names in the "Reuses" column come from the six catalogues in this folder; "New" names are proposals for those catalogues' owners [our choice].

> **Revised by the `docs/PLAN.md` review, 7 October 2026.** (1) The runtime tags this section used (`micropython-ok`, `ulab-ok`, `pyodide-core`, `web`) are void: Pyodide runs on both targets, drills declare `needs`, and placement is decided at run time; read `pyodide-core` as "runs on both targets" and `web` as "needs a group the Artifact build may not ship". (2) The Python budget is 75 MB within a 200 MB, 230-file release (`docs/PLAN.md` 5.6), not 120 MB, and load groups are measured on the phone at `docs/PLAN.md` stage 25, not E8. (3) Accepting proposals is not free of build work: `docs/PLAN.md` 12 lists, per proposal, the new widgets, the modes added to P0 widgets (P2 adds modes to `path-simulator` and `markov-chain`), the Python groups (P4 needs a new `optimisation` group), the file budget and the tutor load (P7, P14 and P16 make proof marking weekly), and sets the deadline: stage 44 for P2, stage 54 for the rest, stage 25 if P4's group is to be measured on the phone. (4) `float-inspector` and `descent-lab` are already P0 in `docs/WIDGETS.md`. (5) Section 5.4 adds the review's 2.1b and A1.

### 5.1 Widgets

| Proposal | Reuses | New | Runtime notes |
|---|---|---|---|
| P1 Research method | `backtest-lab`, `sharpe-lab`, `results-note` (finance 7.1, 7.2, 7.11); `multiple-testing` (prob 7.5); `replication-workbench` (ML 7.6) | `forking-paths` (run many analysis choices on null data and watch the best one look significant; 1.6 lesson 41 may already need it); `bias-audit` (a backtest with planted defects to find) | JavaScript; both targets. Drills on pandas are `pyodide-core` |
| P2 Continuous time | `sim-runner`, `chance-object`, `node-graph`, `markov-chain`; the random-walk composites (prob 6.4); 1.5's `stopping-game` and `poisson-stream` if built for levels Z3 and Z4 | `ctmc-clock` (competing exponential clocks driving jumps); `brownian-path` (refine a walk to Brownian motion; hitting and reflection) | JavaScript |
| P3 Numerical methods | `root-finder` (calc 5.8), `binomial-tree` (finance 5.1), `pricer-compare` (finance 7.5), `matrix`, `sim-runner` | `float-inspector` (IEEE 754 bits, ulps, cancellation; 0.1 lesson 42 may share it); `convergence-plot` (log-log error against work with fitted order); `fd-grid` (finite-difference stencil, stability region); `mc-variance` (variance-reduction race) | Visuals in JavaScript. NumPy drills are `pyodide-core` and run on both targets [measured on the owner's iPhone for NumPy]; drills that need SciPy are `web` until the SciPy load group fits the Artifact (section 5.3) |
| P4 Optimisation | `objective-explorer`, `convexity-chord` (calc 5.10, 5.12), `plot-2d`, `region-select` | `feasible-region` (LP polygon with a moving objective line and active constraints); `descent-lab` (gradient descent, momentum and Newton paths on contours); `dual-pair` (primal and dual side by side) | cvxpy-base (with Clarabel) and HiGHS are in Pyodide's package set [measured: lock file]; drills that use them, or SciPy's `linprog` and `minimize`, depend on SciPy; visuals use small JavaScript solvers |
| P5 Inference | `estimator-compare`, `ci-ladder`, `regression-lab`, `qq-plot` (prob 7.x); 1.6's bootstrap widget | `block-bootstrap-lab` (block length against coverage on autocorrelated data); `shrinkage-lab` (eigenvalues of sample and shrunk covariance; 1.4 lesson 95 may already need it); `tail-lab` (Hill plot) | JavaScript; statsmodels matching is `web` until the SciPy and statsmodels group fits |
| P6 Portfolio, risk, fixed income | `cashflow-timeline`; bonds and yield curve (finance 6.3); shares and portfolios (finance 6.2); `factor-model-lab` (ML 7.3) | `frontier-lab` (constrained efficient frontier); `var-backtest` (exceedances with Kupiec's test; 2.2 lesson 30 may already need it) | JavaScript |
| P7 Proof | `derivation-steps` (calc 4.1), `token-tray`, `epsilon-delta` (calc 5.2), `choice` | `proof-builder` (statements with justifications, reorderable, with gaps; a Parsons problem for proofs); `counterexample-hunt` | Long-form proofs use the rubric marking of `content-format.md` decision 15 (genre `proof`) |
| P8 Differential equations | `slope-field` (calc 5.15), `plot-2d` | `phase-plane` (2-D linear systems, eigenvectors, trajectories); `heat-rod` (diffusion, shared with `fd-grid`) | JavaScript |
| P9 Information theory | `mass-editor` (prob 3.1); the Kelly and betting-game widgets of 3.3 [inferred] | `entropy-lab`; `code-tree` (Huffman construction) | JavaScript |
| P10 Matrix calculus | `matrix`, `live-formula`, `code-cell`, `node-graph` (1.3 lesson 116's computation graph) | none: a gradient-check drill pattern in `code-cell` | `pyodide-core` |
| P11 Econometrics | `regression-lab`, `summary-table`, `portfolio-sort`, `panel-sim` (ML 7.0, 7.1), `arma-lab` | `panel-lab` (Fama-MacBeth step by step); `hac-lab` (how autocorrelation inflates $t$; 1.6 lesson 56 may already need it); `kalman-lab` | statsmodels drills `web` until its group fits; no `linearmodels` or `arch` in Pyodide [measured], so estimators are written from NumPy and statsmodels pieces |
| P12 Microstructure | order book and microstructure composites (finance 6.4, 6.8); `market-maker-sim` (ML 7.5); `quote-entry` | `adverse-selection-game` (Glosten-Milgrom as a playable game); `impact-lab` (Almgren-Chriss trajectories) | JavaScript |
| P13 Systems | `latency-lab` (finance 7.8); `code-cell` C++ adapters (programming decision 9) | `cache-sim` (access pattern against a cache model); `interleaving-lab` (step two threads through shared memory to find the race); `packet-path` | Concept widgets everywhere; C++ drills on the learner's machine; native timings there too |
| P14 ML research | `node-graph` (as a computational graph); neural-network composites (ML 6.5) | `autodiff-tape`; `attention-lab` (queries, keys and values on a toy sequence); `scaling-plot` | NumPy drills `pyodide-core`; no PyTorch or JAX in Pyodide [measured]; course 2 trains off-device |
| P15 Bayesian | `posterior-lab` (prob 7.9), `sim-runner`; 1.5's `markov-chain` (Metropolis mode) | `mcmc-lab` (Metropolis-Hastings and HMC on a 2-D posterior, with diagnostics) | JavaScript and `pyodide-core`; no PyMC, ArviZ or NumPyro in Pyodide [measured]; probabilistic programming off-device |
| P16 Rigour add-on | `epsilon-delta`, `derivation-steps`, `proof-builder`; stochastic-calculus composites (calc 1.3: `binomial-tree`, `filtration-tree`, `measure-change`) | `ito-lab` (quadratic variation as the mesh shrinks) | JavaScript |

**Count.** About 30 new widgets if everything is accepted, about 12 for the minimum set (P1 to P4) [our estimate]. Five of them (`forking-paths`, `float-inspector`, `shrinkage-lab`, `var-backtest`, `hac-lab`) may already be needed by the curriculum files' in-budget lessons, which would move them into the first widget build regardless of the owner's decision [inferred; the catalogues' owners should check]. Most are composites over existing primitives (`plot-2d`, `sim-runner`, `matrix`, `node-graph`); none needs a new primitive except `float-inspector`'s bit view, which `marks` may already cover [unverified].

### 5.2 Engine

1. **A citation registry that knows editions** [our choice]. `content/sources.yaml` grows to about 270 works (section 6). `content-format.md` revision 2 adopted the fields this paper asked for: `edition`, `isbn` (optional), `url` for free texts, `licence` (now including `cc-by-nc-nd`) and an optional `toc` map of chapter numbers to titles, so CI rejects a `loc` that names a chapter the pinned edition does not have. The `checked` flag stays as designed.
2. **Proof marking is load-bearing.** P7, P16 and P14's learning theory make long-form proofs a weekly item type, not an occasional one. The rubric engine and the tutor's per-point suggestions must handle proof steps and justifications, and the `proof-builder` widget must share their misconception ids.
3. **Tracks as data.** Four tracks plus an add-on (P14, P16) means a track is an ordered list of item ids with per-item status (core, elective, optional, absent), read from `curriculum.yaml`, not a fixed enumeration. `content-format.md` revision 2 adopted this (`trk.*`, decision 19).
4. **Hours drive pacing.** Track totals now differ by up to 255 hours, so the weekly plan and the "years to finish" estimate must read per-track hours (`assessment.md` decision 14 does).
5. **Placement for new items.** Every new item has an exit test, so each can be sat first, like the existing ones.
6. **Off-device exits.** P13's labs, P14's language-model course and P15's probabilistic-programming check finish on the learner's machine. The `setup-checklist` project mode (programming catalogue 0.2) must accept pasted benchmark output, loss curves and sampler summaries as evidence.

### 5.3 Python packages per proposal (new)

From the Pyodide 314.0.7 lock file (357 packages, Python 3.14.2) [measured], set against `docs/ARCHITECTURE.md`'s Artifact budget (Python within 75 MB, load groups `numpy-pandas`, `scipy-statsmodels`, `sklearn`, `matplotlib`, `testing`; which groups fit is measured at `docs/PLAN.md` stage 25 on the owner's phone).

| Package | In Pyodide 314.0.7 | Load group | Proposals that use it | Consequence |
|---|---|---|---|---|
| NumPy 2.4.6, pandas 3.0.2 | Yes; run in the Artifact on the owner's iPhone (`spikes/README.md`) | `numpy-pandas` | P1, P3, P5, P10, P14, P15 | `pyodide-core`: both targets |
| SciPy 1.18.0 | Yes | `scipy-statsmodels` | P3 (root finders, quadrature), P4 | Both targets if the group fits at E8; otherwise `web` |
| statsmodels 0.14.6 | Yes | `scipy-statsmodels` | P5, P11 | As SciPy |
| scikit-learn 1.8.0 | Yes | `sklearn` | P14 baselines | As SciPy |
| cvxpy-base 1.8.2 (with Clarabel 0.11.1), highspy 1.13.1 | Yes; cvxpy depends on NumPy, SciPy and Clarabel | Not yet in a load group | P4, P6 (constrained portfolios) | Proposed: add to `scipy-statsmodels` or a small `optimisation` group; import and solve not yet tested in a browser [unverified] |
| SymPy 1.14.0 | Yes | Not in a load group | P8 (verifying the Black-Scholes to heat-equation transformation) | Run in CI or on the web app; the learner-facing check can be numeric |
| linearmodels, arch | No | | P11 (Fama-MacBeth, panels, GARCH) | Written from NumPy, SciPy and statsmodels pieces |
| PyMC, ArviZ, NumPyro | No | | P15 | Samplers from scratch; probabilistic programming off-device |
| PyTorch, JAX | No | | P14 | NumPy networks in the browser; course 2 off-device |

---

### 5.4 Review additions (`docs/PLAN.md` 12 decision 2)

| Addition | Hours | Placement | Widgets | Python | Why |
|---|---|---|---|---|---|
| 2.1b Deep learning core | 120 | New Stage 2 item after 2.1, all tracks | `autodiff-tape`, `attention-lab` (from P14), a training-curve scene | `numpy-pandas`: micrograd, an MLP and a character-level transformer at toy scale in NumPy on Pyodide | The project's aim includes ML-lab-calibre thinking; the counted path holds two neural-network levels. Spine: Prince, *Understanding Deep Learning*, chapters 1 to 12; code: Karpathy's *Neural Networks: Zero to Hero* re-implemented in NumPy; problems: MIT 6.7960. A toy double-descent replication is offered as a 3.1 option |
| A1 Real analysis | 60 | After 1.3, researcher and ML research tracks | `epsilon-delta`, `derivation-steps`, `proof-builder` (P7) | none | Research interviews and ML theory assume proof-based analysis; Abbott, *Understanding Analysis*, chapters 1 to 6, taken from P7 or from P16's 120 h of analysis |

## 6. Resource canon

**How to read the tables.** One table per curriculum item, then one per proposal. Roles map to `Citation.use` (decision 3 in section 0.4): **Spine** = `basis` (the one text lessons follow and cite by section; the owner's pick wherever the curriculum names one); **Lectures** = `parallel-reading`; **Problems** = `problem-inspired` (homework mirrors these problem types, with new wording and numbers); **Stretch** = `further`. **Reading** and **Papers** rows are `parallel-reading` unless a curriculum file says otherwise. The **Id** column gives the `src.*` id for `content/sources.yaml`; ids marked † are new in revision 2 (section 8.1 lists them with their origin).

**Evidence.** Every entry is [recalled] unless tagged [searched] or [unverified]. [recalled] here means I am confident the work exists as described; edition years and chapter numbers still need a person with the book before `checked: true`. [unverified] means I am not confident of a detail named in the entry, and it must be checked before any lesson cites it. Chapter numbers refer to the edition named.

**Licences.** "free" means legally free to read online. Only CC BY works may be adapted (`problem-adapted`): OpenStax Precalculus 2e [searched] and, as I recall, OpenStax Prealgebra, Elementary, Intermediate and College Algebra 2e. **The OpenStax Calculus volumes are CC BY-NC-SA 4.0** [searched] and, like MIT OpenCourseWare (CC BY-NC-SA) and Prince's book (CC BY-NC-ND [searched]), are cited and mirrored, never adapted (`content-format.md` 9.4).

### Where the solutions are

Homework mirrors problem types, so the learner can check a mirrored problem only against our own verified solution; but the original set is still the best second source when its solutions are public. "Public" means free to read online; "paid" means a solutions manual or a book of solutions must be bought; "none" means the app writes and verifies its own worked solutions (`content-format.md` decision 7) and Bertie marks against them.

| Item | Problem source with public solutions | Paid or partial | None public |
|---|---|---|---|
| 0.1, 0.2 | GCSE Higher papers with mark schemes; Corbettmaths 5-a-day answers; UKMT papers with solutions; OpenStax algebra books (answers to odd exercises) | | |
| 0.3 | A-level papers with mark schemes; STEP Support Programme modules with hints and solutions; OpenStax Precalculus 2e (odd answers) | | |
| 0.4, 1.2 | | Automate the Boring Stuff practice questions (answers in an appendix [unverified for the 3rd ed]) | Missing Semester exercises |
| 1.1 | CS50P problem sets (auto-checked by `check50`; no model solutions) | 6.100L problem sets [unverified: solutions] | |
| 1.3 | MIT 18.01SC (Fall 2010) problem sets, exams and final with solutions [searched for the final]; 18.02SC problem sets with solutions | OpenStax Calculus odd answers (NC-SA: cite only) | |
| 1.4 | MIT 18.06 (Spring 2010) exams and final with solutions [searched]; 18.06SC (Fall 2011) problem sets and exams with solutions | Strang's selected solutions for ILA [unverified for the 6th ed] | |
| 1.4b (P7) | MIT 6.042J (Spring 2015) problem sets and exams with solutions; Hammack, *Book of Proof* (odd solutions) | | |
| 1.5 | Stat 110 strategic practice (about 250 problems with detailed solutions) and practice finals [searched]; Blitzstein and Hwang's starred exercises with posted solutions [searched]; MIT 6.041 (Fall 2010) and 18.600 (Fall 2019) problem sets and exams with solutions [searched for 18.600] | | |
| 1.5 (P2) | MIT 18.445 (Spring 2015) homework with solutions [searched] | *One Thousand Exercises in Probability* (solutions in the book) [searched] | Durrett's exercises |
| 1.6 | MIT 18.05 (Spring 2014) problem sets and exams with solutions | DeGroot and Schervish student solutions manual | 18.650 problem sets [unverified: solutions] |
| 1.6b (P8) | MIT 18.03SC (Fall 2011) problem sets and unit exams with solutions | | |
| 1.7 | MIT 15.401 (Fall 2008) problem sets with solutions [unverified] | Hull, Student Solutions Manual | |
| 1.8 | MIT 6.006 (Spring 2020) problem sets with solutions; NeetCode 150 video solutions | | CSES (no official solutions) |
| 1.9 | learncpp.com quizzes with solutions | | Joshi's C++ exercises |
| 2.0a (P3) | MIT 18.335J (Spring 2019) problem sets with solutions [searched] | | Glasserman's exercises |
| 2.0b (P4) | | | Boyd and Vandenberghe's additional exercises [unverified: solutions not public]; EE364A homework |
| 2.0c (P6) | MIT 15.433 (Spring 2003) assignments with solutions [searched] | Luenberger solutions manual (instructors) | |
| 2.0d (P12) | | | None: the app builds every exercise from the papers |
| 2.0e (P13) | CS:APP practice problems (solutions at the end of each chapter); the CS:APP labs (self-checking autograders) | | MIT 6.172 projects |
| 2.1 | MIT 6.036 (Fall 2020) exercises, auto-checked on the Open Learning Library [searched] | | ISLP exercises (community answers only); CS229 problem sets [unverified: solutions] |
| 2.1x (P14) | MIT 6.7960 (Fall 2024) problem sets with solutions [searched]; CS231n and CS336 assignments ship with tests | | |
| 2.2 | | | Tsay's exercises; FPP exercises; 14.384 problem sets [unverified: solutions] |
| 2.2b (P11) | Cochrane's online Asset Pricing class: problem sets and exams [searched; whether solutions are released, unverified] | Wooldridge student solutions manual | |
| 2.2c (P1) | | | None: the app's audit exercises are its own |
| 2.3, 2.4 | Codeforces editorials | | |
| 3.2 (P16) | | Chin, Nel and Ólafsson, vol. 1 (full solutions) [searched] | Shreve's exercises; Cambridge example sheets (no solutions, as I recall) |
| P16 prerequisites | MIT 18.100A (Fall 2020) problem sets [unverified: solutions] | | Abbott's exercises |
| 3.3 | Every book in the list prints its solutions | | |
| P10 | MIT 18.S096 Matrix Calculus (IAP 2023) problem sets with solutions [searched] | | |
| P9 | MacKay (many exercises solved in the book) | | |
| P15 | BDA3 selected solutions (authors' site); McElreath's homework solutions (course repository) [unverified] | | |

### Stage 0

**0.1 Number (60 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Khan Academy, Arithmetic, then Pre-algebra (free) | Whole courses, in order | `src.khan-prealgebra` |
| Reading | OpenStax, Prealgebra 2e (free, CC BY 4.0) | Section exercises; adaptable under CC BY; used by `stage0-number-algebra.md` | `src.openstax-prealgebra-2e` † |
| Problems | GCSE Mathematics Higher past papers and mark schemes (AQA, Pearson Edexcel, OCR; free from the boards) | Number questions, timed | `src.gcse-papers` |
| Problems | Corbettmaths, 5-a-day and topic worksheets with answers (free) | Daily retrieval practice | `src.corbettmaths` |
| Stretch | UKMT Junior and Intermediate Mathematical Challenge past papers with solutions | Number sense as problem solving | `src.ukmt-challenges` |
| Reference | Python documentation, tutorial appendix "Floating-Point Arithmetic: Issues and Limitations" (free) | Lesson 42, binary floating point | `src.python-docs-float` † |

**0.2 Algebra (180 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Khan Academy, Algebra 1 and Algebra 2; UK route Corbettmaths GCSE videos | Whole courses | `src.khan-algebra` |
| Reading | OpenStax, Elementary Algebra 2e, Intermediate Algebra 2e and College Algebra 2e (free, CC BY 4.0) | Section exercises; adaptable | `src.openstax-elementary-algebra-2e` †, `src.openstax-intermediate-algebra-2e` †, `src.openstax-college-algebra-2e` † |
| Problems | GCSE Higher past papers; Corbettmaths worksheets | Timed papers; topic sets | `src.gcse-papers` |
| Stretch | Gelfand and Shen, *Algebra* (Birkhäuser 1993, reprinted) | The whole short book: algebra taught as reasoning, from a correspondence school for strong pupils | `src.gelfand-shen-algebra` |
| Stretch | Rusczyk, *Introduction to Algebra* (Art of Problem Solving; 2nd ed [unverified]) | Chapters on equations, functions and quadratics | `src.aops-intro-algebra` |
| Stretch | University of Oxford, Mathematics Admissions Test (MAT) past papers with solutions (free) | Algebra and functions as problem solving | `src.mat-papers` † |

**0.3 Precalculus (200 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Khan Academy, Precalculus; UK route TLMaths A-level Pure; one-book option Lang, *Basic Mathematics* (Addison-Wesley 1971; Springer reprint 1988) | Whole course | `src.khan-precalc`, `src.lang-basic-math` |
| Problems | A-level Mathematics Pure papers and mark schemes (Pearson Edexcel, AQA, OCR; free) | Exponentials, logarithms, trigonometry, sequences, binomial expansion, vectors | `src.alevel-papers` |
| Problems | OpenStax, Precalculus 2e (free, CC BY 4.0 [searched]) | End-of-section exercises; adaptable under CC BY | `src.openstax-precalc-2e` |
| Problems | Stat 110 Strategic Practice 1 (counting) | Course C, counting and chance | `src.stat110-2013` |
| Stretch | Gelfand and Saul, *Trigonometry* (Birkhäuser 2001); Gelfand, Glagoleva and Shnol, *Functions and Graphs* (1969; Dover reprint) | Trigonometry and graphs as reasoning | `src.gelfand-trig`, `src.gelfand-functions` |
| Stretch | University of Cambridge, STEP Support Programme (free), foundation modules | The bridge to university-style problems; the first modules need only A-level Pure | `src.step-support` |
| Stretch | University of Cambridge, Underground Mathematics (free); Isaac Maths (Cambridge, free) | Rich problems by topic, used by `stage0-precalc-computing.md` | `src.underground-maths` †, `src.isaac-maths` † |

**0.4 Computer basics (40 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Sweigart, *Automate the Boring Stuff with Python*, 3rd ed (No Starch, May 2025) [searched]; free online (the 2nd ed certainly; the 3rd [unverified]) | Introduction and ch. 1 to 3, as the curriculum says. Pin the edition: the 3rd ed reorganised and added chapters, so "the first three chapters" may cover different ground [unverified] | `src.sweigart-atbs` |
| Lectures | MIT, The Missing Semester of Your CS Education, 2026 edition (free, videos): lecture 1, Course Overview and Introduction to the Shell [searched] | Shell | `src.missing-semester-2026` † |
| Reading | Shotts, *The Linux Command Line*, 2nd ed (No Starch 2019; free PDF from the author) ch. 1 to 4 | Navigation, files, commands, used by `stage0-precalc-computing.md` | `src.shotts-tlcl` † |
| Lectures | Harvard CS50x (free) weeks 0 and 1 | First contact with programming ideas | `src.cs50x` |
| Practice | keybr.com | Touch typing | `src.keybr` |

**0.5 Mental arithmetic (20 h, then daily)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Zetamac arithmetic game | Daily 10 minutes | `src.zetamac` |
| Stretch | Benjamin and Shermer, *Secrets of Mental Math* (Three Rivers 2006) | Multiplication, squaring and estimation techniques | `src.benjamin-mental-math` |
| Problems | App-generated timed sets in the 80-in-8 format the curriculum names | Interview format | (generated) |

### Stage 1

**1.1 Python (150 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Harvard CS50P, Introduction to Programming with Python (free; lectures and auto-checked problem sets) | Whole course (`stage1-python-tools.md` decision 2) | `src.cs50p` |
| Lectures | MIT 6.100L Introduction to CS and Programming Using Python, Fall 2022 (OCW) [searched], with Guttag, *Introduction to Computation and Programming Using Python*, 3rd ed (MIT Press 2021) | University-grade parallel: computation, recursion, complexity, testing | `src.mit-6100l-2022`, `src.guttag-2021` |
| Problems | 6.100L problem sets; CS50P problem sets | Homework types | (as above) |
| Spine (data) | McKinney, *Python for Data Analysis*, 3rd ed (O'Reilly 2022, free online) ch. 4 to 11 and appendix A | NumPy, pandas, cleaning, grouping, plotting, time series (the 1.1 exit) | `src.mckinney-pda-3e` |
| Problems (data) | VanderPlas, *Python Data Science Handbook*, 2nd ed (O'Reilly 2022, free online) [unverified year] | NumPy and pandas practice, as `stage1-python-tools.md` uses | `src.vanderplas-pdsh-2e` † |
| Stretch | Ramalho, *Fluent Python*, 2nd ed (O'Reilly 2022) | Stage 2, as the curriculum says | `src.ramalho-fluent-2e` |

**1.2 Tools (40 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | MIT, The Missing Semester, 2026 edition (free): command-line environment, development environment and tools, debugging and profiling, version control and Git, packaging and shipping code, code quality [searched]; the 2020 edition for the lectures 2026 dropped (shell tools and scripting, editors, data wrangling, metaprogramming, security) | Shell, Git, debugging, profiling, packaging, testing culture | `src.missing-semester-2026` †, `src.missing-semester-2020` |
| Spine (Git) | Chacon and Straub, *Pro Git*, 2nd ed (Apress 2014, free) ch. 1 to 3 | Git's object model and branching | `src.pro-git-2e` |
| Spine (SQL) | SQLBolt (free, interactive) | SQL basics | `src.sqlbolt` |
| Lectures | CMU 15-445/645 Database Systems (Pavlo; recorded lectures, free) lectures 1 and 2 | Relational model and modern SQL | `src.cmu-15445` |
| Stretch | Okken, *Python Testing with pytest*, 2nd ed (Pragmatic Bookshelf 2022) ch. 1 to 5 | Fixtures, parametrisation | `src.okken-pytest-2e` |
| Stretch (G18) | MIT Software Construction readings (free; 6.102, formerly 6.031 and 6.005) [searched] | Specifications, testing, abstraction | `src.mit-software-construction` |

**1.3 Calculus (200 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | OpenStax, *Calculus* volumes 1 to 3 (free; CC BY-NC-SA 4.0 [searched], so `problem-inspired` only) | Whole cover list (`stage1-calculus.md` decision 2) | `src.openstax-calculus` |
| Alternative | Stewart, Clegg and Watson, *Calculus: Early Transcendentals*, 9th ed (Cengage 2020): ch. 1 to 7, 11, 14 (14.8 Lagrange multipliers), 15 | The curriculum's other named text; paid | `src.stewart-calculus-9e` |
| Lectures | MIT 18.01SC Single Variable Calculus (Fall 2010) and 18.02SC Multivariable Calculus (Fall 2010) | Lecture parallels | `src.mit-1801sc`, `src.mit-1802sc` |
| Problems | 18.01SC problem sets and exams with solutions, including the final [searched]; 18.02SC problem sets on partial derivatives and Lagrange multipliers; the curriculum's exit is the 18.01 final | Homework and exit | (as above) |
| Intuition | 3Blue1Brown, *Essence of Calculus* (2017) | Before each unit, as the curriculum says | `src.3b1b-calculus` |
| Stretch | Cambridge STEP past papers 2 and 3, with STEP Support worked solutions | The admissions problem standard for technique | `src.step-papers` |
| Stretch | Spivak, *Calculus*, 4th ed (Publish or Perish 2008); Apostol, *Calculus* vol. 1, 2nd ed (Wiley 1967) | For P16 learners | `src.spivak-calculus-4e`, `src.apostol-calculus-1` |
| Stretch | Boyd and Vandenberghe, *Convex Optimization*, §5.1 (the Lagrange dual function) | The multiplier as a price; the bridge to P4 (`stage1-calculus.md` M4) | `src.boyd-cvx` |

**1.4 Linear algebra (150 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Strang, *Introduction to Linear Algebra*, 6th ed (Wellesley-Cambridge 2023) [searched for edition and chapter list]: ch. 1 to 7 (vectors and matrices to the SVD); ch. 9 and 10 later | Whole cover list | `src.strang-ila-6e` |
| Lectures | MIT 18.06 Linear Algebra (Spring 2010, Strang) videos; 18.06SC (Fall 2011) recitations | Lecture parallels | `src.mit-1806`, `src.mit-1806sc` |
| Problems | 18.06 Spring 2010 exams and final with answers [searched]; 18.06SC problem sets and exams with solutions | Homework and exit | (as above) |
| Reading | Hefferon, *Linear Algebra*, 4th ed (2020, free) | A second explanation with proofs, as `stage1-linear-algebra.md` uses | `src.hefferon` † |
| Reading | Deisenroth, Faisal and Ong, *Mathematics for Machine Learning* (CUP 2020, free PDF) ch. 2 to 5 | The ML reading of the same material; ch. 5 is P10's matrix calculus | `src.mml` † |
| Stretch | Boyd and Vandenberghe, *Introduction to Applied Linear Algebra: Vectors, Matrices, and Least Squares* (CUP 2018, free) ch. 12 to 16 | Least squares in applications | `src.boyd-vmls` |
| Stretch | Strang, *Linear Algebra and Learning from Data* (Wellesley-Cambridge 2019), with MIT 18.065 Spring 2018 [searched] | Low rank, covariance, PCA | `src.strang-lalfd`, `src.mit-18065` |
| Papers | Strang, "The Fundamental Theorem of Linear Algebra" (American Mathematical Monthly 1993); Bryan and Leise, "The \$25,000,000,000 Eigenvector: The Linear Algebra behind Google" (SIAM Review 2006); Moler and Van Loan, "Nineteen Dubious Ways to Compute the Exponential of a Matrix, Twenty-Five Years Later" (SIAM Review 2003); von Luxburg, "A Tutorial on Spectral Clustering" (Statistics and Computing 2007) | The four subspaces; PageRank; $e^{At}$; spectral clustering | `src.strang-ftla-1993` †, `src.bryan-leise-2006` †, `src.moler-vanloan-2003` †, `src.vonluxburg-2007` † |
| Papers (finance) | Litterman and Scheinkman, "Common Factors Affecting Bond Returns" (Journal of Fixed Income 1991); Laloux, Cizeau, Bouchaud and Potters, "Noise Dressing of Financial Correlation Matrices" (Physical Review Letters 1999); Ledoit and Wolf, "Honey, I Shrunk the Sample Covariance Matrix" (Journal of Portfolio Management 2004); Avellaneda and Lee, "Statistical Arbitrage in the US Equities Market" (Quantitative Finance 2010) | Yield-curve PCA; random-matrix noise; shrinkage (lesson 95); PCA residual trading | `src.litterman-scheinkman-1991` †, `src.laloux-1999` †, `src.ledoit-wolf-2004` †, `src.avellaneda-lee-2010` † |
| Theory | Hastie, Tibshirani and Friedman, *The Elements of Statistical Learning*, 2nd ed (free), ch. 3 and 14 | Least squares, ridge and PCA as learning methods | `src.esl-2e` |
| Stretch | Axler, *Linear Algebra Done Right*, 4th ed (Springer 2024, open access) | The proof-based second course, after P7 | `src.axler-ladr-4e` |

**1.4b Proof and discrete mathematics (P7, 70 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Velleman, *How to Prove It*, 3rd ed (CUP 2019) ch. 1 to 6 (sentential and quantificational logic, proofs, relations, functions, induction) | Logic and proof as a subject, after 0.3 R1 and R2 | `src.velleman-3e` |
| Spine (discrete) | Lehman, Leighton and Meyer, *Mathematics for Computer Science* (MIT, 2017 revision, free) parts I to III, selected chapters | Number theory, graphs, counting | `src.mcs-2017` |
| Lectures | MIT 6.042J Mathematics for Computer Science (video lectures Fall 2010; problem sets and exams with solutions Spring 2015) | Lecture parallels and exit | `src.mit-6042j` |
| Problems | Hammack, *Book of Proof*, 3rd ed (2018, free) exercises, odd solutions given | Volume practice | `src.hammack-proof-3e` |
| Stretch | Engel, *Problem-Solving Strategies* (Springer 1998) ch. 1 (the invariance principle), 2 (colouring proofs), 3 (the extremal principle), 4 (the box principle) [recalled] | Feeds interview puzzles directly | `src.engel-strategies` |

**1.5 Probability (250 h, +15 h P2)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Blitzstein and Hwang, *Introduction to Probability*, 2nd ed (CRC 2019, free online) ch. 1 to 11, then 12 (MCMC) and 13 (Poisson processes) | Whole cover list | `src.blitzstein-hwang-2019` |
| Lectures | Harvard Stat 110 lectures (free) | Lecture parallels | `src.stat110-2013` |
| Problems | Stat 110 strategic practice and homework with solutions, and practice finals (free) [searched]; the book's exercises marked with solutions online | Homework; the curriculum's exit uses Stat 110 finals | `src.stat110-2013` |
| Alternative | Evans and Rosenthal, *Probability and Statistics: The Science of Uncertainty*, 2nd ed (W. H. Freeman 2010; free PDF from the authors) | The curriculum's named alternative (the Toronto text) | `src.evans-rosenthal-2e` † |
| Lectures (alternative) | MIT RES.6-012 Introduction to Probability (2018, Tsitsiklis) and 6.041 (Fall 2010), with Bertsekas and Tsitsiklis, *Introduction to Probability*, 2nd ed (Athena 2008); MIT 18.600 Probability and Random Variables (Fall 2019, Sheffield; exams with solutions) [searched] | A second explanation of the same material | `src.mit-6041`, `src.bertsekas-tsitsiklis-2e`, `src.mit-18600-2019` † |
| Problems (alternative) | Ross, *A First Course in Probability*, 10th ed (Pearson 2019), the Stanford STATS 116 text [searched] | Volume practice on the named distributions | `src.ross-first-course-10e` † |
| Stretch | Norris, *Markov Chains* (CUP 1997) ch. 1 | The Cambridge treatment of discrete chains, as `stage1-probability.md` Z1 uses | `src.norris-markov` † |
| Spine (P2) | Durrett, *Essentials of Stochastic Processes*, 3rd ed (Springer 2016) ch. 4 (continuous-time Markov chains) and 5 (martingales) [searched] | P2's continuous-time chains and the martingale review | `src.durrett-essentials-3e` † |
| Reading (P2) | Grimmett and Stirzaker, *Probability and Random Processes*, 4th ed (OUP 2020) ch. 12 (martingales; §12.5 optional stopping) and 13 (diffusion processes) [recalled section titles] | Brownian motion and first passage; 1.5 Z4's stretch reading | `src.grimmett-stirzaker-4e` |
| Problems (P2) | Grimmett and Stirzaker, *One Thousand Exercises in Probability*, 3rd ed (OUP 2020), with solutions [searched]; Williams, *Probability with Martingales* ch. 10 exercises | Martingale and stopping problems | `src.grimmett-stirzaker-1000`, `src.williams-martingales` |
| Lectures (P2) | MIT 6.262 Discrete Stochastic Processes (Spring 2011, Gallager, 25 videos) [searched]; MIT 18.445 Introduction to Stochastic Processes (Spring 2015; Markov chains, random walks, martingales; homework with solutions drawn from Levin, Peres and Wilmer) [searched] | Markov, renewal and martingale lectures; solved homework | `src.mit-6262-2011` †, `src.mit-18445` |
| Stretch | Mosteller, *Fifty Challenging Problems in Probability* (1965; Dover 1987) | Already in 3.3; begin here with the weekly problems | `src.mosteller-50` |

**1.6 Statistics (120 h, +25 h P5)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | DeGroot and Schervish, *Probability and Statistics*, 4th ed (Pearson 2012) ch. 7 to 11 and §12.6 (the bootstrap) | Estimation, sampling distributions, tests, categorical and non-parametric methods, linear models | `src.degroot-schervish-4e` |
| Bridge | Diez, Çetinkaya-Rundel and Barr, *OpenIntro Statistics*, 4th ed (2019, free) | The curriculum's "if it is too steep" route | `src.openintro-4e` |
| Lectures | MIT 18.650 Statistics for Applications (Fall 2016, Rigollet) [searched]; MIT 18.05 Introduction to Probability and Statistics (Spring 2014, Orloff and Bloom) as a gentler parallel; Stanford STATS 200 lecture notes (Autumn 2016, Zhou Fan) [searched for the page] | Lecture parallels | `src.mit-18650`, `src.mit-1805`, `src.stanford-stats200` † |
| Problems | 18.05 problem sets and exams with solutions; 18.650 problem sets | Homework | (as above) |
| Problems (regression) | James, Witten, Hastie, Tibshirani and Taylor, *An Introduction to Statistical Learning with Applications in Python* (Springer 2023, free) ch. 3 | Regression practice; `stage1-statistics-ts.md` names the R edition, which maps here (section 8.1) | `src.islp-2023` |
| Papers | Benjamini and Hochberg, "Controlling the False Discovery Rate" (JRSS B 1995); White, "A Heteroskedasticity-Consistent Covariance Matrix Estimator and a Direct Test for Heteroskedasticity" (Econometrica 1980); Anscombe, "Graphs in Statistical Analysis" (The American Statistician 1973); Brown, Cai and DasGupta, "Interval Estimation for a Binomial Proportion" (Statistical Science 2001); Efron and Morris, "Stein's Paradox in Statistics" (Scientific American 1977); Wasserstein and Lazar, "The ASA Statement on p-Values" (The American Statistician 2016) | FDR; HC errors; plotting first; Wilson intervals; shrinkage; what a $p$-value is not | `src.benjamini-hochberg-1995` †, `src.white-1980` †, `src.anscombe-1973` †, `src.brown-cai-dasgupta-2001` †, `src.efron-morris-1977` †, `src.wasserstein-lazar-2016` † |
| Papers (finance) | Lo, "The Statistics of Sharpe Ratios" (FAJ 2002); Bailey and López de Prado, "The Deflated Sharpe Ratio" (JPM 2014); Harvey, Liu and Zhu (RFS 2016) | Lessons 19, 41 and 42 | `src.lo-2002`, `src.dsr-2014`, `src.hlz-2016` |
| Spine (P5) | Wasserman, *All of Statistics* (Springer 2004) ch. 8 to 10, 13 | Bootstrap, parametric inference, testing, regression | `src.wasserman-aos` |
| Stretch | Casella and Berger, *Statistical Inference*, 2nd ed (Duxbury 2002) ch. 6 to 10; Efron and Hastie, *Computer Age Statistical Inference* (CUP 2016, free) | Rigour; modern methods | `src.casella-berger-2e`, `src.efron-hastie-casi` |

**1.6b Differential equations (P8, 45 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Strang, *Differential Equations and Linear Algebra* (Wellesley-Cambridge 2014) ch. 2 (second-order equations), 3 (graphical and numerical methods), 6 (eigenvalues and systems) [recalled], and from ch. 8, Fourier and Laplace Transforms, the heat-equation section [searched] | Second order, systems, heat equation (first order is 1.3 level I6) | `src.strang-delta` |
| Lectures | MIT 18.03SC Differential Equations (Fall 2011); Strang and Moler, RES.18-009 Learn Differential Equations: Up Close (Fall 2015) [searched] | Lecture parallels | `src.mit-1803sc`, `src.mit-res18009` |
| Problems | 18.03SC problem sets and unit exams with solutions | Homework and exit | `src.mit-1803sc` |
| Stretch | Hirsch, Smale and Devaney, *Differential Equations, Dynamical Systems, and an Introduction to Chaos*, 3rd ed (Academic Press 2013) | Phase-plane depth | `src.hirsch-smale-devaney` |

**1.7 Finance basics (100 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine 1 | Khan Academy, Finance and Capital Markets | Shares, bonds, interest | `src.khan-finance` |
| Spine 2 | Zerodha Varsity modules on markets, futures and options (free) | Instruments | `src.zerodha-varsity` |
| Spine 3 | Hull, *Options, Futures, and Other Derivatives*, 11th ed (Pearson; copyright 2022) [searched for edition and chapter list]: ch. 1 (Introduction), 2 (Futures Markets and Central Counterparties), 4 (Interest Rates), 5 (Determination of Forward and Futures Prices), 7 (Swaps), 10 (Mechanics of Options Markets), 11 (Properties of Stock Options), 13 (Binomial Trees), 15 (The Black-Scholes-Merton Model), 19 (The Greek Letters) | Forwards, futures, swaps, option properties, binomial trees, Black-Scholes, Greeks | `src.hull-ofod-11e` |
| Spine 4 | Harris, *Trading and Exchanges: Market Microstructure for Practitioners* (OUP 2003) | Order books, dealers, informed trading | `src.harris-trading-exchanges` |
| Lectures | MIT 15.401 Finance Theory I (Fall 2008, Lo); Yale ECON 252 Financial Markets (2011, Shiller; Open Yale Courses) | Lecture parallels | `src.mit-15401`, `src.yale-econ252` |
| Problems | Hull's end-of-chapter practice questions, with the Student Solutions Manual (Pearson) | Homework | `src.hull-ofod-11e` |
| Stretch | Shreve, *Stochastic Calculus for Finance I* (Springer 2004) ch. 1; Joshi, *The Concepts and Practice of Mathematical Finance*, 2nd ed (CUP 2008) ch. 1 to 3 | Binomial pricing done properly | `src.shreve-1`, `src.joshi-concepts-2e` |

**1.8 Data structures and algorithms (250 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Bhargava, *Grokking Algorithms*, 2nd ed (Manning, March 2024) [searched], then NeetCode 150 | First read, then the problem list | `src.grokking`, `src.neetcode150` |
| Lectures | MIT 6.006 Introduction to Algorithms (Spring 2020, Demaine, Ku and Solomon) [searched]; 6.046J Design and Analysis of Algorithms (Spring 2015) [searched] | Theory thread (G17) | `src.mit-6006-2020`, `src.mit-6046j-2015` |
| Problems | 6.006 problem sets with solutions; NeetCode 150; a held-out bank for the exit | Homework | (as above) |
| Reference | Cormen, Leiserson, Rivest and Stein, *Introduction to Algorithms*, 4th ed (MIT Press 2022) | Reference only, as the curriculum says | `src.clrs-4e` |
| Lectures (developer) | Stanford CS106B Programming Abstractions (C++), with Roberts, *Programming Abstractions in C++* (Pearson 2014) [searched] | The same structures in C++, for the developer track and 1.9 | `src.stanford-cs106b` †, `src.roberts-pac` † |
| Stretch | Skiena, *The Algorithm Design Manual*, 3rd ed (Springer 2020); Aziz, Lee and Prakash, *Elements of Programming Interviews in Python* (2016) | Design catalogue; interview depth | `src.skiena-adm-3e`, `src.epi-python` |

**1.9 C++ (140 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | learncpp.com (free); or Stroustrup, *Programming: Principles and Practice Using C++*, 3rd ed (Addison-Wesley 2024) | Whole course | `src.learncpp`, `src.stroustrup-ppp-3e` |
| Lectures | Stanford CS106L Standard C++ Programming (slides and assignments public) | Modern C++ idioms | `src.stanford-cs106l` |
| Problems | Joshi, *C++ Design Patterns and Derivatives Pricing*, 2nd ed (CUP 2008) | A tree and Monte Carlo pricer built up in C++, matched to the 1.9 exit | `src.joshi-cpp-2e` |
| Stretch | Stroustrup, *A Tour of C++*, 3rd ed (Addison-Wesley 2022); Meyers, *Effective Modern C++* (O'Reilly 2014) | After a first book, as the curriculum says | `src.stroustrup-tour-3e`, `src.meyers-emc` |
| Course | Baruch and QuantNet, C++ Programming for Financial Engineering (online certificate, paid) [searched for existence] | Graded alternative | `src.baruch-cpp` |

### Stage 2

**2.0a Numerical methods and Monte Carlo (P3, 120 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine (numerical analysis) | Süli and Mayers, *An Introduction to Numerical Analysis* (CUP 2003) ch. 1 (equations by iteration), 2 (linear systems), 6 (polynomial interpolation), 7 (numerical integration), 12 (initial value problems) [recalled chapter titles] | Equations, linear systems, interpolation, quadrature, ODE solvers | `src.suli-mayers` |
| Spine (linear algebra) | Trefethen and Bau, *Numerical Linear Algebra* (SIAM 1997) lectures 1 to 31 | SVD, QR, least squares, conditioning, stability, floating point (lecture 13), Gaussian elimination, Cholesky, eigenvalue algorithms | `src.trefethen-bau` |
| Spine (Monte Carlo) | Glasserman, *Monte Carlo Methods in Financial Engineering* (Springer 2003) ch. 1 to 4, 7 | Random variables, paths, variance reduction, sensitivities | `src.glasserman-mc` |
| Lectures | MIT 18.335J Introduction to Numerical Methods (Spring 2019; notes, problem sets and exams with solutions) [searched] | Floating point, backward error, stability | `src.mit-18335j` |
| Paper | Goldberg, "What Every Computer Scientist Should Know About Floating-Point Arithmetic" (ACM Computing Surveys 1991) | Floating point | `src.goldberg-1991` |
| Reading (PDEs) | Wilmott, Howison and Dewynne, *The Mathematics of Financial Derivatives: A Student Introduction* (CUP 1995) | The Black-Scholes PDE, the heat equation and finite differences, from the Oxford school | `src.wilmott-howison-dewynne` † |
| Stretch | Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed (SIAM 2002); Capiński and Zastawniak, *Numerical Methods in Finance with C++* (CUP 2012) | Error analysis reference; finite differences and trees in C++ | `src.higham-accuracy-2e`, `src.capinski-zastawniak` |

**2.0b Optimisation (P4, 80 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Boyd and Vandenberghe, *Convex Optimization* (CUP 2004, free PDF) ch. 1 to 5, 9 and 10 | Convex sets and functions, problems, duality, unconstrained and equality-constrained methods | `src.boyd-cvx` |
| Lectures | Stanford EE364A Convex Optimization I (Boyd; recorded lectures) | Lecture parallels | `src.stanford-ee364a` |
| Problems | Boyd and Vandenberghe, *Additional Exercises for Convex Optimization* (free PDF; solutions not public [unverified]) | Homework types | `src.boyd-cvx-exercises` |
| Finance | Cornuéjols, Peña and Tütüncü, *Optimization Methods in Finance*, 2nd ed (CUP 2018) | LP, QP and mean-variance, conic models in finance | `src.cornuejols-omf-2e` |
| Stretch | Vanderbei, *Linear Programming: Foundations and Extensions*, 5th ed (Springer 2020); Nocedal and Wright, *Numerical Optimization*, 2nd ed (Springer 2006) | LP and duality in depth; algorithms reference | `src.vanderbei-lp-5e`, `src.nocedal-wright-2e` |

**2.0c Portfolio theory, risk and fixed income (P6, 75 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Luenberger, *Investment Science*, 2nd ed (OUP 2013) [searched for the edition, which adds chapters on risk management, credit risk, and data and statistics]: the chapters on the basic theory of interest, fixed-income securities, the term structure, mean-variance portfolio theory, the CAPM, and models and data [titles recalled; numbers unverified for the 2nd ed] | Interest rates, bonds, term structure, mean-variance, CAPM, factor models | `src.luenberger-is-2e` |
| Lectures | MIT 15.401 Finance Theory I (Fall 2008, Lo); MIT 15.433 Investments (Spring 2003; notes for 23 lectures, assignments with solutions) [searched]; MIT 18.S096 Fall 2013 lectures on portfolio theory, factor modelling, value at risk and yield curves [searched for topics] | Lecture parallels | `src.mit-15401`, `src.mit-15433-2003` †, `src.mit-18s096-2013` |
| Problems | Luenberger's end-of-chapter exercises; Hull ch. 4 (Interest Rates) and 22 (Value at Risk and Expected Shortfall) [searched for chapter titles]; 15.433 assignments | Homework | (as above) |
| Stretch | Grinold and Kahn, *Active Portfolio Management*, 2nd ed (McGraw-Hill 1999) ch. 2 (CAPM), 3 (risk), 4 (exceptional return), 5 (the information ratio), 6 (the fundamental law), 14 (portfolio construction) [searched]; Tuckman and Serrat, *Fixed Income Securities: Tools for Today's Markets*, 4th ed (Wiley 2022) [searched]; McNeil, Frey and Embrechts, *Quantitative Risk Management*, revised ed (Princeton 2015) | Fundamental law; fixed income depth; risk measures | `src.grinold-kahn-2e`, `src.tuckman-serrat-4e`, `src.mfe-qrm` |

**2.0d Market microstructure and execution (P12, 50 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Foucault, Pagano and Röell, *Market Liquidity: Theory, Evidence, and Policy*, 2nd ed (OUP 2023) [searched] | Spreads, adverse selection, Kyle, inventory, algorithmic and high-frequency trading | `src.foucault-liquidity` |
| Papers | Roll (JF 1984); Kyle (Econometrica 1985); Glosten and Milgrom (JFE 1985); Almgren and Chriss, "Optimal Execution of Portfolio Transactions" (Journal of Risk 3(2), winter 2000/01) [searched]; Avellaneda and Stoikov (Quantitative Finance 2008) | The models in their original form | `src.roll-1984`, `src.kyle-1985`, `src.glosten-milgrom-1985`, `src.almgren-chriss`, `src.avellaneda-stoikov-2008` |
| Stretch | Hasbrouck, *Empirical Market Microstructure* (OUP 2007); Bouchaud, Bonart, Donier and Gould, *Trades, Quotes and Prices* (CUP 2018); Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (CUP 2015) | Econometrics of microstructure; order-flow facts; execution and market making as control problems | `src.hasbrouck-emm`, `src.bouchaud-tqp`, `src.cartea-ahft` |

**2.0e Computer systems, concurrency and performance (P13, 150 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Bryant and O'Hallaron, *Computer Systems: A Programmer's Perspective*, 3rd ed (Pearson 2015) ch. 2, 3, 5, 6, 8, 9, 11, 12 | Representation, machine code, optimisation, memory hierarchy, processes, virtual memory, networking, concurrency | `src.csapp-3e` |
| Free alternative | Arpaci-Dusseau and Arpaci-Dusseau, *Operating Systems: Three Easy Pieces*, version 1.10 (free PDF and chapters) [searched] | Processes, virtual memory, concurrency | `src.ostep` † |
| Lectures | CMU 15-213 Introduction to Computer Systems (recorded lectures; labs public on the book's site); MIT 6.172 Performance Engineering of Software Systems (Fall 2018) [searched] | Lecture parallels | `src.cmu-15213`, `src.mit-6172` |
| Problems | The CS:APP labs (data, bomb, attack, cache, shell, malloc, proxy) and each chapter's practice problems with solutions | Homework and exit | `src.cmu-15213` |
| Spine (concurrency) | Williams, *C++ Concurrency in Action*, 2nd ed (Manning 2019) ch. 2 to 5, 7 | Threads, sharing, synchronisation, memory model, lock-free structures | `src.williams-concurrency-2e` |
| Stretch | Kurose and Ross, *Computer Networking: A Top-Down Approach*, 9th ed (Pearson 2025) [searched] ch. 1 to 3, or Beej's Guide to Network Programming (free); Drepper, "What Every Programmer Should Know About Memory" (2007); Carl Cook, "When a Microsecond Is an Eternity" (CppCon 2017 talk); Ghosh, *Building Low Latency Applications with C++* (Packt, July 2023) [searched] | Networking; memory; trading-system practice | `src.kurose-ross-9e` †, `src.beej-network`, `src.drepper-memory`, `src.cook-cppcon-2017`, `src.ghosh-low-latency` |

**2.1 Machine learning (200 h, +20 h P9, +10 h P10)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | James, Witten, Hastie, Tibshirani and Taylor, *An Introduction to Statistical Learning with Applications in Python* (Springer 2023, free) ch. 2 to 10, 12, 13 | Whole cover list, with Python labs | `src.islp-2023` |
| Lectures | Stanford CS229 Machine Learning (Ng's Autumn 2018 lectures on YouTube [searched]; current lecture notes) | The mathematical parallel | `src.stanford-cs229` |
| Lectures (alternative) | MIT 6.036 Introduction to Machine Learning (Fall 2020; free on the Open Learning Library with auto-checked exercises) [searched] | A gentler parallel with checkable exercises | `src.mit-6036-2020` † |
| Problems | ISLP conceptual and applied exercises; CS229 problem sets (public; solutions [unverified]) | Homework | (as above) |
| Code | Géron, *Hands-On Machine Learning with Scikit-Learn and PyTorch* (O'Reilly, October 2025) | The curriculum's code companion | `src.geron-2025` |
| Theory | Hastie, Tibshirani and Friedman, *The Elements of Statistical Learning*, 2nd ed (Springer 2009, free) ch. 3, 7, 10, 15 | Linear methods, model assessment, boosting, random forests | `src.esl-2e` |
| Finance | López de Prado, *Advances in Financial Machine Learning* (Wiley 2018) ch. 3, 4, 7, 8 | Labelling, sample weights, purged cross-validation, feature importance | `src.afml-2018` |
| Spine (P9) | MacKay, *Information Theory, Inference, and Learning Algorithms* (CUP 2003, free) ch. 1, 2, 4, 5; his recorded Cambridge lectures | Entropy, coding, inference | `src.mackay-itila` |
| Stretch (P9) | Cover and Thomas, *Elements of Information Theory*, 2nd ed (Wiley 2006) ch. 2, 5, 6, 16 | Entropy; coding; gambling; portfolios | `src.cover-thomas-2e` |
| Spine (P10) | MIT 18.S096 Matrix Calculus for Machine Learning and Beyond (IAP 2023, Edelman and Johnson; videos, notes, problem sets with solutions) [searched]; Deisenroth, Faisal and Ong ch. 5 | Matrix gradients, Jacobians, reverse mode | `src.mit-matrix-calculus-2023`, `src.mml` † |

**2.1x ML research track (P14, 380 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine (deep learning) | Prince, *Understanding Deep Learning* (MIT Press 2023, free PDF, CC BY-NC-ND) [searched] ch. 1 to 12, 18 | Networks, losses, fitting, gradients, regularisation, CNNs, ResNets, transformers, diffusion | `src.prince-udl` |
| Lectures | MIT 6.7960 Deep Learning (Fall 2024; lectures, problem sets with solutions) [searched] | Lecture parallels | `src.mit-67960-2024` |
| Problems | Stanford CS231n assignments (Spring 2025 starter code, notes and lecture videos public) [searched]; 6.7960 problem sets | Build-from-scratch drills | `src.stanford-cs231n` |
| Code companion | Karpathy, *Neural Networks: Zero to Hero* (video series; not a university course) | Autodiff and a GPT built from scratch | `src.karpathy-zero-to-hero` |
| Spine (language models) | Stanford CS336 Language Modeling from Scratch (Spring 2025; the Spring 2026 offering is also public) [searched]: five assignments on tokenisation and the transformer, systems (FlashAttention2 in Triton), scaling laws, data, and alignment by reinforcement learning | Tokenisation, transformers, systems, scaling, data, alignment. Pin one offering per lesson; the assignments change between years | `src.stanford-cs336-2025` |
| Stretch (language models) | Austin et al., "How to Scale Your Model" (Google DeepMind 2025, free online); Vaswani et al., "Attention Is All You Need" (NeurIPS 2017); Kaplan et al., "Scaling Laws for Neural Language Models" (2020); Hoffmann et al., "Training Compute-Optimal Large Language Models" (2022) | Parallelism and memory; the core papers | `src.scaling-book-2025`, `src.vaswani-2017`, `src.kaplan-2020`, `src.hoffmann-2022` |
| Spine (theory) | Shalev-Shwartz and Ben-David, *Understanding Machine Learning* (CUP 2014, free) ch. 2 to 7, 12 to 14 | PAC, VC dimension, convex learning, SGD | `src.ssbd-uml` |
| Stretch (theory) | Bach, *Learning Theory from First Principles* (MIT Press 2024); Hardt and Recht, *Patterns, Predictions, and Actions* (Princeton 2022, free) | Modern theory; datasets and benchmarks | `src.bach-ltfp`, `src.hardt-recht-ppa` |
| Spine (RL) | Sutton and Barto, *Reinforcement Learning: An Introduction*, 2nd ed (MIT Press 2018, free) ch. 2 to 6, 9, 13 | Bandits to policy gradients | `src.sutton-barto-2e` |
| Lectures (RL) | David Silver, UCL reinforcement learning course (2015, recorded); Berkeley CS285 Deep Reinforcement Learning (Levine, recorded) | Lecture parallels | `src.silver-ucl-rl`, `src.berkeley-cs285` |
| Stretch | Bishop and Bishop, *Deep Learning: Foundations and Concepts* (Springer 2024) [searched] | A second, more probabilistic treatment | `src.bishop-dl-2024` |

**2.2 Time series (60 h; 75 h on the researcher track)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Hyndman, Athanasopoulos and co-authors, *Forecasting: Principles and Practice, the Pythonic Way* (OTexts, free) | Graphics, decomposition, the forecaster's toolbox, exponential smoothing, ARIMA (structure follows FPP3 [unverified for the Python edition]) | `src.fpp-python` |
| Spine (finance) | Tsay, *Analysis of Financial Time Series*, 3rd ed (Wiley 2010) ch. 1 to 3, 8 | Returns, linear models, volatility models, multivariate series and cointegration | `src.tsay-afts-3e` |
| Lectures | MIT 14.384 Time Series Analysis (Fall 2013, Mikusheva; lecture notes and five problem sets) [searched] | Theory parallel | `src.mit-14384` |
| Problems | Tsay's exercises with the author's datasets | Homework | `src.tsay-afts-3e` |
| Papers | Engle, "GARCH 101" (Journal of Economic Perspectives 2001); Cont, "Empirical Properties of Asset Returns: Stylized Facts and Statistical Issues" (Quantitative Finance 2001); Roll (JF 1984); Kupiec, "Techniques for Verifying the Accuracy of Risk Measurement Models" (Journal of Derivatives 1995); Andersen and Bollerslev, "Answering the Skeptics: Yes, Standard Volatility Models Do Provide Accurate Forecasts" (International Economic Review 1998); Granger and Newbold, "Spurious Regressions in Econometrics" (Journal of Econometrics 1974); Engle and Granger, "Co-integration and Error Correction" (Econometrica 1987); Gatev, Goetzmann and Rouwenhorst (RFS 2006); Hyndman and Koehler, "Another Look at Measures of Forecast Accuracy" (International Journal of Forecasting 2006); Newey and West (Econometrica 1987) | The papers `stage1-statistics-ts.md` cites, one per lesson that uses it | `src.engle-2001-garch101` †, `src.cont-2001` †, `src.roll-1984`, `src.kupiec-1995` †, `src.andersen-bollerslev-1998` †, `src.granger-newbold-1974` †, `src.engle-granger-1987` †, `src.ggr-2006`, `src.hyndman-koehler-2006` †, `src.newey-west-1987` |
| Stretch | Hamilton, *Time Series Analysis* (Princeton 1994) ch. 3, 17, 19, 21; for the P11 extension ch. 11 (VAR) and 13 (Kalman filter); Durbin and Koopman, *Time Series Analysis by State Space Methods*, 2nd ed (OUP 2012) | Theory reference | `src.hamilton-tsa`, `src.durbin-koopman-2e` |

**2.2b Financial econometrics and empirical asset pricing (P11, 80 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Bali, Engle and Murray, *Empirical Asset Pricing: The Cross Section of Stock Returns* (Wiley 2016) part I | Sorts, Fama-MacBeth, Newey-West, the standard anomaly variables | `src.bali-engle-murray` |
| Reference | Campbell, Lo and MacKinlay, *The Econometrics of Financial Markets* (Princeton 1997) ch. 2, 4 to 6 | Predictability, event studies, CAPM and multifactor tests | `src.clm-1997` |
| Problems | Wooldridge, *Introductory Econometrics: A Modern Approach*, 8th ed (Cengage 2025) [searched for edition] computer exercises; datasets in the `wooldridge` Python package [unverified: not in Pyodide, so data are loaded as CSV] | Heteroskedasticity, time-series regression, panels, instruments | `src.wooldridge-8e` |
| Papers | Fama and MacBeth (JPE 1973); Newey and West (Econometrica 1987); Fama and French (JFE 1993, already in 3.1); Gibbons, Ross and Shanken (Econometrica 1989) | The methods in their original form | `src.fama-macbeth-1973`, `src.newey-west-1987`, `src.grs-1989` |
| Stretch | Cochrane, *Asset Pricing*, revised ed (Princeton 2005) ch. 10 to 12, with his free online class (videos, quizzes, problem sets and exams; moved from Coursera to Canvas) [searched] | GMM and factor-model tests | `src.cochrane-ap` |

**2.2c Research method and statistical honesty (P1, 35 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | López de Prado, *Advances in Financial Machine Learning* (Wiley 2018) ch. 11 to 14 | Dangers of backtesting, cross-validated backtests, backtest statistics | `src.afml-2018` |
| Checklist | Arnott, Harvey and Markowitz, "A Backtesting Protocol in the Era of Machine Learning" (Journal of Financial Data Science 1(1), 2019) [searched] | The protocol the audit exit is scored against | `src.arnott-harvey-markowitz-2019` † |
| Papers (finance) | Harvey, Liu and Zhu, "... and the Cross-Section of Expected Returns" (RFS 2016); Bailey and López de Prado, "The Deflated Sharpe Ratio" (JPM 2014); Bailey, Borwein, López de Prado and Zhu, "The Probability of Backtest Overfitting" (Journal of Computational Finance 20(4), 2017) [searched]; Bailey, Borwein, López de Prado and Zhu, "Pseudo-Mathematics and Financial Charlatanism" (Notices of the AMS 2014); White, "A Reality Check for Data Snooping" (Econometrica 2000); Lo, "The Statistics of Sharpe Ratios" (FAJ 2002); McLean and Pontiff (JF 2016); Hou, Xue and Zhang, "Replicating Anomalies" (RFS 2020); Jensen, Kelly and Pedersen, "Is There a Replication Crisis in Finance?" (JF 2023) | Reading pack | `src.hlz-2016`, `src.dsr-2014`, `src.pbo`, `src.bailey-2014-charlatanism` †, `src.white-2000`, `src.lo-2002`, `src.mclean-pontiff-2016`, `src.hxz-2020`, `src.jkp-2023` |
| Papers (science and ML) | Ioannidis, "Why Most Published Research Findings Are False" (PLoS Medicine 2005); Simmons, Nelson and Simonsohn, "False-Positive Psychology" (Psychological Science 2011); Gelman and Loken, "The Statistical Crisis in Science" (American Scientist 2014); Henderson et al., "Deep Reinforcement Learning That Matters" (AAAI 2018); Recht, Roelofs, Schmidt and Shankar, "Do ImageNet Classifiers Generalize to ImageNet?" (ICML 2019); Dodge et al., "Show Your Work" (EMNLP 2019); Kapoor and Narayanan, "Leakage and the Reproducibility Crisis in Machine-Learning-Based Science" (Patterns 2023) | Reading pack | `src.ioannidis-2005`, `src.simmons-2011` †, `src.gelman-loken-2014`, `src.henderson-2018`, `src.recht-2019` †, `src.dodge-2019`, `src.kapoor-narayanan-2023` |
| Stretch | Reinhart, *Statistics Done Wrong* (No Starch 2015) | Short, readable catalogue of errors | `src.reinhart-sdw` |

**2.3 Projects (400 h)**

| Project | Resources | Ids |
|---|---|---|
| 1 Backtesting engine | AFML ch. 11 to 14; Chan, *Quantitative Trading*, 2nd ed (Wiley 2021) for the practitioner's checklist; the P1 reading pack | `src.afml-2018`, `src.chan-qt-2e` |
| 2 Alpha signal research | Grinold and Kahn ch. 6 and 14; Isichenko, *Quantitative Portfolio Management* (Wiley 2021); Jegadeesh and Titman (JF 1993); Kakushadze, "101 Formulaic Alphas" (Wilmott 2016); data from Kenneth French's data library and Chen and Zimmermann's Open Source Asset Pricing | `src.grinold-kahn-2e`, `src.isichenko-qpm`, `src.jt-1993`, `src.kakushadze-101`, `src.french-library`, `src.osap` |
| 3 Options analytics | Hull ch. 20 (Volatility Smiles and Volatility Surfaces) and 21 (Basic Numerical Procedures) [searched]; Gatheral, *The Volatility Surface* (Wiley 2006) ch. 1 to 3; Glasserman ch. 1 to 4; Sinclair, *Volatility Trading*, 2nd ed (Wiley 2013) | `src.hull-ofod-11e`, `src.gatheral-vs`, `src.glasserman-mc`, `src.sinclair-vt-2e` |
| 4 Market data handler | Kleppmann and Riccomini, *Designing Data-Intensive Applications*, 2nd ed (O'Reilly 2026) [searched] chapters on storage and stream processing; Nasdaq TotalView-ITCH 5.0 specification; CS:APP ch. 11 and 12 | `src.ddia-2e`, `src.itch-50`, `src.csapp-3e` |
| 5 Trading bot | As projects 1 and 4 | |

**2.4 Contests (140 h; 60 h proposed outside the developer track)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Codeforces (contests and the EDU section) | The curriculum's pick | `src.codeforces` |
| Problems | CSES Problem Set (free), with Laaksonen, *Competitive Programmer's Handbook* (free) | Graded problem list | `src.cses`, `src.laaksonen-cph` |
| Guide | USACO Guide (free) | Topic order by level | `src.usaco-guide` |
| Stretch | Halim and Halim, *Competitive Programming 4* (2020); Project Euler; Kaggle; IMC Prosperity | By track, as the curriculum says | `src.halim-cp4`, `src.project-euler` |

### Stage 3

**3.1 Research papers (150 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | The curriculum's five: Jegadeesh and Titman (JF 1993); Fama and French (JFE 1993); Gatev, Goetzmann and Rouwenhorst (RFS 2006); Avellaneda and Stoikov (QF 2008); Harvey, Liu and Zhu (RFS 2016) | Replicate before reading widely | `src.jt-1993`, `src.ff-1993`, `src.ggr-2006`, `src.avellaneda-stoikov-2008`, `src.hlz-2016` |
| Method | Bali, Engle and Murray (2016); the P1 reading pack | How to replicate honestly | `src.bali-engle-murray` |
| Extension | Gu, Kelly and Xiu, "Empirical Asset Pricing via Machine Learning" (RFS 2020) | Where 2.1 meets 3.1 | `src.gkx-2020` |
| Data | Kenneth French's data library; Open Source Asset Pricing (Chen and Zimmermann) | Free inputs for replication | `src.french-library`, `src.osap` |

**3.2 Stochastic calculus (P16; 150 h proposed)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Shreve, *Stochastic Calculus for Finance I: The Binomial Asset Pricing Model* and *II: Continuous-Time Models* (Springer 2004): I ch. 1 to 6; II ch. 1 to 6, then 9 and 10 | The curriculum's pick | `src.shreve-1`, `src.shreve-2` |
| First read | Baxter and Rennie, *Financial Calculus* (CUP 1996) | Intuition before Shreve II | `src.baxter-rennie` |
| Lectures | MIT 18.S096 Fall 2013 lectures on stochastic processes, Itô calculus and Black-Scholes [searched for topics]; MIT 15.070J Advanced Stochastic Processes (Fall 2013) | Lecture parallels | `src.mit-18s096-2013`, `src.mit-15070j` |
| Problems | Chin, Nel and Ólafsson, *Problems and Solutions in Mathematical Finance*, vol. 1: Stochastic Calculus (Wiley 2014; general probability, the Wiener process, SDEs, change of measure, the Poisson process, all with solutions) [searched]; Cambridge Part II Stochastic Financial Models example sheets (2025-26 posted) [searched] | Solved problems; problem types | `src.chin-nel-olafsson-1`, `src.cam-sfm` |
| Stretch | Björk, *Arbitrage Theory in Continuous Time*, 4th ed (OUP 2019); Øksendal, *Stochastic Differential Equations*, 6th ed (Springer 2003) | Second treatment; SDE theory | `src.bjork-4e`, `src.oksendal-6e` |

**P16 prerequisites (real analysis 120 h, measure-theoretic probability 100 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine (analysis) | Abbott, *Understanding Analysis*, 2nd ed (Springer 2015) ch. 1 to 7 | Reals, sequences, series, continuity, derivatives, uniform convergence, Riemann integral | `src.abbott-ua-2e` |
| Lectures (analysis) | MIT 18.100A Real Analysis (Fall 2020, Rodriguez; lecture videos, notes, problem sets and exams) [searched] | Lecture parallels and problems | `src.mit-18100a-2020` |
| Spine (measure) | Williams, *Probability with Martingales* (CUP 1991) | Measure, integration, conditional expectation, martingales | `src.williams-martingales` |
| Alternative | Rosenthal, *A First Look at Rigorous Probability Theory*, 2nd ed (World Scientific 2006) | Gentler measure-theoretic route | `src.rosenthal-2e` |
| Lectures (measure) | MIT 18.175 Theory of Probability (Spring 2014, Sheffield; on Durrett's *Probability: Theory and Examples*, 4th ed; seven problem sets) [searched] | Lecture parallels; graduate level, so selected lectures only | `src.mit-18175` |

**3.3 Interview preparation (250 h)**

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine, in the curriculum's order | Mosteller, *Fifty Challenging Problems in Probability* (Dover 1987); Zhou, *A Practical Guide to Quantitative Finance Interviews* (2008) ch. 2 (brain teasers), 4 (probability), 5 (stochastic processes and stochastic calculus), 6 (finance), 7 (algorithms and numerical methods) [recalled chapter titles]; Crack, *Heard on the Street*, 24th ed (2023) [searched]; Joshi, Denson and Downes, *Quant Job Interview Questions and Answers*, 2nd ed (2013) | The books, easiest first | `src.mosteller-50`, `src.zhou-2008`, `src.crack-hots`, `src.joshi-qjiqa-2e` |
| Added | Stefanica, Radoičić and Wang, *150 Most Frequently Asked Questions on Quant Interviews*, 3rd ed (FE Press; over 200 questions, now with statistics and machine learning) [searched; year unverified]; Winkler, *Mathematical Puzzles: A Connoisseur's Collection* (A K Peters 2004); Jane Street, *Probability and Markets* (free) | Breadth; puzzles; the firm's own guide | `src.stefanica-150`, `src.winkler-puzzles`, `src.js-prob-markets` |
| Problems with solutions | Blitzstein and Hwang exercises with posted solutions; *One Thousand Exercises in Probability* | Cold-solve practice | `src.blitzstein-hwang-2019`, `src.grimmett-stirzaker-1000` |

### Bayesian computation (P15, 40 h, elective)

| Role | Resource | Use | Id |
|---|---|---|---|
| Spine | Gelman, Carlin, Stern, Dunson, Vehtari and Rubin, *Bayesian Data Analysis*, 3rd ed (CRC 2013, free PDF from the authors) ch. 1 to 5, 10 to 12 | Models, hierarchical models, computation, MCMC | `src.bda3` |
| Lectures | McElreath, *Statistical Rethinking* (recorded lecture series) with the book, 2nd ed (CRC 2020) | Lecture parallels and problems | `src.mcelreath-sr-2e` |
| Problems | McElreath's end-of-chapter problems; Blitzstein and Hwang ch. 12 exercises | Homework | (as above) |

---

## 7. Decisions for the owner

1. **Which proposals.** Accept, trim or reject each of P1 to P16 and O1, or accept the minimum set (P1 to P4 with O1, +170 h net). Recommended: priorities 1 and 2 now (section 4.1), priority 3 as the owner sees fit.
2. **Whether the curriculum files' first passes count.** Revision 2 cuts 105 hours from ten proposals because the item files now teach their first passes inside existing hours (section 8.2). Recommended: accept the cuts; the proposals then add depth, not repetition. If the owner would rather keep those topics as separate courses, revision 1's hours apply.
3. **A fourth track.** Whether to add the ML research track (P14, 380 h). Recommended: yes, since ML-lab thinking is a stated goal and 2.1 alone does not reach it.
4. **Stochastic calculus.** Whether to count 3.2 and make it the P16 add-on with stated prerequisites (real analysis and measure, 220 h before Shreve volume II). Recommended: yes; the cost should be visible to the learner who chooses it.
5. **Exit tests.** Whether to adopt the changes in section 4.4 (proof portfolio, differential-equations exam, P1 checklist on results notes, Zhou ch. 5).
6. **Books that cost money.** Paid spines in the proposals: Velleman, Süli and Mayers, Trefethen and Bau, Glasserman, Luenberger, Bali, Engle and Murray, Bryant and O'Hallaron (OSTEP is a free alternative for part of it), Williams (concurrency), Durrett (*Essentials*), Abbott, Williams (martingales), Shreve. Free routes exist for P4 (Boyd and Vandenberghe), P9 (MacKay), P10 (MIT 18.S096, Deisenroth, Faisal and Ong), P14 (all four spines), P15 (BDA3), P7 (Lehman, Leighton and Meyer, Hammack) and P16's analysis (MIT 18.100A notes) [recalled]. Lessons are written from knowledge either way; the question is what the learner is told to buy.
7. **Hours ceiling.** Whether a 3,565 to 3,820 hour path (4.6 to 4.9 years at 15 hours a week) is acceptable, or the minimum set's 3,270 is the cap.

---

## 8. Reconciliation with the papers written after revision 1

### 8.1 Ids

**Duplicates mapped.** `sources.yaml` does not exist yet, so each duplicate is resolved now and the curriculum files' request tables read as below.

| Requested id | Requested by | Canonical id | Reason |
|---|---|---|---|
| `src.esl` | `stage1-linear-algebra.md` | `src.esl-2e` | Revision 1 id; pins the edition |
| `src.lo-2002-sharpe` | `stage1-statistics-ts.md` | `src.lo-2002` | Revision 1 id |
| `src.bailey-lopezdeprado-2014` | `stage1-statistics-ts.md` | `src.dsr-2014` | Revision 1 id |
| `src.harvey-liu-zhu-2016` | `stage1-statistics-ts.md` | `src.hlz-2016` | Revision 1 id; cited by 3.1 |
| `src.gatev-2006` | `stage1-statistics-ts.md` | `src.ggr-2006` | Revision 1 id; cited by 3.1 |
| `src.casi` | `stage1-statistics-ts.md` | `src.efron-hastie-casi` | Revision 1 id |
| `src.islr-2e` | `stage1-statistics-ts.md` | `src.islp-2023` | The curriculum names the Python edition for 2.1; its chapter 3 covers the same regression material with Python labs, so one book serves 1.6 and 2.1 [recalled] |

**Already present.** `src.roll-1984`, `src.newey-west-1987`, `src.mit-18s096-2013` and `src.mit-1805`, which `stage1-statistics-ts.md` asked to add, were in revision 1.

**Renamed.** `src.kurose-ross-8e` becomes `src.kurose-ross-9e`: the 9th edition appeared in June 2025 [searched], and no other file cites the old id.

**New in revision 2 (51 ids).**

| Origin | Ids |
|---|---|
| `stage1-linear-algebra.md` request (10) | `src.mml`, `src.hefferon`, `src.strang-ftla-1993`, `src.litterman-scheinkman-1991`, `src.laloux-1999`, `src.ledoit-wolf-2004` ("Honey, I Shrunk the Sample Covariance Matrix", the paper lesson 95 cites, not the same authors' 2004 JMVA estimator paper), `src.avellaneda-lee-2010`, `src.bryan-leise-2006`, `src.moler-vanloan-2003`, `src.vonluxburg-2007` |
| `stage1-statistics-ts.md` request (13) | `src.benjamini-hochberg-1995`, `src.white-1980`, `src.anscombe-1973`, `src.brown-cai-dasgupta-2001`, `src.efron-morris-1977`, `src.wasserstein-lazar-2016`, `src.engle-2001-garch101`, `src.cont-2001`, `src.kupiec-1995`, `src.andersen-bollerslev-1998`, `src.granger-newbold-1974`, `src.engle-granger-1987`, `src.hyndman-koehler-2006` |
| Used in the curriculum files' text or named by `curriculum.md`, without a request (12) | `src.openstax-prealgebra-2e`, `src.openstax-elementary-algebra-2e`, `src.openstax-intermediate-algebra-2e`, `src.openstax-college-algebra-2e`, `src.python-docs-float`, `src.mat-papers`, `src.underground-maths`, `src.isaac-maths`, `src.shotts-tlcl`, `src.vanderplas-pdsh-2e`, `src.norris-markov`, `src.evans-rosenthal-2e` |
| Revision 2 searches and gaps (16) | `src.missing-semester-2026`, `src.durrett-essentials-3e`, `src.mit-6262-2011`, `src.mit-18600-2019`, `src.ross-first-course-10e`, `src.stanford-stats200`, `src.stanford-cs106b`, `src.roberts-pac`, `src.mit-15433-2003`, `src.mit-6036-2020`, `src.ostep`, `src.arnott-harvey-markowitz-2019`, `src.wilmott-howison-dewynne`, `src.recht-2019`, `src.simmons-2011`, `src.bailey-2014-charlatanism` |

### 8.2 Hours already absorbed by the curriculum files

| Proposal | Rev. 1 | What the files now teach inside existing hours | Rev. 2 | What the proposal still adds |
|---|---|---|---|---|
| P1 | 40 | FDR, forking paths, backtest overfitting (1.6 lessons 40 to 42); the Sharpe ratio's standard error (1.6 lesson 19); look-ahead and point-in-time joins (1.1); pairs without look-ahead (2.2 lesson 42) | 35 | The audit, the protocol, replication and the results note |
| P2 | +40 | Poisson processes with merging and thinning, the inspection paradox, patterns as chains, reflection, ballot, Catalan, a Brownian preview, and level Z4 on martingales, optional stopping, ruin, Wald and the pattern martingale (`stage1-probability.md`) | +15 | Continuous-time chains, Brownian motion and its martingales, green-book chapter 5 volume |
| P5 | +40 | Fisher information, Cramér-Rao, MLE asymptotics, the delta method, the bootstrap, permutation tests, FDR, logistic regression, resistant estimators (1.6, decision S5); linear shrinkage (1.4 lesson 95) | +25 | Dependent-data inference, GLMs beyond logistic, heavy tails, covariance estimation |
| P6 | 80 | Minimum variance (1.3 lesson 128); portfolio variance (1.5 lesson 96); VaR backtesting and volatility targeting (2.2 lessons 30 and 31) | 75 | Fixed income, CAPM and factor models, the fundamental law, risk measures |
| P7 | 90 | Logic, contrapositive, contradiction, induction (0.3 levels R1 and R2); pigeonhole (0.3 lesson 104); long-form proofs throughout 1.3, 1.5 and 1.6 | 70 | Proof as a subject: sets, functions, bijections, number theory, graphs, invariants |
| P8 | 50 | First-order equations: slope fields, separable, Euler, integrating factors (1.3 level I6) | 45 | Second order, systems, stability, Runge-Kutta, the heat equation |
| P9 | +25 | Maximum entropy (1.3 lesson 128); cross-entropy as likelihood (1.6 lesson 65); Kelly preview (1.5 Z6) | +20 | Entropy, KL, mutual information, coding, Kelly derived |
| P10 | +20 | Gradients of quadratic forms, least squares and ridge by calculus (1.4 lesson 82); Eckart-Young (86); gradient descent and conditioning (96); finite differences and dual numbers (1.3 lessons 27, 28); backpropagation on a graph (1.3 lesson 116) | +10 | Jacobians, matrix chain rule, softmax and logistic gradients, two-layer backpropagation in matrix form; moved to 2.1 |
| P11 (2.2 extension) | +20 | VAR, Granger causality and Johansen as a preview (2.2 lesson 41); HC and HAC errors (1.6 lessons 55, 56) | +15 | State space and the Kalman filter, regime switching, VAR estimation |
| P15 | 50 | Metropolis with detailed balance (1.5 lesson 134); course BY (1.6: conjugate updating, empirical Bayes, Bayesian ridge, Bayes factors, Metropolis) | 40 | Hierarchical models, Gibbs, HMC, diagnostics, variational inference |
| **Total** | | | **-105** | |

P3, P4, P12, P13, P14 and P16 are unchanged: the files touch them only in single preview lessons (section 3), which the proposals' hours already assumed.

### 8.3 Spine, slot and licence changes

| Item | Revision 1 | Revision 2 | Why |
|---|---|---|---|
| 1.3 spine | Stewart, 9th ed; OpenStax as free alternative | OpenStax Calculus vols 1 to 3; Stewart as the alternative | `stage1-calculus.md` decision 2; both are the curriculum's named options; OpenStax is free on every device |
| OpenStax Calculus licence | CC BY (wrong) | CC BY-NC-SA 4.0 [searched]: `problem-inspired` only | Search of the book's licence statement |
| P2 spine | Grimmett and Stirzaker ch. 12 | Durrett, *Essentials of Stochastic Processes*, 3rd ed, ch. 4 and 5; Grimmett and Stirzaker ch. 13 for Brownian motion, ch. 12 and the *Thousand Exercises* as problems | 1.5 now holds the discrete material; what is left is continuous time at an undergraduate pitch |
| P2 lectures | MIT 18.445 (described as Poisson, martingales, Brownian motion) | MIT 6.262 (Spring 2011) lectures; 18.445 for solved homework on Markov chains and martingales | 18.445's syllabus is Markov chains, random walks, martingales and Galton-Watson trees [searched] |
| P10 slot | Extension of 1.4 | Opening of 2.1, beside P9 | 1.4 holds the first half; `stage1-linear-algebra.md` places the rest with 2.1 |
| 0.4 and 1.2 lectures | Missing Semester 2020 | 2026 edition, with 2020 for the dropped lectures | The 2026 course exists, with new lectures on packaging, agentic coding and code quality [searched] |
| P13 networking | Kurose and Ross, 8th ed (2020) | 9th ed (2025) | [searched] |

### 8.4 Follow-ups for other files

These are notes for the owners of other papers; this paper edits none of them.

| File | Note |
|---|---|
| `content-format.md` 9.4 | "CC BY (OpenStax) yes" holds for Precalculus and the algebra books, not the Calculus volumes, which are CC BY-NC-SA 4.0 and so `problem-inspired` only |
| `stage1-calculus.md` open item 5 | Answered: CC BY-NC-SA 4.0 [searched] |
| `stage1-calculus.md` decision 7, open item 7 | P8 is now 45 h, second order and systems only |
| `stage1-linear-algebra.md` decision 6 | P10's remainder is +10 h at the opening of 2.1 |
| `stage1-linear-algebra.md` request table | `src.esl` reads `src.esl-2e` |
| `stage1-probability.md` open item 6 | P2 is +15 h with Durrett as spine; Z4's stretch reading (Grimmett and Stirzaker ch. 12) is unchanged |
| `stage1-probability.md` open items 2 and 5 | Item 5 is answered by `spikes/README.md` (WebAssembly and Pyodide run in the Artifact). Item 2: practice finals sit on the Stat 110 site's final-review page [searched]; whether each has full solutions is still [unverified] |
| `stage1-statistics-ts.md` S1, S5 and request table | ISLR 2nd ed ch. 3 reads ISLP ch. 3 (`src.islp-2023`); P5 is +25 h with the scope in section 8.2; six requested ids map to revision 1 ids (section 8.1) |
| `stage1-statistics-ts.md` decision 5 | "Pyodide cannot run in the Artifact" is superseded by `spikes/README.md`, as `content-format.md` revision 2 already records; NumPy-only `web` drills become `pyodide-core` candidates |
| `assessment.md` 6.5 and 8.7 | Path lengths with every proposal are 3,565 to 3,820 h (3,860 with P15 on the ML research track); the Trader track with every proposal is 3,565 h, 238 weeks at 15 h |
| `arch-decision.md` 6.3.3 | cvxpy-base, Clarabel and HiGHS are in the Pyodide set but in no load group; P4 needs them in one (section 5.3) |
| Widget catalogues | `forking-paths`, `float-inspector`, `shrinkage-lab`, `var-backtest` and `hac-lab` may be needed by in-budget lessons whatever the owner decides (section 5.1) |

---

## Sources

Web searches run on 6 October 2026 for revisions 1 and 2. Direct fetches of the Cambridge, Oxford, CMU and Imperial pages were blocked by this environment's proxy (section 1).

**Programmes (revision 1).**

- [Cambridge Part IB lecture list, 2025-26](https://www.maths.cam.ac.uk/undergrad/files/lecturelist/current/Part_IB.pdf); [Lecture lists 2025-26](https://www.maths.cam.ac.uk/undergrad/node/35); [Part II lecture list 2023-24](https://www.maths.cam.ac.uk/undergrad/files/lecturelist/2023-24/Part_II.pdf); [Stochastic Financial Models, DPMMS](https://www.dpmms.cam.ac.uk/study/II/FinancialModels/)
- [Oxford MSc Mathematical and Computational Finance, 2025-26 handbook](https://courses.maths.ox.ac.uk/mod/book/view.php?id=65619); [QuantNet: Oxford MSc MCF](https://quantnet.com/resources/44/); [Oxford B8.2 Continuous Martingales and Stochastic Calculus](https://courses.maths.ox.ac.uk/course/info.php?id=6202)
- [Imperial MSc Mathematics and Finance module structure 2026-27](https://www.imperial.ac.uk/media/imperial-college/faculty-of-natural-sciences/department-of-mathematics/math-finance/MSc-MF-Module-Structure-and-Guide-2026-27_v3.pdf)
- [CMU MSCF curriculum](https://www.cmu.edu/mscf/academics/curriculum); [CMU Computational Finance minor](https://www.math.cmu.edu/~bscf/minor.html); [CMU 21-127 syllabus](https://www.math.cmu.edu/users/wgunther/127m12/syllabus.pdf)
- [Baruch MFE curriculum](https://mfe.baruch.cuny.edu/curriculum/); [Baruch Pre-MFE Program](https://mfe.baruch.cuny.edu/pre-mfe-program/); [QuantNet: 2025-2026 Pre-MFE Program](https://quantnet.com/threads/the-2025-2026-pre-mfe-program-at-baruch-college.62590/post-354636)
- [Princeton ORFE undergraduate courses](https://orfe.princeton.edu/undergraduate/courses); [Princeton ORFE academic unit](https://ua.princeton.edu/academic-units/department-operations-research-and-financial-engineering)
- [MIT 18.S096 Fall 2013 syllabus](https://ocw.mit.edu/courses/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/pages/syllabus); [MIT 18.065 Spring 2018](https://ocw.mit.edu/courses/18-065-matrix-methods-in-data-analysis-signal-processing-and-machine-learning-spring-2018/pages/instructor-insights); [MIT 18.650 Fall 2016 syllabus](https://ocw.mit.edu/courses/18-650-statistics-for-applications-fall-2016/pages/syllabus); [MIT 18.100A Fall 2020](https://ocw.mit.edu/courses/18-100a-real-analysis-fall-2020); [MIT 18.335J Spring 2019](https://ocw.mit.edu/courses/18-335j-introduction-to-numerical-methods-spring-2019/pages/syllabus/); [MIT 6.7960 Fall 2024](https://ocw.mit.edu/courses/6-7960-deep-learning-fall-2024/); [MIT 6.172 Fall 2018](https://ocw.mit.edu/courses/6-172-performance-engineering-of-software-systems-fall-2018); [MIT 6.006 Spring 2020](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/resources/mit6_006s20_lec1); [MIT 6.046J Spring 2015](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015); [MIT 6.100L Fall 2022](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/lists)
- [Harvard STAT 111](https://qrd.college.harvard.edu/directory/stat-111)
- [Stanford STATS 116 texts](https://web.stanford.edu/class/stats116/texts.html); [STATS 116 replaced by STATS 117 and 118](https://datasciencemajor.stanford.edu/news/stats-116-will-be-replaced-stats-117-and-stats-118); [Stanford MS&E 245A](https://bulletin.stanford.edu/courses/2045041); [Luenberger, Investment Science](https://web.stanford.edu/~luen/investment/); [CS229](https://cs229.stanford.edu); [CS336 bulletin](https://bulletin.stanford.edu/courses/2255541)
- [NYU Courant MS in Mathematics in Finance, academics](https://math-finance.cims.nyu.edu/academics/); [Stern MBA/MS Mathematics in Finance](https://stern.nyu.edu/portal-partners/academic-affairs-advising/dual-degree-students/program-details/mba-ms-mathematics-in-finance)
- [Berkeley MFE curriculum](https://mfe.haas.berkeley.edu/academics/curriculum); [Berkeley Guide: Financial Engineering](https://guide.berkeley.edu/graduate/degree-programs/financial-engineering/)
- [UZH and ETH MSc Quantitative Finance course structure](https://www.msfinance.uzh.ch/en/portrait/coursesstructure.html); [ETH Master Quantitative Finance](https://ethz.ch/en/studies/master/degree-programmes/natural-sciences-and-mathematics/quantitative-finance.html)
- Editions: [Hull 11th edition](https://www.iotafinance.com/en/Book-page-Options-Futures-and-Other-Derivatives-Global-edition-11ed--John-HULL.html); [Wooldridge 8th edition](https://cengage.com/c/new-edition/9780357900161); [Strang ILA 6th edition](https://math.mit.edu/~gs/linearalgebra/ila6/indexila6.html); [Kleppmann and Riccomini, DDIA 2nd edition](https://martin.kleppmann.com/2026/03/24/designing-data-intensive-applications-2e.html); [Bishop and Bishop, Deep Learning](https://link.springer.com/book/10.1007/978-3-031-45468-4); [Prince, Understanding Deep Learning](https://bookshop.org/p/books/understanding-deep-learning-simon-j-d-prince/6bcd27d233004c13?digital=t)

**Programmes and courses (revision 2).**

- [Cambridge Part IA lecture list, current](https://www.maths.cam.ac.uk/undergrad/files/lecturelist/current/Part_IA.pdf) (search summary only; the PDF was blocked)
- [MIT 18.01SC final exam solutions](https://www.ocw.mit.edu/courses/18-01sc-single-variable-calculus-fall-2010/resources/mit18_01scf10_finalsol); [MIT 18.06 Spring 2010 exams](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/exams/); [MIT 18.600 Fall 2019](https://ocw.mit.edu/courses/18-600-probability-and-random-variables-fall-2019/download/); [MIT 18.445 Spring 2015](https://ocw.mit.edu/courses/18-445-introduction-to-stochastic-processes-spring-2015/pages/syllabus); [MIT 6.262 Spring 2011](https://ocw.mit.edu/courses/6-262-discrete-stochastic-processes-spring-2011/download); [MIT 18.175 Spring 2014](https://ocw.mit.edu/courses/18-175-theory-of-probability-spring-2014/pages/syllabus); [MIT 14.384 Fall 2013](https://ocw.mit.edu/courses/14-384-time-series-analysis-fall-2013/pages/syllabus/); [MIT 15.433 Spring 2003](https://ocw.mit.edu/courses/15-433-investments-spring-2003/pages/syllabus/); [MIT 6.036 Fall 2020](https://live.ocw.mit.edu/courses/6-036-introduction-to-machine-learning-fall-2020); [MIT 18.S096 Matrix Calculus, IAP 2023](https://ocw.mit.edu/courses/18-s096-matrix-calculus-for-machine-learning-and-beyond-january-iap-2023/pages/instructor-insights/); [MIT RES.18-009, Fall 2015](https://www.ocw.mit.edu/courses/res-18-009-learn-differential-equations-up-close-with-gilbert-strang-and-cleve-moler-fall-2015/pages/differential-equations-and-linear-algebra); [MIT 6.102 Software Construction](https://web.mit.edu/6.102/www/sp26/general/)
- [Harvard Stat 110 strategic practice](https://stat110.hsites.harvard.edu/strategic-practice-problems); [Stat 110 final review](https://stat110.hsites.harvard.edu/resource/final-review)
- [Stanford CS106B syllabus](https://web.stanford.edu/class/archive/cs/cs106b/cs106b.1262/course/syllabus); [Stanford STATS 200 lectures](https://web.stanford.edu/class/stats200/lectures.html); [CS229 Autumn 2018 lectures](https://www.classcentral.com/course/youtube-stanford-cs229-machine-learning-full-course-taught-by-andrew-ng-autumn-2018-107761); [CS231n 2025 schedule](https://cs231n.stanford.edu/2025/schedule.html); [CS336 Spring 2026 coverage](https://www.besthub.dev/articles/why-stanford-s-free-cs336-llm-course-is-the-ultimate-hands-on-ai-lab-628525936c01)
- [The Missing Semester, 2026 lectures](https://missing.csail.mit.edu/2026); [Cochrane, Asset Pricing online class](https://www.johnhcochrane.com/asset-pricing)

**Books, papers and licences (revision 2).**

- [OpenStax Calculus Volume 1 licence (CC BY-NC-SA 4.0)](https://open.umn.edu/opentextbooks/formats/205); [OpenStax Precalculus 2e preface (CC BY 4.0)](https://openstax.org/books/precalculus-2e/pages/preface)
- [Automate the Boring Stuff, 3rd edition](https://bookshop.org/p/books/automate-the-boring-stuff-with-python-3rd-edition-al-sweigart/07df7b58a1c84fa2); [Grokking Algorithms, 2nd edition](https://bookshop.org/p/books/grokking-algorithms-second-edition-aditya-y-bhargava/c5a7ae7af8d74525); [Market Liquidity, 2nd edition](https://india.oup.com/product/market-liquidity-9780197542064/); [One Thousand Exercises in Probability, 3rd edition](https://www.abebooks.com/9780198847618/Thousand-Exercises-Probability-Third-Edition-0198847610/plp); [Heard on the Street](https://www.goodreads.com/book/show/18323900); [150 Most Frequently Asked Questions, 3rd edition](https://quantnet.com/threads/150-most-frequently-asked-questions-on-quant-interviews-third-edition.59976); [Kurose and Ross, 9th edition](https://www.pearson.com/en-ca/subject-catalog/p/computer-networking-a-top-down-approach/P200000013385/9780135415603); [Tuckman and Serrat, 4th edition](https://www.wiley-vch.de/en/areas-interest/finance-economics-law/fixed-income-securities-978-1-119-83555-4); [Ghosh, Building Low Latency Applications with C++](https://www.oreilly.com/library/view/-/9781837639359/); [Durrett, Essentials of Stochastic Processes, 3rd edition](https://link.springer.com/978-3-319-45613-3); [Chin, Nel and Ólafsson, vol. 1](https://www.wiley-vch.de/en/areas-interest/finance-economics-law/problems-and-solutions-in-mathematical-finance-978-1-119-96583-1); [Operating Systems: Three Easy Pieces](https://research.cs.wisc.edu/wind/OSTEP); [Luenberger, Investment Science, 2nd edition](https://www.oupcanada.com/catalog/9780199740086.html)
- Tables of contents: [Hull 11th edition chapters](https://pearsoned.co.in/web/books/9789392970962_Option-Futures-and-other-Derivatives11e_John-C-Hull.aspx); [Grinold and Kahn, 2nd edition chapters](https://ucema.edu.ar/u/mtd98/Links_interesantes/LibGrinold.htm); [Strang, Differential Equations and Linear Algebra, chapter 8](https://www.ocw.mit.edu/courses/res-18-009-learn-differential-equations-up-close-with-gilbert-strang-and-cleve-moler-fall-2015/pages/differential-equations-and-linear-algebra/fourier-and-laplace-transforms/)
- Papers: [The Probability of Backtest Overfitting](https://www.risk.net/journal-of-computational-finance/2471206/the-probability-of-backtest-overfitting); [Almgren and Chriss, Optimal Execution of Portfolio Transactions](https://www.risk.net/journal-risk/2161150/optimal-execution-portfolio-transactions); [Arnott, Harvey and Markowitz, A Backtesting Protocol](https://papers.ssrn.com/abstract=3275654)
- Runtime: [Packages built in Pyodide](https://pyodide.org/en/0.28.2/usage/packages-in-pyodide.html); the Pyodide 314.0.7 `pyodide-lock.json` read locally [measured]
