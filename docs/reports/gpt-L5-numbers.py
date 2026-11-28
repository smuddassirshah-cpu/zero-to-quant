"""Recompute every number stated in gpt level 5 (Hardware and precision) and check each at its JSON path.

Run through the CI runner from app/: node tools/run-number-scripts.mjs --python <venv> --only gpt-L5
(NumPy only; strict coverage; a few seconds; exits 0 when every check passes).

Every figure is computed twice. Rounding to bf16 and fp16 is exact: bf16 by float32 bit manipulation and by math.frexp
(and checked against known values: 1 + 2^-7, the ties near 1, the largest fp16 65,504), fp16 by NumPy's float16 and by
math.frexp. Roofline, memory and cache figures by the closed formula and by a written-out product or sum. The KV-cached
decoder of gpt_ops_l5 is checked against gpt_ops_l2's full forward pass and sampler. Every code widget is run in CPython
with the page's judge (solution passes, starter fails, each mutant first fails its named test).
"""
import hashlib
import math
import os
import shutil
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', 'app')
DATA = os.path.join(APP, 'content', 'data', 'ai')
sys.path.insert(0, os.path.join(APP, 'tools'))
from numbers_lib import Level, ZQ_LIB  # noqa: E402

sys.path.insert(0, DATA)
import gpt_ops_l2 as G2  # noqa: E402
import gpt_ops_l5 as G5  # noqa: E402

lv = Level('gpt', 5, coverage='strict')
E = lv.expect
LIT = lv.literal


def F(fid):
    return lv._file(fid)[1]


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def two(label, a, b, tol=1e-9, covers=None):
    lv.claim(close(a, b, tol), f'{label}: two routes agree ({a!r} vs {b!r})', covers=[a] if covers is None else covers)
    return a


# ---------------- the rounding functions: two methods, and known values ----------------
def bf16_bits(x):
    return G5.to_bf16(x)


def bf16_frexp(x):
    return G5.round_bits(x, 8, 127)


def fp16_np(x):
    with np.errstate(over='ignore'):
        return float(np.float16(x))


def fp16_frexp(x):
    return G5.round_bits(x, 11, 15)


known = {1 + 2 ** -7: 1.0078125, 1 + 2 ** -8: 1.0, 1 + 3 * 2 ** -8: 1.015625, 257: 256.0, 0.1: 0.10009765625, 3.14159: 3.140625, 1000.3: 1000.0, 2.718: 2.71875,
         101.37: 101.5, 70000: 70144.0, -0.1: -0.10009765625, 6.02: 6.03125, 6.04125: 6.03125, 4.01: 4.0, 0.5015: 0.5, 1.001: 1.0}
for x, want in known.items():
    lv.claim(bf16_bits(x) == bf16_frexp(x) == want, f'bf16({x}) = {want} by bits and by frexp', covers=[x, want])
fknown = {2049: 2048.0, 2051: 2052.0, 65519: 65504.0, 65504: 65504.0, 1 + 2 ** -10: 1.0009765625, 0.1: 0.0999755859375, 3.14159: 3.140625, 1000.3: 1000.5}
for x, want in fknown.items():
    lv.claim(fp16_np(x) == fp16_frexp(x) == want, f'fp16({x}) = {want} by NumPy and by frexp', covers=[x, want])
lv.claim(fp16_np(65520) == fp16_frexp(65520) == math.inf and fp16_np(70000) == math.inf, 'fp16 overflows from 65,520', covers=[65520, 65536])
lv.claim(float(np.finfo(np.float16).max) == 65504 == (2 - 2 ** -10) * 2 ** 15, 'largest fp16 65,504', covers=[65504])
lv.claim(float(np.finfo(np.float16).eps) == 2 ** -10 == 0.0009765625 and bf16_bits(1 + 2 ** -7) - 1 == 2 ** -7 == 0.0078125, 'epsilons', covers=[2 ** -10, 2 ** -7, 2 ** -8, 0.0009765625, 0.000977, 0.0039, 0.00390625])
B16MAX = (2 - 2 ** -7) * 2 ** 127
lv.claim(bf16_bits(3.3895e38) == B16MAX and round(B16MAX / 1e38, 2) == 3.39 and round(float(np.finfo(np.float32).max) / 1e38, 2) == 3.40
         and round(2 ** -126 / 1e-38, 2) == 1.18 and round(2 ** -14 / 1e-5, 2) == 6.10 and round(2 ** -24 / 1e-8, 2) == 5.96, 'format limits',
         covers=[3.39, 3.40, 1.18, 6.10, 5.96, 2 ** -24])
lv.claim(fp16_np(2e-8) == 0 and fp16_np(2e-8 * 4096) > 2 ** -14, 'loss scaling: 2e-8 underflows, times 4,096 is normal', covers=[2e-8, 8.192e-5, 8.192, 4096])
lv.claim(abs(70144 - 70000) / 70000 < 0.0021 and 2 ** (16 - 7) == 512, 'bf16 70,144, 0.2%, gaps of 512', covers=[0.002, 512, 70144, 70000])

# stalled totals
two('bf16 total of a thousand 1s', G5.bf16_sum([1.0] * 1000), float(np.float32(256)), covers=[256])
t16 = 0.0
for _ in range(5000):
    t16 = fp16_np(t16 + 1)
two('fp16 total stalls at 2,048', t16, 2 ** 11, covers=[2048, 2 ** 11])
two('float32 accumulator reaches 1,000', G5.fp32_then_bf16([1.0] * 1000), 1000.0, covers=[1000])
two('float32 accumulator of 4,000 quarters', G5.fp32_then_bf16([0.25] * 4000), 1000.0)
w32 = np.float32(1.0)
for _ in range(1000):
    w32 = np.float32(w32 + np.float32(0.001))
wb = 1.0
for _ in range(1000):
    wb = bf16_bits(wb + 0.001)
lv.claim(abs(float(w32) - 2) < 1e-3 and wb == 1.0, 'a thousand updates of 0.001: float32 about 2.0, bf16 stays 1', covers=[2.0, 0.001, 1.0])
lv.claim(float(np.float32(12345678.91)) == 12345679.0 and 2 ** 23 <= 12345678.91 < 2 ** 24 and round((12345679 - 12345678.91) * 100) == 9, 'notional in float32: 9 pence',
         covers=[12345678.91, 12345679, 9, 91, 100, 2 ** 23, 2 ** 24])
lv.claim(round(3.14159 / 0.015625, 2) == 201.06 and 201 * 0.015625 == 3.140625 and round(2.718 / 0.015625, 2) == 173.95 and 174 * 0.015625 == 2.71875, 'quiz and review roundings',
         covers=[201.06, 173.95, 0.015625, 2 ** -6, 3.15625, 2.703125])

# ---------------- l17 ----------------
PEAK, BW = 1e15, 3.3e12
two('ridge 303', PEAK / BW, 1000 / 3.3, covers=[PEAK / BW, 303, 1000, 3.3])
MV_B = 4096 * 4096 * 2
two('reading the 4,096 matrix', MV_B / BW * 1e6, 33554432 / 3.3e6, covers=[MV_B / BW * 1e6, 33554432, 2 * 4096 ** 2])
two('its arithmetic', 2 * 4096 ** 2 / PEAK * 1e6, 0.033554432, covers=[0.034, 0.03, 2 * MV_B / BW * 1e6, (MV_B / BW) / (2 * 4096 ** 2 / PEAK), 1.017e-5])
E('l17', 'screens[0].widget.answer', 10.2)
for n, want in [(128, 42.7), (1024, 341.3), (2048, 682.7), (4096, 1365.3), (512, 170.7)]:
    two(f'intensity n={n}', G5.matmul_intensity(n, n, n, 2), n / 3, covers=[round(n / 3, 1), want, 2 * n ** 3, 6 * n ** 2])
two('intensity without the 2', G5.matmul_flops(1024, 1024, 1024) / 2 / G5.matmul_bytes(1024, 1024, 1024, 2), 1024 / 6, covers=[170.7, 682.7, 512, 2147483648, 6291456, 4194304, 98304])
MVI = G5.matmul_intensity(4096, 1, 4096, 2)
two('matrix-vector intensity', MVI, 4096 / 4098, covers=[MVI, 0.9995, 3.3 * MVI, 3.298])
lv.claim(round(3.3 * 128 / 3, 1) == 140.8, 'the 128 matmul reaches 140.8', covers=[140.8, 42.67, 341.3, 1365.3])
BI = G5.matmul_intensity(64, 4096, 4096, 2)
two('batch 64 intensity', BI, 262144 / 4224, covers=[BI, 62.1, 262144, 4224, 64])
Bneed = math.ceil(303.0303 * 4096 / (4096 - 2 * 303.0303))
lv.claim(Bneed == 356 and G5.matmul_intensity(356, 4096, 4096, 2) >= PEAK / BW > G5.matmul_intensity(355, 4096, 4096, 2), 'a batch of about 356 reaches the ridge', covers=[356])
D7 = 14e9 / BW
two('7B decode', D7 * 1e3, 14 / 3.3, covers=[D7 * 1e3, 4.24, 2.12, 1 / D7, 236, 14, 2000])
lv.claim(round(128 / 1e15 * 1e9, 6) == 0.000128 and round(96 / BW * 1e9, 3) == 0.029 and (16 + 16 + 16) * 2 == 96 and 2 * 4 ** 3 == 128 and round(128 / 96, 2) == 1.33,
         '4 by 4 matmul', covers=[0.000128, 0.029, 96, 128, 1.33, 5000, 5])
lv.claim(50 * 3.3 == 165 and round(1000 / 165, 2) == 6.06, 'intensity 50 reaches 165', covers=[165, 6.06, 50])
lv.claim(close(1.6e10 / 50e9, 0.32) and close(2e9 / 100e9, 0.02) and 2 / 16 == 0.125 and close(0.32 / 2, 0.16) and sys.getsizeof(1.0) == 24 and 24 + 8 == 32,
         'signal over a billion returns', covers=[0.32, 0.02, 0.125, 0.16, 1.6e10, 2e9, 1e9, 5e10, 1e11, 50, 100, 16, 24, 8, 32])
lv.claim(400 / 2 == 200 and close(2 * 128 ** 3 / 2.1e9 * 1e3, 1.997, 1e-3) and close(128 ** 3 / 2.1e9 * 1e3, 1.0, 2e-3), 'quiz: ridge 200, 128 matmul about 2.0 ms', covers=[200, 400, 2.0, 1.0, 0.005, 2.1, 0.7, 1.997, 2.1e9])
lv.claim(PEAK == 1e15 and BW == 3.3e12 and 2000 / 1000 == 2 and 4.24 / 4 < 1.1, 'the chip in powers of ten; a second chip of twice the peak', covers=[1e15, 3.3e12, 0.25])
LIT('a third', why='an ordinal ("a third cost"), not a fraction')
E('l17', 'quiz[2].widget.answer', 2.0)

# ---------------- l18 ----------------
E('l18', 'screens[0].widget.answer', 256)
E('l18', 'screens[2].widget.answer', 0.0078125)
E('l18', 'screens[3].widget.answer', bf16_bits(1 + 3 * 2 ** -8))
lv.claim(1 + 3 * 2 ** -8 == 1.01171875 and 1 + 2 ** -7 == 1.0078125 and 1 + 3 * 2 ** -7 == 1.0234375, 'bf16 neighbours near 1', covers=[1.01171875, 1.0078125, 1.0234375, 1.015625])
E('l18', 'screens[7].widget.answer', wb)
E('l18', 'screens[8].widget.answer', 2e-8 * 4096 / 1e-5)
E('l18', 'screens[10].widget.answer', 9)
E('l18', 'quiz[0].widget.answer', 2 ** -10)
E('l18', 'quiz[1].widget.answer', bf16_bits(3.14159))
E('l18', 'quiz[2].widget.answer', t16)
NL = [v for v in range(248, 256)] + [256, 258, 260, 262, 264, 266]
lv.claim(all(bf16_bits(v) == v for v in NL) and bf16_bits(257) == 256 and bf16_bits(259) == 260, 'the bf16 numbers from 248 to 266', covers=[248, 266, 258])
lv.claim(round(2 ** -14 / 1e-5, 2) == 6.10 and 1 + 10 == 11 and 2 ** 7 - 1 == 127 and 2 ** 4 - 1 == 15, 'fp16 smallest normal; p = 11; exponents 127 and 15',
         covers=[6.10e-5, 1e-5, 11, 127, 15])
lv.claim(float(np.float32(20000.01)) != 20000.01 and 12345678 < 12345678.91 < 12345679, 'the numerics l1 example near 20,000 and the two neighbours', covers=[20000, 12345678])

# ---------------- l19 ----------------
two('7B in bf16', 7e9 * 2 / 1e9, 14, covers=[14, 7, 28, 1.4e10, 7e9])
lv.claim(2 + 2 + 4 + 4 + 4 == 16 == 4 + 4 + 4 + 4 and 2 + 2 + 2 == 6, 'sixteen bytes either way', covers=[16, 6, 8, 2, 4])
two('7B training', 7e9 * 16 / 1e9, 112, covers=[112, 98, 1.12e11, 1.12e12])
two('70B', 70e9 * 16 / 1e9, 1120, covers=[1120, 140, 70e9 * 2 / 1e9])
TINY_N = G5.n_params(65, 32, 32, 1, 128, False)
lv.claim(TINY_N == 18017 == sum(int(np.prod(s)) for _, s in G2.shapes()), 'tiny GPT 18,017 parameters', covers=[18017])
two('tiny training state', TINY_N * 32, 576544, covers=[576544, 144136, 432408, 577, 0.58, 32])
ACT = G5.activation_floats(65, 32, 32, 4, 128, 1, 16)
W = G2.read_weights(os.path.join(DATA, 'gpt-w-embed.json'), os.path.join(DATA, 'gpt-w-block0.json'))
ACT2 = sum(v.size for v in G2.forward_cache(W, np.zeros((16, 32), dtype=int)).values())
two('activation floats', ACT, ACT2, covers=[ACT, 705, 512, 180480, 7 * 32, 224, 96, 128, 64, 65])
two('activation bytes', ACT * 8, 512 * 705 * 8, covers=[ACT * 8, 2.9, ACT * 8 / 576544])
lv.claim(round(ACT * 8 / 576544) == 5, 'about five times', covers=[5])
two('34B', 34e9 * 16 / 1e9, 544, covers=[544, 68, 6.8, 7, 480, 80])
lv.claim(math.ceil(544 / 80) == 7, 'seven chips')
two('70B at 4 bits', 70e9 * 0.5 / 1e9, 35, covers=[35, 70, 280, 0.5, 3.5e10])
two('fine-tune 7B', 112 + 40, 152, covers=[152, 40, 54, 160, 8])
two('1.5B training', 1.5e9 * 16 / 1e9, 24, covers=[24, 3, 1.5])
lv.claim(13 + 3 == 16 and 26 + 3 == 29, 'q-int8', covers=[16, 29, 13])
E('l19', 'screens[5].widget.answer', ACT * 8)
E('l19', 'screens[4].widget.answer', TINY_N * 32)
E('l19', 'quiz[2].widget.answer', TINY_N * 8)
two('16 GB check for 2 GiB', 1.4e10 + 2 ** 31, 16147483648, covers=[2 ** 31, 1.4e10 + 2 ** 31])
lv.claim(0.125 / 4 < 0.05, 'a scale per group: a few per cent', covers=[])
lv.claim(70e9 * 16 == 1.12e12 and 34e9 * 16 == 5.44e11 and 1.5e9 * 16 == 2.4e10 and 35 / 140 == 0.25 and round(144136 / 1000) == 144, 'parameter counts in powers of ten; a quarter; 144 KB',
         covers=[70e9, 34e9, 1.5e9, 0.25, 144])

# ---------------- l20 ----------------
two('positions without a cache', sum(range(1, 33)), 32 * 33 // 2, covers=[528, 496, 1024, 32 * 33])
two('tiny cache', G5.kv_cache_bytes(1, 32, 32, 8), 2 * 1 * 32 * 32 * 8, covers=[16384, 8192])
GC = G5.kv_cache_bytes(12, 768, 1024, 2)
two('GPT-2 cache', GC, 37748736, covers=[GC, 36, 18, GC / 1e6, 37.7, 1048576, 2 ** 20])
SC = G5.kv_cache_bytes(32, 4096, 4096, 2)
two('7B-like cache', SC, 2 ** 31, covers=[SC, 2, 16 * 2, 32, 2 ** 35])
two('per-token GPT-2', 2 * 12 * 768 * 2, 36864, covers=[36864, 18432, 73728])
DEC = (14e9 + SC) / BW
two('7B decode with a 2 GiB cache', DEC * 1e3, (14e9 + 2147483648) / 3.3e9, covers=[DEC * 1e3, 4.89, 4.9, 1 / DEC, 204, 2147483648, 16147483648, 2.15e9])
LC = G5.kv_cache_bytes(32, 4096, 32768, 2)
two('long conversation', (14e9 + LC) / 14e9, 1 + 17179869184 / 14e9, covers=[(14e9 + LC) / 14e9, LC, 17179869184, 17.18, 1.718e10, 2.23, 1.23, 16, 32768])
lv.claim(round(16384 / 144136, 3) == 0.114 and abs(16384 / 144136 - 1 / 9) < 0.003, 'a ninth of the weights', covers=[1 / 9])
ids = G2.encode('First Citizen:\nBefore we pro')
full = G2.forward_logits(W, np.array(ids))
c = G5.new_cache(W)
md = max(float(np.abs(G5.decode_step(W, c, t) - full[i]).max()) for i, t in enumerate(ids))
lv.claim(md < 1e-12, f'cached logits match the full pass to {md:.1e} (about 1e-14)', covers=[1e-14, 1e-12, 1e-10])
ok = sum(G2.sample_text(W, 'First Citizen:\n', 40, seed=s) == G5.generate_cached(W, 'First Citizen:\n', 40, seed=s) for s in range(50))
lv.claim(ok == 50, 'generate_cached equals sample_text on 50 seeds past the window')
lv.claim(len('Before we proceed any further, hear me speak.\n') == 46 and 32 - 1 == 31 and GC == 2 * 12 * 768 * 1024 * 2, 'a 46-character prompt; 31 rows kept; width 768', covers=[46, 31, 768])

# ---------------- review, homework, problems ----------------
two('r-verdict', 600 / 2, 300, covers=[300, 600, 240, 120])
two('r-master', 2 ** -8 / 2, 0.001953125, covers=[0.001953125, 0.0015, 0.5015, 0.50390625])
two('r-13b', 13e9 * 16 / 1e9, 208, covers=[208, 26, 156])
two('r-kv', G5.kv_cache_bytes(24, 2048, 2048, 2, 8) / 2 ** 30, 3, covers=[3, 1.5, 0.375, 3 * 2 ** 30])
two('r-decode-20b', 3.3e12 / 4e10, 82.5, covers=[82.5, 4e10 / 3.3e12 * 1e3, 12.1, 41.3, 4e10, 12.12])
lv.claim(close(70 * 1, 70) and 80 - 70 == 10 and 80 - 35 == 45, 'r-quant', covers=[10, 45, 35])
for name, cfg in [('tiny', 'TINY'), ('gpt2', 'GPT2'), ('seven', 'SEVEN')]:
    pass
HW = F('homework')
w = HW['items'][0]['widget']
ns0 = {}
exec(w['prelude'], ns0)
SEVEN, GPT2 = ns0['SEVEN'], ns0['GPT2']
N7 = G5.n_params(SEVEN['V'], SEVEN['T'], SEVEN['d'], SEVEN['n_layer'], SEVEN['mlp'], SEVEN['tied'])
NG = G5.n_params(GPT2['V'], GPT2['T'], GPT2['d'], GPT2['n_layer'], GPT2['mlp'], GPT2['tied'])
lv.claim(NG == 124439808 and N7 == sum(int(np.prod(s)) for _, s in G2.shapes({'V': 32000, 'T': 4096, 'd': 4096, 'n_layer': 32, 'mlp': 16384})), 'parameter counts by formula and by shapes', covers=[144136])
two('h-vanish half gap', 2 ** -5 / 2, 0.015625, covers=[0.015625, 0.03125, 2 ** -5, 4.01, 4.03125])
LF = 2 * 80 * 8192 * 2
two('longform cache per token', LF, 2621440, covers=[LF, 140, 160, 20, 20e9 / LF, 7600, 2.62])
lv.claim(round(20e9 / LF, -2) == 7600, 'about 7,600 tokens')
two('longform ms per token', 140e9 / 6.6e12 * 1e3, 21.21, 1e-3, covers=[21, 6.6e12, 47, 1300, 28, 94, 1120])
lv.claim(round(6.6e12 / 140e9) == 47 and round(1300 / 47) == 28 and round(6.6e12 / 70e9) == 94, 'longform rates')
two('p1 cache GB', G5.kv_cache_bytes(40, 5120, 3000, 2) / 1e9, 2.4576, covers=[2.4576, 2.46, 2457600000, 1.23, 2.29, 3000, 5120])
lv.claim(round(G5.kv_cache_bytes(40, 5120, 3000, 2) / 2 ** 30, 2) == 2.29 and round(2.4576 / 2, 2) == 1.23, 'p1 slips')
P1 = (26e9 + G5.kv_cache_bytes(40, 5120, 3000, 2)) / 2e12 * 1e3
two('p1 ms', P1, 28.4576 / 2, covers=[P1, 14.23, 28.46, 13, 0.01, 52])
two('p1 tokens', 1000 / P1, 1000 / 14.2288, covers=[70.3, 76.9, 1000 / 13])
lv.claim(round(1000 / 14.23, 1) == 70.3 and round(28.46 / 2, 2) == 14.23, 'p1 from printed figures')
two('p2', 3e9 * 16 / 1e9, 48, covers=[48, 6, 12, 30, 78, 1.95, 49, 7])
lv.claim(round((48 + 30) / 40, 2) == 1.95 and math.ceil(78 / 40) == 2, 'p2 chips')
lv.claim(13e9 * 2 == 2.6e10 and 3e9 * 16 == 4.8e10 and 26e9 + 2.46e9 == 28.46e9 and 2e12 == 2 * 1e12 and 3e38 < B16MAX, 'powers of ten in the sets',
         covers=[13e9, 3e9, 28.46e9, 2e12, 3e38])
two('p3 gap', 2 ** (2 - 7), 0.03125, covers=[0.03125, 0.0078125, 0.015625])
two('p3 update', bf16_frexp(6.02), 6.03125, covers=[6.03125, 6.02, 0.01125, 0.02, 6.0])
two('p3 excess', (0.03125 - 0.02) / 0.02, 0.5625, covers=[0.5625, 56.25, 1.5625])
wp = 6.03125
for _ in range(100):
    wp = bf16_bits(wp + 0.01)
two('p3 hundred updates', wp, 6.03125, covers=[wp, 7.03125, 0.01])

# ---------------- hardware givens ----------------
for t_, why in [('1,000 TFLOP/s', 'the hypothetical chip, a given'), ('3.3 TB/s', 'the hypothetical chip, a given'), ('2,000 TFLOP/s', 'a hypothetical second chip, a given'),
                ('2 TB/s', 'a hypothetical chip, a given'), ('50 GB/s', 'a hypothetical laptop, a given'), ('100 GFLOP/s', 'a hypothetical laptop, a given'),
                ('80 GB', 'a hypothetical chip memory, a given'), ('40 GB', 'a given chip memory'), ('0.05 s', 'the timing loop length, a rule of the task'),
                ('5 microseconds', 'a hypothetical start-up cost, a given'), ('£101.37', 'a given price'), ('£12,345,678.91', 'a given notional'),
                ('£101.50', 'the bf16 value of the given price, checked above as 101.5')]:
    LIT(t_, why=why)

# ---------------- code widgets ----------------
def judge(a, ex, cmp, tol=None):
    def flat(x_):
        return x_.tolist() if hasattr(x_, 'tolist') and not isinstance(x_, (int, float, complex, str)) else x_

    def cl(x_, yv):
        x_, yv = flat(x_), flat(yv)
        if isinstance(x_, dict) and isinstance(yv, dict):
            return set(x_) == set(yv) and all(cl(x_[kk], yv[kk]) for kk in x_)
        if isinstance(x_, (list, tuple)) or isinstance(yv, (list, tuple)):
            return isinstance(x_, (list, tuple)) and isinstance(yv, (list, tuple)) and len(x_) == len(yv) and all(cl(p_, q_) for p_, q_ in zip(x_, yv))
        try:
            rt, at = (tol if tol else (1e-9, 1e-12))
            return math.isclose(float(x_), float(yv), rel_tol=rt, abs_tol=at) or float(x_) == float(yv)
        except Exception:
            return x_ == yv

    def same(x_, yv):
        x_, yv = flat(x_), flat(yv)
        if isinstance(x_, dict) and isinstance(yv, dict):
            return set(x_) == set(yv) and all(same(x_[kk], yv[kk]) for kk in x_)
        if isinstance(x_, (list, tuple)) or isinstance(yv, (list, tuple)):
            return isinstance(x_, (list, tuple)) and isinstance(yv, (list, tuple)) and len(x_) == len(yv) and all(same(p_, q_) for p_, q_ in zip(x_, yv))
        return bool(x_ == yv)
    return cl(a, ex) if cmp == 'isclose' else same(a, ex)


def first_fail(w, src):
    cwd, dd = os.getcwd(), tempfile.mkdtemp()
    for name, path in (w.get('data') or {}).items():
        shutil.copy(os.path.join(APP, path), os.path.join(dd, name))
    os.chdir(dd)
    try:
        ns_ = {'__name__': '__zq__', '__learner_source__': src}
        try:
            with np.errstate(all='ignore'):
                exec(ZQ_LIB, ns_)
                exec((w.get('prelude') or '') + '\n', ns_)
                exec(src, ns_)
        except Exception:
            return -1
        for i, c_ in enumerate(w['tests']):
            try:
                with np.errstate(all='ignore'):
                    if c_.get('setup'):
                        exec(c_['setup'], ns_)
                    got = eval(c_['call'], ns_)
                    t = c_.get('tol')
                    ok_ = judge(got, eval(c_['expect'], ns_), c_.get('compare', 'isclose'), (t.get('rel') or 0, t.get('abs') or 0) if t else None)
            except Exception:
                ok_ = False
            if not ok_:
                return i + 1
        return 0
    finally:
        os.chdir(cwd)
        shutil.rmtree(dd, ignore_errors=True)


nw = nm = 0
for fid, doc in lv.files.items():
    for u in doc.get('screens', []) + doc.get('items', []):
        w = u.get('widget') or {}
        if w.get('kind') != 'code':
            continue
        nw += 1
        lab = f'{fid} {u.get("title") or u.get("id")}'
        lv.claim(first_fail(w, w['solution']) == 0, f'{lab}: model solution passes {len(w["tests"])} tests')
        lv.claim(first_fail(w, w['starter']) != 0, f'{lab}: starter fails')
        lv.claim(len(w.get('mutants', [])) >= 2, f'{lab}: at least two mutants')
        for mu in w.get('mutants', []):
            nm += 1
            got = first_fail(w, mu['source'])
            lv.claim(got == mu['test'], f'{lab}: mutant "{mu["symptom"][:48]}" first fails test {mu["test"]} (got {got})')
print(f'code widgets {nw}, mutants {nm}')

# the shipped module is the file the widgets name (frozen once merged)
with open(os.path.join(DATA, 'gpt_ops_l5.py'), 'rb') as f:
    print('gpt_ops_l5.py sha256', hashlib.sha256(f.read()).hexdigest()[:12])
lv.check_wrongs()
lv.report()
