# representations level 5 (Graph networks): report

Branch `ai-w6-representations` from `60c0c2d8`. Brief: `docs/briefs/representations.md` Level 5. Generators and helpers: scratchpad `representations-5/` (`lib5.py`, `common5.py`, `layout5.py`, `calc20.py`, `gen_l17.py` to `gen_l20.py`, `gen_sets5.py`, `timing5.mjs`, `val.sh`, `play.sh`).

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l17-graphs-as-matrices.json` | 12: problem fill rows A and D of $\mathbf A$ from `markov` l14's venues (`table` widget on a `graph`), explore add a link and watch two entries change (`pair` of `graph` and `matrix` heat, frames), name $\mathbf A$, degrees and $\mathbf D$ (3, 2, 2, 1, total 8), ladder $\mathbf A\mathbf x$ sums (10), ladder $\mathbf D^{-1}\mathbf A$ averages (3.33, the walk's step matrix), ladder self-loops and $\hat{\mathbf A}$ on the path 1, 2, 3 (degrees 2, 3, 2; 0.408), trap a node that forgets its own value (4, not 5.5), ladder edge an isolated venue, generalise symmetric with top eigenvalue 1 (similar matrices: same eigenvalues, not eigenvectors), code `adjacency` and `row_normalised`, code `normalised_adjacency` (path, isolated node, input unchanged), transfer banks P and Q (0.204). 14 min | 3 |
| `l18-passing-messages.json` | 12: problem predict one step from 1 at D (frames after the check), explore many steps settle at $\tfrac18 = \pi_D$, name a message-passing step and the walk's expectation (B gets 3), ladder $k$ looped steps reach $k$ links (`tap-regions`), ladder probability by $\mathbf P^\top$ against values by $\mathbf P$ (1 against $\tfrac13$), ladder vector features (6), trap arrows follow $\mathbf A$ not $\mathbf A^\top$ (9), ladder edge the square swaps for ever ($\tfrac12$ at step 100; $\tfrac14$ with loops), generalise $\mathbf P^k\mathbf x \to (\boldsymbol\pi^\top\mathbf x)\mathbf 1$ (2.5), code `message_step` and `k_steps`, code `settles`, transfer stress in a funding network (0.1). 14 min | 3 |
| `l19-a-gcn-layer.json` | 11: problem mix node 1's neighbourhood by hand on a 20-node, two-community graph (`pair` of `graph` and `table`; $(-0.51, 0.32)$), ladder name the layer and apply $\mathbf W_1$ and ReLU $(0, 1.84)$, ladder node 4 start to finish (3.19), ladder weight count does not grow with nodes (64), ladder two layers see two links (`tap-regions`), trap weights first or averaging first (same layer; ReLU is what matters), ladder edge a firm with only its self-loop (5.7), generalise, code `gcn_layer` and `gcn_layer_loop`, code `gcn_forward` and `gcn_params`, transfer a firm and its supply chain (2.68). 15 min | 3 |
| `l20-labels-on-a-graph.json` | 12: problem guess firm 3's label from its links on 40 firms, explore $\hat{\mathbf A}^k\mathbf X$ separates the clouds (`scatter` frames), name semi-supervised node classification ($\tfrac{35}{36} \approx 0.972$), ladder the per-node network (21 of 36; 14 more; means 0.95 and 0.60 over 20 graphs), trap accuracy on the four training firms, ladder over-smoothing ($\hat{\mathbf A}^k\mathbf X\mathbf W$: 0.65, 0.87, 0.91, 0.96, 0.97, 0.90, 0.77, 0.61, 0.50 for $k$ = 0 to 128; 16 ReLU layers 0.55), ladder edge links that ignore labels (0.57 against 0.60), generalise the objective and the $\sqrt{\tilde d_i}$ limit (0.426), code `planted_partition`, code `train_gcn` (exact 5-step losses; threshold 0.85), code `feature_spread`, transfer sectors of unlisted firms. 15 min | 3 |
| `review-5.json` | 9 items, difficulty 2 to 4, `pass: 0.8`, all four lessons | |
| `homework-5.json` | 8 items, difficulty 3 to 5: performance code `gcn_node_classifier` (5), code `nodes_within` (4), order the $\sqrt{\tilde d_i}$ eigenvector with two distractors (4), longform a graph network for defaults (5, rubric 10, two required rows), numeric a ring of banks (3), numeric two links out (4), choice two normalisations (3), multi do the links carry signal (4) | |
| `problems-5.json` | 3 chained problems, 12 parts: a square with a diagonal, its $\hat{\mathbf A}$, one mixed value and one layer (l17, l19; 4); a path, plain steps that swap, the looped limit, the eigenvector ratio (l18, l20; 5); three credit grades, weights, honest accuracy, the per-node gap, shuffled links (l19, l20; 4) | |

New data file: `app/content/data/ai/representations_ops_l5.py` (v1.0, 3,613 bytes, SHA-256 `5e58fe8c902e...`). No other data file: every graph and feature matrix is generated from a stated seed by that module, so nothing needs a licence. Provenance line for the data README: "`representations_ops_l5.py` generates this level's planted-partition graphs and node features from stated seeds; no third-party data." Reused byte-identical: `autograd.py` (v1.0, `5917d4ec91f7`), `nt_ops_l1.py` (`9c1391a33624`); `representations_ops_l1.py` is untouched (`097ac4d78867`). 11 Python code widgets, 47 mutants (the taught bug among each: one direction of a link, no self-loops, $\tilde{\mathbf D}^{-1}\tilde{\mathbf A}$ for $\hat{\mathbf A}$, $\mathbf P^\top$ for $\mathbf P$, two steps at a time, no self term in the loop over neighbours, ReLU on the scores, training-node accuracy, labels of every node in the loss, gradients never zeroed, entrywise powers, $\mathbf A^k$ for $k$ links). Both training widgets have exact seeded short-run tests (`train_gcn` 5 and 4 steps, `gcn_node_classifier` four 3-step runs, to 6 places).

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors. Level warnings are only `O2-long-sentence` advisories (27) and ladder canvas-kind changes.
2. `VOICE_BASE=app/content/courses/representations python3 docs/reviews/voice-scan.py 35 --summary`: 0 over 35 words, 0 lesson ids in code spans, 0 doubled words, 0 explanations over three sentences.
3. `node tools/run-number-scripts.mjs --only representations-L5` (strict): 312 of 312 checks, 0 uncovered, 5 literals (two scenario counts, a test width, test settings, the review's 30 layers), exit 0, about 5 s.
4. Playthrough with `--local-cdn`, desktop and `--mobile`: all seven files passed (end of this file). `grade-all.mjs --code` on all seven files: 0 failures (solutions pass, starters fail, every mutant fails its named test in Pyodide). `fresh-check.mjs --file` on review, homework and problems: 0 hits. `same-course-reuse.mjs --all`: no error for level 5 files. `perf-reports.mjs`: `representations-5-perf.md` has every part.

## Timing (Pyodide 0.27.7 under node, desktop, per hidden test)

`train_gcn` 200 steps 84 to 98 ms; `gcn_node_classifier` 200 steps 74 to 97 ms (the leakage test runs two 60-step fits in 48 ms); `gcn_layer_loop` on 20 nodes 17 ms; every other case under 10 ms. No case needs a `budget`: the slowest is under 2% of the 5 s limit, so a phone 5 times slower stays under a tenth.

## Numbers and their sources (route A generator, route B number script)

- l17: degrees, $\mathbf A\mathbf x$, $\mathbf D^{-1}\mathbf A\mathbf x$ and the trap by Fractions; every $\hat{\mathbf A}$ entry (path, venues, heat cells, banks, star) entry by entry from $1/\sqrt{\tilde d_i\tilde d_j}$; top eigenvalue 1 by `eigvalsh` and the eigenvector along $\sqrt{\tilde d}$ by power iteration; 14 entries for 7 links.
- l18: every frame value (hook, 40 steps, the square without loops, with loops at step 6, the contagion) by exact Fraction steps; $\tfrac18$, 2.5 and $\boldsymbol\pi$ by Fractions; the two-step reach by looped Fraction steps; quizzes 4.5 and 1.6.
- l19: the graph by a double loop over the seeded table; node 1's weights and mixed row, node 4's, the isolated firm, the supply-chain sum by loops over neighbours; the supplied network labels all 20 nodes (independent forward pass); 64, 352, 3,424 and the slips by arithmetic.
- l20: every trained figure retrained by a hand-written forward and backward pass with a hand-written Adam (any depth): 35 and 21 of 36 on the lesson's graph, the means over 20 graphs (0.953, 0.596, no signal 0.571), the linear $k$-step accuracies, 16 layers 0.547; the eigenvector ratio $\sqrt{2/11} \approx 0.426$ and the spreads by power iteration; the scatter frames by matrix powers.
- Sets: every key by Fractions, loops or iterated steps (the review's limit 3, the ring's 2.8 and the path's $\tfrac{12}{7}$ by 200 to 300 averaging steps), closed forms checked against them.
- Code: every hidden test of the 11 widgets rerun in CPython with the model solution and with an independent twin (loops, Fractions, matrix powers, the hand-backprop trainer, power iteration); each graded threshold checked on four seeds with margin (`train_gcn` and the classifier at least 0.9 against 0.85; isolated node at least 0.85 against 0.8; no-signal graphs at most 0.7 against 0.75). `gcn_logits` and its training loss are gradient-checked through the autograd (relative error about $10^{-11}$), and `train_gcn_params` matches the hand trainer over 30 steps to $10^{-9}$.

## Conventions

- Graphs: `planted_partition(n, p_in, p_out, seed)`, nodes $0$ to $n/2 - 1$ in community 0, one table `default_rng(seed).random((n, n))` read above the diagonal. l19: $n = 20$, 0.35 and 0.05, seed 9, features rounded to 1 decimal from seed 509; l20: $n = 40$, 0.3 and 0.03, seed 13, features seed 113 (graph seed + 100 throughout), labelled firms 0, 1, 20, 21; no-signal graphs link every pair with 0.165.
- Features: `node_features(y, shift=0.6, seed)`, standard normal, first column moved by $\mp 0.6$.
- Network: no biases; weights $N(0, 1/\text{fan-in})$ from `default_rng(seed)` in layer order; ReLU between layers, none after the last; Adam (`nt_ops_l1.adam_step`, 0.05) on the mean cross-entropy of the labelled nodes, 200 full-batch steps, hidden width 16 (2 in l19's supplied network, $\mathbf W_1 = [[4.2, -2.5], [-3.6, 1.8]]$, $\mathbf W_2 = [[-4.4, 4.3], [3.2, -1.7]]$, trained and rounded to 1 decimal).
- Over-smoothing measure: the share of $\hat{\mathbf A}^k\mathbf X$ outside the top eigenvector, $\lVert\mathbf Z - \mathbf v\mathbf v^\top\mathbf Z\rVert / \lVert\mathbf Z\rVert$ (a spread across nodes would not reach 0 under $\hat{\mathbf A}$, since the limit rows still scale with $\sqrt{\tilde d_i}$).

## Deviations from the brief

- `train_gcn` returns `(accuracy on the other nodes, losses)` and `gcn_node_classifier` returns `(predictions, losses)`, so each can carry the exact short-run test the learning-loop rule asks for; predictions alone are too coarse to compare exactly.
- Over-smoothing is shown with the linear model $\hat{\mathbf A}^k\mathbf X\mathbf W$ (one weight matrix, $k$ averaging steps), which isolates the averaging. A ReLU stack mixes over-smoothing with training trouble: in this script's runs 2 to 8 ReLU layers score about the same and 16 layers fall to 0.55, which the lesson states with both causes named.
- The brief's homework code item "how far a deep network sees" is `nodes_within(A, i, k)`; `receptive_field` was taken by `cnn` l7 (fresh-check code-name hit).
- No autograd op was missing: a dense adjacency product is `ndarray @ Tensor` through `__rmatmul__`.

## `representations_ops_l5.py` (v1.0): public names

- `planted_partition(n, p_in, p_out, seed) -> (A, y)`.
- `node_features(y, shift=0.6, seed=0) -> X` (n by 2).
- `normalised_adjacency(A) -> A_hat`.
- `gcn_init(sizes, seed=0) -> [W1, W2, ...]`.
- `gcn_logits(A_hat, X, params) -> Tensor` (arrays or `Tensor`s; gradient-checked to relative $10^{-6}$).
- `train_gcn_params(A_hat, X, y, train_idx, layers=2, hidden=16, steps=200, lr=0.05, seed=0) -> (params, losses)`.
- `predict(A_hat, X, params) -> integer array`.

## Proposed course.json change

None.

## Backlog

Four bullets under "Raised later (representations level 5)" in `docs/BACKLOG-INBOX.md`: a force layout for `graph`, small-node labels, the `scatter` frame array form that draws NaN circles, and a stacked `pair` of `graph` and `matrix`.

## Playthrough with and without --mobile

All seven files with `--local-cdn <pkgs>`, desktop and `--mobile` (440 px): all passed. l17 15 checks, l18 15, l19 14, l20 15, quizzes 3/3 each; review-5 9 of 9; homework-5 8 of 8, 37 of 37 marks, the performance starter fails, the longform marked by the button; problems-5 12 parts with `--why`, 21 typed slips routed. Screens read at 440 px and desktop: the venue table, the 20-node tap screen (re-laid out after the first pass ran an edge behind node 1), the 40-node graphs (labels on six firms only), the scatter frames, the bar charts and the stacked pairs fit without overlap.
