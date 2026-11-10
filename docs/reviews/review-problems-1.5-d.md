# Problem sets 1.5 (d): second-reader findings and fix-pass delta

Read at commit 8e2e553. Section A is a full second read of five sets. Section B is a delta read of the fix pass recorded in `review-problems-1.5-c.md`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question or its explanation can be read two ways or does not give what the learner needs; `minor` = weak part, loose `wrong` entry, wording, freshness or tooling.

## A. Second read: random-vars sets 4 and 5, limits-thm set 4, markov sets 4 and 5

Scope: `random-vars/problems-4.json`, `problems-5.json`, `limits-thm/problems-4.json`, `markov/problems-4.json`, `problems-5.json`: 20 problems, 100 parts (85 numeric, 5 expression, 10 choice).

Method. The three authors' scripts were run first: `problems-random-vars-numbers.py` 1,319 checks, 0 failures; `problems-limits-thm-numbers.py` 1,539 checks, 0 failures; `problems-markov-numbers.py` 1,811 checks, 0 failures. Every part was then solved from its text before its answer was read, by hand in exact fractions. Every `wrong` value was re-derived from the slip its line names. A script of my own compared the last number of each `correct` line with the key and its `tol`, each `wrong` band with the answer band, the `byKey` ids with the `wrong` ids, and the form sentence: no flag. Three things were computed apart from the hand work: the stationary law of the supplier walk under five acceptance rules (eigenvector of each transition matrix), a 40,000-hour simulation of the taxi rank in continuous time, and the five `expression` parts on the real `grade.js` with the local Compute Engine (over 80 learner spellings). The validator gives 0 errors and no warning on the five files; `fresh-check --file` gives 0 hits on each; `voice-scan.py 35` gives 0 and 0. Lessons searched for what each level teaches: total expectation and the fresh-start recursion (random-vars l16), Eve's law (l17), the random-sum variance (l18), Jensen (l19), multinomial and negative binomial with $r(1 - p)/p^2$ (l20); conditional density and the triangle (limits-thm l14), the Jacobian and $Z^2$ (l15), convolution (l16), $\tfrac{k}{n+1}$ (l17), Beta($k$, $n - k + 1$), chi-square as Gamma($\tfrac n2$, $\tfrac12$) and the wait-to-count switch (l18), MGF products, uniqueness and Chernoff (l19); detailed balance and birth-death chains (markov l13), $\tfrac{\deg(i)}{2|E|}$ and $\tfrac{1}{\pi_i}$ (l14), the Metropolis-Hastings ratio with $q$ (l15), merging and splitting by independent coin flips (l16), supermartingales (l17), $S_n^2 - n$ and $(q/p)^{S_n}$ (l18), the three cases of optional stopping and Wald (l19), the uncapped walk (l20), the casino rule (l21), $\lambda t\,E[Y^2]$ (l22).

Result. Every `answer` and every stated number in a `correct` line agrees with my own value. Two parts tell or mark the learner wrongly (findings 1 and 2), both in `markov/problems-4.json`.

Exact values checked: $\tfrac{37}{256}$ (drone, four multinomial cases), $\tfrac{89}{128}$ and $E[W] = 1.2184$ (start-up), $\operatorname{Var}(\ln R) = 0.2099$, $m_B = \tfrac{1.95}{0.7}$, $20s^2 - 26s + 7 = 0$ with root 0.38074 and bound 0.15033, $2e^{-5} - e^{-10} = 0.013430$, $6e^{-5}$ and $5.5e^{-4.5}$, $\tfrac{8}{65}$ and $\tfrac{16}{211}$, $\tfrac{50}{77}$, $\tfrac{24381}{51001}$, $\tfrac{130}{9}$ and $\tfrac{1}{0.3} + \tfrac{1}{0.063}$, the 16 paths of the capped walk (10 reach $+1$, squares sum to 38). The taxi simulation gives a share of 0.1233 of passengers finding the rank empty against $\tfrac{8}{65} = 0.1231$, and 7.30 lost an hour with four spaces against 7.28.

### Findings

1. `wrong` | `markov/problems-4.json` | `p-supplier-survey` | part 3, option `inverse`.
   The question asks which acceptance chance "makes the target uniform". The option $\tfrac{1}{\deg(j)}$ is marked wrong, yet it does that. The flow from $i$ to $j$ is $\pi_i \cdot \tfrac{1}{\deg(i)} \cdot \tfrac{1}{\deg(j)}$, symmetric in $i$ and $j$, so uniform $\pi$ satisfies detailed balance. Computed from the transition matrix: stationary law $(0.2, 0.2, 0.2, 0.2, 0.2)$, the same as the keyed rule. It is only slower (it stays at H with chance 0.25 and at A with 0.625). Its `why` line argues efficiency, not correctness.
   Fix: option text "$\tfrac{1}{\deg(i)}$", `why` "That slows moves out of well linked firms most, so the walk piles up at H: its share rises to $\tfrac{16}{26}$." (Computed: shares proportional to $\deg^2$, H at 0.6154.) The key and the other options stand.

2. `wrong` | `markov/problems-4.json` | `p-taxi-rank` | part 4, `explain`.
   "Each passenger is a thinned arrival, so this is a Poisson stream too." False. l16 splits a stream by independent coin flips; here a passenger is lost exactly when the rank is empty, which depends on the past. Losses bunch while the rank stays empty. Simulation over 40,000 hours: lost passengers an hour have mean 11.84 and variance 29.98, a ratio of 2.53 where a Poisson count has 1 (all passengers: 1.00). The rate 11.82 is right; the Poisson claim is not.
   Fix: replace the third sentence with "Losses bunch while the rank stays empty, so this is a long-run rate, not a Poisson stream."

3. `unclear` | `markov/problems-4.json` | `p-taxi-rank` | part 5, `explain`.
   "One space saves about 4.5 passengers an hour, because extra room only helps when taxis outrun passengers." Read as a general claim it is false: with the ratio $\tfrac23$ a fourth space still cuts $\pi_0$ from 0.4154 to 0.3839. It also does not explain the 4.5.
   Fix: "One space saves about 4.5 passengers an hour: the extra taxi it stores covers some of the gaps between taxis."

4. `unclear` | `markov/problems-4.json` | `p-regime-sampler` | part 5, `explain`.
   "Dropping the $q$ terms biases the sampler towards the regime that proposes least." Mid proposes a move at every step, as Low and High do. What differs is that Mid is proposed for certain from both sides and proposes each side with chance below 1.
   Fix: "Dropping the $q$ terms biases the sampler towards Mid, which is proposed for certain from both sides but proposes each side less often."

5. `minor` | `limits-thm/problems-4.json` | `p-part-errors` | part 3, question.
   "An MGF pins down its distribution." l19 states the condition: "An MGF that is finite near 0 also pins down the distribution." Without it the sentence is not true in general. It holds here, since $(1 - 2s)^{-2}$ is finite for $s < \tfrac12$.
   Fix: "An MGF that is finite near 0 pins down its distribution."

6. `minor` | `limits-thm/problems-4.json` | `p-machine-faults` | part 4; set coverage of l15.
   The question hands over the Jacobian and the transformed density ("so $f_{X,G}(x, g) = e^{-x - g}$ for $x, g > 0$"), leaving one integral. This is the set's only use of l15 (transforming variables), and the learner transforms nothing.
   Fix: end the second sentence at the Jacobian: "The map $(x, y) \to (x, g)$ has Jacobian 1. Find $f_{X,G}(x, g)$, then $P(G > 2)$. Give your answer to 4 decimal places." Part 5 already restates what it needs. Answer, slips and feedback stand.

7. `minor` | `limits-thm/problems-4.json` | `p-ticket-stages` | part 3, `rates`.
   "You used $\tfrac{0.5}{0.5}$ the wrong way up" does not name the slip, which is writing $\tfrac{\lambda}{\lambda - s}$ as $\tfrac{1}{1 - \lambda s}$.
   Fix: "You wrote $\tfrac{1}{1 - 0.5s}$ for the repair stage. Dividing $\tfrac{0.5}{0.5 - s}$ through by 0.5 gives $\tfrac{1}{1 - 2s}$."

8. `minor` | `limits-thm/problems-4.json` | `p-part-errors` | part 1, slips `one` and `added`; engine.
   On `grade.js` the learner's `\frac{1}{\sqrt{1-2s}}` does not match the slip `(1-2s)^{-1/2}`, and `\frac{4}{\sqrt{1-2s}}` does not match `4(1-2s)^{-1/2}`; `(1-2s)^{-\frac{1}{2}}` and `(1-2s)^{-0.5}` do. The grader samples $s$ between 0.3 and 3, where $1 - 2s$ is mostly negative and the two spellings differ. So the commonest way to type the slip gets the generic line. The key and every correct form grade right (over 30 correct spellings tried over the five expression parts, among them `\frac{2}{1-2s}-\frac{1}{1-s}`, `\frac{1}{2s^2-3s+1}`, `e^{-t/2}(1-e^{-t/2})`, `\exp(-x)`, and a leading `f_X(x)=` or `M_T(s)=`).
   Fix (content): add slips `one-root` with tex `\frac{1}{\sqrt{1-2s}}` and `added-root` with tex `\frac{4}{\sqrt{1-2s}}`, with the `byKey` lines of `one` and `added`. Engine item for the inbox: let an `expression` widget name a sampling range for a symbol.

9. `minor` | `random-vars/problems-4.json` | `p-file-retry` | part 2, `carried`.
   The question says "and the same rule for a time-out". A learner who carried part 1's slip $E[T \mid \text{error first}] = m$ and applied the same rule to the time-out solves $m = 0.5 + 0.5m$ and types 1, which has no entry. The stored 3 needs the slip on the error branch only.
   Fix: add `{ "id": "carried-both", "value": 1, "tol": { "abs": 0.0005 } }` with "You left the time used out of both failure branches, so $m = 0.5 + 0.5m$. An error uses 2 seconds and a time-out 5 before the fresh start." No collision (2.1, 2, 1.4, 3).

10. `minor` | `random-vars/problems-5.json` | `p-startup-rounds` | part 3, `count-squared`.
    The slip is named as multiplying $\operatorname{Var}(\ln R)$ by $E[N]^2 = 16$. That gives $3.3584 + 0.0056 = 3.3640$ once the count term is added, as the formula in the same line has it. The stored 3.3584 with `tol` 0.0005 misses it.
    Fix: value 3.3612, `tol` 0.0035 (takes 3.3584 and 3.3640). No collision.

11. `minor` | `random-vars/problems-4.json` | `p-courier-vans` | parts 1 and 3.
    Part 1 ($P(Y = 1)$) and part 3 (independence) feed no later part; the chain is 2, 4, 5. Part 1 returns only in part 5's `explain`.
    Fix: open part 4 with "Part 3 showed the rows differ, so each has its own mean." and add to part 5's question "Check it against the column totals, with $P(Y = 1) = 0.38$ from part 1." Answers stand.

12. `minor` | `markov/problems-5.json` | `p-two-loss-cut` | part 5.
    The `explain` prints "$E[T] = 3.33 + 15.87 \approx 19.21$ days". A learner who works from 19.21 gets $60 \times 19.21 = 1152.6$ and types 1153 for "the nearest pound", outside the band 1151.88 to 1152.88.
    Fix: `tol` `{ "abs": 1 }` on the answer (slips at 952.38 and 866.67 are far off), and in the `explain` "$E[T] \approx 19.2063$ days".

13. `minor` | `markov/problems-5.json` | `p-two-loss-cut` | freshness.
    `markov/problems-1.json` `p-two-losses` is also a trader with win chance 0.7 who stops after two losses in a row.
    Ruling: stands. The chain there depends on the last trade and asks matrix powers; here the days are independent and the parts ask a pattern wait and Wald's identity. No answer is shared. If the story is changed, a drawdown rule or the pattern alone (LWL first) would do.

### Per problem

- Chains. Real in all 20, with the dead ends of finding 11. Dead first parts that set the scene and are not used again: `p-young-drivers` 1 ($\tfrac37$), `p-payment-audits` 1 ($\pi_D$). `p-startup-rounds` 5 and `p-drone-route` 5 turn to a count of cases and use the earlier parts only for the question they answer. `p-ticket-stages` runs two routes to the same tail (parts 1 and 2, parts 3 to 5) and joins them in part 5's comparison. All acceptable.
- Later parts restate what they need: yes in every item. The rounded hand-offs (1.6087, 0.3913, 16.94, 0.3807, 0.4780, 6.10, 325.88, $\tfrac{8}{65}$) each give an answer inside the part's `tol`. Two are close to the edge and hold: `p-signal-trial` 5 ($-1220$ against $-1219.51$, `tol` 0.5) and `p-taxi-rank` 4 (11.82 against 11.8154, `tol` 0.005).
- Nothing is given away in an opening prose. `p-capped-close` 1 and 3 and `p-signal-trial` 4 hand over a formula in the question, which is fair for the level.
- `wrong` entries: every one differs from its answer, matches its named slip and has its `byKey` line, bar findings 9 and 10.
- Conditions of theorems. Optional stopping is used with the lesson's three cases named correctly: bounded $T$ (`p-capped-close` 2 and 4), bounded stopped process (`p-signal-trial` 3), finite $E[T]$ with bounded steps (`p-two-loss-cut` 3). The Chernoff bound is stated for $0 < s < 0.5$, where $M_T$ is finite, and the root above 0.5 is refused for that reason. PASTA is used rightly in `p-taxi-rank` 3: the arrival's kind is independent of the state it meets. Jensen's direction is right both times. Only the MGF sentence (finding 5) drops a condition.
- Notation: limits-thm set 4 writes the MGF argument as $s$ where l19 writes $t$. Right for `p-ticket-stages`, where $t$ is time; no change.

Clean problems (10 of 20): random-vars set 4 `p-late-buses`, `p-young-drivers`; set 5 `p-fishing-catch`, `p-drone-route`, `p-faulty-chips`; limits-thm set 4 `p-dealer-quotes`; markov set 4 `p-payment-audits`; set 5 `p-cash-machine`, `p-signal-trial`, `p-capped-close`.

### Per set

- Lessons. Every lesson of each level is drawn on, and each problem draws on two: random-vars l13 to l16 and l17 to l20; limits-thm l14 to l19; markov l13 to l16 and l17 to l22. Thin: l15 in limits-thm set 4 (finding 6). Nothing is used before its level; the Gamma MGF needed in `p-part-errors` 3 follows from l18 (chi-square with $n$ degrees is Gamma($\tfrac n2$, $\tfrac12$)) or from two exponential MGFs.
- Difficulty. One 5 in each set (`p-file-retry`, `p-startup-rounds`, `p-ticket-stages`, `p-regime-sampler`, `p-capped-close`), and each earns it. `p-file-retry` is the lightest of the five. Typed parts 90 of 100.
- Voice. British spelling, no exclamation marks, no em-dashes, straight apostrophes, £ for money, explanations of at most three sentences (my own scan and `voice-scan.py 35`: 0 and 0).

### Counts (A)

| tag | count |
|---|---|
| `wrong` | 2 |
| `unclear` | 2 |
| `minor` | 9 |

Finding class note (protocol 6): a distractor that is in fact a right answer (finding 1) is new to these reviews. A false sentence in an `explain` that no number check can see (finding 2, and 3) is the class to watch at these levels: the scripts prove the keys, not the prose claims about distributions.

## B. Delta read: fix pass of review (c)

Diff read: `git diff 4163760 d7c89c4 -- app/content/courses/` (nine files, 24 lines changed). Each changed item was read whole as it stands at 8e2e553 and the changed value recomputed.

| item, part | now | my value | verdict |
|---|---|---|---|
| `limits-thm` `p-default-drag` 4, `no-drag` | 0.5438, `tol` 0.002 | $z = \tfrac{-0.04}{0.35} = -0.1143$; table $\Phi(0.11) = 0.5438$; calculator $\Phi(0.1143) = 0.5455$, inside the band | closed |
| `limits-thm` `p-default-drag` 5, `no-drag` | 0.5173, `tol` 0.002 | $0.9512 \times 0.5438 = 0.51726$; calculator route 0.5189, inside | closed |
| `random-vars` `p-token-draw` 5, `carried` | 44.48 | $38 + 15(0.3483 + 0.0837) = 44.48$, with $P(G \ge 2)$ and $P(G \ge 3)$ of Bin(4, 0.3) | closed, see B1 |
| `markov` `p-maker-edge` 3 | $\Phi(2.01) = 0.9778$ supplied, 3 places, `tol` 0.0025 | $\tfrac{80}{39.80} = 2.01$, $1 - 0.9778 = 0.0222$; band 0.0197 to 0.0247 takes 0.020 to 0.024 | closed |
| `markov` `p-rfq-rounds` prose | three Counter chances listed | matches row Counter of the canvas, $(0.5, 0, 0.2, 0.3)$ | closed |
| `markov` `p-rfq-rounds` 5, `rounds` | "about 1.53 rounds against part 3's 1.75" | $t_Q = \tfrac{1.3}{0.85} = 1.5294$ | closed |
| `counting-chance` `p-octahedral-prize` 5 | "Give your answer to the nearest penny." | $16 \times \tfrac{19}{64} = 4.75$, `tol` 0.005 | closed |

Agreement of the unchanged text. `p-default-drag`: the answer bands (0.4761 and 0.4529, `tol` 0.0005) do not meet the widened slip bands (0.5418 to 0.5458, 0.5153 to 0.5193), nor do `phi` 0.5239, `half` 0.5 or `survivor` 0.4761. Part 4's question still supplies $\Phi(0.11)$ "as needed", which is now what the slip uses, and part 5's line "carries part 4's slip" agrees. `p-maker-edge`: the `correct` and `explain` lines print 0.022 under a 3-place question; the slips 0.4799, 0.9778 and 0 lie outside the band; part 4's $z = 2.33$ and 538 are untouched and consistent. `p-rfq-rounds`: parts 1 to 4 use 0.5, 0.2 and 0.3 for the Counter row as the prose now lists them. `p-token-draw`: the answer 43.50 and the other four slips are untouched. The other edits (`p-merger-arb` 5 break-even wording, `p-block-calls` 2, `p-maker-days` 2 `phi`, `p-fund-hedge` placeholder and 0.5833, `p-two-houses` apostrophes) read right and change no number.

### Findings

1. `minor` | `random-vars/problems-2.json` | `p-token-draw` | part 5, `carried`.
   The two fixes of review (c) B1 pull apart. The question now hands over "the 7 hands with three gold tokens", so a learner who carries only part 4's 0.3483 uses $\tfrac{7}{210}$ for the third token and gets $38 + 15(0.3483 + 0.0333) = 43.7245$, the value the fix removed. The stored 44.48 needs the learner to set aside both restated values.
   Fix: keep 44.48 and add `{ "id": "carried-half", "value": 43.72, "tol": { "abs": 0.005 } }` with "You used 0.3483, the with-replacement chance, for $G \ge 2$. Counting hands gives $\tfrac{1}{3}$, so the price is £43.50." No collision (38, 43, 43.50, 44.48, 53, 5.5).

### Counts (B)

| tag | count |
|---|---|
| `wrong` | 0 |
| `unclear` | 0 |
| `minor` | 1 |

Status: **closed**. Every changed value recomputes and nothing else in the six items contradicts a change. Nothing returns to the fixer; B1 can ride with the fix pass for section A.
