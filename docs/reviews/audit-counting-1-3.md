# Concept audit: counting, levels 1 to 3 (round 1)

Blind audit by a fresh reader. Content at commit `f4fd1dec`. Stage 0 course, so the reduced ledger depth applies: definitions, rules, conventions, every graded key, every wrong option and every slip.

Scope: `l1` to `l13`, `review-1` to `review-3`, `homework-1` to `homework-3`, `problems-1` to `problems-3`, and the two fluency files (25 content files).

- Ledger: `docs/reports/audit-counting-1-3-ledger.md`, 1,140 rows: 1,134 correct, 6 imprecise, 0 wrong, 0 misleading, 0 unverified.
- Concepts script: `docs/reports/counting-L1-3-concepts.py`, 1,908 checks. It exits 1 today: the six failing checks are the four findings below (finding 4 has three places). Everything else passes.

## Method

Every count was found by brute-force enumeration with `itertools`, not by the formula the lesson teaches: arrangements as filtered permutations, selections as filtered combinations, words with repeats by recursion on the multiset (MISSISSIPPI gives 34,650, STATISTICS 50,400), round tables as permutations up to rotation, grid routes as R and U words walked cell by cell from the canvas itself, ties as weak orders. Every probability is exact, a count over the whole equally likely sample space (all 1,326 two-card hands, all 2,598,960 five-card hands, all 3,160 pairs of members). Two Monte Carlo runs of 200,000 draws check the enumeration code against a different method (round table of 8: 2/7; BALLOON with no matching blocks touching: 11/21), each within four standard errors.

Every numeric slip value is recomputed from the mistake its feedback line names, and the script fails if any numeric widget in the course has no recomputation. Choice options are parsed and compared the same way. Vector keys are plain component arithmetic; the dot-product and triangle rules are tested on 5,000 random vectors with the angle taken from `atan2`, not from the formula under test.

Fluency: all seven families were run over their whole variable range (74, 88, 76, 224, 70, 360 and 162 instances). In every instance the key equals an independent count, each slip equals the mistake its line names, and no slip equals the key or the other slip.

## What holds

The points the brief asked me to watch all hold as written.

- Product rule: `l1` states the condition (each stage offers the same number of choices, whatever came before) and `l2` uses it in the derivation of $n! = n(n-1)!$.
- Order or no order: `l3` and `l4` separate rankings from committees with a reason each time, and `l8` proves why top and bottom must be counted the same way.
- Overcounting: labelled copies in `l5`, the block in `l6`, and rotations of a round table. Every round-table item states the convention (identical chairs, turns give the same seating), and the mirror-image slip is wrong under that stated convention.
- Complement and inclusion-exclusion in `l7`: correct, including "the complement of at least two is none or exactly one".
- Probability as favourable over total is stated only with "equally likely" in every item that uses it, and the tree items derive equal path chances from independence first.
- Factorial growth: "faster than any doubling" is true ($n! > 2^n$ from $n = 4$).
- Vectors: free vectors, end minus start, scalar multiples, magnitude, the collinear test (parallel and a shared point), the midpoint theorem, the dot product and its cosine form, and beta as a projection ("regression through the origin" is the correct name for $\mathbf{r}\cdot\mathbf{m} / \mathbf{m}\cdot\mathbf{m}$).

## Findings

Severities: 0 wrong, 4 imprecise (1 serious, 3 minor), 0 misleading.

1. `l3-choosing-in-order.json` | `screens[9].widget.wrong[3]` (id `no-zero`, value 3024) and `feedback.byKey.no-zero` | imprecise, minor | The line says "You started at 9, as if 0 could not come first. A PIN may start with 0." A learner who thinks a PIN cannot start with 0 gets $9 \times 9 \times 8 \times 7 = 4536$, and that value has no slip. The value 3024 is $9 \times 8 \times 7 \times 6$: 0 dropped from every place. | Enumeration: 4,536 four-digit PINs with no repeat and first digit not 0; 3,024 with no 0 anywhere. `homework-1` item `h-pin-no-zero` labels the same two numbers the right way round (4536 is its key, 3024 is "You removed 0 from every place"). | Change the line and add a slip.
   - `feedback.byKey.no-zero`: "You used only 9 digits in every place, as if 0 were banned: $9 \times 8 \times 7 \times 6$. Here 0 is a digit like any other, so start at 10."
   - New `wrong` entry `{ "id": "no-zero-first", "value": 4536, "tol": { "abs": 0 } }` with `feedback.byKey.no-zero-first`: "You gave the first place 9 choices, as if a PIN could not start with 0. It can: 0193 is allowed, so the first place has 10."

2. `l9-arrows.json` | `quiz[3].widget.options[3].why` (item `q-parallelogram`, option `d`) | imprecise, minor | "AC is a diagonal. It is longer and points another way." A diagonal of a parallelogram need not be longer than a side. | Counterexample in the script: A(0, 0), B(10, 0), C(8, 1), D(−2, 1) is a parallelogram with $|AC| = \sqrt{65} \approx 8.06 < |AB| = 10$. By the cosine rule $|AC| < |AB|$ whenever $\cos B > |BC| / (2|AB|)$. The option itself stays wrong: AC and AB leave A for different corners. | `why`: "AC is a diagonal. It leaves A like AB but ends at a different corner, so it is a different move."

3. `l11-how-long.json` | `summary.ideas[1]` | imprecise, serious | "The direction comes from $\tan\theta = \tfrac{u_2}{u_1}$". The lesson defines $\theta$ as the anticlockwise angle from the positive $x$-axis and works one first-quadrant case (`screens[4]` says so). The summary drops that condition. Outside the first quadrant the inverse tangent gives the wrong direction, and no screen says so. | $\mathbf{u} = (-3, 3)$: $\tan\theta = -1$, a calculator returns $-45°$, and the arrow points at $135°$ (checked in the script with the dot product). $\tan\theta$ fixes the line, not which way along it. Pearson Edexcel Pure Year 1, 11.3, has the learner sketch the vector before using the inverse tangent. The course asks for a direction angle only in the first quadrant, so no graded key is affected. | `summary.ideas[1]`: "In the first quadrant the direction comes from $\tan\theta = \tfrac{u_2}{u_1}$; elsewhere sketch the arrow first, because the calculator's angle can be 180° out. The unit vector $\hat{\mathbf{u}} = \mathbf{u} / |\mathbf{u}|$ keeps only the direction."

4. Three "you swapped" lines | imprecise, minor | Each line names a swap of the components, but the option shown is not the swapped vector. The swap of $(2, -1)$ is $(-1, 2)$, not $(1, -2)$. The options are still not parallel to the given vector, so the keys stand. | Script check: swap of $(2,-1)$ is $(-1,2)$; of $(6,-4)$ is $(-4,6)$; of $(3,-2)$ is $(-2,3)$. Each option is the negative of the true swap: the two sizes change places and the signs stay put. | Reword each line to the mistake that gives the option.
   - `l10-adding-arrows.json` `screens[4].widget.options[3].why`: "You swapped the 2 and the 1 but left the signs where they were. $(1, -2)$ is not a multiple of $(2, -1)$."
   - `l10-adding-arrows.json` `quiz[2].widget.options[1].why`: "You swapped the 6 and the 4 but left the signs where they were. That is not a multiple of m."
   - `l12-proving-with-vectors.json` `quiz[2].widget.options[2].why`: "You swapped the 3 and the 2 but left the signs where they were. That is not a multiple of $(3, -2)$."

No finding needs more than a sentence, and no screen needs rewriting.

## Notes that are not findings

- `l10` and `l12` call scalar multiples "parallel" without excluding the zero vector. That is the A-level usage and no item turns on it.
- `l13` summary: "zero exactly when the vectors are perpendicular" holds for non-zero vectors, which every item supplies; `screens[7]` and `quiz[1]` say "non-zero" where it matters.
- `l6` `screens[9]` and `homework-2` `h-any-tie` count rankings with one tie. The ties are stated in full ("the other three P&Ls all differ"), and the weak-order enumeration gives 24 and 240.
- `unit: "%"` items (`l11` `screens[9]`, `homework-3` `h-realised`) hold the key as a fraction, which is the engine convention in `docs/AUTHORING.md`.

## Gates run

- Validator: 0 errors (4,620 warnings, none new).
- `node tools/run-number-scripts.mjs --only counting`: 7 scripts, 7 passed.
- `node tools/grade-all.mjs --file <each of the 24 files> --local-cdn <pkgs>`: 331 widgets and 7 fluency templates, 0 failures.
- No playthrough, as the common rules say.
- Python 3 standard library only, so no version-dependent figure.

## Overlap with earlier reads

Read after the ledger and findings above were written: `docs/reviews/review-counting-1-3.md` (35 findings, all fixed) and the counting part of `docs/reviews/review-problems-0.3-a.md` (12 findings on `problems-1` to `problems-3`, all fixed). There are no author reports for this course (`docs/reports/counting-L*-numbers.py` are number scripts, which I ran but did not read before writing the ledger).

I counted as conceptual the earlier findings about a number, a named slip, a stated reason, a dropped condition or a convention, and left out layout, voice, freshness, chain and tolerance-band findings. That gives 14 in `review-counting-1-3` (its findings 1 to 5, 7, 9 to 11, 17 and 19 to 22) and 2 in `review-problems-0.3-a` (its two `unclear` findings).

| Conceptual findings | Count |
|---|---|
| This audit only | 4 (0 wrong, 4 imprecise; 1 serious, 3 minor) |
| Earlier reads only | 16 (5 wrong, all fixed before this audit) |
| Both | 0 |

New `wrong` findings that no earlier read found: 0. The earlier reads' fixes all stand in the content as audited: I recomputed each one (for example `l12` `screens[8]` slip 1.0574, `l7` `screens[6]` slip 3, `homework-3` `items[3]` slip 7, `l10` `screens[7]` option b) and each is a `correct` row in the ledger.

The earlier review's class "the line names a slip that does not give the value" (its findings 2, 4, 5, 9 and 11) is the same class as findings 1 and 4 here, in different places. That is five and four instances across two reads, so by SESSION PROTOCOL 6 it is due a script: the concepts script's pattern (recompute each slip from the mistake its line names) could become a number-script convention for `wrong[]` values.

## Inbox

No engine limit met; nothing added to `docs/BACKLOG-INBOX.md`.
