# makemore level 1 (Bigrams): report

Branch `ai-w3-makemore` (from `bd99bc2c`, fast-forwarded to `caf31d32` for engine 1266 before the final playthrough).

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l1-counting-pairs.json` | 11: problem last letter (`console` of the file head), explore `.emma.` pairs (`array` stepper), name the bigram table (`matrix` slice rows start, a, n, e by columns end, a, e, n, with heat), ladder three names by hand (`table` widget), ladder 228,146 pairs, ladder the start row (`bars`), ladder edge: the 102 empty cells and the one empty by construction, trap no marks, generalise the loop and `N[14, 0]`, code `bigram_counts`, transfer up and down days (`matrix`). 14 min | 3 |
| `l2-the-counts-are-best.json` | 12: problem two rows for q (`bars` groups), explore slide the chance of u (derive caption of the log-likelihood), name the MLE, derive (`order`, one distractor: per-cell derivatives), 4 ladders (row a, the coin inside the row, add-one, dev loss against alpha on `bars`), trap whole-table normalising, edge: unsmoothed dev loss infinite (the 7 unseen pairs), code `bigram_probs` and `nll`, transfer down after two down days. 15 min | 3 |
| `l3-one-loss-two-units.json` | 10: problem equal chances $\ln 27$ (`number-line`), explore nats and bits (derive), name cross-entropy and perplexity (info l7, l8 reused), ladder emma by hand (`table` widget), ladder bits saved on dev, trap bits against nats, ladder edge jo (start and end pairs 0.73 of its loss), generalise the yardstick, code `loss_report`, transfer a claim of 0.01 nats. 14 min | 3 |
| `l4-bigram-as-network.json` | 11: problem what loss can descent reach, explore one-hot times a matrix (`matrix` with a `frames` control), name logits, softmax, `cross_entropy`, ladders one step by hand and a row used twice (planted 3 symbols, 4 pairs), ladder the recorded run (`plane` polyline, dashed counts 2.3820), ladder rows of $W$ as log counts ($\ln(110/51)$), trap better than the counts, ladder edge `W[xs]` is the one-hot product, code `train_bigram_net` (autograd shipped), transfer one day of memory. 15 min | 3 |
| `review-1.json` | 10 items, difficulty 2 to 4, `pass: 0.8`; mk-bigram 5, mk-loss 3, mk-train 2 | |
| `homework-1.json` | 7 items, difficulty 3 to 5: code `best_alpha` (5), code `top_start` (4), order MLE proof with a distractor (4), numeric alpha 0.5 (3), numeric log ratio (4), longform why the network cannot win (5, rubric 10), performance code `bigram_model` and `avg_nll` (4) | |
| `problems-1.json` | 3 chained problems, 13 parts: eight new names (5; l1, l2, l3), four symbols and one step (4; l2, l4), a second split from seed 5 (3; l2, l3) | |

7 Python code widgets, 32 mutants, the taught bug among each widget's (no end mark, rows and columns swapped, whole-table normalising, unseen pair skipped, bits for nats, sum for average, no `zero_grad`).

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors. Level 1 warnings: one problem screen without a canvas (l4 hook, deliberate: the canvas would give the answer), four "ladder reuses the previous canvas kind" (array, bars and matrix views of one table), and `O2-long-sentence` advisories (all under 35 words). No `[ai-mutants]` warning.
2. `voice-scan.py 35 --summary` on the course folder: 0 over 35 words, 0 lesson ids in code spans, 0 doubled words, 0 explanations over three sentences.
3. `docs/reports/makemore-L1-numbers.py` (venv): exit 0, 375 of 375 checks; the 49 "check by hand" lines were read and each states the working of its slip.
4. `grade-all.mjs --code` on the seven files: 76 widgets and 7 code widgets, 0 failures. Playthrough with `--local-cdn --mobile --why`: all passed (l1 14 checks, l2 15, l3 13, l4 14, quizzes 3/3 each; review 10 of 10; homework 7 of 7 with the performance starter failing and the longform marked; problems 13 parts, 15 typed slips routed). Screenshots read at 440 px: two fixes (l1 hook said "on the right"; l3's three-part display formula scrolled, now one display and a sentence). `fresh-check.mjs --file problems-1.json`: 0 hits after rewording three slip lines that repeated l3, l4 and review lines.

## Numbers (each computed twice: NumPy arrays with `np.add.at` against a `Counter` of pairs; autograd against a hand-written gradient)

- File: MD5 matches; 32,033 names, 196,113 letters, 228,146 pairs; split sizes 25,626, 3,203 and 3,204, first training names briah, xzayvion, amad. Last letters n 6,763, a 6,640, e 3,983, y 2,007; first letters a 4,410, k 2,963, m 2,538; start row and end column 32,033; row a 33,885 (the a's); 102 zero cells (109 on the training names), start then end among them; start then q 92; 65 two-letter names.
- Slice: start (0, 4,410, 1,531, 1,146), a (6,640, 556, 692, 5,438), n (6,763, 2,977, 1,359, 1,906), e (3,983, 679, 1,271, 2,675).
- l2: row q 272 (u 206, end 28, a 13, i 13, other 12); log-likelihoods $-237.43$ (shares) and $-260.49$ (row A); peak at $206/272 = 0.757$; $28/272 = 0.1029$; $5{,}438/33{,}885 = 0.1605$; $6{,}640/33{,}885 = 0.1960$; $1/299 = 0.00334$; dev sweep 2.4520, 2.4514, 2.4514, 2.4606, 2.5507 (0.1 is 2.451380 and 1 is 2.451413); row n 18,327, $18{,}327/228{,}146 = 0.0803$; 7 unseen dev pairs (tzvi, zvi, siegfried, comfort, maxmilian, noahh, omkar); $7/11$; row v 2,573 (end 88, a 642).
- l3: 2.4546 nats, 3.5412 bits, 11.64; $\ln 27 = 3.2958$; emma 12.5716 total, 2.5143 a pair; train, dev, test 2.4536, 2.4514, 2.4702 (bits 3.5398, 3.5366, 3.5637; perplexity 11.6304, 11.6047, 11.8245); 1.2182 bits saved on dev; 3.50 bits = 2.4260 nats; jo costs 2.5826, 1.8079, 2.2300, start and end share 0.73 (emma 0.37).
- l4: 3,610 pairs; losses 3.7441, 2.6236 (10), 2.4387 (50), 2.4122 (100), 2.3830 (3,000); counts 2.3820 unsmoothed, 2.4554 add-one; step 0.1 gives 3.7007 after 50; n then end 110, n then a 51, trained gap 0.7687 = $\ln(110/51)$; planted step: $W_{0,1} = 0.1667$, $W_{1,1} = -0.1667$, loss 1.0986 to 0.9805; softmax $(1, 0, -1)$ gives 0.6652, loss 0.4076.
- Sets: y row 9,776 (a 2,143); x row 697; al 2.3145; 3.40 bits = 2.3567 nats; seed-7 split best alpha 0.3 at 2.4629 (1 gives 2.4630); ma 1,453, ja 1,255, ka 1,254; $206.5/285.5 = 0.7233$; a then end 105, a then n 81, $\ln(105/81) = 0.2595$; eight names: row m 9, $6/36$, may 2.1543 nats, 3.1080 bits, perplexity 8.62; four symbols: $\ln 4$, $-0.4167$, 0.8333, $\ln 2$; seed-5 split: 2.4627, 2.4624, 2.4623, 2.4625, 2.4641, 2.4716, best 0.3.

## Conventions

`.` is index 0 and a to z are 1 to 26 everywhere. Split: `np.random.default_rng(42).permutation(32033)`, train `[:25626]`, dev `[25626:28829]`, test `[28829:]`. `nll` returns `math.inf` for a chance of 0 (stated in the `how`). Graded training: 50 full-batch steps on the 500-name subset, thresholds and the 4-place first loss only; tests memoise one run in the postlude. `autograd.py` ships verbatim in `files` (SHA-256 5917d4ec91f7..., checked by the number script). No ops module was needed for level 1.

## Proposed course.json change

None.
