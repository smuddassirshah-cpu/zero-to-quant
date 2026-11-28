# sequence level 4 (The transformer block): author report

Branch `ai-w6-sequence` (from `06e60d8a`, with `56293ddb` merged for `seq_ops_l3.py` v1.1). Skill `sqn-block` on every file.

## Files

| File | Screens or items | Code widgets (mutants) |
|---|---|---|
| `l13-the-block.json` | 11 screens, quiz 4 | `mlp_block` (3), `transformer_block` (4), `block_grad_check` (3) |
| `l14-residual-stream.json` | 11 screens, quiz 4 | `stream_trace` + `update_norms` (4), `ablate_sublayer` (3) |
| `l15-counting-a-block.json` | 11 screens, quiz 4 | `block_params` + `model_params` + `count_arrays` (5) |
| `l16-a-tiny-transformer.json` | 11 screens, quiz 4 | `tiny_forward` (4), `reverse_with` + `heldout_accuracy` (3), `train_reverser` (4) |
| `review-4.json` | 8 items, `pass` 0.8 | none |
| `homework-4.json` | 8 items (one `order` with a distractor, one `longform`, two `code`) | `is_per_position` (4), `transformer_lm_forward` performance task (6) |
| `problems-4.json` | 4 chained items, 17 parts, one at difficulty 5 | none |
| `app/content/data/ai/seq_ops_l4.py` | new module, 6,133 bytes, SHA-256 `9e0a855c2d30...` | |
| `app/content/data/ai/sequence-reverse.json` | weights, 143,841 bytes (base64 float32, the `gpt` format) | |

Number script `docs/reports/sequence-L4-numbers.py` (`--write` retrains and rewrites the weights file); performance report `docs/reports/sequence-4-perf.md`.

## The supplied model

A 2-block pre-norm transformer: vocabulary 11 (digits and a separator, token 10), context 12, width 32, 4 heads, MLP 128 with ReLU, learned positions, final layer norm, untied unembedding with bias: 26,571 parameters (formula, array sizes and a zeros build agree). Task: six digits, the separator, then the six digits reversed; only the six written digits are scored. Trained in the number script: seed 0, Adam 0.003, 50 warm-up steps then cosine decay (`nt_ops_l1.warmup_cosine`), 400 steps of 64 fresh sequences, none from the 1,000 held out by `default_rng(1)`.

- Held-out: 100% of the 1,000 reversed exactly by greedy decoding; seeds 1 and 2 also reach at least 0.99 (asserted). Route B: a plain NumPy forward pass (no autograd) reproduces the stream, the logits and every decoded digit; retraining seed 0 matches the shipped float32 weights to $10^{-4}$.
- Attention: in block 2, head 1, output $t$ puts its largest input weight on input $7 - t$ for every $t$ (checked on 3 1 4 1 5 9 and 8 8 8 8 8 8). Rows 5 and 6 are less clean (0.71 and 0.70 on the right input, the rest on the separator or a neighbour); the lesson says so.
- Ablation (rerun without one write, 1,000 held-out): attention 1 18.4%, MLP 1 23.0%, attention 2 0.6%, MLP 2 99.8%.
- Trap run: 100 Adam steps on one fixed batch of 32 (start `init_model(7)`): training loss 0.0043, 100% of the 32 reversed, 0.5% of held-out sequences, 46.0% of held-out digits.
- Deeper runs (6 blocks, 300 steps of 32, means over 25 steps), stated as thresholds only: as built ends below 0.01; without residuals it stays above 1.8 (seed 1 too); without layer norms it starts above 4 and ends below 1.8. The stalled run is chaotic: under `OPENBLAS_CORETYPE=Haswell` its curve differs from a plain run by up to about 0.1, so the plotted curves are checked to 0.15 and no figure from them is printed. At 2 blocks such variants ended close together (exploration, not stated).

## Self-check (SESSION PROTOCOL 4)

1. Validator: 0 errors; no `[source-ban]` or `[ai-mutants]` warning on these files.
2. Voice: `voice-scan.py 35` on the course folder: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `node tools/run-number-scripts.mjs --python <venv> --only sequence-L4`: passed (strict coverage, 0 uncovered, 31 literals with reasons; 97 s through the runner, under its 150 s local and 300 s CI limits; 37 byKey lines read by hand, all match their slips).
4. Playthrough with `--local-cdn`, desktop and `--mobile`: see the hand-back line; all seven files.

Also: `grade-all.mjs --code --file` on every file, 0 failures (11 Python widgets, 43 mutants each failing its named test first); `same-course-reuse.mjs --all` lists nothing for the course.

## Numbers and their sources

- l13: $8 \times 256 = 2{,}048$; the hand block $(1, 3) \to (0.5, 3.5) \to (0.5, 5.5)$ by `seq_ops_l4.block` and by hand, slips $-1.5$ (no ReLU), 0 (replace), $-0.5$ (first addition dropped); 5 rows move with attention and 1 without, 4 of 6 in the quiz (both on a planted block).
- l14: stream values at position 6 of 3 1 4 1 5 9 (two routes); change of c0 $-1.83$, c2 terms adding to $-2.335$; lengths 4.06, 3.76, 3.76, 5.80, 7.90 against a final 12.20 (sum 25.27).
- l15: 16,640; 33,088; 256; 49,984; 60,545; 49,280 without biases (linear biases and layer-norm shifts dropped, gains kept); 56,385 tied; 99.2% of a 50,257-token one-block model in its two tables; GPT-2 small by our formula 124,490,065 against its published 124,439,808, a gap of 50,257 (no output bias).
- l16: $\ln 11 = 2.398$; curve from 2.64 to 0.004; graded run from 2.716 to 1.454 in 10 steps (threshold 1.6, start seeds 8 and 9 also pass); 100 steps below 0.05.
- Review, problems, homework: each count by formula and by building zero arrays (12,704; 9,408; 14,779; 37,248; 74,208; 111,840; 326,516; 278,516; 421,697; 29,288,704); stream and dot products by NumPy; $6 \ln 11 = 14.387$; $0.99^6 = 0.9415$. The homework reference equals `seq_ops_l4.lm_logits` on six cases.

## Timing of graded cases (Pyodide, desktop, one worker)

Slowest case per widget: l13 16, 20 and 266 ms (`block_grad_check`); l14 53 and 40 ms; l15 38 ms; l16 62 ms, 1,648 ms (`heldout_accuracy` on 1,000 inputs, case `budget` 5,000, limit 10 s, 6.1x) and `train_reverser`: the 10-step case 403 ms, the 100-step case 3,587 ms (case `budget` 15,000, limit 20 s, 5.6x); homework 10 and 34 ms. Every case is under a third of its limit.

## Brief deviations

- The brief's `train_steps` is `train_reverser` (l10 already has a `train_steps`); it returns the list of losses, so a 3-step run is compared exactly to $10^{-6}$ (learning-loop rule) besides the 10-step threshold. `stream_trace` takes `h`; `ablate_sublayer(tokens, model, k)` numbers the parts 1 to 4 and returns logits; l16 adds `reverse_with` for greedy decoding.
- l14's hook: in the trained model the writes are not small next to the stream (each is about its size), so the lesson says each part adds a write, without "small".
- The model of l16 has two blocks (l14 needs two); the objective's "one-block" wording stands in `course.json`.
- ReLU is the MLP's activation (the brief allows it; GELU is named in one sentence), since `autograd.py` v1.0 has ReLU and no GELU.

## For `gpt` L2 and `interp` L1

Pre-norm, ReLU, every projection with a bias, row vectors times matrices. A block dict has `BLOCK_KEYS`; a model dict has `E`, `P`, `blocks`, `lnf_g`, `lnf_b`, `U`, `c`. The `gpt` brief's fused `qkv` weight is `concat([Wq, Wk, Wv], axis=1)` with bias `concat([bq, bk, bv])`; its `proj`, `fc`, `out` are `Wo`, `W1`, `W2`. `stream()` gives the residual stream after the embedding and after each sublayer, which is what a logit lens reads. Seq_ops_l3 v1.1 (merged) is what this module imports; it reaches `permute` only with non-negative axes and never masks a whole row.

## course.json

No change proposed. (Optional: l16's objective says "one-block"; the model has two blocks.)

## Backlog

Two bullets under "Raised later (sequence level 4)" in `docs/BACKLOG-INBOX.md`.

## seq_ops_l4.py as shipped

Imports `Tensor`, `_wrap` from `autograd.py` v1.0, `layernorm` from `nt_ops_l2.py`, and `attention`, `causal_mask`, `merge_heads`, `split_heads` from `seq_ops_l3.py`. Every op takes Tensors or arrays and returns a Tensor; shapes `(..., T, d)`.

- `__version__ = "1.0"`.
- `BLOCK_KEYS = ('ln1_g', 'ln1_b', 'Wq', 'bq', 'Wk', 'bk', 'Wv', 'bv', 'Wo', 'bo', 'ln2_g', 'ln2_b', 'W1', 'b1', 'W2', 'b2')`.
- `mlp(x, p) -> Tensor`: `relu(x @ W1 + b1) @ W2 + b2`, each position alone.
- `mha(x, p, h, mask=True) -> Tensor`: multi-head attention with biases, heads of width `d // h`, causal unless `mask=False`, joined, then `@ Wo + bo`.
- `attn_update(x, p, h) -> Tensor`: `mha(layernorm(x, ln1_g, ln1_b), p, h)`, the attention sublayer's write.
- `mlp_update(x, p) -> Tensor`: `mlp(layernorm(x, ln2_g, ln2_b), p)`, the MLP sublayer's write.
- `block(x, p, h) -> Tensor`: pre-norm block, `x + attn_update(x)`, then `+ mlp_update(.)`.
- `init_block(d, d_mlp, seed=0) -> dict`: weights $N(0, 1/\text{fan\_in})$ from `default_rng(seed)` in `BLOCK_KEYS` order, biases 0, gains 1.
- `lm_logits(tokens, model, h) -> Tensor`: `E[tokens] + P[:T]`, every block, `layernorm(lnf_g, lnf_b)`, `@ U + c`; logits `(..., T, vocab)`.
- `stream(tokens, model, h) -> list[np.ndarray]`: the stream after the embedding and after each sublayer, `1 + 2 * len(blocks)` arrays.
- `flat_params(model) -> list[(name, array)]`: `E`, `P`, `blocks.<i>.<key>`, `lnf_g`, `lnf_b`, `U`, `c` (or a block's keys for a block dict).
- `n_params(model) -> int`.
- `read_model(path) -> dict`: a model from `{name: {"shape", "b64"}}` (little-endian float32), extra keys ignored.

Gradient checks in the number script, all under $10^{-6}$ against central differences: `mlp`, `mha` (causal, 2 heads, a batch) and `block` (4 heads, a batch) over the input and every parameter; `lm_logits` through cross-entropy over every parameter of a 1-block model. `block` equals a plain NumPy block to $10^{-12}$.
