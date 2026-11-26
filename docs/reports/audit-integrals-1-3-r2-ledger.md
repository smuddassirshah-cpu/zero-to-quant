# Claim ledger: integrals levels 1 to 3, round 2 (audit integrals-1-3-r2)

Blind read at commit 83aadaaa. One row per definition, result, method step, convention, graded key, wrong option, slip value, hint, feedback line and explanation. Basis names the source, the derivation or the check in `docs/reports/integrals-L1-3-concepts-r2.py` (concepts-r2). Every row was read against the content; a `correct` row carries a code from the basis key below (one source and one recompute cover the rows of a file); every other row states its basis in full.

Rows: 4085. Verdicts: correct 4069, imprecise 13, misleading 1, wrong 2.

## Basis key

| code | basis |
|---|---|
| B1 | Riemann sums: Stewart 5.1, Spivak ch. 13 (lower and upper sums). Recomputed, concepts-r2 checks 'l1 ...' |
| B2 | Area as a limit of sums, monotone gap (f(b)-f(a))(b-a)/n: Stewart 5.1-5.2, Apostol I.1.3-1.4; sympy sums, concepts-r2 'l2 ...' |
| B3 | Definite integral, additivity and reversed limits: Stewart 5.2 properties 1-8, Spivak ch. 13 thm 4; concepts-r2 'l3 ...' |
| B4 | Net change theorem: Stewart 5.4; ACT/365 accrual by arithmetic; concepts-r2 'l4 ...' |
| B5 | As lessons l1 to l4; recomputed, concepts-r2 'review-1' |
| B6 | As lessons l1 to l4; sums by sympy, concepts-r2 'homework-1 ...' |
| B7 | Model answer re-derived line by line; closed forms by sympy in the concepts script |
| B8 | As lessons l1 to l4; concepts-r2 'problems-1 ...' |
| B9 | FTC part 1 with f continuous: Spivak ch. 14 thm 1, Stewart 5.3; A(x) = 2x^2 - x^3/3 recomputed, concepts-r2 'l5 ...' |
| B10 | Antiderivatives table: Stewart 4.9 / 5.4; each differentiated back in sympy, concepts-r2 'l6' |
| B11 | FTC part 2 (f continuous on [a,b], F' = f): Spivak ch. 14 cor., Stewart 5.3; improper at 0: Stewart 7.8; concepts-r2 'l7 ...' |
| B12 | Area between curves = integral of |f - g|: Stewart 6.1; quad recompute, concepts-r2 'l8' |
| B13 | As lessons l5 to l8; recomputed, concepts-r2 'review-2' |
| B14 | As lessons l5 to l8; FTC proof as Spivak ch. 14 thm 1; concepts-r2 'homework-2 ...' |
| B15 | As lessons l5 to l8; concepts-r2 'problems-2' |
| B16 | Template identity differentiated back in sympy, concepts-r2 'fluency ...'; slip formula re-derived |
| B17 | Template identity by FTC part 2, concepts-r2 'fluency ...'; slip formula re-derived; grade-all at 2 seeds |
| B18 | Substitution rule: Stewart 5.5 thms 4 and 6, Spivak ch. 19 thm 2; concepts-r2 'l9 ...' |
| B19 | Integration by parts: Stewart 7.1, Spivak ch. 19 thm 1; sympy differentiation back, concepts-r2 'l10 ...' |
| B20 | Improper integrals of type 1, p-test: Stewart 7.8 defn 1 and example 4, Apostol 10.23; sympy, concepts-r2 'l11' |
| B21 | Trapezium rule and its error bound K(b-a)^3/(12n^2): Stewart 7.7 thm 3; code run under the page's Pyodide (sweep) and concepts-r2 'l12 ...' |
| B22 | grade-all --code: solution passes, starter fails, each mutant fails its named test first |
| B23 | Swept under the page's Pyodide (docs/reports/integrals-L1-3-test-line-sweep-r2.mjs, results in the audit): natural codings of the named mistake fail this test first, or the line only describes its test |
| B24 | Average value 1/(b-a) int f: Stewart 6.5; E[g(X)] = int g f (law of the unconscious statistician): Casella and Berger 2.2; MC in concepts-r2 'l13 ...' |
| B25 | As lessons l9 to l13; recomputed, concepts-r2 'review-3' |
| B26 | As lessons l9 to l13; parts on [a,b] with C^1 u, v: Spivak ch. 19 thm 1; code run under Pyodide (sweep); concepts-r2 'homework-3 ...' |
| B27 | As lessons l9 to l13; Jensen's inequality (Casella and Berger 4.7.7); MC and quad in concepts-r2 'problems-3 ...' |

## Rows

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l1-thin-rectangles.json | screens[0].prose | How much area lies under the curve $f(x) = x^2$ between $x = 0$ and $x = 1$? Start by counting grid squares... | correct | B1 |
| l1-thin-rectangles.json | screens[0].canvas.state.caption | The curve $f(x) = x^2$. Each square is $\tfrac14$ by $\tfrac14$. | correct | B1 |
| l1-thin-rectangles.json | screens[0].question | Tap every square that lies completely under the curve. | correct | B1 |
| l1-thin-rectangles.json | screens[0].widget.answer | graded key (tap-regions): ["s31", "s41", "s42"] | correct | B1 |
| l1-thin-rectangles.json | screens[0].widget.wrong[0] | slip touched = ["s31", "s41", "s42", "s11", "s21", "s32", "s33", "s43", "s44"] is the value of the named mi... | correct | B1 |
| l1-thin-rectangles.json | screens[0].hints[0].text | A square counts only if all of it sits below the curve. | correct | B1 |
| l1-thin-rectangles.json | screens[0].hints[1].text | The curve stays low on the left. Look at the right half, near the bottom. | correct | B1 |
| l1-thin-rectangles.json | screens[0].hints[2].text | Three squares qualify: the bottom one in the third column, and the bottom two in the fourth column. | correct | B1 |
| l1-thin-rectangles.json | screens[0].feedback.correct | Three whole squares sit under the curve. | correct | B1 |
| l1-thin-rectangles.json | screens[0].feedback.generic | Not quite right. Tap only squares with no part of the curve inside them. | correct | B1 |
| l1-thin-rectangles.json | screens[0].feedback.byKey.touched | You also tapped squares the curve cuts through. Only part of each lies under the curve, so they cannot coun... | correct | B1 |
| l1-thin-rectangles.json | screens[0].feedback.byKey.s11 | The curve passes through that square, so only part of it is under the curve. | correct | B1 |
| l1-thin-rectangles.json | screens[0].feedback.byKey.s21 | The curve passes through that square, so only part of it is under the curve. | correct | B1 |
| l1-thin-rectangles.json | screens[0].feedback.byKey.s32 | The curve passes through that square, so only part of it is under the curve. | correct | B1 |
| l1-thin-rectangles.json | screens[0].feedback.byKey.s33 | The curve passes through that square, so only part of it is under the curve. | correct | B1 |
| l1-thin-rectangles.json | screens[0].feedback.byKey.s43 | The curve passes through that square, so only part of it is under the curve. | correct | B1 |
| l1-thin-rectangles.json | screens[0].feedback.byKey.s44 | The curve passes through that square, so only part of it is under the curve. | correct | B1 |
| l1-thin-rectangles.json | screens[0].feedback.byKey.s12 | That square sits above the curve. None of it is under. | correct | B1 |
| l1-thin-rectangles.json | screens[0].feedback.byKey.s13 | That square sits above the curve. None of it is under. | correct | B1 |
| l1-thin-rectangles.json | screens[0].feedback.byKey.s14 | That square sits above the curve. None of it is under. | correct | B1 |
| l1-thin-rectangles.json | screens[0].feedback.byKey.s22 | That square sits above the curve. None of it is under. | correct | B1 |
| l1-thin-rectangles.json | screens[0].feedback.byKey.s23 | That square sits above the curve. None of it is under. | correct | B1 |
| l1-thin-rectangles.json | screens[0].feedback.byKey.s24 | That square sits above the curve. None of it is under. | correct | B1 |
| l1-thin-rectangles.json | screens[0].feedback.byKey.s34 | That square sits above the curve. None of it is under. | correct | B1 |
| l1-thin-rectangles.json | screens[0].explain.text | Three squares sit fully under the curve, and the curve cuts through six more. Each square has area $\tfrac{... | correct | B1 |
| l1-thin-rectangles.json | screens[0].explain.canvas.caption | Inside: 3 squares. Cut by the curve: 6 more. | correct | B1 |
| l1-thin-rectangles.json | screens[1].prose | Squares are clumsy. Use thin upright rectangles instead. Each one is as tall as the curve at its right edge... | correct | B1 |
| l1-thin-rectangles.json | screens[1].canvas.params.functions[0].label | $f(x) = x^2$ | correct | B1 |
| l1-thin-rectangles.json | screens[1].question | What is the fewest rectangles that brings the total below 0.4? | correct | B1 |
| l1-thin-rectangles.json | screens[1].widget.answer | graded key (numeric): 8 | correct | B1 |
| l1-thin-rectangles.json | screens[1].widget.wrong[0] | slip seven = 7 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[1].widget.wrong[1] | slip nine = 9 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[1].widget.wrong[2] | slip one = 1 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[1].widget.accept | 8. Seven rectangles give 0.408, eight give 0.398. | correct | B1 |
| l1-thin-rectangles.json | screens[1].hints[0].text | Start at 1 and step the slider up one at a time. | correct | B1 |
| l1-thin-rectangles.json | screens[1].hints[1].text | Watch the total in the corner as you go past 6. | correct | B1 |
| l1-thin-rectangles.json | screens[1].hints[2].text | Seven rectangles give 0.408. Try one more. | correct | B1 |
| l1-thin-rectangles.json | screens[1].feedback.correct | Seven give 0.408 and eight give 0.398. | correct | B1 |
| l1-thin-rectangles.json | screens[1].feedback.generic | Not quite right. Step up one rectangle at a time and read the total each time. | correct | B1 |
| l1-thin-rectangles.json | screens[1].feedback.byKey.seven | At 7 rectangles the total reads 0.408, still above 0.4. | correct | B1 |
| l1-thin-rectangles.json | screens[1].feedback.byKey.nine | Nine works, but eight already gives 0.398. | correct | B1 |
| l1-thin-rectangles.json | screens[1].feedback.byKey.one | One rectangle gives a total of 1, the whole square. Add more. | correct | B1 |
| l1-thin-rectangles.json | screens[1].explain.text | The total fell from 1 with one rectangle to 0.398 with eight. Each rectangle pokes above the curve, so ever... | correct | B1 |
| l1-thin-rectangles.json | screens[2].prose | The total you read is a **Riemann sum**: width times height, added over every rectangle. With 4 rectangles ... | correct | B1 |
| l1-thin-rectangles.json | screens[2].canvas.params.functions[0].label | $f(x) = x^2$ | correct | B1 |
| l1-thin-rectangles.json | screens[2].canvas.state.caption | Heights: $f(\tfrac14) = \tfrac{1}{16}$, $f(\tfrac12) = \tfrac{4}{16}$, $f(\tfrac34) = \tfrac{9}{16}$, $f(1)... | correct | B1 |
| l1-thin-rectangles.json | screens[2].question | Compute the sum with 4 rectangles. Give a fraction or a decimal. | correct | B1 |
| l1-thin-rectangles.json | screens[2].widget.answer | graded key (numeric): 0.46875 | correct | B1 |
| l1-thin-rectangles.json | screens[2].widget.wrong[0] | slip no-width = 1.875 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[2].widget.wrong[1] | slip left = 0.21875 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[2].widget.wrong[2] | slip guess = 0.3333 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[2].widget.accept | $\tfrac{15}{32} = 0.46875$ | correct | B1 |
| l1-thin-rectangles.json | screens[2].hints[0].text | Each rectangle's area is $\tfrac14$ times its height. | correct | B1 |
| l1-thin-rectangles.json | screens[2].hints[1].text | Add the heights first: $\tfrac{1 + 4 + 9 + 16}{16}$. | correct | B1 |
| l1-thin-rectangles.json | screens[2].hints[2].text | The heights add to $\tfrac{30}{16}$. Multiply by the width $\tfrac14$ to get $\tfrac{30}{64}$. | correct | B1 |
| l1-thin-rectangles.json | screens[2].feedback.correct | $\tfrac14 \times \tfrac{30}{16} = \tfrac{15}{32}$. | correct | B1 |
| l1-thin-rectangles.json | screens[2].feedback.generic | Not quite right. Multiply each height by the width $\tfrac14$, then add. | correct | B1 |
| l1-thin-rectangles.json | screens[2].feedback.byKey.no-width | You added the heights but did not multiply by the width. Each rectangle is only $\tfrac14$ wide. | correct | B1 |
| l1-thin-rectangles.json | screens[2].feedback.byKey.left | You used heights at the left ends. Here each height comes from the right end. | correct | B1 |
| l1-thin-rectangles.json | screens[2].feedback.byKey.guess | That is close to the true area, but the question asks for the rectangles' total. They overshoot. | correct | B1 |
| l1-thin-rectangles.json | screens[2].explain.text | $\tfrac14\left(\tfrac{1}{16} + \tfrac{4}{16} + \tfrac{9}{16} + \tfrac{16}{16}\right) = \tfrac{30}{64} = 0.4... | correct | B1 |
| l1-thin-rectangles.json | screens[3].prose | Now take each height at the **left** end of its rectangle. The first rectangle starts at $x = 0$. | correct | B1 |
| l1-thin-rectangles.json | screens[3].canvas.params.functions[0].label | $f(x) = x^2$ | correct | B1 |
| l1-thin-rectangles.json | screens[3].canvas.state.caption | Left ends: $0, \tfrac14, \tfrac12, \tfrac34$ | correct | B1 |
| l1-thin-rectangles.json | screens[3].question | Compute the left sum $L_4$. | correct | B1 |
| l1-thin-rectangles.json | screens[3].widget.answer | graded key (numeric): 0.21875 | correct | B1 |
| l1-thin-rectangles.json | screens[3].widget.wrong[0] | slip right-ends = 0.46875 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[3].widget.wrong[1] | slip no-width = 0.875 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[3].widget.wrong[2] | slip three = 0.29167 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[3].widget.accept | $\tfrac{7}{32} = 0.21875$ | correct | B1 |
| l1-thin-rectangles.json | screens[3].hints[0].text | List the four heights $f(0), f(\tfrac14), f(\tfrac12), f(\tfrac34)$. | correct | B1 |
| l1-thin-rectangles.json | screens[3].hints[1].text | The heights are $0, \tfrac{1}{16}, \tfrac{4}{16}, \tfrac{9}{16}$. | correct | B1 |
| l1-thin-rectangles.json | screens[3].hints[2].text | They add to $\tfrac{14}{16}$. Times $\tfrac14$ gives $\tfrac{14}{64} = \tfrac{7}{32}$. | correct | B1 |
| l1-thin-rectangles.json | screens[3].feedback.correct | $\tfrac14 \times \tfrac{14}{16} = \tfrac{7}{32}$. | correct | B1 |
| l1-thin-rectangles.json | screens[3].feedback.generic | Not quite right. Use the heights at $0, \tfrac14, \tfrac12, \tfrac34$, each times $\tfrac14$. | correct | B1 |
| l1-thin-rectangles.json | screens[3].feedback.byKey.right-ends | You used the right ends again: $\tfrac14$ up to 1. The left ends are $0, \tfrac14, \tfrac12, \tfrac34$. | correct | B1 |
| l1-thin-rectangles.json | screens[3].feedback.byKey.no-width | You added the heights but did not multiply by the width $\tfrac14$. | correct | B1 |
| l1-thin-rectangles.json | screens[3].feedback.byKey.three | You left out the flat first rectangle and spread the width over three. It has height 0, but it is still a q... | correct | B1 |
| l1-thin-rectangles.json | screens[3].explain.text | $\tfrac14\left(0 + \tfrac{1}{16} + \tfrac{4}{16} + \tfrac{9}{16}\right) = \tfrac{7}{32} = 0.21875$. The fir... | correct | B1 |
| l1-thin-rectangles.json | screens[4].prose | A third choice: take each height at the **midpoint** of its rectangle, at $x = \tfrac18, \tfrac38, \tfrac58... | correct | B1 |
| l1-thin-rectangles.json | screens[4].canvas.params.functions[0].label | $f(x) = x^2$ | correct | B1 |
| l1-thin-rectangles.json | screens[4].question | Compute the midpoint sum $M_4$. | correct | B1 |
| l1-thin-rectangles.json | screens[4].widget.answer | graded key (numeric): 0.328125 | correct | B1 |
| l1-thin-rectangles.json | screens[4].widget.wrong[0] | slip average-sums = 0.34375 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[4].widget.wrong[1] | slip no-square = 0.5 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[4].widget.wrong[2] | slip no-width = 1.3125 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[4].widget.accept | $\tfrac{21}{64} = 0.328125$ | correct | B1 |
| l1-thin-rectangles.json | screens[4].hints[0].text | Square each midpoint to get its height. | correct | B1 |
| l1-thin-rectangles.json | screens[4].hints[1].text | $f(\tfrac18) = \tfrac{1}{64}$, $f(\tfrac38) = \tfrac{9}{64}$, $f(\tfrac58) = \tfrac{25}{64}$, $f(\tfrac78) ... | correct | B1 |
| l1-thin-rectangles.json | screens[4].hints[2].text | The heights add to $\tfrac{84}{64}$. Times $\tfrac14$ gives $\tfrac{84}{256} = \tfrac{21}{64}$. | correct | B1 |
| l1-thin-rectangles.json | screens[4].feedback.correct | $\tfrac14 \times \tfrac{84}{64} = \tfrac{21}{64}$. | correct | B1 |
| l1-thin-rectangles.json | screens[4].feedback.generic | Not quite right. Square each midpoint, add the four heights, then multiply by $\tfrac14$. | correct | B1 |
| l1-thin-rectangles.json | screens[4].feedback.byKey.average-sums | You averaged $L_4$ and $R_4$. The midpoint sum uses the curve's height at each midpoint instead. | correct | B1 |
| l1-thin-rectangles.json | screens[4].feedback.byKey.no-square | You used the midpoints themselves as heights. The height is $f(x) = x^2$, so square them first. | correct | B1 |
| l1-thin-rectangles.json | screens[4].feedback.byKey.no-width | You added the heights but did not multiply by the width $\tfrac14$. | correct | B1 |
| l1-thin-rectangles.json | screens[4].explain.text | $M_4 = \tfrac{21}{64} = 0.328125$. Each rectangle overshoots the curve on one side and falls short on the o... | correct | B1 |
| l1-thin-rectangles.json | screens[5].prose | Next lesson shows the true area is $\tfrac13$. So $L_4 = 0.219$ is too small and $R_4 = 0.469$ is too big. ... | correct | B1 |
| l1-thin-rectangles.json | screens[5].canvas.params.functions[0].label | $f(x) = x^2$ | correct | B1 |
| l1-thin-rectangles.json | screens[5].question | Why is the left sum too small here? | correct | B1 |
| l1-thin-rectangles.json | screens[5].widget.options[0] | graded key (choice): The curve rises, so each left end is the lowest point of its strip. Every rectangle st... | correct | B1 |
| l1-thin-rectangles.json | screens[5].widget.options[1].text | wrong option, wrong under every convention: The first rectangle is flat, so it loses area | correct | B1 |
| l1-thin-rectangles.json | screens[5].widget.options[1].why | That flat rectangle misses some area, but so does every other one. Each stops short of the curve on its rig... | correct | B1 |
| l1-thin-rectangles.json | screens[5].widget.options[2].text | wrong option, wrong under every convention: Left sums are always too small | correct | B1 |
| l1-thin-rectangles.json | screens[5].widget.options[2].why | Only on a rising curve. If the curve falls, each left end is the highest point of its strip. Then the left ... | correct | B1 |
| l1-thin-rectangles.json | screens[5].widget.options[3].text | wrong option, wrong under every convention: Four is too few. With 100 rectangles the left sum would be too big | correct | B1 |
| l1-thin-rectangles.json | screens[5].widget.options[3].why | More rectangles shrink the shortfall, but on a rising curve every left rectangle still sits under it. The l... | correct | B1 |
| l1-thin-rectangles.json | screens[5].hints[0].text | Compare each rectangle's top with the curve above its strip. | correct | B1 |
| l1-thin-rectangles.json | screens[5].hints[1].text | Look at where each rectangle touches the curve. | correct | B1 |
| l1-thin-rectangles.json | screens[5].hints[2].text | Each left rectangle touches the curve at its left corner only. The curve climbs above it across the strip. | correct | B1 |
| l1-thin-rectangles.json | screens[5].feedback.correct | On a rising curve each strip is lowest at its left end. | correct | B1 |
| l1-thin-rectangles.json | screens[5].feedback.generic | Not quite right. Look at the gap between each rectangle's top and the curve. | correct | B1 |
| l1-thin-rectangles.json | screens[5].feedback.byKey.always | Only on a rising curve. If the curve falls, the left ends are the highest points and the left sum is too big. | correct | B1 |
| l1-thin-rectangles.json | screens[5].explain.text | On a rising curve each strip is lowest at its left end, so every left rectangle misses a sliver. Every righ... | correct | B1 |
| l1-thin-rectangles.json | screens[6].prose | New interval. We want the area under $f(x) = x^2$ from $x = 1$ to $x = 2$, again with 4 rectangles. | correct | B1 |
| l1-thin-rectangles.json | screens[6].canvas.params.functions[0].label | $f(x) = x^2$ | correct | B1 |
| l1-thin-rectangles.json | screens[6].canvas.state.vlines[0].label | $x = 1$ | correct | B1 |
| l1-thin-rectangles.json | screens[6].canvas.state.vlines[1].label | $x = 2$ | correct | B1 |
| l1-thin-rectangles.json | screens[6].question | Compute the left sum $L_4$ as a decimal. | correct | B1 |
| l1-thin-rectangles.json | screens[6].widget.answer | graded key (numeric): 1.96875 | correct | B1 |
| l1-thin-rectangles.json | screens[6].widget.wrong[0] | slip wrong-end = 2.71875 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[6].widget.wrong[1] | slip old-points = 0.21875 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[6].widget.wrong[2] | slip five = 2.96875 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[6].widget.wrong[3] | slip no-width = 7.875 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[6].widget.accept | 1.96875: $0.25 \times (1 + 1.5625 + 2.25 + 3.0625)$ | correct | B1 |
| l1-thin-rectangles.json | screens[6].hints[0].text | Find the width first: $\Delta x = \tfrac{2 - 1}{4}$. | correct | B1 |
| l1-thin-rectangles.json | screens[6].hints[1].text | The left ends are 1, 1.25, 1.5 and 1.75. | correct | B1 |
| l1-thin-rectangles.json | screens[6].hints[2].text | The heights 1, 1.5625, 2.25 and 3.0625 add to 7.875. Multiply by 0.25. | correct | B1 |
| l1-thin-rectangles.json | screens[6].feedback.correct | $0.25 \times 7.875 = 1.96875$. | correct | B1 |
| l1-thin-rectangles.json | screens[6].feedback.generic | Not quite right. Use the left ends 1, 1.25, 1.5 and 1.75, each strip 0.25 wide. | correct | B1 |
| l1-thin-rectangles.json | screens[6].feedback.byKey.wrong-end | You took heights at the right ends, 1.25 up to 2. The left ends start at $x = 1$ and stop at 1.75. | correct | B1 |
| l1-thin-rectangles.json | screens[6].feedback.byKey.old-points | You reused the points $0, \tfrac14, \tfrac12, \tfrac34$ from $[0, 1]$. On $[1, 2]$ the left ends are 1, 1.2... | correct | B1 |
| l1-thin-rectangles.json | screens[6].feedback.byKey.five | You used five heights, both ends included. Four rectangles need four heights. | correct | B1 |
| l1-thin-rectangles.json | screens[6].feedback.byKey.no-width | You added the heights but did not multiply by the width 0.25. | correct | B1 |
| l1-thin-rectangles.json | screens[6].explain.text | The left ends 1, 1.25, 1.5 and 1.75 give $0.25 \times 7.875 = 1.96875$. The right sum is 2.71875 and the tr... | correct | B1 |
| l1-thin-rectangles.json | screens[7].prose | You built every sum the same way. Split $[a, b]$ into $n$ strips of width $\Delta x = \dfrac{b - a}{n}$, pi... | correct | B1 |
| l1-thin-rectangles.json | screens[7].question | On $[2, 5]$ with $n = 6$, where does strip 4 start? | correct | B1 |
| l1-thin-rectangles.json | screens[7].widget.options[0] | graded key (choice): $x = 3.5$ | correct | B1 |
| l1-thin-rectangles.json | screens[7].widget.options[1].text | wrong option, wrong under every convention: $x = 4$ | correct | B1 |
| l1-thin-rectangles.json | screens[7].widget.options[1].why | That is where strip 4 ends: $2 + 4 \times 0.5$. It starts one width earlier. | correct | B1 |
| l1-thin-rectangles.json | screens[7].widget.options[2].text | wrong option, wrong under every convention: $x = 3.75$ | correct | B1 |
| l1-thin-rectangles.json | screens[7].widget.options[2].why | That is the middle of strip 4. It starts a half width earlier. | correct | B1 |
| l1-thin-rectangles.json | screens[7].widget.options[3].text | wrong option, wrong under every convention: $x = 2.5$ | correct | B1 |
| l1-thin-rectangles.json | screens[7].widget.options[3].why | You used a width of $\tfrac16$. The six strips share $[2, 5]$, so each is $\tfrac36 = 0.5$ wide. | correct | B1 |
| l1-thin-rectangles.json | screens[7].hints[0].text | Find $\Delta x$ first. | correct | B1 |
| l1-thin-rectangles.json | screens[7].hints[1].text | $\Delta x = 0.5$. Strip 4 starts after three whole strips: $2 + 3 \times 0.5$. | correct | B1 |
| l1-thin-rectangles.json | screens[7].feedback.correct | Strip 4 runs from 3.5 to 4. | correct | B1 |
| l1-thin-rectangles.json | screens[7].feedback.generic | Not quite right. Each strip is $\tfrac{5 - 2}{6} = 0.5$ wide; count three strips along from 2. | correct | B1 |
| l1-thin-rectangles.json | screens[7].explain.text | $\Delta x = \tfrac{5 - 2}{6} = 0.5$. Strip $k$ runs from $a + (k - 1)\Delta x$ to $a + k\Delta x$, so strip... | correct | B1 |
| l1-thin-rectangles.json | screens[8].prose | On $[0, 1]$ with $n$ strips, $\Delta x = \tfrac1n$ and strip $k$ ends at $x_k = \tfrac{k}{n}$. So the right... | correct | B1 |
| l1-thin-rectangles.json | screens[8].question | For $f(x) = x^2$, write the area of rectangle $k$ in terms of $k$ and $n$. | correct | B1 |
| l1-thin-rectangles.json | screens[8].widget.answer | graded key (expression): "\\frac{k^2}{n^3}" | correct | B1 |
| l1-thin-rectangles.json | screens[8].widget.wrong[0] | slip no-width = "\\frac{k^2}{n^2}" is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[8].widget.wrong[1] | slip no-square = "\\frac{k}{n^2}" is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[8].hints[0].text | Area is height times width. | correct | B1 |
| l1-thin-rectangles.json | screens[8].hints[1].text | The height is $f(\tfrac{k}{n}) = \tfrac{k^2}{n^2}$ and the width is $\tfrac1n$. | correct | B1 |
| l1-thin-rectangles.json | screens[8].hints[2].text | $\tfrac{k^2}{n^2} \times \tfrac1n = \tfrac{k^2}{n^3}$. | correct | B1 |
| l1-thin-rectangles.json | screens[8].feedback.correct | Height $\tfrac{k^2}{n^2}$ times width $\tfrac1n$. | correct | B1 |
| l1-thin-rectangles.json | screens[8].feedback.generic | Not quite right. Square $\tfrac{k}{n}$ for the height, then multiply by the width $\tfrac1n$. | correct | B1 |
| l1-thin-rectangles.json | screens[8].feedback.byKey.no-width | That is the height alone. Multiply by the width $\tfrac1n$ to get the area. | correct | B1 |
| l1-thin-rectangles.json | screens[8].feedback.byKey.no-square | You used $\tfrac{k}{n}$ as the height. The height is $f(\tfrac{k}{n})$, its square. | correct | B1 |
| l1-thin-rectangles.json | screens[8].explain.text | Rectangle $k$ has area $\tfrac{k^2}{n^2} \cdot \tfrac1n = \tfrac{k^2}{n^3}$, so $R_n = \tfrac{1}{n^3}\left(... | correct | B1 |
| l1-thin-rectangles.json | screens[9].prose | In a risk model, the chance that tomorrow's return lands between two values is the area under this curve. R... | correct | B1 |
| l1-thin-rectangles.json | screens[9].question | Estimate the chance of a return between 0 and 1 standard deviation with the midpoint sum. | correct | B1 |
| l1-thin-rectangles.json | screens[9].widget.answer | graded key (numeric): 0.342 | correct | B1 |
| l1-thin-rectangles.json | screens[9].widget.wrong[0] | slip no-width = 1.368 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[9].widget.wrong[1] | slip percent = 34.2 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[9].widget.wrong[2] | slip one-height = 0.3958 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | screens[9].widget.accept | 0.342: $0.25 \times 1.368$. The exact chance is 0.3413. | correct | B1 |
| l1-thin-rectangles.json | screens[9].hints[0].text | Each strip is $\tfrac14$ wide. | correct | B1 |
| l1-thin-rectangles.json | screens[9].hints[1].text | The four heights add to 1.368. | correct | B1 |
| l1-thin-rectangles.json | screens[9].hints[2].text | $0.25 \times 1.368 = 0.342$. | correct | B1 |
| l1-thin-rectangles.json | screens[9].feedback.correct | $0.25 \times 1.368 = 0.342$. | correct | B1 |
| l1-thin-rectangles.json | screens[9].feedback.generic | Not quite right. Add the four heights, then multiply by the strip width 0.25. | correct | B1 |
| l1-thin-rectangles.json | screens[9].feedback.byKey.no-width | You added the heights but did not multiply by the width 0.25. A chance cannot exceed 1. | correct | B1 |
| l1-thin-rectangles.json | screens[9].feedback.byKey.percent | Give the chance as a decimal: 0.342, not 34.2. | correct | B1 |
| l1-thin-rectangles.json | screens[9].feedback.byKey.one-height | You read one height. Area needs all four rectangles, each height times 0.25. | correct | B1 |
| l1-thin-rectangles.json | screens[9].explain.text | $0.25 \times (0.3958 + 0.3719 + 0.3282 + 0.2721) = 0.342$. The exact chance is 0.3413, so four rectangles l... | correct | B1 |
| l1-thin-rectangles.json | summary.ideas[0] | Rectangles under a curve estimate its area: add width times height over every strip. | correct | B1 |
| l1-thin-rectangles.json | summary.ideas[1] | Left, right and midpoint sums take each height at a different point of its strip. | correct | B1 |
| l1-thin-rectangles.json | summary.ideas[2] | On a rising curve the left sum is too small and the right sum too big. On a falling curve they swap. | correct | B1 |
| l1-thin-rectangles.json | summary.formula.name | Riemann sum | correct | B1 |
| l1-thin-rectangles.json | summary.formula.tex | \sum_{k=1}^{n} f(x_k^*)\,\Delta x, \qquad \Delta x = \dfrac{b - a}{n} | correct | B1 |
| l1-thin-rectangles.json | summary.formula.note | $x_k^*$ is the left end, right end or midpoint of strip $k$. | correct | B1 |
| l1-thin-rectangles.json | summary.trap | Left ends start at $a$ and stop one width before $b$. Move them with the interval. | correct | B1 |
| l1-thin-rectangles.json | quiz[0].prose | Take $f(x) = 2x + 1$ on $[0, 2]$ with 4 rectangles. | correct | B1 |
| l1-thin-rectangles.json | quiz[0].question | What is the right sum $R_4$? | correct | B1 |
| l1-thin-rectangles.json | quiz[0].widget.answer | graded key (numeric): 7 | correct | B1 |
| l1-thin-rectangles.json | quiz[0].widget.wrong[0] | slip left = 5 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | quiz[0].widget.wrong[1] | slip no-width = 14 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | quiz[0].widget.wrong[2] | slip exact = 6 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | quiz[0].widget.accept | 7: $0.5 \times (2 + 3 + 4 + 5)$ | correct | B1 |
| l1-thin-rectangles.json | quiz[0].feedback.correct | $0.5 \times (2 + 3 + 4 + 5) = 7$. | correct | B1 |
| l1-thin-rectangles.json | quiz[0].feedback.generic | Not quite right. The width is 0.5 and the right ends are 0.5, 1, 1.5 and 2. | correct | B1 |
| l1-thin-rectangles.json | quiz[0].feedback.byKey.left | You used the left ends 0, 0.5, 1 and 1.5. The right sum uses 0.5, 1, 1.5 and 2. | correct | B1 |
| l1-thin-rectangles.json | quiz[0].feedback.byKey.no-width | You added the heights but did not multiply by the width 0.5. | correct | B1 |
| l1-thin-rectangles.json | quiz[0].feedback.byKey.exact | 6 is the exact area. The right sum overshoots it, because the line rises. | correct | B1 |
| l1-thin-rectangles.json | quiz[0].explain.text | $\Delta x = 0.5$ and the right ends 0.5, 1, 1.5, 2 give heights 2, 3, 4, 5. So $R_4 = 0.5 \times 14 = 7$. T... | correct | B1 |
| l1-thin-rectangles.json | quiz[1].prose | For $f(x) = x^2$ on $[0, 1]$, the right sum with 2 rectangles is $R_2 = 0.625$. | correct | B1 |
| l1-thin-rectangles.json | quiz[1].question | What happens to the right sum when you use 4 rectangles instead? | correct | B1 |
| l1-thin-rectangles.json | quiz[1].widget.options[0] | graded key (choice): It gets smaller | correct | B1 |
| l1-thin-rectangles.json | quiz[1].widget.options[1].text | wrong option, wrong under every convention: It gets bigger, because there are more rectangles | correct | B1 |
| l1-thin-rectangles.json | quiz[1].widget.options[1].why | More rectangles is not more area. Thinner right rectangles poke above the curve less, so the total falls. | correct | B1 |
| l1-thin-rectangles.json | quiz[1].widget.options[2].text | wrong option, wrong under every convention: It stays at 0.625, because the area has not changed | correct | B1 |
| l1-thin-rectangles.json | quiz[1].widget.options[2].why | The area is fixed, but the estimate is not. Each choice of rectangles gives its own total. | correct | B1 |
| l1-thin-rectangles.json | quiz[1].feedback.correct | $R_4 = 0.469$, smaller than 0.625. | correct | B1 |
| l1-thin-rectangles.json | quiz[1].feedback.generic | Not quite right. Think about how far the right rectangles overshoot the curve. | correct | B1 |
| l1-thin-rectangles.json | quiz[1].explain.text | $R_4 = 0.469$, down from $R_2 = 0.625$. Right rectangles overshoot a rising curve, and thinner ones oversho... | correct | B1 |
| l1-thin-rectangles.json | quiz[2].prose | Take $f(x) = x^3$ on $[0, 2]$ with 2 rectangles. | correct | B1 |
| l1-thin-rectangles.json | quiz[2].question | What is the midpoint sum $M_2$? | correct | B1 |
| l1-thin-rectangles.json | quiz[2].widget.answer | graded key (numeric): 3.5 | correct | B1 |
| l1-thin-rectangles.json | quiz[2].widget.wrong[0] | slip average = 5 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | quiz[2].widget.wrong[1] | slip no-cube = 2 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | quiz[2].widget.wrong[2] | slip left = 1 is the value of the named mistake and is not a correct answer | correct | B1 |
| l1-thin-rectangles.json | quiz[2].widget.accept | 3.5: $1 \times (0.125 + 3.375)$ | correct | B1 |
| l1-thin-rectangles.json | quiz[2].feedback.correct | $1 \times (0.5^3 + 1.5^3) = 3.5$. | correct | B1 |
| l1-thin-rectangles.json | quiz[2].feedback.generic | Not quite right. The midpoints are 0.5 and 1.5, and each strip is 1 wide. | correct | B1 |
| l1-thin-rectangles.json | quiz[2].feedback.byKey.average | You averaged the left sum 1 and the right sum 9. The midpoint sum cubes the midpoints 0.5 and 1.5. | correct | B1 |
| l1-thin-rectangles.json | quiz[2].feedback.byKey.no-cube | You used the midpoints as heights. Cube them first: $0.5^3$ and $1.5^3$. | correct | B1 |
| l1-thin-rectangles.json | quiz[2].feedback.byKey.left | You used the left ends 0 and 1. The midpoints are 0.5 and 1.5. | correct | B1 |
| l1-thin-rectangles.json | quiz[2].explain.text | The strips are $[0, 1]$ and $[1, 2]$, with midpoints 0.5 and 1.5. Heights $0.125$ and $3.375$ give $M_2 = 3... | correct | B1 |
| l1-thin-rectangles.json | quiz[3].prose | You want the left sum of some $f$ on $[0, 2]$ with $n = 5$. | correct | B1 |
| l1-thin-rectangles.json | quiz[3].question | At which points do you evaluate $f$? | correct | B1 |
| l1-thin-rectangles.json | quiz[3].widget.options[0] | graded key (choice): $0,\ 0.4,\ 0.8,\ 1.2,\ 1.6$ | correct | B1 |
| l1-thin-rectangles.json | quiz[3].widget.options[1].text | wrong option, wrong under every convention: $0.4,\ 0.8,\ 1.2,\ 1.6,\ 2$ | correct | B1 |
| l1-thin-rectangles.json | quiz[3].widget.options[1].why | Those are the right ends. The left sum starts at 0 and stops one width before 2. | correct | B1 |
| l1-thin-rectangles.json | quiz[3].widget.options[2].text | wrong option, wrong under every convention: $0,\ 0.5,\ 1,\ 1.5,\ 2$ | correct | B1 |
| l1-thin-rectangles.json | quiz[3].widget.options[2].why | Those are five points 0.5 apart, which makes four strips. Five strips on $[0, 2]$ are each 0.4 wide. | correct | B1 |
| l1-thin-rectangles.json | quiz[3].widget.options[3].text | wrong option, wrong under every convention: $0,\ 0.4,\ 0.8,\ 1.2,\ 1.6,\ 2$ | correct | B1 |
| l1-thin-rectangles.json | quiz[3].widget.options[3].why | That is six points, both ends included. Five rectangles need five heights. | correct | B1 |
| l1-thin-rectangles.json | quiz[3].feedback.correct | Width 0.4, starting at 0. | correct | B1 |
| l1-thin-rectangles.json | quiz[3].feedback.generic | Not quite right. Find the width, then start at the left end of the interval. | correct | B1 |
| l1-thin-rectangles.json | quiz[3].explain.text | $\Delta x = \tfrac{2 - 0}{5} = 0.4$. The left ends are $0, 0.4, 0.8, 1.2$ and $1.6$; the last strip runs fr... | correct | B1 |
| l2-thinner.json | screens[0].prose | Top: the left sum for $f(x) = x^2$ on $[0, 1]$. Bottom: the right sum. The true area sits between them. Sli... | correct | B2 |
| l2-thinner.json | screens[0].canvas.derive.caption | $n$ = {{n}}. Gap $R_n - L_n$ = {{fixed(1/n, 4)}}. Error $R_n - \tfrac13$ = {{fixed((3*n+1)/(6*n*n), 4)}} | correct | B2 |
| l2-thinner.json | screens[0].question | What is the smallest $n$ that makes the gap between the two sums 0.05 or less? | correct | B2 |
| l2-thinner.json | screens[0].widget.answer | graded key (numeric): 20 | correct | B2 |
| l2-thinner.json | screens[0].widget.wrong[0] | slip nineteen = 19 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | screens[0].widget.wrong[1] | slip twentyone = 21 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | screens[0].widget.wrong[2] | slip ten = 10 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | screens[0].widget.accept | 20: the gap is exactly $\tfrac{1}{20} = 0.05$. | correct | B2 |
| l2-thinner.json | screens[0].hints[0].text | Read the gap in the caption as you slide. | correct | B2 |
| l2-thinner.json | screens[0].hints[1].text | The gap is 0.1 at $n = 10$. How far must you go to halve it? | correct | B2 |
| l2-thinner.json | screens[0].hints[2].text | At $n = 20$ the gap reads 0.0500. | correct | B2 |
| l2-thinner.json | screens[0].feedback.correct | At $n = 20$ the gap is exactly 0.05. | correct | B2 |
| l2-thinner.json | screens[0].feedback.generic | Not quite right. Slide until the gap first reads 0.0500 or less. | correct | B2 |
| l2-thinner.json | screens[0].feedback.byKey.nineteen | At $n = 19$ the gap is 0.0526, just above 0.05. | correct | B2 |
| l2-thinner.json | screens[0].feedback.byKey.twentyone | 21 works, but 20 already gives a gap of exactly 0.05. | correct | B2 |
| l2-thinner.json | screens[0].feedback.byKey.ten | At $n = 10$ the gap is 0.1. Doubling $n$ halves it. | correct | B2 |
| l2-thinner.json | screens[0].explain.text | The gap fell to 0.05 at $n = 20$, and the two sums were 0.309 and 0.359. The area $\tfrac13$ is trapped bet... | correct | B2 |
| l2-thinner.json | screens[0].explain.canvas.caption | $n = 20$: $L_{20} = 0.309$, $R_{20} = 0.359$, gap 0.05 | correct | B2 |
| l2-thinner.json | screens[1].prose | The area $A$ is trapped: $L_n \le A \le R_n$. As $n$ grows the trap closes, so both sums **converge** to $A... | correct | B2 |
| l2-thinner.json | screens[1].canvas.state.caption | Gaps: $n = 1$: 1. $n = 2$: 0.5. $n = 4$: 0.25. $n = 5$: 0.2. $n = 10$: 0.1. | correct | B2 |
| l2-thinner.json | screens[1].question | Which formula gives the gap $R_n - L_n$? | correct | B2 |
| l2-thinner.json | screens[1].widget.options[0] | graded key (choice): $\dfrac{1}{n}$ | correct | B2 |
| l2-thinner.json | screens[1].widget.options[1].text | wrong option, wrong under every convention: $\dfrac{1}{n^2}$ | correct | B2 |
| l2-thinner.json | screens[1].widget.options[1].why | At $n = 2$ that gives 0.25, but the gap is 0.5. | correct | B2 |
| l2-thinner.json | screens[1].widget.options[2].text | wrong option, wrong under every convention: $\dfrac{1}{2n}$ | correct | B2 |
| l2-thinner.json | screens[1].widget.options[2].why | At $n = 1$ that gives 0.5, but the gap is 1. | correct | B2 |
| l2-thinner.json | screens[1].widget.options[3].text | wrong option, wrong under every convention: $\dfrac{n - 1}{n}$ | correct | B2 |
| l2-thinner.json | screens[1].widget.options[3].why | That grows towards 1 as $n$ grows. The gap shrinks. | correct | B2 |
| l2-thinner.json | screens[1].hints[0].text | Multiply each gap by its $n$. | correct | B2 |
| l2-thinner.json | screens[1].hints[1].text | $1 \times 1$, $2 \times 0.5$, $4 \times 0.25$: what do you notice? | correct | B2 |
| l2-thinner.json | screens[1].hints[2].text | Every product is 1, so the gap is $\tfrac1n$. | correct | B2 |
| l2-thinner.json | screens[1].feedback.correct | Every gap times its $n$ is 1. | correct | B2 |
| l2-thinner.json | screens[1].feedback.generic | Not quite right. Test each formula at $n = 1$ and $n = 2$. | correct | B2 |
| l2-thinner.json | screens[1].explain.text | Slide each left rectangle one strip to the right: it becomes the next right rectangle. Only the tallest rig... | correct | B2 |
| l2-thinner.json | screens[2].prose | Same idea on a new interval: $f(x) = x^2$ on $[1, 3]$ with $n = 10$ rectangles, each 0.2 wide. Top: left re... | correct | B2 |
| l2-thinner.json | screens[2].question | How big is the gap $R_{10} - L_{10}$? | correct | B2 |
| l2-thinner.json | screens[2].widget.answer | graded key (numeric): 1.6 | correct | B2 |
| l2-thinner.json | screens[2].widget.wrong[0] | slip no-height = 0.2 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | screens[2].widget.wrong[1] | slip no-width = 8 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | screens[2].widget.wrong[2] | slip unit-width = 0.8 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | screens[2].widget.accept | 1.6: $(9 - 1) \times 0.2$ | correct | B2 |
| l2-thinner.json | screens[2].hints[0].text | Which two rectangles have no partner once you slide the left ones along? | correct | B2 |
| l2-thinner.json | screens[2].hints[1].text | The last right rectangle has height $f(3) = 9$; the first left one has height $f(1) = 1$. | correct | B2 |
| l2-thinner.json | screens[2].hints[2].text | Both are 0.2 wide, so the gap is $(9 - 1) \times 0.2$. | correct | B2 |
| l2-thinner.json | screens[2].feedback.correct | $(f(3) - f(1)) \times 0.2 = 1.6$. | correct | B2 |
| l2-thinner.json | screens[2].feedback.generic | Not quite right. Only the last right rectangle and the first left rectangle differ. | correct | B2 |
| l2-thinner.json | screens[2].feedback.byKey.no-height | 0.2 is the width alone. Multiply by the height difference $f(3) - f(1) = 8$. | correct | B2 |
| l2-thinner.json | screens[2].feedback.byKey.no-width | 8 is the height difference. Multiply by the width 0.2. | correct | B2 |
| l2-thinner.json | screens[2].feedback.byKey.unit-width | You divided by 10 but forgot the interval is 2 long. Each strip is 0.2 wide, not 0.1. | correct | B2 |
| l2-thinner.json | screens[2].explain.text | The last right rectangle has height 9 and the first left one height 1. Both are 0.2 wide, so the gap is $8 ... | correct | B2 |
| l2-thinner.json | screens[3].prose | Last lesson, rectangle $k$ had area $\tfrac{k^2}{n^3}$, so $R_n = \tfrac{1}{n^3}\left(1^2 + 2^2 + \dots + n... | correct | B2 |
| l2-thinner.json | screens[3].canvas.params.rows | [["1", "1"], ["2", "0.625"], ["4", "0.46875"], ["10", "0.385"]] | correct | B2 |
| l2-thinner.json | screens[3].question | Write $R_n$ as a single fraction in $n$. | correct | B2 |
| l2-thinner.json | screens[3].widget.answer | graded key (expression): "\\frac{(n+1)(2n+1)}{6n^2}" | correct | B2 |
| l2-thinner.json | screens[3].widget.wrong[0] | slip no-scale = "\\frac{n(n+1)(2n+1)}{6}" is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | screens[3].widget.wrong[1] | slip n-squared = "\\frac{(n+1)(2n+1)}{6n}" is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | screens[3].widget.wrong[2] | slip limit-early = "\\frac{1}{3}" is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | screens[3].hints[0].text | Multiply the squares formula by $\tfrac{1}{n^3}$. | correct | B2 |
| l2-thinner.json | screens[3].hints[1].text | One factor $n$ on top cancels one $n$ of the $n^3$ below. | correct | B2 |
| l2-thinner.json | screens[3].hints[2].text | $\tfrac{1}{n^3} \cdot \tfrac{n(n+1)(2n+1)}{6} = \tfrac{(n+1)(2n+1)}{6n^2}$. | correct | B2 |
| l2-thinner.json | screens[3].feedback.correct | $R_n = \dfrac{(n+1)(2n+1)}{6n^2}$. | correct | B2 |
| l2-thinner.json | screens[3].feedback.generic | Not quite right. Multiply the squares formula by $\tfrac{1}{n^3}$ and cancel one $n$. | correct | B2 |
| l2-thinner.json | screens[3].feedback.byKey.no-scale | That is the sum of the squares alone. Multiply by $\tfrac{1}{n^3}$, the width and the scale of each height. | correct | B2 |
| l2-thinner.json | screens[3].feedback.byKey.n-squared | You divided by $n^2$, not $n^3$. After cancelling one $n$, an $n^2$ stays on the bottom. | correct | B2 |
| l2-thinner.json | screens[3].feedback.byKey.limit-early | $\tfrac13$ is where $R_n$ heads as $n$ grows. The question asks for $R_n$ itself, which still depends on $n$. | correct | B2 |
| l2-thinner.json | screens[3].explain.text | $R_n = \tfrac{1}{n^3} \cdot \tfrac{n(n+1)(2n+1)}{6} = \tfrac{(n+1)(2n+1)}{6n^2}$. Check $n = 4$: $\tfrac{5 ... | correct | B2 |
| l2-thinner.json | screens[3].explain.canvas.highlight.rows | [2] | correct | B2 |
| l2-thinner.json | screens[4].prose | You found $R_n = \dfrac{(n+1)(2n+1)}{6n^2} = \dfrac13 + \dfrac{1}{2n} + \dfrac{1}{6n^2}$. The two extra ter... | correct | B2 |
| l2-thinner.json | screens[4].canvas.params.rows | [["1", "1"], ["2", "0.625"], ["4", "0.46875"], ["10", "0.385"], ["100", "?"]] | correct | B2 |
| l2-thinner.json | screens[4].canvas.state.highlight.rows | [4] | correct | B2 |
| l2-thinner.json | screens[4].question | What is $R_{100}$? Give five decimal places. | correct | B2 |
| l2-thinner.json | screens[4].widget.answer | graded key (numeric): 0.33835 | correct | B2 |
| l2-thinner.json | screens[4].widget.wrong[0] | slip limit = 0.33333 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | screens[4].widget.wrong[1] | slip left = 0.32835 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | screens[4].widget.wrong[2] | slip half-term = 0.33833 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | screens[4].widget.accept | 0.33835: $\tfrac{101 \times 201}{60000}$ | correct | B2 |
| l2-thinner.json | screens[4].hints[0].text | Put $n = 100$ into either form. | correct | B2 |
| l2-thinner.json | screens[4].hints[1].text | $\tfrac{1}{2n} = 0.005$ and $\tfrac{1}{6n^2} \approx 0.0000167$. | correct | B2 |
| l2-thinner.json | screens[4].hints[2].text | $0.33333 + 0.005 + 0.0000167 \approx 0.33835$. | correct | B2 |
| l2-thinner.json | screens[4].feedback.correct | $\tfrac{101 \times 201}{60000} = 0.33835$. | correct | B2 |
| l2-thinner.json | screens[4].feedback.generic | Not quite right. Substitute $n = 100$ into $\tfrac13 + \tfrac{1}{2n} + \tfrac{1}{6n^2}$. | correct | B2 |
| l2-thinner.json | screens[4].feedback.byKey.limit | That is the limit $\tfrac13$. At $n = 100$ the error terms still add about 0.005. | correct | B2 |
| l2-thinner.json | screens[4].feedback.byKey.left | That is $L_{100}$, the left sum. The right sum sits above the area, not below it. | correct | B2 |
| l2-thinner.json | screens[4].feedback.byKey.half-term | You dropped the $\tfrac{1}{6n^2}$ term or rounded too early. Keep it: it adds 0.0000167. | correct | B2 |
| l2-thinner.json | screens[4].explain.text | $R_{100} = \tfrac{101 \times 201}{60000} = 0.33835$. The error $\tfrac{1}{2n} + \tfrac{1}{6n^2}$ is about 0... | correct | B2 |
| l2-thinner.json | screens[5].prose | A new curve, $g(x) = 1 - x^2$ on $[0, 1]$, with 4 rectangles. Top: $L_4 = 0.78125$. Bottom: $R_4 = 0.53125$. | correct | B2 |
| l2-thinner.json | screens[5].question | Which sum is too big for the area under $g$? | correct | B2 |
| l2-thinner.json | screens[5].widget.options[0] | graded key (choice): The left sum, 0.781 | correct | B2 |
| l2-thinner.json | screens[5].widget.options[1].text | wrong option, wrong under every convention: The right sum, 0.531 | correct | B2 |
| l2-thinner.json | screens[5].widget.options[1].why | You carried over the rule from $x^2$, where the curve rises. This curve falls, so each right end is the low... | correct | B2 |
| l2-thinner.json | screens[5].widget.options[2].text | wrong option, wrong under every convention: Neither: with 4 rectangles the errors cancel | correct | B2 |
| l2-thinner.json | screens[5].widget.options[2].why | They cannot both be right: the sums differ by 0.25. The area lies strictly between them, so one is too big. | correct | B2 |
| l2-thinner.json | screens[5].widget.options[3].text | wrong option, wrong under every convention: It depends on $n$ | correct | B2 |
| l2-thinner.json | screens[5].widget.options[3].why | For a curve that only falls, the left rectangles overshoot for every $n$. Only the size of the error change... | correct | B2 |
| l2-thinner.json | screens[5].hints[0].text | Does $g$ rise or fall across $[0, 1]$? | correct | B2 |
| l2-thinner.json | screens[5].hints[1].text | Look at the left rectangles. Does each one poke above the curve? | correct | B2 |
| l2-thinner.json | screens[5].hints[2].text | $g$ falls, so each strip is highest at its left end. The left rectangles overshoot. | correct | B2 |
| l2-thinner.json | screens[5].feedback.correct | A falling curve makes the left sum the overestimate. | correct | B2 |
| l2-thinner.json | screens[5].feedback.generic | Not quite right. Check whether $g$ rises or falls, then see which rectangles poke above it. | correct | B2 |
| l2-thinner.json | screens[5].feedback.byKey.right | You carried over the rule from $x^2$, where the curve rises. Here $g$ falls, so the right ends are the lowe... | correct | B2 |
| l2-thinner.json | screens[5].explain.text | $g$ falls, so each strip is highest at its left end: the left rectangles poke above the curve. The area is ... | correct | B2 |
| l2-thinner.json | screens[6].prose | You squeezed the area between sums that converge. For a continuous $f$ on $[a, b]$, every choice of points ... | correct | B2 |
| l2-thinner.json | screens[6].question | For $f(x) = \sqrt{x}$ on $[0, 4]$ with $n = 50$, how big is that gap? | correct | B2 |
| l2-thinner.json | screens[6].widget.options[0] | graded key (choice): 0.16 | correct | B2 |
| l2-thinner.json | screens[6].widget.options[1].text | wrong option, wrong under every convention: 0.08 | correct | B2 |
| l2-thinner.json | screens[6].widget.options[1].why | That is the width $\tfrac{4}{50}$ alone. Multiply by $f(4) - f(0) = 2$. | correct | B2 |
| l2-thinner.json | screens[6].widget.options[2].text | wrong option, wrong under every convention: 0.04 | correct | B2 |
| l2-thinner.json | screens[6].widget.options[2].why | You used a width of $\tfrac{1}{50}$. The interval is 4 long, so each strip is $\tfrac{4}{50}$ wide. | correct | B2 |
| l2-thinner.json | screens[6].widget.options[3].text | wrong option, wrong under every convention: 0.32 | correct | B2 |
| l2-thinner.json | screens[6].widget.options[3].why | You used $f(4) = 4$. The height is $\sqrt{4} = 2$. | correct | B2 |
| l2-thinner.json | screens[6].hints[0].text | Find $f(4) - f(0)$ and the strip width. | correct | B2 |
| l2-thinner.json | screens[6].hints[1].text | $f(4) - f(0) = 2$ and the width is $\tfrac{4}{50} = 0.08$. Multiply. | correct | B2 |
| l2-thinner.json | screens[6].feedback.correct | $2 \times 0.08 = 0.16$. | correct | B2 |
| l2-thinner.json | screens[6].feedback.generic | Not quite right. Multiply the height difference $\sqrt4 - \sqrt0$ by the strip width $\tfrac{4}{50}$. | correct | B2 |
| l2-thinner.json | screens[6].explain.text | $\|f(4) - f(0)\| \cdot \tfrac{4}{50} = 2 \times 0.08 = 0.16$. Double $n$ and the gap halves, so it goes to ... | correct | B2 |
| l2-thinner.json | screens[7].prose | Now prove the area under $x^2$ on $[0, 1]$ is $\tfrac13$ from below. We already have $R_n = \tfrac13 + \tfr... | correct | B2 |
| l2-thinner.json | screens[7].question | Put the lines in order. | correct | B2 |
| l2-thinner.json | screens[7].widget.answer | graded key (order): ["d1", "d2", "d3", "d4", "d5"] | correct | B2 |
| l2-thinner.json | screens[7].widget.answer.order | graded order of 5 lines; each line follows from the one above | correct | B2 |
| l2-thinner.json | screens[7].widget.lines[0].text | $L_n = \sum_{k=0}^{n-1} \left(\tfrac{k}{n}\right)^2 \tfrac1n$: heights at the left ends $0, \tfrac1n, \dots... | correct | B2 |
| l2-thinner.json | screens[7].widget.lines[1].text | $= \tfrac{1}{n^3} \sum_{k=1}^{n-1} k^2$: take out $\tfrac{1}{n^3}$; the $k = 0$ term is 0 | correct | B2 |
| l2-thinner.json | screens[7].widget.lines[2].text | $= \tfrac{1}{n^3} \cdot \tfrac{(n-1)n(2n-1)}{6}$: the squares formula with $n - 1$ in place of $n$ | correct | B2 |
| l2-thinner.json | screens[7].widget.lines[3].text | $= \tfrac13 - \tfrac{1}{2n} + \tfrac{1}{6n^2}$: multiply out $(n-1)(2n-1)$ and divide by $6n^2$ | correct | B2 |
| l2-thinner.json | screens[7].widget.lines[4].text | $L_n \le A \le R_n$ and both tend to $\tfrac13$, so $A = \tfrac13$: the area is squeezed | correct | B2 |
| l2-thinner.json | screens[7].hints[0].text | Start from the definition of the left sum. | correct | B2 |
| l2-thinner.json | screens[7].hints[1].text | The squares formula needs the sum written as $1^2 + \dots + (n-1)^2$ first. | correct | B2 |
| l2-thinner.json | screens[7].hints[2].text | Define, take out the constant, use the formula, simplify, then squeeze. | correct | B2 |
| l2-thinner.json | screens[7].feedback.correct | Each line follows from the one above. | correct | B2 |
| l2-thinner.json | screens[7].feedback.generic | Not quite right. The squeeze can only come once both limits are known. | correct | B2 |
| l2-thinner.json | screens[7].feedback.byKey.d5 | The squeeze needs the limit of $L_n$ first. It is the last step. | correct | B2 |
| l2-thinner.json | screens[7].feedback.byKey.d3 | The formula applies once $\tfrac{1}{n^3}$ is out and the sum is a plain sum of squares. | correct | B2 |
| l2-thinner.json | screens[7].explain.text | The left sum gave $\tfrac13 - \tfrac{1}{2n} + \tfrac{1}{6n^2}$, a mirror of $R_n$. Both tend to $\tfrac13$ ... | correct | B2 |
| l2-thinner.json | screens[8].prose | A pension pays £1 a year, spread evenly through the year, for 10 years. At a 5% discount rate, compounded c... | correct | B2 |
| l2-thinner.json | screens[8].canvas.params.functions[0].label | $D(t) = e^{-0.05t}$ | correct | B2 |
| l2-thinner.json | screens[8].question | A pricing script brackets the value between left and right sums. How many strips make the gap at most £0.01? | correct | B2 |
| l2-thinner.json | screens[8].widget.answer | graded key (numeric): 394 | correct | B2 |
| l2-thinner.json | screens[8].widget.wrong[0] | slip round-down = 393 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | screens[8].widget.wrong[1] | slip no-length = 40 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | screens[8].widget.wrong[2] | slip no-height = 1000 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | screens[8].widget.accept | 394: the gap is $\tfrac{3.935}{n}$, and $\tfrac{3.935}{0.01} = 393.5$. | correct | B2 |
| l2-thinner.json | screens[8].hints[0].text | Use the gap formula $\|D(10) - D(0)\|\,\tfrac{10}{n}$. | correct | B2 |
| l2-thinner.json | screens[8].hints[1].text | $\|D(10) - D(0)\| \times 10 = 0.3935 \times 10 = 3.935$. | correct | B2 |
| l2-thinner.json | screens[8].hints[2].text | Solve $\tfrac{3.935}{n} \le 0.01$: $n \ge 393.5$. | correct | B2 |
| l2-thinner.json | screens[8].feedback.correct | $n \ge 393.5$, so 394 strips. | correct | B2 |
| l2-thinner.json | screens[8].feedback.generic | Not quite right. Set $\tfrac{0.3935 \times 10}{n} \le 0.01$ and solve for $n$. | correct | B2 |
| l2-thinner.json | screens[8].feedback.byKey.round-down | 393 strips give a gap of 0.01001, just over a penny. Round up. | correct | B2 |
| l2-thinner.json | screens[8].feedback.byKey.no-length | You left out the interval length 10. The width is $\tfrac{10}{n}$, not $\tfrac1n$. | correct | B2 |
| l2-thinner.json | screens[8].feedback.byKey.no-height | That ignores the height difference 0.3935. The gap is $0.3935 \times \tfrac{10}{n}$. | correct | B2 |
| l2-thinner.json | screens[8].explain.text | The gap is $(1 - 0.6065) \times \tfrac{10}{n} = \tfrac{3.935}{n}$, so $n \ge 393.5$: 394 strips. $D$ falls,... | correct | B2 |
| l2-thinner.json | summary.ideas[0] | The area is trapped between the left and right sums, and the trap closes as $n$ grows. | correct | B2 |
| l2-thinner.json | summary.ideas[1] | For a curve that only rises or only falls, the gap is $\|f(b) - f(a)\|\,\tfrac{b - a}{n}$, which tends to 0. | correct | B2 |
| l2-thinner.json | summary.ideas[2] | The exact area is the limit of the sums: for $x^2$ on $[0, 1]$, $R_n = \tfrac13 + \tfrac{1}{2n} + \tfrac{1}... | correct | B2 |
| l2-thinner.json | summary.formula.name | Area as a limit | correct | B2 |
| l2-thinner.json | summary.formula.tex | A = \lim_{n \to \infty} \sum_{k=1}^{n} f(x_k^*)\,\Delta x | correct | B2 |
| l2-thinner.json | summary.formula.note | For a continuous $f$, left, right and midpoint choices all give this same limit. | correct | B2 |
| l2-thinner.json | summary.trap | On a falling curve the left sum is the overestimate and the right sum the underestimate. | correct | B2 |
| l2-thinner.json | quiz[0].prose | Take $f(x) = 3x$ on $[0, 2]$ with $n = 6$ rectangles. | correct | B2 |
| l2-thinner.json | quiz[0].question | How big is the gap between the right and left sums? | correct | B2 |
| l2-thinner.json | quiz[0].widget.answer | graded key (numeric): 2 | correct | B2 |
| l2-thinner.json | quiz[0].widget.wrong[0] | slip no-height = 0.3333 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | quiz[0].widget.wrong[1] | slip no-width = 6 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | quiz[0].widget.wrong[2] | slip unit = 1 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | quiz[0].widget.accept | 2: $(6 - 0) \times \tfrac{2}{6}$ | correct | B2 |
| l2-thinner.json | quiz[0].feedback.correct | $(f(2) - f(0)) \times \tfrac26 = 6 \times \tfrac13 = 2$. | correct | B2 |
| l2-thinner.json | quiz[0].feedback.generic | Not quite right. Multiply $f(2) - f(0)$ by the strip width. | correct | B2 |
| l2-thinner.json | quiz[0].feedback.byKey.no-height | That is the strip width alone. Multiply by $f(2) - f(0) = 6$. | correct | B2 |
| l2-thinner.json | quiz[0].feedback.byKey.no-width | That is the height difference. Multiply by the width $\tfrac26$. | correct | B2 |
| l2-thinner.json | quiz[0].feedback.byKey.unit | You used a width of $\tfrac16$. The interval is 2 long, so each strip is $\tfrac13$ wide. | correct | B2 |
| l2-thinner.json | quiz[0].explain.text | Only the last right rectangle and the first left one differ. Their heights differ by $f(2) - f(0) = 6$, and... | correct | B2 |
| l2-thinner.json | quiz[1].prose | For $f(x) = x^2$ on $[0, 1]$, $L_n = \tfrac13 - \tfrac{1}{2n} + \tfrac{1}{6n^2}$. | correct | B2 |
| l2-thinner.json | quiz[1].question | What is $L_{10}$? | correct | B2 |
| l2-thinner.json | quiz[1].widget.answer | graded key (numeric): 0.285 | correct | B2 |
| l2-thinner.json | quiz[1].widget.wrong[0] | slip right = 0.385 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | quiz[1].widget.wrong[1] | slip limit = 0.3333 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | quiz[1].widget.wrong[2] | slip dropped = 0.2833 is the value of the named mistake and is not a correct answer | correct | B2 |
| l2-thinner.json | quiz[1].widget.accept | 0.285: $0.33333 - 0.05 + 0.00167$ | correct | B2 |
| l2-thinner.json | quiz[1].feedback.correct | $\tfrac13 - 0.05 + 0.00167 = 0.285$. | correct | B2 |
| l2-thinner.json | quiz[1].feedback.generic | Not quite right. Substitute $n = 10$ into all three terms. | correct | B2 |
| l2-thinner.json | quiz[1].feedback.byKey.right | That is $R_{10}$. The left sum subtracts $\tfrac{1}{2n}$. | correct | B2 |
| l2-thinner.json | quiz[1].feedback.byKey.limit | That is the limit. At $n = 10$ the left sum is still 0.05 short of it. | correct | B2 |
| l2-thinner.json | quiz[1].feedback.byKey.dropped | You dropped the $\tfrac{1}{6n^2}$ term. It adds 0.00167. | correct | B2 |
| l2-thinner.json | quiz[1].explain.text | $L_{10} = 0.33333 - 0.05 + 0.00167 = 0.285$. Check: $\tfrac{9 \times 19}{600} = 0.285$. It sits below $\tfr... | correct | B2 |
| l2-thinner.json | quiz[2].prose | Take $f(x) = \dfrac{1}{x}$ on $[1, 2]$, which falls as $x$ grows. | correct | B2 |
| l2-thinner.json | quiz[2].question | What is true of the right sum $R_n$, for every $n$? | correct | B2 |
| l2-thinner.json | quiz[2].widget.options[0] | graded key (choice): It is smaller than the area | correct | B2 |
| l2-thinner.json | quiz[2].widget.options[1].text | wrong option, wrong under every convention: It is bigger than the area | correct | B2 |
| l2-thinner.json | quiz[2].widget.options[1].why | That holds for a rising curve such as $x^2$. Here each right end is the lowest point of its strip. | correct | B2 |
| l2-thinner.json | quiz[2].widget.options[2].text | wrong option, wrong under every convention: It equals the area once $n$ is large | correct | B2 |
| l2-thinner.json | quiz[2].widget.options[2].why | It gets as close as we like, but for any fixed $n$ the right rectangles stay under a falling curve. | correct | B2 |
| l2-thinner.json | quiz[2].feedback.correct | Right rectangles sit under a falling curve. | correct | B2 |
| l2-thinner.json | quiz[2].feedback.generic | Not quite right. Ask where each strip of a falling curve is lowest. | correct | B2 |
| l2-thinner.json | quiz[2].explain.text | On a falling curve each strip is lowest at its right end, so every right rectangle sits under the curve. Th... | correct | B2 |
| l2-thinner.json | quiz[3].prose | For $f(x) = x$ on $[0, 1]$, the sum $1 + 2 + \dots + n = \tfrac{n(n+1)}{2}$ gives $R_n = \dfrac{n+1}{2n}$. | correct | B2 |
| l2-thinner.json | quiz[3].question | What does $R_n$ converge to as $n \to \infty$? | correct | B2 |
| l2-thinner.json | quiz[3].widget.options[0] | graded key (choice): $\tfrac12$ | correct | B2 |
| l2-thinner.json | quiz[3].widget.options[1].text | wrong option, wrong under every convention: $1$ | correct | B2 |
| l2-thinner.json | quiz[3].widget.options[1].why | That is $R_1$, the single rectangle. As $n$ grows the overshoot shrinks. | correct | B2 |
| l2-thinner.json | quiz[3].widget.options[2].text | wrong option, wrong under every convention: $0$ | correct | B2 |
| l2-thinner.json | quiz[3].widget.options[2].why | Each rectangle shrinks to nothing, but there are more of them. Their total settles on a positive number. | correct | B2 |
| l2-thinner.json | quiz[3].widget.options[3].text | wrong option, wrong under every convention: It grows without bound | correct | B2 |
| l2-thinner.json | quiz[3].widget.options[3].why | More terms do not mean a bigger total: each term shrinks as $n$ grows. | correct | B2 |
| l2-thinner.json | quiz[3].feedback.correct | $\tfrac{n+1}{2n} = \tfrac12 + \tfrac{1}{2n} \to \tfrac12$. | correct | B2 |
| l2-thinner.json | quiz[3].feedback.generic | Not quite right. Split $\tfrac{n+1}{2n}$ into $\tfrac12 + \tfrac{1}{2n}$. | correct | B2 |
| l2-thinner.json | quiz[3].explain.text | $R_n = \tfrac12 + \tfrac{1}{2n}$, and $\tfrac{1}{2n} \to 0$. So the area under $y = x$ on $[0, 1]$ is $\tfr... | correct | B2 |
| l3-signed-area.json | screens[0].prose | Part of $f(x) = x - 1$ lies below the axis on $[0, 3]$. There the rectangles hang down: their heights are n... | correct | B3 |
| l3-signed-area.json | screens[0].canvas.params.functions[0].label | $f(x) = x - 1$ | correct | B3 |
| l3-signed-area.json | screens[0].canvas.state.caption | Heights: $-0.75,\ -0.25,\ 0.25,\ 0.75,\ 1.25,\ 1.75$ | correct | B3 |
| l3-signed-area.json | screens[0].question | Add height times width over all six rectangles, keeping the signs. | correct | B3 |
| l3-signed-area.json | screens[0].widget.answer | graded key (numeric): 1.5 | correct | B3 |
| l3-signed-area.json | screens[0].widget.wrong[0] | slip no-signs = 2.5 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[0].widget.wrong[1] | slip no-width = 3 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[0].widget.wrong[2] | slip below-only = -0.5 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[0].widget.accept | 1.5: $0.5 \times (-0.75 - 0.25 + 0.25 + 0.75 + 1.25 + 1.75)$ | correct | B3 |
| l3-signed-area.json | screens[0].hints[0].text | A hanging rectangle has a negative height, so it adds a negative amount. | correct | B3 |
| l3-signed-area.json | screens[0].hints[1].text | The heights add to $-1 + 4 = 3$. | correct | B3 |
| l3-signed-area.json | screens[0].hints[2].text | Multiply the total height 3 by the width 0.5. | correct | B3 |
| l3-signed-area.json | screens[0].feedback.correct | $0.5 \times 3 = 1.5$. | correct | B3 |
| l3-signed-area.json | screens[0].feedback.generic | Not quite right. Keep the minus signs on the two hanging rectangles, then multiply by 0.5. | correct | B3 |
| l3-signed-area.json | screens[0].feedback.byKey.no-signs | You treated the hanging rectangles as positive. Their heights are $-0.75$ and $-0.25$, so they pull the tot... | correct | B3 |
| l3-signed-area.json | screens[0].feedback.byKey.no-width | You added the heights but did not multiply by the width 0.5. | correct | B3 |
| l3-signed-area.json | screens[0].feedback.byKey.below-only | That is the two hanging rectangles alone. Add the four above the axis too. | correct | B3 |
| l3-signed-area.json | screens[0].explain.text | The two hanging rectangles add $-0.5$ and the four above add $2$. So the sum is $1.5$, not the $2.5$ of sha... | correct | B3 |
| l3-signed-area.json | screens[1].prose | With thinner and thinner rectangles the sum becomes the **signed area**. Area above the axis counts positiv... | correct | B3 |
| l3-signed-area.json | screens[1].canvas.params.functions[0].label | $f(x) = x - 1$ | correct | B3 |
| l3-signed-area.json | screens[1].canvas.derive.caption | Signed area from 0 to $b$: {{fixed(b*b/2 - b, 3)}} | correct | B3 |
| l3-signed-area.json | screens[1].question | For which $b > 0$ is the signed area from 0 to $b$ exactly zero? | correct | B3 |
| l3-signed-area.json | screens[1].widget.answer | graded key (numeric): 2 | correct | B3 |
| l3-signed-area.json | screens[1].widget.wrong[0] | slip crossing = 1 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[1].widget.wrong[1] | slip end = 3 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[1].widget.accept | 2: the triangle above cancels the triangle below. | correct | B3 |
| l3-signed-area.json | screens[1].hints[0].text | Watch the caption as $b$ passes 1. | correct | B3 |
| l3-signed-area.json | screens[1].hints[1].text | Below the axis there is a triangle of area 0.5. How far right must $b$ go to add 0.5 above? | correct | B3 |
| l3-signed-area.json | screens[1].hints[2].text | At $b = 2$ the triangle above also has area 0.5. | correct | B3 |
| l3-signed-area.json | screens[1].feedback.correct | At $b = 2$ the two triangles cancel. | correct | B3 |
| l3-signed-area.json | screens[1].feedback.generic | Not quite right. Slide until the caption reads 0.000. | correct | B3 |
| l3-signed-area.json | screens[1].feedback.byKey.crossing | At $b = 1$ the curve crosses the axis, but the signed area is $-0.5$. Only the part below has been added. | correct | B3 |
| l3-signed-area.json | screens[1].feedback.byKey.end | At $b = 3$ the signed area is 1.5. The zero comes earlier. | correct | B3 |
| l3-signed-area.json | screens[1].explain.text | At $b = 2$ the triangle above, area 0.5, cancels the triangle below, area 0.5. One square unit is shaded, y... | correct | B3 |
| l3-signed-area.json | screens[2].prose | We write the signed area from $a$ to $b$ as $$\int_a^b f(x)\,dx$$ This is the **definite integral** of $f$ ... | correct | B3 |
| l3-signed-area.json | screens[2].canvas.state.vlines[0].label | $a = 0$ | correct | B3 |
| l3-signed-area.json | screens[2].canvas.state.vlines[1].label | $b = 8$ | correct | B3 |
| l3-signed-area.json | screens[2].question | Tap every region that counts as negative in $\int_0^8 f(x)\,dx$. | correct | B3 |
| l3-signed-area.json | screens[2].widget.answer | graded key (tap-regions): ["C", "E"] | correct | B3 |
| l3-signed-area.json | screens[2].widget.wrong[0] | slip with-a = ["A", "C", "E"] is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[2].hints[0].text | Two things matter: is the region below the axis, and is it between the limits? | correct | B3 |
| l3-signed-area.json | screens[2].hints[1].text | One region below the axis lies left of $a = 0$. | correct | B3 |
| l3-signed-area.json | screens[2].hints[2].text | C and E are below the axis and inside $[0, 8]$. A is outside. | correct | B3 |
| l3-signed-area.json | screens[2].feedback.correct | C and E: below the axis and inside $[0, 8]$. | correct | B3 |
| l3-signed-area.json | screens[2].feedback.generic | Not quite right. Pick the regions below the axis that lie between 0 and 8. | correct | B3 |
| l3-signed-area.json | screens[2].feedback.byKey.with-a | A is below the axis, but it lies left of 0, outside the limits. It is not part of this integral. | correct | B3 |
| l3-signed-area.json | screens[2].feedback.byKey.A | A is below the axis, but it lies left of 0, outside the limits. | correct | B3 |
| l3-signed-area.json | screens[2].feedback.byKey.B | B lies above the axis, so it counts positive. | correct | B3 |
| l3-signed-area.json | screens[2].feedback.byKey.D | D lies above the axis, so it counts positive. | correct | B3 |
| l3-signed-area.json | screens[2].explain.text | C and E count negative; B and D count positive; A lies outside $[0, 8]$. The four humps inside are the same... | correct | B3 |
| l3-signed-area.json | screens[3].prose | Straight-line pieces make triangles, so we can find integrals by geometry. Take $g(x) = 2 - x$ on $[0, 5]$. | correct | B3 |
| l3-signed-area.json | screens[3].canvas.params.functions[0].label | $g(x) = 2 - x$ | correct | B3 |
| l3-signed-area.json | screens[3].question | Find $\int_0^5 (2 - x)\,dx$. | correct | B3 |
| l3-signed-area.json | screens[3].widget.answer | graded key (numeric): -2.5 | correct | B3 |
| l3-signed-area.json | screens[3].widget.wrong[0] | slip area = 6.5 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[3].widget.wrong[1] | slip flipped = 2.5 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[3].widget.wrong[2] | slip above = 2 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[3].widget.wrong[3] | slip below = -4.5 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[3].widget.accept | $-2.5$: $2 - 4.5$ | correct | B3 |
| l3-signed-area.json | screens[3].hints[0].text | Find the area of each triangle, then give the lower one a minus sign. | correct | B3 |
| l3-signed-area.json | screens[3].hints[1].text | The upper triangle has base 2 and height 2. The lower one has base 3 and height 3. | correct | B3 |
| l3-signed-area.json | screens[3].hints[2].text | $2 - 4.5 = -2.5$. | correct | B3 |
| l3-signed-area.json | screens[3].feedback.correct | $2 - 4.5 = -2.5$. | correct | B3 |
| l3-signed-area.json | screens[3].feedback.generic | Not quite right. Upper triangle minus lower triangle. | correct | B3 |
| l3-signed-area.json | screens[3].feedback.byKey.area | 6.5 is the total shaded area. The integral subtracts the part below the axis. | correct | B3 |
| l3-signed-area.json | screens[3].feedback.byKey.flipped | You subtracted the wrong way round. The bigger triangle is below, so the integral is negative. | correct | B3 |
| l3-signed-area.json | screens[3].feedback.byKey.above | That is the upper triangle alone. The lower triangle counts too, as a negative. | correct | B3 |
| l3-signed-area.json | screens[3].feedback.byKey.below | That is the lower triangle alone. Add the upper triangle's 2. | correct | B3 |
| l3-signed-area.json | screens[3].explain.text | Above: $\tfrac12 \times 2 \times 2 = 2$. Below: $\tfrac12 \times 3 \times 3 = 4.5$, counted as $-4.5$. So $... | correct | B3 |
| l3-signed-area.json | screens[3].explain.canvas.caption | Signed: $2 - 4.5 = -2.5$. Area: $2 + 4.5 = 6.5$. | correct | B3 |
| l3-signed-area.json | screens[4].prose | You found $\int_0^3 (x - 1)\,dx = 1.5$. Now run the sum backwards, from 3 down to 0. Each width becomes $\D... | correct | B3 |
| l3-signed-area.json | screens[4].canvas.params.functions[0].label | $f(x) = x - 1$ | correct | B3 |
| l3-signed-area.json | screens[4].canvas.state.segments[0].label | from 3 back to 0 | correct | B3 |
| l3-signed-area.json | screens[4].question | What is $\int_3^0 (x - 1)\,dx$? | correct | B3 |
| l3-signed-area.json | screens[4].widget.answer | graded key (numeric): -1.5 | correct | B3 |
| l3-signed-area.json | screens[4].widget.wrong[0] | slip same = 1.5 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[4].widget.wrong[1] | slip zero = 0 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[4].widget.wrong[2] | slip area = -2.5 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[4].widget.accept | $-1.5$: reversing the limits flips the sign. | correct | B3 |
| l3-signed-area.json | screens[4].hints[0].text | What does a negative width do to each height times width? | correct | B3 |
| l3-signed-area.json | screens[4].hints[1].text | Every term $f(x_k)\,\Delta x$ flips sign. | correct | B3 |
| l3-signed-area.json | screens[4].hints[2].text | So the whole sum flips: $-1.5$. | correct | B3 |
| l3-signed-area.json | screens[4].feedback.correct | Reversing the limits flips the sign. | correct | B3 |
| l3-signed-area.json | screens[4].feedback.generic | Not quite right. Every width is negative now, so every term changes sign. | correct | B3 |
| l3-signed-area.json | screens[4].feedback.byKey.same | You treated the order of the limits as unimportant. Running backwards makes every width negative, so the si... | correct | B3 |
| l3-signed-area.json | screens[4].feedback.byKey.zero | The region has not changed, so it does not vanish. Only the direction changed, which flips the sign. | correct | B3 |
| l3-signed-area.json | screens[4].feedback.byKey.area | That uses the shaded area 2.5. Start from the signed area 1.5 and flip it. | correct | B3 |
| l3-signed-area.json | screens[4].explain.text | Every width is negative, so every term flips: $\int_3^0 = -\int_0^3 = -1.5$. With equal limits the width is... | correct | B3 |
| l3-signed-area.json | screens[4].explain.canvas.caption | $\int_3^0 (x - 1)\,dx = -1.5$ | correct | B3 |
| l3-signed-area.json | screens[5].prose | A midpoint sum with $n = 1000$ gives $\int_0^{\pi} \sin x\,dx = 2.000$. The hump is symmetric about $x = \t... | correct | B3 |
| l3-signed-area.json | screens[5].canvas.state.vlines[0].label | $\tfrac{\pi}{2}$ | correct | B3 |
| l3-signed-area.json | screens[5].question | What is $\int_0^{\pi/2} \sin x\,dx$? | correct | B3 |
| l3-signed-area.json | screens[5].widget.answer | graded key (numeric): 1 | correct | B3 |
| l3-signed-area.json | screens[5].widget.wrong[0] | slip whole = 2 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[5].widget.wrong[1] | slip box = 1.5708 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[5].widget.accept | 1: half of 2, by symmetry. | correct | B3 |
| l3-signed-area.json | screens[5].hints[0].text | Split the hump at $\tfrac{\pi}{2}$. | correct | B3 |
| l3-signed-area.json | screens[5].hints[1].text | The two halves are mirror images, so they have equal integrals. | correct | B3 |
| l3-signed-area.json | screens[5].hints[2].text | $\int_0^{\pi/2} + \int_{\pi/2}^{\pi} = 2$ with equal parts, so each is 1. | correct | B3 |
| l3-signed-area.json | screens[5].feedback.correct | Two equal halves of 2. | correct | B3 |
| l3-signed-area.json | screens[5].feedback.generic | Not quite right. Split $\int_0^{\pi}$ at $\tfrac{\pi}{2}$ into two equal parts. | correct | B3 |
| l3-signed-area.json | screens[5].feedback.byKey.whole | 2 is the whole hump, from 0 to $\pi$. You want the left half. | correct | B3 |
| l3-signed-area.json | screens[5].feedback.byKey.box | That is $\tfrac{\pi}{2} \times 1$, the box around the half hump. The curve stays below height 1, so the are... | correct | B3 |
| l3-signed-area.json | screens[5].explain.text | Splitting at $\tfrac{\pi}{2}$ gives $\int_0^{\pi} = \int_0^{\pi/2} + \int_{\pi/2}^{\pi}$. The halves are mi... | correct | B3 |
| l3-signed-area.json | screens[6].prose | On $[\pi, 2\pi]$ the sine curve is the same hump flipped below the axis. Recall $\int_0^{\pi} \sin x\,dx = 2$. | correct | B3 |
| l3-signed-area.json | screens[6].canvas.state.vlines[1].label | $2\pi$ | correct | B3 |
| l3-signed-area.json | screens[6].question | What is the total area of the two shaded regions? | correct | B3 |
| l3-signed-area.json | screens[6].widget.answer | graded key (numeric): 4 | correct | B3 |
| l3-signed-area.json | screens[6].widget.wrong[0] | slip signed = 0 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[6].widget.wrong[1] | slip one = 2 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[6].widget.wrong[2] | slip negative = -4 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[6].widget.accept | 4: two humps of area 2. | correct | B3 |
| l3-signed-area.json | screens[6].hints[0].text | Area is a size. Can a size be negative? | correct | B3 |
| l3-signed-area.json | screens[6].hints[1].text | Each hump has area 2. | correct | B3 |
| l3-signed-area.json | screens[6].hints[2].text | Add the two sizes: $2 + 2$. | correct | B3 |
| l3-signed-area.json | screens[6].feedback.correct | Area counts both humps as positive: 4. | correct | B3 |
| l3-signed-area.json | screens[6].feedback.generic | Not quite right. Find the size of each shaded region and add them. | correct | B3 |
| l3-signed-area.json | screens[6].feedback.byKey.signed | 0 is the integral $\int_0^{2\pi} \sin x\,dx$, where the lower hump cancels the upper one. The question asks... | correct | B3 |
| l3-signed-area.json | screens[6].feedback.byKey.one | That is one hump. The lower region has area 2 as well. | correct | B3 |
| l3-signed-area.json | screens[6].feedback.byKey.negative | Area is never negative. Both regions add their size, 2 each. | correct | B3 |
| l3-signed-area.json | screens[6].explain.text | Area counts both humps as positive: $2 + 2 = 4$. The integral $\int_0^{2\pi} \sin x\,dx$ is 0, because the ... | correct | B3 |
| l3-signed-area.json | screens[6].explain.canvas.caption | Area: $2 + 2 = 4$. Integral: $2 - 2 = 0$. | correct | B3 |
| l3-signed-area.json | screens[7].prose | You used three rules. For any $a$, $b$, $c$: $$\int_a^a f\,dx = 0, \qquad \int_b^a f\,dx = -\int_a^b f\,dx$... | correct | B3 |
| l3-signed-area.json | screens[7].question | Given $\int_0^2 f(x)\,dx = 3$ and $\int_0^5 f(x)\,dx = 1$, find $\int_2^5 f(x)\,dx$. | correct | B3 |
| l3-signed-area.json | screens[7].widget.options[0] | graded key (choice): $-2$ | correct | B3 |
| l3-signed-area.json | screens[7].widget.options[1].text | wrong option, wrong under every convention: $4$ | correct | B3 |
| l3-signed-area.json | screens[7].widget.options[1].why | You added the two integrals. Split $[0, 5]$ at 2 instead: $1 = 3 + \int_2^5 f\,dx$. | correct | B3 |
| l3-signed-area.json | screens[7].widget.options[2].text | wrong option, wrong under every convention: $2$ | correct | B3 |
| l3-signed-area.json | screens[7].widget.options[2].why | You subtracted the wrong way round: $3 - 1$. Solve $1 = 3 + \int_2^5 f\,dx$. | correct | B3 |
| l3-signed-area.json | screens[7].widget.options[3].text | wrong option, wrong under every convention: $1$ | correct | B3 |
| l3-signed-area.json | screens[7].widget.options[3].why | That is the integral over the whole of $[0, 5]$. | correct | B3 |
| l3-signed-area.json | screens[7].hints[0].text | Split $\int_0^5$ at 2. | correct | B3 |
| l3-signed-area.json | screens[7].hints[1].text | $\int_0^5 = \int_0^2 + \int_2^5$, so $1 = 3 + \int_2^5 f\,dx$. | correct | B3 |
| l3-signed-area.json | screens[7].feedback.correct | $1 = 3 + \int_2^5 f\,dx$, so it is $-2$. | correct | B3 |
| l3-signed-area.json | screens[7].feedback.generic | Not quite right. Write $\int_0^5$ as $\int_0^2 + \int_2^5$ and solve. | correct | B3 |
| l3-signed-area.json | screens[7].explain.text | Splitting at 2: $\int_0^5 = \int_0^2 + \int_2^5$, so $1 = 3 + \int_2^5 f\,dx$ and the answer is $-2$. A neg... | correct | B3 |
| l3-signed-area.json | screens[8].prose | Prove that $\int_0^{2\pi} \sin x\,dx = 0$, using $\int_0^{\pi} \sin x\,dx = 2$ and $\sin(x + \pi) = -\sin x$. | correct | B3 |
| l3-signed-area.json | screens[8].question | Put the lines in order. | correct | B3 |
| l3-signed-area.json | screens[8].widget.answer | graded key (order): ["e1", "e2", "e3", "e4"] | correct | B3 |
| l3-signed-area.json | screens[8].widget.answer.order | graded order of 4 lines; each line follows from the one above | correct | B3 |
| l3-signed-area.json | screens[8].widget.lines[0].text | $\int_0^{2\pi} \sin x\,dx = \int_0^{\pi} \sin x\,dx + \int_{\pi}^{2\pi} \sin x\,dx$: split at $\pi$ | correct | B3 |
| l3-signed-area.json | screens[8].widget.lines[1].text | $= \int_0^{\pi} \sin x\,dx + \int_0^{\pi} \sin(x + \pi)\,dx$: slide the second piece left by $\pi$; its rec... | correct | B3 |
| l3-signed-area.json | screens[8].widget.lines[2].text | $= \int_0^{\pi} \sin x\,dx + \int_0^{\pi} (-\sin x)\,dx$: because $\sin(x + \pi) = -\sin x$ | correct | B3 |
| l3-signed-area.json | screens[8].widget.lines[3].text | $= 2 - 2 = 0$: flipping every height flips every rectangle, so the second piece is $-2$ | correct | B3 |
| l3-signed-area.json | screens[8].hints[0].text | Start by splitting the interval. | correct | B3 |
| l3-signed-area.json | screens[8].hints[1].text | Before using $\sin(x + \pi) = -\sin x$, the second piece has to be written over $[0, \pi]$. | correct | B3 |
| l3-signed-area.json | screens[8].hints[2].text | Split, slide, flip, add. | correct | B3 |
| l3-signed-area.json | screens[8].feedback.correct | Each line follows from the one above. | correct | B3 |
| l3-signed-area.json | screens[8].feedback.generic | Not quite right. The identity can only be used once the second piece runs over $[0, \pi]$. | correct | B3 |
| l3-signed-area.json | screens[8].feedback.byKey.e3 | The identity needs $\sin(x + \pi)$ to appear first. Slide the piece before you flip it. | correct | B3 |
| l3-signed-area.json | screens[8].feedback.byKey.e4 | The numbers come last, once both pieces are written over $[0, \pi]$. | correct | B3 |
| l3-signed-area.json | screens[8].explain.text | Sliding the second piece left by $\pi$ keeps every rectangle's height, and $\sin(x + \pi) = -\sin x$ flips ... | correct | B3 |
| l3-signed-area.json | screens[9].prose | A dealer buys at a rate of $q(t) = 400 - 100t$ shares per minute for 6 minutes. A negative rate means the d... | correct | B3 |
| l3-signed-area.json | screens[9].question | By how many shares does the dealer's inventory change over the 6 minutes? | correct | B3 |
| l3-signed-area.json | screens[9].widget.answer | graded key (numeric): 600 | correct | B3 |
| l3-signed-area.json | screens[9].widget.wrong[0] | slip traded = 1000 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[9].widget.wrong[1] | slip stop = 800 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[9].widget.wrong[2] | slip rate = -200 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | screens[9].widget.accept | 600 shares: $800 - 200$. | correct | B3 |
| l3-signed-area.json | screens[9].hints[0].text | Buying adds to inventory and selling takes it away. | correct | B3 |
| l3-signed-area.json | screens[9].hints[1].text | Buying from 0 to 4 is a triangle of $\tfrac12 \times 4 \times 400$. Selling from 4 to 6 is $\tfrac12 \times... | correct | B3 |
| l3-signed-area.json | screens[9].hints[2].text | $800 - 200 = 600$. | correct | B3 |
| l3-signed-area.json | screens[9].feedback.correct | $800 - 200 = 600$ shares. | correct | B3 |
| l3-signed-area.json | screens[9].feedback.generic | Not quite right. Find the signed area: buying counts positive, selling negative. | correct | B3 |
| l3-signed-area.json | screens[9].feedback.byKey.traded | 1000 is the total area: every share the dealer traded. Inventory nets the 200 sold against the 800 bought. | correct | B3 |
| l3-signed-area.json | screens[9].feedback.byKey.stop | 800 is the buying alone. From minute 4 the dealer sells 200 shares back. | correct | B3 |
| l3-signed-area.json | screens[9].feedback.byKey.rate | That is the rate at minute 6, in shares per minute. The change in inventory is the signed area. | correct | B3 |
| l3-signed-area.json | screens[9].explain.text | Buying from 0 to 4 adds $\tfrac12 \times 4 \times 400 = 800$ shares; selling from 4 to 6 removes $\tfrac12 ... | correct | B3 |
| l3-signed-area.json | screens[9].explain.canvas.area[0].label | +800 | correct | B3 |
| l3-signed-area.json | screens[9].explain.canvas.area[1].label | −200 | correct | B3 |
| l3-signed-area.json | summary.ideas[0] | $\int_a^b f(x)\,dx$ is the signed area: regions below the axis count negative. | correct | B3 |
| l3-signed-area.json | summary.ideas[1] | Reversing the limits flips the sign, equal limits give 0, and integrals over touching intervals add. | correct | B3 |
| l3-signed-area.json | summary.ideas[2] | Area counts every region as positive. It equals the integral only when $f \ge 0$. | correct | B3 |
| l3-signed-area.json | summary.formula.name | Splitting an integral | correct | B3 |
| l3-signed-area.json | summary.formula.tex | \int_a^c f(x)\,dx = \int_a^b f(x)\,dx + \int_b^c f(x)\,dx | correct | B3 |
| l3-signed-area.json | summary.formula.note | Also $\int_b^a f\,dx = -\int_a^b f\,dx$ and $\int_a^a f\,dx = 0$. | correct | B3 |
| l3-signed-area.json | summary.trap | $\int_0^{2\pi} \sin x\,dx = 0$, but the area between $\sin x$ and the axis is 4. Check which one is asked. | correct | B3 |
| l3-signed-area.json | quiz[0].prose | Think of the graph of $y = x$ between $x = -2$ and $x = 2$. | correct | B3 |
| l3-signed-area.json | quiz[0].question | What is $\int_{-2}^{2} x\,dx$? | correct | B3 |
| l3-signed-area.json | quiz[0].widget.answer | graded key (numeric): 0 | correct | B3 |
| l3-signed-area.json | quiz[0].widget.wrong[0] | slip area = 4 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | quiz[0].widget.wrong[1] | slip half = 2 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | quiz[0].widget.wrong[2] | slip neg = -2 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | quiz[0].widget.accept | 0: the two triangles cancel. | correct | B3 |
| l3-signed-area.json | quiz[0].feedback.correct | The triangles $-2$ and $+2$ cancel. | correct | B3 |
| l3-signed-area.json | quiz[0].feedback.generic | Not quite right. Find each triangle's signed area and add. | correct | B3 |
| l3-signed-area.json | quiz[0].feedback.byKey.area | 4 is the total area of the two triangles. The one left of 0 is below the axis, so it counts $-2$. | correct | B3 |
| l3-signed-area.json | quiz[0].feedback.byKey.half | That is the triangle on $[0, 2]$ alone. The one on $[-2, 0]$ counts $-2$. | correct | B3 |
| l3-signed-area.json | quiz[0].feedback.byKey.neg | That is the triangle on $[-2, 0]$ alone. Add the $+2$ on $[0, 2]$. | correct | B3 |
| l3-signed-area.json | quiz[0].explain.text | On $[-2, 0]$ the line is below the axis: a triangle of area 2, counted as $-2$. On $[0, 2]$ it is $+2$. The... | correct | B3 |
| l3-signed-area.json | quiz[1].prose | You are told $\int_1^4 f(x)\,dx = 7$. | correct | B3 |
| l3-signed-area.json | quiz[1].question | What is $\int_4^1 f(x)\,dx$? | correct | B3 |
| l3-signed-area.json | quiz[1].widget.options[0] | graded key (choice): $-7$ | correct | B3 |
| l3-signed-area.json | quiz[1].widget.options[1].text | wrong option, wrong under every convention: $7$ | correct | B3 |
| l3-signed-area.json | quiz[1].widget.options[1].why | You treated the order of the limits as unimportant. Running from 4 down to 1 makes every width negative. | correct | B3 |
| l3-signed-area.json | quiz[1].widget.options[2].text | wrong option, wrong under every convention: $0$ | correct | B3 |
| l3-signed-area.json | quiz[1].widget.options[2].why | The interval is the same length; only its direction changed. That flips the sign, it does not erase the value. | correct | B3 |
| l3-signed-area.json | quiz[1].widget.options[3].text | wrong option, wrong under every convention: $\tfrac17$ | correct | B3 |
| l3-signed-area.json | quiz[1].widget.options[3].why | Reversing the limits flips the sign of each term. It does not turn the value upside down. | correct | B3 |
| l3-signed-area.json | quiz[1].feedback.correct | Reversing the limits flips the sign. | correct | B3 |
| l3-signed-area.json | quiz[1].feedback.generic | Not quite right. Think about the sign of each width when the sum runs backwards. | correct | B3 |
| l3-signed-area.json | quiz[1].explain.text | Running from 4 down to 1 makes every $\Delta x$ negative, so every term flips sign. $\int_4^1 f\,dx = -\int... | correct | B3 |
| l3-signed-area.json | quiz[2].prose | Take $f(x) = x^2 + 5$. | correct | B3 |
| l3-signed-area.json | quiz[2].question | What is $\int_3^3 (x^2 + 5)\,dx$? | correct | B3 |
| l3-signed-area.json | quiz[2].widget.options[0] | graded key (choice): $0$ | correct | B3 |
| l3-signed-area.json | quiz[2].widget.options[1].text | wrong option, wrong under every convention: $14$ | correct | B3 |
| l3-signed-area.json | quiz[2].widget.options[1].why | 14 is the height $f(3)$. From 3 to 3 there is no width, so there is no area. | correct | B3 |
| l3-signed-area.json | quiz[2].widget.options[2].text | wrong option, wrong under every convention: It is undefined | correct | B3 |
| l3-signed-area.json | quiz[2].widget.options[2].why | It is defined: every rectangle has width $\tfrac{3 - 3}{n} = 0$, so the sum is 0 for every $n$. | correct | B3 |
| l3-signed-area.json | quiz[2].feedback.correct | No width, no area. | correct | B3 |
| l3-signed-area.json | quiz[2].feedback.generic | Not quite right. Work out the width of the interval from 3 to 3. | correct | B3 |
| l3-signed-area.json | quiz[2].explain.text | Every rectangle has width $\tfrac{3 - 3}{n} = 0$, so every Riemann sum is 0 and so is the integral. This ho... | correct | B3 |
| l3-signed-area.json | quiz[3].prose | Take $f(x) = x - 1$ on $[0, 3]$. Its integral is 1.5. | correct | B3 |
| l3-signed-area.json | quiz[3].question | What is the total area between the graph and the $x$-axis on $[0, 3]$? | correct | B3 |
| l3-signed-area.json | quiz[3].widget.answer | graded key (numeric): 2.5 | correct | B3 |
| l3-signed-area.json | quiz[3].widget.wrong[0] | slip signed = 1.5 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | quiz[3].widget.wrong[1] | slip above = 2 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | quiz[3].widget.wrong[2] | slip diff = -1.5 is the value of the named mistake and is not a correct answer | correct | B3 |
| l3-signed-area.json | quiz[3].widget.accept | 2.5: $0.5 + 2$. | correct | B3 |
| l3-signed-area.json | quiz[3].feedback.correct | $0.5 + 2 = 2.5$. | correct | B3 |
| l3-signed-area.json | quiz[3].feedback.generic | Not quite right. Find each triangle's size and add the sizes. | correct | B3 |
| l3-signed-area.json | quiz[3].feedback.byKey.signed | 1.5 is the integral, which subtracts the triangle below the axis. Area adds it. | correct | B3 |
| l3-signed-area.json | quiz[3].feedback.byKey.above | That is the triangle above the axis. The one below adds 0.5 more. | correct | B3 |
| l3-signed-area.json | quiz[3].feedback.byKey.diff | Area is never negative. Add the two triangles' sizes. | correct | B3 |
| l3-signed-area.json | quiz[3].explain.text | Below the axis on $[0, 1]$: a triangle of area 0.5. Above on $[1, 3]$: area 2. The area is $0.5 + 2 = 2.5$;... | correct | B3 |
| l4-accumulating-a-rate.json | screens[0].prose | Cash flows into a fund at a steady rate through each day, but the rate changes from day to day. Each bar sh... | correct | B4 |
| l4-accumulating-a-rate.json | screens[0].question | How much cash came in over the five days, in £ thousand? | correct | B4 |
| l4-accumulating-a-rate.json | screens[0].widget.answer | graded key (numeric): 500 | correct | B4 |
| l4-accumulating-a-rate.json | screens[0].widget.wrong[0] | slip average = 100 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[0].widget.wrong[1] | slip peak = 150 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[0].widget.wrong[2] | slip one-day = 120 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[0].widget.accept | 500, that is £500k: $120 + 80 + 150 + 60 + 90$. | correct | B4 |
| l4-accumulating-a-rate.json | screens[0].hints[0].text | How much cash arrives on Monday alone? | correct | B4 |
| l4-accumulating-a-rate.json | screens[0].hints[1].text | Monday's rate is £120k per day, for one day: £120k. | correct | B4 |
| l4-accumulating-a-rate.json | screens[0].hints[2].text | Do the same for each day and add. | correct | B4 |
| l4-accumulating-a-rate.json | screens[0].feedback.correct | £500k came in over the week. | correct | B4 |
| l4-accumulating-a-rate.json | screens[0].feedback.generic | Not quite right. Each day adds its rate times one day. Add the five days. | correct | B4 |
| l4-accumulating-a-rate.json | screens[0].feedback.byKey.average | You averaged the rates: £100k per day is the typical day. The week's total is five days of that. | correct | B4 |
| l4-accumulating-a-rate.json | screens[0].feedback.byKey.peak | That is Wednesday, the busiest day. Add every day's cash. | correct | B4 |
| l4-accumulating-a-rate.json | screens[0].feedback.byKey.one-day | That is Monday alone. Add every day's cash. | correct | B4 |
| l4-accumulating-a-rate.json | screens[0].explain.text | Each bar is one day wide, so its area, rate times 1 day, is that day's cash. The week's total, £500k, is th... | correct | B4 |
| l4-accumulating-a-rate.json | screens[0].explain.canvas.caption | Total area of the bars: 500, so £500k | correct | B4 |
| l4-accumulating-a-rate.json | screens[1].prose | A new fund's inflows ramp up: $t$ days after launch the rate is $r(t) = 20t$ £ thousand per day. The shaded... | correct | B4 |
| l4-accumulating-a-rate.json | screens[1].canvas.params.functions[0].label | $r(t) = 20t$ | correct | B4 |
| l4-accumulating-a-rate.json | screens[1].canvas.derive.caption | Cash in by day {{fixed(T, 2)}}: £{{fixed(10*T*T, 1)}}k of £360k | correct | B4 |
| l4-accumulating-a-rate.json | screens[1].question | When has half of the £360k arrived? Give $T$ to two decimal places. | correct | B4 |
| l4-accumulating-a-rate.json | screens[1].widget.answer | graded key (numeric): 4.24 | correct | B4 |
| l4-accumulating-a-rate.json | screens[1].widget.wrong[0] | slip half-time = 3 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[1].widget.wrong[1] | slip end = 6 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[1].widget.accept | Any value from 4.18 to 4.30. Exactly $\sqrt{18} \approx 4.243$ days. | correct | B4 |
| l4-accumulating-a-rate.json | screens[1].hints[0].text | Half of £360k is £180k. Watch the caption. | correct | B4 |
| l4-accumulating-a-rate.json | screens[1].hints[1].text | At day 4 the caption shows £160k. Go a little further. | correct | B4 |
| l4-accumulating-a-rate.json | screens[1].hints[2].text | The caption passes £180k between day 4.20 and day 4.25. | correct | B4 |
| l4-accumulating-a-rate.json | screens[1].feedback.correct | Half has arrived at about day 4.24. | correct | B4 |
| l4-accumulating-a-rate.json | screens[1].feedback.generic | Not quite right. Slide until the caption reads about £180k. | correct | B4 |
| l4-accumulating-a-rate.json | screens[1].feedback.byKey.half-time | At day 3, halfway in time, only £90k has arrived: a quarter. The rate is low early on. | correct | B4 |
| l4-accumulating-a-rate.json | screens[1].feedback.byKey.end | By day 6 all £360k has arrived. Half arrives earlier. | correct | B4 |
| l4-accumulating-a-rate.json | screens[1].explain.text | Half, £180k, has arrived when the triangle's area $\tfrac12 \cdot T \cdot 20T = 10T^2$ reaches 180: $T = \s... | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].prose | The cash in by day $T$ is the area under the rate from 0 to $T$, written $$A(T) = \int_0^T r(t)\,dt$$ This ... | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].canvas.params.functions[0].label | $r(t) = 20t$ | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].canvas.state.vlines[0].label | $T = 5$ | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].question | What is $A(5)$, in £ thousand? | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].widget.answer | graded key (numeric): 250 | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].widget.wrong[0] | slip rate = 100 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].widget.wrong[1] | slip box = 500 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].widget.wrong[2] | slip half-rate = 50 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].widget.accept | 250, that is £250k: $\tfrac12 \times 5 \times 100$. | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].hints[0].text | The shaded region is a triangle. | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].hints[1].text | Its base is 5 days and its height is $r(5) = 100$. | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].hints[2].text | $\tfrac12 \times 5 \times 100 = 250$. | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].feedback.correct | $\tfrac12 \times 5 \times 100 = 250$, so £250k. | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].feedback.generic | Not quite right. Find the area of the shaded triangle. | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].feedback.byKey.rate | 100 is the rate at day 5, in £k per day. The amount is the area under the rate. | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].feedback.byKey.box | $100 \times 5$ assumes the rate was £100k a day all along. It started at 0, so the region is a triangle. | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].feedback.byKey.half-rate | That is half the final rate. Multiply by the 5 days as well. | correct | B4 |
| l4-accumulating-a-rate.json | screens[2].explain.text | The region is a triangle with base 5 and height 100, so $A(5) = 250$: £250k. The rate at day 5 is only one ... | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].prose | A van pulls away, speeding up steadily to 20 metres per second over 10 seconds, then holds that speed. Spee... | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].question | How far does the van travel in the first 30 seconds? | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].widget.answer | graded key (numeric): 500 | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].widget.wrong[0] | slip top-speed = 600 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].widget.wrong[1] | slip triangle = 300 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].widget.wrong[2] | slip cruise = 400 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].widget.accept | 500 m: $100 + 400$. | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].hints[0].text | Split the region at $t = 10$. | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].hints[1].text | A triangle from 0 to 10, then a rectangle from 10 to 30. | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].hints[2].text | $\tfrac12 \times 10 \times 20 + 20 \times 20$. | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].feedback.correct | $100 + 400 = 500$ metres. | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].feedback.generic | Not quite right. Add the triangle up to 10 seconds and the rectangle after it. | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].feedback.byKey.top-speed | $20 \times 30$ assumes top speed from the start. In the first 10 seconds the van was slower. | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].feedback.byKey.triangle | That treats the whole region as one triangle. After 10 seconds the speed stays at 20. | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].feedback.byKey.cruise | That is the steady part alone. Add the 100 m covered while speeding up. | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].explain.text | Speeding up: a triangle of $\tfrac12 \times 10 \times 20 = 100$ m. Cruising: a rectangle of $20 \times 20 =... | correct | B4 |
| l4-accumulating-a-rate.json | screens[3].explain.canvas.caption | Triangle 100 m + rectangle 400 m = 500 m | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].prose | A trading position earns at a rate of $p(t) = 400 - 200t$ pounds per hour. After two hours the rate turns n... | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].canvas.state.vlines[0].label | $t = 3$ | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].question | What is the position's P&L after 3 hours? | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].widget.answer | graded key (numeric): 300 | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].widget.wrong[0] | slip stop = 400 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].widget.wrong[1] | slip area = 500 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].widget.wrong[2] | slip rate = -200 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].widget.accept | £300: $400 - 100$. | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].hints[0].text | Gains add; losses subtract. | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].hints[1].text | The gain from 0 to 2 is a triangle of $\tfrac12 \times 2 \times 400$. The loss from 2 to 3 is $\tfrac12 \ti... | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].hints[2].text | $400 - 100 = 300$. | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].feedback.correct | £400 gained, £100 given back: £300. | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].feedback.generic | Not quite right. Find the signed area from 0 to 3. | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].feedback.byKey.stop | £400 is the P&L at hour 2. From then on the rate is negative and P&L drains away. | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].feedback.byKey.area | That adds the loss as if it were a gain. The region below the axis counts negative. | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].feedback.byKey.rate | That is the rate at hour 3, in £ per hour. The P&L is the signed area up to hour 3. | correct | B4 |
| l4-accumulating-a-rate.json | screens[4].explain.text | The gain to hour 2 is $\tfrac12 \times 2 \times 400 = \text{£}400$. The loss from hour 2 to 3 is $\tfrac12 ... | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].prose | The same position over 4 hours, with P&L rate $p(t) = 400 - 200t$ pounds per hour. | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].question | When during the 4 hours is the running P&L highest? | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].widget.options[0].text | wrong option, wrong under every convention: At $t = 0$, where the rate is highest | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].widget.options[0].why | You read the rate as the P&L. At $t = 0$ the rate is highest, but nothing has been earned yet: the P&L is 0. | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].widget.options[1] | graded key (choice): At $t = 2$, where the rate is zero | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].widget.options[2].text | wrong option, wrong under every convention: At $t = 4$, after the longest time | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].widget.options[2].why | From hour 2 the rate is negative, so the P&L falls. By hour 4 it is back to 0. | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].widget.options[3].text | wrong option, wrong under every convention: At $t = 1$, halfway to the crossing | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].widget.options[3].why | At hour 1 the rate is still positive, so the P&L is still rising. | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].hints[0].text | While the rate is positive, is the P&L rising or falling? | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].hints[1].text | The rate is positive before hour 2 and negative after it. | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].hints[2].text | The P&L stops rising exactly where the rate stops being positive. | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].feedback.correct | The P&L peaks where the rate crosses zero. | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].feedback.generic | Not quite right. The P&L rises while the rate is positive and falls while it is negative. | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].feedback.byKey.start | You read the rate as the P&L. A high rate means the P&L is rising fast, not that it is large. At $t = 0$ it... | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].explain.text | The P&L rises while the rate is positive and falls once it turns negative. So it peaks at hour 2, at £400, ... | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].explain.canvas.area[0].label | +£400 | correct | B4 |
| l4-accumulating-a-rate.json | screens[5].explain.canvas.area[1].label | −£400 | correct | B4 |
| l4-accumulating-a-rate.json | screens[6].prose | Every time, the total change was the signed area under the rate: $$\text{change from } a \text{ to } b = \i... | correct | B4 |
| l4-accumulating-a-rate.json | screens[6].question | When is the running total $A$ climbing fastest? | correct | B4 |
| l4-accumulating-a-rate.json | screens[6].widget.options[0] | graded key (choice): When the rate $r(T)$ is largest | correct | B4 |
| l4-accumulating-a-rate.json | screens[6].widget.options[1].text | wrong option, wrong under every convention: When the total $A(T)$ is largest | correct | B4 |
| l4-accumulating-a-rate.json | screens[6].widget.options[1].why | The largest total comes where the rate is zero, as with the P&L. There $A$ is flat, not climbing. | correct | B4 |
| l4-accumulating-a-rate.json | screens[6].widget.options[2].text | wrong option, wrong under every convention: When the rate $r(T)$ is zero | correct | B4 |
| l4-accumulating-a-rate.json | screens[6].widget.options[2].why | There $A$ stops climbing: it is at a peak or a dip. | imprecise | Finding 7: r(T) = 0 without a sign change (r = (T-1)^2) gives neither peak nor dip |
| l4-accumulating-a-rate.json | screens[6].widget.options[3].text | wrong option, wrong under every convention: Never: a total grows at a constant speed | correct | B4 |
| l4-accumulating-a-rate.json | screens[6].widget.options[3].why | Only a constant rate gives constant growth. The fund's cash came in faster and faster as $r$ grew. | correct | B4 |
| l4-accumulating-a-rate.json | screens[6].hints[0].text | Think of the fund: when did the cash pile up fastest? | correct | B4 |
| l4-accumulating-a-rate.json | screens[6].hints[1].text | Each day adds about $r(T)$ times one day, so the biggest rate adds the most. | correct | B4 |
| l4-accumulating-a-rate.json | screens[6].feedback.correct | The bigger the rate, the faster the total climbs. | correct | B4 |
| l4-accumulating-a-rate.json | screens[6].feedback.generic | Not quite right. Ask how much $A$ grows over one short step $\Delta t$. | correct | B4 |
| l4-accumulating-a-rate.json | screens[6].explain.text | Over a short step $\Delta t$, the total grows by about $r(T)\,\Delta t$. So it climbs fastest where the rat... | correct | B4 |
| l4-accumulating-a-rate.json | screens[7].prose | Why is the total change exactly $\int_a^b r(t)\,dt$, when the rate keeps changing? Build the argument. | correct | B4 |
| l4-accumulating-a-rate.json | screens[7].question | Put the lines in order. | correct | B4 |
| l4-accumulating-a-rate.json | screens[7].widget.answer | graded key (order): ["f1", "f2", "f3", "f4"] | correct | B4 |
| l4-accumulating-a-rate.json | screens[7].widget.answer.order | graded order of 4 lines; each line follows from the one above | correct | B4 |
| l4-accumulating-a-rate.json | screens[7].widget.lines[0].text | Cut $[a, b]$ into $n$ pieces of length $\Delta t = \tfrac{b - a}{n}$; the total change sums the pieces' cha... | correct | B4 |
| l4-accumulating-a-rate.json | screens[7].widget.lines[1].text | Each piece's rate lies between its lowest and highest values, so its change lies between those rates times ... | correct | B4 |
| l4-accumulating-a-rate.json | screens[7].widget.lines[2].text | Adding over the pieces, the total change lies between a lower and an upper Riemann sum of $r$ | correct | B4 |
| l4-accumulating-a-rate.json | screens[7].widget.lines[3].text | Both sums tend to $\int_a^b r(t)\,dt$ as $n \to \infty$, so the total change is squeezed to equal it | correct | B4 |
| l4-accumulating-a-rate.json | screens[7].hints[0].text | Start by cutting the time into pieces. | correct | B4 |
| l4-accumulating-a-rate.json | screens[7].hints[1].text | Bound each piece before adding the pieces up. | correct | B4 |
| l4-accumulating-a-rate.json | screens[7].hints[2].text | Cut, bound each piece, add the bounds, then let $n$ grow. | correct | B4 |
| l4-accumulating-a-rate.json | screens[7].feedback.correct | Each line builds on the one above. | correct | B4 |
| l4-accumulating-a-rate.json | screens[7].feedback.generic | Not quite right. The limit can only come once the change is trapped between two sums. | correct | B4 |
| l4-accumulating-a-rate.json | screens[7].feedback.byKey.f4 | Letting $n$ grow comes last, once the change sits between two sums. | correct | B4 |
| l4-accumulating-a-rate.json | screens[7].feedback.byKey.f3 | The pieces must be bounded one at a time before their bounds are added. | correct | B4 |
| l4-accumulating-a-rate.json | screens[7].explain.text | Each piece's change is trapped between its lowest and highest rate times $\Delta t$. Added up, the total ch... | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].prose | A £10m floating-rate note pays interest at a rate reset with the market. Its coupon rate is 4% a year for 3... | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].canvas.params.functions[0].label | 4% a year | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].canvas.params.functions[1].label | 4.5% a year | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].question | How much interest has accrued after the 90 days? | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].widget.answer | graded key (numeric): 106849.32 | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].widget.wrong[0] | slip average = 104794.52 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].widget.wrong[1] | slip first-rate = 98630.14 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].widget.wrong[2] | slip second-rate = 110958.9 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].widget.accept | £106,849.32, give or take £1. | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].hints[0].text | Each piece of the rate is a rectangle: rate times days. | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].hints[1].text | $30 \times 1{,}095.89$ and $60 \times 1{,}232.88$. | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].hints[2].text | £32,876.71 plus £73,972.60. | imprecise | Finding 8: 60 x 1,232.88 = 73,972.80, not 73,972.60; the figures come from the unrounded daily rates |
| l4-accumulating-a-rate.json | screens[8].feedback.correct | £32,876.71 plus £73,972.60: about £106,849. | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].feedback.generic | Not quite right. Find each rectangle's area, rate times days, and add. | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].feedback.byKey.average | You averaged 4% and 4.5% as if each ran 45 days. The higher rate ran twice as long. | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].feedback.byKey.first-rate | That keeps 4% for all 90 days. The rate reset to 4.5% after day 30. | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].feedback.byKey.second-rate | That uses 4.5% for all 90 days. The first 30 days accrued at 4%. | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].explain.text | The two rectangles hold $10{,}000{,}000 \times 0.04 \times \tfrac{30}{365} = \text{£}32{,}876.71$ and $10{,... | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].explain.canvas.area[0].label | £32,877 | correct | B4 |
| l4-accumulating-a-rate.json | screens[8].explain.canvas.area[1].label | £73,973 | correct | B4 |
| l4-accumulating-a-rate.json | summary.ideas[0] | A rate times a time is an amount, so the area under a rate is the total it builds up. | correct | B4 |
| l4-accumulating-a-rate.json | summary.ideas[1] | Parts of the rate below the axis take away: the net change is the signed area. | correct | B4 |
| l4-accumulating-a-rate.json | summary.ideas[2] | The running total climbs fastest where the rate is largest and peaks where the rate crosses zero. | imprecise | Finding 7: a crossing from below gives a low, as in review-1 items[8]; l5 summary states the direction |
| l4-accumulating-a-rate.json | summary.formula.name | Total change from a rate | correct | B4 |
| l4-accumulating-a-rate.json | summary.formula.tex | A(b) - A(a) = \int_a^b r(t)\,dt | correct | B4 |
| l4-accumulating-a-rate.json | summary.formula.note | Distance from speed, P&L from a P&L rate, volume from a volume rate, accrued interest from a coupon rate. | correct | B4 |
| l4-accumulating-a-rate.json | summary.trap | A large rate is not a large total. The P&L peaks where its rate is zero, not where the rate is highest. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[0].prose | Shares trade at 2,000 a minute for the first 15 minutes after the open. Then they trade at 500 a minute for... | correct | B4 |
| l4-accumulating-a-rate.json | quiz[0].question | How many shares trade in those 45 minutes? | correct | B4 |
| l4-accumulating-a-rate.json | quiz[0].widget.answer | graded key (numeric): 45000 | correct | B4 |
| l4-accumulating-a-rate.json | quiz[0].widget.wrong[0] | slip rates = 2500 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | quiz[0].widget.wrong[1] | slip average = 56250 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | quiz[0].widget.wrong[2] | slip first = 30000 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | quiz[0].widget.accept | 45,000: $30{,}000 + 15{,}000$. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[0].feedback.correct | $30{,}000 + 15{,}000 = 45{,}000$ shares. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[0].feedback.generic | Not quite right. Multiply each rate by its own number of minutes, then add. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[0].feedback.byKey.rates | You added the two rates. Each rate runs for its own number of minutes. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[0].feedback.byKey.average | You averaged the rates over all 45 minutes. The slow rate ran twice as long. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[0].feedback.byKey.first | That is the first 15 minutes. Add the 15,000 traded afterwards. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[0].explain.text | $2{,}000 \times 15 = 30{,}000$ and $500 \times 30 = 15{,}000$. Total volume is the area under the volume ra... | correct | B4 |
| l4-accumulating-a-rate.json | quiz[1].prose | A car starts from rest with speed $v(t) = 3t$ metres per second. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[1].question | How far does it travel in the first 4 seconds? | correct | B4 |
| l4-accumulating-a-rate.json | quiz[1].widget.answer | graded key (numeric): 24 | correct | B4 |
| l4-accumulating-a-rate.json | quiz[1].widget.wrong[0] | slip final = 12 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | quiz[1].widget.wrong[1] | slip box = 48 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | quiz[1].widget.accept | 24 m: $\tfrac12 \times 4 \times 12$. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[1].feedback.correct | A triangle: $\tfrac12 \times 4 \times 12 = 24$ m. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[1].feedback.generic | Not quite right. Find the area under the speed from 0 to 4. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[1].feedback.byKey.final | 12 is the speed at 4 seconds, in metres per second. Distance is the area under the speed. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[1].feedback.byKey.box | $12 \times 4$ assumes top speed from the start. The car started at rest, so the region is a triangle. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[1].explain.text | Speed rises from 0 to 12 over 4 seconds, so the area is a triangle: $\tfrac12 \times 4 \times 12 = 24$ m. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[2].prose | A strategy loses at a steady £50 an hour for 6 hours, then gains £80 an hour for 2 hours. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[2].question | What is its P&L over the 8 hours? | correct | B4 |
| l4-accumulating-a-rate.json | quiz[2].widget.answer | graded key (numeric): -140 | correct | B4 |
| l4-accumulating-a-rate.json | quiz[2].widget.wrong[0] | slip area = 460 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | quiz[2].widget.wrong[1] | slip rates = 30 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | quiz[2].widget.wrong[2] | slip gain = 160 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | quiz[2].widget.wrong[3] | slip sign = 140 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | quiz[2].widget.accept | −£140: $-300 + 160$. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[2].feedback.correct | $-300 + 160 = -140$ pounds. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[2].feedback.generic | Not quite right. Losses count negative: find the signed area. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[2].feedback.byKey.area | That adds the losses as gains. The £300 lost counts against the £160 gained. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[2].feedback.byKey.rates | You added the two rates. Multiply each by its hours first. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[2].feedback.byKey.gain | That is the gain alone. The first 6 hours lost £300. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[2].feedback.byKey.sign | The loss of £300 is bigger than the gain of £160, so the signed area is below zero. A positive 140 books th... | correct | B4 |
| l4-accumulating-a-rate.json | quiz[2].explain.text | The loss is a rectangle below the axis, $-50 \times 6 = -300$. The gain is $80 \times 2 = 160$. The signed ... | correct | B4 |
| l4-accumulating-a-rate.json | quiz[3].prose | A £1,000,000 bond pays a fixed coupon of 6% a year. Interest accrues daily on an actual/365 basis. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[3].question | How much interest accrues over 73 days? | correct | B4 |
| l4-accumulating-a-rate.json | quiz[3].widget.answer | graded key (numeric): 12000 | correct | B4 |
| l4-accumulating-a-rate.json | quiz[3].widget.wrong[0] | slip year = 60000 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | quiz[3].widget.wrong[1] | slip days = 4380000 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | quiz[3].widget.wrong[2] | slip daily = 164.38 is the value of the named mistake and is not a correct answer | correct | B4 |
| l4-accumulating-a-rate.json | quiz[3].widget.accept | £12,000: $1{,}000{,}000 \times 0.06 \times \tfrac{73}{365}$. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[3].feedback.correct | £164.38 a day for 73 days: £12,000. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[3].feedback.generic | Not quite right. The accrual rate is £60,000 a year; multiply by the fraction of a year. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[3].feedback.byKey.year | That is a full year's coupon. Only 73 of 365 days have passed. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[3].feedback.byKey.days | You multiplied by 73 days without dividing the annual rate by 365. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[3].feedback.byKey.daily | That is one day's interest. Multiply by the 73 days. | correct | B4 |
| l4-accumulating-a-rate.json | quiz[3].explain.text | The accrual rate is $\tfrac{60{,}000}{365} \approx \text{£}164.38$ a day, constant. Over 73 days the rectan... | correct | B4 |
| review-1.json | items[0].prose | Take $f(x) = x^3$ on $[0, 2]$ with 4 rectangles. | correct | B5 |
| review-1.json | items[0].question | What is the left sum $L_4$? | correct | B5 |
| review-1.json | items[0].widget.answer | graded key (numeric): 2.25 | correct | B5 |
| review-1.json | items[0].widget.wrong[0] | slip right = 6.25 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[0].widget.wrong[1] | slip no-width = 4.5 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[0].widget.wrong[2] | slip exact = 4 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[0].widget.accept | 2.25: $0.5 \times (0 + 0.125 + 1 + 3.375)$ | correct | B5 |
| review-1.json | items[0].feedback.correct | $0.5 \times 4.5 = 2.25$. | correct | B5 |
| review-1.json | items[0].feedback.generic | Not quite right. The width is 0.5 and the left ends are 0, 0.5, 1 and 1.5. | correct | B5 |
| review-1.json | items[0].feedback.byKey.right | You used the right ends 0.5 to 2. The left sum starts at 0 and stops at 1.5. | correct | B5 |
| review-1.json | items[0].feedback.byKey.no-width | You added the heights but did not multiply by the width 0.5. | correct | B5 |
| review-1.json | items[0].feedback.byKey.exact | 4 is the exact area. The left sum falls short of it, because $x^3$ rises. | correct | B5 |
| review-1.json | items[0].explain.text | $\Delta x = 0.5$; the left ends 0, 0.5, 1, 1.5 give heights 0, 0.125, 1, 3.375. So $L_4 = 0.5 \times 4.5 = ... | correct | B5 |
| review-1.json | items[1].prose | Think of the graph of $y = x$ from $x = -1$ to $x = 2$. | correct | B5 |
| review-1.json | items[1].question | What is $\int_{-1}^{2} x\,dx$? | correct | B5 |
| review-1.json | items[1].widget.answer | graded key (numeric): 1.5 | correct | B5 |
| review-1.json | items[1].widget.wrong[0] | slip area = 2.5 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[1].widget.wrong[1] | slip right-part = 2 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[1].widget.wrong[2] | slip left-part = -0.5 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[1].widget.accept | 1.5: $-0.5 + 2$. | correct | B5 |
| review-1.json | items[1].feedback.correct | $-0.5 + 2 = 1.5$. | correct | B5 |
| review-1.json | items[1].feedback.generic | Not quite right. Find each triangle's signed area and add. | correct | B5 |
| review-1.json | items[1].feedback.byKey.area | 2.5 is the total area. The triangle on $[-1, 0]$ is below the axis, so it counts $-0.5$. | correct | B5 |
| review-1.json | items[1].feedback.byKey.right-part | That is the triangle on $[0, 2]$. The small one on $[-1, 0]$ counts $-0.5$. | correct | B5 |
| review-1.json | items[1].feedback.byKey.left-part | That is the triangle on $[-1, 0]$. Add the $+2$ on $[0, 2]$. | correct | B5 |
| review-1.json | items[1].explain.text | On $[-1, 0]$ the line is below the axis: a triangle of area 0.5, counted as $-0.5$. On $[0, 2]$ it is a tri... | correct | B5 |
| review-1.json | items[2].prose | Take $f(x) = x^3$ on $[0, 2]$ with $n = 40$ rectangles. | correct | B5 |
| review-1.json | items[2].question | How big is the gap between the right and left sums? | correct | B5 |
| review-1.json | items[2].widget.answer | graded key (numeric): 0.4 | correct | B5 |
| review-1.json | items[2].widget.wrong[0] | slip no-height = 0.05 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[2].widget.wrong[1] | slip no-width = 8 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[2].widget.wrong[2] | slip unit = 0.2 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[2].widget.accept | 0.4: $(8 - 0) \times \tfrac{2}{40}$ | correct | B5 |
| review-1.json | items[2].feedback.correct | $8 \times 0.05 = 0.4$. | correct | B5 |
| review-1.json | items[2].feedback.generic | Not quite right. Multiply $f(2) - f(0)$ by the strip width. | correct | B5 |
| review-1.json | items[2].feedback.byKey.no-height | 0.05 is the width alone. Multiply by $f(2) - f(0) = 8$. | correct | B5 |
| review-1.json | items[2].feedback.byKey.no-width | 8 is the height difference. Multiply by the width $\tfrac{2}{40}$. | correct | B5 |
| review-1.json | items[2].feedback.byKey.unit | You used a width of $\tfrac{1}{40}$. The interval is 2 long, so each strip is $\tfrac{2}{40}$ wide. | correct | B5 |
| review-1.json | items[2].explain.text | Only the last right rectangle and the first left one differ: heights 8 and 0, width 0.05. So the gap is 0.4... | correct | B5 |
| review-1.json | items[3].prose | A stock trades 1,200 shares a minute for the first 30 minutes, then 400 a minute for the next hour. | correct | B5 |
| review-1.json | items[3].question | How many shares trade in those 90 minutes? | correct | B5 |
| review-1.json | items[3].widget.answer | graded key (numeric): 60000 | correct | B5 |
| review-1.json | items[3].widget.wrong[0] | slip rates = 1600 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[3].widget.wrong[1] | slip average = 72000 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[3].widget.wrong[2] | slip first = 36000 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[3].widget.accept | 60,000: $36{,}000 + 24{,}000$. | correct | B5 |
| review-1.json | items[3].feedback.correct | $36{,}000 + 24{,}000 = 60{,}000$ shares. | correct | B5 |
| review-1.json | items[3].feedback.generic | Not quite right. Multiply each rate by its own minutes, then add. | correct | B5 |
| review-1.json | items[3].feedback.byKey.rates | You added the two rates. Each rate runs for its own number of minutes. | correct | B5 |
| review-1.json | items[3].feedback.byKey.average | You averaged the rates over 90 minutes. The slower rate ran twice as long. | correct | B5 |
| review-1.json | items[3].feedback.byKey.first | That is the first 30 minutes. Add the 24,000 traded in the next hour. | correct | B5 |
| review-1.json | items[3].explain.text | $1{,}200 \times 30 = 36{,}000$ and $400 \times 60 = 24{,}000$. The total volume is the area under the volum... | correct | B5 |
| review-1.json | items[4].prose | Recall $\int_0^{\pi} \sin x\,dx = 2$, and that $\sin x$ repeats every $2\pi$. | correct | B5 |
| review-1.json | items[4].question | What is $\int_0^{3\pi} \sin x\,dx$? | correct | B5 |
| review-1.json | items[4].widget.answer | graded key (numeric): 2 | correct | B5 |
| review-1.json | items[4].widget.wrong[0] | slip area = 6 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[4].widget.wrong[1] | slip cancel = 0 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[4].widget.wrong[2] | slip neg = -2 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[4].widget.accept | 2: $2 - 2 + 2$. | correct | B5 |
| review-1.json | items[4].feedback.correct | $2 - 2 + 2 = 2$. | correct | B5 |
| review-1.json | items[4].feedback.generic | Not quite right. Split at $\pi$ and $2\pi$ and give each hump its sign. | correct | B5 |
| review-1.json | items[4].feedback.byKey.area | 6 is the total area of three humps. The middle one is below the axis and counts $-2$. | correct | B5 |
| review-1.json | items[4].feedback.byKey.cancel | Whole periods cancel, but $[0, 3\pi]$ is one and a half periods. The extra hump is above the axis. | correct | B5 |
| review-1.json | items[4].feedback.byKey.neg | The extra hump on $[2\pi, 3\pi]$ is above the axis, so it adds $+2$. | correct | B5 |
| review-1.json | items[4].explain.text | Split at $\pi$ and $2\pi$: the humps give $+2$, $-2$, $+2$. The first two cancel, so $\int_0^{3\pi} \sin x\... | correct | B5 |
| review-1.json | items[5].prose | For $f(x) = x$ on $[0, 1]$ with $n$ strips, the left ends are $0, \tfrac1n, \dots, \tfrac{n-1}{n}$. Use $0 ... | correct | B5 |
| review-1.json | items[5].question | Write the left sum $L_n$ as a fraction in $n$. | correct | B5 |
| review-1.json | items[5].widget.answer | graded key (expression): "\\frac{n-1}{2n}" | correct | B5 |
| review-1.json | items[5].widget.wrong[0] | slip right = "\\frac{n+1}{2n}" is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[5].widget.wrong[1] | slip no-scale = "\\frac{(n-1)n}{2}" is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[5].widget.wrong[2] | slip limit = "\\frac{1}{2}" is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[5].feedback.correct | $L_n = \tfrac{1}{n^2} \cdot \tfrac{(n-1)n}{2} = \tfrac{n-1}{2n}$. | correct | B5 |
| review-1.json | items[5].feedback.generic | Not quite right. Each term is $\tfrac{k}{n} \cdot \tfrac1n$; take out $\tfrac{1}{n^2}$ and use the formula. | correct | B5 |
| review-1.json | items[5].feedback.byKey.right | That is the right sum $R_n$. The left ends stop at $\tfrac{n-1}{n}$. | correct | B5 |
| review-1.json | items[5].feedback.byKey.no-scale | That is the plain sum of $k$. Multiply by $\tfrac{1}{n^2}$: one $\tfrac1n$ for the height, one for the width. | correct | B5 |
| review-1.json | items[5].feedback.byKey.limit | $\tfrac12$ is the limit. $L_n$ itself still depends on $n$. | correct | B5 |
| review-1.json | items[5].explain.text | $L_n = \sum_{k=0}^{n-1} \tfrac{k}{n} \cdot \tfrac1n = \tfrac{1}{n^2} \cdot \tfrac{(n-1)n}{2} = \tfrac{n-1}{... | correct | B5 |
| review-1.json | items[6].prose | A dealer buys at a rate of $q(t) = 300 - 100t$ shares a minute for 5 minutes. A negative rate means selling. | correct | B5 |
| review-1.json | items[6].question | By how many shares does the dealer's inventory change? | correct | B5 |
| review-1.json | items[6].widget.answer | graded key (numeric): 250 | correct | B5 |
| review-1.json | items[6].widget.wrong[0] | slip traded = 650 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[6].widget.wrong[1] | slip stop = 450 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[6].widget.wrong[2] | slip rate = -200 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[6].widget.accept | 250 shares: $450 - 200$. | correct | B5 |
| review-1.json | items[6].feedback.correct | $450 - 200 = 250$ shares. | correct | B5 |
| review-1.json | items[6].feedback.generic | Not quite right. Find the signed area: buying counts positive, selling negative. | correct | B5 |
| review-1.json | items[6].feedback.byKey.traded | 650 is every share traded: the total area. Inventory nets the 200 sold against the 450 bought. | correct | B5 |
| review-1.json | items[6].feedback.byKey.stop | 450 is the buying alone, up to minute 3. After that the dealer sells 200 back. | correct | B5 |
| review-1.json | items[6].feedback.byKey.rate | That is the rate at minute 5, in shares per minute. The change is the signed area. | correct | B5 |
| review-1.json | items[6].explain.text | Buying from 0 to 3 is a triangle of $\tfrac12 \times 3 \times 300 = 450$. Selling from 3 to 5 is $\tfrac12 ... | correct | B5 |
| review-1.json | items[7].prose | Take $f(x) = \sqrt{x}$ on $[0, 4]$ with 2 rectangles. | correct | B5 |
| review-1.json | items[7].question | What is the midpoint sum $M_2$? Give two decimal places. | correct | B5 |
| review-1.json | items[7].widget.answer | graded key (numeric): 5.46 | correct | B5 |
| review-1.json | items[7].widget.wrong[0] | slip left = 2.83 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[7].widget.wrong[1] | slip right = 6.83 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[7].widget.wrong[2] | slip no-root = 8 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[7].widget.accept | 5.46: $2(\sqrt1 + \sqrt3)$ | correct | B5 |
| review-1.json | items[7].feedback.correct | $2(1 + 1.732) = 5.46$. | correct | B5 |
| review-1.json | items[7].feedback.generic | Not quite right. The strips are $[0, 2]$ and $[2, 4]$, with midpoints 1 and 3. | correct | B5 |
| review-1.json | items[7].feedback.byKey.left | You used the left ends 0 and 2. The midpoints are 1 and 3. | correct | B5 |
| review-1.json | items[7].feedback.byKey.right | You used the right ends 2 and 4. The midpoints are 1 and 3. | correct | B5 |
| review-1.json | items[7].feedback.byKey.no-root | You used the midpoints as heights. The heights are $\sqrt1$ and $\sqrt3$. | correct | B5 |
| review-1.json | items[7].explain.text | Each strip is 2 wide, with midpoints 1 and 3. $M_2 = 2(\sqrt1 + \sqrt3) = 5.46$. The true area is $\tfrac{1... | correct | B5 |
| review-1.json | items[8].prose | A strategy's P&L rate is $p(t) = -300 + 100t$ pounds per hour over a 6-hour session. It starts losing and l... | correct | B5 |
| review-1.json | items[8].question | What is the lowest the running P&L goes during the session? | correct | B5 |
| review-1.json | items[8].widget.answer | graded key (numeric): -450 | correct | B5 |
| review-1.json | items[8].widget.wrong[0] | slip rate = -300 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[8].widget.wrong[1] | slip end = 0 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[8].widget.wrong[2] | slip double = -900 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[8].widget.wrong[3] | slip sign = 450 is the value of the named mistake and is not a correct answer | correct | B5 |
| review-1.json | items[8].widget.accept | −£450, at hour 3. | correct | B5 |
| review-1.json | items[8].feedback.correct | At hour 3 the P&L reaches $-\text{£}450$. | correct | B5 |
| review-1.json | items[8].feedback.generic | Not quite right. The P&L falls while the rate is negative. Find where it stops falling. | correct | B5 |
| review-1.json | items[8].feedback.byKey.rate | −300 is the rate at the start, in pounds per hour. At that moment the P&L is still 0. | correct | B5 |
| review-1.json | items[8].feedback.byKey.end | 0 is the P&L at the end: the gain after hour 3 wins back the loss. The low comes earlier. | correct | B5 |
| review-1.json | items[8].feedback.byKey.double | You took the triangle as base times height. A triangle's area is half that: $\tfrac12 \times 3 \times 300$. | correct | B5 |
| review-1.json | items[8].feedback.byKey.sign | The triangle lies below the axis, so its signed area is −½ × 3 × 300 = −450. A positive 450 books the lowes... | correct | B5 |
| review-1.json | items[8].explain.text | The rate is negative until $t = 3$, so the P&L falls until then and rises after. The low is the area of the... | correct | B5 |
| homework-1.json | items[0].prose | Take $f(x) = \dfrac{1}{x}$ on $[1, 3]$ with 4 rectangles. Give three decimal places. | correct | B6 |
| homework-1.json | items[0].question | What is the right sum $R_4$? | correct | B6 |
| homework-1.json | items[0].widget.answer | graded key (numeric): 0.95 | correct | B6 |
| homework-1.json | items[0].widget.wrong[0] | slip left = 1.2833 is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[0].widget.wrong[1] | slip no-width = 1.9 is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[0].widget.wrong[2] | slip exact = 1.0986 is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[0].widget.accept | 0.950: $0.5 \times (\tfrac23 + \tfrac12 + \tfrac25 + \tfrac13)$ | correct | B6 |
| homework-1.json | items[0].feedback.correct | $0.5 \times 1.9 = 0.950$. | correct | B6 |
| homework-1.json | items[0].feedback.generic | Not quite right. The width is 0.5 and the right ends are 1.5, 2, 2.5 and 3. | correct | B6 |
| homework-1.json | items[0].feedback.byKey.left | You used the left ends 1 to 2.5. The right sum uses 1.5 to 3. | correct | B6 |
| homework-1.json | items[0].feedback.byKey.no-width | You added the heights but did not multiply by the width 0.5. | correct | B6 |
| homework-1.json | items[0].feedback.byKey.exact | 1.099 is the exact area. The right sum falls short of it, because $\tfrac1x$ falls. | correct | B6 |
| homework-1.json | items[0].explain.text | Heights at 1.5, 2, 2.5 and 3 are $0.667, 0.5, 0.4, 0.333$, adding to 1.9. So $R_4 = 0.950$. The curve falls... | correct | B6 |
| homework-1.json | items[1].prose | Show that the area under $f(x) = x^3$ on $[0, 1]$ is $\tfrac14$, using right sums and $1^3 + 2^3 + \dots + ... | correct | B6 |
| homework-1.json | items[1].question | Put the lines in order. | correct | B6 |
| homework-1.json | items[1].widget.answer | graded key (order): ["g1", "g2", "g3", "g4", "g5"] | correct | B6 |
| homework-1.json | items[1].widget.answer.order | graded order of 5 lines; each line follows from the one above | correct | B6 |
| homework-1.json | items[1].widget.lines[0].text | $R_n = \sum_{k=1}^{n} \left(\tfrac{k}{n}\right)^3 \tfrac1n$: heights at the right ends $\tfrac{k}{n}$, widt... | correct | B6 |
| homework-1.json | items[1].widget.lines[1].text | $= \tfrac{1}{n^4} \sum_{k=1}^{n} k^3$: the factor $\tfrac{1}{n^4}$ is the same in every term | correct | B6 |
| homework-1.json | items[1].widget.lines[2].text | $= \tfrac{1}{n^4} \cdot \tfrac{n^2(n+1)^2}{4}$: the sum of the first $n$ cubes | correct | B6 |
| homework-1.json | items[1].widget.lines[3].text | $= \tfrac14\left(1 + \tfrac1n\right)^2$: cancel $n^2$, then write $\tfrac{n+1}{n}$ as $1 + \tfrac1n$ | correct | B6 |
| homework-1.json | items[1].widget.lines[4].text | $\to \tfrac14$ as $n \to \infty$, since $\tfrac1n \to 0$ | correct | B6 |
| homework-1.json | items[1].feedback.correct | Define, take out the constant, sum, simplify, take the limit. | correct | B6 |
| homework-1.json | items[1].feedback.generic | Not quite right. The cubes formula only applies once $\tfrac{1}{n^4}$ is out of the sum. | correct | B6 |
| homework-1.json | items[1].feedback.byKey.g5 | The limit is the last step, once $R_n$ is simplified. | correct | B6 |
| homework-1.json | items[1].feedback.byKey.g3 | Take the constant $\tfrac{1}{n^4}$ out before using the formula. | correct | B6 |
| homework-1.json | items[1].explain.text | Each rectangle is $\tfrac{k^3}{n^4}$, so $R_n = \tfrac{1}{n^4} \cdot \tfrac{n^2(n+1)^2}{4} = \tfrac14\left(... | correct | B6 |
| homework-1.json | items[2].prose | Take $f(x) = x^2$ on $[0, 2]$ with $n$ strips. Then $\Delta x = \tfrac2n$ and the right ends are $x_k = \tf... | correct | B6 |
| homework-1.json | items[2].question | Write the right sum $R_n$ as a fraction in $n$. | correct | B6 |
| homework-1.json | items[2].widget.answer | graded key (expression): "\\frac{4(n+1)(2n+1)}{3n^2}" | correct | B6 |
| homework-1.json | items[2].widget.wrong[0] | slip unit = "\\frac{(n+1)(2n+1)}{6n^2}" is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[2].widget.wrong[1] | slip heights = "\\frac{(n+1)(2n+1)}{3n^2}" is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[2].widget.wrong[2] | slip limit = "\\frac{8}{3}" is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[2].feedback.correct | $R_n = \tfrac{8}{n^3} \cdot \tfrac{n(n+1)(2n+1)}{6} = \tfrac{4(n+1)(2n+1)}{3n^2}$. | correct | B6 |
| homework-1.json | items[2].feedback.generic | Not quite right. Each rectangle is $\left(\tfrac{2k}{n}\right)^2 \cdot \tfrac2n = \tfrac{8k^2}{n^3}$. | correct | B6 |
| homework-1.json | items[2].feedback.byKey.unit | That is the right sum on $[0, 1]$. On $[0, 2]$ the heights are $\left(\tfrac{2k}{n}\right)^2$ and the width... | correct | B6 |
| homework-1.json | items[2].feedback.byKey.heights | You doubled the width but not the points. The height is $\left(\tfrac{2k}{n}\right)^2 = \tfrac{4k^2}{n^2}$. | correct | B6 |
| homework-1.json | items[2].feedback.byKey.limit | $\tfrac83$ is the limit. $R_n$ itself still depends on $n$. | correct | B6 |
| homework-1.json | items[2].explain.text | Each term is $\tfrac{4k^2}{n^2} \cdot \tfrac2n = \tfrac{8k^2}{n^3}$, so $R_n = \tfrac{8}{n^3} \cdot \tfrac{... | correct | B6 |
| homework-1.json | items[3].prose | Take $f(x) = \|x\| - 1$ on $[-3, 2]$. The graph is a V with its point at $(0, -1)$. | correct | B6 |
| homework-1.json | items[3].canvas.params.functions[0].label | $\|x\| - 1$ | correct | B6 |
| homework-1.json | items[3].question | What is $\int_{-3}^{2} (\|x\| - 1)\,dx$? | correct | B6 |
| homework-1.json | items[3].widget.answer | graded key (numeric): 1.5 | correct | B6 |
| homework-1.json | items[3].widget.wrong[0] | slip area = 3.5 is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[3].widget.wrong[1] | slip above = 2.5 is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[3].widget.wrong[2] | slip below = -1 is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[3].widget.accept | 1.5: $2 - 1 + 0.5$. | correct | B6 |
| homework-1.json | items[3].feedback.correct | $2 - 1 + 0.5 = 1.5$. | correct | B6 |
| homework-1.json | items[3].feedback.generic | Not quite right. Split at $-1$ and 1, where the graph crosses the axis. | correct | B6 |
| homework-1.json | items[3].feedback.byKey.area | 3.5 is the total area. The triangle on $[-1, 1]$ is below the axis and counts $-1$. | correct | B6 |
| homework-1.json | items[3].feedback.byKey.above | That adds only the parts above the axis. The part below counts $-1$. | correct | B6 |
| homework-1.json | items[3].feedback.byKey.below | That is the part below the axis alone. Add the triangles above it. | correct | B6 |
| homework-1.json | items[3].explain.text | The graph crosses the axis at $-1$ and 1. The pieces on $[-3, -1]$, $[-1, 1]$ and $[1, 2]$ have areas 2, 1 ... | correct | B6 |
| homework-1.json | items[4].prose | You know $\int_0^5 f(x)\,dx = 8$ and $\int_3^5 f(x)\,dx = 10$. | correct | B6 |
| homework-1.json | items[4].question | What is $\int_3^0 f(x)\,dx$? | correct | B6 |
| homework-1.json | items[4].widget.answer | graded key (numeric): 2 | correct | B6 |
| homework-1.json | items[4].widget.wrong[0] | slip no-flip = -2 is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[4].widget.wrong[1] | slip added = 18 is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[4].widget.wrong[2] | slip neg-added = -18 is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[4].widget.accept | 2: $\int_0^3 f\,dx = -2$, and reversing gives 2. | correct | B6 |
| homework-1.json | items[4].feedback.correct | $\int_0^3 = 8 - 10 = -2$, so $\int_3^0 = 2$. | correct | B6 |
| homework-1.json | items[4].feedback.generic | Not quite right. Split $\int_0^5$ at 3, then reverse the limits. | correct | B6 |
| homework-1.json | items[4].feedback.byKey.no-flip | $-2$ is $\int_0^3 f\,dx$. The question runs from 3 down to 0, which flips the sign. | correct | B6 |
| homework-1.json | items[4].feedback.byKey.added | You added the integrals. Splitting gives $8 = \int_0^3 f\,dx + 10$. | correct | B6 |
| homework-1.json | items[4].feedback.byKey.neg-added | You added the integrals and flipped. Splitting gives $8 = \int_0^3 f\,dx + 10$ first. | correct | B6 |
| homework-1.json | items[4].explain.text | Splitting at 3: $\int_0^5 = \int_0^3 + \int_3^5$, so $\int_0^3 f\,dx = 8 - 10 = -2$. Reversing the limits f... | correct | B6 |
| homework-1.json | items[5].prose | The bars show a stock's average trading rate in each half hour of its first four hours. Rates are in shares... | correct | B6 |
| homework-1.json | items[5].canvas.params.categories[0].label | 08:00 | correct | B6 |
| homework-1.json | items[5].canvas.params.categories[1].label | 08:30 | correct | B6 |
| homework-1.json | items[5].canvas.params.categories[2].label | 09:00 | correct | B6 |
| homework-1.json | items[5].canvas.params.categories[3].label | 09:30 | correct | B6 |
| homework-1.json | items[5].canvas.params.categories[4].label | 10:00 | correct | B6 |
| homework-1.json | items[5].canvas.params.categories[5].label | 10:30 | correct | B6 |
| homework-1.json | items[5].canvas.params.categories[6].label | 11:00 | correct | B6 |
| homework-1.json | items[5].canvas.params.categories[7].label | 11:30 | correct | B6 |
| homework-1.json | items[5].question | How many shares traded in the four hours? | correct | B6 |
| homework-1.json | items[5].widget.answer | graded key (numeric): 375000 | correct | B6 |
| homework-1.json | items[5].widget.wrong[0] | slip no-minutes = 12500 is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[5].widget.wrong[1] | slip hours = 750000 is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[5].widget.wrong[2] | slip quarter = 187500 is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[5].widget.accept | 375,000: $12{,}500 \times 30$. | correct | B6 |
| homework-1.json | items[5].feedback.correct | $12{,}500 \times 30 = 375{,}000$ shares. | correct | B6 |
| homework-1.json | items[5].feedback.generic | Not quite right. Each bar covers 30 minutes: rate times 30 gives that half hour's volume. | correct | B6 |
| homework-1.json | items[5].feedback.byKey.no-minutes | You added the rates. Each rate lasts 30 minutes, so multiply by 30. | correct | B6 |
| homework-1.json | items[5].feedback.byKey.hours | You multiplied by 60, as if each bar lasted an hour. Each covers half an hour. | correct | B6 |
| homework-1.json | items[5].feedback.byKey.quarter | You multiplied by 15. Each bar covers 30 minutes. | correct | B6 |
| homework-1.json | items[5].explain.text | Each bar is 30 minutes wide, so its area, rate times 30, is that half hour's volume. The rates add to 12,50... | correct | B6 |
| homework-1.json | items[6].prose | In the seconds before a closing auction, orders arrive at a rate of $v(t) = 300t^2$ shares per second, for ... | correct | B6 |
| homework-1.json | items[6].question | How many shares arrive over the 10 seconds? | correct | B6 |
| homework-1.json | items[6].widget.answer | graded key (numeric): 100000 | correct | B6 |
| homework-1.json | items[6].widget.wrong[0] | slip rate = 30000 is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[6].widget.wrong[1] | slip box = 300000 is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[6].widget.wrong[2] | slip triangle = 150000 is the value of the named mistake and is not a correct answer | correct | B6 |
| homework-1.json | items[6].widget.accept | 100,000: $300 \times \tfrac{10^3}{3}$. | correct | B6 |
| homework-1.json | items[6].feedback.correct | $300 \times \tfrac{1000}{3} = 100{,}000$ shares. | correct | B6 |
| homework-1.json | items[6].feedback.generic | Not quite right. Find $\int_0^{10} t^2\,dt$ from the right sums, then multiply by 300. | correct | B6 |
| homework-1.json | items[6].feedback.byKey.rate | 30,000 is the rate at $t = 10$, in shares per second. The amount is the area under the rate. | correct | B6 |
| homework-1.json | items[6].feedback.byKey.box | $30{,}000 \times 10$ assumes the top rate all along. The rate starts at 0 and climbs. | correct | B6 |
| homework-1.json | items[6].feedback.byKey.triangle | That treats the rate as a straight line. It curves, $300t^2$, so the region is thinner than a triangle. | correct | B6 |
| homework-1.json | items[6].explain.text | On $[0, b]$ the right sum of $t^2$ is $\tfrac{b^3}{n^3} \cdot \tfrac{n(n+1)(2n+1)}{6} \to \tfrac{b^3}{3}$. ... | correct | B6 |
| homework-1.json | items[7].prompt | A market maker's buying rate is $q(t) = 600 - 200t$ shares per minute for $0 \le t \le 5$. A negative rate ... | correct | B6 |
| homework-1.json | items[7].model | **(a)** With $n = 5$ the width is $\Delta t = \tfrac{5 - 0}{5} = 1$ minute. Left ends $0, 1, 2, 3, 4$: $q =... | correct | B7 |
| homework-1.json | items[7].rubric[0].text | Finds $L_5 = 1000$ and $R_5 = 0$ with width 1, and says the left sum overestimates because $q$ falls. | correct | B7 |
| homework-1.json | items[7].rubric[1].text | Splits at $t = 3$ and finds $900 - 400 = 500$ shares, with the lower triangle counted negative. Checks it l... | correct | B7 |
| homework-1.json | items[7].rubric[2].text | Gives 1,300 shares traded as the total area $900 + 400$. Explains that area counts selling as positive whil... | correct | B7 |
| homework-1.json | items[7].rubric[3].text | Places the peak at $t = 3$, where $q$ changes sign, with inventory 900 above the start. Explains why it is ... | correct | B7 |
| homework-1.json | items[7].rubric[4].text | Uses the gap $\|q(5) - q(0)\| \cdot \tfrac{5}{n} = \tfrac{4000}{n}$ and concludes $n \ge 4000$. | correct | B7 |
| homework-1.json | items[8].prompt | Take $f(x) = 9 - x^2$ on $[1, 3]$. Derive the exact value of $\int_1^3 (9 - x^2)\,dx$ from the limit of Rie... | correct | B6 |
| homework-1.json | items[8].model | **Setting up.** With $n$ strips on $[1, 3]$, each has width $\Delta x = \tfrac{3 - 1}{n} = \tfrac{2}{n}$. S... | correct | B7 |
| homework-1.json | items[8].rubric[0].text | (a) Tick only if all are given. The strips are set up: $\Delta x = \tfrac2n$, strip ends $1 + \tfrac{2k}{n}... | correct | B7 |
| homework-1.json | items[8].rubric[1].text | (b) Finds the limit $\tfrac{28}{3}$, saying why each term with $n$ on the bottom tends to 0. | correct | B7 |
| homework-1.json | items[8].rubric[2].text | (c) Gives a reason the limit is the area. Either $R_n \le A \le L_n$ with both ends, or the gap $\tfrac{16}... | correct | B7 |
| homework-1.json | items[8].rubric[3].text | (c) Optional part. Says the left sum is too big because $f$ falls on $[1, 3]$, so the left end is the highe... | correct | B7 |
| homework-1.json | items[8].rubric[4].text | (d) Finds $R_4 = 7.25$ and $L_4 = 11.25$ from the heights, matches the formula from (a) at $n = 4$, and pla... | correct | B7 |
| problems-1.json | items[0].prose | Take the falling curve $f(x) = 12 - 3x^2$ on $[0, 2]$. We split $[0, 2]$ into strips of equal width and est... | correct | B8 |
| problems-1.json | items[0].parts[0].question | With $n = 4$ strips, each 0.5 wide, what is the right sum $R_4$? Give the exact decimal. | correct | B8 |
| problems-1.json | items[0].parts[0].widget.answer | graded key (numeric): 12.75 | correct | B8 |
| problems-1.json | items[0].parts[0].widget.wrong[0] | slip left-ends = 18.75 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[0].parts[0].widget.wrong[1] | slip no-width = 25.5 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[0].parts[0].widget.accept | 12.75 | correct | B8 |
| problems-1.json | items[0].parts[0].feedback.correct | The right ends 0.5, 1, 1.5 and 2 have heights 11.25, 9, 5.25 and 0. Their sum, 25.5, times the width 0.5 is... | correct | B8 |
| problems-1.json | items[0].parts[0].feedback.generic | Not quite. Take each height at the right end of its strip, then multiply the sum by the width. | correct | B8 |
| problems-1.json | items[0].parts[0].feedback.byKey.left-ends | You took each height at the left end of its strip. That is $L_4$; the right sum starts at $x = 0.5$. | correct | B8 |
| problems-1.json | items[0].parts[0].feedback.byKey.no-width | You added the four heights but did not multiply by the width 0.5. | correct | B8 |
| problems-1.json | items[0].parts[0].explain.text | $R_4 = 0.5 \times 25.5 = 12.75$. On a falling curve each right end is the low point of its strip, so $R_4$ ... | correct | B8 |
| problems-1.json | items[0].parts[1].question | Using $R_4 = 12.75$, the gap rule for a curve that only falls gives $L_4$ without adding four more heights.... | correct | B8 |
| problems-1.json | items[0].parts[1].widget.answer | graded key (numeric): 18.75 | correct | B8 |
| problems-1.json | items[0].parts[1].widget.wrong[0] | slip subtracted = 6.75 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[0].parts[1].widget.wrong[1] | slip no-length = 15.75 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[0].parts[1].widget.accept | 18.75 | correct | B8 |
| problems-1.json | items[0].parts[1].feedback.correct | The gap is $\|f(2) - f(0)\| \times \tfrac{2}{4} = 12 \times 0.5 = 6$. The left sum is the larger here, so $... | correct | B8 |
| problems-1.json | items[0].parts[1].feedback.generic | Not quite. Find the gap $\|f(b) - f(a)\|\,\tfrac{b - a}{n}$, then decide which sum is the larger. | correct | B8 |
| problems-1.json | items[0].parts[1].feedback.byKey.subtracted | You took the gap away. On a falling curve the left ends are the high points, so $L_4$ is above $R_4$. | correct | B8 |
| problems-1.json | items[0].parts[1].feedback.byKey.no-length | You used a gap of $12 \times \tfrac{1}{4}$. Each strip is $\tfrac{2}{4}$ wide, not $\tfrac{1}{4}$. | correct | B8 |
| problems-1.json | items[0].parts[1].explain.text | For a curve that only falls, $L_n - R_n = \|f(b) - f(a)\|\,\tfrac{b - a}{n}$. Here that is $12 \times 0.5 =... | correct | B8 |
| problems-1.json | items[0].parts[2].question | Part 2's gap rule gives $L_n - R_n = 12 \times \tfrac{2}{n}$ for $n$ strips. What is the smallest $n$ that ... | correct | B8 |
| problems-1.json | items[0].parts[2].widget.answer | graded key (numeric): 240 | correct | B8 |
| problems-1.json | items[0].parts[2].widget.wrong[0] | slip no-length = 120 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[0].parts[2].widget.wrong[1] | slip strict = 241 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[0].parts[2].feedback.correct | $\tfrac{24}{n} \le 0.1$ needs $n \ge 240$. At $n = 240$ the gap is exactly 0.1, which is allowed. | correct | B8 |
| problems-1.json | items[0].parts[2].feedback.generic | Not quite. Solve $\tfrac{24}{n} \le 0.1$ for $n$. | correct | B8 |
| problems-1.json | items[0].parts[2].feedback.byKey.no-length | You used a gap of $\tfrac{12}{n}$. Each strip is $\tfrac{2}{n}$ wide, so the gap is $\tfrac{24}{n}$. | correct | B8 |
| problems-1.json | items[0].parts[2].feedback.byKey.strict | At $n = 240$ the gap is exactly 0.1, and the question allows 0.1. So 240 is enough. | correct | B8 |
| problems-1.json | items[0].parts[2].explain.text | $12 \times \tfrac{2}{n} \le 0.1$ rearranges to $n \ge 240$. So 240 strips trap the area in a band 0.1 wide. | correct | B8 |
| problems-1.json | items[0].parts[3].question | With $n$ strips, $\Delta x = \tfrac{2}{n}$ and the right ends are $x_k = \tfrac{2k}{n}$. Use $1^2 + 2^2 + \... | correct | B8 |
| problems-1.json | items[0].parts[3].widget.answer | graded key (expression): "16-\\frac{12}{n}-\\frac{4}{n^2}" | correct | B8 |
| problems-1.json | items[0].parts[3].widget.wrong[0] | slip left-ends = "16+\\frac{12}{n}-\\frac{4}{n^2}" is the value of the named mistake and is not a correct a... | correct | B8 |
| problems-1.json | items[0].parts[3].widget.wrong[1] | slip once = "12-\\frac{4(n+1)(2n+1)}{n^2}" is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[0].parts[3].widget.wrong[2] | slip no-width = "12n-\\frac{2(n+1)(2n+1)}{n}" is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[0].parts[3].feedback.correct | $R_n = \sum_{k=1}^{n}\left(12 - \tfrac{12k^2}{n^2}\right)\tfrac{2}{n} = 24 - \tfrac{4(n+1)(2n+1)}{n^2}$, wh... | correct | B8 |
| problems-1.json | items[0].parts[3].feedback.generic | Not quite. Write rectangle $k$ as height times width, then add the 12s and the squares separately. | correct | B8 |
| problems-1.json | items[0].parts[3].feedback.byKey.left-ends | That is $L_n$, which is above $R_n$ by $\tfrac{24}{n}$. The right ends run from $\tfrac{2}{n}$ up to 2. | correct | B8 |
| problems-1.json | items[0].parts[3].feedback.byKey.once | You counted the 12 once. Each of the $n$ strips has a 12 in its height and width $\tfrac{2}{n}$, so the 12s... | correct | B8 |
| problems-1.json | items[0].parts[3].feedback.byKey.no-width | You added the heights but left out the width $\tfrac{2}{n}$ of each strip. | correct | B8 |
| problems-1.json | items[0].parts[3].explain.text | Rectangle $k$ has height $12 - \tfrac{12k^2}{n^2}$ and width $\tfrac{2}{n}$. The 12s add to 24, and the squ... | correct | B8 |
| problems-1.json | items[0].parts[4].question | Using $R_n = 16 - \tfrac{12}{n} - \tfrac{4}{n^2}$ from part 4, what is the exact area under $f$ on $[0, 2]$? | correct | B8 |
| problems-1.json | items[0].parts[4].widget.answer | graded key (numeric): 16 | correct | B8 |
| problems-1.json | items[0].parts[4].widget.wrong[0] | slip no-squares = 24 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[0].parts[4].widget.wrong[1] | slip stopped = 12.75 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[0].parts[4].widget.wrong[2] | slip once = 4 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[0].parts[4].feedback.correct | As $n \to \infty$ both $\tfrac{12}{n}$ and $\tfrac{4}{n^2}$ tend to 0, so the area is 16. It sits between $... | correct | B8 |
| problems-1.json | items[0].parts[4].feedback.generic | Not quite. Let $n$ grow without limit and see which terms survive. | correct | B8 |
| problems-1.json | items[0].parts[4].feedback.byKey.no-squares | 24 is the $2 \times 12$ box, before the squares come off. The limit of $R_n$ is 16. | correct | B8 |
| problems-1.json | items[0].parts[4].feedback.byKey.stopped | That is $R_4$, an underestimate. Let $n$ grow without limit. | correct | B8 |
| problems-1.json | items[0].parts[4].feedback.byKey.once | A limit of 4 comes from counting the 12 once in part 4. With 24 for the 12s, the limit is $24 - 8 = 16$. | correct | B8 |
| problems-1.json | items[0].parts[4].explain.text | The error terms $\tfrac{12}{n}$ and $\tfrac{4}{n^2}$ vanish as $n$ grows, so $R_n \to 16$. The $2 \times 12... | correct | B8 |
| problems-1.json | items[1].prose | A new index fund's net subscriptions arrive at a rate $s(t) = 12 - 4t$, in £m per week, $t$ weeks after lau... | correct | B8 |
| problems-1.json | items[1].parts[0].question | After how many weeks does the fund's running total of net subscriptions stop rising? | correct | B8 |
| problems-1.json | items[1].parts[0].widget.answer | graded key (numeric): 3 | correct | B8 |
| problems-1.json | items[1].parts[0].widget.wrong[0] | slip rate-highest = 0 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[1].parts[0].widget.wrong[1] | slip zero-total = 6 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[1].parts[0].feedback.correct | The total rises while $s(t) > 0$ and falls once $s$ turns negative. $12 - 4t = 0$ at $t = 3$ weeks. | correct | B8 |
| problems-1.json | items[1].parts[0].feedback.generic | Not quite. The running total rises while the rate is positive. | correct | B8 |
| problems-1.json | items[1].parts[0].feedback.byKey.rate-highest | The rate is highest at launch, but the total keeps growing after that. It stops rising where the rate reach... | correct | B8 |
| problems-1.json | items[1].parts[0].feedback.byKey.zero-total | At week 6 the total is back to zero. It stopped rising well before that, when the rate crossed 0. | correct | B8 |
| problems-1.json | items[1].parts[0].explain.text | A running total climbs while its rate is positive. $s(t) = 12 - 4t$ is positive until $t = 3$, so the total... | correct | B8 |
| problems-1.json | items[1].parts[1].question | Using the peak at week 3, how much has the fund taken in by then, in £m? | correct | B8 |
| problems-1.json | items[1].parts[1].widget.answer | graded key (numeric): 18 | correct | B8 |
| problems-1.json | items[1].parts[1].widget.wrong[0] | slip rectangle = 36 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[1].parts[1].widget.wrong[1] | slip rate = 12 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[1].parts[1].feedback.correct | The region under $s$ from 0 to 3 is a triangle with base 3 and height 12. Its area is $\tfrac{1}{2} \times ... | correct | B8 |
| problems-1.json | items[1].parts[1].feedback.generic | Not quite. The total is the area under the rate from 0 to 3. | correct | B8 |
| problems-1.json | items[1].parts[1].feedback.byKey.rectangle | You used a $3 \times 12$ rectangle. The rate falls to 0 at week 3, so the region is a triangle: halve it. | correct | B8 |
| problems-1.json | items[1].parts[1].feedback.byKey.rate | 12 is the opening rate in £m per week, not a total. The total is the area under the rate. | correct | B8 |
| problems-1.json | items[1].parts[1].explain.text | The total by week 3 is $\int_0^3 (12 - 4t)\,dt$, the area of a triangle. $\tfrac{1}{2} \times 3 \times 12 =... | correct | B8 |
| problems-1.json | items[1].parts[2].question | Part 2 found £18m in by week 3. What is the net amount subscribed over the first 5 weeks, in £m? | correct | B8 |
| problems-1.json | items[1].parts[2].widget.answer | graded key (numeric): 10 | correct | B8 |
| problems-1.json | items[1].parts[2].widget.wrong[0] | slip gross = 26 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[1].parts[2].widget.wrong[1] | slip peak = 18 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[1].parts[2].widget.wrong[2] | slip only-outflow = -8 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[1].parts[2].feedback.correct | From week 3 to 5 the rate runs from 0 down to $-8$: a triangle of area $\tfrac{1}{2} \times 2 \times 8 = 8$... | correct | B8 |
| problems-1.json | items[1].parts[2].feedback.generic | Not quite. Split at week 3 and give the region below the axis a minus sign. | correct | B8 |
| problems-1.json | items[1].parts[2].feedback.byKey.gross | You added the outflow. Area below the axis counts negative in the net change. | correct | B8 |
| problems-1.json | items[1].parts[2].feedback.byKey.peak | That is the total at week 3. Weeks 4 and 5 take money out, so include them. | correct | B8 |
| problems-1.json | items[1].parts[2].feedback.byKey.only-outflow | That is weeks 3 to 5 alone. Add the £18m from the first 3 weeks. | correct | B8 |
| problems-1.json | items[1].parts[2].explain.text | $\int_0^5 s\,dt = \int_0^3 s\,dt + \int_3^5 s\,dt = 18 - 8 = 10$. The outflow triangle has base 2 and heigh... | correct | B8 |
| problems-1.json | items[1].parts[3].question | Part 3 gave $\int_0^5 s(t)\,dt = 10$. A script integrates the rate from week 5 back to week 0 by mistake, $... | correct | B8 |
| problems-1.json | items[1].parts[3].widget.answer | graded key (numeric): -10 | correct | B8 |
| problems-1.json | items[1].parts[3].widget.wrong[0] | slip no-flip = 10 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[1].parts[3].widget.wrong[1] | slip gross = -26 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[1].parts[3].feedback.correct | Reversing the limits flips the sign: $\int_5^0 s\,dt = -\int_0^5 s\,dt = -10$. | correct | B8 |
| problems-1.json | items[1].parts[3].feedback.generic | Not quite. Think about what running the sum backwards does to each width. | correct | B8 |
| problems-1.json | items[1].parts[3].feedback.byKey.no-flip | That is $\int_0^5 s\,dt$. Swapping the limits flips the sign. | correct | B8 |
| problems-1.json | items[1].parts[3].feedback.byKey.gross | You flipped the sign of the gross flow, $18 + 8$. Flip the net figure 10 instead. | correct | B8 |
| problems-1.json | items[1].parts[3].explain.text | Each strip now has width $-\Delta t$, because $t$ steps from 5 back to 0. So $\int_5^0 s\,dt = -\int_0^5 s\... | correct | B8 |
| problems-1.json | items[1].parts[4].question | Suppose the rate keeps falling the same way after week 5. Using the £18m in by week 3, after how many weeks... | correct | B8 |
| problems-1.json | items[1].parts[4].widget.answer | graded key (numeric): 6 | correct | B8 |
| problems-1.json | items[1].parts[4].widget.wrong[0] | slip no-half = 5.1213 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[1].parts[4].widget.wrong[1] | slip rate-zero = 3 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[1].parts[4].feedback.correct | From week 3 the outflow triangle has base $T - 3$ and height $4(T - 3)$, so its area is $2(T - 3)^2$. Setti... | correct | B8 |
| problems-1.json | items[1].parts[4].feedback.generic | Not quite. The total is back to zero when the area below the axis matches the area above it. | correct | B8 |
| problems-1.json | items[1].parts[4].feedback.byKey.no-half | You used $4(T - 3)^2$ for the outflow triangle. A triangle's area is half its base times its height. | correct | B8 |
| problems-1.json | items[1].parts[4].feedback.byKey.rate-zero | Week 3 is where the total peaks. The outflow needs as long again to undo the £18m. | correct | B8 |
| problems-1.json | items[1].parts[4].explain.text | The total returns to zero when the outflow triangle's area equals the £18m. $2(T - 3)^2 = 18$ gives $T = 6$. | correct | B8 |
| problems-1.json | items[2].prose | A desk's P&L rate over a 3-hour session is $r(t) = t^2 - 4$, in £k per hour, $t$ hours after the open. For ... | correct | B8 |
| problems-1.json | items[2].parts[0].question | Estimate the session's net P&L, $\int_0^3 r(t)\,dt$, with the midpoint sum on 3 strips of width 1. Give the... | correct | B8 |
| problems-1.json | items[2].parts[0].widget.answer | graded key (numeric): -3.25 | correct | B8 |
| problems-1.json | items[2].parts[0].widget.wrong[0] | slip right-ends = 2 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[2].parts[0].widget.wrong[1] | slip left-ends = -7 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[2].parts[0].widget.wrong[2] | slip unsigned = 7.75 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[2].parts[0].widget.wrong[3] | slip sign = 3.25 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[2].parts[0].widget.accept | -3.25 | correct | B8 |
| problems-1.json | items[2].parts[0].feedback.correct | At the midpoints 0.5, 1.5 and 2.5 the rate is $-3.75$, $-1.75$ and $2.25$. Times the width 1, the sum is $-... | correct | B8 |
| problems-1.json | items[2].parts[0].feedback.generic | Not quite. Take each height at the middle of its strip and keep the signs. | correct | B8 |
| problems-1.json | items[2].parts[0].feedback.byKey.right-ends | You took the heights at the right ends, 1, 2 and 3. The midpoints are 0.5, 1.5 and 2.5. | correct | B8 |
| problems-1.json | items[2].parts[0].feedback.byKey.left-ends | You took the heights at the left ends, 0, 1 and 2. The midpoints are 0.5, 1.5 and 2.5. | correct | B8 |
| problems-1.json | items[2].parts[0].feedback.byKey.unsigned | You counted the strips below the axis as positive. A loss rate makes those rectangles count negative. | correct | B8 |
| problems-1.json | items[2].parts[0].feedback.byKey.sign | The two strips below the axis outweigh the one above, so the net is below zero. A positive 3.25 books the n... | correct | B8 |
| problems-1.json | items[2].parts[0].explain.text | $M_3 = 1 \times (-3.75 - 1.75 + 2.25) = -3.25$. The first two strips hang below the axis, so they count neg... | correct | B8 |
| problems-1.json | items[2].parts[1].question | Now the exact value. Using $\int_0^3 t^2\,dt = 9$, what is the net P&L $\int_0^3 (t^2 - 4)\,dt$, in £k? | correct | B8 |
| problems-1.json | items[2].parts[1].widget.answer | graded key (numeric): -3 | correct | B8 |
| problems-1.json | items[2].parts[1].widget.wrong[0] | slip once = 5 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[2].parts[1].widget.wrong[1] | slip squares-only = 9 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[2].parts[1].widget.wrong[2] | slip sign = 3 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[2].parts[1].feedback.correct | Lowering every height by 4 lowers the area by a $3 \times 4$ rectangle. So $9 - 12 = -3$, a loss of £3k. | correct | B8 |
| problems-1.json | items[2].parts[1].feedback.generic | Not quite. The $-4$ lowers every rectangle for all 3 hours. | correct | B8 |
| problems-1.json | items[2].parts[1].feedback.byKey.once | You took off 4 once. The rate is 4 lower for all 3 hours, so take off $4 \times 3 = 12$. | correct | B8 |
| problems-1.json | items[2].parts[1].feedback.byKey.squares-only | That is the area under $t^2$ alone. The $-4$ in the rate takes off a $3 \times 4$ rectangle. | correct | B8 |
| problems-1.json | items[2].parts[1].feedback.byKey.sign | 9 − 12 is below zero, because the 12 taken off is bigger than the 9. A positive 3 takes 12 − 9, the wrong w... | correct | B8 |
| problems-1.json | items[2].parts[1].explain.text | In each Riemann sum the $-4$ adds $-4 \times 3$ over the 3 hours. So $\int_0^3 (t^2 - 4)\,dt = 9 - 12 = -3$... | correct | B8 |
| problems-1.json | items[2].parts[2].question | At what time $t$ is the running P&L lowest? | correct | B8 |
| problems-1.json | items[2].parts[2].widget.answer | graded key (numeric): 2 | correct | B8 |
| problems-1.json | items[2].parts[2].widget.wrong[0] | slip rate-lowest = 0 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[2].parts[2].widget.wrong[1] | slip end = 3 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[2].parts[2].feedback.correct | The running P&L falls while $r(t) < 0$. $t^2 - 4 = 0$ at $t = 2$, and after that the desk earns. | correct | B8 |
| problems-1.json | items[2].parts[2].feedback.generic | Not quite. The running P&L falls while the rate is negative. | correct | B8 |
| problems-1.json | items[2].parts[2].feedback.byKey.rate-lowest | The rate is lowest at the open, but the P&L keeps falling until the rate reaches 0. | correct | B8 |
| problems-1.json | items[2].parts[2].feedback.byKey.end | The desk earns from $t = 2$ to 3, so the P&L at the close is above its low point. | correct | B8 |
| problems-1.json | items[2].parts[2].explain.text | The running P&L $\int_0^T r(t)\,dt$ falls while $r < 0$ and rises once $r > 0$. The rate crosses 0 at $t = ... | correct | B8 |
| problems-1.json | items[2].parts[3].question | Using the low at $t = 2$, how low does the running P&L go? Give your answer in £k to 2 decimal places. | correct | B8 |
| problems-1.json | items[2].parts[3].widget.answer | graded key (numeric): -5.333333333333333 | correct | B8 |
| problems-1.json | items[2].parts[3].widget.wrong[0] | slip sign = 5.33 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[2].parts[3].widget.wrong[1] | slip squares-only = 2.67 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[2].parts[3].widget.wrong[2] | slip rect-only = -8 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[2].parts[3].widget.accept | Any form equal to $-\tfrac{16}{3}$, or $-5.33 \pm 0.005$ | correct | B8 |
| problems-1.json | items[2].parts[3].feedback.correct | $\int_0^2 t^2\,dt = \tfrac{8}{3}$, and the $-4$ takes off $2 \times 4 = 8$. So the low is $\tfrac{8}{3} - 8... | correct | B8 |
| problems-1.json | items[2].parts[3].feedback.generic | Not quite. Use $\tfrac{b^3}{3}$ with $b = 2$, then take off the rectangle for the $-4$. | correct | B8 |
| problems-1.json | items[2].parts[3].feedback.byKey.sign | The P&L is below zero here: the rate is negative for the first 2 hours. Keep the minus sign. | correct | B8 |
| problems-1.json | items[2].parts[3].feedback.byKey.squares-only | $\tfrac{8}{3}$ is the area under $t^2$ alone. Take off the $2 \times 4$ rectangle as well. | correct | B8 |
| problems-1.json | items[2].parts[3].feedback.byKey.rect-only | You took off the rectangle but left out the $\tfrac{8}{3}$ under $t^2$. | correct | B8 |
| problems-1.json | items[2].parts[3].explain.text | With $b = 2$, $\int_0^2 t^2\,dt = \tfrac{8}{3}$. Then $\int_0^2 (t^2 - 4)\,dt = \tfrac{8}{3} - 8 = -\tfrac{... | correct | B8 |
| problems-1.json | items[2].parts[4].question | The session ends at $-3$ (part 2), after a low of $-\tfrac{16}{3}$ at $t = 2$ (part 4). How much does the d... | correct | B8 |
| problems-1.json | items[2].parts[4].widget.answer | graded key (numeric): 2.3333333333333335 | correct | B8 |
| problems-1.json | items[2].parts[4].widget.wrong[0] | slip added = -8.33 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[2].parts[4].widget.wrong[1] | slip reversed = -2.33 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[2].parts[4].widget.wrong[2] | slip rate-end = 5 is the value of the named mistake and is not a correct answer | correct | B8 |
| problems-1.json | items[2].parts[4].widget.accept | Any form equal to $\tfrac{7}{3}$, or $2.33 \pm 0.005$ | correct | B8 |
| problems-1.json | items[2].parts[4].feedback.correct | Split the session at $t = 2$: $\int_0^3 r\,dt = \int_0^2 r\,dt + \int_2^3 r\,dt$. So the last hour makes $-... | correct | B8 |
| problems-1.json | items[2].parts[4].feedback.generic | Not quite. Split $\int_0^3$ at $t = 2$ and solve for the second piece. | correct | B8 |
| problems-1.json | items[2].parts[4].feedback.byKey.added | You added the two figures. By the split rule the last hour is the whole session minus the first 2 hours. | correct | B8 |
| problems-1.json | items[2].parts[4].feedback.byKey.reversed | That is $\int_3^2 r\,dt$, with the limits reversed. The desk gains in the last hour, so the answer is posit... | correct | B8 |
| problems-1.json | items[2].parts[4].feedback.byKey.rate-end | 5 is the rate at the close, in £k per hour. The hour's P&L is the area under the rate from 2 to 3. | correct | B8 |
| problems-1.json | items[2].parts[4].explain.text | Integrals over touching intervals add, so $\int_2^3 r\,dt = -3 - (-\tfrac{16}{3}) = \tfrac{7}{3}$. As a che... | correct | B8 |
| l5-area-undoes-slope.json | screens[0].prose | The curve is $f(t) = t(4 - t)$. The shaded region runs from $t = 0$ to a right edge at $t = x$. Drag the do... | correct | B9 |
| l5-area-undoes-slope.json | screens[0].canvas.derive.caption | Edge at $x$ = {{fixed(X.x, 2)}}: shaded area {{fixed(2*X.x*X.x - pow(X.x,3)/3, 2)}} | correct | B9 |
| l5-area-undoes-slope.json | screens[0].question | Drag $x$ from 0 to 4 in small steps. Where does the shaded area grow fastest? | correct | B9 |
| l5-area-undoes-slope.json | screens[0].widget.options[0] | graded key (choice): Near $x = 2$, where the curve is tallest | correct | B9 |
| l5-area-undoes-slope.json | screens[0].widget.options[1].text | wrong option, wrong under every convention: Near $x = 4$, where the area is largest | correct | B9 |
| l5-area-undoes-slope.json | screens[0].widget.options[1].why | You watched the total, which is biggest at the end. Near 4 each step adds only a sliver, because the curve ... | correct | B9 |
| l5-area-undoes-slope.json | screens[0].widget.options[2].text | wrong option, wrong under every convention: Near $x = 0$, where the region starts | correct | B9 |
| l5-area-undoes-slope.json | screens[0].widget.options[2].why | Near 0 the curve hugs the axis, so each step adds a thin sliver of area. | correct | B9 |
| l5-area-undoes-slope.json | screens[0].widget.options[3].text | wrong option, wrong under every convention: At the same rate everywhere | correct | B9 |
| l5-area-undoes-slope.json | screens[0].widget.options[3].why | Each step adds a strip as tall as the curve at the edge. The curve's height changes, so the strips do too. | correct | B9 |
| l5-area-undoes-slope.json | screens[0].hints[0].text | Move $x$ by 0.25 at a time and note how much the area changes each step. | correct | B9 |
| l5-area-undoes-slope.json | screens[0].hints[1].text | Compare the step from 1.75 to 2 with the step from 3.75 to 4. | correct | B9 |
| l5-area-undoes-slope.json | screens[0].hints[2].text | Each step adds a strip whose height is the curve's height at the edge. Where is the curve tallest? | correct | B9 |
| l5-area-undoes-slope.json | screens[0].feedback.correct | Each step adds a strip as tall as the curve, and the curve is tallest at 2. | correct | B9 |
| l5-area-undoes-slope.json | screens[0].feedback.generic | Not quite right. Compare how much area one small step adds at different places. | correct | B9 |
| l5-area-undoes-slope.json | screens[0].explain.text | From 1.75 to 2 the area grows by about 0.99, but from 3.75 to 4 by only about 0.12. Each step adds a strip ... | correct | B9 |
| l5-area-undoes-slope.json | screens[1].prose | Call the shaded area $A(x)$. In symbols, $A(x) = \int_0^x f(t)\,dt$, the **accumulation function**. We writ... | correct | B9 |
| l5-area-undoes-slope.json | screens[1].canvas.derive.caption | $x$ = {{fixed(X.x, 2)}}: height $f(x)$ = {{fixed(X.x*(4 - X.x), 2)}}, area $A(x)$ = {{fixed(2*X.x*X.x - pow... | correct | B9 |
| l5-area-undoes-slope.json | screens[1].question | Drag $x$ to 1, 2 and 3. Each time, compare the slope of the $A$ graph with the height $f(x)$. What is the s... | correct | B9 |
| l5-area-undoes-slope.json | screens[1].widget.answer | graded key (numeric): 3 | correct | B9 |
| l5-area-undoes-slope.json | screens[1].widget.wrong[0] | slip area = 9 is the value of the named mistake and is not a correct answer | correct | B9 |
| l5-area-undoes-slope.json | screens[1].widget.wrong[1] | slip fprime = -2 is the value of the named mistake and is not a correct answer | correct | B9 |
| l5-area-undoes-slope.json | screens[1].widget.accept | 3, the height $f(3)$. | correct | B9 |
| l5-area-undoes-slope.json | screens[1].hints[0].text | Read the slope label on the right, and the height $f(x)$ in the caption. | correct | B9 |
| l5-area-undoes-slope.json | screens[1].hints[1].text | At $x = 1$ both read 3. At $x = 2$ both read 4. | correct | B9 |
| l5-area-undoes-slope.json | screens[1].hints[2].text | The slope of $A$ matches $f(x)$ each time. So at 3 it is $f(3) = 3 \times 1 = 3$. | correct | B9 |
| l5-area-undoes-slope.json | screens[1].feedback.correct | At $x = 3$ the slope of $A$ is 3, the same as $f(3)$. | correct | B9 |
| l5-area-undoes-slope.json | screens[1].feedback.generic | Not quite right. Read the slope label on the right graph when $x = 3$. | correct | B9 |
| l5-area-undoes-slope.json | screens[1].feedback.byKey.area | 9 is $A(3)$, the area so far. The slope asks how fast that area grows at 3. | correct | B9 |
| l5-area-undoes-slope.json | screens[1].feedback.byKey.fprime | $-2$ is the slope of $f$ at 3. Read the slope of the $A$ graph on the right instead. | correct | B9 |
| l5-area-undoes-slope.json | screens[1].explain.text | At every $x$ you tried, the slope of $A$ matched the height of $f$. At 3 both are 3, though $A(3) = 9$. The... | correct | B9 |
| l5-area-undoes-slope.json | screens[2].prose | Why does the slope of $A$ match $f$? Move the edge from 2 to 2.25. The region gains a thin strip, 0.25 wide... | correct | B9 |
| l5-area-undoes-slope.json | screens[2].canvas.state.caption | Left: the new strip. Right: the rise in $A$ from 2 to 2.25. | correct | B9 |
| l5-area-undoes-slope.json | screens[2].question | About how much does $A$ rise between $x = 2$ and $x = 2.25$? | correct | B9 |
| l5-area-undoes-slope.json | screens[2].widget.answer | graded key (numeric): 1 | correct | B9 |
| l5-area-undoes-slope.json | screens[2].widget.wrong[0] | slip height = 4 is the value of the named mistake and is not a correct answer | correct | B9 |
| l5-area-undoes-slope.json | screens[2].widget.wrong[1] | slip width = 0.25 is the value of the named mistake and is not a correct answer | correct | B9 |
| l5-area-undoes-slope.json | screens[2].widget.wrong[2] | slip total = 6.33 is the value of the named mistake and is not a correct answer | correct | B9 |
| l5-area-undoes-slope.json | screens[2].widget.accept | About 1: $4 \times 0.25 = 1$. The exact rise is 0.995. | correct | B9 |
| l5-area-undoes-slope.json | screens[2].hints[0].text | The rise in $A$ is the area of the new strip. | correct | B9 |
| l5-area-undoes-slope.json | screens[2].hints[1].text | The strip is nearly a rectangle. | correct | B9 |
| l5-area-undoes-slope.json | screens[2].hints[2].text | Height about 4, width 0.25: area about $4 \times 0.25$. | correct | B9 |
| l5-area-undoes-slope.json | screens[2].feedback.correct | The strip is about $4 \times 0.25 = 1$, and that is the rise in $A$. | correct | B9 |
| l5-area-undoes-slope.json | screens[2].feedback.generic | Not quite right. Find the area of the new strip: height times width. | correct | B9 |
| l5-area-undoes-slope.json | screens[2].feedback.byKey.height | 4 is the strip's height. Its area is height times width. | correct | B9 |
| l5-area-undoes-slope.json | screens[2].feedback.byKey.width | 0.25 is the strip's width. Multiply by its height, about 4. | correct | B9 |
| l5-area-undoes-slope.json | screens[2].feedback.byKey.total | 6.33 is $A(2.25)$, the whole area. We want only the strip added from 2 to 2.25. | correct | B9 |
| l5-area-undoes-slope.json | screens[2].explain.text | The strip is almost a rectangle, so its area is about $f(2) \times 0.25 = 1$. That strip is exactly the ris... | correct | B9 |
| l5-area-undoes-slope.json | screens[3].prose | Now divide the rise by the run $h$. That is the slope of the dashed line on the right. Shrink $h$ with the ... | correct | B9 |
| l5-area-undoes-slope.json | screens[3].canvas.derive.caption | $h$ = {{fixed(h, 2)}}: rise ÷ run = {{fixed(4 - h*h/3, 4)}} | correct | B9 |
| l5-area-undoes-slope.json | screens[3].question | As $h$ shrinks towards 0, what value does rise ÷ run approach? | correct | B9 |
| l5-area-undoes-slope.json | screens[3].widget.answer | graded key (numeric): 4 | correct | B9 |
| l5-area-undoes-slope.json | screens[3].widget.wrong[0] | slip zero = 0 is the value of the named mistake and is not a correct answer | correct | B9 |
| l5-area-undoes-slope.json | screens[3].widget.wrong[1] | slip area = 5.33 is the value of the named mistake and is not a correct answer | correct | B9 |
| l5-area-undoes-slope.json | screens[3].widget.accept | 4, the height $f(2)$. | correct | B9 |
| l5-area-undoes-slope.json | screens[3].hints[0].text | Drag $h$ to its smallest value and read the caption. | correct | B9 |
| l5-area-undoes-slope.json | screens[3].hints[1].text | The dashed line tilts towards the tangent to $A$ at $x = 2$. | correct | B9 |
| l5-area-undoes-slope.json | screens[3].hints[2].text | The ratio is $4 - \tfrac{h^2}{3}$, which tends to 4, the height $f(2)$. | correct | B9 |
| l5-area-undoes-slope.json | screens[3].feedback.correct | The ratio closes in on 4, which is $f(2)$. | correct | B9 |
| l5-area-undoes-slope.json | screens[3].feedback.generic | Not quite right. Read rise ÷ run in the caption as $h$ gets small. | correct | B9 |
| l5-area-undoes-slope.json | screens[3].feedback.byKey.zero | 0 is where the rise itself goes as the strip vanishes. Divided by $h$, the ratio does not vanish. | correct | B9 |
| l5-area-undoes-slope.json | screens[3].feedback.byKey.area | 5.33 is $A(2)$, the area so far, not its rate of growth. | correct | B9 |
| l5-area-undoes-slope.json | screens[3].explain.text | The ratio is $\dfrac{A(2 + h) - A(2)}{h} \approx \dfrac{f(2)\,h}{h} = 4$. As $h \to 0$ the strip's top flat... | correct | B9 |
| l5-area-undoes-slope.json | screens[4].prose | Now let $f(t) = t(4 - t)$ run on to $t = 5$. Past $t = 4$ the curve dips below the axis. Drag $x$ from 4 to 5. | correct | B9 |
| l5-area-undoes-slope.json | screens[4].canvas.derive.caption | $x$ = {{fixed(X.x, 2)}}: $f(x)$ = {{fixed(X.x*(4 - X.x), 2)}}, $A(x)$ = {{fixed(2*X.x*X.x - pow(X.x,3)/3, 2)}} | correct | B9 |
| l5-area-undoes-slope.json | screens[4].question | What happens to $A(x)$ as $x$ moves from 4 to 5? | correct | B9 |
| l5-area-undoes-slope.json | screens[4].widget.options[0] | graded key (choice): It falls, from about 10.67 to 8.33 | correct | B9 |
| l5-area-undoes-slope.json | screens[4].widget.options[1].text | wrong option, wrong under every convention: It keeps rising, more slowly | correct | B9 |
| l5-area-undoes-slope.json | screens[4].widget.options[1].why | You counted the strips below the axis as positive area. In a signed integral they count as negative, so $A$... | correct | B9 |
| l5-area-undoes-slope.json | screens[4].widget.options[2].text | wrong option, wrong under every convention: It stays at 10.67 | correct | B9 |
| l5-area-undoes-slope.json | screens[4].widget.options[2].why | You skipped the region below the axis. It is signed area, so it is subtracted, not ignored. | correct | B9 |
| l5-area-undoes-slope.json | screens[4].hints[0].text | Watch the slope label on the right once $x$ passes 4. | correct | B9 |
| l5-area-undoes-slope.json | screens[4].hints[1].text | Past 4, $f(x)$ is negative. | correct | B9 |
| l5-area-undoes-slope.json | screens[4].hints[2].text | The slope of $A$ is $f(x)$, which is negative past 4. A negative slope means $A$ falls. | correct | B9 |
| l5-area-undoes-slope.json | screens[4].feedback.correct | Past 4 each strip has negative height, so it lowers $A$. | correct | B9 |
| l5-area-undoes-slope.json | screens[4].feedback.generic | Not quite right. Drag past 4 and read $A(x)$ in the caption. | correct | B9 |
| l5-area-undoes-slope.json | screens[4].explain.text | Past $t = 4$ the strips lie below the axis and count as negative. So $A'(x) = f(x) < 0$ there, and $A$ fall... | correct | B9 |
| l5-area-undoes-slope.json | screens[5].prose | Back to $f(t) = t(4 - t)$ and $A(x) = \int_0^x f(t)\,dt$. At $x = 3$ the shaded area is $A(3) = 9$. | correct | B9 |
| l5-area-undoes-slope.json | screens[5].canvas.state.points[0].label | $(3, 3)$ | correct | B9 |
| l5-area-undoes-slope.json | screens[5].canvas.state.caption | $A(3) = 9$ | correct | B9 |
| l5-area-undoes-slope.json | screens[5].question | What is $A'(3)$? | correct | B9 |
| l5-area-undoes-slope.json | screens[5].widget.options[0].text | wrong option, wrong under every convention: $9$ | correct | B9 |
| l5-area-undoes-slope.json | screens[5].widget.options[0].why | You gave the area so far, $A(3)$. The derivative asks how fast that area grows at 3. | correct | B9 |
| l5-area-undoes-slope.json | screens[5].widget.options[1] | graded key (choice): $3$ | correct | B9 |
| l5-area-undoes-slope.json | screens[5].widget.options[2].text | wrong option, wrong under every convention: $-2$ | correct | B9 |
| l5-area-undoes-slope.json | screens[5].widget.options[2].why | You differentiated $f$: $f'(3) = 4 - 6 = -2$. But $A'$ is $f$ itself, not $f'$. | correct | B9 |
| l5-area-undoes-slope.json | screens[5].widget.options[3].text | wrong option, wrong under every convention: $0$ | correct | B9 |
| l5-area-undoes-slope.json | screens[5].widget.options[3].why | You reasoned that a falling curve stops the area growing. $f$ is falling at 3 but still positive, so each s... | correct | B9 |
| l5-area-undoes-slope.json | screens[5].hints[0].text | The derivative measures how fast $A$ changes, not how big it is. | correct | B9 |
| l5-area-undoes-slope.json | screens[5].hints[1].text | A thin strip at the edge has height $f(3)$. | correct | B9 |
| l5-area-undoes-slope.json | screens[5].hints[2].text | $A'(3) = f(3) = 3 \times (4 - 3) = 3$. | correct | B9 |
| l5-area-undoes-slope.json | screens[5].feedback.correct | $A'(3) = f(3) = 3$: the edge height, not the area. | correct | B9 |
| l5-area-undoes-slope.json | screens[5].feedback.generic | Not quite right. The rate at which area piles up is the height of the strip at the edge. | correct | B9 |
| l5-area-undoes-slope.json | screens[5].feedback.byKey.area | You gave the area itself, $A(3) = 9$. The derivative of the area is not the area. It is how fast the area g... | correct | B9 |
| l5-area-undoes-slope.json | screens[5].explain.text | $A(3) = 9$ is how much area has piled up. $A'(3)$ is how fast it piles up: the edge height $f(3) = 3$. A st... | correct | B9 |
| l5-area-undoes-slope.json | screens[5].explain.canvas.caption | A strip at the edge adds about $f(3) \times 0.25$ | correct | B9 |
| l5-area-undoes-slope.json | screens[6].prose | We now prove $A'(x) = f(x)$ for any continuous $f$. Take $h > 0$; for $h < 0$ the same steps run on the str... | correct | B9 |
| l5-area-undoes-slope.json | screens[6].question | Put the lines in order. | correct | B9 |
| l5-area-undoes-slope.json | screens[6].widget.answer | graded key (order): ["strip", "bound", "divide", "limit"] | correct | B9 |
| l5-area-undoes-slope.json | screens[6].widget.answer.order | graded order of 4 lines; each line follows from the one above | correct | B9 |
| l5-area-undoes-slope.json | screens[6].widget.lines[0].text | $A(x + h) - A(x) = \int_x^{x+h} f(t)\,dt$, since the two regions differ only by the strip | correct | B9 |
| l5-area-undoes-slope.json | screens[6].widget.lines[1].text | $m\,h \le \int_x^{x+h} f(t)\,dt \le M\,h$, since the strip sits between two rectangles of width $h$ | correct | B9 |
| l5-area-undoes-slope.json | screens[6].widget.lines[2].text | $m \le \dfrac{A(x + h) - A(x)}{h} \le M$, dividing through by $h > 0$ | correct | B9 |
| l5-area-undoes-slope.json | screens[6].widget.lines[3].text | As $h \to 0$, $m$ and $M$ both tend to $f(x)$ because $f$ is continuous, so $A'(x) = f(x)$ | correct | B9 |
| l5-area-undoes-slope.json | screens[6].hints[0].text | Start with what the difference $A(x + h) - A(x)$ is. | correct | B9 |
| l5-area-undoes-slope.json | screens[6].hints[1].text | Bound the strip before you divide by $h$. | correct | B9 |
| l5-area-undoes-slope.json | screens[6].hints[2].text | Strip, bound it between two rectangles, divide by $h$, then let $h \to 0$. | correct | B9 |
| l5-area-undoes-slope.json | screens[6].feedback.correct | Each line follows from the one above. | correct | B9 |
| l5-area-undoes-slope.json | screens[6].feedback.generic | Not quite right. Name the strip, bound it, divide by $h$, and only then take the limit. | correct | B9 |
| l5-area-undoes-slope.json | screens[6].feedback.byKey.bound | The bounds are on the strip, so the strip must be named first. | correct | B9 |
| l5-area-undoes-slope.json | screens[6].feedback.byKey.divide | Dividing by $h$ turns the bounds on the strip into bounds on the ratio. The bounds come first. | correct | B9 |
| l5-area-undoes-slope.json | screens[6].feedback.byKey.limit | The limit is the last step: it needs the ratio trapped between $m$ and $M$. | correct | B9 |
| l5-area-undoes-slope.json | screens[6].explain.text | The strip is squeezed between rectangles of heights $m$ and $M$. Dividing by $h$ squeezes the ratio between... | correct | B9 |
| l5-area-undoes-slope.json | screens[7].prose | You found that the area function's slope is the curve's height. This is the **fundamental theorem of calcul... | correct | B9 |
| l5-area-undoes-slope.json | screens[7].question | Let $B(x) = \int_1^x f(t)\,dt$ for the same $f$, starting at 1 instead of 0. How does $B'(x)$ compare with ... | correct | B9 |
| l5-area-undoes-slope.json | screens[7].widget.options[0] | graded key (choice): They are equal: both are $f(x)$ | correct | B9 |
| l5-area-undoes-slope.json | screens[7].widget.options[1].text | wrong option, wrong under every convention: $B'(x) = A'(x) - A(1)$ | correct | B9 |
| l5-area-undoes-slope.json | screens[7].widget.options[1].why | You shifted the derivative. $B(x) = A(x) - A(1)$, and the constant $A(1)$ has derivative 0. | correct | B9 |
| l5-area-undoes-slope.json | screens[7].widget.options[2].text | wrong option, wrong under every convention: $B'(x)$ is smaller, since $B$ covers less area | correct | B9 |
| l5-area-undoes-slope.json | screens[7].widget.options[2].why | $B$ is smaller by a fixed amount, $A(1)$. A fixed gap does not change the slope. | correct | B9 |
| l5-area-undoes-slope.json | screens[7].feedback.correct | $B(x) = A(x) - A(1)$, and a constant gap has slope 0. | correct | B9 |
| l5-area-undoes-slope.json | screens[7].feedback.generic | Not quite right. Compare the two graphs: is the gap between them growing? | correct | B9 |
| l5-area-undoes-slope.json | screens[7].explain.text | $B(x) = A(x) - A(1)$: the same area minus the fixed piece from 0 to 1. On the graph $B$ is $A$ shifted down... | correct | B9 |
| l5-area-undoes-slope.json | screens[8].prose | A desk's P&L rate falls steadily through the day: $r(t) = 4 - t$, in £k per hour, $t$ hours after 8 am. Its... | correct | B9 |
| l5-area-undoes-slope.json | screens[8].question | When during the day is cumulative P&L at its highest? | correct | B9 |
| l5-area-undoes-slope.json | screens[8].widget.options[0].text | wrong option, wrong under every convention: At 8 am, when the rate is highest | correct | B9 |
| l5-area-undoes-slope.json | screens[8].widget.options[0].why | You picked the highest rate. While the rate stays positive, every hour still adds P&L, so the total keeps c... | correct | B9 |
| l5-area-undoes-slope.json | screens[8].widget.options[1] | graded key (choice): At noon, when the rate crosses zero | correct | B9 |
| l5-area-undoes-slope.json | screens[8].widget.options[2].text | wrong option, wrong under every convention: At 4 pm, at the end of the day | correct | B9 |
| l5-area-undoes-slope.json | screens[8].widget.options[2].why | You assumed a running total only grows. After noon the rate is negative, so each hour takes P&L away. | correct | B9 |
| l5-area-undoes-slope.json | screens[8].hints[0].text | $C'(x) = r(x)$. When does $C$ stop rising? | correct | B9 |
| l5-area-undoes-slope.json | screens[8].hints[1].text | The rate crosses zero at $t = 4$. | correct | B9 |
| l5-area-undoes-slope.json | screens[8].hints[2].text | Before $t = 4$, $C' > 0$ and $C$ rises. After it, $C' < 0$ and $C$ falls. So the peak is at $t = 4$, noon. | correct | B9 |
| l5-area-undoes-slope.json | screens[8].feedback.correct | $C$ rises while $r > 0$ and falls once $r < 0$, so it peaks at noon. | correct | B9 |
| l5-area-undoes-slope.json | screens[8].feedback.generic | Not quite right. Ask when the rate of change of $C$, which is $r$, turns negative. | correct | B9 |
| l5-area-undoes-slope.json | screens[8].explain.text | Cumulative P&L rises while the rate is positive and falls once it turns negative. At noon $C(4) = 16 - 8 = ... | correct | B9 |
| l5-area-undoes-slope.json | screens[8].explain.canvas.caption | Peak at noon: $C(4) = 8$, in £k | correct | B9 |
| l5-area-undoes-slope.json | summary.ideas[0] | The accumulation function $A(x) = \int_a^x f(t)\,dt$ is the signed area from $a$ up to a moving edge $x$. | correct | B9 |
| l5-area-undoes-slope.json | summary.ideas[1] | Moving the edge by $h$ adds a strip of area about $f(x)\,h$, so $A$ grows at rate $f(x)$. | correct | B9 |
| l5-area-undoes-slope.json | summary.ideas[2] | Where $f$ is negative, $A$ falls. $A$ peaks where $f$ crosses from positive to negative. | correct | B9 |
| l5-area-undoes-slope.json | summary.formula.name | Fundamental theorem (first form) | correct | B9 |
| l5-area-undoes-slope.json | summary.formula.tex | \dfrac{d}{dx}\int_a^x f(t)\,dt = f(x) | correct | B9 |
| l5-area-undoes-slope.json | summary.formula.note | For continuous $f$. The start $a$ does not change the derivative. | correct | B9 |
| l5-area-undoes-slope.json | summary.trap | $A'(x)$ is the edge height $f(x)$, not the area $A(x)$ built up so far. | correct | B9 |
| l5-area-undoes-slope.json | quiz[0].prose | Let $A(x) = \int_0^x f(t)\,dt$. You know $f(5) = 7$ and $A(5) = 20$. | correct | B9 |
| l5-area-undoes-slope.json | quiz[0].question | What is $A'(5)$? | correct | B9 |
| l5-area-undoes-slope.json | quiz[0].widget.answer | graded key (numeric): 7 | correct | B9 |
| l5-area-undoes-slope.json | quiz[0].widget.wrong[0] | slip area = 20 is the value of the named mistake and is not a correct answer | correct | B9 |
| l5-area-undoes-slope.json | quiz[0].widget.accept | 7, the height $f(5)$. | correct | B9 |
| l5-area-undoes-slope.json | quiz[0].feedback.correct | $A'(5) = f(5) = 7$. | correct | B9 |
| l5-area-undoes-slope.json | quiz[0].feedback.generic | Not quite right. The derivative of the accumulated area is the height at the edge. | correct | B9 |
| l5-area-undoes-slope.json | quiz[0].feedback.byKey.area | 20 is the area so far. Its rate of growth is the edge height $f(5)$. | correct | B9 |
| l5-area-undoes-slope.json | quiz[0].explain.text | By the fundamental theorem, $A'(x) = f(x)$, so $A'(5) = f(5) = 7$. The value $A(5) = 20$ says how much has ... | correct | B9 |
| l5-area-undoes-slope.json | quiz[1].prose | Let $G(x) = \int_1^x e^{t^2}\,dt$. No elementary formula exists for this area. | correct | B9 |
| l5-area-undoes-slope.json | quiz[1].question | What is $G'(x)$? | correct | B9 |
| l5-area-undoes-slope.json | quiz[1].widget.options[0] | graded key (choice): $e^{x^2}$ | correct | B9 |
| l5-area-undoes-slope.json | quiz[1].widget.options[1].text | wrong option, wrong under every convention: $e^{x^2} - e$ | correct | B9 |
| l5-area-undoes-slope.json | quiz[1].widget.options[1].why | You subtracted the integrand's value at the lower limit. That evaluates an integral; it does not differenti... | correct | B9 |
| l5-area-undoes-slope.json | quiz[1].widget.options[2].text | wrong option, wrong under every convention: $2x\,e^{x^2}$ | correct | B9 |
| l5-area-undoes-slope.json | quiz[1].widget.options[2].why | You differentiated the integrand. The theorem hands back $f$ itself. | correct | B9 |
| l5-area-undoes-slope.json | quiz[1].widget.options[3].text | wrong option, wrong under every convention: $\dfrac{e^{x^2}}{2x}$ | correct | B9 |
| l5-area-undoes-slope.json | quiz[1].widget.options[3].why | You tried to integrate the integrand. No antiderivative is needed: the theorem gives $f(x)$ directly. | correct | B9 |
| l5-area-undoes-slope.json | quiz[1].feedback.correct | $G'(x) = e^{x^2}$, even though $G$ has no elementary formula. | correct | B9 |
| l5-area-undoes-slope.json | quiz[1].feedback.generic | Not quite right. Apply $\tfrac{d}{dx}\int_a^x f(t)\,dt = f(x)$ directly. | correct | B9 |
| l5-area-undoes-slope.json | quiz[1].explain.text | The theorem needs only a continuous integrand: $G'(x) = e^{x^2}$. We never need a formula for $G$ itself. T... | correct | B9 |
| l5-area-undoes-slope.json | quiz[2].prose | A continuous $f(t)$ is positive for $0 < t < 3$ and negative for $t > 3$. Let $A(x) = \int_0^x f(t)\,dt$. | correct | B9 |
| l5-area-undoes-slope.json | quiz[2].question | For $x \ge 0$, where does $A(x)$ reach its maximum? | correct | B9 |
| l5-area-undoes-slope.json | quiz[2].widget.options[0] | graded key (choice): At $x = 3$ | correct | B9 |
| l5-area-undoes-slope.json | quiz[2].widget.options[1].text | wrong option, wrong under every convention: At $x = 0$ | correct | B9 |
| l5-area-undoes-slope.json | quiz[2].widget.options[1].why | At 0 no area has built up yet. $A$ rises while $f$ is positive. | correct | B9 |
| l5-area-undoes-slope.json | quiz[2].widget.options[2].text | wrong option, wrong under every convention: Where $f$ is largest | correct | B9 |
| l5-area-undoes-slope.json | quiz[2].widget.options[2].why | There $A$ grows fastest, but it keeps growing until $f$ turns negative. | correct | B9 |
| l5-area-undoes-slope.json | quiz[2].widget.options[3].text | wrong option, wrong under every convention: It keeps growing for ever | correct | B9 |
| l5-area-undoes-slope.json | quiz[2].widget.options[3].why | Past 3 the strips lie below the axis, so $A$ falls. | correct | B9 |
| l5-area-undoes-slope.json | quiz[2].feedback.correct | $A' = f$ is positive before 3 and negative after, so $A$ peaks at 3. | correct | B9 |
| l5-area-undoes-slope.json | quiz[2].feedback.generic | Not quite right. Ask where $A' = f$ changes sign. | correct | B9 |
| l5-area-undoes-slope.json | quiz[2].explain.text | $A'(x) = f(x)$ is positive up to 3, so $A$ rises. After 3 it is negative, so $A$ falls. The maximum is at $... | correct | B9 |
| l5-area-undoes-slope.json | quiz[3].prose | A strategy's P&L rate is $r(t) = 6 - 2t$, in £k per hour. Cumulative P&L is $C(x) = \int_0^x r(t)\,dt$. | correct | B9 |
| l5-area-undoes-slope.json | quiz[3].question | At $x = 5$, how fast is cumulative P&L changing, in £k per hour? | correct | B9 |
| l5-area-undoes-slope.json | quiz[3].widget.answer | graded key (numeric): -4 | correct | B9 |
| l5-area-undoes-slope.json | quiz[3].widget.wrong[0] | slip level = 5 is the value of the named mistake and is not a correct answer | correct | B9 |
| l5-area-undoes-slope.json | quiz[3].widget.wrong[1] | slip sign = 4 is the value of the named mistake and is not a correct answer | correct | B9 |
| l5-area-undoes-slope.json | quiz[3].widget.accept | $-4$: falling at £4k per hour. | correct | B9 |
| l5-area-undoes-slope.json | quiz[3].feedback.correct | $C'(5) = r(5) = 6 - 10 = -4$. | correct | B9 |
| l5-area-undoes-slope.json | quiz[3].feedback.generic | Not quite right. $C'(x) = r(x)$. | correct | B9 |
| l5-area-undoes-slope.json | quiz[3].feedback.byKey.level | 5 is the cumulative P&L $C(5) = 30 - 25$. Its rate of change is $r(5)$. | correct | B9 |
| l5-area-undoes-slope.json | quiz[3].feedback.byKey.sign | $r(5) = 6 - 10 = -4$: negative, so cumulative P&L is falling. | correct | B9 |
| l5-area-undoes-slope.json | quiz[3].explain.text | $C'(x) = r(x)$, so $C'(5) = 6 - 2 \times 5 = -4$. Cumulative P&L is still £5k up, but it is falling at £4k ... | correct | B9 |
| l6-working-backwards.json | screens[0].prose | We want a function $F$ whose slope at every $x$ is $2x$. Try $F(x) = ax^2$. Drag P along the curve to read ... | correct | B10 |
| l6-working-backwards.json | screens[0].canvas.params.functions[0].label | $F(x) = ax^2$ | correct | B10 |
| l6-working-backwards.json | screens[0].canvas.derive.caption | At P, $x$ = {{fixed(P.x, 1)}}: slope of $F$ = {{fixed(2*a*P.x, 2)}}, target $2x$ = {{fixed(2*P.x, 2)}} | correct | B10 |
| l6-working-backwards.json | screens[0].question | Which $a$ makes the slope of $F$ equal $2x$ at every $x$? | correct | B10 |
| l6-working-backwards.json | screens[0].widget.answer | graded key (slider): 1 | correct | B10 |
| l6-working-backwards.json | screens[0].widget.wrong[0] | slip two = 2 is the value of the named mistake and is not a correct answer | correct | B10 |
| l6-working-backwards.json | screens[0].widget.wrong[1] | slip half = 0.5 is the value of the named mistake and is not a correct answer | correct | B10 |
| l6-working-backwards.json | screens[0].hints[0].text | Put P at $x = 1$. The target slope there is 2. | correct | B10 |
| l6-working-backwards.json | screens[0].hints[1].text | The slope of $ax^2$ is $2ax$. | correct | B10 |
| l6-working-backwards.json | screens[0].hints[2].text | $2ax = 2x$ at every $x$ needs $a = 1$. | correct | B10 |
| l6-working-backwards.json | screens[0].feedback.correct | $F(x) = x^2$ has slope $2x$ everywhere. | correct | B10 |
| l6-working-backwards.json | screens[0].feedback.generic | Not quite right. Compare the slope with the target $2x$ at two or three points. | correct | B10 |
| l6-working-backwards.json | screens[0].feedback.byKey.two | With $a = 2$ the slope is $4x$, double the target. You matched the 2 in $2x$, but differentiating brings do... | correct | B10 |
| l6-working-backwards.json | screens[0].feedback.byKey.half | With $a = 0.5$ the slope is $x$, half the target. | correct | B10 |
| l6-working-backwards.json | screens[0].explain.text | With $a = 1$ the slope at every P matches $2x$. We ran differentiation backwards: from the slope $2x$ we re... | correct | B10 |
| l6-working-backwards.json | screens[1].prose | Now the target slope is $x^3$. Try $F(x) = ax^4$. | correct | B10 |
| l6-working-backwards.json | screens[1].canvas.params.functions[0].label | $F(x) = ax^4$ | correct | B10 |
| l6-working-backwards.json | screens[1].canvas.derive.caption | At P, $x$ = {{fixed(P.x, 2)}}: slope of $F$ = {{fixed(4*a*pow(P.x, 3), 2)}}, target $x^3$ = {{fixed(pow(P.x... | correct | B10 |
| l6-working-backwards.json | screens[1].question | Which $a$ makes the slope of $F$ equal $x^3$ at every $x$? | correct | B10 |
| l6-working-backwards.json | screens[1].widget.answer | graded key (slider): 0.25 | correct | B10 |
| l6-working-backwards.json | screens[1].widget.wrong[0] | slip third = 0.3 is the value of the named mistake and is not a correct answer | correct | B10 |
| l6-working-backwards.json | screens[1].widget.wrong[1] | slip one = 1 is the value of the named mistake and is not a correct answer | correct | B10 |
| l6-working-backwards.json | screens[1].hints[0].text | The slope of $ax^4$ is $4ax^3$. | correct | B10 |
| l6-working-backwards.json | screens[1].hints[1].text | At $x = 1$ the target slope is 1. | correct | B10 |
| l6-working-backwards.json | screens[1].hints[2].text | $4ax^3 = x^3$ needs $4a = 1$, so $a = 0.25$. | correct | B10 |
| l6-working-backwards.json | screens[1].feedback.correct | $\tfrac{1}{4}x^4$ has slope $x^3$. | correct | B10 |
| l6-working-backwards.json | screens[1].feedback.generic | Not quite right. Differentiate $ax^4$ and match it to $x^3$. | correct | B10 |
| l6-working-backwards.json | screens[1].feedback.byKey.third | You divided by 3, the old power. Differentiating $x^4$ brings down a 4, so divide by 4. | correct | B10 |
| l6-working-backwards.json | screens[1].feedback.byKey.one | With $a = 1$ the slope is $4x^3$, four times too big. | correct | B10 |
| l6-working-backwards.json | screens[1].explain.text | Differentiating $x^4$ brings down a 4, so we divide by 4 to cancel it: $F(x) = \tfrac{x^4}{4}$. The pattern... | correct | B10 |
| l6-working-backwards.json | screens[2].prose | $x^2$ has slope $2x$. So does $x^2 + C$ for any constant $C$. Slide $C$ and watch the slope at P. | correct | B10 |
| l6-working-backwards.json | screens[2].canvas.params.functions[2].label | $x^2 + C$ | correct | B10 |
| l6-working-backwards.json | screens[2].canvas.derive.caption | $C$ = {{fixed(C, 1)}}: slope at P = {{fixed(2*P.x, 2)}} | correct | B10 |
| l6-working-backwards.json | screens[2].question | As you slide $C$, what happens to the slope at P? | correct | B10 |
| l6-working-backwards.json | screens[2].widget.options[0] | graded key (choice): It stays the same: the curve only moves up or down | correct | B10 |
| l6-working-backwards.json | screens[2].widget.options[1].text | wrong option, wrong under every convention: It grows as $C$ grows | correct | B10 |
| l6-working-backwards.json | screens[2].widget.options[1].why | You watched P rise. The slope label reads the same at every $C$, because the whole curve shifts up rigidly. | correct | B10 |
| l6-working-backwards.json | screens[2].widget.options[2].text | wrong option, wrong under every convention: It turns negative when $C$ is negative | correct | B10 |
| l6-working-backwards.json | screens[2].widget.options[2].why | A negative $C$ lowers the curve but keeps its shape, so the slope at P keeps its sign. | correct | B10 |
| l6-working-backwards.json | screens[2].hints[0].text | Fix P at $x = 1$ and move only $C$. | correct | B10 |
| l6-working-backwards.json | screens[2].hints[1].text | Read the slope label at $C = -3$ and at $C = 3$. | correct | B10 |
| l6-working-backwards.json | screens[2].hints[2].text | The slope reads 2.00 at every $C$: shifting the curve does not tilt it. | correct | B10 |
| l6-working-backwards.json | screens[2].feedback.correct | A constant shifts the curve without tilting it. | correct | B10 |
| l6-working-backwards.json | screens[2].feedback.generic | Not quite right. Keep P still and read the slope at several values of $C$. | correct | B10 |
| l6-working-backwards.json | screens[2].explain.text | Shifting a curve up or down leaves every slope unchanged, since a constant has derivative 0. So $2x$ has a ... | correct | B10 |
| l6-working-backwards.json | screens[3].prose | Raise the power by one, then divide by the new power. Check your answer by differentiating it. | correct | B10 |
| l6-working-backwards.json | screens[3].canvas.params.functions[0].label | $x^4$ | correct | B10 |
| l6-working-backwards.json | screens[3].question | Find $\int x^4\,dx$. Leave out the $+C$. | correct | B10 |
| l6-working-backwards.json | screens[3].widget.answer | graded key (expression): "\\frac{x^5}{5}" | correct | B10 |
| l6-working-backwards.json | screens[3].widget.wrong[0] | slip old-power = "\\frac{x^5}{4}" is the value of the named mistake and is not a correct answer | correct | B10 |
| l6-working-backwards.json | screens[3].widget.wrong[1] | slip no-divide = "x^5" is the value of the named mistake and is not a correct answer | correct | B10 |
| l6-working-backwards.json | screens[3].widget.wrong[2] | slip derivative = "4x^3" is the value of the named mistake and is not a correct answer | correct | B10 |
| l6-working-backwards.json | screens[3].hints[0].text | What power must $F$ have, if differentiating lowers it to 4? | correct | B10 |
| l6-working-backwards.json | screens[3].hints[1].text | Try $x^5$: its derivative is $5x^4$. | correct | B10 |
| l6-working-backwards.json | screens[3].hints[2].text | $5x^4$ is five times too big, so take $\tfrac{x^5}{5}$. | correct | B10 |
| l6-working-backwards.json | screens[3].feedback.correct | $\left(\tfrac{x^5}{5}\right)' = x^4$. | correct | B10 |
| l6-working-backwards.json | screens[3].feedback.generic | Not quite right. Raise the power to 5, divide by 5, then differentiate to check. | correct | B10 |
| l6-working-backwards.json | screens[3].feedback.byKey.old-power | You divided by 4, the old power. Differentiate $\tfrac{x^5}{4}$: you get $\tfrac{5}{4}x^4$, too big. Divide... | correct | B10 |
| l6-working-backwards.json | screens[3].feedback.byKey.no-divide | The derivative of $x^5$ is $5x^4$, five times too big. Divide by 5. | correct | B10 |
| l6-working-backwards.json | screens[3].feedback.byKey.derivative | You differentiated $x^4$. We want the function whose derivative is $x^4$. | correct | B10 |
| l6-working-backwards.json | screens[3].explain.text | Differentiating $\tfrac{x^5}{5}$ gives $\tfrac{5x^4}{5} = x^4$. So $\int x^4\,dx = \tfrac{x^5}{5} + C$. The... | correct | B10 |
| l6-working-backwards.json | screens[3].explain.canvas.functions[0].label | $\frac{x^5}{5}$ | correct | B10 |
| l6-working-backwards.json | screens[4].prose | At $n = -1$ the power rule gives $\dfrac{x^0}{0}$, which is meaningless. We need another function with slop... | correct | B10 |
| l6-working-backwards.json | screens[4].canvas.derive.caption | At P, $x$ = {{fixed(P.x, 2)}}: $\tfrac{1}{x}$ = {{fixed(1/P.x, 3)}} | correct | B10 |
| l6-working-backwards.json | screens[4].question | Which function is an antiderivative of $\dfrac{1}{x}$ for $x > 0$? | correct | B10 |
| l6-working-backwards.json | screens[4].widget.options[0] | graded key (choice): $\ln x$ | correct | B10 |
| l6-working-backwards.json | screens[4].widget.options[1].text | wrong option, wrong under every convention: $\dfrac{x^0}{0}$ | correct | B10 |
| l6-working-backwards.json | screens[4].widget.options[1].why | You applied the power rule at $n = -1$. That divides by zero, so it names no function. | correct | B10 |
| l6-working-backwards.json | screens[4].widget.options[2].text | wrong option, wrong under every convention: $-\dfrac{1}{x^2}$ | correct | B10 |
| l6-working-backwards.json | screens[4].widget.options[2].why | That is the derivative of $\tfrac{1}{x}$. We want the function whose derivative is $\tfrac{1}{x}$. | correct | B10 |
| l6-working-backwards.json | screens[4].widget.options[3].text | wrong option, wrong under every convention: $\dfrac{x^{-2}}{-2}$ | correct | B10 |
| l6-working-backwards.json | screens[4].widget.options[3].why | You lowered the power instead of raising it. Its derivative is $x^{-3}$, not $x^{-1}$. | correct | B10 |
| l6-working-backwards.json | screens[4].hints[0].text | Drag P and compare the slope label with $\tfrac{1}{x}$ in the caption. | correct | B10 |
| l6-working-backwards.json | screens[4].hints[1].text | At $x = 2$ the slope of $\ln x$ is 0.5. | correct | B10 |
| l6-working-backwards.json | screens[4].hints[2].text | The derivative of $\ln x$ is $\tfrac{1}{x}$, so $\ln x$ is an antiderivative. | correct | B10 |
| l6-working-backwards.json | screens[4].feedback.correct | $(\ln x)' = \tfrac{1}{x}$, so $\ln x$ fills the gap at $n = -1$. | correct | B10 |
| l6-working-backwards.json | screens[4].feedback.generic | Not quite right. Read the slope of $\ln x$ at a few points and compare it with $\tfrac{1}{x}$. | correct | B10 |
| l6-working-backwards.json | screens[4].explain.text | $\ln x$ has slope $\tfrac{1}{x}$ at every $x > 0$. For $x < 0$, $\ln(-x)$ has slope $\tfrac{-1}{-x} = \tfra... | correct | B10 |
| l6-working-backwards.json | screens[5].prose | The graph shows $\sin x$ and $\cos x$. Drag P along $\cos x$ and compare its slope with $\sin x$. | correct | B10 |
| l6-working-backwards.json | screens[5].canvas.derive.caption | At P, $x$ = {{fixed(P.x, 2)}}: $\sin x$ = {{fixed(sin(P.x), 2)}} | correct | B10 |
| l6-working-backwards.json | screens[5].question | What is $\int \sin x\,dx$? | correct | B10 |
| l6-working-backwards.json | screens[5].widget.options[0] | graded key (choice): $-\cos x + C$ | correct | B10 |
| l6-working-backwards.json | screens[5].widget.options[1].text | wrong option, wrong under every convention: $\cos x + C$ | correct | B10 |
| l6-working-backwards.json | screens[5].widget.options[1].why | The slope of $\cos x$ is $-\sin x$: the label and the caption have opposite signs. So $\cos x$ gives the wr... | correct | B10 |
| l6-working-backwards.json | screens[5].widget.options[2].text | wrong option, wrong under every convention: $\dfrac{\sin^2 x}{2} + C$ | correct | B10 |
| l6-working-backwards.json | screens[5].widget.options[2].why | You treated $\sin x$ like a power of $x$. The power rule works on $x^n$ only. | correct | B10 |
| l6-working-backwards.json | screens[5].widget.options[3].text | wrong option, wrong under every convention: $-\sin x + C$ | correct | B10 |
| l6-working-backwards.json | screens[5].widget.options[3].why | Its slope is $-\cos x$, not $\sin x$. Differentiate your answer to check. | correct | B10 |
| l6-working-backwards.json | screens[5].hints[0].text | Compare the slope label with the caption at a few points. | correct | B10 |
| l6-working-backwards.json | screens[5].hints[1].text | The slope of $\cos x$ is always $-\sin x$. | correct | B10 |
| l6-working-backwards.json | screens[5].hints[2].text | So the slope of $-\cos x$ is $\sin x$. | correct | B10 |
| l6-working-backwards.json | screens[5].feedback.correct | $(-\cos x)' = \sin x$. | correct | B10 |
| l6-working-backwards.json | screens[5].feedback.generic | Not quite right. Differentiate each option and see which gives $\sin x$. | correct | B10 |
| l6-working-backwards.json | screens[5].explain.text | At every P the slope of $\cos x$ was minus the value of $\sin x$. Flipping the sign, $(-\cos x)' = \sin x$.... | correct | B10 |
| l6-working-backwards.json | screens[6].prose | Since $(e^x)' = e^x$, it is tempting to write $\int e^{2x}\,dx = e^{2x} + C$. The graph shows $e^{2x}$. Dra... | correct | B10 |
| l6-working-backwards.json | screens[6].canvas.params.functions[0].label | $e^{2x}$ | correct | B10 |
| l6-working-backwards.json | screens[6].canvas.derive.caption | At P: height {{fixed(exp(2*P.x), 2)}}, slope {{fixed(2*exp(2*P.x), 2)}} | correct | B10 |
| l6-working-backwards.json | screens[6].question | Find $\int e^{2x}\,dx$. Leave out the $+C$. | correct | B10 |
| l6-working-backwards.json | screens[6].widget.answer | graded key (expression): "\\frac{e^{2x}}{2}" | correct | B10 |
| l6-working-backwards.json | screens[6].widget.wrong[0] | slip copy = "e^{2x}" is the value of the named mistake and is not a correct answer | correct | B10 |
| l6-working-backwards.json | screens[6].widget.wrong[1] | slip times-two = "2e^{2x}" is the value of the named mistake and is not a correct answer | correct | B10 |
| l6-working-backwards.json | screens[6].widget.wrong[2] | slip power-rule = "\\frac{e^{2x+1}}{2x+1}" is the value of the named mistake and is not a correct answer | correct | B10 |
| l6-working-backwards.json | screens[6].hints[0].text | Differentiate $e^{2x}$. What extra factor does the chain rule bring out? | correct | B10 |
| l6-working-backwards.json | screens[6].hints[1].text | The slope of $e^{2x}$ is twice its height. | correct | B10 |
| l6-working-backwards.json | screens[6].hints[2].text | $(e^{2x})' = 2e^{2x}$, so $\tfrac{1}{2}e^{2x}$ has derivative $e^{2x}$. | correct | B10 |
| l6-working-backwards.json | screens[6].feedback.correct | $\left(\tfrac{1}{2}e^{2x}\right)' = \tfrac{1}{2} \cdot 2e^{2x} = e^{2x}$. | correct | B10 |
| l6-working-backwards.json | screens[6].feedback.generic | Not quite right. Differentiate your answer: you should get exactly $e^{2x}$. | correct | B10 |
| l6-working-backwards.json | screens[6].feedback.byKey.copy | You copied the rule for $e^x$. The chain rule gives $(e^{2x})' = 2e^{2x}$, twice too big. | correct | B10 |
| l6-working-backwards.json | screens[6].feedback.byKey.times-two | $2e^{2x}$ is the derivative of $e^{2x}$. We want the function whose derivative is $e^{2x}$, so divide by 2. | correct | B10 |
| l6-working-backwards.json | screens[6].feedback.byKey.power-rule | You treated $e^{2x}$ as a power of $x$. Here the variable is in the exponent, so the power rule does not ap... | correct | B10 |
| l6-working-backwards.json | screens[6].explain.text | The caption showed the slope is always twice the height: $(e^{2x})' = 2e^{2x}$. Halving fixes it: $\left(\t... | correct | B10 |
| l6-working-backwards.json | screens[7].prose | Now generalise the fix to $\int e^{kx}\,dx$, for any constant $k \neq 0$. | correct | B10 |
| l6-working-backwards.json | screens[7].question | Put the lines in order. | correct | B10 |
| l6-working-backwards.json | screens[7].widget.answer | graded key (order): ["guess", "fix", "check", "family"] | correct | B10 |
| l6-working-backwards.json | screens[7].widget.answer.order | graded order of 4 lines; each line follows from the one above | correct | B10 |
| l6-working-backwards.json | screens[7].widget.lines[0].text | Guess $F(x) = e^{kx}$: then $F'(x) = k\,e^{kx}$, by the chain rule | correct | B10 |
| l6-working-backwards.json | screens[7].widget.lines[1].text | That is $k$ times too big, so try $F(x) = \dfrac{1}{k}e^{kx}$, which needs $k \neq 0$ | correct | B10 |
| l6-working-backwards.json | screens[7].widget.lines[2].text | $F'(x) = \dfrac{1}{k} \cdot k\,e^{kx} = e^{kx}$, since a constant factor rides through the derivative | correct | B10 |
| l6-working-backwards.json | screens[7].widget.lines[3].text | So $\int e^{kx}\,dx = \dfrac{e^{kx}}{k} + C$, adding the constant for the whole family | correct | B10 |
| l6-working-backwards.json | screens[7].hints[0].text | Start from the natural first guess. | correct | B10 |
| l6-working-backwards.json | screens[7].hints[1].text | The guess is off by a factor. Fix it, then check the fix. | correct | B10 |
| l6-working-backwards.json | screens[7].hints[2].text | Guess $e^{kx}$, divide by $k$, differentiate to check, then add $C$. | correct | B10 |
| l6-working-backwards.json | screens[7].feedback.correct | Guess, fix, check, conclude. | correct | B10 |
| l6-working-backwards.json | screens[7].feedback.generic | Not quite right. The fix comes from what the first guess gets wrong. | correct | B10 |
| l6-working-backwards.json | screens[7].feedback.byKey.fix | You can only see the factor $k$ to divide out after differentiating the first guess. | correct | B10 |
| l6-working-backwards.json | screens[7].feedback.byKey.check | The check differentiates the fixed guess, so the fix must come first. | correct | B10 |
| l6-working-backwards.json | screens[7].feedback.byKey.family | The conclusion comes last, once the check has passed. | correct | B10 |
| l6-working-backwards.json | screens[7].explain.text | Differentiating $e^{kx}$ brings out $k$, so we divide by $k$ and check. With $k = 2$ this gives $\tfrac{1}{... | correct | B10 |
| l6-working-backwards.json | screens[8].prose | Every antiderivative so far came from reading a derivative backwards: $$\int x^n\,dx = \frac{x^{n+1}}{n+1} ... | correct | B10 |
| l6-working-backwards.json | screens[8].question | Match each function to an antiderivative. | correct | B10 |
| l6-working-backwards.json | screens[8].widget.slots | graded matching: {"$\\cos x$": ["t-sin"], "$\\sin x$": ["t-negcos"], "$\\frac{1}{x}$": ["t-ln"], "$e^{3x}$"... | correct | B10 |
| l6-working-backwards.json | screens[8].feedback.correct | Each antiderivative differentiates back to its function. | correct | B10 |
| l6-working-backwards.json | screens[8].feedback.generic | Not quite right. Differentiate each token you placed and compare. | correct | B10 |
| l6-working-backwards.json | screens[8].feedback.byKey.d-cos | $\cos x$ differentiates to $-\sin x$, so it fits no slot. $\sin x$ needs $-\cos x$. | correct | B10 |
| l6-working-backwards.json | screens[8].feedback.byKey.d-3exp | $3e^{3x}$ is the derivative of $e^{3x}$, not an antiderivative. Divide by 3 instead. | correct | B10 |
| l6-working-backwards.json | screens[8].feedback.byKey.d-sq | $-\tfrac{1}{x^2}$ is the derivative of $\tfrac{1}{x}$. Its antiderivative is $\ln\|x\|$. | correct | B10 |
| l6-working-backwards.json | screens[8].explain.text | Each pair is a derivative fact read backwards: $(\sin x)' = \cos x$, $(-\cos x)' = \sin x$, $(\ln\|x\|)' = ... | correct | B10 |
| l6-working-backwards.json | screens[9].prose | A desk carries £2k of P&L into the session. Its P&L rate is $r(t) = 3 - \tfrac{t}{2}$, in £k per hour, $t$ ... | correct | B10 |
| l6-working-backwards.json | screens[9].canvas.params.functions[0].label | $C = 0$ | correct | B10 |
| l6-working-backwards.json | screens[9].canvas.params.functions[1].label | $C = 4$ | correct | B10 |
| l6-working-backwards.json | screens[9].canvas.state.caption | Dashed: $3t - \tfrac{t^2}{4} + C$ for $C = 0$ and $C = 4$. Dot: the start, $P(0) = 2$. | correct | B10 |
| l6-working-backwards.json | screens[9].question | What is $P(4)$, in £k? | correct | B10 |
| l6-working-backwards.json | screens[9].widget.answer | graded key (numeric): 10 | correct | B10 |
| l6-working-backwards.json | screens[9].widget.wrong[0] | slip no-c = 8 is the value of the named mistake and is not a correct answer | correct | B10 |
| l6-working-backwards.json | screens[9].widget.wrong[1] | slip rate = 1 is the value of the named mistake and is not a correct answer | correct | B10 |
| l6-working-backwards.json | screens[9].widget.wrong[2] | slip no-divide = 6 is the value of the named mistake and is not a correct answer | correct | B10 |
| l6-working-backwards.json | screens[9].widget.accept | 10: $P(t) = 3t - \tfrac{t^2}{4} + 2$. | correct | B10 |
| l6-working-backwards.json | screens[9].hints[0].text | Find an antiderivative of $3 - \tfrac{t}{2}$, then fix $C$ with $P(0) = 2$. | correct | B10 |
| l6-working-backwards.json | screens[9].hints[1].text | $P(t) = 3t - \tfrac{t^2}{4} + C$. | correct | B10 |
| l6-working-backwards.json | screens[9].hints[2].text | $P(0) = C = 2$, so $P(4) = 12 - 4 + 2$. | correct | B10 |
| l6-working-backwards.json | screens[9].feedback.correct | $P(4) = 12 - 4 + 2 = 10$, so £10k. | correct | B10 |
| l6-working-backwards.json | screens[9].feedback.generic | Not quite right. Integrate the rate, then use $P(0) = 2$ to fix the constant. | correct | B10 |
| l6-working-backwards.json | screens[9].feedback.byKey.no-c | You left out the constant. $P(0) = 2$ fixes $C = 2$, the P&L carried in. | correct | B10 |
| l6-working-backwards.json | screens[9].feedback.byKey.rate | 1 is the rate $r(4)$, in £k per hour. We want the P&L itself. | correct | B10 |
| l6-working-backwards.json | screens[9].feedback.byKey.no-divide | You integrated $\tfrac{t}{2}$ as $\tfrac{t^2}{2}$. Raising the power gives $t^2$, divided by 2 twice: $\tfr... | correct | B10 |
| l6-working-backwards.json | screens[9].explain.text | The antiderivatives $3t - \tfrac{t^2}{4} + C$ form a family of curves. The carried-in £2k picks the one thr... | correct | B10 |
| l6-working-backwards.json | screens[9].explain.canvas.functions[0].label | $C = 2$ | correct | B10 |
| l6-working-backwards.json | screens[9].explain.canvas.points.T.label | $P(4) = 10$ | correct | B10 |
| l6-working-backwards.json | summary.ideas[0] | An antiderivative of $f$ is any $F$ with $F' = f$: a derivative fact read backwards. | correct | B10 |
| l6-working-backwards.json | summary.ideas[1] | Antiderivatives come as a family $F + C$, because shifting a curve up or down keeps every slope. A starting... | correct | B10 |
| l6-working-backwards.json | summary.ideas[2] | Check every antiderivative by differentiating it. The chain rule is why $\int e^{kx}\,dx = \tfrac{e^{kx}}{k... | correct | B10 |
| l6-working-backwards.json | summary.formula.name | Power rule, backwards | correct | B10 |
| l6-working-backwards.json | summary.formula.tex | \int x^n\,dx = \dfrac{x^{n+1}}{n+1} + C \quad (n \neq -1) | correct | B10 |
| l6-working-backwards.json | summary.formula.note | At $n = -1$ use $\int \tfrac{1}{x}\,dx = \ln\|x\| + C$. | correct | B10 |
| l6-working-backwards.json | summary.trap | Divide by the new power $n + 1$, not the old one. And $\int e^{2x}\,dx$ is $\tfrac{1}{2}e^{2x} + C$, not $e... | correct | B10 |
| l6-working-backwards.json | quiz[0].prose | Use the power rule backwards. | correct | B10 |
| l6-working-backwards.json | quiz[0].question | What is $\int x^{-3}\,dx$? | correct | B10 |
| l6-working-backwards.json | quiz[0].widget.options[0] | graded key (choice): $-\dfrac{1}{2x^2} + C$ | correct | B10 |
| l6-working-backwards.json | quiz[0].widget.options[1].text | wrong option, wrong under every convention: $\dfrac{x^{-4}}{-4} + C$ | correct | B10 |
| l6-working-backwards.json | quiz[0].widget.options[1].why | You lowered the power. Antiderivatives raise it: $-3 + 1 = -2$. | correct | B10 |
| l6-working-backwards.json | quiz[0].widget.options[2].text | wrong option, wrong under every convention: $\dfrac{x^{-2}}{-3} + C$ | correct | B10 |
| l6-working-backwards.json | quiz[0].widget.options[2].why | You divided by the old power, $-3$. Divide by the new power, $-2$. | correct | B10 |
| l6-working-backwards.json | quiz[0].widget.options[3].text | wrong option, wrong under every convention: $\ln\|x^3\| + C$ | correct | B10 |
| l6-working-backwards.json | quiz[0].widget.options[3].why | The log rule is for $x^{-1}$ only. Here $n = -3$, so the power rule works. | correct | B10 |
| l6-working-backwards.json | quiz[0].feedback.correct | $\dfrac{x^{-2}}{-2} = -\dfrac{1}{2x^2}$. | correct | B10 |
| l6-working-backwards.json | quiz[0].feedback.generic | Not quite right. Raise the power by one and divide by the new power. | correct | B10 |
| l6-working-backwards.json | quiz[0].explain.text | Raising $-3$ by one gives $-2$, so $\int x^{-3}\,dx = \tfrac{x^{-2}}{-2} + C = -\tfrac{1}{2x^2} + C$. Check... | correct | B10 |
| l6-working-backwards.json | quiz[1].prose | A continuous discount factor is $e^{-0.04t}$. | correct | B10 |
| l6-working-backwards.json | quiz[1].question | What is $\int e^{-0.04t}\,dt$? | correct | B10 |
| l6-working-backwards.json | quiz[1].widget.options[0] | graded key (choice): $-25e^{-0.04t} + C$ | correct | B10 |
| l6-working-backwards.json | quiz[1].widget.options[1].text | wrong option, wrong under every convention: $25e^{-0.04t} + C$ | correct | B10 |
| l6-working-backwards.json | quiz[1].widget.options[1].why | You divided by 0.04, but $k = -0.04$. The minus sign stays. | correct | B10 |
| l6-working-backwards.json | quiz[1].widget.options[2].text | wrong option, wrong under every convention: $-0.04e^{-0.04t} + C$ | correct | B10 |
| l6-working-backwards.json | quiz[1].widget.options[2].why | You differentiated. Undoing the chain rule divides by $k$; it does not multiply. | correct | B10 |
| l6-working-backwards.json | quiz[1].widget.options[3].text | wrong option, wrong under every convention: $e^{-0.04t} + C$ | correct | B10 |
| l6-working-backwards.json | quiz[1].widget.options[3].why | You copied the rule for $e^x$. The chain rule brings out $-0.04$, which you must divide out. | correct | B10 |
| l6-working-backwards.json | quiz[1].feedback.correct | $\dfrac{e^{-0.04t}}{-0.04} = -25e^{-0.04t}$. | correct | B10 |
| l6-working-backwards.json | quiz[1].feedback.generic | Not quite right. Use $\int e^{kt}\,dt = \tfrac{e^{kt}}{k} + C$ with $k = -0.04$. | correct | B10 |
| l6-working-backwards.json | quiz[1].explain.text | With $k = -0.04$, $\tfrac{1}{k} = -25$, so the antiderivative is $-25e^{-0.04t} + C$. Check: its derivative... | correct | B10 |
| l6-working-backwards.json | quiz[2].prose | A function has $F'(x) = 6x^2$ and $F(1) = 5$. | correct | B10 |
| l6-working-backwards.json | quiz[2].question | What is $F(2)$? | correct | B10 |
| l6-working-backwards.json | quiz[2].widget.answer | graded key (numeric): 19 | correct | B10 |
| l6-working-backwards.json | quiz[2].widget.wrong[0] | slip no-c = 16 is the value of the named mistake and is not a correct answer | correct | B10 |
| l6-working-backwards.json | quiz[2].widget.wrong[1] | slip slope = 24 is the value of the named mistake and is not a correct answer | correct | B10 |
| l6-working-backwards.json | quiz[2].widget.accept | 19: $F(x) = 2x^3 + 3$. | correct | B10 |
| l6-working-backwards.json | quiz[2].feedback.correct | $F(x) = 2x^3 + 3$, so $F(2) = 19$. | correct | B10 |
| l6-working-backwards.json | quiz[2].feedback.generic | Not quite right. Integrate, then use $F(1) = 5$ to find $C$. | correct | B10 |
| l6-working-backwards.json | quiz[2].feedback.byKey.no-c | You left out $C$. $F(1) = 2 + C = 5$ gives $C = 3$. | correct | B10 |
| l6-working-backwards.json | quiz[2].feedback.byKey.slope | 24 is $F'(2)$, the slope. We want the value $F(2)$. | correct | B10 |
| l6-working-backwards.json | quiz[2].explain.text | $F(x) = 2x^3 + C$, and $F(1) = 2 + C = 5$ gives $C = 3$. So $F(2) = 16 + 3 = 19$. | correct | B10 |
| l6-working-backwards.json | quiz[3].prose | On $x > 0$, $\ln x$ is an antiderivative of $\dfrac{1}{x}$. | correct | B10 |
| l6-working-backwards.json | quiz[3].question | What about on $x < 0$? | correct | B10 |
| l6-working-backwards.json | quiz[3].widget.options[0] | graded key (choice): $\ln x$ is undefined there, but $\ln(-x)$ works | correct | B10 |
| l6-working-backwards.json | quiz[3].widget.options[1].text | wrong option, wrong under every convention: $\ln x$ works for every $x \neq 0$ | correct | B10 |
| l6-working-backwards.json | quiz[3].widget.options[1].why | You extended $\ln x$ to negative $x$, where it is not defined. | correct | B10 |
| l6-working-backwards.json | quiz[3].widget.options[2].text | wrong option, wrong under every convention: $\dfrac{1}{x}$ has no antiderivative for $x < 0$ | correct | B10 |
| l6-working-backwards.json | quiz[3].widget.options[2].why | $\ln(-x)$ has derivative $\tfrac{-1}{-x} = \tfrac{1}{x}$, so one exists. | correct | B10 |
| l6-working-backwards.json | quiz[3].feedback.correct | $(\ln(-x))' = \tfrac{1}{x}$ for $x < 0$, hence $\ln\|x\|$. | correct | B10 |
| l6-working-backwards.json | quiz[3].feedback.generic | Not quite right. Differentiate $\ln(-x)$ with the chain rule. | correct | B10 |
| l6-working-backwards.json | quiz[3].explain.text | $\ln x$ needs $x > 0$. For $x < 0$, the chain rule gives $(\ln(-x))' = \tfrac{-1}{-x} = \tfrac{1}{x}$. Both... | correct | B10 |
| l7-evaluating.json | screens[0].prose | The shaded region lies under $f(x) = 2x$ from $x = 1$ to $x = 3$. It is a trapezium, so you can find its ar... | correct | B11 |
| l7-evaluating.json | screens[0].canvas.params.functions[0].label | $f(x) = 2x$ | correct | B11 |
| l7-evaluating.json | screens[0].canvas.state.points[0].label | $(1, 2)$ | correct | B11 |
| l7-evaluating.json | screens[0].canvas.state.points[1].label | $(3, 6)$ | correct | B11 |
| l7-evaluating.json | screens[0].question | What is $\int_1^3 2x\,dx$? | correct | B11 |
| l7-evaluating.json | screens[0].widget.answer | graded key (numeric): 8 | correct | B11 |
| l7-evaluating.json | screens[0].widget.wrong[0] | slip from-zero = 9 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[0].widget.wrong[1] | slip tall-side = 12 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[0].widget.wrong[2] | slip short-side = 4 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[0].widget.accept | 8: the average side, 4, times the width, 2. | correct | B11 |
| l7-evaluating.json | screens[0].hints[0].text | A trapezium's area is the average of its two parallel sides times the width. | correct | B11 |
| l7-evaluating.json | screens[0].hints[1].text | The sides are $f(1) = 2$ and $f(3) = 6$. The width is 2. | correct | B11 |
| l7-evaluating.json | screens[0].hints[2].text | $\tfrac{2 + 6}{2} \times 2 = 8$. | correct | B11 |
| l7-evaluating.json | screens[0].feedback.correct | The average side is 4 and the width is 2, so the area is 8. | correct | B11 |
| l7-evaluating.json | screens[0].feedback.generic | Not quite right. Average the two vertical sides, then multiply by the width. | correct | B11 |
| l7-evaluating.json | screens[0].feedback.byKey.from-zero | 9 is the area from 0 to 3. The region starts at $x = 1$. | correct | B11 |
| l7-evaluating.json | screens[0].feedback.byKey.tall-side | 12 uses the taller side, 6, across the whole width. The top slopes, so average the two sides. | correct | B11 |
| l7-evaluating.json | screens[0].feedback.byKey.short-side | 4 uses the shorter side, 2, across the whole width. Average the two sides instead. | correct | B11 |
| l7-evaluating.json | screens[0].explain.text | The trapezium has sides 2 and 6 and width 2, so its area is $\tfrac{2 + 6}{2} \times 2 = 8$. Notice that $3... | correct | B11 |
| l7-evaluating.json | screens[0].explain.canvas.area.label | 8 | correct | B11 |
| l7-evaluating.json | screens[1].prose | $x^2$ is an antiderivative of $2x$. Drag the two edges, $a$ and $b$, and compare the shaded area with $b^2 ... | correct | B11 |
| l7-evaluating.json | screens[1].canvas.params.functions[0].label | $f(x) = 2x$ | correct | B11 |
| l7-evaluating.json | screens[1].canvas.derive.caption | $a$ = {{fixed(A.x, 2)}}, $b$ = {{fixed(B.x, 2)}}: $b^2 - a^2$ = {{fixed(B.x*B.x - A.x*A.x, 2)}} | correct | B11 |
| l7-evaluating.json | screens[1].question | Try several pairs, including one with $a$ to the right of $b$. What do you notice? | correct | B11 |
| l7-evaluating.json | screens[1].widget.options[0] | graded key (choice): The area always equals $b^2 - a^2$, with a minus sign when $a > b$ | correct | B11 |
| l7-evaluating.json | screens[1].widget.options[1].text | wrong option, wrong under every convention: They agree only when $a = 0$ | correct | B11 |
| l7-evaluating.json | screens[1].widget.options[1].why | Try $a = 1$ and $b = 3$: both read 8. The match does not need $a = 0$. | correct | B11 |
| l7-evaluating.json | screens[1].widget.options[2].text | wrong option, wrong under every convention: $b^2 - a^2$ is double the area | correct | B11 |
| l7-evaluating.json | screens[1].widget.options[2].why | Read both numbers at $a = 1$, $b = 2$: the area is 3, and $4 - 1 = 3$. They are equal. | correct | B11 |
| l7-evaluating.json | screens[1].hints[0].text | Set $a = 1$ and $b = 2$, then read the area label and the caption. | correct | B11 |
| l7-evaluating.json | screens[1].hints[1].text | Now drag $a$ past $b$ and read both again. | correct | B11 |
| l7-evaluating.json | screens[1].hints[2].text | In every case the two numbers agree, sign included. | correct | B11 |
| l7-evaluating.json | screens[1].feedback.correct | Area and $b^2 - a^2$ agree for every pair, sign included. | correct | B11 |
| l7-evaluating.json | screens[1].feedback.generic | Not quite right. Read the area label and the caption for two or three pairs. | correct | B11 |
| l7-evaluating.json | screens[1].explain.text | Every pair gave area $= b^2 - a^2$, and $x^2$ is an antiderivative of $2x$. With $a$ to the right of $b$ bo... | correct | B11 |
| l7-evaluating.json | screens[2].prose | This is the fundamental theorem, second form. If $f$ is continuous on $[a, b]$ and $F' = f$ there, then $$\... | correct | B11 |
| l7-evaluating.json | screens[2].canvas.params.functions[0].label | $3x^2$ | correct | B11 |
| l7-evaluating.json | screens[2].question | Evaluate $\int_1^2 3x^2\,dx$. | correct | B11 |
| l7-evaluating.json | screens[2].widget.answer | graded key (numeric): 7 | correct | B11 |
| l7-evaluating.json | screens[2].widget.wrong[0] | slip forgot-fa = 8 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[2].widget.wrong[1] | slip order = -7 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[2].widget.wrong[2] | slip added = 9 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[2].widget.wrong[3] | slip height = 12 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[2].widget.accept | 7: $\big[x^3\big]_1^2 = 8 - 1$. | correct | B11 |
| l7-evaluating.json | screens[2].hints[0].text | Find an antiderivative $F$ of $3x^2$. | correct | B11 |
| l7-evaluating.json | screens[2].hints[1].text | $F(x) = x^3$. | correct | B11 |
| l7-evaluating.json | screens[2].hints[2].text | $F(2) - F(1) = 8 - 1 = 7$. | correct | B11 |
| l7-evaluating.json | screens[2].feedback.correct | $\big[x^3\big]_1^2 = 8 - 1 = 7$. | correct | B11 |
| l7-evaluating.json | screens[2].feedback.generic | Not quite right. Find $F$ with $F' = 3x^2$, then compute $F(2) - F(1)$. | correct | B11 |
| l7-evaluating.json | screens[2].feedback.byKey.forgot-fa | 8 is $F(2)$ alone. Subtract $F(1) = 1$, the part from 0 to 1. | correct | B11 |
| l7-evaluating.json | screens[2].feedback.byKey.order | You subtracted the wrong way round, $F(1) - F(2)$. It is top limit minus bottom: $F(2) - F(1)$. | correct | B11 |
| l7-evaluating.json | screens[2].feedback.byKey.added | You added $F(2) + F(1)$. The theorem subtracts. | correct | B11 |
| l7-evaluating.json | screens[2].feedback.byKey.height | 12 is $f(2)$, the height at the edge. Find an antiderivative first. | correct | B11 |
| l7-evaluating.json | screens[2].explain.text | $F(x) = x^3$, so $\big[x^3\big]_1^2 = 8 - 1 = 7$. The 8 is the area from 0 to 2. Subtracting 1 removes the ... | correct | B11 |
| l7-evaluating.json | screens[2].explain.canvas.area.label | 7 | correct | B11 |
| l7-evaluating.json | screens[3].prose | One hump of $\sin x$ runs from 0 to $\pi$, above the axis. | correct | B11 |
| l7-evaluating.json | screens[3].question | Evaluate $\int_0^{\pi} \sin x\,dx$. | correct | B11 |
| l7-evaluating.json | screens[3].widget.answer | graded key (numeric): 2 | correct | B11 |
| l7-evaluating.json | screens[3].widget.wrong[0] | slip cos = -2 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[3].widget.wrong[1] | slip cos-pi = 0 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[3].widget.wrong[2] | slip forgot-fa = 1 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[3].widget.accept | 2: $\big[-\cos x\big]_0^{\pi} = 1 - (-1)$. | correct | B11 |
| l7-evaluating.json | screens[3].hints[0].text | An antiderivative of $\sin x$ is $-\cos x$. | correct | B11 |
| l7-evaluating.json | screens[3].hints[1].text | $\cos \pi = -1$ and $\cos 0 = 1$. | correct | B11 |
| l7-evaluating.json | screens[3].hints[2].text | $(-\cos \pi) - (-\cos 0) = 1 + 1 = 2$. | correct | B11 |
| l7-evaluating.json | screens[3].feedback.correct | $\big[-\cos x\big]_0^{\pi} = 1 - (-1) = 2$. | correct | B11 |
| l7-evaluating.json | screens[3].feedback.generic | Not quite right. Use $F(x) = -\cos x$ and keep track of both minus signs. | correct | B11 |
| l7-evaluating.json | screens[3].feedback.byKey.cos | You used $\cos x$ as the antiderivative. Its derivative is $-\sin x$, so use $-\cos x$. | correct | B11 |
| l7-evaluating.json | screens[3].feedback.byKey.cos-pi | You may have used $\cos \pi = 1$. In fact $\cos \pi = -1$. | correct | B11 |
| l7-evaluating.json | screens[3].feedback.byKey.forgot-fa | 1 is $-\cos \pi$ alone. Subtracting $-\cos 0 = -1$ adds another 1. | correct | B11 |
| l7-evaluating.json | screens[3].explain.text | $\big[-\cos x\big]_0^{\pi} = 1 - (-1) = 2$. From $\pi$ to $2\pi$ the hump is below the axis, and the same s... | correct | B11 |
| l7-evaluating.json | screens[3].explain.canvas.area[0].label | +2 | correct | B11 |
| l7-evaluating.json | screens[3].explain.canvas.area[1].label | −2 | correct | B11 |
| l7-evaluating.json | screens[4].prose | Any antiderivative will do. Suppose we evaluate $\int_1^2 3x^2\,dx$ with $F(x) = x^3 + 5$ instead of $x^3$. | correct | B11 |
| l7-evaluating.json | screens[4].canvas.params.functions[0].label | $x^3$ | correct | B11 |
| l7-evaluating.json | screens[4].canvas.params.functions[1].label | $x^3 + 5$ | correct | B11 |
| l7-evaluating.json | screens[4].question | What does $F(2) - F(1)$ come to now? | correct | B11 |
| l7-evaluating.json | screens[4].widget.options[0] | graded key (choice): $7$ | correct | B11 |
| l7-evaluating.json | screens[4].widget.options[1].text | wrong option, wrong under every convention: $12$ | correct | B11 |
| l7-evaluating.json | screens[4].widget.options[1].why | You added the 5 once. It is in $F(2)$ and in $F(1)$, so it cancels. | correct | B11 |
| l7-evaluating.json | screens[4].widget.options[2].text | wrong option, wrong under every convention: $13$ | correct | B11 |
| l7-evaluating.json | screens[4].widget.options[2].why | 13 is $F(2)$ alone. Subtract $F(1) = 6$. | correct | B11 |
| l7-evaluating.json | screens[4].widget.options[3].text | wrong option, wrong under every convention: $2$ | correct | B11 |
| l7-evaluating.json | screens[4].widget.options[3].why | You subtracted the 5 from both, then once more. $(8 + 5) - (1 + 5) = 7$. | correct | B11 |
| l7-evaluating.json | screens[4].hints[0].text | Work out $F(2)$ and $F(1)$ with the $+5$ included. | correct | B11 |
| l7-evaluating.json | screens[4].hints[1].text | $F(2) = 13$ and $F(1) = 6$. | correct | B11 |
| l7-evaluating.json | screens[4].hints[2].text | $13 - 6 = 7$. | correct | B11 |
| l7-evaluating.json | screens[4].feedback.correct | $(8 + 5) - (1 + 5) = 7$: the 5 cancels. | correct | B11 |
| l7-evaluating.json | screens[4].feedback.generic | Not quite right. Include the $+5$ in both $F(2)$ and $F(1)$, then subtract. | correct | B11 |
| l7-evaluating.json | screens[4].explain.text | $(8 + 5) - (1 + 5) = 7$: the 5 appears twice and cancels. Any constant $C$ does the same, so definite integ... | correct | B11 |
| l7-evaluating.json | screens[4].explain.canvas.segments[0].label | 7 | correct | B11 |
| l7-evaluating.json | screens[4].explain.canvas.segments[1].label | 7 | correct | B11 |
| l7-evaluating.json | screens[5].prose | The theorem also works when the limits run backwards, from 3 down to 1. | correct | B11 |
| l7-evaluating.json | screens[5].canvas.params.functions[0].label | $f(x) = 2x$ | correct | B11 |
| l7-evaluating.json | screens[5].canvas.state.segments[0].label | from 3 to 1 | correct | B11 |
| l7-evaluating.json | screens[5].question | Evaluate $\int_3^1 2x\,dx$. | correct | B11 |
| l7-evaluating.json | screens[5].widget.answer | graded key (numeric): -8 | correct | B11 |
| l7-evaluating.json | screens[5].widget.wrong[0] | slip positive = 8 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[5].widget.wrong[1] | slip forgot-fa = 1 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[5].widget.accept | $-8$: $\big[x^2\big]_3^1 = 1 - 9$. | correct | B11 |
| l7-evaluating.json | screens[5].hints[0].text | The top limit is now 1 and the bottom limit is 3. | correct | B11 |
| l7-evaluating.json | screens[5].hints[1].text | Compute $F(1) - F(3)$ with $F(x) = x^2$. | correct | B11 |
| l7-evaluating.json | screens[5].hints[2].text | $1 - 9 = -8$. | correct | B11 |
| l7-evaluating.json | screens[5].feedback.correct | $\big[x^2\big]_3^1 = 1 - 9 = -8$. | correct | B11 |
| l7-evaluating.json | screens[5].feedback.generic | Not quite right. Top limit minus bottom limit, even when the top is smaller. | correct | B11 |
| l7-evaluating.json | screens[5].feedback.byKey.positive | 8 runs from 1 to 3. Here the bottom limit is 3, so compute $F(1) - F(3)$. | correct | B11 |
| l7-evaluating.json | screens[5].feedback.byKey.forgot-fa | 1 is $F(1)$ alone. Subtract $F(3) = 9$. | correct | B11 |
| l7-evaluating.json | screens[5].explain.text | $\big[x^2\big]_3^1 = 1 - 9 = -8$. Swapping the limits flips the sign: $\int_b^a f = -\int_a^b f$. The regio... | correct | B11 |
| l7-evaluating.json | screens[6].prose | An antiderivative of $\dfrac{1}{x^2}$ is $F(x) = -\dfrac{1}{x}$. So the rule seems to give $\int_{-1}^{1} \... | correct | B11 |
| l7-evaluating.json | screens[6].canvas.params.functions[0].label | $1/x^2$ | correct | B11 |
| l7-evaluating.json | screens[6].canvas.state.caption | The curve stays above the axis on both sides of 0 | correct | B11 |
| l7-evaluating.json | screens[6].question | What is $\int_{-1}^{1} \dfrac{1}{x^2}\,dx$? | correct | B11 |
| l7-evaluating.json | screens[6].widget.options[0].text | wrong option, wrong under every convention: $-2$ | correct | B11 |
| l7-evaluating.json | screens[6].widget.options[0].why | You applied $F(b) - F(a)$, but $-\tfrac{1}{x}$ breaks at 0. The theorem needs $F' = f$ across the whole int... | correct | B11 |
| l7-evaluating.json | screens[6].widget.options[1].text | wrong option, wrong under every convention: $2$ | correct | B11 |
| l7-evaluating.json | screens[6].widget.options[1].why | You saw that a positive curve cannot give $-2$ and flipped the sign. The real problem is at 0, where the ar... | correct | B11 |
| l7-evaluating.json | screens[6].widget.options[2].text | wrong option, wrong under every convention: $0$ | correct | B11 |
| l7-evaluating.json | screens[6].widget.options[2].why | You expected the two halves to cancel. Both halves are above the axis, so they add. | correct | B11 |
| l7-evaluating.json | screens[6].widget.options[3] | graded key (choice): It is not a finite number: the area near 0 is unbounded | correct | B11 |
| l7-evaluating.json | screens[6].hints[0].text | Is $\tfrac{1}{x^2}$ ever negative? Can its integral be $-2$? | correct | B11 |
| l7-evaluating.json | screens[6].hints[1].text | Look at what happens to $f$ and $F$ at $x = 0$. | correct | B11 |
| l7-evaluating.json | screens[6].hints[2].text | Both blow up at 0, so the theorem does not apply. The area from a tiny $\varepsilon$ to 1 is $\tfrac{1}{\va... | correct | B11 |
| l7-evaluating.json | screens[6].feedback.correct | A positive integrand cannot give $-2$, and the area near 0 is unbounded. | correct | B11 |
| l7-evaluating.json | screens[6].feedback.generic | Not quite right. Check that $F$ is defined on the whole of $[-1, 1]$ before using it. | correct | B11 |
| l7-evaluating.json | screens[6].explain.text | A positive function cannot have a negative integral, so $-2$ is impossible. The theorem needs $F' = f$ at e... | correct | B11 |
| l7-evaluating.json | screens[7].prose | The shaded region lies under $y = x^2$ from $x = -1$ to $x = 2$, above the axis on both sides of 0. | correct | B11 |
| l7-evaluating.json | screens[7].canvas.params.functions[0].label | $x^2$ | correct | B11 |
| l7-evaluating.json | screens[7].question | Evaluate $\int_{-1}^{2} x^2\,dx$. Give a fraction or a decimal. | correct | B11 |
| l7-evaluating.json | screens[7].widget.answer | graded key (numeric): 3 | correct | B11 |
| l7-evaluating.json | screens[7].widget.wrong[0] | slip forgot-fa = 2.6667 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[7].widget.wrong[1] | slip sign-slip = 2.3333 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[7].widget.wrong[2] | slip order = -3 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[7].widget.accept | 3: $\tfrac{8}{3} - \left(-\tfrac{1}{3}\right)$. | correct | B11 |
| l7-evaluating.json | screens[7].hints[0].text | $F(x) = \tfrac{x^3}{3}$. Work out $F(-1)$ carefully. | correct | B11 |
| l7-evaluating.json | screens[7].hints[1].text | $(-1)^3 = -1$, so $F(-1) = -\tfrac{1}{3}$. | correct | B11 |
| l7-evaluating.json | screens[7].hints[2].text | $\tfrac{8}{3} - \left(-\tfrac{1}{3}\right) = \tfrac{9}{3} = 3$. | correct | B11 |
| l7-evaluating.json | screens[7].feedback.correct | $\tfrac{8}{3} - \left(-\tfrac{1}{3}\right) = 3$. | correct | B11 |
| l7-evaluating.json | screens[7].feedback.generic | Not quite right. Compute $F(2)$ and $F(-1)$ separately, signs included, then subtract. | correct | B11 |
| l7-evaluating.json | screens[7].feedback.byKey.forgot-fa | $\tfrac{8}{3}$ is $F(2)$ alone. You forgot to subtract $F(-1)$. | correct | B11 |
| l7-evaluating.json | screens[7].feedback.byKey.sign-slip | You subtracted $+\tfrac{1}{3}$. But $F(-1) = \tfrac{(-1)^3}{3} = -\tfrac{1}{3}$, and subtracting a negative... | correct | B11 |
| l7-evaluating.json | screens[7].feedback.byKey.order | You computed $F(-1) - F(2)$. Subtract the bottom limit's value from the top's. | correct | B11 |
| l7-evaluating.json | screens[7].explain.text | $F(2) - F(-1) = \tfrac{8}{3} - \left(-\tfrac{1}{3}\right) = 3$. The piece from $-1$ to 0 has area $\tfrac{1... | correct | B11 |
| l7-evaluating.json | screens[7].explain.canvas.area[0].label | 1/3 | correct | B11 |
| l7-evaluating.json | screens[7].explain.canvas.area[1].label | 8/3 | correct | B11 |
| l7-evaluating.json | screens[8].prose | Why does $F(b) - F(a)$ work? Last lesson, for a continuous $f$, $A(x) = \int_a^x f(t)\,dt$ had $A' = f$. Le... | correct | B11 |
| l7-evaluating.json | screens[8].question | Put the lines in order. | correct | B11 |
| l7-evaluating.json | screens[8].widget.answer | graded key (order): ["zero", "const", "at-a", "at-b", "done"] | correct | B11 |
| l7-evaluating.json | screens[8].widget.answer.order | graded order of 5 lines; each line follows from the one above | correct | B11 |
| l7-evaluating.json | screens[8].widget.lines[0].text | $(F - A)'(x) = f(x) - f(x) = 0$, since both are antiderivatives of $f$ | correct | B11 |
| l7-evaluating.json | screens[8].widget.lines[1].text | $F(x) = A(x) + C$ for one constant $C$, since a zero derivative on an interval means a constant | correct | B11 |
| l7-evaluating.json | screens[8].widget.lines[2].text | $F(a) = A(a) + C = C$, since $A(a)$ is the area of a region of zero width | correct | B11 |
| l7-evaluating.json | screens[8].widget.lines[3].text | $F(b) = A(b) + F(a)$, putting $x = b$ and $C = F(a)$ | correct | B11 |
| l7-evaluating.json | screens[8].widget.lines[4].text | $\int_a^b f(t)\,dt = A(b) = F(b) - F(a)$, rearranging | correct | B11 |
| l7-evaluating.json | screens[8].hints[0].text | Compare $F$ and $A$: what is the derivative of their difference? | correct | B11 |
| l7-evaluating.json | screens[8].hints[1].text | A function with derivative 0 on an interval is constant. Then find that constant. | correct | B11 |
| l7-evaluating.json | screens[8].hints[2].text | Difference has derivative 0, so $F = A + C$; put $x = a$ to get $C = F(a)$; put $x = b$ and rearrange. | correct | B11 |
| l7-evaluating.json | screens[8].feedback.correct | Each line follows from the one above. | correct | B11 |
| l7-evaluating.json | screens[8].feedback.generic | Not quite right. First show $F$ and $A$ differ by a constant, then pin the constant at $x = a$. | correct | B11 |
| l7-evaluating.json | screens[8].feedback.byKey.const | The constant comes from the zero derivative, so that line comes first. | correct | B11 |
| l7-evaluating.json | screens[8].feedback.byKey.at-a | You need $F = A + C$ before you can evaluate it at $a$. | correct | B11 |
| l7-evaluating.json | screens[8].feedback.byKey.at-b | Use $x = b$ only after $C$ is known to be $F(a)$. | correct | B11 |
| l7-evaluating.json | screens[8].feedback.byKey.done | The rearranged result is the last line. | correct | B11 |
| l7-evaluating.json | screens[8].explain.text | $F$ and $A$ have the same derivative, so they differ by a constant $C$. At $x = a$ the area $A(a)$ is 0, so... | correct | B11 |
| l7-evaluating.json | screens[9].prose | A contract pays £10,000 per year, spread evenly, for 5 years. At a continuous rate of 4%, money at time $t$... | correct | B11 |
| l7-evaluating.json | screens[9].canvas.params.functions[0].label | $10e^{-0.04t}$ | correct | B11 |
| l7-evaluating.json | screens[9].question | What is the present value, in pounds? | correct | B11 |
| l7-evaluating.json | screens[9].widget.answer | graded key (numeric): 45317.31 | correct | B11 |
| l7-evaluating.json | screens[9].widget.wrong[0] | slip undiscounted = 50000 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[9].widget.wrong[1] | slip forgot-fa = -204682.69 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[9].widget.wrong[2] | slip order = -45317.31 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[9].widget.wrong[3] | slip end-discount = 40936.54 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[9].widget.accept | About £45,317: $250{,}000(1 - e^{-0.2}) = 45{,}317.31$, to within 0.1%. | correct | B11 |
| l7-evaluating.json | screens[9].hints[0].text | An antiderivative of $e^{-0.04t}$ is $\dfrac{e^{-0.04t}}{-0.04} = -25e^{-0.04t}$. | correct | B11 |
| l7-evaluating.json | screens[9].hints[1].text | So $F(t) = -250{,}000\,e^{-0.04t}$. | correct | B11 |
| l7-evaluating.json | screens[9].hints[2].text | $F(5) - F(0) = 250{,}000(1 - e^{-0.2}) \approx 250{,}000 \times 0.18127$. | correct | B11 |
| l7-evaluating.json | screens[9].feedback.correct | About £45,317: that is $250{,}000(1 - e^{-0.2})$. | correct | B11 |
| l7-evaluating.json | screens[9].feedback.generic | Not quite right. Find $F(t) = -250{,}000\,e^{-0.04t}$, then compute $F(5) - F(0)$. | correct | B11 |
| l7-evaluating.json | screens[9].feedback.byKey.undiscounted | £50,000 ignores discounting. Money paid later is worth less today. | correct | B11 |
| l7-evaluating.json | screens[9].feedback.byKey.forgot-fa | You stopped at $F(5) = -250{,}000\,e^{-0.2}$. Subtract $F(0) = -250{,}000$ as well. | correct | B11 |
| l7-evaluating.json | screens[9].feedback.byKey.order | You computed $F(0) - F(5)$. Top limit minus bottom: $F(5) - F(0)$. | correct | B11 |
| l7-evaluating.json | screens[9].feedback.byKey.end-discount | You discounted all £50,000 at year 5. Most payments arrive earlier, so they are discounted less. | correct | B11 |
| l7-evaluating.json | screens[9].explain.text | $\Big[-250{,}000\,e^{-0.04t}\Big]_0^5 = 250{,}000(1 - e^{-0.2}) \approx \text{£}45{,}317$. In general $\int... | correct | B11 |
| l7-evaluating.json | screens[10].prose | A model says tomorrow's price $S$ is equally likely to be anywhere from £90 to £110. Its density is $\tfrac... | correct | B11 |
| l7-evaluating.json | screens[10].canvas.params.functions[0].label | $\max(s - 100, 0)/20$ | correct | B11 |
| l7-evaluating.json | screens[10].question | What is the expected payoff, in pounds? | correct | B11 |
| l7-evaluating.json | screens[10].widget.answer | graded key (numeric): 2.5 | correct | B11 |
| l7-evaluating.json | screens[10].widget.wrong[0] | slip given-pays = 5 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[10].widget.wrong[1] | slip best = 10 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[10].widget.wrong[2] | slip at-mean = 0 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | screens[10].widget.accept | £2.50: $\int_{100}^{110} \tfrac{s - 100}{20}\,ds$. | correct | B11 |
| l7-evaluating.json | screens[10].hints[0].text | Below £100 the payoff is 0. Integrate $\dfrac{s - 100}{20}$ from 100 to 110. | correct | B11 |
| l7-evaluating.json | screens[10].hints[1].text | An antiderivative is $\dfrac{(s - 100)^2}{40}$. | correct | B11 |
| l7-evaluating.json | screens[10].hints[2].text | $\dfrac{10^2}{40} - 0 = 2.5$. | correct | B11 |
| l7-evaluating.json | screens[10].feedback.correct | $\left[\dfrac{(s - 100)^2}{40}\right]_{100}^{110} = 2.5$, so £2.50. | correct | B11 |
| l7-evaluating.json | screens[10].feedback.generic | Not quite right. Integrate payoff times density over the prices where the call pays. | correct | B11 |
| l7-evaluating.json | screens[10].feedback.byKey.given-pays | £5 is the average payoff when the call pays. It pays only half the time, so the expectation is half that. | correct | B11 |
| l7-evaluating.json | screens[10].feedback.byKey.best | £10 is the best case, at £110. Most outcomes pay less, or nothing. | correct | B11 |
| l7-evaluating.json | screens[10].feedback.byKey.at-mean | You priced the payoff at the average price, £100. The payoff is not a straight line, so average the payoff ... | correct | B11 |
| l7-evaluating.json | screens[10].explain.text | $\left[\dfrac{(s - 100)^2}{40}\right]_{100}^{110} = \dfrac{100}{40} = 2.5$, so £2.50. The payoff at the ave... | correct | B11 |
| l7-evaluating.json | summary.ideas[0] | To evaluate $\int_a^b f(x)\,dx$, find any antiderivative $F$ and compute $F(b) - F(a)$. | correct | B11 |
| l7-evaluating.json | summary.ideas[1] | The constant $C$ cancels, and swapping the limits flips the sign. | correct | B11 |
| l7-evaluating.json | summary.ideas[2] | The rule needs $F' = f$ on all of $[a, b]$. Across a blow-up, such as $\tfrac{1}{x^2}$ at 0, it fails. | correct | B11 |
| l7-evaluating.json | summary.formula.name | Fundamental theorem (evaluation) | correct | B11 |
| l7-evaluating.json | summary.formula.tex | \int_a^b f(x)\,dx = F(b) - F(a), \quad F' = f, \ f \text{ continuous on } [a, b] | correct | B11 |
| l7-evaluating.json | summary.formula.note | Top limit first, then subtract the bottom limit's value, sign and all. | correct | B11 |
| l7-evaluating.json | summary.trap | Subtract all of $F(a)$, sign included: $\tfrac{8}{3} - \left(-\tfrac{1}{3}\right) = 3$, not $\tfrac{7}{3}$. | correct | B11 |
| l7-evaluating.json | quiz[0].prose | Use $F(x) = e^x$. | correct | B11 |
| l7-evaluating.json | quiz[0].question | Evaluate $\int_0^2 e^x\,dx$, to 3 decimal places. | correct | B11 |
| l7-evaluating.json | quiz[0].widget.answer | graded key (numeric): 6.389 | correct | B11 |
| l7-evaluating.json | quiz[0].widget.wrong[0] | slip forgot-fa = 7.389 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | quiz[0].widget.accept | $e^2 - 1 \approx 6.389$. | correct | B11 |
| l7-evaluating.json | quiz[0].feedback.correct | $e^2 - e^0 = e^2 - 1 \approx 6.389$. | correct | B11 |
| l7-evaluating.json | quiz[0].feedback.generic | Not quite right. Compute $F(2) - F(0)$ with $F(x) = e^x$. | correct | B11 |
| l7-evaluating.json | quiz[0].feedback.byKey.forgot-fa | $e^2$ alone forgets $F(0) = e^0 = 1$. The exponential is not 0 at 0. | correct | B11 |
| l7-evaluating.json | quiz[0].explain.text | $\big[e^x\big]_0^2 = e^2 - e^0 = e^2 - 1 \approx 6.389$. A common slip is to treat $F(0)$ as 0; here it is 1. | correct | B11 |
| l7-evaluating.json | quiz[1].prose | The limits run from 2 down to 0. | correct | B11 |
| l7-evaluating.json | quiz[1].question | Evaluate $\int_2^0 3x^2\,dx$. | correct | B11 |
| l7-evaluating.json | quiz[1].widget.answer | graded key (numeric): -8 | correct | B11 |
| l7-evaluating.json | quiz[1].widget.wrong[0] | slip positive = 8 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | quiz[1].widget.accept | $-8$: $0^3 - 2^3$. | correct | B11 |
| l7-evaluating.json | quiz[1].feedback.correct | $\big[x^3\big]_2^0 = 0 - 8 = -8$. | correct | B11 |
| l7-evaluating.json | quiz[1].feedback.generic | Not quite right. Top limit minus bottom limit: $F(0) - F(2)$. | correct | B11 |
| l7-evaluating.json | quiz[1].feedback.byKey.positive | 8 is the integral from 0 to 2. Running from 2 to 0 flips the sign. | correct | B11 |
| l7-evaluating.json | quiz[1].explain.text | $\big[x^3\big]_2^0 = 0 - 8 = -8$. Swapping the limits of $\int_0^2 3x^2\,dx = 8$ flips its sign. | correct | B11 |
| l7-evaluating.json | quiz[2].prose | $\int_0^1 (4x^3 - 2x)\,dx = \big[x^4 - x^2\big]_0^1 = 0$. | correct | B11 |
| l7-evaluating.json | quiz[2].question | What does the 0 tell you? | correct | B11 |
| l7-evaluating.json | quiz[2].widget.options[0] | graded key (choice): The signed areas above and below the axis cancel | correct | B11 |
| l7-evaluating.json | quiz[2].widget.options[1].text | wrong option, wrong under every convention: The curve encloses no area with the axis | correct | B11 |
| l7-evaluating.json | quiz[2].widget.options[1].why | The curve dips below the axis on $(0, \tfrac{1}{\sqrt{2}})$ and rises above it later. Those areas are not z... | correct | B11 |
| l7-evaluating.json | quiz[2].widget.options[2].text | wrong option, wrong under every convention: The function is 0 on $[0, 1]$ | correct | B11 |
| l7-evaluating.json | quiz[2].widget.options[2].why | At $x = 1$ it equals 2. Only the signed total is 0. | correct | B11 |
| l7-evaluating.json | quiz[2].feedback.correct | A definite integral is a signed area, and here the two parts cancel. | correct | B11 |
| l7-evaluating.json | quiz[2].feedback.generic | Not quite right. Sketch $4x^3 - 2x$ on $[0, 1]$: is it ever negative? | correct | B11 |
| l7-evaluating.json | quiz[2].explain.text | $4x^3 - 2x = 2x(2x^2 - 1)$ is negative for $0 < x < \tfrac{1}{\sqrt{2}}$ and positive after. Each part has ... | correct | B11 |
| l7-evaluating.json | quiz[3].prose | An annuity pays £2,000 per year continuously for 10 years. The continuous discount rate is 5%. | correct | B11 |
| l7-evaluating.json | quiz[3].question | What is its present value $\int_0^{10} 2000\,e^{-0.05t}\,dt$, in pounds? | correct | B11 |
| l7-evaluating.json | quiz[3].widget.answer | graded key (numeric): 15738.77 | correct | B11 |
| l7-evaluating.json | quiz[3].widget.wrong[0] | slip undiscounted = 20000 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | quiz[3].widget.wrong[1] | slip end-discount = 12130.61 is the value of the named mistake and is not a correct answer | correct | B11 |
| l7-evaluating.json | quiz[3].widget.accept | About £15,739: $40{,}000(1 - e^{-0.5})$, to within 0.1%. | correct | B11 |
| l7-evaluating.json | quiz[3].feedback.correct | About £15,739: that is $40{,}000(1 - e^{-0.5})$. | correct | B11 |
| l7-evaluating.json | quiz[3].feedback.generic | Not quite right. Use $\dfrac{c(1 - e^{-rT})}{r}$ with $c = 2000$, $r = 0.05$, $T = 10$. | correct | B11 |
| l7-evaluating.json | quiz[3].feedback.byKey.undiscounted | £20,000 ignores discounting. Later payments are worth less today. | correct | B11 |
| l7-evaluating.json | quiz[3].feedback.byKey.end-discount | You discounted everything at year 10. Most payments arrive earlier and are discounted less. | correct | B11 |
| l7-evaluating.json | quiz[3].explain.text | $\dfrac{2000(1 - e^{-0.5})}{0.05} = 40{,}000 \times 0.39347 \approx \text{£}15{,}739$. That is about 79% of... | correct | B11 |
| l8-between-curves.json | screens[0].prose | The line $y = x + 2$ and the parabola $y = x^2$ cross twice. Between the crossings they close off a region. | correct | B12 |
| l8-between-curves.json | screens[0].canvas.params.functions[0].label | $y = x + 2$ | correct | B12 |
| l8-between-curves.json | screens[0].canvas.params.functions[1].label | $y = x^2$ | correct | B12 |
| l8-between-curves.json | screens[0].question | Tap the point inside the region enclosed by both curves. | correct | B12 |
| l8-between-curves.json | screens[0].widget.answer | graded key (tap-regions): ["A"] | correct | B12 |
| l8-between-curves.json | screens[0].hints[0].text | Find where the two curves cross first. | correct | B12 |
| l8-between-curves.json | screens[0].hints[1].text | They cross at $x = -1$ and $x = 2$. | correct | B12 |
| l8-between-curves.json | screens[0].hints[2].text | The enclosed region lies between $x = -1$ and $x = 2$, above the parabola and below the line. | correct | B12 |
| l8-between-curves.json | screens[0].feedback.correct | A is above the parabola, below the line, and between the crossings. | correct | B12 |
| l8-between-curves.json | screens[0].feedback.generic | Not quite right. The region is closed off on every side by the two curves. | correct | B12 |
| l8-between-curves.json | screens[0].feedback.byKey.B | B sits between the curves, but past $x = 2$, where they have crossed. That gap is not closed off on the right. | correct | B12 |
| l8-between-curves.json | screens[0].feedback.byKey.C | C is below both curves: under the parabola, outside the region. | correct | B12 |
| l8-between-curves.json | screens[0].feedback.byKey.D | D is above the line, so it is outside the region. | correct | B12 |
| l8-between-curves.json | screens[0].explain.text | A lies above the parabola and below the line, between the crossings. B is between the curves too, but beyon... | correct | B12 |
| l8-between-curves.json | screens[1].prose | Drag the dot along the line. The segment joins the two curves at the same $x$, and the caption gives line m... | correct | B12 |
| l8-between-curves.json | screens[1].canvas.params.functions[0].label | $y = x + 2$ | correct | B12 |
| l8-between-curves.json | screens[1].canvas.params.functions[1].label | $y = x^2$ | correct | B12 |
| l8-between-curves.json | screens[1].canvas.derive.caption | At $x$ = {{fixed(P.x, 2)}}: line − parabola = {{fixed(P.x + 2 - P.x*P.x, 2)}} | correct | B12 |
| l8-between-curves.json | screens[1].question | Where is the gap zero, and which curve is on top between those places? | correct | B12 |
| l8-between-curves.json | screens[1].widget.options[0] | graded key (choice): Zero at $x = -1$ and $x = 2$, with the line on top between them | correct | B12 |
| l8-between-curves.json | screens[1].widget.options[1].text | wrong option, wrong under every convention: Zero at $x = 0$, with the parabola on top | correct | B12 |
| l8-between-curves.json | screens[1].widget.options[1].why | At $x = 0$ the gap is 2, not 0: the line is at 2 and the parabola at 0. | correct | B12 |
| l8-between-curves.json | screens[1].widget.options[2].text | wrong option, wrong under every convention: Zero at $x = -1$ and $x = 2$, with the parabola on top between ... | correct | B12 |
| l8-between-curves.json | screens[1].widget.options[2].why | Between the crossings the caption is positive, so line minus parabola is positive: the line is higher. | correct | B12 |
| l8-between-curves.json | screens[1].widget.options[3].text | wrong option, wrong under every convention: The gap is never zero | correct | B12 |
| l8-between-curves.json | screens[1].widget.options[3].why | Drag to $x = 2$: the caption reads 0.00. | correct | B12 |
| l8-between-curves.json | screens[1].hints[0].text | Drag P to the far left, then to the far right, reading the caption. | correct | B12 |
| l8-between-curves.json | screens[1].hints[1].text | The caption changes sign twice. | correct | B12 |
| l8-between-curves.json | screens[1].hints[2].text | It reads 0.00 at $x = -1$ and $x = 2$, and is positive in between. | correct | B12 |
| l8-between-curves.json | screens[1].feedback.correct | The gap $(x + 2) - x^2$ is zero at $-1$ and 2 and positive between. | correct | B12 |
| l8-between-curves.json | screens[1].feedback.generic | Not quite right. Watch the sign of the caption as you drag. | correct | B12 |
| l8-between-curves.json | screens[1].explain.text | The gap $(x + 2) - x^2$ is zero where $x^2 = x + 2$, at $x = -1$ and $x = 2$. Between them it is positive, ... | correct | B12 |
| l8-between-curves.json | screens[2].prose | Add up thin strips, each as tall as the gap. The **area between the curves** is $$\int_{-1}^{2} \Big[(x + 2... | correct | B12 |
| l8-between-curves.json | screens[2].canvas.params.functions[0].label | $y = x + 2$ | correct | B12 |
| l8-between-curves.json | screens[2].canvas.params.functions[1].label | $y = x^2$ | correct | B12 |
| l8-between-curves.json | screens[2].question | Evaluate it. Give a decimal. | correct | B12 |
| l8-between-curves.json | screens[2].widget.answer | graded key (numeric): 4.5 | correct | B12 |
| l8-between-curves.json | screens[2].widget.wrong[0] | slip under-line = 7.5 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | screens[2].widget.wrong[1] | slip upside = -4.5 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | screens[2].widget.wrong[2] | slip under-para = 3 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | screens[2].widget.accept | 4.5: $\tfrac{10}{3} + \tfrac{7}{6} = \tfrac{27}{6}$. | correct | B12 |
| l8-between-curves.json | screens[2].hints[0].text | An antiderivative of $x + 2 - x^2$ is $\tfrac{x^2}{2} + 2x - \tfrac{x^3}{3}$. | correct | B12 |
| l8-between-curves.json | screens[2].hints[1].text | At 2 it is $\tfrac{10}{3}$; at $-1$ it is $-\tfrac{7}{6}$. | correct | B12 |
| l8-between-curves.json | screens[2].hints[2].text | $\tfrac{10}{3} - \left(-\tfrac{7}{6}\right) = \tfrac{27}{6} = 4.5$. | correct | B12 |
| l8-between-curves.json | screens[2].feedback.correct | $\tfrac{10}{3} + \tfrac{7}{6} = 4.5$. | correct | B12 |
| l8-between-curves.json | screens[2].feedback.generic | Not quite right. Integrate top minus bottom, $x + 2 - x^2$, from $-1$ to 2. | correct | B12 |
| l8-between-curves.json | screens[2].feedback.byKey.under-line | 7.5 is the area under the line alone. Subtract the area under the parabola, which is 3. | correct | B12 |
| l8-between-curves.json | screens[2].feedback.byKey.upside | You took parabola minus line. Top minus bottom keeps the area positive. | correct | B12 |
| l8-between-curves.json | screens[2].feedback.byKey.under-para | 3 is the area under the parabola. The region sits between the curves, above it. | correct | B12 |
| l8-between-curves.json | screens[2].explain.text | $\left[\tfrac{x^2}{2} + 2x - \tfrac{x^3}{3}\right]_{-1}^{2} = \tfrac{10}{3} + \tfrac{7}{6} = 4.5$. Equally,... | correct | B12 |
| l8-between-curves.json | screens[2].explain.canvas.area.label | 4.5 | correct | B12 |
| l8-between-curves.json | screens[3].prose | New pair: $y = 4 - x^2$ and $y = x^2 - 4$. Drag the two dots to the points where the curves cross. | correct | B12 |
| l8-between-curves.json | screens[3].canvas.params.functions[0].label | $y = 4 - x^2$ | correct | B12 |
| l8-between-curves.json | screens[3].canvas.params.functions[1].label | $y = x^2 - 4$ | correct | B12 |
| l8-between-curves.json | screens[3].question | Where do the curves cross? | correct | B12 |
| l8-between-curves.json | screens[3].widget.points | graded key (drag-point): [{"id": "L", "target": [-2, 0], "tol": 0.25}, {"id": "R", "target": [2, 0], "tol":... | correct | B12 |
| l8-between-curves.json | screens[3].widget.wrong[0] | slip vertex = {"x": [-0.3, 0.3], "y": [-4.5, 4.5]} is the value of the named mistake and is not a correct a... | correct | B12 |
| l8-between-curves.json | screens[3].hints[0].text | Set $4 - x^2 = x^2 - 4$. | correct | B12 |
| l8-between-curves.json | screens[3].hints[1].text | That gives $2x^2 = 8$. | correct | B12 |
| l8-between-curves.json | screens[3].hints[2].text | $x = \pm 2$, where both curves are at height 0. | correct | B12 |
| l8-between-curves.json | screens[3].feedback.correct | They cross at $(-2, 0)$ and $(2, 0)$. | correct | B12 |
| l8-between-curves.json | screens[3].feedback.generic | Not quite right. Set the two expressions equal and solve for $x$. | correct | B12 |
| l8-between-curves.json | screens[3].feedback.byKey.vertex | That dot is on the $y$-axis, at a turning point. The curves meet where their heights agree: set $4 - x^2 = ... | correct | B12 |
| l8-between-curves.json | screens[3].feedback.byKey.L | The left dot is not on a crossing yet. Solve $4 - x^2 = x^2 - 4$. | correct | B12 |
| l8-between-curves.json | screens[3].feedback.byKey.R | The right dot is not on a crossing yet. Solve $4 - x^2 = x^2 - 4$. | correct | B12 |
| l8-between-curves.json | screens[3].explain.text | $4 - x^2 = x^2 - 4$ gives $x^2 = 4$, so $x = \pm 2$. Both curves pass through the axis there. Between the c... | correct | B12 |
| l8-between-curves.json | screens[4].prose | The region between $y = 4 - x^2$ and $y = x^2 - 4$ sits half above the axis and half below it. | correct | B12 |
| l8-between-curves.json | screens[4].canvas.params.functions[0].label | $y = 4 - x^2$ | correct | B12 |
| l8-between-curves.json | screens[4].canvas.params.functions[1].label | $y = x^2 - 4$ | correct | B12 |
| l8-between-curves.json | screens[4].question | What is the area between the curves? Give a decimal. | correct | B12 |
| l8-between-curves.json | screens[4].widget.answer | graded key (numeric): 21.333 | correct | B12 |
| l8-between-curves.json | screens[4].widget.wrong[0] | slip cancel = 0 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | screens[4].widget.wrong[1] | slip top-only = 10.667 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | screens[4].widget.accept | $\tfrac{64}{3} \approx 21.33$. | correct | B12 |
| l8-between-curves.json | screens[4].hints[0].text | Top minus bottom: $(4 - x^2) - (x^2 - 4) = 8 - 2x^2$. | correct | B12 |
| l8-between-curves.json | screens[4].hints[1].text | Integrate $8 - 2x^2$ from $-2$ to 2. | correct | B12 |
| l8-between-curves.json | screens[4].hints[2].text | $\Big[8x - \tfrac{2x^3}{3}\Big]_{-2}^{2} = \tfrac{32}{3} + \tfrac{32}{3} = \tfrac{64}{3}$. | correct | B12 |
| l8-between-curves.json | screens[4].feedback.correct | Top minus bottom integrates to $\tfrac{64}{3}$, about 21.33. | correct | B12 |
| l8-between-curves.json | screens[4].feedback.generic | Not quite right. Integrate top minus bottom, $8 - 2x^2$, between the crossings. | correct | B12 |
| l8-between-curves.json | screens[4].feedback.byKey.cancel | You added the signed areas under each curve, $\tfrac{32}{3} + \left(-\tfrac{32}{3}\right)$. Area between cu... | correct | B12 |
| l8-between-curves.json | screens[4].feedback.byKey.top-only | That is the part above the axis only. The part below the axis is enclosed too. | correct | B12 |
| l8-between-curves.json | screens[4].explain.text | Top minus bottom is $8 - 2x^2$ all the way from $-2$ to 2, on both sides of the axis. It integrates to $\tf... | correct | B12 |
| l8-between-curves.json | screens[4].explain.canvas.area.label | 64/3 | correct | B12 |
| l8-between-curves.json | screens[5].prose | $y = x$ and $y = x^3$ cross three times, at $x = -1$, 0 and 1. Together they enclose two pieces. | correct | B12 |
| l8-between-curves.json | screens[5].canvas.params.functions[0].label | $y = x$ | correct | B12 |
| l8-between-curves.json | screens[5].canvas.params.functions[1].label | $y = x^3$ | correct | B12 |
| l8-between-curves.json | screens[5].question | What is the total area enclosed between the curves? Give a decimal. | correct | B12 |
| l8-between-curves.json | screens[5].widget.answer | graded key (numeric): 0.5 | correct | B12 |
| l8-between-curves.json | screens[5].widget.wrong[0] | slip cancelled = 0 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | screens[5].widget.wrong[1] | slip one-piece = 0.25 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | screens[5].widget.accept | 0.5: two pieces of $\tfrac{1}{4}$. | correct | B12 |
| l8-between-curves.json | screens[5].hints[0].text | Which curve is on top on $(-1, 0)$? Test $x = -\tfrac{1}{2}$. | correct | B12 |
| l8-between-curves.json | screens[5].hints[1].text | On $(-1, 0)$, $x^3$ is above $x$. On $(0, 1)$, $x$ is above $x^3$. | correct | B12 |
| l8-between-curves.json | screens[5].hints[2].text | Each piece has area $\tfrac{1}{4}$, so the total is $\tfrac{1}{2}$. | correct | B12 |
| l8-between-curves.json | screens[5].feedback.correct | $\tfrac{1}{4} + \tfrac{1}{4} = \tfrac{1}{2}$. | correct | B12 |
| l8-between-curves.json | screens[5].feedback.generic | Not quite right. Split at the crossing at 0 and use top minus bottom on each piece. | correct | B12 |
| l8-between-curves.json | screens[5].feedback.byKey.cancelled | You integrated $x - x^3$ from $-1$ to 1 in one go. On $(-1, 0)$ that gap is negative, so the two pieces can... | correct | B12 |
| l8-between-curves.json | screens[5].feedback.byKey.one-piece | 0.25 is one piece. There are two, mirror images of each other. | correct | B12 |
| l8-between-curves.json | screens[5].explain.text | One integral of $x - x^3$ gives $\tfrac{1}{4} - \tfrac{1}{4} = 0$, because the left piece counts negative. ... | correct | B12 |
| l8-between-curves.json | screens[5].explain.canvas.area[0].label | 1/4 | correct | B12 |
| l8-between-curves.json | screens[5].explain.canvas.area[1].label | 1/4 | correct | B12 |
| l8-between-curves.json | screens[6].prose | Area between curves is top minus bottom. Where the curves cross, the top changes, so we split there: $$\tex... | correct | B12 |
| l8-between-curves.json | screens[6].canvas.state.vlines[0].label | $\frac{\pi}{4}$ | correct | B12 |
| l8-between-curves.json | screens[6].question | Which gives the area between $\sin x$ and $\cos x$ from 0 to $\pi$? | correct | B12 |
| l8-between-curves.json | screens[6].widget.options[0] | graded key (choice): $\int_0^{\pi/4} (\cos x - \sin x)\,dx + \int_{\pi/4}^{\pi} (\sin x - \cos x)\,dx$ | correct | B12 |
| l8-between-curves.json | screens[6].widget.options[1].text | wrong option, wrong under every convention: $\int_0^{\pi} (\sin x - \cos x)\,dx$ | correct | B12 |
| l8-between-curves.json | screens[6].widget.options[1].why | One integral lets the piece where $\cos x$ is on top count negative. | correct | B12 |
| l8-between-curves.json | screens[6].widget.options[2].text | wrong option, wrong under every convention: $\int_0^{\pi/4} (\sin x - \cos x)\,dx + \int_{\pi/4}^{\pi} (\si... | correct | B12 |
| l8-between-curves.json | screens[6].widget.options[2].why | On $(0, \tfrac{\pi}{4})$, $\cos x$ is on top, so that first piece comes out negative. | correct | B12 |
| l8-between-curves.json | screens[6].widget.options[3].text | wrong option, wrong under every convention: $\int_0^{\pi} (\sin x + \cos x)\,dx$ | correct | B12 |
| l8-between-curves.json | screens[6].widget.options[3].why | Adding the heights stacks two areas. The gap between curves is a difference. | correct | B12 |
| l8-between-curves.json | screens[6].feedback.correct | Each piece takes its own top minus bottom. | correct | B12 |
| l8-between-curves.json | screens[6].feedback.generic | Not quite right. Find which curve is on top on each side of $\tfrac{\pi}{4}$. | correct | B12 |
| l8-between-curves.json | screens[6].explain.text | $\cos x$ is on top until $\tfrac{\pi}{4}$ and $\sin x$ after, so each piece takes its own top minus bottom.... | correct | B12 |
| l8-between-curves.json | screens[7].prose | Now write the area between $y = x$ and $y = x^3$ as a full argument, one justified line at a time. | correct | B12 |
| l8-between-curves.json | screens[7].question | Put the lines in order. | correct | B12 |
| l8-between-curves.json | screens[7].widget.answer | graded key (order): ["meet", "top", "split", "value"] | correct | B12 |
| l8-between-curves.json | screens[7].widget.answer.order | graded order of 4 lines; each line follows from the one above | correct | B12 |
| l8-between-curves.json | screens[7].widget.lines[0].text | $x^3 = x$ gives $x(x - 1)(x + 1) = 0$, so the curves meet at $x = -1, 0, 1$ | correct | B12 |
| l8-between-curves.json | screens[7].widget.lines[1].text | On $(-1, 0)$, $x^3$ is on top; on $(0, 1)$, $x$ is, testing $x = \mp\tfrac{1}{2}$ | correct | B12 |
| l8-between-curves.json | screens[7].widget.lines[2].text | Area $= \int_{-1}^{0} (x^3 - x)\,dx + \int_0^1 (x - x^3)\,dx$, top minus bottom on each piece | correct | B12 |
| l8-between-curves.json | screens[7].widget.lines[3].text | $= \tfrac{1}{4} + \tfrac{1}{4} = \tfrac{1}{2}$, using $F(b) - F(a)$ on each piece | correct | B12 |
| l8-between-curves.json | screens[7].hints[0].text | You cannot know where to split until you know where the curves meet. | correct | B12 |
| l8-between-curves.json | screens[7].hints[1].text | After the crossings, decide which curve is on top on each piece. | correct | B12 |
| l8-between-curves.json | screens[7].hints[2].text | Crossings, which is on top, write the split integral, evaluate. | correct | B12 |
| l8-between-curves.json | screens[7].feedback.correct | Crossings, top curve, split integral, value. | correct | B12 |
| l8-between-curves.json | screens[7].feedback.generic | Not quite right. The split needs the crossings and the top curve on each piece first. | correct | B12 |
| l8-between-curves.json | screens[7].feedback.byKey.top | Testing points needs the pieces, and the pieces come from the crossings. | correct | B12 |
| l8-between-curves.json | screens[7].feedback.byKey.split | You can only write top minus bottom once you know which curve is on top. | correct | B12 |
| l8-between-curves.json | screens[7].feedback.byKey.value | Evaluating comes last. | correct | B12 |
| l8-between-curves.json | screens[7].explain.text | The crossings cut the interval into pieces, and a test point names the top curve on each. Then each piece i... | correct | B12 |
| l8-between-curves.json | screens[8].prose | Over 12 months a fund gains at rate $f(t) = 30 - 2t$, in £k per month. Its benchmark gains at a steady $b(t... | correct | B12 |
| l8-between-curves.json | screens[8].question | After 12 months, how far is the fund's equity curve above the benchmark's, in £k? Use a negative number if ... | correct | B12 |
| l8-between-curves.json | screens[8].widget.answer | graded key (numeric): -24 | correct | B12 |
| l8-between-curves.json | screens[8].widget.wrong[0] | slip total-area = 74 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | screens[8].widget.wrong[1] | slip lead = 25 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | screens[8].widget.wrong[2] | slip sign = 24 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | screens[8].widget.wrong[3] | slip lag = -49 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | screens[8].widget.accept | $-24$: the fund ends £24k behind. | correct | B12 |
| l8-between-curves.json | screens[8].hints[0].text | Integrate $f - b = 10 - 2t$ from 0 to 12, keeping the sign. | correct | B12 |
| l8-between-curves.json | screens[8].hints[1].text | The lead area is 25 and the lag area is 49. | correct | B12 |
| l8-between-curves.json | screens[8].hints[2].text | $\Big[10t - t^2\Big]_0^{12} = 120 - 144 = -24$. | correct | B12 |
| l8-between-curves.json | screens[8].feedback.correct | $\int_0^{12} (f - b)\,dt = 25 - 49 = -24$. | correct | B12 |
| l8-between-curves.json | screens[8].feedback.generic | Not quite right. Integrate $f - b$ over the whole year, keeping the sign. | correct | B12 |
| l8-between-curves.json | screens[8].feedback.byKey.total-area | 74 is the total area between the curves, both pieces counted positive. Here the lagging months take gains a... | correct | B12 |
| l8-between-curves.json | screens[8].feedback.byKey.lead | 25 is the lead built up by month 5. The fund then lags for 7 months. | correct | B12 |
| l8-between-curves.json | screens[8].feedback.byKey.sign | The lag area, 49, is bigger than the lead, 25. So the fund finishes below. | correct | B12 |
| l8-between-curves.json | screens[8].feedback.byKey.lag | $-49$ counts only the lagging months. Add the lead of 25 from the first five. | correct | B12 |
| l8-between-curves.json | screens[8].explain.text | The fund leads until month 5, building a gap of 25, then lags, losing 49. The net gap is $\int_0^{12} (f - ... | correct | B12 |
| l8-between-curves.json | screens[8].explain.canvas.area[0].label | +25 | correct | B12 |
| l8-between-curves.json | screens[8].explain.canvas.area[1].label | −49 | correct | B12 |
| l8-between-curves.json | summary.ideas[0] | The area between two curves is the integral of top minus bottom, between the crossings. | correct | B12 |
| l8-between-curves.json | summary.ideas[1] | Find the crossings by setting the curves equal, and test a point to see which is on top. | correct | B12 |
| l8-between-curves.json | summary.ideas[2] | Where the curves cross inside the interval, split there, or the pieces cancel. The x-axis plays no part. | correct | B12 |
| l8-between-curves.json | summary.formula.name | Area between curves | correct | B12 |
| l8-between-curves.json | summary.formula.tex | \text{area} = \int_a^b \big\|f(x) - g(x)\big\|\,dx | correct | B12 |
| l8-between-curves.json | summary.formula.note | Split at every crossing and use top minus bottom on each piece. | correct | B12 |
| l8-between-curves.json | summary.trap | One integral of $f - g$ across a crossing cancels: $\int_{-1}^{1} (x - x^3)\,dx = 0$, yet the enclosed area... | correct | B12 |
| l8-between-curves.json | quiz[0].prose | $y = x$ and $y = x^2$ cross at $x = 0$ and $x = 1$. | correct | B12 |
| l8-between-curves.json | quiz[0].question | What is the area between them? Give a decimal to 3 places. | correct | B12 |
| l8-between-curves.json | quiz[0].widget.answer | graded key (numeric): 0.167 | correct | B12 |
| l8-between-curves.json | quiz[0].widget.wrong[0] | slip upside = -0.167 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | quiz[0].widget.wrong[1] | slip under-line = 0.5 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | quiz[0].widget.accept | $\tfrac{1}{6} \approx 0.167$. | correct | B12 |
| l8-between-curves.json | quiz[0].feedback.correct | $\int_0^1 (x - x^2)\,dx = \tfrac{1}{2} - \tfrac{1}{3} = \tfrac{1}{6}$. | correct | B12 |
| l8-between-curves.json | quiz[0].feedback.generic | Not quite right. On $(0, 1)$ the line is on top: integrate $x - x^2$. | correct | B12 |
| l8-between-curves.json | quiz[0].feedback.byKey.upside | You took parabola minus line. On $(0, 1)$, $x > x^2$, so the line is on top. | correct | B12 |
| l8-between-curves.json | quiz[0].feedback.byKey.under-line | 0.5 is the area under the line alone. Subtract the area under the parabola. | correct | B12 |
| l8-between-curves.json | quiz[0].explain.text | At $x = \tfrac{1}{2}$ the line is at 0.5 and the parabola at 0.25, so the line is on top. $\int_0^1 (x - x^... | correct | B12 |
| l8-between-curves.json | quiz[1].prose | The line $y = 4$ cuts the parabola $y = x^2$. | correct | B12 |
| l8-between-curves.json | quiz[1].question | What area do they enclose? Give a decimal to 2 places. | correct | B12 |
| l8-between-curves.json | quiz[1].widget.answer | graded key (numeric): 10.67 | correct | B12 |
| l8-between-curves.json | quiz[1].widget.wrong[0] | slip half = 5.33 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | quiz[1].widget.wrong[1] | slip upside = -10.67 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | quiz[1].widget.accept | $\tfrac{32}{3} \approx 10.67$. | correct | B12 |
| l8-between-curves.json | quiz[1].feedback.correct | $\int_{-2}^{2} (4 - x^2)\,dx = \tfrac{32}{3}$. | correct | B12 |
| l8-between-curves.json | quiz[1].feedback.generic | Not quite right. Find the crossings, $x = \pm 2$, then integrate $4 - x^2$. | correct | B12 |
| l8-between-curves.json | quiz[1].feedback.byKey.half | That is the half from 0 to 2. The region runs from $-2$ to 2. | correct | B12 |
| l8-between-curves.json | quiz[1].feedback.byKey.upside | You took parabola minus line. The line $y = 4$ is on top between the crossings. | correct | B12 |
| l8-between-curves.json | quiz[1].explain.text | $x^2 = 4$ at $x = \pm 2$. Then $\Big[4x - \tfrac{x^3}{3}\Big]_{-2}^{2} = \tfrac{16}{3} + \tfrac{16}{3} = \t... | correct | B12 |
| l8-between-curves.json | quiz[2].prose | $\sin x$ and $\cos x$ cross once on $[0, \pi]$, at $\tfrac{\pi}{4}$. | correct | B12 |
| l8-between-curves.json | quiz[2].question | What is the area between them on $[0, \pi]$? Give a decimal to 3 places. | correct | B12 |
| l8-between-curves.json | quiz[2].widget.answer | graded key (numeric): 2.828 | correct | B12 |
| l8-between-curves.json | quiz[2].widget.wrong[0] | slip no-split = 2 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | quiz[2].widget.wrong[1] | slip one-piece = 2.414 is the value of the named mistake and is not a correct answer | correct | B12 |
| l8-between-curves.json | quiz[2].widget.accept | $2\sqrt{2} \approx 2.828$. | correct | B12 |
| l8-between-curves.json | quiz[2].feedback.correct | $(\sqrt{2} - 1) + (\sqrt{2} + 1) = 2\sqrt{2}$. | correct | B12 |
| l8-between-curves.json | quiz[2].feedback.generic | Not quite right. Split at $\tfrac{\pi}{4}$ and take top minus bottom on each piece. | correct | B12 |
| l8-between-curves.json | quiz[2].feedback.byKey.no-split | You integrated $\sin x - \cos x$ from 0 to $\pi$ without splitting. The piece before $\tfrac{\pi}{4}$ cance... | correct | B12 |
| l8-between-curves.json | quiz[2].feedback.byKey.one-piece | That is the piece from $\tfrac{\pi}{4}$ to $\pi$ alone. Add the piece from 0 to $\tfrac{\pi}{4}$, where $\c... | correct | B12 |
| l8-between-curves.json | quiz[2].explain.text | $\int_0^{\pi/4} (\cos x - \sin x)\,dx = \sqrt{2} - 1$ and $\int_{\pi/4}^{\pi} (\sin x - \cos x)\,dx = 1 + \... | correct | B12 |
| l8-between-curves.json | quiz[3].prose | You want the area between $f$ and $g$ on $[a, b]$. | correct | B12 |
| l8-between-curves.json | quiz[3].question | When does $\int_a^b \big(f(x) - g(x)\big)\,dx$ give that area without splitting? | correct | B12 |
| l8-between-curves.json | quiz[3].widget.options[0] | graded key (choice): When $f(x) \ge g(x)$ for every $x$ in $[a, b]$ | correct | B12 |
| l8-between-curves.json | quiz[3].widget.options[1].text | wrong option, wrong under every convention: When both $f$ and $g$ stay above the axis | correct | B12 |
| l8-between-curves.json | quiz[3].widget.options[1].why | The axis does not matter. If the curves cross, the pieces still cancel. | correct | B12 |
| l8-between-curves.json | quiz[3].widget.options[2].text | wrong option, wrong under every convention: When $f(a) \ge g(a)$ and $f(b) \ge g(b)$ | correct | B12 |
| l8-between-curves.json | quiz[3].widget.options[2].why | The curves can cross twice in between, with $g$ on top for a stretch. | correct | B12 |
| l8-between-curves.json | quiz[3].widget.options[3].text | wrong option, wrong under every convention: Always: a negative piece just means a smaller area | correct | B12 |
| l8-between-curves.json | quiz[3].widget.options[3].why | A negative piece cancels part of a real area. Area is never subtracted from area. | correct | B12 |
| l8-between-curves.json | quiz[3].feedback.correct | If $f$ stays on top throughout, $f - g \ge 0$ and nothing cancels. | correct | B12 |
| l8-between-curves.json | quiz[3].feedback.generic | Not quite right. Ask when $f - g$ could be negative somewhere. | correct | B12 |
| l8-between-curves.json | quiz[3].explain.text | If $f \ge g$ everywhere on $[a, b]$, the integrand $f - g$ is never negative, so nothing cancels. Checking ... | correct | B12 |
| review-2.json | items[0].prose | Let $G(x) = \int_0^x \cos(t^2)\,dt$. | correct | B13 |
| review-2.json | items[0].question | What is $G'(x)$? | correct | B13 |
| review-2.json | items[0].widget.options[0] | graded key (choice): $\cos(x^2)$ | correct | B13 |
| review-2.json | items[0].widget.options[1].text | wrong option, wrong under every convention: $-2x\sin(x^2)$ | correct | B13 |
| review-2.json | items[0].widget.options[1].why | You differentiated the integrand. The theorem hands back the integrand itself, at $x$. | correct | B13 |
| review-2.json | items[0].widget.options[2].text | wrong option, wrong under every convention: $\cos(x^2) - 1$ | correct | B13 |
| review-2.json | items[0].widget.options[2].why | You subtracted the integrand at the lower limit, $\cos 0 = 1$. That is not part of the derivative. | correct | B13 |
| review-2.json | items[0].widget.options[3].text | wrong option, wrong under every convention: $\sin(x^2)$ | correct | B13 |
| review-2.json | items[0].widget.options[3].why | You tried to integrate $\cos(t^2)$ as if it were $\cos t$. No antiderivative is needed here. | correct | B13 |
| review-2.json | items[0].feedback.correct | $\dfrac{d}{dx}\int_0^x \cos(t^2)\,dt = \cos(x^2)$. | correct | B13 |
| review-2.json | items[0].feedback.generic | Not quite right. Apply $\tfrac{d}{dx}\int_a^x f(t)\,dt = f(x)$ directly. | correct | B13 |
| review-2.json | items[0].explain.text | The integrand is continuous, so the fundamental theorem gives $G'(x) = \cos(x^2)$ at once. $G$ has no eleme... | correct | B13 |
| review-2.json | items[1].prose | For $x > 0$, find an antiderivative. | correct | B13 |
| review-2.json | items[1].question | Find $\int \left(3x^2 - \dfrac{4}{x}\right)dx$. Leave out the $+C$. | correct | B13 |
| review-2.json | items[1].widget.answer | graded key (expression): "x^3-4\\ln x" | correct | B13 |
| review-2.json | items[1].widget.wrong[0] | slip power-rule = "x^3+\\frac{2}{x^2}" is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[1].widget.wrong[1] | slip no-divide = "3x^3-4\\ln x" is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[1].widget.wrong[2] | slip derivative = "6x+\\frac{4}{x^2}" is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[1].feedback.correct | $x^3 - 4\ln x$: differentiate to get $3x^2 - \tfrac{4}{x}$. | correct | B13 |
| review-2.json | items[1].feedback.generic | Not quite right. Take each term separately and check by differentiating. | correct | B13 |
| review-2.json | items[1].feedback.byKey.power-rule | You used the power rule on $x^{-1}$ but lowered the power. At $n = -1$ use $\ln x$ instead. | correct | B13 |
| review-2.json | items[1].feedback.byKey.no-divide | You raised the power of $3x^2$ but did not divide by 3. $(3x^3)' = 9x^2$. | correct | B13 |
| review-2.json | items[1].feedback.byKey.derivative | You differentiated. We want the function whose derivative is $3x^2 - \tfrac{4}{x}$. | correct | B13 |
| review-2.json | items[1].explain.text | $\int 3x^2\,dx = x^3$ by the power rule, and $\int \tfrac{4}{x}\,dx = 4\ln x$ for $x > 0$. So the answer is... | correct | B13 |
| review-2.json | items[2].prose | An antiderivative of $\sqrt{x} = x^{1/2}$ is $\tfrac{2}{3}x^{3/2}$. | correct | B13 |
| review-2.json | items[2].question | Evaluate $\int_1^4 \sqrt{x}\,dx$. Give a decimal to 2 places. | correct | B13 |
| review-2.json | items[2].widget.answer | graded key (numeric): 4.67 | correct | B13 |
| review-2.json | items[2].widget.wrong[0] | slip forgot-fa = 5.33 is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[2].widget.wrong[1] | slip heights = 1 is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[2].widget.wrong[2] | slip order = -4.67 is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[2].widget.accept | $\tfrac{14}{3} \approx 4.67$. | correct | B13 |
| review-2.json | items[2].feedback.correct | $\tfrac{2}{3}(8 - 1) = \tfrac{14}{3} \approx 4.67$. | correct | B13 |
| review-2.json | items[2].feedback.generic | Not quite right. Compute $F(4) - F(1)$ with $F(x) = \tfrac{2}{3}x^{3/2}$. | correct | B13 |
| review-2.json | items[2].feedback.byKey.forgot-fa | $\tfrac{16}{3}$ is $F(4)$ alone. Subtract $F(1) = \tfrac{2}{3}$. | correct | B13 |
| review-2.json | items[2].feedback.byKey.heights | You subtracted the heights $\sqrt{4} - \sqrt{1}$. Subtract values of the antiderivative instead. | correct | B13 |
| review-2.json | items[2].feedback.byKey.order | You computed $F(1) - F(4)$. Top limit minus bottom. | correct | B13 |
| review-2.json | items[2].explain.text | $F(4) = \tfrac{2}{3} \times 8 = \tfrac{16}{3}$ and $F(1) = \tfrac{2}{3}$. So the integral is $\tfrac{14}{3}... | correct | B13 |
| review-2.json | items[3].prose | The parabola $y = x^2$ and the line $y = 2x$ enclose a region. | correct | B13 |
| review-2.json | items[3].question | What is its area? Give a decimal to 2 places. | correct | B13 |
| review-2.json | items[3].canvas.params.functions[0].label | $y = 2x$ | correct | B13 |
| review-2.json | items[3].canvas.params.functions[1].label | $y = x^2$ | correct | B13 |
| review-2.json | items[3].widget.answer | graded key (numeric): 1.33 | correct | B13 |
| review-2.json | items[3].widget.wrong[0] | slip upside = -1.33 is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[3].widget.wrong[1] | slip under-line = 4 is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[3].widget.wrong[2] | slip under-para = 2.67 is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[3].widget.accept | $\tfrac{4}{3} \approx 1.33$. | correct | B13 |
| review-2.json | items[3].feedback.correct | $\int_0^2 (2x - x^2)\,dx = 4 - \tfrac{8}{3} = \tfrac{4}{3}$. | correct | B13 |
| review-2.json | items[3].feedback.generic | Not quite right. Find the crossings, then integrate top minus bottom. | correct | B13 |
| review-2.json | items[3].feedback.byKey.upside | You took parabola minus line. On $(0, 2)$ the line is on top. | correct | B13 |
| review-2.json | items[3].feedback.byKey.under-line | 4 is the area under the line alone. Subtract the area under the parabola. | correct | B13 |
| review-2.json | items[3].feedback.byKey.under-para | $\tfrac{8}{3}$ is the area under the parabola. The region lies above it, under the line. | correct | B13 |
| review-2.json | items[3].explain.text | $x^2 = 2x$ at $x = 0$ and $x = 2$, and at $x = 1$ the line is higher. So the area is $\Big[x^2 - \tfrac{x^3... | correct | B13 |
| review-2.json | items[4].prose | A desk's P&L rate is $r(t) = 5 - t$, in £k per hour, over a 10-hour session. Cumulative P&L is $C(x) = \int... | correct | B13 |
| review-2.json | items[4].question | What is the highest cumulative P&L during the session, in £k? | correct | B13 |
| review-2.json | items[4].widget.answer | graded key (numeric): 12.5 | correct | B13 |
| review-2.json | items[4].widget.wrong[0] | slip max-rate = 5 is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[4].widget.wrong[1] | slip end = 0 is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[4].widget.accept | 12.5, at $t = 5$. | correct | B13 |
| review-2.json | items[4].feedback.correct | $C$ peaks where $r$ crosses zero, at $t = 5$: $C(5) = 25 - 12.5 = 12.5$. | correct | B13 |
| review-2.json | items[4].feedback.generic | Not quite right. Find where $C' = r$ turns negative, then evaluate $C$ there. | correct | B13 |
| review-2.json | items[4].feedback.byKey.max-rate | 5 is the highest rate, at the open. Cumulative P&L keeps rising until the rate turns negative. | correct | B13 |
| review-2.json | items[4].feedback.byKey.end | 0 is the P&L at the close. The afternoon losses undid the morning gains; the peak came earlier. | correct | B13 |
| review-2.json | items[4].explain.text | $C'(x) = 5 - x$ is positive before $t = 5$ and negative after, so $C$ peaks at 5. $C(5) = \Big[5t - \tfrac{... | correct | B13 |
| review-2.json | items[5].prose | Undo the chain rule. | correct | B13 |
| review-2.json | items[5].question | What is $\int e^{-2x}\,dx$? | correct | B13 |
| review-2.json | items[5].widget.options[0] | graded key (choice): $-\tfrac{1}{2}e^{-2x} + C$ | correct | B13 |
| review-2.json | items[5].widget.options[1].text | wrong option, wrong under every convention: $-2e^{-2x} + C$ | correct | B13 |
| review-2.json | items[5].widget.options[1].why | You differentiated $e^{-2x}$. Undoing the chain rule divides by $-2$. | correct | B13 |
| review-2.json | items[5].widget.options[2].text | wrong option, wrong under every convention: $\tfrac{1}{2}e^{-2x} + C$ | correct | B13 |
| review-2.json | items[5].widget.options[2].why | You divided by 2, but $k = -2$. Differentiate your answer: you get $-e^{-2x}$. | correct | B13 |
| review-2.json | items[5].widget.options[3].text | wrong option, wrong under every convention: $e^{-2x} + C$ | correct | B13 |
| review-2.json | items[5].widget.options[3].why | You copied the rule for $e^x$. Its derivative is $-2e^{-2x}$. | correct | B13 |
| review-2.json | items[5].feedback.correct | $\left(-\tfrac{1}{2}e^{-2x}\right)' = e^{-2x}$. | correct | B13 |
| review-2.json | items[5].feedback.generic | Not quite right. Use $\int e^{kx}\,dx = \tfrac{e^{kx}}{k} + C$ with $k = -2$. | correct | B13 |
| review-2.json | items[5].explain.text | With $k = -2$, $\int e^{-2x}\,dx = \tfrac{e^{-2x}}{-2} + C$. Check: $\left(-\tfrac{1}{2}e^{-2x}\right)' = -... | correct | B13 |
| review-2.json | items[6].prose | On $(-2, 0)$ the curve $y = x^3$ lies below the axis. | correct | B13 |
| review-2.json | items[6].question | Evaluate $\int_{-2}^{0} x^3\,dx$. | correct | B13 |
| review-2.json | items[6].widget.answer | graded key (numeric): -4 | correct | B13 |
| review-2.json | items[6].widget.wrong[0] | slip sign = 4 is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[6].widget.wrong[1] | slip forgot-fa = 0 is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[6].widget.accept | $-4$: $0 - \tfrac{(-2)^4}{4}$. | correct | B13 |
| review-2.json | items[6].feedback.correct | $0 - \tfrac{16}{4} = -4$. | correct | B13 |
| review-2.json | items[6].feedback.generic | Not quite right. $F(x) = \tfrac{x^4}{4}$; compute $F(0) - F(-2)$. | correct | B13 |
| review-2.json | items[6].feedback.byKey.sign | $(-2)^4 = 16$ is positive, so $F(-2) = 4$ and the answer is $0 - 4$. A curve below the axis gives a negativ... | correct | B13 |
| review-2.json | items[6].feedback.byKey.forgot-fa | 0 is $F(0)$ alone. Subtract $F(-2) = 4$. | correct | B13 |
| review-2.json | items[6].explain.text | $\Big[\tfrac{x^4}{4}\Big]_{-2}^{0} = 0 - 4 = -4$. The sign matches the picture: the curve is below the axis... | correct | B13 |
| review-2.json | items[7].prose | Over one full turn, $0 \le x \le 2\pi$, the curve $y = \sin x$ and the $x$-axis enclose two humps. | correct | B13 |
| review-2.json | items[7].question | What is the total area enclosed? | correct | B13 |
| review-2.json | items[7].widget.answer | graded key (numeric): 4 | correct | B13 |
| review-2.json | items[7].widget.wrong[0] | slip no-split = 0 is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[7].widget.wrong[1] | slip one-hump = 2 is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[7].widget.accept | 4: two humps of area 2. | correct | B13 |
| review-2.json | items[7].feedback.correct | Each hump has area 2, so the total is 4. | correct | B13 |
| review-2.json | items[7].feedback.generic | Not quite right. Split at $\pi$, where the curve crosses the axis. | correct | B13 |
| review-2.json | items[7].feedback.byKey.no-split | You integrated $\sin x$ over the whole turn. The hump below the axis cancelled the one above. Split at $\pi$. | correct | B13 |
| review-2.json | items[7].feedback.byKey.one-hump | 2 is one hump. The second, below the axis, encloses area 2 as well. | correct | B13 |
| review-2.json | items[7].explain.text | $\int_0^{\pi} \sin x\,dx = 2$ and $\int_{\pi}^{2\pi} \sin x\,dx = -2$. Area counts both as positive, so it ... | correct | B13 |
| review-2.json | items[8].prose | A licence pays £5,000 per year, continuously, for 3 years. The continuous discount rate is 6%. | correct | B13 |
| review-2.json | items[8].question | What is its present value $\int_0^3 5000\,e^{-0.06t}\,dt$, in pounds? | correct | B13 |
| review-2.json | items[8].widget.answer | graded key (numeric): 13727.48 | correct | B13 |
| review-2.json | items[8].widget.wrong[0] | slip undiscounted = 15000 is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[8].widget.wrong[1] | slip end-discount = 12529.05 is the value of the named mistake and is not a correct answer | correct | B13 |
| review-2.json | items[8].widget.accept | About £13,727: $\tfrac{5000(1 - e^{-0.18})}{0.06}$, to within 0.1%. | correct | B13 |
| review-2.json | items[8].feedback.correct | About £13,727: that is $\tfrac{5000(1 - e^{-0.18})}{0.06}$. | correct | B13 |
| review-2.json | items[8].feedback.generic | Not quite right. Use $\dfrac{c(1 - e^{-rT})}{r}$ with $c = 5000$, $r = 0.06$, $T = 3$. | correct | B13 |
| review-2.json | items[8].feedback.byKey.undiscounted | £15,000 ignores discounting. Later payments are worth less today. | correct | B13 |
| review-2.json | items[8].feedback.byKey.end-discount | You discounted all £15,000 at year 3. Earlier payments are discounted less. | correct | B13 |
| review-2.json | items[8].explain.text | An antiderivative of $5000e^{-0.06t}$ is $-\tfrac{5000}{0.06}e^{-0.06t}$. So the value is $\tfrac{5000}{0.0... | correct | B13 |
| homework-2.json | items[0].prose | For $x > 0$, find an antiderivative term by term. | correct | B14 |
| homework-2.json | items[0].question | Find $\int \left(4x^3 + 6e^{3x} - \dfrac{2}{x}\right)dx$. Leave out the $+C$. | correct | B14 |
| homework-2.json | items[0].widget.answer | graded key (expression): "x^4+2e^{3x}-2\\ln x" | correct | B14 |
| homework-2.json | items[0].widget.wrong[0] | slip copy-exp = "x^4+6e^{3x}-2\\ln x" is the value of the named mistake and is not a correct answer | correct | B14 |
| homework-2.json | items[0].widget.wrong[1] | slip times-k = "x^4+18e^{3x}-2\\ln x" is the value of the named mistake and is not a correct answer | correct | B14 |
| homework-2.json | items[0].widget.wrong[2] | slip derivative = "12x^2+18e^{3x}+\\frac{2}{x^2}" is the value of the named mistake and is not a correct an... | correct | B14 |
| homework-2.json | items[0].feedback.correct | $x^4 + 2e^{3x} - 2\ln x$, which differentiates back to the integrand. | correct | B14 |
| homework-2.json | items[0].feedback.generic | Not quite right. Integrate each term separately, then differentiate your answer to check. | correct | B14 |
| homework-2.json | items[0].feedback.byKey.copy-exp | You kept $6e^{3x}$ as it was. Its derivative is $18e^{3x}$: divide by 3 to undo the chain rule. | correct | B14 |
| homework-2.json | items[0].feedback.byKey.times-k | You multiplied by 3. Undoing the chain rule divides by 3: $\int 6e^{3x}\,dx = 2e^{3x}$. | correct | B14 |
| homework-2.json | items[0].feedback.byKey.derivative | You differentiated. We want the function whose derivative is the integrand. | correct | B14 |
| homework-2.json | items[0].explain.text | $\int 4x^3\,dx = x^4$, $\int 6e^{3x}\,dx = 6 \times \tfrac{e^{3x}}{3} = 2e^{3x}$ and $\int \tfrac{2}{x}\,dx... | correct | B14 |
| homework-2.json | items[1].prose | Use $F(x) = \tfrac{x^3}{3} + x$. | correct | B14 |
| homework-2.json | items[1].question | Evaluate $\int_{-2}^{1} (x^2 + 1)\,dx$. | correct | B14 |
| homework-2.json | items[1].widget.answer | graded key (numeric): 6 | correct | B14 |
| homework-2.json | items[1].widget.wrong[0] | slip forgot-fa = 1.3333 is the value of the named mistake and is not a correct answer | correct | B14 |
| homework-2.json | items[1].widget.wrong[1] | slip sign-slip = -3.3333 is the value of the named mistake and is not a correct answer | correct | B14 |
| homework-2.json | items[1].widget.wrong[2] | slip order = -6 is the value of the named mistake and is not a correct answer | correct | B14 |
| homework-2.json | items[1].widget.accept | 6: $\tfrac{4}{3} - \left(-\tfrac{14}{3}\right)$. | correct | B14 |
| homework-2.json | items[1].feedback.correct | $\tfrac{4}{3} - \left(-\tfrac{14}{3}\right) = 6$. | correct | B14 |
| homework-2.json | items[1].feedback.generic | Not quite right. Compute $F(1)$ and $F(-2)$ separately, signs and all. | correct | B14 |
| homework-2.json | items[1].feedback.byKey.forgot-fa | $\tfrac{4}{3}$ is $F(1)$ alone. Subtract $F(-2) = -\tfrac{14}{3}$, which adds. | correct | B14 |
| homework-2.json | items[1].feedback.byKey.sign-slip | You subtracted $+\tfrac{14}{3}$. But $F(-2) = -\tfrac{8}{3} - 2 = -\tfrac{14}{3}$, and subtracting a negati... | correct | B14 |
| homework-2.json | items[1].feedback.byKey.order | You computed $F(-2) - F(1)$. Top limit minus bottom. | correct | B14 |
| homework-2.json | items[1].explain.text | $F(1) = \tfrac{1}{3} + 1 = \tfrac{4}{3}$ and $F(-2) = -\tfrac{8}{3} - 2 = -\tfrac{14}{3}$. So the integral ... | correct | B14 |
| homework-2.json | items[2].prose | A function has $F'(x) = \cos x$ and $F(0) = 2$. | correct | B14 |
| homework-2.json | items[2].question | What is $F\left(\tfrac{\pi}{6}\right)$? | correct | B14 |
| homework-2.json | items[2].widget.answer | graded key (numeric): 2.5 | correct | B14 |
| homework-2.json | items[2].widget.wrong[0] | slip no-c = 0.5 is the value of the named mistake and is not a correct answer | correct | B14 |
| homework-2.json | items[2].widget.wrong[1] | slip sign = 1.5 is the value of the named mistake and is not a correct answer | correct | B14 |
| homework-2.json | items[2].widget.accept | 2.5: $F(x) = \sin x + 2$. | correct | B14 |
| homework-2.json | items[2].feedback.correct | $F(x) = \sin x + 2$, so $F\left(\tfrac{\pi}{6}\right) = \tfrac{1}{2} + 2 = 2.5$. | correct | B14 |
| homework-2.json | items[2].feedback.generic | Not quite right. Integrate $\cos x$, then use $F(0) = 2$ to fix $C$. | correct | B14 |
| homework-2.json | items[2].feedback.byKey.no-c | You left out $C$. $F(0) = \sin 0 + C = 2$ gives $C = 2$. | correct | B14 |
| homework-2.json | items[2].feedback.byKey.sign | You used $-\sin x$. The derivative of $\sin x$ is $\cos x$, so no minus sign is needed. | correct | B14 |
| homework-2.json | items[2].explain.text | $F(x) = \sin x + C$, and $F(0) = 0 + C = 2$ gives $C = 2$. So $F\left(\tfrac{\pi}{6}\right) = \tfrac{1}{2} ... | correct | B14 |
| homework-2.json | items[3].prose | A cash flow pays $c$ per year continuously for $T$ years, discounted at a continuous rate $r > 0$. Derive $... | correct | B14 |
| homework-2.json | items[3].question | Put the lines in order. | correct | B14 |
| homework-2.json | items[3].widget.answer | graded key (order): ["anti", "ftc", "simp", "factor"] | correct | B14 |
| homework-2.json | items[3].widget.answer.order | graded order of 4 lines; each line follows from the one above | correct | B14 |
| homework-2.json | items[3].widget.lines[0].text | An antiderivative of $c\,e^{-rt}$ is $-\dfrac{c}{r}e^{-rt}$, undoing the chain rule by dividing by $-r$ | correct | B14 |
| homework-2.json | items[3].widget.lines[1].text | $\int_0^T c\,e^{-rt}\,dt = \left(-\dfrac{c}{r}e^{-rT}\right) - \left(-\dfrac{c}{r}e^{0}\right)$, by $F(T) -... | correct | B14 |
| homework-2.json | items[3].widget.lines[2].text | $= \dfrac{c}{r} - \dfrac{c}{r}e^{-rT}$, since $e^0 = 1$ and subtracting a negative adds | correct | B14 |
| homework-2.json | items[3].widget.lines[3].text | $= \dfrac{c\,(1 - e^{-rT})}{r}$, taking out the common factor $\tfrac{c}{r}$ | correct | B14 |
| homework-2.json | items[3].feedback.correct | Antiderivative, evaluate, simplify, factor. | correct | B14 |
| homework-2.json | items[3].feedback.generic | Not quite right. You need the antiderivative before you can evaluate it at the limits. | correct | B14 |
| homework-2.json | items[3].feedback.byKey.ftc | Evaluating at $T$ and 0 needs the antiderivative first. | correct | B14 |
| homework-2.json | items[3].feedback.byKey.simp | Simplify only after both limits are in. | correct | B14 |
| homework-2.json | items[3].feedback.byKey.factor | Factoring is the last step. | correct | B14 |
| homework-2.json | items[3].explain.text | Dividing by $-r$ undoes the chain rule, and $F(T) - F(0)$ evaluates it. The $-F(0)$ term is $+\tfrac{c}{r}$... | correct | B14 |
| homework-2.json | items[4].prose | Let $G(x) = \int_0^{x^3} e^t\,dt$. The upper limit is $x^3$, not $x$. | correct | B14 |
| homework-2.json | items[4].question | What is $G'(1)$? Give a decimal to 3 places. | correct | B14 |
| homework-2.json | items[4].widget.answer | graded key (numeric): 8.155 | correct | B14 |
| homework-2.json | items[4].widget.wrong[0] | slip no-chain = 2.718 is the value of the named mistake and is not a correct answer | correct | B14 |
| homework-2.json | items[4].widget.wrong[1] | slip value = 1.718 is the value of the named mistake and is not a correct answer | correct | B14 |
| homework-2.json | items[4].widget.accept | $3e \approx 8.155$. | correct | B14 |
| homework-2.json | items[4].feedback.correct | $G'(x) = e^{x^3} \cdot 3x^2$, so $G'(1) = 3e \approx 8.155$. | correct | B14 |
| homework-2.json | items[4].feedback.generic | Not quite right. Write $G(x) = A(x^3)$ with $A(u) = \int_0^u e^t\,dt$, then use the chain rule. | correct | B14 |
| homework-2.json | items[4].feedback.byKey.no-chain | You used $A'(u) = e^u$ at $u = 1$ but forgot the chain rule factor $\tfrac{d}{dx}x^3 = 3x^2$. | correct | B14 |
| homework-2.json | items[4].feedback.byKey.value | $e - 1$ is $G(1)$, the value. We want its derivative. | correct | B14 |
| homework-2.json | items[4].explain.text | $G(x) = A(x^3)$, where $A'(u) = e^u$ by the theorem. The chain rule gives $G'(x) = e^{x^3} \cdot 3x^2$, so ... | correct | B14 |
| homework-2.json | items[5].prose | The curves $y = x^3 - 3x$ and $y = x$ enclose two regions. | correct | B14 |
| homework-2.json | items[5].question | What is the total area enclosed? | correct | B14 |
| homework-2.json | items[5].widget.answer | graded key (numeric): 8 | correct | B14 |
| homework-2.json | items[5].widget.wrong[0] | slip no-split = 0 is the value of the named mistake and is not a correct answer | correct | B14 |
| homework-2.json | items[5].widget.wrong[1] | slip one-piece = 4 is the value of the named mistake and is not a correct answer | correct | B14 |
| homework-2.json | items[5].widget.accept | 8: two pieces of 4. | correct | B14 |
| homework-2.json | items[5].feedback.correct | Two pieces of area 4 each: 8. | correct | B14 |
| homework-2.json | items[5].feedback.generic | Not quite right. Solve $x^3 - 3x = x$ for the crossings, then split. | correct | B14 |
| homework-2.json | items[5].feedback.byKey.no-split | You integrated $x - (x^3 - 3x)$ from $-2$ to 2 in one go. The two pieces cancelled. Split at 0. | correct | B14 |
| homework-2.json | items[5].feedback.byKey.one-piece | 4 is one piece. The curves cross at $-2$, 0 and 2, enclosing two pieces. | correct | B14 |
| homework-2.json | items[5].explain.text | $x^3 - 3x = x$ gives $x(x^2 - 4) = 0$, so $x = -2, 0, 2$. On $(0, 2)$ the line is on top: $\int_0^2 (4x - x... | correct | B14 |
| homework-2.json | items[6].prose | A model gives tomorrow's price $S$ a triangular density: $p(s) = \tfrac{s - 90}{100}$ on $[90, 100]$ and $p... | correct | B14 |
| homework-2.json | items[6].question | What is the expected payoff $\int_{90}^{110} \max(s - 100, 0)\,p(s)\,ds$, in pounds? Give 2 decimal places. | correct | B14 |
| homework-2.json | items[6].widget.answer | graded key (numeric): 1.67 | correct | B14 |
| homework-2.json | items[6].widget.wrong[0] | slip uniform = 2.5 is the value of the named mistake and is not a correct answer | correct | B14 |
| homework-2.json | items[6].widget.wrong[1] | slip at-mean = 0 is the value of the named mistake and is not a correct answer | correct | B14 |
| homework-2.json | items[6].widget.wrong[2] | slip given-pays = 3.33 is the value of the named mistake and is not a correct answer | correct | B14 |
| homework-2.json | items[6].widget.accept | $\tfrac{5}{3} \approx \text{£}1.67$. | correct | B14 |
| homework-2.json | items[6].feedback.correct | $\int_{100}^{110} (s - 100)\tfrac{110 - s}{100}\,ds = \tfrac{5}{3} \approx \text{£}1.67$. | correct | B14 |
| homework-2.json | items[6].feedback.generic | Not quite right. Only $[100, 110]$ contributes. Substitute $u = s - 100$ and integrate $\tfrac{u(10 - u)}{1... | correct | B14 |
| homework-2.json | items[6].feedback.byKey.uniform | £2.50 is the answer for a flat density on $[90, 110]$. This density thins out towards £110, where the call ... | correct | B14 |
| homework-2.json | items[6].feedback.byKey.at-mean | You priced the payoff at the mean price, £100. Average the payoff, not the price. | correct | B14 |
| homework-2.json | items[6].feedback.byKey.given-pays | That is the average payoff given the call pays. It pays only half the time. | correct | B14 |
| homework-2.json | items[6].explain.text | With $u = s - 100$, the integral is $\int_0^{10} \tfrac{u(10 - u)}{100}\,du = \tfrac{1}{100}\Big[5u^2 - \tf... | correct | B14 |
| homework-2.json | items[7].prose | For a constant $k > 0$, the line $y = kx$ and the parabola $y = x^2$ enclose a region of area 36. | correct | B14 |
| homework-2.json | items[7].question | What is $k$? | correct | B14 |
| homework-2.json | items[7].widget.answer | graded key (numeric): 6 | correct | B14 |
| homework-2.json | items[7].widget.wrong[0] | slip line-only = 4.16 is the value of the named mistake and is not a correct answer | correct | B14 |
| homework-2.json | items[7].widget.wrong[1] | slip para-only = 4.762 is the value of the named mistake and is not a correct answer | correct | B14 |
| homework-2.json | items[7].widget.accept | 6: the area is $\tfrac{k^3}{6}$. | correct | B14 |
| homework-2.json | items[7].feedback.correct | The area is $\tfrac{k^3}{6} = 36$, so $k^3 = 216$ and $k = 6$. | correct | B14 |
| homework-2.json | items[7].feedback.generic | Not quite right. Find the crossings in terms of $k$, integrate top minus bottom, then solve. | correct | B14 |
| homework-2.json | items[7].feedback.byKey.line-only | You set the area under the line, $\tfrac{k^3}{2}$, equal to 36. Subtract the area under the parabola. | correct | B14 |
| homework-2.json | items[7].feedback.byKey.para-only | You set the area under the parabola, $\tfrac{k^3}{3}$, equal to 36. The region lies between the curves. | correct | B14 |
| homework-2.json | items[7].explain.text | The curves meet at $x = 0$ and $x = k$, with the line on top between. Area $= \int_0^k (kx - x^2)\,dx = \tf... | correct | B14 |
| homework-2.json | items[8].prompt | Let $f$ be continuous on $[a, b]$ and let $A(x) = \int_a^x f(t)\,dt$. (a) Show that $A'(x) = f(x)$, justify... | correct | B14 |
| homework-2.json | items[8].model | **(a)** Fix $x$ and take $h > 0$. The regions under $f$ from $a$ to $x + h$ and from $a$ to $x$ differ only... | correct | B7 |
| homework-2.json | items[8].rubric[0].text | (a) Writes $A(x + h) - A(x)$ as the integral over the strip $[x, x + h]$. | correct | B7 |
| homework-2.json | items[8].rubric[1].text | (a) Bounds the strip between $m_h\,h$ and $M_h\,h$, using the least and greatest values of $f$ on the strip. | correct | B7 |
| homework-2.json | items[8].rubric[2].text | (a) Divides by $h$ and uses continuity to squeeze the ratio to $f(x)$ as $h \to 0$. | correct | B7 |
| homework-2.json | items[8].rubric[3].text | (b) Shows $(F - A)' = 0$ and concludes $F = A + C$ on the interval. | correct | B7 |
| homework-2.json | items[8].rubric[4].text | (b) Uses $A(a) = 0$ to get $C = F(a)$. | correct | B7 |
| homework-2.json | items[8].rubric[5].text | (b) Concludes $\int_a^b f = A(b) = F(b) - F(a)$. | correct | B7 |
| homework-2.json | items[8].rubric[6].text | (c) Uses the antiderivative $-300{,}000\,e^{-0.04t}$ of $12000\,e^{-0.04t}$ (or the formula $\tfrac{c(1 - e... | correct | B7 |
| homework-2.json | items[8].rubric[7].text | (c) Gets £54,381 (within £5), subtracting $F(0)$ correctly. | correct | B7 |
| homework-2.json | items[8].rubric[8].text | (d) Notes a positive integrand cannot give a negative integral. | correct | B7 |
| homework-2.json | items[8].rubric[9].text | (d) Locates the failure: $f$ and $F$ are undefined at 0, inside $[-1, 1]$. So (b) does not apply, and the a... | correct | B7 |
| homework-2.json | items[9].prompt | Let $f$ be continuous on the whole real line, and let $A(x) = \int_0^x f(t)\,dt$. (a) Prove from the defini... | correct | B14 |
| homework-2.json | items[9].model | **(a)** Fix $x$ and take $h \ne 0$. By the rule for split limits, $\int_0^{x+h} f = \int_0^x f + \int_x^{x+... | correct | B7 |
| homework-2.json | items[9].rubric[0].text | (a) Tick only if all are given. Writes $A(x + h) - A(x) = \int_x^{x+h} f(t)\,dt$ by the split-limits rule. ... | correct | B7 |
| homework-2.json | items[9].rubric[1].text | (b) Writes $G(x) = A(2x) - A(x)$, splitting at 0 or at any fixed point, and gets $G'(x) = 2f(2x) - f(x)$ by... | correct | B7 |
| homework-2.json | items[9].rubric[2].text | (c) Solves $2\varphi(2x) = \varphi(x)$ by any route (for example through $e^{-3x^2/2} = \tfrac12$, or by ta... | correct | B7 |
| homework-2.json | items[9].rubric[3].text | (c) Shows it is a maximum: $G' > 0$ before and $G' < 0$ after, from the sign of $2e^{-3x^2/2} - 1$, or $G''... | correct | B7 |
| homework-2.json | items[9].rubric[4].text | (a) Optional part. Says where continuity is used: for the least and greatest values to exist on the strip, ... | correct | B7 |
| problems-2.json | items[0].prose | Let $f(t) = t^2 - 6t + 8$, which factorises as $(t - 2)(t - 4)$. Its accumulation function is $A(x) = \int_... | correct | B15 |
| problems-2.json | items[0].parts[0].question | What is $A'(3)$? | correct | B15 |
| problems-2.json | items[0].parts[0].widget.answer | graded key (numeric): -1 | correct | B15 |
| problems-2.json | items[0].parts[0].widget.wrong[0] | slip area = 6 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[0].parts[0].widget.wrong[1] | slip derivative-of-f = 0 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[0].parts[0].widget.wrong[2] | slip sign = 1 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[0].parts[0].feedback.correct | By the fundamental theorem, $A'(x) = f(x)$. So $A'(3) = 9 - 18 + 8 = -1$. | correct | B15 |
| problems-2.json | items[0].parts[0].feedback.generic | Not quite. The slope of an accumulation function is the height of the curve at its edge. | correct | B15 |
| problems-2.json | items[0].parts[0].feedback.byKey.area | 6 is $A(3)$, the area built up so far. The slope of $A$ is the height of $f$ at the edge. | correct | B15 |
| problems-2.json | items[0].parts[0].feedback.byKey.derivative-of-f | You differentiated $f$. The theorem says $A' = f$ itself, so evaluate $f(3)$. | correct | B15 |
| problems-2.json | items[0].parts[0].feedback.byKey.sign | At x = 3 the factors are (3 − 2) = 1 and (3 − 4) = −1, so f(3) = −1. A positive 1 loses the sign of the sec... | correct | B15 |
| problems-2.json | items[0].parts[0].explain.text | $\tfrac{d}{dx}\int_0^x f(t)\,dt = f(x)$ for continuous $f$. At $x = 3$, $f(3) = (3 - 2)(3 - 4) = -1$, so $A... | correct | B15 |
| problems-2.json | items[0].parts[1].question | Using $A' = f$, at which $x$ does $A$ have a local maximum? | correct | B15 |
| problems-2.json | items[0].parts[1].widget.answer | graded key (numeric): 2 | correct | B15 |
| problems-2.json | items[0].parts[1].widget.wrong[0] | slip min = 4 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[0].parts[1].widget.wrong[1] | slip vertex = 3 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[0].parts[1].feedback.correct | $A' = f$ changes from positive to negative at $x = 2$, so $A$ peaks there. At 4 it changes back, which give... | correct | B15 |
| problems-2.json | items[0].parts[1].feedback.generic | Not quite. Look for where $f$ changes sign, and in which direction. | correct | B15 |
| problems-2.json | items[0].parts[1].feedback.byKey.min | At $x = 4$, $f$ goes from negative to positive, so $A$ stops falling there: a local minimum. | correct | B15 |
| problems-2.json | items[0].parts[1].feedback.byKey.vertex | At 3, $f$ is lowest, so $A$ falls fastest there. It is not a turning point of $A$. | correct | B15 |
| problems-2.json | items[0].parts[1].explain.text | $A$ rises while $f > 0$ and falls while $f < 0$. $f$ is positive on $(0, 2)$ and negative on $(2, 4)$, so $... | correct | B15 |
| problems-2.json | items[0].parts[2].question | Find an antiderivative $F$ of $f(t) = t^2 - 6t + 8$, in $t$. Leave out the $+C$. | correct | B15 |
| problems-2.json | items[0].parts[2].widget.answer | graded key (expression): "\\frac{t^3}{3}-3t^2+8t" | correct | B15 |
| problems-2.json | items[0].parts[2].widget.wrong[0] | slip old-power = "\\frac{t^3}{2}-6t^2+8t" is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[0].parts[2].widget.wrong[1] | slip no-divide = "t^3-6t^2+8t" is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[0].parts[2].widget.wrong[2] | slip derivative = "2t-6" is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[0].parts[2].feedback.correct | Raise each power by one and divide by the new power: $\tfrac{t^3}{3} - 3t^2 + 8t$. Differentiating gives ba... | correct | B15 |
| problems-2.json | items[0].parts[2].feedback.generic | Not quite. Use the power rule backwards on each term, then differentiate to check. | correct | B15 |
| problems-2.json | items[0].parts[2].feedback.byKey.old-power | You divided by the old power. $t^2$ becomes $\tfrac{t^3}{3}$ and $6t$ becomes $\tfrac{6t^2}{2} = 3t^2$. | correct | B15 |
| problems-2.json | items[0].parts[2].feedback.byKey.no-divide | You raised the powers but did not divide. The derivative of $t^3$ is $3t^2$, not $t^2$. | correct | B15 |
| problems-2.json | items[0].parts[2].feedback.byKey.derivative | That is the derivative of $f$. We want a function whose derivative is $f$. | correct | B15 |
| problems-2.json | items[0].parts[2].explain.text | $\int t^2\,dt = \tfrac{t^3}{3}$, $\int 6t\,dt = 3t^2$ and $\int 8\,dt = 8t$. So $F(t) = \tfrac{t^3}{3} - 3t... | correct | B15 |
| problems-2.json | items[0].parts[3].question | Using $F(t) = \tfrac{t^3}{3} - 3t^2 + 8t$, what is $A(2)$, the value at the local maximum? Give an exact fr... | correct | B15 |
| problems-2.json | items[0].parts[3].widget.answer | graded key (numeric): 6.666666666666667 | correct | B15 |
| problems-2.json | items[0].parts[3].widget.wrong[0] | slip at-four = 5.333333333333333 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[0].parts[3].widget.wrong[1] | slip at-three = 6 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[0].parts[3].widget.wrong[2] | slip old-power = -4 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[0].parts[3].widget.accept | Any form equal to $\tfrac{20}{3}$, or $6.667 \pm 0.0005$ | correct | B15 |
| problems-2.json | items[0].parts[3].feedback.correct | $A(2) = F(2) - F(0) = \tfrac{8}{3} - 12 + 16 = \tfrac{20}{3} \approx 6.667$. | correct | B15 |
| problems-2.json | items[0].parts[3].feedback.generic | Not quite. $A(x) = F(x) - F(0)$; evaluate at $x = 2$. | correct | B15 |
| problems-2.json | items[0].parts[3].feedback.byKey.at-four | That is $A(4)$, the local minimum. The maximum from part 2 is at $x = 2$. | correct | B15 |
| problems-2.json | items[0].parts[3].feedback.byKey.at-three | That is $A(3)$. The maximum is at $x = 2$, where $f$ crosses zero. | correct | B15 |
| problems-2.json | items[0].parts[3].feedback.byKey.old-power | That comes from dividing by the old powers in part 3. With $F(t) = \tfrac{t^3}{3} - 3t^2 + 8t$, $F(2) = \tf... | correct | B15 |
| problems-2.json | items[0].parts[3].explain.text | $A(x) = F(x) - F(0)$ and $F(0) = 0$. So $A(2) = \tfrac{8}{3} - 12 + 16 = \tfrac{20}{3}$. | correct | B15 |
| problems-2.json | items[0].parts[4].question | Part 4 gave $A(2) = \tfrac{20}{3}$ at the local maximum. What is the largest value $A$ takes on $[0, 6]$? G... | correct | B15 |
| problems-2.json | items[0].parts[4].widget.answer | graded key (numeric): 12 | correct | B15 |
| problems-2.json | items[0].parts[4].widget.wrong[0] | slip local = 6.666666666666667 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[0].parts[4].widget.wrong[1] | slip unsigned = 14.666666666666666 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[0].parts[4].widget.accept | 12 | correct | B15 |
| problems-2.json | items[0].parts[4].feedback.correct | $A(6) = F(6) = 72 - 108 + 48 = 12$, which beats $\tfrac{20}{3}$. After $x = 4$, $f > 0$ again and $A$ climb... | correct | B15 |
| problems-2.json | items[0].parts[4].feedback.generic | Not quite. Compare the local maximum with the values at the ends of $[0, 6]$. | correct | B15 |
| problems-2.json | items[0].parts[4].feedback.byKey.local | That is the local maximum. $A$ rises again after $x = 4$, so check the end $x = 6$ too. | correct | B15 |
| problems-2.json | items[0].parts[4].feedback.byKey.unsigned | You counted the dip below the axis as positive. $A$ is a signed area, so the part from 2 to 4 takes away. | correct | B15 |
| problems-2.json | items[0].parts[4].explain.text | The candidates are the turning point $x = 2$ and the ends. $A(0) = 0$, $A(2) = \tfrac{20}{3}$ and $A(6) = 1... | correct | B15 |
| problems-2.json | items[1].prose | After a listing, a share's turnover decays: it trades at a rate $v(t) = 8e^{-0.5t}$, in £m per day, $t$ day... | correct | B15 |
| problems-2.json | items[1].parts[0].question | Find an antiderivative of $8e^{-0.5t}$. Leave out the $+C$. | correct | B15 |
| problems-2.json | items[1].parts[0].widget.answer | graded key (expression): "-16e^{-0.5t}" | correct | B15 |
| problems-2.json | items[1].parts[0].widget.wrong[0] | slip times-k = "-4e^{-0.5t}" is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[1].parts[0].widget.wrong[1] | slip no-k = "8e^{-0.5t}" is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[1].parts[0].widget.wrong[2] | slip sign = "16e^{-0.5t}" is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[1].parts[0].feedback.correct | $\int e^{kt}\,dt = \tfrac{e^{kt}}{k}$ with $k = -0.5$, so $\int 8e^{-0.5t}\,dt = \tfrac{8}{-0.5}e^{-0.5t} =... | correct | B15 |
| problems-2.json | items[1].parts[0].feedback.generic | Not quite. Undo the chain rule: divide by the constant in the exponent. | correct | B15 |
| problems-2.json | items[1].parts[0].feedback.byKey.times-k | You multiplied by $-0.5$. Undoing the chain rule divides by it. | correct | B15 |
| problems-2.json | items[1].parts[0].feedback.byKey.no-k | Differentiate $8e^{-0.5t}$: the chain rule gives $-4e^{-0.5t}$. Divide by $-0.5$ to undo it. | correct | B15 |
| problems-2.json | items[1].parts[0].feedback.byKey.sign | Dividing by $-0.5$ makes it negative. Check: the derivative of $16e^{-0.5t}$ is $-8e^{-0.5t}$. | correct | B15 |
| problems-2.json | items[1].parts[0].explain.text | Divide by the inside constant $-0.5$ to get $-16e^{-0.5t}$. Its derivative is $-16 \times (-0.5)e^{-0.5t} =... | correct | B15 |
| problems-2.json | items[1].parts[1].question | So $T(t) = -16e^{-0.5t} + C$. Using $T(0) = 0$, what is $C$? | correct | B15 |
| problems-2.json | items[1].parts[1].widget.answer | graded key (numeric): 16 | correct | B15 |
| problems-2.json | items[1].parts[1].widget.wrong[0] | slip zero = 0 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[1].parts[1].widget.wrong[1] | slip minus = -16 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[1].parts[1].feedback.correct | $T(0) = -16e^{0} + C = -16 + C$, so $C = 16$. | correct | B15 |
| problems-2.json | items[1].parts[1].feedback.generic | Not quite. Put $t = 0$ into $T(t)$ and set it equal to 0. | correct | B15 |
| problems-2.json | items[1].parts[1].feedback.byKey.zero | At $t = 0$, $e^{0} = 1$, not 0. So $T(0) = -16 + C$. | correct | B15 |
| problems-2.json | items[1].parts[1].feedback.byKey.minus | Solve $-16 + C = 0$: $C = 16$, not $-16$. | correct | B15 |
| problems-2.json | items[1].parts[1].explain.text | A starting value fixes the constant. $-16 + C = 0$ gives $C = 16$, so $T(t) = 16 - 16e^{-0.5t}$. | correct | B15 |
| problems-2.json | items[1].parts[2].question | Using $T(t) = 16 - 16e^{-0.5t}$, how much trades in the first 4 days, in £m? Give a decimal to 2 places. | correct | B15 |
| problems-2.json | items[1].parts[2].widget.answer | graded key (numeric): 13.834635468214197 | correct | B15 |
| problems-2.json | items[1].parts[2].widget.wrong[0] | slip no-c = -2.17 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[1].parts[2].widget.wrong[1] | slip times-k = 3.46 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[1].parts[2].widget.wrong[2] | slip rate = 1.08 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[1].parts[2].widget.accept | $13.83$ (13.84 is accepted too) | correct | B15 |
| problems-2.json | items[1].parts[2].feedback.correct | $T(4) = 16 - 16e^{-2} \approx 16 - 2.17 = 13.83$, so about £13.83m. | correct | B15 |
| problems-2.json | items[1].parts[2].feedback.generic | Not quite. Put $t = 4$ into $T(t)$. | correct | B15 |
| problems-2.json | items[1].parts[2].feedback.byKey.no-c | You left out $C = 16$. $T(4) = F(4) - F(0)$, and $F(0) = -16$ must come off. | correct | B15 |
| problems-2.json | items[1].parts[2].feedback.byKey.times-k | That comes from $-4e^{-0.5t}$ in part 1. With $-16e^{-0.5t}$ the total is $16(1 - e^{-2})$. | correct | B15 |
| problems-2.json | items[1].parts[2].feedback.byKey.rate | That is $v(4)$, the rate on day 4. The turnover so far is the area under the rate. | correct | B15 |
| problems-2.json | items[1].parts[2].explain.text | $T(4) = \int_0^4 8e^{-0.5t}\,dt = \big[-16e^{-0.5t}\big]_0^4 = 16(1 - e^{-2})$. That is about 13.83, so £13... | correct | B15 |
| problems-2.json | items[1].parts[3].question | Using $T(t) = 16 - 16e^{-0.5t}$, after how many days has £12m traded? Give a decimal to 2 places. | correct | B15 |
| problems-2.json | items[1].parts[3].widget.answer | graded key (numeric): 2.772588722239781 | correct | B15 |
| problems-2.json | items[1].parts[3].widget.wrong[0] | slip divided = 0.69 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[1].parts[3].widget.wrong[1] | slip wrong-share = 0.58 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[1].parts[3].widget.accept | $2\ln 4 \approx 2.77$, accepted as $2.77 \pm 0.005$ | correct | B15 |
| problems-2.json | items[1].parts[3].feedback.correct | $16e^{-0.5t} = 4$ gives $e^{-0.5t} = 0.25$, so $t = 2\ln 4 \approx 2.77$ days. | correct | B15 |
| problems-2.json | items[1].parts[3].feedback.generic | Not quite. Set $T(t) = 12$ and solve for $t$ with a logarithm. | correct | B15 |
| problems-2.json | items[1].parts[3].feedback.byKey.divided | You divided $\ln 4$ by 2. From $0.5t = \ln 4$, $t = 2\ln 4$. | correct | B15 |
| problems-2.json | items[1].parts[3].feedback.byKey.wrong-share | You solved $e^{-0.5t} = 0.75$. The part still to trade is $\tfrac{4}{16} = 0.25$ of the £16m. | correct | B15 |
| problems-2.json | items[1].parts[3].explain.text | Set $16 - 16e^{-0.5t} = 12$: $e^{-0.5t} = 0.25$ and $0.5t = \ln 4$. So $t = 2\ln 4 \approx 2.77$ days. | correct | B15 |
| problems-2.json | items[2].prose | The parabola $y = 2x^2$ and the line $y = x + 3$ cross twice. We want the areas they enclose. | correct | B15 |
| problems-2.json | items[2].parts[0].question | Where do they cross? Give both $x$ values as exact decimals, separated by a comma. | correct | B15 |
| problems-2.json | items[2].parts[0].widget.answers | graded key (numeric): [-1, 1.5] | correct | B15 |
| problems-2.json | items[2].parts[0].widget.wrong[0] | slip signs = "1, -1.5" is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[2].parts[0].feedback.correct | $2x^2 = x + 3$ gives $2x^2 - x - 3 = 0$, which is $(2x - 3)(x + 1) = 0$. So $x = -1$ and $x = 1.5$. | correct | B15 |
| problems-2.json | items[2].parts[0].feedback.generic | Not quite. Set the two curves equal and factorise. | correct | B15 |
| problems-2.json | items[2].parts[0].feedback.byKey.signs | Those are the roots of $2x^2 + x - 3$, with the signs swapped. Check: at $x = 1.5$, $2x^2 = 4.5 = x + 3$. | correct | B15 |
| problems-2.json | items[2].parts[0].explain.text | Set the curves equal and factorise: $(2x - 3)(x + 1) = 0$. The crossings are $x = -1$ and $x = \tfrac{3}{2}$. | correct | B15 |
| problems-2.json | items[2].parts[1].question | Between $x = -1$ and $x = 1.5$ the line is on top. What is the area enclosed by the two curves? Give an exa... | correct | B15 |
| problems-2.json | items[2].parts[1].widget.answer | graded key (numeric): 5.208333333333333 | correct | B15 |
| problems-2.json | items[2].parts[1].widget.wrong[0] | slip bottom-top = -5.208333333333333 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[2].parts[1].widget.wrong[1] | slip signs = 3.9583333333333335 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[2].parts[1].widget.wrong[2] | slip line-only = 8.125 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[2].parts[1].widget.accept | Any form equal to $\tfrac{125}{24}$, or $5.208 \pm 0.0005$ | correct | B15 |
| problems-2.json | items[2].parts[1].feedback.correct | $\int_{-1}^{1.5} (x + 3 - 2x^2)\,dx = \Big[\tfrac{x^2}{2} + 3x - \tfrac{2x^3}{3}\Big]_{-1}^{1.5} = 3.375 + ... | correct | B15 |
| problems-2.json | items[2].parts[1].feedback.generic | Not quite. Integrate top minus bottom between the two crossings. | correct | B15 |
| problems-2.json | items[2].parts[1].feedback.byKey.bottom-top | You took parabola minus line. Top minus bottom keeps the area positive. | correct | B15 |
| problems-2.json | items[2].parts[1].feedback.byKey.signs | That uses the crossings $-1.5$ and 1 from the slip in part 1. The crossings are $-1$ and 1.5. | correct | B15 |
| problems-2.json | items[2].parts[1].feedback.byKey.line-only | That is the area under the line alone. Take off the area under the parabola. | correct | B15 |
| problems-2.json | items[2].parts[1].explain.text | Area is top minus bottom between the crossings. The antiderivative $\tfrac{x^2}{2} + 3x - \tfrac{2x^3}{3}$ ... | correct | B15 |
| problems-2.json | items[2].parts[2].question | On $[-2, -1]$ the parabola is on top. What is the area between the curves there? Give an exact fraction, or... | correct | B15 |
| problems-2.json | items[2].parts[2].widget.answer | graded key (numeric): 3.1666666666666665 | correct | B15 |
| problems-2.json | items[2].parts[2].widget.wrong[0] | slip signed = -3.1666666666666665 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[2].parts[2].widget.wrong[1] | slip parabola-only = 4.666666666666667 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[2].parts[2].widget.accept | Any form equal to $\tfrac{19}{6}$, or $3.167 \pm 0.0005$ | correct | B15 |
| problems-2.json | items[2].parts[2].feedback.correct | $\int_{-2}^{-1} (2x^2 - x - 3)\,dx = \Big[\tfrac{2x^3}{3} - \tfrac{x^2}{2} - 3x\Big]_{-2}^{-1} = \tfrac{11}... | correct | B15 |
| problems-2.json | items[2].parts[2].feedback.generic | Not quite. Integrate parabola minus line from $-2$ to $-1$. | correct | B15 |
| problems-2.json | items[2].parts[2].feedback.byKey.signed | You kept line minus parabola. Here the parabola is on top, so the gap is $2x^2 - x - 3$. | correct | B15 |
| problems-2.json | items[2].parts[2].feedback.byKey.parabola-only | That is the area under the parabola alone. Take off the area under the line. | correct | B15 |
| problems-2.json | items[2].parts[2].explain.text | At $x = -2$ the parabola is at 8 and the line at 1, so the parabola is on top. Integrating $2x^2 - x - 3$ f... | correct | B15 |
| problems-2.json | items[2].parts[3].question | Using $\tfrac{125}{24}$ from part 2 and $\tfrac{19}{6}$ from part 3, what is the total area between the cur... | correct | B15 |
| problems-2.json | items[2].parts[3].widget.answer | graded key (numeric): 8.375 | correct | B15 |
| problems-2.json | items[2].parts[3].widget.wrong[0] | slip one-integral = 2.0416666666666665 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[2].parts[3].widget.wrong[1] | slip negative = -2.0416666666666665 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[2].parts[3].widget.accept | Any form equal to $\tfrac{201}{24}$, or $8.375 \pm 0.0005$ | correct | B15 |
| problems-2.json | items[2].parts[3].feedback.correct | Split at the crossing $x = -1$ and add the two areas: $\tfrac{125}{24} + \tfrac{76}{24} = \tfrac{201}{24} =... | correct | B15 |
| problems-2.json | items[2].parts[3].feedback.generic | Not quite. Split at the crossing inside the interval and add the pieces. | correct | B15 |
| problems-2.json | items[2].parts[3].feedback.byKey.one-integral | You took one integral of line minus parabola across the crossing, so the pieces partly cancelled. Split at ... | correct | B15 |
| problems-2.json | items[2].parts[3].feedback.byKey.negative | That is one integral of parabola minus line, which is negative overall. Area counts each piece as positive. | correct | B15 |
| problems-2.json | items[2].parts[3].explain.text | Where the curves cross inside the interval, split there and use top minus bottom on each piece. $\tfrac{125... | correct | B15 |
| problems-2.json | items[3].prose | An ETF issuer creates new units at a rate $f(t) = 12t - 3t^2$, in thousands per hour, $t$ hours into a busy... | correct | B15 |
| problems-2.json | items[3].parts[0].question | How fast is $G$ changing at $x = 2$, in thousands of units per hour? | correct | B15 |
| problems-2.json | items[3].parts[0].widget.answer | graded key (numeric): 3 | correct | B15 |
| problems-2.json | items[3].parts[0].widget.wrong[0] | slip no-redeem = 12 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[3].parts[0].widget.wrong[1] | slip value = -2 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[3].parts[0].feedback.correct | By the fundamental theorem, $G'(x) = f(x) - 9$. At $x = 2$ that is $24 - 12 - 9 = 3$. | correct | B15 |
| problems-2.json | items[3].parts[0].feedback.generic | Not quite. The slope of $G$ is its integrand at the edge. | correct | B15 |
| problems-2.json | items[3].parts[0].feedback.byKey.no-redeem | That is $f(2)$, the creation rate alone. $G$ grows at the creation rate minus the redemption rate. | correct | B15 |
| problems-2.json | items[3].parts[0].feedback.byKey.value | $-2$ is $G(2)$, the change so far. Its rate of change is the integrand at $x = 2$. | correct | B15 |
| problems-2.json | items[3].parts[0].explain.text | $\tfrac{d}{dx}\int_0^x (f(t) - 9)\,dt = f(x) - 9$. At $x = 2$ this is 3, so units outstanding are growing b... | correct | B15 |
| problems-2.json | items[3].parts[1].question | Write $G(x)$ as a polynomial in $x$. | correct | B15 |
| problems-2.json | items[3].parts[1].widget.answer | graded key (expression): "-x^3+6x^2-9x" | correct | B15 |
| problems-2.json | items[3].parts[1].widget.wrong[0] | slip no-redeem = "-x^3+6x^2" is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[3].parts[1].widget.wrong[1] | slip old-power = "-\\frac{3}{2}x^3+12x^2-9x" is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[3].parts[1].feedback.correct | An antiderivative of $12t - 3t^2 - 9$ is $6t^2 - t^3 - 9t$, which is 0 at $t = 0$. So $G(x) = -x^3 + 6x^2 -... | correct | B15 |
| problems-2.json | items[3].parts[1].feedback.generic | Not quite. Integrate $f(t) - 9$ term by term, then evaluate from 0 to $x$. | correct | B15 |
| problems-2.json | items[3].parts[1].feedback.byKey.no-redeem | You left out the redemptions. The integrand is $f(t) - 9$, which adds $-9x$. | correct | B15 |
| problems-2.json | items[3].parts[1].feedback.byKey.old-power | You divided by the old powers. $12t$ gives $6t^2$ and $3t^2$ gives $t^3$. | correct | B15 |
| problems-2.json | items[3].parts[1].explain.text | Integrate term by term: $\int (12t - 3t^2 - 9)\,dt = 6t^2 - t^3 - 9t$. Evaluating from 0 to $x$ gives $G(x)... | correct | B15 |
| problems-2.json | items[3].parts[2].question | Using $G(x) = -x^3 + 6x^2 - 9x$: the integrand $f(t) - 9 = -3(t - 1)(t - 3)$ is negative until $t = 1$. Wha... | correct | B15 |
| problems-2.json | items[3].parts[2].widget.answer | graded key (numeric): -4 | correct | B15 |
| problems-2.json | items[3].parts[2].widget.wrong[0] | slip no-redeem = 5 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[3].parts[2].widget.wrong[1] | slip at-three = 0 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[3].parts[2].widget.wrong[2] | slip sign = 4 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[3].parts[2].feedback.correct | $G(1) = -1 + 6 - 9 = -4$: after one hour there are 4 thousand fewer units. | correct | B15 |
| problems-2.json | items[3].parts[2].feedback.generic | Not quite. Put $x = 1$ into $G(x)$. | correct | B15 |
| problems-2.json | items[3].parts[2].feedback.byKey.no-redeem | That leaves out the $-9x$ that the redemptions bring. | correct | B15 |
| problems-2.json | items[3].parts[2].feedback.byKey.at-three | 0 is $G(3)$. At $x = 1$ redemptions are still ahead. | correct | B15 |
| problems-2.json | items[3].parts[2].feedback.byKey.sign | −1 + 6 − 9 is below zero, because the 9 outweighs the 5. The question asks for a negative number for a fall... | correct | B15 |
| problems-2.json | items[3].parts[2].explain.text | $G(1) = -1 + 6 - 9 = -4$. It is the lowest $G$ goes before hour 3, since $G' < 0$ only on $(0, 1)$ there. | correct | B15 |
| problems-2.json | items[3].parts[3].question | Using $G(x) = -x^3 + 6x^2 - 9x$, how many more units are outstanding after 5 hours than at the start, in th... | correct | B15 |
| problems-2.json | items[3].parts[3].widget.answer | graded key (numeric): -20 | correct | B15 |
| problems-2.json | items[3].parts[3].widget.wrong[0] | slip sign = 20 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[3].parts[3].widget.wrong[1] | slip no-redeem = 25 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[3].parts[3].widget.wrong[2] | slip level = 0 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[3].parts[3].feedback.correct | $G(5) = -125 + 150 - 45 = -20$: there are 20 thousand fewer units. | correct | B15 |
| problems-2.json | items[3].parts[3].feedback.generic | Not quite. Put $x = 5$ into $G(x)$ and keep the sign. | correct | B15 |
| problems-2.json | items[3].parts[3].feedback.byKey.sign | Units have fallen, so $G(5)$ is negative. Keep the sign. | correct | B15 |
| problems-2.json | items[3].parts[3].feedback.byKey.no-redeem | That is the creations alone, with no $-9x$ for the redemptions. The change is $-20$. | correct | B15 |
| problems-2.json | items[3].parts[3].feedback.byKey.level | 0 is $G(3)$. After hour 3, $f(t) < 9$ again and units fall. | correct | B15 |
| problems-2.json | items[3].parts[3].explain.text | $G(5) = -125 + 150 - 45 = -20$. Units are back level at hour 3, then the creation rate drops below 9. | correct | B15 |
| problems-2.json | items[3].parts[4].question | The rate curves $y = f(t)$ and $y = 9$ cross at $t = 1$ and $t = 3$. Using $G(1) = -4$, $G(3) = 0$ and $G(5... | correct | B15 |
| problems-2.json | items[3].parts[4].widget.answer | graded key (numeric): 28 | correct | B15 |
| problems-2.json | items[3].parts[4].widget.wrong[0] | slip net = -20 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[3].parts[4].widget.wrong[1] | slip unsigned-net = 20 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[3].parts[4].widget.wrong[2] | slip missed-middle = 24 is the value of the named mistake and is not a correct answer | correct | B15 |
| problems-2.json | items[3].parts[4].feedback.correct | On each piece take the size of the change in $G$: $4 + 4 + 20 = 28$. | correct | B15 |
| problems-2.json | items[3].parts[4].feedback.generic | Not quite. Split at the crossings and add the size of each piece. | correct | B15 |
| problems-2.json | items[3].parts[4].feedback.byKey.net | $-20$ is the net change, where the pieces cancel. Area counts each piece as positive. | correct | B15 |
| problems-2.json | items[3].parts[4].feedback.byKey.unsigned-net | That is the size of the net change. Split at the crossings and add each piece's area. | correct | B15 |
| problems-2.json | items[3].parts[4].feedback.byKey.missed-middle | You left out the piece from 1 to 3, where the creation rate is on top. It adds 4. | correct | B15 |
| problems-2.json | items[3].parts[4].explain.text | Split at $t = 1$ and $t = 3$: the pieces have areas $\|G(1) - G(0)\| = 4$, $\|G(3) - G(1)\| = 4$ and $\|G(5... | correct | B15 |
| fluency-l6-working-backwards.json | families[0].prompt | Find $\int {a:c}{v}^{{{k}}}\,d{v}$. | correct | B16 |
| fluency-l6-working-backwards.json | families[0].widget.answer | graded key template: {r:frac}{v}^{{{k1}}} with let {"k1": "k + 1", "r": "a/(k + 1)"} | correct | B16 |
| fluency-l6-working-backwards.json | families[0].wrong[0] | slip old-power = {a/k:frac}{v}^{{{k1}}} is the value of the named mistake and differs from the key for ever... | correct | B16 |
| fluency-l6-working-backwards.json | families[0].wrong[0].line | You divided by {k}, the old power. Divide by the new power, {k1}. | correct | B16 |
| fluency-l6-working-backwards.json | families[0].wrong[1] | slip no-divide = {a:c}{v}^{{{k1}}} is the value of the named mistake and differs from the key for every dra... | correct | B16 |
| fluency-l6-working-backwards.json | families[0].wrong[1].line | You raised the power to {k1} but did not divide by {k1}. | correct | B16 |
| fluency-l6-working-backwards.json | families[0].wrong[2] | slip differentiated = {a*k}{v}^{{{k - 1}}} is the value of the named mistake and differs from the key for e... | correct | B16 |
| fluency-l6-working-backwards.json | families[0].wrong[2].line | You differentiated. We want the function whose derivative is ${a:c}{v}^{{{k}}}$. | correct | B16 |
| fluency-l6-working-backwards.json | families[0].solution[0] | Raise the power by one, to {k1}, then divide the coefficient ${a}$ by {k1}. | correct | B16 |
| fluency-l6-working-backwards.json | families[0].solution[1] | So $\int {a:c}{v}^{{{k}}}\,d{v} = {r:frac}{v}^{{{k1}}} + C$. | correct | B16 |
| fluency-l6-working-backwards.json | families[1].prompt | Find $\int ({poly(v; a, b, c)})\,d{v}$. | correct | B16 |
| fluency-l6-working-backwards.json | families[1].widget.answer | graded key template: {poly(v; p, q, c, 0)} with let {"a": "3*p", "b": "2*q"} | correct | B16 |
| fluency-l6-working-backwards.json | families[1].wrong[0] | slip no-divide = {poly(v; a, b, c, 0)} is the value of the named mistake and differs from the key for every... | correct | B16 |
| fluency-l6-working-backwards.json | families[1].wrong[0].line | You raised each power by one but did not divide by the new power. | correct | B16 |
| fluency-l6-working-backwards.json | families[1].wrong[1] | slip constant-left = {poly(v; p, q, 0, 0)}{c:+} is the value of the named mistake and differs from the key ... | correct | B16 |
| fluency-l6-working-backwards.json | families[1].wrong[1].line | The constant {c} integrates to ${c}{v}$, not {c}. | correct | B16 |
| fluency-l6-working-backwards.json | families[1].solution[0] | Integrate term by term: ${a} \div 3 = {p}$ and ${b} \div 2 = {q}$. | correct | B16 |
| fluency-l6-working-backwards.json | families[1].solution[1] | The constant ${c}$ integrates to ${c}{v}$. | correct | B16 |
| fluency-l6-working-backwards.json | families[1].solution[2] | So the answer is ${poly(v; p, q, c, 0)} + C$. | correct | B16 |
| fluency-l6-working-backwards.json | families[2].prompt | Find $\int {c}{v}^{{-{k}}}\,d{v}$. | correct | B16 |
| fluency-l6-working-backwards.json | families[2].widget.answer | graded key template: {-m:c}{v}^{{{e}}} with let {"k1": "k - 1", "c": "m*(k - 1)", "e": "1 - k"} | correct | B16 |
| fluency-l6-working-backwards.json | families[2].wrong[0] | slip power-lowered = {-c/(k + 1):frac}{v}^{{{-k - 1}}} is the value of the named mistake and differs from t... | correct | B16 |
| fluency-l6-working-backwards.json | families[2].wrong[0].line | You lowered the power to {-k - 1}. Raise it by one, to {e}. | correct | B16 |
| fluency-l6-working-backwards.json | families[2].wrong[1] | slip sign-lost = {m:c}{v}^{{{e}}} is the value of the named mistake and differs from the key for every draw... | correct | B16 |
| fluency-l6-working-backwards.json | families[2].wrong[1].line | The new power is {e}, so you divide by {e}, which flips the sign. | correct | B16 |
| fluency-l6-working-backwards.json | families[2].solution[0] | Raise the power by one: ${-k} + 1 = {e}$. Then divide by {e}. | correct | B16 |
| fluency-l6-working-backwards.json | families[2].solution[1] | ${c} \div ({e}) = {-m}$, so $\int {c}{v}^{{-{k}}}\,d{v} = {-m:c}{v}^{{{e}}} + C$. | correct | B16 |
| fluency-l6-working-backwards.json | families[3].prompt | A function has $F'(x) = {c}x^{{{k}}}$ and $F({p}) = {q0}$. Work out $F({r})$. | correct | B16 |
| fluency-l6-working-backwards.json | families[3].widget.answer | graded key template: {ans} with let {"k1": "k + 1", "c": "m*(k + 1)", "fp": "m*p^(k + 1)", "fr": "m*r^(k + ... | correct | B16 |
| fluency-l6-working-backwards.json | families[3].wrong[0] | slip no-constant = {fr} is the value of the named mistake and differs from the key for every draw allowed b... | correct | B16 |
| fluency-l6-working-backwards.json | families[3].wrong[0].line | You left out the constant. Use $F({p}) = {q0}$ to find it first. | correct | B16 |
| fluency-l6-working-backwards.json | families[3].wrong[1] | slip no-divide = {q0 + c*(r^k1 - p^k1)} is the value of the named mistake and differs from the key for ever... | correct | B16 |
| fluency-l6-working-backwards.json | families[3].wrong[1].line | You raised the power to {k1} but did not divide by {k1}. | correct | B16 |
| fluency-l6-working-backwards.json | families[3].solution[0] | $F(x) = {m:c}x^{{{k1}}} + C$. | correct | B16 |
| fluency-l6-working-backwards.json | families[3].solution[1] | $F({p}) = {fp} + C = {q0}$, so $C = {cc}$. | correct | B16 |
| fluency-l6-working-backwards.json | families[3].solution[2] | $F({r}) = {fr}{cc:+} = {ans}$. | correct | B16 |
| fluency-l7-evaluating.json | families[0].prompt | Evaluate $\int_{{{p}}}^{{{q}}} {mono(x; c, k)}\,dx$. | correct | B17 |
| fluency-l7-evaluating.json | families[0].widget.answer | graded key template: {ans} with let {"k1": "k + 1", "c": "m*(k + 1)", "fq": "m*q^(k + 1)", "fp": "m*p^(k + ... | correct | B17 |
| fluency-l7-evaluating.json | families[0].wrong[0] | slip limits-swapped = {-ans} is the value of the named mistake and differs from the key for every draw allo... | correct | B17 |
| fluency-l7-evaluating.json | families[0].wrong[0].line | You worked out $F({p}) - F({q})$. The top limit goes first: $F({q}) - F({p})$. | correct | B17 |
| fluency-l7-evaluating.json | families[0].wrong[1] | slip no-divide = {c*(q^k1 - p^k1)} is the value of the named mistake and differs from the key for every dra... | correct | B17 |
| fluency-l7-evaluating.json | families[0].wrong[1].line | You raised the power to {k1} but did not divide by {k1}. | correct | B17 |
| fluency-l7-evaluating.json | families[0].solution[0] | An antiderivative is $F(x) = {mono(x; m, k1)}$. | correct | B17 |
| fluency-l7-evaluating.json | families[0].solution[1] | $F({q}) - F({p}) = {fq} - {fp:()} = {ans}$. | correct | B17 |
| fluency-l7-evaluating.json | families[1].prompt | Evaluate $\int_{{{p}}}^{{{q}}} ({poly(x; a, b, c)})\,dx$. Give a fraction or a decimal. | correct | B17 |
| fluency-l7-evaluating.json | families[1].widget.answer | graded key template: {ans} with let {"b": "2*h", "fq": "a*q^3/3 + h*q^2 + c*q", "fp": "a*p^3/3 + h*p^2 + c*... | correct | B17 |
| fluency-l7-evaluating.json | families[1].wrong[0] | slip limits-swapped = {-ans} is the value of the named mistake and differs from the key for every draw allo... | correct | B17 |
| fluency-l7-evaluating.json | families[1].wrong[0].line | You worked out $F({p}) - F({q})$. The top limit goes first: $F({q}) - F({p})$. | correct | B17 |
| fluency-l7-evaluating.json | families[1].wrong[1] | slip no-divide = {nodiv} is the value of the named mistake and differs from the key for every draw allowed ... | correct | B17 |
| fluency-l7-evaluating.json | families[1].wrong[1].line | You raised each power by one but did not divide by the new power. | correct | B17 |
| fluency-l7-evaluating.json | families[1].solution[0] | An antiderivative is $F(x) = {poly(x; a/3, h, c, 0)}$. | correct | B17 |
| fluency-l7-evaluating.json | families[1].solution[1] | $F({q}) = {fq:frac}$ and $F({p}) = {fp:frac}$. | correct | B17 |
| fluency-l7-evaluating.json | families[1].solution[2] | So the integral is $F({q}) - F({p}) = {ans:frac}$. | correct | B17 |
| fluency-l7-evaluating.json | families[2].prompt | Evaluate $\displaystyle\int_{{{p}}}^{{{q}}} \frac{{{c}}}{{x^2}}\,dx$. Give a fraction or a decimal. | correct | B17 |
| fluency-l7-evaluating.json | families[2].widget.answer | graded key template: {ans} with let {"ans": "c*(1/p - 1/q)", "low": "c*(1/p^3 - 1/q^3)/3"} | correct | B17 |
| fluency-l7-evaluating.json | families[2].wrong[0] | slip sign-lost = {-ans} is the value of the named mistake and differs from the key for every draw allowed b... | correct | B17 |
| fluency-l7-evaluating.json | families[2].wrong[0].line | An antiderivative of $x^{{-2}}$ is $-x^{{-1}}$: the new power is $-1$, so the sign flips. | correct | B17 |
| fluency-l7-evaluating.json | families[2].wrong[1] | slip power-lowered = {low} is the value of the named mistake and differs from the key for every draw allowe... | correct | B17 |
| fluency-l7-evaluating.json | families[2].wrong[1].line | You lowered the power to $-3$. Raise it by one, to $-1$. | correct | B17 |
| fluency-l7-evaluating.json | families[2].solution[0] | An antiderivative is $F(x) = -\frac{{{c}}}{{x}}$. | correct | B17 |
| fluency-l7-evaluating.json | families[2].solution[1] | $F({q}) - F({p}) = {-c/q:frac} - ({-c/p:frac}) = {ans:frac}$. | correct | B17 |
| fluency-l7-evaluating.json | families[3].prompt | Evaluate $\int_{{0}}^{{{q}}} {c:c}e^{{{k:c}{v}}}\,d{v}$, to 3 decimal places. | correct | B17 |
| fluency-l7-evaluating.json | families[3].widget.answer | graded key template: {ans} with let {"r": "c/k", "kqq": "k*q", "ans": "c/k*(exp(k*q) - 1)", "top": "c/k*exp... | correct | B17 |
| fluency-l7-evaluating.json | families[3].wrong[0] | slip lower-limit-zero = {top} is the value of the named mistake and differs from the key for every draw all... | correct | B17 |
| fluency-l7-evaluating.json | families[3].wrong[0].line | You stopped at $F({q})$. Subtract $F(0)$ as well: $e^0 = 1$, not 0. | correct | B17 |
| fluency-l7-evaluating.json | families[3].wrong[1] | slip no-divide = {nodiv} is the value of the named mistake and differs from the key for every draw allowed ... | correct | B17 |
| fluency-l7-evaluating.json | families[3].wrong[1].line | An antiderivative of $e^{{{k:c}{v}}}$ is $\dfrac{{e^{{{k:c}{v}}}}}{{{k}}}$: divide by {k}. | correct | B17 |
| fluency-l7-evaluating.json | families[3].wrong[2] | slip sign-lost = {-ans} is the value of the named mistake and differs from the key for every draw allowed b... | correct | B17 |
| fluency-l7-evaluating.json | families[3].wrong[2].line | Dividing by ${k}$ makes the factor in front negative: you lost its sign. | correct | B17 |
| fluency-l7-evaluating.json | families[3].solution[0] | An antiderivative is $F({v}) = {r:cfrac}e^{{{k:c}{v}}}$. | correct | B17 |
| fluency-l7-evaluating.json | families[3].solution[1] | $F({q}) - F(0) = {r:cfrac}(e^{{{kqq}}} - 1) \approx {ans:dp3}$. | correct | B17 |
| l9-undo-chain.json | screens[0].prose | The curve is $2x\,e^{x^2}$. We want a function $F$ whose derivative is exactly this. Guess, then differenti... | correct | B18 |
| l9-undo-chain.json | screens[0].canvas.params.functions[0].label | $2x\,e^{x^2}$ | correct | B18 |
| l9-undo-chain.json | screens[0].canvas.state.caption | We want $F$ with $F'(x) = 2x\,e^{x^2}$ | correct | B18 |
| l9-undo-chain.json | screens[0].question | Tap a guess to test it. Find a function whose derivative is $2x\,e^{x^2}$. | correct | B18 |
| l9-undo-chain.json | screens[0].widget.states.s0.tex | \int 2x\,e^{x^2}\,dx = \;? | correct | B18 |
| l9-undo-chain.json | screens[0].widget.states.s0.ops[0].why | Differentiating $x^2 e^{x^2}$ needs the product rule, and that adds a second term. | correct | B18 |
| l9-undo-chain.json | screens[0].widget.states.s0.ops[1].why | Only $e^x$ itself is its own derivative. With $x^2$ in the power, the chain rule brings down $2x$. | correct | B18 |
| l9-undo-chain.json | screens[0].widget.states.g1.tex | \frac{d}{dx}\left(x^2 e^{x^2}\right) = 2x\,e^{x^2} + 2x^3 e^{x^2} | correct | B18 |
| l9-undo-chain.json | screens[0].widget.states.g2.tex | \frac{d}{dx}\left(2x\,e^{x^2}\right) = 2e^{x^2} + 4x^2 e^{x^2} | correct | B18 |
| l9-undo-chain.json | screens[0].widget.states.g3.tex | \frac{d}{dx}\,e^{x^2} = e^{x^2} \cdot 2x | correct | B18 |
| l9-undo-chain.json | screens[0].widget.states.s1.tex | \int 2x\,e^{x^2}\,dx = e^{x^2} + C | correct | B18 |
| l9-undo-chain.json | screens[0].hints[0].text | Which guess, differentiated with the chain rule, gives back exactly $2x\,e^{x^2}$? | correct | B18 |
| l9-undo-chain.json | screens[0].hints[1].text | The inside of $e^{x^2}$ is $x^2$, and its derivative is $2x$. | correct | B18 |
| l9-undo-chain.json | screens[0].hints[2].text | Guess $F = e^{x^2}$. The chain rule gives $e^{x^2} \cdot 2x$, which is the curve. | correct | B18 |
| l9-undo-chain.json | screens[0].feedback.correct | $e^{x^2}$ differentiates to $e^{x^2} \cdot 2x$, the curve exactly. | correct | B18 |
| l9-undo-chain.json | screens[0].feedback.generic | Not quite right. Differentiate each guess and compare it with $2x\,e^{x^2}$. | correct | B18 |
| l9-undo-chain.json | screens[0].feedback.byKey.g1 | You integrated each factor on its own. The product rule then adds $2x^3 e^{x^2}$, so the guess overshoots. | correct | B18 |
| l9-undo-chain.json | screens[0].feedback.byKey.g2 | You treated $e^{x^2}$ like $e^x$. Its derivative brings down a $2x$, so the guess gives two extra terms. | correct | B18 |
| l9-undo-chain.json | screens[0].explain.text | You checked $e^{x^2}$ by differentiating it: the outside gives $e^{x^2}$, the inside gives $2x$. So $2x\,e^... | correct | B18 |
| l9-undo-chain.json | screens[0].explain.canvas.functions[0].label | $F = e^{x^2}$ | correct | B18 |
| l9-undo-chain.json | screens[0].explain.canvas.points[0].label | (1, 5.44) | correct | B18 |
| l9-undo-chain.json | screens[1].prose | If $e^{x^2}$ undoes the curve, the fundamental theorem says the area from 0 to $b$ is $F(b) - F(0)$. Slide ... | correct | B18 |
| l9-undo-chain.json | screens[1].canvas.params.functions[0].label | $2x\,e^{x^2}$ | correct | B18 |
| l9-undo-chain.json | screens[1].canvas.derive.caption | Area from 0 to {{b}}: {{fixed(exp(b*b) - 1, 3)}}. Value of $e^{b^2}$: {{fixed(exp(b*b), 3)}} | correct | B18 |
| l9-undo-chain.json | screens[1].question | Which expression gives the area from 0 to $b$? | correct | B18 |
| l9-undo-chain.json | screens[1].widget.options[0] | graded key (choice): $e^{b^2} - 1$ | correct | B18 |
| l9-undo-chain.json | screens[1].widget.options[1].text | wrong option, wrong under every convention: $e^{b^2}$ | correct | B18 |
| l9-undo-chain.json | screens[1].widget.options[1].why | The two numbers in the caption always differ by 1. That 1 is $e^{0^2}$, the value of $F$ at the left end. | correct | B18 |
| l9-undo-chain.json | screens[1].widget.options[2].text | wrong option, wrong under every convention: $2b\,e^{b^2}$ | correct | B18 |
| l9-undo-chain.json | screens[1].widget.options[2].why | That is the height of the curve at $b$, not the area up to $b$. At $b = 1$ the height is 5.44 but the area ... | correct | B18 |
| l9-undo-chain.json | screens[1].hints[0].text | Read both numbers in the caption for two values of $b$. What is the gap? | correct | B18 |
| l9-undo-chain.json | screens[1].hints[1].text | The gap is the same every time. | correct | B18 |
| l9-undo-chain.json | screens[1].hints[2].text | The area is always 1 less than $e^{b^2}$, and $e^{0} = 1$. | correct | B18 |
| l9-undo-chain.json | screens[1].feedback.correct | The area is $e^{b^2} - e^{0} = e^{b^2} - 1$. | correct | B18 |
| l9-undo-chain.json | screens[1].feedback.generic | Not quite right. Compare the area with $e^{b^2}$ for a few values of $b$. | correct | B18 |
| l9-undo-chain.json | screens[1].feedback.byKey.no-lower | You used $F(b)$ alone. The area is $F(b) - F(0)$, and $F(0) = e^0 = 1$. | correct | B18 |
| l9-undo-chain.json | screens[1].explain.text | The area always sat 1 below $e^{b^2}$. That is $F(b) - F(0)$ with $F = e^{x^2}$ and $F(0) = 1$. At $b = 1$ ... | correct | B18 |
| l9-undo-chain.json | screens[2].prose | What you spotted has a name: **substitution**. Call the inside $u = x^2$. Then $du = 2x\,dx$, so the factor... | correct | B18 |
| l9-undo-chain.json | screens[2].canvas.params.rows | [["Inside", "$x^2$", "$u$"], ["Inside's derivative", "$2x\\,dx$", "$du$"], ["Outside", "$\\cos(x^2)$", "$\\... | correct | B18 |
| l9-undo-chain.json | screens[2].question | Use $u = x^2$. Complete $\int 2x\cos(x^2)\,dx = \;? + C$. | correct | B18 |
| l9-undo-chain.json | screens[2].widget.answer | graded key (expression): "\\sin(x^2)" | correct | B18 |
| l9-undo-chain.json | screens[2].widget.wrong[0] | slip sign = "-\\sin(x^2)" is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | screens[2].widget.wrong[1] | slip kept-2x = "x^2\\sin(x^2)" is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | screens[2].widget.wrong[2] | slip left-u = "\\sin u" is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | screens[2].hints[0].text | In $u$ the integral is $\int \cos u\,du$. What is that? | correct | B18 |
| l9-undo-chain.json | screens[2].hints[1].text | $\int \cos u\,du = \sin u + C$. | correct | B18 |
| l9-undo-chain.json | screens[2].hints[2].text | Now put $u = x^2$ back: $\sin(x^2) + C$. | correct | B18 |
| l9-undo-chain.json | screens[2].feedback.correct | $\int \cos u\,du = \sin u$, and $u = x^2$ gives $\sin(x^2)$. | correct | B18 |
| l9-undo-chain.json | screens[2].feedback.generic | Not quite right. Integrate $\cos u$ with respect to $u$, then put $u = x^2$ back. | correct | B18 |
| l9-undo-chain.json | screens[2].feedback.byKey.sign | You added a minus sign. $\sin$ differentiates to $\cos$, so $\int \cos u\,du = \sin u$ with a plus sign. | correct | B18 |
| l9-undo-chain.json | screens[2].feedback.byKey.kept-2x | You integrated the $2x$ as well. In $u$ language $2x\,dx$ is $du$; it is used up, not integrated again. | correct | B18 |
| l9-undo-chain.json | screens[2].feedback.byKey.left-u | That is the answer in $u$. The question is in $x$, so put $u = x^2$ back. | correct | B18 |
| l9-undo-chain.json | screens[2].explain.text | In $u$ the integral is $\int \cos u\,du = \sin u + C$. Putting $u = x^2$ back gives $\sin(x^2) + C$. Check:... | correct | B18 |
| l9-undo-chain.json | screens[3].prose | Now $\int x\,e^{x^2}\,dx$. The same $u = x^2$ gives $du = 2x\,dx$, but the integral holds only $x\,dx$: the... | correct | B18 |
| l9-undo-chain.json | screens[3].canvas.params.rows | [["Inside", "$x^2$", "$u$"], ["Inside's derivative", "$2x\\,dx$", "$du$"], ["What we have", "$x\\,dx$", "?"]] | correct | B18 |
| l9-undo-chain.json | screens[3].canvas.state.caption | Half of $2x\,dx$ is here | correct | B18 |
| l9-undo-chain.json | screens[3].question | Complete $\int x\,e^{x^2}\,dx = \;? + C$. | correct | B18 |
| l9-undo-chain.json | screens[3].widget.answer | graded key (expression): "\\frac{1}{2}e^{x^2}" | correct | B18 |
| l9-undo-chain.json | screens[3].widget.wrong[0] | slip forgot-half = "e^{x^2}" is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | screens[3].widget.wrong[1] | slip doubled = "2e^{x^2}" is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | screens[3].hints[0].text | Write $x\,dx$ in terms of $du$. | correct | B18 |
| l9-undo-chain.json | screens[3].hints[1].text | $du = 2x\,dx$, so $x\,dx = \tfrac{1}{2}\,du$. | correct | B18 |
| l9-undo-chain.json | screens[3].hints[2].text | $\int x\,e^{x^2}\,dx = \tfrac{1}{2}\int e^u\,du = \tfrac{1}{2}e^u + C$. | correct | B18 |
| l9-undo-chain.json | screens[3].feedback.correct | $x\,dx = \tfrac{1}{2}\,du$, so the answer is $\tfrac{1}{2}e^{x^2} + C$. | correct | B18 |
| l9-undo-chain.json | screens[3].feedback.generic | Not quite right. Write $x\,dx$ as a multiple of $du$ first. | correct | B18 |
| l9-undo-chain.json | screens[3].feedback.byKey.forgot-half | You treated $x\,dx$ as the whole of $du$. It is half of it, so a $\tfrac{1}{2}$ comes out in front. | correct | B18 |
| l9-undo-chain.json | screens[3].feedback.byKey.doubled | You multiplied by 2 to make up the missing factor. $x\,dx$ is half of $du$, so divide by 2 instead. | correct | B18 |
| l9-undo-chain.json | screens[3].explain.text | Since $du = 2x\,dx$, the $x\,dx$ we have is $\tfrac{1}{2}\,du$. So the integral is $\tfrac{1}{2}\int e^u\,d... | correct | B18 |
| l9-undo-chain.json | screens[4].prose | The inside need not sit in a power. In $\displaystyle\int \frac{2x}{x^2 + 1}\,dx$ the bottom's derivative i... | correct | B18 |
| l9-undo-chain.json | screens[4].canvas.params.rows | [["Inside", "$x^2 + 1$", "$u$"], ["Inside's derivative", "$2x\\,dx$", "$du$"], ["What is left", "$\\dfrac{1... | correct | B18 |
| l9-undo-chain.json | screens[4].canvas.state.caption | With $u = x^2 + 1$ the integral becomes $\int \frac{1}{u}\,du$ | correct | B18 |
| l9-undo-chain.json | screens[4].question | Complete $\displaystyle\int \frac{2x}{x^2 + 1}\,dx = \;? + C$. | correct | B18 |
| l9-undo-chain.json | screens[4].widget.answer | graded key (expression): "\\ln(x^2+1)" | correct | B18 |
| l9-undo-chain.json | screens[4].widget.wrong[0] | slip kept-2x = "2x\\ln(x^2+1)" is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | screens[4].widget.wrong[1] | slip split = "\\frac{x^2}{\\frac{x^3}{3}+x}" is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | screens[4].hints[0].text | What is $\int \frac{1}{u}\,du$? | correct | B18 |
| l9-undo-chain.json | screens[4].hints[1].text | $\int \frac{1}{u}\,du = \ln\|u\| + C$. | correct | B18 |
| l9-undo-chain.json | screens[4].hints[2].text | $u = x^2 + 1$ is always positive, so the answer is $\ln(x^2 + 1) + C$. | correct | B18 |
| l9-undo-chain.json | screens[4].feedback.correct | $\int \frac{du}{u} = \ln u$, so the answer is $\ln(x^2 + 1) + C$. | correct | B18 |
| l9-undo-chain.json | screens[4].feedback.generic | Not quite right. Rewrite the integral as $\int \frac{1}{u}\,du$ first. | correct | B18 |
| l9-undo-chain.json | screens[4].feedback.byKey.kept-2x | You left the $2x$ outside. It became $du$, so nothing multiplies the logarithm. | correct | B18 |
| l9-undo-chain.json | screens[4].feedback.byKey.split | You integrated the top and the bottom separately. A fraction does not integrate that way; use $u = x^2 + 1$. | correct | B18 |
| l9-undo-chain.json | screens[4].explain.text | With $u = x^2 + 1$, the top $2x\,dx$ is $du$ and the integral is $\int \frac{1}{u}\,du = \ln u$. Since $x^2... | correct | B18 |
| l9-undo-chain.json | screens[4].explain.canvas.highlight.rows | [1, 2] | correct | B18 |
| l9-undo-chain.json | screens[5].prose | Try the same move on $\displaystyle\int e^{x^2}\,dx$, with no $2x$ in front. | correct | B18 |
| l9-undo-chain.json | screens[5].canvas.params.rows | [["Inside", "$x^2$", "$u$"], ["Inside's derivative", "$2x\\,dx$", "$du$"], ["What we have", "$dx$", "$\\dfr... | correct | B18 |
| l9-undo-chain.json | screens[5].question | What does $u = x^2$ do to $\int e^{x^2}\,dx$? | correct | B18 |
| l9-undo-chain.json | screens[5].widget.options[0] | graded key (choice): It fails: an $x$ is left over, and $du$ cannot absorb it | correct | B18 |
| l9-undo-chain.json | screens[5].widget.options[1].text | wrong option, wrong under every convention: It gives $\dfrac{e^{x^2}}{2x} + C$ | correct | B18 |
| l9-undo-chain.json | screens[5].widget.options[1].why | You divided by $2x$ as if it were a constant. Differentiate $\tfrac{e^{x^2}}{2x}$: the quotient rule gives ... | correct | B18 |
| l9-undo-chain.json | screens[5].widget.options[2].text | wrong option, wrong under every convention: It gives $e^{x^2} + C$ | correct | B18 |
| l9-undo-chain.json | screens[5].widget.options[2].why | Differentiate $e^{x^2}$: the chain rule gives $2x\,e^{x^2}$. Without a $2x$ in the integral, that is not a ... | correct | B18 |
| l9-undo-chain.json | screens[5].hints[0].text | Write $dx$ in terms of $du$. Is anything in $x$ left? | correct | B18 |
| l9-undo-chain.json | screens[5].hints[1].text | $dx = \tfrac{du}{2x}$, and $2x$ is not a constant. | correct | B18 |
| l9-undo-chain.json | screens[5].hints[2].text | The integral becomes $\int \frac{e^u}{2x}\,du$, still with an $x$ in it. Substitution has not helped. | correct | B18 |
| l9-undo-chain.json | screens[5].feedback.correct | This direct substitution needs the inside's derivative to be present, up to a constant. Here it is not. | correct | B18 |
| l9-undo-chain.json | screens[5].feedback.generic | Not quite right. Write $dx$ in $u$ language and look at what is left. | correct | B18 |
| l9-undo-chain.json | screens[5].feedback.byKey.divide | You divided by $2x$ as if it were a constant. Differentiate your answer to see it fail. | correct | B18 |
| l9-undo-chain.json | screens[5].explain.text | You found $dx = \tfrac{du}{2x}$, which leaves an $x$ behind. A constant can be moved outside an integral, b... | correct | B18 |
| l9-undo-chain.json | screens[6].prose | Now a definite integral: $\displaystyle\int_0^2 2x\,e^{x^2}\,dx$, the shaded area on the top graph. With $u... | correct | B18 |
| l9-undo-chain.json | screens[6].canvas.left.params.functions[0].label | $2x\,e^{x^2}$ | correct | B18 |
| l9-undo-chain.json | screens[6].question | Evaluate $\displaystyle\int_0^2 2x\,e^{x^2}\,dx$ to 3 decimal places. | correct | B18 |
| l9-undo-chain.json | screens[6].widget.answer | graded key (numeric): 53.598 | correct | B18 |
| l9-undo-chain.json | screens[6].widget.wrong[0] | slip kept-limits = 6.389 is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | screens[6].widget.wrong[1] | slip top-only = 54.598 is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | screens[6].widget.accept | $e^4 - 1 \approx 53.598$: when $x$ runs from 0 to 2, $u = x^2$ runs from 0 to 4. | correct | B18 |
| l9-undo-chain.json | screens[6].hints[0].text | When $x = 2$, what is $u$? | correct | B18 |
| l9-undo-chain.json | screens[6].hints[1].text | The $u$ limits are $0^2$ and $2^2$. | correct | B18 |
| l9-undo-chain.json | screens[6].hints[2].text | $\int_0^4 e^u\,du = e^4 - e^0 = e^4 - 1$. | correct | B18 |
| l9-undo-chain.json | screens[6].feedback.correct | $\int_0^4 e^u\,du = e^4 - 1 \approx 53.598$. | correct | B18 |
| l9-undo-chain.json | screens[6].feedback.generic | Not quite right. Change the limits to $u$ values before you evaluate. | correct | B18 |
| l9-undo-chain.json | screens[6].feedback.byKey.kept-limits | You switched to $u$ but kept the $x$ limits 0 and 2. When $x = 2$, $u = 4$, so the $u$-integral runs from 0... | correct | B18 |
| l9-undo-chain.json | screens[6].feedback.byKey.top-only | You evaluated $e^u$ at the top only. At the bottom $e^0 = 1$, so subtract it. | correct | B18 |
| l9-undo-chain.json | screens[6].explain.text | When $x$ runs from 0 to 2, $u = x^2$ runs from 0 to 4. So the integral is $\int_0^4 e^u\,du = e^4 - 1 \appr... | correct | B18 |
| l9-undo-chain.json | screens[7].prose | You have been running the chain rule backwards. Put the reasons in order, from the chain rule to the rule w... | imprecise | Finding 11: the rule is derived with no hypotheses; it needs g' continuous on [a,b] and f continuous on the range of g (Stewart 5.5 thm 6, Spivak ch. 19 thm 2) |
| l9-undo-chain.json | screens[7].question | Put the lines of the derivation in order. | correct | B18 |
| l9-undo-chain.json | screens[7].widget.answer | graded key (order): ["anti", "chain", "ftc", "limits"] | correct | B18 |
| l9-undo-chain.json | screens[7].widget.answer.order | graded order of 4 lines; each line follows from the one above | correct | B18 |
| l9-undo-chain.json | screens[7].widget.lines[0].text | Let $F$ be an antiderivative of $f$, so $F' = f$ | correct | B18 |
| l9-undo-chain.json | screens[7].widget.lines[1].text | Chain rule: $\dfrac{d}{dx}F(g(x)) = f(g(x))\,g'(x)$ | correct | B18 |
| l9-undo-chain.json | screens[7].widget.lines[2].text | So $\int_a^b f(g(x))\,g'(x)\,dx = F(g(b)) - F(g(a))$, by the fundamental theorem | correct | B18 |
| l9-undo-chain.json | screens[7].widget.lines[3].text | And $F(g(b)) - F(g(a)) = \int_{g(a)}^{g(b)} f(u)\,du$, the integral in $u$ with new limits | correct | B18 |
| l9-undo-chain.json | screens[7].hints[0].text | Name the antiderivative before you differentiate anything. | correct | B18 |
| l9-undo-chain.json | screens[7].hints[1].text | The chain rule line needs $F' = f$. | correct | B18 |
| l9-undo-chain.json | screens[7].hints[2].text | Antiderivative, chain rule, then evaluate with the fundamental theorem, then read the result as an integral... | correct | B18 |
| l9-undo-chain.json | screens[7].feedback.correct | Each line uses the one before: $F' = f$, then the chain rule, then the fundamental theorem twice. | correct | B18 |
| l9-undo-chain.json | screens[7].feedback.generic | Not quite right. Start by naming $F$, and end with the integral in $u$. | correct | B18 |
| l9-undo-chain.json | screens[7].feedback.byKey.limits | The $u$-integral is the last reading of $F(g(b)) - F(g(a))$. It needs the line before it. | correct | B18 |
| l9-undo-chain.json | screens[7].feedback.byKey.ftc | The fundamental theorem needs an antiderivative of $f(g(x))\,g'(x)$. The chain rule line supplies it. | correct | B18 |
| l9-undo-chain.json | screens[7].explain.text | By the chain rule $F(g(x))$ is an antiderivative of $f(g(x))\,g'(x)$; the theorem evaluates it at $a$ and $... | correct | B18 |
| l9-undo-chain.json | screens[8].prose | A price path $S(t)$ has instantaneous return $\dfrac{S'(t)}{S(t)}$ per year. Over one year this stock went ... | correct | B18 |
| l9-undo-chain.json | screens[8].canvas.state.points[0].label | £100 | correct | B18 |
| l9-undo-chain.json | screens[8].canvas.state.points[1].label | £125 | correct | B18 |
| l9-undo-chain.json | screens[8].question | Find $\displaystyle\int_0^1 \frac{S'(t)}{S(t)}\,dt$, the return added up over the year. Give 4 decimal places. | correct | B18 |
| l9-undo-chain.json | screens[8].widget.answer | graded key (numeric): 0.2231 | correct | B18 |
| l9-undo-chain.json | screens[8].widget.wrong[0] | slip simple = 0.25 is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | screens[8].widget.wrong[1] | slip no-lower = 4.8283 is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | screens[8].widget.accept | $\ln 125 - \ln 100 = \ln 1.25 \approx 0.2231$. | correct | B18 |
| l9-undo-chain.json | screens[8].hints[0].text | Try $u = S(t)$. What is $du$? | correct | B18 |
| l9-undo-chain.json | screens[8].hints[1].text | $du = S'(t)\,dt$, so the integral is $\int \frac{1}{u}\,du$. | correct | B18 |
| l9-undo-chain.json | screens[8].hints[2].text | The $u$ limits are $S(0) = 100$ and $S(1) = 125$. So the answer is $\ln 125 - \ln 100$. | correct | B18 |
| l9-undo-chain.json | screens[8].feedback.correct | $\ln \tfrac{125}{100} \approx 0.2231$, the log return. | correct | B18 |
| l9-undo-chain.json | screens[8].feedback.generic | Not quite right. Substitute $u = S(t)$ and change the limits to prices. | correct | B18 |
| l9-undo-chain.json | screens[8].feedback.byKey.simple | That is the simple return $\tfrac{125 - 100}{100}$. Adding up instantaneous returns gives the log return, $... | correct | B18 |
| l9-undo-chain.json | screens[8].feedback.byKey.no-lower | You took $\ln 125$ only. The $u$-integral starts at $S(0) = 100$, so subtract $\ln 100$. | correct | B18 |
| l9-undo-chain.json | screens[8].explain.text | With $u = S(t)$ and $du = S'(t)\,dt$, the integral is $\int_{100}^{125} \frac{du}{u} = \ln 1.25 \approx 0.2... | correct | B18 |
| l9-undo-chain.json | summary.ideas[0] | A factor that is the derivative of an inside function marks a chain-rule output. | correct | B18 |
| l9-undo-chain.json | summary.ideas[1] | Set $u$ to the inside, turn $g'(x)\,dx$ into $du$, and fix any constant factor. | correct | B18 |
| l9-undo-chain.json | summary.ideas[2] | For a definite integral, move the limits to $u$ values, or substitute back before evaluating. | correct | B18 |
| l9-undo-chain.json | summary.formula.name | Substitution | correct | B18 |
| l9-undo-chain.json | summary.formula.tex | \int_a^b f(g(x))\,g'(x)\,dx = \int_{g(a)}^{g(b)} f(u)\,du | correct | B18 |
| l9-undo-chain.json | summary.formula.note | Used this way, it needs $g'(x)$ in the integral, up to a constant factor. | correct | B18 |
| l9-undo-chain.json | summary.trap | Keeping the $x$ limits after switching to $u$. As $x$ runs from 0 to 2, $u = x^2$ runs from 0 to 4. | correct | B18 |
| l9-undo-chain.json | quiz[0].prose | Use substitution on $\displaystyle\int 3x^2 \cos(x^3)\,dx$. | correct | B18 |
| l9-undo-chain.json | quiz[0].question | Complete $\int 3x^2\cos(x^3)\,dx = \;? + C$. | correct | B18 |
| l9-undo-chain.json | quiz[0].widget.answer | graded key (expression): "\\sin(x^3)" | correct | B18 |
| l9-undo-chain.json | quiz[0].widget.wrong[0] | slip sign = "-\\sin(x^3)" is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | quiz[0].widget.wrong[1] | slip kept-factor = "x^3\\sin(x^3)" is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | quiz[0].feedback.correct | With $u = x^3$, $du = 3x^2\,dx$ and $\int \cos u\,du = \sin u$. | correct | B18 |
| l9-undo-chain.json | quiz[0].feedback.generic | Not quite right. Take $u = x^3$ and look for $du$ in the integral. | correct | B18 |
| l9-undo-chain.json | quiz[0].feedback.byKey.sign | $\sin$ differentiates to $\cos$, so $\int \cos u\,du = \sin u$ with a plus sign. | correct | B18 |
| l9-undo-chain.json | quiz[0].feedback.byKey.kept-factor | You integrated $3x^2$ as well. It is $du$, so it is used up. | correct | B18 |
| l9-undo-chain.json | quiz[0].explain.text | Set $u = x^3$, so $du = 3x^2\,dx$ is exactly the rest. Then $\int \cos u\,du = \sin u + C = \sin(x^3) + C$. | correct | B18 |
| l9-undo-chain.json | quiz[1].prose | Evaluate $\displaystyle\int_0^1 x(x^2 + 1)^3\,dx$ with $u = x^2 + 1$. | correct | B18 |
| l9-undo-chain.json | quiz[1].question | What is the value? Give it as a decimal. | correct | B18 |
| l9-undo-chain.json | quiz[1].widget.answer | graded key (numeric): 1.875 | correct | B18 |
| l9-undo-chain.json | quiz[1].widget.wrong[0] | slip forgot-half = 3.75 is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | quiz[1].widget.wrong[1] | slip kept-limits = 0.125 is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | quiz[1].widget.accept | $\tfrac{15}{8} = 1.875$. | correct | B18 |
| l9-undo-chain.json | quiz[1].feedback.correct | $\tfrac{1}{2}\int_1^2 u^3\,du = \tfrac{1}{2} \cdot \tfrac{16 - 1}{4} = \tfrac{15}{8}$. | correct | B18 |
| l9-undo-chain.json | quiz[1].feedback.generic | Not quite right. Find $x\,dx$ in terms of $du$, and the new limits. | correct | B18 |
| l9-undo-chain.json | quiz[1].feedback.byKey.forgot-half | You used $x\,dx = du$. Since $du = 2x\,dx$, it is $\tfrac{1}{2}\,du$. | correct | B18 |
| l9-undo-chain.json | quiz[1].feedback.byKey.kept-limits | You kept the limits 0 and 1. When $x$ runs from 0 to 1, $u = x^2 + 1$ runs from 1 to 2. | correct | B18 |
| l9-undo-chain.json | quiz[1].explain.text | $du = 2x\,dx$, so $x\,dx = \tfrac{1}{2}\,du$, and $u$ runs from 1 to 2. The integral is $\tfrac{1}{2}\int_1... | correct | B18 |
| l9-undo-chain.json | quiz[2].prose | Sam evaluates $\displaystyle\int_0^1 2x(x^2 + 1)^2\,dx$. Sam sets $u = x^2 + 1$, finds $\tfrac{u^3}{3}$, th... | correct | B18 |
| l9-undo-chain.json | quiz[2].question | What is the correct value? Give 3 decimal places. | correct | B18 |
| l9-undo-chain.json | quiz[2].widget.answer | graded key (numeric): 2.3333 | correct | B18 |
| l9-undo-chain.json | quiz[2].widget.wrong[0] | slip sams = 0.3333 is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | quiz[2].widget.wrong[1] | slip upper-only = 2.6667 is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | quiz[2].widget.accept | $\tfrac{7}{3} \approx 2.333$. | correct | B18 |
| l9-undo-chain.json | quiz[2].feedback.correct | $\int_1^2 u^2\,du = \tfrac{8 - 1}{3} = \tfrac{7}{3}$. | correct | B18 |
| l9-undo-chain.json | quiz[2].feedback.generic | Not quite right. Either change the limits to $u$ values, or put $u = x^2 + 1$ back first. | correct | B18 |
| l9-undo-chain.json | quiz[2].feedback.byKey.sams | That is Sam's answer. Sam plugged the $x$ limits into a function of $u$; $u$ runs from 1 to 2. | correct | B18 |
| l9-undo-chain.json | quiz[2].feedback.byKey.upper-only | You evaluated $\tfrac{u^3}{3}$ at $u = 2$ only. Subtract its value at $u = 1$. | correct | B18 |
| l9-undo-chain.json | quiz[2].explain.text | When $x$ runs from 0 to 1, $u$ runs from 1 to 2. So the value is $\left[\tfrac{u^3}{3}\right]_1^2 = \tfrac{... | correct | B18 |
| l9-undo-chain.json | quiz[3].prose | Find $\displaystyle\int \frac{\ln x}{x}\,dx$ for $x > 0$. | correct | B18 |
| l9-undo-chain.json | quiz[3].question | Complete $\displaystyle\int \frac{\ln x}{x}\,dx = \;? + C$. | correct | B18 |
| l9-undo-chain.json | quiz[3].widget.answer | graded key (expression): "\\frac{1}{2}(\\ln x)^2" | correct | B18 |
| l9-undo-chain.json | quiz[3].widget.wrong[0] | slip forgot-half = "(\\ln x)^2" is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | quiz[3].widget.wrong[1] | slip log-log = "\\ln(\\ln x)" is the value of the named mistake and is not a correct answer | correct | B18 |
| l9-undo-chain.json | quiz[3].feedback.correct | With $u = \ln x$, $du = \tfrac{1}{x}\,dx$, and $\int u\,du = \tfrac{u^2}{2}$. | correct | B18 |
| l9-undo-chain.json | quiz[3].feedback.generic | Not quite right. Try $u = \ln x$: what is $du$? | correct | B18 |
| l9-undo-chain.json | quiz[3].feedback.byKey.forgot-half | Differentiate $(\ln x)^2$: you get $\tfrac{2\ln x}{x}$, twice too much. $\int u\,du = \tfrac{u^2}{2}$. | correct | B18 |
| l9-undo-chain.json | quiz[3].feedback.byKey.log-log | You treated it as $\int \frac{du}{u}$. With $u = \ln x$ the integral is $\int u\,du$, not $\int \frac{1}{u}... | correct | B18 |
| l9-undo-chain.json | quiz[3].explain.text | The inside is $u = \ln x$, and its derivative $\tfrac{1}{x}$ is the other factor. So the integral is $\int ... | correct | B18 |
| l10-undo-product.json | screens[0].prose | The curve is $x\,e^x$. By the product rule, $\dfrac{d}{dx}(x\,e^x) = e^x + x\,e^x$. That is the curve plus ... | correct | B19 |
| l10-undo-product.json | screens[0].canvas.state.caption | We want $F$ with $F'(x) = x\,e^x$ | correct | B19 |
| l10-undo-product.json | screens[0].question | Which function has derivative exactly $x\,e^x$? | correct | B19 |
| l10-undo-product.json | screens[0].widget.options[0].text | wrong option, wrong under every convention: $\dfrac{x^2}{2}\,e^x$ | correct | B19 |
| l10-undo-product.json | screens[0].widget.options[0].why | You integrated each factor. The product rule then gives $x\,e^x + \tfrac{x^2}{2}e^x$, one term too many. | correct | B19 |
| l10-undo-product.json | screens[0].widget.options[1].text | wrong option, wrong under every convention: $x\,e^x$ | correct | B19 |
| l10-undo-product.json | screens[0].widget.options[1].why | Its derivative is $e^x + x\,e^x$. There is an extra $e^x$ still to remove. | correct | B19 |
| l10-undo-product.json | screens[0].widget.options[2].text | wrong option, wrong under every convention: $(x + 1)\,e^x$ | correct | B19 |
| l10-undo-product.json | screens[0].widget.options[2].why | Its derivative is $e^x + (x + 1)e^x = (x + 2)e^x$. You added the $e^x$ instead of taking it away. | correct | B19 |
| l10-undo-product.json | screens[0].widget.options[3] | graded key (choice): $(x - 1)\,e^x$ | correct | B19 |
| l10-undo-product.json | screens[0].hints[0].text | Start from $x\,e^x$, whose derivative overshoots by $e^x$. What would cancel that $e^x$? | correct | B19 |
| l10-undo-product.json | screens[0].hints[1].text | $e^x$ is its own derivative. Subtracting $e^x$ from $F$ subtracts $e^x$ from $F'$. | correct | B19 |
| l10-undo-product.json | screens[0].hints[2].text | $\frac{d}{dx}(x\,e^x - e^x) = e^x + x\,e^x - e^x = x\,e^x$. | correct | B19 |
| l10-undo-product.json | screens[0].feedback.correct | $(x - 1)e^x$ differentiates to $e^x + (x - 1)e^x = x\,e^x$. | correct | B19 |
| l10-undo-product.json | screens[0].feedback.generic | Not quite right. Differentiate each option with the product rule and compare it with $x\,e^x$. | correct | B19 |
| l10-undo-product.json | screens[0].explain.text | You started from $x\,e^x$ and took away the $e^x$ its derivative gave too much. So $\int x\,e^x\,dx = x\,e^... | correct | B19 |
| l10-undo-product.json | screens[0].explain.canvas.functions[0].label | $F = (x - 1)e^x$ | correct | B19 |
| l10-undo-product.json | screens[0].explain.canvas.points[0].label | (1, 2.72) | correct | B19 |
| l10-undo-product.json | screens[1].prose | Here $u$ runs across and $v = u^2$ runs up. Blue is the area under the curve. Orange lies between the curve... | correct | B19 |
| l10-undo-product.json | screens[1].canvas.params.functions[0].label | $v = u^2$ | correct | B19 |
| l10-undo-product.json | screens[1].canvas.state.vlines[0].label | $u = b$ | correct | B19 |
| l10-undo-product.json | screens[1].canvas.derive.caption | Blue: {{fixed(b*b*b/3, 3)}}. Orange: {{fixed(2*b*b*b/3, 3)}}. | correct | B19 |
| l10-undo-product.json | screens[1].question | Whatever $b$ is, what do the blue and orange areas add up to? | correct | B19 |
| l10-undo-product.json | screens[1].widget.options[0] | graded key (choice): $b \times b^2$, the rectangle they fill together | correct | B19 |
| l10-undo-product.json | screens[1].widget.options[1].text | wrong option, wrong under every convention: $b^2$, the height of the rectangle | correct | B19 |
| l10-undo-product.json | screens[1].widget.options[1].why | That is the height only. At $b = 2$ the areas are 2.667 and 5.333, which add to 8, not 4. | correct | B19 |
| l10-undo-product.json | screens[1].widget.options[2].text | wrong option, wrong under every convention: $\dfrac{b^3}{3}$ | correct | B19 |
| l10-undo-product.json | screens[1].widget.options[2].why | That is the blue area alone. Orange is twice as big, so the total is three times blue. | correct | B19 |
| l10-undo-product.json | screens[1].hints[0].text | Add the two numbers in the caption for $b = 2$. | correct | B19 |
| l10-undo-product.json | screens[1].hints[1].text | Together the two regions fill a rectangle. | correct | B19 |
| l10-undo-product.json | screens[1].hints[2].text | At $b = 2$ the total is 8, and the rectangle is 2 wide and 4 tall. | correct | B19 |
| l10-undo-product.json | screens[1].feedback.correct | Blue plus orange fills the rectangle $b \times b^2$ exactly. | correct | B19 |
| l10-undo-product.json | screens[1].feedback.generic | Not quite right. Add the two areas for a couple of values of $b$. | correct | B19 |
| l10-undo-product.json | screens[1].explain.text | Blue and orange always fill the rectangle with corner $(b, b^2)$. At $b = 2$ that is $\tfrac{8}{3} + \tfrac... | correct | B19 |
| l10-undo-product.json | screens[1].explain.canvas.vlines[0].label | $u = 2$ | correct | B19 |
| l10-undo-product.json | screens[2].prose | In the picture, blue is $\int v\,du$ and orange is $\int u\,dv$. They fill the rectangle $uv$, so $$\int u\... | correct | B19 |
| l10-undo-product.json | screens[2].canvas.params.rows | [["$u$", "$x$", "$du = dx$"], ["$dv$", "$\\cos x\\,dx$", "$v = \\sin x$"]] | correct | B19 |
| l10-undo-product.json | screens[2].question | Complete $\int x\cos x\,dx = \;? + C$. | correct | B19 |
| l10-undo-product.json | screens[2].widget.answer | graded key (expression): "x\\sin x+\\cos x" | correct | B19 |
| l10-undo-product.json | screens[2].widget.wrong[0] | slip sign = "x\\sin x-\\cos x" is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | screens[2].widget.wrong[1] | slip both = "\\frac{x^2}{2}\\sin x" is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | screens[2].widget.wrong[2] | slip no-integral = "x\\sin x" is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | screens[2].hints[0].text | Write $uv$ first, then the integral $\int v\,du$. | correct | B19 |
| l10-undo-product.json | screens[2].hints[1].text | $uv = x\sin x$ and $\int v\,du = \int \sin x\,dx$. | correct | B19 |
| l10-undo-product.json | screens[2].hints[2].text | $\int \sin x\,dx = -\cos x$, so $x\sin x - (-\cos x) = x\sin x + \cos x$. | correct | B19 |
| l10-undo-product.json | screens[2].feedback.correct | $x\sin x - \int \sin x\,dx = x\sin x + \cos x + C$. | correct | B19 |
| l10-undo-product.json | screens[2].feedback.generic | Not quite right. Use $uv - \int v\,du$ with the table's entries. | correct | B19 |
| l10-undo-product.json | screens[2].feedback.byKey.sign | You lost a sign. $\int \sin x\,dx = -\cos x$, and subtracting it gives $+\cos x$. | correct | B19 |
| l10-undo-product.json | screens[2].feedback.byKey.both | You integrated both factors. Parts differentiates $u$ and integrates only $dv$. | correct | B19 |
| l10-undo-product.json | screens[2].feedback.byKey.no-integral | You stopped at $uv$. Subtract $\int v\,du = \int \sin x\,dx$ as well. | correct | B19 |
| l10-undo-product.json | screens[2].explain.text | $uv = x\sin x$, and $\int v\,du = \int \sin x\,dx = -\cos x$. So $\int x\cos x\,dx = x\sin x + \cos x + C$.... | correct | B19 |
| l10-undo-product.json | screens[3].prose | For $\int x\ln x\,dx$ we must choose which factor is $u$. The table sets out both options. | correct | B19 |
| l10-undo-product.json | screens[3].canvas.params.rows | [["$u$", "$x$", "$\\ln x$"], ["$dv$", "$\\ln x\\,dx$", "$x\\,dx$"], ["$du$", "$dx$", "$\\tfrac{1}{x}\\,dx$"... | correct | B19 |
| l10-undo-product.json | screens[3].question | Which option should we use? | correct | B19 |
| l10-undo-product.json | screens[3].widget.options[0].text | wrong option, wrong under every convention: Option A: $u = x$ | correct | B19 |
| l10-undo-product.json | screens[3].widget.options[0].why | With $u = x$ you need $v = \int \ln x\,dx$ before you can start. That is harder than the integral you began... | imprecise | Finding 6: int ln x dx is not harder than int x ln x dx; it needs parts itself (screen 5) and the route then loops |
| l10-undo-product.json | screens[3].widget.options[1] | graded key (choice): Option B: $u = \ln x$ | correct | B19 |
| l10-undo-product.json | screens[3].widget.options[2].text | wrong option, wrong under every convention: Either works equally well | correct | B19 |
| l10-undo-product.json | screens[3].widget.options[2].why | Option A cannot even fill in $v$ without a harder integral. The choice matters. | correct | B19 |
| l10-undo-product.json | screens[3].hints[0].text | Which factor gets simpler when you differentiate it? | correct | B19 |
| l10-undo-product.json | screens[3].hints[1].text | $\ln x$ differentiates to $\tfrac{1}{x}$, and $x$ is easy to integrate. | correct | B19 |
| l10-undo-product.json | screens[3].hints[2].text | With option B, $\int v\,du = \int \tfrac{x^2}{2} \cdot \tfrac{1}{x}\,dx = \int \tfrac{x}{2}\,dx$, which is ... | correct | B19 |
| l10-undo-product.json | screens[3].feedback.correct | $\ln x$ gets simpler when differentiated, and $x$ is easy to integrate. | correct | B19 |
| l10-undo-product.json | screens[3].feedback.generic | Not quite right. Pick the $u$ that gets simpler when you differentiate it. | correct | B19 |
| l10-undo-product.json | screens[3].feedback.byKey.a | You chose $u = x$. Then $v$ is $\int \ln x\,dx$, which is harder than where you started. | imprecise | Finding 6: as the option line |
| l10-undo-product.json | screens[3].explain.text | Option B gives $uv = \tfrac{x^2}{2}\ln x$ and $\int v\,du = \int \tfrac{x}{2}\,dx = \tfrac{x^2}{4}$. So $\i... | correct | B19 |
| l10-undo-product.json | screens[4].prose | Option B gave $\int x\ln x\,dx = \tfrac{x^2}{2}\ln x - \tfrac{x^2}{4} + C$. Now use it between limits, with... | correct | B19 |
| l10-undo-product.json | screens[4].canvas.params.rows | [["$uv$", "$\\tfrac{x^2}{2}\\ln x$"], ["$\\int v\\,du$", "$\\tfrac{x^2}{4}$"]] | correct | B19 |
| l10-undo-product.json | screens[4].canvas.state.caption | Antiderivative: $\tfrac{x^2}{2}\ln x - \tfrac{x^2}{4}$ | correct | B19 |
| l10-undo-product.json | screens[4].question | Evaluate $\displaystyle\int_1^e x\ln x\,dx$ to 3 decimal places. | correct | B19 |
| l10-undo-product.json | screens[4].widget.answer | graded key (numeric): 2.0973 | correct | B19 |
| l10-undo-product.json | screens[4].widget.wrong[0] | slip lower = 1.8473 is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | screens[4].widget.wrong[1] | slip no-integral = 3.6945 is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | screens[4].widget.accept | $\tfrac{e^2 + 1}{4} \approx 2.097$. | correct | B19 |
| l10-undo-product.json | screens[4].hints[0].text | Evaluate $\tfrac{x^2}{2}\ln x - \tfrac{x^2}{4}$ at $e$, then at 1. | correct | B19 |
| l10-undo-product.json | screens[4].hints[1].text | At $e$: $\tfrac{e^2}{2} - \tfrac{e^2}{4} = \tfrac{e^2}{4}$. At 1: $0 - \tfrac{1}{4}$. | correct | B19 |
| l10-undo-product.json | screens[4].hints[2].text | $\tfrac{e^2}{4} - \left(-\tfrac{1}{4}\right) = \tfrac{e^2 + 1}{4}$. | correct | B19 |
| l10-undo-product.json | screens[4].feedback.correct | $\tfrac{e^2}{4} + \tfrac{1}{4} \approx 2.097$. | correct | B19 |
| l10-undo-product.json | screens[4].feedback.generic | Not quite right. Evaluate the whole antiderivative at both limits and subtract. | correct | B19 |
| l10-undo-product.json | screens[4].feedback.byKey.lower | You treated the value at $x = 1$ as 0. The $\ln$ term vanishes there, but $-\tfrac{x^2}{4}$ gives $-\tfrac{... | correct | B19 |
| l10-undo-product.json | screens[4].feedback.byKey.no-integral | You evaluated $uv$ alone. Subtract the $\int v\,du$ part, $\tfrac{x^2}{4}$, between the limits too. | correct | B19 |
| l10-undo-product.json | screens[4].explain.text | At $x = e$ the antiderivative is $\tfrac{e^2}{2} - \tfrac{e^2}{4} = \tfrac{e^2}{4}$. At $x = 1$ it is $-\tf... | correct | B19 |
| l10-undo-product.json | screens[4].explain.canvas.highlight.rows | [1] | correct | B19 |
| l10-undo-product.json | screens[5].prose | $\int \ln x\,dx$ has only one factor. Write it as $\ln x \cdot 1$: take $u = \ln x$ and $dv = dx$. | correct | B19 |
| l10-undo-product.json | screens[5].canvas.params.rows | [["$u$", "$\\ln x$", "$du = \\tfrac{1}{x}\\,dx$"], ["$dv$", "$dx$", "$v = x$"]] | correct | B19 |
| l10-undo-product.json | screens[5].canvas.state.caption | The hidden factor is 1 | correct | B19 |
| l10-undo-product.json | screens[5].question | Complete $\int \ln x\,dx = \;? + C$. | correct | B19 |
| l10-undo-product.json | screens[5].widget.answer | graded key (expression): "x\\ln x-x" | correct | B19 |
| l10-undo-product.json | screens[5].widget.wrong[0] | slip derivative = "\\frac{1}{x}" is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | screens[5].widget.wrong[1] | slip no-integral = "x\\ln x" is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | screens[5].hints[0].text | Write $uv - \int v\,du$ with the table's entries. | correct | B19 |
| l10-undo-product.json | screens[5].hints[1].text | $uv = x\ln x$, and $\int v\,du = \int x \cdot \tfrac{1}{x}\,dx$. | correct | B19 |
| l10-undo-product.json | screens[5].hints[2].text | $\int x \cdot \tfrac{1}{x}\,dx = \int 1\,dx = x$. So the answer is $x\ln x - x$. | correct | B19 |
| l10-undo-product.json | screens[5].feedback.correct | $x\ln x - \int 1\,dx = x\ln x - x + C$. | correct | B19 |
| l10-undo-product.json | screens[5].feedback.generic | Not quite right. Use $uv - \int v\,du$ with $u = \ln x$ and $v = x$. | correct | B19 |
| l10-undo-product.json | screens[5].feedback.byKey.derivative | That is the derivative of $\ln x$. We want a function whose derivative is $\ln x$. | correct | B19 |
| l10-undo-product.json | screens[5].feedback.byKey.no-integral | You stopped at $uv$. Subtract $\int v\,du = \int 1\,dx = x$ as well. | correct | B19 |
| l10-undo-product.json | screens[5].explain.text | $uv = x\ln x$ and $\int v\,du = \int 1\,dx = x$. So $\int \ln x\,dx = x\ln x - x + C$. Check: $\ln x + x \c... | correct | B19 |
| l10-undo-product.json | screens[6].prose | For $\int x^2 e^x\,dx$, take $u = x^2$. One round of parts lowers the power to $x^1$, so we need a second r... | correct | B19 |
| l10-undo-product.json | screens[6].canvas.params.rows | [["Round 1", "$u = x^2$, $dv = e^x\\,dx$", "$x^2 e^x - \\int 2x\\,e^x\\,dx$"], ["Round 2", "$u = 2x$, $dv =... | correct | B19 |
| l10-undo-product.json | screens[6].question | Complete $\int x^2 e^x\,dx = \;? + C$. | correct | B19 |
| l10-undo-product.json | screens[6].widget.answer | graded key (expression): "(x^2-2x+2)e^x" | correct | B19 |
| l10-undo-product.json | screens[6].widget.wrong[0] | slip sign = "(x^2-2x-2)e^x" is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | screens[6].widget.wrong[1] | slip one-round = "(x^2-2x)e^x" is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | screens[6].hints[0].text | Round 2 gives $\int 2x\,e^x\,dx = 2x\,e^x - \int 2e^x\,dx$. | correct | B19 |
| l10-undo-product.json | screens[6].hints[1].text | So $\int 2x\,e^x\,dx = 2x\,e^x - 2e^x$. | correct | B19 |
| l10-undo-product.json | screens[6].hints[2].text | $x^2 e^x - (2x\,e^x - 2e^x) = x^2 e^x - 2x\,e^x + 2e^x$. | correct | B19 |
| l10-undo-product.json | screens[6].feedback.correct | $x^2 e^x - 2x\,e^x + 2e^x = (x^2 - 2x + 2)e^x$. | correct | B19 |
| l10-undo-product.json | screens[6].feedback.generic | Not quite right. Do round 2 fully, then subtract its whole result. | correct | B19 |
| l10-undo-product.json | screens[6].feedback.byKey.sign | You subtracted the bracket $2x\,e^x - 2e^x$ but changed only one sign. Minus $-2e^x$ is $+2e^x$. | correct | B19 |
| l10-undo-product.json | screens[6].feedback.byKey.one-round | You replaced $\int 2x\,e^x\,dx$ by $2x\,e^x$. That integral needs its own round of parts. | correct | B19 |
| l10-undo-product.json | screens[6].explain.text | Round 2 gives $\int 2x\,e^x\,dx = 2x\,e^x - 2e^x$. Subtracting it from $x^2 e^x$ gives $(x^2 - 2x + 2)e^x +... | correct | B19 |
| l10-undo-product.json | screens[7].prose | Alex tries $\int x\,e^x\,dx$ the other way round, with $u = e^x$ and $dv = x\,dx$. That gives $\tfrac{x^2}{... | correct | B19 |
| l10-undo-product.json | screens[7].canvas.params.rows | [["$u$", "$e^x$", "$du = e^x\\,dx$"], ["$dv$", "$x\\,dx$", "$v = \\tfrac{x^2}{2}$"]] | correct | B19 |
| l10-undo-product.json | screens[7].canvas.state.caption | Alex's new integral: $\int \tfrac{x^2}{2}e^x\,dx$ | correct | B19 |
| l10-undo-product.json | screens[7].question | What should Alex do next? | correct | B19 |
| l10-undo-product.json | screens[7].widget.options[0].text | wrong option, wrong under every convention: Do parts again on $\int \tfrac{x^2}{2}e^x\,dx$ with $u = e^x$ | correct | B19 |
| l10-undo-product.json | screens[7].widget.options[0].why | Each round with $u = e^x$ raises the power of $x$ once more. The integrals get worse forever. | correct | B19 |
| l10-undo-product.json | screens[7].widget.options[1].text | wrong option, wrong under every convention: Stop: the answer is $\tfrac{x^2}{2}e^x$ | correct | B19 |
| l10-undo-product.json | screens[7].widget.options[1].why | You dropped the second term. Differentiate $\tfrac{x^2}{2}e^x$ and you get $x\,e^x + \tfrac{x^2}{2}e^x$. | correct | B19 |
| l10-undo-product.json | screens[7].widget.options[2] | graded key (choice): Start again with $u = x$, which gets simpler when differentiated | correct | B19 |
| l10-undo-product.json | screens[7].hints[0].text | Is $\int \tfrac{x^2}{2}e^x\,dx$ easier or harder than $\int x\,e^x\,dx$? | correct | B19 |
| l10-undo-product.json | screens[7].hints[1].text | The power of $x$ went up, from 1 to 2. | correct | B19 |
| l10-undo-product.json | screens[7].hints[2].text | Differentiating $x$ gives 1; differentiating $e^x$ gives $e^x$ again. Only $u = x$ makes the power fall. | correct | B19 |
| l10-undo-product.json | screens[7].feedback.correct | With $u = x$ the power of $x$ falls to 0, and the new integral is $\int e^x\,dx$. | correct | B19 |
| l10-undo-product.json | screens[7].feedback.generic | Not quite right. Compare the new integral with the one Alex started from. | correct | B19 |
| l10-undo-product.json | screens[7].feedback.byKey.again | You kept $u = e^x$. Differentiating $e^x$ does not simplify it, and integrating $x$ raises its power, so ea... | correct | B19 |
| l10-undo-product.json | screens[7].feedback.byKey.stop | You kept $uv$ and dropped $\int v\,du$. Parts always leaves that second integral to do. | correct | B19 |
| l10-undo-product.json | screens[7].explain.text | Alex chose $u = e^x$, which differentiating leaves unchanged, and integrated $x$ into $\tfrac{x^2}{2}$. The... | correct | B19 |
| l10-undo-product.json | screens[7].explain.canvas.highlight.rows | [0, 1] | correct | B19 |
| l10-undo-product.json | screens[8].prose | The rectangle picture has an algebra version. Start from the product rule for $u(x)\,v(x)$ and reach the fo... | correct | B19 |
| l10-undo-product.json | screens[8].question | Put the lines of the derivation in order. | correct | B19 |
| l10-undo-product.json | screens[8].widget.answer | graded key (order): ["prod", "integ", "rearr", "short"] | correct | B19 |
| l10-undo-product.json | screens[8].widget.answer.order | graded order of 4 lines; each line follows from the one above | correct | B19 |
| l10-undo-product.json | screens[8].widget.lines[0].text | Product rule: $(uv)' = u'v + uv'$ | correct | B19 |
| l10-undo-product.json | screens[8].widget.lines[1].text | Integrate both sides: $uv = \int u'v\,dx + \int uv'\,dx$, since integrating $(uv)'$ gives back $uv$ | correct | B19 |
| l10-undo-product.json | screens[8].widget.lines[2].text | Subtract $\int u'v\,dx$ from both sides: $\int uv'\,dx = uv - \int u'v\,dx$ | correct | B19 |
| l10-undo-product.json | screens[8].widget.lines[3].text | Write $dv = v'\,dx$ and $du = u'\,dx$: $\int u\,dv = uv - \int v\,du$ | correct | B19 |
| l10-undo-product.json | screens[8].hints[0].text | Which line is a rule you already know from differentiation? | correct | B19 |
| l10-undo-product.json | screens[8].hints[1].text | Integrating the product rule comes before any rearranging. | correct | B19 |
| l10-undo-product.json | screens[8].hints[2].text | Product rule, integrate it, rearrange, then shorten with $du$ and $dv$. | correct | B19 |
| l10-undo-product.json | screens[8].feedback.correct | The product rule, integrated and rearranged, is integration by parts. | correct | B19 |
| l10-undo-product.json | screens[8].feedback.generic | Not quite right. Start from the product rule and finish with the short form. | correct | B19 |
| l10-undo-product.json | screens[8].feedback.byKey.short | The short form only renames $v'\,dx$ and $u'\,dx$. It comes last. | correct | B19 |
| l10-undo-product.json | screens[8].feedback.byKey.rearr | You can only rearrange once the product rule has been integrated. | correct | B19 |
| l10-undo-product.json | screens[8].explain.text | Integrating $(uv)' = u'v + uv'$ gives $uv = \int u'v\,dx + \int uv'\,dx$: blue plus orange is the rectangle... | correct | B19 |
| l10-undo-product.json | screens[9].prose | A new trading desk's profit arrives continuously, ramping up at $10t$ thousand pounds a year at time $t$. D... | correct | B19 |
| l10-undo-product.json | screens[9].canvas.params.functions[0].label | undiscounted $10t$ | correct | B19 |
| l10-undo-product.json | screens[9].question | What is the present value, in thousands of pounds? Give 2 decimal places. | correct | B19 |
| l10-undo-product.json | screens[9].widget.answer | graded key (numeric): 18.715 | correct | B19 |
| l10-undo-product.json | screens[9].widget.wrong[0] | slip undiscounted = 20 is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | screens[9].widget.wrong[1] | slip end-discount = 18.097 is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | screens[9].widget.wrong[2] | slip mid-discount = 19.025 is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | screens[9].widget.accept | £18.72 thousand: $\left[-200t\,e^{-0.05t} - 4000e^{-0.05t}\right]_0^2 \approx 18.715$. | correct | B19 |
| l10-undo-product.json | screens[9].hints[0].text | Which factor gets simpler when differentiated: $10t$ or $e^{-0.05t}$? | correct | B19 |
| l10-undo-product.json | screens[9].hints[1].text | Take $u = 10t$ and $dv = e^{-0.05t}\,dt$, so $v = -20e^{-0.05t}$. | correct | B19 |
| l10-undo-product.json | screens[9].hints[2].text | $uv - \int v\,du = -200t\,e^{-0.05t} + \int 200e^{-0.05t}\,dt = -200t\,e^{-0.05t} - 4000e^{-0.05t}$. Evalua... | correct | B19 |
| l10-undo-product.json | screens[9].feedback.correct | About £18.72 thousand, against £20 thousand undiscounted. | correct | B19 |
| l10-undo-product.json | screens[9].feedback.generic | Not quite right. Use parts with $u = 10t$, then evaluate between 0 and 2. | correct | B19 |
| l10-undo-product.json | screens[9].feedback.byKey.undiscounted | That is $\int_0^2 10t\,dt$, with no discounting. The factor $e^{-0.05t}$ makes later pounds worth less. | correct | B19 |
| l10-undo-product.json | screens[9].feedback.byKey.end-discount | You discounted the whole £20 thousand as if it all arrived at year 2. Most of it arrives earlier. | correct | B19 |
| l10-undo-product.json | screens[9].feedback.byKey.mid-discount | You discounted everything from year 1. But the cash ramps up, so more of it arrives late. | correct | B19 |
| l10-undo-product.json | screens[9].explain.text | With $u = 10t$ the antiderivative is $-200t\,e^{-0.05t} - 4000e^{-0.05t}$. At 2 it is $-4400e^{-0.1} \appro... | imprecise | Finding 9: 4000 - 3981.28 = 18.72, not 18.715; the unrounded value is -3981.2846 |
| l10-undo-product.json | screens[9].explain.canvas.area.label | ≈ 18.715 | correct | B19 |
| l10-undo-product.json | summary.ideas[0] | Integration by parts trades $\int u\,dv$ for $uv - \int v\,du$: the product rule, integrated and rearranged. | correct | B19 |
| l10-undo-product.json | summary.ideas[1] | Choose $u$ as the factor that gets simpler when differentiated, such as $x$ or $\ln x$. | correct | B19 |
| l10-undo-product.json | summary.ideas[2] | A lone $\ln x$ takes $dv = dx$, and $x^n$ times $e^x$ needs $n$ rounds of parts. | correct | B19 |
| l10-undo-product.json | summary.formula.name | Integration by parts | correct | B19 |
| l10-undo-product.json | summary.formula.tex | \int u\,dv = uv - \int v\,du | correct | B19 |
| l10-undo-product.json | summary.formula.note | With limits: $\int_a^b u\,dv = \big[uv\big]_a^b - \int_a^b v\,du$. | correct | B19 |
| l10-undo-product.json | summary.trap | Taking $u = e^x$ in $\int x\,e^x\,dx$ raises the power of $x$, so the new integral is worse than the old one. | correct | B19 |
| l10-undo-product.json | quiz[0].prose | Use parts with $u = x$ on $\displaystyle\int x\,e^{2x}\,dx$. | correct | B19 |
| l10-undo-product.json | quiz[0].question | Complete $\int x\,e^{2x}\,dx = \;? + C$. | correct | B19 |
| l10-undo-product.json | quiz[0].widget.answer | graded key (expression): "\\frac{1}{2}xe^{2x}-\\frac{1}{4}e^{2x}" | correct | B19 |
| l10-undo-product.json | quiz[0].widget.wrong[0] | slip v-wrong = "xe^{2x}-e^{2x}" is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | quiz[0].widget.wrong[1] | slip half-once = "\\frac{1}{2}xe^{2x}-\\frac{1}{2}e^{2x}" is the value of the named mistake and is not a co... | correct | B19 |
| l10-undo-product.json | quiz[0].feedback.correct | $v = \tfrac{1}{2}e^{2x}$, so the answer is $\tfrac{1}{2}x\,e^{2x} - \tfrac{1}{4}e^{2x} + C$. | correct | B19 |
| l10-undo-product.json | quiz[0].feedback.generic | Not quite right. Find $v = \int e^{2x}\,dx$ carefully first. | correct | B19 |
| l10-undo-product.json | quiz[0].feedback.byKey.v-wrong | You took $v = e^{2x}$. Its derivative is $2e^{2x}$, so $v = \tfrac{1}{2}e^{2x}$. | correct | B19 |
| l10-undo-product.json | quiz[0].feedback.byKey.half-once | You halved once. $\int \tfrac{1}{2}e^{2x}\,dx = \tfrac{1}{4}e^{2x}$: integrating $e^{2x}$ halves again. | correct | B19 |
| l10-undo-product.json | quiz[0].explain.text | $u = x$, $du = dx$, $v = \tfrac{1}{2}e^{2x}$. So the integral is $\tfrac{1}{2}x\,e^{2x} - \int \tfrac{1}{2}... | correct | B19 |
| l10-undo-product.json | quiz[1].prose | You want $\displaystyle\int x^3 \ln x\,dx$ by parts. | correct | B19 |
| l10-undo-product.json | quiz[1].question | Which choice of $u$ should you make? | correct | B19 |
| l10-undo-product.json | quiz[1].widget.options[0] | graded key (choice): $u = \ln x$, $dv = x^3\,dx$ | correct | B19 |
| l10-undo-product.json | quiz[1].widget.options[1].text | wrong option, wrong under every convention: $u = x^3$, $dv = \ln x\,dx$ | correct | B19 |
| l10-undo-product.json | quiz[1].widget.options[1].why | Then $v = \int \ln x\,dx = x\ln x - x$, and the new integral is harder than the old one. | imprecise | Finding 6: the new integral is 3 int x^3 ln x - 3 int x^3, the same integral again, which solves (sympy check); homework-3 items[9] model says so |
| l10-undo-product.json | quiz[1].widget.options[2].text | wrong option, wrong under every convention: Either choice is as good | correct | B19 |
| l10-undo-product.json | quiz[1].widget.options[2].why | With $u = x^3$ the new integral contains $x^3 \ln x$ terms again. The choice matters. | correct | B19 |
| l10-undo-product.json | quiz[1].feedback.correct | $\ln x$ becomes $\tfrac{1}{x}$, and $\int \tfrac{x^4}{4} \cdot \tfrac{1}{x}\,dx$ is easy. | correct | B19 |
| l10-undo-product.json | quiz[1].feedback.generic | Not quite right. Choose the $u$ that gets simpler when differentiated. | correct | B19 |
| l10-undo-product.json | quiz[1].explain.text | With $u = \ln x$, $v = \tfrac{x^4}{4}$ and the new integral is $\int \tfrac{x^3}{4}\,dx = \tfrac{x^4}{16}$.... | correct | B19 |
| l10-undo-product.json | quiz[2].prose | Use $\int x\,e^x\,dx = (x - 1)e^x + C$. | correct | B19 |
| l10-undo-product.json | quiz[2].question | Evaluate $\displaystyle\int_0^2 x\,e^x\,dx$ to 3 decimal places. | correct | B19 |
| l10-undo-product.json | quiz[2].widget.answer | graded key (numeric): 8.389 | correct | B19 |
| l10-undo-product.json | quiz[2].widget.wrong[0] | slip lower = 7.389 is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | quiz[2].widget.wrong[1] | slip no-integral = 14.778 is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | quiz[2].widget.accept | $e^2 + 1 \approx 8.389$. | correct | B19 |
| l10-undo-product.json | quiz[2].feedback.correct | $(2 - 1)e^2 - (0 - 1)e^0 = e^2 + 1$. | correct | B19 |
| l10-undo-product.json | quiz[2].feedback.generic | Not quite right. Evaluate $(x - 1)e^x$ at 2 and at 0, then subtract. | correct | B19 |
| l10-undo-product.json | quiz[2].feedback.byKey.lower | You treated the value at 0 as 0. There $(x - 1)e^x = -1$, and subtracting it adds 1. | correct | B19 |
| l10-undo-product.json | quiz[2].feedback.byKey.no-integral | You evaluated $x\,e^x$ alone. The antiderivative is $(x - 1)e^x$, not $x\,e^x$. | correct | B19 |
| l10-undo-product.json | quiz[2].explain.text | At $x = 2$, $(x - 1)e^x = e^2$. At $x = 0$ it is $-1$. So the integral is $e^2 + 1 \approx 8.389$. | correct | B19 |
| l10-undo-product.json | quiz[3].prose | Use $\int \ln x\,dx = x\ln x - x + C$. | correct | B19 |
| l10-undo-product.json | quiz[3].question | Evaluate $\displaystyle\int_1^e \ln x\,dx$. | correct | B19 |
| l10-undo-product.json | quiz[3].widget.answer | graded key (numeric): 1 | correct | B19 |
| l10-undo-product.json | quiz[3].widget.wrong[0] | slip no-integral = 2.7183 is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | quiz[3].widget.wrong[1] | slip top-only = 0 is the value of the named mistake and is not a correct answer | correct | B19 |
| l10-undo-product.json | quiz[3].widget.accept | Exactly 1. | correct | B19 |
| l10-undo-product.json | quiz[3].feedback.correct | $(e - e) - (0 - 1) = 1$. | correct | B19 |
| l10-undo-product.json | quiz[3].feedback.generic | Not quite right. Evaluate $x\ln x - x$ at $e$ and at 1, then subtract. | correct | B19 |
| l10-undo-product.json | quiz[3].feedback.byKey.no-integral | You evaluated $x\ln x$ alone. Subtract the $-x$ part between the limits too. | correct | B19 |
| l10-undo-product.json | quiz[3].feedback.byKey.top-only | That is the value at $e$ only. At 1 the antiderivative is $-1$, so subtract it. | correct | B19 |
| l10-undo-product.json | quiz[3].explain.text | At $e$: $e \cdot 1 - e = 0$. At 1: $0 - 1 = -1$. So the integral is $0 - (-1) = 1$. | correct | B19 |
| l11-to-infinity.json | screens[0].prose | The curve $\frac{1}{x^2}$ falls towards 0 but never reaches it. The shaded strip runs from $x = 1$ to $x = ... | correct | B20 |
| l11-to-infinity.json | screens[0].canvas.params.functions[0].label | $\frac{1}{x^2}$ | correct | B20 |
| l11-to-infinity.json | screens[0].canvas.derive.caption | Area from 1 to {{b}}: {{fixed(1 - 1/b, 4)}} | correct | B20 |
| l11-to-infinity.json | screens[0].question | As $b$ grows without limit, what happens to the area? | correct | B20 |
| l11-to-infinity.json | screens[0].widget.options[0] | graded key (choice): It settles towards 1 | correct | B20 |
| l11-to-infinity.json | screens[0].widget.options[1].text | wrong option, wrong under every convention: It grows without limit, because the strip never ends | correct | B20 |
| l11-to-infinity.json | screens[0].widget.options[1].why | The strip is endless, but it thins fast. The caption creeps up and stalls below 1. | correct | B20 |
| l11-to-infinity.json | screens[0].widget.options[2].text | wrong option, wrong under every convention: It reaches exactly 1 at $b = 1000$ | correct | B20 |
| l11-to-infinity.json | screens[0].widget.options[2].why | At $b = 1000$ the caption shows 0.9990. It gets as close to 1 as we like, but never reaches it. | correct | B20 |
| l11-to-infinity.json | screens[0].hints[0].text | Read the caption at $b = 10$, $b = 100$ and $b = 1000$. | correct | B20 |
| l11-to-infinity.json | screens[0].hints[1].text | The area gains less and less as $b$ grows. | correct | B20 |
| l11-to-infinity.json | screens[0].hints[2].text | 0.9, 0.99, 0.999: the area closes in on 1. | correct | B20 |
| l11-to-infinity.json | screens[0].feedback.correct | The area closes in on 1 and never passes it. | correct | B20 |
| l11-to-infinity.json | screens[0].feedback.generic | Not quite right. Read the area for larger and larger $b$. | correct | B20 |
| l11-to-infinity.json | screens[0].explain.text | The caption read 0.9 at $b = 10$, 0.99 at 100 and 0.999 at 1000. An endless strip can have a finite area wh... | correct | B20 |
| l11-to-infinity.json | screens[1].prose | The caption computed $\int_1^b \frac{1}{x^2}\,dx$. Its limit as $b \to \infty$ is written $\int_1^\infty \f... | correct | B20 |
| l11-to-infinity.json | screens[1].canvas.params.functions[0].label | $\frac{1}{x^2}$ | correct | B20 |
| l11-to-infinity.json | screens[1].canvas.state.caption | The strip from 1 to $b = 10$ | correct | B20 |
| l11-to-infinity.json | screens[1].question | Find $\displaystyle\int_1^b \frac{1}{x^2}\,dx$ in terms of $b$. | correct | B20 |
| l11-to-infinity.json | screens[1].widget.answer | graded key (expression): "1-\\frac{1}{b}" | correct | B20 |
| l11-to-infinity.json | screens[1].widget.wrong[0] | slip sign = "\\frac{1}{b}-1" is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | screens[1].widget.wrong[1] | slip power-up = "\\frac{1}{3}-\\frac{1}{3b^3}" is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | screens[1].widget.wrong[2] | slip upper-only = "-\\frac{1}{b}" is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | screens[1].hints[0].text | An antiderivative of $x^{-2}$ is $\frac{x^{-1}}{-1} = -\frac{1}{x}$. | correct | B20 |
| l11-to-infinity.json | screens[1].hints[1].text | Evaluate $-\frac{1}{x}$ at $b$ and at 1. | correct | B20 |
| l11-to-infinity.json | screens[1].hints[2].text | $-\frac{1}{b} - \left(-\frac{1}{1}\right) = 1 - \frac{1}{b}$. | correct | B20 |
| l11-to-infinity.json | screens[1].feedback.correct | $\left[-\tfrac{1}{x}\right]_1^b = 1 - \tfrac{1}{b}$, which tends to 1. | correct | B20 |
| l11-to-infinity.json | screens[1].feedback.generic | Not quite right. Use the antiderivative $-\frac{1}{x}$ and evaluate from 1 to $b$. | correct | B20 |
| l11-to-infinity.json | screens[1].feedback.byKey.sign | You subtracted the wrong way round. It is $F(b) - F(1)$, and the area must be positive. | correct | B20 |
| l11-to-infinity.json | screens[1].feedback.byKey.power-up | You lowered the power to $-3$. Integrating $x^{-2}$ raises it by one, to $x^{-1}$. | correct | B20 |
| l11-to-infinity.json | screens[1].feedback.byKey.upper-only | You evaluated at $b$ only. At $x = 1$, $-\frac{1}{x} = -1$, so subtract it. | correct | B20 |
| l11-to-infinity.json | screens[1].explain.text | $\int_1^b \frac{1}{x^2}\,dx = 1 - \frac{1}{b}$, and $\frac{1}{b} \to 0$ as $b \to \infty$. So $\int_1^\inft... | correct | B20 |
| l11-to-infinity.json | screens[1].explain.canvas.caption | $\int_1^b \frac{1}{x^2}\,dx = 1 - \frac{1}{b} \to 1$ | correct | B20 |
| l11-to-infinity.json | screens[2].prose | Now the steeper curve $\frac{1}{x^3}$, drawn under the dashed $\frac{1}{x^2}$. It thins out even faster. | correct | B20 |
| l11-to-infinity.json | screens[2].canvas.params.functions[0].label | $\frac{1}{x^3}$ | correct | B20 |
| l11-to-infinity.json | screens[2].canvas.params.functions[1].label | $\frac{1}{x^2}$ | correct | B20 |
| l11-to-infinity.json | screens[2].question | Evaluate $\displaystyle\int_1^\infty \frac{1}{x^3}\,dx$. | correct | B20 |
| l11-to-infinity.json | screens[2].widget.answer | graded key (numeric): 0.5 | correct | B20 |
| l11-to-infinity.json | screens[2].widget.wrong[0] | slip one-over-p = 0.3333 is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | screens[2].widget.wrong[1] | slip same = 1 is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | screens[2].widget.wrong[2] | slip sign = -0.5 is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | screens[2].widget.accept | $\tfrac{1}{2}$: $\int_1^b x^{-3}\,dx = \tfrac{1}{2} - \tfrac{1}{2b^2} \to \tfrac{1}{2}$. | correct | B20 |
| l11-to-infinity.json | screens[2].hints[0].text | An antiderivative of $x^{-3}$ is $\frac{x^{-2}}{-2}$. | correct | B20 |
| l11-to-infinity.json | screens[2].hints[1].text | $\int_1^b x^{-3}\,dx = \left[-\frac{1}{2x^2}\right]_1^b$. | correct | B20 |
| l11-to-infinity.json | screens[2].hints[2].text | $-\frac{1}{2b^2} + \frac{1}{2}$, and the first term tends to 0. | correct | B20 |
| l11-to-infinity.json | screens[2].feedback.correct | $\tfrac{1}{2} - \tfrac{1}{2b^2} \to \tfrac{1}{2}$. | correct | B20 |
| l11-to-infinity.json | screens[2].feedback.generic | Not quite right. Integrate from 1 to $b$ first, then let $b \to \infty$. | correct | B20 |
| l11-to-infinity.json | screens[2].feedback.byKey.one-over-p | You divided by 3. Integrating $x^{-3}$ gives $\frac{x^{-2}}{-2}$: divide by the new power, $-2$. | correct | B20 |
| l11-to-infinity.json | screens[2].feedback.byKey.same | That is the area under $\frac{1}{x^2}$. The steeper curve encloses less. | correct | B20 |
| l11-to-infinity.json | screens[2].feedback.byKey.sign | You subtracted the wrong way round. The curve is above the axis, so the area is positive. | correct | B20 |
| l11-to-infinity.json | screens[2].explain.text | $\int_1^b x^{-3}\,dx = \tfrac{1}{2} - \tfrac{1}{2b^2}$, which tends to $\tfrac{1}{2}$. The steeper curve si... | correct | B20 |
| l11-to-infinity.json | screens[3].prose | Now a slower curve, $\frac{1}{\sqrt{x}} = x^{-1/2}$. It also falls towards 0. Here $\int_1^b x^{-1/2}\,dx =... | correct | B20 |
| l11-to-infinity.json | screens[3].canvas.params.functions[0].label | $\frac{1}{\sqrt{x}}$ | correct | B20 |
| l11-to-infinity.json | screens[3].canvas.params.functions[1].label | $\frac{1}{x^2}$ | correct | B20 |
| l11-to-infinity.json | screens[3].question | What does $\displaystyle\int_1^\infty \frac{1}{\sqrt{x}}\,dx$ do? | correct | B20 |
| l11-to-infinity.json | screens[3].widget.options[0].text | wrong option, wrong under every convention: It converges to 2 | correct | B20 |
| l11-to-infinity.json | screens[3].widget.options[0].why | You dropped $2\sqrt{b}$ as if it vanished. It grows without limit as $b$ grows. | correct | B20 |
| l11-to-infinity.json | screens[3].widget.options[1].text | wrong option, wrong under every convention: It converges to $-2$ | correct | B20 |
| l11-to-infinity.json | screens[3].widget.options[1].why | The curve is above the axis, so no area under it is negative. And $2\sqrt{b}$ does not vanish. | correct | B20 |
| l11-to-infinity.json | screens[3].widget.options[2] | graded key (choice): It diverges: $2\sqrt{b} - 2$ grows without limit | correct | B20 |
| l11-to-infinity.json | screens[3].hints[0].text | What happens to $2\sqrt{b}$ as $b$ grows? | correct | B20 |
| l11-to-infinity.json | screens[3].hints[1].text | At $b = 100$ it is 20. At $b = 10\,000$ it is 200. | correct | B20 |
| l11-to-infinity.json | screens[3].hints[2].text | $2\sqrt{b} - 2$ has no finite limit, so the integral diverges. | correct | B20 |
| l11-to-infinity.json | screens[3].feedback.correct | $2\sqrt{b} - 2$ grows without limit, so the integral diverges. | correct | B20 |
| l11-to-infinity.json | screens[3].feedback.generic | Not quite right. Ask what $2\sqrt{b} - 2$ does as $b$ grows. | correct | B20 |
| l11-to-infinity.json | screens[3].explain.text | At $b = 100$ the area is 18; at $b = 10\,000$ it is 198. It never settles, so the integral **diverges**. Th... | correct | B20 |
| l11-to-infinity.json | screens[4].prose | The middle case is $\frac{1}{x}$, which also falls to 0 as $x$ grows. Slide $b$ and watch the area from 1 t... | correct | B20 |
| l11-to-infinity.json | screens[4].canvas.params.functions[0].label | $\frac{1}{x}$ | correct | B20 |
| l11-to-infinity.json | screens[4].canvas.derive.caption | Area from 1 to {{b}}: {{fixed(ln(b), 3)}} | correct | B20 |
| l11-to-infinity.json | screens[4].question | Does $\displaystyle\int_1^\infty \frac{1}{x}\,dx$ converge? | correct | B20 |
| l11-to-infinity.json | screens[4].widget.options[0].text | wrong option, wrong under every convention: Yes, because $\frac{1}{x}$ falls to 0 | correct | B20 |
| l11-to-infinity.json | screens[4].widget.options[0].why | Falling to 0 is not enough. The area is $\ln b$, which grows without limit. | correct | B20 |
| l11-to-infinity.json | screens[4].widget.options[1].text | wrong option, wrong under every convention: Yes, to about 6.9 | correct | B20 |
| l11-to-infinity.json | screens[4].widget.options[1].why | That is $\ln 1000$, the area up to $b = 1000$. At $b = 10^6$ it is 13.8, and it keeps growing. | correct | B20 |
| l11-to-infinity.json | screens[4].widget.options[2] | graded key (choice): No: the area is $\ln b$, which grows without limit | correct | B20 |
| l11-to-infinity.json | screens[4].hints[0].text | An antiderivative of $\frac{1}{x}$ is $\ln x$. What is $\int_1^b \frac{1}{x}\,dx$? | correct | B20 |
| l11-to-infinity.json | screens[4].hints[1].text | It is $\ln b - \ln 1 = \ln b$. | correct | B20 |
| l11-to-infinity.json | screens[4].hints[2].text | $\ln b$ grows slowly but without limit: $\ln 10^6 \approx 13.8$, $\ln 10^{12} \approx 27.6$. | correct | B20 |
| l11-to-infinity.json | screens[4].feedback.correct | $\ln b$ has no finite limit, so the integral diverges. | correct | B20 |
| l11-to-infinity.json | screens[4].feedback.generic | Not quite right. Find $\int_1^b \frac{1}{x}\,dx$ and ask what it does as $b$ grows. | correct | B20 |
| l11-to-infinity.json | screens[4].feedback.byKey.zero | You assumed a curve that falls to 0 has finite area. $\frac{1}{x}$ falls to 0, yet $\int_1^b \frac{1}{x}\,d... | correct | B20 |
| l11-to-infinity.json | screens[4].feedback.byKey.value | You read the area at one value of $b$. Convergence asks about every $b$, and $\ln b$ keeps growing. | correct | B20 |
| l11-to-infinity.json | screens[4].explain.text | $\int_1^b \frac{1}{x}\,dx = \ln b$, and $\ln b \to \infty$, however slowly. So a function can fall to 0 and... | correct | B20 |
| l11-to-infinity.json | screens[4].explain.canvas.caption | $\int_1^b \frac{1}{x}\,dx = \ln b \to \infty$ | correct | B20 |
| l11-to-infinity.json | screens[5].prose | For $p \neq 1$, $$\int_1^b x^{-p}\,dx = \frac{b^{1-p} - 1}{1 - p}.$$ The term $b^{1-p}$ decides everything.... | correct | B20 |
| l11-to-infinity.json | screens[5].canvas.derive.caption | $p$ = {{p}}: area from 1 to {{b}} is {{abs(p - 1) < 0.001 ? fixed(ln(b), 3) : fixed((pow(b, 1 - p) - 1) / (... | correct | B20 |
| l11-to-infinity.json | screens[5].question | Which values of $p$ give a finite $\displaystyle\int_1^\infty x^{-p}\,dx$? | correct | B20 |
| l11-to-infinity.json | screens[5].widget.options[0] | graded key (choice): $p > 1$ | correct | B20 |
| l11-to-infinity.json | screens[5].widget.options[1].text | wrong option, wrong under every convention: $p \ge 1$ | correct | B20 |
| l11-to-infinity.json | screens[5].widget.options[1].why | At $p = 1$ the area is $\ln b$, which grows without limit. The boundary case diverges. | correct | B20 |
| l11-to-infinity.json | screens[5].widget.options[2].text | wrong option, wrong under every convention: $p > 0$ | correct | B20 |
| l11-to-infinity.json | screens[5].widget.options[2].why | Every $p > 0$ makes the curve fall to 0. At $p = \tfrac{1}{2}$ the area still grows like $2\sqrt{b}$. | correct | B20 |
| l11-to-infinity.json | screens[5].hints[0].text | When does $b^{1-p}$ shrink to 0 as $b$ grows? | correct | B20 |
| l11-to-infinity.json | screens[5].hints[1].text | It shrinks when the power $1 - p$ is negative. | correct | B20 |
| l11-to-infinity.json | screens[5].hints[2].text | $1 - p < 0$ means $p > 1$. | correct | B20 |
| l11-to-infinity.json | screens[5].feedback.correct | For $p > 1$, $b^{1-p} \to 0$ and the area settles. | correct | B20 |
| l11-to-infinity.json | screens[5].feedback.generic | Not quite right. Check $p = 1$ and $p = \tfrac{1}{2}$ with the sliders. | correct | B20 |
| l11-to-infinity.json | screens[5].feedback.byKey.ge | You included $p = 1$. That case is $\ln b$, which diverges. | correct | B20 |
| l11-to-infinity.json | screens[5].explain.text | For $p > 1$ the power $1 - p$ is negative, so $b^{1-p} \to 0$. For $p < 1$ it grows, and $p = 1$ gives $\ln... | correct | B20 |
| l11-to-infinity.json | screens[6].prose | Finish the line for $p > 1$, where $b^{1-p} \to 0$: $$\int_1^\infty x^{-p}\,dx = \lim_{b \to \infty} \frac{... | correct | B20 |
| l11-to-infinity.json | screens[6].question | Write the value as a fraction in $p$ with a positive bottom. | correct | B20 |
| l11-to-infinity.json | screens[6].widget.answer | graded key (expression): "\\frac{1}{p-1}" | correct | B20 |
| l11-to-infinity.json | screens[6].widget.wrong[0] | slip sign = "\\frac{1}{1-p}" is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | screens[6].widget.wrong[1] | slip one-over-p = "\\frac{1}{p}" is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | screens[6].hints[0].text | Simplify $\frac{-1}{1 - p}$. | correct | B20 |
| l11-to-infinity.json | screens[6].hints[1].text | Multiply the top and bottom by $-1$. | correct | B20 |
| l11-to-infinity.json | screens[6].hints[2].text | $\frac{-1}{1 - p} = \frac{1}{p - 1}$. Check with $p = 2$: it gives 1. | correct | B20 |
| l11-to-infinity.json | screens[6].feedback.correct | $\frac{-1}{1 - p} = \frac{1}{p - 1}$, which is 1 at $p = 2$ and $\tfrac{1}{2}$ at $p = 3$. | correct | B20 |
| l11-to-infinity.json | screens[6].feedback.generic | Not quite right. Flip the sign of the top and the bottom of $\frac{-1}{1 - p}$. | correct | B20 |
| l11-to-infinity.json | screens[6].feedback.byKey.sign | That is negative for $p > 1$, but the area is positive. The top's minus sign moves to the bottom. | correct | B20 |
| l11-to-infinity.json | screens[6].feedback.byKey.one-over-p | You divided by $p$. The antiderivative of $x^{-p}$ divides by the new power, $1 - p$. | correct | B20 |
| l11-to-infinity.json | screens[6].explain.text | Dividing $-1$ by $1 - p$ gives $\frac{1}{p - 1}$. It matches the screens before: 1 at $p = 2$, $\tfrac{1}{2... | correct | B20 |
| l11-to-infinity.json | screens[7].prose | A perpetuity pays £1 a year forever, arriving continuously. At a 4% continuous discount rate, money at time... | correct | B20 |
| l11-to-infinity.json | screens[7].canvas.params.functions[0].label | $e^{-0.04t}$ | correct | B20 |
| l11-to-infinity.json | screens[7].canvas.derive.caption | Value of the first {{T}} years: {{money((1 - exp(-0.04 * T)) / 0.04)}} | correct | B20 |
| l11-to-infinity.json | screens[7].question | What is the perpetuity worth today? | correct | B20 |
| l11-to-infinity.json | screens[7].widget.answer | graded key (numeric): 25 | correct | B20 |
| l11-to-infinity.json | screens[7].widget.wrong[0] | slip times-rate = 4 is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | screens[7].widget.wrong[1] | slip rate = 0.04 is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | screens[7].widget.wrong[2] | slip sign = -25 is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | screens[7].widget.accept | £25.00: $\int_0^\infty e^{-0.04t}\,dt = \tfrac{1}{0.04}$. | correct | B20 |
| l11-to-infinity.json | screens[7].hints[0].text | An antiderivative of $e^{-0.04t}$ is $-\frac{e^{-0.04t}}{0.04}$. | correct | B20 |
| l11-to-infinity.json | screens[7].hints[1].text | Over $[0, b]$ the value is $\frac{1 - e^{-0.04b}}{0.04}$. | correct | B20 |
| l11-to-infinity.json | screens[7].hints[2].text | $e^{-0.04b} \to 0$, so the value tends to $\frac{1}{0.04}$. | correct | B20 |
| l11-to-infinity.json | screens[7].feedback.correct | $\tfrac{1}{0.04} = 25$: the perpetuity is worth £25.00. | correct | B20 |
| l11-to-infinity.json | screens[7].feedback.generic | Not quite right. Integrate from 0 to $b$, then let $b \to \infty$. | correct | B20 |
| l11-to-infinity.json | screens[7].feedback.byKey.times-rate | You multiplied 0.04 by 100. The integral divides by the rate: $\tfrac{1}{0.04}$. | correct | B20 |
| l11-to-infinity.json | screens[7].feedback.byKey.rate | That is the rate itself. The value is its reciprocal, $\tfrac{1}{0.04}$. | correct | B20 |
| l11-to-infinity.json | screens[7].feedback.byKey.sign | You lost a sign. $\left[-\tfrac{e^{-0.04t}}{0.04}\right]_0^b = \tfrac{1}{0.04} - \tfrac{e^{-0.04b}}{0.04}$,... | correct | B20 |
| l11-to-infinity.json | screens[7].explain.text | Over $[0, b]$ the value is $\frac{1 - e^{-0.04b}}{0.04}$, and $e^{-0.04b} \to 0$. So the perpetuity is wort... | correct | B20 |
| l11-to-infinity.json | screens[8].prose | Now the payment starts at £1 a year and grows at 2% a year continuously. Discounting at 4%, its value is $$... | correct | B20 |
| l11-to-infinity.json | screens[8].canvas.params.functions[0].label | growing at 2% | correct | B20 |
| l11-to-infinity.json | screens[8].canvas.params.functions[1].label | flat £1 | correct | B20 |
| l11-to-infinity.json | screens[8].question | What is the growing perpetuity worth today? | correct | B20 |
| l11-to-infinity.json | screens[8].widget.answer | graded key (numeric): 50 | correct | B20 |
| l11-to-infinity.json | screens[8].widget.wrong[0] | slip no-growth = 25 is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | screens[8].widget.wrong[1] | slip added = 16.67 is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | screens[8].widget.accept | £50.00: $\int_0^\infty e^{-0.02t}\,dt = \tfrac{1}{0.04 - 0.02}$. | correct | B20 |
| l11-to-infinity.json | screens[8].hints[0].text | Combine the powers: $e^{0.02t}\,e^{-0.04t} = e^{-0.02t}$. | correct | B20 |
| l11-to-infinity.json | screens[8].hints[1].text | This is the last screen's integral with rate $r = 0.02$. | correct | B20 |
| l11-to-infinity.json | screens[8].hints[2].text | $\int_0^\infty e^{-0.02t}\,dt = \tfrac{1}{0.02} = 50$. | correct | B20 |
| l11-to-infinity.json | screens[8].feedback.correct | $\tfrac{1}{0.04 - 0.02} = \text{£}50.00$, double the flat perpetuity. | correct | B20 |
| l11-to-infinity.json | screens[8].feedback.generic | Not quite right. Combine the two exponentials first. | correct | B20 |
| l11-to-infinity.json | screens[8].feedback.byKey.no-growth | That ignores the growth. The payments rise, so the stream is worth more than the flat £25.00. | correct | B20 |
| l11-to-infinity.json | screens[8].feedback.byKey.added | You added the rates: $\tfrac{1}{0.06}$. Growth works against discounting, so subtract: $0.04 - 0.02$. | correct | B20 |
| l11-to-infinity.json | screens[8].explain.text | The integrand is $e^{-0.02t}$, so the value is $\frac{1}{0.04 - 0.02} = \text{£}50.00$. This is the continu... | correct | B20 |
| l11-to-infinity.json | summary.ideas[0] | An integral to infinity is the limit of $\int_a^b$ as $b \to \infty$. It converges when that limit is finite. | correct | B20 |
| l11-to-infinity.json | summary.ideas[1] | $\int_1^\infty x^{-p}\,dx$ converges exactly when $p > 1$, and then equals $\frac{1}{p - 1}$. | correct | B20 |
| l11-to-infinity.json | summary.ideas[2] | A perpetual £1 a year at rate $r$ is worth $\int_0^\infty e^{-rt}\,dt = \frac{1}{r}$: £25.00 at 4%. | correct | B20 |
| l11-to-infinity.json | summary.formula.name | Improper integral | correct | B20 |
| l11-to-infinity.json | summary.formula.tex | \int_a^\infty f(x)\,dx = \lim_{b \to \infty} \int_a^b f(x)\,dx | correct | B20 |
| l11-to-infinity.json | summary.formula.note | Integrate to $b$ first, then let $b \to \infty$. | correct | B20 |
| l11-to-infinity.json | summary.trap | A curve that falls to 0 can still have infinite area: $\int_1^b \frac{1}{x}\,dx = \ln b$ grows without limit. | correct | B20 |
| l11-to-infinity.json | quiz[0].prose | Use $\int_1^\infty x^{-p}\,dx = \frac{1}{p - 1}$ for $p > 1$. | correct | B20 |
| l11-to-infinity.json | quiz[0].question | Evaluate $\displaystyle\int_1^\infty \frac{3}{x^4}\,dx$. | correct | B20 |
| l11-to-infinity.json | quiz[0].widget.answer | graded key (numeric): 1 | correct | B20 |
| l11-to-infinity.json | quiz[0].widget.wrong[0] | slip one-over-p = 0.75 is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | quiz[0].widget.wrong[1] | slip no-three = 0.3333 is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | quiz[0].widget.accept | Exactly 1: $3 \times \tfrac{1}{3}$. | correct | B20 |
| l11-to-infinity.json | quiz[0].feedback.correct | $3 \times \tfrac{1}{4 - 1} = 1$. | correct | B20 |
| l11-to-infinity.json | quiz[0].feedback.generic | Not quite right. Take the 3 outside, then use $\tfrac{1}{p - 1}$ with $p = 4$. | correct | B20 |
| l11-to-infinity.json | quiz[0].feedback.byKey.one-over-p | You used $\tfrac{1}{p}$. Integrating $x^{-4}$ divides by $-3$, so the factor is $\tfrac{1}{3}$. | correct | B20 |
| l11-to-infinity.json | quiz[0].feedback.byKey.no-three | That is $\int_1^\infty x^{-4}\,dx$. Multiply by the 3 on top. | correct | B20 |
| l11-to-infinity.json | quiz[0].explain.text | $\int_1^\infty x^{-4}\,dx = \tfrac{1}{3}$, since $p = 4 > 1$. Times 3, the integral is 1. | correct | B20 |
| l11-to-infinity.json | quiz[1].prose | Four improper integrals, each starting at $x = 1$. | correct | B20 |
| l11-to-infinity.json | quiz[1].question | Which one converges? | correct | B20 |
| l11-to-infinity.json | quiz[1].widget.options[0] | graded key (choice): $\int_1^\infty x^{-1.01}\,dx$ | correct | B20 |
| l11-to-infinity.json | quiz[1].widget.options[1].text | wrong option, wrong under every convention: $\int_1^\infty x^{-0.99}\,dx$ | correct | B20 |
| l11-to-infinity.json | quiz[1].widget.options[1].why | Here $p = 0.99 < 1$, so $b^{1-p} = b^{0.01}$ grows without limit, slowly. | correct | B20 |
| l11-to-infinity.json | quiz[1].widget.options[2].text | wrong option, wrong under every convention: $\int_1^\infty \frac{1}{x}\,dx$ | correct | B20 |
| l11-to-infinity.json | quiz[1].widget.options[2].why | This is $\ln b$, which grows without limit. The boundary case diverges. | correct | B20 |
| l11-to-infinity.json | quiz[1].widget.options[3].text | wrong option, wrong under every convention: $\int_1^\infty \frac{1}{\sqrt{x}}\,dx$ | correct | B20 |
| l11-to-infinity.json | quiz[1].widget.options[3].why | Here $p = \tfrac{1}{2}$, and the area grows like $2\sqrt{b}$. | correct | B20 |
| l11-to-infinity.json | quiz[1].feedback.correct | $p = 1.01 > 1$, so it converges, to $\tfrac{1}{0.01} = 100$. | correct | B20 |
| l11-to-infinity.json | quiz[1].feedback.generic | Not quite right. Find the one with $p > 1$. | correct | B20 |
| l11-to-infinity.json | quiz[1].explain.text | Only $p = 1.01$ exceeds 1, so only that integral converges, to $\frac{1}{1.01 - 1} = 100$. Close to the bou... | correct | B20 |
| l11-to-infinity.json | quiz[2].prose | A stream pays £5 a year forever, continuously, discounted at 10% a year continuously. | correct | B20 |
| l11-to-infinity.json | quiz[2].question | What is it worth today? | correct | B20 |
| l11-to-infinity.json | quiz[2].widget.answer | graded key (numeric): 50 | correct | B20 |
| l11-to-infinity.json | quiz[2].widget.wrong[0] | slip times = 0.5 is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | quiz[2].widget.wrong[1] | slip no-discount-factor = 5 is the value of the named mistake and is not a correct answer | correct | B20 |
| l11-to-infinity.json | quiz[2].widget.accept | £50.00: $\int_0^\infty 5e^{-0.1t}\,dt = \tfrac{5}{0.1}$. | correct | B20 |
| l11-to-infinity.json | quiz[2].feedback.correct | $\tfrac{5}{0.1} = \text{£}50.00$. | correct | B20 |
| l11-to-infinity.json | quiz[2].feedback.generic | Not quite right. Use $\int_0^\infty e^{-rt}\,dt = \tfrac{1}{r}$ and multiply by 5. | correct | B20 |
| l11-to-infinity.json | quiz[2].feedback.byKey.times | You multiplied 5 by 0.1. The integral divides by the rate. | correct | B20 |
| l11-to-infinity.json | quiz[2].feedback.byKey.no-discount-factor | That is one year's payment. The stream pays forever. | correct | B20 |
| l11-to-infinity.json | quiz[2].explain.text | $\int_0^\infty 5e^{-0.1t}\,dt = 5 \times \frac{1}{0.1} = \text{£}50.00$. A higher discount rate would make ... | correct | B20 |
| l11-to-infinity.json | quiz[3].prose | A positive function $f$ satisfies $f(x) \to 0$ as $x \to \infty$. | correct | B20 |
| l11-to-infinity.json | quiz[3].question | What can you conclude about $\int_1^\infty f(x)\,dx$? | correct | B20 |
| l11-to-infinity.json | quiz[3].widget.options[0].text | wrong option, wrong under every convention: It converges | correct | B20 |
| l11-to-infinity.json | quiz[3].widget.options[0].why | $\frac{1}{x}$ falls to 0, yet its integral is $\ln b$, which diverges. | correct | B20 |
| l11-to-infinity.json | quiz[3].widget.options[1].text | wrong option, wrong under every convention: It diverges | correct | B20 |
| l11-to-infinity.json | quiz[3].widget.options[1].why | $\frac{1}{x^2}$ falls to 0, and its integral converges to 1. | correct | B20 |
| l11-to-infinity.json | quiz[3].widget.options[2] | graded key (choice): Nothing yet: it depends on how fast $f$ falls | correct | B20 |
| l11-to-infinity.json | quiz[3].feedback.correct | Falling to 0 allows both outcomes: $\frac{1}{x^2}$ converges and $\frac{1}{x}$ diverges. | correct | B20 |
| l11-to-infinity.json | quiz[3].feedback.generic | Not quite right. Test your answer on $\frac{1}{x}$ and on $\frac{1}{x^2}$. | correct | B20 |
| l11-to-infinity.json | quiz[3].explain.text | $\frac{1}{x^2}$ and $\frac{1}{x}$ both fall to 0. The first has finite area, the second does not. So $f \to... | correct | B20 |
| l12-no-formula.json | screens[0].prose | Some integrals have no elementary formula, so we estimate them. Here each strip under $x^2$ is topped by a ... | correct | B21 |
| l12-no-formula.json | screens[0].canvas.params.functions[0].label | $x^2$ | correct | B21 |
| l12-no-formula.json | screens[0].canvas.state.caption | Exact area: $\int_0^1 x^2\,dx = \tfrac{1}{3} \approx 0.33333$ | correct | B21 |
| l12-no-formula.json | screens[0].question | Compared with the exact area $\tfrac{1}{3}$, where do the sums sit? | correct | B21 |
| l12-no-formula.json | screens[0].widget.options[0] | graded key (choice): Always above $\tfrac{1}{3}$, and closing in on it | correct | B21 |
| l12-no-formula.json | screens[0].widget.options[1].text | wrong option, wrong under every convention: Always below $\tfrac{1}{3}$ | correct | B21 |
| l12-no-formula.json | screens[0].widget.options[1].why | Flat lids at the left end would undershoot this rising curve. Chords are different: on a curve that bends u... | correct | B21 |
| l12-no-formula.json | screens[0].widget.options[2].text | wrong option, wrong under every convention: Exactly $\tfrac{1}{3}$ once $n \ge 4$ | correct | B21 |
| l12-no-formula.json | screens[0].widget.options[2].why | At $n = 4$ the sum reads 0.34375. It gets closer as $n$ grows, but never lands exactly on $\tfrac{1}{3}$. | correct | B21 |
| l12-no-formula.json | screens[0].hints[0].text | Compare the sum at $n = 1$, 2 and 4 with 0.33333. | correct | B21 |
| l12-no-formula.json | screens[0].hints[1].text | Look at where each chord sits relative to the curve. | correct | B21 |
| l12-no-formula.json | screens[0].hints[2].text | $x^2$ bends upwards, so every chord lies above it. The sums are 0.5, 0.375, 0.34375. | correct | B21 |
| l12-no-formula.json | screens[0].feedback.correct | Every chord lies above $x^2$, so each sum overshoots, by less as $n$ grows. | correct | B21 |
| l12-no-formula.json | screens[0].feedback.generic | Not quite right. Read the sum for a few values of $n$ and compare with 0.33333. | correct | B21 |
| l12-no-formula.json | screens[0].explain.text | The sums ran 0.5, 0.375, 0.34375 and on down towards 0.33333. Each chord sits above the curve because $x^2$... | correct | B21 |
| l12-no-formula.json | screens[1].prose | Each strip is a trapezium: its width $h$ times the average of its two edge heights. With $n = 2$ strips on ... | correct | B21 |
| l12-no-formula.json | screens[1].canvas.params.functions[0].label | $x^2$ | correct | B21 |
| l12-no-formula.json | screens[1].canvas.state.points[0].label | 0 | correct | B21 |
| l12-no-formula.json | screens[1].canvas.state.points[1].label | 0.25 | correct | B21 |
| l12-no-formula.json | screens[1].canvas.state.points[2].label | 1 | correct | B21 |
| l12-no-formula.json | screens[1].question | Add the two strips' areas. What do you get? | correct | B21 |
| l12-no-formula.json | screens[1].widget.answer | graded key (numeric): 0.375 | correct | B21 |
| l12-no-formula.json | screens[1].widget.wrong[0] | slip no-width = 0.75 is the value of the named mistake and is not a correct answer | correct | B21 |
| l12-no-formula.json | screens[1].widget.wrong[1] | slip left = 0.125 is the value of the named mistake and is not a correct answer | correct | B21 |
| l12-no-formula.json | screens[1].widget.wrong[2] | slip right-rect = 0.625 is the value of the named mistake and is not a correct answer | correct | B21 |
| l12-no-formula.json | screens[1].widget.accept | 0.375: $0.5 \cdot \tfrac{0 + 0.25}{2} + 0.5 \cdot \tfrac{0.25 + 1}{2}$. | correct | B21 |
| l12-no-formula.json | screens[1].hints[0].text | First strip: width 0.5, heights 0 and 0.25. | correct | B21 |
| l12-no-formula.json | screens[1].hints[1].text | Its area is $0.5 \times \tfrac{0 + 0.25}{2} = 0.0625$. | correct | B21 |
| l12-no-formula.json | screens[1].hints[2].text | Second strip: $0.5 \times \tfrac{0.25 + 1}{2} = 0.3125$. Add the two. | correct | B21 |
| l12-no-formula.json | screens[1].feedback.correct | $0.0625 + 0.3125 = 0.375$. | correct | B21 |
| l12-no-formula.json | screens[1].feedback.generic | Not quite right. For each strip, multiply its width by the average of its two heights. | correct | B21 |
| l12-no-formula.json | screens[1].feedback.byKey.no-width | You added the average heights but did not multiply by the width 0.5. | correct | B21 |
| l12-no-formula.json | screens[1].feedback.byKey.left | That uses flat lids at each strip's left height. A trapezium averages both edges. | correct | B21 |
| l12-no-formula.json | screens[1].feedback.byKey.right-rect | That uses flat lids at each strip's right height. A trapezium averages both edges. | correct | B21 |
| l12-no-formula.json | screens[1].explain.text | The strips give 0.0625 and 0.3125, so the total is 0.375. This is the **trapezium rule** with $n = 2$, writ... | correct | B21 |
| l12-no-formula.json | screens[2].prose | With $n$ strips the edges are $x_i = a + ih$. Code will need to visit each edge once. Take $n = 4$ strips o... | correct | B21 |
| l12-no-formula.json | screens[2].canvas.params.functions[0].label | $x^2$ | correct | B21 |
| l12-no-formula.json | screens[2].question | At how many points $x_i$ does the rule evaluate $f$? | correct | B21 |
| l12-no-formula.json | screens[2].widget.answer | graded key (numeric): 5 | correct | B21 |
| l12-no-formula.json | screens[2].widget.wrong[0] | slip strips = 4 is the value of the named mistake and is not a correct answer | correct | B21 |
| l12-no-formula.json | screens[2].widget.wrong[1] | slip inside = 3 is the value of the named mistake and is not a correct answer | correct | B21 |
| l12-no-formula.json | screens[2].widget.accept | 5: $x_0 = 0$ up to $x_4 = 1$. | correct | B21 |
| l12-no-formula.json | screens[2].hints[0].text | Count the vertical edges of the strips, including both ends. | correct | B21 |
| l12-no-formula.json | screens[2].hints[1].text | Each strip has a left and a right edge, and neighbours share one. | correct | B21 |
| l12-no-formula.json | screens[2].hints[2].text | 0, 0.25, 0.5, 0.75 and 1: five points. | correct | B21 |
| l12-no-formula.json | screens[2].feedback.correct | Four strips have five edges: $n$ strips need $n + 1$ points. | correct | B21 |
| l12-no-formula.json | screens[2].feedback.generic | Not quite right. Count every edge, including $x = 0$ and $x = 1$. | correct | B21 |
| l12-no-formula.json | screens[2].feedback.byKey.strips | You counted strips, not edges. Four strips need a fifth edge to close the last one. | correct | B21 |
| l12-no-formula.json | screens[2].feedback.byKey.inside | You counted only the inside edges. The two ends count too. | correct | B21 |
| l12-no-formula.json | screens[2].explain.text | The points are $0, 0.25, 0.5, 0.75, 1$: $x_0$ to $x_4$. So $n$ strips use $n + 1$ points, and $i$ runs from... | correct | B21 |
| l12-no-formula.json | screens[2].explain.canvas.points[0].label | $x_0$ | correct | B21 |
| l12-no-formula.json | screens[2].explain.canvas.points[1].label | $x_1$ | correct | B21 |
| l12-no-formula.json | screens[2].explain.canvas.points[2].label | $x_2$ | correct | B21 |
| l12-no-formula.json | screens[2].explain.canvas.points[3].label | $x_3$ | correct | B21 |
| l12-no-formula.json | screens[2].explain.canvas.points[4].label | $x_4$ | correct | B21 |
| l12-no-formula.json | screens[3].prose | Now in Python. Write `trapezium(f, a, b, n)`: it splits $[a, b]$ into `n` strips of width `h` and adds up t... | correct | B21 |
| l12-no-formula.json | screens[3].canvas.params.functions[0].label | $x^2$ | correct | B21 |
| l12-no-formula.json | screens[3].canvas.state.caption | $T_4$ for $x^2$ on $[0, 1]$ is 0.34375 | correct | B21 |
| l12-no-formula.json | screens[3].question | Complete `trapezium` so it returns the trapezium-rule estimate. | correct | B21 |
| l12-no-formula.json | screens[3].widget.tests | 7 hidden tests, expected values recomputed | correct | B22 |
| l12-no-formula.json | screens[3].widget.solution | solution implements the stated method (composite trapezium; compare with exact) | correct | B22 |
| l12-no-formula.json | screens[3].widget.how | Check runs 7 hidden tests that call `trapezium` with simple functions. Each result is accepted when `math.i... | correct | B21 |
| l12-no-formula.json | screens[3].hints[0].text | Loop `i` over `range(n)`, one pass per strip. | correct | B21 |
| l12-no-formula.json | screens[3].hints[1].text | Strip `i` runs from `a + i * h` to `a + (i + 1) * h`. | correct | B21 |
| l12-no-formula.json | screens[3].hints[2].text | Inside the loop: `total += h * (f(left) + f(right)) / 2`, with `left` and `right` the strip's edges. | correct | B21 |
| l12-no-formula.json | screens[3].feedback.correct | One pass per strip, each adding width times average height. | correct | B21 |
| l12-no-formula.json | screens[3].feedback.generic | Not quite right. Read the first failing test. | correct | B21 |
| l12-no-formula.json | screens[3].feedback.byKey.test-1 | Test 1 expects 0.34375 for $x^2$ on $[0, 1]$ with 4 strips. Check that the loop makes exactly $n$ strips. | correct | B23 |
| l12-no-formula.json | screens[3].feedback.byKey.test-3 | Test 3 is a single strip: $\tfrac{0 + 1}{2} = 0.5$. With `n = 1` your loop must still run once. | correct | B23 |
| l12-no-formula.json | screens[3].feedback.byKey.test-6 | Test 6 starts at $a = -1$. Build each edge from `a`, not from 0. | correct | B23 |
| l12-no-formula.json | screens[3].feedback.byKey.error | Your code stopped with an error. Read the last line of the message under the editor. | correct | B23 |
| l12-no-formula.json | screens[3].explain.text | The loop runs once per strip, so `range(n)` is right here: strip `i` uses edges `i` and `i + 1`. Test 4 is ... | correct | B21 |
| l12-no-formula.json | screens[4].prose | Run your function for $x^2$ on $[0, 1]$ with more and more strips. The table shows each estimate and its er... | correct | B21 |
| l12-no-formula.json | screens[4].canvas.params.rows | [["4", "0.343750", "0.010417"], ["8", "0.335938", "0.002604"], ["16", "0.333984", "0.000651"], ["32", "?", ... | correct | B21 |
| l12-no-formula.json | screens[4].question | Predict the error for $n = 32$, to 6 decimal places. | correct | B21 |
| l12-no-formula.json | screens[4].widget.answer | graded key (numeric): 0.000163 | correct | B21 |
| l12-no-formula.json | screens[4].widget.wrong[0] | slip halved = 0.000326 is the value of the named mistake and is not a correct answer | correct | B21 |
| l12-no-formula.json | screens[4].widget.wrong[1] | slip same = 0.000651 is the value of the named mistake and is not a correct answer | correct | B21 |
| l12-no-formula.json | screens[4].widget.accept | About 0.000163: a quarter of 0.000651. Exactly, the error is $\tfrac{1}{6n^2}$. | correct | B21 |
| l12-no-formula.json | screens[4].hints[0].text | Divide each error by the one below it. | correct | B21 |
| l12-no-formula.json | screens[4].hints[1].text | $0.010417 \div 0.002604 \approx 4$, and the next ratio is also 4. | correct | B21 |
| l12-no-formula.json | screens[4].hints[2].text | Doubling $n$ divides the error by 4: $0.000651 \div 4 \approx 0.000163$. | correct | B21 |
| l12-no-formula.json | screens[4].feedback.correct | Each doubling of $n$ cuts the error by 4. | correct | B21 |
| l12-no-formula.json | screens[4].feedback.generic | Not quite right. Find the ratio between neighbouring errors first. | correct | B21 |
| l12-no-formula.json | screens[4].feedback.byKey.halved | You halved the error. Doubling $n$ halves $h$, and the error shrinks like $h^2$, so it quarters. | correct | B21 |
| l12-no-formula.json | screens[4].feedback.byKey.same | That is the error for $n = 16$. More strips always fit the curve better here. | correct | B21 |
| l12-no-formula.json | screens[4].explain.text | Each error is a quarter of the one above, because the error shrinks like $h^2$. So $n = 32$ gives about 0.0... | correct | B21 |
| l12-no-formula.json | screens[4].explain.canvas.highlight.rows | [3] | correct | B21 |
| l12-no-formula.json | screens[5].prose | Jo saves work by evaluating each point once: halve the two ends, add the inside points, multiply by $h$. Bu... | correct | B21 |
| l12-no-formula.json | screens[5].canvas.params.lines | console code: def trapezium(f, a, b, n): / h = (b - a) / n / xs = [a + i * h for i in range(n)] / total = (... | correct | B21 |
| l12-no-formula.json | screens[5].question | Tap the line that loses a strip. | correct | B21 |
| l12-no-formula.json | screens[5].widget.answer | graded key (tap-regions): ["l3"] | correct | B21 |
| l12-no-formula.json | screens[5].hints[0].text | List the points `xs` holds for $n = 4$ on $[0, 1]$. | correct | B21 |
| l12-no-formula.json | screens[5].hints[1].text | `range(4)` gives `i` = 0, 1, 2, 3. | correct | B21 |
| l12-no-formula.json | screens[5].hints[2].text | So `xs` is 0, 0.25, 0.5, 0.75. The last point, 1, is missing. | correct | B21 |
| l12-no-formula.json | screens[5].feedback.correct | `range(n)` makes only $n$ points, so `xs` stops at $b - h$. | correct | B21 |
| l12-no-formula.json | screens[5].feedback.generic | Not quite right. Write out `xs` for $n = 4$ and check its last value. | correct | B21 |
| l12-no-formula.json | screens[5].feedback.byKey.l2 | Line 2 is right: $n$ strips of width $\tfrac{b - a}{n}$ span $[a, b]$. | correct | B21 |
| l12-no-formula.json | screens[5].feedback.byKey.l4 | You blamed the halved ends. Halving is right, but `xs[-1]` here is 0.75, not $b = 1$. The point list is short. | correct | B21 |
| l12-no-formula.json | screens[5].feedback.byKey.l5 | Skipping the two ends is right, since line 4 already counted them. | correct | B21 |
| l12-no-formula.json | screens[5].feedback.byKey.l7 | Multiplying by `h` once at the end is right; every strip has the same width. | correct | B21 |
| l12-no-formula.json | screens[5].explain.text | `range(n)` gives $n$ points, which bound only $n - 1$ strips, so Jo's sum ignores $[0.75, 1]$. Strips and p... | correct | B21 |
| l12-no-formula.json | screens[5].explain.canvas.lines | console code: def trapezium(f, a, b, n): / h = (b - a) / n / xs = [a + i * h for i in range(n + 1)] # was r... | correct | B21 |
| l12-no-formula.json | screens[6].prose | Jo's fixed loop is the **trapezium rule**, with $h = \frac{b - a}{n}$ and $x_i = a + ih$: $$T_n = h\left[\t... | correct | B21 |
| l12-no-formula.json | screens[6].question | You raise $n$ from 100 to 300. By about what factor does the error shrink? | correct | B21 |
| l12-no-formula.json | screens[6].widget.options[0].text | wrong option, wrong under every convention: 3 | correct | B21 |
| l12-no-formula.json | screens[6].widget.options[0].why | That would be an error shrinking like $h$. It shrinks like $h^2$, so a third of $h$ gives a ninth. | correct | B21 |
| l12-no-formula.json | screens[6].widget.options[1] | graded key (choice): 9 | correct | B21 |
| l12-no-formula.json | screens[6].widget.options[2].text | wrong option, wrong under every convention: 6 | correct | B21 |
| l12-no-formula.json | screens[6].widget.options[2].why | You doubled the factor 3. Squaring is what $h^2$ asks for: $3^2 = 9$. | correct | B21 |
| l12-no-formula.json | screens[6].hints[0].text | By what factor does $h$ shrink? | correct | B21 |
| l12-no-formula.json | screens[6].hints[1].text | $h$ becomes a third of its size. | correct | B21 |
| l12-no-formula.json | screens[6].hints[2].text | The error goes like $h^2$, so it falls by $3^2 = 9$. | correct | B21 |
| l12-no-formula.json | screens[6].feedback.correct | A third of $h$ gives a ninth of the error. | correct | B21 |
| l12-no-formula.json | screens[6].feedback.generic | Not quite right. Square the factor by which $h$ shrinks. | correct | B21 |
| l12-no-formula.json | screens[6].explain.text | Tripling $n$ makes $h$ a third as big, and the error scales like $h^2$. So the error falls by about 9. Doub... | correct | B21 |
| l12-no-formula.json | screens[7].prose | Why do the ends get $\tfrac{1}{2}$ and the inside points 1? Start from the strips and reach $T_n$. | correct | B21 |
| l12-no-formula.json | screens[7].question | Put the lines of the derivation in order. | correct | B21 |
| l12-no-formula.json | screens[7].widget.answer | graded key (order): ["strip", "sum", "count", "rule"] | correct | B21 |
| l12-no-formula.json | screens[7].widget.answer.order | graded order of 4 lines; each line follows from the one above | correct | B21 |
| l12-no-formula.json | screens[7].widget.lines[0].text | Strip $i$ has area $\tfrac{h}{2}\left[f(x_{i-1}) + f(x_i)\right]$: width times average height | correct | B21 |
| l12-no-formula.json | screens[7].widget.lines[1].text | Add the $n$ strips: $T_n = \tfrac{h}{2}\sum_{i=1}^{n}\left[f(x_{i-1}) + f(x_i)\right]$ | correct | B21 |
| l12-no-formula.json | screens[7].widget.lines[2].text | Each inside point is an edge of two strips, so it appears twice; $x_0$ and $x_n$ appear once | correct | B21 |
| l12-no-formula.json | screens[7].widget.lines[3].text | So $T_n = h\left[\tfrac{1}{2}f(x_0) + f(x_1) + \dots + f(x_{n-1}) + \tfrac{1}{2}f(x_n)\right]$ | correct | B21 |
| l12-no-formula.json | screens[7].hints[0].text | Begin with a single strip. | correct | B21 |
| l12-no-formula.json | screens[7].hints[1].text | After adding the strips, count how often each point appears. | correct | B21 |
| l12-no-formula.json | screens[7].hints[2].text | One strip, then the sum, then the count of appearances, then the tidy rule. | correct | B21 |
| l12-no-formula.json | screens[7].feedback.correct | Inside points appear twice and ends once, so $\tfrac{h}{2} \times 2 = h$ inside and $\tfrac{h}{2}$ at the e... | correct | B21 |
| l12-no-formula.json | screens[7].feedback.generic | Not quite right. Build up from one strip to the sum before counting. | correct | B21 |
| l12-no-formula.json | screens[7].feedback.byKey.rule | The tidy rule is the conclusion, so it comes last. | correct | B21 |
| l12-no-formula.json | screens[7].feedback.byKey.count | Counting appearances needs the sum written out first. | correct | B21 |
| l12-no-formula.json | screens[7].explain.text | Each inside point is shared by two strips, so its $\tfrac{h}{2}$ is counted twice and becomes $h$. The ends... | correct | B21 |
| l12-no-formula.json | screens[8].prose | Daily index returns, in standard units, are roughly normal with density $\phi(x) = \dfrac{e^{-x^2/2}}{\sqrt... | correct | B21 |
| l12-no-formula.json | screens[8].canvas.state.vlines[0].label | −1.96 | correct | B21 |
| l12-no-formula.json | screens[8].canvas.state.vlines[1].label | 1.96 | correct | B21 |
| l12-no-formula.json | screens[8].question | Write `phi(x)` and `prob_within(z, n)`, which uses `trapezium` with `n` strips. | correct | B21 |
| l12-no-formula.json | screens[8].widget.tests | 7 hidden tests, expected values recomputed | correct | B22 |
| l12-no-formula.json | screens[8].widget.solution | solution implements the stated method (composite trapezium; compare with exact) | correct | B22 |
| l12-no-formula.json | screens[8].widget.mutants[0] | mutant fails test 4 first: integrates from 0 to `z`: returns 0.475002 | correct | B22 |
| l12-no-formula.json | screens[8].widget.mutants[1] | mutant fails test 4 first: `phi()` raises TypeError inside test 4 | correct | B22 |
| l12-no-formula.json | screens[8].widget.mutants[2] | mutant fails test 4 first: `phi(x)` raises NameError inside test 4 | correct | B22 |
| l12-no-formula.json | screens[8].widget.how | Check runs 7 hidden tests: three values of `phi` and four calls to `prob_within`. Each result is accepted w... | correct | B21 |
| l12-no-formula.json | screens[8].hints[0].text | `phi` is one line with `math.exp`, `math.sqrt` and `math.pi`. | correct | B21 |
| l12-no-formula.json | screens[8].hints[1].text | The interval is symmetric: from `-z` to `z`. | correct | B21 |
| l12-no-formula.json | screens[8].hints[2].text | `return trapezium(phi, -z, z, n)`. Pass the function `phi` itself, without brackets. | correct | B21 |
| l12-no-formula.json | screens[8].feedback.correct | With 1,000 strips the chance is 0.950004: the familiar 95%. | correct | B21 |
| l12-no-formula.json | screens[8].feedback.generic | Not quite right. Read the first failing test. | correct | B21 |
| l12-no-formula.json | screens[8].feedback.byKey.test-1 | Test 1 expects $\phi(0) = \tfrac{1}{\sqrt{2\pi}} \approx 0.39894$. Check the square root and the $2\pi$. | correct | B23 |
| l12-no-formula.json | screens[8].feedback.byKey.test-4 | Test 4 expects 0.950004. Integrate `phi` from `-z` to `z`, not from 0 to `z`, and pass `phi` itself, withou... | correct | B23 |
| l12-no-formula.json | screens[8].feedback.byKey.error | Your code did not load. Read the last line of the message under the editor: a bracket or an indent is often... | correct | B23 |
| l12-no-formula.json | screens[8].explain.text | With 1,000 strips the area is 0.950004, against the exact 0.950004 to six places. So about 1 trading day in... | correct | B21 |
| l12-no-formula.json | screens[8].explain.canvas.area.label | ≈ 0.950 | correct | B21 |
| l12-no-formula.json | summary.ideas[0] | The trapezium rule tops each strip with a straight chord and adds width times average height. | correct | B21 |
| l12-no-formula.json | summary.ideas[1] | $n$ strips need $n + 1$ points, $x_i = a + ih$ for $i = 0$ to $n$. | correct | B21 |
| l12-no-formula.json | summary.ideas[2] | For a smooth $f$ the error shrinks like $h^2$: doubling $n$ cuts it by about 4. | correct | B21 |
| l12-no-formula.json | summary.formula.name | Trapezium rule | correct | B21 |
| l12-no-formula.json | summary.formula.tex | T_n = h\left[\tfrac{1}{2}f(x_0) + f(x_1) + \dots + f(x_{n-1}) + \tfrac{1}{2}f(x_n)\right] | correct | B21 |
| l12-no-formula.json | summary.formula.note | $h = \frac{b - a}{n}$. Exact for straight lines. | correct | B21 |
| l12-no-formula.json | summary.trap | `range(n)` gives $n$ points, which bound only $n - 1$ strips, so the last strip is lost. | correct | B21 |
| l12-no-formula.json | quiz[0].prose | Use the trapezium rule with $n = 2$ on $\int_0^2 x^3\,dx$, whose exact value is 4. | correct | B21 |
| l12-no-formula.json | quiz[0].question | What is $T_2$? | correct | B21 |
| l12-no-formula.json | quiz[0].widget.answer | graded key (numeric): 5 | correct | B21 |
| l12-no-formula.json | quiz[0].widget.wrong[0] | slip no-halves = 9 is the value of the named mistake and is not a correct answer | correct | B21 |
| l12-no-formula.json | quiz[0].widget.wrong[1] | slip half-h = 2.5 is the value of the named mistake and is not a correct answer | correct | B21 |
| l12-no-formula.json | quiz[0].widget.accept | 5: $h = 1$, so $T_2 = \tfrac{1}{2}(0) + 1 + \tfrac{1}{2}(8)$. | correct | B21 |
| l12-no-formula.json | quiz[0].feedback.correct | $1 \times \left[0 + 1 + 4\right] = 5$, an overestimate of 4. | correct | B21 |
| l12-no-formula.json | quiz[0].feedback.generic | Not quite right. Halve the end heights, keep the middle one, and multiply by $h = 1$. | correct | B21 |
| l12-no-formula.json | quiz[0].feedback.byKey.no-halves | You added all three heights in full. The two ends belong to one strip each, so halve them. | correct | B21 |
| l12-no-formula.json | quiz[0].feedback.byKey.half-h | You used $h = 0.5$. Two strips on $[0, 2]$ are each 1 wide. | correct | B21 |
| l12-no-formula.json | quiz[0].explain.text | $h = 1$ and the heights are 0, 1 and 8. So $T_2 = 1 \times \left[\tfrac{0}{2} + 1 + \tfrac{8}{2}\right] = 5... | correct | B21 |
| l12-no-formula.json | quiz[1].prose | A trapezium estimate with $n = 50$ strips has error 0.008. | correct | B21 |
| l12-no-formula.json | quiz[1].question | What error do you expect with $n = 100$? | correct | B21 |
| l12-no-formula.json | quiz[1].widget.answer | graded key (numeric): 0.002 | correct | B21 |
| l12-no-formula.json | quiz[1].widget.wrong[0] | slip halved = 0.004 is the value of the named mistake and is not a correct answer | correct | B21 |
| l12-no-formula.json | quiz[1].widget.accept | 0.002: a quarter of 0.008. | correct | B21 |
| l12-no-formula.json | quiz[1].feedback.correct | Doubling $n$ quarters the error: 0.002. | correct | B21 |
| l12-no-formula.json | quiz[1].feedback.generic | Not quite right. The error shrinks like $h^2$. | correct | B21 |
| l12-no-formula.json | quiz[1].feedback.byKey.halved | You halved it. $h$ halves, and the error goes like $h^2$, so it quarters. | correct | B21 |
| l12-no-formula.json | quiz[1].explain.text | Doubling $n$ halves $h$, and the error scales like $h^2$. So the error falls from 0.008 to $\tfrac{0.008}{4... | correct | B21 |
| l12-no-formula.json | quiz[2].prose | You compute $T_{10}$ on $[0, 5]$. | correct | B21 |
| l12-no-formula.json | quiz[2].question | At how many points must you evaluate $f$? | correct | B21 |
| l12-no-formula.json | quiz[2].widget.answer | graded key (numeric): 11 | correct | B21 |
| l12-no-formula.json | quiz[2].widget.wrong[0] | slip strips = 10 is the value of the named mistake and is not a correct answer | correct | B21 |
| l12-no-formula.json | quiz[2].widget.accept | 11: $x_0 = 0$ up to $x_{10} = 5$. | correct | B21 |
| l12-no-formula.json | quiz[2].feedback.correct | 10 strips need 11 edges. | correct | B21 |
| l12-no-formula.json | quiz[2].feedback.generic | Not quite right. Count edges, not strips. | correct | B21 |
| l12-no-formula.json | quiz[2].feedback.byKey.strips | You counted strips. Ten strips need eleven edges, both ends included. | correct | B21 |
| l12-no-formula.json | quiz[2].explain.text | With $h = 0.5$ the points are $0, 0.5, \dots, 5$: that is $x_0$ to $x_{10}$, eleven of them. | correct | B21 |
| l12-no-formula.json | quiz[3].prose | You apply the trapezium rule to a straight line, $f(x) = 3x + 2$, on $[0, 4]$. | correct | B21 |
| l12-no-formula.json | quiz[3].question | How many strips do you need for the exact answer? | correct | B21 |
| l12-no-formula.json | quiz[3].widget.options[0] | graded key (choice): One strip is already exact | correct | B21 |
| l12-no-formula.json | quiz[3].widget.options[1].text | wrong option, wrong under every convention: It is never exact, only close for large $n$ | correct | B21 |
| l12-no-formula.json | quiz[3].widget.options[1].why | The chord of a straight line is the line itself, so nothing is left over. | correct | B21 |
| l12-no-formula.json | quiz[3].widget.options[2].text | wrong option, wrong under every convention: Four, one per unit of width | correct | B21 |
| l12-no-formula.json | quiz[3].widget.options[2].why | Strip width does not matter for a line: its chord matches it exactly. | correct | B21 |
| l12-no-formula.json | quiz[3].feedback.correct | A chord of a straight line is the line, so $T_1$ is exact. | correct | B21 |
| l12-no-formula.json | quiz[3].feedback.generic | Not quite right. Picture the chord across one strip of a straight line. | correct | B21 |
| l12-no-formula.json | quiz[3].explain.text | For a straight line the chord and the curve coincide, so every $T_n$ is exact. Here $T_1 = 4 \times \tfrac{... | correct | B21 |
| l13-average-as-integral.json | screens[0].prose | The curve is $x^2$ on $[0, 3]$. Drag the handle to move the horizontal line. Blue is where the curve rises ... | correct | B24 |
| l13-average-as-integral.json | screens[0].canvas.params.functions[0].label | $x^2$ | correct | B24 |
| l13-average-as-integral.json | screens[0].canvas.derive.caption | Above the line: {{fixed(9 - 3*c + 2*pow(c, 1.5)/3, 2)}}. Below the line: {{fixed(2*pow(c, 1.5)/3, 2)}}. | correct | B24 |
| l13-average-as-integral.json | screens[0].question | Drag the line until the blue and orange areas are equal. | correct | B24 |
| l13-average-as-integral.json | screens[0].widget.points | graded key (drag-point): [{"id": "H", "target": [0.15, 3], "tol": [0.5, 0.15]}] | correct | B24 |
| l13-average-as-integral.json | screens[0].widget.wrong[0] | slip midrange = {"x": [0, 1], "y": [4.2, 4.8]} is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[0].widget.wrong[1] | slip mid-x = {"x": [0, 1], "y": [2.0, 2.5]} is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[0].hints[0].text | Watch the two numbers in the caption as you drag. | correct | B24 |
| l13-average-as-integral.json | screens[0].hints[1].text | If blue is bigger, the line is too low. | correct | B24 |
| l13-average-as-integral.json | screens[0].hints[2].text | The two areas match when the line is at height 3. | correct | B24 |
| l13-average-as-integral.json | screens[0].feedback.correct | At height 3 the two areas are both about 3.46. | correct | B24 |
| l13-average-as-integral.json | screens[0].feedback.generic | Not quite right. Keep dragging until the caption's two numbers match. | correct | B24 |
| l13-average-as-integral.json | screens[0].feedback.byKey.midrange | You put the line halfway between the lowest and highest values, 0 and 9. The curve spends most of its time ... | correct | B24 |
| l13-average-as-integral.json | screens[0].feedback.byKey.mid-x | You used the curve's height in the middle, $f(1.5) = 2.25$. The steep right end pulls the balance point hig... | correct | B24 |
| l13-average-as-integral.json | screens[0].feedback.byKey.H | The areas do not match yet. If blue is bigger, raise the line; if orange is bigger, lower it. | correct | B24 |
| l13-average-as-integral.json | screens[0].explain.text | The areas balance at height 3. Then the 3 by 3 rectangle under the line holds the same area as the curve do... | correct | B24 |
| l13-average-as-integral.json | screens[0].explain.canvas.points.H.label | height 3 | correct | B24 |
| l13-average-as-integral.json | screens[1].prose | The height you found is the **average value** of the function on the interval. Its rectangle has the same a... | correct | B24 |
| l13-average-as-integral.json | screens[1].canvas.params.functions[0].label | $6x^2$ | correct | B24 |
| l13-average-as-integral.json | screens[1].question | What is the average value of $6x^2$ on $[0, 2]$? | correct | B24 |
| l13-average-as-integral.json | screens[1].widget.answer | graded key (numeric): 8 | correct | B24 |
| l13-average-as-integral.json | screens[1].widget.wrong[0] | slip no-divide = 16 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[1].widget.wrong[1] | slip mid-x = 6 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[1].widget.wrong[2] | slip midrange = 12 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[1].widget.accept | 8: $\tfrac{1}{2}\int_0^2 6x^2\,dx = \tfrac{16}{2}$. | correct | B24 |
| l13-average-as-integral.json | screens[1].hints[0].text | Find the area under the curve first. | correct | B24 |
| l13-average-as-integral.json | screens[1].hints[1].text | $\int_0^2 6x^2\,dx = \left[2x^3\right]_0^2 = 16$. | correct | B24 |
| l13-average-as-integral.json | screens[1].hints[2].text | Divide the area by the width 2. | correct | B24 |
| l13-average-as-integral.json | screens[1].feedback.correct | Area 16 over width 2 gives average 8. | correct | B24 |
| l13-average-as-integral.json | screens[1].feedback.generic | Not quite right. Divide the area under the curve by the width of the interval. | correct | B24 |
| l13-average-as-integral.json | screens[1].feedback.byKey.no-divide | 16 is the area. The average height is the area divided by the width, 2. | correct | B24 |
| l13-average-as-integral.json | screens[1].feedback.byKey.mid-x | That is the height at the middle, $f(1) = 6$. The curve is steeper on the right, so its average is higher. | correct | B24 |
| l13-average-as-integral.json | screens[1].feedback.byKey.midrange | That is halfway between 0 and 24. The curve stays low for most of the interval. | correct | B24 |
| l13-average-as-integral.json | screens[1].explain.text | The area is $\int_0^2 6x^2\,dx = 16$ and the width is 2. So the average value is $\tfrac{16}{2} = 8$: the d... | correct | B24 |
| l13-average-as-integral.json | screens[1].explain.canvas.hlines[0].label | average 8 | correct | B24 |
| l13-average-as-integral.json | screens[2].prose | One arch of $\sin x$ runs from 0 to $\pi$. Its area is $\int_0^\pi \sin x\,dx = 2$. | correct | B24 |
| l13-average-as-integral.json | screens[2].question | What is the average value of $\sin x$ on $[0, \pi]$? Give 3 decimal places. | correct | B24 |
| l13-average-as-integral.json | screens[2].widget.answer | graded key (numeric): 0.6366 | correct | B24 |
| l13-average-as-integral.json | screens[2].widget.wrong[0] | slip midrange = 0.5 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[2].widget.wrong[1] | slip no-divide = 2 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[2].widget.wrong[2] | slip peak = 1 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[2].widget.accept | $\tfrac{2}{\pi} \approx 0.637$. | correct | B24 |
| l13-average-as-integral.json | screens[2].hints[0].text | Divide the area by the width. | correct | B24 |
| l13-average-as-integral.json | screens[2].hints[1].text | The width of $[0, \pi]$ is $\pi$. | correct | B24 |
| l13-average-as-integral.json | screens[2].hints[2].text | $\tfrac{2}{\pi} \approx 0.637$. | correct | B24 |
| l13-average-as-integral.json | screens[2].feedback.correct | $\tfrac{2}{\pi} \approx 0.637$. | correct | B24 |
| l13-average-as-integral.json | screens[2].feedback.generic | Not quite right. Divide the area 2 by the width $\pi$. | correct | B24 |
| l13-average-as-integral.json | screens[2].feedback.byKey.midrange | That is halfway between 0 and 1. The arch is flat near its top, so it spends longer up high. | correct | B24 |
| l13-average-as-integral.json | screens[2].feedback.byKey.no-divide | 2 is the area. Divide it by the width, $\pi$. | correct | B24 |
| l13-average-as-integral.json | screens[2].feedback.byKey.peak | That is the highest value. The average must sit between the lowest and highest. | correct | B24 |
| l13-average-as-integral.json | screens[2].explain.text | The average is $\tfrac{2}{\pi} \approx 0.637$, above the midrange 0.5. The arch stays near its top for a lo... | correct | B24 |
| l13-average-as-integral.json | screens[2].explain.canvas.hlines[0].label | average 0.637 | correct | B24 |
| l13-average-as-integral.json | screens[3].prose | A closing price $X$ is equally likely to be anywhere from £90 to £110: its **density** is $f(x) = \tfrac{1}... | correct | B24 |
| l13-average-as-integral.json | screens[3].canvas.params.functions[0].label | $f(x) = \tfrac{1}{20}$ | correct | B24 |
| l13-average-as-integral.json | screens[3].question | Compute $E[X] = \displaystyle\int_{90}^{110} x \cdot \tfrac{1}{20}\,dx$. | correct | B24 |
| l13-average-as-integral.json | screens[3].widget.answer | graded key (numeric): 100 | correct | B24 |
| l13-average-as-integral.json | screens[3].widget.wrong[0] | slip total = 1 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[3].widget.wrong[1] | slip no-density = 2000 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[3].widget.accept | £100.00: $\tfrac{1}{20}\left[\tfrac{x^2}{2}\right]_{90}^{110} = \tfrac{4000}{40}$. | correct | B24 |
| l13-average-as-integral.json | screens[3].hints[0].text | Take $\tfrac{1}{20}$ outside the integral. | correct | B24 |
| l13-average-as-integral.json | screens[3].hints[1].text | $\int_{90}^{110} x\,dx = \tfrac{110^2 - 90^2}{2} = 2000$. | correct | B24 |
| l13-average-as-integral.json | screens[3].hints[2].text | $\tfrac{2000}{20} = 100$. | correct | B24 |
| l13-average-as-integral.json | screens[3].feedback.correct | £100.00, the middle of the range, as symmetry says. | correct | B24 |
| l13-average-as-integral.json | screens[3].feedback.generic | Not quite right. Integrate $x$ times the density $\tfrac{1}{20}$. | correct | B24 |
| l13-average-as-integral.json | screens[3].feedback.byKey.total | That is $\int f(x)\,dx = 1$, the total probability. The mean needs the extra factor $x$. | correct | B24 |
| l13-average-as-integral.json | screens[3].feedback.byKey.no-density | That is $\int x\,dx$ alone. Weight it by the density $\tfrac{1}{20}$. | correct | B24 |
| l13-average-as-integral.json | screens[3].explain.text | $E[X] = \tfrac{1}{20} \cdot 2000 = 100$, the centre of the range. Here the density is flat, so $E[X]$ is ju... | correct | B24 |
| l13-average-as-integral.json | screens[3].explain.canvas.vlines[0].label | $E[X] = 100$ | correct | B24 |
| l13-average-as-integral.json | screens[4].prose | Now a lopsided density: $f(x) = \dfrac{x}{2}$ on $[0, 2]$. Its total area is 1, and it puts more weight on ... | correct | B24 |
| l13-average-as-integral.json | screens[4].canvas.params.functions[0].label | $f(x) = \frac{x}{2}$ | correct | B24 |
| l13-average-as-integral.json | screens[4].question | Compute $E[X] = \displaystyle\int_0^2 x \cdot \frac{x}{2}\,dx$. Give 3 decimal places. | correct | B24 |
| l13-average-as-integral.json | screens[4].widget.answer | graded key (numeric): 1.3333 | correct | B24 |
| l13-average-as-integral.json | screens[4].widget.wrong[0] | slip midpoint = 1 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[4].widget.wrong[1] | slip avg-density = 0.5 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[4].widget.wrong[2] | slip no-x = 2.6667 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[4].widget.accept | $\tfrac{4}{3} \approx 1.333$. | correct | B24 |
| l13-average-as-integral.json | screens[4].hints[0].text | The integrand is $\tfrac{x^2}{2}$. | correct | B24 |
| l13-average-as-integral.json | screens[4].hints[1].text | $\int_0^2 \tfrac{x^2}{2}\,dx = \left[\tfrac{x^3}{6}\right]_0^2$. | correct | B24 |
| l13-average-as-integral.json | screens[4].hints[2].text | $\tfrac{8}{6} = \tfrac{4}{3}$. | correct | B24 |
| l13-average-as-integral.json | screens[4].feedback.correct | $\left[\tfrac{x^3}{6}\right]_0^2 = \tfrac{4}{3}$. | correct | B24 |
| l13-average-as-integral.json | screens[4].feedback.generic | Not quite right. Integrate $\tfrac{x^2}{2}$ from 0 to 2. | correct | B24 |
| l13-average-as-integral.json | screens[4].feedback.byKey.midpoint | That is the middle of the range. The density leans right, so the mean does too. | correct | B24 |
| l13-average-as-integral.json | screens[4].feedback.byKey.avg-density | That is the average height of the density, $\tfrac{1}{2}\int_0^2 \tfrac{x}{2}\,dx$. The mean weights $x$, n... | correct | B24 |
| l13-average-as-integral.json | screens[4].feedback.byKey.no-x | You integrated $x \cdot x$ and dropped the $\tfrac12$ in the density. The integrand is $x \cdot \tfrac{x}{2}$. | correct | B24 |
| l13-average-as-integral.json | screens[4].explain.text | $E[X] = \int_0^2 \tfrac{x^2}{2}\,dx = \tfrac{4}{3}$. That is right of the midpoint 1, because the density i... | correct | B24 |
| l13-average-as-integral.json | screens[4].explain.canvas.vlines[0].label | $E[X] = \tfrac{4}{3}$ | correct | B24 |
| l13-average-as-integral.json | screens[5].prose | Back to the price $X$, uniform on £90 to £110. A call option struck at £100 pays $(X - 100)^+$: the excess ... | correct | B24 |
| l13-average-as-integral.json | screens[5].canvas.params.functions[0].label | payoff $(x - 100)^+$ | correct | B24 |
| l13-average-as-integral.json | screens[5].canvas.state.vlines[0].label | strike = $E[X]$ | correct | B24 |
| l13-average-as-integral.json | screens[5].canvas.state.caption | Density of $X$: $\tfrac{1}{20}$ on [£90, £110] | correct | B24 |
| l13-average-as-integral.json | screens[5].question | What is the expected payoff $E[(X - 100)^+]$? | correct | B24 |
| l13-average-as-integral.json | screens[5].widget.answer | graded key (numeric): 2.5 | correct | B24 |
| l13-average-as-integral.json | screens[5].widget.wrong[0] | slip at-mean = 0 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[5].widget.wrong[1] | slip only-in-money = 5 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[5].widget.wrong[2] | slip no-density = 50 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[5].widget.accept | £2.50: $\int_{100}^{110} (x - 100) \cdot \tfrac{1}{20}\,dx = \tfrac{50}{20}$. | correct | B24 |
| l13-average-as-integral.json | screens[5].hints[0].text | Write $E[g(X)] = \int g(x)\,f(x)\,dx$ with $g$ the payoff. | correct | B24 |
| l13-average-as-integral.json | screens[5].hints[1].text | The payoff is 0 below 100, so integrate from 100 to 110. | correct | B24 |
| l13-average-as-integral.json | screens[5].hints[2].text | $\tfrac{1}{20}\int_{100}^{110} (x - 100)\,dx = \tfrac{1}{20} \cdot 50$. | correct | B24 |
| l13-average-as-integral.json | screens[5].feedback.correct | £2.50, though the payoff at the expected price is £0.00. | correct | B24 |
| l13-average-as-integral.json | screens[5].feedback.generic | Not quite right. Weight the payoff by the density over the whole range. | correct | B24 |
| l13-average-as-integral.json | screens[5].feedback.byKey.at-mean | You took the payoff at the expected price, $(100 - 100)^+ = 0$. Averaging the payoff is different: half the... | correct | B24 |
| l13-average-as-integral.json | screens[5].feedback.byKey.only-in-money | You averaged the payoff over [£100, £110] only. Half the time the price is below 100 and the call pays noth... | correct | B24 |
| l13-average-as-integral.json | screens[5].feedback.byKey.no-density | 50 is the area under the payoff. Multiply by the density $\tfrac{1}{20}$. | correct | B24 |
| l13-average-as-integral.json | screens[5].explain.text | The payoff is 0 below £100, so $E = \tfrac{1}{20}\int_{100}^{110}(x - 100)\,dx = \tfrac{50}{20} = \text{£}2... | imprecise | Finding 4: true only when the bend lies inside the range of X; counter-example strike 80 in script (Jensen needs strict convexity on the support) |
| l13-average-as-integral.json | screens[5].explain.canvas.area.label | area 50 | correct | B24 |
| l13-average-as-integral.json | screens[6].prose | Turn the balancing line into a formula, then link it to expected value. | correct | B24 |
| l13-average-as-integral.json | screens[6].question | Put the lines of the derivation in order. | correct | B24 |
| l13-average-as-integral.json | screens[6].widget.answer | graded key (order): ["rect", "bal", "avg", "exp"] | correct | B24 |
| l13-average-as-integral.json | screens[6].widget.answer.order | graded order of 4 lines; each line follows from the one above | correct | B24 |
| l13-average-as-integral.json | screens[6].widget.lines[0].text | A line at height $c$ over $[a, b]$ makes a rectangle of area $c(b - a)$ | correct | B24 |
| l13-average-as-integral.json | screens[6].widget.lines[1].text | Balancing means the rectangle matches the curve: $c(b - a) = \int_a^b f(x)\,dx$ | correct | B24 |
| l13-average-as-integral.json | screens[6].widget.lines[2].text | Divide by $b - a$: $c = \dfrac{1}{b - a}\int_a^b f(x)\,dx$, the average value | correct | B24 |
| l13-average-as-integral.json | screens[6].widget.lines[3].text | With $X$ uniform on $[a, b]$, density $\tfrac{1}{b - a}$, this is $E[f(X)] = \int_a^b f(x)\,\tfrac{1}{b - a... | correct | B24 |
| l13-average-as-integral.json | screens[6].hints[0].text | Start with the rectangle under the line. | correct | B24 |
| l13-average-as-integral.json | screens[6].hints[1].text | Balance comes from equal areas. | correct | B24 |
| l13-average-as-integral.json | screens[6].hints[2].text | Rectangle, equal areas, divide, then read it as an expected value. | correct | B24 |
| l13-average-as-integral.json | screens[6].feedback.correct | The average value is the expected value of $f(X)$ for a uniform $X$. | correct | B24 |
| l13-average-as-integral.json | screens[6].feedback.generic | Not quite right. Start from the rectangle and end with the expected value. | correct | B24 |
| l13-average-as-integral.json | screens[6].feedback.byKey.exp | The expected-value reading needs the formula for $c$ first, so it comes last. | correct | B24 |
| l13-average-as-integral.json | screens[6].explain.text | Equal areas give $c(b - a) = \int_a^b f$, so $c$ is the area divided by the width. The factor $\tfrac{1}{b ... | correct | B24 |
| l13-average-as-integral.json | screens[7].prose | A broker fills an order evenly over a 4-hour session. The price follows $S(t) = 100 + 4t - t^2$ pounds, $t$... | correct | B24 |
| l13-average-as-integral.json | screens[7].question | What is the TWAP, $\dfrac{1}{4}\displaystyle\int_0^4 S(t)\,dt$? Give 2 decimal places. | correct | B24 |
| l13-average-as-integral.json | screens[7].widget.answer | graded key (numeric): 102.67 | correct | B24 |
| l13-average-as-integral.json | screens[7].widget.wrong[0] | slip ends = 100 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[7].widget.wrong[1] | slip peak = 104 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[7].widget.wrong[2] | slip no-divide = 410.67 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[7].widget.accept | £102.67: $\tfrac{1}{4}\left(400 + 32 - \tfrac{64}{3}\right)$. | correct | B24 |
| l13-average-as-integral.json | screens[7].hints[0].text | Integrate term by term. | correct | B24 |
| l13-average-as-integral.json | screens[7].hints[1].text | $\int_0^4 (100 + 4t - t^2)\,dt = 400 + 32 - \tfrac{64}{3}$. | correct | B24 |
| l13-average-as-integral.json | screens[7].hints[2].text | That is $410.67$. Divide by the 4 hours. | correct | B24 |
| l13-average-as-integral.json | screens[7].feedback.correct | £102.67: above the open and close, below the peak. | correct | B24 |
| l13-average-as-integral.json | screens[7].feedback.generic | Not quite right. Find the area under the price path, then divide by 4. | correct | B24 |
| l13-average-as-integral.json | screens[7].feedback.byKey.ends | You averaged the open and the close, both £100.00. The price spent the session above them. | correct | B24 |
| l13-average-as-integral.json | screens[7].feedback.byKey.peak | That is the highest price, at $t = 2$. The average sits below it. | correct | B24 |
| l13-average-as-integral.json | screens[7].feedback.byKey.no-divide | That is the area, in pound-hours. Divide by 4 hours to get a price. | correct | B24 |
| l13-average-as-integral.json | screens[7].explain.text | The area is $400 + 32 - \tfrac{64}{3} \approx 410.67$ pound-hours. Over 4 hours that is £102.67 a share. Th... | correct | B24 |
| l13-average-as-integral.json | screens[7].explain.canvas.hlines[0].label | TWAP £102.67 | correct | B24 |
| l13-average-as-integral.json | screens[8].prose | A better model makes prices near £100 more likely: a triangle on [£90, £110] with density $f(x) = \dfrac{10... | correct | B24 |
| l13-average-as-integral.json | screens[8].question | What is the expected payoff now? Give 2 decimal places. | correct | B24 |
| l13-average-as-integral.json | screens[8].widget.answer | graded key (numeric): 1.67 | correct | B24 |
| l13-average-as-integral.json | screens[8].widget.wrong[0] | slip uniform = 2.5 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[8].widget.wrong[1] | slip at-mean = 0 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[8].widget.wrong[2] | slip peak-density = 5 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | screens[8].widget.accept | £1.67: $\int_{100}^{110} (x - 100)\,\tfrac{110 - x}{100}\,dx = \tfrac{5}{3}$. | correct | B24 |
| l13-average-as-integral.json | screens[8].hints[0].text | Above £100 the density is $\tfrac{110 - x}{100}$. | correct | B24 |
| l13-average-as-integral.json | screens[8].hints[1].text | Put $y = x - 100$: the integral is $\tfrac{1}{100}\int_0^{10} y(10 - y)\,dy$. | correct | B24 |
| l13-average-as-integral.json | screens[8].hints[2].text | $\int_0^{10} (10y - y^2)\,dy = 500 - \tfrac{1000}{3} = \tfrac{500}{3}$. Divide by 100. | correct | B24 |
| l13-average-as-integral.json | screens[8].feedback.correct | £1.67, less than the £2.50 under the uniform model. | correct | B24 |
| l13-average-as-integral.json | screens[8].feedback.generic | Not quite right. Multiply the payoff by the triangular density and integrate from 100 to 110. | correct | B24 |
| l13-average-as-integral.json | screens[8].feedback.byKey.uniform | That is the uniform model's answer. The triangle puts less weight out at £110, where the call pays most. | correct | B24 |
| l13-average-as-integral.json | screens[8].feedback.byKey.at-mean | You took the payoff at the expected price. Average the payoff over the density instead. | correct | B24 |
| l13-average-as-integral.json | screens[8].feedback.byKey.peak-density | You used the peak density $\tfrac{1}{10}$ everywhere. The density falls to 0 at £110. | correct | B24 |
| l13-average-as-integral.json | screens[8].explain.text | $\tfrac{1}{100}\int_0^{10} y(10 - y)\,dy = \tfrac{1}{100} \cdot \tfrac{500}{3} \approx \text{£}1.67$. The t... | misleading | Finding 3: the uniform has the thinner tails (kurtosis 1.8 against 2.4); the gap comes from spread (sd 5.77 against 4.08); at equal sd the uniform is still worth more (MC in script) |
| l13-average-as-integral.json | summary.ideas[0] | The average value is the height of the rectangle with the same area: $\bar{f} = \frac{1}{b - a}\int_a^b f(x... | correct | B24 |
| l13-average-as-integral.json | summary.ideas[1] | For a density $f$, the mean weights each $x$ by its density: $E[X] = \int x\,f(x)\,dx$. | correct | B24 |
| l13-average-as-integral.json | summary.ideas[2] | An expected payoff is $E[g(X)] = \int g(x)\,f(x)\,dx$, which is not $g(E[X])$. | imprecise | Finding 4: needs "in general"; equal for a g that is linear on the support of X |
| l13-average-as-integral.json | summary.formula.name | Average value | correct | B24 |
| l13-average-as-integral.json | summary.formula.tex | \bar{f} = \frac{1}{b - a}\int_a^b f(x)\,dx | correct | B24 |
| l13-average-as-integral.json | summary.formula.note | With $X$ uniform on $[a, b]$, this is $E[f(X)]$. | correct | B24 |
| l13-average-as-integral.json | summary.trap | The payoff at the expected price is not the expected payoff. A call struck at the mean pays £0.00 there but... | correct | B24 |
| l13-average-as-integral.json | quiz[0].prose | Take $f(x) = 3x^2$ on $[0, 2]$. | correct | B24 |
| l13-average-as-integral.json | quiz[0].question | What is the average value of $f$ on $[0, 2]$? | correct | B24 |
| l13-average-as-integral.json | quiz[0].widget.answer | graded key (numeric): 4 | correct | B24 |
| l13-average-as-integral.json | quiz[0].widget.wrong[0] | slip no-divide = 8 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | quiz[0].widget.wrong[1] | slip mid-x = 3 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | quiz[0].widget.wrong[2] | slip ends = 6 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | quiz[0].widget.accept | 4: $\tfrac{1}{2}\int_0^2 3x^2\,dx = \tfrac{8}{2}$. | correct | B24 |
| l13-average-as-integral.json | quiz[0].feedback.correct | Area 8 over width 2 gives 4. | correct | B24 |
| l13-average-as-integral.json | quiz[0].feedback.generic | Not quite right. Divide the area under the curve by the width. | correct | B24 |
| l13-average-as-integral.json | quiz[0].feedback.byKey.no-divide | 8 is the area. Divide by the width 2. | correct | B24 |
| l13-average-as-integral.json | quiz[0].feedback.byKey.mid-x | That is $f(1)$, the height in the middle. A curving function's average differs from it. | correct | B24 |
| l13-average-as-integral.json | quiz[0].feedback.byKey.ends | That averages the end values 0 and 12. The curve is low for most of the interval. | correct | B24 |
| l13-average-as-integral.json | quiz[0].explain.text | $\int_0^2 3x^2\,dx = 8$, and the width is 2. So the average value is 4. | correct | B24 |
| l13-average-as-integral.json | quiz[1].prose | Take $\sin x$ over a full wave, $[0, 2\pi]$. | correct | B24 |
| l13-average-as-integral.json | quiz[1].question | What is its average value? | correct | B24 |
| l13-average-as-integral.json | quiz[1].widget.options[0] | graded key (choice): 0 | correct | B24 |
| l13-average-as-integral.json | quiz[1].widget.options[1].text | wrong option, wrong under every convention: $\dfrac{2}{\pi}$ | correct | B24 |
| l13-average-as-integral.json | quiz[1].widget.options[1].why | That is the average over one arch, $[0, \pi]$. The second arch is below the axis and cancels the first. | correct | B24 |
| l13-average-as-integral.json | quiz[1].widget.options[2].text | wrong option, wrong under every convention: $\dfrac{1}{2}$ | correct | B24 |
| l13-average-as-integral.json | quiz[1].widget.options[2].why | That is halfway between 0 and 1. The wave also goes down to $-1$. | correct | B24 |
| l13-average-as-integral.json | quiz[1].feedback.correct | The two arches have signed areas 2 and $-2$, so the average is 0. | correct | B24 |
| l13-average-as-integral.json | quiz[1].feedback.generic | Not quite right. Find $\int_0^{2\pi} \sin x\,dx$ first. | correct | B24 |
| l13-average-as-integral.json | quiz[1].explain.text | $\int_0^{2\pi} \sin x\,dx = 0$: the arch below the axis cancels the arch above. So the average value is 0, ... | correct | B24 |
| l13-average-as-integral.json | quiz[2].prose | A random variable $X$ has density $f(x) = 3x^2$ on $[0, 1]$. | correct | B24 |
| l13-average-as-integral.json | quiz[2].question | What is $E[X]$? | correct | B24 |
| l13-average-as-integral.json | quiz[2].widget.answer | graded key (numeric): 0.75 | correct | B24 |
| l13-average-as-integral.json | quiz[2].widget.wrong[0] | slip midpoint = 0.5 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | quiz[2].widget.wrong[1] | slip total = 1 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | quiz[2].widget.accept | $\tfrac{3}{4}$: $\int_0^1 3x^3\,dx$. | correct | B24 |
| l13-average-as-integral.json | quiz[2].feedback.correct | $\int_0^1 x \cdot 3x^2\,dx = \tfrac{3}{4}$. | correct | B24 |
| l13-average-as-integral.json | quiz[2].feedback.generic | Not quite right. Integrate $x$ times the density. | correct | B24 |
| l13-average-as-integral.json | quiz[2].feedback.byKey.midpoint | That is the middle of the range. The density leans right, so the mean does too. | correct | B24 |
| l13-average-as-integral.json | quiz[2].feedback.byKey.total | That is $\int f(x)\,dx$, the total probability. Multiply by $x$ inside the integral. | correct | B24 |
| l13-average-as-integral.json | quiz[2].explain.text | $E[X] = \int_0^1 3x^3\,dx = \left[\tfrac{3x^4}{4}\right]_0^1 = \tfrac{3}{4}$. | correct | B24 |
| l13-average-as-integral.json | quiz[3].prose | A price $X$ is uniform on £90 to £110. A put struck at £100 pays $(100 - X)^+$. | correct | B24 |
| l13-average-as-integral.json | quiz[3].question | What is the expected payoff of the put? | correct | B24 |
| l13-average-as-integral.json | quiz[3].widget.answer | graded key (numeric): 2.5 | correct | B24 |
| l13-average-as-integral.json | quiz[3].widget.wrong[0] | slip at-mean = 0 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | quiz[3].widget.wrong[1] | slip only-in-money = 5 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | quiz[3].widget.wrong[2] | slip no-density = 50 is the value of the named mistake and is not a correct answer | correct | B24 |
| l13-average-as-integral.json | quiz[3].widget.accept | £2.50: $\tfrac{1}{20}\int_{90}^{100} (100 - x)\,dx$. | correct | B24 |
| l13-average-as-integral.json | quiz[3].feedback.correct | £2.50, by the same reasoning as the call. | correct | B24 |
| l13-average-as-integral.json | quiz[3].feedback.generic | Not quite right. Weight the payoff by the density $\tfrac{1}{20}$. | correct | B24 |
| l13-average-as-integral.json | quiz[3].feedback.byKey.at-mean | That is the payoff at the expected price. Average the payoff instead. | correct | B24 |
| l13-average-as-integral.json | quiz[3].feedback.byKey.only-in-money | You averaged over [£90, £100] only. Half the time the put pays nothing. | correct | B24 |
| l13-average-as-integral.json | quiz[3].feedback.byKey.no-density | 50 is the area under the payoff. Multiply by the density $\tfrac{1}{20}$. | correct | B24 |
| l13-average-as-integral.json | quiz[3].explain.text | The put pays only below £100: $\tfrac{1}{20}\int_{90}^{100} (100 - x)\,dx = \tfrac{50}{20} = \text{£}2.50$. | correct | B24 |
| review-3.json | items[0].prose | Use $u = x^2 + 1$ on $\displaystyle\int_0^2 \frac{x}{x^2 + 1}\,dx$. | correct | B25 |
| review-3.json | items[0].question | What is the value? Give 4 decimal places. | correct | B25 |
| review-3.json | items[0].widget.answer | graded key (numeric): 0.8047 | correct | B25 |
| review-3.json | items[0].widget.wrong[0] | slip forgot-half = 1.6094 is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[0].widget.accept | $\tfrac{1}{2}\ln 5 \approx 0.8047$. | correct | B25 |
| review-3.json | items[0].feedback.correct | $\tfrac{1}{2}\int_1^5 \tfrac{du}{u} = \tfrac{1}{2}\ln 5$. | correct | B25 |
| review-3.json | items[0].feedback.generic | Not quite right. Write $x\,dx$ in terms of $du$ and move the limits to $u$ values. | correct | B25 |
| review-3.json | items[0].feedback.byKey.forgot-half | You used $x\,dx = du$. Since $du = 2x\,dx$, it is $\tfrac{1}{2}\,du$. | correct | B25 |
| review-3.json | items[0].explain.text | $du = 2x\,dx$, so $x\,dx = \tfrac{1}{2}\,du$, and $u$ runs from 1 to 5. The integral is $\tfrac{1}{2}(\ln 5... | correct | B25 |
| review-3.json | items[1].prose | Use parts on $\displaystyle\int x\sin x\,dx$. | correct | B25 |
| review-3.json | items[1].question | Complete $\int x\sin x\,dx = \;? + C$. | correct | B25 |
| review-3.json | items[1].widget.answer | graded key (expression): "\\sin x-x\\cos x" | correct | B25 |
| review-3.json | items[1].widget.wrong[0] | slip sign = "x\\cos x-\\sin x" is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[1].widget.wrong[1] | slip no-integral = "-x\\cos x" is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[1].feedback.correct | $u = x$, $v = -\cos x$: $-x\cos x + \int \cos x\,dx = \sin x - x\cos x$. | correct | B25 |
| review-3.json | items[1].feedback.generic | Not quite right. Take $u = x$ and $dv = \sin x\,dx$, and find $v$ carefully. | correct | B25 |
| review-3.json | items[1].feedback.byKey.sign | You took $v = \cos x$. Its derivative is $-\sin x$, so $v = -\cos x$. | correct | B25 |
| review-3.json | items[1].feedback.byKey.no-integral | You stopped at $uv$. Subtract $\int v\,du = -\int \cos x\,dx$ too. | correct | B25 |
| review-3.json | items[1].explain.text | With $u = x$ and $v = -\cos x$, parts gives $-x\cos x + \int \cos x\,dx = \sin x - x\cos x + C$. Its deriva... | correct | B25 |
| review-3.json | items[2].prose | This tail starts at 2 instead of 1. | correct | B25 |
| review-3.json | items[2].question | Evaluate $\displaystyle\int_2^\infty \frac{1}{x^2}\,dx$. | correct | B25 |
| review-3.json | items[2].widget.answer | graded key (numeric): 0.5 | correct | B25 |
| review-3.json | items[2].widget.wrong[0] | slip from-one = 1 is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[2].widget.wrong[1] | slip sign = -0.5 is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[2].widget.accept | $\tfrac{1}{2}$: $\left[-\tfrac{1}{x}\right]_2^b \to \tfrac{1}{2}$. | correct | B25 |
| review-3.json | items[2].feedback.correct | $\tfrac{1}{2} - \tfrac{1}{b} \to \tfrac{1}{2}$. | correct | B25 |
| review-3.json | items[2].feedback.generic | Not quite right. Evaluate $-\tfrac{1}{x}$ from 2 to $b$, then let $b \to \infty$. | correct | B25 |
| review-3.json | items[2].feedback.byKey.from-one | That is the tail from 1. Starting at 2 leaves out the strip from 1 to 2. | correct | B25 |
| review-3.json | items[2].feedback.byKey.sign | You subtracted the wrong way round. The curve is above the axis, so the area is positive. | correct | B25 |
| review-3.json | items[2].explain.text | $\int_2^b x^{-2}\,dx = \tfrac{1}{2} - \tfrac{1}{b}$, which tends to $\tfrac{1}{2}$. The strip from 1 to 2 h... | correct | B25 |
| review-3.json | items[3].prose | Estimate $\displaystyle\int_1^3 \frac{1}{x}\,dx$ with the trapezium rule and $n = 2$ strips. | correct | B25 |
| review-3.json | items[3].question | What is $T_2$? Give 4 decimal places. | correct | B25 |
| review-3.json | items[3].widget.answer | graded key (numeric): 1.1667 | correct | B25 |
| review-3.json | items[3].widget.wrong[0] | slip exact = 1.0986 is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[3].widget.wrong[1] | slip no-halves = 1.8333 is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[3].widget.wrong[2] | slip half-h = 0.5833 is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[3].widget.accept | $\tfrac{7}{6} \approx 1.1667$: $h = 1$, so $T_2 = \tfrac{1}{2} + \tfrac{1}{2} + \tfrac{1}{6}$. | correct | B25 |
| review-3.json | items[3].feedback.correct | $1 \times \left[\tfrac{1}{2} \cdot 1 + \tfrac{1}{2} + \tfrac{1}{2} \cdot \tfrac{1}{3}\right] = \tfrac{7}{6}$. | correct | B25 |
| review-3.json | items[3].feedback.generic | Not quite right. Use $h = 1$, halve the two end heights, and keep the middle one. | correct | B25 |
| review-3.json | items[3].feedback.byKey.exact | That is the exact value, $\ln 3$. The question asks for the trapezium estimate. | correct | B25 |
| review-3.json | items[3].feedback.byKey.no-halves | You added all three heights in full. The ends belong to one strip each, so halve them. | correct | B25 |
| review-3.json | items[3].feedback.byKey.half-h | You used $h = 0.5$. Two strips on $[1, 3]$ are each 1 wide. | correct | B25 |
| review-3.json | items[3].explain.text | The heights at 1, 2 and 3 are 1, $\tfrac{1}{2}$ and $\tfrac{1}{3}$. So $T_2 = \tfrac{1}{2} + \tfrac{1}{2} +... | correct | B25 |
| review-3.json | items[4].prose | Take $f(x) = x^2$ on $[0, 2]$. | correct | B25 |
| review-3.json | items[4].question | What is its average value? Give 3 decimal places. | correct | B25 |
| review-3.json | items[4].widget.answer | graded key (numeric): 1.3333 | correct | B25 |
| review-3.json | items[4].widget.wrong[0] | slip no-divide = 2.6667 is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[4].widget.wrong[1] | slip mid-x = 1 is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[4].widget.wrong[2] | slip midrange = 2 is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[4].widget.accept | $\tfrac{4}{3} \approx 1.333$. | correct | B25 |
| review-3.json | items[4].feedback.correct | Area $\tfrac{8}{3}$ over width 2 is $\tfrac{4}{3}$. | correct | B25 |
| review-3.json | items[4].feedback.generic | Not quite right. Divide the area under the curve by the width. | correct | B25 |
| review-3.json | items[4].feedback.byKey.no-divide | $\tfrac{8}{3}$ is the area. Divide by the width 2. | correct | B25 |
| review-3.json | items[4].feedback.byKey.mid-x | That is $f(1)$, the middle height. A curving function's average differs from it. | correct | B25 |
| review-3.json | items[4].feedback.byKey.midrange | That averages the end values 0 and 4. The curve is low for most of the interval. | correct | B25 |
| review-3.json | items[4].explain.text | $\int_0^2 x^2\,dx = \tfrac{8}{3}$, and the width is 2. So the average value is $\tfrac{4}{3}$. | correct | B25 |
| review-3.json | items[5].prose | Combine substitution with a limit: $\displaystyle\int_0^\infty x\,e^{-x^2}\,dx$. | correct | B25 |
| review-3.json | items[5].question | What is the value? | correct | B25 |
| review-3.json | items[5].widget.answer | graded key (numeric): 0.5 | correct | B25 |
| review-3.json | items[5].widget.wrong[0] | slip forgot-half = 1 is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[5].widget.wrong[1] | slip sign = -0.5 is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[5].widget.accept | $\tfrac{1}{2}$. | correct | B25 |
| review-3.json | items[5].feedback.correct | With $u = x^2$: $\tfrac{1}{2}\int_0^\infty e^{-u}\,du = \tfrac{1}{2}$. | correct | B25 |
| review-3.json | items[5].feedback.generic | Not quite right. Substitute $u = x^2$, then let the upper limit grow. | correct | B25 |
| review-3.json | items[5].feedback.byKey.forgot-half | You used $x\,dx = du$. It is $\tfrac{1}{2}\,du$. | correct | B25 |
| review-3.json | items[5].feedback.byKey.sign | The integrand is positive for $x > 0$, so the area is positive. Check the order of subtraction. | correct | B25 |
| review-3.json | items[5].explain.text | $u = x^2$ gives $x\,dx = \tfrac{1}{2}\,du$, and $u$ runs from 0 to $\infty$. Then $\tfrac{1}{2}\int_0^b e^{... | correct | B25 |
| review-3.json | items[6].prose | A waiting time $T$ has density $e^{-t}$ for $t \ge 0$. Its mean is $E[T] = \displaystyle\int_0^\infty t\,e^... | correct | B25 |
| review-3.json | items[6].question | What is $E[T]$? | correct | B25 |
| review-3.json | items[6].widget.answer | graded key (numeric): 1 | correct | B25 |
| review-3.json | items[6].widget.wrong[0] | slip upper-only = 0 is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[6].widget.wrong[1] | slip sign = -1 is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[6].widget.accept | 1: $\left[-(t + 1)e^{-t}\right]_0^b \to 1$. | correct | B25 |
| review-3.json | items[6].feedback.correct | Parts with $u = t$ gives $-(t + 1)e^{-t}$, which runs from $-1$ at 0 up to 0. | correct | B25 |
| review-3.json | items[6].feedback.generic | Not quite right. Use parts with $u = t$, evaluate to $b$, then let $b$ grow. | correct | B25 |
| review-3.json | items[6].feedback.byKey.upper-only | You evaluated at the upper end only. At $t = 0$ the antiderivative is $-1$; subtract it. | correct | B25 |
| review-3.json | items[6].feedback.byKey.sign | You subtracted the wrong way round. $F(b) - F(0) = 0 - (-1) = 1$. | correct | B25 |
| review-3.json | items[6].explain.text | $u = t$, $dv = e^{-t}\,dt$ gives $\int t\,e^{-t}\,dt = -(t + 1)e^{-t}$. From 0 to $b$ this is $1 - (b + 1)e... | correct | B25 |
| review-3.json | items[7].prose | A trapezium estimate uses $n = 20$ strips. You rerun it with $n = 80$. | correct | B25 |
| review-3.json | items[7].question | By about what factor does the error shrink? | correct | B25 |
| review-3.json | items[7].widget.options[0].text | wrong option, wrong under every convention: 4 | correct | B25 |
| review-3.json | items[7].widget.options[0].why | That is the factor for $h$, not for the error. The error goes like $h^2$. | correct | B25 |
| review-3.json | items[7].widget.options[1].text | wrong option, wrong under every convention: 8 | correct | B25 |
| review-3.json | items[7].widget.options[1].why | You doubled the factor 4. Square it instead: the error goes like $h^2$. | correct | B25 |
| review-3.json | items[7].widget.options[2] | graded key (choice): 16 | correct | B25 |
| review-3.json | items[7].feedback.correct | $h$ falls by 4, so the error falls by $4^2 = 16$. | correct | B25 |
| review-3.json | items[7].feedback.generic | Not quite right. Square the factor by which $h$ shrinks. | correct | B25 |
| review-3.json | items[7].explain.text | Four times as many strips makes $h$ a quarter as big. The error scales like $h^2$, so it falls by about 16. | correct | B25 |
| review-3.json | items[8].prose | A price $X$ is uniform on £90 to £110. A call struck at £105 pays $(X - 105)^+$. | correct | B25 |
| review-3.json | items[8].question | What is the expected payoff? | correct | B25 |
| review-3.json | items[8].widget.answer | graded key (numeric): 0.625 | correct | B25 |
| review-3.json | items[8].widget.wrong[0] | slip at-mean = 0 is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[8].widget.wrong[1] | slip no-density = 12.5 is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[8].widget.wrong[2] | slip only-in-money = 2.5 is the value of the named mistake and is not a correct answer | correct | B25 |
| review-3.json | items[8].widget.accept | £0.63, exactly 0.625: $\tfrac{1}{20}\int_{105}^{110} (x - 105)\,dx = \tfrac{12.5}{20}$. | wrong | Finding 2: the line prints "£0.63" as accepted, but tol abs 0.001 around 0.625 rejects 0.63 (js/engine/grade.js within(); script check fails) |
| review-3.json | items[8].feedback.correct | About £0.63: a quarter of the time it pays, on average £2.50. | correct | B25 |
| review-3.json | items[8].feedback.generic | Not quite right. Weight the payoff by the density $\tfrac{1}{20}$ over the whole range. | correct | B25 |
| review-3.json | items[8].feedback.byKey.at-mean | That is the payoff at the expected price. Average the payoff over the density instead. | correct | B25 |
| review-3.json | items[8].feedback.byKey.no-density | 12.5 is the area under the payoff. Multiply by the density $\tfrac{1}{20}$. | correct | B25 |
| review-3.json | items[8].feedback.byKey.only-in-money | You averaged over [£105, £110] only. Three quarters of the time the call pays nothing. | correct | B25 |
| review-3.json | items[8].explain.text | The call pays only above £105: $\tfrac{1}{20}\int_{105}^{110} (x - 105)\,dx = \tfrac{12.5}{20} = 0.625$. Th... | correct | B25 |
| homework-3.json | items[0].prose | Find $\displaystyle\int x^2 e^{x^3}\,dx$ by substitution. | correct | B26 |
| homework-3.json | items[0].question | Complete $\int x^2 e^{x^3}\,dx = \;? + C$. | correct | B26 |
| homework-3.json | items[0].widget.answer | graded key (expression): "\\frac{1}{3}e^{x^3}" | correct | B26 |
| homework-3.json | items[0].widget.wrong[0] | slip forgot-third = "e^{x^3}" is the value of the named mistake and is not a correct answer | correct | B26 |
| homework-3.json | items[0].widget.wrong[1] | slip tripled = "3e^{x^3}" is the value of the named mistake and is not a correct answer | correct | B26 |
| homework-3.json | items[0].feedback.correct | $u = x^3$, $x^2\,dx = \tfrac{1}{3}\,du$, so the answer is $\tfrac{1}{3}e^{x^3} + C$. | correct | B26 |
| homework-3.json | items[0].feedback.generic | Not quite right. Take $u = x^3$ and write $x^2\,dx$ in terms of $du$. | correct | B26 |
| homework-3.json | items[0].feedback.byKey.forgot-third | You used $x^2\,dx = du$. Since $du = 3x^2\,dx$, it is $\tfrac{1}{3}\,du$. | correct | B26 |
| homework-3.json | items[0].feedback.byKey.tripled | You multiplied by 3. The missing factor is divided out: $x^2\,dx = \tfrac{1}{3}\,du$. | correct | B26 |
| homework-3.json | items[0].explain.text | With $u = x^3$, $du = 3x^2\,dx$, so the integral is $\tfrac{1}{3}\int e^u\,du = \tfrac{1}{3}e^{x^3} + C$. D... | correct | B26 |
| homework-3.json | items[1].prose | Find $\displaystyle\int x^2 \ln x\,dx$ for $x > 0$. | correct | B26 |
| homework-3.json | items[1].question | Complete $\int x^2\ln x\,dx = \;? + C$. | correct | B26 |
| homework-3.json | items[1].widget.answer | graded key (expression): "\\frac{x^3}{3}\\ln x-\\frac{x^3}{9}" | correct | B26 |
| homework-3.json | items[1].widget.wrong[0] | slip no-second-divide = "\\frac{x^3}{3}\\ln x-\\frac{x^3}{3}" is the value of the named mistake and is not ... | correct | B26 |
| homework-3.json | items[1].widget.wrong[1] | slip no-integral = "\\frac{x^3}{3}\\ln x" is the value of the named mistake and is not a correct answer | correct | B26 |
| homework-3.json | items[1].feedback.correct | $u = \ln x$, $v = \tfrac{x^3}{3}$: $\tfrac{x^3}{3}\ln x - \int \tfrac{x^2}{3}\,dx = \tfrac{x^3}{3}\ln x - \... | correct | B26 |
| homework-3.json | items[1].feedback.generic | Not quite right. Take $u = \ln x$ and $dv = x^2\,dx$. | correct | B26 |
| homework-3.json | items[1].feedback.byKey.no-second-divide | You integrated $\tfrac{x^2}{3}$ as $\tfrac{x^3}{3}$. Raising the power divides by 3 again: $\tfrac{x^3}{9}$. | correct | B26 |
| homework-3.json | items[1].feedback.byKey.no-integral | You stopped at $uv$. Subtract $\int v\,du = \int \tfrac{x^2}{3}\,dx$ too. | correct | B26 |
| homework-3.json | items[1].explain.text | $u = \ln x$ gives $du = \tfrac{1}{x}\,dx$, and $v = \tfrac{x^3}{3}$. The new integral is $\int \tfrac{x^2}{... | correct | B26 |
| homework-3.json | items[2].prose | Parts can loop back to where it started. Let $I = \displaystyle\int e^x \sin x\,dx$. Two rounds of parts br... | correct | B26 |
| homework-3.json | items[2].question | Put the lines of the derivation in order. | correct | B26 |
| homework-3.json | items[2].widget.answer | graded key (order): ["r1", "r2", "sub", "add", "solve"] | correct | B26 |
| homework-3.json | items[2].widget.answer.order | graded order of 5 lines; each line follows from the one above | correct | B26 |
| homework-3.json | items[2].widget.lines[0].text | Parts with $u = \sin x$, $dv = e^x\,dx$: $I = e^x\sin x - \int e^x\cos x\,dx$ | correct | B26 |
| homework-3.json | items[2].widget.lines[1].text | Parts with $u = \cos x$, $dv = e^x\,dx$: $\int e^x\cos x\,dx = e^x\cos x + \int e^x\sin x\,dx$ | correct | B26 |
| homework-3.json | items[2].widget.lines[2].text | Substitute the second line into the first: $I = e^x\sin x - e^x\cos x - I$ | correct | B26 |
| homework-3.json | items[2].widget.lines[3].text | Add $I$ to both sides: $2I = e^x(\sin x - \cos x)$ | correct | B26 |
| homework-3.json | items[2].widget.lines[4].text | Divide by 2 and add the constant: $I = \tfrac{1}{2}e^x(\sin x - \cos x) + C$ | correct | B26 |
| homework-3.json | items[2].feedback.correct | Two rounds bring back $I$; collecting it gives $I = \tfrac{1}{2}e^x(\sin x - \cos x) + C$. | correct | B26 |
| homework-3.json | items[2].feedback.generic | Not quite right. Do both rounds of parts before you substitute. | correct | B26 |
| homework-3.json | items[2].feedback.byKey.sub | The substitution needs the second round's result, so round 2 comes first. | correct | B26 |
| homework-3.json | items[2].feedback.byKey.add | You can only collect $I$ once it appears on both sides. | correct | B26 |
| homework-3.json | items[2].explain.text | Round 2 gives $+\int e^x\sin x\,dx$ because $du = -\sin x\,dx$ and the two minus signs cancel. That integra... | correct | B26 |
| homework-3.json | items[3].prose | A royalty pays continuously at a rate that grows in a straight line. At time $t$ it pays £$t$ a year, forev... | correct | B26 |
| homework-3.json | items[3].question | What is the royalty worth today? | correct | B26 |
| homework-3.json | items[3].widget.answer | graded key (numeric): 400 | correct | B26 |
| homework-3.json | items[3].widget.wrong[0] | slip one-over-r = 20 is the value of the named mistake and is not a correct answer | correct | B26 |
| homework-3.json | items[3].widget.wrong[1] | slip cube = 8000 is the value of the named mistake and is not a correct answer | correct | B26 |
| homework-3.json | items[3].widget.accept | £400.00: $\tfrac{1}{0.05^2}$. | correct | B26 |
| homework-3.json | items[3].feedback.correct | $\tfrac{1}{r^2} = \tfrac{1}{0.0025} = \text{£}400.00$. | correct | B26 |
| homework-3.json | items[3].feedback.generic | Not quite right. Use parts with $u = t$, evaluate to $b$, then let $b \to \infty$. | correct | B26 |
| homework-3.json | items[3].feedback.byKey.one-over-r | That is the flat perpetuity, $\tfrac{1}{r}$. Here the payments grow, so a factor $\tfrac{1}{r}$ more appears. | correct | B26 |
| homework-3.json | items[3].feedback.byKey.cube | You divided by $r$ three times. Parts gives $\tfrac{1}{r} \cdot \tfrac{1}{r}$. | correct | B26 |
| homework-3.json | items[3].explain.text | Parts with $u = t$ gives $\int_0^b t\,e^{-rt}\,dt = -\tfrac{b}{r}e^{-rb} + \tfrac{1 - e^{-rb}}{r^2}$. Both ... | correct | B26 |
| homework-3.json | items[4].prose | How many strips are enough? Write `trapezium(f, a, b, n)` and `n_needed(f, a, b, exact, tol)`. `n_needed` t... | correct | B26 |
| homework-3.json | items[4].question | Write both functions. | correct | B26 |
| homework-3.json | items[4].widget.tests | 8 hidden tests, expected values recomputed | correct | B22 |
| homework-3.json | items[4].widget.solution | solution implements the stated method (composite trapezium; compare with exact) | correct | B22 |
| homework-3.json | items[4].widget.mutants[0] | mutant fails test 8 first: stops when $T_{2n}$ and $T_n$ agree: returns 32 | correct | B22 |
| homework-3.json | items[4].widget.mutants[1] | mutant fails test 8 first: compares each estimate with the one before: returns 32 | correct | B22 |
| homework-3.json | items[4].widget.mutants[2] | mutant fails test 8 first: successive estimates in a bounded loop: returns 32 | correct | B22 |
| homework-3.json | items[4].widget.how | Check runs 8 hidden tests. `trapezium` results are accepted when `math.isclose(result, expected, rel_tol=1e... | correct | B26 |
| homework-3.json | items[4].feedback.correct | Doubling $n$ until the error drops below `tol` finds the smallest power of 2 that works. | correct | B26 |
| homework-3.json | items[4].feedback.generic | Not quite right. Read the first failing test. | correct | B26 |
| homework-3.json | items[4].feedback.byKey.test-1 | Test 1 expects $T_3$ for $x^2$ on $[0, 1]$, about 0.35185. Check that you make exactly `n` strips of width ... | correct | B23 |
| homework-3.json | items[4].feedback.byKey.test-4 | Test 4 is a straight line, which $T_1$ gets exactly. Start the search at `n = 1` and test before doubling. | correct | B23 |
| homework-3.json | items[4].feedback.byKey.test-3 | Test 3 expects 64: at $n = 32$ the error is 0.000163, still above 0.0001. Stop only when the error is below... | imprecise | Finding 10: true of its test, but the natural successive-estimate coding that returns the finer n fails test 3 first with 128 (sweep), so "stop only when below tol" misdescribes it |
| homework-3.json | items[4].feedback.byKey.test-8 | Test 8 expects 64. Compare each estimate with `exact`, not with the estimate before it. | imprecise | Finding 10: fires for the coarser-n codings only (3 mutants, sweep); the finer-n coding gets test-3, the |T2n-Tn|/3 coding gets test-4 |
| homework-3.json | items[4].feedback.byKey.error | Your code stopped with an error. Read the last line of the message under the editor. | correct | B23 |
| homework-3.json | items[4].explain.text | For $x^2$ the error is $\tfrac{1}{6n^2}$, so it first drops below 0.0001 at $n = 64$. A straight line needs... | correct | B26 |
| homework-3.json | items[5].prose | A price $X$ has the triangular density $f(x) = \dfrac{10 - \|x - 100\|}{100}$ on [£90, £110]. A call struck... | correct | B26 |
| homework-3.json | items[5].question | What is the expected payoff? Give 2 decimal places. | correct | B26 |
| homework-3.json | items[5].widget.answer | graded key (numeric): 0.36 | correct | B26 |
| homework-3.json | items[5].widget.wrong[0] | slip uniform = 0.9 is the value of the named mistake and is not a correct answer | correct | B26 |
| homework-3.json | items[5].widget.wrong[1] | slip at-mean = 0 is the value of the named mistake and is not a correct answer | correct | B26 |
| homework-3.json | items[5].widget.wrong[2] | slip peak-density = 1.8 is the value of the named mistake and is not a correct answer | correct | B26 |
| homework-3.json | items[5].widget.accept | £0.36: $\tfrac{1}{100}\int_0^6 y(6 - y)\,dy = \tfrac{36}{100}$, with $y = x - 104$. | correct | B26 |
| homework-3.json | items[5].feedback.correct | $\tfrac{1}{100}(108 - 72) = \text{£}0.36$. | correct | B26 |
| homework-3.json | items[5].feedback.generic | Not quite right. Above £100 the density is $\tfrac{110 - x}{100}$; integrate the payoff times it from 104 t... | correct | B26 |
| homework-3.json | items[5].feedback.byKey.uniform | That uses the uniform density $\tfrac{1}{20}$. The triangle is thinner out at £110. | correct | B26 |
| homework-3.json | items[5].feedback.byKey.at-mean | That is the payoff at the expected price, £100. Average the payoff over the density instead. | correct | B26 |
| homework-3.json | items[5].feedback.byKey.peak-density | You used the peak density $\tfrac{1}{10}$ everywhere. Near £110 it falls to 0. | correct | B26 |
| homework-3.json | items[5].explain.text | With $y = x - 104$ the density is $\tfrac{6 - y}{100}$ and the payoff is $y$. So $E = \tfrac{1}{100}\int_0^... | correct | B26 |
| homework-3.json | items[6].prose | Consider $\displaystyle\int_1^\infty \frac{\ln x}{x}\,dx$. The integrand tends to 0 as $x \to \infty$. | correct | B26 |
| homework-3.json | items[6].question | What does the integral do? | correct | B26 |
| homework-3.json | items[6].widget.options[0].text | wrong option, wrong under every convention: It converges, because $\frac{\ln x}{x} \to 0$ | correct | B26 |
| homework-3.json | items[6].widget.options[0].why | Falling to 0 is not enough. With $u = \ln x$ the area to $b$ is $\tfrac{1}{2}(\ln b)^2$, which grows withou... | correct | B26 |
| homework-3.json | items[6].widget.options[1].text | wrong option, wrong under every convention: It converges to $\tfrac{1}{2}$ | correct | B26 |
| homework-3.json | items[6].widget.options[1].why | That evaluates $\tfrac{1}{2}(\ln x)^2$ as if $\ln b$ stayed at 1. It grows without limit. | correct | B26 |
| homework-3.json | items[6].widget.options[2] | graded key (choice): It diverges: $\int_1^b \frac{\ln x}{x}\,dx = \tfrac{1}{2}(\ln b)^2$ grows without limit | correct | B26 |
| homework-3.json | items[6].feedback.correct | $\tfrac{1}{2}(\ln b)^2 \to \infty$, so the integral diverges. | correct | B26 |
| homework-3.json | items[6].feedback.generic | Not quite right. Substitute $u = \ln x$ and look at the area up to $b$. | correct | B26 |
| homework-3.json | items[6].feedback.byKey.zero | You assumed a curve that falls to 0 has finite area. This one falls more slowly than $\tfrac{1}{x}$ even, a... | correct | B26 |
| homework-3.json | items[6].explain.text | With $u = \ln x$, $du = \tfrac{1}{x}\,dx$ and $u$ runs from 0 to $\ln b$. The area is $\tfrac{1}{2}(\ln b)^... | correct | B26 |
| homework-3.json | items[7].prompt | A perpetuity pays £1 a year continuously, discounted at a continuous rate $r > 0$. Its price is $P = \int_0... | correct | B26 |
| homework-3.json | items[7].model | **(a)** Take $u = t$ and $dv = e^{-rt}\,dt$, so $du = dt$ and $v = -\frac{1}{r}e^{-rt}$. Parts gives $$\beg... | correct | B7 |
| homework-3.json | items[7].rubric[0].text | Chooses $u = t$, $dv = e^{-rt}\,dt$ and finds $v = -\frac{1}{r}e^{-rt}$. | correct | B7 |
| homework-3.json | items[7].rubric[1].text | Reaches $\int_0^b t\,e^{-rt}\,dt = -\frac{b}{r}e^{-rb} + \frac{1 - e^{-rb}}{r^2}$. | correct | B7 |
| homework-3.json | items[7].rubric[2].text | Justifies $b\,e^{-rb} \to 0$ with a reason (a bound such as $e^{rb} > \frac{(rb)^2}{2}$), not just an asser... | correct | B7 |
| homework-3.json | items[7].rubric[3].text | Finds $P = \frac{1}{r}$ and $\int_0^\infty t\,e^{-rt}\,dt = \frac{1}{r^2}$. | correct | B7 |
| homework-3.json | items[7].rubric[4].text | Concludes $D = \frac{1}{r}$, which is 25 years at $r = 0.04$. | correct | B7 |
| homework-3.json | items[7].rubric[5].text | Shows $\frac{1}{P}\frac{dP}{dr} = -D$ and estimates a fall of about 2.5% (exactly 2.44%). | correct | B7 |
| homework-3.json | items[7].explain.text | Parts turns the weighted integral into $\frac{1}{r^2}$, and the price is $\frac{1}{r}$. Their ratio, the du... | correct | B26 |
| homework-3.json | items[8].prose | $\displaystyle\int_0^1 e^{-x^2}\,dx$ has no elementary formula. Estimate it with the trapezium rule and $n ... | correct | B26 |
| homework-3.json | items[8].question | What is $T_4$? Give 4 decimal places. | correct | B26 |
| homework-3.json | items[8].widget.answer | graded key (numeric): 0.743 | correct | B26 |
| homework-3.json | items[8].widget.wrong[0] | slip exact = 0.7468 is the value of the named mistake and is not a correct answer | correct | B26 |
| homework-3.json | items[8].widget.wrong[1] | slip no-halves = 0.914 is the value of the named mistake and is not a correct answer | correct | B26 |
| homework-3.json | items[8].widget.accept | About 0.7430: $0.25\left[\tfrac{1}{2} + e^{-0.0625} + e^{-0.25} + e^{-0.5625} + \tfrac{1}{2}e^{-1}\right]$. | correct | B26 |
| homework-3.json | items[8].feedback.correct | $T_4 \approx 0.7430$, against the true 0.7468. | correct | B26 |
| homework-3.json | items[8].feedback.generic | Not quite right. Evaluate $e^{-x^2}$ at 0, 0.25, 0.5, 0.75 and 1, halve the two ends, add, and multiply by ... | correct | B26 |
| homework-3.json | items[8].feedback.byKey.exact | That is the true value, from a much finer computation. The question asks for $T_4$. | correct | B26 |
| homework-3.json | items[8].feedback.byKey.no-halves | You added all five heights in full. The two ends belong to one strip each, so halve them. | correct | B26 |
| homework-3.json | items[8].explain.text | The heights are 1, 0.9394, 0.7788, 0.5698 and 0.3679. With the ends halved they add to 2.9719, and times $h... | correct | B26 |
| homework-3.json | items[9].prompt | (a) Let $u$ and $v$ have continuous derivatives on $[a, b]$. Starting from the product rule, derive $$\int_... | correct | B26 |
| homework-3.json | items[9].model | **(a)** $u$ and $v$ are differentiable on $[a, b]$, so the product rule gives, at every point of $[a, b]$, ... | correct | B7 |
| homework-3.json | items[9].rubric[0].text | (a) Tick only if all are given. The product rule $(uv)' = u'v + uv'$. Integrating over $[a, b]$ with $\int_... | correct | B7 |
| homework-3.json | items[9].rubric[1].text | (b) Says why the split or the substitution helps: differentiating $\ln x$ removes the logarithm, or $x = e^... | correct | B7 |
| homework-3.json | items[9].rubric[2].text | (b) Reaches $\int_1^b \frac{\ln x}{x^3}\,dx = \frac14 - \frac{1}{4b^2} - \frac{\ln b}{2b^2}$ on a finite ra... | correct | B7 |
| homework-3.json | items[9].rubric[3].text | (b) Justifies $\frac{\ln b}{b^2} \to 0$, or $B\,e^{-2B} \to 0$, with a reason, not just an assertion. A bou... | correct | B7 |
| homework-3.json | items[9].rubric[4].text | (b) Concludes that the integral converges, with value $\frac14$. | correct | B7 |
| problems-3.json | items[0].prose | A desk models the size $X$ of a large order, in thousands of shares, by the density $f(x) = \dfrac{2x}{(1 +... | correct | B27 |
| problems-3.json | items[0].parts[0].question | Use $u = 1 + x^2$ to find $\displaystyle\int \frac{2x}{(1 + x^2)^2}\,dx$. Leave out the $+C$. | correct | B27 |
| problems-3.json | items[0].parts[0].widget.answer | graded key (expression): "-\\frac{1}{1+x^2}" | correct | B27 |
| problems-3.json | items[0].parts[0].widget.wrong[0] | slip sign = "\\frac{1}{1+x^2}" is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[0].parts[0].widget.wrong[1] | slip log = "\\ln(1+x^2)" is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[0].parts[0].widget.wrong[2] | slip power-down = "-\\frac{1}{3(1+x^2)^3}" is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[0].parts[0].feedback.correct | With $u = 1 + x^2$, $du = 2x\,dx$, so the integral is $\int u^{-2}\,du = -u^{-1}$. Back in $x$, that is $-\... | correct | B27 |
| problems-3.json | items[0].parts[0].feedback.generic | Not quite. Turn $2x\,dx$ into $du$, integrate the power of $u$, then put $u = 1 + x^2$ back. | correct | B27 |
| problems-3.json | items[0].parts[0].feedback.byKey.sign | Raising $u^{-2}$ to $u^{-1}$ divides by $-1$, so the result is negative. | correct | B27 |
| problems-3.json | items[0].parts[0].feedback.byKey.log | That integrates $\tfrac{2x}{1 + x^2}$. Here the bottom is squared, so it is $u^{-2}$, not $u^{-1}$. | correct | B27 |
| problems-3.json | items[0].parts[0].feedback.byKey.power-down | You lowered the power. The power rule raises $-2$ to $-1$ and divides by $-1$. | correct | B27 |
| problems-3.json | items[0].parts[0].explain.text | $du = 2x\,dx$ turns the integral into $\int u^{-2}\,du = -u^{-1} + C$. Putting $u = 1 + x^2$ back gives $-\... | correct | B27 |
| problems-3.json | items[0].parts[1].question | Using that antiderivative, what is the chance an order is larger than 2, $P(X > 2) = \int_2^\infty f(x)\,dx... | correct | B27 |
| problems-3.json | items[0].parts[1].widget.answer | graded key (numeric): 0.2 | correct | B27 |
| problems-3.json | items[0].parts[1].widget.wrong[0] | slip below = 0.8 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[0].parts[1].widget.wrong[1] | slip x-limits = 0.5 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[0].parts[1].widget.accept | Any form equal to $\tfrac{1}{5}$, or $0.2 \pm 0.0005$ | correct | B27 |
| problems-3.json | items[0].parts[1].feedback.correct | $\int_2^b f\,dx = \tfrac{1}{5} - \tfrac{1}{1 + b^2}$, and the last term tends to 0 as $b \to \infty$. So $P... | correct | B27 |
| problems-3.json | items[0].parts[1].feedback.generic | Not quite. Integrate from 2 to $b$, then let $b$ grow without limit. | correct | B27 |
| problems-3.json | items[0].parts[1].feedback.byKey.below | That is $P(X \le 2) = \int_0^2 f\,dx$. The tail runs from 2 up to infinity. | correct | B27 |
| problems-3.json | items[0].parts[1].feedback.byKey.x-limits | You switched to $u$ but kept the $x$ limit 2. At $x = 2$, $u = 5$, so the tail is $\int_5^\infty u^{-2}\,du... | correct | B27 |
| problems-3.json | items[0].parts[1].explain.text | Integrate to $b$ first: $\big[-\tfrac{1}{1 + x^2}\big]_2^b = \tfrac{1}{5} - \tfrac{1}{1 + b^2}$. As $b \to ... | correct | B27 |
| problems-3.json | items[0].parts[2].question | Part 2's working gives $P(X > m) = \dfrac{1}{1 + m^2}$ for $m \ge 0$. What is the median order size, the $m... | correct | B27 |
| problems-3.json | items[0].parts[2].widget.answer | graded key (numeric): 1 | correct | B27 |
| problems-3.json | items[0].parts[2].widget.wrong[0] | slip drop-one = 1.4142 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[0].parts[2].feedback.correct | $\tfrac{1}{1 + m^2} = \tfrac{1}{2}$ gives $1 + m^2 = 2$, so $m = 1$: half of large orders are over 1,000 sh... | correct | B27 |
| problems-3.json | items[0].parts[2].feedback.generic | Not quite. Set the tail equal to $\tfrac{1}{2}$ and solve for $m$. | correct | B27 |
| problems-3.json | items[0].parts[2].feedback.byKey.drop-one | You solved $\tfrac{1}{m^2} = \tfrac{1}{2}$. The tail is $\tfrac{1}{1 + m^2}$, so $1 + m^2 = 2$. | correct | B27 |
| problems-3.json | items[0].parts[2].explain.text | Set the tail to $\tfrac{1}{2}$: $1 + m^2 = 2$, and $m = 1$ since sizes are positive. So the median order is... | correct | B27 |
| problems-3.json | items[0].parts[3].question | The desk wants the order size that is exceeded only 1% of the time. Using $P(X > q) = \dfrac{1}{1 + q^2}$, ... | correct | B27 |
| problems-3.json | items[0].parts[3].widget.answer | graded key (numeric): 9.9498743710662 | correct | B27 |
| problems-3.json | items[0].parts[3].widget.wrong[0] | slip drop-one = 10 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[0].parts[3].widget.wrong[1] | slip no-root = 99 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[0].parts[3].widget.wrong[2] | slip wrong-tail = 0.1 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[0].parts[3].widget.accept | $\sqrt{99} \approx 9.95$, accepted as $9.95 \pm 0.005$ | correct | B27 |
| problems-3.json | items[0].parts[3].feedback.correct | $\tfrac{1}{1 + q^2} = 0.01$ gives $1 + q^2 = 100$, so $q = \sqrt{99} \approx 9.95$, about 9,950 shares. | correct | B27 |
| problems-3.json | items[0].parts[3].feedback.generic | Not quite. Set the tail equal to 0.01 and solve for $q$. | correct | B27 |
| problems-3.json | items[0].parts[3].feedback.byKey.drop-one | You solved $q^2 = 100$. The tail is $\tfrac{1}{1 + q^2}$, so $q^2 = 99$. | correct | B27 |
| problems-3.json | items[0].parts[3].feedback.byKey.no-root | 99 is $q^2$. Take the square root. | correct | B27 |
| problems-3.json | items[0].parts[3].feedback.byKey.wrong-tail | That size is exceeded 99% of the time. The desk wants a tail of 0.01. | correct | B27 |
| problems-3.json | items[0].parts[3].explain.text | $1 + q^2 = 100$ gives $q = \sqrt{99} \approx 9.95$. The tail falls only like $\tfrac{1}{q^2}$, so the 1% si... | correct | B27 |
| problems-3.json | items[1].prose | A resting order's time to fill, $X$ minutes, has density $f(x) = x\,e^{-x}$ for $x \ge 0$. You may use that... | correct | B27 |
| problems-3.json | items[1].parts[0].question | Use parts with $u = x$ to find $\int x\,e^{-x}\,dx$. Leave out the $+C$. | correct | B27 |
| problems-3.json | items[1].parts[0].widget.answer | graded key (expression): "-(x+1)e^{-x}" | correct | B27 |
| problems-3.json | items[1].parts[0].widget.wrong[0] | slip minus-sign = "-(x-1)e^{-x}" is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[1].parts[0].widget.wrong[1] | slip uv-only = "-xe^{-x}" is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[1].parts[0].widget.wrong[2] | slip v-sign = "(x+1)e^{-x}" is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[1].parts[0].feedback.correct | Take $u = x$ and $dv = e^{-x}\,dx$, so $v = -e^{-x}$. Then $\int x\,e^{-x}\,dx = -x\,e^{-x} + \int e^{-x}\,... | correct | B27 |
| problems-3.json | items[1].parts[0].feedback.generic | Not quite. Use $\int u\,dv = uv - \int v\,du$ with $u = x$ and $v = -e^{-x}$. | correct | B27 |
| problems-3.json | items[1].parts[0].feedback.byKey.minus-sign | You took $\int v\,du$ with the wrong sign. Since $v = -e^{-x}$, $-\int v\,du = \int e^{-x}\,dx = -e^{-x}$. | correct | B27 |
| problems-3.json | items[1].parts[0].feedback.byKey.uv-only | That is $uv$ alone. Parts also needs $-\int v\,du$. | correct | B27 |
| problems-3.json | items[1].parts[0].feedback.byKey.v-sign | You took $v = e^{-x}$. Its derivative is $-e^{-x}$, so $v = -e^{-x}$. | correct | B27 |
| problems-3.json | items[1].parts[0].explain.text | $\int u\,dv = uv - \int v\,du$ with $u = x$ and $v = -e^{-x}$ gives $-x e^{-x} - e^{-x}$. Differentiating $... | correct | B27 |
| problems-3.json | items[1].parts[1].question | Using $\int x\,e^{-x}\,dx = -(x + 1)e^{-x} + C$, what is the chance the order is still unfilled after 2 min... | correct | B27 |
| problems-3.json | items[1].parts[1].widget.answer | graded key (numeric): 0.4060058497098381 | correct | B27 |
| problems-3.json | items[1].parts[1].widget.wrong[0] | slip dropped-x = 0.135 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[1].parts[1].widget.wrong[1] | slip dropped-one = 0.271 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[1].parts[1].widget.wrong[2] | slip complement = 0.594 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[1].parts[1].widget.accept | $3e^{-2} \approx 0.406$, accepted as $0.406 \pm 0.0005$ | correct | B27 |
| problems-3.json | items[1].parts[1].feedback.correct | $\int_2^b x e^{-x}\,dx = 3e^{-2} - (b + 1)e^{-b}$, and $(b + 1)e^{-b} \to 0$. So $P(X > 2) = 3e^{-2} \appro... | correct | B27 |
| problems-3.json | items[1].parts[1].feedback.generic | Not quite. Integrate from 2 to $b$, then let $b$ grow without limit. | correct | B27 |
| problems-3.json | items[1].parts[1].feedback.byKey.dropped-x | That is $e^{-2}$, the tail of $e^{-x}$ alone. At $x = 2$ the antiderivative is $-(2 + 1)e^{-2}$. | correct | B27 |
| problems-3.json | items[1].parts[1].feedback.byKey.dropped-one | You used $-x e^{-x}$ and lost the $-e^{-x}$ term. At 2 that gives $2e^{-2}$, not $3e^{-2}$. | correct | B27 |
| problems-3.json | items[1].parts[1].feedback.byKey.complement | That is $P(X \le 2)$, the chance it has filled. The question asks for the tail. | correct | B27 |
| problems-3.json | items[1].parts[1].explain.text | Integrate to $b$, then let $b \to \infty$: $\big[-(x + 1)e^{-x}\big]_2^b$ tends to $0 + 3e^{-2}$. That is a... | correct | B27 |
| problems-3.json | items[1].parts[2].question | The mean is $E[X] = \int_0^\infty x^2 e^{-x}\,dx$. Parts with $u = x^2$ turns it into $2\int_0^\infty x\,e^... | correct | B27 |
| problems-3.json | items[1].parts[2].widget.answer | graded key (numeric): 2 | correct | B27 |
| problems-3.json | items[1].parts[2].widget.wrong[0] | slip no-factor = 1 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[1].parts[2].feedback.correct | $\int_0^\infty x\,e^{-x}\,dx = \big[-(x + 1)e^{-x}\big]_0^\infty = 0 - (-1) = 1$. So $E[X] = 2 \times 1 = 2... | correct | B27 |
| problems-3.json | items[1].parts[2].feedback.generic | Not quite. Evaluate $\int_0^\infty x e^{-x}\,dx$ with part 1, then double it. | correct | B27 |
| problems-3.json | items[1].parts[2].feedback.byKey.no-factor | 1 is $\int_0^\infty x e^{-x}\,dx$, the total probability. The mean is twice that, since parts brings down t... | correct | B27 |
| problems-3.json | items[1].parts[2].explain.text | Parts with $u = x^2$ and $v = -e^{-x}$ gives a boundary term $\big[-x^2 e^{-x}\big]_0^\infty = 0$ plus $2\i... | correct | B27 |
| problems-3.json | items[1].parts[3].question | A quote loses value while it waits: it is worth $£100e^{-X}$ when it fills. Its expected value is $E[100e^{... | correct | B27 |
| problems-3.json | items[1].parts[3].widget.answer | graded key (numeric): 25 | correct | B27 |
| problems-3.json | items[1].parts[3].widget.wrong[0] | slip mean-wait = 13.53 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[1].parts[3].widget.wrong[1] | slip half = 50 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[1].parts[3].widget.wrong[2] | slip one = 100 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[1].parts[3].feedback.correct | Parts with $u = x$ and $v = -\tfrac{1}{2}e^{-2x}$ gives $\int_0^\infty x\,e^{-2x}\,dx = 0 + \tfrac{1}{2}\in... | correct | B27 |
| problems-3.json | items[1].parts[3].feedback.generic | Not quite. Use parts with $u = x$ on $\int_0^\infty x e^{-2x}\,dx$, then multiply by 100. | correct | B27 |
| problems-3.json | items[1].parts[3].feedback.byKey.mean-wait | That is the value at the mean wait, $100e^{-2}$. The expected value weights every wait by its density. | correct | B27 |
| problems-3.json | items[1].parts[3].feedback.byKey.half | You found $\tfrac{1}{2}$ for the integral. $\int_0^\infty e^{-2x}\,dx$ is itself $\tfrac{1}{2}$, so the tot... | correct | B27 |
| problems-3.json | items[1].parts[3].feedback.byKey.one | That needs the integral to be 1. With $e^{-2x}$, each step of parts divides by 2. | correct | B27 |
| problems-3.json | items[1].parts[3].explain.text | $E[g(X)] = \int g(x) f(x)\,dx$ with $g(x) = 100e^{-x}$ and $f(x) = x e^{-x}$. The integrand is $100x e^{-2x... | correct | B27 |
| problems-3.json | items[1].parts[4].question | Using $E[X] = 2$ from part 3, a trader values the quote at the mean wait instead: $100e^{-2} \approx £13.53... | correct | B27 |
| problems-3.json | items[1].parts[4].widget.options[0] | graded key (choice): The value $100e^{-x}$ is curved: quick fills gain more than slow fills lose, so the me... | correct | B27 |
| problems-3.json | items[1].parts[4].widget.options[1].text | wrong option, wrong under every convention: The trader should plug in the median wait instead, and that sin... | correct | B27 |
| problems-3.json | items[1].parts[4].widget.options[1].why | You swapped the mean for another single wait. No one wait gives $E[g(X)]$ for a curved $g$; the whole densi... | imprecise | Finding 5: by the intermediate value theorem the wait ln 4 gives exactly £25; what fails is any fixed summary such as the median (£18.67) |
| problems-3.json | items[1].parts[4].widget.options[2].text | wrong option, wrong under every convention: Part 4 must be wrong, because the expected value of $100e^{-X}$... | correct | B27 |
| problems-3.json | items[1].parts[4].widget.options[2].why | You assumed $E[g(X)] = g(E[X])$. That holds for a straight-line $g$, not for $e^{-x}$. | correct | B27 |
| problems-3.json | items[1].parts[4].widget.options[3].text | wrong option, wrong under every convention: Some orders never fill, and the two figures would agree once ev... | correct | B27 |
| problems-3.json | items[1].parts[4].widget.options[3].why | Here the order fills with chance 1 already, since the density integrates to 1. The gap comes from the curve... | correct | B27 |
| problems-3.json | items[1].parts[4].feedback.correct | Correct. $e^{-x}$ is curved, so the average of the values is not the value at the average wait. | correct | B27 |
| problems-3.json | items[1].parts[4].feedback.generic | Not quite. Compare averaging $100e^{-x}$ over the waits with putting in one wait. | correct | B27 |
| problems-3.json | items[1].parts[4].explain.text | For a curved payoff, $E[g(X)]$ and $g(E[X])$ differ in general. Here $g(x) = 100e^{-x}$ bends upwards, so t... | correct | B27 |
| problems-3.json | items[2].prose | A one-year gross return $X$, next year's price over today's, is modelled as uniform on $[0.5, 1.5]$, with d... | correct | B27 |
| problems-3.json | items[2].parts[0].question | Estimate $\int_{0.5}^{1.5} \ln x\,dx$ with the trapezium rule and $n = 2$ strips. Give a decimal to 4 places. | correct | B27 |
| problems-3.json | items[2].parts[0].widget.answer | graded key (numeric): -0.07192051811294523 | correct | B27 |
| problems-3.json | items[2].parts[0].widget.wrong[0] | slip full-ends = -0.1438 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[2].parts[0].widget.wrong[1] | slip midpoint = -0.0323 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[2].parts[0].widget.wrong[2] | slip lost-strip = -0.1733 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[2].parts[0].widget.wrong[3] | slip sign = 0.0719 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[2].parts[0].widget.accept | $-0.0719$ ($-0.0720$ is accepted too) | correct | B27 |
| problems-3.json | items[2].parts[0].feedback.correct | With $h = 0.5$ the points are 0.5, 1 and 1.5. $T_2 = 0.5\big[\tfrac{1}{2}\ln 0.5 + \ln 1 + \tfrac{1}{2}\ln ... | correct | B27 |
| problems-3.json | items[2].parts[0].feedback.generic | Not quite. Use the points 0.5, 1 and 1.5, with half weight on the two ends. | correct | B27 |
| problems-3.json | items[2].parts[0].feedback.byKey.full-ends | You gave the two end points full weight, or left out $h$. Each end counts half, and $h = 0.5$ multiplies th... | correct | B27 |
| problems-3.json | items[2].parts[0].feedback.byKey.midpoint | That is the midpoint sum. The trapezium rule uses the strip edges 0.5, 1 and 1.5. | correct | B27 |
| problems-3.json | items[2].parts[0].feedback.byKey.lost-strip | You used only the first two points, which bound one strip. Two strips need three points. | correct | B27 |
| problems-3.json | items[2].parts[0].feedback.byKey.sign | ln 0.5 is −0.34657 and ln 1.5 is 0.20273, so the negative end outweighs. A positive 0.0719 takes 0.34657 − ... | wrong | Finding 1: ln 0.5 = -0.69315 and ln 1.5 = 0.40547; the printed -0.34657 and 0.20273 are their halves (script check fails) |
| problems-3.json | items[2].parts[0].explain.text | $T_2 = h\big[\tfrac{1}{2}f(x_0) + f(x_1) + \tfrac{1}{2}f(x_2)\big]$ with $h = 0.5$. That is $0.5 \times (-0... | correct | B27 |
| problems-3.json | items[2].parts[1].question | Now exactly, by parts with $u = \ln x$ and $dv = dx$. What is $E[\ln X] = \int_{0.5}^{1.5} \ln x\,dx$? Give... | correct | B27 |
| problems-3.json | items[2].parts[1].widget.answer | graded key (numeric): -0.045228747557780724 | correct | B27 |
| problems-3.json | items[2].parts[1].widget.wrong[0] | slip plus-x = 1.9548 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[2].parts[1].widget.wrong[1] | slip uv-only = 0.9548 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[2].parts[1].widget.wrong[2] | slip estimate = -0.0719 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[2].parts[1].widget.wrong[3] | slip sign = 0.045229 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[2].parts[1].widget.accept | $-0.0452 \pm 0.00005$ | correct | B27 |
| problems-3.json | items[2].parts[1].feedback.correct | $\int \ln x\,dx = x\ln x - x$, so the value is $(1.5\ln 1.5 - 1.5) - (0.5\ln 0.5 - 0.5) \approx -0.0452$. | correct | B27 |
| problems-3.json | items[2].parts[1].feedback.generic | Not quite. Parts gives $\int \ln x\,dx = x\ln x - \int 1\,dx$; evaluate between 0.5 and 1.5. | correct | B27 |
| problems-3.json | items[2].parts[1].feedback.byKey.plus-x | You added $\int v\,du$. Parts subtracts it: $x\ln x - \int x \cdot \tfrac{1}{x}\,dx = x\ln x - x$. | correct | B27 |
| problems-3.json | items[2].parts[1].feedback.byKey.uv-only | That is $\big[x\ln x\big]$ alone. Parts also takes off $\int 1\,dx = x$. | correct | B27 |
| problems-3.json | items[2].parts[1].feedback.byKey.estimate | That is the trapezium estimate from part 1. Parts gives the exact value. | correct | B27 |
| problems-3.json | items[2].parts[1].feedback.byKey.sign | x ln x − x is −0.8918 at 1.5 and −0.8466 at 0.5. The first minus the second is negative; a positive 0.0452 ... | correct | B27 |
| problems-3.json | items[2].parts[1].explain.text | With $u = \ln x$ and $dv = dx$, $\int \ln x\,dx = x\ln x - x$. Between 0.5 and 1.5 that is about $-0.0452$:... | correct | B27 |
| problems-3.json | items[2].parts[2].question | Part 1's estimate $-0.0719$ is out by about 0.0267 against part 2's $-0.0452$. The error shrinks like $h^2$... | correct | B27 |
| problems-3.json | items[2].parts[2].widget.answer | graded key (numeric): 0.00166875 | correct | B27 |
| problems-3.json | items[2].parts[2].widget.wrong[0] | slip linear = 0.0067 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[2].parts[2].widget.wrong[1] | slip eight-squared = 0.0004 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[2].parts[2].widget.accept | $0.0017 \pm 0.00005$ | correct | B27 |
| problems-3.json | items[2].parts[2].feedback.correct | From $n = 2$ to $n = 8$, $h$ is a quarter as big, so the error shrinks by $4^2 = 16$. $0.0267 / 16 \approx ... | correct | B27 |
| problems-3.json | items[2].parts[2].feedback.generic | Not quite. Find how many times smaller $h$ becomes, then square that factor. | correct | B27 |
| problems-3.json | items[2].parts[2].feedback.byKey.linear | You cut the error by 4, as if it shrank like $h$. It shrinks like $h^2$, so by $4^2 = 16$. | correct | B27 |
| problems-3.json | items[2].parts[2].feedback.byKey.eight-squared | You divided by $8^2$. Going from 2 to 8 strips makes $h$ four times smaller, so divide by $4^2$. | correct | B27 |
| problems-3.json | items[2].parts[2].explain.text | The error is about $Kh^2$, and $h$ goes from 0.5 to 0.125. So the error falls by a factor of 16, to about 0... | correct | B27 |
| problems-3.json | items[2].parts[3].question | Part 2 gave $E[\ln X] \approx -0.0452$, while $\ln E[X] = \ln 1 = 0$. What explains the gap? | correct | B27 |
| problems-3.json | items[2].parts[3].widget.options[0] | graded key (choice): The log of the mean return overstates the mean log return, because $\ln x$ bends downw... | correct | B27 |
| problems-3.json | items[2].parts[3].widget.options[1].text | wrong option, wrong under every convention: Part 2 must be wrong, since $E[\ln X]$ always equals $\ln E[X]$... | correct | B27 |
| problems-3.json | items[2].parts[3].widget.options[1].why | You assumed $E[g(X)] = g(E[X])$. That holds for a straight-line $g$, and $\ln x$ is curved. | correct | B27 |
| problems-3.json | items[2].parts[3].widget.options[2].text | wrong option, wrong under every convention: The trapezium rule caused the gap, so running more strips throu... | correct | B27 |
| problems-3.json | items[2].parts[3].widget.options[2].why | Part 2 is exact and uses no strips. The gap comes from the curve of $\ln x$, not from an estimate. | correct | B27 |
| problems-3.json | items[2].parts[3].widget.options[3].text | wrong option, wrong under every convention: The mean gross return is below 1, so the uniform model on $[0.5... | correct | B27 |
| problems-3.json | items[2].parts[3].widget.options[3].why | The mean is $E[X] = 1$, the midpoint of $[0.5, 1.5]$. Only the mean of $\ln X$ is below zero. | correct | B27 |
| problems-3.json | items[2].parts[3].feedback.correct | Correct. $\ln x$ bends downwards, so averaging after taking logs gives less than the log of the average. | correct | B27 |
| problems-3.json | items[2].parts[3].feedback.generic | Not quite. Compare averaging $\ln x$ over the returns with taking $\ln$ of the average return. | correct | B27 |
| problems-3.json | items[2].parts[3].explain.text | For a curved $g$, $E[g(X)]$ and $g(E[X])$ differ in general. Since $\ln x$ bends downwards, $E[\ln X] \appr... | correct | B27 |
| problems-3.json | items[3].prose | A trading signal's strength $t$ hours after an event is $s(t) = t\,e^{-t^2/8}$. The desk wants its average ... | correct | B27 |
| problems-3.json | items[3].parts[0].question | Use $u = \tfrac{t^2}{8}$ to find $\int t\,e^{-t^2/8}\,dt$. Leave out the $+C$. | correct | B27 |
| problems-3.json | items[3].parts[0].widget.answer | graded key (expression): "-4e^{-t^2/8}" | correct | B27 |
| problems-3.json | items[3].parts[0].widget.wrong[0] | slip quarter = "-\\frac{1}{4}e^{-t^2/8}" is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[3].parts[0].widget.wrong[1] | slip sign = "4e^{-t^2/8}" is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[3].parts[0].widget.wrong[2] | slip no-fix = "-e^{-t^2/8}" is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[3].parts[0].feedback.correct | $du = \tfrac{t}{4}\,dt$, so $t\,dt = 4\,du$ and the integral is $4\int e^{-u}\,du = -4e^{-u}$. Back in $t$,... | correct | B27 |
| problems-3.json | items[3].parts[0].feedback.generic | Not quite. Write $t\,dt$ in terms of $du$, then integrate $e^{-u}$. | correct | B27 |
| problems-3.json | items[3].parts[0].feedback.byKey.quarter | You multiplied by $\tfrac{1}{4}$. Since $du = \tfrac{t}{4}\,dt$, $t\,dt$ is $4\,du$. | correct | B27 |
| problems-3.json | items[3].parts[0].feedback.byKey.sign | $\int e^{-u}\,du = -e^{-u}$, so the result is negative. | correct | B27 |
| problems-3.json | items[3].parts[0].feedback.byKey.no-fix | You did not fix the constant. $t\,dt$ is $4\,du$, not $du$. | correct | B27 |
| problems-3.json | items[3].parts[0].explain.text | With $u = \tfrac{t^2}{8}$, $t\,dt = 4\,du$, so $\int t e^{-t^2/8}\,dt = -4e^{-t^2/8} + C$. Differentiating ... | correct | B27 |
| problems-3.json | items[3].parts[1].question | Using $-4e^{-t^2/8}$, what is $\int_0^4 s(t)\,dt$? Give a decimal to 3 places. | correct | B27 |
| problems-3.json | items[3].parts[1].widget.answer | graded key (numeric): 3.458658867053549 | correct | B27 |
| problems-3.json | items[3].parts[1].widget.wrong[0] | slip x-limits = 3.927 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[3].parts[1].widget.wrong[1] | slip quarter = 0.216 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[3].parts[1].widget.wrong[2] | slip sign = -3.459 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[3].parts[1].widget.accept | $4(1 - e^{-2}) \approx 3.459$, accepted as $3.459 \pm 0.0005$ | correct | B27 |
| problems-3.json | items[3].parts[1].feedback.correct | $\big[-4e^{-t^2/8}\big]_0^4 = -4e^{-2} + 4 = 4(1 - e^{-2}) \approx 3.459$. | correct | B27 |
| problems-3.json | items[3].parts[1].feedback.generic | Not quite. Evaluate the antiderivative at 4 and at 0, top limit first. | correct | B27 |
| problems-3.json | items[3].parts[1].feedback.byKey.x-limits | You switched to $u$ but kept the limits 0 and 4. At $t = 4$, $u = \tfrac{16}{8} = 2$. | correct | B27 |
| problems-3.json | items[3].parts[1].feedback.byKey.quarter | That comes from $-\tfrac{1}{4}e^{-t^2/8}$ in part 1. With $-4e^{-t^2/8}$ the value is $4(1 - e^{-2})$. | correct | B27 |
| problems-3.json | items[3].parts[1].feedback.byKey.sign | You subtracted the wrong way round. Top limit first: $F(4) - F(0)$. | correct | B27 |
| problems-3.json | items[3].parts[1].explain.text | In $u$ the limits are 0 and 2, so the integral is $4\int_0^2 e^{-u}\,du = 4(1 - e^{-2})$. That is about 3.459. | correct | B27 |
| problems-3.json | items[3].parts[2].question | Using $\int_0^4 s(t)\,dt \approx 3.459$, what is the average strength over the 4 hours? Give a decimal to 3... | correct | B27 |
| problems-3.json | items[3].parts[2].widget.answer | graded key (numeric): 0.8646647167633873 | correct | B27 |
| problems-3.json | items[3].parts[2].widget.wrong[0] | slip no-divide = 3.459 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[3].parts[2].widget.wrong[1] | slip halved = 1.729 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[3].parts[2].widget.wrong[2] | slip x-limits = 0.982 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[3].parts[2].widget.accept | $1 - e^{-2} \approx 0.865$, accepted as $0.865 \pm 0.0005$ | correct | B27 |
| problems-3.json | items[3].parts[2].feedback.correct | Divide by the length of the interval: $\tfrac{1}{4} \times 4(1 - e^{-2}) = 1 - e^{-2} \approx 0.865$. | correct | B27 |
| problems-3.json | items[3].parts[2].feedback.generic | Not quite. An average value divides the area by the length of the interval. | correct | B27 |
| problems-3.json | items[3].parts[2].feedback.byKey.no-divide | That is the area. The average divides it by the 4 hours. | correct | B27 |
| problems-3.json | items[3].parts[2].feedback.byKey.halved | You divided by 2. The interval runs from 0 to 4, so divide by 4. | correct | B27 |
| problems-3.json | items[3].parts[2].feedback.byKey.x-limits | That carries part 2's slip of keeping the $t$ limits. The area is $4(1 - e^{-2})$. | correct | B27 |
| problems-3.json | items[3].parts[2].explain.text | $\bar{s} = \tfrac{1}{4}\int_0^4 s(t)\,dt = 1 - e^{-2} \approx 0.865$. A flat signal at 0.865 for 4 hours ha... | correct | B27 |
| problems-3.json | items[3].parts[3].question | A script estimates $\int_0^4 s(t)\,dt$ with the trapezium rule and $n = 2$ strips. What does it return? Giv... | correct | B27 |
| problems-3.json | items[3].parts[3].widget.answer | graded key (numeric): 2.9674637717969845 | correct | B27 |
| problems-3.json | items[3].parts[3].widget.wrong[0] | slip full-ends = 3.509 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[3].parts[3].widget.wrong[1] | slip no-h = 1.484 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[3].parts[3].widget.wrong[2] | slip midpoint = 3.713 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[3].parts[3].widget.accept | $2.967$ (2.968 is accepted too) | correct | B27 |
| problems-3.json | items[3].parts[3].feedback.correct | With $h = 2$ the points are 0, 2 and 4. $T_2 = 2\big[\tfrac{1}{2}(0) + 2e^{-0.5} + \tfrac{1}{2}(4e^{-2})\bi... | correct | B27 |
| problems-3.json | items[3].parts[3].feedback.generic | Not quite. Use the points 0, 2 and 4, with half weight on the ends, times $h = 2$. | correct | B27 |
| problems-3.json | items[3].parts[3].feedback.byKey.full-ends | You gave the end points full weight. Each end of the rule counts half. | correct | B27 |
| problems-3.json | items[3].parts[3].feedback.byKey.no-h | You left out the width $h = 2$ that multiplies the bracket. | correct | B27 |
| problems-3.json | items[3].parts[3].feedback.byKey.midpoint | That is the midpoint sum at $t = 1$ and 3. The trapezium rule uses the edges 0, 2 and 4. | correct | B27 |
| problems-3.json | items[3].parts[3].explain.text | $s(0) = 0$, $s(2) = 2e^{-0.5} \approx 1.2131$ and $s(4) = 4e^{-2} \approx 0.5413$. Then $T_2 = 2(1.21306 + ... | correct | B27 |
| problems-3.json | items[3].parts[4].question | Part 2's exact 3.459 and part 4's 2.967 put the error of $T_2$ at about 0.49. The error shrinks like $h^2$.... | correct | B27 |
| problems-3.json | items[3].parts[4].widget.answer | graded key (numeric): 16 | correct | B27 |
| problems-3.json | items[3].parts[4].widget.wrong[0] | slip linear = 128 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[3].parts[4].widget.wrong[1] | slip one-short = 8 is the value of the named mistake and is not a correct answer | correct | B27 |
| problems-3.json | items[3].parts[4].feedback.correct | Each doubling divides the error by 4: about 0.12 at $n = 4$, 0.031 at $n = 8$ and 0.0077 at $n = 16$. So $n... | correct | B27 |
| problems-3.json | items[3].parts[4].feedback.generic | Not quite. Divide the error by 4 for each doubling of $n$ until it is below 0.01. | correct | B27 |
| problems-3.json | items[3].parts[4].feedback.byKey.linear | You halved the error with each doubling, as if it shrank like $h$. It shrinks like $h^2$, so by 4 each time. | correct | B27 |
| problems-3.json | items[3].parts[4].feedback.byKey.one-short | At $n = 8$ the predicted error is about 0.031, still above 0.01. One more doubling is needed. | correct | B27 |
| problems-3.json | items[3].parts[4].explain.text | With the error about $Kh^2$, doubling $n$ cuts it by 4. From 0.49 that gives 0.12, 0.031, then 0.0077 at $n... | correct | B27 |
| fluency-l9-undo-chain.json | families[0].prompt | Find $\int {k:c}{v}({v}^2{b:+})^{{{n}}}\,d{v}$. | correct | B16 |
| fluency-l9-undo-chain.json | families[0].widget.answer | graded key template: {r:cfrac}({v}^2{b:+})^{{{n1}}} with let {"n1": "n + 1", "r": "k/(2*(n + 1))"} | correct | B16 |
| fluency-l9-undo-chain.json | families[0].wrong[0] | slip half-missed = {2*r:cfrac}({v}^2{b:+})^{{{n1}}} is the value of the named mistake and differs from the ... | correct | B16 |
| fluency-l9-undo-chain.json | families[0].wrong[0].line | With $u = {v}^2{b:+}$, $du = 2{v}\,d{v}$, so ${k:c}{v}\,d{v}$ is ${k/2:cfrac}\,du$: you lost the 2. | correct | B16 |
| fluency-l9-undo-chain.json | families[0].wrong[1] | slip no-divide = {k/2:cfrac}({v}^2{b:+})^{{{n1}}} is the value of the named mistake and differs from the ke... | correct | B16 |
| fluency-l9-undo-chain.json | families[0].wrong[1].line | You raised the power to {n1} but did not divide by {n1}. | correct | B16 |
| fluency-l9-undo-chain.json | families[0].solution[0] | Let $u = {v}^2{b:+}$, so $du = 2{v}\,d{v}$ and ${k:c}{v}\,d{v} = {k/2:cfrac}\,du$. | correct | B16 |
| fluency-l9-undo-chain.json | families[0].solution[1] | $\int {k/2:cfrac}u^{{{n}}}\,du = {r:cfrac}u^{{{n1}}} + C$. | correct | B16 |
| fluency-l9-undo-chain.json | families[0].solution[2] | Put $u$ back: ${r:cfrac}({v}^2{b:+})^{{{n1}}} + C$. | correct | B16 |
| fluency-l9-undo-chain.json | families[1].prompt | Find $\int {k:c}{v}e^{{{a:c}{v}^2}}\,d{v}$. | correct | B16 |
| fluency-l9-undo-chain.json | families[1].widget.answer | graded key template: {r:cfrac}e^{{{a:c}{v}^2}} with let {"r": "k/(2*a)"} | correct | B16 |
| fluency-l9-undo-chain.json | families[1].wrong[0] | slip half-missed = {2*r:cfrac}e^{{{a:c}{v}^2}} is the value of the named mistake and differs from the key f... | correct | B16 |
| fluency-l9-undo-chain.json | families[1].wrong[0].line | With $u = {a:c}{v}^2$, $du = {2*a}{v}\,d{v}$: you divided by {a} but not by 2. | correct | B16 |
| fluency-l9-undo-chain.json | families[1].wrong[1] | slip multiplied = {2*a*k}e^{{{a:c}{v}^2}} is the value of the named mistake and differs from the key for ev... | correct | B16 |
| fluency-l9-undo-chain.json | families[1].wrong[1].line | You multiplied by ${2*a}$ instead of dividing by it. | correct | B16 |
| fluency-l9-undo-chain.json | families[1].solution[0] | Let $u = {a:c}{v}^2$, so $du = {2*a}{v}\,d{v}$ and ${k:c}{v}\,d{v} = {r:cfrac}\,du$. | correct | B16 |
| fluency-l9-undo-chain.json | families[1].solution[1] | $\int {r:cfrac}e^u\,du = {r:cfrac}e^u + C = {r:cfrac}e^{{{a:c}{v}^2}} + C$. | correct | B16 |
| fluency-l9-undo-chain.json | families[2].prompt | Find $\displaystyle\int \frac{{{k:c}{v}}}{{{v}^2+{b}}}\,d{v}$. | correct | B16 |
| fluency-l9-undo-chain.json | families[2].widget.answer | graded key template: {r:cfrac}\ln({v}^2+{b}) with let {"r": "k/2"} | correct | B16 |
| fluency-l9-undo-chain.json | families[2].wrong[0] | slip half-missed = {k:c}\ln({v}^2+{b}) is the value of the named mistake and differs from the key for every... | correct | B16 |
| fluency-l9-undo-chain.json | families[2].wrong[0].line | With $u = {v}^2+{b}$, $du = 2{v}\,d{v}$: you lost the 2. | correct | B16 |
| fluency-l9-undo-chain.json | families[2].wrong[1] | slip multiplied = {2*k}\ln({v}^2+{b}) is the value of the named mistake and differs from the key for every ... | correct | B16 |
| fluency-l9-undo-chain.json | families[2].wrong[1].line | You multiplied by 2. Since $du = 2{v}\,d{v}$, divide by 2: ${k:c}{v}\,d{v} = {r:cfrac}\,du$. | correct | B16 |
| fluency-l9-undo-chain.json | families[2].solution[0] | Let $u = {v}^2+{b}$, so $du = 2{v}\,d{v}$ and ${k:c}{v}\,d{v} = {r:cfrac}\,du$. | correct | B16 |
| fluency-l9-undo-chain.json | families[2].solution[1] | ${r:cfrac}\int \frac{{1}}{{u}}\,du = {r:cfrac}\ln u + C$, and $u > 0$, so the answer is ${r:cfrac}\ln({v}^2... | correct | B16 |
| fluency-l9-undo-chain.json | families[3].prompt | Evaluate $\int_{{{p}}}^{{{q}}} {k}x(x^2{b:+}){pw}\,dx$. Give a fraction or a decimal. | correct | B16 |
| fluency-l9-undo-chain.json | families[3].widget.answer | graded key template: {ans} with let {"k": "2*m", "n1": "n + 1", "lo": "p^2 + b", "hi": "q^2 + b", "ans": "m... | correct | B16 |
| fluency-l9-undo-chain.json | families[3].wrong[0] | slip limits-kept = {kept} is the value of the named mistake and differs from the key for every draw allowed... | correct | B16 |
| fluency-l9-undo-chain.json | families[3].wrong[0].line | You kept the $x$ limits {p} and {q}. In $u$ they become {lo} and {hi}. | correct | B16 |
| fluency-l9-undo-chain.json | families[3].solution[0] | Let $u = x^2{b:+}$, so $du = 2x\,dx$. The limits become $u = {lo}$ and $u = {hi}$. | correct | B16 |
| fluency-l9-undo-chain.json | families[3].solution[1] | The integral is ${m:c}\int_{{{lo}}}^{{{hi}}} {mono(u; 1, n)}\,du = {m:c}\left[\frac{{u^{{{n1}}}}}{{{n1}}}\r... | correct | B16 |
| fluency-l10-undo-product.json | families[0].prompt | Find $\int {a:c}{v}e^{{{k:c}{v}}}\,d{v}$. | correct | B16 |
| fluency-l10-undo-product.json | families[0].widget.answer | graded key template: {r:cfrac}{v}e^{{{k:c}{v}}}{-s:+cfrac}e^{{{k:c}{v}}} with let {"r": "a/k", "s": "a/(k*k)"} | correct | B16 |
| fluency-l10-undo-product.json | families[0].wrong[0] | slip sign-slip = {r:cfrac}{v}e^{{{k:c}{v}}}{s:+cfrac}e^{{{k:c}{v}}} is the value of the named mistake and d... | correct | B16 |
| fluency-l10-undo-product.json | families[0].wrong[0].line | Parts is $uv - \int v\,du$: subtract the second term, do not add it. | correct | B16 |
| fluency-l10-undo-product.json | families[0].wrong[1] | slip missing-term = {r:cfrac}{v}e^{{{k:c}{v}}} is the value of the named mistake and differs from the key f... | correct | B16 |
| fluency-l10-undo-product.json | families[0].wrong[1].line | You stopped at $uv$. Subtract $\int v\,du$ as well. | correct | B16 |
| fluency-l10-undo-product.json | families[0].solution[0] | Take $u = {a:c}{v}$, which differentiating makes a constant, and $dv = e^{{{k:c}{v}}}\,d{v}$. | correct | B16 |
| fluency-l10-undo-product.json | families[0].solution[1] | $uv = {r:cfrac}{v}e^{{{k:c}{v}}}$ and $\int v\,du = {s:cfrac}e^{{{k:c}{v}}}$. | correct | B16 |
| fluency-l10-undo-product.json | families[0].solution[2] | So the answer is $uv - \int v\,du = {r:cfrac}{v}e^{{{k:c}{v}}}{-s:+cfrac}e^{{{k:c}{v}}} + C$. | correct | B16 |
| fluency-l10-undo-product.json | families[1].prompt | Find $\int {a:c}{v}\cos({k:c}{v})\,d{v}$. | correct | B16 |
| fluency-l10-undo-product.json | families[1].widget.answer | graded key template: {r:cfrac}{v}\sin({k:c}{v}){s:+cfrac}\cos({k:c}{v}) with let {"r": "a/k", "s": "a/(k*k)"} | correct | B16 |
| fluency-l10-undo-product.json | families[1].wrong[0] | slip sign-slip = {r:cfrac}{v}\sin({k:c}{v}){-s:+cfrac}\cos({k:c}{v}) is the value of the named mistake and ... | correct | B16 |
| fluency-l10-undo-product.json | families[1].wrong[0].line | $\int v\,du$ holds a sine, and the integral of a sine is minus a cosine: the two minus signs make a plus. | correct | B16 |
| fluency-l10-undo-product.json | families[1].wrong[1] | slip missing-term = {r:cfrac}{v}\sin({k:c}{v}) is the value of the named mistake and differs from the key f... | correct | B16 |
| fluency-l10-undo-product.json | families[1].wrong[1].line | You stopped at $uv$. Subtract $\int v\,du$ as well. | correct | B16 |
| fluency-l10-undo-product.json | families[1].solution[0] | Take $u = {a:c}{v}$ and $dv = \cos({k:c}{v})\,d{v}$. | correct | B16 |
| fluency-l10-undo-product.json | families[1].solution[1] | $uv = {r:cfrac}{v}\sin({k:c}{v})$ and $\int v\,du = {-s:cfrac}\cos({k:c}{v})$. | correct | B16 |
| fluency-l10-undo-product.json | families[1].solution[2] | So the answer is $uv - \int v\,du = {r:cfrac}{v}\sin({k:c}{v}){s:+cfrac}\cos({k:c}{v}) + C$. | correct | B16 |
| fluency-l10-undo-product.json | families[2].prompt | Find $\int {a:c}{v}\sin({k:c}{v})\,d{v}$. | correct | B16 |
| fluency-l10-undo-product.json | families[2].widget.answer | graded key template: {-r:cfrac}{v}\cos({k:c}{v}){s:+cfrac}\sin({k:c}{v}) with let {"r": "a/k", "s": "a/(k*k)"} | correct | B16 |
| fluency-l10-undo-product.json | families[2].wrong[0] | slip sign-slip = {r:cfrac}{v}\cos({k:c}{v}){s:+cfrac}\sin({k:c}{v}) is the value of the named mistake and d... | correct | B16 |
| fluency-l10-undo-product.json | families[2].wrong[0].line | The integral of a sine is minus a cosine, so $uv$ carries a minus sign. | correct | B16 |
| fluency-l10-undo-product.json | families[2].wrong[1] | slip missing-term = {-r:cfrac}{v}\cos({k:c}{v}) is the value of the named mistake and differs from the key ... | correct | B16 |
| fluency-l10-undo-product.json | families[2].wrong[1].line | You stopped at $uv$. Subtract $\int v\,du$ as well. | correct | B16 |
| fluency-l10-undo-product.json | families[2].solution[0] | Take $u = {a:c}{v}$ and $dv = \sin({k:c}{v})\,d{v}$. | correct | B16 |
| fluency-l10-undo-product.json | families[2].solution[1] | $uv = {-r:cfrac}{v}\cos({k:c}{v})$ and $\int v\,du = {-s:cfrac}\sin({k:c}{v})$. | correct | B16 |
| fluency-l10-undo-product.json | families[2].solution[2] | So the answer is $uv - \int v\,du = {-r:cfrac}{v}\cos({k:c}{v}){s:+cfrac}\sin({k:c}{v}) + C$. | correct | B16 |
| fluency-l10-undo-product.json | families[3].prompt | Find $\int {mono(v; a, n)}\ln {v}\,d{v}$ for ${v} > 0$. | correct | B16 |
| fluency-l10-undo-product.json | families[3].widget.answer | graded key template: {mono(v; r, n1)}\ln({v}){-s:+cfrac}{v}^{{{n1}}} with let {"n1": "n + 1", "r": "a/(n + ... | correct | B16 |
| fluency-l10-undo-product.json | families[3].wrong[0] | slip sign-slip = {mono(v; r, n1)}\ln({v}){s:+cfrac}{v}^{{{n1}}} is the value of the named mistake and diffe... | correct | B16 |
| fluency-l10-undo-product.json | families[3].wrong[0].line | Parts is $uv - \int v\,du$: subtract the second term, do not add it. | correct | B16 |
| fluency-l10-undo-product.json | families[3].wrong[1] | slip second-divide = {mono(v; r, n1)}\ln({v}){-r:+cfrac}{v}^{{{n1}}} is the value of the named mistake and ... | correct | B16 |
| fluency-l10-undo-product.json | families[3].wrong[1].line | $\int v\,du = \int {mono(v; r, n)}\,d{v}$: raise the power to {n1} and divide by {n1} again. | correct | B16 |
| fluency-l10-undo-product.json | families[3].solution[0] | Take $u = \ln {v}$, which differentiating makes simpler, and $dv = {mono(v; a, n)}\,d{v}$, so $v = {mono(v;... | correct | B16 |
| fluency-l10-undo-product.json | families[3].solution[1] | $\int v\,du = \int {mono(v; r, n)}\,d{v} = {mono(v; s, n1)}$. | correct | B16 |
| fluency-l10-undo-product.json | families[3].solution[2] | So the answer is ${mono(v; r, n1)}\ln {v}{-s:+cfrac}{v}^{{{n1}}} + C$. | correct | B16 |
