# cnn levels 1 and 2 (Convolutional networks): second-reader findings

Scope: `app/content/courses/cnn/` level 1 (`l1` to `l4`, `review-1`, `homework-1`, `problems-1`) and level 2 (`l5` to `l8`, `review-2`, `homework-2`, `problems-2`), and the shared modules `app/content/data/ai/cnn_ops_l1.py` and `cnn_ops_l2.py`, at `256cfc6b`.
Method: every op of both modules gradient-checked by my own central differences in float64 (h = 1e-6, 37 cases: odd and even sides, non-square images and kernels, 1 by 1 and image-sized kernels, 1 to 3 channels, batches of 1 to 3, stride 1 to 3 including strides that do not divide, padding 0 to 2, a 3-D input, max pooling with ties) and their forward passes checked against plain loops, `np.correlate` and the im2col/col2im adjoint identity; both number scripts run with the venv Python (357 of 357 and 331 of 331, exit 0); `grade-all.mjs --file <f> --code` under the local Pyodide on all 14 files (137 widgets, 28 Python code widgets, 0 failures); 85 wrong solutions of my own plus, for every code widget, the model solution with the starter's comments kept, run through the real grader as `mutants` on scratch copies (appendix); every stated number, distractor and tolerance recomputed by hand or in NumPy; `validate.mjs` (0 errors) and `voice-scan.py 35` (0 over 35 words, 0 explanations over three sentences); prose read for false or loose claims, American spelling, em-dashes and exclamation marks (none found).
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, teaching issue or a test that misses what it claims; note = style or small gap.

Counts: 0 errors in the ops modules; content 5 errors, 12 warnings, 10 notes (3 of the notes on the ops modules).

## Ops modules (`cnn_ops_l1.py`, `cnn_ops_l2.py`)

Both are correct. Largest elementwise relative error |a - b| / (|a| + |b|) against my central differences, over every input of every case: `cnn_ops_l1.conv1d` 7.6e-10, `cnn_ops_l1.conv2d` 2.1e-7, `cnn_ops_l2.conv2d` (input, filters and bias) 1.3e-7, `maxpool2d` 1.8e-8, `avgpool2d` 1.3e-8, all below the brief's 1e-6 (the authors' norm-based figures of about 1e-10 are the same result on a gentler metric). Forward passes match loops to 1.8e-15 (level 1) and 7.1e-15 (level 2, bias included); `im2col` and `col2im` satisfy <im2col(x), C> = <x, col2im(C)> to 7e-15 at every stride and padding tried, including stride 2 with padding 1 and stride 3 that drops the last columns. `cnn_ops_l2.conv2d` on one channel with zero bias equals `cnn_ops_l1.conv2d` to 4.4e-16. Both modules compute the unflipped sliding dot product (cross-correlation), which is what every lesson calls convolution; `conv1d([0, 1, 2, 3], [1, 0, -1])` gives (-2, -2), the correlation. Max pooling routes each gradient to the first maximum in row-major order: on the window (3, 3; 1, 0) the gradient lands on the top-left 3, as l6 and its test say. A 3-D input comes back without the batch axis and its gradient has the input's shape; a tensor used twice accumulates its gradient (checked). Shape errors raise `ValueError` with a clear message (a map that does not split into windows, a kernel larger than the padded input, filters with the wrong channel count).

- app/content/data/ai/cnn_ops_l2.py | conv2d | note | The bias shape is never checked: a bias of shape (1,) for 3 filters passes the forward pass by broadcasting and fails only at `backward()` with NumPy's "non-broadcastable output operand". Level 3 learners will meet this as an autograd error far from its cause. | In a new level module (this one is frozen), or in level 3's own code, check `b.shape == (f,)` and raise `ValueError` naming the filter count.
- app/content/data/ai/cnn_ops_l2.py | out_size | note | `out_size(8, 3, 1, 0)` raises `ZeroDivisionError` and `out_size(8, 3, -1, 1)` returns 4 for a negative padding. | Raise `ValueError` for `s < 1` or `p < 0` when level 3 next touches the ops (a new module, since this one is frozen).
- app/content/data/ai/cnn_ops_l2.py | im2col, col2im | note | Level 3 builds on these: `im2col` materialises the whole (N·oh·ow, C·k²) float64 matrix, so a full-batch pass of l11's 16-to-16 3 by 3 convolution over 1,258 training digits at 8 by 8 is 92.7 MB, plus a buffer of the same size in `col2im`. That is heavy for Pyodide on a phone. | Level 3 should train and evaluate in mini-batches (64 digits is about 4.7 MB) and say so in its brief or report.

## Level 1

- app/content/courses/cnn/l2-kernels-that-detect.json | screens[8] explain | error | "$(101, 103, 101)$ centres to $\tfrac43(-1, 2, -1)$": its mean is 101.67, so it centres to $(-\tfrac23, \tfrac43, -\tfrac23) = \tfrac23(-1, 2, -1)$, exactly the centred kernel (feedback.correct says $\tfrac23$). The window's bump of 2 is also the kernel's, so "the size 2 do not matter" shows no scale invariance. | Make option a $(101, 105, 101)$, which centres to $\tfrac43(-1, 2, -1)$, and keep the explain; set feedback.correct to "Centred, $(101, 105, 101)$ is $\tfrac43(-1, 2, -1)$, the same direction as the centred kernel."
- app/content/courses/cnn/l3-convolution-in-2d.json | screens[0] hints[2] | error | "At (1, 3): right column $4 + 4 + 0$ less left column $4 + 0 + 0$" gives 4; the right column of that window is (4, 4, 1), so the output is 9 - 4 = 5, the key. A learner who follows the hint is marked wrong. | "At (1, 3): right column $4 + 4 + 1$ less left column $4 + 0 + 0$."
- app/content/courses/cnn/homework-1.json | items[1] h-full-convolution, test 5 | error | The starter's own comment, "equal to np.convolve(x, k) in full mode", contains `convolve`, and test 5 is `'convolve' not in __learner_source__`. The model solution with the starter's comments kept fails test 5 (run in Pyodide); there is no `test-5` feedback line, so the learner sees only the generic miss. | Reword the comment ("equal to NumPy's full convolution of x and k") and make the check ignore comments, e.g. `not any(isinstance(n, ast.Attribute) and n.attr in ('convolve', 'correlate') for n in ast.walk(ast.parse(__learner_source__)))` with `import ast` in the setup.
- app/content/courses/cnn/l2-kernels-that-detect.json | screens[11] detect, test 4 | warning | The `how` says test 4 checks "flat windows (no division by zero)", but an unguarded `w @ kc / (norm(w) * norm(kc))` passes every test: 0/0 gives `nan`, and `nan > 0.5` is False, the same verdict as the guarded 0. The guard is never tested (appendix W4). | Add a case with a negative threshold, e.g. `detect([5.0, 5.0, 5.0, 9.0, 5.0], [1, 3, 1], -0.6)` expecting `[0, 1, 2]`: the flat window 0 scores 0, above $-0.6$, and the unguarded version returns `[1, 2]` (checked).
- app/content/courses/cnn/l2-kernels-that-detect.json | screens[10] second_difference, test 5 | warning | The brief makes `np.convolve` "the check, never the answer, in the code screens", but only `diff` is banned: `np.convolve(x, [1.0, -2.0, 1.0], 'valid')` passes every test (the symmetric kernel hides the flip). | Ban `convolve` and `correlate` as `conv1d_valid`'s screen does, with the comment-proof check above.
- app/content/courses/cnn/l4-learning-a-kernel.json | screens[10] prose | warning | "Return $\max\lvert g - g_{\text{num}} \rvert$ over the larger of the two largest sizes" does not parse; only the canvas shows the relative error. The tests cannot tell it from the absolute error either: `float(np.abs(g - num).max())` passes all five (appendix W1), because every gradient here is of order 1. | "Return $\max\lvert g - g_{\text{num}} \rvert$ divided by the larger of $\max\lvert g \rvert$ and $\max\lvert g_{\text{num}} \rvert$." Add a test on `x * 1e4` (gradient about $10^8$, absolute gap about $10^{-3}$, relative about $10^{-11}$) asserting `< 1e-6`.
- app/content/courses/cnn/l4-learning-a-kernel.json | screens[10] kernel_gradient_check, test 4 | warning | `type(...).__name__ == 'float'` fails a correct solution that returns `np.abs(g - num).max() / scale`, an `np.float64` (appendix W2, run in Pyodide). The prompt never asks for a Python float, and there is no `test-4` feedback line. | `isinstance(kernel_gradient_check(x, k), float)` (true for `np.float64`), or say "as a Python `float`" in the prompt and add a `test-4` line.
- app/content/courses/cnn/l4-learning-a-kernel.json | screens[5] prose and option b why | note | "The loss grew a thousandfold in one step": 92 to 198,403 is about 2,200 times. | "more than two thousandfold".
- app/content/courses/cnn/l4-learning-a-kernel.json | screens[7] option c why | note | "The output is half of the error" is not a statement about anything; the error is the output minus the target. | "The output is only part of the error, $\hat y_t - y_t$; without the target the gradient never reaches 0."
- app/content/courses/cnn/l4-learning-a-kernel.json | screens[9] explain | note | "100 steps take tens of milliseconds": the report measured 0.05 s in CPython only; Pyodide is slower by a factor the report does not give. | "100 steps take well under a second", or measure in Pyodide.
- app/content/courses/cnn/l1-rolling-mean-is-convolution.json, l4-learning-a-kernel.json | l1 screens[7] or [6]; l4 screens[11] | note | The brief's one-sentence links are missing: in l1, that the density of a sum is a convolution (`limits-thm` l16); in l4's transfer, that an AR model is `arma`'s. | One sentence each, e.g. l1 explain: "The same sum gave the density of $X + Y$ in `limits-thm`: a density slid against a reversed density."
- app/content/courses/cnn/homework-1.json | items[0] h-perf-conv2d | note | Every hidden image is square, so a solution that takes the width from the height passes all 7 (appendix W2). The spec says $n$ by $n$, so this is not wrong, but a rectangular case costs nothing. | Add a $(2, 5, 7)$ image with $(3, 2, 3, 3)$ kernels against the loop-free reference.

## Level 2

- app/content/courses/cnn/l8-im2col.json | screens[9] conv2d_im2col, test 5 | error | Test 5 is `__learner_source__.count('for ') == 0`, and the starter's own comment, "im2col(x, k, stride, pad) is defined for you", contains "for ". The model solution with the starter's comments kept fails test 5, and so does a correct solution with any comment such as "one product for all the maps" (both run in Pyodide). The learner is told "Use one matrix product", which they did. | Check the syntax tree instead: `not any(isinstance(n, (ast.For, ast.While, ast.comprehension)) for n in ast.walk(ast.parse(__learner_source__)))` with `import ast` in the setup.
- app/content/courses/cnn/homework-2.json | items[3] h-design-10k model, "Where the parameters go" | error | "widening the last conv to 32 filters would add 2,320 conv parameters and double the head to 5,130, about 12,500 in all": $80 + 1{,}168 + 4{,}640 + 5{,}130 = 11{,}018$ (6,138 + 2,320 + 2,560). The conclusion, over budget, stands. | "about 11,000 in all, over budget".
- app/content/courses/cnn/homework-2.json | items[3] h-design-10k model, last sentence | warning | "Multiply-adds are dominated by the first two layers, which run on the largest maps": per layer they are 73,728, 294,912, 147,456 and 2,560, so the second and third convolutions hold 85% and the first only 14%. | "Multiply-adds peak in the second conv (294,912 of 518,656), where 16 filters meet 8 channels on a 16 by 16 map; parameters peak in the head."
- app/content/courses/cnn/l5-stride-and-padding.json | screens[10] explain | warning | "With $p = 1$ and $s = 2$ the 9 by 9 image gives $\lfloor 9/2 \rfloor + 1 = 5$": the right number from the wrong expression, on the screen that teaches the formula. | "$\lfloor (9 + 2 - 3)/2 \rfloor + 1 = 5$."
- app/content/courses/cnn/l6-pooling.json | screens[2] prose; screens[5] option d why | warning | "both tolerate a small shift a little, as the left windows did": under this shift every average-pooled value changes (2.5 to 1.25, 1 to 2, 1.5 to 0.75, 3.25 to 2), the left windows included. Option d's why says only "each right-hand window now holds different values". | screens[2]: "Max pooling kept the left windows through this shift; average pooling moves a little with every shift." Option d why: "All four averages changed: 2.5 became 1.25 in the top-left window."
- app/content/courses/cnn/l7-counting-parameters.json | screens[3] explain | warning | "a convolution is cheap to store and not to run" contradicts the table beside it: 9,216 multiply-adds against the dense layer's 65,536. | "Each of the 144 weights is used 64 times: cheap to store, and still cheaper to run than the dense layer."
- app/content/courses/cnn/l8-im2col.json | screens[3] explain | warning | "Only entries 3, 4, 5 and 7 of the kernel are non-zero": entry 1 is 1 too; it meets a 0 of the patch. | "Only entries 3, 4, 5 and 7 give non-zero products: $0 - 4 + 2 + 3 = 1$, ..."
- app/content/courses/cnn/problems-2.json | items[2] parts[1] wrong 'rows' | warning | The value 9.5 matches no slip ("Columns count window entries"). The natural slip, 9 (the rows, or one channel's window), already belongs to 'one-channel'. | Drop 'rows' and widen one-channel's line: "9 is one channel's window, or the number of rows; each row holds both channels: 18 columns."
- app/content/courses/cnn/problems-2.json | items[1] parts[2] explain | warning | "stride 2 halves the series, as a weekly sampling of overlapping windows would": weekly sampling of daily features is stride 5. | "...as sampling every other day would."
- app/content/courses/cnn/l5-stride-and-padding.json | screens[6] explain | note | "Column 9 is never the centre of a window": column 0 is never a centre either, yet it is read; the point is that column 9 is never read. | "Column 9 is never read, and PyTorch, NumPy loops and this formula all drop it without warning."
- app/content/courses/cnn/homework-2.json | items[0] h-perf-conv-layer | note | The forward pass is checked only at stride 1 (test 1): a forward pass wrong only at stride 2 passes all 8 (appendix W5). "By im2col" and "No library convolution" are not enforced: a `scipy.signal.correlate` solution passes (appendix W6). | Add a forward check on the stride-2 case of test 5; optionally ban `scipy` and `convolve` with an import and attribute scan.

## Both levels

- docs/reports/cnn-L1-numbers.py, docs/reports/cnn-L2-numbers.py | whole scripts | warning | `expect` passes when the right value appears somewhere in a string; it never asserts that every number in the string is right. The l2 and l3 errors and three level 2 slips (homework-2 model "12,500", l5 "⌊9/2⌋", l8 "entries 3, 4, 5 and 7") sit beside correct, checked values or in hints the scripts do not read. | Engine item: a `numbers_lib` mode that lists every number in a named string and fails on any not produced by the script (hints and explains included), run on each prose block with numbers; until then the fix pass checks hints by hand.

## Appendix: wrong solutions run through the grader

How: each wrong solution was added as a `mutants` entry (`test: 1`) to a scratch copy of its file and run with `node tools/grade-all.mjs --file <copy> --code --local-cdn <pkgs>`, the real Pyodide harness; the grader reports the first failing hidden test, or that the source passes every test. For every widget the first line is the model solution with the starter's comment lines kept inside the function, as a learner who types into the starter leaves them; two such correct solutions fail (l8 screens[9] and homework-1 items[1]). Results: 85 wrong solutions, 79 caught (listed with the test they fail first) and 6 that survive (l2 `second_difference` W1, l2 `detect` W4, l4 `kernel_gradient_check` W1, homework-1 `conv2d` W2, homework-2 `conv_layer_forward_backward` W5 and W6); 9 further "survivors" are correct alternatives, marked as such. The classes asked for are all caught: a flipped kernel (l4 `conv1d_backward` W1 and `learn_kernel` W2, l5 `conv2d` W4; the authors' mutants cover it in l1, l3 and homework-1), an output one short or one long (l1 `conv1d_valid` W1, l3 `conv2d_valid` W3, l5 `out_size` W2, homework-1 `conv1d_full` W1, homework-2 `maxpool_overlap` W1), padding on one side (l2 `pad_same` W2, l5 `conv2d` W2, l8 `im2col` W2), the stride applied to the input instead of the output (l5 `conv2d` W1, l8 `im2col` W1, homework-2 `maxpool_overlap` W2), the max-pool gradient spread to every cell (l6 `maxpool_backward` W1) and parameter counts without biases (l7 `dense_params` W2, `count_net` W1). The authors' own 83 mutants pass `grade-all` on the original files (each first fails its named test).

### l1-rolling-mean-is-convolution screens[8] `conv1d_valid` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. one window too many (n - m + 2): **fails T1**.

```python
import numpy as np


def conv1d_valid(x, k):
    x = np.asarray(x, dtype=float)
    k = np.asarray(k, dtype=float)
    n, m = len(x), len(k)
    return np.array([x[t:t + m] @ k for t in range(n - m + 2) if t + m <= n] + [0.0])
```
- W2. same-length output with zero padding: **fails T1**.

```python
import numpy as np


def conv1d_valid(x, k):
    x = np.asarray(x, dtype=float)
    k = np.asarray(k, dtype=float)
    m = len(k)
    xp = np.concatenate([np.zeros(m // 2), x, np.zeros(m - 1 - m // 2)])
    return np.array([xp[t:t + m] @ k for t in range(len(x))])
```
- W3. loop into np.zeros(n - m + 1), no guard (n - m + 1 is 0 at worst) [correct alternative]: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def conv1d_valid(x, k):
    x = np.asarray(x, dtype=float)
    k = np.asarray(k, dtype=float)
    n, m = len(x), len(k)
    out = np.zeros(n - m + 1)
    for t in range(n - m + 1):
        out[t] = x[t:t + m] @ k
    return out
```

### l1-rolling-mean-is-convolution screens[9] `rolling_mean_as_conv` (5 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. output on the window centre: **fails T1**.

```python
import numpy as np
import pandas as pd


def rolling_mean_as_conv(close, n):
    y = conv1d_valid(close.to_numpy(), np.ones(n) / n)
    h = (n - 1) // 2
    vals = np.concatenate([np.full(h, np.nan), y, np.full(n - 1 - h, np.nan)])
    return pd.Series(vals, index=close.index)
```
- W2. n NaNs and the last mean dropped: **fails T1**.

```python
import numpy as np
import pandas as pd


def rolling_mean_as_conv(close, n):
    y = conv1d_valid(close.to_numpy(), np.ones(n) / n)
    vals = np.concatenate([np.full(n, np.nan), y[:-1]])
    return pd.Series(vals, index=close.index)
```
- W3. a NumPy array, not a Series: **fails T1**.

```python
import numpy as np
import pandas as pd


def rolling_mean_as_conv(close, n):
    y = conv1d_valid(close.to_numpy(), np.ones(n) / n)
    return np.concatenate([np.full(n - 1, np.nan), y])
```

### l1-rolling-mean-is-convolution screens[10] `ewm_kernel` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. weights alpha ** lag (decay rate swapped): **fails T4**.

```python
import numpy as np


def ewm_kernel(alpha, length):
    w = alpha ** np.arange(length)
    return (w / w.sum())[::-1]
```
- W2. unnormalised pandas form, newest last: **fails T1**.

```python
import numpy as np


def ewm_kernel(alpha, length):
    return (alpha * (1 - alpha) ** np.arange(length))[::-1]
```

### l2-kernels-that-detect screens[9] `pad_same` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. even kernel: extra value on the left: **fails T3**.

```python
import numpy as np


def pad_same(x, k_len, mode):
    x = np.asarray(x, dtype=float)
    left = k_len // 2
    right = k_len - 1 - left
    if mode == 'zero':
        return np.concatenate([np.zeros(left), x, np.zeros(right)])
    if mode == 'edge':
        return np.concatenate([np.full(left, x[0]), x, np.full(right, x[-1])])
    raise ValueError(mode)
```
- W2. all padding on one side (right): **fails T1**.

```python
import numpy as np


def pad_same(x, k_len, mode):
    x = np.asarray(x, dtype=float)
    if mode == 'zero':
        return np.concatenate([x, np.zeros(k_len - 1)])
    if mode == 'edge':
        return np.concatenate([x, np.full(k_len - 1, x[-1])])
    raise ValueError(mode)
```
- W3. edge pads with x[0] both sides: **fails T2**.

```python
import numpy as np


def pad_same(x, k_len, mode):
    x = np.asarray(x, dtype=float)
    left = (k_len - 1) // 2
    right = k_len - 1 - left
    if mode == 'zero':
        return np.concatenate([np.zeros(left), x, np.zeros(right)])
    if mode == 'edge':
        return np.concatenate([np.full(left, x[0]), x, np.full(right, x[0])])
    raise ValueError(mode)
```

### l2-kernels-that-detect screens[10] `second_difference` (5 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. np.convolve with the bend kernel (library call, symmetric kernel): **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def second_difference(x):
    return np.convolve(np.asarray(x, dtype=float), [1.0, -2.0, 1.0], 'valid')
```
- W2. change kernel applied twice [correct alternative]: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def second_difference(x):
    return conv1d_valid(conv1d_valid(x, [-1.0, 1.0]), [-1.0, 1.0])
```
- W3. same-length output (zero padded): **fails T1**.

```python
import numpy as np


def second_difference(x):
    x = np.concatenate([[0.0], np.asarray(x, dtype=float), [0.0]])
    return conv1d_valid(x, [1.0, -2.0, 1.0])
```

### l2-kernels-that-detect screens[11] `detect` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. kernel not centred (norm of raw kernel): **fails T4**.

```python
import numpy as np


def detect(x, k, threshold):
    x = np.asarray(x, dtype=float)
    k = np.asarray(k, dtype=float)
    m = len(k)
    hits = []
    for t in range(len(x) - m + 1):
        w = x[t:t + m] - x[t:t + m].mean()
        d = np.linalg.norm(w) * np.linalg.norm(k)
        r = 0.0 if d == 0 else (w @ k) / d
        if r > threshold:
            hits.append(t)
    return hits
```
- W2. reports the window centre t + m // 2: **fails T1**.

```python
import numpy as np


def detect(x, k, threshold):
    x = np.asarray(x, dtype=float)
    k = np.asarray(k, dtype=float)
    m = len(k)
    kc = k - k.mean()
    hits = []
    for t in range(len(x) - m + 1):
        w = x[t:t + m] - x[t:t + m].mean()
        d = np.linalg.norm(w) * np.linalg.norm(kc)
        r = 0.0 if d == 0 else (w @ kc) / d
        if r > threshold:
            hits.append(t + m // 2)
    return hits
```
- W3. np.corrcoef per window (flat window gives nan) [correct alternative]: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def detect(x, k, threshold):
    x = np.asarray(x, dtype=float)
    k = np.asarray(k, dtype=float)
    m = len(k)
    hits = []
    with np.errstate(all='ignore'):
        for t in range(len(x) - m + 1):
            r = np.corrcoef(x[t:t + m], k)[0, 1]
            if r > threshold:
                hits.append(t)
    return hits
```
- W4. flat windows divide by zero (no guard): **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def detect(x, k, threshold):
    x = np.asarray(x, dtype=float)
    k = np.asarray(k, dtype=float)
    m = len(k)
    kc = k - k.mean()
    hits = []
    for t in range(len(x) - m + 1):
        w = x[t:t + m] - x[t:t + m].mean()
        r = (w @ kc) / (np.linalg.norm(w) * np.linalg.norm(kc))
        if r > threshold:
            hits.append(t)
    return hits
```

### l3-convolution-in-2d screens[8] `conv2d_valid` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. kernel transposed: **fails T1**.

```python
import numpy as np


def conv2d_valid(img, k):
    img = np.asarray(img, dtype=float)
    k = np.asarray(k, dtype=float).T
    kh, kw = k.shape
    oh, ow = img.shape[0] - kh + 1, img.shape[1] - kw + 1
    out = np.zeros((oh, ow))
    for i in range(oh):
        for j in range(ow):
            out[i, j] = np.sum(img[i:i + kh, j:j + kw] * k)
    return out
```
- W2. square kernel assumed (kw = kh): **fails T3**.

```python
import numpy as np


def conv2d_valid(img, k):
    img = np.asarray(img, dtype=float)
    k = np.asarray(k, dtype=float)
    kh = kw = k.shape[0]
    oh, ow = img.shape[0] - kh + 1, img.shape[1] - kw + 1
    out = np.zeros((oh, ow))
    for i in range(oh):
        for j in range(ow):
            out[i, j] = np.sum(img[i:i + kh, j:j + kw] * k)
    return out
```
- W3. output size off by one (n - k): **fails T1**.

```python
import numpy as np


def conv2d_valid(img, k):
    img = np.asarray(img, dtype=float)
    k = np.asarray(k, dtype=float)
    kh, kw = k.shape
    oh, ow = img.shape[0] - kh, img.shape[1] - kw
    out = np.zeros((oh, ow))
    for i in range(oh):
        for j in range(ow):
            out[i, j] = np.sum(img[i:i + kh, j:j + kw] * k)
    return out
```

### l3-convolution-in-2d screens[9] `conv2d_multi` (5 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. each kernel transposed: **fails T2**.

```python
import numpy as np


def conv2d_multi(img, kernels):
    return np.stack([conv2d_valid(img, np.asarray(k).T) for k in kernels])
```
- W2. a list of maps, not an array: **fails T1**.

```python
import numpy as np


def conv2d_multi(img, kernels):
    return [conv2d_valid(img, k) for k in kernels]
```

### l3-convolution-in-2d screens[10] `edge_map` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. larger of |gx| and |gy|: **fails T1**.

```python
import numpy as np


def edge_map(img):
    kv = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=float)
    return np.maximum(np.abs(conv2d_valid(img, kv)), np.abs(conv2d_valid(img, kv.T)))
```
- W2. squared magnitude, no root: **fails T1**.

```python
import numpy as np


def edge_map(img):
    kv = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=float)
    return conv2d_valid(img, kv) ** 2 + conv2d_valid(img, kv.T) ** 2
```
- W3. gy from the row-reversed kernel (kv[::-1], same as kv): **fails T1**.

```python
import numpy as np


def edge_map(img):
    kv = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=float)
    gx = conv2d_valid(img, kv)
    gy = conv2d_valid(img, kv[::-1])
    return np.sqrt(gx ** 2 + gy ** 2)
```
- W4. flipped kernels (true convolution; magnitude is sign-blind) [correct alternative]: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def edge_map(img):
    kv = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=float)
    gx = conv2d_valid(img, kv[::-1, ::-1])
    gy = conv2d_valid(img, kv.T[::-1, ::-1])
    return np.sqrt(gx ** 2 + gy ** 2)
```

### l4-learning-a-kernel screens[8] `conv1d_backward` (5 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. dx by np.convolve with the flipped kernel: **fails T4**.

```python
import numpy as np


def conv1d_backward(x, k, dout):
    x = np.asarray(x, dtype=float)
    k = np.asarray(k, dtype=float)
    dout = np.asarray(dout, dtype=float)
    dx = np.convolve(dout, k[::-1])
    dk = np.array([dout @ x[j:j + len(dout)] for j in range(len(k))])
    return dx, dk
```
- W2. MSE factor 2/m left in: **fails T1**.

```python
import numpy as np


def conv1d_backward(x, k, dout):
    x = np.asarray(x, dtype=float)
    k = np.asarray(k, dtype=float)
    dout = np.asarray(dout, dtype=float)
    m = len(k)
    dx = np.zeros_like(x)
    dk = np.zeros_like(k)
    c = 2 / len(dout)
    for t in range(len(dout)):
        dx[t:t + m] += c * dout[t] * k
        dk += c * dout[t] * x[t:t + m]
    return dx, dk
```
- W3. returns (dk, dx), order swapped: **fails T1**.

```python
import numpy as np


def conv1d_backward(x, k, dout):
    x = np.asarray(x, dtype=float)
    k = np.asarray(k, dtype=float)
    dout = np.asarray(dout, dtype=float)
    m = len(k)
    dx = np.zeros_like(x)
    dk = np.zeros_like(k)
    for t in range(len(dout)):
        dx[t:t + m] += dout[t] * k
        dk += dout[t] * x[t:t + m]
    return dk, dx
```

### l4-learning-a-kernel screens[9] `learn_kernel` (4 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. starts from ones, not zeros: **fails T4**.

```python
import numpy as np
from autograd import Tensor, sgd_step
from cnn_ops_l1 import conv1d


def learn_kernel(x, y, k_len, lr, steps):
    k = Tensor(np.ones(k_len))
    xt = Tensor(x)
    for _ in range(steps):
        k.zero_grad()
        loss = ((conv1d(xt, k) - y) ** 2).mean()
        loss.backward()
        sgd_step([k], lr)
    return k.data.copy()
```
- W2. returns the learned kernel flipped (np.convolve order): **fails T1**.

```python
import numpy as np
from autograd import Tensor, sgd_step
from cnn_ops_l1 import conv1d


def learn_kernel(x, y, k_len, lr, steps):
    k = Tensor(np.zeros(k_len))
    xt = Tensor(x)
    for _ in range(steps):
        k.zero_grad()
        loss = ((conv1d(xt, k) - y) ** 2).mean()
        loss.backward()
        sgd_step([k], lr)
    return k.data[::-1].copy()
```
- W3. returns the Tensor, not an array: **fails T1**.

```python
import numpy as np
from autograd import Tensor, sgd_step
from cnn_ops_l1 import conv1d


def learn_kernel(x, y, k_len, lr, steps):
    k = Tensor(np.zeros(k_len))
    xt = Tensor(x)
    for _ in range(steps):
        k.zero_grad()
        loss = ((conv1d(xt, k) - y) ** 2).mean()
        loss.backward()
        sgd_step([k], lr)
    return k
```

### l4-learning-a-kernel screens[10] `kernel_gradient_check` (5 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. absolute error, not relative: **SURVIVES (passes every hidden test)**.

```python
import numpy as np
from autograd import Tensor, sgd_step
from cnn_ops_l1 import conv1d


def kernel_gradient_check(x, k):
    xt = Tensor(x)
    kt = Tensor(np.array(k, dtype=float))
    loss = lambda: (conv1d(xt, kt) ** 2).mean()
    loss().backward()
    g = kt.grad.copy()
    num = np.zeros_like(g)
    h = 1e-5
    for j in range(len(g)):
        keep = kt.data[j]
        kt.data[j] = keep + h
        up = loss().item()
        kt.data[j] = keep - h
        down = loss().item()
        kt.data[j] = keep
        num[j] = (up - down) / (2 * h)
    return float(np.abs(g - num).max())
```
- W2. correct, but returns np.float64: **fails T4**.

```python
import numpy as np
from autograd import Tensor, sgd_step
from cnn_ops_l1 import conv1d


def kernel_gradient_check(x, k):
    xt = Tensor(x)
    kt = Tensor(np.array(k, dtype=float))
    loss = lambda: (conv1d(xt, kt) ** 2).mean()
    loss().backward()
    g = kt.grad.copy()
    num = np.zeros_like(g)
    h = 1e-5
    for j in range(len(g)):
        keep = kt.data[j]
        kt.data[j] = keep + h
        up = loss().item()
        kt.data[j] = keep - h
        down = loss().item()
        kt.data[j] = keep
        num[j] = (up - down) / (2 * h)
    return np.abs(g - num).max() / max(np.abs(g).max(), np.abs(num).max())
```
- W3. h = 1e-2 (loss is quadratic, so still exact) [correct alternative]: **SURVIVES (passes every hidden test)**.

```python
import numpy as np
from autograd import Tensor, sgd_step
from cnn_ops_l1 import conv1d


def kernel_gradient_check(x, k):
    xt = Tensor(x)
    kt = Tensor(np.array(k, dtype=float))
    loss = lambda: (conv1d(xt, kt) ** 2).mean()
    loss().backward()
    g = kt.grad.copy()
    num = np.zeros_like(g)
    h = 1e-2
    for j in range(len(g)):
        keep = kt.data[j]
        kt.data[j] = keep + h
        up = loss().item()
        kt.data[j] = keep - h
        down = loss().item()
        kt.data[j] = keep
        num[j] = (up - down) / (2 * h)
    return float(np.abs(g - num).max() / max(np.abs(g).max(), np.abs(num).max()))
```

### homework-1 items[0] `conv2d` (7 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. one bias for every map (bias summed): **fails T1**.

```python
import numpy as np


def conv2d(img, kernels, bias):
    img = np.asarray(img, dtype=float)
    kernels = np.asarray(kernels, dtype=float)
    c_out, c_in, kh, kw = kernels.shape
    oh, ow = img.shape[1] - kh + 1, img.shape[2] - kw + 1
    out = np.zeros((c_out, oh, ow))
    for o in range(c_out):
        for i in range(oh):
            for j in range(ow):
                out[o, i, j] = np.sum(img[:, i:i + kh, j:j + kw] * kernels[o])
    return out + np.sum(bias)
```
- W2. width taken from the height (square images assumed): **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def conv2d(img, kernels, bias):
    img = np.asarray(img, dtype=float)
    kernels = np.asarray(kernels, dtype=float)
    c_out, c_in, kh, kw = kernels.shape
    oh = ow = img.shape[1] - kh + 1
    out = np.zeros((c_out, oh, ow))
    for o in range(c_out):
        for i in range(oh):
            for j in range(ow):
                out[o, i, j] = np.sum(img[:, i:i + kh, j:j + kw] * kernels[o]) + bias[o]
    return out
```
- W3. bias added once per input channel: **fails T1**.

```python
import numpy as np


def conv2d(img, kernels, bias):
    img = np.asarray(img, dtype=float)
    kernels = np.asarray(kernels, dtype=float)
    c_out, c_in, kh, kw = kernels.shape
    oh, ow = img.shape[1] - kh + 1, img.shape[2] - kw + 1
    out = np.zeros((c_out, oh, ow))
    for o in range(c_out):
        for c in range(c_in):
            for i in range(oh):
                for j in range(ow):
                    out[o, i, j] += np.sum(img[c, i:i + kh, j:j + kw] * kernels[o, c]) + bias[o]
    return out
```

### homework-1 items[1] `conv1d_full` (5 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **fails T5 (a correct solution marked wrong)**.
- W1. k zeros each side (n + k + 1 values): **fails T1**.

```python
import numpy as np


def conv1d_full(x, k):
    k = np.asarray(k, dtype=float)
    z = np.zeros(len(k))
    return conv1d_valid(np.concatenate([z, np.asarray(x, dtype=float), z]), k[::-1])
```
- W2. x reversed instead of k: **fails T1**.

```python
import numpy as np


def conv1d_full(x, k):
    k = np.asarray(k, dtype=float)
    z = np.zeros(len(k) - 1)
    x = np.asarray(x, dtype=float)[::-1]
    return conv1d_valid(np.concatenate([z, x, z]), k)
```

### l5-stride-and-padding screens[9] `out_size` (7 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. kernel left out: (n + 2p) // s: **fails T1**.

```python
def out_size(n, k, p, s):
    return (n + 2 * p) // s
```
- W2. no + 1: **fails T1**.

```python
def out_size(n, k, p, s):
    return (n + 2 * p - k) // s
```
- W3. int() of true division (truncates like floor here) [correct alternative]: **SURVIVES (passes every hidden test)**.

```python
def out_size(n, k, p, s):
    return int((n + 2 * p - k) / s) + 1
```

### l5-stride-and-padding screens[10] `conv2d` (5 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. stride applied to the input, then a stride-1 slide: **fails T1**.

```python
import numpy as np


def conv2d(img, k, stride, pad):
    img = np.asarray(img, dtype=float)
    k = np.asarray(k, dtype=float)
    x = np.pad(img, pad)[::stride, ::stride]
    kh, kw = k.shape
    oh, ow = x.shape[0] - kh + 1, x.shape[1] - kw + 1
    out = np.zeros((oh, ow))
    for i in range(oh):
        for j in range(ow):
            out[i, j] = np.sum(x[i:i + kh, j:j + kw] * k)
    return out
```
- W2. all 2p of padding on the top and left: **fails T1**.

```python
import numpy as np


def conv2d(img, k, stride, pad):
    img = np.asarray(img, dtype=float)
    k = np.asarray(k, dtype=float)
    x = np.pad(img, ((2 * pad, 0), (2 * pad, 0)))
    kh, kw = k.shape
    oh = (x.shape[0] - kh) // stride + 1
    ow = (x.shape[1] - kw) // stride + 1
    out = np.zeros((oh, ow))
    for i in range(oh):
        for j in range(ow):
            r, c = i * stride, j * stride
            out[i, j] = np.sum(x[r:r + kh, c:c + kw] * k)
    return out
```
- W3. padding p on the top and left only, size from the formula, windows cropped at the far edge (equals zero padding) [correct alternative]: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def conv2d(img, k, stride, pad):
    img = np.asarray(img, dtype=float)
    k = np.asarray(k, dtype=float)
    x = np.pad(img, ((pad, 0), (pad, 0)))
    kh, kw = k.shape
    oh = (img.shape[0] + 2 * pad - kh) // stride + 1
    ow = (img.shape[1] + 2 * pad - kw) // stride + 1
    out = np.zeros((oh, ow))
    for i in range(oh):
        for j in range(ow):
            r, c = i * stride, j * stride
            win = x[r:r + kh, c:c + kw]
            out[i, j] = np.sum(win * k[:win.shape[0], :win.shape[1]])
    return out
```
- W4. kernel flipped: **fails T1**.

```python
import numpy as np


def conv2d(img, k, stride, pad):
    img = np.asarray(img, dtype=float)
    k = np.asarray(k, dtype=float)[::-1, ::-1]
    x = np.pad(img, pad)
    kh, kw = k.shape
    oh = (x.shape[0] - kh) // stride + 1
    ow = (x.shape[1] - kw) // stride + 1
    out = np.zeros((oh, ow))
    for i in range(oh):
        for j in range(ow):
            out[i, j] = np.sum(x[i * stride:i * stride + kh, j * stride:j * stride + kw] * k)
    return out
```
- W5. full stride-1 map, then every stride-th output [correct alternative]: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def conv2d(img, k, stride, pad):
    img = np.asarray(img, dtype=float)
    k = np.asarray(k, dtype=float)
    x = np.pad(img, pad)
    kh, kw = k.shape
    full = np.array([[np.sum(x[i:i + kh, j:j + kw] * k) for j in range(x.shape[1] - kw + 1)] for i in range(x.shape[0] - kh + 1)])
    return full[::stride, ::stride]
```

### l5-stride-and-padding screens[11] `padding_for_same` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. k // 2 (equal for odd k) [correct alternative]: **SURVIVES (passes every hidden test)**.

```python
def padding_for_same(k):
    if k % 2 == 0:
        raise ValueError('even')
    return k // 2
```
- W2. raises a TypeError, not ValueError: **fails T4**.

```python
def padding_for_same(k):
    if k % 2 == 0:
        raise TypeError('even')
    return (k - 1) // 2
```

### l6-pooling screens[8] `maxpool2d` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. overlapping windows at stride 1: **fails T1**.

```python
import numpy as np


def maxpool2d(x, size):
    x = np.asarray(x, dtype=float)
    return np.lib.stride_tricks.sliding_window_view(x, (size, size)).max(axis=(2, 3))


def avgpool2d(x, size):
    x = np.asarray(x, dtype=float)
    return np.lib.stride_tricks.sliding_window_view(x, (size, size)).mean(axis=(2, 3))
```
- W2. largest absolute value: **fails T3**.

```python
import numpy as np


def maxpool2d(x, size):
    x = np.asarray(x, dtype=float)
    h, w = x.shape
    return np.abs(x).reshape(h // size, size, w // size, size).max(axis=(1, 3))


def avgpool2d(x, size):
    x = np.asarray(x, dtype=float)
    h, w = x.shape
    return x.reshape(h // size, size, w // size, size).mean(axis=(1, 3))
```
- W3. average pool by max / size**2 style typo: median: **fails T2**.

```python
import numpy as np


def maxpool2d(x, size):
    x = np.asarray(x, dtype=float)
    h, w = x.shape
    return x.reshape(h // size, size, w // size, size).max(axis=(1, 3))


def avgpool2d(x, size):
    x = np.asarray(x, dtype=float)
    h, w = x.shape
    return np.median(x.reshape(h // size, size, w // size, size), axis=(1, 3))
```

### l6-pooling screens[9] `maxpool_backward` (5 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. full gradient to every cell of the window: **fails T1**.

```python
import numpy as np


def maxpool_backward(x, size, dout):
    x = np.asarray(x, dtype=float)
    dout = np.asarray(dout, dtype=float)
    return np.repeat(np.repeat(dout, size, axis=0), size, axis=1)
```
- W2. last largest entry on a tie: **fails T2**.

```python
import numpy as np


def maxpool_backward(x, size, dout):
    x = np.asarray(x, dtype=float)
    dout = np.asarray(dout, dtype=float)
    dx = np.zeros_like(x)
    for i in range(dout.shape[0]):
        for j in range(dout.shape[1]):
            win = x[i * size:(i + 1) * size, j * size:(j + 1) * size].ravel()
            a = len(win) - 1 - np.argmax(win[::-1])
            dx[i * size + a // size, j * size + a % size] += dout[i, j]
    return dx
```
- W3. a 1 at the winner, dout ignored: **fails T3**.

```python
import numpy as np


def maxpool_backward(x, size, dout):
    x = np.asarray(x, dtype=float)
    dout = np.asarray(dout, dtype=float)
    dx = np.zeros_like(x)
    for i in range(dout.shape[0]):
        for j in range(dout.shape[1]):
            win = x[i * size:(i + 1) * size, j * size:(j + 1) * size]
            a, b = np.unravel_index(np.argmax(win), win.shape)
            dx[i * size + a, j * size + b] = 1.0
    return dx
```
- W4. mask x == window max (all ties), times dout: **fails T2**.

```python
import numpy as np


def maxpool_backward(x, size, dout):
    x = np.asarray(x, dtype=float)
    dout = np.asarray(dout, dtype=float)
    h, w = x.shape
    mx = x.reshape(h // size, size, w // size, size).max(axis=(1, 3))
    up = np.repeat(np.repeat(mx, size, 0), size, 1)
    return (x == up) * np.repeat(np.repeat(dout, size, 0), size, 1)
```

### l6-pooling screens[10] `pool_shift_change` (5 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. moves the map left, not right: **fails T1**.

```python
import numpy as np


def pool_shift_change(x, size):
    x = np.asarray(x, dtype=float)
    moved = np.zeros_like(x)
    moved[:, :-1] = x[:, 1:]
    return int((maxpool2d(x, size) != maxpool2d(moved, size)).sum())
```
- W2. average pooling instead of max: **fails T1**.

```python
import numpy as np


def pool_shift_change(x, size):
    x = np.asarray(x, dtype=float)
    moved = np.zeros_like(x)
    moved[:, 1:] = x[:, :-1]
    h, w = x.shape
    ap = lambda a: a.reshape(h // size, size, w // size, size).mean(axis=(1, 3))
    return int((ap(x) != ap(moved)).sum())
```
- W3. returns the share changed, not the count: **fails T1**.

```python
import numpy as np


def pool_shift_change(x, size):
    x = np.asarray(x, dtype=float)
    moved = np.zeros_like(x)
    moved[:, 1:] = x[:, :-1]
    return float((maxpool2d(x, size) != maxpool2d(moved, size)).mean())
```

### l7-counting-parameters screens[8] `conv_params` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. a bias per input channel: **fails T1**.

```python
def conv_params(c_in, c_out, k):
    return c_out * c_in * k * k + c_in


def dense_params(n_in, n_out):
    return n_in * n_out + n_out
```
- W2. dense layer without biases: **fails T3**.

```python
def conv_params(c_in, c_out, k):
    return c_out * (c_in * k * k + 1)


def dense_params(n_in, n_out):
    return n_in * n_out
```
- W3. k counted once, not k squared: **fails T1**.

```python
def conv_params(c_in, c_out, k):
    return c_out * (c_in * k + 1)


def dense_params(n_in, n_out):
    return n_in * n_out + n_out
```

### l7-counting-parameters screens[9] `count_net` (5 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. conv without biases: **fails T1**.

```python
def count_net(layers):
    total = 0
    for layer in layers:
        if layer[0] == 'conv':
            _, c_in, c_out, k = layer
            total += c_out * c_in * k * k
        elif layer[0] == 'dense':
            _, n_in, n_out = layer
            total += n_in * n_out + n_out
    return total
```
- W2. dense bias per input: **fails T1**.

```python
def count_net(layers):
    total = 0
    for layer in layers:
        if layer[0] == 'conv':
            _, c_in, c_out, k = layer
            total += c_out * (c_in * k * k + 1)
        elif layer[0] == 'dense':
            _, n_in, n_out = layer
            total += n_in * n_out + n_in
    return total
```

### l7-counting-parameters screens[10] `receptive_field` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. stride multiplied in before the layer is added: **fails T3**.

```python
def receptive_field(layers):
    r, jump = 1, 1
    for k, s in layers:
        jump *= s
        r += (k - 1) * jump
    return r
```
- W2. sum of (k - 1) * s: **fails T3**.

```python
def receptive_field(layers):
    return 1 + sum((k - 1) * s for k, s in layers)
```

### l8-im2col screens[8] `im2col` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. stride applied to the input (subsample, then stride 1): **fails T4**.

```python
import numpy as np


def im2col(x, k, stride, pad):
    x = np.asarray(x, dtype=float)
    xp = np.pad(x, ((0, 0), (pad, pad), (pad, pad)))[:, ::stride, ::stride]
    c, h, w = xp.shape
    rows = []
    for i in range(h - k + 1):
        for j in range(w - k + 1):
            rows.append(xp[:, i:i + k, j:j + k].ravel())
    return np.array(rows)
```
- W2. padding on one side only: **fails T1**.

```python
import numpy as np


def im2col(x, k, stride, pad):
    x = np.asarray(x, dtype=float)
    xp = np.pad(x, ((0, 0), (0, 2 * pad), (0, 2 * pad)))
    c, h, w = xp.shape
    oh, ow = (h - k) // stride + 1, (w - k) // stride + 1
    rows = []
    for i in range(oh):
        for j in range(ow):
            rows.append(xp[:, i * stride:i * stride + k, j * stride:j * stride + k].ravel())
    return np.array(rows)
```
- W3. positions in column-major order: **fails T1**.

```python
import numpy as np


def im2col(x, k, stride, pad):
    x = np.asarray(x, dtype=float)
    xp = np.pad(x, ((0, 0), (pad, pad), (pad, pad)))
    c, h, w = xp.shape
    oh, ow = (h - k) // stride + 1, (w - k) // stride + 1
    rows = []
    for j in range(ow):
        for i in range(oh):
            rows.append(xp[:, i * stride:i * stride + k, j * stride:j * stride + k].ravel())
    return np.array(rows)
```

### l8-im2col screens[9] `conv2d_im2col` (5 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **fails T5 (a correct solution marked wrong)**.
- W1. filters reshaped (-1, F) instead of (F, -1).T: **fails T1**.

```python
import numpy as np


def conv2d_im2col(x, W, b, stride, pad):
    x = np.asarray(x, dtype=float)
    W = np.asarray(W, dtype=float)
    f, c, k, _ = W.shape
    oh = (x.shape[1] + 2 * pad - k) // stride + 1
    ow = (x.shape[2] + 2 * pad - k) // stride + 1
    y = im2col(x, k, stride, pad) @ W.reshape(-1, f) + b
    return y.T.reshape(f, oh, ow)
```
- W2. oh from the unpadded input: **fails T1**.

```python
import numpy as np


def conv2d_im2col(x, W, b, stride, pad):
    x = np.asarray(x, dtype=float)
    W = np.asarray(W, dtype=float)
    f, c, k, _ = W.shape
    oh = (x.shape[1] - k) // stride + 1
    ow = (x.shape[2] - k) // stride + 1
    y = im2col(x, k, stride, pad) @ W.reshape(f, -1).T + b
    return y.T.reshape(f, oh, ow)
```
- W3. correct, with a comment that says "for": **fails T5**.

```python
import numpy as np


def conv2d_im2col(x, W, b, stride, pad):
    # one product for all the maps
    x = np.asarray(x, dtype=float)
    W = np.asarray(W, dtype=float)
    f, c, k, _ = W.shape
    oh = (x.shape[1] + 2 * pad - k) // stride + 1
    ow = (x.shape[2] + 2 * pad - k) // stride + 1
    y = im2col(x, k, stride, pad) @ W.reshape(f, -1).T + b
    return y.T.reshape(f, oh, ow)
```

### l8-im2col screens[10] `col2im` (5 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. padding stripped with [pad:-pad] (empty at pad 0): **fails T5**.

```python
import numpy as np


def col2im(cols, x_shape, k, stride, pad):
    c, h, w = x_shape
    oh = (h + 2 * pad - k) // stride + 1
    ow = (w + 2 * pad - k) // stride + 1
    xp = np.zeros((c, h + 2 * pad, w + 2 * pad))
    cols = np.asarray(cols, dtype=float)
    for i in range(oh):
        for j in range(ow):
            xp[:, i * stride:i * stride + k, j * stride:j * stride + k] += cols[i * ow + j].reshape(c, k, k)
    return xp[:, pad:-pad, pad:-pad]
```
- W2. patch read as (k, k, c), channel last: **fails T3**.

```python
import numpy as np


def col2im(cols, x_shape, k, stride, pad):
    c, h, w = x_shape
    oh = (h + 2 * pad - k) // stride + 1
    ow = (w + 2 * pad - k) // stride + 1
    xp = np.zeros((c, h + 2 * pad, w + 2 * pad))
    cols = np.asarray(cols, dtype=float)
    for i in range(oh):
        for j in range(ow):
            xp[:, i * stride:i * stride + k, j * stride:j * stride + k] += cols[i * ow + j].reshape(k, k, c).transpose(2, 0, 1)
    return xp[:, pad:pad + h, pad:pad + w]
```
- W3. padding never stripped: **fails T1**.

```python
import numpy as np


def col2im(cols, x_shape, k, stride, pad):
    c, h, w = x_shape
    oh = (h + 2 * pad - k) // stride + 1
    ow = (w + 2 * pad - k) // stride + 1
    xp = np.zeros((c, h + 2 * pad, w + 2 * pad))
    cols = np.asarray(cols, dtype=float)
    for i in range(oh):
        for j in range(ow):
            xp[:, i * stride:i * stride + k, j * stride:j * stride + k] += cols[i * ow + j].reshape(c, k, k)
    return xp
```

### homework-2 items[0] `conv_layer_forward_backward` (8 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. db as one total over every filter: **fails T3**.

```python
import numpy as np


def conv_layer_forward_backward(x, W, b, stride, pad, dout):
    x = np.asarray(x, dtype=float)
    W = np.asarray(W, dtype=float)
    dout = np.asarray(dout, dtype=float)
    c, h, w = x.shape
    f, _, k, _ = W.shape
    xp = np.pad(x, ((0, 0), (pad, pad), (pad, pad)))
    oh = (h + 2 * pad - k) // stride + 1
    ow = (w + 2 * pad - k) // stride + 1
    cols = np.array([xp[:, i * stride:i * stride + k, j * stride:j * stride + k].ravel()
                     for i in range(oh) for j in range(ow)])
    Wm = W.reshape(f, -1)
    out = (cols @ Wm.T + b).T.reshape(f, oh, ow)
    g = dout.reshape(f, -1).T
    dW = (g.T @ cols).reshape(W.shape)
    db = dout.sum()
    dcols = g @ Wm
    dxp = np.zeros_like(xp)
    for i in range(oh):
        for j in range(ow):
            r, q = i * stride, j * stride
            dxp[:, r:r + k, q:q + k] += dcols[i * ow + j].reshape(c, k, k)
    dx = dxp[:, pad:pad + h, pad:pad + w]
    return out, dx, dW, db
```
- W2. dx stripped with [pad:-pad] (empty at pad 0): **fails T8**.

```python
import numpy as np


def conv_layer_forward_backward(x, W, b, stride, pad, dout):
    x = np.asarray(x, dtype=float)
    W = np.asarray(W, dtype=float)
    dout = np.asarray(dout, dtype=float)
    c, h, w = x.shape
    f, _, k, _ = W.shape
    xp = np.pad(x, ((0, 0), (pad, pad), (pad, pad)))
    oh = (h + 2 * pad - k) // stride + 1
    ow = (w + 2 * pad - k) // stride + 1
    cols = np.array([xp[:, i * stride:i * stride + k, j * stride:j * stride + k].ravel()
                     for i in range(oh) for j in range(ow)])
    Wm = W.reshape(f, -1)
    out = (cols @ Wm.T + b).T.reshape(f, oh, ow)
    g = dout.reshape(f, -1).T
    dW = (g.T @ cols).reshape(W.shape)
    db = g.sum(axis=0)
    dcols = g @ Wm
    dxp = np.zeros_like(xp)
    for i in range(oh):
        for j in range(ow):
            r, q = i * stride, j * stride
            dxp[:, r:r + k, q:q + k] += dcols[i * ow + j].reshape(c, k, k)
    dx = dxp[:, pad:-pad, pad:-pad] if pad else dxp[:, :0, :0]
    return out, dx, dW, db
```
- W3. dx keeps the padding: **fails T4**.

```python
import numpy as np


def conv_layer_forward_backward(x, W, b, stride, pad, dout):
    x = np.asarray(x, dtype=float)
    W = np.asarray(W, dtype=float)
    dout = np.asarray(dout, dtype=float)
    c, h, w = x.shape
    f, _, k, _ = W.shape
    xp = np.pad(x, ((0, 0), (pad, pad), (pad, pad)))
    oh = (h + 2 * pad - k) // stride + 1
    ow = (w + 2 * pad - k) // stride + 1
    cols = np.array([xp[:, i * stride:i * stride + k, j * stride:j * stride + k].ravel()
                     for i in range(oh) for j in range(ow)])
    Wm = W.reshape(f, -1)
    out = (cols @ Wm.T + b).T.reshape(f, oh, ow)
    g = dout.reshape(f, -1).T
    dW = (g.T @ cols).reshape(W.shape)
    db = g.sum(axis=0)
    dcols = g @ Wm
    dxp = np.zeros_like(xp)
    for i in range(oh):
        for j in range(ow):
            r, q = i * stride, j * stride
            dxp[:, r:r + k, q:q + k] += dcols[i * ow + j].reshape(c, k, k)
    dx = dxp
    return out, dx, dW, db
```
- W4. forward without the bias (gradients right): **fails T1**.

```python
import numpy as np


def conv_layer_forward_backward(x, W, b, stride, pad, dout):
    x = np.asarray(x, dtype=float)
    W = np.asarray(W, dtype=float)
    dout = np.asarray(dout, dtype=float)
    c, h, w = x.shape
    f, _, k, _ = W.shape
    xp = np.pad(x, ((0, 0), (pad, pad), (pad, pad)))
    oh = (h + 2 * pad - k) // stride + 1
    ow = (w + 2 * pad - k) // stride + 1
    cols = np.array([xp[:, i * stride:i * stride + k, j * stride:j * stride + k].ravel()
                     for i in range(oh) for j in range(ow)])
    Wm = W.reshape(f, -1)
    out = (cols @ Wm.T).T.reshape(f, oh, ow)
    g = dout.reshape(f, -1).T
    dW = (g.T @ cols).reshape(W.shape)
    db = g.sum(axis=0)
    dcols = g @ Wm
    dxp = np.zeros_like(xp)
    for i in range(oh):
        for j in range(ow):
            r, q = i * stride, j * stride
            dxp[:, r:r + k, q:q + k] += dcols[i * ow + j].reshape(c, k, k)
    dx = dxp[:, pad:pad + h, pad:pad + w]
    return out, dx, dW, db
```
- W5. bias added only at stride 1 (forward wrong at stride 2, never checked there): **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def conv_layer_forward_backward(x, W, b, stride, pad, dout):
    x = np.asarray(x, dtype=float)
    W = np.asarray(W, dtype=float)
    dout = np.asarray(dout, dtype=float)
    c, h, w = x.shape
    f, _, k, _ = W.shape
    xp = np.pad(x, ((0, 0), (pad, pad), (pad, pad)))
    oh = (h + 2 * pad - k) // stride + 1
    ow = (w + 2 * pad - k) // stride + 1
    cols = np.array([xp[:, i * stride:i * stride + k, j * stride:j * stride + k].ravel()
                     for i in range(oh) for j in range(ow)])
    Wm = W.reshape(f, -1)
    out = (cols @ Wm.T + (b if stride == 1 else 0)).T.reshape(f, oh, ow)
    g = dout.reshape(f, -1).T
    dW = (g.T @ cols).reshape(W.shape)
    db = g.sum(axis=0)
    dcols = g @ Wm
    dxp = np.zeros_like(xp)
    for i in range(oh):
        for j in range(ow):
            r, q = i * stride, j * stride
            dxp[:, r:r + k, q:q + k] += dcols[i * ow + j].reshape(c, k, k)
    dx = dxp[:, pad:pad + h, pad:pad + w]
    return out, dx, dW, db
```
- W6. scipy correlate, no im2col (library convolution): **SURVIVES (passes every hidden test)**.

```python
import numpy as np
from scipy.signal import correlate


def conv_layer_forward_backward(x, W, b, stride, pad, dout):
    x = np.asarray(x, dtype=float); W = np.asarray(W, dtype=float); dout = np.asarray(dout, dtype=float)
    xp = np.pad(x, ((0, 0), (pad, pad), (pad, pad)))
    f, c, k, _ = W.shape
    full = np.array([correlate(xp, W[o], 'valid')[0] for o in range(f)])
    out = full[:, ::stride, ::stride] + np.asarray(b)[:, None, None]
    up = np.zeros((f,) + full.shape[1:]); up[:, ::stride, ::stride] = dout
    dW = np.array([[correlate(xp[ci], up[o], 'valid') for ci in range(c)] for o in range(f)])
    dxp = np.zeros_like(xp)
    for o in range(f):
        for ci in range(c):
            dxp[ci] += correlate(np.pad(up[o], k - 1), W[o, ci][::-1, ::-1], 'valid')
    h, w = x.shape[1:]
    return out, dxp[:, pad:pad + h, pad:pad + w], dW, dout.sum(axis=(1, 2))
```

### homework-2 items[1] `maxpool_overlap` (5 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. no + 1 in the size: **fails T1**.

```python
import numpy as np


def maxpool_overlap(x, size, stride):
    x = np.asarray(x, dtype=float)
    oh = (x.shape[0] - size) // stride
    ow = (x.shape[1] - size) // stride
    return np.array([[x[i * stride:i * stride + size, j * stride:j * stride + size].max() for j in range(ow)] for i in range(oh)])
```
- W2. stride applied to the input, then windows at stride 1: **fails T1**.

```python
import numpy as np


def maxpool_overlap(x, size, stride):
    x = np.asarray(x, dtype=float)[::stride, ::stride]
    return np.lib.stride_tricks.sliding_window_view(x, (size, size)).max(axis=(2, 3)) if min(x.shape) >= size else np.array([[x.max()]])
```

## Fix pass

Status per finding, in the order of the review. Checks: validator 0 errors with no `[ai-mutants]` warning on cnn; voice scan 0 and 0; `cnn-L1-numbers.py` 362 of 362 and `cnn-L2-numbers.py` 333 of 333, exit 0; `grade-all.mjs --file <f> --code` 0 failures on all 11 edited files (every new mutant first fails its named test); playthrough green with and without `--mobile` on l1 to l8, homework-1 and homework-2 (`problems-2` is not playable by `--set`, so it was graded by `grade-all` only). Graded answers changed: none by value; l2 screens[8] option a now reads (101, 105, 101) (still the correct id), and problems-2 p-im2col-chain part 2 lost its `rows` wrong value (9.5).

Ops modules (not edited)
- cnn_ops_l2.py conv2d bias shape never checked | for level 3 (check `b.shape == (f,)` in level 3's own module).
- cnn_ops_l2.py out_size with s < 1 or p < 0 | for level 3 (raise `ValueError` in a new module).
- cnn_ops_l2.py im2col memory for full-batch l11 | for level 3 (train in mini-batches of about 64 and say so in its brief).

Level 1
- l2 screens[8] explain 4/3 | fixed: recomputed, the mean of (101, 103, 101) is 101.67, centre (-2/3, 4/3, -2/3) = 2/3 (-1, 2, -1); took the reviewer's route, option a is now (101, 105, 101) which centres to 4/3 (-1, 2, -1) (mean 102.33, deviations -4/3, 8/3, -4/3); feedback, explain and "size of the bump" reworded.
- l3 screens[0] hint "4 + 4 + 0" | fixed: window rows 1 to 3, columns 3 to 5, right column (4, 4, 1) = 9, left (4, 0, 0) = 4, output 5.
- homework-1 h-full-convolution test 5 | fixed: test 5 now parses `__learner_source__` and rejects an attribute or name `convolve` or `correlate`; starter comment reworded; the solution carries the starter's comments (regression); mutant `np.convolve(x, k)` fails test 5.
- l2 detect, flat window guard | fixed: test 7 `detect([5, 5, 5, 9, 5], [1, 3, 1], -0.6)` expects [0, 1, 2] (recomputed: scores 0, -0.5, 1); the unguarded mutant gives [1, 2] and fails test 7.
- l2 second_difference, `np.convolve` | fixed: test 5 bans `diff`, `convolve`, `correlate` by syntax tree; mutant `np.convolve(..., [1, -2, 1], 'valid')` fails test 5.
- l4 kernel_gradient_check prose | fixed: prose now says divided by the larger of max|g| and max|g_num|; test 6 on `x * 1e4` expects below 1e-6; mutant returning the absolute error fails test 6.
- l4 kernel_gradient_check test 4 | fixed: `isinstance(..., float)`; `np.float64` now passes.
- l4 screens[5] "thousandfold" | fixed: 198,403 / 92 = 2,156, so "more than two thousandfold".
- l4 screens[7] option c | fixed as proposed.
- l4 screens[9] "tens of milliseconds" | fixed: "well under a second".
- l1 and l4 missing links | fixed: l1 screens[6] prose links `limits-thm` (density of X + Y), l4 screens[11] prose links `arma`.
- homework-1 h-perf-conv2d square images | fixed: test 8 on a (2, 5, 7) image with (3, 2, 3, 3) kernels against the loop-free reference, shape and values; starter comment now says h by w; mutant `oh = ow = ...` fails test 8.

Level 2
- l8 screens[9] test 5 | fixed: test 5 checks the syntax tree for `For`, `While` and `comprehension` nodes; the solution carries the starter's comment (and one with "for"), so a correct commented solution is covered; a list-comprehension mutant fails test 5 (the existing loop mutant still does).
- homework-2 "about 12,500" | fixed: 80 + 1,168 + 4,640 + 5,130 = 11,018 = 6,138 + 2,320 + 2,560; now "about 11,000".
- homework-2 multiply-adds sentence | fixed: 73,728 + 294,912 + 147,456 + 2,560 = 518,656; second conv is 56.9%; sentence replaced as proposed.
- l5 screens[10] explain | fixed: (9 + 2 - 3)/2 = 4, plus 1 = 5.
- l6 screens[2] prose and screens[5] option d | fixed: recomputed the shifted map's averages 1.25, 2, 0.75, 2 (all four change from 2.5, 1, 1.5, 3.25).
- l7 screens[3] explain | fixed: 9,216 against 65,536 in the table.
- l8 screens[3] explain | fixed with a correction to the proposal: entry 3 of the kernel is 1 but meets a 0 of the patch, so the non-zero products are at entries 4, 5 and 7 only: -4 + 2 + 3 = 1 (the proposed "3, 4, 5 and 7" would still be wrong).
- problems-2 'rows' wrong value | fixed: `rows` dropped; one-channel line widened.
- problems-2 weekly sampling | fixed: "as sampling every other day would".
- l5 screens[6] explain | fixed: "Column 9 is never read" (windows start 0, 2, 4, 6 and reach column 8).
- homework-2 h-perf-conv-layer | fixed: test 9 checks the forward pass at stride 2 (bias-at-stride-1 mutant fails it); test 10 bans `convolve`, `correlate` variants and any `scipy` import by syntax tree (scipy mutant fails it).

Both levels
- numbers scripts do not check every number in a string | deferred: engine item (a `numbers_lib` mode); this pass checked every hint and explain it touched by hand.

Declined: none. Never edited: `course.json`, lesson ids, `cnn_ops_l1.py`, `cnn_ops_l2.py`.
