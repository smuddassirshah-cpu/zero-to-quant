# sequence level 4 (The transformer block and the residual stream): second-reader findings

Scope: `app/content/courses/sequence/` level 4 (`l13-the-block`, `l14-residual-stream`, `l15-counting-a-block`, `l16-a-tiny-transformer`, `review-4`, `homework-4`, `problems-4`), the new module `app/content/data/ai/seq_ops_l4.py` (v1.0, SHA-256 `9e0a855c2d30...`), the weights file `app/content/data/ai/sequence-reverse.json` and `docs/reports/sequence-L4-numbers.py`, at `04c28ba5`.
Method: every op of `seq_ops_l4.py` gradient-checked by my own central differences in float64 (h = 1e-6, every entry of the input and of every parameter, with non-trivial gains, shifts and biases: `mlp`; `mha` causal with 2 heads and unmasked with 4 on a batch; `attn_update`; `mlp_update`; `block` with the residual; the same sublayers chained without the residual; a post-norm block built from the same ops; `layernorm` on a 3-D batch; a two-block stack of 2 and 4 heads; `lm_logits` of a 2-block model through `cross_entropy` over all 38 arrays), `block` against my own NumPy block, `stream` against `block` and `lm_logits`, a leak test, `n_params` against the formula; the shipped `autograd.py`, `seq_ops_l2.py`, `seq_ops_l3.py` (v1.1, `6187fda66d52...`) and `nt_ops_l2.py` compared with the fix-pass commit `fa384717` (`git diff --stat`: unchanged) and with the script's SHA prefixes; every `import` in the level's widgets read for the `softmax` clash; the number script run through `node tools/run-number-scripts.mjs --only sequence-L4` (one thread, Haswell: passed, 93 s) and directly with default threads and `ZQ_NUMBERS_STRICT=1` (619 of 619 checks, 0 uncovered, 31 literals, exit 0, 77 s); `--write` replayed into a scratch copy under default threads (byte-identical to the shipped file, 143,841 bytes) and under one Haswell thread (differs only in 64 entries of `blocks.0.bk`, by at most 7.3e-12; see Modules); `grade-all.mjs --file <f> --code --local-cdn <pkgs>` on each of the seven files alone (11 Python widgets, 0 failures), each solution timed per case; 58 wrong solutions of my own through the real grader (`makeRunner(...).grade(spec, src, 'tests')` from `tools/code-runner.mjs`, appendix); `same-course-reuse.mjs --all` (0 errors, nothing for `sequence`); every stated number, distractor and tolerance recomputed by hand and in Python (each parameter count by formula and by summing array shapes); every `byKey` key checked against the keys its widget can return; `voice-scan.py 35` (0 over 35 words, 0 explanations over three sentences) and greps for em-dashes, exclamation marks and American spellings (none); prose read for false or loose claims; the interfaces read against `docs/briefs/gpt.md` Level 2 and `docs/briefs/interp.md` Level 1.
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, teaching issue or a test that misses what it claims; note = style or small gap.

Counts: modules 0 errors, 0 warnings, 4 notes; number script 2 notes; content 2 errors, 8 warnings, 8 notes. Totals: 2 errors, 8 warnings, 14 notes. Wrong solutions: 58 tried, 2 of them acceptable variants (marked); of the 56 wrong ones 2 survive (l13 `block_grad_check` W1, which leaves `x` out of the check, and l15 `block_params` W4, which takes the MLP width as $4d$). No module or interface error.

## Modules (`seq_ops_l4.py`; frozen copies)

Largest relative error, max |analytic − numeric| / (max |analytic| + max |numeric|), against my central differences: `mlp` 3.3e-10; `mha` causal, 2 heads, batch of 2, 5.1e-10, unmasked with 4 heads 2.4e-10; `attn_update` 8.7e-10; `mlp_update` 3.1e-10; `block` with the residual 4.4e-10; the two sublayers chained without the residual 1.9e-9; a post-norm block from the same ops 1.6e-9; `layernorm` on (2, 5, 8) 4.0e-10; a stack of two blocks (2 then 4 heads) 1.1e-9; `lm_logits` of a 2-block model through `cross_entropy`, all 38 arrays, 1.3e-8. All under the brief's 1e-6. The key bias `bk` has an analytic gradient of exactly 0 in every case (at most 1.6e-15, against central differences of at most 2.7e-9): adding a constant to every key score of a query row leaves its softmax unchanged, so this is correct, not a missing wire. `block` equals my NumPy pre-norm block to 1.8e-15; the last entry of `stream` equals two chained `block` calls exactly, and through the final layer norm and unembedding equals `lm_logits` to 4.4e-16; changing the last token moves no earlier logit (0.0); one token works; `n_params(init_block(64, 256))` is 49,984; the shipped model reads as 2 blocks and 26,571 numbers; a width that does not split into the heads raises `ValueError` from `split_heads`. Layer norm sits inside each branch (pre-norm), over the last axis, with $\epsilon = 10^{-5}$; the MLP is ReLU. The four frozen copies are unchanged since `fa384717` and match the script's SHA prefixes (`5917d4ec91f7`, `fa2bed08afe4`, `6187fda66d52`, `5712fe43db9b`). No widget of the level imports `softmax` at all; `seq_ops_l4.py` imports `Tensor` and `_wrap` from `autograd` by name, so the clash cannot arise; it calls `seq_ops_l3.attention` only with the causal mask or `None`, never a fully masked row.

Interfaces. `gpt` L2's counts follow from this module's convention: `mp(65, 32, 32, 128, 1)` is 18,017 and two blocks 30,721, the figures its brief quotes; its fused `qkv` is `concat([Wq, Wk, Wv], axis=1)`, which `split_heads` slices head by head as nanoGPT's `view` does, and `proj`, `fc`, `out`, `head` map to `Wo`, `W1`, `W2`, `U` (author report). `interp` L1 reads `stream()`: the stream after the embedding and after each of the $2L$ sublayers, as arrays. Both are pre-norm, row vectors times matrices, shapes `(..., T, d)`. Nothing mismatches.

- app/content/data/ai/seq_ops_l4.py | lm_logits, stream | note | Past the context the two fail differently: `lm_logits` raises `IndexError` (`P[np.arange(T)]`), while `stream` slices `P[:T]` to 12 rows and then fails with a broadcast error. `gpt` l8 slides a window once the context is full, and `interp` may call either. | One sentence in the module README line and the `gpt` and `interp` briefs: "inputs longer than the context raise; crop to the last `ctx` tokens first".
- app/content/data/ai/seq_ops_l4.py | attn_update, block, lm_logits | note | Only `mha` takes a `mask` argument; the sublayer, block and model ops are always causal, so a key-padding or attention-ablation mask (`interp` patching and ablation) cannot be passed through. | Say so in the module README; a later module adds `mask=` if `interp` needs it (never a whole row of `-inf`, per the interfaces brief).
- app/content/data/ai/seq_ops_l4.py | (training with it) | note | Because the `bk` gradient is exactly zero, Adam moves `bk` only by round-off (about $10^{-12}$), and that round-off depends on the BLAS kernel: `--write` under one Haswell thread differs from the shipped file in exactly the 64 `bk` entries of block 1, by at most 7.3e-12. Harmless (the script checks the retrain to $10^{-4}$), but it explains why the file is not byte-stable across machines. | A line in the report; optionally note in l15 that $\mathbf b_K$ is counted although it never learns anything.
- app/content/data/ai/seq_ops_l4.py | mlp (for `gpt` L2) | note | The block uses ReLU; nanoGPT's `model.py`, which `gpt` L2 reads for layout, uses GELU. `gpt` L2's brief says to keep `sequence` L4's activation, so its number script must train and serve a ReLU model. | One sentence in `docs/briefs/gpt.md` Level 2: "the MLP is ReLU, as in `seq_ops_l4.mlp`; nanoGPT's GELU is named, not used".

## Number script and the weights file

The script recomputes: the shipped model is retrained (seed 0, 400 steps) and matched to the file, seeds 1 and 2 retrained for the held-out threshold, every accuracy and attention cell recomputed by a plain NumPy forward pass as well as by the autograd, the ablation table rerun with each write skipped, the trap run and both 10-step start seeds retrained, the three 6-block runs retrained (plus a second no-residual seed), every count by formula and by building zero arrays, and every code widget run with the page's judge (solution passes, starter fails, each mutant first fails its named test). The `--write` branch exits before any check, so no check reads values the branch could have planted; no dead branch elsewhere. Results hold with default threads and with one Haswell thread; the stalled 6-block curves are checked to 0.15, as the report says, and only thresholds are stated.

- docs/reports/sequence-L4-numbers.py | lines 488, 663, 669 | note | Some claims that cover on-screen numbers are tautologies: `6 * 2 == 12` (covers 12), `12 * 2 == 24`, `64 / 8 == 8 and 9 - 3 == 6 ... covers=[1/11, 1/5, 8, 9, 10.25]`, `abs(-log(1/11) - log 11) < 1e-12`. Each number is right. Second time in this course (review-sequence, Number scripts); one more makes it a rule under SESSION PROTOCOL 6. | Cover each number with the claim that computes it (the 6-block model's `nb=6` times 2, `D // H`), or `literal()` with a reason.
- docs/reports/sequence-L4-numbers.py | l16 quiz | note | Neither `E` nor `check_wrongs` caught the l16 `quiz[0]` slip whose value (5) is not what its `byKey` line describes (Content, first error). | `E(L16, 'quiz[0].widget.wrong[1].value', 7 - 3)` beside the answer check.

## Level 4

- app/content/courses/sequence/l16-a-tiny-transformer.json | quiz[0] wrong 'seven' | error | The slip is "You used $7 - t$, which is for six digits", but $7 - 3 = 4$, and the stored value is 5 ($8 - t$). A learner who makes the named slip types 4 and gets only the generic line; one who types 5 is told a slip they did not make. | `"value": 4`.
- app/content/courses/sequence/l16-a-tiny-transformer.json | screens[9] feedback.generic | error | "Recall what differed between the four curves": screens[7] draws three (as built, no residuals, no layer norms). | "...between the three curves."
- app/content/courses/sequence/review-4.json, homework-4.json, problems-4.json | 13 strings | warning | The KaTeX thousands separator `{,}` is written outside `$...$`, so the braces show on screen: review-4 `items[1].explain` ("norms 128: 12{,}704"); homework-4 `items[0].explain` ("421{,}697"), `items[4].explain` ("29{,}288{,}704"); problems-4 `items[0].parts[2].question`, `.feedback.correct`, `.explain`, `parts[3].feedback.correct`, `.explain`, `items[1].parts[1].question`, `parts[2].feedback.correct`, `.explain`, `parts[3].question`, `items[3].parts[2].question`. These 13 are most of the 17 such strings in all of `content/courses`. | Plain `12,704` outside maths (or wrap in `$...$`); raise a validator rule `[text-thousands-brace]` for `\d\{,\}\d` outside maths.
- app/content/courses/sequence/l16-a-tiny-transformer.json | objectives[0] | warning | "Run a one-block transformer from supplied weights": the model has two blocks, and `course.json` was changed to "two-block" at `04c28ba5`; the lesson file still says one-block. | Copy the `course.json` objective: "Run a two-block transformer from supplied weights, and train it for a few steps on a toy task."
- app/content/courses/sequence/l16-a-tiny-transformer.json | screens[7] explain | warning | "At 2 blocks such runs end close together: depth exposes the difference" is computed nowhere in the number script; the author report calls it "exploration, not stated". A stated claim without a recompute breaks "every stated number computed twice". | Either add the three 2-block runs to the script with a threshold claim (for example, all three end below a stated loss), or cut the sentence: "Depth is what exposes the difference."
- app/content/courses/sequence/l16-a-tiny-transformer.json | screens[9] question, feedback.correct | warning | "Which pair of design choices let the 6-block model train at all?" contradicts screens[7], where the run without layer norms trains (1.47 at the end, "slow, not stuck"); only the residuals are needed for it to train at all. | "Which pair of design choices let the 6-block model train well?"; feedback.correct as is ("without norms it limped").
- app/content/courses/sequence/l14-residual-stream.json | screens[6] explain | warning | "Removing attention 2 drops the score to 0.6%, so that part does the reversing": ablation shows that a part is needed, not that it does the task alone; removing attention 1 or MLP 1 also drops the score to 18.4% and 23.0%. `interp` will lean on exactly this distinction. | "Removing attention 2 drops the score to 0.6%, so the reversal depends on it most; MLP 2 adds little."
- app/content/courses/sequence/problems-4.json | items[1] prose | warning | "It reads 500 tokens and at most 64 positions" reads as a sequence of 500 tokens; 500 is the vocabulary (48,000 = 500 × 96). | "It knows 500 tokens and reads at most 64 positions", as `items[3]` says "knows 11 tokens".
- app/content/courses/sequence/l13-the-block.json | screens[8] tests | warning | The prose asks for `grad_check` "over $\mathbf x$ and every parameter", but a check that leaves `x` out passes all 4 tests (appendix, W1): the only planted bug is in a parameter. | Add to the prelude `def no_x_grad(x, P): return block(Tensor(x.data), P, 2)` (the input is used as a constant) and a test `block_grad_check(no_x_grad, X3, P4, M3) > 1e-3`: the solution gives 0.816, W1 gives 2.6e-9.
- app/content/courses/sequence/l15-counting-a-block.json | screens[6] tests | warning | Every test has an MLP width of exactly $4d$ (256 at 64, 128 at 32, 3,072 at 768), so a `block_params` that ignores `d_mlp` and uses `4 * d` passes all 8 (appendix, W4), although the signature and the l15 table (`2 d d_mlp + d_mlp + d`) make the width a free argument. | Add `block_params(64, 100)` expecting 29,860 and `model_params(11, 12, 32, 96, 2)` expecting 22,411 (both by formula and by array shapes).
- app/content/courses/sequence/l14-residual-stream.json | screens[3] prose | note | "The five terms have lengths that add to 25.27": the bars as shown (4.06, 3.76, 3.76, 5.80, 7.90) add to 25.28, which a learner who checks will get. | "add to about 25.3".
- app/content/courses/sequence/l16-a-tiny-transformer.json | screens[1] explain | note | "they put 0.71 and 0.70 on the right input and the rest nearby": row 5 puts 0.26 on the separator, five positions away. | "...and most of the rest on the separator or a neighbour".
- app/content/courses/sequence/l13-the-block.json | screens[0] explain | note | "the MLP reads a vector that already holds the other positions' information": under the mask it holds only earlier positions'. | "...the earlier positions' information."
- app/content/courses/sequence/l13-the-block.json | screens[2] prose | note | The MLP is said to have no biases; the attention's biases are not mentioned, although "attention returns $\operatorname{LN}_1(\mathbf x)\mathbf W_V\mathbf W_O$" needs them to be zero. | "...here $\mathbf W_V = \mathbf I$, $\mathbf W_O = 0.5\mathbf I$, with no biases anywhere."
- app/content/courses/sequence/l15-counting-a-block.json | screens[8] prose | note | "GPT-2 ties its embeddings ... Keep the unembedding's bias of 65" runs GPT-2 into our model; screens[10] then shows GPT-2 has no output bias. | "GPT-2 ties its embeddings: ... Tie our spike model the same way, keeping its unembedding bias of 65."
- app/content/courses/sequence/homework-4.json | items[1] option 'extra' why | note | "more norms on the main path make it worse, not better" is stated as fact with no source or run. | "A further norm on the main path still leaves no identity path."
- app/content/courses/sequence/homework-4.json | items[6] widget.model | note | "12, 48 or more identical blocks" contradicts l13's transfer ("only the weights differ"). | "12, 48 or more blocks of the same form, each with its own weights".
- app/content/courses/sequence/problems-4.json | items[0].parts[3] explain.text | note | "74,208 of 111,840: 66.4%. The MLP holds about two thirds: 66.4%." states 66.4% twice. | "...: 66.4%. The MLP holds about two thirds of the block."

Checked and right (no finding): every count of l15, review-4 (12,704; 9,408; 14,779 and each slip), problems-4 (37,248; 74,208; 111,840; 326,516; 278,516; 26,571; 8,448; the shares 66.4%, 29.6%, 17.4%, 95.6%; $6 \ln 11 = 14.387$; $0.99^6 = 0.9415$) and homework-4 (421,697 and its three slips, 29,288,704 and 55.9%, 35.9% untied, 43.1% blocks); GPT-2 small by the formula, 124,490,065, against the card's 124,439,808, a gap of 50,257 with no output bias; the l13 hand block $(1, 3) \to (0.5, 3.5) \to (0.5, 5.5)$ and its three slips ($-1.5$, 0, $-0.5$); l14's sums ($-2.335$, $-1.777$, $-2.091$, $-1.83$, $-0.59$); the l16 attention rows (output $t$ on input $7 - t$ for every row), $\ln 11$, $\log_2 11$, $\ln 10$, $\ln 5$, $\log_2 5$. Every numeric `wrong[]` has its `byKey` line and every `byKey` key is one its widget can return; the two order widgets' keys (`s3`, `s5`; `c`, `e`) fire when that line is the first out of place. The longform rubric adds to 10 and the model answer has 263 words (under 300). The claims about pre-norm are hedged as the brief asks ("a likely reason ... (Xiong et al., 2020). Post-norm can still train well with tuning"; "usually eases the warm-up"), and the residual stream is defined as the running sum each sublayer reads through its layer norm and writes to by addition, which is right.

## Code widgets

All 11 Python widgets pass `grade-all --code` alone (each file 0 failures; the authors' 43 mutants each first fail their named test). Slowest cases under the local Pyodide against the page limits: l16 `heldout_accuracy` on 1,000 inputs 1.56 s of 10 s (6.4x), `train_reverser` 100 steps 2.86 s of 20 s (7.0x; the author's desktop 3.6 s gives 5.6x), `block_grad_check` 0.23 s of 35 s; every other case under 0.3 s. No margin under 3x. No code widget has a `byKey` line, so none is keyed to a test that cannot fail.

The classes asked for are caught except one: the residual added after layer norm where pre-norm is taught (l13 W1, homework W2), layer norm over the wrong axis (l13 W2, l16 W4 on the final norm, homework W1), a count that forgets biases (l15 W1), the layer-norm gains (W2) or the output projection (W3), the MLP width wrong in the forward pass (l13 `mlp_block` W1) but **not** in the count (l15 W4 survives), no causal mask (the authors' l13 and homework mutants; my mask that also hides the diagonal, l13 W7), no gradient zeroing (l16 W1, zeroed once), and the residual applied twice (l13 W3, l14 W3, l16 W2, homework W3).

## Appendix: wrong solutions run through the grader

How: each source was graded by `makeRunner({ pkgs, root, jobs: 1 }).grade(spec, source, 'tests')` from `tools/code-runner.mjs` (the harness `grade-all.mjs --code` uses: the page's worker grader, its per-case limits, local Pyodide 0.27.7) on the unedited content files; the result is the first failing hidden test or that the source passes every test. 58 tried: 2 acceptable variants (l13 `block_grad_check` W3 without the mask `M`, and l16 `train_reverser` W5 with the gradient scaled by a constant, which Adam ignores); of the 56 wrong ones, 54 are caught and 2 survive (l13 `block_grad_check` W1, l15 `block_params` W4).

### l13-the-block screens[3] `mlp_block` (5 hidden tests)
- W1 mlp_block: hidden width d (first 8 units only) instead of 4d: **fails T1**.

```python
import numpy as np


def mlp_block(x, params):
    d = np.shape(x)[-1]
    h = np.maximum(0, np.asarray(x, dtype=float) @ params['W1'][:, :d] + params['b1'][:d])
    return h @ params['W2'][:d] + params['b2']
```

- W2 mlp_block: forgets b2: **fails T1**.

```python
import numpy as np


def mlp_block(x, params):
    h = np.maximum(0, np.asarray(x, dtype=float) @ params['W1'] + params['b1'])
    return h @ params['W2']
```

- W3 mlp_block: ReLU on the output as well: **fails T1**.

```python
import numpy as np


def mlp_block(x, params):
    h = np.maximum(0, np.asarray(x, dtype=float) @ params['W1'] + params['b1'])
    return np.maximum(0, h @ params['W2'] + params['b2'])
```

- W4 mlp_block: residual added inside the MLP: **fails T1**.

```python
import numpy as np


def mlp_block(x, params):
    x = np.asarray(x, dtype=float)
    h = np.maximum(0, x @ params['W1'] + params['b1'])
    return x + h @ params['W2'] + params['b2']
```


### l13-the-block screens[5] `transformer_block` (5 hidden tests)
- W1 transformer_block: residual added to the normalised copy (x = LN1(x) + Attn(LN1(x))): **fails T1**.

```python
import numpy as np
from nt_ops_l2 import layernorm
from seq_ops_l3 import attention, causal_mask, merge_heads, split_heads


def transformer_block(x, params, h):
    p = params
    x = np.asarray(x, dtype=float)
    T = x.shape[-2]
    a = layernorm(x, p['ln1_g'], p['ln1_b']).data
    q, k, v = (split_heads(a @ p[w] + p[b], h) for w, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
    att = merge_heads(attention(q, k, v, causal_mask(T))) @ p['Wo'] + p['bo']
    x = a + att.data
    m = layernorm(x, p['ln2_g'], p['ln2_b']).data
    return m + ((m @ p['W1'] + p['b1']).relu() @ p['W2'] + p['b2']).data
```

- W2 transformer_block: layer norm over the positions (axis 0) instead of the features: **fails T1**.

```python
import numpy as np
from nt_ops_l2 import layernorm
from seq_ops_l3 import attention, causal_mask, merge_heads, split_heads


def _ln0(x, g, b, eps=1e-5):
    mu = x.mean(axis=0, keepdims=True)
    var = ((x - mu) ** 2).mean(axis=0, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def transformer_block(x, params, h):
    p = params
    x = np.asarray(x, dtype=float)
    T = x.shape[-2]
    a = _ln0(x, p['ln1_g'], p['ln1_b'])
    q, k, v = (split_heads(a @ p[w] + p[b], h) for w, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
    att = merge_heads(attention(q, k, v, causal_mask(T))) @ p['Wo'] + p['bo']
    x = x + att.data
    m = _ln0(x, p['ln2_g'], p['ln2_b'])
    return x + ((m @ p['W1'] + p['b1']).relu() @ p['W2'] + p['b2']).data
```

- W3 transformer_block: residual applied twice (x + x + Attn): **fails T1**.

```python
import numpy as np
from nt_ops_l2 import layernorm
from seq_ops_l3 import attention, causal_mask, merge_heads, split_heads


def transformer_block(x, params, h):
    p = params
    x = np.asarray(x, dtype=float)
    T = x.shape[-2]
    a = layernorm(x, p['ln1_g'], p['ln1_b'])
    q, k, v = (split_heads(a @ p[w] + p[b], h) for w, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
    att = merge_heads(attention(q, k, v, causal_mask(T))) @ p['Wo'] + p['bo']
    x = x + x + att.data
    m = layernorm(x, p['ln2_g'], p['ln2_b'])
    return x + ((m @ p['W1'] + p['b1']).relu() @ p['W2'] + p['b2']).data
```

- W4 transformer_block: LN 1 parameters used for both norms: **fails T1**.

```python
import numpy as np
from nt_ops_l2 import layernorm
from seq_ops_l3 import attention, causal_mask, merge_heads, split_heads


def transformer_block(x, params, h):
    p = params
    x = np.asarray(x, dtype=float)
    T = x.shape[-2]
    a = layernorm(x, p['ln1_g'], p['ln1_b'])
    q, k, v = (split_heads(a @ p[w] + p[b], h) for w, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
    att = merge_heads(attention(q, k, v, causal_mask(T))) @ p['Wo'] + p['bo']
    x = x + att.data
    m = layernorm(x, p['ln1_g'], p['ln1_b'])
    return x + ((m @ p['W1'] + p['b1']).relu() @ p['W2'] + p['b2']).data
```

- W5 transformer_block: no ReLU in the MLP: **fails T1**.

```python
import numpy as np
from nt_ops_l2 import layernorm
from seq_ops_l3 import attention, causal_mask, merge_heads, split_heads


def transformer_block(x, params, h):
    p = params
    x = np.asarray(x, dtype=float)
    T = x.shape[-2]
    a = layernorm(x, p['ln1_g'], p['ln1_b'])
    q, k, v = (split_heads(a @ p[w] + p[b], h) for w, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
    att = merge_heads(attention(q, k, v, causal_mask(T))) @ p['Wo'] + p['bo']
    x = x + att.data
    m = layernorm(x, p['ln2_g'], p['ln2_b'])
    return x + ((m @ p['W1'] + p['b1']) @ p['W2'] + p['b2']).data
```

- W6 transformer_block: MLP before attention: **fails T1**.

```python
import numpy as np
from nt_ops_l2 import layernorm
from seq_ops_l3 import attention, causal_mask, merge_heads, split_heads


def transformer_block(x, params, h):
    p = params
    x = np.asarray(x, dtype=float)
    T = x.shape[-2]
    m = layernorm(x, p['ln2_g'], p['ln2_b'])
    x = x + ((m @ p['W1'] + p['b1']).relu() @ p['W2'] + p['b2']).data
    a = layernorm(x, p['ln1_g'], p['ln1_b'])
    q, k, v = (split_heads(a @ p[w] + p[b], h) for w, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
    att = merge_heads(attention(q, k, v, causal_mask(T))) @ p['Wo'] + p['bo']
    return x + att.data
```

- W7 transformer_block: mask that also hides the diagonal: **fails T1**.

```python
import numpy as np
from nt_ops_l2 import layernorm
from seq_ops_l3 import attention, causal_mask, merge_heads, split_heads


def transformer_block(x, params, h):
    p = params
    x = np.asarray(x, dtype=float)
    T = x.shape[-2]
    a = layernorm(x, p['ln1_g'], p['ln1_b'])
    q, k, v = (split_heads(a @ p[w] + p[b], h) for w, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
    M = np.triu(np.full((T, T), -1e9), 0)
    M[0, 0] = 0.0
    att = merge_heads(attention(q, k, v, M)) @ p['Wo'] + p['bo']
    x = x + att.data
    m = layernorm(x, p['ln2_g'], p['ln2_b'])
    return x + ((m @ p['W1'] + p['b1']).relu() @ p['W2'] + p['b2']).data
```


### l13-the-block screens[8] `block_grad_check` (4 hidden tests)
- W1 block_grad_check: checks the parameters but not x: **SURVIVES**.

```python
import numpy as np
from autograd import Tensor, grad_check


def block_grad_check(fn, x, params, M):
    X = Tensor(np.array(x, dtype=float))
    P = {k: Tensor(np.array(v, dtype=float)) for k, v in params.items()}
    return grad_check(lambda: (fn(X, P) * M).sum(), list(P.values()))
```

- W2 block_grad_check: checks the weight matrices only, no biases or norms: **fails T2**.

```python
import numpy as np
from autograd import Tensor, grad_check


def block_grad_check(fn, x, params, M):
    X = Tensor(np.array(x, dtype=float))
    P = {k: Tensor(np.array(v, dtype=float)) for k, v in params.items()}
    return grad_check(lambda: (fn(X, P) * M).sum(), [X] + [P[k] for k in P if k.startswith('W')])
```

- W3 block_grad_check: loss sum(fn) without the mask M: **SURVIVES** (an acceptable variant: still a sound check over every Tensor, and it catches the planted bug).

```python
import numpy as np
from autograd import Tensor, grad_check


def block_grad_check(fn, x, params, M):
    X = Tensor(np.array(x, dtype=float))
    P = {k: Tensor(np.array(v, dtype=float)) for k, v in params.items()}
    return grad_check(lambda: fn(X, P).sum(), [X] + list(P.values()))
```

- W4 block_grad_check: returns the error of the attention weights only (Wq, Wk, Wv, Wo): **fails T2**.

```python
import numpy as np
from autograd import Tensor, grad_check


def block_grad_check(fn, x, params, M):
    X = Tensor(np.array(x, dtype=float))
    P = {k: Tensor(np.array(v, dtype=float)) for k, v in params.items()}
    return grad_check(lambda: (fn(X, P) * M).sum(), [P[k] for k in ('Wq', 'Wk', 'Wv', 'Wo')])
```


### l14-residual-stream screens[4] `stream_trace`, `update_norms` (6 hidden tests)
- W1 stream_trace: no positions in x0: **fails T1**.

```python
import numpy as np
from seq_ops_l4 import attn_update, mlp_update
from nt_ops_l2 import layernorm


def update_norms(trace):
    return np.array([np.linalg.norm(trace[k] - trace[k - 1], axis=-1) for k in range(1, len(trace))])


def stream_trace(tokens, model, h):
    tokens = np.asarray(tokens)
    x = model['E'][tokens]
    trace = [x]
    for p in model['blocks']:
        x = x + attn_update(x, p, h).data
        trace.append(x)
        x = x + mlp_update(x, p).data
        trace.append(x)
    return trace
```

- W2 stream_trace: one entry per block, not per part: **fails T2**.

```python
import numpy as np
from seq_ops_l4 import attn_update, mlp_update
from nt_ops_l2 import layernorm


def update_norms(trace):
    return np.array([np.linalg.norm(trace[k] - trace[k - 1], axis=-1) for k in range(1, len(trace))])


def stream_trace(tokens, model, h):
    tokens = np.asarray(tokens)
    x = model['E'][tokens] + model['P'][:len(tokens)]
    trace = [x]
    for p in model['blocks']:
        x = x + attn_update(x, p, h).data
        x = x + mlp_update(x, p).data
        trace.append(x)
    return trace
```

- W3 stream_trace: the residual applied twice (x + x + write): **fails T1**.

```python
import numpy as np
from seq_ops_l4 import attn_update, mlp_update
from nt_ops_l2 import layernorm


def update_norms(trace):
    return np.array([np.linalg.norm(trace[k] - trace[k - 1], axis=-1) for k in range(1, len(trace))])


def stream_trace(tokens, model, h):
    tokens = np.asarray(tokens)
    x = model['E'][tokens] + model['P'][:len(tokens)]
    trace = [x]
    for p in model['blocks']:
        x = x + x + attn_update(x, p, h).data
        trace.append(x)
        x = x + x + mlp_update(x, p).data
        trace.append(x)
    return trace
```

- W4 stream_trace: post-norm, the stream normalised after each addition: **fails T1**.

```python
import numpy as np
from seq_ops_l4 import attn_update, mlp_update
from nt_ops_l2 import layernorm


def update_norms(trace):
    return np.array([np.linalg.norm(trace[k] - trace[k - 1], axis=-1) for k in range(1, len(trace))])


def stream_trace(tokens, model, h):
    tokens = np.asarray(tokens)
    x = model['E'][tokens] + model['P'][:len(tokens)]
    trace = [x]
    for p in model['blocks']:
        x = layernorm(x + attn_update(x, p, h).data, p['ln1_g'], p['ln1_b']).data
        trace.append(x)
        x = layernorm(x + mlp_update(x, p).data, p['ln2_g'], p['ln2_b']).data
        trace.append(x)
    return trace
```

- W5 update_norms: squared lengths: **fails T4**.

```python
import numpy as np
from seq_ops_l4 import attn_update, mlp_update


def stream_trace(tokens, model, h):
    tokens = np.asarray(tokens)
    x = model['E'][tokens] + model['P'][:len(tokens)]
    trace = [x]
    for p in model['blocks']:
        x = x + attn_update(x, p, h).data
        trace.append(x)
        x = x + mlp_update(x, p).data
        trace.append(x)
    return trace


def update_norms(trace):
    return np.array([((trace[k] - trace[k - 1]) ** 2).sum(-1) for k in range(1, len(trace))])
```

- W6 update_norms: length of each stream entry against the first (cumulative): **fails T4**.

```python
import numpy as np
from seq_ops_l4 import attn_update, mlp_update


def stream_trace(tokens, model, h):
    tokens = np.asarray(tokens)
    x = model['E'][tokens] + model['P'][:len(tokens)]
    trace = [x]
    for p in model['blocks']:
        x = x + attn_update(x, p, h).data
        trace.append(x)
        x = x + mlp_update(x, p).data
        trace.append(x)
    return trace


def update_norms(trace):
    return np.array([np.linalg.norm(trace[k] - trace[0], axis=-1) for k in range(1, len(trace))])
```


### l14-residual-stream screens[7] `ablate_sublayer` (5 hidden tests)
- W1 ablate_sublayer: parts numbered attention 1, attention 2, MLP 1, MLP 2: **fails T2**.

```python
import numpy as np
from nt_ops_l2 import layernorm
from seq_ops_l4 import attn_update, mlp_update


def ablate_sublayer(tokens, model, k, h=4):
    tokens = np.asarray(tokens)
    x = model['E'][tokens] + model['P'][:len(tokens)]
    n = len(model['blocks'])
    for i, p in enumerate(model['blocks']):
        if k != i + 1:
            x = x + attn_update(x, p, h).data
        if k != n + i + 1:
            x = x + mlp_update(x, p).data
    return layernorm(x, model['lnf_g'], model['lnf_b']).data @ model['U'] + model['c']
```

- W2 ablate_sublayer: removes the whole block that holds part k: **fails T1**.

```python
import numpy as np
from nt_ops_l2 import layernorm
from seq_ops_l4 import attn_update, mlp_update


def ablate_sublayer(tokens, model, k, h=4):
    tokens = np.asarray(tokens)
    x = model['E'][tokens] + model['P'][:len(tokens)]
    for i, p in enumerate(model['blocks']):
        if (k + 1) // 2 == i + 1:
            continue
        x = x + attn_update(x, p, h).data
        x = x + mlp_update(x, p).data
    return layernorm(x, model['lnf_g'], model['lnf_b']).data @ model['U'] + model['c']
```

- W3 ablate_sublayer: stops at part k (drops every later write too): **fails T1**.

```python
import numpy as np
from nt_ops_l2 import layernorm
from seq_ops_l4 import attn_update, mlp_update


def ablate_sublayer(tokens, model, k, h=4):
    tokens = np.asarray(tokens)
    x = model['E'][tokens] + model['P'][:len(tokens)]
    j = 0
    for p in model['blocks']:
        for part in (lambda x: attn_update(x, p, h), lambda x: mlp_update(x, p)):
            j += 1
            if j == k:
                return layernorm(x, model['lnf_g'], model['lnf_b']).data @ model['U'] + model['c']
            x = x + part(x).data
    return layernorm(x, model['lnf_g'], model['lnf_b']).data @ model['U'] + model['c']
```

- W4 ablate_sublayer: the part reads zeros instead of the stream: **fails T1**.

```python
import numpy as np
from nt_ops_l2 import layernorm
from seq_ops_l4 import attn_update, mlp_update


def ablate_sublayer(tokens, model, k, h=4):
    tokens = np.asarray(tokens)
    x = model['E'][tokens] + model['P'][:len(tokens)]
    j = 0
    for p in model['blocks']:
        for part in (lambda x: attn_update(x, p, h), lambda x: mlp_update(x, p)):
            j += 1
            x = x + part(np.zeros_like(x) if j == k else x).data
    return layernorm(x, model['lnf_g'], model['lnf_b']).data @ model['U'] + model['c']
```


### l15-counting-a-block screens[6] `block_params`, `model_params`, `count_arrays` (8 hidden tests)
- W1 model_params: unembedding without its bias: **fails T3**.

```python
import numpy as np


def block_params(d, d_mlp, bias=True):
    attn = 4 * d * d + (4 * d if bias else 0)
    mlp = 2 * d * d_mlp + (d_mlp + d if bias else 0)
    norms = 4 * d if bias else 2 * d
    return attn + mlp + norms


def model_params(vocab, ctx, d, d_mlp, n_blocks, tied=False):
    unembed = (0 if tied else d * vocab)
    return vocab * d + ctx * d + n_blocks * block_params(d, d_mlp) + 2 * d + unembed


def count_arrays(params):
    if isinstance(params, dict):
        return sum(count_arrays(v) for v in params.values())
    if isinstance(params, (list, tuple)):
        return sum(count_arrays(v) for v in params)
    return int(np.size(params))
```

- W2 block_params: forgets the layer-norm gains (norms 2d with biases, 0 without): **fails T1**.

```python
import numpy as np


def block_params(d, d_mlp, bias=True):
    attn = 4 * d * d + (4 * d if bias else 0)
    mlp = 2 * d * d_mlp + (d_mlp + d if bias else 0)
    norms = 2 * d if bias else 0
    return attn + mlp + norms


def model_params(vocab, ctx, d, d_mlp, n_blocks, tied=False):
    unembed = (0 if tied else d * vocab) + vocab
    return vocab * d + ctx * d + n_blocks * block_params(d, d_mlp) + 2 * d + unembed


def count_arrays(params):
    if isinstance(params, dict):
        return sum(count_arrays(v) for v in params.values())
    if isinstance(params, (list, tuple)):
        return sum(count_arrays(v) for v in params)
    return int(np.size(params))
```

- W3 block_params: forgets the output projection W_O and b_O: **fails T1**.

```python
import numpy as np


def block_params(d, d_mlp, bias=True):
    attn = 3 * d * d + (3 * d if bias else 0)
    mlp = 2 * d * d_mlp + (d_mlp + d if bias else 0)
    norms = 4 * d if bias else 2 * d
    return attn + mlp + norms


def model_params(vocab, ctx, d, d_mlp, n_blocks, tied=False):
    unembed = (0 if tied else d * vocab) + vocab
    return vocab * d + ctx * d + n_blocks * block_params(d, d_mlp) + 2 * d + unembed


def count_arrays(params):
    if isinstance(params, dict):
        return sum(count_arrays(v) for v in params.values())
    if isinstance(params, (list, tuple)):
        return sum(count_arrays(v) for v in params)
    return int(np.size(params))
```

- W4 block_params: MLP width taken as 4d, ignoring d_mlp: **SURVIVES**.

```python
import numpy as np


def block_params(d, d_mlp, bias=True):
    attn = 4 * d * d + (4 * d if bias else 0)
    mlp = 2 * d * 4 * d + (4 * d + d if bias else 0)
    norms = 4 * d if bias else 2 * d
    return attn + mlp + norms


def model_params(vocab, ctx, d, d_mlp, n_blocks, tied=False):
    unembed = (0 if tied else d * vocab) + vocab
    return vocab * d + ctx * d + n_blocks * block_params(d, d_mlp) + 2 * d + unembed


def count_arrays(params):
    if isinstance(params, dict):
        return sum(count_arrays(v) for v in params.values())
    if isinstance(params, (list, tuple)):
        return sum(count_arrays(v) for v in params)
    return int(np.size(params))
```

- W5 model_params: no final layer norm: **fails T3**.

```python
import numpy as np


def block_params(d, d_mlp, bias=True):
    attn = 4 * d * d + (4 * d if bias else 0)
    mlp = 2 * d * d_mlp + (d_mlp + d if bias else 0)
    norms = 4 * d if bias else 2 * d
    return attn + mlp + norms


def model_params(vocab, ctx, d, d_mlp, n_blocks, tied=False):
    unembed = (0 if tied else d * vocab) + vocab
    return vocab * d + ctx * d + n_blocks * block_params(d, d_mlp) + unembed


def count_arrays(params):
    if isinstance(params, dict):
        return sum(count_arrays(v) for v in params.values())
    if isinstance(params, (list, tuple)):
        return sum(count_arrays(v) for v in params)
    return int(np.size(params))
```

- W6 count_arrays: counts arrays, not numbers: **fails T5**.

```python
import numpy as np


def block_params(d, d_mlp, bias=True):
    attn = 4 * d * d + (4 * d if bias else 0)
    mlp = 2 * d * d_mlp + (d_mlp + d if bias else 0)
    norms = 4 * d if bias else 2 * d
    return attn + mlp + norms


def model_params(vocab, ctx, d, d_mlp, n_blocks, tied=False):
    unembed = (0 if tied else d * vocab) + vocab
    return vocab * d + ctx * d + n_blocks * block_params(d, d_mlp) + 2 * d + unembed


def count_arrays(params):
    if isinstance(params, dict):
        return sum(count_arrays(v) for v in params.values())
    if isinstance(params, (list, tuple)):
        return sum(count_arrays(v) for v in params)
    return 1
```

- W7 block_params: MLP biases both of width d: **fails T1**.

```python
import numpy as np


def block_params(d, d_mlp, bias=True):
    attn = 4 * d * d + (4 * d if bias else 0)
    mlp = 2 * d * d_mlp + (2 * d if bias else 0)
    norms = 4 * d if bias else 2 * d
    return attn + mlp + norms


def model_params(vocab, ctx, d, d_mlp, n_blocks, tied=False):
    unembed = (0 if tied else d * vocab) + vocab
    return vocab * d + ctx * d + n_blocks * block_params(d, d_mlp) + 2 * d + unembed


def count_arrays(params):
    if isinstance(params, dict):
        return sum(count_arrays(v) for v in params.values())
    if isinstance(params, (list, tuple)):
        return sum(count_arrays(v) for v in params)
    return int(np.size(params))
```

- W8 model_params: tied also drops the position table: **fails T4**.

```python
import numpy as np


def block_params(d, d_mlp, bias=True):
    attn = 4 * d * d + (4 * d if bias else 0)
    mlp = 2 * d * d_mlp + (d_mlp + d if bias else 0)
    norms = 4 * d if bias else 2 * d
    return attn + mlp + norms


def model_params(vocab, ctx, d, d_mlp, n_blocks, tied=False):
    unembed = (0 if tied else d * vocab) + vocab
    return vocab * d + (0 if tied else ctx * d) + n_blocks * block_params(d, d_mlp) + 2 * d + unembed


def count_arrays(params):
    if isinstance(params, dict):
        return sum(count_arrays(v) for v in params.values())
    if isinstance(params, (list, tuple)):
        return sum(count_arrays(v) for v in params)
    return int(np.size(params))
```


### l16-a-tiny-transformer screens[3] `tiny_forward` (5 hidden tests)
- W1 tiny_forward: one head per block (h ignored): **fails T1**.

```python
import numpy as np
from nt_ops_l2 import layernorm
from seq_ops_l4 import block


def tiny_forward(model, seq, h=4):
    seq = np.asarray(seq)
    x = model['E'][seq] + model['P'][:seq.shape[-1]]
    for p in model['blocks']:
        x = block(x, p, 1).data
    return layernorm(x, model['lnf_g'], model['lnf_b']).data @ model['U'] + model['c']
```

- W2 tiny_forward: the residual added again around each block: **fails T1**.

```python
import numpy as np
from nt_ops_l2 import layernorm
from seq_ops_l4 import block


def tiny_forward(model, seq, h=4):
    seq = np.asarray(seq)
    x = model['E'][seq] + model['P'][:seq.shape[-1]]
    for p in model['blocks']:
        x = x + block(x, p, h).data
    return layernorm(x, model['lnf_g'], model['lnf_b']).data @ model['U'] + model['c']
```

- W3 tiny_forward: no output bias c: **fails T1**.

```python
import numpy as np
from nt_ops_l2 import layernorm
from seq_ops_l4 import block


def tiny_forward(model, seq, h=4):
    seq = np.asarray(seq)
    x = model['E'][seq] + model['P'][:seq.shape[-1]]
    for p in model['blocks']:
        x = block(x, p, h).data
    return layernorm(x, model['lnf_g'], model['lnf_b']).data @ model['U']
```

- W4 tiny_forward: the final layer norm over positions (applied to x.T): **fails T1**.

```python
import numpy as np
from nt_ops_l2 import layernorm
from seq_ops_l4 import block


def tiny_forward(model, seq, h=4):
    seq = np.asarray(seq)
    x = model['E'][seq] + model['P'][:seq.shape[-1]]
    for p in model['blocks']:
        x = block(x, p, h).data
    z = np.swapaxes(x, -1, -2)
    z = layernorm(z, np.ones(z.shape[-1]), np.zeros(z.shape[-1])).data
    x = np.swapaxes(z, -1, -2) * model['lnf_g'] + model['lnf_b']
    return x @ model['U'] + model['c']
```


### l16-a-tiny-transformer screens[4] `reverse_with`, `heldout_accuracy` (4 hidden tests)
- W1 heldout_accuracy: counts the right rows instead of their share: **fails T2**.

```python
import numpy as np
from seq_ops_l4 import lm_logits


def reverse_with(model, digits, h=4):
    digits = np.asarray(digits)
    x = np.concatenate([digits, np.full((len(digits), 1), 10)], axis=1)
    for _ in range(6):
        nxt = lm_logits(x, model, h).data[:, -1].argmax(-1)
        x = np.concatenate([x, nxt[:, None]], axis=1)
    return x[:, 7:]


def heldout_accuracy(model, digits):
    digits = np.asarray(digits)
    return float(np.sum((reverse_with(model, digits) == digits[:, ::-1]).all(axis=1)))
```

- W2 heldout_accuracy: compares with the digits unreversed: **fails T1**.

```python
import numpy as np
from seq_ops_l4 import lm_logits


def reverse_with(model, digits, h=4):
    digits = np.asarray(digits)
    x = np.concatenate([digits, np.full((len(digits), 1), 10)], axis=1)
    for _ in range(6):
        nxt = lm_logits(x, model, h).data[:, -1].argmax(-1)
        x = np.concatenate([x, nxt[:, None]], axis=1)
    return x[:, 7:]


def heldout_accuracy(model, digits):
    digits = np.asarray(digits)
    return float(np.mean((reverse_with(model, digits) == digits).all(axis=1)))
```

- W3 reverse_with: no separator before decoding: **fails T1**.

```python
import numpy as np
from seq_ops_l4 import lm_logits


def reverse_with(model, digits, h=4):
    x = np.asarray(digits)
    for _ in range(6):
        nxt = lm_logits(x, model, h).data[:, -1].argmax(-1)
        x = np.concatenate([x, nxt[:, None]], axis=1)
    return x[:, 6:]


def heldout_accuracy(model, digits):
    digits = np.asarray(digits)
    return float(np.mean((reverse_with(model, digits) == digits[:, ::-1]).all(axis=1)))
```

- W4 reverse_with: decodes five digits and pads the sixth by copying the first input: **fails T2**.

```python
import numpy as np
from seq_ops_l4 import lm_logits


def reverse_with(model, digits, h=4):
    digits = np.asarray(digits)
    x = np.concatenate([digits, np.full((len(digits), 1), 10)], axis=1)
    for _ in range(5):
        nxt = lm_logits(x, model, h).data[:, -1].argmax(-1)
        x = np.concatenate([x, nxt[:, None]], axis=1)
    return np.concatenate([x[:, 7:], digits[:, :1]], axis=1)


def heldout_accuracy(model, digits):
    digits = np.asarray(digits)
    return float(np.mean((reverse_with(model, digits) == digits[:, ::-1]).all(axis=1)))
```


### l16-a-tiny-transformer screens[6] `train_reverser` (4 hidden tests)
- W1 train_reverser: zeroes the gradients once, before the loop: **fails T1**.

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step
from seq_ops_l4 import flat_params, lm_logits


def train_reverser(model, X, Y, steps, lr):
    P = {k: Tensor(v) for k, v in model.items() if k != 'blocks'}
    P['blocks'] = [{k: Tensor(v) for k, v in p.items()} for p in model['blocks']]
    params = [a for _, a in flat_params(P)]
    m = [np.zeros_like(p.data) for p in params]
    v = [np.zeros_like(p.data) for p in params]
    keep = np.nonzero(Y.reshape(-1) >= 0)[0]
    losses = []
    for p in params:
        p.zero_grad()
    for t in range(1, steps + 1):
        loss = cross_entropy(lm_logits(X, P, 4).reshape(-1, 11)[keep], Y.reshape(-1)[keep])
        losses.append(loss.item())
        loss.backward()
        new, m, v = adam_step([p.data for p in params], [p.grad for p in params], m, v, t, lr)
        for p, a in zip(params, new):
            p.data = a
    return losses
```

- W2 train_reverser: records the loss after the step (a second forward pass): **fails T1**.

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step
from seq_ops_l4 import flat_params, lm_logits


def train_reverser(model, X, Y, steps, lr):
    P = {k: Tensor(v) for k, v in model.items() if k != 'blocks'}
    P['blocks'] = [{k: Tensor(v) for k, v in p.items()} for p in model['blocks']]
    params = [a for _, a in flat_params(P)]
    m = [np.zeros_like(p.data) for p in params]
    v = [np.zeros_like(p.data) for p in params]
    keep = np.nonzero(Y.reshape(-1) >= 0)[0]
    losses = []
    for t in range(1, steps + 1):
        for p in params:
            p.zero_grad()
        loss = cross_entropy(lm_logits(X, P, 4).reshape(-1, 11)[keep], Y.reshape(-1)[keep])
        loss.backward()
        new, m, v = adam_step([p.data for p in params], [p.grad for p in params], m, v, t, lr)
        for p, a in zip(params, new):
            p.data = a
        losses.append(cross_entropy(lm_logits(X, P, 4).reshape(-1, 11)[keep], Y.reshape(-1)[keep]).item())
    return losses
```

- W3 train_reverser: only the block arrays are Tensors; embeddings, U, c stay fixed: **fails T1**.

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step
from seq_ops_l4 import flat_params, lm_logits


def train_reverser(model, X, Y, steps, lr):
    P = dict(model)
    P['blocks'] = [{k: Tensor(v) for k, v in p.items()} for p in model['blocks']]
    params = [a for _, a in flat_params(P) if isinstance(a, Tensor)]
    m = [np.zeros_like(p.data) for p in params]
    v = [np.zeros_like(p.data) for p in params]
    keep = np.nonzero(Y.reshape(-1) >= 0)[0]
    losses = []
    for t in range(1, steps + 1):
        for p in params:
            p.zero_grad()
        loss = cross_entropy(lm_logits(X, P, 4).reshape(-1, 11)[keep], Y.reshape(-1)[keep])
        losses.append(loss.item())
        loss.backward()
        new, m, v = adam_step([p.data for p in params], [p.grad for p in params], m, v, t, lr)
        for p, a in zip(params, new):
            p.data = a
    return losses
```

- W4 train_reverser: a warm-up and cosine schedule instead of the fixed rate: **fails T1**.

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step
from seq_ops_l4 import flat_params, lm_logits


def train_reverser(model, X, Y, steps, lr):
    from nt_ops_l1 import warmup_cosine
    P = {k: Tensor(v) for k, v in model.items() if k != 'blocks'}
    P['blocks'] = [{k: Tensor(v) for k, v in p.items()} for p in model['blocks']]
    params = [a for _, a in flat_params(P)]
    m = [np.zeros_like(p.data) for p in params]
    v = [np.zeros_like(p.data) for p in params]
    keep = np.nonzero(Y.reshape(-1) >= 0)[0]
    losses = []
    for t in range(1, steps + 1):
        for p in params:
            p.zero_grad()
        loss = cross_entropy(lm_logits(X, P, 4).reshape(-1, 11)[keep], Y.reshape(-1)[keep])
        losses.append(loss.item())
        loss.backward()
        new, m, v = adam_step([p.data for p in params], [p.grad for p in params], m, v, t, warmup_cosine(t, lr, 2, steps))
        for p, a in zip(params, new):
            p.data = a
    return losses
```

- W5 train_reverser: sums the loss over scored tokens instead of the mean, backward on the loss times the 192 scored tokens: **SURVIVES** (a correct alternative in effect: Adam is invariant to a constant scale of the gradient, up to its epsilon, and the recorded losses are the means).

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step
from seq_ops_l4 import flat_params, lm_logits


def train_reverser(model, X, Y, steps, lr):
    P = {k: Tensor(v) for k, v in model.items() if k != 'blocks'}
    P['blocks'] = [{k: Tensor(v) for k, v in p.items()} for p in model['blocks']]
    params = [a for _, a in flat_params(P)]
    m = [np.zeros_like(p.data) for p in params]
    v = [np.zeros_like(p.data) for p in params]
    keep = np.nonzero(Y.reshape(-1) >= 0)[0]
    losses = []
    for t in range(1, steps + 1):
        for p in params:
            p.zero_grad()
        loss = cross_entropy(lm_logits(X, P, 4).reshape(-1, 11)[keep], Y.reshape(-1)[keep])
        losses.append(loss.item())
        (loss * float(len(keep))).backward()
        new, m, v = adam_step([p.data for p in params], [p.grad for p in params], m, v, t, lr)
        for p, a in zip(params, new):
            p.data = a
    return losses
```


### homework-4 items[2] `is_per_position` (5 hidden tests)
- W1 is_per_position: perturbs only the last row: **fails T2**.

```python
import numpy as np


def is_per_position(f, x):
    x = np.asarray(x, dtype=float)
    base = np.asarray(f(x))
    j = len(x) - 1
    y = x.copy()
    y[j] = y[j] + 1.0
    moved = np.abs(np.asarray(f(y)) - base).max(axis=-1) > 1e-9
    moved[j] = False
    return not moved.any()
```

- W2 is_per_position: perturbs every row at once: **fails T1**.

```python
import numpy as np


def is_per_position(f, x):
    x = np.asarray(x, dtype=float)
    y = x + 1.0
    return bool(np.allclose(np.asarray(f(y)), np.asarray(f(x))))
```

- W3 is_per_position: checks that the perturbed row moves and nothing else: **fails T4**.

```python
import numpy as np


def is_per_position(f, x):
    x = np.asarray(x, dtype=float)
    base = np.asarray(f(x))
    for j in range(len(x)):
        y = x.copy()
        y[j] = y[j] + 1.0
        moved = np.abs(np.asarray(f(y)) - base).max(axis=-1) > 1e-9
        if not moved[j]:
            return False
        moved[j] = False
        if moved.any():
            return False
    return True
```


### homework-4 items[7] `transformer_lm_forward` (8 hidden tests)
- W1 transformer_lm_forward: layer norm over positions (axis 0): **fails T1**.

```python
import numpy as np


def _ln(x, g, b, eps=1e-5, axis=-1):
    mu = x.mean(axis, keepdims=True)
    var = ((x - mu) ** 2).mean(axis, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def transformer_lm_forward(tokens, params, n_blocks, h):
    tokens = np.asarray(tokens)
    T = len(tokens)
    x = params['E'][tokens] + params['P'][:T]
    d = x.shape[-1]
    w = d // h
    mask = np.triu(np.full((T, T), -np.inf), 1)
    for p in params['blocks'][:n_blocks]:
        a = _ln(x, p['ln1_g'], p['ln1_b'], axis=0)
        q, k, v = ((a @ p[W] + p[b]).reshape(T, h, w).transpose(1, 0, 2) for W, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
        S = q @ k.transpose(0, 2, 1) / np.sqrt(w) + mask
        A = np.exp(S - S.max(-1, keepdims=True))
        A = A / A.sum(-1, keepdims=True)
        o = (A @ v).transpose(1, 0, 2).reshape(T, d) @ p['Wo'] + p['bo']
        x = x + o
        m = _ln(x, p['ln2_g'], p['ln2_b'], axis=0)
        x = x + np.maximum(0, m @ p['W1'] + p['b1']) @ p['W2'] + p['b2']
    return _ln(x, params['lnf_g'], params['lnf_b']) @ params['U'] + params['c']
```

- W2 transformer_lm_forward: residual added after the layer norm (x = LN(x) + Attn(LN(x))): **fails T1**.

```python
import numpy as np


def _ln(x, g, b, eps=1e-5, axis=-1):
    mu = x.mean(axis, keepdims=True)
    var = ((x - mu) ** 2).mean(axis, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def transformer_lm_forward(tokens, params, n_blocks, h):
    tokens = np.asarray(tokens)
    T = len(tokens)
    x = params['E'][tokens] + params['P'][:T]
    d = x.shape[-1]
    w = d // h
    mask = np.triu(np.full((T, T), -np.inf), 1)
    for p in params['blocks'][:n_blocks]:
        a = _ln(x, p['ln1_g'], p['ln1_b'])
        q, k, v = ((a @ p[W] + p[b]).reshape(T, h, w).transpose(1, 0, 2) for W, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
        S = q @ k.transpose(0, 2, 1) / np.sqrt(w) + mask
        A = np.exp(S - S.max(-1, keepdims=True))
        A = A / A.sum(-1, keepdims=True)
        o = (A @ v).transpose(1, 0, 2).reshape(T, d) @ p['Wo'] + p['bo']
        x = a + o
        m = _ln(x, p['ln2_g'], p['ln2_b'])
        x = m + np.maximum(0, m @ p['W1'] + p['b1']) @ p['W2'] + p['b2']
    return _ln(x, params['lnf_g'], params['lnf_b']) @ params['U'] + params['c']
```

- W3 transformer_lm_forward: residual applied twice: **fails T1**.

```python
import numpy as np


def _ln(x, g, b, eps=1e-5, axis=-1):
    mu = x.mean(axis, keepdims=True)
    var = ((x - mu) ** 2).mean(axis, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def transformer_lm_forward(tokens, params, n_blocks, h):
    tokens = np.asarray(tokens)
    T = len(tokens)
    x = params['E'][tokens] + params['P'][:T]
    d = x.shape[-1]
    w = d // h
    mask = np.triu(np.full((T, T), -np.inf), 1)
    for p in params['blocks'][:n_blocks]:
        a = _ln(x, p['ln1_g'], p['ln1_b'])
        q, k, v = ((a @ p[W] + p[b]).reshape(T, h, w).transpose(1, 0, 2) for W, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
        S = q @ k.transpose(0, 2, 1) / np.sqrt(w) + mask
        A = np.exp(S - S.max(-1, keepdims=True))
        A = A / A.sum(-1, keepdims=True)
        o = (A @ v).transpose(1, 0, 2).reshape(T, d) @ p['Wo'] + p['bo']
        x = 2 * x + o
        m = _ln(x, p['ln2_g'], p['ln2_b'])
        x = 2 * x + np.maximum(0, m @ p['W1'] + p['b1']) @ p['W2'] + p['b2']
    return _ln(x, params['lnf_g'], params['lnf_b']) @ params['U'] + params['c']
```

- W4 transformer_lm_forward: heads split along the wrong axis (reshape(h, T, w)): **fails T1**.

```python
import numpy as np


def _ln(x, g, b, eps=1e-5, axis=-1):
    mu = x.mean(axis, keepdims=True)
    var = ((x - mu) ** 2).mean(axis, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def transformer_lm_forward(tokens, params, n_blocks, h):
    tokens = np.asarray(tokens)
    T = len(tokens)
    x = params['E'][tokens] + params['P'][:T]
    d = x.shape[-1]
    w = d // h
    mask = np.triu(np.full((T, T), -np.inf), 1)
    for p in params['blocks'][:n_blocks]:
        a = _ln(x, p['ln1_g'], p['ln1_b'])
        q, k, v = ((a @ p[W] + p[b]).reshape(h, T, w) for W, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
        S = q @ k.transpose(0, 2, 1) / np.sqrt(w) + mask
        A = np.exp(S - S.max(-1, keepdims=True))
        A = A / A.sum(-1, keepdims=True)
        o = (A @ v).reshape(T, d) @ p['Wo'] + p['bo']
        x = x + o
        m = _ln(x, p['ln2_g'], p['ln2_b'])
        x = x + np.maximum(0, m @ p['W1'] + p['b1']) @ p['W2'] + p['b2']
    return _ln(x, params['lnf_g'], params['lnf_b']) @ params['U'] + params['c']
```

- W5 transformer_lm_forward: no output bias c: **fails T1**.

```python
import numpy as np


def _ln(x, g, b, eps=1e-5, axis=-1):
    mu = x.mean(axis, keepdims=True)
    var = ((x - mu) ** 2).mean(axis, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def transformer_lm_forward(tokens, params, n_blocks, h):
    tokens = np.asarray(tokens)
    T = len(tokens)
    x = params['E'][tokens] + params['P'][:T]
    d = x.shape[-1]
    w = d // h
    mask = np.triu(np.full((T, T), -np.inf), 1)
    for p in params['blocks'][:n_blocks]:
        a = _ln(x, p['ln1_g'], p['ln1_b'])
        q, k, v = ((a @ p[W] + p[b]).reshape(T, h, w).transpose(1, 0, 2) for W, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
        S = q @ k.transpose(0, 2, 1) / np.sqrt(w) + mask
        A = np.exp(S - S.max(-1, keepdims=True))
        A = A / A.sum(-1, keepdims=True)
        o = (A @ v).transpose(1, 0, 2).reshape(T, d) @ p['Wo'] + p['bo']
        x = x + o
        m = _ln(x, p['ln2_g'], p['ln2_b'])
        x = x + np.maximum(0, m @ p['W1'] + p['b1']) @ p['W2'] + p['b2']
    return _ln(x, params['lnf_g'], params['lnf_b']) @ params['U']
```

- W6 transformer_lm_forward: layer norm without epsilon: **fails T1**.

```python
import numpy as np


def _ln(x, g, b, eps=1e-5, axis=-1):
    mu = x.mean(axis, keepdims=True)
    var = ((x - mu) ** 2).mean(axis, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def transformer_lm_forward(tokens, params, n_blocks, h):
    tokens = np.asarray(tokens)
    T = len(tokens)
    x = params['E'][tokens] + params['P'][:T]
    d = x.shape[-1]
    w = d // h
    mask = np.triu(np.full((T, T), -np.inf), 1)
    for p in params['blocks'][:n_blocks]:
        a = _ln(x, p['ln1_g'], p['ln1_b'], eps=0.0)
        q, k, v = ((a @ p[W] + p[b]).reshape(T, h, w).transpose(1, 0, 2) for W, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
        S = q @ k.transpose(0, 2, 1) / np.sqrt(w) + mask
        A = np.exp(S - S.max(-1, keepdims=True))
        A = A / A.sum(-1, keepdims=True)
        o = (A @ v).transpose(1, 0, 2).reshape(T, d) @ p['Wo'] + p['bo']
        x = x + o
        m = _ln(x, p['ln2_g'], p['ln2_b'], eps=0.0)
        x = x + np.maximum(0, m @ p['W1'] + p['b1']) @ p['W2'] + p['b2']
    return _ln(x, params['lnf_g'], params['lnf_b'], eps=0.0) @ params['U'] + params['c']
```

- W7 transformer_lm_forward: unembedding tied to E.T (U ignored): **fails T1**.

```python
import numpy as np


def _ln(x, g, b, eps=1e-5, axis=-1):
    mu = x.mean(axis, keepdims=True)
    var = ((x - mu) ** 2).mean(axis, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def transformer_lm_forward(tokens, params, n_blocks, h):
    tokens = np.asarray(tokens)
    T = len(tokens)
    x = params['E'][tokens] + params['P'][:T]
    d = x.shape[-1]
    w = d // h
    mask = np.triu(np.full((T, T), -np.inf), 1)
    for p in params['blocks'][:n_blocks]:
        a = _ln(x, p['ln1_g'], p['ln1_b'])
        q, k, v = ((a @ p[W] + p[b]).reshape(T, h, w).transpose(1, 0, 2) for W, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
        S = q @ k.transpose(0, 2, 1) / np.sqrt(w) + mask
        A = np.exp(S - S.max(-1, keepdims=True))
        A = A / A.sum(-1, keepdims=True)
        o = (A @ v).transpose(1, 0, 2).reshape(T, d) @ p['Wo'] + p['bo']
        x = x + o
        m = _ln(x, p['ln2_g'], p['ln2_b'])
        x = x + np.maximum(0, m @ p['W1'] + p['b1']) @ p['W2'] + p['b2']
    return _ln(x, params['lnf_g'], params['lnf_b']) @ params['E'].T + params['c']
```

- W8 transformer_lm_forward: no ReLU in the MLP: **fails T1**.

```python
import numpy as np


def _ln(x, g, b, eps=1e-5, axis=-1):
    mu = x.mean(axis, keepdims=True)
    var = ((x - mu) ** 2).mean(axis, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def transformer_lm_forward(tokens, params, n_blocks, h):
    tokens = np.asarray(tokens)
    T = len(tokens)
    x = params['E'][tokens] + params['P'][:T]
    d = x.shape[-1]
    w = d // h
    mask = np.triu(np.full((T, T), -np.inf), 1)
    for p in params['blocks'][:n_blocks]:
        a = _ln(x, p['ln1_g'], p['ln1_b'])
        q, k, v = ((a @ p[W] + p[b]).reshape(T, h, w).transpose(1, 0, 2) for W, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
        S = q @ k.transpose(0, 2, 1) / np.sqrt(w) + mask
        A = np.exp(S - S.max(-1, keepdims=True))
        A = A / A.sum(-1, keepdims=True)
        o = (A @ v).transpose(1, 0, 2).reshape(T, d) @ p['Wo'] + p['bo']
        x = x + o
        m = _ln(x, p['ln2_g'], p['ln2_b'])
        x = x + (m @ p['W1'] + p['b1']) @ p['W2'] + p['b2']
    return _ln(x, params['lnf_g'], params['lnf_b']) @ params['U'] + params['c']
```

- W9 transformer_lm_forward: no output projection W_O (heads merged straight into the stream, b_O kept): **fails T1**.

```python
import numpy as np


def _ln(x, g, b, eps=1e-5, axis=-1):
    mu = x.mean(axis, keepdims=True)
    var = ((x - mu) ** 2).mean(axis, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def transformer_lm_forward(tokens, params, n_blocks, h):
    tokens = np.asarray(tokens)
    T = len(tokens)
    x = params['E'][tokens] + params['P'][:T]
    d = x.shape[-1]
    w = d // h
    mask = np.triu(np.full((T, T), -np.inf), 1)
    for p in params['blocks'][:n_blocks]:
        a = _ln(x, p['ln1_g'], p['ln1_b'])
        q, k, v = ((a @ p[W] + p[b]).reshape(T, h, w).transpose(1, 0, 2) for W, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
        S = q @ k.transpose(0, 2, 1) / np.sqrt(w) + mask
        A = np.exp(S - S.max(-1, keepdims=True))
        A = A / A.sum(-1, keepdims=True)
        o = (A @ v).transpose(1, 0, 2).reshape(T, d) + p['bo']
        x = x + o
        m = _ln(x, p['ln2_g'], p['ln2_b'])
        x = x + np.maximum(0, m @ p['W1'] + p['b1']) @ p['W2'] + p['b2']
    return _ln(x, params['lnf_g'], params['lnf_b']) @ params['U'] + params['c']
```

