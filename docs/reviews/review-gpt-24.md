# gpt levels 2 to 4 (forward pass, training, scale): second-reader findings

Scope: `app/content/courses/gpt/` l5 to l16, review-2 to -4, homework-2 to -4, problems-2 to -4; `app/content/data/ai/gpt_ops_l2.py`, `gpt_ops_l3.py`; `gpt-w-embed.json`, `gpt-w-block0.json`, `gpt-w2-embed.json`, `gpt-w2-block0.json`, `gpt-w2-block1.json`; at `71ca01d0`. Context read: `docs/briefs/gpt.md` Levels 2 to 4, `docs/reports/gpt-L2.md` to `-L4.md`, `docs/reviews/review-gpt-1.md`, `docs/briefs/ai-strand-interfaces.md`, `docs/AUTHORING.md` section 9.
Method, no browser: (1) modules: central differences in float64 on every array of `gpt_ops_l3.loss_and_grads` for three tiny configurations (one and two blocks, 2 and 4 heads, a repeated token, shorter $T$) and on sampled coordinates of both shipped models; an independent loop forward (positions and heads one at a time) against `gpt_ops_l2.forward_logits` on both shipped models; Adam, `get_batch`, `bigram_loss` and `eval_loss` against hand versions; every widget's imports and `data` map read; SHA-256 of every shipped module; (2) the three number scripts through `run-number-scripts.mjs --only gpt-L` (4 of 4 passed, 89 s) and directly with default threads and `ZQ_NUMBERS_STRICT=1` (293, 251, 194 checks passed), each read for fiat and dead branches; (3) level 4 arithmetic written out separately (`scratchpad/rv24/l4check.py`: counts array by array, 6ND, days and pounds, Kaplan, Chinchilla by golden-section search); (4) `grade-all.mjs --file <f> --code --strict-feedback --local-cdn <pkgs>` on each of the 21 files alone; solution case times against limits through `code-runner.mjs`; 81 own wrong solutions graded by the app's Pyodide runner (appendix); `same-course-reuse.mjs --all`; validator; (5) every stated number recomputed, every distractor read against its `why`, voice scan (`voice-scan.py 35`: 0 and 0) and a spelling and punctuation grep.
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, teaching issue or a test gap that lets a taught bug pass; note = style, script or minor wording.

Counts: 2 errors, 5 warnings, 13 notes. No module error.

## Modules and weights (for `interp` L1 and `post-train` L1)

Verdict: correct; nothing to change in a frozen file.

- Gradients: worst relative error over every array $1.1 \times 10^{-8}$ (two blocks, $h = 10^{-6}$), $2.5 \times 10^{-9}$ and $4.8 \times 10^{-9}$ in the other configurations, $10^{-8}$ and $2.7 \times 10^{-9}$ on the shipped one- and two-block weights; shorter windows the same. The gradient of an embedding row no input uses is exactly 0; a repeated token's row sums its uses.
- Forward: an independent loop forward agrees with `forward_logits` to $3.2 \times 10^{-14}$ (one block) and $1.9 \times 10^{-14}$ (two blocks) on four validation windows and a 5-character input; batched equals single. `loss_and_grads` equals `mean_loss` to $10^{-12}$. Validation 1.793292 (one block) and 1.741290 (two blocks), both over the 781 windows of the last 25,000 characters only; training batches come from the first 225,000 (largest start 224,967), so no window touches validation.
- Weights: 18,017 and 30,721 numbers, every shape as `shapes`, every value float32-exact, every file under 256 KB.
- Adam: `adam_update` equals a hand-written bias-corrected Adam over three steps to $5.6 \times 10^{-12}$. `bigram_loss` equals a pure-Python counter (2.455384).
- Safe order: no widget star-imports `autograd`; no widget imports `softmax` by name. The autograd path is `seq_ops_l4` to `seq_ops_l3.attention` (masked softmax); the NumPy paths use a causal mask whose diagonal is 0, so no fully masked row reaches `seq_ops_l2.softmax`.
- Byte identity: SHA-256 `autograd.py` 5917d4ec91f7, `seq_ops_l3.py` 6187fda66d52 (v1.1), `gpt_ops_l2.py` d6477cfcc475, `gpt_ops_l3.py` e7c2949a22c8, as the reports state. Every widget ships them by path through `data`, and the L2 script asserts byte identity.

- app/content/data/ai/gpt_ops_l3.py | `eval_loss` | note | On data shorter than $T + 1$ characters there are no windows: it returns `nan` with a NumPy warning instead of raising. `interp`'s last 2,000 characters are safe. | Nothing in the frozen file; callers pass at least 33 characters (worth one line in the `interp` and `post-train` briefs).
- app/content/data/ai/gpt_ops_l3.py | `bigram_loss` | note | `V` defaults to 65, while `loss_and_grads`, `train` and `eval_loss` read the vocabulary from `head_w`. A resized vocabulary in `post-train` must pass `V` here. | One line in the `post-train` brief.
- app/content/data/ai/gpt_ops_l2.py | `sample_text`; also l8 screens[4] and homework-2 items[1] solutions | note | Top-$k$ keeps every logit equal to the $k$-th (`z < kth`), so ties keep more than $k$. Harmless on float logits. | None needed; say "ties are kept" if a later course tests ties.
- app/content/data/ai/gpt_ops_l2.py | `forward_cache` | note | It takes no mask argument and uses plain NumPy `_softmax`. An ablation in `interp` must edit cached arrays or call `seq_ops_l3.attention`, which handles a fully masked row. | One line in the `interp` brief.

## Lessons

- app/content/courses/gpt/l14-counting-compute.json | screens[7] option `att` why | error | "Attention adds about 11% at GPT-3's context, not 200%." The 11.1% is GPT-2 small at $T = 1{,}024$ ($T/12d$, screen 5). At GPT-3's context, $T = 2{,}048$ and $d = 12{,}288$, $2LTd$ over $2N$ for the blocks is $2048/147456 = 1.4\%$. | "Attention adds about 1.4% at GPT-3's context, not 200%."
- app/content/courses/gpt/l14-counting-compute.json | screens[0] prose and feedback; screens[4] | warning | "Almost every parameter of a GPT is a matrix weight that each token meets once in the forward pass", then $2N = 36{,}034$ for the tiny GPT. 3,104 of its 18,017 parameters (17%) are `wte` and `wpe` rows, looked up and not multiplied, and l15 quotes Kaplan's law with $N$ the non-embedding parameters. l14 never says which $N$ its $6ND$ uses (14,913 without the tables, $2N = 29{,}826$). | Add after screen 0's first sentence: "Here $N$ counts every parameter. Kaplan et al. leave out the embedding tables, which a token looks up rather than multiplies: 14,913 of the tiny GPT's 18,017."
- app/content/courses/gpt/l10-checking-gradients.json | screens[5] tests | warning | Every test only bounds the returned number ($10^{-13}$ to $10^{-6}$). `return 1e-9` passes all 4 tests, and so does a check of the first array only (appendix, l10 s5 items 3 and 4). The task "for every array" is not enforced. | Add a test whose setup swaps in a `loss_and_grads` that doubles the gradient of `h0.fc_w`, expecting $1/3$ (tol abs $10^{-6}$): `_lg = loss_and_grads; loss_and_grads = lambda w, X, Y, h: (lambda r: (r[0], {**r[1], 'h0.fc_w': 2 * r[1]['h0.fc_w']}))(_lg(w, X, Y, h))`.
- app/content/courses/gpt/l12-beating-the-bigram.json | screens[5] `beats_bigram` | warning | A `beats_bigram` that counts the bigram on train plus validation, the leak this level warns about, passes all 6 tests: the leaked bigram is still above 1.79 (appendix, l12 s5 item 2). | Add a test that records the call: setup `_seen = []; _bv = bigram_val_loss; bigram_val_loss = lambda t, v, a: (_seen.append((len(t), len(v))), _bv(t, v, a))[1]`, call `beats_bigram(W, TRAIN, VAL) and _seen[-1]`, expect `(225000, 25000)`.
- app/content/courses/gpt/l7-next-character.json | screens[6] tests | note | The prose asks for a stable log-softmax; an unshifted one passes all 4 tests, since the model's logits stay below 12. | Add a test on a forward shifted by 1,000, as homework-2 items[1] test 8 does.
- app/content/courses/gpt/l8-generating-text.json | screens[9] code block | note | The summary loop divides by `tau` unconditionally, two screens after the trap that calls that division the bug, while its last line says $\tau = 0$ gives greedy decoding. | `z = forward(W, ids[-T:])[-1]` then `ids.append(argmax(z) if tau == 0 else draw(softmax(top_k(z / tau, k))))`.
- app/content/courses/gpt/l16-a-fixed-budget.json | screens[6] option `paper` why, feedback.correct; review-4 items[9] | note | The lesson reads as if the paper's third approach itself gives about 93 tokens per parameter. As far as I recall the paper (arXiv was not reachable from the sandbox, so check this), its own Approach 3 puts the Gopher-budget optimum near 40B parameters, about 60 tokens per parameter. The 93 comes from the published constants rounded to two figures ($\beta/(\alpha+\beta) = 0.45$ against the paper's 0.46). Besiroglu et al. (2024) found the published fit inconsistent with Approaches 1 and 2, and their re-fit agrees with them. | Add to the feedback: "Rounded to two figures, the constants exaggerate the gap; the paper's own fit gives fewer tokens, and Besiroglu et al. (2024) re-fitted it near 20."

## Review, homework and problems

- app/content/courses/gpt/review-2.json | items[4] question, feedback.correct, option `text` why | error | The item says a square array stored transposed explains a validation loss of 4.17, "about $\ln 65$". It does not. On the 781 validation windows, `wpe` transposed gives 3.41, `h0.proj_w` transposed 3.75 and both 3.83 (`scratchpad/rv24/transpose.py`). A loss at $\ln 65$ means the trained numbers are not in use at all, which l6 screens[9] teaches for the same 4.18. The option `text` why also argues against the key. | Change the stated loss to 3.75. Feedback: "Shapes pass, and the loss is far above 1.79 but below $\ln 65$: a square array in the wrong orientation fits." `text` why: "Unusual words move the loss a little, not from 1.79 to 3.75." Add the 3.75 to `gpt-L2-numbers.py`.
- app/content/courses/gpt/homework-3.json | items[0] `grad_check` tests | warning | As in l10: tests 5 and 6 only bound the value, so `def grad_check(seed): return 1e-9` passes all 7 tests (appendix, homework-3 items[0] item 5). The brief asks for "a gradient check of its own". | Test 5: `grad_check` with the learner's `loss_grads` swapped for one that doubles one array's gradient (setup as in the l10 fix, on `loss_grads`), expecting about $1/3$; or have `grad_check` return `{name: error}` and test its keys and its maximum.
- app/content/courses/gpt/homework-3.json | items[1] tests | note | The non-finite half of the stability rule is untested. Dropping the `math.isfinite` clause passes all 6 tests, because no recorded run holds `nan` or `inf` with a lower last loss. | Plant a run `[4.1, nan, 3.0, ...]` among the rates.
- app/content/courses/gpt/homework-3.json | items[0] prose | note | "For `grad_check`, scale those initial weights by 15 first" is not enforced: unscaled weights pass. | None needed, or drop the rule from the prose.
- app/content/courses/gpt/homework-4.json | items[0] widget.how | note | "its split within a factor of 1.5", but test 7 is `abs(ratio - 1) < 0.5`, which accepts a split from 0.5 to 1.5 times the reference. | "within 50%", or test `1 / 1.5 < r < 1.5`.
- app/content/courses/gpt/problems-2.json | items[2] parts[2] feedback.correct | note | "$1.3804 / \ln 2 \approx 1.9914$": $1.3804 / \ln 2 = 1.99150$. The 1.9914 is the unrounded mean's ($1.380365 / \ln 2 = 1.99145$). The tolerance of 0.0002 accepts both. | "$\approx 1.9915$".

## Every file, `grade-all --strict-feedback`

- 12 of 21 files | `feedback.byKey` | warning | With `--strict-feedback`, which the author's reports omit, 12 files fail: 22 `feedback-missing` and 3 `feedback-unreachable`. A learner whose recorded mistake first fails one of these tests sees only "Check the first failing test". Missing: l6 screens[3] tests 2, 4, 9; l6 screens[7] test 3; l7 screens[6] test 4; l8 screens[4] tests 3, 4; homework-2 items[0] test 1; homework-2 items[1] tests 2, 3, 4; l9 screens[5] test 1; l10 screens[3] test 4; l11 screens[8] tests 3, 4; l12 screens[5] test 1; homework-3 items[1] test 2; l13 screens[5] tests 2, 5; l14 screens[6] test 3; l16 screens[5] tests 1, 4. Unreachable: homework-2 items[0] `test-6`, l10 screens[5] `test-3`, l13 screens[5] `test-4` (its line about the untied head belongs on test 2, which the untied mutant fails first). | Add one byKey line per missing test from its mutant's symptom; move l13's `test-4` text to `test-2`; the l10 fix above makes `test-3` reachable; reword or drop homework-2 `test-6`. Then re-run with `--strict-feedback` (0 failures).

## Number scripts

All three recompute rather than restate, and every figure holds with one BLAS thread (CI runner) and with default threads under `ZQ_NUMBERS_STRICT=1`. L2 builds forward figures three ways (`gpt_ops_l2`, `seq_ops_l4.lm_logits`, a per-position loop) and counts by formula and by summing `shapes`. L3 retrains the shipped weights with its own loop (to $10^{-4}$ of the float32 file; validation equal to $10^{-6}$), checks `gpt_ops_l3.train` against that loop, and counts the bigram twice. L4 has formula against array sum, closed form against a 400,001-point grid, `polyfit` against covariance. Validation figures use the last 25,000 characters only. Every code widget is also replayed in CPython.

- docs/reports/gpt-L2-numbers.py, gpt-L3-numbers.py, gpt-L4-numbers.py | several `two(...)` calls | note | Labelled "two routes agree", these compare an expression with itself or with its own literal. L2: 'l7 hook loss' ($-\ln P_T$ twice), 'validation loss in bits' (`VAL / ln 2` against `VAL * (1 / ln 2)`). L3: 'bigram in bits', 'p1 bits'. L4: 'Chinchilla 6ND' (against the literal 5.88e23), 'r-6nd' (against 2.028). They are unit conversions and products, so nothing false rests on them. | Use `lv.claim` with a plain label, or a real second route (for example `math.log2`).
- docs/reports/gpt-L3-numbers.py | claim 'batch of 16, width 16, 1.99, scale 15' | note | `A and B and C and D or E` parses as `(A and B and C and D) or E`, so the claim passes on its last term alone and its first four conjuncts are dead. | Parenthesise the last two terms.

## Level 4 arithmetic and the papers (no finding beyond those above)

Recomputed separately: GPT-2 small 124,439,808 (block 7,087,872; embeddings 31.6%; MLP 45.5%); untied without head bias 163,037,184; frames 8,943,488, 40,986,240, 450,942,400; tiny tied 15,872; GPT-3 by $12Ld^2$ 173.9B, tied full count 174,604,259,328; "7B" 6.70B; review 236,406,784; problem 1,315,723,264. $6ND$: GPT-3 $3.15 \times 10^{23}$ (the paper's Table D.1 gives $3.14 \times 10^{23}$, which l14 names), Chinchilla $5.88 \times 10^{23}$, tiny GPT $2.767 \times 10^{11}$ (131.8 s at 2.1 GFLOP/s), GPT-2 on 10B tokens $7.47 \times 10^{18}$. GPT-3 on 1,000 GPUs at 312 TFLOP/s and 40%: 29.21 days, £1,051,560. The other workings: Chinchilla days 23.7, review 14.5, problem 10.2 days and £28,201. Kaplan 2.8300, 2.3756, 1.9943, 1.6741, factor 0.8395 per decade, $N$ non-embedding as l15 says. Chinchilla law 1.9366 and 2.0023; at $5.76 \times 10^{23}$, $N = 3.219 \times 10^{10}$, $D = 2.982 \times 10^{12}$, 92.6 tokens per parameter, minimum 1.9307 against 1.9376 at 70B; 92.8 at $5.88 \times 10^{23}$; 50.1 at $10^{21}$ (the ratio drifts, as screen 9 says); tenfold compute gives 2.83 and 3.53. Kaplan's attention term $2 n_\text{layer} n_\text{ctx} d_\text{attn}$, the Gopher budget, 300B tokens for GPT-3, 1.4T for Chinchilla and the comparison with Gopher (4 times fewer parameters, 4.7 times the tokens) match the papers. Memory per precision does not appear before level 5, and no bf16 figure is in scope.

## Margins

Solution case times under the app's runner (node, Pyodide 0.27.7) against the page's limits: the thinnest are l10 screens[5] test 3 (991 ms of 13 s, 13.1x), l12 screens[5] test 1 (16.6x), l11 screens[5] test 2 (17.9x), homework-3 items[0] test 6 (18.9x) and homework-4 items[0] test 2 (37.3x); everything else is above 250x. None is under 3x, though a slow phone may be two or three times slower. Threshold margins: `init_loss` within 0.05 of $\ln 65$ against 0.0023, 0.0113 and 0.0060 (seeds 0, 1, 3; 4.4x at worst); overfit below 0.01 against 0.0015 and 0.0016 (6.3x; under 0.01 from step 40 of 100); gradient bars $10^{-6}$ against $1.5 \times 10^{-9}$ (660x). The homework-3 bar of 3.2 against 2.87 and 2.78 is 1.3x if measured as a share of the fall from 4.17. These runs are seeded and deterministic, and test 1 replays them exactly, so the bar decides nothing.

## Automated checks (no finding)

`same-course-reuse.mjs --all`: no error for any gpt file (one warning on level 1's problems-1, outside scope). Validator: 0 errors. Voice: 0 sentences over 35 words, 0 explanations over three sentences, no em-dash, no exclamation mark, British spellings throughout (`memorise`, `normalise`, `utilisation`, `optimiser`).

## Appendix: reviewer wrong solutions

Each source is the widget's own solution with the edit named. Each was graded by `tools/code-runner.mjs` (the page's harness, the local Pyodide, the page's time limits) through a scratch harness, `scratchpad/rv24/runmut.mjs`. The result is the first hidden test it fails, or SURVIVES. 81 sources: 67 fail a test and 14 survive. Of the survivors, 8 are correct alternatives or harmless probes (marked "equivalent" or "probe") and 6 are real bugs: l7 s6 item 4, l10 s5 items 3 and 4, l12 s5 item 2, homework-3 items[0] item 5, homework-3 items[1] item 2. The brief's list maps as follows. No causal mask, positions after the block, post-norm and a wrongly oriented head are l7 s4 and homework-2 items[0]. The loss over the wrong axis is l7 s6, homework-2 items[0] and l9 s5. Adam without bias correction is l9 s5, l11 s5 and homework-3 items[0]. Overlapping train and validation text is l12 s3 and s5. $6ND$ with the wrong $N$ is homework-4 items[1]. bf16 does not appear in levels 2 to 4, so its analogue, float32 read at 8 bytes, is tried in l6 s3.

### l5-the-whole-model.json screens[8] `param_count` / `shapes`

1. wpe counted as V x d: fails test 1

```python
def param_count(V, T, d, n_layer, mlp):
    block = 4 * d + (d * 3 * d + 3 * d) + (d * d + d) + (d * mlp + mlp) + (mlp * d + d)
    return V * d + V * d + n_layer * block + 2 * d + d * V + V


def shapes(config):
    V, T, d, m = config['V'], config['T'], config['d'], config['mlp']
    out = {'wte': (V, d), 'wpe': (T, d)}
    for i in range(config['n_layer']):
        p = f'h{i}.'
        out.update({p + 'ln1_g': (d,), p + 'ln1_b': (d,), p + 'qkv_w': (d, 3 * d), p + 'qkv_b': (3 * d,),
                    p + 'proj_w': (d, d), p + 'proj_b': (d,), p + 'ln2_g': (d,), p + 'ln2_b': (d,),
                    p + 'fc_w': (d, m), p + 'fc_b': (m,), p + 'out_w': (m, d), p + 'out_b': (d,)})
    out.update({'lnf_g': (d,), 'lnf_b': (d,), 'head_w': (d, V), 'head_b': (V,)})
    return out
```

2. head bias left out: fails test 1

```python
def param_count(V, T, d, n_layer, mlp):
    block = 4 * d + (d * 3 * d + 3 * d) + (d * d + d) + (d * mlp + mlp) + (mlp * d + d)
    return V * d + T * d + n_layer * block + 2 * d + d * V


def shapes(config):
    V, T, d, m = config['V'], config['T'], config['d'], config['mlp']
    out = {'wte': (V, d), 'wpe': (T, d)}
    for i in range(config['n_layer']):
        p = f'h{i}.'
        out.update({p + 'ln1_g': (d,), p + 'ln1_b': (d,), p + 'qkv_w': (d, 3 * d), p + 'qkv_b': (3 * d,),
                    p + 'proj_w': (d, d), p + 'proj_b': (d,), p + 'ln2_g': (d,), p + 'ln2_b': (d,),
                    p + 'fc_w': (d, m), p + 'fc_b': (m,), p + 'out_w': (m, d), p + 'out_b': (d,)})
    out.update({'lnf_g': (d,), 'lnf_b': (d,), 'head_w': (d, V), 'head_b': (V,)})
    return out
```

3. shapes: head transposed (V, d): fails test 10

```python
def param_count(V, T, d, n_layer, mlp):
    block = 4 * d + (d * 3 * d + 3 * d) + (d * d + d) + (d * mlp + mlp) + (mlp * d + d)
    return V * d + T * d + n_layer * block + 2 * d + d * V + V


def shapes(config):
    V, T, d, m = config['V'], config['T'], config['d'], config['mlp']
    out = {'wte': (V, d), 'wpe': (T, d)}
    for i in range(config['n_layer']):
        p = f'h{i}.'
        out.update({p + 'ln1_g': (d,), p + 'ln1_b': (d,), p + 'qkv_w': (d, 3 * d), p + 'qkv_b': (3 * d,),
                    p + 'proj_w': (d, d), p + 'proj_b': (d,), p + 'ln2_g': (d,), p + 'ln2_b': (d,),
                    p + 'fc_w': (d, m), p + 'fc_b': (m,), p + 'out_w': (m, d), p + 'out_b': (d,)})
    out.update({'lnf_g': (d,), 'lnf_b': (d,), 'head_w': (V, d), 'head_b': (V,)})
    return out
```


### l6-loading-weights.json screens[3] `load_weights` / `check_shapes`

1. float32 read as 8 bytes (float64), the bytes-per-number slip: fails test 1

```python
import base64
import json

import numpy as np


def load_weights(json_text):
    out = {}
    for name, entry in json.loads(json_text).items():
        raw = np.frombuffer(base64.b64decode(entry['b64']), dtype='<f8')
        out[name] = raw.reshape(entry['shape']).astype(np.float64)
    return out


def check_shapes(weights, config):
    bad = []
    for name, shape in expected_shapes(config).items():
        if name not in weights or tuple(weights[name].shape) != tuple(shape):
            bad.append(name)
    return sorted(bad)
```

2. reshape to the reversed shape then transpose (square arrays hide it): fails test 2

```python
import base64
import json

import numpy as np


def load_weights(json_text):
    out = {}
    for name, entry in json.loads(json_text).items():
        raw = np.frombuffer(base64.b64decode(entry['b64']), dtype='<f4')
        out[name] = raw.reshape(entry['shape'][::-1]).T.astype(np.float64)
    return out


def check_shapes(weights, config):
    bad = []
    for name, shape in expected_shapes(config).items():
        if name not in weights or tuple(weights[name].shape) != tuple(shape):
            bad.append(name)
    return sorted(bad)
```

3. check_shapes compares sizes only: fails test 8

```python
import base64
import json

import numpy as np


def load_weights(json_text):
    out = {}
    for name, entry in json.loads(json_text).items():
        raw = np.frombuffer(base64.b64decode(entry['b64']), dtype='<f4')
        out[name] = raw.reshape(entry['shape']).astype(np.float64)
    return out


def check_shapes(weights, config):
    bad = []
    for name, shape in expected_shapes(config).items():
        if name not in weights or weights[name].size != int(np.prod(shape)):
            bad.append(name)
    return sorted(bad)
```

4. check_shapes returns names unsorted: fails test 10

```python
import base64
import json

import numpy as np


def load_weights(json_text):
    out = {}
    for name, entry in json.loads(json_text).items():
        raw = np.frombuffer(base64.b64decode(entry['b64']), dtype='<f4')
        out[name] = raw.reshape(entry['shape']).astype(np.float64)
    return out


def check_shapes(weights, config):
    bad = []
    for name, shape in expected_shapes(config).items():
        if name not in weights or tuple(weights[name].shape) != tuple(shape):
            bad.append(name)
    return bad[::-1]
```


### l6-loading-weights.json screens[7] `init_loss`

1. biases drawn at random too: fails test 2

```python
import numpy as np


def init_loss(seed):
    rng = np.random.default_rng(seed)
    w = {}
    for name, shape in expected_shapes(CFG).items():
        if name.endswith('_g'):
            w[name] = np.ones(shape)
        else:
            w[name] = rng.standard_normal(shape) * 0.02
    return model_loss(w, XB, YB)
```

2. scale 0.2 instead of 0.02: fails test 1

```python
import numpy as np


def init_loss(seed):
    rng = np.random.default_rng(seed)
    w = {}
    for name, shape in expected_shapes(CFG).items():
        if name.endswith('_g'):
            w[name] = np.ones(shape)
        elif len(shape) == 1:
            w[name] = np.zeros(shape)
        else:
            w[name] = rng.standard_normal(shape) * 0.2
    return model_loss(w, XB, YB)
```


### l7-next-character.json screens[4] `causal_mask` / `forward`

1. no causal mask: fails test 2

```python
import numpy as np


def causal_mask(T):
    return np.triu(np.full((T, T), -np.inf), 1)


def layer_norm(x, g, b, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def softmax(s):
    e = np.exp(s - s.max(-1, keepdims=True))
    return e / e.sum(-1, keepdims=True)


def forward(weights, idx):
    idx = np.asarray(idx)
    T = idx.shape[-1]
    x = weights['wte'][idx] + weights['wpe'][:T]
    a = layer_norm(x, weights['h0.ln1_g'], weights['h0.ln1_b'])
    qkv = a @ weights['h0.qkv_w'] + weights['h0.qkv_b']
    heads = []
    for j in range(3):
        part = qkv[..., j * 32:(j + 1) * 32].reshape(*idx.shape, 4, 8)
        heads.append(np.swapaxes(part, -2, -3))
    q, k, v = heads
    att = softmax(q @ np.swapaxes(k, -1, -2) / np.sqrt(8))
    z = np.swapaxes(att @ v, -2, -3).reshape(*idx.shape, 32)
    x = x + z @ weights['h0.proj_w'] + weights['h0.proj_b']
    a2 = layer_norm(x, weights['h0.ln2_g'], weights['h0.ln2_b'])
    x = x + np.maximum(a2 @ weights['h0.fc_w'] + weights['h0.fc_b'], 0) @ weights['h0.out_w'] + weights['h0.out_b']
    return layer_norm(x, weights['lnf_g'], weights['lnf_b']) @ weights['head_w'] + weights['head_b']
```

2. position embeddings added after the block: fails test 2

```python
import numpy as np


def causal_mask(T):
    return np.triu(np.full((T, T), -np.inf), 1)


def layer_norm(x, g, b, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def softmax(s):
    e = np.exp(s - s.max(-1, keepdims=True))
    return e / e.sum(-1, keepdims=True)


def forward(weights, idx):
    idx = np.asarray(idx)
    T = idx.shape[-1]
    x = weights['wte'][idx]
    a = layer_norm(x, weights['h0.ln1_g'], weights['h0.ln1_b'])
    qkv = a @ weights['h0.qkv_w'] + weights['h0.qkv_b']
    heads = []
    for j in range(3):
        part = qkv[..., j * 32:(j + 1) * 32].reshape(*idx.shape, 4, 8)
        heads.append(np.swapaxes(part, -2, -3))
    q, k, v = heads
    att = softmax(q @ np.swapaxes(k, -1, -2) / np.sqrt(8) + causal_mask(T))
    z = np.swapaxes(att @ v, -2, -3).reshape(*idx.shape, 32)
    x = x + z @ weights['h0.proj_w'] + weights['h0.proj_b']
    a2 = layer_norm(x, weights['h0.ln2_g'], weights['h0.ln2_b'])
    x = x + np.maximum(a2 @ weights['h0.fc_w'] + weights['h0.fc_b'], 0) @ weights['h0.out_w'] + weights['h0.out_b']
    x = x + weights['wpe'][:T]
    return layer_norm(x, weights['lnf_g'], weights['lnf_b']) @ weights['head_w'] + weights['head_b']
```

3. post-norm: layer norm after each residual add: fails test 2

```python
import numpy as np


def causal_mask(T):
    return np.triu(np.full((T, T), -np.inf), 1)


def layer_norm(x, g, b, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def softmax(s):
    e = np.exp(s - s.max(-1, keepdims=True))
    return e / e.sum(-1, keepdims=True)


def forward(weights, idx):
    idx = np.asarray(idx)
    T = idx.shape[-1]
    x = weights['wte'][idx] + weights['wpe'][:T]
    a = x
    qkv = a @ weights['h0.qkv_w'] + weights['h0.qkv_b']
    heads = []
    for j in range(3):
        part = qkv[..., j * 32:(j + 1) * 32].reshape(*idx.shape, 4, 8)
        heads.append(np.swapaxes(part, -2, -3))
    q, k, v = heads
    att = softmax(q @ np.swapaxes(k, -1, -2) / np.sqrt(8) + causal_mask(T))
    z = np.swapaxes(att @ v, -2, -3).reshape(*idx.shape, 32)
    x = layer_norm(x + z @ weights['h0.proj_w'] + weights['h0.proj_b'], weights['h0.ln1_g'], weights['h0.ln1_b'])
    a2 = x
    x = layer_norm(x + np.maximum(a2 @ weights['h0.fc_w'] + weights['h0.fc_b'], 0) @ weights['h0.out_w'] + weights['h0.out_b'], weights['h0.ln2_g'], weights['h0.ln2_b'])
    return layer_norm(x, weights['lnf_g'], weights['lnf_b']) @ weights['head_w'] + weights['head_b']
```

4. head tied to wte (wte.T) instead of head_w: fails test 2

```python
import numpy as np


def causal_mask(T):
    return np.triu(np.full((T, T), -np.inf), 1)


def layer_norm(x, g, b, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def softmax(s):
    e = np.exp(s - s.max(-1, keepdims=True))
    return e / e.sum(-1, keepdims=True)


def forward(weights, idx):
    idx = np.asarray(idx)
    T = idx.shape[-1]
    x = weights['wte'][idx] + weights['wpe'][:T]
    a = layer_norm(x, weights['h0.ln1_g'], weights['h0.ln1_b'])
    qkv = a @ weights['h0.qkv_w'] + weights['h0.qkv_b']
    heads = []
    for j in range(3):
        part = qkv[..., j * 32:(j + 1) * 32].reshape(*idx.shape, 4, 8)
        heads.append(np.swapaxes(part, -2, -3))
    q, k, v = heads
    att = softmax(q @ np.swapaxes(k, -1, -2) / np.sqrt(8) + causal_mask(T))
    z = np.swapaxes(att @ v, -2, -3).reshape(*idx.shape, 32)
    x = x + z @ weights['h0.proj_w'] + weights['h0.proj_b']
    a2 = layer_norm(x, weights['h0.ln2_g'], weights['h0.ln2_b'])
    x = x + np.maximum(a2 @ weights['h0.fc_w'] + weights['h0.fc_b'], 0) @ weights['h0.out_w'] + weights['h0.out_b']
    return layer_norm(x, weights['lnf_g'], weights['lnf_b']) @ weights['wte'].T + weights['head_b']
```

5. head bytes in the wrong order: head_w.reshape(65, 32).T: fails test 2

```python
import numpy as np


def causal_mask(T):
    return np.triu(np.full((T, T), -np.inf), 1)


def layer_norm(x, g, b, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def softmax(s):
    e = np.exp(s - s.max(-1, keepdims=True))
    return e / e.sum(-1, keepdims=True)


def forward(weights, idx):
    idx = np.asarray(idx)
    T = idx.shape[-1]
    x = weights['wte'][idx] + weights['wpe'][:T]
    a = layer_norm(x, weights['h0.ln1_g'], weights['h0.ln1_b'])
    qkv = a @ weights['h0.qkv_w'] + weights['h0.qkv_b']
    heads = []
    for j in range(3):
        part = qkv[..., j * 32:(j + 1) * 32].reshape(*idx.shape, 4, 8)
        heads.append(np.swapaxes(part, -2, -3))
    q, k, v = heads
    att = softmax(q @ np.swapaxes(k, -1, -2) / np.sqrt(8) + causal_mask(T))
    z = np.swapaxes(att @ v, -2, -3).reshape(*idx.shape, 32)
    x = x + z @ weights['h0.proj_w'] + weights['h0.proj_b']
    a2 = layer_norm(x, weights['h0.ln2_g'], weights['h0.ln2_b'])
    x = x + np.maximum(a2 @ weights['h0.fc_w'] + weights['h0.fc_b'], 0) @ weights['h0.out_w'] + weights['h0.out_b']
    return layer_norm(x, weights['lnf_g'], weights['lnf_b']) @ weights['head_w'].reshape(65, 32).T + weights['head_b']
```

6. heads interleaved: reshape (.., 8, 4) then swap: fails test 2

```python
import numpy as np


def causal_mask(T):
    return np.triu(np.full((T, T), -np.inf), 1)


def layer_norm(x, g, b, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def softmax(s):
    e = np.exp(s - s.max(-1, keepdims=True))
    return e / e.sum(-1, keepdims=True)


def forward(weights, idx):
    idx = np.asarray(idx)
    T = idx.shape[-1]
    x = weights['wte'][idx] + weights['wpe'][:T]
    a = layer_norm(x, weights['h0.ln1_g'], weights['h0.ln1_b'])
    qkv = a @ weights['h0.qkv_w'] + weights['h0.qkv_b']
    heads = []
    for j in range(3):
        part = np.swapaxes(qkv[..., j * 32:(j + 1) * 32].reshape(*idx.shape, 8, 4), -1, -2)
        heads.append(np.swapaxes(part, -2, -3))
    q, k, v = heads
    att = softmax(q @ np.swapaxes(k, -1, -2) / np.sqrt(8) + causal_mask(T))
    z = np.swapaxes(att @ v, -2, -3).reshape(*idx.shape, 32)
    x = x + z @ weights['h0.proj_w'] + weights['h0.proj_b']
    a2 = layer_norm(x, weights['h0.ln2_g'], weights['h0.ln2_b'])
    x = x + np.maximum(a2 @ weights['h0.fc_w'] + weights['h0.fc_b'], 0) @ weights['h0.out_w'] + weights['h0.out_b']
    return layer_norm(x, weights['lnf_g'], weights['lnf_b']) @ weights['head_w'] + weights['head_b']
```

7. layer norm with the n - 1 variance: fails test 2

```python
import numpy as np


def causal_mask(T):
    return np.triu(np.full((T, T), -np.inf), 1)


def layer_norm(x, g, b, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).sum(-1, keepdims=True) / (x.shape[-1] - 1)
    return g * (x - mu) / np.sqrt(var + eps) + b


def softmax(s):
    e = np.exp(s - s.max(-1, keepdims=True))
    return e / e.sum(-1, keepdims=True)


def forward(weights, idx):
    idx = np.asarray(idx)
    T = idx.shape[-1]
    x = weights['wte'][idx] + weights['wpe'][:T]
    a = layer_norm(x, weights['h0.ln1_g'], weights['h0.ln1_b'])
    qkv = a @ weights['h0.qkv_w'] + weights['h0.qkv_b']
    heads = []
    for j in range(3):
        part = qkv[..., j * 32:(j + 1) * 32].reshape(*idx.shape, 4, 8)
        heads.append(np.swapaxes(part, -2, -3))
    q, k, v = heads
    att = softmax(q @ np.swapaxes(k, -1, -2) / np.sqrt(8) + causal_mask(T))
    z = np.swapaxes(att @ v, -2, -3).reshape(*idx.shape, 32)
    x = x + z @ weights['h0.proj_w'] + weights['h0.proj_b']
    a2 = layer_norm(x, weights['h0.ln2_g'], weights['h0.ln2_b'])
    x = x + np.maximum(a2 @ weights['h0.fc_w'] + weights['h0.fc_b'], 0) @ weights['h0.out_w'] + weights['h0.out_b']
    return layer_norm(x, weights['lnf_g'], weights['lnf_b']) @ weights['head_w'] + weights['head_b']
```

8. layer norm epsilon 1e-6 instead of 1e-5: fails test 2

```python
import numpy as np


def causal_mask(T):
    return np.triu(np.full((T, T), -np.inf), 1)


def layer_norm(x, g, b, eps=1e-6):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def softmax(s):
    e = np.exp(s - s.max(-1, keepdims=True))
    return e / e.sum(-1, keepdims=True)


def forward(weights, idx):
    idx = np.asarray(idx)
    T = idx.shape[-1]
    x = weights['wte'][idx] + weights['wpe'][:T]
    a = layer_norm(x, weights['h0.ln1_g'], weights['h0.ln1_b'])
    qkv = a @ weights['h0.qkv_w'] + weights['h0.qkv_b']
    heads = []
    for j in range(3):
        part = qkv[..., j * 32:(j + 1) * 32].reshape(*idx.shape, 4, 8)
        heads.append(np.swapaxes(part, -2, -3))
    q, k, v = heads
    att = softmax(q @ np.swapaxes(k, -1, -2) / np.sqrt(8) + causal_mask(T))
    z = np.swapaxes(att @ v, -2, -3).reshape(*idx.shape, 32)
    x = x + z @ weights['h0.proj_w'] + weights['h0.proj_b']
    a2 = layer_norm(x, weights['h0.ln2_g'], weights['h0.ln2_b'])
    x = x + np.maximum(a2 @ weights['h0.fc_w'] + weights['h0.fc_b'], 0) @ weights['h0.out_w'] + weights['h0.out_b']
    return layer_norm(x, weights['lnf_g'], weights['lnf_b']) @ weights['head_w'] + weights['head_b']
```

9. mask on the diagonal too (strict): fails test 1

```python
import numpy as np


def causal_mask(T):
    return np.triu(np.full((T, T), -np.inf), 0)


def layer_norm(x, g, b, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def softmax(s):
    e = np.exp(s - s.max(-1, keepdims=True))
    return e / e.sum(-1, keepdims=True)


def forward(weights, idx):
    idx = np.asarray(idx)
    T = idx.shape[-1]
    x = weights['wte'][idx] + weights['wpe'][:T]
    a = layer_norm(x, weights['h0.ln1_g'], weights['h0.ln1_b'])
    qkv = a @ weights['h0.qkv_w'] + weights['h0.qkv_b']
    heads = []
    for j in range(3):
        part = qkv[..., j * 32:(j + 1) * 32].reshape(*idx.shape, 4, 8)
        heads.append(np.swapaxes(part, -2, -3))
    q, k, v = heads
    att = softmax(q @ np.swapaxes(k, -1, -2) / np.sqrt(8) + causal_mask(T))
    z = np.swapaxes(att @ v, -2, -3).reshape(*idx.shape, 32)
    x = x + z @ weights['h0.proj_w'] + weights['h0.proj_b']
    a2 = layer_norm(x, weights['h0.ln2_g'], weights['h0.ln2_b'])
    x = x + np.maximum(a2 @ weights['h0.fc_w'] + weights['h0.fc_b'], 0) @ weights['h0.out_w'] + weights['h0.out_b']
    return layer_norm(x, weights['lnf_g'], weights['lnf_b']) @ weights['head_w'] + weights['head_b']
```


### l7-next-character.json screens[6] `loss`

1. loss averaged over the vocabulary axis (mean of all log-probabilities): fails test 1

```python
import numpy as np


def loss(weights, idx, targets):
    z = forward(weights, idx)
    z = z - z.max(-1, keepdims=True)
    logp = z - np.log(np.exp(z).sum(-1, keepdims=True))
    targets = np.asarray(targets)
    return float(-logp.mean())
```

2. sum over positions, mean over windows: fails test 1

```python
import numpy as np


def loss(weights, idx, targets):
    z = forward(weights, idx)
    z = z - z.max(-1, keepdims=True)
    logp = z - np.log(np.exp(z).sum(-1, keepdims=True))
    targets = np.asarray(targets)
    return float(-np.take_along_axis(logp, targets[..., None], -1)[..., 0].sum(-1).mean())
```

3. divides by 32 positions whatever T is: fails test 3

```python
import numpy as np


def loss(weights, idx, targets):
    z = forward(weights, idx)
    z = z - z.max(-1, keepdims=True)
    logp = z - np.log(np.exp(z).sum(-1, keepdims=True))
    targets = np.asarray(targets)
    return float(-np.take_along_axis(logp, targets[..., None], -1).sum() / (targets.size // targets.shape[-1] * 32))
```

4. no max subtraction (unstable log-softmax): **SURVIVES**

```python
import numpy as np


def loss(weights, idx, targets):
    z = forward(weights, idx)
    logp = z - np.log(np.exp(z).sum(-1, keepdims=True))
    targets = np.asarray(targets)
    return float(-np.take_along_axis(logp, targets[..., None], -1).mean())
```


### l8-generating-text.json screens[4] `sample_next`

1. top-k keeps k - 1 (<= instead of <): fails test 4

```python
import numpy as np


def sample_next(logits, temperature, top_k, rng):
    z = np.asarray(logits, dtype=float)
    if temperature == 0:
        return int(np.argmax(z))
    z = z / temperature
    if top_k is not None:
        kth = np.sort(z)[-top_k]
        z = np.where(z <= kth, -np.inf, z)
    p = np.exp(z - z.max())
    p = p / p.sum()
    return int(rng.choice(len(z), p=p))
```

2. global np.random instead of rng: fails test 2

```python
import numpy as np


def sample_next(logits, temperature, top_k, rng):
    z = np.asarray(logits, dtype=float)
    if temperature == 0:
        return int(np.argmax(z))
    z = z / temperature
    if top_k is not None:
        kth = np.sort(z)[-top_k]
        z = np.where(z < kth, -np.inf, z)
    p = np.exp(z - z.max())
    p = p / p.sum()
    return int(np.random.choice(len(z), p=p))
```

3. temperature applied as a power of the chances, renormalised (equivalent): **SURVIVES**

```python
import numpy as np


def sample_next(logits, temperature, top_k, rng):
    z = np.asarray(logits, dtype=float)
    if temperature == 0:
        return int(np.argmax(z))
    if top_k is not None:
        kth = np.sort(z)[-top_k]
        z = np.where(z < kth, -np.inf, z)
    p = np.exp(z - z.max())
    p = p ** (1 / temperature)
    p = p / p.sum()
    return int(rng.choice(len(z), p=p))
```


### l8-generating-text.json screens[6] `generate`

1. window of the last 31 ids: fails test 5

```python
import numpy as np


def generate(weights, prompt, n, temperature, seed):
    rng = np.random.default_rng(seed)
    ids = encode(prompt)
    for _ in range(n):
        logits = forward(weights, np.array(ids[-31:]))[-1]
        ids.append(sample_next(logits, temperature, None, rng))
    return decode(ids)
```

2. window from the start of the text, not the end: fails test 3

```python
import numpy as np


def generate(weights, prompt, n, temperature, seed):
    rng = np.random.default_rng(seed)
    ids = encode(prompt)
    for _ in range(n):
        logits = forward(weights, np.array(ids[:32]))[-1]
        ids.append(sample_next(logits, temperature, None, rng))
    return decode(ids)
```

3. top-k of 5 always: fails test 1

```python
import numpy as np


def generate(weights, prompt, n, temperature, seed):
    rng = np.random.default_rng(seed)
    ids = encode(prompt)
    for _ in range(n):
        logits = forward(weights, np.array(ids[-32:]))[-1]
        ids.append(sample_next(logits, temperature, 5, rng))
    return decode(ids)
```


### homework-2.json items[0] `gpt_loss`

1. no causal mask: fails test 1

```python
import numpy as np


def layer_norm(x, g, b):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + 1e-5) + b


def gpt_loss(weights, text):
    ids = np.array([VOCAB.index(c) for c in text])
    x_ids, y = ids[:-1], ids[1:]
    T = len(x_ids)
    x = weights['wte'][x_ids] + weights['wpe'][:T]
    a = layer_norm(x, weights['h0.ln1_g'], weights['h0.ln1_b'])
    qkv = a @ weights['h0.qkv_w'] + weights['h0.qkv_b']
    q, k, v = [qkv[:, j * 32:(j + 1) * 32].reshape(T, 4, 8).transpose(1, 0, 2) for j in range(3)]
    s = q @ k.transpose(0, 2, 1) / np.sqrt(8)
    att = np.exp(s - s.max(-1, keepdims=True))
    att = att / att.sum(-1, keepdims=True)
    z = (att @ v).transpose(1, 0, 2).reshape(T, 32)
    x = x + z @ weights['h0.proj_w'] + weights['h0.proj_b']
    h = np.maximum(layer_norm(x, weights['h0.ln2_g'], weights['h0.ln2_b']) @ weights['h0.fc_w'] + weights['h0.fc_b'], 0)
    x = x + h @ weights['h0.out_w'] + weights['h0.out_b']
    logits = layer_norm(x, weights['lnf_g'], weights['lnf_b']) @ weights['head_w'] + weights['head_b']
    logits = logits - logits.max(-1, keepdims=True)
    logp = logits - np.log(np.exp(logits).sum(-1, keepdims=True))
    return float(-logp[np.arange(T), y].mean())
```

2. position embeddings added after the block: fails test 1

```python
import numpy as np


def layer_norm(x, g, b):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + 1e-5) + b


def gpt_loss(weights, text):
    ids = np.array([VOCAB.index(c) for c in text])
    x_ids, y = ids[:-1], ids[1:]
    T = len(x_ids)
    x = weights['wte'][x_ids]
    a = layer_norm(x, weights['h0.ln1_g'], weights['h0.ln1_b'])
    qkv = a @ weights['h0.qkv_w'] + weights['h0.qkv_b']
    q, k, v = [qkv[:, j * 32:(j + 1) * 32].reshape(T, 4, 8).transpose(1, 0, 2) for j in range(3)]
    s = q @ k.transpose(0, 2, 1) / np.sqrt(8) + np.triu(np.full((T, T), -np.inf), 1)
    att = np.exp(s - s.max(-1, keepdims=True))
    att = att / att.sum(-1, keepdims=True)
    z = (att @ v).transpose(1, 0, 2).reshape(T, 32)
    x = x + z @ weights['h0.proj_w'] + weights['h0.proj_b']
    h = np.maximum(layer_norm(x, weights['h0.ln2_g'], weights['h0.ln2_b']) @ weights['h0.fc_w'] + weights['h0.fc_b'], 0)
    x = x + h @ weights['h0.out_w'] + weights['h0.out_b']
    x = x + weights['wpe'][:T]
    logits = layer_norm(x, weights['lnf_g'], weights['lnf_b']) @ weights['head_w'] + weights['head_b']
    logits = logits - logits.max(-1, keepdims=True)
    logp = logits - np.log(np.exp(logits).sum(-1, keepdims=True))
    return float(-logp[np.arange(T), y].mean())
```

3. post-norm: fails test 1

```python
import numpy as np


def layer_norm(x, g, b):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + 1e-5) + b


def gpt_loss(weights, text):
    ids = np.array([VOCAB.index(c) for c in text])
    x_ids, y = ids[:-1], ids[1:]
    T = len(x_ids)
    x = weights['wte'][x_ids] + weights['wpe'][:T]
    a = x
    qkv = a @ weights['h0.qkv_w'] + weights['h0.qkv_b']
    q, k, v = [qkv[:, j * 32:(j + 1) * 32].reshape(T, 4, 8).transpose(1, 0, 2) for j in range(3)]
    s = q @ k.transpose(0, 2, 1) / np.sqrt(8) + np.triu(np.full((T, T), -np.inf), 1)
    att = np.exp(s - s.max(-1, keepdims=True))
    att = att / att.sum(-1, keepdims=True)
    z = (att @ v).transpose(1, 0, 2).reshape(T, 32)
    x = layer_norm(x + z @ weights['h0.proj_w'] + weights['h0.proj_b'], weights['h0.ln1_g'], weights['h0.ln1_b'])
    h = np.maximum(x @ weights['h0.fc_w'] + weights['h0.fc_b'], 0)
    x = layer_norm(x + h @ weights['h0.out_w'] + weights['h0.out_b'], weights['h0.ln2_g'], weights['h0.ln2_b'])
    logits = layer_norm(x, weights['lnf_g'], weights['lnf_b']) @ weights['head_w'] + weights['head_b']
    logits = logits - logits.max(-1, keepdims=True)
    logp = logits - np.log(np.exp(logits).sum(-1, keepdims=True))
    return float(-logp[np.arange(T), y].mean())
```

4. head tied to wte (wte.T): fails test 1

```python
import numpy as np


def layer_norm(x, g, b):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + 1e-5) + b


def gpt_loss(weights, text):
    ids = np.array([VOCAB.index(c) for c in text])
    x_ids, y = ids[:-1], ids[1:]
    T = len(x_ids)
    x = weights['wte'][x_ids] + weights['wpe'][:T]
    a = layer_norm(x, weights['h0.ln1_g'], weights['h0.ln1_b'])
    qkv = a @ weights['h0.qkv_w'] + weights['h0.qkv_b']
    q, k, v = [qkv[:, j * 32:(j + 1) * 32].reshape(T, 4, 8).transpose(1, 0, 2) for j in range(3)]
    s = q @ k.transpose(0, 2, 1) / np.sqrt(8) + np.triu(np.full((T, T), -np.inf), 1)
    att = np.exp(s - s.max(-1, keepdims=True))
    att = att / att.sum(-1, keepdims=True)
    z = (att @ v).transpose(1, 0, 2).reshape(T, 32)
    x = x + z @ weights['h0.proj_w'] + weights['h0.proj_b']
    h = np.maximum(layer_norm(x, weights['h0.ln2_g'], weights['h0.ln2_b']) @ weights['h0.fc_w'] + weights['h0.fc_b'], 0)
    x = x + h @ weights['h0.out_w'] + weights['h0.out_b']
    logits = layer_norm(x, weights['lnf_g'], weights['lnf_b']) @ weights['wte'].T + weights['head_b']
    logits = logits - logits.max(-1, keepdims=True)
    logp = logits - np.log(np.exp(logits).sum(-1, keepdims=True))
    return float(-logp[np.arange(T), y].mean())
```

5. loss summed over positions: fails test 1

```python
import numpy as np


def layer_norm(x, g, b):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + 1e-5) + b


def gpt_loss(weights, text):
    ids = np.array([VOCAB.index(c) for c in text])
    x_ids, y = ids[:-1], ids[1:]
    T = len(x_ids)
    x = weights['wte'][x_ids] + weights['wpe'][:T]
    a = layer_norm(x, weights['h0.ln1_g'], weights['h0.ln1_b'])
    qkv = a @ weights['h0.qkv_w'] + weights['h0.qkv_b']
    q, k, v = [qkv[:, j * 32:(j + 1) * 32].reshape(T, 4, 8).transpose(1, 0, 2) for j in range(3)]
    s = q @ k.transpose(0, 2, 1) / np.sqrt(8) + np.triu(np.full((T, T), -np.inf), 1)
    att = np.exp(s - s.max(-1, keepdims=True))
    att = att / att.sum(-1, keepdims=True)
    z = (att @ v).transpose(1, 0, 2).reshape(T, 32)
    x = x + z @ weights['h0.proj_w'] + weights['h0.proj_b']
    h = np.maximum(layer_norm(x, weights['h0.ln2_g'], weights['h0.ln2_b']) @ weights['h0.fc_w'] + weights['h0.fc_b'], 0)
    x = x + h @ weights['h0.out_w'] + weights['h0.out_b']
    logits = layer_norm(x, weights['lnf_g'], weights['lnf_b']) @ weights['head_w'] + weights['head_b']
    logits = logits - logits.max(-1, keepdims=True)
    logp = logits - np.log(np.exp(logits).sum(-1, keepdims=True))
    return float(-logp[np.arange(T), y].sum())
```

6. loss averaged over the vocabulary axis: fails test 1

```python
import numpy as np


def layer_norm(x, g, b):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + 1e-5) + b


def gpt_loss(weights, text):
    ids = np.array([VOCAB.index(c) for c in text])
    x_ids, y = ids[:-1], ids[1:]
    T = len(x_ids)
    x = weights['wte'][x_ids] + weights['wpe'][:T]
    a = layer_norm(x, weights['h0.ln1_g'], weights['h0.ln1_b'])
    qkv = a @ weights['h0.qkv_w'] + weights['h0.qkv_b']
    q, k, v = [qkv[:, j * 32:(j + 1) * 32].reshape(T, 4, 8).transpose(1, 0, 2) for j in range(3)]
    s = q @ k.transpose(0, 2, 1) / np.sqrt(8) + np.triu(np.full((T, T), -np.inf), 1)
    att = np.exp(s - s.max(-1, keepdims=True))
    att = att / att.sum(-1, keepdims=True)
    z = (att @ v).transpose(1, 0, 2).reshape(T, 32)
    x = x + z @ weights['h0.proj_w'] + weights['h0.proj_b']
    h = np.maximum(layer_norm(x, weights['h0.ln2_g'], weights['h0.ln2_b']) @ weights['h0.fc_w'] + weights['h0.fc_b'], 0)
    x = x + h @ weights['h0.out_w'] + weights['h0.out_b']
    logits = layer_norm(x, weights['lnf_g'], weights['lnf_b']) @ weights['head_w'] + weights['head_b']
    logits = logits - logits.max(-1, keepdims=True)
    logp = logits - np.log(np.exp(logits).sum(-1, keepdims=True))
    return float(-logp.mean())
```

7. final layer norm left out: fails test 1

```python
import numpy as np


def layer_norm(x, g, b):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + 1e-5) + b


def gpt_loss(weights, text):
    ids = np.array([VOCAB.index(c) for c in text])
    x_ids, y = ids[:-1], ids[1:]
    T = len(x_ids)
    x = weights['wte'][x_ids] + weights['wpe'][:T]
    a = layer_norm(x, weights['h0.ln1_g'], weights['h0.ln1_b'])
    qkv = a @ weights['h0.qkv_w'] + weights['h0.qkv_b']
    q, k, v = [qkv[:, j * 32:(j + 1) * 32].reshape(T, 4, 8).transpose(1, 0, 2) for j in range(3)]
    s = q @ k.transpose(0, 2, 1) / np.sqrt(8) + np.triu(np.full((T, T), -np.inf), 1)
    att = np.exp(s - s.max(-1, keepdims=True))
    att = att / att.sum(-1, keepdims=True)
    z = (att @ v).transpose(1, 0, 2).reshape(T, 32)
    x = x + z @ weights['h0.proj_w'] + weights['h0.proj_b']
    h = np.maximum(layer_norm(x, weights['h0.ln2_g'], weights['h0.ln2_b']) @ weights['h0.fc_w'] + weights['h0.fc_b'], 0)
    x = x + h @ weights['h0.out_w'] + weights['h0.out_b']
    logits = x @ weights['head_w'] + weights['head_b']
    logits = logits - logits.max(-1, keepdims=True)
    logp = logits - np.log(np.exp(logits).sum(-1, keepdims=True))
    return float(-logp[np.arange(T), y].mean())
```


### homework-2.json items[1] `topk_probs`

1. top-k keeps k - 1 (<=): fails test 3

```python
import numpy as np


def topk_probs(logits, temperature, k):
    z = np.asarray(logits, dtype=float)
    if temperature == 0:
        p = np.zeros(len(z))
        p[np.argmax(z)] = 1.0
        return p
    z = z / temperature
    if k is not None:
        z = np.where(z <= np.sort(z)[-k], -np.inf, z)
    e = np.exp(z - z.max())
    return e / e.sum()
```

2. temperature 0 as a tiny temperature (1e-9) (equivalent: one-hot except on exact ties): **SURVIVES**

```python
import numpy as np


def topk_probs(logits, temperature, k):
    z = np.asarray(logits, dtype=float)
    if temperature == 0:
        temperature = 1e-9
    z = z / temperature
    if k is not None:
        z = np.where(z < np.sort(z)[-k], -np.inf, z)
    e = np.exp(z - z.max())
    return e / e.sum()
```


### l9-the-training-loop.json screens[3] `get_batch`

1. starts drawn below len - T - 1 (never the last valid start): fails test 1

```python
import numpy as np


def get_batch(data, B, T, rng):
    data = np.asarray(data)
    starts = rng.integers(0, len(data) - T - 1, B)
    X = np.stack([data[i:i + T] for i in starts])
    Y = np.stack([data[i + 1:i + T + 1] for i in starts])
    return X, Y
```

2. targets equal to the inputs: fails test 2

```python
import numpy as np


def get_batch(data, B, T, rng):
    data = np.asarray(data)
    starts = rng.integers(0, len(data) - T, B)
    X = np.stack([data[i:i + T] for i in starts])
    Y = np.stack([data[i:i + T] for i in starts])
    return X, Y
```


### l9-the-training-loop.json screens[5] `train_step`

1. Adam without bias correction: fails test 2

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step
from seq_ops_l4 import lm_logits
from gpt_ops_l2 import to_model


def train_step(params, opt_state, batch, lr):
    X, Y = batch
    names = list(params)
    for k in names:
        params[k].zero_grad()
    logits = lm_logits(X, to_model(params), 4)
    loss = cross_entropy(logits.reshape(-1, 65), Y.reshape(-1))
    loss.backward()
    opt_state['t'] += 1
    m = [opt_state['m'].get(k, np.zeros_like(params[k].data)) for k in names]
    v = [opt_state['v'].get(k, np.zeros_like(params[k].data)) for k in names]
    g = [params[k].grad for k in names]
    m = [0.9 * a + 0.1 * b for a, b in zip(m, g)]
    v = [0.999 * a + 0.001 * b * b for a, b in zip(v, g)]
    new = [params[k].data - lr * mi / (np.sqrt(vi) + 1e-8) for k, mi, vi in zip(names, m, v)]
    for k, a, mi, vi in zip(names, new, m, v):
        params[k].data = a
        opt_state['m'][k], opt_state['v'][k] = mi, vi
    return loss.item()
```

2. loss averaged over the wrong axis (per-window sums, then mean): fails test 1

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step
from seq_ops_l4 import lm_logits
from gpt_ops_l2 import to_model


def train_step(params, opt_state, batch, lr):
    X, Y = batch
    names = list(params)
    for k in names:
        params[k].zero_grad()
    logits = lm_logits(X, to_model(params), 4)
    loss = cross_entropy(logits.reshape(-1, 65), Y.reshape(-1)) * Y.shape[-1]
    loss.backward()
    opt_state['t'] += 1
    m = [opt_state['m'].get(k, np.zeros_like(params[k].data)) for k in names]
    v = [opt_state['v'].get(k, np.zeros_like(params[k].data)) for k in names]
    new, m, v = adam_step([params[k].data for k in names], [params[k].grad for k in names], m, v, opt_state['t'], lr)
    for k, a, mi, vi in zip(names, new, m, v):
        params[k].data = a
        opt_state['m'][k], opt_state['v'][k] = mi, vi
    return loss.item()
```


### l10-checking-gradients.json screens[3] `numeric_grad` / `rel_error`

1. rel_error divided by the larger norm: fails test 4

```python
import numpy as np


def numeric_grad(f, x, h):
    g = np.zeros_like(x, dtype=float)
    for i in np.ndindex(x.shape):
        keep = x[i]
        x[i] = keep + h
        up = f()
        x[i] = keep - h
        down = f()
        x[i] = keep
        g[i] = (up - down) / (2 * h)
    return g


def rel_error(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    scale = max(np.linalg.norm(a), np.linalg.norm(b))
    if scale == 0:
        return 0.0
    return float(np.linalg.norm(a - b) / scale)
```

2. rel_error as a max absolute difference: fails test 6

```python
import numpy as np


def numeric_grad(f, x, h):
    g = np.zeros_like(x, dtype=float)
    for i in np.ndindex(x.shape):
        keep = x[i]
        x[i] = keep + h
        up = f()
        x[i] = keep - h
        down = f()
        x[i] = keep
        g[i] = (up - down) / (2 * h)
    return g


def rel_error(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    scale = np.linalg.norm(a) + np.linalg.norm(b)
    if scale == 0:
        return 0.0
    return float(np.abs(a - b).max() / scale)
```


### l10-checking-gradients.json screens[5] `check_model`

1. h = 1e-11: fails test 1

```python
import numpy as np
from gpt_ops_l2 import mean_loss
from gpt_ops_l3 import init_weights, loss_and_grads


def check_model(config, seed):
    w = init_weights(seed, config, sd=0.3)
    nh = config['n_head']
    _, grads = loss_and_grads(w, XT, YT, nh)
    worst = 0.0
    for name in w:
        num = numeric_grad(lambda: mean_loss(w, XT, YT, nh), w[name], 1e-11)
        worst = max(worst, rel_error(grads[name], num))
    return worst
```

2. weights at the default scale 0.02 (not a bug; probe): **SURVIVES**

```python
import numpy as np
from gpt_ops_l2 import mean_loss
from gpt_ops_l3 import init_weights, loss_and_grads


def check_model(config, seed):
    w = init_weights(seed, config)
    nh = config['n_head']
    _, grads = loss_and_grads(w, XT, YT, nh)
    worst = 0.0
    for name in w:
        num = numeric_grad(lambda: mean_loss(w, XT, YT, nh), w[name], 1e-5)
        worst = max(worst, rel_error(grads[name], num))
    return worst
```

3. checks only the first array: **SURVIVES**

```python
import numpy as np
from gpt_ops_l2 import mean_loss
from gpt_ops_l3 import init_weights, loss_and_grads


def check_model(config, seed):
    w = init_weights(seed, config, sd=0.3)
    nh = config['n_head']
    _, grads = loss_and_grads(w, XT, YT, nh)
    worst = 0.0
    for name in list(w)[:1]:
        num = numeric_grad(lambda: mean_loss(w, XT, YT, nh), w[name], 1e-5)
        worst = max(worst, rel_error(grads[name], num))
    return worst
```

4. returns a constant 1e-9 (no check at all): **SURVIVES**

```python
def check_model(config, seed):
    return 1e-9
```


### l11-short-runs.json screens[5] `overfit_one_batch`

1. Adam without bias correction (own update): fails test 1

```python
import numpy as np
from gpt_ops_l3 import init_weights, loss_and_grads, adam_init, adam_update


def overfit_one_batch(steps, lr, seed):
    w = init_weights(seed)
    state = adam_init(w)
    losses = []
    for _ in range(steps):
        loss, grads = loss_and_grads(w, XO, YO)
        for k in w:
            state['m'][k] = 0.9 * state['m'][k] + 0.1 * grads[k]
            state['v'][k] = 0.999 * state['v'][k] + 0.001 * grads[k] ** 2
        w = {k: w[k] - lr * state['m'][k] / (np.sqrt(state['v'][k]) + 1e-8) for k in w}
        losses.append(loss)
    return losses
```

2. returns the losses after each update: fails test 1

```python
import numpy as np
from gpt_ops_l3 import init_weights, loss_and_grads, adam_init, adam_update


def overfit_one_batch(steps, lr, seed):
    w = init_weights(seed)
    state = adam_init(w)
    losses = []
    for _ in range(steps):
        loss, grads = loss_and_grads(w, XO, YO)
        w = adam_update(w, grads, state, lr)
        losses.append(loss_and_grads(w, XO, YO)[0])
    return losses
```


### l11-short-runs.json screens[8] `diagnose`

1. slow threshold 0.9 instead of 0.98: fails test 7

```python
import math


def diagnose(losses):
    first = losses[0]
    if any(not math.isfinite(x) for x in losses) or max(losses) > 1.1 * first:
        return 'diverging'
    if all(abs(x - first) < 1e-12 for x in losses):
        return 'stuck'
    if losses[-1] > 0.9 * first:
        return 'slow'
    return 'healthy'
```

2. checks slow before stuck (equivalent once stuck is excluded): **SURVIVES**

```python
import math


def diagnose(losses):
    first = losses[0]
    if any(not math.isfinite(x) for x in losses) or max(losses) > 1.1 * first:
        return 'diverging'
    if losses[-1] > 0.98 * first and losses[-1] != first:
        return 'slow'
    if all(abs(x - first) < 1e-12 for x in losses):
        return 'stuck'
    return 'healthy'
```

3. slow tested before stuck: fails test 4

```python
import math


def diagnose(losses):
    first = losses[0]
    if any(not math.isfinite(x) for x in losses) or max(losses) > 1.1 * first:
        return 'diverging'
    if losses[-1] > 0.98 * first:
        return 'slow'
    if all(abs(x - first) < 1e-12 for x in losses):
        return 'stuck'
    return 'healthy'
```


### l12-beating-the-bigram.json screens[3] `bigram_val_loss`

1. train and validation text overlapping (counts include val): fails test 1

```python
import numpy as np


def bigram_val_loss(train, val, alpha):
    train, val = np.asarray(train), np.asarray(val)
    counts = np.zeros((65, 65))
    both = np.concatenate([train, val])
    np.add.at(counts, (both[:-1], both[1:]), 1)
    probs = (counts + alpha) / (counts + alpha).sum(axis=1, keepdims=True)
    return float(-np.log(probs[val[:-1], val[1:]]).mean())
```

2. alpha only in the numerator: fails test 1

```python
import numpy as np


def bigram_val_loss(train, val, alpha):
    train, val = np.asarray(train), np.asarray(val)
    counts = np.zeros((65, 65))
    np.add.at(counts, (train[:-1], train[1:]), 1)
    probs = (counts + alpha) / (counts.sum(axis=1, keepdims=True) + 1e-300)
    return float(-np.log(probs[val[:-1], val[1:]]).mean())
```

3. pair across the train/val boundary counted (train + first val char): fails test 1

```python
import numpy as np


def bigram_val_loss(train, val, alpha):
    train, val = np.asarray(train), np.asarray(val)
    counts = np.zeros((65, 65))
    ext = np.concatenate([train, val[:1]])
    np.add.at(counts, (ext[:-1], ext[1:]), 1)
    probs = (counts + alpha) / (counts + alpha).sum(axis=1, keepdims=True)
    return float(-np.log(probs[val[:-1], val[1:]]).mean())
```


### l12-beating-the-bigram.json screens[5] `gpt_val_loss` / `beats_bigram`

1. overlapping windows (stride 16): fails test 1

```python
import numpy as np


def gpt_val_loss(weights, val):
    val = np.asarray(val)
    n = (len(val) - 1) // 32
    st = range(0, len(val) - 32, 16)
    X = np.stack([val[i:i + 32] for i in st])
    Y = np.stack([val[i + 1:i + 33] for i in st])
    return mean_loss(weights, X, Y)


def beats_bigram(weights, train, val):
    return bool(gpt_val_loss(weights, val) < bigram_val_loss(train, val, 1.0))
```

2. beats_bigram against the bigram counted on train + val: **SURVIVES**

```python
import numpy as np


def gpt_val_loss(weights, val):
    val = np.asarray(val)
    n = (len(val) - 1) // 32
    X = val[:n * 32].reshape(n, 32)
    Y = val[1:n * 32 + 1].reshape(n, 32)
    return mean_loss(weights, X, Y)


def beats_bigram(weights, train, val):
    return bool(gpt_val_loss(weights, val) < bigram_val_loss(np.concatenate([np.asarray(train), np.asarray(val)]), val, 1.0))
```


### homework-3.json items[0] `train` / `grad_check`

1. Adam without bias correction: fails test 1

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step
from seq_ops_l4 import lm_logits
from gpt_ops_l2 import shapes, to_model, mean_loss


def init(config, seed):
    rng = np.random.default_rng(seed)
    w = {}
    for name, shape in shapes(config):
        if name.endswith('_g'):
            w[name] = np.ones(shape)
        elif len(shape) == 1:
            w[name] = np.zeros(shape)
        else:
            w[name] = rng.standard_normal(shape) * 0.02
    return w


def loss_grads(w, X, Y, heads):
    P = {k: Tensor(v) for k, v in w.items()}
    V = w['head_w'].shape[1]
    loss = cross_entropy(lm_logits(X, to_model(P), heads).reshape(-1, V), Y.reshape(-1))
    loss.backward()
    return loss.item(), {k: P[k].grad for k in w}


def train(steps, lr, seed):
    w = init(SMALL, seed)
    names = list(w)
    m = [np.zeros_like(w[k]) for k in names]
    v = [np.zeros_like(w[k]) for k in names]
    rng = np.random.default_rng(seed + 1)
    losses = []
    for t in range(1, steps + 1):
        starts = rng.integers(0, len(TRAIN) - 16, 8)
        X = np.stack([TRAIN[i:i + 16] for i in starts])
        Y = np.stack([TRAIN[i + 1:i + 17] for i in starts])
        loss, g = loss_grads(w, X, Y, 2)
        m = [0.9 * a + 0.1 * g[k] for a, k in zip(m, names)]
        v = [0.999 * a + 0.001 * g[k] ** 2 for a, k in zip(v, names)]
        new = [w[k] - lr * mi / (np.sqrt(vi) + 1e-8) for k, mi, vi in zip(names, m, v)]
        w = dict(zip(names, new))
        losses.append(loss)
    return w, losses


def grad_check(seed):
    w = init(TINY, seed)
    for k in w:
        w[k] = w[k] * 15
    _, g = loss_grads(w, XT, YT, 2)
    worst = 0.0
    for k in w:
        num = np.zeros_like(w[k])
        for i in np.ndindex(w[k].shape):
            keep = w[k][i]
            w[k][i] = keep + 1e-5
            up = mean_loss(w, XT, YT, 2)
            w[k][i] = keep - 1e-5
            down = mean_loss(w, XT, YT, 2)
            w[k][i] = keep
            num[i] = (up - down) / 2e-5
        d = np.linalg.norm(g[k]) + np.linalg.norm(num)
        worst = max(worst, 0.0 if d == 0 else float(np.linalg.norm(g[k] - num) / d))
    return worst
```

2. grad_check without the scale of 15 (probe): **SURVIVES**

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step
from seq_ops_l4 import lm_logits
from gpt_ops_l2 import shapes, to_model, mean_loss


def init(config, seed):
    rng = np.random.default_rng(seed)
    w = {}
    for name, shape in shapes(config):
        if name.endswith('_g'):
            w[name] = np.ones(shape)
        elif len(shape) == 1:
            w[name] = np.zeros(shape)
        else:
            w[name] = rng.standard_normal(shape) * 0.02
    return w


def loss_grads(w, X, Y, heads):
    P = {k: Tensor(v) for k, v in w.items()}
    V = w['head_w'].shape[1]
    loss = cross_entropy(lm_logits(X, to_model(P), heads).reshape(-1, V), Y.reshape(-1))
    loss.backward()
    return loss.item(), {k: P[k].grad for k in w}


def train(steps, lr, seed):
    w = init(SMALL, seed)
    names = list(w)
    m = [np.zeros_like(w[k]) for k in names]
    v = [np.zeros_like(w[k]) for k in names]
    rng = np.random.default_rng(seed + 1)
    losses = []
    for t in range(1, steps + 1):
        starts = rng.integers(0, len(TRAIN) - 16, 8)
        X = np.stack([TRAIN[i:i + 16] for i in starts])
        Y = np.stack([TRAIN[i + 1:i + 17] for i in starts])
        loss, g = loss_grads(w, X, Y, 2)
        new, m, v = adam_step([w[k] for k in names], [g[k] for k in names], m, v, t, lr)
        w = dict(zip(names, new))
        losses.append(loss)
    return w, losses


def grad_check(seed):
    w = init(TINY, seed)
    for k in w:
        pass
    _, g = loss_grads(w, XT, YT, 2)
    worst = 0.0
    for k in w:
        num = np.zeros_like(w[k])
        for i in np.ndindex(w[k].shape):
            keep = w[k][i]
            w[k][i] = keep + 1e-5
            up = mean_loss(w, XT, YT, 2)
            w[k][i] = keep - 1e-5
            down = mean_loss(w, XT, YT, 2)
            w[k][i] = keep
            num[i] = (up - down) / 2e-5
        d = np.linalg.norm(g[k]) + np.linalg.norm(num)
        worst = max(worst, 0.0 if d == 0 else float(np.linalg.norm(g[k] - num) / d))
    return worst
```

3. grad_check with h = 1e-11: fails test 5

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step
from seq_ops_l4 import lm_logits
from gpt_ops_l2 import shapes, to_model, mean_loss


def init(config, seed):
    rng = np.random.default_rng(seed)
    w = {}
    for name, shape in shapes(config):
        if name.endswith('_g'):
            w[name] = np.ones(shape)
        elif len(shape) == 1:
            w[name] = np.zeros(shape)
        else:
            w[name] = rng.standard_normal(shape) * 0.02
    return w


def loss_grads(w, X, Y, heads):
    P = {k: Tensor(v) for k, v in w.items()}
    V = w['head_w'].shape[1]
    loss = cross_entropy(lm_logits(X, to_model(P), heads).reshape(-1, V), Y.reshape(-1))
    loss.backward()
    return loss.item(), {k: P[k].grad for k in w}


def train(steps, lr, seed):
    w = init(SMALL, seed)
    names = list(w)
    m = [np.zeros_like(w[k]) for k in names]
    v = [np.zeros_like(w[k]) for k in names]
    rng = np.random.default_rng(seed + 1)
    losses = []
    for t in range(1, steps + 1):
        starts = rng.integers(0, len(TRAIN) - 16, 8)
        X = np.stack([TRAIN[i:i + 16] for i in starts])
        Y = np.stack([TRAIN[i + 1:i + 17] for i in starts])
        loss, g = loss_grads(w, X, Y, 2)
        new, m, v = adam_step([w[k] for k in names], [g[k] for k in names], m, v, t, lr)
        w = dict(zip(names, new))
        losses.append(loss)
    return w, losses


def grad_check(seed):
    w = init(TINY, seed)
    for k in w:
        w[k] = w[k] * 15
    _, g = loss_grads(w, XT, YT, 2)
    worst = 0.0
    for k in w:
        num = np.zeros_like(w[k])
        for i in np.ndindex(w[k].shape):
            keep = w[k][i]
            w[k][i] = keep + 1e-11
            up = mean_loss(w, XT, YT, 2)
            w[k][i] = keep - 1e-11
            down = mean_loss(w, XT, YT, 2)
            w[k][i] = keep
            num[i] = (up - down) / 2e-11
        d = np.linalg.norm(g[k]) + np.linalg.norm(num)
        worst = max(worst, 0.0 if d == 0 else float(np.linalg.norm(g[k] - num) / d))
    return worst
```

4. batches from the init generator (one rng): fails test 1

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step
from seq_ops_l4 import lm_logits
from gpt_ops_l2 import shapes, to_model, mean_loss


def init(config, seed):
    rng = np.random.default_rng(seed)
    w = {}
    for name, shape in shapes(config):
        if name.endswith('_g'):
            w[name] = np.ones(shape)
        elif len(shape) == 1:
            w[name] = np.zeros(shape)
        else:
            w[name] = rng.standard_normal(shape) * 0.02
    return w


def loss_grads(w, X, Y, heads):
    P = {k: Tensor(v) for k, v in w.items()}
    V = w['head_w'].shape[1]
    loss = cross_entropy(lm_logits(X, to_model(P), heads).reshape(-1, V), Y.reshape(-1))
    loss.backward()
    return loss.item(), {k: P[k].grad for k in w}


def train(steps, lr, seed):
    w = init(SMALL, seed)
    names = list(w)
    m = [np.zeros_like(w[k]) for k in names]
    v = [np.zeros_like(w[k]) for k in names]
    rng = np.random.default_rng(seed)
    losses = []
    for t in range(1, steps + 1):
        starts = rng.integers(0, len(TRAIN) - 16, 8)
        X = np.stack([TRAIN[i:i + 16] for i in starts])
        Y = np.stack([TRAIN[i + 1:i + 17] for i in starts])
        loss, g = loss_grads(w, X, Y, 2)
        new, m, v = adam_step([w[k] for k in names], [g[k] for k in names], m, v, t, lr)
        w = dict(zip(names, new))
        losses.append(loss)
    return w, losses


def grad_check(seed):
    w = init(TINY, seed)
    for k in w:
        w[k] = w[k] * 15
    _, g = loss_grads(w, XT, YT, 2)
    worst = 0.0
    for k in w:
        num = np.zeros_like(w[k])
        for i in np.ndindex(w[k].shape):
            keep = w[k][i]
            w[k][i] = keep + 1e-5
            up = mean_loss(w, XT, YT, 2)
            w[k][i] = keep - 1e-5
            down = mean_loss(w, XT, YT, 2)
            w[k][i] = keep
            num[i] = (up - down) / 2e-5
        d = np.linalg.norm(g[k]) + np.linalg.norm(num)
        worst = max(worst, 0.0 if d == 0 else float(np.linalg.norm(g[k] - num) / d))
    return worst
```

5. grad_check returns a constant 1e-9: **SURVIVES**

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step
from seq_ops_l4 import lm_logits
from gpt_ops_l2 import shapes, to_model, mean_loss


def init(config, seed):
    rng = np.random.default_rng(seed)
    w = {}
    for name, shape in shapes(config):
        if name.endswith('_g'):
            w[name] = np.ones(shape)
        elif len(shape) == 1:
            w[name] = np.zeros(shape)
        else:
            w[name] = rng.standard_normal(shape) * 0.02
    return w


def loss_grads(w, X, Y, heads):
    P = {k: Tensor(v) for k, v in w.items()}
    V = w['head_w'].shape[1]
    loss = cross_entropy(lm_logits(X, to_model(P), heads).reshape(-1, V), Y.reshape(-1))
    loss.backward()
    return loss.item(), {k: P[k].grad for k in w}


def train(steps, lr, seed):
    w = init(SMALL, seed)
    names = list(w)
    m = [np.zeros_like(w[k]) for k in names]
    v = [np.zeros_like(w[k]) for k in names]
    rng = np.random.default_rng(seed + 1)
    losses = []
    for t in range(1, steps + 1):
        starts = rng.integers(0, len(TRAIN) - 16, 8)
        X = np.stack([TRAIN[i:i + 16] for i in starts])
        Y = np.stack([TRAIN[i + 1:i + 17] for i in starts])
        loss, g = loss_grads(w, X, Y, 2)
        new, m, v = adam_step([w[k] for k in names], [g[k] for k in names], m, v, t, lr)
        w = dict(zip(names, new))
        losses.append(loss)
    return w, losses


def grad_check(seed):
    return 1e-9
```


### homework-3.json items[1] `find_lr`

1. stability judged by the last loss only: fails test 3

```python
import math


def find_lr(rates):
    best, best_loss = None, math.inf
    for lr in rates:
        losses = short_run(lr)
        first = losses[0]
        if any(not math.isfinite(x) for x in losses) or losses[-1] > 1.1 * first:
            continue
        if losses[-1] < best_loss:
            best, best_loss = lr, losses[-1]
    return best
```

2. non-finite runs not skipped: **SURVIVES**

```python
import math


def find_lr(rates):
    best, best_loss = None, math.inf
    for lr in rates:
        losses = short_run(lr)
        first = losses[0]
        if max(losses) > 1.1 * first:
            continue
        if losses[-1] < best_loss:
            best, best_loss = lr, losses[-1]
    return best
```


### l13-counting-parameters.json screens[5] `gpt_params`

1. tied head keeps its bias: fails test 1

```python
def gpt_params(V, T, d, L, mlp_ratio, tied):
    m = mlp_ratio * d
    block = 4 * d + (3 * d * d + 3 * d) + (d * d + d) + (d * m + m) + (m * d + d)
    n = V * d + T * d + L * block + 2 * d
    n += V
    if not tied:
        n += d * V
    return n
```

2. untied adds the bias only (vocabulary counted once): fails test 2

```python
def gpt_params(V, T, d, L, mlp_ratio, tied):
    m = mlp_ratio * d
    block = 4 * d + (3 * d * d + 3 * d) + (d * d + d) + (d * m + m) + (m * d + d)
    n = V * d + T * d + L * block + 2 * d
    if not tied:
        n += V
    return n
```

3. final layer norm left out: fails test 1

```python
def gpt_params(V, T, d, L, mlp_ratio, tied):
    m = mlp_ratio * d
    block = 4 * d + (3 * d * d + 3 * d) + (d * d + d) + (d * m + m) + (m * d + d)
    n = V * d + T * d + L * block
    if not tied:
        n += d * V + V
    return n
```


### l14-counting-compute.json screens[6] `train_flops` / `attention_flops` / `days_to_train`

1. utilisation multiplied into the FLOPs: fails test 4

```python
def train_flops(N, D):
    return 6 * N * D


def attention_flops(L, T, d):
    return 2 * L * T * d


def days_to_train(flops, flops_per_s, utilisation):
    return flops * utilisation / flops_per_s / 86400
```

2. attention term of training (6LTd): fails test 3

```python
def train_flops(N, D):
    return 6 * N * D


def attention_flops(L, T, d):
    return 6 * L * T * d


def days_to_train(flops, flops_per_s, utilisation):
    return flops / (flops_per_s * utilisation) / 86400
```


### l15-power-laws.json screens[5] `fit_power_law` / `predict_loss`

1. log10 fit, e^intercept: fails test 1

```python
import numpy as np


def fit_power_law(N, L):
    x, y = np.log10(np.asarray(N, dtype=float)), np.log10(np.asarray(L, dtype=float))
    slope = np.cov(x, y, bias=True)[0, 1] / np.var(x)
    intercept = y.mean() - slope * x.mean()
    return float(np.exp(intercept)), float(-slope)


def predict_loss(a, alpha, N):
    return a * np.asarray(N, dtype=float) ** (-alpha)
```

2. np.var with ddof=1 against cov with bias: fails test 1

```python
import numpy as np


def fit_power_law(N, L):
    x, y = np.log(np.asarray(N, dtype=float)), np.log(np.asarray(L, dtype=float))
    slope = np.cov(x, y, bias=True)[0, 1] / np.var(x, ddof=1)
    intercept = y.mean() - slope * x.mean()
    return float(np.exp(intercept)), float(-slope)


def predict_loss(a, alpha, N):
    return a * np.asarray(N, dtype=float) ** (-alpha)
```

3. log10 fit, 10^intercept (equivalent): **SURVIVES**

```python
import numpy as np


def fit_power_law(N, L):
    x, y = np.log10(np.asarray(N, dtype=float)), np.log10(np.asarray(L, dtype=float))
    slope = np.cov(x, y, bias=True)[0, 1] / np.var(x)
    intercept = y.mean() - slope * x.mean()
    return float(10 ** intercept), float(-slope)


def predict_loss(a, alpha, N):
    return a * np.asarray(N, dtype=float) ** (-alpha)
```


### l16-a-fixed-budget.json screens[5] `chinchilla_loss` / `optimal_split`

1. grid over D instead of N (equivalent): **SURVIVES**

```python
import numpy as np


def chinchilla_loss(N, D):
    return 1.69 + 406.4 / np.asarray(N, dtype=float) ** 0.34 + 410.7 / np.asarray(D, dtype=float) ** 0.28


def optimal_split(C):
    Ds = np.logspace(6, 16, 200001)
    losses = chinchilla_loss(C / (6 * Ds), Ds)
    N = float(C / (6 * Ds[np.argmin(losses)]))
    return N, C / (6 * N)
```

2. grid of 2,001 points: fails test 5

```python
import numpy as np


def chinchilla_loss(N, D):
    return 1.69 + 406.4 / np.asarray(N, dtype=float) ** 0.34 + 410.7 / np.asarray(D, dtype=float) ** 0.28


def optimal_split(C):
    Ns = np.logspace(6, 14, 2001)
    losses = chinchilla_loss(Ns, C / (6 * Ns))
    N = float(Ns[np.argmin(losses)])
    return N, C / (6 * N)
```

3. E left out: fails test 1

```python
import numpy as np


def chinchilla_loss(N, D):
    return 406.4 / np.asarray(N, dtype=float) ** 0.34 + 410.7 / np.asarray(D, dtype=float) ** 0.28


def optimal_split(C):
    Ns = np.logspace(6, 14, 200001)
    losses = chinchilla_loss(Ns, C / (6 * Ns))
    N = float(Ns[np.argmin(losses)])
    return N, C / (6 * N)
```


### homework-4.json items[0] `fit_scaling` / `best_split`

1. grid stops at 0.59 (harmless: the planted exponents are below 0.59; the prose says 0.60): **SURVIVES**

```python
import numpy as np


def fit_scaling(runs):
    runs = np.asarray(runs, dtype=float)
    N, D, L = runs[:, 0], runs[:, 1], runs[:, 2]
    best = None
    for alpha in np.round(np.arange(0.10, 0.595, 0.01), 2):
        for beta in np.round(np.arange(0.10, 0.595, 0.01), 2):
            X = np.column_stack([np.ones_like(N), N ** -alpha, D ** -beta])
            coef = np.linalg.lstsq(X, L, rcond=None)[0]
            sse = float(((X @ coef - L) ** 2).sum())
            if best is None or sse < best[0]:
                best = (sse, coef, alpha, beta)
    _, (E, A, B), alpha, beta = best
    return {'E': float(E), 'A': float(A), 'B': float(B), 'alpha': float(alpha), 'beta': float(beta)}


def best_split(p, C):
    a, b = p['alpha'], p['beta']
    G = (a * p['A'] / (b * p['B'])) ** (1 / (a + b))
    N = G * (C / 6) ** (b / (a + b))
    return float(N), float(C / (6 * N))
```

2. best_split with D from 2N: fails test 4

```python
import numpy as np


def fit_scaling(runs):
    runs = np.asarray(runs, dtype=float)
    N, D, L = runs[:, 0], runs[:, 1], runs[:, 2]
    best = None
    for alpha in np.round(np.arange(0.10, 0.601, 0.01), 2):
        for beta in np.round(np.arange(0.10, 0.601, 0.01), 2):
            X = np.column_stack([np.ones_like(N), N ** -alpha, D ** -beta])
            coef = np.linalg.lstsq(X, L, rcond=None)[0]
            sse = float(((X @ coef - L) ** 2).sum())
            if best is None or sse < best[0]:
                best = (sse, coef, alpha, beta)
    _, (E, A, B), alpha, beta = best
    return {'E': float(E), 'A': float(A), 'B': float(B), 'alpha': float(alpha), 'beta': float(beta)}


def best_split(p, C):
    a, b = p['alpha'], p['beta']
    G = (a * p['A'] / (b * p['B'])) ** (1 / (a + b))
    N = G * (C / 6) ** (b / (a + b))
    return float(N), float(C / (2 * N))
```

3. best_split ignores the budget factor 6 (C instead of C/6): fails test 4

```python
import numpy as np


def fit_scaling(runs):
    runs = np.asarray(runs, dtype=float)
    N, D, L = runs[:, 0], runs[:, 1], runs[:, 2]
    best = None
    for alpha in np.round(np.arange(0.10, 0.601, 0.01), 2):
        for beta in np.round(np.arange(0.10, 0.601, 0.01), 2):
            X = np.column_stack([np.ones_like(N), N ** -alpha, D ** -beta])
            coef = np.linalg.lstsq(X, L, rcond=None)[0]
            sse = float(((X @ coef - L) ** 2).sum())
            if best is None or sse < best[0]:
                best = (sse, coef, alpha, beta)
    _, (E, A, B), alpha, beta = best
    return {'E': float(E), 'A': float(A), 'B': float(B), 'alpha': float(alpha), 'beta': float(beta)}


def best_split(p, C):
    a, b = p['alpha'], p['beta']
    G = (a * p['A'] / (b * p['B'])) ** (1 / (a + b))
    N = G * C ** (b / (a + b))
    return float(N), float(C / (6 * N))
```


### homework-4.json items[1] `config_costs`

1. 6ND with N excluding the embeddings: fails test 1

```python
def config_costs(V, T, d, L, tokens):
    m = 4 * d
    block = 4 * d + 3 * d * d + 3 * d + d * d + d + 2 * d * m + m + d
    n = V * d + T * d + L * block + 2 * d
    return {'params': n, 'flops': 6 * (n - V * d - T * d) * tokens}
```

2. params excluding the position table: fails test 1

```python
def config_costs(V, T, d, L, tokens):
    m = 4 * d
    block = 4 * d + 3 * d * d + 3 * d + d * d + d + 2 * d * m + m + d
    n = V * d + L * block + 2 * d
    return {'params': n, 'flops': 6 * n * tokens}
```

3. MLP width d (ratio 1): fails test 1

```python
def config_costs(V, T, d, L, tokens):
    m = d
    block = 4 * d + 3 * d * d + 3 * d + d * d + d + 2 * d * m + m + d
    n = V * d + T * d + L * block + 2 * d
    return {'params': n, 'flops': 6 * n * tokens}
```
