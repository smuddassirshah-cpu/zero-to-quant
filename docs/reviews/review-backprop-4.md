# backprop (Backpropagation) level 4 and the strand's autograd.py: second-reader findings

Scope: `app/content/data/ai/autograd.py` (version 1.0, SHA-256 `5917d4ec91f7…`, 11,277 bytes, matching the report), and the level 4 files in `app/content/courses/backprop/`: l13 to l16, review-4, homework-4, problems-4 (7 files). Branch `review-backprop-4` at `bd99bc2c`.
Method: autograd.py first. An independent float64 central-difference check of my own ($h = 10^{-6}$, my own loop, not `grad_check`) covered 128 cases. These were: `+ - * /` over nine shape pairs (broadcasting both ways, `()`, `(1,)`, a leading axis, `(2,1,4)` with `(3,1)`), reflected operators with ndarrays, NumPy scalars and numbers, `**` at six powers, `sum` and `mean` over every axis, negative axes and tuples, each with and without `keepdims`, `@` on nine 2-D and batched shape pairs plus `ndarray @ Tensor`, `tanh`, `relu`, `exp`, `log`, `reshape`, `T` (2-D and 3-D), indexing (repeats, tuple, slice, int, a 2-D embedding index), `concat` (axis 0, −1, one tensor twice), reused nodes (`x*x`, `x+x`, `x@x`, `x@x.T`, a diamond), `cross_entropy` (list, int64 and int32 targets, logits near 1000 and spread to ±900, composed) and a two-layer MLP. Worst relative error $4.9 \times 10^{-8}$ (logits near 1000, where the difference itself loses digits; the closed form $(\mathbf{P}-\mathbf{Y})/n$ matches the backward exactly), all others below $2.6 \times 10^{-9}$. I also checked behaviour (`ValueError` on a non-scalar `backward`, `zero_grad` in place, accumulation over two `backward` calls, a 60-level diamond chain with $2^{60}$ paths in 1 ms, so the visited set works, a chain 40,000 operations deep with the recursion limit at 100, and chains 10,000 to 100,000 operations deep in Pyodide 0.27.7 under node). I compared the API name by name with the brief's contract and the report's last section and found no mismatch: the shipped extras are supersets (batched `@`, `T` on n-D, `zero_grad` replacing a reshaped `grad`). I ran `docs/reports/backprop-L4-numbers.py` with the venv Python: 326 of 326, exit 0. It asserts each lesson value at its JSON path, recomputed by a second route, so it checks the screen; it does not read `how` text. `node tools/grade-all.mjs --file <f> --code --local-cdn <pkgs>` on all 7 files: 0 failures (10 Python widgets, 27 authored mutants). My own 37 wrong or alternative solutions went through the same runner, as `mutants` on scratch copies of the JSON (appendix). I recomputed every stated number and distractor by hand or in Python, ran `voice-scan.py 35` (0 and 0), and grepped for American spelling, em-dashes and exclamation marks (none).
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, loose claim, test gap or teaching issue; note = style or minor.

Counts: 2 errors, 8 warnings, 13 notes. autograd.py: 0 errors, 1 warning, 4 notes. Nothing found blocks the freeze.

## autograd.py

Every op's gradient is right, including broadcasting in both directions, every reduction axis, batched `@`, reuse and stable cross-entropy. The topological sort is iterative with a visited set marked on pop, which is correct for a DAG. `backward()` refuses a tensor of size other than 1, as the contract says.

- app/content/data/ai/autograd.py | module name | warning | Pyodide 0.27.7's lockfile has a package called `autograd` (HIPS autograd 1.7.0, which needs `future`). The code widget's import hint (`importHint` in `js/engine/widgets/code.js`) repeats `from autograd import ...` as `import autograd`, and the worker's `loadPackagesFromImports` then downloads and installs `autograd-1.7.0` and `future-1.0.0` (about 490 KB of wheels) on the first run of every widget that ships the file. I checked in Pyodide under node: the message is "Loading autograd, future, numpy". The local file still wins, because the working directory goes first on `sys.path` (it imported `/tmp/.../autograd.py`, version 1.0), so the grading is right. The cost is a wasted download for seven courses, plus a load-failure message wherever the wheel is missing. | Engine item, no content change: leave out of the import hint any module name that `files` provides (`autograd.py` gives `autograd`). The other fix, renaming the module, changes the frozen contract and is only cheap before later courses ship it.
- app/content/data/ai/autograd.py | `cross_entropy` | note | A negative target is accepted and wraps to the last class (`targets = [0, -1]` gives a finite loss). An out-of-range one raises `IndexError`. A later course that pads with −1 would get a silent wrong loss. | In a 1.1, if one is ever made: raise `ValueError` unless `0 <= y < K`. Until then, say in the contract that targets must lie in `0..K-1`.
- app/content/data/ai/autograd.py | `unbroadcast` | note | It does not check that `shape` could have broadcast to `grad.shape`. For example `unbroadcast(ones((4, 1, 3)), (2, 3))` returns shape `(1, 3)` with no error. The ops never call it like this, but the function is public and taught. | Optional in a 1.1: assert that the result's shape equals `shape`.
- app/content/data/ai/autograd.py | `reshape`, `T`, basic indexing | note | These outputs' `data` are NumPy views of the input's `data` (`np.shares_memory` is True). Editing an op output's `.data` in place, or running `sgd_step` on one, writes into the parent. This is consistent with the contract's no-in-place rule, but nothing says it. | One line in the contract's Conventions: "`data` of an op's output may share memory with its input; never modify it in place."
- app/content/data/ai/autograd.py | `__pow__` | note | Only a `Tensor` exponent is refused. An ndarray exponent broadcasts forward, but the backward has no `unbroadcast`, so `Tensor(ones(3)) ** ones((2, 3))` fails in `backward`. The contract says `k` is a Python number. | Optional in a 1.1: refuse any non-scalar `k`.

## Level 4 (Gradients for arrays)

- app/content/courses/backprop/l16-a-small-array-autograd.json | screens[3] canvas console and widget | error | The console runs `L = ...sum(); L.backward()` and then `L = ...mean(); L.backward(); b2.grad` on the same graph with no `zero_grad()`. Run as shown, the shipped autograd prints $-7.8406$, not $-0.6031$. The shared nodes `a`, `p2` and so on still hold the first pass's gradient, so it flows again. The answer key, $-0.6031$, needs a fresh graph. The screen contradicts the lesson's own quiz[0] ("only `zero_grad()` clears them"). A learner who applies that rule cannot reach the key. | Insert `>>> for p in params: p.zero_grad()` and rebuild the forward before the mean (`>>> a = forward(X)`), or show the two runs as separate sessions headed "fresh network".
- app/content/courses/backprop/l16-a-small-array-autograd.json | screens[4] widget tests[2] | error | The setup is `out = x.sum(axis=0) + y.sum(axis=1, keepdims=True); out.grad = ...; out._backward()`. That runs only the `+` node's backward, so the two `sum` nodes get gradients but `x` and `y` never do. The expected value is all zeros, so the test passes for any `sum` backward. The `how` says this test checks "`sum` along each axis". My mutant with `sum` ignoring `axis` (no `expand_dims`) passes all six tests. On a 3 by 3 tensor that mutant gives `a.sum(axis=1)` the gradient column $(1, 1, 1)$ instead of $(1, 2, 3)$. | Run the root's backward, with a dropped non-leading axis on a square tensor: `x = Tensor(np.ones((3, 3))); L = (x.sum(axis=1) * Tensor([1.0, 2.0, 3.0])).sum() + (x.sum(axis=0, keepdims=True) * Tensor([[1.0, -1.0, 0.0]])).sum(); L.backward()`, call `x.grad.tolist()`, expect `[[2.0, 0.0, 1.0], [3.0, 1.0, 2.0], [4.0, 2.0, 3.0]]`. The appendix's "sum ignores axis" mutant gives `[2.0, 1.0, 3.0]` in every row; add it, naming this test.
- app/content/courses/backprop/l13-backward-through-a-product.json | screens[2] widget lines[5] (x1) why | warning | "$\mathbf{G}$ has no entry $(k, j)$ for $k = 3$" is false. $\mathbf{G}$ is 4 by 2, so $G_{3j}$ exists, and so does $X_{3j}$. The elementwise formula can be computed; it is just wrong. | "That treats the product as elementwise. $W_{kj}$ meets $X_{ik}$ in every row $i$, not one entry, and $\mathbf{G}$ (4 by 2) does not even have $\mathbf{W}$'s shape."
- app/content/courses/backprop/l16-a-small-array-autograd.json | screens[6] feedback.correct | warning | "and `z.data` was changed under the earlier `@` node too" is false for this network. The `@` node that made `z` reads only `X.data` and `W1.data` in its backward. The later `@` reads `z.data`, which now holds the ReLU output, the right value. The whole fault is the missing node and mask. | "Returning `z` adds no node and no slope, so the gradient flows back through entries ReLU had blocked."
- app/content/courses/backprop/l16-a-small-array-autograd.json | screens[8] widget how | warning | "50 training steps on 32 rows must bring the loss below 0.5 from $\ln 2$." The model solution starts `train_run` at 0.8888, not $\ln 2 = 0.6931$: the weights are random, not zero. It ends at 0.3701. | "...must bring the loss from about 0.89 to below 0.5."
- app/content/courses/backprop/l16-a-small-array-autograd.json screens[2], screens[8]; homework-4.json items[5] | hidden tests | warning | A `backward` with no visited set, or with one but in pre-order, passes every hidden test in all three widgets. No test has an interior node with two consumers: reuse is only ever of a leaf (`w * x + w`, `W` twice, `(w * w + w)`). Both bugs give wrong gradients once an interior node is shared. With `a = w * x` and `L = a * 2 + a * 3` at $w = 2$, $x = 3$, the true $\partial L/\partial w$ is 15; the no-seen version gives 21 and the pre-order one gives 9. With `h = w * x` and `L = h * h`, the no-seen version gives 72 against 36. AUTHORING section 9 names "a backward pass with no `seen` set" as the bug to cover. | Add a hidden test in each widget, `w = Tensor([2.0]); x = Tensor([3.0]); a = w * x; L = a * 2.0 + a * 3.0; L.backward()` with call `w.grad.tolist()` and expect `[15.0]`. Add both appendix mutants naming it.
- app/content/courses/backprop/l16-a-small-array-autograd.json screens[8]; homework-4.json items[5] | hidden tests | warning | No hidden test sends a gradient through `sum(axis=...)`. Every network ends in `cross_entropy`, and the tensor-used-twice test uses `.sum()` with no axis. A `sum` that ignores `axis` passes both widgets. Homework items[5]'s prose asks for `sum(axis=None, keepdims=False)` explicitly. | Add the axis test proposed for screens[4] to both widgets.
- app/content/courses/backprop/l15-softmax-cross-entropy.json screens[9]; l16-a-small-array-autograd.json screens[8]; homework-4.json items[5] | hidden tests | warning | One maximum for the whole batch, `logits.max()` in place of the row maximum, passes every test in all three widgets. Each batch test has rows of similar size, and each extreme test has one row. On a batch whose rows sit 1000 apart (rows $(0, -1)$ and $(1000, 999)$) that version returns $-\infty$ where the true loss is 0.8133. l15's explain teaches "each row's largest logit". | Add one hidden test per widget: logits `[[0.0, -1.0], [1000.0, 999.0]]`, targets `[1, 0]`, loss 0.813262 and gradient `[[0.365529, -0.365529], [-0.134471, 0.134471]]` (each row's $\mathbf{p} - \mathbf{y}$ over 2).
- app/content/courses/backprop/l16-a-small-array-autograd.json | screens[9] widget tests[1] | warning | The call `grad_check(lambda: ..., [C, W]) < 1e-6` resolves `grad_check` in the learner's namespace. A correct solution that trims the starter's import to what it uses (`from autograd import Tensor, cross_entropy, concat`) fails test 2 with a `NameError` and is graded wrong. I checked: the same `concat` solution with the full import passes all four tests. | Import inside the test: `__import__('autograd').grad_check(...)`, or a one-line `prelude` `from autograd import grad_check as _gc` with the call using `_gc`.
- app/content/courses/backprop/l13-backward-through-a-product.json | screens[6] options[1] why | note | "Rounding is twelve orders of magnitude smaller": 1.89 against about $10^{-11}$ is eleven. | "eleven orders of magnitude".
- app/content/courses/backprop/l13-backward-through-a-product.json | screens[9] feedback.correct | note | $\mathbf{e}\mathbf{F}^T$ uses $\mathbf{e}$, which the screen never defines (prose and hints call it the residual row $\hat{\mathbf{r}} - \mathbf{r}$). | "The residuals $\mathbf{e} = \hat{\mathbf{r}} - \mathbf{r}$ are $(-0.2, 0, -0.09)$, and $\mathbf{e}\mathbf{F}^T$..."
- app/content/courses/backprop/l14-broadcasting-backwards.json | screens[8] canvas rows[3] | note | "axis 0, then axis 2 kept" counts axes of the original `(2, 4, 3)` array. The prose's second step, and the code, index the array after the leading sum, where that axis is 1. | "axis 0, then the last axis, kept".
- app/content/courses/backprop/l16-a-small-array-autograd.json | screens[4] prose | note | "Your class from the last screen is in the editor": the editor holds the model class from the starter, not the learner's own. | "The class from the last screen is in the editor."
- app/content/courses/backprop/l16-a-small-array-autograd.json screens[2] widget how; homework-4.json items[5] widget how | how | note | "A chain 5,000 operations deep": each of the 5,000 steps is `* 1.0001` then `+ 0.0`, so the graph is 10,000 operations deep. | "A chain of 10,000 operations".
- app/content/courses/backprop/review-4.json items[8] explain; l16-a-small-array-autograd.json screens[5], summary.ideas[2] | explain | note | Review items[8] says a float32 check "stalls near $10^{-5}$"; l16 says "near $10^{-4}$". Both are consistent with their own figures ($3 \times 10^{-5}$ and $8.0 \times 10^{-5}$), but they read as two floors. | "stalls between $10^{-5}$ and $10^{-4}$" in review-4.
- app/content/courses/backprop/homework-4.json | items[3] model | note | "A real bug gives errors of order $10^{-2}$ to 1 in both precisions" is too strong. A missing small term can give $10^{-5}$, which is review-4 items[8]'s point ("a real bug can hide at that size"). | "A real bug usually gives errors far above the rounding floor, in both precisions."
- app/content/courses/backprop/l16-a-small-array-autograd.json screens[4]; l16 screens[8]; homework-4.json items[0] | hidden tests | note | Assigning (`=`) instead of adding (`+=`) survives where no test feeds a tensor two gradients: in `@` on screens[4], in the `cross_entropy` backward on screens[8], and in `tensor_exp` on homework items[0]. screens[8] does catch `=` in `@` (its test 3). Harmless in these tests, but it breaks the contract as soon as a logit or input is reused. | Optional: on screens[8] add `cross_entropy(Z, y) + (Z * Z).sum()` to one gradient check; on homework items[0] use `tensor_exp(A) * A`.
- app/content/courses/backprop/l16-a-small-array-autograd.json | screens[9] | note | The brief has the remaining contract ops "shown, read and tested in one screen". The screen lists them, and its tests exercise indexing, `reshape`, `@`, `cross_entropy` and `grad_check` only. `-`, `/`, `**`, `mean`, `exp`, `log`, `T`, `concat`, `softmax` and `sgd_step` are tested on the canonical file by the number script, never in the lesson. | Acceptable as it stands; say so in the report, or add one test using `mean` and `concat`.
- app/content/courses/backprop/l15-softmax-cross-entropy.json | screens[4] explain | note | "lowers the others, each by its own chance" leaves out the step size (each falls by $\eta p_i$). screens[10] has it right ("in proportion to their chances"). | "...lowers the others in proportion to their chances."

Checked and right (no finding): every number in l13 (the $\mathbf{Y}$ of the hook, 4.5, 3.5, −4, 1.89, $9.5 \times 10^{-12}$, −0.272, −0.013, 4, 6.5, 2), l14 (column sums 1.2, 0.2, 0.6; row sums (0.7, 0.6, 0.2, −0.1, 0.6); 0.002, −0.001, 0.0004; $\tfrac1{15}$; 2.0; £10, £2.5, £3.5; −0.5, −0.1667; 0.025), l15 (0.659, 0.2424, 0.0986, 0.645; 0.417, 0.602, 0.181; −0.341; (0.2119, 0.2119, −0.4239); −0.1705; (0.0723, 0.3, −0.0141); `nan` and `inf` routes; 800; −0.7; 3.2958, 4.7549, 0.037), l16 (1.3892, 22.2272; $b = -0.946928$ as the 13th `Random(42)` draw; −0.6031, −9.65; 2.6e-11, 8.0e-5; 0.161, 7.0e-12; 6; 7.194565; 2179, 4358, 4288; 0.2, 0.0125), review-4 (all 10), homework-4 items[3] and [4], problems-4 (all 13 parts, including 0.3005 from 0.1269 and 0.4741). Every distractor's value matches its `why`, and no answer's tolerance band touches a distractor's. The tolerances suit the decimals asked.

## Appendix: reviewer mutants

Each went through `grade-all.mjs --code` (Pyodide, the page's harness) as a `mutants` entry on a scratch copy of the file. "Fails T*n*" is the first hidden test it fails; SURVIVES means it passes every hidden test. For a class widget, a source is the widget's model `solution` byte for byte with the block shown replaced. A function widget's source is given whole.

### l13 screens[8] `matmul_backward`

1. Transposes on the wrong side of both products. Fails T1.
```python
import numpy as np


def matmul_backward(X, W, G):
    dX = W.T @ G.T
    dW = G.T @ X
    return dX, dW
```
2. `dW` as $\mathbf{G}^T\mathbf{X}$. Fails T1.
```python
import numpy as np


def matmul_backward(X, W, G):
    dX = G @ W.T
    dW = G.T @ X
    return dX, dW
```
3. `dW` averaged over rows. Fails T1.
```python
import numpy as np


def matmul_backward(X, W, G):
    dX = G @ W.T
    dW = X.T @ G / len(X)
    return dX, dW
```
4. `dX` without the transpose of `W`. Fails T1.
```python
import numpy as np


def matmul_backward(X, W, G):
    dX = G @ W
    dW = X.T @ G
    return dX, dW
```

### l14 screens[8] `unbroadcast`

1. A broadcast gradient returned unsummed. Fails T1.
```python
import numpy as np


def unbroadcast(grad, shape):
    return grad
```
2. Axis 0 summed, whatever the shape. Fails T2.
```python
import numpy as np


def unbroadcast(grad, shape):
    return grad.sum(axis=0)
```
3. Size-1 axes matched from the left, before the leading sum. Fails T4.
```python
import numpy as np


def unbroadcast(grad, shape):
    shape = tuple(shape)
    axes = tuple(i for i, n in enumerate(shape) if n == 1)
    if axes:
        grad = grad.sum(axis=axes, keepdims=True)
    extra = grad.ndim - len(shape)
    if extra > 0:
        grad = grad.sum(axis=tuple(range(extra)))
    return grad
```
4. Only one leading axis summed. Fails T3.
```python
import numpy as np


def unbroadcast(grad, shape):
    shape = tuple(shape)
    extra = grad.ndim - len(shape)
    if extra > 0:
        grad = grad.sum(axis=0)
    axes = tuple(i for i, n in enumerate(shape) if n == 1 and grad.shape[i] != 1)
    if axes:
        grad = grad.sum(axis=axes, keepdims=True)
    return grad
```

### l15 screens[9] `softmax_ce`

1. One maximum for the whole batch. SURVIVES.
```python
import numpy as np


def softmax_ce(logits, targets):
    n = logits.shape[0]
    rows = np.arange(n)
    m = np.full((n, 1), logits.max())
    e = np.exp(logits - m)
    s = e.sum(axis=1, keepdims=True)
    loss = np.mean(m[:, 0] + np.log(s[:, 0]) - logits[rows, targets])
    d = e / s
    d[rows, targets] -= 1
    return loss, d / n
```
2. Softmax without subtracting the maximum. Fails T3.
```python
import numpy as np


def softmax_ce(logits, targets):
    n = logits.shape[0]
    rows = np.arange(n)
    m = np.zeros((n, 1))
    e = np.exp(logits - m)
    s = e.sum(axis=1, keepdims=True)
    loss = np.mean(m[:, 0] + np.log(s[:, 0]) - logits[rows, targets])
    d = e / s
    d[rows, targets] -= 1
    return loss, d / n
```
3. Softmax then log, max subtracted, clipped at $10^{-300}$. Fails T4.
```python
import numpy as np


def softmax_ce(logits, targets):
    n = logits.shape[0]
    rows = np.arange(n)
    e = np.exp(logits - logits.max(axis=1, keepdims=True))
    p = e / e.sum(axis=1, keepdims=True)
    loss = -np.mean(np.log(np.maximum(p[rows, targets], 1e-300)))
    d = p.copy()
    d[rows, targets] -= 1
    return loss, d / n
```
4. Targets indexed as columns of every row (`d[:, targets] -= 1`, the rest as the model). Fails T2.
```python
import numpy as np


def softmax_ce(logits, targets):
    n = logits.shape[0]
    rows = np.arange(n)
    m = logits.max(axis=1, keepdims=True)
    e = np.exp(logits - m)
    s = e.sum(axis=1, keepdims=True)
    loss = np.mean(m[:, 0] + np.log(s[:, 0]) - logits[rows, targets])
    d = e / s
    d[:, targets] -= 1
    return loss, d / n
```
5. Loss summed over rows, gradient divided by $n$ (`loss = np.sum(...)`, the rest as the model). Fails T2.

### l16 screens[2] `Tensor`: `+`, `*`, `backward`

1. No visited set. SURVIVES. The model's `backward` ordering block becomes:
```python
        order, stack = [], [(self, False)]
        while stack:
            node, done = stack.pop()
            if done:
                order.append(node)
            else:
                stack.append((node, True))
                for p in node._prev:
                    stack.append((p, False))
```
2. A visited set, but pre-order (a node can run before all its consumers have added in). SURVIVES. The ordering block and the loop that follows become:
```python
        order, seen, stack = [], set(), [self]
        while stack:
            node = stack.pop()
            if id(node) in seen:
                continue
            seen.add(id(node))
            order.append(node)
            stack.extend(node._prev)
        self.grad = np.ones_like(self.data)
        for node in order:
            node._backward()
```
3. A product gradient not summed back to a broadcast operand. Fails T3. The `__mul__` closure body becomes:
```python
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
```

### l16 screens[4] `@`, `sum`, `tanh`, `relu`

1. `sum` backward ignores `axis`. SURVIVES (see the tests[2] error). The `sum` closure body becomes:
```python
            self.grad += np.broadcast_to(out.grad, self.data.shape)
```
2. `@` overwrites instead of adding. SURVIVES. The `__matmul__` closure body becomes:
```python
            self.grad = out.grad @ other.data.T
            other.grad = self.data.T @ out.grad
```
3. `@` with the transpose on the wrong side. Fails T1. The `__matmul__` closure body becomes:
```python
            self.grad += other.data.T @ out.grad.T
            other.grad += out.grad.T @ self.data
```

### l16 screens[8] `cross_entropy` and the whole class

1. No visited set (block as in screens[2] mutant 1). SURVIVES.
2. Pre-order (block as in screens[2] mutant 2). SURVIVES.
3. `sum` ignores `axis` (block as in screens[4] mutant 1). SURVIVES.
4. One maximum for the batch: `m = z.max(axis=1, keepdims=True)` becomes `m = np.full((z.shape[0], 1), z.max())`. SURVIVES.
5. The fused backward overwrites: `logits.grad += p * (out.grad / n)` becomes `logits.grad = p * (out.grad / n)`. SURVIVES.
6. `@` overwrites (block as in screens[4] mutant 2). Fails T3.

### l16 screens[9] `lookup_loss` on the shipped file

1. A correct alternative by `concat` with a trimmed import. Fails T2 with a `NameError` on `grad_check` (a correct solution graded wrong). With the starter's full import line the same body passes all four tests.
```python
import numpy as np
from autograd import Tensor, cross_entropy, concat


def lookup_loss(C, idx, W, y):
    parts = [C[idx[:, j]] for j in range(idx.shape[1])]
    return cross_entropy(concat(parts, axis=1) @ W, y)
```
2. The loss summed over rows, not averaged. Fails T1.
```python
import numpy as np
from autograd import Tensor, cross_entropy


def lookup_loss(C, idx, W, y):
    n = len(idx)
    return cross_entropy(C[idx].reshape(n, -1) @ W, y) * n
```

### homework-4 items[0] `tensor_exp`, `tensor_log`, `logsumexp`

1. The `logsumexp` backward forgets to divide by the row sum: `x.grad += e / s * out.grad` becomes `x.grad += e * out.grad`. Fails T4.
2. `logsumexp` keeps no axis: `out = Tensor(m + np.log(s), (x,), "logsumexp")` becomes `out = Tensor((m + np.log(s))[:, 0], (x,), "logsumexp")`. Fails T3.
3. The `exp` backward overwrites: `x.grad += e * out.grad` (in `tensor_exp`) becomes `x.grad = e * out.grad`. SURVIVES.

### homework-4 items[1] `batch_matmul_backward`

1. `dW` from the first batch item only. Fails T2.
```python
import numpy as np


def batch_matmul_backward(X, W, G):
    dX = G @ W.T
    dW = X[0].T @ G[0]
    return dX, dW
```
2. `dW` by `X.T` on a 3-D array (which reverses all three axes). Fails T1.
```python
import numpy as np


def batch_matmul_backward(X, W, G):
    dX = G @ W.T
    dW = (X.T @ G).sum(axis=0)
    return dX, dW
```

### homework-4 items[5] performance task

1. No visited set (block as in l16 screens[2] mutant 1). SURVIVES.
2. Pre-order (block as in l16 screens[2] mutant 2). SURVIVES.
3. `sum` ignores `axis` (block as in l16 screens[4] mutant 1). SURVIVES.
4. One maximum for the batch: `m = z.max(axis=1, keepdims=True)` becomes `m = np.full((z.shape[0], 1), z.max())`. SURVIVES.

## Fix pass

Graded answers changed: none (l16 screens[3] key stays -0.6031; the console now matches it). Mutants verified by `grade-all.mjs --code`: each fails its named test first.

- autograd.py | module name | fixed in engine 1266 (merged at caf31d32); no content change.
- autograd.py | `cross_entropy` negative target, `unbroadcast` shape check, views from `reshape`/`T`, `__pow__` ndarray exponent | frozen, not applied (v1.0, byte-identical in seven courses).
- l16 screens[3] console | fixed: console now runs `zero_grad()` on the params and rebuilds `a = forward(X)` before the mean, so it prints -0.6031 as the key says; explain teaches the reset and the -7.8406 that follows without it.
- l16 screens[4] tests[2] | fixed: replaced by the 3 by 3 root-backward test (expect `[[2,0,1],[3,1,2],[4,2,3]]`); mutant "sum ignores axis" added, fails test 3.
- l13 screens[2] "no entry (k, j)" | fixed: now says the product is treated elementwise, W_kj meets X_ik in every row, G is 4 by 2.
- l16 screens[6] feedback.correct | fixed: dropped the false `z.data` under the earlier `@` claim.
- l16 screens[8] how "from ln 2" | fixed: "from about 0.89 to below 0.5" (model run starts at 0.8888).
- l16 screens[2], screens[8], homework items[5] visited-set and order | fixed: shared interior node test (`[15.0]`) added to all three; mutants no-seen and pre-order added (fail the new test).
- l16 screens[8], homework items[5] sum axis | fixed: sum-axis test added to both; mutant added.
- l15 screens[9], l16 screens[8], homework items[5] one batch maximum | fixed: rows-1000-apart test added to all three (0.813262 and gradient as proposed, recomputed: rows give 1.3133 and 0.3133); mutant added.
- l16 screens[9] tests[1] | fixed: call uses `__import__('autograd').grad_check`, so a trimmed import no longer gives a NameError.
- l13 screens[6] "twelve orders" | fixed: eleven.
- l13 screens[9] feedback.correct | fixed: defines e as the residual row.
- l14 screens[8] canvas rows[3] | fixed: "axis 0, then the last axis, kept".
- l16 screens[4] prose "Your class" | fixed: "The class".
- l16 screens[2] how, homework items[5] how "5,000 deep" | fixed: 10,000 operations (hows also list the new tests).
- review-4 items[8] explain | fixed: "between 1e-5 and 1e-4".
- homework items[3] model "order 1e-2 to 1" | fixed: "usually far above the rounding floor, in both precisions".
- l16 screens[8], homework items[0] `=` for `+=` | fixed: l16 test 10 (`(Z*Z).sum() + cross_entropy(Z, y)`) and homework test 7 (`tensor_exp(A) * A`) with assign mutants.
- l16 screens[9] contract ops untested | declined: reviewer calls it acceptable; the number script covers them on the canonical file.
- l15 screens[4] explain | fixed: "in proportion to their chances".
