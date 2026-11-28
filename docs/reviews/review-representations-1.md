# representations level 1 (Embeddings and cosine similarity): second-reader findings

Scope: `app/content/courses/representations/` level 1 (`l1-a-table-of-vectors`, `l2-cosine-similarity`, `l3-nearest-in-the-space`, `l4-embedding-stocks`, `review-1`, `homework-1`, `problems-1`) and `app/content/data/ai/representations_ops_l1.py` (`factor_returns`), at `8cfe50c7`.
Method: `docs/reports/representations-L1-numbers.py` run with the venv Python and `ZQ_NUMBERS_STRICT=1` (304 of 304 checks, 0 uncovered, 5 literals, exit 0, 3 s), its route B read and its five literals spot-checked; `node tools/grade-all.mjs --file <path> --code --local-cdn <pkgs>` on each of the seven files alone (0 failures); 50 wrong solutions, 8 model solutions with the starter's comments kept and 10 correct alternatives run through the real Pyodide harness as `mutants` of scratch copies (appendix); every stated number recomputed in my own scripts (NumPy, Fractions, the makemore dev split, the lesson fits by a hand gradient), including side checks the level does not make (a stretched letter table, row length against letter counts, fits with the diagonal kept, cross-sector cosines of the l4 table); distractors read against their `why`; `voice-scan.py 35 --summary` (0 over 35 words, 0 explanations over three sentences) and a grep for em-dashes, exclamation marks and American spellings (none); the downstream brief `docs/briefs/llm-apps.md` Level 1 read for interface mismatches.
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, teaching issue or a test that misses what it claims; note = style or small gap.

Counts: 7 errors, 18 warnings, 10 notes. Wrong solutions: 9 of 50 survive; 1 of 8 model solutions typed into the starter fails.

## Lessons

- app/content/courses/representations/l1-a-table-of-vectors.json | screens[1] option `none`, screens[6] explain, summary.ideas[0] | error | "Only distances between rows mean anything", "only its geometry is fixed" and "only distances and angles between rows carry meaning" are false for a table that feeds a linear layer. Any invertible map undone by the first layer leaves the model unchanged: stretching column 0 of makemore's table by 5 and dividing the matching rows of `W1` by 5 keeps the dev loss at 2.160942, yet a's five nearest rows by distance go from e, z, t, k, o to k, z, t, o, p and by cosine from o, e, u, t, k to z, s, t, k, c. A rotation is the one change that keeps distances, so the spin proves only that single columns mean nothing. | Option: "Nothing on its own: the model only fixes how rows relate to each other". Explain: "A spin undone by the next layer changes every column and leaves the model as it was, so a column means nothing on its own." Summary: "...single columns carry no meaning; distances and angles survive a spin, but a stretch undone by the next layer would change them too, so neighbours describe this training run and need checking."
- app/content/courses/representations/l1-a-table-of-vectors.json | screens[10] explain | error | "Level 2's next lesson asks whether distance is the right measure": the next lesson is l2 of this level (cosine similarity); level 2 is the autoencoder. | "The next lesson asks whether distance is the right measure for rows of different lengths."
- app/content/courses/representations/l1-a-table-of-vectors.json | screens[0] feedback.correct | note | "a and e: about 1 apart in each run": the hint gives 0.95 and 1.38. | "a and e: 0.95 and 1.38 apart, while t is more than 3 away in both runs."
- app/content/courses/representations/l2-cosine-similarity.json | screens[8] question; screens[0] prose; summary.ideas[0] | error | The level states that frequency sets length: "appears 100 times as often as another, and so has a row 10 times as long", "v is longer because its item came up far more often", "a long, often-seen row". In makemore's own table the link runs the other way: the correlation of row length with log letter count is $-0.35$; u (3,135 uses in names) has a row of 4.74 and a (33,885 uses) 3.08. Length depends on the model and the data, with no square-root law. The number script backs the screen with `claim(10 ** 2 == 100)`. | Question: "An item's row is 10 times as long as another's and points the same way. How does its cosine with any other row change?" Screen 0: "$\mathbf v$ is longer, as rows of some items grow in training." Summary: "a long row looks far from a short one pointing the same way". Drop the claim from the script.
- app/content/courses/representations/l2-cosine-similarity.json | screens[9] how | note | "each compared within relative $10^{-9}$": tests 3 and 4 use an absolute $10^{-12}$ (a relative tolerance cannot pass at 0). | "...within relative $10^{-9}$ (absolute $10^{-12}$ where the answer is 0)".
- app/content/courses/representations/l3-nearest-in-the-space.json | quiz[2] (option `bg`, explain); screens[7] explain; summary.ideas[2] | warning | The background is random directions, but trained tables are not random. In this level's own l4 table, pairs from different sectors have cosines averaging 0.448 (lowest 0.146). "Even unrelated items sit near 0" fails there, and 0.12 at 2.08 spreads is not "a weak but real hint": 3.8% of random pairs pass it, about 1,900 rows for each query in a 50,000-row table. | Compare a cosine with the spread of cosines in the same table: "As a hint at best: compare it with how the table's other pairs score, since many unrelated pairs reach it by chance." Explain screen 7: "...so read a similarity against the rest of the table, not against 1."
- app/content/courses/representations/l3-nearest-in-the-space.json | screens[7] question | warning | It asks for the standard deviation "to 2 places" from three histograms, but the rule $1/\sqrt d$ appears only in hint 2 and the feedback; `stat-learning` l4 does not give it (it warns about distances). A learner cannot read 0.06 off bins of width 0.1. | Name the rule in the prose ("random cosines spread about $1/\sqrt d$") and ask for $1/\sqrt{300}$, or ask which width gives the narrowest histogram.
- app/content/courses/representations/l3-nearest-in-the-space.json | screens[5] prose; summary.formula | warning | Downstream mismatch with `llm-apps` L1: there recall at $k$ is "the share of relevant notes in the top $k$" for each labelled query, and `recall_at_k(ranked, relevant, k)` works on one query; here recall pools all known pairs. The two agree only when every query has the same number of partners: review-1's r-recall is 0.6 pooled but 0.625 as a mean over queries. `top_k(E, i, k)` here also takes a row index and leaves it out, while `llm-apps`' `top_k(query, docs, k)` takes an outside query (homework-1's `nearest_for_queries` is that one). The report's "keep the names and meaning `llm-apps` L1 uses" overstates it. | Add one sentence to screen 5: "Retrieval tools usually average this share over queries; with equal numbers of partners, as here, the two agree." Tell the `llm-apps` author (BACKLOG-INBOX) that `top_k` and `recall_at_k` here differ in signature.
- app/content/courses/representations/l3-nearest-in-the-space.json | screens[1] feedback.correct | note | "letters that stop the sound much as p does" is a story read into five neighbours, the reading the trap screen warns against. | "p: its neighbours are t, c, g, b and k, other consonants."
- app/content/courses/representations/l4-embedding-stocks.json | screens[6] option `s1` why | error | "Sector 1 is the lowest bar in both halves": in the first 250 days stock 9's mean correlation is 0.31 with sector 1 and 0.28 with sector 2 (the bars on the screen; I get 0.310 and 0.276). | "Sector 1's bar falls in the second half; sector 2's is the one that rises."
- app/content/courses/representations/l4-embedding-stocks.json | screens[4] explain | error | "On seeds 7 to 16 the share never fell below 0.97": six of the ten seeds give 29 of 30, 0.967 (seeds 7, 9, 11, 13, 15 and 16; the rest 1.0). The script covers the figure with `round(min, 2)`. | "On seeds 7 to 16 the share never fell below 0.967."
- app/content/courses/representations/l4-embedding-stocks.json | screens[8] (option `len`, its why and the `speed` why, feedback.correct, explain); summary.formula.note | error | The screen says keeping the diagonal "would force every row to length 1" and "give the lone stock a long, meaningless row". On the lesson's own data it does neither: fitted with the diagonal kept (31 stocks, 300 steps), the lone row is 0.088 long against 0.074 without it, and the others 0.675 to 0.843 against 0.648 to 0.827; the eigenvector closed form gives the same 0.088. One diagonal term among 31 in a row barely moves it. | Teach the true reason: the diagonal holds each stock's correlation with itself, 1 by definition, so fitting it spends the table's few numbers on entries that carry no information about co-movement. Option: "The diagonal is 1 for every stock by definition, so it says nothing about how stocks move together". Rewrite the feedback, explain and note to match, and drop "force".
- app/content/courses/representations/l4-embedding-stocks.json | screens[2] explain | warning | "90 numbers to fit 435 pairs, which is why it is called a low-rank fit": low rank names the rank of $\mathbf E\mathbf E^\top$, at most 3 for a $30 \times 3$ table, not the count of numbers. | "$\mathbf E\mathbf E^\top$ has rank at most 3, far below 30, so this is a low-rank fit: 90 numbers stand in for 435 pairs."
- app/content/courses/representations/l4-embedding-stocks.json | screens[3] explain | note | "because three sectors drive them": the model has a market move as well; it fits in three numbers because the market loadings lie close to the sum of the sector directions (eigenvalues 11.1, 4.2, 2.8, then 0.70; a width-4 fit only moves the typical error from 0.0187 to 0.0171). | "...because a market move and three sectors drive them, and three directions hold both."
- app/content/courses/representations/l4-embedding-stocks.json | screens[9] widget test 8 | error | The test fails a correct solution: the starter's comment "(no np.corrcoef)" contains `corrcoef`, so the model solution typed into the starter, comments kept, first fails test 8 (appendix) and is told "Build the matrix from demeaned columns yourself". | Reword the comment ("without NumPy's correlation helper") or test the call, not the text: run `corr_from_returns` with `np.corrcoef` replaced by a function that raises.
- app/content/courses/representations/l4-embedding-stocks.json | screens[9] feedback.byKey test-3, test-1 | warning | test-3 ("should be 30 by 30... Transpose the other way") cannot show for the mistake it names: `X @ X.T` gives a 5 by 5 matrix on test 1 and fails there, with test-1's "Subtract each column's mean" line. Only a non-array return (a list) reaches test 3 first (appendix W6). | Move the shape test to first place with the transpose message, or make test-1's line cover both ("Subtract each column's mean, and multiply `X.T @ X` for stocks by stocks").
- app/content/courses/representations/l4-embedding-stocks.json | screens[10] widget tests 1 and 3 | warning | The first exact run diverges: at step size 10 on the 4-stock matrix the entries reach $-338$ to $-394$ after 5 steps, so the reference is a blow-up, and a learner reading the failed case sees numbers that look like their own bug. test-3's "Check the sign of your step" never shows for a sign flip, which fails test 1 first. (Five correct variants still match to 6 places, so the run is reproducible.) | Use step size 1 for test 1, or 5 steps on `factor_returns(7)`'s matrix, from the number script; reword test-3's line to "300 steps at step size 10 should bring the typical error to about 0.019".

## Review, homework and problem set

- app/content/courses/representations/review-1.json | items[9] explain | note | "Column 2 has length $\sqrt{10}$" counts columns from 1, while the item's entry $(1, 1)$ and l2's labels "col 0, col 1" count from 0. | "Column 1 has length $\sqrt{10}$".
- app/content/courses/representations/homework-1.json | items[7] explain, feedback.correct | warning | "A real signal in this table" for a cosine of 0.35 between two stocks' rows. Return embeddings share a market factor: in l4's table the typical cross-sector pair scores 0.448, above 0.35. Random directions are the wrong background for stocks, the point the item should teach. | "0.35 is 3.5 spreads from random directions, but stock rows share the market, so compare it with other pairs in the same table before calling it a signal."
- app/content/courses/representations/homework-1.json | items[0] tests | warning | Three wrong solutions pass all 8 tests: ranking by the fitted correlation $\mathbf e_i \cdot \mathbf e_j$ instead of cosine (it changes all 30 lists on seed 7), fitting a covariance matrix in percent instead of correlations, and a guard at squared length 0.25. test-3's line names "demean the returns and rank by cosine", but skipping the demeaning first fails test 8 and the dot product passes. | Add a test with each column scaled by a different positive factor (`R * np.linspace(0.5, 3, 30)`, lists must not change), and a planted stock with weak loadings whose row lies between 0.25 and 0.5 long; for the dot product, a planted short row that points like stock 0's. Verify each against the solution in the number script.
- app/content/courses/representations/homework-1.json | items[1] test 3, mutant 2 symptom, byKey test-3 | warning | The test is meant to show a long row winning by dot product, but row 1, $(10, 1)$, is also the cosine winner (0.998765 against 0.998752 for row 0). The dot-product mistake gives `[1, 3, 0]` and is caught only on the order of rows 0 and 3, while its message says "Row 1 is long". | Query `[[1, 0]]`: cosines 1, 0.995, 0, 1 give `[0, 3, 1]`, and the dot product gives `[1, 3, 0]`, so the long row wins only by the wrong measure.
- app/content/courses/representations/problems-1.json | items[2].parts[3] wrong `all`, byKey `all` | warning | The guard does not change this answer. Without it, stock 4's nearest row is stock 1 (cosine 0.918), not stock 0 (0.859), so recall at 1 is 0.8 either way and 1.0 comes from no slip; the byKey implies the guard is what loses the pair $(4, 0)$. | Make stock 4 $(0.05, 0.01, 0)$, parallel to stock 0 (length 0.051; recompute parts 2 and 3). Then the unguarded search finds $(4, 0)$, recall 1.0, and the guard gives 0.8.
- app/content/courses/representations/problems-1.json | items[1].parts[0] wrong `col` | warning | 0.3 has no natural slip: its why says it "sits in column 2 of the table, read from the top", but the table has two columns and the lesson counts from 0, and reading down a column for "the second entry" gives 0.4. | Wrong value 0.4, id `row1`: "You counted rows from 1. Row 2 is the third row, $(0.1, 0.8)$." (l1's own slip).

## Code widgets: surviving wrong solutions and unreachable feedback

- app/content/courses/representations/l1-a-table-of-vectors.json | screens[9] test 7 | warning | The check that `one_hot_lookup` multiplies passes on any `@` in the file: `one_hot_lookup` returning `E[idx]`, with `embedding_grad` written by hand as `one_hot(idx, n).T @ dout`, passes all 7 tests, skipping both the product and the autograd the screen asks for (appendix W2). | Test through `one_hot`: `_oh = one_hot; one_hot = lambda i, n: 2 * _oh(i, n); r = one_hot_lookup(E, [1]); one_hot = _oh` expecting `2 * E[1]`. For `embedding_grad`, either accept a hand gradient or say in the prose that the tests cannot tell.
- app/content/courses/representations/l1-a-table-of-vectors.json | screens[10] tests | warning | "Sort, then drop the first entry" passes all 5 tests. It returns the query itself whenever an identical row comes earlier: for rows $(1, 1)$, $(0, 0)$, $(1, 1)$ and $i = 2$ it gives `[2]`. Test 3 has the duplicate after the query only. | Add `nearest_rows([[1, 1], [0, 0], [1, 1]], 2, 1)` expecting `[0]`.
- app/content/courses/representations/l1-a-table-of-vectors.json | screens[10] byKey test-3 | note | The line is about identical rows, but the named dot-product mutant meets it first and is told about duplicates. | "Rows 0 and 2 are identical, so row 2 is at distance 0 and comes first; rank by distance, not by dot product."
- app/content/courses/representations/l2-cosine-similarity.json | screens[9] tests | warning | A guard on the first vector only passes all 7 tests; `cosine([1, 2, 3], [0, 0, 0])` gives NaN. Test 4 puts the zero vector first. | Add `cosine([1, 2, 3], [0, 0, 0])` expecting 0.0.
- app/content/courses/representations/l2-cosine-similarity.json | screens[10] byKey test-3 | warning | "The diagonal must be 1. Dividing columns leaves rows of other lengths" never shows for column division: dividing columns in `safe_normalise` fails test 1, and in `cosine_matrix` fails test 2 (appendix). | Key the diagonal line to test-2, where column division in `cosine_matrix` lands; column division in `safe_normalise` already meets test-1's line.
- app/content/courses/representations/l3-nearest-in-the-space.json | screens[9] tests | warning | "Sort, then drop the first entry" passes all 7 tests; with a twin before the query it returns the query (test 2's twin, row 3, comes after query 1). | Add `top_k([[1, 0], [0, 1], [1, 0]], 2, 1)` expecting `[0]`.
- app/content/courses/representations/l3-nearest-in-the-space.json | screens[10] byKey test-4 | warning | The lesson's own taught bug, the three inputs left in, first fails test 4 and is told "Row 3 is long but points the way of the query. Compare by cosine, not distance" (appendix W5; the distance mutant meets the same line). | Add a test before test 4 on which leaving the inputs in changes the answer, keyed to "Leave out rows a, b and c", or widen test-4's line to name both faults.
- app/content/courses/representations/l1-a-table-of-vectors.json, l3-nearest-in-the-space.json | screens[10], screens[9] tie tests | note | NumPy's default `argsort` passes both searches: every tie is in a table of at most 5 rows, where the default sort keeps index order in practice. | One tie in a table of more than 16 rows (for example 20 equal rows).
- app/content/courses/representations/homework-1.json | items[0] guard | note | The guard is checked only at the extremes (0.07 against 0.65 and up), so a threshold anywhere from 0.08 to 0.64 passes. | Covered by the planted weak stock above.

## Number script and ops module

- docs/reports/representations-L1-numbers.py | whole script | warning | Seven `lv.claim(True, ..., covers=[...])` lines work as literals without a `why` in the count ("quiz row values", "lengths 0.05 and 0.8", "review short-row figures", "3 blocks of 4", "diagonal of E E^T: 0.64, 0.49, 0.09", "how lines"), and `covers=[round(min(rec_seeds), 2)]` let the false "never fell below 0.97" pass. `claim(10 ** 2 == 100, ...)` restates the false frequency law in l2. The five `literal()` marks (3,000 and 64 in the vendor prompt, £150m, the trap's 200 stocks, the homework's 5,000) are all given scenario figures; none should have been computed. | Turn given values into `literal(..., why=...)`, compute 0.64, 0.49 and 0.09 as squares, and state the seed minimum to 3 places. Engine item: flag `claim(True, covers=...)` in strict mode.
- docs/reports/representations-L1-numbers.py | l1 spin check | note | The "rotation" $\mathbf Q$ from `np.linalg.qr` of seed 5 has determinant $-1$, a reflection. The loss check is still right (any orthogonal map works). | Flip one column of $\mathbf Q$ when its determinant is negative, so the check matches the word on screen.
- app/content/data/ai/representations_ops_l1.py | factor_returns | note | Correct and as documented: sectors of 10, loadings $U(0.7, 1.3)$, moves of 1%, noise 1.2%, stock 9 on sector 2's move from day `days // 2`, the twin at index 30 and the lone stock last (31 with both), and the first 30 columns unchanged by either flag. The docstring says "lone=True adds a last stock" but not that it comes after the twin. | "...a last stock (after the twin when both are set)".

## Automated checks (no finding)

- Number script: 304 of 304, strict coverage, exit 0. Route B recomputes rather than restates for the small cases (Fractions, loops), the fits (a hand gradient matched to the autograd to $10^{-9}$, 300 steps), the k-means table (scikit-learn), and every hidden test twice (model solution and a loop twin). The three makemore figures (dev loss 2.1609 on 22,807 rows, the 2D runs, the letter neighbours) are recomputed from the shipped files.
- `grade-all.mjs --file <f> --code`: 0 failures on all seven files (78 non-code widgets, 10 code widgets: solutions pass, starters fail, all 36 mutants fail their named tests).
- Every other stated number recomputed and right: l1 (0.95, 1.38, 3.61, 3.12; 2.66 and $-0.19$; $(-0.7, 0.8, 2)$; 15,000,000; $(-0.3, 0.4, 0.5)$; 900 million; 13,824), l2 (4 and 1.41; 0.8; $-0.3162$; lengths 3.08, 2.81, 1.93, 2.9, 4.09, 4.74, z the shortest; 0.3 and 0.6128; 1.7; 0.774 from 11,500, 3,400, 65,000; 0.96), l3 (the four top-5 lists and values; i at rank 8, 0.079; recall 0.2, 0.5, 0.6; Small Tech 0.993 and $\mathbf q \approx (-0.03, 0.92, 0.08, -0.70)$; spreads 0.70, 0.33, 0.057; 6 and 28 of 30), l4 (the 12 by 12 block; stock 9 between the sector 0 and 2 clouds on the full fit; 0.0038, 0.0113, 0.1378; loss 0.1440 to 0.00035, 0.0187; 9 of 10, 0.967; k-means 29 of 30; 0.51, 0.31, 0.28 and 0.29, 0.20, 0.57; stock 20; 0.07, 0.65 to 0.83, 0.90, stock 27 at 0.09), review (3, 0.5963, $-0.4472$ and raw 0.2928, item 2, 0.6, 0.0121, 0.9), homework (164,096; guarded sum 1; analogy 1 and swap 0; 3.5; rubric points 2, 2, 2, 1, 1, 1, 1 = 10), problems (1, 0.2828, raw 0.6928 and 0.7249, 0.9597 and $-0.7894$, 0.8, 0.54, 0.0001, 0.22, 0.987, 0.062, 4, 0.8). Every other distractor matches its `why`; tolerances do not overlap.
- Voice: 2,593 sentences, none over 35 words, no explanation over three sentences, no em-dash, exclamation mark or American spelling; £ used for money.
- Downstream: the zero-vector convention (cosine 0, no neighbours) matches `llm-apps` L1's "return no results"; its l2 reasoning (cosine, so long notes do not win) builds on l2 and l3 here.

## Appendix: wrong solutions run through the grader

How: each source was added as a `mutants` entry (`test: 1`) to a scratch copy of its file (the widget's own mutants removed) and run with `node tools/grade-all.mjs --file <copy> --code --local-cdn <pkgs>`, the real Pyodide harness; the grader reports the first failing hidden test, or that the source passes every test. "Model solution, starter comment lines kept" is the authored solution typed into the starter with its comments left in (shown in full only where it fails). Entries marked [correct alternative] are right answers that should pass. "Factor returns from the wrong regression direction" has no widget to try: no code screen regresses returns on factors (`factor_returns` is a supplied generator). Results: 50 wrong solutions, 41 caught, 9 SURVIVE (l1 screens[9] W2; l1 screens[10] W1 and W2; l2 screens[9] W1; l3 screens[9] W1 and W6; homework items[0] W1, W5 and W6); 8 model solutions with comments kept, 1 fails (l4 screens[9], test 8); 10 correct alternatives, 9 pass (the defensible unit-row analogy in l3 screens[10] fails test 5, as the spec asks for $\mathbf e_b - \mathbf e_a + \mathbf e_c$).

### l1-a-table-of-vectors screens[9] `one_hot`, `one_hot_lookup`, `embedding_grad` (7 hidden tests)

- Model solution, starter comment lines kept: **passes**.

- W1. embedding_grad with mean() in place of sum(): **fails T4**.

```python
import numpy as np
from autograd import Tensor


def one_hot(idx, n):
    H = np.zeros((len(idx), n))
    H[np.arange(len(idx)), idx] = 1.0
    return H


def one_hot_lookup(E, idx):
    E = np.asarray(E, dtype=float)
    return one_hot(idx, len(E)) @ E


def embedding_grad(E, idx, dout):
    T = Tensor(E)
    out = T[np.asarray(idx)]
    (out * np.asarray(dout, dtype=float)).mean().backward()
    return T.grad
```

- W2. one_hot_lookup indexes E directly; the gradient is H.T @ dout by hand (no product in the lookup, no autograd): **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def one_hot(idx, n):
    H = np.zeros((len(idx), n))
    H[np.arange(len(idx)), idx] = 1.0
    return H


def one_hot_lookup(E, idx):
    return np.asarray(E, dtype=float)[np.asarray(idx)]


def embedding_grad(E, idx, dout):
    return one_hot(idx, len(E)).T @ np.asarray(dout, dtype=float)
```

- W3. one_hot sized by the largest index, not by the table: **fails T1**.

```python
import numpy as np
from autograd import Tensor


def one_hot(idx, n):
    H = np.zeros((len(idx), max(idx) + 1))
    H[np.arange(len(idx)), idx] = 1.0
    return H


def one_hot_lookup(E, idx):
    E = np.asarray(E, dtype=float)
    return one_hot(idx, len(E)) @ E[:max(idx) + 1]


def embedding_grad(E, idx, dout):
    return one_hot(idx, len(E)).T @ np.asarray(dout, dtype=float)
```

- W4. gradient read from the looked-up tensor instead of the table (returns dout itself): **fails T4**.

```python
import numpy as np
from autograd import Tensor


def one_hot(idx, n):
    H = np.zeros((len(idx), n))
    H[np.arange(len(idx)), idx] = 1.0
    return H


def one_hot_lookup(E, idx):
    E = np.asarray(E, dtype=float)
    return one_hot(idx, len(E)) @ E


def embedding_grad(E, idx, dout):
    T = Tensor(E)
    out = T[np.asarray(idx)]
    (out * np.asarray(dout, dtype=float)).sum().backward()
    return out.grad
```

- W5. np.add.at by hand [correct alternative, not the autograd]: **passes**.

```python
import numpy as np


def one_hot(idx, n):
    H = np.zeros((len(idx), n))
    H[np.arange(len(idx)), idx] = 1.0
    return H


def one_hot_lookup(E, idx):
    E = np.asarray(E, dtype=float)
    return one_hot(idx, len(E)) @ E


def embedding_grad(E, idx, dout):
    g = np.zeros(np.shape(E))
    np.add.at(g, np.asarray(idx), np.asarray(dout, dtype=float))
    return g
```


### l1-a-table-of-vectors screens[10] `nearest_rows` (5 hidden tests)

- Model solution, starter comment lines kept: **passes**.

- W1. sort, then drop the first entry on the assumption that it is row i (returns the query itself when an identical row comes earlier): **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def nearest_rows(E, i, k):
    E = np.asarray(E, dtype=float)
    d = np.sqrt(((E - E[i]) ** 2).sum(axis=1))
    order = np.argsort(d, kind="stable")
    return [int(j) for j in order[1:k + 1]]
```

- W2. default (unstable) argsort: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def nearest_rows(E, i, k):
    E = np.asarray(E, dtype=float)
    d = np.sqrt(((E - E[i]) ** 2).sum(axis=1))
    d[i] = np.inf
    return [int(j) for j in np.argsort(d)[:k]]
```

- W3. cosine in place of distance: **fails T1**.

```python
import numpy as np


def nearest_rows(E, i, k):
    E = np.asarray(E, dtype=float)
    U = E / np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    s = U @ U[i]
    s[i] = -np.inf
    return [int(j) for j in np.argsort(-s, kind="stable")[:k]]
```

- W4. row i deleted first, indices of the shorter table returned: **fails T1**.

```python
import numpy as np


def nearest_rows(E, i, k):
    E = np.asarray(E, dtype=float)
    F = np.delete(E, i, axis=0)
    d = np.sqrt(((F - E[i]) ** 2).sum(axis=1))
    return [int(j) for j in np.argsort(d, kind="stable")[:k]]
```

- W5. Manhattan distance: **fails T4**.

```python
import numpy as np


def nearest_rows(E, i, k):
    E = np.asarray(E, dtype=float)
    d = np.abs(E - E[i]).sum(axis=1)
    d[i] = np.inf
    return [int(j) for j in np.argsort(d, kind="stable")[:k]]
```

- W6. squared distance, no root [correct alternative]: **passes**.

```python
import numpy as np


def nearest_rows(E, i, k):
    E = np.asarray(E, dtype=float)
    d = ((E - E[i]) ** 2).sum(axis=1)
    d[i] = np.inf
    return [int(j) for j in np.argsort(d, kind="stable")[:k]]
```


### l2-cosine-similarity screens[9] `cosine` (7 hidden tests)

- Model solution, starter comment lines kept: **passes**.

- W1. guard on the first vector only: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def cosine(u, v):
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    nu, nv = np.sqrt(u @ u), np.sqrt(v @ v)
    if nu == 0:
        return 0.0
    return float(u @ v / (nu * nv))
```

- W2. precedence slip: divides by |u| and multiplies by |v|: **fails T1**.

```python
import numpy as np


def cosine(u, v):
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    if not u.any() or not v.any():
        return 0.0
    return float(u @ v / np.linalg.norm(u) * np.linalg.norm(v))
```

- W3. centres both vectors first (a correlation, not a cosine): **fails T1**.

```python
import numpy as np


def cosine(u, v):
    u = np.asarray(u, dtype=float); u = u - u.mean()
    v = np.asarray(v, dtype=float); v = v - v.mean()
    nu, nv = np.sqrt(u @ u), np.sqrt(v @ v)
    if nu == 0 or nv == 0:
        return 0.0
    return float(u @ v / (nu * nv))
```

- W4. dot product of the raw vectors, guarded (cosine without normalising): **fails T1**.

```python
import numpy as np


def cosine(u, v):
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    if not u.any() or not v.any():
        return 0.0
    return float(u @ v)
```

- W5. guard returns 1.0 (a zero vector is "like everything"): **fails T4**.

```python
import numpy as np


def cosine(u, v):
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    nu, nv = np.sqrt(u @ u), np.sqrt(v @ v)
    if nu == 0 or nv == 0:
        return 1.0
    return float(u @ v / (nu * nv))
```


### l2-cosine-similarity screens[10] `safe_normalise`, `cosine_matrix` (7 hidden tests)

- Model solution, starter comment lines kept: **passes**.

- W1. lengths without keepdims, so the division broadcasts across columns: **fails T1**.

```python
import numpy as np


def safe_normalise(E, eps=1e-12):
    E = np.asarray(E, dtype=float)
    n = np.sqrt((E ** 2).sum(axis=1))
    return np.where(n > eps, E / np.where(n > eps, n, 1.0), E)


def cosine_matrix(E):
    N = safe_normalise(E)
    return N @ N.T
```

- W2. right safe_normalise; cosine_matrix normalises the columns itself: **fails T2**.

```python
import numpy as np


def safe_normalise(E, eps=1e-12):
    E = np.asarray(E, dtype=float)
    n = np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    return np.where(n > eps, E / np.where(n > eps, n, 1.0), E)


def cosine_matrix(E):
    E = np.asarray(E, dtype=float)
    c = np.sqrt((E ** 2).sum(axis=0, keepdims=True))
    N = E / np.where(c > 0, c, 1.0)
    return N @ N.T
```

- W3. cosine_matrix as E E^T over the outer product of lengths, no guard: **fails T4**.

```python
import numpy as np


def safe_normalise(E, eps=1e-12):
    E = np.asarray(E, dtype=float)
    n = np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    return np.where(n > eps, E / np.where(n > eps, n, 1.0), E)


def cosine_matrix(E):
    E = np.asarray(E, dtype=float)
    n = np.sqrt((E ** 2).sum(axis=1))
    return (E @ E.T) / np.outer(n, n)
```

- W4. cosine_matrix sets the diagonal to 1 (every row is like itself): **fails T4**.

```python
import numpy as np


def safe_normalise(E, eps=1e-12):
    E = np.asarray(E, dtype=float)
    n = np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    return np.where(n > eps, E / np.where(n > eps, n, 1.0), E)


def cosine_matrix(E):
    N = safe_normalise(E)
    S = N @ N.T
    np.fill_diagonal(S, 1.0)
    return S
```

- W5. centres each column before normalising rows: **fails T2**.

```python
import numpy as np


def safe_normalise(E, eps=1e-12):
    E = np.asarray(E, dtype=float)
    n = np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    return np.where(n > eps, E / np.where(n > eps, n, 1.0), E)


def cosine_matrix(E):
    E = np.asarray(E, dtype=float)
    N = safe_normalise(E - E.mean(axis=0))
    return N @ N.T
```

- W6. returns the result as a list: **fails T6**.

```python
import numpy as np


def safe_normalise(E, eps=1e-12):
    E = np.asarray(E, dtype=float)
    n = np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    return np.where(n > eps, E / np.where(n > eps, n, 1.0), E)


def cosine_matrix(E):
    N = safe_normalise(E)
    return (N @ N.T).tolist()
```


### l3-nearest-in-the-space screens[9] `top_k`, `recall_at_k` (7 hidden tests)

- Model solution, starter comment lines kept: **passes**.

- W1. sort, then drop the first entry on the assumption that it is row i: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def top_k(E, i, k):
    E = np.asarray(E, dtype=float)
    n = np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    U = np.where(n > 0, E / np.where(n > 0, n, 1.0), 0.0)
    s = U @ U[i]
    order = np.argsort(-s, kind="stable")
    return [int(j) for j in order[1:k + 1]]


def recall_at_k(E, pairs, k):
    hits = sum(1 for i, j in pairs if j in top_k(E, i, k))
    return hits / len(pairs)
```

- W2. normalises columns instead of rows: **fails T1**.

```python
import numpy as np


def top_k(E, i, k):
    E = np.asarray(E, dtype=float)
    c = np.sqrt((E ** 2).sum(axis=0, keepdims=True))
    U = E / np.where(c > 0, c, 1.0)
    s = U @ U[i]
    s[i] = -np.inf
    return [int(j) for j in np.argsort(-s, kind="stable")[:k]]


def recall_at_k(E, pairs, k):
    hits = sum(1 for i, j in pairs if j in top_k(E, i, k))
    return hits / len(pairs)
```

- W3. leaves the query out by setting its cosine to 0: **fails T3**.

```python
import numpy as np


def top_k(E, i, k):
    E = np.asarray(E, dtype=float)
    n = np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    U = np.where(n > 0, E / np.where(n > 0, n, 1.0), 0.0)
    s = U @ U[i]
    s[i] = 0.0
    return [int(j) for j in np.argsort(-s, kind="stable")[:k]]


def recall_at_k(E, pairs, k):
    hits = sum(1 for i, j in pairs if j in top_k(E, i, k))
    return hits / len(pairs)
```

- W4. leaves out every row with cosine 1 (drops the twin too): **fails T2**.

```python
import numpy as np


def top_k(E, i, k):
    E = np.asarray(E, dtype=float)
    n = np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    U = np.where(n > 0, E / np.where(n > 0, n, 1.0), 0.0)
    s = U @ U[i]
    s[s > 1 - 1e-12] = -np.inf
    return [int(j) for j in np.argsort(-s, kind="stable")[:k]]


def recall_at_k(E, pairs, k):
    hits = sum(1 for i, j in pairs if j in top_k(E, i, k))
    return hits / len(pairs)
```

- W5. no zero-row guard (NaN cosine): **fails T3**.

```python
import numpy as np


def top_k(E, i, k):
    E = np.asarray(E, dtype=float)
    U = E / np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    s = U @ U[i]
    s[i] = -np.inf
    return [int(j) for j in np.argsort(-s, kind="stable")[:k]]


def recall_at_k(E, pairs, k):
    hits = sum(1 for i, j in pairs if j in top_k(E, i, k))
    return hits / len(pairs)
```

- W6. default (unstable) argsort: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def top_k(E, i, k):
    E = np.asarray(E, dtype=float)
    n = np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    U = np.where(n > 0, E / np.where(n > 0, n, 1.0), 0.0)
    s = U @ U[i]
    s[i] = -np.inf
    return [int(j) for j in np.argsort(-s)[:k]]


def recall_at_k(E, pairs, k):
    hits = sum(1 for i, j in pairs if j in top_k(E, i, k))
    return hits / len(pairs)
```

- W7. recall counts the pair when i is in j's list (direction swapped): **fails T6**.

```python
import numpy as np


def top_k(E, i, k):
    E = np.asarray(E, dtype=float)
    n = np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    U = np.where(n > 0, E / np.where(n > 0, n, 1.0), 0.0)
    s = U @ U[i]
    s[i] = -np.inf
    return [int(j) for j in np.argsort(-s, kind="stable")[:k]]


def recall_at_k(E, pairs, k):
    hits = sum(1 for i, j in pairs if i in top_k(E, j, k))
    return hits / len(pairs)
```


### l3-nearest-in-the-space screens[10] `analogy` (5 hidden tests)

- Model solution, starter comment lines kept: **passes**.

- W1. dot product with the query in place of cosine: **fails T5**.

```python
import numpy as np


def analogy(E, a, b, c, k):
    E = np.asarray(E, dtype=float)
    q = E[b] - E[a] + E[c]
    s = E @ q
    s[[a, b, c]] = -np.inf
    return [int(j) for j in np.argsort(-s, kind="stable")[:k]]
```

- W2. leaves out only c, the row the query starts from: **fails T5**.

```python
import numpy as np


def analogy(E, a, b, c, k):
    E = np.asarray(E, dtype=float)
    q = E[b] - E[a] + E[c]
    U = E / np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    s = U @ (q / np.sqrt(q @ q))
    s[c] = -np.inf
    return [int(j) for j in np.argsort(-s, kind="stable")[:k]]
```

- W3. averages b and c and subtracts nothing (the brief's averaging test): **fails T3**.

```python
import numpy as np


def analogy(E, a, b, c, k):
    E = np.asarray(E, dtype=float)
    q = (E[b] + E[c]) / 2
    U = E / np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    s = U @ (q / np.sqrt(q @ q))
    s[[a, b, c]] = -np.inf
    return [int(j) for j in np.argsort(-s, kind="stable")[:k]]
```

- W4. normalises each input row before forming the query (3CosAdd on unit rows) [defensible variant]: **fails T5**.

```python
import numpy as np


def analogy(E, a, b, c, k):
    E = np.asarray(E, dtype=float)
    U = E / np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    q = U[b] - U[a] + U[c]
    s = U @ q
    s[[a, b, c]] = -np.inf
    return [int(j) for j in np.argsort(-s, kind="stable")[:k]]
```

- W5. inputs left in the search (the taught bug; checks which byKey line it meets): **fails T4**.

```python
import numpy as np


def analogy(E, a, b, c, k):
    E = np.asarray(E, dtype=float)
    q = E[b] - E[a] + E[c]
    U = E / np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    s = U @ (q / np.sqrt(q @ q))
    return [int(j) for j in np.argsort(-s, kind="stable")[:k]]
```


### l4-embedding-stocks screens[9] `corr_from_returns`, `sector_recovery` (8 hidden tests)

- Model solution, starter comment lines kept: **fails T8**.

```python
import numpy as np


def corr_from_returns(R):
    # R is days by stocks; return the stocks-by-stocks correlation matrix,
    # built from demeaned columns (no np.corrcoef)
    X = np.asarray(R, dtype=float)
    X = X - X.mean(axis=0)
    X = X / np.sqrt((X ** 2).sum(axis=0))
    return X.T @ X


def sector_recovery(E, sectors):
    # share of stocks whose nearest other row by cosine has the same sector
    E = np.asarray(E, dtype=float)
    U = E / np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    S = U @ U.T
    np.fill_diagonal(S, -np.inf)
    nearest = S.argmax(axis=1)
    sectors = np.asarray(sectors)
    return float(np.mean(sectors[nearest] == sectors))
```

- W1. centring after normalising: **fails T1**.

```python
import numpy as np


def corr_from_returns(R):
    X = np.asarray(R, dtype=float)
    X = X / np.sqrt((X ** 2).sum(axis=0))
    X = X - X.mean(axis=0)
    return X.T @ X


def sector_recovery(E, sectors):
    E = np.asarray(E, dtype=float)
    U = E / np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    S = U @ U.T
    np.fill_diagonal(S, -np.inf)
    nearest = S.argmax(axis=1)
    sectors = np.asarray(sectors)
    return float(np.mean(sectors[nearest] == sectors))
```

- W2. sample standard deviation (ddof 1) with a divide by n: **fails T1**.

```python
import numpy as np


def corr_from_returns(R):
    X = np.asarray(R, dtype=float)
    X = (X - X.mean(axis=0)) / X.std(axis=0, ddof=1)
    return X.T @ X / len(X)


def sector_recovery(E, sectors):
    E = np.asarray(E, dtype=float)
    U = E / np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    S = U @ U.T
    np.fill_diagonal(S, -np.inf)
    nearest = S.argmax(axis=1)
    sectors = np.asarray(sectors)
    return float(np.mean(sectors[nearest] == sectors))
```

- W3. sector_recovery by dot product of the raw rows: **fails T6**.

```python
import numpy as np


def corr_from_returns(R):
    X = np.asarray(R, dtype=float)
    X = X - X.mean(axis=0)
    X = X / np.sqrt((X ** 2).sum(axis=0))
    return X.T @ X


def sector_recovery(E, sectors):
    E = np.asarray(E, dtype=float)
    S = E @ E.T
    np.fill_diagonal(S, -np.inf)
    sectors = np.asarray(sectors)
    return float(np.mean(sectors[S.argmax(axis=1)] == sectors))
```

- W4. sector_recovery returns the count, not the share: **fails T4**.

```python
import numpy as np


def corr_from_returns(R):
    X = np.asarray(R, dtype=float)
    X = X - X.mean(axis=0)
    X = X / np.sqrt((X ** 2).sum(axis=0))
    return X.T @ X


def sector_recovery(E, sectors):
    E = np.asarray(E, dtype=float)
    U = E / np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    S = U @ U.T
    np.fill_diagonal(S, -np.inf)
    sectors = np.asarray(sectors)
    return float(np.sum(sectors[S.argmax(axis=1)] == sectors))
```

- W5. normalises rows of R (days) instead of columns before the product: **fails T1**.

```python
import numpy as np


def corr_from_returns(R):
    X = np.asarray(R, dtype=float)
    X = X - X.mean(axis=0)
    X = X / np.sqrt((X ** 2).sum(axis=1, keepdims=True))
    return X.T @ X


def sector_recovery(E, sectors):
    E = np.asarray(E, dtype=float)
    U = E / np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    S = U @ U.T
    np.fill_diagonal(S, -np.inf)
    nearest = S.argmax(axis=1)
    sectors = np.asarray(sectors)
    return float(np.mean(sectors[nearest] == sectors))
```

- W6. returns the matrix as a list (fails only the shape test): **fails T3**.

```python
import numpy as np


def corr_from_returns(R):
    X = np.asarray(R, dtype=float)
    X = X - X.mean(axis=0)
    X = X / np.sqrt((X ** 2).sum(axis=0))
    return (X.T @ X).tolist()


def sector_recovery(E, sectors):
    E = np.asarray(E, dtype=float)
    U = E / np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    S = U @ U.T
    np.fill_diagonal(S, -np.inf)
    nearest = S.argmax(axis=1)
    sectors = np.asarray(sectors)
    return float(np.mean(sectors[nearest] == sectors))
```

- W7. sector_recovery by Euclidean distance of the unit rows [correct alternative]: **passes**.

```python
import numpy as np


def corr_from_returns(R):
    X = np.asarray(R, dtype=float)
    X = X - X.mean(axis=0)
    X = X / np.sqrt((X ** 2).sum(axis=0))
    return X.T @ X


def sector_recovery(E, sectors):
    E = np.asarray(E, dtype=float)
    U = E / np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    d = ((U[:, None] - U[None]) ** 2).sum(-1)
    np.fill_diagonal(d, np.inf)
    sectors = np.asarray(sectors)
    return float(np.mean(sectors[d.argmin(axis=1)] == sectors))
```


### l4-embedding-stocks screens[10] `fit_embeddings` (5 hidden tests)

- W1. zero_grad once, before the loop: **fails T1**.

```python
import numpy as np
from autograd import Tensor, sgd_step


def fit_embeddings(C, dim, steps, lr, seed):
    # start: 0.1 * np.random.default_rng(seed).standard_normal((n, dim))
    # loss: mean over pairs i != j of (E E^T - C)^2; plain gradient descent
    n = len(C)
    E = Tensor(0.1 * np.random.default_rng(seed).standard_normal((n, dim)))
    C = np.asarray(C, dtype=float)
    M = 1.0 - np.eye(n)
    E.zero_grad()
    for _ in range(steps):
        D = (E @ E.T - C) * M
        loss = (D ** 2).sum() / (n * (n - 1))
        loss.backward()
        sgd_step([E], lr)
    return E.data
```

- W2. mask applied after squaring, loss scaled the other way round [correct alternative]: **passes**.

```python
import numpy as np
from autograd import Tensor, sgd_step


def fit_embeddings(C, dim, steps, lr, seed):
    # start: 0.1 * np.random.default_rng(seed).standard_normal((n, dim))
    # loss: mean over pairs i != j of (E E^T - C)^2; plain gradient descent
    n = len(C)
    E = Tensor(0.1 * np.random.default_rng(seed).standard_normal((n, dim)))
    C = np.asarray(C, dtype=float)
    M = 1.0 - np.eye(n)
    for _ in range(steps):
        E.zero_grad()
        D = E @ E.T - C
        loss = ((D * D) * M).sum() * (1.0 / (n * (n - 1)))
        loss.backward()
        sgd_step([E], lr)
    return E.data
```

- W3. hand gradient 4 M(EE^T - C)E / n(n-1) on the array [correct alternative, no autograd]: **passes**.

```python
import numpy as np
from autograd import Tensor, sgd_step


def fit_embeddings(C, dim, steps, lr, seed):
    n = len(C)
    E = 0.1 * np.random.default_rng(seed).standard_normal((n, dim))
    C = np.asarray(C, dtype=float)
    M = 1.0 - np.eye(n)
    for _ in range(steps):
        D = (E @ E.T - C) * M
        E = E - lr * 4 * D @ E / (n * (n - 1))
    return E
```

- W4. half the pairs (upper triangle) over half the count [correct alternative]: **passes**.

```python
import numpy as np
from autograd import Tensor, sgd_step


def fit_embeddings(C, dim, steps, lr, seed):
    # start: 0.1 * np.random.default_rng(seed).standard_normal((n, dim))
    # loss: mean over pairs i != j of (E E^T - C)^2; plain gradient descent
    n = len(C)
    E = Tensor(0.1 * np.random.default_rng(seed).standard_normal((n, dim)))
    C = np.asarray(C, dtype=float)
    M = 1.0 - np.eye(n)
    U = np.triu(np.ones((n, n)), 1)
    for _ in range(steps):
        E.zero_grad()
        D = (E @ E.T - C) * U
        loss = (D ** 2).sum() / (n * (n - 1) / 2)
        loss.backward()
        sgd_step([E], lr)
    return E.data
```

- W5. upper triangle only, divided by n(n - 1) (half the gradient): **fails T1**.

```python
import numpy as np
from autograd import Tensor, sgd_step


def fit_embeddings(C, dim, steps, lr, seed):
    # start: 0.1 * np.random.default_rng(seed).standard_normal((n, dim))
    # loss: mean over pairs i != j of (E E^T - C)^2; plain gradient descent
    n = len(C)
    E = Tensor(0.1 * np.random.default_rng(seed).standard_normal((n, dim)))
    C = np.asarray(C, dtype=float)
    M = 1.0 - np.eye(n)
    U = np.triu(np.ones((n, n)), 1)
    for _ in range(steps):
        E.zero_grad()
        D = (E @ E.T - C) * U
        loss = (D ** 2).sum() / (n * (n - 1))
        loss.backward()
        sgd_step([E], lr)
    return E.data
```

- W6. zero_grad after the step [correct alternative]: **passes**.

```python
import numpy as np
from autograd import Tensor, sgd_step


def fit_embeddings(C, dim, steps, lr, seed):
    # start: 0.1 * np.random.default_rng(seed).standard_normal((n, dim))
    # loss: mean over pairs i != j of (E E^T - C)^2; plain gradient descent
    n = len(C)
    E = Tensor(0.1 * np.random.default_rng(seed).standard_normal((n, dim)))
    C = np.asarray(C, dtype=float)
    M = 1.0 - np.eye(n)
    for _ in range(steps):
        D = (E @ E.T - C) * M
        loss = (D ** 2).sum() / (n * (n - 1))
        loss.backward()
        sgd_step([E], lr)
        E.zero_grad()
    return E.data
```

- W7. a fresh Tensor each step from the updated array, never zeroed [correct alternative]: **passes**.

```python
import numpy as np
from autograd import Tensor, sgd_step


def fit_embeddings(C, dim, steps, lr, seed):
    n = len(C)
    A = 0.1 * np.random.default_rng(seed).standard_normal((n, dim))
    C = np.asarray(C, dtype=float)
    M = 1.0 - np.eye(n)
    for _ in range(steps):
        E = Tensor(A)
        D = (E @ E.T - C) * M
        ((D ** 2).sum() / (n * (n - 1))).backward()
        A = A - lr * E.grad
    return A
```

- W8. absolute error in place of squared error: **fails T1**.

```python
import numpy as np
from autograd import Tensor, sgd_step


def fit_embeddings(C, dim, steps, lr, seed):
    # start: 0.1 * np.random.default_rng(seed).standard_normal((n, dim))
    # loss: mean over pairs i != j of (E E^T - C)^2; plain gradient descent
    n = len(C)
    E = Tensor(0.1 * np.random.default_rng(seed).standard_normal((n, dim)))
    C = np.asarray(C, dtype=float)
    M = 1.0 - np.eye(n)
    for _ in range(steps):
        E.zero_grad()
        D = (E @ E.T - C) * M
        loss = ((D * D) ** 0.5).sum() / (n * (n - 1))
        loss.backward()
        sgd_step([E], lr)
    return E.data
```


### homework-1 items[0] `similar_stocks` (8 hidden tests)

- W1. ranks by the fitted correlation e_i . e_j (dot product) in place of cosine: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def similar_stocks(R, k, dim, seed):
    X = np.asarray(R, dtype=float)
    X = X - X.mean(axis=0)
    X = X / np.sqrt((X ** 2).sum(axis=0))
    C = X.T @ X
    n = len(C)
    M = 1.0 - np.eye(n)
    E = 0.1 * np.random.default_rng(seed).standard_normal((n, dim))
    for _ in range(300):
        D = (E @ E.T - C) * M
        E = E - 10.0 * 4 * D @ E / (n * (n - 1))
    length = np.sqrt((E ** 2).sum(axis=1))
    ok = length >= 0.25
    out = []
    for i in range(n):
        if not ok[i]:
            out.append([])
            continue
        s = [(-(E[i] @ E[j]), j) for j in range(n) if j != i and ok[j]]
        out.append([j for _, j in sorted(s)[:k]])
    return out
```

- W2. centring after normalising the return columns: **fails T8**.

```python
import numpy as np


def similar_stocks(R, k, dim, seed):
    X = np.asarray(R, dtype=float)
    X = X / np.sqrt((X ** 2).sum(axis=0))
    X = X - X.mean(axis=0)
    C = X.T @ X
    n = len(C)
    M = 1.0 - np.eye(n)
    E = 0.1 * np.random.default_rng(seed).standard_normal((n, dim))
    for _ in range(300):
        D = (E @ E.T - C) * M
        E = E - 10.0 * 4 * D @ E / (n * (n - 1))
    length = np.sqrt((E ** 2).sum(axis=1))
    ok = length >= 0.25
    out = []
    for i in range(n):
        if not ok[i]:
            out.append([])
            continue
        s = [(-(E[i] @ E[j]) / (length[i] * length[j]), j) for j in range(n) if j != i and ok[j]]
        out.append([j for _, j in sorted(s)[:k]])
    return out
```

- W3. rows of the correlation matrix as the embedding, guard on their length: **fails T6**.

```python
import numpy as np


def similar_stocks(R, k, dim, seed):
    X = np.asarray(R, dtype=float)
    X = X - X.mean(axis=0)
    X = X / np.sqrt((X ** 2).sum(axis=0))
    E = X.T @ X
    n = len(E)
    length = np.sqrt((E ** 2).sum(axis=1))
    ok = length >= 0.25
    out = []
    for i in range(n):
        if not ok[i]:
            out.append([])
            continue
        s = [(-(E[i] @ E[j]) / (length[i] * length[j]), j) for j in range(n) if j != i and ok[j]]
        out.append([j for _, j in sorted(s)[:k]])
    return out
```

- W4. eigenvectors of C scaled by root eigenvalues [correct alternative]: **passes**.

```python
import numpy as np


def similar_stocks(R, k, dim, seed):
    X = np.asarray(R, dtype=float)
    X = X - X.mean(axis=0)
    X = X / np.sqrt((X ** 2).sum(axis=0))
    C = X.T @ X
    n = len(C)
    w, V = np.linalg.eigh(C)
    E = V[:, -dim:] * np.sqrt(np.maximum(w[-dim:], 0))
    length = np.sqrt((E ** 2).sum(axis=1))
    ok = length >= 0.25
    out = []
    for i in range(n):
        if not ok[i]:
            out.append([])
            continue
        s = [(-(E[i] @ E[j]) / (length[i] * length[j]), j) for j in range(n) if j != i and ok[j]]
        out.append([j for _, j in sorted(s)[:k]])
    return out
```

- W5. guard compares squared length with 0.25 (threshold 0.5 on length): **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def similar_stocks(R, k, dim, seed):
    X = np.asarray(R, dtype=float)
    X = X - X.mean(axis=0)
    X = X / np.sqrt((X ** 2).sum(axis=0))
    C = X.T @ X
    n = len(C)
    M = 1.0 - np.eye(n)
    E = 0.1 * np.random.default_rng(seed).standard_normal((n, dim))
    for _ in range(300):
        D = (E @ E.T - C) * M
        E = E - 10.0 * 4 * D @ E / (n * (n - 1))
    length = np.sqrt((E ** 2).sum(axis=1))
    ok = length ** 2 >= 0.25
    out = []
    for i in range(n):
        if not ok[i]:
            out.append([])
            continue
        s = [(-(E[i] @ E[j]) / (length[i] * length[j]), j) for j in range(n) if j != i and ok[j]]
        out.append([j for _, j in sorted(s)[:k]])
    return out
```

- W6. fit from the covariance of demeaned returns scaled to percent (rows long, guard never fires): **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def similar_stocks(R, k, dim, seed):
    X = 100 * np.asarray(R, dtype=float)
    X = X - X.mean(axis=0)
    C = X.T @ X / len(X)
    n = len(C)
    M = 1.0 - np.eye(n)
    E = 0.1 * np.random.default_rng(seed).standard_normal((n, dim))
    for _ in range(300):
        D = (E @ E.T - C) * M
        E = E - 0.5 * 4 * D @ E / (n * (n - 1))
    length = np.sqrt((E ** 2).sum(axis=1))
    ok = length >= 0.25
    out = []
    for i in range(n):
        if not ok[i]:
            out.append([])
            continue
        s = [(-(E[i] @ E[j]) / (length[i] * length[j]), j) for j in range(n) if j != i and ok[j]]
        out.append([j for _, j in sorted(s)[:k]])
    return out
```


### homework-1 items[1] `nearest_for_queries` (5 hidden tests)

- Model solution, starter comment lines kept: **passes**.

- W1. drops the top match as if the query were in the table: **fails T1**.

```python
import numpy as np


def nearest_for_queries(E, Q, k):
    E = np.asarray(E, dtype=float)
    ne = np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    U = np.where(ne > 0, E / np.where(ne > 0, ne, 1.0), 0.0)
    out = []
    for q in np.asarray(Q, dtype=float):
        nq = np.sqrt(q @ q)
        if nq == 0:
            out.append([])
            continue
        s = U @ (q / nq)
        out.append([int(j) for j in np.argsort(-s, kind="stable")[1:k + 1]])
    return out
```

- W2. normalises the columns of E: **fails T3**.

```python
import numpy as np


def nearest_for_queries(E, Q, k):
    E = np.asarray(E, dtype=float)
    c = np.sqrt((E ** 2).sum(axis=0, keepdims=True))
    U = E / np.where(c > 0, c, 1.0)
    out = []
    for q in np.asarray(Q, dtype=float):
        nq = np.sqrt(q @ q)
        if nq == 0:
            out.append([])
            continue
        s = U @ (q / nq)
        out.append([int(j) for j in np.argsort(-s, kind="stable")[:k]])
    return out
```

- W3. no guard on zero rows of E (NaN cosine): **fails T4**.

```python
import numpy as np


def nearest_for_queries(E, Q, k):
    E = np.asarray(E, dtype=float)
    U = E / np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    out = []
    for q in np.asarray(Q, dtype=float):
        nq = np.sqrt(q @ q)
        if nq == 0:
            out.append([])
            continue
        s = U @ (q / nq)
        out.append([int(j) for j in np.argsort(-s, kind="stable")[:k]])
    return out
```

- W4. Euclidean distance from the query: **fails T3**.

```python
import numpy as np


def nearest_for_queries(E, Q, k):
    E = np.asarray(E, dtype=float)
    ne = np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    U = np.where(ne > 0, E / np.where(ne > 0, ne, 1.0), 0.0)
    out = []
    for q in np.asarray(Q, dtype=float):
        nq = np.sqrt(q @ q)
        if nq == 0:
            out.append([])
            continue
        s = -np.sqrt(((E - q) ** 2).sum(axis=1))
        out.append([int(j) for j in np.argsort(-s, kind="stable")[:k]])
    return out
```

- W5. normalises the query only, not the rows (dot product ranking): **fails T3**.

```python
import numpy as np


def nearest_for_queries(E, Q, k):
    E = np.asarray(E, dtype=float)
    ne = np.sqrt((E ** 2).sum(axis=1, keepdims=True))
    U = np.where(ne > 0, E / np.where(ne > 0, ne, 1.0), 0.0)
    out = []
    for q in np.asarray(Q, dtype=float):
        nq = np.sqrt(q @ q)
        if nq == 0:
            out.append([])
            continue
        s = E @ (q / nq)
        out.append([int(j) for j in np.argsort(-s, kind="stable")[:k]])
    return out
```

