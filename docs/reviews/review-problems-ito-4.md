# Problem set 3.2, ito level 4: second-reader findings

Scope: `app/content/courses/ito/problems-4.json`: 3 problems, 13 parts (11 numeric, 1 `expression`, 1 choice), 35 `wrong` entries. Rules: `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md`, `docs/briefs/wave-c-author-ag.md`, `docs/briefs/wave-c-reader-ag.md`. Sets 1 to 3 were read as reuse sources only.

## Verdicts

| problem | closest lesson screen | closest quiz, review, homework | closest other set, exam | verdict |
|---|---|---|---|---|
| `p-tracking-review` | l13 S1 ($W_t^3 - c\,tW_t$, slide $c$ to 3); l14 S3 ($a = 2$, $b = 3$: $P$ and $E[\tau]$); l14 S7 ($X = \sigma W$, $X_t^2 - \sigma^2t$, $E[\tau] = ab/\sigma^2$) | l14 `q-ratio`, `q-sigma`; review-4 `r-exit-sigma`; homework-4 `h-stopping` | no set problem; exam `e-exit-drift` | **re-author** (finding 1) |
| `p-two-date-product` | l15 S5 ($\text{Var}(W_2 + W_3)$ by $\min(s, t)$); l16 S4, S5 ($S_T^2$ by the mgf) | l15 `q-const`; l16 `q-cube`; review-4 `r-sqrt`; homework-4 `h-moments` | set 1 `p-quarter-rally` (restart at 0.25, one price); exam `e-var-two-times`, `e-cubed-claim` | **reuse**, two lines (finding 2) |
| `p-dividend-hedge` | l17 S2 to S5 (derivation, where $\mu$ goes); l17 S8 (forward in the equation); l16 S2 (forward, no dividends) | l17 `q-vt`; l16 `q-fwd2`; review-4 `r-mu`; homework-4 `h-derivation` | set 3 `p-touch-note` (a claim solved in the equation); exam `e-theta-from-pde` | **clean**; the dividend ruling is finding 3 |

## Tool results

| check | result |
|---|---|
| author's script | `problems-ito-4-numbers.py` 323 of 323, exit 0 |
| reader's script | `problems-ito-4-numbers-read.py` 315 of 316, exit 0, 1 FINDING line (finding 4) |
| validator | 0 errors, 4567 warnings, none on `ito/problems-4`; `manifest.json` restored |
| voice scan 35, course folder | 0 and 0 (8,752 sentences) |
| `fresh-check --files problems-4 --pairs` | 0 hits |
| `grade-all --file` | 13 widgets, 0 failures |

Method. Every key, `wrong` value and printed number was recomputed by routes the author did not use: Gaussian conditional moments for the cubic martingale; the boundary-value problems $\tfrac12\sigma^2u'' = -1$ and $\tfrac12\sigma^2w'' = -h$ for $E[\tau]$ and $E[\tau\,\mathbf 1_{\{X_\tau = 2\}}]$; the closed form $(L^2 - x_0^2)/(3\sigma^2)$; Gauss-Hermite quadrature over the two yearly moves and the tower rule; finite differences of $V$, a reinvested share count and a quadrature of $S_T$ at drift $r - q$. No root finder is used. Lessons l13 to l17, review-4, homework-4 and the ito-skilled items of `exams/topic-3.2.json` and `exams/mock-superday-strats.json` were read for reuse.

## Findings

1. `problems-4.json` | `items[0]` (`p-tracking-review`), parts 1 to 3 | reuse, **re-author** | Parts 1, 2 and 3 walk three course items in a row, each with that item's own slips. Parts 4 and 5 (the stopped cubic martingale and $E[\tau \mid X_\tau = 2] = \tfrac{125}{3}$) are new and correct.
   - Part 1 against l13 S1. Lesson: "For $f = x^3 - ctx$ we have $f_t = -cx$ and $\tfrac12f_{xx} = 3x$. The drift $(3 - c)x$ vanishes at $c = 3$." Set: "With $f = x^3 - ctx$ we have $f_t = -cx$ and $f_{xx} = 6x$. The drift is ... $(0.48 - c)x$. It is zero for every $x$ only at $c = 0.48$." Slip `no-half` (0.96) is the lesson's `whole` (6) times $\sigma^2$.
   - Part 2 against l14 `q-ratio`. Quiz: "$P = b/(a + b) = 1/5$"; `swapped` "That is the chance of reaching $-1$ first"; `half` "You assumed a fair coin". Set: "$P = b/(a + b) = 4/6$"; `swapped` "That is the chance of reaching $-4$ first"; `even`.
   - Part 3 against l14 S7 and review-4 `r-exit-sigma`. Lesson: "$E[X_\tau^2] = ab = 6$ and $E[X_\tau^2] = \sigma^2E[\tau] = 4E[\tau]$, so $E[\tau] = 1.5$"; `unsquared` "You divided by $\sigma = 2$ rather than $\sigma^2 = 4$"; "variance builds as $\sigma^2t$". Set: "$E[X_\tau^2] = 0.16E[\tau]$ and $E[X_\tau^2] = ab = 8$, so $E[\tau] = 8/0.16 = 50$"; `sigma-unsquared` "You divided by $\sigma = 0.4$. Variance builds as $\sigma^2t$". Review: `no-sigma` "You gave $ab = 3$, ignoring the volatility"; set `no-sigma` "That is $ab = 8$".
   - Not to walk in the new problem: l13 S1 (the $c$ slider for $W^3 - ctW$) and S4 (repair of $W^4$); l14 S1 to S3 ($P = b/(a + b)$, $E[\tau] = ab$), S7 ($ab/\sigma^2$), `q-ratio`, `q-sigma`; review-4 `r-exit-sigma`; homework-4 `h-stopping`, `h-exit-drift`; exam `e-exit-drift`, `e-sixth-repair`. No graded part may be "find $c$", "find $P$" or "find $E[\tau]$" on their own. The conditional exit time and the stopped cubic martingale are not in the course and may be kept as the result.
   - Carry into the re-author: findings 4 and 5.

2. `problems-4.json` | `items[1].parts[1].feedback` (`p-two-date-product`, part 2) | reuse | Two lines paraphrase l15 S5. Lesson generic: "Add the two variances and twice the covariance, which is $\min(2, 3)$." Set generic: "Add the two variances, $\sigma^2 \times 1$ and $\sigma^2 \times 2$, and twice the covariance." Lesson `no-cov`: "You added the variances only, $2 + 3 = 5$. The two times share the first 2 units of increments." Set `no-cov`: "You added the two variances alone. The logs move together, so twice their covariance joins the sum." The task itself (the level's standard step, feeding a product price the course never sets) stands. Exact fix:
   - `generic`: "Not quite. One year of $\sigma^2$ is 0.09. Count the years in $\text{Var}(X) + \text{Var}(Y) + 2\,\text{Cov}(X, Y)$: one, two and twice one."
   - `byKey.no-cov`: "That is 0.27, the answer for independent logs. Year 1 sits in both logs and adds $2 \times 0.09$."
   - Check: $0.09 \times (1 + 2 + 2) = 0.45$; $0.27 + 0.18 = 0.45$.

3. `problems-4.json` | `items[2]` (`p-dividend-hedge`), `prose`, `parts[2].question`, `parts[2].feedback.byKey.plus`, `parts[3].explain` | misleading | **Ruling on the dividend yield.** The course only ever says "pays no dividends" (l16 S2, homework-3, homework-4); it never defines a yield. The stem's cash-flow sentence is enough for parts 1 and 2: with it, the derivation is l17's with one more $dt$ term. Three places still lean on knowledge the course does not give, and one line is false for a continuous yield.
   - (a) Stem. It does not say that the claim gets no dividends, so a learner cannot tell whether being short the claim costs the desk dividend cash. Exact `prose`: "A share pays its holder a steady dividend: over each $dt$, $\Delta$ shares pay cash $q\Delta S\,dt$. The rate $q$ is the dividend yield. The claim $V(t, S)$ receives no dividends. The share follows $dS = \mu S\,dt + \sigma S\,dW$, and cash earns $r$. A desk sells one claim and holds $\Delta = V_S$ shares."
   - (b) Part 3 question. "A claim pays one share at $T$, with no dividends before then" reads as the share paying none, against $q = 2\%$. Exact text for that sentence: "A claim delivers one share at $T$, and its holder receives none of the dividends paid before then. Its value is $V = Se^{-q(T - t)}$, so $V_S = e^{-q(T - t)}$ and $V_{SS} = 0$." The rest of the question is unchanged.
   - (c) Part 3 `byKey.plus`: "The claim gains value as the dividend dates pass." A yield paid over every $dt$ has no dates. Exact text: "That uses $r + q$ in the equation, which flips the sign. The claim gains value with time, as fewer dividends are left to miss." ($V_t = qV = 2.3643 > 0$.)
   - (d) Part 4 `explain`: "Under $Q$ the share grows at $r - q$" is not taught; the course's $Q$ drift is $r$. Exact text: "The forward is worth $Se^{-qT} - Ke^{-rT}$, so $K = Se^{(r - q)T}$. The growth rate $r - q$ is the bracket of part 2. Here $K = 120e^{0.025 \times 0.75} \approx 122.27$."
   - Numbers unchanged: $V = 120e^{-0.015} = 118.2134$, $V_t = 2.3643$, $K = 120e^{0.01875} = 122.27$.

4. `problems-4.json` | `items[0].parts[2].question` | continuity | The part states no form ("what is $E[\tau]$ in trading days?"); the band is exact. Exact fix if the part survives the re-author: append "Give a whole number."

5. `problems-4.json` | `items[0].parts[3].question` | misleading | Optional stopping is used on $X_t^3 - 0.48tX_t$ with no condition; l14 S4 and `h-stopping` teach that the condition matters. The step is valid here (the gap is bounded up to $\tau$ and $E[\tau] = 50$ is finite, so the stopped martingale is dominated by $64 + 1.92\tau$). Exact fix for the first sentence: "Stop the martingale $X_t^3 - 0.48tX_t$ from part 1 at $\tau$. The gap stays between $-4$ and $2$ and $E[\tau]$ is finite, so optional stopping holds: $E[X_\tau^3] = 0.48E[\tau X_\tau]$."

## Same-course reuse, read by eye

- `p-two-date-product` parts 3 and 4 against l16 S4, S5: the lesson squares one price; the set takes the lognormal mean of a product at two dates and names the shared year as the source of $e^{0.09}$. Slip lines differ. Clean.
- `p-dividend-hedge` part 3 against l17 S8: both put a claim with $V_{SS} = 0$ into the equation, and both discount by $e^{-0.015}$ (lesson: $r = 3\%$, half a year; set: $q = 2\%$, 0.75 years). One shared factor, different claim, coefficient and sign of $V_t$; no line is shared. Clean, noted.
- `p-dividend-hedge` part 4 against l16 `q-fwd2` ($100e^{0.1}$) and l16 S2: the set's forward carries the yield. Clean.
- Stories (fund's return gap to an index; product of two prices; dividend yield hedge) are not in `app/content/courses/ito` or the two exams. Dividend yields are taught in `markets` and `opt-dash` only.

## Verified

- Keys: 0.48, $\tfrac23$, 50, $-\tfrac{100}{3}$, $\tfrac{125}{3}$; 0.09, 0.45, $25e^{0.18} = 29.9304$, $25e^{0.12} = 28.1874$; option `with-yield`, $r - q$, 2.364269, 122.271226. All 35 `wrong` values rebuilt from their slips, each refused by its key band and carrying its own line.
- Bands: each takes the stated rounding and the printed working ($27.78/\tfrac23 = 41.67$; $0.02 \times 118.2134$; $118.2134e^{0.03375}$); no rounding tie; £ parts carry the unit; no percentage part.
- Claims: nearer level likelier; conditioning on it shortens the wait ($41.67 < 50 < 66.67$); $a(a + 2b)/(3\sigma^2)$; each price's $Q$-mean is its forward; the gap £2.43; dividends lower the forward.
- Chain: each later part restates its input. No part can be passed backwards from a printed target. Every lesson l13 to l17 is drawn on.

## Counts

| severity | count | findings |
|---|---|---|
| wrong | 0 | |
| misleading | 2 | 3, 5 |
| reuse | 2 | 1 (re-author), 2 |
| continuity | 1 | 4 |
| voice | 0 | |

## Engine

- `fresh-check` passes `p-tracking-review` parts 1 to 3. Each is a course item with $\sigma^2$ folded in: same explain skeleton, same slip set by formula (`whole` and `no-half`; `swapped`, `half` and `even`; `none`, `unsquared` and `no-sigma`, `sigma-unsquared`). Raised in `docs/BACKLOG-INBOX.md`.

## Fix pass

Session AF, re-author and fix pass (brief `docs/briefs/reauthor-fix-af.md`).

1. Re-authored as `p-band-wait`. A currency held in a 50-pip band, $X = 30 + 2W$ in pips, exit at 0 or 50. Chain: $E[X_\tau^3] = 75{,}000$ (via $X_\tau^3 = 2{,}500X_\tau$); $c = 12$ and the stopped cubic martingale give $E[\tau X_\tau] = 4{,}000$; $A = 80$; $E[\tau \mid X_\tau = 50] = 133.33$; $E[\tau \mid X_\tau = 0] = 175$ minutes. $P = \tfrac35$ and $E[\tau] = 150$ are given; no part asks for $c$, $P$ or $E[\tau]$ alone. Every part states its form. The trade-exit story was avoided (l14, review-4).
2. Fixed: `generic` and `byKey.no-cov` as given ($0.09 \times 5 = 0.45$; $0.27 + 0.18 = 0.45$).
3. Fixed (a) to (d) as given; numbers unchanged ($V = 118.2134$, $V_t = 2.3643$, $K = 122.27$).
4. Carried into the re-author: every numeric part of `p-band-wait` states its form ("Give a whole number" or "Give 2 decimal places").
5. Carried into the re-author: part 2 states the condition as given ("Up to $\tau$ the rate stays between 0 and 50 and $E[\tau]$ is finite, so optional stopping holds").

Keys changed: `items[0]` only (75000, 4000, 80, 133.333333, 175 with 15 new `wrong` values). Scripts: author's `problems-ito-4-numbers.py` 325 of 325, exit 0 (new block for `p-band-wait`, `0.27` added to the printed checks of `p-two-date-product` part 2); reader's `problems-ito-4-numbers-read.py` retargeted from `p-tracking-review` to `p-band-wait` on the reader's own routes (Gaussian conditional moments, boundary-value problems, closed forms), 299 of 299, 0 FINDING lines, exit 0.

Gates: validator 0 errors, no warnings on `ito/problems-4`; voice scan 35 0 and 0 (8,767 sentences); `fresh-check --file --pairs` 0 hits; `grade-all --file` 13 widgets, 0 failures; playthrough `--problems ito/problems-4` green desktop and `--mobile`, part shots at 440 px read, no layout faults.
