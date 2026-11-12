# Problem sets 1.10, analysis levels 1 to 3: second-reader findings

Scope: `app/content/courses/analysis/problems-1.json`, `-2`, `-3`: 9 problems, 45 parts (32 numeric, 5 `expression`, 8 choice), 80 `wrong` entries. Rules: `docs/briefs/chained.md`. Pattern: `review-problems-1.4-c.md`.

Method. The author's script was run first. Lessons l1 to l14, `review-1` to `-3`, `homework-1` to `-3` and `exams/topic-1.10.json` were then read screen by screen (`review-problems-analysis-1-3-scripts/taught.py` prints the learner-facing text of a file), for what each level teaches and for reused settings, numbers and sentences. Every part was solved by hand from its text and again in `mine.py`, which imports nothing from the author's script and types every set, sequence and series from the prose. Route 1 is exact (fractions, sympy: bisection in exact fractions, `solve`, `limit`, `summation`). Route 2 is another method: a brute search for every "smallest $n$" (each claimed least $N$ is shown least and shown to hold for all later $n$), the recursion iterated at 30 digits, the telescoping formula against a running sum for $N = 1$ to 1199, `mpmath.altzeta` and `nsum` for the cube-root series, the greedy rule run for 200,000 terms, the true $N$ of the sum law by its quadratic. Every `wrong` value was rebuilt from the slip its line names and each number printed in a `feedback`, `byKey`, `why` or `explain` string was recomputed. Each theorem use was read for its hypotheses: monotone convergence (rising and bounded, both stated), the alternating bound (sizes checked to decrease to 0), the ratio test (run on the positive sizes), comparison ($0 < a_n < b_n$ checked), the cube bound $(s + \tfrac1n)^3 \le s^3 + \tfrac{3s^2 + 3s + 1}{n}$ (proved as an identity for $n \ge 1$), density ($\tfrac1n < b - a$), Bolzano-Weierstrass ($|a_n| < 2$ checked). Every typed part then went through the engine's own graders in node with the local Compute Engine (`grade-probe.mjs`: `numGrade` and `exprGrade`): the key, with one more place, a letter and `=`, a true minus sign; each `accept` form; each `wrong` entry on its own key; and 271 strings of my own (fraction against decimal, the rounding the part asks for and the next coarser one, other forms of each expression, the answer one step short, the question retyped). `try-fix.mjs` tries the fix of finding 5 on an in-memory copy and `proposed.py` computes the numbers of the fixes of findings 1 and 3. Freshness was read by eye, helped by `fresh.py` (formulas, key numbers and nouns of each problem across `app/content`) and `fresh-check.mjs --cross-numbers`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question or a line can be read two ways, or refuses a sensible entry; `minor` = weak part, loose chain, loose `wrong` entry, missing restatement, wording or freshness.

## Tool results

| check | result |
|---|---|
| author's script (scratchpad venv) | `problems-analysis-numbers.py` 517 of 517, exit 0 |
| `mine.py` (reader's own keys, slips, stated numbers, set shape) | 424 checks, 0 failures, exit 0; 1 CLAIM line (finding 5), 2 NOTE lines |
| `grade-probe.mjs` (engine graders, 37 typed parts) | 546 checks, 271 reader rows, 0 failures, exit 0; 4 rows held to be faults (finding 5, Engine note 1) |
| `try-fix.mjs` (fix of finding 5; `form` tried for Engine note 1) | 29 checks, 0 failures |
| `proposed.py` (numbers of the fixes of findings 1 and 3) | 15 of 15, exit 0 |
| `skills.py` | every `skills` id of each set is carried by a lesson of its level |
| `grade-all.mjs --file`, three sets | 15 widgets each, 0 failures |
| validator | 0 errors, 4522 warnings, none on the three files; `manifest.json` restored |
| voice scan 35, course folder | 0 and 0; no exclamation mark, no em-dash, British spelling, no money in the sets |
| `fresh-check.mjs --file --cross-numbers`, three sets | 0 hits; 1, 3 and 14 advisories, read: the taught formulas and powers of 2, as the author says, and the l7 pairing of finding 3 |
| browser, `playthrough.mjs` | not run (reader rule) |

Result. All 37 typed keys and the 8 choice keys agree with mine, and so does every one of the 80 `wrong` values and every number in a feedback or explanation string. Every claimed least $N$ is least (138, 80, 109, 2250, 16, 100001, 14, 6, 998, 6). Every limit, supremum, infimum and convergence claim holds, and each theorem is used with its hypotheses met. No learner is marked wrongly: no `wrong`-tagged finding. One line names the wrong half of the supremum test when read the natural way (finding 2). One slip band catches the true sum (finding 5). Two problems replay a lesson or review screen with the same numbers (findings 1 and 3). One restatement names a value the step does not use (finding 4).

## A. `problems-1`

1. `minor` | `analysis/problems-1.json` | `p-cube-root-twenty` | `items[0].parts[0]` and the numbers that follow it | same-course reuse.
   `review-1` "Bisection for the root of 5" reads "Bisect $[2, 3]$ for $\sqrt5$ ... What is the left end of the interval after 3 halvings?" Part 1 reads "Halve $[2, 3]$ three times ... Give its left end". Same interval, same count, same ask; only the target and the answer differ (2.125 there, 2.625 here). The author's report already moved the target from 10 to 20 for this reason. The interval cannot change (the root of 20 lies in it), so change the count.
   Fix (all values in `proposed.py`): four halvings.
   - Part 1 question: "Halve $[2, 3]$ four times, each time keeping the half whose ends cube to either side of 20. Which interval is left? Give its left end as an exact decimal." `answer` 2.6875. `wrong`: `right-end` 2.75; replace `two-steps` by `one-short` 2.625. `correct`: "$2.5^3 = 15.625$ and $2.625^3 \approx 18.09$ are too small, $2.75^3 \approx 20.80$ too big and $2.6875^3 \approx 19.41$ too small, so the left end is 2.6875." `right-end`: "That is the right end. The interval left is $[2.6875, 2.75]$, so its left end is 2.6875." `one-short`: "That is the left end after three halvings, $[2.625, 2.75]$. The fourth midpoint 2.6875 cubes to about 19.41, below 20, so it becomes the left end." `explain`: "The intervals run $[2.5, 3]$, $[2.5, 2.75]$, $[2.625, 2.75]$, then $[2.6875, 2.75]$. The last step holds because $2.6875^3 \approx 19.41 < 20 < 2.75^3 \approx 20.80$."
   - Part 2: "$2.6875 = \tfrac{43}{16}$", $p = 43$, $q = 16$. `answer` $-2413$ ($43^3 = 79507$, $20 \times 16^3 = 81920$). `wrong`: `sign` 2413, `squares` $-3271$ ($1849 - 5120$), `no-twenty` 75411 ($79507 - 4096$). Replace the same numbers in the four lines and in `explain` ("so $\tfrac{43}{16}$ falls short").
   - Part 4: "Take the illustrative value $s = 2.6875$ from part 1." `answer` 53. Top $21.66796875 + 8.0625 + 1 = 30.73046875$, bottom $20 - 19.410888671875 = 0.589111328125$, bound about 52.16. `wrong`: `round-down` 52, `no-ones` 37 ($3s^2$ alone gives about 36.78), and a new `no-plus-one` 51 (the top without its $+1$ gives about 50.47; today's `round-down` line says this slip lands on the same value, which it no longer does). Lines: `round-down` "The bound is about 52.16, and 52 lies below it."; `no-plus-one` "You dropped the $+1$ from the top, which gives about 50.47. The top is $3s^2 + 3s + 1 = 30.73046875$."; `no-ones` "You kept only $3s^2$ on top, which gives about 36.78. The top is $3s^2 + 3s + 1 = 30.73046875$." `explain` ends "Indeed $\left(2.6875 + \tfrac{1}{53}\right)^3 \approx 19.82 < 20$."
   - Part 5: "as 53 did for 2.6875"; option `illustrative` "$s = 2.6875$, the left end from part 1", `why` "... $2.6875^3 \approx 19.41$, so 2.6875 is not the cube root."
   None of 2.6875, $\tfrac{43}{16}$ or $-2413$ occurs in `app/content`.

2. `unclear` | `analysis/problems-1.json` | `p-cube-root-twenty` | `items[0].parts[4]` `feedback.correct`, `explain.text` (and the question's "A matching step").
   "$s^3 < 20$ breaks the upper-bound half of $s = \sup S$, and $s^3 > 20$ fails the same way". Read plainly, the second case also breaks the upper-bound half. It does not: it gives an upper bound $s - \tfrac1n$ below $s$, which breaks the least half (l3 "Case two": "An upper bound below $s$ breaks leastness"). The learner is being asked which half each case contradicts (`generic`: "Ask what each case contradicts").
   Fix, `feedback.correct`: "$s^3 < 20$ puts an element of $S$ above $s$, and $s^3 > 20$ gives an upper bound below $s$. Both contradict $s = \sup S$, so $s^3 = 20$."
   Fix, `explain.text`: "If $s^3 < 20$, then $s + \tfrac1n$ lies in $S$ above the upper bound $s$, a contradiction. If $s^3 > 20$, some $s - \tfrac1n$ is an upper bound below $s$, against leastness, so $s^3 = 20$. Part 3 showed no fraction has that cube, so $s$ is irrational."

## B. `problems-2`

3. `minor` | `analysis/problems-2.json` | `p-sum-law-band` | `items[0]`, whole item | same-course reuse.
   l7 "Limit laws, proved" screens 1 to 4: $a_n \to 3$, $b_n \to 2$, the sums in the band $5 \pm 0.1$, "Take $\varepsilon = 0.1$, so each gap must be below 0.05", the first index for each, the proof's $N$, and the first $n$ from which the sums stay in the band. The problem has the same limits 3 and 2, the same sum 5, the same $\varepsilon = 0.1$ and half band 0.05, and asks the same four things in the same order. Only the two formulas differ. `fresh-check` lists the pair as an advisory (`|b_n - 2|`, `|a_n + b_n - 5|`).
   Fix (values in `proposed.py`): new limits and band. Prose: "Two sequences meet the sum law: $a_n = \tfrac{8n + 3}{2n + 5}$ tends to 4 and $b_n = \tfrac{3n - 1}{n + 1}$ tends to 3. We run the proof of the sum law with $\varepsilon = 0.04$, then compare its $N$ with the truth."
   - Part 1: $|a_n - 4|$; `answer` `\frac{17}{2n+5}`, `accept` `17/(2n+5)`, `\frac{17}{5+2n}`; `wrong` `plus-one` `\frac{23}{2n+5}` ($8n + 3 - 4(2n + 5) = 3 - 20 = -17$; adding gives 23), `sign` `-\frac{17}{2n+5}`.
   - Part 2: half band 0.02. $2n + 5 > 850$, $n > 422.5$, `answer` 423; `round-down` 422 (gap $\tfrac{17}{849} \approx 0.02002$); `full-band` 211.
   - Part 3: "$|b_n - 3| = \tfrac{4}{n + 1}$"; $n + 1 > 200$, `answer` 200; `equal` 199 (gap $\tfrac{4}{200} = 0.02$ exactly); `full-band` 100.
   - Part 4: `answer` 423; `min` 200; `sum` 623. `explain`: "$|a_n + b_n - 7| \le |a_n - 4| + |b_n - 3| < 0.04$".
   - Part 5: "$|a_n + b_n - 7| = \tfrac{17}{2n + 5} + \tfrac{4}{n + 1}$ exactly ... below 0.04"; `answer` 311; gap about 0.04006 at $n = 310$ and about 0.03993 at $n = 311$; `proof` 423; `round-down` 310 ("$\tfrac{17}{625} + \tfrac{4}{311} \approx 0.04006$").
   Neither new formula occurs in `app/content`. If the item is kept as it is, record the l7 pairing in the author's report as judged.

4. `minor` | `analysis/problems-2.json` | `p-root-recursion` | `items[1].parts[2].question` | the restated value is not the one the step uses.
   "Using the bound $a_n < 7$ from part 2, what is $L$?" The bound does not choose between the roots 7 and $-3$; the part's own lines use $a_n \ge 1$ ("and $L \ge 1$, so $L = 7$"). The bound is what the theorem needs. A learner told to use it may look for a step that is not there.
   Fix: "The terms also rise and, by part 2, stay below 7. So the monotone convergence theorem gives a limit $L$, with $L = \sqrt{4L + 21}$. What is $L$? Give a whole number."

## C. `problems-3`

5. `minor` | `analysis/problems-3.json` | `p-alternating-quarters` | `items[1].parts[4].widget.wrong` (`s7`) | a slip band catches the true sum.
   `s7` is 0.1600952 with band 0.0001, so it takes every entry from 0.1599952. A learner who types 0.16 or $\tfrac{4}{25}$ (the sum itself, which the explanation prints, or $S_6$ to 2 places) is told "That is $S_7$, one term too far" (`grade-probe.mjs`, 3 rows). It is rightly refused; the line is false for it.
   Fix (`try-fix.mjs`, 13 checks): give `s7` `"tol": { "abs": 0.00005 }` and add `{ "id": "sum", "value": 0.16, "tol": { "abs": 0.00004 } }` with the line "That is the sum itself, $\tfrac{4}{25}$, or $S_6$ cut to 2 places. $S_6$ stops after six terms: $\tfrac{327}{2048} \approx 0.1597$." Then 0.1601 and 0.1600952 still reach `s7`, and 0.1597, 0.15967, 0.1596 and $\tfrac{327}{2048}$ still pass.

## Same-course reuse, read by eye

Read against l1 to l14, the three reviews, the three homework sets and `exams/topic-1.10.json`. Findings 1 and 3 are the two cases where numbers and the ask are shared. The rest are the taught method on new numbers, judged acceptable:

| problem | nearest items | shared | judgement |
|---|---|---|---|
| p-cube-root-twenty | l1 (miss $p^2 - 2q^2$, $p = 2k$), l3 (bisection, $\sup S$, illustrative $s$, "smallest whole number $n$ beyond that bound"), review-1 | the proof skeleton; `[2, 3]` and three halvings | finding 1 for part 1; the cube version of the proof is a fair transfer |
| p-climbing-fractions | l2 ($\{1 - \tfrac1n\}$, two-part test), homework-1, topic exam ($\tfrac{2n+1}{n+4}$) | the sentence "holds exactly when $n$ is greater than what?" | stock ask of l2, l6, homework-1 and review-2; numbers new |
| p-diagonal-fraction | l5 (the 5-and-4 rule), l4 and review-1 (recipe, $n = 101$), topic exam (list starts $0.5544\ldots$) | the taught rule and recipe; our $x$ starts 0.5544 too | chance: digits are 4s and 5s by the rule |
| p-root-recursion | l8 ($\sqrt{2 + a_n}$, $a_1 = 1$), review-2 ($\sqrt{6 + a_n}$), topic exam ($\sqrt{3a_n + 10}$, $a_1 = 1$) | $a_1 = 1$; the limit-equation step | fourth member of a family; parts 4 and 5 (the rate) are new |
| p-two-strands-cauchy | l9 ($(-1)^n(1 + \tfrac1n)$), review-1 ($(-1)^n(1 - \tfrac1n)$), l9 quiz ("limit of the odd-indexed terms $a_1, a_3, a_5, \dots$") | the shape $(-1)^n(c \pm \tfrac dn)$; one stock sentence | acceptable; parts 3 to 5 (steps, Cauchy) are new |
| p-telescoping-tail | review-3 ($\tfrac{2}{n(n+2)}$, sum 1.5), homework-3 ($\tfrac{3}{k(k+3)}$), topic exam ($\tfrac{1}{n(n+3)}$) | the series is review-3's with the index moved by one and halved | close cousin; sum, tail and comparison parts are new. Worth a line in the author's report |
| p-alternating-quarters | l12 ($\sum \tfrac{n}{2^n}$, ratios $\tfrac{n+1}{2n}$), l13 quiz ("smallest $n$ for which the bound guarantees an error below 0.001") | 4 for 2 in the first step; that sentence with the same 0.001 | acceptable; the answers differ (31 there, 6 here) |
| p-cube-root-greedy | l14, review-3 (greedy rule, the same wording of the rule) | the rule's statement | the taught rule; series and target new |

## Verified

- Keys: 37 typed and 8 choice keys recomputed by two routes; all agree. `wrong` values: 80 of 80 follow from the slip their line names, land on their own key in the engine's grader and lie clear of the key's band.
- Least $N$: each "smallest" answer is least and holds from there on (brute search, with each gap shown to fall): 16, 2250 and 100001 (set 1); 138, 80, 109, 14 and 6 (set 2); 998, 6 (set 3). Part 4 of `p-cube-root-twenty` asks for the least $n$ beyond the bound (16), not the least $n$ with $s + \tfrac1n \in S$ (12); it says so.
- Stated numbers: every decimal and fraction in a feedback or explanation line, among them $a_9 \approx 6.9997$ (the first term within 0.001 of 7), the series sums $\tfrac{5}{12}$, $\tfrac{4}{25}$ and 0.5718, the steps 2.9, 3.071 and 3.196, the tails 0.0010005 and 0.0009995.
- Claims: $0.55445 < x < 0.55446$ for any tail of 4s and 5s; $|a_n| < 2$ for every $n$ in the strands problem; the Cauchy condition fails at $\varepsilon = 3$ (and for every $\varepsilon$ below 4), so "only for $\varepsilon$ below 3" is rightly a distractor; the second series of `p-telescoping-tail` sums to about 0.3474, below $\tfrac{5}{12}$, and its ratios tend to 1; $\sqrt[3]{n} \le n$ gives the comparison with $\sum \tfrac1n$; the greedy total after 200,000 terms is within 0.03 of 0.2.
- Chain: every later part restates the value it uses; slips carried from the part before have lines (`slip-4` in `p-root-recursion` part 5, `no-half` and `one-start` in `p-telescoping-tail` part 3). Finding 4 is the one loose restatement.
- Bands: each takes the key, the rounding the part asks for and its cut-off form; none takes a `wrong` value. Rounded routes pass ($-0.4237 + 0.6934$).
- Level: nothing beyond the level's lessons. Set 1 uses l1 to l5, set 2 l6 to l10, set 3 l11 to l14; every lesson of each level appears.
- Shape: 3 problems of 5 parts a set, 12 typed parts of 15, one difficulty 5 a set, explanations of at most three sentences.

## Counts

| set | wrong | unclear | minor |
|---|---|---|---|
| problems-1 | 0 | 1 | 1 |
| problems-2 | 0 | 0 | 2 |
| problems-3 | 0 | 0 | 1 |

## Engine

1. A "write as one fraction" `expression` part passes the question retyped. `p-climbing-fractions` part 2 accepts `5-\frac{5n-4}{n+1}` and `p-sum-law-band` part 1 accepts `3-\frac{6n+1}{2n+5}` and `\left|\frac{6n+1}{2n+5}-3\right|`. `"form": "simplified"` does not refuse them (`try-fix.mjs`), so there is no content fix. l6 "Simplify $|a_n - 2|$" is built the same way (not probed). Appended to `docs/BACKLOG-INBOX.md`.

## Fix pass

1. `p-cube-root-twenty` part 1 onward: fixed with the review's four halvings. Recomputed by exact bisection (trail [2.5, 3], [2.5, 2.75], [2.625, 2.75], [2.6875, 2.75]) and by the sixteenths grid (floor(16 x 20^(1/3)) = 43). Part 1 key 2.625 to 2.6875 (`two-steps` 2.5 replaced by `one-short` 2.625). Part 2 key -979 to -2413 (`sign` 979 to 2413, `squares` -839 to -3271, `no-twenty` 8749 to 75411). Part 4 key 16 to 53 (bound 52.16; `round-down` 15 to 52, `no-ones` 11 to 37, new `no-plus-one` 51, the top without its +1 giving 50.47). Part 5 option, questions, lines and explanations carried through. The new numbers do not occur elsewhere in `app/content`.
2. `p-cube-root-twenty` part 5 wording: fixed with the review's two sentences (`feedback.correct`, `explain.text`). Basis: l3 "Case two" (an upper bound below s breaks leastness); s - 1/n is an upper bound when s^3 > 20 for large n.
3. `p-sum-law-band`: fixed with the review's sequences (8n+3)/(2n+5) to 4, (3n-1)/(n+1) to 3, epsilon 0.04. Gaps 17/(2n+5) and 4/(n+1) by symbolic simplification and by exact fractions for n up to 3000. Part 1 key and slips: `plus-one` 16/(2n+5) to 23/(2n+5), `sign` -17/(2n+5). Part 2 key 138 to 423 (`round-down` 137 to 422, `full-band` 68 to 211). Part 3 key 80 to 200 (`equal` 79 to 199, `full-band` 40 to 100). Part 4 key 138 to 423 (`min` 80 to 200, `sum` 218 to 623). Part 5 key 109 to 311 (`proof` 138 to 423, `round-down` 108 to 310; gaps 0.04006 at 310 and 0.03993 at 311, confirmed by the quadratic, root 310.48). Neither formula occurs elsewhere in `app/content`.
4. `p-root-recursion` part 3 restatement: fixed, the question now says the terms rise and stay below 7, so the theorem gives L, with no step named that the part does not use.
5. `p-alternating-quarters` part 5: fixed. `s7` band 0.0001 to 0.00005; new `sum` slip 0.16 (band 0.00004) with the review's line. Checked: 0.16 now reaches `sum`; 0.1601 and 0.1600952 reach `s7`; 0.1597 and 327/2048 still pass the key. Key unchanged.

Counts: 5 fixed, 0 disputed, 0 deferred.

Graded values changed, old to new: set 1 p-cube-root-twenty p1 2.625 to 2.6875, p2 -979 to -2413, p4 16 to 53; set 2 p-sum-law-band p2 138 to 423, p3 80 to 200, p4 138 to 423, p5 109 to 311 (p1 expression key 14/(2n+5) to 17/(2n+5)); set 3 none (a slip added, key unchanged). Wrong values changed as listed above.

Scripts: `docs/reports/problems-analysis-numbers.py` updated (new keys, slips and stated numbers; 532 of 532, exit 0). Reader's `mine.py` updated likewise (435 of 435, exit 0, the finding 5 CLAIM line now a check); `proposed.py` unchanged (15 of 15).

Gates: validator 0 errors, 4522 warnings (unchanged), `manifest.json` restored. `grade-all.mjs --file` on the three sets: 0 failures each. Voice scan 35: 0 and 0. Playthrough `--problems analysis/problems-1`, `-2`, `-3`, desktop and `--mobile`: all passed.
