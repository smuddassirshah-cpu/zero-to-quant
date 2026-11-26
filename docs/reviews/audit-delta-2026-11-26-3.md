# Delta concept audit, 26 Nov 2026, batch 3

Blind audit of the content changed in eleven closed courses between each course's close and `e69cac72`. Scope list: 38 files in `delta-batch3.tsv` (algo-think, coding-int, conditional, ds, ito, limits-thm, mental-pressure, numerics, pdes, random-vars, research-int). Eleven courses in one batch exceeds the eight-course cap, by agreement: four of them total 14 changed lines.

Ledger: `docs/reports/audit-delta-2026-11-26-3-ledger.md` (131 rows). Script: `docs/reports/audit-delta-2026-11-26-3-concepts.py` (342 checks, exit 0, two notes that match findings 2 and 3).

## What changed

- 43 new numeric slips with feedback: 34 `sign` (the key with its minus dropped), 8 `decimal` (a per cent or %² key typed as a decimal) and one `exact-rounded`. The script confirms each value is what the named mistake gives, and that no new band meets the key's band or another slip's band.
- One new longform, `pdes/homework-1` `h-derive-lazy-walk` (prompt, eight-step model, four rubric rows).
- `conditional/l3-shrinking`: six new per-cell feedback lines, the filter experiment moved from `bars` to the `dice-sim` canvas with a "total 10" event, one reworded explain, one new caption.
- Six one-line rewordings: algo-think (2), ds (1), limits-thm (1), and lesson ids replaced by lesson names in coding-int (3).

## Findings

No `wrong` and no `misleading` finding. Three `imprecise`, all `minor`.

1. `conditional/l3-shrinking.json` | `screens[6].explain.text` | imprecise, minor | "settle near $\tfrac{1}{11}$, the shrunk space" names a number as the space. The shrunk space is the 11 kept outcomes; $\tfrac{1}{11}$ is the chance of a total of 10 inside it. | Enumeration: 11 of 36 outcomes hold a 5, one of them totals 10. The canvas itself is right: seed 4226 keeps 308 of 1,000 rolls, 28 with total 10, and $28/308 = \tfrac{1}{11}$. | Replace the last sentence with: "Roll 1,000 and watch the share of total 10 among kept rolls settle near $\\tfrac{1}{11}$, its chance in the shrunk space."

2. `ito/l5-integrating-noise.json` | `screens[0].feedback.byKey.sign` | imprecise, minor | "The products 0, 0.2675, −0.2745 and −0.1782 add to −0.1853". The four numbers shown add to −0.1852. The key −0.1853 is the unrounded sum, which the `accept` line and the explain on the same screen both say in brackets; the new line drops that. | $0.2675 - 0.2745 - 0.1782 = -0.1852$; the path to full precision gives $-0.18527$. Both sit inside the key's band, so no grade changes. | Replace with: "The products 0, 0.2675, −0.2745 and −0.1782 add to about −0.185, because the losses outweigh the one gain. A positive 0.1853 books the net loss as a gain."

3. `research-int/homework-1.json` | `items[0].parts[0].feedback.byKey.sign`, `items[0].parts[1].feedback.byKey.sign`; `research-int/l2-correlation-limits.json` | `screens[5].feedback.byKey.sign` | imprecise, minor | The three new lines call 0.64, 0.5724 and 0.75 "the width". Each is the half-width $\sqrt{(1 - a^2)(1 - b^2)}$; the range is twice as wide. Every older line of the same items (hint, generic, `product`) says "half-width". | For $a = b = 0.6$ the range is $[-0.28, 1]$, width 1.28. The script confirms each floor is the edge of positive semi-definiteness. | In each line replace "the width" by "the half-width": "The centre is 0.36 and the half-width 0.64, so ..."; "The half-width 0.5724 is bigger than the centre 0.24, so ..."; "The centre is 0.25 and the half-width 0.75, so ...".

## Checked and found right (the changes that carried risk)

- `pdes/homework-1` `h-derive-lazy-walk`: the update, both Taylor remainders, $c = (p - q)\Delta x/\Delta t$, $D = (1 - r)\Delta x^2/(2\Delta t)$, the scaling ($\Delta t \sim \Delta x^2$, $p - q \sim \Delta x$), the remainder bounds $\tfrac12\Delta t\max|u_{tt}|$ and $\tfrac13 D\Delta x\max|u_{xxx}|$, and the remark that the true space remainder is of order $\Delta x^2$. Numbers: $D = 1$, $c = 2.5$, walk mean 2.5 and variance 1.975, gap $c^2\Delta t\,t = 0.025$. The script gets the moments three ways (formula, iterating the stated update, 40,000 simulated walks), checks that $N(ct, 2Dt)$ solves $u_t + c\,u_x = D\,u_{xx}$, and sees the update's residual fall fourfold when $\Delta x$ halves.
- `numerics/l12-stiff-equations`: exact 5.2253%, Euler 8.2393% at $h = 0.04$ and 5.2222% at $h = 0.02$, all recomputed. The tightened band (0.00002) now keeps 5.2253%, 5.23% and 5.2222% apart.
- `algo-think/l9-halving` test 12: the three-comparison search returns −1 in 20 passes with exactly 50 reads; the one-read search uses 20.
- `ds/l4-frequencies`: the `.count` loop passes (`ab`, `abc`), and is right on every equal-length pair tried, so "without a length check" is the true condition.
- `limits-thm/l19`: the Cauchy density decays like $1/x^2$ (its tail like $1/x$), so "density" corrects the old "tails".
- `ito/l9-bs-pde`: the put's $V$, $\Delta$, $\Gamma$ and $\Theta = -1.6579$ recomputed from Black–Scholes two ways.
- `conditional/l3` canvas: the event share is exactly $\tfrac{1}{11}$; at seed 4226 the 1,000-roll count (308) lies inside the accepted 280 to 330.

## Observation, not a concept finding

`pdes/homework-1` `h-derive-lazy-walk`: the prompt asks for a derivation "from a blank page", and its optional line then prints the update and the reason for it in full. That line is the 1-point optional rubric row, so no required mark is given away, but the first step of the derivation is on the page. If that is not intended, the optional line could read: "Optional, one more point: write the update for $u(x, t + \Delta t)$ and say why each term is there."

## Counts per course

| course | files | ledger rows | wrong | imprecise | misleading | findings serious | findings minor |
|---|---|---|---|---|---|---|---|
| algo-think | 2 | 4 | 0 | 0 | 0 | 0 | 0 |
| coding-int | 2 | 3 | 0 | 0 | 0 | 0 | 0 |
| conditional | 1 | 12 | 0 | 1 | 0 | 0 | 1 |
| ds | 1 | 2 | 0 | 0 | 0 | 0 | 0 |
| ito | 4 | 12 | 0 | 1 | 0 | 0 | 1 |
| limits-thm | 1 | 2 | 0 | 0 | 0 | 0 | 0 |
| mental-pressure | 5 | 16 | 0 | 0 | 0 | 0 | 0 |
| numerics | 5 | 11 | 0 | 0 | 0 | 0 | 0 |
| pdes | 5 | 35 | 0 | 0 | 0 | 0 | 0 |
| random-vars | 5 | 10 | 0 | 0 | 0 | 0 | 0 |
| research-int | 7 | 24 | 0 | 3 (one finding, three lines) | 0 | 0 | 1 |
| total | 38 | 131 | 0 | 5 rows, 3 findings | 0 | 0 | 3 |

Verdicts over the 131 rows: 126 correct, 5 imprecise, 0 wrong, 0 misleading, 0 unverified.

By the convergence rule every course stays within "at most one new `wrong` per three levels": no course has a `wrong`.

## Overlap table

OVERLAP_PLACEHOLDER

## Runs

- Validator: `node tools/validate.mjs`, 0 errors (4,606 warnings, none new: no content edited).
- Concepts script: 342 checks, exit 0.
- No playthrough: content unchanged.
