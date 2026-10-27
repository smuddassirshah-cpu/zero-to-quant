# Topic 0.3 exam: precalculus

File: `app/content/exams/topic-0.3.json` (id `topic-0.3`, 90 minutes, pass 0.7). Minutes follow `examMinutes` in `learn.js`: topic 0.3 is 200 h, over 150 h, so 90.
Generator and checks: `scratchpad/exam-0.3-0.5/` (`gen03.py` builds the file and asserts every answer two ways, `common.py`, `lint.py` for the copy rules).

## Shape

25 items, interleaving the four courses (exp-log, trig, series, counting).

| Difficulty | Items | Share | Ramp |
|---|---|---|---|
| 2 | 5 | 20% | 20% |
| 3 | 13 | 52% | 50% |
| 4 | 5 | 20% | 20% |
| 5 | 2 | 8% | 10% |

Widgets: 21 numeric, 3 choice, 1 multi. Canvases: plane (triangle), plane (wave), vectors.

| # | id | d | skills | widget / canvas | answer |
|---|---|---|---|---|---|
| 1 | e-log-thousandth | 2 | ex-logs | numeric | −3 |
| 2 | e-ticket-count | 2 | ct-product | numeric | 30 |
| 3 | e-arc-length | 2 | tr-circle | numeric | 10 cm |
| 4 | e-geom-eighth | 2 | seq-geom | numeric | 896 |
| 5 | e-four-falls | 2 | ex-growth | choice | $0.97^4$ |
| 6 | e-fraction-powers | 3 | ex-laws | numeric | 4.5 |
| 7 | e-weekly-savings | 3 | seq-arith, seq-sums | numeric | £2,775 |
| 8 | e-cosine-rule | 3 | tr-triangles | numeric, plane triangle | 7 km |
| 9 | e-years-to-target | 3 | ex-solve | numeric | 9 years |
| 10 | e-continuous-four | 3 | ex-e | numeric | £2,442.81 |
| 11 | e-wave-fit | 3 | tr-graphs | choice, plane graph | $3\sin(\pi x/6) + 5$ |
| 12 | e-sigma-odd | 3 | seq-sums | numeric | 216 |
| 13 | e-desk-block | 3 | ct-perm | numeric | 240 |
| 14 | e-double-angle-solve | 3 | tr-equations, tr-graphs | multi | 30°, 150°, 210°, 330° |
| 15 | e-binomial-cube | 3 | seq-binomial | numeric | −160 |
| 16 | e-tech-pick | 3 | ct-comb | numeric | 0.3 |
| 17 | e-log-returns | 3 | ex-logs, ex-laws | numeric | −0.0198 |
| 18 | e-two-u-minus-v | 3 | vc-arrows | numeric | 7.21 |
| 19 | e-tan-third-quadrant | 4 | tr-identities, tr-circle | numeric | 1.875 |
| 20 | e-log-quotient | 4 | ex-logs, ex-laws, ex-solve | numeric | 0.75 |
| 21 | e-perpetuity-now | 4 | seq-converge, seq-geom | numeric | £1,560 |
| 22 | e-vector-ratio | 4 | vc-geometry | choice, vectors | $\tfrac23\mathbf{a} + \tfrac13\mathbf{b}$ |
| 23 | e-code-repeat | 4 | ct-product, ct-perm | numeric | 21,856 |
| 24 | e-accounts-meet | 5 | ex-e, ex-solve, ex-growth | numeric | 9.12 years |
| 25 | e-loan-payment | 5 | seq-geom, seq-sums | numeric | £1,295.05 |

Skills: all 20 of the topic are covered (the `skills` map is the union of the four course.json files): ex-growth 2, ex-laws 3, ex-logs 3, ex-e 2, ex-solve 3, tr-triangles 1, tr-circle 2, tr-graphs 2, tr-identities 1, tr-equations 1, seq-arith 1, seq-geom 3, seq-sums 3, seq-binomial 1, seq-converge 1, ct-product 2, ct-perm 2, ct-comb 1, vc-arrows 1, vc-geometry 1.

Every numeric item names its misconceptions as `wrong[]` entries with a `byKey` line (for example 8 years from rounding 8.07 down, £2,431.01 from yearly compounding, $\sqrt{89}$ from Pythagoras, −0.02 from not undoing the log, 1.85 from subtracting lengths). Items that need a calculator say so in the prose; the others say "Work without a calculator."

Fresh against the courses: each item's key expression was searched in the four courses and the Stage 0 precalculus paper. Five first drafts matched lesson items and were replaced: $\sin 2x = 0.5$ (trig l11) became $\cos 2x = \tfrac12$; 3, 6, 12, 24 (series l1, l3) became 7, 14, 28, 56; the PIN complement (counting l7) became 4-character hex codes; Ana and Ben (counting l6) became Priya and Tom; $\cos\theta = -\tfrac{5}{13}$ became $-\tfrac{8}{17}$.

## Numbers computed twice

All in `gen03.py`, which fails if any pair disagrees: the log by `math.log10`; the geometric term by iteration against $7 \times 2^7$; tickets, block seatings (240), tech picks (36 of 120) and hex codes (21,856) by brute-force enumeration against the formula; the years by a loop against $\lfloor \ln 1.6 / \ln 1.06 \rfloor + 1$ (balances £7,969.24 and £8,447.39); $2000e^{0.2}$ by its power series; the log returns by a product of $e^{r}$; the cosine rule by coordinates; the wave's peaks, troughs and period by evaluation; $\tan\theta$ from $\theta = 180^\circ + \arccos\tfrac{8}{17}$; the $\cos 2x$ solutions by a scan of whole degrees; the savings and sigma sums by direct addition (and $15^2 - 9$); the binomial coefficient by polynomial multiplication; $|2\mathbf{u} - \mathbf{v}|$ by `hypot`; the log equation by substitution; the perpetuity by a 3,000-term sum; X by section formula and by distances (ratio 0.5); the meeting time by bisection (accounts both £1,577.44); the loan payment by running the balance to zero over 10 years.

## Validation and playthrough

- `node tools/validate.mjs`: 0 errors, no warning for this file; the manifest lists `exams/topic-0.3.json`.
- Copy lint (`lint.py`): no `!`, no em or en dash, no sentence of 20 words or more, no American spellings; every explanation and feedback line at most three sentences.
- `playthrough.mjs --exam topic-0.3 --local-cdn <pkgs>`: 25 of 25, passed, desktop and `--mobile`.
- Screenshots reviewed (`scratchpad/exam-0.3-0.5/shots03`). Fixes made from them: the triangle's labels moved off its sides and the canvas capped at 260 px; the vectors figure's AB segment moved into `state` (in `params` it was not drawn) and its range tightened so it fills a phone column.

## Engine notes

See `docs/BACKLOG-INBOX.md`, "Raised later (exams topic-0.3, topic-0.4 and topic-0.5)": the start card's lede has no article, and the `--why` result capture is blank below the header.
