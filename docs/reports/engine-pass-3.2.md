# Engine pass 3.2: expression grader (items 501 and 502)

Source: `docs/reviews/review-briefs-3.2.md`, "[Must] engine requirements". Compute Engine 0.30.2, loaded from the local packages in the session scratchpad (`pkgs`). Test scripts: `h.cjs` (loads `grade.js` and the engine under Node), `t.cjs`, `p.cjs` in the scratchpad.

## 501 P32-expr-exp

Change: `unexp()` in `prep()` (`app/js/engine/grade.js`). `\exp`, `\operatorname{exp}` and `\mathrm{exp}` followed by `(..)`, `\left(..\right)`, `[..]`, `{..}` or one token become `\left(\exponentialE^{(arg)}\right)`, innermost last, so `\exp(x)^2` and `\exp(x)\exp(y)` stay valid. `prep()` feeds `exprEqual`, `exprEqualUpToConstant`, `exprShape`, `exprShapeLine` and the widget's `form` check, so exam items (same widget) are covered. Validator: warning on `\exp`, `\operatorname{exp}` or `\mathrm{exp}` in an authored `answer` or `accept`.

Before (old `grade.js`, input first, target second), all false: `\exp(x)` / `e^{x}`; `\exp\left(x\right)` / `e^{x}`; `\exp x` / `e^{x}`; `e^{x}` / `\exp(x)`; `\exp\left(\theta x-\frac{\theta^2}{2}\right)` / `e^{\theta x-\theta^2/2}`; `S_0\exp(\sigma W_T)` / `S_0e^{\sigma W_T}`; `\mathrm{exp}{x+1}` / `e^{x+1}`; the power payoff `S_0^n\exp(n(r-0.5\sigma^2)T+n^2\sigma^2T/2)` against its `e^{...}` form.
After: all true. `\exp(W)` / `\exp(W)` true; `\exp(x)` / `e^{2x}` false; `\exp(n(r-0.5\sigma^2)T)` against `e^{n(r-\sigma^2/2)T+1}` false.

## 502 P32-expr-callhead

Change: `uncall()` in `prep()` inserts `\cdot ` between a lone Latin or Greek letter (optional `_` and `^` part) and a following `(` or `\left(`, unless the letter is in the screen's new `functions` list (`"functions": ["f", "\\sigma"]`, passed from `expression.js` as `{ functions }` to `exprEqual`, `exprEqualUpToConstant`, `exprShapeLine` and the new `ZQ.grade.withParsed`). `scoped()` runs every comparison and the form check between `ce.pushScope()` and `ce.popScope()`, so declarations the engine makes while parsing do not outlive the call. The validator errors on a malformed `functions`. The form check in the widget now parses through `withParsed` (prepared text), so `r(1-x)` counts as a product with a bracketed sum there too.

Before, all false: `r(1-x)` / `r-rx`; `r(1-x)` / `r\cdot(1-x)`; `K(v_x-v_y)` / `Kv_x-Kv_y`; `k(1-r)` / `k\cdot(1-r)`; `n(r-0.5\sigma^2)T` / `n(r-\sigma^2/2)T`. (`\sigma(S+1)` / `\sigma S+\sigma` already passed in this order on a fresh engine; it is in the after list.) Pollution reproduced on one shared engine: after `f(x)` is parsed, `2f` / `f+f` is false.
After, all true, including `\sigma(S+1)` / `\sigma S+\sigma`, then on the same engine `2x` / `x+x` and `x^2` / `x\cdot x`; `2f` / `f+f` after `f(x)` (declared in `functions`) true.

## Regression (Node harness, 37 + 17 cases, 0 failures except one pre-existing)

Still right: `e^{x+y}` / `e^xe^y`; `\exp(x)\exp(y)` / `e^{x+y}`; `3+4i` / `4i+3`; `1+i` / `i+1`; `i(1+i)` / `i-1`; `e^{i\theta}` and `\exp(i\theta)` against `\cos\theta+i\sin\theta`; `\exp(i\pi)` / `-1`; `(1,2,3)` / `(1,2,3)`; a pmatrix column against `(1,2)`; `\sin(x)` / `\sin x`; `\ln(x)` / `\ln x`; `x^2(x+1)` / `x^3+x^2`; `f(x)` / `f(x)` with `f` declared; `N(0,1)` / `N(0,1)`. Still wrong: `r(1-x)` / `r-x`; `r(1+x)` / `r-rx`; `\sin(x)` / `\cos(x)`; `(1,2,3)` / `(1,2,4)`; `f(x)` / `f(y)`.
Pre-existing, unchanged: `f(x)+1` against itself with `f` declared is false in the comparison (no numeric value, and the symbolic check of an undefined function says no); the widget's plain-text fallback (`normExpr`) still accepts identical text.

## Validator scratch test

A hidden sample review (`review-sample-zz`, since deleted) with `answer: "\\exp(x)"` and `functions: ["ff"]` gave one warning ("write e^{...} in an authored answer") and one error (the `functions` shape), plus its own items-count error.

## Checks

- `node tools/validate.mjs`: 0 errors (537 warnings, none new).
- `node tools/playthrough.mjs --routes-only --local-cdn <pkgs>`: all passed.
- Lessons with `--local-cdn`: `integrals/l9-undo-chain` (5 expression screens, 13 checks, quiz 4/4), `linear-maps/l8-maps-as-matrices` (15 checks, quiz 4/4), `analysis/l15-epsilon-delta` (17 checks, quiz 5/5): all ok.
- Full `--all --local-cdn`: see the final line below.

## Files

`app/js/engine/grade.js`, `app/js/engine/widgets/expression.js`, `app/tools/validate.mjs`, `docs/AUTHORING.md` (section 3, new paragraph before "Complex answers"), `docs/ENGINE-BACKLOG.md` (items 501, 502 and status block), `docs/BACKLOG-INBOX.md` (two bullets and their heading removed), this report. No content JSON changed.

## Full run

The unabridged `--all` run (1,001 lessons, 465 sets, 40 exams, about 3 hours) was not completed: a first attempt was stopped by me after about 94 lessons, all ok, because it could not finish in the session. In its place, every lesson, review, homework set and exam whose JSON contains an `expression` widget (195 files, samples excluded) was played with `--lesson`, `--set` and `--exam` and `--local-cdn`: 195 ok, 0 FAIL, "All passed". The change touches only the expression grader, the expression widget and the validator, so lessons without an expression widget cannot be affected. The orchestrator may still run `--all` in a long session.

## 503 P32-expr-int

Source: `docs/reviews/answers-3.2-pdes-2.md`, worst finding. `\frac{2(1-(-1)^k)}{k\pi}` is undefined at the grader's non-integer sample points, so equivalent forms such as `\frac{2(1-\cos k\pi)}{k\pi}` failed.

Change: optional `integers: ["k"]` on the `expression` widget (`js/engine/widgets/expression.js` passes it in `opts` beside `functions`). In `js/engine/grade.js`, `scalarEqual` samples each listed symbol at six distinct whole numbers from 1 to 9, a fixed shuffle per symbol (own generator, so two integer symbols differ and the draws for every other symbol and for expressions without `integers` are unchanged); other symbols keep 0.3 to 3. `exprEqualUpToConstant` honours it too. Comparison keeps the 1e-9 relative tolerance, which covers `\cos(k\pi)` rounding (about 1e-16). Exam and bank items use the same widget. The factorial path (24 whole-number points) is untouched.

Validator: error when `integers` is not a list of single Latin letters or Greek commands; warning when an authored `answer` or `accept` contains `(-1)^k` or `(-1)^{k...}` and that symbol is not in `integers`. Documented in `docs/AUTHORING.md` section 3 (paragraph "Whole-number symbols") and `docs/ENGINE-BACKLOG.md` (item 503).

Before and after (Node harness, Compute Engine 0.30.2, input / target `\frac{2(1-(-1)^k)}{k\pi}`):
- Without `integers`: `\frac{2(1-\cos k\pi)}{k\pi}` false, `\frac{2(1-\cos(k\pi))}{k\pi}` false (wrong); `\frac{2-2(-1)^k}{k\pi}` and `\frac{2(1-(-1)^{k})}{\pi k}` true (both sides undefined, symbolic check); `\frac{4}{k\pi}`, `\frac{2(1+(-1)^k)}{k\pi}` false.
- With `integers: ["k"]`: the four equivalent forms true; `\frac{4}{k\pi}` and `\frac{2(1+(-1)^k)}{k\pi}` false. Also `\sin\frac{k\pi}{2}` equals `\sin\frac{\pi k}{2}`, not `\cos\frac{k\pi}{2}`; `x+k` is not `x+k+1`; mixed `x` stays at 0.3 to 3.

Regression: all 37 cases of items 501 and 502 re-run without `integers` (script `t-reg.cjs` in the scratchpad): 0 failures, same results as above. Validator scratch test on a temporary edit of `pdes/l6-fourier-series` (restored): `integers: ["k"]` removes the warnings, `["k", "kk"]` and `"k"` each give the error.

Checks: `node tools/validate.mjs`: 0 errors. New warnings from the `(-1)^k` rule in existing content: `content/courses/pdes/l6-fourier-series.json` screens[3] (`answer`, `accept[0]`, `accept[1]`, all `(-1)^{k}`); no other file. Not edited (content agents add `"integers": ["k"]`). `--routes-only --local-cdn`: all passed. Playthroughs with `--local-cdn`: `integrals/l9-undo-chain`, `linear-maps/l8-maps-as-matrices`, `analysis/l15-epsilon-delta`, `pdes/l6-fourier-series`: all passed.
Files: `app/js/engine/grade.js`, `app/js/engine/widgets/expression.js`, `app/tools/validate.mjs`, `docs/AUTHORING.md`, `docs/ENGINE-BACKLOG.md`, this report.

## 514 P32-expr-D

Source: `docs/reviews/review-pdes.md`. Compute Engine 0.30.2 reads `D` and `N` as operators: `Dt` is `["Tuple","D","t"]`, `4Dt` is `["Tuple",4,"D","t"]`, `tD` is `["Tuple","t","D"]`, `D\cdot t` is an error. Every other capital letter before a letter is a product (checked A to Z with `t`; `G` is the Catalan constant, a number, so it still compares correctly on both sides). `d` is a product. `\partial t` is `["Tuple",["PartialDerivative"],"t"]`, `\frac{d}{dt}f` a nonsense product, `\frac{\partial}{\partial t}u` an error: derivative typing is unsupported by the grader before and after, and left alone.

Change: in `prep()` the old rule (`D` or `N` not followed by a letter, not preceded by a letter or backslash) is replaced by one rule: every `D` or `N` that is not inside a command name (`\Delta`) and not the first letter of a `\mathrm{..}`, `\mathbb{..}`, `\text{..}`, `\operatorname{..}` group becomes `\mathrm{D}` or `\mathrm{N}`. `functions: ["D"]` keeps the operator reading before a letter. `prep()` feeds every comparison, so exams and banks are covered.

Before (old grader, all false): `\sqrt{2Dt}` / `\sqrt{2tD}`; `\sqrt{2Dt}` / `\sqrt{2}\sqrt{D}\sqrt{t}`; `4Dt` / `4tD`; `4Dt` / `2D\cdot 2t`; `\frac{x^2}{4Dt}` / `\frac{x^2}{4tD}`; `Dx` / `xD`; `DT` / `TD`. Identical text (`Dt` / `Dt`) passed.
After: all true; `2Dt` / `4Dt` false; `\partial t` / `t` false.

Regression (Node harness, scripts `tReg2.cjs`, `tInt2.cjs`, `t2.cjs` in the scratchpad): the 37 cases of items 501 and 502 and the item 503 cases give the same results as recorded above (0 failures; the pre-existing `f(x)+1` and the two documented without-`integers` cases only).

Content scan (answer and accept keys of 307 `expression` widgets, all courses, exams and banks; no content edited): only `content/courses/pdes/l2-heat-equation.json`, screen index 5 (`screens.5.widget`), keys `-\frac{1}{2t}+\frac{x^2}{4Dt^2}`, `-1/(2t)+x^2/(4Dt^2)` and `x^2/(4Dt^2)-1/(2t)`; the old grader parsed them as tuples, so only identical text passed. `mental-pressure/l11-word-problems` screen 8 has `Prm/1200` (multi-letter symbol, unaffected by this rule).

Checks: `node tools/validate.mjs`: 0 errors (541 warnings). `--routes-only --local-cdn`: all passed. Playthroughs with `--local-cdn`: `pdes/l2-heat-equation`, `integrals/l9-undo-chain`, `analysis/l15-epsilon-delta`: all passed. The full `--all` run was not repeated (same reasoning as above: grader-only change).
Files: `app/js/engine/grade.js`, `docs/AUTHORING.md`, `docs/ENGINE-BACKLOG.md`, this report. The validator needed no rule.
