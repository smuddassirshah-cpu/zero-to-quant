# Concept audit: equations levels 1 to 3 (round 1, blind)

Audit name `equations-1-3`. Commit read: c7d4b505. Stage 0, reduced ledger depth.

Scope: `l1` to `l13`, `review-1` to `review-3`, `homework-1` to `homework-3`, `problems-1` to `problems-3`, and the fluency sets for l2, l3, l4, l6, l7, l8 and l13 (29 files). Level 4 and `fluency-l15` are out of scope.

Sources: Gelfand and Shen, *Algebra* (letters and notation, the commutative and distributive laws, equations, inequalities); a standard GCSE and A-level algebra text (expressions, linear equations, inequalities on a number line, rearranging formulae).

Ledger: `docs/reports/audit-equations-1-3-ledger.md`, 1,068 rows: correct 1,064, wrong 1, imprecise 3, misleading 0, unverified 0.

Concepts script: `docs/reports/equations-L1-3-concepts.py`, 761 checks, exit 0. It recomputes from each item's givens every numeric key, slip value, drag target and table cell. It tests the algebra of every expression and algebraic choice item with sympy, the solution set of 31 inequality items, and each fluency family over its whole variable range. These levels make no empirical or statistical claim, so there is no Monte Carlo part.

## Findings

1. `review-1.json` | `items[2].widget.options[sign-9].why` | wrong, minor | The option is $6n + 5$ and the line says "You added the 9. It follows a minus sign: $4 - 9 = -5$." Adding the 9 gives $4 + 9 = 13$, so that slip's value is $6n + 13$, not $6n + 5$. | $6n + 5$ comes from taking 4 from 9 and dropping the sign, $9 - 4 = 5$. Auditor rule 5: a line that names a mistake must give that mistake's value. The option is still correctly a wrong option (script: differs from $6n - 5$). | Replace the `why` with: `You took 4 from 9 and lost the sign. The 9 follows a minus sign: $4 - 9 = -5$.`

2. `l10-ranges-of-answers.json` | `quiz[0].widget.options[e].why` | imprecise, minor | "With negatives, the bigger digit is the smaller number." This is a digit rule, and it fails as stated: for $-19$ and $-21$ the bigger digits belong to $-19$, the larger number; it says nothing useful about $-3.5$ against $-3.25$. | For negative numbers the one further from 0 is the smaller (Gelfand and Shen, negative numbers and order; the lesson's own number-line reading, "lies left of"). | Replace the `why` with: `−4 lies left of −3. With negatives, the number further from 0 is the smaller one.`

3. `l12-trapped.json` | `quiz[3].explain.text` | imprecise, minor | "The solution set is empty, which is why the smaller limit always goes on the left." The same lesson writes $2 \ge x > -3$ at `screens[5]`, a true statement with the larger limit on the left. What fails in $5 < x < 2$ is the limit order for symbols pointing that way, not an "always". | $a < x < b$ is empty exactly when $a \ge b$; $b > x > a$ is the same set written the other way round (Gelfand and Shen, inequalities: $a < b$ means $b > a$). | Replace the last sentence, so the text reads: `$5 < x < 2$ means $x > 5$ and $x < 2$. A number bigger than 5 cannot also be below 2. The solution set is empty, so with $<$ signs the smaller limit must go on the left.`

4. `l13-changing-the-subject.json` | `screens[4].explain.text`, `screens[6].widget.lines[d]`, `summary.formula.note`; `homework-3.json` `items[4]` | imprecise, minor | The lesson divides by $Pr$, $s$, $p - c$ and $1 + r$, and the homework by $y - 1$, with no word that the divisor must not be zero. l5 ("Divide only by a number that is not zero"), l6 ("needs $a \neq 0$"), l7 and homework-2 ("allowed only when $a \neq c$") say it for numbers, then the condition is dropped once the divisor is a letter or a bracket. A learner takes away that a rearranged formula holds for every value. | Division by zero is undefined, so $q = \dfrac{F}{p - c}$ fails at $p = c$ (no break-even exists), $P_0 = \dfrac{P_1}{1 + r}$ at $r = -1$, and $x = \dfrac{y + 2}{y - 1}$ at $y = 1$ (no $x$ gives $y = 1$). | In `l13` set `summary.formula.note` to: `Test any rearrangement with one row of numbers. Divide only by something that is not zero: here $r \neq -1$.` In `homework-3` `items[4].explain.text` replace the last sentence with: `Then one division frees it, which needs $y \neq 1$.`

Severity counts: wrong 1 (serious 0, minor 1); imprecise 3 (serious 0, minor 3); misleading 0.

## Checked and found sound (the watch list)

- Same to both sides: every manipulate state was re-derived, including the "one side only" states, which the content correctly presents as breaking the balance. No item squares both sides. Division by a possibly zero number carries its condition in l5, l6, l7 and homework-2 (finding 4 covers l13).
- Inequality flips: all 31 inequality items match their sympy solution sets, including both signs of each double inequality and the end that stays included after a flip (`problems-3` van item, `l12` quiz).
- No solution and every solution: l7 `screens[5]`, l7 `quiz[2]`, homework-2 `items[8]` and the l7 summary are right.
- Rearranging: all eight formula items equal sympy's solved form, and every wrong option differs.
- Rounding in word problems: the safe direction is right in all nine items (budget rounds down, break-even and cash-raising round up, whole pence in homework-2 and problems-2).
- Money and percentages: each percentage names its base (0.5% of the value of the shares, 0.25% of the sale value, 6% below the entry, 25% of the account); pence and pounds are converted where mixed.
- Fluency: for each of the 14 families in scope the key solves the item and neither slip ever equals the key, over every draw of the variable ranges.

## Notes for the fixer (not conceptual findings)

- Learner-facing prose cites lesson ids: "as in l1" (`l13` `screens[0].explain`), "as in l4" (`l9` `screens[7].prose`), "as in l9" (`l13` `screens[4].prose`). A learner sees lesson titles, not ids.

## Tool results

- Validator: `node tools/validate.mjs`, 0 errors.
- Number scripts: `node tools/run-number-scripts.mjs --only equations`, 6 of 6 passed.
- `node tools/grade-all.mjs --file` on all 29 files with `--local-cdn`, 6 fluency seeds: 1,065 widgets, 0 failures.
- Concepts script: 761 checks, exit 0. Run with the scratch venv (sympy 1.14.0); no figure depends on a library version.
- No playthrough was run (auditor rules).

## Overlap with earlier reads

Read after the ledger and findings were written: `review-equations-1-2.md` (l1 to l9, review and homework 1 and 2), `review-equations-3-4.md` (its level 3 part), `review-problems-0.2-a.md` (problems-2 and problems-3). The reuse and freshness reviews that name equations hold no conceptual finding in scope. No earlier concept audit of this course exists.

| Conceptual findings | Count |
|---|---|
| This audit only | 4 (findings 1 to 4) |
| Earlier reads only | 14 (review-equations-1-2 findings 1 to 7; review-equations-3-4 findings 2, 4, 5, 6, 7, 9, 10) |
| Both (same defect) | 0 |

All 14 earlier findings were fixed before c7d4b505, and each fixed line was read here as a ledger row and stands `correct`. New `wrong` that no earlier read found: 1 (finding 1, minor). The three lesson-id citations noted for the fixer came from the earlier fix passes (review-equations-1-2 finding 17, review-equations-3-4 findings 11 and 12).

Earlier findings counted as not conceptual: entry forms and grader behaviour (1-2 finding 8, 0.2-a findings 1 to 7), key length, bands, freshness, lesson shape and voice.

## Fix pass

Opus fixer, from 1a9cdc01. No key, slip value, hidden test or solution changed; all edits are `why`, `explain`, `prose` or `note` text.

1. `review-1` `items[2]` option `sign-9` | fixed | Own check: $4 + 9 = 13$ would give $6n + 13$; $6n + 5$ is $|4 - 9|$ with the sign dropped, i.e. $9 - 4$. Text now: "You took 4 from 9 and lost the sign. The 9 follows a minus sign: $4 - 9 = -5$."
2. `l10` `quiz[0]` option `e` | fixed | For $a, b < 0$, $a < b \iff |a| > |b|$ (order is reversed by $x \mapsto -x$); the digit rule fails on $-19$ against $-21$. Text now: "With negatives, the number further from 0 is the smaller one."
3. `l12` `quiz[3]` explain | fixed differently | $a < x < b$ is non-empty exactly when $a < b$, while $2 \ge x > -3$ (screens[5]) is valid with the larger limit first. Last sentence now: "The solution set is empty. With $<$ signs, a number can pass only when the smaller limit is on the left." (Stated as the condition for any number to pass, rather than "must".)
4. `l13` summary, `homework-3` `items[4]` | fixed | $P_0(1 + r) = P_1$ at $r = -1$ reads $0 = P_1$, so no division; $y = \frac{x+2}{x-1} = 1$ forces $x + 2 = x - 1$, impossible, so $y \neq 1$ is needed. Stated once in each: l13 `summary.formula.note` gains "Divide only by something that is not zero: here $r \neq -1$."; homework-3 explain ends "Then one division frees it, which needs $y \neq 1$." The $p - c$ step in `screens[4]` is left to the summary line, as asked ("state it once").
5. Inbox note, lesson ids in learner prose | fixed | Each cited lesson checked to hold the idea: l1 teaches substituting, l4 `screens` and l9 define break-even. Replaced with italic titles from `course.json`, the form other courses use: l13 `screens[0].explain` "as in *Letters that stand for numbers*"; l13 `screens[4].prose` "as in *Turning a story into an equation*"; l9 `screens[7].prose` "as in *Putting brackets back*". A grep for `as in l<n>` in the course now finds nothing.

Gates: validator 0 errors; voice scan 35 on the six edited files 0 and 0; concepts script 761 checks, exit 0, unchanged (it holds no check on the edited text); `run-number-scripts --only equations` 6 of 6 passed; `grade-all --file` 0 failures on each edited file; playthrough of l9, l10, l12, l13, review-1 and homework-3 green desktop and `--mobile`.
