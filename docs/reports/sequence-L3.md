# sequence level 3 (Self-attention): author report

Branch `ai-w5-sequence`. Skill `sqn-self` on every file.

## Files

| File | Screens or items | Code widgets (mutants) |
|---|---|---|
| `l9-self-attention.json` | 9 screens, quiz 3 | `attention_matrix` + `self_attention` + `permutation_check` (4) |
| `l10-causal-mask.json` | 11 screens, quiz 3 | `causal_mask` + `masked_attention` + `leak_test` (4), `dev_loss` + `train_steps` (3) |
| `l11-many-heads.json` | 9 screens, quiz 3 | `split_heads` + `merge_heads` + `head_params` + `multi_head_attention` (4) |
| `l12-positions.json` | 10 screens, quiz 3 | `sinusoidal_positions` + `add_positions` + `order_matters` (4) |
| `review-3.json` | 9 items, `pass` 0.8 | none |
| `homework-3.json` | 8 items (one `order`, one `longform`, two `code`) | `head_patterns` (3), `causal_mha_forward` performance task (5) |
| `problems-3.json` | 4 chained items, 16 parts, one at difficulty 5 | none |
| `app/content/data/ai/seq_ops_l3.py` | new module, 2,351 bytes, SHA-256 `37ce243f0a9a...` | |
| `app/content/data/ai/sequence-attn-names.json` | weights, 116,103 bytes, SHA-256 `6f9c03264262...` | |

Number script `docs/reports/sequence-L3-numbers.py` (`--write` retrains and rewrites the weights file); performance report `docs/reports/sequence-3-perf.md`.

## The supplied model

One causal self-attention layer over makemore's 27 symbols: token embeddings and a learned position table (8 by 32), width 32, context 8, one head (`h1`) or 4 heads (`h4`), output matrix $\mathbf W_O$ and a linear readout; no residual (level 4 adds it). Trained by the number script with a hand-written NumPy backward pass and Adam (0.003), 3,000 steps of 64 windows, seed 0, on makemore's training names (its split: `default_rng(42)` permutation, 25,626 / 3,203 / 3,204). Each next symbol of each name, the end mark included, is scored once with up to 8 symbols of context, as makemore's "nats a letter".

**Dev loss of the supplied weights against the bigram's:** one head 2.273664 nats a letter (3.2802 bits), 4 heads 2.172923 (3.1348 bits), bigram 2.4514 (3.5366 bits), all over the same 22,807 dev symbols. Seeds 1 and 2 of both models also beat the bigram by more than 0.08 (asserted in the script).

Route B: the hand backward pass equals `autograd.py` with `seq_ops_l3` on a batch (both models, to $10^{-8}$); the dev loss of the shipped weights is recomputed with the autograd forward; the bigram's 2.4514 is recomputed from add-one counts on the training names; retraining seed 0 matches the shipped weights to $10^{-4}$.

## Self-check (SESSION PROTOCOL 4)

1. Validator: 0 errors; no `[source-ban]` or `[ai-mutants]` warning on these files.
2. Voice: `voice-scan.py 35` on the course folder: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `node tools/run-number-scripts.mjs --python <venv> --only sequence-L3`: passed (strict coverage; 41 s; every `wrong` value read against its `why`: 35 lines checked by hand, all match).
4. Playthrough with `--local-cdn`, desktop and `--mobile`: all 4 lessons, `review-3`, `homework-3` (performance starter fails, longform marked) and `problems-3` passed; l10, l11, `homework-3` and `problems-3` replayed after their last edits, both modes.

Also: `grade-all.mjs --code --file` on every file, 0 failures (7 Python widgets, 31 mutants each failing its named test first); `same-course-reuse.mjs --all` lists nothing for the course (a `problems-3` item first retold a review sentence and was reworded; a shared-numbers warning was removed by moving the homework to the 4-head model).

## Numbers and their sources

- l9: the toy sequence $a\,b\,c\,a\,b$ with identity matrices: row a4 0.267, 0.132, 0.202, 0.267, 0.132; b5 on b2 0.2594 (vectorised against a loop); 121 scores; 16 times the scores for 4 times the headlines.
- l10: the recorded runs (300 steps, seed 0, means over tens of steps): unmasked training loss falls to about 0.16, the same weights score 6.84 on dev with the mask, the masked run sits near 2.35. 10 and 528 allowed pairs (counted on `causal_mask`); masked row 0.2689 and 0.7311; masking after the softmax leaves 0.0566; graded training starts at 3.3803 and its tenth loss is 2.6899 (threshold 2.75).
- l11: 16 features a head; feature 37 in head 2; $4 \times 64^2 = 16{,}384$ weights.
- l12: without positions, ".mar" and ".amr" give the same chance of i next, 0.2377 (equal to $10^{-12}$); with positions 0.2910 and 0.4306. $\sin 3 = 0.1411$, $\sin(2.8117) = 0.3239$, self dot product 16 and 15.31 at offset 1, the same at every $t$ (checked on a table of 20 positions).
- Review, problems, homework: each answer and slip recomputed (0.8808; 9,216; 3.1348 bits; masked weights 0.3302, 0.5035 and output 0.7517 by a loop; 528, 4,224, 16,384; $\sin 2$, $\cos 2$; gap 0.1777 nats, 0.2564 bits, perplexity 9.71, 1.79 bits a name; 8,256; $\cos 7 = 0.7539$; 4-head perplexity 8.78). The homework's `causal_mha_forward` equals an explicit loop over heads and positions for five cases, including one token and heads of width 1.

## Timing of graded cases (Pyodide, desktop, one worker)

Slowest case per widget: l9 21 ms; l10 98 ms and 650 ms (`train_steps`, 10 steps through the autograd on 256 windows, widget `budget` 4,000 ms, limit 9 s, 13.8x); l11 18 ms; l12 57 ms; homework 19 and 22 ms. Every case is under a third of its limit.

## Module `seq_ops_l3.py` (frozen once merged)

Public names and signatures, for `sequence` L4, `gpt` and `interp` (it imports `Tensor` and `_wrap` from `autograd.py` v1.0 and `softmax`, `swap_last` from `seq_ops_l2.py`):

- `causal_mask(T) -> np.ndarray`: T by T float array, 0 where key $j \le$ query $i$, `-inf` above the diagonal. Add it to the scores.
- `permute(x, axes) -> Tensor`: `np.transpose` of a Tensor by `axes`; backward applies the inverse permutation.
- `split_heads(x, h) -> Tensor`: $(\dots, T, d) \to (\dots, h, T, d/h)$; head $k$ holds features $k\,d/h$ to $(k + 1)\,d/h - 1$. Raises `ValueError` if $h$ does not divide $d$.
- `merge_heads(x) -> Tensor`: $(\dots, h, T, d_h) \to (\dots, T, h\,d_h)$, the inverse of `split_heads`.
- `attention(Q, K, V, mask=None) -> Tensor`: $\operatorname{softmax}(\mathbf Q\mathbf K^\top/\sqrt d + \text{mask})\,\mathbf V$, the softmax along the last axis, $d$ the last axis of $\mathbf Q$; works on stacks of heads.
- `__version__ = "1.0"`.

Gradient checks: `permute` on a 3-D array, `split_heads` and `merge_heads` alone and in a round trip on a batch, masked `attention` on a stack with the mask fixed (all under $10^{-6}$ against central differences), and `causal_mask(32)` with 528 zeros and 496 entries at $-\infty$.

`sequence-attn-names.json` holds `vocab`, `context`, `width`, `h1` and `h4` (each `E`, `P`, `Wq`, `Wk`, `Wv`, `Wo`, `U`, `c` as nested lists, rounded to 6 places), `dev_h1` and `dev_h4`, and an `about` line with the makemore credit (MIT). A line for `app/content/data/ai/README.md` is proposed for the main session (content agents do not edit it): "`sequence-attn-names.json`: sequence L3's causal self-attention layers (1 and 4 heads) on the makemore names, written by `docs/reports/sequence-L3-numbers.py --write`; derived from `names.txt` (MIT, makemore)."

## Notes for the brief

The brief's l12 hook ("ab" and "ba" give the same output at the last position) does not hold for a causal model: the last query is the last token, and the mask lets earlier positions see different prefixes. The lesson uses ".mar" and ".amr", which share the last token and the set before it, and says in one sentence that the mask itself carries some order.

## course.json

No change proposed.

## Backlog

One bullet under "Raised later (sequence level 3)" in `docs/BACKLOG-INBOX.md`.
