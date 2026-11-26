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

Filled after the ledger and findings were committed (`7a9c5d50`). Earlier reads opened: the `audit-<course>-*` files of the eleven courses, `review-perf-retrofit-2.md` (the lazy walk's second read), `review-delta-ag-pdes.md` and `review-problems-pdes-1-3.md`.

| course | this audit only | earlier read only | both |
|---|---|---|---|
| conditional | 1 | 0 | 0 |
| ito | 1 | 0 | 0 |
| research-int | 1 | 0 | 0 |
| the other eight | 0 | 0 | 0 |
| total | 3 | 0 | 0 |

All three findings sit on strings added after the courses closed, so no earlier read could have met them. Nothing an earlier read raised on the changed strings is still open:

- `algo-think/l9` `test-12`: `audit-algo-think-1-3-r3` row 13 called the old line imprecise (a miss takes 19 or 20 passes; the `<`, `>`, `==` order reads less). The new line says "this miss" and names the `==`, `<`, `>` order. Read blind, it is correct.
- `ds/l4` loop `why`: the new text is the paste-ready fix of `audit-ds-1-3-r2`. Read blind, correct.
- `limits-thm/l19` Cauchy line: the new text is the fix quoted in `audit-limits-thm-4-r2`. Read blind, correct.
- `pdes/homework-1` `h-derive-lazy-walk`: `review-perf-retrofit-2` raised PD1-1 and PD1-2 (both "could"), and both are in the text audited here (the "sharper $\Delta x^2$" clause, the "first dropped term" route). It found no error in the derivation; neither did this audit.

No inbox bullet: no engine or canvas limit met.

## Runs

- Validator: `node tools/validate.mjs`, 0 errors (4,606 warnings, none new: no content edited).
- Concepts script: 342 checks, exit 0.
- No playthrough: content unchanged.

## Fix pass

Opus fixer, content commit `c7e51348`. No graded key, slip value, tolerance or hidden test changed.

1. `conditional/l3-shrinking` `screens[6].explain.text` | fixed differently | Enumerated myself: 11 of 36 outcomes hold a 5; of the totals of 10, (4, 6) and (6, 4) hold no 5, so only (5, 5) is kept, giving $\tfrac{1}{11}$. The last clause now says why instead of naming a number as the space: "settle near $\tfrac{1}{11}$: of the 11 kept outcomes, only (5, 5) totals 10."
2. `ito/l5-integrating-noise` `screens[0].feedback.byKey.sign` | fixed | From the table: $0.5561 \times 0.4810 = 0.26748$, $1.0371 \times (-0.2647) = -0.27452$, $0.7724 \times (-0.2307) = -0.17819$, sum $-0.18523$ (4 dp products: $-0.1852$), so "add to about −0.185" is right at either precision. The rest of the line is unchanged.
3. `research-int/homework-1` parts 0 and 1 `byKey.sign`, `l2-correlation-limits` `screens[5].feedback.byKey.sign` | fixed | $\det R \ge 0$ is $-c^2 + 2abc + 1 - a^2 - b^2 \ge 0$, whose roots are $ab \pm \sqrt{(1 - a^2)(1 - b^2)}$, so the root term is the half-width. "the width" is now "the half-width" in the three lines. Also changed, same screen and same error, not in the finding: `l2` `screens[5].prose` "the width comes from what is left" now reads "the half-width".

Observation, not edited: on `ito/l5` `screens[0]` the `accept` line writes "$0 + 0.2675 - 0.2745 - 0.1782$" beside $-0.1853$, and the explain implies the unrounded products give $-0.1853$. The products of the table's own 4 dp values sum to $-0.18523$, which rounds to $-0.1852$; $-0.1853$ needs the hidden full-precision path. Both lie inside the key's band, so no grade is affected.

Gates: validator 0 errors (4,606 warnings); voice scan 35 on conditional, ito and research-int, 0 over and 0 explanations over three sentences; concepts script exit 0 (its two notes are hard-coded and still print); number scripts `--only` conditional (4), ito (9), research-int (3) all pass; playthrough desktop and `--mobile` of `conditional/l3-shrinking`, `ito/l5-integrating-noise`, `research-int/l2-correlation-limits` and set `research-int/homework-1`, all passed.
