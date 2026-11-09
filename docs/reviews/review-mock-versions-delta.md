# Delta read: changed items in mock versions

Reader: delta second reader, at commit 43883132 of `claude/amazing-wright-d4mx7i`. Scope: only the items that the two fix passes replaced or re-keyed (`## Fix pass` in `review-exam-mock-oa-trader-versions.md` and `review-exam-mock-oa-sig-versions.md`). Each item was solved blind (question and options printed without key, with `mock-versions-delta-scripts/show.py ... blind`), then compared with the key.

Evidence: `docs/reviews/mock-versions-delta-scripts/check.py` (scratchpad venv, seed 20261109, about 10 seconds, exit 0). It recomputes every changed key by exact enumeration and by a second method (closed form or seeded simulation), and runs a rival-rule search on each changed sequence: polynomials of degree 0 to 3, linear recurrences of order 1 to 3 with integer coefficients and a constant, "times k plus a linear term", periodic gaps, two and three interleaved strands, residue classes mod 2 to 14 (counted only over two full periods), the factors of the smallest fitting N, unions of two sets of multiples, and p-smooth numbers. Scope: `node tools/closure.mjs --target mock-oa-trader` reaches vectors/L3 (transpose, inverse) and counting-chance; `--target mock-oa-sig` covers Bayes and branching as before.

Totals: 0 errors, 1 warning, 2 notes.

## Findings

1. **warning**, `app/content/exams/mock-oa-trader-3.json`, `a13-back-if-you-can`, `parts[0].items[12]`. Fails 2(b). Key 20 is right (Recamán: $13 - 7 = 6$ is used, so $13 + 7 = 20$), and no searched rule gives another value, so 2(a) holds in the narrow sense. But the shown gaps $+1, +2, +3, -4, +5, +6$ hold one backward step, so the sign of step 7 is a guess unless the candidate already knows Recamán's "back if new" rule. "Every fourth step goes back" gives 20; "steps 4, 7, 10 go back" gives 6, which is option b. Version 1's item at this place (`a13-consecutive-products`, $n(n+1)$) is found in seconds; this one rewards prior knowledge or a lucky sign. Fix: replace the item (new id, since this id is new in this pass and has no progress data yet; keep the old one if the orchestrator prefers, with this content).
   - id `a13-twice-plus-before`, difficulty 4, title as the paper's pattern.
   - question: "What comes next? 1, 2, 5, 12, 29, 70, ?"
   - rule: each term is twice the one before plus the one before that. $2 \times 2 + 1 = 5$, $2 \times 5 + 2 = 12$, $2 \times 12 + 5 = 29$, $2 \times 29 + 12 = 70$, so $2 \times 70 + 29 = 169$. Second method: the gaps 1, 3, 7, 17, 41 obey the same rule, so the next gap is $2 \times 41 + 17 = 99$ and $70 + 99 = 169$.
   - options: 169 (correct); 140, why "You doubled 70. Each term also adds the one before it: $140 + 29 = 169$."; 99, why "You added the two before, as in Fibonacci. The last term counts twice: $2 \times 70 + 29$."; 111, why "You repeated the last gap of 41. The gaps grow by the same rule: $2 \times 41 + 17 = 99$."
   - feedback correct: "Each term is twice the one before plus the one before that." generic: "The terms grow by a ratio near 2.4. Try twice the last term plus something."
   - explain: "Each term is twice the one before plus the one before that: $2 \times 29 + 12 = 70$. So the next is $2 \times 70 + 29 = 169$. Check: the gaps 1, 3, 7, 17 and 41 follow the same rule, and $70 + 99 = 169$."
   - Rivals: the search finds only `rec2 (2, 1)` (next 169). The cubic through the first four terms misses 29, and ratios, interleaved strands and periodic gaps do not fit. Template check: v1 A7 (Fibonacci) and A15 (tribonacci) add the earlier terms with coefficient 1, so their worked solution with numbers swapped gives 99, not 169. Sibling, not shared template. "29, 70" and "Pell" appear nowhere else in `app/content`.

2. **note**, `app/content/exams/mock-oa-trader-3.json`, `c06-rank`, `parts[2].items[5].explain.text`. Correct, but it restates each line with its value and shows no method; 0.418 is not obvious. The same house style is in v1 and v2 c06, which are outside this delta. Proposed text (three sentences, values checked by enumeration and by the Fibonacci and tribonacci counts): "In 4 tosses, 8 of the 16 sequences avoid two heads in a row, so the chance is 0.500. In 8 tosses, 149 of the 256 avoid three in a row, a count that adds the three before at each length, so the chance is $\tfrac{107}{256} = 0.418$. Four months have 30 days, April, June, September and November, so 0.333."

3. **note**, `app/content/exams/mock-oa-trader-3.json`, `c04-rank-coprime`, `parts[2].items[3].widget.lines`. The top two values are 0.778 and 0.750, a gap of 0.028, below the 0.032 the fixer set as the floor for v2. Exact counting (7 of 9 and 3 of 4) settles it, so no change is needed; record it only if the floor is meant to bind.

## Sound

- `mock-oa-trader-2` `a03-multiples-3-or-5`: key 18 twice; only rival found is the intended rule; d2, as easy as v1 A3.
- `mock-oa-trader-2` `a05-three-power-plus-place`: key 735 ($3^6 + 6$; $3 \times 248 - 9$); no rival; distractors 744, 411, 734 match their whys.
- `mock-oa-trader-2` `a08-three-smooth`: key 18; "factors of 72" no longer fits (16 does not divide 72), factors of 144 also give 18; gaps in the list (5, 7, 10, 11) make the rule findable in time.
- `mock-oa-trader-2` `c01-rank-target` (0.640, 0.490, 0.250; simulation 0.640, 0.491, 0.251), `c02-rank-unbeaten` (1/2, 3/8, 1/4 over all 64 and 8 results), `c03-rank-matrix` (1/2, 3/8, 1/8 over 16; in scope via vectors/L3), `c04-rank-dominoes` (12, 10, 7 of 28), `c05-rank-diagonals` (5/10, 15/36, 35/91, also by a segment-crossing test).
- `mock-oa-trader-3` `b07-dice-run`: 24 of 216 = 1/9 (simulation 0.111); 1/54, 1/12, 1/6 are the named slips (4, 18, 36 of 216).
- `mock-oa-trader-3` `c01-rank-product` (15, 8, 6 of 36), `c02-rank-painted` (12, 8, 6 of 27), `c03-rank-landing` (3/4, 11/16, 5/8 over all 16 runs and by $p_n = 1 - p_{n-1}/2$), `c04-rank-coprime` (7/9, 3/4, 11/16 by gcd and by Moebius), `c05-rank-friends` (41/64, 1/2, 1/8 over all graphs and by inclusion-exclusion), `c06-rank` ranking and key (1/2, 107/256, 1/3).
- `mock-oa-sig-2` `q04-two-swaps`: key 2 over all 100 swap pairs; 1.8, 3 and 1 are the named slips.
- `mock-oa-sig-2` `q07-one-more-toss`: key 1/2 (16 of 32); 13/16 and 11/32 are win-or-tie and half the no-tie chance.
- `mock-oa-sig-3` `q11-extinction`: key 1/2 (root of $2q^2 - 3q + 1$, iteration from 0, simulation 0.499); changed option 1/3 is $\tfrac14 / \tfrac34$, the slip its why names.
- `mock-oa-sig-3` `q13-next-search`: key 12/65 (exact and simulation 0.185); 12/25, 3/13, 4/5 are the named slips.
- Templates: no changed item shares a worked solution with another item in its own version or in versions 1 to 3 of its mock (trader `b12-more-heads` and sig `q07` are in different mocks; trader-2 `b15` and sig-3 `q11` likewise).
