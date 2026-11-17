# Delta read AG, measure-prob problem sets 1 to 3: the four re-authored problems and the fix-pass parts

Brief `docs/briefs/delta-read-af.md`. Review read: `docs/reviews/review-problems-measure-prob-1-3.md` with its `## Fix pass`. Commit range `9e67f72c..470b65ad` on `app/content/courses/measure-prob/problems-1.json`, `-2`, `-3`. No browser, no content or engine edit.

Counts: `wrong` 0, `misleading` 5 (one a band that refuses its own printed working), `reuse` 1 (one part, with a replacement), `re-author` 0, `continuity` 3, `voice` 0. Every key, every `wrong` value and every other printed number in scope agrees with mine. All seven fixes (3, 4, 7 to 11) were applied as the reader wrote them, character for character. No replacement problem retells course material as a chain; one part of one does (finding 4).

## Scope

- Re-authored, whole items: `p-quote-ladder` (was `p-reciprocal-grid`), `p-settlement-fails` (was `p-billed-hours`), `p-boom-bust` (was `p-root-of-uniform`), `p-trial-stake` (was `p-red-card-call`).
- Renamed: `p-no-double-four` (was `p-no-double-seven`), whole item read.
- Fix-pass parts: `p-compounding` parts 2 and 3 (findings 8, 7); `p-random-maturity` part 2 (9); `p-nested-forecasts` part 5 (10); `p-two-ups-stop` part 3 (11).

## Method

Each part was worked from its text before its key was read. `docs/reports/delta-review-delta-ag-measure-prob-numbers.py` imports no earlier script and uses the standard library only. Routes: the ladder law in exact fractions, and $P(X \le 2U)$ again on a grid of 400,000 levels with $N$ found by search; the fails law summed to 400 terms, with $E[N]$ and the variance checked against the negative binomial forms $2q/p$ and $2q/p^2$, and $G$, $G'$, $G''$ against the series at several $s$; the capital by the binomial law of the up days, the 16 paths of four days, and the tail sum to day 6,000; the biotech tree by its four leaves, $M_n$ at each node, the martingale step at each node and both selling rules run path by path; the digit strings by listing all strings to length 5 with the block 44. Each `wrong` value is rebuilt from the slip its line names. Each band is rebuilt with the engine's rule (`_base.js`: `|x - answer| <= abs + 1e-12`) and fed the key and each slip typed at the places asked, and each figure the printed working gives.

Pass 8 rules were checked by hand on every numeric part in scope: each printed quotient worked through at the figures printed, each key and slip against a tie at the asked places, each pair of bands for overlap, the source of $\Phi(0.5)$, and whether a question or an earlier slip line hands over a key.

Proof checks. Every definition was read against the lesson's wording (simple function, l5 screen 3; monotone convergence, l6 screen 2; Fatou, l6 screen 5; almost surely, l8 screen 2; Chebyshev's proof, l8 screen 6; stopping time, l13 screen 2; Doob martingale, l12 screen 2). Every hypothesis was checked as stated.

Reuse. Every learner-facing string of l1 to l17, `review-1` to `-4`, `homework-1` to `-4`, `problems-4` and `exams/topic-3.2.json` was dumped to one file and searched for each number, noun and step. The course's exam items were found by skill id (`mt-sigma`, `mt-integral`, `mt-condexp`, `mt-martingale`, `mt-change`): 11 items, all in `topic-3.2`; no stage or mock exam carries one. Each story was then searched over all of `app/content` (mock exams, `bank`, `puzzles`, `brainteasers`, `markov`, `conditional`, `limits-thm` included) by keyword and key number.

## Tool results

| check | result |
|---|---|
| author's script `problems-measure-prob-numbers.py` | 800 checks, 0 failures |
| reader's script `problems-measure-prob-numbers-read.py` | 665 checks, 0 findings |
| `delta-review-delta-ag-measure-prob-numbers.py` | 470 checks, 9 FINDING lines (findings 1 to 9), exit 0; 0 FINDING lines on the scratch copy with the fixes |
| validator | 0 errors; on the three sets only three advisory `O2-long-sentence` lines; `manifest.json` unchanged |
| voice scan 35, course folder | 0 and 0 |
| `fresh-check --file`, each set | 0 hits |
| `grade-all --file`, each set | 19, 19 and 18 widgets, 0 failures |

The validator and `fresh-check` see none of findings 1 to 9. All nine fix texts were applied to a copy of `app/` in the scratch folder (`delta-review-delta-ag-measure-prob/app`, script `apply.py`) and passed validator (0 errors, no new warning), voice scan, `fresh-check --file` and `grade-all --file` there. The worktree content is untouched.

## Verdict per item

| item | scope | numbers | bands, pass 8 | closest lesson screen | quiz | review | homework | other set | exam | reuse |
|---|---|---|---|---|---|---|---|---|---|---|
| `p-quote-ladder` | whole | clean | clean | l4 "Outcomes behind a value", "Pushing a measure forward"; l2 "Why countable unions" (finite and cofinite sets, the even numbers) | l2 `q-two` | `r-events` | `h-build-space` ($p_k = \tfrac{1}{k(k+1)}$) | `p-ball-machine` (atoms of $\sigma(X)$) | `e-atoms-three-sets` | `clean`: no $\tfrac1n$ tail, no left limit, no continuity part; finding 7 is a wording line |
| `p-settlement-fails` | whole | clean | clean | l6 "Summing the tail"; l5 "A payout with no ceiling", "Does every random variable have a mean?"; l6 "Edge case: an infinite limit" | l6 `q-inf`, `q-sum` | `r-heavy` ($1.5^K$), `r-tail` | `h-geom` | `p-compounding` (which theorem) | `e-tail-integral` | parts 1 to 4 `clean`; part 5 `reuse` (finding 4) |
| `p-boom-bust` | whole | clean | finding 1 (part 4) | l8 "Mean square implies in probability", "The spike in mean square"; l3 "The union bound" | l8 `q-cheb` | `r-cheb`, `r-mode` | `h-modes`, `homework-1` `h-long` | `problems-4` `p-ten-trades` (see note) | `e-swap-limits` | `clean` |
| `p-trial-stake` | whole | clean | clean | l12 "The forecaster"; l13 "Optional stopping, bounded case", "Stops, targets and the daily high" | l12 `q-doob` | `r-doob`, `r-tower` | `h-prove-urn`, `h-long` | `p-two-ups-stop` part 3 (same theorem, same set) | `e-ruin-by-martingale`, `e-variance-split` | `clean` |
| `p-no-double-four` | whole | clean | clean | l1 "Covering the rationals", l3 "The union bound" | l1 `q-irrational` | `r-union` | `h-borel` ("no digit 7"), `h-long` | none | none | `clean`: the shared digit is gone |
| `p-compounding` | parts 2, 3 | clean | clean | l7 "A dominated sequence" | | `r-dom` | | | | `clean`: fixes 7 and 8 exact |
| `p-random-maturity` | part 2 | clean | n/a | l7 "Swapping derivative and expectation" | | `r-delta` | | | | `clean`: fix 9 exact |
| `p-nested-forecasts` | part 5 | clean | clean | l10 "Splitting the variance" | | `r-die` | `h-proj` | | | `clean`: fix 10 exact |
| `p-two-ups-stop` | part 3 | clean | clean | l13 "Optional stopping, bounded case" | | `r-stop` | | | | `clean`: fix 11 exact |

Note on `p-boom-bust`. The factors 1.6 and 0.4 at chance $\tfrac12$ are the one-step weights $\tfrac{dQ}{dP}$ of `problems-4` `p-ten-trades` (win chance 0.5 under $P$, 0.8 under $Q$). That problem prints only $\tfrac{dP}{dQ}$ (0.625 and 2.5) and never a product that dies, so nothing is shared on the page. The bound 1.1455 here and the weight 0.1455 there are a coincidence of digits.

## The two parts the author named

**`p-trial-stake` part 1: `clean`.**
Problem: "Find $M_1$ on the event that the trial succeeds. Give your answer in £ to 2 decimal places." Explain: "Average from the end back: approval gives $E[X] = 90$, and a success mixes 90 with 40 in the ratio 0.75 to 0.25. So $M_1 = 77.50$."
l12 "The forecaster": "Three fair tosses. Let $X = 1$ if at least two are heads, else 0. After each toss, a forecaster quotes $E[X \mid \mathcal{F}_n]$. Type her quote at each node as a decimal." Hint: "At the last level the quote is $X$ itself. Work backwards." Nearest of all is `r-doob`: "A coin lands heads with chance 0.8. Three tosses are made, $X$ is the number of heads, and $M_n = E[X \mid \mathcal{F}_n]$. What is $M_1$ when the first toss is H?"
One Doob value on a tree is the level's standard task. The tree here has unequal chances, branches of unequal depth and its own story; no number, sentence or line is shared, and the value feeds a stopping rule that no course item has. A learner would see practice, not a retelling.

**`p-settlement-fails` part 5: `reuse`** (finding 4, with a replacement).
Problem: "A harsher schedule charges $5^N$, in £000. By the step of part 1, what is $E[5^N]$?" Options: "It is infinite: the step of part 1 gives $\sum_k 0.64(k + 1)$, which diverges"; "It does not exist, since $\tfrac{16}{(5 - s)^2}$ is undefined at $s = 5$" (why: "A non-negative variable always has a mean in $[0, \infty]$. ..."); "It is finite, since $5^N$ is finite at every outcome"; "It is large but finite, since the chances $0.2^k$ shrink fast" (why: "They shrink at exactly the rate $5^k$ grows: $5^k \times 0.2^k = 1$. ...").
l5 "Does every random variable have a mean?": "A colleague says the chances $2^{-k}$ shrink fast, so $E[X]$ must be a finite number." Options: "$\infty$: the capped means rise without bound."; "Finite, because the chances $2^{-k}$ shrink." (why: "You trusted the shrinking chances. The payouts $2^k$ grow just as fast, so every term is 1."); "Undefined: no mean exists." (why: "... For $X \ge 0$ the integral is always defined, possibly $\infty$."). Feedback: "Every $X \ge 0$ has a mean in $[0, \infty]$, and this one is infinite."
The payout is again a power whose growth cancels the chances exactly, the same three answers are offered (infinite, finite because the chances shrink, undefined), and two `why` lines are the lesson's lines in other words. With part 1 the pair is also `review-2` `r-heavy` beside it ("A game pays $X = 1.5^K$ ... Shrinking chances beat the growth here because $1.5 < 2$", "unlike $2^K$"): the author's own inbox note says a draft charged $1.5^N$ and was moved to $1.25^N$. Part 1 alone is a standard task with its own law and stays. Parts 2 to 4 are new.

## What changed in `p-no-double-four`, and why

Three things, all from the first read. (a) Finding 3: the block is 44, not 77, because `homework-1` `h-borel` is "the set of $x \in [0, 1]$ with no digit 7". A field-by-field diff against `9e67f72c` shows 22 strings changed by the digit alone; no number moved, and $0.1111\ldots$ in the `surely` line stays. (b) The id follows the digit. The set was first committed on 2026-11-17 in this session and has never shipped, so no progress data keys on the old id; the two number scripts are the only files that name the old ids, in comments. (c) Finding 4: part 2 gained the slip `independent`, 0.97119 with band 0.0003, for the learner who multiplies $P(D_3) \times 0.99$. Recomputed: $0.981 \times 0.99 = 0.97119$; typed at 3 places it is 0.971, inside $[0.97089, 0.97149]$; the key band $[0.9718, 0.9722]$ is clear of it; `square` (0.9624, band 0.0005) and `one-term` are clear of it too. Its line is the reader's, word for word. Counts recomputed with the digit 4: 99, 981, 9720, 96309; 19 three-digit strings hold 44; $P(D_{200}) = 0.1599$ lies between $0.99^{199}$ and $0.99^{100}$.

## Findings

1. `misleading` (band refuses the printed working) | `measure-prob/problems-2.json` | `p-boom-bust` | `items[2].parts[3].feedback.correct` | The line prints "$10 \times \tfrac{0.0000266}{0.0513} \approx 0.00518$". Those figures give $0.0051852$, which is 0.00519 at the 5 places asked. The band is $0.005176 \pm 0.000005$, so a learner who checks the line by hand gets a figure the part refuses. $0.9^{100} = 0.0000265614$; three figures are too few here.
   Fix: "The sum is geometric with ratio $\sqrt{0.9}$: $10 \times \tfrac{0.9^{100}}{1 - \sqrt{0.9}} = 10 \times \tfrac{0.00002656}{0.0513} \approx 0.00518$." Check: $0.0002656 / 0.0513 = 0.0051774$, typed 0.00518, taken. The `explain` line ($1 - 0.9487$ with the learner's own $0.9^{100}$) gives 0.0051776 and is fine.

2. `continuity` | `measure-prob/problems-2.json` | `p-settlement-fails` | `items[0].parts[0].feedback.byKey.jensen` | "That is $1.25^{E[N]} = 1.25^{0.5}$." Part 3 asks for $E[N]$ and its key is 0.5. The same class as finding 7 of the first read.
   Fix: "That is $1.25^{E[N]}$, a power of the mean. A mean does not pass inside a power. Weight each value $1.25^k$ by its own chance."

3. `continuity` | `measure-prob/problems-3.json` | `p-trial-stake` | `items[3].parts[3].explain.text` | "its mean is 54.5 by part 4" sits in part 4 itself. The mean comes from part 3.
   Fix: "$M_T$ is 90, 20 or 40 with chances 0.45, 0.4 and 0.15, and its mean is 54.5 by part 3. So $\mathrm{Var}(M_T) = 4045 - 2970.25 = 1074.75$."

4. `reuse` | `measure-prob/problems-2.json` | `p-settlement-fails` | `items[0].parts[4]` | Part 5 is l5 "Does every random variable have a mean?" in other numbers; texts above. The key option is also the only one that repeats the question's own words ("the step of part 1").
   Fix: replace the part. The new part keeps the infinite mean and tests a step no course item has: a closed form read outside the range it was derived for.
   - `question`: "Part 2 gave $G(s) = \tfrac{16}{(5 - s)^2}$ for $0 \le s < 5$. A harsher schedule charges $6^N$, in £000. What is $E[6^N]$?"
   - option `inf`, correct: "It is infinite: the series has terms $0.64(k + 1)\,1.2^k$, which grow"
   - option `formula`: "It is 16, the value of $\tfrac{16}{(5 - s)^2}$ at $s = 6$"; `why`: "The closed form holds only for $s < 5$, where the series converges. At $s = 6$ the terms $0.64(k + 1)\,1.2^k$ grow, so the sum is infinite."
   - option `finite`: "It is finite, since $6^N$ is finite at every outcome"; `why`: "A variable that is finite everywhere can still have an infinite mean. Here the terms of the series do not shrink."
   - option `power`: "It is $6^{E[N]} = 6^{0.5} \approx 2.45$"; `why`: "That puts the mean inside the power, the slip of part 1. $E[6^N]$ weights each value $6^k$ by its own chance."
   - `feedback.correct`: "Monotone convergence gives $E[6^N] = \sum_k 6^k \times 0.64(k + 1)\,0.2^k = \sum_k 0.64(k + 1)\,1.2^k = \infty$."
   - `feedback.generic`: "Not quite. Write out the series of part 1 with $6^k$ in place of $1.25^k$."
   - `explain.text`: "Each term is $0.64(k + 1)(0.2 \times 6)^k = 0.64(k + 1)\,1.2^k$. The terms grow, so the sum and the mean are infinite. The closed form gives 16 at $s = 6$, but it was derived only for $s < 5$."
   Recomputed: $0.2 \times 6 = 1.2$; $\tfrac{16}{(5 - 6)^2} = 16$; $\sqrt6 = 2.449$. Layout `stack`, as now. The author's script checks this part's key id, which stays `inf`, and the terms of $5^N$ (line 354), which the fixer moves to $6^N$; the reader's script has no check on it. If the main session keeps the part as it is, the entry for KNOWN_ISSUES is: "`p-settlement-fails` part 5 retells l5 screen 8 with $5^N$ for $2^K$".

5. `misleading` (minor) | `measure-prob/problems-2.json` | `p-boom-bust` | `items[2].parts[4].question` | "The bound of part 4 shrinks to 0 as the start day grows, so $M_n \to 0$ almost surely." The bound of part 4 is for the level 0.01 alone, and it gives only that $M_n$ ends below 0.01. Almost sure convergence (l8: "$P(X_n \to X) = 1$") needs the same for every level. It does hold: the bound is $\tfrac{0.9^{m/2}}{(1 - \sqrt{0.9})\sqrt\varepsilon}$ from day $m$, for any $\varepsilon$.
   Fix: "The bound of part 4 shrinks to 0 as the start day grows. The same holds with any $\varepsilon > 0$ in place of 0.01, so $M_n \to 0$ almost surely. Yet each day $E[M_{n+1}^2] = 1.36\,E[M_n^2]$. Find $E[(M_{10} - 0)^2]$, the mean-square distance of $M_{10}$ from that limit. Give 2 decimal places."

6. `misleading` (minor) | `measure-prob/problems-2.json` | `p-settlement-fails` | `items[0].parts[1].explain.text` | "For fixed $N$, $s^{N-1}$ rises with $s$ on $[0, 1]$" is false at $N = 0$, where $s^{-1}$ falls and is undefined at 0. The product $Ns^{N-1}$ is 0 there, so the conclusion holds.
   Fix: "For each $N \ge 1$, $s^{N-1}$ does not fall as $s$ rises on $(0, 1]$, and for $N = 0$ the term is 0. So $Ns^{N-1}$ rises to $N$, and all are non-negative. Their means then rise to $E[N]$ by monotone convergence, with no bound on $N$."

7. `misleading` (minor) | `measure-prob/problems-1.json` | `p-quote-ladder` | `items[2].parts[3].widget.options[1].why` (`countable`) | "There is one for each set of values, and those sets are uncountable." Each set of values is countable; it is the family of sets that is uncountable.
   Fix: "That counts only the atoms. Every union of atoms is an event too. There is one for each set of values, and there are uncountably many such sets."
   Noted, not ruled: that the subsets of $\{0, 1, 2, \dots\}$ are uncountable is taught in `analysis` l5, which level 1 does not list as a prerequisite. The other three options fall to course material alone (l2 "Why countable unions", the band cut by $\{U \le 0.5\}$, atoms against events), so the part can be passed without it.

8. `continuity` (minor) | `measure-prob/problems-3.json` | `p-trial-stake` | `items[3].parts[1].feedback.generic` and `items[3].parts[2].widget.options[3].text` (`law`) | "the first day $M_n$ reaches 80" and "the law of the selling day": $n$ counts pieces of news, and the prose names no days.
   Fix, `generic`: "Not quite. Find the first $n$ at which $M_n$ reaches 80 on each path." Option `law`: "Neither can be found without the law of $T$". Its `why` stays.

9. `misleading` (minor) | `measure-prob/problems-2.json` | `p-settlement-fails` | `items[0].parts[1].widget.options[1]` (`dct`) | "Dominated convergence with $Y = N$, since $Ns^{N-1} \le N$" is marked wrong, yet it is a true statement: $E[N] = 0.5$ is finite, so $Y = N$ does dominate. Its `why` says only that the mean is not yet known. A learner who sees from the series that $E[N]$ is finite is marked wrong for a valid proof.
   Fix: make the option claim what is false. Text: "Dominated convergence with $Y = N$, which needs no further check since $Ns^{N-1} \le N$". `why`: "The bound $Y = N$ must have a finite mean, and $E[N]$ is the number being found. Monotone convergence needs no bound."

## Verified with no finding

- Keys and slips. All 17 numeric keys, 2 expression keys, 5 choice keys and 51 `wrong` entries of the five whole items agree with mine; so do the numbers of the five fix-pass parts ($2e^{0.125} \times 0.6915 = 1.567$; $\Phi(0.5) = 0.6915$ from `erfc`; $1.024 + 4.096$ and 3.38; 0.625 and $-0.625$ over the 16 paths).
- Bands. Every key typed at the places asked is taken; every slip typed at the places asked is refused by the key and lands in its own band; no two bands meet; no key or slip sits on a rounding tie at the asked places. $0.00027$ and $0.00052$, the 5-place forms of the slips of `p-boom-bust` part 4, are inside their bands by $10^{-6}$ and $3 \times 10^{-6}$. No percentage part exists. The only table value, $\Phi(0.5)$, is printed in the part that uses it.
- Printed working, other than finding 1: $0.6/0.936$, $0.64/0.5625$, $0.81/0.7071$ (1.14552, taken), $96/256$, $32/64$, $4045 - 2970.25$.
- Definitions. "Simple" is used twice and rightly both times: the partial sums $\sum_{k \le m} 1.25^k \mathbf{1}_{\{N = k\}}$ and the two-valued $\sqrt{M_1}$ take finitely many values (l5: "A **simple function** takes finitely many values"). Monotone convergence is used only on non-negative rising terms, and "finite or not" matches l6 ("The limit $E[X]$ may be $\infty$"). Fatou's inequality is stated the right way round. The indicator bound $\mathbf{1}_{\{M > \varepsilon\}} \le \sqrt{M/\varepsilon}$ holds on every value and follows l8's proof. The union bound of part 4 needs no independence. $E[M_n] = 1$ and $E[\sqrt{M_n}] = 0.9^{n/2}$ hold for $n$ up to 11 by the binomial law.
- `p-trial-stake`. $M$ is a martingale at every node; neither rule stops at $n = 0$ ($M_0 = 54.5$ lies between 45 and 80); both rules are decided by the news so far and stop by 3; both means are 54.5 path by path; $\mathrm{Var}(X) - \mathrm{Var}(M_T) = 180 = 0.45 \times 400$, the variance left inside the sale.
- `p-quote-ladder`. "The first rung at or above it" agrees with $0.4^{N+1} < U \le 0.4^N$; the cut-off $0.5 \times 0.4^k$ lies above each floor; the `swap` expression $0.4 \times 0.6^k$ equals the key at $k = 1$ only, and the engine still routes it (grade-all).
- Working backwards and word matching. No numeric part can be reversed from a printed target. Three parts are near free and noted, not ruled, as in the first read: `p-boom-bust` part 5 (the question prints 1.36, the answer is its tenth power); `p-settlement-fails` part 3 (one substitution, by design of part 2); `p-trial-stake` part 3, where the question prints $M_0 = 54.5$ and only the key option carries £54.50 (the two distractors are the beliefs the level corrects, and part 4 needs the value).
- Stories over `app/content`. Biotech, trial and approval: no hit beyond single nouns. Settlement: `limits-thm/problems-1` `p-settlement-checks` samples 50 of 2,000 trades for failing ones, another course and another task. A capital multiplied each day: no item with these factors or with the pair "mean 1, dies almost surely"; `integrals/problems-3` `p-log-return` has one closing line on shrinking wealth, with a uniform return. Ladder and rung: none. The key numbers 77.5, 54.5, 1074.75, 21.65, 1.1455, 0.00518, 25/39, 256/225 occur nowhere else in a like setting.
- The first read's "not to walk" lists. `p-quote-ladder` has no $\tfrac1n$ tail, left limit or continuity step. `p-settlement-fails` has no tail sum, cap, grid or layer cake. `p-boom-bust` has none of the five exam sequences, no layer cake, and its bound is a root-moment bound at $\varepsilon = 0.5$, not `r-cheb`. `p-trial-stake` has no cards, urn or coin game.

## Engine

1. `[working-band]` reads the last printed figure only (third report: `review-delta-ag-ito` findings 1 and 1b, and finding 1 here). It should evaluate a printed quotient or product of printed figures and test the result against the band.
2. A slip line that prints a later part's key is found only by reading (first read findings 7 and 11, finding 2 here: three times, so a rule is due). Rule: no `byKey` line, `generic` line or option `why` of part $k$ holds the `answer` of a later numeric part of the same item, as a number or as a power with that exponent, unless the question of part $k$ prints it.
3. An `explain` or `feedback` line of part $k$ that cites "part $k$" itself, or a later part, is cheap to flag (finding 3).
4. `fresh-check` reads `why` lines but did not match "A non-negative variable always has a mean in $[0, \infty]$" against l5's "Every $X \ge 0$ has a mean in $[0, \infty]$", nor the option set of a choice part against the option set of a lesson choice screen (finding 4).
