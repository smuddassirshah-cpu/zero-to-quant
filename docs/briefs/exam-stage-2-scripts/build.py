"""Build app/content/exams/stage-2.json, the Stage 2 exit test (topics 2.1 to 2.6), and its data files.

Route A for every key: the closed forms and reference implementations below. check_numbers.py recomputes each value
by a second route and asserts it at its path in the written file. Run: python3 docs/briefs/exam-stage-2-scripts/build.py
Data files are written to app/content/data/stage-2/ from fixed seeds; every expected value is computed from the file
as pandas reads it back, so rounding in the CSV is part of the key.
"""
import io
import json
import math
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..', '..')
OUT = os.path.join(ROOT, 'app', 'content', 'exams', 'stage-2.json')
DATA = os.path.join(ROOT, 'app', 'content', 'data', 'stage-2')
os.makedirs(DATA, exist_ok=True)


def r(x, n=6):
    return round(float(x), n)


def Phi(z):
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def phi(z):
    return math.exp(-z * z / 2) / math.sqrt(2 * math.pi)


def bs_call(S, K, r_, s, T):
    d1 = (math.log(S / K) + (r_ + s * s / 2) * T) / (s * math.sqrt(T))
    return S * Phi(d1) - K * math.exp(-r_ * T) * Phi(d1 - s * math.sqrt(T))


def fb(correct, generic, by_key=None):
    d = {"correct": correct, "generic": generic}
    if by_key:
        d["byKey"] = by_key
    return d


def num(answer, tol, wrong=(), unit=None, placeholder="a number", accept=None):
    w = {"kind": "numeric", "answer": answer, "tol": {"abs": tol}, "placeholder": placeholder}
    if unit:
        w["unit"] = unit
    if accept:
        w["accept"] = accept
    if wrong:
        w["wrong"] = [{"id": i, "value": v, "tol": {"abs": t}} for i, v, t in wrong]
    return w


def choice(options, kind="choice"):
    return {"kind": kind, "layout": "stack", "shuffle": True, "options": options}


def opt(id, text, why=None, correct=False):
    o = {"id": id, "text": text}
    if correct:
        o["correct"] = True
    if why:
        o["why"] = why
    return o


def item(id, d, skills, tags, pace, title, prose, question, widget, feedback, explain):
    it = {"id": id, "difficulty": d, "skills": skills, "tags": tags, "pace": pace, "title": title}
    if prose:
        it["prose"] = prose
    it.update({"question": question, "widget": widget, "feedback": feedback, "explain": {"text": explain}})
    return it


def parts(id, d, skills, tags, pace, title, prose, ps, explain, question=None):
    it = {"id": id, "difficulty": d, "skills": skills, "tags": tags, "pace": pace, "title": title, "prose": prose}
    if question:
        it["question"] = question
    it["parts"] = [dict(([("prose", pp[3])] if len(pp) > 3 else []) + [("question", pp[0]), ("widget", pp[1]), ("feedback", pp[2])]) for pp in ps]
    it["explain"] = {"text": explain}
    return it


def code_fb(correct, by_key):
    by_key = dict(by_key)
    by_key.setdefault("error", "Your code stopped with an error. Read the first line of the message under the editor.")
    return fb(correct, "Some tests failed. Open the first one that failed below the editor.", by_key)


def T(call, expect, cmp="isclose", setup=None, tol=None):
    t = {}
    if setup:
        t["setup"] = setup
    t.update({"call": call, "expect": expect, "compare": cmp})
    if tol:
        t["tol"] = tol
    return t


def ex(t):
    """A visible example copied from a hidden test, with the test's compare and tolerance (a float needs its isclose)."""
    e = {}
    if t.get("setup"):
        e["setup"] = t["setup"]
    e.update({"call": t["call"], "expect": t["expect"]})
    if t.get("compare") == "isclose" and t.get("tol"):
        e["compare"], e["tol"] = "isclose", t["tol"]
    return e


def rep(x):
    if isinstance(x, (list, tuple, np.ndarray)):
        return repr([float('%.12g' % v) for v in x])
    return repr(float('%.12g' % x))


def run_solution(src, call, setup=None):
    """Evaluate a test call against a reference solution, in DATA (so data files open by bare name)."""
    here = os.getcwd()
    os.chdir(DATA)
    try:
        ns = {}
        exec(src, ns)
        if setup:
            exec(setup, ns)
        return eval(call, ns)
    finally:
        os.chdir(here)


A, B, C, D = [], [], [], []

# ======================================================================== data files (fixed seeds)
rng = np.random.default_rng(20261106)

# factor-days.csv: four features on different scales, one drifting, and a next-day return
nF = 360
dates = pd.bdate_range('2024-01-02', periods=nF).strftime('%Y-%m-%d')
z = rng.standard_normal((nF, 4))
tt = np.arange(nF)
f1 = z[:, 0]
f2 = 50 + 12 * z[:, 1]
f3 = 0.01 * z[:, 2]
f4 = 5 * z[:, 3] + 0.04 * tt
yF = 0.002 * f1 - 0.0001 * (f2 - 50) + 0.12 * f3 + 0.0004 * (f4 - 0.04 * tt) + 0.01 * rng.standard_normal(nF)
fd = pd.DataFrame({'date': dates, 'f1': np.round(f1, 4), 'f2': np.round(f2, 2), 'f3': np.round(f3, 6),
                   'f4': np.round(f4, 3), 'y': np.round(yF, 6)})
fd.to_csv(os.path.join(DATA, 'factor-days.csv'), index=False)

# pair-closes.csv: a cointegrated with b; c an unrelated random walk
nP = 500
lb = math.log(40) + np.cumsum(0.012 * rng.standard_normal(nP))
sp = np.zeros(nP)
for k in range(1, nP):
    sp[k] = 0.9 * sp[k - 1] + 0.008 * rng.standard_normal()
la = 0.35 + 1.25 * lb + sp
lc = math.log(60) + np.cumsum(0.015 * rng.standard_normal(nP))
pdates = pd.bdate_range('2023-06-01', periods=nP).strftime('%Y-%m-%d')
pc = pd.DataFrame({'date': pdates, 'a': np.round(np.exp(la), 2), 'b': np.round(np.exp(lb), 2), 'c': np.round(np.exp(lc), 2)})
pc.to_csv(os.path.join(DATA, 'pair-closes.csv'), index=False)

# fill-buckets, jump-days and chains were the data of the topic 2.6 items, which left the gating papers.
# They are still drawn, so that signal-panel.csv below keeps its seed stream, but they are not written.
# fill-buckets: fills out of orders placed, by day and size bucket, against spread and queue
nL = 120
spread = np.round(rng.uniform(0.5, 6.0, nL), 2)
queue = np.round(rng.uniform(0, 20, nL), 1)
orders = rng.integers(20, 81, nL)
pL = 1 / (1 + np.exp(-(1.5 - 0.45 * spread - 0.06 * queue)))
fills = rng.binomial(orders, pL)

# jump-days: price jumps per session against the VIX close, with session hours as exposure
nJ = 240
vix = np.zeros(nJ)
vix[0] = 18
for k in range(1, nJ):
    vix[k] = 18 + 0.85 * (vix[k - 1] - 18) + 2.2 * rng.standard_normal()
vix = np.round(np.clip(vix, 10.5, 45), 2)
hours = np.where(rng.uniform(size=nJ) < 0.04, 3.5, 6.5)
jumps = rng.poisson(hours * np.exp(-2.3 + 0.07 * vix))

# chains: four AR(1) chains of 400 draws, the fourth sitting a little higher
nC = 400
ch = np.zeros((4, nC))
for j in range(4):
    x = 0.0
    for k in range(nC):
        x = 0.6 * x + 0.8 * rng.standard_normal()
        ch[j, k] = x
ch[3] += 0.4

# signal-panel.csv: 20 weekly dates, 30 tickers, a persistent signal and the next week's return
nD, nT = 20, 30
sig = np.zeros((nD, nT))
sig[0] = rng.standard_normal(nT)
for k in range(1, nD):
    sig[k] = 0.6 * sig[k - 1] + 0.8 * rng.standard_normal(nT)
fwd = 0.003 * sig + 0.025 * rng.standard_normal((nD, nT))
wdates = pd.date_range('2025-03-07', periods=nD, freq='7D').strftime('%Y-%m-%d')
rows = [(wdates[k], f'T{j + 1:02d}', round(sig[k, j], 5), round(fwd[k, j], 7)) for k in range(nD) for j in range(nT)]
panel = pd.DataFrame(rows, columns=['date', 'ticker', 'signal', 'fwd_ret'])
assert all(g['signal'].nunique() == nT and g['fwd_ret'].nunique() == nT for _, g in panel.groupby('date')), 'ties in the panel'
panel.to_csv(os.path.join(DATA, 'signal-panel.csv'), index=False)

DATA_REL = 'content/data/stage-2/'

# ======================================================================== Paper A: machine learning and validation
# A1 shrinking a mean toward zero (bias against variance)
mu1, sd1, n1 = 0.0004, 0.02, 250
v1 = sd1 ** 2 / n1
c1 = mu1 ** 2 / (mu1 ** 2 + v1)
A.append(item("a-shrink-mean", 4, ["sl-tradeoff"], ["shrink-estimate"], 240, "Shrinking a mean return",
    "We estimate a share's mean daily return $\\mu$ by $c\\bar X$, a shrunk sample mean of $n = 250$ days. "
    "Take $\\mu = 0.0004$ and a daily standard deviation $\\sigma = 0.02$.",
    "Which shrink factor $c$ minimises $E[(c\\bar X - \\mu)^2]$? Give 4 decimal places.",
    num(r(c1), 0.0005, [("ratio", r(mu1 ** 2 / v1), 0.0005), ("flipped", r(1 - c1), 0.0005)]),
    fb("A little bias buys a large cut in variance.", "Write the error as squared bias plus variance, then set its derivative in $c$ to zero.",
       {"ratio": "You divided $\\mu^2$ by the variance alone. The denominator is $\\mu^2 + \\sigma^2/n$.",
        "flipped": "You gave $1 - c$, the share removed. The question asks for the factor kept."}),
    "The error is $(c - 1)^2\\mu^2 + c^2\\sigma^2/n$, squared bias plus variance. "
    "Its minimum is at $c = \\mu^2/(\\mu^2 + \\sigma^2/n) = 1.6 \\times 10^{-7}/(1.76 \\times 10^{-6})$. "
    f"That is $1/11 \\approx {c1:.4f}$, so the sample mean is mostly noise."))

# A2 a cost threshold for a classifier
c2 = 40 / 160
A.append(item("a-review-threshold", 2, ["sl-classify"], ["cost-threshold"], 90, "When to review a fill",
    "A classifier gives the probability $p$ that a trade was a bad fill. Reviewing a trade costs £40 and catches a bad fill. "
    "An unreviewed bad fill costs £160.",
    "Above which $p$ should a trade be reviewed?",
    num(c2, 0.0005, [("sum-denominator", 40 / 200, 0.0005), ("inverted", 1 - c2, 0.0005), ("half", 0.5, 0.0005)]),
    fb("Review when the expected loss passes the review cost.", "Compare the expected loss of not reviewing, $160p$, with the fixed £40.",
       {"sum-denominator": "You divided by $40 + 160$. The review cost is paid whatever the outcome, so compare $160p$ with 40.",
        "inverted": "You flipped the rule. A review pays when $p$ is high, not low.",
        "half": "You used the default 0.5. Unequal costs move the threshold."}),
    f"Not reviewing costs $160p$ on average; reviewing costs £40. So review when $160p > 40$, that is $p > {c2}$."))

# A3 a purged walk-forward fold
k3, first3, blk3, h3 = 3, 600, 120, 10
start3 = first3 + (k3 - 1) * blk3 + 1          # rows numbered from 1
train3 = start3 - 1 - h3
A.append(item("a-purged-fold", 3, ["vl-time"], ["purged-fold"], 150, "Rows left after a purge",
    "A daily study has rows 1 to 1,500. Each row's label is the return over the next 10 rows. "
    "Walk-forward test blocks hold 120 rows, the first being rows 601 to 720. "
    "Each block trains on all earlier rows, less any row whose label reaches into the block.",
    "How many training rows does the third test block use?",
    num(train3, 0, [("no-purge", start3 - 1, 0), ("second-block", train3 - blk3, 0), ("rolling", 600 - h3, 0)]),
    fb("The purge removes the ten rows whose labels overlap the block.", "Find the block's first row, then drop every earlier row whose label reaches it.",
       {"no-purge": f"You kept all {start3 - 1} earlier rows. The last 10 have labels that use test-block returns.",
        "second-block": "You worked on the second block. The third starts 120 rows later.",
        "rolling": "You used a fixed window of 600 rows. Each block here trains on every earlier row."}),
    f"The third block is rows {start3} to {start3 + blk3 - 1}. A row $t$ has a label using rows up to $t + 10$, so rows from {start3 - h3} on overlap it. "
    f"That leaves rows 1 to {train3}: {train3} training rows."))

# A4 which steps leak (multi, three keys)
A.append(item("a-leak-steps", 3, ["vl-leakage"], ["leak-steps"], 150, "Steps that leak",
    "A study predicts next-day returns from 120 features over 2015 to 2024, with walk-forward test blocks.",
    "Which steps let a row use information from after its own date? Select all that apply.",
    choice([opt("a", "Scaling each feature by its average and spread over all ten years at once.", correct=True),
            opt("b", "Filling a missing close with the next trading day's close.", correct=True),
            opt("c", "Keeping the 20 features best correlated with the target over the whole sample.", correct=True),
            opt("d", "Lagging every feature by one day before joining it to the target.",
                "You flagged the lag. Lagging is the cure: each feature is then known before its target."),
            opt("e", "Fitting the scaler on each training span and applying it to the next block.",
                "You flagged per-block scaling. That is the honest way; it uses no later rows."),
            opt("f", "Dropping training rows whose label window overlaps the test block.",
                "You flagged the purge. It removes leakage; it does not add any.")], kind="multi"),
    fb("Three steps use rows from after the training span.", "For each step, ask whether a row's value uses anything dated after it."),
    "The full-sample scaler and the full-sample feature choice both read test-block values. "
    "A backward fill copies tomorrow's close into today. Lagging, per-block scaling and the purge all remove leaks."))

# A5 learning curves that meet high
A.append(item("a-curves-meet", 3, ["sl-tradeoff", "vl-overfit"], ["learning-curve"], 150, "Two curves that meet too high",
    "As we add training years, a model's training error rises to 1.02 and its validation error falls to 1.05. "
    "The noise floor, the error of a perfect model, is 0.80.",
    "What does this say, and what should we try?",
    choice([opt("a", "High bias: the curves meet far above the floor, so add features, not data.", correct=True),
            opt("b", "High variance: the small gap means we should collect more years of data.",
                "You read the small gap as variance. A small gap at a high error is bias; more data will not lower it."),
            opt("c", "Overfitting: the training error rose, so add a stronger penalty to the fit.",
                "You took the rising training error as overfitting. A stronger penalty adds bias, which is already the problem."),
            opt("d", "Leakage: validation error this close to training error means the folds overlap.",
                "You took closeness as leakage. Leakage shows as validation error far below live error, not as high curves.")]),
    fb("Both errors are high and close together.", "Compare the gap between the curves with their distance from the floor."),
    "Training and validation error have met at about 1.05, far above 0.80. That is bias: the model cannot fit the signal. "
    "More data narrows a gap, and there is no gap left to narrow."))

# A6 the best regression-tree split, scored by absolute error about each side's median
y6 = np.array([-14, -9, -2, 5, 7, 18], float)
sae = lambda v: float(np.abs(v - np.median(v)).sum()) if len(v) else 0.0
sse = lambda v: float(((v - v.mean()) ** 2).sum()) if len(v) else 0.0
P6 = sae(y6)
red6 = {k: P6 - sae(y6[:k]) - sae(y6[k:]) for k in range(1, 6)}
k6 = max(red6, key=red6.get)
sq6 = sse(y6) - min(sse(y6[:k]) + sse(y6[k:]) for k in range(1, 6))
A.append(item("a-tree-split", 4, ["en-trees"], ["split-gain"], 240, "One split of a regression tree",
    "Six weeks, sorted by a momentum score, have next-week returns of $-14, -9, -2, 5, 7, 18$ basis points. "
    "A regression tree tries each split between neighbours. "
    "It scores a split by the drop in the sum of absolute errors about each side's median.",
    "What is the largest drop any one split achieves?",
    num(r(red6[k6], 4), 0.005, [("squared", r(sq6, 4), 0.005), ("parent", r(P6, 4), 0.005), ("biggest-gap", r(red6[5], 4), 0.005)]),
    fb(f"The split after the third week wins, with a drop of {red6[k6]:.0f}.", "Find the parent's absolute error about its median, then try all five splits.",
       {"squared": "You scored by squared error. This tree scores by absolute error about the median.",
        "parent": "You gave the parent's absolute error. Subtract the two children's errors from it.",
        "biggest-gap": "You split at the widest gap, between 7 and 18. Score every split; the widest gap is not the best."}),
    f"The parent's median is 1.5 and its absolute error {P6:.0f}. Splitting after $-2$ leaves 12 and 13 about the medians $-9$ and 7. "
    f"The drop is {red6[k6]:.0f}, the best of the five."))

# A7 distinct blocks in a block bootstrap
n7 = 25
d7 = n7 * (1 - (1 - 1 / n7) ** n7)
A.append(item("a-block-bootstrap", 2, ["en-bagging"], ["bootstrap-distinct"], 90, "Distinct blocks in a resample",
    "A bagged model resamples 25 monthly blocks with replacement, 25 draws for each tree.",
    "How many distinct blocks does a tree see, on average? Give 2 decimal places.",
    num(r(d7, 4), 0.005, [("limit", r(n7 * (1 - math.exp(-1)), 4), 0.005), ("out-of-bag", r(n7 - d7, 4), 0.005)]),
    fb("Each block is missed with probability $(1 - 1/25)^{25}$.", "Find the chance one block is never drawn, then count the blocks that are.",
       {"limit": "You used the limit $1 - e^{-1}$. With 25 blocks use $(24/25)^{25}$ exactly.",
        "out-of-bag": "You counted the blocks a tree never sees. The question asks for those it does see."}),
    f"A block is missed with probability $0.96^{{25}} \\approx {(1 - 1 / n7) ** n7:.4f}$. "
    f"So a tree sees $25(1 - {(1 - 1 / n7) ** n7:.4f}) \\approx {d7:.2f}$ distinct blocks."))

# A8 one boosting step on log-loss
F0 = math.log(13 / 7)
p0 = 13 / 20
g8 = (4 * (1 - p0) - 1 * p0) / (5 * p0 * (1 - p0))
F8 = F0 + 0.1 * g8
p8 = 1 / (1 + math.exp(-F8))
A.append(item("a-boost-leaf", 4, ["en-boosting"], ["boost-newton-leaf"], 240, "One tree of a boosted classifier",
    "A boosted classifier for up days starts from the log-odds of the base rate: 13 up days in 20. "
    "One leaf of the first tree holds 4 up days and 1 down day. "
    "Its value is $\\sum(y - p)/\\sum p(1 - p)$ over the leaf, with learning rate 0.1.",
    "What probability of an up day does the model now give that leaf? Give 4 decimal places.",
    num(r(p8), 0.0005, [("no-shrink", r(1 / (1 + math.exp(-(F0 + g8)))), 0.0005),
                         ("mean-residual", r(1 / (1 + math.exp(-(F0 + 0.1 * (4 * (1 - p0) - p0) / 5)))), 0.0005),
                         ("base-rate", p0, 0.0005)]),
    fb("The leaf moves the log-odds a tenth of its Newton step.", "Find the start $p = 0.65$, the leaf value, then add a tenth of it to the log-odds.",
       {"no-shrink": "You added the whole leaf value. The learning rate scales it by 0.1.",
        "mean-residual": "You averaged the residuals. The Newton leaf divides by $\\sum p(1 - p)$, not by the count.",
        "base-rate": "You gave the starting probability. The first tree moves it."}),
    f"The start is $\\ln(13/7) \\approx {F0:.4f}$, so $p = 0.65$. The leaf value is $0.75/1.1375 \\approx {g8:.4f}$. "
    f"The new log-odds ${F8:.4f}$ give $p \\approx {p8:.4f}$."))

# A9 adding SHAP values in log-odds
s9 = -0.55 + 0.48 - 0.12 + 0.41
p9 = 1 / (1 + math.exp(-s9))
A.append(item("a-shap-sum", 2, ["en-interpret"], ["shap-additive"], 90, "Adding up the contributions",
    "A boosted classifier explains one prediction in log-odds. The base value is $-0.55$. "
    "Momentum adds $0.48$, volatility $-0.12$ and value $0.41$.",
    "What probability does the model give this case? Give 4 decimal places.",
    num(r(p9), 0.0005, [("log-odds", r(s9), 0.0005), ("base-only", r(1 / (1 + math.exp(0.55))), 0.0005)]),
    fb("The contributions add in log-odds, then the sigmoid turns them into a probability.", "Add the base and the three contributions, then apply $1/(1 + e^{-s})$.",
       {"log-odds": "You stopped at the log-odds. Apply the sigmoid to get a probability.",
        "base-only": "You gave the base value's probability. Add the three contributions first."}),
    f"The log-odds are $-0.55 + 0.48 - 0.12 + 0.41 = {s9:.2f}$. The probability is $1/(1 + e^{{-{s9:.2f}}}) \\approx {p9:.4f}$."))

# A10 the penalty at which the lasso keeps nothing
xty10 = [12.4, -18.6, 7.2, 15.0]
lmax10 = max(abs(v) for v in xty10) / 250
A.append(item("a-lasso-entry", 3, ["sl-regularise"], ["lasso-path-start"], 150, "Where the lasso path starts",
    "Four standardised features over 250 days have $\\mathbf X^T\\mathbf y = (12.4, -18.6, 7.2, 15.0)$. "
    "The lasso minimises $\\tfrac{1}{2n}\\|\\mathbf y - \\mathbf X\\boldsymbol\\beta\\|^2 + \\lambda\\|\\boldsymbol\\beta\\|_1$ with $n = 250$.",
    "What is the smallest $\\lambda$ at which every lasso slope is exactly zero? Give 4 decimal places.",
    num(r(lmax10), 0.00005, [("no-n", 18.6, 0.00005), ("signed-max", r(15.0 / 250), 0.00005), ("two-n", r(18.6 / 500), 0.00005)]),
    fb("All slopes are zero once $\\lambda \\ge \\max_j |\\mathbf x_j^T\\mathbf y|/n$.", "Write the subgradient condition at $\\boldsymbol\\beta = \\mathbf 0$ for each feature.",
       {"no-n": "You left out the $\\tfrac1n$ in front of the squares. It divides each $\\mathbf x_j^T\\mathbf y$ by 250.",
        "signed-max": "You took the largest signed value, 15.0. The condition uses absolute values, so $-18.6$ binds.",
        "two-n": "You divided by $2n$. Differentiating $\\tfrac{1}{2n}\\|\\cdot\\|^2$ cancels the 2."}),
    f"At $\\boldsymbol\\beta = \\mathbf 0$ the gradient of the fit term is $-\\mathbf X^T\\mathbf y/n$. Zero is optimal while every $|\\mathbf x_j^T\\mathbf y|/n \\le \\lambda$. "
    f"So the path starts at $18.6/250 = {lmax10:.4f}$, where the second feature enters first."))

# A11 the order of fractional differencing that sets the third weight
d11 = (1 - math.sqrt(0.2)) / 2
d11o = (1 + math.sqrt(0.2)) / 2
d11h = (1 - math.sqrt(0.6)) / 2
A.append(item("a-frac-weight", 3, ["fm-features"], ["frac-diff-weight"], 150, "Which order gives a weight of minus 0.1",
    "A fractionally differenced price is $\\sum_k w_k \\ln p_{t-k}$ with $w_0 = 1$ and $w_k = -w_{k-1}\\tfrac{d - k + 1}{k}$. "
    "For $0 < d < 1$, the weight $w_2$ is negative.",
    "Which $d$ below 0.5 makes $w_2 = -0.1$? Give 4 decimal places.",
    num(r(d11), 0.0005, [("other-root", r(d11o), 0.0005), ("dropped-half", r(d11h), 0.0005)]),
    fb("Write $w_2$ in terms of $d$, then solve the quadratic.", "Find $w_1 = -d$, then $w_2$ from the rule, and set it equal to $-0.1$.",
       {"other-root": "You took the root above 0.5. The question asks for the one below.",
        "dropped-half": "You left out the 2 in $w_2 = d(d - 1)/2$. The rule divides by $k = 2$."}),
    f"We have $w_1 = -d$ and $w_2 = d(d - 1)/2$. Setting $w_2 = -0.1$ gives $d^2 - d + 0.2 = 0$. "
    f"The roots are $(1 \\pm \\sqrt{{0.2}})/2$, so the one below 0.5 is {d11:.4f}."))

# A12 how many independent labels five overlapping ones are worth
def _uniq(spans):
    dmax = max(b for _, b in spans.values())
    conc = {d: sum(a <= d <= b for a, b in spans.values()) for d in range(1, dmax + 1)}
    u = {i: sum(1 / conc[d] for d in range(a, b + 1)) / (b - a + 1) for i, (a, b) in spans.items()}
    return conc, u, sum(u.values())


spans12 = {1: (1, 5), 2: (4, 7), 3: (6, 8), 4: (7, 10)}
spans12f = dict(spans12)
spans12f[5] = (3, 9)
conc12, u12, tot12 = _uniq(spans12f)
tot12_four = _uniq(spans12)[2]
A.append(item("a-label-uniqueness", 3, ["fm-labels"], ["label-uniqueness"], 180, "Five overlapping labels",
    "Four labels span days 1 to 5, 4 to 7, 6 to 8 and 7 to 10. A fifth label then spans days 3 to 9. "
    "A day covered by $c_t$ labels gives each of them $1/c_t$ of itself. "
    "A label's uniqueness is that share averaged over its own days.",
    "Add the five uniquenesses. About how many independent labels are the five worth? Give 2 decimal places.",
    num(r(tot12, 4), 0.005, [("count", 5, 0.005), ("four-before", r(tot12_four, 4), 0.005), ("old-plus-one", r(tot12_four + 1, 4), 0.005)]),
    fb("The fifth label overlaps the others, so the five are worth less than the four were.", "Find $c_t$ for days 1 to 10, average $1/c_t$ over each label, then add.",
       {"count": "You counted the labels. Overlapping labels share days, so each is worth less than one.",
        "four-before": "You added the four labels without the fifth. Count the fifth in every $c_t$ it covers.",
        "old-plus-one": "You gave the fifth label a full one. It shares days with the others, and it lowers their shares too."}),
    "Days 1 to 10 have $c_t = " + ", ".join(str(conc12[d]) for d in range(1, 11)) + f"$. The uniquenesses are "
    + ", ".join(f"{u12[i]:.4f}" for i in range(1, 5)) + f" and {u12[5]:.4f}, adding to {tot12:.2f}. "
    f"Without the fifth label the four were worth {tot12_four:.2f}, so adding it lowers the total."))

# A13 the probability that sizes a bet at half the full position
from statistics import NormalDist as _ND
z13 = _ND().inv_cdf(0.75)
q13 = 1 + z13 ** 2
p13 = (q13 + math.sqrt(q13 ** 2 - q13)) / (2 * q13)          # root above 0.5 of (p - 0.5)^2 = z^2 p (1 - p)
assert abs(2 * Phi((p13 - 0.5) / math.sqrt(p13 * (1 - p13))) - 1 - 0.5) < 1e-12
A.append(item("a-bet-size", 3, ["fm-sizing"], ["size-from-probability"], 150, "Sizing a bet backwards",
    "A meta-label gives a probability $p$ that a trade is right. The size rule is $m = 2\\Phi(z) - 1$, "
    "with $z = \\tfrac{p - 0.5}{\\sqrt{p(1 - p)}}$. Only $p > 0.5$ takes a long position.",
    "What probability $p$ gives half the full position, $m = 0.5$? Give 4 decimal places.",
    num(r(p13), 0.0005, [("linear", 0.75, 0.0005)]),
    fb("Half the position needs $\\Phi(z) = 0.75$.", "Find $z$ from $\\Phi(z) = 0.75$, then solve $(p - 0.5)^2 = z^2p(1 - p)$ for $p$.",
       {"linear": "You solved $2p - 1 = 0.5$. The rule passes $p$ through $z$ and $\\Phi$ first."}),
    f"A size of 0.5 needs $\\Phi(z) = 0.75$, so $z \\approx {z13:.4f}$. "
    "Then $(p - 0.5)^2 = z^2p(1 - p)$ is a quadratic in $p$. "
    f"Its root above 0.5 is {p13:.4f}."))

# A14 probabilistic Sharpe ratio
SR14, T14, g3, g4 = 0.12, 156, -0.8, 5.5
den14 = math.sqrt(1 - g3 * SR14 + (g4 - 1) / 4 * SR14 ** 2)
z14 = SR14 * math.sqrt(T14 - 1) / den14
psr14 = Phi(z14)
zn14 = SR14 * math.sqrt(T14 - 1) / math.sqrt(1 + 0.5 * SR14 ** 2)
zs14 = SR14 * math.sqrt(T14 - 1) / math.sqrt(1 + g3 * SR14 + (g4 - 1) / 4 * SR14 ** 2)
A.append(item("a-psr", 4, ["fm-eval"], ["probabilistic-sharpe"], 300, "How sure is a weekly Sharpe",
    "A strategy has a weekly Sharpe ratio of 0.12 over 156 weeks. Its returns have skew $-0.8$ and kurtosis 5.5. "
    "The probabilistic Sharpe ratio against 0 is "
    "$$\\Phi\\left(\\frac{\\widehat{SR}\\sqrt{T - 1}}{\\sqrt{1 - \\gamma_3\\widehat{SR} + \\frac{\\gamma_4 - 1}{4}\\widehat{SR}^2}}\\right).$$",
    "What is it? Give 4 decimal places.",
    num(r(psr14), 0.0005, [("normal", r(Phi(zn14)), 0.0005), ("skew-sign", r(Phi(zs14)), 0.0005)]),
    fb("Negative skew and fat tails widen the denominator.", "Put $\\gamma_3 = -0.8$ and $\\gamma_4 = 5.5$ into the denominator, then take $\\Phi$.",
       {"normal": "You used normal returns, skew 0 and kurtosis 3. This strategy's tails lower the confidence.",
        "skew-sign": "You added $\\gamma_3\\widehat{SR}$. The formula subtracts it, so negative skew raises the denominator."}),
    f"The denominator is $\\sqrt{{1 + 0.096 + 0.0162}} \\approx {den14:.4f}$. The numerator is $0.12\\sqrt{{155}} \\approx {SR14 * math.sqrt(155):.4f}$. "
    f"So $z \\approx {z14:.4f}$ and the ratio is $\\Phi(z) \\approx {psr14:.4f}$."))

# A15 choosing lambda without peeking (parts)
lams15 = [0.1, 1, 10, 100]
val15 = np.array([[4.10, 3.95, 3.90, 4.20], [3.70, 3.62, 3.66, 3.95], [4.40, 4.30, 4.18, 4.25]])
held15 = [3.85, 3.80, 3.88, 3.79]
mean15 = val15.mean(axis=0)
j15 = int(np.argmin(mean15))
A.append(parts("a-lambda-honest", 3, ["vl-cv", "vl-overfit"], ["honest-selection"], 240, "Choosing a penalty without peeking",
    "A ridge model is scored on three walk-forward validation blocks, then on a held-out final block. "
    "Mean squared errors, in units of $10^{-4}$:\n\n"
    "| $\\lambda$ | 0.1 | 1 | 10 | 100 |\n|---|---|---|---|---|\n"
    "| Block 1 | 4.10 | 3.95 | 3.90 | 4.20 |\n| Block 2 | 3.70 | 3.62 | 3.66 | 3.95 |\n"
    "| Block 3 | 4.40 | 4.30 | 4.18 | 4.25 |\n| Held out | 3.85 | 3.80 | 3.88 | 3.79 |",
    [("Which $\\lambda$ do the validation blocks choose?",
      num(lams15[j15], 0, [("held-out-peek", 100, 0), ("block-two", 1, 0)]),
      fb("The lowest mean over the three validation blocks.", "Average each column over blocks 1 to 3 and take the smallest.",
         {"held-out-peek": "You chose by the held-out row. That block is for the final report only.",
          "block-two": "You chose by block 2 alone. Average all three validation blocks."})),
     ("What held-out error, in units of $10^{-4}$, should the report state?",
      num(held15[j15], 0.005, [("best-held-out", min(held15), 0.005), ("validation-mean", r(mean15[j15], 4), 0.005)]),
      fb("The held-out error of the chosen $\\lambda$.", "Read the held-out row in the column you chose.",
         {"best-held-out": "You reported the best held-out value. Picking it after looking makes it optimistic.",
          "validation-mean": "You reported the validation mean. The held-out block gives the honest figure."}))],
    f"The validation means are {mean15[0]:.4f}, {mean15[1]:.4f}, {mean15[2]:.4f} and {mean15[3]:.4f}, so $\\lambda = 10$ wins. "
    f"Its held-out error, {held15[j15]:.2f}, is the honest figure. Quoting 3.79 would choose on the test block."))

# A16 the 2.1 exit task: walk-forward ridge, its penalty chosen on a time-ordered tail of each training span
wf_sol = ("import numpy as np\nimport pandas as pd\n\n\ndef _fit_predict(Xtr, ytr, Xte, lam):\n"
          "    m, s = Xtr.mean(axis=0), Xtr.std(axis=0)      # this fit's training rows only\n"
          "    Z, Zt = (Xtr - m) / s, (Xte - m) / s\n    yb = ytr.mean()\n"
          "    beta = np.linalg.solve(Z.T @ Z + lam * np.eye(Z.shape[1]), Z.T @ (ytr - yb))\n    return yb + Zt @ beta\n\n\n"
          "def nested_walk_forward(X, y, lams, first, step, val):\n    X, y = np.asarray(X, float), np.asarray(y, float)\n    errs = []\n"
          "    for start in range(first, len(y), step):\n        cut = start - val\n"
          "        scores = [np.mean((y[cut:start] - _fit_predict(X[:cut], y[:cut], X[cut:start], lam)) ** 2) for lam in lams]\n"
          "        lam = lams[int(np.argmin(scores))]\n        pred = _fit_predict(X[:start], y[:start], X[start:start + step], lam)\n"
          "        errs.extend((y[start:start + step] - pred) ** 2)\n    return float(np.mean(errs))\n")
wf_setup = ("import numpy as np, pandas as pd; df = pd.read_csv('factor-days.csv'); "
            "X = df[['f1', 'f2', 'f3', 'f4']].to_numpy(); y = df['y'].to_numpy()")
wf_hand = "X = [[1], [2], [4], [3], [6], [5], [8], [7], [9], [11]]; y = [0.1, 0.3, 0.2, 0.5, 0.4, 0.7, 0.6, 0.9, 0.8, 1.2]"
LAMS = "[0.1, 1.0, 10.0, 100.0, 1000.0]"
wf_cases = [(wf_setup, f"nested_walk_forward(X, y, {LAMS}, 150, 50, 50)"), (wf_setup, f"nested_walk_forward(X, y, {LAMS}, 200, 40, 60)"),
            (wf_setup, "nested_walk_forward(X, y, [0.0], 200, 40, 60)"), (wf_setup, f"nested_walk_forward(X, y, {LAMS}, 120, 100, 40)"),
            (wf_hand, "nested_walk_forward(X, y, [0.1, 10.0], 6, 2, 2)")]
wf_tests = [T(c, rep(run_solution(wf_sol, c, s)), setup=s, tol={"rel": 1e-7}) for s, c in wf_cases]
A.append(item("a-walk-forward-ridge", 5, ["vl-time", "vl-leakage", "vl-cv", "sl-setup", "sl-linear", "sl-regularise"], ["nested-walk-forward"], 1500,
    "One tabular problem, walked forward",
    "`factor-days.csv` holds 360 trading days in date order: features `f1` to `f4` and the next day's return `y`. Feature `f4` drifts upward. "
    "Test blocks start at row `first` and hold `step` rows, the last perhaps fewer. "
    "For each block, the last `val` rows before it validate each penalty in `lams`, fitted on the rows before them. "
    "The best penalty, the first if tied, is refitted on every row before the block and predicts it. "
    "Every fit scales features by its own training rows' mean and population standard deviation, and penalises the slopes only. "
    "A fit with penalty $\\lambda$ minimises $\\sum_i (y_i - \\hat y_i)^2 + \\lambda\\sum_j \\beta_j^2$, as `Ridge(alpha=lam)` does.",
    "Write `nested_walk_forward(X, y, lams, first, step, val)`: the mean squared error over all test rows.",
    {"kind": "code", "language": "python", "data": {"factor-days.csv": DATA_REL + "factor-days.csv"},
     "starter": "# keep these imports: the tests load the file with pandas\nimport numpy as np\nimport pandas as pd\n\n\ndef nested_walk_forward(X, y, lams, first, step, val):\n    # choose each penalty on rows before the block\n    ...\n",
     "solution": wf_sol,
     "examples": [ex(wf_tests[0])],
     "tests": wf_tests,
     "how": "Check runs 5 hidden tests at a relative tolerance of 1e-7. Tests 1 to 4 read the file; test 5 is a small hand case."},
    code_fb("Every choice and every fit sees only rows before the block it scores.",
            {"test-1": "Test 1 is the file with five penalties. Choose each on the validation tail, and scale every fit by its own training rows.",
             "test-2": "Test 2 has a longer tail. The inner fit stops `val` rows before the block; the refit uses them all.",
             "test-3": "Test 3 has one penalty, 0, so no choice is made. Check the block edges and the intercept.",
             "test-4": "Test 4's last block holds 40 rows. Average over every test row, not over blocks.",
             "test-5": "Test 5 has one feature. Each fit, inner or outer, rescales with its own training rows."}),
    "The penalty is chosen on a tail that ends before the block, so the test error stays honest. "
    "Scaling on the full sample would let the drifting feature carry later means into every fit. "
    "Choosing the penalty by the test blocks' own errors would report the best of five, which is optimistic."))

# ======================================================================== Paper B: time series
# B1 why returns and not prices
B.append(item("b-returns-not-prices", 2, ["ts-stationary"], ["returns-not-prices"], 90, "Returns or prices",
    None, "Why do we fit an ARMA model to daily log returns rather than to log prices?",
    choice([opt("a", "Log prices have a unit root, so their mean and variance drift and the tests mislead.", correct=True),
            opt("b", "Returns are normally distributed while prices are not, and ARMA needs normal data.",
                "You took normality as the reason. Returns have fat tails too; the problem is the unit root."),
            opt("c", "Prices are autocorrelated and returns never are, so an ARMA on returns is simpler.",
                "You blamed autocorrelation. ARMA models autocorrelation; it cannot model a unit root."),
            opt("d", "Returns are larger numbers than log prices, so the fitted coefficients are more precise.",
                "You looked at the size of the numbers. Scale changes nothing; shocks that never fade are the problem.")]),
    fb("A unit root makes the price's shocks permanent.", "Ask what happens to the variance of a log price as time passes."),
    "A log price is a random walk to a good approximation, so its variance grows with time. "
    "Regressions and t tests on such a series give spurious results. Differencing once gives returns, which are stationary."))

# B2 the long-run spread of an AR(1)
phi2, c2b, se2 = 0.6, 0.3, 0.02
sd2 = se2 / math.sqrt(1 - phi2 ** 2)
B.append(item("b-ar1-spread", 3, ["ts-stationary"], ["ar1-variance"], 150, "How wide an AR(1) wanders",
    "A spread follows $s_t = 0.3 + 0.6s_{t-1} + \\varepsilon_t$, with shocks of standard deviation 0.02 basis points.",
    "What is the spread's long-run standard deviation, in basis points?",
    num(r(sd2), 0.0005, [("no-square", r(se2 / (1 - phi2)), 0.0005), ("shock-sd", se2, 0.0005)]),
    fb("The variance solves $V = 0.36V + 0.0004$.", "Take the variance of both sides of the equation in the steady state.",
       {"no-square": "You divided by $1 - \\phi$. The variance divides by $1 - \\phi^2$, then take the root.",
        "shock-sd": "You gave the shock's standard deviation. Past shocks add to it through $\\phi$."}),
    f"In the steady state $V = \\phi^2 V + \\sigma^2$, so $V = 0.0004/0.64 = 0.000625$. The standard deviation is ${sd2:.3f}$ basis points."))

# B3 Ljung-Box on three lags
n3, rh3 = 250, [0.12, -0.05, 0.08]
Q3 = n3 * (n3 + 2) * sum(rk ** 2 / (n3 - k) for k, rk in enumerate(rh3, 1))
BP3 = n3 * sum(rk ** 2 for rk in rh3)
B.append(item("b-ljung-box", 3, ["ts-acf"], ["ljung-box"], 150, "Three lags of a residual",
    "An AR(1) fit on 250 days leaves residual autocorrelations $0.12, -0.05$ and $0.08$ at lags 1, 2 and 3.",
    "What is the Ljung-Box statistic $Q = n(n + 2)\\sum_k \\hat\\rho_k^2/(n - k)$ over these three lags? Give 2 decimal places.",
    num(r(Q3, 4), 0.005, [("box-pierce", r(BP3, 4), 0.005), ("no-square", r(n3 * (n3 + 2) * sum(rk / (n3 - k) for k, rk in enumerate(rh3, 1)), 4), 0.005)]),
    fb(f"$Q \\approx {Q3:.2f}$, just below 5.99, the 5% point of $\\chi^2_2$: three lags less one fitted coefficient.", "Square each autocorrelation, divide by $n - k$, add, then multiply by $n(n + 2)$.",
       {"box-pierce": "You used $n\\sum\\hat\\rho_k^2$, the Box-Pierce form. Ljung-Box weights each lag by $(n + 2)/(n - k)$.",
        "no-square": "You added the autocorrelations without squaring. Signs would then cancel."}),
    f"$Q = 250 \\times 252 \\times (0.0144/249 + 0.0025/248 + 0.0064/247) \\approx {Q3:.2f}$. "
    "That is below 5.99, the 5% point of $\\chi^2_2$, so the test finds no autocorrelation left at these lags."))

# B4 the persistence of an AR(2)
roots4 = sorted(np.roots([1, -1.1, 0.3]).real)
B.append(item("b-ar2-root", 3, ["ts-models"], ["ar2-roots"], 150, "How fast an AR(2) forgets",
    "Order flow follows $x_t = 1.1x_{t-1} - 0.3x_{t-2} + \\varepsilon_t$. "
    "A shock fades like $\\lambda^k$, where $\\lambda$ is the largest root of $\\lambda^2 = 1.1\\lambda - 0.3$.",
    "What is that root?",
    num(r(roots4[-1]), 0.0005, [("smaller", r(roots4[0]), 0.0005), ("sum", 0.8, 0.0005)]),
    fb("The roots are 0.6 and 0.5, both inside the unit circle.", "Solve $\\lambda^2 - 1.1\\lambda + 0.3 = 0$ and take the larger root.",
       {"smaller": "You gave the smaller root. The slower decay, the larger root, sets the persistence.",
        "sum": "You added the coefficients. Their sum shows stationarity, but the decay rate is a root."}),
    "The roots are $(1.1 \\pm \\sqrt{1.21 - 1.2})/2 = (1.1 \\pm 0.1)/2$, so 0.6 and 0.5. "
    "Both lie inside the unit circle, so the process is stationary and shocks fade like $0.6^k$."))

# B5 an AR(2) fitted by Yule-Walker
r1_5, r2_5 = 0.45, 0.05
ph2_5 = (r2_5 - r1_5 ** 2) / (1 - r1_5 ** 2)
ph1_5 = r1_5 * (1 - r2_5) / (1 - r1_5 ** 2)
B.append(item("b-yule-walker", 4, ["ts-acf", "ts-models"], ["yule-walker"], 240, "An AR(2) from two autocorrelations",
    "A daily volume series has sample autocorrelations $\\hat\\rho_1 = 0.45$ and $\\hat\\rho_2 = 0.05$. "
    "An AR(2) fitted by Yule-Walker solves $\\rho_1 = \\phi_1 + \\phi_2\\rho_1$ and $\\rho_2 = \\phi_1\\rho_1 + \\phi_2$.",
    "What is $\\hat\\phi_2$, which is also the lag-2 partial autocorrelation? Give 4 decimal places.",
    num(r(ph2_5), 0.0005, [("gave-acf", r2_5, 0.0005), ("no-denominator", r(r2_5 - r1_5 ** 2), 0.0005), ("gave-phi1", r(ph1_5), 0.0005)]),
    fb("$\\hat\\phi_2 = (\\rho_2 - \\rho_1^2)/(1 - \\rho_1^2)$.", "Eliminate $\\phi_1$: take $\\rho_1$ times the first equation from the second.",
       {"gave-acf": "You gave $\\hat\\rho_2$. The partial autocorrelation removes what lag 1 already explains.",
        "no-denominator": "You stopped at $\\rho_2 - \\rho_1^2$. Divide by $1 - \\rho_1^2$.",
        "gave-phi1": "You gave $\\hat\\phi_1$. The question asks for the lag-2 coefficient."}),
    f"Eliminating $\\phi_1$ gives $\\phi_2(1 - \\rho_1^2) = \\rho_2 - \\rho_1^2$. So $\\hat\\phi_2 = -0.1525/0.7975 \\approx {ph2_5:.4f}$. "
    f"Then $\\hat\\phi_1 \\approx {ph1_5:.4f}$."))

# B6 forecasts from an MA(1)
mu6, th6, e6 = 0.0008, 0.35, 0.014
f1_6 = mu6 + th6 * e6
B.append(parts("b-ma-forecast", 3, ["ts-forecast"], ["ma-forecast"], 180, "Forecasts from an MA(1)",
    "Daily returns follow $r_t = 0.0008 + \\varepsilon_t + 0.35\\varepsilon_{t-1}$. Today's fitted shock is $\\varepsilon_T = 0.014$.",
    [("What is the forecast of tomorrow's return?",
      num(r(f1_6), 0.00005, [("no-mean", r(th6 * e6), 0.00005), ("no-shock", mu6, 0.00005)]),
      fb("The mean plus 0.35 times today's shock.", "Tomorrow's own shock has mean 0; today's shock is known.",
         {"no-mean": "You left out the mean 0.0008.", "no-shock": "You dropped today's shock. It enters tomorrow through $0.35\\varepsilon_T$."})),
     ("What is the forecast of the return two days ahead?",
      num(mu6, 0.00005, [("decayed", r(mu6 + th6 ** 2 * e6), 0.00005), ("same-as-one", r(f1_6), 0.00005)]),
      fb("An MA(1) has no memory past one day.", "Both shocks in the two-day-ahead return are unknown today.",
         {"decayed": "You decayed the shock by $0.35^2$, as an AR(1) would. An MA(1) forgets it after one day.",
          "same-as-one": "You repeated tomorrow's forecast. Today's shock does not reach two days ahead."}))],
    f"Tomorrow's return is $0.0008 + 0.35 \\times 0.014 = {f1_6:.4f}$. "
    "Two days ahead, both shocks are in the future, so the forecast is the mean, 0.0008."))

# B7 an ARCH LM test
n7b, R2_7 = 750, 0.0188
LM7 = n7b * R2_7
B.append(item("b-arch-lm", 2, ["gv-clustering"], ["arch-lm"], 90, "Is there volatility clustering",
    "We regress squared residuals on five of their own lags over 750 days. The regression has $R^2 = 0.0188$.",
    "What is the ARCH LM statistic $nR^2$?",
    num(r(LM7, 4), 0.05, [("per-lag", r(LM7 / 5, 4), 0.02), ("r-not-n", r(R2_7 * 100, 4), 0.02)]),
    fb(f"$nR^2 = {LM7:.1f}$, above 11.07, the 5% point of $\\chi^2_5$.", "Multiply the number of days by $R^2$.",
       {"per-lag": "You divided by the 5 lags. The statistic is $nR^2$, compared with $\\chi^2_5$.",
        "r-not-n": "You turned $R^2$ into a percentage. Multiply by $n = 750$."}),
    f"$nR^2 = 750 \\times 0.0188 = {LM7:.1f}$. It beats 11.07, the 5% point of $\\chi^2_5$, so the squared residuals carry memory."))

# B8 fixing omega of a GARCH(1,1) by variance targeting
vol8, days8, al8, be8 = 0.18, 252, 0.06, 0.92
V8 = vol8 ** 2 / days8
om8 = V8 * (1 - al8 - be8)
B.append(item("b-garch-target", 3, ["gv-models"], ["garch-variance-target"], 150, "Fixing omega by variance targeting",
    "A desk fits a GARCH(1,1) to daily returns with variance targeting. "
    "It fixes the long-run volatility at 18% a year, over 252 days, and estimates $\\alpha = 0.06$ and $\\beta = 0.92$.",
    "What $\\omega$ does that fix? Give it in units of $10^{-6}$ to 2 decimal places.",
    num(r(om8 * 1e6, 4), 0.005, [("annual", r(vol8 ** 2 * (1 - al8 - be8) * 1e6, 4), 0.005),
                                  ("vol-not-variance", r(vol8 / math.sqrt(days8) * (1 - al8 - be8) * 1e6, 4), 0.005),
                                  ("one-minus-beta", r(V8 * (1 - be8) * 1e6, 4), 0.005)]),
    fb("The long-run variance times $1 - \\alpha - \\beta$ is $\\omega$.", "Turn 18% a year into a daily variance, then multiply by $1 - \\alpha - \\beta$.",
       {"annual": "You used the annual variance. Divide $0.18^2$ by 252 to get the daily variance first.",
        "vol-not-variance": "You used the daily volatility as if it were a variance. Square it first.",
        "one-minus-beta": "You multiplied by $1 - \\beta$. The factor is $1 - \\alpha - \\beta$."}),
    f"The daily long-run variance is $0.18^2/252 \\approx {V8 * 1e4:.4f} \\times 10^{{-4}}$. "
    f"Then $\\omega = V_L(1 - \\alpha - \\beta) = {V8 * 1e4:.4f} \\times 10^{{-4}} \\times 0.02$. "
    f"That is ${om8 * 1e6:.2f} \\times 10^{{-6}}$."))

# B9 an EWMA update
lam9, s9b, r9 = 0.94, 0.011, -0.028
v9 = lam9 * s9b ** 2 + (1 - lam9) * r9 ** 2
B.append(item("b-ewma-update", 3, ["gv-forecast"], ["ewma-update"], 150, "Tomorrow's volatility after a bad day",
    "A risk desk uses an EWMA with $\\lambda = 0.94$. Yesterday's volatility estimate was 0.011 a day, and today's return was $-0.028$.",
    "What is the new daily volatility estimate? Give 5 decimal places.",
    num(r(math.sqrt(v9)), 0.00005, [("swapped", r(math.sqrt((1 - lam9) * s9b ** 2 + lam9 * r9 ** 2)), 0.00005),
                                     ("vol-not-variance", r(lam9 * s9b + (1 - lam9) * abs(r9)), 0.00005)]),
    fb("Average the variances, not the volatilities.", "Use $\\sigma_t^2 = 0.94\\sigma_{t-1}^2 + 0.06r_t^2$, then take the root.",
       {"swapped": "You put 0.94 on the new return. The weight 0.94 belongs to the old variance.",
        "vol-not-variance": "You averaged volatilities. EWMA averages squared values, then takes the root."}),
    f"$\\sigma^2 = 0.94 \\times 0.000121 + 0.06 \\times 0.000784 \\approx {v9 * 1e4:.4f} \\times 10^{{-4}}$. "
    f"The volatility is ${math.sqrt(v9):.5f}$ a day."))

# B10 expected shortfall from a volatility forecast
pos10, sig10, a10 = 3_000_000, 0.014, 0.025
z10 = 1.959963984540054
ES10 = pos10 * sig10 * phi(z10) / a10
VaR10 = pos10 * sig10 * z10
B.append(item("b-es-normal", 4, ["gv-risk"], ["expected-shortfall"], 240, "The average loss beyond the line",
    "A GARCH model forecasts tomorrow's volatility at 0.014 for a £3,000,000 position. Returns are taken as normal with mean 0.",
    "What is the one-day 97.5% expected shortfall, in pounds?",
    num(r(ES10, 2), 100, [("var", r(VaR10, 2), 10), ("density-only", r(pos10 * sig10 * phi(z10), 2), 10)], unit="£"),
    fb("For a normal, $ES = \\sigma\\varphi(z)/(1 - 0.975)$.", "Find $z = 1.96$, its density $\\varphi(z)$, then divide by the tail mass 0.025.",
       {"var": "You gave the 97.5% value at risk. Expected shortfall averages the losses beyond it.",
        "density-only": "You forgot to divide by the tail mass 0.025."}),
    f"$\\varphi(1.96) \\approx {phi(z10):.5f}$, so $ES = 42{{,}}000 \\times {phi(z10):.5f}/0.025$. "
    f"That is about £{ES10:,.0f}, against a value at risk of £{VaR10:,.0f}."))

# B11 a regression of one random walk on another
B.append(item("b-spurious-read", 3, ["co-spurious"], ["spurious-regression"], 150, "A slope that is too good",
    "We regress the log price of one share on an unrelated share's log price over 1,000 days. "
    "The slope has $t = 11.4$, $R^2 = 0.42$, and the residuals have lag-1 autocorrelation 0.98.",
    "Which reading is right?",
    choice([opt("a", "The residuals look like a random walk, so test them for a unit root before trusting $t$.", correct=True),
            opt("b", "A $t$ of 11.4 shows a strong link at any usual significance level, so the pair is related.",
                "You read $t$ as if the residuals were stationary. With a unit root in them, $t$ grows with the sample."),
            opt("c", "An $R^2$ of 0.42 is low, so the two prices are unrelated and the slope is noise.",
                "You judged by $R^2$. Unrelated random walks often give a high $R^2$; the residuals decide."),
            opt("d", "With 1,000 days the slope is estimated precisely, so a hedge built on it is safe.",
                "You trusted the sample size. In a spurious regression more days make $t$ larger, not the slope truer.")]),
    fb("Residuals that barely mean-revert are the warning.", "Look at the residuals' autocorrelation before the $t$ statistic."),
    "Two independent random walks regressed on each other give large $t$ values far too often. "
    "Residuals with autocorrelation 0.98 are close to a random walk. Test them for a unit root before trusting the slope."))

# B12 a Dickey-Fuller t by hand
e12 = np.array([0.40, 0.25, 0.05, 0.12, -0.06, 0.02, -0.10, 0.03])
de12, el12 = np.diff(e12), e12[:-1]
rho12 = float(el12 @ de12 / (el12 @ el12))
u12b = de12 - rho12 * el12
s2_12 = float(u12b @ u12b) / (len(de12) - 1)
t12 = rho12 / math.sqrt(s2_12 / float(el12 @ el12))
B.append(item("b-df-hand", 4, ["co-test"], ["dickey-fuller-hand"], 300, "A unit-root test by hand",
    "A pair regression leaves residuals $e_t$: $0.40, 0.25, 0.05, 0.12, -0.06, 0.02, -0.10, 0.03$. "
    "We regress $\\Delta e_t$ on $e_{t-1}$ with no constant. The residual variance divides by the 7 changes less one.",
    "What is the $t$ statistic of the slope? Give 2 decimal places.",
    num(r(t12, 4), 0.01, [("slope", r(rho12, 4), 0.005), ("n-divisor", r(t12 * math.sqrt(7 / 6), 4), 0.005)]),
    fb("The slope over its standard error.", "Find $\\hat\\rho = \\sum e_{t-1}\\Delta e_t/\\sum e_{t-1}^2$, then its standard error from the fitted residuals.",
       {"slope": "You gave the slope $\\hat\\rho$. Divide it by its standard error.",
        "n-divisor": "You divided the residual sum of squares by 7. With one slope fitted, divide by 6."}),
    f"$\\sum e_{{t-1}}\\Delta e_t = {float(el12 @ de12):.4f}$ and $\\sum e_{{t-1}}^2 = {float(el12 @ el12):.4f}$, so $\\hat\\rho \\approx {rho12:.4f}$. "
    f"The residual variance is {s2_12:.5f}, giving $t \\approx {t12:.2f}$. "
    "That misses the Engle-Granger 5% point, about $-3.34$, though it passes $-1.95$, the plain Dickey-Fuller point."))

# B13 the 2.2 exit task: an augmented Dickey-Fuller test on a pair's spread, then the half-life
eg_sol = ("import numpy as np\nimport pandas as pd\n\n\ndef adf1_spread(a, b):\n    y, x = np.log(np.asarray(a, float)), np.log(np.asarray(b, float))\n"
          "    X = np.column_stack([np.ones(len(x)), x])\n    coef = np.linalg.lstsq(X, y, rcond=None)[0]\n    e = y - X @ coef\n"
          "    de = np.diff(e)\n    Z = np.column_stack([e[1:-1], de[:-1]])   # e_{t-1} and the lagged change\n    Y = de[1:]\n"
          "    g = np.linalg.lstsq(Z, Y, rcond=None)[0]\n    u = Y - Z @ g\n    s2 = (u @ u) / (len(Y) - 2)\n"
          "    se = np.sqrt(s2 * np.linalg.inv(Z.T @ Z)[0, 0])\n    return float(coef[1]), float(g[0] / se)\n")
eg_setup = ("import numpy as np, pandas as pd; df = pd.read_csv('pair-closes.csv'); "
            "a = df['a'].to_numpy(); b = df['b'].to_numpy(); c = df['c'].to_numpy()")
eg_hand = "a = [10, 10.5, 10.2, 10.8, 10.4, 10.9, 10.6, 11.0]; b = [20, 20.6, 20.5, 21.2, 20.9, 21.5, 21.3, 21.6]"
eg_cases = [(eg_setup, "adf1_spread(a, b)[0]"), (eg_setup, "adf1_spread(a, b)[1]"), (eg_setup, "adf1_spread(a[:250], b[:250])[1]"),
            (eg_setup, "adf1_spread(a, c)[1]"), (eg_hand, "adf1_spread(a, b)[1]")]
eg_tests = [T(c, rep(run_solution(eg_sol, c, s)), setup=s, tol={"rel": 1e-7}) for s, c in eg_cases]
eg_vals = [float(t["expect"]) for t in eg_tests]
_df = pd.read_csv(os.path.join(DATA, 'pair-closes.csv'))
_y, _x = np.log(_df['a'].to_numpy()), np.log(_df['b'].to_numpy())
_X = np.column_stack([np.ones(len(_x)), _x])
_e = _y - _X @ np.linalg.lstsq(_X, _y, rcond=None)[0]
rho13 = float(_e[:-1] @ np.diff(_e) / (_e[:-1] @ _e[:-1]))
rho13g = round(rho13, 4)
hl13 = math.log(0.5) / math.log(1 + rho13g)
B.append(parts("b-eg-pair", 5, ["co-test", "co-spread"], ["engle-granger-adf"], 1200, "A pair tested for cointegration",
    "`pair-closes.csv` holds 500 daily closes of three shares, `a`, `b` and `c`, in date order.",
    [("Write `adf1_spread(a, b)` for two arrays of closes, returning `(beta, t)`.",
      {"kind": "code", "language": "python", "data": {"pair-closes.csv": DATA_REL + "pair-closes.csv"},
       "starter": "# keep these imports: the tests load the file with pandas\nimport numpy as np\nimport pandas as pd\n\n\ndef adf1_spread(a, b):\n    # returns (beta, t)\n    ...\n",
       "solution": eg_sol,
       "examples": [ex(eg_tests[0])],
       "tests": eg_tests,
       "how": "Check runs 5 hidden tests at a relative tolerance of 1e-7. Tests 1 to 4 read the file; test 5 is a short hand case."},
      code_fb("Beta first, then the augmented unit-root $t$ on the residuals.",
              {"test-1": "Test 1 is beta. Regress the log of `a` on a constant and the log of `b`, not the prices.",
               "test-2": "Test 2 is the $t$ statistic. Keep the lagged change as a second regressor, and divide by the observations less 2.",
               "test-4": "Test 4 pairs `a` with `c`, which is unrelated. Its residuals barely revert, so $t$ is small."}),
      "Both log prices have a unit root on the file; their own ADF tests do not reject. "
      "Regress $\\ln a$ on a constant and $\\ln b$ by least squares; the slope is beta. Take the residuals $e_t$. "
      "Regress $\\Delta e_t$ on $e_{t-1}$ and $\\Delta e_{t-1}$, with no constant, over every $t$ that has both. "
      "Then `t` is the coefficient on $e_{t-1}$ over its standard error. Divide the residual sum of squares by the observations less 2."),
     (f"A first-order fit $\\Delta e_t = \\hat\\rho e_{{t-1}}$ of the file's spread gives $\\hat\\rho = {rho13g}$. What is the spread's half-life in days? Give 2 decimal places.",
      num(r(hl13, 4), 0.05, [("small-rho", r(-math.log(2) / rho13g, 4), 0.05), ("no-log", r(-1 / rho13g, 4), 0.05)]),
      fb("The spread keeps $1 + \\hat\\rho$ of itself each day.", "Solve $(1 + \\hat\\rho)^h = 0.5$ for $h$.",
         {"small-rho": "You used $-\\ln 2/\\hat\\rho$, the small-slope shortcut. Use $\\ln 0.5/\\ln(1 + \\hat\\rho)$.",
          "no-log": "You took $-1/\\hat\\rho$, the mean life. The half-life uses $\\ln 0.5$."}))],
    f"On the file, $a$ against $b$ gives $t \\approx {eg_vals[1]:.2f}$, well past $-3.34$, so we reject no cointegration at 5%. "
    f"Against $c$ it gives ${eg_vals[3]:.2f}$, short of the Engle-Granger line. "
    f"The spread keeps $1 + \\hat\\rho = {1 + rho13g:.4f}$ a day, so it halves in about {hl13:.2f} days."))

# B14 the hedge notional from a log-price regression
beta14, long14 = 1.6, 800_000
B.append(item("b-hedge-notional", 2, ["co-pairs"], ["hedge-notional"], 90, "How much to short",
    "A pair has $\\ln A = 0.35 + 1.6\\ln B + e$. You buy £800,000 of A.",
    "How many pounds of B do you sell to hedge it?",
    num(int(round(beta14 * long14)), 1, [("divided", int(round(long14 / beta14)), 1), ("equal", long14, 1)], unit="£"),
    fb("A 1% move in B moves A by 1.6%.", "In log prices the slope is a ratio of percentage moves, so scale the notional by it.",
       {"divided": "You divided by 1.6. A moves 1.6 times as much as B in percentage terms, so B needs more notional.",
        "equal": "You matched notionals. The slope says A moves 1.6% for each 1% of B."}),
    f"A 1% move in B moves A by 1.6%, or £12,800 on £800,000. Selling £{beta14 * long14:,.0f} of B loses the same £12,800 on that move."))

# B15 a pair trade's net P&L
qa15, qb15 = 20_000, 70_000
pa15, pb15 = (50.00, 48.20), (20.00, 20.10)
gross15 = qa15 * (pa15[0] - pa15[1]) + qb15 * (pb15[1] - pb15[0])
traded15 = qa15 * (pa15[0] + pa15[1]) + qb15 * (pb15[0] + pb15[1])
cost15 = 0.0005 * traded15
B.append(item("b-pair-pnl", 3, ["co-pairs"], ["pair-pnl"], 150, "What a pair trade made",
    "You sold 20,000 A at £50.00 and bought 70,000 B at £20.00. You closed both when A was £48.20 and B was £20.10. "
    "Each trade costs 5 basis points of its value.",
    "What is the net P&L, in pounds?",
    num(r(gross15 - cost15, 2), 0.5, [("gross", r(gross15, 2), 0.5), ("entry-costs-only", r(gross15 - 0.0005 * (qa15 * pa15[0] + qb15 * pb15[0]), 2), 0.5)], unit="£"),
    fb("Gross P&L less costs on all four trades.", "Add the two legs' P&L, then charge 5 basis points on the value of each of the four trades.",
       {"gross": "You left out the costs. Each of the four trades pays 5 basis points.",
        "entry-costs-only": "You charged costs on the opening trades only. Closing both legs costs as well."}),
    f"The short makes £36,000 and the long £7,000, so £{gross15:,.0f} gross. "
    f"The four trades are worth £{traded15:,.0f}, costing £{cost15:,.2f}. Net P&L is £{gross15 - cost15:,.2f}."))
# ======================================================================== Paper C: numerical methods and optimisation (topic 2.5; topic 2.6 sits in topic-2.6)
# C1 a float32 running total
tot1 = np.float32(100000)
for _ in range(1000):
    tot1 = np.float32(tot1 + np.float32(0.01))
grow1 = float(tot1) - 100000
ulp1 = 2.0 ** (16 - 23)
C.append(item("c-float32-fees", 3, ["nm-float"], ["float-absorption"], 150, "A running total in single precision",
    "A ledger keeps a running total in 32-bit floats, which carry a 24-bit significand. "
    "The total starts at £100,000 and a 1p fee is added 1,000 times.",
    "By how much, in pounds, has the stored total grown?",
    num(grow1, 0.005, [("exact", 10, 0.0001), ("absorbed", 0, 0.0001)], unit="£"),
    fb("Each 1p rounds to one step of the float grid, $2^{-7}$ pounds.", "Find the spacing of 32-bit floats between $2^{16}$ and $2^{17}$, then round 0.01 to it.",
       {"exact": "You added the fees exactly. Near £100,000 the float grid is too coarse to hold 1p.",
        "absorbed": "You let every fee vanish. A fee rounds to the nearest grid step, and 0.01 is nearer $2^{-7}$ than 0."}),
    f"Between $2^{{16}}$ and $2^{{17}}$ the spacing is $2^{{16 - 23}} = {ulp1}$. "
    f"Each 1p fee rounds to one step, so 1,000 fees add $1000 \\times {ulp1} = {grow1}$ pounds, not £10."))

# C2 the correlation at which a pair of signals loses four digits
kap2 = 1e4
rho2c = (kap2 - 1) / (kap2 + 1)
C.append(item("c-condition-digits", 3, ["nm-stability"], ["condition-digits"], 150, "How close to one before digits go",
    "Two assets have correlation matrix $\\begin{pmatrix} 1 & r \\\\ r & 1 \\end{pmatrix}$ with $0 < r < 1$. "
    "Solving a system with a matrix of condition number $\\kappa = \\lambda_{\\max}/\\lambda_{\\min}$ can lose about $\\log_{10}\\kappa$ significant digits.",
    "At what $r$ does $\\kappa$ reach $10^4$, so about four digits go? Give 4 decimal places.",
    num(r(rho2c, 6), 0.00002, [("one-over-gap", r(1 - 1 / kap2), 0.00002)]),
    fb("The eigenvalues are $1 \\pm r$.", "Find both eigenvalues in terms of $r$, set their ratio to $10^4$, then solve for $r$.",
       {"one-over-gap": "You solved $1/(1 - r) = 10^4$. The larger eigenvalue is $1 + r$, not 1."}),
    "The eigenvalues are $1 + r$ and $1 - r$, so $\\kappa = (1 + r)/(1 - r)$. "
    "Setting $\\kappa = 10^4$ gives $r = (10^4 - 1)/(10^4 + 1)$. "
    f"That is about {rho2c:.4f}, so a correlation that close to 1 costs four of the sixteen digits."))

# C3 one Newton step for a bond yield
f3c = lambda y: 5 / (1 + y) + 105 / (1 + y) ** 2 - 95
fp3c = lambda y: -5 / (1 + y) ** 2 - 210 / (1 + y) ** 3
y1_3 = 0.05 - f3c(0.05) / fp3c(0.05)
v3 = (-5 + math.sqrt(25 + 4 * 105 * 95)) / (2 * 105)
ytrue3 = 1 / v3 - 1
C.append(item("c-newton-yield", 2, ["nm-roots"], ["newton-yield"], 150, "One Newton step for a yield",
    "A bond costs 95 and pays 5 in one year and 105 in two. Its yield solves $f(y) = \\tfrac{5}{1 + y} + \\tfrac{105}{(1 + y)^2} - 95 = 0$.",
    "Newton's method starts at $y_0 = 0.05$. What is $y_1$? Give 4 decimal places.",
    num(r(y1_3), 0.00005, [("sign", r(0.05 + f3c(0.05) / fp3c(0.05)), 0.00005), ("converged", r(ytrue3), 0.00005)]),
    fb("$y_1 = y_0 - f(y_0)/f'(y_0)$.", "Find $f(0.05)$ and $f'(0.05)$, then take one step.",
       {"sign": "You added $f/f'$. Newton subtracts it, and here $f' < 0$, so $y$ rises.",
        "converged": "You gave the exact yield. The question asks for the first step only."}),
    f"$f(0.05) = 4.7619 + 95.2381 - 95 = 5$ and $f'(0.05) \\approx {fp3c(0.05):.4f}$. "
    f"So $y_1 = 0.05 + 5/{-fp3c(0.05):.4f} \\approx {y1_3:.4f}$, near the true yield {ytrue3:.4f}."))

# C4 Simpson's rule across a jump (a digital call)
C.append(item("c-simpson-jump", 4, ["nm-quadrature"], ["quadrature-jump"], 240, "Simpson's rule over a digital strike",
    "A digital call pays £1 when $S_T > K$. It is priced by Simpson's rule on $\\int \\mathbf 1\\{S(z) > K\\}\\varphi(z)\\,dz$ over a fixed grid of $z$. "
    "The strike falls between two nodes.",
    "How does the error shrink as the spacing $h$ falls, and what fixes it?",
    choice([opt("a", "Like $h$, since the payoff jumps at the strike; split the integral there for $h^4$.", correct=True),
            opt("b", "Like $h^2$, as for a call's kink; split the integral at the strike to get $h^4$ back.",
                "You used the rate for a call's kink. A jump in the payoff costs more than a kink does."),
            opt("c", "Like $h^4$, which is Simpson's usual order, so nothing needs fixing at the strike.",
                "You took Simpson's $h^4$ as given. It needs a smooth integrand, and the jump breaks that."),
            opt("d", "Not at all, since the payoff is bounded; refine the grid far from the strike instead.",
                "You trusted the bound on the payoff. The jump at the strike is the trouble, not the tails.")]),
    fb("A jump between nodes costs three orders.", "Ask where the integrand fails to be smooth, and whether a node sits there."),
    "Simpson's $h^4$ error needs a smooth integrand on each panel. A panel holding the strike sees a jump of 1 in the payoff, which leaves an error of order $h$. "
    "Starting a panel at the strike, where the payoff jumps, restores $h^4$."))

# C5 how each pricer's error shrinks (table)
C.append(item("c-error-rates", 3, ["nm-mc", "nm-fd", "nm-quadrature"], ["error-rates"], 180, "How each error shrinks",
    "One European call is priced three ways: Monte Carlo, an explicit finite-difference grid and Simpson's rule split at the strike.",
    "Fill in the factor by which each error is divided.",
    {"kind": "table", "columns": ["Change", "Error divided by"],
     "rows": [["Monte Carlo with four times the paths", {"edit": True, "answer": 2, "tol": {"abs": 0}, "wrong": [{"id": "mc-linear", "value": 4, "tol": {"abs": 0}}]}],
              ["Grid with $\\Delta S$ halved and $\\Delta\\tau$ quartered", {"edit": True, "answer": 4, "tol": {"abs": 0}, "wrong": [{"id": "fd-first-order", "value": 2, "tol": {"abs": 0}}]}],
              ["Simpson split at the strike, $h$ halved", {"edit": True, "answer": 16, "tol": {"abs": 0}, "wrong": [{"id": "simpson-unsplit", "value": 4, "tol": {"abs": 0}}]}]]},
    fb("2, 4 and 16.", "Recall each method's error rate, then put the change into it.",
       {"mc-linear": "You took Monte Carlo error as falling like $1/n$. It falls like $1/\\sqrt n$, so four times the paths halves it.",
        "fd-first-order": "You took the grid error as first order in $\\Delta S$. It is second order, and $\\Delta\\tau$ quartered keeps pace.",
        "simpson-unsplit": "You used the $h^2$ rate of an unsplit rule. Split at the strike, Simpson is $h^4$."}),
    "Four times the paths divides the error by $\\sqrt4 = 2$. Halving $\\Delta S$ and quartering $\\Delta\\tau$ divides both grid terms by 4. "
    "Halving $h$ divides Simpson's $h^4$ error by 16."))

# C6 the 2.5 exit task: one call, three pricers
P6c = (100, 105, 0.03, 0.25, 1.0)
bs6 = bs_call(P6c[0], P6c[1], P6c[2], P6c[3], P6c[4])
fd_sol = ("import math\nimport numpy as np\n\n\ndef fd_call(S0, K, r, sigma, T, M, N):\n    w = 5 * sigma * math.sqrt(T)\n"
          "    x = np.linspace(math.log(S0) - w, math.log(S0) + w, M + 1)\n    dx, dt = x[1] - x[0], T / N\n    nu = r - sigma ** 2 / 2\n"
          "    a = dt * (sigma ** 2 / (2 * dx ** 2) - nu / (2 * dx))\n    b = 1 - dt * (sigma ** 2 / dx ** 2 + r)\n"
          "    c = dt * (sigma ** 2 / (2 * dx ** 2) + nu / (2 * dx))\n    V = np.maximum(np.exp(x) - K, 0.0)\n    for n in range(1, N + 1):\n"
          "        V[1:-1] = a * V[:-2] + b * V[1:-1] + c * V[2:]\n        V[0], V[-1] = 0.0, math.exp(x[-1]) - K * math.exp(-r * n * dt)\n"
          "    return float(V[M // 2])\n")
quad_sol = ("import math\n\n\ndef quad_call(S0, K, r, sigma, T, n):\n    m, s = (r - sigma ** 2 / 2) * T, sigma * math.sqrt(T)\n"
            "    U = S0 * math.exp(m + 8 * s)\n    h = (U - K) / n          # the grid starts at the strike\n\n    def f(S):\n"
            "        z = (math.log(S / S0) - m) / s\n        return (S - K) * math.exp(-z * z / 2) / (math.sqrt(2 * math.pi) * S * s)\n\n"
            "    tot = f(K) + f(U)\n    for k in range(1, n):\n        tot += (4 if k % 2 else 2) * f(K + k * h)\n"
            "    return math.exp(-r * T) * tot * h / 3\n")
mc_sol = ("import numpy as np\n\n\ndef mc_cv_call(S0, K, r, sigma, T, n, seed):\n    z = np.random.default_rng(seed).standard_normal(n)\n"
          "    ST = S0 * np.exp((r - sigma ** 2 / 2) * T + sigma * np.sqrt(T) * z)\n    disc = np.exp(-r * T)\n    Y = disc * np.maximum(ST - K, 0.0)\n"
          "    # both controls less their known means\n"
          "    C = np.column_stack([disc * ST - S0, disc * ST ** 2 - S0 ** 2 * np.exp((r + sigma ** 2) * T)])\n"
          "    b = np.linalg.lstsq(C - C.mean(axis=0), Y - Y.mean(), rcond=None)[0]\n    adj = Y - C @ b\n"
          "    return float(adj.mean()), float(adj.std(ddof=1) / np.sqrt(n))\n")
fd_cases = ["fd_call(100, 105, 0.03, 0.25, 1.0, 200, 1000)", "fd_call(50, 45, 0.01, 0.4, 0.5, 160, 800)", "fd_call(100, 100, 0.05, 0.2, 2.0, 200, 1000)"]
fd_tests = [T(c, rep(run_solution(fd_sol, c)), tol={"abs": 1e-6}) for c in fd_cases]
quad_cases = [((100, 105, 0.03, 0.25, 1.0), 1000), ((50, 45, 0.01, 0.4, 0.5), 1000), ((80, 100, 0.02, 0.3, 0.25), 1000)]
quad_tests = [T("quad_call(%s, %s, %s, %s, %s, %d)" % (p + (n,)), rep(bs_call(*p)), tol={"abs": 1e-5}) for p, n in quad_cases]
bs6b = bs_call(50, 45, 0.01, 0.4, 0.5)
mc_setup1 = "res = mc_cv_call(100, 105, 0.03, 0.25, 1.0, 100000, 11)"
mc_setup2 = "res = mc_cv_call(50, 45, 0.01, 0.4, 0.5, 100000, 5)"
mc_setup3 = "r1 = mc_cv_call(100, 105, 0.03, 0.25, 1.0, 100000, 21); r4 = mc_cv_call(100, 105, 0.03, 0.25, 1.0, 400000, 22)"
# the plain Monte Carlo standard error, for the bound in test 2
_zp = np.random.default_rng(11).standard_normal(100000)
_Yp = math.exp(-0.03) * np.maximum(100 * np.exp((0.03 - 0.03125) + 0.25 * _zp) - 105, 0)
plain6 = float(_Yp.std(ddof=1) / math.sqrt(100000))
_Xp = math.exp(-0.03) * 100 * np.exp((0.03 - 0.03125) + 0.25 * _zp)
one6 = float((_Yp - np.cov(_Yp, _Xp)[0, 1] / np.var(_Xp, ddof=1) * (_Xp - 100)).std(ddof=1) / math.sqrt(100000))
mc_tests = [T("bool(abs(res[0] - %.6f) < 4 * res[1])" % bs6, "True", "equal", setup=mc_setup1),
            T("bool(res[1] < 0.016)", "True", "equal", setup=mc_setup1),
            T("bool(abs(res[0] - %.6f) < 4 * res[1])" % bs6b, "True", "equal", setup=mc_setup2),
            T("bool(0.4 < r4[1] / r1[1] < 0.6)", "True", "equal", setup=mc_setup3)]
mc_vals = [run_solution(mc_sol, t["call"], t["setup"]) for t in mc_tests]
assert all(mc_vals), mc_vals
C.append(parts("c-three-pricers", 5, ["nm-fd", "nm-quadrature", "nm-mc"], ["three-pricers"], 1800, "One call, three pricers",
    "We price a European call three ways and compare each with Black-Scholes. "
    "Write each function to the specification in its part.",
    [("Write `fd_call(S0, K, r, sigma, T, M, N)`, the explicit grid's value at `S0`.",
      {"kind": "code", "language": "python", "starter": "import math\nimport numpy as np\n\n\ndef fd_call(S0, K, r, sigma, T, M, N):\n    # M even: S0 sits on the middle node\n    ...\n",
       "solution": fd_sol, "examples": [ex(fd_tests[0])], "tests": fd_tests,
       "how": "Check runs 3 hidden tests, each within 1e-6 of the specified grid's value."},
      code_fb("The grid matches its specification.",
              {"test-1": "Test 1 is the base case. Update every interior node from the old values at once, then reset both ends.",
               "test-2": "Test 2 has $r = 0.01$ and $\\sigma = 0.4$. In log price the drift is $r - \\tfrac12\\sigma^2$, not $r$.",
               "test-3": "Test 3 runs two years. The upper boundary discounts $K$ by the time to expiry at each step."}),
      "Work in $x = \\ln S$ on $M + 1$ equally spaced nodes from $\\ln S_0 - 5\\sigma\\sqrt T$ to $\\ln S_0 + 5\\sigma\\sqrt T$, with $\\nu = r - \\tfrac12\\sigma^2$. "
      "Take $N$ steps of $\\Delta\\tau = T/N$ from the payoff, each setting $V_j \\leftarrow a V_{j-1} + bV_j + cV_{j+1}$ at every inner node from the old values. "
      "Here $a = \\Delta\\tau\\big(\\tfrac{\\sigma^2}{2\\Delta x^2} - \\tfrac{\\nu}{2\\Delta x}\\big)$, $b = 1 - \\Delta\\tau\\big(\\tfrac{\\sigma^2}{\\Delta x^2} + r\\big)$ and $c = \\Delta\\tau\\big(\\tfrac{\\sigma^2}{2\\Delta x^2} + \\tfrac{\\nu}{2\\Delta x}\\big)$. "
      "Then set $V_0 = 0$ and $V_M = e^{x_M} - Ke^{-r\\tau}$. Return the middle node, where $x = \\ln S_0$."),
     ("Write `quad_call(S0, K, r, sigma, T, n)`, Simpson's rule with `n` panels.",
      {"kind": "code", "language": "python", "cumulative": False, "starter": "import math\n\n\ndef quad_call(S0, K, r, sigma, T, n):\n    ...\n",
       "solution": quad_sol, "examples": [ex(quad_tests[0])], "tests": quad_tests,
       "how": "Check runs 3 hidden tests, each within 1e-5 of the Black-Scholes price."},
      code_fb("Split at the strike, Simpson matches Black-Scholes to five places.",
              {"test-1": "Test 1 is the base case. Start the grid at $K$, so the kink is on a node.",
               "test-3": "Test 3 is far out of the money. The density at $S$ carries a factor $1/(S\\sigma\\sqrt T)$."}),
      "Compute $e^{-rT}\\int_K^U (S - K)f(S)\\,dS$, with $U = S_0e^{(r - \\sigma^2/2)T + 8\\sigma\\sqrt T}$. "
      "Here $f$ is the lognormal density of $S_T$: $\\ln S_T$ is normal with mean $\\ln S_0 + (r - \\sigma^2/2)T$ and variance $\\sigma^2T$."),
     ("Write `mc_cv_call(S0, K, r, sigma, T, n, seed)`, returning `(price, standard_error)`.",
      {"kind": "code", "language": "python", "cumulative": False,
       "starter": "import numpy as np\n\n\ndef mc_cv_call(S0, K, r, sigma, T, n, seed):\n    # returns (price, standard_error)\n    ...\n",
       "solution": mc_sol, "examples": [{"setup": mc_tests[0]["setup"], "call": mc_tests[0]["call"], "expect": "True"}], "tests": mc_tests,
       "how": "Check runs 4 hidden tests. The price must lie within 4 standard errors of Black-Scholes. The error must be small, and halve with 4 times the paths."},
      code_fb("The two controls remove most of the variance.",
              {"test-1": "Test 1 compares with Black-Scholes. Subtract each control less its mean, times its coefficient, before you average.",
               "test-2": f"Test 2 asks for an error below 0.016. The share alone gives about {one6:.3f}, so use both controls in one least-squares fit.",
               "test-4": "Test 4 quadruples the paths. The standard error divides by $\\sqrt n$."}),
      "Draw with `np.random.default_rng(seed)`. Use two controls: $X_1 = e^{-rT}S_T$, with mean $S_0$, and $X_2 = e^{-rT}S_T^2$, with mean $S_0^2e^{(r + \\sigma^2)T}$. "
      "Take their coefficients from a least-squares fit of the discounted payoff on both.")],
    f"The grid's error is about $\\Delta\\tau + \\Delta x^2$, Simpson's split at the strike $h^4$, and Monte Carlo's $1/\\sqrt n$. "
    f"Black-Scholes gives {bs6:.4f} for the base case. Two controls cut the standard error from {plain6:.3f} to {run_solution(mc_sol, 'res[1]', mc_setup1):.3f}; the share alone gives {one6:.3f}."))
# C6 test 2's bound sits between the control-variate error and the plain one
assert run_solution(mc_sol, "res[1]", mc_setup1) < 0.016 < one6 < plain6

# C7 a mean-variance problem through KKT, by hand (parts)
mu7 = np.array([0.06, 0.10])
S7 = np.array([[0.0225, 0.0075], [0.0075, 0.0625]])
g7 = 2.5
K7 = np.block([[g7 * S7, np.ones((2, 1))], [np.ones((1, 2)), np.zeros((1, 1))]])
sol7 = np.linalg.solve(K7, np.append(mu7, 1))
w7, lam7 = sol7[:2], sol7[2]
un7 = np.linalg.solve(S7, mu7)
minv7 = (S7[1, 1] - S7[0, 1]) / (S7[0, 0] + S7[1, 1] - 2 * S7[0, 1])
C.append(parts("c-kkt-hand", 4, ["cv-qp"], ["kkt-mean-variance"], 300, "Two assets through the KKT conditions",
    "Two assets have expected returns 0.06 and 0.10, volatilities 0.15 and 0.25, and correlation 0.2. "
    "We maximise $\\boldsymbol\\mu^T\\mathbf w - 1.25\\,\\mathbf w^T\\boldsymbol\\Sigma\\mathbf w$ subject to $w_1 + w_2 = 1$. "
    "Stationarity reads $2.5\\boldsymbol\\Sigma\\mathbf w + \\lambda\\mathbf 1 = \\boldsymbol\\mu$.",
    [("What is $w_1$? Give 4 decimal places.",
      num(r(w7[0]), 0.0005, [("normalised", r(un7[0] / un7.sum()), 0.0005), ("min-variance", r(minv7), 0.0005)]),
      fb("Subtract the two stationarity rows to remove $\\lambda$.", "Subtract the rows, put $w_2 = 1 - w_1$, and solve one linear equation.",
         {"normalised": "You scaled the unconstrained weights to sum to 1. The budget changes the solution through $\\lambda$, not by rescaling.",
          "min-variance": "You found the minimum-variance weight. The objective also rewards return."})),
     ("What is the multiplier $\\lambda$? Give 4 decimal places.",
      num(r(lam7), 0.00005, [("sign", r(-lam7), 0.00005), ("unscaled", r(mu7[0] - (S7 @ w7)[0]), 0.00005)]),
      fb("$\\lambda$ is what the budget is worth at the margin.", "Put $\\mathbf w$ into either stationarity row.",
         {"sign": "You flipped the sign of $\\lambda$. With $\\lambda\\mathbf 1$ added on the left, $\\lambda = \\mu_1 - 2.5(\\boldsymbol\\Sigma\\mathbf w)_1$.",
          "unscaled": "You left out the 2.5 in front of $\\boldsymbol\\Sigma\\mathbf w$."}))],
    f"$\\boldsymbol\\Sigma$ has entries 0.0225, 0.0075 and 0.0625. Subtracting the rows gives $0.07w_1 = 0.039$, so $w_1 \\approx {w7[0]:.4f}$. "
    f"Then $\\lambda = 0.06 - 2.5(\\boldsymbol\\Sigma\\mathbf w)_1 \\approx {lam7:.4f}$."))

# C8 the KKT system in code, matched to a solver
kkt_sol = ("import numpy as np\n\n\ndef mv_weights(mu, cov, gamma):\n    mu, cov = np.asarray(mu, float), np.asarray(cov, float)\n    n = len(mu)\n"
           "    A = np.zeros((n + 1, n + 1))\n    A[:n, :n] = gamma * cov\n    A[:n, n] = 1.0      # the budget's multiplier\n    A[n, :n] = 1.0\n"
           "    return np.linalg.solve(A, np.append(mu, 1.0))[:n]\n")
mu8a = [0.05, 0.08, 0.11]
cov8a = [[0.04, 0.006, 0.002], [0.006, 0.09, 0.018], [0.002, 0.018, 0.16]]
mu8b = [0.03, 0.06, 0.07, 0.10]
cov8b = [[0.02, 0.004, 0.0, 0.003], [0.004, 0.05, 0.01, 0.0], [0.0, 0.01, 0.06, 0.012], [0.003, 0.0, 0.012, 0.12]]
kkt_cases = ["mv_weights(%r, %r, 3.0)" % (mu8a, cov8a), "mv_weights(%r, %r, 5.0)" % (mu8b, cov8b),
             "mv_weights([0.05, 0.09], [[0.0196, 0.0042], [0.0042, 0.0484]], 4.0)", "float(sum(mv_weights(%r, %r, 0.5)))" % (mu8b, cov8b)]
kkt_tests = [T(c, rep(run_solution(kkt_sol, c)), tol={"abs": 1e-8}) for c in kkt_cases]
C.append(item("c-kkt-code", 4, ["cv-qp", "cv-duality"], ["kkt-solve"], 600, "The KKT system in code",
    "For $n$ assets we maximise $\\boldsymbol\\mu^T\\mathbf w - \\tfrac{\\gamma}{2}\\mathbf w^T\\boldsymbol\\Sigma\\mathbf w$ subject to $\\mathbf 1^T\\mathbf w = 1$, with shorts allowed. "
    "The expected weights in the hidden tests come from SciPy's SLSQP.",
    "Write `mv_weights(mu, cov, gamma)`: solve the $(n + 1)$-equation KKT system for $\\mathbf w$ and $\\lambda$, and return $\\mathbf w$.",
    {"kind": "code", "language": "python", "starter": "import numpy as np\n\n\ndef mv_weights(mu, cov, gamma):\n    ...\n",
     "solution": kkt_sol, "examples": [ex(kkt_tests[2])], "tests": kkt_tests,
     "how": "Check runs 4 hidden tests at an absolute tolerance of 1e-8. Weights are compared entry by entry."},
    code_fb("One linear solve gives the solver's answer.",
            {"test-1": "Test 1 has three assets. Stack $\\gamma\\boldsymbol\\Sigma$ with a column of ones, and the budget row below.",
             "test-4": "Test 4 checks the weights sum to 1. Return $\\mathbf w$ alone, not $\\lambda$ as well."}),
    "Stationarity gives $n$ equations $\\gamma\\boldsymbol\\Sigma\\mathbf w + \\lambda\\mathbf 1 = \\boldsymbol\\mu$, and the budget one more. "
    "The objective is concave and the constraint affine, so the KKT point is the optimum. A solver such as SLSQP lands on the same weights."))

# C9 a dedication LP, its dual and a pricing-out test (parts)
L1_9, L2_9 = 80, 120
pA9, cpB9, pB9, pC9, cfC9 = 0.96, 0.05, 1.01, 0.95, 1.07
fB9 = L2_9 / (1 + cpB9)
fA9 = L1_9 - cpB9 * fB9
cost9 = pA9 * fA9 + pB9 * fB9
y1_9 = pA9
y2_9 = (pB9 - cpB9 * y1_9) / (1 + cpB9)
rc9 = pC9 - cfC9 * y2_9
C.append(parts("c-dedication-lp", 3, ["cv-lp", "cv-duality"], ["dedication-lp"], 240, "Buying bonds to meet two payments",
    "A scheme must pay £80,000 in one year and £120,000 in two. Bond A pays £1 in one year and costs 0.96. "
    "Bond B pays 0.05 in one year and 1.05 in two, and costs 1.01. "
    "In £ thousand, the plan solves: minimise $0.96a + 1.01b$ with $a + 0.05b \\ge 80$, $1.05b \\ge 120$ and $a, b \\ge 0$.",
    [("What is the cheapest cost, in £ thousand? Give 2 decimal places.",
      num(r(cost9, 4), 0.005, [("no-coupon", r(pA9 * L1_9 + pB9 * fB9, 4), 0.005)]),
      fb("B covers year two, and its coupon covers part of year one.", "Both constraints bind: solve $1.05b = 120$, then $a = 80 - 0.05b$.",
         {"no-coupon": "You bought 80 of A as well. B's coupon already pays part of the year-one bill."})),
     ("The duals are the discount factors the prices imply. A third bond pays 1.07 in two years only, and costs 0.95. What is its reduced cost, $0.95 - 1.07y_2$? Give 4 decimal places.",
      num(r(rc9), 0.00005, [("ignored-coupon", r(pC9 - cfC9 * pB9 / (1 + cpB9)), 0.00005), ("sign", r(-rc9), 0.00005)]),
      fb("Price the third bond with the duals, and compare with its cost.", "Make both bonds' reduced costs zero: $y_1 = 0.96$ and $0.05y_1 + 1.05y_2 = 1.01$.",
         {"ignored-coupon": "You divided B's price by 1.05. Part of that price pays for the year-one coupon, worth $0.05y_1$.",
          "sign": "You flipped the sign. The reduced cost is the bond's price less the value the duals give it."}))],
    f"$b = 120/1.05 \\approx {fB9:.4f}$ and $a = 80 - 0.05b \\approx {fA9:.4f}$, costing {cost9:.2f}. "
    f"The duals are $y_1 = 0.96$ and $y_2 = (1.01 - 0.048)/1.05 \\approx {y2_9:.4f}$. "
    f"The third bond's reduced cost is negative, so buying it would cut the cost."))

# C10 which functions are convex (multi, four keys)
C.append(item("c-convex-functions", 2, ["cv-convex"], ["convex-functions"], 120, "Risk measures that are convex",
    "Here $\\mathbf w$ is a portfolio, $\\boldsymbol\\Sigma$ a covariance matrix and $\\mathbf r_s$ the asset returns in scenario $s$.",
    "Which functions are convex? Select all that apply.",
    choice([opt("a", "$\\mathbf w^T\\boldsymbol\\Sigma\\mathbf w$, the portfolio variance", correct=True),
            opt("b", "$\\sqrt{\\mathbf w^T\\boldsymbol\\Sigma\\mathbf w}$, the portfolio volatility", correct=True),
            opt("c", "$\\max_s(-\\mathbf r_s^T\\mathbf w)$, the worst loss over five scenarios", correct=True),
            opt("d", "$-\\ln x$ for $x > 0$, a log-utility loss", correct=True),
            opt("e", "$\\boldsymbol\\mu^T\\mathbf w/\\sqrt{\\mathbf w^T\\boldsymbol\\Sigma\\mathbf w}$, the Sharpe ratio",
                "You took the Sharpe ratio as convex. A ratio of a linear function and a norm is not."),
            opt("f", "$x^3$ on the whole real line, a cubic penalty",
                "You took $x^3$ as convex everywhere. Its second derivative $6x$ is negative for $x < 0$.")], kind="multi"),
    fb("Four of the six are convex.", "Use the rules: a positive semidefinite quadratic, a norm, a maximum of affine maps."),
    "The variance has a positive semidefinite Hessian, and the volatility is a norm. A maximum of linear functions is convex, and $-\\ln x$ has second derivative $1/x^2 > 0$. "
    "The Sharpe ratio and $x^3$ are not."))

# C11 one projected gradient step on the simplex
w11c = np.array([0.6, 0.3, 0.1])
g11 = np.array([0.2, -0.6, 0.5])
v11 = w11c - 0.5 * g11


def proj_simplex(v):
    u = np.sort(v)[::-1]
    cs = np.cumsum(u)
    k = max(j for j in range(1, len(v) + 1) if u[j - 1] - (cs[j - 1] - 1) / j > 0)
    th = (cs[k - 1] - 1) / k
    return np.maximum(v - th, 0), th


p11, th11 = proj_simplex(v11)
C.append(item("c-projected-step", 3, ["cv-descent"], ["projected-gradient"], 240, "A step that leaves the simplex",
    "A long-only, fully invested book has weights $(0.6, 0.3, 0.1)$. The gradient of its loss is $(0.2, -0.6, 0.5)$. "
    "Projected gradient descent steps by 0.5, then projects onto $\\{\\mathbf w \\ge 0, \\sum w_i = 1\\}$. "
    "The projection is $w_i = \\max(v_i - \\theta, 0)$, with one $\\theta$ chosen so the weights sum to 1.",
    "What is the new weight of the first asset?",
    num(r(p11[0]), 0.0005, [("renormalise", r(max(v11[0], 0) / np.maximum(v11, 0).sum()), 0.0002),
                            ("shift-all", r(v11[0] - (v11.sum() - 1) / 3), 0.0005), ("no-projection", r(v11[0]), 0.0005)]),
    fb("The third weight hits zero, so only two share the shift.", "Step to $\\mathbf v = \\mathbf w - 0.5\\mathbf g$, then find $\\theta$ with the negative entry set to zero.",
       {"renormalise": "You clipped at zero and rescaled. The Euclidean projection shifts by $\\theta$; it does not rescale.",
        "shift-all": "You shifted all three entries equally. The third would stay negative, so it is set to zero first.",
        "no-projection": "You stopped after the step. The weights must be projected back onto the simplex."}),
    f"The step gives $\\mathbf v = (0.5, 0.6, -0.15)$. With the third weight at zero, $(0.5 - \\theta) + (0.6 - \\theta) = 1$ gives $\\theta = {th11:.2f}$. "
    f"So the weights are $({p11[0]:.2f}, {p11[1]:.2f}, 0)$."))

# ======================================================================== Paper D: backtesting, alpha, options and contests
# D1 a Sortino ratio from six months
r1d = np.array([0.021, -0.012, 0.008, -0.025, 0.015, 0.006])
dd1 = math.sqrt(float(np.mean(np.minimum(r1d, 0) ** 2)))
so1 = r1d.mean() / dd1 * math.sqrt(12)
sh1 = r1d.mean() / r1d.std(ddof=1) * math.sqrt(12)
dd1b = math.sqrt(float(np.sum(np.minimum(r1d, 0) ** 2)) / 2)
D.append(item("d-sortino", 3, ["bt-metrics"], ["sortino"], 180, "A Sortino ratio from six months",
    "A backtest's monthly excess returns are $0.021, -0.012, 0.008, -0.025, 0.015$ and $0.006$. "
    "Its downside deviation is $\\sqrt{\\tfrac1n\\sum\\min(r_t, 0)^2}$, over all six months.",
    "What is the annualised Sortino ratio, the mean over the downside deviation times $\\sqrt{12}$? Give 3 decimal places.",
    num(r(so1, 5), 0.0005, [("sharpe", r(sh1, 5), 0.0005), ("losing-months-only", r(r1d.mean() / dd1b * math.sqrt(12), 5), 0.0005),
                            ("monthly", r(so1 / math.sqrt(12), 5), 0.0005)]),
    fb("Only the losing months enter the downside deviation, but all six count in $n$.", "Square the two losses, divide by 6, take the root, then form the ratio.",
       {"sharpe": "You used the full standard deviation. Sortino penalises only the losing months.",
        "losing-months-only": "You divided by 2, the losing months. The formula divides by all six.",
        "monthly": "You left the ratio monthly. Multiply by $\\sqrt{12}$."}),
    f"The mean is {r1d.mean():.6f}. The downside deviation is $\\sqrt{{(0.000144 + 0.000625)/6}} \\approx {dd1:.5f}$. "
    f"So the Sortino ratio is ${r1d.mean():.6f}/{dd1:.5f} \\times \\sqrt{{12}} \\approx {so1:.3f}$."))

# D2 a participation schedule's average fill
vol2 = [120_000, 80_000, 200_000, 150_000, 90_000]
px2 = [50.10, 50.20, 50.05, 50.30, 50.40]
left2, fills2 = 60_000, []
for v in vol2:
    q = min(0.1 * v, left2)
    fills2.append(q)
    left2 -= q
avg2 = sum(q * p for q, p in zip(fills2, px2)) / 60_000
full5 = fills2[:4] + [9_000]
avg2f = sum(q * p for q, p in zip(full5, px2)) / sum(full5)
D.append(item("d-participation-fill", 3, ["bt-execution"], ["participation-fill"], 180, "Filling at 10% of the volume",
    "An engine buys 60,000 shares at 10% of each bar's volume, filling at the bar's average price. "
    "The bars trade 120,000, 80,000, 200,000, 150,000 and 90,000 shares at average prices £50.10, £50.20, £50.05, £50.30 and £50.40.",
    "What is the order's average fill price, in pounds? Give 4 decimal places.",
    num(r(avg2, 6), 0.00005, [("mean-price", r(sum(px2) / 5, 6), 0.00005), ("full-last-bar", r(avg2f, 6), 0.00005)], unit="£"),
    fb("The last bar fills only the 5,000 shares left.", "Fill 10% of each bar until 60,000 is reached, then weight each price by its fill.",
       {"mean-price": "You averaged the five prices. Weight each by the shares filled in that bar.",
        "full-last-bar": "You filled 9,000 in the last bar. Only 5,000 shares were left to buy."}),
    f"The fills are 12,000, 8,000, 20,000, 15,000 and then the last 5,000. They cost £{sum(q * p for q, p in zip(fills2, px2)):,.0f} in all. "
    f"So the average price is £{avg2:.4f}."))

# D3 survivorship in a universe
D.append(item("d-survivors", 2, ["bt-bias"], ["survivorship"], 90, "The names that disappeared",
    "A universe began a year with 500 shares. The 400 that still trade today returned 9% on average. "
    "The 100 delisted during the year returned $-30\\%$ on average.",
    "What was the equal-weighted return of the whole starting universe, as a decimal?",
    num(r((400 * 0.09 + 100 * -0.30) / 500, 6), 0.0005, [("survivors", 0.09, 0.0005), ("plain-mean", r((0.09 - 0.30) / 2, 6), 0.0005)]),
    fb("Weight each group by its count.", "Average over all 500 starting names, the delisted ones included.",
       {"survivors": "You used today's survivors only. That is the survivorship bias the question is about.",
        "plain-mean": "You averaged the two group means. The groups have 400 and 100 names."}),
    "The universe made $(400 \\times 0.09 + 100 \\times (-0.30))/500 = 0.012$. "
    "A backtest on today's survivors would show 0.09, a bias of 7.8 percentage points."))

# D4 where the held-out period sits
D.append(item("d-held-out", 3, ["bt-design"], ["held-out-period"], 120, "Where to hold data back",
    "An engine has daily data from 2012 to 2025. You will tune rules, costs and sizes before reporting.",
    "Where should the held-out period sit?",
    choice([opt("a", "The last two years, untouched until every choice is fixed, then run once.", correct=True),
            opt("b", "Two years of days drawn at random from across the whole sample, so every regime appears.",
                "You drew days at random. Neighbouring days then sit on both sides, so the test leaks."),
            opt("c", "The first two years, so the rules are tuned on the most recent data.",
                "You held out the start. The test then sits before the training data, which no live trade can."),
            opt("d", "The two worst years, so the strategy is tested under stress.",
                "You chose the years by their outcome. That selection is itself a look at the test data.")]),
    fb("The held-out block comes last in time and is used once.", "Ask which choice matches what live trading will face."),
    "Live trading always meets data after everything it was tuned on. "
    "A final block, run once after every decision is made, copies that. Random or chosen years leak or select."))

# D5 an interval for a Sharpe ratio
sr5, T5 = 0.35, 60
se5 = math.sqrt((1 + sr5 ** 2 / 2) / T5)
lo5 = (sr5 - 1.96 * se5) * math.sqrt(12)
D.append(item("d-sharpe-interval", 4, ["bt-report"], ["sharpe-interval"], 240, "How low could the Sharpe be",
    "A backtest has a monthly Sharpe ratio of 0.35 over 60 months. For roughly normal returns, "
    "its standard error is $\\sqrt{(1 + \\widehat{SR}^2/2)/T}$.",
    "What is the lower end of a 95% interval for the annualised Sharpe ratio? Give 3 decimal places.",
    num(r(lo5, 5), 0.002, [("monthly", r(sr5 - 1.96 * se5, 5), 0.002), ("point", r(sr5 * math.sqrt(12), 5), 0.002)]),
    fb("Build the interval monthly, then scale by $\\sqrt{12}$.", "Find the standard error, subtract 1.96 of them from 0.35, then annualise.",
       {"monthly": "You stopped at the monthly figure. Multiply by $\\sqrt{12}$.",
        "point": "You annualised the point estimate. The question asks for the interval's lower end."}),
    f"The standard error is $\\sqrt{{1.06125/60}} \\approx {se5:.4f}$. The monthly lower end is $0.35 - 1.96 \\times {se5:.4f} \\approx {sr5 - 1.96 * se5:.4f}$. "
    f"Annualised, that is {lo5:.3f}, against a point estimate of {sr5 * math.sqrt(12):.2f}."))

# D6 a universe chosen at the end
D.append(item("d-universe-date", 3, ["al-universe"], ["universe-look-ahead"], 120, "A universe picked at the end",
    "A momentum study takes the 300 largest shares by market value on 31 December 2024. It backtests them from 2015 to 2024.",
    "What is wrong with this universe?",
    choice([opt("a", "It uses end-of-sample values, so it keeps firms that grew and drops those that failed.", correct=True),
            opt("b", "Nothing: the 300 largest shares are liquid in every year, so costs stay small.",
                "You checked only liquidity. The list uses 2024 values to choose shares for 2015."),
            opt("c", "It only biases the short side, where the shares that later fell are missing.",
                "You limited the bias to shorts. Winners that grew into the list lift the long side too."),
            opt("d", "It biases returns down, because the large firms of 2024 grow more slowly than small ones.",
                "You expected a downward bias. Firms that are large in 2024 are mostly ones that rose.")]),
    fb("Rank the universe at each date with data known then.", "Ask what a 2015 investor could have known about the 2024 list."),
    "Market value at the end of 2024 rewards shares that rose over the test. So the universe is chosen with future data. "
    "Rank it each month from that month's values instead."))

# D7 cross-sectional reversal weights
r7 = np.array([0.05, -0.02, 0.01, -0.04, 0.03])
s7 = -(r7 - r7.mean())
w7d = s7 / np.abs(s7).sum()
D.append(item("d-reversal-weights", 3, ["al-signal", "al-portfolio"], ["reversal-weights"], 150, "A short-term reversal book",
    "Five shares returned $0.05, -0.02, 0.01, -0.04$ and $0.03$ last week. "
    "The signal is minus each return less the cross-sectional mean. Weights are the signals scaled so absolute weights sum to 1.",
    "What weight does the share that returned $-0.04$ get? Give 4 decimal places.",
    num(r(w7d[3]), 0.0005, [("no-demean", r(0.04 / np.abs(r7).sum()), 0.0005), ("momentum", r(-w7d[3]), 0.0005)]),
    fb("Demean, flip the sign, then scale.", "Subtract the mean 0.006 from each return, negate, then divide by the sum of absolute values.",
       {"no-demean": "You skipped the demeaning. The book is dollar-neutral only after the mean is taken out.",
        "momentum": "You kept the sign of the return. Reversal buys last week's losers."}),
    f"After demeaning, the share's return is $-0.046$, so its signal is $0.046$. The absolute signals sum to {np.abs(s7).sum():.3f}. "
    f"Its weight is $0.046/{np.abs(s7).sum():.3f} \\approx {w7d[3]:.4f}$."))

# D8 the IC that a target information ratio needs, by the fundamental law
n8, k8, tc8, ir_t8 = 250, 52, 0.4, 0.8
br8 = n8 * k8
ic8 = ir_t8 / (tc8 * math.sqrt(br8))
D.append(item("d-fundamental-law", 3, ["al-ic"], ["fundamental-law"], 150, "What IC a target needs",
    "A book trades 250 shares and rebalances weekly, 52 times a year. Constraints give a transfer coefficient of 0.4. "
    "The fundamental law says $IR = TC \\cdot IC\\sqrt{\\text{breadth}}$.",
    "What information coefficient does an annual information ratio of 0.8 need? Give 4 decimal places.",
    num(r(ic8, 6), 0.00005, [("no-tc", r(ir_t8 / math.sqrt(br8), 6), 0.00005), ("tc-multiplied", r(ir_t8 * tc8 / math.sqrt(br8), 6), 0.00005),
                             ("one-rebalance", r(ir_t8 / (tc8 * math.sqrt(n8)), 6), 0.00005)]),
    fb("Breadth is the number of independent bets a year: 13,000.", "Multiply 250 shares by 52 rebalances for the breadth, then solve the law for the IC.",
       {"no-tc": "You left out the transfer coefficient. Constraints keep only 40% of the signal, so the IC must be higher.",
        "tc-multiplied": "You multiplied by the transfer coefficient. It sits under the IC in the law, so divide by it.",
        "one-rebalance": "You used 250 for the breadth. A year holds 52 rebalances."}),
    f"Breadth is $250 \\times 52 = {br8}$, with $\\sqrt{{{br8}}} \\approx {math.sqrt(br8):.2f}$. So $IC = 0.8/(0.4 \\times {math.sqrt(br8):.2f}) \\approx {ic8:.4f}$."))

# D9 a Sharpe ratio after costs
cost9d = 12 * 0.40 * 0.0012
net9 = (0.09 - cost9d) / 0.06
D.append(item("d-net-sharpe", 3, ["al-costs"], ["net-sharpe"], 150, "What costs leave of a Sharpe",
    "A long-short book makes 9% a year gross on its gross value, with volatility 6%. "
    "Each month it trades 40% of its gross value, at 12 basis points of the value traded.",
    "What is its Sharpe ratio after costs? Give 3 decimal places.",
    num(r(net9, 5), 0.0005, [("one-month", r((0.09 - 0.40 * 0.0012) / 0.06, 5), 0.0005), ("gross", 1.5, 0.0005)]),
    fb("Annual cost is $12 \\times 0.40 \\times 0.0012$.", "Find the yearly cost drag, subtract it from 9%, then divide by 6%.",
       {"one-month": "You charged one month of trading. Costs come every month.",
        "gross": "You left costs out. That is the gross Sharpe ratio."}),
    f"Costs take $12 \\times 0.40 \\times 0.0012 = {cost9d:.5f}$ a year. The net return is ${0.09 - cost9d:.5f}$. "
    f"Divided by 0.06, the Sharpe ratio is {net9:.3f}, against 1.5 gross."))

# D10 the alpha project's report line: rank IC and turnover from a panel file
sr_sol = ("import numpy as np\nimport pandas as pd\n\n\ndef ic_and_turnover(df):\n    ics, ws = [], []\n"
          "    for _, g in df.sort_values(['date', 'ticker']).groupby('date'):\n        rs = g['signal'].rank().to_numpy()\n"
          "        ics.append(np.corrcoef(rs, g['fwd_ret'].rank().to_numpy())[0, 1])\n        w = rs - rs.mean()\n"
          "        ws.append(w / np.abs(w).sum())\n    turns = [0.5 * np.abs(ws[k] - ws[k - 1]).sum() for k in range(1, len(ws))]\n"
          "    return float(np.mean(ics)), float(np.mean(turns))\n")
sr_setup = "import pandas as pd; df = pd.read_csv('signal-panel.csv')"
sr_hand = ("import pandas as pd; df = pd.DataFrame({'date': ['d1'] * 4 + ['d2'] * 4 + ['d3'] * 4, 'ticker': list('ABCD') * 3, "
           "'signal': [0.2, -0.1, 0.5, 0.0, 0.3, 0.1, -0.2, 0.4, -0.3, 0.6, 0.1, 0.2], "
           "'fwd_ret': [0.01, -0.02, 0.03, 0.0, -0.01, 0.02, 0.01, 0.04, 0.0, 0.02, -0.03, 0.01]})")
sr_cases = [(sr_setup, "ic_and_turnover(df)[0]"), (sr_setup, "ic_and_turnover(df)[1]"),
            (sr_setup, "ic_and_turnover(df[df['date'] <= sorted(df['date'].unique())[9]])[0]"),
            (sr_hand, "ic_and_turnover(df)[0]"), (sr_hand, "ic_and_turnover(df)[1]")]
sr_tests = [T(c, rep(run_solution(sr_sol, c, s)), setup=s, tol={"rel": 1e-9}) for s, c in sr_cases]
sr_vals = [float(t["expect"]) for t in sr_tests]
D.append(item("d-signal-report", 5, ["al-ic", "al-portfolio", "al-costs"], ["ic-turnover"], 1200, "An IC and a turnover from a panel",
    "`signal-panel.csv` holds 20 weekly dates for the same 30 tickers: each share's `signal` and its next-week return `fwd_ret`. "
    "On each date the IC is the Spearman correlation of `signal` with `fwd_ret`. "
    "The weights are each share's signal rank less the mean rank, scaled so absolute weights sum to 1. "
    "Turnover is the mean, over consecutive dates, of half the sum of absolute weight changes. "
    "`Series.corr(method='spearman')` needs SciPy; import it, or correlate the ranks.",
    "Write `ic_and_turnover(df)` returning `(mean_ic, turnover)`.",
    {"kind": "code", "language": "python", "data": {"signal-panel.csv": DATA_REL + "signal-panel.csv"},
     "starter": "# keep these imports: the tests load the file with pandas\nimport numpy as np\nimport pandas as pd\n\n\ndef ic_and_turnover(df):\n    # returns (mean_ic, turnover)\n    ...\n",
     "solution": sr_sol, "examples": [ex(sr_tests[0])], "tests": sr_tests,
     "how": "Check runs 5 hidden tests at a relative tolerance of 1e-9. Tests 1 to 3 read the file; tests 4 and 5 use four tickers on three dates."},
    code_fb("The IC and the turnover match.",
            {"test-1": "Test 1 is the mean IC. Correlate ranks, not raw values, on each date, then average over dates.",
             "test-2": "Test 2 is turnover. Align tickers between dates and halve the sum of absolute changes.",
             "test-5": "Test 5 has three dates, so two changes. Average over date pairs, not over dates."}),
    f"On the file the mean IC is about {sr_vals[0]:.4f} and the turnover about {sr_vals[1]:.4f} a week. "
    "Turnover times the cost per trade is the drag the results note must subtract. "
    "A persistent signal trades less, which is why its net Sharpe holds up."))

# D11 the gamma part of a hedged option's P&L
S11, K11, r11, s11, T11, dS11 = 80, 84, 0.03, 0.32, 0.4, 3
d1_11 = (math.log(S11 / K11) + (r11 + s11 ** 2 / 2) * T11) / (s11 * math.sqrt(T11))
gam11 = phi(d1_11) / (S11 * s11 * math.sqrt(T11))
pnl11 = 0.5 * gam11 * dS11 ** 2
D.append(item("d-gamma-pnl", 3, ["od-greeks"], ["gamma-pnl"], 180, "A hedged call on a £3 move",
    "You hold one call with $S = 80$, $K = 84$, $r = 0.03$, $\\sigma = 0.32$ and $T = 0.4$, delta-hedged with shares. The share jumps £3.",
    "Ignoring time decay, what does the hedged position make, $\\tfrac12\\Gamma(\\Delta S)^2$? Give 4 decimal places.",
    num(r(pnl11), 0.0005, [("no-half", r(2 * pnl11), 0.0005), ("not-squared", r(0.5 * gam11 * dS11), 0.0005)], unit="£"),
    fb("Gamma times half the squared move.", "Find $d_1$, then $\\Gamma = \\varphi(d_1)/(S\\sigma\\sqrt T)$.",
       {"no-half": "You left out the $\\tfrac12$ of the second-order term.",
        "not-squared": "You multiplied by the move, not its square."}),
    f"$d_1 \\approx {d1_11:.4f}$, so $\\Gamma = {phi(d1_11):.4f}/(80 \\times 0.32 \\times \\sqrt{{0.4}}) \\approx {gam11:.5f}$. "
    f"The hedged position makes about $\\tfrac12 \\times {gam11:.5f} \\times 9 \\approx {pnl11:.4f}$."))

# D12 a negative butterfly in a quoted chain
bf12 = (12.45 - 2 * 8.35 + 4.10) / 25
D.append(item("d-butterfly-density", 4, ["od-surface", "od-data"], ["butterfly-density"], 240, "A chain that pays you to hold it",
    "Calls on one expiry have mid prices 12.45, 8.35 and 4.10 at strikes 90, 95 and 100.",
    "What is the finite-difference density estimate $(C_{90} - 2C_{95} + C_{100})/5^2$?",
    num(r(bf12, 6), 0.00005, [("sign", r(-bf12, 6), 0.00005), ("no-square", r(bf12 * 5, 6), 0.00005)]),
    fb("A negative density is an arbitrage: clean such quotes before fitting the surface.", "Combine the three prices, then divide by the square of the strike gap.",
       {"sign": "You reversed the combination. It is the outer prices less twice the middle one.",
        "no-square": "You divided by 5. The second difference divides by $5^2$."}),
    f"$12.45 - 16.70 + 4.10 = -0.15$, and $-0.15/25 = {r(bf12, 6)}$. "
    "A butterfly never pays less than zero at expiry. So buying the wings and selling two middles locks in a gain."))

# D13 the forward and discount factor from a chain, by least squares on put-call parity
pf_sol = ("import math\nimport numpy as np\n\n\ndef parity_fit(strikes, calls, puts):\n    K, C, P = (np.asarray(v, float) for v in (strikes, calls, puts))\n"
          "    ok = ~(np.isnan(C) | np.isnan(P))\n    if ok.sum() < 2:\n        raise ValueError('need two strikes with both prices')\n"
          "    A = np.column_stack([np.ones(ok.sum()), -K[ok]])   # C - P = D*F - D*K\n    a, D = np.linalg.lstsq(A, (C - P)[ok], rcond=None)[0]\n"
          "    return float(D), float(a / D)\n")
K13 = [90, 95, 100, 105, 110, 115]
_S, _r, _q, _T = 100.0, 0.03, 0.015, 0.5


def _cq(K, s_):
    d1 = (math.log(_S / K) + (_r - _q + s_ * s_ / 2) * _T) / (s_ * math.sqrt(_T))
    return _S * math.exp(-_q * _T) * Phi(d1) - K * math.exp(-_r * _T) * Phi(d1 - s_ * math.sqrt(_T))


_vols = [0.26 - 0.004 * (k - 90) / 5 * 2 for k in K13]   # a gentle skew
C13 = [round(_cq(k, v), 2) for k, v in zip(K13, _vols)]
P13 = [round(_cq(k, v) - _S * math.exp(-_q * _T) + k * math.exp(-_r * _T), 2) for k, v in zip(K13, _vols)]
pf_cases = ["parity_fit(%r, %r, %r)[0]" % (K13, C13, P13), "parity_fit(%r, %r, %r)[1]" % (K13, C13, P13),
            "parity_fit(%r, %r, %r)[1]" % (K13, C13[:2] + [float('nan')] + C13[3:], P13),
            "parity_fit([100, 110], [6.0, 1.5], [4.0, 9.4])[1]"]
pf_tests = [T(c.replace('nan', "float('nan')"), rep(run_solution(pf_sol, c.replace('nan', "float('nan')"))), tol={"rel": 1e-9}) for c in pf_cases]
pf_tests += [{"call": "parity_fit([100, 105], [8.36, float('nan')], [6.11, 8.38])", "expect": "ValueError", "compare": "raises"}]
pf_D, pf_F = (float(pf_tests[0]["expect"]), float(pf_tests[1]["expect"]))
D.append(item("d-parity-fit", 4, ["od-data", "od-pricers"], ["parity-forward"], 900, "The forward a chain implies",
    "Put-call parity says $C - P = D(F - K)$ at every strike, where $D$ is the discount factor and $F$ the forward. "
    "Quotes are noisy, so we fit both by least squares across strikes. A strike missing either price is skipped.",
    "Write `parity_fit(strikes, calls, puts)` returning `(D, F)`. Raise `ValueError` with fewer than two usable strikes.",
    {"kind": "code", "language": "python", "starter": "import math\nimport numpy as np\n\n\ndef parity_fit(strikes, calls, puts):\n    ...\n",
     "solution": pf_sol, "examples": [ex(pf_tests[3])], "tests": pf_tests,
     "how": "Check runs 5 hidden tests at a relative tolerance of 1e-9. Test 3 has a missing call; test 5 expects a ValueError."},
    code_fb("One straight line through $C - P$ against $K$ gives both numbers.",
            {"test-1": "Test 1 is the discount factor: minus the slope of $C - P$ against $K$.",
             "test-2": "Test 2 is the forward: the intercept divided by $D$, not the intercept itself.",
             "test-3": "Test 3 has a NaN call. Drop that strike before you fit.",
             "test-5": "Test 5 leaves one usable strike. Raise `ValueError` rather than fit a line through one point."}),
    f"Regressing $C - P$ on $K$ gives slope $-D$ and intercept $DF$. On the six quotes $D \\approx {pf_D:.4f}$ and $F \\approx {pf_F:.2f}$. "
    "Every implied volatility on the dashboard then prices against this forward, not the spot."))

# D13b an at-the-money implied volatility in the head
c13b, F13b, T13b = 9.80, 250, 0.25
sig13b = c13b * math.sqrt(2 * math.pi) / (F13b * math.sqrt(T13b))
D.append(item("d-atm-vol", 2, ["od-iv"], ["atm-vol-approx"], 90, "A volatility from one quote",
    "An at-the-money-forward call, undiscounted, is worth about $F\\sigma\\sqrt T/\\sqrt{2\\pi}$. "
    "A three-month call with $F = K = 250$ is quoted at 9.80.",
    "What implied volatility does the approximation give? Give 4 decimal places.",
    num(r(sig13b, 6), 0.0005, [("no-root-t", r(c13b * math.sqrt(2 * math.pi) / F13b, 6), 0.0005), ("inverted", r(c13b / (math.sqrt(2 * math.pi) * F13b * math.sqrt(T13b)), 6), 0.0005)]),
    fb("$\\sigma \\approx \\sqrt{2\\pi}\\,C/(F\\sqrt T)$.", "Solve the approximation for $\\sigma$, with $\\sqrt T = 0.5$.",
       {"no-root-t": "You left out $\\sqrt T$. Three months gives $\\sqrt{0.25} = 0.5$.",
        "inverted": "You divided by $\\sqrt{2\\pi}$ instead of multiplying. $1/\\sqrt{2\\pi} \\approx 0.4$ sits in the price, so the volatility gets $\\sqrt{2\\pi}$."}),
    f"$\\sigma \\approx 9.80 \\times 2.5066/(250 \\times 0.5) \\approx {sig13b:.4f}$. "
    "The rule of thumb is $C \\approx 0.4F\\sigma\\sqrt T$, close to exact at the money."))

# D14 inclusion and exclusion
cnt14 = 10 ** 6 // 6 + 10 ** 6 // 14 - 10 ** 6 // 42
D.append(item("d-audit-ids", 3, ["cn-maths"], ["inclusion-exclusion"], 150, "Trades picked for an audit",
    "Trades have ids 1 to 1,000,000. An audit takes every id divisible by 6 or by 14.",
    "How many trades does it take?",
    num(cnt14, 0, [("no-overlap", 10 ** 6 // 6 + 10 ** 6 // 14, 0), ("product", 10 ** 6 // 6 + 10 ** 6 // 14 - 10 ** 6 // 84, 0)]),
    fb("Add both counts, then remove those counted twice.", "Ids divisible by both are the multiples of the least common multiple, 42.",
       {"no-overlap": "You counted the multiples of 42 twice. Subtract them once.",
        "product": "You removed multiples of 84, the product. The overlap is the multiples of 42."}),
    f"There are 166,666 multiples of 6 and 71,428 of 14. Both hold for the 23,809 multiples of 42. So the audit takes {cnt14:,} trades."))

# D15 subarrays with a given sum
a15 = [2, -1, 3, 1, -2, 2, 1, -3, 3]
cnt15 = sum(1 for i in range(9) for j in range(i + 1, 10) if sum(a15[i:j]) == 3)
D.append(item("d-sum-runs", 3, ["cn-patterns"], ["prefix-sum-count"], 180, "Runs of days that sum to 3",
    "A desk's daily P&L, in £ thousand, is $2, -1, 3, 1, -2, 2, 1, -3, 3$.",
    "How many runs of consecutive days sum to exactly 3?",
    num(cnt15, 0, [("window", 2, 0), ("singles-missed", 6, 0)]),
    fb("Count pairs of prefix sums that differ by 3.", "Keep a count of each prefix sum seen; at each day add the count of the prefix sum less 3.",
       {"window": "You used a sliding window. It needs non-negative values; losses break it.",
        "singles-missed": "You left out single days. The two days with P&L 3 count as runs too."}),
    f"The prefix sums are 0, 2, 1, 4, 5, 3, 5, 6, 3, 6. Pairs that differ by 3 number {cnt15}. "
    "A hash map of prefix-sum counts finds them in one pass."))

# D16 reading the constraints
D.append(item("d-constraints", 2, ["cn-reading", "cn-impl"], ["constraints-read"], 90, "Reading the limits",
    "A problem has $n \\le 200{,}000$ and a time limit of 1 second. A judge runs about $10^8$ simple steps a second.",
    "Which approach fits?",
    choice([opt("a", "Sort once, then one sweep: $O(n \\log n)$, a few million steps.", correct=True),
            opt("b", "Compare every pair: $O(n^2)$, about $4 \\times 10^{10}$ steps.",
                "You chose all pairs. At $10^8$ steps a second that takes minutes."),
            opt("c", "Every pair, with a sorted search inside: $O(n^2 \\log n)$ steps.",
                "You added a log factor to all pairs. That is slower still than $O(n^2)$."),
            opt("d", "Try every subset of the input: $O(2^n)$ steps in the worst case.",
                "You chose every subset. That is hopeless past $n$ of about 25.")]),
    fb("$n \\log n$ is about $3.5 \\times 10^6$.", "Put $n = 200{,}000$ into each cost and compare with $10^8$."),
    "$200{,}000 \\log_2 200{,}000$ is about $3.5 \\times 10^6$, well inside a second. "
    "$O(n^2)$ is $4 \\times 10^{10}$, four hundred seconds."))

# D17 the odds the rating model gives a contest pairing
e17 = 1 / (1 + 10 ** ((1600 - 1400) / 400))
D.append(item("d-rating-odds", 2, ["cn-strategy"], ["rating-odds"], 90, "Your odds against a stronger field",
    "Codeforces-style ratings expect a player rated $R_A$ to beat one rated $R_B$ with probability $1/(1 + 10^{(R_B - R_A)/400})$. "
    "You are rated 1400.",
    "What chance does the model give you against a player rated 1600? Give 4 decimal places.",
    num(r(e17), 0.0005, [("flipped", r(1 - e17), 0.0005), ("natural-base", r(1 / (1 + math.exp(0.5))), 0.0005)]),
    fb("A 200-point gap gives the stronger player about three chances in four.", "Put $R_B - R_A = 200$ into the formula, so the power is $10^{0.5}$.",
       {"flipped": "You gave the stronger player's chance. Yours is one minus it.",
        "natural-base": "You used $e^{0.5}$. The rating formula uses powers of 10."}),
    f"$10^{{200/400}} = \\sqrt{{10}} \\approx 3.1623$, so your chance is $1/4.1623 \\approx {e17:.4f}$. "
    "Beating such players often is how the rating climbs past 1400."))

# ======================================================================== the exam document
CHECKS = [
    ("tabular-project", "One tabular prediction problem, done end to end with time-ordered cross-validation",
     "In your own repository: the data, the features, walk-forward folds with a purge, the model and a held-out final block. Add a short note on what failed."),
    ("explain-aloud", "You explain leakage, regularisation and the bias-variance trade-off aloud, without notes",
     "Two minutes on each to a friend or a recording, with one example from your own project."),
    ("project-backtest", "Backtesting engine: README, tests and a one-page results note",
     "Transaction costs, slippage, a look-ahead check and a held-out period. The note reports Sharpe, Calmar and maximum drawdown, and what failed."),
    ("project-alpha", "Alpha signal research: README, tests and a one-page results note",
     "Cross-sectional momentum and mean reversion over a few hundred shares. The note reports information coefficient, turnover and Sharpe after costs, and what failed."),
    ("project-options", "Options analytics dashboard: README, tests and a one-page results note",
     "An implied volatility surface and Greeks, with Black-Scholes, binomial and Monte Carlo pricers compared. The note says what failed. On the developer track the live market data handler may replace it."),
    ("contests", "Weekly Codeforces contests, with your rating recorded",
     "One rated contest most weeks once 100 problems are behind you. A rating of 1400 is a fair first-year target."),
]


def minutes(items, extra=0):
    return int(math.ceil(1.25 * (sum(it["pace"] for it in items) + extra) / 60 / 5) * 5)


DRAW_D = [{"from": "drills/oa", "difficulty": [3, 4], "n": 1}]
DRAW_D_PACE = 1800
doc = {
    "id": "stage-2", "stage": 2, "name": "Stage 2 exit test",
    "description": "The exit test for Intermediate, in four papers and six checks. "
                   "Paper A is machine learning and validation, paper B time series. "
                   "Paper C is numerical methods and optimisation. Paper D is backtesting, alpha, options and contests. "
                   "Statistical modelling, topic 2.6, is the researcher track, so it sits in its own topic exam. The checks cover your projects, your explanations and your contests.",
    "parts": [
        {"kind": "paper", "id": "ml-validation", "name": "Paper A: machine learning and validation", "minutes": minutes(A), "pass": 0.7, "items": A},
        {"kind": "paper", "id": "time-series", "name": "Paper B: time series", "minutes": minutes(B), "pass": 0.7, "items": B},
        {"kind": "paper", "id": "numerics-optimisation", "name": "Paper C: numerical methods and optimisation", "minutes": minutes(C), "pass": 0.7, "items": C},
        {"kind": "paper", "id": "projects-contests", "name": "Paper D: backtesting, alpha, options and contests", "minutes": minutes(D, DRAW_D_PACE), "pass": 0.7,
         "items": D, "draw": DRAW_D},
    ] + [{"kind": "check", "id": i, "name": n, "detail": dt} for i, n, dt in CHECKS],
}

if __name__ == '__main__':
    with open(OUT, 'w', encoding='utf8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write('\n')
    for p in doc["parts"]:
        if p["kind"] == "paper":
            ds = [it["difficulty"] for it in p["items"]]
            print(p["id"], len(p["items"]), "authored +", sum(d_["n"] for d_ in p.get("draw", [])), "drawn,",
                  p["minutes"], "min, ramp", [ds.count(k) for k in (2, 3, 4, 5)])
    print("wrote", os.path.relpath(OUT))
