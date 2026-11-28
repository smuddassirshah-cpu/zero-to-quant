# backprop level 2 (The backward pass): report

## Files written

All in `app/content/courses/backprop/`, £ for money. Skills: `bp-backward` on l5 and l6, `bp-autograd` on l7 and l8; the review tags five items with each.

| File | Screens / items | Code |
|---|---|---|
| `l5-where-paths-meet.json` | 9 screens, 3 quiz items | none |
| `l6-doing-the-work-in-order.json` | 9 screens, 3 quiz items | `topo_order(node, parents)` |
| `l7-a-number-that-remembers.json` | 9 screens, 3 quiz items | `Value` forward only; `Value` with closures and right-hand methods |
| `l8-backward-in-code.json` | 9 screens, 3 quiz items | `Value.backward()` |
| `review-2.json` | 10 items, difficulty 2 to 4, `pass: 0.8` | none (one `order`, one code-reading `choice`) |
| `homework-2.json` | 6 items, difficulty 3 to 5 (two at 5) | `zero_grads` (4), `__pow__`/`__neg__`/`__sub__`/`__rsub__`/`exp` (5), performance `Value` class (5); `order` item; `longform` with a 10-point rubric |
| `problems-2.json` | 3 problems, 14 parts, difficulty 3, 4, 5 | none (one `order` part) |

Lesson shapes. l5: nudge hook on $g = (x + y)x$ at $(2, 3)$ (0.0701), frames slider showing the two contributions 5 and 2 arriving at $x$, name (paths add), a value used three times (10), the `+=` table (5 then 7), trap (Priya's `=` prints 2), edge case $x \cdot x$ at 3 (6), generalise, a gilt in two books ($-2{,}100$ per bp). l6: hook (the sum box run first leaves `y.grad` at 0), name topological order (an `order` widget with precedence rules, so any valid order passes), the recursive search on a stacked `pair` of graph and `array` (frames), a seven-node graph with two branches worked in reverse order, trap (Sam's list of every node ever made adds a stale 3: 8 against 5), edge case (an unreachable node is left out: 7 nodes), `topo_order` code (a hidden checker accepts any valid order on four graphs, a diamond among them), generalise, a swap pricer's order. l7: hook (what a number must remember, `multi`), Python operator methods in one screen (`__add__`, `__mul__`, `__rmul__`), a forward-only `Value`, the product closure (code options), a closure called by hand ($-6$, 4.5), trap (Ali's `=` closure on `v + v`: 1 against 2), edge case (numbers on either side: `2 * v` needs `__rmul__`), the class with closures, futures transfer (2,500 per point). l8: hook (`L.grad = 1`), frames slider over the reversed loop, the three steps (`order` with a forward-loop distractor), `backward()` code (seven tests: course expression, branch, $x \cdot x$, a ten-box chain, a constant, an unused node), running twice (12; 24 when the same graph is reused), trap (no reset: $-10.5$ against $-6$), edge case `x * x + 3 * x + 1` (7), generalise, a three-position P&L in pounds ($-320$ per dollar).

Graphs use the 1227 `valueLines` (forward value, `g = ...` gradient). The value used twice in one box ($x \cdot x$) is drawn with one edge labelled "both slots": the graph keeps one edge per pair of nodes (backlog).

Generators: `/tmp/claude-0/-home-user-zero-to-quant/b2245dfe-6f55-570e-8d22-d9384c33129b/scratchpad/backprop-1/` (`common2.py`, `gen2.py`, `gen2b.py`, `gen2c.py`); every code-test `expect` is the model solution's output.

## Gates

1. Validator: `node tools/validate.mjs` 0 errors; no backprop error (advisory warnings only).
2. Voice: `voice-scan.py 35` with `VOICE_BASE=app/content/courses/backprop`: 0 over 35 words, 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words.
3. Numbers: `docs/reports/backprop-L2-numbers.py` with the venv: 216 of 216 checks, exit 0. Route 1 runs the l8 model `Value`; route 2 is a central difference of each closed form. The `=` slips are recomputed by a copy of the class with `=` closures (2, 1, 4 and 1 as stated), Sam's list by a class that records every node it makes (8), and every code item's model solution is run against its hidden tests.
4. Playthrough: every L2 file with `--local-cdn <pkgs> --mobile`: all passed at 1280 and 440 (each lesson 12 checks, quiz 3/3; review 10 of 10; homework 6 of 6, 31 of 31 marks, the performance starter fails, the longform marked; problems 3 problems, 14 parts). Screens read at 440; one fix (the $x \cdot x$ edges).
5. Freshness: `fresh-check.mjs --file` on review-2 and problems-2: 0 hits (problems-2 reworded twice to clear `retold` hits against review-2, l6 and review-1). homework-2: 2 code-name hits, `backward` against l8 screen 4: `zero_grads` runs on the l8 class (prelude) and the performance task is the level's own class, so the method name is the course's API by design. One advisory on review-2 (three shared small numbers with an l7 quiz item, different setup).
6. L1 change made here: l4's code function renamed from `backward` to `all_gradients`, so that `backward` is only the `Value` method (L1 numbers script and report updated; l4 replayed green with `--mobile`).

## The final `Value` class (level 2)

```python
class Value:
    def __init__(self, data, _prev=(), _op=""):
        self.data = data
        self.grad = 0.0
        self._prev = tuple(_prev)
        self._op = _op
        self._backward = lambda: None

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), "+")

        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), "*")

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def __radd__(self, other):
        return self + other

    def __rmul__(self, other):
        return self * other

    def backward(self):
        topo, seen = [], set()

        def build(v):
            if v not in seen:
                seen.add(v)
                for p in v._prev:
                    build(p)
                topo.append(v)
        build(self)
        self.grad = 1.0
        for v in reversed(topo):
            v._backward()
```

`_prev` is a tuple (not micrograd's set), matching the `autograd.py` contract's `Tensor._prev`. Homework-2 item 2 adds `__pow__` (plain-number exponent), `__neg__` (`self * -1`), `__sub__`, `__rsub__` and `exp()`; level 3 starts from the class with those methods.

## Numbers stated (source: the numbers script)

$g = (x + y)x$ at $(2, 3)$: 10, gradients 7 and 2, nudge 0.0701; $h = xy + x^2 + 3x$: 16, 10; $x \cdot x$ at 3: 6; desk $-3{,}200 + 1{,}100 = -2{,}100$; seven-node graph $k = -2$, $m = 1$, $n = 2$, $o = 1$, gradients 1, 2, 2, 2, $-1$, 5; DFS order $a, b, e, c, d, f, L$; closure by hand $-6$ and 4.5; futures £30,000 and 2,500 per point; twice 12 (same graph 24); no reset $-10.5$ against $-6$; $x^2 + 3x + 1$ at 2: 11 and 7; P&L $0.8 \times (-400) = -320$; homework $e^{x^2 - y}$ at $(1, 0.5)$: 1.648721, 3.297443, $-1.648721$; problems 12, 3, 6; 2.5, 4, 3, 7, 0.07 (exact 0.0704); 6, 3 paths, 1, 6, and 1 for the `=` slip.

## Proposed course.json change

None.

## Backlog

Two bullets under "Raised later (backprop level 2)".
