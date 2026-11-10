# Claim ledger: ito L4 (concept audit, blind)

Auditor: Fable, 10 Nov 2026. Scope: `app/content/courses/ito/` lessons l13 to l17, review-4, homework-4. One row for every prose line, question, graded key, derive line, option, `why`, hint, feedback line, slip, `accept` text, explain, summary line, rubric line and model answer. Verdicts: correct, wrong, imprecise, misleading, unverified. Basis: a named source (Shreve = *Stochastic Calculus for Finance II*; KS = Karatzas and Shreve, *Brownian Motion and Stochastic Calculus*; Williams = *Probability with Martingales*; Hull = *Options, Futures and Other Derivatives*, 10th ed.; C&B = Casella and Berger), a short derivation, or `sim: <check>` naming a check in `docs/reports/ito-L4-concepts.py`. A row carries its screen's basis unless it has its own. "Finding n" points to `docs/reviews/audit-ito-4.md`.

Rows: 1209. Verdicts: correct 1190, wrong 2, imprecise 16, misleading 1, unverified 0.

## l13-martingale-or-not.json

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l13-martingale-or-not.json | screens[0].prose | Topic 3.2 is optional: it serves derivatives pricing and desk quant roles, so traders and researchers may ski… | correct | Itô formula for f(t,W): drift f_t + ½f_xx (Shreve 4.4.1); sim: l13.s0 |
| l13-martingale-or-not.json | screens[0].question | Slide $c$ until the drift is zero at every $W_t$. | correct | Itô formula for f(t,W): drift f_t + ½f_xx (Shreve 4.4.1); sim: l13.s0 |
| l13-martingale-or-not.json | screens[0].widget.answer | graded key 3 | correct | Itô formula for f(t,W): drift f_t + ½f_xx (Shreve 4.4.1); sim: l13.s0 |
| l13-martingale-or-not.json | screens[0].hints[0].text | Watch the slope of the line as you slide. | correct | Itô formula for f(t,W): drift f_t + ½f_xx (Shreve 4.4.1); sim: l13.s0 |
| l13-martingale-or-not.json | screens[0].hints[1].text | The line is $(3 - c)x$: its slope is zero at one setting. | correct | Itô formula for f(t,W): drift f_t + ½f_xx (Shreve 4.4.1); sim: l13.s0 |
| l13-martingale-or-not.json | screens[0].feedback.correct | At $c = 3$ the line lies flat on zero: $W_t^3 - 3tW_t$ has no drift. | correct | Itô formula for f(t,W): drift f_t + ½f_xx (Shreve 4.4.1); sim: l13.s0 |
| l13-martingale-or-not.json | screens[0].feedback.generic | Not quite right. Look for the setting where the line lies flat along the axis. | correct | Itô formula for f(t,W): drift f_t + ½f_xx (Shreve 4.4.1); sim: l13.s0 |
| l13-martingale-or-not.json | screens[0].feedback.byKey.half-twice | You halved the second derivative twice. For $x^3$ it is $6x$, and half of it is $3x$. | correct | Itô formula for f(t,W): drift f_t + ½f_xx (Shreve 4.4.1); sim: l13.s0 |
| l13-martingale-or-not.json | screens[0].feedback.byKey.whole | You cancelled all of $f_{xx} = 6x$. Itô's lemma carries only half of it. | correct | Itô formula for f(t,W): drift f_t + ½f_xx (Shreve 4.4.1); sim: l13.s0 |
| l13-martingale-or-not.json | screens[0].explain.text | For $f = x^3 - ctx$ we have $f_t = -cx$ and $\tfrac12f_{xx} = 3x$. The drift $(3 - c)x$ vanishes at $c = 3$, … | imprecise | zero drift gives a local martingale; a martingale needs E∫f_x² dt < ∞, which the summary states. Finding 1 |
| l13-martingale-or-not.json | screens[1].prose | Why does zero drift make $f(t, W_t)$ a martingale? Build the argument, each line with its reason. Leave out t… | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].question | Put the lines in order. | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].widget.lines[0].text | Take a smooth $f(t, x)$ and the process $X_t = f(t, W_t)$. | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].widget.lines[1].text | Itô's lemma: $dX = f_t\,dt + f_x\,dW$ ${}+ \tfrac12f_{xx}\,(dW)^2$, and $(dW)^2 = dt$. | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].widget.lines[2].text | Collect terms: $dX = (f_t$ ${}+ \tfrac12f_{xx})\,dt$ ${}+ f_x\,dW$, a drift part and a noise part. | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].widget.lines[3].text | The noise part has mean zero given the past, so $E[dX \mid \mathcal F_t]$ ${}= (f_t + \tfrac12f_{xx})\,dt$. | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].widget.lines[4].text | So $X$ is a martingale when $f_t + \tfrac12f_{xx} = 0$, and not otherwise (if $f_x$ is tame). | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].widget.lines[5].text | Use the ordinary chain rule, $dX = f_t\,dt + f_x\,dW$, so the test is $f_t = 0$. | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].widget.lines[5].why | $(dW)^2 = dt$ is the same size as $dt$. The term $\tfrac12f_{xx}\,dt$ stays. | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].widget.lines[6].text | Check that $E[X_t]$ is the same for every $t$. That settles it. | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].widget.lines[6].why | A constant mean is necessary, not enough. A martingale must hold its forecast given the path so far. | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].hints[0].text | Start with Itô's lemma for $f(t, W_t)$. | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].hints[1].text | The $dW$ term has mean zero given the past. | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].feedback.correct | That is the drift test: $f_t + \tfrac12f_{xx} = 0$. | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].feedback.generic | Not quite right. Name the process, apply the lemma, collect the $dt$ terms, then drop the noise. | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].feedback.byKey.x1 | You used the ordinary chain rule. It misses the half-second-derivative term that Brownian noise adds. | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].feedback.byKey.x2 | You checked the mean over all paths. A martingale must also hold its forecast given the path so far. | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].feedback.byKey.left-out | A line of the argument is in the Left out list. Only the two flawed lines belong there. | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[1].explain.text | Only the $dt$ coefficient moves the forecast, so the test is a single line: $f_t + \tfrac12f_{xx} = 0$. Say t… | correct | Shreve Thm 4.4.1 and 4.3.1(iv): the dW integral is a martingale when E∫f_x² dt < ∞; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].prose | Drill, two minutes for four. Say the one-line reason aloud, then answer. At $t = 1$ and $W_t = 2$, find the d… | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].question | Fill in the drift (a whole number) and yes or no for each row. | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].widget.rows[0][1].answer | graded key 2 | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].widget.rows[0][2].answer | graded key no | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].widget.rows[1][1].answer | graded key 0 | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].widget.rows[1][2].answer | graded key yes | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].widget.rows[2][1].answer | graded key 0 | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].widget.rows[2][2].answer | graded key yes | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].widget.rows[3][1].answer | graded key 24 | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].widget.rows[3][2].answer | graded key no | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].hints[0].text | Work one row at a time: $f_t$ first, then $f_{xx}$. | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].hints[1].text | Add $f_t$ and half of $f_{xx}$. | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].hints[2].text | A martingale needs the drift to be zero at every point, not just this one. | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].feedback.correct | Drifts $2, 0, 0, 24$: only $e^{4W_t - 8t}$ and $W_t^3 - 3tW_t$ are martingales. | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].feedback.generic | Not quite right. Evaluate $f_t + \tfrac12f_{xx}$ at $t = 1$, $x = 2$, one row at a time. | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].feedback.byKey.r0c1 | For $W_t^2 + t$: $f_t = 1$ and $\tfrac12f_{xx} = 1$, so the drift is 2. Check for the whole $f_{xx}$ (3) or a… | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].feedback.byKey.r1c1 | For $e^{4x - 8t}$: $f_t = -8f$ and $\tfrac12f_{xx} = 8f$. They cancel. | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].feedback.byKey.r2c1 | For $x^3 - 3tx$: $f_t = -3x$ and $\tfrac12f_{xx} = 3x$. They cancel. | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].feedback.byKey.r3c1 | For $x^4$: $f_t = 0$ and $\tfrac12f_{xx} = 6x^2 = 24$. Without the half you would get 48. | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].feedback.byKey.r0c2 | A drift of 2 is not zero, so $W_t^2 + t$ is not a martingale. | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].feedback.byKey.r1c2 | Zero drift means a martingale. | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].feedback.byKey.r2c2 | Zero drift means a martingale. | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].feedback.byKey.r3c2 | A drift of 24 is not zero, so $W_t^4$ is not a martingale. | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[2].explain.text | Two of the four have drift. The same test sorts any smooth function of $(t, W_t)$ in seconds. | correct | sympy drifts at (1,2): 2, 0, 0, 24; sim: l13.s2 |
| l13-martingale-or-not.json | screens[3].prose | Now repair a process that fails. $W_t^4$ has drift $6W_t^2$. The term $-6\,tW_t^2$ cancels the $W_t^2$ part o… | correct | drift of x⁴ − 6tx² + ct² is (2c − 6)t; Hermite polynomial He₄ (KS Ex. 3.3.31); sim: l13.s3 |
| l13-martingale-or-not.json | screens[3].question | Which $c$ makes the drift of $W_t^4 - 6\,tW_t^2 + c\,t^2$ equal zero? | correct | drift of x⁴ − 6tx² + ct² is (2c − 6)t; Hermite polynomial He₄ (KS Ex. 3.3.31); sim: l13.s3 |
| l13-martingale-or-not.json | screens[3].widget.answer | graded key 3 | correct | drift of x⁴ − 6tx² + ct² is (2c − 6)t; Hermite polynomial He₄ (KS Ex. 3.3.31); sim: l13.s3 |
| l13-martingale-or-not.json | screens[3].widget.accept | The drift is $(2c - 6)t$, so $c = 3$. | correct | drift of x⁴ − 6tx² + ct² is (2c − 6)t; Hermite polynomial He₄ (KS Ex. 3.3.31); sim: l13.s3 |
| l13-martingale-or-not.json | screens[3].widget.wrong[0] | slip 6: wrong under every valid reading of the item | correct | drift of x⁴ − 6tx² + ct² is (2c − 6)t; slip arithmetic recomputed |
| l13-martingale-or-not.json | screens[3].widget.wrong[1] | slip 1.5: wrong under every valid reading of the item | correct | drift of x⁴ − 6tx² + ct² is (2c − 6)t; slip arithmetic recomputed |
| l13-martingale-or-not.json | screens[3].hints[0].text | Add the drift of the three terms. | correct | drift of x⁴ − 6tx² + ct² is (2c − 6)t; Hermite polynomial He₄ (KS Ex. 3.3.31); sim: l13.s3 |
| l13-martingale-or-not.json | screens[3].hints[1].text | $c\,t^2$ has $f_t = 2ct$ and $f_{xx} = 0$. | correct | drift of x⁴ − 6tx² + ct² is (2c − 6)t; Hermite polynomial He₄ (KS Ex. 3.3.31); sim: l13.s3 |
| l13-martingale-or-not.json | screens[3].hints[2].text | The $x^2$ terms already cancel. Collect the $t$ terms: $2ct - 6t$. | correct | drift of x⁴ − 6tx² + ct² is (2c − 6)t; Hermite polynomial He₄ (KS Ex. 3.3.31); sim: l13.s3 |
| l13-martingale-or-not.json | screens[3].feedback.correct | $c = 3$: $W_t^4 - 6tW_t^2 + 3t^2$ is a martingale. | correct | drift of x⁴ − 6tx² + ct² is (2c − 6)t; Hermite polynomial He₄ (KS Ex. 3.3.31); sim: l13.s3 |
| l13-martingale-or-not.json | screens[3].feedback.generic | Not quite right. Add the drift of each term: $6x^2$, then $-6x^2 - 6t$, then $2ct$. | correct | drift of x⁴ − 6tx² + ct² is (2c − 6)t; Hermite polynomial He₄ (KS Ex. 3.3.31); sim: l13.s3 |
| l13-martingale-or-not.json | screens[3].feedback.byKey.no-two | You took $f_t = ct$ for $ct^2$. The derivative of $t^2$ is $2t$, so the drift is $(2c - 6)t$. | correct | drift of x⁴ − 6tx² + ct² is (2c − 6)t; Hermite polynomial He₄ (KS Ex. 3.3.31); sim: l13.s3 |
| l13-martingale-or-not.json | screens[3].feedback.byKey.half-twice | You halved $-6t$ again, giving $2c = 3$. The term $-6tx^2$ already gives $\tfrac12f_{xx} = -6t$, so $2c = 6$. | correct | drift of x⁴ − 6tx² + ct² is (2c − 6)t; Hermite polynomial He₄ (KS Ex. 3.3.31); sim: l13.s3 |
| l13-martingale-or-not.json | screens[3].explain.text | A martingale keeps its mean at 0, so $E[W_t^4] = 6t\,E[W_t^2]$ ${}- 3t^2 = 3t^2$. One line replaces an integr… | correct | drift of x⁴ − 6tx² + ct² is (2c − 6)t; Hermite polynomial He₄ (KS Ex. 3.3.31); sim: l13.s3 |
| l13-martingale-or-not.json | screens[4].prose | Exponentials are the quickest case, because $f_t = cf$ and $\tfrac12f_{xx} = \tfrac12a^2f$ for $f = e^{aW_t +… | correct | exponential martingale exp(aW − ½a²t) (Shreve Thm 3.6.1); sim: l13.s4 |
| l13-martingale-or-not.json | screens[4].question | Which constant $c$ makes $e^{5W_t + ct}$ a martingale? | correct | exponential martingale exp(aW − ½a²t) (Shreve Thm 3.6.1); sim: l13.s4 |
| l13-martingale-or-not.json | screens[4].widget.answer | graded key -12.5 | correct | exponential martingale exp(aW − ½a²t) (Shreve Thm 3.6.1); sim: l13.s4 |
| l13-martingale-or-not.json | screens[4].widget.accept | $c + \tfrac12 \times 25 = 0$, so $c = -12.5$. | correct | exponential martingale exp(aW − ½a²t) (Shreve Thm 3.6.1); sim: l13.s4 |
| l13-martingale-or-not.json | screens[4].widget.wrong[0] | slip 12.5: wrong under every valid reading of the item | correct | exponential martingale exp(aW − ½a²t) (Shreve Thm 3.6.1); slip arithmetic recomputed |
| l13-martingale-or-not.json | screens[4].widget.wrong[1] | slip -2.5: wrong under every valid reading of the item | correct | exponential martingale exp(aW − ½a²t) (Shreve Thm 3.6.1); slip arithmetic recomputed |
| l13-martingale-or-not.json | screens[4].widget.wrong[2] | slip -25: wrong under every valid reading of the item | correct | exponential martingale exp(aW − ½a²t) (Shreve Thm 3.6.1); slip arithmetic recomputed |
| l13-martingale-or-not.json | screens[4].hints[0].text | Write $f_t$ and $\tfrac12f_{xx}$ for $f = e^{5x + ct}$. | correct | exponential martingale exp(aW − ½a²t) (Shreve Thm 3.6.1); sim: l13.s4 |
| l13-martingale-or-not.json | screens[4].hints[1].text | $f_t = cf$ and $f_{xx} = 25f$. | correct | exponential martingale exp(aW − ½a²t) (Shreve Thm 3.6.1); sim: l13.s4 |
| l13-martingale-or-not.json | screens[4].feedback.correct | $c = -12.5$: $e^{5W_t - 12.5t}$ is a martingale. | correct | exponential martingale exp(aW − ½a²t) (Shreve Thm 3.6.1); sim: l13.s4 |
| l13-martingale-or-not.json | screens[4].feedback.generic | Not quite right. The drift is $(c + \tfrac12a^2)f$. Set it to zero. | correct | exponential martingale exp(aW − ½a²t) (Shreve Thm 3.6.1); sim: l13.s4 |
| l13-martingale-or-not.json | screens[4].feedback.byKey.sign | You cancelled with the wrong sign. The drift is $c + 12.5$, so $c$ must be negative. | correct | exponential martingale exp(aW − ½a²t) (Shreve Thm 3.6.1); sim: l13.s4 |
| l13-martingale-or-not.json | screens[4].feedback.byKey.no-square | You used $\tfrac12a = 2.5$. The second derivative brings $a^2 = 25$. | correct | exponential martingale exp(aW − ½a²t) (Shreve Thm 3.6.1); sim: l13.s4 |
| l13-martingale-or-not.json | screens[4].feedback.byKey.no-half | You used $a^2 = 25$ without the half. Itô gives $\tfrac12 \times 25$. | correct | exponential martingale exp(aW − ½a²t) (Shreve Thm 3.6.1); sim: l13.s4 |
| l13-martingale-or-not.json | screens[4].explain.text | In general $e^{aW_t - \tfrac12a^2t}$ is a martingale. With $a = 1$ this is the $e^{W_t - t/2}$ that appears i… | correct | exponential martingale exp(aW − ½a²t) (Shreve Thm 3.6.1); sim: l13.s4 |
| l13-martingale-or-not.json | screens[5].prose | A candidate says: "$E[W_t^3] = 0$ for every $t$, so $W_t^3$ is a martingale." Test the claim. We watch $W_1 =… | correct | E[(2+Z)³] = 8 + 6E[Z²] = 14; sim: l13.s5 |
| l13-martingale-or-not.json | screens[5].question | What is $E[W_2^3 \mid W_1 = 2]$? | correct | E[(2+Z)³] = 8 + 6E[Z²] = 14; sim: l13.s5 |
| l13-martingale-or-not.json | screens[5].widget.answer | graded key 14 | correct | E[(2+Z)³] = 8 + 6E[Z²] = 14; sim: l13.s5 |
| l13-martingale-or-not.json | screens[5].widget.accept | $E[(2 + Z)^3] = 8 + 3 \times 2 \times E[Z^2] = 8 + 6 = 14$, not 8. | correct | E[(2+Z)³] = 8 + 6E[Z²] = 14; sim: l13.s5 |
| l13-martingale-or-not.json | screens[5].widget.wrong[0] | slip 8: wrong under every valid reading of the item | correct | E[(2+Z)³] = 8 + 6E[Z²] = 14; slip arithmetic recomputed |
| l13-martingale-or-not.json | screens[5].widget.wrong[1] | slip 0: wrong under every valid reading of the item | correct | E[(2+Z)³] = 8 + 6E[Z²] = 14; slip arithmetic recomputed |
| l13-martingale-or-not.json | screens[5].widget.wrong[2] | slip 6: wrong under every valid reading of the item | correct | E[(2+Z)³] = 8 + 6E[Z²] = 14; slip arithmetic recomputed |
| l13-martingale-or-not.json | screens[5].hints[0].text | Expand $(2 + Z)^3 = 8 + 12Z + 6Z^2$ ${}+ Z^3$. | correct | E[(2+Z)³] = 8 + 6E[Z²] = 14; sim: l13.s5 |
| l13-martingale-or-not.json | screens[5].hints[1].text | $E[Z] = 0$, $E[Z^2] = 1$ and $E[Z^3] = 0$. | correct | E[(2+Z)³] = 8 + 6E[Z²] = 14; sim: l13.s5 |
| l13-martingale-or-not.json | screens[5].feedback.correct | $14 \neq 8 = W_1^3$: the forecast moves, so $W_t^3$ is not a martingale. | correct | E[(2+Z)³] = 8 + 6E[Z²] = 14; sim: l13.s5 |
| l13-martingale-or-not.json | screens[5].feedback.generic | Not quite right. Expand $(2 + Z)^3$ and take the mean of each term. | correct | E[(2+Z)³] = 8 + 6E[Z²] = 14; sim: l13.s5 |
| l13-martingale-or-not.json | screens[5].feedback.byKey.martingale | You forecast $8 = W_1^3$, which is what a martingale would do. The cross term $3 \cdot 2 \cdot Z^2$ adds 6. | correct | E[(2+Z)³] = 8 + 6E[Z²] = 14; sim: l13.s5 |
| l13-martingale-or-not.json | screens[5].feedback.byKey.zero | You used the mean over all paths, 0. Given $W_1 = 2$, the forecast starts from 8. | correct | E[(2+Z)³] = 8 + 6E[Z²] = 14; sim: l13.s5 |
| l13-martingale-or-not.json | screens[5].feedback.byKey.drift-only | You kept only the drift: $3W = 6$ over one unit of time. You gave the gain alone, and the forecast is today's… | correct | E[(2+Z)³] = 8 + 6E[Z²] = 14; sim: l13.s5 |
| l13-martingale-or-not.json | screens[5].explain.text | The drift of $W^3$ is $3W$, and it pushes the forecast from 8 to 14. A constant mean (zero) is necessary for … | correct | E[(2+Z)³] = 8 + 6E[Z²] = 14; sim: l13.s5 |
| l13-martingale-or-not.json | screens[6].prose | Edge case. $d(tW_t) = W_t\,dt + t\,dW_t$, so $tW_t$ has drift $W_t$, which is random. We want to cancel it. | correct | product rule d(tW) = W dt + t dW (Shreve Cor. 4.6.3); tW − ∫W ds = ∫s dW; sim: l13.s6 |
| l13-martingale-or-not.json | screens[6].question | Which process is a martingale? | correct | product rule d(tW) = W dt + t dW (Shreve Cor. 4.6.3); tW − ∫W ds = ∫s dW; sim: l13.s6 |
| l13-martingale-or-not.json | screens[6].widget.options[0].text | $tW_t - \int_0^t W_s\,ds$ | correct | product rule d(tW) = W dt + t dW (Shreve Cor. 4.6.3); tW − ∫W ds = ∫s dW; sim: l13.s6 |
| l13-martingale-or-not.json | screens[6].widget.options[1].text | $tW_t - \tfrac12t^2$ | correct | product rule d(tW) = W dt + t dW (Shreve Cor. 4.6.3); tW − ∫W ds = ∫s dW; sim: l13.s6 |
| l13-martingale-or-not.json | screens[6].widget.options[1].why | You removed a drift of $t$. The drift is $W_t$, which is random, so no function of $t$ cancels it. | correct | product rule d(tW) = W dt + t dW (Shreve Cor. 4.6.3); tW − ∫W ds = ∫s dW; sim: l13.s6 |
| l13-martingale-or-not.json | screens[6].widget.options[2].text | $tW_t$ itself, because its mean is 0 | correct | product rule d(tW) = W dt + t dW (Shreve Cor. 4.6.3); tW − ∫W ds = ∫s dW; sim: l13.s6 |
| l13-martingale-or-not.json | screens[6].widget.options[2].why | You used the constant-mean test again. The forecast of $tW_t$ given the path still drifts. | correct | product rule d(tW) = W dt + t dW (Shreve Cor. 4.6.3); tW − ∫W ds = ∫s dW; sim: l13.s6 |
| l13-martingale-or-not.json | screens[6].widget.options[3].text | $tW_t + \int_0^t W_s\,ds$ | correct | product rule d(tW) = W dt + t dW (Shreve Cor. 4.6.3); tW − ∫W ds = ∫s dW; sim: l13.s6 |
| l13-martingale-or-not.json | screens[6].widget.options[3].why | You added the integral, doubling the drift. It must be subtracted to cancel it. | correct | product rule d(tW) = W dt + t dW (Shreve Cor. 4.6.3); tW − ∫W ds = ∫s dW; sim: l13.s6 |
| l13-martingale-or-not.json | screens[6].hints[0].text | The correction must cancel $W_t\,dt$ as time passes. | correct | product rule d(tW) = W dt + t dW (Shreve Cor. 4.6.3); tW − ∫W ds = ∫s dW; sim: l13.s6 |
| l13-martingale-or-not.json | screens[6].hints[1].text | $d\int_0^t W_s\,ds = W_t\,dt$. | correct | product rule d(tW) = W dt + t dW (Shreve Cor. 4.6.3); tW − ∫W ds = ∫s dW; sim: l13.s6 |
| l13-martingale-or-not.json | screens[6].feedback.correct | $d\big(tW_t$ ${}- \int_0^t W_s\,ds\big)$ ${}= t\,dW_t$: no drift left. | correct | product rule d(tW) = W dt + t dW (Shreve Cor. 4.6.3); tW − ∫W ds = ∫s dW; sim: l13.s6 |
| l13-martingale-or-not.json | screens[6].feedback.generic | Not quite right. The drift of $tW_t$ is $W_t\,dt$. Which choice subtracts exactly that? | correct | product rule d(tW) = W dt + t dW (Shreve Cor. 4.6.3); tW − ∫W ds = ∫s dW; sim: l13.s6 |
| l13-martingale-or-not.json | screens[6].explain.text | The correction is a running integral of the path, so this martingale is not a function of $(t, W_t)$ alone. T… | correct | product rule d(tW) = W dt + t dW (Shreve Cor. 4.6.3); tW − ∫W ds = ∫s dW; sim: l13.s6 |
| l13-martingale-or-not.json | screens[7].prose | The interviewer pushes the question one step: add a drift. Let $X_t = W_t + \mu t$ with $\mu = 0.75$. Then $X… | correct | Itô for X = W + μt: drift of e^{cX} is (μc + ½c²)f, roots 0 and −2μ (KS 3.5.C; Shreve Ex. 3.7); sim: l13.s7 |
| l13-martingale-or-not.json | screens[7].question | Which nonzero $c$ makes $e^{cX_t}$ a martingale? | correct | Itô for X = W + μt: drift of e^{cX} is (μc + ½c²)f, roots 0 and −2μ (KS 3.5.C; Shreve Ex. 3.7); sim: l13.s7 |
| l13-martingale-or-not.json | screens[7].widget.answer | graded key -1.5 | correct | Itô for X = W + μt: drift of e^{cX} is (μc + ½c²)f, roots 0 and −2μ (KS 3.5.C; Shreve Ex. 3.7); sim: l13.s7 |
| l13-martingale-or-not.json | screens[7].widget.accept | $\mu c + \tfrac12c^2 = 0$ gives $c = -2\mu = -1.5$. | correct | Itô for X = W + μt: drift of e^{cX} is (μc + ½c²)f, roots 0 and −2μ (KS 3.5.C; Shreve Ex. 3.7); sim: l13.s7 |
| l13-martingale-or-not.json | screens[7].widget.wrong[0] | slip -0.75: wrong under every valid reading of the item | correct | Itô for X = W + μt: drift of e^{cX} is (μc + ½c²)f, roots 0 and −2μ (KS 3.5.C; slip arithmetic recomputed |
| l13-martingale-or-not.json | screens[7].widget.wrong[1] | slip 1.5: wrong under every valid reading of the item | correct | Itô for X = W + μt: drift of e^{cX} is (μc + ½c²)f, roots 0 and −2μ (KS 3.5.C; slip arithmetic recomputed |
| l13-martingale-or-not.json | screens[7].hints[0].text | Factor $c(\mu + \tfrac12c) = 0$. | correct | Itô for X = W + μt: drift of e^{cX} is (μc + ½c²)f, roots 0 and −2μ (KS 3.5.C; Shreve Ex. 3.7); sim: l13.s7 |
| l13-martingale-or-not.json | screens[7].hints[1].text | The nonzero root solves $\mu + \tfrac12c = 0$. | correct | Itô for X = W + μt: drift of e^{cX} is (μc + ½c²)f, roots 0 and −2μ (KS 3.5.C; Shreve Ex. 3.7); sim: l13.s7 |
| l13-martingale-or-not.json | screens[7].feedback.correct | $c = -2\mu = -1.5$: $e^{-2\mu X_t}$ is a martingale, which the next lesson uses. | correct | Itô for X = W + μt: drift of e^{cX} is (μc + ½c²)f, roots 0 and −2μ (KS 3.5.C; Shreve Ex. 3.7); sim: l13.s7 |
| l13-martingale-or-not.json | screens[7].feedback.generic | Not quite right. Solve $\mu c + \tfrac12c^2 = 0$ for the nonzero root. | correct | Itô for X = W + μt: drift of e^{cX} is (μc + ½c²)f, roots 0 and −2μ (KS 3.5.C; Shreve Ex. 3.7); sim: l13.s7 |
| l13-martingale-or-not.json | screens[7].feedback.byKey.no-half | You solved $\mu c + c^2 = 0$, dropping the half in $\tfrac12c^2$. The root is $-2\mu$. | correct | Itô for X = W + μt: drift of e^{cX} is (μc + ½c²)f, roots 0 and −2μ (KS 3.5.C; Shreve Ex. 3.7); sim: l13.s7 |
| l13-martingale-or-not.json | screens[7].feedback.byKey.sign | You gave the root with the wrong sign. The drift of $X$ is positive, so $c$ must be negative. | correct | Itô for X = W + μt: drift of e^{cX} is (μc + ½c²)f, roots 0 and −2μ (KS 3.5.C; Shreve Ex. 3.7); sim: l13.s7 |
| l13-martingale-or-not.json | screens[7].explain.text | The exponent $-2\mu$ undoes the drift: $e^{-2\mu X_t}$ is a martingale for any $\mu$. Lesson 14 uses it to fi… | correct | Itô for X = W + μt: drift of e^{cX} is (μc + ½c²)f, roots 0 and −2μ (KS 3.5.C; Shreve Ex. 3.7); sim: l13.s7 |
| l13-martingale-or-not.json | screens[8].prose | Check it by machine. `ito_drift` estimates $f_t + \tfrac12f_{xx}$ by central differences with step $h$. `mart… | correct | solution run in CPython, 9/9 hidden tests, starter 0/9; sim: l13.s8 |
| l13-martingale-or-not.json | screens[8].question | Complete both functions. | correct | solution run in CPython, 9/9 hidden tests, starter 0/9; sim: l13.s8 |
| l13-martingale-or-not.json | screens[8].widget.solution | code solution: method taught and hidden tests | correct | solution run in CPython, 9/9 hidden tests, starter 0/9; sim: l13.s8 |
| l13-martingale-or-not.json | screens[8].widget.how | Submit runs 9 hidden tests: six drifts and three simulations on seed 4 with 100,000 draws. Martingales give 0… | correct | solution run in CPython, 9/9 hidden tests, starter 0/9; sim: l13.s8 |
| l13-martingale-or-not.json | screens[8].hints[0].text | $f_t \approx \dfrac{f(t + h, x) - f(t - h, x)}{2h}$. | correct | solution run in CPython, 9/9 hidden tests, starter 0/9; sim: l13.s8 |
| l13-martingale-or-not.json | screens[8].hints[1].text | $f_{xx} \approx \dfrac{f(x + h) - 2f(x) + f(x - h)}{h^2}$. | correct | solution run in CPython, 9/9 hidden tests, starter 0/9; sim: l13.s8 |
| l13-martingale-or-not.json | screens[8].hints[2].text | Simulate $W_T = \sqrt{T}\,Z$, apply $f$, and take the mean and its standard error. | correct | solution run in CPython, 9/9 hidden tests, starter 0/9; sim: l13.s8 |
| l13-martingale-or-not.json | screens[8].feedback.correct | $e^{W_t - t/2}$ keeps its mean 1 on seed 4 (0.9955, standard error 0.0074). The plain $e^{W_t}$ drifts to abo… | correct | solution run in CPython, 9/9 hidden tests, starter 0/9; sim: l13.s8 |
| l13-martingale-or-not.json | screens[8].feedback.generic | Not quite right. Check the example: the drift of $x^3$ at $x = 2$ is $3x = 6$. | correct | solution run in CPython, 9/9 hidden tests, starter 0/9; sim: l13.s8 |
| l13-martingale-or-not.json | screens[8].explain.text | Central differences give $f_t + \tfrac12f_{xx}$ to about $10^{-7}$ here. A martingale keeps $E[f(T, W_T)] = f… | correct | solution run in CPython, 9/9 hidden tests, starter 0/9; sim: l13.s8 |
| l13-martingale-or-not.json | screens[9].prose | A strats interview opens: "Is $e^{W_t}$ a martingale? If not, fix it, then tell me $E[e^{W_2}]$." You have th… | correct | E[e^{W_t}] = e^{t/2} (normal mgf; Shreve 3.6); sim: l13.s9 |
| l13-martingale-or-not.json | screens[9].question | What is $E[e^{W_2}]$? Give 4 decimal places. | correct | E[e^{W_t}] = e^{t/2} (normal mgf; Shreve 3.6); sim: l13.s9 |
| l13-martingale-or-not.json | screens[9].widget.answer | graded key 2.7183 | correct | E[e^{W_t}] = e^{t/2} (normal mgf; Shreve 3.6); sim: l13.s9 |
| l13-martingale-or-not.json | screens[9].widget.accept | The drift of $e^{W_t}$ is $\tfrac12e^{W_t}$, so $e^{W_t - t/2}$ is a martingale with mean 1. Then $E[e^{W_2}]… | correct | E[e^{W_t}] = e^{t/2} (normal mgf; Shreve 3.6); sim: l13.s9 |
| l13-martingale-or-not.json | screens[9].widget.wrong[0] | slip 1: wrong under every valid reading of the item | correct | E[e^{W_t}] = e^{t/2} (normal mgf; slip arithmetic recomputed |
| l13-martingale-or-not.json | screens[9].widget.wrong[1] | slip 7.3891: wrong under every valid reading of the item | correct | E[e^{W_t}] = e^{t/2} (normal mgf; slip arithmetic recomputed |
| l13-martingale-or-not.json | screens[9].widget.wrong[2] | slip 0.3679: wrong under every valid reading of the item | correct | E[e^{W_t}] = e^{t/2} (normal mgf; slip arithmetic recomputed |
| l13-martingale-or-not.json | screens[9].hints[0].text | The drift of $e^{W_t}$ is $\tfrac12e^{W_t}$. | correct | E[e^{W_t}] = e^{t/2} (normal mgf; Shreve 3.6); sim: l13.s9 |
| l13-martingale-or-not.json | screens[9].hints[1].text | So $e^{W_t - t/2}$ is a martingale, with mean 1 at every $t$. | correct | E[e^{W_t}] = e^{t/2} (normal mgf; Shreve 3.6); sim: l13.s9 |
| l13-martingale-or-not.json | screens[9].hints[2].text | Then $E[e^{W_2}] = e^{2/2} \cdot 1$. | correct | E[e^{W_t}] = e^{t/2} (normal mgf; Shreve 3.6); sim: l13.s9 |
| l13-martingale-or-not.json | screens[9].feedback.correct | $E[e^{W_t}] = e^{t/2}$, so at $t = 2$ it is $e = 2.7183$. | correct | E[e^{W_t}] = e^{t/2} (normal mgf; Shreve 3.6); sim: l13.s9 |
| l13-martingale-or-not.json | screens[9].feedback.generic | Not quite right. Fix the process with $e^{-t/2}$, keep its mean 1, then undo the fix. | correct | E[e^{W_t}] = e^{t/2} (normal mgf; Shreve 3.6); sim: l13.s9 |
| l13-martingale-or-not.json | screens[9].feedback.byKey.martingale | You treated $e^{W_t}$ as a martingale with mean 1. Its drift $\tfrac12e^{W_t}$ is not zero. | correct | E[e^{W_t}] = e^{t/2} (normal mgf; Shreve 3.6); sim: l13.s9 |
| l13-martingale-or-not.json | screens[9].feedback.byKey.no-half | You gave $e^t$. The correction is $e^{-t/2}$, because $\tfrac12$ of the second derivative counts. | correct | E[e^{W_t}] = e^{t/2} (normal mgf; Shreve 3.6); sim: l13.s9 |
| l13-martingale-or-not.json | screens[9].feedback.byKey.inverse | You gave $e^{-t/2}$ at $t = 2$. The correction divides the process, so the mean is $e^{+t/2}$. | correct | E[e^{W_t}] = e^{t/2} (normal mgf; Shreve 3.6); sim: l13.s9 |
| l13-martingale-or-not.json | screens[9].explain.text | Drift test, fix, number: thirty seconds. Shreve, Stochastic Calculus for Finance II, chapter 4, proves the te… | correct | E[e^{W_t}] = e^{t/2} (normal mgf; Shreve 3.6); sim: l13.s9 |
| l13-martingale-or-not.json | summary.ideas[0] | A smooth $f(t, W_t)$ with tame $f_x$ is a martingale exactly when its drift $f_t + \tfrac12f_{xx}$ is zero. T… | correct | Shreve Thm 4.3.1 and 4.4.1; a local martingale with E∫f_x² dt < ∞ is a martingale (KS Prop. 3.2.10) |
| l13-martingale-or-not.json | summary.ideas[1] | To repair a process, add the term that cancels its drift: $W_t^3 - 3tW_t$, $e^{W_t - t/2}$ and $W_t^4 - 6tW_t… | correct | Shreve Thm 4.3.1 and 4.4.1; a local martingale with E∫f_x² dt < ∞ is a martingale (KS Prop. 3.2.10) |
| l13-martingale-or-not.json | summary.ideas[2] | A martingale keeps its mean, so $E[W_t^4] = 3t^2$ follows in one line from its repair. | correct | Shreve Thm 4.3.1 and 4.4.1; a local martingale with E∫f_x² dt < ∞ is a martingale (KS Prop. 3.2.10) |
| l13-martingale-or-not.json | summary.formula.name | Drift test | correct | Shreve Thm 4.3.1 and 4.4.1; a local martingale with E∫f_x² dt < ∞ is a martingale (KS Prop. 3.2.10) |
| l13-martingale-or-not.json | summary.formula.note | Zero drift means a martingale when $f_x$ is tame, as for every process in this lesson. Add $\mu f_x$ if the p… | correct | Shreve Thm 4.3.1 and 4.4.1; a local martingale with E∫f_x² dt < ∞ is a martingale (KS Prop. 3.2.10) |
| l13-martingale-or-not.json | summary.trap | A constant mean is necessary for a martingale, not enough: $E[W_t^3] = 0$ and $W_t^3$ still drifts. | correct | Shreve Thm 4.3.1 and 4.4.1; a local martingale with E∫f_x² dt < ∞ is a martingale (KS Prop. 3.2.10) |
| l13-martingale-or-not.json | quiz[0].question | A process is $tW_t^2$. What is its drift at $t = 2$, $W_t = 3$? | correct | f = tx²: f_t = x², ½f_xx = t; sim: l13.quiz0 |
| l13-martingale-or-not.json | quiz[0].widget.answer | graded key 11 | correct | f = tx²: f_t = x², ½f_xx = t; sim: l13.quiz0 |
| l13-martingale-or-not.json | quiz[0].widget.accept | $f_t = x^2 = 9$ and $\tfrac12f_{xx} = t = 2$, so the drift is $11$. | correct | f = tx²: f_t = x², ½f_xx = t; sim: l13.quiz0 |
| l13-martingale-or-not.json | quiz[0].widget.wrong[0] | slip 9: wrong under every valid reading of the item | correct | f = tx²: f_t = x², ½f_xx = t; slip arithmetic recomputed |
| l13-martingale-or-not.json | quiz[0].widget.wrong[1] | slip 2: wrong under every valid reading of the item | correct | f = tx²: f_t = x², ½f_xx = t; slip arithmetic recomputed |
| l13-martingale-or-not.json | quiz[0].feedback.correct | $9 + 2 = 11$. | correct | f = tx²: f_t = x², ½f_xx = t; sim: l13.quiz0 |
| l13-martingale-or-not.json | quiz[0].feedback.generic | Not quite right. Add $f_t$ and $\tfrac12f_{xx}$ for $f = tx^2$. | correct | f = tx²: f_t = x², ½f_xx = t; sim: l13.quiz0 |
| l13-martingale-or-not.json | quiz[0].feedback.byKey.no-fxx | You left out $\tfrac12f_{xx} = t = 2$. The lemma has both terms. | correct | f = tx²: f_t = x², ½f_xx = t; sim: l13.quiz0 |
| l13-martingale-or-not.json | quiz[0].feedback.byKey.no-ft | You kept $\tfrac12f_{xx} = 2$ and left out $f_t = x^2 = 9$. | correct | f = tx²: f_t = x², ½f_xx = t; sim: l13.quiz0 |
| l13-martingale-or-not.json | quiz[0].explain.text | $f_t = W_t^2 = 9$ and $f_{xx} = 2t = 4$, so half of it is 2. The drift is not zero, so $tW_t^2$ is not a mart… | correct | f = tx²: f_t = x², ½f_xx = t; sim: l13.quiz0 |
| l13-martingale-or-not.json | quiz[1].question | For which constant $c$ is $e^{ct}\cos(2W_t)$ a martingale? | correct | f = e^{ct}cos 2x: ½f_xx = −2f; sim: l13.quiz1 |
| l13-martingale-or-not.json | quiz[1].widget.answer | graded key 2 | correct | f = e^{ct}cos 2x: ½f_xx = −2f; sim: l13.quiz1 |
| l13-martingale-or-not.json | quiz[1].widget.accept | $f_t = cf$ and $\tfrac12f_{xx} = \tfrac12(-4)f = -2f$, so $c = 2$. | correct | f = e^{ct}cos 2x: ½f_xx = −2f; sim: l13.quiz1 |
| l13-martingale-or-not.json | quiz[1].widget.wrong[0] | slip -2: wrong under every valid reading of the item | correct | f = e^{ct}cos 2x: ½f_xx = −2f; slip arithmetic recomputed |
| l13-martingale-or-not.json | quiz[1].widget.wrong[1] | slip 4: wrong under every valid reading of the item | correct | f = e^{ct}cos 2x: ½f_xx = −2f; slip arithmetic recomputed |
| l13-martingale-or-not.json | quiz[1].feedback.correct | $c = 2$. | correct | f = e^{ct}cos 2x: ½f_xx = −2f; sim: l13.quiz1 |
| l13-martingale-or-not.json | quiz[1].feedback.generic | Not quite right. Set $c - \tfrac12 \times 4 = 0$. | correct | f = e^{ct}cos 2x: ½f_xx = −2f; sim: l13.quiz1 |
| l13-martingale-or-not.json | quiz[1].feedback.byKey.sign | You took $c = -2$, the value of $\tfrac12f_{xx}/f$. It must cancel it, so $c = +2$. | correct | f = e^{ct}cos 2x: ½f_xx = −2f; sim: l13.quiz1 |
| l13-martingale-or-not.json | quiz[1].feedback.byKey.no-half | You used $f_{xx} = -4f$ without the half. Itô carries $\tfrac12f_{xx} = -2f$. | correct | f = e^{ct}cos 2x: ½f_xx = −2f; sim: l13.quiz1 |
| l13-martingale-or-not.json | quiz[1].explain.text | Differentiating $\cos(2x)$ twice gives $-4\cos(2x)$. Half of that is $-2f$, and $f_t = cf$ must add $+2f$. | correct | f = e^{ct}cos 2x: ½f_xx = −2f; sim: l13.quiz1 |
| l13-martingale-or-not.json | quiz[2].question | Using the martingale $W_t^4 - 6tW_t^2 + 3t^2$, what is $E[W_3^4]$? | correct | E[W_t⁴] = 3t² (normal fourth moment); sim: l13.s3/quiz2 |
| l13-martingale-or-not.json | quiz[2].widget.answer | graded key 27 | correct | E[W_t⁴] = 3t² (normal fourth moment); sim: l13.s3/quiz2 |
| l13-martingale-or-not.json | quiz[2].widget.accept | $E[W_3^4] = 6 \times 3 \times E[W_3^2] - 3 \times 9 = 54 - 27 = 27 = 3t^2$. | correct | E[W_t⁴] = 3t² (normal fourth moment); sim: l13.s3/quiz2 |
| l13-martingale-or-not.json | quiz[2].widget.wrong[0] | slip 9: wrong under every valid reading of the item | correct | E[W_t⁴] = 3t² (normal fourth moment); slip arithmetic recomputed |
| l13-martingale-or-not.json | quiz[2].widget.wrong[1] | slip 81: wrong under every valid reading of the item | correct | E[W_t⁴] = 3t² (normal fourth moment); slip arithmetic recomputed |
| l13-martingale-or-not.json | quiz[2].feedback.correct | $3t^2 = 27$. | correct | E[W_t⁴] = 3t² (normal fourth moment); sim: l13.s3/quiz2 |
| l13-martingale-or-not.json | quiz[2].feedback.generic | Not quite right. The martingale has mean 0 at $t = 3$, and $E[W_3^2] = 3$. | correct | E[W_t⁴] = 3t² (normal fourth moment); sim: l13.s3/quiz2 |
| l13-martingale-or-not.json | quiz[2].feedback.byKey.squared | You gave $t^2 = 9$, the square of the variance. The fourth moment of a normal is $3\sigma^4$. | correct | E[W_t⁴] = 3t² (normal fourth moment); sim: l13.s3/quiz2 |
| l13-martingale-or-not.json | quiz[2].feedback.byKey.fourth | You gave $t^4 = 81$. The fourth moment is $3\sigma^4 = 3t^2$. | correct | E[W_t⁴] = 3t² (normal fourth moment); sim: l13.s3/quiz2 |
| l13-martingale-or-not.json | quiz[2].explain.text | Setting the mean of the martingale to its start value 0 gives $E[W_t^4] = 6t \cdot t - 3t^2$ ${}= 3t^2$. At $… | correct | E[W_t⁴] = 3t² (normal fourth moment); sim: l13.s3/quiz2 |
| l13-martingale-or-not.json | quiz[3].prose | A candidate says $W_t^3$ is a martingale because $E[W_t^3] = 0$ for every $t$. | correct | E[(w + √(t−s)Z)³] = w³ + 3(t−s)w; sim: l13.quiz3 |
| l13-martingale-or-not.json | quiz[3].question | Which reply rebuts it in one line? | correct | E[(w + √(t−s)Z)³] = w³ + 3(t−s)w; sim: l13.quiz3 |
| l13-martingale-or-not.json | quiz[3].widget.options[0].text | Given $W_s$, the forecast of $W_t^3$ is $W_s^3 + 3(t - s)W_s$, not $W_s^3$. | correct | E[(w + √(t−s)Z)³] = w³ + 3(t−s)w; sim: l13.quiz3 |
| l13-martingale-or-not.json | quiz[3].widget.options[1].text | The mean of $W_t^3$ is not zero for positive $t$, so the claim fails. | correct | E[(w + √(t−s)Z)³] = w³ + 3(t−s)w; sim: l13.quiz3 |
| l13-martingale-or-not.json | quiz[3].widget.options[1].why | You disputed the mean. By symmetry it is zero, so the fault lies elsewhere. | correct | E[(w + √(t−s)Z)³] = w³ + 3(t−s)w; sim: l13.quiz3 |
| l13-martingale-or-not.json | quiz[3].widget.options[2].text | A cube of a normal variable is not normal, so no martingale. | correct | E[(w + √(t−s)Z)³] = w³ + 3(t−s)w; sim: l13.quiz3 |
| l13-martingale-or-not.json | quiz[3].widget.options[2].why | You tested the shape of the distribution. Martingales need not be normal. | correct | E[(w + √(t−s)Z)³] = w³ + 3(t−s)w; sim: l13.quiz3 |
| l13-martingale-or-not.json | quiz[3].widget.options[3].text | Itô's lemma does not apply to a cube of $W_t$, so the claim is void. | correct | E[(w + √(t−s)Z)³] = w³ + 3(t−s)w; sim: l13.quiz3 |
| l13-martingale-or-not.json | quiz[3].widget.options[3].why | You doubted the lemma. It applies to any smooth $f$, cubes included. | correct | E[(w + √(t−s)Z)³] = w³ + 3(t−s)w; sim: l13.quiz3 |
| l13-martingale-or-not.json | quiz[3].feedback.correct | The forecast given the past moves: that is what a martingale forbids. | correct | E[(w + √(t−s)Z)³] = w³ + 3(t−s)w; sim: l13.quiz3 |
| l13-martingale-or-not.json | quiz[3].feedback.generic | Not quite right. Compare the forecast given $W_s$ with $W_s^3$. | correct | E[(w + √(t−s)Z)³] = w³ + 3(t−s)w; sim: l13.quiz3 |
| l13-martingale-or-not.json | quiz[3].explain.text | The extra $3(t - s)W_s$ is the accumulated drift $3W\,dt$. Subtracting $3tW_t$ removes it. | correct | E[(w + √(t−s)Z)³] = w³ + 3(t−s)w; sim: l13.quiz3 |

## l14-hitting-and-exit.json

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l14-hitting-and-exit.json | screens[0].prose | Brownian motion starts at 0 and stops when it first touches $+1$ or $-2$. Each faint path is one run; press N… | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[0].question | Of the paths that reach a barrier, about what share reach $+1$ first? | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[0].widget.options[0].text | $\tfrac13$ | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[0].widget.options[0].why | You took the near barrier's distance, 1, over the total, 3. That is the wrong way up: the nearer barrier is h… | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[0].widget.options[1].text | $\tfrac12$ | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[0].widget.options[1].why | You assumed symmetry. The barriers are at different distances, and the count is far from even. | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[0].widget.options[2].text | $\tfrac23$ | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[0].widget.options[3].text | about $\tfrac{9}{10}$ | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[0].widget.options[3].why | You assumed the nearer barrier nearly always wins. The count shows a sizeable minority reaching $-2$. | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[0].hints[0].text | Divide the top count by the sum of the two counts. | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[0].hints[1].text | Press New paths a few times and watch the share settle. | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[0].feedback.correct | About two thirds: $\tfrac23 = \dfrac{2}{1 + 2}$, the distance to the far barrier over the total. | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[0].feedback.generic | Not quite right. Read the two counts and divide the top count by their sum. | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[0].feedback.byKey.third | You gave the near distance over the total. The count shows the top hit more often than the bottom. | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[0].feedback.byKey.half | The counts are not equal. The top barrier is hit about twice as often. | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[0].feedback.byKey.nearly | The bottom barrier still takes about a third of the paths. | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[0].explain.text | The nearer barrier wins about twice as often: $\tfrac23$ to $\tfrac13$, the ratio of the distances 2 and 1. T… | correct | P = b/(a+b) (KS Prob. 2.8.13; Shreve Ex. 3.7 as μ → 0); sim: l14.s0 |
| l14-hitting-and-exit.json | screens[1].prose | Now derive it. Let $\tau$ be the first time $W$ leaves $(-b, a)$. Each line carries its reason. Leave out the… | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].question | Put the lines in order. Finish the chance before the time. | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].widget.lines[0].text | $W$ is a martingale and stays in $[-b, a]$ until $\tau$, so optional stopping gives $E[W_\tau] = 0$. | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].widget.lines[1].text | $W_\tau$ is $a$ with chance $P$ and $-b$ otherwise, so $Pa - (1 - P)b = 0$. | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].widget.lines[2].text | Solve: $P = \dfrac{b}{a + b}$, the far distance over the total. | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].widget.lines[3].text | $W_t^2 - t$ is a martingale too (drift $-1 + \tfrac12 \cdot 2 = 0$), so $E[W_\tau^2] = E[\tau]$. | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].widget.lines[4].text | Compute $E[W_\tau^2] = Pa^2 + (1$ ${}- P)b^2$ ${}= \dfrac{ba^2 + ab^2}{a + b}$ ${}= ab$, so $E[\tau] = ab$. | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].widget.lines[5].text | $E[W_\tau] = 0$ holds for every stopping time, so no conditions need checking. | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].widget.lines[5].why | A stopping time with an infinite mean can break the rule. Two barriers keep $W$ bounded; one barrier does not. | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].widget.lines[6].text | The path must cover the distance $a + b$, so $E[\tau] = a + b$. | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].widget.lines[6].why | Distance is not time. Brownian paths wander, and the time grows like distance squared. | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].hints[0].text | Stop $W$ at the exit time and use its mean. | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].hints[1].text | $W^2 - t$ gives the second equation. | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].feedback.correct | Two martingales, two barriers: $P = b/(a + b)$ and $E[\tau] = ab$. | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].feedback.generic | Not quite right. Stop the martingale $W$ first, then $W^2 - t$. | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].feedback.byKey.x1 | You skipped the conditions. Optional stopping needs a bounded stopped value or a finite mean time. | imprecise | a finite mean time suffices for W and W² − t (Wald, KS Prob. 2.7.19), not for a general martingale: exp(2W − 2t) stopped at W = t − 1 has E[τ] = 1 and mean e⁻². sim: l14.s1.x1 EXPECTED_FAIL. Finding 2 |
| l14-hitting-and-exit.json | screens[1].feedback.byKey.x2 | You equated time with distance. Brownian motion needs about distance squared in time. | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].feedback.byKey.left-out | A line of the derivation is in the Left out list. Only the two flawed lines belong there. | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[1].explain.text | Markov lesson 8 found $k/N$ for the fair walk. Here is the continuous form: $P = b/(a + b)$, and the walk's s… | correct | optional sampling for a bounded stopped martingale, Wald identities for BM (KS Thm 1.3.22, Prob. 2.7.19); sim: l14.s1 |
| l14-hitting-and-exit.json | screens[2].prose | Drill, two minutes. Say the one-line reason aloud first. Now $a = 2$ and $b = 3$: the path stops at $+2$ or $… | correct | P = 3/5, E[τ] = ab = 6; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[2].question | Give $P$(reach $+2$ first) and $E[\tau]$ as decimals. | correct | P = 3/5, E[τ] = ab = 6; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[2].widget.rows[0][1].answer | graded key 0.6 | correct | P = 3/5, E[τ] = ab = 6; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[2].widget.rows[1][1].answer | graded key 6 | correct | P = 3/5, E[τ] = ab = 6; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[2].hints[0].text | The far distance is 3, the total is 5. | correct | P = 3/5, E[τ] = ab = 6; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[2].hints[1].text | $E[\tau] = a \times b$. | correct | P = 3/5, E[τ] = ab = 6; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[2].feedback.correct | $P = 3/5 = 0.6$ and $E[\tau] = 2 \times 3 = 6$. | correct | P = 3/5, E[τ] = ab = 6; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[2].feedback.generic | Not quite right. $P = b/(a + b)$ and $E[\tau] = ab$. | correct | P = 3/5, E[τ] = ab = 6; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[2].feedback.byKey.r0c1 | $P = b/(a + b) = 3/5$. The values 0.4 (near distance over total) and 0.5 (symmetry) are the usual slips. | correct | P = 3/5, E[τ] = ab = 6; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[2].feedback.byKey.r1c1 | $E[\tau] = ab = 6$. The value 5 is $a + b$, the distance covered, which is not the time. | correct | P = 3/5, E[τ] = ab = 6; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[2].explain.text | $P = \tfrac35$ because the barrier at $-3$ is the far one, and $E[\tau] = 6$ time units. Say the reason befor… | correct | P = 3/5, E[τ] = ab = 6; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[3].prose | Driftless Brownian motion reaches $+1$ sooner or later, with chance 1. A candidate stops at $+1$ alone and wr… | correct | P(τ_a > t) = 2Φ(a/√t) − 1, so τ_a < ∞ a.s. and E[τ_a] = ∞ (Shreve Thm 3.7.1, Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | screens[3].question | Why does optional stopping not apply to one barrier? | correct | P(τ_a > t) = 2Φ(a/√t) − 1, so τ_a < ∞ a.s. and E[τ_a] = ∞ (Shreve Thm 3.7.1, Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | screens[3].widget.options[0].text | $E[\tau] = \infty$, so the rule's conditions fail | correct | P(τ_a > t) = 2Φ(a/√t) − 1, so τ_a < ∞ a.s. and E[τ_a] = ∞ (Shreve Thm 3.7.1, Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | screens[3].widget.options[1].text | the path may never reach $+1$, so $W_\tau$ is undefined | correct | P(τ_a > t) = 2Φ(a/√t) − 1, so τ_a < ∞ a.s. and E[τ_a] = ∞ (Shreve Thm 3.7.1, Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | screens[3].widget.options[1].why | You doubted the hit. It happens with probability 1; the problem is the length of the wait. | correct | P(τ_a > t) = 2Φ(a/√t) − 1, so τ_a < ∞ a.s. and E[τ_a] = ∞ (Shreve Thm 3.7.1, Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | screens[3].widget.options[2].text | $W_t$ is not a martingale until a barrier is added | correct | P(τ_a > t) = 2Φ(a/√t) − 1, so τ_a < ∞ a.s. and E[τ_a] = ∞ (Shreve Thm 3.7.1, Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | screens[3].widget.options[2].why | You doubted the martingale. $W_t$ is one with or without a barrier. | correct | P(τ_a > t) = 2Φ(a/√t) − 1, so τ_a < ∞ a.s. and E[τ_a] = ∞ (Shreve Thm 3.7.1, Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | screens[3].widget.options[3].text | stopping at $+1$ gives the path a drift | correct | P(τ_a > t) = 2Φ(a/√t) − 1, so τ_a < ∞ a.s. and E[τ_a] = ∞ (Shreve Thm 3.7.1, Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | screens[3].widget.options[3].why | You added a drift. The stopped process has none; the failure comes from passing to infinite time. | correct | P(τ_a > t) = 2Φ(a/√t) − 1, so τ_a < ∞ a.s. and E[τ_a] = ∞ (Shreve Thm 3.7.1, Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | screens[3].hints[0].text | Think about the average waiting time for $+1$. | correct | P(τ_a > t) = 2Φ(a/√t) − 1, so τ_a < ∞ a.s. and E[τ_a] = ∞ (Shreve Thm 3.7.1, Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | screens[3].hints[1].text | Let $b$ grow in $E[\tau] = ab$. | correct | P(τ_a > t) = 2Φ(a/√t) − 1, so τ_a < ∞ a.s. and E[τ_a] = ∞ (Shreve Thm 3.7.1, Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | screens[3].feedback.correct | The hit is certain, but its mean time is infinite, so $E[W_\tau] = 0$ is not available. | correct | P(τ_a > t) = 2Φ(a/√t) − 1, so τ_a < ∞ a.s. and E[τ_a] = ∞ (Shreve Thm 3.7.1, Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | screens[3].feedback.generic | Not quite right. The path does reach $+1$. Ask how long it takes on average. | correct | P(τ_a > t) = 2Φ(a/√t) − 1, so τ_a < ∞ a.s. and E[τ_a] = ∞ (Shreve Thm 3.7.1, Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | screens[3].feedback.byKey.never | You said the path may never arrive. It arrives with probability 1. | correct | P(τ_a > t) = 2Φ(a/√t) − 1, so τ_a < ∞ a.s. and E[τ_a] = ∞ (Shreve Thm 3.7.1, Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | screens[3].feedback.byKey.notmart | You said $W$ stops being fair. A martingale stays a martingale. | correct | P(τ_a > t) = 2Φ(a/√t) − 1, so τ_a < ∞ a.s. and E[τ_a] = ∞ (Shreve Thm 3.7.1, Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | screens[3].feedback.byKey.drift | You gave the stopped path a drift. It has none at any fixed time. | correct | P(τ_a > t) = 2Φ(a/√t) − 1, so τ_a < ∞ a.s. and E[τ_a] = ∞ (Shreve Thm 3.7.1, Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | screens[3].explain.text | At each fixed time the stopped mean is 0: paths that hit $+1$ are balanced by paths still far below. Their wa… | imprecise | an infinite mean wait does not by itself give E[W_τ] ≠ 0 (τ = first zero after time 1 has E[τ] = ∞ and W_τ = 0). Finding 3 |
| l14-hitting-and-exit.json | screens[4].prose | Now add a drift: $X_t = \mu t + W_t$, from 0, stopped at $+a$ or $-b$. Lesson 13 gave the martingale $e^{-2\m… | correct | scale function e^{−2μx/σ²}: P solves ½σ²u″ + μu′ = 0 (KS 5.5.B; Shreve Ex. 3.7); sim: l14.s4 |
| l14-hitting-and-exit.json | screens[4].question | Solve for $P$, the chance of reaching $+a$ first. | correct | scale function e^{−2μx/σ²}: P solves ½σ²u″ + μu′ = 0 (KS 5.5.B; Shreve Ex. 3.7); sim: l14.s4 |
| l14-hitting-and-exit.json | screens[4].widget.answer | graded key \frac{1-e^{2\mu b}}{e^{-2\mu a}-e^{2\mu b}} | correct | scale function e^{−2μx/σ²}: P solves ½σ²u″ + μu′ = 0 (KS 5.5.B; Shreve Ex. 3.7); sim: l14.s4 |
| l14-hitting-and-exit.json | screens[4].widget.wrong[0] | slip \frac{1-e^{-2\mu b}}{e^{2\mu a}-e^{-2\mu b}}: wrong under every valid reading of the item | correct | scale function e^{−2μx/σ²}: P solves ½σ²u″ + μu′ = 0 (KS 5.5.B; slip arithmetic recomputed |
| l14-hitting-and-exit.json | screens[4].widget.wrong[1] | slip \frac{b}{a+b}: wrong under every valid reading of the item | correct | scale function e^{−2μx/σ²}: P solves ½σ²u″ + μu′ = 0 (KS 5.5.B; slip arithmetic recomputed |
| l14-hitting-and-exit.json | screens[4].hints[0].text | Expand: $P\,e^{-2\mu a} + e^{2\mu b}$ ${}- P\,e^{2\mu b} = 1$. | correct | scale function e^{−2μx/σ²}: P solves ½σ²u″ + μu′ = 0 (KS 5.5.B; Shreve Ex. 3.7); sim: l14.s4 |
| l14-hitting-and-exit.json | screens[4].hints[1].text | Move the terms without $P$ to the right. | correct | scale function e^{−2μx/σ²}: P solves ½σ²u″ + μu′ = 0 (KS 5.5.B; Shreve Ex. 3.7); sim: l14.s4 |
| l14-hitting-and-exit.json | screens[4].feedback.correct | $P$ ${}= \dfrac{1 - e^{2\mu b}}{e^{-2\mu a} - e^{2\mu b}}$. At $\mu \to 0$ it tends to $b/(a + b)$. | correct | scale function e^{−2μx/σ²}: P solves ½σ²u″ + μu′ = 0 (KS 5.5.B; Shreve Ex. 3.7); sim: l14.s4 |
| l14-hitting-and-exit.json | screens[4].feedback.generic | Not quite right. Collect the terms in $P$: $P(e^{-2\mu a} - e^{2\mu b})$ ${}= 1 - e^{2\mu b}$. | correct | scale function e^{−2μx/σ²}: P solves ½σ²u″ + μu′ = 0 (KS 5.5.B; Shreve Ex. 3.7); sim: l14.s4 |
| l14-hitting-and-exit.json | screens[4].feedback.byKey.flipped | You flipped the sign of $\mu$ throughout. That is the chance of reaching $+a$ first when the drift is reverse… | correct | scale function e^{−2μx/σ²}: P solves ½σ²u″ + μu′ = 0 (KS 5.5.B; Shreve Ex. 3.7); sim: l14.s4 |
| l14-hitting-and-exit.json | screens[4].feedback.byKey.driftless | You gave the driftless answer $b/(a + b)$. The drift changes the odds, as the curve shows. | correct | scale function e^{−2μx/σ²}: P solves ½σ²u″ + μu′ = 0 (KS 5.5.B; Shreve Ex. 3.7); sim: l14.s4 |
| l14-hitting-and-exit.json | screens[4].explain.text | Solving gives $P = (1 - e^{2\mu b})/(e^{-2\mu a} - e^{2\mu b})$. The curve crosses $\mu = 0$ at $b/(a + b)$ w… | correct | scale function e^{−2μx/σ²}: P solves ½σ²u″ + μu′ = 0 (KS 5.5.B; Shreve Ex. 3.7); sim: l14.s4 |
| l14-hitting-and-exit.json | screens[5].prose | Take $\mu = 0.5$ and $a = b = 1$ (unit volatility). Then $P = 1/(1 + e^{-1})$. For the exit time, stop the ma… | correct | Wald: X_t − μt stopped at the bounded exit (KS 3.5.D); sim: l14.s5 |
| l14-hitting-and-exit.json | screens[5].question | Give $P$ and $E[\tau]$ to 4 decimal places. | correct | Wald: X_t − μt stopped at the bounded exit (KS 3.5.D); sim: l14.s5 |
| l14-hitting-and-exit.json | screens[5].widget.rows[0][1].answer | graded key 0.7311 | correct | Wald: X_t − μt stopped at the bounded exit (KS 3.5.D); sim: l14.s5 |
| l14-hitting-and-exit.json | screens[5].widget.rows[1][1].answer | graded key 0.9242 | correct | Wald: X_t − μt stopped at the bounded exit (KS 3.5.D); sim: l14.s5 |
| l14-hitting-and-exit.json | screens[5].hints[0].text | $e^{-1} = 0.3679$, so $P = 1/1.3679$. | correct | Wald: X_t − μt stopped at the bounded exit (KS 3.5.D); sim: l14.s5 |
| l14-hitting-and-exit.json | screens[5].hints[1].text | $aP - b(1 - P) = 2P - 1$ ${}= 0.4621$. | correct | Wald: X_t − μt stopped at the bounded exit (KS 3.5.D); sim: l14.s5 |
| l14-hitting-and-exit.json | screens[5].hints[2].text | Divide by $\mu = 0.5$. | correct | Wald: X_t − μt stopped at the bounded exit (KS 3.5.D); sim: l14.s5 |
| l14-hitting-and-exit.json | screens[5].feedback.correct | $P = 0.7311$ and $E[\tau] = (2P - 1)/0.5$ ${}= 0.9242$. | correct | Wald: X_t − μt stopped at the bounded exit (KS 3.5.D); sim: l14.s5 |
| l14-hitting-and-exit.json | screens[5].feedback.generic | Not quite right. $P = 1/(1 + e^{-1})$, then $E[\tau] = (aP - b(1 - P))/\mu$. | correct | Wald: X_t − μt stopped at the bounded exit (KS 3.5.D); sim: l14.s5 |
| l14-hitting-and-exit.json | screens[5].feedback.byKey.r0c1 | $P = 1/(1 + e^{-1}) = 0.7311$. Using $e^{+1}$ gives 0.2689, the other barrier. | correct | Wald: X_t − μt stopped at the bounded exit (KS 3.5.D); sim: l14.s5 |
| l14-hitting-and-exit.json | screens[5].feedback.byKey.r1c1 | $E[\tau] = (0.7311$ ${}- 0.2689)/0.5 = 0.9242$ from unrounded values. The value 1 comes from $ab = 1$, which … | correct | Wald: X_t − μt stopped at the bounded exit (KS 3.5.D); sim: l14.s5 |
| l14-hitting-and-exit.json | screens[5].explain.text | The drift lifts $P$ from 0.5 to 0.7311 and shortens the exit from $ab = 1$ to 0.9242. Both numbers come from … | correct | Wald: X_t − μt stopped at the bounded exit (KS 3.5.D); sim: l14.s5 |
| l14-hitting-and-exit.json | screens[6].prose | Edge case: volatility. For $X_t = \sigma W_t$ with no drift, $P$ is unchanged, but $X_t^2 - \sigma^2t$ is the… | correct | X² − σ²t is a martingale for X = σW; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[6].question | What is $E[\tau]$ for $a = 2$, $b = 3$ and $\sigma = 2$? | correct | X² − σ²t is a martingale for X = σW; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[6].widget.answer | graded key 1.5 | correct | X² − σ²t is a martingale for X = σW; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[6].widget.accept | $E[X_\tau^2] = ab = 6$ and $E[X_\tau^2] = \sigma^2E[\tau] = 4E[\tau]$, so $E[\tau] = 1.5$. | correct | X² − σ²t is a martingale for X = σW; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[6].widget.wrong[0] | slip 6: wrong under every valid reading of the item | correct | X² − σ²t is a martingale for X = σW; slip arithmetic recomputed |
| l14-hitting-and-exit.json | screens[6].widget.wrong[1] | slip 3: wrong under every valid reading of the item | correct | X² − σ²t is a martingale for X = σW; slip arithmetic recomputed |
| l14-hitting-and-exit.json | screens[6].hints[0].text | $E[X_\tau^2] = ab$, because $X_\tau$ is $a$ or $-b$. | correct | X² − σ²t is a martingale for X = σW; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[6].hints[1].text | $\sigma^2E[\tau] = ab$. | correct | X² − σ²t is a martingale for X = σW; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[6].feedback.correct | $E[\tau] = ab/\sigma^2 = 6/4$ ${}= 1.5$: doubling the volatility cuts the time by 4. | correct | X² − σ²t is a martingale for X = σW; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[6].feedback.generic | Not quite right. The martingale is $X_t^2 - \sigma^2t$. Equate $ab$ with $\sigma^2E[\tau]$. | correct | X² − σ²t is a martingale for X = σW; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[6].feedback.byKey.none | You kept $E[\tau] = ab = 6$. Volatility $\sigma = 2$ makes the path move faster. | correct | X² − σ²t is a martingale for X = σW; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[6].feedback.byKey.unsquared | You divided by $\sigma = 2$ rather than $\sigma^2 = 4$. | correct | X² − σ²t is a martingale for X = σW; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[6].explain.text | Time scales with $1/\sigma^2$: variance builds as $\sigma^2t$. With drift, the exponent in $P$ becomes $2\mu/… | correct | X² − σ²t is a martingale for X = σW; sim: l14.s8 tests |
| l14-hitting-and-exit.json | screens[7].prose | The interviewer pushes the question one step: keep $\mu = 0.5$ and $\sigma = 1$, but move the barriers to $a … | correct | same formulas at a = 1, b = 2, μ = 0.5; sim: l14.s7 |
| l14-hitting-and-exit.json | screens[7].question | Give $P$ and $E[\tau]$ to 4 decimal places. | correct | same formulas at a = 1, b = 2, μ = 0.5; sim: l14.s7 |
| l14-hitting-and-exit.json | screens[7].widget.rows[0][1].answer | graded key 0.91 | correct | same formulas at a = 1, b = 2, μ = 0.5; sim: l14.s7 |
| l14-hitting-and-exit.json | screens[7].widget.rows[1][1].answer | graded key 1.4598 | correct | same formulas at a = 1, b = 2, μ = 0.5; sim: l14.s7 |
| l14-hitting-and-exit.json | screens[7].hints[0].text | $2\mu b = 2$ here, so $e^{2} = 7.3891$. | correct | same formulas at a = 1, b = 2, μ = 0.5; sim: l14.s7 |
| l14-hitting-and-exit.json | screens[7].hints[1].text | $P = (1 - 7.3891)/(0.3679$ ${}- 7.3891)$. | correct | same formulas at a = 1, b = 2, μ = 0.5; sim: l14.s7 |
| l14-hitting-and-exit.json | screens[7].hints[2].text | Then $aP - b(1 - P) = 0.9100$ ${}- 2 \times 0.0900$. | correct | same formulas at a = 1, b = 2, μ = 0.5; sim: l14.s7 |
| l14-hitting-and-exit.json | screens[7].feedback.correct | $P = 0.9100$ and $E[\tau] = (0.9100$ ${}- 2 \times 0.0900)/0.5$ ${}= 1.4598$ from unrounded values. | correct | same formulas at a = 1, b = 2, μ = 0.5; sim: l14.s7 |
| l14-hitting-and-exit.json | screens[7].feedback.generic | Not quite right. $P = (1 - e^{2})/(e^{-1}$ ${}- e^{2})$, then $E[\tau] = (aP - b(1 - P))/\mu$. | correct | same formulas at a = 1, b = 2, μ = 0.5; sim: l14.s7 |
| l14-hitting-and-exit.json | screens[7].feedback.byKey.r0c1 | $P = (1 - e)/(e^{-1} - e) = 0.7311$ is for $b = 1$. With $b = 2$ the exponent is $2\mu b = 2$, so $P = (1 - e… | correct | same formulas at a = 1, b = 2, μ = 0.5; sim: l14.s7 |
| l14-hitting-and-exit.json | screens[7].feedback.byKey.r1c1 | $E[\tau] = (aP - b(1 - P))/\mu$ with $b = 2$: $(0.9100 - 0.1800)/0.5 = 1.4598$ from unrounded values. | correct | same formulas at a = 1, b = 2, μ = 0.5; sim: l14.s7 |
| l14-hitting-and-exit.json | screens[7].explain.text | The lower barrier is twice as far, so the path reaches $+1$ first 91% of the time. It leaves sooner than $ab … | correct | same formulas at a = 1, b = 2, μ = 0.5; sim: l14.s7 |
| l14-hitting-and-exit.json | screens[8].prose | Last, simulate it. At step $\Delta t = 0.001$ a discrete path can step over a barrier and back, so the simula… | correct | solution run in CPython, 9/9, starter 0/9; discrete-monitoring bias, barrier shift 0.5826σ√Δt (Broadie, Glasserman and Kou 1997); sim: l14.s8 |
| l14-hitting-and-exit.json | screens[8].question | Complete the three functions. | correct | solution run in CPython, 9/9, starter 0/9; discrete-monitoring bias, barrier shift 0.5826σ√Δt (Broadie, Glasserman and Kou 1997); sim: l14.s8 |
| l14-hitting-and-exit.json | screens[8].widget.solution | code solution: method taught and hidden tests | correct | solution run in CPython, 9/9, starter 0/9; discrete-monitoring bias, barrier shift 0.5826σ√Δt (Broadie, Glasserman and Kou 1997); sim: l14.s8 |
| l14-hitting-and-exit.json | screens[8].widget.how | Submit runs 9 hidden tests. Six are exact cases, two are simulations with the stated draw order, and one chec… | correct | solution run in CPython, 9/9, starter 0/9; discrete-monitoring bias, barrier shift 0.5826σ√Δt (Broadie, Glasserman and Kou 1997); sim: l14.s8 |
| l14-hitting-and-exit.json | screens[8].hints[0].text | For no drift, return $b/(a + b)$ and $ab/\sigma^2$. | correct | solution run in CPython, 9/9, starter 0/9; discrete-monitoring bias, barrier shift 0.5826σ√Δt (Broadie, Glasserman and Kou 1997); sim: l14.s8 |
| l14-hitting-and-exit.json | screens[8].hints[1].text | Step all live paths together: draw one normal per live path. | correct | solution run in CPython, 9/9, starter 0/9; discrete-monitoring bias, barrier shift 0.5826σ√Δt (Broadie, Glasserman and Kou 1997); sim: l14.s8 |
| l14-hitting-and-exit.json | screens[8].hints[2].text | Mark a path done at the first step with $X \ge a$ or $X \le -b$. | correct | solution run in CPython, 9/9, starter 0/9; discrete-monitoring bias, barrier shift 0.5826σ√Δt (Broadie, Glasserman and Kou 1997); sim: l14.s8 |
| l14-hitting-and-exit.json | screens[8].feedback.correct | On seed 1: $P = 0.7464$ and $E[\tau] = 0.9454$ against 0.7311 and 0.9242, a gap of 0.021. | correct | solution run in CPython, 9/9, starter 0/9; discrete-monitoring bias, barrier shift 0.5826σ√Δt (Broadie, Glasserman and Kou 1997); sim: l14.s8 |
| l14-hitting-and-exit.json | screens[8].feedback.generic | Not quite right. Check the examples: the formula gives 0.7311 and the driftless exit time is 6. | correct | solution run in CPython, 9/9, starter 0/9; discrete-monitoring bias, barrier shift 0.5826σ√Δt (Broadie, Glasserman and Kou 1997); sim: l14.s8 |
| l14-hitting-and-exit.json | screens[8].explain.text | The simulation overshoots the formula because crossings between steps are missed, exactly as for the barrier … | correct | solution run in CPython, 9/9, starter 0/9; discrete-monitoring bias, barrier shift 0.5826σ√Δt (Broadie, Glasserman and Kou 1997); sim: l14.s8 |
| l14-hitting-and-exit.json | screens[9].prose | A trade's profit, in £ a share, moves like Brownian motion. Volatility is £1 a day and drift is £0.05 a day (… | correct | P = 0.4717 at k = 0.1; Sharpe 0.05√252 = 0.794 (252-day year); sim: l14.s9 |
| l14-hitting-and-exit.json | screens[9].question | What is the chance it reaches the take-profit first? Give 4 decimal places. | correct | P = 0.4717 at k = 0.1; Sharpe 0.05√252 = 0.794 (252-day year); sim: l14.s9 |
| l14-hitting-and-exit.json | screens[9].widget.answer | graded key 0.4717 | correct | P = 0.4717 at k = 0.1; Sharpe 0.05√252 = 0.794 (252-day year); sim: l14.s9 |
| l14-hitting-and-exit.json | screens[9].widget.accept | $k = 2\mu = 0.1$: $P = (1 - e^{0.15})/(e^{-0.2} - e^{0.15}) = 0.4717$, against $1.5/3.5 = 0.4286$ with no dri… | correct | P = 0.4717 at k = 0.1; Sharpe 0.05√252 = 0.794 (252-day year); sim: l14.s9 |
| l14-hitting-and-exit.json | screens[9].widget.wrong[0] | slip 0.4286: wrong under every valid reading of the item | correct | P = 0.4717 at k = 0.1; slip arithmetic recomputed |
| l14-hitting-and-exit.json | screens[9].widget.wrong[1] | slip 0.5: wrong under every valid reading of the item | correct | P = 0.4717 at k = 0.1; slip arithmetic recomputed |
| l14-hitting-and-exit.json | screens[9].widget.wrong[2] | slip 0.5714: wrong under every valid reading of the item | correct | P = 0.4717 at k = 0.1; slip arithmetic recomputed |
| l14-hitting-and-exit.json | screens[9].hints[0].text | $2\mu b = 0.15$ and $2\mu a = 0.2$. | correct | P = 0.4717 at k = 0.1; Sharpe 0.05√252 = 0.794 (252-day year); sim: l14.s9 |
| l14-hitting-and-exit.json | screens[9].hints[1].text | $e^{0.15} = 1.1618$ and $e^{-0.2} = 0.8187$. | correct | P = 0.4717 at k = 0.1; Sharpe 0.05√252 = 0.794 (252-day year); sim: l14.s9 |
| l14-hitting-and-exit.json | screens[9].feedback.correct | $P = 0.4717$: a drift of only £0.05 a day lifts the chance by about four points. | correct | P = 0.4717 at k = 0.1; Sharpe 0.05√252 = 0.794 (252-day year); sim: l14.s9 |
| l14-hitting-and-exit.json | screens[9].feedback.generic | Not quite right. Use $P = (1$ ${}- e^{2\mu b})/(e^{-2\mu a}$ ${}- e^{2\mu b})$ with $\mu = 0.05$, $a = 2$ and… | correct | P = 0.4717 at k = 0.1; Sharpe 0.05√252 = 0.794 (252-day year); sim: l14.s9 |
| l14-hitting-and-exit.json | screens[9].feedback.byKey.no-drift | You used $b/(a + b) = 0.4286$. The small drift matters: it moves $P$ by more than four points. | correct | P = 0.4717 at k = 0.1; Sharpe 0.05√252 = 0.794 (252-day year); sim: l14.s9 |
| l14-hitting-and-exit.json | screens[9].feedback.byKey.half | You called it a coin flip. The barriers are unequal and there is a drift. | correct | P = 0.4717 at k = 0.1; Sharpe 0.05√252 = 0.794 (252-day year); sim: l14.s9 |
| l14-hitting-and-exit.json | screens[9].feedback.byKey.swapped | You used $a/(a + b) = 0.5714$, the far distance over the total. That is the chance of the stop-loss first. | correct | P = 0.4717 at k = 0.1; Sharpe 0.05√252 = 0.794 (252-day year); sim: l14.s9 |
| l14-hitting-and-exit.json | screens[9].explain.text | Expected profit per trade is $2P - 1.5(1 - P)$ ${}= \text{£}0.1509$, from a drift of £0.05 a day. The edge is… | correct | P = 0.4717 at k = 0.1; Sharpe 0.05√252 = 0.794 (252-day year); sim: l14.s9 |
| l14-hitting-and-exit.json | summary.ideas[0] | Stopping the martingale $W$ at $(-b, a)$ gives $P = b/(a + b)$, and stopping $W^2 - t$ gives $E[\tau] = ab$. | correct | KS Prob. 2.8.13 and 5.5.B; Shreve Thm 3.7.1; sim: l14.s1, l14.s3 |
| l14-hitting-and-exit.json | summary.ideas[1] | With drift, stop $e^{-2\mu X_t}$ for $P$ and use Wald, $E[X_\tau] = \mu E[\tau]$, for $E[\tau]$. Volatility d… | correct | KS Prob. 2.8.13 and 5.5.B; Shreve Thm 3.7.1; sim: l14.s1, l14.s3 |
| l14-hitting-and-exit.json | summary.ideas[2] | A single barrier is reached with probability 1 when there is no drift. The mean wait is infinite, so the rule… | correct | KS Prob. 2.8.13 and 5.5.B; Shreve Thm 3.7.1; sim: l14.s1, l14.s3 |
| l14-hitting-and-exit.json | summary.formula.name | Exit of Brownian motion | correct | KS Prob. 2.8.13 and 5.5.B; Shreve Thm 3.7.1; sim: l14.s1, l14.s3 |
| l14-hitting-and-exit.json | summary.formula.note | Driftless, unit volatility. Distances are measured to the barriers $a$ and $-b$. | correct | KS Prob. 2.8.13 and 5.5.B; Shreve Thm 3.7.1; sim: l14.s1, l14.s3 |
| l14-hitting-and-exit.json | summary.trap | Not one half, and not $a + b$. The nearer barrier wins more often, and the time is the product of the distanc… | correct | KS Prob. 2.8.13 and 5.5.B; Shreve Thm 3.7.1; sim: l14.s1, l14.s3 |
| l14-hitting-and-exit.json | quiz[0].question | Driftless Brownian motion stops at $+4$ or $-1$. What is the chance it reaches $+4$ first? | correct | P = b/(a+b) = 1/5 |
| l14-hitting-and-exit.json | quiz[0].widget.answer | graded key 0.2 | correct | P = b/(a+b) = 1/5 |
| l14-hitting-and-exit.json | quiz[0].widget.accept | $P = b/(a + b) = 1/5 = 0.2$: the far barrier is $+4$, so it is rarely reached first. | correct | P = b/(a+b) = 1/5 |
| l14-hitting-and-exit.json | quiz[0].widget.wrong[0] | slip 0.8: wrong under every valid reading of the item | correct | P = b/(a+b) = 1/5; slip arithmetic recomputed |
| l14-hitting-and-exit.json | quiz[0].widget.wrong[1] | slip 0.5: wrong under every valid reading of the item | correct | P = b/(a+b) = 1/5; slip arithmetic recomputed |
| l14-hitting-and-exit.json | quiz[0].feedback.correct | $1/5 = 0.2$. | correct | P = b/(a+b) = 1/5 |
| l14-hitting-and-exit.json | quiz[0].feedback.generic | Not quite right. $P$(reach $a$ first) is the distance to the other barrier over the total. | correct | P = b/(a+b) = 1/5 |
| l14-hitting-and-exit.json | quiz[0].feedback.byKey.swapped | You gave $a/(a + b) = 0.8$. That is the chance of reaching $-1$ first. | correct | P = b/(a+b) = 1/5 |
| l14-hitting-and-exit.json | quiz[0].feedback.byKey.half | You assumed a fair coin. The distances differ, so the chances do too. | correct | P = b/(a+b) = 1/5 |
| l14-hitting-and-exit.json | quiz[0].explain.text | The nearer barrier $-1$ takes 80% of the paths. The chance of reaching $+4$ first is $1/(1 + 4) = 0.2$. | correct | P = b/(a+b) = 1/5 |
| l14-hitting-and-exit.json | quiz[1].question | Volatility is $\sigma = 2$ and there is no drift. The path stops at $\pm1$. What is $E[\tau]$? | correct | E[τ] = ab/σ² |
| l14-hitting-and-exit.json | quiz[1].widget.answer | graded key 0.25 | correct | E[τ] = ab/σ² |
| l14-hitting-and-exit.json | quiz[1].widget.accept | $E[\tau] = ab/\sigma^2 = 1/4$. | correct | E[τ] = ab/σ² |
| l14-hitting-and-exit.json | quiz[1].widget.wrong[0] | slip 1: wrong under every valid reading of the item | correct | E[τ] = ab/σ²; slip arithmetic recomputed |
| l14-hitting-and-exit.json | quiz[1].widget.wrong[1] | slip 0.5: wrong under every valid reading of the item | correct | E[τ] = ab/σ²; slip arithmetic recomputed |
| l14-hitting-and-exit.json | quiz[1].widget.wrong[2] | slip 4: wrong under every valid reading of the item | correct | E[τ] = ab/σ²; slip arithmetic recomputed |
| l14-hitting-and-exit.json | quiz[1].feedback.correct | $1/4$. | correct | E[τ] = ab/σ² |
| l14-hitting-and-exit.json | quiz[1].feedback.generic | Not quite right. $E[\tau] = ab/\sigma^2$ with $a = b = 1$ and $\sigma^2 = 4$. | correct | E[τ] = ab/σ² |
| l14-hitting-and-exit.json | quiz[1].feedback.byKey.none | You gave $ab = 1$, with no volatility. A larger $\sigma$ shortens the time. | correct | E[τ] = ab/σ² |
| l14-hitting-and-exit.json | quiz[1].feedback.byKey.unsquared | You divided by $\sigma = 2$ instead of $\sigma^2 = 4$. | correct | E[τ] = ab/σ² |
| l14-hitting-and-exit.json | quiz[1].feedback.byKey.times | You multiplied by $\sigma^2$. Higher volatility makes the exit faster, not slower. | correct | E[τ] = ab/σ² |
| l14-hitting-and-exit.json | quiz[1].explain.text | $X_t^2 - \sigma^2t$ is a martingale and $X_\tau^2 = 1$, so $E[\tau] = 1/\sigma^2 = 0.25$. | correct | E[τ] = ab/σ² |
| l14-hitting-and-exit.json | quiz[2].question | A price has drift $-0.5$ and volatility 2. What is the chance it ever reaches $+1$ (no lower barrier)? | imprecise | start point not stated; the key needs X₀ = 0. Finding 4 |
| l14-hitting-and-exit.json | quiz[2].widget.answer | graded key 0.7788 | correct | P(sup X ≥ a) = e^{−2∣μ∣a/σ²} for negative drift (KS 3.5.C; Shreve Ex. 3.7); sim: l14.quiz2 |
| l14-hitting-and-exit.json | quiz[2].widget.accept | The chance is $e^{-2∣\mu∣a/\sigma^2} = e^{-2 \times 0.5/4} = e^{-0.25} = 0.7788$. | correct | P(sup X ≥ a) = e^{−2∣μ∣a/σ²} for negative drift (KS 3.5.C; Shreve Ex. 3.7); sim: l14.quiz2 |
| l14-hitting-and-exit.json | quiz[2].widget.wrong[0] | slip 0.3679: wrong under every valid reading of the item | correct | P(sup X ≥ a) = e^{−2∣μ∣a/σ²} for negative drift (KS 3.5.C; slip arithmetic recomputed |
| l14-hitting-and-exit.json | quiz[2].widget.wrong[1] | slip 0.6065: wrong under every valid reading of the item | correct | P(sup X ≥ a) = e^{−2∣μ∣a/σ²} for negative drift (KS 3.5.C; slip arithmetic recomputed |
| l14-hitting-and-exit.json | quiz[2].feedback.correct | $e^{-0.25} = 0.7788$. | correct | P(sup X ≥ a) = e^{−2∣μ∣a/σ²} for negative drift (KS 3.5.C; Shreve Ex. 3.7); sim: l14.quiz2 |
| l14-hitting-and-exit.json | quiz[2].feedback.generic | Not quite right. The exponent is $2\mu a/\sigma^2$ in size. | correct | P(sup X ≥ a) = e^{−2∣μ∣a/σ²} for negative drift (KS 3.5.C; Shreve Ex. 3.7); sim: l14.quiz2 |
| l14-hitting-and-exit.json | quiz[2].feedback.byKey.no-sigma | You used $e^{-2\mu a} = e^{-1}$. Volatility 2 makes escape likelier and divides the exponent by $\sigma^2 = 4… | correct | P(sup X ≥ a) = e^{−2∣μ∣a/σ²} for negative drift (KS 3.5.C; Shreve Ex. 3.7); sim: l14.quiz2 |
| l14-hitting-and-exit.json | quiz[2].feedback.byKey.unsquared | You divided by $\sigma = 2$ rather than $\sigma^2 = 4$. | correct | P(sup X ≥ a) = e^{−2∣μ∣a/σ²} for negative drift (KS 3.5.C; Shreve Ex. 3.7); sim: l14.quiz2 |
| l14-hitting-and-exit.json | quiz[2].explain.text | Letting $b \to \infty$ in the exit formula gives $e^{-2∣\mu∣a/\sigma^2}$. High volatility means noise can bea… | correct | P(sup X ≥ a) = e^{−2∣μ∣a/σ²} for negative drift (KS 3.5.C; Shreve Ex. 3.7); sim: l14.quiz2 |
| l14-hitting-and-exit.json | quiz[3].question | Driftless Brownian motion has only an upper barrier at $+1$. What is $E[\tau]$? | correct | E[τ_a] = ∞ (Shreve Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | quiz[3].widget.options[0].text | infinite, because the mean wait diverges | correct | E[τ_a] = ∞ (Shreve Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | quiz[3].widget.options[1].text | zero, because $ab = 0$ when $b = 0$ (no lower barrier) | correct | E[τ_a] = ∞ (Shreve Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | quiz[3].widget.options[1].why | You let $b$ shrink to 0. With no lower barrier $b$ is infinite, and $ab$ grows. | correct | E[τ_a] = ∞ (Shreve Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | quiz[3].widget.options[2].text | one, the distance squared, $a^2 = 1$ | correct | E[τ_a] = ∞ (Shreve Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | quiz[3].widget.options[2].why | You squared the distance. That needs a second barrier to bound the path. | correct | E[τ_a] = ∞ (Shreve Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | quiz[3].widget.options[3].text | one half, the same as a coin flip | correct | E[τ_a] = ∞ (Shreve Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | quiz[3].widget.options[3].why | You used coin odds for the time. Time and chance are different questions. | correct | E[τ_a] = ∞ (Shreve Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | quiz[3].feedback.correct | It is infinite: $E[\tau] = ab \to \infty$ as $b \to \infty$. | correct | E[τ_a] = ∞ (Shreve Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | quiz[3].feedback.generic | Not quite right. Let the lower barrier move away in $E[\tau] = ab$. | correct | E[τ_a] = ∞ (Shreve Rem. 3.6.4); sim: l14.s3 |
| l14-hitting-and-exit.json | quiz[3].explain.text | The hit is certain, but a few paths wander far below first, and they push the mean time to infinity. | correct | E[τ_a] = ∞ (Shreve Rem. 3.6.4); sim: l14.s3 |

## l15-moments-quickly.json

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l15-moments-quickly.json | screens[0].prose | A standard normal $Z$ has $E[e^{sZ}] = e^{s^2/2}$. Expand both sides in powers of $s$: on the left the coeffi… | correct | E[Z^{2k}] = (2k−1)!! from the mgf e^{s²/2} (C&B Ex. 2.3.9); sim: l15.s0 |
| l15-moments-quickly.json | screens[0].question | Read off $E[Z^4]$ and $E[Z^6]$. Fill in the last column. | correct | E[Z^{2k}] = (2k−1)!! from the mgf e^{s²/2} (C&B Ex. 2.3.9); sim: l15.s0 |
| l15-moments-quickly.json | screens[0].widget.rows[1][2].answer | graded key 3 | correct | E[Z^{2k}] = (2k−1)!! from the mgf e^{s²/2} (C&B Ex. 2.3.9); sim: l15.s0 |
| l15-moments-quickly.json | screens[0].widget.rows[2][2].answer | graded key 15 | correct | E[Z^{2k}] = (2k−1)!! from the mgf e^{s²/2} (C&B Ex. 2.3.9); sim: l15.s0 |
| l15-moments-quickly.json | screens[0].hints[0].text | The coefficient of $s^4$ on the left is $E[Z^4]/4!$. | correct | E[Z^{2k}] = (2k−1)!! from the mgf e^{s²/2} (C&B Ex. 2.3.9); sim: l15.s0 |
| l15-moments-quickly.json | screens[0].hints[1].text | Match it with $\tfrac18$ and solve. | correct | E[Z^{2k}] = (2k−1)!! from the mgf e^{s²/2} (C&B Ex. 2.3.9); sim: l15.s0 |
| l15-moments-quickly.json | screens[0].hints[2].text | $E[Z^4] = 24 \times \tfrac18$. | correct | E[Z^{2k}] = (2k−1)!! from the mgf e^{s²/2} (C&B Ex. 2.3.9); sim: l15.s0 |
| l15-moments-quickly.json | screens[0].feedback.correct | $E[Z^4] = 24/8 = 3$ and $E[Z^6] = 720/48 = 15$. | correct | E[Z^{2k}] = (2k−1)!! from the mgf e^{s²/2} (C&B Ex. 2.3.9); sim: l15.s0 |
| l15-moments-quickly.json | screens[0].feedback.generic | Not quite right. Multiply each coefficient by $k!$: $4! = 24$ and $6! = 720$. | correct | E[Z^{2k}] = (2k−1)!! from the mgf e^{s²/2} (C&B Ex. 2.3.9); sim: l15.s0 |
| l15-moments-quickly.json | screens[0].feedback.byKey.r1c2 | $E[Z^4] = 4! \times \tfrac18$ ${}= 3$. The value 1 would be the variance squared. | correct | E[Z^{2k}] = (2k−1)!! from the mgf e^{s²/2} (C&B Ex. 2.3.9); sim: l15.s0 |
| l15-moments-quickly.json | screens[0].feedback.byKey.r2c2 | $E[Z^6]$ ${}= 6! \times \tfrac1{48} = 15$. Check that you used $720$, not $120$. | correct | E[Z^{2k}] = (2k−1)!! from the mgf e^{s²/2} (C&B Ex. 2.3.9); sim: l15.s0 |
| l15-moments-quickly.json | screens[0].explain.text | The fourth moment is $3$ and the sixth is $15$: $1 \times 3 \times 5$. For $W_t$ scale by $t^{k/2}$, so $E[W_… | correct | E[Z^{2k}] = (2k−1)!! from the mgf e^{s²/2} (C&B Ex. 2.3.9); sim: l15.s0 |
| l15-moments-quickly.json | screens[1].prose | Two times at once. To find $E[W_1^2W_2^2]$, split $W_2 = W_1 + D$ with $D = W_2 - W_1$. Each line carries its… | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].question | Put the lines in order. | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].widget.lines[0].text | $D$ is independent of $W_1$, with $E[D] = 0$ and $E[D^2] = 1$ (independent increments). | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].widget.lines[1].text | Expand: $W_1^2W_2^2 = W_1^4 + 2W_1^3D$ ${}+ W_1^2D^2$. | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].widget.lines[2].text | Independence: $E[W_1^3D] = E[W_1^3]E[D] = 0$ and $E[W_1^2D^2] = E[W_1^2]E[D^2]$ ${}= 1$. | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].widget.lines[3].text | Normal moment: $E[W_1^4] = 3$. | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].widget.lines[4].text | Add: $E[W_1^2W_2^2] = 3 + 0 + 1 = 4$. | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].widget.lines[5].text | Treat $W_1$ and $W_2$ as independent: $E[W_1^2]E[W_2^2] = 1 \times 2$ ${}= 2$. | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].widget.lines[5].why | $W_2$ contains $W_1$, so they are correlated: $\text{Cov}(W_1, W_2) = 1$. | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].widget.lines[6].text | Drop $W_1^2D^2$ because $E[D] = 0$. | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].widget.lines[6].why | $E[D] = 0$ kills only odd powers of $D$. The square $D^2$ has mean 1. | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].hints[0].text | Write $W_2$ as $W_1$ plus a fresh increment. | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].hints[1].text | After expanding there are three terms. | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].feedback.correct | $E[W_1^2W_2^2] = 4$, not 2: the shared $W_1$ adds 2. | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].feedback.generic | Not quite right. Split $W_2$, expand, then use independence term by term. | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].feedback.byKey.x1 | You treated the two times as independent. They share the increment from 0 to 1. | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].feedback.byKey.x2 | You dropped a term because the mean of $D$ is 0. A square has a positive mean. | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].feedback.byKey.left-out | A line of the working is in the Left out list. Only the two flawed lines belong there. | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[1].explain.text | Split at the earlier time, so every extra factor is independent of what came before. The cross term has mean … | correct | independent increments (Shreve Def. 3.3.1); sim: l15.s1 |
| l15-moments-quickly.json | screens[2].prose | Drill, two minutes. The integral $\int_0^2 s\,dW_s$ has mean 0. Its variance is the area under $f(s)^2 = s^2$… | correct | Itô isometry, deterministic integrand (Shreve Thm 4.4.9); sim: l15.s2/s8 |
| l15-moments-quickly.json | screens[2].question | What is $\text{Var}\big(\int_0^2 s\,dW_s\big)$? Give 4 decimal places. | correct | Itô isometry, deterministic integrand (Shreve Thm 4.4.9); sim: l15.s2/s8 |
| l15-moments-quickly.json | screens[2].widget.answer | graded key 2.6667 | correct | Itô isometry, deterministic integrand (Shreve Thm 4.4.9); sim: l15.s2/s8 |
| l15-moments-quickly.json | screens[2].widget.accept | $\int_0^2 s^2\,ds = 8/3 = 2.6667$. | correct | Itô isometry, deterministic integrand (Shreve Thm 4.4.9); sim: l15.s2/s8 |
| l15-moments-quickly.json | screens[2].widget.wrong[0] | slip 4: wrong under every valid reading of the item | correct | Itô isometry, deterministic integrand (Shreve Thm 4.4.9); slip arithmetic recomputed |
| l15-moments-quickly.json | screens[2].widget.wrong[1] | slip 2: wrong under every valid reading of the item | correct | Itô isometry, deterministic integrand (Shreve Thm 4.4.9); slip arithmetic recomputed |
| l15-moments-quickly.json | screens[2].hints[0].text | Variance is an integral of the squared integrand. | correct | Itô isometry, deterministic integrand (Shreve Thm 4.4.9); sim: l15.s2/s8 |
| l15-moments-quickly.json | screens[2].hints[1].text | $\int_0^2 s^2\,ds = [s^3/3]_0^2$. | correct | Itô isometry, deterministic integrand (Shreve Thm 4.4.9); sim: l15.s2/s8 |
| l15-moments-quickly.json | screens[2].feedback.correct | $\int_0^2 s^2\,ds = 8/3$ ${}= 2.6667$. | correct | Itô isometry, deterministic integrand (Shreve Thm 4.4.9); sim: l15.s2/s8 |
| l15-moments-quickly.json | screens[2].feedback.generic | Not quite right. Integrate the square of the integrand: $s^2$ from 0 to 2. | correct | Itô isometry, deterministic integrand (Shreve Thm 4.4.9); sim: l15.s2/s8 |
| l15-moments-quickly.json | screens[2].feedback.byKey.square-outside | You squared the integral, $(\int_0^2 s\,ds)^2 = 4$. The isometry integrates the square instead. | correct | Itô isometry, deterministic integrand (Shreve Thm 4.4.9); sim: l15.s2/s8 |
| l15-moments-quickly.json | screens[2].feedback.byKey.no-square | You integrated $s$, not $s^2$. That gives $\int_0^2 s\,ds = 2$. | correct | Itô isometry, deterministic integrand (Shreve Thm 4.4.9); sim: l15.s2/s8 |
| l15-moments-quickly.json | screens[2].explain.text | The isometry says $\text{Var}\int f\,dW$ ${}= \int f^2\,dt$: squares go inside, the sum of variances of indep… | correct | Itô isometry, deterministic integrand (Shreve Thm 4.4.9); sim: l15.s2/s8 |
| l15-moments-quickly.json | screens[3].prose | Careful. $\int_0^{2.5} W_t\,dt$ is a $dt$ integral, so the isometry does not apply to it directly. By parts i… | correct | ∫₀ᵀW dt = ∫₀ᵀ(T−t) dW by parts, variance T³/3 (Shreve Ex. 4.7.1 area under BM); sim: l15.s3 |
| l15-moments-quickly.json | screens[3].question | What is $\text{Var}\big(\int_0^{2.5} W_t\,dt\big)$? Give 4 decimal places. | correct | ∫₀ᵀW dt = ∫₀ᵀ(T−t) dW by parts, variance T³/3 (Shreve Ex. 4.7.1 area under BM); sim: l15.s3 |
| l15-moments-quickly.json | screens[3].widget.answer | graded key 5.2083 | correct | ∫₀ᵀW dt = ∫₀ᵀ(T−t) dW by parts, variance T³/3 (Shreve Ex. 4.7.1 area under BM); sim: l15.s3 |
| l15-moments-quickly.json | screens[3].widget.accept | $\int_0^{2.5} (2.5 - t)^2\,dt = 2.5^3/3 = 5.2083$. | correct | ∫₀ᵀW dt = ∫₀ᵀ(T−t) dW by parts, variance T³/3 (Shreve Ex. 4.7.1 area under BM); sim: l15.s3 |
| l15-moments-quickly.json | screens[3].widget.wrong[0] | slip 3.125: wrong under every valid reading of the item | correct | ∫₀ᵀW dt = ∫₀ᵀ(T−t) dW by parts, variance T³/3 (Shreve Ex. 4.7.1 area under BM); slip arithmetic recomputed |
| l15-moments-quickly.json | screens[3].widget.wrong[1] | slip 2.5: wrong under every valid reading of the item | correct | ∫₀ᵀW dt = ∫₀ᵀ(T−t) dW by parts, variance T³/3 (Shreve Ex. 4.7.1 area under BM); slip arithmetic recomputed |
| l15-moments-quickly.json | screens[3].hints[0].text | Integrate by parts: $\int_0^{2.5} W_t\,dt = 2.5\,W_{2.5}$ ${}- \int_0^{2.5} t\,dW_t$. | correct | ∫₀ᵀW dt = ∫₀ᵀ(T−t) dW by parts, variance T³/3 (Shreve Ex. 4.7.1 area under BM); sim: l15.s3 |
| l15-moments-quickly.json | screens[3].hints[1].text | Combine: $\int_0^{2.5} (2.5 - t)\,dW_t$. | correct | ∫₀ᵀW dt = ∫₀ᵀ(T−t) dW by parts, variance T³/3 (Shreve Ex. 4.7.1 area under BM); sim: l15.s3 |
| l15-moments-quickly.json | screens[3].hints[2].text | Variance: $\int_0^{2.5} (2.5 - t)^2\,dt$. | correct | ∫₀ᵀW dt = ∫₀ᵀ(T−t) dW by parts, variance T³/3 (Shreve Ex. 4.7.1 area under BM); sim: l15.s3 |
| l15-moments-quickly.json | screens[3].feedback.correct | $\int_0^{2.5} (2.5 - t)^2\,dt = 2.5^3/3 = 5.2083$, so the integral has variance 5.2083. | correct | ∫₀ᵀW dt = ∫₀ᵀ(T−t) dW by parts, variance T³/3 (Shreve Ex. 4.7.1 area under BM); sim: l15.s3 |
| l15-moments-quickly.json | screens[3].feedback.generic | Not quite right. Convert to a $dW$ integral first: $\int_0^{2.5} W_t\,dt$ ${}= \int_0^{2.5} (2.5 - t)\,dW_t$. | correct | ∫₀ᵀW dt = ∫₀ᵀ(T−t) dW by parts, variance T³/3 (Shreve Ex. 4.7.1 area under BM); sim: l15.s3 |
| l15-moments-quickly.json | screens[3].feedback.byKey.isometry-dt | You applied the isometry to $\int W_t\,dt$ directly, getting $\int_0^{2.5} t\,dt = 3.125$. A $dt$ integral ne… | correct | ∫₀ᵀW dt = ∫₀ᵀ(T−t) dW by parts, variance T³/3 (Shreve Ex. 4.7.1 area under BM); sim: l15.s3 |
| l15-moments-quickly.json | screens[3].feedback.byKey.whole | You took $\int_0^{2.5} W_t\,dt \approx W_{2.5}$, variance 2.5. The integral sums the whole path, so it spread… | correct | ∫₀ᵀW dt = ∫₀ᵀ(T−t) dW by parts, variance T³/3 (Shreve Ex. 4.7.1 area under BM); sim: l15.s3 |
| l15-moments-quickly.json | screens[3].explain.text | Early increments of $W$ count for more, because they stay in the path for longer: weight $2.5 - t$. The varia… | correct | ∫₀ᵀW dt = ∫₀ᵀ(T−t) dW by parts, variance T³/3 (Shreve Ex. 4.7.1 area under BM); sim: l15.s3 |
| l15-moments-quickly.json | screens[4].prose | Covariance of Brownian motion is $\text{Cov}(W_s, W_t)$ ${}= \min(s, t)$, because the overlap is the shared i… | correct | Cov(W_s, W_t) = min(s,t) (Shreve 3.3.2); sim: l15.s4/s8 |
| l15-moments-quickly.json | screens[4].question | What is $\text{Var}(W_2 + W_3)$? | correct | Cov(W_s, W_t) = min(s,t) (Shreve 3.3.2); sim: l15.s4/s8 |
| l15-moments-quickly.json | screens[4].widget.answer | graded key 9 | correct | Cov(W_s, W_t) = min(s,t) (Shreve 3.3.2); sim: l15.s4/s8 |
| l15-moments-quickly.json | screens[4].widget.accept | $2 + 3 + 2\,\text{Cov}(W_2, W_3) = 5 + 2 \times 2 = 9$. | correct | Cov(W_s, W_t) = min(s,t) (Shreve 3.3.2); sim: l15.s4/s8 |
| l15-moments-quickly.json | screens[4].widget.wrong[0] | slip 5: wrong under every valid reading of the item | correct | Cov(W_s, W_t) = min(s,t) (Shreve 3.3.2); slip arithmetic recomputed |
| l15-moments-quickly.json | screens[4].widget.wrong[1] | slip 11: wrong under every valid reading of the item | correct | Cov(W_s, W_t) = min(s,t) (Shreve 3.3.2); slip arithmetic recomputed |
| l15-moments-quickly.json | screens[4].hints[0].text | $\text{Var}(X + Y)$ ${}= \text{Var}X + \text{Var}Y$ ${}+ 2\,\text{Cov}(X, Y)$. | correct | Cov(W_s, W_t) = min(s,t) (Shreve 3.3.2); sim: l15.s4/s8 |
| l15-moments-quickly.json | screens[4].hints[1].text | $\text{Cov}(W_2, W_3)$ ${}= \min(2, 3) = 2$. | correct | Cov(W_s, W_t) = min(s,t) (Shreve 3.3.2); sim: l15.s4/s8 |
| l15-moments-quickly.json | screens[4].feedback.correct | $\text{Var}(W_2 + W_3) = 2 + 3$ ${}+ 2 \times 2 = 9$. | correct | Cov(W_s, W_t) = min(s,t) (Shreve 3.3.2); sim: l15.s4/s8 |
| l15-moments-quickly.json | screens[4].feedback.generic | Not quite right. Add the two variances and twice the covariance, which is $\min(2, 3)$. | correct | Cov(W_s, W_t) = min(s,t) (Shreve 3.3.2); sim: l15.s4/s8 |
| l15-moments-quickly.json | screens[4].feedback.byKey.no-cov | You added the variances only, $2 + 3 = 5$. The two times share the first 2 units of increments. | correct | Cov(W_s, W_t) = min(s,t) (Shreve 3.3.2); sim: l15.s4/s8 |
| l15-moments-quickly.json | screens[4].explain.text | Write $W_2 + W_3 = 2W_2 + (W_3 - W_2)$: variance $4 \times 2 + 1 = 9$. Both routes agree. | correct | Cov(W_s, W_t) = min(s,t) (Shreve 3.3.2); sim: l15.s4/s8 |
| l15-moments-quickly.json | screens[5].prose | Edge case. Odd moments of one time vanish by symmetry: $E[W_2^3] = 0$. A product across two times can still b… | wrong | W₁W₂³ has total power 4; every odd total power has mean 0 by W → −W. sim: l15.s5 prose EXPECTED_FAIL. Finding 5 |
| l15-moments-quickly.json | screens[5].question | What is $E[W_1W_2^3]$? | correct | E[W₁W₂³] = 3 + 3 = 6; Isserlis: 3·Cov·Var = 3·1·2; sim: l15.s5 |
| l15-moments-quickly.json | screens[5].widget.answer | graded key 6 | correct | E[W₁W₂³] = 3 + 3 = 6; Isserlis: 3·Cov·Var = 3·1·2; sim: l15.s5 |
| l15-moments-quickly.json | screens[5].widget.accept | $W_1(W_1 + D)^3$ gives $E[W_1^4] + 3E[W_1^2]E[D^2] = 3 + 3 = 6$; the other terms have mean 0. | correct | E[W₁W₂³] = 3 + 3 = 6; Isserlis: 3·Cov·Var = 3·1·2; sim: l15.s5 |
| l15-moments-quickly.json | screens[5].widget.wrong[0] | slip 0: wrong under every valid reading of the item | correct | E[W₁W₂³] = 3 + 3 = 6; slip arithmetic recomputed |
| l15-moments-quickly.json | screens[5].widget.wrong[1] | slip 3: wrong under every valid reading of the item | correct | E[W₁W₂³] = 3 + 3 = 6; slip arithmetic recomputed |
| l15-moments-quickly.json | screens[5].hints[0].text | Expand $(W_1 + D)^3 = W_1^3 + 3W_1^2D$ ${}+ 3W_1D^2 + D^3$. | correct | E[W₁W₂³] = 3 + 3 = 6; Isserlis: 3·Cov·Var = 3·1·2; sim: l15.s5 |
| l15-moments-quickly.json | screens[5].hints[1].text | Multiply by $W_1$ and take means term by term. | correct | E[W₁W₂³] = 3 + 3 = 6; Isserlis: 3·Cov·Var = 3·1·2; sim: l15.s5 |
| l15-moments-quickly.json | screens[5].feedback.correct | $E[W_1W_2^3] = 3 + 3 = 6$. | correct | E[W₁W₂³] = 3 + 3 = 6; Isserlis: 3·Cov·Var = 3·1·2; sim: l15.s5 |
| l15-moments-quickly.json | screens[5].feedback.generic | Not quite right. Expand $W_1(W_1 + D)^3$ and use independence of $D$. | correct | E[W₁W₂³] = 3 + 3 = 6; Isserlis: 3·Cov·Var = 3·1·2; sim: l15.s5 |
| l15-moments-quickly.json | screens[5].feedback.byKey.odd-zero | You called it odd, so zero. The total power is 4, and $W_1$ is correlated with $W_2$. | correct | E[W₁W₂³] = 3 + 3 = 6; Isserlis: 3·Cov·Var = 3·1·2; sim: l15.s5 |
| l15-moments-quickly.json | screens[5].feedback.byKey.one-term | You kept $E[W_1^4] = 3$ only. The term $3W_1^2D^2$ adds another 3. | correct | E[W₁W₂³] = 3 + 3 = 6; Isserlis: 3·Cov·Var = 3·1·2; sim: l15.s5 |
| l15-moments-quickly.json | screens[5].explain.text | The surviving terms are $W_1^4$ and $3W_1^2D^2$, with means 3 and 3. Zero by symmetry applies only to a singl… | wrong | symmetry also gives E[W₁W₂²] = E[W₁²W₂] = 0, not only single odd powers. sim: l15.s5 explain. Finding 5 |
| l15-moments-quickly.json | screens[6].prose | The interviewer pushes the question one step: take general times $s < t$. Split $W_t = W_s + D$ with $E[D^2] … | correct | E[W_s²W_t²] = 3s² + s(t−s); Isserlis: st + 2s²; sim: l15.s6 |
| l15-moments-quickly.json | screens[6].question | Give $E[W_s^2W_t^2]$ in terms of $s$ and $t$. | correct | E[W_s²W_t²] = 3s² + s(t−s); Isserlis: st + 2s²; sim: l15.s6 |
| l15-moments-quickly.json | screens[6].widget.answer | graded key 2s^2+st | correct | E[W_s²W_t²] = 3s² + s(t−s); Isserlis: st + 2s²; sim: l15.s6 |
| l15-moments-quickly.json | screens[6].widget.wrong[0] | slip st: wrong under every valid reading of the item | correct | E[W_s²W_t²] = 3s² + s(t−s); slip arithmetic recomputed |
| l15-moments-quickly.json | screens[6].widget.wrong[1] | slip s^2+st: wrong under every valid reading of the item | correct | E[W_s²W_t²] = 3s² + s(t−s); slip arithmetic recomputed |
| l15-moments-quickly.json | screens[6].hints[0].text | $W_s^2(W_s + D)^2 = W_s^4$ ${}+ 2W_s^3D + W_s^2D^2$. | correct | E[W_s²W_t²] = 3s² + s(t−s); Isserlis: st + 2s²; sim: l15.s6 |
| l15-moments-quickly.json | screens[6].hints[1].text | Means: $3s^2$, $0$ and $s(t - s)$. | correct | E[W_s²W_t²] = 3s² + s(t−s); Isserlis: st + 2s²; sim: l15.s6 |
| l15-moments-quickly.json | screens[6].feedback.correct | $E[W_s^2W_t^2] = 3s^2 + s(t$ ${}- s) = 2s^2 + st$. At $s = 1$, $t = 2$ it gives 4. | correct | E[W_s²W_t²] = 3s² + s(t−s); Isserlis: st + 2s²; sim: l15.s6 |
| l15-moments-quickly.json | screens[6].feedback.generic | Not quite right. Expand $W_s^2(W_s + D)^2$ and use $E[W_s^4] = 3s^2$, $E[D^2] = t - s$. | correct | E[W_s²W_t²] = 3s² + s(t−s); Isserlis: st + 2s²; sim: l15.s6 |
| l15-moments-quickly.json | screens[6].feedback.byKey.independent | You multiplied the variances, $st$. That treats the two times as independent, which they are not. | correct | E[W_s²W_t²] = 3s² + s(t−s); Isserlis: st + 2s²; sim: l15.s6 |
| l15-moments-quickly.json | screens[6].feedback.byKey.drop-cross | You gave $s^2 + st$, missing one $s^2$. That follows from $E[W_s^4] = 2s^2$; the fourth moment of a normal is… | correct | E[W_s²W_t²] = 3s² + s(t−s); Isserlis: st + 2s²; sim: l15.s6 |
| l15-moments-quickly.json | screens[6].explain.text | The sum is $3s^2 + st - s^2 = 2s^2 + st$. Check: $s = 1$, $t = 2$ gives $2 + 2 = 4$, the value from the first… | correct | E[W_s²W_t²] = 3s² + s(t−s); Isserlis: st + 2s²; sim: l15.s6 |
| l15-moments-quickly.json | screens[7].prose | Check the formulas by machine. `bm_moment` gives the exact moment, `isometry_var` integrates $f^2$ by the mid… | correct | solution run in CPython, 10/10, starter 0/10; sim: l15.s7 |
| l15-moments-quickly.json | screens[7].question | Complete the three functions. | correct | solution run in CPython, 10/10, starter 0/10; sim: l15.s7 |
| l15-moments-quickly.json | screens[7].widget.solution | code solution: method taught and hidden tests | correct | solution run in CPython, 10/10, starter 0/10; sim: l15.s7 |
| l15-moments-quickly.json | screens[7].widget.how | Submit runs 10 hidden tests. They check exact moments (even and odd), midpoint-rule variances to 4 places, tw… | correct | solution run in CPython, 10/10, starter 0/10; sim: l15.s7 |
| l15-moments-quickly.json | screens[7].hints[0].text | For even $k$, the double factorial is $(k - 1)(k - 3)\cdots 1$. | correct | solution run in CPython, 10/10, starter 0/10; sim: l15.s7 |
| l15-moments-quickly.json | screens[7].hints[1].text | The midpoint rule sums $f(\text{midpoint})^2 \times \Delta s$. | correct | solution run in CPython, 10/10, starter 0/10; sim: l15.s7 |
| l15-moments-quickly.json | screens[7].hints[2].text | Simulate $W_t = \sqrt{t}\,Z$ and take the mean and standard error of $W_t^k$. | correct | solution run in CPython, 10/10, starter 0/10; sim: l15.s7 |
| l15-moments-quickly.json | screens[7].feedback.correct | $E[W_2^4] = 12$ and the isometry integral of $s$ over $[0, 2]$ is 2.6667. On seed 5 the simulated fourth mome… | correct | solution run in CPython, 10/10, starter 0/10; sim: l15.s7 |
| l15-moments-quickly.json | screens[7].feedback.generic | Not quite right. Check the examples: $E[W_2^4] = 3 \times 2^2 = 12$. | correct | solution run in CPython, 10/10, starter 0/10; sim: l15.s7 |
| l15-moments-quickly.json | screens[7].explain.text | Exact and simulated moments agree within three standard errors. The simulation is the cross-check an intervie… | correct | solution run in CPython, 10/10, starter 0/10; sim: l15.s7 |
| l15-moments-quickly.json | screens[8].prose | Rapid-fire round. The interviewer asks five questions in a row, and every answer is a number with a one-line … | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].question | Fill in all five answers. | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].widget.rows[0][1].answer | graded key 120 | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].widget.rows[1][1].answer | graded key 2 | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].widget.rows[2][1].answer | graded key 5 | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].widget.rows[3][1].answer | graded key 7.3891 | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].widget.rows[4][1].answer | graded key 2.3333 | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].hints[0].text | Name the rule for each row before computing. | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].hints[1].text | Normal moments are $(2k - 1)!!\,t^k$ for $E[W_t^{2k}]$. | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].hints[2].text | The mgf gives $E[e^{aW_t}] = e^{a^2t/2}$. | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].feedback.correct | $15 \times 8 = 120$, $\min(2, 5) = 2$, $1 + 2 + 2 = 5$, $e^{4/2} = 7.3891$, $\int_0^1 (1 + t)^2\,dt = 7/3$ ${… | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].feedback.generic | Not quite right. Match each question to its rule: normal moments, $\min$, variance of a sum, mgf, isometry. | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].feedback.byKey.r0c1 | $E[W_2^6] = 15t^3$ ${}= 15 \times 8 = 120$. Using $15t^2$ or $15t$ is the usual slip. | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].feedback.byKey.r1c1 | $E[W_2W_5] = \text{Cov}$ ${}= \min(2, 5) = 2$, not the product 10. | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].feedback.byKey.r2c1 | $\text{Var}(W_1 + W_2) = 1 + 2$ ${}+ 2 \times 1 = 5$. Without the covariance you would get 3. | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].feedback.byKey.r3c1 | $E[e^{aW_t}] = e^{a^2t/2}$, so $e^{4/2} = e^2 = 7.3891$. Forgetting the half gives $e^4$. | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].feedback.byKey.r4c1 | The isometry gives $\int_0^1 (1 + t)^2\,dt = 1$ ${}+ 1 + \tfrac13 = 2.3333$. Squaring the integral gives 2.25. | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | screens[8].explain.text | Five rules cover most moment questions. They are normal moments, $\min(s, t)$ for covariance, splitting at th… | correct | the four rules above; sim: l15.s0, l15.s4/s8, l15.s2/s8 |
| l15-moments-quickly.json | summary.ideas[0] | Moments of $W_t$ come from the normal: $E[W_t^{2k}] = (2k - 1)!!\,t^k$, and odd powers of one time vanish. | correct | Shreve Thm 4.3.1 (isometry, general) and 4.4.9 (deterministic); sim: l15.s3 |
| l15-moments-quickly.json | summary.ideas[1] | For two times, split at the earlier one so the new increment is independent: $E[W_s^2W_t^2] = 2s^2 + st$. | correct | Shreve Thm 4.3.1 (isometry, general) and 4.4.9 (deterministic); sim: l15.s3 |
| l15-moments-quickly.json | summary.ideas[2] | Variances of $\int f\,dW$ follow the isometry $\int f^2\,dt$. A $dt$ integral must first become a $dW$ integr… | imprecise | for a random integrand the isometry is ∫E[f²] dt (Shreve Thm 4.3.1(vi)), which quiz q-ito needs. Finding 6 |
| l15-moments-quickly.json | summary.formula.name | Isometry | correct | Shreve Thm 4.3.1 (isometry, general) and 4.4.9 (deterministic); sim: l15.s3 |
| l15-moments-quickly.json | summary.formula.note | The mean is 0 for a $dW$ integral whose $E\int f^2\,dt$ is finite. It does not hold for $dt$ integrals. | correct | Shreve Thm 4.3.1 (isometry, general) and 4.4.9 (deterministic); sim: l15.s3 |
| l15-moments-quickly.json | summary.trap | The isometry is not for $\int W_t\,dt$: convert it to $\int (T - t)\,dW_t$ first, and the variance is $T^3/3$… | correct | Shreve Thm 4.3.1 (isometry, general) and 4.4.9 (deterministic); sim: l15.s3 |
| l15-moments-quickly.json | quiz[0].question | What is $E[W_5^4]$? | correct | 3t² at t = 5 |
| l15-moments-quickly.json | quiz[0].widget.answer | graded key 75 | correct | 3t² at t = 5 |
| l15-moments-quickly.json | quiz[0].widget.accept | $E[W_t^4] = 3t^2 = 3 \times 25 = 75$. | correct | 3t² at t = 5 |
| l15-moments-quickly.json | quiz[0].widget.wrong[0] | slip 25: wrong under every valid reading of the item | correct | 3t² at t = 5; slip arithmetic recomputed |
| l15-moments-quickly.json | quiz[0].widget.wrong[1] | slip 15: wrong under every valid reading of the item | correct | 3t² at t = 5; slip arithmetic recomputed |
| l15-moments-quickly.json | quiz[0].feedback.correct | $3t^2 = 75$. | correct | 3t² at t = 5 |
| l15-moments-quickly.json | quiz[0].feedback.generic | Not quite right. The fourth moment of a normal with variance $t$ is $3t^2$. | correct | 3t² at t = 5 |
| l15-moments-quickly.json | quiz[0].feedback.byKey.squared | You gave $t^2 = 25$, the variance squared. The fourth moment is 3 times that. | correct | 3t² at t = 5 |
| l15-moments-quickly.json | quiz[0].feedback.byKey.linear | You gave $3t = 15$. The fourth moment scales as $t^2$. | correct | 3t² at t = 5 |
| l15-moments-quickly.json | quiz[0].explain.text | $W_5$ is normal with variance 5, so its fourth moment is $3 \times 5^2 = 75$. | correct | 3t² at t = 5 |
| l15-moments-quickly.json | quiz[1].question | What is $E[W_2^5]$? | correct | symmetry W → −W |
| l15-moments-quickly.json | quiz[1].widget.answer | graded key 0 | correct | symmetry W → −W |
| l15-moments-quickly.json | quiz[1].widget.accept | Odd moments of a symmetric distribution vanish: $E[W_2^5] = 0$. | correct | symmetry W → −W |
| l15-moments-quickly.json | quiz[1].widget.wrong[0] | slip 5.6569: wrong under every valid reading of the item | correct | symmetry W → −W; slip arithmetic recomputed |
| l15-moments-quickly.json | quiz[1].widget.wrong[1] | slip 15: wrong under every valid reading of the item | correct | symmetry W → −W; slip arithmetic recomputed |
| l15-moments-quickly.json | quiz[1].feedback.correct | $0$ by symmetry. | correct | symmetry W → −W |
| l15-moments-quickly.json | quiz[1].feedback.generic | Not quite right. $W_2$ is symmetric about 0, so odd powers cancel. | correct | symmetry W → −W |
| l15-moments-quickly.json | quiz[1].feedback.byKey.formula | You used $t^{k/2} = 2^{2.5} = 5.6569$ with no double factorial. For odd $k$ the answer is 0. | correct | symmetry W → −W |
| l15-moments-quickly.json | quiz[1].feedback.byKey.fifteen | You used the even-moment factor $15$ for an odd power. Odd moments vanish. | correct | symmetry W → −W |
| l15-moments-quickly.json | quiz[1].explain.text | $W_2$ and $-W_2$ have the same law, so $E[W_2^5] = -E[W_2^5]$, which forces 0. | correct | symmetry W → −W |
| l15-moments-quickly.json | quiz[2].question | What is $\text{Var}\big(\int_0^3 2\,dW_t\big)$? | correct | isometry; 2W₃ has variance 12 |
| l15-moments-quickly.json | quiz[2].widget.answer | graded key 12 | correct | isometry; 2W₃ has variance 12 |
| l15-moments-quickly.json | quiz[2].widget.accept | The isometry gives $\int_0^3 2^2\,dt = 12$. Equivalently $2W_3$ has variance $4 \times 3$. | correct | isometry; 2W₃ has variance 12 |
| l15-moments-quickly.json | quiz[2].widget.wrong[0] | slip 6: wrong under every valid reading of the item | correct | isometry; slip arithmetic recomputed |
| l15-moments-quickly.json | quiz[2].widget.wrong[1] | slip 36: wrong under every valid reading of the item | correct | isometry; slip arithmetic recomputed |
| l15-moments-quickly.json | quiz[2].feedback.correct | $\int_0^3 4\,dt = 12$. | correct | isometry; 2W₃ has variance 12 |
| l15-moments-quickly.json | quiz[2].feedback.generic | Not quite right. Integrate the square of the integrand, $2^2 = 4$. | correct | isometry; 2W₃ has variance 12 |
| l15-moments-quickly.json | quiz[2].feedback.byKey.no-square | You integrated 2, not $2^2$, which gives $\int_0^3 2\,dt = 6$. | correct | isometry; 2W₃ has variance 12 |
| l15-moments-quickly.json | quiz[2].feedback.byKey.square-outside | You squared the integral, $(2 \times 3)^2 = 36$. Squares go inside. | correct | isometry; 2W₃ has variance 12 |
| l15-moments-quickly.json | quiz[2].explain.text | $\int_0^3 2\,dW = 2W_3$, whose variance is $4 \times 3 = 12$. The isometry says the same. | correct | isometry; 2W₃ has variance 12 |
| l15-moments-quickly.json | quiz[3].question | What is $\text{Var}\big(\int_0^2 W_t\,dW_t\big)$? | correct | Itô isometry with E[W_t²] = t (Shreve Thm 4.3.1(vi)); sim: l15.quiz3 |
| l15-moments-quickly.json | quiz[3].widget.answer | graded key 2 | correct | Itô isometry with E[W_t²] = t (Shreve Thm 4.3.1(vi)); sim: l15.quiz3 |
| l15-moments-quickly.json | quiz[3].widget.accept | $\int_0^2 E[W_t^2]\,dt = \int_0^2 t\,dt = 2$. | correct | Itô isometry with E[W_t²] = t (Shreve Thm 4.3.1(vi)); sim: l15.quiz3 |
| l15-moments-quickly.json | quiz[3].widget.wrong[0] | slip 4: wrong under every valid reading of the item | correct | Itô isometry with E[W_t²] = t (Shreve Thm 4.3.1(vi)); slip arithmetic recomputed |
| l15-moments-quickly.json | quiz[3].widget.wrong[1] | slip 2.6667: wrong under every valid reading of the item | correct | Itô isometry with E[W_t²] = t (Shreve Thm 4.3.1(vi)); slip arithmetic recomputed |
| l15-moments-quickly.json | quiz[3].feedback.correct | $\int_0^2 t\,dt = 2$. | correct | Itô isometry with E[W_t²] = t (Shreve Thm 4.3.1(vi)); sim: l15.quiz3 |
| l15-moments-quickly.json | quiz[3].feedback.generic | Not quite right. The integrand is $W_t$, so its square has mean $t$. | correct | Itô isometry with E[W_t²] = t (Shreve Thm 4.3.1(vi)); sim: l15.quiz3 |
| l15-moments-quickly.json | quiz[3].feedback.byKey.squared | You squared the integral $\int_0^2 t\,dt = 2$. Squares go inside the integral. | correct | Itô isometry with E[W_t²] = t (Shreve Thm 4.3.1(vi)); sim: l15.quiz3 |
| l15-moments-quickly.json | quiz[3].feedback.byKey.one | You used $E[W_t^2] = t^2$, giving $\int_0^2 t^2\,dt = 8/3$. The variance of $W_t$ is $t$, so $E[W_t^2] = t$, … | correct | Itô isometry with E[W_t²] = t (Shreve Thm 4.3.1(vi)); sim: l15.quiz3 |
| l15-moments-quickly.json | quiz[3].explain.text | The isometry for a random integrand uses $E[f(W_t)^2] = E[W_t^2] = t$. The result is $\int_0^2 t\,dt = 2$. | correct | Itô isometry with E[W_t²] = t (Shreve Thm 4.3.1(vi)); sim: l15.quiz3 |

## l16-pricing-in-a-minute.json

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l16-pricing-in-a-minute.json | screens[0].prose | Drill, two minutes. Say the reason first: price is the discounted $Q$-expectation. Our market: $S_0 = 100$, $… | correct | risk-neutral pricing, digital = e^{−rT}Φ(d₂) (Shreve 5.2.5; Hull ch. 26 binary options); sim: l16.s0 |
| l16-pricing-in-a-minute.json | screens[0].question | What is the digital call's price today? Give 4 decimal places. | correct | risk-neutral pricing, digital = e^{−rT}Φ(d₂) (Shreve 5.2.5; Hull ch. 26 binary options); sim: l16.s0 |
| l16-pricing-in-a-minute.json | screens[0].widget.answer | graded key 0.5323 | correct | risk-neutral pricing, digital = e^{−rT}Φ(d₂) (Shreve 5.2.5; Hull ch. 26 binary options); sim: l16.s0 |
| l16-pricing-in-a-minute.json | screens[0].widget.accept | $e^{-rT}\,Q(S_T > 100) = 0.951229 \times 0.559618 = 0.5323$. | correct | risk-neutral pricing, digital = e^{−rT}Φ(d₂) (Shreve 5.2.5; Hull ch. 26 binary options); sim: l16.s0 |
| l16-pricing-in-a-minute.json | screens[0].widget.wrong[0] | slip 0.5596: wrong under every valid reading of the item | correct | risk-neutral pricing, digital = e^{−rT}Φ(d₂) (Shreve 5.2.5; slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[0].widget.wrong[1] | slip 0.6577: wrong under every valid reading of the item | correct | risk-neutral pricing, digital = e^{−rT}Φ(d₂) (Shreve 5.2.5; slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[0].widget.wrong[2] | slip 0.5: wrong under every valid reading of the item | correct | risk-neutral pricing, digital = e^{−rT}Φ(d₂) (Shreve 5.2.5; slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[0].hints[0].text | The label shows the shaded chance under $Q$. | correct | risk-neutral pricing, digital = e^{−rT}Φ(d₂) (Shreve 5.2.5; Hull ch. 26 binary options); sim: l16.s0 |
| l16-pricing-in-a-minute.json | screens[0].hints[1].text | Discount it: multiply by $e^{-0.05} = 0.9512$. | correct | risk-neutral pricing, digital = e^{−rT}Φ(d₂) (Shreve 5.2.5; Hull ch. 26 binary options); sim: l16.s0 |
| l16-pricing-in-a-minute.json | screens[0].feedback.correct | $0.9512 \times 0.5596 = 0.5323$: the shaded $Q$-chance, discounted. | correct | risk-neutral pricing, digital = e^{−rT}Φ(d₂) (Shreve 5.2.5; Hull ch. 26 binary options); sim: l16.s0 |
| l16-pricing-in-a-minute.json | screens[0].feedback.generic | Not quite right. Read the shaded chance off the curve, then discount it from time $T$. | correct | risk-neutral pricing, digital = e^{−rT}Φ(d₂) (Shreve 5.2.5; Hull ch. 26 binary options); sim: l16.s0 |
| l16-pricing-in-a-minute.json | screens[0].feedback.byKey.no-discount | You gave the $Q$-chance 0.5596 as a price. £1 arrives at time $T$, so we discount by $e^{-rT} = 0.9512$. | correct | risk-neutral pricing, digital = e^{−rT}Φ(d₂) (Shreve 5.2.5; Hull ch. 26 binary options); sim: l16.s0 |
| l16-pricing-in-a-minute.json | screens[0].feedback.byKey.real-drift | You used the real drift 12%, so $\Phi(0.5) = 0.6915$, then discounted. Prices use the $Q$ drift $r$, not $\mu… | correct | risk-neutral pricing, digital = e^{−rT}Φ(d₂) (Shreve 5.2.5; Hull ch. 26 binary options); sim: l16.s0 |
| l16-pricing-in-a-minute.json | screens[0].feedback.byKey.coin | You called it a fair coin. The curve is skewed up: $Q(S_T > 100) = \Phi(d_2)$ ${}= 0.5596$. | correct | risk-neutral pricing, digital = e^{−rT}Φ(d₂) (Shreve 5.2.5; Hull ch. 26 binary options); sim: l16.s0 |
| l16-pricing-in-a-minute.json | screens[0].explain.text | The shaded chance is $\Phi(d_2) = \Phi(0.15)$ ${}= 0.5596$, and discounting gives £0.5323. The real drift $\m… | correct | risk-neutral pricing, digital = e^{−rT}Φ(d₂) (Shreve 5.2.5; Hull ch. 26 binary options); sim: l16.s0 |
| l16-pricing-in-a-minute.json | screens[1].prose | Next, a forward struck at 100: it pays $S_T - 100$ at $T$. The payoff is linear, so no model of $S_T$ is need… | imprecise | S₀ − Ke^{−rT} needs a share with no dividends (Hull 5.5 to 5.7); lessons l13 to l17 never say so. Finding 7 |
| l16-pricing-in-a-minute.json | screens[1].question | What is the forward worth today, in £? Give 4 decimal places. | correct | forward value S₀ − Ke^{−rT} for a non-dividend share (Hull 5.7); sim: l16.s1 |
| l16-pricing-in-a-minute.json | screens[1].widget.answer | graded key 4.8771 | correct | forward value S₀ − Ke^{−rT} for a non-dividend share (Hull 5.7); sim: l16.s1 |
| l16-pricing-in-a-minute.json | screens[1].widget.accept | $S_0 - Ke^{-rT} = 100 - 95.1229 = 4.8771$, whatever $\sigma$ is. | correct | forward value S₀ − Ke^{−rT} for a non-dividend share (Hull 5.7); sim: l16.s1 |
| l16-pricing-in-a-minute.json | screens[1].widget.wrong[0] | slip 0: wrong under every valid reading of the item | correct | forward value S₀ − Ke^{−rT} for a non-dividend share (Hull 5.7); slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[1].widget.wrong[1] | slip 105.1271: wrong under every valid reading of the item | correct | forward value S₀ − Ke^{−rT} for a non-dividend share (Hull 5.7); slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[1].widget.wrong[2] | slip 5: wrong under every valid reading of the item | correct | forward value S₀ − Ke^{−rT} for a non-dividend share (Hull 5.7); slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[1].hints[0].text | Value $= e^{-rT}E_Q[S_T - 100]$. | correct | forward value S₀ − Ke^{−rT} for a non-dividend share (Hull 5.7); sim: l16.s1 |
| l16-pricing-in-a-minute.json | screens[1].hints[1].text | $e^{-rT}E_Q[S_T] = S_0$, and $e^{-rT} \times 100 = 95.1229$. | correct | forward value S₀ − Ke^{−rT} for a non-dividend share (Hull 5.7); sim: l16.s1 |
| l16-pricing-in-a-minute.json | screens[1].feedback.correct | $100 - 95.1229 = 4.8771$. | correct | forward value S₀ − Ke^{−rT} for a non-dividend share (Hull 5.7); sim: l16.s1 |
| l16-pricing-in-a-minute.json | screens[1].feedback.generic | Not quite right. Discount the strike, not the share: $S_0 - Ke^{-rT}$. | correct | forward value S₀ − Ke^{−rT} for a non-dividend share (Hull 5.7); sim: l16.s1 |
| l16-pricing-in-a-minute.json | screens[1].feedback.byKey.free | You called an at-the-money forward free. It is free only when $K = S_0e^{rT} = 105.1271$. | correct | forward value S₀ − Ke^{−rT} for a non-dividend share (Hull 5.7); sim: l16.s1 |
| l16-pricing-in-a-minute.json | screens[1].feedback.byKey.forward-price | You gave the forward price $S_0e^{rT}$. The contract's value is today's share less the discounted strike. | correct | forward value S₀ − Ke^{−rT} for a non-dividend share (Hull 5.7); sim: l16.s1 |
| l16-pricing-in-a-minute.json | screens[1].feedback.byKey.simple | You gave $rS_0 = 5$, simple interest on the share. The strike discounts at $e^{-rT}$: $95.1229$. | correct | forward value S₀ − Ke^{−rT} for a non-dividend share (Hull 5.7); sim: l16.s1 |
| l16-pricing-in-a-minute.json | screens[1].explain.text | A forward needs no volatility: $\sigma$ appears nowhere in $S_0 - Ke^{-rT}$. That is why it is the first answ… | correct | forward value S₀ − Ke^{−rT} for a non-dividend share (Hull 5.7); sim: l16.s1 |
| l16-pricing-in-a-minute.json | screens[2].prose | Now the digital put, which pays £1 if $S_T < 100$. The curve shades that side. Its chance under $Q$ is $\Phi(… | correct | digital put e^{−rT}Φ(−d₂); the pair pays £1 a.s.; sim: l16.s2 |
| l16-pricing-in-a-minute.json | screens[2].question | What is the digital put's price? Give 4 decimal places. | correct | digital put e^{−rT}Φ(−d₂); the pair pays £1 a.s.; sim: l16.s2 |
| l16-pricing-in-a-minute.json | screens[2].widget.answer | graded key 0.4189 | correct | digital put e^{−rT}Φ(−d₂); the pair pays £1 a.s.; sim: l16.s2 |
| l16-pricing-in-a-minute.json | screens[2].widget.accept | $e^{-rT}\,\Phi(-d_2) = 0.951229 \times 0.440382 = 0.4189$. | correct | digital put e^{−rT}Φ(−d₂); the pair pays £1 a.s.; sim: l16.s2 |
| l16-pricing-in-a-minute.json | screens[2].widget.wrong[0] | slip 0.4404: wrong under every valid reading of the item | correct | digital put e^{−rT}Φ(−d₂); slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[2].widget.wrong[1] | slip 0.4677: wrong under every valid reading of the item | correct | digital put e^{−rT}Φ(−d₂); slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[2].hints[0].text | The shaded chance is on the other side of 100. | correct | digital put e^{−rT}Φ(−d₂); the pair pays £1 a.s.; sim: l16.s2 |
| l16-pricing-in-a-minute.json | screens[2].hints[1].text | Multiply by $e^{-0.05} = 0.9512$. | correct | digital put e^{−rT}Φ(−d₂); the pair pays £1 a.s.; sim: l16.s2 |
| l16-pricing-in-a-minute.json | screens[2].feedback.correct | $0.9512 \times 0.4404 = 0.4189$. Call plus put is $0.5323 + 0.4189 = 0.9512$. | correct | digital put e^{−rT}Φ(−d₂); the pair pays £1 a.s.; sim: l16.s2 |
| l16-pricing-in-a-minute.json | screens[2].feedback.generic | Not quite right. Discount the shaded $Q$-chance 0.4404. | correct | digital put e^{−rT}Φ(−d₂); the pair pays £1 a.s.; sim: l16.s2 |
| l16-pricing-in-a-minute.json | screens[2].feedback.byKey.no-discount | You gave the chance 0.4404 without discounting. £1 at time $T$ is worth $e^{-rT}$ times that chance. | correct | digital put e^{−rT}Φ(−d₂); the pair pays £1 a.s.; sim: l16.s2 |
| l16-pricing-in-a-minute.json | screens[2].feedback.byKey.complement | You took $1 - 0.5323 = 0.4677$. The two digitals add to $e^{-rT} = 0.9512$, not to 1. | correct | digital put e^{−rT}Φ(−d₂); the pair pays £1 a.s.; sim: l16.s2 |
| l16-pricing-in-a-minute.json | screens[2].explain.text | The call and the put together pay £1 for certain, so they must add to the bond, $e^{-rT} = 0.9512$. Say that … | correct | digital put e^{−rT}Φ(−d₂); the pair pays £1 a.s.; sim: l16.s2 |
| l16-pricing-in-a-minute.json | screens[3].prose | A power payoff pays $S_T^2$ at $T$. Build its price, each line with its reason. Leave out the two flawed line… | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].question | Put the lines in order. | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].widget.lines[0].text | Under $Q$, $S_T = S_0\exp\!\big((r$ ${}- \tfrac12\sigma^2)T$ ${}+ \sigma\sqrt{T}\,Z\big)$ with $Z$ standard n… | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].widget.lines[1].text | Square it: $S_T^2 = S_0^2\exp\!\big(2(r$ ${}- \tfrac12\sigma^2)T$ ${}+ 2\sigma\sqrt{T}\,Z\big)$. | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].widget.lines[2].text | Normal mgf: $E[e^{aZ}] = e^{a^2/2}$ with $a = 2\sigma\sqrt{T}$ gives the factor $e^{2\sigma^2T}$. | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].widget.lines[3].text | Combine exponents: $E_Q[S_T^2]$ ${}= S_0^2e^{(2r - \sigma^2 + 2\sigma^2)T}$ ${}= S_0^2e^{(2r + \sigma^2)T}$. | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].widget.lines[4].text | Discount by $e^{-rT}$: the price is $S_0^2e^{(r + \sigma^2)T}$. | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].widget.lines[5].text | $E_Q[S_T^2] = (E_Q[S_T])^2$ ${}= (S_0e^{rT})^2$. | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].widget.lines[5].why | The mean of a square exceeds the square of the mean. The gap is $e^{\sigma^2T}$. | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].widget.lines[6].text | Use the real drift $\mu$ in $S_T$, since prices should reflect expected growth. | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].widget.lines[6].why | A price is a $Q$-expectation. The hedge removed $\mu$, so the drift is $r$. | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].hints[0].text | Start from the $Q$-law of $S_T$. | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].hints[1].text | The mgf of $Z$ gives the extra $e^{2\sigma^2T}$. | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].feedback.correct | The price is $S_0^2e^{(r + \sigma^2)T}$. | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].feedback.generic | Not quite right. Write $S_T$ under $Q$, square it, use the mgf, then discount. | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].feedback.byKey.x1 | You squared the mean. For a convex payoff that undervalues it by the factor $e^{\sigma^2 T}$. | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].feedback.byKey.x2 | You put the real drift in. Replace $\mu$ by $r$ before taking the expectation. | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].feedback.byKey.left-out | A line of the working is in the Left out list. Only the two flawed lines belong there. | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[3].explain.text | The extra $e^{\sigma^2T}$ over $(S_0e^{rT})^2$ is the price of convexity: volatility makes a convex payoff wo… | correct | lognormal moment by the normal mgf (Hull 15.1; Shreve 5.2); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[4].prose | A junior prices the power claim as "the share squared": $e^{-rT}(S_0e^{rT})^2$. Another leaves out the discou… | correct | 6400e^{0.15375}; sim: l16.s4 |
| l16-pricing-in-a-minute.json | screens[4].question | What is the claim's price in £? Give 2 decimal places. | correct | 6400e^{0.15375}; sim: l16.s4 |
| l16-pricing-in-a-minute.json | screens[4].widget.answer | graded key 7463.68 | correct | 6400e^{0.15375}; sim: l16.s4 |
| l16-pricing-in-a-minute.json | screens[4].widget.accept | $S_0^2e^{(r + \sigma^2)T} = 6400e^{0.15375} = 7{,}463.68$. | correct | 6400e^{0.15375}; sim: l16.s4 |
| l16-pricing-in-a-minute.json | screens[4].widget.wrong[0] | slip 6795.75: wrong under every valid reading of the item | correct | 6400e^{0.15375}; slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[4].widget.wrong[1] | slip 7925.2: wrong under every valid reading of the item | correct | 6400e^{0.15375}; slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[4].widget.wrong[2] | slip 6400: wrong under every valid reading of the item | correct | 6400e^{0.15375}; slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[4].hints[0].text | Add the exponents and multiply by $T$: $(0.04 + 0.0625) \times 1.5$. | correct | 6400e^{0.15375}; sim: l16.s4 |
| l16-pricing-in-a-minute.json | screens[4].hints[1].text | $e^{0.15375} = 1.166199$. | correct | 6400e^{0.15375}; sim: l16.s4 |
| l16-pricing-in-a-minute.json | screens[4].feedback.correct | $6{,}400e^{0.15375} = 7{,}463.68$. | correct | 6400e^{0.15375}; sim: l16.s4 |
| l16-pricing-in-a-minute.json | screens[4].feedback.generic | Not quite right. Price $= S_0^2e^{(r + \sigma^2)T}$. Compute $e^{0.15375}$. | correct | 6400e^{0.15375}; sim: l16.s4 |
| l16-pricing-in-a-minute.json | screens[4].feedback.byKey.jensen | You squared the forward and discounted: $6400e^{0.06} = 6{,}795.75$. That misses the factor $e^{\sigma^2T}$. | correct | 6400e^{0.15375}; sim: l16.s4 |
| l16-pricing-in-a-minute.json | screens[4].feedback.byKey.no-discount | You gave $E_Q[S_T^2] = 6400e^{0.21375}$ ${}= 7{,}925.20$, undiscounted. Multiply by $e^{-0.06}$. | correct | 6400e^{0.15375}; sim: l16.s4 |
| l16-pricing-in-a-minute.json | screens[4].feedback.byKey.spot | You gave $S_0^2 = 6{,}400$, today's share squared. The claim pays at $T$, after growth and convexity. | correct | 6400e^{0.15375}; sim: l16.s4 |
| l16-pricing-in-a-minute.json | screens[4].explain.text | The convexity term $e^{\sigma^2T} = 1.0983$ lifts the price from £6,795.75 to £7,463.68. Say "the mean of a s… | correct | 6400e^{0.15375}; sim: l16.s4 |
| l16-pricing-in-a-minute.json | screens[5].prose | Any payoff splits into pieces we can price. The call is the asset-or-nothing payoff (the share if $S_T > 100$… | correct | call = asset-or-nothing − K cash-or-nothing (Hull ch. 26); sim: l16.s5 |
| l16-pricing-in-a-minute.json | screens[5].question | Price 100 digitals and the call, to 4 decimal places. | correct | call = asset-or-nothing − K cash-or-nothing (Hull ch. 26); sim: l16.s5 |
| l16-pricing-in-a-minute.json | screens[5].widget.rows[1][1].answer | graded key 53.2325 | correct | call = asset-or-nothing − K cash-or-nothing (Hull ch. 26); sim: l16.s5 |
| l16-pricing-in-a-minute.json | screens[5].widget.rows[2][1].answer | graded key 10.4506 | correct | call = asset-or-nothing − K cash-or-nothing (Hull ch. 26); sim: l16.s5 |
| l16-pricing-in-a-minute.json | screens[5].hints[0].text | One digital costs $0.532325$. | correct | call = asset-or-nothing − K cash-or-nothing (Hull ch. 26); sim: l16.s5 |
| l16-pricing-in-a-minute.json | screens[5].hints[1].text | Multiply by the strike, 100. | correct | call = asset-or-nothing − K cash-or-nothing (Hull ch. 26); sim: l16.s5 |
| l16-pricing-in-a-minute.json | screens[5].hints[2].text | Subtract from 63.6831. | correct | call = asset-or-nothing − K cash-or-nothing (Hull ch. 26); sim: l16.s5 |
| l16-pricing-in-a-minute.json | screens[5].feedback.correct | $100 \times 0.532325 = 53.2325$ and $63.6831 - 53.2325 = 10.4506$, the call of lesson 9. | correct | call = asset-or-nothing − K cash-or-nothing (Hull ch. 26); sim: l16.s5 |
| l16-pricing-in-a-minute.json | screens[5].feedback.generic | Not quite right. Price the digital as in screen 1, multiply by 100, then subtract. | correct | call = asset-or-nothing − K cash-or-nothing (Hull ch. 26); sim: l16.s5 |
| l16-pricing-in-a-minute.json | screens[5].feedback.byKey.r1c1 | One digital is $e^{-rT}\Phi(d_2) = 0.532325$. For 100 of them, $53.2325$. Without discounting you would get 5… | correct | call = asset-or-nothing − K cash-or-nothing (Hull ch. 26); sim: l16.s5 |
| l16-pricing-in-a-minute.json | screens[5].feedback.byKey.r2c1 | The call is $63.6831 - 53.2325 = 10.4506$. A sum, not a difference, would give 116.9. | correct | call = asset-or-nothing − K cash-or-nothing (Hull ch. 26); sim: l16.s5 |
| l16-pricing-in-a-minute.json | screens[5].explain.text | The pieces recover the Black-Scholes price: £10.4506. When a payoff is odd, split it into a share-or-nothing … | correct | call = asset-or-nothing − K cash-or-nothing (Hull ch. 26); sim: l16.s5 |
| l16-pricing-in-a-minute.json | screens[6].prose | Edge case. A claim pays £1 at $T$ whatever happens. There is no $S_T$ in it, so no $\sigma$ either. | correct | zero-coupon bond e^{−rT} |
| l16-pricing-in-a-minute.json | screens[6].question | What is it worth today? Give 4 decimal places. | correct | zero-coupon bond e^{−rT} |
| l16-pricing-in-a-minute.json | screens[6].widget.answer | graded key 0.9512 | correct | zero-coupon bond e^{−rT} |
| l16-pricing-in-a-minute.json | screens[6].widget.accept | $e^{-rT} = e^{-0.05} = 0.9512$. | correct | zero-coupon bond e^{−rT} |
| l16-pricing-in-a-minute.json | screens[6].widget.wrong[0] | slip 1: wrong under every valid reading of the item | correct | zero-coupon bond e^{−rT}; slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[6].widget.wrong[1] | slip 0.95: wrong under every valid reading of the item | correct | zero-coupon bond e^{−rT}; slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[6].widget.wrong[2] | slip 1.0513: wrong under every valid reading of the item | correct | zero-coupon bond e^{−rT}; slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[6].hints[0].text | Price $= e^{-rT}E_Q[1]$. | correct | zero-coupon bond e^{−rT} |
| l16-pricing-in-a-minute.json | screens[6].hints[1].text | $E_Q[1] = 1$. | correct | zero-coupon bond e^{−rT} |
| l16-pricing-in-a-minute.json | screens[6].feedback.correct | $e^{-0.05} = 0.9512$: a zero-coupon bond. | correct | zero-coupon bond e^{−rT} |
| l16-pricing-in-a-minute.json | screens[6].feedback.generic | Not quite right. Discount £1 by $e^{-rT}$. | correct | zero-coupon bond e^{−rT} |
| l16-pricing-in-a-minute.json | screens[6].feedback.byKey.none | You gave £1, no discounting. Money later is worth less than money now. | correct | zero-coupon bond e^{−rT} |
| l16-pricing-in-a-minute.json | screens[6].feedback.byKey.simple | You subtracted $r$, giving 0.95. Continuous discounting is $e^{-rT} = 0.9512$. | correct | zero-coupon bond e^{−rT} |
| l16-pricing-in-a-minute.json | screens[6].feedback.byKey.grow | You grew £1 by $e^{rT}$. A future payment is discounted back, not grown. | correct | zero-coupon bond e^{−rT} |
| l16-pricing-in-a-minute.json | screens[6].explain.text | The bond is the unit every other price is built from. It also gives the sum check for digitals: call plus put… | correct | zero-coupon bond e^{−rT} |
| l16-pricing-in-a-minute.json | screens[7].prose | The interviewer pushes the question one step: a payoff $S_T^n$ for any $n$. The same line as before, with $2$… | correct | E_Q[S_T^n] = S₀ⁿexp(n(r−½σ²)T + ½n²σ²T); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[7].question | Give $E_Q[S_T^n]$ in terms of $S_0$, $n$, $r$, $\sigma$ and $T$. | correct | E_Q[S_T^n] = S₀ⁿexp(n(r−½σ²)T + ½n²σ²T); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[7].widget.answer | graded key S_0^ne^{n(r-\sigma^2/2)T+n^2\sigma^2T/2} | correct | E_Q[S_T^n] = S₀ⁿexp(n(r−½σ²)T + ½n²σ²T); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[7].widget.wrong[0] | slip S_0^ne^{nrT}: wrong under every valid reading of the item | correct | E_Q[S_T^n] = S₀ⁿexp(n(r−½σ²)T + ½n²σ²T); slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[7].widget.wrong[1] | slip S_0^ne^{n(r-\sigma^2/2)T}: wrong under every valid reading of the item | correct | E_Q[S_T^n] = S₀ⁿexp(n(r−½σ²)T + ½n²σ²T); slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[7].hints[0].text | $S_T^n = S_0^n\exp\!\big(n(r$ ${}- \tfrac12\sigma^2)T$ ${}+ n\sigma\sqrt{T}\,Z\big)$. | correct | E_Q[S_T^n] = S₀ⁿexp(n(r−½σ²)T + ½n²σ²T); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[7].hints[1].text | The mgf gives $E[e^{aZ}] = e^{a^2/2}$ with $a = n\sigma\sqrt{T}$. | correct | E_Q[S_T^n] = S₀ⁿexp(n(r−½σ²)T + ½n²σ²T); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[7].feedback.correct | $E_Q[S_T^n]$ ${}= S_0^n\exp\!\big(n(r$ ${}- \tfrac12\sigma^2)T$ ${}+ \tfrac12n^2\sigma^2T\big)$. | correct | E_Q[S_T^n] = S₀ⁿexp(n(r−½σ²)T + ½n²σ²T); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[7].feedback.generic | Not quite right. Raise $S_T$ to the $n$ and use the mgf with $a = n\sigma\sqrt{T}$. | correct | E_Q[S_T^n] = S₀ⁿexp(n(r−½σ²)T + ½n²σ²T); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[7].feedback.byKey.jensen | You gave $(E_Q[S_T])^n$, which ignores the spread of $S_T$. The mgf adds $\tfrac12n^2\sigma^2T$. | correct | E_Q[S_T^n] = S₀ⁿexp(n(r−½σ²)T + ½n²σ²T); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[7].feedback.byKey.no-var | You left out the mgf factor $e^{n^2\sigma^2T/2}$. It is the effect of the noise on a power. | correct | E_Q[S_T^n] = S₀ⁿexp(n(r−½σ²)T + ½n²σ²T); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[7].explain.text | Check $n = 1$: the exponent is $rT$, the forward. Check $n = 2$: it is $(2r + \sigma^2)T$, which matches scre… | correct | E_Q[S_T^n] = S₀ⁿexp(n(r−½σ²)T + ½n²σ²T); sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | screens[8].prose | Make the five-minute answers executable. Each formula uses `math.erf` for $\Phi$, and `mc_price` checks any p… | correct | solution run in CPython, 8/8, starter 0/8; sim: l16.s8 |
| l16-pricing-in-a-minute.json | screens[8].question | Complete the four functions. | correct | solution run in CPython, 8/8, starter 0/8; sim: l16.s8 |
| l16-pricing-in-a-minute.json | screens[8].widget.solution | code solution: method taught and hidden tests | correct | solution run in CPython, 8/8, starter 0/8; sim: l16.s8 |
| l16-pricing-in-a-minute.json | screens[8].widget.how | Submit runs 8 hidden tests. They check the forward, digitals at two strikes, and powers (including n = 1, 3 a… | correct | solution run in CPython, 8/8, starter 0/8; sim: l16.s8 |
| l16-pricing-in-a-minute.json | screens[8].hints[0].text | Digital: $e^{-rT}\Phi(d_2)$ with $d_2$ ${}= \dfrac{\ln(S/K) + (r - \sigma^2/2)T}{\sigma\sqrt{T}}$. | correct | solution run in CPython, 8/8, starter 0/8; sim: l16.s8 |
| l16-pricing-in-a-minute.json | screens[8].hints[1].text | Power: $e^{-rT}S^n\exp(n(r$ ${}- \sigma^2/2)T$ ${}+ n^2\sigma^2T/2)$. | correct | solution run in CPython, 8/8, starter 0/8; sim: l16.s8 |
| l16-pricing-in-a-minute.json | screens[8].hints[2].text | Simulate $S_T$ under $Q$, discount each payoff and take mean and standard error. | correct | solution run in CPython, 8/8, starter 0/8; sim: l16.s8 |
| l16-pricing-in-a-minute.json | screens[8].feedback.correct | The formula gives £10,941.74 for $S_T^2$; seed 16 simulates £10,948.77 with standard error £4.56, within 1.5 … | imprecise | gap 7.03 over se 4.56 is 1.54 standard errors. sim: l16.s8 feedback EXPECTED_FAIL. Finding 8 |
| l16-pricing-in-a-minute.json | screens[8].feedback.generic | Not quite right. Check the examples: the forward is 4.8771 and the digital call 0.5323. | correct | solution run in CPython, 8/8, starter 0/8; sim: l16.s8 |
| l16-pricing-in-a-minute.json | screens[8].explain.text | A one-minute formula and a simulation that agrees give two independent checks. Quote the formula; keep the si… | correct | solution run in CPython, 8/8, starter 0/8; sim: l16.s8 |
| l16-pricing-in-a-minute.json | screens[9].prose | A desk quant is asked to price a digital call and digital put at 100 on the spot. A junior writes 0.5323 and … | correct | digital call + put = e^{−rT}; sim: l16.s9 |
| l16-pricing-in-a-minute.json | screens[9].question | By how much does the junior's pair miss the sum that must hold? Give 4 decimal places. | correct | digital call + put = e^{−rT}; sim: l16.s9 |
| l16-pricing-in-a-minute.json | screens[9].widget.answer | graded key 0.0488 | correct | digital call + put = e^{−rT}; sim: l16.s9 |
| l16-pricing-in-a-minute.json | screens[9].widget.accept | The sum must be $e^{-0.05} = 0.9512$; the junior's pair sums to 1, so it is off by $1 - 0.9512 = 0.0488$. | correct | digital call + put = e^{−rT}; sim: l16.s9 |
| l16-pricing-in-a-minute.json | screens[9].widget.wrong[0] | slip 0: wrong under every valid reading of the item | correct | digital call + put = e^{−rT}; slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[9].widget.wrong[1] | slip 0.9512: wrong under every valid reading of the item | correct | digital call + put = e^{−rT}; slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[9].widget.wrong[2] | slip 0.05: wrong under every valid reading of the item | correct | digital call + put = e^{−rT}; slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | screens[9].hints[0].text | The pair together pays £1 for certain at $T$. | correct | digital call + put = e^{−rT}; sim: l16.s9 |
| l16-pricing-in-a-minute.json | screens[9].hints[1].text | Its price is $e^{-rT} = 0.9512$. | correct | digital call + put = e^{−rT}; sim: l16.s9 |
| l16-pricing-in-a-minute.json | screens[9].feedback.correct | $1 - 0.9512 = 0.0488$: the junior forgot to discount the put. | imprecise | 0.4677 is 1 − 0.5323; an undiscounted put would be 0.4404. sim: l16.s9 feedback EXPECTED_FAIL. Finding 9 |
| l16-pricing-in-a-minute.json | screens[9].feedback.generic | Not quite right. Compare the pair's sum with the bond $e^{-rT}$. | correct | digital call + put = e^{−rT}; sim: l16.s9 |
| l16-pricing-in-a-minute.json | screens[9].feedback.byKey.none | You accepted a sum of 1. The two digitals pay £1 at $T$, so they are worth the bond, not £1. | correct | digital call + put = e^{−rT}; sim: l16.s9 |
| l16-pricing-in-a-minute.json | screens[9].feedback.byKey.bond | You gave the required sum 0.9512, not the miss. The miss is the gap between that and the pair's sum. | correct | digital call + put = e^{−rT}; sim: l16.s9 |
| l16-pricing-in-a-minute.json | screens[9].feedback.byKey.simple | You gave $r = 0.05$ as the miss. Continuous discounting makes it $1 - e^{-0.05} = 0.0488$. | correct | digital call + put = e^{−rT}; sim: l16.s9 |
| l16-pricing-in-a-minute.json | screens[9].explain.text | Habit: after any digital, add the call and put and compare with $e^{-rT}$. The junior's pair is £0.0488 per £… | correct | digital call + put = e^{−rT}; sim: l16.s9 |
| l16-pricing-in-a-minute.json | summary.ideas[0] | Price is $e^{-rT}E_Q[\text{payoff}]$: drift $r$, never $\mu$, and always discount. | correct | Shreve 5.2.4 to 5.2.5; sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | summary.ideas[1] | A forward is $S_0 - Ke^{-rT}$ with no $\sigma$. A digital call is $e^{-rT}\Phi(d_2)$, and call plus put equal… | correct | Shreve 5.2.4 to 5.2.5; sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | summary.ideas[2] | For a power, $E_Q[S_T^n]$ ${}= S_0^n\exp\!\big(n(r$ ${}- \tfrac12\sigma^2)T$ ${}+ \tfrac12n^2\sigma^2T\big)$,… | correct | Shreve 5.2.4 to 5.2.5; sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | summary.formula.name | Power payoff | correct | Shreve 5.2.4 to 5.2.5; sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | summary.formula.note | At $n = 1$ this is the forward $S_0e^{rT}$. Discount by $e^{-rT}$ for the price. | correct | Shreve 5.2.4 to 5.2.5; sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | summary.trap | Do not square the forward: $E[S_T^2] \neq (E[S_T])^2$, and do not skip the discount. | correct | Shreve 5.2.4 to 5.2.5; sim: l16.s3/s7 |
| l16-pricing-in-a-minute.json | quiz[0].question | What is the forward price of the share for delivery in 2 years ($S_0 = 100$, $r = 5\%$)? Give 4 decimal place… | correct | forward price S₀e^{rT} (Hull 5.4) |
| l16-pricing-in-a-minute.json | quiz[0].widget.answer | graded key 110.5171 | correct | forward price S₀e^{rT} (Hull 5.4) |
| l16-pricing-in-a-minute.json | quiz[0].widget.accept | $S_0e^{rT} = 100e^{0.1} = 110.5171$. | correct | forward price S₀e^{rT} (Hull 5.4) |
| l16-pricing-in-a-minute.json | quiz[0].widget.wrong[0] | slip 110: wrong under every valid reading of the item | correct | forward price S₀e^{rT} (Hull 5.4); slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | quiz[0].widget.wrong[1] | slip 105.1271: wrong under every valid reading of the item | correct | forward price S₀e^{rT} (Hull 5.4); slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | quiz[0].feedback.correct | $100e^{0.1} = 110.5171$. | correct | forward price S₀e^{rT} (Hull 5.4) |
| l16-pricing-in-a-minute.json | quiz[0].feedback.generic | Not quite right. Grow continuously: $S_0e^{rT}$ with $T = 2$. | correct | forward price S₀e^{rT} (Hull 5.4) |
| l16-pricing-in-a-minute.json | quiz[0].feedback.byKey.simple | You used simple interest, $100(1 + 0.05 \times 2) = 110$. Continuous growth compounds. | correct | forward price S₀e^{rT} (Hull 5.4) |
| l16-pricing-in-a-minute.json | quiz[0].feedback.byKey.one-year | You gave the one-year forward. The delivery is in two years. | correct | forward price S₀e^{rT} (Hull 5.4) |
| l16-pricing-in-a-minute.json | quiz[0].explain.text | Continuous compounding over two years multiplies by $e^{0.1} = 1.10517$. | correct | forward price S₀e^{rT} (Hull 5.4) |
| l16-pricing-in-a-minute.json | quiz[1].question | A claim pays $\ln S_T$ at $T = 1$ (our market). What is its price? Give 4 decimal places. | correct | ln S_T ~ N(ln S₀ + (r−½σ²)T, σ²T) under Q; sim: l16.quiz1 |
| l16-pricing-in-a-minute.json | quiz[1].widget.answer | graded key 4.4091 | correct | ln S_T ~ N(ln S₀ + (r−½σ²)T, σ²T) under Q; sim: l16.quiz1 |
| l16-pricing-in-a-minute.json | quiz[1].widget.accept | $E_Q[\ln S_T] = \ln 100 + (r - \tfrac12\sigma^2)T = 4.6052 + 0.03 = 4.6352$. Discount: $0.9512 \times 4.6352 … | correct | ln S_T ~ N(ln S₀ + (r−½σ²)T, σ²T) under Q; sim: l16.quiz1 |
| l16-pricing-in-a-minute.json | quiz[1].widget.wrong[0] | slip 4.6352: wrong under every valid reading of the item | correct | ln S_T ~ N(ln S₀ + (r−½σ²)T, σ²T) under Q; slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | quiz[1].widget.wrong[1] | slip 4.3806: wrong under every valid reading of the item | correct | ln S_T ~ N(ln S₀ + (r−½σ²)T, σ²T) under Q; slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | quiz[1].feedback.correct | $e^{-0.05}(\ln 100 + 0.03)$ ${}= 4.4091$. | correct | ln S_T ~ N(ln S₀ + (r−½σ²)T, σ²T) under Q; sim: l16.quiz1 |
| l16-pricing-in-a-minute.json | quiz[1].feedback.generic | Not quite right. Take the mean of $\ln S_T$ under $Q$, then discount. | correct | ln S_T ~ N(ln S₀ + (r−½σ²)T, σ²T) under Q; sim: l16.quiz1 |
| l16-pricing-in-a-minute.json | quiz[1].feedback.byKey.no-discount | You gave the $Q$-mean 4.6352 without discounting it. | correct | ln S_T ~ N(ln S₀ + (r−½σ²)T, σ²T) under Q; sim: l16.quiz1 |
| l16-pricing-in-a-minute.json | quiz[1].feedback.byKey.no-drift | You discounted $\ln 100 = 4.6052$ and dropped the drift $r - \tfrac12\sigma^2 = 0.03$. | correct | ln S_T ~ N(ln S₀ + (r−½σ²)T, σ²T) under Q; sim: l16.quiz1 |
| l16-pricing-in-a-minute.json | quiz[1].explain.text | $\ln S_T$ is normal under $Q$ with mean $\ln S_0 + (r$ ${}- \tfrac12\sigma^2)T$, so no integral is needed. | correct | ln S_T ~ N(ln S₀ + (r−½σ²)T, σ²T) under Q; sim: l16.quiz1 |
| l16-pricing-in-a-minute.json | quiz[2].prose | Four claims on our share, all at $T = 1$. | correct | E_Q[S_T] = S₀e^{rT}; sim: l16.s1 |
| l16-pricing-in-a-minute.json | quiz[2].question | Which price does not depend on $\sigma$? | correct | E_Q[S_T] = S₀e^{rT}; sim: l16.s1 |
| l16-pricing-in-a-minute.json | quiz[2].widget.options[0].text | a claim paying $S_T - 100$ | correct | E_Q[S_T] = S₀e^{rT}; sim: l16.s1 |
| l16-pricing-in-a-minute.json | quiz[2].widget.options[1].text | a claim paying £1 if $S_T > 100$ | correct | E_Q[S_T] = S₀e^{rT}; sim: l16.s1 |
| l16-pricing-in-a-minute.json | quiz[2].widget.options[1].why | You forgot that $d_2$ holds $\sigma$. The digital depends on volatility through $\Phi(d_2)$. | correct | E_Q[S_T] = S₀e^{rT}; sim: l16.s1 |
| l16-pricing-in-a-minute.json | quiz[2].widget.options[2].text | a claim paying $S_T^2$ | correct | E_Q[S_T] = S₀e^{rT}; sim: l16.s1 |
| l16-pricing-in-a-minute.json | quiz[2].widget.options[2].why | You forgot the mgf factor $e^{\sigma^2T}$. The square depends on $\sigma$. | correct | E_Q[S_T] = S₀e^{rT}; sim: l16.s1 |
| l16-pricing-in-a-minute.json | quiz[2].widget.options[3].text | a claim paying $\max(S_T - 100, 0)$ | correct | E_Q[S_T] = S₀e^{rT}; sim: l16.s1 |
| l16-pricing-in-a-minute.json | quiz[2].widget.options[3].why | You forgot that an option's price rises with volatility. It depends on $\sigma$. | correct | E_Q[S_T] = S₀e^{rT}; sim: l16.s1 |
| l16-pricing-in-a-minute.json | quiz[2].feedback.correct | A linear payoff needs only $E_Q[S_T]$, which is free of $\sigma$. | correct | E_Q[S_T] = S₀e^{rT}; sim: l16.s1 |
| l16-pricing-in-a-minute.json | quiz[2].feedback.generic | Not quite right. Which payoff is linear in $S_T$? | correct | E_Q[S_T] = S₀e^{rT}; sim: l16.s1 |
| l16-pricing-in-a-minute.json | quiz[2].explain.text | $E_Q[S_T] = S_0e^{rT}$ has no $\sigma$, so the forward needs none. Every nonlinear payoff does. | imprecise | "every" fails at a single spot: √(S_T/F) ln(S_T/F) prices at 0 for all σ. sim: l16.quiz2 EXPECTED_FAIL. Finding 10 |
| l16-pricing-in-a-minute.json | quiz[3].question | What is the price of a claim paying $S_T^3$ (our market)? Give the nearest £. | correct | power formula at n = 3; sim: l16.quiz3 |
| l16-pricing-in-a-minute.json | quiz[3].widget.answer | graded key 1246077 | correct | power formula at n = 3; sim: l16.quiz3 |
| l16-pricing-in-a-minute.json | quiz[3].widget.accept | $S_0^3e^{(2r + 3\sigma^2)T} = 10^6e^{0.10 + 0.12} = 10^6e^{0.22} = 1{,}246{,}076.73$. | correct | power formula at n = 3; sim: l16.quiz3 |
| l16-pricing-in-a-minute.json | quiz[3].widget.wrong[0] | slip 1105170.92: wrong under every valid reading of the item | correct | power formula at n = 3; slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | quiz[3].widget.wrong[1] | slip 1309964.45: wrong under every valid reading of the item | correct | power formula at n = 3; slip arithmetic recomputed |
| l16-pricing-in-a-minute.json | quiz[3].feedback.correct | $10^6e^{0.22}$ ${}= 1{,}246{,}076.73$. | correct | power formula at n = 3; sim: l16.quiz3 |
| l16-pricing-in-a-minute.json | quiz[3].feedback.generic | Not quite right. The exponent is $-r + n(r - \tfrac12\sigma^2)$ ${}+ \tfrac12n^2\sigma^2$ at $n = 3$. | correct | power formula at n = 3; sim: l16.quiz3 |
| l16-pricing-in-a-minute.json | quiz[3].feedback.byKey.jensen | You cubed the forward and discounted: $10^6e^{0.10}$ ${}= 1{,}105{,}170.92$. That misses the convexity factor. | correct | power formula at n = 3; sim: l16.quiz3 |
| l16-pricing-in-a-minute.json | quiz[3].feedback.byKey.no-discount | You gave $E_Q[S_T^3] = 10^6e^{0.27}$, undiscounted. Multiply by $e^{-0.05}$. | correct | power formula at n = 3; sim: l16.quiz3 |
| l16-pricing-in-a-minute.json | quiz[3].explain.text | The exponent is $-0.05 + 3 \times 0.03$ ${}+ \tfrac12 \times 9 \times 0.04$ ${}= 0.22$. Cubes pay a larger co… | correct | power formula at n = 3; sim: l16.quiz3 |

## l17-derivation-aloud.json

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l17-derivation-aloud.json | screens[0].prose | A candidate answers the question below. The interviewer marks the reasoning as much as the result. Three line… | correct | delta-hedge derivation (Hull 15.6; Shreve 4.5.3); sim: l17.s0 |
| l17-derivation-aloud.json | screens[0].question | Tap the three lines that lose marks. | correct | delta-hedge derivation (Hull 15.6; Shreve 4.5.3); sim: l17.s0 |
| l17-derivation-aloud.json | screens[0].hints[0].text | One line has no words at all. | correct | delta-hedge derivation (Hull 15.6; Shreve 4.5.3); sim: l17.s0 |
| l17-derivation-aloud.json | screens[0].hints[1].text | Compare line 4 with Itô's lemma: a term is missing. | correct | delta-hedge derivation (Hull 15.6; Shreve 4.5.3); sim: l17.s0 |
| l17-derivation-aloud.json | screens[0].hints[2].text | Line 6 states a result with no "because". | correct | delta-hedge derivation (Hull 15.6; Shreve 4.5.3); sim: l17.s0 |
| l17-derivation-aloud.json | screens[0].feedback.correct | Silence (line 3), the missing $\tfrac12\sigma^2S^2V_{SS}$ (line 4) and "earns $r$" with no reason (line 6). | correct | delta-hedge derivation (Hull 15.6; Shreve 4.5.3); sim: l17.s0 |
| l17-derivation-aloud.json | screens[0].feedback.generic | Not quite right. Look for a gap in speech, a missing term, and a claim with no "because". | correct | delta-hedge derivation (Hull 15.6; Shreve 4.5.3); sim: l17.s0 |
| l17-derivation-aloud.json | screens[0].feedback.byKey.l1 | You tapped the interviewer. Only the candidate's lines are marked. | correct | delta-hedge derivation (Hull 15.6; Shreve 4.5.3); sim: l17.s0 |
| l17-derivation-aloud.json | screens[0].feedback.byKey.l2 | You tapped the model line. It is correct and states what is assumed. | correct | delta-hedge derivation (Hull 15.6; Shreve 4.5.3); sim: l17.s0 |
| l17-derivation-aloud.json | screens[0].feedback.byKey.l5 | You tapped the hedge. It gives a reason: the $dW$ coefficient vanishes at $\Delta = V_S$. | correct | delta-hedge derivation (Hull 15.6; Shreve 4.5.3); sim: l17.s0 |
| l17-derivation-aloud.json | screens[0].feedback.byKey.l7 | You tapped the check. A forward is the right quick test. | misleading | the forward has V_SS = 0, so it also satisfies the flawed equation of line 6 and cannot catch the dropped term. sim: l17.s0. Finding 11 |
| l17-derivation-aloud.json | screens[0].explain.text | Silence gives the interviewer nothing to mark. Line 4 drops $\tfrac12\sigma^2S^2V_{SS}$ because $(dW)^2 = dt$… | correct | delta-hedge derivation (Hull 15.6; Shreve 4.5.3); sim: l17.s0 |
| l17-derivation-aloud.json | screens[1].prose | Now say it right. These are the lines a strong candidate says, in order, with the reason inside each. The fiv… | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].question | Put the spoken lines in order. | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].widget.lines[0].text | One minute, model and lemma: $dS = \mu S\,dt + \sigma S\,dW$, so $dV = (V_t + \mu SV_S$ ${}+ \tfrac12\sigma^2… | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].widget.lines[1].text | Two minutes, hedge: sell one option, hold $\Delta$ shares. The $dW$ coefficient is $\sigma S(\Delta - V_S)$, … | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].widget.lines[2].text | One minute, no arbitrage: the book has no noise, so it must earn $r$, or cash would beat it. So $d\Pi = r\Pi\… | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].widget.lines[3].text | Equate the $dt$ terms: $V_t + rSV_S$ ${}+ \tfrac12\sigma^2S^2V_{SS}$ ${}- rV = 0$, with $\mu$ gone. | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].widget.lines[4].text | One minute, check: a forward solves it, because $V_{SS} = 0$. I assumed constant $\sigma$, continuous hedging… | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].widget.lines[5].text | Write the final equation first, then fill in the steps behind it. | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].widget.lines[5].why | A result with no route leaves the interviewer to supply the reasons. Say the route first, in order. | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].widget.lines[6].text | Work silently, then read out the finished page. | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].widget.lines[6].why | Silence gives nothing to mark, and a slip cannot be caught early. Every step needs its reason as you go. | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].hints[0].text | Follow the clock: 1, 2, 1, 1 minutes. | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].hints[1].text | The equation comes after the no-arbitrage line, and the check comes last. | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].feedback.correct | That is the five-minute answer: lemma, hedge, no arbitrage, equation, check. | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].feedback.generic | Not quite right. Model and lemma first, then hedge, then no arbitrage, then the equation, then the check. | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].feedback.byKey.x1 | You led with the answer. A derivation goes from the model to the equation, one reason at a time. | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].feedback.byKey.x2 | You worked in silence. The reasons are the marks, so say them as you write. | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].feedback.byKey.left-out | A line of the answer is in the Left out list. Only the two lines that lose marks belong there. | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[1].explain.text | Each line states a step and its reason in one breath. After the equation, the check shows the interviewer you… | correct | Hull 15.6; Shreve 4.5; sim: l17.s1 |
| l17-derivation-aloud.json | screens[2].prose | The interviewer interrupts at the hedge. Answer in one sentence. | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[2].question | Which answer gets the marks? | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[2].widget.options[0].text | $\Delta$ is mine to choose, and $V_S$ makes the $dW$ term zero | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[2].widget.options[1].text | $V_S$ is the delta that dealers quote, so the market sets it, not me | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[2].widget.options[1].why | You treated delta as a market quote. We build the book, and we choose $\Delta$ to kill the noise. | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[2].widget.options[2].text | $V_S$ is the chance the option finishes in the money | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[2].widget.options[2].why | You read delta as a probability. For our call it is $\Phi(d_1) = 0.6368$, not $\Phi(d_2) = 0.5596$. | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[2].widget.options[3].text | any $\Delta$ works, because $dW$ has mean zero and averages out | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[2].widget.options[3].why | You ignored leftover noise. With $\Delta \neq V_S$ the book is risky, so it need not earn $r$. | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[2].hints[0].text | Look at the $dW$ coefficient of the book: $\sigma S(\Delta - V_S)$. | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[2].hints[1].text | Which $\Delta$ makes it zero? | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[2].feedback.correct | $\Delta$ is a free choice, and $V_S$ is the one that cancels the $dW$ term. | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[2].feedback.generic | Not quite right. Ask which choice makes the book riskless. | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[2].feedback.byKey.market | You made delta a market quote. It is a choice that removes the noise. | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[2].feedback.byKey.itm | You read delta as a chance. It is a hedge ratio, and it differs from $\Phi(d_2)$. | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[2].feedback.byKey.any | You said any $\Delta$ works. Only $\Delta = V_S$ leaves no noise. | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[2].explain.text | The $dW$ coefficient of the book is $\sigma S(\Delta - V_S)$. Setting it to zero is the whole reason for $\De… | correct | dW coefficient of −V + ΔS is σS(Δ − V_S); Φ(d₁) = 0.6368, Φ(d₂) = 0.5596 |
| l17-derivation-aloud.json | screens[3].prose | The interviewer asks why the hedged book earns $r$. A junior answers: "It holds shares, so it earns what shar… | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[3].question | Which reply is right? | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[3].widget.options[0].text | no noise is left, so any other return is a sure profit | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[3].widget.options[1].text | shares earn $r$ on average, so the book earns $r$ too | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[3].widget.options[1].why | You gave shares the return $r$. In the real world they earn $\mu$. The argument does not use their average re… | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[3].widget.options[2].text | a hedge removes return as well as risk, so it earns zero | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[3].widget.options[2].why | You assumed a hedge kills return. A riskless book still earns interest on its value. | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[3].widget.options[3].text | $\Delta$ is fixed over the step, so the return is fixed at $r$ | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[3].widget.options[3].why | Holding $\Delta$ fixed is a modelling step. It does not set the return. | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[3].hints[0].text | What if the riskless book earned more than cash? | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[3].hints[1].text | You could borrow cash and hold the book for a sure profit. | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[3].feedback.correct | Riskless means it earns $r$: a riskless book beating or trailing cash is an arbitrage. | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[3].feedback.generic | Not quite right. Ask what an investor could do if a riskless book earned more or less than cash. | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[3].feedback.byKey.mu | You gave the book the share's return. The share's $\mu$ cancelled with the noise. | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[3].feedback.byKey.zero | You said the hedge removes the return. It removes the risk only. | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[3].feedback.byKey.fixed | You pointed at the fixed $\Delta$. That is the set-up, not the reason. | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[3].explain.text | A book with no noise that earned more than $r$ would be a sure profit financed by cash. So it earns exactly $… | correct | no arbitrage: a riskless self-financing book earns r (Hull 15.6) |
| l17-derivation-aloud.json | screens[4].prose | The interviewer notes that the answer has no $\mu$ in it, and asks where it went. | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[4].question | Which answer gets the marks? | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[4].widget.options[0].text | $\mu$ is in $dV$ and in $\Delta\,dS$ with opposite signs, so it cancels | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[4].widget.options[1].text | I assumed $\mu = r$ to keep the algebra short, as an approximation | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[4].widget.options[1].why | You added an assumption. None is needed: $\mu$ cancels by itself. | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[4].widget.options[2].text | $dW$ has mean zero, so $\mu$ averages out over the path | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[4].widget.options[2].why | You averaged away $\mu$. It multiplies $dt$, not $dW$, so averaging leaves it. The hedge removes it. | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[4].widget.options[3].text | discounting at $r$ absorbs $\mu$ into the present value | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[4].widget.options[3].why | You blamed discounting. That uses $r$, and $\mu$ has gone before any discounting. | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[4].hints[0].text | Where does $\mu$ sit in $dV$? | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[4].hints[1].text | And in $d\Pi = -dV + \Delta\,dS$? The signs are opposite. | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[4].feedback.correct | The share's drift appears in the option and in the shares, with opposite signs, and the hedge cancels it. | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[4].feedback.generic | Not quite right. Look at where $\mu$ appears in $dV$ and in $\Delta\,dS$. | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[4].feedback.byKey.assume | You assumed $\mu = r$. Nothing about $\mu$ is assumed. | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[4].feedback.byKey.mean | You averaged $\mu$ away. The cancellation is exact, path by path. | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[4].feedback.byKey.disc | You said discounting removes it. $\mu$ is gone before we discount. | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[4].explain.text | In $d\Pi = -dV + \Delta\,dS$ the $\mu$ terms are $-\mu SV_S$ and $+\mu S\Delta$. With $\Delta = V_S$ they can… | correct | μ terms −μSV_S + μSΔ cancel at Δ = V_S; sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].prose | Last interruption on the assumptions: "What if $\sigma$ is not constant?" | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].question | Which answer gets the marks? | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].widget.options[0].text | $\sigma(t, S)$ changes nothing; a random $\sigma$ needs a second hedge | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].widget.options[1].text | Nothing changes whatever $\sigma$ does, because $\mu$ cancelled | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].widget.options[1].why | You carried the cancellation of $\mu$ over to $\sigma$. A random $\sigma$ is a second source of noise that sh… | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].widget.options[2].text | The equation fails for any $\sigma$ that is not constant | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].widget.options[2].why | You said it fails for every non-constant $\sigma$. With $\sigma(t, S)$ the argument is intact. | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].widget.options[3].text | $\sigma$ moves into the drift term, so $\mu$ returns to the price | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].widget.options[3].why | You moved $\sigma$ into the drift. The new problem is noise from $\sigma$, not a drift. | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].hints[0].text | Does the hedge still cancel $dW$ if $\sigma = \sigma(t, S)$? | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].hints[1].text | What if $\sigma$ had a noise of its own? | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].feedback.correct | With $\sigma(t, S)$ the same steps give the same equation. A stochastic $\sigma$ adds noise the share cannot … | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].feedback.generic | Not quite right. Separate a $\sigma$ that depends on $(t, S)$ from one with its own noise. | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].feedback.byKey.same | You said nothing changes. A random $\sigma$ needs its own hedge, such as another option. | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].feedback.byKey.fails | You said it fails always. A deterministic function $\sigma(t, S)$ keeps the argument. | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].feedback.byKey.drift | You moved $\sigma$ into the drift. The issue is unhedgeable noise. | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[5].explain.text | Local volatility $\sigma(t, S)$ keeps the same equation with $\sigma$ inside. Stochastic volatility needs a s… | correct | local volatility keeps the hedge argument (Hull 27.3); stochastic volatility is incomplete with the share alone (Hull 27.2; Shreve Ex. 6.7); sim: l17.s4/s5/hw |
| l17-derivation-aloud.json | screens[6].prose | Check at $S = 100$, $t = 0$ ($K = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 1$). Take $V = 10.4506$, $\Delta = 0… | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].question | Fill in the four terms and their sum, to 4 decimal places. | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].widget.rows[0][1].answer | graded key -6.414 | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].widget.rows[1][1].answer | graded key 3.1842 | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].widget.rows[2][1].answer | graded key 3.7524 | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].widget.rows[3][1].answer | graded key 0.5225 | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].widget.rows[4][1].answer | graded key 0 | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].hints[0].text | $\Theta$ has two pieces: the volatility piece and the interest piece. | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].hints[1].text | $S\varphi(d_1)\sigma/(2\sqrt{T})$ ${}= 100 \times 0.37524 \times 0.2/2$ ${}= 3.7524$. | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].hints[2].text | Then add the four terms with the sign shown. | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].feedback.correct | $-6.4140 + 3.1842 + 3.7524$ ${}- 0.5225 = 0.0001$ from rounded terms, and $0$ before rounding. | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].feedback.generic | Not quite right. Compute each term to 4 places, then add the first three and subtract $rV$. | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].feedback.byKey.r0c1 | $\Theta = -3.7524 - 2.6616$ ${}= -6.4140$. The first piece is $S\varphi(d_1)\sigma/(2\sqrt{T})$ ${}= 3.7524$,… | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].feedback.byKey.r1c1 | $rS\Delta$ ${}= 0.05 \times 100 \times 0.6368$ ${}= 3.1842$. | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].feedback.byKey.r2c1 | $\tfrac12 \times 0.04 \times 10{,}000 \times 0.018762$ ${}= 3.7524$. | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].feedback.byKey.r3c1 | $rV = 0.05 \times 10.4506$ ${}= 0.5225$. | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].feedback.byKey.r4c1 | The four terms cancel: the sum is zero before rounding, and $0.0001$ from the rounded values. | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[6].explain.text | The terms are $\Theta = -6.4140$, $rS\Delta = 3.1842$, $\tfrac12\sigma^2S^2\Gamma$ ${}= 3.7524$ and $rV = 0.5… | correct | Black-Scholes greeks (Hull 19.5 to 19.7); sim: l17.s6 |
| l17-derivation-aloud.json | screens[7].prose | Follow-up: "Check it on something simple." A forward $V = S - Ke^{-r(T - t)}$ has $V_{SS} = 0$, so the $\sigm… | correct | V = S − Ke^{−r(T−t)}; sim: l17.s7 |
| l17-derivation-aloud.json | screens[7].question | What is $V_t$? Give 4 decimal places. | correct | V = S − Ke^{−r(T−t)}; sim: l17.s7 |
| l17-derivation-aloud.json | screens[7].widget.answer | graded key -2.6598 | correct | V = S − Ke^{−r(T−t)}; sim: l17.s7 |
| l17-derivation-aloud.json | screens[7].widget.accept | $V_t = -rKe^{-r(T - t)} = -0.03 \times 90 \times 0.985112 = -2.6598$. | correct | V = S − Ke^{−r(T−t)}; sim: l17.s7 |
| l17-derivation-aloud.json | screens[7].widget.wrong[0] | slip 2.6598: wrong under every valid reading of the item | correct | V = S − Ke^{−r(T−t)}; slip arithmetic recomputed |
| l17-derivation-aloud.json | screens[7].widget.wrong[1] | slip -2.7: wrong under every valid reading of the item | correct | V = S − Ke^{−r(T−t)}; slip arithmetic recomputed |
| l17-derivation-aloud.json | screens[7].widget.wrong[2] | slip 0: wrong under every valid reading of the item | correct | V = S − Ke^{−r(T−t)}; slip arithmetic recomputed |
| l17-derivation-aloud.json | screens[7].hints[0].text | $\dfrac{d}{dt}\big(-Ke^{-r(T - t)}\big)$ ${}= -rKe^{-r(T - t)}$. | correct | V = S − Ke^{−r(T−t)}; sim: l17.s7 |
| l17-derivation-aloud.json | screens[7].hints[1].text | $e^{-0.015} = 0.985112$. | correct | V = S − Ke^{−r(T−t)}; sim: l17.s7 |
| l17-derivation-aloud.json | screens[7].feedback.correct | $V_t = -2.6598$, and $-2.6598 + 2.4 - (-0.2598) = 0$. | correct | V = S − Ke^{−r(T−t)}; sim: l17.s7 |
| l17-derivation-aloud.json | screens[7].feedback.generic | Not quite right. Differentiate $-Ke^{-r(T - t)}$ with respect to $t$. | correct | V = S − Ke^{−r(T−t)}; sim: l17.s7 |
| l17-derivation-aloud.json | screens[7].feedback.byKey.sign | You gave the right size with the wrong sign. As $t$ rises the strike's present value rises, so $V$ falls: $V_… | correct | V = S − Ke^{−r(T−t)}; sim: l17.s7 |
| l17-derivation-aloud.json | screens[7].feedback.byKey.no-discount | You gave $-rK = -2.7$, with no discount factor $e^{-r(T - t)} = 0.9851$. | correct | V = S − Ke^{−r(T−t)}; sim: l17.s7 |
| l17-derivation-aloud.json | screens[7].feedback.byKey.zero | You set $V_t$ to zero because $V$ is linear in $S$. Time still moves the discounted strike. | correct | V = S − Ke^{−r(T−t)}; sim: l17.s7 |
| l17-derivation-aloud.json | screens[7].explain.text | Then $V_t + rSV_S - rV = -2.6598$ ${}+ 2.4 + 0.2598 = 0$, with $V_{SS} = 0$ and $V = -8.6601$. In one sentenc… | correct | V = S − Ke^{−r(T−t)}; sim: l17.s7 |
| l17-derivation-aloud.json | screens[8].prose | Make the check executable. `pde_terms` returns $\Theta$, $rS\Delta$, $\tfrac12\sigma^2S^2\Gamma$, $rV$ and th… | correct | solution run in CPython, 6/6, starter 0/6; sim: l17.s8 |
| l17-derivation-aloud.json | screens[8].question | Complete `pde_terms`. | correct | solution run in CPython, 6/6, starter 0/6; sim: l17.s8 |
| l17-derivation-aloud.json | screens[8].widget.solution | code solution: method taught and hidden tests | correct | solution run in CPython, 6/6, starter 0/6; sim: l17.s8 |
| l17-derivation-aloud.json | screens[8].widget.how | Submit runs 6 hidden tests. They check the four terms to 4 places at three inputs, and the unrounded sum with… | correct | solution run in CPython, 6/6, starter 0/6; sim: l17.s8 |
| l17-derivation-aloud.json | screens[8].hints[0].text | $\Gamma$ ${}= \varphi(d_1)/(S\sigma\sqrt{T})$ and $\Delta = \Phi(d_1)$. | correct | solution run in CPython, 6/6, starter 0/6; sim: l17.s8 |
| l17-derivation-aloud.json | screens[8].hints[1].text | $\Theta$ ${}= -S\varphi(d_1)\sigma/(2\sqrt{T})$ ${}- rKe^{-rT}\Phi(d_2)$. | correct | solution run in CPython, 6/6, starter 0/6; sim: l17.s8 |
| l17-derivation-aloud.json | screens[8].hints[2].text | Return the list, then the sum of the first three minus the fourth. | correct | solution run in CPython, 6/6, starter 0/6; sim: l17.s8 |
| l17-derivation-aloud.json | screens[8].feedback.correct | At the shared option the terms are $-6.4140$, $3.1842$, $3.7524$, $0.5225$, and the sum is zero to 1e-10. | correct | solution run in CPython, 6/6, starter 0/6; sim: l17.s8 |
| l17-derivation-aloud.json | screens[8].feedback.generic | Not quite right. Check the example: the terms are $-6.414$, $3.1842$, $3.7524$ and $0.5225$. | correct | solution run in CPython, 6/6, starter 0/6; sim: l17.s8 |
| l17-derivation-aloud.json | screens[8].explain.text | A zero residual at three different markets is strong evidence that the equation and the formula agree. It is … | correct | solution run in CPython, 6/6, starter 0/6; sim: l17.s8 |
| l17-derivation-aloud.json | screens[9].prose | A strats final round. You finish the call and the interviewer says: "Now the put. Same hedge. What changes?" … | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | screens[9].question | Which answer gets the marks? | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | screens[9].widget.options[0].text | The equation is the same; only the condition at $T$ changes, to $\max(K - S, 0)$ | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | screens[9].widget.options[1].text | The equation gains a minus sign on $rSV_S$ because $\Delta$ is negative | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | screens[9].widget.options[1].why | You moved the sign into the equation. A negative $\Delta$ is a value of $V_S$, and the equation holds it as i… | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | screens[9].widget.options[2].text | A put needs a fresh derivation with $\Delta = -V_S$ | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | screens[9].widget.options[2].why | You started again. The argument never used the payoff, only that $V$ is a smooth function of $(t, S)$. | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | screens[9].widget.options[3].text | $\mu$ comes back because a put gains when the share falls | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | screens[9].widget.options[3].why | You brought $\mu$ back. The hedge cancels it for any European claim, puts included. | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | screens[9].hints[0].text | The derivation uses only that $V$ is smooth in $(t, S)$. | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | screens[9].hints[1].text | Where does the payoff enter? | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | screens[9].feedback.correct | Same equation, different payoff at $T$: $V_t + rSV_S$ ${}+ \tfrac12\sigma^2S^2V_{SS}$ ${}- rV = 0$ with $V(T,… | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | screens[9].feedback.generic | Not quite right. Which part of the derivation depends on the payoff? | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | screens[9].feedback.byKey.sign | You changed the equation. It holds for any European claim; the put's $V_S$ is simply negative. | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | screens[9].feedback.byKey.new | You restarted. The derivation holds for any European claim, so only the payoff at $T$ changes. | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | screens[9].feedback.byKey.mu | You let $\mu$ back in. The hedge cancels it for any European claim. | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | screens[9].explain.text | Now answer it all aloud. The homework item "Derivation" asks for the five-minute derivation and two interview… | correct | the equation is payoff-free; only the terminal condition changes (Shreve 4.5.4); sim: l17.s9 |
| l17-derivation-aloud.json | summary.ideas[0] | Say the route first, with its reason in each line: model and lemma, hedge, no arbitrage, equation, check. | correct | Hull 15.6; Shreve 4.5 |
| l17-derivation-aloud.json | summary.ideas[1] | $\Delta = V_S$ cancels the $dW$ term and $\mu$ together; a noiseless book earns $r$, or cash would beat it. | correct | Hull 15.6; Shreve 4.5 |
| l17-derivation-aloud.json | summary.ideas[2] | The equation holds for any European claim paying $g(S_T)$, puts and forwards included. Only the payoff at $T$… | correct | Hull 15.6; Shreve 4.5 |
| l17-derivation-aloud.json | summary.formula.name | Black-Scholes equation | correct | Hull 15.6; Shreve 4.5 |
| l17-derivation-aloud.json | summary.formula.note | Five minutes: lemma one, hedge two, arbitrage and equation one, check one. | correct | Hull 15.6; Shreve 4.5 |
| l17-derivation-aloud.json | summary.trap | Do not derive in silence or drop the Itô term. The reasons are the marks, and $\tfrac12\sigma^2S^2V_{SS}$ is … | correct | Hull 15.6; Shreve 4.5 |
| l17-derivation-aloud.json | quiz[0].prose | A claim has $V = 8$ at $S = 80$, with $V_S = 0.5$ and $V_{SS} = 0.01$. Take $r = 4\%$ and $\sigma = 25\%$. | correct | equation solved for V_t; sim: l17.quiz0 |
| l17-derivation-aloud.json | quiz[0].question | What must $V_t$ be for the equation to hold? | correct | equation solved for V_t; sim: l17.quiz0 |
| l17-derivation-aloud.json | quiz[0].widget.answer | graded key -3.28 | correct | equation solved for V_t; sim: l17.quiz0 |
| l17-derivation-aloud.json | quiz[0].widget.accept | $V_t = rV - rSV_S - \tfrac12\sigma^2S^2V_{SS} = 0.32 - 1.6 - 2.0 = -3.28$. | correct | equation solved for V_t; sim: l17.quiz0 |
| l17-derivation-aloud.json | quiz[0].widget.wrong[0] | slip -1.28: wrong under every valid reading of the item | correct | equation solved for V_t; slip arithmetic recomputed |
| l17-derivation-aloud.json | quiz[0].widget.wrong[1] | slip 3.28: wrong under every valid reading of the item | correct | equation solved for V_t; slip arithmetic recomputed |
| l17-derivation-aloud.json | quiz[0].feedback.correct | $0.32 - 1.6 - 2.0 = -3.28$. | correct | equation solved for V_t; sim: l17.quiz0 |
| l17-derivation-aloud.json | quiz[0].feedback.generic | Not quite right. Move $rSV_S$ and the gamma term to the other side of the equation. | correct | equation solved for V_t; sim: l17.quiz0 |
| l17-derivation-aloud.json | quiz[0].feedback.byKey.no-gamma | You left out $\tfrac12\sigma^2S^2V_{SS}$ ${}= 2.0$. That is the Itô term again. | correct | equation solved for V_t; sim: l17.quiz0 |
| l17-derivation-aloud.json | quiz[0].feedback.byKey.flipped | You kept the signs of the left side. Moving terms across changes their signs. | correct | equation solved for V_t; sim: l17.quiz0 |
| l17-derivation-aloud.json | quiz[0].explain.text | The gamma term is $\tfrac12 \times 0.0625 \times 6400 \times 0.01$ ${}= 2.0$. With $rSV_S = 1.6$ and $rV = 0.… | correct | equation solved for V_t; sim: l17.quiz0 |
| l17-derivation-aloud.json | quiz[1].prose | The put with $K = 110$ at $S = 100$ ($r = 5\%$, $\sigma = 20\%$, $T = 1$) has $V = 10.6753$, $\Delta = -0.550… | correct | put greeks; Θ from the equation equals the closed form; sim: l17.quiz1 |
| l17-derivation-aloud.json | quiz[1].question | What is its $\Theta$ from the equation? Give 4 decimal places. | correct | put greeks; Θ from the equation equals the closed form; sim: l17.quiz1 |
| l17-derivation-aloud.json | quiz[1].widget.answer | graded key -0.6721 | correct | put greeks; Θ from the equation equals the closed form; sim: l17.quiz1 |
| l17-derivation-aloud.json | quiz[1].widget.accept | $\Theta = rV - rS\Delta - \tfrac12\sigma^2S^2\Gamma = 0.5338 + 2.7518 - 3.9576 = -0.6721$ from unrounded term… | correct | put greeks; Θ from the equation equals the closed form; sim: l17.quiz1 |
| l17-derivation-aloud.json | quiz[1].widget.wrong[0] | slip -3.4238: wrong under every valid reading of the item | correct | put greeks; slip arithmetic recomputed |
| l17-derivation-aloud.json | quiz[1].widget.wrong[1] | slip -6.414: wrong under every valid reading of the item | correct | put greeks; slip arithmetic recomputed |
| l17-derivation-aloud.json | quiz[1].widget.wrong[2] | slip 0.6721: wrong under every valid reading of the item | correct | put greeks; slip arithmetic recomputed |
| l17-derivation-aloud.json | quiz[1].feedback.correct | $0.5338 + 2.7518 - 3.9576$ ${}= -0.6721$ from unrounded terms ($-0.6720$ from the rounded ones). | correct | put greeks; Θ from the equation equals the closed form; sim: l17.quiz1 |
| l17-derivation-aloud.json | quiz[1].feedback.generic | Not quite right. Solve the equation for $\Theta$ with the put's own $V$, $\Delta$ and $\Gamma$. | correct | put greeks; Θ from the equation equals the closed form; sim: l17.quiz1 |
| l17-derivation-aloud.json | quiz[1].feedback.byKey.no-delta | You dropped $-rS\Delta$. For a put $\Delta$ is negative, so it adds $+2.7518$. | correct | put greeks; Θ from the equation equals the closed form; sim: l17.quiz1 |
| l17-derivation-aloud.json | quiz[1].feedback.byKey.call | You gave the call's theta. The put has the same equation and its own numbers. | correct | put greeks; Θ from the equation equals the closed form; sim: l17.quiz1 |
| l17-derivation-aloud.json | quiz[1].feedback.byKey.flipped | You flipped the sign. The put decays slightly: $\Theta < 0$. | correct | put greeks; Θ from the equation equals the closed form; sim: l17.quiz1 |
| l17-derivation-aloud.json | quiz[1].explain.text | The same equation works for the put. Its negative $\Delta$ makes $-rS\Delta = +2.7518$. | correct | put greeks; Θ from the equation equals the closed form; sim: l17.quiz1 |
| l17-derivation-aloud.json | quiz[2].prose | The interviewer asks: "Is $\Delta = V_S$ held fixed until expiry?" | correct | continuous rebalancing (Hull 15.6, 19.4) |
| l17-derivation-aloud.json | quiz[2].question | Which answer gets the marks? | correct | continuous rebalancing (Hull 15.6, 19.4) |
| l17-derivation-aloud.json | quiz[2].widget.options[0].text | No: it is fixed only over $dt$, then reset to the new $V_S$ | correct | continuous rebalancing (Hull 15.6, 19.4) |
| l17-derivation-aloud.json | quiz[2].widget.options[1].text | Yes: one hedge at the start lasts all the way to $T$ | correct | continuous rebalancing (Hull 15.6, 19.4) |
| l17-derivation-aloud.json | quiz[2].widget.options[1].why | You said hedge once. As $S$ moves, $V_S$ moves, and the book picks up risk. | correct | continuous rebalancing (Hull 15.6, 19.4) |
| l17-derivation-aloud.json | quiz[2].widget.options[2].text | No: it is reset to the share's drift $\mu$ after each step | correct | continuous rebalancing (Hull 15.6, 19.4) |
| l17-derivation-aloud.json | quiz[2].widget.options[2].why | You swapped delta for $\mu$. The hedge ratio is always $V_S$. | correct | continuous rebalancing (Hull 15.6, 19.4) |
| l17-derivation-aloud.json | quiz[2].widget.options[3].text | Yes: gamma corrects the hedge automatically, with no trading | correct | continuous rebalancing (Hull 15.6, 19.4) |
| l17-derivation-aloud.json | quiz[2].widget.options[3].why | You said gamma fixes it. Gamma measures how fast $V_S$ changes. It does not rebalance anything. | correct | continuous rebalancing (Hull 15.6, 19.4) |
| l17-derivation-aloud.json | quiz[2].feedback.correct | The hedge is rebalanced continuously: fixed over each $dt$, new at the next. | correct | continuous rebalancing (Hull 15.6, 19.4) |
| l17-derivation-aloud.json | quiz[2].feedback.generic | Not quite right. $V_S$ changes as $S$ and $t$ change. | correct | continuous rebalancing (Hull 15.6, 19.4) |
| l17-derivation-aloud.json | quiz[2].explain.text | Fixed over an instant is the modelling step. Rebalancing in practice is discrete, which is where hedging erro… | correct | continuous rebalancing (Hull 15.6, 19.4) |
| l17-derivation-aloud.json | quiz[3].prose | A book has $\Gamma = 0.0125$ per call at $S = 100$, with $\sigma = 30\%$. | correct | ½σ²S²Γ = 450 × 0.0125; sim: l17.quiz1/quiz3 |
| l17-derivation-aloud.json | quiz[3].question | What is $\tfrac12\sigma^2S^2\Gamma$ per call, in £ a year? | correct | ½σ²S²Γ = 450 × 0.0125; sim: l17.quiz1/quiz3 |
| l17-derivation-aloud.json | quiz[3].widget.answer | graded key 5.625 | correct | ½σ²S²Γ = 450 × 0.0125; sim: l17.quiz1/quiz3 |
| l17-derivation-aloud.json | quiz[3].widget.accept | $\tfrac12 \times 0.09 \times 10{,}000 \times 0.0125 = 5.625$. | correct | ½σ²S²Γ = 450 × 0.0125; sim: l17.quiz1/quiz3 |
| l17-derivation-aloud.json | quiz[3].widget.wrong[0] | slip 11.25: wrong under every valid reading of the item | correct | ½σ²S²Γ = 450 × 0.0125; slip arithmetic recomputed |
| l17-derivation-aloud.json | quiz[3].widget.wrong[1] | slip 18.75: wrong under every valid reading of the item | correct | ½σ²S²Γ = 450 × 0.0125; slip arithmetic recomputed |
| l17-derivation-aloud.json | quiz[3].feedback.correct | $450 \times 0.0125 = 5.625$. | correct | ½σ²S²Γ = 450 × 0.0125; sim: l17.quiz1/quiz3 |
| l17-derivation-aloud.json | quiz[3].feedback.generic | Not quite right. $\tfrac12\sigma^2S^2 = 450$, then multiply by $\Gamma$. | correct | ½σ²S²Γ = 450 × 0.0125; sim: l17.quiz1/quiz3 |
| l17-derivation-aloud.json | quiz[3].feedback.byKey.no-half | You left out the half: $\sigma^2S^2\Gamma = 11.25$. | correct | ½σ²S²Γ = 450 × 0.0125; sim: l17.quiz1/quiz3 |
| l17-derivation-aloud.json | quiz[3].feedback.byKey.sigma | You used $\sigma = 0.3$ in place of $\sigma^2 = 0.09$. | correct | ½σ²S²Γ = 450 × 0.0125; sim: l17.quiz1/quiz3 |
| l17-derivation-aloud.json | quiz[3].explain.text | $\tfrac12\sigma^2S^2$ ${}= 0.5 \times 0.09 \times 10{,}000$ ${}= 450$, and $450 \times 0.0125 = 5.625$. | correct | ½σ²S²Γ = 450 × 0.0125; sim: l17.quiz1/quiz3 |

## review-4.json

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| review-4.json | items[0].prose | Drill, about a minute. Name the reason before the number. | correct | drift of x³ + tx is x + 3x; sim: review.r-drift |
| review-4.json | items[0].question | What is the drift of $W_t^3 + tW_t$ when $W_t = 1.5$? | correct | drift of x³ + tx is x + 3x; sim: review.r-drift |
| review-4.json | items[0].widget.answer | graded key 6 | correct | drift of x³ + tx is x + 3x; sim: review.r-drift |
| review-4.json | items[0].widget.accept | $f_t = x = 1.5$ and $\tfrac12f_{xx} = 3x = 4.5$, so the drift is $6$. | correct | drift of x³ + tx is x + 3x; sim: review.r-drift |
| review-4.json | items[0].widget.wrong[0] | slip 4.5: wrong under every valid reading of the item | correct | drift of x³ + tx is x + 3x; slip arithmetic recomputed |
| review-4.json | items[0].widget.wrong[1] | slip 1.5: wrong under every valid reading of the item | correct | drift of x³ + tx is x + 3x; slip arithmetic recomputed |
| review-4.json | items[0].feedback.correct | $1.5 + 4.5 = 6$. | correct | drift of x³ + tx is x + 3x; sim: review.r-drift |
| review-4.json | items[0].feedback.generic | Not quite right. Add $f_t$ and $\tfrac12f_{xx}$ for $f = x^3 + tx$. | correct | drift of x³ + tx is x + 3x; sim: review.r-drift |
| review-4.json | items[0].feedback.byKey.no-ft | You left out $f_t = x = 1.5$, the drift of the $tW_t$ term. | correct | drift of x³ + tx is x + 3x; sim: review.r-drift |
| review-4.json | items[0].feedback.byKey.no-fxx | You kept $f_t = 1.5$ and dropped $\tfrac12f_{xx} = 3x = 4.5$, the Itô term of the cube. | correct | drift of x³ + tx is x + 3x; sim: review.r-drift |
| review-4.json | items[0].explain.text | The cube contributes $\tfrac12 \times 6x = 4.5$ and the product $tx$ contributes $f_t = 1.5$. The drift is no… | correct | drift of x³ + tx is x + 3x; sim: review.r-drift |
| review-4.json | items[1].question | For which constant $c$ is $e^{1.5W_t + ct}$ a martingale? | correct | exp(aW − ½a²t); sim: review.r-drift |
| review-4.json | items[1].widget.answer | graded key -1.125 | correct | exp(aW − ½a²t); sim: review.r-drift |
| review-4.json | items[1].widget.accept | The drift is $(c + \tfrac12 \times 2.25)f$, so $c = -1.125$. | correct | exp(aW − ½a²t); sim: review.r-drift |
| review-4.json | items[1].widget.wrong[0] | slip 1.125: wrong under every valid reading of the item | correct | exp(aW − ½a²t); slip arithmetic recomputed |
| review-4.json | items[1].widget.wrong[1] | slip -0.75: wrong under every valid reading of the item | correct | exp(aW − ½a²t); slip arithmetic recomputed |
| review-4.json | items[1].widget.wrong[2] | slip -2.25: wrong under every valid reading of the item | correct | exp(aW − ½a²t); slip arithmetic recomputed |
| review-4.json | items[1].feedback.correct | $c = -1.125$. | correct | exp(aW − ½a²t); sim: review.r-drift |
| review-4.json | items[1].feedback.generic | Not quite right. The drift of $e^{aW_t + ct}$ is $(c + \tfrac12a^2)f$ with $a = 1.5$. | correct | exp(aW − ½a²t); sim: review.r-drift |
| review-4.json | items[1].feedback.byKey.sign | You took $c = +1.125$. The drift is $c + 1.125$, so $c$ must cancel it with $-1.125$. | correct | exp(aW − ½a²t); sim: review.r-drift |
| review-4.json | items[1].feedback.byKey.no-square | You used $\tfrac12a = 0.75$. The second derivative brings $a^2 = 2.25$. | correct | exp(aW − ½a²t); sim: review.r-drift |
| review-4.json | items[1].feedback.byKey.no-half | You used $a^2 = 2.25$ without the half. Itô gives $\tfrac12a^2 = 1.125$. | correct | exp(aW − ½a²t); sim: review.r-drift |
| review-4.json | items[1].explain.text | The sign of $a$ does not matter, because $a^2$ enters. The correction is always $-\tfrac12a^2t$. | correct | exp(aW − ½a²t); sim: review.r-drift |
| review-4.json | items[2].prose | A trade's profit moves like driftless Brownian motion with volatility £0.50 a day. It exits at a take-profit … | correct | E[τ] = ab/σ²; sim: review.r-exit-sigma |
| review-4.json | items[2].question | What is the expected number of days to exit? | correct | E[τ] = ab/σ²; sim: review.r-exit-sigma |
| review-4.json | items[2].widget.answer | graded key 12 | correct | E[τ] = ab/σ²; sim: review.r-exit-sigma |
| review-4.json | items[2].widget.accept | $E[\tau] = ab/\sigma^2 = 3/0.25 = 12$ days. | correct | E[τ] = ab/σ²; sim: review.r-exit-sigma |
| review-4.json | items[2].widget.wrong[0] | slip 3: wrong under every valid reading of the item | correct | E[τ] = ab/σ²; slip arithmetic recomputed |
| review-4.json | items[2].widget.wrong[1] | slip 4: wrong under every valid reading of the item | correct | E[τ] = ab/σ²; slip arithmetic recomputed |
| review-4.json | items[2].widget.wrong[2] | slip 0.75: wrong under every valid reading of the item | correct | E[τ] = ab/σ²; slip arithmetic recomputed |
| review-4.json | items[2].feedback.correct | $3/0.25 = 12$ days. | correct | E[τ] = ab/σ²; sim: review.r-exit-sigma |
| review-4.json | items[2].feedback.generic | Not quite right. $E[\tau] = ab/\sigma^2$ with $a = 3$, $b = 1$ and $\sigma^2 = 0.25$. | correct | E[τ] = ab/σ²; sim: review.r-exit-sigma |
| review-4.json | items[2].feedback.byKey.no-sigma | You gave $ab = 3$, ignoring the volatility. A quieter market takes longer. | correct | E[τ] = ab/σ²; sim: review.r-exit-sigma |
| review-4.json | items[2].feedback.byKey.sum | You gave $a + b = 4$. Distance is not time: the time is the product $ab$, scaled by $\sigma^2$. | correct | E[τ] = ab/σ²; sim: review.r-exit-sigma |
| review-4.json | items[2].feedback.byKey.times | You multiplied by $\sigma^2$. Low volatility makes the exit slower, so divide. | correct | E[τ] = ab/σ²; sim: review.r-exit-sigma |
| review-4.json | items[2].explain.text | The martingale $X_t^2 - \sigma^2t$ gives $E[X_\tau^2] = \sigma^2E[\tau]$, and $E[X_\tau^2] = ab = 3$. With $\… | correct | E[τ] = ab/σ²; sim: review.r-exit-sigma |
| review-4.json | items[3].prose | A price has drift $-0.3$ a day and volatility 1.5 a day, starting at 0. | correct | e^{−2∣μ∣a/σ²} (KS 3.5.C); sim: review.r-ever |
| review-4.json | items[3].question | What is the chance it ever reaches $+1.5$? | correct | e^{−2∣μ∣a/σ²} (KS 3.5.C); sim: review.r-ever |
| review-4.json | items[3].widget.answer | graded key 0.6703 | correct | e^{−2∣μ∣a/σ²} (KS 3.5.C); sim: review.r-ever |
| review-4.json | items[3].widget.accept | The chance is $e^{-2∣\mu∣a/\sigma^2} = e^{-2 \times 0.3 \times 1.5/2.25} = e^{-0.4} = 0.6703$. | correct | e^{−2∣μ∣a/σ²} (KS 3.5.C); sim: review.r-ever |
| review-4.json | items[3].widget.wrong[0] | slip 0.4066: wrong under every valid reading of the item | correct | e^{−2∣μ∣a/σ²} (KS 3.5.C); slip arithmetic recomputed |
| review-4.json | items[3].widget.wrong[1] | slip 0.5488: wrong under every valid reading of the item | correct | e^{−2∣μ∣a/σ²} (KS 3.5.C); slip arithmetic recomputed |
| review-4.json | items[3].feedback.correct | $e^{-0.4} = 0.6703$. | correct | e^{−2∣μ∣a/σ²} (KS 3.5.C); sim: review.r-ever |
| review-4.json | items[3].feedback.generic | Not quite right. The exponent is $2∣\mu∣a/\sigma^2$. | correct | e^{−2∣μ∣a/σ²} (KS 3.5.C); sim: review.r-ever |
| review-4.json | items[3].feedback.byKey.no-sigma | You used $e^{-2\mu a} = e^{-0.9}$. Volatility 1.5 divides the exponent by $\sigma^2 = 2.25$. | correct | e^{−2∣μ∣a/σ²} (KS 3.5.C); sim: review.r-ever |
| review-4.json | items[3].feedback.byKey.unsquared | You divided by $\sigma = 1.5$ rather than $\sigma^2 = 2.25$. | correct | e^{−2∣μ∣a/σ²} (KS 3.5.C); sim: review.r-ever |
| review-4.json | items[3].explain.text | Letting the lower barrier go to $-\infty$ leaves $e^{-2∣\mu∣a/\sigma^2}$. A downward drift lowers the chance,… | correct | e^{−2∣μ∣a/σ²} (KS 3.5.C); sim: review.r-ever |
| review-4.json | items[4].prose | Use $E[W_s^2W_t^2] = 2s^2 + st$ for $s < t$. | correct | 2s² + st; sim: review.r-s2t2 |
| review-4.json | items[4].question | What is $E[W_2^2W_3^2]$? | correct | 2s² + st; sim: review.r-s2t2 |
| review-4.json | items[4].widget.answer | graded key 14 | correct | 2s² + st; sim: review.r-s2t2 |
| review-4.json | items[4].widget.accept | $2 \times 4 + 2 \times 3 = 14$ at $s = 2$, $t = 3$. | correct | 2s² + st; sim: review.r-s2t2 |
| review-4.json | items[4].widget.wrong[0] | slip 6: wrong under every valid reading of the item | correct | 2s² + st; slip arithmetic recomputed |
| review-4.json | items[4].widget.wrong[1] | slip 18: wrong under every valid reading of the item | correct | 2s² + st; slip arithmetic recomputed |
| review-4.json | items[4].feedback.correct | $8 + 6 = 14$. | correct | 2s² + st; sim: review.r-s2t2 |
| review-4.json | items[4].feedback.generic | Not quite right. Substitute $s = 2$ and $t = 3$ into $2s^2 + st$. | correct | 2s² + st; sim: review.r-s2t2 |
| review-4.json | items[4].feedback.byKey.independent | You multiplied the variances, $2 \times 3 = 6$. The two times share the first 2 units of increments. | correct | 2s² + st; sim: review.r-s2t2 |
| review-4.json | items[4].feedback.byKey.no-subtract | You used $3s^2 + st = 18$. The cross term gives $s(t - s)$, so the total is $3s^2 + s(t - s) = 2s^2 + st$. | correct | 2s² + st; sim: review.r-s2t2 |
| review-4.json | items[4].explain.text | Split $W_3 = W_2 + D$: $E[W_2^4] = 12$ and $E[W_2^2]E[D^2] = 2 \times 1$ ${}= 2$, which add to 14. | correct | 2s² + st; sim: review.r-s2t2 |
| review-4.json | items[5].prose | The time integral $\int_0^3 W_t\,dt$ is a $dt$ integral, so convert it first: it equals $\int_0^3 (3 - t)\,dW… | correct | T³/3; sim: review.r-exit-sigma |
| review-4.json | items[5].question | What is $\text{Var}\big(\int_0^3 W_t\,dt\big)$? | correct | T³/3; sim: review.r-exit-sigma |
| review-4.json | items[5].widget.answer | graded key 9 | correct | T³/3; sim: review.r-exit-sigma |
| review-4.json | items[5].widget.accept | $\int_0^3 (3 - t)^2\,dt = 9$. | correct | T³/3; sim: review.r-exit-sigma |
| review-4.json | items[5].widget.wrong[0] | slip 4.5: wrong under every valid reading of the item | correct | T³/3; slip arithmetic recomputed |
| review-4.json | items[5].widget.wrong[1] | slip 27: wrong under every valid reading of the item | correct | T³/3; slip arithmetic recomputed |
| review-4.json | items[5].feedback.correct | $\int_0^3 (3 - t)^2\,dt = 9$. | correct | T³/3; sim: review.r-exit-sigma |
| review-4.json | items[5].feedback.generic | Not quite right. Square the integrand $3 - t$ and integrate over $[0, 3]$. | correct | T³/3; sim: review.r-exit-sigma |
| review-4.json | items[5].feedback.byKey.isometry-dt | You used $\int_0^3 t\,dt = 4.5$, the isometry applied to $W_t\,dt$ directly. Convert to $dW$ first. | correct | T³/3; sim: review.r-exit-sigma |
| review-4.json | items[5].feedback.byKey.cube | You gave $T^3 = 27$. The variance of a time integral is $T^3/3$. | correct | T³/3; sim: review.r-exit-sigma |
| review-4.json | items[5].explain.text | $\int_0^3 (3 - t)^2\,dt = 27/3$ ${}= 9$. The general result is $T^3/3$. | correct | T³/3; sim: review.r-exit-sigma |
| review-4.json | items[6].prose | A new market: $S_0 = 60$, $r = 4\%$, $\sigma = 30\%$. A digital call pays £1 at $T = 2$ if $S_T > 64$. | correct | digital e^{−rT}Φ(d₂); sim: review.r-dig110 |
| review-4.json | items[6].question | What is its price? Give 4 decimal places. | correct | digital e^{−rT}Φ(d₂); sim: review.r-dig110 |
| review-4.json | items[6].widget.answer | graded key 0.3972 | correct | digital e^{−rT}Φ(d₂); sim: review.r-dig110 |
| review-4.json | items[6].widget.accept | $d_2 = (\ln(60/64) + (0.04 - 0.045) \times 2)/(0.3\sqrt2) = -0.1757$, so the price is $e^{-0.08}\Phi(-0.1757)… | correct | digital e^{−rT}Φ(d₂); sim: review.r-dig110 |
| review-4.json | items[6].widget.wrong[0] | slip 0.4303: wrong under every valid reading of the item | correct | digital e^{−rT}Φ(d₂); slip arithmetic recomputed |
| review-4.json | items[6].widget.wrong[1] | slip 0.5522: wrong under every valid reading of the item | correct | digital e^{−rT}Φ(d₂); slip arithmetic recomputed |
| review-4.json | items[6].feedback.correct | $0.9231 \times 0.4303 = 0.3972$. | correct | digital e^{−rT}Φ(d₂); sim: review.r-dig110 |
| review-4.json | items[6].feedback.generic | Not quite right. Use $d_2 = (\ln(S/K) + (r$ ${}- \tfrac12\sigma^2)T)/(\sigma\sqrt{T})$, then discount. | correct | digital e^{−rT}Φ(d₂); sim: review.r-dig110 |
| review-4.json | items[6].feedback.byKey.no-discount | You gave the $Q$-chance $\Phi(d_2) = 0.4303$ as a price. Multiply by $e^{-rT} = 0.9231$. | correct | digital e^{−rT}Φ(d₂); sim: review.r-dig110 |
| review-4.json | items[6].feedback.byKey.d1 | You used $d_1 = 0.2486$, which prices the asset-or-nothing leg. A cash digital uses $d_2$. | correct | digital e^{−rT}Φ(d₂); sim: review.r-dig110 |
| review-4.json | items[6].explain.text | A strike above today's price makes finishing above it less likely than a coin flip, here 0.4303. Discounting … | imprecise | the test is K against the Q-median S₀e^{(r−σ²/2)T}; K = 102 > S₀ = 100 gives 0.52 in the course market. sim: review.r-dig110 EXPECTED_FAIL. Finding 12 |
| review-4.json | items[7].prose | A claim pays $\sqrt{S_T}$ at $T = 2$. Take $S_0 = 100$, $r = 4\%$ and $\sigma = 30\%$. | correct | power formula at n = ½; Jensen for a concave payoff; sim: review.r-sqrt |
| review-4.json | items[7].question | What is its price? Give 4 decimal places. | correct | power formula at n = ½; Jensen for a concave payoff; sim: review.r-sqrt |
| review-4.json | items[7].widget.answer | graded key 9.3941 | correct | power formula at n = ½; Jensen for a concave payoff; sim: review.r-sqrt |
| review-4.json | items[7].widget.accept | $e^{-rT}S_0^{1/2}\exp\!\big(\tfrac12(r - \tfrac12\sigma^2)T + \tfrac18\sigma^2T\big) = 10e^{-0.08 - 0.005 + 0… | correct | power formula at n = ½; Jensen for a concave payoff; sim: review.r-sqrt |
| review-4.json | items[7].widget.wrong[0] | slip 9.6079: wrong under every valid reading of the item | correct | power formula at n = ½; slip arithmetic recomputed |
| review-4.json | items[7].widget.wrong[1] | slip 10.1765: wrong under every valid reading of the item | correct | power formula at n = ½; slip arithmetic recomputed |
| review-4.json | items[7].feedback.correct | $10e^{-0.0625} = 9.3941$. | correct | power formula at n = ½; Jensen for a concave payoff; sim: review.r-sqrt |
| review-4.json | items[7].feedback.generic | Not quite right. Use $n = \tfrac12$ in $S_0^n\exp(n(r$ ${}- \tfrac12\sigma^2)T$ ${}+ \tfrac12n^2\sigma^2T)$, … | correct | power formula at n = ½; Jensen for a concave payoff; sim: review.r-sqrt |
| review-4.json | items[7].feedback.byKey.jensen | You took the square root of the forward and discounted: $e^{-0.08}\sqrt{100e^{0.08}}$ ${}= 9.6079$. A concave… | correct | power formula at n = ½; Jensen for a concave payoff; sim: review.r-sqrt |
| review-4.json | items[7].feedback.byKey.no-discount | You gave $E_Q[\sqrt{S_T}] = 10.1765$, undiscounted. Multiply by $e^{-0.08}$. | correct | power formula at n = ½; Jensen for a concave payoff; sim: review.r-sqrt |
| review-4.json | items[7].explain.text | For $n = \tfrac12$ the volatility term is negative: $\tfrac12n(n - 1)\sigma^2T$ ${}= -0.0225$. A concave payo… | correct | power formula at n = ½; Jensen for a concave payoff; sim: review.r-sqrt |
| review-4.json | items[8].prose | You finish the derivation aloud. The interviewer asks: "So what does the option's price depend on?" | correct | Black-Scholes price is a function of S, t, K, T, r, σ (Hull 15.8) |
| review-4.json | items[8].question | Which answer gets the marks? | correct | Black-Scholes price is a function of S, t, K, T, r, σ (Hull 15.8) |
| review-4.json | items[8].widget.options[0].text | $r$, $\sigma$, the strike and the time, but not $\mu$ | imprecise | omits today's share price (Hull 15.8). Finding 13 |
| review-4.json | items[8].widget.options[1].text | $\mu$ too, because the share's growth sets its value | correct | Black-Scholes price is a function of S, t, K, T, r, σ (Hull 15.8) |
| review-4.json | items[8].widget.options[1].why | You let the real growth rate back in. It cancelled in the hedge, so the price does not carry it. | correct | Black-Scholes price is a function of S, t, K, T, r, σ (Hull 15.8) |
| review-4.json | items[8].widget.options[2].text | only $r$, because the book is riskless | correct | Black-Scholes price is a function of S, t, K, T, r, σ (Hull 15.8) |
| review-4.json | items[8].widget.options[2].why | You forgot the gamma term. Volatility enters through $\tfrac12\sigma^2S^2V_{SS}$. | correct | Black-Scholes price is a function of S, t, K, T, r, σ (Hull 15.8) |
| review-4.json | items[8].widget.options[3].text | the trader's view of $\mu$, which sets the hedge ratio | correct | Black-Scholes price is a function of S, t, K, T, r, σ (Hull 15.8) |
| review-4.json | items[8].widget.options[3].why | You made $\Delta$ depend on $\mu$. $\Delta = V_S$ is fixed by the price curve alone. | correct | Black-Scholes price is a function of S, t, K, T, r, σ (Hull 15.8) |
| review-4.json | items[8].feedback.correct | The price depends on $r$, $\sigma$, $K$ and $T$. Two traders who disagree about $\mu$ agree on it. | imprecise | omits today's share price. Finding 13 |
| review-4.json | items[8].feedback.generic | Not quite right. Which input cancelled in the hedge? | correct | Black-Scholes price is a function of S, t, K, T, r, σ (Hull 15.8) |
| review-4.json | items[8].feedback.byKey.mu | You kept $\mu$ in the price. It cancelled with the noise. | correct | Black-Scholes price is a function of S, t, K, T, r, σ (Hull 15.8) |
| review-4.json | items[8].feedback.byKey.ronly | You dropped $\sigma$. It enters the equation through the gamma term. | correct | Black-Scholes price is a function of S, t, K, T, r, σ (Hull 15.8) |
| review-4.json | items[8].feedback.byKey.view | You tied the hedge to a view of $\mu$. The hedge ratio is $V_S$. | correct | Black-Scholes price is a function of S, t, K, T, r, σ (Hull 15.8) |
| review-4.json | items[8].explain.text | The hedge removes both the noise and the share's drift, so price depends on $r$ and $\sigma$ only. Say it as … | imprecise | "r and σ only" omits S, K and T. Finding 13 |

## homework-4.json

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| homework-4.json | items[0].prose | Derive $P(\text{hit } a \text{ before } -b)$ and $E[\tau]$ for driftless Brownian motion, with the conditions… | correct | optional sampling with bounded and monotone convergence (KS Thm 1.3.22; Williams 10.10); sim: l14.s1 |
| homework-4.json | items[0].question | Put the lines in order. | correct | optional sampling with bounded and monotone convergence (KS Thm 1.3.22; Williams 10.10); sim: l14.s1 |
| homework-4.json | items[0].widget.lines[0].text | Let $\tau$ be the first exit from $(-b, a)$. The stopped process $W_{t \wedge \tau}$ is a martingale in $[-b,… | correct | optional sampling with bounded and monotone convergence (KS Thm 1.3.22; Williams 10.10); sim: l14.s1 |
| homework-4.json | items[0].widget.lines[1].text | $W_t^2 - t$ stopped gives $E[W_{t \wedge \tau}^2]$ ${}= E[t \wedge \tau]$. The left side is at most $\max(a, … | correct | optional sampling with bounded and monotone convergence (KS Thm 1.3.22; Williams 10.10); sim: l14.s1 |
| homework-4.json | items[0].widget.lines[2].text | Let $t \to \infty$ in line 1 (bounded convergence): $E[W_\tau] = 0$, so $Pa - (1 - P)b = 0$ and $P = \dfrac{b… | correct | optional sampling with bounded and monotone convergence (KS Thm 1.3.22; Williams 10.10); sim: l14.s1 |
| homework-4.json | items[0].widget.lines[3].text | Let $t \to \infty$ in line 2: $E[\tau] = E[W_\tau^2] = Pa^2$ ${}+ (1 - P)b^2 = ab$. | correct | optional sampling with bounded and monotone convergence (KS Thm 1.3.22; Williams 10.10); sim: l14.s1 |
| homework-4.json | items[0].widget.lines[4].text | Apply $E[W_\tau] = 0$ at the exit time directly. It holds for every stopping time, so no conditions are neede… | correct | optional sampling with bounded and monotone convergence (KS Thm 1.3.22; Williams 10.10); sim: l14.s1 |
| homework-4.json | items[0].widget.lines[4].why | It fails for a stopping time with infinite mean, such as the hit of a single barrier. Boundedness is the cond… | imprecise | it can fail, it need not: τ = first zero after time 1 has infinite mean and E[W_τ] = 0. Finding 15 |
| homework-4.json | items[0].widget.lines[5].text | Use $E[W_\tau^2] = 0$ too, because $W_t$ has mean 0, so $E[\tau] = 0$. | correct | optional sampling with bounded and monotone convergence (KS Thm 1.3.22; Williams 10.10); sim: l14.s1 |
| homework-4.json | items[0].widget.lines[5].why | $W_t^2$ does not have mean 0. The martingale is $W_t^2 - t$, whose stopped mean gives $E[\tau]$. | correct | optional sampling with bounded and monotone convergence (KS Thm 1.3.22; Williams 10.10); sim: l14.s1 |
| homework-4.json | items[0].feedback.correct | With the stopped martingale bounded and $E[\tau]$ finite, optional stopping gives $P = b/(a + b)$ and $E[\tau… | correct | optional sampling with bounded and monotone convergence (KS Thm 1.3.22; Williams 10.10); sim: l14.s1 |
| homework-4.json | items[0].feedback.generic | Not quite right. Bound the stopped process first, show $E[\tau]$ is finite, then pass to the limit. | correct | optional sampling with bounded and monotone convergence (KS Thm 1.3.22; Williams 10.10); sim: l14.s1 |
| homework-4.json | items[0].feedback.byKey.x1 | You skipped the conditions. Optional stopping needs a bounded stopped value or a finite mean time. | imprecise | same sentence as l14 screens[1]: a finite mean time is not enough for a general martingale. sim: l14.s1.x1 EXPECTED_FAIL. Finding 14 |
| homework-4.json | items[0].feedback.byKey.x2 | You treated $W^2$ as a martingale. Only $W^2 - t$ is one. | correct | optional sampling with bounded and monotone convergence (KS Thm 1.3.22; Williams 10.10); sim: l14.s1 |
| homework-4.json | items[0].feedback.byKey.left-out | A line of the derivation is in the Left out list. Only the two flawed lines belong there. | correct | optional sampling with bounded and monotone convergence (KS Thm 1.3.22; Williams 10.10); sim: l14.s1 |
| homework-4.json | items[0].explain.text | The conditions are the point: a bounded stopped martingale for $P$, and a finite $E[\tau]$ for the second mom… | imprecise | circular: the single barrier "fails finite E[τ], which is why E[τ] = ∞". Finding 16 |
| homework-4.json | items[1].prose | A desk wants one report for a trade that exits at $+a$ or $-b$. The price moves like $X_t = \mu t + \sigma W_… | correct | solution run in CPython, 5/5, starter 0/5; sim: hw.h-exit-report |
| homework-4.json | items[1].question | Complete `exit_report`. | correct | solution run in CPython, 5/5, starter 0/5; sim: hw.h-exit-report |
| homework-4.json | items[1].widget.solution | code solution: method taught and hidden tests | correct | solution run in CPython, 5/5, starter 0/5; sim: hw.h-exit-report |
| homework-4.json | items[1].widget.how | Submit runs 5 hidden tests on seeds 7, 3 and 5. They check the eight numbers, the sign of the time gap, and t… | correct | solution run in CPython, 5/5, starter 0/5; sim: hw.h-exit-report |
| homework-4.json | items[1].feedback.correct | On seed 7 the formula gives $P = 0.5808$ and $E[\tau] = 1.5065$; the simulation gives 0.6008 and 1.6599, a ti… | correct | solution run in CPython, 5/5, starter 0/5; sim: hw.h-exit-report |
| homework-4.json | items[1].feedback.generic | Not quite right. Check the example: it lists all eight numbers on seed 7. | correct | solution run in CPython, 5/5, starter 0/5; sim: hw.h-exit-report |
| homework-4.json | items[1].explain.text | The simulated exit is late because a discrete path can step across a barrier and back. The gap shrinks as $\D… | correct | solution run in CPython, 5/5, starter 0/5; sim: hw.h-exit-report |
| homework-4.json | items[2].prose | Interview habit: price four standard payoffs in under a minute each, with a check that must hold. | correct | solution run in CPython, 5/5, starter 0/5; sim: hw.h-quick-prices |
| homework-4.json | items[2].question | Complete `quick_prices`. | correct | solution run in CPython, 5/5, starter 0/5; sim: hw.h-quick-prices |
| homework-4.json | items[2].widget.solution | code solution: method taught and hidden tests | correct | solution run in CPython, 5/5, starter 0/5; sim: hw.h-quick-prices |
| homework-4.json | items[2].widget.how | Submit runs 5 hidden tests at three markets. They check four prices to 4 places, the digital pair sum, and th… | correct | solution run in CPython, 5/5, starter 0/5; sim: hw.h-quick-prices |
| homework-4.json | items[2].feedback.correct | At $S = 40$, $K = 38$, $r = 2\%$, $\sigma = 15\%$, $T = 0.25$: forward 2.1895, digital call 0.7583, put 0.236… | correct | solution run in CPython, 5/5, starter 0/5; sim: hw.h-quick-prices |
| homework-4.json | items[2].feedback.generic | Not quite right. Check the example: the digital call and put add to $e^{-rT} = 0.9950$. | correct | solution run in CPython, 5/5, starter 0/5; sim: hw.h-quick-prices |
| homework-4.json | items[2].explain.text | Each answer is one line: a linear payoff needs no model, a digital needs $\Phi(d_2)$, a square needs the mgf.… | correct | solution run in CPython, 5/5, starter 0/5; sim: hw.h-quick-prices |
| homework-4.json | items[3].prose | Find $a$ and $b$ so that $M_t = W_t^5 + a\,tW_t^3$ ${}+ b\,t^2W_t$ is a martingale. Its drift is $(a + 10)W_t… | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[0].question | What is $a$? | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[0].widget.answer | graded key -10 | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[0].widget.accept | The $W_t^3$ part of the drift is $(a + 10)W_t^3$, which vanishes at $a = -10$. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[0].widget.wrong[0] | slip 10: wrong under every valid reading of the item | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; slip arithmetic recomputed |
| homework-4.json | items[3].parts[0].widget.wrong[1] | slip -5: wrong under every valid reading of the item | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; slip arithmetic recomputed |
| homework-4.json | items[3].parts[0].feedback.correct | $a = -10$. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[0].feedback.generic | Not quite right. Set the coefficient of $W_t^3$, namely $a + 10$, to zero. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[0].feedback.byKey.sign | You took $a = +10$. The coefficient is $a + 10$, so $a$ must be $-10$. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[0].feedback.byKey.half | You halved the cube coefficient. The cube term of the drift is $\tfrac12 \times 20 = 10$, so $a = -10$. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[0].explain.text | $\tfrac12f_{xx}$ for $x^5$ is $10x^3$, and $f_t$ for $a\,tx^3$ is $ax^3$. They cancel at $a = -10$. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[1].question | With $a = -10$, what is $b$? | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[1].widget.answer | graded key 15 | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[1].widget.accept | The $tW_t$ part is $(3a + 2b) = -30 + 2b$, which vanishes at $b = 15$. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[1].widget.wrong[0] | slip 7.5: wrong under every valid reading of the item | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; slip arithmetic recomputed |
| homework-4.json | items[3].parts[1].widget.wrong[1] | slip -15: wrong under every valid reading of the item | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; slip arithmetic recomputed |
| homework-4.json | items[3].parts[1].widget.wrong[2] | slip 30: wrong under every valid reading of the item | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; slip arithmetic recomputed |
| homework-4.json | items[3].parts[1].feedback.correct | $b = 15$: $W_t^5 - 10tW_t^3 + 15t^2W_t$ is a martingale. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[1].feedback.generic | Not quite right. Set $3a + 2b = 0$ with $a = -10$. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[1].feedback.byKey.half | You halved the $\tfrac12f_{xx}$ term of $a\,tx^3$ a second time, solving $\tfrac32a + 2b = 0$. That term is a… | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[1].feedback.byKey.sign | You took $b = -15$. Then $3a + 2b = -60$, not 0. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[1].feedback.byKey.no-two | You solved $3a + b = 0$, giving 30. The $t^2$ term has $f_t = 2btx$, so the equation is $3a + 2b = 0$. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[1].explain.text | $f_t$ of $b\,t^2x$ is $2btx$, and $\tfrac12f_{xx}$ of $a\,tx^3$ is $3atx$. They cancel at $2b = -3a = 30$. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[2].question | Drop the $t^2W_t$ term. What is the drift of $W_t^5 - 10tW_t^3$ at $t = 1$, $W_t = 1$? | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[2].widget.answer | graded key -30 | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[2].widget.accept | The drift is $(3a)\,tW_t = -30tW_t = -30$. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[2].widget.wrong[0] | slip 30: wrong under every valid reading of the item | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; slip arithmetic recomputed |
| homework-4.json | items[3].parts[2].widget.wrong[1] | slip 0: wrong under every valid reading of the item | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; slip arithmetic recomputed |
| homework-4.json | items[3].parts[2].feedback.correct | $-30$. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[2].feedback.generic | Not quite right. With $a = -10$ the drift is $3a\,tW_t$. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[2].feedback.byKey.sign | You gave $+30$. The coefficient $3a = -30$ is negative. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[2].feedback.byKey.zero | You assumed the process is a martingale. Without the $15t^2W_t$ term the $tW_t$ drift remains. | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[3].parts[2].explain.text | The missing $15t^2W_t$ term contributed $+30tW_t$ to the drift. Without it the drift is $-30tW_t$, so given a… | correct | Hermite He₅: x⁵ − 10tx³ + 15t²x; sim: hw.h-hermite |
| homework-4.json | items[4].prose | A price has drift 0.2 and volatility 0.7 a day. It exits at $+1.5$ or $-2.5$. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[0].question | What is the chance it reaches $+1.5$ first? Give 4 decimal places. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[0].widget.answer | graded key 0.9046 | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[0].widget.accept | $k = 2\mu/\sigma^2 = 0.8163$: $P = (1 - e^{2.0408})/(e^{-1.2245} - e^{2.0408}) = -6.6969/-7.4030 = 0.9046$. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[0].widget.wrong[0] | slip 0.625: wrong under every valid reading of the item | correct | scale function and Wald; slip arithmetic recomputed |
| homework-4.json | items[4].parts[0].widget.wrong[1] | slip 0.792: wrong under every valid reading of the item | correct | scale function and Wald; slip arithmetic recomputed |
| homework-4.json | items[4].parts[0].feedback.correct | $P = 0.9046$. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[0].feedback.generic | Not quite right. The exponent is $2\mu/\sigma^2 = 0.8163$ times $a$ or $b$. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[0].feedback.byKey.no-drift | You gave $b/(a + b) = 0.625$. The drift of 0.2 lifts the chance to 0.9046. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[0].feedback.byKey.no-sigma | You used $2\mu = 0.4$ and no volatility. Dividing by $\sigma^2 = 0.49$ gives 0.8163. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[0].explain.text | With $\mu = 0.2$ and $\sigma^2 = 0.49$ the martingale is $e^{-0.8163X_t}$. Stopping it at $+1.5$ and $-2.5$ g… | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[1].question | What is $E[\tau]$ in days? Give 4 decimal places. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[1].widget.answer | graded key 5.5924 | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[1].widget.accept | Wald: $E[\tau] = (aP - b(1 - P))/\mu = (1.3569 - 0.2384)/0.2 = 5.5924$ from unrounded values. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[1].widget.wrong[0] | slip 7.6531: wrong under every valid reading of the item | correct | scale function and Wald; slip arithmetic recomputed |
| homework-4.json | items[4].parts[1].widget.wrong[1] | slip 3.75: wrong under every valid reading of the item | correct | scale function and Wald; slip arithmetic recomputed |
| homework-4.json | items[4].parts[1].feedback.correct | $E[\tau] = 5.5924$ days. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[1].feedback.generic | Not quite right. Use $E[X_\tau] = \mu E[\tau]$ with $X_\tau = a$ or $-b$. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[1].feedback.byKey.driftless | You used $ab/\sigma^2 = 7.6531$, the driftless formula. With drift the exit is sooner. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[1].feedback.byKey.no-sigma | You gave $ab = 3.75$. That ignores both the drift and the volatility. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[1].explain.text | $E[X_\tau] = aP - b(1 - P)$ ${}= 1.1185$. Dividing by $\mu = 0.2$ gives 5.5924 days. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[2].question | A simulation with $\Delta t = 0.01$ gives a mean exit time above 5.5924. Which is the most likely reason? | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[2].widget.options[0].text | discrete paths cross a barrier between steps, so exits are seen late | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[2].widget.options[1].text | Wald's identity fails when there is drift, so the formula is off | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[2].widget.options[1].why | You blamed Wald. The identity holds for this stopping time. The simulation, not the formula, is off. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[2].widget.options[2].text | the standard error is too small, so neither answer can be trusted | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[2].widget.options[2].why | You blamed noise. The gap is a bias, and it has one sign however many paths you run. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[2].widget.options[3].text | optional stopping fails with two barriers, so the formula is invalid | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[2].widget.options[3].why | You blamed the theorem. Two barriers keep $X$ bounded, and the theorem applies. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[2].feedback.correct | A discrete path can step over a barrier and back, so the simulated exit comes late. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[2].feedback.generic | Not quite right. Ask which direction the bias points as $\Delta t$ shrinks. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[2].feedback.byKey.wald | You said Wald fails. It holds here. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[2].feedback.byKey.se | You called it noise. A bias keeps one sign. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[2].feedback.byKey.stop | You said the theorem fails. It holds with two barriers. | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[4].parts[2].explain.text | The same effect shifts the barrier by about $0.5826\,\sigma\sqrt{\Delta t}$, as in the barrier option. A smal… | correct | scale function and Wald; BGK shift 0.5826σ√Δt; sim: hw.h-exit-drift, l14.s8/hw |
| homework-4.json | items[5].prose | Three moment questions in a row. Split at the earlier time or use the isometry, and say the rule. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[0].question | What is $E[W_2^4W_3^2]$? | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[0].widget.answer | graded key 132 | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[0].widget.accept | $W_3 = W_2 + D$: $E[W_2^4(W_2^2 + 2W_2D + D^2)] = E[W_2^6] + E[W_2^4] = 15 \times 8 + 3 \times 4 = 132$. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[0].widget.wrong[0] | slip 36: wrong under every valid reading of the item | correct | split at the earlier time; slip arithmetic recomputed |
| homework-4.json | items[5].parts[0].widget.wrong[1] | slip 12: wrong under every valid reading of the item | correct | split at the earlier time; slip arithmetic recomputed |
| homework-4.json | items[5].parts[0].feedback.correct | $120 + 12 = 132$. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[0].feedback.generic | Not quite right. Split $W_3$, expand, and use $E[W_2^6] = 15 \times 2^3$ and $E[W_2^4] = 3 \times 2^2$. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[0].feedback.byKey.independent | You multiplied $E[W_2^4] = 12$ by $E[W_3^2] = 3$. The times share $W_2$. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[0].feedback.byKey.no-six | You kept $E[W_2^4]E[D^2] = 12$ and dropped $E[W_2^6] = 120$. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[0].explain.text | The cross term $2W_2^5D$ has mean 0. The sixth moment 120 and the fourth moment 12 add to 132. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[1].question | What is $\text{Var}\big(\int_0^4 W_t\,dt\big)$? Give 4 decimal places. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[1].widget.answer | graded key 21.3333 | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[1].widget.accept | $\int_0^4 W_t\,dt = \int_0^4 (4 - t)\,dW_t$, so the variance is $\int_0^4 (4 - t)^2\,dt = 64/3 = 21.3333$. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[1].widget.wrong[0] | slip 8: wrong under every valid reading of the item | correct | split at the earlier time; slip arithmetic recomputed |
| homework-4.json | items[5].parts[1].widget.wrong[1] | slip 64: wrong under every valid reading of the item | correct | split at the earlier time; slip arithmetic recomputed |
| homework-4.json | items[5].parts[1].feedback.correct | $T^3/3 = 64/3 = 21.3333$. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[1].feedback.generic | Not quite right. Convert to a $dW$ integral first. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[1].feedback.byKey.isometry-dt | You gave $\int_0^4 t\,dt = 8$, the isometry on a $dt$ integral. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[1].feedback.byKey.cube | You gave $T^3 = 64$ and missed the $\tfrac13$. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[1].explain.text | The weight on the increment at time $t$ is the time it stays in the path, $4 - t$. Squaring and integrating g… | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[2].question | What is $\text{Cov}\big(W_1, \int_0^1 W_t\,dt\big)$? | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[2].widget.answer | graded key 0.5 | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[2].widget.accept | $\int_0^1 \text{Cov}(W_1, W_t)\,dt = \int_0^1 t\,dt = 0.5$. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[2].widget.wrong[0] | slip 1: wrong under every valid reading of the item | correct | split at the earlier time; slip arithmetic recomputed |
| homework-4.json | items[5].parts[2].widget.wrong[1] | slip 0.3333: wrong under every valid reading of the item | correct | split at the earlier time; slip arithmetic recomputed |
| homework-4.json | items[5].parts[2].feedback.correct | $\int_0^1 \min(1, t)\,dt$ ${}= \tfrac12$. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[2].feedback.generic | Not quite right. Use $\text{Cov}(W_1, W_t)$ ${}= \min(1, t) = t$ and integrate over $t$. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[2].feedback.byKey.one | You gave $\text{Var}(W_1) = 1$. The time average is correlated with the endpoint, but not perfectly. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[2].feedback.byKey.third | You gave the variance of the time average, $\tfrac13$. The covariance with $W_1$ is $\tfrac12$. | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[5].parts[2].explain.text | Covariance passes inside the integral: $\text{Cov}(W_1, W_t)$ ${}= \min(1, t) = t$, and $\int_0^1 t\,dt = 0.5… | correct | split at the earlier time; T³/3; Fubini for the covariance; sim: review.r-s2t2, hw.h-moments |
| homework-4.json | items[6].prompt | This is the five-minute spoken derivation from lesson 17. Answer aloud, with a watch, in about five minutes. … | correct | Hull 15.6; Shreve 4.5; sim: l17.s7, l17.s4/s5/hw |
| homework-4.json | items[6].model | **1. Model and lemma (about one minute).** The share follows $dS = \mu S\,dt + \sigma S\,dW$ with $(dW)^2 = d… | correct | Hull 15.6; Shreve 4.5; sim: l17.s7, l17.s4/s5/hw |
| homework-4.json | items[6].rubric[0].text | States the model $dS = \mu S\,dt + \sigma S\,dW$ and Itô's lemma for $V(t, S)$, keeping $\tfrac12\sigma^2S^2V… | correct | Hull 15.6; Shreve 4.5; sim: l17.s7, l17.s4/s5/hw |
| homework-4.json | items[6].rubric[1].text | Builds the book $-V + \Delta S$, shows the $dW$ coefficient $\sigma S(\Delta - V_S)$ and chooses $\Delta = V_… | correct | Hull 15.6; Shreve 4.5; sim: l17.s7, l17.s4/s5/hw |
| homework-4.json | items[6].rubric[2].text | Argues that a noiseless book must earn $r$ (an arbitrage against cash otherwise) and states $V_t + rSV_S$ ${}… | correct | Hull 15.6; Shreve 4.5; sim: l17.s7, l17.s4/s5/hw |
| homework-4.json | items[6].rubric[3].text | Checks the result, for example with a forward ($V_{SS} = 0$), and names the assumptions: constant $\sigma$, c… | correct | Hull 15.6; Shreve 4.5; sim: l17.s7, l17.s4/s5/hw |
| homework-4.json | items[6].rubric[4].text | Answers where $\mu$ went: it enters $dV$ and $\Delta\,dS$ with opposite signs and cancels at $\Delta = V_S$. | correct | Hull 15.6; Shreve 4.5; sim: l17.s7, l17.s4/s5/hw |
| homework-4.json | items[6].rubric[5].text | Answers what fails when volatility moves: $\sigma(t, S)$ keeps the equation, a random $\sigma$ needs a second… | correct | Hull 15.6; Shreve 4.5; sim: l17.s7, l17.s4/s5/hw |
| homework-4.json | items[6].rubric[6].text | Says each reason aloud, in order, with no silent steps. Keeps close to the five-minute plan of 1, 2, 1 and 1 … | correct | Hull 15.6; Shreve 4.5; sim: l17.s7, l17.s4/s5/hw |
| homework-4.json | items[7].prompt | Interview round: 30 seconds to plan, then five minutes spoken. A share pays no dividends and follows $dS_t = … | correct | Shreve 4.5 (self-financing book with cash) and 5.2 to 5.4 (the market price of risk needs ∫θ² dt < ∞); sim: l17.s4/s5/hw, hw.h-aloud |
| homework-4.json | items[7].followUps[0] | Your $\Delta$ changes every instant. Why is there no $S\,d\Delta$ term in the book's change, and what does se… | correct | Shreve 4.5 (self-financing book with cash) and 5.2 to 5.4 (the market price of risk needs ∫θ² dt < ∞); sim: l17.s4/s5/hw, hw.h-aloud |
| homework-4.json | items[7].followUps[1] | Which risk has your hedge removed, and which risks would still hit a real book? | correct | Shreve 4.5 (self-financing book with cash) and 5.2 to 5.4 (the market price of risk needs ∫θ² dt < ∞); sim: l17.s4/s5/hw, hw.h-aloud |
| homework-4.json | items[7].followUps[2] | Your $\mu_t$ may depend on the whole past path. Why does it still drop out, and does the drift then never mat… | correct | Shreve 4.5 (self-financing book with cash) and 5.2 to 5.4 (the market price of risk needs ∫θ² dt < ∞); sim: l17.s4/s5/hw, hw.h-aloud |
| homework-4.json | items[7].model | **The plan.** One minute for assumptions and lemma, two for the hedge, one for the equation, one for where ea… | correct | Shreve 4.5 (self-financing book with cash) and 5.2 to 5.4 (the market price of risk needs ∫θ² dt < ∞); sim: l17.s4/s5/hw, hw.h-aloud |
| homework-4.json | items[7].rubric[0].text | Tick only if all are stated before the derivation. A European claim paying $g(S_T)$ at $T$. $V_t$, $V_S$ and … | correct | Shreve 4.5 (self-financing book with cash) and 5.2 to 5.4 (the market price of risk needs ∫θ² dt < ∞); sim: l17.s4/s5/hw, hw.h-aloud |
| homework-4.json | items[7].rubric[1].text | Tick only if both are given. Itô's lemma with $\mu_t$ inside, keeping $\tfrac12\sigma^2S^2V_{SS}$ because $(d… | correct | Shreve 4.5 (self-financing book with cash) and 5.2 to 5.4 (the market price of risk needs ∫θ² dt < ∞); sim: l17.s4/s5/hw, hw.h-aloud |
| homework-4.json | items[7].rubric[2].text | Gives the $dW$ coefficient $\sigma S(\Delta - V_S)$, chooses $\Delta = V_S$, and shows $-\mu_tSV_S + \mu_tS\D… | correct | Shreve 4.5 (self-financing book with cash) and 5.2 to 5.4 (the market price of risk needs ∫θ² dt < ∞); sim: l17.s4/s5/hw, hw.h-aloud |
| homework-4.json | items[7].rubric[3].text | Argues that the riskless book must earn no more and no less than cash, or there is a sure profit. States $V_t… | correct | Shreve 4.5 (self-financing book with cash) and 5.2 to 5.4 (the market price of risk needs ∫θ² dt < ∞); sim: l17.s4/s5/hw, hw.h-aloud |
| homework-4.json | items[7].rubric[4].text | Tick only if all three follow-ups are answered. No $S\,d\Delta$ term, because each rebalance is paid from cas… | correct | Shreve 4.5 (self-financing book with cash) and 5.2 to 5.4 (the market price of risk needs ∫θ² dt < ∞); sim: l17.s4/s5/hw, hw.h-aloud |
