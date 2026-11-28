"""gpt level 5 ops: low-precision rounding, roofline arithmetic, memory budgets and a KV-cached decoder for the tiny GPT.

Rounding (exact; ties go to the even neighbour):
    to_bf16(x)                         nearest bf16 value of a float (via float32 bits: add 0x7FFF plus the lowest kept bit, clear the low 16)
    round_bits(x, p, emax=None)        nearest number with p significant bits (math.frexp); above the largest finite value with that
                                       exponent limit, inf (fp16: p 11, emax 15; bf16: p 8, emax 127; subnormals are not modelled)
    to_fp16(x)                         float(np.float16(x)), NumPy's own fp16 rounding
    bf16_sum(xs), fp32_then_bf16(xs)   a running total rounded to bf16 after every add; a float32 total rounded once at the end
Roofline:
    matmul_flops(m, n, k), matmul_bytes(m, n, k, bytes_per), matmul_intensity(m, n, k, bytes_per)
                                       an (m by k) times (k by n) product: 2mnk FLOPs over (mk + kn + mn) values moved
    bound(intensity, peak_flops, bandwidth)    "memory" below the ridge peak/bandwidth, else "compute"
Memory:
    n_params(V, T, d, n_layer, mlp, tied)      the level 4 count (biases and norms included; a tied head has no bias)
    training_bytes(N, bytes_weights, bytes_grads, bytes_optimizer, master)   N times the sum of the four per-parameter sizes
    inference_bytes(N, bytes_per, kv_bytes)    weights plus the KV cache
    kv_cache_bytes(layers, d, T, bytes_per, batch=1)    2 (K and V) * layers * d * T * bytes_per * batch
    activation_floats(V, T, d, n_head, mlp, n_layer, B)  floats that gpt_ops_l2.forward_cache keeps for a batch of B windows of T
KV cache (float64, same numbers as gpt_ops_l2.forward_logits for one sequence):
    new_cache(weights)                 {"k": [per block, an (n_head, 0, dh) array], "v": [...], "pos": 0}
    decode_step(weights, cache, token) logits (V,) of one new token at position cache["pos"]; appends its keys and values
    generate_cached(weights, prompt, n, seed=0, temperature=1.0)
                                       the same text as gpt_ops_l2.sample_text(weights, prompt, n, temperature, seed=seed): cached while the
                                       window has room; once it is full the learned positions shift, so the window is re-run from scratch
Checked in docs/reports/gpt-L5-numbers.py. Frozen once merged.
"""
__version__ = "1.0"

import math

import numpy as np

from gpt_ops_l2 import VOCAB, decode, encode  # noqa: F401


# ---------------- rounding ----------------
def to_bf16(x):
    """The bf16 value nearest to x (ties to even), from x's float32 bits."""
    b = int(np.array(x, dtype=np.float32).view(np.uint32))
    b = (b + 0x7FFF + ((b >> 16) & 1)) & 0xFFFF0000
    return float(np.array(b, dtype=np.uint32).view(np.float32))


def round_bits(x, p, emax=None):
    """x rounded to p significant bits, ties to even; inf past the largest finite value when emax (the top exponent) is given."""
    if x == 0 or not math.isfinite(x):
        return float(x)
    m, e = math.frexp(abs(x))            # abs(x) = m * 2**e with 0.5 <= m < 1
    q = m * 2 ** p                       # p bits before the point; exact for a float64 x
    r = math.floor(q)
    f = q - r
    if f > 0.5 or (f == 0.5 and r % 2 == 1):
        r += 1
    y = math.ldexp(r, e - p)
    if emax is not None and y >= 2.0 ** (emax + 1):
        y = math.inf
    return math.copysign(y, x)


def to_fp16(x):
    return float(np.float16(x))


def bf16_sum(xs):
    t = 0.0
    for x in xs:
        t = to_bf16(t + x)
    return t


def fp32_then_bf16(xs):
    t = np.float32(0.0)
    for x in xs:
        t = np.float32(t + np.float32(x))
    return to_bf16(float(t))


# ---------------- roofline ----------------
def matmul_flops(m, n, k):
    return 2 * m * n * k


def matmul_bytes(m, n, k, bytes_per):
    return (m * k + k * n + m * n) * bytes_per


def matmul_intensity(m, n, k, bytes_per):
    return matmul_flops(m, n, k) / matmul_bytes(m, n, k, bytes_per)


def bound(intensity, peak_flops, bandwidth):
    return "memory" if intensity < peak_flops / bandwidth else "compute"


# ---------------- memory ----------------
def n_params(V, T, d, n_layer, mlp, tied=False):
    n = V * d + T * d + n_layer * (4 * d * d + 2 * d * mlp + 9 * d + mlp) + 2 * d
    return n if tied else n + d * V + V


def training_bytes(N, bytes_weights, bytes_grads, bytes_optimizer, master):
    return N * (bytes_weights + bytes_grads + bytes_optimizer + master)


def inference_bytes(N, bytes_per, kv_bytes):
    return N * bytes_per + kv_bytes


def kv_cache_bytes(layers, d, T, bytes_per, batch=1):
    return 2 * layers * d * T * bytes_per * batch


def activation_floats(V, T, d, n_head, mlp, n_layer, B):
    per_block = 10 * d + mlp + n_head * T           # ln1, q, k, v, z, attn_out, mid, ln2, mlp_out, post (d each), hidden, att
    return B * T * (d + n_layer * per_block + d + V)  # x0, the blocks, lnf, logits


# ---------------- KV cache ----------------
def _ln(x, g, b, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    var = ((x - mu) ** 2).mean(-1, keepdims=True)
    return g * (x - mu) / np.sqrt(var + eps) + b


def _layers(weights):
    return 1 + max([int(k.split(".")[0][1:]) for k in weights if k.startswith("h") and "." in k] or [-1])


def new_cache(weights, n_head=4):
    d = weights["wte"].shape[1]
    e = np.zeros((n_head, 0, d // n_head))
    L = _layers(weights)
    return {"k": [e.copy() for _ in range(L)], "v": [e.copy() for _ in range(L)], "pos": 0}


def decode_step(weights, cache, token, n_head=4):
    """Logits of one token at position cache["pos"], attending to every cached key and value and its own."""
    d = weights["wte"].shape[1]
    dh = d // n_head
    x = weights["wte"][token] + weights["wpe"][cache["pos"]]
    for i in range(_layers(weights)):
        g = lambda k: weights[f"h{i}.{k}"]  # noqa: E731
        qkv = _ln(x, g("ln1_g"), g("ln1_b")) @ g("qkv_w") + g("qkv_b")
        q, k, v = (qkv[j * d:(j + 1) * d].reshape(n_head, 1, dh) for j in range(3))
        cache["k"][i] = np.concatenate([cache["k"][i], k], axis=1)
        cache["v"][i] = np.concatenate([cache["v"][i], v], axis=1)
        s = q @ np.swapaxes(cache["k"][i], -1, -2) / np.sqrt(dh)          # (n_head, 1, t)
        a = np.exp(s - s.max(-1, keepdims=True))
        a = a / a.sum(-1, keepdims=True)
        z = (a @ cache["v"][i]).reshape(d)
        x = x + z @ g("proj_w") + g("proj_b")
        h = np.maximum(_ln(x, g("ln2_g"), g("ln2_b")) @ g("fc_w") + g("fc_b"), 0.0)
        x = x + h @ g("out_w") + g("out_b")
    cache["pos"] += 1
    return _ln(x, weights["lnf_g"], weights["lnf_b"]) @ weights["head_w"] + weights["head_b"]


def _prefill(weights, ids, n_head=4):
    cache = new_cache(weights, n_head)
    z = None
    for t in ids:
        z = decode_step(weights, cache, t, n_head)
    return cache, z


def generate_cached(weights, prompt, n, seed=0, temperature=1.0, n_head=4):
    rng = np.random.default_rng(seed)
    T = weights["wpe"].shape[0]
    ids = encode(prompt)
    cache, z = _prefill(weights, ids[-T:], n_head)
    for _ in range(n):
        if temperature == 0:
            nxt = int(np.argmax(z))
        else:
            zz = z / temperature
            p = np.exp(zz - zz.max())
            nxt = int(rng.choice(len(zz), p=p / p.sum()))
        ids.append(nxt)
        if cache["pos"] < T:
            z = decode_step(weights, cache, nxt, n_head)
        else:
            cache, z = _prefill(weights, ids[-T:], n_head)
    return decode(ids)
