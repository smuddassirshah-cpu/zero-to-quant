# Answer check, topic 3.2, measure-prob level 1

Independent recomputation of every graded widget in `courses/measure-prob/` `l1-why-measure`, `l2-sigma-algebras`, `l3-measures`, `l4-measurable-functions`, `review-1` and `homework-1`. Neither the author's scripts nor `docs/reports/measure-prob-1.md` were used. Scripts are in the scratchpad folder `ac-mp1`.

**Method.**
- Exact `Fraction`, `itertools` enumeration and closed forms for every count and probability. Walk chances come from a dynamic programme, brute force over all paths (n up to 12) and the closed form `1 - C(n, floor(n/2)) / 2^n` (n up to 120). The three agree, and the 100 plotted values and 60 default values match to four places.
- Sigma-algebra sizes by closure under complements and unions (a fixed-point loop), with atoms by membership pattern as a second route. Every `review-1` `r-which` family is tested for each property separately.
- Tree prices by exact risk-neutral weights. Exponential, VaR and digital values with `math` and SciPy (`Phi(0.15)`), tail sums with `mpmath.zeta(2, 100)`.
- Code: each solution and each starter run in CPython with the `code.js` harness rules (the `fraction` mode needs a `Fraction` instance; `equal`; `setup` before `call`). Five code items, 46 hidden tests. Expected values were re-derived by brute force, not copied. Alternative learner solutions (plain `sum`, `hit = 0`, `Fraction(2**n, 3**n)`, `eps * Fraction(1, 2**j)`, a sorted-set listing) were also run.
- Expression grading: the real `grade.js` `exprEqual` with Compute Engine 0.30.2, on 18 forms a learner might type.
- Table byKey ids checked against `table.js` (zero-based `r{row}c{col}`). Numeric `wrong` bands checked for overlap with the answer band and each other. Choice and multi options checked for a second correct option. Key lengths measured against the longest distractor (the 1.5 limit of earlier checks).
- Canvas data: cover intervals (`c1` to `c10`), Cantor frames (stages 0 to 4), the distribution-function steps, the loss curve and the default series.

**Summary.** 81 widgets checked (80 graded plus one longform). All 81 keys are right. Errors: 3, all wrong feedback (one shifted table key set, two `wrong` slips that do not match their value or their family). Warnings: 8. Notes: 6. The worst finding is item 1: in `l3` screen 0 the table feedback keys are one row out, so a learner who misses n = 3 is told about n = 2 and a learner who misses n = 4 is told about n = 3.

## Widgets checked

Key column: the keyed answer. Mine: my value. OK means the key, its tolerance, every `wrong` value and every stated number in the screen's prose, hints and explanation agree with my recomputation, and the numbers are not repeated from a lesson (reviews and homework). See the numbered list for the exceptions.

| File | Screen or item | Key | Mine | Verdict |
|---|---|---|---|---|
| l1 | s0 table | 0.3, 0.2, 0.02 | 0.3, 0.2, 0.02 | OK |
| l1 | s1 numeric | 0 (tol 0) | 0; wrong 0.001 | Warning 8 (feedback) |
| l1 | s2 numeric | 0.00999 | 0.0099902 = 1023/102400 | OK |
| l1 | s3 choice | a | a only; key long (1.27) | OK |
| l1 | s4 numeric | 0.0173415 | 1024/59049 = 0.01734153; third 1.6935e-5, half 9.766e-4 | OK |
| l1 | s5 choice | a | a only | OK, key long (1.77), item 10 |
| l1 | s6 order | s1 to s6, same s3/s4 | valid; no other valid order | OK |
| l1 | s7 choice | a | a only | OK |
| l1 | s8 code | 10 tests | solution 10/10, starter 0/10, alternatives 10/10 | OK |
| l1 | s9 numeric | 0.4479 | q = 5/9; 40/81 / 1.1025 = 0.447916; ge 0.72786, gt 0.27995 | OK |
| l1 | q-irrational choice | a | a only | OK |
| l1 | q-ends numeric | 0.3 | 0.3 | OK |
| l1 | q-cantor choice | a | a only | OK, key long (1.85), item 10 |
| l1 | q-vitali choice | a | a only | OK, key long (2.44), item 10 |
| l2 | s0 multi | odd, even, empty, all | same four | OK |
| l2 | s1 choice | a | a only | OK |
| l2 | s2 numeric | 8 | 8; 7 and 6 slips match, 3 = atoms | OK |
| l2 | s3 tap-regions | r1c1, r1c2, r1c3 | same | OK |
| l2 | s4 numeric | 16 | 16 (atoms {1}, {2}, {3}, {4, 5, 6}) | OK |
| l2 | s5 multi | comp, union | complement of {1} and {1, 2} missing; Omega, empty present | OK |
| l2 | s6 choice | a | a only | OK, key long (1.65), item 10 |
| l2 | s7 multi | closed, pt, rat, irr | same; V not Borel | OK, note 13 |
| l2 | s8 numeric | 6 | 4 + 4 - 2 = 6 (checked by enumeration) | OK |
| l2 | s9 choice | a | a only | OK, key long (1.52), item 10 |
| l2 | s10 code | 10 tests | solution 10/10, starter 0/10 | OK |
| l2 | s11 choice | a | a only | OK |
| l2 | q-largest numeric | 64 | 64 | OK |
| l2 | q-must choice | a ({4}) | {4} forced; {2}, {1, 2} not (8 sets) | OK |
| l2 | q-irr choice | a | a only | OK, key long (1.94), item 10 |
| l2 | q-two numeric | 8 | 8 | OK |
| l3 | s0 table | 0.5, 0.5, 0.625, 0.625 | 1/2, 1/2, 5/8, 5/8 (brute force) | OK key; Error 1 (byKey) |
| l3 | s1 numeric | 1 | limit 1 (recurrence); n = 100 gives 0.92041, n = 10 gives 193/256 | OK |
| l3 | s2 choice | a | a only | OK |
| l3 | s3 table | 0.5, 0.75, 0.5 | same | OK |
| l3 | s4 numeric | 0.6 | 0.6; span 0.8 | OK |
| l3 | s5 order | c1 to c6 | valid | OK, note 14 |
| l3 | s6 choice | a | a only | OK |
| l3 | s7 numeric | 3 % | 3 %; independent 2.9701 | OK |
| l3 | s8 choice | a | a only | OK, key long (2.02), item 10 |
| l3 | s9 code | 9 tests | solution 9/9, starter 0/9; n = 100 value matches | OK, note 16 |
| l3 | s10 table | 0.1829, 0.6358, 1 | 0.182927, 0.635830, 1 | OK |
| l3 | q-as choice | a | a only | OK |
| l3 | q-union numeric | 2 % | 2 %; independent 1.98505 | Warning 7 |
| l3 | q-above numeric | 0 | 0 | OK |
| l3 | q-default numeric | 0.3324 | 0.332392 | OK |
| l4 | s0 tap-regions | six cells with sum 7 | same | OK |
| l4 | s1 tap-regions | six cells with sum at most 4 | same | OK |
| l4 | s2 choice | a | a only | OK, key long (1.77), item 10 |
| l4 | s3 multi | d1, d2, d3 | functions of the first die only | OK |
| l4 | s4 numeric | 0.5833 | 21/36 = 0.58333; F steps match 12 levels; 15/36, 26/36 slips match | OK |
| l4 | s5 order | r1 to r5 | valid | OK |
| l4 | s6 numeric | 0.9393 | 0.939347; tail 0.0393, exp 0.3935 | OK |
| l4 | s7 choice | a | a only | OK |
| l4 | s8 code | 10 tests | solution 10/10, starter 0/10 | Warning 4 |
| l4 | s9 numeric | 6931.47 | 10000 ln 2 = 6931.4718 | OK |
| l4 | q-expu numeric | 0.1353 | e^-2 = 0.135335 | OK |
| l4 | q-left choice | a | a only | OK |
| l4 | q-indic choice | a | a only | OK |
| l4 | q-tail numeric | 0.0833 | 3/36 = 0.08333; 1 - 33/36 | OK |
| review | r-cover numeric | 0.01969 | 0.0196875 | OK |
| review | r-which choice | a | a only | Error 2 (option c feedback) |
| review | r-dice numeric | 0.2222 | 8/36 = 0.2222 (enumerated) | OK key; Error 3 (slip `six`) |
| review | r-default numeric | 0.2603 | 0.260300; lin 0.3, surv 0.7397 | OK |
| review | r-cantor table | 64, 0.0878 | 64, 64/729 = 0.087791 | OK |
| review | r-events numeric | 256 | 8 atoms, 256 (enumerated) | OK |
| review | r-counting choice | a | a only | OK, note 15 |
| review | r-var numeric | 8789 | 8000 ln 3 = 8788.898 | OK |
| review | r-borel choice | a | a only | OK, key long (3.18), item 10; note 15 |
| review | r-union numeric | 4 % | 4 %; independent 3.93651 | OK |
| homework | h-borel multi | half, seven, dyadic | same | OK |
| homework | h-cantor part 1 numeric | 18 | 17.037, so 18; (2/3)^17 = 0.001015, (2/3)^18 = 0.000677 | OK |
| homework | h-cantor part 2 numeric | 262144 | 2^18 | OK |
| homework | h-cantor part 3 choice | a | a only | Warning 9 (repeat) |
| homework | h-tail numeric | 0.01005 | 0.0100502 (mpmath); 1/99 = 0.010101, 1/100^2 | OK |
| homework | h-order | o1 to o5 | valid, but o3 and o4 swap | Warning 5 |
| homework | h-var part 1 numeric | 0.8484 | 0.848367 | OK |
| homework | h-var part 2 numeric | 64378 | 20000 ln 25 = 64377.516 | OK |
| homework | h-var part 3 numeric | 0 | 0; slip `pos` 5000 matches nothing | Warning 6 |
| homework | h-expr expression | 1-e^{-rx} | 1 - e^{-rx} | OK key; Warning 11 (`\exp`) |
| homework | h-code | 7 tests | solution 7/7, starter 0/7 | OK |
| homework | h-long longform | 6 rubric points, 10 marks | sum 10; each point checkable; model correct | OK |

## Mismatches

Errors

1. **Error. `l3-measures.json` screens[0] (the table for P(A_n)), `feedback.byKey`: the cell keys are one row out.** The engine keys a table cell `r{row}c{col}` with zero-based rows (`table.js`; the same file's `l1` s0 and `l3` s3 follow this). Row 0 is n = 1, row 1 is n = 2, row 2 is n = 3, row 3 is n = 4. The file has `r0c1` (After 1 step, right), `r2c1` ("After 2 steps ... still 1/2") and `r3c1` ("After 3 steps, 5 of the 8 paths"). So a learner who gets n = 3 wrong is told about n = 2, one who gets n = 4 wrong is told about n = 3, and a wrong n = 2 gets only the generic line. Fix: rename `r2c1` to `r1c1`, rename `r3c1` to `r2c1`, and add `r3c1`: "After 4 steps, a walk cannot first reach +1 on an even step. Four steps add no new path, so the chance is still $\tfrac58$." (10 of 16 paths).
2. **Error. `review-1.json` items[1] `r-which`, option `c` `why`.** It says "You checked complements only". Family c, $\{\varnothing, \{1\}, \{2\}, \{3, 4\}, \Omega\}$, fails complements too: the complements of $\{1\}$ and $\{2\}$ ($\{2, 3, 4\}$ and $\{1, 3, 4\}$) and of $\{3, 4\}$ ($\{1, 2\}$) are all unlisted. A learner who checked complements would have rejected c. Fix: "You checked only that $\varnothing$, $\Omega$ and the pair $\{3, 4\}$ are present. $\{1\}^c = \{2, 3, 4\}$ is not listed, and nor is $\{1\} \cup \{2\} = \{1, 2\}$." The `byKey.c` and option `b` text are right (family b fails complements only: $\{1, 2\}^c = \{3, 4\}$; its unions all land inside the list).
3. **Error. `review-1.json` items[2] `r-dice`, `wrong` `six` (0.1667) and `byKey.six`.** The feedback says "You counted only the cells with product above 24. The preimage includes 20 and 24." Products above 24 are 25, 30, 30 and 36: 4 cells, 4/36 = 0.1111. The value 0.1667 is 6/36, the cells with product at least 24 (it drops only the two cells with product 20). The text names a slip that gives 0.1111, not 0.1667. Fix (either): change the wrong value to 0.1111 and keep the text; or keep 0.1667 and write "You dropped the cells with product 20, (4, 5) and (5, 4). The event includes them." Key 8/36 is right (8 cells: products 20, 20, 24, 24, 25, 30, 30, 36).

Warnings

4. **Warning. `l4-measurable-functions.json` screens[8] code, test 8 (`cdf(pushforward(two, ...), 1)`, expect `Fraction(0)`, compare `fraction`).** The natural solution `sum(p for v, p in dist.items() if v <= x)` returns the integer 0 for an empty selection, and the `fraction` mode needs a `Fraction` instance, so it fails this one test (9 of 10; verified). The model solution passes only because it writes `sum(..., Fraction(0))`. Neither the prompt nor the docstring asks for that. Fix: set this test's `compare` to `equal` (`Fraction(0) == 0`), or add "return a `Fraction`, even when no value qualifies" to the docstring and the prompt.
5. **Warning. `homework-1.json` items[3] `h-order`: a valid alternative order is marked wrong.** Lines `o3` (continuity from below) and `o4` (the two subtractions by finite additivity) can swap: `o4` needs only `o1`, `o2` and finiteness, and `o5` uses both. Fix: add `"same": [["o3", "o4"]]` to the widget.
6. **Warning. `homework-1.json` items[4] `h-var` part 3, `wrong` `pos` (5000) and `byKey.pos`.** The text says "You solved the smooth equation". Solving $0.75 + 0.25(1 - e^{-x/20000}) = 0.70$ gives $x = -20000 \ln 1.2 = -3{,}646$, a negative loss, not 5000. No slip in the item yields 5000. Fix: set the wrong value to $-3646$ (tol 1) and the text to "You solved the smooth equation. It gives a negative loss, which tells you the atom already covers 0.70." Key 0 is right.
7. **Warning. `l3-measures.json` quiz `q-union`: stated number 1.9851.** Independent desks give $1 - 0.995^4 = 0.01985050$, so 1.9850 % to four places (1.98505 rounds down). The `wrong` value `indep` (1.9851) and the explanation ("= 1.9851 %") overstate by 0.0001. Both are inside the 0.001 tolerance, so grading is unaffected. Fix: write 1.9850 in the `wrong` value and the explanation. (The 2.9701 % of `l3` s7 and the 3.9365 % of `r-union` are correct.)
8. **Warning. `l1-why-measure.json` screens[1], `byKey.tiny` (wrong value 0.001, band 0.0005 to 0.0015).** The text reads "A window of half-width 0.0005 already has a smaller chance." That window has chance $2 \times 0.0005 = 0.001$, equal to the value typed, not smaller. Fix: "A window of half-width 0.0004 has chance 0.0008, and the point lies inside it, so $P(X = 0.5)$ is at most 0.0008. No positive number works."
9. **Warning. `homework-1.json` items[1] `h-cantor` part 3 repeats `l1-why-measure.json` quiz `q-cantor`.** Same question (is the Cantor set countable), same key, same two distractors and the same `why` sentences. DECISIONS "Fresh numbers in reviews and homework" bars this. Fix: ask something new about the same idea, for example "The end points of the removed intervals form a set. Is it countable?" with key "Yes: each stage adds finitely many, so the list can be built stage by stage", and distractors that confuse it with the whole Cantor set.
10. **Warning. Choice keys visibly longer than their distractors** (key characters against the longest distractor, limit 1.5 as in earlier checks). Worst first: `review-1` `r-borel` (89 against 28, 3.18); `l1` quiz `q-vitali` (83 against 34, 2.44); `l3` s8 (95 against 47, 2.02); `l2` quiz `q-irr` (103 against 53, 1.94); `l1` quiz `q-cantor` (102 against 55, 1.85); `l1` s5 (140 against 79, 1.77); `l4` s2 (78 against 44, 1.77); `l2` s6 (91 against 55, 1.65); `l2` s9 (132 against 87, 1.52). Fix: shorten each key to its claim without the reason (for example `r-borel` a: "The Vitali set $V$") or lengthen the distractors to match. Within the limit but worth watching: `l1` s3 (1.27), `r-counting` (1.41).
11. **Warning. `homework-1.json` items[5] `h-expr`: `1-\exp(-rx)` is graded wrong.** Compute Engine 0.30.2 parses `\exp(...)` after `1-` as an error tuple, and MathLive turns typed "exp" into `\exp`. Forms with `e^{...}`, `-e^{-rx}+1`, `1-\frac{1}{e^{rx}}` and `1-e^{-r\cdot x}` all pass; `e^{-rx}` and `1-e^{rx}` fail as intended. This is the known engine item P32-expr-exp (BACKLOG-INBOX), still unbuilt in this worktree. Fix: none in content; the item needs that engine fix before it ships, or an authored note "write the exponential as $e^{...}$". The `accept` strings serve only the text fallback.

Notes

12. **Note. `l1` s3 explanation.** "Countable additivity, with overlaps only helping, bounds that by $\varepsilon$" is countable subadditivity. Fix: "Countable subadditivity bounds that by $\varepsilon$." (Lesson 3 names it the union bound.)
13. **Note. `l2` s7 canvas.** The prose says the bars are $n = 4, 8, 16, 32$. The canvas draws $n = 4, 8, 16$ and the limit. Fix: add `n32` (from 0.36875 to 0.63125, open, row 4) or write "for $n = 4, 8, 16$".
14. **Note. `l3` s5 order, lines `c4` and `c5`.** `c5` (partial sums equal $P(A_n)$) could follow `c3` before `c4` without a logical gap, though `c5` reuses the partial-sum notation that `c4` introduces. The hint's order (series limit, then partial sums) agrees with the key. No change needed. Add `"same": [["c4", "c5"]]` only if the author wants both accepted.
15. **Note. Review and homework items close to a lesson item.** `r-borel` has the same key as `l2` s7 (the Vitali set is the one non-Borel set), `r-counting` has the same answer as `l3` s8 (infinite, so continuity from above fails), `h-expr` is the `l4` `q-expu` transformation with a general rate, and `h-long` part 2 asks for the 0.01005 that `h-tail` already asks (a repeat inside the homework). All use different numbers or set-ups, so none repeats a number. If strictness is wanted, give `r-counting` a different measure (a weighted count) and drop the 0.01005 from `h-long`. `markov/homework-5` and `markov/l20` quote the same 0.9204 for the same walk; a different course, so allowed.
16. **Note. `l3` s9 `hit_prob(0)`.** The solution `hit = 0` returns the integer 0 for n = 0 and fails the `fraction` test (the prompt does say "as a `Fraction`"). Every other test passes with it. Fix only if wanted: `compare: "equal"` for test 1.
17. **Note. Numeric `wrong` values with no `byKey` text.** 14 slips (in `l1` q-ends, `l2` q-largest and q-two, `l3` q-union, q-above and q-default, `l4` q-expu and q-tail, `r-dice` `half`) have no line, so a learner who types one sees the generic line. Their values are all sensible slips (6 and 36 for 64; 2 % against 1.9851 %; 0.5 and 0.2 for 0.1353). Add a line only if wanted.

## Checks with nothing found

- Every `wrong` band lies outside its answer band and outside every other wrong band (numeric fields and table cells). No byKey names an option or value that does not exist.
- No choice item has two correct options; every distractor in every choice and multi widget has a `why`.
- Order keys: `l1` s6 (one `same` group, correct), `l3` s5, `l4` s5 and `h-order` (item 5 apart) have no other valid order. Distractor lines `d1`, `d2` and `x1`, `x2` are false as the `why` texts say.
- All five code items: each solution passes all its tests and examples; each starter fails every test and example (0 of 46). The stated counts in `how` (10, 10, 9, 10, 7) match.
- Canvas data: cover intervals `c1` to `c10` are centred on the listed rationals with half-width $\varepsilon / 2^{k+1}$; Cantor frames give 1, 2, 4, 8, 16 intervals and total lengths 1, 0.6667, 0.4444, 0.2963, 0.1975; the plotted $F_X$ steps equal the 12 exact levels; the loss curve and 0.95 line match 10000 ln 2.
- Review and homework numbers are fresh: none of 0.02 with six terms, 1 % over 30 years, stage 6 and stage 18, 0.85 with £8,000, 0.75 with £20,000, 5 desks at 0.8 % or the product of two dice appears in the lessons. A word-boundary search of every other course, exam and bank file finds no copy of these answers (only the same walk quantity noted in item 15).
- Longform rubric (`h-long`): six points of 2, 2, 2, 2, 1 and 1 make 10; each is checkable; the model answer is correct (the union bound on the tail, a convergent series, continuity from above with $P(B_1) \le 1$, and about 0.01005 from day 100 on).
