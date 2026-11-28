# The two code items of topic-2.7 (difficulty 5). Executed by build.py in its own namespace (fb, r, items, DATA, np, os).
# Route A writes each expect by running the model solution here in CPython; check_numbers.py re-runs everything from the
# written file and recomputes the expects by a second route (the shipped cnn_ops_l3 and seq_ops_l3 modules).

CNN_PRELUDE = '''import json
import numpy as np

_DIG = "0123456789abcdefg"


def _held_out(path="cnn-digits.txt"):
    xs, ys = [], []
    for line in open(path, encoding="utf8"):
        line = line.strip()
        if line and not line.startswith("#") and line[0] == "h":
            ys.append(int(line[1]))
            xs.append([_DIG.index(ch) for ch in line[2:66]])
    return np.array(xs, dtype=float).reshape(-1, 1, 8, 8) / 16.0, np.array(ys)


X_test, y_test = _held_out()
EXIT = [np.array(a, dtype=float) for a in json.load(open("cnn-w-exit.json"))]


def planted(seed, filters=1, symmetric=False, shift=0.0):
    """A random net of the exit net's layout with `filters` filters; a symmetric kernel reads the same flipped."""
    g = np.random.default_rng(seed)
    W = g.standard_normal((filters, 1, 3, 3))
    if symmetric:
        W = (W + W[:, :, ::-1, ::-1]) / 2
    return [W, g.standard_normal(filters) + shift, g.standard_normal((16 * filters, 10)), g.standard_normal(10)]
'''

CNN_STARTER = '''import numpy as np


def cnn_logits_np(params, X):
    # params = [W (F, 1, 3, 3), b (F,), V (16F, 10), c (10,)]; X (N, 1, 8, 8)
    # conv 3 by 3, unflipped, stride 1, padding 1; ReLU; 2 by 2 max pool; flatten channel first; h V + c
    ...


def held_out_accuracy(params, X, y):
    # the share of images whose largest logit is at the label
    ...
'''

CNN_SOLUTION = '''import numpy as np


def cnn_logits_np(params, X):
    W, b, V, c = (np.asarray(a, dtype=float) for a in params)
    X = np.asarray(X, dtype=float)
    n, _, H, Wd = X.shape
    F = W.shape[0]
    P = np.pad(X[:, 0], ((0, 0), (1, 1), (1, 1)))
    cols = np.stack([P[:, i:i + H, j:j + Wd] for i in range(3) for j in range(3)], axis=-1)
    conv = cols @ W.reshape(F, 9).T + b
    h = np.maximum(conv, 0.0)
    h = h.reshape(n, H // 2, 2, Wd // 2, 2, F).max(axis=(2, 4))
    flat = h.transpose(0, 3, 1, 2).reshape(n, -1)
    return flat @ V + c


def held_out_accuracy(params, X, y):
    pred = cnn_logits_np(params, X).argmax(axis=1)
    return float(np.mean(pred == np.asarray(y)))
'''


def mutate(src, old, new):
    assert src.count(old) == 1, old
    return src.replace(old, new)


CNN_MUTANTS = [
    (mutate(mutate(mutate(CNN_SOLUTION, "P = np.pad(X[:, 0], ((0, 0), (1, 1), (1, 1)))", "P = X[:, 0]"),
                   "P[:, i:i + H, j:j + Wd]", "P[:, i:i + H - 2, j:j + Wd - 2]"),
            "h.reshape(n, H // 2, 2, Wd // 2, 2, F)", "h.reshape(n, (H - 2) // 2, 2, (Wd - 2) // 2, 2, F)"),
     "No padding: the 8 by 8 map shrinks to 6 by 6 and the dense layer gets 144 numbers, not 256."),
    (mutate(CNN_SOLUTION, ".max(axis=(2, 4))", ".mean(axis=(2, 4))"), "Average pooling where the net was trained with max pooling."),
    (mutate(CNN_SOLUTION, "h = np.maximum(conv, 0.0)", "h = conv"), "No ReLU after the convolution."),
    (mutate(CNN_SOLUTION, "W.reshape(F, 9)", "W[:, :, ::-1, ::-1].reshape(F, 9)"),
     "The textbook flipped convolution instead of the unflipped slide."),
    (mutate(CNN_SOLUTION, "h.transpose(0, 3, 1, 2).reshape(n, -1)", "h.reshape(n, -1)"),
     "Flattens position first, so the rows of V meet the wrong numbers."),
    (mutate(CNN_SOLUTION, "pred == np.asarray(y)", "pred != np.asarray(y)"), "Returns the error rate, not the accuracy."),
    (mutate(CNN_SOLUTION, ".argmax(axis=1)", ".argmax(axis=0)"), "Takes the largest logit down each column, over the images."),
]

ATT_PRELUDE = '''import numpy as np


def make_params(seed, d, flat=False, plain_out=False):
    """Wq, Wk, Wv and Wo, each d by d; flat sets Wq and Wk to 0 (every score 0), plain_out sets Wo to the identity."""
    g = np.random.default_rng(seed)
    P = {k: g.standard_normal((d, d)) / np.sqrt(d) for k in ("Wq", "Wk", "Wv", "Wo")}
    if flat:
        P["Wq"], P["Wk"] = np.zeros((d, d)), np.zeros((d, d))
    if plain_out:
        P["Wo"] = np.eye(d)
    return P


def make_x(seed, T, d):
    return np.random.default_rng(seed + 100).standard_normal((T, d))
'''

ATT_STARTER = '''import numpy as np


def padded_attention(X, params, h, pad):
    # X (T, d); params: Wq, Wk, Wv, Wo, each d by d, no biases; pad[j] True where position j is padding
    # h heads of width d // h; scores over sqrt(d // h); key j allowed for query i when j <= i and not pad[j];
    # softmax over the keys; a query with no allowed key gives zeros; join the heads, then times Wo
    ...
'''

ATT_SOLUTION = '''import numpy as np


def padded_attention(X, params, h, pad):
    X = np.asarray(X, dtype=float)
    T, d = X.shape
    dk = d // h
    pad = np.asarray(pad, dtype=bool)

    def split(M):
        return M.reshape(T, h, dk).transpose(1, 0, 2)

    Q, K, V = (split(X @ params[k]) for k in ("Wq", "Wk", "Wv"))
    S = Q @ K.transpose(0, 2, 1) / np.sqrt(dk)
    allowed = np.tril(np.ones((T, T), dtype=bool)) & ~pad[None, :]
    S = np.where(allowed, S, -np.inf)
    out = np.zeros((h, T, dk))
    rows = allowed.any(axis=1)
    Sr = S[:, rows]
    E = np.exp(Sr - Sr.max(axis=-1, keepdims=True))
    out[:, rows] = (E / E.sum(axis=-1, keepdims=True)) @ V
    return out.transpose(1, 0, 2).reshape(T, d) @ params["Wo"]
'''

_ATT_TAIL = '''    out = np.zeros((h, T, dk))
    rows = allowed.any(axis=1)
    Sr = S[:, rows]
    E = np.exp(Sr - Sr.max(axis=-1, keepdims=True))
    out[:, rows] = (E / E.sum(axis=-1, keepdims=True)) @ V
'''
_ATT_PLAIN = '''    E = np.exp(S - S.max(axis=-1, keepdims=True))
    out = (E / E.sum(axis=-1, keepdims=True)) @ V
'''
_ATT_COLS = '''    E = np.exp(S - S.max(axis=-2, keepdims=True))
    out = np.nan_to_num(E / E.sum(axis=-2, keepdims=True)) @ V
'''
ATT_MUTANTS = [
    (mutate(ATT_SOLUTION, "np.tril(np.ones((T, T), dtype=bool))", "np.ones((T, T), dtype=bool)"),
     "No causal mask: every query reads later keys."),
    (mutate(ATT_SOLUTION, _ATT_TAIL, _ATT_COLS), "Softmax down each column, over the queries."),
    (mutate(ATT_SOLUTION, " / np.sqrt(dk)", ""), "Scores not scaled."),
    (mutate(ATT_SOLUTION, " / np.sqrt(dk)", " / np.sqrt(d)"), "Scales by the model width d, not the head width."),
    (mutate(ATT_SOLUTION, "M.reshape(T, h, dk).transpose(1, 0, 2)", "M.reshape(h, T, dk)"),
     "Splits by reshaping alone, so a head gets a block of positions, not of features."),
    (mutate(ATT_SOLUTION, '.reshape(T, d) @ params["Wo"]', '.reshape(T, d)'), "Forgets the output matrix Wo."),
    (mutate(ATT_SOLUTION, " & ~pad[None, :]", ""), "Ignores the padding."),
    (mutate(ATT_SOLUTION, "~pad[None, :]", "~pad[:, None]"), "Masks the padded queries instead of the padded keys."),
    (mutate(ATT_SOLUTION, _ATT_TAIL, _ATT_PLAIN), "A fully masked row goes through the softmax and gives NaN."),
    (mutate(mutate(ATT_SOLUTION, "np.where(allowed, S, -np.inf)", "np.where(allowed, S, -1e9)"), _ATT_TAIL, _ATT_PLAIN),
     "Masks with -1e9, so a fully masked row spreads its weight over every key."),
]


def run_cases(prelude, src, cases, cwd):
    """Route A: run the code as the page does (prelude, code, then each setup and call) and return each result."""
    here = os.getcwd()
    os.chdir(cwd)
    try:
        ns = {}
        exec(prelude, ns)
        exec(src, ns)
        out = []
        for c in cases:
            if c.get('setup'):
                exec(c['setup'], ns)
            v = eval(c['call'], ns)
            out.append(v.tolist() if hasattr(v, 'tolist') else v)
        return out
    finally:
        os.chdir(here)


def with_expects(prelude, src, cases, cwd):
    for c, v in zip(cases, run_cases(prelude, src, cases, cwd)):
        c['expect'] = repr(v)
    return cases


def first_fail(prelude, src, tests, cwd):
    """The first hidden test the source fails, in route A's own run (check_numbers.py re-runs each mutant)."""
    here = os.getcwd()
    os.chdir(cwd)
    try:
        ns = {}
        exec(prelude, ns)
        exec(src, ns)
        for k, c in enumerate(tests):
            try:
                if c.get('setup'):
                    exec(c['setup'], ns)
                got = eval(c['call'], ns)
                got = got.tolist() if hasattr(got, 'tolist') else got
                want = eval(c['expect'])
                if c['compare'] == 'equal':
                    ok = got == want
                else:
                    ok = bool(np.allclose(np.asarray(got, dtype=float), np.asarray(want, dtype=float), rtol=0, atol=1e-9))
            except Exception:
                ok = False
            if not ok:
                return k + 1
        return None
    finally:
        os.chdir(here)


def mutants_of(prelude, ms, tests):
    out = []
    for src, symptom in ms:
        n = first_fail(prelude, src, tests, DATA)
        assert n is not None, symptom
        out.append({"source": src, "test": n, "symptom": symptom})
    return out


TOL9 = {"rel": 0, "abs": 1e-9}

cnn_tests = [
    {"call": "list(cnn_logits_np(EXIT, X_test[:5]).shape)", "compare": "equal"},
    {"call": "cnn_logits_np(planted(1, 1, True, 20.0), X_test[:4])", "compare": "isclose", "tol": TOL9},
    {"call": "cnn_logits_np(planted(2, 1, True, -1.0), X_test[:4])", "compare": "isclose", "tol": TOL9},
    {"call": "cnn_logits_np(planted(3), X_test[:4])", "compare": "isclose", "tol": TOL9},
    {"call": "cnn_logits_np(planted(4, 3), X_test[:4])", "compare": "isclose", "tol": TOL9},
    {"call": "cnn_logits_np(EXIT, X_test[:3])", "compare": "isclose", "tol": TOL9},
    {"call": "held_out_accuracy(EXIT, X_test, y_test)", "compare": "isclose", "tol": TOL9},
    {"call": "held_out_accuracy(EXIT, X_test, y_test) >= 0.95", "compare": "equal"},
]
cnn_examples = [
    {"call": "list(cnn_logits_np(EXIT, X_test[:2]).shape)", "compare": "equal"},
    {"call": "int(cnn_logits_np(EXIT, X_test[:1]).argmax())", "compare": "equal"},
]
with_expects(CNN_PRELUDE, CNN_SOLUTION, cnn_tests, DATA)
with_expects(CNN_PRELUDE, CNN_SOLUTION, cnn_examples, DATA)
acc31 = eval(cnn_tests[6]['expect'])
right31 = round(acc31 * 540)

att_tests = [
    {"setup": "P = make_params(1, 4, True, True); X = make_x(1, 4, 4)", "call": "padded_attention(X, P, 1, [False] * 4)"},
    {"setup": "P = make_params(2, 4, False, True); X = make_x(2, 4, 4)", "call": "padded_attention(X, P, 1, [False] * 4)"},
    {"setup": "P = make_params(3, 4, False, True); X = make_x(3, 5, 4)", "call": "padded_attention(X, P, 2, [False] * 5)"},
    {"setup": "P = make_params(4, 4); X = make_x(4, 5, 4)", "call": "padded_attention(X, P, 2, [False] * 5)"},
    {"setup": "P = make_params(5, 4); X = make_x(5, 5, 4)", "call": "padded_attention(X, P, 2, [False, True, False, False, True])"},
    {"setup": "P = make_params(6, 4); X = make_x(6, 4, 4)", "call": "padded_attention(X, P, 2, [True, True, False, False])"},
    {"setup": "P = make_params(7, 4); X = make_x(7, 3, 4)", "call": "padded_attention(X, P, 2, [True] * 3)"},
    {"setup": "P = make_params(8, 8); X = make_x(8, 6, 8)", "call": "padded_attention(X, P, 4, [True, False, False, True, False, False])"},
]
for c in att_tests:
    c.update({"compare": "isclose", "tol": TOL9})
att_examples = [
    {"setup": "P = make_params(0, 2, True, True)", "call": "padded_attention(np.eye(2), P, 1, [False, False])",
     "compare": "isclose", "tol": TOL9},
    {"setup": "P = make_params(0, 2, True, True)", "call": "padded_attention(np.eye(2), P, 1, [True, False])",
     "compare": "isclose", "tol": TOL9},
]
with_expects(ATT_PRELUDE, ATT_SOLUTION, att_tests, DATA)
with_expects(ATT_PRELUDE, ATT_SOLUTION, att_examples, DATA)

cnn_widget = {
    "kind": "code", "language": "python", "starter": CNN_STARTER, "solution": CNN_SOLUTION, "prelude": CNN_PRELUDE,
    "data": {"cnn-digits.txt": "content/data/ai/cnn-digits.txt", "cnn-w-exit.json": "content/data/ai/cnn-w-exit.json"},
    "examples": cnn_examples, "tests": cnn_tests, "budget": 3000,
    "how": "Submit runs 8 hidden tests, each within $10^{-9}$ of ours. Four planted nets isolate the pooling, the ReLU, "
           "the kernel's orientation and the flatten order. The rest check the exit net's shape, logits and held-out "
           "accuracy, exactly and against 0.95. Digits: Alpaydin and Kaynak, UCI Machine Learning Repository, CC BY 4.0, "
           "via scikit-learn; the weights were trained on them for this course.",
    "mutants": mutants_of(CNN_PRELUDE, CNN_MUTANTS, cnn_tests),
}
items.append({
    "id": "e-cnn-exit", "difficulty": 5, "skills": ["cnn-train", "cnn-conv"], "tags": ["cnn-forward"], "pace": 720,
    "title": "The digits net in NumPy",
    "prose": "The held-out split of the course digits is loaded as `X_test` (540 images of shape $(1, 8, 8)$, grey levels "
             "divided by 16) with labels `y_test`. `EXIT` holds the exit net's weights `[W, b, V, c]`: `W` is "
             "$(16, 1, 3, 3)$, `b` is $(16,)$, `V` is $(256, 10)$ and `c` is $(10,)$. `planted(seed, filters, symmetric, "
             "shift)` makes random nets of the same layout for testing.",
    "question": "Write `cnn_logits_np(params, X)` in NumPy alone. It slides a 3 by 3 convolution unflipped with stride 1 "
                "and padding 1, applies ReLU and 2 by 2 max pooling, flattens channel first, then returns "
                "$\\mathbf h\\mathbf V + \\mathbf c$. Then "
                "write `held_out_accuracy(params, X, y)`, the share of images whose largest logit is at the label. This "
                "exam's check asks for at least 0.95 held out.",
    "widget": cnn_widget,
    "feedback": fb(f"The exit net reads {right31} of the 540 held-out digits, {r(acc31, 4)}, above the 0.95 the check asks for.",
                   "Read the first failing test.",
                   {"test-1": "The output is one row of 10 logits per image. Pad each side by 1 so the 8 by 8 map stays "
                              "8 by 8. Pooling then leaves 16 maps of 4 by 4, the 256 numbers `V` expects.",
                    "test-2": "Keep the largest value of each 2 by 2 window, not the mean.",
                    "test-3": "Apply ReLU to the convolution plus its bias, before the pool.",
                    "test-4": "Slide the kernel unflipped: output $(i, j)$ is $\\sum_{a,b} W_{ab}\\,x_{i+a,\\,j+b}$ over the "
                              "padded image, not the textbook flipped convolution.",
                    "test-5": "Flatten each image's pooled maps channel first, as `h.reshape(N, -1)` does on an "
                              "$(N, F, 4, 4)$ array, so the rows of `V` meet the right numbers.",
                    "test-7": "Take the largest logit along each row, `argmax(axis=1)`, compare it with the label, and "
                              "return the share that match."}),
    "explain": {"text": f"Convolution, ReLU, pooling and one dense layer read {right31} of 540 held-out digits right. "
                        "Each planted test fixes one convention the weights were trained with: unflipped kernels, ReLU "
                        "before the pool, the maximum of each window and channel-first flattening."}})

att_widget = {
    "kind": "code", "language": "python", "starter": ATT_STARTER, "solution": ATT_SOLUTION, "prelude": ATT_PRELUDE,
    "examples": att_examples, "tests": att_tests,
    "how": "Submit runs 8 hidden tests, each within $10^{-9}$ of ours. Four cover one head with every score 0, one head, "
           "two heads, and two heads with `Wo`. Four cover padding inside a sequence, padding at the start, a sequence of "
           "padding only, and a mixed case with four heads.",
    "mutants": mutants_of(ATT_PRELUDE, ATT_MUTANTS, att_tests),
}
items.append({
    "id": "e-padded-heads", "difficulty": 5, "skills": ["sqn-self", "sqn-attend"], "tags": ["masked-attention"], "pace": 720,
    "title": "Heads with padding",
    "prose": "Sequences of different lengths share a batch by padding: `pad[j]` is True where position $j$ holds no token. "
             "Query $i$ may attend to key $j$ only when $j \\le i$ and position $j$ is not padding. A query with no such key "
             "outputs a row of zeros: a whole row of $-\\infty$ through a softmax gives NaN. A padded query follows the same rule; "
             "its output is ignored later. `make_params(seed, d, flat, "
             "plain_out)` and `make_x(seed, T, d)` build test inputs.",
    "question": "Write `padded_attention(X, params, h, pad)` for `X` of shape $(T, d)$ and `params` holding `Wq`, `Wk`, `Wv` "
                "and `Wo`, each $d$ by $d$, with no biases. Split the projections into `h` heads of width $d/h$, head $k$ "
                "taking features $k\\,d/h$ to $(k + 1)\\,d/h - 1$. Divide each head's scores by $\\sqrt{d/h}$, mask, take "
                "the softmax over the keys, join the heads and multiply by `Wo`.",
    "widget": att_widget,
    "feedback": fb("Causal and padding masks combine into one set of allowed keys per query, and a query with none returns zeros.",
                   "Read the first failing test.",
                   {"test-1": "Each query averages only the keys at or before it. Add the mask to the scores, then take "
                              "the softmax across each row, over the keys.",
                    "test-2": "Divide the scores by $\\sqrt{d/h}$ before the softmax.",
                    "test-3": "Cut the features into heads, `X @ W` reshaped to $(T, h, d/h)$ then transposed to "
                              "$(h, T, d/h)$, and scale by the head's width $d/h$, not by $d$.",
                    "test-4": "Multiply the joined heads by `Wo`.",
                    "test-5": "Mask the keys at padded positions, the columns of the scores, for every query.",
                    "test-6": "A query whose keys are all masked must output zeros. A row of $-\\infty$ gives NaN, and a "
                              "large negative number spreads the weight over every key: handle that row on its own."}),
    "explain": {"text": "A padding mask is one more set of keys a query may not see, added to the scores like the causal "
                        "mask. Left padding leaves the first queries nothing to attend to, and the safe answer for such a "
                        "row is zeros, as the course's `seq_ops_l3.attention` gives."}})
