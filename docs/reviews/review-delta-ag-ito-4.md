# Delta read AG, ito level 4: the re-authored `p-band-wait` and the text fixes

Counts: `wrong` 0, `misleading` 1, `reuse` 1 (two lines), `re-author` 0, `continuity` 1, `voice` 0, `other` 0. No key, `wrong` value or printed number is mistaken. No item is ruled `re-author`.

Scope, commit range `ff3c8309..1b415c2c` on `app/content/courses/ito/problems-4.json`, read against `docs/reviews/review-problems-ito-4.md` and its `## Fix pass`:

- `p-band-wait` (replaces `p-tracking-review`), all five parts;
- `p-two-date-product` part 2, `generic` and `byKey.no-cov`;
- `p-dividend-hedge` `prose`, part 3 question and `byKey.plus`, part 4 `explain`.

No browser, no content or engine edit. Fix texts were tried on a copy of the course in the scratch folder, not in the worktree.

## Method

`docs/reports/delta-review-delta-ag-ito-4-numbers.py` imports no earlier script. `p-band-wait` was solved from its text before its keys were read, then by four routes, none of them the author's chain of stopped martingales:

- A. Cubic solutions of $\tfrac12\sigma^2u'' = -g$ for $g = 0$, $1$, $h$, $1 - h$ and $x$, checked by substitution in sympy, in exact fractions. The identity $E[X_\tau^3] = x_0^3 + 12E\int_0^\tau X\,dt$ and the martingale $tX_t - \int_0^t X\,ds$ give $E[\tau X_\tau]$ afresh.
- B. The absorbing walk on whole pips with a step of a quarter minute, solved as a linear system. Its exit law and exit times equal the continuous ones exactly.
- C. The Laplace transforms $\sinh(xk)/\sinh(Lk)$ and $\sinh((L - x)k)/\sinh(Lk)$ of the exit time on each edge, differentiated at 0 by a series.
- D. A simulation of the walk, 20,000 paths, fixed seed, 5% tolerance, printed as NOTE lines only.

Each band was rebuilt and fed what a learner types at the asked places; each slip was rebuilt from its formula, typed at the asked places and routed. The pass 8 rules were checked by hand as well as by the validator.

## Tool results

| check | result |
|---|---|
| author's script `problems-ito-4-numbers.py` | 325 of 325, exit 0 |
| reader's script `problems-ito-4-numbers-read.py` | 299 of 299, 0 FINDING lines, exit 0 |
| course scripts `problems-ito-numbers.py`, `-read.py` | 988 of 988; 320 checks, 0 FINDING lines |
| `delta-review-delta-ag-ito-4-numbers.py` | 204 checks, 0 failed, 3 FINDING rows (the findings below), 6 NOTE lines, exit 0 |
| validator | 0 errors, 4566 warnings, none on `ito/problems-4`; `manifest.json` restored |
| voice scan 35, course folder | 0 and 0 (8,798 sentences) |
| `fresh-check --file --pairs` | 0 hits |
| `grade-all --file` | 13 widgets, 0 failures |

Simulation (seed 20261117): $P$ 0.6007, $E[\tau]$ 149.01, top 131.69, floor 175.07, $E[\tau X_\tau]$ 3,955, $E[X_\tau^3]$ 75,088. All agree.

## Verdict per item

| item | changed part | numbers | reuse | chain |
|---|---|---|---|---|
| `p-band-wait` | parts 1, 3, 4, 5 | clean | clean, one likeness below | holds |
| | part 2 | clean | reuse, two lines (finding 1) | holds; misleading wording (finding 2) |
| | part 4 `explain` | clean | clean | continuity (finding 3) |
| `p-two-date-product` | part 2 lines | clean | clean | holds |
| `p-dividend-hedge` | stem, parts 3 and 4 lines | clean | clean | holds |

### `p-band-wait`: closest items

| source | text | ruling |
|---|---|---|
| l13 `screens[0]` (slide $c$ for $W_t^3 - c\,tW_t$) | "For $f = x^3 - ctx$ we have $f_t = -cx$ and $\tfrac12f_{xx} = 3x$. The drift $(3 - c)x$ vanishes at $c = 3$." | **reuse**, part 2 `explain` and `no-half` (finding 1) |
| l14 `screens[2]` ($a = 2$, $b = 3$: "$P = 3/5 = 0.6$ ... The values 0.4 (near distance over total) and 0.5") and `screens[6]` ($a = 2$, $b = 3$, $\sigma = 2$: $E[\tau] = 1.5$) | set: start 30 in a band of 50, $\sigma = 2$; $P = \tfrac35$, slip 0.4, $E[\tau] = 150$ | clean, likeness noted below |
| l14 `quiz` `q-ratio`, `q-sigma`; review-4 `r-exit-sigma` (take-profit £3, stop £1, $\sigma = 0.5$, 12 days); homework-4 `h-stopping`, `h-exit-drift` | $P$ or $E[\tau]$ asked alone, trade-exit story | clean: the set asks neither alone and tells another story |
| set 2 `p-cube-path` part 4 ("$f_{xx} = 6x$, so $\tfrac12f_{xx} = 3w$") | the cube's $dt$ term on a coarse path | clean: another task; covered by the fix of finding 1 |
| sets 1 to 3, with `p-twin-shares` (a ratio note on two shares) and `p-bridge-closes` (a barrier touched between daily closes) | no exit time, no $\tau$, no band | clean, no collision |
| exams `topic-3.2` `e-exit-drift` ($-0.3t + 0.9W$, $+1$ or $-2$), `e-pick-martingales`, `e-sixth-repair`; `mock-superday-strats` `s1`, `s3-touch` | drifted exit, repairs, one-barrier touch | clean |
| `markov/problems-3` `p-pairs-exit` (fair walk, target $+3$, stop $-5$: $\tfrac58$, 15 days, financing cost) | "The target is the nearer end, so it is likelier." | clean: another course, discrete, $P$ and the mean asked, no conditional wait |
| `markov/problems-2` `p-band-days` (closes labelled Below, Inside, Above a band; a three-state chain) | shares the word "band" and the id stem `p-band-` | clean: no exit, no shared number or step |

Story greps of `app/content/`: "pips", "central bank" and a currency band appear in no other file. "Band" appears in `markov` as above and in `topic-0.4` `e-code-band` (a code item on closes outside a band): no collision.

Likeness, not a finding. The barrier distances 20 and 30 with $\sigma = 2$ are l14 `screens[2]` and `screens[6]` ($a = 2$, $b = 3$, $\sigma = 2$) with the distances times 10. So $P = \tfrac35$ and the slip 0.4 are the lesson's, and $E[\tau] = 150$ is 100 times its 1.5. $P$ and $E[\tau]$ are givens of parts 4 and 5 here, the stem states a start and a band rather than $a$ and $b$, and no sentence is shared. A learner would not place it. If the set is renumbered for another reason, move off the 2 to 3 split.

The first read's conditions hold: no part asks for $c$, $P$ or $E[\tau]$ alone; the trade-exit story is gone; every numeric part states its form; the results (the stopped cubic martingale and both conditional waits) are in no lesson, review, homework, set or exam item.

### Optional stopping in part 2

The condition stated is the right one and it is sufficient. $X$ bounded alone is not enough, since $tX_t$ is unbounded. With $0 \le X \le 50$ up to $\tau$, $|M_{t \wedge \tau}| \le 50^3 + 12 \times 50\,\tau$, which has finite mean $125{,}000 + 600 \times 150 = 215{,}000$. Dominated convergence then gives $E[M_\tau] = M_0$. This matches l14 `screens[1]` ("a finite $E[\tau]$ is also enough") and `h-stopping`. Only the wording of the conclusion is loose (finding 2).

## Findings

1. `problems-4.json` | `items[0].parts[1].explain.text`, `items[0].parts[1].feedback.byKey.no-half` (`p-band-wait` part 2) | reuse | Two lines retell l13 `screens[0]` with $\sigma^2$ folded in. This is the pair the first read quoted in its finding 1, carried into the new problem.
   - Lesson `explain`: "For $f = x^3 - ctx$ we have $f_t = -cx$ and $\tfrac12f_{xx} = 3x$. The drift $(3 - c)x$ vanishes at $c = 3$." Set `explain`: "The drift of $x^3 - ctx$ under $X = 30 + 2W$ is $-cx + \tfrac12 \times 4 \times 6x = (12 - c)x$, so $c = 12$."
   - Lesson `whole`: "You cancelled all of $f_{xx} = 6x$. Itô's lemma carries only half of it." Set `no-half`: "You used $c = 24$, from $6 \times 4$. Itô's lemma halves the second derivative, so $c = 12$."
   - Exact `explain.text`: "Since $(dX)^2 = 4\,dt$, the constant 3 of $W_t^3 - 3tW_t$ is scaled by 4, so $c = 12$. The stopped mean equals the start, $30^3 = 27{,}000$. So $12E[\tau X_\tau] = 75{,}000 - 27{,}000$ and $E[\tau X_\tau] = 4{,}000$."
   - Exact `byKey.no-half`: "That takes $c = 24$. Check it on the drift: $X^3$ gains $12X\,dt$, and $24tX$ would take off twice as much."
   - Check: $d(X^3) = 3X^2\,dX + 3X(dX)^2$ gives $12X\,dt$ whatever the start; $48{,}000/12 = 4{,}000$; $48{,}000/24 = 2{,}000$, the slip's value, unchanged.

2. `problems-4.json` | `items[0].parts[1].question` (`p-band-wait` part 2) | misleading | "optional stopping holds: the stopped process keeps its starting value." The process does not keep its value: it ends at $50^3 - 600\tau$ or at 0. Its mean keeps the starting value. A learner who takes the line as written has nothing to equate. Exact fix for that clause: "so optional stopping holds: the mean at $\tau$ equals the value at $t = 0$." The rest of the question is unchanged.

3. `problems-4.json` | `items[0].parts[3].explain.text` (`p-band-wait` part 4) | continuity | "As a check, $(50^2 - 30^2)/12 = 1{,}600/12$ gives the same." The closed form is taught nowhere and is not named, so the check reads as arithmetic from nowhere. Exact `explain.text`: "$A$ is $P$ times the mean wait given the top, so the wait is $80/0.6 \approx 133.33$ minutes. A band of width $L$ entered at $x$ gives $(L^2 - x^2)/(3\sigma^2)$ in general, here $1{,}600/12$." Check: route A gives $w(x)/h(x) = (L^2 - x^2)/(3\sigma^2)$; $1{,}600/12 = 133.33$.

All three fixes together, on a scratch copy of the course: this script 204 checks, 0 failed, three rows `resolved`; voice scan 0 and 0; `fresh-check --content <copy> --file --pairs` 0 hits; `grade-all --file` 0 failures. Neither earlier script pins a changed line. No key or `wrong` value changes.

## Verified with no finding

- Keys, each by routes A, B and C: $E[X_\tau^3] = 75{,}000$; $c = 12$ and $E[\tau X_\tau] = 4{,}000$; $A = 80$; $E[\tau \mid X_\tau = 50] = \tfrac{400}{3}$; $E[\tau \mid X_\tau = 0] = 175$. Givens: $P = \tfrac35$, $E[\tau] = 150$. Check sums: $A + 70 = 150$; $50A = 4{,}000$.
- All 15 `wrong` values rebuilt from their slips: 27,000, 50,000, 125,000; 2,000 ($c = 24$), 8,000 ($c = 6$), 6,250, 16,000 ($c = 3$); 1.6, 4,000; 48, 80, 200; 41.67, 70, 116.67. Each is refused by the key band, taken by its own band as typed at the asked places, and has its own line. No two bands of a part meet.
- Pass 8 by hand. Working band: each `correct` and `explain` ends on the key at the asked places. Rounding ties: none; 133.33 is taken, 133.3 and 133.34 are refused; a learner who carries 133.33 into the `wrong-weight` slip types 42 and is routed. No percentage part; no table value. No `wrong` band is wider than its value (1.6 with 0.5 is the widest).
- Claims: $X_\tau^3 = 2{,}500X_\tau$ on both edges; the drift of $X_t^3$ is $12X_t$, positive in the band; the rate starts nearer the top; "volatility 1" suits $c = 3$; the far edge takes longer ($175 > 150 > 133.33$).
- Chain: each part restates its input, and no part can be passed backwards from a printed target. Skills `it-martingale` and `it-bm` are the level's.
- `p-two-date-product` part 2: both lines are the first read's text word for word. $0.09 \times (1 + 2 + 2) = 0.45$, also from the covariance matrix of $(W_1, W_2)$; 0.27 is the `no-cov` slip's value. Neither line retells l15 `screens[5]`.
- `p-dividend-hedge`: the four texts are the first read's word for word; "dividend dates" and "Under $Q$ the share grows" are gone. $V = 118.2134$; $V_t = 2.3643$ by a central difference, positive; $K = 122.27$ both ways. No number changed.

## Engine

- `fresh-check` passes `p-band-wait` part 2, whose `explain` is l13 `screens[0]`'s `explain` with $\sigma^2$ folded into each coefficient ($3$ to $12$, $6x$ to $4 \times 6x$). The same class as the bullet raised by the first read; one more instance.
- `fresh-check --file <path outside the content root>` reads the file as an exam and reports the set against itself. With `--content <copy>` it works. A line in its usage text would save the next reader the detour.
