# Problem set 3.4, algebra level 4: second-reader findings

Scope: `app/content/courses/algebra/problems-4.json`: 3 problems, 14 parts (11 numeric, 1 `expression`, 2 choice), 23 `wrong` entries. Rules: `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md` (Reader, Author rules, session AE additions), `docs/briefs/wave-c-author-ag.md` rules 1 to 6, `docs/briefs/wave-c-reader-ag.md` rules 1 to 5. Format: `review-problems-analysis-1-3.md`.

## Verdicts

| problem | closest lesson screen | closest quiz item | closest review item | closest homework item | closest other set problem | closest exam item | verdict |
|---|---|---|---|---|---|---|---|
| `p-cipher-29` | `l14` `screens[6]`, `[7]` (real $2 \times 2$ matrices as a ring; canvas $\begin{pmatrix}1&0\\0&0\end{pmatrix}\begin{pmatrix}0&0\\0&1\end{pmatrix} = \mathbf{0}$) | `l14` `q-units-closed` (units form a group) | `review-4` `items[1]`, `[3]` ($7^{-1} \bmod 15$, $4^{-1} \bmod 11$) | `homework-4` `items[4]` (key split over $\mathbb{Z}_{13}$, $3^{-1}$ given) | none in sets 1 to 3 (no matrix over $\mathbb{Z}_n$, no cipher) | `topic-3.4` `e-which-fields` (option "The real $2 \times 2$ matrices") | **clean** as a chain; one reused matrix pair in a `why` (finding 3) |
| `p-sixteen-factorial` | `l17` `screens[3]` "At most d roots"; `l13` `screens[3]` (Fermat) | `l17` `q-count-quadratics` | `review-4` `items[5]` (roots of $x^2 - 4$ in $\mathbb{Z}_{12}$) | `homework-4` `h-prove-roots` (rubric line 3) | none in sets 1 to 3 (no factorial, no $x^{p-1} - 1$) | `topic-3.4` `e-remainder-z7` | **reuse**, part 2 only (finding 2); parts 1, 3, 4, 5 are a new chain |
| `p-three-year-return` | `l17` `screens[7]` (rational root test on $x^3 - 2$); `l16` `screens[6]` (divide by $x - 3$) | `l16` quiz 1 (is a division valid) | `review-4` `items[4]` (remainder of $x^3 + x + 1$ at 2) | `homework-4` `items[2]` (division over $\mathbb{Z}_3$) | none in algebra; `numerics/problems-2` `p-project-irr` (another course: three-year cubic in $v$, solved by Newton) | `topic-3.4` `e-irreducible-z3` | **clean** |

No problem is ruled re-author. None walks several quiz, review or exam items in a row. The one retold step is a single part, and its exact replacement is in finding 2.

Both texts for the `reuse` ruling:
- `l17` `screens[3].explain`: "A root $a$ splits $f = (x - a)q$. Any other root $b$ has $(b - a)q(b) = 0$, so $q(b) = 0$ in a field."
- `problems-4` `items[1].parts[1].explain`: "By the factor theorem, $f = (x - 1)g$. For $b \ne 1$, $0 = f(b) = (b - 1)g(b)$ forces $g(b) = 0$, as $\mathbb{Z}_{17}$ is a field."

## Method

The author's script was run first. `l13` to `l17`, `review-4`, `homework-4` and the five `topic-3.4` exam items carrying `ag-rings` or `ag-poly` were read as learner text (a dump of every string per file; no other exam file has an item with those skills). Each part was solved by hand, then in `docs/reports/problems-algebra-4-numbers-read.py`, which imports nothing from the author's script. Route: brute force and exact arithmetic where the author used rules. Each row of $\mathbf{K}^{-1}$ is found by search over $29^2$ pairs. The plaintext is found by coding all 841 pairs. $(x - 1)\cdots(x - 16)$ is multiplied out in $\mathbb{Z}_{17}[x]$ and $16!$, $15!$, $14!$ are reduced from the integers. The rational candidates are substituted as exact fractions, the long division is run step by step, and real roots are counted by exact sign changes on a grid. Claims were checked too: the determinant test and the centre of $M_2$ on all 625 matrices over $\mathbb{Z}_5$, each distractor's counterexample, the break-even equation, the £8,000 check. Every `wrong` value was rebuilt from its named slip. The 12 typed parts then went through the engine's graders in node (`numGrade`, `exprGrade`, local Compute Engine) with 62 strings of my own.

## Tool results

| check | result |
|---|---|
| author's script | `problems-algebra-4-numbers.py` 173 of 173, exit 0 |
| reader's script | `problems-algebra-4-numbers-read.py` 172 checks, exit 0, 4 `FINDING` lines (findings 1 to 4) |
| engine graders, 12 typed parts | every key accepted, every `wrong` value routed to its own line; 1 fault (finding 1) |
| `grade-all.mjs --file` | 14 widgets, 0 failures |
| validator | 0 errors, 4567 warnings, none on this file; `manifest.json` restored |
| voice scan 35, course folder | 0 and 0 |
| `fresh-check.mjs --files ... --pairs` | 0 hits, 1 advisory (27, 28, 23 with `mock-oa-trader`, a mental-arithmetic item: no action) |
| browser, playthrough | not run (reader rule) |

Result. All 12 typed keys and both choice keys agree with mine, as do all 23 `wrong` values and every number printed in a feedback or explain line. No learner is marked wrongly. Every claim holds: the unit test by determinant, "only the multiples of $\mathbf{I}$ commute with every matrix", Fermat's hypothesis ($a \ne 0$, and $f(0) = -1$ checked apart), the root bound attained, the monic argument for the constant, the rational root test as worded in `l17`, and "one real root". Bands: all whole-number or exact, no rounding tie, the percentage part carries unit "%", slip bands are `abs 0` or `0.0001`. Chain: each later part restates the value it uses, the last part of each problem is its result, and `l14` to `l17` are all drawn on.

## Findings

1. `algebra/problems-4.json` | `items[2].parts[2].widget` | misleading | the quotient part is passed by retyping the question (brief rule 3; AUTHORING "Choosing `form`").
   Evidence: `exprGrade` accepts `\frac{8x^3-6x^2-x-5}{4x-5}` and `(8x^3-6x^2-x-5)\div(4x-5)` as correct; $f$ is printed in the prose. Also accepted: `\frac{8x^2+4x+4}{4}`.
   Exact fix: add `"form": "expanded"` to the widget, and to `feedback.byKey` add `"form": "That equals the quotient, with the division left undone. Carry it out and give $ax^2 + bx + c$."` Tried on an in-memory copy: `2x^2+x+1`, `1+x+2x^2`, `2x^{2}+x+1` and `q(x)=2x^2+x+1` still pass; both retyped forms, `x(2x+1)+1` and `\frac{8x^2+4x+4}{4}` return `form`; `8x^2+4x+4` still returns `by-root`. (`"simplified"` does not work: it accepts the retyped fraction.)

2. `algebra/problems-4.json` | `items[1].parts[1]` (`explain.text`, `options[1].why`) | reuse | the explanation retells `l17` `screens[3]` (texts above; the same step is rubric line 3 of `homework-4` `h-prove-roots`), and the `splits` counterexample is the lesson's own: `l17` `screens[6]` shows $x^2 + 1$ with no root in $\mathbb{Z}_3$.
   The part itself stays: the lesson proves a bound, the part uses the step to reach a full factorisation, a new conclusion.
   Exact fix, `explain.text`: "This is the step behind the root bound of l17, used 16 times. Dividing out $x - 1$ leaves a quotient that still has the roots 2 to 16, since $\mathbb{Z}_{17}$ has no zero divisors. Sixteen divisions leave a constant, which is 1 because $f$ and the product are both monic."
   Exact fix, `options[1].why` (`splits`): "Not over every field: $x^2 - 3$ has no root in $\mathbb{Z}_{17}$, so it has no linear factor there." Checked: the squares modulo 17 are 0, 1, 2, 4, 8, 9, 13, 15, 16, so 3 is not one. $x^2 - 3$ appears nowhere in `courses/algebra` or `topic-3.4`.

3. `algebra/problems-4.json` | `items[0].parts[0].widget.options[2].why` (`field`) | reuse | the zero-divisor pair is the canvas of `l14` `screens[6]`: matrices `[[1,0],[0,0]]` and `[[0,0],[0,1]]`, product $\mathbf{0}$ (`fresh-check` does not read canvas params).
   Exact fix: "A matrix ring is not a field. It is not commutative, and $\begin{pmatrix}0&1\\0&0\end{pmatrix}^2 = \mathbf{0}$ shows a zero divisor." Checked; the matrix appears nowhere in `courses/algebra` or the exams.

4. `algebra/problems-4.json` | `items[2].parts[0]` (`question`, `feedback.byKey.added`) | misleading | "How many positive fractions" can be read as leaving out the whole numbers 1 and 5. That count is $8 - 2 = 6$, the `added` value, whose line then describes a slip the learner did not make.
   Exact fix, `question`: "How many positive candidates $\tfrac uv$, whole numbers included, pass this test for $f$? Give a whole number."
   Exact fix, `byKey.added`: "6 adds the 2 choices of $u$ to the 4 of $v$, or leaves out the whole numbers 1 and 5. Each $u$ pairs with each $v$, so multiply."
   If the question changes, `feedback.correct` may keep "distinct fractions" or read "distinct candidates".

5. `algebra/problems-4.json` | `items[0].parts[2].feedback.byKey.sign` | continuity | 2 is also $15^{-1}$, the answer that follows from the `reversed` slip of part 2 ($30 \equiv 1$). The line names only the sign slip.
   Exact fix: "$14 \cdot 2 = 28 \equiv -1$, so 2 is $-14^{-1}$, and it is also $15^{-1}$. The inverse of 14 is its negative, $-2$."

6. `algebra/problems-4.json` | `items[0].prose` | continuity | parts 1 and 4 need the determinant test and the $2 \times 2$ adjugate over a ring. Level 4 never states either (`l14` names the real $2 \times 2$ matrices as a ring and stops); they come from stage 1 over $\mathbb{R}$. The explanations give them, the prose does not.
   Exact fix, append to `prose`: " As over $\mathbb{R}$, $\mathbf{K}\operatorname{adj}\mathbf{K} = (\det\mathbf{K})\mathbf{I}$ holds over any commutative ring." This does not give away part 1: the learner must still say why $\det\mathbf{K}$ has an inverse.

Read and left alone: `items[1].parts[3]` `kept` (16) is also what the `plus-one` slip of part 3 gives ($1 \cdot 16^{-1} = 16$), and its line is true either way. `items[2].parts[3]` has two sensible answers only (1 or 3), which a result part may have. The IRR story exists in `markets` l4 and `numerics/problems-2` with other numbers and another method (search, Newton); the algebra course has none.

## Engine

- `fresh-check` reads no `canvas.params` matrices of a lesson, so a matrix pair shown on a canvas and retold in a set's `why` is not reported (finding 3).
- An `expression` part with no `form` whose key is a polynomial and whose stem holds a `\div` or a fraction of polynomials could raise a validator warning (finding 1; the class of `review-problems-analysis-1-3` finding on a retyped question).

Inbox bullets, `Raised later (review problems algebra):` the two lines above. Not written to `docs/BACKLOG-INBOX.md` by this reader (review and script only are committed).

## Fix pass

1. Fixed: `items[2].parts[2]` now has `"form": "expanded"` and a `byKey.form` line. Recomputed: the key `2x^2+x+1` is the expanded quotient of $8x^3 - 6x^2 - x - 5$ by $4x - 5$.
2. Fixed: `items[1].parts[1]` `explain.text` and `options[1].why` replaced as given. Squares mod 17 recomputed: 0, 1, 2, 4, 8, 9, 13, 15, 16, so 3 is not one.
3. Fixed: `items[0].parts[0].widget.options[2].why` uses $\begin{pmatrix}0&1\\0&0\end{pmatrix}^2 = \mathbf{0}$.
4. Fixed: `items[2].parts[0]` `question`, `byKey.added` and `correct` ("distinct candidates"). $8 - 2 = 6$ rechecked.
5. Fixed: `items[0].parts[2].feedback.byKey.sign`. $14 \cdot 2 = 28 \equiv -1$ and $15 \cdot 2 = 30 \equiv 1$ rechecked.
6. Fixed: sentence appended to `items[0].prose`.

Gates: author script 177 of 177 (four checks added), reader script 172 checks, 0 FINDING lines, both exit 0. Validator 0 errors, nothing on this file. Voice scan 0 and 0. `fresh-check` 0 hits (the one advisory is the known `mock-oa-trader` one). `grade-all` 14 widgets, 0 failures. Playthrough green with and without `--mobile`. No graded answer or `wrong` value changed.
