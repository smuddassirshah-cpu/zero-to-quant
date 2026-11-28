# cnn level 2 (Stride, padding and pooling): report

## Files written

All in `app/content/courses/cnn/`, skill `cnn-layers` throughout. Plus `app/content/data/ai/cnn_ops_l2.py` (version 1.0, imports the frozen `autograd.py` v1.0 only), for level 3.

| File | Screens / items | Code widgets |
|---|---|---|
| `l5-stride-and-padding.json` | 12 screens, 3 quiz, 15 min | `out_size`, `conv2d(img, k, stride, pad)`, `padding_for_same` (raises `ValueError` for even $k$) |
| `l6-pooling.json` | 12 screens, 3 quiz, 15 min | `maxpool2d` with `avgpool2d`, `maxpool_backward` (routing, first maximum on a tie), `pool_shift_change` |
| `l7-counting-parameters.json` | 12 screens, 3 quiz, 15 min | `conv_params` with `dense_params`, `count_net`, `receptive_field` |
| `l8-im2col.json` | 12 screens (one ungraded `trainer` timing screen), 3 quiz, 18 min | `im2col`, `conv2d_im2col` (no loop), `col2im` (adjoint test) |
| `review-2.json` | 9 items, difficulty 2 to 4, `pass: 0.8` | none |
| `homework-2.json` | 7 items, difficulty 3 to 5 | performance `conv_layer_forward_backward` (5), `maxpool_overlap` (4); `order` (why the input gradient is col2im of $\mathbf{G}\mathbf{W}$, one distractor); `longform` "a CNN for 32 by 32 under 10,000 parameters" (10-point rubric, model design of 6,138 parameters); three numeric or choice |
| `problems-2.json` | 3 problems, 11 parts, difficulty 4, 3, 5 | none |

Lesson shapes follow the brief. l5: predict 6, 8 and 4 for the 7 from l3 and step a stride-2 window over the padded image (`matrix`, padding and window in two colours), the formula (16 for 32, 5, 2, 2), a table of four layers, the derivation as an `order` with a distractor ($n + p$), "same" padding, stride as downsampling, trap the missing floor (4.5 against 4), edge case a stride longer than the kernel (3 columns never read), transfer a volatility-surface model's shapes. l6: max pool by hand, a one-pixel shift that changes 2 of 4 pooled values, average pooling (2.5), the routing backward (tap the winner), the average backward (0.5 each), trap "pooling is shift-invariant", edge case a tie (first maximum), transfer the worst daily loss of each week (£410). l7: 160 against 66,560 (416 times), sliders on channels with log-scale bars, 9,216 multiply-adds, the level 3 net ($160 + 0 + 2{,}570 = 2{,}730$), receptive fields 5 and 7, trap biases and channels (608 against 208 and 8,792), the edge case 1 by 1 in the quiz (2,080), transfer 4,608,000 multiply-adds a minute for 500 stocks. l8: the second patch as a row, a 16-frame walk of patches to rows, $64 \times 9$ times $9 \times 16$, one entry (1), col2im counts (4, 6, 9), trap a col2im with `=`, the timing `trainer`, the backward as products, transfer memory (14.04 MB against 1.56 MB).

## Ops added: `cnn_ops_l2.py`

`out_size`, `im2col(x, k, stride, pad)` and `col2im(cols, x_shape, k, stride, pad)` on `(N, C, H, W)` arrays; `conv2d(x, W, b, stride=1, pad=0)` as a `Tensor` op by im2col (forward one product; backward $\mathbf{G}^T\mathbf{C}$, column sums, col2im of $\mathbf{G}\mathbf{W}$); `maxpool2d(x, size)` (routes to the first maximum) and `avgpool2d(x, size)`; a 3-D input is a batch of one. Gradient checks in float64 (number script, two routes: `grad_check`, and loops with the script's own central differences): `conv2d` 1.5e-10, 4.5e-11, 8.0e-11 (own 1.9e-10, 7.5e-11, 2.2e-9) on (2, 3, 7, 7) k3 s2 p1, (1, 1, 8, 8) k3 s1 p1 and (3, 6, 6) k2 s2 p0; max pool 5.2e-11 (own 5.2e-11), average pool 3.3e-11 (own 3.3e-11); the tie routing and the im2col/col2im adjoint identity are checked too. Speed: one forward and backward of conv (16 filters, padding 1), ReLU and max pool on a batch of 64 digits takes about 9 ms in CPython, so a level 3 epoch of the digits stays within the timing rule. No level 2 widget ships the module; level 3 will, beside `autograd.py`.

## Gates

1. Validator: `node tools/validate.mjs` 0 errors; no `[ai-mutants]` warning. Advisory warnings on level 2 files: point hints without highlight, ladder canvas-kind changes, `O2-long-sentence` (34 on level 2), three `O2-explain-answer` where the answer is a padding stated in words.
2. Voice: `voice-scan.py 35` on the course: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `docs/reports/cnn-L2-numbers.py` with the venv: 331 of 331 checks, exit 0, about 2 s. Route B lists every window start for sizes, builds weight arrays for counts, counts multiply-adds term by term, pools and convolves by loops, and stamps windows for col2im counts. It checks every lesson, review, homework and problem number at its JSON path, every numeric `wrong`, the ops module, and every code widget (14 widgets, 42 mutants). Writing it caught one wrong figure in the homework model answer (a receptive field of 15 that left out the pools; now 18).
4. Code in Pyodide: `node tools/grade-all.mjs --code --local-cdn <pkgs>` on all seven files: 67 widgets graded and 14 Python widgets run, 0 failures.
5. Playthrough: all seven files with `--local-cdn <pkgs> --mobile` (desktop and 440 px): all passed; homework "1 performance starter fail" as required. Screens read at 440 px; fixes made: padding cells no longer hide the window on the l5 matrix. The 16 by 9 patch matrix of l8 still runs below the fold at 440 px with `maxHeight` set (it caps only the stack as a whole); the learner scrolls to the slider (inbox bullet).
6. Performance task: `docs/reports/cnn-2-perf.md`.

Browser timing (l8, brief: loop against im2col, never graded): the `trainer` screen times both on a 16 by 16 image with 16 filters of 3 by 3. Pyodide 0.27.7 under Node: loop 23.5 ms, im2col 0.48 ms (about 50 times); CPython: 9.0 ms and 0.21 ms. The playthrough does not press Run, so no in-page figure was recorded; the prose states the Node figure and says a device will differ.

## Data and seeds

The 7 of l3 (seed 8) for l5; the 4 by 4 map $(1, 3, 2, 0; 4, 2, 1, 1; 0, 1, 5, 2; 3, 2, 0, 6)$ for l6; the 4 by 4 image $(1, 2, 0, 1; 3, 1, 2, 0; 0, 2, 1, 3; 1, 0, 2, 1)$ for l8; ten days of P&L in l6's transfer. Test seeds 51 to 94 as named in each `setup`.

## Proposed course.json change

None.
