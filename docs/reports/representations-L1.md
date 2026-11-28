# representations level 1 (Embeddings): report

Branch `ai-w4-representations` from `f9616b05`. Brief: `docs/briefs/representations.md` Level 1. Generators and helpers: scratchpad `representations-1/` (`gen_l1.py` to `gen_l4.py`, `gen_sets.py`, `lib.py`, `timing.mjs`).

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l1-a-table-of-vectors.json` | 12: problem which pair stays close in two runs (makemore L2's recorded 2D tables, `scatter` with a run control), explore what an axis means, name the embedding and a one-hot product by hand (`matrix`, `table` widget), ladder lookup cost (15,000,000 multiplications), ladder only looked-up rows get gradient (`multi`), ladder widths (2, 10, 300; word2vec 900 million numbers), trap spin the table (dev loss 2.1609 unchanged), ladder edge a row that never trained, generalise $\mathbf{H}\mathbf{E}$ and $\mathbf{H}^\top\mathbf{G}$, code `one_hot`, `one_hot_lookup`, `embedding_grad` (autograd), code `nearest_rows`, transfer a stock identifier as input (13,824 weights). 14 min | 3 |
| `l2-cosine-similarity.json` | 12: problem same direction, different length (distance 4 against 1.41), explore stretch a vector (live caption), name cosine (0.8), ladder every pair at once ($-0.3162$), ladder back to the letters (z's short row), ladder demeaned returns (0.3 against raw 0.6128), trap normalising columns (1.7), ladder edge a zero row, generalise $\hat{\mathbf{E}}\hat{\mathbf{E}}^\top$, code `cosine`, code `safe_normalise` and `cosine_matrix`, transfer two funds' holdings (0.774). 15 min | 3 |
| `l3-nearest-in-the-space.json` | 12: problem five neighbours of a (`bars`), explore four queries (frames), name top $k$ (heat `matrix`), ladder ties and twins, ladder analogy on a supplied firms table (hedged), ladder recall at 3 (0.5), trap close is not caused, ladder edge many dimensions (`bars` histograms, spread 0.058 at 300), generalise the search and recall, code `top_k` and `recall_at_k`, code `analogy`, transfer stocks like this one (6 of 30 exact partners hold, 28 sectors). 15 min | 3 |
| `l4-embedding-stocks.json` | 12: problem groups you cannot see (12 of 30 stocks, heat `matrix`, shuffled and sorted frames), explore the rows in a picture (three aligned fits), name the low-rank fit (3 by 3 loss 0.0038), ladder train it (loss curve, typical error 0.019), ladder neighbours find sectors (29 of 30), ladder $k$-means (`table`), trap in and out of sample (stock 9 changes sector), ladder edge a lone stock (row 0.07, top cosine 0.90 on correlation 0.09), generalise the loss and gradient, code `corr_from_returns` and `sector_recovery`, code `fit_embeddings` (autograd), transfer data groups against official labels. 15 min | 3 |
| `review-1.json` | 10 items, difficulty 2 to 4, `pass: 0.8`, all four lessons | |
| `homework-1.json` | 8 items, difficulty 3 to 5: performance code `similar_stocks` (5), code `nearest_for_queries` (4), order why a cosine is a correlation with two distractors (4), longform buying stock embeddings (5, rubric 10, two required rows), numeric weights (3), numeric a guarded matrix (4), numeric one analogy (4), numeric against the background (3) | |
| `problems-1.json` | 3 chained problems, 12 parts: returns, demeaning and the nearest of three (l2, l3; 3), a fitted table, a lookup, an implied correlation and gradient rows (l1, l4; 4), search, a short row, the guard and recall (l2, l3, l4; 5) | |

New data file: `app/content/data/ai/representations_ops_l1.py` (ops module, v1.0, NumPy only). Reused: `makemore-mlp.json` (the trained $27 \times 10$ letter table `C` and the MLP, for the spin and the letter neighbours), `autograd.py` (byte-identical, SHA-256 `5917d4ec91f7...`, shipped by path through `data`), and makemore l6's recorded 2D runs (copied coordinates; the number script checks they are unchanged).

10 Python code widgets, 36 mutants (the taught bug among each widget's: fancy-index `+=`, distance for cosine, columns for rows, no zero guard, no `zero_grad`, the diagonal left in, no demeaning, no length guard). Every training or search widget has an exact seeded test: `fit_embeddings` 5 and 3 steps to 6 places; searches compared exactly.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors. Level warnings: ladder canvas-kind changes, `O2-long-sentence` advisories under 35 words.
2. `voice-scan.py 35 --summary` with `VOICE_BASE` the course folder: 0 over 35 words, 0 lesson ids in code spans, 0 doubled words, 0 explanations over three sentences.
3. `ZQ_NUMBERS_STRICT=1 docs/reports/representations-L1-numbers.py` (venv): 304 of 304 checks, coverage 0 uncovered with 5 literals, exit 0, about 5 s. The 25 "check by hand" byKey lines were read; none states a wrong number. The script found one false figure, fixed: l2's funds dot product was printed as 13,000; it is 11,500 (the stored cosine 0.774 was right).
4. `grade-all.mjs --code` on all seven files: 78 widgets and 10 code widgets, 0 failures (solutions pass, starters fail, each mutant fails its named test). Playthrough with `--local-cdn` desktop: all passed (each lesson 15 checks, quizzes 3/3; review 10 of 10; homework 8 of 8, performance starter fails, longform marked; problems 12 parts, 12 slips routed with `--why`). With `--mobile --why`: all passed (end of this report). `fresh-check.mjs --file` on review, homework and problems: 0 hits (two retold lines in problems-1 reworded); one advisory on problems-1 (four shared small parameters with a stage-2 item, coincidence).

## Timing (Pyodide 0.27.7 under node, desktop)

Per hidden test: `fit_embeddings` 300 autograd steps of the $30 \times 3$ fit 74 to 76 ms (the 5-step exact run 3 ms); `similar_stocks` 8 to 14 ms; the 27-row letter searches 25 to 33 ms (file read included); every other case 0 to 8 ms. Every graded case is under 0.1 s, at least 13 times inside the 1 s rule; the two fit cases also carry `budget: 4000` for a phone.

## Numbers and their sources (route A generator, route B number script)

- l1: run distances a to e 0.95 and 1.38, a to t 3.61 and 3.12 (makemore l6 coordinates, pure Python); one-hot product $(-0.7, 0.8, 2)$ (loop); $50{,}000 \times 300$; gradient rows (loop); $3 \times 300$; dev loss 2.1609 before and after a seeded $10 \times 10$ rotation with the block-transposed first layer (makemore split, 22,807 rows; equal to $10^{-9}$); nearest a by distance e, z, t, k, o (loop); 13,824 weights.
- l2: 4 and $\sqrt 2$ (Fractions); 0.8; $\mp 1/\sqrt{10}$; z's row 1.93 the shortest, cosine neighbours o, e, u, t, k (loops); 0.3 (Fractions and `np.corrcoef`), raw 0.6128; 1.7 (Fractions); funds 0.774 from 11,500, 3,400, 65,000.
- l3: top-5 lists and values for a, e, o, p (loops); i at rank 8 (0.079); vowel recall 0.2, 0.5, 0.6 at 1, 3, 5 (Fractions); analogy Small Tech at 0.993 (seeded table, loop); random-direction spreads 0.70, 0.33, 0.057 against $1/\sqrt d$; 6 and 28 of 30 (hand gradient against autograd).
- l4: loss 0.1440 to 0.00035, typical error 0.019, loss curve every 10 steps (hand gradient against autograd, equal to $10^{-9}$); recovery 29 of 30 (0.967), seeds 7 to 16 from 0.967 with typical error at most 0.0193 (thresholds 0.9 and 0.03 hold with margin); scikit-learn KMeans 29 of 30; stock 9's neighbours 1 then 20 and mean correlations by sector and half; lone row 0.07 against 0.65 to 0.83, top cosine 0.90 with stock 27 at correlation 0.09; 3 by 3 loss 0.0038 (Fractions); the 12 by 12 block equals `np.corrcoef` to 1 place.
- Sets: every key and slip recomputed by loops or Fractions; the performance threshold 0.85 holds from 0.967 on ten seeds by the model solution and by an eigenvector twin.
- Literals (5): the vendor's 3,000 stocks and 64 numbers, fund Y's £150m holdings, the trap's 200 stocks, the homework's 5,000 stocks (scenario figures).

## Conventions

- Seeds: `factor_returns(7)` for the lesson universe (30 stocks, sectors of 10, 500 days, stock 9 switching from sector 0 to sector 2 at day 250); seeds 7 to 16 for thresholds; fit start `0.1 * default_rng(seed).standard_normal((n, dim))`, step 10, 300 steps, loss the mean over $i \ne j$.
- Cosine with a zero vector is 0 by the guard, and a search reports no neighbours for such a row; this matches `llm-apps` L1 (a zero query returns no results). `top_k` and `recall_at_k` keep the names and meaning `llm-apps` L1 uses (recall: share of known pairs found in the top $k$).
- Notation: $\mathbf{E}$ for the table (makemore's $C$ named once), $\hat{\mathbf{E}}$ row-normalised, $\mathbf{S} = \hat{\mathbf{E}}\hat{\mathbf{E}}^\top$.

## Deviations from the brief

- Adam (`nn-train` L1) is not used: that course is not written and level 1 does not require it. l4 trains with plain gradient descent through the autograd and says later optimisers need fewer steps.
- No ops for the autograd were needed (indexing with `np.add.at` backward is in v1.0). The brief's `rp_ops.py` is replaced, per `docs/briefs/ai-strand-interfaces.md`, by `representations_ops_l1.py`, which holds only the data generator.
- l4's hook shows 12 of the 30 stocks (heat cells at 440 px; inbox bullet).
- The l1 hook reuses makemore L2's two recorded 2D runs and asks a new question (which pair stays close, then what an axis means), so the level studies the table rather than reteaching the lookup.

## `representations_ops_l1.py` (v1.0)

- `__version__ = "1.0"`
- `factor_returns(seed=7, days=500, lone=False, twin=False) -> (R, sectors)`: `R` days by stocks, `sectors` integer labels. 30 stocks in 3 sectors of 10; return = market move $\times U(0.7, 1.3)$ + sector move $\times U(0.7, 1.3)$ + noise 1.2%, moves of spread 1%; stock 9 trades as sector 2 from day `days // 2` (label stays 0). `twin=True` appends a copy of stock 0 (label 0); `lone=True` appends a noise-only stock of spread 1.5% (label $-1$). The first 30 columns never depend on `lone` or `twin`.

## Proposed course.json change

None. (A note for level 2's author: `nn-train/L1` is required there, not here, which matches the decision not to use Adam in level 1.)

## Playthrough with --mobile

All seven files with `--mobile --why --local-cdn <pkgs>` (desktop and 440 px): all passed. l1 to l4 15 checks each, quizzes 3/3; review-1 10 of 10; homework-1 8 of 8, 37 of 37 marks, performance starter fails, longform marked by the button; problems-1 12 parts, 12 typed slips routed (replayed after its last edit, with and without `--mobile`). Screens read at 440 px: the 12 by 12 heat matrix, the letter scatter and the firms table fit; no layout fixes were needed. `perf-reports.mjs` reports no missing part for this level.
