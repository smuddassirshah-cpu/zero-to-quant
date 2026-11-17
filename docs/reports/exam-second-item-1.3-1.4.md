# Second auto item for one-item skills: topic-1.4 and topic-1.3

Brief: `docs/briefs/exam-second-item.md` (session AG, PLAN task 4). Numbers: `docs/reports/exam-second-item-1.3-1.4-numbers.py` (160 of 160 checks, exit 0). Scratch: `scratchpad/exam2-1.3-1.4/` (`pairs.py` recomputes the pairs, `gen.py` writes the items).

Both exams held 30 items, so rule (a) was closed: rules (b) and (c) apply. Item counts stay at 30 and minutes at 60, so no hours note.

## Pairs, recomputed

Rule: a skill tagged on a level review of a course whose `topic` is the exam's, with fewer than two auto (non-longform) items in the exam. Recomputed from the exam files, every `course.json` and its reviews; the lists match the 16 Nov table.

| exam | skill | levels | the one item before |
|---|---|---|---|
| topic-1.4 | la-vectors | vectors/L1, L2 | a-portfolio-dot |
| topic-1.4 | la-product | vectors/L2, L3 | a-order-matters |
| topic-1.4 | la-inverse | vectors/L3 | a-hedge |
| topic-1.4 | gx-elim | elimination/L1, L3 | a-eliminate |
| topic-1.4 | gx-spaces | elimination/L2 | a-column-space |
| topic-1.4 | ls-qr | least-squares/L1, L2 | a-qr |
| topic-1.4 | eg-svd | eigen/L3, L4 | a-svd |
| topic-1.3 | in-area | integrals/L1, L2, L3 | c-left-sum |
| topic-1.3 | lm-rules | limits/L2, L3, L5 | c-quotient |
| topic-1.3 | mv-partial | multivar/L1, L2, L3 | c-partials |
| topic-1.3 | ty-converge | taylor/L1, L2, L3 | c-radius |

## topic-1.4: five swaps, seven pairs placed

| new id | skills | d | widget | task | replaces (skills, d) |
|---|---|---|---|---|---|
| a-desk-lengths | la-vectors | 2 | numeric | length of a merged P&L vector from two lengths and a dot product (key 15) | a-rank-null (gx-rank, 2) |
| a-undo-two-steps | la-inverse, la-product (b) | 3 | expression, matrix | the matrix that undoes $\mathbf{p} = \mathbf{A}\mathbf{B}\mathbf{g}$ from the two stored inverses, $\mathbf{B}^{-1}\mathbf{A}^{-1}$ | a-char-poly (eg-eigen, 3) |
| a-reachable-k | gx-elim, gx-spaces (b) | 3 | numeric | eliminate $[\mathbf{A} \mid \mathbf{b}]$ for a rank-2 $3 \times 3$ matrix and find the $k$ that makes it solvable (key 5) | a-beta (ls-fit, 3) |
| a-qr-solve | ls-qr | 3 | numeric | least squares from a given $\mathbf{Q}$, $\mathbf{R}$: $\mathbf{R}\hat{\mathbf{x}} = \mathbf{Q}^T\mathbf{b}$, back substitution (key 2) | a-det-inverse (gx-det, 3) |
| a-rank-one | eg-svd | 4 | numeric | an entry of the best rank-1 approximation of a $3 \times 2$ matrix, via $\mathbf{A}^T\mathbf{A}$ (key 8) | a-pca-share (eg-pca, 4) |

Both (b) items need both skills: the inverse rule alone gives no matrix without the product, and the product alone gives the wrong order; the solvability condition comes only from carrying $\mathbf{b}$ through the elimination. Removals were the weakest or most duplicated items whose skills keep two other auto items: gx-rank 3 to 2 (a-solutions, a-redundant), eg-eigen 4 to 3, ls-fit 4 to 3 (a-beta duplicated the regression of a-code-normal-eq), gx-det 3 to 2 (a-det-area, a-redundant), eg-pca 3 to 2 (a-pca-share was the share sum that a-code-pca-changes also computes). a-char-poly was the only expression item, so a-undo-two-steps is an expression item; the order item a-normal-order was kept for the same reason. Difficulty mix unchanged (5, 15, 7, 3). After: every skill of the exam has at least two auto items (la-vectors, la-product, la-inverse, gx-elim, gx-spaces, gx-rank, gx-det, ls-qr, eg-svd, eg-pca, eg-diag, la-transform, ls-orth 2; eg-eigen, ls-proj, ls-fit, eg-pd 3). Pairs left: none.

## topic-1.3: three swaps, four pairs placed

| new id | skills | d | widget | task | replaces (skills, d) |
|---|---|---|---|---|---|
| c-trapezium | in-area | 2 | numeric | trapezium estimate from five readings with no formula (key 21) | c-log-return (ty-finance, 2) |
| c-quotient-partial | lm-rules, mv-partial (b) | 3 | numeric | $\partial f / \partial y$ of $\frac{xy^2}{x + y}$ at $(2, 1)$ by the quotient rule (key $\frac{10}{9}$) | c-pnl-peak (in-apply, 3) |
| c-terms-needed | ty-converge | 3 | numeric | smallest degree of $T_n$ for $e^x$ on $|x| \le 0.3$ with Lagrange error below $10^{-5}$ (key 5) | c-double (mv-integrals, 3) |

Removals: ty-finance 3 to 2 (c-convexity, c-yield-newton), in-apply 4 to 3, mv-integrals 3 to 2 (c-gauss-disc, c-change-and-constrain). c-log-return was a one-line substitution into a given formula, c-pnl-peak a choice item on the most duplicated skill, and c-double a routine rectangle integral. Choice items fall from 4 to 2. Difficulty mix unchanged (5, 14, 7, 4). After: every skill has at least two auto items (in-techniques, mv-optimise, lm-optimise, mv-lagrange, in-apply 3; the rest 2). Pairs left: none.

## Reuse

Each new item is a different task from the exam's existing item on its skill (dot product versus length of a sum; pivots versus the solvability condition; Gram-Schmidt versus solving from QR; $\sigma_1$ versus the rank-1 piece; a left sum versus the trapezium rule; a radius versus the Lagrange degree). `fresh-check.mjs --file`: 0 hits on both exams. Advisories on new items: a-undo-two-steps shares the stock instruction "type it row by row as `[[a, b], [c, d]]`" with three problem sets; a-reachable-k first shared a 12-word stem with `elimination/problems-2` item 2 part 3 (another matrix, a futures story), and the question was reworded. No number set, matrix, story or sentence is shared with the stage-1 exam, the mocks, or the courses' lessons, reviews, homework, problem sets and Fluency sets.

## Gates

- `node tools/validate.mjs`: 0 errors; no warning on a new item (the files carry two older warnings, topic-1.4 items[22] and topic-1.3 items[14]).
- `VOICE_BASE=app/content/exams python3 docs/reviews/voice-scan.py 35`: 0 explanations over three sentences, 0 sentences over 35 words.
- `grade-all.mjs --file`: topic-1.4 23 widgets, topic-1.3 25 widgets, 0 failures each.
- `playthrough.mjs --exam` with `--local-cdn`: topic-1.4 and topic-1.3 30 of 30, passed, desktop (with `--why`) and `--mobile`; the 440 px screenshots of the eight new items show no overflow.
- Number script exits 0.
