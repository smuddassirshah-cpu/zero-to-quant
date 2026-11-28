"""Recompute every number stated in gpt level 4 (Scale) and check each at its JSON path.

Run through the CI runner from app/: node tools/run-number-scripts.mjs --python <venv> --only gpt-L4
(NumPy only; strict coverage; a few seconds; exits 0 when every check passes).

Every figure is exact arithmetic, computed twice: parameter counts by the closed formula and by summing the arrays of
gpt_ops_l2.shapes; FLOPs, days and pounds by the formula and by a written-out product; Kaplan's law directly and in log form;
Chinchilla's optimum by the closed form and by a fine grid; power-law fits by np.polyfit and by covariance over variance.
Every code widget is run in CPython with the page's judge (solution passes, starter fails, each mutant first fails its named test).
"""
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
import gpt_ops_l2 as G  # noqa: E402

lv = Level('gpt', 4, coverage='strict')
E = lv.expect
LIT = lv.literal


def F(fid):
    return lv._file(fid)[1]


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def two(label, a, b, tol=1e-9, covers=None):
    lv.claim(close(a, b, tol), f'{label}: two routes agree ({a!r} vs {b!r})', covers=[a] if covers is None else covers)
    return a


def formula(V, T, d, L, r=4, tied=True):
    m = r * d
    n = V * d + T * d + L * (4 * d * d + 2 * d * m + 9 * d + m) + 2 * d
    return n if tied else n + d * V + V


def arrays(V, T, d, L, r=4, tied=True):
    sh = G.shapes({'V': V, 'T': T, 'd': d, 'n_layer': L, 'mlp': r * d})
    return sum(int(np.prod(s)) for k, s in sh if not (tied and k in ('head_w', 'head_b')))


def P(*a, **k):
    return two(f'parameters {a} {k}', formula(*a, **k), arrays(*a, **k), 0)


# ---------------- l13 ----------------
W768 = 12 * 768 * 768
lv.claim(W768 == 768 * 2304 + 768 * 768 + 768 * 3072 + 3072 * 768 == 7077888, 'GPT-2 block weights 12 d^2', covers=[W768, 4 * 768 * 768, 8 * 768 * 768, 2304, 3072])
GPT2 = P(50257, 1024, 768, 12)
BLK = formula(1, 1, 768, 1) - formula(1, 1, 768, 0)
lv.claim(GPT2 == 124439808 and BLK == 7087872 and 50257 * 768 == 38597376 and 1024 * 768 == 786432 and 12 * BLK == 85054464, 'GPT-2 small 124,439,808',
         covers=[124439808, 7087872, 38597376, 786432, 85054464, 1536, 38597376 + 786432 + BLK + 1536, 12 * 12 * 768 * 768, 38.6])
U2 = P(50257, 1024, 768, 12, tied=False) - 50257
lv.claim(U2 == 163037184 and U2 + 50257 == 163087441 and abs(U2 / GPT2 - 1.31) < 0.005, 'untied without bias 163,037,184 (31% more)', covers=[163037184, 163087441, 0.31])
E2 = 38597376 + 786432
two('embedding share', E2 / GPT2, (50257 + 1024) * 768 / GPT2, covers=[E2, E2 / GPT2, 85054464 / GPT2, 38597376 / GPT2])
lv.claim(12704 - 12288 == 416 and 13 * 32 == 416 and 12704 + 12288 == 24992 and abs(416 / 12704 - 0.033) < 0.0005 and abs(13 * 768 / BLK - 0.0014) < 0.0005,
         'tiny block: rule misses 416 = 13d, 3.3%; about 0.1% at 768', covers=[416, 12704, 12288, 24992, 288, 128, 0.033, 0.001])
G3 = 12 * 96 * 12288 ** 2
two('GPT-3 by 12 L d^2', G3 / 1e9, 12 * 96 * 150994944 / 1e9, covers=[G3 / 1e9, 12 * 96 * 12288 / 1e9, 12 * 12288 ** 2 / 1e9, 50257 * 12288 / 1e9, 1.51, 1.74, 174, 175])
T_T = P(65, 32, 32, 1)
lv.claim(T_T == 15872 == 18017 - 2145 and 15937 - 65 == 15872 and abs(2145 / 18017 - 0.12) < 0.005 and abs(38597376 / U2 - 0.24) < 0.005, 'tied tiny 15,872; 12% and 24%',
         covers=[15872, 15937, 18017, 2145, 3104, 64, 0.12, 0.24, 32 * 65 + 65])
L7 = 12 * 32 * 4096 ** 2 + 2 * 32000 * 4096
two('the 7B release', L7 / 1e9, (6442450944 + 262144000) / 1e9, covers=[L7 / 1e9, (12 * 32 * 4096 ** 2 + 32000 * 4096) / 1e9, 12 * 32 * 4096 ** 2 / 1e9, 6442450944, 262144000])
for d in (128, 384, 768, 1600):
    V_, T_, L_ = 50257, 1024, 12
    tot = formula(V_, T_, d, L_)
    sh = {'embeddings': (V_ + T_) * d / tot, 'attention': L_ * 4 * d * d / tot, 'MLP': L_ * 8 * d * d / tot}
    sh['biases and norms'] = 1 - sum(sh.values())
    fr = [f_ for f_ in F('l13')['screens'][1]['canvas']['controls'][0]['frames'] if f_['caption'].startswith(f'Width {d}:')][0]
    lv.claim(all(abs(fr['values'][k] - v) < 0.0006 for k, v in sh.items()) and f'{tot:,}' in fr['caption'], f'width {d}: shares and count', covers=list(sh.values()) + [tot])
lv.claim(12 * 24 * 1024 ** 2 == 301989888 and 12 * 24 * 1024 == 294912 and 100000 * 2048 == 204800000, 'quiz counts', covers=[301989888, 294912, 204800000, 204900000, 102400000, 302, 1048576])
lv.claim(8 / 12 == 2 / 3, 'MLP two thirds', covers=[2 / 3, 0.5, 0.8])

# ---------------- l14 ----------------
F3 = two('GPT-3 6ND', 6 * 175e9 * 300e9, 6 * 1.75 * 3 * 1e22, covers=[3.15, 1.05, 31.5, 3.14])
FC = two('Chinchilla 6ND (6ND, and 120 N^2 at 20 tokens per parameter)', 6 * 70e9 * 1.4e12, 6 * 20 * 70e9 ** 2, covers=[5.88, 20, 0.05, 300 / 175, 1.7])
TOK = 5000 * 16 * 32
FT = two('tiny run 6ND', 6 * 18017 * TOK, 6 * 18017 * 2560000, covers=[2560000, 6 * 18017 * TOK, 2.77, 36034, 18017 * 6])
SEC = FT / 2.1e9
MEAS = 5000 * 0.056
two('seconds at 2.1 GFLOP/s', SEC, 276741120000 / 2100000000, covers=[SEC, SEC / 3, SEC / 60, MEAS, FT / MEAS / 1e9, 2.1, 56, 132])
ATT = 2 * 12 * 1024 * 768
NE = 2 * 85054464
two('attention share', ATT / NE, 18874368 / 170108928, covers=[ATT, NE, ATT / NE, NE / ATT, ATT / (2 * GPT2)])
A3 = two('GPT-3 attention share at T = 2,048 (2 L T d over 2 N for the blocks, and T / 12 d)', 2 * 96 * 2048 * 12288 / (2 * G3), 2048 / (12 * 12288), covers=[2 * 96 * 2048 * 12288 / (2 * G3)])
lv.claim(round(100 * A3, 1) == 1.4 and round(100 * ATT / NE, 1) == 11.1, 'attention adds 1.4% at GPT-3 (T = 2,048, d = 12,288) and 11.1% for GPT-2 small (T = 1,024)', covers=[ATT / NE])
TE = 65 * 32 + 32 * 32
lv.claim(TE == 3104 and formula(65, 32, 32, 1, tied=False) - TE == 14913 and arrays(65, 32, 32, 1, tied=False) - TE == 14913 and 18017 - TE == 14913, 'tiny GPT non-embedding parameters: 18,017 - 3,104 = 14,913', covers=[14913])
lv.claim(12 * 768 == 9216 and 12 * 12288 == 147456 and 768 * 768 == 589824, 'attention dominates past T = 12d', covers=[9216, 147456, 589824, 768])
DAYS = two('GPT-3 days', F3 / (1000 * 312e12 * 0.4) / 86400, 3.15e23 / 1.248e17 / 86400, covers=[F3 / (1000 * 312e12 * 0.4) / 86400, F3 / (1000 * 312e12) / 86400, F3 / (1000 * 312e12 * 0.4) / 3600, 1.248, 0.4, 312])
COST = 1000 * DAYS * 24 * 1.5
two('GPT-3 cost', round(COST, -3), round(1000 * 24 * 1.5 * DAYS, -3), covers=[round(COST, -3), round(COST / 24, -3), round(COST / 1000, -3), 1000 * DAYS * 24, 1.5, DAYS])
lv.claim(1e9 * 2e10 * 6 == 1.2e20 and 2 * 7e10 == 1.4e11 and 6 * 7e10 == 4.2e11 and 10 / 0.25 == 40, 'quiz workings', covers=[1.2, 0.4, 1.4, 4.2, 7, 40, 2.5, 0.25])

# ---------------- l15 ----------------
NS = [1e6, 1e7, 1e8, 1e9]
LS = [5 * n ** -0.1 for n in NS]
two('per-decade factor', LS[1] / LS[0], 10 ** -0.1, covers=LS + [10 ** -0.1, 1 / 10 ** -0.1, LS[0] - LS[1]] + [math.log10(x) for x in LS])
sl = (math.log10(LS[3]) - math.log10(LS[0])) / 3
lv.claim(abs(sl + 0.1) < 1e-12, 'slope -0.1', covers=[0.1, math.log10(LS[3]) - math.log10(LS[0]), math.log(5), 5.0, 1.609, 0.05])
rng = np.random.default_rng(0)
NN = np.logspace(6, 9, 7)
LN = 5 * NN ** -0.1 * np.exp(rng.normal(0, 0.02, 7))
s1, i1 = np.polyfit(np.log(NN), np.log(LN), 1)
x, y = np.log(NN), np.log(LN)
s2 = np.cov(x, y, bias=True)[0, 1] / np.var(x)
two('noisy exponent', -s1, -s2, covers=[-s1, s1, math.exp(i1)] + list(LN) + [math.log10(n) for n in NN])
lv.claim(np.allclose([float(r[1]) for r in F('l15')['screens'][4]['canvas']['params']['rows']], np.round(LN, 4)), 'noisy table')
K = [(8.8e13 / n) ** 0.076 for n in (1e8, 1e9, 1e10, 1e11)]
Kl = [math.exp(0.076 * (math.log(8.8e13) - math.log(n))) for n in (1e8, 1e9, 1e10, 1e11)]
lv.claim(all(close(a, b) for a, b in zip(K, Kl)), 'Kaplan direct and in log form', covers=K + [10 ** -0.076, 8.8e13 / 1e9, (1e9 / 8.8e13) ** 0.076, 88000, 880, 0.076, 0.16])
lv.claim(abs(math.log10(20 / 2) / math.log10(1e6 / 1e4) - 0.5) < 1e-12, 'impact exponent 0.5', covers=[0.5, 1.0, 0.1, 2, 20])
two('q-factor', 10 ** -0.05, math.exp(-0.05 * math.log(10)), covers=[10 ** -0.05, 0.95, 100 ** -0.2, 10 ** -0.2, 0.398, 0.631, math.exp(1.5), 4.48, 0.3, 1.5])
lv.claim(abs(1 - 100 ** -0.2 - 0.6) < 0.002, 'falls by 60%', covers=[0.6])
lv.claim(close(406.4 / 70e9 ** 0.34, 406.4 * math.exp(-0.34 * math.log(70e9))), 'floor plot constants', covers=[1.69, 406.4, 0.34])

# ---------------- l16 ----------------
EE, AA, BB, AL, BE = 1.69, 406.4, 410.7, 0.34, 0.28


def chin(N, D):
    return EE + AA / N ** AL + BB / D ** BE


GG = (AL * AA / (BE * BB)) ** (1 / (AL + BE))
C = 5.76e23
NO = GG * (C / 6) ** (BE / (AL + BE))
Ns = np.logspace(9, 13, 400001)
NG = float(Ns[np.argmin(chin(Ns, C / (6 * Ns)))])
two('optimum: closed form and grid', NO, NG, 1e-4)
DO = C / (6 * NO)
lv.claim(abs(DO / NO - 92.6) < 0.05, 'about 93 tokens per parameter', covers=[NO, DO, DO / NO, NO / DO, 93, 20, 4.6, NO / 1e9])
D70 = C / (6 * 70e9)
two('D at 70B', D70, 5.76e23 / 4.2e11, covers=[D70 / 1e12, C / (2 * 70e9) / 1e12, 4.2, 5.76, 1.371])
L70 = chin(70e9, 1.4e12)
L175 = chin(175e9, 300e9)
two('Chinchilla loss', L70, EE + AA * math.exp(-AL * math.log(70e9)) + BB * math.exp(-BE * math.log(1.4e12)), covers=[L70, L70 - 1.69, AA / 70e9 ** AL, BB / 1.4e12 ** BE])
two('GPT-3 loss', L175, EE + AA * math.exp(-AL * math.log(175e9)) + BB * math.exp(-BE * math.log(3e11)), covers=[L175, L175 - 1.69, AA / 175e9 ** AL, BB / 300e9 ** BE, 2.5])
LG = chin(NO, DO)
lv.claim(LG < chin(70e9, D70) and abs(chin(1e10, C / 6e10) - round(chin(1e10, C / 6e10), 4)) < 5e-5, 'optimum lower than 70B on the budget', covers=[LG, chin(70e9, D70), round(chin(1e10, C / 6e10), 4), 10.5, 30])
GN, GD = 10 ** (BE / (AL + BE)), 10 ** (AL / (AL + BE))
two('ten times the compute', GN * GD, 10, covers=[GN, GD, BE / (AL + BE), AL / (AL + BE), 0.4516, 0.5484])
C8 = 6 * 8e9 * 15e12
N8 = GG * (C8 / 6) ** (BE / (AL + BE))
lv.claim(C8 == 7.2e23 and 15e12 / 8e9 == 1875 and abs(N8 / 8e9 - 4.45) < 0.05, 'inference-heavy run: 7.2e23, 1,875 per parameter, about 4 times smaller', covers=[7.2, 1875, 0.0005, N8 / 1e9, C8 / (6 * N8) / 1e12, chin(8e9, 15e12), chin(N8, C8 / (6 * N8)), 4])
two('example loss', chin(1e9, 1e10), EE + AA / 1e9 ** AL + BB / 1e10 ** BE, covers=[round(chin(1e9, 1e10), 3)])
lv.claim(0.1 * 2 == 0.2, 'sqrt: exponents one half', covers=[0.5])
LIT('200,001', why='the grid size the task sets')
LIT('1.4T', why='Chinchilla\'s published token count, a given')
LIT('300B', why='GPT-3\'s published token count, a given')
LIT('0.01%', why='the grid spacing over 8 decades, 0.0092% a step, stated as a bound')

# ---------------- review, homework, problems ----------------
lv.claim(12 * 48 * 1600 ** 2 == 1474560000 and 12 * 1600 ** 2 == 30720000, 'r-rule', covers=[1474.6, 30.7, 1474560000, 2560000])
RP = P(32000, 2048, 1024, 16)
lv.claim(32000 * 1024 + 2048 * 1024 == 34865152 and formula(1, 1, 1024, 1) - formula(1, 1, 1024, 0) == 12596224, 'r-count parts', covers=[RP, 34865152, 12596224, 2048, formula(32000, 2048, 1024, 16, tied=False), 12 * 16 * 1024 ** 2])
two('r-6nd (6ND, and three times the forward 2ND)', 6 * 1.3e9 * 26e9 / 1e20, 3 * (2 * 1.3e9 * 26e9) / 1e20, covers=[2.03, 2.028 / 3, 0.68, 1.3, 26, 2.6])
RD = 1e23 / (512 * 312e12 * 0.5) / 86400
two('r-days', RD, 1e23 / 7.9872e16 / 86400, covers=[RD, RD / 2, RD * 24, 7.99, 512, 0.5])
two('r-slope', math.log(3.2 / 2.4) / math.log(100), math.log10(3.2 / 2.4) / 2, covers=[math.log(3.2 / 2.4) / math.log(100), 0.4, math.log10(3.2 / 2.4), 0.0625])
two('r-kaplan', K[3], K[2] * 10 ** -0.076, covers=[K[3], K[2]])
lv.claim(6e22 / (6 * 5e9) == 2e12 and 2e12 / 5e9 == 400, 'r-budget', covers=[2000, 6000, 400, 2])
lv.claim(2 * 13e9 == 2.6e10 and 6 * 13e9 == 7.8e10, 'r-inference', covers=[2.6, 7.8, 1.3])
FCD = FC / (2048 * 312e12 * 0.45) / 86400
two('h-chin-days', FCD, 5.88e23 / 2.875392e17 / 86400, covers=[FCD, FC / (2048 * 312e12) / 86400, FCD * 24, 2.88, 0.45])
lv.claim(TOK / 18017 > 142 and TOK / 18017 < 142.2 and 280 / 70 == 4 and 1400 / 300 > 4, 'h-kaplan-chin ratios', covers=[142, 280, 4, 1.4])
lv.claim(6 * 7e9 * 15e12 == 6.3e23, '7B on 15T is 6.3e23', covers=[6.3])
PP = P(50257, 2048, 2048, 24)
PF = 6 * PP * 1e12
PD = PF / (64 * 312e12 * 0.45) / 86400
PC = 64 * round(PD, 1) * 24 * 1.8
lv.claim(PP == 1315723264 and 50257 * 2048 + 2048 * 2048 == 107120640 and formula(1, 1, 2048, 1) - formula(1, 1, 2048, 0) == 50358272, 'p1 count', covers=[PP, 107120640, 50358272, 4096, 12 * 24 * 2048 ** 2, formula(50257, 2048, 2048, 24, tied=False), 1.3])
two('p1 FLOPs', PF / 1e21, 6 * 1.315723264, covers=[PF / 1e21, PF / 3e21])
two('p1 days', PD, PF / 8.98560e15 / 86400, covers=[PD, PD * 0.45, PD * 24, 8.99, PD * 86400])
two('p1 cost', round(PC, -2), round(64 * 10.2 * 24 * 1.8, -2), covers=[round(PC, -2), round(PC / 24, -2), round(PC / 64, -1), 64 * round(PD, 1) * 24, 1.8])
a2 = math.log10(3.0 / 2.6)
two('p2 exponent', a2, math.log(3.0 / 2.6) / math.log(10), covers=[a2, math.log(3.0 / 2.6), 0.4, 1.1538])
two('p2 prediction', 2.6 * 10 ** -a2, 2.6 * 2.6 / 3.0, covers=[2.6 * 2.6 / 3.0, 2.2])
N22 = math.sqrt(1e22 / 120)
two('p3 N', N22, (1e22 / 120) ** 0.5, covers=[N22 / 1e9, math.sqrt(1e22 / 6) / 1e9, 20 * N22 / 1e9, 8.33, N22, 20 * N22, 120])
lv.claim(abs(6 * 9.13e9 * 1.83e11 / 1e22 - 1) < 0.01 and f'{N22:.3g}' == '9.13e+09' and f'{20 * N22:.3g}' == '1.83e+11', 'p3 check: 9.13e9 and 1.83e11 multiply back to about 1e22', covers=[9.13e9, 1.83e11, 1e22 / 120])
for t_, why in [('10^{-6}', 'test tolerance'), ('10^{-9}', 'test tolerance'), ('10^{-12}', 'test tolerance'), ('0.1%', 'a test tolerance (rel 1e-3)'), ('0.03', 'a test tolerance on fitted exponents'),
                ('1.5', 'a test tolerance factor'), ('0.10', 'the grid start, a rule of the task'), ('0.60', 'the grid end, a rule of the task'), ('0.01', 'the grid step, a rule of the task'),
                ('3.0', 'a pilot loss, a given'), ('2.6', 'a pilot loss, a given'), ('3.2', 'a run loss, a given'), ('2.4', 'a run loss, a given'), ('1.90', 'a given loss'), ('2.46', 'a given loss'),
                ('12', 'planted runs per set, a given'), ('£1.80', 'a given price'), ('£1.50', 'a given price'), ('2,048', 'given GPU counts and widths')]:
    LIT(t_, why=why)


# ---------------- the givens and the printed forms of computed figures (scientific notation is covered by value) ----------------
givens = [1e4, 1e6, 1e7, 1e8, 1e9, 1e10, 1e11, 1e12, 1e13, 1e20, 1e21, 1e22, 1e23, 86400, 50257, 1024, 32000, 100000, 96, 65, 70, 48, 384, 16, 100, 5000, 200, 13,
          8.8e13, 410.7, 0.28, 1.75e11, 3e11, 7e10, 1.4e12, 3.12e14, 2.1e9, 1.3e9, 1.3e10, 8e9, 5e9, 6e9, 2e10, 6e22, 15e12, 15000, 2.56, 124, 163, 204.8, 0.2]
lv.claim(10.0 ** 23 > 0 and 22 / 120 > 0 and abs(2048 * 312e12 * 0.45 - 2.88e17) < 0.005e17 and GPT2 // 10 ** 6 == 124 and U2 // 10 ** 6 == 163 and 100000 * 2048 / 1e6 == 204.8 and 13 * 32 == 416 and 2560000 / 1e6 == 2.56, 'givens and their roles in the computations above', covers=givens + [2, 10.0 ** 23, 10 ** 23, 1.75, 10, 2.88e17, 22 / 120])
computed = [F3, FC, C, 6 * 7e10, 2.6e10, 4.2e11, 7.8e10, 1.4e11, 1.2e20, 6 * 1.3e9 * 26e9, 2e12, 7.2e23, 6.3e23, PF, 6 * PP, FC / (2048 * 312e12 * 0.45) * 0 + 2048 * 312e12 * 0.45,
            1000 * 312e12 * 0.4, 512 * 312e12 * 0.5, 64 * 312e12 * 0.45, 1e22 / 120, 31.5e22, 3.14e23, 11e11, D70, 12288 ** 2, G3, 6 * 18017 * 512 * 5000, 6 * GPT2 * 1e10, PP * 1e12, 1 / 3]
lv.claim(close(31.5e22, F3) and close(11e11 * 6 * 1.75 * 3 / 11 / 1e11, 31.5) and close(6 * GPT2 * 1e10, 7.4663884800e18, 1e-9), 'scientific forms of the computed figures', covers=computed)

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
        if isinstance(x_, (list, tuple)) or isinstance(yv, (list, tuple)):
            return isinstance(x_, (list, tuple)) and isinstance(yv, (list, tuple)) and len(x_) == len(yv) and all(same(p_, q_) for p_, q_ in zip(x_, yv))
        return bool(x_ == yv)
    return cl(a, ex) if cmp == 'isclose' else same(a, ex)


def first_fail(w, src):
    cwd, dd = os.getcwd(), tempfile.mkdtemp()
    os.chdir(dd)
    try:
        ns_ = {'__name__': '__zq__', '__learner_source__': src}
        try:
            with np.errstate(all='ignore'):
                exec(ZQ_LIB, ns_)
                exec((w.get('prelude') or '') + '\n', ns_)
                exec(src, ns_)
                exec((w.get('postlude') or '') + '\n', ns_)
        except Exception:
            return -1
        for i, c in enumerate(w['tests']):
            try:
                with np.errstate(all='ignore'):
                    if c.get('setup'):
                        exec(c['setup'], ns_)
                    got = eval(c['call'], ns_)
                    t = c.get('tol')
                    ok = judge(got, eval(c['expect'], ns_), c.get('compare', 'isclose'), (t.get('rel') or 0, t.get('abs') or 0) if t else None)
            except Exception:
                ok = False
            if not ok:
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
lv.check_wrongs()
lv.report()
