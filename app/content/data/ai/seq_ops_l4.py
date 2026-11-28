"""sequence level 4 ops: the pre-norm transformer block and a small causal language model, on autograd.py (v1.0) Tensors.

Built on autograd.py, nt_ops_l2.py (layernorm), seq_ops_l2.py and seq_ops_l3.py (heads, masks, attention); rows are
positions, so a vector times a matrix is x @ W. Every op accepts Tensors or arrays and returns a Tensor.
    BLOCK_KEYS                       the 16 names of a block's arrays, in order
    mlp(x, p)                        relu(x @ W1 + b1) @ W2 + b2 on the last axis: each position alone
    mha(x, p, h, mask=True)          causal multi-head attention with biases: heads of width d/h, joined, then Wo, bo
    attn_update(x, p, h)             mha(layernorm(x, ln1_g, ln1_b)): what the attention sublayer adds to the stream
    mlp_update(x, p)                 mlp(layernorm(x, ln2_g, ln2_b)): what the feed-forward sublayer adds
    block(x, p, h)                   x + attn_update(x); then that + mlp_update(that). Pre-norm; x is (..., T, d)
    init_block(d, d_mlp, seed=0)     a block's arrays: weights N(0, 1/fan_in), biases 0, gains 1
    lm_logits(tokens, model, h)      E[tokens] + P[:T], every block, layernorm(lnf_g, lnf_b), then @ U + c: (..., T, vocab)
    stream(tokens, model, h)         the residual stream as arrays: after the embedding, then after each sublayer
    flat_params(model)               [(name, array)] in a fixed order: E, P, blocks.<i>.<key>, lnf_g, lnf_b, U, c
    n_params(model)                  the number of numbers in a model (or a block's dict)
    read_model(path)                 a model from a JSON file of {name: {"shape": [...], "b64": little-endian float32}}
A model is a dict: E (vocab, d), P (ctx, d), blocks (a list of block dicts), lnf_g, lnf_b (d), U (d, vocab), c (vocab).
Gradient-checked in docs/reports/sequence-L4-numbers.py. Frozen once merged: later levels and courses import it, never edit it.
"""
__version__ = "1.0"

import base64
import json

import numpy as np

from autograd import Tensor, _wrap
from nt_ops_l2 import layernorm
from seq_ops_l3 import attention, causal_mask, merge_heads, split_heads

BLOCK_KEYS = ('ln1_g', 'ln1_b', 'Wq', 'bq', 'Wk', 'bk', 'Wv', 'bv', 'Wo', 'bo', 'ln2_g', 'ln2_b', 'W1', 'b1', 'W2', 'b2')


def mlp(x, p):
    """The position-wise feed-forward net: relu(x W1 + b1) W2 + b2, acting on the last axis only."""
    x = _wrap(x)
    return (x @ p['W1'] + p['b1']).relu() @ p['W2'] + p['b2']


def mha(x, p, h, mask=True):
    """Multi-head attention with biases on (..., T, d): heads of width d/h, causal unless mask is False."""
    x = _wrap(x)
    T = x.shape[-2]
    q, k, v = (split_heads(x @ p[w] + p[b], h) for w, b in (('Wq', 'bq'), ('Wk', 'bk'), ('Wv', 'bv')))
    return merge_heads(attention(q, k, v, causal_mask(T) if mask else None)) @ p['Wo'] + p['bo']


def attn_update(x, p, h):
    """The attention sublayer's write to the stream: mha(layernorm(x))."""
    return mha(layernorm(x, p['ln1_g'], p['ln1_b']), p, h)


def mlp_update(x, p):
    """The feed-forward sublayer's write to the stream: mlp(layernorm(x))."""
    return mlp(layernorm(x, p['ln2_g'], p['ln2_b']), p)


def block(x, p, h):
    """A pre-norm transformer block: x + Attn(LN1(x)), then + MLP(LN2(.))."""
    x = _wrap(x)
    x = x + attn_update(x, p, h)
    return x + mlp_update(x, p)


def init_block(d, d_mlp, seed=0):
    """A block's arrays: weights N(0, 1/fan_in) from default_rng(seed) in BLOCK_KEYS order, biases 0, layer-norm gains 1."""
    g = np.random.default_rng(seed)
    shapes = {'Wq': (d, d), 'Wk': (d, d), 'Wv': (d, d), 'Wo': (d, d), 'W1': (d, d_mlp), 'W2': (d_mlp, d)}
    p = {}
    for k in BLOCK_KEYS:
        if k in shapes:
            p[k] = g.standard_normal(shapes[k]) / np.sqrt(shapes[k][0])
        elif k.endswith('_g'):
            p[k] = np.ones(d)
        else:
            p[k] = np.zeros(d_mlp if k == 'b1' else d)
    return p


def lm_logits(tokens, model, h):
    """Next-token logits of a causal model for integer tokens of shape (..., T), T at most the context."""
    tokens = np.asarray(tokens)
    T = tokens.shape[-1]
    x = _wrap(model['E'])[tokens] + _wrap(model['P'])[np.arange(T)]
    for p in model['blocks']:
        x = block(x, p, h)
    return layernorm(x, model['lnf_g'], model['lnf_b']) @ model['U'] + model['c']


def stream(tokens, model, h):
    """The residual stream as arrays: [x0, after attention 1, after feed-forward 1, ...], 1 + 2 * blocks entries."""
    tokens = np.asarray(tokens)
    T = tokens.shape[-1]
    x = np.asarray(model['E'], dtype=float)[tokens] + np.asarray(model['P'], dtype=float)[:T]
    out = [x]
    for p in model['blocks']:
        x = x + attn_update(x, p, h).data
        out.append(x)
        x = x + mlp_update(x, p).data
        out.append(x)
    return out


def flat_params(model):
    """[(name, array)]: E, P, blocks.<i>.<key> in BLOCK_KEYS order, lnf_g, lnf_b, U, c (keys a dict lacks are skipped)."""
    out = [(k, model[k]) for k in ('E', 'P') if k in model]
    for i, p in enumerate(model.get('blocks', [])):
        out += [(f'blocks.{i}.{k}', p[k]) for k in BLOCK_KEYS if k in p]
    out += [(k, model[k]) for k in ('lnf_g', 'lnf_b', 'U', 'c') if k in model]
    if 'blocks' not in model and 'E' not in model:
        out = [(k, model[k]) for k in BLOCK_KEYS if k in model]
    return out


def n_params(model):
    """The number of numbers in a model dict, or in one block's dict."""
    return int(sum(np.size(a.data if isinstance(a, Tensor) else a) for _, a in flat_params(model)))


def read_model(path):
    """Load {name: {"shape", "b64"}} (little-endian float32) into a model dict of float64 arrays."""
    with open(path) as f:
        raw = json.load(f)
    arr = {k: np.frombuffer(base64.b64decode(v['b64']), dtype='<f4').reshape(v['shape']).astype(np.float64)
           for k, v in raw.items() if isinstance(v, dict) and 'b64' in v}
    n = 1 + max([int(k.split('.')[1]) for k in arr if k.startswith('blocks.')] or [-1])
    model = {k: v for k, v in arr.items() if not k.startswith('blocks.')}
    model['blocks'] = [{k: arr[f'blocks.{i}.{k}'] for k in BLOCK_KEYS} for i in range(n)]
    return model
