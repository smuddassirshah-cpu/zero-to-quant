"""Build app/content/exams/topic-2.8.json (topic 2.8, Reinforcement learning: rl levels 1 to 5).

Route A for every key: plain floats, closed forms and loops below. check_numbers.py recomputes each value by a second
route (exact Fractions, linear solves with NumPy, numerical integration, brute-force game search, an independent run of
each code item in CPython) and asserts it at its path in the written file.
Run from anywhere: python3 docs/briefs/exam-2.8-scripts/build.py
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-2.8.json')


def r(x, n=6):
    return round(x, n)


def fb(correct, generic, by_key=None):
    d = {"correct": correct, "generic": generic}
    if by_key:
        d["byKey"] = by_key
    return d


def num(answer, tol, wrong=(), placeholder="a number", label="Answer", accept=None):
    w = {"kind": "numeric", "answer": answer, "tol": {"abs": tol}, "placeholder": placeholder, "label": label}
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


def parts(id, d, skills, tags, pace, title, prose, question, ps, explain):
    return {"id": id, "difficulty": d, "skills": skills, "tags": tags, "pace": pace, "title": title,
            "prose": prose, "question": question,
            "parts": [{"question": q, "widget": w, "feedback": f} for q, w, f in ps],
            "explain": {"text": explain}}


def sig(x):
    return 1 / (1 + math.exp(-x))


items = []

# ================================================================ difficulty 2
# B1 (l1): regret from pull counts, four venues
ps1, n1 = [0.52, 0.48, 0.61, 0.55], [300, 150, 400, 150]
reg1 = sum(n * (max(ps1) - p) for n, p in zip(n1, ps1))
fills1 = sum(n * p for n, p in zip(n1, ps1))
items.append(item(
    "e-regret-four-venues", 2, ["rl-bandit"], ["regret"], 75, "Four venues, one month",
    "A broker routed 1,000 orders over four venues whose fill chances are 0.52, 0.48, 0.61 and 0.55. "
    "They received 300, 150, 400 and 150 orders.",
    "What is the expected regret of this routing, in fills? Give a decimal to 1 place.",
    num(r(reg1, 4), 0.05, [("fills", r(fills1, 4), 0.05), ("per-order", r(reg1 / 1000, 6), 0.00005),
                            ("worst-only", r(150 * (0.61 - 0.48), 4), 0.05)], label="Regret"),
    fb("The gaps to 0.61 are 0.09, 0.13, 0 and 0.06, so regret is $27 + 19.5 + 0 + 9 = 55.5$ fills.",
       "Multiply each venue's orders by its gap to the best fill chance, then add.",
       {"fills": "That is the expected number of fills. Regret is the shortfall against sending all 1,000 orders to the 0.61 venue, which gives 610.",
        "per-order": "That is the regret per order. Multiply by the 1,000 orders.",
        "worst-only": "You counted only the 0.48 venue. The 0.52 and 0.55 venues trail the best one too."}),
    "The best venue fills with chance 0.61, so each order sent elsewhere loses its gap on average. "
    "$300 \\times 0.09 + 150 \\times 0.13 + 150 \\times 0.06 = 55.5$. Regret uses the true chances, not the fills that happened to arrive."))

# M1 (l5): a discounted return
rw2, g2 = [3, -1, 0, 5], 0.8
G2 = sum(g2 ** k * x for k, x in enumerate(rw2))
items.append(item(
    "e-return-with-fees", 2, ["rl-mdp"], ["return"], 60, "Fees on the way",
    "A quoting rule's episode pays £3, then $-$£1 in fees, then nothing, then £5, and ends. The discount is $\\gamma = 0.8$.",
    "What is the discounted return from the start, in pounds? Give 2 decimal places.",
    num(r(G2, 4), 0.005, [("no-disc", 7, 0.005), ("disc-first", r(G2 * g2, 4), 0.005),
                           ("fee-added", r(G2 + 2 * 0.8, 4), 0.005)], label="Return (£)"),
    fb("$3 - 0.8 + 0 + 0.512 \\times 5 = 4.76$.",
       "Discount the reward $k$ steps after the first by $0.8^k$, then add.",
       {"no-disc": "You added the rewards without discounting. Each later step counts 0.8 times as much as the one before.",
        "disc-first": "You discounted the first £3 too. It is paid at once and counts in full.",
        "fee-added": "You added the fee as a gain. The fee lowers the return by 0.8 after discounting."}),
    "$G_0 = 3 + 0.8 \\times (-1) + 0.64 \\times 0 + 0.512 \\times 5 = 4.76$. The £5 three steps after the first is worth only £2.56 now."))

# T1 (l10): one TD(0) update
v3, r3, v3n, a3, g3 = 0.4, -0.1, 0.9, 0.2, 0.95
d3 = r3 + g3 * v3n - v3
items.append(item(
    "e-td-wide-spread", 2, ["rl-td"], ["td-update"], 60, "Wide, then tight",
    "A desk evaluates a quoting rule by TD(0). Its estimate for the state W (wide spread) is 0.4. "
    "One step pays $-0.1$ and lands in state T (tight spread), estimated at 0.9. Take $\\alpha = 0.2$ and $\\gamma = 0.95$.",
    "What is the new estimate for W? Give a decimal to 3 places.",
    num(r(v3 + a3 * d3, 4), 0.0005, [("delta", r(d3, 4), 0.0005), ("no-disc", r(v3 + a3 * (r3 + v3n - v3), 4), 0.0005),
                                     ("target", r(r3 + g3 * v3n, 4), 0.0005)], label="V(W)"),
    fb("$\\delta = -0.1 + 0.95 \\times 0.9 - 0.4 = 0.355$, so the estimate rises by $0.2 \\times 0.355 = 0.071$ to 0.471.",
       "Form the TD error $r + \\gamma V(s') - V(s)$, then add $\\alpha$ times it.",
       {"delta": "That is the TD error. Add $\\alpha$ times it to the old estimate.",
        "no-disc": "You left out $\\gamma$ on the next estimate: $\\delta$ would be 0.4, not 0.355.",
        "target": "That is the target. Move only a fifth of the way towards it."}),
    "The target $-0.1 + 0.855 = 0.755$ stands in for the rest of the return. "
    "The estimate moves a fifth of the way towards it, from 0.4 to 0.471, without waiting for the episode to end."))

# P1 (l13): softmax over three dials
th4 = [1.0, 0.0, -1.0]
e4 = [math.exp(t) for t in th4]
pi4 = [x / sum(e4) for x in e4]
items.append(item(
    "e-softmax-three-dials", 2, ["rl-pg"], ["softmax"], 60, "Three dials",
    "A softmax policy has dials $\\boldsymbol\\theta = (1, 0, -1)$ for three moves.",
    "What is the chance of the first move? Give a decimal to 4 places.",
    num(r(pi4[0], 4), 0.0001, [("two-moves", r(sig(1.0), 4), 0.0001), ("uniform", r(1 / 3, 4), 0.0001),
                                ("third", r(pi4[2], 4), 0.0001)], label="Chance"),
    fb("$e^1 / (e^1 + e^0 + e^{-1}) = 2.7183 / 4.0862 = 0.6652$.",
       "Exponentiate each dial and divide the first by their sum.",
       {"two-moves": "You compared the first dial with the second only, as for two moves. The third move's $e^{-1}$ belongs in the sum too.",
        "uniform": "That would need equal dials. Here the first dial is the largest.",
        "third": "That is the third move's chance, $e^{-1} / 4.0862$."}),
    "The exponentials are 2.7183, 1 and 0.3679, adding to 4.0862. "
    "The first move takes 0.6652 of that, the second 0.2447 and the third 0.0900."))

# S1 (l17): minimax on a two-level tree
tree5 = {"a": [6, 2, 9], "b": [5, 7, 4], "c": [8, 3, 10]}
mins5 = {k: min(v) for k, v in tree5.items()}
items.append(item(
    "e-three-replies", 2, ["rl-search"], ["minimax"], 60, "Three moves, three replies",
    "You choose move a, b or c; your opponent then picks one of three replies. "
    "Your payoffs are 6, 2 and 9 under a, 5, 7 and 4 under b, and 8, 3 and 10 under c.",
    "With both sides playing their best, what payoff do you get?",
    num(max(mins5.values()), 0, [("helps", 10, 0), ("worst", 2, 0), ("average", 7, 0)], label="Payoff"),
    fb("Your opponent holds you to 2 under a, 4 under b and 3 under c. You choose b, worth 4.",
       "Take the smallest payoff under each move, then the largest of those.",
       {"helps": "You took the best payoff anywhere, as if your opponent helped you. Under c they reply with 3.",
        "worst": "That is the smallest payoff overall. You choose the move, so take the best of the three minima.",
        "average": "You chose c for its average, 7. Your opponent does not reply at random: under c they pick 3."}),
    "Each min node takes its smallest payoff: 2, 4 and 3. The max root takes the largest of those, 4. "
    "The 10 under c is never reached, because your opponent answers c with 3."))

# B2 (l4): Beta posterior mean
items.append(item(
    "e-beta-new-quote", 2, ["rl-bandit"], ["beta-posterior"], 60, "A prior for a new quote",
    "A desk's prior for a new quote's hit rate is $\\mathrm{Beta}(2, 4)$. The quote then hits 9 times in 15.",
    "What is the posterior mean of the hit rate? Give a decimal to 4 places.",
    num(r(11 / 21, 4), 0.0001, [("raw", 0.6, 0.0001), ("flat", r(10 / 17, 4), 0.0001), ("swap", r(8 / 21, 4), 0.0001),
                                ("prior", r(2 / 6, 4), 0.0001)], label="Mean"),
    fb("$\\mathrm{Beta}(2 + 9, 4 + 6) = \\mathrm{Beta}(11, 10)$, with mean $\\tfrac{11}{21} = 0.5238$.",
       "Add the hits to the first parameter and the misses to the second, then divide the first by the sum.",
       {"raw": "That is the raw rate, 9 of 15. The prior counts too.",
        "flat": "You used a $\\mathrm{Beta}(1, 1)$ prior: $\\tfrac{10}{17}$. This prior is $\\mathrm{Beta}(2, 4)$.",
        "swap": "You added the hits to the second parameter: $\\tfrac{8}{21}$.",
        "prior": "That is the prior mean, $\\tfrac26$, before any quotes."}),
    "Hits add to the first parameter and misses to the second. "
    "The prior counts as 6 quotes already seen, 2 of them hits, so it pulls the raw 0.6 down to 0.5238."))

# ================================================================ difficulty 3
# B3 (l3): which arm UCB1 pulls
t7 = 150
rec7 = {"P": (90, 0.58), "Q": (40, 0.55), "R": (20, 0.40)}
bon7 = {k: math.sqrt(2 * math.log(t7) / n) for k, (n, m) in rec7.items()}
sc7 = {k: m + bon7[k] for k, (n, m) in rec7.items()}
f4 = lambda x: f"{x:.4f}"
items.append(item(
    "e-ucb-three-venues", 3, ["rl-bandit"], ["ucb"], 120, "Pull 150",
    "At pull $t = 150$ a UCB1 router's record is as follows. Venue P has 90 pulls with mean 0.58, venue Q 40 with mean 0.55 "
    f"and venue R 20 with mean 0.40. Here $2\\ln 150 = {2 * math.log(150):.4f}$.",
    "Which venue does UCB1 pull next?",
    choice([
        opt("R", f"Venue R, with score {f4(sc7['R'])}", correct=True),
        opt("P", "Venue P, with the best mean",
            f"P's 90 pulls leave a bonus of only {f4(bon7['P'])}, so it scores {f4(sc7['P'])}."),
        opt("Q", "Venue Q, between the two",
            f"Q scores {f4(sc7['Q'])}. R's 20 pulls earn a bonus of {f4(bon7['R'])}, the largest of the three."),
        opt("wait", "None yet: UCB1 waits until R has 40 pulls",
            "UCB1 pulls the venue with the largest score on every step. It never waits.")]),
    fb(f"R scores $0.40 + \\sqrt{{10.0213/20}} = {f4(sc7['R'])}$, above Q's {f4(sc7['Q'])} and P's {f4(sc7['P'])}.",
       "Add each venue's bonus $\\sqrt{2\\ln t / n_a}$ to its mean and compare the scores."),
    f"The bonuses are {f4(bon7['P'])}, {f4(bon7['Q'])} and {f4(bon7['R'])}. "
    "R's low mean rests on only 20 pulls, so its upper limit is the highest. UCB1 checks R again before writing it off."))

# B4 (l2): epsilon-greedy floor, five signals
ps8, eps8, T8 = [0.30, 0.42, 0.50, 0.56, 0.62], 0.12, 25000
qbar8 = sum(ps8) / len(ps8)
fl8 = T8 * eps8 * (max(ps8) - qbar8)
items.append(item(
    "e-floor-five-signals", 3, ["rl-bandit"], ["regret-floor"], 90, "Five signals",
    "A fund allocates trades among five signals that win with chance 0.30, 0.42, 0.50, 0.56 and 0.62. "
    "Its allocator is epsilon-greedy with $\\varepsilon = 0.12$ and runs for 25,000 trades.",
    "However well it learns, what is the least regret its random trades cost over the 25,000 trades?",
    num(r(fl8, 4), 0.5, [("per-trade", r(fl8 / T8, 6), 0.00005), ("no-eps", r(T8 * (max(ps8) - qbar8), 4), 0.5),
                         ("worst", r(T8 * eps8 * (max(ps8) - min(ps8)), 4), 0.5)], label="Regret"),
    fb("$\\bar q = 0.48$, so the floor is $25000 \\times 0.12 \\times (0.62 - 0.48) = 420$.",
       "Average the five values, take the gap to 0.62, then scale by $\\varepsilon$ and the trades.",
       {"per-trade": "That is the floor per trade. Multiply by the 25,000 trades.",
        "no-eps": "You charged every trade the random loss of 0.14. Only 12% of trades are random.",
        "worst": "You used the worst signal's gap, 0.32. A uniform random pick loses the average gap, 0.14."}),
    "A random trade picks each signal one time in five, so it loses $0.62 - 0.48 = 0.14$ on average. "
    "About 3,000 trades are random, which costs 420 wins even once the best signal is known."))

# B5 (l2): weight of an old reward under a constant step
al9 = 0.25
w9 = al9 * (1 - al9) ** 4
items.append(item(
    "e-ewma-old-reward", 3, ["rl-bandit"], ["constant-step"], 90, "How much an old fill counts",
    "A venue's fill estimate is updated with a constant step, $Q \\leftarrow Q + \\alpha(R - Q)$, with $\\alpha = 0.25$. "
    "The latest reward carries weight $\\alpha$ in the current estimate.",
    "What weight does the reward that came four updates before the latest one carry? Give a decimal to 4 places.",
    num(r(w9, 4), 0.00005, [("no-alpha", r((1 - al9) ** 4, 4), 0.00005), ("k-plus", r(al9 * (1 - al9) ** 5, 4), 0.00005),
                            ("k-minus", r(al9 * (1 - al9) ** 3, 4), 0.00005)], label="Weight"),
    fb("$0.25 \\times 0.75^4 = 0.0791$.",
       "A reward enters with weight $\\alpha$, and each later update keeps $1 - \\alpha$ of it.",
       {"no-alpha": "You left out the $\\alpha$: a reward enters with weight 0.25 before four later updates scale it by $0.75^4$.",
        "k-plus": "You counted five later updates. Four came after it, so the factor is $0.75^4$.",
        "k-minus": "You counted three later updates. Four came after it, so the factor is $0.75^4$."}),
    "A reward enters with weight 0.25, and each later update keeps 0.75 of everything before. "
    "After four more updates it carries $0.25 \\times 0.75^4 = 0.0791$. Old evidence fades by a constant factor, so the estimate can follow a venue that changes."))

# M2 (l6): a two-state policy value
g10 = 0.9
A10 = [[1 - g10 * 0.7, -g10 * 0.3], [-g10 * 0.6, 1 - g10 * 0.4]]
b10 = [2.0, -1.0]
det10 = A10[0][0] * A10[1][1] - A10[0][1] * A10[1][0]
vF = (b10[0] * A10[1][1] - A10[0][1] * b10[1]) / det10
vL = (A10[0][0] * b10[1] - A10[1][0] * b10[0]) / det10
items.append(item(
    "e-quiet-or-carrying", 3, ["rl-mdp"], ["policy-evaluation"], 150, "Quiet or carrying stock",
    "A market maker's fixed rule earns £2 a step when it holds no stock (state N) and loses £1 a step while it carries inventory (state I). "
    "In N it takes on inventory with chance 0.3 a step; in I it sells out, back to N, with chance 0.6. Rewards are discounted by $\\gamma = 0.9$.",
    "Starting in N, what is the rule worth, in pounds? Give 2 decimal places.",
    num(r(vF, 4), 0.005, [("inventory", r(vL, 4), 0.005), ("gamma-r", r(g10 * vF, 4), 0.005), ("n-only", 20, 0.005)],
        label="Value (£)"),
    fb("$0.37 v_N - 0.27 v_I = 2$ and $-0.54 v_N + 0.64 v_I = -1$ give $v_N = 1.01 / 0.091 = 11.10$.",
       "Write one Bellman equation per state, reward now plus 0.9 times the expected next value, and solve the pair.",
       {"inventory": "That is the value starting in I. The question asks about N.",
        "gamma-r": "You discounted the step's own reward too. Only the next value carries the 0.9.",
        "n-only": "You valued £2 for ever, $2/(1 - 0.9)$. Spells with inventory cost some of that."}),
    "The equations are $v_N = 2 + 0.9(0.7 v_N + 0.3 v_I)$ and $v_I = -1 + 0.9(0.6 v_N + 0.4 v_I)$. "
    "Solving gives £11.10 in N and £7.80 in I. Inventory spells are short, so starting in I costs only £3.30."))

# M3 (l7): a slippery backup from shown values
V11 = {"r4c3": 0.2168, "r4c4": 0.2830, "r3c3": 0.2915}
sc11 = -0.04 + 0.9 * (0.8 * V11["r4c4"] + 0.1 * V11["r3c3"] + 0.1 * V11["r4c3"])
items.append(item(
    "e-slip-bottom-row", 3, ["rl-mdp"], ["backup"], 120, "A move along the bottom row",
    "On the course's slippery grid a move goes ahead with chance 0.8 and slips to each side with 0.1. Each move costs 0.04, and $\\gamma = 0.9$. "
    "The optimal values are 0.2168 at row 4 column 3 and 0.2830 at row 4 column 4, and row 3 column 3 is worth 0.2915.",
    "What does moving R score at row 4, column 3? Give a decimal to 4 places.",
    num(r(sc11, 4), 0.00005, [("no-slip", r(-0.04 + 0.9 * V11["r4c4"], 4), 0.00005),
                              ("edge-zero", r(-0.04 + 0.9 * (0.8 * V11["r4c4"] + 0.1 * V11["r3c3"]), 4), 0.00005),
                              ("no-step", r(sc11 + 0.04, 4), 0.00005)], label="Score"),
    fb("$-0.04 + 0.9(0.8 \\times 0.2830 + 0.1 \\times 0.2915 + 0.1 \\times 0.2168) = 0.2095$, below the cell's own value 0.2168.",
       "List where R can land and with what chance, then take the step cost plus 0.9 times the expected value.",
       {"no-slip": "You took R as certain. It slips up or down one time in ten each.",
        "edge-zero": "A slip down runs off the grid, which leaves the agent at row 4 column 3, worth 0.2168, not nothing.",
        "no-step": "You left out the step cost of 0.04."}),
    "R lands at row 4 column 4 with 0.8, slips up to row 3 column 3 with 0.1 and bumps the bottom edge with 0.1. "
    "Its score, 0.2095, is below 0.2168, so R is not the best move there. U is, and its score equals the cell's value."))

# M4 (homework-2): sweeps for a certificate
g12, c12, tgt12 = 0.8, 2.5, 0.001
k12 = math.ceil(math.log(tgt12 * (1 - g12) / c12) / math.log(g12))
items.append(item(
    "e-certificate-sweeps", 3, ["rl-mdp"], ["contraction"], 90, "A certificate at 0.8",
    "Value iteration runs with $\\gamma = 0.8$. Its first sweep changes the values by at most 2.5. "
    "After $k$ sweeps the error is at most $\\gamma^k \\times 2.5 / (1 - \\gamma)$.",
    "How many sweeps make that certificate at most 0.001?",
    num(k12, 0, [("no-tail", math.ceil(math.log(tgt12 / c12) / math.log(g12)), 0), ("floor", k12 - 1, 0),
                 ("no-first", math.ceil(math.log(tgt12 * (1 - g12)) / math.log(g12)), 0)], label="Sweeps"),
    fb("$0.8^k \\le 0.001 \\times 0.2 / 2.5 = 0.00008$ needs $k \\ge 42.3$, so 43 sweeps.",
       "Solve $0.8^k \\times 2.5 / 0.2 \\le 0.001$ for $k$ and round up.",
       {"no-tail": "You left out the factor $1/(1 - \\gamma) = 5$, the tail of all later changes.",
        "floor": "You rounded down. After 42 sweeps the certificate is still just above 0.001.",
        "no-first": "You left out the first sweep's change, 2.5."}),
    "Taking logs, $k \\ge \\ln 0.00008 / \\ln 0.8 = 42.3$, and the count must be whole, so 43 sweeps. "
    "The certificate holds for every MDP with this discount, and a given problem often settles sooner."))

# T2 (l9): first-visit Monte Carlo with a discount
def returns(rew, g):
    G, out = 0.0, []
    for x in reversed(rew):
        G = x + g * G
        out.append(G)
    return out[::-1]


ep1, ep2 = (["X", "Y", "X", "Z"], [1, -2, 4, 3]), (["X", "Z"], [0, 3])
R1, R2 = returns(ep1[1], 0.9), returns(ep2[1], 0.9)
fv13 = (R1[0] + R2[0]) / 2
ev13 = (R1[0] + R1[2] + R2[0]) / 3
items.append(item(
    "e-mc-two-episodes", 3, ["rl-td"], ["monte-carlo"], 150, "Two visits in one episode",
    "A fixed policy gives two episodes, with $\\gamma = 0.9$. Episode 1 visits X, Y, X and Z, with rewards 1, $-2$, 4 and 3 on the four steps. "
    "Episode 2 visits X and Z, with rewards 0 and 3.",
    "What is the first-visit Monte Carlo estimate of $v(X)$? Give a decimal to 4 places.",
    num(r(fv13, 4), 0.00005, [("every", r(ev13, 4), 0.00005), ("no-disc", r((6 + 3) / 2, 4), 0.00005),
                              ("ep1", r(R1[0], 4), 0.00005)], label="v(X)"),
    fb("The first-visit returns are 4.627 and 2.7, which average 3.6635.",
       "Work out each episode's return from X's first visit, backwards from the end, then average.",
       {"every": "You also counted X's second visit in episode 1, with return 6.7. That is every-visit Monte Carlo.",
        "no-disc": "You added the rewards without the discount.",
        "ep1": "That is episode 1 alone. Average both episodes' first-visit returns."}),
    "Backwards through episode 1: 3, then $4 + 0.9 \\times 3 = 6.7$, then $-2 + 0.9 \\times 6.7 = 4.03$, then $1 + 0.9 \\times 4.03 = 4.627$. "
    "Episode 2 gives $0 + 0.9 \\times 3 = 2.7$. Their mean is 3.6635."))

# T3 (l11): the terminal mask under an optimistic start
q14, rr14, a14, g14, q0_14 = 1.2, 0.96, 0.2, 0.9, 1.2
items.append(item(
    "e-optimistic-end-cell", 3, ["rl-td"], ["q-update"], 90, "An optimistic start at the goal",
    "Q-learning on the deterministic course grid starts every $Q$ at 1.2, the two end cells included. "
    "No true value there is above 0.96, so the start is optimistic. "
    "The agent moves R from r1c4 for the first time: it enters the +1 cell with reward $1 - 0.04 = 0.96$, and the episode ends. "
    "Take $\\alpha = 0.2$ and $\\gamma = 0.9$.",
    "What is the new $Q(\\text{r1c4}, R)$? Give a decimal to 3 places.",
    num(r(q14 + a14 * (rr14 - q14), 4), 0.0005,
        [("no-mask", r(q14 + a14 * (rr14 + g14 * q0_14 - q14), 4), 0.0005), ("target", rr14, 0.0005),
         ("no-step", r(q14 + a14 * (1 - q14), 4), 0.0005)], label="Q"),
    fb("The step ends the episode, so the target is 0.96 alone: $1.2 + 0.2(0.96 - 1.2) = 1.152$.",
       "Ask whether the step ends the episode before you build the target.",
       {"no-mask": "You bootstrapped from the end cell's 1.2. An end cell has no future, so the target is the reward alone.",
        "target": "That is the target. Move only a fifth of the way towards it.",
        "no-step": "The reward for entering the +1 cell is $1 - 0.04 = 0.96$, not 1."}),
    "At an end cell the Q-learning target is $r$, with no $\\gamma \\max Q$ term, so the value falls from 1.2 to 1.152. "
    "The end cells' stored values are leftovers of the start and never change. Adding them would build a false 1.08 into every value near the goal."))

# T4 (l11): the step-size conditions
items.append(item(
    "e-step-size-rule", 3, ["rl-td"], ["step-size"], 90, "Settling on Q*",
    "On the slippery grid two moves at one cell differ by only 0.007, and every target is noisy. "
    "You want Q-learning's estimates to settle on $Q^*$ exactly, not to jiggle in a band around it.",
    "Which step size for the $n$th update of a pair does that need?",
    choice([
        opt("harmonic", "$\\alpha_n = 1/n$", correct=True),
        opt("const", "$\\alpha = 0.1$ for every update",
            "A constant step keeps weighing the latest noisy targets, so the estimates stay in a band and two close moves keep swapping."),
        opt("square", "$\\alpha_n = 1/n^2$",
            "These steps add up to a finite total, so the estimate stops moving before the noise is averaged out."),
        opt("one", "$\\alpha = 1$ for every update",
            "The estimate jumps to each new target, so it is as noisy as one sample.")]),
    fb("Steps of $1/n$ add up to infinity, so learning never stops, while their squares add up to a finite total, so the noise dies away.",
       "Ask which steps never stop learning yet still average away the noise."),
    "Convergence needs $\\sum \\alpha_n = \\infty$ and $\\sum \\alpha_n^2 < \\infty$ (Sutton and Barto, equation 2.7). "
    "$1/n$ meets both; a constant step meets only the first, and $1/n^2$ only the second."))

# P2 (l14): a one-order REINFORCE estimate
pi16, rew16 = [0.5, 0.3, 0.2], 12
items.append(item(
    "e-venue-three-estimate", 3, ["rl-pg"], ["score-estimate"], 90, "An order to venue 3",
    "A softmax router has chances $\\boldsymbol\\pi = (0.5, 0.3, 0.2)$ over three venues. It sends an order to venue 3, which earns £12.",
    "What is this order's REINFORCE estimate for venue 1's dial, in pounds?",
    num(rew16 * (0 - pi16[0]), 0.005, [("sign", rew16 * pi16[0], 0.005), ("pulled-chance", r(-rew16 * pi16[2], 4), 0.005),
                                        ("own-dial", r(rew16 * (1 - pi16[2]), 4), 0.005)], label="Estimate (£)"),
    fb("Venue 1 was not chosen, so its score entry is $-0.5$, and the estimate is $12 \\times (-0.5) = -6$.",
       "Multiply the reward by the score's entry for venue 1's dial, $[1 = a] - \\pi_1$.",
       {"sign": "Venue 1 was not chosen, so its entry is $-\\pi_1$, which is negative.",
        "pulled-chance": "You used venue 3's chance, 0.2. Each dial's entry uses its own chance.",
        "own-dial": "That is the estimate for venue 3's dial, $12 \\times (1 - 0.2)$."}),
    "The score is $(-0.5, -0.3, 0.8)$: the chosen venue's dial goes up and every other goes down by its chance. "
    "Times the £12 reward, venue 1's dial gets $-6$. One order is one noisy sample of the gradient."))

# P3 (l15): variance with the mean as baseline
pi17, rw17, b17 = [0.75, 0.25], [4, 12], 6


def est17(b):
    return [(rw17[0] - b) * (1 - pi17[0]), (rw17[1] - b) * (0 - pi17[0])]


def var17(b):
    e = est17(b)
    m = sum(p * x for p, x in zip(pi17, e))
    return sum(p * x * x for p, x in zip(pi17, e)) - m * m


ex2_17 = sum(p * x * x for p, x in zip(pi17, est17(b17)))
items.append(item(
    "e-baseline-mean-payment", 3, ["rl-pg"], ["baseline-variance"], 150, "The mean payment as baseline",
    "Two venues pay a fixed £4 and £12 an order and are chosen with $\\boldsymbol\\pi = (0.75, 0.25)$. "
    "The baseline is the mean payment, $b = 6$.",
    "What is the variance of the one-order estimate for the first venue's dial?",
    num(r(var17(b17), 4), 0.005, [("nomean", r(ex2_17, 4), 0.005), ("sd", r(math.sqrt(var17(b17)), 4), 0.005),
                                   ("none", r(var17(0), 4), 0.005)], label="Variance"),
    fb("The estimates are $(4 - 6)(0.25) = -0.5$ and $(12 - 6)(-0.75) = -4.5$. Their mean is $-1.5$ and $E[X^2] = 5.25$, so the variance is 3.",
       "Find the estimate after each venue, then its mean and its mean square, each weighted by $\\pi$.",
       {"nomean": "That is $E[X^2]$. Subtract the squared mean, $(-1.5)^2 = 2.25$.",
        "sd": "That is the standard deviation. Square it.",
        "none": "That is the variance with no baseline. With $b = 6$ it falls to 3."}),
    "Without a baseline the estimates are 1 and $-9$, with variance 18.75. "
    "The baseline keeps the mean at the true $-1.5$ and cuts the variance to 3. It is a control variate: the score has mean 0, so subtracting $b$ times it adds no bias."))

# P4 (l14): why reward-to-go
items.append(item(
    "e-why-reward-to-go", 3, ["rl-pg"], ["reward-to-go"], 75, "Only what comes after",
    "REINFORCE weights the score of the move at step $t$ by the reward-to-go $G_t$, the rewards from step $t$ on, "
    "rather than by the whole episode's return.",
    "Why?",
    choice([
        opt("noise", "Earlier rewards cannot depend on that move; they only add noise", correct=True),
        opt("bias", "The whole return would bias the estimate",
            "It would still be unbiased. The earlier rewards have mean 0 against the later score, so they only add noise."),
        opt("discount", "It discounts the rewards that come later on",
            "Reward-to-go here is a plain sum. It drops the earlier rewards; it does not shrink the later ones."),
        opt("exact", "It makes one episode give the exact gradient",
            "One episode is still one noisy sample. Reward-to-go makes it less noisy.")]),
    fb("The earlier rewards multiply a score whose mean is 0 given the past, so they add only noise.",
       "Ask what a move at step $t$ can change."),
    "A move cannot change rewards already paid, so their product with its score averages to 0. "
    "Dropping them keeps the estimate unbiased and lowers its variance, much as a baseline does."))


# S2 (l18): alpha-beta leaf count
def ab_leaves(branches):
    alpha, read = -math.inf, 0
    for leaves in branches:
        m = math.inf
        for x in leaves:
            read += 1
            m = min(m, x)
            if m <= alpha:
                break
        alpha = max(alpha, m)
    return read, alpha


br19 = [(4, 8, 6), (9, 7, 2), (3, 9, 9)]
n19, v19 = ab_leaves(br19)
items.append(item(
    "e-ab-nine-leaves", 3, ["rl-search"], ["alpha-beta"], 120, "Nine leaves, left to right",
    "Alpha-beta reads the leaves left to right. The max root has three min children, with leaves (4, 8, 6), (9, 7, 2) and (3, 9, 9).",
    "How many of the nine leaves does it read?",
    num(n19, 0, [("all", 9, 0), ("value", v19, 0), ("first-leaf", 5, 0)], label="Leaves"),
    fb("It reads all 3 leaves of the first branch (worth 4) and all 3 of the second, where 9 and 7 are above 4 and 2 ends it. The third stops at its first leaf, 3: 7 in all.",
       "Track the value the root can already guarantee, and stop a branch once one of its leaves is no better.",
       {"all": "Pruning skips the last two leaves of the third branch: its first leaf, 3, is already below 4.",
        "value": "That is the root's value. The question asks how many leaves are read.",
        "first-leaf": "You stopped the second branch after its first leaf. 9 and 7 are both above 4, so reading goes on until 2."}),
    "After the first branch the root can guarantee 4, and a min node is cut once a leaf is 4 or less. "
    "In the second branch that is the last leaf, 2; in the third it is the first, 3. So 7 leaves are read, and the root is worth 4."))

# S3 (l19): a UCT score
w20, n20, N20 = 6, 9, 30
uct20 = w20 / n20 + math.sqrt(2) * math.sqrt(math.log(N20) / n20)
items.append(item(
    "e-uct-six-of-nine", 3, ["rl-search"], ["uct"], 90, "Six of nine",
    "In a Monte Carlo tree search a child has won 6 of its 9 playouts, and its parent has 30 visits. The exploration constant is $c = \\sqrt 2$.",
    "What is the child's UCT score? Give a decimal to 4 places.",
    num(r(uct20, 4), 0.0001, [("nob", r(w20 / n20, 4), 0.0001),
                               ("nosq", r(w20 / n20 + math.sqrt(2) * math.log(N20) / n20, 4), 0.00005),
                               ("own-n", r(w20 / n20 + math.sqrt(2) * math.sqrt(math.log(n20) / n20), 4), 0.00005)],
        label="Score"),
    fb(f"The average is $\\tfrac69 = 0.6667$ and the bonus $\\sqrt2\\sqrt{{\\ln 30 / 9}}$ is {math.sqrt(2) * math.sqrt(math.log(30) / 9):.4f}, so the score is {uct20:.4f}.",
       "Add the average $w/n$ to $c\\sqrt{\\ln N / n}$, with $N$ the parent's visits.",
       {"nob": "That is the average alone. Add the exploration bonus.",
        "nosq": "You left out the square root over $\\ln N / n$.",
        "own-n": "You used the child's own 9 visits as $N$. The bonus uses the parent's 30."}),
    f"$\\ln 30 = {math.log(30):.4f}$, over 9 visits is {math.log(30) / 9:.4f}, and $\\sqrt 2$ times its square root is "
    f"{math.sqrt(2) * math.sqrt(math.log(30) / 9):.4f}. The average, 0.6667, plus that bonus gives {uct20:.4f}."))

# S4 (l20): one self-play update
q21, opp21, a21 = 0.2, -0.6, 0.5
items.append(item(
    "e-selfplay-update", 3, ["rl-search"], ["self-play"], 75, "The opponent's best, negated",
    "A self-play table plays both sides of a stick game, with $\\alpha = 0.5$. "
    "Its value for taking $k$ sticks from a pile of $n$ is $Q(n, k) = 0.2$. After the take, the opponent's best value at the new pile is $-0.6$.",
    "What is $Q(n, k)$ after the update? Give a decimal to 1 place.",
    num(r(q21 + a21 * (-opp21 - q21), 4), 0.05, [("sign", r(q21 + a21 * (opp21 - q21), 4), 0.05), ("target", -opp21, 0.05)],
        label="Q"),
    fb("The target is $-(-0.6) = 0.6$, so $Q$ moves half way: $0.2 + 0.5 \\times 0.4 = 0.4$.",
       "Negate the opponent's best value to get the target, then move half way towards it.",
       {"sign": "You used the opponent's value as your own. Their best is your worst, so the target is $+0.6$.",
        "target": "That is the target. With $\\alpha = 0.5$ the value moves only half way."}),
    "Zero-sum: the opponent's best is your worst, so the target negates it. "
    "A pile where the opponent's best is $-0.6$ is good for you, and the value rises from 0.2 to 0.4."))

# ================================================================ difficulty 4
# B6 (l4, problems-1): Thompson with one try each
items.append(parts(
    "e-thompson-one-try-each", 4, ["rl-bandit"], ["thompson"], 300, "One try each",
    "Two quoting rules start from $\\mathrm{Beta}(1, 1)$. Rule A was tried once and filled; rule B was tried once and missed. "
    "So A's posterior is $\\mathrm{Beta}(2, 1)$, with density $2x$, and B's is $\\mathrm{Beta}(1, 2)$, with density $2(1 - x)$.",
    "Thompson sampling chooses between them.",
    [("What is the chance that a draw from B's posterior lands below 0.5? Give a decimal to 2 places.",
      num(0.75, 0.005, [("density", 1.0, 0.005), ("uniform", 0.5, 0.005), ("a-cdf", 0.25, 0.005)], label="Chance"),
      fb("$P(B < x) = 2x - x^2$, so at 0.5 it is $1 - 0.25 = 0.75$.",
         "Integrate B's density $2(1 - u)$ from 0 to 0.5.",
         {"density": "That is B's density at 0.5, not the chance of landing below it. Integrate the density from 0.",
          "uniform": "That would hold for the uniform prior. A miss tilts B's density towards 0.",
          "a-cdf": "That is A's chance, $x^2$. B's density leans the other way."})),
     ("Using B's chance $2x - x^2$ of a draw below $x$, what is the chance that A's draw beats B's? Give a decimal to 4 places.",
      num(r(5 / 6, 4), 0.00005, [("uniform-b", r(2 / 3, 4), 0.00005), ("half", 0.5, 0.00005)], label="Chance"),
      fb("$\\int_0^1 2x(2x - x^2)\\,dx = \\tfrac43 - \\tfrac12 = \\tfrac56 = 0.8333$.",
         "Weight $P(B < x)$ by A's density $2x$ and integrate from 0 to 1.",
         {"uniform-b": "You treated B as uniform, $P(B < x) = x$. Its miss makes it $2x - x^2$.",
          "half": "That would hold if the two posteriors were the same. A leans towards 1 and B towards 0."})),
     ("Using the chance $\\tfrac56$, how many of the next 60 pulls go to A on average, if the posteriors stayed as they are?",
      num(50, 0.05, [("all", 60, 0.05), ("half", 30, 0.05)], label="Pulls"),
      fb("$60 \\times \\tfrac56 = 50$.",
         "Thompson pulls A whenever A's draw is the larger.",
         {"all": "Thompson does not always pull the rule that looks better. B wins one draw in six.",
          "half": "That treats the rules as equal. A wins five draws in six."})),
     ("A is tried again and fills, so its density becomes $3x^2$. What is the chance now that A's draw beats B's? Give a decimal to 2 places.",
      num(0.9, 0.005, [("old", r(5 / 6, 4), 0.005), ("uniform-b", 0.75, 0.005)], label="Chance"),
      fb("$\\int_0^1 3x^2(2x - x^2)\\,dx = \\tfrac32 - \\tfrac35 = 0.9$.",
         "Weight $2x - x^2$ by A's new density $3x^2$ and integrate.",
         {"old": "That is the chance before A's second fill.",
          "uniform-b": "You treated B as uniform: $\\int 3x^2 \\cdot x\\,dx = \\tfrac34$. B is still $\\mathrm{Beta}(1, 2)$."}))],
    "$P(A > B) = \\int_0^1 f_A(x)\\,P(B < x)\\,dx$, which is $\\tfrac56$ for $f_A = 2x$ and 0.9 for $f_A = 3x^2$. "
    "Probability matching gives A that share of the pulls. B still gets one pull in ten, in case its single miss was bad luck."))

# M5 (l5, l8): take an offer or wait
g23 = 0.75
offers = [1, 2, 3, 4, 5]


def rule_value(k, g):
    keep = [x for x in offers if x >= k]
    return (sum(keep) / 5) / (1 - g * (5 - len(keep)) / 5)


V45 = rule_value(4, g23)
V345 = rule_value(3, g23)
items.append(parts(
    "e-take-or-wait", 4, ["rl-mdp"], ["optimal-stopping"], 300, "Take the offer or wait",
    "Each round a client offers an edge of £1k, £2k, £3k, £4k or £5k, each equally likely. "
    "You take it, which ends the game, or wait for the next round's offer. An offer one round later is worth $\\gamma = 0.75$ of the same offer now.",
    "Value the waiting game.",
    [("What is the game worth, in £k, under the rule that takes only £4k or £5k? Give a decimal to 4 places.",
      num(r(V45, 4), 0.00005, [("no-disc", r(rule_value(4, 1.0), 4), 0.00005), ("kept-only", 1.8, 0.00005),
                               ("any", 3.0, 0.00005)], label="Value (£k)"),
      fb("$V = \\tfrac95 + \\tfrac35 \\times 0.75 V$, so $V = 1.8 / 0.55 = 3.2727$.",
         "Condition on the first offer: keep it if it is 4 or 5, else you get $0.75V$.",
         {"no-disc": "You let waiting cost nothing: $V = 1.8 + 0.6V$ gives 4.5. A later offer is worth only 0.75 as much.",
          "kept-only": "That is the kept part alone, $(4 + 5)/5$. Add $\\tfrac35 \\times 0.75V$ for the rounds you wait.",
          "any": "That is the mean offer: the rule that takes anything."})),
     ("Using that value, what is waiting one round worth, in £k? Give a decimal to 4 places.",
      num(r(g23 * V45, 4), 0.00005, [("same", r(V45, 4), 0.00005)], label="Wait (£k)"),
      fb("$0.75 \\times 3.2727 = 2.4545$.",
         "Waiting gives the game's value one round later.",
         {"same": "Waiting is worth $0.75V$, not $V$: the game restarts one round later."})),
     ("With waiting worth 2.4545, is the rule that takes only £4k or £5k the best rule?",
      choice([
          opt("take3", "No: take £3k as well, since 3 beats 2.4545", correct=True),
          opt("yes", "Yes: 3 is below the game's value, 3.2727",
              "Compare an offer with what waiting is worth, $0.75V = 2.4545$, not with $V$."),
          opt("only5", "No: take only £5k",
              "4 beats waiting at 2.4545, so the best rule keeps it."),
          opt("take2", "No: take every offer of £2k or more",
              "2 is below 2.4545, so waiting beats it.")]),
      fb("An offer should be taken when it beats waiting. Here 3, 4 and 5 do, and 1 and 2 do not.",
         "Compare each offer with the value of waiting.")),
     ("What is the game worth, in £k, under the rule that takes £3k, £4k or £5k? Give a decimal to 4 places.",
      num(r(V345, 4), 0.00005, [("no-disc", r(rule_value(3, 1.0), 4), 0.00005), ("old", r(V45, 4), 0.00005),
                               ("kept-only", 2.4, 0.00005)], label="Value (£k)"),
      fb("$V = \\tfrac{12}{5} + \\tfrac25 \\times 0.75 V$, so $V = 2.4 / 0.7 = 3.4286$, more than 3.2727.",
         "Keep 3, 4 or 5; otherwise you get $0.75V$.",
         {"no-disc": "You let waiting cost nothing: $V = 2.4 + 0.4V$ gives 4. Waiting is worth $0.75V$.",
          "old": "That is the old rule's value. The new rule keeps £3k too.",
          "kept-only": "That is the kept part alone, $(3 + 4 + 5)/5$. Add the rounds you wait."}))],
    "Under the new rule waiting is worth $0.75 \\times 3.4286 = 2.5714$. "
    "Now 3 beats waiting and 2 does not, so the rule takes exactly the offers worth more than going on, and it is optimal. "
    "One step of policy improvement found it."))


# T5 (l9, l10): TD against constant-step Monte Carlo on a chain
def run24(eps_n):
    Vt = {"A": 0.0, "B": 0.0, "C": 0.0}
    Vm = dict(Vt)
    hist = []
    path, rew = ["A", "B", "C"], [0, 1, 2]
    for _ in range(eps_n):
        for i, s in enumerate(path):
            target = rew[i] + (Vt[path[i + 1]] if i + 1 < 3 else 0.0)
            Vt[s] += 0.5 * (target - Vt[s])
        G = returns(rew, 1.0)
        for s, g in zip(path, G):
            Vm[s] += 0.5 * (g - Vm[s])
        hist.append((dict(Vt), dict(Vm)))
    return hist


h24 = run24(2)
items.append(parts(
    "e-chain-td-mc", 4, ["rl-td"], ["td-vs-mc"], 270, "News along a chain",
    "Every episode of a fixed policy walks A, B, C and ends, with rewards 0, 1 and 2 on the three steps, and $\\gamma = 1$. "
    "All estimates start at 0. TD(0) updates after each step with $\\alpha = 0.5$. "
    "Constant-step Monte Carlo moves each state towards its return at the end of the episode, also with $\\alpha = 0.5$.",
    "Follow both learners.",
    [("After episode 1, what is TD's $V(B)$? Give a decimal to 2 places.",
      num(h24[0][0]["B"], 0.005, [("full", 1.0, 0.005), ("return", 1.5, 0.005)], label="V(B)"),
      fb("When B is updated, $V(C)$ is still 0, so the target is 1 and $V(B) = 0.5 \\times 1 = 0.5$.",
         "Use the estimates as they stand at the moment of each update.",
         {"full": "That is the target. Move only half way.",
          "return": "That is Monte Carlo's update towards the return 3. TD's target is $1 + V(C)$."})),
     ("After episode 1, what is TD's $V(A)$? Give a decimal to 2 places.",
      num(h24[0][0]["A"], 0.005, [("late", 0.25, 0.005), ("mc", 1.5, 0.005)], label="V(A)"),
      fb("A is updated first, when $V(B)$ is 0, so its target is $0 + 0 = 0$ and it stays at 0.",
         "A's update comes before B's in the episode.",
         {"late": "You used B's new 0.5, but B is updated after A in the episode.",
          "mc": "That is Monte Carlo's estimate. TD's target from A is $0 + V(B)$."})),
     ("After episode 1, what is Monte Carlo's $V(A)$? Give a decimal to 2 places.",
      num(h24[0][1]["A"], 0.005, [("full", 3.0, 0.005), ("td", 0.0, 0.005)], label="V(A)"),
      fb("A's return is $0 + 1 + 2 = 3$, and half way from 0 is 1.5.",
         "Monte Carlo's target is the whole return from A.",
         {"full": "That is the return. With $\\alpha = 0.5$ the estimate moves half way.",
          "td": "That is TD's estimate. Monte Carlo uses the whole return, 3."})),
     ("After episode 2, what is TD's $V(A)$? Give a decimal to 2 places.",
      num(h24[1][0]["A"], 0.005, [("mc", h24[1][1]["A"], 0.005), ("new-b", 0.625, 0.006)], label="V(A)"),
      fb("At the start of episode 2, $V(B) = 0.5$, so A's target is 0.5 and $V(A) = 0.25$.",
         "Update A with $V(B)$ as it stands at the start of episode 2.",
         {"mc": "That is Monte Carlo's $V(A)$ after two episodes, $1.5 + 0.5(3 - 1.5)$.",
          "new-b": "You used B's value after its own update in episode 2, 1.25. A is updated first."}))],
    "TD's targets use the next estimate, so the rewards reach A one step per episode: 0, then 0.25. "
    "Monte Carlo's target is the whole return, 3, so A jumps to 1.5 and then 2.25. "
    "TD learns at every step but passes news back slowly; Monte Carlo waits for the end and passes it all at once."))

# P5 (l14, problems-4): a two-dial REINFORCE step
p25 = sig(0.4)
acts25, rew25 = [1, 0, 1], [-1, -1, 4]
rtg25 = [sum(rew25[t:]) for t in range(3)]
ent25 = [(1 - p25) if a else -p25 for a in acts25]
est25 = sum(g * e for g, e in zip(rtg25, ent25))
whole25 = sum(rew25) * sum(ent25)
right25 = sum(g * e for g, e, a in zip(rtg25, ent25, acts25) if a)
newp25 = sig(0.4 + 2 * 0.1 * est25)
items.append(parts(
    "e-two-dial-step", 4, ["rl-pg"], ["reinforce-step"], 300, "One episode, one step",
    "A corridor policy has dials $(\\theta_L, \\theta_R) = (0, 0.4)$, so the chance of R is $p = 1/(1 + e^{-0.4})$ in every state. "
    "One episode takes three moves, R, L and R, with rewards $-1$, $-1$ and 4, and no discount.",
    "Work out the REINFORCE step for this episode.",
    [("What is $p$? Give a decimal to 4 places.",
      num(r(p25, 4), 0.00005, [("dial", 0.4, 0.00005), ("left", r(1 - p25, 4), 0.00005)], label="p"),
      fb("$1/(1 + e^{-0.4}) = 0.5987$.",
         "The chance of R is the logistic function of the gap $\\theta_R - \\theta_L$.",
         {"dial": "That is the gap itself. Pass it through $1/(1 + e^{-x})$.",
          "left": "That is the chance of L."})),
     ("What reward-to-go weights the score of the L move?",
      num(rtg25[1], 0, [("whole", sum(rew25), 0), ("after", rtg25[2], 0)], label="Reward-to-go"),
      fb("From the L move on: $-1 + 4 = 3$.",
         "Add the rewards from that move's own step to the end.",
         {"whole": "That is the whole return, which counts the reward paid before the L move.",
          "after": "You left out the L move's own reward, $-1$."})),
     ("The right dial's score entry is $1 - p$ after R and $-p$ after L. What is the episode's estimate $\\sum_t G_t \\times$ entry$_t$ for the right dial? Give a decimal to 4 places.",
      num(r(est25, 4), 0.0002, [("whole", r(whole25, 4), 0.0002), ("right-only", r(right25, 4), 0.0002)], label="Estimate"),
      fb(f"$2 \\times {1 - p25:.5f} + 3 \\times ({-p25:.5f}) + 4 \\times {1 - p25:.5f} = {est25:.4f}$.",
         "Multiply each move's reward-to-go by its entry and add the three terms.",
         {"whole": "You weighted every move by the whole return, 2. Each move takes its own reward-to-go: 2, 3 and 4.",
          "right-only": "You left out the L move. Its entry, $-p$, counts too."})),
     ("Take a step with learning rate 0.1: $\\theta_R$ rises by 0.1 times the estimate and $\\theta_L$ falls by the same. What is the new $p$? Give a decimal to 4 places.",
      num(r(newp25, 4), 0.00005, [("one-dial", r(sig(0.4 + 0.1 * est25), 4), 0.00005), ("same", r(p25, 4), 0.00005)],
          label="New p"),
      fb(f"The gap grows by $2 \\times 0.1 \\times {est25:.4f} = {0.2 * est25:.4f}$ to {0.4 + 0.2 * est25:.4f}, so $p = {newp25:.4f}$.",
         "Both dials move, so the gap changes by twice the step.",
         {"one-dial": "You moved only $\\theta_R$. $\\theta_L$ falls too, so the gap grows by twice the step.",
          "same": "The step is small, but it is not zero."}))],
    f"The entries are {1 - p25:.4f}, ${-p25:.4f}$ and {1 - p25:.4f}, weighted by 2, 3 and 4, for a sum of {est25:.4f}. "
    f"Raising $\\theta_R$ and lowering $\\theta_L$ widens the gap by {0.2 * est25:.4f}, so $p$ rises to {newp25:.4f}. "
    "This episode ended well after its R moves, so the step favours R."))

# S5 (l19): an MCTS back-up from both sides
A26, B26 = (5, 8), (2, 4)
Bn = (B26[0] + 1, B26[1] + 1)
An = (A26[0], A26[1] + 1)
uct26 = Bn[0] / Bn[1] + math.sqrt(2) * math.sqrt(math.log(An[1]) / Bn[1])
items.append(parts(
    "e-mcts-two-sides", 4, ["rl-search"], ["mcts-backup"], 240, "A win for O",
    "A tic-tac-toe search follows the path root, A, B and then expands a new child C. X moved into A, O moved into B and X moved into C. "
    "Before this iteration A had $w = 5$, $n = 8$ and B had $w = 2$, $n = 4$. "
    "Each node's $w$ counts wins for the player who moved into it, with a draw as half. The playout from C ends in a win for O.",
    "Back up the result.",
    [("What is B's average $w/n$ after the back-up? Give a decimal to 2 places.",
      num(r(Bn[0] / Bn[1], 4), 0.005, [("same-side", r(B26[0] / Bn[1], 4), 0.005), ("nocount", r(Bn[0] / B26[1], 4), 0.005),
                                         ("draw", r((B26[0] + 0.5) / Bn[1], 4), 0.005)], label="Average"),
      fb("O moved into B and O won, so B goes from 2 of 4 to 3 of 5: 0.6.",
         "Every node on the path gains a visit; a win counts only for the player who moved into the node.",
         {"same-side": "You scored B from X's side. O moved into B, so O's win counts there.",
          "nocount": "You added the win but not the visit: $n$ rises to 5.",
          "draw": "The playout was a win for O, not a draw."})),
     ("What is A's average after the back-up? Give a decimal to 4 places.",
      num(r(An[0] / An[1], 4), 0.00005, [("credit", r((A26[0] + 1) / An[1], 4), 0.00005), ("nocount", r(A26[0] / A26[1], 4), 0.00005)],
          label="Average"),
      fb("X moved into A and lost, so A gains a visit but no win: $5/9 = 0.5556$.",
         "Ask who moved into A.",
         {"credit": "You credited A with O's win. X moved into A, so A gains only the visit.",
          "nocount": "A gains a visit even though X lost: $n$ rises to 9."})),
     ("A now has 9 visits. With $c = \\sqrt 2$, what is B's UCT score as a child of A? Give a decimal to 4 places.",
      num(r(uct26, 4), 0.00005, [("nob", r(Bn[0] / Bn[1], 4), 0.00005),
                                 ("old-n", r(Bn[0] / Bn[1] + math.sqrt(2) * math.sqrt(math.log(A26[1]) / Bn[1]), 4), 0.00005)],
          label="Score"),
      fb(f"$0.6 + \\sqrt2\\sqrt{{\\ln 9 / 5}} = 0.6 + {uct26 - 0.6:.4f} = {uct26:.4f}$.",
         "Use B's new average and visits, and A's 9 visits as $N$.",
         {"nob": "That is the average alone. Add the bonus.",
          "old-n": "You used A's old 8 visits. The back-up raised them to 9."}))],
    "Each node on the path gains a visit, and only the nodes O moved into gain the win. So B goes to 3 of 5 and A to 5 of 9. "
    "At A it is O's turn, so A's children are compared by averages from O's side, which is how B's $w$ is kept."))

# M6 (l7): value iteration on a two-state choice
def vi27(sweeps, g=0.9):
    L, H = 0.0, 0.0
    for _ in range(sweeps):
        L, H = max(1.0, g * (0.5 * L + 0.5 * H)), max(3.0, g * H)
    return L, H


L2, _ = vi27(2)
Lstar = 1.35 / 0.55
items.append(parts(
    "e-sell-low-or-wait", 4, ["rl-mdp"], ["value-iteration"], 210, "Sell low or wait",
    "A position is Low or High. In Low you may sell for £1, which ends the episode, or wait for no reward. "
    "After a wait it is High next step with chance 0.5, else still Low. In High you may sell for £3 and end, or wait and stay High. "
    "$\\gamma = 0.9$, and value iteration starts from all zeros.",
    "Run value iteration.",
    [("What is $V(\\text{Low})$ after two sweeps? Give a decimal to 1 place.",
      num(r(L2, 4), 0.05, [("one-sweep", 1.0, 0.05), ("no-disc", 2.0, 0.05)], label="V(Low)"),
      fb("Sweep 1 gives Low 1 and High 3. Sweep 2 gives Low $\\max(1, 0.9 \\times (0.5 \\times 1 + 0.5 \\times 3)) = 1.8$.",
         "Back up each state from the previous sweep's table, twice.",
         {"one-sweep": "That is after one sweep. Back up once more with the new table.",
          "no-disc": "You left out $\\gamma$: waiting is worth $0.9 \\times 2 = 1.8$, not 2."})),
     ("What is the optimal value $V^*(\\text{Low})$? Give a decimal to 4 places.",
      num(r(Lstar, 4), 0.00005, [("sell", 1.0, 0.00005), ("no-disc", 3.0, 0.00005), ("sweep2", r(L2, 4), 0.00005)], label="V*(Low)"),
      fb("$V^*(\\text{High}) = 3$, and waiting in Low gives $V = 0.9(0.5V + 1.5)$, so $V = 1.35/0.55 = 2.4545$.",
         "Find $V^*(\\text{High})$ first, then solve Low's equation for the better action.",
         {"sell": "That is selling at once. Waiting is worth more.",
          "no-disc": "You dropped the discount: $V = 0.5V + 1.5$ gives 3.",
          "sweep2": "That is the value after two sweeps. Value iteration has not settled yet."}))],
    "At the fixed point waiting in Low is worth $0.45V + 1.35$, so $V^*(\\text{Low}) = 2.4545$, well above selling at £1. "
    "Two sweeps already show the right action, but the value is still 0.65 short. Quote values only once the sweeps have settled."))


# ================================================================ difficulty 5
# S6 (l17, l20): a new stick game, by search and by self-play
def losing(n, takes=(1, 3, 4)):
    L = [False] * (n + 1)
    for m in range(n + 1):
        L[m] = all(not L[m - k] for k in takes if k <= m)
    return L


L28 = losing(30)
lose28 = [m for m in range(1, 11) if L28[m]]
take28 = [k for k in (1, 3, 4) if k <= 12 and L28[12 - k]]
items.append(parts(
    "e-take-one-three-four", 5, ["rl-search"], ["minimax", "self-play"], 360, "Take 1, 3 or 4",
    "A new stick game: each player in turn takes 1, 3 or 4 sticks, and whoever takes the last stick wins. "
    "With 0 sticks left, the player to move has lost.",
    "Solve the game, then check a self-play table.",
    [("How many of the piles from 1 to 10 lose for the player to move against best play?",
      num(len(lose28), 0, [("mult4", 2, 0), ("with-zero", len(lose28) + 1, 0)], label="Piles"),
      fb("Piles 2, 7 and 9 lose: every take from them leaves a pile that wins.",
         "Work up from 0: a pile loses when every take leaves a winning pile for your opponent.",
         {"mult4": "You used the rule of the game with takes 1 to 3, the multiples of 4. Here 4 wins at once.",
          "with-zero": "You counted pile 0, which is not between 1 and 10."})),
     ("From a pile of 12, how many sticks should you take?",
      num(take28[0], 0, [("four", 4, 0), ("one", 1, 0)], label="Take"),
      fb("Take 3 and leave 9, a losing pile for your opponent.",
         "Find the take that leaves your opponent a losing pile.",
         {"four": "That leaves 8: your opponent takes 1 and leaves you 7.",
          "one": "That leaves 11: your opponent takes 4 and leaves you 7."})),
     ("A self-play table starts with every value at 0 and $\\alpha = 0.5$. Its first update takes 4 from a pile of 4 and wins, so $Q(4, 4) = 0.5$. "
      "Next it takes 4 from a pile of 8, and the best value at the pile of 4 is 0.5. What is $Q(8, 4)$ now? Give a decimal to 2 places.",
      num(-0.25, 0.005, [("sign", 0.25, 0.005), ("target", -0.5, 0.005)], label="Q(8, 4)"),
      fb("The target is $-0.5$, minus the opponent's best at 4, so $Q(8, 4) = 0 + 0.5 \\times (-0.5) = -0.25$.",
         "Negate the opponent's best value at the pile you leave, then move half way.",
         {"sign": "You used the opponent's value as your own. Leaving them a pile worth 0.5 to them is bad for you.",
          "target": "That is the target. Move only half way."})),
     ("After 500 self-play episodes the table wins 50% of its games against its own latest copy. What does that number show?",
      choice([
          opt("nothing", "Nothing about its skill: test it against fixed opponents", correct=True),
          opt("exact", "That it has learned the game exactly by now",
              "Two equal copies split their games whatever their skill, so 50% says nothing."),
          opt("half", "That it is about half way to the best rule",
              "The rate against itself does not measure distance from the best rule."),
          opt("explore", "That it needs to explore more in training",
              "Any agent scores about 50% against its own copy, however much it explores.")]),
      fb("A copy against itself splits its games. A random player or an earlier version shows progress.",
         "Ask what any agent scores against an exact copy of itself."))],
    "Pile 0 loses, and 1, 3 and 4 win at once; 2 forces a move to 1, and 7 and 9 leave only winning piles. "
    "So from 12 you take 3 and leave 9. Self-play finds the same piles by negating the opponent's best value, and it is judged against fixed opponents."))

# P6: contextual REINFORCE with a baseline per state (code)
ROUTER_SOL = '''import math
import random

def probs(theta):
    """Softmax chances from a list of dials."""
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def pick(pi, rng):
    """An index drawn with chances pi, from one rng.random()."""
    u, c = rng.random(), 0.0
    for i, p in enumerate(pi):
        c += p
        if u < c:
            return i
    return len(pi) - 1

def train_router(R, steps, lr, beta, seed):
    """REINFORCE on a two-state router. Return [probs(theta[0]), probs(theta[1])]."""
    rng = random.Random(seed)
    k = len(R[0])
    theta = [[0.0] * k, [0.0] * k]
    b = [0.0, 0.0]
    for _ in range(steps):
        s = 1 if rng.random() < 0.5 else 0
        pi = probs(theta[s])
        a = pick(pi, rng)
        r = R[s][a]
        adv = r - b[s]
        theta[s] = [t + lr * adv * ((1.0 if j == a else 0.0) - pi[j]) for j, t in enumerate(theta[s])]
        b[s] += beta * (r - b[s])
    return [probs(theta[0]), probs(theta[1])]
'''
ROUTER_STARTER = '''import math
import random

def probs(theta):
    """Softmax chances from a list of dials."""
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def pick(pi, rng):
    """An index drawn with chances pi, from one rng.random()."""
    u, c = rng.random(), 0.0
    for i, p in enumerate(pi):
        c += p
        if u < c:
            return i
    return len(pi) - 1

def train_router(R, steps, lr, beta, seed):
    """REINFORCE on a two-state router. Return [probs(theta[0]), probs(theta[1])]."""
    rng = random.Random(seed)
    k = len(R[0])
    theta = [[0.0] * k, [0.0] * k]   # dials for state 0 (calm) and state 1 (busy)
    b = [0.0, 0.0]                   # one baseline per state
    # each step: draw s, then pick a, then step theta[s], then update b[s]
    ...
'''


def mutate(old, new):
    assert old in ROUTER_SOL, old
    return ROUTER_SOL.replace(old, new)


ROUTER_B_FIRST = mutate("        adv = r - b[s]\n", "        b[s] += beta * (r - b[s])\n        adv = r - b[s]\n").replace(
    "        b[s] += beta * (r - b[s])\n    return", "    return")
ROUTER_SHARED = ROUTER_SOL.replace("adv = r - b[s]", "adv = r - b[0]").replace("b[s] += beta * (r - b[s])", "b[0] += beta * (r - b[0])")
ROUTER_ALL = mutate("        theta[s] = [t + lr * adv * ((1.0 if j == a else 0.0) - pi[j]) for j, t in enumerate(theta[s])]\n",
                    "        for z in (0, 1):\n            theta[z] = [t + lr * adv * ((1.0 if j == a else 0.0) - pi[j]) for j, t in enumerate(theta[z])]\n")
ROUTER_ONLY = mutate("((1.0 if j == a else 0.0) - pi[j])", "((1.0 - pi[j]) if j == a else 0.0)")
ROUTER_NOB = mutate("        b[s] += beta * (r - b[s])\n", "")

R29 = [[1, 2, 0], [0, 1, 3]]
ns29 = {}
exec(ROUTER_SOL, ns29)
TR = ns29["train_router"]
router_cases = [
    ("train_router([[1, 2, 0], [0, 1, 3]], 3, 0.5, 0.5, 7)", None),
    ("train_router([[1, 2, 0], [0, 1, 3]], 4, 0.5, 0.2, 3)", None),
    ("train_router([[5, 6, 4], [5, 6, 4]], 6, 0.5, 0.5, 2)", None),
    ("train_router([[1, 2, 0], [0, 1, 3]], 1, 0.1, 0.1, 1)[0]", None),
    ("train_router([[1, 2, 0], [0, 1, 3]], 50, 0.0, 0.1, 4)", None),
    ("all(t[0][1] > 0.9 and t[1][2] > 0.9 for t in (train_router([[1, 2, 0], [0, 1, 3]], 2000, 0.1, 0.1, s) for s in range(5)))", None),
    ("min(train_router([[1, 2, 0], [0, 1, 3]], 2000, 0.1, 0.1, 5)[1][2], train_router([[2, 0, 1], [0, 3, 1]], 2000, 0.1, 0.1, 6)[1][1])", None),
]
router_tests = []
for call, _ in router_cases:
    got = eval(call, ns29)
    if isinstance(got, bool):
        router_tests.append({"call": call, "expect": repr(got), "compare": "equal"})
    elif isinstance(got, float):
        router_tests.append({"call": f"{call} > 0.9", "expect": "True", "compare": "equal"})
    else:
        router_tests.append({"call": call, "expect": repr(got), "compare": "isclose"})
items.append({
    "id": "e-router-two-states", "difficulty": 5, "skills": ["rl-pg"], "tags": ["reinforce", "baseline"], "pace": 600,
    "title": "A router for calm and busy steps",
    "prose": "A router meets two kinds of step, calm (state 0) and busy (state 1), and chooses among three venues. `R[s][a]` is venue `a`'s fixed payment in state `s`. "
             "Each state has its own softmax dials, all 0 at first, and its own baseline `b[s]`, also 0. `probs` (the softmax) and `pick` are written for you.",
    "question": "Write `train_router(R, steps, lr, beta, seed)`. Each step: `s = 1 if rng.random() < 0.5 else 0`, then `pi = probs(theta[s])`, `a = pick(pi, rng)` and `r = R[s][a]`. "
                "Add `lr * (r - b[s])` times the score to `theta[s]` only; the score's entry for venue `j` is 1 if `j == a`, else 0, minus `pi[j]`. "
                "Then update `b[s] += beta * (r - b[s])`.",
    "widget": {
        "kind": "code", "language": "python",
        "starter": ROUTER_STARTER,
        "solution": ROUTER_SOL,
        "examples": [{"call": "train_router([[1, 2, 0], [0, 1, 3]], 0, 0.1, 0.1, 0)",
                      "expect": repr(TR([[1, 2, 0], [0, 1, 3]], 0, 0.1, 0.1, 0)), "compare": "isclose"},
                     {"call": "train_router([[0, 0, 0], [0, 0, 0]], 10, 0.1, 0.1, 0)",
                      "expect": repr(TR([[0, 0, 0], [0, 0, 0]], 10, 0.1, 0.1, 0)), "compare": "isclose"}],
        "tests": router_tests,
        "how": f"Submit runs {len(router_tests)} hidden tests. Three short seeded runs must match ours within `math.isclose`, so draw `s`, then `a`, then step the dials, then the baseline. "
               "Others check that the unvisited state's dials stay put and that a zero learning rate changes nothing. The last two need each state's best venue above 0.9 after 2,000 steps.",
        "mutants": [
            {"source": ROUTER_B_FIRST, "test": 1, "symptom": "Updates the baseline before the step, so the step's baseline has already seen this reward."},
            {"source": ROUTER_SHARED, "test": 2, "symptom": "Keeps one baseline for both states."},
            {"source": ROUTER_ALL, "test": 1, "symptom": "Steps the dials of both states with the visited state's score."},
            {"source": ROUTER_ONLY, "test": 1, "symptom": "Moves only the chosen venue's dial, leaving out the minus pi for the others."},
            {"source": ROUTER_NOB, "test": 1, "symptom": "Never updates the baseline, so it stays at 0."},
        ],
    },
    "feedback": fb("The router learns each state's best venue, with a baseline per state that never sees the reward it is subtracted from.",
                   "Read the first failing test.",
                   {"test-1": "Step only `theta[s]`, give every dial its entry `[j == a] - pi[j]`, and update `b[s]` after the step, never before it.",
                    "test-2": "Keep a baseline per state, and update the visited state's baseline after each step.",
                    "test-4": "Only the visited state's dials move. The other state's chances stay at a third each.",
                    "test-6": "Check the sign: the step adds `lr * (r - b[s])` times the score."}),
    "explain": {"text": "Each state's dials form their own softmax policy, so a step moves only the dials of the state that was seen. "
                        "A baseline per state tracks that state's typical payment, as a learned $V(s)$ would. "
                        "Updating it after the step keeps it fixed before the action is drawn, so the estimate stays unbiased."}})

# T6 / exit: Q-learning on a new grid against value iteration (code)
GRID_HEAD = '''import random

ROWS, COLS = 3, 5
WALL = {'r2c2', 'r2c4'}
ENDS = {'r1c5': 1.0, 'r3c5': -1.0}
STEP = -0.05
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]
OPEN = [s for s in CELLS if s not in ENDS]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = int(s[1]), int(s[3])
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def pay(t):
    """Reward for entering cell t: its payoff plus the step cost."""
    return ENDS.get(t, 0.0) + STEP

def optimal_sets(gamma=0.9):
    """Value iteration to convergence; {open cell: set of best actions, ties within 1e-9 kept}."""
    V = {s: 0.0 for s in CELLS}
    while True:
        new = {s: 0.0 if s in ENDS else max(pay(move(s, a)) + gamma * V[move(s, a)] for a in 'URDL')
               for s in CELLS}
        done = max(abs(new[s] - V[s]) for s in CELLS) < 1e-12
        V = new
        if done:
            break
    sets = {}
    for s in OPEN:
        q = {a: pay(move(s, a)) + gamma * V[move(s, a)] for a in 'URDL'}
        sets[s] = {a for a in 'URDL' if q[a] > max(q.values()) - 1e-9}
    return sets
'''
GRID_SOL = GRID_HEAD + '''
def q_learn(episodes, seed, alpha=0.2, eps=0.2, q0=0.0, gamma=0.9):
    """Q-learning on the grid. Return Q as {(cell, action): value} for all 13 cells."""
    rng = random.Random(seed)
    Q = {(s, a): q0 for s in CELLS for a in 'URDL'}
    for _ in range(episodes):
        s = rng.choice(OPEN)
        while s not in ENDS:
            if rng.random() < eps:
                a = rng.choice('URDL')
            else:
                a = max('URDL', key=lambda b: Q[(s, b)])   # ties: first in U, R, D, L
            t = move(s, a)
            r = pay(t)
            target = r if t in ENDS else r + gamma * max(Q[(t, b)] for b in 'URDL')
            Q[(s, a)] += alpha * (target - Q[(s, a)])
            s = t
    return Q

def greedy_ok(Q):
    """True when every open cell's first best action is in optimal_sets()[cell]."""
    sets = optimal_sets()
    return all(max('URDL', key=lambda b: Q[(s, b)]) in sets[s] for s in OPEN)
'''
GRID_STARTER = GRID_HEAD + '''
def q_learn(episodes, seed, alpha=0.2, eps=0.2, q0=0.0, gamma=0.9):
    """Q-learning on the grid. Return Q as {(cell, action): value} for all 13 cells."""
    rng = random.Random(seed)
    ...

def greedy_ok(Q):
    """True when every open cell's first best action is in optimal_sets()[cell]."""
    ...
'''


def gmut(old, new):
    assert old in GRID_SOL, old
    return GRID_SOL.replace(old, new)


GRID_NO_MASK = gmut("target = r if t in ENDS else r + gamma * max(Q[(t, b)] for b in 'URDL')",
                    "target = r + gamma * max(Q[(t, b)] for b in 'URDL')")
GRID_LAST_TIE = gmut("a = max('URDL', key=lambda b: Q[(s, b)])   # ties: first in U, R, D, L",
                     "a = max('LDRU', key=lambda b: Q[(s, b)])")
GRID_NO_STEP = gmut("            r = pay(t)\n", "            r = ENDS.get(t, 0.0)\n")
GRID_ARGMAX = gmut("    sets = optimal_sets()\n    return all(max('URDL', key=lambda b: Q[(s, b)]) in sets[s] for s in OPEN)",
                   "    sets = optimal_sets()\n    return all(max('URDL', key=lambda b: Q[(s, b)]) == min(sets[s], key='URDL'.index) for s in OPEN)")
GRID_SARSA = gmut("""            t = move(s, a)
            r = pay(t)
            target = r if t in ENDS else r + gamma * max(Q[(t, b)] for b in 'URDL')""",
                  """            t = move(s, a)
            r = pay(t)
            nxt = max('URDL', key=lambda b: Q[(t, b)]) if rng.random() >= eps else rng.choice('URDL')
            target = r if t in ENDS else r + gamma * Q[(t, nxt)]""")

nsg = {}
exec(GRID_SOL, nsg)
sets30 = nsg["optimal_sets"]()
SETS_LIT = "{" + ", ".join(f"'{s}': {sorted(v)!r}" for s, v in sets30.items()) + "}"
grid_cases = [
    {"call": "len(q_learn(1, 0))"},
    {"call": "sum(q_learn(5, 0).values())"},
    {"call": "sum(q_learn(5, 1, q0=0.5).values())"},
    {"call": "[q_learn(3, 2, q0=0.3)[('r1c5', a)] for a in 'URDL']"},
    {"call": "greedy_ok(q_learn(300, 0))"},
    {"setup": f"S = {SETS_LIT}",
     "call": "all(all(max('URDL', key=lambda b: Q[(c, b)]) in S[c] for c in S) for Q in (q_learn(300, k) for k in range(1, 5)))"},
    {"call": "greedy_ok({(c, a): 0.0 for c in CELLS for a in 'URDL'})"},
    {"setup": "Q = q_learn(2000, 0)\nQ[('r3c1', 'R')] = max(Q[('r3c1', b)] for b in 'URDL') + 0.001", "call": "greedy_ok(Q)"},
    {"call": "abs(max(q_learn(2000, 0)[('r3c1', a)] for a in 'URDL') - 0.3562) < 0.001"},
]
grid_tests = []
for case in grid_cases:
    g = dict(nsg)
    if "setup" in case:
        exec(case["setup"], g)
    got = eval(case["call"], g)
    t = dict(case)
    t["expect"] = repr(got)
    t["compare"] = "isclose" if isinstance(got, (float, list)) else "equal"
    grid_tests.append(t)
V30 = None
items.append({
    "id": "e-q-learning-exit", "difficulty": 5, "skills": ["rl-td", "rl-mdp"], "tags": ["q-learning", "gridworld"], "pace": 600,
    "title": "Q-learning on a new grid",
    "prose": "A deterministic grid of 3 rows and 5 columns, row 1 at the top. There are walls at r2c2 and r2c4. Entering r1c5 pays +1 and entering r3c5 pays $-1$, and both end the episode. "
             "Every move also costs 0.05, and a move into a wall or off the grid stays put. "
             "The editor holds the grid, `move`, `pay` (the reward for entering a cell) and `optimal_sets()`: value iteration's best moves in each open cell, ties kept, with $\\gamma = 0.9$.",
    "question": "Write `q_learn(episodes, seed, alpha=0.2, eps=0.2, q0=0.0)`: start every $Q$ at `q0`, end cells included, and begin each episode at `rng.choice(OPEN)`. "
                "Each step draws `rng.random()`; below `eps` take `rng.choice('URDL')`, else the first best action in the order U, R, D, L. "
                "Entering an end cell, the target is the reward alone. Then write `greedy_ok(Q)`, true when every open cell's first best action is in its optimal set.",
    "widget": {
        "kind": "code", "language": "python",
        "starter": GRID_STARTER,
        "solution": GRID_SOL,
        "examples": [{"call": "q_learn(0, 0)[('r1c1', 'U')]", "expect": "0.0", "compare": "isclose"},
                     {"call": "sorted(optimal_sets()['r3c1'])", "expect": repr(sorted(sets30['r3c1'])), "compare": "equal"}],
        "tests": grid_tests,
        "how": f"Submit runs {len(grid_tests)} hidden tests. Two short seeded runs must match ours within `math.isclose`, so follow the order of random calls and the U, R, D, L tie rule. "
               "One of them starts at `q0 = 0.5`. After 300 episodes the greedy policy must lie in the optimal sets for seeds 0 to 4. "
               "`greedy_ok` must also accept a policy that takes the other of two tied moves.",
        "mutants": [
            {"source": GRID_NO_MASK, "test": 3, "symptom": "Bootstraps from the end cells, whose values stay at q0."},
            {"source": GRID_LAST_TIE, "test": 2, "symptom": "Breaks greedy ties towards L, D, R, U instead of U, R, D, L."},
            {"source": GRID_NO_STEP, "test": 2, "symptom": "Leaves out the 0.05 step cost."},
            {"source": GRID_SARSA, "test": 2, "symptom": "Bootstraps from a sampled next action, as SARSA does, not from the max."},
            {"source": GRID_ARGMAX, "test": 5, "symptom": "Compares with value iteration's first best move only, so a tie taken the other way fails."},
        ],
    },
    "feedback": fb("Q-learning's greedy policy lands in value iteration's optimal sets, ties allowed, without ever seeing the model.",
                   "Read the first failing test.",
                   {"test-2": "Follow the order: `rng.choice(OPEN)` per episode, then `rng.random()` each step, `rng.choice('URDL')` only when exploring, ties to U, R, D, L, and the 0.05 step cost.",
                    "test-3": "Entering an end cell, the target is the reward alone. The end cells' values stay at `q0` and must not be bootstrapped from.",
                    "test-7": "`greedy_ok` must say False when a move is wrong. With every $Q$ at 0 the first best move is U everywhere, which is not optimal at r1c1.",
                    "test-8": "Compare each greedy move with the whole optimal set. At r3c1 both U and R are optimal."}),
    "explain": {"text": "Value iteration needs the model; Q-learning needs only moves and rewards, and its greedy policy reaches the same optimal sets here. "
                        "The comparison must use sets, because at r3c1 U and R tie. "
                        "The terminal mask matters as soon as the end cells hold anything but 0, as a start at `q0 = 0.5` shows."}})

order_d = {2: [], 3: [], 4: [], 5: []}
for it in items:
    order_d[it["difficulty"]].append(it)
exam = {
    "id": "topic-2.8", "topic": "2.8", "name": "Reinforcement learning", "minutes": 90, "pass": 0.7,
    "skills": {"rl-bandit": "Bandits and exploration", "rl-mdp": "Markov decision processes and dynamic programming",
               "rl-td": "Temporal-difference learning", "rl-pg": "Policy gradients", "rl-search": "Search and self-play"},
    "items": order_d[2] + order_d[3] + order_d[4] + order_d[5],
}
with open(OUT, "w", encoding="utf8") as f:
    json.dump(exam, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("wrote", os.path.normpath(OUT), len(exam["items"]), "items, pace", sum(i["pace"] for i in exam["items"]), "s",
      {k: len(v) for k, v in order_d.items()})
