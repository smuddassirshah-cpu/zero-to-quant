"""Numbers stated in the 2.7 briefs, each computed two ways."""
import math
import numpy as np
from fractions import Fraction

out = []
def chk(label, a, b, tol=1e-9):
    ok = abs(a - b) <= tol * max(1, abs(a))
    out.append((label, a, b, ok))

# --- nn-train L1
chk("momentum 1/(1-0.9)", 1 / (1 - 0.9), sum(0.9 ** k for k in range(2000)))
chk("momentum 1/(1-0.99)", 1 / (1 - 0.99), sum(0.99 ** k for k in range(20000)))
kappa = 10.0
r_gd = (kappa - 1) / (kappa + 1)
# best fixed GD step on diag(1,10): s = 2/(1+10); factors |1-s| and |1-10s|
s = 2 / 11
chk("GD best rate 9/11", r_gd, max(abs(1 - s), abs(1 - 10 * s)))
sq = math.sqrt(kappa)
beta_hb = ((sq - 1) / (sq + 1)) ** 2
alpha_hb = 4 / (1 + sq) ** 2
chk("heavy-ball beta", beta_hb, 0.26987, 1e-4)
chk("heavy-ball step", alpha_hb, 0.23094, 1e-4)
# rate of heavy ball = sqrt(beta); check via spectral radius of iteration matrix on lambda=1 and 10
def hb_rate(lam):
    M = np.array([[1 + beta_hb - alpha_hb * lam, -beta_hb], [1, 0]])
    return max(abs(np.linalg.eigvals(M)))
chk("heavy-ball rate sqrt(beta)", math.sqrt(beta_hb), max(hb_rate(1), hb_rate(10)), 1e-6)
# Adam bias correction at t=1 and t=10
chk("1-0.999^10", 1 - 0.999 ** 10, sum(math.comb(10, k) * (-0.001) ** k * -1 for k in range(1, 11)) * -1 * -1 if False else 1 - math.exp(10 * math.log(0.999)))
chk("1-0.9^10", 1 - 0.9 ** 10, 0.6513215599)
# minibatch sd ratio B=32 vs 128
chk("sd ratio 32 vs 128", math.sqrt(128 / 32), 2.0)
# cosine schedule halfway
chk("cosine half", 0.5 * (1 + math.cos(math.pi * 0.5)), 0.5)

# --- nn-train L2
chk("tanh'(3)", 1 - math.tanh(3) ** 2, 1 / math.cosh(3) ** 2)
chk("0.25^10", 0.25 ** 10, 2 ** -20)
chk("He sd n=100", math.sqrt(2 / 100), 0.1414213562)
# variance after one layer n=100, w sd 1, x var 1 -> 100 ; simulate
rng = np.random.default_rng(0)
z = (rng.standard_normal((20000, 100)) * rng.standard_normal((20000, 100))).sum(1)
chk("var z ~ 100 (sim, loose)", 100.0, float(np.var(z)), 0.15)

# --- nn-train L3
chk("decay factor 1-0.1*0.01", 1 - 0.1 * 0.01, 0.999)
chk("inverted dropout keep 0.8", 1 / 0.8, 1.25)
chk("1-0.95^20", 1 - 0.95 ** 20, 0.6415140775)

# --- cnn
def out_size(n, k, p, s):
    return (n + 2 * p - k) // s + 1
chk("out 8 k3 p0 s1", out_size(8, 3, 0, 1), len(range(0, 8 - 3 + 1)))
chk("out 8 k3 p1 s1", out_size(8, 3, 1, 1), 8)
chk("out 8 k3 p1 s2", out_size(8, 3, 1, 2), len(range(0, 10 - 3 + 1, 2)))
chk("rolling 12 k3 valid", 12 - 3 + 1, len(np.convolve(np.ones(12), np.ones(3) / 3, mode="valid")))
x = np.arange(1.0, 13.0)

chk("conv == rolling mean", float(np.convolve(x, np.ones(3) / 3, "valid")[-1]), float(x[-3:].mean()))
conv_params = 16 * (1 * 9) + 16
dense = (4 * 4 * 16) * 10 + 10
chk("CNN params 2730", conv_params + dense, 2730)
chk("MLP 64-40-10 params 3010", 64 * 40 + 40 + 40 * 10 + 10, 75 * 40 + 10)
chk("conv 8->16 3x3 params", 16 * 8 * 9 + 16, 1168)
res_params = 2 * (16 * 16 * 9 + 16)
chk("residual block two 16->16 convs", res_params, 4640)
chk("im2col rows 8x8 pad1", out_size(8, 3, 1, 1) ** 2, 64)
chk("conv MACs 64*9*16", 64 * 9 * 16, 9216)
# receptive field of two 3x3 layers stride 1
chk("receptive field 2 layers", 1 + 2 * (3 - 1), 5)
chk("receptive field 3 layers", 1 + 3 * (3 - 1), 7)
# one-pixel shift: a 2x2 maxpool is invariant only for some shifts (no number)

# --- sequence
chk("0.9^50", 0.9 ** 50, math.exp(50 * math.log(0.9)))
chk("1.1^50", 1.1 ** 50, math.exp(50 * math.log(1.1)))
chk("clip 5 to 1 scale", 1 / 5, 0.2)
rng = np.random.default_rng(1)
q = rng.standard_normal((20000, 64)); k = rng.standard_normal((20000, 64))
dots = (q * k).sum(1)
chk("var q.k d=64 (sim, loose)", 64.0, float(dots.var()), 0.05)
chk("causal pairs T=4", 4 * 5 / 2, int(np.tril(np.ones((4, 4))).sum()))
chk("causal pairs T=32", 32 * 33 / 2, int(np.tril(np.ones((32, 32))).sum()))
d, m = 64, 256
attn = 4 * (d * d + d)
mlp = d * m + m + m * d + d
ln = 2 * 2 * d
block = attn + mlp + ln
chk("block params", block, 49984)
whole = block + 65 * d + 32 * d + 2 * d + d * 65 + 65
chk("one-block GPT params", whole, 60545)
# softmax of scores (2, 1, 0)
sc = np.array([2.0, 1.0, 0.0]); w = np.exp(sc) / np.exp(sc).sum()
chk("softmax(2,1,0)[0]", float(w[0]), math.e ** 2 / (math.e ** 2 + math.e + 1))
# scaled by sqrt(4): scores (2,1,0)/2
w2 = np.exp(sc / 2) / np.exp(sc / 2).sum()
chk("softmax((2,1,0)/2)[0]", float(w2[0]), math.e / (math.e + math.e ** 0.5 + 1))

# --- representations
u = np.array([1.0, 2.0]); v = np.array([2.0, 1.0])
chk("cos (1,2),(2,1)", float(u @ v / np.linalg.norm(u) / np.linalg.norm(v)), float(Fraction(4, 5)))
def kl_gauss(mu, s):
    return 0.5 * (mu ** 2 + s ** 2 - 1 - math.log(s ** 2))
# numeric KL by integration
from scipy import integrate, stats
def kl_num(mu, s):
    f = lambda t: stats.norm.pdf(t, mu, s) * (stats.norm.logpdf(t, mu, s) - stats.norm.logpdf(t))
    return integrate.quad(f, -30, 30)[0]
chk("KL N(1,0.5^2)||N(0,1)", kl_gauss(1, 0.5), kl_num(1, 0.5), 1e-7)
chk("KL N(0,1)||N(0,1)", kl_gauss(0, 1), kl_num(0, 1), 1e-7)
chk("KL N(2,1)||N(0,1)", kl_gauss(2, 1), kl_num(2, 1), 1e-7)
# diffusion linear schedule
betas = np.linspace(1e-4, 0.02, 1000)
abar = np.cumprod(1 - betas)
chk("abar_1000", float(abar[-1]), math.exp(np.log(1 - betas).sum()))
chk("abar_500", float(abar[499]), math.exp(np.log(1 - betas[:500]).sum()))
# small schedule for 2D toy: T=50, betas linspace(1e-4, 0.2)? use cosine-free linear 1e-3..0.2
b50 = np.linspace(1e-3, 0.2, 50); a50 = np.cumprod(1 - b50)
chk("abar_50 toy", float(a50[-1]), math.exp(np.log(1 - b50).sum()))
# GCN normalised adjacency path 1-2-3
A = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], float) + np.eye(3)
Dm = np.diag(1 / np.sqrt(A.sum(1)))
Ah = Dm @ A @ Dm
chk("Ahat[0,0]", float(Ah[0, 0]), 0.5)
chk("Ahat[0,1]", float(Ah[0, 1]), 1 / math.sqrt(6))
chk("Ahat[1,1]", float(Ah[1, 1]), 1 / 3)
chk("Ahat top eigenvalue 1", float(max(np.linalg.eigvalsh(Ah))), 1.0)
# linear AE error = dropped eigenvalue, on a 2x2 covariance
S = np.array([[4.0, 1.5], [1.5, 3.0]])
lam = np.linalg.eigvalsh(S)
X = np.random.default_rng(3).multivariate_normal([0, 0], S, 200000)
Xc = X - X.mean(0)
U, sv, Vt = np.linalg.svd(Xc, full_matrices=False)
rec = Xc @ Vt[:1].T @ Vt[:1]
chk("AE error = smallest eigenvalue (sim, loose)", float(lam[0]), float(((Xc - rec) ** 2).sum(1).mean()), 0.02)

# --- additions
chk("GD 20 steps (9/11)^20", (9 / 11) ** 20, math.exp(20 * math.log(9 / 11)))
chk("HB 20 steps sqrt(beta)^20", math.sqrt(beta_hb) ** 20, beta_hb ** 10)
chk("dense 8x8x1 -> 8x8x16", 64 * 1024 + 1024, 64 * (64 * 16) + 64 * 16)
S2 = np.array([[5.0, 2.0], [2.0, 2.0]])
l2 = np.linalg.eigvalsh(S2)
chk("eigen l11 small eigenvalue", float(l2[0]), (7 - math.sqrt(49 - 24)) / 2)
chk("eigen l11 large eigenvalue", float(l2[1]), (7 + math.sqrt(49 - 24)) / 2)
chk("share PC1 6/7", 6 / 7, float(l2[1] / l2.sum()))
rng = np.random.default_rng(5)
Z = rng.multivariate_normal([0, 0], S2, 50000); Z -= Z.mean(0)
Sh = Z.T @ Z / (len(Z) - 1)
w = np.array([[0.3], [0.1]]); v = np.array([[0.2, 0.4]])
for _ in range(3000):
    R = Z @ w @ v - Z
    gv = 2 * (Z @ w).T @ R / len(Z); gw = 2 * Z.T @ (R @ v.T) / len(Z)
    v -= 0.02 * gv; w -= 0.02 * gw
err = float(((Z @ w @ v - Z) ** 2).sum(1).mean()) * len(Z) / (len(Z) - 1)
chk("trained linear AE error = smallest eigenvalue of sample cov (GD)", float(np.linalg.eigvalsh(Sh)[0]), err, 1e-3)
for t, val in ((1, 3.16228), (10, 6.52788), (100, 3.24080), (1000, 1.25758)):
    chk(f"uncorrected Adam ratio t={t}", (1 - 0.9 ** t) / math.sqrt(1 - 0.999 ** t),
        -math.expm1(t * math.log(0.9)) / math.sqrt(-math.expm1(t * math.log(0.999))))
    chk(f"uncorrected Adam ratio t={t} stated", (1 - 0.9 ** t) / math.sqrt(1 - 0.999 ** t), val, 1e-5)
chk("DDPM sigma check: 1/sqrt(alpha) for beta=0.02", 1 / math.sqrt(0.98), 1.0101525445522108)

for label, a, b, ok in out:
    print(("OK " if ok else "BAD"), label, a, b)
print("all ok" if all(o[3] for o in out) else "SOME BAD")
