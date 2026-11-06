# Topic 3.4 exam: pure mathematics

File: `app/content/exams/topic-3.4.json` (100 minutes, pass 0.7, 30 items, all twelve skills of `algebra` and `topology`). Scripts: `docs/briefs/exam-3.4-scripts/` (`build.py` route A, `check_numbers.py` route B, `fresh.py`).

## Result

- Ramp 6, 15, 6, 3 at difficulties 2 to 5; pace 4,995 s (83 min).
- By course and level: algebra L1 3, L2 5, L3 5, L4 4; topology L1 4, L2 4, L3 5.
- Coverage: every level of both courses has an auto-graded item on a skill first met there. `check_numbers.py` checks this from `course.json` and the lesson files, and checks that all twelve skills sit on auto items.
- Kinds: 7 parts, 7 multi, 6 numeric, 6 choice, 1 table, 2 order proofs, 1 longform (self-marked, 10-point rubric).
- Proofs: every subgroup of a cyclic group is cyclic (L2, `same` on two steps), and the set where two maps into a Hausdorff space agree is closed (L2 with L1, `same` on the two preimages). Each has two flawed lines. The longform proves that $T$ has one fixed point when some $T^k$ contracts, then applies it to $e^{-x}$ on $[0, \infty)$, where only $T^2$ contracts.
- Notation follows the review-algebra-1-2 Continuity list: right-to-left products, $e$, $\operatorname{ord}$, $\mathbb{Z}_n^{\times}$, $\varphi$ for a homomorphism with Euler's function named each time. Topology uses $\overline{A}$, $A^\circ$, $\partial A$, $\tau$, $d_1$, $d_2$, $d_\infty$, and $T$ with constant $q$.
- Hypotheses: each general claim names its setting (finite group, abelian, over a field, commutative ring with $1 \ne 0$, Hausdorff, complete metric space, Heine-Borel in $\mathbb{R}^n$).
- The table item keys its slip lines on the `wrong[].id` (`sigma-first-k`), not on cell ids.

## Gates

- Validator: 0 errors, no topic-3.4 warnings.
- Voice scan on a copy (`VOICE_BASE=<scratch>/voice34/`): 0 sentences over 20 words, 0 explanations over three sentences, 712 sentences. No exclamation marks, em-dashes or en-dashes.
- `check_numbers.py`: 311 of 311, exit 0. Route B is brute force: orders by repeated multiplication, $S_4$ and $S_6$ enumerated, normality by conjugating with all 24 elements, irreducibility by trial division over $\mathbb{Z}_3$, topology axioms over every pair. Permutations are parsed from the printed cycle notation. Maxima come from fine grids, integrals from Simpson, fixed points from bisection. Boundaries come from sampled small balls. It checks every key, every `wrong`, every choice key and `check_wrongs`. A final pass reads every number in every learner-visible string.
- Playthrough with `--local-cdn`: green with and without `--mobile` (30 of 30, 39 widgets). Screenshots at 1280 and 440 px checked, including the table, both order items, the parts items and the longform.

## Freshness

Six clashes were changed before the gates. The non-metric $(x - y)^2$ at 0, 1, 2 is analysis l22's example, and so is $|x^2 - y^2|$; the item became a jump metric that passes. The preimage of $(1, 4)$ under $x^2$ is topology l4's; it became $x^2 - 4x$ and $(-3, 5)$. Newton's $\tfrac x2 + \tfrac1x$ is topology l13's; it became a contraction of the plane in $d_\infty$. $x^4 + 2x^2 + 1$ is algebra review-4's trap; it became $(x^2 + 1)(x^2 + x + 2)$ over $\mathbb{Z}_3$. $\tau = (1\,2)(3\,4\,5)$ is algebra l8's example; it became $(1\,5)(2\,3\,4)$. $3^{100}$ is brainteasers homework-3's (mod 7); it became $5^{100} \bmod 14$. The 21 hits left are unrelated: generic strings or numbers in other courses, a different question on $\mathbb{Z}_{11}^{\times}$ (homework-1 asks the order of 2), and $xe^{-x}$ in l10.

## Notes

- A byKey line first said $5^9 \equiv 3$; route B gives 13. The line now says 13, and the script asserts the stated residue.
