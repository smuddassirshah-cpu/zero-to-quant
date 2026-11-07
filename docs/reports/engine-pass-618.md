# Engine pass 618 (expression grader and equations)

Cause: `ZQ.grade.exprEqual` parsed `n=5` and `n=a/(c-b)` as Compute Engine `Equal` terms and compared them as truth values, so any two equations matched. A leading `n =` was never stripped.

Fix (`app/js/engine/grade.js`): `splitRel` plus a proportional-difference comparison in `scalarEqual` (`prop` mode). See ENGINE-BACKLOG 618 and 619 and AUTHORING (expression widget).

Audit: 520 expression widgets; none has `=`, `<`, `>`, `\le` or `\ge` in `answer`, `accept` or `wrong[].tex`; none accepted a wrong equation. No content change needed. (Other `tex` strings with `=` belong to derive and step widgets, which do not call `exprEqual`.)

Test: `app/tools/test-expr-equations.mjs`, 37 checks pass; against the old grader (`--grade`) 14 fail.

## Follow-up: item 620 (left-hand labels)

Cause: the 619 strip accepted only a single (subscripted) symbol, so `f(k)=4k+1`, `S_\infty=...`, `u_{n+1}=...`, `(x+3)^3=x^3+...` and `OB=\sqrt{2}` got the generic line. Fix in `app/js/engine/grade.js` (`isLabel`, `CALLSYM`, `nameFree`, and the restated-expression branch in `exprEqualIn`); see ENGINE-BACKLOG 620 and AUTHORING.

Test: `app/tools/test-expr-equations.mjs` 129 checks pass; on the 619 grader 40 fail. It covers the real items series homework-2 items[0], l11 screens[2], homework-3 items[0] and trig l4 screens[2] and [4]. The restated-expression slips (`(x+3)^3 = x^3+27`) get the generic line, by design.

Audit (functions and series, 20 expression widgets, answer typed as `y=`, `f(x)=`, `u_n=`, `a_n=`): every prefix now passes for all 20 (`f(x)=` passed 0 of 20 before; the others 20); no wrong[] value with a `y=` prefix equals an answer.
