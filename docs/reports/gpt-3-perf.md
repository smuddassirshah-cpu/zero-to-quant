# gpt level 3: performance task

`homework-3.json`, `h-train-small`, item 1 of 6. Kind `code` (Python).

Matched objective: l9-the-training-loop "Build the training loop: batches, loss, backward pass and an Adam step." (also l10 "Check the GPT's gradients against central differences.").

Task: from a stub starter, `train(steps, lr, seed)` for a small GPT (vocabulary 65, context 16, width 16, 2 heads, MLP 64, 5,713 parameters) on the training part of the slice, returning `(weights, losses)`, and `grad_check(seed)` on the tiny configuration of l10 (1,005 numbers) with central differences at $h = 10^{-5}$. The rules (initial weights in `shapes` order, batches of 8 from `default_rng(seed + 1)`, Adam from `nt_ops_l1` at a fixed rate) make one run exact. `gpt_ops_l3.py` is not shipped with this item, so the learner writes the batches, the loss and backward pass and the Adam loop; `autograd.py`, `nt_ops_l1.py`, `seq_ops_l2/3/4.py`, `nt_ops_l2.py` and `gpt_ops_l2.py` are.

Tests: 7 hidden, 2 examples. The first 3 losses of seed 0 at 0.01 compared to $10^{-6}$ relative (the learning-loop rule); 60 steps for seeds 0 and 1 below 3.2 nats on 2,000 validation characters (the number script measures 2.87 and 2.78); the array names; the gradient check below $10^{-6}$ and above $10^{-13}$; a run at rate 0. Mutants: plain gradient descent (test 1), targets equal to inputs (test 1), a one-sided difference in the check (test 5), an extra random draw before the batches (test 1).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/gpt/ python3 docs/reviews/voice-scan.py 35`: 0 over 35 words and 0 explanations over three sentences.
3. Numbers script: `node tools/run-number-scripts.mjs --python <venv> --only gpt-L3`: passed (strict coverage).
4. Playthrough: `node tools/playthrough.mjs --set gpt/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: all passed, the starter fails; `grade-all.mjs --file ... --code`: 0 failures (solution, starter, mutants).

Overlapping screens: l9-the-training-loop screens[3] (`get_batch`) and screens[5] (`train_step`), l10-checking-gradients screens[3] and [5] (`numeric_grad`, `rel_error`, `check_model`). New here: a whole run from initialisation to held-out loss in one function, a different model size, and a gradient check written without the helpers.
