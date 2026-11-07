# Quadratics levels 1 to 3 (Factorising; Solving; Parabolas): second-reader findings

Scope: `app/content/courses/quadratics/` l1 to l13, `review-1` to `review-3`, `homework-1` to `homework-3` (the whole course). Stage 0 (0.2), read for a GCSE-entry learner against `course.json` `requires` (number-sense, equations, functions). Continuity skim of every outside reference to the course: complex l1 (the $(x - 2)^2 = -1$ opener matches l8 `screens[0]`), algebra l14 ("zero product rule (`quadratics` l5)" matches l5's summary name), and the `requires` lines of trig, eigen and limits. All hold.

There is no course brief (`docs/briefs/quadratics.md` or `gap-quadratics.md`) and no author report (`docs/reports/quadratics-<n>.md`): the course predates both. I read against `course.json` (`lessonObjectives`), `docs/curriculum.md` 0.2 and AUTHORING.

Method: every graded key, every `wrong[]` value and every number in prose, hints, feedback, explanations, tables and canvas captions recomputed in three committed scripts. Each number is computed two ways: method 1 is exact polynomial arithmetic (a small Fraction parser), the formula or the vertex rule; method 2 is values at sample points, bisection, a fine scan for extremes or brute-force counting. Every choice option written as a polynomial is expanded and compared with the target, or with the expansion its `why` claims ("That expands to ..."). Every claim was read against the screen it sits on. Wrong claims are coded with `lv.stated()`, so they fail now and pass once reworded. The two `expression` items (l13 `screens[2]` and `screens[7]`) were graded on the real `grade.js` and `expression.js` with Compute Engine 0.30.2, against 34 learner forms (scratch harness `expr-test.mjs`). There are no code items in the course.

Tool results:
- `python3 docs/reports/quadratics-L1-numbers.py`: exit 1, 399 of 402. The 3 failures are findings 1, 2 and 3, each failing because the content is wrong. 26 "check by hand" lines, each read: every wrong value matches its slip.
- `python3 docs/reports/quadratics-L2-numbers.py`: exit 1, 369 of 373. The 4 failures are findings 5, 6, 8 and 12. 32 "check by hand" lines read; the only mismatch is finding 6.
- `python3 docs/reports/quadratics-L3-numbers.py`: exit 1, 269 of 271. The 2 failures are findings 13 and 14. 36 "check by hand" lines read; the l12 `equal` line states a variance (0.0125) for a weight slip (0.5), which is fine.
- `cd app && node tools/validate.mjs`: 0 errors. The 17 quadratics warnings are:
  - 6 `key-length`: l4 `screens[6]`, l5 `screens[7]`, l8 `screens[6]`, l12 `screens[1]` and `screens[5]`, homework-3 `items[5]`. Finding 18 covers the five that really give the answer away; l12 `screens[5]` ("Every $x$ except 3" against "Every $x$") does not.
  - 1 `shuffle-false`: l10 `screens[6]`. Its options are the ordered numbers 12, 6, 3, −3, so no change.
  - 4 `O2-explain-answer`: l9 `screens[9]` and homework-3 `items[6]` are finding 19. l12 `screens[4]` lists the five numbers and homework-3 `items[4]` says "six of them", so no change.
  - 6 ladder-canvas notes: l1 s4, l2 s3 and s5, l3 s3 and s4, l4 s5. A table beside an area model of the same numbers, so no change.
- `VOICE_BASE=app/content/courses/quadratics python3 docs/reviews/voice-scan.py 35`: 0 sentences over 35 words, 0 explanations over three sentences. My own scan of L1 to L3: no exclamation marks, no em-dashes, no American spellings, £ throughout, and no option named by its place.
- `node tools/playthrough.mjs` with the 13 `--lesson` and 6 `--set` targets and `--local-cdn <scratchpad>/pkgs`: "All passed", 19 of 19 desktop and 19 of 19 with `--mobile`, 0 browser relaunches.
- Screenshots: I looked at 6 of the 274 `--shots` images (l6 s4, l7 s4, l12 s9, l13 s6, homework-3 item 6, and others). Layout is clean except one engine fault (Engine 3).
- `node tools/fresh-check.mjs --file content/courses/quadratics/<set>.json --min-run 10`: 3 hits, which are findings 20, 21 and 22. Grepping the key nouns added the reused setups in findings 23 to 26.
- Expression items: both keys accept the equivalent forms a learner would type and return the named slips. For l13 `screens[2]`, `-20p^2+800p` and `800\cdot p-20\cdot p^2` pass; `p(800-20p)`, `20p(40-p)` and `-20p(p-40)` return `form`; `800p+20p^2` returns `plus` and `800-20p` returns `no-p`. For l13 `screens[7]`, `\frac{A}{2\cdot B}`, `0.5\frac{A}{B}`, `\frac{A}{B}\div2` and `A/(2B)` pass; `\frac{A}{B}` returns `choke`, and `-\frac{A}{2B}` and `\frac{-A}{2B}` return `minus`. One input slip gets only the generic line (finding 17). No expression item in the course asks for a factorised form, a surd or a ± answer: all of those are `choice` items. So factor order, surd forms and ± forms are untested by grading. A probe shows a ± key would reject equal forms (Engine 1).

Format: `N. file | JSON path | severity | problem | evidence | exact fix`. Severities: wrong, misleading, voice, layout, continuity. Fix text is the string value; double each backslash when writing it into JSON.

## Findings

1. l1-two-brackets.json | `quiz[2].widget.options[1].why` (`each-squared`, option $r^2 - m^2$) | misleading | "You squared each term" describes the other distractor. Squaring each term of $r - m$ gives $r^2 + (-m)^2 = r^2 + m^2$, which is option `dropped-middle`, whose why says the same. | L1 script: `lv.stated` fails (with $m = 3$, $r^2 + 9 \ne r^2 - 9$). | "You squared $r$ and $m$ and kept the minus between them. The two $-mr$ strips are missing, and the corner is $(-m)^2 = +m^2$."

2. l2-product-and-sum.json `quiz[1].explain.text`; review-1.json `items[2].explain.text` | misleading | "the sum is $-1$, so the larger number is negative": the numbers are $-5$ and 4, and the larger of them is 4. The rule meant is "the one further from zero". review-1 uses the same phrase with "positive". | L1 script: `lv.stated` fails on l2 (max(−5, 4) = 4 > 0). | l2: "The product is $-20$, so the signs differ. The sum is $-1$, so the number further from zero is negative: $-5$ and 4 work, and $x^2 - x - 20 = (x - 5)(x + 4)$." review-1: "The product is negative, so the signs differ. The sum is positive, so the number further from zero is positive: 7 and $-4$ work, and $x^2 + 3x - 28 = (x + 7)(x - 4)$."

3. l4-difference-of-squares.json `summary.trap`, `summary.ideas[2]`, `screens[6].feedback.correct`, `quiz[3].widget.options[3].why`; homework-1.json `items[8].model` | wrong | "A sum of two squares has no factors at all" is false as a rule. $4x^2 + 36 = 4(x^2 + 9)$ and $2x^2 + 8 = 2(x^2 + 4)$ are sums of two squares with a common factor, and the same lesson's `screens[5]` teaches "check for a common factor before you decide something will not factorise". What is true is that $x^2 + 9$ (monic, no common factor) has no bracket factors. | L1 script: `lv.stated` fails ($4x^2 + 36 = 4(x^2 + 9)$). | summary.trap: "$x^2 + 9$ is not $(x + 3)^2$, which is $x^2 + 6x + 9$. No two numbers have product 9 and sum 0, so $x^2 + 9$ has no bracket factors." summary.ideas[2]: "Take out a common factor first. $x^2 + 9$, a sum of two squares, has no bracket factors." feedback.correct: "$x^2 + 9$ has no bracket factors." quiz[3] option `d` why: "That is a sum of two squares. No two numbers have product 25 and sum 0." homework-1 model, last sentence of (d): "So no such brackets exist, and $x^2 + 16$ does not factorise." (Finding 18 shortens the same screen's correct option.)

4. l5-product-of-zero.json `screens[2].prose`; l11-meeting-the-axis.json `screens[2].prose`, `screens[5].explain.text` | continuity | **roots** is bolded as new in l5 `screens[1].explain` and again in l5 `screens[2].prose`. l11 then bolds **roots** a third time as if new. l11 `screens[5]` bolds **repeated root**, which l5 `screens[5]` already named. The real new term in l11 `screens[2]`, the $y$-intercept, is not bolded. | l5 `screens[1].explain.text`: "These values of $x$ are the **roots**". | l5 `screens[2].prose`: "A root is a value of $x$ that makes the quadratic zero. A product is zero when one of its factors is zero. We use that to solve $(x + 3)(x - 7) = 0$." l11 `screens[2].prose`: "As in lesson 5, the $x$ values where a curve meets the $x$-axis are its roots. The height where it meets the $y$-axis, at $x = 0$, is its **$y$-intercept**. Here is $y = (x + 2)(x - 4)$." l11 `screens[5].explain.text`, middle sentence: "The two roots have merged into the repeated root of lesson 5."

5. l6-completing-the-square.json | `screens[4].explain.text`; `screens[4].feedback.correct` | layout | The explanation reads "So $x = -1$ or $x = -5$\; check: ...". The `\;` sits outside the `$` signs, so the learner sees a literal backslash and semicolon. This is also where ± first appears, undefined. No number-sense, equations or functions lesson required by L2 defines the symbol. Number-sense l11 `quiz[3]` teaches that $x^2 = 49$ gives 7 or $-7$, but never writes ±. | L2 script: `lv.stated` fails on `$\; check`. Raw string: `"... $x = -5$\\; check: $1 - 6 + 5 = 0$."` | explain: "$(x + 3)^2 = 4$ means $x + 3 = 2$ or $x + 3 = -2$, written $x + 3 = \pm 2$ and read plus or minus 2. So $x = -1$ or $x = -5$. Check $x = -1$: $1 - 6 + 5 = 0$." feedback.correct: "$x + 3 = \pm 2$, meaning 2 or $-2$, so $x = -1$ or $x = -5$."

6. l6-completing-the-square.json | `screens[5].widget.wrong[2]` (`whole`, $-1$); `screens[5].feedback.byKey.whole` | wrong | The line "You used the whole 3 as the corner's side" cannot produce $-1$. With side 3, $(x + 3)^2 - 9 - 4 = 0$ gives $x = -3 \pm \sqrt{13}$, about 0.61 or $-6.61$. A learner who types $-1$ has flipped the sign of the root 1, and is told something false. | L2 script: `lv.stated` fails; $-3 \pm \sqrt{13} \ne -1$. | Rename the id `whole` to `flip` in both places. `"flip": "You flipped a sign. $x + 1.5 = 2.5$ gives $x = 1$; the negative root comes from $x + 1.5 = -2.5$."`

7. l6-completing-the-square.json | `quiz[2].feedback.byKey.sign` ($-3$) | misleading | "You used $x + 5$": with $(x + 5)^2 = 4$ the roots are $-3$ and $-7$, so a learner asked for the smaller root would give $-7$. Typing $-3$ is more simply a flipped sign on the root 3. | $(x + 5)^2 - 25 + 21 = 0$ gives $x = -5 \pm 2$. | "You flipped the sign. $(x - 5)^2 = 4$ gives $x - 5 = \pm 2$, so $x = 3$ or $x = 7$."

8. l7-the-formula.json | `screens[0].widget.options[2].why` (`noroot`) | wrong | "The 5 is a square, so $x + 2 = \sqrt{5}$": 5 is not a square number. The intended sense is that $(x + 2)^2$ equals 5. To a GCSE-entry learner the sentence states a false fact. | L2 script: `lv.stated` fails (5 is not a perfect square). | "You set $x + 2 = 5$. It is $(x + 2)^2$ that equals 5, so $x + 2 = \pm\sqrt{5}$."

9. l5, l7, review-2, homework-2 (every surd in the course: list below) | continuity | No Stage 0 lesson defines a surd, an "exact" root, or $\sqrt{ab} = \sqrt{a}\sqrt{b}$ (this is review-number-sense-1-3 finding 30, where the `course.json` why line was already corrected). Number-sense l11 teaches $\sqrt{n}$ as a number to estimate ($\sqrt{20}$ between two decimals), so a bare $\sqrt{5}$ is readable. Two things are untaught: leaving a root as an exact answer, and simplifying one. Four places simplify. In l7 `quiz[0]` and `quiz[3]` the learner must simplify to find the key among the options; review-2 `items[5]` is reachable by completing the square. L1 and L3 use no surds.

   Every use (S marks a simplification):
   - l5 `screens[6]` option `root` ($\sqrt{5}$, a distractor).
   - l7 `screens[0]`: options, hints[2], feedback, explain ($-2 \pm \sqrt{5}$); the first exact root.
   - l7 `screens[2]` accept, hints, feedback, explain ($3 \pm \sqrt{5}$).
   - l7 `screens[3]` accept, feedback, explain ($-2 \pm \sqrt{2.5}$).
   - l7 `screens[4]` and `screens[7]`: the formula; `screens[7].explain` ($\tfrac{-3 \pm \sqrt{17}}{4}$).
   - l7 `screens[8]` accept, hints, feedback, explain ($\tfrac{7 \pm \sqrt{29}}{2}$).
   - l7 `quiz[0]` options, why, feedback, explain (S: $\sqrt{12} = 2\sqrt{3}$).
   - l7 `quiz[3]` options, whys, feedback, explain (S: $\sqrt{8} = 2\sqrt{2}$, "half of $\sqrt{8}$ is $\sqrt{2}$").
   - l8 `screens[2].explain` ($\sqrt{-8}$, to say it does not exist).
   - review-2 `items[1]` option ($\pm\sqrt{3}$), `items[4]` ($\tfrac{3 \pm \sqrt{41}}{4}$), `items[5]` (S: half of $\sqrt{8}$).
   - homework-2 `items[4]` ($\sqrt{\Delta}$), `items[5]` (S: $\tfrac{6 \pm \sqrt{52}}{2} = 3 \pm \sqrt{13}$).

   The graded answers of l7 `screens[2]`, `screens[3]`, `screens[8]`, review-2 `items[4]` and homework-2 `items[5]` are already decimals, so the decimal alternative is in place there. Exact surd answers are graded only in l7 `quiz[0]`, l7 `quiz[3]` and review-2 `items[5]`. | `grep -il surd` over number-sense, equations and functions: no hits. No `\sqrt{12} = 2\sqrt{3}` pattern before l7. | Smallest fix: a definition at first use, plus a squaring check at each simplification. No level is added.
   - (a) l7 `screens[0].explain.text`: "$x + 2 = \pm\sqrt{5}$, so $x = -2 \pm \sqrt{5}$: about 0.24 and $-4.24$. A root such as $\sqrt{5}$, left unrounded, is exact and is called a **surd**. Completing the square solves quadratics that will not factorise."
   - (b) l7 `quiz[0].prose`: "Solve $x^2 + 2x - 2 = 0$ with the formula. You may need $\sqrt{12} = 2\sqrt{3}$: check that $(2\sqrt{3})^2 = 4 \times 3 = 12$."
   - (c) l7 `quiz[3].prose`: "Solve $x^2 - 6x + 7 = 0$ with the formula. You may need $\sqrt{8} = 2\sqrt{2}$: check that $(2\sqrt{2})^2 = 4 \times 2 = 8$."
   - (d) review-2 `items[5].widget.options[2].why`: "You halved the 2 but not $\sqrt{8}$. Since $\sqrt{8} = 2\sqrt{2}$, half of it is $\sqrt{2}$." review-2 `items[5].feedback.correct`: "$(x - 1)^2 = 2$, so $x = 1 \pm \sqrt{2}$." review-2 `items[5].explain.text`: "Completing the square: $(x - 1)^2 = 2$, so $x = 1 \pm \sqrt{2}$. The formula agrees: $\tfrac{2 \pm \sqrt{8}}{2}$, since $\sqrt{8} = 2\sqrt{2}$."
   - (e) homework-2 `items[5].explain.text`: "Multiplying by $-2$ gives $t^2 - 6t - 4 = 0$, so $t = \tfrac{6 \pm \sqrt{52}}{2} = 3 \pm \sqrt{13}$, since $\sqrt{52} = 2\sqrt{13}$. Only $3 + \sqrt{13} \approx 6.61$ is after entry. The other root, $-0.61$, is outside the model's range."

10. quadratics/course.json | `levels[1].requires` | continuity | L2 solves linear inequalities, but requires only `equations/L2` (linear equations). The inequalities are l8 `quiz[2]` ($64 - 4c > 0$ gives $c < 16$), l8 `screens[9]` hints ($2500 - 4T \geq 0$), review-2 `items[7]` ($36 - 12c > 0$) and homework-2 `items[6]` ($324 - 4A \geq 0$). Inequalities are taught in `equations` L3 (l10 to l12). L3 already requires `equations/L3`. Outside my files: an orchestrator item. | equations `course.json`: L3 "Inequalities and formulae" (`l10-ranges-of-answers`, `l11-one-twist`, `l12-trapped`). | Add to quadratics L2 `requires`: `{ "ref": "equations/L3", "why": "Solves linear inequalities such as 64 − 4c > 0 to find which constants give two roots." }`

11. l8-how-many-solutions.json | `summary.formula.tex`; `summary.formula.note` | continuity | The summary writes $\Delta = b^2 - 4ac$, but no l8 screen names $\Delta$. The letter appears next in homework-2 `items[4]`, which defines it again. | l8 screens use "$b^2 - 4ac$" or "the discriminant" only. | note: "Written $\Delta$ (delta). Above 0: two roots. Equal to 0: one. Below 0: none."

12. homework-2.json | `items[4].feedback.byKey.o3` | misleading | "then the roots cancel": in this item the roots are $x_1$ and $x_2$, which are added, not cancelled. It is $+\sqrt{\Delta}$ and $-\sqrt{\Delta}$ that cancel, as the item's own explanation says. | `items[4].explain.text`: "The $+\sqrt{\Delta}$ and $-\sqrt{\Delta}$ cancel". | "You cancelled before adding. Add the two tops first; then the square roots cancel."

13. l11-meeting-the-axis.json | `screens[2].feedback.byKey.sum` (wrong value 2) | wrong | "You added the numbers in the brackets": $2 + (-4) = -2$, not 2. The value 2 comes from adding the roots, $-2 + 4$. | L3 script: `lv.stated` fails. | "You added the roots, $-2 + 4$. The intercept is the height at $x = 0$: $(0 + 2)(0 - 4) = -8$."

14. homework-3.json | `items[4].widget.wrong[2]` (`signs`, 4); `items[4].feedback.byKey.signs` | wrong | "You took the roots as 5 and $-2$" cannot give 4. The whole numbers strictly between $-2$ and 5 are $-1$ to 4, six of them: the same count as the key. So this slip is graded correct, and the line never fires on the slip it names. | L3 script: `lv.stated` fails (the count is 6, not 4). | Delete `items[4].widget.wrong[2]` (`{ "id": "signs", "value": 4 }`) and `items[4].feedback.byKey.signs`.

15. homework-3.json | `items[6].prose` | continuity | $|x|$ is used without definition. Functions defines it in l14 (L4), but quadratics L3 requires only `functions/L3`, and number-sense has no absolute value. | functions `l14-sliding.json` `screens[2].prose`: "$f(x) = |x|$, the distance of $x$ from 0". | "A straddle bought for £6.00 at strike £100.00 has expiry P&L $|x| - 6$, where $x$ is the stock's move and $|x|$ is its size, ignoring the sign. A trader fits a parabola with the same break-evens, $\pm 6$, and the same value, $-6$, at $x = 0$."

16. homework-3.json | `items[8].prose` | misleading | The formula uses $\sigma_A$, $\sigma_B$ and $\rho$, but the prose gives "volatility 10%", "20%" and "correlation 0.25" in words only. A Stage 0 learner is not told which symbol is which, or that 10% enters as 0.1. | Prose: "Asset A has volatility 10% and B has 20%, with correlation 0.25." | "Asset A has volatility $\sigma_A = 0.1$ and B has $\sigma_B = 0.2$, with correlation $\rho = 0.25$. With weight $w$ in A, $$V(w) = w^2\sigma_A^2 + (1 - w)^2\sigma_B^2 + 2w(1 - w)\rho\sigma_A\sigma_B$$"

17. l13-best-price.json | `screens[7].widget.wrong`; `screens[7].feedback.byKey` | misleading | In MathLive, typing `A/2B` gives $\tfrac{A}{2}B$, which is $\tfrac{AB}{2}$. A learner with the right idea gets only the generic line, "Find the two zero-revenue prices", which misdiagnoses a bracket slip. | Harness: `\frac{A}{2}B` returns no key (generic); `\frac{A}{2B}`, `A/(2B)` and `\frac{A}{2\cdot B}` pass. | Add to `widget.wrong`: `{ "id": "bracket", "tex": "\\frac{A}{2}B" }`. Add `"bracket": "That reads as $\tfrac{A}{2} \times B$. Type A/(2B), with the brackets, so that $2B$ sits under the line."`

18. l4 `screens[6]`, l5 `screens[7]`, l8 `screens[6]`, l12 `screens[1]`, homework-3 `items[5]` | `widget.options[*]` (the correct option) | misleading | Each key is over 1.5 times the longest distractor and carries its own proof, so length alone gives it away (advisory rule 586). l12 `screens[5]`, also flagged by the validator, is not a real giveaway and is left alone. | Validator `key-length`: 63 against 37, 82 against 47, 42 against 24, 48 against 23 and 43 against 26 characters. | l4 `options[0].text`: "No. $(x + 3)^2$ is $x^2 + 6x + 9$". l5 `options[0].text`: "Only a product of 0 forces one factor to be 0". l8 `options[0].text`: "No: the discriminant is negative". l12 `options[0].text`: "They merge into one, then vanish". homework-3 `items[5]` `options[0].text`: "Once, at $(3, 4)$". Each explanation already shows the working.

19. l9-shape-of-a-square.json `screens[9].explain.text`; homework-3.json `items[6].explain.text` | voice | Neither explanation states the answer, £101.20 or £4.50. | Validator `O2-explain-answer` on both. | l9: "The $-7d$ parts cancel: $-14$ and $+14$. The $0.3d^2$ part is $+1.2$ for both moves, because a square is never negative, so the average is £101.20. With $a = 0.3 > 0$ the curve opens upwards, so big moves either way help the holder: this is **convexity**." homework-3: "The parabola is $k(x - 6)(x + 6)$, and $-36k = -6$ gives $k = \tfrac{1}{6}$. At $x = 9$ it is $\tfrac{45}{6} = 7.50$, while $|9| - 6 = 3.00$, so it is £4.50 too high. The fit overstates big moves, because a parabola keeps steepening and the payoff does not."

20. review-2.json | `items[7].prose`, `items[7].question` | continuity | The stem repeats l8 `quiz[2]` word for word ("Look at ... For which values of ... are there two real roots?"). | `fresh-check --min-run 10`: run 11, share 1, Jaccard 1. | prose: "The curve $y = 3x^2 - 6x + c$ should cross the $x$-axis at two points." question: "Which values of $c$ make that happen?" Options, whys and key are unchanged.

21. review-2.json | `items[8]` (whole item) | continuity | This repeats l6 `quiz[1]`, two-year growth with $(1 + r)^2$ given and the yearly return asked. homework-2 `items[3]` uses the same template a third time, though as a step up (the equation is not given). | `fresh-check`: run 16, share 0.7, Jaccard 0.86. | Make it a two-year loss.
   - prose: "A car worth £20,000.00 loses the same percentage of its value each year. After two years it is worth £16,200.00. So $(1 - r)^2 = 0.81$."
   - question: "What is the yearly loss, as a percentage?"
   - widget: `answer` 0.1 (unit `%`, `tol.abs` 0.0005, `accept` "10%"); `wrong` `halved` 0.095 and `total` 0.19 (`tol.abs` 0.0005 each).
   - feedback.correct: "$1 - r = 0.9$, so $r = 10\%$ a year."
   - generic: "Not quite right. Square-root both sides, then solve for $r$."
   - byKey.halved: "You halved the 19% total. Losses compound: $0.9 \times 0.9 = 0.81$, so 10% a year."
   - byKey.total: "19% is the loss over both years. Square-root to undo the two years."
   - explain: "$1 - r = \pm 0.9$. The root $1 - r = -0.9$ gives $r = 190\%$, which would leave a negative value. So $r = 0.1$: 10% a year."
   - Checks: $20000 \times 0.9^2 = 16200$; $0.19 / 2 = 0.095$.

22. review-3.json | `items[1].prose`, `items[1].question` | continuity | The stem repeats l10 `quiz[0]` ("A curve is ... What is its vertex, and what kind of point is it?"). | `fresh-check`: run 15, share 0.68. | prose: "Without sketching, describe the turning point of $y = 3(x - 2)^2 - 5$." question: "Which description is right?" Options are unchanged.

23. review-1.json | `items[6]`, `items[7]` | continuity | Both repeat lesson transfer setups with new numbers. `items[6]` (£5,000 at 3% for two years) is l1 `screens[8]` (£2,000 at 4%), and `items[7]` (a share up 5% then down 5%) is l4 `screens[8]` (up 8% then down 8%). | Same contexts, same questions. | Two replacements:
   - `items[6]`, photo area:
     - prose: "A photo is enlarged so that each side is 3% longer. Its area grows by the factor $(1.03)^2$."
     - question: "By what percentage does its area grow?"
     - widget: `answer` 0.0609 (unit `%`, `tol.abs` 0.00005, label "Growth in area", `accept` "6.09%: $1.03^2 = 1 + 0.06 + 0.0009$"); `wrong` `simple` 0.06, `each-squared` 0.0009 and `one-strip` 0.03 (each `tol.abs` 0.00005; `one-strip` replaces `one-year`).
     - feedback.correct: "$1.03^2 = 1.0609$: the area grows by 6.09%."
     - generic: "Expand $(1 + r)^2$ as $1 + 2r + r^2$ with $r = 0.03$."
     - byKey.simple: "You counted the two strips and missed the $r^2$ corner, 0.0009."
     - byKey.each-squared: "You used $1 + r^2$, squaring each term. $(1 + r)^2$ also has two strips of $r$."
     - byKey.one-strip: "That is one strip. The square has a strip along the top and one down the side."
     - explain: "Each side is $1 + r$ times as long, so the area is $(1 + r)^2 = 1 + 2r + r^2$ times as big. With $r = 0.03$ that is $1 + 0.06 + 0.0009 = 1.0609$. The strips add 6% and the corner adds another 0.09%."
   - `items[7]`, the inverse question:
     - prose: "A share rises by $r$ and then falls by $r$, as fractions of its price. It ends exactly 1% below where it started."
     - question: "What is $r$, as a percentage?"
     - widget: `answer` 0.1 (unit `%`, `tol.abs` 0.0005, `accept` "10%: $1 - r^2 = 0.99$"); `wrong` `one-pc` 0.01 and `two-r` 0.005 (`tol.abs` 0.0005 each).
     - feedback.correct: "$r^2 = 0.01$, so $r = 10\%$: $1.1 \times 0.9 = 0.99$."
     - generic: "Up then down multiplies by $(1 + r)(1 - r) = 1 - r^2$."
     - byKey.one-pc: "You took the 1% loss as $r$. The loss is $r^2$, so $r^2 = 0.01$."
     - byKey.two-r: "You set $2r = 1\%$. The difference of squares loses $r^2$, not $2r$."
     - explain: "Up then down multiplies by $(1 + r)(1 - r) = 1 - r^2$. Ending 1% down means $r^2 = 0.01$, so $r = 0.1$. A 10% rise and a 10% fall lose 1%."

24. homework-1.json | `items[4]` | continuity | $1003^2 - 997^2$ repeats l4 `quiz[1]` ($51^2 - 49^2$): the same template, bigger numbers. | Same prompt shape and method. | Keep the title.
   - prose: "Work out $1003 \times 997$ without a calculator."
   - widget: `answer` 999991, `tol.abs` 0, `accept` "999,991 exactly: $1000^2 - 3^2$"; `wrong` `added` 1000009 and `no-corner` 1000000.
   - feedback.correct: "$(1000 + 3)(1000 - 3) = 1000000 - 9 = 999991$."
   - generic: "Write each number as 1000 plus or minus something."
   - byKey.added: "You added the 9. $(1000 + 3)(1000 - 3) = 1000^2 - 3^2$."
   - byKey.no-corner: "You dropped the $3^2$. The corner is taken away: $1000000 - 9$."
   - explain: "Write $1003 = 1000 + 3$ and $997 = 1000 - 3$. Their product is $1000^2 - 3^2 = 1000000 - 9$. So $1003 \times 997 = 999991$."

25. homework-3.json | `items[0]` | continuity | It repeats l9 `screens[9]`: a bond priced by $100 - bd + ad^2$, a symmetric move, and the average price asked. | Same context and question. | Ask where the approximation breaks instead.
   - prose: "A bond's price is approximated by $P(d) = 100 - 6d + 0.4d^2$ pounds, where $d$ is the yield move in percentage points. Real bond prices keep falling as yields rise."
   - question: "Beyond which yield move $d$ does the approximation wrongly start to rise?"
   - widget: `answer` 7.5, `tol.abs` 0.005, no unit, label "Yield move d", `accept` "7.5: $\tfrac{6}{2 \times 0.4}$"; `wrong` `minus-b` 6, `over-a` 15 and `sign` $-7.5$.
   - feedback.correct: "$d = \tfrac{6}{0.8} = 7.5$ points, where $P = 77.50$."
   - generic: "Not quite right. The price is lowest at the vertex, $d = -\tfrac{b}{2a}$."
   - byKey.minus-b: "You used $d = -b$. Divide by $2a = 0.8$ as well."
   - byKey.over-a: "You divided by $a$, not $2a$."
   - byKey.sign: "You lost a minus: $-\tfrac{-6}{0.8} = +7.5$."
   - explain: "$P$ is a parabola with $a = 0.4 > 0$, lowest at $d = \tfrac{6}{2 \times 0.4} = 7.5$, where $P = 77.50$. Beyond that the model says the price rises as yields rise, which a real bond never does. So the approximation is only used for small moves."
   - Checks: $P(7.5) = 100 - 45 + 22.5 = 77.5$, and a scan confirms the minimum.

26. l13-best-price.json `screens[9]`; homework-3.json `items[7].explain.text` | continuity | l13's transfer uses exactly l12 `screens[9]`'s portfolio, $V(w) = 0.05w^2 - 0.08w + 0.04$, and its answer, 0.8, is already stated in l12 `feedback.byKey.vertex` ("0.8 is the weight with the least variance"). | l12 `screens[9]`, l13 `screens[9]`: same assets, same $V$. | Use B at 30%.
   - l13 `screens[9]` prose: "Two uncorrelated assets: A with volatility 10%, B with 30%. Putting weight $w$ in A and $1 - w$ in B gives variance $V(w) = 0.1w^2 - 0.18w + 0.09$."
   - canvas: `y` [0, 0.1]; `functions[0].expr` "0.1*x^2 - 0.18*x + 0.09".
   - widget: `points[0].target` [0.9, 0.009]; `wrong` regions `equal` x [0.45, 0.55] and `swapped` x [0.05, 0.15], both y [0, 0.1].
   - hints[1]: "$w = -\tfrac{b}{2a} = \tfrac{0.18}{2 \times 0.1}$."
   - hints[2]: "$w = 0.9$: 90% in A and 10% in B."
   - feedback.correct: "$w = 0.9$, with variance 0.009."
   - byKey.equal: "Equal weights give $V = 0.025$. Tilting towards the calmer asset A lowers it further."
   - byKey.swapped: "You put 90% in B, the riskier asset. The vertex is at 0.9 in A."
   - explain: "The vertex is at $w = \tfrac{0.18}{2 \times 0.1} = 0.9$. There $V = 0.009$, a volatility of about 9.5%, below either asset alone. Because the assets are uncorrelated, their moves partly cancel." explain.canvas: P at (0.9, 0.009), label "(0.9, 0.009)".
   - homework-3 `items[7].explain.text`, last sentence: "With 0.01 and 0.09 that is 0.9, as in lesson 13."
   - Checks: $0.01w^2 + 0.09(1 - w)^2$ expands to $0.1w^2 - 0.18w + 0.09$; $V(0.9) = 0.009$; $\sqrt{0.009} = 0.0949$; $V(0.5) = 0.025$.

## Continuity

Notation is steady across the 13 lessons:
- Brackets are expanded as four area pieces (square, two strips, corner) throughout, and "strip" and "corner" carry into completing the square (l6) and the formula (l7).
- The product-and-sum rule (l2) is reused for $ac$ (l3) and for the zero middle term (l4).
- Roots, intercept, vertex and line of symmetry keep one meaning each. Lessons cite each other as "lesson 4" and "the roots lesson".
- Money is £ to the penny, and inequalities use $<$, $\le$ and $\ge$.

Every in-course cross-reference was checked: l1 `quiz[1]` "comes back in lesson 4"; l4 `screens[7]` "from lesson 2"; l6 `quiz[3]` and l8 `screens[0]` (a square equal to a negative); l8 `screens[5]` "The ± from the last lesson"; l10 `screens[6]` "Last screen"; l11 `screens[5]` "the discriminant test"; l13 `screens[3]` "the midpoint rule from the roots lesson". All hold.

Stage 0 knowledge: number-sense L2 and L3 cover negatives times negatives, powers and square roots, including both signs of a square root (l11 `quiz[3]`). Equations L1 covers expanding and common factors; L2 covers linear equations; L3 covers inequalities (finding 10). Functions L3 covers reading curves. Not covered anywhere before use:
- surds and exact roots (finding 9);
- the ± symbol (finding 5);
- linear inequalities in L2 (finding 10);
- $|x|$ (finding 15);
- the portfolio symbols (finding 16).

homework-1 `items[7]` uses $\tfrac{1}{n}\sum_i$ and $\overline{x^2}$ but defines both in its prose, so no change.

## Engine

1. Expression grader: a key written with `\pm` is compared as one expression, not as the pair of values. On the real `grade.js` with Compute Engine 0.30.2, `\frac{-2\pm\sqrt{12}}{2}` is graded wrong for the key `-1\pm\sqrt{3}`, and `-1+\sqrt{3}` is graded wrong too. No item uses a ± key today. If the surd choices in finding 9 ever become entry items, the grader needs to compare $\{a + b, a - b\}$ as a set.
2. Expression grader: `form: "simplified"` on a surd constant is inconsistent. It refuses `\frac{-2+\sqrt{12}}{2}` for `-1+\sqrt{3}`, but accepts `3+\frac{\sqrt{8}}{2}` for `3+\sqrt{2}`, because Compute Engine canonicalises $\tfrac{\sqrt{8}}{2}$ at parse. So the form cannot yet demand a simplified surd.
3. Plane canvas: a y-axis tick label's white halo hides the curve where the curve passes behind it. In homework-3 `items[6]`, the "−5.0" label cuts the expiry-P&L line near $x = -1$ (desktop screenshot `quadratics_homework-3-item-06.png`).

These three are also appended to `docs/BACKLOG-INBOX.md` under "Raised later (review quadratics L1 to L3)". Finding 10 is an orchestrator item (`course.json`).

## Fix pass

1. fixed: l1 quiz[2] option `each-squared` why now describes keeping the minus (squaring each term gives $r^2 + m^2$, the other option).
2. fixed: l2 quiz[1] and review-1 items[2] now say "further from zero". Basis: for $x^2 + bx + c$ with $c < 0$ the roots' sum is $b$, so the larger magnitude takes the sign of $b$.
3. fixed: l4 trap, ideas[2], screens[6] feedback, quiz[3] option d, homework-1 items[8] model. Basis: $4x^2 + 36 = 4(x^2 + 9)$, and $x^2 + 9$ has no integer pair with product 9 and sum 0 (checked by script).
4. fixed: l5 screens[2] unbolds root; l11 screens[2] bolds y-intercept; l11 screens[5] cites the repeated root of lesson 5.
5. fixed: l6 screens[4] explain and feedback define ± at first use and drop the stray `\;`. Basis: $x + 3 = \pm 2$ is shorthand for the two cases 2 and $-2$.
6. fixed: l6 screens[5] `whole` renamed `flip`, text rewritten. Recomputed: $x^2 + 3x - 4$ has roots 1 and $-4$; $-1$ is the root 1 with its sign flipped.
7. fixed: l6 quiz[2] `sign` now "You flipped the sign". Recomputed: $(x - 5)^2 = 4$ gives 3 and 7.
8. fixed: l7 screens[0] `noroot` why. Recomputed: $(x + 2)^2 = 5$.
9. fixed at smallest scope: surd defined at l7 screens[0] explain; squaring checks added to l7 quiz[0] and quiz[3] prose, review-2 items[5] (why, correct feedback, explain) and homework-2 items[5] explain. No screens or levels added. Basis: $(2\sqrt{3})^2 = 12$, $(2\sqrt{2})^2 = 8$, $(2\sqrt{13})^2 = 52$ (script). Surd is the standard term (Edexcel GCSE 9-1 Maths, Number, surds).
10. fixed (orchestrator): `course.json` L2 `requires` equations/L3; not touched here.
11. fixed: l8 summary formula note defines $\Delta$.
12. fixed: homework-2 items[4] o3 feedback.
13. fixed: l11 screens[2] `sum` feedback ($-2 + 4$).
14. fixed: homework-3 items[4] `signs` wrong value and feedback deleted (the slip counts 6, the same as the key).
15. fixed: homework-3 items[6] prose defines $|x|$.
16. fixed: homework-3 items[8] prose names $\sigma_A = 0.1$, $\sigma_B = 0.2$, $\rho = 0.25$.
17. fixed: l13 screens[7] `bracket` wrong (`\frac{A}{2}B`) and its byKey line.
18. fixed: l4 screens[6], l5 screens[7], l8 screens[6], l12 screens[1], homework-3 items[5] correct options shortened as listed.
19. fixed: l9 screens[9] and homework-3 items[6] explanations state £101.20 and £4.50. Recomputed: $P(2) = 87.20$, $P(-2) = 115.20$, mean 101.20; $\tfrac{45}{6} - 3 = 4.50$.
20. fixed: review-2 items[7] prose and question reworded.
21. fixed: review-2 items[8] is now the two-year loss. Recomputed: $20000 \times 0.9^2 = 16200$; root $-0.9$ gives 190%. Graded answer changed (0.2 to 0.1).
22. fixed: review-3 items[1] prose and question reworded.
23. fixed: review-1 items[6] (photo area, answer 0.0609) and items[7] (r = 0.1). Recomputed: $1.03^2 = 1.0609$; $1.1 \times 0.9 = 0.99$. Graded answers changed. Explanation of items[6] also states 6.09% (validator O2).
24. fixed: homework-1 items[4] is $1003 \times 997 = 999991$ (graded answer changed from 12000). Recomputed: $10^6 - 9$.
25. fixed: homework-3 items[0] asks for the vertex 7.5 (graded answer changed from 100.9). Recomputed: $6 / 0.8 = 7.5$, $P = 100 - 45 + 22.5 = 77.50$; scan confirms the minimum.
26. fixed: l13 screens[9] (B at 30%, drag target (0.9, 0.009), start point y updated to 0.08125) and homework-3 items[7] last sentence. Recomputed: $V = 0.1w^2 - 0.18w + 0.09$, $V(0.9) = 0.009$, $V(0.5) = 0.025$, $\sqrt{0.009} = 9.5\%$. Graded answer changed.
Engine 1, 2, 3: deferred, engine-only, already in the inbox.
From review-functions-3-4 finding 34: fixed. l9 screens[0] prose now starts from the curve ("You plotted $y = x^2$ from its table in the functions course"), with no lesson number.

Gates: number scripts L1, L2, L3 exit 0 (408, 381 and 279 checks; the old-or-new checks were replaced by new-value-only checks). Voice scan 35: 0 sentences, 0 explanations. Validator: 0 errors. Playthrough with `--local-cdn`: 11 lessons and 6 sets, 17 of 17 desktop and 17 of 17 `--mobile`, All passed. No code items touched.
