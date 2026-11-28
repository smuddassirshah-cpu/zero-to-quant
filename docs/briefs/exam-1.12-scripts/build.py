"""Build app/content/exams/topic-1.12.json (topic 1.12, Neural networks from scratch: info L1 to L3, backprop L1 to L4,
makemore L1 to L3).

Route A for every key: plain floats and the loops below. check_numbers.py recomputes each value by a second route (exact
Fractions, series for the logs where they can be exact, an independent backward pass and bigram count, and both code
items run in CPython with the engine's shared namespace) and asserts it at its path in the written file.
Run from anywhere: python3 docs/briefs/exam-1.12-scripts/build.py
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.join(HERE, '..', '..', '..', 'app')
OUT = os.path.join(APP, 'content', 'exams', 'topic-1.12.json')
LN2 = math.log(2)


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


def H(p):
    return -sum(x * math.log2(x) for x in p if x > 0)


def CE(p, q):
    return -sum(a * math.log2(b) for a, b in zip(p, q) if a > 0)


def softmax(z):
    m = max(z)
    e = [math.exp(v - m) for v in z]
    s = sum(e)
    return [v / s for v in e]


items = []

# ================================================================ difficulty 2
# 1 (info l1): surprise of a rare move
p1 = 0.0125
s1 = -math.log2(p1)
items.append(item(
    "e-tail-move-bits", 2, ["if-surprise"], ["surprise"], 60, "A rare move",
    "A risk model gives a one-day move of three standard deviations a chance of 0.0125.",
    "How many bits of surprise does such a day carry? Give a decimal to 2 places.",
    num(r(s1, 4), 0.005, [("nats", r(-math.log(p1), 4), 0.005), ("log10", r(-math.log10(p1), 4), 0.005),
                          ("reciprocal", 80, 0.005)], label="Surprise (bits)"),
    fb("$-\\log_2 0.0125 = \\log_2 80 \\approx 6.32$ bits.",
       "Take minus the log of the chance, in base 2.",
       {"nats": "That is the surprise in nats, from $\\ln$. Divide by $\\ln 2$ to get bits.",
        "log10": "You used the base 10 log. Bits need the base 2 log.",
        "reciprocal": "That is one over the chance. The surprise is its log in base 2."}),
    "An outcome of chance $p$ carries $-\\log_2 p$ bits. Here $1/0.0125 = 80$, and $\\log_2 80 \\approx 6.32$. "
    "That is a little more than the 6 bits of a 1 in 64 event."))

# 2 (makemore l1): pairs from wrapped tickers
n2, letters2 = 400, 1530
items.append(item(
    "e-ticker-pairs", 2, ["mk-bigram"], ["bigram-counts"], 60, "Pairs from tickers",
    "A desk builds a bigram table from 400 ticker symbols holding 1,530 letters between them. "
    "Each ticker is wrapped in a start mark and an end mark before its pairs are counted.",
    "How many pairs does the table count in all?",
    num(letters2 + n2, 0, [("no-end", letters2, 0), ("marks-twice", letters2 + 2 * n2, 0),
                           ("inside-only", letters2 - n2, 0)], label="Pairs"),
    fb("A ticker of $n$ letters gives $n + 1$ pairs, so the table counts $1{,}530 + 400 = 1{,}930$.",
       "Count the pairs of one wrapped ticker, then add over all 400.",
       {"no-end": "You counted one pair per letter. The pair that ends at the end mark adds one more per ticker.",
        "marks-twice": "You added two pairs per ticker, one for each mark. Wrapping adds one symbol to the pairs, not two.",
        "inside-only": "You counted only the pairs between two letters. The pairs that start or stop at a mark count too."}),
    "Wrapped as `.ibm.`, a ticker of 3 letters gives the 4 pairs `.i`, `ib`, `bm` and `m.`: one more than its letters. "
    "Over 400 tickers that is $1{,}530 + 400 = 1{,}930$ pairs."))

# 3 (backprop l2, l3): a slippage cost with a subtraction box
q3, pf3, mid3 = 400, 50.30, 50.25
items.append(item(
    "e-slippage-grad", 2, ["bp-chain"], ["path-gradient"], 75, "A cost with two boxes",
    "A desk draws its slippage cost as two boxes: $s = p - m$, then $C = qs$. "
    "Today $q = 400$ shares, the fill price $p$ is £50.30 and the mid $m$ is £50.25, so the cost $C$ is £20.",
    "What is $\\partial C/\\partial m$, in pounds per pound of the mid?",
    num(-q3, 0, [("sign", q3, 0), ("other-input", r(pf3 - mid3, 4), 0.0005), ("value", 20, 0)], label="Gradient"),
    fb("The product box passes $s$ its other input, 400, and the subtraction box multiplies by $-1$: $-400$.",
       "Walk back from $C$ with 1, multiplying one local derivative per arrow.",
       {"sign": "The subtraction box passes $-1$ to $m$, not 1. A higher mid lowers the cost.",
        "other-input": "That is $s = p - m$, the product box's gift to $q$. The path to $m$ goes through $s$.",
        "value": "That is the cost itself, £20. The gradient is a rate, not a value."}),
    "Walking back from $C$ starts with 1. The product box sends $s$ the other input, $q = 400$, and the subtraction box "
    "multiplies by $\\partial s/\\partial m = -1$. So $\\partial C/\\partial m = 400 \\times (-1) = -400$."))

# 4 (info l7): perplexity back to a loss
items.append(item(
    "e-perplexity-sixteen", 2, ["if-likelihood"], ["perplexity"], 60, "From perplexity back to a loss",
    "A vendor reports that its character model has a perplexity of 16 on held-out text.",
    "What is the model's average loss, in nats per character? Give a decimal to 4 places.",
    num(r(math.log(16), 4), 0.00005, [("bits", 4, 0.00005), ("log10", r(math.log10(16), 4), 0.00005),
                                      ("inverse", r(1 / 16, 4), 0.00005)], label="Loss (nats)"),
    fb("Perplexity is $e^{H}$ for a loss $H$ in nats, so $H = \\ln 16 \\approx 2.7726$.",
       "Undo the exponential that turned the loss into a perplexity.",
       {"bits": "That is the loss in bits, $\\log_2 16$. Multiply by $\\ln 2$ for nats.",
        "log10": "You used the base 10 log. Nats use $\\ln$.",
        "inverse": "That is one over the perplexity. Take its log instead."}),
    "Perplexity undoes the log of an average loss: $16 = e^{H}$ in nats and $16 = 2^{H}$ in bits. "
    "So the loss is $\\ln 16 \\approx 2.7726$ nats, which is the same as $\\log_2 16 = 4$ bits."))

# 5 (backprop l10): parameter count of a 6-10-3 network
items.append(item(
    "e-count-six-ten-three", 2, ["bp-networks"], ["parameter-count"], 60, "Sizing a small network",
    "A desk's classifier is a 6-10-3 network: six inputs, one hidden layer of ten tanh neurons and three outputs. "
    "Every neuron has a bias.",
    "How many parameters does it have?",
    num(7 * 10 + 11 * 3, 0, [("edges", 6 * 10 + 10 * 3, 0), ("one-bias", 6 * 10 + 10 * 3 + 1, 0),
                             ("hidden-only", 7 * 10, 0)], label="Parameters"),
    fb("$7 \\times 10 + 11 \\times 3 = 70 + 33 = 103$.",
       "Count each layer's weights and biases, then add the layers.",
       {"edges": "You counted the weights only. Each of the 13 neurons has a bias as well.",
        "one-bias": "You gave the network one bias. Each neuron has its own.",
        "hidden-only": "That is the hidden layer alone. Add the output layer's $11 \\times 3$."}),
    "A layer from $m$ inputs to $k$ neurons holds $(m + 1)k$ parameters. "
    "Here that is $7 \\times 10 = 70$ for the hidden layer and $11 \\times 3 = 33$ for the outputs, 103 in all."))

# 6 (makemore l9): a draw that lands on a running total
row6 = [("end", 0.25), ("r", 0.35), ("x", 0.15), ("y", 0.25)]
items.append(item(
    "e-draw-on-a-total", 2, ["mk-eval"], ["sampling-rule"], 60, "A draw on a running total",
    "After the context `ma`, a trained model gives the next symbol these chances, in this order: "
    "end 0.25, r 0.35, x 0.15 and y 0.25. The sampler draws $u = 0.6$.",
    "Which symbol does the course's sampling rule pick?",
    choice([opt("x", "x", correct=True),
            opt("r", "r", "The running total after r is exactly 0.6, not above it. The rule wants a total strictly above $u$."),
            opt("y", "y", "The total after x is already 0.75, above 0.6. The draw stops there."),
            opt("end", "The end mark", "The end mark's total is 0.25, below 0.6, so the draw goes on.")]),
    fb("The running totals are 0.25, 0.6, 0.75 and 1, and the first strictly above 0.6 is x's.",
       "Lay the chances end to end and take the first running total strictly above $u$."),
    "The running totals are 0.25, 0.6, 0.75 and 1. A $u$ that equals r's total belongs to the next symbol, "
    "as `searchsorted(..., side=\"right\")` gives, so the draw writes x."))

# ================================================================ difficulty 3
# 7 (info l2): entropy of five order kinds
p7 = [0.5, 0.25, 0.125, 0.0625, 0.0625]
H7 = H(p7)
items.append(item(
    "e-order-kinds-entropy", 3, ["if-surprise"], ["entropy"], 90, "Five kinds of order",
    "An exchange logs five kinds of order message with chances $\\tfrac12, \\tfrac14, \\tfrac18, \\tfrac1{16}$ and $\\tfrac1{16}$.",
    "What is the entropy of the message kind, in bits? Give a decimal to 3 places.",
    num(r(H7, 4), 0.0005, [("equal", r(math.log2(5), 4), 0.0005), ("nats", r(H7 * LN2, 4), 0.0005),
                           ("sum", 14, 0.0005), ("mean", 2.8, 0.0005)], label="Entropy (bits)"),
    fb("$0.5 + 0.5 + 0.375 + 0.25 + 0.25 = 1.875$ bits.",
       "Weigh each kind's surprise by its chance, then add.",
       {"equal": "That is the entropy of five equal chances, the most five kinds can carry. These chances are unequal.",
        "nats": "That is the entropy in nats. Use $\\log_2$ for bits.",
        "sum": "You added the five surprises without weighing them by their chances.",
        "mean": "You averaged the five surprises equally. Weigh each one by its own chance."}),
    "The surprises are 1, 2, 3, 4 and 4 bits. Weighed by their chances they give $0.5 + 0.5 + 0.375 + 0.25 + 0.25 = 1.875$ bits, "
    "below the $\\log_2 5 \\approx 2.322$ of five equal chances."))

# 8 (info l3): Huffman's average length, merges given
p8, l8 = [0.4, 0.25, 0.2, 0.1, 0.05], [1, 2, 3, 4, 4]
avg8 = sum(a * b for a, b in zip(p8, l8))
items.append(item(
    "e-huffman-five-types", 3, ["if-codes"], ["huffman"], 120, "Huffman on five message types",
    "A feed's five message types have chances 0.4, 0.25, 0.2, 0.1 and 0.05. "
    "Huffman's method merges 0.05 with 0.1, then 0.15 with 0.2, then 0.25 with 0.35, and last 0.4 with 0.6.",
    "How many bits does Huffman's code spend per message on average? Give a decimal to 2 places.",
    num(r(avg8, 4), 0.005, [("entropy", r(H(p8), 4), 0.005), ("fixed", 3, 0.005), ("unweighted", 2.8, 0.005)],
        label="Average length (bits)"),
    fb("The word lengths are 1, 2, 3, 4 and 4, so the average is $0.4 + 0.5 + 0.6 + 0.4 + 0.2 = 2.1$ bits.",
       "Find each type's depth from the merges, then weigh the depths by the chances.",
       {"entropy": "That is the entropy, the floor no prefix code beats. Huffman's code sits a little above it.",
        "fixed": "That is a fixed code of 3 bits for five types. Huffman gives the common types shorter words.",
        "unweighted": "You averaged the five word lengths equally. Weigh each by its type's chance."}),
    "Each merge puts one more bit on every type inside it, so 0.05 and 0.1 end 4 deep, 0.2 three deep, 0.25 two deep and 0.4 one deep. "
    "Weighed by the chances, that is $0.4 \\times 1 + 0.25 \\times 2 + 0.2 \\times 3 + 0.15 \\times 4 = 2.1$ bits, within one bit of the entropy, 2.04."))

# 9 (info l4): zlib against a model, in bits per symbol
n9, model9, zb9 = 600000, 3.2, 260000
z9 = zb9 * 8 / n9
items.append(item(
    "e-zlib-on-ticks", 3, ["if-codes"], ["compression"], 90, "zlib against a model",
    "A tick log holds 600,000 symbols. A model of the log spends 3.2 bits per symbol, and zlib packs the whole log into 260,000 bytes.",
    "How many bits per symbol does zlib spend? Give a decimal to 2 places.",
    num(r(z9, 4), 0.005, [("bytes", r(zb9 / n9, 4), 0.005), ("inverse", r(n9 / (zb9 * 8), 4), 0.005),
                          ("model", 3.2, 0.005)], label="Bits per symbol"),
    fb("$260{,}000 \\times 8 = 2{,}080{,}000$ bits over 600,000 symbols is about 3.47 bits a symbol.",
       "Turn the bytes into bits, then share them over the symbols.",
       {"bytes": "That is bytes per symbol. A byte is 8 bits.",
        "inverse": "You divided the wrong way round: that is symbols per bit.",
        "model": "That is the model's cost, not zlib's. Work zlib's out from its 260,000 bytes."}),
    "zlib spends $2{,}080{,}000 / 600{,}000 \\approx 3.47$ bits a symbol. "
    "A code built on the model would need $600{,}000 \\times 3.2 / 8 = 240{,}000$ bytes, so the model's code is the shorter one."))

# 10 (info l8, l6): the gap above the least log loss is a KL divergence, in nats
ph10, q10 = [0.2, 0.3, 0.5], [0.2, 0.4, 0.4]
gap10 = sum(a * math.log(a / b) for a, b in zip(ph10, q10))
rev10 = sum(b * math.log(b / a) for a, b in zip(ph10, q10))
items.append(item(
    "e-fixed-forecast-gap", 3, ["if-likelihood", "if-cross"], ["likelihood-gap"], 120, "A fixed forecast's extra loss",
    "Over 100 days a share fell 20 times, held flat 30 times and rose 50 times. "
    "A desk's fixed forecast gives fall, flat and rise the chances 0.2, 0.4 and 0.4.",
    "How many nats a day does the forecast's average negative log-likelihood sit above the least that any forecast reaches? Give a decimal to 4 places.",
    num(r(gap10, 6), 0.00005, [("bits", r(gap10 / LN2, 6), 0.00005), ("reverse", r(rev10, 6), 0.00005),
                               ("total", r(100 * gap10, 4), 0.00005), ("floor", r(H(ph10) * LN2, 4), 0.00005)],
        label="Gap (nats)"),
    fb("The data's shares are (0.2, 0.3, 0.5), and the gap is $0.3\\ln\\tfrac{0.3}{0.4} + 0.5\\ln\\tfrac{0.5}{0.4} \\approx 0.0253$ nats.",
       "Split the average loss into the data's entropy plus a divergence.",
       {"bits": "That is the gap in bits. The question asks for nats, with $\\ln$.",
        "reverse": "You weighed by the forecast's chances, $D(q \\| \\hat p)$. The days come from the data's shares, so weigh by those.",
        "total": "That is the gap over all 100 days. The question asks for it per day.",
        "floor": "That is the least loss itself, $H(\\hat p)$ in nats. The question asks how far above it the forecast sits."}),
    "The average negative log-likelihood is $H(\\hat p) + D(\\hat p \\| q)$, and the least is $H(\\hat p)$, reached at $q = \\hat p$. "
    "So the gap is $D(\\hat p \\| q) \\approx 0.0253$ nats a day. The fall term drops out, since both give a fall 0.2."))

# 11 (info l9, l10): mutual information of a 2 by 2 table
J11 = [[0.3, 0.1], [0.2, 0.4]]
px11 = [sum(rw) for rw in J11]
py11 = [sum(c) for c in zip(*J11)]
I11 = sum(J11[i][j] * math.log2(J11[i][j] / (px11[i] * py11[j])) for i in range(2) for j in range(2))
Hxy11 = H([v for rw in J11 for v in rw])
items.append(item(
    "e-flag-table-mi", 3, ["if-mutual"], ["mutual-information"], 150, "A news flag and the next day",
    "A news flag and the next day's sign have these joint chances. Flag on: up 0.3, down 0.1. Flag off: up 0.2, down 0.4.",
    "What is the mutual information between the flag and the sign, in bits? Give a decimal to 3 places.",
    num(r(I11, 5), 0.0006, [("cond", r(1 - I11, 4), 0.0005), ("nats", r(I11 * LN2, 4), 0.0005),
                            ("joint", r(Hxy11, 4), 0.0005)], label="Information (bits)"),
    fb("The margins are (0.4, 0.6) and (0.5, 0.5), and $\\sum p \\log_2 \\tfrac{p}{p_X p_Y}$ over the four cells is about 0.125 bits.",
       "Compare each cell with its row total times its column total.",
       {"cond": "That is the doubt about the sign left after reading the flag, $H(Y \\mid X)$. Subtract it from $H(Y) = 1$.",
        "nats": "That is the information in nats. Use $\\log_2$ for bits.",
        "joint": "That is the joint entropy $H(X, Y)$. Mutual information is $H(X) + H(Y) - H(X, Y)$."}),
    "Mutual information is the KL divergence of the joint table from the product of its margins. "
    "Each product is a row total times 0.5, so the four ratios are 1.5, 0.5, $\\tfrac23$ and $\\tfrac43$. "
    "Weighed by the cells and added, they give about 0.125 bits a day."))

# 12 (info l12): plug-in bias correction, five states and three outcomes
kx12, ky12, n12, est12 = 5, 3, 500, 0.015
bias12 = (kx12 - 1) * (ky12 - 1) / (2 * n12 * LN2)
items.append(item(
    "e-five-state-bias", 3, ["if-mutual"], ["plug-in-bias"], 90, "A five-state signal on 500 days",
    "A signal with 5 states is scored against the next day's move, fall, flat or rise, on 500 days. "
    "Read straight off the sample's table, the signal shows 0.015 bits of mutual information.",
    "How many bits are left once the plug-in bias is taken off? Give a decimal to 4 places.",
    num(r(est12 - bias12, 6), 0.00005,
        [("no-ln2", r(est12 - 8 / 1000, 4), 0.00005), ("no-minus-one", r(est12 - 15 / (1000 * LN2), 6), 0.00005),
         ("bias", r(bias12, 6), 0.00005), ("two-outcomes", r(est12 - 4 / (1000 * LN2), 6), 0.00005)],
        label="Corrected (bits)"),
    fb("The bias is $\\tfrac{4 \\times 2}{1000 \\ln 2} \\approx 0.0115$ bits, which leaves about 0.0035.",
       "Subtract $\\tfrac{(k_X - 1)(k_Y - 1)}{2n \\ln 2}$ from the plug-in figure.",
       {"no-ln2": "You left out the $\\ln 2$. The correction in bits divides by $2n\\ln 2$.",
        "no-minus-one": "You used $5 \\times 3$. The correction uses one less than each count of states: $4 \\times 2$.",
        "bias": "That is the bias itself. Subtract it from 0.015.",
        "two-outcomes": "You counted two outcomes. The move has three: fall, flat and rise."}),
    "The plug-in bias is $\\tfrac{(k_X - 1)(k_Y - 1)}{2n\\ln 2} = \\tfrac{8}{1000 \\ln 2} \\approx 0.0115$ bits. "
    "Subtracting it leaves about $0.015 - 0.0115 = 0.0035$ bits, so most of the plug-in figure was the sample's own noise."))

# 13 (backprop l4): a four-box chain through exp and log
w13, x13 = 0.5, 2.0
u13 = w13 * x13
s13 = 1 + math.exp(u13)
g13 = math.exp(u13) / s13 * x13
items.append(item(
    "e-smooth-payoff-grad", 3, ["bp-chain"], ["path-gradient"], 120, "A smooth payoff",
    "A smoothed payoff is drawn as four boxes: $u = wx$, $v = e^u$, $s = 1 + v$, then $L = \\ln s$. Take $w = 0.5$ and $x = 2$.",
    "What is $\\partial L/\\partial w$? Give a decimal to 4 places.",
    num(r(g13, 6), 0.00005, [("no-x", r(g13 / x13, 6), 0.00005), ("used-w", r(g13 / x13 * w13, 6), 0.00005),
                             ("no-log", r(math.exp(u13) * x13, 6), 0.00005)], label="Gradient"),
    fb("$\\tfrac1s \\times 1 \\times e^{u} \\times x = \\tfrac{2.7183}{3.7183} \\times 2 \\approx 1.4621$.",
       "Multiply the four local derivatives on the path from $L$ back to $w$.",
       {"no-x": "You stopped at $u$. The product box $u = wx$ passes $w$ the other input, $x = 2$.",
        "used-w": "The product box passes $w$ the other input, $x$, not $w$ itself.",
        "no-log": "You left out the log box. Its local derivative is $1/s$."}),
    "Along the one path the local derivatives are $\\tfrac1s$, 1, $e^u$ and $x$. "
    "At $u = 1$ and $s = 1 + e \\approx 3.7183$ their product is $\\tfrac{2.7183}{3.7183} \\times 2 \\approx 1.4621$."))

# 14 (backprop l5): a value that feeds two boxes
x14, y14 = -2.0, 3.0
q14 = x14 * y14 + 1
d14 = q14 + x14 * y14
items.append(item(
    "e-two-uses-of-x", 3, ["bp-backward"], ["branch-gradient"], 120, "A value used twice",
    "A graph computes $p = xy$, $q = p + 1$, then $z = qx$, at $x = -2$ and $y = 3$.",
    "What is $\\partial z/\\partial x$?",
    num(d14, 0, [("direct", q14, 0), ("through-p", x14 * y14, 0), ("sign", -d14, 0)], label="Gradient"),
    fb("The direct arrow gives $q = -5$ and the path through $p$ gives $x \\times y = -6$: $-11$ in all.",
       "The value $x$ feeds two boxes. Add the contributions of both paths.",
       {"direct": "That is the direct arrow into $z = qx$ only. The path through $p$ and $q$ adds $x \\times y$.",
        "through-p": "That is the path through $p$ only. The product $z = qx$ also sends $x$ the value $q$ directly.",
        "sign": "Both contributions are negative here: $q = -5$ and $xy = -6$."}),
    "Because $x$ feeds two boxes, its gradient is the sum of two paths. "
    "The product $z = qx$ sends $q = -5$ straight back, and the path through $p$ gives $\\partial z/\\partial q \\times y = -2 \\times 3 = -6$. "
    "Together they make $-11$, which matches $z = x^2y + x$ and $2xy + 1 = -11$."))

# 15 (backprop l8): backward() with no seen set
e15 = 2.0 * 3
true15 = 2 * e15 * 3
items.append(item(
    "e-no-seen-set", 3, ["bp-autograd"], ["autograd-bug"], 120, "A search with no memory",
    "Ali's `backward()` builds its order with `build(v)`, which builds each parent of `v` and then appends `v`, but it keeps no `seen` set. "
    "He runs `x = Value(2.0)`, `e = x * 3`, `y = e * e` and then `y.backward()`, with every gradient at 0.",
    "What does `x.grad` show afterwards?",
    num(2 * true15, 0, [("true", true15, 0), ("e-grad", 2 * e15, 0)], label="x.grad"),
    fb("The order lists $e$ twice, so its closure runs twice and adds $3 \\times 12 = 36$ each time: 72.",
       "Write out the order `build(y)` makes. How many times does $e$ appear?",
       {"true": "That is the true $\\partial y/\\partial x$. Without `seen`, $e$ enters the order once per arrow into $y$, and its closure runs each time.",
        "e-grad": "That is `e.grad` after $y$'s closure. $e$'s own closure then passes it back to $x$, times 3."}),
    "Without `seen`, `build(e)` runs once for each of the two arrows from $e$ into $y$, so $e$ appears twice in the order. "
    "Each run of $e$'s closure adds $3 \\times 12 = 36$ to `x.grad`, giving 72 instead of $\\partial y/\\partial x = 2e \\times 3 = 36$. "
    "The `seen` set makes each node appear once."))

# 16 (backprop l9, l11): one gradient step for a neuron
w16, b16, x16, t16, lr16 = 0.2, 0.2, 1.5, 1.0, 0.1
n16 = w16 * x16 + b16
o16 = math.tanh(n16)
g16 = 2 * (o16 - t16) * (1 - o16 ** 2) * x16
items.append(item(
    "e-neuron-one-step", 3, ["bp-networks"], ["gradient-step"], 150, "One step for a neuron",
    "A neuron computes $o = \\tanh(wx + b)$ with $w = 0.2$ and $b = 0.2$, on one point $x = 1.5$ with target 1. "
    "The loss is $L = (o - 1)^2$ and the step size is 0.1.",
    "What is $w$ after one gradient-descent step? Give a decimal to 4 places.",
    num(r(w16 - lr16 * g16, 6), 0.00005,
        [("uphill", r(w16 + lr16 * g16, 6), 0.00005),
         ("no-x", r(w16 - lr16 * g16 / x16, 6), 0.00005),
         ("slope-of-n", r(w16 - lr16 * 2 * (o16 - t16) * (1 - n16 ** 2) * x16, 6), 0.00005),
         ("no-two", r(w16 - lr16 * g16 / 2, 6), 0.00005)], label="New w"),
    fb("$o = \\tanh 0.5 \\approx 0.4621$, so $\\partial L/\\partial w = 2(o - 1)(1 - o^2)x \\approx -1.2691$ and $w$ becomes about 0.3269.",
       "Find $o$, then multiply $2(o - 1)$, the tanh slope $1 - o^2$ and $x$. Step against the gradient.",
       {"uphill": "You stepped up the gradient. Gradient descent subtracts the step size times the gradient.",
        "no-x": "You left out the product box: $\\partial n/\\partial w = x = 1.5$.",
        "slope-of-n": "You used $1 - n^2$ for the tanh slope. The slope is $1 - o^2$, from the output.",
        "no-two": "You left out the 2 from the square: $\\partial L/\\partial o = 2(o - 1)$."}),
    "The forward pass gives $n = 0.5$ and $o \\approx 0.4621$. "
    "The gradient is $2(o - 1)(1 - o^2)x \\approx -1.0758 \\times 0.7864 \\times 1.5 \\approx -1.2691$. "
    "One step gives $0.2 - 0.1 \\times (-1.2691) \\approx 0.3269$."))

# 17 (backprop l12): a gradient check by two bumps
up17, dn17, mid17, bp17, h17 = 0.693649, 0.692149, 0.692898, 0.7503, 0.001
cd17 = (up17 - dn17) / (2 * h17)
fd17 = (up17 - mid17) / h17
items.append(item(
    "e-check-by-bumps", 3, ["bp-check"], ["gradient-check"], 120, "A check by bumps",
    "Backpropagation gives one weight a gradient of 0.7503. Bumping that weight by $h = 0.001$ gives losses of 0.693649 above and 0.692149 below. "
    "The loss at the weight itself is 0.692898.",
    "What is the relative error between backpropagation and the central difference? Give 2 significant figures.",
    num(0.0004, 0.000005, [("absolute", 0.0003, 0.000005), ("forward", r(abs(bp17 - fd17) / fd17, 6), 0.000005)],
        label="Relative error"),
    fb("The central difference is $\\tfrac{0.693649 - 0.692149}{0.002} = 0.75$, and $\\tfrac{0.0003}{0.7503} \\approx 0.00040$.",
       "Form the central difference first, then divide the gap by the larger of the two gradients.",
       {"absolute": "That is the absolute gap. A relative error divides it by the larger gradient, 0.7503.",
        "forward": "You used the forward difference from the loss at the weight. A check uses the central difference."}),
    "The central difference is $\\tfrac{0.693649 - 0.692149}{0.002} = 0.75$. "
    "The relative error is $\\tfrac{|0.7503 - 0.75|}{0.7503} \\approx 0.00040$, far above the course's $10^{-6}$ bar, so this gradient needs a closer look."))

# 18 (backprop l13): the gradient for an input, G W^T
W18 = np.array([[1.0, -2.0], [0.5, 3.0], [-1.0, 4.0]])
G18 = np.array([[2.0, 1.0], [-1.0, 0.5]])
dX18 = G18 @ W18.T
items.append(item(
    "e-input-gradient-entry", 3, ["bp-arrays"], ["matmul-backward"], 150, "The gradient for an input",
    "A layer computes $\\mathbf{Y} = \\mathbf{X}\\mathbf{W}$, with $\\mathbf{X}$ of shape 2 by 3 and "
    "$$\\mathbf{W} = \\begin{pmatrix} 1 & -2 \\\\ 0.5 & 3 \\\\ -1 & 4 \\end{pmatrix}.$$ "
    "The incoming gradient is $$\\mathbf{G} = \\frac{\\partial L}{\\partial \\mathbf{Y}} = \\begin{pmatrix} 2 & 1 \\\\ -1 & 0.5 \\end{pmatrix}.$$",
    "What is $\\partial L/\\partial X_{23}$, the entry in row 2, column 3?",
    num(float(dX18[1, 2]), 0, [("row-1", float(dX18[0, 2]), 0), ("w-row-1", float(dX18[1, 0]), 0), ("sign", -float(dX18[1, 2]), 0)],
        label="Gradient"),
    fb("$G_{21}W_{31} + G_{22}W_{32} = (-1)(-1) + 0.5 \\times 4 = 3$.",
       "$\\partial L/\\partial \\mathbf{X} = \\mathbf{G}\\mathbf{W}^T$. Pair a row of $\\mathbf{G}$ with a row of $\\mathbf{W}$.",
       {"row-1": "You used row 1 of $\\mathbf{G}$. Row 2 of the gradient comes from row 2 of $\\mathbf{G}$.",
        "w-row-1": "You paired row 2 of $\\mathbf{G}$ with row 1 of $\\mathbf{W}$. Column 3 of $\\mathbf{X}$ meets row 3 of $\\mathbf{W}$.",
        "sign": "Check the signs: $(-1)(-1)$ is $+1$."}),
    "$\\partial L/\\partial \\mathbf{X} = \\mathbf{G}\\mathbf{W}^T$ has the shape of $\\mathbf{X}$, 2 by 3. "
    "Its row 2, column 3 pairs row 2 of $\\mathbf{G}$ with row 3 of $\\mathbf{W}$: $1 + 2 = 3$."))

# 19 (makemore l3): a dev total in bits per symbol
tot19, syms19, names19 = 50000, 22807, 3203
items.append(item(
    "e-dev-total-in-bits", 3, ["mk-loss"], ["nats-bits"], 90, "A total on the dev names",
    "Summed over the 3,203 dev names, a name model's negative log-likelihood comes to 50,000 nats. "
    "Those names hold 22,807 next symbols, the end marks included.",
    "What is the average loss in bits per symbol? Give a decimal to 4 places.",
    num(r(tot19 / syms19 / LN2, 6), 0.00005,
        [("nats", r(tot19 / syms19, 6), 0.00005), ("per-name", r(tot19 / names19, 4), 0.00005),
         ("no-ends", r(tot19 / (syms19 - names19) / LN2, 6), 0.00005), ("times-ln2", r(tot19 / syms19 * LN2, 6), 0.00005)],
        label="Loss (bits)"),
    fb("$50{,}000 / 22{,}807 \\approx 2.1923$ nats a symbol, and $2.1923 / \\ln 2 \\approx 3.1628$ bits.",
       "Share the total over the symbols, then turn nats into bits.",
       {"nats": "That is the loss in nats. Divide by $\\ln 2$ for bits.",
        "per-name": "You shared the total over the names. The loss is per next symbol.",
        "no-ends": "You left out the end marks. The model predicts each one, so each counts as a symbol.",
        "times-ln2": "You multiplied by $\\ln 2$. A bit is smaller than a nat, so the figure in bits is larger."}),
    "Per symbol the loss is $50{,}000 / 22{,}807 \\approx 2.1923$ nats. Dividing by $\\ln 2$ gives about 3.1628 bits. "
    "The end marks count because the model predicts them too."))

# 20 (makemore l7): size of an MLP with four symbols of context
blk20, emb20, hid20, V20 = 4, 6, 80, 27
parts20 = [V20 * emb20, blk20 * emb20 * hid20, hid20, hid20 * V20, V20]
items.append(item(
    "e-mlp-size-four", 3, ["mk-mlp"], ["mlp-size"], 90, "A wider context",
    "An MLP language model reads 4 symbols of context from 27, embeds each symbol in 6 numbers and has 80 tanh units.",
    "How many numbers does it learn, counting the embedding table, both weight matrices and both biases?",
    num(sum(parts20), 0, [("no-table", sum(parts20) - parts20[0], 0),
                          ("one-symbol", parts20[0] + emb20 * hid20 + hid20 + hid20 * V20 + V20, 0),
                          ("table-each", blk20 * parts20[0] + sum(parts20[1:]), 0)], label="Numbers"),
    fb("$162 + 1{,}920 + 80 + 2{,}160 + 27 = 4{,}349$.",
       "Count the table, then $W_1$ from the joined context, then $W_2$, then the biases.",
       {"no-table": "You left out the embedding table, $27 \\times 6 = 162$. It is learned with the rest.",
        "one-symbol": "You sized $W_1$ for one symbol's 6 numbers. It reads all 4 joined, 24 numbers.",
        "table-each": "You gave each context place its own table. The 4 places share one table."}),
    "The table holds $27 \\times 6 = 162$, $W_1$ takes the 24 joined numbers to 80 units, $24 \\times 80 = 1{,}920$, and $W_2$ is $80 \\times 27 = 2{,}160$. "
    "With the biases of 80 and 27 the total is 4,349."))

# 21 (makemore l8): epochs at a batch of 48
rows21, steps21, b21 = 182531, 30000, 48
items.append(item(
    "e-epochs-at-48", 3, ["mk-train"], ["epochs"], 90, "Epochs at a batch of 48",
    "The course MLP trains on 182,531 rows. A colleague runs 30,000 minibatch steps of 48 rows each.",
    "How many epochs is that? Give a decimal to 2 places.",
    num(r(steps21 * b21 / rows21, 6), 0.005,
        [("steps", round(rows21 / b21), 0.5), ("batch-32", r(steps21 * 32 / rows21, 6), 0.005),
         ("inverse", r(rows21 / (steps21 * b21), 6), 0.005)], label="Epochs"),
    fb("$30{,}000 \\times 48 = 1{,}440{,}000$ rows, and $1{,}440{,}000 / 182{,}531 \\approx 7.89$ epochs.",
       "One epoch is as many rows as the training set. Count the rows the steps use.",
       {"steps": "That is the number of steps in one epoch. Divide the 30,000 steps by it.",
        "batch-32": "You used the course's batch of 32. This run takes 48 rows a step.",
        "inverse": "You divided the wrong way round: that is the share of an epoch per run."}),
    "One epoch is $182{,}531 / 48 \\approx 3{,}803$ steps of 48. "
    "So 30,000 steps make $30{,}000 \\times 48 / 182{,}531 \\approx 7.89$ epochs."))

# ================================================================ difficulty 4
# 22 (info l2, l5, l6; exit): entropy and KL in bits for a given pair
p22, q22 = [0.45, 0.35, 0.2], [0.25, 0.5, 0.25]
Hp22, Hpq22, Hq22, Hqp22 = H(p22), CE(p22, q22), H(q22), CE(q22, p22)
D22, Dr22 = Hpq22 - Hp22, Hqp22 - Hq22
items.append(parts(
    "e-pair-in-bits", 4, ["if-cross", "if-surprise"], ["kl-divergence"], 300, "Entropy and KL for a pair",
    "A venue fills an order fully, partly or not at all, with true chances $p = (0.45, 0.35, 0.2)$. "
    "A routing model assumes $q = (0.25, 0.5, 0.25)$.",
    "Work in bits throughout.",
    [("What is the entropy $H(p)$? Give a decimal to 4 places.",
      num(r(Hp22, 6), 0.00005, [("nats", r(Hp22 * LN2, 6), 0.00005), ("model", r(Hq22, 4), 0.00005),
                                ("equal", r(math.log2(3), 6), 0.00005)], label="H(p)"),
      fb("$0.45 \\times 1.1520 + 0.35 \\times 1.5146 + 0.2 \\times 2.3219 \\approx 1.5129$ bits.",
         "Weigh each outcome's surprise $-\\log_2 p_i$ by its true chance.",
         {"nats": "That is the entropy in nats. Use $\\log_2$ for bits.",
          "model": "That is the entropy of the model's chances $q$. The question asks about the truth $p$.",
          "equal": "That is the entropy of three equal chances. These chances are unequal."})),
     ("What is the cross-entropy $H(p, q)$? Give a decimal to 4 places.",
      num(r(Hpq22, 6), 0.00005, [("swapped", r(Hqp22, 6), 0.00005), ("nats", r(Hpq22 * LN2, 6), 0.00005)], label="H(p, q)"),
      fb("The model's words cost 2, 1 and 2 bits, so $0.45 \\times 2 + 0.35 \\times 1 + 0.2 \\times 2 = 1.65$ bits.",
         "Weigh the model's word lengths $-\\log_2 q_i$ by the true chances $p_i$.",
         {"swapped": "You weighed the truth's word lengths by the model's chances: that is $H(q, p)$.",
          "nats": "That is the cross-entropy in nats. Use $\\log_2$ for bits."})),
     ("Using parts 1 and 2, what is $D(p \\| q)$? Give a decimal to 4 places.",
      num(r(D22, 6), 0.00005, [("reverse", r(Dr22, 6), 0.00005), ("added", r(Hpq22 + Hp22, 6), 0.00005),
                               ("nats", r(D22 * LN2, 6), 0.00005)], label="D(p || q)"),
      fb("$D(p \\| q) = H(p, q) - H(p) = 1.65 - 1.5129 = 0.1371$ bits.",
         "The KL divergence is the extra cost of the wrong code over the right one.",
         {"reverse": "That is $D(q \\| p)$, with the roles swapped. Here the outcomes come from $p$.",
          "added": "You added the two figures. The divergence is the cross-entropy minus the entropy.",
          "nats": "That is the divergence in nats. Stay in bits."})),
     ("Now the roles swap: outcomes come from $q$ and the code is built for $p$. What is $D(q \\| p)$? Give a decimal to 4 places.",
      num(r(Dr22, 6), 0.00005, [("symmetric", r(D22, 6), 0.00005), ("nats", r(Dr22 * LN2, 6), 0.00005)], label="D(q || p)"),
      fb("$H(q, p) \\approx 1.6258$ and $H(q) = 1.5$, so $D(q \\| p) \\approx 0.1258$ bits.",
         "Repeat parts 1 to 3 with the roles of $p$ and $q$ swapped.",
         {"symmetric": "That is $D(p \\| q)$ again. KL is not symmetric: weigh by $q$ now.",
          "nats": "That is the divergence in nats. Stay in bits."}))],
    "$H(p) \\approx 1.5129$ bits, and the code built for $q$ costs $H(p, q) = 1.65$ bits, so $D(p \\| q) \\approx 0.1371$ bits is the price of the wrong model. "
    "With the roles swapped, $D(q \\| p) \\approx 0.1258$ bits. The two differ because KL is not symmetric."))

# 23 (info l11, l12): three buckets, then two, before and after the bias correction
cnt23 = {"low": (60, 60), "mid": (70, 50), "high": (110, 50)}
n23 = sum(a + b for a, b in cnt23.values())


def mi_counts(rows):
    tot = sum(a + b for a, b in rows)
    col = [sum(rw[j] for rw in rows) for j in range(2)]
    return sum(c / tot * math.log2(c * tot / ((rw[0] + rw[1]) * col[j])) for rw in rows for j, c in enumerate(rw) if c)


I23 = mi_counts(list(cnt23.values()))
merged23 = [(130, 110), (110, 50)]
Im23 = mi_counts(merged23)
HY23 = H([240 / 400, 160 / 400])
b3_23 = 2 * 1 / (2 * n23 * LN2)
b2_23 = 1 * 1 / (2 * n23 * LN2)
lead23 = (I23 - b3_23) - (Im23 - b2_23)
items.append(parts(
    "e-volume-buckets", 4, ["if-mutual"], ["mutual-information", "plug-in-bias"], 300, "Three buckets, then two",
    "Over 400 days a desk files the day's volume as low, mid or high and records the next day's sign. "
    "Low: 60 up, 60 down. Mid: 70 up, 50 down. High: 110 up, 50 down.",
    "Work in bits.",
    [("How many bits of doubt does the next day's sign hold, from its 240 up days and 160 down days? Give a decimal to 3 places.",
      num(r(HY23, 6), 0.0005, [("fair", 1, 0.0005), ("nats", r(HY23 * LN2, 6), 0.0005)], label="H(sign)"),
      fb("$H(0.6, 0.4) \\approx 0.971$ bits.",
         "Use the sign's shares over all 400 days.",
         {"fair": "That would hold for equally many up and down days. Here 0.6 of the days rose.",
          "nats": "That is the entropy in nats. Use $\\log_2$ for bits."})),
     ("What is the plug-in mutual information between the volume bucket and the sign? Give a decimal to 4 places.",
      num(r(I23, 6), 0.0001, [("cond", r(HY23 - I23, 6), 0.00005), ("nats", r(I23 * LN2, 6), 0.00005)], label="I"),
      fb("The rows have sign entropies 1, 0.9799 and 0.8960 bits, weighted 0.3, 0.3 and 0.4, so $I \\approx 0.9710 - 0.9524 = 0.0186$.",
         "Take $H(\\text{sign})$ minus the average entropy of the sign within each bucket.",
         {"cond": "That is the doubt left within the buckets, $H(Y \\mid X)$. Subtract it from $H(Y)$.",
          "nats": "That is the information in nats. Use $\\log_2$ for bits."})),
     ("An engineer merges low and mid into one bucket of 130 up and 110 down. What is the plug-in mutual information now? Give a decimal to 4 places.",
      num(r(Im23, 6), 0.0001, [("unchanged", r(I23, 6), 0.00005), ("cond", r(HY23 - Im23, 6), 0.00005)], label="I merged"),
      fb("The merged row has entropy 0.9950, so $H(Y \\mid X) \\approx 0.9554$ and $I \\approx 0.0155$ bits.",
         "Recompute the weighted row entropies with the merged row in place of the two.",
         {"unchanged": "Merging keeps the information only when the two rows have the same split. Low splits 50:50 and mid 58:42.",
          "cond": "That is the doubt left after reading the merged bucket. Subtract it from $H(Y)$."})),
     ("Correct both plug-in figures for their bias, with $n = 400$. By how many bits does the three-bucket feature still lead the merged one? Give a decimal to 4 places.",
      num(r(lead23, 6), 0.0001, [("plug-in", r(I23 - Im23, 6), 0.00005), ("no-ln2", r((I23 - 2 / 800) - (Im23 - 1 / 800), 6), 0.00005)],
          label="Lead (bits)"),
      fb("The biases are $\\tfrac{2}{800\\ln 2} \\approx 0.0036$ and $\\tfrac{1}{800\\ln 2} \\approx 0.0018$, so the lead shrinks to about 0.0012 bits.",
         "Each table loses $\\tfrac{(k_X - 1)(k_Y - 1)}{2n\\ln 2}$, and the two tables have different $k_X$.",
         {"plug-in": "That is the lead before correcting. The three-bucket table carries the larger bias, so it loses more.",
          "no-ln2": "You left out the $\\ln 2$ in the corrections. In bits each divides by $2n\\ln 2$."}))],
    "The three buckets carry about 0.0186 bits about the sign, and merging low with mid loses some, leaving 0.0155, because their splits differ. "
    "The plug-in bias is twice as large for three buckets as for two, so after correcting the lead falls to about 0.0012 bits."))

# 24 (backprop l5, l6, l7): an interior node with two consumers, and closures that overwrite
u24, v24 = 2.0, 1.5
k24 = u24 * v24
m24 = k24 + u24
n24v = m24 * k24
dk24 = m24 + k24
du24 = k24 + dk24 * v24
# Priya's run with = for +=: closures of n, then m, then k
pm, pk = k24, m24          # n's closure
pk, pu = 1.0 * pm, 1.0 * pm  # m's closure overwrites k.grad and sets u.grad
pu, pv = v24 * pk, u24 * pk  # k's closure overwrites u.grad
items.append(parts(
    "e-node-two-consumers", 4, ["bp-backward", "bp-autograd"], ["branch-gradient", "autograd-bug"], 300, "A node with two consumers",
    "A graph computes $k = uv$, $m = k + u$, then $n = mk$, at $u = 2$ and $v = 1.5$. The node $k$ feeds two boxes, and so does $u$.",
    "Work back from $n$.",
    [("What does the forward pass give for $n$?",
      num(n24v, 0, [("m-only", m24, 0), ("k-squared", k24 * k24, 0)], label="n"),
      fb("$k = 3$, $m = 5$ and $n = 5 \\times 3 = 15$.",
         "Compute $k$, then $m$, then $n$, each from values already found.",
         {"m-only": "That is $m$. The last box multiplies it by $k$.",
          "k-squared": "You used $k$ for both inputs of the last box. Its inputs are $m = 5$ and $k = 3$."})),
     ("What is $\\partial n/\\partial k$, adding every path?",
      num(dk24, 0, [("direct", m24, 0), ("through-m", k24, 0)], label="dn/dk"),
      fb("The product passes $k$ the other input, $m = 5$, and the path through $m$ adds $k \\times 1 = 3$: 8.",
         "$k$ reaches $n$ directly and through $m$. Add both.",
         {"direct": "That is the direct arrow only. The path through $m$ adds $\\partial n/\\partial m = k = 3$.",
          "through-m": "That is the path through $m$ only. The product $n = mk$ also passes $k$ the value $m$."})),
     ("Using $\\partial n/\\partial k = 8$, what is $\\partial n/\\partial u$?",
      num(du24, 0, [("m-path", k24, 0), ("k-path", dk24 * v24, 0), ("direct-k", k24 + m24 * v24, 0)], label="dn/du"),
      fb("Through $m$: $3 \\times 1 = 3$. Through $k$: $8 \\times v = 12$. Together 15.",
         "$u$ feeds $m$ and $k$. Add both contributions.",
         {"m-path": "That is the path through $m$ only. The path through $k$ adds $8 \\times 1.5 = 12$.",
          "k-path": "That is the path through $k$ only. $u$ also feeds $m$ directly.",
          "direct-k": "You used $\\partial n/\\partial k = 5$, the direct arrow only. With both paths it is 8."})),
     ("Priya's closures use `=` where they need `+=`. Her loop runs the closures of $n$, then $m$, then $k$. What does it leave in `u.grad`?",
      num(pu, 0, [("true", du24, 0), ("m-closure", 3, 0), ("k-path", dk24 * v24, 0)], label="u.grad"),
      fb("$n$ sets `k.grad` to 5, then $m$ overwrites it with 3 and sets `u.grad` to 3, then $k$ overwrites `u.grad` with $1.5 \\times 3 = 4.5$.",
         "Run the three closures in turn, replacing each gradient instead of adding to it.",
         {"true": "That is the true gradient. With `=`, each closure throws away what an earlier one sent.",
          "m-closure": "That is `u.grad` after $m$'s closure. $k$'s closure runs next and overwrites it.",
          "k-path": "That would need `k.grad` to keep the 8 from both paths. $m$'s closure overwrote the direct 5 with 3."}))],
    "The node $k$ feeds $m$ and $n$, so its gradient adds $5 + 3 = 8$, and $u$ then collects $3 + 8 \\times 1.5 = 15$. "
    "This matches $n = u^2v^2 + u^2v$, whose slope in $u$ is $9 + 6 = 15$. "
    "With `=` each closure overwrites the last, and Priya's run ends with 4.5."))

# 25 (makemore l9, l12): the same u at two temperatures
row25 = [0.1, 0.5, 0.3, 0.1]
u25 = 0.58
rt25 = [math.sqrt(v) for v in row25]
t25 = [v / sum(rt25) for v in rt25]
sq25 = [v * v for v in row25]
cum1 = np.cumsum(row25)
cumh = np.cumsum(t25)
extra25 = math.log(row25[1] / t25[1])
items.append(parts(
    "e-temperature-same-u", 4, ["mk-eval"], ["temperature", "sampling-rule"], 270, "The same draw at two temperatures",
    "After the context `jo`, a model gives the next symbol these chances, in this order: end 0.1, a 0.5, e 0.3 and n 0.1. The sampler draws $u = 0.58$.",
    "Use the course's sampling rule: the first running total strictly above $u$.",
    [("At $T = 1$, which symbol does $u = 0.58$ pick?",
      choice([opt("a", "a", correct=True),
              opt("e", "e", "a's running total is 0.6, already above 0.58, so the draw stops at a."),
              opt("n", "n", "The draw stops at the first total above 0.58, and a's 0.6 comes first."),
              opt("end", "The end mark", "The end mark's total is 0.1, far below 0.58.")]),
      fb("The totals are 0.1, 0.6, 0.9 and 1, and 0.6 is the first above 0.58.",
         "Add the chances in order until the total passes $u$.")),
     ("Now take $T = 2$. What is a's new chance? Give a decimal to 4 places.",
      num(r(t25[1], 6), 0.00005, [("colder", r(sq25[1] / sum(sq25), 6), 0.00005), ("unscaled", r(rt25[1], 6), 0.00005),
                                  ("unchanged", 0.5, 0.00005)], label="Chance of a"),
      fb(f"Square roots give {rt25[0]:.4f}, {rt25[1]:.4f}, {rt25[2]:.4f} and {rt25[3]:.4f}, which add to {sum(rt25):.4f}, "
         f"so a gets ${rt25[1]:.4f} / {sum(rt25):.4f} \\approx {t25[1]:.4f}$.",
         "At $T = 2$ each chance is raised to the power $\\tfrac12$, then rescaled to add to 1.",
         {"colder": "You squared the chances, which is $T = \\tfrac12$. Dividing the logits by 2 halves them, so the chances are square-rooted.",
          "unscaled": "You took the square root but did not rescale. The roots do not add to 1.",
          "unchanged": "Temperature changes the chances. Only $T = 1$ leaves them as they are."})),
     ("At $T = 2$, which symbol does the same $u = 0.58$ pick?",
      choice([opt("e", "e", correct=True),
              opt("a", "a", f"That was the pick at $T = 1$. a's running total is now {cumh[1]:.4f}, below 0.58."),
              opt("n", "n", f"The total after e, {cumh[2]:.4f}, is already above 0.58."),
              opt("end", "The end mark", f"The end mark's total is now about {cumh[0]:.4f}, below 0.58.")]),
      fb(f"The totals become {cumh[0]:.4f}, {cumh[1]:.4f}, {cumh[2]:.4f} and 1, and {cumh[2]:.4f} is the first above 0.58.",
         "Rebuild the running totals from the flattened chances.")),
     ("The dev names show a after `jo` here. How many more nats does that pair cost at $T = 2$ than at $T = 1$? Give a decimal to 4 places.",
      num(r(extra25, 6), 0.0001,
          [("bits", r(extra25 / LN2, 6), 0.00005), ("sign", -r(extra25, 6), 0.00005),
           ("chances", r(row25[1] - t25[1], 6), 0.00005)], label="Extra cost (nats)"),
      fb(f"a's chance falls from 0.5 to about {t25[1]:.4f}, so the cost rises by $\\ln(0.5/{t25[1]:.4f}) \\approx {extra25:.4f}$ nats.",
         "Compare $-\\ln$ of a's chance at the two temperatures.",
         {"bits": "That is the extra cost in bits. The question asks for nats.",
          "sign": "a's chance falls at $T = 2$, so its cost goes up, not down.",
          "chances": "That is the drop in a's chance. The cost is $-\\ln$ of the chance."}))],
    f"Dividing the logits by 2 takes the square root of each chance before rescaling, so a's 0.5 becomes about {t25[1]:.4f}. "
    f"Its running total falls to {cumh[1]:.4f}, below $u = 0.58$, so the same draw writes e instead of a. "
    f"On a dev pair that ends in a the flatter chances cost about {extra25:.4f} nats more, which is why $T$ is chosen by dev loss."))

# 26 (makemore l1 to l3): a bigram of trading weeks
weeks26 = ["uud", "udd", "uu", "dud"]
S26 = {".": 0, "u": 1, "d": 2}
N26 = np.zeros((3, 3))
for w in weeks26:
    cs = [0] + [S26[c] for c in w] + [0]
    for a, b in zip(cs, cs[1:]):
        N26[a, b] += 1
P26 = (N26 + 1) / (N26 + 1).sum(axis=1, keepdims=True)
held26 = "ud"
cs = [0] + [S26[c] for c in held26] + [0]
nll26 = -sum(math.log(P26[a, b]) for a, b in zip(cs, cs[1:])) / (len(cs) - 1)
items.append(parts(
    "e-bigram-of-weeks", 4, ["mk-bigram", "mk-loss"], ["bigram-counts", "nats-bits"], 300, "A bigram of trading weeks",
    "A desk writes each week's daily signs as a word: u for up, d for down. Each word is wrapped in the marks `.`, as names were. "
    "Its four training weeks are uud, udd, uu and dud. The symbols are `.`, u and d.",
    "Build the bigram table from the four weeks.",
    [("How many pairs does the table count in all?",
      num(float(N26.sum()), 0, [("letters", 11, 0), ("two-marks", 19, 0)], label="Pairs"),
      fb("The weeks hold 11 letters, and each adds one pair for its end mark: $11 + 4 = 15$.",
         "A wrapped week of $n$ letters gives $n + 1$ pairs.",
         {"letters": "You counted one pair per letter. Each week also gives the pair that ends at its end mark.",
          "two-marks": "You counted two extra pairs per week. Wrapping adds one pair, not two."})),
     ("With add-one smoothing over the three symbols, what chance does the end mark get straight after u? Give a decimal to 4 places.",
      num(r(P26[1, 0], 6), 0.00005, [("raw", r(N26[1, 0] / N26[1].sum(), 6), 0.00005),
                                     ("plus-one", r((N26[1, 0] + 1) / (N26[1].sum() + 1), 6), 0.00005),
                                     ("twenty-seven", r((N26[1, 0] + 1) / (N26[1].sum() + 27), 6), 0.00005)], label="Chance"),
      fb("Row u holds 6 pairs, one of them u then the end. Smoothed: $\\tfrac{1 + 1}{6 + 3} \\approx 0.2222$.",
         "Add 1 to each of row u's three counts, then divide by the new row total.",
         {"raw": "That is the raw share, $\\tfrac16$. Smoothing adds 1 to every count of the row first.",
          "plus-one": "You added 1 to the row total once. Each of the three cells gets 1, so the total rises by 3.",
          "twenty-seven": "You smoothed over 27 symbols. This table has three."})),
     ("A held-out week reads ud. Under the add-one table, what is its average loss per pair, in nats? Give a decimal to 4 places.",
      num(r(nll26, 6), 0.00005, [("total", r(nll26 * 3, 6), 0.00005), ("bits", r(nll26 / LN2, 6), 0.00005),
                                 ("no-end", r(-(math.log(P26[0, 1]) + math.log(P26[1, 2])) / 2, 6), 0.00005)], label="Loss (nats)"),
      fb("The pairs cost $-\\ln\\tfrac47$, $-\\ln\\tfrac49$ and $-\\ln\\tfrac12$, about 0.5596, 0.8109 and 0.6931, which average about 0.6879.",
         "Wrap the week as `.ud.`, look up its three pairs in the smoothed table and average their costs.",
         {"total": "That is the total over the three pairs. Divide by 3 for the average.",
          "bits": "That is the loss in bits. The question asks for nats.",
          "no-end": "You left out the pair that ends at the end mark. The model must predict the end too."})),
     ("What is that average loss in bits? Give a decimal to 4 places.",
      num(r(nll26 / LN2, 6), 0.00005, [("times", r(nll26 * LN2, 6), 0.00005), ("perplexity", r(math.exp(nll26), 6), 0.00005)],
          label="Loss (bits)"),
      fb("$0.6879 / \\ln 2 \\approx 0.9924$ bits.",
         "Divide a loss in nats by $\\ln 2$ to get bits.",
         {"times": "You multiplied by $\\ln 2$. A bit is smaller than a nat, so the figure in bits is larger.",
          "perplexity": "That is the perplexity, $e^{0.6879}$. The question asks for the loss in bits."}))],
    "The table counts 15 pairs, and row u, with 6 of them, gives the end mark $\\tfrac{1 + 1}{6 + 3} = \\tfrac29 \\approx 0.2222$ once smoothed. "
    "The held-out week `.ud.` costs about 0.6879 nats a pair, or 0.9924 bits. "
    "The end pair counts, as it does for names."))

# 27 (makemore l4, backprop l15): the bigram network by descent on four pairs
pairs27 = [(1, 1), (1, 2), (1, 2), (2, 0)]   # u then u, u then d twice, d then end
n27 = len(pairs27)
W27 = np.zeros((3, 3))
P0 = np.full(3, 1 / 3)
g_ud = sum((P0[2] - (1.0 if y == 2 else 0.0)) for x, y in pairs27 if x == 1) / n27
floor27 = (math.log(3) + 2 * math.log(1.5)) / n27
items.append(parts(
    "e-bigram-net-four-pairs", 4, ["bp-arrays", "mk-train"], ["bigram-network", "softmax-gradient"], 300, "The same counts by descent",
    "A one-layer network reads one symbol, `.` (0), u (1) or d (2), and outputs 3 logits, row $x$ of a 3 by 3 matrix $W$. "
    "It trains on four pairs: u then u, u then d, u then d, and d then the end. $W$ starts at zero and the loss is the mean cross-entropy.",
    "Work in nats.",
    [("What is the mean loss at the start? Give a decimal to 4 places.",
      num(r(math.log(3), 6), 0.00005, [("bits", r(math.log2(3), 6), 0.00005), ("zero", 0, 0.00005)], label="Loss"),
      fb("Every chance is $\\tfrac13$, so every pair costs $\\ln 3 \\approx 1.0986$.",
         "With all logits 0 the softmax gives equal chances.",
         {"bits": "That is $\\log_2 3$, in bits. The course's cross-entropy uses $\\ln$.",
          "zero": "Zero weights give equal chances, not certainty. Each pair costs $\\ln 3$."})),
     ("Find $\\partial L/\\partial W_{1,2}$ for the weight from u to d, where $L$ is the mean loss. Give a decimal to 4 places.",
      num(r(g_ud, 6), 0.00005, [("no-mean", r(g_ud * n27, 6), 0.00005), ("one-row", r((1 / 3 - 1) / n27, 6), 0.00005),
                                ("sign", -r(g_ud, 6), 0.00005)], label="Gradient"),
      fb("The three u rows give $\\tfrac13 - 0$, $\\tfrac13 - 1$ and $\\tfrac13 - 1$, which add to $-1$. Over 4 pairs that is $-0.25$.",
         "Each row that reads u adds $p_d - y_d$ to that weight. Divide by the 4 pairs of the mean.",
         {"no-mean": "You added the rows without dividing by 4. The loss is a mean.",
          "one-row": "You used one u then d row only. Every row that reads u adds to row u of $W$.",
          "sign": "Check the signs: two of the three rows have $y_d = 1$, so the sum is negative."})),
     ("Using $-0.25$ from part 2, what is $W_{1,2}$ after one step of size 2? Give a decimal.",
      num(r(-2 * g_ud, 6), 0.00005, [("uphill", r(2 * g_ud, 6), 0.00005), ("unit-step", r(-g_ud, 6), 0.00005)], label="New weight"),
      fb("$0 - 2 \\times (-0.25) = 0.5$.",
         "Subtract the step size times the gradient.",
         {"uphill": "You stepped up the gradient. Descent subtracts the step size times the gradient.",
          "unit-step": "You took a step of size 1. The step size is 2."})),
     ("After many steps, what mean loss does training approach on these four pairs? Give a decimal to 4 places.",
      num(r(floor27, 6), 0.00005, [("u-row", r((math.log(3) + 2 * math.log(1.5)) / 3, 6), 0.00005), ("zero", 0, 0.00005),
                                   ("bits", r(floor27 / LN2, 6), 0.00005)], label="Loss"),
      fb("The rows settle on the counts: u gives u $\\tfrac13$ and d $\\tfrac23$, and d gives the end 1. "
         "The mean is $\\tfrac{\\ln 3 + 2\\ln 1.5 + 0}{4} \\approx 0.4774$.",
         "Descent can do no better than the count table on its own training pairs.",
         {"u-row": "That is the average over the three u pairs only. The d pair costs 0 and still counts in the mean of 4.",
          "zero": "Row u sees u once and d twice, so no logits can make both certain. The counts' loss is the floor.",
          "bits": "That is the floor in bits. Stay in nats."}))],
    "The softmax gradient is $(\\mathbf{p} - \\mathbf{y})/n$, and the three u rows add into row u of $W$: $-1/4 = -0.25$, so one step of 2 gives 0.5. "
    "Training drives the rows towards the counts, the best a one-symbol model can do, so the loss falls towards about 0.4774 and no lower."))

# ================================================================ difficulty 5
# 28 (makemore l7, backprop l15): a planted model forward and back by hand
C28 = np.array([0.5, -1.0, 2.0])          # one number a symbol for ., a, b
ctx28 = [2, 1]                             # b then a
W1_28 = np.array([[0.5, -0.25], [1.0, 0.5]])
b1_28 = np.array([0.25, 0.3])
W2_28 = np.array([[1.0, 0.0, -1.0], [2.0, -1.0, 0.5]])
b2_28 = np.array([0.0, 0.2, 0.0])
e28 = C28[ctx28]
h28 = np.tanh(e28 @ W1_28 + b1_28)
z28 = h28 @ W2_28 + b2_28
p28 = np.exp(z28 - z28.max()) / np.exp(z28 - z28.max()).sum()
L28 = -math.log(p28[1])
dz28 = p28.copy()
dz28[1] -= 1
dh2_28 = float(dz28 @ W2_28[1])
EZ = [float(v) for v in np.exp(z28)]
items.append(parts(
    "e-planted-forward-back", 5, ["mk-mlp", "bp-arrays"], ["mlp-forward", "softmax-gradient"], 360, "A planted model, forward and back",
    "A planted MLP language model has three symbols, `.`, a and b, a block of 2 and one number a symbol: $C = (0.5, -1, 2)$. "
    "Its weights are $$W_1 = \\begin{pmatrix} 0.5 & -0.25 \\\\ 1 & 0.5 \\end{pmatrix}, \\quad \\mathbf{b}_1 = (0.25, 0.3),$$ "
    "$$W_2 = \\begin{pmatrix} 1 & 0 & -1 \\\\ 2 & -1 & 0.5 \\end{pmatrix}, \\quad \\mathbf{b}_2 = (0, 0.2, 0).$$ "
    "The context is b then a, and the true next symbol is a.",
    "Run the model forward, then start the backward pass.",
    [("The joined embedding is $(2, -1)$. What is the second hidden unit, $\\tanh$ of $(2, -1)W_1 + \\mathbf{b}_1$ in place 2? Give a decimal to 4 places.",
      num(r(h28[1], 6), 0.00005, [("no-tanh", r(e28 @ W1_28[:, 1] + b1_28[1], 6), 0.00005),
                                  ("first-unit", r(h28[0], 6), 0.00005),
                                  ("sign", -r(h28[1], 6), 0.00005)], label="Hidden unit 2"),
      fb("$2 \\times (-0.25) + (-1) \\times 0.5 + 0.3 = -0.7$, and $\\tanh(-0.7) \\approx -0.6044$.",
         "Take column 2 of $W_1$, add the bias, then apply tanh.",
         {"no-tanh": "That is the input to the unit. Apply tanh to it.",
          "first-unit": "That is the first hidden unit, from column 1 of $W_1$.",
          "sign": "Check the sign: the sum before tanh is $-0.7$."})),
     ("The hidden values are $\\mathbf{h} = (0.2449, -0.6044)$. What is the logit for a, place 2 of $\\mathbf{h}W_2 + \\mathbf{b}_2$? Give a decimal to 4 places.",
      num(r(z28[1], 6), 0.0001, [("no-bias", r(z28[1] - 0.2, 6), 0.00005), ("first-logit", r(z28[0], 6), 0.00005)], label="Logit for a"),
      fb("$0.2449 \\times 0 + (-0.6044) \\times (-1) + 0.2 = 0.8044$.",
         "Pair $\\mathbf{h}$ with column 2 of $W_2$, then add 0.2.",
         {"no-bias": "You left out the bias $b_{2,2} = 0.2$.",
          "first-logit": "That is the logit for `.`, from column 1 of $W_2$."})),
     ("The three logits are about $(-0.9638, 0.8044, -0.5471)$. What is the loss in nats? Give a decimal to 4 places.",
      num(r(L28, 6), 0.0001, [("bits", r(L28 / LN2, 6), 0.0001), ("chance", r(p28[1], 6), 0.0001),
                              ("no-logit", r(L28 + z28[1], 6), 0.0001)],
          label="Loss"),
      fb(f"$e^{{-0.9638}} + e^{{0.8044}} + e^{{-0.5471}} \\approx {EZ[0]:.4f} + {EZ[1]:.4f} + {EZ[2]:.4f} = {sum(round(v, 4) for v in EZ):.4f}$, "
         f"so $p_a \\approx {p28[1]:.4f}$ and the loss is about {L28:.4f}.",
         "Softmax the logits, then take $-\\ln$ of a's chance.",
         {"bits": "That is the loss in bits. The question asks for nats.",
          "chance": "That is a's chance. The loss is $-\\ln$ of it.",
          "no-logit": "That is the log-sum-exp alone. Subtract a's logit from it."})),
     ("What is $\\partial L/\\partial z_a$, the gradient for a's logit? Give a decimal to 4 places.",
      num(r(dz28[1], 6), 0.0001, [("chance", r(p28[1], 6), 0.0001), ("sign", -r(dz28[1], 6), 0.0001)], label="Gradient"),
      fb(f"$p_a - 1 \\approx {p28[1]:.4f} - 1 = {dz28[1]:.4f}$.",
         "The gradient of softmax with cross-entropy is $\\mathbf{p} - \\mathbf{y}$.",
         {"chance": "That is $p_a$. For the true class, subtract 1.",
          "sign": "For the true class, $p - 1$ is negative: raising a's logit lowers the loss."})),
     (f"Using $\\mathbf{{p}} - \\mathbf{{y}} \\approx ({dz28[0]:.5f}, {dz28[1]:.5f}, {dz28[2]:.5f})$, what is $\\partial L/\\partial h_2$? Give a decimal to 4 places.",
      num(r(dh2_28, 6), 0.0002, [("first-row", r(float(dz28 @ W2_28[0]), 6), 0.0002), ("a-only", r(dz28[1] * W2_28[1, 1], 6), 0.0002)],
          label="Gradient"),
      fb(f"Row 2 of $W_2$ is $(2, -1, 0.5)$, so $2 \\times {dz28[0]:.5f} + {-dz28[1]:.5f} + 0.5 \\times {dz28[2]:.5f} \\approx {dh2_28:.4f}$.",
         "$\\partial L/\\partial \\mathbf{h} = (\\mathbf{p} - \\mathbf{y})W_2^T$. Pair it with row 2 of $W_2$.",
         {"first-row": "You used row 1 of $W_2$, which belongs to $h_1$.",
          "a-only": "You used a's logit only. All three logits read $h_2$, so all three gradients flow back."}))],
    "Forward, the context gives $\\mathbf{h} \\approx (0.2449, -0.6044)$, logits about $(-0.9638, 0.8044, -0.5471)$ and a loss of about 0.3573 nats. "
    "Backward, the logits get $\\mathbf{p} - \\mathbf{y}$, and $h_2$ collects $(\\mathbf{p} - \\mathbf{y})$ times row 2 of $W_2$, about 0.6297. "
    "Every logit reads $h_2$, so every class sends a share back."))

# ------------------------------------------------------------------ code item: backward by hand (exit 1)
GRAD_PRELUDE = '''import numpy as np


def loss_fn(P, X, y):
    """Mean cross-entropy, in nats, of softmax(tanh(X W1 + b1) W2 + b2) against the classes y."""
    Z = np.tanh(X @ P["W1"] + P["b1"]) @ P["W2"] + P["b2"]
    m = Z.max(axis=1, keepdims=True)
    lse = m[:, 0] + np.log(np.exp(Z - m).sum(axis=1))
    return float((lse - Z[np.arange(len(y)), y]).mean())


def make_case(seed, n=5, d=4, hid=3, k=4, shift=0.0):
    """A fresh seeded case (P, X, y); shift adds a large spread to the output biases."""
    rng = np.random.default_rng(seed)
    P = {"W1": rng.standard_normal((d, hid)), "b1": rng.standard_normal(hid),
         "W2": rng.standard_normal((hid, k)), "b2": rng.standard_normal(k) + shift * np.arange(k)}
    X = rng.standard_normal((n, d))
    y = rng.integers(0, k, n)
    return P, X, y
'''
GRAD_SOL = '''import numpy as np


def mlp_grads(P, X, y):
    """Gradients of loss_fn(P, X, y) for W1, b1, W2 and b2, by hand."""
    n = len(y)
    A = X @ P["W1"] + P["b1"]
    Hd = np.tanh(A)
    Z = Hd @ P["W2"] + P["b2"]
    E = np.exp(Z - Z.max(axis=1, keepdims=True))
    dZ = E / E.sum(axis=1, keepdims=True)
    dZ[np.arange(n), y] -= 1.0
    dZ /= n
    dA = (dZ @ P["W2"].T) * (1.0 - Hd ** 2)
    return {"W1": X.T @ dA, "b1": dA.sum(axis=0), "W2": Hd.T @ dZ, "b2": dZ.sum(axis=0)}


def grad_error(G, P, X, y, h=1e-5):
    """Global relative error between G and central differences of loss_fn."""
    worst, scale = 0.0, 1e-12
    for key, W in P.items():
        for i in np.ndindex(W.shape):
            keep = W[i]
            W[i] = keep + h
            up = loss_fn(P, X, y)
            W[i] = keep - h
            down = loss_fn(P, X, y)
            W[i] = keep
            num = (up - down) / (2 * h)
            worst = max(worst, abs(G[key][i] - num))
            scale = max(scale, abs(G[key][i]), abs(num))
    return worst / scale
'''
GRAD_STARTER = '''import numpy as np


def mlp_grads(P, X, y):
    """Gradients of loss_fn(P, X, y) for W1, b1, W2 and b2, by hand."""
    # forward: A = X W1 + b1, H = tanh(A), Z = H W2 + b2
    # backward: start from the mean cross-entropy's gradient for Z
    ...


def grad_error(G, P, X, y, h=1e-5):
    """Global relative error between G and central differences of loss_fn."""
    # bump each entry of each array in P by +h and -h, and put it back
    ...
'''


def gmut(old, new, src=GRAD_SOL):
    assert old in src, old
    return src.replace(old, new)


GM_NO_MEAN = gmut("    dZ /= n\n", "")
GM_B1_ROWS = gmut('"b1": dA.sum(axis=0)', '"b1": dA')
GM_SLOPE_A = gmut("(1.0 - Hd ** 2)", "(1.0 - A ** 2)")
GM_NO_MAX = gmut("E = np.exp(Z - Z.max(axis=1, keepdims=True))", "E = np.exp(Z)")
GM_FORWARD = gmut("""            W[i] = keep - h
            down = loss_fn(P, X, y)
            W[i] = keep
            num = (up - down) / (2 * h)""", """            W[i] = keep
            down = loss_fn(P, X, y)
            num = (up - down) / h""")
GM_PER_ENTRY = gmut("""            worst = max(worst, abs(G[key][i] - num))
            scale = max(scale, abs(G[key][i]), abs(num))
    return worst / scale""", """            worst = max(worst, abs(G[key][i] - num) / max(abs(G[key][i]), abs(num), 1e-12))
    return worst""")
GM_SCALE_G = gmut("scale = max(scale, abs(G[key][i]), abs(num))", "scale = max(scale, abs(G[key][i]))")
GM_NO_RESTORE = gmut("""            W[i] = keep - h
            down = loss_fn(P, X, y)
            W[i] = keep
""", """            W[i] = keep - h
            down = loss_fn(P, X, y)
""")

REF_SETUP = ("P, X, y = make_case(11)\n"
             "_A = X @ P['W1'] + P['b1']; _H = np.tanh(_A); _Z = _H @ P['W2'] + P['b2']\n"
             "_E = np.exp(_Z - _Z.max(axis=1, keepdims=True)); _D = _E / _E.sum(axis=1, keepdims=True)\n"
             "_D[np.arange(len(y)), y] -= 1; _D /= len(y); _dA = (_D @ P['W2'].T) * (1 - _H ** 2)\n"
             "REF = {'W1': X.T @ _dA, 'b1': _dA.sum(axis=0), 'W2': _H.T @ _D, 'b2': _D.sum(axis=0)}")
grad_cases = [
    {"setup": "P, X, y = make_case(7)", "call": "mlp_grads(P, X, y)['W2']", "tol": {"rel": 1e-7, "abs": 1e-10}},
    {"setup": "P, X, y = make_case(7)", "call": "mlp_grads(P, X, y)['b1'].shape"},
    {"setup": "P, X, y = make_case(7)", "call": "mlp_grads(P, X, y)['W1']", "tol": {"rel": 1e-7, "abs": 1e-10}},
    {"setup": "P, X, y = make_case(8, n=6, d=2, hid=5, k=3)", "call": "[mlp_grads(P, X, y)[k_] for k_ in ('b2', 'b1', 'W1')]",
     "tol": {"rel": 1e-7, "abs": 1e-10}},
    {"setup": "P, X, y = make_case(9, shift=1000.0)", "call": "mlp_grads(P, X, y)['W2']", "tol": {"rel": 1e-7, "abs": 1e-10}},
    {"setup": "P, X, y = make_case(7)", "call": "grad_error(mlp_grads(P, X, y), P, X, y) < 1e-6"},
    {"setup": REF_SETUP + "\nBAD = {k_: v.copy() for k_, v in REF.items()}; BAD['b2'] = BAD['b2'] * 1.01",
     "call": "grad_error(BAD, P, X, y)", "tol": {"rel": 1e-4, "abs": 0}},
    {"setup": REF_SETUP, "call": "grad_error(REF, P, X, y, h=1e-3) < 1e-5"},
    {"setup": REF_SETUP + "\nP0 = {k_: v.copy() for k_, v in P.items()}\n_e = grad_error(REF, P, X, y, h=0.01)",
     "call": "float(_e) < 1 and all(np.allclose(P[k_], P0[k_], rtol=0, atol=1e-12) for k_ in P)"},
    {"setup": "P, X, y = make_case(12, n=3, d=3, hid=6, k=5)", "call": "grad_error(mlp_grads(P, X, y), P, X, y) < 1e-6"},
    {"setup": REF_SETUP + "\nHALF = {k_: v / 2 for k_, v in REF.items()}", "call": "grad_error(HALF, P, X, y)", "tol": {"rel": 1e-4, "abs": 0}},
]


def run_suite(src, cases, prelude):
    ns = {}
    exec(prelude, ns)
    exec(src, ns)
    out = []
    for c in cases:
        if c.get("setup"):
            exec(c["setup"], ns)
        out.append(eval(c["call"], ns))
    return out


grad_vals = run_suite(GRAD_SOL, grad_cases, GRAD_PRELUDE)
grad_tests = []
for c, v in zip(grad_cases, grad_vals):
    t = {k_: c[k_] for k_ in ("setup", "call") if k_ in c}
    if isinstance(v, (bool, np.bool_)):
        v = bool(v)
        t.update({"expect": repr(v), "compare": "equal"})
    elif isinstance(v, tuple):
        t.update({"expect": repr(v), "compare": "equal"})
    else:
        val = v.tolist() if hasattr(v, "tolist") else [x.tolist() for x in v] if isinstance(v, list) else float(v)
        t.update({"expect": repr(val), "compare": "isclose", "tol": c["tol"]})
    grad_tests.append(t)
ex_ns = {}
exec(GRAD_PRELUDE, ex_ns)
exec(GRAD_SOL, ex_ns)
exec("P, X, y = make_case(2, n=2, d=2, hid=2, k=2)", ex_ns)
grad_examples = [
    {"setup": "P, X, y = make_case(2, n=2, d=2, hid=2, k=2)", "call": "sorted(mlp_grads(P, X, y))", "expect": repr(["W1", "W2", "b1", "b2"]), "compare": "equal"},
    {"setup": "P, X, y = make_case(2, n=2, d=2, hid=2, k=2)", "call": "mlp_grads(P, X, y)['b2']",
     "expect": repr(eval("mlp_grads(P, X, y)['b2']", ex_ns).tolist()), "compare": "isclose", "tol": {"rel": 1e-7, "abs": 1e-10}},
]
items.append({
    "id": "e-backward-by-hand", "difficulty": 5, "skills": ["bp-arrays", "bp-check", "bp-networks"],
    "tags": ["manual-backward", "gradient-check"], "pace": 720, "title": "A backward pass by hand, then checked",
    "prose": "A two-layer network scores $K$ classes: $\\mathbf{A} = \\mathbf{X}\\mathbf{W}_1 + \\mathbf{b}_1$, $\\mathbf{H} = \\tanh \\mathbf{A}$ and "
             "$\\mathbf{Z} = \\mathbf{H}\\mathbf{W}_2 + \\mathbf{b}_2$. The loss is the mean cross-entropy of the rows of $\\mathbf{Z}$ against the classes `y`, in nats. "
             "`loss_fn(P, X, y)` computes it for a dict `P` of float64 arrays, and `make_case(seed)` builds a seeded case `(P, X, y)`. No autograd is loaded.",
    "question": "Write `mlp_grads(P, X, y)`: the gradients of the loss for `W1`, `b1`, `W2` and `b2`, by hand, as a dict with those keys and each array's shape. "
                "Then write `grad_error(G, P, X, y, h=1e-5)`. Bump every entry of every array by $+h$ and $-h$, then put it back. "
                "Return the global relative error between `G` and the central differences: the largest gap over the largest entry of either.",
    "widget": {
        "kind": "code", "language": "python",
        "starter": GRAD_STARTER,
        "solution": GRAD_SOL,
        "prelude": GRAD_PRELUDE,
        "examples": grad_examples,
        "tests": grad_tests,
        "how": f"Submit runs {len(grad_tests)} hidden tests. Four compare your gradients with ours within a relative $10^{{-7}}$, on cases that are not square. "
               "One of those has logits 1,000 apart, and one more test checks the shape of `b1`'s gradient. "
               "Two need `grad_error` of your gradients below $10^{-6}$, the exit's bar. "
               "The others give `grad_error` planted gradients, a step of $h = 0.001$, and check that `P` is put back.",
        "budget": 3000,
        "mutants": [
            {"source": GM_NO_MEAN, "test": 1, "symptom": "Leaves out the division by n, so every gradient is n times too large."},
            {"source": GM_B1_ROWS, "test": 2, "symptom": "Keeps one bias gradient per row instead of summing down the rows."},
            {"source": GM_SLOPE_A, "test": 3, "symptom": "Uses 1 - A**2 for the tanh slope, from the input instead of the output."},
            {"source": GM_NO_MAX, "test": 5, "symptom": "Exponentiates the logits without taking the row maximum out, so logits near 1,000 overflow."},
            {"source": GM_FORWARD, "test": 6, "symptom": "Uses the forward difference, whose error of order h fails the 1e-6 bar."},
            {"source": GM_PER_ENTRY, "test": 7, "symptom": "Takes the worst relative error entry by entry instead of the largest gap over the largest entry."},
            {"source": GM_SCALE_G, "test": 11, "symptom": "Scales by the largest entry of G only, so gradients that are too small read as twice as wrong."},
            {"source": GM_NO_RESTORE, "test": 6, "symptom": "Leaves each entry at keep - h instead of putting it back, so the later bumps start from the wrong place."},
        ],
    },
    "feedback": fb("Your backward pass matches central differences to the exit's $10^{-6}$, and your check catches a planted 1% error.",
                   "Read the first failing test.",
                   {"test-1": "Start from $(\\mathbf{P} - \\mathbf{Y})/n$ for $\\mathbf{Z}$: the loss is a mean over the $n$ rows. Then $\\partial L/\\partial \\mathbf{W}_2 = \\mathbf{H}^T(\\partial L/\\partial \\mathbf{Z})$.",
                    "test-2": "The bias was broadcast down the rows, so its gradient is summed down them: `dA.sum(axis=0)` has shape `(3,)`.",
                    "test-3": "The tanh slope is $1 - \\mathbf{H}^2$, from the output, and $\\partial L/\\partial \\mathbf{W}_1 = \\mathbf{X}^T(\\partial L/\\partial \\mathbf{A})$.",
                    "test-5": "Take each row's largest logit out before `np.exp`. Logits 1,000 apart overflow otherwise.",
                    "test-6": "Use the central difference $\\tfrac{f(w + h) - f(w - h)}{2h}$, and put each entry back to its kept value after its two bumps.",
                    "test-7": "Divide the largest gap over all entries by the largest entry of either, as the course's global relative error does.",
                    "test-11": "Scale by the largest entry of either `G` or the central differences. Here the differences hold the larger entries."}),
    "explain": {"text": "Backward from the mean cross-entropy, $\\partial L/\\partial \\mathbf{Z} = (\\mathbf{P} - \\mathbf{Y})/n$, the products pass $\\mathbf{H}^T$ and $\\mathbf{W}_2^T$, "
                        "the tanh multiplies by $1 - \\mathbf{H}^2$, and each bias sums its gradient down the rows. "
                        "Central differences in float64 agree with it to far better than $10^{-6}$, while a forward difference or a slip in any line misses that bar."}})

# ------------------------------------------------------------------ code item: beat the bigram (exit 3)
BEAT_PRELUDE = '''import json
import math
import numpy as np

words = open('names.txt').read().splitlines()
perm = np.random.default_rng(42).permutation(len(words))
train_names = [words[i] for i in perm[:25626]]
dev_names = [words[i] for i in perm[25626:28829]]
INDEX = {c: i for i, c in enumerate(".abcdefghijklmnopqrstuvwxyz")}


def build_dataset(ws, block=3):
    """Rows of (block indices of context, next index), each name padded with block start marks."""
    X, Y = [], []
    for w in ws:
        context = [0] * block
        for ch in w + ".":
            X.append(context)
            Y.append(INDEX[ch])
            context = context[1:] + [INDEX[ch]]
    return np.array(X, dtype=int).reshape(-1, block), np.array(Y, dtype=int)


def mlp_logits(params, X):
    """Logits of the MLP language model: look up and join, tanh layer, output layer."""
    E = params["C"][X].reshape(X.shape[0], -1)
    return np.tanh(E @ params["W1"] + params["b1"]) @ params["W2"] + params["b2"]


trained = {k: np.array(v) for k, v in json.load(open('makemore-mlp.json')).items() if k != 'about'}


def planted(seed, shift=0.0):
    """A small seeded MLP over the 27 symbols, block 3, 2 numbers a symbol, 4 hidden units."""
    rng = np.random.default_rng(seed)
    return {"C": rng.standard_normal((27, 2)), "W1": rng.standard_normal((6, 4)), "b1": rng.standard_normal(4),
            "W2": rng.standard_normal((4, 27)), "b2": rng.standard_normal(27) + shift}
'''
BEAT_SOL = '''import math
import numpy as np


def dev_report(train_words, dev_words, params, alpha):
    """Dev losses, in nats per next symbol, of the add-alpha bigram and of the MLP, and the bits saved."""
    N = np.zeros((27, 27))
    for w in train_words:
        cs = [0] + [INDEX[c] for c in w] + [0]
        for a, b in zip(cs, cs[1:]):
            N[a, b] += 1
    P = (N + alpha) / (N + alpha).sum(axis=1, keepdims=True)
    cost, count = 0.0, 0
    for w in dev_words:
        cs = [0] + [INDEX[c] for c in w] + [0]
        for a, b in zip(cs, cs[1:]):
            cost -= math.log(P[a, b])
            count += 1
    bigram = cost / count
    X, Y = build_dataset(dev_words)
    Z = mlp_logits(params, X)
    m = Z.max(axis=1, keepdims=True)
    lse = m[:, 0] + np.log(np.exp(Z - m).sum(axis=1))
    mlp = float((lse - Z[np.arange(len(Y)), Y]).mean())
    return {"bigram": bigram, "mlp": mlp, "saved_bits": (bigram - mlp) / math.log(2)}
'''
BEAT_STARTER = '''import math
import numpy as np


def dev_report(train_words, dev_words, params, alpha):
    """Dev losses, in nats per next symbol, of the add-alpha bigram and of the MLP, and the bits saved."""
    # bigram: counts from train_words with alpha added, each row divided by its total,
    #         then the average -ln P[a, b] over every pair of dev_words, end marks included
    # MLP: build_dataset(dev_words), mlp_logits(params, X), mean cross-entropy by log-sum-exp
    ...
'''


def bmut(old, new, src=BEAT_SOL):
    assert old in src, old
    return src.replace(old, new)


BM_NO_MAX = bmut("""    m = Z.max(axis=1, keepdims=True)
    lse = m[:, 0] + np.log(np.exp(Z - m).sum(axis=1))""", """    lse = np.log(np.exp(Z).sum(axis=1))""")
BM_TABLE_TOTAL = bmut("P = (N + alpha) / (N + alpha).sum(axis=1, keepdims=True)", "P = (N + alpha) / (N + alpha).sum()")
BM_NO_BITS = bmut('"saved_bits": (bigram - mlp) / math.log(2)', '"saved_bits": bigram - mlp')
BM_ALPHA_ONE = bmut("P = (N + alpha) / (N + alpha).sum(axis=1, keepdims=True)", "P = (N + 1) / (N + 1).sum(axis=1, keepdims=True)")
BM_NO_END = bmut("""    for w in dev_words:
        cs = [0] + [INDEX[c] for c in w] + [0]""", """    for w in dev_words:
        cs = [0] + [INDEX[c] for c in w]""")
BM_PER_NAME = bmut("""            cost -= math.log(P[a, b])
            count += 1""", """            cost -= math.log(P[a, b])
        count += 1""")
BM_JOINED = bmut("    X, Y = build_dataset(dev_words)\n", "    X, Y = build_dataset([\".\".join(dev_words)])\n    X, Y = X[:-1], Y[:-1]\n")

beat_cases = [
    {"setup": "Q = planted(5)", "call": "dev_report(['ab', 'ba', 'abb'], ['ab', 'bab'], Q, 1)", "tol": {"rel": 0, "abs": 0.0002}},
    {"setup": "Q = planted(5)", "call": "dev_report(['emma', 'ava', 'mae'], ['eva', 'am'], Q, 0.5)", "tol": {"rel": 0, "abs": 0.0002}},
    {"setup": "Q = planted(6, shift=1000.0)", "call": "dev_report(['ab', 'ba'], ['ab', 'ba'], Q, 1)['mlp']", "tol": {"rel": 0, "abs": 0.0002}},
    {"call": "dev_report(train_names, dev_names, trained, 1)", "tol": {"rel": 0, "abs": 0.0002}},
    {"setup": "R5 = dev_report(train_names, dev_names, trained, 1)", "call": "R5['mlp'] < R5['bigram']"},
    {"setup": "Q = planted(3)", "call": "dev_report(train_names[:300], dev_names[:40], Q, 0.1)", "tol": {"rel": 0, "abs": 0.0002}},
]


def run_beat(src, cases):
    cwd = os.getcwd()
    os.chdir(os.path.join(APP, 'content', 'data', 'ai'))
    try:
        return run_suite(src, cases, BEAT_PRELUDE)
    finally:
        os.chdir(cwd)


beat_vals = run_beat(BEAT_SOL, beat_cases)
beat_tests = []
for c, v in zip(beat_cases, beat_vals):
    t = {k_: c[k_] for k_ in ("setup", "call") if k_ in c}
    if isinstance(v, (bool, np.bool_)):
        v = bool(v)
        t.update({"expect": repr(v), "compare": "equal"})
    else:
        t.update({"expect": repr(v), "compare": "isclose", "tol": c["tol"]})
    beat_tests.append(t)
BIG = beat_vals[3]
beat_examples = [
    {"setup": "Q = planted(5)", "call": "sorted(dev_report(['ab'], ['ab'], Q, 1))", "expect": repr(["bigram", "mlp", "saved_bits"]), "compare": "equal"},
    {"setup": "Q = planted(5)", "call": "dev_report(['ab'], ['ab'], Q, 1)['bigram']",
     "expect": repr(run_beat(BEAT_SOL, [{"setup": "Q = planted(5)", "call": "dev_report(['ab'], ['ab'], Q, 1)['bigram']"}])[0]),
     "compare": "isclose", "tol": {"rel": 0, "abs": 0.0002}},
]
items.append({
    "id": "e-beat-the-bigram", "difficulty": 5, "skills": ["mk-eval", "mk-loss", "mk-bigram", "mk-mlp"],
    "tags": ["dev-loss", "bigram-baseline"], "pace": 600, "title": "Does the network beat the counts?",
    "prose": "The course split is loaded: `train_names` (25,626) and `dev_names` (3,203), with `INDEX` (`.` is 0, a to z are 1 to 26). "
             "So are `build_dataset(words)` (block 3), `mlp_logits(params, X)` and `trained`, the MLP's supplied weights. "
             "`planted(seed)` makes a small seeded MLP for testing.",
    "question": "Write `dev_report(train_words, dev_words, params, alpha)`. Count the bigram table of `train_words`, add `alpha` to every cell and divide each row by its own total. "
                "Return a dict of three numbers. `bigram` is its average $-\\ln P$ over every pair of `dev_words`, end marks included. "
                "`mlp` is the mean cross-entropy of the MLP's logits on `dev_words`, by log-sum-exp. "
                "`saved_bits` is the bigram's loss minus the MLP's, in bits.",
    "widget": {
        "kind": "code", "language": "python",
        "starter": BEAT_STARTER,
        "solution": BEAT_SOL,
        "prelude": BEAT_PRELUDE,
        "data": {"names.txt": "content/data/ai/names.txt", "makemore-mlp.json": "content/data/ai/makemore-mlp.json"},
        "examples": beat_examples,
        "tests": beat_tests,
        "how": f"Submit runs {len(beat_tests)} hidden tests, each within 0.0002 of ours, so rounding to 4 places is fine. Three use tiny word lists and planted models, one of them with logits near 1,000. "
               "One scores the supplied weights on the course split, one checks that the MLP's dev loss is below the bigram's, and one uses $\\alpha = 0.1$ on part of the split. "
               "Names and weights: Andrej Karpathy's makemore names list (MIT licence).",
        "budget": 4000,
        "mutants": [
            {"source": BM_TABLE_TOTAL, "test": 1, "symptom": "Divides every count by the table's total, so the rows no longer add to 1."},
            {"source": BM_NO_BITS, "test": 1, "symptom": "Reports the saving in nats, not bits."},
            {"source": BM_NO_END, "test": 1, "symptom": "Leaves out each dev name's end pair."},
            {"source": BM_PER_NAME, "test": 1, "symptom": "Averages the cost over names instead of over next symbols."},
            {"source": BM_JOINED, "test": 1, "symptom": "Joins the dev names into one string, so a name's context runs on from the name before."},
            {"source": BM_ALPHA_ONE, "test": 2, "symptom": "Always adds 1, whatever alpha is."},
            {"source": BM_NO_MAX, "test": 3, "symptom": "Takes no maximum out before np.exp, so logits near 1,000 overflow."},
        ],
    },
    "feedback": fb(f"On the dev names the MLP scores {BIG['mlp']:.4f} nats a symbol against the bigram's {BIG['bigram']:.4f}, a saving of {BIG['saved_bits']:.4f} bits.",
                   "Read the first failing test.",
                   {"test-1": "Divide each row by its own total, and average over every next symbol of the dev words, end marks included. "
                              "Build the dev rows name by name, and divide the saving by $\\ln 2$.",
                    "test-2": "Add `alpha` to every cell, not 1.",
                    "test-3": "Take each row's largest logit out before `np.exp`, as log-sum-exp does."}),
    "explain": {"text": f"Both models are scored the same way, by the average cost of each next symbol of names neither model was fitted to. "
                        f"The bigram from add-one counts scores {BIG['bigram']:.4f} nats and the MLP {BIG['mlp']:.4f}, so three letters of context save about {BIG['saved_bits']:.4f} bits a symbol. "
                        "That held-out gap, not the training loss, is the evidence that the network is the better model."}})

# ------------------------------------------------------------------ write
order_d = {2: [], 3: [], 4: [], 5: []}
for it in items:
    order_d[it["difficulty"]].append(it)
exam = {
    "id": "topic-1.12", "topic": "1.12", "name": "Neural networks from scratch", "minutes": 100, "pass": 0.7,
    "skills": {"if-surprise": "Surprise and entropy", "if-codes": "Codes and compression", "if-cross": "Cross-entropy and KL divergence",
               "if-likelihood": "Perplexity and likelihood", "if-mutual": "Mutual information",
               "bp-chain": "The chain rule on a graph", "bp-backward": "The backward pass", "bp-autograd": "Writing an autograd",
               "bp-networks": "Neurons, layers and training", "bp-check": "Gradient checks", "bp-arrays": "Gradients for arrays",
               "mk-bigram": "Bigram models", "mk-loss": "Likelihood losses", "mk-mlp": "Embeddings and the MLP model",
               "mk-train": "Training and tuning", "mk-eval": "Sampling and held-out evaluation"},
    "items": order_d[2] + order_d[3] + order_d[4] + order_d[5],
}
with open(OUT, "w", encoding="utf8") as f:
    json.dump(exam, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("wrote", os.path.normpath(OUT), len(exam["items"]), "items, pace", sum(i["pace"] for i in exam["items"]), "s",
      {k: len(v) for k, v in order_d.items()})
print("big", {k_: round(v, 4) for k_, v in BIG.items()})
