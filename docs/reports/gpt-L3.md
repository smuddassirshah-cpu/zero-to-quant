# gpt level 3: Training on Tiny Shakespeare (report)

Author: content agent, wave 6, branch `ai-w6-gpt`. Brief: `docs/briefs/gpt.md` Level 3 with `docs/briefs/ai-strand-interfaces.md`. Skill `gpt-train` throughout; ids, names and objectives from `course.json`. This level carries the strand exit "a tiny GPT whose held-out loss per character beats the bigram's" (l12).

## Files

| File | Screens or items | Quiz | Code widgets (mutants) |
|---|---|---|---|
| `l9-the-training-loop.json` | 11 | 3 | trainer (40 live steps, ungraded), `get_batch` (4), `train_step` (5) |
| `l10-checking-gradients.json` | 11 | 3 | `numeric_grad` + `rel_error` (4), `check_model` (4) |
| `l11-short-runs.json` | 11 | 3 | `overfit_one_batch` (3), `diagnose` (4) |
| `l12-beating-the-bigram.json` | 12 | 3 | `bigram_val_loss` (4), `gpt_val_loss` + `beats_bigram` (4) |
| `review-3.json` | 10 items, `pass` 0.8 | | difficulty 2 to 4, every lesson at least twice |
| `homework-3.json` | 6 items | | `h-train-small` performance task (4 mutants), `find_lr` (3), order with a distractor, longform (10-point rubric), numeric, choice |
| `problems-3.json` | 3 problems, 13 parts | | a desk chat model from step 0 to the bigram gap (d5), a gradient check by hand (d4), a slow first run (d3) |
| `app/content/data/ai/gpt_ops_l3.py` | module, SHA-256 `e7c2949a22c8...` | | |
| `app/content/data/ai/gpt-w2-embed.json`, `gpt-w2-block0.json`, `gpt-w2-block1.json` | the two-block model for `interp`, 28,580, 68,271 and 68,271 bytes | | |

Canvases: `series` (live trainer; recorded training and validation curves with the bigram line; zeroed against never-zeroed gradients; the sweep with frames; the overfit run; loss by position), `plane` (error against $h$ on a log axis; loss at step 10 against the rate), `table`, `array`, `bars` (smoothing frames), `console` (two samples). Performance report: `docs/reports/gpt-3-perf.md`.

## Self-check (SESSION PROTOCOL 4)

1. Validator: 0 errors; no `[source-ban]` or `[ai-mutants]` warning on these files.
2. Voice: `voice-scan.py 35` on the course folder: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `node tools/run-number-scripts.mjs --python <venv> --only gpt-L3`: passed, 78 s; strict coverage, 0 uncovered, 33 literals with reasons; 251 checks.
4. Playthrough, `--local-cdn`, `--why`, desktop and `--mobile`, all seven files: all passed (lessons 13 to 15 checks, review 10 of 10, homework 6 of 6 with the performance starter failing and the longform marked, problems 13 parts, 15 slips routed). l9 and l10 replayed after their last edits.

Also `grade-all.mjs --file <each> --code --local-cdn`: 0 failures (10 Python widgets, 39 mutants each failing its named test). `same-course-reuse.mjs --all`: nothing for the course.

## Runtime (measured, Pyodide 0.27.7 through the app's code runner)

One training step of the tiny GPT (batch 16, context 32, one block) with `autograd.py` and `seq_ops_l4`: 56 ms; batch 4: 10 ms; a forward pass of 16 by 32: 8 ms. Hence: `train_step` cases run 1 to 3 steps; the overfit test uses a batch of 4 so 100 steps take about 1 s (case `budget` 15,000); the homework's small GPT (width 16, context 16, batch 8) runs 60 steps per case with `budget` 8,000; `check_model` and `grad_check` do 2,010 small forward passes (budget 8,000). No case approaches 10 s on a desktop.

## The long runs (number scripts)

- The one-block tiny GPT (level 2's weights) is retrained by this script with a written-out loop and matches the shipped float32 weights to $10^{-4}$; its validation loss is 1.7933 by both. 5,000 steps; training batches end near 1.69, validation 1.79 (curve every 250 steps on l9).
- The two-block model for `interp` L1: same recipe and seed, `--write` only (about two minutes): 30,721 parameters, validation 1.7413 nats on the same 25,000 characters. Its forward pass equals `seq_ops_l4.lm_logits`.
- Exact figures are given only for deterministic or short stable runs (the 3-step tests, the 10-step sweep to 0.002, the overfit run); the rate-1 run of the homework's finder diverges and is checked only as diverging.

## Numbers and sources (two ways each, in the script)

Bigram 2.4554 (validation), 2.4237 (training), 2.4494 at $\alpha = 0.1$, by NumPy counts and a pure-Python counter; `q` 102 times, always before `u`, add-one chance 0.6168; 45 unseen validation pairs of 19 kinds; GPT 1.7933 by `eval_loss` and the windows; gap 0.9552 bits; per-character standard deviation 1.553, standard error 0.110 on 200 characters; one Adam step 1.8394 to 1.7199 on the fixed batch (two routes); Adam by hand 0.5030; zeroed against never-zeroed gradients after 20 steps 3.16 against 3.35; central differences 12.0001 and the float64 and float32 error curves (Python floats and NumPy); the tiny model's check ranges (float64 below $10^{-8}$, float32 between $10^{-3}$ and $10^{-1}$, one-sided between $10^{-5}$ and $10^{-4}$, $h = 10^{-11}$ between $10^{-5}$ and $10^{-3}$); sweep at 7 rates (best 0.01, 3.2357; 0.1 spikes above 6.9); overfit 0.0015 after 100 steps, validation 8.04; homework threshold 3.2 (2.87 and 2.78 measured).

## For `interp` L1 and `post-train` L1

Shipped and frozen once merged (import, never edit):

- `gpt_ops_l2.py` v1.0 (level 2): `VOCAB`, `CONFIG`, `encode(text)`, `decode(ids)`, `shapes(config)`, `load_weights(*texts)`, `read_weights(*paths)`, `weights_json(weights, names)`, `to_model(weights, n_layer=None)`, `forward_cache(weights, idx, n_head=4)`, `forward_logits(weights, idx, n_head=4)`, `mean_loss(weights, idx, targets, n_head=4)`, `sample_text(weights, prompt, n, temperature=1.0, top_k=None, seed=0, n_head=4)`. `forward_cache` keys per block `h<i>.ln1`, `.q`, `.k`, `.v` (heads, T, 8), `.att` (heads, T, T), `.z` (heads joined, before `proj_w`), `.attn_out`, `.mid`, `.ln2`, `.hidden`, `.mlp_out`, `.post`; then `lnf` and `logits`; `x0` is embedding plus position. A head's write is `z[..., 8h:8h+8] @ proj_w[8h:8h+8]`; `proj_b` is one more part of the attention write.
- `gpt_ops_l3.py` v1.0 (this level): `init_weights(seed, config=None, sd=0.02)`, `get_batch(data, B, T, rng)`, `loss_and_grads(weights, X, Y, n_head=4) -> (float, {name: grad})`, `adam_init(weights)`, `adam_update(weights, grads, state, lr) -> new weights` (state updated), `train(weights, data, steps, lr, B=16, T=32, seed=1, warmup=0, n_head=4) -> (weights, losses)`, `eval_loss(weights, data, T=32, n_head=4)`, `bigram_loss(train_ids, val_ids, alpha=1.0, V=65)`. All take any vocabulary size (from `head_w`), so a resized embedding works.
- Weights: one block `gpt-w-embed.json` + `gpt-w-block0.json` (18,017); two blocks `gpt-w2-embed.json` + `gpt-w2-block0.json` + `gpt-w2-block1.json` (30,721). Read with `gpt_ops_l2.read_weights(*files)`. Names `wte`, `wpe`, `h<i>.ln1_g`, `.ln1_b`, `.qkv_w` (Q, K, V in columns 0 to 31, 32 to 63, 64 to 95), `.qkv_b`, `.proj_w`, `.proj_b`, `.ln2_g`, `.ln2_b`, `.fc_w`, `.fc_b`, `.out_w`, `.out_b`, `lnf_g`, `lnf_b`, `head_w`, `head_b`. Untied head with a bias.
- Data: both models trained only on the first 225,000 characters of `tiny-shakespeare.txt`; the last 25,000 (so the last 2,000 that interp uses) are held out. Width is 32 (the brief's tiny GPT), not the 64 the interp brief mentions as a possible fix; two blocks as interp needs.
- Shipping in a widget: `data` with `autograd.py`, `nt_ops_l1.py`, `nt_ops_l2.py`, `seq_ops_l2.py`, `seq_ops_l3.py`, `seq_ops_l4.py`, `gpt_ops_l2.py`, `gpt_ops_l3.py` and the weight files, as l11 does.

## Data files and credit lines

- `gpt-w2-embed.json`, `gpt-w2-block0.json`, `gpt-w2-block1.json`: "Weights trained by this course on Tiny Shakespeare (the text as distributed with Andrej Karpathy's char-rnn; Shakespeare's plays are in the public domain)." Written by `docs/reports/gpt-L3-numbers.py --write`.
- `gpt_ops_l3.py`: "Code written for this course."

## Brief deviations

- `train_step(params, opt_state, batch, lr)` takes a dict of `Tensor`s kept between steps (so zeroing the gradients is the learner's job, which the trap needs) and returns the batch loss before the update; tests check the loss after the step separately.
- The long run is 5,000 steps (the brief allowed 2,000 to 5,000).
- The homework performance task trains a smaller GPT (width 16, context 16) so 60 steps fit a case; its gradient check uses l10's tiny configuration with weights scaled to $\sigma = 0.3$.
- l10's error plot shows $\log_{10}$ of the error on a linear axis (see backlog).

## Proposed course.json change

None.

## Backlog

One bullet under "Raised later (gpt level 3)" in `docs/BACKLOG-INBOX.md`.

## Fix pass notes for later authors (frozen module `gpt_ops_l3.py`)

Second reader (`docs/reviews/review-gpt-24.md`) found no module error. Two usage notes for `interp` and `post-train`:

- `eval_loss` on fewer than $T + 1$ characters has no windows and returns `nan` with a NumPy warning instead of raising. Callers pass at least 33 characters (`interp`'s last 2,000 are safe).
- `bigram_loss` defaults `V` to 65, while `loss_and_grads`, `train` and `eval_loss` read the vocabulary from `head_w`. A resized vocabulary must pass `V` to `bigram_loss`.
