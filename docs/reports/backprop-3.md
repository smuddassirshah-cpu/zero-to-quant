# backprop level 3 (Neurons, layers and training): report

## Files written

All in `app/content/courses/backprop/`, £ for money. Skills: `bp-networks` on l9 to l11, `bp-check` on l12; the review tags six items `bp-networks` and four `bp-check`.

| File | Screens / items | Code |
|---|---|---|
| `l9-neuron-of-values.json` | 9 screens, 3 quiz items | `Value.tanh()` |
| `l10-layers-and-networks.json` | 9 screens, 3 quiz items | `Neuron`, `Layer`, `MLP` |
| `l11-the-training-loop.json` | 9 screens (one ungraded `trainer`), 3 quiz items | `train(model, X, Y, steps, lr)` |
| `l12-checking-gradients.json` | 10 screens, 3 quiz items | `check_gradients(model, X, Y, h)` |
| `review-3.json` | 10 items, difficulty 2 to 4, `pass: 0.8` | none |
| `homework-3.json` | 6 items, difficulty 3 to 5 (two at 5) | `mlp_param_count` and `mlp_forward_fixed` (4), `hidden_layer_gain` (5), performance network (5); `order` item; `longform` with a 10-point rubric |
| `problems-3.json` | 3 problems, 14 parts, difficulty 3, 4, 5 | none |

Lesson shapes. l9: a threshold neuron has no slope (nudge gives 0), tanh and its slope on a `plane` (drag P; 0.9151 at 0.3), the derivative $1 - \tanh^2$ as an `order` derivation, the course neuron by hand on a `graph` with weights on edges and edge width by weight (engine 1227), the other four gradients, trap ($1 - n^2 = 0.91$), edge case $n = 5$ (0.000182), `tanh()` code, a squashed credit score (0.0099). l10: one line cannot split the XOR (`scatter` with groups), the 2-3-1 network as a `graph` with `edgeWidth` (sign by colour, width by size, biases on the second value line) stepped by frames to the output $-0.3266$, parameter counts 13, 41, 337, the seeded draw order, trap (edges only: 32 against 41), edge case one neuron settles at 4, the three classes in code, a fund's 5-8-8-1 network (129). l11: one step for the output bias, a live `trainer` screen (engine 1237; the learner runs and edits the loop), the loop's order (precedence rules), 200 steps on a `series` (first below 0.1 at step 68), four step sizes, trap (no reset: the weights reach 74 and the loss reads 0 by saturation; other seeds stick near 2), edge case (fitting four points is not prediction), `train` in code (thresholds), next-day returns. l12: the plausible bug, the central difference on a `plane` with an `h` control (0.7855 at $h = 0.1$), the $h^2$ error from the Taylor curvature term (`order`), the error table as powers of ten, relative error, the course network's check at three $h$, trap (a forward difference read as a bug), edge case (a kink gives 0.5), `check_gradients` with a planted $1 - n^2$ bug, a swapped $N(d_1)$ and $N(d_2)$ delta caught by a bumped price.

Timing: the l11 code case trains 200 steps on the course network; graded in Pyodide 0.27.7 under node (`tools/code-runner.mjs`), all seven tests took 1.7 s including Python start-up and the 200-step case about 0.15 s. The widget carries `budget: 4000` for a phone. homework-3 items 2 and 6 run four and three short trainings (about 0.1 s each natively) under `budget: 6000`.

Generators: `/tmp/claude-0/-home-user-zero-to-quant/b2245dfe-6f55-570e-8d22-d9384c33129b/scratchpad/backprop-1/` (`common3.py`, `gen3.py`, `gen3b.py`, `gen3c.py`); every test `expect` comes from the model solution.

## Gates

1. Validator: `node tools/validate.mjs` 0 errors; no backprop error (advisory warnings only).
2. Voice: `voice-scan.py 35` with `VOICE_BASE=app/content/courses/backprop`: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `docs/reports/backprop-L3-numbers.py` with the venv: 271 of 271 checks, exit 0. Route 1 is the level's classes taken from the JSON; route 2 a NumPy network with hand-written matrix gradients from the same 13 draws, and central differences of a plain-float loss. It reruns the 200-step training and asserts every quoted loss: 5.556800, 4.955816, 1.588956, 0.153664, 0.059298, 0.025020 (Value and NumPy agree to 1e-9; step-0 gradients to 1e-12); 0.1756 and 0.0241 at 0.2, 3.3716 and 4.0001 at 0.5, 8.0 at 2.0; the check 1.6e-3, 1.6e-7, 2.8e-8; the step-size table; the planted bug 1.65.
4. Playthrough: every L3 file with `--local-cdn <pkgs> --mobile`: all passed at 1280 and 440 (see the run in the hand-back). Screens read at 440; fixes made: the error plot redrawn as powers of ten on linear axes (the plane's log scale stops at $10^{-9}$, backlog), the neuron graph spread so edge labels clear the sum box.
5. Freshness: `fresh-check.mjs --file` on review-3 and problems-3: 0 hits (three stems reworded). homework-3: code-name hits `Neuron`, `parameters`, `check_gradients` against l10 and l12, from the performance task, which rebuilds the level's classes by design and checks them with the l12 checker in its postlude.
6. `rubric-passes.mjs` on `h-loss-went-up`: every row can be left out of a pass (no row required; it is not a performance item).

## Final class sources (level 3)

The `Value` class is level 2's (see `docs/reports/backprop-2.md`) plus homework 2's methods and `tanh()`:

```python
    def __pow__(self, k):
        out = Value(self.data ** k, (self,), f"**{k}")

        def _backward():
            self.grad += k * self.data ** (k - 1) * out.grad
        out._backward = _backward
        return out

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def exp(self):
        out = Value(math.exp(self.data), (self,), "exp")

        def _backward():
            self.grad += out.data * out.grad
        out._backward = _backward
        return out

    def tanh(self):
        t = math.tanh(self.data)
        out = Value(t, (self,), "tanh")

        def _backward():
            self.grad += (1 - t * t) * out.grad
        out._backward = _backward
        return out
```

```python
import random


class Neuron:
    def __init__(self, nin, rng):
        self.w = [Value(rng.uniform(-1, 1)) for _ in range(nin)]
        self.b = Value(rng.uniform(-1, 1))

    def __call__(self, x):
        act = sum((wi * xi for wi, xi in zip(self.w, x)), self.b)
        return act.tanh()

    def parameters(self):
        return self.w + [self.b]


class Layer:
    def __init__(self, nin, nout, rng):
        self.neurons = [Neuron(nin, rng) for _ in range(nout)]

    def __call__(self, x):
        return [n(x) for n in self.neurons]

    def parameters(self):
        return [p for n in self.neurons for p in n.parameters()]


class MLP:
    def __init__(self, nin, nouts, seed=42):
        rng = random.Random(seed)
        sizes = [nin] + list(nouts)
        self.layers = [Layer(sizes[i], sizes[i + 1], rng) for i in range(len(nouts))]

    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x[0] if len(x) == 1 else x

    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]


def train(model, X, Y, steps, lr):
    losses = []
    for k in range(steps + 1):
        loss = sum(((model(x) - y) ** 2 for x, y in zip(X, Y)), Value(0.0))
        losses.append(loss.data)
        if k == steps:
            break
        for p in model.parameters():
            p.grad = 0.0
        loss.backward()
        for p in model.parameters():
            p.data -= lr * p.grad
    return losses


def total_loss(model, X, Y):
    return sum(((model(x) - y) ** 2 for x, y in zip(X, Y)), Value(0.0))


def check_gradients(model, X, Y, h):
    params = model.parameters()
    for p in params:
        p.grad = 0.0
    total_loss(model, X, Y).backward()
    worst = 0.0
    for p in params:
        keep = p.data
        p.data = keep + h
        up = total_loss(model, X, Y).data
        p.data = keep - h
        down = total_loss(model, X, Y).data
        p.data = keep
        num = (up - down) / (2 * h)
        rel = abs(p.grad - num) / max(abs(p.grad), abs(num), 1e-12)
        worst = max(worst, rel)
    return worst
```

What the level 4 contract builds on: `MLP(2, [3, 1], seed=42).parameters()` lists the 13 draws of `random.Random(42).uniform(-1, 1)` in the order hidden neuron 1 (weight on $x_1$, weight on $x_2$, bias), neuron 2, neuron 3, then the output (three weights, bias); so the layer-1 weight matrix is rows $(p_0, p_1)$, $(p_3, p_4)$, $(p_6, p_7)$ with biases $(p_2, p_5, p_8)$, and the output row is $(p_9, p_{10}, p_{11})$ with bias $p_{12}$. Every layer applies tanh, the output included; the loss is the sum (not the mean) of squared errors on `X4`, `Y4`; the attribute names `data`, `grad`, `_prev` (a tuple), `_op`, `_backward` and `backward()` match the contract's `Tensor`. A `Tensor` rebuild of this network must give loss 5.556800 at the start and 0.025020 after 200 steps at 0.05 (the contract's own loss is a mean, so a check against these figures uses a sum or multiplies by 4).

## Proposed course.json change

None.

## Backlog

Two bullets under "Raised later (backprop level 3)".
