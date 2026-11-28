# representations level 1: performance task

- `homework-1.json`, item `h-similar-stocks`, index 0. Kind `code` (Python, difficulty 5).
- Matched objective: l4 "Build stock embeddings from return co-movement, and compare them with sector labels." (also l2 "Write cosine similarity for a whole table at once, and say why length is divided out.").
- Task: from a one-line stub, `similar_stocks(R, k, dim, seed)` builds the correlation matrix from a days-by-stocks return array, fits an embedding of width `dim` (any method; the level's off-diagonal fit works), and returns each stock's `k` nearest other stocks by cosine, ties to the earlier stock, with a length guard (a row shorter than 0.25 gets no list and is never listed).
- 8 hidden tests, 1 example, all on `factor_returns` data from `representations_ops_l1.py`: the shape; no stock lists itself; same-sector share of neighbours at least 0.85 on seeds 7 and 12 (recorded 0.97 to 1.0 on seeds 7 to 16, for the fit and for an eigenvector embedding alike); a duplicate stock (each the other's nearest, exact); a stock with no factor (empty list, never listed, `k` = 30 so a missing column guard shows); both together; an answer unchanged when each stock's returns are shifted by a constant (catches a missing demean). Five mutants: no length guard, self left in, no demeaning, covariance for correlation, row guard without the column guard.
- Overlapping screens: l2 screens 9 and 10 code `cosine` and `cosine_matrix`, l3 screen 9 codes `top_k` (screens counted from 0), l4 screens 9 and 10 code `corr_from_returns`, `sector_recovery` and `fit_embeddings`, each with its scaffold; the task joins them from nothing, adds the length guard that l2's zero-row screen and l4's lone-stock screen only discuss, and is tested on universes no screen uses (a twin, a lone stock, shifted returns).

Gates:
1. `node tools/validate.mjs`: 0 errors.
2. `VOICE_BASE=app/content/courses/representations python3 docs/reviews/voice-scan.py 35`: 0 over 35 words and 0 lesson ids in code spans.
3. Numbers script `docs/reports/representations-L1-numbers.py` (venv, `ZQ_NUMBERS_STRICT=1`): 303 of 303 checks, exit 0; it reruns the solution against every test and reruns the tests with an eigenvector twin, which also passes.
4. Playthrough `--set representations/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: all passed, the starter fails. Desktop time per hidden test in Pyodide: 8 to 14 ms.
