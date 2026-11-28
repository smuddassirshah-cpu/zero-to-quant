"""gpt level 2 ops: the tiny GPT's vocabulary, its weights files and a plain NumPy forward pass.

The model is seq_ops_l4's pre-norm block stacked into a character language model (ReLU MLP, every linear layer with a bias,
learned positions, a final layer norm and an untied head with a bias). Rows are positions, so a vector times a matrix is x @ W.
Weights are a dict of float64 arrays named as below; a block's arrays carry the prefix h<i>. ("h0.qkv_w").
    VOCAB, CONFIG                      the 65 characters in sorted order; V 65, T 32, d 32, n_head 4, n_layer 1, mlp 128
    encode(text), decode(ids)          characters to ids in VOCAB and back
    shapes(config)                     [(name, shape)] in file order: wte, wpe, h<i>.<key> for every block, lnf_g, lnf_b, head_w, head_b
    load_weights(*texts)               one dict from JSON texts of {name: {"shape": [...], "b64": little-endian float32}}
    read_weights(*paths)               load_weights on files ("gpt-w-embed.json", "gpt-w-block0.json")
    weights_json(weights, names)       the JSON text of the named arrays (float32, base64), the format load_weights reads
    to_model(weights, n_layer=None)    the same arrays as a seq_ops_l4 model dict (E, P, blocks, lnf_g, lnf_b, U, c)
    forward_cache(weights, idx)        every intermediate array of one forward pass, as a dict (see its docstring)
    forward_logits(weights, idx)       logits (..., T, V) for integer ids (..., T), T at most the context
    mean_loss(weights, idx, targets)   mean cross-entropy in nats of the next-character predictions
    sample_text(weights, prompt, n, temperature=1.0, top_k=None, seed=0)    prompt plus n sampled characters
Checked against seq_ops_l4.lm_logits in docs/reports/gpt-L2-numbers.py. Frozen once merged: later levels and courses import it.
"""
__version__ = "1.0"

import base64
import json

import numpy as np

VOCAB = "\n !$&',-.3:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
CONFIG = {"V": 65, "T": 32, "d": 32, "n_head": 4, "n_layer": 1, "mlp": 128}
BLOCK = ("ln1_g", "ln1_b", "qkv_w", "qkv_b", "proj_w", "proj_b", "ln2_g", "ln2_b", "fc_w", "fc_b", "out_w", "out_b")
_STOI = {c: i for i, c in enumerate(VOCAB)}


def encode(text):
    """The id of each character of `text` in VOCAB."""
    return [_STOI[c] for c in text]


def decode(ids):
    """The characters of a list of ids."""
    return "".join(VOCAB[int(i)] for i in ids)


def shapes(config=CONFIG):
    """[(name, shape)] for every array of a model with this config, in file order."""
    V, T, d, m = config["V"], config["T"], config["d"], config["mlp"]
    blk = {"ln1_g": (d,), "ln1_b": (d,), "qkv_w": (d, 3 * d), "qkv_b": (3 * d,), "proj_w": (d, d), "proj_b": (d,),
           "ln2_g": (d,), "ln2_b": (d,), "fc_w": (d, m), "fc_b": (m,), "out_w": (m, d), "out_b": (d,)}
    out = [("wte", (V, d)), ("wpe", (T, d))]
    for i in range(config["n_layer"]):
        out += [(f"h{i}.{k}", blk[k]) for k in BLOCK]
    return out + [("lnf_g", (d,)), ("lnf_b", (d,)), ("head_w", (d, V)), ("head_b", (V,))]


def load_weights(*texts):
    """Merge JSON texts of {name: {"shape", "b64"}} (little-endian float32) into one dict of float64 arrays."""
    out = {}
    for text in texts:
        for k, v in json.loads(text).items():
            if isinstance(v, dict) and "b64" in v:
                raw = np.frombuffer(base64.b64decode(v["b64"]), dtype="<f4")
                out[k] = raw.reshape(v["shape"]).astype(np.float64)
    return out


def read_weights(*paths):
    """load_weights on the text of each file."""
    texts = []
    for p in paths:
        with open(p) as f:
            texts.append(f.read())
    return load_weights(*texts)


def weights_json(weights, names):
    """JSON text of the named arrays as little-endian float32 in base64, readable by load_weights."""
    out = {}
    for k in names:
        a = np.asarray(weights[k], dtype="<f4")
        out[k] = {"shape": list(a.shape), "b64": base64.b64encode(a.tobytes()).decode("ascii")}
    return json.dumps(out)


def _n_layer(weights):
    return 1 + max([int(k.split(".")[0][1:]) for k in weights if k.startswith("h") and "." in k] or [-1])


def to_model(weights, n_layer=None):
    """The same numbers as a seq_ops_l4 model dict: qkv_w splits into Wq, Wk, Wv; proj, fc, out are Wo, W1, W2."""
    n = _n_layer(weights) if n_layer is None else n_layer
    d = weights["wte"].shape[1]
    blocks = []
    for i in range(n):
        g = lambda k: weights[f"h{i}.{k}"]  # noqa: E731
        w, b = g("qkv_w"), g("qkv_b")
        blocks.append({"ln1_g": g("ln1_g"), "ln1_b": g("ln1_b"),
                       "Wq": w[:, :d], "bq": b[:d], "Wk": w[:, d:2 * d], "bk": b[d:2 * d], "Wv": w[:, 2 * d:], "bv": b[2 * d:],
                       "Wo": g("proj_w"), "bo": g("proj_b"), "ln2_g": g("ln2_g"), "ln2_b": g("ln2_b"),
                       "W1": g("fc_w"), "b1": g("fc_b"), "W2": g("out_w"), "b2": g("out_b")})
    return {"E": weights["wte"], "P": weights["wpe"], "blocks": blocks, "lnf_g": weights["lnf_g"], "lnf_b": weights["lnf_b"],
            "U": weights["head_w"], "c": weights["head_b"]}


def _ln(x, g, b, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def _softmax(z):
    e = np.exp(z - z.max(-1, keepdims=True))
    return e / e.sum(-1, keepdims=True)


def forward_cache(weights, idx, n_head=4):
    """One forward pass, keeping every intermediate array (float64).

    Keys: "x0" (embedding plus position), and for block i: "h<i>.ln1", "h<i>.q", "h<i>.k", "h<i>.v" (..., heads, T, d/heads),
    "h<i>.att" (..., heads, T, T), "h<i>.z" (heads joined, before proj), "h<i>.attn_out", "h<i>.mid" (stream after attention),
    "h<i>.ln2", "h<i>.hidden" (after ReLU), "h<i>.mlp_out", "h<i>.post" (stream after the block); then "lnf", "logits".
    """
    idx = np.asarray(idx)
    T = idx.shape[-1]
    d = weights["wte"].shape[1]
    dh = d // n_head
    x = weights["wte"][idx] + weights["wpe"][:T]
    c = {"x0": x}
    mask = np.triu(np.full((T, T), -np.inf), 1)
    for i in range(_n_layer(weights)):
        g = lambda k: weights[f"h{i}.{k}"]  # noqa: E731
        a = _ln(x, g("ln1_g"), g("ln1_b"))
        qkv = a @ g("qkv_w") + g("qkv_b")
        heads = [np.swapaxes(qkv[..., j * d:(j + 1) * d].reshape(*idx.shape, n_head, dh), -2, -3) for j in range(3)]
        q, k, v = heads
        att = _softmax(q @ np.swapaxes(k, -1, -2) / np.sqrt(dh) + mask)
        z = np.swapaxes(att @ v, -2, -3).reshape(*idx.shape, d)
        ao = z @ g("proj_w") + g("proj_b")
        x = x + ao
        c.update({f"h{i}.ln1": a, f"h{i}.q": q, f"h{i}.k": k, f"h{i}.v": v, f"h{i}.att": att, f"h{i}.z": z,
                  f"h{i}.attn_out": ao, f"h{i}.mid": x})
        a2 = _ln(x, g("ln2_g"), g("ln2_b"))
        hid = np.maximum(a2 @ g("fc_w") + g("fc_b"), 0.0)
        mo = hid @ g("out_w") + g("out_b")
        x = x + mo
        c.update({f"h{i}.ln2": a2, f"h{i}.hidden": hid, f"h{i}.mlp_out": mo, f"h{i}.post": x})
    c["lnf"] = _ln(x, weights["lnf_g"], weights["lnf_b"])
    c["logits"] = c["lnf"] @ weights["head_w"] + weights["head_b"]
    return c


def forward_logits(weights, idx, n_head=4):
    """Next-character logits (..., T, V) for integer ids (..., T)."""
    return forward_cache(weights, idx, n_head)["logits"]


def mean_loss(weights, idx, targets, n_head=4):
    """Mean of -ln p(target) over every position, in nats."""
    z = forward_logits(weights, idx, n_head)
    z = z - z.max(-1, keepdims=True)
    lp = z - np.log(np.exp(z).sum(-1, keepdims=True))
    return float(-np.take_along_axis(lp, np.asarray(targets)[..., None], -1).mean())


def sample_text(weights, prompt, n, temperature=1.0, top_k=None, seed=0, n_head=4):
    """`prompt` followed by n characters, each drawn from the last position's distribution (window: the last T ids).

    temperature 0 takes the most likely character; top_k keeps the k largest logits. Draws use default_rng(seed).choice.
    """
    rng = np.random.default_rng(seed)
    T = weights["wpe"].shape[0]
    ids = encode(prompt)
    for _ in range(n):
        z = forward_logits(weights, np.array(ids[-T:]), n_head)[-1]
        if temperature == 0:
            ids.append(int(np.argmax(z)))
            continue
        z = z / temperature
        if top_k is not None:
            z = np.where(z < np.sort(z)[-top_k], -np.inf, z)
        ids.append(int(rng.choice(len(z), p=_softmax(z))))
    return decode(ids)
