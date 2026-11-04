# Prerequisite mapping: `requires` for every course

Mapping agent for `docs/briefs/prereq-gating.md` section 8. Edited fields: `requires` on levels (172 explicit lists) and one top-level `lessonRequires` (coding-int). No other field or byte of any `course.json` changed: `check.mjs` parses each file and the HEAD version and finds them equal once those two fields are removed (key order included). Scripts and the data live in `docs/reports/prereq-mapping-scripts/`: `mapping.txt` (the single source of every list and reason below), `apply.mjs` (text insertion into each `course.json`), `check.mjs` (diff against HEAD, rules, depth, closure), `warnings.mjs`, `gen-report.mjs` (the per-course section), `dump-maps.mjs` and `candidates.mjs` (read every map and brief citation).

## Results

- Validator (`app/`): **0 errors**, 467 warnings, no cycles. The mapping adds 35 warnings, all "reference to a level with no written lesson" (listed below). Nothing else new.
- Routes (`--routes-only --local-cdn ...`), with and without `--mobile`: all passed ("gating  Stage 0 open, puzzles/l7-cards-and-colours locked with its card ... Strict, Open anyway, test-out, old save").
- 279 levels in 76 courses. 172 carry an explicit list; the rest are the first level of a course (open) or take the implicit previous level. Largest direct list: 5 references.
- Longest chain: **34 levels** (counted with every level on the path, the end level included): `number-sense/L1` to `L2`, `equations/L1`, `counting/L1`, `L2`, `counting-chance/L1` to `L3`, `random-vars/L1` to `L3`, `limits-thm/L1` to `L3`, `estimation/L1` to `L3`, `testing/L1`, `regression/L2`, `L3`, `stat-learning/L1`, `L2`, `validation/L1`, `L2`, `fin-ml/L1` to `L3`, `alpha/L1` to `L4`, `momentum-rep/L1` to `L3`. It is the researcher spine (probability, statistics, machine learning, the alpha project, the replication) and is real, not padding. Each level on it is also met by passing its topic exam or stage exit test.

## Rules applied and where I departed from the briefs

- Direct references only, smallest set. Where a course's own level N needs only level N-1 the list is left implicit. Where it needs another course as well, the list names the previous level too, because an explicit list replaces the implicit one.
- Sources used in order: the "Prerequisites" and "Builds on" lines of `docs/briefs/breadth-plan.md` and `interview-plan.md`; per-level "Builds on" lines in each course brief (through `candidates.mjs`, which maps each cited lesson id to its level); `docs/curriculum.md` topic order; lesson titles in each `course.json`. The original Stage 0 and Stage 1 courses have no briefs, so their lists come from lesson titles and topic order (a judgement, flagged for the second reader).
- Pure strand never gates a non-pure course. Four plan lines named a pure course and were changed:
  - `measure-prob/L1`: the plan names `analysis` (all levels). Replaced by `ito/L1` and `counting-chance/L3`. This is the most doubtful change: the lessons lean on analysis l5 and l20. Add `analysis/L5` back only if the strand rule is relaxed.
  - `complex/L1`: "topic 1.10 finished" dropped (curriculum order only).
  - `pdes/L1`: `vector-calc` dropped (divergence and curl are one cited lesson).
  - `brainteasers/L1`: `proof` L3 to L4 dropped; the lessons cite contests invariants and modulo instead.
- Interview courses gate only on what their briefs name: `brainteasers` (counting-chance L2, contests L2, graphs-dp L3, mental L2), `game-theory`, `puzzles`, `mm-games`, `mental-pressure`, `coding-int`, `research-int`, `systems` use the plan's prerequisite lines and the "Builds on" lines of that level. No interview course waits on a topic outside those.
- `systems/L4`: the plan also names `cpp` L5 (titles only, unwritten). Left out so a written L4 is not blocked by an unwritten level; add `cpp/L5` if wanted.
- `topology/L3`: the plan names `numerics/L2`. Replaced by `taylor/L1` (Newton's method, written) to avoid a second unwritten reference.
- `numerics/L1`: the plan says "Stage 1 finished including odes L4". Replaced by the four things its lessons cite (`py-found/L1`, `cpp-pricing/L1`, `regression/L3`, which carries `least-squares/L3`).
- `recruiting`, `mental`, `terminal`, `first-python`, `number-sense` first levels stay open. `sql/L1` takes `equations/L3` (WHERE conditions are inequalities) so no Stage 1 course is open to a fresh profile.
- Projects: `recruiting/L2` and `L3` cite finished Stage 2 projects, but only as examples, and a Stage 0 course cannot require a later stage; both keep the implicit chain.
- One `lessonRequires`: `coding-int` `l5-bit-tricks` needs `contests/L3` (bitmasks, l11) while the rest of level 1 needs only `contests/L1` (stress testing). Without the override either the whole level waits for three contests levels or the lesson is under-gated. The list repeats the level's other two references because it replaces them.
- Same-stage later-topic references: none (the one found, `multivar/L2` to `vectors/L1`, was replaced by `counting/L3`; `multivar` lessons must teach the dot product themselves, as `counting` l9 to l13 only gives arrows and lengths).

## Warnings added (reference to a level with no written lesson in this worktree)

Most are a level of a course not yet written depending on the previous level of the same unwritten course, which is unavoidable and harmless. The cross-course ones, all genuine, are `pdes/L1` on `odes/L4` and `ito/L3`, `pdes/L3` on `numerics/L4`, `numerics/L3` on `odes/L4`, `odes/L2` and `pdes/L2` on `complex/L1`, `convex/L4` on `numerics/L2`, `measure-prob/L3` on `ito/L2`, `measure-prob/L4` and `pdes/L1` on `ito/L3`, `topology/L1` on `analysis/L5`. `coding-int/L4` on `coding-int/L3` clears when the parallel coding-int agent's level 3 merges.

- `complex/L2` requires `complex/L1`
- `complex/L3` requires `complex/L2`
- `vector-calc/L2` requires `vector-calc/L1`
- `vector-calc/L3` requires `vector-calc/L2`
- `odes/L2` requires `odes/L1`
- `odes/L2` requires `complex/L1`
- `odes/L3` requires `odes/L2`
- `odes/L4` requires `odes/L3`
- `numerics/L2` requires `numerics/L1`
- `numerics/L3` requires `numerics/L2`
- `numerics/L3` requires `odes/L4`
- `numerics/L4` requires `numerics/L3`
- `convex/L3` requires `convex/L2`
- `convex/L4` requires `convex/L3`
- `convex/L4` requires `numerics/L2`
- `stat-models/L2` requires `stat-models/L1`
- `stat-models/L3` requires `stat-models/L2`
- `stat-models/L4` requires `stat-models/L3`
- `momentum-rep/L3` requires `momentum-rep/L2`
- `pairs-rep/L2` requires `pairs-rep/L1`
- `ito/L4` requires `ito/L3`
- `measure-prob/L2` requires `measure-prob/L1`
- `measure-prob/L3` requires `measure-prob/L2`
- `measure-prob/L3` requires `ito/L2`
- `measure-prob/L4` requires `measure-prob/L3`
- `measure-prob/L4` requires `ito/L3`
- `pdes/L1` requires `odes/L4`
- `pdes/L1` requires `ito/L3`
- `pdes/L2` requires `pdes/L1`
- `pdes/L2` requires `complex/L1`
- `pdes/L3` requires `pdes/L2`
- `pdes/L3` requires `numerics/L4`
- `coding-int/L4` requires `coding-int/L3`
- `topology/L1` requires `analysis/L5`
- `topology/L3` requires `topology/L2`


## Stage 3 example: `research-int/L3` (The open case)

Its list is the implicit `research-int/L2`. Following the chain, a fresh profile must finish, or test out of, exactly these **85 levels** (83 outside the course; each is met by its review, its topic exam, its stage exit test or a level test-out):

- Stage 0, 0.1: number-sense L1 to L3, ratio L1 to L3
- Stage 0, 0.2: equations L1 to L4, functions L1 to L3, quadratics L1 to L2
- Stage 0, 0.3: counting L1 to L3, exp-log L1 to L3, series L1 to L2, trig L1 to L2
- Stage 0, 0.4: first-python L1 to L3, terminal L1
- Stage 1, 1.1: py-found L1 to L2, numpy-pandas L1 to L3
- Stage 1, 1.3: limits L1 to L4, integrals L1 to L2
- Stage 1, 1.4: vectors L1 to L3, elimination L1 to L3, least-squares L1 to L3, eigen L1 to L3
- Stage 1, 1.5: counting-chance L1 to L3, conditional L1 to L2, random-vars L1 to L3, limits-thm L1 to L3
- Stage 1, 1.6: estimation L1 to L3, testing L1 to L3, regression L1 to L3
- Stage 2, 2.1: stat-learning L1 to L3, validation L1 to L3, ensembles L1 to L3, fin-ml L1 to L2
- Stage 3, 3.5: research-int L1 to L2

Not required: markov, multivariable calculus, taylor, the finance topics, algorithms, C++, the three Stage 2 projects and every pure course. The Stage 0 exit test and the Stage 1 exit test each stand in for their stage's part of this list.

## Second-reader notes

- Doubtful by judgement (no brief): the Stage 0 and Stage 1 lists in the first two sections below, notably `counting-chance/L3` before `conditional/L1` and `random-vars/L1` (deep for the probability spine; `counting-chance/L2` would shorten it by one), `plotting/L3` on `exp-log/L2`, `pytest/L3` on `git/L3` and `plotting/L2`, `eigen/L4` on `taylor/L2` and `multivar/L4`.
- `linear-maps/L2` takes `eigen/L4` (the plan's "builds on eigen l13"), which drags `taylor/L2` and `multivar/L4` behind a pure course; drop it if that is too heavy.

# Per course


## Stage 0

### number-sense (topic 0.1): Number Sense

- L1 Fractions as amounts: open (first level, no `requires`).
- L2 Decimals and negatives: implicit, `number-sense/L1`.
- L3 Powers, roots and estimates: implicit, `number-sense/L2`.

### ratio (topic 0.1): Ratio and Percentages

- L1 Percentages: `number-sense/L2` (percentages are fractions and decimals).
- L2 Change over time: implicit, `ratio/L1`.
- L3 Ratio and proportion: implicit, `ratio/L2`.

### equations (topic 0.2): Equations and Inequalities

- L1 Expressions: `number-sense/L2` (letters stand for fractions, decimals and negatives).
- L2 Solving linear equations: implicit, `equations/L1`.
- L3 Inequalities and formulae: implicit, `equations/L2`.
- L4 Simultaneous equations: implicit, `equations/L3`.

### functions (topic 0.2): Functions and Graphs

- L1 Functions: `equations/L1` (a function rule is written with letters).
- L2 Straight lines: `functions/L1` (a line is a function); `equations/L2` (slope and intercept need solving a linear equation).
- L3 Curves and what they tell you: implicit, `functions/L2`.
- L4 Building new functions: `functions/L3` (new functions come from curves); `equations/L3` (running backwards is changing the subject).

### quadratics (topic 0.2): Quadratics

- L1 Factorising: `equations/L1` (factorising reverses opening brackets).
- L2 Solving: `quadratics/L1` (solving uses the factors); `equations/L2` (solving linear equations); `number-sense/L3` (the formula and completing the square need roots).
- L3 Parabolas: `quadratics/L2` (parabolas come from the roots); `functions/L3` (reading curves); `equations/L3` (above-or-below is a quadratic inequality).

### counting (topic 0.3): Counting and Vectors

- L1 Counting: `equations/L1` (the formulas are written with letters).
- L2 Harder counting: implicit, `counting/L1`.
- L3 Vectors: `functions/L2` (vectors use coordinates and lines); `trig/L1` (length of an arrow is Pythagoras).

### exp-log (topic 0.3): Exponentials and Logarithms

- L1 Exponential growth: `number-sense/L3` (powers and roots); `ratio/L2` (growth factors are percentage multipliers).
- L2 Logarithms: implicit, `exp-log/L1`.
- L3 The natural base: implicit, `exp-log/L2`.

### series (topic 0.3): Sequences and Series

- L1 Sequences: `equations/L1` (the n-th term is an expression); `number-sense/L3` (geometric sequences use powers).
- L2 Series: implicit, `series/L1`.
- L3 Binomial expansion and applications: `series/L2` (sums of powers); `counting/L1` (Pascal's triangle is choosing without order).

### trig (topic 0.3): Trigonometry

- L1 Triangles: `ratio/L3` (ratios that stay are similar triangles); `number-sense/L3` (exact values use roots).
- L2 The unit circle: implicit, `trig/L1`.
- L3 Identities and equations: `trig/L2` (identities from the unit circle); `quadratics/L2` (trig equations reduce to quadratics).

### first-python (topic 0.4): First Python Scripts

- L1 Values: open (first level, no `requires`).
- L2 Control flow: implicit, `first-python/L1`.
- L3 Functions and files: `first-python/L2` (functions use decisions and loops); `terminal/L1` (reading a file needs paths).

### terminal (topic 0.4): Your Machine and the Terminal

- L1 Files and folders: open (first level, no `requires`).
- L2 The terminal: implicit, `terminal/L1`.
- L3 Setting up to code: implicit, `terminal/L2`.

### mental (topic 0.5): Mental Arithmetic Drills

- L1 Adding and subtracting: open (first level, no `requires`).
- L2 Multiplying: implicit, `mental/L1`.
- L3 Dividing and fractions: `mental/L2` (division reverses multiplication); `number-sense/L2` (fractions to decimals).

### proof (topic 0.6, strand pure): Reasoning and Proof

- L1 Statements and logic: `equations/L3` (statements about ranges of answers); `functions/L1` (functions as rules to prove things about).
- L2 Sets and functions: `proof/L1` (sets use the logic of L1); `functions/L4` (functions as sets, inverses); `counting/L1` (choosing without order as a set count).
- L3 Proof methods: `proof/L2` (methods apply to sets and functions); `series/L2` (induction proves sums); `quadratics/L2` (the formula is proved); `counting/L3` (proving with vectors).

### recruiting (topic 0.7): Getting the Internship

- L1 The landscape: open (first level, no `requires`).
- L2 The application: implicit, `recruiting/L1`.
- L3 Interviews and after: implicit, `recruiting/L2`.


## Stage 1

### numpy-pandas (topic 1.1): NumPy and pandas

- L1 Arrays: `py-found/L2` (lists, dictionaries and functions).
- L2 DataFrames: implicit, `numpy-pandas/L1`.
- L3 Time series and groups: implicit, `numpy-pandas/L2`.

### plotting (topic 1.1): Plotting Market Data

- L1 First charts: `numpy-pandas/L2` (charts draw DataFrame columns).
- L2 Returns and risk: `plotting/L1` (charts of returns); `numpy-pandas/L3` (returns with shift and rolling windows).
- L3 Clear and honest: `plotting/L2` (honest charts of risk); `exp-log/L2` (the log axis).

### py-found (topic 1.1): Python Foundations

- L1 Core types: `first-python/L3` (functions and files are assumed).
- L2 Dictionaries and functions: implicit, `py-found/L1`.
- L3 Structure: implicit, `py-found/L2`.
- L4 From script to tool: implicit, `py-found/L3`.

### git (topic 1.2): Git and the Command Line

- L1 Commits: `terminal/L2` (commits are made from the command line).
- L2 Branches: implicit, `git/L1`.
- L3 GitHub and the shell: implicit, `git/L2`.

### pytest (topic 1.2): Testing with pytest

- L1 First tests: `py-found/L2` (tests call functions); `terminal/L2` (pytest runs from the terminal).
- L2 Better tests: implicit, `pytest/L1`.
- L3 Testable code: `pytest/L2` (testable code); `plotting/L2` (testing a drawdown function); `git/L3` (tests on every push).

### sql (topic 1.2): SQL Basics

- L1 Asking a table a question: `equations/L3` (WHERE conditions are inequalities).
- L2 Summaries: implicit, `sql/L1`.
- L3 Several tables: `sql/L2` (joins follow summaries); `numpy-pandas/L2` (database to pandas).

### integrals (topic 1.3): Integrals

- L1 Accumulating: `limits/L2` (accumulating a rate undoes slope); `series/L2` (sigma notation for rectangle sums).
- L2 The fundamental theorem: implicit, `integrals/L1`.
- L3 Techniques: `integrals/L2` (techniques use the fundamental theorem); `limits/L3` (undoing the chain and product rules).
- L4 More techniques: `integrals/L3` (harder techniques); `trig/L3` (circles and powers use identities).

### limits (topic 1.3): Limits and Derivatives

- L1 Approaching a value: `functions/L3` (limits read curves); `quadratics/L1` (computing limits factorises).
- L2 The derivative: implicit, `limits/L1`.
- L3 Rules: `limits/L2` (rules extend the derivative); `trig/L2` (derivatives of sin and cos); `exp-log/L3` (derivatives of e^x and ln).
- L4 Using derivatives: implicit, `limits/L3`.
- L5 Theorems, rates and shape: implicit, `limits/L4`.

### multivar (topic 1.3): Multivariable Calculus

- L1 Functions of two variables: `limits/L3` (partial derivatives use the rules).
- L2 Gradients: `multivar/L1` (gradients of two-input functions); `counting/L3` (a direction is an arrow with a length).
- L3 Optimisation: implicit, `multivar/L2`.
- L4 Multiple integrals: `multivar/L2` (polar and volume use gradients' geometry); `integrals/L3` (improper integrals for the bell curve).
- L5 Changing variables and many constraints: `multivar/L3` (many constraints extend Lagrange); `multivar/L4` (change of variables rewrites multiple integrals).

### taylor (topic 1.3): Series and Approximation

- L1 Approximating with lines: `limits/L4` (tangent lines, Newton and duration use derivatives and sensitivity).
- L2 Polynomials that hug a curve: `taylor/L1` (matching derivatives); `exp-log/L3` (the series of e^x and ln); `trig/L2` (the series of sin and cos).
- L3 Infinite series: `taylor/L2` (infinite series of the polynomials); `series/L2` (adding forever).

### eigen (topic 1.4): Eigenvalues and the SVD

- L1 Eigenvectors: `elimination/L3` (the characteristic polynomial is a determinant); `quadratics/L2` (its roots).
- L2 Symmetric matrices: `eigen/L1` (symmetric matrices are special eigen-cases); `least-squares/L1` (perpendicular eigenvectors).
- L3 The SVD: implicit, `eigen/L2`.
- L4 Factorisations at work: `eigen/L3` (factorisations at work); `taylor/L2` (e^(At) is a power series); `multivar/L4` (the normal density).

### elimination (topic 1.4): Elimination and Rank

- L1 Elimination: `vectors/L3` (elimination solves matrix equations).
- L2 Spaces: implicit, `elimination/L1`.
- L3 Determinants: implicit, `elimination/L2`.

### least-squares (topic 1.4): Orthogonality and Least Squares

- L1 Orthogonality: `elimination/L2` (four subspaces need column space and null space).
- L2 Projections: implicit, `least-squares/L1`.
- L3 Least squares: implicit, `least-squares/L2`.

### vectors (topic 1.4): Vectors and Matrices

- L1 Vectors: `counting/L3` (vectors as arrows); `trig/L2` (angles between vectors).
- L2 Matrices: implicit, `vectors/L1`.
- L3 Inverses and systems: `vectors/L2` (inverses of matrices); `equations/L4` (systems of equations).

### conditional (topic 1.5): Conditional Probability

- L1 Updating on evidence: `counting-chance/L3` (conditioning shrinks sample spaces and uses the probability rules).
- L2 Bayes’ rule: implicit, `conditional/L1`.
- L3 Independence: implicit, `conditional/L2`.
- L4 Puzzles that fool experts: implicit, `conditional/L3`.
- L5 Reasoning in the wild: implicit, `conditional/L4`.

### counting-chance (topic 1.5): Counting and Chance

- L1 Sample spaces: `counting/L2` (counts turn into chances).
- L2 Counting tools: implicit, `counting-chance/L1`.
- L3 Probability rules: implicit, `counting-chance/L2`.

### limits-thm (topic 1.5): Distributions and Limit Theorems

- L1 Named discrete distributions: `random-vars/L3` (counting successes needs mean and variance); `exp-log/L3` (the Poisson uses e).
- L2 Continuous distributions: `limits-thm/L1` (continuous analogues); `integrals/L2` (probability as area).
- L3 Limit theorems: implicit, `limits-thm/L2`.
- L4 Joint densities and transformations: `limits-thm/L3` (joint densities extend the limit theorems); `random-vars/L4` (joint tables come first); `multivar/L5` (Jacobians change variables); `integrals/L4` (Gamma and Beta integrals).

### markov (topic 1.5): Markov Chains and Random Walks

- L1 Markov chains: `conditional/L1` (transition probabilities are conditional); `vectors/L2` (the transition matrix acts on a vector).
- L2 The long run: `markov/L1` (the long run of a chain); `vectors/L3` (stationary distributions solve a linear system).
- L3 Random walks: `markov/L2` (walks use first-step analysis); `random-vars/L3` (expectation and variance of steps).
- L4 Reversible chains and sampling: `markov/L3` (reversible chains); `limits-thm/L4` (Gamma waits for the arrivals of the Poisson process).
- L5 Martingales and stopping: `markov/L4` (martingales extend the chains); `random-vars/L4` (conditional expectation).

### random-vars (topic 1.5): Random Variables

- L1 Random variables: `counting-chance/L3` (a random variable labels outcomes).
- L2 Expectation: implicit, `random-vars/L1`.
- L3 Spread: implicit, `random-vars/L2`.
- L4 Two variables at once: `random-vars/L3` (joint tables); `conditional/L3` (independence of variables).
- L5 Conditioning and inequalities: `random-vars/L4` (conditioning on a variable); `limits/L5` (convex bets use the second derivative).

### estimation (topic 1.6): Estimation

- L1 Estimators: `limits-thm/L3` (sampling variation needs the CLT).
- L2 Likelihood: `estimation/L1` (likelihood); `limits/L4` (maximising uses derivatives).
- L3 Uncertainty: `estimation/L2` (uncertainty of a fit); `conditional/L2` (updating a belief is Bayes).

### regression (topic 1.6): Linear Regression

- L1 Fitting a line: `estimation/L1` (estimators); `least-squares/L3` (the best line is a least-squares fit).
- L2 Inference: `regression/L1` (inference on a fitted line); `testing/L1` (is-slope-zero is a test).
- L3 Many variables and assumptions: implicit, `regression/L2`.

### testing (topic 1.6): Hypothesis Testing

- L1 Setting up a test: `estimation/L3` (a p-value is a statement about uncertainty).
- L2 Errors and power: implicit, `testing/L1`.
- L3 Testing many things: implicit, `testing/L2`.

### markets (topic 1.7): Markets and Instruments

- L1 Time value of money: `exp-log/L3` (interest on interest); `series/L3` (streams of payments).
- L2 Bonds and shares: implicit, `markets/L1`.
- L3 Forwards, futures and shorting: implicit, `markets/L2`.

### micro (topic 1.7): Market Microstructure

- L1 The order book: `markets/L2` (bids and asks of shares).
- L2 Costs: implicit, `micro/L1`.
- L3 Market makers: `micro/L2` (market makers); `conditional/L2` (adverse selection is Bayes).

### options (topic 1.7): Options and Payoffs

- L1 Calls and puts: `markets/L2` (options on shares and bonds); `functions/L4` (a payoff is a function).
- L2 Strategies: implicit, `options/L1`.
- L3 Prices: `options/L2` (prices of strategies); `markets/L3` (put-call parity uses forwards).

### trees (topic 1.7): Pricing with Trees

- L1 One step: `options/L3` (a tree copies an option's payoff); `random-vars/L2` (risk-neutral expectation).
- L2 Many steps: implicit, `trees/L1`.
- L3 Towards Black-Scholes: `trees/L2` (tiny steps); `limits-thm/L3` (sums of steps look normal).
- L4 Options at interview: `trees/L3` (Black-Scholes at interview); `markov/L3` (reflection principle).

### algo-think (topic 1.8): Algorithmic Thinking

- L1 Counting steps: `py-found/L2` (code to count steps in); `exp-log/L2` (logarithmic growth).
- L2 Recursion: implicit, `algo-think/L1`.
- L3 Searching and sorting: implicit, `algo-think/L2`.

### ds (topic 1.8): Core Data Structures

- L1 Arrays and hashing: `algo-think/L1` (Big-O and memory choose a structure).
- L2 Pointers and windows: implicit, `ds/L1`.
- L3 Stacks, queues and lists: implicit, `ds/L2`.
- L4 Trees and heaps: `ds/L3` (trees and heaps); `algo-think/L2` (tree recursion).

### graphs-dp (topic 1.8): Graphs and Dynamic Programming

- L1 Graphs: `ds/L3` (breadth-first search uses queues); `algo-think/L2` (depth-first search is recursion).
- L2 Paths: `graphs-dp/L1` (paths); `ds/L4` (Dijkstra needs a heap).
- L3 Backtracking and memory: implicit, `graphs-dp/L2`.
- L4 Dynamic programming: implicit, `graphs-dp/L3`.

### cpp (topic 1.9): C++ Foundations

- L1 First programs: `first-python/L3` (control flow and functions are assumed); `terminal/L3` (compile and run from the terminal).
- L2 References and memory: implicit, `cpp/L1`.
- L3 Classes: implicit, `cpp/L2`.
- L4 The standard library and tools: implicit, `cpp/L3`.
- L5 C++ questions at interview: implicit, `cpp/L4`.

### cpp-pricing (topic 1.9): C++ for Pricing

- L1 Numbers in C++: `cpp/L2` (doubles and cmath need references and memory).
- L2 Pricers: `cpp-pricing/L1` (pricers); `cpp/L3` (payoff classes); `trees/L3` (binomial and Black-Scholes to rewrite).
- L3 Fast and correct: `cpp-pricing/L2` (speed up the pricers); `cpp/L4` (testing and tools).

### analysis (topic 1.10, strand pure): Real Analysis

- L1 The real numbers: `proof/L3` (every lesson is a proof).
- L2 Sequences: `analysis/L1` (sequences of reals); `limits/L2` (epsilon-N formalises limits).
- L3 Series: `analysis/L2` (series are sequences of partial sums); `taylor/L3` (convergence of series).
- L4 Continuity and the derivative: `analysis/L3` (continuity); `limits/L5` (mean value theorem and first-principles derivatives).
- L5 Integration and metric spaces: `analysis/L4` (integration after the derivative); `integrals/L2` (Riemann sums); `least-squares/L1` (perpendicular, for metric spaces).

### linear-maps (topic 1.10, strand pure): Linear Maps and Proof

- L1 Vector spaces: `proof/L3` (abstract vector spaces are proved); `elimination/L2` (spaces, bases and rank).
- L2 Linear maps: `linear-maps/L1` (maps between vector spaces); `least-squares/L1` (four subspaces); `eigen/L4` (same map, new basis).
- L3 Duality and inner products: `linear-maps/L2` (duality); `least-squares/L2` (projections and inner products).
- L4 Operators: `linear-maps/L3` (operators); `eigen/L2` (spectral theorem builds on symmetric matrices).

### complex (topic 1.11, strand quant): Complex Numbers

- L1 The complex plane: `trig/L3` (Euler's formula needs identities); `exp-log/L3` (e^x); `taylor/L2` (series of e^x, sin and cos).
- L2 Complex functions: `complex/L1` (functions of a complex variable); `multivar/L1` (partial derivatives for Cauchy-Riemann).
- L3 Integrals and Fourier: `complex/L2` (contour integrals); `integrals/L3` (improper integrals); `limits-thm/L4` (characteristic and generating functions).

### odes (topic 1.11, strand quant): Differential Equations

- L1 First-order equations: `integrals/L3` (separable equations need integration techniques); `exp-log/L3` (exponential solutions).
- L2 Second-order equations: `odes/L1` (second-order); `complex/L1` (complex roots and Euler's formula).
- L3 Systems and stability: `odes/L2` (systems); `eigen/L4` (stability from eigenvalues and e^(At)).
- L4 Transforms and numerical solution: `odes/L3` (transforms and numerical solution); `taylor/L3` (Taylor error of Euler and Runge-Kutta); `numpy-pandas/L1` (NumPy solvers).

### vector-calc (topic 1.11, strand pure): Vector Calculus

- L1 Fields and line integrals: `multivar/L2` (gradients and fields); `integrals/L2` (line integrals are evaluated integrals).
- L2 Green’s theorem: `vector-calc/L1` (Green's theorem); `multivar/L4` (double integrals).
- L3 Surfaces and space: `vector-calc/L2` (surfaces); `multivar/L5` (change of variables and triple integrals).


## Stage 2

### ensembles (topic 2.1): Trees and Ensembles

- L1 Decision trees: `stat-learning/L3` (trees classify); `validation/L1` (overfitting is measured by holding out).
- L2 Averaging trees: implicit, `ensembles/L1`.
- L3 Boosting: implicit, `ensembles/L2`.

### fin-ml (topic 2.1): Financial Machine Learning

- L1 Labels: `validation/L2` (time-ordered labels); `stat-learning/L3` (models to label).
- L2 Features: implicit, `fin-ml/L1`.
- L3 From prediction to profit: implicit, `fin-ml/L2`.

### stat-learning (topic 2.1): Statistical Learning

- L1 What learning means: `regression/L3` (learning generalises regression); `numpy-pandas/L3` (data handling).
- L2 Linear models: implicit, `stat-learning/L1`.
- L3 Classification: `stat-learning/L2` (classification extends linear models); `conditional/L2` (probabilities of classes).

### validation (topic 2.1): Validation and Leakage

- L1 Cross-validation: `stat-learning/L2` (cross-validation of fitted models).
- L2 Time: implicit, `validation/L1`.
- L3 Leakage: implicit, `validation/L2`.

### arma (topic 2.2): Stationarity and ARMA

- L1 Stationarity: `regression/L3` (ARMA is regression on the past); `numpy-pandas/L3` (time series handling).
- L2 Memory: implicit, `arma/L1`.
- L3 ARMA: implicit, `arma/L2`.

### coint (topic 2.2): Cointegration

- L1 Spurious relationships: `arma/L2` (spurious regressions come from non-stationary series).
- L2 Spreads: implicit, `coint/L1`.
- L3 Pairs trading: implicit, `coint/L2`.

### garch (topic 2.2): Volatility and GARCH

- L1 Clustering: `arma/L2` (volatility clusters like autocorrelation of squares).
- L2 Models: `garch/L1` (models of clustering); `arma/L3` (GARCH extends ARMA).
- L3 Using forecasts: implicit, `garch/L2`.

### alpha (topic 2.3): Alpha Signal Research

- L1 Universe: `fin-ml/L3` (signals are features); `validation/L3` (leakage in the universe).
- L2 Signals: implicit, `alpha/L1`.
- L3 Measuring: implicit, `alpha/L2`.
- L4 From signal to strategy: `alpha/L3` (signal to strategy); `micro/L2` (costs).

### backtest (topic 2.3): Backtesting Engine

- L1 Design: `fin-ml/L3` (the engine backtests predictions); `validation/L3` (leakage is the engine's first check).
- L2 Execution: `backtest/L1` (execution); `micro/L2` (costs and spread); `pytest/L2` (the engine is tested).
- L3 Metrics: `backtest/L2` (metrics of executed trades); `pytest/L3` (testable code).
- L4 Honest results: implicit, `backtest/L3`.

### opt-dash (topic 2.3): Options Analytics Dashboard

- L1 Data: `trees/L3` (the dashboard prices options); `numpy-pandas/L2` (option chains in DataFrames).
- L2 Pricers: implicit, `opt-dash/L1`.
- L3 Implied volatility: implicit, `opt-dash/L2`.
- L4 Greeks and the dashboard: implicit, `opt-dash/L3`.

### contests (topic 2.4): Contest Practice

- L1 How contests work: `graphs-dp/L2` (contest problems use graphs and heaps).
- L2 Contest maths: implicit, `contests/L1`.
- L3 Common patterns: implicit, `contests/L2`.
- L4 In the contest: implicit, `contests/L3`.

### convex (topic 2.5, strand quant): Convex Optimisation

- L1 Convexity: `eigen/L2` (convexity of quadratic forms); `multivar/L3` (second-derivative test); `random-vars/L5` (Jensen).
- L2 Linear programmes: implicit, `convex/L1`.
- L3 Duality and KKT: `convex/L2` (duality); `multivar/L5` (Lagrange multipliers with many constraints).
- L4 Algorithms: `convex/L3` (algorithms); `numerics/L2` (Newton and bisection convergence).

### numerics (topic 2.5, strand quant): Numerical Methods

- L1 Errors: `py-found/L1` (floating point); `cpp-pricing/L1` (doubles in C++); `regression/L3` (conditioning and collinearity).
- L2 Equations and curves: `numerics/L1` (root finding after errors); `taylor/L1` (Newton); `algo-think/L3` (bisection is halving); `trees/L3` (implied volatility).
- L3 Integrals and time steps: `numerics/L2` (integrals and steps); `odes/L4` (Euler and Runge-Kutta).
- L4 One option, three ways: `numerics/L3` (three ways to price); `trees/L3` (the pricer); `opt-dash/L2` (Monte Carlo pricers).

### stat-models (topic 2.6, strand quant): Statistical Modelling

- L1 Generalised linear models: `stat-learning/L3` (logistic models); `regression/L3` (GLMs generalise regression).
- L2 Experiments: `stat-models/L1` (experiments); `testing/L3` (multiple testing and ANOVA).
- L3 Without the assumptions: `stat-models/L2` (without the assumptions); `limits-thm/L4` (order statistics).
- L4 Bayesian models: `stat-models/L3` (Bayesian models); `markov/L4` (MCMC is a Markov chain).


## Stage 3

### momentum-rep (topic 3.1): Replicating Momentum

- L1 The paper: `alpha/L4` (the momentum signal and portfolios); `testing/L3` (t statistics and Sharpe).
- L2 Data and portfolios: implicit, `momentum-rep/L1`.
- L3 Evidence and extension: `momentum-rep/L2` (evidence on the replicated table); `backtest/L4` (held-out period and honest results).

### pairs-rep (topic 3.1): Replicating Pairs Trading

- L1 The paper: `coint/L3` (the paper is read against cointegration pairs trading).
- L2 Trading: `pairs-rep/L1` (trading the pairs); `backtest/L2` (fills and costs).
- L3 Beyond the paper: implicit, `pairs-rep/L2`.

### ito (topic 3.2): Brownian Motion and Itô

- L1 Brownian motion: `markov/L3` (walks scale to Brownian motion); `limits-thm/L3` (sums look normal); `trees/L3` (tiny steps).
- L2 Itô calculus: `ito/L1` (Itô calculus); `taylor/L2` (second-order expansion); `random-vars/L4` (conditional expectation).
- L3 Pricing: implicit, `ito/L2`.
- L4 Stochastic calculus at interview: `ito/L3` (interview questions on the derivation); `markov/L5` (optional stopping and reflection).

### measure-prob (topic 3.2, strand quant): Measure-Theoretic Probability

- L1 Measures: `ito/L1` (the course follows Brownian motion); `counting-chance/L3` (events as sets and the axioms).
- L2 Integration: `measure-prob/L1` (integration); `limits-thm/L3` (laws of large numbers and the CLT).
- L3 Information and martingales: `measure-prob/L2` (conditional expectation); `markov/L5` (martingales); `ito/L2` (fair games).
- L4 Changing measure: `measure-prob/L3` (change of measure); `ito/L3` (risk-neutral pricing).

### pdes (topic 3.2, strand quant): Partial Differential Equations

- L1 The heat equation: `odes/L4` (PDEs extend ODEs); `ito/L3` (the Black-Scholes equation).
- L2 Separation and Fourier series: `pdes/L1` (Fourier series); `complex/L1` (Euler's formula).
- L3 Pricing equations: `pdes/L2` (pricing equations); `numerics/L4` (finite differences).

### brainteasers (topic 3.3): Logic and Brainteasers

- L1 Invariants and counting arguments: `counting-chance/L2` (counting in stages); `contests/L2` (invariants and modulo).
- L2 Strategy and logic: `brainteasers/L1` (strategy); `graphs-dp/L3` (remembering (dynamic programming)).
- L3 Quick reasoning: `brainteasers/L2` (quick reasoning); `mental/L2` (squaring); `series/L2` (Gauss); `exp-log/L3` (doubling time and natural log).

### game-theory (topic 3.3): Games, Auctions and Poker

- L1 Games in a table: `random-vars/L2` (fair price); `equations/L4` (simultaneous equations for mixing).
- L2 Sequential games and auctions: `game-theory/L1` (sequential games); `graphs-dp/L4` (dice stopping); `micro/L3` (adverse selection and winner's curse); `limits/L4` (optimising a bid).
- L3 Poker and decisions: `game-theory/L2` (poker and decisions); `puzzles/L4` (Kelly sizing and who wins).

### mental-pressure (topic 3.3): Mental Maths Under Pressure

- L1 Speed: `mental/L3` (speed drills extend the mental drills).
- L2 Fractions and estimates: implicit, `mental-pressure/L1`.
- L3 Test formats: implicit, `mental-pressure/L2`.
- L4 Assessment batteries: `mental-pressure/L3` (batteries); `conditional/L2` (natural frequencies); `limits-thm/L2` (bell curve).

### mm-games (topic 3.3): Market-Making Games

- L1 Fair value: `random-vars/L3` (fair value and spread); `micro/L1` (bids and asks).
- L2 Quoting: `mm-games/L1` (quoting); `micro/L3` (informed flow is adverse selection).
- L3 Risk: implicit, `mm-games/L2`.
- L4 Trading games firms run: `mm-games/L3` (trading games); `options/L3` (put-call parity); `puzzles/L4` (Kelly sizing).

### puzzles (topic 3.3): Probability Puzzles

- L1 Expected value: `random-vars/L2` (expected value and indicators); `markov/L2` (waiting times by first step).
- L2 Conditioning: `puzzles/L1` (conditioning); `conditional/L2` (Bayes in a minute); `markov/L3` (ruin in interviews).
- L3 Continuous and geometric: `puzzles/L2` (continuous puzzles); `limits-thm/L2` (densities and areas).
- L4 Games and betting: implicit, `puzzles/L3`.
- L5 Puzzles firms keep asking: `puzzles/L4` (firms' favourites); `conditional/L4` (Monty Hall); `limits-thm/L4` (smallest and largest); `estimation/L1` (right target).

### algebra (topic 3.4, strand pure): Abstract Algebra

- L1 Groups: `proof/L3` (groups are proved); `linear-maps/L2` (structure-preserving maps); `contests/L2` (modulo and gcd).
- L2 Inside a group: implicit, `algebra/L1`.
- L3 Maps between groups: implicit, `algebra/L2`.
- L4 Rings and fields: implicit, `algebra/L3`.

### topology (topic 3.4, strand pure): Metric and Topological Spaces

- L1 Metric spaces revisited: `analysis/L5` (metric spaces are revisited).
- L2 Topological spaces: implicit, `topology/L1`.
- L3 Compact and complete: `topology/L2` (compactness); `taylor/L1` (Newton iteration as a fixed-point example).

### coding-int (topic 3.5): Coding Interviews

- L1 Patterns still to learn: `graphs-dp/L4` (ds and graph patterns); `algo-think/L3` (sorting by hand and greedy); `contests/L1` (stress testing).
  - override `l5-bit-tricks`: `graphs-dp/L4` (ds and graph patterns); `algo-think/L3` (sorting by hand and greedy); `contests/L3` (bitmasks).
- L2 Strings and simulation: `coding-int/L1` (strings build on patterns); `micro/L1` (the matching engine).
- L3 Design in code: `coding-int/L2` (design); `py-found/L3` (data with behaviour).
- L4 Under the clock: `coding-int/L3` (under the clock); `contests/L4` (choosing which problem first and debugging under time).

### research-int (topic 3.5): Research Interviews

- L1 Statistics and linear algebra questions: `regression/L3` (regression and its assumptions); `testing/L3` (tests in words and correction); `eigen/L2` (covariance and PSD).
- L2 Machine learning questions: `research-int/L1` (ML questions); `ensembles/L3` (trees, forests, boosting); `validation/L3` (leakage and weak signals); `eigen/L3` (PCA); `fin-ml/L2` (hidden look-ahead).
- L3 The open case: implicit, `research-int/L2`.
- L4 Data tasks and take-homes: `research-int/L2` (data tasks); `fin-ml/L3` (the end-to-end task); `pytest/L2` (take-home tests).

### systems (topic 3.5): Systems for Developer Interviews

- L1 Memory and the machine: `cpp/L4` (addresses, heap and vector); `cpp-pricing/L3` (timing, memory layout and flags).
- L2 Concurrency: `systems/L1` (concurrency); `ds/L3` (queues for producer-consumer).
- L3 Operating systems and networks: implicit, `systems/L2`.
- L4 Low-latency C++: implicit, `systems/L3`.

