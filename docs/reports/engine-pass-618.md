# Engine pass 618 (expression grader and equations)

Cause: `ZQ.grade.exprEqual` parsed `n=5` and `n=a/(c-b)` as Compute Engine `Equal` terms and compared them as truth values, so any two equations matched. A leading `n =` was never stripped.

Fix (`app/js/engine/grade.js`): `splitRel` plus a proportional-difference comparison in `scalarEqual` (`prop` mode). See ENGINE-BACKLOG 618 and 619 and AUTHORING (expression widget).

Audit: 520 expression widgets; none has `=`, `<`, `>`, `\le` or `\ge` in `answer`, `accept` or `wrong[].tex`; none accepted a wrong equation. No content change needed. (Other `tex` strings with `=` belong to derive and step widgets, which do not call `exprEqual`.)

Test: `app/tools/test-expr-equations.mjs`, 37 checks pass; against the old grader (`--grade`) 14 fail.
