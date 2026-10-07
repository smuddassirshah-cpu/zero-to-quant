# Widget catalogue: machine learning and research papers

Blueprint work file, Stage 2 Phase 1. Draft 1, 6 October 2026.

**Scope.** Every interactive widget needed to teach curriculum items 2.1 Machine learning (200 h) and 3.1 Research papers (150 h), Brilliant-style (act before you read, the diagram explains, direct manipulation, one idea per screen) and at the depth a top quantitative programme expects. Depth is set by these sources:

- **2.1 core:** An Introduction to Statistical Learning with Python (James, Witten, Hastie, Tibshirani and Taylor), the curriculum's core text, with The Elements of Statistical Learning (Hastie, Tibshirani and Friedman) behind it for the theory a top programme examines.
- **2.1 code:** Géron, Hands-On Machine Learning, PyTorch edition.
- **2.1 method:** López de Prado, Advances in Financial Machine Learning (bars, labelling, sample weights, fractional differentiation, purged and combinatorial cross-validation, feature importance, bet sizing, backtest overfitting), with Jansen for breadth.
- **2.1 method papers:** Lo (2002) and Mertens (2002) on Sharpe ratio statistics; Bailey and López de Prado (2012, 2014) on the probabilistic and deflated Sharpe ratios; Bailey, Borwein, López de Prado and Zhu (2014, 2017) on minimum backtest length and the probability of backtest overfitting; Harvey and Liu (2015) on haircut Sharpe ratios; Bergmeir, Hyndman and Koo (2018) on cross-validation for time series; Kaufman, Rosset and Perlich (2012) on leakage.
- **2.1 networks:** ISLP chapter 10, Goodfellow, Bengio and Courville chapters 6 to 8, and the 3Blue1Brown and Karpathy treatments at an intuitive level.
- **3.1:** the five papers on the curriculum's starting list (Jegadeesh and Titman 1993; Fama and French 1993; Gatev, Goetzmann and Rouwenhorst 2006; Avellaneda and Stoikov 2008; Harvey, Liu and Zhu 2016) and the methods they use: Newey and West (1987), Fama and MacBeth (1973), Gibbons, Ross and Shanken (1989), Benjamini and Yekutieli (2001), McLean and Pontiff (2016), Hou, Xue and Zhang (2020), Daniel and Moskowitz (2016), Grinold's fundamental law, and Kakushadze's 101 formulaic alphas for the WorldQuant BRAIN style.

**Read for this file.** `docs/curriculum.md`; `docs/design-research.md` sections 1, 2.6, 4, 5, 8, 9 and 10; the Stage 1 prototype (`css/tokens.css`, `js/screens/lesson.js`, `drill.js`, `drill-worker.js`); the four sibling work files (`widgets-stage0.md`, `widgets-calc-linalg.md`, `widgets-prob-stats-ts.md`, `widgets-programming.md`); the owner's lesson-creator, maths-teaching, code-craft and project-forge skills with `blueprint.md` and `engineering-floor.md`; the Artifact `sample` and `db` contracts (version 0.2.69).

**How to read it.**

- Section 0: summary, decisions, findings and naming.
- Section 1: every lesson in 2.1 and 3.1, with what the learner manipulates, builds or predicts before any rule is named. Every widget below exists because a row in section 1 needs it.
- Section 2: what this cluster adds to the shared widget contract, and the ten things the P0 engine must already support so that these P2 widgets fit without rework. Read 2.1 first: it is the part that matters for the engine-first build.
- Sections 3 to 7: the new primitive, additions to shared primitives, extensions to sibling widgets, then the composites.
- Sections 8 to 13: screens built from primitives alone, generators, the misconception register, rejected alternatives and open questions, the full widget table, and cross-cluster needs.

**Numbering.** Course and lesson numbers (2.1.1 to 2.1.10, 3.1.1 to 3.1.6, and L1, L2 inside them) are this catalogue's working outline, written to test coverage. The course-architecture blueprint owns the final outline; renumbering it changes no widget.

**Evidence tags**, as in the design research and the siblings: [our choice] for decisions without Brilliant evidence; [unverified] for facts not yet measured; [inferred] for deductions; [sourced] for facts from a cited source; **[recalled, unverified]** for figures quoted from papers from memory. Every [recalled, unverified] figure must be checked against the paper by the content team before any item grades against it. Until then such figures appear only as context, never as an answer key (decision 9).

---

## 0. Summary and decisions

- **39 new widgets: 1 primitive (`span-track`) and 38 composites.** 1 is P1 (`viva`, first useful at the 1.6 exit) and 38 are P2. Section 12 lists them all.
- **35 sibling widgets are reused with a change:** 23 composites gain a mode this cluster needs (section 5) and 12 shared primitives gain additions (section 4). Reuse comes first. Nothing here rebuilds `regression-lab`, `summary-table`, `multiple-testing`, `coint-lab`, `forecast-lab`, `test-lab`, `contingency-table`, `descent-lab`, `dependency-graph`, `pca-lab`, `least-squares-fit` or `pipeline-flow`.
- **No widget here is P0, but ten engine decisions are** (section 2.1). The owner's priority is the best possible engine and widget library before content. Deterministic elementary functions, the worker job protocol, cross-widget bindings and the prediction gate are cheap to decide now and expensive to retrofit: a later switch to deterministic maths, for example, would silently change every seeded P0 item.
- **Generators.** 36 of the 38 composites need seeded item generators for practice, homework and exams (section 9). `ml-workbench` uses seeds only to vary each learner's data; `viva` draws from a seeded question bank. The primitive needs none.
- **Build waves inside P2:** G0 (cluster services, `span-track`, primitive additions), G1 (2.1.1 to 2.1.4), G2 (2.1.5 trees, ensembles and clustering), G3 (2.1.6 neural networks), G4 (2.1.7 to 2.1.9: time-ordered validation, leakage, labels, backtest overfitting), G5 (2.1.10 capstone), H1 (3.1.1 to 3.1.3: method, momentum, Fama and French), H2 (3.1.4 to 3.1.6: pairs, market making, multiple testing). `viva` ships in wave E with the 1.6 exit, as a P1 widget.

### 0.1 Decisions

| # | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| 1 | Where models are computed for widgets | Our own `ml-core` in JavaScript, run in a worker, instrumented so it can yield its internals (every candidate split and its gain, the residuals after each boosting round, every gradient), with CI parity tests against scikit-learn | scikit-learn in Pyodide for widget numbers; TensorFlow.js; ml.js | Pyodide is about 13 MB and cannot run in the Artifact. A widget must answer within a frame. The lessons need internals that library APIs hide: a tree's rejected splits, a forest's per-tree votes, a network's every activation. This is the programming catalogue's `algo-trace` rule (instrumented JavaScript, checked against Python) applied to models |
| 2 | Floating-point determinism | `dmath`: deterministic `exp`, `log`, `log1p`, `expm1`, `tanh`, `pow`, `sin`, `cos` (ports of fdlibm) used in every seeded computation, adopted in the **P0** maths core | `Math.exp` and friends | ECMAScript lets engines approximate these functions differently in the last bit [sourced: the specification's "implementation-approximated" wording, as the prob-stats catalogue notes]. Training loops amplify last-bit differences into different trees and different networks. A learner's run must equal the graded run and Bertie's description on every device. Switching after P0 ships would change every seeded P0 item, so the choice belongs to the engine now |
| 3 | What a trained model may be graded on | (a) predictions made before training, (b) exact computations on fixed small data, or (c) a deterministic run on the item's fixed seed whose threshold sits at least a stated margin below what the reference settings reach, proved in CI | A tolerance on a resampled or re-seeded metric | Extends the prob-stats rule "never grade a random estimate". A seed-sensitive metric fails honest learners on unlucky seeds |
| 4 | Data | Seeded synthetic data with known truth from two services: `dataset-gen` (ML data sets, with planted leaks on request) and `panel-sim` (an equity panel with planted premia that decay after a "publication date", delistings, microcaps and crashes). Real data appear only in learner-run code on the web app or the learner's machine | Bundling CRSP, Compustat, Yahoo or Ken French files | CRSP and Compustat are licensed; redistribution terms for free sources are unclear [unverified]. Synthetic data let every item know the truth, so a replication on rehearsal data can be graded |
| 5 | Time-ordered fold machinery | `time-cv-lab` owns folds, label spans, purging, embargo and combinatorial purged CV for 2.1. `forecast-lab`'s shuffled-CV mode (prob-stats, 2.2) embeds its fold strip | Separate implementations per catalogue | One purge rule, one set of tests. Purging is easy to get subtly wrong at the window's left edge (section 10, `purge-only-after-test`) |
| 6 | Strategy zoo | `overfit-lab` owns the simulation of many trials and the selection of the best. `multiple-testing`'s zoo mode (prob-stats) embeds `overfit-lab`'s zoo panel | Two zoo engines | Same reason as 5 |
| 7 | Neural networks in widgets | Our own small autodiff inside `ml-core`: at most 6 hidden layers of 8 units in the playground, and 12 hand-placed units in `relu-composer`. PyTorch appears only in code the learner runs on their own machine | TensorFlow.js; ONNX Runtime Web; brain.js | TensorFlow.js is large and its WebGL backend is not bit-reproducible across GPUs [inferred]; ONNX Runtime Web is inference-only and needs WebAssembly, which the Artifact may block [unverified]. The lessons need every neuron's activation over the plane, which these runtimes do not expose cheaply |
| 8 | Python drills for 2.1 and 3.1 | Two tiers. **Implement-it drills** in pure Python or NumPy (soft-thresholding, Gini search, k-fold and purged splitters, triple-barrier labels, fractional-difference weights, a scalar autograd), which CI tags for MicroPython. **Use-the-library drills** (scikit-learn, pandas, statsmodels) are web-only. PyTorch drills run locally with paste-back verification | All drills web-only; all drills in-app | Implement-it drills teach the method and run on every target the platform allows. PyTorch is not in Pyodide's package set as far as we know [unverified]; the curriculum's Géron edition uses it, so learners run it locally |
| 9 | Published numbers from papers | Compare mode grades against the synthetic truth or the learner's own reference computation. Published figures appear as context, cited and marked until the content team verifies them | Grading a real-data replication against the published table | Sample periods, data vendors and filters differ; matching a published table within a tight tolerance is not expected with free data, and figures recalled here may be wrong |
| 10 | "Explain without notes" in exit tests | `viva`: Bertie as examiner, with up to two follow-ups probing gaps against a rubric; Bertie's mark is advisory and the learner confirms the final mark | `free-response` alone; speech capture | The 2.1 exit says "explain leakage, regularisation and the bias-variance trade-off without notes". An interviewer probes; a single typed answer does not. Speech recognition is not reliable across browsers or in the Artifact [unverified]; OS dictation into the text field works everywhere |
| 11 | Capstones | `ml-workbench` and `replication-workbench` are structured scaffolds that check the pipeline and the ledger. The exit artefact is the learner's own repository | Fully in-app projects | The curriculum's exits are GitHub projects. A scaffold catches leakage and missing steps; the repository proves the skill |
| 12 | Timelines of folds, labels, windows and trades | New primitive `span-track` | `region-select` brushes (one range, no rows); `array-strip` cells (no continuous time, no overlap) | Purging, label concurrency, formation and holding windows, pairs trades and sample periods are all rows of intervals on one time axis, and all need overlap counting and per-span selection |
| 13 | Decision regions and loss surfaces | A `field` mark: a coarse grid (64 × 64) on Canvas 2D with boundary contours in SVG | Per-pixel evaluation; WebGL | Per-pixel evaluation is banned by the owner's maths-teaching skill. A 64 × 64 grid of model queries fits the frame budget in a worker; WebGL would be a second rendering model |
| 14 | Avellaneda-Stoikov simulation | Discrete time steps with a fill probability $\lambda(\delta)\,dt$ per side, as in the paper; the widget clamps $\lambda\,dt$ at 0.5 and says so | Continuous-time event simulation only | Replication should match the paper's set-up. The clamp keeps a probability a probability when a learner sets extreme parameters |
| 15 | Model explanations | Exact Shapley values by enumeration for at most 8 features (256 coalitions) with an interventional background sample of 50 rows; permutation importance; partial dependence | TreeSHAP; KernelSHAP | Exact values follow a definition the learner can check by hand on a 2-feature toy. TreeSHAP's algorithm is a lesson of its own; KernelSHAP is approximate |
| 16 | Shared names | The calculus and linear algebra catalogue's primitive names, as Stage 0 recommends and the programming catalogue already uses (section 0.4) | The Stage 0 names that the prob-stats catalogue kept | Three of four siblings agree; the mapping is mechanical either way |

### 0.2 Finding: the exit tests and the core text examine more than the cover lists

The same pattern every sibling catalogue found holds here.

- **2.1 exit.** "One tabular prediction problem done end to end with time-ordered cross-validation, and you can explain leakage, regularisation and the bias-variance trade-off without notes." That needs three things no cover item names: an end-to-end pipeline scaffold that audits leakage (`ml-workbench`), a code environment with scikit-learn (web or local only), and an oral-style check (`viva`).
- **2.1 core text.** ISLP teaches classification metrics and ROC curves, support vector machines, splines and generalised additive models, clustering and multiple testing. The 2.1 cover names none of them, and quant interviews ask about precision, recall, ROC and clustering. This catalogue covers them at lighter depth: `threshold-lab`, `classifier-plane` (SVM mode), `basis-lab` and `cluster-lab`. Calibration is not in ISLP, but López de Prado's bet sizing (chapter 10) turns predicted probabilities into positions and fails when they are dishonest, so `calibration-lab` covers it.
- **3.1 exit.** "One replication on GitHub with an out-of-sample extension and a plain note on how much of the effect survived." Three gaps:
  - Overlapping holding-period returns (Jegadeesh and Titman) need Newey-West standard errors. The 1.6 cover list does not name them; `regression-lab`'s HAC mode, P2 in the prob-stats catalogue, becomes required (section 5).
  - "How much survived" needs a definition. `replication-workbench` defines it as the ratio of post-sample to in-sample mean return, with a confidence interval (section 7.6).
  - Market making (Avellaneda and Stoikov) rests on stochastic control, which sits in optional item 3.2. The lessons present the paper's closed-form approximations with a derivation sketch, and say so.

**Recommendation (curriculum, not widgets):** the 2.1 cover could name classification metrics, calibration and clustering, and the 3.1 cover could name Newey-West standard errors, so the course map and the exit tests agree. The widgets are specified either way.

### 0.3 Owner decision needed: the data route for the 3.1 replication

Stock-level replications need data the app cannot ship.

| Route | What it allows | Cost and caveat |
|---|---|---|
| Ken French's data library (free) | Fama and French three-factor replication at portfolio level (the 25 size and book-to-market portfolios and the factors); momentum at decile level | Portfolio-level only: the learner cannot rebuild the sorts from stocks. Redistribution terms [unverified], so the learner downloads the files |
| yfinance or Stooq daily prices (free) | Pairs trading on current constituents; momentum on current constituents | Survivorship-biased: delisted stocks are missing. The out-of-sample note must say so |
| WRDS (CRSP, Compustat) | Faithful stock-level replications of all five papers | Needs institutional access |

**Recommendation** [our choice]: the default exit project is the Fama and French three-factor replication from Ken French's library, extended past 1993 to the present. Stock-level replications are optional and must state their survivorship bias unless the learner has WRDS access. Every route is rehearsed first on `panel-sim` data, where the truth is known. The widgets are the same under every route.

### 0.4 Names against the sibling catalogues

The siblings disagree on primitive names. Stage 0 section 15.1 recommends the calculus and linear algebra names and the programming catalogue uses them, so this file does too. The engine blueprint picks the final names; the mapping is mechanical.

| Used here | Stage 0 and prob-stats | Notes |
|---|---|---|
| `plot-2d`, `plot-3d` | `plot-axes`, `view-3d` | |
| `marks` | `curve-layer`, `geo-layer`, `bar-layer` (Stage 0); `marks` (prob-stats) | One primitive, many mark types; section 4 adds four |
| `drag-point` | `draggable-point` | |
| `region-select` | `region-selector` | |
| `value-table` | `data-table` | Including the programming catalogue's frame mode |
| `live-formula` | `tex-terms` | |
| `choice`, `numeric-input`, `expression-input` | `choice-cards`, `numeric-entry`, `expression-entry` | |
| `derivation-steps` | `derivation` | |
| `slider`, `stepper`, `token-tray`, `sketch-pad`, `sim-runner`, `matrix`, `code-cell`, `free-response`, `card-sort` | same | `code-cell` is owned by the programming catalogue |
| `node-link` (programming) | `node-graph` (prob-stats) | Same concept: one renderer for trees, graphs, networks and dendrograms. The engine should merge them |
| `cell-grid` (programming) | none | Heatmaps and matrices of cells |
| Element ids `kind:name` | `kind-name` (Stage 0 only) | |

---

## 1. Lesson map: what the learner does to get each idea

Each row is one lesson idea in depth-first order. "Act" is the hook: what the learner manipulates, builds or predicts before any rule is named. "Check" is the main answer type. A lesson's Explore screen uses the same widget in `explore` mode with no check. The general inputs (`choice`, `numeric-input`, `expression-input`, `derivation-steps`, `free-response`, `card-sort`) appear only where they carry the idea. "Code" means a `code-cell` drill; section 2.11 says where each tier runs.

### 1.1 Machine learning (2.1, 200 h; ISLP core, ESL for theory, Géron for code, López de Prado for method)

**2.1.1 The learning problem** (ISLP chapter 2; ESL chapters 2 and 7)

| L | Lesson idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | A model is judged on data it has not seen | Drag a curve through 15 noisy points to fit them as closely as you can; then 15 fresh points from the same source appear and your wiggly curve scores worse than a plain one | `fit-explorer` (sketch mode) | choice (predict which curve wins on new points) |
| 2 | Flexibility: training error falls, test error is U-shaped | Sketch the training and test error curves you expect against polynomial degree, then sweep the degree | `fit-explorer` (flex), `error-curves` (predict) | curve features; numeric (degree with the lowest test error, margin-checked) |
| 3 | k-nearest neighbours; flexibility as $n/k$ | Slide $k$ from 1 to $n$; at $k = 1$ the fit threads every point, at $k = n$ it is the mean | `fit-explorer` (k-NN) | numeric (the $k = 3$ prediction at $x_0$ from the shown neighbours) |
| 4 | Loss functions and what they make you predict | Drag one constant prediction to minimise squared, absolute and Huber loss in turn; drag an outlier and watch the mean follow it and the median stay | `loss-lab` (constant) | point (the minimiser); choice |
| 5 | Bias and variance at a point | Draw 50 training sets from the same truth; the fits fan out; read bias and spread at $x_0$ for a rigid and a flexible model | `bias-variance-lab` (pointwise) | ordering (rank three models by variance); numeric (bias and variance from a fixed table of 20 fits) |
| 6 | The decomposition, integrated | Complete the derivation of $E[(Y - \hat f(x_0))^2] = \sigma^2 + \text{bias}^2 + \text{variance}$, then sweep flexibility and watch the stacked parts add to the test curve | `bias-variance-lab` (integrated), `error-curves`, `derivation-steps` | expression; derivation line |
| 7 | The curse of dimensionality | Slide the dimension $p$ and watch the edge of a cube holding 10% of the data grow towards the full width; nearest and farthest neighbours become equally far | screen from primitives (section 8.1) | numeric ($0.1^{1/10} \approx 0.794$) |
| 8 | Low signal-to-noise: what finance looks like | Raise the noise until the true curve explains 1% of variance; the best possible out-of-sample $R^2$ is 1%, and a 30% in-sample $R^2$ is a warning | `fit-explorer` (snr mode) | choice |
| 9 | Trap: choosing with the test set | Pick the degree that does best on the test points, then score it on a third, fresh set | `fit-explorer` (peek mode) | choice (predict the fresh score) |

**2.1.2 Linear and logistic models for prediction** (ISLP chapters 3, 4, 7 and 9; ESL chapters 4 and 5)

| L | Lesson idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Regression for prediction, not inference | Compare the confidence band with the prediction band at a new $x$; widen the noise | `regression-lab` (prediction mode, extension) | numeric (prediction interval width) |
| 2 | Encoding features: dummies, the dummy trap, interactions, transforms | Add a one-hot column for every level plus an intercept and watch the rank drop; drop one level; add an interaction and see two slopes | `feature-builder` | table (predict the encoded rows); choice |
| 3 | Basis expansions and splines | Drag knots along the axis; each basis function scales and the sum becomes the fit; count degrees of freedom | `basis-lab` | numeric (degrees of freedom); state (residual sum of squares below a target) |
| 4 | Logistic regression | Drag the sigmoid's midpoint and steepness to fit 0 and 1 labels; read the log-likelihood | `logistic-lab` (1D) | point (within 0.5 of the maximum log-likelihood); numeric ($p$ at $x$) |
| 5 | Likelihood, cross-entropy and log-odds | Watch each point's log-loss bar as you move the curve; switch the axis to log-odds and see a straight line; meet perfect separation | `logistic-lab` (loss and log-odds), `descent-lab` (extension) | numeric (log loss; odds ratio $e^w$); choice |
| 6 | Decision boundaries in 2D | Predict the boundary each model draws (logistic, LDA, QDA, naive Bayes), then reveal | `classifier-plane` (predict mode) | region agreement; choice |
| 7 | Thresholds and the confusion matrix | Drag the threshold across two score distributions and watch the four cells trade off; set the base rate to 1% | `threshold-lab`, `contingency-table` (confusion preset), `icon-array` | numeric (precision from counts) |
| 8 | ROC, AUC and precision-recall | Trace the ROC point as you drag; pair positives with negatives to count AUC by hand; compare ROC and PR under imbalance | `threshold-lab` (ROC and PR) | numeric (AUC of a 4 by 4 pairing); choice |
| 9 | Calibration | Bend a model's probability mapping until the reliability diagram leaves the diagonal; recalibrate with Platt and isotonic fits | `calibration-lab` | choice (over or under confident); numeric (Brier score of five forecasts) |
| 10 | Multiclass and softmax | Drag three logits and watch the probabilities; turn the temperature down until one class takes all | `logistic-lab` (softmax), `mass-editor` (read-only) | numeric |
| 11 | Margins and support vector machines | Tap the support vectors; move a point that is not one and watch nothing change; bend the boundary with an RBF kernel | `classifier-plane` (SVM) | set (support vectors); choice |
| 12 | Transfer: predicting the sign of next month's return | 52% accuracy with unequal wins and losses; set a cost matrix and find the threshold that maximises expected profit | `threshold-lab` (cost mode) | point (optimal threshold); numeric |

**2.1.3 Resampling and model selection** (ISLP chapters 5 and 6.1; ESL chapter 7; Arlot and Celisse 2010; Varma and Simon 2006; Cawley and Talbot 2010; Bergstra and Bengio 2012)

| L | Lesson idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | The validation set and its variance | Re-split the same data five times and watch the estimate jump | `cv-lab` (split) | choice |
| 2 | k-fold cross-validation | Assign rows to folds, step through the folds, average the fold errors | `cv-lab` (k-fold) | numeric (estimate and standard error from fold errors); set (training rows of fold 3) |
| 3 | Leave-one-out and its shortcut | Compute one LOOCV error the slow way, then with $\frac{y_i - \hat y_i}{1 - h_i}$ | `cv-lab` (LOOCV), `regression-lab` (hat values) | numeric |
| 4 | Bias and variance of the CV estimate in $k$ | Slide $k$ from 2 to $n$ and watch the estimate's centre and spread | `cv-lab` (k sweep) | choice |
| 5 | The one-standard-error rule | Pick the simplest model within one standard error of the best | `error-curves` (one-se) | point |
| 6 | Selection inflates the score: nested CV | Tune on the folds, report the same folds, then run the nested version | `cv-lab` (nested), `tuning-lab` | ordering (rank the three estimates) |
| 7 | Grid against random search | Spend nine evaluations on a surface where one hyperparameter matters | `tuning-lab` | choice; numeric (distinct values tried per axis) |
| 8 | Subset selection and information criteria | Step forward through a stepwise path and read $C_p$, AIC, BIC and adjusted $R^2$; add pure-noise columns | `regularisation-path` (stepwise) | numeric (AIC from RSS); choice |
| 9 | The bootstrap and the 0.632 rule | Resample rows and count the ones never drawn | `sampling-lab` (bootstrap, extension), screen from primitives (section 8.2) | numeric ($1 - (1 - 1/n)^n \to 1 - e^{-1}$) |
| 10 | Trap: selecting features before the folds | Pick the 20 noise features most correlated with the label on all the data, then cross-validate: near-perfect accuracy on pure noise | `cv-lab` (selection-outside), `leakage-detective` (pipeline) | choice; numeric |

**2.1.4 Regularisation** (ISLP 6.2 to 6.4; ESL 3.4 and 18; Hoerl and Kennard 1970; Tibshirani 1996; Zou and Hastie 2005; Friedman, Hastie and Tibshirani 2010)

| L | Lesson idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Shrinking can predict better | Multiply every OLS coefficient by one shrink factor and watch the test error dip below OLS | `regularisation-path` (uniform shrink) | point (a shrink factor that beats OLS) |
| 2 | Ridge and its path | Drag $\lambda$ from 0 to large along the path; coefficients glide to zero but never reach it | `regularisation-path` (ridge) | numeric (1D ridge: $\frac{\sum x_i y_i}{\sum x_i^2 + \lambda}$) |
| 3 | Ridge geometry | Shrink the budget disc until it touches the error ellipses; drag your guess of the tangent point | `penalty-geometry` (L2) | point |
| 4 | Ridge through the SVD | Watch each principal direction shrink by $\frac{d_j^2}{d_j^2 + \lambda}$; the low-variance directions go first; read the effective degrees of freedom | `regularisation-path` (SVD panel), `pca-lab` | numeric (degrees of freedom) |
| 5 | Lasso: corners make zeros | Swap the disc for a diamond; the solution lands on a corner and one coefficient is exactly zero | `penalty-geometry` (L1) | point (on a corner) |
| 6 | Hard, soft and proportional thresholds | Drag the OLS estimate in an orthonormal design and match each penalty to its threshold function | `penalty-geometry` (1D), `card-sort` | mapping; numeric ($S(z, \lambda)$) |
| 7 | Standardise first | Rescale one feature by 100 and watch the lasso change its mind | `regularisation-path` (standardise toggle) | choice |
| 8 | Choosing $\lambda$ by cross-validation | Read $\lambda_{\min}$ and $\lambda_{1\text{se}}$ off the CV curve | `regularisation-path`, `error-curves` | point (margin-checked) |
| 9 | Correlated features: lasso picks one, elastic net groups | Resample the data and watch the lasso swap between twin features; mix in an L2 part | `penalty-geometry` (elastic net), `regularisation-path` (stability) | choice |
| 10 | Regularisation as a prior | Line up a Gaussian prior with the ridge disc and a Laplace prior with the diamond | `posterior-lab` (MAP mode, extension), `penalty-geometry` | expression ($\lambda = \sigma^2/\tau^2$) |
| 11 | Principal components regression against ridge | Keep 1, 2, 3 components and compare with ridge's smooth shrinkage | `pca-lab`, `regularisation-path` (PCR) | choice |
| 12 | More features than rows, and double descent | Add random features past $p = n$ and predict where the test error peaks | `fit-explorer` (random features), `error-curves` (double descent) | choice (predict the spike) |
| 13 | Transfer: shrinking noisy return forecasts | Shrink 50 noisy signal estimates towards zero and score next year | `regularisation-path` | numeric |

**2.1.5 Trees, ensembles and clustering** (ISLP chapters 8 and 12; ESL 9.2, 10, 14.3, 15 and 16; Breiman 1996 and 2001; Friedman 2001; Chen and Guestrin 2016; Ke and others 2017; Strobl and others 2007; Lundberg and Lee 2017)

| L | Lesson idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Grow a tree by hand | Split the plane with axis-aligned cuts until the boxes are nearly pure; the tree grows beside it | `tree-builder` | state (at most 4 leaves reaching a stated training accuracy) |
| 2 | Impurity: Gini, entropy and misclassification | Drag a threshold along one feature and watch the weighted child impurity | `split-scorer` | numeric (Gini of a node; gain of a split); point (best threshold) |
| 3 | Regression trees | Split a 1D scatter into steps; each leaf predicts its mean | `split-scorer` (RSS), `tree-builder` (1D) | numeric |
| 4 | Depth, overfitting and pruning | Grow deep, then slide the cost-complexity $\alpha$ and watch leaves fold | `tree-builder` (prune), `error-curves` | numeric (leaves at $\alpha$); choice |
| 5 | Trees are unstable | Resample the data and watch the tree change shape | `tree-builder` (resample), `bias-variance-lab` (tree model) | choice |
| 6 | Bagging and out-of-bag error | Average more and more trees; read the OOB error; check $\rho\sigma^2 + \frac{1 - \rho}{B}\sigma^2$ | `ensemble-lab` (bagging) | numeric (the variance formula) |
| 7 | Random forests decorrelate | Lower the features tried per split and watch $\rho$ fall and the error with it | `ensemble-lab` (forest) | choice; numeric |
| 8 | Boosting: fit what is left | Before each round, drag a stump onto the residuals; the fit climbs by $\nu$ times your stump | `boosting-lab` (predict mode) | point (split and leaf values); numeric |
| 9 | Gradient boosting and early stopping | Switch to log loss and see residuals become $y - p$; run too many rounds | `boosting-lab`, `error-curves` (rounds) | expression (pseudo-residual); choice |
| 10 | XGBoost and LightGBM ideas | Score candidate splits with gradient and Hessian sums and the $\lambda$ and $\gamma$ penalties | `split-scorer` (gain), `tuning-lab` | numeric (gain) |
| 11 | AdaBoost (optional) | Watch misclassified points grow in weight; compute $\alpha_m$ | `boosting-lab` (AdaBoost) | numeric |
| 12 | Feature importance and its traps | Shuffle one column and watch the score drop; add an ID column with many values and watch impurity importance crown it; add a twin of the best feature | `importance-lab` | ordering; choice |
| 13 | Partial dependence and Shapley values | Sweep one feature with the others held; split a prediction into contributions by hand for two features | `importance-lab` (PDP, Shapley) | curve features; numeric (a Shapley value) |
| 14 | Clustering: k-means and hierarchical | Drag centroids and watch points reassign; build a dendrogram and cut it | `cluster-lab` | mapping; numeric |
| 15 | Transfer: trees on noisy financial features | Lower the minimum leaf size on a low-signal data set and watch the test error | `ensemble-lab`, `time-cv-lab` (preview) | choice |

**2.1.6 Neural networks at an intuitive level** (ISLP chapter 10; Goodfellow, Bengio and Courville chapters 6 to 8; Géron, PyTorch edition; Montúfar and others 2014; Telgarsky 2016; Grinsztajn, Oyallon and Varoquaux 2022; Gu, Kelly and Xiu 2020)

| L | Lesson idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | A neuron is logistic regression | Redraw the logistic unit as a neuron: inputs, weights, sum, activation | `logistic-lab` (neuron), `nn-playground` (one unit) | choice |
| 2 | Hidden units are learned features | Solve XOR: first by hand-setting the weights of a 2-2-1 network, then by training; inspect each unit's map | `nn-playground` (hand-set, train) | state (100% training accuracy) |
| 3 | Sums of ReLUs approximate any curve | Add ReLU ramps and drag their kinks until the sum follows a target curve | `relu-composer` | curve (within a band with at most 6 units) |
| 4 | Depth multiplies pieces | Compose two layers and count the linear pieces; compare width and depth with the same unit count | `relu-composer` (depth), `nn-playground` (regions) | numeric (pieces) |
| 5 | Training: learning rates, minibatches, momentum and Adam | Race four optimisers on a narrow valley; push the learning rate until training diverges | `descent-lab` (extension) | choice; numeric (the divergence threshold $2/\lambda_{\max}$) |
| 6 | Backpropagation is the chain rule | Run the forward pass, then fill in each gradient on a small graph; check with a finite difference | `dependency-graph` (backprop, extension) | numeric (a gradient) |
| 7 | Initialisation and vanishing gradients | Change the initial weight scale and watch activations collapse or explode through ten layers | `nn-playground` (depth statistics) | choice |
| 8 | Overfitting and its remedies | Train a large network on 50 points; add weight decay, dropout and early stopping | `nn-playground`, `error-curves` (epochs) | choice |
| 9 | Sequences: filters, recurrence and attention | Drag kernel weights over a return series; see EWMA as a recurrent state; soften attention weights with temperature | `sequence-filter` | numeric (output at $t$); choice (causal or leaking) |
| 10 | Where networks fit in quant work | Run linear, forest, boosting and a small network on the same noisy panel with time-ordered folds | `ml-workbench` (arena) | choice; free text |

**2.1.7 Validation when time matters** (López de Prado chapters 7 and 12; Bergmeir and Benítez 2012; Bergmeir, Hyndman and Koo 2018; Hyndman and Athanasopoulos, FPP chapter 5)

| L | Lesson idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Shuffled k-fold flatters time series | Predict which scheme will report higher accuracy, then run shuffled and blocked folds on overlapping 20-day labels | `time-cv-lab` (compare) | choice (prediction) |
| 2 | Walk-forward: expanding and rolling | Drag the window and step the origin forward | `time-cv-lab` (walk-forward) | set (training samples of split 3); numeric (number of splits) |
| 3 | Overlapping labels share returns | See each label as a bar from $t_0$ to $t_1$; count the labels covering one day | `time-cv-lab` (spans), `labelling-lab` (weights) | numeric (overlap count) |
| 4 | Purging | Tap every training label whose span touches the test fold, on both sides | `time-cv-lab` (purge task) | set (exact purge set) |
| 5 | Embargo | Slide the embargo after the test fold and watch features that still carry test information drop out | `time-cv-lab` (embargo) | numeric (embargo size); set |
| 6 | Combinatorial purged CV | Choose $N$ groups and $k$ test groups; assemble backtest paths from the split matrix | `time-cv-lab` (CPCV) | numeric ($\binom{N}{k}$ splits, $\varphi = \frac{k}{N}\binom{N}{k}$ paths); state (a valid path) |
| 7 | When k-fold is fine | For a pure autoregression with uncorrelated errors, k-fold is valid; add an overlapping label and it is not | `time-cv-lab` (AR mode) | choice |
| 8 | Trap: tune and report on the same walk-forward | Tune on the walk-forward, report it, then score a locked hold-out | `time-cv-lab`, `tuning-lab` | choice |

**2.1.8 Leakage, labels and financial features** (López de Prado chapters 2 to 5, 8 and 10; Kaufman, Rosset and Perlich 2012; Luo and others 2014, "Seven sins of quantitative investing"; Jansen; López de Prado 2016 on hierarchical risk parity)

| L | Lesson idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | A taxonomy of leakage | Audit a described study and tap every flaw | `leakage-detective` (audit) | set |
| 2 | When is each value known? | Place each feature's "known at" time against the decision time | `leakage-detective` (timeline) | set (leaky features); ordering |
| 3 | Preprocessing leakage | Move the scaler, imputer and feature selection inside or outside the folds; watch which rows each was fitted on | `leakage-detective` (pipeline), `pipeline-flow` (sklearn mode, extension) | state (no stage fitted on test rows); code |
| 4 | Survivorship bias | Backtest on today's survivors, then on the point-in-time universe with delisting returns | `leakage-detective` (universe), `portfolio-sort` | numeric (bias in mean return) |
| 5 | Bars: time, tick, volume and dollar | Sample one trade stream four ways and compare the return histograms with the normal | `bar-sampler` | numeric (bars from a short trade list); choice |
| 6 | Fixed-horizon labels and their flaws | Label events by the sign of the 10-day return; find a path that hit $-8\%$ on the way to $+1\%$ | `labelling-lab` (fixed) | numeric |
| 7 | The triple-barrier method | Drag the profit-taking and stop-loss barriers and the time limit; predict which barrier each path touches first | `labelling-lab` (triple barrier) | choice; point (first-touch time) |
| 8 | Meta-labelling | A simple rule picks the side; a second model decides whether to act; watch precision rise as recall falls | `labelling-lab` (meta), `threshold-lab` | numeric (precision before and after) |
| 9 | Concurrency, uniqueness and sample weights | Read how many labels cover each day; compute a label's average uniqueness; watch the sequential bootstrap favour unique labels | `labelling-lab` (weights) | numeric |
| 10 | Fractional differentiation | Slide $d$ from 0 to 1 and find the smallest $d$ that passes the ADF test while keeping memory | `fracdiff-lab` | numeric (weights $w_k$); point (minimum $d$) |
| 11 | Feature importance in finance | Compare MDI, MDA and single-feature importance with twin features; cluster the features first | `importance-lab` (finance), `cluster-lab` (feature clusters) | choice |
| 12 | Clustering assets by correlation | Turn correlations into distances $\sqrt{\frac{1}{2}(1 - \rho)}$, build a dendrogram and reorder the correlation matrix | `cluster-lab` (correlation) | numeric; ordering |
| 13 | Bet sizing from probabilities | Drag the predicted probability and watch the bet size; overstate the probability and watch the drawdowns | `calibration-lab` (sizing), `game-lab` (Kelly) | numeric (size at $p = 0.6$) |

**2.1.9 Backtest overfitting** (Lo 2002; Mertens 2002; Bailey and López de Prado 2012 and 2014; Bailey, Borwein, López de Prado and Zhu 2014 and 2017; Harvey and Liu 2015; López de Prado chapters 11 to 14; Blum and Hardt 2015)

| L | Lesson idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | A Sharpe ratio is an estimate | Shrink the track record and watch the Sharpe ratio's sampling distribution widen | `sharpe-lab` (sampling) | numeric (standard error $\sqrt{(1 + \frac{1}{2}SR^2)/T}$) |
| 2 | Annualising and autocorrelation | Add positive autocorrelation and watch $\sqrt{12}$ overstate the annual Sharpe ratio | `sharpe-lab` (annualise) | numeric |
| 3 | Skew, fat tails and the probabilistic Sharpe ratio | Make returns negatively skewed and fat-tailed and watch the confidence fall | `sharpe-lab` (PSR) | numeric |
| 4 | The best of many noise strategies | Predict the best in-sample Sharpe ratio among 100 coin-flip strategies, then run them | `overfit-lab` (zoo) | choice (prediction); numeric ($E[\max]$ approximation) |
| 5 | Parameter sweeps and plateaus | Pick the best cell of a moving-average grid on a random walk, then see it out of sample | `overfit-lab` (sweep) | choice |
| 6 | The deflated Sharpe ratio | Enter the number of trials and their dispersion; the hurdle rises | `sharpe-lab` (DSR) | numeric |
| 7 | Probability of backtest overfitting | Split the performance matrix into blocks, choose halves, and count how often the in-sample winner ranks below the median out of sample | `overfit-lab` (CSCV) | numeric (PBO from shown counts) |
| 8 | Minimum backtest length | Place your research (trials tried, years of data) against the curve | `overfit-lab` (MinBTL) | point (log scale) |
| 9 | Haircut Sharpe ratios | Convert a Sharpe ratio to a $t$-statistic, adjust for 100 tests, and convert back | `sharpe-lab` (haircut) | numeric |
| 10 | Leaderboards overfit too | Submit 100 times to a public leaderboard and watch the private score | `overfit-lab` (leaderboard) | choice |
| 11 | A research protocol that resists overfitting | Log every trial, lock a hold-out, write the plan before the data | `ml-workbench` (ledger) | free text |

**2.1.10 Capstone and exit**

| L | Lesson idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Frame the problem | Choose target, horizon, universe and metric; state the decision the model serves | `ml-workbench` (frame) | state |
| 2 | Build a leak-free pipeline | Assemble features, labels, folds and models; the audit stays green | `ml-workbench` (pipeline) | state (all audit predicates pass) |
| 3 | Compare models honestly | Run the arena with purged walk-forward folds; read paired differences with error bars | `ml-workbench` (arena) | choice; numeric |
| 4 | Write it up | Fill the results note, including what failed | `ml-workbench` (note) | free text (rubric) |
| 5 | Exit: the code | Run the exported scikit-learn script with the provided tests | `code-cell` (web or local) | code |
| 6 | Exit: explain without notes | Explain leakage, regularisation and the bias-variance trade-off to Bertie | `viva` | free text (rubric, advisory plus self-mark) |

### 1.2 Research papers (3.1, 150 h; SSRN, arXiv q-fin, WorldQuant BRAIN; the five starting papers)

**3.1.1 Reading and replicating** (McLean and Pontiff 2016; Hou, Xue and Zhang 2020; Harvey 2017; Kakushadze 2016)

| L | Lesson idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Anatomy of an empirical paper | Match questions ("what sample?", "what is the main claim?") to the sections that answer them | `replication-workbench` (read) | mapping |
| 2 | Reading a results table | Tap a coefficient and its $t$-statistic in parentheses; compute $t$ from the coefficient and standard error | `replication-workbench` (table), `summary-table` | numeric; choice |
| 3 | The replication ledger | List every choice that could move the number; tap the ones the paper leaves unstated | `replication-workbench` (ledger) | set |
| 4 | Replicate where the truth is known | Run a planted-premium sort on rehearsal data and recover the premium | `portfolio-sort`, `replication-workbench` (compare) | numeric (within tolerance of the truth) |
| 5 | Out of sample and after publication | Split the history at the sample end and the publication date; read how much survived | `replication-workbench` (decay) | numeric; interval |
| 6 | Data traps | Survivorship, point-in-time fundamentals, corporate actions | `leakage-detective` (universe, timeline) | set |
| 7 | Formulaic alphas as small replications | Build an alpha from operator tokens; read its IC and turnover; delay it by one day | `signal-lab` (expression) | state (valid and delayed); numeric |

**3.1.2 Momentum: Jegadeesh and Titman (1993)**

| L | Lesson idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Winners keep winning, for a while | Sort 50 stocks by past six-month return and predict which decile does best next month | `portfolio-sort` (single, one date) | choice (prediction) |
| 2 | Formation, skip and holding windows | Set the windows for "12-1" momentum on the timeline | `portfolio-sort` (timeline) | state; numeric (months of history needed) |
| 3 | Deciles and winners minus losers | Read average returns by decile; compute WML | `portfolio-sort` | numeric |
| 4 | Overlapping portfolios | Hold $K$ cohorts at once; each month one cohort is replaced; average them | `portfolio-sort` (overlap) | numeric |
| 5 | The $J \times K$ table | Scan the grid of strategies; find the pattern | `portfolio-sort` (grid) | choice |
| 6 | $t$-statistics with overlapping returns | Compare plain and Newey-West standard errors on overlapping returns | `regression-lab` (HAC, extension) | numeric |
| 7 | Is momentum just risk? | Regress WML on the market and on the three Fama and French factors | `factor-model-lab` (single) | choice |
| 8 | Momentum crashes | Find the months after bear markets when losers rebound | `portfolio-sort` (crash view), `sharpe-lab` (skew) | choice |
| 9 | Costs and turnover | Raise the cost per unit of turnover until the net premium vanishes | `signal-lab` (costs) | numeric |
| 10 | Extend out of sample | Run past the paper's sample end; read the decay | `replication-workbench` (decay) | interval; free text |

**3.1.3 The three-factor model: Fama and French (1993)**

| L | Lesson idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | CAPM fails in the cross-section | Plot portfolio betas against average returns; the line is too flat | `factor-model-lab` (SML) | choice |
| 2 | Building SMB and HML | Drag size and book-to-market breakpoints on the NYSE stocks; form six portfolios; combine them | `portfolio-sort` (double, factor) | state (breakpoints); numeric (SMB from six returns) |
| 3 | Time-series regressions | Drag a portfolio's loadings to fit, then reveal OLS; read alpha | `factor-model-lab` (single) | point (loadings within tolerance of OLS); numeric (alpha) |
| 4 | Twenty-five portfolios | Switch CAPM to three factors and watch the alpha grid fade | `factor-model-lab` (grid) | choice |
| 5 | The GRS test | Are all 25 alphas zero together? | `factor-model-lab` (GRS), `dist-explorer` ($F$ tail) | numeric |
| 6 | Fama-MacBeth regressions | Step through monthly cross-sectional regressions and average the slopes | `factor-model-lab` (Fama-MacBeth) | numeric (average slope and $t$) |
| 7 | Loadings or characteristics? (optional) | Daniel and Titman's test in one picture | `factor-model-lab` | choice |
| 8 | Beyond three factors | Add momentum (Carhart); meet profitability and investment | `factor-model-lab`, `multiple-testing` | choice |
| 9 | Extend out of sample | Rerun after 1993; value's weak decade | `replication-workbench` (decay) | free text |

**3.1.4 Pairs trading: Gatev, Goetzmann and Rouwenhorst (2006)**

| L | Lesson idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Trade the gap between twins | Watch two normalised prices drift apart and back; decide when to open | `pairs-lab` (single pair) | choice |
| 2 | Formation by distance | Scan the matrix of squared distances and pick the closest pairs | `pairs-lab` (formation) | set (top pairs); numeric (one distance) |
| 3 | The trading rule | Open at two historical standard deviations, close at the crossing; mark the trades | `pairs-lab` (trading) | point (open and close days); numeric (trade return) |
| 4 | A portfolio of pairs | Compare returns on committed capital and on capital actually employed | `pairs-lab` (portfolio) | numeric |
| 5 | The one-day wait | Execute a day late and watch bid-ask bounce profits vanish | `pairs-lab` (wait toggle) | choice |
| 6 | Distance or cointegration? | Select pairs both ways and compare out of sample | `pairs-lab` (compare), `coint-lab` (trading) | choice |
| 7 | Mean-reversion speed | Fit the spread's half-life | `sde-stepper`, `coint-lab` (ECM) | numeric |
| 8 | Decay and crowding | Run the strategy across decades | `pairs-lab`, `replication-workbench` (decay) | free text |

**3.1.5 Market making: Avellaneda and Stoikov (2008)**

| L | Lesson idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Earn the spread, carry the inventory | Quote symmetrically around the mid and watch inventory wander | `market-maker-sim` (live, symmetric) | choice |
| 2 | Fill intensity and the best one-sided quote | Drag the quote distance $\delta$ and watch $\delta \cdot A e^{-k\delta}$ peak at $\delta = 1/k$ | `market-maker-sim` (geometry) | point; numeric |
| 3 | The reservation price | Drag inventory $q$ and time left; the quote centre slides to $r = s - q\gamma\sigma^2(T - t)$ | `market-maker-sim` (geometry) | numeric |
| 4 | The optimal spread | Read $\delta^a + \delta^b = \gamma\sigma^2(T - t) + \frac{2}{\gamma}\ln(1 + \frac{\gamma}{k})$ off the picture | `market-maker-sim` (geometry) | numeric |
| 5 | Inventory strategy against symmetric | Predict which has the lower spread of profits, then run 1,000 days | `market-maker-sim` (batch) | choice (prediction) |
| 6 | Sensitivity | Order the effects of $\gamma$, $k$ and $\sigma$ on spread and inventory | `market-maker-sim` | ordering |
| 7 | What the model leaves out | Turn on informed flow and watch the maker lose; cap inventory | `market-maker-sim` (adverse selection, limits) | free text |
| 8 | Replicate the paper's simulation | Reproduce the comparison table with fixed seeds | `market-maker-sim`, `code-cell`, `replication-workbench` | code |
| 9 | You are the market maker | Quote live against the simulator | `market-maker-sim` (play) | none (explore); feeds 3.3 |

**3.1.6 Multiple testing in factor research: Harvey, Liu and Zhu (2016)**

| L | Lesson idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | The factor zoo | Watch the count of published factors climb by year; predict the false discoveries among 300 nulls at 5% | `multiple-testing` (zoo timeline, extension) | numeric |
| 2 | $t$-hurdles under Bonferroni and Holm | Read the hurdle for $M$ tests on a $t$ axis | `multiple-testing` ($t$ axis) | numeric ($\Phi^{-1}(1 - 0.025/M)$) |
| 3 | False discovery rates under dependence | Apply BH and BHY to a list of factor $t$-statistics | `multiple-testing` (BHY) | set |
| 4 | The hurdle rises with time | Slide the year; the hurdle climbs as tests accumulate | `multiple-testing` (timeline) | point |
| 5 | Tests you never see | Add unpublished failures and watch the adjustment tighten | `multiple-testing` (unobserved tests) | choice |
| 6 | Haircut Sharpe ratios | Haircut a backtest's Sharpe ratio for the number of strategies tried | `sharpe-lab` (haircut) | numeric |
| 7 | What survives replication | Compare in-sample, post-sample and post-publication returns across many planted anomalies | `replication-workbench` (decay, many), `multiple-testing` | free text |
| 8 | Exit: replicate one paper | Run the replication, extend it out of sample, write the note, defend it | `replication-workbench`, `viva` | code; free text |

**Coverage check.** Every topic in the 2.1 cover and use lists (linear and regularised models, trees and ensembles, bias-variance, time-ordered cross-validation, purged cross-validation, leakage, labelling, backtest overfitting, neural networks at an intuitive level) and every paper on the 3.1 starting list maps to at least one lesson above, and every lesson names its widgets. Lesson counts: 2.1 has 107 lessons across 10 courses; 3.1 has 51 across 6. At 10 to 15 minutes each that is about 18 to 27 hours and 9 to 13 hours of lessons; homework, code drills, the capstone and the replication project carry the rest of the 200 and 150 hours, as the design research's time budget expects.

---

## 2. What this cluster adds to the shared contract

The shared widget contract is proposed in `widgets-stage0.md` section 1 and `widgets-calc-linalg.md` section 2, with additions in the prob-stats and programming catalogues: a module with `mount`, serialisable state, `answer()`, `lock`, grading marks that recolour answer objects only, declarative show-why recipes, `reveal`, `describe`, stable `kind:name` element ids, `highlight` and `annotate`, `on('change' | 'commit')` and `destroy`. This file assumes that contract. Where the drafts differ, the engine blueprint decides. This section states only what machine learning and research add.

### 2.1 What the P0 engine must already support

Every widget in this file is P2, but the engine is built first. These ten requirements cost little at P0 and a great deal later. Each is phrased as an acceptance test.

| # | Requirement | Acceptance test | Why it cannot wait |
|---|---|---|---|
| 1 | **`dmath` in the maths core.** Deterministic `exp`, `log`, `log1p`, `expm1`, `pow`, `tanh`, `sin`, `cos`, `atan2` (fdlibm ports). Every seeded computation uses them: RNG normals, `dist`, `sim-runner`, `ml-core`. `Math.sqrt` and the four arithmetic operations are already correctly rounded and stay | $10^6$ seeded arguments give bit-identical results on Chrome, Firefox and Safari; error at most 1 ulp against a correctly rounded reference [fdlibm's claim, unverified per function]; speed within 3× of `Math.*` [unverified] | Box-Muller normals call `log` and `cos`. If P0 ships on `Math.*` and P2 switches, every seeded P0 item changes |
| 2 | **One worker job protocol** for `sim-runner` and `ml-core`: `start(kind, params, seed)` returns a job that emits `progress`, `snapshot` (into a ring buffer of at most 200 states) and `result`, and accepts `pause`, `resume`, `step(n)` and `cancel`. Typed arrays move as transferables. A newer job from the same widget supersedes the old one through a generation counter, as the prototype's `showGen` does | Cancel lands within 50 ms (work runs in chunks of at most 16 ms); a superseded job never paints; `stepper` trace mode scrubs the snapshot buffer | Training, bias-variance resampling, CSCV and portfolio sorts are all long jobs that the learner pauses, steps and scrubs |
| 3 | **Asynchronous predicates.** A check may call a registered predicate that runs in the worker (for example `accuracy-at-least`) with a 2 s limit, inside the design research's `evaluating` state (loader after 400 ms) | A slow predicate shows the loader, never blocks input handling, and times out to a neutral "Could not check; try again" without costing an attempt | Several checks here train or score a model |
| 4 | **Cross-widget bindings** declared in screen data: `bind: [{ a: 'fit.degree', b: 'curves.cursor', dir: 'both' }]`. Widgets list their bindable fields; the engine propagates on `commit` (and on `change` where both sides declare it cheap) and refuses cycles | Two widgets stay in step under drag, keyboard and `setState`; a cycle is a content-build error | `error-curves`, `regularisation-path`, `cv-lab` and most composites here are read beside a second widget |
| 5 | **A prediction gate** in screen data: `gate: { predict: 'answer-id', hides: ['curves:test', 'readout:test-error'] }`. The engine keeps the named elements hidden until the prediction is committed, records it, and lets misconception rules refer to it | Hidden elements are absent from the DOM, `describe` and the table view until release; the prediction is stored with the attempt | "Predict, then reveal" is the commonest hook in section 1. Prob-stats built it into one widget (`predictFirst`); it should be engine-wide |
| 6 | **A Canvas field layer in `marks`** under the SVG handle layer: a `Float32Array` grid with a palette function read from tokens at draw time, the device-pixel ratio capped at 2, and SVG contours drawn on top | A 64 × 64 field repaints in 2 ms or less on the reference phone and redraws on theme change | Decision regions, loss surfaces, hyperparameter surfaces and heatmaps all use it |
| 7 | **`plot-2d` time and stacked axes**: date and trading-day ticks, panels sharing an $x$ axis, reversed log axes ($\lambda$ paths read right to left), and inset panels anchored to a data point | A stacked three-panel plot keeps its $x$ cursor aligned under drag and zoom | Every research widget and the time-ordered validation widgets are stacked time panels |
| 8 | **Tutor channel features**: `describe` budgets; the `secret()` block proposed by prob-stats (true functions, planted leaks, true labels), passed only in lesson and explore modes; small computed-number tools; and a bounded multi-turn transcript for `viva`, resent on each call because the `sample` capability remembers nothing between calls [sourced: `sample.d.ts`] | A five-turn viva fits the `sample` input cap, which the page reads from `limits()` at runtime; `secret()` never appears in screen-reader text | Bertie is built in from the start (owner decision); these hooks shape its prompt format |
| 9 | **Versioned generator services.** Item data name a generator and a major version (`panel-sim@1`); an algorithm never changes under the same major version; CI stores golden hashes of generated data for fixed seeds | Changing a generator's output without a version bump fails CI | Homework and redo items replay weeks later and must show the same data |
| 10 | **Saved state is configuration plus actions.** Widgets save configs, seeds and the learner's choices, never fitted models or simulation outputs; everything re-derives on load, which requirement 1 makes exact | Reloading any widget reproduces its picture bit for bit; saved state stays within 32 KB per instance | A forest or a network does not fit the `db` document budget and need not be stored |

### 2.2 Answers, checks and predicates

This cluster adds **no new answer types**. It uses the shared ones (`choice`, `numeric`, `expression`, `set`, `interval`, `ordering`, `mapping`, `point`, `curve`, `state`, `code`, `text`) plus the programming catalogue's `table`. That keeps the checker small. What it adds is predicates: named, pure, unit-tested functions in the registry. Content names them and passes arguments; content never ships code.

| Predicate | Tests | Used by |
|---|---|---|
| `region-agrees` | The learner's painted region agrees with the model's region on at least a stated share of grid cells | `classifier-plane` |
| `separates` | A learner-drawn line or boundary classifies every training point (or a stated share) correctly | `classifier-plane`, `logistic-lab` |
| `loglik-within` | The log-likelihood at the learner's parameters is within $\delta$ of the maximum | `logistic-lab` |
| `rss-within` | The residual sum of squares is within a factor $1 + \varepsilon$ of the least-squares minimum | `basis-lab`, `factor-model-lab`, `boosting-lab` |
| `mse-at-most` | The mean squared error of a learner-built function on the item's fixed points is at most a threshold | `relu-composer`, `basis-lab` |
| `accuracy-at-least` | A deterministic run on the item seed reaches a stated accuracy on the named split (section 2.3, rule 2) | `nn-playground`, `tree-builder`, `classifier-plane` |
| `tree-size-at-most` | The learner's tree has at most $L$ leaves | `tree-builder` |
| `folds-valid` | A fold assignment is a partition; sizes differ by at most 1; stratification within a stated tolerance; groups never split | `cv-lab` |
| `purge-exact`, `embargo-exact` | The selected training ids equal the exact purge set (overlap rule in section 6.6.1) or embargo set for split $j$ | `time-cv-lab` |
| `purge-misses-left-edge` | A misconception predicate: the selection contains every overlapping span that starts after the test fold begins and misses at least one that starts before it | `time-cv-lab` |
| `cpcv-path-valid` | A backtest path uses each group exactly once, each from a split in which that group is a test group | `time-cv-lab` |
| `no-fit-on-test` | No pipeline stage is fitted on rows of the test fold | `leakage-detective`, `ml-workbench` |
| `features-available` | Every feature's available time is at or before the decision time | `leakage-detective`, `ml-workbench`, `signal-lab` |
| `labels-purged` | The workbench's folds purge and embargo by the label spans | `ml-workbench` |
| `near-optimum` | The best evaluated point of a search is within a stated score of the surface's true optimum, using at most the budget | `tuning-lab` |
| `stump-near-best` | The learner's stump reduces the residual sum of squares to within $\varepsilon$ of the best stump | `boosting-lab` |
| `on-corner` | A constrained solution has the expected coordinates exactly zero (within $10^{-9}$) | `penalty-geometry` |
| `kmeans-fixed-point` | Assignments and centroids are a fixed point of one Lloyd step | `cluster-lab` |
| `breakpoints-match` | Breakpoints equal the stated percentiles of the stated subset, to within one stock | `portfolio-sort` |
| `expression-valid` | An alpha expression type-checks and uses data delayed by at least one period | `signal-lab` |
| `kernel-matches` | A learner kernel reproduces the target output within tolerance | `sequence-filter` |
| `ledger-complete` | Every required ledger field has a value and a reason | `replication-workbench` |
| `audit-green` | Every workbench audit predicate passes | `ml-workbench` |

### 2.3 Grading rules for learned models and simulations

1. **Never grade a resampled or re-seeded quantity.** This is the prob-stats rule, unchanged. Bias-variance fans, bootstrap draws, strategy zoos and market-making batches exist to confirm a prediction, never to be the answer.
2. **A deterministic run may be graded** when all of these hold: it uses `dmath` and a fixed operation order; it runs on the item's seed; the check scores the learner's own displayed run, not a fresh one; and CI proves a margin. The proof: the reference settings clear the threshold on every one of 1,000 generated items, by at least the stated margin (default 5 percentage points of accuracy, or 10% of the loss).
3. **"Which setting is best" items** are generated only when the argmin is unique with a margin: the runner-up must be worse by at least the larger of 5% (relative) and one standard error across folds. Otherwise the item accepts the set of settings inside the one-standard-error band.
4. **Predictions before reveal** are graded against the item's deterministic outcome. The generator guarantees the qualitative outcome is unambiguous; for example, shuffled folds beat purged walk-forward by at least 10 accuracy points.
5. **Small-data computations are exact** where the inputs are counts: Gini impurity, precision, recall and AUC by pair counting are rationals and use the shared `rational` service. Logs and exponentials use a tolerance.
6. **Free text** is self-marked against a model answer and rubric; Bertie may draft a mark (`marking: 'tutor-draft'`), which the learner confirms.
7. **Code** is graded by tests against CI fixtures generated with scikit-learn, pandas and statsmodels pinned to the versions Pyodide ships [unverified which]; comparisons use `allclose` with `rtol` $10^{-6}$ unless stated, and estimators with randomness are called with a fixed `random_state`.

### 2.4 Data, seeds and streams

- **Streams.** Each widget asks `ctx.rng(stream)` with these labels: `data` (item data, fixed), `split` (fold assignments), `init` (initial weights), `batch` (minibatch order), `resample` (bias-variance draws, bootstraps) and `explore`. "New seed" changes only `explore` and `resample`; "New data" exists only in explore mode.
- **Item data are shown.** Every number a learner computes from appears on screen or in the table view. Test points are fixed by the item seed and hidden only by a gate, never regenerated.
- **Sizes.** Widgets keep data small enough to see and to fit the frame budget: 2D classification at most 500 points; 1D regression at most 200; tabular data at most 2,000 rows and 30 features; panels at most 1,000 stocks by 720 months, or 200 stocks by 2,520 days. Larger data belong in code drills.
- **Data shared with code drills** travel as CSV files or literals (prob-stats decision 7). A pure-Python `zq_data` port of `dataset-gen` exists for drills that need fresh draws; those drills never compare values bit for bit, because CPython's `math.exp` is the platform's libm, not `dmath` [inferred].
- **Truth is kept.** Generators return the truth alongside the data: the true function, true coefficients, which features carry signal, which leaks were planted, true labels and planted premia. It reaches Bertie only through `secret()`.

### 2.5 Example screen as data

A Problem screen from 2.1.7 L4. The widget, the check, the misconception and its show-why are all data; no lesson code exists.

```json
{
  "id": "2.1.7.L4.s3",
  "type": "problem",
  "prose": "Each bar is one training example. Its label uses returns from its first day to its last. The shaded block is the test fold.",
  "widgets": [{
    "type": "time-cv-lab", "id": "cv", "label": "Folds and label spans",
    "data": { "gen": "dataset-gen@1/overlap-labels", "T": 40, "horizon": [3, 8], "seed": 2117 },
    "scheme": { "kind": "purged-kfold", "k": 4, "embargo": 0 },
    "split": 2, "task": "purge", "show": ["spans", "bands"], "editable": ["select"]
  }],
  "question": "Tap every training example that must be purged.",
  "check": { "kind": "predicate", "name": "purge-exact", "args": { "widget": "cv", "split": 2 } },
  "misconceptions": [{
    "when": { "kind": "predicate", "name": "purge-misses-left-edge", "args": { "widget": "cv", "split": 2 } },
    "id": "purge-only-after-test",
    "line": "Labels that start before the test fold can still end inside it.",
    "showWhy": { "key": "leak-path" } }]
}
```

### 2.6 Visual roles for this cluster

All tokens are from `prototype/css/tokens.css`. Following the calc-linalg rule, series slot 1 (#2A78D6) is skipped in any plot with a handle, because it sits too close in hue to `--manip` (#2F6BFF). For the same reason the diverging ramp (whose positive end is #2A78D6) is used only in plots without handles, and always with signs or numbers in the cells.

| Role | Style | Examples |
|---|---|---|
| Learner-controlled | `--manip` handles (20px disc, 2px white ring, 1px ink outline); `--manip-wash` regions; `--manip` 2.5px learner curves, kinks, thresholds, breakpoints and $\lambda$ cursors | sketched fits, threshold handles, fold boundaries, barriers, quotes in play mode |
| Truth (the generating process) | `--s3` (aqua) 2px with a "truth" label | true $f(x)$, Bayes-optimal boundary (dashed), true coefficients, planted premium |
| Fitted model and its outputs | `--s2` (orange) 2.5px | the fitted curve, predicted values, the ensemble average, a strategy's equity curve |
| Comparison or reference | `--s6` (violet) 2px dashed | the average fit across training sets, a symmetric strategy, CAPM against three factors |
| Training data | ink dots at 70% opacity, filled | |
| Held-out data | ink rings (1.5px, hollow) | test and validation points; shape, not colour, separates them from training data |
| Training error curve | `--s6` dashed with the label "train" | `error-curves` |
| Test or validation error curve | `--s2` solid with the label "test" or "CV"; error bars as whiskers | `error-curves` |
| Irreducible error and other floors | 1.5px dashed ink, 6 on and 4 off, labelled | $\sigma^2$ line, the 5% critical value |
| Classes | class A `--s2` with a filled circle; class B `--s3` with a filled triangle; class C `--s6` with a filled square. Never colour alone | scatter, regions, confusion cells |
| Decision regions | the class hue at an opacity of $0.06 + 0.30 \cdot \lvert 2p - 1 \rvert$; the $p = 0.5$ boundary in 2px ink | `classifier-plane`, `nn-playground` |
| Fold roles on a time axis | train: `--s6` at 20% with "train"; test: `--s2` at 30% with "test"; purged: `--out` with a diagonal hatch and "purged"; embargo: `--out` with a cross-hatch and "embargo" | `time-cv-lab`, `ml-workbench` |
| Long and short legs, gains and losses | long or gain `--s3` with "+"; short or loss `--s2` with "−" | portfolio legs, pairs trades, P&L bars, network weights |
| Sample periods | in-sample: `--bg-sunken` band labelled; post-sample: no fill; post-publication: dot pattern, labelled | `replication-workbench`, `portfolio-sort` |
| Heatmaps without handles | `--seq-1` to `--seq-6` for magnitudes (SSD, CV score); `--div-neg`, `--div-mid`, `--div-pos` for signed values (alphas, correlations), always with numbers or glyphs | `pairs-lab`, `factor-model-lab`, `cluster-lab` |
| Ruled out or unavailable | `--out` (opacity 0.25 light, 0.3 dark) | values not yet known at the decision time; delisted stocks |

Grading recolours answer objects only: the chosen card, the learner's threshold, region, stump, selected spans or placed breakpoints. Truth, fitted, comparison and data marks never change colour on grading. A reveal uses a 2px `--hint` outline so it never reads as success.

### 2.7 Motion and show-why

- **Direct manipulation is never tweened.** Dragged thresholds, kinks, barriers, breakpoints, centroids and $\lambda$ cursors, and everything derived from them, redraw on the same frame.
- **Training is data arriving.** Loss curves extend as epochs complete; decision fields repaint at most 10 times a second while training runs. Nothing is interpolated between snapshots.
- **Consequence animations** play the result of a learner action and only start from one, at 200 to 600ms with `--ease-morph`, skippable with a tap: a shuffled column's values scattering (`importance-lab`); purged spans fading to hatched (`time-cv-lab`); a stump dropping onto the residuals (`boosting-lab`); points reassigning and centroids stepping (`cluster-lab`); two clusters merging into a dendrogram node (`cluster-lab`); a cohort rolling out of the book (`portfolio-sort`); a matrix reordering by the dendrogram (`cluster-lab`).
- **Show-why** uses the calc-linalg declarative recipe (tween non-answer variables, highlight, annotate, 480 to 800ms). Each widget lists its keys.
- **Reduced motion.** Training shows its state at each pause or on Step only (no live repaint); consequence animations and show-why become a before-and-after pair with a Play button; springs land at once.

### 2.8 Accessibility additions

- **Training announces milestones, not frames:** on pause, on finish, and at each 10% of a run: "Epoch 200 of 1,000. Training loss 0.21, test loss 0.27."
- **Fields are described by what they divide:** "Class A region covers the left 40% and a band at the top; the boundary curves round the cluster at (2, 1)." The table view lists points with their predicted class and probability.
- **Structures have list views:** trees as nested lists ("x1 ≤ 0.42: 30 points, Gini 0.18; leaf A"), networks as a table of layers and weights, dendrograms as merge lists, spans as a table of (id, start, end, role), heatmaps as tables.
- **Timing is adjustable.** `viva` and any timed task meet WCAG 2.2 success criterion 2.2.1: the learner can turn the limit off or extend it tenfold before starting.
- **Colour is never alone:** classes have shapes, long and short legs have signs, fold roles have patterns and words.

### 2.9 Tutor hooks for Brainy Bertie

- **`describe('brief')`** at most 300 characters; **`describe('full')`** at most 1,500 characters. It always names the model, its hyperparameters, the data generator and seed, and the metrics on screen. It never includes more than 20 raw values.
- **`secret()`** holds the truth: the true function or coefficients, which features carry signal, the planted leaks, true test labels, planted premia and their decay. The engine includes it in lesson and explore modes only, under a never-reveal instruction (prob-stats decision 9).
- **Element ids** follow `kind:name`: `point:<i>`, `curve:fit`, `curve:truth`, `slider:lambda`, `span:<id>`, `band:test`, `leaf:<id>`, `node:<id>`, `edge:<from>-<to>`, `cell:<r>,<c>`, `readout:<metric>`.
- **Suggestion chips** Bertie may propose for the learner to tap: "Try depth 3", "Show the test points", "Resample the data", "Turn on purging", "Run 1,000 more days". Bertie never changes answer state.
- **Computed numbers.** On default and complex tiers the engine may give Bertie one tool, `ml_eval(config_patch)`, which scores a variant of the current model on the item's data in the worker and returns metrics under 1 KB. Any number Bertie quotes about "what would happen if" is then computed, not recalled. The `sample` advice to keep tools few and results small holds.
- **Model tiers** [our choice]: `quick` for hints, `default` for "Why?" explanations, `complex` for `viva` marking and for reviewing a replication note.
- **Code** follows the programming catalogue's code guard: no code block longer than 2 lines before the item passes.

### 2.10 Performance

The reference phone is the engine blueprint's (the siblings name a Galaxy A53 or a Pixel 4a class device). Per pointer frame, P95: widget script 4 ms or less and style, layout and paint 6 ms or less, as in the siblings. Workloads in this cluster:

| Workload | Where | Budget or cap |
|---|---|---|
| Decision field, 64 × 64 queries (k-NN on 400 points, a 100-tree forest of depth 8, an RBF SVM with 200 support vectors) | worker | 10 ms or less per field; 32 × 32 during a drag, 64 × 64 on release |
| Refit on a point drag (logistic by Newton steps, LDA, QDA, a depth-6 tree on 400 points) | worker | 5 ms or less [unverified for the tree; measured in G0] |
| Network training step (500 points, 6 layers of 8 units, one epoch) | worker | 2 ms or less; up to 30 epochs a second with field repaints at 10 Hz |
| Lasso or elastic-net path (100 values of $\lambda$, $p \le 50$, $n \le 500$, coordinate descent with a precomputed Gram matrix and warm starts) | worker | 10 ms or less; 10-fold CV of the path 100 ms or less |
| Forest of 500 trees on 500 rows | worker | 400 ms or less, streamed 10 trees at a time [unverified] |
| Portfolio sorts (1,000 stocks by 720 months, deciles, overlapping cohorts) | worker | 50 ms per strategy; the 12 × 12 $J \times K$ grid 1.5 s or less with progress, cached per panel [unverified] |
| CSCV with $S = 16$ blocks (12,870 combinations, 100 strategies) | worker | 100 ms or less, from per-block sums |
| Avellaneda-Stoikov batch (1,000 runs of 200 steps) | worker | 30 ms or less |
| SVG nodes per screen | main | 1,500; dense layers move to Canvas 2D under an SVG layer of focusable handles |

### 2.11 Artifact and web

| Concern | Artifact | Web app |
|---|---|---|
| All concept widgets (JavaScript `ml-core`, `panel-sim`, `backtest-core`) | full | full |
| Implement-it drills (pure Python or NumPy) | MicroPython with ulab if the WebAssembly probe passes and CI tags the drill compatible [unverified]; otherwise handoff | Pyodide |
| Use-the-library drills (scikit-learn, pandas, statsmodels) | handoff | Pyodide |
| PyTorch drills | local only, with paste-back of the test output | local only, with paste-back |
| Learner CSV upload (workbenches) | file input [unverified whether the Artifact sandbox allows it] | file input |
| Exporting a script, ledger or results note | `downloads` capability | Blob link |
| Saving workbench ledgers and notes | `db` capability, one document per project, at most 64 KB | IndexedDB, synced by the engine |
| Tutor and `viva` transport | `sample` capability on the viewer's account | proxy |
| Real data (Ken French, yfinance) | none (the CSP blocks other hosts) | none in the app; the learner downloads files and runs code locally or loads the CSV |

### 2.12 Services this cluster needs (not widgets)

Requirements on the engine's shared modules, written as acceptance tests. The engine blueprint owns their design.

| Module | Must provide | Accuracy acceptance | Used by |
|---|---|---|---|
| `dmath` | Section 2.1, requirement 1 | bit-identical across browsers | everything seeded |
| `ml-core` | OLS and ridge (QR and SVD); lasso and elastic net by coordinate descent with warm starts (the glmnet strategy); forward stepwise; best subset to $p = 12$; logistic regression (Newton for small problems, L-BFGS with L2); softmax regression; LDA, QDA, Gaussian naive Bayes; k-NN (brute force, k-d tree in 2D); linear and RBF SVM by SMO for at most 500 points; CART (exact greedy splits, Gini, entropy, misclassification, squared error, second-order gain; cost-complexity pruning); bagging, random forests, extra trees; gradient boosting (squared and log loss, shrinkage, subsampling) and AdaBoost.M1; k-means (Lloyd, k-means++ seeding) and agglomerative clustering (single, complete, average, Ward); dense networks with ReLU, tanh, sigmoid and linear activations, SGD, momentum, RMSProp and Adam, L2 and dropout; permutation importance, drop-column importance, partial dependence and ICE, exact Shapley values for at most 8 features. Every model can yield its internals | Parity with scikit-learn on 30 fixtures per model: closed-form models to $10^{-10}$ relative; iterative convex models to $10^{-6}$; trees identical in structure on tie-free data (tie rule: lowest feature index, then lowest threshold); forests and networks by distributional tests across 20 seeds, plus finite-difference gradient checks (relative error at most $10^{-6}$) and cross-browser determinism (identical loss after 1,000 steps) | most of section 6 |
| `dataset-gen` | 1D regression (sine, cubic, step, absolute value, Runge's function; homoscedastic or fanning noise); linear $p$-feature data with sparse or dense truth and equicorrelated or Toeplitz design; 2D classification (blobs, moons, circles, XOR, spirals, linear with label noise, imbalanced); financial features with overlapping forward-return labels; leaky variants with planted leaks (centred windows, future-dated features, full-sample scaling, target-derived features); a tabular capstone set | Generated statistics match their stated parameters within 4 standard errors at $n = 10^6$ in CI; golden hashes per seed | section 6 |
| `panel-sim` | A monthly and daily equity panel (section 7.0) | Planted premia recovered by the reference sorts within 4 standard errors at large $N$ and $T$; golden hashes per seed | section 7, `leakage-detective`, `ml-workbench` |
| `backtest-core` | Portfolio returns from weights; equal and value weights; long-short legs; overlapping cohorts; turnover; costs per unit of turnover; delisting returns; performance statistics (mean, SD, Sharpe ratio, $t$ with Newey-West, drawdown through the programming catalogue's drawdown functions) | Against a pandas reference on 20 fixtures to $10^{-10}$ | section 7, `overfit-lab` |
| `sharpe-stats` | Sharpe ratio standard errors (IID and non-normal), Lo's annualisation factor, PSR, MinTRL, the expected maximum of $N$ Sharpe ratios, DSR, MinBTL, haircuts (Bonferroni, Holm, BHY), CSCV and PBO | Formulas checked against hand-computed cases and simulation in CI; the published examples [recalled, unverified] as secondary checks | `sharpe-lab`, `overfit-lab`, `multiple-testing` |
| `as-sim` | The Avellaneda-Stoikov model in discrete time: mid-price as arithmetic Brownian motion, fills with probability $\lambda(\delta)\,dt$ per side, inventory, cash and marked-to-market wealth; strategies: inventory (AS), symmetric, fixed spread, learner-driven | Closed-form quotes exact; batch means against an independent Python implementation on fixed seeds | `market-maker-sim` |
| `tests` additions | Newey-West (Bartlett kernel; default lag $\lfloor 4(T/100)^{2/9} \rfloor$); Hansen-Hodrick for overlapping returns; the GRS test; Fama-MacBeth with plain and Newey-West standard errors; BHY; ADF reused by `fracdiff-lab` | Against statsmodels fixtures as in prob-stats section 2.10; GRS against a reference implementation, with its covariance divisors fixed by the fixture [unverified which convention] | `factor-model-lab`, `portfolio-sort`, `multiple-testing`, `fracdiff-lab` |
| Fixture pipeline | The prob-stats pipeline extended: CPython with scikit-learn, pandas and statsmodels pinned to Pyodide's versions writes golden JSON for every `ml-core` model and every research computation | CI fails on any mismatch | everything above |

---

## 3. New primitive

### 3.1 `span-track`: Span track

**Primitive (host layer) · P2 · G0.** Rows of time intervals on one time axis: label spans, folds, formation and holding windows, trades and sample periods, with overlap counting and per-span selection.

- **Purpose.** Much of financial machine learning and paper replication is about which interval overlaps which: a label's return window against a test fold (purging), a feature's availability against a decision time (leakage), the formation, skip and holding windows of a momentum cohort, a pair trade's open and close, a paper's sample against its publication date. One primitive draws and edits all of them, computes overlaps and concurrency, and makes every span selectable, so a set answer such as "tap the labels to purge" needs no composite-specific code.
- **Serves.** 2.1.7 L1 to L8; 2.1.8 L2, L3, L9; 2.1.10 L2; 3.1.1 L5; 3.1.2 L2, L4; 3.1.4 L3; 3.1.6 L7. Hosts: `time-cv-lab`, `labelling-lab`, `leakage-detective`, `portfolio-sort`, `pairs-lab`, `replication-workbench`, `ml-workbench`; and, cross-cluster, `forecast-lab`'s rolling origin (2.2) and the 2.3 backtesting project.
- **Uses.** `plot-2d` time axis (date or sample-index ticks), `drag-point` (span-end handles, constrained to the axis and to sample times), `marks` (bars, bands, fill patterns, `step` for the concurrency series).
- **Layouts.**
  - `rows`: one span per row, ordered by start (label spans, trades).
  - `lanes`: spans packed greedily into the fewest lanes without overlap (many short trades).
  - `bands`: full-height bands behind other layers (folds, sample periods, embargo zones).
  - `gantt`: named rows with several spans each (formation, skip and holding windows of each cohort; a feature's event and availability times).
- **Derived layers.** `concurrency`: the number of spans covering each sample time, drawn as a step series below the rows; computed by a sweep over sorted endpoints in $O(n \log n)$. `overlaps(a, b)`: the overlap rule used for purging (section 6.6.1), exposed to hosts and predicates.
- **Interactions.**
  - Pointer: tap a span to select or deselect it (multi-select where allowed); drag a span's end handles; drag its body to move it; drag across empty track to brush a time window, which selects every span the window touches; tap-then-tap moves a span without dragging.
  - Keyboard: spans form a roving group in start-time order. Left and Right move to the previous or next span; Up and Down change row; Space selects; `[` and `]` move the focused end handle by one sample (Shift: 10); M then arrows moves the whole span; E opens the exact editor (dates or indices); Escape cancels a drag.
- **State.** `{ spans: { id: string; row: number; t0: number; t1: number; role: string }[]; selected: string[]; brush?: [number, number] }`. Roles change through the host (for example `train` becomes `purged`), never by direct learner edit.
- **Answers.** `set` (selected span ids), `interval` (one span's $[t_0, t_1]$), `point` (one end), `state` (through host predicates such as `purge-exact`).
- **Config.**

```ts
interface SpanTrackConfig {
  axis: { kind: 'index' | 'date' | 'trading-day' | 'month'; min: number; max: number; label?: string };
  spans: { id: string; row?: number; t0: number; t1: number; role: SpanRole; label?: string; closed?: '[]' | '[)' }[];
  layout: 'rows' | 'lanes' | 'bands' | 'gantt';
  rowLabels?: string[];                          // gantt
  editable?: ('start' | 'end' | 'move')[];
  editableRoles?: SpanRole[];                    // which spans may be edited
  snap?: 'sample' | 'day' | 'month' | 'none';
  select?: 'none' | 'single' | 'multi';
  selectableRoles?: SpanRole[];
  concurrency?: boolean;                         // draw the coverage step series
  maxRowsShown?: number;                         // above this, rows aggregate into a density strip
}
type SpanRole = 'train' | 'test' | 'purged' | 'embargo' | 'label' | 'formation' | 'skip' | 'holding'
              | 'long' | 'short' | 'in-sample' | 'post-sample' | 'post-publication' | 'event' | 'available' | 'neutral';
```

- **Visual.**
  - Row spans are 8px bars with 2px gaps; bands are full-height fills. Each role has the style in section 2.6 (train `--s6` at 20%, test `--s2` at 30%, purged and embargo `--out` with diagonal and cross hatches, long `--s3` with "+", short `--s2` with "−", and so on) and a word label at the first span of each role.
  - End handles are `--manip` pills (12 × 20px with a 44px hit area), shown only on editable spans.
  - A selected span gets a 2px `--manip` outline. Grading recolours selected spans only (green or amber outline plus a badge); host roles never change colour on grading.
  - The concurrency series is a 1.5px ink step line with its axis on the right.
- **Motion.** Handle drags are direct; release snaps to the nearest sample with `spring-snap`. Role changes caused by a learner action (purging after a fold edit) cross-fade over 200ms with `--ease-standard`.
- **Reduced motion.** Snaps and role changes are instant.
- **Accessibility.** A group named by the host ("Label spans, 40 examples"). Each span is focusable with a name such as "Label 14, days 30 to 38, training". Selection is announced on commit ("Selected 6 of 40"). The table view lists id, row, start, end and role, with a concurrency column when shown.
- **Tutor hooks.** Describe: "40 label spans, lengths 3 to 8 days. Test fold days 21 to 30. Selected: 14, 15, 16." Ids: `span:<id>`, `row:<r>`, `handle:<id>:start`, `handle:<id>:end`, `band:<role>`, `series:concurrency`.
- **Performance.** SVG up to 300 spans; Canvas 2D above, up to 20,000, with an SVG overlay for the focused and selected spans; a brush selects in $O(\log n + k)$ from an interval index built once per data change.
- **Artifact and web.** No difference.
- **Generators.** None of its own; hosts generate.
- **Cross-cluster.** The 2.3 backtesting engine (holding periods, a look-ahead audit), 2.2 rolling-origin evaluation, 1.7 option lifetimes and expiry ladders.

---

## 4. Additions to shared primitives

These primitives are specified in the sibling catalogues. This cluster needs the additions below; without them the named lessons cannot be built.

| Primitive (owner) | Addition | First needed |
|---|---|---|
| `marks` (engine) | `field`: a grid of values (scalar or per-class probabilities) drawn on the Canvas layer of section 2.1 requirement 6, with a palette function (`sequential`, `diverging`, `classes`) and opacity rule; `boundary` contours at a level or at argmax changes, by marching squares from the shared `sample` module, drawn in SVG | 2.1.2 L6 |
| `marks` | `partition`: axis-aligned rectangles with ids, labels and outlines, for tree leaves and sort buckets | 2.1.5 L1 |
| `marks` | `norm-ball`: the $L_1$ diamond, $L_2$ disc, elastic-net ball $\alpha\lVert\beta\rVert_1 + (1 - \alpha)\lVert\beta\rVert_2^2 \le t$, $L_q$ for $q = 0.5$, and the $L_0$ cross, all for a budget $t$; shared with calc-linalg's `condition-number` norm-balls mode | 2.1.4 L3 |
| `marks` | `scatter` gains a shape channel (circle, triangle, square) and a hollow channel (training filled, held-out hollow); `bars` gain error whiskers and a sign glyph | 2.1.1 L1 |
| `plot-2d` (engine) | Reversed log axes ($\lambda$ decreasing to the right, as glmnet plots read); inset panels anchored to a data point (a histogram at $x_0$); a weight-space preset with equal aspect and the origin marked | 2.1.1 L5, 2.1.4 L2 |
| `slider` (engine) | Log scale with decade ticks and a typed exact value ($\lambda$, learning rate, $\gamma$); paired thumbs on one track for windows | 2.1.4 L2 |
| `sim-runner` (calc-linalg) | Job kinds on the worker protocol of section 2.1 requirement 2: `train` (iterate a model with snapshots), `resample-fit` (refit on $M$ training sets), `strategy-zoo`, `cscv`, `as-market`, `tick-stream`, `panel` (calls `panel-sim`), `bet-sequence`, `nn-distance` | 2.1.1 L5 |
| `stepper` (programming, trace mode) | Reads job snapshots: epochs, boosting rounds, folds, k-means iterations, Fama-MacBeth months, walk-forward origins | 2.1.3 L2 |
| `token-tray` (engine) | Typed expression slots: tokens carry an arity and a type (`series`, `cross-section`, `scalar`, `window`); dropping an operator onto a filled slot wraps it; invalid drops spring back with the type mismatch named | 3.1.1 L7 |
| `node-link` (programming) | `layered-dense` layout for networks (edge thickness proportional to $\lvert w \rvert$, sign by colour plus a dash pattern for negative weights, node thumbnails as Canvas mini-fields); `dendrogram` layout with a height axis and a draggable cut line; tidy-tree nodes linked to `partition` boxes | 2.1.5 L1, 2.1.6 L2 |
| `cell-grid` (programming) | Signed heatmaps with numbers and glyphs in cells; row and column headers; a permutation reorder played as a consequence animation (cluster quasi-diagonalisation); a paint mode for split matrices (CPCV) | 2.1.5 L14, 2.1.7 L6 |
| `value-table` (programming, frame mode) | A panel view (dates by assets) with as-of greying: cells not yet known at a chosen decision time render `--out`; a column-shuffle animation for permutation importance | 2.1.5 L12, 2.1.8 L2 |
| `code-cell` (programming) | ML helpers: `assert_no_lookahead(fn, frame)` (perturbs future rows and asserts that past outputs do not change), `assert_folds_purged(splits, t0, t1, embargo)`, `assert_fixture(name, value, rtol)` against scikit-learn fixtures, `zq_data` loaders; scikit-learn suites (web-only); the local paste-back mode for PyTorch drills (the learner pastes the test runner's output, which carries a hash of the test file) | 2.1.1 (first drill) |
| `sketch-pad` (calc-linalg) | Two labelled curves on one set of axes (train and test), with the features `interior-min`, `monotone`, `plateau` and `peak-near` | 2.1.1 L2 |
| `region-select` (calc-linalg) | Paint mode on a coarse grid (Stage 0 already recommends it), used to predict decision regions | 2.1.2 L6 |

---

## 5. Extensions to widgets owned by the sibling catalogues

Each row is a mode or change this cluster needs from a widget specified elsewhere. The owning catalogue keeps the full spec; the more demanding configuration wins.

| Widget (owner) | What this cluster needs | Priority, wave | Lessons |
|---|---|---|---|
| `regression-lab` (prob-stats) | **Prediction mode:** a train and test split, out-of-sample $R^2 = 1 - \frac{\sum (y - \hat y)^2}{\sum (y - \bar y_{\text{train}})^2}$, confidence against prediction bands at a new $x$. **HAC mode, now required:** Newey-West and Hansen-Hodrick standard errors with the lag shown; an overlapping-returns demonstration where $K$-month holding returns sampled monthly make plain $t$-statistics too large by roughly $\sqrt{K}$ [inferred for positively autocorrelated overlaps]. Hat values feed `cv-lab`'s LOOCV shortcut | P2, G1; HAC P2, H1 | 2.1.2 L1; 2.1.3 L3; 3.1.2 L6 |
| `summary-table` (prob-stats) | The `HAC` covariance type with `maxlags`, printed as statsmodels prints it | P2, H1 | 3.1.2 L6; 3.1.3 L3 |
| `multiple-testing` (prob-stats) | A $t$-statistic axis beside the p-value axis; BHY (Benjamini-Yekutieli, valid under arbitrary dependence: compare sorted p-values with $\frac{i}{m \sum_{j=1}^{m} 1/j} q$); `zoo-timeline` mode (factors per year from a seeded zoo and the rising hurdle under each method); `unobserved-tests` mode (add $u$ unpublished failures and watch the adjustment tighten); the zoo mode embeds `overfit-lab`'s zoo panel (decision 6) | P2, H2 | 3.1.3 L8; 3.1.6 L1 to L5, L7 |
| `forecast-lab` (prob-stats) | Its shuffled-CV comparison embeds `time-cv-lab`'s fold strip and purge logic (decision 5) | P2, G4 | 2.2.3 L9 (theirs); 2.1.7 L1 |
| `coint-lab` (prob-stats) | A pair source "selected by distance" from `pairs-lab`; trading-mode statistics exported to `pairs-lab`'s comparison | P2, H2 | 3.1.4 L6, L7 |
| `test-lab` (prob-stats) | A compact ADF readout (statistic, 5% critical value, verdict) embeddable in `fracdiff-lab` | P2, G4 | 2.1.8 L10 |
| `contingency-table` (prob-stats) | Confusion preset: predicted by actual, with precision, recall, specificity, F1 and MCC in the margins, and a cost-matrix overlay | P2, G1 | 2.1.2 L7, L8, L12 |
| `icon-array` (prob-stats) | Imbalance mode: 1,000 glyphs coloured by confusion outcome, bound to `threshold-lab`'s threshold | P2, G1 | 2.1.2 L7 |
| `sampling-lab` (prob-stats) | Bootstrap rows never drawn are marked out-of-bag; the share converges to $1 - e^{-1}$ | P2, G1 | 2.1.3 L9; 2.1.5 L6 |
| `posterior-lab` (prob-stats) | MAP mode in coefficient space: a Gaussian prior's circular contours against the ridge disc, a Laplace prior's diamonds against the lasso, with $\lambda = \sigma^2/\tau^2$ for ridge and $\lambda = 2\sigma^2/b$ for the lasso (Laplace scale $b$, loss $\lVert y - X\beta \rVert^2$) | P2, G1 | 2.1.4 L10 |
| `dist-explorer` (prob-stats) | A "maximum of $N$" family: density $N\varphi(x)\Phi(x)^{N-1}$ for $N$ independent standard normals, with the $E[\max]$ approximation marked | P2, G4 | 2.1.9 L4 |
| `descent-lab` (calc-linalg) | RMSProp and Adam beside the existing momentum and SGD modes; a race of four optimisers from one start; minibatch noise on a loss defined by data (logistic loss, a two-weight network); step-decay and cosine learning-rate schedules | P2, G3 | 2.1.2 L5; 2.1.6 L5 |
| `dependency-graph` (calc-linalg) | Backprop mode extended: neuron operations (affine, ReLU, sigmoid, softmax with cross-entropy) as nodes; "fill the gradient" tasks on edges; a finite-difference check readout; layout through `node-link` | P2, G3 | 2.1.6 L6 |
| `pca-lab` (calc-linalg) | PCR link (regress on the top $m$ components, sending coefficients to `regularisation-path`); a returns-panel preset whose first component is the market | P2, G1 | 2.1.4 L4, L11 |
| `quadratic-form` (calc-linalg) | Ridge-shift mode: $X^\top X + \lambda I$ moves every eigenvalue up by $\lambda$ and rounds the bowl | P2, G1 | 2.1.4 L4 |
| `condition-number` (calc-linalg) | Its norm-balls mode draws with the shared `norm-ball` mark; collinearity link from `feature-builder` | P2, G1 | 2.1.2 L2; 2.1.4 L3 |
| `surface-explorer` (calc-linalg) | Loss surfaces over two weights: convex logistic loss; the non-convex loss of a two-weight network with its symmetric minima | P2, G3 | 2.1.2 L5; 2.1.6 L5 |
| `pipeline-flow` (programming) | `sklearn` mode, which the programming catalogue proposes: stages are transformers and estimators; each connector shows which rows the stage was fitted on and which it transformed; a stage fitted on test rows is flagged "fitted on test" with a hatch and a word | P2, G4 | 2.1.3 L10; 2.1.8 L3; 2.1.10 L2 |
| `groupby-lab` (programming) | Cross-sectional mode: rank, z-score and `qcut` within each date | P2, H1 | 3.1.2 L3 (drill) |
| `time-series-lab` (programming) | Alignment trap: a centred rolling window is flagged as using future rows; `shift` direction shown as arrows | P2, G4 | 2.1.8 L2 |
| `drawdown-lab` (programming) | Accepts a return series bound from another widget (section 2.1 requirement 4) | P2, G4 | 2.1.9 L1 to L5 |
| `setup-checklist` (programming, project mode) | Project templates for the 2.1 capstone and the 3.1 replication: README sections, tests present, results note present, data provenance stated, survivorship statement where the data route needs one | P2, G5 and H2 | 2.1.10 L5; 3.1.6 L8 |
| `free-response` (Stage 0) | Timed mode with a no-notes lock (Notebook and summaries hidden while active) and an exportable transcript; `viva` builds on it | P1, E | 1.6 exit; 2.1.10 L6 |

**Three extensions carry most of the weight** and get a short spec here.

- **`multiple-testing` for Harvey, Liu and Zhu.** The hurdle on the $t$ axis is the point. Bonferroni at $M$ tests needs $\lvert t \rvert > \Phi^{-1}(1 - \frac{0.025}{M})$; at $M = 300$ that is about 3.76 (normal approximation). The zoo-timeline mode draws a seeded factor zoo whose count by year follows a configurable curve (the paper's own count of 316 factors by 2012 is [recalled, unverified] and appears only as a labelled context line). A year slider moves a cursor; the hurdle for each method is drawn as a step series; dots are factors with their $t$-statistics; dots under the hurdle fade to `--out`. Show-why `hurdle-rises` advances the year over 800ms while the line climbs. Tutor describe adds "Year 2005: 180 tests; Bonferroni hurdle 3.64; 22 factors clear it."
- **`dependency-graph` backprop.** Nodes are operations with values from the forward pass; edges carry local derivatives; the backward pass multiplies along edges and sums at forks. The learner fills one edge gradient per step; Check uses `numeric` with relative tolerance $10^{-3}$. A "check by nudging" button perturbs one input by $10^{-4}$ and shows the finite-difference estimate beside the backpropagated value. Show-why `fork-sum` highlights both paths into a node whose gradient the learner took from one path only.
- **`descent-lab` optimiser race.** Four markers start from one point on an elongated bowl or a data-defined loss: SGD, momentum ($\beta = 0.9$), RMSProp, Adam ($\beta_1 = 0.9$, $\beta_2 = 0.999$, bias-corrected). The learning-rate slider is shared, so the race shows that the same rate means different things to each. Minibatch mode redraws the loss contours from a different batch each step (faint) while the full-data contours stay in ink, so "noisy gradient" is a picture. The divergence threshold $\eta > 2/\lambda_{\max}$ from the existing spec stays the gradable fact.

**Misconceptions the extensions add** (texts in section 10): `t-two-is-enough-for-a-new-factor` and `ignore-unpublished-tests` (`multiple-testing`), `gradient-from-one-path` (`dependency-graph`), `overlapping-returns-plain-t` (`regression-lab`); `descent-lab` reuses `high-learning-rate-trains-faster`.

---

## 6. Machine-learning composites (2.1)

All 32 composites in this section are P2, in waves G1 to G5, except `viva`, which is P1. Each entry states only what differs from the shared contract and section 2. Default data come from `dataset-gen` (section 2.12); a data spec names a generator, its parameters and a seed, or a CSV file on the web app.

```ts
type DataSpec =
  | { gen: 'dataset-gen@1/regression-1d'; f: 'sin' | 'cubic' | 'step' | 'abs' | 'runge' | 'linear';
      n: number; nTest: number; sigma: number; design: 'grid' | 'uniform'; fan?: number; seed: number }
  | { gen: 'dataset-gen@1/linear'; n: number; nTest: number; p: number; sparsity: number;
      corr: { kind: 'none' | 'equi' | 'toeplitz'; rho: number }; snr: number; seed: number }
  | { gen: 'dataset-gen@1/classes-2d'; shape: 'blobs' | 'moons' | 'circles' | 'xor' | 'spirals' | 'linear';
      n: number; nTest: number; noise: number; flip?: number; positiveRate?: number; seed: number }
  | { gen: 'dataset-gen@1/overlap-labels'; T: number; horizon: [number, number]; featureAr: number;
      signal: number; leaks?: LeakKind[]; seed: number }
  | { gen: 'dataset-gen@1/tabular'; rows: number; features: FeatureSpec[]; target: 'continuous' | 'binary'; seed: number }
  | { csv: string; target: string; features: string[]; time?: string };
type LeakKind = 'centred-window' | 'future-dated' | 'full-sample-scale' | 'target-derived' | 'survivor-only';
```

### 6.1 The learning problem

#### 6.1.1 `fit-explorer`: Fit explorer

**Composite · P2 · G1.** Fit a 1D regression at chosen flexibility and judge it on points it has not seen.

- **Purpose.** The founding idea of the course: a model is judged on new data. Training error always falls with flexibility; test error falls, then rises. The widget fits polynomials, k-nearest neighbours, natural splines and random ReLU features (for double descent), or takes the learner's own sketched curve. Peek mode is the Trap: choose with the test set and the score on a fresh set is worse than promised. SNR mode shows what finance looks like: when the truth explains 1% of the variance, an out-of-sample $R^2$ of 1% is the ceiling.
- **Serves.** 2.1.1 L1, L2, L3, L8, L9; 2.1.4 L12; 2.1.5 L3 (link).
- **Uses.** `plot-2d`, `marks` (scatter with hollow held-out points, `curve`, residual segments), `sketch-pad` (sketch mode), `slider` (degree, $k$, knots, features $p$, noise), `choice` (model chips), `live-formula` (readouts), `error-curves` (linked panel), `least-squares-fit` (link for degree 1 to 3), `basis-lab` (link for splines).
- **Interactions.**
  - Pointer: in sketch mode drag control points through the training data, then tap "New points"; in flex mode drag the flexibility slider; reveal test points; in peek mode tap the degree that wins on the test points, then reveal the fresh set; in SNR mode slide the noise.
  - Keyboard: sketch control points are 2D handles (calc-linalg keyboard map); sliders; R reveals the gated points when allowed; chips with arrow keys.
- **State.** `{ model: 'sketch' | 'poly' | 'knn' | 'spline' | 'rff'; degree?: number; k?: number; knots?: number; p?: number; sketch?: Vec2[]; revealed: ('test' | 'fresh')[]; peekPick?: number; sigma?: number }`.
- **Answers and checks.** `choice` (which curve wins on new points; predicted fresh score), `numeric` (the $k$-NN prediction at $x_0$ from the shown neighbours, exact; the degree with the lowest test error, margin-checked under rule 3 of section 2.3), `point` via the linked `error-curves`.
- **Config.**

```ts
interface FitExplorerConfig {
  data: Extract<DataSpec, { gen: 'dataset-gen@1/regression-1d' }>;
  mode: 'sketch' | 'flex' | 'peek' | 'snr' | 'explore';
  models: ('poly' | 'knn' | 'spline' | 'rff')[];
  ranges?: { degree?: [number, number]; k?: [number, number]; knots?: [number, number]; p?: [number, number] };
  show: ('truth' | 'residuals' | 'readouts' | 'error-curves')[];
  gateTest: boolean;                       // test points hidden until revealed
  freshSet?: number;                       // peek mode: size of the third set
}
```

- **Visual.** Training points as ink dots; held-out points as ink rings; the fitted curve `--s2` 2.5px; the truth `--s3` 2px, shown only where configured; the learner's sketch `--manip` 2.5px with handles; residual segments 1px `--text-muted`. Readouts: "Train MSE 0.08 · Test MSE 0.61" in tabular figures; out-of-sample $R^2$ in SNR mode. Answer objects: the chosen card and the field; the sketch only when a sketch is graded.
- **Motion.** Direct: the fit redraws on every slider frame. Show-why keys: `fresh-points` (fresh points drop in over 400ms and residual segments draw to the learner's curve); `neighbours` (the $k$ nearest points ring and connect to $x_0$, and their mean appears).
- **Reduced motion.** Fresh points appear at once with residuals.
- **Accessibility.** Table of $x$, $y$, set (train, test, fresh), fitted value and residual. Describe: "Degree 9 polynomial on 15 training points: train MSE 0.02, test MSE 1.84. The curve swings between 0.8 and 0.95."
- **Tutor hooks.** Ids: `point:<i>`, `curve:fit`, `curve:truth`, `curve:sketch`, `handle:<i>`, `slider:degree`, `slider:k`, `slider:p`, `readout:train`, `readout:test`, `set:fresh`. Secret: the true function, $\sigma$, and test values while gated.
- **Performance.** Polynomial fits by QR on a Legendre basis over the scaled range (degree 15 on 30 points stays well conditioned); about 0.1 ms per fit on the main thread. Random features: the $p$-sweep (1 to 200 features, minimum-norm least squares) runs once per data set in the worker, about 400 ms [unverified]; dragging $p$ reads cached fits.
- **Artifact and web.** No difference. The 2.1.1 drill (k-NN regression in NumPy) is implement-it tier.
- **Generators.** `knn-predict` (exact), `pick-the-winner` (prediction of which of two shown curves wins, with a margin of at least 20% in test MSE), `best-degree` (unique argmin with margin), `snr-ceiling` (compute $R^2_{\text{truth}} = \frac{\mathrm{Var}(f)}{\mathrm{Var}(f) + \sigma^2}$). Difficulty 1 to 3.
- **Misconceptions.** `lower-train-error-is-better`, `test-set-reuse-is-harmless`, `high-r2-expected-in-finance`, `k1-is-best`.

#### 6.1.2 `loss-lab`: Loss lab

**Composite · P2 · G1.** What each loss makes you predict, and how each treats an outlier.

- **Purpose.** A loss is a choice about what to predict. One constant prediction $c$ against data: squared loss is minimised at the mean, absolute loss at the median (any point between the middle two for even $n$), Huber loss between them, and the pinball loss $\rho_\tau$ at the $\tau$-quantile (the bridge to quantile regression and value at risk). For classification, losses are functions of the margin $m = y f(x)$ with $y \in \{-1, +1\}$: 0-1, hinge $\max(0, 1 - m)$, logistic $\log_2(1 + e^{-m})$, exponential $e^{-m}$ and squared $(1 - m)^2$; the 0-1 loss is flat almost everywhere, so it cannot be trained by gradients, and squared loss punishes points that are "too correct".
- **Serves.** 2.1.1 L4; 2.1.2 L5, L11; 2.1.5 L9, L11 (exponential loss behind AdaBoost).
- **Uses.** `plot-2d` (a vertical dot strip of the data, the loss curve $L(c)$, the margin plot), `drag-point` ($c$ on the $y$ axis; data points), `marks` (`curve`, residual bars), `slider` ($\delta$, $\tau$), `choice` (loss chips), `live-formula`.
- **Interactions.**
  - Pointer: drag $c$; drag any data point, usually the outlier; choose one or several losses; slide $\delta$ and $\tau$; in margin mode drag a point's margin along the axis.
  - Keyboard: $c$ is a slider; points are vertical handles; chips; sliders.
- **State.** `{ c: number; data: number[]; losses: LossId[]; delta: number; tau: number; mode: 'constant' | 'margin' | 'per-point' }`.
- **Answers and checks.** `point` ($c$ at the minimiser, tolerance in data units), `interval` (the set of minimisers of absolute loss for even $n$), `numeric` (the loss at $c$; the minimiser's value), `mapping` (loss names to curves), `choice` (which prediction resists the outlier).
- **Config.**

```ts
interface LossLabConfig {
  mode: 'constant' | 'margin' | 'per-point';
  data: number[] | { n: number; outlier?: number; seed: number };
  losses: ('squared' | 'absolute' | 'huber' | 'pinball' | 'zero-one' | 'hinge' | 'logistic' | 'exponential' | 'squared-margin')[];
  delta?: number; tau?: number;
  movable: ('c' | 'points')[];
  showMinimiser: 'live' | 'after-check' | 'never';
}
```

- **Visual.** Data dots in ink; $c$ as a horizontal `--manip` line with a handle; residual bars from each point to $c$ in `--s2` at 50%, their squares drawn as `--s2` squares at 15% when squared loss is on (so a large residual's square visibly dominates); loss curves in `--s2`, `--s6` and `--s4` with direct labels; minimisers as dashed ink ticks labelled "mean", "median", "$\tau$-quantile". Answer objects: the $c$ handle.
- **Motion.** Direct. Show-why `outlier-pull`: the outlier slides outwards over 700ms while the mean line follows and the median line stays.
- **Reduced motion.** Before-and-after pair.
- **Accessibility.** "c = 2.4. Squared loss 18.2 (minimum 11.6 at the mean, 3.1). Absolute loss 9.0 (minimum 8.2 at any c from 2.0 to 2.6)." Table of points and residuals.
- **Tutor hooks.** Ids: `handle:c`, `point:<i>`, `curve:<loss>`, `tick:mean`, `tick:median`, `tick:quantile`, `slider:delta`, `slider:tau`. Secret: none beyond the minimisers while hidden.
- **Performance.** Loss curves on 200 grid points; the Huber minimiser by iteratively reweighted least squares to $10^{-12}$; all under 1 ms.
- **Artifact and web.** No difference.
- **Generators.** `minimiser` (data with tidy mean and median), `huber` (minimiser value to tolerance), `pinball` (quantile index), `margin-match` (mapping). Difficulty 1 to 3.
- **Misconceptions.** `mean-minimises-absolute-loss`, `squared-loss-is-neutral`, `zero-one-is-trainable`.

#### 6.1.3 `error-curves`: Error curves

**Composite · P2 · G1.** Training, validation and test error against complexity, training time or sample size; sketched before they are shown.

- **Purpose.** The single picture that most of 2.1 returns to. The learner first sketches what they expect (training error falls; test error has an interior minimum), then reads the real curves bound to a host widget's control. Modes: the one-standard-error rule (pick the simplest model whose CV error is within one standard error of the minimum); learning curves against $n$ (training error rises, test error falls, both approach bias plus noise); training curves against epochs or boosting rounds (early stopping); double descent against the number of features $p$, with the spike at $p = n$.
- **Serves.** 2.1.1 L2, L6; 2.1.3 L5; 2.1.4 L8, L12; 2.1.5 L4, L9; 2.1.6 L8.
- **Uses.** `plot-2d` (log or reversed log axes for $\lambda$), `marks` (`curve`, whiskers, markers), `sketch-pad` (two labelled curves with the section 4 features), `drag-point` (the cursor, bound to the host), `value-table`.
- **Interactions.**
  - Pointer: in predict mode sketch the train curve and the test curve, then Check; in read mode drag the cursor (the host follows through the binding) or move the host and watch the cursor; in one-se mode tap the chosen complexity.
  - Keyboard: sketch control points as handles; the cursor is a slider over the $x$ positions; T opens the table.
- **State.** `{ mode: string; cursor: number; sketch?: { train: Vec2[]; test: Vec2[] }; picked?: number; revealed: boolean }`.
- **Answers and checks.** `curve` (features: train `monotone` decreasing; test `interior-min`; for learning curves train `monotone` increasing; for double descent `peak-near` $p = n$), `point` (the picked complexity: exact $\lambda_{1\text{se}}$ or degree, margin-checked), `numeric` (the minimum CV error and its standard error).
- **Config.**

```ts
interface ErrorCurvesConfig {
  x: { kind: 'degree' | 'k' | 'lambda' | 'leaves' | 'rounds' | 'epochs' | 'features' | 'n' | 'df'; scale: 'linear' | 'log' | 'reversed-log' };
  source: { bind: string } | { series: { x: number[]; train?: number[]; cv?: number[]; cvSe?: number[]; test?: number[]; bias2?: number[]; variance?: number[] } };
  show: ('train' | 'cv' | 'test' | 'noise' | 'decomposition')[];
  mode: 'predict' | 'read' | 'one-se' | 'learning' | 'double-descent';
  noiseFloor?: number;
}
```

- **Visual.** Train `--s6` dashed; CV `--s2` solid with whiskers; test `--s2` solid when it is the only held-out curve, and `--s4` 2.5px with a direct label when it shares the plot with CV; noise floor dashed ink; the learner's sketches `--manip` with "your train" and "your test" labels; the minimum and one-standard-error markers as ink triangles with labels. Answer objects: the sketches and the picked marker.
- **Motion.** Curves extend as the host's job reports progress (data arriving). Show-why `gap-opens` highlights the widening gap between train and test as complexity rises.
- **Reduced motion.** Curves appear complete.
- **Accessibility.** Table of $x$, train, CV, standard error and test. "Test error lowest at degree 3 (0.41). Training error keeps falling to 0.02 at degree 12."
- **Tutor hooks.** Ids: `curve:train`, `curve:cv`, `curve:test`, `whisker:<x>`, `cursor`, `line:noise`, `marker:min`, `marker:1se`, `sketch:train`, `sketch:test`. Secret: the test curve while gated.
- **Performance.** At most 200 $x$ positions; the host computes values in its worker; drawing under 1 ms.
- **Artifact and web.** No difference.
- **Generators.** Through the host's generators (`shape` and `one-se` items); the curve features are fixed by the mode.
- **Misconceptions.** `test-error-falls-forever`, `pick-the-minimum-always`, `train-error-falls-with-n`.

#### 6.1.4 `bias-variance-lab`: Bias-variance lab

**Composite · P2 · G1.** Many training sets from one truth: the fan of fits, and the error split into bias, variance and noise.

- **Purpose.** Draw $M$ training sets from the same process and fit the same model to each. At a point $x_0$: bias is how far the average fit misses the truth; variance is how much the fits disagree; and $E[(Y - \hat f(x_0))^2] = \sigma^2 + (f(x_0) - E\hat f(x_0))^2 + E[(\hat f(x_0) - E\hat f(x_0))^2]$. Rigid models miss consistently; flexible ones disagree. Averaged over $x$ and swept over flexibility, the stacked parts add up to the test-error curve. With a fixed design and Gaussian noise, every linear smoother $\hat f(x_0) = \ell(x_0)^\top y$ has exact theory: $E\hat f(x_0) = \ell(x_0)^\top f$ and $\mathrm{Var}\,\hat f(x_0) = \sigma^2\lVert\ell(x_0)\rVert^2$. The widget shows theory and simulation side by side.
- **Serves.** 2.1.1 L5, L6; 2.1.5 L5 (tree model, simulation only); 2.1.4 L1 (shrinkage trades bias for variance); 2.1.10 L6 (viva preparation).
- **Uses.** `plot-2d` (fits and an inset histogram anchored at $x_0$), `marks` (`curve` bundle, `hist`, stacked `bars`, `band`), `drag-point` ($x_0$ along the axis), `slider` (flexibility, $\sigma$, $n$, $M$), `sim-runner` (`resample-fit`), `error-curves` (integrated mode), `derivation-steps`, `value-table`.
- **Interactions.**
  - Pointer: tap "Draw 50 training sets"; drag $x_0$; slide flexibility and watch the fan narrow or widen; toggle theory; switch to integrated mode.
  - Keyboard: $x_0$ is a slider along the axis; sliders; D draws a batch; T opens the table of fits at $x_0$.
- **State.** `{ model: ModelSpec; x0: number; M: number; seed: number; mode: 'pointwise' | 'integrated' | 'estimator'; theory: boolean }`.
- **Answers and checks.** `ordering` (rank shown models by variance or squared bias at $x_0$, from exact theory), `numeric` (bias, variance and mean squared error from a fixed table of 20 fitted values shown on screen; variance uses divisor $M$, stated), `expression` and `derivation-steps` lines (the decomposition), `choice`.
- **Config.**

```ts
interface BiasVarianceLabConfig {
  data: Extract<DataSpec, { gen: 'dataset-gen@1/regression-1d' }> & { design: 'grid' | 'fixed-random' | 'random' };
  models: ModelSpec[];                     // poly degree, knn k, ridge lambda, tree depth
  mode: 'pointwise' | 'integrated' | 'estimator';
  x0?: number; M: number;
  show: ('truth' | 'fits' | 'average' | 'hist' | 'bars' | 'theory')[];
  tableOfFits?: number;                    // fixed fits listed for numeric items (default 20)
}
```

- **Visual.** Truth `--s3`; individual fits `--s2` at 15% opacity (at most 30 drawn); the average fit `--s6` dashed; the $x_0$ handle `--manip` with a vertical guide; the inset histogram of $\hat f(x_0)$ in `--s2` with the theoretical normal in `--s3`; decomposition bars stacked: $\text{bias}^2$ `--s6`, variance `--s2`, $\sigma^2$ ink hatched, each labelled with its value. Answer objects: fields and ordered cards.
- **Motion.** Fits arrive in batches (data arriving). Show-why keys: `fan-out` (highlights the spread at $x_0$ and labels it "variance"); `average-misses` (draws the gap between the average fit and the truth and labels it "bias").
- **Reduced motion.** Batches appear complete.
- **Accessibility.** Table at $x_0$: fit index and $\hat f(x_0)$, then mean, bias and variance. "Degree 1: bias squared 0.30, variance 0.01 at x0 = 0.8. Degree 9: bias squared 0.00, variance 0.42."
- **Tutor hooks.** Ids: `handle:x0`, `curve:truth`, `curve:average`, `fits`, `hist:x0`, `bar:bias2`, `bar:variance`, `bar:noise`, `slider:<param>`. Secret: none beyond the generator.
- **Performance.** For linear smoothers the $n \times n$ smoother matrix is built once per model; each draw's fit is one matrix-vector product, so 200 draws on $n = 50$ cost about 0.5M operations. Tree models refit per draw in the worker (200 trees, about 50 ms [unverified]).
- **Artifact and web.** No difference.
- **Generators.** `rank-variance`, `rank-bias` (exact theory, distinct by at least 20%), `table-compute` (bias and variance from a shown table), `decompose` (fill one term of the identity). Difficulty 2 to 4.
- **Misconceptions.** `bias-means-unfair`, `variance-is-the-noise`, `flexible-models-have-low-variance`, `more-data-cures-bias`.

### 6.2 Linear and logistic models, classification and features

#### 6.2.1 `logistic-lab`: Logistic lab

**Composite · P2 · G1.** Fit a sigmoid by hand, read it as log-odds, score it by likelihood, and grow it into softmax and a neuron.

- **Purpose.** Logistic regression models $p(x) = \sigma(wx + b) = \frac{1}{1 + e^{-(wx + b)}}$, so the log-odds $\ln\frac{p}{1 - p} = wx + b$ are linear and each unit of $x$ multiplies the odds by $e^w$. The learner fits it by dragging the midpoint ($x = -b/w$, where $p = 0.5$) and the 73% point ($x = (1 - b)/w$, where $wx + b = 1$), reading the log-likelihood $\ell = \sum_i y_i \ln p_i + (1 - y_i)\ln(1 - p_i)$. Per-point log-loss bars show why a confident wrong answer costs so much ($-\ln 0.01 \approx 4.6$). Perfectly separated data have no maximum: the likelihood keeps rising as the curve steepens, until an L2 penalty restores a finite optimum. Softmax mode generalises to $K$ classes with temperature; neuron mode redraws the same unit as the building block of 2.1.6.
- **Serves.** 2.1.2 L4, L5, L10; 2.1.6 L1; 2.1.8 L8 (the secondary model in meta-labelling).
- **Uses.** `plot-2d` (data rows at 0 and 1 with jitter, the curve, log-odds axis, a 2D plane), `drag-point` (midpoint and 73% handles; in 2D a weight-vector arrow and an offset handle), `marks` (`curve`, per-point bars, `field`, `boundary`), `slider` (L2 strength, temperature, logits), `mass-editor` (read-only softmax output), `surface-explorer` (the loss over $(w, b)$, extension), `descent-lab` (link), `node-link` (neuron mode), `live-formula`.
- **Interactions.**
  - Pointer: drag the two handles; toggle the $y$ axis between probability and log-odds; open the loss surface and drag the $(w, b)$ point on it; in 2D drag the weight arrow (it stays normal to the boundary) and the offset; in softmax mode drag each logit bar and the temperature slider.
  - Keyboard: handles move along their constraints (calc-linalg map); E opens exact entry for $w$ and $b$; sliders; L toggles log-odds.
- **State.** `{ w: number | number[]; b: number; mode: '1d' | 'log-odds' | 'loss' | '2d' | 'softmax' | 'neuron'; l2: number; logits?: number[]; temperature?: number }`.
- **Answers and checks.** `point` with predicate `loglik-within` ($\delta = 0.5$ nats by default), `numeric` ($p$ at $x$; one point's log loss; the odds ratio $e^w$; a softmax probability; a cross-entropy), `choice` (what happens under separation; how temperature changes the output), `expression` (the log-odds form).
- **Config.**

```ts
interface LogisticLabConfig {
  mode: '1d' | 'log-odds' | 'loss' | '2d' | 'softmax' | 'neuron';
  data?: { x: number[] | number[][]; y: (0 | 1)[] } | { gen: 'dataset-gen@1/classes-2d' | 'logistic-1d'; w: number | number[]; b: number; n: number; seed: number };
  init?: { w: number | number[]; b: number };
  editable: ('w' | 'b' | 'l2' | 'logits' | 'temperature')[];
  show: ('loglik' | 'bars' | 'mle-after-check' | 'odds' | 'surface')[];
  softmax?: { classes: string[]; logits: number[]; trueClass?: number };
}
```

- **Visual.** Class 0 points as `--s2` circles on the lower row, class 1 as `--s3` triangles on the upper row; the learner's curve and handles `--manip`; the maximum-likelihood curve as a dashed `--s2` ghost after Check; per-point log-loss bars hang from each point in `--s2` at 40%, with the largest labelled; in log-odds view the straight line in `--manip`; in 2D the probability `field` with the boundary in ink. Answer objects: the learner's curve and its handles.
- **Motion.** Direct. Show-why keys: `log-loss-explodes` (a confidently wrong point's bar grows as the curve passes it, labelled $-\ln p$); `separation` (the curve steepens step by step while the log-likelihood readout climbs towards 0 with no maximum).
- **Reduced motion.** Before-and-after pairs.
- **Accessibility.** Table of $x$, $y$, $p(x)$ and log loss. "Midpoint at x = 1.2, slope at midpoint 0.6 per unit (w = 2.4). Log-likelihood −8.31; the maximum is −7.95."
- **Tutor hooks.** Ids: `handle:mid`, `handle:73`, `curve:learner`, `curve:mle`, `bar:<i>`, `point:<i>`, `vec:w`, `handle:offset`, `logit:<k>`, `slider:temperature`, `slider:l2`, `readout:loglik`. Secret: the true $(w, b)$ of generated data and the MLE.
- **Performance.** Newton's method converges in under 25 iterations on 500 points (about 0.2 ms); the likelihood surface is a 64 × 64 `field` over $(w, b)$, recomputed only when the data change.
- **Artifact and web.** No difference. The drill (logistic regression by gradient descent in NumPy, then compared with scikit-learn) has an implement-it part and a web-only comparison.
- **Generators.** `p-at-x`, `odds-ratio`, `log-loss` (exact inputs), `fit-by-hand` (data with a well-defined MLE; generator rejects separable data unless separation is the point), `softmax` (tidy logits). Difficulty 1 to 3.
- **Misconceptions.** `probability-linear-in-x`, `squared-loss-for-probabilities`, `separable-is-easy`, `softmax-is-argmax`.

#### 6.2.2 `classifier-plane`: Classifier plane

**Composite · P2 · G1 (tree, forest, boosting and network models arrive in G2 and G3).** Two-dimensional classification with every model in the course, drawn as decision regions.

- **Purpose.** One plane, many models, so the learner sees what each assumes. k-NN carves local cells; logistic regression draws a line (or a curve with polynomial features); LDA's shared covariance gives a line and QDA's separate covariances a conic; naive Bayes ignores correlation within a class; a linear SVM maximises the margin and depends only on its support vectors; an RBF kernel bends the boundary; trees cut in steps; forests and boosting smooth the steps; a small network bends freely. Where the data come from known densities, the Bayes-optimal boundary is drawn for comparison. Predict mode asks the learner to paint the region a model will draw before it is shown.
- **Serves.** 2.1.2 L6, L11; 2.1.1 L3 (classification variant); 2.1.5 L5, L7 (forest boundaries); 2.1.6 L2 (link); 2.1.3 L1 (split variance, optional).
- **Uses.** `plot-2d`, `marks` (`scatter` with shapes and hollow held-out points, `field`, `boundary`, margin lines, rings), `drag-point` (data points), `region-select` (paint mode), `sketch-pad` (boundary sketch), `slider` (hyperparameters), `choice` (model chips), `sim-runner` (`train` jobs).
- **Interactions.**
  - Pointer: tap empty canvas to add a point of the selected class; drag points; long-press or drag off the canvas to delete; choose a model and slide its hyperparameters; toggle probabilities, the Bayes boundary, held-out points and margins; in predict mode paint cells with the selected class, then Check.
  - Keyboard: points are 2D handles in a roving group; A adds a point at a crosshair moved by the arrow keys; Delete removes the focused point; C cycles the class of the next point; chips and sliders; paint mode uses `region-select`'s grid keys.
- **State.** `{ points: { x: number; y: number; c: number; held: boolean }[]; model: ModelSpec; overlays: string[]; painted?: number[] }`.
- **Answers and checks.** Predicate `region-agrees` (the painted region agrees with the model on at least 85% of grid cells by default), `set` (the support vectors, from SMO with tolerance $10^{-6}$, on generated separable data with a unique support set; the misclassified held-out points), `numeric` (held-out accuracy from shown points; the $k$-NN vote at a query point by counting), `choice` (which model drew this boundary; generated), predicate `separates` (a learner-drawn line separates the training classes).
- **Config.**

```ts
interface ClassifierPlaneConfig {
  data: Extract<DataSpec, { gen: 'dataset-gen@1/classes-2d' }> | { points: { x: number; y: number; c: number; held?: boolean }[] };
  models: ModelSpec[];                     // knn, logistic(degree, C), lda, qda, nb, svm-linear(C), svm-rbf(C, gamma), tree, forest, boosting, mlp
  mode: 'explore' | 'predict' | 'which-model' | 'svm' | 'separate';
  editable: ('add' | 'move' | 'delete' | 'model' | 'params')[];
  overlays: ('probability' | 'boundary' | 'bayes' | 'margin' | 'support' | 'held-out' | 'errors')[];
  grid: 32 | 48 | 64;
}
```

- **Visual.** Classes as in section 2.6 (circle `--s2`, triangle `--s3`, square `--s6`); held-out points hollow; the decision `field` at low opacity with the boundary 2px ink; the Bayes boundary dashed `--s3` labelled "best possible"; SVM margins dashed ink with support vectors ringed in ink; the painted prediction as a `--manip-wash` overlay with a 1px `--manip` outline. Answer objects: painted cells, tapped points, the learner's line.
- **Motion.** Direct: the field follows point drags at 32 × 32 and refines to 64 × 64 on release. Show-why keys: `nearest-votes` (lines from a query point to its $k$ neighbours, with the vote count); `margin` (the margin width and its two closest points); `bayes-gap` (shades where the model and the Bayes boundary disagree).
- **Reduced motion.** Show-why becomes before-and-after; the field still follows drags (the learner's own motion).
- **Accessibility.** Describe: "QDA on 'circles', 200 points: class A inside a ring of radius 1.1; held-out accuracy 0.93. 3 held-out points misclassified." The table lists points with true class, predicted class and probability. Painting uses the grid's keyboard path.
- **Tutor hooks.** Ids: `point:<i>`, `field`, `boundary`, `boundary:bayes`, `margin`, `sv:<i>`, `chip:<model>`, `slider:<param>`, `cell:<r>,<c>` (paint grid). Secret: the generating densities and the Bayes error.
- **Performance.** Section 2.10 budgets: fields in the worker, 32 × 32 during drags; SMO for at most 500 points; forests capped at 100 trees in this widget.
- **Artifact and web.** No difference.
- **Generators.** `which-model` (boundaries from distinct model families on one data set), `support-vectors` (separable data with a unique support set), `knn-vote` (query points with no tied distances), `paint-region` (data where the model's region is smooth enough that 85% agreement is reachable by reasoning). Difficulty 2 to 4.
- **Misconceptions.** `linear-model-cannot-curve`, `k1-is-best`, `boundary-follows-the-points`, `svm-uses-all-points`.

#### 6.2.3 `threshold-lab`: Threshold lab

**Composite · P2 · G1.** One score, one threshold: the confusion matrix, ROC and precision-recall curves, base rates and costs.

- **Purpose.** A classifier outputs a score; a decision needs a threshold. Dragging it trades false positives for false negatives. Precision $\frac{TP}{TP + FP}$ collapses at low base rates even when the ROC curve does not move, because the ROC's axes (true and false positive rates) condition on the true class. AUC equals the probability that a random positive outscores a random negative, counted by hand on a small pairing grid. With costs, the best threshold is not 0.5: for equal-variance normal scores it is $t^* = \frac{\mu_0 + \mu_1}{2} + \frac{\sigma^2}{\mu_1 - \mu_0}\ln\frac{(1 - \pi)C_{FP}}{\pi C_{FN}}$. In trading terms, a 52% hit rate is valuable when wins and losses are symmetric, and a 60% hit rate can lose money when they are not.
- **Serves.** 2.1.2 L7, L8, L12; 2.1.8 L8 (meta-labelling precision and recall).
- **Uses.** `plot-2d` (score densities or histograms; ROC; PR; expected profit against threshold), `drag-point` (the threshold, axis-constrained), `marks` (`hist`, `curve`, `step`, shaded AUC), `contingency-table` (confusion preset, extension), `icon-array` (imbalance mode, extension), `cell-grid` (pairing grid), `slider` (base rate, separation, costs), `live-formula`.
- **Interactions.**
  - Pointer: drag the threshold; slide the base rate and the separation $d' = \frac{\mu_1 - \mu_0}{\sigma}$; edit the cost matrix or the win and loss sizes; in pairing mode tap each cell of the positives-by-negatives grid as "positive higher", "lower" or "tie".
  - Keyboard: the threshold is a slider over score values (between distinct scores for lists); sliders; the pairing grid is a roving grid with 1, 0 and H for half.
- **State.** `{ threshold: number; baseRate: number; separation?: number; costs?: { fp: number; fn: number }; payoff?: { win: number; loss: number }; pairs?: Record<string, 0 | 0.5 | 1> }`.
- **Answers and checks.** `numeric` (precision, recall, specificity, false positive rate and F1 from counts, as exact rationals; AUC by pair counting; expected profit at a threshold; $t^*$ from the formula), `point` or `interval` (the profit-maximising threshold: exact for parametric scores; for score lists, any threshold in the optimal interval), `choice` (ROC against PR under imbalance), `set`.
- **Config.**

```ts
interface ThresholdLabConfig {
  scores: { kind: 'normal'; mu0: number; mu1: number; sigma: number }
        | { kind: 'lists'; negatives: number[]; positives: number[] }
        | { kind: 'model'; source: string };
  baseRate: number;
  panels: ('densities' | 'confusion' | 'icons' | 'roc' | 'pr' | 'profit' | 'pairs')[];
  costs?: { fp: number; fn: number }; payoff?: { win: number; loss: number };
  editable: ('threshold' | 'baseRate' | 'separation' | 'costs')[];
}
```

- **Visual.** Negatives `--s2` with circles, positives `--s3` with triangles (histogram bars carry the glyph in their label); the threshold a vertical `--manip` line with a handle; the four regions under the densities labelled TP, FP, TN and FN with hatch patterns for the error regions; the ROC and PR curves in ink with the current point `--manip`; AUC shaded `--s3` at 15% with its value; the profit curve `--s2` with its maximum marked after Check. Answer objects: the threshold handle and the fields.
- **Motion.** Direct. Show-why keys: `base-rate` (positives shrink to 1% over 800ms; precision falls while the ROC point stays); `pair-count` (fills the pairing grid cell by cell and averages it).
- **Reduced motion.** Before-and-after.
- **Accessibility.** "Threshold 0.62. TP 42, FP 18, TN 920, FN 20. Precision 0.70, recall 0.68, false positive rate 0.019. AUC 0.91." The table lists thresholds with the four counts.
- **Tutor hooks.** Ids: `handle:threshold`, `region:tp`, `region:fp`, `region:tn`, `region:fn`, `curve:roc`, `curve:pr`, `point:roc`, `point:pr`, `area:auc`, `curve:profit`, `cell:<i>,<j>`, `slider:base-rate`. Secret: the profit-maximising threshold.
- **Performance.** Sorted scores make every metric $O(\log n)$ per threshold move; curves are precomputed; under 1 ms.
- **Artifact and web.** No difference.
- **Generators.** `counts-to-metrics`, `pair-auc` (lists of at most 5 by 5), `bayes-threshold`, `profit-threshold` (unique optimum), `imbalance-precision`. Difficulty 1 to 4.
- **Misconceptions.** `accuracy-is-enough`, `threshold-must-be-half`, `roc-hides-base-rate-so-its-fine`, `auc-measures-calibration`.

#### 6.2.4 `calibration-lab`: Calibration lab

**Composite · P2 · G1 (sizing mode G4).** Are the probabilities honest, how to fix them, and what dishonest probabilities do to bet sizes.

- **Purpose.** A forecast of 70% should come true 70% of the time. The reliability diagram bins forecasts and plots the observed frequency against the mean forecast; over-confident models fall below the diagonal at high forecasts and above it at low ones. The Brier score $\frac{1}{n}\sum(p_i - o_i)^2$ splits into reliability minus resolution plus uncertainty (Murphy). Platt scaling fits a logistic curve to the scores; isotonic regression fits a monotone step function; both must be fitted on a calibration split, never the test set. Sizing mode turns probabilities into positions: López de Prado's size $m = 2\Phi(z) - 1$ with $z = \frac{p - 1/2}{\sqrt{p(1 - p)}}$, or the Kelly fraction $f^* = p - \frac{1 - p}{b}$ for net odds $b$; a 1,000-bet simulation shows over-stated probabilities becoming over-sized bets and deep drawdowns.
- **Serves.** 2.1.2 L9; 2.1.8 L13; cross-cluster 3.3 (betting games, with `game-lab`'s Kelly mode).
- **Uses.** `plot-2d` (reliability diagram with a count histogram below; mapping curve; wealth paths), `marks` (`scatter`, whiskers, `step`, `hist`, `paths`), `sketch-pad` (the distortion curve), `slider` (bins, $p$, $b$), `choice` (method chips), `sim-runner` (`bet-sequence`), `drawdown-lab` (link), `live-formula`.
- **Interactions.**
  - Pointer: drag the distortion curve's control points to make the model over- or under-confident; choose none, Platt or isotonic; slide the bin count; in sizing mode drag $p$ and the odds and run 1,000 bets with the stated and the true probabilities side by side.
  - Keyboard: control points as handles; chips; sliders; R runs.
- **State.** `{ distortion: Vec2[]; method: 'none' | 'platt' | 'isotonic'; bins: number; sizing?: { p: number; b: number; trueP: number; seed: number } }`.
- **Answers and checks.** `numeric` (Brier score of five forecasts; the Kelly fraction; López de Prado's size at $p$; a bin's observed frequency from counts), `choice` (over- or under-confident from a diagram), `curve` (sketch the reliability curve of an over-confident model: below the diagonal above 0.5, above it below 0.5).
- **Config.**

```ts
interface CalibrationLabConfig {
  forecasts: { p: number[]; o: (0 | 1)[] } | { n: number; trueCurve: 'calibrated' | 'over' | 'under' | Vec2[]; seed: number };
  mode: 'diagram' | 'recalibrate' | 'sizing';
  methods: ('none' | 'platt' | 'isotonic')[];
  split?: { calibration: number; test: number };
  sizing?: { p: number; b: number; trueP: number; rule: 'kelly' | 'lopez-de-prado' | 'both' };
}
```

- **Visual.** The diagonal dashed ink labelled "honest"; bin points `--s2` with Wilson whiskers and counts below as grey bars; the distortion curve `--manip` with handles; the Platt curve `--s6` and the isotonic steps `--s4`, labelled; wealth paths: stated-probability sizing `--s2`, true-probability sizing `--s3`, with the drawdown of each shaded. Answer objects: fields and the sketched curve.
- **Motion.** Direct. Show-why keys: `overconfident` (each bin's gap from the diagonal draws as an arrow); `kelly-overbet` (the wealth path at twice the Kelly fraction draws beside the Kelly path).
- **Reduced motion.** Before-and-after.
- **Accessibility.** "10 bins. Forecasts near 0.9 come true 0.74 of the time: over-confident. Brier 0.192 = reliability 0.021 − resolution 0.079 + uncertainty 0.250." Table of bins with counts, mean forecast, observed frequency and interval.
- **Tutor hooks.** Ids: `bin:<k>`, `line:diagonal`, `curve:distortion`, `curve:platt`, `curve:isotonic`, `handle:p`, `path:stated`, `path:true`, `readout:brier`. Secret: the true calibration curve.
- **Performance.** Isotonic fitting by pool-adjacent-violators in $O(n)$; Platt by Newton's method; 1,000 bets times 2 strategies in under 2 ms.
- **Artifact and web.** No difference.
- **Generators.** `brier`, `kelly`, `ldp-size`, `read-diagram` (generated diagrams with a clear direction). Difficulty 2 to 4.
- **Misconceptions.** `high-auc-means-calibrated`, `isotonic-on-test-data`, `bet-more-when-unsure`, `brier-is-accuracy`.

#### 6.2.5 `feature-builder`: Feature builder

**Composite · P2 · G1 (cross-sectional transforms H1).** Turn raw columns into a design matrix, and see the rank, the collinearity and the leaks that encodings create.

- **Purpose.** Models see numbers in columns, not categories or dates. One-hot encoding a 5-level factor with an intercept needs 4 columns; with 5, the columns sum to the intercept and $X^\top X$ is singular (the dummy trap). Interactions give each group its own slope. Transforms carry hidden leaks: a scaler fitted on all rows, a centred rolling mean that uses tomorrow, target encoding computed on the rows it encodes. For panels, cross-sectional transforms (rank or z-score within each date, winsorising) are how quant features are made comparable across stocks.
- **Serves.** 2.1.2 L2; 2.1.8 L2, L3 (link); 2.1.10 L2; 3.1.1 L7 and 3.1.3 L2 (cross-sectional transforms).
- **Uses.** `value-table` (frame mode: the raw and encoded frames side by side), `token-tray` (transform chips dropped onto columns), `matrix` (the design matrix with rank and condition number), `regression-lab` or `logistic-lab` (linked fit), `condition-number` (link), and the programming catalogue's `frame-core` service for the transforms.
- **Interactions.**
  - Pointer: drag a transform chip onto a column (one-hot, drop-first, interaction, power, log1p, standardise, rank-by-date, z-score-by-date, winsorise, lag, rolling mean, difference, target encoding); set its options (fit on train or on all rows; trailing or centred window); tap a derived column to remove it; tap columns flagged as suspect.
  - Keyboard: chips use `token-tray` keys (Space lifts, arrows choose a column, Space drops); options are native controls; the frame is a roving grid.
- **State.** `{ transforms: { id: string; kind: string; column: string | string[]; options: Record<string, unknown> }[]; flagged: string[] }`.
- **Answers and checks.** `table` (predict the encoded rows for three inputs), `numeric` (rank of $X$; number of columns after encoding), `set` (leaky columns, against the generator's planted leaks), `choice`, `code` (a scikit-learn `ColumnTransformer` drill, web-only).
- **Config.**

```ts
interface FeatureBuilderConfig {
  frame: { columns: { name: string; type: 'numeric' | 'category' | 'date' | 'asset' }[]; rows: unknown[][] } | { gen: string; seed: number };
  palette: string[];                       // allowed transform kinds
  split?: { trainRows: number[]; testRows: number[] } | { timeColumn: string; cutoff: string };
  flagLeaks: 'live' | 'after-check' | 'never';
  linkedFit?: 'regression' | 'logistic' | 'ridge-cv' | 'none';
  task: 'encode' | 'predict-rows' | 'find-leaks' | 'explore';
}
```

- **Visual.** Raw columns on `--bg-surface`; derived columns with a header chip naming the transform; the design matrix's rank readout ("rank 5 of 6 columns") with the dependent combination highlighted by the pear focus wash and a + chain ("A + B + C = intercept"); leak flags after Check: the column header hatched with the word "leak" and the reason. Answer objects: flagged columns and predicted cells.
- **Motion.** A transform's new column slides in over 200ms (a consequence). Show-why `dummy-trap`: the three dummy columns add, cell by cell, into a copy of the intercept column.
- **Reduced motion.** Columns appear at once; the sum shows as a static equation.
- **Accessibility.** The frames are real tables. "Encoded 'sector' into 4 columns (drop first). Rank 6 of 6. Linked fit: test MSE 0.84."
- **Tutor hooks.** Ids: `col:<name>`, `chip:<kind>`, `cell:<r>,<c>`, `readout:rank`, `readout:cond`, `combo:dependent`. Secret: the planted leaks.
- **Performance.** At most 2,000 rows by 30 columns; transforms in `frame-core` (rolling and group operations are $O(n)$); the linked ridge with 5-fold CV under 5 ms.
- **Artifact and web.** No difference, except the `ColumnTransformer` drill (web-only).
- **Generators.** `encode-rows`, `count-columns`, `rank` (designs with and without the trap), `find-leaks` (one to three planted leaks from a catalogue with reasons). Difficulty 1 to 4.
- **Misconceptions.** `dummy-for-every-level-with-intercept`, `scale-on-all-data`, `centred-window-is-fine`, `target-encoding-is-free`.

#### 6.2.6 `basis-lab`: Basis lab

**Composite · P2 · G1.** A flexible fit as a weighted sum of simple functions you can see and move.

- **Purpose.** Linear models fit curves by adding columns: powers of $x$, steps, hinges $(x - \xi)_+$, cubic splines with knots $\xi_k$, natural splines (linear beyond the boundary knots), Gaussian bumps, or sines and cosines. The fit is $\hat f(x) = \sum_j \hat\beta_j b_j(x)$, so the learner sees each scaled basis function and their sum. Degrees of freedom count the columns: a cubic spline with $K$ interior knots has $K + 4$ (with the intercept); a natural cubic spline with $K$ knots has $K$ (ESL 5.2.1). Polynomials swing at the edges; natural splines do not. Additive models (GAMs) sum one such function per predictor.
- **Serves.** 2.1.2 L3; 2.1.1 L2 (spline model in `fit-explorer`); 2.1.6 L3 (contrast with learned ReLU features).
- **Uses.** `plot-2d`, `drag-point` (knots on the axis; coefficient handles on each basis function's peak), `marks` (`curve` bundle, `scatter`), `choice` (family chips), `slider` (number of terms, bump width), `fit-explorer` and `error-curves` (links), `live-formula`.
- **Interactions.**
  - Pointer: drag knots along the axis; tap the axis to add a knot (at most 12); drag a knot off the axis to remove it; choose a family; in manual mode drag each basis function's scale handle and watch the sum; tap Fit for least squares.
  - Keyboard: knots are sliders along the axis; Insert adds a knot at the focused position; Delete removes; scale handles are vertical sliders; F fits.
- **State.** `{ family: string; knots: number[]; coefs?: number[]; manual: boolean; width?: number; gam?: { f1: string; f2: string } }`.
- **Answers and checks.** `numeric` (degrees of freedom; the fitted value at $x$ from shown coefficients), predicate `rss-within` or `mse-at-most` (place at most $K$ knots to bring the residual sum of squares near its best), `choice` (behaviour beyond the boundary), `mapping` (basis sets to families).
- **Config.**

```ts
interface BasisLabConfig {
  data: Extract<DataSpec, { gen: 'dataset-gen@1/regression-1d' }> | { x: number[]; y: number[] };
  families: ('poly' | 'step' | 'hinge' | 'cubic-spline' | 'natural-spline' | 'bspline' | 'rbf' | 'fourier')[];
  knots: number[]; maxKnots: number;
  editable: ('knots' | 'family' | 'coefs')[];
  show: ('basis' | 'scaled-basis' | 'sum' | 'df' | 'extrapolation')[];
  gam?: { predictors: [string, string] };
}
```

- **Visual.** Data ink; unscaled basis functions as thin `--text-muted` curves; scaled basis functions in `--s6` at 50%; their sum, the fit, in `--s2` 2.5px; knots as `--manip` diamonds on the axis with dashed verticals; an extrapolation zone beyond the data shaded `--bg-sunken` and labelled. Answer objects: knots and fields.
- **Motion.** Direct: dragging a knot refits on every frame. Show-why keys: `sum-of-parts` (each scaled function lifts into place in turn and the sum builds); `wild-ends` (the polynomial and the natural spline extend into the extrapolation zone together).
- **Reduced motion.** Before-and-after.
- **Accessibility.** "Natural cubic spline, 4 knots at 0.2, 0.4, 0.6, 0.8: 4 degrees of freedom. RSS 3.1." Table of $x$, each basis value and the fit.
- **Tutor hooks.** Ids: `knot:<i>`, `basis:<j>`, `scaled:<j>`, `curve:fit`, `zone:extrapolation`, `chip:<family>`, `readout:df`, `readout:rss`. Secret: the generator's change points.
- **Performance.** At most 16 columns and 200 points: one QR per frame (about 0.05 ms).
- **Artifact and web.** No difference.
- **Generators.** `df-count`, `place-knots` (piecewise truths with known change points; threshold set from the optimum with a 10% margin), `match-family`. Difficulty 2 to 4.
- **Misconceptions.** `more-knots-always-better`, `polynomials-behave-at-edges`, `spline-is-one-polynomial`.

### 6.3 Resampling, model selection and regularisation

#### 6.3.1 `cv-lab`: Cross-validation lab

**Composite · P2 · G1.** Validation sets, k-fold, leave-one-out and nested cross-validation for exchangeable data, plus the feature-selection Trap.

- **Purpose.** A single validation split gives an estimate that moves with the split. k-fold cross-validation rotates the held-out fold and averages: $\mathrm{CV}_{(k)} = \sum_j \frac{n_j}{n}\,\mathrm{MSE}_j$, with a standard error from the fold scores. Leave-one-out for least squares has the shortcut $\mathrm{CV}_{(n)} = \frac{1}{n}\sum_i \left(\frac{y_i - \hat y_i}{1 - h_i}\right)^2$. As $k$ grows, the estimate's bias falls and its variance can rise; 5 or 10 is the usual compromise. Tuning on the same folds you report makes the score optimistic; nested cross-validation tunes inside each outer training set. The Trap (Ambroise and McLachlan 2002): choose the 20 of 500 pure-noise features most correlated with the label on all rows, then cross-validate, and the accuracy looks excellent; choose inside each fold and it falls to chance. This widget is for exchangeable rows; time-ordered data go to `time-cv-lab`.
- **Serves.** 2.1.3 L1 to L4, L6, L10; 2.1.4 L8 (link); 2.1.10 L3 (link).
- **Uses.** `cell-grid` (rows as cells coloured by fold; nested folds as an inner grid), `marks` (fold score bars, a histogram of estimates across repeated partitions), `stepper` (trace mode over folds), `slider` ($k$, repeats), `choice` (scheme chips), `regression-lab` (hat values for the shortcut), `error-curves` (link), `sim-runner` (`train`, repeated partitions).
- **Interactions.**
  - Pointer: tap Auto-assign or drag rows into fold columns by hand; step through the folds; slide $k$; toggle stratification or groups; in nested mode open an outer fold to see its inner folds; in the Trap run "select then CV" and "select inside CV" side by side.
  - Keyboard: the row grid is a roving grid; 1 to 9 assigns the focused row to a fold; N and P step folds; sliders; T opens the score table.
- **State.** `{ scheme: 'split' | 'kfold' | 'loocv' | 'nested' | 'selection-trap'; k: number; assignment: number[]; step: number; stratify: boolean; groups?: number[]; repeats?: number; seed: number }`.
- **Answers and checks.** `numeric` (the CV estimate and its standard error from shown fold errors; one LOOCV term by the shortcut), `set` (the training rows of fold $j$), predicate `folds-valid` (a hand assignment is a valid stratified partition), `ordering` (rank three estimates: tuned and reported on the same folds, nested, and the true test error), `choice`.
- **Config.**

```ts
interface CvLabConfig {
  data: DataSpec;
  model: ModelSpec;
  scheme: 'split' | 'kfold' | 'loocv' | 'nested' | 'selection-trap';
  k: number; kRange?: [number, number];
  stratify?: boolean; groups?: number[];
  tuning?: { param: string; values: number[] };          // nested and tuned-and-reported comparisons
  trap?: { noiseFeatures: number; select: number; n: number };
  task: 'compute' | 'assign' | 'which-rows' | 'rank-estimates' | 'explore';
}
```

- **Visual.** Each row a cell carrying its fold number; in the current split the test fold `--s2` at 30% with "test", the rest `--s6` at 20% with "train"; fold scores as ink bars with the mean dashed and the standard error as a whisker; repeated-partition estimates as a `--s2` histogram with the true test error dashed ink. Answer objects: hand-assigned cells, tapped rows and fields.
- **Motion.** Stepping folds slides the test band to the next fold over 240ms (a consequence of Step). Show-why keys: `peeked-labels` (in the Trap, the selected features' correlations recomputed on training rows only shrink towards zero); `same-folds` (highlights that tuning and reporting used identical cells).
- **Reduced motion.** Bands jump.
- **Accessibility.** "5-fold CV, fold 3 of 5 held out: rows 25 to 36. Fold MSEs 0.92, 1.10, 0.85, 1.31, 0.97; estimate 1.03, standard error 0.08." The row grid has a table view with row, fold and role.
- **Tutor hooks.** Ids: `row:<i>`, `fold:<j>`, `bar:fold-<j>`, `readout:estimate`, `readout:se`, `hist:repeats`, `panel:inner-<j>`, `trap:outside`, `trap:inside`. Secret: the true test error.
- **Performance.** At most 2,000 rows (cells aggregate above 120 shown); the Trap uses $p = 500$, $n = 50$: correlations and five small refits under 5 ms; 50 repeated partitions in the worker.
- **Artifact and web.** No difference. The k-fold splitter drill is implement-it tier.
- **Generators.** `cv-estimate`, `which-rows`, `assign-stratified`, `loocv-shortcut` (data with tidy hat values), `rank-estimates` (gaps of at least 3 percentage points). Difficulty 1 to 4.
- **Misconceptions.** `validation-split-is-stable`, `cv-score-of-tuned-model-is-unbiased`, `select-features-then-cv`, `loocv-is-always-best`.

#### 6.3.2 `tuning-lab`: Tuning lab

**Composite · P2 · G1.** Hyperparameter search on a surface you cannot see: grid against random, a fixed budget, and the winner's curse.

- **Purpose.** With a budget of nine evaluations over two hyperparameters, a 3 by 3 grid tries 3 distinct values of each; random search tries 9 of each, which wins when only one hyperparameter matters (Bergstra and Bengio 2012). Every evaluation is a noisy CV estimate, so the best of $N$ is optimistic: for independent noise of standard deviation $s$ the expected optimism is about $s \cdot E[\max_N Z]$. Nested cross-validation or a locked hold-out removes it.
- **Serves.** 2.1.3 L6, L7; 2.1.5 L10; 2.1.7 L8; 2.1.10 L3.
- **Uses.** `plot-2d` (the search space with log axes and marginal rugs), `marks` (`scatter`, `field` for the revealed surface, `rug`, best-so-far `step`), `region-select` (tap placement on a fine grid), `choice` (strategy chips), `slider` (budget), `sim-runner`.
- **Interactions.**
  - Pointer: choose grid, random or manual; in manual mode tap up to $N$ points to evaluate; slide the budget; reveal the surface; compare the reported best score with its value on a large hold-out.
  - Keyboard: a crosshair moves over the fine grid with arrows; Enter evaluates; chips; slider.
- **State.** `{ strategy: 'grid' | 'random' | 'manual'; budget: number; evaluated: { x: number; y: number; score: number }[]; revealed: boolean; seed: number }`.
- **Answers and checks.** `choice` (which strategy suits a surface with one important axis), `numeric` (distinct values tried per axis; the expected optimism from the formula), predicate `near-optimum` (the best evaluated point is within a stated score of the true optimum, using at most the budget; the surface is deterministic per item, so this grades no random estimate).
- **Config.**

```ts
interface TuningLabConfig {
  surface: { recorded: string }                               // authored: recorded at build time from real models
         | { analytic: 'one-axis' | 'ridge' | 'two-peaks' | 'bowl'; noise: number; seed: number };
  axes: { name: string; range: [number, number]; scale: 'linear' | 'log' }[];
  strategies: ('grid' | 'random' | 'manual')[];
  budget: number;
  show: ('rugs' | 'best-so-far' | 'surface-after' | 'holdout')[];
}
```

- **Visual.** Evaluated points as `--s2` dots sized by score rank; manual taps `--manip` until evaluated; marginal rugs on both axes showing distinct values; the revealed surface as a sequential `field` with the true optimum as a dashed ink cross; best-so-far as an ink step line. Answer objects: tapped points and fields.
- **Motion.** Evaluations appear one by one at 120ms (a consequence of Run). Show-why `projected` collapses the points onto the important axis so the learner counts distinct values.
- **Reduced motion.** Points appear together.
- **Accessibility.** "Random search, 9 evaluations: 9 distinct learning rates, 9 distinct depths. Best CV score 0.71 at (0.03, 6); its hold-out score 0.66."
- **Tutor hooks.** Ids: `point:<i>`, `rug:x`, `rug:y`, `field:surface`, `marker:optimum`, `curve:best-so-far`, `chip:<strategy>`, `slider:budget`. Secret: the surface and its optimum.
- **Performance.** Recorded surfaces are 48 × 48 values shipped with the item (about 9 KB); analytic surfaces evaluate in microseconds. No model is trained at runtime.
- **Artifact and web.** No difference.
- **Generators.** `grid-vs-random` (analytic one-axis surfaces), `optimism` (formula items), `find-optimum` (budgets with a proven reachable margin). Difficulty 2 to 4.
- **Misconceptions.** `grid-search-is-thorough`, `best-cv-score-is-the-expected-score`, `tune-on-test`.

#### 6.3.3 `regularisation-path`: Regularisation path

**Composite · P2 · G1.** Coefficients as the penalty changes: ridge, lasso, elastic net, stepwise, best subset and principal components regression on one canvas.

- **Purpose.** Shrinking coefficients trades a little bias for less variance. Ridge minimises $\lVert y - X\beta \rVert^2 + \lambda\lVert\beta\rVert_2^2$: coefficients glide towards zero and never reach it, and through the SVD each principal direction is shrunk by $\frac{d_j^2}{d_j^2 + \lambda}$, with effective degrees of freedom $\sum_j \frac{d_j^2}{d_j^2 + \lambda}$. The lasso's $\lambda\lVert\beta\rVert_1$ sets coefficients exactly to zero, one by one. Elastic net mixes the two and keeps correlated features together. Forward stepwise and best subset add features discretely and are judged by $C_p$, AIC, BIC and adjusted $R^2$ (ISLP's least-squares forms). PCR keeps the top $m$ components. Penalties only make sense on standardised features; rescaling one feature by 100 changes the lasso's choice. The $\lambda$ cursor is bound to `error-curves`, where $\lambda_{\min}$ and $\lambda_{1\text{se}}$ are read.
- **Serves.** 2.1.3 L8; 2.1.4 L1, L2, L4, L7, L8, L9, L11, L13; 2.1.10 L3.
- **Uses.** `plot-2d` (reversed log $\lambda$ axis), `marks` (`curve` bundle, `bars`, markers), `drag-point` (the $\lambda$ cursor), `slider` (shrink factor, $\alpha$, $m$), `choice` (method chips), `error-curves` (bound), `cv-lab` (fold scores), `pca-lab` (PCR link), `matrix` (singular values), `value-table`, `sim-runner` (bootstrap stability).
- **Interactions.**
  - Pointer: drag the $\lambda$ cursor along the path or the error panel; choose a method; slide $\alpha$; toggle standardisation; rescale one feature; tap "Resample 50 times" for selection frequencies; in stepwise mode step forward one feature at a time.
  - Keyboard: the cursor is a slider over the $\lambda$ grid (Page keys jump a decade); chips; N steps stepwise; S toggles standardisation.
- **State.** `{ method: 'shrink' | 'ridge' | 'lasso' | 'enet' | 'stepwise' | 'subset' | 'pcr'; lambda: number; alpha?: number; shrink?: number; m?: number; step?: number; standardise: boolean; rescaled?: { feature: number; by: number }; revealedTruth: boolean }`.
- **Answers and checks.** `numeric` (1D ridge $\hat\beta = \frac{\sum x_i y_i}{\sum x_i^2 + \lambda}$; degrees of freedom from shown singular values; AIC or BIC from RSS with the stated convention), `point` ($\lambda_{1\text{se}}$ or a shrink factor that beats OLS, margin-checked), `set` (features the lasso keeps at the cursor; the generator keeps every feature at least 2% of a decade from its entry or exit point), `choice`, `ordering`.
- **Config.**

```ts
interface RegularisationPathConfig {
  data: Extract<DataSpec, { gen: 'dataset-gen@1/linear' }> | { X: number[][]; y: number[]; names: string[] };
  methods: ('shrink' | 'ridge' | 'lasso' | 'enet' | 'stepwise' | 'subset' | 'pcr')[];
  lambdaGrid: { min: number; max: number; count: number };
  panels: ('path' | 'bars' | 'errors' | 'svd' | 'criteria' | 'stability')[];
  standardise: 'on' | 'off' | 'toggle';
  truth: 'hidden' | 'after-check' | 'shown';
  cvFolds?: number;
}
```

- **Visual.** Before the truth is revealed every path is ink 1.5px with direct labels on the five largest; afterwards true-signal features are ink 2px and labelled, noise features `--text-muted` 1px; the $\lambda$ cursor a vertical `--manip` line with a handle; coefficient bars at the cursor in ink with sign glyphs; SVD shrink factors as `--s3` bars from 0 to 1; criteria curves `--s2`, `--s4` and `--s6` with labels; selection frequencies as `--s2` bars. Answer objects: the cursor and fields.
- **Motion.** Direct: dragging the cursor moves the bars and the bound error cursor on the same frame. Show-why keys: `shrink-not-zero` (ridge bars approach zero and stop short, labelled with their values); `unit-change` (one feature is multiplied by 100 and its lasso path leaves later); `twin-swap` (stability bars for two correlated features split their selections).
- **Reduced motion.** Before-and-after.
- **Accessibility.** "Lasso at log λ = −1.2: 4 features kept (x1 0.82, x3 −0.40, x7 0.11, x12 0.05). CV MSE 1.21 (standard error 0.06); λ1se is at −0.8." Tables for the path (rows by $\lambda$), bars and criteria.
- **Tutor hooks.** Ids: `cursor:lambda`, `path:<feature>`, `bar:<feature>`, `svd:<j>`, `curve:cp`, `curve:aic`, `curve:bic`, `curve:adjr2`, `freq:<feature>`, `toggle:standardise`, `chip:<method>`. Secret: the true coefficients.
- **Performance.** Section 2.10: the lasso and elastic-net paths by coordinate descent on a precomputed Gram matrix with warm starts; the lasso path is piecewise linear in $\lambda$, so the cursor interpolates in $\lambda$ between grid points; ridge evaluates in closed form from the SVD per frame ($O(p^2)$); best subset enumerates up to $2^{12}$ subsets in the worker.
- **Artifact and web.** No difference. The coordinate-descent lasso drill is implement-it tier; the `LassoCV` comparison is web-only.
- **Generators.** `ridge-1d`, `ridge-df`, `lasso-active-set`, `lambda-1se` (unique with margin), `criteria` (AIC and BIC from RSS), `stepwise-next` (the next feature to enter, unique). Difficulty 2 to 5.
- **Misconceptions.** `ridge-sets-coefficients-to-zero`, `lasso-picks-the-true-feature`, `no-need-to-standardise`, `lambda-from-test-set`, `stepwise-p-values-are-valid`.

#### 6.3.4 `penalty-geometry`: Penalty geometry

**Composite · P2 · G1.** Why the lasso gives zeros: error ellipses meeting a disc, a diamond and an elastic-net ball, and the matching threshold functions in one dimension.

- **Purpose.** With two coefficients, the residual sum of squares has elliptical contours centred at the OLS estimate, shaped by $X^\top X$. The constrained problem ($\lVert\beta\rVert \le t$) is solved where the smallest ellipse touches the budget region. A disc is touched anywhere, so ridge solutions are rarely zero; a diamond is usually touched at a corner, so lasso solutions often sit on an axis. Each budget $t$ matches a penalty $\lambda$. In an orthonormal design the three classic estimators are explicit functions of the OLS estimate $z$: ridge $\frac{z}{1 + \lambda}$; lasso $\operatorname{sign}(z)(\lvert z \rvert - \lambda)_+$ (soft threshold); best subset $z \cdot \mathbb{1}[\lvert z \rvert > \sqrt{2\lambda}]$ (hard threshold), for the loss $\frac{1}{2}\lVert y - X\beta \rVert^2$.
- **Serves.** 2.1.4 L3, L5, L6, L9, L10.
- **Uses.** `plot-2d` (weight-space preset), `marks` (ellipse contours, `norm-ball`, solution path, threshold `curve`s), `drag-point` (OLS centre; the learner's predicted solution, constrained to the ball's boundary), `slider` ($t$ or $\lambda$, correlation $\rho$, $\alpha$), `choice` (penalty chips), `card-sort` (threshold matching), `posterior-lab` (MAP link).
- **Interactions.**
  - Pointer: drag the OLS centre; slide the budget and the feature correlation (which tilts and stretches the ellipses); choose L2, L1, elastic net, $L_{0.5}$ or $L_0$; in predict mode drag a marker round the ball's boundary to where you expect contact, then Check; in 1D mode drag $z$ and $\lambda$.
  - Keyboard: handles (the boundary marker moves along the boundary with Left and Right); sliders; chips.
- **State.** `{ ols: Vec2; rho: number; penalty: 'l2' | 'l1' | 'enet' | 'lq' | 'l0'; t: number; alpha?: number; guess?: Vec2; mode: '2d' | '1d'; z?: number; lambda?: number }`.
- **Answers and checks.** `point` (the constrained solution, Euclidean tolerance), predicate `on-corner` (for lasso items whose solution has a zero coordinate), `numeric` ($S(z, \lambda)$; ridge shrinkage; the hard-threshold cut-off $\sqrt{2\lambda}$), `mapping` (threshold functions to penalties), `choice`.
- **Config.**

```ts
interface PenaltyGeometryConfig {
  mode: '2d' | '1d';
  ols: Vec2; gram?: [[number, number], [number, number]] | { rho: number };
  penalties: ('l2' | 'l1' | 'enet' | 'lq' | 'l0')[];
  budget: { t: number; range: [number, number] } | { lambda: number; range: [number, number] };
  movable: ('ols' | 'rho' | 'budget' | 'guess')[];
  show: ('contours' | 'path' | 'solution-after-check' | 'prior')[];
}
```

- **Visual.** Contours 1px ink, the touching contour 2px; the ball `--s3` at 20% with a 2px `--s3` edge; the OLS centre ink with a label; the solution `--s2` dot; the learner's guess `--manip`; the solution path as $t$ grows `--s2` 1.5px from the origin to the OLS point; in 1D the three threshold functions `--s2`, `--s3` and `--s6` with the identity line dashed ink. Answer objects: the guess marker and fields.
- **Motion.** Direct: contours, ball and solution redraw per frame. Show-why keys: `corner-contact` (the contours inflate from the centre until the first touch, which lands on a corner, over 800ms); `ridge-misses-zero` (the same inflation against the disc).
- **Reduced motion.** Before-and-after.
- **Accessibility.** "OLS at (2.0, 0.6), correlation 0.5. Lasso budget 1.5: solution (1.5, 0.0), on the β1 axis. Your guess (1.4, 0.1), 0.14 away."
- **Tutor hooks.** Ids: `handle:ols`, `ball`, `contour:touch`, `point:solution`, `handle:guess`, `path:solution`, `slider:t`, `slider:rho`, `curve:ridge`, `curve:lasso`, `curve:subset`. Secret: the solution while hidden.
- **Performance.** Exact solutions: for the disc, a one-dimensional root find on the ridge multiplier; for the diamond, the KKT conditions on 4 edges and 4 corners; contours as exact ellipses from the 2 by 2 Gram matrix (no contouring). Under 0.2 ms per frame.
- **Artifact and web.** No difference.
- **Generators.** `predict-contact` (cases on and off corners), `soft-threshold`, `match-thresholds`, `budget-to-lambda`. Difficulty 2 to 4.
- **Misconceptions.** `ridge-sets-coefficients-to-zero`, `lasso-shrinks-proportionally`, `constraint-and-penalty-differ`.

### 6.4 Trees, ensembles and clustering

#### 6.4.1 `split-scorer`: Split scorer

**Composite · P2 · G2.** One node, one feature, one threshold: the impurity arithmetic every tree repeats.

- **Purpose.** A tree grows by choosing, at each node, the feature and threshold that most reduce impurity. For class shares $p_k$: Gini $1 - \sum_k p_k^2$, entropy $-\sum_k p_k \log_2 p_k$, misclassification $1 - \max_k p_k$. A split's score is the parent's impurity minus the size-weighted children's, $\frac{n_L}{n}I_L + \frac{n_R}{n}I_R$. Regression trees use the residual sum of squares about each child's mean. Thresholds sit at midpoints between consecutive distinct values, as scikit-learn places them. The concavity panel shows why misclassification error is a poor growing criterion: from a (400, 400) node, the splits (300, 100) and (100, 300) against (200, 400) and (200, 0) have equal error, 0.25, but Gini and entropy prefer the second, which makes a pure node (ESL 9.2.3). Gain mode shows the second-order score used by XGBoost and LightGBM: $\frac{1}{2}\left[\frac{G_L^2}{H_L + \lambda} + \frac{G_R^2}{H_R + \lambda} - \frac{(G_L + G_R)^2}{H_L + H_R + \lambda}\right] - \gamma$, with leaf weight $-\frac{G}{H + \lambda}$.
- **Serves.** 2.1.5 L2, L3, L10; inside `tree-builder` and `boosting-lab`.
- **Uses.** `plot-2d` (one strip per feature with class glyphs or $y$ values; the score against threshold; the impurity-against-$p$ panel), `drag-point` (the threshold, snapping to midpoints), `marks` (`scatter`, `curve`, `bars` for child counts), `choice` (criterion chips), `live-formula` (the arithmetic with this node's counts substituted).
- **Interactions.**
  - Pointer: drag the threshold along a feature strip; tap another strip to switch feature; choose the criterion; reveal the score curve (hidden in predict mode); in gain mode slide $\lambda$ and $\gamma$.
  - Keyboard: the threshold is a slider over candidate midpoints; Up and Down change feature; chips; R reveals when allowed.
- **State.** `{ feature: number; threshold: number; criterion: 'gini' | 'entropy' | 'error' | 'rss' | 'gain'; lambda?: number; gamma?: number; revealed: boolean }`.
- **Answers and checks.** `numeric` (a node's Gini or entropy from counts, exact rationals for Gini; weighted child impurity; the gain; a leaf weight), `interval` (the best threshold: any value between the two data points around the optimal cut), `choice` (which feature to split; which criterion prefers which split).
- **Config.**

```ts
interface SplitScorerConfig {
  node: { features: { name: string; values: number[] }[]; y: number[]; task: 'class' | 'regression' }
      | { counts: { left: number[]; right: number[] }[] }          // arithmetic-only items
      | { gradients: { g: number[]; h: number[] }; values: number[] };   // gain mode
  criteria: ('gini' | 'entropy' | 'error' | 'rss' | 'gain')[];
  predict: boolean;                        // hide the score curve until Check
  show: ('counts' | 'formula' | 'score-curve' | 'concavity')[];
}
```

- **Visual.** Class glyphs as in section 2.6 along each strip; the threshold `--manip` with a handle; child count bars below each side; the score curve `--s2` with its maximum marked after Check; the concavity panel with Gini, entropy and error as `--s2`, `--s6` and `--s4` labelled curves and two splits drawn as chords. Answer objects: the threshold handle and fields.
- **Motion.** Direct. Show-why `chord`: the two candidate splits' children drop onto the concavity panel as points joined by chords, showing the weighted average below the curve for Gini and on the line for error.
- **Reduced motion.** Static chords.
- **Accessibility.** "x2 at 3.45: left 12 (10 A, 2 B), right 18 (3 A, 15 B). Gini parent 0.499, children weighted 0.271, gain 0.228." Table of thresholds and scores.
- **Tutor hooks.** Ids: `handle:threshold`, `strip:<feature>`, `bar:left`, `bar:right`, `curve:score`, `marker:best`, `panel:concavity`, `chip:<criterion>`. Secret: the best split.
- **Performance.** Sorted values make every threshold an $O(1)$ update from running counts; the full score curve in $O(n)$ per feature.
- **Artifact and web.** No difference. The Gini split-search drill is implement-it tier.
- **Generators.** `gini-node`, `entropy-node`, `split-gain`, `best-threshold` (unique optimum), `criterion-prefers` (ESL-style pairs), `xgb-gain`. Difficulty 1 to 4.
- **Misconceptions.** `misclassification-error-for-splitting`, `split-at-a-data-value`, `gini-is-error-rate`.

#### 6.4.2 `tree-builder`: Tree builder

**Composite · P2 · G2.** Grow a decision tree by hand or greedily, prune it, and watch it change when the data are resampled.

- **Purpose.** A tree partitions the plane into boxes and predicts the majority class (or mean) in each. The learner splits boxes by hand, guided by `split-scorer`, and the diagram grows beside the plot with counts and impurity at each node. Greedy growth to depth $d$ fits the training data ever better; cost-complexity pruning minimises $R_\alpha(T) = R(T) + \alpha\lvert T \rvert$ and folds leaves as $\alpha$ rises, tracing a nested sequence of subtrees. Resampling the data regrows a very different tree: high variance, which bagging will exploit.
- **Serves.** 2.1.5 L1, L3, L4, L5; 2.1.5 L6 (single trees inside `ensemble-lab`).
- **Uses.** `plot-2d`, `marks` (`partition` boxes linked to leaves, `scatter`, 1D `step` fits), `node-link` (tidy tree linked to boxes), `split-scorer` (embedded for the selected box), `drag-point` (a split line inside the selected box, vertical or horizontal), `slider` (depth, minimum leaf size, $\alpha$), `stepper` (trace mode over greedy steps), `error-curves` (leaves against error), `sim-runner` (`train`, resample).
- **Interactions.**
  - Pointer: tap a box (or its node) to select it; drag a split line inside it, choosing the axis with a toggle; tap Split; tap a node to undo its subtree; in auto mode slide depth and $\alpha$; tap Resample; in trace mode tap the nodes a query point visits.
  - Keyboard: boxes and nodes form one roving group (the tree order); V and H choose the split axis; the split line is a slider; Enter splits; Backspace collapses a node; sliders; R resamples.
- **State.** `{ nodes: { id: string; parent?: string; feature?: number; threshold?: number }[]; selected?: string; depth?: number; alpha?: number; minLeaf?: number; seed: number; mode: 'hand' | 'auto' | 'prune' | 'resample' | 'trace'; path?: string[] }`.
- **Answers and checks.** Predicates `accuracy-at-least` and `tree-size-at-most` together (a tree of at most 4 leaves reaching a stated training accuracy, feasible by construction), `numeric` (a leaf's prediction; a node's impurity; leaves after pruning at $\alpha$), `ordering` (the nodes a query point visits), `set` (the points in a leaf), `choice`.
- **Config.**

```ts
interface TreeBuilderConfig {
  data: Extract<DataSpec, { gen: 'dataset-gen@1/classes-2d' | 'dataset-gen@1/regression-1d' }> | { points: { x: number[]; y: number }[] };
  mode: 'hand' | 'auto' | 'prune' | 'resample' | 'trace' | 'explore';
  criterion: 'gini' | 'entropy' | 'rss';
  limits?: { maxLeaves?: number; maxDepth?: number; minLeaf?: number };
  show: ('boxes' | 'tree' | 'scorer' | 'held-out' | 'errors' | 'overlay-previous')[];
  query?: number[];                        // trace mode
}
```

- **Visual.** Boxes as `partition` outlines in ink with a 12% wash of the leaf's majority class hue and its glyph; the selected box outlined `--manip`; the split line `--manip`; the tree as lipped node chips (feature, threshold, counts) with edges labelled "≤" and ">"; in resample mode the previous trees' boundaries as faint dashed `--s6` lines. Answer objects: the learner's splits (as lines and nodes) and tapped nodes.
- **Motion.** A new split draws its line and grows two child nodes over 240ms (a consequence of Split). Show-why keys: `prune-fold` (leaves fold into their parent in order of weakest link as $\alpha$ tweens); `instability` (two resampled trees cross-fade with their boundaries overlaid).
- **Reduced motion.** Splits and folds are instant; resamples show side by side.
- **Accessibility.** The tree is a nested list with counts and impurity at each node; boxes are named by their bounds ("x1 ≤ 0.42 and x2 > 1.3: 14 points, 13 A"). "Depth 3, 6 leaves; training accuracy 0.91, held-out 0.78."
- **Tutor hooks.** Ids: `node:<id>`, `leaf:<id>`, `box:<id>`, `line:split`, `toggle:axis`, `slider:depth`, `slider:alpha`, `panel:scorer`. Secret: the generator's true boundary and held-out labels while gated.
- **Performance.** Exact greedy splits: $O(p\,n\log n)$ per level from presorted features; $n \le 1{,}000$ and depth $\le 10$ grow in under 5 ms in the worker; the whole pruning sequence by weakest-link in under 2 ms; at most 256 boxes in SVG.
- **Artifact and web.** No difference.
- **Generators.** `build-small-tree` (data separable by 3 to 4 axis-aligned cuts), `leaf-predict`, `prune-count`, `trace-path`. Difficulty 1 to 4.
- **Misconceptions.** `deeper-tree-is-better`, `trees-are-stable`, `tree-splits-diagonally`.

#### 6.4.3 `ensemble-lab`: Ensemble lab

**Composite · P2 · G2.** Bagging and random forests: average many unstable trees and watch the variance fall.

- **Purpose.** Averaging $B$ identically distributed predictions with variance $\sigma^2$ and pairwise correlation $\rho$ gives variance $\rho\sigma^2 + \frac{1 - \rho}{B}\sigma^2$: more trees remove the second term, never the first. Bagging fits each tree to a bootstrap sample; each row is left out of a given sample with probability $(1 - \frac{1}{n})^n \approx e^{-1} \approx 0.368$, so out-of-bag predictions give a free validation estimate. Random forests also sample the features tried at each split (mtry), which lowers $\rho$ and with it the floor. Adding trees does not overfit a random forest; the error curve flattens. Extra trees randomise thresholds as well.
- **Serves.** 2.1.5 L6, L7, L15; 2.1.3 L9 (OOB link).
- **Uses.** `plot-2d` (1D regression fits or a 2D vote-share `field`), `marks` (faint individual fits, the ensemble mean, `field`, OOB error `curve`), `slider` ($B$, mtry, depth, minimum leaf), `choice` (bagging, forest, extra trees), `sim-runner` (`train` with streaming trees), `error-curves` (error against $B$), `tree-builder` (open one tree), `live-formula` (the variance formula with sliders for $\rho$, $\sigma^2$ and $B$).
- **Interactions.**
  - Pointer: slide $B$ from 1 to 500 (trees stream in); slide mtry and compare curves for mtry $= p$ and $\sqrt{p}$; tap a faint member to open it in `tree-builder`; in formula mode slide $\rho$, $\sigma^2$ and $B$ and compare with the measured variance and correlation.
  - Keyboard: sliders; chips; O opens the focused member.
- **State.** `{ method: 'bagging' | 'forest' | 'extra'; B: number; mtry: number; depth?: number; minLeaf?: number; seed: number; formula?: { rho: number; sigma2: number; B: number } }`.
- **Answers and checks.** `numeric` (the variance formula; its limit $\rho\sigma^2$; the OOB probability), `choice` (why forests beat bagging; what more trees do), `ordering` (rank three settings by OOB error from a fixed table).
- **Config.**

```ts
interface EnsembleLabConfig {
  data: DataSpec;
  methods: ('bagging' | 'forest' | 'extra')[];
  B: { max: number; init: number }; mtry?: number[]; depth?: number; minLeaf?: number;
  show: ('members' | 'mean' | 'field' | 'oob-curve' | 'test-curve' | 'rho' | 'formula')[];
}
```

- **Visual.** Members `--s2` at 12% (first 20 drawn); the ensemble mean `--s2` 2.5px; the truth `--s3`; in 2D the vote share as a `field`; OOB error `--s2` against $B$, test error `--s4` with labels; the measured $\rho$ and the theory floor $\rho\sigma^2$ as a dashed ink line. Answer objects: fields and cards.
- **Motion.** Trees stream in (data arriving). Show-why `floor`: as $B$ tweens to 500 the variance falls onto the dashed $\rho\sigma^2$ line and stays there.
- **Reduced motion.** The final state appears.
- **Accessibility.** "Random forest, 200 trees, mtry 3 of 10: OOB error 0.142, test error 0.150; mean pairwise correlation of tree predictions 0.31."
- **Tutor hooks.** Ids: `member:<i>`, `curve:mean`, `field`, `curve:oob`, `curve:test`, `line:floor`, `slider:B`, `slider:mtry`, `formula:var`. Secret: the true function.
- **Performance.** Section 2.10: 500 trees on 500 rows in about 400 ms, streamed 10 at a time; the field from at most 100 members; $\rho$ estimated on 200 held-out points.
- **Artifact and web.** No difference.
- **Generators.** `variance-formula`, `oob-probability`, `rank-settings`. Difficulty 2 to 4.
- **Misconceptions.** `bagging-reduces-bias`, `more-trees-overfit`, `oob-needs-a-holdout`.

#### 6.4.4 `boosting-lab`: Boosting lab

**Composite · P2 · G2.** Fit what is left: stumps on residuals, the learning rate, early stopping, log-loss pseudo-residuals and AdaBoost's weights.

- **Purpose.** Gradient boosting builds $F_m = F_{m-1} + \nu h_m$, where $h_m$ is a small tree fitted to the negative gradient of the loss: the residuals $y - F_{m-1}$ for squared loss, and $y - p$ for log loss with $p = \sigma(F)$. In predict mode the learner drags each round's stump onto the residual plot before the algorithm reveals its own. A small learning rate $\nu$ needs more rounds and usually generalises better; too many rounds overfit, which the validation curve catches. AdaBoost.M1 reweights misclassified points by $e^{\alpha_m}$ with $\alpha_m = \ln\frac{1 - \text{err}_m}{\text{err}_m}$ (ESL algorithm 10.1).
- **Serves.** 2.1.5 L8, L9, L11; 2.1.5 L10 (gain link).
- **Uses.** `plot-2d` (data and fit above, residuals below, sharing $x$), `marks` (`scatter`, `step` fits, residual stems, point size by weight), `drag-point` (the stump's split and its two leaf values on the residual panel), `split-scorer` (gain mode link), `slider` ($\nu$, rounds, depth, subsample), `stepper` (trace mode over rounds), `error-curves` (rounds), `classifier-plane` (2D field for classification), `sim-runner` (`train`).
- **Interactions.**
  - Pointer: in predict mode drag the stump's split and leaf levels onto the residuals, then Check; then tap Add to apply $\nu$ times the best stump; scrub rounds; slide $\nu$ and depth; mark the early-stopping round on the validation curve; switch to log loss or AdaBoost.
  - Keyboard: the split and leaf handles are sliders; Enter checks; A adds the round; the stepper's Left and Right scrub rounds; sliders.
- **State.** `{ loss: 'squared' | 'log' | 'adaboost'; nu: number; depth: number; round: number; guess?: { split: number; left: number; right: number }; subsample?: number; seed: number }`.
- **Answers and checks.** Predicate `stump-near-best` (the guessed stump's RSS reduction within 10% of the best stump's), `numeric` (a residual after round 1; AdaBoost's $\alpha_m$ and one weight update; the fit at $x$ after two rounds), `expression` (the pseudo-residual for a named loss), `point` (the early-stopping round, margin-checked), `choice` (the effect of a smaller $\nu$).
- **Config.**

```ts
interface BoostingLabConfig {
  data: DataSpec;
  loss: 'squared' | 'log' | 'adaboost';
  nu: number; depth: 1 | 2 | 3; rounds: number;
  mode: 'predict' | 'run' | 'early-stop' | 'explore';
  show: ('fit' | 'residuals' | 'stump' | 'weights' | 'errors' | 'field')[];
}
```

- **Visual.** Data ink; the current fit `--s2` as a step function; residual stems `--text-muted`; the learner's stump `--manip` (a split line and two level bars); the algorithm's stump dashed `--s6` after Check; in AdaBoost point radius grows with weight; validation error `--s2`, training error `--s6` dashed. Answer objects: the guessed stump and fields.
- **Motion.** Add drops the stump from the residual panel into the fit, scaled by $\nu$, over 400ms (a consequence). Show-why keys: `residual-shrink` (residual stems shorten where the stump fits); `overshoot` (with $\nu = 1$ the fit chases noise over a few rounds).
- **Reduced motion.** Rounds apply instantly.
- **Accessibility.** "Round 3 of 50, ν = 0.3, stumps. Training MSE 0.84, validation 0.91. Your stump: split at 0.42, levels −0.31 and 0.27; best: 0.45, −0.33 and 0.29."
- **Tutor hooks.** Ids: `handle:split`, `handle:left`, `handle:right`, `stump:best`, `curve:fit`, `residual:<i>`, `point:<i>`, `slider:nu`, `curve:train`, `curve:val`, `marker:stop`. Secret: the best stump while hidden.
- **Performance.** A stump search is $O(n)$ per feature on presorted data; 500 rounds on 500 points in under 20 ms in the worker; snapshots every round up to 200, then every fifth.
- **Artifact and web.** No difference. The "boost stumps by hand in NumPy" drill is implement-it tier; the `GradientBoostingRegressor` comparison is web-only.
- **Generators.** `next-stump` (residuals with a clear best split), `residual-after`, `adaboost-weights`, `pseudo-residual`, `early-stop` (validation curves with a unique minimum). Difficulty 2 to 4.
- **Misconceptions.** `boosting-rounds-cannot-overfit`, `bigger-learning-rate-is-better`, `boosting-averages-like-bagging`.

#### 6.4.5 `importance-lab`: Importance lab

**Composite · P2 · G2 (finance mode G4).** Which features matter, by four methods that disagree, with the traps made visible.

- **Purpose.** Impurity importance (MDI) is computed in-sample and favours features with many distinct values, so a pure-noise ID column can top the chart (Strobl and others 2007). Permutation importance (MDA) shuffles one column on held-out data and measures the score drop; it is honest about generalisation but splits credit between correlated twins (the substitution effect), so both can look unimportant. Drop-column importance refits without the feature. Single-feature importance (SFI) scores each feature alone and has no substitution effect but misses interactions. Clustered permutation importance shuffles whole clusters of correlated features together (López de Prado). Partial dependence and ICE curves show the shape of an effect; exact Shapley values split one prediction into additive contributions by averaging marginal contributions over all coalitions. None of these is causal.
- **Serves.** 2.1.5 L12, L13; 2.1.8 L11; 2.1.10 L3.
- **Uses.** `value-table` (frame mode with the column-shuffle animation), `marks` (`bars` with whiskers across repeats, ICE and PDP `curve`s), `plot-2d`, `choice` (method chips), `slider` (twin correlation, ID cardinality, repeats), `cluster-lab` (feature clusters), `sim-runner` (`train`), `card-sort` (rank features), `live-formula` (the Shapley average for a 2-feature toy).
- **Interactions.**
  - Pointer: choose a method; tap a column to permute it and watch the score drop; slide the twin's correlation with the best feature; add or remove the ID column; switch to PDP and drag the feature value; in Shapley mode tap coalitions in the toy game's table.
  - Keyboard: chips; the frame is a roving grid with P to permute the focused column; sliders; ranking through `card-sort` keys.
- **State.** `{ method: 'mdi' | 'mda' | 'drop' | 'sfi' | 'clustered-mda' | 'pdp' | 'shapley'; twinRho: number; idColumn: boolean; repeats: number; feature?: string; seed: number }`.
- **Answers and checks.** `ordering` (rank features by a method; the generator keeps adjacent importances apart by at least two standard errors across repeats), `choice` (why MDI crowned the ID column; what the twin did to MDA), `numeric` (a Shapley value in a 2-feature game: $\phi_1 = \frac{1}{2}[v(\{1\}) - v(\varnothing)] + \frac{1}{2}[v(\{1, 2\}) - v(\{2\})]$), `curve` (sketch the PDP's shape).
- **Config.**

```ts
interface ImportanceLabConfig {
  data: Extract<DataSpec, { gen: 'dataset-gen@1/tabular' }>;   // features carry roles: strong, weak, twin, id, noise, interaction
  model: ModelSpec;
  methods: ('mdi' | 'mda' | 'drop' | 'sfi' | 'clustered-mda' | 'pdp' | 'shapley')[];
  evaluation: 'holdout' | 'kfold' | 'purged-kfold';
  editable: ('twinRho' | 'idColumn' | 'repeats')[];
  shapleyToy?: { values: Record<string, number> };   // v(S) for each coalition
}
```

- **Visual.** Importance bars ink with whiskers; after reveal, true-signal features labelled "signal", noise "noise", the ID column "ID (noise)", twins joined by a bracket; permuted cells shuffle with values in `--s2`; PDP `--s2` 2.5px over ICE curves `--s2` at 15%. Answer objects: ranked cards and fields.
- **Motion.** Permuting a column scatters its values over 400ms and the score readout drops (a consequence). Show-why keys: `id-crown` (the ID column's many split points light up across the trees); `twin-split` (the importance of the best feature halves when its twin is added).
- **Reduced motion.** Before-and-after.
- **Accessibility.** Table of features with each method's importance and spread. "Permutation importance on held-out data: x1 0.21, x2 0.19 (twins, correlation 0.9), x5 0.03; ID column 0.00. MDI ranks the ID column second."
- **Tutor hooks.** Ids: `bar:<method>:<feature>`, `col:<feature>`, `bracket:twins`, `curve:pdp`, `ice:<i>`, `slider:twin-rho`, `toggle:id`, `cell:<coalition>`. Secret: feature roles.
- **Performance.** Permutation importance of 6 features with 5 repeats on 500 held-out rows for a 100-tree forest: about 12M node visits, under 60 ms in the worker; exact Shapley for 8 features with 50 background rows: 256 coalitions × 50 rows of predictions, under 100 ms.
- **Artifact and web.** No difference.
- **Generators.** `rank-by-method`, `id-trap`, `twin-effect`, `shapley-toy` (exact rationals). Difficulty 2 to 5.
- **Misconceptions.** `mdi-is-reliable`, `importance-means-causation`, `low-mda-means-useless`.

#### 6.4.6 `cluster-lab`: Cluster lab

**Composite · P2 · G2 (correlation mode G4).** k-means by hand, dendrograms by linkage, and clustering assets and features by correlation.

- **Purpose.** k-means alternates two steps, assign each point to its nearest centroid and move each centroid to its points' mean, and stops at a fixed point that depends on the start; within-cluster sum of squares falls with $k$, and the elbow is a judgement. Agglomerative clustering merges the closest pair repeatedly; single, complete, average and Ward linkage give different trees from the same distances. In finance, correlations become distances $d_{ij} = \sqrt{\frac{1}{2}(1 - \rho_{ij})}$; the dendrogram reorders the correlation matrix into blocks (the quasi-diagonalisation behind hierarchical risk parity) and groups features for clustered importance.
- **Serves.** 2.1.5 L14; 2.1.8 L11, L12; cross-cluster 2.3 (portfolio construction).
- **Uses.** `plot-2d`, `drag-point` (centroids), `marks` (`scatter`, Voronoi cell outlines, elbow `curve`), `node-link` (dendrogram layout with a cut line), `cell-grid` (correlation heatmap with reorder animation), `stepper` (assign and update steps; merges), `slider` ($k$, cut height), `choice` (linkage chips).
- **Interactions.**
  - Pointer: drag centroids, then tap Assign and Update alternately; reseed and compare inertia; slide $k$ for the elbow plot; in hierarchical mode tap the next pair to merge (or let it run) and drag the cut line; in correlation mode watch the matrix reorder.
  - Keyboard: centroids are 2D handles; A assigns, U updates; the merge list is a roving list; the cut line is a slider; chips.
- **State.** `{ mode: 'kmeans' | 'hierarchical' | 'correlation'; centroids?: Vec2[]; step?: number; k?: number; linkage?: 'single' | 'complete' | 'average' | 'ward'; merges?: [string, string][]; cut?: number; seed: number }`.
- **Answers and checks.** `mapping` (points to clusters after one assignment step), `numeric` (a centroid update; a correlation distance, for example $\rho = 0.5$ gives $0.5$; inertia), predicate `kmeans-fixed-point`, `ordering` (the merge order under single linkage for five points), `set` (the clusters at a cut height).
- **Config.**

```ts
interface ClusterLabConfig {
  mode: 'kmeans' | 'hierarchical' | 'correlation';
  data: { points: Vec2[] } | { gen: 'blobs'; k: number; n: number; seed: number }
      | { corr: number[][]; names: string[] } | { gen: 'block-corr'; blocks: number[]; within: number; between: number; seed: number };
  k?: number; linkage?: ('single' | 'complete' | 'average' | 'ward')[];
  task: 'assign' | 'update' | 'merge-order' | 'cut' | 'explore';
}
```

- **Visual.** Points in ink until assigned, then by cluster with the class shapes and hues (at most 3 hues, then shapes alone with labels); centroids `--manip` crosses with handles; Voronoi outlines 1px `--text-muted`; the dendrogram in ink with the cut line `--manip`; the correlation heatmap diverging with numbers. Answer objects: assigned points, centroids, merges and the cut line.
- **Motion.** Assign recolours points; Update slides centroids to the means over 300ms (consequences). Show-why keys: `bad-start` (two seeds converge to different partitions side by side); `chaining` (single linkage strings a long chain of merges).
- **Reduced motion.** Steps cut.
- **Accessibility.** Assignments as a table; the dendrogram as a merge list with heights; the heatmap as a table. "k = 3 after 4 iterations: sizes 40, 35, 25; inertia 61.2."
- **Tutor hooks.** Ids: `centroid:<j>`, `point:<i>`, `cell:<i>,<j>`, `merge:<m>`, `line:cut`, `curve:elbow`, `chip:<linkage>`. Secret: the generating clusters.
- **Performance.** Lloyd steps on 500 points under 1 ms; agglomerative clustering on at most 200 items in $O(n^2 \log n)$, under 20 ms in the worker.
- **Artifact and web.** No difference.
- **Generators.** `assign-step` (no ties in distance), `update-step`, `merge-order`, `corr-distance`, `cut-clusters`. Difficulty 1 to 4.
- **Misconceptions.** `kmeans-finds-the-true-clusters`, `elbow-is-objective`, `correlation-is-a-distance`.

### 6.5 Neural networks

#### 6.5.1 `nn-playground`: Network playground

**Composite · P2 · G3.** A small dense network on 2D data: see every unit's map, train it, break it and fix it.

- **Purpose.** Hidden units are learned features: each draws its own boundary, and the next layer combines them. With linear activations the stack collapses to one linear model; with ReLU, tanh or sigmoid it bends. The learner first hand-sets the weights of a 2-2-1 network to solve XOR, then trains. Parameter count is $\sum_\ell (n_{\ell-1} n_\ell + n_\ell)$. Depth-statistics mode shows activations collapsing or exploding through ten layers when the initial scale is wrong, against Glorot ($\mathrm{Var}(w) = \frac{2}{n_{\text{in}} + n_{\text{out}}}$) and He ($\frac{2}{n_{\text{in}}}$) scales. Regions mode colours the plane by ReLU activation pattern, so the learner counts linear pieces. Regularisation (weight decay, dropout, early stopping) and the learning rate are live controls. The design follows TensorFlow Playground's idea [sourced: Smilkov and Carter's open-source playground]; the implementation is ours, on our primitives.
- **Serves.** 2.1.6 L1, L2, L4, L7, L8; 2.1.2 L6 (link from `classifier-plane`).
- **Uses.** `node-link` (`layered-dense` layout with unit thumbnails), `plot-2d`, `marks` (`field`, `boundary`, `scatter`, activation `hist` per layer), `slider` (learning rate on a log scale, batch size, L2, dropout, noise, initial scale), `choice` (data sets, activations, feature chips), `stepper` (trace mode over epochs), `error-curves` (epochs), `sim-runner` (`train`), `matrix` (a layer's weights in hand-set mode).
- **Interactions.**
  - Pointer: choose a data set and input features ($x_1$, $x_2$, $x_1^2$, $x_2^2$, $x_1x_2$, $\sin x_1$, $\sin x_2$); add or remove layers and units with + and −; choose the activation; Play, Pause, Step and Reset; tap a unit to enlarge its map; in hand-set mode tap an edge and drag its weight on a popover slider; scrub epochs.
  - Keyboard: layers and units form a roving group (Left and Right between layers, Up and Down within one); + and − add or remove; Enter enlarges a unit; Space plays or pauses; S steps; edges in hand-set mode are reached from their unit with E and edited as sliders.
- **State.** `{ data: DataSpec; features: string[]; layers: number[]; activation: string; lr: number; batch: number; l2: number; dropout: number; initScale: 'glorot' | 'he' | number; epoch: number; seed: number; handWeights?: number[][][]; mode: 'train' | 'hand-set' | 'depth-stats' | 'regions' }`.
- **Answers and checks.** Predicate `accuracy-at-least` (hand-set XOR at 100%; a trained configuration at a stated test accuracy, under section 2.3 rule 2), `choice` (predict the effect of linear activations, a learning rate ten times larger, or no regularisation on 50 points), `numeric` (parameter count; linear regions of a small ReLU net), `curve` (sketch the training and test loss against epochs).
- **Config.**

```ts
interface NnPlaygroundConfig {
  data: Extract<DataSpec, { gen: 'dataset-gen@1/classes-2d' | 'dataset-gen@1/regression-1d' }>;
  mode: 'train' | 'hand-set' | 'depth-stats' | 'regions' | 'explore';
  architecture: { layers: number[]; maxLayers: number; maxUnits: number; activation: 'relu' | 'tanh' | 'sigmoid' | 'linear' };
  features: string[]; featurePalette?: string[];
  optimiser: { kind: 'sgd' | 'momentum' | 'adam'; lr: number; batch: number };
  regularise?: { l2?: number; dropout?: number; earlyStop?: boolean };
  editable: ('data' | 'features' | 'architecture' | 'activation' | 'optimiser' | 'regularise' | 'weights')[];
  epochs: number;
}
```

- **Visual.** Units as rounded squares holding their activation map (a 24 × 24 thumbnail on the sequential ramp); edges with thickness proportional to $\lvert w \rvert$, positive `--s3` solid and negative `--s2` dashed (sign by pattern as well as colour); the output field large on the right with classes as in section 2.6 and held-out points hollow; training and test loss curves below; in depth-statistics mode a histogram per layer. Answer objects: hand-set weights and fields.
- **Motion.** Training is data arriving: fields and thumbnails repaint at up to 10 Hz, curves extend per epoch. Show-why keys: `collapse` (with linear activations the hidden maps are all planes and the output stays a straight boundary); `diverge` (a large learning rate sends the loss upward with the field flickering between classes, rate-limited to 2 Hz).
- **Reduced motion.** No live repaint: the state updates on Pause, Step and at the end of a run.
- **Accessibility.** Layers as a table of units with their weights and biases; each unit's map described by its boundary ("unit 2 of layer 1: active right of the line x1 + 0.4 x2 = 0.3"). "Epoch 300: training loss 0.08, test 0.12; test accuracy 0.96." Milestones announced as in section 2.8.
- **Tutor hooks.** Ids: `unit:<layer>:<i>`, `edge:<layer>:<i>-<j>`, `field:output`, `curve:train`, `curve:test`, `chip:<feature>`, `slider:lr`, `slider:l2`, `slider:dropout`, `hist:layer-<l>`. Secret: the generator and the Bayes error.
- **Performance.** Section 2.10: at most 6 layers of 8 units and 500 points; one epoch about 2 ms in the worker; the 48 × 48 output field and every thumbnail come from one forward pass over the grid; float64 with `dmath` throughout so runs reproduce on every device.
- **Artifact and web.** No difference. Drills: a scalar autograd in pure Python (implement-it tier, MicroPython-tagged where CI agrees); a two-layer network in NumPy with manual backpropagation; the PyTorch version runs locally with paste-back.
- **Generators.** `param-count`, `predict-effect` (settings pairs whose outcomes differ by a CI-proven margin), `hand-set-xor` (weight targets with a tolerance band), `regions-count` (small ReLU nets with exact counts). Difficulty 2 to 4.
- **Misconceptions.** `linear-activations-add-power`, `high-learning-rate-trains-faster`, `more-units-always-better`, `zero-initialisation-is-fine`.

#### 6.5.2 `relu-composer`: ReLU composer

**Composite · P2 · G3.** Build a curve from ReLU ramps by hand; then compose layers and count the pieces.

- **Purpose.** One hidden layer of ReLU units computes $c + \sum_i a_i \max(0, w_i x + b_i)$: a piecewise linear function with a kink at each $-b_i/w_i$. With enough kinks it follows any continuous curve on an interval, which is the universal approximation idea in a form the learner can build. With the kinks placed, the output weights are a linear least-squares problem, so "Fit the slopes" is exact. Depth mode composes layers: the tent map $g(x) = 2\max(0, x) - 4\max(0, x - \frac{1}{2})$ composed $L$ times has $2^L$ linear pieces from $2L$ units (Telgarsky 2016), while one layer of $2L$ units has at most $2L + 1$. Sigmoid mode builds bumps from pairs of steps.
- **Serves.** 2.1.6 L3, L4; 2.1.2 L3 (contrast with fixed knots in `basis-lab`).
- **Uses.** `plot-2d`, `drag-point` (each unit's kink on the axis and its slope handle), `marks` (`curve` for each unit, the sum, the target, piece boundaries), `slider` (depth, steepness in sigmoid mode), `live-formula`.
- **Interactions.**
  - Pointer: tap Add unit (at most 12); drag a unit's kink along the axis and its slope handle up or down; tap Fit the slopes; remove a unit by dragging its kink off the axis; in depth mode slide the number of composed layers.
  - Keyboard: each unit's kink and slope are sliders; Insert adds a unit; Delete removes; F fits; the depth slider.
- **State.** `{ units: { kink: number; slope: number }[]; c: number; mode: 'shallow' | 'depth' | 'sigmoid'; depth?: number }`.
- **Answers and checks.** Predicate `mse-at-most` (the sum follows the target within a threshold using at most $m$ units; the threshold sits 10% above the best achievable with $m$ units, computed in CI), `curve` (band coverage against the target), `numeric` (the output at $x$ from shown units; the number of linear pieces), `choice`.
- **Config.**

```ts
interface ReluComposerConfig {
  target: { expr: Expr; domain: [number, number] } | { points: Vec2[] };
  mode: 'shallow' | 'depth' | 'sigmoid';
  maxUnits: number;
  init?: { kink: number; slope: number }[];
  show: ('units' | 'sum' | 'target' | 'pieces' | 'mse')[];
}
```

- **Visual.** The target ink; each unit `--s6` at 50% with its kink as a `--manip` diamond and slope handle; the sum `--s2` 2.5px; piece boundaries as faint vertical ticks with a count label. Answer objects: the units' handles and fields.
- **Motion.** Direct. Show-why keys: `kink-adds-a-bend` (one unit is toggled off and on, showing exactly where the sum bends); `sawtooth` (each composed layer doubles the teeth).
- **Reduced motion.** Before-and-after.
- **Accessibility.** Units listed with kink, slope and contribution. "5 units, kinks at −1.2, −0.4, 0.3, 0.9, 1.6. MSE against the target 0.012. 6 linear pieces."
- **Tutor hooks.** Ids: `unit:<i>`, `kink:<i>`, `slope:<i>`, `curve:sum`, `curve:target`, `readout:mse`, `readout:pieces`, `slider:depth`. Secret: the best achievable MSE.
- **Performance.** At most 12 units on 200 points: under 0.1 ms per frame; fitting slopes is one small least-squares solve.
- **Artifact and web.** No difference.
- **Generators.** `output-at-x`, `count-pieces`, `approximate` (targets with known best $m$-unit error). Difficulty 2 to 4.
- **Misconceptions.** `relu-is-linear`, `width-equals-depth`.

#### 6.5.3 `sequence-filter`: Sequence filter

**Composite · P2 · G3.** Convolution as a learned moving average, recurrence as a carried state, attention as soft lookback.

- **Purpose.** Networks for sequences reuse three ideas a quant already knows. A causal 1D convolution computes $y_t = \sum_{k=0}^{L-1} w_k x_{t-k}$: a moving average, a momentum difference or any other technical filter is one kernel, and training learns the kernel. A centred kernel uses $x_{t+1}$ and leaks the future. A recurrent unit carries a state: $h_t = \alpha h_{t-1} + (1 - \alpha)x_t$ is an EWMA with weights $(1 - \alpha)\alpha^k$. Attention averages past values with softmax weights $a_k = \frac{e^{s_k/\tau}}{\sum_j e^{s_j/\tau}}$ computed from similarity scores; the temperature $\tau$ sharpens or flattens the lookback. On synthetic AR data, fitting the kernel by ridge regression recovers the AR coefficients.
- **Serves.** 2.1.6 L9; 2.1.8 L2 (the causal-window leak, link); cross-cluster 2.2 (filters and EWMA).
- **Uses.** `plot-2d` (the input series, the output series, the kernel as stems), `drag-point` (stem heads), `marks` (`stems`, `paths`, attention weights as `bars`), `slider` ($L$, $\alpha$, $\tau$), `choice` (presets: moving average, EWMA, momentum, difference; causal or centred), `regularisation-path` (link for the learned kernel's ridge).
- **Interactions.**
  - Pointer: drag kernel stem heads; choose a preset; toggle causal or centred; slide $\alpha$ in recurrent mode and watch the implied kernel; in attention mode drag the query time and the temperature; tap Learn to fit the kernel to predict the next value.
  - Keyboard: stems are vertical sliders in a roving group; chips; sliders; L learns.
- **State.** `{ mode: 'conv' | 'recurrent' | 'attention' | 'learn'; kernel: number[]; causal: boolean; alpha?: number; tau?: number; queryT?: number }`.
- **Answers and checks.** `numeric` (the output at $t$ from a shown kernel and series; an EWMA weight), `choice` (causal or leaking; which preset a kernel is), predicate `kernel-matches` (set a kernel that reproduces a target output).
- **Config.**

```ts
interface SequenceFilterConfig {
  series: { values: number[] } | { gen: 'ar' | 'random-walk-returns' | 'trend-noise'; params: Record<string, number>; T: number; seed: number };
  mode: 'conv' | 'recurrent' | 'attention' | 'learn';
  L: number; init?: number[];
  presets?: ('ma' | 'ewma' | 'momentum' | 'difference')[];
  allowCentred: boolean;
  target?: number[];                       // kernel-matching tasks
}
```

- **Visual.** The input series ink; the output `--s2`; kernel stems `--manip` (editable) or ink (shown); in centred mode the future-side stems sit in a hatched zone labelled "future"; attention weights `--s6` bars under the past window with the query time `--manip`. Answer objects: stems and fields.
- **Motion.** Direct: the output redraws per stem drag. Show-why `future-leak`: the centred output at $t$ highlights the input value at $t + 1$ it used.
- **Reduced motion.** Static highlight.
- **Accessibility.** Kernel as a table of lags and weights; "Causal kernel of length 5 (moving average): output at t = 40 is 0.31."
- **Tutor hooks.** Ids: `stem:<k>`, `series:input`, `series:output`, `zone:future`, `slider:alpha`, `slider:tau`, `handle:query`, `bar:<k>`. Secret: the AR coefficients of generated series.
- **Performance.** $T \le 2{,}000$ and $L \le 20$: under 0.1 ms per frame.
- **Artifact and web.** No difference.
- **Generators.** `output-at-t`, `ewma-weight`, `name-the-filter`, `match-kernel`. Difficulty 1 to 3.
- **Misconceptions.** `centred-window-is-fine`, `rnn-has-no-memory-decay`, `attention-is-magic`.

### 6.6 Time-ordered validation and leakage

#### 6.6.1 `time-cv-lab`: Time-ordered CV lab

**Composite · P2 · G4.** Folds on a timeline with label spans: shuffled against blocked, walk-forward, purging, embargo and combinatorial purged cross-validation.

- **Purpose.** Financial labels span time: a label at $t$ uses returns from $t_{i,0}$ to $t_{i,1}$, and features are autocorrelated. Shuffled k-fold puts near-duplicates of each test example into training and flatters the model. Walk-forward validation trains on the past only (expanding or rolling windows). Purged k-fold (López de Prado, chapter 7) removes from training every example whose label span overlaps a test span, where spans $[t_{i,0}, t_{i,1}]$ and $[t_{j,0}, t_{j,1}]$ overlap exactly when $t_{i,0} \le t_{j,1}$ and $t_{j,0} \le t_{i,1}$, and that includes labels that start before the test fold and end inside it. An embargo then drops training examples that start within $h = \lceil \delta T \rceil$ periods after the test fold ($\delta \approx 0.01$), because features just after the test period still carry its information. Combinatorial purged CV splits $T$ into $N$ groups and tests on every choice of $k$ groups: $\binom{N}{k}$ splits, each group tested $\binom{N - 1}{k - 1}$ times, which assemble into $\varphi = \frac{k}{N}\binom{N}{k}$ complete backtest paths. For a pure autoregression with uncorrelated errors, ordinary k-fold is valid (Bergmeir, Hyndman and Koo 2018); overlapping labels break that condition.
- **Serves.** 2.1.7 L1 to L8; 2.1.5 L15 (preview); 2.1.10 L2, L3; cross-cluster 2.2 (`forecast-lab` embeds the fold strip) and 2.3 (backtest validation).
- **Uses.** `span-track` (label spans in rows; fold bands; purge and embargo roles), `cell-grid` (the CPCV split matrix with paint mode for paths), `stepper` (trace mode over splits), `slider` ($k$, embargo $\delta$, window, $N$, $k_{\text{test}}$), `choice` (scheme chips), `marks` (score `bars` per scheme), `sim-runner` (`train` for the score comparison), `tuning-lab` (link for the Trap).
- **Interactions.**
  - Pointer: choose a scheme; drag fold boundaries; step through splits; slide the embargo; in task mode tap training spans to mark them purged or embargoed; in CPCV mode paint one test cell per group to assemble a path; run the score comparison.
  - Keyboard: `span-track` keys for spans; fold boundaries are sliders; N and P step splits; the split matrix is a roving grid with Space to paint; R runs the comparison.
- **State.** `{ scheme: 'shuffled' | 'blocked' | 'purged' | 'walk-forward' | 'rolling' | 'cpcv' | 'ar'; k: number; split: number; embargo: number; window?: number; N?: number; kTest?: number; selected: string[]; paths?: number[][]; ran: boolean }`.
- **Answers and checks.** Predicates `purge-exact` and `embargo-exact` (a misconception predicate `purge-misses-left-edge` catches the commonest error), `set` (the training examples of split $j$), `numeric` (number of splits; number of paths; the embargo length; examples removed), predicate `cpcv-path-valid`, `choice` (predict which scheme reports the higher score; whether k-fold is valid for a stated model).
- **Config.**

```ts
interface TimeCvLabConfig {
  data: Extract<DataSpec, { gen: 'dataset-gen@1/overlap-labels' }> | { spans: { id: string; t0: number; t1: number }[] };
  scheme: { kind: 'shuffled' | 'blocked' | 'purged' | 'walk-forward' | 'rolling' | 'cpcv' | 'ar'; k?: number;
            embargo?: number; window?: number; gap?: number; N?: number; kTest?: number };
  split?: number;
  model?: ModelSpec;                       // for the score comparison
  task: 'purge' | 'embargo' | 'which-train' | 'count' | 'assemble-path' | 'predict-score' | 'explore';
  show: ('spans' | 'bands' | 'concurrency' | 'scores' | 'matrix')[];
  editable: ('scheme' | 'boundaries' | 'embargo' | 'select' | 'paint')[];
}
```

- **Visual.** Label spans in rows; fold bands with section 2.6 roles (train `--s6` at 20%, test `--s2` at 30%, purged hatched `--out`, embargo cross-hatched `--out`); selected spans outlined `--manip`; the CPCV matrix with test cells in `--s2` and painted path cells outlined `--manip` with path numbers; score bars per scheme in ink with whiskers across splits. Answer objects: selected spans and painted cells.
- **Motion.** Fold changes re-role spans with a 200ms cross-fade (a consequence). Show-why keys: `leak-path` (a training span overlapping the test band highlights with an arrow to the shared days); `shuffled-neighbours` (in shuffled mode each test example's nearest training neighbour in time lights up, one day away).
- **Reduced motion.** Static highlights.
- **Accessibility.** Spans as a table (id, start, end, role in this split). "Purged 4-fold, split 2: test days 11 to 20; 5 examples purged (3 before, 2 after the test fold); embargo 1 day removes 1 more."
- **Tutor hooks.** Ids: `span:<id>`, `band:test`, `band:train`, `band:embargo`, `slider:embargo`, `split:<j>`, `cell:<group>,<split>`, `path:<p>`, `bar:<scheme>`. Secret: the exact purge and embargo sets; the true out-of-sample score.
- **Performance.** Overlaps by a sweep over sorted endpoints; at most 2,000 spans (Canvas above 300); the score comparison trains at most 15 small models (logistic or a 50-tree forest) in the worker, under 300 ms.
- **Artifact and web.** No difference. The `PurgedKFold` splitter drill is implement-it tier and uses `assert_folds_purged`; the scikit-learn-compatible version (a `BaseCrossValidator` subclass) is web-only.
- **Generators.** `purge-set` (spans of varied lengths, with at least one left-edge overlap), `embargo-set`, `train-rows`, `cpcv-count`, `assemble-path`, `predict-score` (data where shuffled CV beats purged walk-forward by at least 10 accuracy points). Difficulty 2 to 5.
- **Misconceptions.** `shuffled-kfold-is-fine-for-time-series`, `purge-only-after-test`, `walk-forward-needs-no-purge`, `embargo-is-optional`.

#### 6.6.2 `leakage-detective`: Leakage detective

**Composite · P2 · G4.** Find the leaks: when each value was known, which rows each pipeline step saw, who was in the universe, and what a study left out.

- **Purpose.** Leakage is information at training or decision time that would not exist in live trading. Four kinds, each with its own picture:
  - **Timing.** Each feature has an event time and an availability time. A daily close is known after 16:00, so a 15:59 decision cannot use it; quarterly earnings arrive weeks after the quarter ends and may be restated; index membership is decided in advance but published on a date. Anything available after the decision time leaks.
  - **Preprocessing.** A scaler, imputer, PCA or feature selection fitted on all rows has seen the test fold.
  - **Universe.** Backtesting on today's survivors drops the failures; delisting returns matter.
  - **Study design.** A described study is audited against a checklist built on Luo and others' "seven sins" (survivorship, look-ahead, storytelling, data snooping, turnover and costs, outliers, shorting constraints) [recalled, unverified as the paper's exact list].
- **Serves.** 2.1.8 L1 to L4; 2.1.3 L10 (pipeline Trap); 2.1.10 L2; 3.1.1 L6.
- **Uses.** `span-track` (`gantt` layout: event and availability spans per feature, the decision time as a cursor), `pipeline-flow` (sklearn mode, extension), `value-table` (frame mode with as-of greying), `portfolio-sort` (universe mode link), `card-sort` (audit cards), `choice`, `drag-point` (the decision-time cursor).
- **Interactions.**
  - Pointer: in timeline mode drag the decision-time cursor and tap every feature that is not yet known; in pipeline mode drag each stage inside or outside the CV loop and inspect what it was fitted on; in universe mode toggle point-in-time membership and delisting returns; in audit mode tap the flaws on a study card.
  - Keyboard: `span-track` keys; the cursor is a slider over times; `pipeline-flow` keys; audit cards as a multi-select list.
- **State.** `{ mode: 'timeline' | 'pipeline' | 'universe' | 'audit'; decisionTime?: number; flagged: string[]; pipeline?: { stage: string; inside: boolean }[]; universe?: { pointInTime: boolean; delistings: boolean } }`.
- **Answers and checks.** `set` (exactly the leaky features or the flaws, against the generator's planted list), `ordering` (sort events by availability time), predicates `no-fit-on-test` and `features-available`, `numeric` (survivorship bias in mean annual return, computed exactly on the item panel), `code` (a function that must pass `assert_no_lookahead`).
- **Config.**

```ts
interface LeakageDetectiveConfig {
  mode: 'timeline' | 'pipeline' | 'universe' | 'audit';
  features?: { name: string; event: number; available: number; note: string }[] | { gen: 'leak-catalogue@1'; count: number; leaks: number; seed: number };
  decisionTime?: number;
  pipeline?: { stages: string[]; init: { stage: string; inside: boolean }[] };
  panel?: { gen: 'panel-sim@1'; seed: number };
  study?: { card: string; flaws: string[]; distractors: string[] };
}
```

- **Visual.** Event spans ink, availability spans `--s6`, the decision cursor `--manip` with "decide" above it; features available after the cursor fade to `--out` with a hatch once revealed; flagged features outlined `--manip`; in pipeline mode stages fitted on test rows hatched with "fitted on test"; in universe mode delisted stocks in `--out` with a cross glyph. Answer objects: flagged features, stage placements and audit cards.
- **Motion.** Direct for the cursor. Show-why keys: `known-later` (the leaky feature's availability span slides past the cursor with the gap labelled in hours or days); `fitted-on-test` (the scaler's connector highlights the test rows it read).
- **Reduced motion.** Static highlights.
- **Accessibility.** Features listed with event and availability times and whether each is known at the decision time. "Decision at 15:59 on day t. Close(t) available 16:00: not known. Volume(t−1): known."
- **Tutor hooks.** Ids: `feature:<name>`, `span:<name>:event`, `span:<name>:available`, `cursor:decision`, `stage:<id>`, `toggle:pit`, `toggle:delist`, `card:<flaw>`. Secret: the planted leaks and their reasons.
- **Performance.** Trivial except universe mode, which runs `portfolio-sort` on the item panel in the worker (about 50 ms).
- **Artifact and web.** No difference. The look-ahead drill is implement-it tier.
- **Generators.** `leak-catalogue` (about 40 named leak patterns with reasons, sampled into feature lists with 1 to 3 leaks), `pipeline-order`, `survivorship-bias`, `audit-study`. Difficulty 2 to 5.
- **Misconceptions.** `scaler-on-full-data-is-harmless`, `close-price-is-known-at-the-close`, `survivors-represent-the-market`, `restated-data-is-what-you-knew`.

### 6.7 Financial labels and features

#### 6.7.1 `labelling-lab`: Labelling lab

**Composite · P2 · G4.** Events, fixed-horizon labels, the triple-barrier method, meta-labels, and the weights that overlapping labels need.

- **Purpose.** López de Prado's chapters 2 to 4 in one workbench on a price path.
  - **Events.** The symmetric CUSUM filter samples moments worth labelling: $S^+_t = \max(0, S^+_{t-1} + r_t - E_{t-1}[r_t])$, $S^-_t = \min(0, S^-_{t-1} + r_t - E_{t-1}[r_t])$, an event when either crosses $\pm h$, then a reset.
  - **Fixed-horizon labels** use the sign of the return over $h$ bars with a fixed threshold. They ignore the path (a trade stopped out at −8% on the way to +1% is labelled a win) and ignore changing volatility.
  - **Triple barrier.** An upper barrier at $P_{t_0}(1 + \text{pt} \cdot \sigma_{t_0})$, a lower one at $P_{t_0}(1 - \text{sl} \cdot \sigma_{t_0})$ with $\sigma$ an EWM volatility, and a vertical barrier at $t_0 + h$. The label is the first barrier touched.
  - **Meta-labelling.** A primary rule gives the side; a secondary classifier predicts whether the primary trade will hit profit-taking first, trading recall for precision.
  - **Weights.** Labels overlap, so concurrency $c_t$ counts the labels spanning $t$. Uniqueness is $\frac{1}{c_t}$, and label $i$'s average uniqueness is $\bar u_i = \frac{1}{t_{i,1} - t_{i,0} + 1}\sum_{t = t_{i,0}}^{t_{i,1}} \frac{1}{c_t}$. Return-attribution weights are proportional to $\left\lvert \sum_{t = t_{i,0}}^{t_{i,1}} \frac{r_t}{c_t} \right\rvert$, and the sequential bootstrap draws labels with probability proportional to their average uniqueness given the labels already drawn.
- **Serves.** 2.1.8 L6 to L9; 2.1.7 L3; 2.1.10 L2.
- **Uses.** `plot-2d` (price with barriers; returns and CUSUM sums below), `drag-point` (barrier multipliers as handles on the first event's barriers; the vertical barrier; event markers), `span-track` (label spans and the concurrency series), `marks` (`paths`, horizontal barrier segments, first-touch markers, `step`), `slider` ($h$ for CUSUM, pt, sl, horizon, volatility span), `threshold-lab` (meta mode link), `sim-runner` (`bet-sequence` for the sequential bootstrap), `value-table`.
- **Interactions.**
  - Pointer: slide the CUSUM threshold and watch events appear and vanish; drag the upper and lower barriers (multipliers update for every event) and the vertical barrier; tap an event to focus it; in predict mode tap which barrier the focused path touches first, or drag a marker to the first-touch time; in meta mode slide the secondary model's threshold; in weights mode read concurrency and draw sequential-bootstrap samples one at a time.
  - Keyboard: sliders and barrier handles; events form a roving group; 1, 2 and 3 answer "upper", "lower", "time"; D draws one bootstrap sample.
- **State.** `{ mode: 'events' | 'fixed' | 'triple' | 'meta' | 'weights'; cusumH: number; pt: number; sl: number; horizon: number; volSpan: number; focused?: string; guess?: { barrier: 'upper' | 'lower' | 'vertical'; t?: number }; metaThreshold?: number; draws?: string[]; seed: number }`.
- **Answers and checks.** `choice` (the first barrier), `point` (the first-touch time, tolerance zero bars), `numeric` (a label; concurrency at $t$; a label's average uniqueness; the next sequential-bootstrap probability; precision before and after meta-labelling), `set` (the CUSUM events on a short shown series, exact).
- **Config.**

```ts
interface LabellingLabConfig {
  prices: { values: number[]; dates?: string[] } | { gen: 'price-series'; T: number; seed: number };
  mode: 'events' | 'fixed' | 'triple' | 'meta' | 'weights';
  cusum?: { h: number; expected: 'zero' | 'ewm' };
  barriers?: { pt: number; sl: number; horizon: number; volSpan: number; verticalLabel: 'sign' | 'zero' };
  primary?: { rule: 'ma-cross' | 'breakout'; params: Record<string, number> };   // meta mode
  editable: ('cusum' | 'pt' | 'sl' | 'horizon' | 'events' | 'meta-threshold')[];
  task: 'first-touch' | 'label' | 'events' | 'uniqueness' | 'bootstrap' | 'meta-precision' | 'explore';
}
```

- **Visual.** The price path ink; event markers as small ink ticks above the path; for the focused event the upper barrier `--s3` with "+", the lower `--s2` with "−", the vertical dashed ink, all with `--manip` handles where editable; the first touch marked with a filled ink dot and the label word; spans and the concurrency step series below; sequential-bootstrap probabilities as `--s2` bars updating after each draw. Answer objects: the barrier choice, the touch marker and fields.
- **Motion.** Direct for barriers. Show-why `first-touch`: a playhead runs along the path from the event to the first barrier over 800ms and lights it.
- **Reduced motion.** The touch point is marked statically.
- **Accessibility.** Events as a table (start, end, barrier touched, label, return, uniqueness). "Event 7 on day 112: upper barrier 104.1, lower 97.3, time limit day 122. Touched lower on day 116: label −1."
- **Tutor hooks.** Ids: `event:<id>`, `barrier:upper`, `barrier:lower`, `barrier:vertical`, `marker:touch`, `span:<id>`, `series:concurrency`, `bar:prob-<id>`, `slider:<param>`. Secret: labels while predicting.
- **Performance.** At most 2,520 bars and 500 events; first touches by a forward scan per event, $O(h)$ each; concurrency by a sweep; under 2 ms per barrier drag.
- **Artifact and web.** No difference. The triple-barrier drill (pandas) is web-only; the pure-Python version on a list is implement-it tier.
- **Generators.** `first-touch` (paths without ties at a barrier), `label-value`, `cusum-events` (series of at most 20 returns), `uniqueness` (5 to 8 spans), `bootstrap-prob`, `meta-precision`. Difficulty 2 to 5.
- **Misconceptions.** `horizon-return-tells-the-story`, `overlapping-labels-are-independent`, `stop-loss-is-free`.

#### 6.7.2 `bar-sampler`: Bar sampler

**Composite · P2 · G4.** One trade stream, four ways to cut it into bars.

- **Purpose.** Time bars sample at fixed clock intervals, but information arrives with trading. Tick bars close every $N$ trades, volume bars every $V$ shares, dollar bars every $D$ of notional. Activity-based bars sample more in busy periods, and their returns are closer to independent and normal than time bars' [López de Prado, chapter 2, sourced as the book's claim; the size of the effect varies by market]. The widget shows bars as candles on one time axis, bars per hour, and the return histogram against the normal with kurtosis and the Jarque-Bera statistic.
- **Serves.** 2.1.8 L5.
- **Uses.** `plot-2d` (trades, candles, bars per hour, the return histogram), `marks` (`scatter` for trades sized by volume, candlesticks as requested by the programming catalogue, `hist`, `curve`), `slider` (interval, $N$, $V$, $D$), `choice` (bar type chips), `sim-runner` (`tick-stream`), `value-table`, `qq-plot` (link).
- **Interactions.**
  - Pointer: choose a bar type and slide its threshold; tap a bar to see the trades inside it; toggle the normal overlay; in build mode tap the trade at which each bar closes on a short trade list.
  - Keyboard: chips; sliders; candles form a roving group; Enter opens a bar.
- **State.** `{ type: 'time' | 'tick' | 'volume' | 'dollar'; threshold: number; selectedBar?: number; closes?: number[] }`.
- **Answers and checks.** `numeric` (the number of volume bars, or one bar's open, high, low and close, from a short trade list), `set` (the trades that close each bar), `choice` (which bar type's returns look most normal), `ordering`.
- **Config.**

```ts
interface BarSamplerConfig {
  trades: { t: number; price: number; size: number }[] | { gen: 'tick-stream'; days: number; intensity: 'u-shaped' | 'flat'; seed: number };
  types: ('time' | 'tick' | 'volume' | 'dollar')[];
  thresholds: Partial<Record<'time' | 'tick' | 'volume' | 'dollar', number>>;
  panels: ('trades' | 'candles' | 'per-hour' | 'histogram')[];
  task: 'build' | 'count' | 'compare' | 'explore';
}
```

- **Visual.** Trades as small ink dots sized by volume; candles with bodies in ink outline and wicks; bar boundaries as faint verticals; the return histogram `--s2` with the normal `--s3`; tapped closes `--manip`. Answer objects: tapped closes and fields.
- **Motion.** Direct. Show-why `busy-hours` highlights the opening and closing hours, where activity bars crowd together.
- **Reduced motion.** Static.
- **Accessibility.** Bars as a table (open time, close time, OHLC, volume). "Dollar bars of 2 million: 41 bars today, 14 in the first hour. Return kurtosis 3.4 against 7.9 for 5-minute bars."
- **Tutor hooks.** Ids: `bar:<i>`, `trade:<i>`, `hist:returns`, `curve:normal`, `chip:<type>`, `slider:threshold`, `readout:kurtosis`. Secret: none.
- **Performance.** At most 50,000 trades per item (Canvas); aggregation is one pass, $O(n)$.
- **Artifact and web.** No difference.
- **Generators.** `build-bars` (at most 20 trades), `count-bars`, `ohlc`. Difficulty 1 to 3.
- **Misconceptions.** `time-bars-are-neutral`, `volume-bar-has-fixed-duration`.

#### 6.7.3 `fracdiff-lab`: Fractional differentiation lab

**Composite · P2 · G4.** The memory-against-stationarity trade-off, with $d$ on a slider.

- **Purpose.** Prices keep memory but are not stationary; returns ($d = 1$) are stationary but have forgotten the level. Fractional differencing applies $(1 - B)^d$ with weights $w_0 = 1$, $w_k = -w_{k-1}\frac{d - k + 1}{k}$; the fixed-width version drops weights below a threshold $\tau$. Sliding $d$ from 0 to 1, the ADF statistic falls through the 5% critical value at some $d^*$ well below 1, where the series is stationary and still highly correlated with the original (López de Prado, chapter 5).
- **Serves.** 2.1.8 L10; cross-cluster 2.2 (stationarity).
- **Uses.** `plot-2d` (the weights as stems; the original and transformed series; ADF statistic and correlation against $d$), `marks` (`stems`, `paths`, `curve`, the critical line), `slider` ($d$, $\tau$), `drag-point` (the chosen $d$ on the ADF curve), `test-lab` (compact ADF readout, extension), `series-lab` (link).
- **Interactions.**
  - Pointer: slide $d$ and $\tau$; drag a marker on the ADF-against-$d$ curve to the smallest $d$ that passes; toggle the original series overlay.
  - Keyboard: sliders; the marker is a slider over the $d$ grid.
- **State.** `{ d: number; tau: number; chosen?: number }`.
- **Answers and checks.** `numeric` ($w_1$ and $w_2$ for a stated $d$: at $d = 0.5$, $w_1 = -0.5$ and $w_2 = -0.125$), `point` (the minimum passing $d$ on the item's series, computed exactly on a 0.05 grid; the generator requires the ADF curve to cross the critical value cleanly, at least 0.3 apart at the neighbouring grid points), `choice` (what $d = 1$ means).
- **Config.**

```ts
interface FracdiffLabConfig {
  series: { values: number[] } | { gen: 'price-series'; T: number; seed: number };
  log: boolean;
  dGrid: { min: number; max: number; step: number };
  tau: number;
  show: ('weights' | 'series' | 'adf-curve' | 'corr-curve')[];
}
```

- **Visual.** Weight stems ink (negative stems hang below the axis with a "−"); the original series `--text-muted`; the transformed series `--s2`; the ADF curve ink with the 5% critical value dashed and labelled; the correlation curve `--s6`; the chosen marker `--manip`. Answer objects: the marker and fields.
- **Motion.** Direct. Show-why `memory-kept`: at $d^*$ the transformed and original series overlay with their correlation labelled, then $d = 1$ overlays for contrast.
- **Reduced motion.** Static overlays.
- **Accessibility.** "d = 0.35: 214 weights above τ; ADF −3.1 against a 5% critical value of −2.86: stationary; correlation with log price 0.91." Table of $d$, ADF and correlation.
- **Tutor hooks.** Ids: `slider:d`, `slider:tau`, `stem:<k>`, `series:original`, `series:fracdiff`, `curve:adf`, `line:critical`, `curve:corr`, `marker:d`. Secret: $d^*$.
- **Performance.** At most 500 weights over 2,000 points (1M operations per $d$); the ADF sweep over 41 values of $d$ in the worker in about 50 ms; dragging $d$ between grid points interpolates the precomputed curves.
- **Artifact and web.** No difference. The weights drill is implement-it tier.
- **Generators.** `weights`, `min-d`, `meaning-of-d`. Difficulty 2 to 4.
- **Misconceptions.** `fracdiff-d-one-is-best`, `stationary-means-no-memory`.

### 6.8 Backtest overfitting

#### 6.8.1 `sharpe-lab`: Sharpe ratio lab

**Composite · P2 · G4.** How much to believe one Sharpe ratio: its sampling error, annualisation, fat tails, and the deflations for many trials.

- **Purpose.** A Sharpe ratio is an estimate. Every formula below uses the per-period ratio $\widehat{SR}$ and $T$ periods; the widget always labels units.
  - **Standard error.** For IID normal returns it is about $\sqrt{(1 + \frac{1}{2}SR^2)/T}$ (Lo 2002). With skewness $\gamma_3$ and kurtosis $\gamma_4$ (not excess) the variance becomes $\frac{1 - \gamma_3 SR + \frac{\gamma_4 - 1}{4}SR^2}{T - 1}$ (Mertens 2002), which reduces to Lo's form when $\gamma_3 = 0$ and $\gamma_4 = 3$.
  - **Annualisation.** Multiplying by $\sqrt{q}$ is right only for IID returns. Lo's factor $\eta(q) = \frac{q}{\sqrt{q + 2\sum_{k=1}^{q-1}(q - k)\rho_k}}$ corrects for autocorrelation.
  - **Probabilistic Sharpe ratio.** $\widehat{PSR}(SR^*) = \Phi\left(\frac{(\widehat{SR} - SR^*)\sqrt{T - 1}}{\sqrt{1 - \gamma_3\widehat{SR} + \frac{\gamma_4 - 1}{4}\widehat{SR}^2}}\right)$; the minimum track record length is $1 + \left(1 - \gamma_3\widehat{SR} + \frac{\gamma_4 - 1}{4}\widehat{SR}^2\right)\left(\frac{z_\alpha}{\widehat{SR} - SR^*}\right)^2$ (Bailey and López de Prado 2012).
  - **Deflated Sharpe ratio.** The PSR with the benchmark set to the expected maximum of $N$ trials, $SR^* = \sqrt{V[\widehat{SR}_n]}\left((1 - \gamma)\Phi^{-1}\left[1 - \frac{1}{N}\right] + \gamma\Phi^{-1}\left[1 - \frac{1}{N}e^{-1}\right]\right)$ with $\gamma \approx 0.5772$ (Bailey and López de Prado 2014).
  - **Haircut Sharpe ratio** (Harvey and Liu 2015). Convert to $t = \widehat{SR}\sqrt{T}$, take its p-value, adjust it for $M$ tests (Bonferroni, Holm or BHY), convert back, and report the haircut $1 - \frac{SR_{\text{adj}}}{\widehat{SR}}$.
- **Serves.** 2.1.9 L1, L2, L3, L6, L9; 3.1.2 L8; 3.1.6 L6; cross-cluster 2.3 (results notes).
- **Uses.** `plot-2d` (the sampling distribution; the PSR curve against $T$; the haircut ladder), `marks` (`hist`, `curve`, `band`, markers), `slider` (true $SR$, $T$, frequency, $\gamma_3$, $\gamma_4$, $\rho_1$, $N$, $V$, $M$), `drag-point` (the observed $\widehat{SR}$), `choice` (adjustment chips), `sim-runner` (resampled paths), `dist-explorer` (maximum-of-$N$ family, extension), `drawdown-lab` (linked equity curve), `qq-plot` (link), `live-formula`.
- **Interactions.**
  - Pointer: slide the true Sharpe ratio and track length and run resampled paths; drag the observed $\widehat{SR}$; slide skew, kurtosis and autocorrelation; choose PSR, DSR or haircut mode and set $N$, $V$ or $M$.
  - Keyboard: sliders; the observed-ratio handle is a slider; chips; R runs.
- **State.** `{ mode: 'sampling' | 'annualise' | 'psr' | 'dsr' | 'haircut' | 'mintrl'; sr: number; srHat?: number; T: number; freq: 'daily' | 'weekly' | 'monthly'; skew: number; kurt: number; rho1: number; N?: number; V?: number; M?: number; method?: 'bonferroni' | 'holm' | 'bhy'; seed: number }`.
- **Answers and checks.** `numeric` (the standard error; an annualised ratio with Lo's factor; PSR; MinTRL; the DSR benchmark; a haircut Sharpe ratio; all with stated units and tolerances), `choice` (which record is more convincing: 2.0 over one year or 1.0 over ten), `ordering`.
- **Config.**

```ts
interface SharpeLabConfig {
  mode: 'sampling' | 'annualise' | 'psr' | 'dsr' | 'haircut' | 'mintrl';
  returns?: { gen: 'iid' | 'ar1' | 'skewed'; sr: number; T: number; freq: string; skew?: number; kurt?: number; rho1?: number; seed: number };
  reported?: { srHat: number; T: number; freq: string; skew: number; kurt: number };
  trials?: { N: number; V: number };
  tests?: { M: number; methods: ('bonferroni' | 'holm' | 'bhy')[] };
  editable: string[];
}
```

- **Visual.** The resampled $\widehat{SR}$ histogram `--s2` with the theoretical normal `--s3` and the true value dashed ink; the observed ratio `--manip`; PSR as a curve against $T$ with the 95% line dashed; the DSR benchmark $SR^*$ as an `--s6` dashed line labelled "best of N by luck"; the haircut as a ladder of three bars (reported, adjusted, haircut) with words. Answer objects: fields and the handle where a point is asked.
- **Motion.** Resampled ratios arrive in batches. Show-why keys: `wide-error` (the 95% band of the sampling distribution draws around the observed ratio); `luck-line` (the DSR benchmark rises as $N$ tweens from 1 to 100).
- **Reduced motion.** Final states only.
- **Accessibility.** "Annual Sharpe 1.0 over 3 years of monthly data: standard error 0.59 (annualised); PSR against 0 is 0.95. With 50 trials whose annual Sharpe ratios have variance 0.25, the luck benchmark is 1.14 and DSR is 0.41."
- **Tutor hooks.** Ids: `hist:srhat`, `curve:theory`, `line:true`, `handle:srhat`, `curve:psr`, `line:benchmark`, `bar:reported`, `bar:adjusted`, `bar:haircut`, `slider:<param>`. Secret: the true Sharpe ratio of generated returns.
- **Performance.** Formulas are instant; 2,000 resampled paths of at most 2,520 periods in the worker in under 100 ms.
- **Artifact and web.** No difference. The DSR drill is implement-it tier.
- **Generators.** `se`, `annualise`, `psr`, `mintrl`, `dsr-benchmark`, `haircut`, `which-is-convincing`. Difficulty 2 to 5.
- **Misconceptions.** `sharpe-is-exact`, `annualise-by-sqrt-always`, `fat-tails-do-not-matter`, `deflation-only-for-many-trials`.

#### 6.8.2 `overfit-lab`: Overfitting lab

**Composite · P2 · G4.** Many trials, one winner: the strategy zoo, parameter sweeps, CSCV and the probability of backtest overfitting, minimum backtest length, and leaderboards.

- **Purpose.** Selection is the overfitting. The modes:
  - **Zoo.** $N$ strategies of pure noise: the best in-sample Sharpe ratio grows like $E[\max_N] \approx (1 - \gamma)\Phi^{-1}[1 - \frac{1}{N}] + \gamma\Phi^{-1}[1 - \frac{1}{N}e^{-1}]$ standard errors (about 2.53 for $N = 100$), while its out-of-sample Sharpe ratio scatters around zero.
  - **Sweep.** A moving-average crossover over a grid of windows on a random walk: the best cell looks real; spikes generalise worse than plateaus; with a small planted edge, the plateau survives.
  - **CSCV** (Bailey, Borwein, López de Prado and Zhu 2017). Split the $T \times N$ performance matrix into $S$ blocks. For each of the $\binom{S}{S/2}$ ways to choose half the blocks as in-sample, pick the best in-sample strategy, find its relative rank $\bar\omega$ out of sample, and take $\lambda = \ln\frac{\bar\omega}{1 - \bar\omega}$. The probability of backtest overfitting is the share of $\lambda \le 0$.
  - **MinBTL** (Bailey and others 2014). The years needed so that the best of $N$ independent trials is unlikely to reach a target Sharpe ratio by luck, about $\left(\frac{E[\max_N]}{\overline{SR}}\right)^2$: about 5 years for $N = 45$ at an annual target of 1, consistent with the paper's example [recalled, unverified as the paper's wording].
  - **Leaderboard.** Repeated submissions to a public leaderboard climb while the private score does not (Blum and Hardt 2015); this mode also serves the programming catalogue's Kaggle-style request for 2.4.
- **Serves.** 2.1.9 L4, L5, L7, L8, L10; 3.1.6 L5 and L7 (zoo inside `multiple-testing`); cross-cluster 2.3 (alpha research), 2.4 (Kaggle).
- **Uses.** `plot-2d` (in-sample against out-of-sample scatter; max against $N$; the sweep heatmap; the logit histogram; MinBTL curve on log $N$), `marks` (`scatter`, `curve`, `field`, `hist`), `cell-grid` (the sweep grid; the CSCV block chooser), `slider` ($N$, $T_{\text{IS}}$, $T_{\text{OOS}}$, edge size, $S$), `drag-point` (the learner's research point on the MinBTL plot), `sim-runner` (`strategy-zoo`, `cscv`), `drawdown-lab` (the picked strategy's equity curve), `sharpe-lab` (DSR link).
- **Interactions.**
  - Pointer: predict, then Run the zoo; tap the best in-sample point and reveal its out-of-sample result; slide $N$ and watch the maximum climb against theory; tap the best sweep cell, then reveal; in CSCV mode tap blocks to form one in-sample half and see that combination's logit, then run all; drag your research point on the MinBTL plot; submit to the leaderboard repeatedly.
  - Keyboard: R runs; scatter points and grid cells are roving groups with Enter to pick; sliders; the MinBTL point is a 2D handle.
- **State.** `{ mode: 'zoo' | 'sweep' | 'cscv' | 'minbtl' | 'leaderboard'; N: number; tIS: number; tOOS: number; edge: number; S?: number; picked?: string; blocks?: number[]; research?: { N: number; years: number }; submissions?: number; seed: number }`.
- **Answers and checks.** `choice` (predict the out-of-sample Sharpe ratio of the in-sample winner; which sweep region to trust), `numeric` ($E[\max_N]$ from the formula; $\binom{S}{S/2}$, for example 12,870 at $S = 16$; PBO from a shown logit histogram's counts; MinBTL), `point` (the largest $N$ for a stated history and target on the MinBTL plot, with a log-scale tolerance `factor` of 1.25).
- **Config.**

```ts
interface OverfitLabConfig {
  mode: 'zoo' | 'sweep' | 'cscv' | 'minbtl' | 'leaderboard';
  zoo?: { N: number; tIS: number; tOOS: number; freq: string; edge?: number };
  sweep?: { rule: 'ma-cross' | 'breakout' | 'threshold'; grid: [number[], number[]]; series: { gen: 'random-walk' | 'planted-edge'; T: number; seed: number } };
  cscv?: { S: number; N: number; T: number; edge: number };
  minbtl?: { target: number; maxN: number };
  leaderboard?: { publicRows: number; privateRows: number; maxSubmissions: number };
  seed: number;
}
```

- **Visual.** Zoo: points ink, the picked point ringed `--manip`, its out-of-sample result `--s2` with a connector, the zero line dashed; max-against-$N$: simulation `--s2`, theory `--s3`. Sweep: a sequential heatmap with numbers, the picked cell outlined `--manip`, the out-of-sample heatmap beside it. CSCV: blocks as cells (in-sample `--s6` at 20%, out-of-sample `--s2` at 30%), the logit histogram with the $\lambda \le 0$ area hatched and PBO labelled. MinBTL: the curve ink, the region above it `--s3` at 15% labelled "enough data", the learner's point `--manip`. Answer objects: the picked point or cell, the research point and fields.
- **Motion.** Strategies and combinations arrive in batches. Show-why keys: `winner-regresses` (the picked strategy's out-of-sample point slides down to near zero); `spike-vs-plateau` (neighbouring cells of a spike highlight with their much lower values).
- **Reduced motion.** Final states only.
- **Accessibility.** "100 noise strategies, 2 years in sample: best in-sample Sharpe 1.83 (theory 1.79); its out-of-sample Sharpe −0.12. CSCV with 16 blocks: PBO 0.63." Tables for scatter points (top 20), the sweep grid and the logit histogram.
- **Tutor hooks.** Ids: `point:<i>`, `point:picked`, `curve:max-sim`, `curve:max-theory`, `cell:<i>,<j>`, `block:<b>`, `hist:logits`, `area:pbo`, `curve:minbtl`, `handle:research`, `slider:<param>`. Secret: which strategies carry a planted edge.
- **Performance.** Section 2.10: zoo of 1,000 strategies by 2,520 days in the worker; sweep grids of 30 × 30 by prefix sums; CSCV at $S = 16$ from per-block sums in under 100 ms.
- **Artifact and web.** No difference. The CSCV drill is implement-it tier.
- **Generators.** `emax`, `cscv-count`, `pbo-from-counts`, `minbtl`, `predict-oos` (zoos where the winner's out-of-sample ratio is near zero by construction), `trust-region` (sweeps with one spike and one planted plateau). Difficulty 2 to 5.
- **Misconceptions.** `best-backtest-is-skill`, `more-trials-more-confidence`, `spike-is-the-best-parameter`, `leaderboard-is-the-test-set`.

### 6.9 Capstone and assessment

#### 6.9.1 `ml-workbench`: ML workbench

**Composite · P2 · G5.** The 2.1 exit project as a guided pipeline: frame, data, features, labels, folds, models, evaluation and the results note, with a leakage audit that never sleeps.

- **Purpose.** The exit asks for one tabular prediction problem done end to end with time-ordered cross-validation. The workbench lays the project out as eight steps, each a small panel that embeds the widget that taught it, and keeps an audit strip at the top that turns amber (with a word, not colour alone) when any rule breaks: a feature not available at the decision time, a stage fitted on test rows, folds not purged by the label spans, the hold-out touched before the final run, or a trial not logged. Arena mode compares models on the same purged walk-forward folds and reports paired differences with error bars, which is where "neural networks rarely win on small, noisy tabular data" is seen rather than told (Grinsztajn, Oyallon and Varoquaux 2022; but see Gu, Kelly and Xiu 2020, where networks and trees did best on US equities with monthly predictive $R^2$ under 1% [recalled, unverified]). The trial ledger logs every configuration run, feeding the DSR in `sharpe-lab`. Export produces a scikit-learn script with tests (`assert_no_lookahead`, `assert_folds_purged`) for the learner's repository.
- **Serves.** 2.1.10 L1 to L5; 2.1.6 L10 (arena); 2.1.9 L11 (ledger); cross-cluster 2.4 (Kaggle-style tabular workflow, with `overfit-lab`'s leaderboard mode) and 2.3 project 2.
- **Uses.** `feature-builder`, `labelling-lab`, `time-cv-lab`, `leakage-detective` (audit predicates), `pipeline-flow` (sklearn mode), `tuning-lab`, `regularisation-path`, `ensemble-lab`, `boosting-lab`, `nn-playground` (small preset), `signal-lab` (IC and a simple long-short evaluation), `sharpe-lab`, `error-curves`, `value-table`, `free-response` (results note), `setup-checklist` (project mode), `code-cell` (export and the exit drill).
- **Interactions.**
  - Pointer: work through the step rail (each step opens its panel); tap the audit strip to see the failing rule and jump to its step; run the arena; lock or unlock the hold-out (unlocking twice is logged and shown in the note); export.
  - Keyboard: the step rail is a tab list; each panel uses its widget's keys; A opens the audit; X exports.
- **State.** `{ step: number; frame: { target: string; horizon: number; universe: string; metric: string; decision: string }; features: unknown; labels: unknown; folds: unknown; models: ModelSpec[]; ledger: { id: string; config: unknown; score: number; at: string }[]; holdout: { locked: boolean; unlocks: number }; note?: string }`. Under 64 KB; models are re-derived (section 2.1 requirement 10).
- **Answers and checks.** Predicate `audit-green` (all of `features-available`, `no-fit-on-test`, `labels-purged`, hold-out untouched until final, ledger complete), `choice` and `numeric` in the arena (which model wins by more than its error bar), `free-text` (the results note against a 10-point rubric, self-marked with a Bertie draft), `code` (the exported script's tests, web or local).
- **Config.**

```ts
interface MlWorkbenchConfig {
  data: { gen: 'dataset-gen@1/tabular' | 'panel-sim@1'; seed: number; params?: Record<string, unknown> } | { csv: string };   // CSV on the web only
  steps: ('frame' | 'data' | 'features' | 'labels' | 'folds' | 'models' | 'evaluate' | 'note')[];
  audit: ('features-available' | 'no-fit-on-test' | 'labels-purged' | 'holdout' | 'ledger')[];
  models: string[];                        // allowed families
  rubric: { point: string; marks: number }[];
  mode: 'capstone' | 'arena' | 'kaggle';
}
```

- **Visual.** A step rail with ticks; the audit strip as a row of rule chips with icons and words (passing, failing); embedded widgets keep their own visuals; arena results as paired-difference bars with whiskers against a reference model; the ledger as a table. Answer objects: the note field and arena answers.
- **Motion.** Step changes slide panels (200ms); audit chips flip state with a 150ms wash. No show-why of its own: embedded widgets bring theirs.
- **Reduced motion.** Panels cut.
- **Accessibility.** The audit strip is a live region on commit ("Audit: 1 rule failing. Feature 'eps_next' is not known at the decision time."). Every panel follows its widget's accessibility; the ledger and arena results are tables.
- **Tutor hooks.** Describe: "Step 5 of 8 (folds). Purged walk-forward, 6 splits, embargo 5 days. Audit: green. Ledger: 14 trials." Ids: `step:<name>`, `audit:<rule>`, `arena:<model>`, `ledger:<id>`, `holdout`, `export`. Secret: the planted signal and leaks of generated data. Bertie can review the results note at the `complex` tier on request.
- **Performance.** Each step's cost is its widget's; the arena runs at most 5 models on at most 6 splits in the worker, about 2 s with progress [unverified].
- **Artifact and web.** All steps run in both; CSV upload and the exit drill are web or local; export goes through `downloads` in the Artifact.
- **Generators.** Seeds only: each learner's capstone data set is seeded so planted signal and leaks differ between attempts.
- **Misconceptions.** Those of the embedded widgets, plus `holdout-peeking-is-harmless` and `unlogged-trials-do-not-count`.

#### 6.9.2 `viva`: Viva

**Composite (input) · P1 · E (first used at the 1.6 exit), required at G5.** An oral-style examination in text: Bertie asks, probes twice, and drafts a mark the learner confirms.

- **Purpose.** Exit tests that say "explain without notes" need an examiner who follows up. The viva hides notes, asks one seeded question from a bank, gives a time limit (adjustable or off), then asks up to two follow-ups chosen to probe the rubric points the answer missed. Bertie marks against the rubric, quoting the learner's words as evidence for each point, and the learner confirms or changes the mark (the lesson-creator skill's model answer and 10-point rubric). Bertie gives no hints during the viva and reveals the model answer only after marking.
- **Serves.** 1.6 exit ("explain every number"), 2.1.10 L6 (leakage, regularisation, bias-variance), 3.1.6 L8 (defend the replication note); cross-cluster 3.3 (mock interviews, where speaking the answer aloud is the skill: the learner may dictate through the operating system's keyboard).
- **Uses.** `free-response` (timed mode with the no-notes lock, extension), `live-formula` (KaTeX preview of maths typed as LaTeX), the tutor transport (section 2.9), `value-table` (rubric marks).
- **Interactions.**
  - Pointer: Start (notes lock); type the answer; Submit; answer the follow-ups; review Bertie's draft marks point by point and confirm or adjust each; reveal the model answer.
  - Keyboard: a standard textarea; Ctrl+Enter submits; the rubric is a list of checkboxes and number fields; Escape pauses the timer when timing is off-by-setting.
- **State.** `{ questionId: string; seed: number; turns: { role: 'examiner' | 'learner'; text: string }[]; timeLimitS?: number; draft?: { point: string; awarded: number; quote: string }[]; final?: number[]; done: boolean }`. The transcript stays under 6 KB so it fits every resend.
- **Answers and checks.** `text` with check kind `free-text` and marking `tutor-draft` (Bertie drafts; the learner confirms; the confirmed mark is the grade).
- **Config.**

```ts
interface VivaConfig {
  bank: { id: string; question: string; rubric: { point: string; marks: number }[]; model: string; followUps: string[] }[];
  pick: { seed: number } | { ids: string[] };
  timeLimitS?: number;                     // learner can extend tenfold or turn off (WCAG 2.2.1)
  maxFollowUps: 0 | 1 | 2;
  noNotes: boolean;
  offline: 'static-follow-ups' | 'self-mark-only';
}
```

- **Visual.** A quiet examination card: Bertie's face (the Einstein bobble head) small at the left of examiner turns, in its "listening" pose, never celebrating; the learner's turns right-aligned; the timer as a thin `--text-muted` bar with seconds in tabular figures (never amber, since amber is reserved for grading); the rubric review as rows with Bertie's quote under each point. Answer objects: the confirmed marks.
- **Motion.** Turns enter over 200ms; Bertie's face blinks at most once per turn. No show-why.
- **Reduced motion.** Turns appear; the face is static.
- **Accessibility.** The transcript is a log region; the timer announces at the half-way point and one minute before the end; timing can be extended or switched off before starting (WCAG 2.2 success criterion 2.2.1).
- **Tutor hooks.** This widget is a tutor surface. Prompts carry the question, the rubric and the transcript; the examiner instruction forbids hints and model-answer disclosure before marking. Follow-ups use the `default` tier; marking uses `complex`; caching is off. When the `sample` capability is absent or a call rejects, the widget falls back to the authored static follow-ups and self-marking, and says so.
- **Performance.** Text only; one model call per turn.
- **Artifact and web.** `sample` on the viewer's account in the Artifact; the proxy on the web. The transcript saves to `db` (Artifact) or IndexedDB (web) under the attempt.
- **Generators.** Seeded selection from the bank; no numeric generation.
- **Misconceptions.** Not applicable; rubric points carry the content.

## 7. Research-paper composites (3.1)

All 6 composites in this section are P2, in waves H1 and H2. `sharpe-lab` and `overfit-lab` (section 6.8) and the extended `multiple-testing`, `regression-lab`, `coint-lab` and `leakage-detective` also serve 3.1.

### 7.0 The rehearsal market: `panel-sim`

Every 3.1 widget runs first on `panel-sim` (decision 4), a seeded synthetic equity market whose effects are planted, so a replication can be graded against the truth before the learner meets real data. It is a service, not a widget; this is its requirement list.

- **Monthly panel.** $N \le 1{,}000$ stocks over $T \le 720$ months with a market cap (evolving with returns), a book-to-market ratio (persistent in logs), a beta, a sector (10 groups), an exchange flag (about 30% "NYSE", larger on average, used for breakpoints) and a risk-free rate path.
- **Returns.** $r_{i,t} = r_{f,t} + \beta_{i,t}\,\text{MKT}_t + \mu_{i,t} + s_{g(i),t} + \varepsilon_{i,t}$, with sector shocks $s$ and idiosyncratic noise whose volatility rises as size falls. The planted expected return is $\mu_{i,t} = \lambda_{\text{size}}\,z(-\ln \text{ME}_{i,t-1}) + \lambda_{\text{value}}\,z(\ln \text{BM}_{i,t-1}) + m_{i,t} - \kappa\,\varepsilon_{i,t-1}$, where $m_{i,t}$ is a persistent latent drift (AR(1) with persistence $\phi_m$), so past returns forecast future returns and momentum emerges rather than being imposed, and $\kappa$ plants short-term reversal.
- **Crashes.** After market drawdowns, past losers' betas rise, so a sharp rebound produces a momentum crash, the mechanism Daniel and Moskowitz (2016) describe [recalled, unverified as their exact mechanism].
- **Publication.** At a configurable month $t_{\text{pub}}$ every planted premium is multiplied by $1 - d$ (default $d = 0.5$ [our choice], in the range McLean and Pontiff's post-publication decline suggests [recalled, unverified]).
- **Microcaps and costs.** Stocks below the 20th "NYSE" size percentile carry larger planted anomaly returns and a half-spread inversely related to size, so their premia shrink or vanish after costs, which is the pattern Hou, Xue and Zhang (2020) emphasise [recalled, unverified].
- **Delistings.** A hazard rising with poor past returns and small size; a delisting return drawn around a negative mean (default −30% [our choice]); a `survivorsOnly` view that drops delisted histories.
- **Daily pairs universe.** Clusters of stocks whose log prices share a random-walk trend plus stationary Ornstein-Uhlenbeck deviations (cointegrated within a cluster), independent stocks, and pairs that break (lose their shared trend) after a date. At most 200 stocks over 2,520 days.
- **Truth.** Every planted parameter, the publication month, the decay, the cointegrated pairs and the break dates are returned for `secret()` and for grading.
- **Acceptance.** At $N = 1{,}000$ and $T = 720$ with the CI seed, the reference decile sorts recover each planted premium within 4 standard errors; golden hashes per seed (section 2.1 requirement 9).

### 7.1 `portfolio-sort`: Portfolio sort

**Composite · P2 · H1.** Rank stocks on a characteristic, form portfolios, hold them, and read the spread: the engine of momentum and of the Fama and French factors.

- **Purpose.** The empirical method behind most of 3.1. At each rebalance date, rank stocks on a characteristic (past $J$-month return skipping $S$ months, size, book-to-market, beta, volatility), split them at breakpoints into quantile portfolios, weight them (equal or by market cap at formation), hold them for $K$ months, and record returns. Jegadeesh and Titman's overlapping method holds $K$ cohorts at once, each formed in a different month, so each month's portfolio return is the average of $K$ cohort returns and one cohort is replaced. Double sorts on size and book-to-market with "NYSE" breakpoints (the median for size; the 30th and 70th percentiles for book-to-market) give six value-weighted portfolios, from which $\text{SMB} = \frac{1}{3}(\text{SL} + \text{SM} + \text{SH}) - \frac{1}{3}(\text{BL} + \text{BM} + \text{BH})$ and $\text{HML} = \frac{1}{2}(\text{SH} + \text{BH}) - \frac{1}{2}(\text{SL} + \text{BL})$. The $J \times K$ grid repeats the paper's main table on the rehearsal market. Excluding microcaps, adding delisting returns and charging costs show which effects survive sensible choices.
- **Serves.** 3.1.1 L4; 3.1.2 L1 to L5, L8; 3.1.3 L2; 2.1.8 L4 (universe link); cross-cluster 2.3 project 2.
- **Uses.** `plot-2d` (one date's characteristic against next-month return with breakpoints; decile bars; cumulative long-short returns on a log scale; the grid), `drag-point` (breakpoints, constrained to the characteristic axis), `span-track` (`gantt` timeline of formation, skip and holding windows per cohort), `marks` (`scatter`, `bars` with whiskers and sign glyphs, `paths`), `cell-grid` ($J \times K$ heatmap with mean and $t$), `slider` ($J$, $S$, $K$, quantiles), `choice` (characteristic, weighting, sort type chips), `stepper` (dates), `value-table` (the decile table), `regression-lab` (Newey-West link), `sim-runner` (`panel`).
- **Interactions.**
  - Pointer: choose a characteristic and slide $J$, $S$ and $K$; scrub dates to see one month's sort; drag breakpoints in breakpoint tasks; toggle microcaps, delisting returns, survivors-only and costs; in grid mode tap a cell to open its strategy; in timeline mode drag the windows of the focused cohort.
  - Keyboard: chips; sliders; breakpoints are sliders over the sorted characteristic; the date stepper uses Left and Right; the grid is a roving grid.
- **State.** `{ characteristic: string; J: number; S: number; K: number; quantiles: number; weighting: 'equal' | 'value'; sort: 'single' | 'double' | 'factor' | 'grid'; date: number; breakpoints?: number[]; filters: { microcaps: boolean; delisting: boolean; survivorsOnly: boolean; costBps: number }; seed: number }`.
- **Answers and checks.** `numeric` (WML from the decile table; one portfolio's return from five stocks' weights and returns, exact; SMB or HML from six portfolio returns; the overlapping-cohort average; months of history a strategy needs, $J + S$), `set` (the stocks in the top decile on a shown date), predicate `breakpoints-match`, `state` (windows set for "12-1" momentum), `choice` (pattern reading), `code` (the pandas decile-sort drill against fixtures, web-only).
- **Config.**

```ts
interface PortfolioSortConfig {
  panel: { gen: 'panel-sim@1'; N: number; T: number; seed: number; params?: Record<string, number> } | { csv: string };
  sort: 'single' | 'double' | 'factor' | 'grid';
  characteristic: 'momentum' | 'size' | 'book-to-market' | 'beta' | 'volatility' | 'reversal';
  windows: { J: number; S: number; K: number; overlap: boolean };
  quantiles: number;
  breakpoints: 'all' | 'nyse';
  weighting: 'equal' | 'value';
  filters?: { excludeMicrocaps?: boolean; delisting?: boolean; survivorsOnly?: boolean; costBps?: number };
  grid?: { J: number[]; K: number[] };
  task: 'predict-decile' | 'set-breakpoints' | 'compute' | 'set-windows' | 'read-grid' | 'explore';
}
```

- **Visual.** The one-date scatter: stocks as ink dots sized by cap, breakpoints `--manip` with handles, quantile bands alternating `--bg-sunken`; decile bars ink with whiskers, the long leg labelled "+" in `--s3` and the short leg "−" in `--s2`; the cumulative long-short path `--s2` on a log axis with sample periods banded (section 2.6); the $J \times K$ grid on the sequential ramp with mean and $t$ in each cell; the timeline in `gantt` layout. Answer objects: breakpoints, selected stocks, windows and fields.
- **Motion.** Scrubbing dates re-sorts the scatter instantly (direct). A cohort rolling out of the book slides left over 300ms when the date steps (a consequence). Show-why keys: `skip-month` (the formation window's last month highlights with its reversal return); `overlap-average` (the $K$ cohorts' returns stack and average).
- **Reduced motion.** Cohort changes cut.
- **Accessibility.** The decile table (mean, $t$, SD, average stocks); "Momentum 6-1-6, equal-weighted deciles, 1965 to 2024 in rehearsal time: WML 0.92% a month, Newey-West t 4.1; decile 10 1.38%, decile 1 0.46%." The scatter's table lists stocks with characteristic, decile and next return.
- **Tutor hooks.** Ids: `handle:bp:<i>`, `decile:<q>`, `path:wml`, `cell:<J>,<K>`, `cohort:<c>`, `span:<cohort>:<window>`, `chip:<characteristic>`, `toggle:<filter>`, `slider:<window>`. Secret: planted premia, decay and $t_{\text{pub}}$.
- **Performance.** Section 2.10: one strategy about 50 ms on the full panel in the worker; the 12 × 12 grid cached per panel with progress; the scatter for one date redraws in under 2 ms.
- **Artifact and web.** No difference; the pandas drill and real-data runs are web or local.
- **Generators.** `wml-from-table`, `portfolio-return` (exact), `smb-hml`, `cohort-average`, `history-needed`, `top-decile`, `breakpoints`. Difficulty 1 to 4.
- **Misconceptions.** `momentum-means-buying-last-month`, `skip-month-is-optional`, `equal-and-value-weights-agree`, `breakpoints-from-all-stocks`.

### 7.2 `signal-lab`: Signal lab

**Composite · P2 · H1.** Evaluate a cross-sectional signal: information coefficient, decay, turnover, costs and breadth; build formulaic alphas from operator tokens.

- **Purpose.** A cross-sectional signal $s_{i,t}$ is judged by how well it ranks next period's returns: the information coefficient $\text{IC}_t$ (Pearson) or rank IC (Spearman) each date, its mean, its standard deviation, the information ratio of the IC series and its $t$-statistic; by how fast that falls with the horizon (IC decay); by turnover, since trading costs scale with it; and by breadth. Grinold's fundamental law, $\text{IR} \approx \text{IC}\sqrt{\text{BR}}$, extended with the transfer coefficient, $\text{IR} = \text{TC} \cdot \text{IC}\sqrt{\text{BR}}$ (Clarke, de Silva and Thorley 2002), explains why an IC of 0.05 across hundreds of stocks is valuable. Neutralising by market or sector removes exposures the signal did not intend. Expression mode builds formulaic alphas in the WorldQuant BRAIN style (Kakushadze 2016) from typed tokens such as `rank(-ts_delta(close, 5))`, with a delay of one period enforced: an alpha built from today's close and traded at today's close is a look-ahead leak.
- **Serves.** 3.1.1 L7; 3.1.2 L9; 2.1.2 L12; 2.1.4 L13; 2.1.10 L3 (evaluation); cross-cluster 2.3 project 2 (information coefficient, turnover and Sharpe ratio after costs).
- **Uses.** `plot-2d` (one date's signal against next return; the IC time series; decay; net and gross equity; the breadth curve), `marks` (`scatter`, `bars`, `paths`, `curve`), `token-tray` (typed expression slots, section 4), `slider` (horizon, cost per unit of turnover, breadth, transfer coefficient), `choice` (signal presets, neutralisation chips), `portfolio-sort` (quantile spreads link), `sharpe-lab` (link), `sim-runner` (`panel`), `live-formula`.
- **Interactions.**
  - Pointer: choose a signal or build one by dragging operator and field tokens into slots; toggle neutralisation; scrub dates to see one cross-section; slide the horizon, the cost and the breadth; in hand-compute mode rank five stocks by signal and by return.
  - Keyboard: `token-tray` keys (Space lifts, arrows choose a slot, Space drops; Delete removes a token); chips; sliders; the date stepper.
- **State.** `{ source: 'preset' | 'expression' | 'model'; preset?: string; expression?: TokenTree; neutralise: ('market' | 'sector' | 'size' | 'beta')[]; delay: 0 | 1; horizon: number; costBps: number; breadth?: number; tc?: number; date: number }`.
- **Answers and checks.** `numeric` (rank IC for five stocks by hand, exact; the IC information ratio and $t$; the fundamental-law IR, for example $0.05\sqrt{400} = 1.0$; a net return as gross minus cost times turnover), predicate `expression-valid`, predicate `features-available` (delay), `choice`, `ordering` (signals by net Sharpe ratio, margin-checked).
- **Config.**

```ts
interface SignalLabConfig {
  panel: { gen: 'panel-sim@1'; N: number; T: number; seed: number } | { csv: string };
  source: { preset: 'momentum' | 'reversal' | 'value' | 'low-vol' | 'size' } | { expression: string; editable: boolean } | { model: string };
  operators?: ('rank' | 'zscore' | 'ts_mean' | 'ts_std' | 'ts_delta' | 'ts_rank' | 'delay' | 'correlation' | 'decay_linear' | 'neutralise' | 'sign' | 'abs' | 'log')[];
  fields?: ('close' | 'open' | 'high' | 'low' | 'volume' | 'vwap' | 'returns' | 'cap' | 'sector')[];
  delay: 0 | 1; enforceDelay: boolean;
  panels: ('cross-section' | 'ic-series' | 'decay' | 'quantiles' | 'turnover' | 'equity' | 'breadth')[];
  costBps?: number;
}
```

- **Visual.** The cross-section scatter ink with a rank-fit line `--s2`; the IC series as thin ink bars with its mean dashed `--s2`; decay as `--s2` stems against horizon; gross equity `--s6` dashed and net equity `--s2`; tokens as lipped chips (operators `--code-keyword`, fields ink) in typed slots, an invalid drop springing back with the type named. Answer objects: the expression, ranks and fields.
- **Motion.** Direct; slotting a token re-evaluates and redraws within one interaction. Show-why keys: `cost-drag` (the gap between gross and net equity shades as the cost tweens up); `delay-leak` (with delay 0 the signal's fit to same-day returns lights up, labelled "uses today's close").
- **Reduced motion.** Static.
- **Accessibility.** The expression reads as text ("rank of minus the 5-day change in close"); the IC series as a table; "Rank IC mean 0.031, SD 0.11, t 6.9 over 600 months; turnover 38% a month; net Sharpe 0.6 at 20 basis points."
- **Tutor hooks.** Ids: `token:<i>`, `slot:<path>`, `series:ic`, `stem:<h>`, `path:gross`, `path:net`, `chip:<neutraliser>`, `slider:cost`, `slider:breadth`, `readout:ir`. Secret: which planted premia the expression can capture.
- **Performance.** Rank IC over 600 months by 1,000 stocks: about 6M operations; expression evaluation capped at depth 6, each time-series operator $O(NTd)$ with prefix sums where possible; under 100 ms in the worker.
- **Artifact and web.** No difference.
- **Generators.** `rank-ic-by-hand`, `fundamental-law`, `net-return`, `ic-t`, `fix-the-expression` (an expression with a delay-0 leak). Difficulty 2 to 4.
- **Misconceptions.** `high-ic-means-profitable`, `turnover-is-free`, `delay-zero-is-fine`, `breadth-is-number-of-stocks` (independent bets, not names).

### 7.3 `factor-model-lab`: Factor model lab

**Composite · P2 · H1.** CAPM against three factors: loadings by hand, alphas across 25 portfolios, the GRS test and Fama-MacBeth regressions.

- **Purpose.** Fama and French (1993) explain the cross-section of returns with three factors. The modes:
  - **SML.** The CAPM's security market line is too flat: portfolio betas barely explain average returns, while size and book-to-market portfolios line up off the line.
  - **Single.** A time-series regression $R_{p,t} - R_{f,t} = \alpha_p + b_p\,\text{MKT}_t + s_p\,\text{SMB}_t + h_p\,\text{HML}_t + e_{p,t}$, which the learner first fits by dragging the loadings, then compares with OLS. The intercept $\alpha_p$ is the return the factors leave unexplained.
  - **Grid.** 25 size and book-to-market portfolios: alphas shrink and $R^2$ rises from CAPM to three factors, and the loadings form monotone patterns across the grid.
  - **GRS.** Gibbons, Ross and Shanken (1989) test whether all $N$ alphas are zero together: $W = \frac{T - N - L}{N} \cdot \frac{\hat\alpha^\top\hat\Sigma^{-1}\hat\alpha}{1 + \bar\mu^\top\hat\Omega^{-1}\bar\mu} \sim F_{N,\,T - N - L}$ under normal errors, with $L$ factors of mean $\bar\mu$ and covariance $\hat\Omega$ and residual covariance $\hat\Sigma$ (divisor conventions fixed by the fixture; [unverified] which the paper uses).
  - **Fama-MacBeth** (1973). Each month a cross-sectional regression of returns on loadings or characteristics; the slopes' time-series mean and its standard error $\frac{s(\hat\lambda_t)}{\sqrt{T}}$; the errors-in-variables issue when loadings are estimated, with Shanken's correction named.
  - **Momentum.** Regressing WML on the three factors shows it is not explained by them (3.1.2 L7); adding Carhart's UMD shows a fourth factor.
- **Serves.** 3.1.2 L7; 3.1.3 L1, L3 to L8; cross-cluster 2.3 (factor attribution of a project's returns).
- **Uses.** `plot-2d` (SML scatter; the regression fit; residuals), `slider` (loadings), `marks` (`scatter`, `bars` for loadings, residual `paths`), `cell-grid` (5 × 5 grids of alpha, $t$, $R^2$ and loadings, diverging with numbers), `regression-lab` and `summary-table` (single-regression detail), `dist-explorer` ($F$ tail), `stepper` (Fama-MacBeth months), `choice` (model chips: CAPM, FF3, FF3 + UMD), `portfolio-sort` (factor construction link), `matrix` ($\hat\Sigma$ and $\hat\Omega$ in GRS mode), `live-formula`.
- **Interactions.**
  - Pointer: choose a model; drag the loading sliders until the residual variance stops falling, then reveal OLS; tap a grid cell to open its regression; step through Fama-MacBeth months and watch the slope series build; open the GRS panel.
  - Keyboard: chips; loading sliders; the grid is a roving grid with Enter to open; the month stepper.
- **State.** `{ mode: 'sml' | 'single' | 'grid' | 'grs' | 'fama-macbeth'; model: 'capm' | 'ff3' | 'ff3-umd'; portfolio?: string; loadings?: number[]; month?: number; revealed: boolean }`.
- **Answers and checks.** `numeric` (alpha from mean excess return and loadings: $\alpha = \bar R^e - b\,\overline{\text{MKT}} - s\,\overline{\text{SMB}} - h\,\overline{\text{HML}}$; GRS from given pieces; the Fama-MacBeth mean slope and $t$), predicate `rss-within` (hand-fitted loadings within 5% of the OLS residual sum of squares), `choice` (CAPM or three factors from a grid; is momentum explained), `code` (statsmodels drill, web-only).
- **Config.**

```ts
interface FactorModelLabConfig {
  source: { panel: { gen: 'panel-sim@1'; seed: number } } | { csv: { portfolios: string; factors: string } };   // Ken French files on the web
  mode: 'sml' | 'single' | 'grid' | 'grs' | 'fama-macbeth';
  models: ('capm' | 'ff3' | 'ff3-umd')[];
  portfolio?: string;
  se?: 'ols' | 'newey-west';
  task: 'fit-loadings' | 'alpha' | 'read-grid' | 'grs' | 'fm-slope' | 'explore';
}
```

- **Visual.** SML: portfolios as ink dots labelled by size and value group, the CAPM line `--s6` dashed, the fitted line `--s2`; single mode: loading bars with sign glyphs, the fit `--s2` against the portfolio's excess return in ink, the learner's loadings `--manip` until revealed; grids: diverging cells with values and "+" or "−"; the GRS $F$ tail hatched beyond the observed statistic. Answer objects: loadings and fields.
- **Motion.** Direct for loading sliders. Show-why keys: `alphas-fade` (CAPM to three factors cross-fades the grid's alphas towards zero); `flat-sml` (the CAPM line pivots to the fitted line).
- **Reduced motion.** Before-and-after.
- **Accessibility.** Grids as tables; "Small-value portfolio on three factors: alpha 0.12% a month (t 1.4), b 1.02, s 1.31, h 0.74, R squared 0.94. CAPM alpha was 0.61% (t 3.2)."
- **Tutor hooks.** Ids: `point:<portfolio>`, `line:capm`, `line:fit`, `slider:b`, `slider:s`, `slider:h`, `cell:<size>,<value>`, `readout:alpha`, `readout:grs`, `series:lambda`, `chip:<model>`. Secret: the planted factor structure.
- **Performance.** 25 regressions on $T \le 720$ months with at most 4 factors: under 1 ms each; Fama-MacBeth over 720 months with $N \le 1{,}000$: about 12M operations, under 50 ms in the worker.
- **Artifact and web.** Rehearsal data on both; Ken French files only on the web or locally (the learner downloads them).
- **Generators.** `alpha-from-means`, `grs-from-pieces`, `fm-slope`, `read-grid`, `fit-loadings`. Difficulty 2 to 5.
- **Misconceptions.** `alpha-is-skill-whatever-the-model`, `ff3-explains-momentum`, `loading-is-a-characteristic`, `fm-standard-errors-ignore-estimation`.

### 7.4 `pairs-lab`: Pairs lab

**Composite · P2 · H2.** Gatev, Goetzmann and Rouwenhorst's distance method: formation, trading, portfolios of pairs, and the comparison with cointegration.

- **Purpose.** Normalise each stock's total-return index to 1 at the start of a 12-month formation period; for every pair compute the sum of squared deviations $\text{SSD}_{AB} = \sum_t (P^A_t - P^B_t)^2$; take the pairs with the smallest SSD. In the next 6 months, open a position when the normalised spread exceeds two formation-period standard deviations (long the cheaper, short the dearer) and close when the prices cross, or at the end. Returns can be measured on committed capital (all selected pairs) or on capital employed (pairs that traded); executing one day late removes profits that were bid-ask bounce. The paper reports annualised excess returns of up to about 11% for its top pairs over 1962 to 2002 [recalled, unverified]. Comparison mode selects pairs by Engle-Granger cointegration instead (through `coint-lab`) and compares out of sample, including pairs that break.
- **Serves.** 3.1.4 L1 to L6, L8; cross-cluster 2.2.5 (cointegration, through `coint-lab`).
- **Uses.** `plot-2d` (normalised prices; the spread with bands; portfolio equity), `cell-grid` (the SSD matrix on the sequential ramp with ranks), `span-track` (trades as long and short spans), `marks` (`paths`, `band`, open and close markers), `slider` (formation and trading lengths, the opening threshold in standard deviations, number of pairs, cost per round trip), `drag-point` (open and close markers in task mode), `choice` (distance or cointegration; capital basis), `coint-lab` (comparison, extension), `sde-stepper` (half-life link), `sim-runner` (`panel`, daily pairs universe), `value-table`.
- **Interactions.**
  - Pointer: in formation mode scan the SSD matrix, tap cells to open pairs and tap the smallest-distance pairs; in trading mode drag markers to the opening and closing days of the focused pair (task) or watch them drawn; slide the threshold; toggle the one-day wait; switch capital basis; run the rolling portfolio; compare selection methods.
  - Keyboard: the matrix is a roving grid with Enter to open a pair; markers are sliders over days; sliders; chips.
- **State.** `{ mode: 'single' | 'formation' | 'trading' | 'portfolio' | 'compare'; formation: number; trading: number; threshold: number; topN: number; wait: boolean; basis: 'committed' | 'employed'; costBps: number; selected: string[]; focusedPair?: string; markers?: { open: number[]; close: number[] }; seed: number }`.
- **Answers and checks.** `numeric` (the SSD of a pair from a short normalised series; a trade's return; a portfolio's monthly return under each capital basis), `set` (the $k$ smallest-SSD pairs from a small matrix), `point` (the opening and closing days, tolerance zero days), `choice` (why the wait matters; which selection held up out of sample).
- **Config.**

```ts
interface PairsLabConfig {
  universe: { gen: 'panel-sim@1/pairs'; stocks: number; days: number; clusters: number; breaks: number; seed: number } | { csv: string };
  formationDays: number; tradingDays: number;
  threshold: number;                       // in formation standard deviations
  topN: number;
  wait: boolean; basis: 'committed' | 'employed'; costBps: number;
  mode: 'single' | 'formation' | 'trading' | 'portfolio' | 'compare';
  task?: 'pick-pairs' | 'ssd' | 'mark-trades' | 'trade-return' | 'portfolio-return' | 'explore';
}
```

- **Visual.** Normalised prices: stock A ink, stock B `--s6` dashed (shape as well as colour), the spread `--s2` with ±2 SD bands dashed ink; open markers `--s3` "+" for the long leg and `--s2` "−" for the short; the learner's markers `--manip`; the SSD matrix with the top pairs outlined; trades as spans below; equity `--s2` with periods banded. Answer objects: tapped cells, markers and fields.
- **Motion.** Direct. Show-why keys: `bounce` (with no wait, the trade's first-day return highlights as a bid-ask reversal); `broken-pair` (a pair that breaks keeps diverging past every band).
- **Reduced motion.** Static.
- **Accessibility.** The SSD matrix as a ranked table of pairs; trades as a table (open, close, legs, return); "Top 20 pairs, 6-month trading, committed capital: 0.71% a month before costs, 0.38% after 10 basis points per side."
- **Tutor hooks.** Ids: `cell:<a>,<b>`, `series:a`, `series:b`, `series:spread`, `band:upper`, `band:lower`, `marker:open:<k>`, `marker:close:<k>`, `span:trade:<k>`, `toggle:wait`, `chip:<basis>`, `slider:threshold`. Secret: the true clusters and break dates.
- **Performance.** SSD over 200 stocks (19,900 pairs) by 252 days: about 5M operations; the rolling portfolio over 10 years in the worker in under 300 ms.
- **Artifact and web.** No difference; real-data runs (with the survivorship caveat of section 0.3) are web or local.
- **Generators.** `ssd`, `pick-pairs`, `mark-trades` (spreads with one clean opening and closing), `trade-return`, `capital-basis`. Difficulty 2 to 4.
- **Misconceptions.** `ssd-pairs-are-cointegrated`, `same-day-execution`, `committed-equals-employed`, `pairs-never-break`.

### 7.5 `market-maker-sim`: Market-maker simulator

**Composite · P2 · H2.** Avellaneda and Stoikov's market maker: fill intensity, the reservation price, the optimal spread, inventory risk, and the model's blind spots.

- **Purpose.** A market maker earns the spread and carries inventory. In Avellaneda and Stoikov (2008), the mid-price follows $dS = \sigma\,dW$; a quote at distance $\delta$ from the mid is hit at rate $\lambda(\delta) = Ae^{-k\delta}$. A risk-neutral one-sided quoter maximises $\delta\lambda(\delta)$ at $\delta = 1/k$. With exponential utility and risk aversion $\gamma$, the paper's approximate solution centres quotes on the reservation price $r = s - q\gamma\sigma^2(T - t)$, which leans against inventory $q$, with total spread $\delta^a + \delta^b = \gamma\sigma^2(T - t) + \frac{2}{\gamma}\ln\left(1 + \frac{\gamma}{k}\right)$. Compared with a symmetric quoter using the same spread around the mid, the inventory strategy gives a slightly lower mean profit and a much smaller spread of profits and of terminal inventory [recalled, unverified as to the paper's figures; the simulator reproduces the pattern on fixed seeds]. The model leaves out adverse selection (informed traders), inventory limits (Guéant, Lehalle and Fernandez-Tapia 2013) and changing volatility; toggles add each. The stochastic control behind the formulas belongs to optional item 3.2, so the lessons give a derivation sketch only and say so.
- **Serves.** 3.1.5 L1 to L9; cross-cluster 3.3 (market-making games: play mode) and 1.7 (spreads and the order book, as a forward link).
- **Uses.** `plot-2d` (mid, reservation price and quotes over time; inventory; wealth; the intensity and profit curves; batch histograms), `marks` (`paths`, `step`, fill markers, `hist`, `curve`), `slider` ($\gamma$ on a log scale, $k$, $A$, $\sigma$, $T$, speed), `drag-point` ($q$ and $t$ handles in geometry mode; bid and ask handles in play mode; $\delta$ on the profit curve), `choice` (strategy chips), `sim-runner` (`as-market`), `live-formula`, `value-table`.
- **Interactions.**
  - Pointer: in live mode Play, Pause and Step a session and watch fills; in geometry mode drag inventory $q$ and time $t$ and watch $r$ and the spread move, and drag $\delta$ along the profit curve; in batch mode predict, then run 1,000 sessions per strategy; in play mode drag your own bid and ask while the session runs slowly; toggle informed flow, inventory limits and stochastic volatility.
  - Keyboard: Space plays or pauses; S steps; sliders; handles; in play mode B and A focus the bid and ask, arrows move them by one tick.
- **State.** `{ mode: 'live' | 'geometry' | 'batch' | 'play' | 'extensions'; params: { gamma: number; k: number; A: number; sigma: number; T: number; dt: number; s0: number }; strategy: 'as' | 'symmetric' | 'fixed' | 'learner'; q?: number; t?: number; delta?: number; toggles: { informed: boolean; limits: boolean; stochVol: boolean }; seed: number; prediction?: string }`.
- **Answers and checks.** `numeric` (the reservation price, for example $s = 100$, $q = 2$, $\gamma = 0.1$, $\sigma = 2$, $T - t = 0.5$ gives $r = 99.6$; the total spread, here $0.2 + 20\ln(1 + \frac{0.1}{1.5}) \approx 1.491$; the best one-sided $\delta = 1/k$), `point` ($\delta$ on the profit curve), `choice` (predict which strategy has the smaller spread of profits; what informed flow does), `ordering` (the effect of $\gamma$, $k$ and $\sigma$ on the spread), `code` (replicate the comparison with fixed seeds; the learner's script must match the reference outputs for the same seeds, which grades no random estimate).
- **Config.**

```ts
interface MarketMakerSimConfig {
  mode: 'live' | 'geometry' | 'batch' | 'play' | 'extensions';
  params: { gamma: number; k: number; A: number; sigma: number; T: number; dt: number; s0: number; q0: number };
  strategies: ('as' | 'symmetric' | 'fixed' | 'learner')[];
  batch?: { runs: number };
  extensions?: { informed?: { share: number; edge: number }; limits?: { qMax: number }; stochVol?: { volOfVol: number } };
  editable: ('gamma' | 'k' | 'A' | 'sigma' | 'T' | 'q' | 't' | 'delta' | 'quotes')[];
}
```

- **Visual.** The mid ink; the reservation price `--s6` dashed with an "r" label; bid and ask as step lines (bid `--s3` "B", ask `--s2` "A"); fills as triangles (a buy at the bid points up, a sell at the ask points down) with the same letters; inventory as an ink step series; wealth `--s2`; in play mode the learner's quotes `--manip` with handles; batch histograms: AS `--s2`, symmetric `--s6` dashed outline. Answer objects: handles in geometry and play tasks, and fields.
- **Motion.** Sessions run as data arriving at a chosen speed (default 20 steps a second). Show-why keys: `lean` (as $q$ tweens from 0 to 5 the quotes slide down together while the spread stays); `inventory-risk` (symmetric runs' terminal inventories spread wide beside AS's).
- **Reduced motion.** Sessions show their state on Pause and at the end only; play mode steps on key presses.
- **Accessibility.** Fills listed in a table (time, side, price, inventory after); "t = 0.42, mid 100.8, inventory +3, reservation price 100.1, quotes 99.4 and 100.8, wealth +12.3." Batch results as a table (mean and SD of profit, terminal inventory) per strategy.
- **Tutor hooks.** Ids: `series:mid`, `series:r`, `series:bid`, `series:ask`, `fill:<i>`, `series:inventory`, `series:wealth`, `handle:q`, `handle:t`, `handle:delta`, `handle:bid`, `handle:ask`, `hist:<strategy>`, `toggle:<ext>`, `slider:<param>`. Secret: the batch outcome while a prediction is pending.
- **Performance.** One session of 200 steps is trivial; the batch of 1,000 sessions per strategy under 30 ms in the worker. The fill probability $\lambda\,dt$ is clamped at 0.5 per side per step with a notice (decision 14); at the paper's settings [recalled, unverified: $s_0 = 100$, $T = 1$, $\sigma = 2$, $dt = 0.005$, $\gamma = 0.1$, $k = 1.5$, $A = 140$] typical quotes give $\lambda\,dt$ near 0.3.
- **Artifact and web.** No difference. The replication drill (NumPy) is implement-it tier.
- **Generators.** `reservation-price`, `optimal-spread`, `best-delta`, `sensitivity-order`, `predict-batch` (parameter sets where the SD ratio between strategies exceeds 1.5). Difficulty 2 to 4.
- **Misconceptions.** `quote-around-the-mid`, `wider-spread-is-always-safer`, `inventory-is-free`, `no-informed-traders`.

### 7.6 `replication-workbench`: Replication workbench

**Composite · P2 · H1 (read, table, ledger, compare) and H2 (decay, note).** Read a paper, record every choice, compare your numbers, measure what survived, and write the note.

- **Purpose.** The 3.1 method in one place.
  - **Read.** A paper card (our own summary, never the paper's text: question, data, sample, method, main claim, with SSRN or DOI identifiers as copyable text) and a "paper map" task.
  - **Table.** The main results table recreated as data, every cell addressable and explainable (coefficient, $t$ in parentheses, Newey-West or not, stars). Published figures carry the [recalled, unverified] flag until the content team verifies them against the paper, and are never an answer key before that (decision 9).
  - **Ledger.** Every choice that can move the number (universe and exchange filters, sample dates, price and share filters, weighting, rebalancing dates, the skip month, return frequency, delisting returns, costs, standard errors) with the paper's stated value or "not stated", the learner's value and a reason.
  - **Compare.** The learner's results (from `portfolio-sort`, `factor-model-lab`, `pairs-lab` or `market-maker-sim`, or pasted from their own code) cell by cell against the rehearsal truth or their reference computation, with differences and tolerance bands.
  - **Decay.** The strategy's returns split into in-sample, post-sample and post-publication periods. "How much survived" is defined as the survival ratio $\hat\rho = \frac{\bar r_{\text{post}}}{\bar r_{\text{in}}}$ with a delta-method interval, $\mathrm{Var}(\hat\rho) \approx \frac{\mathrm{Var}(\bar r_{\text{post}})}{\bar r_{\text{in}}^2} + \frac{\bar r_{\text{post}}^2\,\mathrm{Var}(\bar r_{\text{in}})}{\bar r_{\text{in}}^4}$, using Newey-West variances [our choice]. When the in-sample $t$ is below 2 the ratio is unstable, so the widget reports the difference in means with its interval instead and says why. The many-anomalies view repeats this across planted anomalies, the picture McLean and Pontiff and Hou, Xue and Zhang draw [recalled, unverified as to their figures].
  - **Note.** A results note against a 10-point rubric (what was replicated, what differed and why, how much survived with its interval, what failed, data provenance and survivorship), self-marked with a Bertie draft at the `complex` tier, and defended in `viva`.
- **Serves.** 3.1.1 L1 to L5; 3.1.2 L10; 3.1.3 L9; 3.1.4 L8; 3.1.5 L8; 3.1.6 L7, L8; cross-cluster 2.3 (results notes).
- **Uses.** `value-table` (the results table and the ledger), `cell-grid` (difference grid with tolerance colouring on answer cells only), `span-track` (the three periods as bands), `plot-2d` and `marks` (period means with intervals; cumulative returns), `card-sort` (paper map), `free-response` (note and reasons), `viva` (link), `setup-checklist` (project mode, extension), `code-cell` (paste or run), `summary-table` (link for regression tables).
- **Interactions.**
  - Pointer: match questions to paper sections; tap any table cell to open its explanation; fill ledger rows; paste or link results; drag the period boundaries if the paper's dates are not fixed; write the note; open the viva.
  - Keyboard: tables are roving grids; ledger fields are form controls; period boundaries are sliders; standard text editing in the note.
- **State.** `{ paper: string; mode: 'read' | 'table' | 'ledger' | 'compare' | 'decay' | 'note'; mapping?: Record<string, string>; ledger: Record<string, { value: string; reason: string }>; results?: Record<string, number>; periods?: { inEnd: number; pub: number }; note?: string; selfMark?: number[] }`. Under 64 KB, saved to `db` in the Artifact.
- **Answers and checks.** `mapping` (paper map), `numeric` ($t$ from coefficient and standard error; the survival ratio from shown means), `interval` (its delta-method interval), `set` (choices the paper leaves unstated), predicate `ledger-complete`, `free-text` (the note), `code` (the learner's replication tests on web or local).
- **Config.**

```ts
interface ReplicationWorkbenchConfig {
  paper: 'jt1993' | 'ff1993' | 'ggr2006' | 'as2008' | 'hlz2016' | string;
  card: { question: string; data: string; sample: string; method: string; claim: string; ids: string[] };
  table?: { rows: string[]; cols: string[]; cells: Record<string, { value: number; t?: number; verified: boolean }> };
  ledger: { field: string; paperValue: string | 'not stated'; options?: string[] }[];
  compareTo: 'rehearsal-truth' | 'reference-computation' | 'published-verified';
  periods?: { inSampleEnd: string; publication: string };
  rubric: { point: string; marks: number }[];
  mode: 'read' | 'table' | 'ledger' | 'compare' | 'decay' | 'note';
}
```

- **Visual.** The table in the paper's layout with $t$ in parentheses, unverified cells marked with a small "unverified" tag; ledger rows with "not stated" in `--text-muted`; compare cells in the answer state only (green or amber outline and a badge on the learner's cells), never on the paper's; period bands per section 2.6 with means as ink dots and intervals as whiskers; the survival ratio as a large readout with its interval. Answer objects: the learner's values, ledger rows and the note.
- **Motion.** Period boundary drags are direct. Show-why keys: `unstable-ratio` (the interval of the ratio widens dramatically as the in-sample mean tweens towards zero); `unstated-choice` (two values of an unstated choice produce visibly different table cells).
- **Reduced motion.** Static.
- **Accessibility.** All tables are real tables; "Momentum 6-1-6 on rehearsal data: in-sample 0.94% a month (t 4.4); post-publication 0.41% (t 1.6). Survival ratio 0.44, 95% interval 0.05 to 0.83."
- **Tutor hooks.** Ids: `cell:<row>,<col>`, `ledger:<field>`, `band:in-sample`, `band:post-sample`, `band:post-publication`, `readout:ratio`, `note`, `rubric:<k>`. Secret: rehearsal truth (planted premium and decay). Bertie reviews the note at the `complex` tier on request, after the learner's self-mark.
- **Performance.** Tables and ledgers are small; the decay panel runs `backtest-core` on the item's strategy in under 50 ms.
- **Artifact and web.** All modes in both; pasting results works everywhere; running real-data code is web or local; the note exports through `downloads` (Artifact) or a Blob link (web).
- **Generators.** Seeds vary rehearsal panels (planted premia, decay and publication dates) per learner; item generators `t-from-coef` (from rehearsal tables), `survival-ratio` (ratio and interval from shown means and variances) and `unstated-choices`. Difficulty 2 to 4.
- **Misconceptions.** `replication-equals-reproduction`, `in-sample-equals-out-of-sample`, `unstated-choices-do-not-matter`, `published-number-is-the-truth`.

---
## 8. Screens built from primitives alone

Some ideas need no composite: a plot, a slider, a live formula and at most one `sim-runner` model carry them. Each is screen data, with no widget-specific code.

### 8.1 The curse of dimensionality (2.1.1 L7)

- **Act.** Slide the dimension $p$ from 1 to 50. Panel one plots the edge length of a sub-cube holding a fraction $r$ of a uniform unit cube, $e_p(r) = r^{1/p}$, with a `--manip` point at the current $p$; at $p = 10$ and $r = 0.1$ the edge is $0.1^{0.1} \approx 0.794$ of the full width. Panel two is a histogram of $\frac{d_{\min}}{d_{\max}}$ (nearest over farthest neighbour distance from a query) for 500 uniform points, which crowds towards 1 as $p$ grows.
- **Primitives.** `plot-2d` (two panels), `slider` ($p$, $r$), `marks` (`curve`, `hist`), `live-formula`, `sim-runner` (`nn-distance`, section 4).
- **Check.** `numeric` on $e_p(r)$ with relative tolerance 0.5%.

```json
{ "widgets": [
  { "type": "plot-2d", "id": "edge", "x": { "min": 1, "max": 50, "label": "dimension p" }, "y": { "min": 0, "max": 1, "label": "edge for 10% of the data" },
    "marks": [ { "type": "curve", "expr": "r^(1/x)", "vars": { "r": 0.1 }, "role": "derived" } ] },
  { "type": "slider", "id": "p", "min": 1, "max": 50, "step": 1, "bind": "edge.cursor.x" },
  { "type": "plot-2d", "id": "ratio", "x": { "min": 0, "max": 1, "label": "nearest / farthest distance" },
    "marks": [ { "type": "hist", "source": { "sim": "nn-distance", "n": 500, "p": "@p" } } ] } ],
  "check": { "kind": "numeric", "value": "0.1^(1/10)", "tol": { "rel": 0.005 } } }
```

### 8.2 The 0.632 limit (2.1.3 L9)

- **Act.** Slide $n$ and watch $1 - (1 - \frac{1}{n})^n$, the chance a given row appears in a bootstrap sample, settle on $1 - e^{-1} \approx 0.632$, drawn as a dashed asymptote.
- **Primitives.** `plot-2d` (log $x$), `slider` (discrete $n$ list), `marks` (`stems`, dashed line), `live-formula`.
- **Check.** `numeric` (the limit; or the value at a stated $n$).

### 8.3 The Bonferroni hurdle on a $t$ axis (3.1.6 L2)

- **Act.** Slide the number of tests $M$ on a log scale from 1 to 10,000 and watch the two-sided 5% hurdle $\Phi^{-1}(1 - \frac{0.025}{M})$ climb from 1.96 past 3 near $M = 20$ (about 3.02) to about 3.76 at $M = 300$.
- **Primitives.** `plot-2d` (log $x$), `slider`, `marks` (`curve`, a horizontal line at 3 labelled), `live-formula`.
- **Check.** `numeric` (the hurdle at a stated $M$, tolerance 0.01).

---

## 9. Generators

Practice, quizzes, homework and exams need many instances of each item. This cluster follows the sibling rule (calc-linalg section 2.12): a generator is a pure function `make(seed, difficulty)` returning a widget config, a check, a worked solution and the misconceptions its distractors encode, and each ships with a property test over 1,000 seeds.

**Rules this cluster adds** [our choice]:

1. **Truth first.** Choose the answer's shape first (planted coefficients, a unique best split, a clean barrier touch, a planted premium), then build the data around it.
2. **Margins proven in CI** (section 2.3, rules 2 to 4). Every selection item's best setting is unique by the stated margin; every "predict, then run" item's qualitative outcome holds on every generated instance; every deterministic-run threshold sits the stated margin below the reference run.
3. **No ties.** Distances, thresholds, barrier touches, ranks and SSDs are generated tie-free: rejection with a bounded retry count, then a deterministic nudge of the offending value by a stated amount.
4. **Exact where countable.** Counts give rationals (Gini, precision, recall, AUC by pairs, uniqueness, concurrency), checked with the shared `rational` service.
5. **Fixed data are shown.** Every number a learner computes from is on screen or in the table view.
6. **Story variety.** Quant contexts (returns, defaults, fills, trades, factors) alternate with general ones (screening, spam, churn), so practice tests the idea rather than the wording.
7. **Versioned.** Generator ids carry the major version of the data service they call (section 2.1, requirement 9).

| Widget | Generator ids | What varies | Answer computed by | Difficulty |
|---|---|---|---|---|
| `fit-explorer` | `knn-predict`, `pick-the-winner`, `best-degree`, `snr-ceiling` | truth, $n$, $\sigma$, query point | exact neighbours; QR fits; margin rule | 1 to 3 |
| `loss-lab` | `minimiser`, `huber`, `pinball`, `margin-match` | data, outlier, $\delta$, $\tau$ | order statistics; IRLS to $10^{-12}$ | 1 to 3 |
| `error-curves` | `shape`, `one-se` | host model family, noise | host's exact curves; margin rule | 2 to 4 |
| `bias-variance-lab` | `rank-variance`, `rank-bias`, `table-compute`, `decompose` | truth, models, $x_0$ | smoother-matrix theory; shown table | 2 to 4 |
| `logistic-lab` | `p-at-x`, `odds-ratio`, `log-loss`, `fit-by-hand`, `softmax` | $w$, $b$, data, logits | closed forms; Newton MLE | 1 to 3 |
| `classifier-plane` | `which-model`, `support-vectors`, `knn-vote`, `paint-region` | data shape, models, query | `ml-core`; SMO to $10^{-6}$ | 2 to 4 |
| `threshold-lab` | `counts-to-metrics`, `pair-auc`, `bayes-threshold`, `profit-threshold`, `imbalance-precision` | scores, base rate, costs | exact rationals; closed forms | 1 to 4 |
| `calibration-lab` | `brier`, `kelly`, `ldp-size`, `read-diagram` | forecasts, odds, distortion | closed forms | 2 to 4 |
| `feature-builder` | `encode-rows`, `count-columns`, `rank`, `find-leaks` | columns, levels, planted leaks | `frame-core`; exact rank | 1 to 4 |
| `basis-lab` | `df-count`, `place-knots`, `match-family` | family, knots, truth | column counts; least squares | 2 to 4 |
| `cv-lab` | `cv-estimate`, `which-rows`, `assign-stratified`, `loocv-shortcut`, `rank-estimates` | fold errors, $k$, classes | exact arithmetic; hat values | 1 to 4 |
| `tuning-lab` | `grid-vs-random`, `optimism`, `find-optimum` | analytic surface, budget | analytic optimum; $E[\max]$ formula | 2 to 4 |
| `regularisation-path` | `ridge-1d`, `ridge-df`, `lasso-active-set`, `lambda-1se`, `criteria`, `stepwise-next` | design, sparsity, correlation | closed forms; coordinate descent to $10^{-10}$; margin rule | 2 to 5 |
| `penalty-geometry` | `predict-contact`, `soft-threshold`, `match-thresholds`, `budget-to-lambda` | OLS point, correlation, budget | exact KKT solutions | 2 to 4 |
| `split-scorer` | `gini-node`, `entropy-node`, `split-gain`, `best-threshold`, `criterion-prefers`, `xgb-gain` | counts, values, $\lambda$, $\gamma$ | exact rationals (Gini); enumeration | 1 to 4 |
| `tree-builder` | `build-small-tree`, `leaf-predict`, `prune-count`, `trace-path` | boxes, depth, $\alpha$ | exact greedy CART; weakest link | 1 to 4 |
| `ensemble-lab` | `variance-formula`, `oob-probability`, `rank-settings` | $\rho$, $\sigma^2$, $B$, $n$ | closed forms; fixed tables | 2 to 4 |
| `boosting-lab` | `next-stump`, `residual-after`, `adaboost-weights`, `pseudo-residual`, `early-stop` | data, $\nu$, loss | exact stump search; closed forms | 2 to 4 |
| `importance-lab` | `rank-by-method`, `id-trap`, `twin-effect`, `shapley-toy` | feature roles, twin correlation | deterministic runs with margins; exact Shapley | 2 to 5 |
| `cluster-lab` | `assign-step`, `update-step`, `merge-order`, `corr-distance`, `cut-clusters` | points, linkage, correlations | exact arithmetic | 1 to 4 |
| `nn-playground` | `param-count`, `predict-effect`, `hand-set-xor`, `regions-count` | architecture, settings | closed forms; deterministic runs with margins | 2 to 4 |
| `relu-composer` | `output-at-x`, `count-pieces`, `approximate` | units, target | closed forms; CI best-$m$ error | 2 to 4 |
| `sequence-filter` | `output-at-t`, `ewma-weight`, `name-the-filter`, `match-kernel` | kernel, series, $\alpha$ | closed forms | 1 to 3 |
| `time-cv-lab` | `purge-set`, `embargo-set`, `train-rows`, `cpcv-count`, `assemble-path`, `predict-score` | spans, $k$, $N$, embargo | exact overlap rule; binomials; margin rule | 2 to 5 |
| `leakage-detective` | `leak-catalogue`, `pipeline-order`, `survivorship-bias`, `audit-study` | features, timings, studies | planted labels; exact panel computation | 2 to 5 |
| `labelling-lab` | `first-touch`, `label-value`, `cusum-events`, `uniqueness`, `bootstrap-prob`, `meta-precision` | paths, barriers, spans | forward scans; exact rationals | 2 to 5 |
| `bar-sampler` | `build-bars`, `count-bars`, `ohlc` | trade lists, thresholds | one-pass aggregation | 1 to 3 |
| `fracdiff-lab` | `weights`, `min-d`, `meaning-of-d` | $d$, series | recursion; ADF on a grid with margin | 2 to 4 |
| `sharpe-lab` | `se`, `annualise`, `psr`, `mintrl`, `dsr-benchmark`, `haircut`, `which-is-convincing` | SR, $T$, moments, $N$, $M$ | closed forms (`sharpe-stats`) | 2 to 5 |
| `overfit-lab` | `emax`, `cscv-count`, `pbo-from-counts`, `minbtl`, `predict-oos`, `trust-region` | $N$, $S$, target, sweeps | closed forms; planted edges | 2 to 5 |
| `portfolio-sort` | `wml-from-table`, `portfolio-return`, `smb-hml`, `cohort-average`, `history-needed`, `top-decile`, `breakpoints` | panels, windows, stocks | exact arithmetic on shown data | 1 to 4 |
| `signal-lab` | `rank-ic-by-hand`, `fundamental-law`, `net-return`, `ic-t`, `fix-the-expression` | ranks, IC, breadth, costs | exact ranks; closed forms | 2 to 4 |
| `factor-model-lab` | `alpha-from-means`, `grs-from-pieces`, `fm-slope`, `read-grid`, `fit-loadings` | factor means, loadings, panels | closed forms; `tests` service | 2 to 5 |
| `pairs-lab` | `ssd`, `pick-pairs`, `mark-trades`, `trade-return`, `capital-basis` | normalised series, thresholds | exact arithmetic | 2 to 4 |
| `market-maker-sim` | `reservation-price`, `optimal-spread`, `best-delta`, `sensitivity-order`, `predict-batch` | $\gamma$, $k$, $\sigma$, $q$, $T - t$ | closed forms; margin rule | 2 to 4 |
| `replication-workbench` | `t-from-coef`, `survival-ratio`, `unstated-choices` | rehearsal tables, periods | closed forms; delta method | 2 to 4 |

**Not generated:** `ml-workbench` (seeds vary each learner's data and planted leaks) and `viva` (a seeded draw from an authored bank). **Extensions to sibling generators:** `multiple-testing` gains `bhy-set` and `hurdle-at-m`; `regression-lab` gains `nw-se` (overlapping returns with a stated lag); `contingency-table` gains `confusion-metrics`; `posterior-lab` gains `map-lambda`; `descent-lab` gains `adam-step` (one Adam update by hand); `dependency-graph` gains `fill-gradient`.

---

## 10. Misconception register

Each misconception has an id, the wrong belief, the verdict-chip line (at most 20 words) and the show-why that answers it. Widgets list ids; this table holds the text. Lines are written in the design research's voice.

| Id | Widget | Wrong belief | Verdict line | Show-why |
|---|---|---|---|---|
| `lower-train-error-is-better` | `fit-explorer` | The curve closest to the training points is the best model | Close to the points you have; far from the points you will get. | `fresh-points` |
| `test-set-reuse-is-harmless` | `fit-explorer` | Choosing by test score still leaves an honest test score | You chose with these points, so they now flatter you. | `fresh-points` |
| `high-r2-expected-in-finance` | `fit-explorer` | A good return model explains much of the variance | Here the truth explains 1%. Anything above that is noise. | `fresh-points` |
| `k1-is-best` | `fit-explorer`, `classifier-plane` | One neighbour uses the most local information | One neighbour copies its noise into every prediction. | `neighbours` |
| `mean-minimises-absolute-loss` | `loss-lab` | Any sensible loss is minimised at the mean | Absolute loss is minimised at the median. | `outlier-pull` |
| `squared-loss-is-neutral` | `loss-lab` | Squared loss treats every point fairly | One big miss has a big square; it drags the answer. | `outlier-pull` |
| `zero-one-is-trainable` | `loss-lab` | Minimise the error count directly | The error count is flat almost everywhere: no slope to follow. | none |
| `test-error-falls-forever` | `error-curves` | More flexibility keeps improving test error | Training error keeps falling; test error turns up. | `gap-opens` |
| `pick-the-minimum-always` | `error-curves` | Always take the lowest CV point | Within one standard error, prefer the simpler model. | none |
| `train-error-falls-with-n` | `error-curves` | More data lowers training error | More rows are harder to fit: training error rises towards the test error. | none |
| `bias-means-unfair` | `bias-variance-lab` | Bias is prejudice in the data | Here bias is how far the average fit misses the truth. | `average-misses` |
| `variance-is-the-noise` | `bias-variance-lab` | Variance is the noise in $y$ | Variance is how much the fits disagree with each other. | `fan-out` |
| `flexible-models-have-low-variance` | `bias-variance-lab` | Flexible models are more reliable | Flexible fits chase each sample: they disagree most. | `fan-out` |
| `more-data-cures-bias` | `bias-variance-lab` | Enough data fixes a straight line on a curve | More data shrinks variance. A line still cannot bend. | `average-misses` |
| `probability-linear-in-x` | `logistic-lab` | Each unit of $x$ adds the same probability | Each unit multiplies the odds by $e^w$. | none |
| `squared-loss-for-probabilities` | `logistic-lab` | Fit probabilities by squared error | Log loss punishes confident mistakes hardest. Look at this bar. | `log-loss-explodes` |
| `separable-is-easy` | `logistic-lab` | Perfectly separated classes give the best fit | Separated data have no best slope: the likelihood keeps rising. | `separation` |
| `softmax-is-argmax` | `logistic-lab` | Softmax picks the largest logit | Softmax gives every class a share; temperature sets how sharp. | none |
| `linear-model-cannot-curve` | `classifier-plane` | A linear model draws a straight boundary | Linear in its features. Square a feature and the boundary bends. | none |
| `boundary-follows-the-points` | `classifier-plane` | The boundary passes near the points | It sits where the model's probability is one half. | `bayes-gap` |
| `svm-uses-all-points` | `classifier-plane` | Every point moves an SVM's boundary | Only the support vectors matter. Move another point: nothing changes. | `margin` |
| `accuracy-is-enough` | `threshold-lab` | 99% accuracy is excellent | Predicting "no" for everyone scores 99% here. | `base-rate` |
| `threshold-must-be-half` | `threshold-lab` | Classify at 0.5 | The best threshold depends on the costs and the base rate. | none |
| `roc-hides-base-rate-so-its-fine` | `threshold-lab` | An unchanged ROC means unchanged usefulness | The ROC did not move. Precision fell to 0.12. | `base-rate` |
| `auc-measures-calibration` | `threshold-lab` | High AUC means honest probabilities | AUC only ranks. Squash every score and it stays the same. | `pair-count` |
| `high-auc-means-calibrated` | `calibration-lab` | A good ranker gives honest probabilities | This model ranks well and says 0.9 when it means 0.7. | `overconfident` |
| `isotonic-on-test-data` | `calibration-lab` | Recalibrate on the test set | Fit the calibration on its own split, or the test score lies. | none |
| `bet-more-when-unsure` | `calibration-lab` | Uncertainty is a reason to bet big | Size falls as the probability nears one half. | `kelly-overbet` |
| `brier-is-accuracy` | `calibration-lab` | Brier score counts right answers | Brier scores the probabilities, not the decisions. | none |
| `dummy-for-every-level-with-intercept` | `feature-builder` | One column per level, plus an intercept | Those columns add up to the intercept: the matrix is singular. | `dummy-trap` |
| `scale-on-all-data` | `feature-builder` | Fit the scaler once on everything | The scaler has seen the test rows. Fit it on training rows. | none |
| `centred-window-is-fine` | `feature-builder`, `sequence-filter` | A centred average is a smoother average | It uses tomorrow's value. | `future-leak` |
| `target-encoding-is-free` | `feature-builder` | Encode a category by its mean target | Each row's own label is inside its encoding. | none |
| `more-knots-always-better` | `basis-lab` | More knots, better fit | More knots fit the noise too. | none |
| `polynomials-behave-at-edges` | `basis-lab` | A high-degree polynomial extrapolates calmly | Look past the data: it swings. | `wild-ends` |
| `spline-is-one-polynomial` | `basis-lab` | A spline is a single polynomial | A spline is pieces joined smoothly at the knots. | `sum-of-parts` |
| `validation-split-is-stable` | `cv-lab` | One split gives the answer | Another split, another answer. Average over folds. | none |
| `cv-score-of-tuned-model-is-unbiased` | `cv-lab` | The best CV score is the expected score | You picked the best of many noisy scores. | `same-folds` |
| `select-features-then-cv` | `cv-lab` | Select features first, then cross-validate | The selection saw every label. This is pure noise. | `peeked-labels` |
| `loocv-is-always-best` | `cv-lab` | Leave-one-out uses the most data, so it is best | Its estimate can swing more than 10-fold's. | none |
| `grid-search-is-thorough` | `tuning-lab` | A grid covers the space | Nine grid points try three values of the axis that matters. | `projected` |
| `best-cv-score-is-the-expected-score` | `tuning-lab` | The winning score will repeat | The winner was lucky as well as good. | none |
| `tune-on-test` | `tuning-lab` | Tune on the test set to save data | Then nothing is left to test with. | none |
| `ridge-sets-coefficients-to-zero` | `regularisation-path`, `penalty-geometry` | Ridge removes features | Ridge shrinks; only the lasso's corners give exact zeros. | `shrink-not-zero` |
| `lasso-picks-the-true-feature` | `regularisation-path` | The lasso finds the true one of two twins | Resample: it picks either twin. | `twin-swap` |
| `no-need-to-standardise` | `regularisation-path` | Penalties ignore units | Change units and the penalty changes its mind. | `unit-change` |
| `lambda-from-test-set` | `regularisation-path` | Choose $\lambda$ on the test set | Choose it by cross-validation; keep the test set for last. | none |
| `stepwise-p-values-are-valid` | `regularisation-path` | p-values after stepwise selection mean what they say | Selection used the same data; the p-values are too small. | none |
| `lasso-shrinks-proportionally` | `penalty-geometry` | The lasso scales coefficients down | It subtracts a fixed amount and stops at zero. | `corner-contact` |
| `constraint-and-penalty-differ` | `penalty-geometry` | A budget and a penalty are different methods | Each budget matches a penalty. Same solutions. | none |
| `misclassification-error-for-splitting` | `split-scorer` | Split to reduce the error count | These two splits tie on errors; Gini sees that one makes a pure node. | `chord` |
| `split-at-a-data-value` | `split-scorer` | Thresholds sit on data values | Thresholds sit halfway between neighbouring values. | none |
| `gini-is-error-rate` | `split-scorer` | Gini is the misclassification rate | Gini is the chance two random draws disagree. | none |
| `deeper-tree-is-better` | `tree-builder` | Grow until every leaf is pure | Pure leaves memorise. Look at the held-out points. | `prune-fold` |
| `trees-are-stable` | `tree-builder` | Similar data give similar trees | Resample once: a different root split. | `instability` |
| `tree-splits-diagonally` | `tree-builder` | A tree can cut at any angle | Each split is one feature against one threshold. | none |
| `bagging-reduces-bias` | `ensemble-lab` | Averaging trees fixes their bias | Averaging cuts variance; the average of biased trees stays biased. | none |
| `more-trees-overfit` | `ensemble-lab` | Too many trees overfit a forest | The forest's error flattens. Extra trees cost time, not accuracy. | `floor` |
| `oob-needs-a-holdout` | `ensemble-lab` | OOB error needs separate data | Each tree never saw a third of the rows. | none |
| `boosting-rounds-cannot-overfit` | `boosting-lab` | Boosting keeps improving | Validation error has turned up. Stop earlier. | `overshoot` |
| `bigger-learning-rate-is-better` | `boosting-lab` | Large steps learn faster and better | Large steps chase noise. Small steps and more rounds generalise. | `overshoot` |
| `boosting-averages-like-bagging` | `boosting-lab` | Boosting averages independent trees | Each tree fits what the last ones missed. | `residual-shrink` |
| `mdi-is-reliable` | `importance-lab` | Impurity importance is trustworthy | It crowned a random ID column. | `id-crown` |
| `importance-means-causation` | `importance-lab` | An important feature causes the outcome | Importance says the model uses it, not that it matters in the world. | none |
| `low-mda-means-useless` | `importance-lab` | Low permutation importance means no signal | Its twin carries the same signal. | `twin-split` |
| `kmeans-finds-the-true-clusters` | `cluster-lab` | k-means finds the real groups | A different start, a different answer. | `bad-start` |
| `elbow-is-objective` | `cluster-lab` | The elbow tells you $k$ | This curve has no clear elbow. $k$ is a choice. | none |
| `correlation-is-a-distance` | `cluster-lab` | Correlation is a distance | Distance falls as correlation rises: use $\sqrt{\frac{1}{2}(1 - \rho)}$. | none |
| `linear-activations-add-power` | `nn-playground` | More linear layers, more power | Linear layers collapse into one. The boundary stays straight. | `collapse` |
| `high-learning-rate-trains-faster` | `nn-playground`, `descent-lab` | Bigger steps reach the bottom sooner | Past $2/\lambda_{\max}$ the steps overshoot and grow. | `diverge` |
| `more-units-always-better` | `nn-playground` | Bigger networks are better | On 50 points, a big network memorises. | none |
| `zero-initialisation-is-fine` | `nn-playground` | Start all weights at zero | Identical units learn identical things. | none |
| `relu-is-linear` | `relu-composer` | ReLU is just a line | It bends once, at its kink. Sums of bends make curves. | `kink-adds-a-bend` |
| `width-equals-depth` | `relu-composer` | Units count the same in any arrangement | Stacked, the pieces multiply. | `sawtooth` |
| `rnn-has-no-memory-decay` | `sequence-filter` | A recurrent state remembers equally | Old inputs fade by $\alpha^k$. | none |
| `attention-is-magic` | `sequence-filter` | Attention is not a weighted average | It is one: softmax weights over the past. | none |
| `gradient-from-one-path` | `dependency-graph` | Take the gradient along one path | Where paths fork, gradients add. | `fork-sum` |
| `shuffled-kfold-is-fine-for-time-series` | `time-cv-lab` | Shuffled folds work for any data | Each test day has its neighbours in training. | `shuffled-neighbours` |
| `purge-only-after-test` | `time-cv-lab` | Purge only labels after the test fold | Labels that start before the test fold can still end inside it. | `leak-path` |
| `walk-forward-needs-no-purge` | `time-cv-lab` | Training on the past needs no purging | The last training labels still end in the test window. | `leak-path` |
| `embargo-is-optional` | `time-cv-lab` | Purging is enough | Features just after the test fold still carry its information. | none |
| `scaler-on-full-data-is-harmless` | `leakage-detective` | Scaling is too small a step to leak | The scaler's mean included the test rows. | `fitted-on-test` |
| `close-price-is-known-at-the-close` | `leakage-detective` | Use today's close to trade today | The close is known after the close. | `known-later` |
| `survivors-represent-the-market` | `leakage-detective` | Today's stocks are a fair sample of the past | The failures are missing, and so are their losses. | none |
| `restated-data-is-what-you-knew` | `leakage-detective` | Database values are what was known then | This number was revised months later. | `known-later` |
| `horizon-return-tells-the-story` | `labelling-lab` | The return at the horizon says how the trade went | This path hit −8% before ending at +1%. | `first-touch` |
| `overlapping-labels-are-independent` | `labelling-lab` | Each label is a separate observation | These labels share most of their days. | none |
| `stop-loss-is-free` | `labelling-lab` | A tight stop only removes losses | Tight stops also cut trades that would have recovered. | `first-touch` |
| `time-bars-are-neutral` | `bar-sampler` | Clock time is the natural sampling | Markets are busier at the open and close. | `busy-hours` |
| `volume-bar-has-fixed-duration` | `bar-sampler` | Every volume bar lasts the same time | Busy hours fill a bar in minutes. | `busy-hours` |
| `fracdiff-d-one-is-best` | `fracdiff-lab` | Returns are the right transform | $d = 1$ passes the test and throws the memory away. | `memory-kept` |
| `stationary-means-no-memory` | `fracdiff-lab` | Stationary series forget the past | This one is stationary and 0.9 correlated with the price. | `memory-kept` |
| `sharpe-is-exact` | `sharpe-lab` | The backtest's Sharpe ratio is the strategy's | Three years leave an error of about 0.6. | `wide-error` |
| `annualise-by-sqrt-always` | `sharpe-lab` | Multiply by $\sqrt{12}$ | Autocorrelated returns break the square-root rule. | none |
| `fat-tails-do-not-matter` | `sharpe-lab` | Skew and kurtosis do not change confidence | Negative skew and fat tails widen the error. | none |
| `deflation-only-for-many-trials` | `sharpe-lab` | Deflation matters only for huge searches | Ten trials already raise the hurdle. | `luck-line` |
| `best-backtest-is-skill` | `overfit-lab` | The top strategy of many has an edge | Every strategy here is noise. The winner was the luckiest. | `winner-regresses` |
| `more-trials-more-confidence` | `overfit-lab` | Testing more ideas makes the winner more trustworthy | More trials raise the luck you must beat. | `winner-regresses` |
| `spike-is-the-best-parameter` | `overfit-lab` | Use the single best cell | Its neighbours are poor: the spike is luck. | `spike-vs-plateau` |
| `leaderboard-is-the-test-set` | `overfit-lab` | The public score measures generalisation | You tuned on it 100 times. | none |
| `holdout-peeking-is-harmless` | `ml-workbench` | A quick look at the hold-out costs nothing | Each look turns the hold-out into validation data. | none |
| `unlogged-trials-do-not-count` | `ml-workbench` | Only the final model's trial counts | Every trial raises the luck benchmark. | none |
| `momentum-means-buying-last-month` | `portfolio-sort` | Momentum buys last month's winners | Last month tends to reverse; momentum skips it. | `skip-month` |
| `skip-month-is-optional` | `portfolio-sort` | The skip month is a detail | Without it, short-term reversal eats the premium. | `skip-month` |
| `equal-and-value-weights-agree` | `portfolio-sort` | Weighting does not change the result | Equal weights lean on small stocks. | none |
| `breakpoints-from-all-stocks` | `portfolio-sort` | Breakpoints use every stock | Many tiny stocks would crowd the small portfolios; use NYSE breakpoints. | none |
| `high-ic-means-profitable` | `signal-lab` | A high IC guarantees profit | This signal's turnover costs more than it earns. | `cost-drag` |
| `turnover-is-free` | `signal-lab` | Trading costs are a rounding error | At 38% a month, 20 basis points halve the net return. | `cost-drag` |
| `delay-zero-is-fine` | `signal-lab` | Use today's data to trade today | Today's close was not known when you traded. | `delay-leak` |
| `breadth-is-number-of-stocks` | `signal-lab` | Breadth is the number of names | Breadth counts independent bets. | none |
| `alpha-is-skill-whatever-the-model` | `factor-model-lab` | A positive alpha proves skill | Add the factors and the alpha shrinks. | `alphas-fade` |
| `ff3-explains-momentum` | `factor-model-lab` | Three factors explain momentum | WML's three-factor alpha is still large. | none |
| `loading-is-a-characteristic` | `factor-model-lab` | A stock's HML loading is its book-to-market | The loading is a regression slope, not a ratio. | none |
| `fm-standard-errors-ignore-estimation` | `factor-model-lab` | Fama-MacBeth $t$ needs no correction | The loadings were estimated; the errors are understated. | none |
| `ssd-pairs-are-cointegrated` | `pairs-lab` | Close pairs share a long-run link | Close in this window; this pair breaks next year. | `broken-pair` |
| `same-day-execution` | `pairs-lab` | Trade at the signal's price | That price includes the bid-ask bounce. | `bounce` |
| `committed-equals-employed` | `pairs-lab` | Return is return | Idle pairs dilute committed capital. | none |
| `pairs-never-break` | `pairs-lab` | A good pair stays a pair | This one never comes back. | `broken-pair` |
| `quote-around-the-mid` | `market-maker-sim` | Centre the quotes on the mid | Long inventory: centre lower, to sell. | `lean` |
| `wider-spread-is-always-safer` | `market-maker-sim` | Wider spreads cut risk | Wider spreads cut fills and profit too. | none |
| `inventory-is-free` | `market-maker-sim` | Inventory is just a number | Inventory carries the mid's risk. | `inventory-risk` |
| `no-informed-traders` | `market-maker-sim` | Fills are random | Informed traders fill you before the price moves against you. | none |
| `replication-equals-reproduction` | `replication-workbench` | Rerunning their code is replication | Replication rebuilds the result from the method and new choices. | none |
| `in-sample-equals-out-of-sample` | `replication-workbench` | The paper's number holds after it | After publication, less than half remains here. | `unstable-ratio` |
| `unstated-choices-do-not-matter` | `replication-workbench` | Unstated details are minor | Two readings of one line change this cell by a third. | `unstated-choice` |
| `published-number-is-the-truth` | `replication-workbench` | Match the paper exactly | Different data and dates; match the method, explain the gap. | none |
| `t-two-is-enough-for-a-new-factor` | `multiple-testing` | $t > 2$ makes a factor real | With hundreds tested, the hurdle is near 3 or more. | `hurdle-rises` |
| `ignore-unpublished-tests` | `multiple-testing` | Count only published tests | Failed tests went unpublished; they still count. | none |
| `overlapping-returns-plain-t` | `regression-lab` | Plain standard errors are fine for overlapping returns | Overlaps make returns autocorrelated; use Newey-West. | none |

---

## 11. Rejected alternatives and open questions

### 11.1 Rejected

| Rejected | Chosen instead | Reason |
|---|---|---|
| scikit-learn in Pyodide for widget numbers | `ml-core` in JavaScript with scikit-learn fixtures | 13 MB, absent from the Artifact, and too slow for a frame |
| TensorFlow.js, ONNX Runtime Web, brain.js | `ml-core`'s small autodiff | Size; GPU nondeterminism; WebAssembly uncertainty; hidden internals |
| ml.js libraries | `ml-core` | Their APIs do not yield the internals the lessons show (candidate splits, per-round residuals, per-unit activations) |
| Embedding TensorFlow Playground | `nn-playground` on our primitives | The Artifact forbids iframes; the design system, accessibility and tutor hooks must be ours |
| mlfinlab for López de Prado's methods | Our implementations tested against hand-computed cases | Its licence became commercial [unverified]; the book's own code is copyrighted, so we reimplement from the method's description |
| TreeSHAP or KernelSHAP | Exact Shapley values for at most 8 features | Exact, checkable by hand, and enough for intuition |
| Bundling CRSP, Compustat, Yahoo or Ken French files | `panel-sim` rehearsal data; learner-downloaded files | Licences; unknown truth; size |
| Grading a trained model's metric with a tolerance | Rules 1 to 4 of section 2.3 | Seed-sensitive metrics fail honest learners |
| Separate widgets for ridge, lasso, elastic net, stepwise and PCR | One `regularisation-path` | One cursor, one error panel, one set of tests |
| A dedicated confusion-matrix widget | `contingency-table`'s confusion preset | Prob-stats already owns the table |
| A second strategy-zoo engine in `multiple-testing` | `overfit-lab`'s zoo embedded there | One implementation (decision 6) |
| A dedicated backpropagation widget | `dependency-graph`'s backprop mode, extended | Calc-linalg already owns the computation graph |
| WebGL decision fields | Canvas 2D 64 × 64 `field` | Fits the budget; one rendering model |
| Continuous-time-only market-making simulation | Discrete $dt$ as in the paper, clamped | Matches the paper; replicable |
| Speech capture in `viva` | Typed answers with OS dictation | Web Speech support is uneven and untested in the Artifact [unverified] |
| A drag-and-drop visual ML pipeline builder (Orange style) | `ml-workbench`'s fixed eight steps | Free-form graphs are a product of their own; the exit needs one honest pipeline |
| A curse-of-dimensionality composite | A screen from primitives (section 8.1) | No logic beyond a formula and one simulation model |

### 11.2 Open questions

1. **WebAssembly in the Artifact** decides whether implement-it drills run there under MicroPython [unverified; the probe is running]. No concept widget depends on it.
2. **Pinned library versions in Pyodide** (scikit-learn, pandas, statsmodels) fix fixture values and some defaults [unverified which versions].
3. **PyTorch in Pyodide** is assumed absent [unverified]; PyTorch drills are local with paste-back.
4. **`dmath` cost.** If deterministic functions run more than 3× slower than `Math.*` [unverified], `nn-playground` drops to 15 epochs a second; measured in G0, but the decision to adopt `dmath` belongs to the P0 engine.
5. **Timings on the reference phone** for SMO, CART and forests [unverified]; measured in G0 against section 2.10.
6. **Paper figures** marked [recalled, unverified] in this file: Jegadeesh and Titman's 6/6 return, Fama and French's $R^2$ levels, Gatev and others' 11%, Avellaneda and Stoikov's parameters and table, Harvey, Liu and Zhu's 316 factors, McLean and Pontiff's decay, Hou, Xue and Zhang's failure rates, Bailey and others' MinBTL example, Gu, Kelly and Xiu's findings, and Luo and others' seven sins. The content team verifies each against the paper before any item uses it.
7. **Ken French data library:** its redistribution terms and whether the web app may fetch it directly (CORS) [unverified]. The plan assumes the learner downloads files.
8. **File input inside the Artifact sandbox** for learner CSVs [unverified], shared with prob-stats.
9. **GRS covariance divisors** in the reference implementation [unverified]; the fixture decides.
10. **`sample` limits for `viva`:** the input cap and any tool-count limit are read from `limits()` at runtime; the 6 KB transcript budget is set to fit [inferred from the contract's advice to keep inputs small].
11. **Owner decision:** the 3.1 data route (section 0.3).

---

## 12. All widgets

Kinds: **primitive** (a building block, also usable alone) and **composite** (assembled from primitives). Generator: **yes** (item generators), **seeds** (seeds vary data only), **bank** (a seeded draw from an authored bank), **no**.

| # | Id | Kind | Priority | Wave | Curriculum items | Generator |
|---|---|---|---|---|---|---|
| 1 | `span-track` | primitive (host layer) | P2 | G0 | 2.1.7, 2.1.8, 2.1.10, 3.1.1, 3.1.2, 3.1.4, 3.1.6; cross-cluster 2.2, 2.3 | no |
| 2 | `fit-explorer` | composite | P2 | G1 | 2.1.1, 2.1.4, 2.1.5 | yes |
| 3 | `loss-lab` | composite | P2 | G1 | 2.1.1, 2.1.2, 2.1.5 | yes |
| 4 | `error-curves` | composite | P2 | G1 | 2.1.1, 2.1.3, 2.1.4, 2.1.5, 2.1.6 | yes |
| 5 | `bias-variance-lab` | composite | P2 | G1 | 2.1.1, 2.1.4, 2.1.5, 2.1.10 | yes |
| 6 | `logistic-lab` | composite | P2 | G1 | 2.1.2, 2.1.6, 2.1.8 | yes |
| 7 | `classifier-plane` | composite | P2 | G1 (models in G2, G3) | 2.1.1, 2.1.2, 2.1.3, 2.1.5, 2.1.6 | yes |
| 8 | `threshold-lab` | composite | P2 | G1 | 2.1.2, 2.1.8 | yes |
| 9 | `calibration-lab` | composite | P2 | G1 (sizing G4) | 2.1.2, 2.1.8; cross-cluster 3.3 | yes |
| 10 | `feature-builder` | composite | P2 | G1 (cross-sectional H1) | 2.1.2, 2.1.8, 2.1.10, 3.1.1, 3.1.3 | yes |
| 11 | `basis-lab` | composite | P2 | G1 | 2.1.1, 2.1.2, 2.1.6 | yes |
| 12 | `cv-lab` | composite | P2 | G1 | 2.1.3, 2.1.4, 2.1.10 | yes |
| 13 | `tuning-lab` | composite | P2 | G1 | 2.1.3, 2.1.5, 2.1.7, 2.1.10 | yes |
| 14 | `regularisation-path` | composite | P2 | G1 | 2.1.3, 2.1.4, 2.1.10 | yes |
| 15 | `penalty-geometry` | composite | P2 | G1 | 2.1.4 | yes |
| 16 | `split-scorer` | composite | P2 | G2 | 2.1.5 | yes |
| 17 | `tree-builder` | composite | P2 | G2 | 2.1.5 | yes |
| 18 | `ensemble-lab` | composite | P2 | G2 | 2.1.3, 2.1.5 | yes |
| 19 | `boosting-lab` | composite | P2 | G2 | 2.1.5 | yes |
| 20 | `importance-lab` | composite | P2 | G2 (finance G4) | 2.1.5, 2.1.8, 2.1.10 | yes |
| 21 | `cluster-lab` | composite | P2 | G2 (correlation G4) | 2.1.5, 2.1.8; cross-cluster 2.3 | yes |
| 22 | `nn-playground` | composite | P2 | G3 | 2.1.2, 2.1.6 | yes |
| 23 | `relu-composer` | composite | P2 | G3 | 2.1.2, 2.1.6 | yes |
| 24 | `sequence-filter` | composite | P2 | G3 | 2.1.6, 2.1.8; cross-cluster 2.2 | yes |
| 25 | `time-cv-lab` | composite | P2 | G4 | 2.1.5, 2.1.7, 2.1.10; cross-cluster 2.2, 2.3 | yes |
| 26 | `leakage-detective` | composite | P2 | G4 | 2.1.3, 2.1.8, 2.1.10, 3.1.1 | yes |
| 27 | `labelling-lab` | composite | P2 | G4 | 2.1.7, 2.1.8, 2.1.10 | yes |
| 28 | `bar-sampler` | composite | P2 | G4 | 2.1.8 | yes |
| 29 | `fracdiff-lab` | composite | P2 | G4 | 2.1.8; cross-cluster 2.2 | yes |
| 30 | `sharpe-lab` | composite | P2 | G4 | 2.1.9, 3.1.2, 3.1.6; cross-cluster 2.3 | yes |
| 31 | `overfit-lab` | composite | P2 | G4 | 2.1.9, 3.1.6; cross-cluster 2.3, 2.4 | yes |
| 32 | `ml-workbench` | composite | P2 | G5 | 2.1.6, 2.1.9, 2.1.10; cross-cluster 2.3, 2.4 | seeds |
| 33 | `viva` | composite (input) | P1 | E (required at G5) | 1.6 exit, 2.1.10, 3.1.6; cross-cluster 3.3 | bank |
| 34 | `portfolio-sort` | composite | P2 | H1 | 2.1.8, 3.1.1, 3.1.2, 3.1.3; cross-cluster 2.3 | yes |
| 35 | `signal-lab` | composite | P2 | H1 | 2.1.2, 2.1.4, 2.1.10, 3.1.1, 3.1.2; cross-cluster 2.3 | yes |
| 36 | `factor-model-lab` | composite | P2 | H1 | 3.1.2, 3.1.3; cross-cluster 2.3 | yes |
| 37 | `pairs-lab` | composite | P2 | H2 | 3.1.4; cross-cluster 2.2 | yes |
| 38 | `market-maker-sim` | composite | P2 | H2 | 3.1.5; cross-cluster 1.7, 3.3 | yes |
| 39 | `replication-workbench` | composite | P2 | H1, H2 | 3.1.1 to 3.1.6; cross-cluster 2.3 | yes |

**Count:** 39 widgets: 1 primitive and 38 composites. 1 is P1 and 38 are P2. 36 composites need item generators.

**Build order inside P2.** G0: `ml-core`, `dataset-gen`, `panel-sim`, `backtest-core`, `sharpe-stats` and `as-sim` services (with their fixture pipeline), `span-track`, and the section 4 additions. G1: `fit-explorer`, `error-curves`, `loss-lab`, `bias-variance-lab`, then `logistic-lab`, `classifier-plane`, `threshold-lab`, `calibration-lab`, `feature-builder`, `basis-lab`, then `cv-lab`, `tuning-lab`, `regularisation-path`, `penalty-geometry`, with the prob-stats and calc-linalg extensions they use. G2: `split-scorer`, `tree-builder`, `ensemble-lab`, `boosting-lab`, `importance-lab`, `cluster-lab`. G3: `relu-composer`, `nn-playground`, `sequence-filter`, with the `descent-lab`, `dependency-graph` and `surface-explorer` extensions. G4: `time-cv-lab`, `leakage-detective` (with `pipeline-flow`'s sklearn mode), `labelling-lab`, `bar-sampler`, `fracdiff-lab`, `sharpe-lab`, `overfit-lab`. G5: `ml-workbench` (and `viva` if not already shipped in E). H1: `portfolio-sort`, `signal-lab`, `factor-model-lab`, `replication-workbench` (read, table, ledger, compare), with `regression-lab`'s HAC mode. H2: `pairs-lab`, `market-maker-sim`, `replication-workbench` (decay, note), with the `multiple-testing` and `coint-lab` extensions.

---

## 13. Cross-cluster needs

### 13.1 Primitives and engine features other clusters will need

1. **`span-track`**: rolling-origin evaluation in 2.2; holding periods, trade logs and the look-ahead check in the 2.3 backtesting engine; option lifetimes and expiry ladders in 1.7; any timeline of events.
2. **The `field` mark with `boundary` contours**: joint densities and likelihood maps (1.5, 1.6), loss surfaces (1.3), volatility surfaces as heatmaps (2.3 project 3).
3. **`dmath`**: every seeded simulation in every cluster; prob-stats already notes the cross-browser issue it solves.
4. **The worker job protocol with snapshots** (`sim-runner` train jobs): ARMA and GARCH fitting with progress (2.2), likelihood optimisation (1.6), descent visualisations (1.3), Monte Carlo pricing (1.7).
5. **Cross-widget bindings and the prediction gate**: any screen with two linked widgets; any "predict, then reveal" hook in any cluster.
6. **Typed `token-tray` slots**: expression building in algebra (0.2), regular expressions and SQL clauses (1.1, 1.2), alpha expressions here.
7. **`node-link` layered-dense and dendrogram layouts** and **`cell-grid` signed heatmaps**: Markov chains and probability trees (1.5), correlation matrices and portfolio construction (2.3), computation graphs (1.3).

### 13.2 Composites from this catalogue other clusters should reuse

| Composite | Other uses |
|---|---|
| `viva` | Every exit test that says "explain"; 3.3 mock interviews |
| `sharpe-lab`, `overfit-lab` | 2.3 project results notes; 2.4 Kaggle leaderboards; 3.3 interview questions on backtests |
| `portfolio-sort`, `signal-lab` | 2.3 project 2 (alpha signal research: IC, turnover, Sharpe ratio after costs) |
| `time-cv-lab`, `leakage-detective` | 2.2 rolling origin and the shuffled-CV Trap; 2.3 project 1's look-ahead check and held-out period |
| `market-maker-sim` | 3.3 market-making games (play mode); 1.7 spreads and inventory as a forward link |
| `calibration-lab` | 3.3 betting games and Kelly sizing, beside `game-lab` |
| `cluster-lab` | 2.3 portfolio construction (hierarchical risk parity's quasi-diagonalisation) |
| `threshold-lab` | 1.6 test power as a trade-off between error types, as an optional view |
| `sequence-filter`, `fracdiff-lab` | 2.2 filters, EWMA and stationarity |
| `bias-variance-lab` | 1.6 estimator mean squared error, through its estimator mode |

### 13.3 What this catalogue needs from other clusters

| Need | Expected owner | Used in |
|---|---|---|
| The ten engine requirements of section 2.1 | engine blueprint | everything here |
| `plot-2d`, `marks`, `drag-point`, `slider`, `stepper`, `region-select`, `sketch-pad`, `matrix`, `live-formula`, `sim-runner` with the section 4 additions | engine (union of catalogues) | everything here |
| `regression-lab` (prediction and HAC modes), `summary-table`, `multiple-testing`, `coint-lab`, `test-lab`, `contingency-table`, `icon-array`, `sampling-lab`, `posterior-lab`, `dist-explorer`, `qq-plot`, `game-lab`, and the `tests`, `ols` and `stats-core` services | prob-stats | 2.1.2, 2.1.3, 2.1.8, 2.1.9, 3.1.2, 3.1.3, 3.1.4, 3.1.6 |
| `descent-lab`, `dependency-graph`, `pca-lab`, `quadratic-form`, `condition-number`, `surface-explorer`, `least-squares-fit`, `sde-stepper` | calc-linalg | 2.1.2, 2.1.4, 2.1.6, 3.1.4 |
| `code-cell`, `pipeline-flow` (sklearn mode), `frame-core`, `node-link`, `cell-grid`, `value-table` frame mode, `groupby-lab`, `time-series-lab`, `drawdown-lab`, `setup-checklist`, `price-series` | programming | most code drills; `feature-builder`, `leakage-detective`, `ml-workbench`, `portfolio-sort` |
| `free-response` (timed no-notes mode), `card-sort` | Stage 0 | `viva`; matching tasks |
| An order-book and spread widget for context before 3.1.5 | finance cluster (1.7) | 3.1.5 L1 |
| The 2.3 backtesting engine project scaffold, sharing `backtest-core` | finance or projects cluster (2.3) | `overfit-lab`, `signal-lab`, `portfolio-sort` |
| Bertie's face assets, including a calm "listening" pose for examinations, and the speech-bubble and pointer components | engine and tutor blueprint | `viva`; every `annotate` call |
