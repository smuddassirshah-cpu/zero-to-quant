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

## Fix pass

Fixer: Opus, 11 Nov 2026. Seven files changed: `l5`, `l6`, `l7`, `l8`, `l12`, `review-2`, `homework-2`. No key, option, slip value, test or code changed; prose, explain, feedback and summary strings only.

1. fixed. Basis: $(w\sigma_X + (1-w)\sigma_Y)^2 - \operatorname{Var}(P) = 2w(1-w)\sigma_X\sigma_Y(1-\rho)$, positive only when $0 < w < 1$; recomputed the lesson's own short mix ($w = -0.27$, $\rho = 0.8$): sd 7.89% against a weighted average of 4.6%. The three pastes applied as proposed; the ideas line now says "weighted average", which the sentence needs once weights are named.
2. fixed. Basis: the weak law bounds the chance of a large gap, not the gap on each run (Blitzstein and Hwang 10.2); a single seeded path can and does widen. Paste applied.
3. fixed. Basis: Ross 4.3 and Blitzstein and Hwang 4.1 require $\sum |x| P(X=x) < \infty$ for countably many values; every variable in these levels is finite, and the uncapped game in `homework-2` is the counterexample. Paste applied.
4. fixed. Basis: $P(\text{up, up}) = P(\text{up})P(\text{up} \mid \text{up})$, which is 0.16 only under an added assumption; "independently of the day before" is stated as the model's assumption, enough for the key (0.16 × £100 = £16, as only up, up ends above £102), not claimed as necessary.
5. fixed. Basis: as 4; under the stated independence $0.25 \times (60.5 - 50) = 2.625$.
6. fixed. Basis: $P(B_i = B_j) = \sum_d P(B_i = d)P(B_j = d) = 1/365$ under independence of uniform birthdays; independence is the stated model assumption that the key and the 0.5073 slip need.
7. fixed. Basis: as 6, for $n$ people.
8. fixed differently. Basis: read `multivar/l12-min-variance.json`: the general formula comes "from one derivative" after substituting $w_2 = 1 - w_1$, and a separate screen shows "a multiplier on $w_1 + w_2 = 1$ gives the same weights". New sentence: "The minimum variance portfolio lesson in Multivariable Calculus reaches the same weight by substitution and with a Lagrange multiplier." It names both methods that lesson uses and drops the lesson number.
9. fixed differently. Basis: the proposed "guaranteed only for independent variables" repeats the necessary-condition error, since $E[XY] = E[X]E[Y]$ holds exactly when $X$ and $Y$ are uncorrelated. New line: "Independence would make that product rule safe, but $X$ is not independent of itself." For the die the gap is $\tfrac{91}{6} - \tfrac{49}{4} = \tfrac{35}{12} \ne 0$.
10. fixed. Basis: the model answer and rubric give $40 \times \tfrac{1}{40} = 1$, an expected count; the prompt now asks for that quantity. Paste applied.

Lessons cited by number (inbox bullet): the five strings replaced by titles. `l8` `screens[2].question`, `screens[7].explain` and `screens[8].explain` now cite "the long-run average lesson" (`l5` holds the indicator edge case); `homework-2` `items[3].explain` cites "the fair price lesson" (`l6` holds $E[X - c] = E[X] - c$); `l12` `screens[7].prose` under finding 8. Number citations in levels 4 and 5 (`l17` to `l20`) were left for the agent editing those levels.

Gates: validator 0 errors, 4864 warnings; `random-vars-L1-3-concepts-r2.py`, `random-vars-L1-3-concepts.py`, `random-vars-L1-3-fixread.py`, `random-vars-1-perf-numbers.py`, `problems-random-vars-numbers.py`, `fluency-random-vars-numbers.py` all exit 0 (no check needed updating); voice scan 35: 0 sentences over, 0 explanations over three sentences; playthrough of the seven changed files, desktop and `--mobile`: all passed.

## Fix-pass read

Fresh Fable reader, blind to the audit above until these rows were written (the last 600 bytes of this file, the fix pass's gate lines, were seen when locating the append point, after every verdict below was formed). Diff read: `git diff 059e5143^..059e5143 -- app/content/courses/random-vars/`, 16 changed strings in seven files, no key, option or slip value changed.

| # | File | JSON path | Claim (new text) | Verdict | Basis |
|---|---|---|---|---|---|
| 1 | homework-2 | `items[2].prose` | Each birthday uniform on 365 days, independently of the others; $N$ counts sharing pairs. | correct | Under the stated model $P(\text{pair shares}) = 365 \cdot (1/365)^2 = 1/365$, so $E[N] = \binom{n}{2}/365 = (n^2-n)/730$, the key; at 23, $253/365 = 0.6932$. Independence is sufficient for the pair chance and the item does not call it necessary. |
| 2 | homework-2 | `items[3].explain.text` | $a = 1$, $b = -c$ gives the pricing rule from the fair price lesson, $E[X - c] = E[X] - c$. | correct | Substitution in $E[aX+b] = aE[X]+b$. Reference checked: `l6-fair-price` is titled "A fair price for a bet" and derives $E[X - c] = \sum_x (x - c)P(X = x)$. |
| 3 | homework-2 | `items[10].prompt` part 4 | "What is the expected number of traders who keep their own account?" | correct | Now asks for $E[N]$, which the model answers: $40 \times 1/40 = 1$ (fixed points of a uniform permutation, Feller vol. 1, IV.4). |
| 4 | l12-diversification | `screens[5].explain.text` | Variance $0.0225 + 0.0025 + 0.003 = 0.028$, sd 16.73%; below $\rho = 1$ a mix with both weights positive is always safer than that average. | correct | $0.25 \cdot 0.09$, $0.25 \cdot 0.01$, $2 \cdot 0.25 \cdot 0.2 \cdot 0.03$; $\sqrt{0.028} = 0.16733$. $(w\sigma_X + (1-w)\sigma_Y)^2 - \sigma_p^2 = 2w(1-w)(1-\rho)\sigma_X\sigma_Y > 0$ for $0 < w < 1$, $\rho < 1$, positive sds. |
| 5 | l12-diversification | `screens[7].prose` | $w^*$ formula; the minimum variance portfolio lesson in Multivariable Calculus reaches the same weight by substitution and with a Lagrange multiplier. | correct | $\tfrac{d}{dw}$ of the variance is $2w\sigma_X^2 - 2(1-w)\sigma_Y^2 + 2(1-2w)\rho\sigma_X\sigma_Y$; zero at the stated $w^*$. Key: $0.0075/0.055 = 0.13636$. Reference checked: `multivar/l12-min-variance` ("The minimum variance portfolio", course name "Multivariable Calculus") has screens "Setting the slope to zero" and "The same answer with a multiplier" and states the same formula for $w_1^*$. |
| 6 | l12-diversification | `summary.ideas[1]` | Both weights positive and $\rho < 1$: mix sd below the weighted average of the sds; at $\rho = -1$ it can be riskless. | correct | Identity in row 4. At $\rho = -1$, $\sigma_p = \lvert w\sigma_X - (1-w)\sigma_Y \rvert$, zero at $w = \sigma_Y/(\sigma_X + \sigma_Y)$. |
| 7 | l12-diversification | `summary.trap` | For a mix with both weights positive, averaging the sds is right only at $\rho = 1$. | correct | Row 4 identity: equality iff $\rho = 1$ when $w(1-w)\sigma_X\sigma_Y > 0$. Agrees with `screens[5].feedback.byKey.avg` and with the short-selling remark in `screens[7].explain`. |
| 8 | l5-long-run-average | `screens[7].prose` | For a discrete random variable with finitely many values, $E[X] = \sum_x x\,P(X = x)$. | correct | Definition (Casella and Berger, Def. 2.2.1); the finite restriction removes the absolute-convergence hypothesis. No variable with infinitely many values appears in l5 to l8 (searched), so no neighbour contradicts it. |
| 9 | l5-long-run-average | `screens[8].explain.text` | Simulation gave 3.50167; more draws tend to shrink the gap, though not at every step. | correct | Reran `random.Random(1).choices(..., k=100000)`: mean 3.50167. LLN: the error has sd $\sigma/\sqrt{n}$, and the running mean's error is not monotone. |
| 10 | l6-fair-price | `screens[9].prose` | Daily moves $+2$, flat, $-2$ with chances 0.4, 0.4, 0.2, independently of the day before. | correct | Independence is the hypothesis the tree's product $0.4 \times 0.4 = 0.16$ needs; only up, up ends above £102, so the price is £16, the key. |
| 11 | l7-linearity | `screens[6].feedback.byKey.squared` | Independence would make the product rule safe, but $X$ is not independent of itself. | correct | Independence is stated as sufficient, not necessary. $X$ is independent of itself only if it is almost surely constant; a die is not. $E[X^2] = 91/6$ against $12.25$. Agrees with the screen's explain. |
| 12 | l8-indicators | `screens[2].question` | Each $E[I_k] = \tfrac{1}{6}$, as in the long-run average lesson. | correct | `l5-long-run-average` ("The long-run average") has $E[I] = 0 \cdot \tfrac{5}{6} + 1 \cdot \tfrac{1}{6} = \tfrac{1}{6}$. Key $10/6 = 1.6667$. |
| 13 | l8-indicators | `screens[5].prose` | 23 people, each birthday uniform on 365 days, independently of the others. | correct | As row 1: $\binom{23}{2}/365 = 253/365 = 0.69315$, the key. Slip `at-least-one` 0.5073 is $1 - \prod_{k<23}(1 - k/365)$, which also needs the independence now stated. |
| 14 | l8-indicators | `screens[7].explain.text` | $E[I_k] = P(A_k)$, the edge case from the long-run average lesson. | correct | Two-point pmf. l5 calls it "that edge case" in the same words. |
| 15 | l8-indicators | `screens[8].explain.text` | Line 2 is linearity with no independence asked; line 3 is the fact from the long-run average lesson that an indicator's expected value is its chance. | correct | Linearity holds for any jointly defined variables with finite means (Casella and Berger, Thm 4.5.3 form for sums). Reference as row 12. |
| 16 | review-2 | `items[8].prose` | Stock at £50, up or down 10% with equal chance, independently of the day before; call struck at £50 after two days. | correct | Leaves 60.50, 49.50, 49.50, 40.50; with independence up, up has chance 0.25, payoff 10.50, price 2.625, the key. |

Count: 16 rows; 16 correct, 0 wrong, 0 imprecise, 0 misleading, 0 unverified. No replacement text needed. No lesson is cited by number in any changed string.
