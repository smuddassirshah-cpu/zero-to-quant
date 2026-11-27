# AI strand: proposal for approval (27 Nov 2026)

Status: proposal only. Nothing is built until the user approves.

User decisions (27 Nov, DECISIONS "Session AK"): topics inside the existing stages; never gates the quant path; `ai-safety` and `ml-int` kept; built alongside the concept audit in separate sessions with separate next-session prompts. Figures are estimates; on build, hours come from `curriculum-hours.mjs` and never by hand.

## Shape

- An **[AI]** strand woven into the existing four stages as new topics, like the **[Pure maths]** items: own exit tests, never gates the quant path.
- It reuses the maths and ML already in the app through `requires` edges and does not reteach it: functions, counting, first-python (Stage 0); multivar, vectors, elimination, eigen, random-vars, estimation, regression, numpy-pandas, markov, graphs-dp (Stage 1); stat-learning, validation, fin-ml, convex (Stage 2).
- In-app code is NumPy and pure Python in Pyodide. No PyTorch in the browser (only a third-party `torch-pyodide` exists; not trusted for grading). GPU work (nanoGPT, fine-tuning) is outside study on free Colab.
- Size: 7 topics or course groups, 16 courses, 60 levels, 240 lessons. About 127 h in the app and 853 h outside, 980 h stored, about 15 months at 15 h a week.

## Stage 0

### 0.8 AI from nothing (50 h; app 15) [AI]
Requires: functions L1, counting L1, first-python L1, number-sense.

| Course | Levels |
| --- | --- |
| `ai-basics` What AI is | 1 Models from data (rules against learning, features, labels, train and test). 2 Learning by nudging (error, mean squared error by hand, sliding a line downhill). 3 One neuron (weighted sum, threshold, AND and OR by hand, why XOR needs two layers). 4 Language by counting (next-word tables, probabilities, sampling, temperature, tokens) |
| `ai-use` Using AI well | 1 How a chatbot is made (pretraining, fine-tuning, human feedback, as a story). 2 Asking and checking (prompting, hallucination, checking sums and sources). 3 Risks (bias, privacy, misuse, what alignment means) |

Resources: 3Blue1Brown Neural Networks ch. 1 and 2; Elements of AI (University of Helsinki); Google Machine Learning Crash Course; Karpathy, Intro to Large Language Models and Deep Dive into LLMs like ChatGPT; Anthropic prompt engineering docs.

Exit: a neuron's output by hand; a bigram table built and sampled from; a 15-line script that fits a line by gradient descent.

## Stage 1

### 1.12 Neural networks from scratch (180 h; app 23) [AI], after 1.3, 1.4, 1.6
Requires: multivar (chain rule, gradients), vectors and elimination (matrix products), random-vars, estimation (MLE), numpy-pandas.

| Course | Levels |
| --- | --- |
| `backprop` Backpropagation | 1 Derivatives as nudges, the chain rule on a graph. 2 The backward pass (topological order, accumulating gradients). 3 Neuron, layer, MLP in pure Python (micrograd style). 4 Vectorised in NumPy: shapes, broadcasting, gradient check by finite differences |
| `nn-train` Training networks | 1 Losses as likelihoods (MSE, softmax, cross-entropy). 2 Optimisers (SGD, minibatches, momentum, Adam, schedules). 3 Activations, initialisation, normalisation (saturation, vanishing gradients). 4 Generalisation (weight decay, dropout, early stopping) |
| `makemore` First language models | 1 Bigram by counting and as a one-layer net: same loss two ways. 2 MLP with embeddings (Bengio 2003). 3 Sampling and held-out evaluation |

Resources: Karpathy Neural Networks: Zero to Hero lectures 1 to 5; 3Blue1Brown ch. 3 and 4; Prince, Understanding Deep Learning (free PDF) ch. 1 to 9; Karpathy, A Recipe for Training Neural Networks; Distill, Why Momentum Really Works.

Exit: an MLP in NumPy whose gradients match finite differences to 1e-6; a character model on names that beats the bigram baseline on held-out loss.

## Stage 2

### 2.7 Deep learning (200 h; app 23) [AI], after 2.1
Requires: 1.12, stat-learning, validation, eigen.

| Course | Levels |
| --- | --- |
| `cnn` Convolutional networks | 1 Convolution as a sliding dot product. 2 Stride, padding, pooling, parameter counts. 3 A CNN on scikit-learn digits in NumPy. 4 Residual connections and normalisation |
| `sequence` Sequences and attention | 1 RNNs and backprop through time. 2 Attention as a soft lookup (query, key, value). 3 Self-attention, masks, heads, positions. 4 The transformer block and the residual stream |
| `representations` Embeddings and generative models | 1 Embeddings and cosine similarity. 2 Autoencoders and their link to PCA. 3 Generative models: VAE and diffusion as denoising |

Resources: 3Blue1Brown ch. 5 to 7 (transformers, attention); Understanding Deep Learning ch. 10 to 12, 14, 17, 18; DeepMind x UCL Deep Learning Lectures (2020); Stanford CS231n notes; Vaswani et al. 2017.

### 2.8 Reinforcement learning (120 h; app 11) [AI]
Requires: markov, conditional, graphs-dp, 1.12.

| Course | Levels |
| --- | --- |
| `rl` Reinforcement learning | 1 Bandits (explore or exploit). 2 MDPs and value iteration. 3 TD and Q-learning. 4 Policy gradients (REINFORCE). 5 Deep RL and search (AlphaGo, AlphaZero) |

Resources: Sutton and Barto, 2nd ed. (free PDF); DeepMind x UCL Reinforcement Learning Lectures (2021, 13 lectures); OpenAI Spinning Up; DeepMind AlphaGo and AlphaZero papers.

### 2.9 Language models (220 h; app 25) [AI]
Requires: sequence, rl L4, validation (leakage), fin-ml L1.

| Course | Levels |
| --- | --- |
| `gpt` Build a GPT | 1 Tokenisation (byte-pair encoding by hand). 2 A tiny GPT forward pass in NumPy. 3 Training it on Shakespeare. 4 Scale (parameter, memory and FLOP counts; Kaplan and Chinchilla) |
| `post-train` Base model to assistant | 1 Supervised fine-tuning and chat formats. 2 Reward models, RLHF, DPO (Bradley-Terry). 3 Constitutional AI. 4 Evaluation (benchmarks, contamination, judges) |
| `llm-apps` Building with language models | 1 Prompts as programs. 2 Retrieval. 3 Tools and agents. 4 LLMs in quant research (look-ahead bias from training cut-offs, leakage in text features) |

Resources: Karpathy, Let's build GPT, Let's build the GPT Tokenizer, Let's reproduce GPT-2 (124M), nanoGPT; Stanford CS336 (free lectures, GPU needed for assignments); Hugging Face LLM Course; Hoffmann et al. 2022 (DeepMind, Chinchilla); Ouyang et al. 2022; Bai et al. 2022 (Anthropic, Constitutional AI); Rafailov et al. 2023; Anthropic, Building effective agents.

Stage 2 exit: a NumPy CNN at 95% or more on held-out digits; Q-learning that solves a gridworld; a tiny GPT that beats the bigram baseline; outside the app, nanoGPT trained on Colab with a written results note.

## Stage 3

### 3.6 Frontier AI (160 h; app 23) [AI]
Requires: gpt, post-train, momentum-rep L1 (paper method).

| Course | Levels |
| --- | --- |
| `interp` Interpretability | 1 The residual stream and the logit lens. 2 Induction heads. 3 Superposition and sparse autoencoders (toy model rebuilt in NumPy). 4 Circuits and attribution graphs |
| `ai-papers` Reading and replicating | 1 How to read an ML paper. 2 Replicate one figure. 3 Compute arithmetic and scaling fits. 4 Write-up and critique |
| `ai-safety` Alignment and safety | 1 Specification gaming and reward hacking. 2 Evaluations, red-teaming, scaling policies. 3 Oversight and constitutional methods |

Resources: transformer-circuits.pub (A Mathematical Framework, Induction Heads, Toy Models of Superposition, Towards and Scaling Monosemanticity, On the Biology of a Large Language Model); ARENA curriculum; DeepMind, Specification gaming; Anthropic Responsible Scaling Policy; Google DeepMind Frontier Safety Framework; Jumper et al. 2021 (AlphaFold 2); BlueDot Impact AI Safety Fundamentals.

### 3.5 addition: `ml-int` ML interviews (50 h; app 6)
Levels: 1 Theory questions (backprop by hand, why Adam, bias and variance in deep nets). 2 From-scratch coding under time (stable softmax, attention, k-means). 3 ML research case at a fund. Overlap check against `research-int` L2 first; if it overlaps by more than half, add levels there instead. Resources: Chip Huyen, Introduction to Machine Learning Interviews.

Exit: one figure from Toy Models of Superposition replicated; a written critique of one paper; the ML interview mock at 70%.

## Assessments

- Topic exams: 0.8, 1.12, 2.7, 2.8, 2.9, 3.6 (six, pattern `topic-1.7.json`).
- One AI strand final, kept out of the four stage exams so the quant path is unchanged.
- One ML researcher mock in two versions; a prep path `interview-ml`.
- Per level: review, homework, a problem set, number scripts. Fluency families: shapes, parameter counts, softmax and cross-entropy by hand, attention arithmetic, FLOPs.

## Engine work (first, before any content)

1. `network` canvas: layers, weighted edges, live activations, editable weights.
2. `compgraph` canvas: forward values and backward gradients, stepped.
3. `contour` canvas: loss surface with optimiser paths and a learning-rate slider.
4. `heatmap`: attention, confusion and similarity matrices (extend `grid` if it fits).
5. `tokens` canvas: text split into tokens, byte-pair merges stepped.
6. `kernel` canvas: a kernel sliding over a small image.
7. `gridworld`: values, policy arrows, an agent (extend `grid`).
8. `trainer` widget: a small training loop run live with a loss curve.
9. A timing spike: largest model and step count that train inside the per-case grading limit on a mid-range phone.
10. Data: scikit-learn digits (bundled), a public-domain names list, Tiny Shakespeare (public domain).

## Build order

Engine pass, then waves of three or four content agents per SESSION PROTOCOL 3 (60 levels, at most three per agent, about six waves), second reads and fix passes per protocol 5, then exams. Runs alongside the concept audit (PLAN 5b) in separate sessions.
