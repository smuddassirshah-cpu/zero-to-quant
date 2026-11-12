# Concept audit: random-vars levels 4 and 5 (round 1, blind)

Scope: `l13` to `l20`, `review-4`, `review-5`, `homework-4`, `homework-5`, `problems-4`, `problems-5` in `app/content/courses/random-vars/`. No fluency file belongs to these levels. Stage 1, full ledger. Read blind: no earlier review, author report or audit of this course was opened before the ledger and the findings below were committed.

Ledger: `docs/reports/audit-random-vars-4-5-ledger.md`, 371 rows: 343 correct, 3 wrong, 25 imprecise, 0 misleading, 0 unverified.
Script: `docs/reports/random-vars-L4-5-concepts.py`, 81 checks. It exits 1 now: five checks are tied to sentences that are false as written (findings 2, 8 twice, 15, 16) and pass once those sentences are changed.

## Summary

19 findings: 3 wrong (all minor), 16 imprecise (1 serious, 15 minor), 0 misleading.

Every graded key, every `wrong[]` value and every slip was recomputed and is right under the item's stated convention. No key depends on an unstated convention except the two items in findings 4 and 9, where independence is left out of the prompt. All three code tasks teach a right method, their starters fail, and every printed figure (`1.99834`, `6.03976`, `5.03602`, `18466.21`, `120.21`, `22822.56`, `99.66`, `18248.28`) matches what the taught code prints.

The class named in the brief does appear. Independence is stated as necessary where it is only sufficient in findings 6, 8 and 19, and dropped where it is needed in findings 4 and 9.

## Findings

Pattern: `N. file | JSON path | severity | serious or minor | problem | evidence and basis | exact fix`.

1. `l13-joint-tables.json` | `screens[8].explain.text` | imprecise | minor | "You met this table as Bayes on a trading signal in Conditional Probability." The table is new. | `conditional/l26-trading-signal.json` gives a signal that flashes before 60% of up days and 40% of down days, with up and down equally common. Here $P(\text{fires} \mid \text{up}) = 0.23$ and $P(\text{up} \mid \text{fires}) = 0.60$. Same method, different numbers. | Replace the last sentence with: `You met this turn-around as Bayes on a trading signal in Conditional Probability.`

2. `l14-independent-rvs.json` | `screens[5].explain.text` | wrong | minor | "A default in one pool makes two in the other likelier." False for one default. | From the table, $P(Y = 2 \mid X = 1) = 0.01/0.30 = 0.033$, below the 0.10 overall. $P(Y = 2 \mid X \ge 1) = 0.05/0.50 = 0.10$, exactly the overall chance. Only $X = 2$ lifts it, and that is the case the sentence then quotes. Script check `l14 s5`. | `Four cells fail: $(1, 1)$, $(1, 2)$, $(2, 1)$ and $(2, 2)$. Two defaults in one pool make two in the other likelier: $P(Y = 2 \mid X = 2) = 0.04 / 0.20 = 0.20$, against 0.10 overall. Checking the first row or the margins would miss all of this.`

3. `l14-independent-rvs.json` | `summary.formula.note`, `summary.trap` | imprecise | minor | "Matching margins, or one matching cell, prove nothing" and "Checking one cell, or the margins, is not a test" are false for a 2 by 2 table. The lesson's own `screens[10]` and `quiz[0]` are 2 by 2. | With margins $r$ and $c$, if the cell $a = rc$ then the others are $r - a = r(1 - c)$, $c - a = (1 - r)c$ and $(1 - r)(1 - c)$. One matching cell forces all four. Script check `2x2`. For larger tables the claim holds (the loan pools). | `summary.formula.note`: `Check every cell. Matching margins prove nothing, and beyond a 2 by 2 table neither does one matching cell.` `summary.trap`: `Checking the margins is not a test, and beyond 2 by 2 nor is checking one cell. Two tables with the same margins can differ inside.`

4. `l16-averaging-averages.json` | `summary.ideas[2]`; `l20-many-categories.json` | `quiz[2].prose` | imprecise | minor | Independence dropped where it is needed. "Trials that each succeed with chance $p$ take $1/p$ on average"; and a negative binomial key on "Each trial succeeds with chance 0.5". | The first-step proof in `l16` `screens[7]` uses a fresh copy after a failure, which is independence. If all trials share one outcome, each still succeeds with chance $p$, but the wait is 1 or never ends. Ross, *First Course*, 7.5. | `l16` `summary.ideas[2]`: `Independent trials that each succeed with chance $p$ take $1/p$ trials on average: 2 tosses for a head, 6 rolls for a six, 5 minutes for a fill at 0.2.` `l20` `quiz[2].prose`: `Independent trials each succeed with chance 0.5. $T$ is the trial of the second success.`

5. `l17-variance-given-information.json` | `screens[10].explain.text`; `homework-5.json` | `items[7].model` (Step 5) | imprecise | minor | "a mixture has fatter tails than either regime." The comparison has no clear meaning and is false on the natural reading. | With normal regimes, the mixture's chance of a day below −£480 is $0.2 \times 0.159 + 0.8 \times 10^{-9} = 0.032$, against 0.159 for the volatile regime alone. What is true: the mixture's kurtosis (7.5 here) is above a normal's 3. Script check `mixture`. | `l17`: `$14{,}400 / 40{,}400 = 0.356$. With calm sd £100, a −£480 day is 6 sds below the calm mean. It is only one sd below the volatile mean, so a model fitted on calm days alone badly understates such days.` `homework-5` Step 5, last sentence: `Such a mixture usually has fatter tails than one normal with the same 7% sd, which pulls the typical outcome down further.`

6. `l17-variance-given-information.json` | `quiz[2].widget.options[1].why` | imprecise | minor | "That holds only if $X$ tells you nothing about $Y$." Independence stated as necessary. | $E[\mathrm{Var}(Y \mid X)] = \mathrm{Var}(Y)$ exactly when $\mathrm{Var}(E[Y \mid X]) = 0$, a flat conditional mean. The course's own volatility-regime table has a flat mean and dependent variables. Script check `flat conditional mean`. | `That needs $E[Y \mid X]$ to be the same for every value of $X$. Here it is $X^2$, which changes with $X$.` Optional, to close the edge case where $X^2$ is constant and both options are 0: add `$Y$ is not constant.` to `quiz[2].prose`.

7. `l18-random-sums.json` | `screens[3].prose`, `screens[7].explain.text`; `l20-many-categories.json` | `screens[6].prose`; `problems-5.json` | `items[0].parts[3].explain.text`, `items[2].parts[3].explain.text` | imprecise | minor | "Eve's law" and "Adam's law" are used as known names. `l16` and `l17` teach them only as the law of total expectation and the law of total variance. `l18` says "Eve's law from lesson 17", which that lesson never says. | Grep of the course: the two names occur only at these five paths. The names are from Blitzstein and Hwang 9.3 and 9.5. | Either name them once in `l17` `screens[3].prose` (add: `Some books call it Eve's law, and the law of total expectation Adam's law.`), or replace: `l18` `screens[3].prose` first sentence `The law of total variance now applies, with $N$ as the condition.`; `l18` `screens[7].explain.text` first sentence `The law of total expectation gives the mean the same way: $E[S] = E[N\,E[X]] = E[N]E[X]$.`; `l20` `screens[6].prose` `The law of total variance gives $V = 0.6\,V + 1.5$, where 1.5 is the variance of the conditional means 1 and 3.5.`; `problems-5` both paths: `Eve's law` becomes `The law of total variance`.

8. `l18-random-sums.json` | `summary.ideas[2]`, `screens[8].explain.text`, `quiz[2].widget.options[1].why` | imprecise | serious | "If $N$ depends on the fills, the formulas fail", "The formulas also need $N$ independent of the fills" and "They fail only if the count and the fills are linked." The summary states the converse of the theorem as a rule. | Independence is the hypothesis of the proof, not a condition the result needs. Wald's identity: for $N$ = the trade of the first £35 fill, $N$ depends on the fills, yet $E[S] = E[N]E[X] = 10$ (script MC), though the variance formula does fail there (1,250 against 1,850). If only the shape of a fill changes with $N$, with mean and variance unchanged, both formulas hold (script MC: 100 and 18,500). The "only if" also fails the other way: fills correlated with each other break the variance formula with $N$ independent. Ross 7.5; Blitzstein and Hwang Example 9.6.1. The keyed option of `quiz[2]` is right: worse fills on busy days do change $E[S \mid N]$. | `summary.ideas[2]`: `If the fills average zero the count adds no variance. The formulas assume $N$ is independent of the fills; without that, check before you use them.` `screens[8].explain.text`, last sentence: `The proof also assumed $N$ independent of the fills: if busy days have worse fills, $E[S \mid N]$ is no longer $N\,E[X]$ and the formulas fail.` `quiz[2].widget.options[1].why`: `Random counts are what the formulas are for. What they assume is fills independent of the count and of each other.`

9. `l18-random-sums.json` | `quiz[3].prose` | imprecise | minor | The key £13,115 uses the random-sum formula, but the prompt never says the claims are independent of each other and of the count. `quiz[0]` beside it does. | Same hypothesis as finding 8, here dropped. | `An insurer's claim count has mean 12 and variance 16. Each claim has mean £2,000 and sd £3,000, independent of the other claims and of the count.`

10. `l19-convex-bets.json` | `screens[6].feedback.byKey.equal` | imprecise | minor | "The gap is about $\sigma^2$ over a few times the mean." Wrong form. | Taylor to second order: $\sqrt{\mu} - E[\sqrt{X}] \approx \sigma^2 / (8\mu^{3/2})$. For $X = 1$ or 9 that is 0.18 against an exact 0.24; "$\sigma^2$ over a few times the mean" would give about 1. Script check `root gap`. | `'Nearly linear' is the trap. To second order the gap is $\sigma^2 / (8\mu^{3/2})$: small, never 0.`

11. `l19-convex-bets.json` | `screens[8].prose`, `screens[8].explain.text` | imprecise | minor | The proof uses $g'(\mu)$, so it covers smooth $g$ only. The lesson's own convex example, the call payoff, has a kink exactly at its mean, £100. | A convex function has a supporting line at every interior point, tangent or not (Casella and Berger, proof of Theorem 4.7.7). The hypothesis should be said. | `screens[8].prose`: `Prove Jensen for a smooth convex $g$. Write $\mu = E[X]$. Convexity says the curve lies above its tangent line at $\mu$.` Append to `screens[8].explain.text`: `At a kink, such as a call's strike, any line through that point lying under the curve does the same job.`

12. `l19-convex-bets.json` | `screens[9].feedback.byKey.sign` | imprecise | minor | "This $X$ lives where the cube bends down." $X$ is $-3$ or $1$, and at 1 the cube bends up. | The gap is negative because the chord from $(-3, -27)$ to $(1, 1)$ is at $-13$ over the mean $-1$, below the curve's $-1$. | `You used the convex direction. Here the chord from $-3$ to $1$ passes below the curve at the mean, $-1$.`

13. `l19-convex-bets.json` | `screens[11].explain.text` | imprecise | minor | "Over 120 months that is $e^{0.982} = 2.67$ times your money, not $1.01^{120} = 3.30$." This reads as if 3.30 were wrong. It is the exact expected wealth; 2.67 is the typical path. | With independent months $E[W] = (1.01)^{120} = 3.30$. Script MC over 40,000 paths: median 2.67, mean 3.30. `homework-5` `h-long-fund` makes this distinction correctly, so the two places disagree in tone. | `Exactly 0.818%, close to the second-order approximation $\mu - \sigma^2/2 = 1\% - 0.18\% = 0.82\%$ from the Taylor series. Over 120 months a typical path makes $e^{0.982} = 2.67$ times your money, while the average over all paths is still $1.01^{120} = 3.30$. Kelly, from the Limits course, maximises $E[\ln W]$, not $E[W]$, because only the log counts this drag.`

14. `l19-convex-bets.json` | `summary.ideas[1]` | imprecise | minor | "Equality needs $X$ constant." True only for a curve with no straight stretch. | The call payoff of `screens[5]` is convex, and $E[(X - 100)^+] = (E[X] - 100)^+$ for any $X$ that stays on one side of 100. `quiz[0]` already says "or a straight-line $g$". | `For a curve with no straight stretch, equality needs $X$ constant. The gap for $x^2$ is the variance, and for $\ln(1 + R)$ it is about $\sigma^2/2$: volatility drag.`

15. `l19-convex-bets.json` | `quiz[1].feedback.byKey.sd` | wrong | minor | The slip value 0.5 is answered with "Half the range is not the variance." Half the range of $\{1, 3\}$ is 1, which is the variance here. | $(3 - 1)/2 = 1$; the keyed gap is 1. The feedback tells a learner who typed 0.5 that they typed 1. | `That is not the gap. $E[X^2] = 5$ and $(E[X])^2 = 4$, so compute $5 - 4$.`

16. `l20-many-categories.json` | `screens[2].feedback.byKey.one` | wrong | minor | The slip value 0.0313 is called "the chance of one particular record. Multiply by the 252 ways." | $0.0313 = 0.5^5$. One up or not-up record of ten days has chance $0.5^{10} = 0.00098$, and $252 \times 0.0313 = 7.9$ is not a chance. | `That is $0.5^5$, the chance that five chosen days are all up. The other five must be not up, another $0.5^5$, and there are 252 ways to choose the five.`

17. `l20-many-categories.json` | `screens[4].widget.accept` | imprecise | minor | "$3150 \times 0.0000202$" does not give the key. | $0.5^4 \times 0.2^2 \times 0.3^4 = 0.00002025$. $3150 \times 0.0000202 = 0.0636$; $3150 \times 0.00002025 = 0.0638$. | `0.0638: $\tfrac{10!}{4!\,2!\,4!}(0.5)^4(0.2)^2(0.3)^4 = 3150 \times 0.00002025$`

18. `homework-4.json` | `items[2].explain.text` | imprecise | minor | "Margins never fix the cells." A "never" that fails. | If $X$ is constant, each cell equals $Y$'s margin. | Last sentence: `Margins alone do not fix the cells.`

19. `l20-many-categories.json` | `screens[5].explain.text` | imprecise | minor | "The waits need not be independent for the mean, only for the variance." Independence stated as needed for adding variances. | $\mathrm{Var}(A + B) = \mathrm{Var}(A) + \mathrm{Var}(B) + 2\,\mathrm{Cov}(A, B)$: zero covariance is enough. Level 3 of this course teaches that. | `By linearity $E[T] = 2.5 + 2.5 + 2.5 = 7.5$. The mean needs no independence between the waits; adding their variances, next, will use it.`

## Notes that are not findings

- `problems-5` `p-startup-rounds` parts 2 and 3 key $-0.2108$ and $0.8452$ from rounded inputs; the exact values are $-0.2107$ and $0.8451$. Both bands are 0.0005, so either is accepted.
- `l15` `screens[8]` uses "conditional beta" for a ratio of mean moves at $x = \mp 1$. It matches the practitioner's downside and upside beta closely enough to stand.
- Several strings cite lessons by number ("lesson 15", "lessons 8 and 11", "limits lesson 14"). That is a voice matter, not a concept one; raised as a lint idea in the inbox.

## Gates

- `node tools/validate.mjs 2>&1 | tail -5`: 0 errors, 4863 warnings.
- `python3 docs/reports/problems-random-vars-numbers.py`: exit 0, 1333 checks, 0 failures (needs `sympy`, which was missing and was installed with pip).
- `python3 docs/reports/fluency-random-vars-numbers.py`: exit 0, 1767 checks (also needs `sympy`).
- `python3 docs/reports/random-vars-1-perf-numbers.py`: exit 0, 109 checks.
- `python3 docs/reports/random-vars-L1-3-concepts.py`: exit 0. `random-vars-L1-3-fixread.py`: exit 0.
- `python3 docs/reports/random-vars-L4-5-concepts.py`: exit 1, 81 checks, 5 failing by design (findings 2, 8 summary, 8 quiz option, 15, 16).
- No number script for the lessons, reviews or homework of levels 4 and 5 was found under `docs/reports/`; the concepts script recomputes their keys.
- No playthrough was run: no grading defect is suspected.

## Overlap with earlier reads

Earlier reads of this scope: `docs/reviews/review-1.5.md` (level 4 lessons, review and homework; findings 71 to 80 with fix pass 57 to 66), `docs/reviews/review-problems-1.5-d.md` section A (problem sets 4 and 5; findings 9 to 11) and `docs/reviews/review-delta-session-aa.md` (finding 10). Level 5's lessons, review and homework had an author report (`docs/reports/random-vars-5.md`) but no second-reader review, so this audit is their first independent read.

| | count |
|---|---|
| Conceptual findings found by this audit only | 19 |
| Found by the earlier reviews only | 3 |
| Found by both | 0 |

The three found only by the earlier reviews are slip values that did not match their feedback: `l14` `screens[6]` `var` (4/9 called a variance), `l16` `screens[4]` `third` (4/3 against a why that gives 1) and `problems-5` `p-startup-rounds` `count-squared` (3.3584 against 3.3640). All three were fixed before this read, and the fixed values recompute correctly here. The earlier reviews' other lines on this scope are voice, sentence length and part-chaining notes, which are not counted.

Two points on fix-pass text:

- Finding 1's sentence was written by the review-1.5 fix pass (its line 57). The fix cured the course order and left the claim that the table is the same one.
- Findings 15 and 16 are the same class as the earlier `var` and `third` findings (a slip whose feedback names a quantity the value does not equal). That class has now been seen four times in this course; an inbox bullet proposes a script check.

## Inbox

Four bullets appended to `docs/BACKLOG-INBOX.md` under `Raised later (audit random-vars):` a slip-value against named-quantity check, a lint for lessons cited by number, a named-law introduction check, and the `sympy` dependency of two number scripts.

## Fix pass

Fixer: Opus, round 1. Content edits only, levels 4 and 5 files. No key, answer, option id, slip value, test or code changed; one `accept` display string changed (finding 17).

1. fixed. Basis: `l13` table gives $P(\text{up} \mid \text{fires}) = 0.12/0.20 = 0.60$ and $P(\text{fires} \mid \text{up}) = 0.12/0.52 = 0.23$; the Conditional Probability signal has $P(\text{flash} \mid \text{up}) = 0.60$, a different table. Now "the same turn-around, with other numbers".
2. fixed. Basis: $P(Y = 2 \mid X = 1) = 0.01/0.30 = 0.033 < 0.10$; only $X = 2$ lifts it, $0.04/0.20 = 0.20$. Now "Two defaults in pool 1 make two in pool 2 likelier".
3. fixed. Basis: in a 2 by 2 table with margins $r, c$, the cell $a = rc$ forces $r - a = r(1 - c)$, $c - a = (1 - r)c$ and the last cell $(1 - r)(1 - c)$. Note and trap now limit the one-cell claim to tables beyond 2 by 2.
4. fixed. Basis: with all trials equal to one shared coin flip, each succeeds with chance $p$ but the wait is 1 with chance $p$ and infinite otherwise; the first-step proof uses a fresh independent copy. "Independent" added to `l16` `summary.ideas[2]` and `l20` `quiz[2].prose`.
5. fixed. Basis: a mixture's tail chance is the weighted average $0.2\,P_{\text{vol}} + 0.8\,P_{\text{calm}}$, so it lies between the regimes' tails and cannot exceed both. `l17` now says a calm-only model understates the −£480 day; `homework-5` Step 5 compares with one normal of the same 7% sd and says the extra tail lowers $E[\ln(1 + R)]$ (the fourth-order Taylor term $-E[(R - \mu)^4]/4$ is negative).
6. fixed. Basis: $\mathrm{Var}(Y) - E[\mathrm{Var}(Y \mid X)] = \mathrm{Var}(E[Y \mid X])$, zero exactly when $E[Y \mid X]$ is constant; independence is sufficient only. Option `vary` why rewritten; `quiz[2].prose` now says $Y$ is not constant, so $E[Y \mid X] = X^2$ really varies.
7. fixed differently. Basis: neither name is defined in the course (grep). Replaced, not named: every "Eve's law" became "the law of total variance" (`l18` `screens[3]`, `l20` `screens[6]`, `problems-5` items 0 and 2) and "Adam's law" became "the law of total expectation" (`l18` `screens[7]`). Lesson-number citations in level 4 and 5 learner text replaced with plain references: `l17` (three), `l18` (three), `l19` (two, including "limits lesson 14" now "the Limits course"), `l20` (two), `homework-5` (one).
8. fixed. Basis: Wald's identity (Ross, *First Course*, 7.5): for $N$ a stopping time, dependent on the terms, $E[S] = E[N]E[X]$ still holds, so independence is a hypothesis of the proof, not a necessary condition; correlated fills with $N$ independent also break the variance step, so "only if" fails too. `summary.ideas[2]` now says the proof assumes independence and to check without it; `screens[8].explain` says the proof assumed it and the formulas "can fail"; `screens[10].explain` sibling "would fail" became "could fail"; `quiz[2]` option `rand` why states both assumptions. Sibling `quiz[2].explain` said a changed fill distribution breaks $E[S \mid N] = N\,E[X]$; a changed shape with the same mean does not, so it now says "changes their mean". The keyed option stands: worse fills on busy days change $E[S \mid N]$.
9. fixed. Basis: the key $12 \times 9{,}000{,}000 + 16 \times 4{,}000{,}000 = 172{,}000{,}000$, sd £13,115, uses the random-sum formula, which needs the independence now stated in `quiz[3].prose`.
10. fixed. Basis: $\sqrt{x} \approx \sqrt{\mu} + (x - \mu)/(2\sqrt{\mu}) - (x - \mu)^2/(8\mu^{3/2})$, so the gap is about $\sigma^2/(8\mu^{3/2})$; for 1 or 9, $16/(8 \times 11.18) = 0.18$ against exact $\sqrt5 - 2 = 0.236$.
11. fixed. Basis: a convex function has a supporting line at every interior point (Casella and Berger, proof of 4.7.7); the tangent version needs differentiability. Prose now says "smooth convex $g$"; explain adds the kink case. Explain stays at three sentences.
12. fixed. Basis: chord from $(-3, -27)$ to $(1, 1)$ is at $-13$ over $x = -1$, below the curve's $-1$; gap $-12$.
13. fixed. Basis: $0.5\ln 1.07 + 0.5\ln 0.95 = 0.008183$; $e^{120 \times 0.008183} = e^{0.982} = 2.67$ is the typical path, while independent months give $E[W] = 1.01^{120} = 3.30$. Explain reworded; `screens[11].prose` now says the months are independent, which the mean $1.01^{120}$ needs.
14. fixed. Basis: equality in Jensen forces $X$ constant only for strictly convex or concave $g$; a call payoff gives equality for any $X$ on one side of the strike.
15. fixed. Basis: half the range of $\{1, 3\}$ is $1$, the key, so the feedback misnamed 0.5. New text names no quantity for 0.5 and shows $5 - 4$. Slip value unchanged.
16. fixed. Basis: $0.5^5 = 0.03125$; one full ten-day record has chance $0.5^{10} = 0.00098$, and $252 \times 0.5^{10} = 0.2461$, the key.
17. fixed. Basis: $0.5^4 \times 0.2^2 \times 0.3^4 = 0.0625 \times 0.04 \times 0.0081 = 0.00002025$, and $3150 \times 0.00002025 = 0.0638$ (recomputed as $3150 \times 2.025 \times 10^{-5}$). `accept` display string only.
18. fixed. Basis: with $X$ constant each cell equals $Y$'s margin; now "Margins alone do not, in general, fix the cells."
19. fixed. Basis: $\mathrm{Var}(A + B) = \mathrm{Var}(A) + \mathrm{Var}(B) + 2\,\mathrm{Cov}(A, B)$, so zero covariance suffices. Now says adding variances needs the waits uncorrelated, which independence gives.

Gates:
- `node tools/validate.mjs 2>&1 | tail -5`: 0 errors, 4864 warnings.
- `random-vars-L4-5-concepts.py`: exit 0, 81 checks, 0 failed (no check edited). `problems-random-vars-numbers.py`, `fluency-random-vars-numbers.py`, `random-vars-1-perf-numbers.py`, `random-vars-L1-3-concepts.py`, `random-vars-L1-3-fixread.py`: all exit 0.
- `voice-scan.py 35` over the course: 0 sentences over 35 words, 0 explanations over three sentences.
- Playthrough, desktop and `--mobile`, all passed: lessons `l13`, `l14`, `l16`, `l17`, `l18`, `l19`, `l20`; sets `homework-4`, `homework-5`; `--problems random-vars/problems-5`.

## Fix-pass read

Round 1, fresh Fable reader, blind to this file until the rows were written. Read: `git diff 4bc3a770^..4bc3a770 -- app/content/courses/random-vars/` (10 files, 42 changed strings), each judged in its screen's context. Every number named was recomputed in a scratch script (all checks pass), including a simulation for the random-sum hypothesis and a quadrature for the regime mixture.

| # | File | JSON path | Claim (short) | Verdict | Basis |
|---|---|---|---|---|---|
| 1 | homework-4 | `items[2].explain.text` | Margins alone do not, in general, fix the cells | correct | Fréchet class has more than one member unless a margin is degenerate; "in general" covers that case |
| 2 | homework-5 | `items[6].explain.text` | Var(N) = 400p(1−p); 23,200 at p = 0.2; cited by lesson name | correct | 24 × 900 + 64 × 25 = 23,200 |
| 3 | homework-5 | `items[7].model` step 5 | A regime mixture usually has fatter tails than one normal of the same sd; the extra tail lowers E[ln(1+R)] | correct | Equal-mean scale mixture: E[s⁴] ≥ (E[s²])², so kurtosis above 3 and the −μ₄/4 Taylor term is larger; quadrature 0.009485 against 0.009519; "usually" covers unequal regime means |
| 4 | l13 | `screens[8].explain.text` | 0.60 against 0.50; 0.12/0.52 ≈ 0.23; same turn-around, other numbers, in Conditional Probability | correct | 3/13 = 0.2308; the trading-signal lesson there uses neither 0.12 nor 0.52 |
| 5 | l14 | `screens[5].explain.text` | Four cells fail; two defaults in pool 1 make two in pool 2 likelier, 0.20 against 0.10 | correct | Products of margins against the table: (1,1), (1,2), (2,1), (2,2) differ; 0.04/0.20 = 0.20 |
| 6 | l14 | `summary.formula.note` | Margins prove nothing; beyond 2 by 2 neither does one matching cell | correct | In a 2 by 2 table a = (a+b)(a+c) forces ad = bc, so one cell does suffice there; the pool table is the 3 by 3 counterexample |
| 7 | l14 | `summary.trap` | Same statement as the trap | correct | As row 6 |
| 8 | l16 | `summary.ideas[2]` | Independent trials with chance p take 1/p trials on average | correct | Geometric mean; independence stated as a sufficient hypothesis |
| 9 | l17 | `screens[4].prose` | "from earlier" in place of a lesson number | correct | Wording only |
| 10 | l17 | `screens[6].prose` | "before" in place of a lesson number | correct | Wording only |
| 11 | l17 | `screens[9].prose` | Proof ingredients: Var(Y) = E[Y²] − (E[Y])² and the law of total expectation | correct | Standard proof (Casella and Berger, Theorem 4.4.7) |
| 12 | l17 | `screens[10].explain.text` | −£480 is 6 sds below the calm mean and one below the volatile mean; a calm-only model understates such days | correct | (120 + 480)/100 = 6; (−180 + 480)/300 = 1; 14,400/40,400 = 0.3564 |
| 13 | l17 | `quiz[2].prose` | Y = X² is not constant | correct | Added hypothesis makes the `vary` option strictly wrong |
| 14 | l17 | `quiz[2].widget.options[1].why` | E[Var(Y∣X)] = Var(Y) needs E[Y∣X] the same for every X | correct | Var(E[Y∣X]) = 0 exactly when E[Y∣X] is constant |
| 15 | l18 | `screens[3].prose` | Law of total variance with N as the condition | correct | Var(S) = E[Var(S∣N)] + Var(E[S∣N]); right law for the table beside it |
| 16 | l18 | `screens[5].feedback.correct` | 1.6042, as found earlier | correct | 77/48; the same value stands in the lesson on variance given information |
| 17 | l18 | `screens[5].explain.text` | 0.875 + 0.7292 = 1.6042 | correct | Recomputed |
| 18 | l18 | `screens[7].explain.text` | Law of total expectation gives E[S] = E[N E[X]] = E[N]E[X] | correct | E[S] = E[E[S∣N]]; right law for the formula beside it |
| 19 | l18 | `screens[8].explain.text` | Proof assumed N independent of the fills; otherwise E[S∣N] is no longer N E[X] and the formulas can fail | correct | "Can" is right: for a stopping time N the mean formula still holds (Wald) while the variance formula fails; simulation E[S] 6.686 against E[N]E[X] 6.685, Var(S) 0.62 against formula 7.26 |
| 20 | l18 | `screens[10].explain.text` | 23,200; with dependent count and fills the formulas could fail | correct | Recomputed; as row 19 |
| 21 | l18 | `summary.ideas[2]` | Proof assumes N independent of the fills; without that, check the formulas | correct | As row 19 |
| 22 | l18 | `quiz[2].widget.options[1].why` | The formulas assume fills independent of the count and of each other | correct | Hypotheses of the derivation as taught |
| 23 | l18 | `quiz[2].explain.text` | If the count changes the fills' mean, E[S∣N] is no longer N E[X] | correct | E[S∣N = n] = n E[X∣N = n] |
| 24 | l18 | `quiz[3].prose` | Claims independent of each other and of the count | correct | Hypothesis now stated; √172,000,000 = 13,115 |
| 25 | l19 | `screens[6].feedback.byKey.equal` | Second-order gap σ²/(8μ^{3/2}) | correct | g″(μ) = −μ^{−3/2}/4, gap ≈ −g″σ²/2; numeric ratio 1.000 for small σ |
| 26 | l19 | `screens[8].prose` | Jensen proved for a smooth convex g by the tangent at μ | correct | Tangent-line proof needs differentiability at μ |
| 27 | l19 | `screens[8].explain.text` | At a kink any line through the point lying under the curve does the same job | correct | Supporting line of a convex function (Rockafellar, Theorem 23.4) |
| 28 | l19 | `screens[9].feedback.byKey.sign` | Slip 12: the chord from −3 to 1 passes below the curve at the mean −1 | correct | Chord height −13 against curve height −1; slip value 12 is the gap with the sign reversed |
| 29 | l19 | `screens[10].prose` | "as for covariance earlier" | correct | Wording only |
| 30 | l19 | `screens[11].prose` | Each month independently +7% or −5% | correct | Mean 1%, sd 6%; independence is what the 120-month figures need |
| 31 | l19 | `screens[11].explain.text` | Typical path e^0.982 = 2.67; average over paths 1.01^120 = 3.30; Kelly from the Limits course | correct | 120 × 0.0081827 = 0.9819; the median path has 60 up months, exactly e^0.982; Kelly is taught in Limits |
| 32 | l19 | `summary.ideas[1]` | For a curve with no straight stretch, equality needs X constant | correct | Strict convexity gives equality only for degenerate X |
| 33 | l19 | `quiz[1].feedback.byKey.sd` | Slip 0.5 is not the gap; 5 − 4 | correct | E[X²] = 5, (E[X])² = 4; line no longer misnames the slip |
| 34 | l20 | `screens[2].feedback.byKey.one` | Slip 0.0313 is 0.5⁵; other five not up; 252 ways | correct | 0.5⁵ = 0.03125; 252 × 0.5¹⁰ = 0.2461 |
| 35 | l20 | `screens[3].prose` | "as earlier in the course" | correct | Wording only |
| 36 | l20 | `screens[4].widget.accept` | 3150 × 0.00002025 = 0.0638 | correct | 0.0625 × 0.04 × 0.0081 = 0.00002025 exactly; product 0.0637875 |
| 37 | l20 | `screens[5].explain.text` | Mean needs no independence; adding variances needs uncorrelated waits, which independence gives | correct | Linearity; Var of a sum is the sum of variances when covariances vanish |
| 38 | l20 | `screens[6].prose` | Law of total variance gives V = 0.6V + 1.5 | correct | E[Var(W∣trade 1)] = 0.6V; Var of means 1 and 3.5 is 0.4 × 0.6 × 2.5² = 1.5; V = 3.75 = 0.6/0.16 |
| 39 | l20 | `quiz[2].prose` | Independent trials each succeed with chance 0.5 | correct | Hypothesis the negative binomial needs |
| 40 | l20 | `quiz[3].explain.text` | r = 1 gives p(1−p)^{t−1}, the first-success wait from earlier | correct | Geometric pmf |
| 41 | problems-5 | `items[0].parts[3].explain.text` | Law of total variance gives 0.25 × 31 + 2.25 × 220 = 502.75 | correct | 7.75 + 495; right law |
| 42 | problems-5 | `items[2].parts[3].explain.text` | Law of total variance: 124 + 24 = 148 | correct | 0.6 × 180 + 0.4 × 40 = 124; 0.6 × 16 + 0.4 × 36 = 24 |

Count: 42 rows, 42 correct, 0 wrong, 0 imprecise, 0 misleading, 0 unverified. No "Eve's law", "Adam's law" or lesson-number citation remains in the course folder.
