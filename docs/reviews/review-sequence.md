# sequence levels 1 to 3 (Sequences and Attention): second-reader findings

Scope: `app/content/courses/sequence/` levels 1 to 3 (`l1` to `l12`, `review-1` to `-3`, `homework-1` to `-3`, `problems-1` to `-3`), the modules `app/content/data/ai/seq_ops_l2.py` and `seq_ops_l3.py`, and `app/content/data/ai/sequence-attn-names.json`, at `06e60d8a`.
Method: every op of both modules gradient-checked by my own central differences in float64 (h = 1e-6, 27 cases: softmax along each axis of a 3-D array and on 1-D, scores near 1,000 and scaled by 500, arbitrary and causal `-inf` masks, a fully masked row, `swap_last` on 2-D and 4-D, `permute` with positive and negative axes, `split_heads`/`merge_heads` alone, on a batch and in a round trip, `attention` with and without a mask on a stack of heads, a whole batched causal multi-head layer, a node used twice); the three number scripts run through `run-number-scripts.mjs --only sequence` (one thread: 3 of 3 passed, 43 s) and directly with default threads and `ZQ_NUMBERS_STRICT=1` (388, 302 and 287 checks, exit 0, 0 uncovered); `sequence-L3-numbers.py --write` replayed into a scratch file under default and single threads (byte-identical to the shipped `sequence-attn-names.json` both times); the dev split checked against makemore's; `grade-all.mjs --file <f> --code --local-cdn <pkgs>` on all 21 files alone (23 Python widgets, 0 failures), every solution timed per case under the local Pyodide; 62 wrong solutions of my own run through the real grader (`tools/code-runner.mjs`, appendix); every stated number, distractor and tolerance recomputed in Python; `voice-scan.py 35` (0 over 35 words, 0 explanations over three sentences) and greps for em-dashes, exclamation marks and American spellings (none); prose read for false or loose claims.
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, teaching issue or a test that misses what it claims; note = style or small gap.

Counts: modules 1 error, 1 warning, 2 notes; number scripts 3 notes; content 1 error, 13 warnings, 12 notes. Totals: 2 errors, 14 warnings, 17 notes. Wrong solutions: 62 tried, 5 of them correct alternatives or no-ops; of the 57 wrong ones 4 survive (l3 `explodes` W2 and W3, l6 `stable_softmax` W2, l10 `leak_test` W5).

## Modules (`seq_ops_l2.py`, `seq_ops_l3.py`)

Largest relative error, max |analytic − numeric| / (max |analytic| + max |numeric|), against my central differences: `softmax` 7.8e-11 to 2.2e-10 on every axis (0, 1, 2, −1, −2) and on 1-D, 1.3e-9 at scores near 1,000, 5.3e-11 with an arbitrary `-inf` mask on axis −1 and 4.3e-10 on axis 0; `swap_last` 1.0e-10 (2-D) and 2.3e-10 (4-D); `permute` 1.0e-10 and 5.2e-11 for positive axes; `split_heads` 1.4e-10 (batch) and 9.3e-11 (2-D), `merge_heads` 1.5e-10, round trip 1.6e-10 and exact in value; `attention` 1.6e-10 unmasked (4 queries, 5 keys), 2.7e-10 causal, 4.6e-10 on a (2, 3, 5, 4) stack of heads, 4.3e-12 with scores scaled by 40; a full causal multi-head layer through `split_heads`, `attention`, `merge_heads` and `W_O` 2.5e-10, and with a batch of 2 1.4e-9; a softmax node used twice 8.8e-11. All under the brief's 1e-6. Softmax at scores scaled by 500 gave a "relative error" of 5.7e-6 only because every gradient is about 1e-78 (saturated); against the analytic Jacobian the gap is 3e-78, so it is correct. Large scores never overflow (the maximum is subtracted first); `causal_mask(32)` has 528 zeros and 496 entries at `-inf`, `causal_mask(1)` is `[[0]]`; head k of `split_heads` holds features k·d/h to (k + 1)·d/h − 1, as documented; width not divisible by h and `swap_last` on 1-D raise `ValueError` with clear messages.

- app/content/data/ai/seq_ops_l3.py | permute | error | The docstring promises `np.transpose(x, axes)`, but the backward inverts the order with `np.argsort(axes)`, which is wrong for negative axes. On a (3, 3, 3) array, `permute(x, (-1, 0, 1))` and `permute(x, (0, -1, -2))` return the right forward values and a silently wrong gradient; on (2, 3, 4) the same calls crash in `backward()` with a broadcast error. No current caller passes negative axes, but `gpt` and `interp` import this module frozen. | The module is frozen, so in the next ops module (or a documented wrapper): `axes = tuple(int(a) % x.data.ndim for a in axes)` before `argsort`; until then state "non-negative axes only" in the module's README line and in the `gpt` and `interp` briefs.
- app/content/data/ai/seq_ops_l2.py | softmax (and seq_ops_l3.attention) | warning | A row with every entry at `-inf` (a fully masked query) gives NaN in the forward pass and NaN gradients for that row (`invalid value encountered in subtract`). A causal mask never does this, but a padding or key mask in `gpt` batching or an ablation mask in `interp` can. | Document it beside `causal_mask`; if a later course needs padding, add `masked_softmax` in a new module that sets a fully masked row's weights and gradient to 0.
- app/content/data/ai/seq_ops_l2.py | softmax name | note | `autograd.softmax` (v1.0) is a plain-array softmax with no gradient and the same name. `from autograd import *` after `from seq_ops_l2 import softmax` silently swaps it in; my l7 W1 shows the result: every `W_Q` and `W_K` gradient is 0. | One sentence in the modules README and AUTHORING section 9: import `softmax` from `seq_ops_l2` by name, never `autograd`'s with `*`.
- app/content/data/ai/seq_ops_l3.py | attention, permute | note | A `Tensor` mask raises NumPy's "setting an array element with a sequence"; `permute(x, None)` raises `TypeError: 'NoneType' object is not iterable`. | Say "`mask` is a NumPy array" and "`axes` is required" in the docstrings of the next module.

## Number scripts and the weights file

All three recompute: every training figure is retrained (both models, seeds 0 to 2, the copy task on seeds 0 to 2), the dev losses are recomputed by NumPy and by the autograd, the bigram's 2.4514 is rebuilt from add-one counts, and the code widgets are run with the page's judge. Results hold with default threads and with one thread. `sequence-attn-names.json` is exactly what `--write` produces (byte-identical, 116,103 bytes; dev 2.273664 and 2.172923). Training uses only `windows(TRN)`, the first 25,626 names of makemore's `default_rng(42)` permutation; every dev loss is on the next 3,203 (22,807 scored symbols).

- docs/reports/sequence-L1-numbers.py, -L2, -L3 | claims with `covers=` | note | A few claims cover numbers they do not compare: L1 line 208 covers 0.9 and 0.1 (A's eigenvalues) under a check of C's; line 393 covers 0.95 and 0.99 under a check of R's eigenvalues; L2 line 93 (`0 / 0.002 == 0`) and 162 (`exp(0.7)/exp(0.7) == 1`) and L3's `math.sin(3 / 1) == math.sin(3)` are tautologies. Each number happens to be right. | Compare each number in the claim that covers it, or move it to `literal()` with a reason.
- docs/reports/sequence-L3-numbers.py | literal '2.6899' | note | The reference's tenth training loss, stated in l10 screens[9] `how`, is marked literal ("from the solution run") although the script runs that solution. I recomputed it in CPython: 3.3803, ..., 2.7132, 2.6899. | `E(L10, 'screens[9].widget.how', round(losses[-1], 4))` from the run the script already makes.
- docs/reports/sequence-L1.md to -L3.md | figures | note | Report-only slips: L1 claims 389 checks (the script runs 388); L2 gives the l6 slope as "−0.116 and 0.055" (the lesson and `kernel_grad` test 1 give −0.096 for the second entry); L3 gives b5 on b2 as 0.2594 (0.259453, the lesson's 0.2595). | Correct the reports; no content change.

## Level 1

- app/content/courses/sequence/l2-unrolling.json | screens[5] prose and feedback.byKey.test-1 | warning | "replace `h` by `Tensor(h.data)` before step $K$, $2K$" contradicts the solution under the lesson's own indexing ($h_t$ is made at step $t$, from $h_0$): the solution cuts at loop index `t = K`, which is before step $K + 1$, so each window holds $K$ steps. A learner who cuts before step $K$ as written (my W1) fails test 1 and is told again to "cut only before steps $K$, $2K$". Only hint 2's code reveals the intended cut. | Prose: "before steps $K + 1$, $2K + 1$, and so on (loop index `t = K, 2K, ...`), so each window holds $K$ steps"; the same words in byKey test-1.
- app/content/courses/sequence/l3-exploding-and-vanishing.json | screens[9] option `explode` why | warning | "If any entry of $\mathbf W$ exceeds 1 the gradient explodes" is answered with $\mathbf N$ (entries 0.9, none above 1) and $\mathbf D$ (an entry of 1.05 that does explode): neither refutes the claim. | "Entries do not decide it: lesson 3's $\begin{pmatrix} 0.85 & 4 \\ 0 & 0.85 \end{pmatrix}$ has an entry of 4 and radius 0.85, and its gradient vanishes in the long run."
- app/content/courses/sequence/l3-exploding-and-vanishing.json | screens[8] tests 7 and 8 (`explodes`) | warning | `explodes` is defined by $\rho^T$, and the lesson's point is that a non-normal matrix's actual size differs, but no test uses one: judging by the actual norm from $\mathbf g = (1, 0)$ (my W3) passes every test, as does `>=` (W2). | Add `explodes([[0.85, 4.0], [0.0, 0.85]], 6, 5.0)` expecting `False` ($\rho^6 = 0.377$ while the actual size at $k = 6$ is 10.66; W3 returns `True`).
- app/content/courses/sequence/homework-1.json | items[3] explain | warning | "the size is at most $\lVert\mathbf W\rVert^T$, which is why the eigenvalues of $\mathbf W$ decide explosion and vanishing": the bound uses the operator norm (largest singular value), not the eigenvalues, and an upper bound cannot show explosion. | "the size is at most $\lVert\mathbf W\rVert^T$, so a largest singular value below 1 guarantees vanishing; in the long run the eigenvalues set the rate (lesson 3)."
- app/content/courses/sequence/l2-unrolling.json | screens[4] explain | note | `$10^-5$` renders as $10^-5$ (only the minus raised). | `$10^{-5}$`.
- app/content/courses/sequence/l2-unrolling.json | quiz[1] byKey `w` | note | "You differentiated with respect to $h_0$ and set $w = 0$" is not a slip anyone makes to reach 0. | "You treated $w\,h_0$ as a constant. Its derivative in $w$ is $h_0$."
- app/content/courses/sequence/l2-unrolling.json | screens[8] hints[2] | note | "The open and the close are 17 windows apart": the first and last windows are 16 apart (17 in all). | "The open and the close sit in the first and the 17th window."
- app/content/courses/sequence/l3-exploding-and-vanishing.json | screens[3] option `C` why, screens[6] | note | "$\mathbf C$'s eigenvalues have size exactly 1": with entries 0.866 they are 0.99998, the figure code test 4 expects. | "size 1 (0.99998 with these rounded entries)".
- app/content/courses/sequence/problems-1.json | items[0] parts[2] | note | "A gradient of norm 0.5 is carried back those 20 steps" grows by exactly $1.1^{20}$ only if it lies along the growing eigenvector. | "A gradient of norm 0.5 along the growing direction ...".

## Level 2

- app/content/courses/sequence/l6-soft-neighbours.json | screens[7] tests 1 to 3 (`stable_softmax`) | warning | Subtracting the global maximum instead of each slice's (my W2) passes every test, yet it is not stable along an axis: `stable_softmax(np.array([[1.0, -1000.0], [0.0, -1001.0]]), axis=0)` gives NaN in the second column (both exponentials underflow), against 0.7311 and 0.2689. Test 3's columns have similar scales, so it cannot tell. | Add that call as a test expecting `[[0.7311, 0.7311], [0.2689, 0.2689]]` (to $10^{-9}$), with byKey "Subtract each slice's own maximum: `keepdims=True` along `axis`."
- app/content/courses/sequence/l8-scaled-dot-product.json | screens[8] feedback.byKey.test-6 | warning | Test 6 is the first failure for dividing by $d$ in `softmax_saturation` (my W2: it returns 0.0792), but its line says "Return the raw weight first, then the scaled one". | "Return `[raw, scaled by √d]`: on seed 4 the raw weight is 0.9996 and the scaled 0.2927."
- app/content/courses/sequence/l8-scaled-dot-product.json | screens[7] explain (edge case) | warning | "Layer normalisation, in level 4, keeps them standardised before every attention layer": layer norm standardises the block's input $\mathbf x$, not $\mathbf q = \mathrm{LN}(\mathbf x)\mathbf W_Q$ or $\mathbf k$; their scale also depends on $\mathbf W_Q$, $\mathbf W_K$. | "Layer normalisation, in level 4, standardises the input to each attention layer, and the initial $\mathbf W_Q$ and $\mathbf W_K$ are scaled to keep $\mathbf q$ and $\mathbf k$ near unit variance."
- app/content/courses/sequence/homework-2.json | items[5] feedback.byKey.d2 | warning | "Dropping the off-diagonal terms is the bug the homework's first mutant makes": `mutants` are author-only (the page ignores them), so the learner cannot know what it means. | "Dropping the off-diagonal terms treats each weight as if it moved alone; the next item's backward pass would then fail."
- app/content/courses/sequence/l8-scaled-dot-product.json | screens[3] prose | note | "A gap of 8 is one standard deviation at $d = 64$": a score has sd 8, but the gap between two independent scores has sd $8\sqrt 2 \approx 11.3$. | "A score of 8 against one of 0 is one standard deviation at $d = 64$."
- app/content/courses/sequence/l5-lookup-table.json | screens[5] prose | note | "$(0.5, 0)$ is row 5, $(0, -1)$ row 7" counts from 0, but no row numbers are shown on the plane and a reader counts from 1 (rows 6 and 8). | "$(0.5, 0)$ is the sixth day listed, $(0, -1)$ the eighth (indices 5 and 7)."
- app/content/courses/sequence/l7-queries-keys-values.json | screens[3] prose | note | "$\mathbf q \cdot \mathbf k$ can be any bilinear similarity $\mathbf x_q^\top\mathbf W_Q\mathbf W_K^\top\mathbf x_k$": only one of rank at most the key width. | "any bilinear similarity of rank up to the key width".

## Level 3

- app/content/courses/sequence/problems-3.json | items[3] parts[2] | error | The item gives the model's loss as 2.2737 nats, but the key 9.71 is $e^{2.273664}$, a figure the learner never sees. $e^{2.2737} = 9.7153$, which rounds to 9.72, outside $9.71 \pm 0.005$: a learner who follows the item exactly is marked wrong. | Key 9.72 (tol 0.005 takes 9.7153); feedback.correct "$e^{2.2737} = 9.72$"; explain "a fair choice among 9.72 symbols".
- app/content/courses/sequence/l9-self-attention.json, l10-causal-mask.json, l12-positions.json | l9 screens[3] explain, l10 screens[0] prose, l12 screens[0] prose | warning | Level 3 counts lessons within the level while levels 1 and 2, and l9's own "lesson 7's attention", count across the course: "Lesson 4 adds positions" (l12, but lesson 4 is clipping and gates), "The self-attention layer of lesson 1" (l9, but lesson 1 is the AR(1) net), "Take lesson 2's trained model" (l10, but lesson 2 is unrolling). l9's generaliser says "lesson 4 of this level", which shows the intent. | "Lesson 12 adds positions", "The self-attention layer of lesson 9", "Take lesson 10's trained model".
- app/content/courses/sequence/l11-many-heads.json | screens[6] feedback.byKey.test-5 | warning | Test 5 is the first failure for every `multi_head_attention` mistake made after a correct split: the authors' own mutant that forgets $\mathbf W_O$, and joining the heads with a plain reshape (my W3). All are told "Scale by the square root of the head width". | "Scale by $\sqrt{d/h}$, join the heads with a transpose then a reshape, and finish with $\mathbf W_O$."
- app/content/courses/sequence/l10-causal-mask.json | screens[8] tests 6 to 9 (`leak_test`) | warning | The only leaky model is fully unmasked, so any change after $t$ moves output $t$. A leak test that changes only the last token (my W5) passes every test, yet it misses a mask that leaks one step ahead. | Add `leaky1_fn` (the same weights with `np.triu(..., 2)`) to the prelude and a test `leak_test(leaky1_fn, NAME, 3)` expecting `True`; W5 returns `False` there (checked), the reference `True`.
- app/content/courses/sequence/l12-positions.json | screens[3] explain | warning | "Because the dot product depends on the offset only, attention can learn 'look 3 back' once for all positions" overstates it: the scores use $\mathbf p_t\mathbf W_Q\mathbf W_K^\top\mathbf p_{t+k}^\top$ (plus token terms), which depends on $t$ unless the matrices fit the rotations. Vaswani et al. offer it as a hypothesis. | "$\mathbf p_{t+k}$ is a fixed rotation of $\mathbf p_t$ for every $t$, which Vaswani et al. expected to make 'look 3 back' easy to learn."
- app/content/courses/sequence/l12-positions.json | quiz[1] | warning | The prose says only "Self-attention without positions reads 'abc' and 'bac'"; the why of `every` and the explain rely on a causal mask. Without one, l9's equivariance holds and a's and b's outputs are also unchanged, only moved, so the reasoning given is not the reason. | Prose: "Causal self-attention without positions reads ...".
- app/content/courses/sequence/l10-causal-mask.json, problems-3.json | l10 screens[5] feedback.correct; problems-3 items[0] parts[2] feedback.correct | note | Shown working does not give the shown figure at the stated precision: $2.2737/\ln 2 = 3.28026$, so 3.2803, not 3.2802 (the key is from 2.273664); $0.2483 + 0.5035 = 0.7518$, not 0.7517 (the key is from unrounded weights). Both still grade right, at the edge of their 0.0001 bands. | "$2.273664/\ln 2 = 3.2802$" (or key 3.2803 from 2.2737); "$\approx 0.7518$" with key 0.7518, or quote the weights to 6 places.
- app/content/courses/sequence/l11-many-heads.json | screens[3] feedback.correct | note | `4{{,}}096` has doubled braces (it renders, but every other figure uses `{,}`). | `4{,}096`.
- app/content/courses/sequence/l10-causal-mask.json, problems-3.json | dev loss on "held-out names" | note | The split is by line, as makemore's: 390 of the 3,203 dev names (12.2%) also occur among the training names (names.txt has 32,033 lines and 29,494 distinct names). The bigram is scored on the same lines, so the comparison is fair, but "names it never saw" would be false for those 390. | No change needed; if the level ever says "unseen names", say "held-out lines of names.txt".

## Code widgets across the levels

Every solution passes and every starter fails under the local Pyodide (grade-all, 0 failures). Slowest case per widget against its page limit: l4 screens[8] `train_gated_copy` 979 ms of 41 s (budget 6,000 ms; 42x), l10 screens[9] `train_steps` 549 ms of 39 s (71x), l8 screens[8] 73 ms, everything else under 35 ms of 35 s. No margin is under 3x, and every case meets the brief's budget rule (at most 1 s, or 10 s with a budget). Training thresholds have room: l10 test 6 needs below 2.75 and the reference's tenth loss is 2.6899 (recomputed); l4 tests 5 and 6 need 0.95 and the reference reaches 1.0. Every byKey `test-N` line can show: for each N a plausible mistake (the authors' mutant or mine) fails test N first; the mis-targeted ones are listed above.

- app/content/courses/sequence/l1-memory-in-a-loop.json, l6-soft-neighbours.json, l12-positions.json, homework-1.json, l10-causal-mask.json | l1 screens[7], l6 screens[7], l12 screens[7], homework-1 items[7], l10 screens[9] | note | Mistakes the levels teach reach only a generic or a neighbouring line: ignoring `h0` (l1 W1, test 3, generic "Carry the state from step to step"); choosing $\tau$ on the training rows (l6 W3, test 7, generic about the softmax); concatenating positions, the l12 trap (W2, test 4, generic about sines); assigning the BPTT gradients instead of adding them over steps, the commonest bug of l2 (homework-1 W1, test 2: the line never says "add"); a dev loss in bits (l10 W3, test 1: the line is about scored positions). | byKey lines: l1 `test-3` "Start from `h0`, not from 0."; l6 `test-7` "Score each $\tau$ on the held-out rows only."; l12 `test-4` "Add the positions; concatenating doubles the width."; homework-1 `test-2` add "and add each step's term (`+=`): the weights are shared."; l10 `test-1` add "in nats (natural log)".

## Appendix: wrong solutions run through the grader

How: each wrong solution was graded by `makeRunner(...).grade(spec, source, 'tests')` from `tools/code-runner.mjs`, the harness `grade-all.mjs --code` uses (the page's worker grader and per-case limits, local Pyodide 0.27.7), on the unedited content files; the grader reports the first failing hidden test or that the source passes every test. Results: 62 tried; 5 are correct alternatives or no-ops (marked); of the 57 wrong ones, 53 are caught and 4 survive (l3 `explodes` W2 at exact equality and W3 by one gradient norm, l6 `stable_softmax` W2 with a global maximum, l10 `leak_test` W5 changing only the last token). The classes asked for are all caught: BPTT that does not accumulate across steps (l2 W1, homework-1 rnn_bptt W1, both fail at the gradient test), clipping by value where norm is taught (l4 screens[4] W1, screens[8] W2), attention scaled by $d$ (l8 W1, homework-2 W1, l9 W1), softmax over the wrong axis (l6 W1, l7 W1 and attention_autograd W2, homework-2 W3), a causal mask that excludes the diagonal or includes the future (l10 W1 and W2, homework-3 W3), heads split along the wrong dimension (l11 W1 and W2, homework-3 W4), positions added after attention or after the projections (homework-3 W1 and W6), and no or a single gradient zeroing (l4 screens[8] W1, l10 screens[9] W1 and W2). The authors' own 83 mutants pass `grade-all` on the original files (each first fails its named test).

### l1-memory-in-a-loop screens[3] `fit_w` (6 hidden tests)

- W1 fit_w: sum instead of mean in the gradient: **fails T1**.

```python
import numpy as np


def fit_w(x, lr, steps):
    x = np.asarray(x, dtype=float)
    prev, now = x[:-1], x[1:]
    w = 0.0
    for _ in range(steps):
        grad = -2 * np.sum(prev * (now - w * prev))
        w = w - lr * grad
    return w
```

- W2 fit_w: closed-form least squares, ignoring lr and steps: **fails T1**.

```python
import numpy as np


def fit_w(x, lr, steps):
    x = np.asarray(x, dtype=float)
    return float(x[:-1] @ x[1:] / (x[:-1] @ x[:-1]))
```

- W3 fit_w: stops early once the gradient is below 1e-4: **fails T5**.

```python
import numpy as np


def fit_w(x, lr, steps):
    x = np.asarray(x, dtype=float)
    prev, now = x[:-1], x[1:]
    w = 0.0
    for _ in range(steps):
        grad = -2 * np.mean(prev * (now - w * prev))
        if abs(grad) < 1e-4:
            break
        w = w - lr * grad
    return w
```


### l1-memory-in-a-loop screens[7] `rnn_linear`, `rnn_tanh` (7 hidden tests)

- W1 rnn_linear ignores h0 (starts from 0): **fails T3**.

```python
import numpy as np


def rnn_linear(x, w, u, h0):
    h, out = 0.0, []
    for xt in x:
        h = w * h + u * xt
        out.append(h)
    return np.array(out)


def rnn_tanh(x, w, u, b, h0):
    h, out = h0, []
    for xt in x:
        h = np.tanh(w * h + u * xt + b)
        out.append(h)
    return np.array(out)
```


### l2-unrolling screens[3] `unroll`, `bptt_grad` (6 hidden tests)

- W1 BPTT that does not accumulate across steps: backward per step, gradients overwritten: **fails T3**.

```python
import numpy as np
from autograd import Tensor


def _graph(x, params):
    p = {k: Tensor(v) for k, v in params.items()}
    h = Tensor(0.0)
    err = []
    for t in range(len(x) - 1):
        h = (p['w'] * h + p['u'] * x[t]).tanh()
        err.append((p['v'] * h - x[t + 1]) ** 2)
    loss = err[0]
    for e in err[1:]:
        loss = loss + e
    return loss / len(err), p


def unroll(x, params):
    loss, _ = _graph(x, params)
    return loss.item()


def bptt_grad(x, params):
    n = len(x) - 1
    out = {}
    for t in range(n):
        p = {k: Tensor(v) for k, v in params.items()}
        h = Tensor(0.0)
        for s in range(t + 1):
            h = (p['w'] * h + p['u'] * x[s]).tanh()
        e = (p['v'] * h - x[t + 1]) ** 2 / n
        e.backward()
        out = {k: float(q.grad) for k, q in p.items()}
    return out
```

- W2 BPTT with the state detached each step (one-step gradient): **fails T3**.

```python
import numpy as np
from autograd import Tensor


def _graph(x, params, cut):
    p = {k: Tensor(v) for k, v in params.items()}
    h = Tensor(0.0)
    err = []
    for t in range(len(x) - 1):
        hin = Tensor(h.data) if cut else h
        h = (p['w'] * hin + p['u'] * x[t]).tanh()
        err.append((p['v'] * h - x[t + 1]) ** 2)
    loss = err[0]
    for e in err[1:]:
        loss = loss + e
    return loss / len(err), p


def unroll(x, params):
    loss, _ = _graph(x, params, False)
    return loss.item()


def bptt_grad(x, params):
    loss, p = _graph(x, params, True)
    loss.backward()
    return {k: float(t.grad) for k, t in p.items()}
```

- W3 sum of squared errors, not the mean: **fails T1**.

```python
import numpy as np
from autograd import Tensor


def _graph(x, params):
    p = {k: Tensor(v) for k, v in params.items()}
    h = Tensor(0.0)
    loss = Tensor(0.0)
    for t in range(len(x) - 1):
        h = (p['w'] * h + p['u'] * x[t]).tanh()
        loss = loss + (p['v'] * h - x[t + 1]) ** 2
    return loss, p


def unroll(x, params):
    loss, _ = _graph(x, params)
    return loss.item()


def bptt_grad(x, params):
    loss, p = _graph(x, params)
    loss.backward()
    return {k: float(t.grad) for k, t in p.items()}
```


### l2-unrolling screens[5] `truncated_bptt` (5 hidden tests)

- W1 truncated_bptt cutting before step K in the 1-based reading of the prose (t % K == K - 1): **fails T1**.

```python
import numpy as np
from autograd import Tensor


def truncated_bptt(x, params, K):
    p = {k: Tensor(v) for k, v in params.items()}
    h = Tensor(0.0)
    err = []
    for t in range(len(x) - 1):
        if t > 0 and (t + 1) % K == 0:
            h = Tensor(h.data)
        h = (p['w'] * h + p['u'] * x[t]).tanh()
        err.append((p['v'] * h - x[t + 1]) ** 2)
    loss = err[0]
    for e in err[1:]:
        loss = loss + e
    (loss / len(err)).backward()
    return {k: float(t.grad) for k, t in p.items()}
```

- W2 truncated_bptt that also stops the loss gradient: backward per window, grads overwritten [no-op: zeroing before the single backward() changes nothing, so this equals the solution]: **SURVIVES (passes every hidden test)**.

```python
import numpy as np
from autograd import Tensor


def truncated_bptt(x, params, K):
    p = {k: Tensor(v) for k, v in params.items()}
    h = Tensor(0.0)
    n = len(x) - 1
    loss = Tensor(0.0)
    for t in range(n):
        if t > 0 and t % K == 0:
            for q in p.values():
                q.zero_grad()
            h = Tensor(h.data)
        h = (p['w'] * h + p['u'] * x[t]).tanh()
        loss = loss + (p['v'] * h - x[t + 1]) ** 2
    (loss / n).backward()
    return {k: float(t.grad) for k, t in p.items()}
```


### l3-exploding-and-vanishing screens[8] `grad_norm_through_time`, `spectral_radius`, `explodes` (8 hidden tests)

- W1 spectral_radius as the largest singular value (2-norm): **fails T5**.

```python
import numpy as np


def grad_norm_through_time(W, g, T):
    W, v = np.asarray(W, dtype=float), np.asarray(g, dtype=float)
    out = []
    for _ in range(T + 1):
        out.append(float(np.linalg.norm(v)))
        v = W.T @ v
    return out


def spectral_radius(W):
    return float(np.linalg.norm(np.asarray(W, dtype=float), 2))


def explodes(W, T, factor):
    return bool(spectral_radius(W) ** T > factor)
```

- W2 explodes with >= instead of > [wrong only at exact equality]: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def grad_norm_through_time(W, g, T):
    W, v = np.asarray(W, dtype=float), np.asarray(g, dtype=float)
    out = []
    for _ in range(T + 1):
        out.append(float(np.linalg.norm(v)))
        v = W.T @ v
    return out


def spectral_radius(W):
    return float(np.max(np.abs(np.linalg.eigvals(np.asarray(W, dtype=float)))))


def explodes(W, T, factor):
    return bool(spectral_radius(W) ** T >= factor)
```

- W3 explodes judged by the actual gradient norm from g = (1, 0, ...): **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def grad_norm_through_time(W, g, T):
    W, v = np.asarray(W, dtype=float), np.asarray(g, dtype=float)
    out = []
    for _ in range(T + 1):
        out.append(float(np.linalg.norm(v)))
        v = W.T @ v
    return out


def spectral_radius(W):
    return float(np.max(np.abs(np.linalg.eigvals(np.asarray(W, dtype=float)))))


def explodes(W, T, factor):
    g = np.zeros(len(W)); g[0] = 1.0
    return bool(grad_norm_through_time(W, g, T)[-1] > factor)
```


### l4-clipping-and-gates screens[4] `clip_by_norm`, `gated_step` (8 hidden tests)

- W1 clipping by value (np.clip at c) where norm is taught: **fails T1**.

```python
import numpy as np
from autograd import Tensor


def clip_by_norm(grads, c):
    return [np.clip(np.asarray(g, dtype=float), -c, c) for g in grads]


def sig(t):
    return 1.0 / (1.0 + (-t).exp())


def gated_step(h, x, f, p):
    z = sig(p['ax'] * x + p['af'] * f + p['ah'] * h + p['c'])
    cand = (p['w'] * h + p['ux'] * x + p['uf'] * f + p['b']).tanh()
    return (1.0 - z) * h + z * cand
```

- W2 clipping by the largest entry (infinity norm): **fails T1**.

```python
import numpy as np
from autograd import Tensor


def clip_by_norm(grads, c):
    top = max(float(np.max(np.abs(np.asarray(g, dtype=float)))) for g in grads)
    scale = c / top if top > c else 1.0
    return [np.asarray(g, dtype=float) * scale for g in grads]


def sig(t):
    return 1.0 / (1.0 + (-t).exp())


def gated_step(h, x, f, p):
    z = sig(p['ax'] * x + p['af'] * f + p['ah'] * h + p['c'])
    cand = (p['w'] * h + p['ux'] * x + p['uf'] * f + p['b']).tanh()
    return (1.0 - z) * h + z * cand
```

- W3 gate reads the candidate, not the old state (a_h times the candidate): **fails T5**.

```python
import numpy as np
from autograd import Tensor


def clip_by_norm(grads, c):
    total = np.sqrt(sum(float(np.sum(np.asarray(g, dtype=float) ** 2)) for g in grads))
    scale = c / total if total > c else 1.0
    return [np.asarray(g, dtype=float) * scale for g in grads]


def sig(t):
    return 1.0 / (1.0 + (-t).exp())


def gated_step(h, x, f, p):
    cand = (p['w'] * h + p['ux'] * x + p['uf'] * f + p['b']).tanh()
    z = sig(p['ax'] * x + p['af'] * f + p['ah'] * cand + p['c'])
    return (1.0 - z) * h + z * cand
```


### l4-clipping-and-gates screens[8] `train_gated_copy` (6 hidden tests)

- W1 gradients zeroed once, before the loop only: **fails T1**.

```python
import numpy as np
from autograd import Tensor


def train_gated_copy(T, steps, seed, lr=0.5, n=64, c=1.0):
    p = init_gated(seed)
    rng = np.random.default_rng(1000 + seed)
    for q in p.values():
        q.zero_grad()
    for step in range(steps):
        X, F, y = copy_batch(T, n, rng)
        h = Tensor(np.zeros(n))
        for t in range(T):
            h = gated_step(h, X[t], F[t], p)
        loss = bce(p['v'] * h + p['d'], y)
        loss.backward()
        norm = np.sqrt(sum(float((q.grad ** 2).sum()) for q in p.values()))
        scale = min(1.0, c / max(norm, 1e-12))
        for q in p.values():
            q.data -= lr * scale * q.grad
    return accuracy(p, T), loss.item()
```

- W2 clipping each gradient by value at c (np.clip), not the global norm: **fails T4**.

```python
import numpy as np
from autograd import Tensor


def train_gated_copy(T, steps, seed, lr=0.5, n=64, c=1.0):
    p = init_gated(seed)
    rng = np.random.default_rng(1000 + seed)
    for step in range(steps):
        X, F, y = copy_batch(T, n, rng)
        for q in p.values():
            q.zero_grad()
        h = Tensor(np.zeros(n))
        for t in range(T):
            h = gated_step(h, X[t], F[t], p)
        loss = bce(p['v'] * h + p['d'], y)
        loss.backward()
        for q in p.values():
            q.data -= lr * np.clip(q.grad, -c, c)
    return accuracy(p, T), loss.item()
```

- W3 global norm clipped but only when the norm is below c (inverted test): **fails T1**.

```python
import numpy as np
from autograd import Tensor


def train_gated_copy(T, steps, seed, lr=0.5, n=64, c=1.0):
    p = init_gated(seed)
    rng = np.random.default_rng(1000 + seed)
    for step in range(steps):
        X, F, y = copy_batch(T, n, rng)
        for q in p.values():
            q.zero_grad()
        h = Tensor(np.zeros(n))
        for t in range(T):
            h = gated_step(h, X[t], F[t], p)
        loss = bce(p['v'] * h + p['d'], y)
        loss.backward()
        norm = np.sqrt(sum(float((q.grad ** 2).sum()) for q in p.values()))
        scale = c / norm if norm < c else 1.0
        for q in p.values():
            q.data -= lr * scale * q.grad
    return accuracy(p, T), loss.item()
```


### homework-1 items[1] `linear_bptt` (6 hidden tests)

- W1 linear_bptt starting the derivative at 1: **fails T1**.

```python
def linear_bptt(x, w, h0):
    h, d = h0, 1.0
    for xt in x:
        d = h + w * d
        h = w * h + xt
    return h, d
```


### homework-1 items[7] `rnn_bptt` (10 hidden tests)

- W1 rnn_bptt that assigns the Wh, Wx, b gradients instead of accumulating them over steps: **fails T2**.

```python
import numpy as np


def rnn_bptt(x, y, params):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    Wx, Wh, b, Wy, by = (np.asarray(params[k], dtype=float) for k in ('Wx', 'Wh', 'b', 'Wy', 'by'))
    T, n = x.shape[0], Wh.shape[0]
    hs = [np.zeros(n)]
    for t in range(T):
        hs.append(np.tanh(x[t] @ Wx + hs[-1] @ Wh + b))
    H = np.array(hs[1:])
    E = H @ Wy + by - y
    loss = 0.5 * np.sum(E ** 2) / T
    dY = E / T
    g = {'Wx': np.zeros_like(Wx), 'Wh': np.zeros_like(Wh), 'b': np.zeros_like(b), 'Wy': H.T @ dY, 'by': dY.sum(axis=0)}
    carry = np.zeros(n)
    for t in reversed(range(T)):
        dh = dY[t] @ Wy.T + carry
        da = dh * (1 - H[t] ** 2)
        g['Wx'] = np.outer(x[t], da)
        g['Wh'] = np.outer(hs[t], da)
        g['b'] = da
        carry = da @ Wh.T
    return float(loss), g
```

- W2 rnn_bptt carrying the gradient back through Wh without the tanh slope: **fails T2**.

```python
import numpy as np


def rnn_bptt(x, y, params):
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    Wx, Wh, b, Wy, by = (np.asarray(params[k], dtype=float) for k in ('Wx', 'Wh', 'b', 'Wy', 'by'))
    T, n = x.shape[0], Wh.shape[0]
    hs = [np.zeros(n)]
    for t in range(T):
        hs.append(np.tanh(x[t] @ Wx + hs[-1] @ Wh + b))
    H = np.array(hs[1:])
    E = H @ Wy + by - y
    loss = 0.5 * np.sum(E ** 2) / T
    dY = E / T
    g = {'Wx': np.zeros_like(Wx), 'Wh': np.zeros_like(Wh), 'b': np.zeros_like(b), 'Wy': H.T @ dY, 'by': dY.sum(axis=0)}
    carry = np.zeros(n)
    for t in reversed(range(T)):
        dh = dY[t] @ Wy.T + carry
        da = dh * (1 - H[t] ** 2)
        g['Wx'] += np.outer(x[t], da)
        g['Wh'] += np.outer(hs[t], da)
        g['b'] += da
        carry = dh @ Wh.T
    return float(loss), g
```


### l5-lookup-table screens[6] `hard_lookup`, `knn_lookup`, `lookup_gradient_zero` (8 hidden tests)

- W1 forward difference instead of central: **fails T8**.

```python
import numpy as np


def _dist(q, K):
    return np.sqrt(((np.asarray(K, dtype=float) - np.asarray(q, dtype=float)) ** 2).sum(axis=1))


def hard_lookup(q, K, V):
    return float(np.asarray(V, dtype=float)[np.argmin(_dist(q, K))])


def knn_lookup(q, K, V, k):
    idx = np.argsort(_dist(q, K), kind='stable')[:k]
    return float(np.mean(np.asarray(V, dtype=float)[idx]))


def lookup_gradient_zero(q, K, V, eps):
    q = np.asarray(q, dtype=float)
    out = []
    for j in range(len(q)):
        up = q.copy()
        up[j] += eps
        out.append((hard_lookup(up, K, V) - hard_lookup(q, K, V)) / eps)
    return out
```

- W2 knn_lookup with the default (unstable) argsort [correct alternative in practice] [correct alternative: NumPy sorts ten numbers stably]: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def _dist(q, K):
    return np.sqrt(((np.asarray(K, dtype=float) - np.asarray(q, dtype=float)) ** 2).sum(axis=1))


def hard_lookup(q, K, V):
    return float(np.asarray(V, dtype=float)[np.argmin(_dist(q, K))])


def knn_lookup(q, K, V, k):
    idx = np.argsort(_dist(q, K))[:k]
    return float(np.mean(np.asarray(V, dtype=float)[idx]))


def lookup_gradient_zero(q, K, V, eps):
    q = np.asarray(q, dtype=float)
    out = []
    for j in range(len(q)):
        up, dn = q.copy(), q.copy()
        up[j] += eps
        dn[j] -= eps
        out.append((hard_lookup(up, K, V) - hard_lookup(dn, K, V)) / (2 * eps))
    return out
```


### l6-soft-neighbours screens[7] `stable_softmax`, `soft_lookup`, `best_tau` (8 hidden tests)

- W1 softmax over the wrong axis: axis argument ignored (always the last): **fails T3**.

```python
import numpy as np


def stable_softmax(s, axis=-1):
    s = np.asarray(s, dtype=float)
    z = np.exp(s - s.max(axis=-1, keepdims=True))
    return z / z.sum(axis=-1, keepdims=True)


def soft_lookup(q, K, V, tau):
    K, q = np.asarray(K, dtype=float), np.asarray(q, dtype=float)
    scores = -((K - q) ** 2).sum(axis=1) / tau
    return float(stable_softmax(scores) @ np.asarray(V, dtype=float))


def best_tau(K_tr, V_tr, K_val, V_val, taus):
    errs = []
    for tau in taus:
        pred = np.array([soft_lookup(q, K_tr, V_tr, tau) for q in K_val])
        errs.append(np.mean((pred - np.asarray(V_val)) ** 2))
    return taus[int(np.argmin(errs))]
```

- W2 stable_softmax subtracting the global maximum, not each slice's: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def stable_softmax(s, axis=-1):
    s = np.asarray(s, dtype=float)
    z = np.exp(s - s.max())
    return z / z.sum(axis=axis, keepdims=True)


def soft_lookup(q, K, V, tau):
    K, q = np.asarray(K, dtype=float), np.asarray(q, dtype=float)
    scores = -((K - q) ** 2).sum(axis=1) / tau
    return float(stable_softmax(scores) @ np.asarray(V, dtype=float))


def best_tau(K_tr, V_tr, K_val, V_val, taus):
    errs = []
    for tau in taus:
        pred = np.array([soft_lookup(q, K_tr, V_tr, tau) for q in K_val])
        errs.append(np.mean((pred - np.asarray(V_val)) ** 2))
    return taus[int(np.argmin(errs))]
```

- W3 best_tau scored on the training rows (no held-out data): **fails T7**.

```python
import numpy as np


def stable_softmax(s, axis=-1):
    s = np.asarray(s, dtype=float)
    z = np.exp(s - s.max(axis=axis, keepdims=True))
    return z / z.sum(axis=axis, keepdims=True)


def soft_lookup(q, K, V, tau):
    K, q = np.asarray(K, dtype=float), np.asarray(q, dtype=float)
    scores = -((K - q) ** 2).sum(axis=1) / tau
    return float(stable_softmax(scores) @ np.asarray(V, dtype=float))


def best_tau(K_tr, V_tr, K_val, V_val, taus):
    errs = []
    for tau in taus:
        pred = np.array([soft_lookup(q, K_tr, V_tr, tau) for q in K_tr])
        errs.append(np.mean((pred - np.asarray(V_tr)) ** 2))
    return taus[int(np.argmin(errs))]
```


### l7-queries-keys-values screens[6] `attention`, `attention_shapes` (7 hidden tests)

- W1 softmax over the whole score matrix: **fails T2**.

```python
import numpy as np


def attention(Q, K, V):
    Q, K, V = (np.asarray(a, dtype=float) for a in (Q, K, V))
    S = Q @ K.T
    A = np.exp(S - S.max())
    A = A / A.sum()
    return A @ V


def attention_shapes(n_q, n_k, d, d_v):
    return {'Q': [n_q, d], 'K': [n_k, d], 'V': [n_k, d_v], 'scores': [n_q, n_k], 'out': [n_q, d_v]}
```

- W2 attention scaled by sqrt(d) (scaling not yet asked for): **fails T1**.

```python
import numpy as np


def attention(Q, K, V):
    Q, K, V = (np.asarray(a, dtype=float) for a in (Q, K, V))
    S = Q @ K.T / np.sqrt(Q.shape[-1])
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    return A @ V


def attention_shapes(n_q, n_k, d, d_v):
    return {'Q': [n_q, d], 'K': [n_k, d], 'V': [n_k, d_v], 'scores': [n_q, n_k], 'out': [n_q, d_v]}
```


### l7-queries-keys-values screens[7] `attention_autograd` (6 hidden tests)

- W1 attention_autograd with autograd.softmax (no gradient through the weights): **fails T2**.

```python
import numpy as np
from autograd import Tensor, softmax
from seq_ops_l2 import swap_last


def attention_autograd(Xq, Xk, params):
    W = {k: Tensor(v) for k, v in params.items()}
    Q = Tensor(Xq) @ W['WQ']
    K = Tensor(Xk) @ W['WK']
    V = Tensor(Xk) @ W['WV']
    out = Tensor(softmax(Q @ swap_last(K), axis=-1)) @ V
    out.sum().backward()
    return out.data, {k: t.grad for k, t in W.items()}
```

- W2 attention_autograd with the softmax along axis 0: **fails T1**.

```python
import numpy as np
from autograd import Tensor
from seq_ops_l2 import softmax, swap_last


def attention_autograd(Xq, Xk, params):
    W = {k: Tensor(v) for k, v in params.items()}
    Q = Tensor(Xq) @ W['WQ']
    K = Tensor(Xk) @ W['WK']
    V = Tensor(Xk) @ W['WV']
    out = softmax(Q @ swap_last(K), axis=0) @ V
    out.sum().backward()
    return out.data, {k: t.grad for k, t in W.items()}
```


### l8-scaled-dot-product screens[8] `dot_variance`, `scaled_attention`, `softmax_saturation` (7 hidden tests)

- W1 scaled_attention divided by d; saturation also divided by d: **fails T3**.

```python
import numpy as np


def dot_variance(d, n, seed):
    rng = np.random.default_rng(seed)
    q = rng.standard_normal((n, d))
    k = rng.standard_normal((n, d))
    return float(np.var((q * k).sum(axis=1)))


def _softmax(S):
    S = S - S.max(axis=-1, keepdims=True)
    E = np.exp(S)
    return E / E.sum(axis=-1, keepdims=True)


def scaled_attention(Q, K, V):
    Q, K, V = (np.asarray(a, dtype=float) for a in (Q, K, V))
    return _softmax(Q @ K.T / Q.shape[-1]) @ V


def softmax_saturation(d, seed):
    rng = np.random.default_rng(seed)
    q = rng.standard_normal(d)
    K = rng.standard_normal((16, d))
    s = K @ q
    return [float(_softmax(s).max()), float(_softmax(s / d).max())]
```

- W2 scaled_attention right, softmax_saturation divided by d only: **fails T6**.

```python
import numpy as np


def dot_variance(d, n, seed):
    rng = np.random.default_rng(seed)
    q = rng.standard_normal((n, d))
    k = rng.standard_normal((n, d))
    return float(np.var((q * k).sum(axis=1)))


def _softmax(S):
    S = S - S.max(axis=-1, keepdims=True)
    E = np.exp(S)
    return E / E.sum(axis=-1, keepdims=True)


def scaled_attention(Q, K, V):
    Q, K, V = (np.asarray(a, dtype=float) for a in (Q, K, V))
    return _softmax(Q @ K.T / np.sqrt(Q.shape[-1])) @ V


def softmax_saturation(d, seed):
    rng = np.random.default_rng(seed)
    q = rng.standard_normal(d)
    K = rng.standard_normal((16, d))
    s = K @ q
    return [float(_softmax(s).max()), float(_softmax(s / d).max())]
```

- W3 scaled by the square root of the number of keys: **fails T3**.

```python
import numpy as np


def dot_variance(d, n, seed):
    rng = np.random.default_rng(seed)
    q = rng.standard_normal((n, d))
    k = rng.standard_normal((n, d))
    return float(np.var((q * k).sum(axis=1)))


def _softmax(S):
    S = S - S.max(axis=-1, keepdims=True)
    E = np.exp(S)
    return E / E.sum(axis=-1, keepdims=True)


def scaled_attention(Q, K, V):
    Q, K, V = (np.asarray(a, dtype=float) for a in (Q, K, V))
    return _softmax(Q @ K.T / np.sqrt(K.shape[0])) @ V


def softmax_saturation(d, seed):
    rng = np.random.default_rng(seed)
    q = rng.standard_normal(d)
    K = rng.standard_normal((16, d))
    s = K @ q
    return [float(_softmax(s).max()), float(_softmax(s / np.sqrt(d)).max())]
```

- W4 dot_variance draws k before q [order differs from the comment] [correct alternative within the tolerance]: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def dot_variance(d, n, seed):
    rng = np.random.default_rng(seed)
    k = rng.standard_normal((n, d))
    q = rng.standard_normal((n, d))
    return float(np.mean(((q * k).sum(axis=1)) ** 2))


def _softmax(S):
    S = S - S.max(axis=-1, keepdims=True)
    E = np.exp(S)
    return E / E.sum(axis=-1, keepdims=True)


def scaled_attention(Q, K, V):
    Q, K, V = (np.asarray(a, dtype=float) for a in (Q, K, V))
    return _softmax(Q @ K.T / np.sqrt(Q.shape[-1])) @ V


def softmax_saturation(d, seed):
    rng = np.random.default_rng(seed)
    q = rng.standard_normal(d)
    K = rng.standard_normal((16, d))
    s = K @ q
    return [float(_softmax(s).max()), float(_softmax(s / np.sqrt(d)).max())]
```


### homework-2 items[7] `attention_backward` (9 hidden tests)

- W1 attention_backward with d in place of sqrt(d), forward and back: **fails T1**.

```python
import numpy as np


def attention_backward(Q, K, V, dout):
    Q, K, V, dout = (np.asarray(a, dtype=float) for a in (Q, K, V, dout))
    c = 1 / Q.shape[-1]
    S = Q @ K.T * c
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    dV = A.T @ dout
    dA = dout @ V.T
    dS = A * (dA - (dA * A).sum(axis=-1, keepdims=True))
    return dS @ K * c, dS.T @ Q * c, dV
```

- W2 attention_backward forgetting the 1/sqrt(d) on dK only: **fails T1**.

```python
import numpy as np


def attention_backward(Q, K, V, dout):
    Q, K, V, dout = (np.asarray(a, dtype=float) for a in (Q, K, V, dout))
    c = 1 / np.sqrt(Q.shape[-1])
    S = Q @ K.T * c
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    dV = A.T @ dout
    dA = dout @ V.T
    dS = A * (dA - (dA * A).sum(axis=-1, keepdims=True))
    return dS @ K * c, dS.T @ Q, dV
```

- W3 attention_backward with the softmax over the wrong axis in the forward pass: **fails T1**.

```python
import numpy as np


def attention_backward(Q, K, V, dout):
    Q, K, V, dout = (np.asarray(a, dtype=float) for a in (Q, K, V, dout))
    c = 1 / np.sqrt(Q.shape[-1])
    S = Q @ K.T * c
    S = S - S.max(axis=0, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=0, keepdims=True)
    dV = A.T @ dout
    dA = dout @ V.T
    dS = A * (dA - (dA * A).sum(axis=0, keepdims=True))
    return dS @ K * c, dS.T @ Q * c, dV
```


### l9-self-attention screens[6] `attention_matrix`, `self_attention`, `permutation_check` (7 hidden tests)

- W1 attention_matrix scaled by d instead of sqrt(d): **fails T1**.

```python
import numpy as np


def _softmax(S):
    S = S - S.max(axis=-1, keepdims=True)
    E = np.exp(S)
    return E / E.sum(axis=-1, keepdims=True)


def attention_matrix(X, params):
    X = np.asarray(X, dtype=float)
    Q, K = X @ params['Wq'], X @ params['Wk']
    return _softmax(Q @ K.T / Q.shape[-1])


def self_attention(X, Wq, Wk, Wv):
    X = np.asarray(X, dtype=float)
    return attention_matrix(X, {'Wq': Wq, 'Wk': Wk}) @ (X @ Wv)


def permutation_check(X, params, perm):
    X = np.asarray(X, dtype=float)
    out = self_attention(X, params['Wq'], params['Wk'], params['Wv'])
    out_p = self_attention(X[perm], params['Wq'], params['Wk'], params['Wv'])
    return bool(np.allclose(out_p, out[perm]))
```

- W2 permutation_check reordering by the inverse permutation: **fails T6**.

```python
import numpy as np


def _softmax(S):
    S = S - S.max(axis=-1, keepdims=True)
    E = np.exp(S)
    return E / E.sum(axis=-1, keepdims=True)


def attention_matrix(X, params):
    X = np.asarray(X, dtype=float)
    Q, K = X @ params['Wq'], X @ params['Wk']
    return _softmax(Q @ K.T / np.sqrt(Q.shape[-1]))


def self_attention(X, Wq, Wk, Wv):
    X = np.asarray(X, dtype=float)
    return attention_matrix(X, {'Wq': Wq, 'Wk': Wk}) @ (X @ Wv)


def permutation_check(X, params, perm):
    X = np.asarray(X, dtype=float)
    out = self_attention(X, params['Wq'], params['Wk'], params['Wv'])
    out_p = self_attention(X[perm], params['Wq'], params['Wk'], params['Wv'])
    return bool(np.allclose(out_p, out[np.argsort(perm)]))
```


### l10-causal-mask screens[8] `causal_mask`, `masked_attention`, `leak_test` (9 hidden tests)

- W1 causal mask that excludes the position itself (k=0): **fails T1**.

```python
import numpy as np


def causal_mask(T):
    return np.triu(np.full((T, T), -np.inf), 0)


def masked_attention(Q, K, V, mask):
    Q, K, V = (np.asarray(a, dtype=float) for a in (Q, K, V))
    S = Q @ K.T / np.sqrt(Q.shape[-1]) + mask
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    return A @ V


def leak_test(f, x, t):
    base = f(list(x))
    for j in range(t + 1, len(x)):
        y = list(x)
        y[j] = (y[j] + 1) % 27
        if not np.allclose(f(y)[:t + 1], base[:t + 1]):
            return True
    return False
```

- W2 causal mask that lets each position see one step of the future (k=2): **fails T1**.

```python
import numpy as np


def causal_mask(T):
    return np.triu(np.full((T, T), -np.inf), 2)


def masked_attention(Q, K, V, mask):
    Q, K, V = (np.asarray(a, dtype=float) for a in (Q, K, V))
    S = Q @ K.T / np.sqrt(Q.shape[-1]) + mask
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    return A @ V


def leak_test(f, x, t):
    base = f(list(x))
    for j in range(t + 1, len(x)):
        y = list(x)
        y[j] = (y[j] + 1) % 27
        if not np.allclose(f(y)[:t + 1], base[:t + 1]):
            return True
    return False
```

- W3 mask with -1e9 instead of -inf [a common alternative] [a common alternative, refused by the exact-equality test 1; the spec asks for -inf]: **fails T1**.

```python
import numpy as np


def causal_mask(T):
    return np.triu(np.full((T, T), -1e9), 1)


def masked_attention(Q, K, V, mask):
    Q, K, V = (np.asarray(a, dtype=float) for a in (Q, K, V))
    S = Q @ K.T / np.sqrt(Q.shape[-1]) + mask
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    return A @ V


def leak_test(f, x, t):
    base = f(list(x))
    for j in range(t + 1, len(x)):
        y = list(x)
        y[j] = (y[j] + 1) % 27
        if not np.allclose(f(y)[:t + 1], base[:t + 1]):
            return True
    return False
```

- W4 mask after the softmax, then renormalised [mathematically equal to masking first] [correct alternative]: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def causal_mask(T):
    return np.triu(np.full((T, T), -np.inf), 1)


def masked_attention(Q, K, V, mask):
    Q, K, V = (np.asarray(a, dtype=float) for a in (Q, K, V))
    S = Q @ K.T / np.sqrt(Q.shape[-1])
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    A = A * np.isfinite(mask)
    A = A / A.sum(axis=-1, keepdims=True)
    return A @ V


def leak_test(f, x, t):
    base = f(list(x))
    for j in range(t + 1, len(x)):
        y = list(x)
        y[j] = (y[j] + 1) % 27
        if not np.allclose(f(y)[:t + 1], base[:t + 1]):
            return True
    return False
```

- W5 leak_test that changes only the last token: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def causal_mask(T):
    return np.triu(np.full((T, T), -np.inf), 1)


def masked_attention(Q, K, V, mask):
    Q, K, V = (np.asarray(a, dtype=float) for a in (Q, K, V))
    S = Q @ K.T / np.sqrt(Q.shape[-1]) + mask
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    return A @ V


def leak_test(f, x, t):
    if t + 1 >= len(x):
        return False
    base = f(list(x))
    y = list(x)
    y[-1] = (y[-1] + 1) % 27
    return not np.allclose(f(y)[:t + 1], base[:t + 1])
```

- W6 leak_test comparing every output, not only 0..t: **fails T6**.

```python
import numpy as np


def causal_mask(T):
    return np.triu(np.full((T, T), -np.inf), 1)


def masked_attention(Q, K, V, mask):
    Q, K, V = (np.asarray(a, dtype=float) for a in (Q, K, V))
    S = Q @ K.T / np.sqrt(Q.shape[-1]) + mask
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    return A @ V


def leak_test(f, x, t):
    base = f(list(x))
    for j in range(t + 1, len(x)):
        y = list(x)
        y[j] = (y[j] + 1) % 27
        if not np.allclose(f(y), base):
            return True
    return False
```


### l10-causal-mask screens[9] `dev_loss`, `train_steps` (6 hidden tests)

- W1 train_steps zeroing gradients only once, before the loop: **fails T4**.

```python
import numpy as np
from autograd import Tensor


def dev_loss(model, X, Y):
    z = logits_of(model, X)
    z = z - z.max(axis=-1, keepdims=True)
    lse = np.log(np.exp(z).sum(axis=-1))
    keep = Y >= 0
    pick = np.take_along_axis(z, np.where(keep, Y, 0)[..., None], axis=-1)[..., 0]
    return float(((lse - pick) * keep).sum() / keep.sum())


def train_steps(model, X, Y, steps, lr):
    P = {k: Tensor(np.array(v, dtype=float)) for k, v in model.items()}
    losses = []
    for p in P.values():
        p.zero_grad()
    for _ in range(steps):
        loss = loss_tensor(P, X, Y)
        losses.append(loss.item())
        loss.backward()
        for p in P.values():
            p.data -= lr * p.grad
    return losses
```

- W2 train_steps with no gradient zeroing at all: **fails T4**.

```python
import numpy as np
from autograd import Tensor


def dev_loss(model, X, Y):
    z = logits_of(model, X)
    z = z - z.max(axis=-1, keepdims=True)
    lse = np.log(np.exp(z).sum(axis=-1))
    keep = Y >= 0
    pick = np.take_along_axis(z, np.where(keep, Y, 0)[..., None], axis=-1)[..., 0]
    return float(((lse - pick) * keep).sum() / keep.sum())


def train_steps(model, X, Y, steps, lr):
    P = {k: Tensor(np.array(v, dtype=float)) for k, v in model.items()}
    losses = []
    for _ in range(steps):
        loss = loss_tensor(P, X, Y)
        losses.append(loss.item())
        loss.backward()
        for p in P.values():
            p.data -= lr * p.grad
    return losses
```

- W3 dev_loss in bits (log base 2) [a common alternative, refused by the exact-equality test 1; the spec asks for -inf]: **fails T1**.

```python
import numpy as np
from autograd import Tensor


def dev_loss(model, X, Y):
    z = logits_of(model, X)
    z = z - z.max(axis=-1, keepdims=True)
    lse = np.log(np.exp(z).sum(axis=-1))
    keep = Y >= 0
    pick = np.take_along_axis(z, np.where(keep, Y, 0)[..., None], axis=-1)[..., 0]
    return float(((lse - pick) * keep).sum() / keep.sum() / np.log(2))


def train_steps(model, X, Y, steps, lr):
    P = {k: Tensor(np.array(v, dtype=float)) for k, v in model.items()}
    losses = []
    for _ in range(steps):
        for p in P.values():
            p.zero_grad()
        loss = loss_tensor(P, X, Y)
        losses.append(loss.item())
        loss.backward()
        for p in P.values():
            p.data -= lr * p.grad
    return losses
```


### l11-many-heads screens[6] `split_heads`, `merge_heads`, `head_params`, `multi_head_attention` (8 hidden tests)

- W1 heads split along the sequence axis (rows cut into h blocks): **fails T1**.

```python
import numpy as np


def split_heads(X, h):
    return np.stack(np.split(np.asarray(X), h, axis=0))


def merge_heads(Xh):
    return np.concatenate(list(Xh), axis=0)


def head_params(d, h):
    return {'per_head_width': d // h, 'weights': 4 * d * d}


def multi_head_attention(X, params, h, mask=None):
    X = np.asarray(X, dtype=float)
    Q, K, V = (split_heads(X @ params[k], h) for k in ('Wq', 'Wk', 'Wv'))
    S = Q @ K.transpose(0, 2, 1) / np.sqrt(Q.shape[-1])
    if mask is not None:
        S = S + mask
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    return merge_heads(A @ V) @ params['Wo']
```

- W2 interleaved feature split (head k holds features k, k + h, ...) with its matching merge: **fails T1**.

```python
import numpy as np


def split_heads(X, h):
    T, d = X.shape
    return np.asarray(X).reshape(T, d // h, h).transpose(2, 0, 1)


def merge_heads(Xh):
    h, T, w = Xh.shape
    return np.asarray(Xh).transpose(1, 2, 0).reshape(T, h * w)


def head_params(d, h):
    return {'per_head_width': d // h, 'weights': 4 * d * d}


def multi_head_attention(X, params, h, mask=None):
    X = np.asarray(X, dtype=float)
    Q, K, V = (split_heads(X @ params[k], h) for k in ('Wq', 'Wk', 'Wv'))
    S = Q @ K.transpose(0, 2, 1) / np.sqrt(Q.shape[-1])
    if mask is not None:
        S = S + mask
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    return merge_heads(A @ V) @ params['Wo']
```

- W3 split right, but heads joined by a plain reshape (no transpose): **fails T5**.

```python
import numpy as np


def split_heads(X, h):
    T, d = X.shape
    return np.asarray(X).reshape(T, h, d // h).transpose(1, 0, 2)


def merge_heads(Xh):
    h, T, w = Xh.shape
    return np.asarray(Xh).transpose(1, 0, 2).reshape(T, h * w)


def head_params(d, h):
    return {'per_head_width': d // h, 'weights': 4 * d * d}


def multi_head_attention(X, params, h, mask=None):
    X = np.asarray(X, dtype=float)
    Q, K, V = (split_heads(X @ params[k], h) for k in ('Wq', 'Wk', 'Wv'))
    S = Q @ K.transpose(0, 2, 1) / np.sqrt(Q.shape[-1])
    if mask is not None:
        S = S + mask
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    return (A @ V).reshape(X.shape[0], -1) @ params['Wo']
```

- W4 split right, MHA with the scale of the full width: **fails T5**.

```python
import numpy as np


def split_heads(X, h):
    T, d = X.shape
    return np.asarray(X).reshape(T, h, d // h).transpose(1, 0, 2)


def merge_heads(Xh):
    h, T, w = Xh.shape
    return np.asarray(Xh).transpose(1, 0, 2).reshape(T, h * w)


def head_params(d, h):
    return {'per_head_width': d // h, 'weights': 4 * d * d}


def multi_head_attention(X, params, h, mask=None):
    X = np.asarray(X, dtype=float)
    Q, K, V = (split_heads(X @ params[k], h) for k in ('Wq', 'Wk', 'Wv'))
    S = Q @ K.transpose(0, 2, 1) / np.sqrt(X.shape[-1])
    if mask is not None:
        S = S + mask
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    return merge_heads(A @ V) @ params['Wo']
```


### l12-positions screens[7] `sinusoidal_positions`, `add_positions`, `order_matters` (8 hidden tests)

- W1 positions counted from t = 1: **fails T1**.

```python
import numpy as np


def sinusoidal_positions(T, d):
    P = np.zeros((T, d))
    t = np.arange(1, T + 1)[:, None]
    w = 1.0 / 10000 ** (np.arange(0, d, 2) / d)
    P[:, 0::2] = np.sin(t * w)
    P[:, 1::2] = np.cos(t * w)
    return P


def add_positions(E, P):
    E, P = np.asarray(E, dtype=float), np.asarray(P, dtype=float)
    if len(E) > len(P):
        raise IndexError('context longer than the table')
    return E + P[:len(E)]


def order_matters(model, a, b):
    no = float(np.abs(last_logits(model, a) - last_logits(model, b)).max())
    yes = float(np.abs(last_logits(model, a, model['P']) - last_logits(model, b, model['P'])).max())
    return [no, yes]
```

- W2 positions concatenated instead of added: **fails T4**.

```python
import numpy as np


def sinusoidal_positions(T, d):
    P = np.zeros((T, d))
    t = np.arange(0, T + 0)[:, None]
    w = 1.0 / 10000 ** (np.arange(0, d, 2) / d)
    P[:, 0::2] = np.sin(t * w)
    P[:, 1::2] = np.cos(t * w)
    return P


def add_positions(E, P):
    E, P = np.asarray(E, dtype=float), np.asarray(P, dtype=float)
    if len(E) > len(P):
        raise IndexError('context longer than the table')
    return np.concatenate([E, P[:len(E)]], axis=1)


def order_matters(model, a, b):
    no = float(np.abs(last_logits(model, a) - last_logits(model, b)).max())
    yes = float(np.abs(last_logits(model, a, model['P']) - last_logits(model, b, model['P'])).max())
    return [no, yes]
```

- W3 no length check (NumPy raises ValueError on the shape clash): **fails T5**.

```python
import numpy as np


def sinusoidal_positions(T, d):
    P = np.zeros((T, d))
    t = np.arange(0, T + 0)[:, None]
    w = 1.0 / 10000 ** (np.arange(0, d, 2) / d)
    P[:, 0::2] = np.sin(t * w)
    P[:, 1::2] = np.cos(t * w)
    return P


def add_positions(E, P):
    E, P = np.asarray(E, dtype=float), np.asarray(P, dtype=float)
    return E + P[:len(E)]


def order_matters(model, a, b):
    no = float(np.abs(last_logits(model, a) - last_logits(model, b)).max())
    yes = float(np.abs(last_logits(model, a, model['P']) - last_logits(model, b, model['P'])).max())
    return [no, yes]
```


### homework-3 items[7] `causal_mha_forward` (9 hidden tests)

- W1 positions added after attention (to the joined heads, before W_O): **fails T1**.

```python
import numpy as np


def causal_mha_forward(X, params, h):
    X = np.asarray(X, dtype=float)
    T, d = X.shape
    w = d // h
    x = X + 0.0
    split = lambda a: a.reshape(T, h, w).transpose(1, 0, 2)
    Q, K, V = split(x @ params['Wq']), split(x @ params['Wk']), split(x @ params['Wv'])
    S = Q @ K.transpose(0, 2, 1) / np.sqrt(w) + np.triu(np.full((T, T), -np.inf), 1)
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    return (A @ V).transpose(1, 0, 2).reshape(T, d) + params['P'][:T] @ params['Wo']
```

- W2 positions added to queries and keys only, not to the values: **fails T1**.

```python
import numpy as np


def causal_mha_forward(X, params, h):
    X = np.asarray(X, dtype=float)
    T, d = X.shape
    w = d // h
    xp = X + params['P'][:T]
    split = lambda a: a.reshape(T, h, w).transpose(1, 0, 2)
    Q, K, V = split(xp @ params['Wq']), split(xp @ params['Wk']), split(X @ params['Wv'])
    S = Q @ K.transpose(0, 2, 1) / np.sqrt(w) + np.triu(np.full((T, T), -np.inf), 1)
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    return (A @ V).transpose(1, 0, 2).reshape(T, d) @ params['Wo']
```

- W3 causal mask letting each position see one future step (k=2): **fails T1**.

```python
import numpy as np


def causal_mha_forward(X, params, h):
    X = np.asarray(X, dtype=float)
    T, d = X.shape
    w = d // h
    x = X + params['P'][:T]
    split = lambda a: a.reshape(T, h, w).transpose(1, 0, 2)
    Q, K, V = split(x @ params['Wq']), split(x @ params['Wk']), split(x @ params['Wv'])
    S = Q @ K.transpose(0, 2, 1) / np.sqrt(w) + np.triu(np.full((T, T), -np.inf), 2)
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    return (A @ V).transpose(1, 0, 2).reshape(T, d)  @ params['Wo']
```

- W4 heads split along the sequence axis when T allows it: **fails T1**.

```python
import numpy as np


def causal_mha_forward(X, params, h):
    X = np.asarray(X, dtype=float)
    T, d = X.shape
    x = X + params['P'][:T]
    Q, K, V = x @ params['Wq'], x @ params['Wk'], x @ params['Wv']
    out = np.zeros((T, d))
    blocks = np.array_split(np.arange(T), h)
    for idx in blocks:
        if len(idx) == 0:
            continue
        S = Q[idx] @ K[idx].T / np.sqrt(d // h) + np.triu(np.full((len(idx), len(idx)), -np.inf), 1)
        S = S - S.max(axis=-1, keepdims=True)
        A = np.exp(S)
        A = A / A.sum(axis=-1, keepdims=True)
        out[idx] = A @ V[idx]
    return out @ params['Wo']
```

- W5 mask built for the full table length Tmax = 8, sliced to T (correct alternative) [correct alternative]: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def causal_mha_forward(X, params, h):
    X = np.asarray(X, dtype=float)
    T, d = X.shape
    w = d // h
    x = X + params['P'][:T]
    split = lambda a: a.reshape(T, h, w).transpose(1, 0, 2)
    Q, K, V = split(x @ params['Wq']), split(x @ params['Wk']), split(x @ params['Wv'])
    S = Q @ K.transpose(0, 2, 1) / np.sqrt(w) + np.triu(np.full((8, 8), -np.inf), 1)[:T, :T]
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    return (A @ V).transpose(1, 0, 2).reshape(T, d)  @ params['Wo']
```

- W6 positions added after the projections (x Wq + P): **fails T1**.

```python
import numpy as np


def causal_mha_forward(X, params, h):
    X = np.asarray(X, dtype=float)
    T, d = X.shape
    w = d // h
    P = params['P'][:T]
    split = lambda a: a.reshape(T, h, w).transpose(1, 0, 2)
    Q, K, V = split(X @ params['Wq'] + P), split(X @ params['Wk'] + P), split(X @ params['Wv'] + P)
    S = Q @ K.transpose(0, 2, 1) / np.sqrt(w) + np.triu(np.full((T, T), -np.inf), 1)
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    A = A / A.sum(axis=-1, keepdims=True)
    return (A @ V).transpose(1, 0, 2).reshape(T, d) @ params['Wo']
```


### homework-3 items[4] `head_patterns` (5 hidden tests)

- W1 head_patterns with the scale of the full width: **fails T1**.

```python
import numpy as np


def head_patterns(X, params, h):
    X = np.asarray(X, dtype=float)
    T, d = X.shape
    w = d // h
    Q = (X @ params['Wq']).reshape(T, h, w).transpose(1, 0, 2)
    K = (X @ params['Wk']).reshape(T, h, w).transpose(1, 0, 2)
    S = Q @ K.transpose(0, 2, 1) / np.sqrt(d) + np.triu(np.full((T, T), -np.inf), 1)
    S = S - S.max(axis=-1, keepdims=True)
    A = np.exp(S)
    return A / A.sum(axis=-1, keepdims=True)
```


## Fix pass

I recomputed every corrected number before writing it: $e^{2.2737} = 9.7153$ and $e^{2.273664} = 9.7149$; $2.273664/\ln 2 = 3.28020$; the three attention weights of problems-3 item 1 as 0.248255, 0.248255, 0.503490 (sum of the first and third 0.751745); $0.85^6 = 0.37715$ and the actual size 10.6556 at $k = 6$. Number scripts: `run-number-scripts.mjs --only sequence-L` 3 of 3 passed; directly with `ZQ_NUMBERS_STRICT=1` L1 395, L2 302 and L3 303 checks, exit 0, 0 uncovered, no `claim(True, covers=...)`. Validator 0 errors with no `[ai-mutants]` or `[source-ban]` on sequence files; voice scan 0 and 0; `same-course-reuse.mjs --all` no error for sequence; `grade-all.mjs --file <f> --code` 0 failures on all 15 edited files, each alone; playthrough of every edited lesson, set and problem set green with and without `--mobile`.

Status: fixed 31, disputed 0 (one finding needs no change, by its own text), deferred 1. Graded answers changed: 1 (problems-3 items[3].parts[2]). Hidden tests added: l3 tests 9 and 10, l6 test 9, l10 test 10, each with a mutant.

### Modules
- seq_ops_l3 `permute`, error: fixed in v1.1: axes are normalised with `a % ndim` before the inverse; gradient-checked on 3x3x3 and 2x3x4 with negative axes in `sequence-L3-numbers.py`. SHA-256 `6187fda66d5275176b60f5dd2e91643306aded66a2847fff70a3b8204c40bf94` (end of `docs/reports/sequence-L3.md`).
- seq_ops_l2 `softmax` fully masked row, warning: fixed where it matters, in `seq_ops_l3.attention` (private `_masked_softmax`: weights 0, output 0, gradient 0, other rows bit-identical); `seq_ops_l2.py` is a warning only and stays byte-identical (SHA-256 unchanged). Gradient-checked with a fully masked row.
- `softmax` name clash with `autograd.softmax`, note: deferred to the main session (one sentence in `app/content/data/ai/README.md` and AUTHORING section 9, which content agents do not edit).
- `attention`/`permute` argument notes: fixed in the v1.1 docstring ("`mask` is a NumPy array", "`axes` is required").

### Number scripts and reports
- `covers=` claims, note: fixed. L1 compares A's eigenvalues, P's (0.95) and Q's squared (0.99) where it covers them; L2 marks 0.002 and 0.001 literal with a reason and checks one-key softmax with the real softmax; L3 compares the table's first sine entries.
- l10 '2.6899', note: fixed. `E(L10, 'screens[9].widget.how', ...)` from the solution's own run (`ref_eval`); the literal is gone.
- Report slips, note: fixed in `sequence-L1.md` (395 checks), `-L2.md` (second slope -0.096), `-L3.md` (0.2595).

### Level 1
- l2 screens[5] cut position, warning: fixed in prose and `byKey.test-1`: before steps $K + 1$, $2K + 1$ (loop index `t = K, 2K, ...`), each window $K$ steps.
- l3 screens[9] option `explode`, warning: fixed with the 0.85/4 matrix as proposed.
- l3 screens[8] `explodes`, warning: fixed. Test 9 `explodes([[0.85, 4.0], [0.0, 0.85]], 6, 5.0)` is `False` and test 10 `explodes([[2.0]], 3, 8.0)` is `False` (exact tie, so `>=` returns `True`); mutants for `>=` (test 10) and for the actual gradient norm (test 9); byKey lines added; `how` says 10 tests.
- homework-1 items[3] explain, warning: fixed ("largest singular value below 1 guarantees vanishing; ... eigenvalues set the rate").
- l2 screens[4] `10^-5`, note: fixed (`10^{-5}`).
- l2 quiz[1] `w`, note: fixed.
- l2 screens[8] hint, note: fixed (first and 17th window).
- l3 option C, note: fixed ("size 1 (0.99998 with these rounded entries)"), checked in the L1 script.
- problems-1 items[0] parts[2], note: fixed ("along the growing direction").

### Level 2
- l6 `stable_softmax`, warning: fixed. Test 9 `stable_softmax([[1, -1000], [0, -1001]], axis=0)` expects 0.7311 and 0.2689 in both columns (full precision); mutant with the global maximum fails it; byKey `test-9` added.
- l8 test-6 line, warning: fixed.
- l8 screens[7] layer normalisation, warning: fixed with the proposed wording.
- homework-2 `d2`, warning: fixed (no reference to author-only mutants).
- l8 screens[3] "gap of 8", note: fixed.
- l5 screens[5] row numbers, note: fixed (sixth and eighth listed, indices 5 and 7).
- l7 screens[3] bilinear, note: fixed ("of rank up to the key width").

### Level 3
- problems-3 items[3] parts[2], error: fixed. Key 9.72 (the item shows 2.2737 and $e^{2.2737} = 9.7153$); tolerance widened from 0.005 to 0.006 so that both 9.7153 (what the learner computes) and 9.7149 (from the unrounded loss) are marked right; correct feedback and explain say 9.72; the script now computes `exp(round(dev, 4))` and checks all three fields.
- Lesson numbering, warning: fixed in l9 (two places: "Lesson 12", "lesson 12"), l10 ("lesson 9") and l12 ("lesson 10's trained model").
- l11 test-5 line, warning: fixed.
- l10 `leak_test`, warning: fixed. `leaky1_fn` (mask `np.triu(..., 2)`) added to the prelude (`logits_of` takes `lead`), test 10 `leak_test(leaky1_fn, NAME, 3)` is `True`; the last-token mutant fails it; byKey `test-10` added.
- l12 screens[3] explain, warning: fixed with the rotation wording.
- l12 quiz[1], warning: fixed ("Causal self-attention without positions").
- l10 screens[5] and problems-3 items[0] shown working, note: fixed without changing a key: the l10 line quotes 2.273664, the problems-3 item quotes the weights to 6 places (0.751745 rounds to 0.7517, the existing key).
- l11 `4{{,}}096`, note: fixed.
- "held-out names", note: no change needed, as the finding says; the lessons never say "unseen names".

### Code widgets
- byKey gaps, note: fixed: l1 `test-3`, l6 `test-7`, l12 `test-4`, homework-1 `test-2` (adds "add each step's term"), l10 `test-1` (adds "in nats").
