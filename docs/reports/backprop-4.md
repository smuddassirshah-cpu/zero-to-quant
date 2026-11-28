# backprop level 4 (Gradients for arrays): report

## Files written

All in `app/content/courses/backprop/`, skills `bp-arrays` on l13 to l16 and `bp-check` on l16; the review tags eight items `bp-arrays` and two `bp-check`. Plus the strand's canonical `app/content/data/ai/autograd.py` (11,277 bytes, version 1.0, SHA-256 `5917d4ec91f7d1c85b8ca8ba052be5b565fa99afa3d9c08219529cdaf032bda8`).

| File | Screens / items | Code |
|---|---|---|
| `l13-backward-through-a-product.json` | 10 screens, 3 quiz items, 15 min | `matmul_backward(X, W, G)` |
| `l14-broadcasting-backwards.json` | 10 screens, 3 quiz items, 14 min | `unbroadcast(grad, shape)` |
| `l15-softmax-cross-entropy.json` | 11 screens, 3 quiz items, 15 min | `softmax_ce(logits, targets)` |
| `l16-a-small-array-autograd.json` | 11 screens, 3 quiz items, 20 min | `Tensor` in three steps (`+`, `*`, `backward`; `@`, `sum`, `tanh`, `relu`; `cross_entropy`), then `lookup_loss` on the shipped `autograd.py` |
| `review-4.json` | 10 items, difficulty 2 to 4, `pass: 0.8` | none |
| `homework-4.json` | 6 items, difficulty 3 to 5 (two at 5) | `tensor_exp`/`tensor_log`/`logsumexp` (5), `batch_matmul_backward` (4), performance `Tensor` (5); `order` item (the Jacobian route to $p - y$); `longform` float64 against float32 with a 10-point rubric; one numeric |
| `problems-4.json` | 3 problems, 13 parts, difficulty 3, 4, 5 | none |

Lesson shapes. l13: where a weight reaches (matrix canvas, frames light each $W_{kj}$, its column of $\mathbf{X}$ and its column of $\mathbf{Y}$), the derivation of $\mathbf{X}^T\mathbf{G}$ as an `order` with a distractor, a 2 by 2 by hand (4.5), the shape check and $(\mathbf{A}\mathbf{B})^T = \mathbf{B}^T\mathbf{A}^T$, $\tfrac12\lVert\mathbf{A}\mathbf{B}\rVert^2$ at $9.5 \times 10^{-12}$, trap $\mathbf{G}^T\mathbf{X}$ on square matrices (1.89), edge case a 1-D vector (`np.outer` or reshape), code, a factor model's exposures ($-0.272$). l14: a nudge of $b_2$ (0.002), column sums on a `pair` of `matrix` and `array` stepped by frames, the rule, a column broadcast with a central-difference console, `keepdims`, `sum()` and `mean()` backwards ($\tfrac1{15}$), trap (a bias that becomes 5 by 3 under broadcasting), edge case a scalar (2.0), code, one fee rate over four trades (£10 a basis point). l15: softmax of $(2, 1, 0.1)$ (0.659), shift invariance on live `bars` (controls on $z_0$ and a shared shift), the loss 0.417 nats, the derivation of $p - y$ (`order`), the gradient $(-0.341, 0.2424, 0.0986)$, logits near 1000, a batch ($-0.1705$), tanh and ReLU backwards (table widget beside a `plane`), trap softmax then log ($e^{-800}$ underflows: `inf` against 800), code, next-day return buckets ($-0.7$). l16: the backward order of the array network (`order`), shapes all the way back (`graph` with two value lines, frames; the mean 1.3892 against the sum 5.5568), code A, matching level 3 ($-2.412490/4 = -0.6031$), code B, float64 against float32 ($2.6 \times 10^{-11}$, $8.0 \times 10^{-5}$), trap an in-place ReLU (0.161 against $7.0 \times 10^{-12}$), edge case a tensor used twice (6), code C, the shared file (`files` ships the canonical `autograd.py`), checking a 64-32-3 signal model (4358 forward passes).

The factor of 4: l16 screen 2 says plainly that level 3's loss is a sum and the contract's a mean (5.5568 against 1.3892); screen 4 asks for the output bias's gradient as a mean ($-0.6031$); the l16 quiz asks for the step that retraces level 3 (0.2 on the mean for 0.05 on the sum, giving 0.025020 summed after 200 steps).

Generators and helpers: `/tmp/claude-0/-home-user-zero-to-quant/b2245dfe-6f55-570e-8d22-d9384c33129b/scratchpad/backprop-4/` (`common4.py`, `tsrc.py` with the learner's class at each step, `mut.py`, `gen13.py` to `gen16.py`, `genrev.py`, `genhw.py`); every test `expect` comes from the model solution.

Timing (Pyodide 0.27.7 under node, canonical file): the level 3 network, 200 steps, 74 ms; 50 steps of a 2-16-2 net on 32 rows, 17 ms; `grad_check` on that net, 23 ms; a one-block char GPT step built from `Tensor` ops (vocab 65, context 32, width 64, 4 heads, MLP 256, batch 16, with a helper for the last-two-axes transpose) 88 to 126 ms, against 86 ms for the hand-written spike. The l16 code C and homework performance widgets carry `budget: 4000` for a phone; every case is well under 1 s on a desktop.

## Gates

1. Validator: `node tools/validate.mjs` 0 errors; for level 4 files one advisory canvas-kind warning (l13 screen 5, a table after a matrix) and five `O2-long-sentence` advisories.
2. Voice: `voice-scan.py 35` with `VOICE_BASE=app/content/courses/backprop`: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `docs/reports/backprop-L4-numbers.py` with the venv: 326 of 326 checks, exit 0. Route A is the canonical `autograd.py`; route B plain NumPy with hand gradients and the script's own central differences. It checks every op (22 combinations: broadcasting both ways, a leading axis, a scalar, batched `@`, an index with repeats, a slice, `concat`, a reused tensor) by `grad_check` and independently below $10^{-6}$; the 200-step and 5,000-step chains with the recursion limit at 150; the SHA-256 of every shipped copy; the course network (5.556800, 0.025020, $-2.412490$, both routes); $9.5 \times 10^{-12}$, $2.6 \times 10^{-11}$, $8.0 \times 10^{-5}$, 0.161, $7.0 \times 10^{-12}$; every lesson, review, homework and problem number at its JSON path; and every code widget (model passes, starter fails, each mutant first fails its named test).
4. Code widgets: `node tools/grade-all.mjs --code --local-cdn <pkgs>` on all seven files: 10 Python widgets, 0 failures. Mutants (ENGINE-BACKLOG 1263): 27 across the 10 widgets, each the taught bug or a near miss (transpose on square matrices, no `keepdims`, no division by $n$, softmax then log, no max subtracted, `=` for `+=`, a recursive `backward`, `1 - n^2` in tanh, ReLU passing at 0, a lookup through `.data`). The validator accepts the field.
5. Playthrough: all seven files with `--local-cdn <pkgs> --mobile` (desktop and 440 px): all passed. Screens read at 440; fixes made: shorter console lines and starter comments, `wrap` on the contract console, `showIndex: false` and a caption on the bias `array`, four-place bar labels.
6. Freshness: `fresh-check.mjs --file` on review-4 and problems-4: 0 hits (a weight matrix and a slip line reused from l13 and l14 were changed). homework-4: code-name hits `Tensor`, `cross_entropy`, `backward` against l16 and homework-2, from the performance task, which rebuilds the contract's class by design.

## Proposed course.json change

None.

## autograd.py contract as shipped

`app/content/data/ai/autograd.py`, version "1.0", SHA-256 `5917d4ec91f7d1c85b8ca8ba052be5b565fa99afa3d9c08219529cdaf032bda8`, 11,277 bytes, imports NumPy only, no side effects at import, no random state. Ship it with `"files": { "autograd.py": "<exact text>" }` and `from autograd import Tensor, cross_entropy, softmax, sgd_step, grad_check, concat, unbroadcast`.

Public names (module): `__version__`, `Tensor`, `unbroadcast`, `cross_entropy`, `softmax`, `concat`, `sgd_step`, `grad_check`. Private: `_noop`, `_wrap`.

`class Tensor`
- `Tensor(data, _prev=(), _op="")`: `data` is anything `np.asarray` takes (a `Tensor` is unwrapped); `self.data = np.asarray(data, dtype=np.float64)` (no copy for a float64 array, so `sgd_step` writes through to it); `self.grad = np.zeros_like(self.data)`; `self._prev` a tuple; `self._op` a string; `self._backward` a no-argument callable. `__array_ufunc__ = None`, so `ndarray (op) Tensor` and NumPy scalars on the left give a `Tensor`. `repr` is `Tensor(shape=..., op=...)`.
- Properties: `shape` (`data.shape`); `T` (a new tensor in the graph, NumPy's `.T`: the transpose of a 2-D tensor, all axes reversed for more).
- `item()`: a Python float for a size-1 tensor, else `ValueError`.
- Operators, each a new tensor; numbers and arrays are wrapped as constants; NumPy broadcasting forward, `unbroadcast` backward: `a + b`, `b + a`, `a - b`, `b - a`, `-a`, `a * b`, `b * a`, `a / b`, `b / a`, `a ** k` (`k` a number; a `Tensor` power raises `TypeError`), `a @ b` and `b @ a` (both at least 2-D, else `ValueError`; backward $\mathbf{G}\mathbf{B}^T$ and $\mathbf{A}^T\mathbf{G}$; stacks broadcast as `np.matmul`, so `(B, n, k) @ (k, m)` works and the weight gradient sums over the batch).
- Methods, each a new tensor: `sum(axis=None, keepdims=False)`, `mean(axis=None, keepdims=False)` (axis an int, negative or a tuple), `tanh()`, `relu()` (slope 0 at exactly 0), `exp()`, `log()`, `reshape(*shape)` (also `reshape((a, b))` and `-1`), indexing `a[idx]` with an integer array, a tuple of them, slices or a mix (backward `np.add.at`, so repeats add; a `Tensor` index raises `TypeError`).
- `backward()`: size-1 only, else `ValueError`; sets its own `grad` to ones, orders the graph with an explicit stack (no recursion: checked at 5,000 steps with the recursion limit at 150), runs each `_backward` in reverse. Gradients accumulate with `+=`; calling `backward()` twice on one graph adds twice.
- `zero_grad()`: zeroes `grad` in place (a fresh array if `data` changed shape).

Functions
- `unbroadcast(grad, shape) -> ndarray`: sums the leading axes broadcasting added, then every axis where `shape` has 1 (kept); `shape` may be `()`.
- `cross_entropy(logits, targets) -> Tensor` (shape `()`): `logits` a 2-D tensor or array `(n, K)`; `targets` a 1-D integer array or list of length `n` (else `ValueError`; a float dtype raises `TypeError`); mean over rows of $-\ln \operatorname{softmax}(z_r)_{y_r}$ in nats by log-sum-exp; one fused backward $(\mathbf{P} - \mathbf{Y})/n$. Stable at logits near 1000 and at $(0, -800)$ (gives 800).
- `softmax(x, axis=-1) -> ndarray`: a plain array (a `Tensor` is read through `.data`), max subtracted, no gradient.
- `concat(tensors, axis=0) -> Tensor`: numbers or arrays are wrapped; negative `axis` works; backward hands each its slice.
- `sgd_step(params, lr)`: `p.data -= lr * p.grad` in place; does not zero gradients.
- `grad_check(f, params, h=1e-5) -> float`: zeroes every parameter's gradient, runs `f().backward()`, then central differences over every entry of every parameter's `data` (restored), and returns $\max|g_{bp} - g_{num}| / \max(\max|g_{bp}|, \max|g_{num}|, 10^{-12})$. The analytic gradients stay in `grad` afterwards.

Ops present: every op the contract lists; none is missing. Not present (later courses write them in their own ops modules, per the contract's growth rule): a differentiable softmax on a `Tensor` (compose it from `exp`, `sum`, `/`, subtracting `Tensor(x.data.max(axis, keepdims=True))` as a constant), a transpose of chosen axes or of the last two axes (`T` reverses all axes, so batched attention's $\mathbf{K}^T$ needs a `swapaxes` op), `max` and max-pooling, `stack`, `sigmoid`, `abs`, `sqrt` (use `** 0.5`), `var` and layer norm (compose from `mean`, `-`, `**`), a masked fill (add a constant mask of $-10^9$), dropout, `where`, and comparison operators. The l16 timing above used a 3-line last-two-axes transpose in the benchmark, as a `gpt` ops module would.
