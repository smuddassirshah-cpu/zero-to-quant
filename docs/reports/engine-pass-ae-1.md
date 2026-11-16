# Engine pass AE part 1 (inbox, same-course shapes, number-scripts CI)

Three jobs, one commit each, on a worktree branch descended from `claude/elegant-ritchie-x1xs97`.

## 1. Inbox numbered (items 1028 to 1051)

The inbox held 54 bullets after the merge. The 17 from "problems analysis" to "review problems vector-calc" were already numbered in the backlog (974 to 1025) and were dropped. The other 37 (audit ds round 2, graphs-dp rounds 1 to 3, cpp rounds 1 to 3, algo-think rounds 2 and 3, contests session 12, limits-thm L4 round 2) became 24 items, 1028 to 1051, with their sources kept. The largest merges: 1028 (a `mutants` list for `test-N` lines, 6 bullets), 1031 (a `--code` mode for `grade-all.mjs`, 4), 1029 (slip value against feedback, 3). The backlog file also held its whole "Engine pass AD part 1" section twice (a merge artefact, 67 identical lines); the second copy was removed. The statuses of 972 and 973 (done in AD part 2) were corrected. The inbox is its heading and a one-line note. Last number: 1051.

## 2. Reuse shapes in same-course mode (item 993)

The tool that runs same-course mode is `app/tools/same-course-reuse.mjs` (called by `fresh-check.mjs --file` on a `problems-<n>.json`); the new code is `app/tools/reuse-shapes.mjs`, wired in through `unitsOfFile` (a `shapes` field per unit), `loadCorpus` (an index over every unit of the courses, exams and bank) and `scanSet`. The `static` CI step already runs `same-course-reuse.mjs --all`, so the new mode runs there with no workflow change; the new kinds are advisory (`warn`) and never fail it. New kinds:

| kind | what it sees | scope |
|---|---|---|
| function | a function with its interval (one sentence or an integral's bounds); a one-variable polynomial with its factorisation, letter renamed (the product is expanded); the heavy terms of a two-letter polynomial | interval and terms: whole app; polynomial: the course, and other courses only for a cubic or higher with three terms, not a quadratic with small whole roots, not $(x+a)^n$ |
| pair | two consecutive part keys that a sentence of another file of the course holds as its only two non-stock numbers | course |
| transform | a polynomial of degree 3 or more (three terms) equal to another after $x \to ax + b$ and a factor (depressed monic form), also as a denominator; a number set of four or more values equal to another under $x \to ax + b$ (an arithmetic progression is stock) | course |
| region | a corner set in a sentence naming a polygon or intercepts (a plane's intercepts projected on z = 0 with the origin); a circle with an integrand number; end points with a route | whole app |

Stock handling: variables limited to `x y z t s u v w` (other letters are parameters); a shape held by more than 4 files is dropped (`--shape-df`); corners inside the unit square, the common decimals (0.5, 0.05, 1.96 ...) and whole numbers up to 20 are not pair keys. `--no-shapes` turns the four kinds off.

Test: `app/tools/test-fresh-check-same-course-ae.mjs` (0.6 s; registered in the `static` job of `acceptance.yml`; `ci-coverage.mjs` passes). Fixtures `app/tools/fixtures/same-course-ae/content/`: the pre-fix items of the eight findings (rebuilt with `git show <fix commit>^`, the source items copied unchanged from HEAD) and four silent rulings. It also checks a number set under $x \to 2x + 16$ (hit), an arithmetic progression and an unrelated set (silent), the same chain inside one course (hit), the `fresh-check.mjs --file` line and `--no-shapes`.

| # | finding | kind caught |
|---|---|---|
| 1 | analysis `p-accumulated-cubic` against l18 (review-problems-analysis-4-5 finding 2) | function |
| 2 | analysis `p-diamond-ball` against l23, 0.7 then 0.3 (finding 3) | pair |
| 3 | analysis `p-root-sums` against integrals l2 and review-1, $\sqrt{x}$ on $[0, 4]$ (note A) | function |
| 4 | odes `p-test-rig` against l15 (review-problems-odes-4 finding 1) | transform |
| 5 | vector-calc `p-bead-semicircle` against review-1 `r4-clockwise` (review-problems-vector-calc-1-3 finding 1) | region |
| 6 | vector-calc `p-two-routes-cubic` against homework-1 `h1-two-paths` (finding 2) | region |
| 7 | vector-calc `p-cubic-potential` against multivar review-1 (finding 3) | function |
| 8 | vector-calc `p-triangle-flux` against multivar problems-5 and homework-3 (finding 4) | region |

Silent (zero hits of any kind): a single common fraction, a simple quadratic with small whole roots shared with another topic's factorising screen, a taught definition or basis, a two-state chain across two topics (eigen against markov; the same chain inside one course does fire). Not covered of the findings in the five reviews: the l15 sentence with its letters changed (linear-maps finding 1, a text hit under the 10-word line) and a story noun in a screen title (vector-calc finding 7). Both stay listed under item 993 as not done.

The first version of the rule gave 123 hits on the 116 sets (86 function, 31 pair), over the limit of 40. Tightened: parameter letters out, perfect squares and binomial powers out, other-course polynomials only for a cubic or higher, a pair sentence must hold exactly the two keys, a corner sentence must name a region, a transform needs three terms. Result: **28 hits** on the 116 existing sets (`node tools/same-course-reuse.mjs --all`, 19 s against 11 s before: the parsing). Verdicts are for the main session; no content edited, no waivers added.

| file | item | kind | source | evidence | verdict |
|---|---|---|---|---|---|
| analysis/problems-5.json | p-root-sums | function | integrals/l16-infinite-height.json:quiz[2] | \sqrt{x} on [0, 9] (a function with its interval) | to read |
| counting/problems-1.json | p-team-photo | pair | counting/l2-arranging.json:screens[8] | consecutive part keys 5040 and 720 sit together in "So $7! = 7 \times 720 = 5040$." | to read |
| counting/problems-1.json | p-team-photo | pair | counting/review-2.json:items[5] | consecutive part keys 5040 and 720 sit together in "The $7! = 5040$ rows give each round seating 7 times, so there are $\tfrac{5040}{7} = 6! =" | to read |
| integrals/problems-3.json | p-order-size-tail | transform | integrals/l9-undo-chain.json:quiz[2] | 3x^6 + 9x^4 + 9x^2 + 3 against x^6 + 3x^4 + 3x^2 + 1: the same polynomial shifted and scaled (equal after x -> a x + b, up to a factor) | to read |
| limits-thm/problems-2.json | p-quote-life | function | ito/review-4.json:items[5] | x^2 - 6x + 9 on [0, 3] (a function with its interval) | to read |
| markov/problems-4.json | p-regime-sampler | pair | markov/l13-balanced-flows.json:screens[2] | consecutive part keys 0.6 and 0.3 sit together in "Balance gives $0.3\pi_i = 0.5\pi_{i+1}$, so $\pi_{i+1} = \tfrac{0.3}{0.5}\pi_i = 0.6\pi_i$" | to read |
| markov/problems-4.json | p-regime-sampler | pair | markov/l2-transition-matrix.json:screens[3] | consecutive part keys 0.6 and 0.3 sit together in "Multiply pairwise and add: $0.6(0.1) + 0.3(0.3) + 0.1(0.3)$." | to read |
| markov/problems-4.json | p-regime-sampler | pair | markov/l7-how-long.json:screens[8] | consecutive part keys 0.6 and 0.3 sit together in "Each minute at the back, it stays with chance 0.6, moves up with 0.3, or is cancelled with" | to read |
| markov/problems-4.json | p-regime-sampler | pair | markov/l8-which-end.json:screens[8] | consecutive part keys 0.6 and 0.3 sit together in "At the back an order stays with 0.6, moves to the front with 0.3, or is cancelled with 0.1" | to read |
| markov/problems-4.json | p-regime-sampler | pair | markov/problems-2.json:items[1] | consecutive part keys 0.6 and 0.3 sit together in "$h = 0.3 + 0.5h$, so $h = \tfrac{0.3}{0.5} = 0.6$." | to read |
| multivar/problems-5.json | p-triangle-field | function | limits-thm/l17-smallest-and-largest.json:screens[6] | -x^4 + 3x^3 - 3x^2 + x (the same polynomial in another course) | to read |
| multivar/problems-5.json | p-triangle-field | region | vector-calc/homework-3.json:items[1] | corners (0, 0), (4, 0), (0, 2) | to read |
| quadratics/problems-4.json | p-storage-crate | function | quadratics/review-4.json:items[6] | x^3 + 4x^2 + x - 6 (the same polynomial, factorised or not, with the letter renamed) | to read |
| quadratics/problems-4.json | p-storage-crate | function | quadratics/l17-dividing-polynomials.json:screens[5] | x^3 - 7x - 6 (the same polynomial, factorised or not, with the letter renamed) | to read |
| quadratics/problems-4.json | p-storage-crate | function | quadratics/l1-two-brackets.json:screens[1] | x^2 + 5x + 6 (the same polynomial, factorised or not, with the letter renamed) | to read |
| quadratics/problems-4.json | p-storage-crate | function | quadratics/l15-fractions-with-letters.json:screens[1] | x^2 + 5x + 6 (the same polynomial, factorised or not, with the letter renamed) | to read |
| quadratics/problems-4.json | p-storage-crate | function | quadratics/l3-leading-coefficient.json:screens[5] | x^2 + 5x + 6 (the same polynomial, factorised or not, with the letter renamed) | to read |
| quadratics/problems-4.json | p-storage-crate | function | quadratics/l5-product-of-zero.json:screens[3] | x^2 + 5x + 6 (the same polynomial, factorised or not, with the letter renamed) | to read |
| regression/problems-3.json | p-power-price | pair | regression/homework-1.json:items[7] | consecutive part keys 0.3 and 0.6 sit together in "The slopes also give $r^2 = 2 \times 0.3 = 0.6$." | to read |
| regression/problems-3.json | p-power-price | pair | regression/review-3.json:items[0] | consecutive part keys 0.3 and 0.6 sit together in "β₁ + β₂δ is 0.5 + 2 × (−0.3), which is 0.5 − 0.6." | to read |
| taylor/problems-3.json | p-tail-bound | function | taylor/l7-standard-series.json:screens[9] | 0.166667x^3 + 0.5x^2 + x + 1 (the same polynomial, factorised or not, with the letter renamed) | to read |
| taylor/problems-3.json | p-tail-bound | function | exams/topic-1.3.json:items[10] | 0.166667x^3 + 0.5x^2 + x + 1 (the same polynomial in another course) | to read |
| taylor/problems-3.json | p-big-gain | function | taylor/l7-standard-series.json:screens[5] | -0.25x^4 + 0.333333x^3 - 0.5x^2 + x (the same polynomial, factorised or not, with the letter renamed) | to read |
| trig/problems-2.json | p-two-buoys | pair | trig/l9-stretching-a-wave.json:screens[4] | consecutive part keys 2.5 and 5.5 sit together in "So $y$ runs from 2.5 to 5.5." | to read |
| vector-calc/problems-2.json | p-cycloid-arch | function | vector-calc/l12-stokes.json:screens[5] | \cos^2x on [0, 2pi] (a function with its interval) | to read |
| vector-calc/problems-2.json | p-cycloid-arch | function | vector-calc/l3-work-done.json:quiz[2] | \cos^2x on [0, 2pi] (a function with its interval) | to read |
| vector-calc/problems-3.json | p-can-curl | function | vector-calc/l10-surface-integrals.json:screens[8] | x^2 + y^2 on [0, 2] (a function with its interval) | to read |
| vector-calc/problems-3.json | p-can-curl | function | vector-calc/review-3.json:items[2] | x^2 + y^2 on [0, 2] (a function with its interval) | to read |
