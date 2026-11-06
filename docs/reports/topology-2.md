# topology level 2 (Topological spaces): report

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l5-topologies.json` | 12 screens | 3 |
| `l6-bases-and-subspaces.json` | 11 screens | 3 |
| `l7-homeomorphisms.json` | 11 screens | 3 |
| `l8-connectedness.json` | 12 screens | 3 |
| `review-2.json` | 9 items (difficulty 2 to 4, `pass` 0.8, every lesson, one recalling level 1's preimage test) | |
| `homework-2.json` | 8 items (difficulty 3 to 5, three at 5) | |

The performance task (the verb rule matches "Prove" in l7 and l8) is `h2-ivt-proof`, a `derivation` longform: images of connected spaces, connected subsets of $\mathbb{R}$, then the intermediate value theorem (rubric 2, 2, 3, 3).

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; the only level 2 warnings are "a problem screen without a canvas before the ladder ends" on proof-only `order` ladders.
2. Voice scan of the whole course folder: 0 sentences over 20 words, 0 explanations over three sentences.
3. `python3 docs/reports/topology-L2-numbers.py`: exits 0, 141 of 141 checks; every "check by hand" byKey line was read and names its slip correctly.
4. Playthrough with `--local-cdn`: all six files pass at desktop, with `--mobile` and with `--tablet`. Screenshots at 440 px were read for the l5 Hasse diagram and the union-intersection grid, the l6 simplex, the l7 letters and the l8 return line.

## Finite topologies on screen

- Hasse diagrams on `graph`: each set a `pill` node, rows by size (at most three a row: ∅; singletons; pairs; X), undirected edges for covering inclusions, non-members `dashed`. At 440 px the frame narrows and the labels `{a,b}` stay legible.
- The union and intersection table on `grid`: a 4 by 4 `cells` array of two-line plain text (`∪ X` over `∩ b`); the learner taps the two cells whose intersection is missing. Cells read clearly at 440 px.
- The 16 subsets of $\{a, b, c, d\}$ (l6 hook) on a 4 by 4 grid, the pieces pre-shaded, with a live tap count.

## Proof steps and their widgets

- l5: metric spaces are Hausdorff: `order` with a "radius $d(x, y)$" distractor; Sierpiński has no metric and the cofinite topology: `choice`.
- l6: subbasis topology: `multi`; open subspace theorem: `order` with a dropped-hypothesis distractor; finite subspace: `multi`.
- l7: $(-1, 1) \cong \mathbb{R}$: `order` with a `same` pair and the "continuous bijection is enough" distractor; the inverse by `choice` (an `expression` cannot see the absolute value) and `numeric` $g(-3)$; $[0, 1) \not\cong (0, 1)$: `order`.
- l8: $[a, b]$ connected: `order` with the "largest point of $U$" distractor; images of connected spaces: `order`; intervals: `choice`; the intermediate value theorem: `order` of four lines.
- homework: a union of connected sets with a common point: `order` with a distractor; the theorem chain as the `longform`.

## Numbers and sources

All are recomputed in `docs/reports/topology-L2-numbers.py`.

- Topology counts 1, 1, 4, 29, 355 (0 to 4 points): brute force over families and a count of preorders agree.
- Homeomorphism classes 1, 1, 3, 9 and connected counts 1, 1, 3, 19: by relabelling topologies and by relabelling preorders; connectedness by clopen sets and by the symmetric closure of the preorder.
- The 9 generated sets: unions of pieces, and again by minimal neighbourhoods; the subbasis topology and the Sierpiński subspace by direct computation; the basis $\{\{a\}, \{a, b\}, \{a, c\}\}$ gives 5.
- $\tfrac{1}{\sqrt6} \approx 0.4082$: distance to the edge midpoint and the inradius of a triangle of side $\sqrt2$; the corner distance 0.8165.
- Radial map: $(1, 1) \mapsto 0.7071$, $(1, 0.5) \mapsto (0.8944, 0.4472)$, $(0.5, 0.25) \mapsto (0.4472, 0.2236)$ by two formulas; the homework preimage $(0.75, 1)$ of $(0.6, 0.8)$.
- $f(0.5) = 1$, $f(0.75) = 3$, $f(-0.9) = -9$, $g(\pm 3) = \pm 0.75$, $f(-0.75) = -3$: formula and bisection.
- Letter piece counts 3, 4, 3: arms at each junction counted from the segment list.
- The trap's points $t_n = 2\pi - \tfrac1n$ on the circle checked against the canvas coordinates.
- $\operatorname{artanh} 0.5 \approx 0.5493$, $\operatorname{artanh}(-0.9) \approx -1.4722$, $\tanh 1 \approx 0.7616$: library and log formula.
- 7% from $(0.4, 0, 0.6)$ and $(0, \tfrac23, \tfrac13)$; the weight 0.6 by formula and bisection.
- Exactly 1 bijection carries $\{\varnothing, a, ab, X\}$ onto $\{\varnothing, b, bc, X\}$ (all six tried).

## Other notes

- Level 1 was written in this session; its notation, the $d_p$ balls and the preimage test are reused. `proof` l9 and `analysis` l16 exist and are cited by id.
- Code screens: `is_topology`/`count_topologies` (11 tests), `generate`/`is_basis`/`subspace` (10), `is_continuous`/`are_homeomorphic` (10), `is_connected`/`components` (8) and homework `count_connected` (4). Each prelude holds `norm` and a builder `T('', 'a', 'ab')`. Hidden tests stop at three points; four-point counts are stated in prose. The number script runs each solution (passes) and starter (fails) in CPython; the playthrough runs them in Pyodide.
- Pyodide first load, as measured for level 1: 1.7 s cold start from disk plus the download; each `how` says about 4 s.
- The l7 letters screen asks for the piece count by `numeric`; the junctions are labelled rather than tapped, since one tap target per letter added nothing.
- No `course.json` change proposed. Backlog: 3 bullets under "Raised later (topology level 2)".
