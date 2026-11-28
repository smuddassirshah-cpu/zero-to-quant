"""Build app/content/exams/topic-2.7.json (topic 2.7, Deep learning: nn-train L1 to L4, cnn L1 to L3, sequence L1 to L4,
representations L1 to L5).

Route A for every key: plain floats, closed forms and the two code solutions run here in CPython to write their expects.
check_numbers.py recomputes every value by a second route (exact Fractions where the data allow, numpy.linalg for the
eigen items, the shipped cnn_ops_l3 and seq_ops_l3 modules for the code items) and asserts it at its path in the written file.
Run from anywhere: python3 docs/briefs/exam-2.7-scripts/build.py
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', '..', 'app')
OUT = os.path.join(APP, 'content', 'exams', 'topic-2.7.json')
DATA = os.path.join(APP, 'content', 'data', 'ai')


def r(x, n=6):
    return round(float(x), n)


def fb(correct, generic, by_key=None):
    d = {"correct": correct, "generic": generic}
    if by_key:
        d["byKey"] = by_key
    return d


def num(answer, tol, wrong=(), label="Answer"):
    w = {"kind": "numeric", "answer": answer, "tol": {"abs": tol}, "placeholder": "a number", "label": label}
    if wrong:
        w["wrong"] = [{"id": i, "value": v, "tol": {"abs": t}} for i, v, t in wrong]
    return w


def choice(options):
    return {"kind": "choice", "layout": "stack", "options": options}


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


def parts(id, d, skills, tags, pace, title, prose, question, ps, explain):
    return {"id": id, "difficulty": d, "skills": skills, "tags": tags, "pace": pace, "title": title,
            "prose": prose, "question": question,
            "parts": [{"question": q, "widget": w, "feedback": f} for q, w, f in ps],
            "explain": {"text": explain}}


items = []

# ================================================================ difficulty 2
# 1 (cnn l9, l10): misreads the exit allows
n1, bar1 = 540, 0.98
mis1 = math.floor(n1 * (1 - bar1) + 1e-9)
items.append(item(
    "e-misreads-allowed", 2, ["cnn-train"], ["held-out-accuracy"], 60, "Room for error",
    "This exam's digits check asks for a held-out accuracy of at least 0.98. The held-out split holds 540 digits.",
    "At most how many of the 540 may the net misread and still pass?",
    num(mis1, 0, [("up", mis1 + 1, 0), ("share", 10.8, 0.05), ("right", n1 - mis1, 0)], label="Misreads"),
    fb("$540 \\times 0.02 = 10.8$ is the limit, so 10 whole digits. Ten misreads leave 530 right, "
       "$530/540 = 0.9815$, which meets the bar.",
       "Find the share it may get wrong, then turn it into a whole number of digits.",
       {"up": "Eleven misreads leave 529 right, $529/540 = 0.9796$, under the bar. Round the limit of 10.8 down.",
        "share": "10.8 is $540 \\times 0.02$, but misreads are whole digits. Ten passes and eleven does not.",
        "right": "530 is about how many it must read right. The question asks how many it may misread."}),
    "Passing needs at least $0.98 \\times 540 = 529.2$ right, so at least 530, and at most $540 - 530 = 10$ wrong. "
    "The supplied exit net of `cnn` misreads 8, inside that."))

# 2 (nn-train l13): seeds for a standard error
s2, se2 = 0.03, 0.005
n2 = (s2 / se2) ** 2
items.append(item(
    "e-seeds-for-se", 2, ["nt-experiment"], ["seed-spread"], 75, "Seeds for a tight mean",
    "A set-up's validation loss has an sd of 0.03 across training seeds. You will report the mean over $n$ seeds "
    "with its standard error, $s/\\sqrt n$.",
    "How many seeds bring the standard error down to 0.005?",
    num(round(n2), 0, [("root", round(math.sqrt(n2)), 0)], label="Seeds"),
    fb("$\\sqrt n = 0.03/0.005 = 6$, so $n = 36$ seeds.",
       "Set $0.03/\\sqrt n = 0.005$ and solve for $n$.",
       {"root": "Six is $\\sqrt n$. The standard error falls with the square root of the seed count, so square it."}),
    "The standard error shrinks like $1/\\sqrt n$, so halving it costs four times the seeds. "
    "Here 36 seeds give $0.03/6 = 0.005$."))

# 3 (representations l1): one row looked up twice
G3 = [(0.5, -1), (2, 0.3), (-0.2, 0.6)]
g3 = G3[0][0] + G3[2][0]
items.append(item(
    "e-repeated-lookup", 2, ["rp-embed"], ["embedding-gradient"], 75, "One row looked up twice",
    "A batch looks up rows $(4, 1, 4)$ of an embedding table. The loss sends back one gradient row per lookup, in batch "
    "order: $(0.5, -1)$, $(2, 0.3)$ and $(-0.2, 0.6)$.",
    "What is the first entry of the gradient for row 4 of the table? Give a decimal.",
    num(r(g3, 4), 0.0005, [("last", -0.2, 0.0005), ("first", 0.5, 0.0005), ("mean", r(g3 / 2, 4), 0.0005),
                           ("row1", 2, 0.0005)], label="Gradient entry"),
    fb("Both lookups of row 4 add their shares: $0.5 + (-0.2) = 0.3$.",
       "Add the gradient rows of every lookup that read row 4.",
       {"last": "That keeps only the second lookup of row 4. Each lookup adds its share to the row it read.",
        "first": "That keeps only the first lookup of row 4. The second lookup adds its share too.",
        "mean": "You averaged the two shares. The gradient of a row looked up twice is their sum.",
        "row1": "That is the share of the lookup of row 1."}),
    "A lookup is a product with a one-hot row, so backward multiplies by the transposed one-hot matrix. "
    "That adds up the gradient rows of every lookup of the same item: here the first and the third, $0.5 - 0.2 = 0.3$."))

# 4 (nn-train l6, cnn l7): He for a convolution
fan4 = 16 * 3 * 3
he4 = math.sqrt(2 / fan4)
items.append(item(
    "e-he-for-a-conv", 2, ["nt-signal"], ["initialisation"], 75, "He for a convolution",
    "A ReLU convolution reads 16 input channels through 3 by 3 kernels. Each output sums over every weight of one filter.",
    "What weight sd does He initialisation give? Give 4 decimal places.",
    num(r(he4, 4), 0.0001, [("lecun", r(math.sqrt(1 / fan4), 4), 0.0001), ("fan9", r(math.sqrt(2 / 9), 4), 0.0001),
                            ("var", r(2 / fan4, 4), 0.0001)], label="Weight sd"),
    fb("The fan-in is $16 \\times 3 \\times 3 = 144$, so He gives $\\sqrt{2/144} \\approx 0.1179$.",
       "Count the weights one output sums over, then use He's $\\sqrt{2/n}$.",
       {"lecun": "That is $\\sqrt{1/144}$, LeCun's scale for linear or tanh units. ReLU halves the second moment, so "
                  "He doubles the variance to $2/n$.",
        "fan9": "You took the fan-in of one channel, 9. Each output sums over all 16 channels, so $n = 144$.",
        "var": "That is the variance $2/144$. The sd is its square root."}),
    "He keeps the second moment steady through ReLU layers with $\\operatorname{Var}(w) = 2/n$, where $n$ is the fan-in. "
    "A convolution's fan-in is its input channels times the kernel area, $16 \\times 9 = 144$, so the sd is 0.1179."))

# 5 (representations l11): KL of a wide code
kl5 = 0.5 * (0 + 4 - 1 - math.log(4))
items.append(item(
    "e-kl-wide-code", 2, ["rp-vae"], ["gaussian-kl"], 75, "A code wider than the prior",
    "An encoder gives one code coordinate $\\mu = 0$ and $\\sigma = 2$.",
    "What is its KL to $\\mathcal{N}(0, 1)$, in nats? Give a decimal to 3 places.",
    num(r(kl5, 3), 0.0005, [("nolog", 1.5, 0.0005), ("sd", r(0.5 * (2 - 1 - math.log(2)), 3), 0.0005),
                            ("logsd", r(0.5 * (4 - 1 - math.log(2)), 3), 0.0005)], label="KL (nats)"),
    fb("$\\tfrac12(0 + 4 - 1 - \\ln 4) = \\tfrac12(3 - 1.386) \\approx 0.807$ nats.",
       "Use $\\tfrac12(\\mu^2 + \\sigma^2 - 1 - \\ln\\sigma^2)$ with the variance, $\\sigma^2 = 4$.",
       {"nolog": "You left out $-\\ln\\sigma^2$. Without it a wide code is charged too much and a narrow one too little.",
        "sd": "You put in $\\sigma = 2$ where the formula wants the variance, $\\sigma^2 = 4$.",
        "logsd": "You took $\\ln\\sigma$, not $\\ln\\sigma^2 = \\ln 4$."}),
    "The KL charges a code for straying from the prior in width as well as in centre. "
    "A code twice as wide as the prior costs 0.807 nats even with its mean at 0."))

# 6 (sequence l2, l3): what survives 25 steps back
w6, T6 = 0.92, 25
k6 = w6 ** T6
items.append(item(
    "e-gradient-kept", 2, ["sqn-rnn"], ["vanishing-gradient"], 60, "What survives 25 steps",
    "A one-unit linear recurrent net has recurrent weight $w = 0.92$.",
    "What share of its size does a gradient keep after travelling 25 steps back? Give 4 decimal places.",
    num(r(k6, 4), 0.0001, [("linear", r(1 - T6 * (1 - w6), 4), 0.0001), ("one-fewer", r(w6 ** (T6 - 1), 4), 0.0001)],
        label="Share kept"),
    fb("Each step back multiplies the gradient by $w$, so the factor is $0.92^{25} \\approx 0.1244$.",
       "Multiply by $w$ once for each step back.",
       {"linear": "You took 0.08 off for each step. The gradient is multiplied by 0.92 at each step, so it shrinks by a power.",
        "one-fewer": "That is $0.92^{24}$. A gradient that travels 25 steps back is multiplied 25 times."}),
    "For $h_t = w\\,h_{t-1} + u\\,x_t$ the derivative $\\partial h_T/\\partial h_0$ is $w^T$. "
    "At $w = 0.92$ a gradient from 25 steps back keeps 0.1244 of its size, about 12%."))

# ================================================================ difficulty 3
# 7 (nn-train l3): Adam when the gradient is as small as epsilon
eta7, g7, eps7, b1, b2 = 0.01, 1e-8, 1e-8, 0.9, 0.999
m7, v7 = (1 - b1) * g7, (1 - b2) * g7 ** 2
mh7, vh7 = m7 / (1 - b1), v7 / (1 - b2)
step7 = eta7 * mh7 / (math.sqrt(vh7) + eps7)
raw7 = eta7 * m7 / (math.sqrt(v7) + eps7)
items.append(item(
    "e-adam-tiny-gradient", 3, ["nt-optim"], ["adam-step"], 90, "A gradient as small as epsilon",
    "Adam runs with $\\eta = 0.01$, $\\beta_1 = 0.9$, $\\beta_2 = 0.999$ and $\\epsilon = 10^{-8}$. At step 1 one "
    "coordinate's gradient is $10^{-8}$.",
    "How far does that coordinate move at step 1? Give a decimal.",
    num(r(step7, 6), 0.00005, [("noeps", 0.01, 0.00005), ("sgd", 1e-10, 1e-11), ("raw", r(raw7, 6), 0.00005)],
        label="Move"),
    fb("After the corrections $\\hat m = 10^{-8}$ and $\\sqrt{\\hat v} = 10^{-8}$, so the step is "
       "$0.01 \\times 10^{-8}/(10^{-8} + 10^{-8}) = 0.005$.",
       "Correct $m$ and $v$ for step 1, then divide by $\\sqrt{\\hat v} + \\epsilon$, not by $\\sqrt{\\hat v}$ alone.",
       {"noeps": "That drops $\\epsilon$. Here $\\epsilon$ is as large as $\\sqrt{\\hat v}$, so it halves the step.",
        "sgd": "That is plain SGD, $\\eta g$. Adam divides by the gradient's own size.",
        "raw": "You skipped the bias corrections. At step 1 they turn $m = 0.1g$ and $v = 0.001g^2$ back into $g$ and $g^2$."}),
    "Adam's first step is about $\\eta$ in every coordinate, because $\\hat m/\\sqrt{\\hat v} = \\pm 1$. "
    "That fails only when the gradient is as small as $\\epsilon$, which here halves the step to 0.005."))

# 8 (nn-train l1, l4): linear scaling and a warm-up
eta8, B8a, B8b, wu8, t8 = 0.05, 128, 512, 40, 15
peak8 = eta8 * B8b / B8a
rate8 = peak8 * t8 / wu8
items.append(item(
    "e-scaled-warmup", 3, ["nt-optim"], ["lr-schedule"], 100, "A bigger batch, a warm-up",
    "A net trains well at batch 128 with $\\eta = 0.05$. The team moves to batch 512, scales the rate by the linear "
    "scaling rule, and warms up linearly from 0 over 40 steps.",
    "What rate does step 15 use? Give a decimal.",
    num(r(rate8, 6), 0.0005, [("noscale", r(eta8 * t8 / wu8, 6), 0.0005), ("nowarm", r(peak8, 6), 0.0005),
                              ("sqrt", r(eta8 * math.sqrt(B8b / B8a) * t8 / wu8, 6), 0.0005)], label="Rate"),
    fb("Linear scaling gives $0.05 \\times 512/128 = 0.2$. Fifteen steps into a 40-step warm-up the rate is "
       "$0.2 \\times 15/40 = 0.075$.",
       "Scale the peak rate with the batch size first, then take the warm-up's share at step 15.",
       {"noscale": "That warms up to the old rate, 0.05, so step 15 reads only $0.05 \\times 15/40$. The rule raises the "
                   "peak in proportion to the batch, to 0.2.",
        "nowarm": "0.2 is the peak. At step 15 the warm-up has climbed only $15/40$ of the way.",
        "sqrt": "That uses the square-root rule, a peak of 0.1. The linear scaling rule multiplies by $512/128 = 4$."}),
    "The linear scaling rule grows the rate with the batch, and the warm-up keeps the first large steps small. "
    "At step 15 the warm-up has climbed $15/40$ of the way, to 0.075, and the run then climbs to 0.2. "
    "Treat that peak as a starting point to confirm with a short sweep."))

# 9 (nn-train l6): variance after a ReLU
var9, n9, sd9 = 1.5, 200, 0.08
out9 = n9 * sd9 ** 2 * var9 / 2
items.append(item(
    "e-relu-variance", 3, ["nt-signal"], ["initialisation"], 100, "Variance after a ReLU",
    "A layer's pre-activations $z$ are symmetric about 0 with variance 1.5. They pass through ReLU, $h = \\max(0, z)$, "
    "into a next layer with 200 inputs per unit and independent zero-mean weights of sd 0.08.",
    "What is the variance of the next layer's pre-activation? Give a decimal to 2 places.",
    num(r(out9, 2), 0.005, [("nohalf", r(n9 * sd9 ** 2 * var9, 2), 0.005), ("sd", r(n9 * sd9 * var9 / 2, 2), 0.005)],
        label="Variance"),
    fb("$E[h^2] = \\tfrac12 \\times 1.5 = 0.75$, so the variance is $200 \\times 0.08^2 \\times 0.75 = 0.96$.",
       "Use $n\\operatorname{Var}(w)E[h^2]$, with $E[h^2]$ half of $E[z^2]$ after ReLU.",
       {"nohalf": "You used 1.5 as it stood. ReLU zeroes the negative half, so $E[h^2]$ is half of 1.5.",
        "sd": "You used the sd 0.08 where the rule wants the variance, $0.08^2 = 0.0064$."}),
    "For a symmetric $z$, $E[\\max(0, z)^2] = \\tfrac12 E[z^2]$: the positive half carries half the second moment. "
    "So the next layer's variance is 0.96, and that halving is why He initialisation doubles LeCun's variance."))

# 10 (nn-train l10): stop, then read it as ridge
L10 = [0.90, 0.70, 0.58, 0.55, 0.56, 0.53, 0.52, 0.54, 0.55, 0.57]
eta10, every10, pat10 = 0.005, 50, 3
best10, stop10 = 0, None
for i, v in enumerate(L10):
    if v < L10[best10]:
        best10 = i
    if i - best10 >= pat10:
        stop10 = i
        break
lam10 = 1 / (eta10 * best10 * every10)
items.append(parts(
    "e-stop-then-ridge", 3, ["nt-general"], ["early-stopping"], 150, "Stop, then read it as ridge",
    "Plain gradient descent from zero on a least-squares loss uses $\\eta = 0.005$. Validation loss is taken every 50 "
    "steps, evaluation 0 at step 0: " + ", ".join(f"{v:.2f}" for v in L10) + ". Training stops once 3 evaluations in "
    "a row bring no new best, and keeps the best evaluation's weights.",
    "Early stopping chooses a step count on validation data.",
    [("At which evaluation, counting from 0, does training stop?",
      num(stop10, 0, [("best", best10, 0), ("p2", best10 + 2, 0), ("first-rise", 4, 0)], label="Evaluation"),
      fb("The best is 0.52 at evaluation 6. Evaluations 7, 8 and 9 bring no new best, so training stops at 9.",
         "Track the best so far, and count the evaluations since it was set.",
         {"best": "Evaluation 6 holds the best loss, and its weights are kept. Training stops only after 3 more "
                  "evaluations bring nothing better.",
          "p2": "Patience 3 means three evaluations with no new best: 7, 8 and 9.",
          "first-rise": "Evaluation 4 rose, but evaluation 5 then set a new best. Patience counts from the last best."})),
     ("Using the kept weights, read stopping as ridge with $\\lambda \\approx 1/(\\eta t)$, $t$ the step count. What "
      "$\\lambda$ is that? Give 4 decimal places.",
      num(r(lam10, 4), 0.0001, [("stopstep", r(1 / (eta10 * stop10 * every10), 4), 0.0001),
                                ("prod", r(eta10 * best10 * every10, 4), 0.0001),
                                ("evals", r(1 / (eta10 * best10), 4), 0.0001)], label="Lambda"),
      fb("The kept weights are from step $6 \\times 50 = 300$, so $\\lambda \\approx 1/(0.005 \\times 300) = 0.6667$.",
         "Turn the kept evaluation into a step count, then take $1/(\\eta t)$.",
         {"stopstep": "That uses step 450, where training stopped. The kept weights are evaluation 6's, from step 300.",
          "prod": "That is $\\eta t$ itself. The matching penalty is its reciprocal.",
          "evals": "You counted evaluations, not steps. Evaluation 6 is step 300."}))],
    "Patience decides when to stop, and the weights kept are the best evaluation's. For descent from zero on least "
    "squares, stopping at step $t$ behaves much like ridge with $\\lambda \\approx 1/(\\eta t)$, so stopping later is a "
    "weaker penalty."))

# 11 (nn-train l12): the minimum-norm fit
a11, y11 = np.array([1.0, 2.0, 2.0]), 18.0
w11 = a11 * y11 / (a11 @ a11)
items.append(item(
    "e-min-norm-three", 3, ["nt-general"], ["min-norm"], 120, "The gentlest exact fit",
    "A least-squares problem has one equation in three weights: $w_1 + 2w_2 + 2w_3 = 18$. It has infinitely many exact fits.",
    "What is $w_2$ in the minimum-norm solution?",
    num(r(w11[1], 4), 0.001, [("equal", r(y11 / a11.sum(), 4), 0.001), ("one", r(y11 / a11[1], 4), 0.001),
                              ("nonorm", r(y11 * a11[1], 4), 0.001)], label="w2"),
    fb("The minimum-norm fit is a multiple of the row $\\mathbf a = (1, 2, 2)$: $\\mathbf w = 18\\,\\mathbf a/\\lVert\\mathbf a"
       "\\rVert^2 = 2(1, 2, 2)$, so $w_2 = 4$.",
       "Take $\\mathbf w = c\\,(1, 2, 2)$, the row of the equation, and choose $c$ so the equation holds.",
       {"equal": "Equal weights fit, with $w = 3.6$, but they are not the shortest fit. The shortest points along the row $(1, 2, 2)$.",
        "one": "Putting everything on $w_2$ fits too, with norm 9. The fit $(2, 4, 4)$ is shorter, with norm 6.",
        "nonorm": "You took $18\\,\\mathbf a$ without dividing by $\\lVert\\mathbf a\\rVert^2 = 9$. That gives "
                  "$18 + 2 \\times 36 + 2 \\times 36 = 162$, not 18."}),
    "Any exact fit is the shortest one plus a direction the equation cannot see. "
    "So the shortest lies along the equation's own row, $\\mathbf w = \\mathbf F^+\\mathbf y = 2(1, 2, 2)$: $w_2 = 4$, with norm 6. "
    "Gradient descent from zero ends there too."))

# 12 (nn-train l16): what pairing buys
sa12, sb12, rho12 = 0.040, 0.045, 0.9
v12 = sa12 ** 2 + sb12 ** 2 - 2 * rho12 * sa12 * sb12
sd12 = math.sqrt(v12)
ind12 = math.sqrt(sa12 ** 2 + sb12 ** 2)
items.append(item(
    "e-paired-sd", 3, ["nt-experiment"], ["paired-seeds"], 120, "What pairing buys",
    "Set-ups A and B ran on the same seeds. Across seeds A's loss has sd 0.040 and B's 0.045, and the two are "
    "correlated with $\\rho = 0.9$. For the difference, $\\operatorname{Var}(B - A) = \\operatorname{Var}(A) + "
    "\\operatorname{Var}(B) - 2\\rho\\,\\operatorname{sd}(A)\\operatorname{sd}(B)$.",
    "What is the sd of the paired differences $B - A$? Give 4 decimal places.",
    num(r(sd12, 4), 0.0001, [("indep", r(ind12, 4), 0.0001),
                             ("half", r(math.sqrt(sa12 ** 2 + sb12 ** 2 - rho12 * sa12 * sb12), 4), 0.0001),
                             ("nosqrt", r(v12, 6), 0.0001)], label="sd of B - A"),
    fb("$0.0016 + 0.002025 - 2 \\times 0.9 \\times 0.040 \\times 0.045 = 0.000385$, and $\\sqrt{0.000385} \\approx 0.0196$.",
       "Put the two sds and $\\rho$ into the formula, then take the square root.",
       {"indep": "That treats the runs as independent, $\\rho = 0$. Shared seeds make the runs move together, which "
                  "shrinks the difference.",
        "half": "You left out the 2 in $2\\rho\\,\\operatorname{sd}(A)\\operatorname{sd}(B)$.",
        "nosqrt": "That is the variance. The sd is its square root."}),
    "Seeds that give both set-ups the same weights and batches make their losses move together, and the shared part "
    "cancels in $B - A$. Here pairing cuts the sd of a comparison from 0.0602 to 0.0196, so a paired test needs far "
    "fewer seeds."))

# 12b (cnn l12, homework-3): the clear-margin rule on shifted digits
cnn12b = [0.66, 0.64, 0.50, 0.62]
mean12b = sum(cnn12b) / 4
cap12b = mean12b - 0.10
items.append(item(
    "e-shift-margin", 3, ["cnn-train"], ["shift-margin"], 100, "A clear margin on shifted digits",
    "The exit compares the CNN with a same-size MLP on digits shifted one pixel right, left, down and up. It asks the "
    "CNN's mean shifted accuracy to beat the MLP's by at least 0.10. The CNN scores 0.66, 0.64, 0.50 and 0.62 on the "
    "four shifts.",
    "What is the highest mean shifted accuracy the MLP may have for the CNN to meet the margin? Give a decimal to 3 places.",
    num(r(cap12b, 3), 0.0005, [("nomargin", r(mean12b, 3), 0.0005), ("plus", r(mean12b + 0.10, 3), 0.0005),
                               ("ratio", r(mean12b / 1.10, 3), 0.0005)], label="MLP mean"),
    fb("The CNN's mean is $(0.66 + 0.64 + 0.50 + 0.62)/4 = 0.605$. The MLP must sit 0.10 below it: $0.605 - 0.10 = 0.505$.",
       "Average the CNN's four accuracies, then take the margin off.",
       {"nomargin": "0.605 is the CNN's own mean. The CNN must lead by 0.10, so the MLP must sit 0.10 below it.",
        "plus": "0.705 adds the margin. The MLP must be 0.10 below the CNN, not above it.",
        "ratio": "That divides by 1.10. The margin is a gap of 0.10 in accuracy, not a ratio."}),
    "The margin rule is a difference of mean accuracies: not a ratio, and not any lead. A tie at 0.505 still passes, "
    "since the rule asks for at least 0.10."))

# 13 (cnn l7): receptive field through a pool
layers13 = [(3, 1), (2, 2), (3, 1), (3, 1)]
rf13, prod13 = 1, 1
for k, s in layers13:
    rf13 += (k - 1) * prod13
    prod13 *= s
items.append(item(
    "e-receptive-field", 3, ["cnn-layers"], ["receptive-field"], 100, "How far a deep output sees",
    "A net stacks a 3 by 3 conv at stride 1 and a 2 by 2 max pool at stride 2. Two more 3 by 3 convs at stride 1 follow.",
    "What is the side of the receptive field of the last conv's outputs, in input pixels?",
    num(rf13, 0, [("nostride", 1 + sum(k - 1 for k, _ in layers13), 0), ("sum-k", sum(k for k, _ in layers13), 0)],
        label="Side (pixels)"),
    fb("Each layer adds $(k - 1)$ times the product of the strides before it: $1 + 2 + 1 + 2 \\times 2 + 2 \\times 2 = 12$.",
       "Start at 1 and add $(k - 1)$ times the stride product of the earlier layers, layer by layer.",
       {"nostride": "You added $k - 1$ for every layer as if all strides were 1. After the pool one step of a map is 2 "
                    "input pixels, so the last two convs add 4 each.",
        "sum-k": "You added the kernel sizes. Each layer widens the view by $k - 1$ steps of its input, not by $k$."}),
    "One step on the pooled map is 2 input pixels. So each later 3 by 3 conv widens the view by 4 pixels, not 2, for a side of 12. "
    "Pooling is what lets a few small kernels see the whole of an 8 by 8 digit."))

# 14 (sequence l7, l8): one query, three keys
q14 = np.array([1.0, -1.0, 2.0, 0.0])
K14 = np.array([[2.0, 0.0, 1.0, 1.0], [0.0, 2.0, 1.0, 0.0], [1.0, 1.0, 0.0, 3.0]])
s14 = K14 @ q14 / 2.0
a14 = np.exp(s14) / np.exp(s14).sum()
araw14 = np.exp(K14 @ q14) / np.exp(K14 @ q14).sum()
ad14 = np.exp(K14 @ q14 / 4) / np.exp(K14 @ q14 / 4).sum()
items.append(parts(
    "e-scaled-attention", 3, ["sqn-attend"], ["attention-weights"], 150, "One query, three keys",
    "Three keys, $(2, 0, 1, 1)$, $(0, 2, 1, 0)$ and $(1, 1, 0, 3)$, store the values 10, $-5$ and 3. The query is "
    "$\\mathbf q = (1, -1, 2, 0)$, and its scores are divided by $\\sqrt d$ with $d = 4$.",
    "The output is the weighted mean of the values.",
    [("What weight does the first key get? Give 4 decimal places.",
      num(r(a14[0], 4), 0.0001, [("raw", r(araw14[0], 4), 0.0001), ("byd", r(ad14[0], 4), 0.0001),
                                 ("third", r(1 / 3, 4), 0.0001)], label="Weight"),
      fb("The raw scores are 4, 0 and 0, scaled to 2, 0 and 0. The first key gets $e^2/(e^2 + 2) \\approx 0.7870$.",
         "Take each dot product, divide by $\\sqrt 4$, then apply the softmax over the three keys.",
         {"raw": "You skipped the $\\sqrt d$ scaling. Divide the scores 4, 0 and 0 by 2 first.",
          "byd": "You divided by $d = 4$, not by $\\sqrt d = 2$.",
          "third": "Equal weights ignore the scores. The first key's scaled score is 2 above the others."})),
     (f"The weights are 0.7870, {r(a14[1], 4)} and {r(a14[2], 4)}. By how much does the output move if the second key's "
      "value rises from $-5$ to $-4$? Give 4 decimal places.",
      num(r(a14[1], 4), 0.0001, [("one", 1, 0.0001), ("first", r(a14[0], 4), 0.0001), ("third", r(1 / 3, 4), 0.0001)],
          label="Change in output"),
      fb(f"The output is $\\sum_i \\alpha_i v_i$, so it moves by $\\alpha_2 \\times 1 \\approx {r(a14[1], 4)}$.",
         "The output is linear in each value. Its slope in a value is that key's weight.",
         {"one": "That would hold only if the second key had all the weight. The output moves by that key's weight "
                 "times the change.",
          "first": "That is the first key's weight. The change is in the second key's value.",
          "third": "That is an equal share. The second key's weight is set by its score."}))],
    "Scaling keeps a score gap of 4 from becoming a near-certain choice: unscaled, the first key would take 0.9647. "
    "Because the output is a weighted mean of the values, the slope in any one value is its key's weight."))

# 15 (sequence l12): two positions apart
pe15 = math.cos(2) + math.cos(0.02)
items.append(item(
    "e-pe-offset", 3, ["sqn-self"], ["positions"], 120, "Two positions apart",
    "Sinusoidal positions at width $d = 4$ use the angles $t$ and $t/100$: "
    "$\\mathbf p_t = (\\sin t, \\cos t, \\sin(t/100), \\cos(t/100))$.",
    "What is $\\mathbf p_t \\cdot \\mathbf p_{t+2}$, for any $t$? Give 4 decimal places.",
    num(r(pe15, 4), 0.0001, [("one-pair", r(math.cos(2), 4), 0.0001),
                             ("deg", r(math.cos(math.radians(2)) + math.cos(math.radians(0.02)), 4), 0.0001),
                             ("self", 2, 0.0001)], label="Dot product"),
    fb("Each sine and cosine pair gives the cosine of its angle gap: $\\cos 2 + \\cos 0.02 \\approx -0.4161 + 0.9998 = 0.5837$.",
       "Use $\\sin a \\sin b + \\cos a \\cos b = \\cos(a - b)$ for each pair.",
       {"one-pair": "That is the fast pair alone. The slow pair adds $\\cos 0.02 \\approx 0.9998$.",
        "deg": "You took the angles in degrees. Position codes use radians.",
        "self": "That is a position with itself, offset 0."}),
    "For each pair, $\\sin a \\sin b + \\cos a \\cos b = \\cos(a - b)$, and the angle gap depends only on the offset. "
    "So the dot product, 0.5837 at offset 2, depends on how far apart two positions are, not on where they sit."))

# 16 (sequence l15): counting a small model
d16, V16, C16, M16 = 80, 100, 16, 320
att16 = 4 * (d16 * d16 + d16)
mlp16 = d16 * M16 + M16 + M16 * d16 + d16
ln16 = 2 * 2 * d16
blk16 = att16 + mlp16 + ln16
tot16 = blk16 + V16 * d16 + C16 * d16 + 2 * d16 + d16 * V16 + V16
items.append(item(
    "e-model-count-80", 3, ["sqn-block"], ["parameter-count"], 150, "Counting a small model",
    "A one-block model knows 100 tokens and has learned positions for at most 16. The block has width 80, 4 heads and an MLP of "
    "width 320. Every projection has a bias, and both of its layer norms have a gain and a shift. It ends in a final layer norm "
    "and an untied unembedding with a bias.",
    "How many parameters does the model hold?",
    num(tot16, 0, [("tied", tot16 - V16 * d16, 0), ("nopos", tot16 - C16 * d16, 0), ("nobias", tot16 - V16, 0),
                   ("heads", tot16 + 3 * att16, 0)], label="Parameters"),
    fb("The block holds $25{,}920 + 51{,}600 + 320 = 77{,}840$. Add $8{,}000$ for tokens, $1{,}280$ for positions, 160 for "
       "the final norm and $8{,}100$ for the unembedding: 95,380.",
       "Count attention, the MLP and the two norms of the block, then the embeddings, positions, final norm and unembedding.",
       {"tied": "That ties the unembedding to the token table. It is untied here, so its $80 \\times 100$ weights count.",
        "nopos": "You left out the 16 learned position rows of width 80.",
        "nobias": "The unembedding keeps a bias of 100.",
        "heads": "The heads are slices of the four matrices: attention costs $4(80^2 + 80)$ whatever the number of heads."}),
    "Attention holds four $d \\times d$ matrices and their biases, $4(d^2 + d)$, and the MLP $2 \\times 80 \\times 320 + 320 + 80$. "
    "With so small a vocabulary the block holds most of the model's 95,380 parameters, 82% of them."))

# 17 (sequence l15): twice as wide
f17 = lambda d: 12 * d * d + 13 * d
ratio17 = f17(128) / f17(64)
items.append(item(
    "e-width-doubling", 3, ["sqn-block"], ["parameter-count"], 120, "Twice as wide",
    "A pre-norm block of width $d$ has an MLP four times as wide, a bias on each projection, and layer norms with a "
    "gain and a shift. At $d = 64$ it holds 49,984 parameters.",
    "How many times as many parameters does the same design hold at $d = 128$? Give 2 decimal places.",
    num(r(ratio17, 2), 0.005, [("two", 2, 0.005), ("four", 4, 0.005), ("eight", 8, 0.005)], label="Ratio"),
    fb("The block holds $12d^2 + 13d$: 198,272 at $d = 128$ against 49,984, a ratio of 3.97.",
       "Write the block's count as a function of $d$, then compare the two widths.",
       {"two": "Parameters do not grow with the width alone: every matrix is $d$ by $d$ or $d$ by $4d$, so they grow "
               "with $d^2$.",
        "four": "The matrices grow fourfold, but the biases and norms, $13d$, only double, so the ratio is a little under 4.",
        "eight": "Doubling $d$ doubles both sides of each matrix, a factor of 4, not 8."}),
    "Attention holds $4d^2 + 4d$, the MLP $8d^2 + 5d$ and the norms $4d$: $12d^2 + 13d$ in all. "
    "The $d^2$ terms dominate, so doubling the width roughly quadruples the block, here by 3.97."))

# 18 (representations l2): distance to cosine
dist18 = 0.6
cos18 = 1 - dist18 ** 2 / 2
items.append(item(
    "e-distance-to-cosine", 3, ["rp-embed"], ["cosine-similarity"], 100, "From distance to cosine",
    "Two rows of an embedding table have been divided by their lengths. The unit rows lie 0.6 apart by Euclidean distance.",
    "What is their cosine similarity? Give a decimal to 2 places.",
    num(r(cos18, 2), 0.005, [("lin", r(1 - dist18, 2), 0.005), ("sq", r(1 - dist18 ** 2, 2), 0.005),
                             ("half", r(1 - dist18 / 2, 2), 0.005)], label="Cosine"),
    fb("For unit rows $\\lVert\\hat{\\mathbf u} - \\hat{\\mathbf v}\\rVert^2 = 2 - 2\\cos$, so $\\cos = 1 - 0.36/2 = 0.82$.",
       "Expand $\\lVert\\hat{\\mathbf u} - \\hat{\\mathbf v}\\rVert^2$ for two rows of length 1.",
       {"lin": "Cosine is not one minus the distance. Expand the squared distance of two unit rows.",
        "sq": "You dropped the factor 2: $\\lVert\\hat{\\mathbf u} - \\hat{\\mathbf v}\\rVert^2 = 2 - 2\\cos$.",
        "half": "You halved the distance, not its square."}),
    "Expanding gives $\\lVert\\hat{\\mathbf u}\\rVert^2 + \\lVert\\hat{\\mathbf v}\\rVert^2 - 2\\,\\hat{\\mathbf u} \\cdot "
    "\\hat{\\mathbf v} = 2 - 2\\cos$, so a distance of 0.6 is a cosine of 0.82. Once rows are normalised, nearest by distance and nearest by cosine give the same ranking."))

# 19 (representations l5, l6): one code for two stocks
S19 = np.array([[3.0, 1.0], [1.0, 3.0]])
lam19 = sorted(np.linalg.eigvalsh(S19))
u19 = np.array([1.0, 1.0]) / math.sqrt(2)
x19 = np.array([2.0, -1.0])
z19 = x19 @ u19
e19 = float(((x19 - z19 * u19) ** 2).sum())
items.append(parts(
    "e-one-code-rebuild", 3, ["rp-autoenc"], ["linear-autoencoder"], 150, "One code for two stocks",
    "Two stocks' centred daily returns have covariance $\\boldsymbol\\Sigma = \\begin{pmatrix} 3 & 1 \\\\ 1 & 3 "
    "\\end{pmatrix}$, with eigenvalues 4 and 2. The best one-code linear autoencoder codes each day as $z = \\mathbf x "
    "\\cdot \\mathbf u$ along the top eigenvector $\\mathbf u = (1, 1)/\\sqrt 2$, and rebuilds $z\\mathbf u$.",
    "The error is the mean squared rebuild distance.",
    [("What is its error, averaged over days?",
      num(r(lam19[0], 4), 0.001, [("kept", r(lam19[1], 4), 0.001), ("total", r(sum(lam19), 4), 0.001), ("diag", 3, 0.001)],
          label="Error"),
      fb("The error is the variance it drops, the smaller eigenvalue, 2.",
         "A linear autoencoder's error is the sum of the eigenvalues it drops.",
         {"kept": "4 is the variance it keeps along $\\mathbf u$. The error is what it drops.",
          "total": "6 is the total variance, the error with no code at all.",
          "diag": "3 is one stock's variance. The error is the dropped eigenvalue."})),
     ("One day is $\\mathbf x = (2, -1)$. What is that day's squared rebuild distance? Give a decimal.",
      num(r(e19, 4), 0.001, [("code", r(z19 ** 2, 4), 0.001), ("whole", r(x19 @ x19, 4), 0.001)], label="Squared distance"),
      fb("$z = (2 - 1)/\\sqrt 2 \\approx 0.7071$, the rebuild is $(0.5, 0.5)$, and $1.5^2 + 1.5^2 = 4.5$.",
         "Code the day, rebuild it as $z\\mathbf u$, then add the squared differences.",
         {"code": "0.5 is $z^2$, the part of the day the code keeps. The distance is what is left: $5 - 0.5$.",
          "whole": "5 is the day's whole squared length. Subtract the part along $\\mathbf u$."}))],
    "A one-code linear autoencoder keeps a day's part along the top eigenvector, so its average error is the variance "
    "across it. This day moves against the pair's usual co-movement, so it rebuilds worse than the average of 2."))

# 20 (representations l11): KL from log-variances
mu20 = [0.8, -0.6]
ell20 = [math.log(2), math.log(0.25)]
k20 = [0.5 * (m * m + math.exp(l) - 1 - l) for m, l in zip(mu20, ell20)]
sd20 = sum(0.5 * (m * m + math.exp(l / 2) - 1 - l / 2) for m, l in zip(mu20, ell20))
nolog20 = sum(0.5 * (m * m + math.exp(l) - 1) for m, l in zip(mu20, ell20))
items.append(item(
    "e-kl-two-coords", 3, ["rp-vae"], ["gaussian-kl"], 120, "KL from a log-variance",
    "An encoder returns a two-coordinate code with $\\boldsymbol\\mu = (0.8, -0.6)$ and log-variances "
    "$\\boldsymbol\\ell = (\\ln 2, \\ln 0.25)$.",
    "What is the code's KL to $\\mathcal N(\\mathbf 0, \\mathbf I)$, in nats? Give a decimal to 3 places.",
    num(r(sum(k20), 3), 0.0005, [("nolog", r(nolog20, 3), 0.0005), ("first", r(k20[0], 3), 0.0005),
                                 ("sd", r(sd20, 3), 0.0005)], label="KL (nats)"),
    fb("Each coordinate gives $\\tfrac12(\\mu^2 + e^{\\ell} - 1 - \\ell)$: $\\tfrac12(0.64 + 2 - 1 - 0.693) \\approx 0.473$ and "
       "$\\tfrac12(0.36 + 0.25 - 1 + 1.386) \\approx 0.498$, adding to 0.972.",
       "Work each coordinate with $e^{\\ell}$ for the variance and $-\\ell$ for $-\\ln\\sigma^2$, then add.",
       {"nolog": "You left out $-\\ell$. The second coordinate's narrow variance, 0.25, costs $+1.386$ through it.",
        "first": "That is the first coordinate alone. Independent coordinates add their KLs.",
        "sd": "You used the sds, $\\sqrt 2$ and 0.5, where the formula wants the variances $e^{\\ell}$."}),
    "Against $\\mathcal N(\\mathbf 0, \\mathbf I)$ the KL of a code with independent coordinates is the sum of one-coordinate KLs, here 0.972 nats. "
    "Working from $\\ell$ directly, with $e^{\\ell}$ and $-\\ell$, avoids taking the log of a variance that has underflowed."))

# 21 (representations l13, l14): undoing the noise in one go
ab21, xt21, eh21 = 0.36, 1.1, 0.5
x021 = (xt21 - math.sqrt(1 - ab21) * eh21) / math.sqrt(ab21)
items.append(item(
    "e-x0-from-noise", 3, ["rp-diffuse"], ["closed-form-noise"], 100, "Undoing the noise in one go",
    "At a step with $\\bar\\alpha_t = 0.36$, a one-coordinate point sits at $x_t = 1.1$. The noise predictor's guess of "
    "the standard normal draw is $\\hat\\epsilon = 0.5$. The closed form is $x_t = \\sqrt{\\bar\\alpha_t}\\,x_0 + "
    "\\sqrt{1 - \\bar\\alpha_t}\\,\\epsilon$.",
    "What estimate of $x_0$ does that guess give? Give 4 decimal places.",
    num(r(x021, 4), 0.0001, [("noroot", r((xt21 - (1 - ab21) * eh21) / ab21, 4), 0.0001),
                             ("nodiv", r(xt21 - math.sqrt(1 - ab21) * eh21, 4), 0.0001),
                             ("sign", r((xt21 + math.sqrt(1 - ab21) * eh21) / math.sqrt(ab21), 4), 0.0001)],
        label="Estimate of x0"),
    fb("$\\hat x_0 = (1.1 - 0.8 \\times 0.5)/0.6 = 0.7/0.6 \\approx 1.1667$.",
       "Solve the closed form for $x_0$, with the square roots of $\\bar\\alpha_t$ and $1 - \\bar\\alpha_t$.",
       {"noroot": "You used $\\bar\\alpha_t$ and $1 - \\bar\\alpha_t$ as they stand. The closed form scales by their square "
                  "roots, 0.6 and 0.8.",
        "nodiv": "That takes the noise off but does not undo the shrink: divide by $\\sqrt{\\bar\\alpha_t} = 0.6$.",
        "sign": "You added the noise term. Subtract it to undo the noise."}),
    "A noise predictor is also a denoiser: subtracting the scaled guess and undoing the shrink estimates the clean point, here 1.1667. "
    "The reverse sampler does not jump there; each step moves only part of the way and adds fresh noise."))

# 22 (representations l18): where averaging settles
deg22 = [2, 3, 3, 2]
x22 = [4, 0, 0, 0]
set22 = sum(d * x for d, x in zip(deg22, x22)) / sum(deg22)
items.append(item(
    "e-settle-path", 3, ["rp-graph"], ["message-passing"], 120, "Where averaging settles",
    "Four firms form a path, 1 to 2 to 3 to 4, and each has a self-loop. Firm 1 holds the value 4 and the others 0. "
    "Each step replaces every value by the mean over the firm and its neighbours, $\\tilde{\\mathbf D}^{-1}\\tilde{\\mathbf A}$.",
    "What value does every firm settle on? Give a decimal.",
    num(r(set22, 4), 0.0005, [("mean", 1, 0.0005), ("noloop", r(4 * 1 / 6, 4), 0.0005)], label="Settled value"),
    fb("The settled value weights each firm by its degree with the loop, 2, 3, 3 and 2: $(2 \\times 4)/10 = 0.8$.",
       "Repeated averaging keeps the degree-weighted mean: weight each firm's start by its degree, counting the loop.",
       {"mean": "The plain mean, $4/4 = 1$, would hold if every firm had the same degree. The middle firms count 3 each, "
                "the ends 2.",
        "noloop": "That uses the degrees without loops, 1, 2, 2 and 1. Each firm's own loop adds 1."}),
    "Averaging keeps the eigenvalue-1 part of the start, which weights each firm by its degree, here counting its loop. "
    "Firm 1 has degree 2 of a total of 10, so its 4 spreads to 0.8 everywhere."))

# ================================================================ difficulty 4
# 23 (nn-train l8): layer norm backwards
x23 = np.array([1.0, 3.0, 5.0, 7.0])
mu23, s23 = x23.mean(), math.sqrt(x23.var())
xh23 = (x23 - mu23) / s23
d23 = np.array([1.0, 0.0, 0.0, 0.0])
dx23 = (d23 - d23.mean() - xh23 * (d23 * xh23).mean()) / s23
items.append(parts(
    "e-layernorm-backward", 4, ["nt-signal"], ["layer-norm"], 240, "Layer norm, backwards",
    "Layer norm with $\\gamma = 1$ meets one example $\\mathbf x = (1, 3, 5, 7)$; ignore $\\epsilon$. The gradient "
    "reaching $\\hat{\\mathbf x}$ is $\\mathbf d = (1, 0, 0, 0)$. With $s = \\sqrt{\\sigma^2}$ over the 4 features, "
    "$\\partial L/\\partial x_i = \\frac1s\\big(d_i - \\bar d - \\hat x_i\\,\\overline{d\\hat x}\\big)$, where the bars "
    "are means over the features.",
    "The variance divides by the number of features.",
    [("What is $\\partial L/\\partial x_1$? Give 4 decimal places.",
      num(r(dx23[0], 4), 0.0001, [("plain", r(1 / s23, 4), 0.0001), ("centred", r(0.75 / s23, 4), 0.0001)], label="Gradient"),
      fb("$\\mu = 4$, $\\sigma^2 = 5$, $\\hat{\\mathbf x} = (-3, -1, 1, 3)/\\sqrt 5$, $\\bar d = 0.25$ and "
         "$\\overline{d\\hat x} = -3/(4\\sqrt 5)$. So $\\partial L/\\partial x_1 = (0.75 - 0.45)/\\sqrt 5 \\approx 0.1342$.",
         "Find $\\mu$, $s$ and $\\hat{\\mathbf x}$, then the two means, then the formula for $i = 1$.",
         {"plain": "That is $d_1/s$ alone. The mean and the variance both depend on $x_1$, so subtract $\\bar d$ and the "
                   "$\\hat x_1$ term.",
          "centred": "You subtracted $\\bar d$ but not $\\hat x_1\\,\\overline{d\\hat x} = 0.45$, the path through $\\sigma^2$."})),
     ("What do the four gradients $\\partial L/\\partial x_i$ add up to?",
      num(0, 0.0005, [("d", 1, 0.0005), ("s", r(1 / s23, 4), 0.0005)], label="Sum"),
      fb("They add up to 0: adding the same amount to every feature leaves $\\hat{\\mathbf x}$ unchanged, so the loss "
         "cannot change in that direction.",
         "Ask what happens to $\\hat{\\mathbf x}$ when every feature of $\\mathbf x$ moves by the same amount.",
         {"d": "That is the sum of $\\mathbf d$. Layer norm removes the mean, so its input gradient has none.",
          "s": "That is $1/s$, the scale, not the sum of the gradients."}))],
    "Shifting every feature of $\\mathbf x$ by the same amount leaves $\\hat{\\mathbf x}$ unchanged, so the input "
    "gradient is orthogonal to $(1, 1, 1, 1)$. A hand-written backward that does not add up to 0 over the features has "
    "lost the path through $\\mu$."))

# 24 (cnn l1, l2): two kernels in turn
comb24 = np.convolve([-1.0, 1.0], [0.5, 0.5])
n24 = 30
items.append(parts(
    "e-two-kernels-in-turn", 4, ["cnn-conv"], ["kernel-composition"], 180, "Two kernels in turn",
    "Closes go through the daily-change kernel $(-1, 1)$, then the 2-day mean kernel $(0.5, 0.5)$. Each is slid "
    "unflipped over valid positions, oldest weight first.",
    "Two linear slides make one.",
    [("Which single kernel gives the same outputs in one slide?",
      choice([opt("full", "$(-0.5, 0, 0.5)$", correct=True),
              opt("prod", "$(-0.5, 0.5)$", "That multiplies the kernels entry by entry. Sliding one after the other "
                  "spreads the weights over three closes."),
              opt("flip", "$(0.5, 0, -0.5)$", "That is the right kernel reversed: oldest weight first, it gives minus "
                  "the change over two days, halved."),
              opt("nohalf", "$(-1, 0, 1)$", "That is the change over two days without the 2-day mean's factor 0.5.")]),
      fb("The two-step output is $0.5(x_{t+2} - x_{t+1}) + 0.5(x_{t+1} - x_t) = -0.5x_t + 0.5x_{t+2}$: the kernel "
         "$(-0.5, 0, 0.5)$.",
         "Write one output of the second slide in terms of the closes.")),
     ("From 30 closes, how many outputs come out of the two slides?",
      num(n24 - 2, 0, [("one", n24 - 1, 0), ("sum", n24 - 4 + 1, 0), ("all", n24, 0)], label="Outputs"),
      fb("Each valid slide of a kernel of length 2 loses one output: $30 - 1 - 1 = 28$, the same as one slide of length 3.",
         "Count the outputs of the first slide, then slide the second kernel over those.",
         {"one": "That is after the first slide. The second slide loses one more.",
          "sum": "You took the combined kernel as length $2 + 2 = 4$. It has length $2 + 2 - 1 = 3$.",
          "all": "Valid positions only: each slide loses one output at the end."}))],
    "Convolutions are linear, so two in turn are one convolution whose kernel spreads each weight of the first over the "
    "second. The combined kernel has length $2 + 2 - 1 = 3$, which is why the count matches a single slide of 3."))

# 25 (cnn l5, l7): costing a strided layer
n25, k25, p25, s25, c25, F25 = 20, 5, 2, 2, 3, 12
o25 = (n25 + 2 * p25 - k25) // s25 + 1
par25 = F25 * (c25 * k25 * k25 + 1)
mac25 = o25 * o25 * c25 * k25 * k25 * F25
items.append(parts(
    "e-conv-layer-costs", 4, ["cnn-layers"], ["conv-arithmetic"], 240, "Costing a strided layer",
    "A first layer reads 3-channel 20 by 20 maps with 12 filters of 5 by 5, padding 2 and stride 2.",
    "Work out its size and cost.",
    [("What is the side of its output?",
      num(o25, 0, [("nofloor", (n25 + 2 * p25 - k25) / s25 + 1, 0), ("same", n25, 0),
                   ("nopad", (n25 - k25) // s25 + 1, 0)], label="Side"),
      fb("$\\lfloor (20 + 4 - 5)/2 \\rfloor + 1 = \\lfloor 9.5 \\rfloor + 1 = 10$.",
         "Use $\\lfloor (n + 2p - k)/s \\rfloor + 1$.",
         {"nofloor": "A layer has whole columns: round $(20 + 4 - 5)/2 = 9.5$ down before adding 1.",
          "same": "Padding 2 keeps the size only at stride 1. Stride 2 roughly halves it.",
          "nopad": "You left out the padding: the padded side is $20 + 2 \\times 2 = 24$."})),
     ("How many parameters does it have?",
      num(par25, 0, [("nobias", par25 - F25, 0), ("nocin", F25 * (k25 * k25 + 1), 0)], label="Parameters"),
      fb("$12 \\times (3 \\times 25 + 1) = 912$: each filter has a 5 by 5 kernel per input channel and one bias.",
         "Use $c_{\\text{out}}(c_{\\text{in}}k^2 + 1)$.",
         {"nobias": "Each of the 12 filters also has a bias.",
          "nocin": "Each filter has a 5 by 5 kernel for every one of the 3 input channels."})),
     ("Using the 10 by 10 output of part 1, how many multiply-adds does it take per image?",
      num(mac25, 0, [("stride1", n25 * n25 * c25 * k25 * k25 * F25, 0), ("onech", o25 * o25 * k25 * k25 * F25, 0),
                     ("params", par25, 0)], label="Multiply-adds"),
      fb("Each of the $10 \\times 10$ outputs of each filter is a dot product of $3 \\times 25 = 75$ terms: "
         "$100 \\times 75 \\times 12 = 90{,}000$.",
         "Multiply the output positions by the terms in one dot product and by the filters.",
         {"stride1": "That counts 400 positions, as at stride 1. Stride 2 leaves 100.",
          "onech": "Each dot product runs over all 3 channels, 75 terms.",
          "params": "That is the parameter count. Each weight is used at every one of the 100 positions."}))],
    "Parameters do not depend on the map size, but multiply-adds do: each weight is used once per output position. "
    "Stride 2 cuts the positions, and so the cost, by four against stride 1."))

# 26 (representations l17, l19): a hub and its neighbours
dA, dH, dF = 3, 6, 2
aAH = 1 / math.sqrt(dA * dH)
aAF = 1 / math.sqrt(dA * dF)
mix26 = 3 / dA - 1 * aAH + 2 * aAF
out26 = max(0.0, 1.5 * mix26)
items.append(parts(
    "e-gcn-hub", 4, ["rp-graph"], ["gcn-layer"], 270, "A hub and its neighbours",
    "A lending network has a hub H linked to firms A, B, C, D and E; A is also linked to F. Every firm gets a "
    "self-loop, and $\\hat{\\mathbf A} = \\tilde{\\mathbf D}^{-1/2}\\tilde{\\mathbf A}\\tilde{\\mathbf D}^{-1/2}$.",
    "A graph layer mixes each firm with its neighbours through $\\hat{\\mathbf A}$.",
    [("What is $\\hat A_{AH}$? Give 3 decimal places.",
      num(r(aAH, 3), 0.0005, [("noloop", r(1 / math.sqrt(2 * 5), 3), 0.0005), ("row", r(1 / dA, 3), 0.0005),
                              ("noroot", r(1 / (dA * dH), 3), 0.0005)], label="Entry"),
      fb("A has 2 links and H has 5, so with loops $\\tilde d_A = 3$ and $\\tilde d_H = 6$: $1/\\sqrt{18} \\approx 0.236$.",
         "Add 1 to each degree for the loop, then divide by the square root of their product.",
         {"noloop": "That uses the degrees without loops, $1/\\sqrt{2 \\times 5}$. Each loop adds 1 to a degree.",
          "row": "That divides by A's degree alone, as $\\tilde{\\mathbf D}^{-1}\\tilde{\\mathbf A}$ does. $\\hat{\\mathbf A}$ "
                 "divides by the root of both degrees.",
          "noroot": "You divided by $3 \\times 6$ without the square root."})),
     ("Each firm holds one number: A 3, H $-1$ and F 2. A graph layer computes $\\operatorname{ReLU}(1.5\\,(\\hat{\\mathbf A}"
      "\\mathbf h)_A)$. What does it give for A? Give 2 decimal places.",
      num(r(out26, 2), 0.005, [("mean", r(1.5 * (3 - 1 + 2) / 3, 2), 0.005), ("sum", r(1.5 * (3 - 1 + 2), 2), 0.005)],
          label="Output"),
      fb("$(\\hat{\\mathbf A}\\mathbf h)_A = 3/3 - 1/\\sqrt{18} + 2/\\sqrt 6 \\approx 1 - 0.236 + 0.816 = 1.580$, and "
         "$1.5 \\times 1.580 = 2.37$, positive, so ReLU keeps it.",
         "Weight A, H and F by their entries in A's row of $\\hat{\\mathbf A}$, add, multiply by 1.5, then apply ReLU.",
         {"mean": "That is the plain mean of the three values. $\\hat{\\mathbf A}$ weights each by $1/\\sqrt{\\tilde d_A"
                  "\\tilde d_j}$, so F, of degree 2, counts for more than H.",
          "sum": "You added the three values unweighted."})),
     ("Stack two such layers. Counting F itself, how many firms' numbers reach F's output?",
      num(3, 0, [("onehop", 2, 0), ("all", 7, 0)], label="Firms"),
      fb("Two layers reach two links: F, then A, then H. The other firms are three links away.",
         "Each layer reaches one link further. List the firms within two links of F.",
         {"onehop": "That is one layer's reach. A second layer adds the neighbours of A.",
          "all": "B, C, D and E are three links from F, beyond two layers."}))],
    "$\\hat{\\mathbf A}$ divides each link by the root of both degrees, so a busy hub passes a smaller share than a "
    "quiet firm does. Each layer reaches one link further, so a two-layer net at F never hears from B to E."))

# 27 (representations l15): one step back, with fresh noise
b27, ab27, xt27, eh27, z27 = 0.1, 0.5, 0.8, -0.6, 0.5
al27 = 1 - b27
m27 = (xt27 - b27 / math.sqrt(1 - ab27) * eh27) / math.sqrt(al27)
x27 = m27 + math.sqrt(b27) * z27
items.append(item(
    "e-reverse-step", 4, ["rp-diffuse"], ["reverse-sampling"], 210, "One step back, with fresh noise",
    "At step $t$ of a sampler, $\\beta_t = 0.1$ and $\\bar\\alpha_t = 0.5$, in one coordinate. The point is $x_t = 0.8$, "
    "the net's noise guess is $\\hat\\epsilon = -0.6$, and the fresh draw is $z = 0.5$, with $\\sigma_t = \\sqrt{\\beta_t}$. "
    "The reverse step is $x_{t-1} = \\frac{1}{\\sqrt{\\alpha_t}}\\big(x_t - \\frac{\\beta_t}{\\sqrt{1 - \\bar\\alpha_t}}"
    "\\,\\hat\\epsilon\\big) + \\sigma_t z$.",
    "What is $x_{t-1}$? Give a decimal to 3 places.",
    num(r(x27, 3), 0.0005, [("noz", r(m27, 3), 0.0005),
                            ("abar", r((xt27 - b27 / math.sqrt(1 - ab27) * eh27) / math.sqrt(ab27) + math.sqrt(b27) * z27, 3), 0.0005),
                            ("noscale", r((xt27 - b27 * eh27) / math.sqrt(al27) + math.sqrt(b27) * z27, 3), 0.0005)],
        label="x_{t-1}"),
    fb("$\\alpha_t = 0.9$. The bracket is $0.8 + (0.1/0.7071)(0.6) \\approx 0.8849$; divided by $\\sqrt{0.9}$ it is 0.9327, "
       "and $\\sqrt{0.1} \\times 0.5 \\approx 0.1581$ brings it to 1.091.",
       "Find $\\alpha_t = 1 - \\beta_t$, work the bracket, divide by $\\sqrt{\\alpha_t}$, then add $\\sigma_t z$.",
       {"noz": "That is the mean of $x_{t-1}$. This is not the last step, so add $\\sigma_t z \\approx 0.1581$.",
        "abar": "You divided by $\\sqrt{\\bar\\alpha_t}$. One reverse step undoes one step's shrink, $\\sqrt{\\alpha_t}$.",
        "noscale": "You subtracted $\\beta_t\\hat\\epsilon$ without dividing by $\\sqrt{1 - \\bar\\alpha_t}$."}),
    "The bracket removes one step's share of the predicted noise, and dividing by $\\sqrt{\\alpha_t}$ undoes one step's "
    "shrink. The fresh $\\sigma_t z$ keeps the samples spread and takes this step to 1.091; only the step from $t = 1$ leaves it out."))

# 28 (representations l6): what two codes leave out
v1 = np.array([1.0, 1.0, 1.0]) / math.sqrt(3)
v2 = np.array([1.0, -1.0, 0.0]) / math.sqrt(2)
v3 = np.array([1.0, 1.0, -2.0]) / math.sqrt(6)
x28 = np.array([2.0, 0.0, -1.0])
p28 = [(x28 @ v) ** 2 for v in (v1, v2, v3)]
items.append(item(
    "e-ae-dropped-part", 4, ["rp-autoenc"], ["linear-autoencoder"], 210, "What two codes leave out",
    "Three bonds' centred returns have covariance eigenvectors $\\mathbf v_1 = (1, 1, 1)/\\sqrt 3$, "
    "$\\mathbf v_2 = (1, -1, 0)/\\sqrt 2$ and $\\mathbf v_3 = (1, 1, -2)/\\sqrt 6$, in falling order of variance. "
    "The best two-code linear autoencoder keeps a day's parts along $\\mathbf v_1$ and $\\mathbf v_2$. One day is "
    "$\\mathbf x = (2, 0, -1)$.",
    "What is that day's squared rebuild distance? Give 4 decimal places.",
    num(r(p28[2], 4), 0.0001, [("onecode", r(p28[1] + p28[2], 4), 0.0001), ("whole", r(x28 @ x28, 4), 0.0001),
                               ("kept", r(p28[0] + p28[1], 4), 0.0001)], label="Squared distance"),
    fb("The dropped part is along $\\mathbf v_3$: $\\mathbf x \\cdot \\mathbf v_3 = (2 + 0 + 2)/\\sqrt 6$, and its square is "
       "$16/6 \\approx 2.6667$.",
       "Project the day on the eigenvector the code drops, then square.",
       {"onecode": "That drops $\\mathbf v_2$ as well, as one code would. Two codes keep $\\mathbf v_1$ and $\\mathbf v_2$.",
        "whole": "5 is the day's whole squared length. The rebuild keeps the parts along $\\mathbf v_1$ and $\\mathbf v_2$.",
        "kept": "That is the squared length the rebuild keeps, $1/3 + 2$. The distance is what it leaves out."}),
    "A linear autoencoder with $k$ codes rebuilds a day by its projection on the top $k$ eigenvectors. The distance is "
    "the squared length along the rest, 2.6667 for this day. Averaged over days it is the sum of the dropped eigenvalues, "
    "which one day can sit far above or below."))

# 29 (nn-train l11): the noise dropout adds
a29, p29 = 2.0, 0.2
mean29 = (1 - p29) * a29 / (1 - p29)
ex2_29 = (1 - p29) * (a29 / (1 - p29)) ** 2
var29 = ex2_29 - mean29 ** 2
items.append(parts(
    "e-dropout-spread", 4, ["nt-general"], ["dropout"], 210, "The noise dropout adds",
    "A hidden unit outputs 2 and trains with inverted dropout at $p = 0.2$: it is kept with chance 0.8 and scaled by "
    "$1/(1 - p)$, or zeroed.",
    "Dropout changes what a unit passes on in training.",
    [("What is its expected output in training? Give a decimal.",
      num(r(mean29, 4), 0.0005, [("noscale", r((1 - p29) * a29, 4), 0.0005), ("surv", r(a29 / (1 - p29), 4), 0.0005)],
          label="Mean"),
      fb("$0.8 \\times 2/0.8 + 0.2 \\times 0 = 2$: inverted dropout keeps the mean.",
         "Weight each outcome by its chance: kept and scaled, or zeroed.",
         {"noscale": "1.6 is the unscaled mean, $0.8 \\times 2$. Survivors are scaled by $1/0.8$.",
          "surv": "2.5 is what a survivor passes on. One time in five it passes 0."})),
     ("What is the variance of its training output? Give a decimal.",
      num(r(var29, 4), 0.0005, [("noscale", r(a29 ** 2 * p29 * (1 - p29), 4), 0.0005), ("second", r(ex2_29, 4), 0.0005),
                                ("p", r(a29 ** 2 * p29, 4), 0.0005)], label="Variance"),
      fb("$E[X^2] = 0.8 \\times 2.5^2 = 5$, so the variance is $5 - 2^2 = 1$. In general it is $a^2 p/(1 - p)$.",
         "Find $E[X^2]$ over the two outcomes, then subtract the square of the mean.",
         {"noscale": "That is the variance before scaling, $4 \\times 0.2 \\times 0.8$. Scaling by $1/0.8$ multiplies it "
                     "by $1/0.64$.",
          "second": "5 is $E[X^2]$. Subtract the square of the mean, 4.",
          "p": "That is $a^2 p$. Divide by $1 - p$ as well."})),
     ("What happens to that variance as $p$ rises towards 1?",
      choice([opt("grows", "It grows without bound, like $4p/(1 - p)$", correct=True),
              opt("shrinks", "It falls to 0, since fewer units pass", "Fewer survive, but each survivor is scaled by "
                  "$1/(1 - p)$, which grows without bound."),
              opt("flat", "It stays at 1, since the mean stays at 2", "The mean is held at 2, but the spread around it "
                  "is $4p/(1 - p)$, which depends on $p$."),
              opt("peak", "It peaks at $p = 0.5$, then falls", "That is the shape of $p(1 - p)$, the unscaled mask's "
                  "variance. The scale $1/(1 - p)$ keeps it rising.")]),
      fb("$a^2 p/(1 - p)$ with $a = 2$ is $4p/(1 - p)$, which grows without bound as $p$ nears 1.",
         "Read the general form from part 2 as a function of $p$."))],
    "Inverted dropout keeps every unit's mean but adds noise of variance $a^2 p/(1 - p)$. That noise is the regulariser, "
    "and at $p$ near 1 it swamps the signal."))

# ================================================================ difficulty 5
# 30 (sequence l2, l4): backprop through two steps, then clip
w30, h0_30, x1_30, x2_30 = 0.5, 1.0, 0.0, 0.2
h1_30 = math.tanh(w30 * h0_30 + x1_30)
h2_30 = math.tanh(w30 * h1_30 + x2_30)
H1, H2 = r(h1_30, 4), r(h2_30, 4)                # printed in part 2
G30 = (1 - H2 ** 2) * (H1 + w30 * (1 - H1 ** 2) * h0_30)
GP = r(G30, 4)                                   # printed in part 3
dL30 = 2 * (H2 - 1) * GP
clip30 = 0.5
g30 = dL30 * min(1.0, clip30 / abs(dL30))
w_new30 = w30 - 0.2 * g30
items.append(parts(
    "e-bptt-two-steps", 5, ["sqn-rnn"], ["bptt"], 360, "Backprop through two steps",
    "A one-unit tanh net runs $h_t = \\tanh(w\\,h_{t-1} + x_t)$ with $w = 0.5$, from $h_0 = 1$, on the inputs "
    "$x_1 = 0$ and $x_2 = 0.2$. The weight $w$ is shared by both steps.",
    "Run it forward, then back.",
    [("What is $h_2$? Give 4 decimal places.",
      num(H2, 0.0001, [("notanh", r(w30 * (w30 * h0_30 + x1_30) + x2_30, 4), 0.0001), ("one-step", H1, 0.0001)], label="h2"),
      fb("$h_1 = \\tanh 0.5 \\approx 0.4621$, then $h_2 = \\tanh(0.2311 + 0.2) = \\tanh 0.4311 \\approx 0.4062$.",
         "Apply the update twice, with $x_1$ and then $x_2$.",
         {"notanh": "You left out the tanh: $h_t$ is the tanh of the sum.",
          "one-step": "That is $h_1$. Run the update once more, with $x_2 = 0.2$."})),
     (f"Using $h_1 = {H1}$ and $h_2 = {H2}$, what is $\\partial h_2/\\partial w$? Give 4 decimal places.",
      num(GP, 0.0001, [("last", r((1 - H2 ** 2) * H1, 4), 0.0001), ("noinner", r((1 - H2 ** 2) * (H1 + w30 * h0_30), 4), 0.0001),
                       ("noouter", r(H1 + w30 * (1 - H1 ** 2) * h0_30, 4), 0.0001)], label="dh2/dw"),
      fb("$w$ acts at both steps: $\\partial h_2/\\partial w = (1 - h_2^2)\\big(h_1 + w(1 - h_1^2)h_0\\big) \\approx "
         "0.835 \\times 0.8553 \\approx 0.7142$.",
         "Unroll: $w$ enters at step 2 directly and at step 1 through $h_1$. Add the two paths.",
         {"last": "That keeps only step 2's use of $w$. Step 1 used $w$ too, and its effect reaches $h_2$ through "
                  "$w(1 - h_1^2)$.",
          "noinner": "You carried step 1's term back without its own tanh slope, $1 - h_1^2 \\approx 0.7865$.",
          "noouter": "You left out step 2's slope, $1 - h_2^2 \\approx 0.835$, which multiplies both terms."})),
     (f"The loss is $(h_2 - 1)^2$. Using $\\partial h_2/\\partial w = {GP}$, what is $\\partial L/\\partial w$? Give 4 "
      "decimal places.",
      num(r(dL30, 4), 0.0001, [("sign", r(-dL30, 4), 0.0001), ("nochain", r(2 * (H2 - 1), 4), 0.0001),
                               ("half", r(dL30 / 2, 4), 0.0001)], label="dL/dw"),
      fb("$\\partial L/\\partial w = 2(h_2 - 1)\\,\\partial h_2/\\partial w = 2(-0.5938)(0.7142) \\approx -0.8482$.",
         "Chain the loss's slope in $h_2$ with $\\partial h_2/\\partial w$.",
         {"sign": "$h_2$ is below the target 1, so raising $w$ lowers the loss: the slope is negative.",
          "nochain": "That is $\\partial L/\\partial h_2$. Multiply by $\\partial h_2/\\partial w$.",
          "half": "The derivative of $(h_2 - 1)^2$ is $2(h_2 - 1)$."})),
     ("The gradient is clipped by norm at $c = 0.5$, then one step of size 0.2 is taken. What is the new $w$? Give a decimal.",
      num(r(w_new30, 4), 0.0005, [("noclip", r(w30 - 0.2 * dL30, 4), 0.0005), ("sign", r(w30 + 0.2 * g30, 4), 0.0005)],
          label="New w"),
      fb("The gradient's size, 0.8482, is above 0.5, so it is cut to $-0.5$, and the step gives $0.5 + 0.2 \\times 0.5 = 0.6$.",
         "Clip first: scale the gradient to size $c$ if it is larger. Then step against it.",
         {"noclip": "That steps with the full gradient. Its size, 0.8482, is above $c = 0.5$, so it is scaled down first.",
          "sign": "A step goes against the gradient: the gradient is negative, so $w$ rises."}))],
    "A shared weight collects one term per step it acts at, each carried to the output by the later steps' slopes and "
    "weights. Clipping caps the size of the step but keeps its direction."))

# ================================================================ the two code items (difficulty 5)
exec(open(os.path.join(HERE, 'code_items.py'), encoding='utf8').read())

# ================================================================ the exam
COURSES = ['nn-train', 'cnn', 'sequence', 'representations']
skills = {}
for c in COURSES:
    with open(os.path.join(APP, 'content', 'courses', c, 'course.json'), encoding='utf8') as f:
        skills.update(json.load(f)['skills'])
doc = {"id": "topic-2.7", "topic": "2.7", "name": "Deep learning", "minutes": 105, "pass": 0.7, "skills": skills,
       "items": items}
with open(OUT, 'w', encoding='utf8') as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)
    f.write('\n')
paces = sum(it['pace'] for it in items)
print(f'wrote {OUT}: {len(items)} items, paces {paces} s = {paces / 60:.1f} min')
