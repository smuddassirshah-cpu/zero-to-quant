# Delta review: topology problems-2, `p-right-rays` (session AI re-author)

Method: read the item as a learner; recomputed by hand every number and claim (closure of (1,2) ∪ {5} is (-inf, 5]; interior of [3,8] ∪ (10, inf) is (10, inf); homeomorphisms of the right-ray line are exactly the increasing bijections, so x+5, x^3, x-10 give 3; subspace (-inf, 5] has non-empty opens (-inf,5] and (t,5], t<5, so it is connected and not Hausdorff). Ran `problems-topology-numbers.py` with the venv Python (764 checks, 0 failures; system python lacks sympy) and `grade-all.mjs --file` (16 widgets, 0 failures). Voice scan by hand and script: no em-dashes, no exclamation marks, no sentence over 35 words.

Keys, bands, distractors and their `why` lines are all correct. Findings:

1. unclear | part 3 | The chain is cosmetic. The answer 3 holds for any c and k (every shift x+a, x-a is a homeomorphism; c-x never is), so a learner who skipped parts 1 and 2 gets it right with any guess. Fix: make a map's status depend on the value, for example replace `x - k` with a map such as `x^2 - k` or `(x - k)^3 + c`... or better, ask for a quantity that needs both values (for instance the image of the interior's left end k under `x + c`, then state whether the result is a homeomorphism image). Acceptable alternative: keep as is and drop "the chain is real" from the claims for part 3.

2. unclear | part 4 | Options hard-code 5 (`(-1, 5]`, `(0.5, 5]`, `(0, 5]`) although the question says "Take the closed set (-inf, c] from part 1". This gives away part 1's answer and lets a learner skip it. Fix: write the options with `c` (`(-1, c]`, `(0.5, c]`, `(0, c]`), including the feedback and explain lines, or state in the question that the learner should substitute their c.

3. unclear | part 4 | The key option states its own reason ("any two non-empty open sets meet"), and the question already lists the open sets, so the choice is close to a reading exercise. Fix: shorten the key to "It is connected but not Hausdorff." and leave the reason to the feedback.

4. style | part 2 `byKey.usual` | "the left end of (3, 8) ∪ (10, inf)" is true but awkward, since that set has left end 3 only because of its first piece. Fix: "That is the left end of the usual-topology interior, (3, 8) ∪ (10, inf)."

Wrong: none.

## Fix pass

1 fixed: part 3 now asks for the image of the ray from part 2 under the shift by part 1's c, key 15 (was 3), so it needs both. 2 fixed: part 4 options use $c$. 3 fixed: key option shortened. 4 fixed: `usual` reworded. Script extended; all checks green.
