# Report: proof level 2, "Sets and functions"

Course `proof` (topic 0.6, strand pure), level 2, from `## Level 2` of `docs/briefs/proof.md`. Lesson ids, names, objectives and skills are those of `app/content/courses/proof/course.json` (l6 `pv-sets`; l7 `pv-sets`, `pv-direct`; l8 `pv-sets`; l9 `pv-sets`, `pv-direct`). Level 1 was written, and `l2` to `l5` were read for notation and voice.

## Files written

All in `app/content/courses/proof/`.

| File | Screens | Quiz / items | Canvases | Notes |
|---|---:|---:|---|---|
| `l6-sets.json` | 11 | 4 | grid (1 to 20), number-line, table | multiples of 3 tap, set/list/rule, $\|A\|$, repeats, subset tap, $[0, 1)$ tap, $2^3$ subsets table, $\in$ against $\subseteq$ trap, vacuous $\varnothing \subseteq A$, subset proof `order` with distractor, why $2k$ is an integer, stock-screen transfer |
| `l7-combining-sets.json` | 12 | 4 | venn (two and three sets, elements in regions), table | union, intersection, difference, complement taps, inclusion-exclusion, distributing-the-complement trap, De Morgan, element-chasing `order` with distractor, reasons by `place` assign, reversal `choice`, distributive law, momentum/value transfer |
| `l8-functions-as-sets.json` | 11 | 4 | grid ($A \times B$), graph (arrow diagram), table | seating pairs, $\|A \times B\| = 12$, two desks, no desk, building the arrows with `place` `onPlace`, the arrow that breaks the rule, $4^3 = 64$, everyone-on-FX trap, domain/codomain/image, $x^2$ on $\mathbb{Z}$ against $\mathbb{R}$, data-mapping transfer |
| `l9-one-to-one-onto.json` | 11 | 4 | graph, table, number-line, plane, grid | unhit desks, shared desk, one-to-one, how-to-start trap, one-to-one `order` with distractor, reasons by `place`, onto `expression`, $f^{-1}(11)$, $x^2$ by domain, 24 one-to-one functions, ids/hash/currency transfer |
| `review-2.json` | | 8 | venn, grid, graph | difficulties 2, 3, 2, 3, 3, 3, 3, 4; covers l6 (2), l7 (2), l8 (1), l9 (3), interleaved |
| `homework-2.json` | | 9 | venn | difficulties 4, 4, 3, 3, 4, 3, 4, 5, 5; two `order` derivations with distractors, one `expression`, one `longform` (10-point rubric, model answer) |

Generators (Python, one per file) and checks are in the scratchpad folder `proof-2` (`gen_l6.py` to `gen_l9.py`, `gen_review.py`, `gen_hw.py`, `common.py`, `common_graph.py`, `checks.py`, `checks2.py`, `voice.py`). Proofs end with $\blacksquare$ throughout.

## Validator

`node tools/validate.mjs` from `app/`: **0 errors**, 366 warnings, none in a level 2 proof file (the only proof warning is the course's "not yet written" line for level 3). No markov errors were reported while I ran it.

## Playthrough

All with `--local-cdn` set to the scratchpad `pkgs` folder. Each lesson was also run with `--shots --why` and with `--mobile`; the sets with `--shots` and `--mobile`. I looked at the screenshots of every screen.

| Target | Result |
|---|---|
| `--lesson proof/l6-sets` | ok, 15 checks, quiz 4/4 |
| `--lesson proof/l7-combining-sets` | ok, 16 checks, quiz 4/4 |
| `--lesson proof/l8-functions-as-sets` | ok, 15 checks, quiz 4/4 |
| `--lesson proof/l9-one-to-one-onto` | ok, 15 checks, quiz 4/4 |
| `--set proof/review-2` | ok, 8 of 8 recorded |
| `--set proof/homework-2` | ok, 9 of 9 right, 40 of 40 marks |

No set-mode run flaked.

Fixes made after looking at the screenshots:
- l6 interval: tappable points at 0 and 1 hid the interval's filled and hollow end dots, so 1 looked included. The interval now sits on `row: 2` above the axis, with point labels below.
- l7 and homework three-set venn: the "∅" region value drew as a tiny "ø". The two empty regions now say "empty".
- l8 and l9 arrow diagrams: four pill desks in one horizontal lane overlapped at 390 px. Traders now sit in a left column and desks in a right column, with a caption naming the sides.
- l8 arrows (`place` with `onPlace`): the first Why? sheet showed only two of the three arrows. The cause was each FX chip being listed in both Ana's and Cal's `accepts`. The widget then treats Cal's slot as both chips' only home, so a correct learner would have been marked wrong. Each chip is now listed in one slot, with `byText`. I made the same fix in l7's reasons screen, where "Definition of complement" appears twice (backlog bullet).
- l9 onto screen: the illustration arrow ran from 11 to 3, which gave away the next screen's $f^{-1}(11)$. It now runs from 8 to 2.

## Numbers, each computed twice

First pass: `checks.py`, from the brief's data. Second pass: `checks2.py`, which reads the written JSON back. It parses grid cell text, venn region strings and graph edges into sets, then recomputes each answer. No number failed its double check.

- Multiples of 3 up to 20: 3, 6, 9, 12, 15, 18 at `r1c3`, `r2c1`, `r2c4`, `r3c2`, `r3c5`, `r4c3`; $|A| = 6$. Multiples of 6: 6, 12, 18 (`r2c1`, `r3c2`, `r4c3`), all in $A$. 13 is $3 \times 4 + 1$, 20 is $3 \times 6 + 2$, 10 is $3 \times 3 + 1$.
- $|\{1, 2, 2, 3\}| = 3$; $\{1, 2, 2, 3\} = \{3, 1, 2\}$. $[0, 1)$ holds 0, 0.25, 0.75 and not −0.5, 1, 1.5.
- Subsets of $\{a, b, c\}$ by size: 1, 3, 3, 1, total $8 = 2^3$. Four products: $2^4 = 16$ (15 without $\varnothing$). $|\{\varnothing\}| = 1$. $\{n : 1 \le n \le 20, 5 \mid n\} = \{5, 10, 15, 20\}$.
- l6 transfer (invented stocks): P/E below 10 are Avonmore 6.8, Bridgegate 8.9, Dunmore 7.5 and Fenwick 9.7. With yield above 5% as well: Avonmore 7.1%, Bridgegate 5.6% and Fenwick 6.3%, a subset.
- l7, $U = \{1, \dots, 12\}$: $A = \{2, 4, 6, 8, 10, 12\}$, $B = \{3, 6, 9, 12\}$. $A \cup B = \{2, 3, 4, 6, 8, 9, 10, 12\}$ (8). $A \cap B = \{6, 12\}$, $A \setminus B = \{2, 4, 8, 10\}$, $B \setminus A = \{3, 9\}$ and $A^c = \{1, 3, 5, 7, 9, 11\}$. $6 + 4 - 2 = 8$.
- l7 De Morgan: $(A \cup B)^c = A^c \cap B^c = \{1, 5, 7, 11\}$. The wrong $A^c \cup B^c = \{1, 2, 3, 4, 5, 7, 8, 9, 10, 11\}$ has 10 elements, and so does $(A \cap B)^c$, since $12 - 2 = 10$.
- Three sets, with $C = \{4, 8, 12\}$: regions A only $\{2, 10\}$, B only $\{3, 9\}$, C only empty, AB $\{6\}$, AC $\{4, 8\}$, BC empty, ABC $\{12\}$, none $\{1, 5, 7, 11\}$. $A \cap (B \cup C) = (A \cap B) \cup (A \cap C) = \{4, 6, 8, 12\}$.
- l7 transfer: $40 + 25 - 10 = 55$ pass at least one, so $100 - 55 = 45$ pass neither. The regions are momentum only 30 and value only 15. Wrong answers: 35 ($100 - 65$) and 25 ($100 - 75$).
- l7 quiz: disjoint $5 + 7 = 12$; complements $100 - 12 = 88$ and $600 - 12 = 588$.
- l8: $|A \times B| = 3 \times 4 = 12$ and $4^3 = 64$ functions (wrong forms 7, 81 and 24). The seating function's image is $\{\text{FX}, \text{Rates}\}$. There is 1 function from $\varnothing$ ($4^0$). 2 analysts to 5 projects: $5^2 = 25$ (wrong forms 32, 10, 20).
- l8 transfer tickers and sectors (BARC and LLOY banks, SHEL and BP. energy, AZN pharma) are real classifications. Banks maps to two tickers.
- l9: the desks never reached are Equities and Credit; Ana and Cal share FX. $f(x) = 3x + 2$: $f^{-1}(y) = (y - 2)/3$. $f^{-1}(11) = 3$ and $f(3) = 11$; $f^{-1}(-4) = -2$ and $f(-2) = -4$. Wrong forms: $f(11) = 35$, $(11 + 2)/3 = 4.33$ and $(-4 + 2)/3 = -0.67$. Examples: $f(1) = 5$, $f(2) = 8$.
- $g(x) = x^2$: $g(-2) = g(2) = 4$, and no real $x$ has $x^2 = -1$.
- One-to-one functions from 3 traders to 4 desks: $4 \times 3 \times 2 = 24$, of which 0 are onto (brute force). From 3 to 3 there are $3! = 6$, all onto. The 3 to 3 count with repeats is $3^3 = 27$.
- l9 transfer: 5,000 ids into 1,024 buckets forces a collision. £200 × 1.25 = \$250 and \$250 / 1.25 = £200; the wrong form is $250 \times 1.25 = 312.5$. For $h(x) = 5x - 1$, the onto witness is $x = (y + 1)/5$.
- Review: primes to 10 are $\{2, 3, 5, 7\}$ and the odd numbers are $\{1, 3, 5, 7, 9\}$, so $(A \cap B)^c = \{1, 2, 4, 6, 8, 9, 10\}$ (7). $18 + 15 - 7 = 26$, so $30 - 26 = 4$ (wrong forms −3 and −10). $h(x) = 2x - 6$ gives $h^{-1}(y) = (y + 6)/2$, with $h^{-1}(4) = 5$ and $h(5) = 4$. One-to-one from 2 to 5: $5 \times 4 = 20$ (25 counts all functions, $\binom{5}{2} = 10$).
- Homework: $|\{1, \{1\}, \{1, 2\}\}| = 3$. The $B \cup C$ computations:
  - $B \cup C = \{3, 4, 6, 8, 9, 12\}$, so $A \setminus (B \cup C) = \{2, 10\}$.
  - $A \setminus B = \{2, 4, 8, 10\}$ and $A \setminus C = \{2, 6, 10\}$, which meet in $\{2, 10\}$.
  - The "or" distractor gives $(A \setminus B) \cup (A \setminus C) = \{2, 4, 6, 8, 10\}$.
- Homework inverse: $g(x) = 5x - 7$ gives $g^{-1}(y) = (y + 7)/5$. $g^{-1}(8) = 3$ and $g(3) = 8$; the wrong forms are $g(8) = 33$ and $(8 - 7)/5 = 0.2$.
- Homework onto count, 4 to 3: brute force gives 36. As a check, $\binom{4}{2} \times 3! = 6 \times 6 = 36$ and $3^4 - 3 \times 2^4 + 3 = 81 - 48 + 3 = 36$.
- Longform counterexample: $A = \{1\}$, $B = \{1, 2\}$, $C = \{1\}$, $f(1) = 1$, $g(1) = g(2) = 1$. Then $g \circ f$ is one-to-one and $g$ is not (checked in code). Rubric $2 + 2 + 2 + 2 + 2 = 10$.

## Departures from the brief

- l6: the subsets are counted by size in a `table` widget (1, 3, 3, 1, then total 8), beside a static table listing them. So the 8 is a table cell, not a separate `numeric`. $\varnothing \subseteq A$ is the confirmation item of the `generalise` screen that states the subset definition. $|\{\varnothing\}| = 1$ and the "which sets equal $\{1, 2, 3\}$" `multi` are quiz items. The interval screen is a `problem`, not a `ladder` (the validator warns when a ladder changes canvas kind). The transfer uses invented company names "from a FTSE 100 universe", so no real company gets made-up P/E figures.
- l7 and l9: the per-line justifications are each one `place` assign screen, with every reason chip plus one unused distractor reason. The brief asked for a `choice` per line, which would have cost four or three screens and pushed l7 past 12. l7 also keeps the separate `choice` on why each step reverses.
- l7: the second law $(A \cap B)^c$ (10 elements) is the `generalise` screen's numeric check, and its explanation gives the trap's wrong set its home. The disjoint-sets edge case and the universe-dependence `choice` are quiz items. The momentum/value transfer asks for the 45. The "Venn diagram is a proof by cases" line is in the reversal screen's explanation.
- l8: I tried the `place` `onPlace` build. Dropping a desk chip on a trader draws that graph edge, and it works, so it is used (screen 5). The empty function is a quiz item. "The graph is a set of pairs" is in the explanation of the $x^2$ on $\mathbb{Z}$ against $\mathbb{R}$ screen.
- l8 and l9 arrow diagrams use two columns (node `x`) with a caption, not `lanes`, which overlapped on a phone (backlog bullet).
- l9: the trap (which opening starts a one-to-one proof) comes before the proof, since it is about how to start it. The one-to-one `order` has one added distractor (dividing only part of each side by 3). $3! = 6$ and $f^{-1}(-4) = -2$ are quiz items, and the pigeonhole idea is named in the transfer explanation.
- Homework: the onto count is a `numeric` at difficulty 4, with by-cases working in the explanation. The difficulty-5 items are the $g \circ f$ `order` (two distractors: assuming $g$ is one-to-one, and starting from $a = b$) and the `longform`.

## Proposed course.json change

None.
