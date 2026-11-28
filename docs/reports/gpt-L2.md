# gpt level 2: A tiny GPT forward pass (report)

Author: content agent, wave 6, branch `ai-w6-gpt` (from `04c28ba5`). Brief: `docs/briefs/gpt.md` Level 2 with `docs/briefs/ai-strand-interfaces.md`. Skill `gpt-forward` throughout; ids, names and objectives from `course.json`. The block is `sequence` L4's (`seq_ops_l4.py`, merged): pre-norm, ReLU MLP, every projection with a bias.

## Files

| File | Screens or items | Quiz | Code widgets (mutants) |
|---|---|---|---|
| `l5-the-whole-model.json` | 11 | 4 | `param_count` + `shapes` (5) |
| `l6-loading-weights.json` | 11 | 3 | `load_weights` + `check_shapes` (5), `init_loss` (3) |
| `l7-next-character.json` | 12 | 3 | `causal_mask` + `forward` (5), `loss` (4) |
| `l8-generating-text.json` | 11 | 3 | `sample_next` (5), `generate` (4) |
| `review-2.json` | 10 items, `pass` 0.8 | | difficulty 2 to 4, every lesson at least twice |
| `homework-2.json` | 6 items | | `h-gpt-loss` performance task (4 mutants), `topk_probs` (4), order with a distractor, longform (10-point rubric), numeric, choice |
| `problems-2.json` | 3 problems, 13 parts | | sizing a desk model to file sizes (d5), shapes through a batch (d3), losses from chances (d4) |
| `app/content/data/ai/gpt_ops_l2.py` | module, SHA-256 `d6477cfcc475...` | | |
| `app/content/data/ai/gpt-w-embed.json`, `gpt-w-block0.json` | the trained tiny GPT, 28,580 and 68,271 bytes | | |

Canvases: `graph` (data flow with shapes; the block), `table` (counts, files, steps), `matrix` with heat (head 3 on `MENENIUS`), `bars` with frames (next-character chances while reading a name; temperature 0.5, 1, 2), `series` (loss by position with the bigram line), `array` (bytes, windows, the sliding window), `console` (file start, a run, a 200-character sample). Performance report: `docs/reports/gpt-2-perf.md`.

## Self-check (SESSION PROTOCOL 4)

1. Validator: 0 errors; no `[source-ban]` or `[ai-mutants]` warning on these files.
2. Voice: `VOICE_BASE=app/content/courses/gpt/ python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `node tools/run-number-scripts.mjs --python <venv> --only gpt-L2`: passed; strict coverage, 0 uncovered, 11 literals with reasons; 293 checks.
4. Playthrough, `--local-cdn`, `--why`, desktop and `--mobile`, all seven files: all passed (lessons 14 to 15 checks each, review 10 of 10, homework 6 of 6 with the performance starter failing and the longform marked, problems 13 parts with 21 slips routed). l5, the review, homework and problems replayed after their last edits: passed.

Also `grade-all.mjs --file <each> --code --local-cdn`: 0 failures (9 Python widgets: solution passes, starter fails, 39 mutants each fail their named test; the number script checks the same in CPython). `same-course-reuse.mjs --all`: nothing for the course. `fresh-check --file problems-2.json`: 0 hits, 2 advisory lines (shared widths of a desk model with the homework, changed after a first run; the remaining advisory is the stock 48 and 64).

Screenshots looked at: the data-flow graph and block diagram were crowded at 440 px (labels truncated, edge labels on top of nodes); redrawn in two columns and without edge labels. The rest (matrix heat, bars frames, series, console) read cleanly.

## The supplied model

The app's tiny GPT: vocabulary 65, context 32, width 32, 4 heads of 8, one block, MLP 128, 18,017 parameters. Trained by `docs/reports/gpt-L2-numbers.py --write`: weights $N(0, 0.02^2)$ from `default_rng(0)` in `gpt_ops_l2.shapes` order, biases 0, gains 1; Adam (`nt_ops_l1.adam_step`) at 0.003, 100 warm-up steps then cosine (`warmup_cosine`), 5,000 steps of 16 windows of 32 from the first 225,000 characters, batches from `default_rng(1)`; about 40 to 70 s in CPython. Validation (the last 25,000 characters, never trained on, 781 windows): 1.7933 nats, 2.5872 bits a character, against the bigram's 2.4554. Weights are little-endian float32 in base64, one file for `wte`, `wpe`, `lnf`, head and one for the block; together 96,851 bytes, the brief's single-file figure (the sizes depend only on the shapes).

Route B for every forward figure: `gpt_ops_l2` (plain NumPy), `seq_ops_l4.lm_logits` through `to_model`, and a per-position loop in the script agree to $10^{-10}$.

## Numbers and sources (all in the script, two ways each)

- Counts: 18,017, 30,721, block 12,704, 60,545 against the spike's 59,840 (gap 705: attention biases 256, layer norms 384, head bias 65), card 120,672, review 5,969, homework 44,105 (tied), problem 28,272 and 67,472; each by the closed formula and by summing `shapes` (tied: dropping `head_w`).
- Bytes: 5,464, 10,924, 11,096, 72,068, 269,888, 359,852 characters, by building base64 and by $4 \lceil 4n/3 \rceil$.
- Losses: $\ln 65 = 4.1744$ and the all-zero model; init loss 4.1767 (seed 0) by two routes; validation 1.7933 by three; position 0 2.566 against later positions near 1.76; window 1.7487; chance of `t` after `⏎First Ci` 0.9850 (loss 0.0152); `C` after `First␣` 0.048; head 3 attention by the loop and the cache; temperature bars at 0.5, 1, 2 (chance of `l` 0.834, 0.619, 0.316); hand softmaxes by `math` and NumPy; surprise of 0.02 is 5.6439 bits.
- Samples: 200 characters at $\tau = 1$, seed 0, and the greedy loop (`The the the ...`), from `gpt_ops_l2.sample_text`, matched by the learner-style `generate` in the widget tests.

## Runtime (Pyodide 0.27.7, node, the app's code runner)

Measured with a scratch harness on the app's runner: one forward pass of 16 windows of 32, 8 ms; one training step of the same batch with `autograd.py` and `seq_ops_l4`, 56 ms (for level 3). The heaviest L2 case is `generate` with 40 characters, 40 forward passes of one window, well under the 1 s rule; no `budget` needed. The tools print no per-case times (already raised by `sequence` L4).

## For later levels (interp L1, post-train L1)

`gpt_ops_l2.py` v1.0 as shipped: `VOCAB`, `CONFIG`, `BLOCK`, `encode(text)`, `decode(ids)`, `shapes(config)`, `load_weights(*texts)`, `read_weights(*paths)`, `weights_json(weights, names)`, `to_model(weights, n_layer=None)`, `forward_cache(weights, idx, n_head=4)` (keys `x0`, `h<i>.ln1`, `.q`, `.k`, `.v`, `.att`, `.z`, `.attn_out`, `.mid`, `.ln2`, `.hidden`, `.mlp_out`, `.post`, `lnf`, `logits`), `forward_logits(weights, idx, n_head=4)`, `mean_loss(weights, idx, targets, n_head=4)`, `sample_text(weights, prompt, n, temperature=1.0, top_k=None, seed=0, n_head=4)`. Imports only NumPy, base64 and json. The level-3 report lists the two-block model and the training module.

## Data files and credit lines

- `gpt-w-embed.json`, `gpt-w-block0.json`: "Weights trained by this course on Tiny Shakespeare (the text as distributed with Andrej Karpathy's char-rnn; Shakespeare's plays are in the public domain)." Written by `docs/reports/gpt-L2-numbers.py --write`.
- `gpt_ops_l2.py`: "Code written for this course."

## Brief deviations

- Array names follow the brief (`wte`, `wpe`, `h0.qkv_w`, `h0.proj_w`, `h0.fc_w`, `h0.out_w`, `lnf_g`, `head_w` ...); `to_model` maps them to `seq_ops_l4`'s `E`, `P`, `Wq`, `Wk`, `Wv` (columns 0 to 31, 32 to 63, 64 to 95 of `qkv_w`), `Wo`, `W1`, `W2`, `U`, `c`.
- Weights come in two files (interfaces: one per block); `load_weights(json_text)` loads one, and the lessons merge the two dicts.
- l7's "logits for ROMEO: step by step" uses `⏎First Citizen:`: the slice holds no Romeo, and the trained model's guesses inside an unseen name are not instructive.
- The temperature slider is a frames control over three precomputed states (see backlog).

## Proposed course.json change

None.

## Backlog

Two bullets under "Raised later (gpt level 2)" in `docs/BACKLOG-INBOX.md`.
