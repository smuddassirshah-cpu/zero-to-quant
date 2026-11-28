# representations level 5 (Graph networks): second-reader findings

Scope: `app/content/courses/representations/` level 5 (`l17-graphs-as-matrices`, `l18-passing-messages`, `l19-a-gcn-layer`, `l20-labels-on-a-graph`, `review-5`, `homework-5`, `problems-5`) and `app/content/data/ai/representations_ops_l5.py`, at `037a8048` (`claude/inspiring-dirac-ckxdoa`).
Method: every module op gradient-checked by central differences in float64 through the frozen autograd (scratchpad folder `rv5/`, `gradcheck.py`): `gcn_logits` with 1, 2 and 3 layers against the weights and the input, the training cross-entropy, one $\operatorname{ReLU}(\hat{\mathbf A}\mathbf X\mathbf W)$ layer; `normalised_adjacency` against an explicit $\tilde{\mathbf D}^{-1/2}\tilde{\mathbf A}\tilde{\mathbf D}^{-1/2}$, its similarity to $\tilde{\mathbf D}^{-1}\tilde{\mathbf A}$, and the no-loop $\mathbf D^{-1/2}\mathbf A\mathbf D^{-1/2}$ on the square and the venues; the over-smoothing claims against the eigenvalues of $\hat{\mathbf A}$ on the lesson graphs and all 20 seeded graphs (`chk1.py`), connectivity included; the 16-layer runs retrained and their hidden layers inspected (`chk2.py`); every derivation re-derived by hand; `docs/reports/representations-L5-numbers.py` through `node tools/run-number-scripts.mjs --python <venv> --only representations-L5` (1 of 1 passed, 4 s) and directly with `ZQ_NUMBERS_STRICT=1` under default threads and under one thread (312 of 312 checks, 0 uncovered, 5 literals, identical output, 4 s each), every claim read for fiat and dead branches; `node tools/grade-all.mjs --file <path> --code --local-cdn <pkgs>` on each of the 7 files alone (0 failures; 11 Python code widgets, 73 other widgets); 51 wrong solutions, harmless variants and correct alternatives run through the page's harness (`tools/code-runner.mjs`, one job; appendix); every `byKey` test-N line checked for a mutant or wrong solution that reaches it first; every graph canvas checked against the seeded matrices (l17 screen 0 layout, l18 screen 3 edges, l19 screen 4's 37 edges, l20 firm 3's links); every stated number recomputed; distractors read against their `why`; `same-course-reuse.mjs --all` (no error line for representations); `voice-scan.py 35 --summary` and a scan for em-dashes, exclamation marks and American spellings.
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, teaching issue or a test that misses what it claims; note = style or small gap.

Counts: 1 error, 8 warnings, 11 notes. Wrong solutions: 3 of 38 survive (the model-selection leak in `train_gcn`, an off-by-one in `settles`, $\mathbf A^k + \mathbf A^{k-1}$ in `nodes_within`); 6 harmless variants pass; 1 of 7 correct alternatives fails (l20 `feature_spread`, test 3). No module error.

## Module and number script

- app/content/data/ai/representations_ops_l5.py | all public names | note | Correct and as documented. Central differences agree with the autograd to relative 1.1e-10 to 4.8e-10 for `gcn_logits` (1 to 3 layers, weights and input), 1.4e-9 to 9.5e-9 for the cross-entropy over the training rows, 4.3e-10 for one ReLU layer. `normalised_adjacency` equals the explicit $\tilde{\mathbf D}^{-1/2}\tilde{\mathbf A}\tilde{\mathbf D}^{-1/2}$ exactly, is symmetric, equals $\tilde{\mathbf D}^{1/2}(\tilde{\mathbf D}^{-1}\tilde{\mathbf A})\tilde{\mathbf D}^{-1/2}$ to 1e-16 with the same eigenvalues to 4e-15, gives an isolated node $\hat A_{ii} = 1$, and leaves its input unchanged; `train_gcn_params` records each loss before its step (the first equals the loss at `gcn_init`). Without loops, $\mathbf D^{-1/2}\mathbf A\mathbf D^{-1/2}$ on the square has eigenvalues $-1, 0, 0, 1$ (the swap of l18 screen 7), and with loops $-\tfrac13, \tfrac13, \tfrac13, 1$ (it settles). | None.
- docs/reports/representations-L5-numbers.py | lines 201, 230, 170, 228, 579, 592 | warning | Fiat and dead code in a strict script. Line 230 claims `9 == 9 and 1 + 3 == 4 and 1 + 3 + 9 == 13` for l18 screen 6's directed banks, so no matrix is built and the answer, the trap and both slips are covered by assertion. Line 201 is a loop whose body is `pass`. Slip values are asserted as literal fractions instead of recomputed from the data: `Fr(14, 4) == Fr(7, 2)` (l17's 3.5), `Fr(28, 4) == 7` (l18's 7), `Fr(8, 4) == 2` and `8 * 4 / 12` (review's 2 and 2.667), `1 + 3 == 4`, `3 + 6 == 9`, `1 + 3 + 6 + 3 == 13` (homework item 5, whose key is also `1 + 3 + 3 * 2`, one route only). The figures are right. | Build the directed $\mathbf A$ (B to A, C to A, A to D) and compute $(\mathbf A\mathbf x)_A$, $(\mathbf A^\top\mathbf x)_A$ and the symmetrised sum; compute the l17, l18 and review slips with `step_fr(..., loops=True)` or the plain mean of the stated values; build F's two-level tree and count it by breadth-first search; delete line 201.

## Mathematics (no finding)

Checked and correct: $\mathbf A\mathbf x$ sums neighbours, $\mathbf D^{-1}\mathbf A$ is the walk's step matrix with rows summing to 1, $(\mathbf P\mathbf x)_i$ is the expected value of $\mathbf x$ at the walker's next position, and probability moves by $\mathbf P^\top$ (l18 screen 4, review item 5); $\hat A_{ij} = \tilde A_{ij}/\sqrt{\tilde d_i\tilde d_j}$ with the brief's 2, 3, 2, $\tfrac12$, 0.408, $\tfrac13$; $\hat{\mathbf A}$ and $\tilde{\mathbf D}^{-1}\tilde{\mathbf A}$ similar, eigenvectors related by $\tilde{\mathbf D}^{1/2}$ (homework item 6), largest eigenvalue 1; $\mathbf P^k\mathbf x \to (\boldsymbol\pi^\top\mathbf x)\mathbf 1$ on a connected non-bipartite graph with $\pi_i = d_i/2|E|$, and with loops $\pi_i \propto \tilde d_i$ (1.6, $\tfrac{12}{7}$); the square and the path swap for ever without loops; $k$ looped steps or $k$ layers reach exactly the nodes within $k$ links ($\hat{\mathbf A}^k$ has a non-zero $(i, j)$ entry exactly then, since $\hat{\mathbf A} \ge 0$ with a positive diagonal); $\hat{\mathbf A}(\mathbf H\mathbf W) = (\hat{\mathbf A}\mathbf H)\mathbf W$ and the linear collapse to $\hat{\mathbf A}^2\mathbf H\mathbf W_1\mathbf W_2$; the weight counts; over-smoothing: every l20 graph (seed 13 and the 20 seeds) is connected, so eigenvalue 1 is simple with eigenvector $\propto\sqrt{\tilde d_i}$ (homework item 2's proof is sound: Perron and Frobenius for the irreducible matrix), and the next eigenvalue in size is $\lambda_2$ (0.872 on seed 13, 0.79 to 0.94 over the 20 seeds; the most negative is $-0.42$), so the share outside $\mathbf v$ decays like $0.872^k$, as l20 screen 10 says; the limit rows differ only by $\sqrt{\tilde d_i}$, which gives a bias-free linear head one class for every node, hence the 0.50 at 128 steps; 0.426, 0.5 and 1.225 as square roots of degree ratios. Self-loops slow the blur a little on these graphs ($\lambda_2$ 0.849 without them, 0.872 with), as review item 3's `why` says.

## l17 to l20

- app/content/courses/representations/l20-labels-on-a-graph.json | quiz[1] option `relu` why, explain; screens[5] explain | error | The quiz asks why 40 graph layers predict every node in one class and its ReLU option's why says "ReLU alone does not make all nodes alike; the repeated averaging does." The level's own deep runs say otherwise. Retraining the 16-layer ReLU stack on the 20 graphs (the script's setting), 17 of 20 runs predict a single class, and in 11 of them every one of the 16 units of the last hidden layer is dead, so the output is 0 at every node: averaging has nothing left to blur. With $N(0, 1/\text{fan-in})$ weights the signal also vanishes before training (the last hidden layer's largest entry is 0.002 at `gcn_init` on the seed-13 graph). Screen 5 hedges ("deep stacks are also hard to train"); the quiz states the opposite. | Ask about the linear stack the lesson measured: "A team applies $\hat{\mathbf A}$ 40 times and then one weight matrix ..." (keep the key), and reword the ReLU option's why: "ReLU cannot cause it here: this stack has no ReLU, yet 40 multiplications by $\hat{\mathbf A}$ leave only the top eigenvector." In screen 5's explain name the second cause: "... the training loss stays above 0.6: in most of them every ReLU unit has died, so deep stacks are also hard to train."
- app/content/courses/representations/l19-a-gcn-layer.json | screens[1] feedback.correct, byKey `no-relu`, explain | warning | The learner is told to use the mixed row $(-0.51, 0.32)$, and the hints write $-0.51 \times 4.2 + 0.32 \times (-3.6)$, which is $-3.29$; the second entry is $1.85$. The feedback and explain state $(-0.51, 0.32)\mathbf W_1 \approx (-3.27, 1.84)$, the product of the unrounded row $(-0.507, 0.318)$. The bands accept both, so only the stated arithmetic is wrong. | Explain: "$(-0.51, 0.32)\,\mathbf W_1 \approx (-3.29, 1.85)$; from the unrounded row it is $(-3.27, 1.84)$, and ReLU gives $(0, 1.84)$." Byline `no-relu`: "about $-3.29$".
- app/content/courses/representations/l18-passing-messages.json | screens[6] explain, summary.trap | warning | The trap presents "messages follow $\mathbf A$, not $\mathbf A^\top$" as a fact, and the summary calls collecting along the arrows into a node the error. Which way messages flow is a modelling choice: with $A_{ij} = 1$ for "$i$ lent to $j$", $\mathbf A\mathbf x$ makes a lender read its borrowers, which suits exposure, while graph libraries such as PyTorch Geometric pass messages along arrows into a node by default, which is $\mathbf A^\top\mathbf x$ here. The real trap is not knowing which one the product computes. | Explain: "$(\mathbf A\mathbf x)_i$ sums over the $j$ with $A_{ij} = 1$, so A collects D's 9: a lender reads the banks it is exposed to. Collecting along arrows into a node is $\mathbf A^\top\mathbf x$; choose the direction on purpose." Summary trap: "On a directed graph, mixing up $\mathbf A\mathbf x$ (row $i$: the arrows out of $i$) with $\mathbf A^\top\mathbf x$ (the arrows into $i$)."
- app/content/courses/representations/l20-labels-on-a-graph.json | screens[11] hints[1] | warning | "Shuffled links keep the degrees but drop any link between similar firms" is false: a degree-preserving shuffle still links some same-sector firms by chance; it breaks the association between links and sectors. | "Shuffled links keep every firm's degree but link firms at random, whatever their sector."
- app/content/courses/representations/review-5.json | items[3] prompt and option `w` why | warning | "A team stacks 30 graph convolution layers and finds its accuracy near a coin toss" then credits only the blur, and the `w` why asserts "The blur comes from multiplying by $\hat{\mathbf A}$ again and again". A ReLU stack of that depth near a coin toss is, in this level's own runs, mostly dead units and vanished signal (error above). | Prompt: "A team applies $\hat{\mathbf A}$ 30 times before one weight matrix and finds its accuracy near a coin toss." Keep the options.
- app/content/courses/representations/l17-graphs-as-matrices.json | quiz[1] explain | note | "its rows sum to 1 only when neighbouring degrees match" is loose for one row (a row can sum to 1 by a balance of larger and smaller degrees). All rows sum to 1 exactly when each connected piece is regular, since $\hat{\mathbf A}\mathbf 1 = \mathbf 1$ would make $\mathbf 1$ the top eigenvector. | "... so its rows all sum to 1 only when every node has the same degree."
- app/content/courses/representations/l20-labels-on-a-graph.json | screens[0] option `blue` | note | "almost all of its links go to the left-hand cluster" while the hint and feedback say all 5 do. | "Blue, because all 5 of its links go to the left-hand cluster".
- app/content/courses/representations/l19-a-gcn-layer.json | screens[3] prose | note | "as a `cnn` kernel is shared over positions": `cnn` is not among this level's requirements (`representations/L1`, `markov/L4`, `eigen/L1`, `nn-train/L1`); the brief asked for the clause only if the learner has it. | "as a convolution kernel is shared over positions, if you have met one in `cnn`."
- app/content/courses/representations/l20-labels-on-a-graph.json | screens[2] explain (or l19 screens[7] explain) | note | The level never says the setting is transductive: the unlabelled firms' numbers and links enter training through $\hat{\mathbf A}$, so the 0.972 is for this graph. l19 screen 7's "one trained network runs on a graph of any size" is true mechanically but invites reading it as "transfers to any graph". | Add to l20 screen 2's explain: "The unlabelled firms' numbers and links were used in training, only their labels were not: the score is for this graph, and a new graph needs its own check."

## Code widgets: surviving wrong solutions, unreachable and misrouted feedback

- app/content/courses/representations/l18-passing-messages.json | screens[9] test 6 | warning | The lesson's own trap gets the generic miss: symmetrising the directed graph (W11) and reading the arrows into a node (W12) both fail test 6, which has no byKey line, and no mutant targets the trap. | byKey `test-6`: "On a directed graph row $i$ of $\mathbf A$ lists the arrows out of $i$: average along them, without transposing or symmetrising." Add a mutant `A = np.maximum(A, A.T)` declared on test 6.
- app/content/courses/representations/l20-labels-on-a-graph.json | screens[9] tests | warning | Choosing the weights by accuracy on the unlabelled nodes, a leak of the test labels, passes all 6 tests (W29): the losses are unchanged and at 5 steps the best accuracy is also the last. The homework catches the same leak with a label-flip test (W40, test 8). | Add `round(train_gcn(Ah, X, y, [0, 1, 20, 21], 40, 0.05, 0)[0], 6)` expecting 0.972222 on the lesson's graph: the reference scores 1.0 after 36 and 37 steps and 0.972222 after 40 (my run of the module's trainer), so a solution that keeps its best step reports 1.0. Key it "Report the accuracy of the final weights: choosing the step by the unlabelled nodes' labels uses labels the task does not have."
- app/content/courses/representations/homework-5.json | items[2] | warning | The order item forces lines a to f into one order, but line e (the similar row-stochastic matrix caps every eigenvalue at 1) does not depend on a to d, and line c ($\tilde{\mathbf A}\mathbf 1 = \tilde{\mathbf D}\mathbf 1$) can come before b. A correct proof that bounds the eigenvalues first is marked wrong. | `"after": {"b": ["a"], "d": ["b", "c"], "f": ["d", "e"]}`.
- app/content/courses/representations/l18-passing-messages.json | screens[10] tests | note | Running $k - 1$ steps passes all 8 tests (W17): no test sits where step $k$ is the first to settle. | Add `settles(V, [0, 0, 0, 1], 22, 1e-3)` expecting True (the 22nd step is the first to move every value by less than 0.001: 0.00076; 21 steps give False), keyed "Run exactly $k$ steps."
- app/content/courses/representations/homework-5.json | items[1] tests | note | The non-zero pattern of $\mathbf A^k + \mathbf A^{k-1}$ passes all 7 tests (W50). It is right except at a start node with no links and $k \ge 2$, which no test has (test 6's start node 3 has links). | Add `nodes_within(B, 2, 2)` with test 6's `B` (node 2 is isolated), expecting `[2]`.
- app/content/courses/representations/l20-labels-on-a-graph.json | screens[10] test 3 | note | Test 3 passes a venues matrix rounded to 6 places by hand, which is not quite a normalised adjacency (top eigenvalue 0.9999993). A correct alternative that takes $\mathbf v \propto \sqrt{1/\hat A_{ii}} = \sqrt{\tilde d_i}$ (W32) differs from `eigh`'s vector by 2.8e-7 and fails it with the generic miss. | Build `Va` in the setup from the exact formula (`At = A + np.eye(4); s = 1 / np.sqrt(At.sum(1)); Va = s[:, None] * At * s[None, :]`) and recompute the expected list.
- app/content/courses/representations/l20 screens[9] byKey test-5; l20 screens[10] byKey test-2, test-4; homework-5 items[1] byKey test-3 | unreachable lines | note | Every named mutant and every wrong solution I tried fails an earlier test (test 1 in each widget), so these lines never show. The earlier lines already name the same faults (l20 screen 10's test-1 line covers the entrywise power and the part outside $\mathbf v$; the homework's test-1 line covers $k$ rounds). Two other unpaired lines are reachable: l17 screen 10 test-6 (W7, an in-place `fill_diagonal`) and l18 screen 10 test-4 (W16, a loop that ignores $k$). | Delete the four unreachable lines.
- docs/ENGINE-BACKLOG.md (proposed) | grade-all `--code` | note | SESSION PROTOCOL 6: "a byKey test-N line no mutant reaches" has now been raised in review-representations-1, twelve times in review-representations-24 and four times here, and no engine item exists. | Engine item: `grade-all --code` warns on a `byKey` test-N that no mutant's declared test names, and on a mutant whose declared test has no `byKey` line.
- several widgets | harmless survivors | note | Six variants pass and are harmless (appendix): degrees from axis 0 on a symmetric matrix (W8, W43), $\mathbf D^{-1/2}\mathbf A\mathbf D^{-1/2}$ or $\mathbf A\mathbf D^{-1}$ in `settles`, which are similar to $\mathbf P$, so the step-to-step changes vanish at the same rate (W14, W15), and `<=` for `<` (W18, W25). Recorded so nobody adds a test for them. | None.

## Automated checks (no finding)

- Number script: CI runner 1 of 1 passed, 4 s; direct strict runs exit 0 with 312 of 312 checks, 0 uncovered, 5 literals (2,000 and 150 firms, the hidden-test settings, 30 layers, width 16), the same under default threads and one thread. Frozen modules byte-identical (`autograd.py` `5917d4ec91f7`, `nt_ops_l1.py` `9c1391a33624`, `representations_ops_l1.py` `097ac4d78867`). The hand-backprop trainer matches `train_gcn_params` over 30 steps to 1e-9; every code widget's solution and twin pass in CPython; each graded threshold holds with margin on four seeds (at least 0.9 against 0.85, 0.85 against 0.8, at most 0.7 against 0.75).
- `grade-all.mjs --code`, each file alone: 0 failures (l17 13 widgets and 2 code, l18 12 and 2, l19 11 and 2, l20 12 and 3, review 9, homework 4 and 2, problems 12). `same-course-reuse.mjs --all`: no error line for representations.
- Every stated number recomputed: l17's degrees 3, 2, 2, 1 (8), 10, 3.33, 3.5, 0.408, 0.5, 0.167, 0.707, 4, 5.5, the venues' $\hat{\mathbf A}$ heat cells (0.25, 0.289, 0.354, 0.333, 0.5), row sum 1.18, 0.204, 0.258, 0.042, 0.354, 0.577, 14; l18's hook frames ($\tfrac13$; $\tfrac16, \tfrac16, \tfrac13$; $\tfrac29, \tfrac1{12}, \tfrac1{12}, 0$), $\tfrac18$, 3, 2, the two-step reach (S, a, f, b, d, matching the canvas edges), 1 against $\tfrac13$, $(\tfrac{10}3, 6)$, 7, 9, 4, 13, the square's $\tfrac12$ and $\tfrac14$, 2.5 against 3, 0.1, 0.2, 0.25, 4.5, 1.6, 2; l19's weights 0.333 and 0.289, $(-0.51, 0.32)$, slips $-0.53$ and $-1.6$, node 4's $(-0.77, 0.69)$, 3.19, 3.98, 7.95, $-5.75$, 64, 1,280,000, 8, 32, the six nodes within two links (matching the 37 canvas edges), 5.7 and $-3.05$, all 20 nodes labelled by the supplied network, 2.68, 2.5, 10, 352, 768, 387, 3, 0 and $-1$; l20's 35 and 21 of 36, 0.972, 0.975, 14, means 0.95 and 0.60, training accuracy 1.0 for both networks (final losses 0.0002 and 0.0014), the $k$-step bars, 16 layers 0.55 with 14 of 20 losses above 0.6, no-signal 0.57, $\sqrt{2/11} = 0.426$, 0.182, 0.316, the spread bars, 0.82, 0.85, 0.5, 0.25, 0.447; firm 3's five links all to firms 0 to 19 and its first number 1.88; review's 0.258, 0.354, 0.067, 0.2, 4, 3, 12, 3, 2, 5, 112, 48, 130, 3, 2, 2.667, 44; homework's 2.8, 5, 3, 10, 9, 4, 13 and the rubric's 10 points; problems' 0.25, 0.3333, 0.289, 0.408, 0.083, 2.577, 2.667, 0.577, 3.87, $-2.58$, 2.58, 3, 2, 6, 1.5, 0, 1.714, 1.225, 1.414, 80, 64, 96, 0.8, 0.81, 85, 180.
- Distractors: every `wrong` value reproduced from its `why`, and `grade-all` routes each to its line. Graph canvases: l17 screen 0 draws D on the left (x 0.1), as the `miss` line says.
- Voice: `voice-scan.py 35 --summary` finds 0 sentences over 35 words, 0 explanations over three sentences, 0 doubled words and 0 lesson ids in code spans in level 5 (the one sentence over 35 words in the course is l10's `how`, level 3); no em-dashes, exclamation marks or American spellings in the level's learner text.

## Appendix: wrong solutions run through the grader

How: each source was graded through `tools/code-runner.mjs` (`makeRunner(...).grade(widget, source, 'tests')`, the page's harness and per-case limits under the local Pyodide 0.27.7) by `rv24/wrongs.mjs`; most are the authored solution with one change, built by `rv5/build_wrongs5.py`, which asserts that each change applies. "Shown" names the byKey line the page would show; "no byKey line" means the generic miss. The brief's list maps to: no self-loops W4, W38 (and W2, loops where none are asked); row normalisation where symmetric is taught W5, W37, and the reverse W3, W9, W14 (harmless); degree from the wrong axis W1, W10, W15 (harmless), W8 and W43 (harmless on symmetric input); directed graphs W11, W12; neighbours within $k$ leaving out node $i$ or stopping at $k - 1$ W46, W47, W51 (the task counts node $i$ itself, so counting it is correct), and W45, W48, W50 (SURVIVES); training on test nodes' labels W28, W44, and test labels used for model selection W29 (SURVIVES), W40; no gradient zeroing W26, W27, W39.

Results: 38 wrong solutions, 35 caught, 3 SURVIVE; 6 harmless variants, 6 pass; 7 correct alternatives, 6 pass, 1 fails.

### l17-graphs-as-matrices screens[9] `adjacency`, `row_normalised` (6 hidden tests)

- W1. row_normalised without keepdims: divides column j by d_j (degree on the wrong axis): **fails T4** (byKey `test-4` shown).

```python
import numpy as np


def adjacency(edges, n):
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = 1.0
        A[j, i] = 1.0
    return A


def row_normalised(A):
    A = np.asarray(A, dtype=float)
    return A / A.sum(axis=1)
```

- W2. row_normalised adds self-loops first (D~^-1 A~ where D^-1 A is asked): **fails T4** (byKey `test-4` shown).

```python
import numpy as np


def adjacency(edges, n):
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = 1.0
        A[j, i] = 1.0
    return A


def row_normalised(A):
    A = np.asarray(A, dtype=float) + np.eye(len(A))
    return A / A.sum(axis=1, keepdims=True)
```

- W3. row_normalised symmetric D^-1/2 A D^-1/2 where row normalisation is taught: **fails T4** (byKey `test-4` shown).

```python
import numpy as np


def adjacency(edges, n):
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = 1.0
        A[j, i] = 1.0
    return A


def row_normalised(A):
    A = np.asarray(A, dtype=float)
    s = 1 / np.sqrt(A.sum(axis=1))
    return s[:, None] * A * s[None, :]
```


### l17-graphs-as-matrices screens[10] `normalised_adjacency` (6 hidden tests)

- W4. no self-loops, isolated degree guarded to 1: **fails T1** (byKey `test-1` shown).

```python
import numpy as np


def normalised_adjacency(A):
    A = np.asarray(A, dtype=float)
    At = A
    s = 1.0 / np.sqrt(np.maximum(At.sum(axis=1), 1))
    return s[:, None] * At * s[None, :]
```

- W5. row normalisation D~^-1 A~ where symmetric is taught (scales rows by 1/d~ only): **fails T1** (byKey `test-1` shown).

```python
import numpy as np


def normalised_adjacency(A):
    A = np.asarray(A, dtype=float)
    At = A + np.eye(len(A))
    s = 1.0 / np.sqrt(At.sum(axis=1))
    return (s ** 2)[:, None] * At
```

- W6. divides by d~_i d~_j without the square root: **fails T1** (byKey `test-1` shown).

```python
import numpy as np


def normalised_adjacency(A):
    A = np.asarray(A, dtype=float)
    At = A + np.eye(len(A))
    s = 1.0 / At.sum(axis=1)
    return s[:, None] * At * s[None, :]
```

- W7. sets the caller's diagonal to 1 in place (np.fill_diagonal), idempotent: **fails T6** (byKey `test-6` shown).

```python
import numpy as np


def normalised_adjacency(A):
    A = np.asarray(A, dtype=float)
    np.fill_diagonal(A, 1.0)
    s = 1.0 / np.sqrt(A.sum(axis=1))
    return s[:, None] * A * s[None, :]
```

- W8. [harmless: same result on every input the widget allows] degrees from the columns (axis 0); same on a symmetric A: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def normalised_adjacency(A):
    A = np.asarray(A, dtype=float)
    At = A + np.eye(len(A))
    s = 1.0 / np.sqrt(At.sum(axis=0))
    return s[:, None] * At * s[None, :]
```


### l18-passing-messages screens[9] `message_step`, `k_steps` (7 hidden tests)

- W9. symmetric normalisation D^-1/2 A D^-1/2 where row averaging is taught: **fails T1** (byKey `test-1` shown).

```python
import numpy as np


def message_step(A, X, self_loops):
    A = np.asarray(A, dtype=float)
    if self_loops:
        A = A + np.eye(len(A))
    s = 1 / np.sqrt(A.sum(axis=1))
    P = s[:, None] * A * s[None, :]
    return P @ np.asarray(X, dtype=float)


def k_steps(A, X, k):
    for _ in range(k):
        X = message_step(A, X, False)
    return np.asarray(X, dtype=float)
```

- W10. no keepdims: divides column j by node j's degree: **fails T1** (byKey `test-1` shown).

```python
import numpy as np


def message_step(A, X, self_loops):
    A = np.asarray(A, dtype=float)
    if self_loops:
        A = A + np.eye(len(A))
    P = A / A.sum(axis=1)
    return P @ np.asarray(X, dtype=float)


def k_steps(A, X, k):
    for _ in range(k):
        X = message_step(A, X, False)
    return np.asarray(X, dtype=float)
```

- W11. symmetrises the directed graph (messages along arrows both ways): **fails T6** (no byKey line: generic feedback).

```python
import numpy as np


def message_step(A, X, self_loops):
    A = np.asarray(A, dtype=float)
    A = np.maximum(A, A.T)
    if self_loops:
        A = A + np.eye(len(A))
    P = A / A.sum(axis=1, keepdims=True)
    return P @ np.asarray(X, dtype=float)


def k_steps(A, X, k):
    for _ in range(k):
        X = message_step(A, X, False)
    return np.asarray(X, dtype=float)
```

- W12. directed graph read along incoming arrows (A^T): **fails T6** (no byKey line: generic feedback).

```python
import numpy as np


def message_step(A, X, self_loops):
    A = np.asarray(A, dtype=float).T
    if self_loops:
        A = A + np.eye(len(A))
    P = A / A.sum(axis=1, keepdims=True)
    return P @ np.asarray(X, dtype=float)


def k_steps(A, X, k):
    for _ in range(k):
        X = message_step(A, X, False)
    return np.asarray(X, dtype=float)
```

- W13. k_steps runs k + 1 steps: **fails T4** (byKey `test-4` shown).

```python
import numpy as np


def message_step(A, X, self_loops):
    A = np.asarray(A, dtype=float)
    if self_loops:
        A = A + np.eye(len(A))
    P = A / A.sum(axis=1, keepdims=True)
    return P @ np.asarray(X, dtype=float)


def k_steps(A, X, k):
    for _ in range(k + 1):
        X = message_step(A, X, False)
    return np.asarray(X, dtype=float)
```


### l18-passing-messages screens[10] `settles` (8 hidden tests)

- W14. [harmless: same result on every input the widget allows] symmetric normalisation D^-1/2 A D^-1/2 (similar to P, same spectrum): **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def settles(A, x, k, tol):
    A = np.asarray(A, dtype=float)
    s = 1 / np.sqrt(A.sum(axis=1))
    P = s[:, None] * A * s[None, :]
    x = np.asarray(x, dtype=float)
    prev = x
    for _ in range(k):
        prev, x = x, P @ x
    return bool(np.max(np.abs(x - prev)) < tol)
```

- W15. [harmless: same result on every input the widget allows] column-normalised A D^-1 (degree from the wrong axis; similar to P): **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def settles(A, x, k, tol):
    A = np.asarray(A, dtype=float)
    P = A / A.sum(axis=0, keepdims=True)
    x = np.asarray(x, dtype=float)
    prev = x
    for _ in range(k):
        prev, x = x, P @ x
    return bool(np.max(np.abs(x - prev)) < tol)
```

- W16. ignores k: iterates until the change is below tol (at most 10,000 steps): **fails T4** (byKey `test-4` shown).

```python
import numpy as np


def settles(A, x, k, tol):
    A = np.asarray(A, dtype=float)
    P = A / A.sum(axis=1, keepdims=True)
    x = np.asarray(x, dtype=float)
    for _ in range(10000):
        new = P @ x
        if np.max(np.abs(new - x)) < tol:
            return True
        x = new
    return False
```

- W17. runs k - 1 steps: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def settles(A, x, k, tol):
    A = np.asarray(A, dtype=float)
    P = A / A.sum(axis=1, keepdims=True)
    x = np.asarray(x, dtype=float)
    prev = x
    for _ in range(k - 1):
        prev, x = x, P @ x
    return bool(np.max(np.abs(x - prev)) < tol)
```

- W18. [harmless: same result on every input the widget allows] <= tol instead of < tol: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def settles(A, x, k, tol):
    A = np.asarray(A, dtype=float)
    P = A / A.sum(axis=1, keepdims=True)
    x = np.asarray(x, dtype=float)
    prev = x
    for _ in range(k):
        prev, x = x, P @ x
    return bool(np.max(np.abs(x - prev)) <= tol)
```


### l19-a-gcn-layer screens[8] `gcn_layer`, `gcn_layer_loop` (7 hidden tests)

- W19. loop applies ReLU to each neighbour term before summing: **fails T3** (byKey `test-3` shown).

```python
import numpy as np


def gcn_layer(A_hat, H, W):
    return np.maximum(np.asarray(A_hat) @ np.asarray(H) @ np.asarray(W), 0.0)


def gcn_layer_loop(A_hat, H, W):
    A_hat, H, W = np.asarray(A_hat), np.asarray(H), np.asarray(W)
    out = np.zeros((len(H), W.shape[1]))
    for i in range(len(H)):
        mixed = np.zeros(H.shape[1])
        for j in range(len(H)):
            if A_hat[i, j] != 0:
                mixed += np.maximum(A_hat[i, j] * H[j] @ W, 0.0)
        out[i] = mixed
    return out
```

- W20. [correct alternative] loop multiplies each neighbour row by W first, then sums (same layer): **passes**.

```python
import numpy as np


def gcn_layer(A_hat, H, W):
    return np.maximum(np.asarray(A_hat) @ np.asarray(H) @ np.asarray(W), 0.0)


def gcn_layer_loop(A_hat, H, W):
    A_hat, H, W = np.asarray(A_hat), np.asarray(H), np.asarray(W)
    out = np.zeros((len(H), W.shape[1]))
    for i in range(len(H)):
        mixed = np.zeros(W.shape[1])
        for j in range(len(H)):
            if A_hat[i, j] != 0:
                mixed += A_hat[i, j] * (H[j] @ W)
        out[i] = np.maximum(mixed, 0.0)
    return out
```

- W21. [correct alternative] loop with a binary mask: sums h_j over the neighbourhood, divided by sqrt(d_i d_j) recomputed from the mask: **passes**.

```python
import numpy as np


def gcn_layer(A_hat, H, W):
    return np.maximum(np.asarray(A_hat) @ np.asarray(H) @ np.asarray(W), 0.0)


def gcn_layer_loop(A_hat, H, W):
    A_hat, H, W = np.asarray(A_hat), np.asarray(H), np.asarray(W)
    out = np.zeros((len(H), W.shape[1]))
    for i in range(len(H)):
        mixed = np.zeros(H.shape[1])
        for j in range(len(H)):
            if A_hat[i, j] != 0:
                mixed += H[j] / np.sqrt((A_hat[i] != 0).sum() * (A_hat[j] != 0).sum())
        out[i] = np.maximum(mixed @ W, 0.0)
    return out
```


### l19-a-gcn-layer screens[9] `gcn_forward`, `gcn_params` (6 hidden tests)

- W22. first layer without A_hat (ReLU(X W1)): **fails T1** (byKey `test-1` shown).

```python
import numpy as np


def gcn_forward(A_hat, X, params):
    W1, W2 = params
    H = np.maximum(X @ W1, 0.0)
    return A_hat @ H @ W2


def gcn_params(d_in, d_hidden, d_out):
    return d_in * d_hidden + d_hidden * d_out
```

- W23. gcn_params adds a d_hidden x d_hidden matrix: **fails T4** (byKey `test-4` shown).

```python
import numpy as np


def gcn_forward(A_hat, X, params):
    W1, W2 = params
    H = np.maximum(A_hat @ X @ W1, 0.0)
    return A_hat @ H @ W2


def gcn_params(d_in, d_hidden, d_out):
    return d_in * d_hidden + d_hidden * d_hidden + d_hidden * d_out
```


### l20-labels-on-a-graph screens[8] `planted_partition` (6 hidden tests)

- W24. reads the lower triangle U[j, i] (j > i): **fails T1** (byKey `test-1` shown).

```python
import numpy as np


def planted_partition(n, p_in, p_out, seed):
    U = np.random.default_rng(seed).random((n, n))
    y = (np.arange(n) >= n // 2).astype(int)
    P = np.where(y[:, None] == y[None, :], p_in, p_out)
    A = np.tril((U < P).astype(float), -1)
    return A + A.T, y
```

- W25. [harmless: same result on every input the widget allows] <= in place of < on the uniform draw: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def planted_partition(n, p_in, p_out, seed):
    U = np.random.default_rng(seed).random((n, n))
    y = (np.arange(n) >= n // 2).astype(int)
    P = np.where(y[:, None] == y[None, :], p_in, p_out)
    A = np.triu((U <= P).astype(float), 1)
    return A + A.T, y
```


### l20-labels-on-a-graph screens[9] `train_gcn` (6 hidden tests)

- W26. no gradient zeroing: tensors made once and updated in place, gradients accumulate: **fails T1** (byKey `test-1` shown).

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step


def train_gcn(A_hat, X, y, train_idx, steps, lr, seed):
    A_hat = np.asarray(A_hat, dtype=float)
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    tr = np.asarray(train_idx)
    K = int(y.max()) + 1
    rng = np.random.default_rng(seed)
    W = [rng.standard_normal((X.shape[1], 16)) / np.sqrt(X.shape[1]),
         rng.standard_normal((16, K)) / np.sqrt(16)]
    m = [np.zeros_like(w) for w in W]
    v = [np.zeros_like(w) for w in W]
    losses = []
    W1, W2 = Tensor(W[0]), Tensor(W[1])
    for t in range(1, steps + 1):
        W1.data, W2.data = W[0], W[1]
        logits = A_hat @ (A_hat @ X @ W1).relu() @ W2
        loss = cross_entropy(logits[tr], y[tr])
        loss.backward()
        losses.append(loss.item())
        W, m, v = adam_step(W, [W1.grad, W2.grad], m, v, t, lr)
    pred = (A_hat @ np.maximum(A_hat @ X @ W[0], 0) @ W[1]).argmax(axis=1)
    other = np.setdiff1d(np.arange(len(y)), tr)
    return float(np.mean(pred[other] == y[other])), losses
```

- W27. zero_grad called after backward, so Adam sees zero gradients: **fails T1** (byKey `test-1` shown).

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step


def train_gcn(A_hat, X, y, train_idx, steps, lr, seed):
    A_hat = np.asarray(A_hat, dtype=float)
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    tr = np.asarray(train_idx)
    K = int(y.max()) + 1
    rng = np.random.default_rng(seed)
    W = [rng.standard_normal((X.shape[1], 16)) / np.sqrt(X.shape[1]),
         rng.standard_normal((16, K)) / np.sqrt(16)]
    m = [np.zeros_like(w) for w in W]
    v = [np.zeros_like(w) for w in W]
    losses = []
    for t in range(1, steps + 1):
        W1, W2 = Tensor(W[0]), Tensor(W[1])
        logits = A_hat @ (A_hat @ X @ W1).relu() @ W2
        loss = cross_entropy(logits[tr], y[tr])
        loss.backward()
        W1.zero_grad(); W2.zero_grad()
        losses.append(loss.item())
        W, m, v = adam_step(W, [W1.grad, W2.grad], m, v, t, lr)
    pred = (A_hat @ np.maximum(A_hat @ X @ W[0], 0) @ W[1]).argmax(axis=1)
    other = np.setdiff1d(np.arange(len(y)), tr)
    return float(np.mean(pred[other] == y[other])), losses
```

- W28. trains on every node: loss over all 40 labels (test nodes included): **fails T1** (byKey `test-1` shown).

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step


def train_gcn(A_hat, X, y, train_idx, steps, lr, seed):
    A_hat = np.asarray(A_hat, dtype=float)
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    tr = np.asarray(train_idx)
    K = int(y.max()) + 1
    rng = np.random.default_rng(seed)
    W = [rng.standard_normal((X.shape[1], 16)) / np.sqrt(X.shape[1]),
         rng.standard_normal((16, K)) / np.sqrt(16)]
    m = [np.zeros_like(w) for w in W]
    v = [np.zeros_like(w) for w in W]
    losses = []
    for t in range(1, steps + 1):
        W1, W2 = Tensor(W[0]), Tensor(W[1])
        logits = A_hat @ (A_hat @ X @ W1).relu() @ W2
        loss = cross_entropy(logits, y)
        loss.backward()
        losses.append(loss.item())
        W, m, v = adam_step(W, [W1.grad, W2.grad], m, v, t, lr)
    pred = (A_hat @ np.maximum(A_hat @ X @ W[0], 0) @ W[1]).argmax(axis=1)
    other = np.setdiff1d(np.arange(len(y)), tr)
    return float(np.mean(pred[other] == y[other])), losses
```

- W29. model selection on the test labels: keeps the weights of the step with the best accuracy on the other nodes: **SURVIVES (passes every hidden test)**.

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step


def train_gcn(A_hat, X, y, train_idx, steps, lr, seed):
    A_hat = np.asarray(A_hat, dtype=float)
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    tr = np.asarray(train_idx)
    K = int(y.max()) + 1
    rng = np.random.default_rng(seed)
    W = [rng.standard_normal((X.shape[1], 16)) / np.sqrt(X.shape[1]),
         rng.standard_normal((16, K)) / np.sqrt(16)]
    m = [np.zeros_like(w) for w in W]
    v = [np.zeros_like(w) for w in W]
    losses = []
    other = np.setdiff1d(np.arange(len(y)), tr)
    best, bestW = -1, W
    for t in range(1, steps + 1):
        W1, W2 = Tensor(W[0]), Tensor(W[1])
        logits = A_hat @ (A_hat @ X @ W1).relu() @ W2
        loss = cross_entropy(logits[tr], y[tr])
        loss.backward()
        losses.append(loss.item())
        acc = float(np.mean(logits.data.argmax(axis=1)[other] == y[other]))
        if acc > best:
            best, bestW = acc, W
        W, m, v = adam_step(W, [W1.grad, W2.grad], m, v, t, lr)
    W = bestW
    pred = (A_hat @ np.maximum(A_hat @ X @ W[0], 0) @ W[1]).argmax(axis=1)
    other = np.setdiff1d(np.arange(len(y)), tr)
    return float(np.mean(pred[other] == y[other])), losses
```

- W30. W2 drawn before W1: **fails T1** (byKey `test-1` shown).

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step


def train_gcn(A_hat, X, y, train_idx, steps, lr, seed):
    A_hat = np.asarray(A_hat, dtype=float)
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    tr = np.asarray(train_idx)
    K = int(y.max()) + 1
    rng = np.random.default_rng(seed)
    W2_ = rng.standard_normal((16, K)) / np.sqrt(16)
    W = [rng.standard_normal((X.shape[1], 16)) / np.sqrt(X.shape[1]), W2_]
    m = [np.zeros_like(w) for w in W]
    v = [np.zeros_like(w) for w in W]
    losses = []
    for t in range(1, steps + 1):
        W1, W2 = Tensor(W[0]), Tensor(W[1])
        logits = A_hat @ (A_hat @ X @ W1).relu() @ W2
        loss = cross_entropy(logits[tr], y[tr])
        loss.backward()
        losses.append(loss.item())
        W, m, v = adam_step(W, [W1.grad, W2.grad], m, v, t, lr)
    pred = (A_hat @ np.maximum(A_hat @ X @ W[0], 0) @ W[1]).argmax(axis=1)
    other = np.setdiff1d(np.arange(len(y)), tr)
    return float(np.mean(pred[other] == y[other])), losses
```

- W31. [correct alternative] accuracy with np.delete instead of setdiff1d: **passes**.

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step


def train_gcn(A_hat, X, y, train_idx, steps, lr, seed):
    A_hat = np.asarray(A_hat, dtype=float)
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    tr = np.asarray(train_idx)
    K = int(y.max()) + 1
    rng = np.random.default_rng(seed)
    W = [rng.standard_normal((X.shape[1], 16)) / np.sqrt(X.shape[1]),
         rng.standard_normal((16, K)) / np.sqrt(16)]
    m = [np.zeros_like(w) for w in W]
    v = [np.zeros_like(w) for w in W]
    losses = []
    for t in range(1, steps + 1):
        W1, W2 = Tensor(W[0]), Tensor(W[1])
        logits = A_hat @ (A_hat @ X @ W1).relu() @ W2
        loss = cross_entropy(logits[tr], y[tr])
        loss.backward()
        losses.append(loss.item())
        W, m, v = adam_step(W, [W1.grad, W2.grad], m, v, t, lr)
    pred = (A_hat @ np.maximum(A_hat @ X @ W[0], 0) @ W[1]).argmax(axis=1)
    other = np.delete(np.arange(len(y)), tr)
    return float(np.mean(pred[other] == y[other])), losses
```


### l20-labels-on-a-graph screens[10] `feature_spread` (5 hidden tests)

- W32. [correct alternative] top eigenvector from the diagonal: v = sqrt(1 / diag(A_hat)), normalised: **fails T3** (no byKey line: generic feedback).

```python
import numpy as np


def feature_spread(A_hat, X, depth):
    A_hat = np.asarray(A_hat, dtype=float)
    Z = np.asarray(X, dtype=float)
    v = np.sqrt(1 / np.diag(A_hat))
    v = v / np.linalg.norm(v)
    out = []
    for k in range(depth + 1):
        out.append(float(np.linalg.norm(Z - np.outer(v, v @ Z)) / np.linalg.norm(Z)))
        Z = A_hat @ Z
    return out
```

- W33. [correct alternative] top eigenvector by 2,000 steps of power iteration: **passes**.

```python
import numpy as np


def feature_spread(A_hat, X, depth):
    A_hat = np.asarray(A_hat, dtype=float)
    Z = np.asarray(X, dtype=float)
    v = np.ones(len(A_hat))
    for _ in range(2000):
        v = A_hat @ v
        v = v / np.linalg.norm(v)
    out = []
    for k in range(depth + 1):
        out.append(float(np.linalg.norm(Z - np.outer(v, v @ Z)) / np.linalg.norm(Z)))
        Z = A_hat @ Z
    return out
```

- W34. spectral norm (ord 2) in place of the Frobenius norm: **fails T1** (byKey `test-1` shown).

```python
import numpy as np


def feature_spread(A_hat, X, depth):
    A_hat = np.asarray(A_hat, dtype=float)
    Z = np.asarray(X, dtype=float)
    lam, V = np.linalg.eigh(A_hat)
    v = V[:, -1]
    out = []
    for k in range(depth + 1):
        out.append(float(np.linalg.norm(Z - np.outer(v, v @ Z), 2) / np.linalg.norm(Z, 2)))
        Z = A_hat @ Z
    return out
```

- W35. squared share (norms squared): **fails T1** (byKey `test-1` shown).

```python
import numpy as np


def feature_spread(A_hat, X, depth):
    A_hat = np.asarray(A_hat, dtype=float)
    Z = np.asarray(X, dtype=float)
    lam, V = np.linalg.eigh(A_hat)
    v = V[:, -1]
    out = []
    for k in range(depth + 1):
        out.append(float((np.linalg.norm(Z - np.outer(v, v @ Z)) / np.linalg.norm(Z)) ** 2))
        Z = A_hat @ Z
    return out
```

- W36. stops at depth - 1: **fails T1** (byKey `test-1` shown).

```python
import numpy as np


def feature_spread(A_hat, X, depth):
    A_hat = np.asarray(A_hat, dtype=float)
    Z = np.asarray(X, dtype=float)
    lam, V = np.linalg.eigh(A_hat)
    v = V[:, -1]
    out = []
    for k in range(depth):
        out.append(float(np.linalg.norm(Z - np.outer(v, v @ Z)) / np.linalg.norm(Z)))
        Z = A_hat @ Z
    return out
```


### homework-5 items[0] `gcn_node_classifier` (10 hidden tests)

- W37. row normalisation D~^-1 A~ where symmetric is taught: **fails T1** (byKey `test-1` shown).

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step


def gcn_node_classifier(edges, X, y, train_idx, layers, steps, lr, seed):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    tr = np.asarray(train_idx)
    n = len(X)
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = A[j, i] = 1.0
    At = A + np.eye(n)
    s = 1.0 / np.sqrt(At.sum(axis=1))
    Ah = At / At.sum(axis=1, keepdims=True)
    sizes = [X.shape[1]] + [16] * (layers - 1) + [int(y.max()) + 1]
    rng = np.random.default_rng(seed)
    W = [rng.standard_normal((a, b)) / np.sqrt(a) for a, b in zip(sizes[:-1], sizes[1:])]
    m = [np.zeros_like(w) for w in W]
    v = [np.zeros_like(w) for w in W]
    losses = []
    for t in range(1, steps + 1):
        P = [Tensor(w) for w in W]
        h = Tensor(X)
        for k, p in enumerate(P):
            h = Ah @ h @ p
            if k < len(P) - 1:
                h = h.relu()
        loss = cross_entropy(h[tr], y[tr])
        loss.backward()
        losses.append(loss.item())
        W, m, v = adam_step(W, [p.grad for p in P], m, v, t, lr)
    h = X
    for k, w in enumerate(W):
        h = Ah @ h @ w
        if k < len(W) - 1:
            h = np.maximum(h, 0.0)
    return h.argmax(axis=1), losses
```

- W38. no self-loops, isolated degree guarded to 1: **fails T1** (byKey `test-1` shown).

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step


def gcn_node_classifier(edges, X, y, train_idx, layers, steps, lr, seed):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    tr = np.asarray(train_idx)
    n = len(X)
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = A[j, i] = 1.0
    At = A
    s = 1.0 / np.sqrt(np.maximum(At.sum(axis=1), 1))
    Ah = s[:, None] * At * s[None, :]
    sizes = [X.shape[1]] + [16] * (layers - 1) + [int(y.max()) + 1]
    rng = np.random.default_rng(seed)
    W = [rng.standard_normal((a, b)) / np.sqrt(a) for a, b in zip(sizes[:-1], sizes[1:])]
    m = [np.zeros_like(w) for w in W]
    v = [np.zeros_like(w) for w in W]
    losses = []
    for t in range(1, steps + 1):
        P = [Tensor(w) for w in W]
        h = Tensor(X)
        for k, p in enumerate(P):
            h = Ah @ h @ p
            if k < len(P) - 1:
                h = h.relu()
        loss = cross_entropy(h[tr], y[tr])
        loss.backward()
        losses.append(loss.item())
        W, m, v = adam_step(W, [p.grad for p in P], m, v, t, lr)
    h = X
    for k, w in enumerate(W):
        h = Ah @ h @ w
        if k < len(W) - 1:
            h = np.maximum(h, 0.0)
    return h.argmax(axis=1), losses
```

- W39. no gradient zeroing: tensors made once, gradients accumulate: **fails T1** (byKey `test-1` shown).

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step


def gcn_node_classifier(edges, X, y, train_idx, layers, steps, lr, seed):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    tr = np.asarray(train_idx)
    n = len(X)
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = A[j, i] = 1.0
    At = A + np.eye(n)
    s = 1.0 / np.sqrt(At.sum(axis=1))
    Ah = s[:, None] * At * s[None, :]
    sizes = [X.shape[1]] + [16] * (layers - 1) + [int(y.max()) + 1]
    rng = np.random.default_rng(seed)
    W = [rng.standard_normal((a, b)) / np.sqrt(a) for a, b in zip(sizes[:-1], sizes[1:])]
    m = [np.zeros_like(w) for w in W]
    v = [np.zeros_like(w) for w in W]
    losses = []
    P = [Tensor(w) for w in W]
    for t in range(1, steps + 1):
        for p, w in zip(P, W):
            p.data = w
        h = Tensor(X)
        for k, p in enumerate(P):
            h = Ah @ h @ p
            if k < len(P) - 1:
                h = h.relu()
        loss = cross_entropy(h[tr], y[tr])
        loss.backward()
        losses.append(loss.item())
        W, m, v = adam_step(W, [p.grad for p in P], m, v, t, lr)
    h = X
    for k, w in enumerate(W):
        h = Ah @ h @ w
        if k < len(W) - 1:
            h = np.maximum(h, 0.0)
    return h.argmax(axis=1), losses
```

- W40. model selection on every label: returns the predictions of the step with the best accuracy over all nodes: **fails T8** (byKey `test-8` shown).

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step


def gcn_node_classifier(edges, X, y, train_idx, layers, steps, lr, seed):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    tr = np.asarray(train_idx)
    n = len(X)
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = A[j, i] = 1.0
    At = A + np.eye(n)
    s = 1.0 / np.sqrt(At.sum(axis=1))
    Ah = s[:, None] * At * s[None, :]
    sizes = [X.shape[1]] + [16] * (layers - 1) + [int(y.max()) + 1]
    rng = np.random.default_rng(seed)
    W = [rng.standard_normal((a, b)) / np.sqrt(a) for a, b in zip(sizes[:-1], sizes[1:])]
    m = [np.zeros_like(w) for w in W]
    v = [np.zeros_like(w) for w in W]
    losses = []
    best, bestW = -1, W
    for t in range(1, steps + 1):
        P = [Tensor(w) for w in W]
        h = Tensor(X)
        for k, p in enumerate(P):
            h = Ah @ h @ p
            if k < len(P) - 1:
                h = h.relu()
        loss = cross_entropy(h[tr], y[tr])
        loss.backward()
        losses.append(loss.item())
        acc = float(np.mean(h.data.argmax(axis=1) == y))
        if acc > best:
            best, bestW = acc, W
        W, m, v = adam_step(W, [p.grad for p in P], m, v, t, lr)
    W = bestW
    h = X
    for k, w in enumerate(W):
        h = Ah @ h @ w
        if k < len(W) - 1:
            h = np.maximum(h, 0.0)
    return h.argmax(axis=1), losses
```

- W41. [correct alternative] number of classes from the training labels only: **passes**.

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step


def gcn_node_classifier(edges, X, y, train_idx, layers, steps, lr, seed):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    tr = np.asarray(train_idx)
    n = len(X)
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = A[j, i] = 1.0
    At = A + np.eye(n)
    s = 1.0 / np.sqrt(At.sum(axis=1))
    Ah = s[:, None] * At * s[None, :]
    sizes = [X.shape[1]] + [16] * (layers - 1) + [int(y[tr].max()) + 1]
    rng = np.random.default_rng(seed)
    W = [rng.standard_normal((a, b)) / np.sqrt(a) for a, b in zip(sizes[:-1], sizes[1:])]
    m = [np.zeros_like(w) for w in W]
    v = [np.zeros_like(w) for w in W]
    losses = []
    for t in range(1, steps + 1):
        P = [Tensor(w) for w in W]
        h = Tensor(X)
        for k, p in enumerate(P):
            h = Ah @ h @ p
            if k < len(P) - 1:
                h = h.relu()
        loss = cross_entropy(h[tr], y[tr])
        loss.backward()
        losses.append(loss.item())
        W, m, v = adam_step(W, [p.grad for p in P], m, v, t, lr)
    h = X
    for k, w in enumerate(W):
        h = Ah @ h @ w
        if k < len(W) - 1:
            h = np.maximum(h, 0.0)
    return h.argmax(axis=1), losses
```

- W42. weights scaled by sqrt(fan-out): **fails T1** (byKey `test-1` shown).

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step


def gcn_node_classifier(edges, X, y, train_idx, layers, steps, lr, seed):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    tr = np.asarray(train_idx)
    n = len(X)
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = A[j, i] = 1.0
    At = A + np.eye(n)
    s = 1.0 / np.sqrt(At.sum(axis=1))
    Ah = s[:, None] * At * s[None, :]
    sizes = [X.shape[1]] + [16] * (layers - 1) + [int(y.max()) + 1]
    rng = np.random.default_rng(seed)
    W = [rng.standard_normal((a, b)) / np.sqrt(b) for a, b in zip(sizes[:-1], sizes[1:])]
    m = [np.zeros_like(w) for w in W]
    v = [np.zeros_like(w) for w in W]
    losses = []
    for t in range(1, steps + 1):
        P = [Tensor(w) for w in W]
        h = Tensor(X)
        for k, p in enumerate(P):
            h = Ah @ h @ p
            if k < len(P) - 1:
                h = h.relu()
        loss = cross_entropy(h[tr], y[tr])
        loss.backward()
        losses.append(loss.item())
        W, m, v = adam_step(W, [p.grad for p in P], m, v, t, lr)
    h = X
    for k, w in enumerate(W):
        h = Ah @ h @ w
        if k < len(W) - 1:
            h = np.maximum(h, 0.0)
    return h.argmax(axis=1), losses
```

- W43. [harmless: same result on every input the widget allows] degrees from the columns (axis 0); same for an undirected graph: **SURVIVES (passes every hidden test)**.

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step


def gcn_node_classifier(edges, X, y, train_idx, layers, steps, lr, seed):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    tr = np.asarray(train_idx)
    n = len(X)
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = A[j, i] = 1.0
    At = A + np.eye(n)
    s = 1.0 / np.sqrt(At.sum(axis=0))
    Ah = s[:, None] * At * s[None, :]
    sizes = [X.shape[1]] + [16] * (layers - 1) + [int(y.max()) + 1]
    rng = np.random.default_rng(seed)
    W = [rng.standard_normal((a, b)) / np.sqrt(a) for a, b in zip(sizes[:-1], sizes[1:])]
    m = [np.zeros_like(w) for w in W]
    v = [np.zeros_like(w) for w in W]
    losses = []
    for t in range(1, steps + 1):
        P = [Tensor(w) for w in W]
        h = Tensor(X)
        for k, p in enumerate(P):
            h = Ah @ h @ p
            if k < len(P) - 1:
                h = h.relu()
        loss = cross_entropy(h[tr], y[tr])
        loss.backward()
        losses.append(loss.item())
        W, m, v = adam_step(W, [p.grad for p in P], m, v, t, lr)
    h = X
    for k, w in enumerate(W):
        h = Ah @ h @ w
        if k < len(W) - 1:
            h = np.maximum(h, 0.0)
    return h.argmax(axis=1), losses
```

- W44. loss over every node (test labels in training): **fails T1** (byKey `test-1` shown).

```python
import numpy as np
from autograd import Tensor, cross_entropy
from nt_ops_l1 import adam_step


def gcn_node_classifier(edges, X, y, train_idx, layers, steps, lr, seed):
    X = np.asarray(X, dtype=float)
    y = np.asarray(y)
    tr = np.asarray(train_idx)
    n = len(X)
    A = np.zeros((n, n))
    for i, j in edges:
        A[i, j] = A[j, i] = 1.0
    At = A + np.eye(n)
    s = 1.0 / np.sqrt(At.sum(axis=1))
    Ah = s[:, None] * At * s[None, :]
    sizes = [X.shape[1]] + [16] * (layers - 1) + [int(y.max()) + 1]
    rng = np.random.default_rng(seed)
    W = [rng.standard_normal((a, b)) / np.sqrt(a) for a, b in zip(sizes[:-1], sizes[1:])]
    m = [np.zeros_like(w) for w in W]
    v = [np.zeros_like(w) for w in W]
    losses = []
    for t in range(1, steps + 1):
        P = [Tensor(w) for w in W]
        h = Tensor(X)
        for k, p in enumerate(P):
            h = Ah @ h @ p
            if k < len(P) - 1:
                h = h.relu()
        loss = cross_entropy(h, y)
        loss.backward()
        losses.append(loss.item())
        W, m, v = adam_step(W, [p.grad for p in P], m, v, t, lr)
    h = X
    for k, w in enumerate(W):
        h = Ah @ h @ w
        if k < len(W) - 1:
            h = np.maximum(h, 0.0)
    return h.argmax(axis=1), losses
```


### homework-5 items[1] `nodes_within` (7 hidden tests)

- W45. frontier only: the nodes at exactly k links, plus node i: **fails T2** (byKey `test-2` shown).

```python
import numpy as np


def nodes_within(A, i, k):
    A = np.asarray(A)
    seen = {i}
    frontier = {i}
    for _ in range(k):
        frontier = {int(j) for u in frontier for j in np.nonzero(A[u])[0] if int(j) not in seen and A[u, j]}
        seen.update(frontier)
    return sorted(frontier | {i})
```

- W46. leaves node i out: **fails T1** (byKey `test-1` shown).

```python
import numpy as np


def nodes_within(A, i, k):
    A = np.asarray(A)
    seen = {i}
    frontier = {i}
    for _ in range(k):
        frontier = {int(j) for u in frontier for j in np.nonzero(A[u])[0] if int(j) not in seen and A[u, j]}
        seen.update(frontier)
    return sorted(seen - {i})
```

- W47. stops at k - 1 rounds: **fails T1** (byKey `test-1` shown).

```python
import numpy as np


def nodes_within(A, i, k):
    A = np.asarray(A)
    seen = {i}
    frontier = {i}
    for _ in range(k - 1):
        frontier = {int(j) for u in frontier for j in np.nonzero(A[u])[0] if int(j) not in seen and A[u, j]}
        seen.update(frontier)
    return sorted(seen)
```

- W48. runs k + 1 rounds: **fails T1** (byKey `test-1` shown).

```python
import numpy as np


def nodes_within(A, i, k):
    A = np.asarray(A)
    seen = {i}
    frontier = {i}
    for _ in range(k + 1):
        frontier = {int(j) for u in frontier for j in np.nonzero(A[u])[0] if int(j) not in seen and A[u, j]}
        seen.update(frontier)
    return sorted(seen)
```

- W49. [correct alternative] non-zero pattern of (A + I)^k in integers: **passes**.

```python
import numpy as np


def nodes_within(A, i, k):
    M = np.linalg.matrix_power(np.asarray(A, dtype=np.int64) + np.eye(len(A), dtype=np.int64), k)
    return [int(j) for j in np.nonzero(M[i])[0]]
```

- W50. non-zero pattern of A^k + A^(k-1): right on every graph except an isolated start node with k >= 2, where it drops node i: **SURVIVES (passes every hidden test)**.

```python
import numpy as np


def nodes_within(A, i, k):
    A = np.asarray(A, dtype=float)
    M = np.linalg.matrix_power(A, k) + np.linalg.matrix_power(A, max(k - 1, 0))
    return sorted(int(j) for j in np.nonzero(M[i])[0])
```

- W51. excludes node i, then adds it back only when k = 0: **fails T1** (byKey `test-1` shown).

```python
import numpy as np


def nodes_within(A, i, k):
    A = np.asarray(A)
    seen = {i}
    frontier = {i}
    for _ in range(k):
        frontier = {int(j) for u in frontier for j in np.nonzero(A[u])[0] if int(j) not in seen and A[u, j]}
        seen.update(frontier)
    return sorted(seen - {i}) if k else [i]
```


## Fix pass

I recomputed every corrected number before writing it: Fractions for the settling run (the 21st step moves a value by 0.00105, the 22nd by 0.00076), breadth-first search for the reach counts, a built directed matrix for l18 screen 6, the rounded-row product for l19 screen 1, and both trainers (hand backprop and the autograd generator) for the deep runs and the 40-step accuracies. After the edits: validator 0 errors with no `[ai-mutants]` or `[source-ban]` line for representations; `voice-scan.py 35` 0 and 0; no reuse error line for representations; `grade-all.mjs --file <path> --code --strict-feedback` 0 failures on each of the 7 files alone; the number script passes through the CI runner and directly with `ZQ_NUMBERS_STRICT=1` (326 of 326 checks, 0 uncovered, 5 literals); playthrough of l17 to l20, review-5, homework-5 and problems-5 green with and without `--mobile`.

Status: fixed 20, disputed 0 (one number differs from the report, see item 2), deferred 0. Graded answers changed: none. Hidden tests added: l18 `settles` test 9, l20 `train_gcn` test 7, homework `nodes_within` test 8; l20 `feature_spread` test 3 now builds its matrix from the formula and its third expected value is 0.106861 (the hand-rounded matrix gave 0.10686).

1. representations_ops_l5.py (note, all public names): no action, the module was correct.
2. l20 quiz[1] and screens[5] (error): fixed. The quiz now asks about the linear stack ($\hat{\mathbf A}$ applied 40 times, then one weight matrix), the ReLU option's why says this stack has no ReLU, and the explain names the other cause: dead units. Screen 5's explain says the bars show over-smoothing with no ReLU, and that of the 20 runs of the 16-layer ReLU stack 17 predict one class and in 11 every last-layer unit is dead, so the output is 0. The script computes this on the generator route (autograd: 17, 11 and 11 with an all-zero output). The hand-backprop route counts 13 dead of the same 17 (deep stacks amplify float differences once a layer is at 0), so its claim is `>= 11` and 17 exactly; the stated 11 is the generator's figure and agrees with the report.
3. Number script fiat, dead loop and literal slips (warning): fixed. The directed banks are built (B to A, C to A, A to D) and give 9, 4 and 13 for $\mathbf A\mathbf x$, $\mathbf A^\top\mathbf x$ and the symmetrised sum; the dead loop is deleted; l17's 3.5, l18's 7, the review's 2 and 2.667 and l19's rounded-row figures come from `step_fr` (looped steps iterated 300 times where a limit is stated) or the product; the review's reach counts and homework item 5's 10, 4, 9 and 13 come from breadth-first search on the path and on F's tree. New claims cover the dead-unit counts, the 40-step accuracies and the isolated-node reach.
4. l19 screens[1] (warning): fixed. Feedback, byKey `no-relu` and explain give $(-3.29, 1.85)$ from the rounded row and $(-3.27, 1.84)$ from the unrounded one; the bands are unchanged.
5. l18 screens[6] (warning): fixed. The explain and summary trap now say which way messages flow is a choice: $\mathbf A\mathbf x$ reads the arrows out of a node, $\mathbf A^\top\mathbf x$ the arrows into it.
6. l20 screens[11] hints[1] (warning): fixed with the proposed wording.
7. review-5 items[3] (warning): fixed. The prompt now asks about $\hat{\mathbf A}$ applied 30 times before one weight matrix; the options are unchanged.
8. l18 screens[9] test 6 (warning): fixed. byKey `test-6` names the direction mistake, and a mutant that symmetrises with `np.maximum(A, A.T)` is declared on test 6 (a transposing solution fails the same test).
9. l20 screens[9] (warning): fixed. Hidden test 7 (`round(train_gcn(..., 40, 0.05, 0)[0], 6)` expects 0.972222; the best step on the way reaches 1.0 at steps 36 and 37, computed in the script), byKey `test-7` and a model-selection mutant on test 7.
10. homework-5 items[2] (warning): fixed with `"after": {"b": ["a"], "d": ["b", "c"], "f": ["d", "e"]}`.
11. l17 quiz[1] (note): fixed with the proposed wording.
12. l20 screens[0] option `blue` (note): fixed, "all 5 of its links".
13. l19 screens[3] (note): fixed, the `cnn` clause now reads "if you have met one in `cnn`".
14. l20 screens[2] explain (note): fixed with a transductive sentence (the unlabelled firms' numbers and links are used in training, so the score is for this graph).
15. l18 screens[10] (note): fixed. Hidden test 9 `settles(V, [0, 0, 0, 1], 22, 1e-3)` expects True, byKey `test-9`, and a `k - 1` mutant on test 9.
16. homework-5 items[1] (note): fixed. Hidden test 8 `nodes_within(B, 2, 2)` expects `[2]`, byKey `test-8`, and an $\mathbf A^k + \mathbf A^{k-1}$ mutant on test 8 (it returns `[]` there).
17. l20 screens[10] test 3 (note): fixed. The setup builds the matrix from the exact formula and the expected list is recomputed (0.399843, 0.188735, 0.106861, 0.060503, 0.034185).
18. Unreachable byKey lines (note): fixed. The strict check flags a line that no recorded mutant reaches, so each line either gained a mutant or went. Kept with a mutant: l18 screens[10] `test-4` (loop that ignores $k$) and l20 screens[9] `test-5` (hard-codes the four training firms; line reworded to say use `train_idx`). Deleted: l20 screens[10] `test-2` and `test-4` (test 1's line now also names the mean-row slip) and homework items[1] `test-2` and `test-3` (the report named `test-3`; the checker also flags `test-2`). The check also needed mutants for two lines the report called reachable: l17 screens[10] `test-6` (in-place `fill_diagonal`) and homework items[0] `test-8` (model selection on every label).
19. ENGINE-BACKLOG proposal (note): no action here; `grade-all --code` already warns on both cases (`feedback-unreachable`, `feedback-missing`) and `--strict-feedback` fails on them (AUTHORING section 9), and every level 5 file passes it. Engine files are not mine to edit.
20. Harmless survivors (note): no action, as the report says.
