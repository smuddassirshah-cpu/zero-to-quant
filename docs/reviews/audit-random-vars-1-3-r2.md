# Concept audit, round 2 (blind): random-vars levels 1 to 3

Reader: Fable, 11 Nov 2026, blind to the round 1 audit (`audit-random-vars-1-3.md`), its ledger, its concepts and fix-read scripts and every earlier review until the ledger and the findings below were committed (commit "WIP"). Scope: lessons l1 to l12, `review-1` to `review-3`, `homework-1` to `homework-3`, `problems-1` to `problems-3`, `fluency-l9-measuring-spread.json`. Stage 1, full ledger.

- Ledger: `docs/reports/audit-random-vars-1-3-r2-ledger.md`, 342 rows: correct 330, imprecise 11, misleading 1, wrong 0, unverified 0.
- Script: `docs/reports/random-vars-L1-3-concepts-r2.py`, 173 checks (exact recomputation of keys and slip values, the engine's seeded explore runs reproduced, Monte Carlo for each empirical claim), exit 0.

## Verdict

No claim in scope is false as stated. Every graded key, every `wrong[]` value and every slip line recomputes under the reading the item gives. Ten findings, all minor: nine `imprecise` (a hypothesis left unstated or a finite-sample statement worded as certain) and one `misleading` wording. None changes a graded answer.

## Findings

1. `l12-diversification.json` | `summary.ideas[1]`, `screens[5].explain.text` (third sentence), `summary.trap` | imprecise | minor | "Below $\rho = 1$ the mix is safer than the average of the sds" is stated without the condition that both weights are positive. The same lesson teaches a short weight on the screen before. | For $0 < w < 1$, $\rho < 1$ and positive sds, $(w\sigma_X + (1-w)\sigma_Y)^2 - \operatorname{Var}(P) = 2w(1-w)\sigma_X\sigma_Y(1-\rho) > 0$. With $w < 0$ the factor $w(1-w)$ is negative and the inequality reverses: at $w = -0.27$, $\rho = 0.8$, sds 30% and 10%, the sd is 7.89% and the weighted average of sds is 4.6% (script note). | Paste: `summary.ideas[1]`: "With both weights positive and $\rho$ below 1, the mix's sd is below the weighted average of the sds; at $\rho = -1$ it can be riskless." `screens[5].explain.text`, third sentence: "Below 1, a mix with both weights positive is always safer than that average." `summary.trap`: "For a mix with both weights positive, averaging the sds is right only at $\rho = 1$, where mixing gives no benefit at all."

2. `l5-long-run-average.json` | `screens[8].explain.text` (third sentence) | imprecise | minor | "More draws shrink that gap" reads as certain. It holds for the typical gap, not for each longer run. | The root-mean-square gap falls like $1/\sqrt{n}$ (script Monte Carlo: ratio near 4 between 100 and 1,600 rolls). With the lesson's own `simulate` and seed 1 the gap is 0.00167 at 100,000 draws and 0.00325 at 200,000 (script note). Law of large numbers, Blitzstein and Hwang section 10.2. | Paste, third sentence: "More draws tend to shrink that gap, though not at every step; the exact sum needs no draws."

3. `l5-long-run-average.json` | `screens[7].prose` | imprecise | minor | "For any discrete random variable $X$" states the sum formula without the condition that the sum converges. `homework-2` `items[4]` then shows a case, the uncapped game, where it does not. | Blitzstein and Hwang section 4.1 and Ross section 4.3 define $E[X]$ for countably many values only when $\sum_x |x|\,P(X = x)$ is finite. Every variable in levels 1 to 3 has finitely many values, so restricting the sentence loses nothing. | Paste: "Every time, you multiplied each value by its chance and added. For a discrete random variable $X$ with finitely many values, $$E[X] = \sum_x x\,P(X = x).$$ The sum runs over every value $X$ can take."

4. `l6-fair-price.json` | `screens[9].prose` | imprecise | minor | The key (£16) and the hint multiply $0.4 \times 0.4$, which needs the two days independent. The prose does not say so; only the tree's repeated branch labels imply it. | $P(\text{up, up}) = P(\text{up}) P(\text{up} \mid \text{up})$; this is 0.16 only if day 2 does not depend on day 1. The sibling items state it (`l2` `screens[8]`, `homework-1` `items[4]`, `problems-2` `items[1]`). | Paste: "A stock is at £100. Each day it rises £2 with chance 0.4, stays flat with chance 0.4, or falls £2 with chance 0.2, independently of the day before. A binary option pays £100 if the price after two days is above £102."

5. `review-2.json` | `items[8].prose` | imprecise | minor | Same class as finding 4: the key 2.625 uses $0.5 \times 0.5$ and independence of the days is not stated. | As finding 4. | Paste: "A stock is at £50. Each day it rises 10% or falls 10%, with equal chance, independently of the day before. A call option pays the price minus £50 after two days, or nothing if that is negative."

6. `l8-indicators.json` | `screens[5].prose` | imprecise | minor | "Birthdays spread evenly over 365 days" gives each person a uniform birthday. The key needs more: a pair shares with chance $\tfrac{1}{365}$ only if the two birthdays are independent, and the slip value 0.5073 needs all 23 independent. | $P(B_i = B_j) = \sum_d P(B_i = d, B_j = d)$, which is $\tfrac{1}{365}$ under independence and 1 for twins. Class: independence dropped where needed. | Paste: "A room holds 23 people. Each birthday is equally likely to be any of 365 days, independently of the others. Each pair of people gets an indicator: 1 if they share a birthday."

7. `homework-2.json` | `items[2].prose` | imprecise | minor | Same as finding 6 for $n$ people. | As finding 6. | Paste: "A room holds $n$ people. Each birthday is equally likely to be any of 365 days, independently of the others. Let $N$ be the number of pairs who share a birthday."

8. `l12-diversification.json` | `screens[7].prose` (last sentence) | imprecise | minor | "Multivariable calculus, lesson 12, derived it with a Lagrange multiplier." That lesson (`multivar/l12-min-variance`) solves one numeric portfolio with a multiplier and derives the general formula by substituting $w_2 = 1 - w_1$ and taking one derivative ("The formula, from one derivative"). The sentence also cites a lesson by number. | Read of `multivar/l12-min-variance.json`: objectives and the derive screen's feedback. | Paste, last sentence: "The minimum variance portfolio lesson in Multivariable Calculus finds this weight with a Lagrange multiplier too."

9. `l7-linearity.json` | `screens[6].feedback.byKey.squared` | imprecise | minor | "That product rule fails here, because $X$ depends completely on itself." Dependence does not make the rule fail; it only removes the guarantee. The course's own pair $X \in \{-1, 0, 1\}$, $Y = X^2$ (`l11` `screens[7]`) is fully dependent and still has $E[XY] = E[X]E[Y]$. | $E[X^2] - E[X]^2 = \operatorname{Var}(X) = \tfrac{35}{12} > 0$ is why it fails for the die. The explain text of the same screen words it correctly ("can fail without independence"). | Paste: "You assumed $E[X \cdot X] = E[X] \cdot E[X]$. That product rule is guaranteed only for independent variables, and $X$ is not independent of itself."

10. `homework-2.json` | `items[10].prompt` (part 4) | misleading | minor | "How many traders expect to keep their own account?" Read literally the answer is none: each trader keeps it with chance $\tfrac{1}{40}$. The model answer and rubric give the expected number of traders, 1. | Model text part 4: "the expected number is $40 \times \tfrac{1}{40} = 1$". The slip between "how many expect" and "expected how many" is the values-against-outcomes confusion the course trains against. | Paste, part 4: "4. A desk reassigns 40 client accounts among its 40 traders at random, one each. What is the expected number of traders who keep their own account?"

## Checked and found sound (classes the brief names)

- Independence as sufficient, not necessary: `l7` summary and `screens[7]`, `l10` `screens[8]` and summary, `l11` `screens[7]` and summary, `review-3` `items[5]` all word it as sufficient only.
- Linearity without independence: every use (`l7`, `l8`, `review-2`, `homework-2`, `problems-2`) is on dependent variables correctly; `problems-2` `items[1]` part 3's option "one reversal makes the next more likely" is true (0.5 against 0.48, script) and its feedback does not deny it.
- Conventions: $F(x) = P(X \le x)$ with the closed dot stated at `l3` `screens[2]`; VaR as the smallest $x$ with $F(x) \ge 0.95$ stated wherever it is keyed; 252 trading days stated at `l10` `screens[9]`; variance of a pmf is the population form throughout, and no estimator is presented.
- Code: `expectation`, `variance` and `pmf_of` teach the definitions; the two printed outputs (3.50167 and 2.9207) and both float totals quoted in `homework-1` `items[8]` feedback reproduce.
- Seeded explore screens: the engine's generator was reproduced; `l6` `screens[1]` shows 167 sevens in 1,000, `l8` `screens[1]` an average of 1.662, `l7` `screens[1]` averages 7.00 and 6.99, matching the explain texts.
- Cross-references: "Correlated defaults" exists in Conditional Probability; the 0.5073 birthday value is the Counting and Chance figure.

## Gates

- `node tools/validate.mjs 2>&1 | tail -5` (from `app/`): 0 errors, 4863 warnings.
- `python3 docs/reports/random-vars-L1-3-concepts-r2.py`: 173 checks, 0 failed, exit 0.
- Course number scripts: `random-vars-1-perf-numbers.py` exit 0, `problems-random-vars-numbers.py` exit 0, `fluency-random-vars-numbers.py` exit 0. No `random-vars-L1..L3-numbers.py` exists in `docs/reports/`.
- Round 1 scripts, run after the blind commit: `random-vars-L1-3-concepts.py` exit 0, `random-vars-L1-3-fixread.py` exit 0.
- Playthrough: not run; no grading defect is suspected.

## Overlap with earlier reads

Read after the blind commit `f7df39f2`: `docs/reviews/audit-random-vars-1-3.md` (round 1 findings, fix pass, fix-pass read and follow-up), `docs/reviews/review-1.5.md` (random-vars section and fix pass) and `docs/reviews/review-problems-1.5-a.md` to `-d.md` (searched for each of this round's ten findings). Only conceptual findings on levels 1 to 3 are counted.

| Finding | This round | Earlier read |
|---|---|---|
| l12 summary and `screens[5]`: mix below the average of sds, no positive-weights condition | 1 | seen by round 1 and listed under "Notes that are not findings" (read for weights between 0 and 1); not raised |
| l5 `screens[8]`: "more draws shrink that gap" | 2 | not found |
| l5 `screens[7]`: "for any discrete random variable" | 3 | not found (round 1 noted that every variable in scope is finite) |
| l6 `screens[9]`: days not said to be independent | 4 | not found |
| review-2 `items[8]`: the same | 5 | not found |
| l8 `screens[5]`: birthdays not said to be independent | 6 | not found |
| homework-2 `items[2]`: the same | 7 | not found |
| l12 `screens[7]`: "derived it with a Lagrange multiplier" | 8 | seen by round 1 and noted as sound ("exists and contains it"); the formula there comes from one derivative |
| l7 `screens[6]` slip line: "fails here, because X depends completely on itself" | 9 | not found (round 1 findings 2 and 3 fixed five sibling strings of this class; this one was left) |
| homework-2 `items[10]` part 4: "how many traders expect" | 10 | not found |
| Round 1 audit findings 1 to 10 (two `wrong`: l7 `screens[2]`, l7 `quiz[2]` with homework-2 `items[6]`) | not found: fixed before this read; each fixed string is a `correct` row in this ledger | audit round 1 |
| Round 1 fix-pass read: l10 `screens[9]` conditions of the √252 rule; l3 `screens[10]` "worst 5%" | not found: fixed; both strings are `correct` rows here | fix-pass read |
| review-1.5 and review-problems-1.5: l6 `one-up` slip, l11 `count` slip, homework-2 overround, problems-3 % unit, problems-2 `carried` slip | not found: fixed; each value recomputed in the script | reviews |

Counts: this round only 10; earlier reads only 17 (10 from the round 1 audit, 2 from its fix-pass read, 5 from the reviews); both 0. Two of the ten (1 and 8) were looked at by round 1 and judged not findings, so eight are new to every earlier read.

New `wrong` findings that no earlier read found: **0**. There is no `wrong` in this round, so none sits on original text and none on fix-pass text. All ten findings are on original text: none of the 17 strings changed by the fix pass and its follow-up (`git diff d67c2d45~1 44205fb1`, eight files) is a finding path. Those 17 strings were each read again here as ledger rows and are `correct`.

On the convergence rule (at most one new `wrong` per three levels): this round meets it with zero.

One round 1 note is worth keeping in view and is not raised here either: homework-3 `items[6]` part (d) asks for the sd "if $\rho$ were 1", which these two-point marginals cannot reach; it is sound as a formula exercise.

## Inbox

Two bullets appended to `docs/BACKLOG-INBOX.md` under "Raised later (audit random-vars, round 2):": a content lint for multi-step chances multiplied without "independent" in the prose (findings 4 to 7), and one for lessons cited by number (five strings in levels 1 to 3).
