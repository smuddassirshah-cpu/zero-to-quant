# Delta read: fix passes of problems 1.3 a and b

Scope: only what the two fix passes changed, read at commit bf1b940. `changed.py` confirms no file of the nine has changed since its fix pass.

- Fix pass a (460a4a2): `limits/problems-2` and `-3`, `integrals/problems-1`, `-2` and `-3`. Nine items, 20 parts. Record: `review-problems-1.3-a.md`, "Fix pass".
- Fix pass b (ebbc857): `taylor/problems-1` and `-3`, `multivar/problems-2` and `-3`. Eight items, 21 parts. Record: `review-problems-1.3-b.md`, "Fix pass".

Method. Each of the 17 changed items was read whole as it now stands. The four re-authored items (`p-falling-parabola`, `p-relative-strength`, `p-cube-root-27`, `p-min-variance-pair`) were solved from the text before the key was read. Every changed answer, band and `wrong` value was then recomputed twice in `recompute.py`: exactly (sympy, fractions) and by a second route (the Riemann sums by a loop, slopes by a central difference, the turnover and tail integrals by quadrature, a root-finder for the times and sizes, a second difference for $f''$, a 30-digit value for the fourth root and the logs, the geometric tail by its own series, the variance by a fitted parabola and a grid search, the budget of 1.02 by the Lagrange system solved in the budget and by a grid). The same script checks, on all 113 numeric parts of the nine files, that no `wrong` value sits in the answer band, that no two bands meet and that every `wrong` id has its `byKey` line. `grade.mjs` runs the engine's own graders (`grade.js` with the local Compute Engine, the `%` field as `numeric.js` reads it) on every answer, `accept` form and `wrong` entry of the 17 items and on 226 typed strings: the value each feedback and explanation prints, the sensible roundings in the stated form, each slip as a learner would type it, the old keys, and the slips unscaled. `fresh.py` searches each course and every exam for the four new setups. Authors' scripts, the validator, the voice scan, `fresh-check` and the playthrough were run.

Scripts: `docs/reviews/delta-problems-1.3-ab-scripts/`, run from the repo root: `changed.py`; `recompute.py` (scratchpad venv Python); `grade.mjs --local-cdn <pkgs>`; `fresh.py`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = a statement reads two ways; `minor` = otherwise.

## Tool results

- `recompute.py`: 1,275 checks, 0 failures; 6 FINDING rows (findings 1, 3 and 4).
- `grade.mjs`: 675 checks, 0 failures; 8 FINDING rows (finding 1). Every printed value and sensible rounding is accepted, every slip is given its own key, every old key is refused.
- `problems-limits-numbers.py` 1,253 checks, `problems-integrals-numbers.py` 1,064, `problems-taylor-numbers.py` 937, `problems-multivar-numbers.py` 727: 0 failures each.
- `node tools/validate.mjs`: 0 errors. On the nine files: the five `[wrong-band]` warnings the fixer reported, nothing else.
- `voice-scan.py 35` on the four courses: 0 and 0. `fresh-check.mjs --file` on the four sets with a new item: 0 hits each.
- `playthrough --problems` on all nine sets, with and without `--mobile`: all passed.
- No changed answer, band or `wrong` value is wrong. No two bands meet.

## Findings: fix pass a (limits, integrals)

1. `minor` | `integrals/problems-2.json`, `problems-3.json` | three `accept` lines of the widened bands.
   Each line prints a band about the rounded figure, while the engine's band sits about the unrounded key. So one printed end is refused: `p-turnover-decay` part 3 "$13.83 \pm 0.01$" (13.82 refused; band 13.825 to 13.845), `p-log-return` part 1 "$-0.0719 \pm 0.0001$" ($-0.0718$ refused), `p-signal-average` part 4 "$2.967 \pm 0.001$" (2.966 refused). No working I could build lands on those three values, so no learner is marked wrongly; the line is only looser than the band. The five lines of review finding 6 ("accepted as $2.77 \pm 0.005$" and the like) have the same shape, but their refused ends have more places than the part asks for.
   Fix (the form fix pass b used): "$13.83$ (13.84 is accepted too)", "$-0.0719$ ($-0.0720$ is accepted too)", "$2.967$ (2.968 is accepted too)". No edit to the five.

2. `minor` | `integrals/problems-1.json` | `p-falling-parabola` | part 4, freshness.
   The new curve $12 - 3x^2$ appears nowhere else, and the item no longer copies `h-derive-falling-area`. The interval the reader proposed, $[0, 2]$, is that of `homework-1` item `h-square-02`: "$f(x) = x^2$ on $[0, 2]$ with $n$ strips. Then $\Delta x = \tfrac2n$ and the right ends are $x_k = \tfrac{2k}{n}$. Use $1^2 + \dots + n^2 = \dots$". Part 4 opens with the same line, and its answer is 24 minus three times the homework's $\tfrac{4(n+1)(2n+1)}{3n^2}$. `fresh-check` does not see it.
   Ruling proposed: stands, no edit. One step is shared, and any right sum of a square on $[0, b]$ shares it; the falling shape, $R_4$, the gap rule, the count of strips and the limit are not in that homework item. For the main session to confirm.

## Findings: fix pass b (taylor, multivar)

3. `wrong` | `taylor/problems-1.json` | `p-cube-root-27` | part 3, `feedback.generic`.
   "Not quite. Find $f''(27)$, then take half of it times $h^2$." The line survives from the cube root about 27. The item is now the fourth root about 16, and 27 appears nowhere else in it. A learner who misses and follows the line gets $\tfrac12 f''(27)\,h^2 \approx -0.00003$, refused again. Every other string of the item was changed; the author's script and the playthrough do not read generic lines.
   Fix: "Not quite. Find $f''(16)$, then take half of it times $h^2$."

4. `minor` | `multivar/problems-3.json` | `p-min-variance-pair` | part 5, two printed figures.
   The part asks for 5 places and keys 0.05824. The explanation ends "to 0.0582", one place short of the answer. The `correct` line says scaling the weights "gives $0.056 \times 1.0404 \approx 0.0583$ too", beside 0.05824: at the 4 places printed the two differ. The exact value is 0.0582624. Both are accepted, so nothing is marked wrongly.
   Fix: `explain` "... by about $0.112 \times 0.02 = 0.00224$ to 0.05824. Placing 2% more money scales the risk up." `correct`, second sentence: "Scaling both weights by 1.02 gives the exact value, $0.056 \times 1.0404 \approx 0.05826$."

5. `minor` | `multivar/problems-3.json` | `p-min-variance-pair` | freshness.
   The pair 40%, 25% is new, and no computed number of the item appears in the course or its exams. The correlation, 0.3, is lesson l12's own ("Asset A has volatility 20% and asset B 10%. Their returns have correlation 0.3", screens 1, 2, 3 and 8, the summary and quiz 3), and the prose opens in the lesson's words. The mock `mock-oa-quant-data` also has 25%, 20% and 0.3. The review's "a pair the course and its exams do not use" holds for the pair, not for the correlation.
   Ruling proposed: stands, no edit. 0.3 is what makes $w = 0.2$ exact (0.2 and 0.5 give $w = 0.2329$ and 0.1020), and the brief's test is setup, numbers or story: the volatilities, the quadratic, the weight, $\lambda$ and the budget step are all new.

## The five `[wrong-band]` warnings

- Four are false alarms: the `unscaled` entries of `p-two-months` parts 2, 4 and 5 and `p-tail-bound` part 4. The rule reads "to 1 decimal place" as the rounding of the slip, but that rounding is in units of $10^{-5}$ or $10^{-4}$ and the slip is the value in plain units. Each band takes the slip as typed to 2, 3 or 4 figures (0.00017, 0.000171, 0.0001707; 0.000049, 0.0000486; 0.00022, 0.000219; 0.00116, 0.0011594) and refuses every other slip of its part unscaled (`grade.mjs`, `recompute.py`). The inbox bullet stands.
- `p-loss-limit` part 3 `one-lot` (0.0354, band 0.005) is a true hit by the letter and harmless. The part asks for the nearest pound, and the slip rounded so is 0, which the old band of 0.5 took and the new one does not. A typed 0 now gets the generic line, "Multiply the slope by $\Delta y = 0.0001$, then by the 40,000 lots", which is the cure. A band wide enough for 0 would also take 0.0096, the price slip on one lot, and tell it something untrue. No edit.

## Verified clean

- Each original finding was really fixed: a 1 to 8, 10 and 11; b 1 to 9 and 11, bar the one line of finding 3 above. Findings a 9 and b 10 were no-edit rulings; a 12 and b 12 are in `docs/BACKLOG-INBOX.md`.
- `p-perpetuity-slope` part 2: the 4-place route gives $-2041$ and the penny route $-2040$; both are accepted, $-2042$ and $-2039$ are not, and 2040, 2041 and 2.04 go to `sign` and `no-divide`.
- `p-relative-strength`: $P'(0) = 2.1$, $I'(0) = 75$, top $3150 - 2250 = 900$, $R'(0) = 0.0004$, growth 2%. In the `%` field, 2 and 2% are accepted, 0.02 is given `decimal`, 0.04 `raw`, 12 `added`, 7 `share-only`. Fresh: no formula, rate pair or number of it elsewhere in limits or the exams (l9's quiz has a price to earnings ratio with straight-line rates, a different question).
- `p-falling-parabola`: heights 11.25, 9, 5.25, 0; $R_4 = 12.75$, $L_4 = 18.75$, gap 6, $n = 240$, $R_n = 16 - \tfrac{12}{n} - \tfrac{4}{n^2}$ (symbolic sum and loops at $n = 1, 4, 10, 240$), area 16 by limit, antiderivative and quadrature. The engine takes four other forms of $R_n$, gives $L_n$, the `once` form and the no-width form their keys, and refuses the old key.
- `p-cube-root-27`: slope $\tfrac{1}{32}$, $L(16.32) = 2.01$, $f''(16) = -\tfrac{3}{2048}$, error exactly $-0.000075$, corrected 2.009925; the true value is 2.0099259, so "2.009926 to 6 places" and "within 0.000001" are both true. The stale id does not matter to a learner: no screen prints an item id, and progress for a problem set is stored under the set (`course/problems-n`, `state.js`). The author's report records the kept id. Fresh: no fourth root, $x^{1/4}$ or base point 16 in taylor.
- `p-min-variance-pair`: $0.1625w^2 - 0.065w + 0.0625$, $w = 0.2$, variance 0.056, $\sigma_p = 0.2366$, $\lambda = 0.112$ from both partials and from the Lagrange system, estimate 0.05824 against the exact 0.0582624. Part 4 now reads "treat both weights as free".
- `p-two-months` part 5 reads true as a whole: the question asks for the bound from the sizes alone, the key is their sum, and the explanation gives the true total error, $11.8 \times 10^{-5}$, with the signs $+16.10$ and $-4.33$ (30-digit logs). Parts 2 and 4 state only true errors.
- `p-newton-cubic` part 3 reads true: $x_0 = 1 < 1.2134 < x_2 < x_1 = 1.25$; the tangent at each point lies under the curve; on a grid no step from the right crosses the root and every step from the left does.
- Bands: `p-tail-bound` part 4 takes 11.59, 11.60 and 11.598 and refuses the true error 11.58; `p-two-months` part 4 takes 4.85, 4.854 and 4.86; `p-turnover-decay` part 3 takes 13.83, 13.84 and 13.8352; `p-log-return` part 1 takes $-0.0719$, $-0.0720$ and $-0.07195$; `p-signal-average` part 4 takes 2.967, 2.968 and 2.9676.
- Printed terms: 338.6340 and the sum 354.4349; 2.468107 and the sum 5.10281.
- Wording only: `p-inventory-penalty` parts 1 and 2, `p-two-book-risk` part 5, the five `accept` lines of a 6.

## Counts

| tag | fix pass a | fix pass b | total |
|---|---|---|---|
| `wrong` | 0 | 1 | 1 |
| `unclear` | 0 | 0 | 0 |
| `minor` | 2 | 2 | 4 |

Findings 1, 3 and 4 are text edits with no graded value changed; a fix pass on Sonnet covers them without a further delta read. Findings 2 and 5 need a ruling, and both are proposed to stand.
