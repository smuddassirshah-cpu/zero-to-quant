# nn-train levels 1 to 3 (optimisers; signal and normalisation; generalisation): second-reader findings

Scope: the 21 level 1 to 3 files in `app/content/courses/nn-train/` (twelve lessons, three reviews, three homeworks, three problem sets) and the shared modules `app/content/data/ai/nt_ops_l1.py`, `nt_ops_l2.py` (whose `layernorm` `sequence` L4 imports) and `nt_ops_l3.py`, at `ccf3e7e7`.
Method, no browser: every module function with a backward gradient-checked by central differences in float64 ($h = 10^{-6}$), including reuse of one input by two ops; optimisers stepped against Polyak's heavy ball, Kingma and Ba's Algorithm 1 and the PyTorch form of AdamW; the three number scripts run through `tools/run-number-scripts.mjs --only nn-train` and directly with `ZQ_NUMBERS_STRICT=1` under default (4) and single BLAS threads, `--verbose` outputs diffed; the l10 3,000-step run recomputed with the shipped modules under both thread settings; ten `literal()` marks read; `grade-all.mjs --file <f> --code --local-cdn <pkgs>` on each of the 21 files alone; per-case times against the page's limits through `tools/code-runner.mjs`, and every threshold test's value margin in CPython; 77 reviewer-written solutions injected as `mutants` and graded in Pyodide (appendix); every stated number in the text recomputed (closed forms in a scratch script, the trained ones from the number scripts) and every distractor checked against its `why`; `voice-scan.py 35` and a scan for American spellings, em-dashes and exclamation marks.
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, gap or teaching issue; note = style or small polish.

Counts: 2 errors, 8 warnings, 14 notes. No module error. Wrong solutions: 77 tried, 3 of them correct alternatives (accepted, as they should be), 3 of the other 74 survive.

## Modules (nt_ops_l1.py, nt_ops_l2.py, nt_ops_l3.py)

Gradient checks (relative error, central differences, float64): `sigmoid` 5.5e-10 (and 4.5e-10 at $|x| = 40$); `batchnorm` train $(6, 4)$ 2.4e-10, 9.7e-11, 5.0e-11 for $x$, $\gamma$, $\beta$; eval 2.4e-10, 6.3e-11, 1.9e-10; train with $N = 2$, where $\partial L/\partial x$ is near 0, 1.1e-6 (round-off on a near-zero gradient); two batch-norm calls sharing $\gamma$, $\beta$ 3.6e-10; `layernorm` $(6, 4)$ 1.7e-10, $(2, 3, 5)$ 6.7e-11, one vector 7.8e-10, and with $x$ reused outside the op 2.4e-10; `dropout` with the mask fixed 1.5e-10; `loss_and_grads` on the spiral net, every parameter, below 5.1e-9. Forwards of batch and layer norm match the textbook to 2.2e-16; running averages exact. Optimisers: `momentum_step` is Polyak's heavy ball exactly ($\mathbf v \leftarrow \beta\mathbf v - \eta\mathbf g$, $\mathbf p \leftarrow \mathbf p + \mathbf v$), `adam_step` is Kingma and Ba's Algorithm 1 exactly over five steps, with $\epsilon$ outside the root and a first step of size $\eta$; `adamw_step` matches $\mathbf p(1 - \eta\lambda) - \eta\,\hat m/(\sqrt{\hat v} + \epsilon)$ to 5.6e-17 and reduces to `adam_step` at $\lambda = 0$; `decayed_sgd_step` is SGD on $L + \tfrac\lambda2\lVert\mathbf w\rVert^2$, coupled, as l9 says. Inits: `init_net`, `lecun_sd`, `he_sd` and `init_layer` draw the stated sds (within 0.4% on 120,000 draws). No function mutates its inputs.

- app/content/data/ai/nt_ops_l3.py | `adamw_step` | warning | It decays every array it is given, biases included, while l9 teaches "biases usually unpenalised", the level 3 runs penalise weights only, and `gpt` L3 and `representations` will reach for this AdamW. The usual practice also exempts layer-norm gains. Nothing in the docstring says the caller must pass the weights alone. | Add an optional `decay=None` list of booleans (default: decay all, so the shipped behaviour is unchanged), or state in the docstring and the module README line: "decays every array passed; pass biases and norm gains with lam = 0 or in a second call".
- app/content/data/ai/nt_ops_l3.py | `dropout` | note | Any `mode` other than `"eval"` trains: `mode="test"` drops units silently, where `batchnorm` raises on an unknown mode. `p` is validated only after the eval and `p == 0` returns, and `early_stop([], k)` returns `(-1, -1)`. | Raise `ValueError` for a mode not in `("train", "eval")` and check `p` first; document the empty-list return.
- app/content/data/ai/nt_ops_l1.py | `warmup_cosine` | note | The rate at $t = 0$ is 0 under any warm-up, so in the course loop (rate `schedule(t)`, Adam step `t + 1`) Adam's first update, the one resting on a single squared gradient, moves nothing: it only fills $m$ and $v$. This matches common library schedules and is not wrong, but l4 never says it (see the l4 screens[4] note). | None in the module; say it in l4.

## Number scripts

- docs/reports/nn-train-L1/L2/L3-numbers.py | coverage | warning | Each script ends with `lv.claim(True, 'route B values', covers=COV)`, so every value passed to `cov()` counts as checked with no comparison. Most are computed values, which still guard coverage. In L3 line 222, `cov(shown_v[ia], shown_t[ia], shown_v[-1], shown_t[-1], 3000)` covers l10's 0.1029, 0.0528, 0.1668 and 0.0106 by reading them back from the lesson's own series, so they are never recomputed: route B gives 0.1654 for the final error and the run is not repeated with route A. This is how the l10 error below got through strict coverage. | Recompute route A for the 3,000-step run in the script and `expect` the stated figures; drop the read-back `cov`. Engine inbox: `numbers_lib` should refuse `covers=` on a claim whose `ok` is the literal `True`.

Both runs recompute and exit 0: CI runner 3 of 3 passed (21 s); direct with `ZQ_NUMBERS_STRICT=1`, L1 305 of 305, L2 229 of 229, L3 231 of 231, 0 uncovered (20, 13 and 15 literals) at default threads and at one thread. Diffing the `--verbose` outputs: L1 differs only below $10^{-12}$; L2 only in the batch-norm hook's final losses (op route 0.1902 against 0.1766 on seed 1, 0.1043 against 0.0919 on seed 4), which the lesson does not state, though the L2 report's "0.177 with the op and 0.194 composed" is stale under one thread; L3 in the last digits of the 50-step checks and in route B's 3,000-step final (0.165405 against 0.165390). Ten `literal()` marks read (L1 400, 1,000, 0.31, 3.75, 0.99, 10^-8; L2 2.31, 1,048,576, 2,048; L3 10,000): all are stated settings, sizes or givens with true reasons; 1,048,576 and 2,048 are computed facts marked literal, true but better as `expect`.

## Level 1: optimisers (l1 to l4, review-1, homework-1, problems-1)

- app/content/courses/nn-train/l4-schedules.json | screens[6] trap, explain and hints | error | The explain says "A decaying schedule trades early speed for a low finish, so a mid-run snapshot favours the constant rate". On this least-squares problem it does not: at step 150 the cosine's mean excess over the ten seeds is 0.0017 against the constant's 0.0034, and the constant is lower on only 5 of 10 seeds. Seed 11's 0.000046 is one lucky draw from the band. The point hint ("Nothing yet: it matches the constant rate until 180") is about the step schedule, which Dee did not compare. | Explain: "One step's loss is one draw from the band: over ten seeds the cosine is already lower at step 150 (0.0017 against 0.0034). Judge schedules at the end of equal runs, on several seeds." Point hint: "At step 150 the cosine still runs at half the starting rate."
- app/content/courses/nn-train/l4-schedules.json | screens[7] code | warning | The prompt asks for $t$ clamped to $[0, T]$, but no test uses $t < 0$: a solution that clamps only above passes every hidden test (appendix, l4 W3). | Add a test `warmup_cosine(-5, 0.1, 20, 300)` expecting 0.0, and one at `-5` with no warm-up expecting 0.2 (the clamp to 0 gives $\eta_{\max}$ there).
- app/content/courses/nn-train/l4-schedules.json | screens[4] prose and byKey `zero` | note | "Step 1 runs at $0.1 \times 1/20$" uses a step count from 0 while Adam counts from 1. In the course's own loop ($t$ from 0, `adam_step(..., t + 1, schedule(t))`) Adam's first update runs at rate 0, so the first step that moves is Adam's second. The `zero` line says step 0 does not move but not why that matters for $v$. | Add: "At $t = 0$ the rate is 0, so Adam's first gradient only fills $m$ and $v$; the first step that moves, $t = 1$, runs at $0.1 \times 1/20$."
- app/content/courses/nn-train/l1-noisy-steps.json | screens[3] canvas | note | The batch-32 curve at $\eta = 0.5$ jumps to 1.0976 at epoch 15 and 0.7776 at epoch 19 with no word, so a learner may read the run as unstable just before l1 calls 0.5 the best steady rate. | One sentence in the explain: "Its two spikes are single bad epochs at a large step; it recovers at once."
- app/content/courses/nn-train/l2-momentum.json | screens[7] code `how` | note | A learner who codes the PyTorch convention ($\mathbf v \leftarrow \beta\mathbf v + \mathbf g$, $\mathbf x \leftarrow \mathbf x - s\mathbf v$) follows the same path but fails test 1 on the returned velocity (appendix, l2 W2). The prompt fixes $\mathbf v$, so the grade is fair, but the how line does not say the velocity is compared. | "Tests 1 and 2 check the new point and the velocity $\mathbf v$ of the lesson's rule against the hand steps."
- app/content/courses/nn-train/review-1.json | items[8] explain | note | "A minibatch loss varies from batch to batch by more than 0.04 here": the item has no data that shows it. | "A minibatch loss can vary from batch to batch by more than the 0.04 gap."
- app/content/courses/nn-train/l3-adam.json, l3 screens[8]; l10 screens[6]; homework-1 items[1] | threshold tests | note | Value margins under 3x: SGD at 300 steps on seed 2 ends at 0.140 against the bar of 0.2 (1.4x); l10 test 8 lands at 0.179 against 0.25 (1.4x); `lr_sweep([0.2, 0.02], 150, 5)` picks 0.02 by 1.1% (0.1283 against 0.1296). All three are deterministic, agree to $10^{-8}$ between Pyodide and CPython and do not move with BLAS threads, so none can flip for a correct solution; recorded for the next reader. | None needed; raise the l10 bar only if a future edit makes the comparison noisy.

## Level 2: activations, initialisation and normalisation (l5 to l8, review-2, homework-2, problems-2)

- app/content/courses/nn-train/l6-initialisation.json | screens[3] prose and summary.ideas[1]; problems-2.json items[0] parts[3] question, byKey `lecun` and explain | warning | "ReLU halves the variance", "pass on half the variance" and "ReLU keeps half the variance": ReLU halves the second moment, $E[h^2] = \sigma^2/2$, while $\operatorname{Var}(h) = \sigma^2(\tfrac12 - \tfrac1{2\pi}) \approx 0.34\sigma^2$. homework-2 h2-relu-order marks exactly "$\operatorname{Var}(h) = \sigma^2/2$, so the variance of $h$ halves" as a distractor, so the course contradicts itself. The l6 derive also assumes zero-mean inputs, which ReLU outputs are not; the rule survives because only the weights need mean 0. | l6 screens[3]: "so the next layer's pre-activation variance halves: with zero-mean weights, $\operatorname{Var}(z) = n\operatorname{Var}(w)E[x^2]$." Summary: "ReLU halves the second moment, so He uses $\sqrt{2/n}$". problems-2 part 3: "which pass on half the second moment"; explain "ReLU keeps half of $E[z^2]$".
- app/content/courses/nn-train/l6-initialisation.json | summary.ideas[1] | warning | "Weight sd $1/\sqrt n$ (LeCun) keeps the variance through linear or tanh layers near 0" reads as "keeps the variance near 0" (the brief's "a tanh layer near 0" lost its noun). | "Weight sd $1/\sqrt n$ (LeCun) keeps the variance steady through linear layers, and through tanh layers working near $z = 0$; ReLU ..."
- app/content/courses/nn-train/l5-saturation.json | screens[4] prose; summary.ideas[2] | warning | "a **dead** unit, which no step can revive" and "is dead and never learns": the unit's own weights and bias get no gradient, but in a deeper net the layers below keep changing its inputs, so it can come back on. The claim holds only for a unit fed by fixed inputs. | "...passes nothing back, so its own weights and bias stop learning: a **dead** unit. Only changes in the layers below it can bring it back."
- app/content/courses/nn-train/l8-layer-norm.json | screens[6] code tests | warning | No hidden test feeds one tensor to a layer norm and to another path, so an op that assigns `x.grad` (or all three gradients) instead of adding passes every test (appendix, l8 W1 and W2). l7's op checks this (test 5), and the pre-norm block of `sequence` L4 reuses $\mathbf x$ on the residual path, exactly where assignment breaks. | Add a test like l7's: `L = (layernorm(x, g, b) * Tensor(Rl)).sum() + (x * Tensor(Rl)).sum()`, then compare `x.grad`.
- app/content/courses/nn-train/l5-saturation.json | screens[0] explain | note | "Each layer back from the output shrinks the gradient by roughly a factor of 4 to 5": from layer 2 to layer 1 it is 17 (7.4e-07 to 4.4e-08), because layer 1's inputs have mean 0 while the sigmoid outputs above it do not. | "...by a factor of about 4 to 5 a layer, and more at layer 1, whose inputs average 0."
- app/content/courses/nn-train/l5-saturation.json | screens[7] explain | note | "every gradient through this unit is cut ten-thousandfold": $1/(1.22 \times 10^{-4}) = 8{,}200$. | "cut about eight-thousandfold".
- app/content/courses/nn-train/review-2.json | items[4] explain | note | "already a fifteenth of its peak": $1/0.0707 = 14.2$. | "about a fourteenth of its peak".
- app/content/courses/nn-train/l7-batch-norm.json | screens[2] explain | note | "the layer would give back the raw batch exactly": with $\epsilon$ the 8 comes back as 7.999997. | "almost exactly ($\epsilon$ aside)".
- app/content/courses/nn-train/l7-batch-norm.json | screens[7] prose | note | The backward formula has $\frac{1}{N\sigma}$; the forward and the model op divide by $\sqrt{\sigma^2 + \epsilon}$. | "with $s = \sqrt{\sigma^2 + \epsilon}$ and $d_i = \gamma g_i$: $\frac{1}{Ns}(\dots)$".

## Level 3: generalisation in networks (l9 to l12, review-3, homework-3, problems-3)

- app/content/courses/nn-train/l10-early-stopping.json | screens[0] feedback.correct; summary.ideas[0] | error | "0.1668 at step 3,000" and "the training error falls from 0.0528 to 0.0106" do not hold under CI's single-thread BLAS. The shipped modules give 0.16677 and 0.01058 at default threads but 0.16667 and 0.01052 at one thread (0.1667, 0.0105), and the shipped series differs from the one-thread run by up to 0.029 mid-curve. The step (660) and its errors (0.1029, 0.0528) hold under both. The number script never recomputes these figures (see Number scripts). | State 0.167 and 0.011, which hold under both settings: "validation 0.1029, against 0.167 at step 3,000, while the training error falls from 0.0528 to 0.011"; the summary likewise. Label the chart as one run.
- app/content/courses/nn-train/l9-weight-decay.json screens[3] `train`; l4-schedules.json screens[4] `half`; l10-early-stopping.json screens[0] `start` and screens[2] `end` | byKey | note | Four `wrong[]` slips route to their id but have no `byKey` line, so the learner who makes the slip sees only the generic line. | One line each, for example l10 screens[2] `end`: "Evaluation 8 is the last one; patience 3 stops at 6, three past the best."
- app/content/courses/nn-train/l10-early-stopping.json | screens[6] | note | The brief's graded `train_with_early_stopping(steps, patience, seed)` is not written, and `gd_vs_ridge_path` takes one rate `eta`, not the brief's `etas`; the L3 report discloses both. | Accept, and record it in DECISIONS, or add the function in a fix pass within the budget rule.

## Course-wide

- app/content/courses/nn-train/ (l3, l6, l7, l8, l11, l12) | screens where each idea is named | warning | The course header of `docs/briefs/nn-train.md` asks for each paper to be named in one sentence where its idea is introduced. Only Loshchilov and Hutter (l9 screens[4]) appears. Missing: Kingma and Ba 2015 (l3 screens[1]), He et al. 2015 (l6 screens[3]), Ioffe and Szegedy 2015 (l7 screens[1]), Ba, Kiros and Hinton 2016 (l8 screens[1]), Srivastava et al. 2014 (l11 screens[1]), Belkin et al. 2019 (l12 screens[1]). | Add the name and year in brackets after the bolded term, as l9 does: "**Adam** (Kingma and Ba, 2015) keeps ...".

## Automated checks (no finding)

- `grade-all.mjs --file <f> --code --local-cdn <pkgs>`, each of the 21 files alone: 0 failures; 23 Python code widgets run; every starter fails test 1 and every authored mutant fails its named test. No code feedback in the course uses `byKey` `test-N` lines (each code screen has only `correct` and `generic`), so there is no `test-N` line to show or miss.
- Per-case time against the page's limit (two runs, the slower kept): the slowest case is homework-3 test 3 at 0.72 s against 43 s (60x), then l3 screens[8] test 6 at 0.39 s (100x) and l4 screens[8] test 4 at 0.19 s (210x). No case is near 3x.
- Every stated number recomputed by closed form or taken from the number scripts' route comparisons: the bowl (0.1816, best $\beta$ 0.40 at 0.00025, 3.00 at 0.9, 7.62 and 4.72 at 0.99, $s = 0.2309$, $\beta = 0.2699$, $0.519^{20} = 2.0 \times 10^{-6}$, measured $2.3 \times 10^{-5}$); Adam's factors 3.16, 4.25, 5.80, 6.53, 3.24, 1.26 and the hand steps 0.8004, 0.002663, 0.000533; every schedule rate; 15 and 66, 14 and 56, 2,215; the sigmoid chain 0.001213, $0.1966^8 = 2.23 \times 10^{-6}$, $0.1966^7 = 1.136 \times 10^{-5}$; every normalised value (1.3416, 3.6833, 5.314, 2.35, 1.389, 1.6036, 1.5811, 1.405); $2.56^5 = 110.0$, $1.44^6 = 8.92$, $0.9999^{1000} = 0.9048$, 0.941192, 1.4286, 2.8571. All match. Every distractor matches its `why`; no tolerance band overlaps another (grade-all's routing checks agree).
- Teaching claims checked and sound: Adam's scale invariance and its step of about $\eta$ per coordinate, with $\epsilon$ aside; the bias correction derived as $E[m_t] = (1 - \beta_1^t)E[g]$ for stationary gradients; the heavy-ball rates stated for quadratics only, with the $k\rho^k$ lag explained; batch norm never claims "internal covariate shift" (only "keeps each layer's inputs on a fixed scale"); coupled decay against AdamW stated correctly; early stopping as ridge hedged as an approximation for a quadratic loss from zero; double descent and the implicit bias of descent hedged as an observed tendency; Monte Carlo dropout given its caveat.
- `voice-scan.py 35` on the course: 0 sentences over 35 words (5,687 scanned), 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words. No em-dashes; exclamation marks only inside code (`{name!r}`); no American spellings in prose ("license" appears only as the verb).

## Appendix: wrong solutions

Each widget's model solution was edited into a wrong one and graded as a `mutant` in Pyodide by `grade-all.mjs --code` (scratch copies, nothing committed). "fails Tn" is the first hidden test it fails. The first line of each widget checks that the model solution, with the starter's comment lines kept, still passes. Builder: the scratchpad's `rv-nt/wrongs.py` and `mkwrong.py`.

### l1-noisy-steps screens[8] `minibatch_indices` (9 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. grad_spread draws each batch without replacement: **fails T7**.

```python
import numpy as np


def minibatch_indices(n, B, seed):
    order = np.random.default_rng(seed).permutation(n)
    return [order[i:i + B] for i in range(0, n, B)]


def sgd_step(params, grads, lr):
    return [p - lr * g for p, g in zip(params, grads)]


def grad_spread(B, trials, seed):
    rng = np.random.default_rng(seed)
    rows = grad_rows(np.zeros(3))[:, 0]
    draws = [rows[rng.choice(len(Xr), B, replace=False)].mean() for _ in range(trials)]
    return float(np.std(draws, ddof=1))
```
- W2. minibatch_indices shuffles with the global np.random, ignoring the seed: **fails T1**.

```python
import numpy as np


def minibatch_indices(n, B, seed):
    order = np.random.permutation(n)
    return [order[i:i + B] for i in range(0, n, B)]


def sgd_step(params, grads, lr):
    return [p - lr * g for p, g in zip(params, grads)]


def grad_spread(B, trials, seed):
    rng = np.random.default_rng(seed)
    rows = grad_rows(np.zeros(3))[:, 0]
    draws = [rows[rng.integers(0, len(Xr), B)].mean() for _ in range(trials)]
    return float(np.std(draws, ddof=1))
```

### l2-momentum screens[7] `momentum_step` (9 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. momentum as an average of gradients (dampened form v = beta v + (1 - beta) g, x - s v): **fails T1**.

```python
import numpy as np


def momentum_step(x, v, grad, s, beta):
    v = beta * np.asarray(v, dtype=float) + (1 - beta) * np.asarray(grad, dtype=float)
    return np.asarray(x, dtype=float) - s * v, v


def run_momentum(grad, x0, s, beta, n):
    x = np.asarray(x0, dtype=float)
    v = np.zeros_like(x)
    path = [x.copy()]
    for _ in range(n):
        x, v = momentum_step(x, v, grad(x), s, beta)
        path.append(x.copy())
    return np.array(path)


def best_heavy_ball(lmin, lmax):
    s = 4 / (np.sqrt(lmax) + np.sqrt(lmin)) ** 2
    k = np.sqrt(lmax / lmin)
    return float(s), float(((k - 1) / (k + 1)) ** 2)
```
- W2. momentum on the update, PyTorch convention (v = beta v + g, x - s v): same path, velocity in other units: **fails T1** (the returned velocity is in other units; fair, since the prompt fixes v as the lesson's velocity).

```python
import numpy as np


def momentum_step(x, v, grad, s, beta):
    v = beta * np.asarray(v, dtype=float) + np.asarray(grad, dtype=float)
    return np.asarray(x, dtype=float) - s * v, v


def run_momentum(grad, x0, s, beta, n):
    x = np.asarray(x0, dtype=float)
    v = np.zeros_like(x)
    path = [x.copy()]
    for _ in range(n):
        x, v = momentum_step(x, v, grad(x), s, beta)
        path.append(x.copy())
    return np.array(path)


def best_heavy_ball(lmin, lmax):
    s = 4 / (np.sqrt(lmax) + np.sqrt(lmin)) ** 2
    k = np.sqrt(lmax / lmin)
    return float(s), float(((k - 1) / (k + 1)) ** 2)
```
- W3. best_heavy_ball returns plain descent's best step 2/(lmin + lmax): **fails T7**.

```python
import numpy as np


def momentum_step(x, v, grad, s, beta):
    v = beta * np.asarray(v, dtype=float) - s * np.asarray(grad, dtype=float)
    return np.asarray(x, dtype=float) + v, v


def run_momentum(grad, x0, s, beta, n):
    x = np.asarray(x0, dtype=float)
    v = np.zeros_like(x)
    path = [x.copy()]
    for _ in range(n):
        x, v = momentum_step(x, v, grad(x), s, beta)
        path.append(x.copy())
    return np.array(path)


def best_heavy_ball(lmin, lmax):
    s = 2 / (lmax + lmin)
    k = np.sqrt(lmax / lmin)
    return float(s), float(((k - 1) / (k + 1)) ** 2)
```

### l3-adam screens[7] `adam_step` (9 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. Adam without bias correction: **fails T1**.

```python
import numpy as np


def adam_step(params, grads, m, v, t, lr, b1=0.9, b2=0.999, eps=1e-8):
    m = [b1 * mi + (1 - b1) * g for mi, g in zip(m, grads)]
    v = [b2 * vi + (1 - b2) * g * g for vi, g in zip(v, grads)]
    c1, c2 = 1.0, 1.0
    new = [p - lr * (mi / c1) / (np.sqrt(vi / c2) + eps) for p, mi, vi in zip(params, m, v)]
    return new, m, v


def adam_first_step_size(g, lr):
    g = np.asarray(g, dtype=float)
    return lr * np.abs(g) / (np.abs(g) + 1e-8)
```
- W2. bias correction on m only: **fails T1**.

```python
import numpy as np


def adam_step(params, grads, m, v, t, lr, b1=0.9, b2=0.999, eps=1e-8):
    m = [b1 * mi + (1 - b1) * g for mi, g in zip(m, grads)]
    v = [b2 * vi + (1 - b2) * g * g for vi, g in zip(v, grads)]
    c1, c2 = 1 - b1 ** t, 1.0
    new = [p - lr * (mi / c1) / (np.sqrt(vi / c2) + eps) for p, mi, vi in zip(params, m, v)]
    return new, m, v


def adam_first_step_size(g, lr):
    g = np.asarray(g, dtype=float)
    return lr * np.abs(g) / (np.abs(g) + 1e-8)
```
- W3. bias correction with the step counted from 0 (t - 1): **fails T1**.

```python
import numpy as np


def adam_step(params, grads, m, v, t, lr, b1=0.9, b2=0.999, eps=1e-8):
    m = [b1 * mi + (1 - b1) * g for mi, g in zip(m, grads)]
    v = [b2 * vi + (1 - b2) * g * g for vi, g in zip(v, grads)]
    c1, c2 = 1 - b1 ** (t - 1), 1 - b2 ** (t - 1)
    new = [p - lr * (mi / c1) / (np.sqrt(vi / c2) + eps) for p, mi, vi in zip(params, m, v)]
    return new, m, v


def adam_first_step_size(g, lr):
    g = np.asarray(g, dtype=float)
    return lr * np.abs(g) / (np.abs(g) + 1e-8)
```
- W4. first step size taken as lr in every coordinate (zero gradient and eps ignored): **fails T8**.

```python
import numpy as np


def adam_step(params, grads, m, v, t, lr, b1=0.9, b2=0.999, eps=1e-8):
    m = [b1 * mi + (1 - b1) * g for mi, g in zip(m, grads)]
    v = [b2 * vi + (1 - b2) * g * g for vi, g in zip(v, grads)]
    c1, c2 = 1 - b1 ** t, 1 - b2 ** t
    new = [p - lr * (mi / c1) / (np.sqrt(vi / c2) + eps) for p, mi, vi in zip(params, m, v)]
    return new, m, v


def adam_first_step_size(g, lr):
    g = np.asarray(g, dtype=float)
    return lr * np.ones_like(g)
```

### l3-adam screens[8] `train_spiral` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. Adam passed t from 0: **fails T1**.

```python
import numpy as np
from nt_ops_l1 import spirals, init_net, loss_and_grads, full_loss, sgd_step, momentum_step, adam_step

RATE = {"sgd": 0.5, "momentum": 0.3, "adam": 0.1}   # momentum uses beta = 0.9


def train_spiral(opt, steps, seed):
    X, y = spirals()
    params = init_net()
    rng = np.random.default_rng(seed)
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    for t in range(steps):
        idx = rng.choice(len(X), 32, replace=False)
        loss, grads = loss_and_grads(params, X[idx], y[idx])
        if opt == "sgd":
            params = sgd_step(params, grads, RATE[opt])
        elif opt == "momentum":
            params, m = momentum_step(params, m, grads, RATE[opt], 0.9)
        else:
            params, m, v = adam_step(params, grads, m, v, t, RATE[opt])
    return full_loss(params, X, y)
```
- W2. momentum as an average of gradients (dampened), written by hand: **fails T2**.

```python
import numpy as np
from nt_ops_l1 import spirals, init_net, loss_and_grads, full_loss, sgd_step, momentum_step, adam_step

RATE = {"sgd": 0.5, "momentum": 0.3, "adam": 0.1}   # momentum uses beta = 0.9


def train_spiral(opt, steps, seed):
    X, y = spirals()
    params = init_net()
    rng = np.random.default_rng(seed)
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    for t in range(steps):
        idx = rng.choice(len(X), 32, replace=False)
        loss, grads = loss_and_grads(params, X[idx], y[idx])
        if opt == "sgd":
            params = sgd_step(params, grads, RATE[opt])
        elif opt == "momentum":
            m = [0.9 * a + 0.1 * g for a, g in zip(m, grads)]
            params = [p - RATE[opt] * a for p, a in zip(params, m)]
        else:
            params, m, v = adam_step(params, grads, m, v, t + 1, RATE[opt])
    return full_loss(params, X, y)
```
- W3. no gradient zeroing: each step uses the sum of every gradient so far: **fails T1**.

```python
import numpy as np
from nt_ops_l1 import spirals, init_net, loss_and_grads, full_loss, sgd_step, momentum_step, adam_step

RATE = {"sgd": 0.5, "momentum": 0.3, "adam": 0.1}   # momentum uses beta = 0.9


def train_spiral(opt, steps, seed):
    X, y = spirals()
    params = init_net()
    rng = np.random.default_rng(seed)
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    for t in range(steps):
        idx = rng.choice(len(X), 32, replace=False)
        loss, new = loss_and_grads(params, X[idx], y[idx])
        acc = new if t == 0 else [a + g for a, g in zip(acc, new)]
        grads = acc
        if opt == "sgd":
            params = sgd_step(params, grads, RATE[opt])
        elif opt == "momentum":
            params, m = momentum_step(params, m, grads, RATE[opt], 0.9)
        else:
            params, m, v = adam_step(params, grads, m, v, t + 1, RATE[opt])
    return full_loss(params, X, y)
```
- W4. Adam without bias correction, written by hand: **fails T1**.

```python
import numpy as np
from nt_ops_l1 import spirals, init_net, loss_and_grads, full_loss, sgd_step, momentum_step, adam_step

RATE = {"sgd": 0.5, "momentum": 0.3, "adam": 0.1}   # momentum uses beta = 0.9


def train_spiral(opt, steps, seed):
    X, y = spirals()
    params = init_net()
    rng = np.random.default_rng(seed)
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    for t in range(steps):
        idx = rng.choice(len(X), 32, replace=False)
        loss, grads = loss_and_grads(params, X[idx], y[idx])
        if opt == "sgd":
            params = sgd_step(params, grads, RATE[opt])
        elif opt == "momentum":
            params, m = momentum_step(params, m, grads, RATE[opt], 0.9)
        else:
            m = [0.9 * a + 0.1 * g for a, g in zip(m, grads)]
            v = [0.999 * b + 0.001 * g * g for b, g in zip(v, grads)]
            params = [p - RATE[opt] * a / (np.sqrt(b) + 1e-8) for p, a, b in zip(params, m, v)]
    return full_loss(params, X, y)
```

### l4-schedules screens[7] `warmup_cosine` (7 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. warm-up counts from 1: lr_max (t + 1) / warmup: **fails T3**.

```python
import math


def warmup_cosine(t, lr_max, warmup, total):
    t = min(max(t, 0), total)
    if t < warmup:
        return lr_max * (t + 1) / warmup
    span = total - warmup
    if span <= 0:
        return lr_max
    return lr_max * 0.5 * (1 + math.cos(math.pi * (t - warmup) / span))


def schedule_table(lr_max, warmup, total, ts):
    return [warmup_cosine(t, lr_max, warmup, total) for t in ts]
```
- W2. cosine measured over total, not total - warmup: **fails T4**.

```python
import math


def warmup_cosine(t, lr_max, warmup, total):
    t = min(max(t, 0), total)
    if t < warmup:
        return lr_max * t / warmup
    span = total - warmup
    if span <= 0:
        return lr_max
    return lr_max * 0.5 * (1 + math.cos(math.pi * (t - warmup) / total))


def schedule_table(lr_max, warmup, total, ts):
    return [warmup_cosine(t, lr_max, warmup, total) for t in ts]
```
- W3. clamps t above only (negative t not clamped): **SURVIVES (passes every hidden test)**.

```python
import math


def warmup_cosine(t, lr_max, warmup, total):
    t = min(t, total)
    if t < warmup:
        return lr_max * t / warmup
    span = total - warmup
    if span <= 0:
        return lr_max
    return lr_max * 0.5 * (1 + math.cos(math.pi * (t - warmup) / span))


def schedule_table(lr_max, warmup, total, ts):
    return [warmup_cosine(t, lr_max, warmup, total) for t in ts]
```

### l4-schedules screens[8] `train_with_schedule` (4 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. Adam passed t from 0: **fails T1**.

```python
import numpy as np
from nt_ops_l1 import spirals, init_net, loss_and_grads, full_loss, adam_step, warmup_cosine


def train_with_schedule(schedule, steps, seed):
    X, y = spirals()
    params = init_net()
    rng = np.random.default_rng(seed)
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    for t in range(steps):
        idx = rng.choice(len(X), 32, replace=False)
        loss, grads = loss_and_grads(params, X[idx], y[idx])
        params, m, v = adam_step(params, grads, m, v, t, schedule(t))
    return full_loss(params, X, y)
```
- W2. Adam without bias correction, written by hand: **fails T1**.

```python
import numpy as np
from nt_ops_l1 import spirals, init_net, loss_and_grads, full_loss, adam_step, warmup_cosine


def train_with_schedule(schedule, steps, seed):
    X, y = spirals()
    params = init_net()
    rng = np.random.default_rng(seed)
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    for t in range(steps):
        idx = rng.choice(len(X), 32, replace=False)
        loss, grads = loss_and_grads(params, X[idx], y[idx])
        m = [0.9 * a + 0.1 * g for a, g in zip(m, grads)]
        v = [0.999 * b + 0.001 * g * g for b, g in zip(v, grads)]
        params = [p - schedule(t) * a / (np.sqrt(b) + 1e-8) for p, a, b in zip(params, m, v)]
    return full_loss(params, X, y)
```
- W3. Adam state reset every step: **fails T1**.

```python
import numpy as np
from nt_ops_l1 import spirals, init_net, loss_and_grads, full_loss, adam_step, warmup_cosine


def train_with_schedule(schedule, steps, seed):
    X, y = spirals()
    params = init_net()
    rng = np.random.default_rng(seed)
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    for t in range(steps):
        m = [np.zeros_like(p) for p in params]
        v = [np.zeros_like(p) for p in params]
        idx = rng.choice(len(X), 32, replace=False)
        loss, grads = loss_and_grads(params, X[idx], y[idx])
        params, m, v = adam_step(params, grads, m, v, t + 1, schedule(t))
    return full_loss(params, X, y)
```

### homework-1 items[0] `make_optimizer` (10 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. Adam without bias correction: **fails T4**.

```python
import numpy as np


class _Opt:
    def __init__(self, name, lr, beta=0.9, b1=0.9, b2=0.999, eps=1e-8):
        if name not in ("sgd", "momentum", "adam"):
            raise ValueError(f"unknown optimiser {name!r}")
        self.name, self.lr, self.beta = name, lr, beta
        self.b1, self.b2, self.eps = b1, b2, eps
        self.t, self.m, self.v = 0, None, None

    def step(self, params, grads):
        params = [np.asarray(p, dtype=float) for p in params]
        grads = [np.asarray(g, dtype=float) for g in grads]
        if self.m is None:
            self.m = [np.zeros_like(p) for p in params]
            self.v = [np.zeros_like(p) for p in params]
        if self.name == "sgd":
            return [p - self.lr * g for p, g in zip(params, grads)]
        if self.name == "momentum":
            self.m = [self.beta * m - self.lr * g for m, g in zip(self.m, grads)]
            return [p + m for p, m in zip(params, self.m)]
        self.t += 1
        self.m = [self.b1 * m + (1 - self.b1) * g for m, g in zip(self.m, grads)]
        self.v = [self.b2 * v + (1 - self.b2) * g * g for v, g in zip(self.v, grads)]
        c1, c2 = 1.0, 1.0
        return [p - self.lr * (m / c1) / (np.sqrt(v / c2) + self.eps) for p, m, v in zip(params, self.m, self.v)]


def make_optimizer(name, **settings):
    return _Opt(name, **settings)
```
- W2. momentum as an average of gradients (dampened form): **fails T2**.

```python
import numpy as np


class _Opt:
    def __init__(self, name, lr, beta=0.9, b1=0.9, b2=0.999, eps=1e-8):
        if name not in ("sgd", "momentum", "adam"):
            raise ValueError(f"unknown optimiser {name!r}")
        self.name, self.lr, self.beta = name, lr, beta
        self.b1, self.b2, self.eps = b1, b2, eps
        self.t, self.m, self.v = 0, None, None

    def step(self, params, grads):
        params = [np.asarray(p, dtype=float) for p in params]
        grads = [np.asarray(g, dtype=float) for g in grads]
        if self.m is None:
            self.m = [np.zeros_like(p) for p in params]
            self.v = [np.zeros_like(p) for p in params]
        if self.name == "sgd":
            return [p - self.lr * g for p, g in zip(params, grads)]
        if self.name == "momentum":
            self.m = [self.beta * m + (1 - self.beta) * g for m, g in zip(self.m, grads)]
            return [p - self.lr * m for p, m in zip(params, self.m)]
        self.t += 1
        self.m = [self.b1 * m + (1 - self.b1) * g for m, g in zip(self.m, grads)]
        self.v = [self.b2 * v + (1 - self.b2) * g * g for v, g in zip(self.v, grads)]
        c1, c2 = 1 - self.b1 ** self.t, 1 - self.b2 ** self.t
        return [p - self.lr * (m / c1) / (np.sqrt(v / c2) + self.eps) for p, m, v in zip(params, self.m, self.v)]


def make_optimizer(name, **settings):
    return _Opt(name, **settings)
```
- W3. momentum on the update, PyTorch convention (v = beta v + g, p - lr v): **passes every hidden test (a correct alternative, rightly accepted)**.

```python
import numpy as np


class _Opt:
    def __init__(self, name, lr, beta=0.9, b1=0.9, b2=0.999, eps=1e-8):
        if name not in ("sgd", "momentum", "adam"):
            raise ValueError(f"unknown optimiser {name!r}")
        self.name, self.lr, self.beta = name, lr, beta
        self.b1, self.b2, self.eps = b1, b2, eps
        self.t, self.m, self.v = 0, None, None

    def step(self, params, grads):
        params = [np.asarray(p, dtype=float) for p in params]
        grads = [np.asarray(g, dtype=float) for g in grads]
        if self.m is None:
            self.m = [np.zeros_like(p) for p in params]
            self.v = [np.zeros_like(p) for p in params]
        if self.name == "sgd":
            return [p - self.lr * g for p, g in zip(params, grads)]
        if self.name == "momentum":
            self.m = [self.beta * m + g for m, g in zip(self.m, grads)]
            return [p - self.lr * m for p, m in zip(params, self.m)]
        self.t += 1
        self.m = [self.b1 * m + (1 - self.b1) * g for m, g in zip(self.m, grads)]
        self.v = [self.b2 * v + (1 - self.b2) * g * g for v, g in zip(self.v, grads)]
        c1, c2 = 1 - self.b1 ** self.t, 1 - self.b2 ** self.t
        return [p - self.lr * (m / c1) / (np.sqrt(v / c2) + self.eps) for p, m, v in zip(params, self.m, self.v)]


def make_optimizer(name, **settings):
    return _Opt(name, **settings)
```
- W4. Adam step count read before it is advanced (t from 0): **fails T4**.

```python
import numpy as np


class _Opt:
    def __init__(self, name, lr, beta=0.9, b1=0.9, b2=0.999, eps=1e-8):
        if name not in ("sgd", "momentum", "adam"):
            raise ValueError(f"unknown optimiser {name!r}")
        self.name, self.lr, self.beta = name, lr, beta
        self.b1, self.b2, self.eps = b1, b2, eps
        self.t, self.m, self.v = 0, None, None

    def step(self, params, grads):
        params = [np.asarray(p, dtype=float) for p in params]
        grads = [np.asarray(g, dtype=float) for g in grads]
        if self.m is None:
            self.m = [np.zeros_like(p) for p in params]
            self.v = [np.zeros_like(p) for p in params]
        if self.name == "sgd":
            return [p - self.lr * g for p, g in zip(params, grads)]
        if self.name == "momentum":
            self.m = [self.beta * m - self.lr * g for m, g in zip(self.m, grads)]
            return [p + m for p, m in zip(params, self.m)]
        self.m = [self.b1 * m + (1 - self.b1) * g for m, g in zip(self.m, grads)]
        self.v = [self.b2 * v + (1 - self.b2) * g * g for v, g in zip(self.v, grads)]
        c1, c2 = 1 - self.b1 ** self.t, 1 - self.b2 ** self.t
        self.t += 1
        return [p - self.lr * (m / c1) / (np.sqrt(v / c2) + self.eps) for p, m, v in zip(params, self.m, self.v)]


def make_optimizer(name, **settings):
    return _Opt(name, **settings)
```
- W5. unknown name raises only at the first step: **fails T8**.

```python
import numpy as np


class _Opt:
    def __init__(self, name, lr, beta=0.9, b1=0.9, b2=0.999, eps=1e-8):
        self.name, self.lr, self.beta = name, lr, beta
        self.b1, self.b2, self.eps = b1, b2, eps
        self.t, self.m, self.v = 0, None, None

    def step(self, params, grads):
        params = [np.asarray(p, dtype=float) for p in params]
        grads = [np.asarray(g, dtype=float) for g in grads]
        if self.name not in ("sgd", "momentum", "adam"):
            raise ValueError(self.name)
        if self.m is None:
            self.m = [np.zeros_like(p) for p in params]
            self.v = [np.zeros_like(p) for p in params]
        if self.name == "sgd":
            return [p - self.lr * g for p, g in zip(params, grads)]
        if self.name == "momentum":
            self.m = [self.beta * m - self.lr * g for m, g in zip(self.m, grads)]
            return [p + m for p, m in zip(params, self.m)]
        self.t += 1
        self.m = [self.b1 * m + (1 - self.b1) * g for m, g in zip(self.m, grads)]
        self.v = [self.b2 * v + (1 - self.b2) * g * g for v, g in zip(self.v, grads)]
        c1, c2 = 1 - self.b1 ** self.t, 1 - self.b2 ** self.t
        return [p - self.lr * (m / c1) / (np.sqrt(v / c2) + self.eps) for p, m, v in zip(params, self.m, self.v)]


def make_optimizer(name, **settings):
    return _Opt(name, **settings)
```

### homework-1 items[1] `final_loss` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. filters blow-ups with np.isinf only, so a nan loss stays in: **fails T4**.

```python
import numpy as np


def final_loss(rate, steps, seed):
    rng = np.random.default_rng(seed)
    w = np.zeros(3)
    with np.errstate(all="ignore"):
        for _ in range(steps):
            idx = rng.integers(0, len(Xr), 8)
            g = Xr[idx].T @ (Xr[idx] @ w - yr[idx]) / 8
            w = w - rate * g
        return full_loss_ls(w)


def lr_sweep(rates, steps, seed):
    losses = [final_loss(r, steps, seed) for r in rates]
    ok = [(l, r) for l, r in zip(losses, rates) if not np.isinf(l)]
    return min(ok)[1], losses
```
- W2. np.nanargmin over the raw list (correct alternative): **passes every hidden test (a correct alternative, rightly accepted)**.

```python
import numpy as np


def final_loss(rate, steps, seed):
    rng = np.random.default_rng(seed)
    w = np.zeros(3)
    with np.errstate(all="ignore"):
        for _ in range(steps):
            idx = rng.integers(0, len(Xr), 8)
            g = Xr[idx].T @ (Xr[idx] @ w - yr[idx]) / 8
            w = w - rate * g
        return full_loss_ls(w)


def lr_sweep(rates, steps, seed):
    losses = [final_loss(r, steps, seed) for r in rates]
    return rates[int(np.nanargmin(losses))], losses
```

### l5-saturation screens[6] `layer_slopes` (7 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. ReLU slope 0.5 at exactly 0: **fails T3**.

```python
import numpy as np
from autograd import Tensor
from nt_ops_l2 import sigmoid


def layer_slopes(z, act):
    z = np.asarray(z, dtype=float)
    if act == "sigmoid":
        s = 1 / (1 + np.exp(-z))
        return s * (1 - s)
    if act == "tanh":
        return 1 - np.tanh(z) ** 2
    if act == "relu":
        return np.where(z > 0, 1.0, np.where(z == 0, 0.5, 0.0))
    raise ValueError(act)


def grad_norms_by_layer(Ws, x):
    ts = [Tensor(W) for W in Ws]
    h = Tensor(x)
    for W in ts:
        h = sigmoid(h @ W)
    (h * h).mean().backward()
    return [float(np.linalg.norm(W.grad)) for W in ts]


def dead_units(W, b, X):
    Z = np.asarray(X) @ np.asarray(W) + np.asarray(b)
    return int((Z.max(axis=0) <= 0).sum())
```
- W2. loss is the mean of h, not of h squared: **fails T4**.

```python
import numpy as np
from autograd import Tensor
from nt_ops_l2 import sigmoid


def layer_slopes(z, act):
    z = np.asarray(z, dtype=float)
    if act == "sigmoid":
        s = 1 / (1 + np.exp(-z))
        return s * (1 - s)
    if act == "tanh":
        return 1 - np.tanh(z) ** 2
    if act == "relu":
        return (z > 0).astype(float)
    raise ValueError(act)


def grad_norms_by_layer(Ws, x):
    ts = [Tensor(W) for W in Ws]
    h = Tensor(x)
    for W in ts:
        h = sigmoid(h @ W)
    h.mean().backward()
    return [float(np.linalg.norm(W.grad)) for W in ts]


def dead_units(W, b, X):
    Z = np.asarray(X) @ np.asarray(W) + np.asarray(b)
    return int((Z.max(axis=0) <= 0).sum())
```
- W3. dead when the largest pre-activation is below 0 (a unit peaking at exactly 0 counted alive): **fails T7**.

```python
import numpy as np
from autograd import Tensor
from nt_ops_l2 import sigmoid


def layer_slopes(z, act):
    z = np.asarray(z, dtype=float)
    if act == "sigmoid":
        s = 1 / (1 + np.exp(-z))
        return s * (1 - s)
    if act == "tanh":
        return 1 - np.tanh(z) ** 2
    if act == "relu":
        return (z > 0).astype(float)
    raise ValueError(act)


def grad_norms_by_layer(Ws, x):
    ts = [Tensor(W) for W in Ws]
    h = Tensor(x)
    for W in ts:
        h = sigmoid(h @ W)
    (h * h).mean().backward()
    return [float(np.linalg.norm(W.grad)) for W in ts]


def dead_units(W, b, X):
    Z = np.asarray(X) @ np.asarray(W) + np.asarray(b)
    return int((Z.max(axis=0) < 0).sum())
```

### l6-initialisation screens[6] `activation_sd_by_layer` (9 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. He where LeCun is asked (He for every activation): **fails T7**.

```python
import numpy as np

ACT = {"linear": lambda z: z, "tanh": np.tanh, "relu": lambda z: np.maximum(z, 0)}


def activation_sd_by_layer(depth, width, w_sd, act, seed):
    rng = np.random.default_rng(seed)
    h = rng.standard_normal((1000, width))
    out = []
    for _ in range(depth):
        W = rng.standard_normal((width, width)) * w_sd
        h = ACT[act](h @ W)
        out.append(float(h.std()))
    return out


def lecun_sd(fan_in):
    return 1 / np.sqrt(fan_in)


def he_sd(fan_in):
    return np.sqrt(2 / fan_in)


def init_layer(fan_in, fan_out, act, seed):
    sd = he_sd(fan_in)
    W = np.random.default_rng(seed).standard_normal((fan_in, fan_out)) * sd
    return W, np.zeros(fan_out)
```
- W2. Xavier (Glorot) sqrt(2/(fan_in + fan_out)) where LeCun is asked: **fails T7**.

```python
import numpy as np

ACT = {"linear": lambda z: z, "tanh": np.tanh, "relu": lambda z: np.maximum(z, 0)}


def activation_sd_by_layer(depth, width, w_sd, act, seed):
    rng = np.random.default_rng(seed)
    h = rng.standard_normal((1000, width))
    out = []
    for _ in range(depth):
        W = rng.standard_normal((width, width)) * w_sd
        h = ACT[act](h @ W)
        out.append(float(h.std()))
    return out


def lecun_sd(fan_in):
    return 1 / np.sqrt(fan_in)


def he_sd(fan_in):
    return np.sqrt(2 / fan_in)


def init_layer(fan_in, fan_out, act, seed):
    sd = he_sd(fan_in) if act == "relu" else np.sqrt(2 / (fan_in + fan_out))
    W = np.random.default_rng(seed).standard_normal((fan_in, fan_out)) * sd
    return W, np.zeros(fan_out)
```
- W3. W drawn as (fan_out, fan_in): **fails T8**.

```python
import numpy as np

ACT = {"linear": lambda z: z, "tanh": np.tanh, "relu": lambda z: np.maximum(z, 0)}


def activation_sd_by_layer(depth, width, w_sd, act, seed):
    rng = np.random.default_rng(seed)
    h = rng.standard_normal((1000, width))
    out = []
    for _ in range(depth):
        W = rng.standard_normal((width, width)) * w_sd
        h = ACT[act](h @ W)
        out.append(float(h.std()))
    return out


def lecun_sd(fan_in):
    return 1 / np.sqrt(fan_in)


def he_sd(fan_in):
    return np.sqrt(2 / fan_in)


def init_layer(fan_in, fan_out, act, seed):
    sd = he_sd(fan_in) if act == "relu" else lecun_sd(fan_in)
    W = np.random.default_rng(seed).standard_normal((fan_out, fan_in)) * sd
    return W, np.zeros(fan_out)
```
- W4. draws every weight matrix before the inputs: **fails T1**.

```python
import numpy as np

ACT = {"linear": lambda z: z, "tanh": np.tanh, "relu": lambda z: np.maximum(z, 0)}


def activation_sd_by_layer(depth, width, w_sd, act, seed):
    rng = np.random.default_rng(seed)
    Ws = [rng.standard_normal((width, width)) * w_sd for _ in range(depth)]
    h = rng.standard_normal((1000, width))
    out = []
    for W in Ws:
        h = ACT[act](h @ W)
        out.append(float(h.std()))
    return out


def lecun_sd(fan_in):
    return 1 / np.sqrt(fan_in)


def he_sd(fan_in):
    return np.sqrt(2 / fan_in)


def init_layer(fan_in, fan_out, act, seed):
    sd = he_sd(fan_in) if act == "relu" else lecun_sd(fan_in)
    W = np.random.default_rng(seed).standard_normal((fan_in, fan_out)) * sd
    return W, np.zeros(fan_out)
```

### l7-batch-norm screens[6] `batchnorm_forward` (7 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. training mode normalises with the running statistics (test-time statistics in training): **fails T1**.

```python
import numpy as np


def batchnorm_forward(x, gamma, beta, eps, mode, running):
    x = np.asarray(x, dtype=float)
    rm, rv = np.asarray(running[0], dtype=float), np.asarray(running[1], dtype=float)
    if mode == "train":
        new = (0.9 * rm + 0.1 * x.mean(axis=0), 0.9 * rv + 0.1 * x.var(axis=0))
        mu, var = rm, rv
    else:
        mu, var, new = rm, rv, (rm, rv)
    out = gamma * (x - mu) / np.sqrt(var + eps) + beta
    return out, new
```
- W2. inference mode normalises with the batch statistics: **fails T4**.

```python
import numpy as np


def batchnorm_forward(x, gamma, beta, eps, mode, running):
    x = np.asarray(x, dtype=float)
    rm, rv = np.asarray(running[0], dtype=float), np.asarray(running[1], dtype=float)
    if mode == "train":
        mu, var = x.mean(axis=0), x.var(axis=0)
        new = (0.9 * rm + 0.1 * mu, 0.9 * rv + 0.1 * var)
    else:
        mu, var, new = x.mean(axis=0), x.var(axis=0), (rm, rv)
    out = gamma * (x - mu) / np.sqrt(var + eps) + beta
    return out, new
```
- W3. running variance kept unbiased (N - 1), as PyTorch does: **fails T2**.

```python
import numpy as np


def batchnorm_forward(x, gamma, beta, eps, mode, running):
    x = np.asarray(x, dtype=float)
    rm, rv = np.asarray(running[0], dtype=float), np.asarray(running[1], dtype=float)
    if mode == "train":
        mu, var = x.mean(axis=0), x.var(axis=0)
        new = (0.9 * rm + 0.1 * mu, 0.9 * rv + 0.1 * x.var(axis=0, ddof=1))
    else:
        mu, var, new = rm, rv, (rm, rv)
    out = gamma * (x - mu) / np.sqrt(var + eps) + beta
    return out, new
```
- W4. inference mode still moves the running averages: **fails T5**.

```python
import numpy as np


def batchnorm_forward(x, gamma, beta, eps, mode, running):
    x = np.asarray(x, dtype=float)
    rm, rv = np.asarray(running[0], dtype=float), np.asarray(running[1], dtype=float)
    if mode == "train":
        mu, var = x.mean(axis=0), x.var(axis=0)
        new = (0.9 * rm + 0.1 * mu, 0.9 * rv + 0.1 * var)
    else:
        mu, var = rm, rv
        new = (0.9 * rm + 0.1 * x.mean(axis=0), 0.9 * rv + 0.1 * x.var(axis=0))
    out = gamma * (x - mu) / np.sqrt(var + eps) + beta
    return out, new
```

### l7-batch-norm screens[7] `batchnorm_op` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. backward of inference mode (batch statistics treated as constants): **fails T3**.

```python
import numpy as np
from autograd import Tensor


def batchnorm_op(x, gamma, beta, eps=1e-5):
    n = x.data.shape[0]
    mu = x.data.mean(axis=0)
    inv = 1 / np.sqrt(x.data.var(axis=0) + eps)
    xhat = (x.data - mu) * inv
    out = Tensor(gamma.data * xhat + beta.data, (x, gamma, beta), "batchnorm")

    def _backward():
        g = out.grad
        gamma.grad += (g * xhat).sum(axis=0)
        beta.grad += g.sum(axis=0)
        d = g * gamma.data
        x.grad += d * inv
    out._backward = _backward
    return out
```
- W2. forward with the unbiased variance (N - 1): **fails T1**.

```python
import numpy as np
from autograd import Tensor


def batchnorm_op(x, gamma, beta, eps=1e-5):
    n = x.data.shape[0]
    mu = x.data.mean(axis=0)
    inv = 1 / np.sqrt(x.data.var(axis=0, ddof=1) + eps)
    xhat = (x.data - mu) * inv
    out = Tensor(gamma.data * xhat + beta.data, (x, gamma, beta), "batchnorm")

    def _backward():
        g = out.grad
        gamma.grad += (g * xhat).sum(axis=0)
        beta.grad += g.sum(axis=0)
        d = g * gamma.data
        x.grad += inv / n * (n * d - d.sum(axis=0) - xhat * (d * xhat).sum(axis=0))
    out._backward = _backward
    return out
```
- W3. beta gradient averaged over the batch, not summed: **fails T2**.

```python
import numpy as np
from autograd import Tensor


def batchnorm_op(x, gamma, beta, eps=1e-5):
    n = x.data.shape[0]
    mu = x.data.mean(axis=0)
    inv = 1 / np.sqrt(x.data.var(axis=0) + eps)
    xhat = (x.data - mu) * inv
    out = Tensor(gamma.data * xhat + beta.data, (x, gamma, beta), "batchnorm")

    def _backward():
        g = out.grad
        gamma.grad += (g * xhat).sum(axis=0)
        beta.grad += g.mean(axis=0)
        d = g * gamma.data
        x.grad += inv / n * (n * d - d.sum(axis=0) - xhat * (d * xhat).sum(axis=0))
    out._backward = _backward
    return out
```

### l8-layer-norm screens[5] `layernorm_forward` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. compare_norms: batch norm with the unbiased variance: **fails T5**.

```python
import numpy as np


def layernorm_forward(x, gamma, beta, eps):
    x = np.asarray(x, dtype=float)
    mu = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    return gamma * (x - mu) / np.sqrt(var + eps) + beta


def compare_norms(x):
    x = np.asarray(x, dtype=float)
    ln = layernorm_forward(x, 1.0, 0.0, 1e-5)
    bn = (x - x.mean(axis=0)) / np.sqrt(x.var(axis=0, ddof=1) + 1e-5)
    return ln, bn
```
- W2. eps outside the root: **fails T1**.

```python
import numpy as np


def layernorm_forward(x, gamma, beta, eps):
    x = np.asarray(x, dtype=float)
    mu = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    return gamma * (x - mu) / (np.sqrt(var) + eps) + beta


def compare_norms(x):
    x = np.asarray(x, dtype=float)
    ln = layernorm_forward(x, 1.0, 0.0, 1e-5)
    bn = (x - x.mean(axis=0)) / np.sqrt(x.var(axis=0) + 1e-5)
    return ln, bn
```

### l8-layer-norm screens[6] `layernorm` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. assigns x.grad instead of adding into it: **SURVIVES (passes every hidden test)**.

```python
import numpy as np
from autograd import Tensor


def layernorm(x, gamma, beta, eps=1e-5):
    d = x.data.shape[-1]
    mu = x.data.mean(axis=-1, keepdims=True)
    inv = 1 / np.sqrt(x.data.var(axis=-1, keepdims=True) + eps)
    xhat = (x.data - mu) * inv
    out = Tensor(gamma.data * xhat + beta.data, (x, gamma, beta), "layernorm")

    def _backward():
        g = out.grad
        lead = tuple(range(g.ndim - 1))
        gamma.grad += (g * xhat).sum(axis=lead) if lead else g * xhat
        beta.grad += g.sum(axis=lead) if lead else g
        dx = g * gamma.data
        x.grad = inv / d * (d * dx - dx.sum(axis=-1, keepdims=True) - xhat * (dx * xhat).sum(axis=-1, keepdims=True))
    out._backward = _backward
    return out
```
- W2. assigns all three gradients instead of adding: **SURVIVES (passes every hidden test)**.

```python
import numpy as np
from autograd import Tensor


def layernorm(x, gamma, beta, eps=1e-5):
    d = x.data.shape[-1]
    mu = x.data.mean(axis=-1, keepdims=True)
    inv = 1 / np.sqrt(x.data.var(axis=-1, keepdims=True) + eps)
    xhat = (x.data - mu) * inv
    out = Tensor(gamma.data * xhat + beta.data, (x, gamma, beta), "layernorm")

    def _backward():
        g = out.grad
        lead = tuple(range(g.ndim - 1))
        gamma.grad = (g * xhat).sum(axis=lead) if lead else g * xhat
        beta.grad = g.sum(axis=lead) if lead else g
        dx = g * gamma.data
        x.grad = inv / d * (d * dx - dx.sum(axis=-1, keepdims=True) - xhat * (dx * xhat).sum(axis=-1, keepdims=True))
    out._backward = _backward
    return out
```
- W3. drops the scale path (the x-hat times sum term): **fails T2**.

```python
import numpy as np
from autograd import Tensor


def layernorm(x, gamma, beta, eps=1e-5):
    d = x.data.shape[-1]
    mu = x.data.mean(axis=-1, keepdims=True)
    inv = 1 / np.sqrt(x.data.var(axis=-1, keepdims=True) + eps)
    xhat = (x.data - mu) * inv
    out = Tensor(gamma.data * xhat + beta.data, (x, gamma, beta), "layernorm")

    def _backward():
        g = out.grad
        lead = tuple(range(g.ndim - 1))
        gamma.grad += (g * xhat).sum(axis=lead) if lead else g * xhat
        beta.grad += g.sum(axis=lead) if lead else g
        dx = g * gamma.data
        x.grad += inv / d * (d * dx - dx.sum(axis=-1, keepdims=True))
    out._backward = _backward
    return out
```

### homework-2 items[0] `layernorm_backward` (8 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. gamma and beta gradients summed over the last axis: **fails T2**.

```python
import numpy as np


def layernorm_backward(x, gamma, dout, eps):
    x = np.asarray(x, dtype=float)
    d = x.shape[-1]
    mu = x.mean(axis=-1, keepdims=True)
    inv = 1 / np.sqrt(x.var(axis=-1, keepdims=True) + eps)
    xhat = (x - mu) * inv
    lead = tuple(range(x.ndim - 1))
    dgamma = (dout * xhat).sum(axis=-1)
    dbeta = dout.sum(axis=-1)
    dxh = dout * gamma
    dx = inv / d * (d * dxh - dxh.sum(axis=-1, keepdims=True) - xhat * (dxh * xhat).sum(axis=-1, keepdims=True))
    return dx, dgamma, dbeta
```
- W2. eps outside the root: **fails T1**.

```python
import numpy as np


def layernorm_backward(x, gamma, dout, eps):
    x = np.asarray(x, dtype=float)
    d = x.shape[-1]
    mu = x.mean(axis=-1, keepdims=True)
    inv = 1 / (np.sqrt(x.var(axis=-1, keepdims=True)) + eps)
    xhat = (x - mu) * inv
    lead = tuple(range(x.ndim - 1))
    dgamma = (dout * xhat).sum(axis=lead)
    dbeta = dout.sum(axis=lead)
    dxh = dout * gamma
    dx = inv / d * (d * dxh - dxh.sum(axis=-1, keepdims=True) - xhat * (dxh * xhat).sum(axis=-1, keepdims=True))
    return dx, dgamma, dbeta
```
- W3. means of d taken as sums (1/D dropped): **fails T1**.

```python
import numpy as np


def layernorm_backward(x, gamma, dout, eps):
    x = np.asarray(x, dtype=float)
    d = x.shape[-1]
    mu = x.mean(axis=-1, keepdims=True)
    inv = 1 / np.sqrt(x.var(axis=-1, keepdims=True) + eps)
    xhat = (x - mu) * inv
    lead = tuple(range(x.ndim - 1))
    dgamma = (dout * xhat).sum(axis=lead)
    dbeta = dout.sum(axis=lead)
    dxh = dout * gamma
    dx = inv * (d * dxh - dxh.sum(axis=-1, keepdims=True) - xhat * (dxh * xhat).sum(axis=-1, keepdims=True))
    return dx, dgamma, dbeta
```

### homework-2 items[1] `fold_bn` (4 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. eps outside the root: **fails T1**.

```python
import numpy as np


def fold_bn(W, b, gamma, beta, mean, var, eps):
    s = np.asarray(gamma) / (np.sqrt(np.asarray(var)) + eps)
    return np.asarray(W) * s, (np.asarray(b) - mean) * s + beta
```
- W2. scales by gamma over the variance (no root): **fails T1**.

```python
import numpy as np


def fold_bn(W, b, gamma, beta, mean, var, eps):
    s = np.asarray(gamma) / (np.asarray(var) + eps)
    return np.asarray(W) * s, (np.asarray(b) - mean) * s + beta
```
- W3. new bias leaves the mean unscaled: b s - mean + beta: **fails T1**.

```python
import numpy as np


def fold_bn(W, b, gamma, beta, mean, var, eps):
    s = np.asarray(gamma) / np.sqrt(np.asarray(var) + eps)
    return np.asarray(W) * s, np.asarray(b) * s - mean + beta
```

### l9-weight-decay screens[6] `decayed_sgd_step` (7 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. weight decay added to the loss but not to the gradient (plain SGD step): **fails T1**.

```python
import numpy as np


def decayed_sgd_step(w, g, lr, lam):
    return np.asarray(w, dtype=float) - lr * np.asarray(g, dtype=float)


def _adam(w, g, m, v, t, lr):
    m = 0.9 * m + 0.1 * g
    v = 0.999 * v + 0.001 * g * g
    return w - lr * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-8)


def l2_vs_decoupled(w, g, m, v, t, lr, lam):
    w, g = np.asarray(w, dtype=float), np.asarray(g, dtype=float)
    l2 = _adam(w, g + lam * w, m, v, t, lr)
    adamw = _adam(w, g, m, v, t, lr) - lr * lam * w
    return l2, adamw


def best_lambda(results):
    return min(results, key=results.get)
```
- W2. AdamW decays the updated weight (lr lam times the new w): **fails T3**.

```python
import numpy as np


def decayed_sgd_step(w, g, lr, lam):
    return (1 - lr * lam) * np.asarray(w, dtype=float) - lr * np.asarray(g, dtype=float)


def _adam(w, g, m, v, t, lr):
    m = 0.9 * m + 0.1 * g
    v = 0.999 * v + 0.001 * g * g
    return w - lr * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-8)


def l2_vs_decoupled(w, g, m, v, t, lr, lam):
    w, g = np.asarray(w, dtype=float), np.asarray(g, dtype=float)
    l2 = _adam(w, g + lam * w, m, v, t, lr)
    adamw = _adam(w, g, m, v, t, lr)
    adamw = adamw - lr * lam * adamw
    return l2, adamw


def best_lambda(results):
    return min(results, key=results.get)
```
- W3. AdamW with the decay inside m only (lam w added to the gradient for m, not v): **fails T3**.

```python
import numpy as np


def decayed_sgd_step(w, g, lr, lam):
    return (1 - lr * lam) * np.asarray(w, dtype=float) - lr * np.asarray(g, dtype=float)


def _adam(w, g, m, v, t, lr):
    m = 0.9 * m + 0.1 * g
    v = 0.999 * v + 0.001 * g * g
    return w - lr * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-8)


def l2_vs_decoupled(w, g, m, v, t, lr, lam):
    w, g = np.asarray(w, dtype=float), np.asarray(g, dtype=float)
    l2 = _adam(w, g + lam * w, m, v, t, lr)
    mm = 0.9 * m + 0.1 * (g + lam * w)
    vv = 0.999 * v + 0.001 * g * g
    adamw = w - lr * (mm / (1 - 0.9 ** t)) / (np.sqrt(vv / (1 - 0.999 ** t)) + 1e-8)
    return l2, adamw


def best_lambda(results):
    return min(results, key=results.get)
```
- W4. decay factor 1 - lr lam / 2: **fails T1**.

```python
import numpy as np


def decayed_sgd_step(w, g, lr, lam):
    return (1 - lr * lam / 2) * np.asarray(w, dtype=float) - lr * np.asarray(g, dtype=float)


def _adam(w, g, m, v, t, lr):
    m = 0.9 * m + 0.1 * g
    v = 0.999 * v + 0.001 * g * g
    return w - lr * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-8)


def l2_vs_decoupled(w, g, m, v, t, lr, lam):
    w, g = np.asarray(w, dtype=float), np.asarray(g, dtype=float)
    l2 = _adam(w, g + lam * w, m, v, t, lr)
    adamw = _adam(w, g, m, v, t, lr) - lr * lam * w
    return l2, adamw


def best_lambda(results):
    return min(results, key=results.get)
```

### l10-early-stopping screens[6] `early_stop` (8 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. best index looked up over the whole list (peeks past the stop): **fails T2**.

```python
import numpy as np


def early_stop(val_losses, patience):
    best, best_i = float("inf"), -1
    for i, loss in enumerate(val_losses):
        if loss < best:
            best, best_i = loss, i
        elif i - best_i >= patience:
            return i, int(np.argmin(val_losses))
    return len(val_losses) - 1, best_i


def gd_vs_ridge_path(X, y, eta, ts, lams):
    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    n, d = X.shape
    w, t, gd = np.zeros(d), 0, []
    for target in ts:
        while t < target:
            w = w - eta * X.T @ (X @ w - y) / n
            t += 1
        gd.append(w.copy())
    ridge = [np.linalg.solve(X.T @ X / n + lam * np.eye(d), X.T @ y / n) for lam in lams]
    return gd, ridge
```
- W2. patience counts rises in a row, reset by any fall: **fails T1**.

```python
import numpy as np


def early_stop(val_losses, patience):
    best, best_i, run = float("inf"), -1, 0
    for i, loss in enumerate(val_losses):
        if loss < best:
            best, best_i = loss, i
        run = run + 1 if i and loss > val_losses[i - 1] else 0
        if run >= patience:
            return i, best_i
    return len(val_losses) - 1, best_i


def gd_vs_ridge_path(X, y, eta, ts, lams):
    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    n, d = X.shape
    w, t, gd = np.zeros(d), 0, []
    for target in ts:
        while t < target:
            w = w - eta * X.T @ (X @ w - y) / n
            t += 1
        gd.append(w.copy())
    ridge = [np.linalg.solve(X.T @ X / n + lam * np.eye(d), X.T @ y / n) for lam in lams]
    return gd, ridge
```
- W3. ridge solved with X^T X (not over n) beside X^T y / n: **fails T7**.

```python
import numpy as np


def early_stop(val_losses, patience):
    best, best_i = float("inf"), -1
    for i, loss in enumerate(val_losses):
        if loss < best:
            best, best_i = loss, i
        elif i - best_i >= patience:
            return i, best_i
    return len(val_losses) - 1, best_i


def gd_vs_ridge_path(X, y, eta, ts, lams):
    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    n, d = X.shape
    w, t, gd = np.zeros(d), 0, []
    for target in ts:
        while t < target:
            w = w - eta * X.T @ (X @ w - y) / n
            t += 1
        gd.append(w.copy())
    ridge = [np.linalg.solve(X.T @ X + lam * np.eye(d), X.T @ y / n) for lam in lams]
    return gd, ridge
```

### l11-dropout screens[5] `dropout_forward` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. dropout without rescaling: **fails T1**.

```python
import numpy as np


def dropout_forward(x, p, mode, seed):
    x = np.asarray(x, dtype=float)
    if mode == "eval":
        return x, None
    mask = (np.random.default_rng(seed).random(x.shape) >= p).astype(float)
    return x * mask, mask
```
- W2. eval mode scales by 1 - p (old-style dropout at inference on top): **fails T3**.

```python
import numpy as np


def dropout_forward(x, p, mode, seed):
    x = np.asarray(x, dtype=float)
    if mode == "eval":
        return x * (1 - p), None
    mask = (np.random.default_rng(seed).random(x.shape) >= p) / (1 - p)
    return x * mask, mask
```
- W3. mask drawn as rng.random < 1 - p (same law, other draws): **fails T1**.

```python
import numpy as np


def dropout_forward(x, p, mode, seed):
    x = np.asarray(x, dtype=float)
    if mode == "eval":
        return x, None
    mask = (np.random.default_rng(seed).random(x.shape) < 1 - p) / (1 - p)
    return x * mask, mask
```

### l11-dropout screens[6] `dropout_op` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. Monte Carlo passes also drop the output: **fails T4**.

```python
import numpy as np
from autograd import Tensor


def dropout_op(x, mask):
    out = Tensor(x.data * mask, (x,), "dropout")

    def _backward():
        x.grad += out.grad * mask
    out._backward = _backward
    return out


def mc_dropout_spread(params, x, p, draws, seed):
    rng = np.random.default_rng(seed)
    outs = []
    for _ in range(draws):
        h = np.array([[float(x)]])
        for i in range(3):
            h = h @ params[2 * i] + params[2 * i + 1]
            if i < 2:
                h = np.tanh(h)
            h = h * (rng.random(h.shape) >= p) / (1 - p)
        outs.append(float(h[0, 0]))
    return float(np.std(outs))
```
- W2. dropout applied before tanh: **fails T4**.

```python
import numpy as np
from autograd import Tensor


def dropout_op(x, mask):
    out = Tensor(x.data * mask, (x,), "dropout")

    def _backward():
        x.grad += out.grad * mask
    out._backward = _backward
    return out


def mc_dropout_spread(params, x, p, draws, seed):
    rng = np.random.default_rng(seed)
    outs = []
    for _ in range(draws):
        h = np.array([[float(x)]])
        for i in range(3):
            h = h @ params[2 * i] + params[2 * i + 1]
            if i < 2:
                h = h * (rng.random(h.shape) >= p) / (1 - p)
                h = np.tanh(h)
        outs.append(float(h[0, 0]))
    return float(np.std(outs))
```
- W3. sample sd (ddof = 1): **fails T4**.

```python
import numpy as np
from autograd import Tensor


def dropout_op(x, mask):
    out = Tensor(x.data * mask, (x,), "dropout")

    def _backward():
        x.grad += out.grad * mask
    out._backward = _backward
    return out


def mc_dropout_spread(params, x, p, draws, seed):
    rng = np.random.default_rng(seed)
    outs = []
    for _ in range(draws):
        h = np.array([[float(x)]])
        for i in range(3):
            h = h @ params[2 * i] + params[2 * i + 1]
            if i < 2:
                h = np.tanh(h)
                h = h * (rng.random(h.shape) >= p) / (1 - p)
        outs.append(float(h[0, 0]))
    return float(np.std(outs, ddof=1))
```

### l12-double-descent screens[6] `random_relu_features` (7 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. min_norm_fit by lstsq (correct alternative): **passes every hidden test (a correct alternative, rightly accepted)**.

```python
import numpy as np


def random_relu_features(X, p, seed):
    X = np.asarray(X, dtype=float)
    W = np.random.default_rng(seed).standard_normal((X.shape[1], p)) / np.sqrt(X.shape[1])
    return np.maximum(X @ W, 0)


def min_norm_fit(F, y):
    return np.linalg.lstsq(np.asarray(F, dtype=float), np.asarray(y, dtype=float), rcond=None)[0]


def double_descent_curve(ps, n, noise, seed):
    g = np.random.default_rng(seed)
    beta = g.standard_normal(10)
    beta /= np.linalg.norm(beta)
    Xa = g.standard_normal((n, 10))
    ya = Xa @ beta + noise * g.standard_normal(n)
    Xs = g.standard_normal((2000, 10))
    ys = Xs @ beta
    out = []
    for p in ps:
        F = random_relu_features(np.vstack([Xa, Xs]), p, seed + 1000)
        w = min_norm_fit(F[:n], ya)
        out.append(float(np.mean((F[n:] @ w - ys) ** 2)))
    return out
```
- W2. min_norm_fit by the normal equations: **fails T2**.

```python
import numpy as np


def random_relu_features(X, p, seed):
    X = np.asarray(X, dtype=float)
    W = np.random.default_rng(seed).standard_normal((X.shape[1], p)) / np.sqrt(X.shape[1])
    return np.maximum(X @ W, 0)


def min_norm_fit(F, y):
    F = np.asarray(F, dtype=float)
    return np.linalg.solve(F.T @ F, F.T @ np.asarray(y, dtype=float))


def double_descent_curve(ps, n, noise, seed):
    g = np.random.default_rng(seed)
    beta = g.standard_normal(10)
    beta /= np.linalg.norm(beta)
    Xa = g.standard_normal((n, 10))
    ya = Xa @ beta + noise * g.standard_normal(n)
    Xs = g.standard_normal((2000, 10))
    ys = Xs @ beta
    out = []
    for p in ps:
        F = random_relu_features(np.vstack([Xa, Xs]), p, seed + 1000)
        w = min_norm_fit(F[:n], ya)
        out.append(float(np.mean((F[n:] @ w - ys) ** 2)))
    return out
```
- W3. features without the ReLU: **fails T1**.

```python
import numpy as np


def random_relu_features(X, p, seed):
    X = np.asarray(X, dtype=float)
    W = np.random.default_rng(seed).standard_normal((X.shape[1], p)) / np.sqrt(X.shape[1])
    return X @ W


def min_norm_fit(F, y):
    return np.linalg.pinv(np.asarray(F, dtype=float)) @ np.asarray(y, dtype=float)


def double_descent_curve(ps, n, noise, seed):
    g = np.random.default_rng(seed)
    beta = g.standard_normal(10)
    beta /= np.linalg.norm(beta)
    Xa = g.standard_normal((n, 10))
    ya = Xa @ beta + noise * g.standard_normal(n)
    Xs = g.standard_normal((2000, 10))
    ys = Xs @ beta
    out = []
    for p in ps:
        F = random_relu_features(np.vstack([Xa, Xs]), p, seed + 1000)
        w = min_norm_fit(F[:n], ya)
        out.append(float(np.mean((F[n:] @ w - ys) ** 2)))
    return out
```
- W4. train and test features drawn with different seeds: **fails T5**.

```python
import numpy as np


def random_relu_features(X, p, seed):
    X = np.asarray(X, dtype=float)
    W = np.random.default_rng(seed).standard_normal((X.shape[1], p)) / np.sqrt(X.shape[1])
    return np.maximum(X @ W, 0)


def min_norm_fit(F, y):
    return np.linalg.pinv(np.asarray(F, dtype=float)) @ np.asarray(y, dtype=float)


def double_descent_curve(ps, n, noise, seed):
    g = np.random.default_rng(seed)
    beta = g.standard_normal(10)
    beta /= np.linalg.norm(beta)
    Xa = g.standard_normal((n, 10))
    ya = Xa @ beta + noise * g.standard_normal(n)
    Xs = g.standard_normal((2000, 10))
    ys = Xs @ beta
    out = []
    for p in ps:
        Fa = random_relu_features(Xa, p, seed + 1000)
        Fs = random_relu_features(Xs, p, seed + 2000)
        w = min_norm_fit(Fa, ya)
        out.append(float(np.mean((Fs @ w - ys) ** 2)))
    return out
```

### homework-3 items[0] `regularise_and_select` (5 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. dropout without rescaling (own mask): **fails T1**.

```python
import numpy as np
from autograd import Tensor
from nt_ops_l3 import dropout


def _adam(P, G, m, v, t, lr=0.02):
    m = [0.9 * a + 0.1 * g for a, g in zip(m, G)]
    v = [0.999 * a + 0.001 * g * g for a, g in zip(v, G)]
    return [p - lr * (a / (1 - 0.9 ** t)) / (np.sqrt(b / (1 - 0.999 ** t)) + 1e-8) for p, a, b in zip(P, m, v)], m, v


def _fit(X, y, lam, p, steps):
    g = np.random.default_rng(0)
    P = [g.standard_normal((1, 16)), np.zeros(16), g.standard_normal((16, 1)) / 4, np.zeros(1)]
    m = [np.zeros_like(q) for q in P]
    v = [np.zeros_like(q) for q in P]
    rng = np.random.default_rng(1)
    for t in range(steps):
        T = [Tensor(q) for q in P]
        h = (Tensor(X) @ T[0] + T[1]).tanh()
        if p > 0:
            h = h * Tensor((rng.random(h.data.shape) >= p).astype(float))
        out = h @ T[2] + T[3]
        loss = ((out - Tensor(y)) ** 2).mean() + 0.5 * lam * ((T[0] ** 2).sum() + (T[2] ** 2).sum())
        loss.backward()
        P, m, v = _adam(P, [q.grad for q in T], m, v, t + 1)
    return P


def regularise_and_select(X_tr, y_tr, X_val, y_val, lams, ps, steps=300):
    losses = {}
    for lam in lams:
        for p in ps:
            P = _fit(X_tr, y_tr, lam, p, steps)
            pred = np.tanh(X_val @ P[0] + P[1]) @ P[2] + P[3]
            losses[(lam, p)] = float(np.mean((pred - y_val) ** 2))
    return min(losses, key=losses.get), losses
```
- W2. selects on the training error (the wrong split): **fails T4**.

```python
import numpy as np
from autograd import Tensor
from nt_ops_l3 import dropout


def _adam(P, G, m, v, t, lr=0.02):
    m = [0.9 * a + 0.1 * g for a, g in zip(m, G)]
    v = [0.999 * a + 0.001 * g * g for a, g in zip(v, G)]
    return [p - lr * (a / (1 - 0.9 ** t)) / (np.sqrt(b / (1 - 0.999 ** t)) + 1e-8) for p, a, b in zip(P, m, v)], m, v


def _fit(X, y, lam, p, steps):
    g = np.random.default_rng(0)
    P = [g.standard_normal((1, 16)), np.zeros(16), g.standard_normal((16, 1)) / 4, np.zeros(1)]
    m = [np.zeros_like(q) for q in P]
    v = [np.zeros_like(q) for q in P]
    rng = np.random.default_rng(1)
    for t in range(steps):
        T = [Tensor(q) for q in P]
        h = (Tensor(X) @ T[0] + T[1]).tanh()
        if p > 0:
            h, _ = dropout(h, p, rng=rng)
        out = h @ T[2] + T[3]
        loss = ((out - Tensor(y)) ** 2).mean() + 0.5 * lam * ((T[0] ** 2).sum() + (T[2] ** 2).sum())
        loss.backward()
        P, m, v = _adam(P, [q.grad for q in T], m, v, t + 1)
    return P


def regularise_and_select(X_tr, y_tr, X_val, y_val, lams, ps, steps=300):
    losses, train = {}, {}
    for lam in lams:
        for p in ps:
            P = _fit(X_tr, y_tr, lam, p, steps)
            pred = np.tanh(X_val @ P[0] + P[1]) @ P[2] + P[3]
            losses[(lam, p)] = float(np.mean((pred - y_val) ** 2))
            fit_tr = np.tanh(X_tr @ P[0] + P[1]) @ P[2] + P[3]
            train[(lam, p)] = float(np.mean((fit_tr - y_tr) ** 2))
    return min(train, key=train.get), losses
```
- W3. penalty lam instead of lam / 2: **fails T1**.

```python
import numpy as np
from autograd import Tensor
from nt_ops_l3 import dropout


def _adam(P, G, m, v, t, lr=0.02):
    m = [0.9 * a + 0.1 * g for a, g in zip(m, G)]
    v = [0.999 * a + 0.001 * g * g for a, g in zip(v, G)]
    return [p - lr * (a / (1 - 0.9 ** t)) / (np.sqrt(b / (1 - 0.999 ** t)) + 1e-8) for p, a, b in zip(P, m, v)], m, v


def _fit(X, y, lam, p, steps):
    g = np.random.default_rng(0)
    P = [g.standard_normal((1, 16)), np.zeros(16), g.standard_normal((16, 1)) / 4, np.zeros(1)]
    m = [np.zeros_like(q) for q in P]
    v = [np.zeros_like(q) for q in P]
    rng = np.random.default_rng(1)
    for t in range(steps):
        T = [Tensor(q) for q in P]
        h = (Tensor(X) @ T[0] + T[1]).tanh()
        if p > 0:
            h, _ = dropout(h, p, rng=rng)
        out = h @ T[2] + T[3]
        loss = ((out - Tensor(y)) ** 2).mean() + lam * ((T[0] ** 2).sum() + (T[2] ** 2).sum())
        loss.backward()
        P, m, v = _adam(P, [q.grad for q in T], m, v, t + 1)
    return P


def regularise_and_select(X_tr, y_tr, X_val, y_val, lams, ps, steps=300):
    losses = {}
    for lam in lams:
        for p in ps:
            P = _fit(X_tr, y_tr, lam, p, steps)
            pred = np.tanh(X_val @ P[0] + P[1]) @ P[2] + P[3]
            losses[(lam, p)] = float(np.mean((pred - y_val) ** 2))
    return min(losses, key=losses.get), losses
```
- W4. no gradient zeroing: Tensors made once, grads accumulate: **fails T1**.

```python
import numpy as np
from autograd import Tensor
from nt_ops_l3 import dropout


def _adam(P, G, m, v, t, lr=0.02):
    m = [0.9 * a + 0.1 * g for a, g in zip(m, G)]
    v = [0.999 * a + 0.001 * g * g for a, g in zip(v, G)]
    return [p - lr * (a / (1 - 0.9 ** t)) / (np.sqrt(b / (1 - 0.999 ** t)) + 1e-8) for p, a, b in zip(P, m, v)], m, v


def _fit(X, y, lam, p, steps):
    g = np.random.default_rng(0)
    P = [g.standard_normal((1, 16)), np.zeros(16), g.standard_normal((16, 1)) / 4, np.zeros(1)]
    m = [np.zeros_like(q) for q in P]
    v = [np.zeros_like(q) for q in P]
    rng = np.random.default_rng(1)
    T = [Tensor(q) for q in P]          # made once; grads never zeroed
    for t in range(steps):
        h = (Tensor(X) @ T[0] + T[1]).tanh()
        if p > 0:
            h, _ = dropout(h, p, rng=rng)
        out = h @ T[2] + T[3]
        loss = ((out - Tensor(y)) ** 2).mean() + 0.5 * lam * ((T[0] ** 2).sum() + (T[2] ** 2).sum())
        loss.backward()
        P, m, v = _adam([q.data for q in T], [q.grad for q in T], m, v, t + 1)
        for q, new in zip(T, P):
            q.data = new
    return P


def regularise_and_select(X_tr, y_tr, X_val, y_val, lams, ps, steps=300):
    losses = {}
    for lam in lams:
        for p in ps:
            P = _fit(X_tr, y_tr, lam, p, steps)
            pred = np.tanh(X_val @ P[0] + P[1]) @ P[2] + P[3]
            losses[(lam, p)] = float(np.mean((pred - y_val) ** 2))
    return min(losses, key=losses.get), losses
```
- W5. weight decay in the reported loss but not in the gradient: **fails T1**.

```python
import numpy as np
from autograd import Tensor
from nt_ops_l3 import dropout


def _adam(P, G, m, v, t, lr=0.02):
    m = [0.9 * a + 0.1 * g for a, g in zip(m, G)]
    v = [0.999 * a + 0.001 * g * g for a, g in zip(v, G)]
    return [p - lr * (a / (1 - 0.9 ** t)) / (np.sqrt(b / (1 - 0.999 ** t)) + 1e-8) for p, a, b in zip(P, m, v)], m, v


def _fit(X, y, lam, p, steps):
    g = np.random.default_rng(0)
    P = [g.standard_normal((1, 16)), np.zeros(16), g.standard_normal((16, 1)) / 4, np.zeros(1)]
    m = [np.zeros_like(q) for q in P]
    v = [np.zeros_like(q) for q in P]
    rng = np.random.default_rng(1)
    for t in range(steps):
        T = [Tensor(q) for q in P]
        h = (Tensor(X) @ T[0] + T[1]).tanh()
        if p > 0:
            h, _ = dropout(h, p, rng=rng)
        out = h @ T[2] + T[3]
        mse = ((out - Tensor(y)) ** 2).mean()
        loss = mse.item() + 0.5 * lam * float((P[0] ** 2).sum() + (P[2] ** 2).sum())
        mse.backward()
        P, m, v = _adam(P, [q.grad for q in T], m, v, t + 1)
    return P


def regularise_and_select(X_tr, y_tr, X_val, y_val, lams, ps, steps=300):
    losses = {}
    for lam in lams:
        for p in ps:
            P = _fit(X_tr, y_tr, lam, p, steps)
            pred = np.tanh(X_val @ P[0] + P[1]) @ P[2] + P[3]
            losses[(lam, p)] = float(np.mean((pred - y_val) ** 2))
    return min(losses, key=losses.get), losses
```
- W6. dropout generator re-seeded every step: **fails T1**.

```python
import numpy as np
from autograd import Tensor
from nt_ops_l3 import dropout


def _adam(P, G, m, v, t, lr=0.02):
    m = [0.9 * a + 0.1 * g for a, g in zip(m, G)]
    v = [0.999 * a + 0.001 * g * g for a, g in zip(v, G)]
    return [p - lr * (a / (1 - 0.9 ** t)) / (np.sqrt(b / (1 - 0.999 ** t)) + 1e-8) for p, a, b in zip(P, m, v)], m, v


def _fit(X, y, lam, p, steps):
    g = np.random.default_rng(0)
    P = [g.standard_normal((1, 16)), np.zeros(16), g.standard_normal((16, 1)) / 4, np.zeros(1)]
    m = [np.zeros_like(q) for q in P]
    v = [np.zeros_like(q) for q in P]
    rng = np.random.default_rng(1)
    for t in range(steps):
        T = [Tensor(q) for q in P]
        h = (Tensor(X) @ T[0] + T[1]).tanh()
        if p > 0:
            h, _ = dropout(h, p, rng=np.random.default_rng(1))
        out = h @ T[2] + T[3]
        loss = ((out - Tensor(y)) ** 2).mean() + 0.5 * lam * ((T[0] ** 2).sum() + (T[2] ** 2).sum())
        loss.backward()
        P, m, v = _adam(P, [q.grad for q in T], m, v, t + 1)
    return P


def regularise_and_select(X_tr, y_tr, X_val, y_val, lams, ps, steps=300):
    losses = {}
    for lam in lams:
        for p in ps:
            P = _fit(X_tr, y_tr, lam, p, steps)
            pred = np.tanh(X_val @ P[0] + P[1]) @ P[2] + P[3]
            losses[(lam, p)] = float(np.mean((pred - y_val) ** 2))
    return min(losses, key=losses.get), losses
```

### homework-3 items[1] `decay_vs_ridge` (4 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. decay added to the loss but not the gradient (plain descent): **fails T1**.

```python
import numpy as np


def decay_vs_ridge(X, y, lam, eta, steps):
    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    n, d = X.shape
    w = np.zeros(d)
    for _ in range(steps):
        w = w - eta * X.T @ (X @ w - y) / n
    ridge = np.linalg.solve(X.T @ X / n + lam * np.eye(d), X.T @ y / n)
    return w, ridge
```
- W2. ridge with lam / 2: **fails T2**.

```python
import numpy as np


def decay_vs_ridge(X, y, lam, eta, steps):
    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    n, d = X.shape
    w = np.zeros(d)
    for _ in range(steps):
        w = (1 - eta * lam) * w - eta * X.T @ (X @ w - y) / n
    ridge = np.linalg.solve(X.T @ X / n + lam / 2 * np.eye(d), X.T @ y / n)
    return w, ridge
```
- W3. decay applied to the stepped weight: (1 - eta lam)(w - eta g): **fails T1**.

```python
import numpy as np


def decay_vs_ridge(X, y, lam, eta, steps):
    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    n, d = X.shape
    w = np.zeros(d)
    for _ in range(steps):
        w = (1 - eta * lam) * (w - eta * X.T @ (X @ w - y) / n)
    ridge = np.linalg.solve(X.T @ X / n + lam * np.eye(d), X.T @ y / n)
    return w, ridge
```

## Fix pass

I recomputed every changed figure before writing it: the l10 3,000-step run by route A in the number script (autograd, the shipped modules, `adam_step`) under default threads and under CI's single-thread environment (`OPENBLAS_CORETYPE=Haswell`, one thread), the ten-seed step-150 means of l4 by the script's own `ls_run`, the l5 gradient norms and ratios in a scratch script, and the new l8 expected values with the model solution, checked against test 2's values. I disputed nothing; one finding needed no action and two were not mine to change (frozen module, state file).

Status: fixed 21, declined 1, no action 1, deferred 1. Graded answers changed: none. Stated figures changed: l10 "0.1668" to "0.167" and "0.0106" to "0.011" (feedback and summary), l5 "ten-thousandfold" to "about eight-thousandfold", review-2 "a fifteenth" to "about a fourteenth", l4 trap explain (new figures 0.0017 against 0.0034, recomputed).

Number scripts: `lv.claim(True, 'route B values', covers=COV)` is gone from all three. The 487 values that went through it are now 391 recomputed values, each compared with the figures the level states at their stated precision (`cov()` covers a value only when it equals a stated figure; L1 189, L2 135, L3 67), 13 recomputed values that no figure states (dropped), and 83 typed constants that matched nothing or were covered by a computed value (dropped). Literals: 28 added with reasons, 2 removed (L2's 1,048,576 and 2,048 are now `cov(4 ** 10)` and `cov(16 * 128)`), so 74 in total against 48. Added literals are settings, sizes, step inputs of an `E()` call, three given validation curves, and three rounding words (a quarter, ten times, halved) each beside a claim that checks the figure behind it. All three scripts exit 0 through `run-number-scripts.mjs` and directly with `ZQ_NUMBERS_STRICT=1`, 0 uncovered.

### Modules
1. `adamw_step` decays every array: fixed in the text, module frozen. l9 screens[4] explain now says the course's `adamw_step` decays every array it is given, so pass the weights alone or give biases and norm gains $\lambda = 0$; the L3 report says the same.
2. `dropout` mode, `p` order and `early_stop([])`: declined, the modules are frozen for this pass. Left for the engine inbox.
3. `warmup_cosine` rate 0 at $t = 0$: fixed in l4 (see the l4 screens[4] line).

### Number scripts
4. Coverage by `claim(True, covers=...)`: fixed as above. L3 now runs route A for the 3,000 steps of l10 and `expect`s 660, 0.1029, 0.0528, 0.167 and 0.011 in the feedback and the summary, and checks route B ends at the same figures to the places stated.

### Level 1
5. l4 screens[6] trap: fixed. Explain now reads "One step's loss is one draw from the band: over ten seeds the cosine is already lower at step 150 (0.0017 against 0.0034). Judge schedules at the end of equal runs, on several seeds." The point hint says the cosine still runs at half the starting rate (0.1 against 0.2, checked). I also changed the `seed` distractor's why, which said more seeds would not help, to say that over ten the cosine is already lower at step 150, so it stays true. The script computes both means and `expect`s them.
6. l4 screens[7] clamp: fixed. Tests 6 and 7, `warmup_cosine(-5, 0.1, 20, 300)` giving 0.0 and `warmup_cosine(-5, 0.2, 0, 300)` giving 0.2, now sit after the past-the-end test (so the tests after them are 8 and 9); the clamp-above-only solution is a `mutant` failing test 6 (it returns -0.025). The `how` line says 9 tests.
7. l4 screens[4] note: fixed in byKey `zero`: at $t = 0$ the rate is 0, so Adam's first gradient only fills $m$ and $v$; the first step that moves, $t = 1$, runs at $0.1 \times 1/20$.
8. l1 screens[3] spikes: fixed, one sentence in the explain; the script checks epochs 15 and 19 spike (1.0976, 0.7776) and recover (0.1824, 0.1421).
9. l2 screens[7] `how`: fixed, tests 1 and 2 check the new point and the velocity.
10. review-1 items[8]: fixed, "can vary ... by more than the 0.04 gap".
11. Threshold margins: no action, as the finding says.

### Level 2
12. l6 ReLU "halves the variance": fixed in l6 screens[3] prose and explain, the summary, problems-2 part 3 (question, `lecun` line, explain) and the homework-2 item title, which said the same thing the item's own distractor marks wrong. ReLU halves the second moment.
13. l6 summary LeCun and tanh: fixed with the proposed wording.
14. l5 dead unit: fixed in screens[4] prose and the summary ("its own weights stop learning"; only the layers below can bring it back).
15. l8 screens[6] tests: fixed. Tests 7 (two layer-norm calls sharing $x$, $\gamma$, $\beta$, all three gradients compared) and 8 (the residual-path form the review proposed) are added; W1 and W2 are `mutants` failing test 7. Test 8 alone would depend on the order of the backward pass, which is why test 7 is the one the mutants name. The `how` line says 8 tests.
16. l5 screens[0]: fixed, "about 4 to 5 a layer, and more at layer 1, whose inputs average 0" (recomputed: 16.9 from layer 1 to 2, 4.1 to 5.1 elsewhere).
17. l5 screens[7]: fixed, "about eight-thousandfold" (1 / 1.22e-4 = 8,197), covered by `cov(round(1 / slope, -3))`.
18. review-2 items[4]: fixed, "about a fourteenth" (1 / 0.0707 = 14.2); the script's claim now rounds to 14.
19. l7 screens[2]: fixed, "almost exactly, $\epsilon$ aside".
20. l7 screens[7]: fixed, $s = \sqrt{\sigma^2 + \epsilon}$ and $1/(Ns)$.

### Level 3
21. l10 screens[0] and summary: fixed, 0.167 and 0.011; the chart is labelled as one run in the prose. Recomputed at 0.16667 and 0.01052 under CI's environment and 0.16677 and 0.01058 under default threads; both round to the figures stated.
22. Four missing `byKey` lines: fixed (l9 screens[3] `train`, l4 screens[4] `half`, l10 screens[0] `start` and screens[2] `end`).
23. l10 screens[6] graded function and `gd_vs_ridge_path` rate: deferred. The L3 report discloses both; the DECISIONS entry is for the main session, since state files are outside this pass.

### Course-wide
24. Paper names: fixed in l3 (Kingma and Ba, 2015), l6 (He et al., 2015), l7 (Ioffe and Szegedy, 2015), l8 (Ba, Kiros and Hinton, 2016), l11 (after Srivastava et al., 2014) and l12 (Belkin et al., 2019); l7's sentence is split to stay under 35 words.

Checks after the edits: validator 0 errors with no `[ai-mutants]` or `[source-ban]` warning on nn-train; voice scan 0 sentences over 35 words and 0 explanations over three sentences; `same-course-reuse.mjs --all` no error for nn-train; `grade-all.mjs --file <f> --code` 0 failures on each of the 16 edited files alone, every new mutant failing its named test.
