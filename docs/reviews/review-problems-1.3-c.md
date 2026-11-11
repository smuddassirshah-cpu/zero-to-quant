# Problem sets 1.3 (c): second-reader findings

Read at commit 90e1198. A full second read of five sets. Pattern: `review-problems-1.3-a.md`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways, does not give what the learner needs, or refuses a sensible rounding in the stated form; `minor` = weak part, loose `wrong` entry, wording, freshness or tooling.

## C. Second read: limits 4 and 5, integrals 4, multivar 4 and 5

Scope: `app/content/courses/limits/problems-4.json` and `problems-5.json`, `integrals/problems-4.json`, `multivar/problems-4.json` and `problems-5.json`: 17 problems, 78 parts (31 limits, 18 integrals, 29 multivar; 60 numeric, 15 expression, 3 choice). Sets 1 to 3 of these courses were not read.

Method. The three authors' scripts were run first. Every part was then solved from its text, by hand, and again in `problems-1.3-c-scripts/mine.py`: sympy for the exact value, then a second route (mpmath quadrature in one, two or three variables, a numeric limit, a central difference, a root finder, a grid scan over the triangle of shares or the field). Every `wrong` value was rebuilt from the slip its feedback line names and compared inside that entry's own band; every expression key, `accept` form and `wrong[].tex` was compared with my own expression at sample points. Every part was then put through the engine's own graders in node (`grade-check.mjs`: `parseNum`, `within`, `exprEqual`, `exprEqualUpToConstant`, with the local Compute Engine): the answer, each `accept` form, each `wrong` entry, and 142 typed strings of my own (fractions, roundings in the stated form, other correct forms of each expression, near misses, a root outside its domain). The lessons of each level were searched and the passages read for each idea a set leans on (`taught.py`): the second derivative test (limits l13), ends of a closed range (l14), the tangent estimate and convexity (l15), $\tfrac{\infty}{\infty}$ and the rule used twice (l16), bounding with $|f'| \le M$ (l17), the slope of $\arctan u$ and the inverse rule (l19), inflection (l20); cover-up and "divide first" (integrals l14), $x = a\sin\theta$, even and odd powers (l15), $\int_0^1 x^{-p}\,dx$ (l16), discs and shells (l17); strips (multivar l14), polar (l15), $\sigma\sqrt{2\pi}$ (l16), the area factor (l17), triple integrals (l18), two multipliers (l19), edges and corners (l20).

Tool results.

| check | result |
|---|---|
| authors' number scripts | limits 1242 checks, 0 failures; integrals 1053 of 1053; multivar 718 of 718 |
| `mine.py` (reader's own answers and slips) | 78 parts, 729 checks, 0 failures |
| `grade-check.mjs` (engine graders) | 733 checks, 0 failures, 1 row held to be a fault (finding 12), 2 wide `wrong` bands noted (findings 5, 9) |
| `proposed.py` (numbers of the fixes below, item skills) | all hold |
| validator | 0 errors; 0 warnings on the five files |
| playthrough `--problems`, five sets, `--local-cdn` | green |
| the same with `--mobile` | green |
| voice scan 35, three course folders | 0 and 0 |
| `fresh-check.mjs --file`, gate | 0 hits on each set |
| `fresh-grep.py` (reader's own: formulas and nouns across each course and the exams) | one hit that matters (finding 11); the rest judged below |

Result. No `answer`, `accept`, feedback line or explanation states a wrong value of the quantity asked, and no claim in the 78 parts is false. Every stated number agrees with my own. Every expression answer is LaTeX (`\ln`, `\sqrt`, `\pi`, `e^{...}`); every answer and `accept` form grades correct and every `wrong[].tex` grades wrong. Restricted domains: `\sqrt{9-x^2}` (`p-corner-sprinkler` part 1) is real on the whole sampling range 0.3 to 3, takes $\sqrt{(3-x)(3+x)}$ and $(9-x^2)^{0.5}$, and refuses $-\sqrt{9-x^2}$ and $\sqrt{x^2-9}$; the $\arcsin$ slip `\frac{1}{\sqrt{1-\frac{x^2}{900}}}` (`p-camera-pan` part 1) is real there and grades wrong. The antiderivative part (`p-impact-kernel` part 2, `upToConstant`) takes `+ C`, $2\ln\tfrac{1+u}{2+u}$, $\ln\tfrac{(1+u)^2}{(2+u)^2}$, $2\ln\tfrac{2+2u}{2+u}$ and the form with bars. The constant answers $8\pi$, $\tfrac{1}{8\pi}$, $2\pi$, $\tfrac{4\pi}{3}$ refuse their decimals (25.13, 6.28) and take equal forms ($\tfrac{0.125}{\pi}$, $\tfrac{8\pi}{6}$). Keys that are steep in the sampled symbol still tell the slips apart: $\tfrac{1000}{250000+q^2}$ refuses $\tfrac{1}{250}$ and $\tfrac{1000}{250000+q}$.

Claims checked beyond the keys: $V(u) > 0$ for every $u \ne 0$ on $-3$ to 3, so "any shift, up or down, raises the book's value" is true globally and not only near 0; $A(r)$ is $\int_0^{10} e^{-rt}\,dt$; $R'' < 0$ at $s = 1$ and the true gain 6.51; the logistic curve obeys the stated rate law, starts at 100, has its inflection at $t = \ln 9$ and reaches 900 at $t = \ln 81$; the stated $p''(q)$; $w(t) < \tfrac{1}{2\sqrt t}$ and $w \sim t^{-3/2}$; $f(\sqrt2) \approx 0.17$ is the top of the dish's region; the shell integral of the seal is $6\pi^2$ in $x$ as well as in $\theta$; the sprinkler's water by Cartesian quadrature (31.81); the tent's volume and $\iiint z\,dV$ by quadrature over the ellipse; the field's total $\tfrac{32}{15}$ in $x, y$ directly; the fund's best point by a grid over the whole triangle (2.125 at $(0.75, 0.25, 0)$), the edge values 1.125 and 2, and the corners 2, 1, 0.

### Findings

1. `unclear` | `limits/problems-5.json` | `p-app-adoption` | part 5.
   "What is the shortest time to go from 100 to 900 thousand users?" The app's true time is fixed by the prose: $\ln 81 \approx 4.39$ months. The part wants the bound 3.2. "Use only that and the mean value theorem" is the only signal, and a learner who answers the question as asked is refused (the `actual` line then explains).
   Fix: question "Part 4 showed $N' \le 250$ at all times. Use only that and the mean value theorem. At least how many months must it take to go from 100 to 900 thousand users? Give months as a decimal." No other edit; `actual` stays.

2. `minor` | `limits/problems-4.json` | `p-signal-decay` | chain.
   Parts 1 and 2 (57 and $-3$) feed nothing: part 3 uses them only as a story ("rises at first and falls in the end") and solves $N'(t) = 0$ afresh. Only part 4 uses an earlier answer. The author's report does not list this one.
   Fix: part 3 question "Part 1's working gave the slope $N'(t) = \dfrac{60}{1+t} - 3$, which is 57 at $t = 0$. Part 2 shows $N$ falls in the end. On which day $t$ is $N(t)$ largest? Give a whole number." The chain is then 1 to 3 to 4, with part 2 the reason a largest day exists. Answer, `wrong` and feedback unchanged.

3. `minor` | `limits/problems-4.json` | `p-barbell-hedge` | part 4.
   The lead-in "Using parts 2 and 3:" promises a use the part does not make: the answer is $V(0.01)$ from the formula. A learner who does use them gets $\tfrac12 V''(0)u^2 = 0.045$ thousand, types 45 and sees only the generic line. Three terms near 50 and 95 cancel to 0.04, and the need for 5 places is said only after a miss.
   Fix: question "Parts 2 and 3 say the tangent at $u = 0$ is flat and $V$ bends up, so the tangent predicts no change. Yields rise by 1 percentage point, so $u = 0.01$. Work out the true value $V(0.01)$ from the formula, keeping each term to 5 decimal places. Give your answer in pounds, to the nearest pound." Add to `wrong` `{ "id": "second-order", "value": 45, "tol": { "abs": 0.5 } }` and to `byKey` `"second-order": "That is the estimate $\\tfrac12 V''(0)u^2 = \\tfrac12 \\times 900 \\times 0.0001$ thousand. The question asks for the true value from the formula, which is a little lower."` Bands: answer 42.31 to 43.31, new entry 44.5 to 45.5, `wrong-way` 46.81 to 47.81.

4. `unclear` | `limits/problems-4.json` | `p-level-annuity` | part 5.
   `tol` 0.00005 on 9.0635 (true value 9.06346). The explanation's own printed working, $\tfrac{0.181269}{0.02}$, is 9.06345 exactly: a rounding tie, and 9.0634 is refused. Dividing by 0.02 multiplies any rounding of $e^{-0.2}$ by 50, so a learner who keeps 4 places ($0.8187$) has 9.065 and is refused too. Nothing in the question says how many places to keep.
   Fix: question "Now find the true value $A(0.02) = \dfrac{1 - e^{-0.2}}{0.02}$. Keep $e^{-0.2}$ to 6 decimal places. Give pounds to 4 decimal places." Answer `tol` `{ "abs": 0.0001 }`; `accept` "9.0635: $\\tfrac{0.181269}{0.02}$, accepted as $9.0635 \\pm 0.0001$". The `wrong` values (9, 0.9901, 0.1813) stay outside.

5. `minor` | `limits/problems-5.json` | `p-impact-curve` | part 4, `wrong` `not-inverted`.
   Value 0.0031 with `tol` 0.5: the band runs from $-0.50$ to 0.50. A typed 0.4 (part 2's answer), 0.002 or 0 is told "That is $p'(273.15)$", which is false for each.
   Fix: `"tol": { "abs": 0.0005 }` on that entry ($p'(273.15) = 0.00308$ is inside; 0.002, 0.4 and 0 are not).

6. `minor` | `integrals/problems-4.json` | `p-dish-and-spindle` | part 3.
   `tol` 0.0005 on 0.14076. The value is $\pi$ times the small difference $\tfrac53 - 1.62186 = 0.0448$. With $\ln\tfrac23 = -0.4055$, a normal 4 places, the learner has $\pi \times 0.0447 = 0.1403$, types 0.140 and is refused. This is the weaker case review a met in `p-turnover-decay`.
   Fix: answer `tol` `{ "abs": 0.001 }`; `accept` "$\\pi\\left(\\tfrac{5}{3} + 4\\ln\\tfrac{2}{3}\\right) \\approx 0.141$, accepted as $0.141 \\pm 0.001$". The `wrong` values (0.260, 0.904, 5.236) stay far outside. Part 4 is unaffected: $\tfrac{2.048}{0.140} = 14.6$ still rounds to 15.

7. `minor` | `integrals/problems-4.json` | ten more `accept` lines.
   "Any form equal to $2\ln\tfrac32$" and its like on numeric parts. The numeric field takes numbers and fractions only: `parseNum` returns NaN for `2ln(3/2)`, `2pi`, `pi^2/6`, `sqrt(2)/2`, `6pi^2`, `50/pi^2` (`grade-check.mjs --accept-lines`). Each question does ask for decimal places, so no learner is misled before answering; the line promises a form the field cannot take. Same class as review a, finding 6.
   Fix: `p-impact-kernel` part 3 "$2\\ln\\tfrac{3}{2} \\approx 0.811$, accepted as $0.811 \\pm 0.0005$"; part 4 "$2\\ln 2 \\approx 1.386$, accepted as $1.386 \\pm 0.0005$"; `p-flared-mouth` part 1 "$2\\pi \\approx 6.283$, accepted as $6.283 \\pm 0.0005$"; part 2 "$\\tfrac{\\pi^2}{6} \\approx 1.645$, accepted as $1.645 \\pm 0.0005$"; part 3 "$\\tfrac{\\pi^2}{2} \\approx 4.935$, accepted as $4.935 \\pm 0.0005$"; part 4 "$\\tfrac{\\sqrt{2}}{2} \\approx 0.707$, accepted as $0.707 \\pm 0.0005$"; `p-dish-and-spindle` part 2 "$2\\pi(2 + \\ln 3 - 4\\ln 2) \\approx 2.048$, accepted as $2.048 \\pm 0.0005$"; `p-rubber-seal` part 1 "$\\tfrac{\\pi}{2} \\approx 1.571$, accepted as $1.571 \\pm 0.0005$"; part 3 "$6\\pi^2 \\approx 59.22$, accepted as $59.22 \\pm 0.005$"; part 5 "$\\tfrac{50}{\\pi^2} \\approx 5.07$, accepted as $5.07 \\pm 0.005$". (`p-dish-and-spindle` part 3 is in finding 6.)

8. `minor` | `integrals/problems-4.json` | `p-impact-kernel` | part 1, `byKey` `unit-rule`.
   "$\tfrac{1}{1 - p}$ is the value on $[0, 1]$." With $p = \tfrac12$ that is 2; the entry is 1, the bound $\tfrac12 \times 2$ on $[0, 1]$. The line names a number the learner did not type.
   Fix: `"unit-rule": "1 is the bound on $[0, 1]$: $\\tfrac{1}{2} \\times \\tfrac{1}{1 - p}$ with $p = \\tfrac{1}{2}$. Here the range is $[0, 4]$, so use $\\big[\\sqrt{t}\\big]_0^4$."`

9. `minor` | `integrals/problems-4.json` | `p-dish-and-spindle` | part 4, `wrong` `inverse`.
   Value 0.0687 with `tol` 0.5: any entry from $-0.43$ to 0.57 is told "You divided the spindle by the dish", among them a carried 0.141 or 0.326.
   Fix: `"tol": { "abs": 0.005 }` on that entry.

10. `minor` | `multivar/problems-4.json` | `p-corner-sprinkler` | part 1 (the author's first reported loose chain).
    Judgement: it does not meet the brief. Part 1's answer $\sqrt{9 - x^2}$ is used by no later part; part 2 starts again in polar. Parts 2 to 5 are a real chain of four, so the item is sound without it, and the set keeps l14 through `p-weighted-rectangle` parts 3 and 4.
    Fix: replace part 1 with a step that part 2 uses. Question "The depth depends only on the distance $r$ from the sprinkler. Write the depth $d$ as a function of $r$." Widget `expression`, answer `9-r^2`, `accept` `["9-r^{2}", "(3-r)(3+r)"]`, `wrong` `[{ "id": "r-not-squared", "tex": "9-r" }, { "id": "with-r", "tex": "9r-r^3" }]`. Feedback: `correct` "$x^2 + y^2 = r^2$, so $d = 9 - r^2$."; `generic` "Not quite. Write $x^2 + y^2$ in polar."; `r-not-squared` "You wrote $x^2 + y^2$ as $r$. It is $r^2$."; `with-r` "That already carries the area factor $r$. The depth alone is $9 - r^2$." `explain` "In polar $x^2 + y^2 = r^2$, so the depth is $9 - r^2$. It is 9 mm at the sprinkler and 0 at the edge $r = 3$." Part 2 question "Using the depth $9 - r^2$ from part 1: the quarter disc is $0 \le r \le 3$, $0 \le \theta \le \tfrac{\pi}{2}$. Write the depth times the area factor, the integrand of $dr\,d\theta$, as a function of $r$." The item then draws on l15 and l13 (an inner integral free of $\theta$ multiplies out).

11. `minor` | `multivar/problems-4.json` | `p-drone-landing` | freshness.
    Lesson l16 asks "What constant $c$ makes $c\,e^{-x^2/8}$ a density?" (answer $\tfrac{1}{2\sqrt{2\pi}}$). Part 1 here integrates the same $e^{-x^2/8}$ and its answer $\sqrt{8\pi}$ is that key's reciprocal. Parts 2 to 5 (the plane, polar, the 90% radius) are new. The brief bars a lesson's numbers.
    Fix (all in `proposed.py`): density $c\,e^{-(x^2 + y^2)/32}$, so $\sigma = 4$; 18 is taken by `homework-4`.
    - Part 1: $x = 4\sqrt2\,u$; answer $\sqrt{32\pi} = 10.0265$. `no-scale` 1.7725, `inverted` 0.3133, `sigma-root8` (rename `sigma-root32`) 14.1796; the bell has $\sigma = 4$ and the integral is $4\sqrt{2\pi}$.
    - Part 2: `32\pi`; `not-squared` `\sqrt{32\pi}`, `doubled` `2\sqrt{32\pi}`, `carried` `\pi`.
    - Part 3: `\frac{1}{32\pi}` ($\approx 0.0099$); `not-inverted` `32\pi`, `from-root` `\frac{1}{\sqrt{32\pi}}`, `carried` `\frac{1}{\pi}`.
    - Part 4: "within 4 m": $\int_0^4 e^{-r^2/32}\,r\,dr = 16(1 - e^{-1/2})$, answer 0.3935 as now. `r-not-squared` 0.1175 ($1 - e^{-4/32}$), `no-2pi` 0.0626, `outside` 0.6065.
    - Part 5: $P = 1 - e^{-a^2/32}$, 0.3935 at $a = 4$; $a = \sqrt{32\ln 10} = 8.58$. `no-root` 73.68, `tail-swap` 1.84, `log10` 5.66. "A little more than doubles" still holds ($8.58 / 4 = 2.15$).

12. `minor` | engine, met in `limits/problems-4.json` | `p-barbell-hedge` | part 1.
    The correct form $-\tfrac{100}{e^{2u}} - \tfrac{400}{e^{8u}} + \tfrac{500}{e^{5u}}$ is refused. The likely cause: at $u = 2.9$, inside the sampling range, the Compute Engine returns exactly 0 for $400e^{-8u}$ but $3.4 \times 10^{-8}$ for $\tfrac{400}{e^{8u}}$, a gap wider than the grader's $10^{-9}$ band (`probe-e8u.mjs`). `exprs.mjs` shows the refusal for $e^{8u}$ and $e^{9u}$ with the factor 400, not for $e^{7u}$, $e^{10u}$ or the factor 4. The key's own form, any reordering of it and the factored $-100(\ldots)$ grade correct, so the usual learner is safe. No content edit; see Engine.

### Per problem

- Chains. Every problem but `p-corner-sprinkler` (finding 10) and `p-signal-decay` (finding 2) has each part's result used later, and every last part asks for the result the problem is about. Nine parts use no earlier answer and feed a later one: `p-level-annuity` 2, `p-camera-pan` 3, `p-impact-kernel` 2, `p-flared-mouth` 2, `p-dish-and-spindle` 2, `p-rubber-seal` 2, `p-dome-tent` 2, `p-three-strategies` 4, `p-triangle-field` 4. All acceptable, as in review a: each is a second result that a later part joins to the first.
- `p-triangle-field` part 4 (the author's second reported loose chain). Judgement: it meets the brief. It is a second branch, and part 5 needs both branches (the average from parts 1 to 3 and the largest value from part 4) and restates both. No edit.
- Later parts restate what they need: yes. The rounded hand-offs give answers inside the bands: $0.811 / 1.386 = 0.5851$ (`p-impact-kernel` 5), $2.0485 / 0.1408$ and $2.048 / 0.141$ both round to 15 (`p-dish-and-spindle` 4), $\ln 20 = 2.9957$ gives 122.74 (`p-signal-decay` 4), 273.15 gives 324.61 (`p-impact-curve` 4).
- Answer form. Every numeric part with a non-whole answer names its form. 16 parts with a whole-number answer and `tol` 0 do not say "whole number" (limits 4: nine; limits 5: four; integrals: one; multivar 5: two); none refuses a sensible entry. Stored keys that are themselves rounded (1.3333, $-0.1667$, 0.6667, 2.1333, 0.5333, 2.3704, 5.0133, 31.81) take both the exact fraction and the rounding.
- `wrong` entries: every one differs from its answer and from its neighbours, and every one is the value its named slip gives (202 entries: 161 numeric and 41 `wrong[].tex`, all rebuilt in `mine.py`). Carried slips are present where a learner would carry one. `p-spread-quote` part 1 `product-of-derivatives` is $900 \times \tfrac{d}{ds}(2+s)^{-2}$; its line "You multiplied the two derivatives" is true of that product form.
- The three choice parts are judgements (which way the curve bends, where the best allowed point lies, why Pappus's product appears). No option, `why` or feedback line names an option by place, and no key stands out by length.
- `p-level-annuity` part 4 writes $A'(0) = -50$ for the limit of $A'$ found in part 3. For the curve filled in at $r = 0$ that is its slope there. No edit.

Clean problems (8 of 17): limits set 4 `p-spread-quote`; set 5 `p-camera-pan`; integrals set 4 `p-flared-mouth` and `p-rubber-seal` (bar their `accept` lines, finding 7); multivar set 4 `p-weighted-rectangle`; set 5 `p-three-strategies`, `p-dome-tent`, `p-triangle-field`.

### Per set

- Lessons. Every lesson of each level is drawn on, and each problem draws on at least two. Limits 4: l13 (`p-spread-quote`, `p-signal-decay`, `p-barbell-hedge`), l14 (`p-spread-quote` 4), l15 (`p-spread-quote` 5, `p-barbell-hedge`, `p-level-annuity` 4), l16 (`p-signal-decay`, `p-level-annuity`). Limits 5: l17 (`p-camera-pan` 4, `p-app-adoption` 5), l18 (all three), l19 (`p-camera-pan`, `p-impact-curve`), l20 (`p-app-adoption`, `p-impact-curve` 3). Integrals 4: l14 (`p-impact-kernel`, `p-dish-and-spindle`), l15 (`p-flared-mouth`, `p-rubber-seal`), l16 (`p-impact-kernel`, `p-flared-mouth`), l17 (`p-flared-mouth`, `p-dish-and-spindle`, `p-rubber-seal`). Multivar 4: l13 and l14 (`p-weighted-rectangle`), l14 and l15 (`p-corner-sprinkler`), l13, l15 and l16 (`p-drone-landing`); l16 rests on that one problem. Multivar 5: l17 (`p-dome-tent`, `p-triangle-field`), l18 (`p-three-strategies`, `p-dome-tent`), l19 (`p-three-strategies`), l20 (`p-three-strategies`, `p-triangle-field`). Nothing is used before its level: the second-order estimate is not needed (finding 3), the logistic law is given, and $\int e^{-u^2}\,du = \sqrt\pi$ is given.
- Difficulty. One 5 in each set (`p-level-annuity`, `p-camera-pan`, `p-dish-and-spindle`, `p-drone-landing`, `p-three-strategies`), and each earns it. Typed parts 75 of 78.
- Freshness. Gate clean. My own reading: the zero-coupon bonds of limits l10, l18, `review-3` and `homework-3` are one bond's slope each (`homework-3` has $100e^{-5y}$ along a yield path), and none is a hedged book of three; market impact in l14 and `review-4` is a quadratic cost, not an $\arctan$ curve; the radar item of `review-5` is a slant distance, not an angle; the horn of integrals l17 is $\tfrac1x$; l14's $(x+1)(x+2)$ carries a bare 1 on top and no solid; multivar l17's stretched discs use $x = 2u$, $y = 3v$ and $x = 4u$, $y = \tfrac v2$ with no height over them; l18's tent is a ridge over a square; quarter discs in l15 and `review-4` have radius 1 and 2 with integrands $x$ and $xy$. One real hit: finding 11.
- Voice. British spelling, no exclamation marks, no em-dashes, £ and pence for money, explanations of at most three sentences (`forms.py` and `voice-scan.py 35`: 0 and 0).

### Engine

- Expression grader: a term that is tiny on part of the sampling range (here $400e^{-8u}$ for $u$ near 3) can evaluate to exactly 0 in one written form and to its true $10^{-8}$ value in another, so two equal forms are told apart. Seen with $\tfrac{400}{e^{8u}}$ against $400e^{-8u}$ and with $e^{9u}$; `probe-e8u.mjs` prints the values. A relative band on each term, or a sampling range a key can narrow, would cure it. Not appended to `docs/BACKLOG-INBOX.md` by this reader (findings only).
- Validator rule worth adding: a numeric part whose `accept` string says "Any form equal to" a value that is not a ratio of whole numbers. Review a found five, this review eleven.
- Validator rule worth adding: a `wrong[]` entry whose band is wider than its own value (findings 5 and 9).

### Counts

| tag | limits | integrals | multivar | tooling | total |
|---|---|---|---|---|---|
| `wrong` | 0 | 0 | 0 | 0 | 0 |
| `unclear` | 2 | 0 | 0 | 0 | 2 |
| `minor` | 3 | 4 | 2 | 1 | 10 |

### Verdict by set

| set | verdict |
|---|---|
| limits `problems-4` | sound; findings 2, 3, 4 (and 12, engine) |
| limits `problems-5` | sound; findings 1, 5 |
| integrals `problems-4` | sound; findings 6, 7, 8, 9 |
| multivar `problems-4` | sound; findings 10, 11 |
| multivar `problems-5` | clean; no edit |

One fix pass on Sonnet covers all of it. Findings 10 and 11 change graded answers (a new part 1 for the sprinkler, new numbers through the drone item), so a delta reader should recompute those two items and the author's script needs the same edits; the rest change bands and text only.

### Scripts (`docs/reviews/problems-1.3-c-scripts/`)

| file | what it does | run |
|---|---|---|
| `mine.py` | the reader's own answer and named-slip value for every numeric and expression part, two methods each, and the claims above | `<venv>/bin/python`, exit 0 |
| `grade-check.mjs` | the engine's graders on every answer, `accept`, `wrong` and 142 typed strings; `--accept-lines` for finding 7 | `node ... --local-cdn <pkgs>`, exit 0, 1 FINDING row, 2 NOTE rows |
| `proposed.py` | the numbers of every fix above, twice; item skills against lesson skills | `<venv>/bin/python`, exit 0 |
| `exprs.mjs`, `probe-e8u.mjs` | finding 12: which forms the grader refuses, and what the Compute Engine returns for each | `node ... --local-cdn <pkgs>` |
| `taught.py` | per lesson, counts of each idea a set leans on; `--show` prints the passages | `python3` |
| `forms.py` | parts and kinds, form sentences, explanation length, wide `wrong` bands, restated values, "Any form" lines | `python3` |
| `fresh-grep.py` | each setup's formula and nouns across the course and the exams | `python3` |
| `dump.py` | compact dump of a set for reading | `python3` |

All run from the repo root.
