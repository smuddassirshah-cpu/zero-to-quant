# makemore level 2 (A network with embeddings): report

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l5-three-letters-of-context.json` | 10: problem after em against after m (`bars` groups), explore the rows of `...emma.` (`array` stepper with context and next bands), name X and Y (`table` canvas, `table` widget), ladder 182,531 rows, ladder why not count contexts (5,440 of 19,683 seen), trap a window across joined names, ladder edge jo (3 rows, all with a start mark), generalise any block size (block 1 is the bigram), code `build_dataset`, transfer three days of returns. 14 min | 3 |
| `l6-letters-as-points.json` | 10: problem one-hot distance $\sqrt 2$, explore the recorded 2D embedding of two seeds (`scatter` with a `frames` control, vowels grouped), name the lookup (4 by 2 `matrix`), ladder shapes (32, 3, 10), ladder the gradient of a repeated row, trap `dC[X] += dE` keeps one copy (`console`), ladder edge a letter absent from the batch, generalise lookup as a one-hot product (270), code `embed` and `embed_backward`, transfer ticker embeddings. 14 min | 3 |
| `l7-the-mlp-model.json` | 12: problem how many weights (`graph`, directed), explore shapes layer by layer (`graph` with a `frames` control and node values), name and count (6,097, `table` widget), ladders a planted forward pass (hidden unit, then logit), ladder the 0.01 on $W_2$ (3.3010 against $\ln 27$), trap no tanh, ladder edge the context `...` (first-letter chances from the supplied weights), ladder bits saved over the bigram, code `mlp_forward`, code `mlp_dev_loss` on the supplied weights, transfer sector embeddings. 15 min | 3 |
| `l8-minibatches-and-rates.json` | 10: problem 5,704 minibatch steps a full step, explore the recorded 40,000-step run (`series` with a reveal control, bigram line, step-drop line), name minibatch descent and epochs (7.01), ladder the sweep (`bars`), ladder edge a step of 5 diverges, ladder the drop to 0.01 (0.0589), trap one batch is not the loss, explore a live `trainer` (3,000 steps, never graded), code `train_mlp` (autograd), transfer a risk model on sampled days. 15 min | 3 |
| `review-2.json` | 10 items, difficulty 2 to 4, `pass: 0.8`; mk-mlp 6, mk-train 4 | |
| `homework-2.json` | 7 items, difficulty 3 to 5: code `contexts` and `block4_run` (5), `table` three model sizes (4), order the forward pass with a distractor (4), numeric perplexity (3), numeric rows used across a batch (4), longform is the gap real (5, rubric 10), performance code `mlp_forward`, `mlp_loss`, `n_params` (4) | |
| `problems-2.json` | 3 chained problems, 11 parts: a toy alphabet and the name cab (5; l5, l6, l7), a training schedule (4; l8), a lookup and its step (3; l6, l8) | |

New data file: `app/content/data/ai/makemore-mlp.json` (57,838 bytes): the course MLP's weights after 40,000 steps, rounded to 6 places, written by `docs/reports/makemore-L2-numbers.py --write`. It is derived from `names.txt` (MIT, makemore); please add a line to `app/content/data/ai/README.md` (not a course-prefixed file, so not edited here): "makemore-mlp.json: weights of the makemore level 2 MLP, trained on names.txt by docs/reports/makemore-L2-numbers.py".

7 Python code widgets and one trainer; 26 mutants, the taught bug among each widget's (contexts across names, no end row, fancy-index `+=`, joined in the wrong order, no tanh, no `zero_grad`, re-seeding each step, bits for nats). The trainer ships `autograd.py` through `data` (`content/data/ai/autograd.py`) because a trainer has no `files`; the file is the canonical one by reference.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; level 2 warnings: three problem screens without a canvas (hooks and the initialisation question, deliberate), ladder canvas-kind changes and `O2-long-sentence` advisories under 35 words. No `[ai-mutants]` warning.
2. `voice-scan.py 35 --summary`: 0 over 35 words, 0 lesson ids in code spans, 0 doubled words, 0 explanations over three sentences.
3. `docs/reports/makemore-L2-numbers.py` (venv): exit 0, 207 of 207 checks, about a minute (it reruns the 40,000-step run, the sweep, the two 2D runs, five batch seeds and the block-4 run). The 28 "check by hand" lines were read; one found a slip value wrong (problems-2 part 2, 31 for 33), fixed.
4. `grade-all.mjs --code` on the seven files: 72 widgets and 7 code widgets, 0 failures after two mutant test numbers were corrected. Playthrough with `--local-cdn --mobile --why`: all passed (l5 13 checks, l6 13, l7 15, l8 12, quizzes 3/3; review 10 of 10; homework 7 of 7 with the performance starter failing and the longform marked; problems 11 parts, 14 slips routed); l5, l6, l7, review-2 and problems-2 replayed after their last edits. Screenshots at 440 px: three fixes (a code span in a narrow table column stacked its letters; graph labels "context" and "softmax" were cut to "conte..."; the scatter legend sat on points). The trainer was checked natively (60 reports in 2.1 s; the playthrough does not run a trainer). `fresh-check.mjs --file problems-2.json`: 0 hits after rewording one slip line.

## Numbers (route A: NumPy with hand gradients; route B: the autograd for short runs and a row-by-row loop for losses from the supplied weights)

- Dataset: 182,531, 22,807, 22,808 rows (156,905 training letters plus 25,626 names); 5,440 of 19,683 contexts seen; 531,441 cells; after m: a 2,590 of 6,642; after em: i 160, a 140, end 128, m 100 of 769; z in 1 context in 35, so 4 batches in 10 hold none.
- Model: 6,097 weights; initial dev 3.3010; (train, dev) at 200, 1,000, 3,000, 10,000, 20,000, 30,000, 40,000 steps as in the brief; supplied weights train 2.1356, dev 2.1609, test 2.1742 (vectorised and row by row agree to 1e-9); 0.4191 bits a letter saved over the bigram; perplexity 8.68; first letters from `...`: a 0.1502, k 0.0992, m 0.0811, s 0.0722, j 0.0702 (training share of a 0.1358).
- Sweep after 1,000 steps: 3.0666, 2.6407, 2.4249, 2.4190, 2.4529; step 5: first losses 3.28, 7.93, 7.93, dev above 30 (order-sensitive, 31.89 to 44.33). Five batch seeds at step 0.1: 2.4249, 2.4160, 2.4226, 2.4321, 2.4314. Batch losses at steps 196 to 200: 2.6831, 2.5913, 2.3616, 2.5334, 2.2918. 200 autograd steps give the same batch losses as the hand gradient, train 2.5816.
- 2D embedding: dev 2.32 and 2.33 for init seeds 0 and 3; vowels' mean pairwise distance 1.29 and 1.24 against 1.83 and 2.06 for consonants.
- Block 4: 3.2937 at the start, 2.5619 after 200 steps. Sizes: 6,097, 3,481, 22,059, 4,083, 2,062. Planted forward: $h = (-0.4621, -0.8854)$, logits $(-0.9048, 0.4621, -1.5708)$.

## Conventions

The MLP and its split, initialisation and batches are the brief's. The supplied weights are the single source of every stated MLP loss; the number script reruns the training and requires agreement with the file to 1e-3, since BLAS sums may differ between machines. Graded training: 200 minibatch steps with thresholds (below 2.65; recorded 2.5816), run once through a memoised postlude helper. No ops module was needed: `autograd.py` has indexing, `reshape`, `tanh`, `@` and `cross_entropy`.

## Brief notes

- l5 edge case: the brief says jo gives "three rows, two with padding", but all three contexts (`...`, `..j`, `.jo`) hold a start mark; the screen says so.
- The brief calls the `trainer` pending; it has landed, so l8 has one trainer screen and the recorded curve.

## Proposed course.json change

None.

## Exact short-run tests (AUTHORING section 9, rule added at 6c79d9c5)

Every widget of the level that trains carries a seeded short run compared exactly: `train_mlp` (l8) checks two steps on a planted model to 6 places (losses and two weights), and `block4_run` (homework) now also checks 5 steps on the first 12 training names to 6 places (2.809033, recomputed with the hand gradient and with the autograd in the number script). Level 1's `train_bigram_net` already checks two steps on a planted list exactly.
