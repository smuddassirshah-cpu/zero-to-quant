# Concept audit: markov L1 to L3 (round 1, blind read, 11 Nov 2026)

Scope: lessons `l1` to `l12`, `review-1` to `review-3`, `homework-1` to `homework-3`, `problems-1` to `problems-3`, `fluency-l2-transition-matrix.json`. Every screen, item, hint, `why`, `byKey`, `explain`, model answer, rubric and code solution was read. Ledger: `docs/reports/audit-markov-1-3-ledger.md` (339 rows: 322 correct, 12 imprecise, 2 misleading, 3 wrong, 0 unverified). Script: `docs/reports/markov-L1-3-concepts.py` (82 checks; 8 left failing on purpose, one per scriptable finding; each turns green when its sentence is fixed). Sources are named in the ledger header.

Format: `N. file | JSON path | severity | serious or minor | problem | evidence and basis | exact fix`.

Totals: 16 findings. `wrong` 2 (1 serious, 1 minor). `imprecise` 12 (all minor). `misleading` 2 (1 serious, 1 minor). No graded key, `wrong[]` value or code solution was found wrong: every one was recomputed, and every seeded canvas figure quoted in the text (9 of 30, 2,398 bets, 13 of 40 and the rest) was reproduced from the engine's generator.

Points the brief asked to press, and what was found:

- Markov property: stated throughout as "given the present, the past adds nothing" (l1 `screens[7]`, summary). Correct. Time-homogeneity is used everywhere and never said (finding 5).
- Row against column convention: said once in l2 `screens[0]`, restated in l2 `screens[7]`, quiz and summary, and in l5 `screens[5]`; kept in every file.
- Stationary distributions: existence, uniqueness and convergence are separated correctly in l6 (`screens[7]`, summary formula note), except the summary's claim about reducible chains (finding 1).
- Stationary against limiting: handled correctly (swap, ring, Long/Flat/Short rule).
- Absorbing chains, $(I - Q)^{-1}$, times and probabilities: correct, boundary values right in every item.
- Gambler's ruin: both formulas, limits and boundary conventions correct.
- Reflection: inequalities, factor of two and parity correct in every item; one unconditioned count formula (finding 10).
- Recurrence: correct (fair walk returns with chance 1; return counts 7 and 79 verified).
- Root-n scaling and price paths: log returns and independence are stated where first used. One CLT statement drops "identically distributed" (finding 11).
- Regimes and identification: estimation noise and memorylessness are named; one item assumes the regime is observed in real time without saying so (finding 16), and one "fair price" uses chances that do not make the share a fair bet (finding 3).

## Wrong

1. l6-always-settle.json | `summary.ideas[1]`; `screens[6].feedback.byKey.unique` | wrong | serious | "A reducible chain has several closed classes and many stationary distributions." and "This chain is reducible, so it has many". False as stated. The lesson defines reducible as "not every state reaches every other", so the loan chain of the previous lesson (Perf, Def) is reducible, yet it has one closed class and the single stationary distribution $(0, 1)$, as that lesson itself shows. So is every chain with one absorbing state (the A, B, Default ratings chain). A learner carries away "reducible means no unique $\pi$". | A finite chain has a unique stationary distribution exactly when it has one closed class; the number of extreme stationary distributions equals the number of closed classes (Levin, Peres and Wilmer, Prop. 1.26 and exercise 1.13; Norris 1.7 to 1.8). Script: $\pi P = \pi$ for $\begin{pmatrix}0.97 & 0.03\\ 0 & 1\end{pmatrix}$ has a one-dimensional solution set. Checks "FINDING l6 summary" and "FINDING l6 s6 feedback" fail on purpose. | `summary.ideas[1]`: "A chain with two or more closed classes has many stationary distributions, and its long-run split depends on the start. Such a chain is reducible. A reducible chain with one closed class, such as a chain with one absorbing state, still has one $\\pi$." `screens[6].feedback.byKey.unique`: "You assumed $\\pi P = \\pi$ has one solution. This chain has two closed classes, so it has many, and the start picks the limit."

2. l1-only-now.json | `screens[4].widget.options[2].why` | wrong | minor | "You stopped one step early or went round backwards." Stopping one step early (6 steps) lands on Open, which is a different option. Pre-open comes from one step too many (8 steps) or from going backwards. | Open, Closed, Pre-open, Open: step 6 is Open, step 7 Closed, step 8 Pre-open; seven steps backwards from Open is Pre-open. Script check "FINDING l1 s4" fails on purpose. | "You took one step too many or went round backwards. After 6 steps it is Open; the 7th step goes to Closed."

## Misleading, serious

3. problems-3.json | `items[1].parts[3].question`, `items[1].parts[3].explain.text` (also `feedback.byKey.pays-on-touch`) | misleading | serious | "what is the fair price of the note" and "With no interest the fair price is the expected pay-out." The share is multiplied by 1.1 or divided by 1.1 "with equal chance". Under those chances the share itself gains $0.5(1.1) + 0.5/1.1 - 1 = 0.45\%$ a day on average, so they are not the chances a price is taken under. The item teaches "price a derivative by its expected pay-out under the real-world chances", the habit an interviewer tests for. Lesson 12's one-touch does not have this problem: its walk is in unit steps of price, a fair bet, so expectation and price agree. | In a binomial model with no interest the no-arbitrage value is the expectation under $q = \tfrac{1 - d}{u - d}$ (Shreve, *Stochastic Calculus for Finance I*, 1.1 to 1.2; Hull, ch. 13). Here $q = \tfrac{0.1}{0.21} \approx 0.476$, and the note is then worth £55.57, not £61.23 (script, check "FINDING p3 barrier note", failing on purpose). The keyed number 61.2305 is the right expected pay-out; only its name is wrong. | Keep the key. `question`: "Using the touch chance 0.3877 from part 3, what is the note's expected pay-out, in pounds? Give a decimal to 2 places." `explain.text`: "The note pays £100 with chance $1 - 0.3877 = 0.6123$, so its expected pay-out is £61.23. Judging by the end alone would give £80.62, far too much. A desk would not price with the 0.5: it uses the up-chance that makes the share itself a fair bet, about 0.476 here, which gives about £55.57." `feedback.byKey.pays-on-touch`: "That is the expected pay-out of a note that pays when the barrier is touched. This one pays when it is not."

## Imprecise, minor

4. l4-regimes.json | `screens[10].question` (also `homework-1.json` `items[9].model` part (f), "still expected to last 6.67 more") | imprecise | minor | "How many more weeks is the drawdown expected to last?" is keyed 6.67. That counts the present week. Read as weeks after this one, the answer is $0.85/0.15 = 5.67$, which is graded wrong with the generic line. The lesson's own run length $L$ counts periods in the state, so both readings are natural. | With $P(L = n) = p^{n-1}(1 - p)$: $E[L - 4 \mid L > 4] = 6.67$ and $E[L - 4 \mid L \ge 4] = 5.67$. Script check "FINDING l4 s10" fails on purpose. | `screens[10].question`: "Counting this week, how many more weeks is the drawdown expected to last?" homework-1 model (f), replace "is still expected to last 6.67 more" with "is still expected to last 6.67 more, counting the present week".

5. l1-only-now.json | `screens[7].prose` | imprecise | minor | The display sets $P(X_{n+1} = j \mid X_n = i) = p_{ij}$ with no $n$ on the right. That is a second assumption, the same arrows on every day, and it is never said in levels 1 to 3. Powers $\mathbf{P}^k$, geometric runs and stationary distributions all rest on it. | Grimmett and Stirzaker 6.1 define the Markov property and homogeneity separately; Norris 1.1 builds the fixed matrix into the definition. | Insert as the second sentence of the prose: "The arrows are the same on every day."

6. l3-never-leave.json | `screens[4].prose` | imprecise | minor | "A group of states that all communicate is a **communicating class**." By this wording $\{D\}$ alone is a class, yet the item marks it wrong. A class is the largest such group. | Communicating classes are the equivalence classes of "each reaches the other" (Norris 1.2). | "Two states **communicate** if each can reach the other. A **communicating class** is a group of states that all communicate, together with every state that communicates with them."

7. l3-never-leave.json | `screens[3].feedback.byKey.D`, `screens[3].feedback.byKey.E` | imprecise | minor | "From D the chain goes only to E, and E sends it back." D keeps the chain with chance 0.6 and E with 0.3, so neither "goes only" to the other. The conclusion is right. | Arrows: D to D 0.6, D to E 0.4, E to D 0.7, E to E 0.3. | `D`: "From D the chain can only stay or move to E, and E can only stay or move back. It returns to D with chance 1, so D is recurrent." `E`: "From E the chain can only stay or move to D, and D can only stay or move back. It returns to E with chance 1, so E is recurrent."

8. l6-always-settle.json | `screens[4].explain.text` | imprecise | minor | "A set the chain never leaves is a **closed class**." A closed set need not be a class: $\{A, B, C, D\}$ is never left either. Level 1 defined a closed class correctly. | Norris 1.2. | Replace the second sentence with: "A and B reach each other and the chain never leaves them, so they form a **closed class**."

9. l9-coin-flip-walk.json | `screens[6].explain.text` | imprecise | minor | "The variance needs independence, so that the covariance terms vanish." Sufficient, not necessary: zero covariances are enough. | $\operatorname{Var}(\sum X_i) = \sum \operatorname{Var}(X_i) + 2\sum_{i<j}\operatorname{Cov}(X_i, X_j)$. Script: $X_1, X_2$ fair and $X_3 = X_1 X_2$ are dependent with variance of the sum 3. Check "FINDING l9 s6" fails on purpose. | "The variance uses independence, which makes every covariance term zero. Uncorrelated steps would be enough."

10. l11-reflection.json | `screens[3].explain.text` | imprecise | minor | "In general: paths to $(n, k)$ touching $m$ number $\binom{n}{(n + 2m - k)/2}$." True only for an end at or below the level. For $k > m$ every path touches. The lesson's own quiz 2 treats the misuse as a slip. | $n = 6$, $k = 4$, $m = 2$: all 6 paths touch, the formula gives 20 (script, check "FINDING l11 s3", failing on purpose). Feller vol. 1, III.1. | Replace "In general:" with "For an end at or below the level, $k \\le m$:".

11. l12-price-paths.json | `screens[3].prose` | imprecise | minor | "If they are independent with mean $\mu$ and sd $\sigma$, the central limit theorem gives..." The classical theorem also needs identical distributions (or a Lindeberg condition). | Casella and Berger Thm 5.5.14. | "If they are independent and identically distributed with mean $\\mu$ and sd $\\sigma$, the central limit theorem gives".

12. l12-price-paths.json | `quiz[2].explain.text` | imprecise | minor | "a path with $k$ ups ends at $100 \times 1.1^{2k - 5}$". The item gives no starting price. | Read of the prose. | "a path with $k$ ups ends at the starting price times $1.1^{2k - 5}$, whatever the order."

13. l10-gamblers-ruin.json | `screens[5].explain.text` | imprecise | minor | "Bet big when the odds are against you, small when they are for you." True for reaching a fixed target with even-money bets; stated as a general rule. | Bold play is optimal for a subfair even-money game with a target (Dubins and Savage); the screen's own numbers (0.49 against 0.1192; 0.8808 against 0.51) are for that goal. | "To reach a fixed target, bet big when the odds are against you and small when they are for you."

14. review-2.json | `items[3].explain.text` | imprecise | minor | "The limit depends on the start because the chain is reducible." Same inference as finding 1: the cause is two closed classes. | As finding 1. | "The limit depends on the start because the chain has two closed classes."

15. homework-2.json | `items[7].feedback.byKey.eight` | imprecise | minor | "8 is $1/P(\text{HTH}) = 2^3$, as if each block of three days were a fresh trial." Block trials would take $3 \times 8 = 24$ days. 8 is the mean wait for one event of chance $\tfrac18$ tried daily. | Arithmetic; script check "FINDING hw2 HTH feedback" fails on purpose. | "8 is $1/P(\\text{HTH}) = 2^3$, the wait for a single event of chance $\\tfrac18$ tried once a day. The pattern needs three days in a row, and overlapping windows are not independent trials."

## Misleading, minor

16. problems-1.json | `items[3].parts[4].explain.text` | misleading | minor | The rule "run the trade next month only when this month is calm" is shown to beat always-on by £0.67m a month. The arithmetic is right, but it assumes each month's regime is known as the month ends. Regimes are inferred from data, late and with error, and the item does not say so. This is the point at which a learner meets "use the regime to time the trade". | Hamilton, *Time Series Analysis*, 22.4: the regime is unobserved and only filtered probabilities are available in real time. | Replace the last sentence with: "That beats £1.43m by about 0.67, but only if each month's regime is known as the month ends; real regimes are estimated late and with error."

## Gates

- `node tools/validate.mjs`: see the lines under "Gate results" below.
- Number scripts and the concepts script: exit codes under "Gate results".

## Overlap with earlier reviews

Filled after the WIP commit (see below).
