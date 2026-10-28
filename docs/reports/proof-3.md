# Report: proof level 3, "Proof methods"

Course `proof` (topic 0.6, strand pure), level 3, from `## Level 3` of `docs/briefs/proof.md`. Lesson ids, names, objectives and skills are those of `app/content/courses/proof/course.json` (l10 `pv-direct`; l11 and l12 `pv-indirect`; l13 `pv-induction`; l14 `pv-logic` and `pv-direct`; l15 `pv-writing`). Levels 1 and 2 were written; I read `l3`, `l5`, `l7`, `l9`, both reports and the level 2 generators for notation, voice and workarounds. Proofs end with $\blacksquare$, as in level 2. No topic exam was written.

## Files written

All in `app/content/courses/proof/`.

| File | Screens | Quiz / items | Canvases | Notes |
|---|---:|---:|---|---|
| `l10-direct-proof.json` | 11 | 4 | grid (sums typed into it by `bind`), area, table | even sums, is checking enough, model proof `order` (`same` on the two "write as" lines, example distractor), why $j + k$ is an integer, odd plus odd bracket, odd times odd area and bracket, same-$k$ trap (tap rows), cases proof `order`, 0 and negatives edge, AM-GM `order` (backward distractor), volatility-drag transfer (0.8660) |
| `l11-contrapositive.json` | 11 | 4 | table | stuck at $\sqrt{2m}$, which statement says the same, model proof `order` (converse opening as distractor), bracket $2k^2 + 2k$, build the contrapositive of "$3n + 1$ even ⇒ $n$ odd" (`place`, converse and inverse chips as decoys), bracket $2k^2 - 6k + 2$, converse trap, $n$ even ⇔ $n^2$ even, when a direct proof is shorter, two-position book transfer (`place` with a De Morgan decoy) and its `order` |
| `l12-contradiction.json` | 12 | 4 | number-line (1.41 to 1.42, then zoomed), table | $99^2 - 2 \times 70^2 = 1$, why checking fractions fails, $\sqrt{2}$ proof in two `order` screens with a justification `choice` between, lowest-terms trap (tap rows), Euclid `order` ("$N$ is prime" as distractor), $30031 \div 59 = 509$, $\sqrt{4}$ break (tap rows), no largest integer, bond arbitrage `order` and £1 transfer |
| `l13-induction.json` | 11 | 4 | grid (L shapes, staircase), area, table, plane (log scale) | odd sums table, guess $n^2$, model induction `order`, $(k + 1)^2$ factorised, Gauss step bracket, geometric step $2^{k+1} - 1$, no-base-case trap, base case 5 for $2^n > n^2$, `sum_odds` code screen, compound-growth `order`, £1,628.89 transfer |
| `l14-counterexamples.json` | 11 | 4 | grid (values typed into it), area, number-line, table, venn | $n^2 + n + 41$ for $n = 0$ to 5, then 1681, one case is enough, tap 9, $(a + b)^2$ `multi`, $\sqrt{2} + (-\sqrt{2})$, 2047 = 23 × 89, prime ⇒ odd trap on a venn (region A), `first_failure` code screen, counterexample write-up `order`, 6.5% transfer |
| `l15-proof-a-stranger-can-check.json` | 11 | 4 | pair of tables, table | tap the uncheckable lines of write-up B, what a proof must contain (`multi`), backward scratch to forward proof `order`, missing case, arbitrary or chosen (`place`), $-2 = 2$ squaring trap (tap rows), steps that reverse, correct but not checkable (tap rows), five claims to five methods (`place`), risk-note `order`, colleague's unjustified line (tap rows) |
| `review-3.json` | | 9 | table | difficulties 3, 2, 2, 3, 3, 4, 3, 4, 2; covers l10 (2), l11 (2), l12, l13 (2), l14, l15 (2, one shared with l11) |
| `homework-3.json` | | 9 | table | difficulties 5, 4, 3, 4, 4, 4, 4, 4, 5; sum-of-squares `order` (two distractors) and factorised `expression`, 385, $2^n > n^2$ `order`, $\sqrt{3}$ `order` and its lemma `choice`, `first_mismatch` code item, horses (tap rows), exit-line `longform` (10 one-point rubric lines, full model answer) |

Generators (Python, one per file) and checks are in the scratchpad folder `proof-3` (`gen_l10.py` to `gen_l15.py`, `gen_sets.py`, `common.py`, `checks.py`, `checks2.py`, `voice.py`).

## Validator

`node tools/validate.mjs` from `app/`: **0 errors**, 364 to 365 warnings (the count moved with the markov agent's files), none in a proof file. The course's "not yet written" warning is gone, since every proof lesson, review and homework now exists. No markov errors were reported in any run.

## Playthrough

All with `--local-cdn` set to the scratchpad `pkgs` folder, with `--shots --mobile --why` while authoring and a final clean run of all six lessons together. I looked at the screenshots of every screen and set item.

| Target | Result |
|---|---|
| `--lesson proof/l10-direct-proof` | ok, 15 checks, quiz 4/4 |
| `--lesson proof/l11-contrapositive` | ok, 15 checks, quiz 4/4 |
| `--lesson proof/l12-contradiction` | ok, 16 checks, quiz 4/4 |
| `--lesson proof/l13-induction` | ok, 15 checks, quiz 4/4 (the code solution passes its 6 tests in Pyodide) |
| `--lesson proof/l14-counterexamples` | ok, 15 checks, quiz 4/4 (the code solution passes its 6 tests in Pyodide) |
| `--lesson proof/l15-proof-a-stranger-can-check` | ok, 15 checks, quiz 4/4 |
| `--set proof/review-3` | ok, 9 of 9 recorded |
| `--set proof/homework-3` | ok, 9 of 9 right, 42 of 42 marks |

No set-mode run flaked.

Fixes made after looking at the screenshots:
- l10 cases `order`: each case line was one long formula, which did not wrap at 390 px and pushed the Left out cross off the card. Each formula is now split into two maths spans so the line breaks between them (backlog bullet).
- l10 and l13 hook grids were tall enough to push the table widget off a laptop screen; they are `compact` with `maxHeight`.
- l12 zoomed number-line: the automatic tick labels printed "1.414" five times at step 0.0001. The labels are now an explicit list to 4 places (backlog bullet).
- l12 trap: the prose said the classmate had dropped "in lowest terms" while the table still showed it; the prose now says "suppose a classmate left it out".
- l13 $2^n$ against $n^2$: polyline `functions` entries drew no labels, so the two series were unnamed. The last point of each now carries the label (backlog bullet).
- l14 trap venn: "3, 5, 7, 11, 13" ran out of the lens at 390 px. The universe is now 1 to 10 (backlog bullet).

## Numbers, each computed twice

First pass: `checks.py`, from the brief's data, with every identity tested on all integers from −20 to 20 (or −50 to 50). Second pass: `checks2.py`, which reads the written JSON back, recomputes every `numeric` answer independently, lists every table answer, and runs each code solution and starter against its tests in CPython. No number failed its double check.

- Identities: $(2j + 1)(2k + 1) = 2(2jk + j + k) + 1$; $(2k + 1)^2 = 2(2k^2 + 2k) + 1$; $(2k)^2 - 6(2k) + 5 = 2(2k^2 - 6k + 2) + 1$; $3(2k) + 1 = 2(3k) + 1$; $5(2k) + 3 = 2(5k + 1) + 1$; $(2j + 1) + (2k + 1) = 2(j + k + 1)$; $n^2 + n$ even in both cases, $(2k + 1)(2k + 2) = 2(2k + 1)(k + 1)$.
- Added identities: $7(2k + 1) + 4 = 14k + 11 = 2(7k + 5) + 1$ (l11 quiz); $(2k + 1)^3 = 2(4k^3 + 6k^2 + 3k) + 1$ (l11 quiz); $(2j + 1)(2k + 3) = 2(2jk + 3j + k + 1) + 1$ (review); $(3m + 1)^2 = 3(3m^2 + 2m) + 1$ and $(3m + 2)^2 = 3(3m^2 + 4m + 1) + 1$ (review, homework).
- l10 sums 6, 18, 6, 14. AM-GM: $\sqrt{0.75} = 0.8660$; £100 to £150 to £75; arithmetic mean of 1.5 and 0.5 is 1.0. Quiz: £100 at +20% then −20% is £96, $\sqrt{0.96} = 0.9798$.
- l12: $99^2 = 9801$, $2 \times 70^2 = 9800$, difference 1; $\tfrac{140}{99} = 1.414141$, $\sqrt{2} = 1.414214$, $\tfrac{99}{70} = 1.414286$. $30031 = 2 \cdot 3 \cdot 5 \cdot 7 \cdot 11 \cdot 13 + 1$, remainder 1 on each of the six primes, $30031 = 59 \times 509$ (both prime). $2 \cdot 3 \cdot 5 \cdot 7 + 1 = 211$ (prime). The £1 arbitrage ($96 - 95$); wrong forms 4, 5 and 191.
- l13: odd sums 1, 4, 9, 16, 25; 100 for $n = 10$; 10000 for $n = 100$; 0 for $n = 0$; the slip `range(1, 2*n - 1, 2)` gives 16 for $n = 5$. Gauss 5050. $2^n$ against $n^2$ for $n = 1$ to 7: 2/1, 4/4, 8/9, 16/16, 32/25, 64/36, 128/49; $k^2 \ge 2k + 1$ from $k = 3$; smallest lasting base case 5. Both sides of the trap's line 3 equal $k^2 + 3k + 3$; $n^2 + n + 1$ odd for every $n$. $4^{k+1} - 1 = 4(4^k - 1) + 3$. £1,628.89 compound (also by a ten-step loop), £1,500 simple, £1,102.50 and £1,100 at year 2, £1,551.33 at year 9. Bernoulli checked for $r \in \{-1, -0.5, 0, 0.05, 0.3, 2\}$, $n \le 29$.
- l14: $n^2 + n + 41$ gives 41, 43, 47, 53, 61, 71 for $n = 0$ to 5, first fails at 40 (1681 = $41^2$), then 41 (1763 = $41 \times 43$); $n^2 - n + 41$ first fails at 41; $6n + 5$ at 5 (35); $n^2 + 1$ at 0; $n^2 - n + 11$ gives 11, 11, 13, 17, 23, 31, 41, 53, 67, 83, 101 (all prime) then 121; $2n + 3$ first fails at 3. $2^p - 1$ is 3, 7, 31, 127 for $p = 2, 3, 5, 7$ and $2047 = 23 \times 89$. 9 is the first odd composite. $(1 + 1)^2 = 4$ against 2; $(2 + 3)^2 = 25$ against 13. Portfolio $0.5 \times 8\% + 0.5 \times 5\% = 6.5\%$. Venn on 1 to 10: primes 2, 3, 5, 7; odd 1, 3, 5, 7, 9.
- l15: £10,000 $= 5 \times £2{,}000$. $\sqrt{x + 6} = x$ gives $x = 3$ or $-2$, and only 3 works (review).
- Review: smallest $n$ with $n! > 2^n$ is 4 (24 against 16); $\tfrac{3^k - 1}{2} + 3^k = \tfrac{3^{k+1} - 1}{2}$ (checked for $k \le 29$ as fractions).
- Homework: $1^2 + \dots + 10^2 = 385 = \tfrac{10 \cdot 11 \cdot 21}{6}$, and $10 \cdot 11 \cdot 21 = 2310$; $\tfrac{k(k + 1)(2k + 1)}{6} + (k + 1)^2 = \tfrac{(k + 1)(k + 2)(2k + 3)}{6}$ (checked as fractions for $k \le 29$), bracket $2k^2 + 7k + 6 = (k + 2)(2k + 3)$. Longform: $5(2k) + 3 = 2(5k + 1) + 1$; $\tfrac{r}{2} = \tfrac{p}{2q}$; $2^k - 1 + 2^k = 2^{k+1} - 1$; $11^2 - 11 + 11 = 121 = 11 \times 11$. Rubric 10 × 1 = 10.

### Code tests, with expected values

All expected values were run in CPython (`checks2.py`) and again in Pyodide by the playthrough. Each starter returns `None`.

- l13 `sum_odds(n)`: 1 → 1, 5 → 25, 10 → 100, 100 → 10000, 0 → 0, 2 → 4 (example 3 → 9). Starter fails all 6.
- l14 `first_failure(f, n_max)` (prelude `is_prime`, below 2 not prime): $n^2 + n + 41$, 100 → 40; same, 39 → `None`; $6n + 5$, 20 → 5; $n^2 - n + 41$, 50 → 41; $n^2 + 1$, 10 → 0; $n^2 - n + 11$, 20 → 11 (example $2n + 3$, 10 → 3). Starter passes only the `None` case.
- Homework `first_mismatch(formula, n_max)`: true formula, 50 → `None`; `n*n`, 50 → 2; true formula plus 1 at 12, 50 → 12; true formula below 20 and 0 from 20, 30 → 20; same, 19 → `None`; $n^3 - 2n^2 + 2n$, 10 → 2 (example `n * n`, 5 → 2). Starter passes only the two `None` cases.

## Departures from the brief

- l10: the hook types the four sums into a `table` widget that writes them into a `grid` (`bind`), so the "does checking settle it" question has its own screen. Divisibility ($a \mid b$, $b \mid c$ gives $a \mid c$) is a quiz item, and so is "why both cases". The examples-for-a-proof slip is the quiz item, not a second trap option. The £75 is in the transfer's table and explanation, and the quiz asks for £96 from ±20% instead.
- l11: the opening `choice` has one correct option ("nothing useful"), since a choice needs one. The "choice naming the method" is a quiz item. The trap uses the claim "if $n^2$ is odd then $n$ is odd", whose converse is also true, so the converse opening tempts. The transfer is the `place` build; its three-line proof is an `order` after it.
- l12: the hook asks for $99^2 - 2 \times 70^2$ on the brief's 1.41 to 1.42 line; a second screen zooms to 1.4140 to 1.4145 so that $\tfrac{140}{99}$, $\sqrt{2}$ and $\tfrac{99}{70}$ can be told apart. The $\sqrt{2}$ proof is two `order` screens of four lines each, with the justification `choice` for "$p^2$ even so $p$ even" between them. "No largest integer" is the `generalise` screen's confirmation. The 30031 `numeric` asks for 509; 211 is a quiz item.
- l13: the brief's `expression` answers $\tfrac{(k + 1)(k + 2)}{2}$ and $2^{k+1} - 1$ became "fill the bracket" (`k+2`) and "simplify" ($2^{k+1} - 1$), and $(k + 1)^2$ uses `form: "factorised"`. A free $\tfrac{(k + 1)(k + 2)}{2}$ answer would have accepted the unsimplified left side. The L shapes are on a `grid` rather than `area`, because `area` overlays at most three shadings and the 5 by 5 picture needs five. The divisibility claim (3 divides $4^n - 1$) is a quiz item. The horses argument is a homework item.
- l14: the ∃-claim example ("2 is even and prime") and "which word" are quiz items; the transfer asks for 6.5%. The venn of the trap uses 1 to 10, not 1 to 15, to fit a phone. The code screen has the brief's five tests plus $n^2 - n + 11$ (11).
- l15: the hook is a `pair` of two tables with taps on write-up B only. "Let $x$ be arbitrary" against "take $x = 2$" is a `place` with two slots, not a `choice`. The five methods `place` puts the claims in a table and labels the slots "Claim A" to "Claim E".
- Homework: the sum-of-squares bracket `expression` asks for the factorised $(k + 2)(2k + 3)$ with `form`. The $\sqrt{3}$ lemma is a `choice` item beside the `order`. The longform rubric is ten one-point lines, two per part, matching the brief's "1 for the method set up, 1 for every step justified".

## Proposed course.json change

None.

## Conventions

No datasets or seeds. Money in £. Even $n = 2k$, odd $n = 2k + 1$, $a \mid b$ for divides, proofs ending with $\blacksquare$. Earlier lessons are named by title in prose ("as in If, then", "Proving the contrapositive").
