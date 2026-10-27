# Engine breadth pass 2: grading (items 429, 430, 433, 434, 437)

Files changed (all in the owned set): `app/js/engine/grade.js`, `app/js/engine/widgets/expression.js`, `app/js/engine/widgets/order.js`, `app/js/engine/widgets/code.js`, `app/js/engine/widgets/cpp-grade.js`. The Python and C++ harnesses are template strings inside `code.js` (`JUDGE`) and `cpp-grade.js` (`LIB`, `TESTKIT`), so no other file holds harness source. `app/js/screens/drill.js` has its own separate Python `isclose` (floats only); it is not touched and would need the same cmath branch if drills ever return complex values.

Scratch work: `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/grading/` (`t6.cjs`, `t7.cjs` grader unit cases in node against the real Compute Engine 0.30.2; `reg.cjs` old-against-new comparison; `pw.mjs` Playwright gallery tests and screenshots; `app/` the scratch copy with the gallery examples and a scratch lesson `contests/l99-scratch`; `validate-patch.diff`; `gallery-extras.txt`).

## Item 429: complex values in `expression`

What changed (`grade.js`, `exprEqual`): if either side has an `i` (also `\mathrm{i}`, `\imaginaryI`; not in a subscript), both sides are rewritten with `i` as the symbol `\iota` and `\bar{` as `\overline{`, and the numeric test uses our own complex evaluator over the engine's MathJSON (`cxEval`: Add, Multiply, Divide, Power, Sqrt, Root, Exp, Ln, Log, Sin, Cos, Tan, Sinh, Cosh, Tanh, Abs, Conjugate, OverBar, Re, Im, Arg, constants) with `\iota` bound to 0 + 1i. Real and imaginary parts are both compared (relative 1e-9) at every seeded point (6 points, free symbols still real in 0.3 to 3). The rewrite is needed because the engine folds `1/(1+i)` into a wrong constant at parse time; with `i` as a symbol it stays an expression and our division is exact. A function the evaluator does not know falls back to the engine's `N()` with `\iota` as `Complex(0,1)`. Without an `i` on either side the path is the old one (real part of `N()`), so real-only grading is unchanged: `reg.cjs` compared old and new `exprEqual` over every answer, accept form and wrong form of all 195 expression widgets in `app/content` (1,837 pairs): 0 differences.

How checked: `t6.cjs`/`t7.cjs`: `1/(1+i)` = `(1-i)/2` accepted, `3-4i` rejected for `3+4i`, `0` and `-2i` rejected for `(1+i)^2` while `2i` passes, `e^{i\theta}` = `\cos\theta + i\sin\theta` but not `\cos\theta - i\sin\theta`, `(3+4i)/(1+2i)`, `i^3 = -i`, `\sqrt{-4} = 2i` not `-2i`, `e^{i\pi} = -1`, `|3+4i| = 5`, `\overline{3+4i}`, `x+iy` against `x-iy`, `1/(x+iy)` against `(x-iy)/(x^2+y^2)`, `\cosh(ix) = \cos x`, `\sin(ix) = i\sinh x`, an unsupported function (`\arcsin x + i`) through the fallback. In the browser (`pw.mjs`, real MathLive and Compute Engine): the same on the real widget plus typing into the gallery card.

Known limit: free symbols are real, so `\bar{z}` for a symbol `z` is `z`; write `x + iy`. A real answer that uses `i` as an index or variable is now read as the imaginary unit and both parts compared (before, only the real part). The one place in content that does this is `markov/homework-3` (`i(20-i)`, `20i-i^2`, ...): those pairs are identical polynomials and still grade as before (checked in `reg.cjs`); authors should use another letter.

## Item 430: complex `isclose` (Python and C++)

Python (`code.js`, `JUDGE.__zq_cmp`): before the `float()` attempt, if either value is a Python `complex`, a NumPy `complex128` (a `complex` subclass) or any type whose name starts with `complex` (`complex64`), compare with `cmath.isclose(complex(x), complex(y), rel_tol, abs_tol)`; the tolerances are the case's `tol` or the old defaults (rel 1e-9, abs 1e-12). Real values take the unchanged `math.isclose` branch. NumPy arrays already go through `tolist()` and the recursive compare, so a complex array compares element by element. Checked in Pyodide 0.27.7 (`pw.mjs`, 12 cases): complex against complex, wrong sign, complex array right and wrong, `np.complex128`, `np.complex64`, complex against a real expect (3-4j against 3 fails, `1+0j` passes for 1), per-case `tol` abs 0.001 passing 0.5001 against 0.5, default tolerance failing it, `equal` on complex.

C++ (`cpp-grade.js`): the harness `put` prints any type with `.real()` and `.imag()` (so `std::complex<double>`, `<float>`, and a vector of them) as `{"re":..,"im":..}`; before, a complex return value was reported as unprintable. The JS compare treats `{ re, im }` as a complex number: `isclose` uses `|a - e| <= max(rel * max(|a|, |e|), abs)` with the existing defaults (rel 1e-9, abs 1e-12, the same as for real values) or the case's `tol`; `equal` compares both parts exactly; a plain number as `expect` means imaginary part 0; the actual column reads `(5,5)` like `std::complex` output. The testkit's `CHECK_CLOSE(a, b, tol)` now takes real or complex arguments (distance in the plane, same message for reals). Checked in YoWASP clang 21 (`pw.mjs`): complex product, a wrong (sum) function failing, `-1` as a real expect for `i*i`, a double result, a vector of complex roots right and wrong, `std::complex<float>`, tol abs 0.01 passing 5.001 against 5, default failing it, testkit with complex `CHECK_CLOSE` pass and fail.

Per-test `tol` already existed for both languages (items 378, 425, 442); nothing new to add.

## Item 433: vector and matrix answers in one `expression`

What changed (`grade.js`): `exprEqual` reads a Tuple, List or Matrix from the engine's MathJSON (after turning `\langle ... \rangle` into brackets) and compares entry by entry, each entry by the same seeded-point method (complex entries work). A column (`pmatrix`, `bmatrix`), a row and `(a, b, c)` are one vector; a matrix with rows and columns compares entry by entry and needs the same shape. New `exprShape` and `exprShapeLine`; `expression.js` returns key `length` and a line when a wrong-size answer is typed ("Your answer has 2 components. The answer has 3 components." / "That is a single value. The answer has 3 components." / "The answer is a single value, not a vector." / "... rows and ... columns"), after `wrong[]` has been tried. An unparsable input gets no length line.

How checked: `t6.cjs` (tuple against pmatrix, `\left(...\right)`, brackets, `\langle`, wrong entry, wrong length, scalar against vector, symbolic entries `(x+1, 2y)` against `(1+x, y+y)`, 2 by 2 matrix right, wrong and as a flat list, complex entries) and `pw.mjs` in the real widget (the gallery card shows the line and key).

## Item 434: `order` distractors (and `same`)

`same` groups already existed (item 201, `order.js`, validator and AUTHORING.md `### order`), so nothing was added for them; `pw.mjs` re-checks them (swapping the two interchangeable lines passes, moving a fixed line fails). New: `"distractors": ["d1", "d2"]` lists the ids of lines that must be left out; `answer` lists only the lines that belong. Every line then has a cross button (and Delete on a focused line) that moves it to a "Left out" list under the sequence, with a plus to put it back at the end; the buttons give way to the marks after grading. Grading: all and only the right lines in the right order (with `same` as before) is correct; a distractor in the sequence returns its id as the key and its `why` (if the line has one) as the default line; a needed line left out returns key `left-out`; otherwise the first misplaced line's id as before. A left-out distractor shows a tick, a left-out needed line a cross. `value()`/`set()` carry the sequence only, so the test hook's `answerCorrect` (`set(answer)`) leaves every other line out. Without `distractors` the widget behaves as before. No CSS file was touched: the new parts use existing classes with a few inline styles; they can move into `widgets.css` if preferred.

How checked: `pw.mjs` direct grading (right, distractor used with and without `why`, needed line left out, wrong sequence, `same`, plain order unchanged) and the gallery card (cross, put back, Fill answer, Check right and wrong, Reset), screenshots below; the playthrough of every lesson that uses `order` (below).

## Item 437: `\min`, `\max`, capital N and D, `\epsilon`

`grade.js` `prep()` rewrites both sides before the engine parses them: `\min(a,b,...)` and `\max(...)` (also `\operatorname{min}`, `\left(`, `[`, `\{`) become `\left(\frac{(a)+(b)-|(a)-(b)|}{2}\right)`, folded for more arguments (the engine's own `Min` cannot be added to or multiplied: `\max(a,b)+1` is invalid in 0.30.2); a lone capital `N` or `D` (not after a letter or backslash, not inside `\mathbb{}`, `\mathrm{}` and the like) becomes `\mathrm{N}`, an ordinary symbol; `\epsilon`, `ε` and `ϵ` become `\varepsilon`. The text fallback `normExpr` also folds `varepsilon` and the Unicode letters into `epsilon`. `exprEqualUpToConstant` uses the same `prep`. Limit (unchanged, seeded points are 0.3 to 3): a switch at 0 or below cannot be told from its absence, so `\max(0, x)` passes for `x`, as `|x|` does.

How checked: `t6.cjs` (min against max, min plus 1, `2\min(x,1)`, `x\min(x,1)`, three arguments, braces, `\operatorname`, nested min and max, `N^2+1`, `N(N+1)/2`, `\binom{N}{2}`, `D^2`, `n` against `N` rejected, `\epsilon` against `\varepsilon`, `\delta` rejected, `+C` with N) and the 1,837-pair regression above.

## Regression

- `node tools/validate.mjs` (from `app/`): 0 errors (365 warnings, as before).
- `node tools/playthrough.mjs --lesson ... --local-cdn <pkgs>` on the repository app (the final grading files, with the other agents' canvas work in the tree): every written lesson that uses `order` or `expression` (461 with `order`, 67 with `expression`, 486 distinct): 486 of 486 ok, 0 failures (two runs of 243). 26 lessons that use `code` (18 Python and 8 C++, a seeded random sample): 26 of 26 ok. 39 reviews and homework sets (16 with `order`, 16 with `expression`, 6 Python code, 3 C++, including `markov/homework-3`, whose `i` is a real variable): 39 of 39 ok, "All passed".
- Old against new `exprEqual` over every expression widget in `app/content` (answer, accept forms, wrong forms, cross pairs; 1,837 pairs): 0 differences.
- Scratch copy: scratch lesson `contests/l99-scratch` (a complex expression, a vector expression, `\min` with N, an order with distractors, Python and C++ complex code) plays through with its authored answers: 10 checks ok. `tools/playthrough.mjs --routes-only --shots --mobile` on the scratch copy (gallery with the new examples): all passed, no console errors.
- Not run: the full `--all` suite and the exams (the integration agent runs them).

## Notes for the integration agent

- With `distractors` the starting list is every line shuffled (without them, as before, the answer lines shuffled). The `ctx.change` payload of `order` gained `out` (the left-out ids). `exam.js` line 38 prints the answer lines only, which is right for distractors.
- `player.js` `answerWrong` (playthrough `--why`) makes no wrong answer for `order` or `expression`; nothing to add.
- `app/js/screens/drill.js` keeps its own float-only `isclose` (see the top).
- `D` was folded into the capital-letter fix next to `N` because the validator warned about both; remove the whole warning, as in the patch.

## Shared-file changes (for the integration agent)

### 1. `app/tools/validate.mjs`

Tested on the scratch copy against a scratch lesson (the unified diff against the repository file is `validate-patch.diff` beside the scratch folder; applied there the lesson passes every rule except its own screen count). Spec:

- C++ value cases: `expect` may be a complex `{ re, im }` (two finite numbers), alone or inside a list, including with `compare: "isclose"`. Add `cppComplex`, `cppExpect` and let `cppNumbers` accept `cppComplex`; the error text becomes "expect is a number, a boolean, a string, a complex { re, im } or a list of those".
- `order`: `distractors` (optional) is a non-empty list of known line ids, each once, else an error on `.distractors`; with it, `answer` must be a permutation of the line ids that are not distractors (message "answer must be a permutation of the line ids that are not distractors"); the `byKey` keys then include `left-out` (every distractor id is already a line id, so already a key).
- `expression`: drop the warning for a capital N or D (they grade now). If `answer` looks like a vector or matrix (`/^\s*(\\left\s*)?[(\[][^]*,|\\begin\{[pbv]?matrix\}/`), add `length` to the allowed `byKey` keys.

Patch:

```diff
@@ -88,8 +88,11 @@
 const CPP_TYPES = [...];
+/* engine pass (item 430): a std::complex result is expected as { re, im } (alone, or inside a list) */
+const cppComplex = (v) => !!v && typeof v === 'object' && !Array.isArray(v) && Object.keys(v).length === 2 && Number.isFinite(v.re) && Number.isFinite(v.im);
+const cppExpect = (v) => cppValue(v) || cppComplex(v) || (Array.isArray(v) && v.every(cppExpect));
 const cppValue = (v) => (typeof v === 'number' && Number.isFinite(v)) || typeof v === 'boolean' || typeof v === 'string' || (Array.isArray(v) && v.every(cppValue));
-const cppNumbers = (v) => (typeof v === 'number' && Number.isFinite(v)) || (Array.isArray(v) && v.every(cppNumbers));
+const cppNumbers = (v) => (typeof v === 'number' && Number.isFinite(v)) || cppComplex(v) || (Array.isArray(v) && v.every(cppNumbers));
@@ -143,7 +146,7 @@
-      else if (!cppValue(t.expect)) err(file, `${at}.expect`, 'expect is a number, a boolean, a string or a list of those');
+      else if (!cppExpect(t.expect)) err(file, `${at}.expect`, 'expect is a number, a boolean, a string, a complex { re, im } or a list of those');
@@ -351,8 +354,8 @@
     case 'expression':
-      /* inbox (validation 3): the Compute Engine reads a lone capital N (and D) as its own functions, so the answer never grades */
-      if (typeof w.answer === 'string' && /(^|[^\\A-Za-z])[ND](?![A-Za-z])/.test(w.answer)) warn(...);
+      /* engine pass (items 433, 437): a capital N or D, \min, \max and \epsilon now grade; a vector or matrix answer has the key "length" for a wrong size */
+      if (typeof w.answer === 'string' && /^\s*(\\left\s*)?[(\[][^]*,|\\begin\{[pbv]?matrix\}/.test(w.answer)) keys.add('length');
@@ -458,7 +461,13 @@
     case 'order': {
-      if (!Array.isArray(a) || a.length !== lines.size || new Set(a).size !== a.length || a.some(x => !lines.has(x))) err(file, `${where}.answer`, 'answer must be a permutation of the line ids');
+      /* engine pass (item 434): distractors lists lines that must be left out; answer is a permutation of the rest */
+      let dis = [];
+      if (w.distractors != null) {
+        if (!Array.isArray(w.distractors) || !w.distractors.length || w.distractors.some(x => !lines.has(x)) || new Set(w.distractors).size !== w.distractors.length) err(file, `${where}.distractors`, 'distractors lists one or more line ids, each once');
+        else { dis = w.distractors; keys.add('left-out'); }
+      }
+      if (!Array.isArray(a) || a.length !== lines.size - dis.length || new Set(a).size !== a.length || a.some(x => !lines.has(x) || dis.includes(x))) err(file, `${where}.answer`, dis.length ? 'answer must be a permutation of the line ids that are not distractors' : 'answer must be a permutation of the line ids');
```

(The exact, complete diff, with context lines, is in `validate-patch.diff`; the three hunks above are its content.)

### 2. `docs/AUTHORING.md`

Section 3, `### expression`, append after the "How equivalence is decided" paragraph:

> **Complex answers.** An `i` in the answer or in the learner's input is the imaginary unit (`\mathrm{i}` too), and the grader compares the real and the imaginary part at every seeded point, so `\frac{1}{1+i}`, `\frac{1-i}{2}` and `0.5-0.5i` agree, `3-4i` fails for `3+4i`, and `0` fails for `(1+i)^2`. Free symbols stay real: write `x + iy`, not `z` and `\bar{z}`. `\overline{...}` and `\bar{...}` are the conjugate, `|z|` the modulus, and `e^{i\theta}` equals `\cos\theta + i\sin\theta`. A real answer must not use a bare `i` as an index or variable; use `k`, `j` or `n`.
>
> **Vectors and matrices.** One widget can take a vector: `"answer": "(2, -1, 3)"` or `\begin{pmatrix}2\\-1\\3\end{pmatrix}`. A column, a row, `(a, b, c)`, `[a, b, c]` and `\langle a, b, c\rangle` are the same vector, each entry is compared by the usual seeded-point test (symbols and complex entries are fine), and a matrix answer (`pmatrix` with rows and columns) is compared entry by entry and needs the same shape. A wrong number of entries returns the key `length` (give it a `byKey` line; the default says "Your answer has 2 components. The answer has 3 components."). `\mathbf{i}, \mathbf{j}, \mathbf{k}` notation is not read: ask for the components.
>
> **`\min`, `\max`, `N`, `\epsilon`.** `\min(a, b)` and `\max(a, b, c)` work anywhere in an answer, also added to or multiplied by something. A capital `N` or `D` is an ordinary symbol. `\epsilon`, `\varepsilon` and ε are one symbol, so list only one form. Seeded points lie between 0.3 and 3, so a switch at 0 or below (`\max(0, x)` against `x`) cannot be told apart.

Section 3, `### order`, append to the last paragraph:

> `"distractors": ["d1", "d2"]` lists lines that must be left out (a flawed proof step, a wrong justification): include them in `lines`, leave them out of `answer`, and give each a `why` (shown as the feedback when the learner uses it). Each line gets a cross that moves it to a "Left out" list. Using a distractor returns its id as the `byKey` key, leaving out a line that belongs returns `left-out`, any other mistake the id of the first misplaced line as before. `same` and `distractors` combine.

Section 3, `### code`, after the compare paragraph (Python):

> `isclose` also compares complex numbers: a function may return a `complex`, a NumPy complex scalar or array, and `expect` is a Python expression such as `(0.5-0.5j)` or `[1+1j, 2-2j]`; the test is `cmath.isclose` with the same `tol` (default relative 1e-9, absolute 1e-12). A real `expect` against a complex result compares as a complex number with imaginary part 0. Without this, split the value in the call (`[w.real, w.imag]`) as before.

C++ addendum (the "Tolerance, flags and variants" bullet or a new bullet):

> **Complex results.** A `std::complex<double>` (or `float`, or a vector of them) can be a function's result; write `expect` as `{ "re": 0.5, "im": -0.5 }`, or a list of those; a plain number means imaginary part 0. `isclose` compares the distance in the plane, `|actual - expected| <= max(rel * max(|actual|, |expected|), abs)` with the case's `tol` (default relative 1e-9, absolute 1e-12); `equal` compares both parts exactly. The failing row reads `(5,5)`, like `std::complex` output. With `"testkit": true`, `CHECK_CLOSE(a, b, tol)` accepts complex values too.

Section 7, new paragraph (validation rules): "Engine pass 2 grading rules. Errors: `order.distractors` that is not a non-empty list of known line ids, each once; with `distractors`, an `order.answer` that is not a permutation of the other lines; a C++ value case `expect` that is not a number, a boolean, a string, a complex `{ re, im }` or a list of those. `byKey` keys: `length` on an `expression` whose answer is a vector or matrix; `left-out` on an `order` with `distractors`. The warning about a capital N or D in an expression answer is gone."

### 3. `docs/ENGINE-BACKLOG.md` status lines (suggested text, items 429, 430, 433, 434, 437)

- 429. Done: `exprEqual` compares real and imaginary parts at every seeded point when an `i` appears (own complex evaluator over MathJSON; `1/(1+i)` = `(1-i)/2`; `3-4i` and `0` rejected); real-only grading unchanged (1,837 pairs identical).
- 430. Done: complex-aware `isclose` in the Python harness (`cmath.isclose`, same tolerances, NumPy complex too) and the C++ harness (`std::complex` printed as `{ re, im }`, `expect: { re, im }`, `CHECK_CLOSE` takes complex); defaults kept (rel 1e-9, abs 1e-12), per-case `tol` already existed.
- 433. Done: one `expression` takes a vector or matrix (`(2, -1, 3)`, a `pmatrix`, `\langle\rangle`), compared entry by entry; wrong size returns key `length` with a line.
- 434. Done: `order` `distractors` (a "Left out" list, keys: distractor ids and `left-out`); `same` groups already existed (item 201).
- 437. Done: `\min`/`\max` (rewritten to (a+b-/+|a-b|)/2), capital `N` and `D`, and `\epsilon` = `\varepsilon` in expression answers (text fallback too).

### 4. `app/js/screens/system.js` gallery examples

Add these to `WIDGET_EXTRAS` (before the C++ entries). The `lazy` line in the widget-card loop should also change, so that a Python code variant loads Pyodide on request like the plain `code` card: `const lazy = kind === 'code' || (!!(item.widget && item.widget.kind === 'code' && item.widget.language !== 'cpp')), cpp = ...`. Optionally show `r.line` after the key in the check output (`... key "length". Your answer has 2 components. ...`), as the scratch copy does. The scratch copy's `js/screens/system.js` (with these entries and both edits) is at `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/grading/app/js/screens/system.js`.

```js
    /* engine pass (items 429, 430, 433, 434, 437): complex and vector expressions, order with distractors, complex code */
    { name: 'expression (complex)', kind: 'expression', item: { question: 'Write $\\dfrac{1}{1+i}$ as $a + bi$.', widget: { kind: 'expression', answer: '\\frac{1-i}{2}', accept: ['(1-i)/2', '0.5-0.5i'], wrong: [{ id: 'conj', tex: '\\frac{1+i}{2}' }], keyboard: 'algebra', label: 'The value' } } },
    { name: 'expression (vector)', kind: 'expression', item: { question: 'Type $\\mathbf{a} \\times \\mathbf{b}$ for $\\mathbf{a} = (1, 2, 0)$ and $\\mathbf{b} = (0, 1, 3)$ as a vector.', widget: { kind: 'expression', answer: '(6, -3, 1)', accept: ['(6,-3,1)'], wrong: [{ id: 'flipped', tex: '(-6, 3, -1)' }], keyboard: 'algebra', label: 'The cross product' } } },
    { name: 'order (distractors)', kind: 'order', item: { question: 'Put the steps of the proof in order. Leave out the lines that do not belong.', widget: { kind: 'order', lines: [
      { id: 's1', text: 'Write the two odd numbers as $2a + 1$ and $2b + 1$' }, { id: 's2', text: 'Add them: $2a + 2b + 2$' }, { id: 's3', text: 'Factor out 2: $2(a + b + 1)$, which is even' },
      { id: 'd1', text: 'Add them: $2a + 2b + 1$', why: 'The two ones add to 2, not 1.' }, { id: 'd2', text: 'Two odd numbers are both prime' }], answer: ['s1', 's2', 's3'], distractors: ['d1', 'd2'] } } },
    { name: 'code (complex)', kind: 'code', item: { question: 'Return the product of the two complex numbers.', widget: { kind: 'code', language: 'python', starter: 'def cmul(z, w):\n    return 0\n', solution: 'def cmul(z, w):\n    return z * w\n',
      examples: [{ call: 'cmul(1+2j, 3-1j)', expect: '(5+5j)', compare: 'isclose' }], tests: [{ call: 'cmul(1+2j, 3-1j)', expect: '(5+5j)', compare: 'isclose' }, { call: 'cmul(1j, 1j)', expect: '-1', compare: 'isclose' }, { call: 'cmul(0.1+0.2j, 0.3)', expect: '(0.03+0.06j)', compare: 'isclose', tol: { rel: 1e-9, abs: 1e-12 } }], how: 'Check runs 3 hidden tests.' } } },
    { name: 'code (C++ complex)', kind: 'code', item: { question: 'Return the product of the two complex numbers.', widget: { kind: 'code', language: 'cpp', starter: '#include <complex>\n\nstd::complex<double> cmul(std::complex<double> z, std::complex<double> w) {\n    return 0;\n}\n', solution: '#include <complex>\n\nstd::complex<double> cmul(std::complex<double> z, std::complex<double> w) {\n    return z * w;\n}\n',
      examples: [{ call: 'cmul({1, 2}, {3, -1})', expect: { re: 5, im: 5 }, compare: 'isclose' }], tests: [{ call: 'cmul({1, 2}, {3, -1})', expect: { re: 5, im: 5 }, compare: 'isclose' }, { call: 'cmul({0, 1}, {0, 1})', expect: -1, compare: 'isclose' }], how: 'Check runs 2 hidden tests.' } } },
```

Screenshots (gallery cards, both themes, desktop 1280 and mobile 390 wide), in `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/grading/shots/`, named `<card>-<state>-<light|dark>-<desktop|mobile>.png`:

- `expression-complex-wrong-*`, `expression-complex-right-*` (1/(1+i) typed; the conjugate wrong answer shows key `conj`).
- `expression-vector-wrong-*` (two components typed, the `length` line), `expression-vector-right-*` (typed as a `pmatrix` column).
- `order-distractors-start-*`, `order-distractors-filled-*` (Fill answer: the two distractors in "Left out"), `order-distractors-right-*`, `order-distractors-wrong-*` (a distractor in the sequence, key `d1`).
- `code-complex-wrong-*` (`z + w` against the product: the failing rows show complex expected values and the tolerance note), `code-complex-right-*`, `code-cpp-complex-right-*`.
- `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/grading/shots-routes/route-system.png` and `route-system-390.png`: the whole gallery page, from `tools/playthrough.mjs --routes-only --shots ... --mobile` run in the scratch copy (routes: all passed, no console errors).
