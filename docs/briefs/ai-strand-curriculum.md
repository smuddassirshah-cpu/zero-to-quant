# AI strand: corrected curriculum (27 Nov 2026)

Status: for user approval. It replaces `docs/briefs/ai-strand-proposal.md`. The findings are in `docs/reviews/review-ai-strand.md` (F1 to F18). Nothing is built before approval and engine item 0.

User decisions kept (DECISIONS "Session AK"): new topics inside the four stages; never gates the quant path; out of the four stage exams; `ai-safety` and `ml-int` kept; built in sessions separate from the concept audit; no lesson id renamed or removed. Hours are estimates; on build they come from `curriculum-hours.mjs`.

## Shape

- Six **[AI]** topics: 0.8, 1.12, 2.7, 2.8, 2.9, 3.6. Every course carries `strand: "ai"` (engine item 0). No level is added to an existing quant course. A level added there would join the quant path, because strands are per course and role readiness needs every level of a required course (F1, F11). Folding happens inside the strand, and existing lessons are reused through `requires` edges.
- What it builds on (lesson ids checked): `multivar` l8-walking-downhill and `convex` l14-gradient-descent (descent and step size); `estimation` L2 (likelihood); `stat-learning` l10 (sigmoid, log loss), l15 (SVM and kernels), l16 (clustering) and l17 (a small network); `eigen` l11 (PCA); `ensembles` l2 (entropy as impurity); `graphs-dp` l17 (backward induction); `markov` L4 (random walks on networks); `numerics` L4 (control variates).
- In-app code is NumPy and pure Python in Pyodide 0.27.7. There is no PyTorch. GPU work (nanoGPT, ARENA, CS336) is outside study.
- Size: 6 topics, 17 courses, 63 levels, about 252 lessons. 950 h stored: 132 h in the app, 818 h outside, about 15 months at 15 h a week.
- Marks used below: **(moved)** a level kept from the proposal but placed elsewhere; **(merged)** two proposed levels made one; **(new)** not in the proposal. No level is added to an existing course.

## Stage 0

### 0.8 AI from nothing (40 h; app 15) [AI], alongside 0.3 and 0.4
Requires: `functions`/L2 (slope and intercept), `counting`/L2 (l8-counts-to-chances), `first-python`/L3 (loops and functions), `number-sense`/L3 (powers).

| Course | Levels |
| --- | --- |
| `ai-basics` What AI is | 1 Models from data (rules against learning, features, labels, questions the model has not seen). 2 Learning by nudging (error, mean squared error by hand, nudge a weight each way and keep the better; no derivatives). 3 One neuron (weighted sum, threshold, AND and OR by hand, why XOR needs a second layer; numbers differ from `stat-learning` l17). 4 Language by counting (next-word tables, probabilities, sampling, temperature as powers of probabilities, tokens) |
| `ai-use` Using AI well | 1 How a chatbot is made, and why it makes things up (pretraining, fine-tuning, human feedback as a story; hallucination). 2 Asking and checking (prompting, checking sums and sources). 3 Risks (privacy, bias, misuse; alignment previewed in one screen, taught in `ai-safety`) **(restored** to three levels: the validator requires 3 to 5 levels a course) |

Resources: 3Blue1Brown Neural Networks ch. 1 and 2 (watch only); Elements of AI (University of Helsinki, free; hours unverified); Karpathy, Intro to Large Language Models (2023) and Deep Dive into LLMs like ChatGPT (2025); Anthropic prompt engineering docs. Dropped: Google ML Crash Course, which assumes algebra, Python and pandas.

Exit: a neuron's output by hand; a bigram table built from text and sampled from; a script that fits a line by nudging two weights until the mean squared error stops falling.

## Stage 1

### 1.12 Neural networks from scratch (150 h; app 21) [AI], opens when its edges are met, alongside 1.8
Requires: `limits`/L3 and `multivar`/L1 (chain rule), `multivar`/L2 (gradient descent), `taylor`/L2 (central differences), `py-found`/L1 (floating point) and L3 (classes), `vectors`/L3 and `numpy-pandas`/L1 (arrays, broadcasting), `random-vars`/L5 (Jensen), `estimation`/L2 (likelihood), `testing`/L3 (out of sample), `graphs-dp`/L1 (`gate: false`: topological order is retaught in one screen).

| Course | Levels |
| --- | --- |
| `info` Information theory **(new)** | 1 Surprise and entropy (bits, surprisal, entropy of a distribution, codes and compression; links `ensembles` l2 later). 2 Cross-entropy and KL (code length under the wrong model, KL at least 0 by Jensen, perplexity, maximum likelihood as least cross-entropy). 3 Mutual information **(new**, level rule) (MI as KL between joint and product of marginals, MI of a feature with a label, data processing inequality, the bits a discrete signal carries about the next return's sign and its small-sample bias) |
| `backprop` Backpropagation | 1 The chain rule on a graph (forward values, local derivatives, gradients by hand; builds on `limits` L3, no reteach). 2 The backward pass (topological order, gradients that add at a branch, a scalar autograd class). 3 Neuron, layer, MLP on scalars, trained by gradient descent (`multivar` l8); gradient check by central differences (`taylor` L2). 4 A small array autograd in NumPy (matmul, broadcast sums, tanh, ReLU, softmax with cross-entropy), checked to relative error 1e-6 in float64. Every later course reuses it |
| `makemore` First language models | 1 Bigram by counting and as a one-layer net (normalised counts are the maximum likelihood estimate; softmax; one loss two ways, in nats and bits; `info` L2). 2 MLP with embeddings (Bengio et al. 2003; minibatches, a learning-rate sweep). 3 Sampling and held-out loss (train, dev and test names; overfitting seen first-hand; temperature) |

Moved out: `nn-train` to 2.7 (F2). Dropped: `backprop` L1 "derivatives as nudges", which `limits` L2 and `taylor` L1 already teach (F4).

Resources: Karpathy, Neural Networks: Zero to Hero lectures 1 to 5 (micrograd, makemore parts 1 to 4); 3Blue1Brown ch. 3 and 4; MacKay, Information Theory, Inference, and Learning Algorithms (free online), ch. 1 and 2; Prince, Understanding Deep Learning (free PDF, CC BY-NC-ND), ch. 1 to 7 (numbers unverified); Bengio et al. 2003.

Exit: an autograd MLP whose gradients match central differences to relative error 1e-6 (tanh, float64); entropy and KL computed in bits for a given pair; a character model whose dev loss on names beats the bigram's (the number script states both).

## Stage 2

### 2.7 Deep learning (240 h; app 33) [AI], after 2.1 and 1.12, alongside 2.5
Requires: 1.12; `stat-learning`/L2 (ridge), L3 (logistic, log loss) and L4 (l17); `validation`/L1; `convex`/L4 (step size from curvature); `eigen`/L1, L3 (PCA) and L4 (multivariate normal); `arma`/L1; `markov`/L4; `numpy-pandas`/L3 (rolling windows); `testing`/L2.

| Course | Levels |
| --- | --- |
| `nn-train` Training networks **(moved** from 1.12) | 1 Optimisers (minibatch noise, momentum, Adam, schedules; builds on `convex` l14). 2 Activations, initialisation and normalisation (saturation, vanishing gradients, batch and layer norm; the one home of normalisation). 3 Generalisation in networks (weight decay as ridge, early stopping as validation, dropout). 4 Experiments you can trust **(new)** (seeds, ablations, a training log, a paired comparison across seeds) |
| `cnn` Convolutional networks | 1 Convolution as a sliding dot product (1D first: a rolling mean is a convolution). 2 Stride, padding, pooling, parameter counts, im2col as one matrix product. 3 A CNN on digits in NumPy with one residual block, tested on shifted digits **(merged** old L3 and L4; normalisation stays in `nn-train` L2) |
| `sequence` Sequences and attention | 1 RNNs and backprop through time (AR(1) as a linear RNN, `arma` L1; exploding gradients from eigenvalues, `eigen` L1). 2 Attention as a soft lookup (nearest neighbours made smooth, `stat-learning` l4). 3 Self-attention, masks, heads, positions. 4 The transformer block and the residual stream |
| `representations` Embeddings and generative models | 1 Embeddings and cosine similarity (`vectors` L1, `makemore` L2). 2 Autoencoders: a linear one spans the top principal components (`eigen` l11). 3 The VAE on 2D data (ELBO by Jensen, Gaussian KL, the reparameterisation trick; `info` L2) **(new**, split from old L3). 4 Diffusion as denoising on 2D points (noise schedule, predict the noise, sample) **(new**, split from old L3). 5 Graph networks **(new)** (message passing as a normalised adjacency step, `markov` L4; one GCN layer on a small graph) |

Resources: Prince, Understanding Deep Learning ch. 8 to 13, 17 and 18 (13, 17 and 18 checked); 3Blue1Brown ch. 5 to 7 (ch. 7 checked); DeepMind x UCL Deep Learning Lectures (2020); Stanford CS231n notes; Karpathy, A Recipe for Training Neural Networks; Goh, Why Momentum Really Works (Distill, 2017); Vaswani et al. 2017; Kingma and Welling 2014; Ho et al. 2020; Kipf and Welling 2017.

### 2.8 Reinforcement learning (120 h; app 11) [AI], after 1.12, alongside 2.7
Requires: `markov`/L2, `graphs-dp`/L4 (l17-dice-stopping), `conditional`/L2, `limits-thm`/L3 (bounds) and L4 (Beta family), `estimation`/L3, `numerics`/L4 (control variates), `backprop`/L4.

| Course | Levels |
| --- | --- |
| `rl` Reinforcement learning | 1 Bandits (epsilon-greedy, UCB from a concentration bound, Thompson sampling with Beta posteriors). 2 MDPs and value iteration (backward induction made infinite; `graphs-dp` l17). 3 TD and Q-learning on a gridworld. 4 Policy gradients (REINFORCE; a baseline is a control variate, `numerics` L4). 5 Search and self-play (minimax and Monte Carlo tree search on a small game, taught in place because `game-theory` L1 is Stage 3; AlphaGo and AlphaZero read) |

Resources: Sutton and Barto, 2nd ed. (2018, free PDF); DeepMind x UCL Reinforcement Learning Lectures (2021, 13 lectures, checked); OpenAI Spinning Up (old and unmaintained; the policy-gradient pages still stand); Silver et al. 2016 and 2018.

### 2.9 Language models (200 h; app 25) [AI], after 2.7, and after 2.8 for `post-train` L2
Requires: `sequence`/L4, `backprop`/L4, `rl`/L4, `info`/L2, `stat-learning`/L3 (Bradley-Terry is a logistic regression), `testing`/L3, `numerics`/L1, `exp-log`/L2 with `regression`/L1 (power-law fits), `validation`/L3, `fin-ml`/L2 (hidden look-ahead).

| Course | Levels |
| --- | --- |
| `gpt` Build a GPT | 1 Tokenisation (bytes, UTF-8, byte-pair encoding by hand; deduplication). 2 A tiny GPT forward pass in NumPy (from supplied weights). 3 Training it on Tiny Shakespeare with the `backprop` L4 autograd (graded on short runs; the long run is outside). 4 Scale (parameters, about 6ND FLOPs, memory; Kaplan and Chinchilla; fitting a power law in log space) **(merged** with `ai-papers` old L3). 5 Hardware and precision **(new)** (bandwidth against FLOPs, arithmetic intensity, bf16 rounding, KV cache size; `numerics` L1) |
| `post-train` Base model to assistant | 1 Supervised fine-tuning and chat formats (loss masking). 2 Reward models, RLHF and DPO (Bradley-Terry, a KL penalty, `rl` L4). 3 Constitutional AI and AI feedback (the one home of constitutional methods). 4 Evaluation as statistics (standard errors, paired comparisons, contamination by n-gram overlap, judge bias; the one home of benchmark method) |
| `llm-apps` Language models at work | 1 Retrieval (TF-IDF and embedding search, cosine, recall at k). 2 Language models in quant research (training cut-offs as look-ahead, leakage in text features). 3 Tools and agents with a scripted model **(new**, level rule) (an agent loop against a deterministic stub model: tool schemas, parsing, stop conditions, step caps, trajectory evaluation; workflows against agents) |

Resources: Karpathy, Let's build GPT, Let's build the GPT Tokenizer, Let's reproduce GPT-2 (124M), nanoGPT; Stanford CS336 (free lectures; the site points self-learners to paid cloud GPUs for assignments); Hugging Face LLM Course (free); Kaplan et al. 2020; Hoffmann et al. 2022; Ouyang et al. 2022; Bai et al. 2022; Rafailov et al. 2023; Anthropic, Building effective agents (outside study).

Stage 2 strand exit: a NumPy CNN at 98% or more on held-out digits that beats a same-size MLP by a clear margin on digits shifted one pixel (thresholds from the number script; one seed of mine gave 0.985, and 0.643 against 0.483 shifted); Q-learning whose greedy policy equals value iteration's on the gridworld; a tiny GPT whose held-out loss per character beats the bigram's; outside the app, nanoGPT trained on Colab with a results note.

## Stage 3

### 3.6 Frontier AI (200 h; app 27) [AI], after 2.9, alongside 3.1
Requires: `gpt`/L3, `post-train`/L3 and L4, `rl`/L3, `representations`/L2, `research-int`/L3, `momentum-rep`/L1 (`gate: false`: its closure pulls in `alpha` L1 to L4).

| Course | Levels |
| --- | --- |
| `interp` Interpretability | 1 The residual stream and the logit lens (on the app's tiny GPT). 2 Induction heads (a two-layer attention-only model, supplied weights). 3 Superposition and sparse autoencoders (the toy model rebuilt in NumPy; one figure replicated). 4 Ablation and activation patching on the app's models (attribution graphs read only, F15) |
| `ai-papers` Reading and replicating | 1 How to read an ML paper (claim, baselines, ablations; modelled on `momentum-rep` L1). 2 Replicate one result (the `interp` L3 figure or a Chinchilla-style fit). 3 Write-up and critique (seeds, error bars, threats to validity) **(merged**: old L3 went to `gpt` L4) |
| `ai-safety` Alignment and safety | 1 Specification gaming and reward hacking (a gridworld agent that games its reward, then the fix; reward over-optimisation). 2 Dangerous-capability evaluations, red-teaming and scaling policies (builds on `post-train` L4). 3 Scalable oversight (debate, weak-to-strong, interpretability for audits; builds on `post-train` L3 and `interp` L4, no reteach) |
| `ml-int` ML interviews **(moved** from 3.5, F11) | 1 Theory questions aloud (backprop by hand, why Adam, double descent). 2 From-scratch coding under time (stable softmax, attention, k-means, one layer's backward pass) as a drills pack. 3 A deep learning case at a fund (when a net beats boosting on tabular returns, and when it does not; builds on `research-int` L3) |

Overlap check run (F11): `research-int` L2 shares only bias and variance with `ml-int` L1; L3 matches in method, so `ml-int` L3 was reshaped. That is under half, so `ml-int` stays a course.

Resources: transformer-circuits.pub (A Mathematical Framework; In-context Learning and Induction Heads; Toy Models of Superposition; Towards Monosemanticity; Scaling Monosemanticity; On the Biology of a Large Language Model); ARENA (PyTorch and GPU, outside only); Krakovna et al., Specification gaming (DeepMind, 2020); Gao et al. 2022, reward model over-optimisation; Irving et al. 2018, debate; Burns et al. 2023, weak-to-strong; Anthropic Responsible Scaling Policy; Google DeepMind Frontier Safety Framework; BlueDot Impact, Technical AI Safety (formerly AI Safety Fundamentals; free, cohort-based); Chip Huyen, Introduction to Machine Learning Interviews (free online). Dropped: Jumper et al. 2021 (no level used it).

Exit: the toy-models figure replicated in NumPy; the reward-hacking demo and its fix; an evaluation reported with standard errors; the ML mock at 70%. The written critique is required but self-marked, so it does not meet a level (AUTHORING 13).

## Assessments

- Topic exams: 0.8, 1.12, 2.7, 2.8, 2.9, 3.6 (six, pattern `topic-1.7.json`). They hold no training runs: code items are short, with small budgets.
- One AI strand final, outside the four stage exams. Check that an exam can stand outside topics and stages, else use a mock file.
- An ML researcher mock in two versions (`versionOf`), drawn from a new bank family; a prep path `interview-ml`; `docs/readiness.md` rows "optional" for every role.
- Per level: review, homework, a problem set, number scripts with thresholds for anything trained; a performance task from Stage 1 on (`perf-rules.mjs`).
- Fluency families (JSON only): array shapes and broadcasting; parameter counts; softmax and cross-entropy by hand; entropy and KL in bits; attention arithmetic; FLOP and memory counts; Bellman backups.

## Engine work (first, before any content)

0. **Strand `ai`** (blocking, F1): validator and `content.js` accept it; a badge; its own visibility setting, separate from "Quant path only"; kept out of the stage count, Today (unless opted in), quant-path hours in `curriculum-hours.mjs` and `hours.js`, census, readiness and stage papers.
1. `graph`: a second value line per node (forward value and gradient) and edge width by weight. This replaces the proposed `network` and `compgraph` canvases; l17 already draws a network on `graph`.
2. `matrix`: a `heat` fill by value with a legend, for attention, confusion and similarity matrices.
3. `grid`: a per-cell arrow glyph for policies. Values and paths exist already.
4. `trainer`: stream losses from a running worker into a `series` canvas; never graded.
5. Timing spike on the user's phone: Pyodide NumPy matmul throughput, the digits CNN (0.72 s natively for 40 epochs), 500 steps of a one-block GPT, `load_digits` offline. The limits are 5 s per case plus a budget of up to 120 s, plus 30 s for heavy imports.
6. Data: digits (UCI CC BY 4.0, credit line), `names.txt` and Tiny Shakespeare (licences checked at build), and weight files made by committed number scripts.
7. A drill pattern for `ml-int` L2 and a bank family for the mock.

Dropped: the `contour` canvas (`plane` has contour, heat and paths), `tokens` (`array` ranges and steps) and `kernel` (`matrix` highlight with frames) (F13).

## Totals (computed twice)

| Topic | Levels | Stored h | App h | Outside h |
| --- | --- | --- | --- | --- |
| 0.8 | 7 | 40 | 15 | 25 |
| 1.12 | 10 | 150 | 21 | 129 |
| 2.7 | 16 | 240 | 33 | 207 |
| 2.8 | 5 | 120 | 11 | 109 |
| 2.9 | 12 | 200 | 25 | 175 |
| 3.6 | 13 | 200 | 27 | 173 |
| All | 63 | 950 | 132 | 818 |

App hours are 2 h a level (four lessons of about 14 min, a 20 min review and a 45 min homework) plus 1 h for the topic exam. Check: 2 x 63 + 6 = 132, and 15 + 21 + 33 + 11 + 25 + 27 = 132. Stored: 40 + 150 + 240 + 120 + 200 + 200 = 950, and (40 + 120) + (150 + 200) + (240 + 200) = 950. Outside: 950 - 132 = 818, and 25 + 129 + 207 + 109 + 175 + 173 = 818. Months: 950 / 15 = 63.3 weeks, or 14.6 months at 4.33 weeks a month. Courses: 2 + 3 + 4 + 1 + 3 + 4 = 17.

## Build order

Engine item 0 and the spike first, then items 1 to 7, then waves of three or four content agents (SESSION PROTOCOL 3; 60 levels at most three per agent, about six waves), second reads and fix passes (protocol 5), then the exams. It runs in sessions separate from the concept audit (PLAN 5b).

## Change log

| # | Change | Finding |
| --- | --- | --- |
| 1 | Engine item 0, strand `ai`; no AI level added to a quant course | F1, F11 |
| 2 | `nn-train` moved to 2.7; 1.12 is `info`, `backprop` and `makemore` | F2 |
| 3 | Stage 0 exit fits by nudging; 0.8 edges corrected | F3 |
| 4a | `backprop` L1 builds on `limits` L3, no reteach | F4 |
| 4b | `nn-train` L1 "losses as likelihoods" dropped (in `info` L2, `makemore` L1, `stat-learning` l10) | F4 |
| 4c | `cnn` L3 and L4 merged; normalisation in `nn-train` L2 only | F4 |
| 4d | `ai-papers` old L3 merged into `gpt` L4 | F4 |
| 4e | Constitutional methods in `post-train` L3 only; `ai-safety` L3 is oversight | F4 |
| 4f | Benchmark method in `post-train` L4; `ai-safety` L2 builds on it | F4 |
| 4g | `ai-use` L2 and L3 merged; alignment in `ai-safety` | F4 |
| 4h | Prompting kept only in `ai-use`; `llm-apps` prompts moved outside | F4, F10 |
| 5 | Edges to l8, l10, l11, l14, l15, l17, ensembles l2, graphs-dp l17; no SVM course; fresh numbers in `ai-basics` L3 | F5 |
| 6 | New `info` course, two levels | F6 |
| 7 | Edges fixed: `fin-ml`/L2, `limits-thm`/L4, `estimation`/L3, `numerics`/L4, `eigen`/L4; minimax taught in `rl` L5; `gate: false` on `graphs-dp`/L1 and `momentum-rep`/L1 | F7 |
| 8 | CNN exit: 98% held out and a margin on shifted digits | F8 |
| 9 | Array autograd in `backprop` L4; graded cases on supplied weights or short runs; threshold tests | F9 |
| 10 | `llm-apps` cut to two gradeable levels | F10 |
| 11 | `ml-int` moved to 3.6; L3 reshaped | F11 |
| 12 | Added `nn-train` L4, `gpt` L5, `representations` L3 to L5 | F12 |
| 13 | Five canvases dropped; `graph`, `matrix`, `grid` extended | F13 |
| 14 | Resources corrected, added and dropped | F14 |
| 15 | `interp` L4 downscoped | F15 |
| 16 | Licence and credit notes | F16 |
| 17 | Totals 950, 126, 824; strand shown apart | F17 |
| 19 | `ai-use`, `info` and `llm-apps` given a third level each (session AK, after approval): the validator requires 3 to 5 levels a course | main session |
| 18 | 1.12 opens on its edges; performance tasks; no training in exams; strand final exam kind | F18 |
