# Algebra levels 1 and 2 (Groups; Inside a group): second-reader findings

Scope: `app/content/courses/algebra/` l1 to l9, `review-1.json`, `review-2.json`, `homework-1.json`, `homework-2.json`. Continuity skim of l10 to l17 (first screens, summaries, every cross-reference to l1 to l9).

Method: every stated number and every `wrong[]` value recomputed in a scratch script (numpy matrices for $D_4$, brute-force subgroup and Hasse counts, permutations by cycle walk and inversion count, Landau maxima by partition, shuffles as maps, Fractions for the prisoners sum and Kendall's $\tau$): 102 checks, all agree. Every `why` and `byKey` read against the action it names. Every code widget run in CPython (prelude, solution, starter, every test): all 10 solutions pass every test and every starter fails at least one. Engine checked for how a `table` widget picks its key (`app/js/engine/widgets/table.js` line 86) and how the validator lists table keys (`app/tools/validate.mjs` line 647, item 576).

Tool results:
- `python3 docs/reports/algebra-L1-numbers.py`: exit 0, 122 of 122, 19 "check by hand" lines (each read; all fine).
- `python3 docs/reports/algebra-L2-numbers.py`: exit 0, 126 of 126, 17 "check by hand" lines (each read; all fine).
- Stated numbers the author scripts do not check (all verified here and correct): l5 `screens[10].widget.wrong[1]` 500 (lcm); l9 `screens[7].widget.options[2]` 5,230,697,472,000 ($16!/4$); l9 `screens[4].hints[2]` the per-entry counts 4, 2, 5, 0, 1, 2, 1, 0; homework-2 `items[4].feedback.byKey.indep` $(1/2)^{100} \approx 8 \times 10^{-31}$; l8 `screens[7].hints[1]` "2 + 5 gives 10". The L2 script's "max S8" method 2 uses a hand-picked partition list, not every partition of 8.
- `cd app && node tools/validate.mjs`: 0 errors. L1 and L2 warnings: 10, all "a problem screen without a canvas before the ladder ends" (l7 screens 3 to 5, l8 screens 2, 3, 6, 7, l9 screens 2, 5, 7), as the author reported.
- `VOICE_BASE=app/content/courses/algebra python3 docs/reviews/voice-scan.py`: 0 sentences over 20 words, 0 explanations over three sentences (whole folder). My own scan of L1 and L2 text: no exclamation marks, no em-dashes, no American spellings.

Format: `N. file | JSON path | severity | problem | evidence | fix`. Severities: wrong, misleading, voice, layout, continuity.

## Findings

1. homework-1.json | `items[2].explain.text` | wrong | "only $n = 1, 2, 4, p^k$ and $2p^k$ qualify" drops the hypothesis that $p$ is odd. | The same explanation says $\mathbb{Z}_8^{\times}$ is not cyclic, and $8 = 2^3$ is a $p^k$; so are 16 and 32, and their unit groups are not cyclic either. | "The theorem behind the list says only $n = 1, 2, 4, p^k$ and $2p^k$ qualify, with $p$ an odd prime."

2. l9-odd-and-even.json | `screens[11].explain.text` | wrong | "The starter's $(-1)^{c'}$ ... is right only when the moved cycles have even lengths" is false. | The true sign is the product of $(-1)^{\ell - 1}$ over the moved cycles, the starter's is $(-1)$ per moved cycle. They agree exactly when an even number of moved cycles have odd length: on $(1\,2\,3)(4\,5\,6)$ both give $+1$. | "The starter's $(-1)^{c'}$, with $c'$ the moved cycles, is right exactly when an even number of them have odd length. It fails the 3-cycle $(1, 2, 0)$ and the 5-cycle, which are even."

3. l3-modular-arithmetic.json, l8-permutations-and-cycles.json, l9-odd-and-even.json | eight table cells (below) | misleading | Each cell names its slip in `wrong[]`, but the `byKey` line for that slip is keyed on the cell id. `table.js` returns the wrong id when the slip matches, so the named slip gets only the generic line, and the slip's line fires on any other wrong entry in that cell. | `table.js` line 86: `key: w0 && w0.id ? w0.id : wrong[0].id`. Typing 25 for $5^2$ in l3 returns `raw5`, which has no line; typing 5 returns `r1c1` and reads "You left 25 unreduced". The validator now accepts a cell's wrong ids as keys (`validate.mjs` line 647, item 576), so no engine change is needed. | Rename each key to the wrong id and give the cell id a neutral line:
   - l3 `screens[3].feedback.byKey`: rename `r2c1` to `div`; add `"r2c1": "Row 3 holds 4 once, in column 8: $3 \\times 8 = 24$."`
   - l3 `screens[7].feedback.byKey`: rename `r3c1` to `neg`; add `"r3c1": "Back-substitute: $1 = 5 - 2 \\times 2 = 3 \\times 5 - 2 \\times 7 = 3 \\times 26 - 11 \\times 7$."`
   - l3 `screens[9].feedback.byKey`: rename `r1c1`, `r2c1`, `r3c1` to `raw5`, `raw7`, `raw11`; add `"r1c1": "$5^2 = 25 = 2 \\times 12 + 1$."`, `"r2c1": "$7^2 = 49 = 4 \\times 12 + 1$."`, `"r3c1": "$11^2 = 121 = 10 \\times 12 + 1$."`
   - l8 `screens[6].feedback.byKey`: rename `r1c1` to `sum`; add `"r1c1": "The lengths are 3 and 5, and $\\operatorname{lcm}(3, 5) = 15$."`
   - l9 `screens[10].feedback.byKey`: rename `r0c1` to `pairs`; add `"r0c1": "List the pairs out of order: $(2, 1)$, $(4, 3)$ and $(5, 3)$."`
   - l9 `quiz[0].feedback.byKey`: keep `r0c1`; add `"fact": "You counted all 24 orderings of 1 to 4. Each 4-cycle can be written 4 ways, so there are 6."`

4. l1-symmetries.json | `screens[3].widget.rows[3][1]` | misleading | A learner who types `sr` for $s \cdot r$ names the right element and is told "Not quite. Do the column move first, then the row move." | `sr` is $s \cdot r$ by definition; the summary formula itself says $sr = r^3s$. | Add `"wrong": [{ "id": "sr", "text": "sr" }]` to the cell and `"sr": "That is the same element, but use the table's name. The first screen found $sr = r^3s$."` to `feedback.byKey`.

5. l4-cyclic-groups.json | `screens[0].feedback.byKey.two` | misleading | The line for 2 says "You stopped too soon", but the likely slip is not counting seat 0, which the question asks for. | The walk visits 0, 2, 4; a learner who answers 2 has counted 2 and 4. | "You left out seat 0. The walk from 0 visits 0, 2 and 4."

6. review-2.json | `items[4].widget.options[1]` (`one`) | misleading | The why "You read along the bottom row" does not produce $(1\,3\,6\,2)(4\,5)$. | Reading the bottom row 3, 6, 1, ... as a cycle gives $(3\,6\,1) = (1\,3\,6)$; no reading of $3, 6, 1, 5, 4, 2$ gives $1 \to 3 \to 6 \to 2$. | Option text "$(1\,3\,6)(4\,5)$", why "You read 3, 6, 1 along the bottom row as a cycle. Follow $k \to \sigma(k)$: $1 \to 3 \to 1$."

7. l7-lagrange.json | `quiz[1].widget.options[2].why` | misleading | "In $\mathbb{Z}_3$, $1 + 1 \ne 0$, and $|G|/2$ is not even a whole number" gives a counterexample whose exponent does not exist, then a sum unrelated to it. | $|\mathbb{Z}_3|/2 = 1.5$. | "You halved the exponent. In $\mathbb{Z}_4$, $1 + 1 = 2 \ne 0$."

8. l7-lagrange.json | `screens[0].explain.text` | misleading | "With $x \ne e$ in the set, $x^2$ must be $e$ or $x$'s partner, and the products then leave the set" is asserted, not shown, and $x^2 = e$ is in fact impossible in a subgroup of order 3. | In $\{e, x, y\}$: $x^2 = e$ forces $xy \notin \{e, x, y\}$; so $x^2 = y$, then $xy = x^3$ must be $e$. | "Every choice leaks. A subgroup $\{e, x, y\}$ would force $x^2 = y$ and $xy = e$, so $x^3 = e$. No element of $D_4$ has order 3."

9. l1-symmetries.json | `screens[8].prose` | misleading | "Two facts make the symmetries a group" omits associativity and the identity, which l2 then lists as axioms. | The explain says "These are two of the group axioms", contradicting "two facts make". | "Composing moves is associative, and $e$ does nothing. Two more facts make the symmetries a group: combining two gives another, and each one can be undone. Put the reasons in order."

10. l9-odd-and-even.json | `screens[7].prose` | misleading | "Exactly the even arrangements with the blank home can be reached, and a theorem says all of them can" states the conclusion before the theorem it cites; screen 6 proved only "at most the even ones". | Screen 6, k4: "the reachable arrangements with the blank home are even permutations". | "Only even arrangements with the blank home can be reached, and a theorem says every one of them can. So, letting the blank roam too, exactly half of the arrangements of the 16 squares are reachable."

11. l7-lagrange.json | `screens[7].prose`; `screens[7].widget.options[2].why` | misleading | The trap calls $A_4$ "the even permutations of 4 objects (l9)" two lessons before l9 defines even permutations, and the why cites $D_6$, never named in L1 or L2. | l8 and l9 come after l7; "D_6" appears nowhere else in L1 to L4. | Prose: "$A_4$ is a group of 12 permutations of 4 objects, built in l9. Lagrange says its subgroups have sizes among 1, 2, 3, 4, 6, 12." Why: "You assumed a group of order 12 is cyclic. $A_4$ is not, and nor is the hexagon's group of 12 symmetries."

12. l5-subgroups.json | `screens[2].prose` | misleading | "Pinter's one-step test" attributes the $ab^{-1}$ form to Pinter; his chapter 5 theorem is the two-condition test (closed under products and under inverses), with the one-step form left to the exercises. Check against the text before keeping the attribution. | Reference text named in the brief. | "The one-step test: a non-empty $H \subseteq G$ is a subgroup when $a, b \in H$ implies $ab^{-1} \in H$. Why does this one condition give all four axioms?"

13. l2-group-axioms.json | `quiz[3].explain.text` | misleading | The last sentence, "The smallest true group is $\{e\}$, with $ee = e$", has nothing to do with the table on screen. | The item is about a 3-element table. | Replace it with "A true table on $\{e, a, b\}$ with $ab = e$ has row $b$ equal to $b, e, a$."

14. l3-modular-arithmetic.json | `screens[1].hints[1].text` | misleading | "Look in the rows of the odd numbers" points the learner at row 5, which holds no 1; the next screen's `odd` distractor punishes the same idea. | Row 5 of the table is $0, 5, 0, 5, \dots$. | "Only some odd rows reach 1. Row 5 never does."

15. l1-symmetries.json | `summary.trap`; `summary.formula.note` | voice | The trap names "turn then flip" first but gives $rs$ (flip then turn) first, so the pairs read crossed. The note "a turn after a flip, the other way round" reads as "in the other order". | Hook: turn then flip is $sr$, fixing corners 1 and 3. | Trap: "Turn then flip is not flip then turn: $sr$ fixes corners 1 and 3, and $rs$ fixes 2 and 4." Note: "Turning then flipping equals flipping then turning the opposite way."

16. homework-1.json | `items[0].model` (the $D_4$ paragraph) | voice | "The half turn gives $r^2 \ne e$, and $r^2 \cdot r^2 = e$ but $r \cdot r = r^2 \ne e$" muddles which element fails. | The rubric asks only for $r^2 \ne e$. | "The quarter turn has $r \cdot r = r^2 \ne e$. So $x^2 = e$ fails for $x = r$, and the theorem does not apply. Indeed $D_4$ is not abelian: $rs \ne sr$."

17. l5-subgroups.json | `screens[0].hints[2].text` | layout | The step hint shows engine region ids: "The e cells are r1c1, r2c4, r3c3 and r4c2." The learner sees element names, not ids. | Grid cells are labelled by row and column heads only. | "The e cells are $e \cdot e$, $r \cdot r^3$, $r^2 \cdot r^2$ and $r^3 \cdot r$."

18. l5-subgroups.json | `screens[7].feedback.byKey.all` | layout | "Only the middle row has 2 elements": the lattice has four rows (y = 0.07, 0.33, 0.64, 0.93), so there is no middle row. | Canvas `params.nodes` y values. | "You counted every subgroup. Only the row of five, second from the bottom, has 2 elements."

19. l8-permutations-and-cycles.json, l9-odd-and-even.json | `screens` | layout | Neither lesson has an `explore` screen; AUTHORING section 2 gives the shape hook, explore, name, ladder. | l8: problem, ladder, problem...; l9: problem, problem, problem... | l8: make `screens[0]` an `explore` (its `tap-regions` on the arrow graph is canvas-bound). l9: make `screens[0]` an `explore` if the validator accepts the `manipulate` on the grid, else leave and note in the report.

20. l2-group-axioms.json | `screens[2]` to `screens[4]` | layout | The ladder is three rungs at difficulty 2 with the same question; the brief's rungs $\{1, -1, i, -i\}$ (a group of 4) and the invertible matrices (a non-abelian group) are missing, so "abelian" is named only inside an explanation. | `docs/briefs/algebra.md`, Level 1, the l2 bullet: five candidate sets. | Add a rung after `screens[3]`: "$\{1, -1, i, -i\}$ under multiplication", `choice` "None: it is a group", with `why` lines for closure ($i \cdot i = -1$ is in the set) and inverses ($i \cdot (-i) = 1$); bold **abelian** in its explain.

21. l7-lagrange.json | `quiz[2].explain.text` | continuity | "$G \cong \mathbb{Z}_2$" uses $\cong$ before l10 defines isomorphism (`l10-homomorphisms.json` `quiz[2].prose` bolds **isomorphism**). L2 side should change. | No L1 or L2 screen defines $\cong$. | "So $g^2 = e$, and $G$ has the same table as $\mathbb{Z}_2$."

22. l9-odd-and-even.json | `screens[9].prose` | continuity | "The sign is a homomorphism" uses the word before l10 bolds **homomorphism** as new (`l10-homomorphisms.json` `screens[2].prose`). The brief asks for this sentence, so the fix keeps the idea and drops the undefined word. L2 side should change. | — | "The sign turns products into products: $\operatorname{sgn}(\sigma\tau) = \operatorname{sgn}\sigma \operatorname{sgn}\tau$, since transposition counts add. l10 calls such a map a homomorphism."

## Continuity

Notation in L3 and L4 matches L1 and L2 on the main points: products by juxtaposition read right to left, $e$ as identity, $|G|$ and $\operatorname{ord}(g)$, left cosets $gH$ and $g + H$, $[G : H]$, $\mathbb{Z}_n$ and $\mathbb{Z}_n^{\times}$ (no $U(n)$ or $\mathbb{Z}_n^*$), $D_4$ (no $D_8$ beyond l1's remark), the $D_4$ table order (rotations first, then flips). Every L3 and L4 citation of l1 to l9 was checked; the ones below are wrong or thin. Items 21 and 22 above are continuity findings on the L2 side.

23. l13-fermat-and-euler.json `screens[5].prose` against l3-modular-arithmetic.json `screens[2].prose` and l10-homomorphisms.json `screens[2].prose` | continuity | $\varphi$ means Euler's function in l3, a homomorphism in l10 to l12 and homework-3, then Euler's function again in l13, with no word about the switch. L3 side should change (l13). | l3 bolds "Euler's $\varphi(n)$"; l10 uses $\varphi$ 121 times as a map. | In l13 `screens[5].prose`, after the first sentence: "This $\varphi$ is l3's count of units, not a homomorphism."

24. l10-homomorphisms.json `screens[5].prose` against l2-group-axioms.json `screens[1].prose` | continuity | $e_G$ and $e_H$ appear without saying they are the identities of $G$ and $H$; L1 and L2 write a bare $e$. L3 side should change. | l10 uses $e_G$ 25 times. | Start the prose: "Write $e_G$ and $e_H$ for the identities of $G$ and $H$."

25. l11-normal-subgroups.json `screens[10].prose` against l3-modular-arithmetic.json `screens[0]` and `screens[1]` | continuity | "Time of day is the quotient $\mathbb{Z}/1440\mathbb{Z}$" uses a second name for clock arithmetic one lesson before l12 proves $\mathbb{Z}/n\mathbb{Z} \cong \mathbb{Z}_n$; l3 taught the clock as $\mathbb{Z}_{12}$. L3 side should change. | l12 `screens[3].explain.text` states $\mathbb{Z}/n\mathbb{Z} \cong \mathbb{Z}_n$. | "Time of day is the quotient $\mathbb{Z}/1440\mathbb{Z}$, which behaves like l3's $\mathbb{Z}_{1440}$; l12 proves they match."

26. l10-homomorphisms.json `screens[1]` against l4-cyclic-groups.json `screens[1]` | continuity | l10 repeats l4's explore (the same `complex-map`, $z \mapsto z^k$ on $\mu_{12}$, $k = 4$) and re-defines $e^{i\theta}$, citing `complex` l4 and `trig` l12 but not l4. L3 side should change. | l4 `screens[1].prose` has the same definition and citations. | l10 `screens[1].prose`: "In l4, $z \mapsto z^4$ sent the twelve 12th roots of unity to three points. Move $k$ and watch where the points land." Drop the definition of $e^{i\theta}$.

27. l13-fermat-and-euler.json `screens[0]` to `screens[2]` against l4-cyclic-groups.json `screens[6]` and l7-lagrange.json `screens[4]`, `quiz[1]` | continuity | l13 re-derives the powers of 2 and 3 modulo 7 and the order in $\mathbb{Z}_7^{\times}$, which l4 already found ($\operatorname{ord}(2) = 3$, $\operatorname{ord}(3) = 6$). Its core step, $g^{|G|} = e$ for finite $G$, is already proved in l7. Both levels teach these as new. L3 side should change. | l7 explain: "Hence $g^{|G|} = e$ for every $g$." | l13 `screens[2].prose`: "As in l4, each row's period is the order $\operatorname{ord}(a)$." l13 `screens[3]`: cite l7's $g^{|G|} = e$ and apply it to $\mathbb{Z}_p^{\times}$.

28. l13-fermat-and-euler.json `screens[3].hints[1]` against l4-cyclic-groups.json and l7-lagrange.json `screens[4].hints[1]` | continuity | "Its size is $\operatorname{ord}(a)$ (l4)": l4 never states $|\langle g \rangle| = \operatorname{ord}(g)$; l7 does. L3 side should change. | l7 hint: "$\langle g \rangle = \{e, g, \dots, g^{m-1}\}$ with $m = \operatorname{ord}(g)$." | "(l7)".

29. l13-fermat-and-euler.json `screens[4].prose` against l3-modular-arithmetic.json `screens[6].explain.text` | continuity | "Recall from l3 that every non-zero residue modulo a prime has an inverse": l3 says so only in the explanation of a quiz item (`quiz[2].explain.text`). L1 side should change. | l3 screens never state the prime case. | Append to l3 `screens[6].explain.text`: "So modulo a prime every non-zero residue is a unit."

30. l12-first-isomorphism-theorem.json `screens[3].explain.text` against l9-odd-and-even.json `screens[9]` | continuity | "$S_n/A_n \cong \{1, -1\}$, giving $|A_n| = n!/2$" presents the count as new; l9 counted it by pairing with $(1\,2)$. L3 side should change. | l9 explain: "Multiplying by $(1\,2)$ pairs each even permutation with an odd one". | "...$S_n/A_n \cong \{1, -1\}$, which gives l9's count $|A_n| = n!/2$ again."

31. l14-rings.json `screens[0].prose` against l3-modular-arithmetic.json `screens[1]` | continuity | "This is the multiplication table of $\mathbb{Z}_{12}$ (l3)": l3 showed the table of $\mathbb{Z}_{10}$, not $\mathbb{Z}_{12}$. L4 side should change. | l3 `screens[1].canvas` is a 10 by 10 grid. | "This is the multiplication table of $\mathbb{Z}_{12}$, built as l3 built $\mathbb{Z}_{10}$'s."

32. l14-rings.json `screens[2].prose` against l3-modular-arithmetic.json `screens[2].prose` | continuity | Both bold **unit** as a new term. L4 side should change. | l3: "is a **unit**: it has an inverse". | "A **unit** has an inverse under $\times$, as the units of $\mathbb{Z}_n$ did in l3."

33. l10-homomorphisms.json `screens[0].prose` against l2-group-axioms.json `screens[9]`, `screens[10]` | continuity | l10 reintroduces "gross returns multiply" from `exp-log` l6; l2 already built the group of returns under $\oplus$ with identity $0\%$. Low priority. L3 side should change. | l2 `screens[9].prose`. | Add: "In l2 these returns formed a group under $\oplus$."

## Engine

No engine change is needed for these fixes: the validator already accepts a table cell's own wrong ids as `byKey` keys (item 576). The class in finding 3 (a cell's `wrong[]` id with no `byKey` line while a `byKey` line sits on that cell's id) occurs 8 times here and could be a validator warning.
