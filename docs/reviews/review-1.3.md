# Topic 1.3 second-reader findings

Format: file | screen or item id | severity | what is wrong | corrected value or wording.
Severity: error = wrong number, false claim or wrong grading; warning = weak explanation or teaching issue; note = style.
Checks: dump.py, style.py, check_limits.py, check_integrals.py, check_multivar.py (also runs every Python code widget against its tests), check_exam.py, all in this folder.

## app/content/courses/integrals/homework-1.json
- app/content/courses/integrals/homework-1.json | h-volume-profile explain | warning | "Note the U shape: trading is heaviest at the open." The bars contradict it: 11:30 (2,800 a minute) is above 08:00 (2,400). A real U is heavy at open and close, and 11:30 is mid-morning. | Lower the 11:30 bar (e.g. to 1,300, adjusting the total), or say "heaviest at the open, quietest mid-morning".
- app/content/courses/integrals/homework-1.json | .items[3].explain.text | note | Explanation has 5 sentences (limit 3). | Merge or cut to three sentences.
- app/content/courses/integrals/homework-1.json | .items[5].prose | note | Sentence of 21 words (limit 20): "The bars show a stock's average trading rate in each half hour of its first four hours, in shares per minute." | Split into two sentences of 20 words or fewer.
- app/content/courses/integrals/homework-1.json | .items[7].prompt | note | Sentence of 21 words (limit 20): "(a) Compute the left and right sums  [maths]  and  [maths]  for  [maths] , and say which is an overestimate and why." | Split into two sentences of 20 words or fewer.
- app/content/courses/integrals/homework-1.json | .items[7].rubric[1].text | note | Sentence of 21 words (limit 20): "Splits at  [maths] , finds  [maths]  shares with the lower triangle counted negative, and checks it lies between 0 and 1000." | Split into two sentences of 20 words or fewer.
- app/content/courses/integrals/homework-1.json | .items[7].rubric[2].text | note | Sentence of 23 words (limit 20): "Gives 1,300 shares traded as the total area  [maths] , and explains that area counts selling as positive while the integral nets it." | Split into two sentences of 20 words or fewer.
- app/content/courses/integrals/homework-1.json | .items[7].rubric[3].text | note | Sentence of 25 words (limit 20): "Places the peak at  [maths] , where  [maths]  changes sign, with inventory 900 above the start, and explains why it is not at  [maths] ." | Split into two sentences of 20 words or fewer.

## app/content/courses/integrals/homework-2.json
- app/content/courses/integrals/homework-2.json | .items[8].rubric[9].text | note | Sentence of 23 words (limit 20): "(d) Locates the failure:  [maths]  and  [maths]  are undefined at 0, inside  [maths] , so (b) does not apply; the area is unbounded." | Split into two sentences of 20 words or fewer.

## app/content/courses/integrals/homework-3.json
- app/content/courses/integrals/homework-3.json | .items[3].prose | note | Sentence of 22 words (limit 20): "A royalty pays continuously at a rate that grows in a straight line: £ [maths]  a year at time  [maths] , forever." | Split into two sentences of 20 words or fewer.
- app/content/courses/integrals/homework-3.json | .items[3].feedback.correct | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.
- app/content/courses/integrals/homework-3.json | .items[5].feedback.correct | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.
- app/content/courses/integrals/homework-3.json | .items[7].model | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.

## app/content/courses/integrals/l1-thin-rectangles.json
- app/content/courses/integrals/l1-thin-rectangles.json | .screens[4].explain.text | note | Sentence of 21 words (limit 20): "Each rectangle sticks out above the curve on one side and falls short on the other, so the errors nearly cancel." | Split into two sentences of 20 words or fewer.
- app/content/courses/integrals/l1-thin-rectangles.json | .screens[5].widget.options[2].why | note | Sentence of 21 words (limit 20): "If the curve falls, each left end is the highest point of its strip, and the left sum is too big." | Split into two sentences of 20 words or fewer.
- app/content/courses/integrals/l1-thin-rectangles.json | .screens[5].explain.text | note | Sentence of 21 words (limit 20): "On a rising curve each strip is lowest at its left end, so every left rectangle misses a sliver of area." | Split into two sentences of 20 words or fewer.
- app/content/courses/integrals/l1-thin-rectangles.json | .screens[9].prose | note | Sentence of 21 words (limit 20): "A risk model says the chance that tomorrow's return lands between two values is the area under this curve between them." | Split into two sentences of 20 words or fewer.

## app/content/courses/integrals/l11-to-infinity.json
- app/content/courses/integrals/l11-to-infinity.json | .quiz[2].explain.text | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.
- app/content/courses/integrals/l11-to-infinity.json | .quiz[2].feedback.correct | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.
- app/content/courses/integrals/l11-to-infinity.json | .screens[7].explain.text | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.
- app/content/courses/integrals/l11-to-infinity.json | .screens[8].explain.text | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.
- app/content/courses/integrals/l11-to-infinity.json | .screens[8].feedback.correct | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.

## app/content/courses/integrals/l13-average-as-integral.json
- app/content/courses/integrals/l13-average-as-integral.json | S9 | note | Same triangular density and £100 call as homework-2 h-ev-triangle, answer £1.67 both times: a repeat, not a transfer. | Change the strike to £105: $\tfrac{1}{100}\int_5^{10}(y - 5)(10 - y)\,dy \approx £0.21$.
- app/content/courses/integrals/l13-average-as-integral.json | S5 feedback byKey no-x | note | "You doubled the right answer" names the result, not the action. 8/3 comes from integrating $x \cdot x$ and dropping the density's $\tfrac12$. | "You integrated $x \cdot x$ and dropped the $\tfrac12$ in the density."
- app/content/courses/integrals/l13-average-as-integral.json | .summary.trap | note | Sentence of 24 words (limit 20): "The payoff at the expected price is not the expected payoff: a call struck at the mean pays £0,00 there but is worth £2,50." | Split into two sentences of 20 words or fewer.
- app/content/courses/integrals/l13-average-as-integral.json | .quiz[3].explain.text | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.
- app/content/courses/integrals/l13-average-as-integral.json | .screens[5].explain.text | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.
- app/content/courses/integrals/l13-average-as-integral.json | .screens[8].explain.text | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.

## app/content/courses/integrals/l2-thinner.json
- app/content/courses/integrals/l2-thinner.json | .screens[1].prose | note | Sentence of 22 words (limit 20): "As  [maths]  grows the trap closes, so both sums **converge** to  [maths] : they get as close to it as we like." | Split into two sentences of 20 words or fewer.

## app/content/courses/integrals/l3-signed-area.json
- app/content/courses/integrals/l3-signed-area.json | .screens[1].prose | note | Sentence of 21 words (limit 20): "With thinner and thinner rectangles the sum becomes the **signed area**: area above the axis counts positive, area below counts negative." | Split into two sentences of 20 words or fewer.
- app/content/courses/integrals/l3-signed-area.json | .screens[1].feedback.byKey.crossing | note | Sentence of 21 words (limit 20): "At  [maths]  the curve crosses the axis, but the signed area is  [maths] : only the part below has been added." | Split into two sentences of 20 words or fewer.
- app/content/courses/integrals/l3-signed-area.json | .screens[2].prose | note | Sentence of 21 words (limit 20): "We write the signed area from  [maths]  to  [maths]  as  [maths]  the **definite integral** of  [maths]  from  [maths]  to  [maths] ." | Split into two sentences of 20 words or fewer.

## app/content/courses/integrals/l4-accumulating-a-rate.json
- app/content/courses/integrals/l4-accumulating-a-rate.json | quiz[3] (Q4) | note | Using act/365 day counts for a fixed-rate bond accrual is a simplification (UK gilts use actual/actual); fine for the lesson, but unlabelled. | Add "on an actual/365 basis" to the prose.
- app/content/courses/integrals/l4-accumulating-a-rate.json | .screens[2].prose | note | Sentence of 22 words (limit 20): "The cash in by day  [maths]  is the area under the rate from 0 to  [maths] , written  [maths]  the **accumulated amount**." | Split into two sentences of 20 words or fewer.
- app/content/courses/integrals/l4-accumulating-a-rate.json | .screens[7].widget.lines[0].text | note | Sentence of 21 words (limit 20): "Cut  [maths]  into  [maths]  pieces of length  [maths] : the total change is the sum of the changes on the pieces" | Split into two sentences of 20 words or fewer.
- app/content/courses/integrals/l4-accumulating-a-rate.json | .screens[7].widget.lines[1].text | note | Sentence of 23 words (limit 20): "On each piece the rate stays between its lowest and highest values there, so that piece's change lies between those rates times  M" | Split into two sentences of 20 words or fewer.
- app/content/courses/integrals/l4-accumulating-a-rate.json | .quiz[0].prose | note | Sentence of 24 words (limit 20): "Shares trade at 2,000 a minute for the first 15 minutes after the open, then at 500 a minute for the next 30 minutes." | Split into two sentences of 20 words or fewer.
- app/content/courses/integrals/l4-accumulating-a-rate.json | .quiz[3].explain.text | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.
- app/content/courses/integrals/l4-accumulating-a-rate.json | .screens[4].explain.text | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.
- app/content/courses/integrals/l4-accumulating-a-rate.json | .screens[8].explain.text | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.

## app/content/courses/integrals/l5-area-undoes-slope.json
- app/content/courses/integrals/l5-area-undoes-slope.json | .screens[0].explain.text | note | Explanation has 4 sentences (limit 3). | Merge or cut to three sentences.
- app/content/courses/integrals/l5-area-undoes-slope.json | .screens[5].feedback.byKey.area | note | Sentence of 21 words (limit 20): "The derivative of the area is not the area: it is how fast the area grows, the edge height  [maths] ." | Split into two sentences of 20 words or fewer.

## app/content/courses/integrals/l7-evaluating.json
- app/content/courses/integrals/l7-evaluating.json | S7 explain | warning | Promises "level 3 treats such integrals" (an unbounded integrand, $\int_\varepsilon^1 x^{-2}\,dx$), but level 3's l11 treats only infinite intervals. No lesson handles an integrand that blows up at an end of $[a, b]$. | Add a screen to l11 on $\int_0^1 x^{-p}\,dx$ (finite for $p < 1$, e.g. $\int_0^1 x^{-1/2}\,dx = 2$), or change the promise to "such integrals have no finite value".

## app/content/courses/integrals/l9-undo-chain.json
- app/content/courses/integrals/l9-undo-chain.json | .screens[7].explain.text | note | Explanation has 4 sentences (limit 3). | Merge or cut to three sentences.

## app/content/courses/integrals/review-1.json
- app/content/courses/integrals/review-1.json | .items[8].explain.text | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.
- app/content/courses/integrals/review-1.json | .items[8].feedback.correct | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.

## app/content/courses/limits/homework-1.json
- app/content/courses/limits/homework-1.json | .items[8].rubric[2].text | note | Sentence of 21 words (limit 20): "Says  [maths]  is not continuous because  [maths] , names a hole, and rules out a jump and an asymptote with reasons." | Split into two sentences of 20 words or fewer.

## app/content/courses/limits/homework-2.json
- app/content/courses/limits/homework-2.json | hw2-negative-power explain | warning | "Left of 0 the curve climbs towards the axis": $5/x^2$ climbs without bound as $x \to 0^-$, away from the $x$-axis; "the axis" reads as the $x$-axis. | "...left of 0 the curve climbs as it nears the $y$-axis."
- app/content/courses/limits/homework-2.json | hw2-corners model (d) | note | Explains delta near 0.5 as "about as likely to finish in the money as out", which is $N(d_2)$, not delta $N(d_1)$; teaches delta as a probability. | "...so its slope sits between the 0 and 1 of the payoff, close to 0.5 (a little above it)."

## app/content/courses/limits/homework-3.json
- app/content/courses/limits/homework-3.json | h-portfolio-correlated explain | note | Four sentences (limit three), and the reason covers only the denominator (0.014 against 0.008); the numerator grows too (0.032 against 0.024). | "The cross term adds 0.008 to the top and 0.006 to the bottom. The bottom grows faster in proportion, so each unit of equity needs a smaller bond cut: −2.286, not −3."

## app/content/courses/limits/homework-4.json
- app/content/courses/limits/homework-4.json | h-second-order feedback.correct vs explain | note | Feedback says "within 7p of the true £84.03", explain says "cuts the error to 6p". The gap is £84.0947 − £84.0292 = 6.5p. | Use one figure in both: "about 6p".

## app/content/courses/limits/l1-getting-closer.json
- app/content/courses/limits/l1-getting-closer.json | S6 hint nudge | warning | Hint says "Compare the two $s(x)$ columns" but the canvas is a plane of dots, not a table. | "Compare the heights of the A dots and the B dots."
- app/content/courses/limits/l1-getting-closer.json | .screens[0].prose | note | Sentence of 22 words (limit 20): "At  [maths]  the top and the bottom are both 0, so the formula gives  [maths] , which is no number at all." | Split into two sentences of 20 words or fewer.
- app/content/courses/limits/l1-getting-closer.json | .screens[3].widget.options[1].why | note | Sentence of 21 words (limit 20): "The limit asks where the heights head as  [maths]  closes in on 2, and from both sides they head to 3." | Split into two sentences of 20 words or fewer.
- app/content/courses/limits/l1-getting-closer.json | .screens[5].widget.options[0].text | note | Sentence of 21 words (limit 20): "No: two runs closing in on 0 give outputs stuck at 0 and stuck at 1, so no single number fits" | Split into two sentences of 20 words or fewer.
- app/content/courses/limits/l1-getting-closer.json | .screens[7].prose | note | Sentence of 25 words (limit 20): "M  means  [maths]  gets as close to  [maths]  as we like once  [maths]  is close enough to  [maths] , from both sides, with  [maths] ." | Split into two sentences of 20 words or fewer.
- app/content/courses/limits/l1-getting-closer.json | .screens[9].prose | note | Sentence of 21 words (limit 20): "The bid always sits a quarter of the spread below a fair price  [maths] , and the ask three quarters above." | Split into two sentences of 20 words or fewer.
- app/content/courses/limits/l1-getting-closer.json | .summary.ideas[0] | note | Sentence of 21 words (limit 20): "A limit is the number the outputs close in on as the input closes in on  [maths] , from both sides." | Split into two sentences of 20 words or fewer.
- app/content/courses/limits/l1-getting-closer.json | .quiz[3].explain.text | note | Sentence of 21 words (limit 20): "Every input on the list is closer to 0 than the last, yet the outputs flip between −1 and 1 forever." | Split into two sentences of 20 words or fewer.

## app/content/courses/limits/l10-inside-function.json
- app/content/courses/limits/l10-inside-function.json | S11 explain | note | "A 0.01 rise in yield cuts the price by about £6.60" is the tangent estimate; the true fall is £6.27. Taylor l8 later teaches this exact gap. | "...by about £6.60 on the tangent line (the true fall is £6.27)."

## app/content/courses/limits/l12-implicit.json
- app/content/courses/limits/l12-implicit.json | S7 feedback byKey no-y-prime | warning | "Your slope is the dashed line, which cuts the circle" refers to a dashed line that no state or option canvas draws. | Draw $y - 3 = -\tfrac{10}{3}(x - 2)$ dashed for this key, or reword: "A line of slope $-\tfrac{10}{3}$ through (2, 3) would cut the circle."
- app/content/courses/limits/l12-implicit.json | S10 | note | Weights 0.3 and 0.4 sum to 0.7 with no word on the other 0.3. | Add "the rest is in cash, which has no risk".

## app/content/courses/limits/l2-computing-limits.json
- app/content/courses/limits/l2-computing-limits.json | S8 explain + summary.ideas[1] | warning | "$\tfrac00$ means a factor $(x - a)$ hides top and bottom" is given as a general rule. It holds for polynomials only: l1's $(\sqrt x - 1)/(x - 1)$ and l16's $\sin x / x$ are $0/0$ with no polynomial factor. | "For polynomials, $\tfrac00$ means a factor $(x - a)$ hides top and bottom. Other $\tfrac00$ limits need other tools (lesson 16)."
- app/content/courses/limits/l2-computing-limits.json | S8 / summary.ideas[2] | note | "A non-zero number over 0 means no limit" lumps $1/(x-1)$ (sides disagree) with $1/(x-1)^2$ (both sides go to $+\infty$, which l4 writes as $\lim = \infty$). | "...means no finite limit: the outputs blow up."
- app/content/courses/limits/l2-computing-limits.json | .screens[2].prose | note | Sentence of 22 words (limit 20): "The top,  [maths] , and the bottom,  [maths] , are both 0 at  [maths] , so they share the factor  [maths] ." | Split into two sentences of 20 words or fewer.

## app/content/courses/limits/l3-without-lifting.json
- app/content/courses/limits/l3-without-lifting.json | .screens[0].hints[2].text | note | Sentence of 21 words (limit 20): "Three places: the open circle at  [maths] , the drop at  [maths] , and the curve shooting off at  [maths] ." | Split into two sentences of 20 words or fewer.
- app/content/courses/limits/l3-without-lifting.json | .screens[0].feedback.correct | note | Sentence of 22 words (limit 20): "Three breaks: a gap at  [maths] , a drop at  [maths] , and a curve that runs off the page at 3." | Split into two sentences of 20 words or fewer.
- app/content/courses/limits/l3-without-lifting.json | .screens[6].explain.text | note | Sentence of 24 words (limit 20): "The heights near 2 close in on 4, but the value is 5, so the pen must jump up to the dot and back." | Split into two sentences of 20 words or fewer.
- app/content/courses/limits/l3-without-lifting.json | .screens[9].explain.text | note | Sentence of 22 words (limit 20): "A price path jumps while the market is shut, so the stop fills at £98,15, £1,85 a share worse than its level." | Split into two sentences of 20 words or fewer.
- app/content/courses/limits/l3-without-lifting.json | .summary.ideas[0] | note | Sentence of 25 words (limit 20): "M  is continuous at  [maths]  when you can draw through it without lifting the pen: the value exists, the limit exists, and they are equal." | Split into two sentences of 20 words or fewer.

## app/content/courses/limits/l4-far-out.json
- app/content/courses/limits/l4-far-out.json | S2 explain, excanvas, option `equal` why | error | At $x = 1000$ the shares of $1{,}051{,}000$ are 0.9515, 0.0476 and 0.00095, not 0.9443, 0.0472 and 0.0009; "holds 94%" is wrong. | "holds 95%"; excanvas values 0.9515, 0.0476, 0.0010.
- app/content/courses/limits/l4-far-out.json | .screens[6].prose | note | Sentence of 21 words (limit 20): "But  [maths]  always lies between  [maths]  and 1, so the curve is trapped between  [maths]  and  [maths] , the dashed curves." | Split into two sentences of 20 words or fewer.

## app/content/courses/limits/l5-instant-speed.json
- app/content/courses/limits/l5-instant-speed.json | S10 explain | note | "A desk would call that the price's instantaneous drift" misuses drift, which is the expected rate $\mu$ of a random price model, not the slope of one path. | "That is the price's instantaneous rate of change at 2 hours."

## app/content/courses/limits/l6-first-principles.json
- app/content/courses/limits/l6-first-principles.json | .summary.ideas[2] | note | Sentence of 21 words (limit 20): "The derivative is a function: one slope for every  [maths] , and it can be negative where the height is positive." | Split into two sentences of 20 words or fewer.

## app/content/courses/limits/l8-slope-graph.json
- app/content/courses/limits/l8-slope-graph.json | S9 explain + hint point | warning | "At the money it is 0.50" is true of this toy softplus curve but stated as a fact about calls. A Black-Scholes at-the-money call has delta $N(d_1)$, about 0.54 at 20% vol and one year. | "On this curve the delta at the strike is 0.50; real at-the-money deltas sit a little above that."
- app/content/courses/limits/l8-slope-graph.json | .screens[1].explain.text | note | Sentence of 25 words (limit 20): "S went through 4, 0 and  [maths]  at  [maths] , 3 and 5: a straight line falling through 0 under the top of the hill." | Split into two sentences of 20 words or fewer.

## app/content/courses/limits/l9-products-quotients.json
- app/content/courses/limits/l9-products-quotients.json | S10 order item q2 | note | Deriving the quotient rule from $u = qv$ assumes $q$ is differentiable, which is part of what is being shown; no line says so. | Add to the reason: "assuming $q$ has a derivative (true wherever $v \neq 0$)".

## app/content/courses/multivar/homework-2.json
- app/content/courses/multivar/homework-2.json | h-plane-expr wrong[fy] | error | The distractor for the mistake $f_y = 7$ is `4x+7y-10`, but $3 + 4(x - 2) + 7(y - 1) = 4x + 7y - 12$. A learner who makes the named mistake gets generic feedback. | Change the tex to `4x+7y-12`.
- app/content/courses/multivar/homework-2.json | .items[4].prose | note | Sentence of 21 words (limit 20): "It returns the first step count  [maths] , from 0, at which  [maths]  at the current point is below  C ." | Split into two sentences of 20 words or fewer.
- app/content/courses/multivar/homework-2.json | .items[4].widget.how | note | Sentence of 25 words (limit 20): "Check runs 7 hidden tests on  [maths]  and  [maths] : good steps, a tiny step, a start at the minimum, and steps that never settle." | Split into two sentences of 20 words or fewer.

## app/content/courses/multivar/homework-4.json
- app/content/courses/multivar/homework-4.json | .items[7].rubric[0].text | note | Sentence of 21 words (limit 20): "(a) Renames the dummy variable and writes  [maths]  as a double integral over the square, citing the product rule  [maths] ." | Split into two sentences of 20 words or fewer.
- app/content/courses/multivar/homework-4.json | .items[3].feedback.correct | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.
- app/content/courses/multivar/homework-4.json | .items[3].widget.accept | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.

## app/content/courses/multivar/l1-two-inputs.json
- app/content/courses/multivar/l1-two-inputs.json | .summary.ideas[0] | note | Sentence of 22 words (limit 20): "A function of two variables takes a pair  [maths]  to one number  [maths] : a height above each point of the plane." | Split into two sentences of 20 words or fewer.

## app/content/courses/multivar/l10-second-derivative-test.json
- app/content/courses/multivar/l10-second-derivative-test.json | .screens[0].widget.options[2].why | note | Sentence of 21 words (limit 20): "Rings close round a peak too, but here the heights fall towards A: the inner ring is  [maths]  and  [maths] ." | Split into two sentences of 20 words or fewer.
- app/content/courses/multivar/l10-second-derivative-test.json | .screens[7].explain.text | note | Sentence of 23 words (limit 20): "With  [maths]  they agree in sign, so every step goes the same way: a pit if  [maths] , a peak if  [maths] ." | Split into two sentences of 20 words or fewer.

## app/content/courses/multivar/l13-volume.json
- app/content/courses/multivar/l13-volume.json | .screens[1].prose | note | Sentence of 24 words (limit 20): "A row of boxes is a **slab**: a strip of floor 1 unit deep in  [maths] , running the full width in  [maths] ." | Split into two sentences of 20 words or fewer.
- app/content/courses/multivar/l13-volume.json | .screens[9].hints[2].text | note | Sentence of 22 words (limit 20): "Pull out  [maths] , name the inner integral  [maths] , pull  [maths]  out of the outer integral, then write  [maths]  in full." | Split into two sentences of 20 words or fewer.

## app/content/courses/multivar/l14-other-regions.json
- app/content/courses/multivar/l14-other-regions.json | .screens[8].widget.lines[0].text | note | Sentence of 22 words (limit 20): "For fixed  [maths] ,  [maths]  runs from the line  [maths]  to the parabola  [maths] , and  [maths]  runs from 0 to 1" | Split into two sentences of 20 words or fewer.
- app/content/courses/multivar/l14-other-regions.json | .summary.ideas[2] | note | Sentence of 21 words (limit 20): "To swap the order, redraw the strips the other way and rewrite every curve as  [maths]  in terms of  [maths] ." | Split into two sentences of 20 words or fewer.

## app/content/courses/multivar/l15-polar.json
- app/content/courses/multivar/l15-polar.json | .screens[1].prose | note | Sentence of 24 words (limit 20): "It becomes a near-rectangle: one side  [maths]  along the ray, the other an arc of angle  [maths]  on a circle of radius  [maths] ." | Split into two sentences of 20 words or fewer.
- app/content/courses/multivar/l15-polar.json | .screens[5].explain.text | note | Sentence of 21 words (limit 20): "In polar coordinates the curved region is a rectangle:  [maths]  from 1 to 2 and  [maths]  from 0 to  [maths] ." | Split into two sentences of 20 words or fewer.
- app/content/courses/multivar/l15-polar.json | .screens[6].prose | note | Sentence of 24 words (limit 20): "To switch to polar: write  [maths]  and  [maths] , describe the region by ranges of  [maths]  and  [maths] , and use  [maths] :  M" | Split into two sentences of 20 words or fewer.
- app/content/courses/multivar/l15-polar.json | .summary.ideas[0] | note | Sentence of 22 words (limit 20): "A polar cell is a near-rectangle with sides  [maths]  and  [maths] , so  [maths] : cells far from the origin are bigger." | Split into two sentences of 20 words or fewer.
- app/content/courses/multivar/l15-polar.json | .summary.trap | note | Sentence of 21 words (limit 20): "Forgetting the  [maths]  in  [maths] : it gives  [maths]  for a disc's area, and  [maths]  instead of  [maths]  for  [maths] ." | Split into two sentences of 20 words or fewer.

## app/content/courses/multivar/l4-chain-two-inputs.json
- app/content/courses/multivar/l4-chain-two-inputs.json | S9 explain | note | $dV/dt$ from delta and vega alone ignores time decay over the hour; fine for the lesson but unstated. | Add "ignoring time decay" to the prose or explain.
- app/content/courses/multivar/l4-chain-two-inputs.json | .screens[7].prose | note | Sentence of 23 words (limit 20): "We split the change in  [maths]  into a step in  [maths]  and a step in  [maths] , as you did on the map." | Split into two sentences of 20 words or fewer.

## app/content/courses/multivar/l5-steepest-climb.json
- app/content/courses/multivar/l5-steepest-climb.json | .screens[6].explain.text | note | Sentence of 21 words (limit 20): "The hill is steepest across its narrow side, so the best first step heads for the ridge line, not the summit." | Split into two sentences of 20 words or fewer.
- app/content/courses/multivar/l5-steepest-climb.json | .screens[8].explain.text | note | Explanation has 4 sentences (limit 3). | Merge or cut to three sentences.

## app/content/courses/multivar/l7-tangent-planes.json
- app/content/courses/multivar/l7-tangent-planes.json | .screens[5].explain.text | note | Sentence of 22 words (limit 20): "The tangent plane is built only from what we know at (2, 1): the height 6 and the slopes 4 and 4." | Split into two sentences of 20 words or fewer.

## app/content/courses/multivar/l8-walking-downhill.json
- app/content/courses/multivar/l8-walking-downhill.json | S6 explain | note | "$x$ grows by 1.2 and $y$ by 1.4 each step" reads as adding 1.2 and 1.4; they are factors. | "$x$ is multiplied by 1.2 and $y$ by 1.4 each step."
- app/content/courses/multivar/l8-walking-downhill.json | .screens[8].widget.how | note | Sentence of 26 words (limit 20): "Three check 0, 1 and 3 steps exactly; three run 3,000 steps and compare with the exact least-squares line, which the descent has reached by then." | Split into two sentences of 20 words or fewer.

## app/content/courses/multivar/review-1.json
- app/content/courses/multivar/review-1.json | r1-pnl-zero feedback byKey wrong-diagonal | error | The grid is 1-indexed (r1 is ΔB = 2, c1 is ΔA = −2), so r1c1, r3c3, r5c5 is the diagonal ΔB = −ΔA: the prices move in opposite directions. The feedback says "both prices fall or rise together", which is false. | "On that diagonal B moves opposite to A by the same amount, but A's move is worth twice as much, so the P&L is ±£100 off the centre."
- app/content/courses/multivar/review-1.json | .items[0].feedback.byKey.centre-only | note | Sentence of 21 words (limit 20): "No move at all gives £0, but so do pairs that cancel, such as A down £1 with B up £2." | Split into two sentences of 20 words or fewer.
- app/content/courses/multivar/review-1.json | .items[8].prose | note | Sentence of 22 words (limit 20): "Today the 2-year yield  [maths]  rises 2 basis points a day and the 10-year yield  [maths]  falls 1 basis point a day." | Split into two sentences of 20 words or fewer.

## app/content/courses/taylor/homework-1.json
- app/content/courses/taylor/homework-1.json | h-long-bond model (d), (f) | note | `\text{\text{£}}97.17` and `\text{\text{£}}0.80` nest \text twice; it renders, but it is a typo. | `\text{£}97.17`, `\text{£}0.80`.
- app/content/courses/taylor/homework-1.json | .items[8].rubric[3].text | note | Sentence of 21 words (limit 20): "Gives the tangent's price £97,17 and the true price £97,38 at 7%, a gap of £0,20 with the true price above." | Split into two sentences of 20 words or fewer.

## app/content/courses/taylor/homework-3.json
- app/content/courses/taylor/homework-3.json | hw3-drag-longform model (a) | note | Prompt names daily moments $\mu_d$, $\sigma_d$, but model (a) writes $E[R] = \mu$, $Var(R) = \sigma^2$ for the daily return, then (b) uses $\mu = 8\%$ as the annual figure: one letter, two meanings. | Use $\mu_d$ and $\sigma_d$ throughout (a).
- app/content/courses/taylor/homework-3.json | .items[0].explain.text | note | Explanation has 4 sentences (limit 3). | Merge or cut to three sentences.
- app/content/courses/taylor/homework-3.json | .items[2].prose | note | Sentence of 21 words (limit 20): "We want to prove that the Maclaurin series of  [maths]  equals  [maths]  for every real  [maths] , not just near 0." | Split into two sentences of 20 words or fewer.

## app/content/courses/taylor/l1-tangent-approx.json
- app/content/courses/taylor/l1-tangent-approx.json | S6 prose | error | "Only one of them wrote a straight line" is false: option no-base, $L(x) = x$, is a straight line too, and its own why calls it "that line". | "Only one of them wrote the tangent at $(0, 1)$."
- app/content/courses/taylor/l1-tangent-approx.json | .screens[6].prose | note | Sentence of 21 words (limit 20): "Every estimate so far used two numbers from a base point  [maths] : the height  [maths]  and the slope  [maths] ." | Split into two sentences of 20 words or fewer.

## app/content/courses/taylor/l10-how-far.json
- app/content/courses/taylor/l10-how-far.json | S9 | note | "A spreadsheet finds the log return by adding 50 terms" is not how spreadsheets work (LN exists); context invented, though the point (series fails outside R) stands. | "A junior's script computes $\ln(1 + r)$ from 50 terms of the series..."

## app/content/courses/taylor/l11-bounding-error.json
- app/content/courses/taylor/l11-bounding-error.json | S5 feedback byKey two-terms | error | The value 0.0094 is $|S_5 - S_3| = 0.015625 - 0.00625$, but the feedback says "That is the gap from $S_4$ to $S_5$", which is 0.00625. | "You added the next two left-out terms, $-\tfrac{0.5^4}{4} + \tfrac{0.5^5}{5}$. The bound is the first left-out term alone, 0.0156."
- app/content/courses/taylor/l11-bounding-error.json | S9 | note | "To save time it uses $e^{-x} \approx 1 - x + \tfrac{x^2}{2}$": no desk saves time this way on one exponential. | Frame it as a mental check, or as bounding a hand calculation.
- app/content/courses/taylor/l11-bounding-error.json | .screens[4].explain.text | note | Explanation has 4 sentences (limit 3). | Merge or cut to three sentences.

## app/content/courses/taylor/l12-log-vs-simple.json
- app/content/courses/taylor/l12-log-vs-simple.json | .screens[0].widget.label | note | "percent" is American usage in visible text. | "per cent".
- app/content/courses/taylor/l12-log-vs-simple.json | .screens[9].widget.label | note | "percent" is American usage in visible text. | "per cent".
- app/content/courses/taylor/l12-log-vs-simple.json | .summary.ideas[0] | note | Sentence of 21 words (limit 20): "M , so a log return is about  [maths] : 0,00005 below  [maths]  at 1%, 0,0047 at 10%, 0,0945 at 50%." | Split into two sentences of 20 words or fewer.
- app/content/courses/taylor/l12-log-vs-simple.json | .quiz[1].widget.label | note | "percent" is American usage in visible text. | "per cent".
- app/content/courses/taylor/l12-log-vs-simple.json | .quiz[3].widget.label | note | "percent" is American usage in visible text. | "per cent".

## app/content/courses/taylor/l2-how-wrong.json
- app/content/courses/taylor/l2-how-wrong.json | S11 | note | The hedged book's £500 gamma gain ignores theta; a desk would say time decay pays for it. | Add "before the option's time decay" to the explain.

## app/content/courses/taylor/l3-newton.json
- app/content/courses/taylor/l3-newton.json | .screens[2].prose | note | Sentence of 22 words (limit 20): "Repeating this is **Newton's method**: from each guess, follow the tangent to the axis and use that point as the next guess." | Split into two sentences of 20 words or fewer.
- app/content/courses/taylor/l3-newton.json | .summary.ideas[2] | note | Sentence of 27 words (limit 20): "It can fail: a flat tangent ( [maths] ), a jump to a far root, or a cycle such as 0, 1, 0, 1 on  [maths] ." | Split into two sentences of 20 words or fewer.

## app/content/courses/taylor/l4-duration.json
- app/content/courses/taylor/l4-duration.json | whole lesson | warning | Repeats limits l15 almost screen for screen: same 5-year 4% bond, $P'(0.05) = -420.98$, $D = 4.40$, £4.21 tangent fall, £0.11 and £0.99 gaps, same "a fall gains more" point. Nothing new until S9 (DV01), which l15 S9 also touched. | Give this lesson a different bond (e.g. 10-year) and build on l15 openly ("in limits you found $D = 4.40$; now..."), or cut l15 back to sensitivity and leave duration here.
- app/content/courses/taylor/l4-duration.json | S7 + quiz Q1 | note | "Yields fall 0.5%" and "falls by 0.25%" are ambiguous (relative or absolute?); desks say basis points. | "yields fall 50 basis points ($\Delta y = -0.005$)".

## app/content/courses/taylor/l5-curvature-term.json
- app/content/courses/taylor/l5-curvature-term.json | S5 explain | error | "The curvature term cut the error by a factor of nine." The errors are 0.004555 and 0.000445: a factor of 10.2. The lesson summary says "about ten times". | "...cut the error by a factor of about ten."

## app/content/courses/taylor/l6-matching-derivatives.json
- app/content/courses/taylor/l6-matching-derivatives.json | S10 prose | warning | "Risk systems approximate it with $P_3$ of $\ln x$ about 1" is false: any system computes $\ln 1.06$ directly. The quant context is invented. | "Without a calculator, a trader can estimate it with $P_3$..." or frame it as checking how far simple and log returns differ.
- app/content/courses/taylor/l6-matching-derivatives.json | .screens[2].prose | note | Sentence of 22 words (limit 20): "The curve on the first screen is the **Taylor polynomial**  [maths] : it copies  [maths]  and its first  [maths]  derivatives at 0." | Split into two sentences of 20 words or fewer.

## app/content/courses/taylor/l7-standard-series.json
- app/content/courses/taylor/l7-standard-series.json | S10, quiz Q3, summary.formula.note | warning | Calls $e^{0.05} - 1$ the "equivalent simple annual rate" that "banks quote". It is the effective annual rate (the AER UK banks quote). "Simple" clashes with l1 S9, where simple interest means no compounding. | "Banks quote the equivalent annual rate (AER), $e^{0.05} - 1$"; question: "What annual rate is that..."
- app/content/courses/taylor/l7-standard-series.json | .screens[9].question | note | "percent" is American usage in visible text. | "per cent".
- app/content/courses/taylor/l7-standard-series.json | .quiz[2].question | note | "percent" is American usage in visible text. | "per cent".

## app/content/courses/taylor/l9-does-it-add-up.json
- app/content/courses/taylor/l9-does-it-add-up.json | .screens[2].explain.text | note | Explanation has 4 sentences (limit 3). | Merge or cut to three sentences.

## app/content/courses/taylor/review-3.json
- app/content/courses/taylor/review-3.json | .items[7].question | note | "percent" is American usage in visible text. | "per cent".
- app/content/courses/taylor/review-3.json | .items[7].widget.label | note | "percent" is American usage in visible text. | "per cent".
- app/content/courses/taylor/review-3.json | .items[8].question | note | "percent" is American usage in visible text. | "per cent".
- app/content/courses/taylor/review-3.json | .items[8].widget.label | note | "percent" is American usage in visible text. | "per cent".

## app/content/exams/topic-1.3.json
- app/content/exams/topic-1.3.json | c-gauss-disc (I26) wrong[no-half] | error | Value 0.6321 is $1 - e^{-1}$, but the feedback says the learner "integrates $e^{-r^2}$ instead", which gives $\tfrac12(1 - e^{-1}) = 0.3161$. Value and why do not match. | Keep 0.6321 with "You wrote $e^{-1}$ for $e^{-1/2}$ at $r = 1$: the exponent is $-\tfrac{r^2}{2}$", or change the value to 0.3161.
- app/content/exams/topic-1.3.json | c-gauss-disc (I26) explain | note | "Both shocks stay inside the unit circle" is loose: it is the pair $(X, Y)$ that lands inside, not each shock. | "The pair $(X, Y)$ lands inside the unit circle only about 39% of the time."
- app/content/exams/topic-1.3.json | .items[24].explain.text | note | Explanation has 4 sentences (limit 3). | Merge or cut to three sentences.
- app/content/exams/topic-1.3.json | .items[26].model | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.
- app/content/exams/topic-1.3.json | .items[26].rubric[3].text | note | Bare £ inside $...$ renders in italic maths type (AUTHORING). | Write `\\text{£}` inside the maths, or move the amount out of it.

## docs/curriculum.md (topic 1.3 coverage)
- docs/curriculum.md (topic 1.3 coverage) | Cover: integrals | warning | Improper integrals with an unbounded integrand ($\int_0^1 x^{-1/2}\,dx$) are never taught, though integrals l7 S7 promises them. They are standard on the 18.01 final. | Add to integrals l11: a ladder screen and a quiz item on $\int_0^1 x^{-p}\,dx$.
- docs/curriculum.md (topic 1.3 coverage) | Exit: 18.01 final | warning | No partial fractions anywhere in integrals (zero hits). 18.01 finals routinely set $\int \tfrac{dx}{x^2 - 1}$-type items. | Add a lesson or a level-3 screen block on partial fractions.
- docs/curriculum.md (topic 1.3 coverage) | Exit: 18.01 final | warning | No trigonometric substitution or integrals of trig powers, and no inverse trig functions: $\arctan$, $\arcsin$ and $\int \tfrac{dx}{1 + x^2}$ never appear in limits or integrals. | Add $\frac{d}{dx}\arctan x$ and $\arcsin x$ to limits l11 or l12 (implicit differentiation gives them), and a trig-substitution screen to integrals l9.
- docs/curriculum.md (topic 1.3 coverage) | Exit: 18.01 final | warning | No related rates, and no volumes of revolution, arc length or surface area. These are core 18.01 applications of derivatives and integrals. | Add a related-rates transfer to limits l12 and a volumes or arc length lesson to integrals level 2 or 3.
- docs/curriculum.md (topic 1.3 coverage) | Exit: 18.01 final | note | The mean value theorem is cited as a fact (integrals homework-3 model, taylor Lagrange remainder) but never taught. Hyperbolic functions are absent (minor for 18.01). | Add an MVT screen to limits l13 (Rolle then MVT), used later by the FTC proof.
- docs/curriculum.md (topic 1.3 coverage) | Cover: multiple integrals; Exit: 18.02 problem sets | note | Multivar covers double integrals (rectangles, general regions, polar) only: no triple integrals or general change of variables (Jacobian). Lagrange is taught only for $f(x, y)$ with one constraint; 18.02 sets also use three variables, two constraints and boundary checks for absolute extrema on closed regions. | Add one Lagrange screen in three variables (e.g. minimise $x^2 + y^2 + z^2$ on a plane) and one screen on checking the boundary of a closed region. Triple integrals can wait if "multiple" means double.
- docs/curriculum.md (topic 1.3 coverage) | Exam skills map | note | All 18 skills are tested and every exam item tests something taught (L'Hôpital in limits l16, Newton in taylor l3, ratio test in taylor l9-l10, parts in integrals l10, Kelly in limits l14). The gaps above are absent from the exam too, so passing it does not show 18.01-final readiness on those topics. | Add exam items once the gaps are taught.

## Fix pass

Fix agent, 2026-10-21. Status per finding: fixed, disputed (with reason) or deferred (with reason). Validator: 0 errors. Playthrough: all 55 touched files pass (40 lessons, 14 sets, exam topic-1.3).

Counts: integrals: deferred 1, disputed 1, fixed 43; limits: fixed 31; multivar: fixed 28; taylor: fixed 32; exam: fixed 5; coverage: deferred 7.

- integrals/homework-1.json | h-volume-profile explain | warning | fixed: reworded to "quietest mid-morning, at 10:00"; bars and graded answer unchanged
- integrals/homework-1.json | .items[3].explain.text | note | fixed
- integrals/homework-1.json | .items[5].prose | note | fixed
- integrals/homework-1.json | .items[7].prompt | note | fixed
- integrals/homework-1.json | .items[7].rubric[1].text | note | fixed
- integrals/homework-1.json | .items[7].rubric[2].text | note | fixed
- integrals/homework-1.json | .items[7].rubric[3].text | note | fixed
- integrals/homework-2.json | .items[8].rubric[9].text | note | fixed
- integrals/homework-3.json | .items[3].prose | note | fixed
- integrals/homework-3.json | .items[3].feedback.correct | note | fixed
- integrals/homework-3.json | .items[5].feedback.correct | note | fixed
- integrals/homework-3.json | .items[7].model | note | fixed
- integrals/l1-thin-rectangles.json | .screens[4].explain.text | note | fixed
- integrals/l1-thin-rectangles.json | .screens[5].widget.options[2].why | note | fixed
- integrals/l1-thin-rectangles.json | .screens[5].explain.text | note | fixed
- integrals/l1-thin-rectangles.json | .screens[9].prose | note | fixed
- integrals/l11-to-infinity.json | .quiz[2].explain.text | note | fixed
- integrals/l11-to-infinity.json | .quiz[2].feedback.correct | note | fixed
- integrals/l11-to-infinity.json | .screens[7].explain.text | note | fixed
- integrals/l11-to-infinity.json | .screens[8].explain.text | note | fixed
- integrals/l11-to-infinity.json | .screens[8].feedback.correct | note | fixed
- integrals/l13-average-as-integral.json | S9 | note | deferred: changing the strike to £105 breaks the screen's comparison with the lesson's own £100 uniform call (S6) and changes a graded answer; better resolved by changing homework-2 h-ev-triangle in a later pass
- integrals/l13-average-as-integral.json | S5 feedback byKey no-x | note | fixed
- integrals/l13-average-as-integral.json | .summary.trap | note | fixed
- integrals/l13-average-as-integral.json | .quiz[3].explain.text | note | fixed
- integrals/l13-average-as-integral.json | .screens[5].explain.text | note | fixed
- integrals/l13-average-as-integral.json | .screens[8].explain.text | note | fixed
- integrals/l2-thinner.json | .screens[1].prose | note | fixed
- integrals/l3-signed-area.json | .screens[1].prose | note | fixed
- integrals/l3-signed-area.json | .screens[1].feedback.byKey.crossing | note | fixed
- integrals/l3-signed-area.json | .screens[2].prose | note | fixed
- integrals/l4-accumulating-a-rate.json | quiz[3] (Q4) | note | disputed: the prose already reads "Interest accrues daily on an actual/365 basis"; no edit needed
- integrals/l4-accumulating-a-rate.json | .screens[2].prose | note | fixed
- integrals/l4-accumulating-a-rate.json | .screens[7].widget.lines[0].text | note | fixed
- integrals/l4-accumulating-a-rate.json | .screens[7].widget.lines[1].text | note | fixed
- integrals/l4-accumulating-a-rate.json | .quiz[0].prose | note | fixed
- integrals/l4-accumulating-a-rate.json | .quiz[3].explain.text | note | fixed
- integrals/l4-accumulating-a-rate.json | .screens[4].explain.text | note | fixed
- integrals/l4-accumulating-a-rate.json | .screens[8].explain.text | note | fixed
- integrals/l5-area-undoes-slope.json | .screens[0].explain.text | note | fixed
- integrals/l5-area-undoes-slope.json | .screens[5].feedback.byKey.area | note | fixed
- integrals/l7-evaluating.json | S7 explain | warning | fixed: promise replaced by "such integrals have no finite value"; the missing l11 screen is a coverage gap (backlog 383)
- integrals/l9-undo-chain.json | .screens[7].explain.text | note | fixed
- integrals/review-1.json | .items[8].explain.text | note | fixed
- integrals/review-1.json | .items[8].feedback.correct | note | fixed
- limits/homework-1.json | .items[8].rubric[2].text | note | fixed
- limits/homework-2.json | hw2-negative-power explain | warning | fixed
- limits/homework-2.json | hw2-corners model (d) | note | fixed
- limits/homework-3.json | h-portfolio-correlated explain | note | fixed
- limits/homework-4.json | h-second-order feedback.correct vs explain | note | fixed: both now say "about 6.5p" (84.0947 − 84.0292 = 0.0655; "6p" would round the wrong way)
- limits/l1-getting-closer.json | S6 hint nudge | warning | fixed
- limits/l1-getting-closer.json | .screens[0].prose | note | fixed
- limits/l1-getting-closer.json | .screens[3].widget.options[1].why | note | fixed
- limits/l1-getting-closer.json | .screens[5].widget.options[0].text | note | fixed
- limits/l1-getting-closer.json | .screens[7].prose | note | fixed
- limits/l1-getting-closer.json | .screens[9].prose | note | fixed
- limits/l1-getting-closer.json | .summary.ideas[0] | note | fixed
- limits/l1-getting-closer.json | .quiz[3].explain.text | note | fixed
- limits/l10-inside-function.json | S11 explain | note | fixed
- limits/l12-implicit.json | S7 feedback byKey no-y-prime | warning | fixed: reworded as proposed; note the option's own canvas does draw the dashed segment on Show why, so the premise was only partly right
- limits/l12-implicit.json | S10 | note | fixed
- limits/l2-computing-limits.json | S8 explain + summary.ideas[1] | warning | fixed
- limits/l2-computing-limits.json | S8 / summary.ideas[2] | note | fixed
- limits/l2-computing-limits.json | .screens[2].prose | note | fixed
- limits/l3-without-lifting.json | .screens[0].hints[2].text | note | fixed
- limits/l3-without-lifting.json | .screens[0].feedback.correct | note | fixed
- limits/l3-without-lifting.json | .screens[6].explain.text | note | fixed
- limits/l3-without-lifting.json | .screens[9].explain.text | note | fixed
- limits/l3-without-lifting.json | .summary.ideas[0] | note | fixed
- limits/l4-far-out.json | S2 explain, excanvas, option `equal` why | error | fixed
- limits/l4-far-out.json | .screens[6].prose | note | fixed
- limits/l5-instant-speed.json | S10 explain | note | fixed
- limits/l6-first-principles.json | .summary.ideas[2] | note | fixed
- limits/l8-slope-graph.json | S9 explain + hint point | warning | fixed
- limits/l8-slope-graph.json | .screens[1].explain.text | note | fixed
- limits/l9-products-quotients.json | S10 order item q2 | note | fixed
- multivar/homework-2.json | h-plane-expr wrong[fy] | error | fixed
- multivar/homework-2.json | .items[4].prose | note | fixed
- multivar/homework-2.json | .items[4].widget.how | note | fixed
- multivar/homework-4.json | .items[7].rubric[0].text | note | fixed
- multivar/homework-4.json | .items[3].feedback.correct | note | fixed
- multivar/homework-4.json | .items[3].widget.accept | note | fixed
- multivar/l1-two-inputs.json | .summary.ideas[0] | note | fixed
- multivar/l10-second-derivative-test.json | .screens[0].widget.options[2].why | note | fixed
- multivar/l10-second-derivative-test.json | .screens[7].explain.text | note | fixed
- multivar/l13-volume.json | .screens[1].prose | note | fixed
- multivar/l13-volume.json | .screens[9].hints[2].text | note | fixed
- multivar/l14-other-regions.json | .screens[8].widget.lines[0].text | note | fixed
- multivar/l14-other-regions.json | .summary.ideas[2] | note | fixed
- multivar/l15-polar.json | .screens[1].prose | note | fixed
- multivar/l15-polar.json | .screens[5].explain.text | note | fixed
- multivar/l15-polar.json | .screens[6].prose | note | fixed
- multivar/l15-polar.json | .summary.ideas[0] | note | fixed
- multivar/l15-polar.json | .summary.trap | note | fixed
- multivar/l4-chain-two-inputs.json | S9 explain | note | fixed
- multivar/l4-chain-two-inputs.json | .screens[7].prose | note | fixed
- multivar/l5-steepest-climb.json | .screens[6].explain.text | note | fixed
- multivar/l5-steepest-climb.json | .screens[8].explain.text | note | fixed
- multivar/l7-tangent-planes.json | .screens[5].explain.text | note | fixed
- multivar/l8-walking-downhill.json | S6 explain | note | fixed
- multivar/l8-walking-downhill.json | .screens[8].widget.how | note | fixed
- multivar/review-1.json | r1-pnl-zero feedback byKey wrong-diagonal | error | fixed
- multivar/review-1.json | .items[0].feedback.byKey.centre-only | note | fixed
- multivar/review-1.json | .items[8].prose | note | fixed
- taylor/homework-1.json | h-long-bond model (d), (f) | note | fixed
- taylor/homework-1.json | .items[8].rubric[3].text | note | fixed
- taylor/homework-3.json | hw3-drag-longform model (a) | note | fixed
- taylor/homework-3.json | .items[0].explain.text | note | fixed
- taylor/homework-3.json | .items[2].prose | note | fixed
- taylor/l1-tangent-approx.json | S6 prose | error | fixed
- taylor/l1-tangent-approx.json | .screens[6].prose | note | fixed
- taylor/l10-how-far.json | S9 | note | fixed
- taylor/l11-bounding-error.json | S5 feedback byKey two-terms | error | fixed
- taylor/l11-bounding-error.json | S9 | note | fixed
- taylor/l11-bounding-error.json | .screens[4].explain.text | note | fixed
- taylor/l12-log-vs-simple.json | .screens[0].widget.label | note | fixed
- taylor/l12-log-vs-simple.json | .screens[9].widget.label | note | fixed
- taylor/l12-log-vs-simple.json | .summary.ideas[0] | note | fixed
- taylor/l12-log-vs-simple.json | .quiz[1].widget.label | note | fixed
- taylor/l12-log-vs-simple.json | .quiz[3].widget.label | note | fixed
- taylor/l2-how-wrong.json | S11 | note | fixed
- taylor/l3-newton.json | .screens[2].prose | note | fixed
- taylor/l3-newton.json | .summary.ideas[2] | note | fixed
- taylor/l4-duration.json | whole lesson | warning | fixed: rebuilt on a 7-year 5% annual coupon bond at 6%, computed twice (term sum and annuity closed form/Decimal): P = £94.42, P′ = −538.40, D = 5.70, tangent fall £5.38 vs true £5.20, convexity gap £0.19 at 7% and £1.60 at 9%, DV01 £5,384 on £10m face (true 1 bp loss £5,382.04); S1 says it builds on limits l15; homework-1 h-yield-93 and l8-convexity S1 now point to limits l15 for the 5-year bond
- taylor/l4-duration.json | S7 + quiz Q1 | note | fixed
- taylor/l5-curvature-term.json | S5 explain | error | fixed
- taylor/l6-matching-derivatives.json | S10 prose | warning | fixed
- taylor/l6-matching-derivatives.json | .screens[2].prose | note | fixed
- taylor/l7-standard-series.json | S10, quiz Q3, summary.formula.note | warning | fixed
- taylor/l7-standard-series.json | .screens[9].question | note | fixed
- taylor/l7-standard-series.json | .quiz[2].question | note | fixed
- taylor/l9-does-it-add-up.json | .screens[2].explain.text | note | fixed
- taylor/review-3.json | .items[7].question | note | fixed
- taylor/review-3.json | .items[7].widget.label | note | fixed
- taylor/review-3.json | .items[8].question | note | fixed
- taylor/review-3.json | .items[8].widget.label | note | fixed
- exams/topic-1.3.json | c-gauss-disc (I26) wrong[no-half] | error | fixed: distractor value changed 0.6321 → 0.3161 = ½(1 − e^{−1}) (recomputed), why now names integrating re^{−r²}
- exams/topic-1.3.json | c-gauss-disc (I26) explain | note | fixed
- exams/topic-1.3.json | .items[24].explain.text | note | fixed
- exams/topic-1.3.json | .items[26].model | note | fixed
- exams/topic-1.3.json | .items[26].rubric[3].text | note | fixed
- docs/curriculum.md (topic 1.3 coverage) | Cover: integrals | warning | deferred: coverage gap, recorded in docs/ENGINE-BACKLOG.md item 383; no lessons added in this pass
- docs/curriculum.md (topic 1.3 coverage) | Exit: 18.01 final | warning | deferred: coverage gap, recorded in docs/ENGINE-BACKLOG.md item 383; no lessons added in this pass
- docs/curriculum.md (topic 1.3 coverage) | Exit: 18.01 final | warning | deferred: coverage gap, recorded in docs/ENGINE-BACKLOG.md item 383; no lessons added in this pass
- docs/curriculum.md (topic 1.3 coverage) | Exit: 18.01 final | warning | deferred: coverage gap, recorded in docs/ENGINE-BACKLOG.md item 383; no lessons added in this pass
- docs/curriculum.md (topic 1.3 coverage) | Exit: 18.01 final | note | deferred: coverage gap, recorded in docs/ENGINE-BACKLOG.md item 383; no lessons added in this pass
- docs/curriculum.md (topic 1.3 coverage) | Cover: multiple integrals; Exit: 18.02 problem sets | note | deferred: coverage gap, recorded in docs/ENGINE-BACKLOG.md item 383; no lessons added in this pass
- docs/curriculum.md (topic 1.3 coverage) | Exam skills map | note | deferred: coverage gap, recorded in docs/ENGINE-BACKLOG.md item 383; no lessons added in this pass
