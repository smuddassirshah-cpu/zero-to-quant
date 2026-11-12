# Concept audit, round 2 (blind): random-vars levels 4 and 5

Auditor: Fable, blind second round. Date: 12 Nov 2026. Branch state: `claude/fable-audit` fast-forwarded before reading.

Scope read in full: `l13-joint-tables`, `l14-independent-rvs`, `l15-given-information`, `l16-averaging-averages`, `l17-variance-given-information`, `l18-random-sums`, `l19-convex-bets`, `l20-many-categories`, `review-4`, `review-5`, `homework-4`, `homework-5`, `problems-4`, `problems-5`. No `fluency-*.json` file belongs to l13 to l20.

Blind rule: the ledger, the findings below and the concepts script were written and committed (WIP commit) before any earlier audit, review, report or script for these files was opened. The overlap section was added afterwards.

Outputs:
- Ledger: `docs/reports/audit-random-vars-4-5-r2-ledger.md`, 357 hand-judged rows: 346 `correct`, 1 `wrong`, 9 `imprecise`, 1 `misleading`, 0 `unverified`.
- Script: `docs/reports/random-vars-L4-5-concepts-r2.py`, 401 checks. It recomputes every graded key, wrong option and slip value, replays the three code solutions on their stated seeds, and runs exact enumerations and Monte Carlo checks.

## Summary

The mathematics of both levels is sound. Every graded key, every wrong option and every slip value recomputes, and every slip's feedback names a quantity the slip value really is. The three console figures quoted from code (l16, l18, homework-5) are printed digit for digit by the taught code. The independence class is handled well in the lesson text: l18 says "the formulas can fail", l20 says adding variances "needs them uncorrelated, which independence gives".

One `wrong` was found: a canvas on l20 shows the wrong stock's chances. The other ten findings are wording: nine `imprecise` and one `misleading`, all `minor`.

Counts: 11 findings. `wrong` 1 (minor), `imprecise` 9 (minor), `misleading` 1 (minor). Serious 0, minor 11.

## Findings

Pattern: `N. file | JSON path | severity, tag | problem | evidence and basis | exact fix`.

1. `l20-many-categories.json` | `screens[9].canvas.params.levels[0].branches[*].p` | **wrong, minor** | The tree on this screen shows Up 0.5, Flat 0.2, Down 0.3. The prose and the key are about a different stock, with chances 0.6, 0 and 0.4. The picture contradicts the question. | The prose reads "A stock that cannot be flat has chances up 0.6, flat 0, down 0.4", and the key is $\binom{10}{6}(0.6)^6(0.4)^4 = 0.2508$. A learner who reads the chances off the tree computes $210 \times 0.5^6 \times 0.3^4 = 0.0266$ and is marked wrong with the generic line. The canvas is a copy of the tree on `screens[4]`. Tagged minor because the prose states the right chances and no wrong rule is taught. Script check `l20 s9 canvas tree matches the prose chances 0.6 / 0 / 0.4` fails on purpose. | Set the three `p` values to `"0.6"`, `"0"` and `"0.4"`, in the order Up, Flat, Down. If the tree canvas cannot draw a branch with chance 0, keep the three branches and check the screen in the playthrough at both widths.

2. `l16-averaging-averages.json` | `screens[5].feedback.byKey.three` | **imprecise, minor** | "Three tosses would be enough only if no tail ever interrupted." With no tail at all, two tosses are enough. The line does not say what the 3 is. | The slip value 3 is the wait for one head, 2, plus one more toss. It is also the solution of $E = \tfrac12(1 + E) + \tfrac12 \cdot 2$, which forgets the restart after head then tail. Script check `l16 s5 slip three is wait for one head plus one toss`. | "3 is the wait for one head plus one more toss. That works only if the next toss is a head. A tail sends you back to the start, so weight the leaves and solve."

3. `l18-random-sums.json` | `screens[2].feedback.byKey.sd` | **imprecise, minor** | "Sds do not add, variances do." As a bare rule this is false both ways: variances add only for uncorrelated terms, and sds do add for perfectly correlated ones. The same screen's `squared` slip relies on that second fact. | $\mathrm{Var}(X + Y) = \mathrm{Var}(X) + \mathrm{Var}(Y) + 2\,\mathrm{Cov}(X, Y)$ (Blitzstein and Hwang, ch. 7.3). The lesson's own summary trap says it correctly: "Independent fills add variances." | "That is $25 \times 30$. For independent fills the variances add, not the sds."

4. `l18-random-sums.json` | `quiz[2].question`, `quiz[2].feedback.correct` | **imprecise, minor** | The stem asks "When do they fail?" and the key is "when ... $N$ and the fills are dependent". This states independence of the count as necessary. It is only sufficient. | $E[S] = E[N]E[X]$ still holds when $N$ depends on the terms as a stopping time (Wald's identity). Script checks `l18 dependence can break ...` and `l18 Wald: mean formula holds ...` show both outcomes. The lesson's own explain on `screens[8]` uses the right wording, "the formulas can fail". | `quiz[2].question`: "When can they fail?" `quiz[2].feedback.correct`: "The proof conditioned on $N$ and treated the fills as independent of it. That independence is enough; without it the formulas can fail."

5. `l15-given-information.json` | `screens[8].explain.text` | **imprecise, minor** | "Its conditional beta is 0.9 on the way down and 0.7 on the way up. A single beta of 0.8 would hide an asymmetry". On this screen $x = -1$ and $x = 1$ label down days and up days. They are not market moves of 1%, so the averages $-0.9$ and $0.7$ are not betas. | Beta is the slope of the stock's return on the market's return (Hull, *Options, Futures and Other Derivatives*, ch. 3). The screen gives no size for the market's move, so no slope per 1% can be read from it. | "The stock falls 0.9% on an average down day but rises only 0.7% on an up day. A single figure of 0.8% for both kinds of day would hide the gap. The asymmetry hurts a long holder."

6. `homework-4.json` | `items[5].explain.text`, last sentence | **misleading, minor** | "Head then tail beats head then head because a failed attempt keeps the head." "Beats" reads as "comes first more often". In a race the two patterns are equally likely to come first. Only the mean wait differs, 4 against 6. | After the first head the next toss decides the race, so each pattern wins with chance $\tfrac12$. Monte Carlo check `hw4 5 race HT v HH is even` gives 0.50. Interview questions ask both versions, so the two ideas must stay apart. | Replace the last sentence with: "Head then tail has the shorter wait, 4 against 6 for two heads, because a failed attempt keeps the head."

7. `homework-5.json` | `items[4].prose` | **imprecise, minor** | "Over 50 days, up has chance 0.4, down 0.35 and flat 0.25." Independence of the days is not stated, and the key $-n\,p_i p_j$ needs it. | The derivation in `items[1]` uses "for $k \ne l$ the trials are independent". With dependent days the covariance of the counts can take other values. | "Over 50 days, each day is independently up with chance 0.4, down with 0.35 or flat with 0.25. $N_{\text{up}}$ and $N_{\text{down}}$ count the up and down days."

8. `review-5.json` | `items[8].prose` | **imprecise, minor** | "Each quote has a fee with mean £3 and variance 5, independent of $N$." The fees' independence of each other is not stated. The first term, $E[N]\mathrm{Var}(X)$, needs the fees uncorrelated. | $\mathrm{Var}(S \mid N = n) = n\,\mathrm{Var}(X)$ holds for uncorrelated terms (Blitzstein and Hwang, ch. 7.3). The other random-sum items in scope all say "independent of each other and of $N$" or the same in other words. | Last sentence: "Each quote has a fee with mean £3 and variance 5, independent of the other fees and of $N$."

9. `homework-5.json` | `items[7].model`, Step 2 | **imprecise, minor** | "the typical (median) wealth is $e^{120\,E[\ln(1 + R)]}$". The median of log wealth equals its mean only for a symmetric distribution. For a sum of 120 months it is close, not equal. | Log wealth is a sum of 120 independent terms, so it is near normal and its median is near its mean (central limit theorem). The model answer's own caveat lists two approximations and omits this one. | In Step 2 replace "so the typical (median) wealth is $e^{120\,E[\ln(1 + R)]}$, below the mean" with "so the typical (median) wealth is close to $e^{120\,E[\ln(1 + R)]}$, below the mean".

10. `problems-4.json` | `items[1].parts[3].widget.options[3].why` (option `small`) | **imprecise, minor** | "Any total that depends on $Y$ moves its chances." A total and $Y$ are always dependent, but one seen value of the total can leave $Y$'s chances unchanged. | Two independent fair bits: $P(Y = 1 \mid X + Y = 1) = \tfrac12 = P(Y = 1)$. Script check `p4 1.3 counterexample`. In this problem every value of $S$ does move $Y$, so the key and the other lines are right. | "The size of $P(S = 2)$ is not the reason. The total is built from $Y$, and here a total of 2 makes a late route 2 likelier."

11. `problems-5.json` | `items[3].parts[4].explain.text` | **imprecise, minor** | "An up round and a down round together multiply value by 0.9. So $W < 1$ exactly when at most half the rounds are up." The pairing argument proves one direction only. The "exactly" is true for $N = 2$, 4 and 6 and false as a general rule. | With $N = 20$ and 11 up rounds, $1.5^{11} \times 0.6^{9} = 0.87 < 1$. The exact condition is $k < 0.5575N$. Script checks `p5 3.4 W<1 iff k<=N/2` (true for the three values of $N$) and `p5 3.4 general counterexample`. The key 0.6953 is right. | "An up round and a down round together multiply value by 0.9, so at most half up rounds gives $W < 1$. One up round more than half gives $W > 1$ for $N = 2$, 4 and 6. Given $N$ that is a binomial chance, and by total probability $P(W < 1) = \tfrac{89}{128} \approx 0.6953$, though $E[W] = 1.2184$."

## Checked and passed (classes the brief asks for by name)

- Keys, wrong options and slips: all recomputed in the script; none is correct under a valid alternative method. Three slip values coincide with a second quantity (l13 `screens[9]` 0.40, l14 `screens[10]` 0.30, l16 `screens[0]` $-0.16$, l17 `screens[2]` 3,600); in each the feedback line is true of the value.
- Independence as sufficient, not necessary: l14 quiz, l15 `screens[6]`, l18 `screens[8]` and `screens[10]`, l20 `screens[5]` and homework-4 `items[2]` all state the one-way implication. The two true equivalences in l17 (`quiz[2]`, `quiz[3]`: the second piece vanishes only when the conditional means agree) are correct as written. Only finding 4 states necessity.
- Hypotheses: $P(X = x) > 0$ is stated where rows are rescaled; $p > 0$ where $1/p$ is derived; $N$ independent of the terms is stated in l18 and in every random-sum item except finding 8; $X > 0$ and "not constant" are stated where strict Jensen is keyed.
- Strict against non-strict: strict inequalities are keyed only with "not constant" in the stem. In problems-5 `items[1].parts[4]` no total equals 80 minutes, so "more than" is safe.
- Frequency phrases: "one day in five" (0.2), "about one day in seven" (0.1445), "more than twice as common" (0.7 against 0.3) and "about three times" (220 against 70) all match.
- Puzzle protocols: two heads in a row, head then tail, and two sixes in a row each state the stopping rule; keys 6, 4 and 42 are confirmed by first-step equations and by simulation.
- Console lines: l16 `1.99834`, `6.03976`, `5.03602`; l18 `18466.21`; homework-5 `120.21`, `22822.56`, `99.66`, `18248.28`. All are reproduced by the taught code in CPython, which uses the same Mersenne Twister as Pyodide.
- Conventions: population variance in the simulations matches the lesson's definition; the negative binomial counts trials and the failures convention is named once (l20 `screens[7]`); $0^0 = 1$ is stated as a convention where it is used.
- Real-world and cross-course facts: "Stat 110 style" matches the inequality exercises of Blitzstein and Hwang ch. 10; "Bayes on a trading signal" is the title of `conditional/l26`; the Kelly reference matches `limits/l14`. None is left `unverified`.

## Gates

- Validator, from `app/`: `0 errors, 5023 warnings`. `content/manifest.json` restored afterwards.
- `docs/reports/problems-random-vars-numbers.py`: exit 0, 1333 checks, 0 failures.
- `docs/reports/fluency-random-vars-numbers.py`: exit 0, 1767 checks, 0 failures.
- `docs/reports/random-vars-1-perf-numbers.py`: exit 0, 109 checks, 0 failures.
- `docs/reports/random-vars-L4-5-concepts-r2.py`: exit 1, 401 checks, 1 failure. The failure is on purpose: `l20 s9 canvas tree matches the prose chances 0.6 / 0 / 0.4` (finding 1). It will pass once the canvas is fixed. No other check fails.
- Playthrough with `--local-cdn`, each file by selector, desktop and `--mobile`: the eight lessons `ok` (13 to 16 checks each, quiz 4 of 4), `review-4` 8 of 8, `review-5` 10 of 10, `homework-4` 9 of 9 (41 of 41 marks), `homework-5` 9 of 9 (42 of 42 marks), `problems-4` and `problems-5` (via `--problems`) 4 problems and 20 parts each. All passed at both widths.

## Overlap

Filled after the WIP commit `d873e3b3`. Earlier reads of this scope, all read now:

- `docs/reviews/audit-random-vars-4-5.md`: round 1 audit (19 findings: 3 `wrong`, 16 `imprecise`), its Fix pass (19 fixed) and its Fix-pass read (42 rows, all `correct`).
- `docs/reviews/review-1.5.md`, lines 71 to 80 (level 4 lessons, review and homework).
- `docs/reviews/review-problems-1.5-d.md`, section A, findings 9 to 11 (problem sets 4 and 5).
- `docs/reviews/review-delta-session-aa.md`, finding 10 (problems-4 wording).
- `docs/reviews/fix-pct-keys.md` (percentage keys of l19 `screens[11]` and review-5 `items[5]`) and `docs/reviews/review-precision-3.2.md` rows 64 and 65. Neither raises a conceptual finding on this scope.

| | count |
|---|---|
| Conceptual findings found by this audit only | 11 |
| Found by earlier reads only | 22 |
| Found by both | 0 |

The 22 are round 1's 19 findings plus the 3 slip-and-feedback findings that round 1 counted from the earlier reviews. All 22 were fixed before this read, so this audit read the fixed text. It judged each fixed string `correct` in the ledger, which agrees with the round 1 Fix-pass read. A round 2 reader cannot re-find a fixed finding, so "both: 0" measures only that no earlier read raised any of the 11 here.

Each of this audit's findings against the earlier reads:

| # | finding | severity | found by any earlier read? |
|---|---|---|---|
| 1 | l20 `screens[9]` tree shows 0.5, 0.2, 0.3 | wrong | No. No earlier read mentions this canvas. **New `wrong`.** |
| 2 | l16 `screens[5]` slip `three` feedback | imprecise | No. review-1.5 line 79 is about the `three` slip of homework-4 `h-ht`, a different item. |
| 3 | l18 `screens[2]` "Sds do not add, variances do" | imprecise | No. |
| 4 | l18 `quiz[2]` "When do they fail?" | imprecise | No. Round 1 finding 8 fixed the summary, `screens[8]` and the option `rand` why on this class, and judged the keyed option of `quiz[2]` right. The stem and the feedback kept the "fail when dependent" reading. |
| 5 | l15 `screens[8]` "conditional beta" | imprecise | Seen and passed. Round 1 lists it under "Notes that are not findings" as close enough to practitioner usage. This audit disagrees: the screen gives no market move size, so no beta can be read. Counted as found by this audit only. |
| 6 | homework-4 `h-ht` "beats" | misleading | No. |
| 7 | homework-5 `items[4]` independence of days unsaid | imprecise | No. Round 1 findings 4 and 9 are the same class on other items (l16 summary, l20 `quiz[2]`, l18 `quiz[3]`). |
| 8 | review-5 `items[8]` fees independent of each other unsaid | imprecise | No. Same class as round 1 finding 9. |
| 9 | homework-5 `items[7]` median stated as exact | imprecise | No. Round 1 finding 5 and its fix changed Step 5 of the same model answer, not Step 2. |
| 10 | problems-4 `p-late-buses` part 4, option `small` | imprecise | No. review-problems-1.5-d lists `p-late-buses` as clean. |
| 11 | problems-5 `p-startup-rounds` part 5 explain | imprecise | No. review-problems-1.5-d finding 10 is about the `count-squared` slip of part 3. |

`wrong` findings that no earlier read found: **1** (finding 1), over two levels. It is in text that neither the round 1 fix pass nor its fix-pass read touched (`screens[9].canvas` is not in the fix diff).

Classes seen again: independence left out of a prompt whose key needs it (findings 7 and 8) has now been raised in both rounds on five items of this course. An inbox bullet below proposes a check.

## Inbox

- Validator (warning): a `tree` canvas whose branch chances are identical to a tree on an earlier screen of the same lesson, on a screen whose prose states chances that match none of them. This would have caught finding 1 (l20 `screens[9]` reuses the `screens[4]` tree under new chances).
- Validator (warning), wording lint for the independence class: flag "do not add" or "fail" next to "sds", "variances" or "formulas" when the sentence has no "independent" or "uncorrelated" (findings 3 and 4). Low precision, so a warning only.
- Script (reader aid): list every item whose key or explain uses a product of chances, $-n\,p_i p_j$, $r/p$ or the random-sum variance while its prose has none of "independent", "independently" or "multinomial". Raised twice in round 1 (findings 4 and 9) and twice here (findings 7 and 8), so the class has passed the three-sightings rule.
