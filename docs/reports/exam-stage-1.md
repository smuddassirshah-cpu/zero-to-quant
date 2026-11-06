# Stage 1 exit test

File: `app/content/exams/stage-1.json`. Scripts: `docs/briefs/exam-stage-1-scripts/` (`build.py` route A, `check_numbers.py` route B, `fresh.py`).

## Design (written before the build)

Source: the `**Exit:**` line of each of topics 1.1 to 1.11 in `docs/curriculum.md`. What the app can mark becomes paper items; what it cannot becomes a `check`.

| Exit line | Paper items (auto) | Check (self-ticked) |
|---|---|---|
| 1.1 returns, annualised volatility, drawdown from a CSV, plotted | C: three-part Python code item from CSV text; plotting choice; broadcasting and group-by items | project in a repository (with 1.2) |
| 1.2 the project in Git with a test | C: SQL parts item, Git order item, pytest choice | project in a repository with a passing test |
| 1.3 18.01 final at 70%, 18.02 sets | A: nine calculus items (limit, chain rule, FTC, parts, optimisation, Taylor, gradient, Lagrange, double integral) | 18.01 final and 18.02 sets |
| 1.4 18.06 final at 70%, least squares and PCA in NumPy | A: five items plus a two-part NumPy code item (normal equations, then PCA by `eigh`) | 18.06 final |
| 1.5 two Stat 110 finals at 70% | B: five authored items plus five drawn from `bank/probability` | two Stat 110 finals |
| 1.6 regression in NumPy matching statsmodels, every summary number explained | B: MLE, interval, p-value, multiple testing; a parts item: OLS code, then t and p read from the table | the regression matches statsmodels and every summary number is explained in a line |
| 1.7 order book, spread, market against limit, parity, binomial tree in Python | B: book parts item, parity, two-step tree, CRR pricer in Python; two drawn from `bank/market-making` | none |
| 1.8 150 problems, a fresh medium in 30 minutes | C: complexity table, DP count, two-pointer code item; one drawn `drills/oa` medium | 150 problems solved |
| 1.9 the binomial pricer in C++, tested and timed | C: C++ CRR pricer item, a by-value and by-reference item; one drawn `drills/ci-cpp` drill | tests and a timing against Python |
| 1.10 18.100A final at 60%, rank-nullity and spectral theorem without notes | D: epsilon-N, series, delta, MVT, compactness, inner product, dimension; two order proofs | 18.100A past final, and the two proofs written without notes |
| 1.11 18.03 final at 70%, a numerical solution matching its closed form to 4 dp | D: complex power, residue, Green, second-order solution, Laplace; RK4 code item on a mean-reverting rate | 18.03 final |

Papers (pass 0.7 each, the stage-exam pass in DECISIONS):

- **A. Calculus and linear algebra** (1.3, 1.4): 15 authored items, ramp 3, 8, 3, 1 at difficulties 2 to 5.
- **B. Probability, statistics and finance** (1.5, 1.6, 1.7): 14 authored items plus draws `bank/probability` (n 5) and `bank/market-making` (n 2). The draws exclude the tags `at-least-one` and `bayes-in-a-minute`, whose pool items are twins of two authored items.
- **C. Programming in Python and C++** (1.1, 1.2, 1.8, 1.9): 13 authored items plus draws `drills/oa` (n 1) and `drills/ci-cpp` (n 1).
- **D. Analysis, proof and 1.11 methods** (1.10, 1.11): 15 authored items, ramp 3, 8, 3, 1.
- Nine checks for the past finals, the project repository, the 150 problems, the C++ timing, the two proofs without notes and the explained regression summary.

Minutes come from the summed `pace` of each paper. Every authored number is fresh (`fresh.py`) and recomputed by `check_numbers.py`; code solutions run against their tests there (Python in-process, C++ with the local `g++`), and the starters fail.

## Result

- Paper A, calculus and linear algebra: 60 min, 15 items (12 numeric, 1 expression, 1 choice, 1 two-part NumPy code item), ramp 3, 8, 3, 1.
- Paper B, probability, statistics and finance: 105 min, 14 authored items plus 7 drawn (21). Authored: 11 numeric, a parts item (OLS code, t statistic, reading P>|t|), an order-book parts item (spread, a market order walking the book, a resting limit order), a CRR put pricer in Python with a dividend yield.
- Paper C, programming in Python and C++: 145 min, 13 authored items plus 2 drawn drills (15). Authored: the 1.1 exit as three code parts (returns from CSV text, annualised volatility, drawdown), SQL parts, a Git order item, pytest, broadcasting and plotting choices, a big-O table with slip ids, a DP count, a two-pointer code item with a 200,000-price speed test, the CRR pricer in C++ (calls and puts, 1,000 steps), a by-value and by-reference program.
- Paper D, analysis, proof and the 1.11 methods: 70 min, 15 items (9 numeric, 2 choice, 1 expression, 2 order proofs with two flawed lines each, 1 RK4 code item), ramp 3, 8, 3, 1. The proofs are the two the 1.10 exit names: rank-nullity and the spectral theorem for symmetric matrices.
- Nine checks: 18.01 with the 18.02 sets, 18.06, two Stat 110 finals, the price-file project in Git with a test, 150 problems with a fresh medium in 30 minutes, the C++ pricer tested and timed, 18.100A at 60% with two proofs without notes, 18.03 at 70%, and the regression summary explained (added in the fix pass, after the original eight, so check positions hold).
- Every topic 1.1 to 1.11 has at least two authored auto-graded items; `check_numbers.py` asserts this from each item's skills against `curriculum.json`.
- Minutes are 1.25 times the summed `pace`, drawn items counted at 180 s (bank) and their own pace (drills), rounded up to 5.

## Draws (bank tags used)

- B: `bank/probability`, difficulty 3 to 4: `dice-ev`, `every-coupon`, `hats` (n 3, pool 11); `indicator-tricks`, `given-the-total`, `urns` (n 2, pool 6). `at-least-one` and `bayes-in-a-minute` were dropped in the fix pass: each had a pool item that was a twin of `b-forty-tests` or `b-fraud-flag`.
- B: `bank/market-making`, difficulty 3 to 4: `quote-centre`, `informed-loss`, `position-limit`, `skew` (n 2, pool 7), for the 1.7 market-making cover.
- C: `drills/oa`, difficulty 3 to 4 (n 1, pool 8), the fresh medium of the 1.8 exit; `drills/ci-cpp`, difficulty 3 to 4 (n 1, pool 5), a C++ data-structure task for 1.9.
- The 1.1 risk drills (`daily-returns`, `annualised-vol`, `max-drawdown`) have no pack, so a one-drill pool would warn; the 1.1 exit is authored instead (backlog bullet).

## Gates

- Validator: 0 errors, no warning on `stage-1.json`. (The first build had none; the later key-length rule flagged three options, which the fix pass shortened.)
- Voice scan on a copy (`VOICE_BASE=<scratch>/voice1/`): 0 sentences over 20 words, 0 explanations over three sentences, 1,092 sentences. No exclamation marks, em-dashes or en-dashes.
- `check_numbers.py`: 458 of 458, exit 0. Route B: numerical derivatives and Simpson integrals, grid searches, Fractions, QR and SVD, power iteration, a linear solve for ruin, the incomplete beta for the t tail, replication on the tree, sqlite3 running the printed SQL, g++ running the printed C++ program and the C++ solution, the closed-form binomial sum for every pricer test, a contour sum, four line integrals and a fine RK4 for the damped equation. Every Python and C++ solution passes its tests and every starter fails one. A last pass reads every number in every learner-visible string.
- Playthrough with `--local-cdn`: green with and without `--mobile` (74 items, 66 of 66 scored, passed). Screenshots at 440 px checked: the order proofs, the code editor and the result page lay out cleanly.
- `readiness-sums.mjs`: OK after the fix pass (it failed on the catalogue block at the first build, since fixed outside the exam files).

## Freshness

`fresh.py` greps each item's distinctive setup and key against every content file. First-build clashes, all replaced before the commit:

- $(3x^2 + 1)^4$ (limits l10) became $(x^3 + 2x)^4$; $\int_0^1 xe^{2x}$ (integrals l10, key 2.0973) became $xe^{3x}$; $e^x \sin x$ (integrals homework 3) became $e^x \cos x$.
- $x^2y + 3y$ (multivar l2), the triangle $0 \le y \le x \le 2$ (multivar homework 4), the matrix $\begin{pmatrix}5&2\\2&2\end{pmatrix}$ (eigen l2, l11) and $\begin{pmatrix}3&0\\4&5\end{pmatrix}$ (topic-1.4) were all replaced.
- The line-distance key $\sqrt8$ was eigen review-4's key; the item now keys $\sqrt{10}$ on a new line.
- `crr_call` was trees homework 3's task, so B's pricer is now a put on a dividend-paying share. 400 independent bets (limits-thm l11) became 350; 0.08% a day (topic-1.6) became 0.07% over 484 days.
- Also changed: the 1,000,000-price search (algo-think l3), $\sum 3^n/n!$ (analysis homework 3), $x^3 - 3x$ for the MVT (limits l17, topic-1.3) and $\oint e^z/(z - 1)$ (complex l10).
- Fix pass: seven setups that the second read found reused with new constants were replaced: the 144-trade interval half-width (was estimation homework 1's P&L item scaled), the delta for $x^2 + 3x$ at 1 (was analysis l15's $x^2$ at 3), at least two of 40 tests (was the at-least-one question of testing l9 and review 3), `HAVING AVG(px) > 3` (was l7's `COUNT(*)` ladder), $\lim \tfrac{1 - \cos 3x}{x \sin x}$ (was limits review 4's $\tfrac{1 - \cos 2x}{x^2}$), $\oint \tfrac{\cos z}{z^2 - 4z + 3}$ (was complex l10's simple pole at 1), and the cosine between $x$ and $x^2$ (was two screens of linear-maps l11). `fresh-check.mjs --exam stage-1 --min-run 10` still hits the compactness item against topology review-3 (same key set, judged acceptable: the 1.10 exit is about this fact, and option b now differs) and LaTeX or table skeletons.
- Remaining hits are common values in unrelated items ($0.85$, $0.625$, 50p, `(5, 1)`), generic clauses (heapify), or later-stage courses.

## Notes for the main session

- `curriculum.json` stage 1 `exitTests` still lists two lines ("University finals at 70% in calculus, linear algebra and probability", "150 algorithm problems solved"). The exam follows the per-topic exit lines of `docs/curriculum.md`, which ask for more. Not edited here.
