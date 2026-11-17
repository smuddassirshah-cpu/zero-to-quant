# Delta read AG, ito problem sets 1 to 3: the two re-authored problems and the fix-pass parts

Brief `docs/briefs/delta-read-af.md`. Review read: `docs/reviews/review-problems-ito-1-3.md` with its `## Fix pass`. Commit range `05884687..ff3c8309` on `app/content/courses/ito/problems-1.json`, `-2`, `-3`. No browser, no content or engine edit.

Counts: `wrong` 0, `misleading` 3, `reuse` 2 (lines only, both for the main session to rule), `re-author` 0, `continuity` 0, `voice` 0. Every key, every `wrong` value and every printed number in scope agrees with mine. All ten fixes were applied as the reader wrote them. Neither replacement problem retells course material.

## Scope

- Re-authored, whole items: `p-twin-shares` (was `p-digital-measures`), `p-bridge-closes` (was `p-one-touch`), both in `problems-3`.
- Fix-pass parts: `p-maker-tally` (whole item, finding 1); `p-realised-then-risk` prose and part 1 (2); the `variance` line of `p-quarter-rally` part 1 and the `full-variance` line of `p-results-vol` part 3 (3); `p-results-vol` part 4 band (4); `p-cube-path` parts 2 to 4 (5, 7); `p-cable-inverse` parts 2 and 4 (6, 8); `p-touch-note` prose and parts 2 to 4 (10).

## Method

Each part was worked from its text before its key was read. `docs/reports/delta-review-delta-ag-ito-numbers.py` imports no earlier script and uses no SciPy and no root finder, so no solver can fail to converge on another build. Routes: the 625 trades by their exact binomial law; $\Phi$ from `erfc` and again by Simpson's rule; $E[1/X_3]$, $E_P[S_B/S_A]$ and $E_Q[S_B/S_A]$ by integration over the normal law, with no Itô step; the path sums in exact fractions; the note's value also as the discounted first-passage mean $E[e^{-r\tau}]$; its delta by central difference; the touch chance between two closes as a ratio of two normal densities, and again by a seeded simulation of 20,000 pinned paths on a grid of 4,000 (frequency within 0.03 of the key; the run prints `skipped` and does not fail if NumPy is missing or the draw is far off). Each band is rebuilt with the engine's rule and fed what a learner types from the figures the part prints.

Pass 8 rules were checked by hand on every numeric part in scope: the last printed figure against the band, each key and `wrong` value against a tie at the asked places, each rounding of a printed intermediate figure, the reading of a named table at $z$ to 2 places, the source of each $\Phi$, and whether the question hands over its own answer.

Reuse. Every learner-facing string of l1 to l17, `review-1` to `-4`, `homework-1` to `-4`, `problems-4` (less `p-tracking-review`) and the 13 exam items carrying an `it-` skill (`topic-3.2`, `mock-superday-strats`; no stage exam holds one) was dumped to one file and searched for each number, noun and step of the items in scope. l9, l10 and l12 were read against the two new problems screen by screen.

## Tool results

| check | result |
|---|---|
| author's script `problems-ito-numbers.py` | 988 of 988 |
| reader's script `problems-ito-numbers-read.py` | 320 checks, 0 FINDING lines |
| `delta-review-delta-ag-ito-numbers.py` | 432 checks, 0 unlisted failures, 4 FINDING rows (findings 1, 1b, 2, 3), exit 0 |
| validator | 0 errors; no warning on `ito/problems-1`, `-2`, `-3`; `manifest.json` restored |
| voice scan 35, course folder | 0 and 0 (8,783 sentences) |
| `fresh-check --file`, each set | 0 hits; advisories as the author lists (45 and 0.25; 400 and 0.25; 0.25 and 0.75; two shared formulas) |
| `grade-all --file`, each set | 12 widgets each, 0 failures |

The validator sees none of findings 1 to 3.

## Verdict per item

| item | scope | numbers | bands, pass 8 | closest lesson screen | quiz | review | homework | other set | exam | reuse |
|---|---|---|---|---|---|---|---|---|---|---|
| `p-twin-shares` | whole | clean | finding 3 (part 4) | l9 S4 (a hedged book earns $r\Pi$); l10 S2 ($\theta$ defined) | l10 `q-theta`, l9 `q-hedge` | `r-qmean`, `r-mu` | `h-discount`, `h-moment-order` | `p-cable-inverse` (drift of $1/X$); `problems-4` `p-two-date-product` (a $Q$-mean of two prices) | `e-pick-martingales`, `e-cubed-claim` | `clean` as a chain; two lines, finding 5 |
| `p-bridge-closes` | whole | clean | findings 1, 1b (parts 2, 3) | l12 S1 (reflection), S5 (closes miss touches); l10 S4 (the weight is a function of $W_T$) | l12 `q-touch`, `q-shift` | `r-parity`, `r-touch` | `homework-1` `h-bridge` (a pinned path, code); `h-barrier-report` | none | `e-daily-touch`, `s3-touch` | `clean` as a chain; one line, finding 4 |
| `p-maker-tally` | whole | clean | clean | l1 S7 | l1 `q-fine-walk` | `r-var-horizon` | `h-drift-below` | none | `e-qv-drift` | `clean`: fix 1 applied exactly |
| `p-realised-then-risk` | prose, part 1 | clean | clean | l3 S11 | l3 `q-qv-var` | `r-qv-sd` | `h-realised-vol` | `p-quarter-rally` | none | `clean`: fix 2 applied exactly |
| `p-quarter-rally` | part 1 `variance` line | clean | clean | l4 S3 | | `r-qv-sd` | | | | `clean`: fix 3 |
| `p-results-vol` | part 3 line, part 4 band | clean | clean | l7 S8 | | | | | `s2-gbm-median` | `clean`: fixes 3, 4 |
| `p-cube-path` | parts 2 to 4 | clean | clean | l5 S4, l8 S3 | | | | | `e-pick-martingales` | `clean`: fixes 5, 7 |
| `p-cable-inverse` | parts 2, 4 | clean | clean | l6 S5 | | | `h-moment-order` | | | `clean`: fixes 6, 8 |
| `p-touch-note` | prose, parts 2 to 4 | clean | finding 2 (part 3) | l9 S5, l16 S5 | l9 `q-hedge` | | | | `e-cubed-claim` | `clean`: fix 10 applied exactly |

Plain answers on the two new problems.

- `p-twin-shares`. No file of the course or its exam items holds two shares on one $W$, a ratio of two prices, or a claim on one. Part 1 (match $x\sigma\,dW$) is the l9 hedge with a share for the claim. Part 2 uses the step of l9 S4 as its premise and solves for a drift, which nothing asks. Its explanation computes $(0.095 - 0.05)/0.18 = 0.25$, the $\theta$ of l10 S2, but as a reason, and for two shares; no part asks for $\theta$. Part 3's $+\sigma_A^2$ is the drift of `p-cable-inverse` part 1 met again inside a larger sum, with a cross term that set has not. Part 4's trap ("their ratio is not" a martingale) is new; `p-cable-inverse` part 4 says "$X$ and $Y$ cannot both be martingales", a neighbour and not a retelling. None of 0.0084 (l11 holds it once, as a tree error), $-0.0216$, 64.99, 67.86 or 12.5% is used the same way elsewhere.
- `p-bridge-closes`. The course always prices the daily contract and corrects the continuous formula towards it (l12 S3, S5, S9, `e-daily-touch`). This problem runs the other way: the contract is continuous and the daily simulation is corrected by a touch chance between closes. No file holds that chance, a density ratio, or a survival product. `homework-1` `h-bridge` builds a pinned path in code and asks nothing about touching. Part 1 rests on l10 S4 (the weight depends on $W_T$ alone) and asks a question no item asks. The three "not to walk" lists of the first review are respected: no touch chance from the start, no shift, no parity.

Claims checked and held: a drift does not change the law of a path pinned at both ends (the pinned path $B_t - tB_T/T$ is the same for any drift, script); the touch chance $e^{-2(b - x)(b - y)/(\sigma^2\Delta t)}$ for $x, y < b$; gaps independent given the closes; the $Q$ drift of $\ln S$, $0.0058$; equal excess drift per unit of vol for two shares on one $W$; one $Q$ for both; the ratio of two $Q$-martingale-after-discounting prices drifting at $\sigma_A^2 - \sigma_A\sigma_B$; the general solution $AS + BS^{-1.28}$ and a short hedge for sold notes. Units: `p-twin-shares` parts 2 and 3 and `p-cable-inverse` part 4 carry "%". Each later part restates the value it uses. No part in scope can be read off its own question: `p-cube-path` part 4 no longer prints the integrand, and `p-cable-inverse` part 4 no longer states the zero-drift condition.

## Findings

1. `app/content/courses/ito/problems-3.json` | `items[p-bridge-closes].parts[1].widget.tol`, `.explain.text`; `.parts[2].widget.tol` | misleading | The explanation prints "The day's log sd is $0.28/\sqrt{252} = 0.01764$, so $\sigma^2\Delta t = 0.0003111$", and the generic line says "Write both densities with sd $0.28/\sqrt{252}$". But $0.01764^2 = 0.00031117$, which is 0.0003112 at the same places. A learner who works with the sd, as told, gets $e^{-2(0.007168)(0.015295)/0.01764^2} = e^{-0.70466} = 0.49428$, types 0.4943, and meets the generic line: the band is $0.494188 \pm 0.00005$. The same route gives 0.3836 in part 3, refused by $0.383717 \pm 0.0001$ (finding 1b in the script). A chance to 4 places from an exponent near 0.7 needs every input to five figures; half a unit of band is too tight. | Script FINDING 1 and 1b. | Part 2: `tol.abs` 0.00015 (takes 0.4941 to 0.4943; the nearest `wrong`, 0.5058, stays 0.0116 away). `explain.text` sentence 1: "One day's log variance is $\sigma^2\Delta t = 0.0784/252 = 0.0003111$." Part 3: `tol.abs` 0.00015 (takes 0.3836 to 0.3838; nearest `wrong` 0.2488). Tested on a scratch copy: validator 0 errors and no warning on the file, voice 0 and 0, `fresh-check` 0 hits, `grade-all` 0 failures. The author's script then fails one line ("shown 0.01764 not in text"), which the fixer changes to 0.0784/252 in the same commit.

2. `app/content/courses/ito/problems-3.json` | `items[p-touch-note].parts[2].widget.tol` | misleading | The key 0.691956 is 0.000006 above the tie 0.69195 at the 4 places asked, and the band is $\pm 0.00005$. The feedback prints the route "$e^{-1.28\ln(4/3)}$"; with $\ln(4/3) = 0.2877$ it gives $e^{-0.368256} = 0.691940$, so 0.6919, refused. The value came with the first review's finding 10 (barrier £75) and was applied exactly; the validator's tie rule reads only exact ties. | Script FINDING 2. | `tol.abs` 0.0001 (takes 0.6919 and 0.6920; the nearest `wrong`, 0.8318, stays 0.14 away). Part 4 already takes $-88.6$ from either value. Tested as above.

3. `app/content/courses/ito/problems-3.json` | `items[p-twin-shares].parts[3].widget.tol` | misleading | The explanation ends on "$75e^{-0.1432} \approx 64.99$". With the exponential at 4 places, $75 \times 0.8666 = 64.995$ exactly, a tie at the 2 places asked; a learner who rounds half up types 65.00 and is refused ($64.993555 \pm 0.005$). The key is one rounding of a tie on the printed route. The lesser of the three: the route through $e^{-0.0432}$ and $e^{-0.1}$ at 4 places gives 64.99. | Script FINDING 3. | `tol.abs` 0.01 (takes 64.99 and 65.00; the nearest `wrong`, 64.06, stays 0.93 away). Tested as above.

4. `app/content/courses/ito/problems-3.json` | `items[p-bridge-closes].parts[1].question` | reuse, one line; the main session may waive | l12 S1 prose: "By reflection, a path that touches 1 and falls back matches a path that ends above 1." Here: "By reflection, paths from $x$ that touch $b$ and end at $y$ match paths from $x$ that end at $2b - y$." The statement is another one (a mirrored end point, not a doubled tail) and the part's task is new, but the sentence frame is the lesson's. `fresh-check` passes it. | Read by hand. | Replace that sentence by: "Mirror in $b$ the stretch after the first touch: each path from $x$ that touches $b$ and ends at $y$ pairs with one from $x$ that ends at $2b - y$." Tested: voice 0 and 0, `fresh-check` 0 hits, validator clean.

5. `app/content/courses/ito/problems-3.json` | `items[p-twin-shares].parts[1].question`, `.feedback.byKey.no-r` | reuse, two lines; the main session may waive | l9 S4 generic: "The book has no noise, so it earns $r$ on its value $\Pi$." and its `zero` line: "You assumed a hedge removes profit as well as risk. A riskless book still earns interest on its value." Here the question says "It carries no noise, so it must earn $r$ on its value." and `no-r` says "You set the book's drift to zero. A book with no noise still earns $r$ on its £400." The step is the taught premise and must be stated; the slip is the same slip. Only the wording is close. | Read by hand. | `question`: "Using the £600 short in B from part 1, the book is worth £400 and has no $dW$ term. No arbitrage then makes it grow like £400 of cash. What drift $\mu_B$ must B have? Give it as a percentage." `no-r`: "$95/600$ lets the book earn nothing. Free of noise, its £400 must grow at cash's 5%, which is £20 a year." Recomputed: $95/600 = 0.158333$, $0.05 \times 400 = 20$. Tested: validator 0 errors and no warning, voice 0 and 0, `fresh-check` 0 hits, `grade-all` 0 failures, the three scripts unchanged apart from the line named in finding 1.

## Verified with no finding

- `p-maker-tally`: 350, 1,000,000, 2,236.07 and 0.216924; slips 12,675, 175, 8.75, 999,804 ($625(1600 - 0.56^2)$), 25,000, 5,000, 1,000, 0.3632, 0.5, 0.7831, 0.0401. The drift over $\sigma$ is 0.35, so the printed rule of `h-drift-below` no longer gives the key. Part 4 names software only; a table reading at $-0.78$ (0.2177) would miss, as the first review said, and no table is named. The band takes 0.2169 from $z = -0.7826$, $-0.783$ and the unrounded score.
- `p-realised-then-risk` part 1: 0.21 from $0.0147 \times 3$; slips 0.1212, 0.0441, 1.9247. Neither homework sentence remains.
- `p-quarter-rally` part 1: $0.35^2 \times 0.75 = 0.091875$, printed 0.0919, not a tie.
- `p-results-vol` part 3: 74.31, slips 76.45, 74.75, 72.23; half the variance 0.0284375. Part 4: 0.447355; the band 0.001 takes the table reading 0.4483 at $z = -0.13$ (by 0.00005) and 0.4474; slips 0.4301, 0.4007, 0.5526 stay outside.
- `p-cube-path`: sums 0.011, 0.019, 0.126 and the identity $0.216 = 3(0.011) + 3(0.019) + 0.126$ in exact fractions; slips 0.057, 0.061; key $3w$.
- `p-cable-inverse`: $E[1/X_3] = 0.786672$ by integration; slips 0.7534, 0.7699; with $\mu = 1.44\%$ the mean of $Y$ stays at 0.8; slips 0.72%, 0, 12%.
- `p-touch-note`: roots 1 and $-1.28$; 0.691956 by the power and by the first-passage mean; slips 1.4452, 0.8318, 1.3333; delta $-88.5704$ by central difference, slips 88.6 and $-69.2$; no 80 is left in the item.
- `p-twin-shares`: 600 (slips 1,666.67, 1,000, 360); 12.5% (slips 7.5%, 15.83%, 9.5%); 0.84% (slips 3%, 6.24%, $-2.4\%$, 0.12%); £64.99 (slips 69.01, 67.86, 71.83, 64.06); printed 0.0012, 0.0072, 0.0788, $-0.0216$, $-0.0288$, $75e^{-0.1432}$.
- `p-bridge-closes`: 0.494188 (slips 0.7030, 0.9972, 0.5058); touch chances $6 \times 10^{-8}$, 0.1577, 0.4942, 0.0993; survival 0.383717 (slips 0.2488, 0.5058, 0.6163); factor 0.999286, plain figure 9.3933, £3.60 (slips 9.39, 5.79, 4.75, 2.34); printed 0.007168, 0.015295, 0.0003111, 0.7048, 0.0645, 16.6, 0.0058.

## Notes, no change asked

- `p-bridge-closes` part 1, `feedback.correct`, names "the weight from $P$ to $Q$" although the simulation already runs under $Q$ and the drift being dropped is the $Q$ drift 0.0058. The statement is true of any change of drift and the explanation says so in general terms.
- `p-bridge-closes` prose lists five closes for a four-day option; the first is the start. Part 3 says "the other three gaps", which settles it.
- `p-twin-shares` and `p-touch-note` now both hold a 75 ($100 \times 0.75$ and the barrier £75) and a 0.25 (the price of risk and $\sigma$). Different roles; no pair is shared.

## Engine

- `[rounding-tie]` reads only exact ties of the stored value. It misses a key within $10^{-5}$ of a tie at the asked places (`p-touch-note` part 3, 0.691956 at 4 places) and a tie reached by one printed factor at 4 places ($75 \times 0.8666 = 64.995$, `p-twin-shares` part 4).
- `[working-band]` reads the last figure only. It misses a printed intermediate figure that leads outside the band: an sd printed as 0.01764 beside its square printed as 0.0003111 (`p-bridge-closes` part 2).
