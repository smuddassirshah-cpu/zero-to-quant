# Engine 835 onward: Fluency authoring reach and answer correctness

Source: the bullets under the six `Raised later (fluency ...)` headings in `docs/BACKLOG-INBOX.md` (each now marked "numbered n"). Items 835 to 841 are appended to `docs/ENGINE-BACKLOG.md`, each with a status line. Commits: `Engine 835+: isolate test-cumulative ...` (group 1) and `Engine 835+: let and where functions ...` (group 2), then a last commit for the test and report fixes.

## Group 1 (correctness)

**835 `test-cumulative`.** The weekly review's cap was not broken. The five failures were fixtures wrongly reading real content: once real Fluency sets existed in several courses, cases that expected "no Fluency set written" or "four generated items from the one course with a set" counted the generated items of every real set. Part C now reads the real sets once, starts each case with none (`C._setFluency([])`) and registers the fixture itself. One new case puts every real set in force and checks that no course gives more than four items and generated items stay within the cap of each course. 26 of 26. `select.js` is unchanged.

**836 plain-text function names.** `plainFns` (first step of `prep` in `js/engine/grade.js`) reads `ln`, `log`, `exp`, `sin`, `cos`, `tan`, `sqrt` directly before `(` as the functions in `answer`, `accept` and learner input. Not touched: a name behind a backslash, inside a longer word (`arcsin(`, `sinh(`), with no bracket (`sinx`), and products of single letters (`ab(x)`). `ln(97)/ln(4)` no longer equals 97/4. Cases in `tools/test-expr-equations.mjs` (146 of 146) and the widget case in `tools/test-answer-forms.mjs`. `test-expr-equations --audit` output is identical before and after.

**Audit (`tools/audit-plain-functions.mjs`, run with `--local-cdn <pkgs>`; compares with the grader of commit 657ce91c).** expression widgets read: 521 (Fluency families count once per draw); entries with a function name: 115; same 3, CHANGED 86, DEAD 8 (read after the fix), STILL-DEAD 18, WRONG-OK 0 entries whose grading was wrong before the fix: 112. In plain words: of 115 entries (answer, accept and wrong, content and Fluency families drawn on five seeds), **112 were graded wrongly before the fix**: 86 CHANGED (an `accept` or `answer` took the product-of-letters value, a wrong value, while the intended value was accepted by another form), 8 DEAD and fixed (the intended value was refused before), 18 STILL-DEAD (the entry did not parse before and still does not: text spellings such as `**`, `x²` and `e^(3x)` that are not LaTeX; these are content to repair, an engine fault only in that nothing warns). 3 entries (the trees homework `sigma*sqrt(T)/2` forms) read the same either way. No `wrong[]` value was graded correct before and incorrect after (WRONG-OK 0): the exp-log case the inbox names was already worked round in that set. No Fluency family is affected (all 46 sets draw identically, see below). The 112 are in lessons, homework, reviews and exams; the content is not edited. List, one entry per line (status, file, widget, role, text):

```
CHANGED content/courses/analysis/homework-1.json .items[1].widget  accept  "1/sqrt(\\varepsilon)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/analysis/l21-fundamental-theorem-proved.json .screens[5].widget  accept  "2x cos(x^2)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/analysis/l21-fundamental-theorem-proved.json .screens[5].widget  accept  "2*x*cos(x^2)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/analysis/review-5.json .items[2].widget  accept  "3x^2 ln(x^3)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/analysis/review-5.json .items[2].widget  accept  "9x^2 ln(x)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/estimation/homework-3.json .items[0].widget  accept  "1/(2sqrt(n))"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/estimation/homework-3.json .items[0].widget  accept  "1/(2*sqrt(n))"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/estimation/homework-3.json .items[0].widget  accept  "0.5/sqrt(n)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/estimation/homework-3.json .items[0].widget  accept  "1/(2 sqrt(n))"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/estimation/homework-3.json .items[0].widget  accept  "(1/2)/sqrt(n)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/exp-log/homework-3.json .items[5].widget  accept  "ln(4)/0.08"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/exp-log/homework-3.json .items[5].widget  accept  "12.5ln(4)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/exp-log/homework-3.json .items[5].widget  accept  "12.5*ln(4)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/exp-log/homework-3.json .items[5].widget  accept  "25ln(2)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/exp-log/homework-3.json .items[5].widget  accept  "25*ln(2)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/exp-log/homework-3.json .items[5].widget  accept  "ln(4)/(0.08)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
STILL-DEAD content/courses/integrals/homework-2.json .items[0].widget  accept  "x^4+2e^(3x)-2ln(x)"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
STILL-DEAD content/courses/integrals/homework-2.json .items[0].widget  accept  "x^4+2e^(3*x)-2ln(x)"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
STILL-DEAD content/courses/integrals/homework-2.json .items[0].widget  accept  "x^4+2*e^(3x)-2ln(x)"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
STILL-DEAD content/courses/integrals/homework-2.json .items[0].widget  accept  "x^4+2e^(3x)-2ln(x)+C"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
STILL-DEAD content/courses/integrals/homework-2.json .items[0].widget  accept  "x^4+2e^(3x)-2ln(x)+c"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
STILL-DEAD content/courses/integrals/homework-2.json .items[0].widget  accept  "x^4+2e^(3*x)-2ln(x)+C"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
STILL-DEAD content/courses/integrals/homework-2.json .items[0].widget  accept  "x^4+2e^(3*x)-2ln(x)+c"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
STILL-DEAD content/courses/integrals/homework-2.json .items[0].widget  accept  "x^4+2*e^(3x)-2ln(x)+C"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
STILL-DEAD content/courses/integrals/homework-2.json .items[0].widget  accept  "x^4+2*e^(3x)-2ln(x)+c"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
CHANGED content/courses/integrals/homework-3.json .items[1].widget  accept  "(x^3/3)ln(x)-x^3/9"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/integrals/homework-3.json .items[1].widget  accept  "x^3*ln(x)/3-x^3/9"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/integrals/homework-3.json .items[1].widget  accept  "x^3(3ln(x)-1)/9"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
DEAD    content/courses/integrals/l10-undo-product.json .screens[2].widget  accept  "xsin(x)+cos(x)"  [the intended value was refused before the fix (the entry took a different value)]
CHANGED content/courses/integrals/l10-undo-product.json .screens[2].widget  accept  "x*sin(x)+cos(x)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/integrals/l10-undo-product.json .screens[2].widget  accept  "cos(x)+x*sin(x)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/integrals/l10-undo-product.json .screens[5].widget  accept  "x*ln(x)-x"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/integrals/l10-undo-product.json .screens[5].widget  accept  "x(ln(x)-1)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/integrals/l14-splitting-fractions.json .screens[5].widget  accept  "ln(x)-0.5ln(x^2+1)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/integrals/l14-splitting-fractions.json .screens[5].widget  accept  "ln(x)-1/2*ln(x^2+1)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/integrals/l14-splitting-fractions.json .screens[5].widget  accept  "ln(x)-ln(x^2+1)/2"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/integrals/l15-circles-and-powers.json .screens[3].widget  accept  "-cos(x)+cos(x)^3/3"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/integrals/l15-circles-and-powers.json .screens[3].widget  accept  "cos(x)^3/3-cos(x)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/integrals/l9-undo-chain.json .screens[2].widget  accept  "sin(x^2)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
STILL-DEAD content/courses/integrals/l9-undo-chain.json .screens[2].widget  accept  "sin(x²)"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
CHANGED content/courses/integrals/l9-undo-chain.json .screens[2].widget  accept  "sin (x^2)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
STILL-DEAD content/courses/integrals/l9-undo-chain.json .screens[2].widget  accept  "sin(x**2)"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
CHANGED content/courses/integrals/l9-undo-chain.json .screens[4].widget  accept  "ln(x^2+1)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
DEAD    content/courses/integrals/l9-undo-chain.json .screens[4].widget  accept  "log(x^2+1)"  [the intended value was refused before the fix (the entry took a different value)]
CHANGED content/courses/integrals/l9-undo-chain.json .screens[4].widget  accept  "ln(1+x^2)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
STILL-DEAD content/courses/integrals/l9-undo-chain.json .screens[4].widget  accept  "ln(x**2+1)"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
CHANGED content/courses/integrals/l9-undo-chain.json .quiz[0].widget  accept  "sin(x^3)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
STILL-DEAD content/courses/integrals/l9-undo-chain.json .quiz[0].widget  accept  "sin(x³)"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
STILL-DEAD content/courses/integrals/l9-undo-chain.json .quiz[0].widget  accept  "sin(x**3)"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
CHANGED content/courses/integrals/l9-undo-chain.json .quiz[3].widget  accept  "(ln(x))^2/2"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
DEAD    content/courses/integrals/l9-undo-chain.json .quiz[3].widget  accept  "1/2(ln(x))^2"  [the intended value was refused before the fix (the entry took a different value)]
CHANGED content/courses/integrals/l9-undo-chain.json .quiz[3].widget  accept  "0.5(ln(x))^2"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/integrals/l9-undo-chain.json .quiz[3].widget  accept  "ln(x)^2/2"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/integrals/review-2.json .items[1].widget  accept  "x^3-4ln(x)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/integrals/review-2.json .items[1].widget  accept  "x^3-4ln(x)+C"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/integrals/review-2.json .items[1].widget  accept  "x^3-4ln(x)+c"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/integrals/review-3.json .items[1].widget  accept  "sin(x)-x*cos(x)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
DEAD    content/courses/integrals/review-3.json .items[1].widget  accept  "-xcos(x)+sin(x)"  [the intended value was refused before the fix (the entry took a different value)]
DEAD    content/courses/integrals/review-3.json .items[1].widget  accept  "sin(x)-xcos(x)"  [the intended value was refused before the fix (the entry took a different value)]
CHANGED content/courses/limits/homework-2.json .items[2].widget  accept  "1/sqrt(x)+3/x^2+x^3"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits/homework-2.json .items[2].widget  accept  "x^3+3/x^2+1/sqrt(x)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits/homework-2.json .items[2].widget  accept  "1/sqrt(x) + 3/x^2 + x^3"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits/homework-3.json .items[6].widget  accept  "x^x(ln(x)+1)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits/homework-3.json .items[6].widget  accept  "x^x*ln(x)+x^x"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits/homework-3.json .items[6].widget  accept  "x^x(1+ln(x))"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits/l10-inside-function.json .screens[6].widget  accept  "x/sqrt(x^2+1)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits/l10-inside-function.json .screens[6].widget  accept  "2x/(2sqrt(x^2+1))"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits/l11-standard-derivatives.json .screens[8].widget  accept  "-2x*exp(-x^2)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits/l19-running-backwards.json .quiz[1].widget  accept  "1/sqrt(4-x^2)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits/l19-running-backwards.json .quiz[1].widget  accept  "1/(2*sqrt(1-x^2/4))"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits/l20-which-way-it-bends.json .screens[11].widget  accept  "(x^2-1)*exp(-x^2/2)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits/l20-which-way-it-bends.json .screens[11].widget  accept  "-(1-x^2)exp(-x^2/2)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits-thm/homework-2.json .items[0].widget  accept  "exp(-x/3)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits-thm/homework-4.json .items[8].widget  accept  "(1-p+p*exp(t))^n"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits-thm/l14-joint-densities.json .screens[3].widget  accept  "exp(-x)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits-thm/l17-smallest-and-largest.json .screens[1].widget  accept  "exp(-0.1t)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits-thm/l17-smallest-and-largest.json .screens[1].widget  accept  "exp(-0.1*t)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits-thm/l17-smallest-and-largest.json .screens[1].widget  accept  "exp(-t/10)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits-thm/l19-generating-functions.json .screens[3].widget  accept  "(0.7+0.3exp(t))^3"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits-thm/l19-generating-functions.json .screens[3].widget  accept  "(0.7+0.3*exp(t))^3"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits-thm/l6-uniform-exponential.json .screens[4].widget  accept  "exp(-2t)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/limits-thm/l6-uniform-exponential.json .screens[4].widget  accept  "exp(-2*t)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/measure-prob/homework-1.json .items[5].widget  accept  "1-exp(-r*x)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/multivar/homework-1.json .items[4].widget  accept  "(t^2+2t)exp(t)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/multivar/l2-slicing.json .screens[4].widget  accept  "y*exp(x*y)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
DEAD    content/courses/numerics/l2-cancellation.json .screens[7].widget  accept  "2sqrt(epsilon c/m)"  [the intended value was refused before the fix (the entry took a different value)]
DEAD    content/courses/numerics/l2-cancellation.json .screens[7].widget  accept  "sqrt(4 epsilon c/m)"  [the intended value was refused before the fix (the entry took a different value)]
DEAD    content/courses/numerics/l2-cancellation.json .screens[7].widget  accept  "2*sqrt(epsilon*c/m)"  [the intended value was refused before the fix (the entry took a different value)]
CHANGED content/courses/odes/homework-3.json .items[5].widget  accept  "-1/4+sqrt(5)/4*i"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
STILL-DEAD content/courses/odes/homework-4.json .items[2].widget  accept  "2e^(-t)cos(2t)+0.5e^(-t)sin(2t)"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
STILL-DEAD content/courses/odes/homework-4.json .items[2].widget  accept  "e^(-t)(2cos(2t)+sin(2t)/2)"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
CHANGED content/courses/odes/l13-linearising.json .screens[3].widget  accept  "sqrt(3)/2*i"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
STILL-DEAD content/courses/odes/l15-solving-with-laplace.json .screens[4].widget  accept  "e^(-t)*cos(2t)+0.5*e^(-t)*sin(2t)"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
STILL-DEAD content/courses/odes/l15-solving-with-laplace.json .screens[4].widget  accept  "e^(-t)(cos(2t)+sin(2t)/2)"  [did not parse before the fix; and the entry still does not read after the fix (a text-mode spelling such as ** or e^(..) that is not LaTeX; content to repair)]
CHANGED content/courses/testing/homework-1.json .items[2].widget  accept  "2sqrt(n)(x-0.5)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/testing/homework-1.json .items[2].widget  accept  "2*sqrt(n)*(x-0.5)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/testing/homework-1.json .items[2].widget  accept  "(x-0.5)/(0.5/sqrt(n))"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/testing/homework-1.json .items[2].widget  accept  "sqrt(n)(2x-1)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/testing/homework-1.json .items[2].widget  accept  "(2x-1)sqrt(n)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/testing/homework-1.json .items[2].widget  accept  "2sqrt(n)(x-1/2)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/testing/homework-1.json .items[2].widget  accept  "2*sqrt(n)*x-sqrt(n)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
same    content/courses/trees/homework-3.json .items[1].widget  accept  "sigma*sqrt(T)/2"
same    content/courses/trees/homework-3.json .items[1].widget  accept  "(sigma*sqrt(T))/2"
same    content/courses/trees/homework-3.json .items[1].widget  accept  "0.5*sigma*sqrt(T)"
CHANGED content/courses/trig/homework-1.json .items[4].widget  accept  "15+5sqrt(3)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/trig/homework-1.json .items[4].widget  accept  "15+5*sqrt(3)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/trig/homework-1.json .items[4].widget  accept  "5(3+sqrt(3))"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/trig/homework-1.json .items[4].widget  accept  "5*(3+sqrt(3))"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/trig/homework-1.json .items[4].widget  accept  "5sqrt(3)+15"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/trig/l4-exact-values.json .screens[2].widget  accept  "sqrt(2)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/trig/l4-exact-values.json .screens[4].widget  accept  "sqrt(3)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/trig/review-1.json .items[7].widget  accept  "3sqrt(3)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/trig/review-1.json .items[7].widget  accept  "3*sqrt(3)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/courses/trig/review-1.json .items[7].widget  accept  "sqrt(27)"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
CHANGED content/exams/topic-1.11.json .items[7].widget  accept  "e^x sin(y) - x^2 + y^2"  [the entry took a different (wrong) value before the fix; the intended value was accepted by another form]
```

STILL-DEAD entries to repair by the content owners: integrals homework-2 item 0 (nine accepts), integrals l9-undo-chain (`sin(x²)`, `sin(x**2)`, `ln(x**2+1)`, `sin(x³)`, `sin(x**3)`), odes homework-4 item 2 and odes l15-solving-with-laplace screen 4 (`e^(-t)` forms). Their canonical `answer` still grades, so no learner is blocked.

**837 stock-key lines.** A generated item answered with key `length`, `form` or `count` shows that key's line and then the solution steps (`notYetLine` in `js/engine/player.js`). `tools/test-answer-forms.mjs` runs the real player on a generated item for each of the three keys and an ordinary wrong answer (it fails without the fix). The playthrough fixture gains a vector family (`vector-sum`).

## Group 2 (authoring reach, section 16 of AUTHORING)

- **838** `let` and `where`: `ln`, `log10`, `exp`, `sin`, `cos`, `tan` (radians), `pi`, lazy `if(cond, a, b)`; a `where` on vars alone is tested before the lets; a `let` that divides by zero rejects the draw with no error.
- **839** `wrong[].when`: offered only on draws where it holds; the validator and tests read the drawn list, so "wrong equals answer" respects it. Static check of the condition.
- **840** formats `cfrac`, `+cfrac`, `(frac)`, `sfN`, `+sfN`; placeholders `mono(v; c, k)` and `falling(n; r)`; `poly` already wrote no power of 1; the surd text var of `poly` documented.
- **841** `form: "fraction"` and `form: "exact-angle"` (a new form; `simplified` is unchanged), read from the typed text, default lines, validator enum.
- Tests: `tools/test-fluency-reach.mjs` (140 cases, plain node), `test-answer-forms` part 4b and widget cases, `test-fluency` (the let division case changed to the new rule), `test-validate-fluency` (three cases added). Fixture `tools/fixtures/fluency/fluency-l1-letters-for-numbers.json`: nine families (`fraction-lowest`, `exact-angle`, `mono-derivative`, `log-significant`, `height-with-sine`, `divide-reject`, `falling-product`, `fractional-coefficient`, `vector-sum`); the old fixture is untouched.

## Existing content unchanged

A digest of all 141 families of the 46 real sets on seeds 1 to 200 (items, answers, wrongs, solutions, reject counts) and of one attempt per set is identical before and after (`4665dd192ae9d1975c7be5b49287e0ab`). The ten `docs/reports/fluency-*-numbers.py` scripts pass (counting 4200, equations 2600, exp-log 18800, integrals 22400, limits 14000, multivar 3800, quadratics 25400, series 11600, taylor 4800, trig 20000 checks, 0 failures). `test-expr-equations --audit` output identical.

## Verification

Validator 0 errors (4110 warnings, none in the new fixture; manifest unchanged); `readiness-sums.mjs` OK; every `tools/test-*` green including `test-cumulative` (26 of 26), `test-fluency` (892 of 892), `test-validate-fluency` (43 of 43), `test-answer-forms` (306 of 306), `test-expr-equations` (146 of 146). Playthrough, desktop and `--mobile`: `--fluency` on both fixtures, `trig/fluency-l4-exact-values`, `exp-log/fluency-l8-solving-for-the-power` (desktop also `quadratics/fluency-l1-two-brackets`); lessons `integrals/l9-undo-chain`, `integrals/l10-undo-product`, `numerics/l2-cancellation` (desktop also `odes/l15-solving-with-laplace`); `--routes-only`. All passed.

## Deferred

- The full `playthrough --all` run (too long for a foreground call; the four shards are the main session's).
- `log(x, b)`, `asin`, `acos`, `atan`, a constant `e` and a degree form of the trigonometric functions in `let` (not in the brief of this pass).
- A numeric `tol` stated as half a unit in the last significant figure (authors write `abs`, documented).
- The 18 STILL-DEAD text-mode `accept` spellings above (content).
- A per-value `form` for set answers (from pass 830 to 834) and `form` on `numeric` (`exact: true`) remain open.
