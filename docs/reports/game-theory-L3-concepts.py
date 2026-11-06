"""Concept checks for game-theory L3 (lessons l11 to l15, review-3, homework-3).

Pot odds and outs are recomputed exactly and by Monte Carlo; the hold'em equities by full
enumeration with a 7-card evaluator; combo counts by enumeration; the toy poker equilibria by
best-reply enumeration (cut-down game) and by LP over all 64 pure plans a side (full Kuhn
poker); value of information by exact Bayes; Kelly growth and gambler's ruin exactly and by
simulation; the seeded walk count by replicating the engine's mulberry32. Each assert names
the ledger row it covers. Run: python3 -I docs/reports/game-theory-L3-concepts.py
"""
import math
from fractions import Fraction as F
from itertools import combinations, product

import numpy as np
from scipy.optimize import linprog

rng = np.random.default_rng(20261106)

RANKS = "23456789TJQKA"
SUITS = "shdc"
DECK = [r + s for r in RANKS for s in SUITS]
RV = {r: i + 2 for i, r in enumerate(RANKS)}


def rank5(cards):
    """Rank a 5-card hand: higher tuple wins. Categories 8 straight flush ... 0 high card."""
    vals = sorted((RV[c[0]] for c in cards), reverse=True)
    flush = len({c[1] for c in cards}) == 1
    counts = {}
    for v in vals:
        counts[v] = counts.get(v, 0) + 1
    groups = sorted(counts.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    uniq = sorted(counts, reverse=True)
    straight_high = None
    if len(uniq) == 5:
        if uniq[0] - uniq[4] == 4:
            straight_high = uniq[0]
        elif uniq == [14, 5, 4, 3, 2]:
            straight_high = 5
    if straight_high and flush:
        return (8, straight_high)
    if groups[0][1] == 4:
        return (7, groups[0][0], groups[1][0])
    if groups[0][1] == 3 and groups[1][1] == 2:
        return (6, groups[0][0], groups[1][0])
    if flush:
        return (5, *vals)
    if straight_high:
        return (4, straight_high)
    if groups[0][1] == 3:
        return (3, groups[0][0], *[g[0] for g in groups[1:]])
    if groups[0][1] == 2 and groups[1][1] == 2:
        return (2, groups[0][0], groups[1][0], groups[2][0])
    if groups[0][1] == 2:
        return (1, groups[0][0], *[g[0] for g in groups[1:]])
    return (0, *vals)


def best7(cards):
    return max(rank5(c) for c in combinations(cards, 5))


def equity(hero, villain, board):
    """(wins, ties, total) over every runout to five board cards."""
    dead = set(hero + villain + board)
    live = [c for c in DECK if c not in dead]
    need = 5 - len(board)
    w = t = n = 0
    for run in combinations(live, need):
        b = board + list(run)
        h, v = best7(hero + b), best7(villain + b)
        n += 1
        if h > v:
            w += 1
        elif h == v:
            t += 1
    return w, t, n


# ---------- l11 pot odds and outs ----------
assert F(50, 200) == F(1, 4) and 200 * 0.25 - 50 == 0, "l11 screens[0] break-even 25%"
assert abs(0.3 * 150 - 0.7 * 50 - 10) < 1e-12, "l11 screens[1] call earns 10"
price = lambda B, P: F(B, P + 2 * B)
assert price(50, 100) == F(1, 4) and price(30, 90) == F(1, 5) and price(20, 60) == F(1, 5) and price(25, 75) == F(1, 5), "l11 price B/(P+2B)"
# turn: 8h7h on Kh4h2s9c, villain KcQd: 9 of 44 rivers win (l11 screens[2].explain)
w, t, n = equity(["8h", "7h"], ["Kc", "Qd"], ["Kh", "4h", "2s", "9c"])
assert (w, t, n) == (9, 0, 44), "l11 screens[2] against KcQd exactly 9 of 44 rivers win"
# the three counts the convention question turns on (l11 screens[2]/[3] finding): 9/46, 9/45, 9/44
assert F(9, 46) < F(1, 5) == F(9, 45) < F(9, 44), "l11 screens[3]: 19.57% (46 unseen) < 20% price = 9/45 (his king known) < 20.45% (KcQd known)"
assert abs(9 / 46 * 120 - 37 / 46 * 30 + 0.65) < 0.005, "l11 screens[3] (before the audit fix pass) call earned -0.65 under the 46-card count"
# fix pass: screens[3] is now £40 into £90, price 40/170, a fold under every count
assert F(9, 44) < price(40, 90) == F(4, 17), "l11 screens[3]: price 23.5% is above 9/46, 9/45 and 9/44"
assert F(9, 46) * 130 - F(37, 46) * 40 == F(-155, 23) and abs(-155 / 23 + 6.74) < 0.005, "l11 screens[3] call earns -155/23 = -6.74"
assert abs(9 / 46 * 130 - 25.43) < 0.005 and abs(37 / 46 * 40 - 32.17) < 0.005, "l11 screens[3] win side 25.43, loss side 32.17"
assert F(9, 44) * 130 - F(35, 44) * 40 < 0 and F(9, 45) * 130 - F(36, 45) * 40 < 0, "l11 screens[3] the call loses even against his known cards"
assert abs(9 / 45 * 120 - 36 / 45 * 30) < 1e-12, "l11 screens[3] the same call breaks even exactly once his known king is removed from the unseen cards"
# flop: at least one heart of two cards among 47 unseen: 1 - 38/47 * 37/46 (l11 screens[4])
assert abs(1 - 38 / 47 * 37 / 46 - 0.3497) < 5e-5, "l11 screens[4] 34.97%"
# exact flop equity of 8h7h vs KcQd on Kh4h2s (l11 screens[4].explain claims 376/990)
w, t, n = equity(["8h", "7h"], ["Kc", "Qd"], ["Kh", "4h", "2s"])
assert n == 990, "l11 screens[4] 990 runouts"
assert (w, t) == (376, 0), f"l11 screens[4].explain: exact equity is {w}/990 (ties {t}), text says 376/990"
# two-card draws by simulation (l11 screens[8], review-3 items[2])
def two_card(outs, unseen=47, draws=2 * 10 ** 6):
    deck = np.arange(unseen)
    hit = 0
    for _ in range(4):
        d = rng.permuted(np.tile(deck, (draws // 4, 1)), axis=1)[:, :2]
        hit += (d < outs).any(axis=1).sum()
    return hit / draws


assert abs(two_card(8) - 0.3145) < 0.002 and abs(1 - 39 / 47 * 38 / 46 - 0.3145) < 5e-5, "l11 screens[8] 8 outs twice: 31.45%"
assert abs(two_card(12) - 0.4496) < 0.002 and abs(1 - 35 / 47 * 34 / 46 - 0.4496) < 5e-5, "review-3 items[2] 12 outs twice: 44.96%"
assert abs(two_card(9) - 0.3497) < 0.002, "l11 screens[4] by simulation"
# rule of 2 and 4 is a quick check, not exact
assert abs(9 * 4 / 100 - 0.3497) < 0.011 and abs(12 * 4 / 100 - 0.4496) > 0.03, "l11/review-3: rule of four overstates big draws"
# implied odds (l11 screens[9], homework-3 items[2])
assert abs((38 / 46 * 20) / (8 / 46) - 80 - 15) < 1e-9, "l11 screens[9] X = 15"
assert abs((37 / 46 * 25) / (9 / 46) - 75 - 250 / 9) < 1e-9, "homework-3 items[2] X = 250/9"
# open-ended straight draw on 9s8s / 7d6c2hKs has 8 outs and no flush draw (l11 screens[8] row 1)
outs = 0
dead = {"9s", "8s", "7d", "6c", "2h", "Ks"}
for c in DECK:
    if c in dead:
        continue
    if best7(["9s", "8s", "7d", "6c", "2h", "Ks", c])[0] >= 4:
        outs += 1
assert outs == 8, "l11 screens[8] 8 outs for the open-ended draw"
# quiz q3 why: EV of a call = (chance - price) x final pot
P, B = 100, 50
assert abs((0.2 * (P + B) - 0.8 * B) - (0.2 - 0.25) * (P + 2 * B)) < 1e-9, "l11 quiz[2] each call loses 5% of the final pot"

# ---------- l12 combos ----------
def combos(hand, dead):
    r1, r2, kind = hand[0], hand[1], hand[2:]
    live = [c for c in DECK if c not in dead]
    n = 0
    for a, b in combinations(live, 2):
        if sorted(a[0] + b[0]) != sorted(r1 + r2):
            continue
        suited = a[1] == b[1]
        if kind == "s" and not suited:
            continue
        if kind == "o" and suited:
            continue
        n += 1
    return n


RIVER = ["Ks", "Kh", "Ad", "9c", "6h", "3s", "2d"]
assert combos("AK", ["As"]) == 12 and combos("AA", []) == 6 and combos("AA", ["As"]) == 3, "l12 screens[0], [1]"
assert [combos(h, RIVER) for h in ("AQ", "99", "54s", "JTs", "KQs", "QJs")] == [12, 3, 4, 4, 2, 4], "l12 screens[2], [4], [9] combo counts"
assert combos("AK", ["Ah", "Ac"]) == 8 and combos("AA", ["As", "Ac", "Ad"]) == 0, "l12 screens[3], [6]"
assert combos("QJo", []) == 12 and combos("KQo", ["Ks"]) == 9 and combos("AQ", ["Ad", "Qs"]) == 9, "l12 screens[7], [8], review-3 items[4]"
assert combos("88", ["8s", "8h"]) == 1 and combos("AJs", ["Ac"]) == 3 and combos("JJ", ["Js"]) == 3, "l12 quiz, review-3 items[3]"
assert F(13 * 6, math.comb(52, 2)) == F(1, 17), "l12 screens[8] chance of a pair"
# the river hands really beat or lose to KK on AdD9c6h3s2d (l12 screens[2])
board = ["Ad", "9c", "6h", "3s", "2d"]
hero = best7(["Ks", "Kh"] + board)
for hand, beats in [(("Ac", "Qc"), False), (("9s", "9h"), False), (("5c", "4c"), False), (("Jc", "Tc"), True), (("Kd", "Qd"), True)]:
    assert (hero > best7(list(hand) + board)) == beats, f"l12 screens[2] KK against {hand}"
assert F(6, 25) < F(1, 4) < F(7, 26) and F(9, 28) < F(1, 3) <= F(10, 29), "l12 screens[4], [8], [9] thresholds"
assert abs(6 / 25 * 150 - 19 / 25 * 50 + 2) < 1e-9 and abs(8 / 27 * 150 - 19 / 27 * 50 - 250 / 27) < 1e-9, "l12 screens[5] -2 and +9.26"
# homework-3 items[1] expected values
assert F(sum(combos(h, RIVER) for h in ["JTs"]), sum(combos(h, RIVER) for h in ["AQ", "99", "54s", "JTs"])) == F(4, 23), "homework-3 items[1] 4/23"
assert F(6, 25) == F(combos("JTs", RIVER) + combos("KQs", RIVER), 25) and F(10, 29) == F(10, 29), "homework-3 items[1] 6/25, 10/29"
assert combos("AKo", ["As"]) == 9 and combos("KQs", ["Ks", "Kh"]) == 2 and combos("T9s", ["Ts", "9h"]) == 2, "homework-3 items[1] combo tests"

# ---------- l13 bluffing ----------
bluff = lambda B, P: F(B, P + 2 * B)
calls = lambda B, P: F(P, P + B)
assert bluff(100, 100) == F(1, 3) and calls(100, 100) == F(1, 2), "l13 screens[0], [1]"
assert bluff(50, 100) == F(1, 4) and calls(50, 100) == F(2, 3), "l13 screens[2]"
assert bluff(150, 100) == F(3, 8) and calls(150, 100) == F(2, 5), "l13 screens[6]"
assert bluff(200, 100) == F(2, 5) and calls(200, 100) == F(1, 3) and bluff(75, 100) == F(3, 10) and calls(75, 100) == F(4, 7), "l13 screens[7]"
assert bluff(100, 300) == F(1, 5) and calls(100, 300) == F(3, 4) and bluff(60, 120) == F(1, 4) and calls(60, 120) == F(2, 3) and bluff(100, 150) == F(2, 7) and calls(100, 150) == F(3, 5), "l13 quiz, review-3, homework-3"
assert 0.7 * 100 - 0.3 * 100 == 40, "review-3 items[6] bluff earns +40 against a 30% caller"

# cut-down three-card game (l13 screens[3]): Ana bets or checks; Ben calls or folds. Enumerate Ana's value for strategies
CARDS = [0, 1, 2]  # J, Q, K


def value_cut(beta, ben_call):
    """Ana's expected net with bet frequencies beta[card] and Ben's call frequencies ben_call[card]."""
    tot = F(0)
    for a, b in product(CARDS, repeat=2):
        if a == b:
            continue
        show = 1 if a > b else -1  # antes: win or lose 1 at showdown
        # bet: Ben calls -> +-2, folds -> +1
        bet_ev = ben_call[b] * (2 * show) + (1 - ben_call[b]) * 1
        tot += F(1, 6) * (beta[a] * bet_ev + (1 - beta[a]) * show)
    return tot


EQ_A = {0: F(1, 3), 1: F(0), 2: F(1)}
EQ_B = {0: F(0), 1: F(1, 3), 2: F(1)}
v = value_cut(EQ_A, EQ_B)
assert v == F(1, 18), "l13 screens[3] cut-down game worth +1/18 to Ana"
# equilibrium check: no pure deviation by either side improves on it
for a_dev in product([F(0), F(1)], repeat=3):
    dev = dict(zip(CARDS, a_dev))
    assert value_cut(dev, EQ_B) <= v, "l13 screens[3] Ana cannot gain against Ben's mix"
for b_dev in product([F(0), F(1)], repeat=3):
    dev = dict(zip(CARDS, b_dev))
    assert value_cut(EQ_A, dev) >= v, "l13 screens[3] Ben cannot gain against Ana's mix"
# the Q is indifferent exactly at one jack bet per three kings; the jack bluff is indifferent at a third of queens calling
assert value_cut(EQ_A, {0: F(0), 1: F(0), 2: F(1)}) == value_cut(EQ_A, {0: F(0), 1: F(1), 2: F(1)}) == v, "l13 screens[3] Ben's queen is indifferent"
assert value_cut({0: F(0), 1: F(0), 2: F(1)}, EQ_B) == value_cut({0: F(1), 1: F(0), 2: F(1)}, EQ_B) == v, "l13 screens[3] Ana's jack is indifferent"
# uniqueness of the mix: any other jack rate lets Ben's queen gain by a pure reply
for beta_j in (F(0), F(1, 6), F(1, 2), F(1)):
    alt = {0: beta_j, 1: F(0), 2: F(1)}
    best_ben = min(value_cut(alt, dict(zip(CARDS, bd))) for bd in product([F(0), F(1)], repeat=3))
    assert best_ben < v or beta_j == F(1, 3), "l13 screens[4] only a third keeps Ben's queen indifferent"
# Ana betting every queen too (l13 screens[7] row 4): value -1/9 whatever Ben's queen does
alt = {0: F(1, 3), 1: F(1), 2: F(1)}
vals = {value_cut(alt, {0: F(0), 1: c, 2: F(1)}) for c in (F(0), F(1, 3), F(1))}
assert vals == {F(-1, 9)}, "l13 screens[7] betting the queen: -1/9 against any queen reply"
assert min(value_cut(alt, dict(zip(CARDS, bd))) for bd in product([F(0), F(1)], repeat=3)) == F(-1, 9), "l13 screens[7] Ben's best reply gives -1/9"

# full Kuhn poker (l13 screens[8]): value -1/18 to the first player, by LP over the 64 x 64 pure-strategy matrix
def kuhn_payoff(s1, s2, a, b):
    """s1[card] = (first action 0 check/1 bet, reply to a bet after checking 0 fold/1 call); s2[card] = (facing bet 0 fold/1 call, facing check 0 check/1 bet)."""
    show = 1 if a > b else -1
    first, call_back = s1[a]
    call_vs_bet, bet_vs_check = s2[b]
    if first == 1:
        return 2 * show if call_vs_bet else 1
    if bet_vs_check == 0:
        return show
    return 2 * show if call_back else -1


S1 = list(product(product([0, 1], repeat=2), repeat=3))
S2 = list(product(product([0, 1], repeat=2), repeat=3))
assert len(S1) == len(S2) == 64, "l13 screens[8] 64 pure plans a side"
M = np.zeros((64, 64))
for i, s1 in enumerate(S1):
    for j, s2 in enumerate(S2):
        M[i, j] = sum(kuhn_payoff(dict(zip(CARDS, s1)), dict(zip(CARDS, s2)), a, b) for a in CARDS for b in CARDS if a != b) / 6
shift = abs(M.min()) + 1
Ms = M + shift
c = np.zeros(65)
c[-1] = -1
res = linprog(c, A_ub=np.hstack([-Ms.T, np.ones((64, 1))]), b_ub=np.zeros(64), A_eq=np.hstack([np.ones((1, 64)), np.zeros((1, 1))]), b_eq=[1], bounds=[(0, 1)] * 64 + [(None, None)])
assert res.success and abs(res.x[-1] - shift + 1 / 18) < 1e-7, "l13 screens[8] full Kuhn poker is worth -1/18 to the first player"

# ---------- l14 value of information ----------
assert 90 / 3 == 30 and 90 * (1 / 3 + 2 / 3 * 1 / 2) == 60, "l14 screens[1] 30, 60, worth 30"
voi = lambda pays, probs, acc: None
def analyst(payoffs, probs, acc):
    """Value of a symmetric binary signal with accuracy acc on a take/skip trade."""
    win_pay, lose_pay = payoffs
    pw, pl = probs
    now = max(0.0, pw * win_pay + pl * lose_pay)
    p_good = acc * pw + (1 - acc) * pl
    ev_good = (acc * pw * win_pay + (1 - acc) * pl * lose_pay) / p_good
    ev_bad = ((1 - acc) * pw * win_pay + acc * pl * lose_pay) / (1 - p_good)
    with_it = p_good * max(0.0, ev_good) + (1 - p_good) * max(0.0, ev_bad)
    return with_it - now, now, ev_good, ev_bad


v5, now, g, b = analyst((30, -20), (0.5, 0.5), 0.8)
assert abs(v5 - 5) < 1e-12 and abs(g - 20) < 1e-12 and abs(b + 10) < 1e-12 and now == 5, "l14 screens[3] 80% analyst worth 5"
assert abs(analyst((30, -20), (0.5, 0.5), 1.0)[0] - 10) < 1e-12, "l14 screens[2] perfect information worth 10"
assert abs(analyst((50, -10), (0.5, 0.5), 0.8)[0]) < 1e-12, "l14 screens[4] worth 0 when no message flips the move"
assert abs(analyst((30, -20), (0.5, 0.5), 0.6)[0]) < 1e-12 and abs(analyst((30, -20), (0.5, 0.5), 0.7)[0] - 2.5) < 1e-12, "l14 screens[5] 0 and 2.5"
assert abs(analyst((30, -20), (0.5, 0.5), 0.9)[0] - 7.5) < 1e-12, "review-3 items[7] 7.5"
assert abs(analyst((40, -40), (0.6, 0.4), 1.0)[0] - 16) < 1e-12, "l14 quiz[0] 16"
assert abs(analyst((40, -20), (0.4, 0.6), 1.0)[0] - 12) < 1e-12 and abs(analyst((40, -20), (0.4, 0.6), 0.75)[0] - 5) < 1e-12, "homework-3 items[4] 12 and 5"
# VOI is never negative and at most the perfect-information value, over a grid of accuracies and payoffs
for acc in np.linspace(0.5, 1, 26):
    for wp in (10, 30, 50):
        v_, _, _, _ = analyst((wp, -20), (0.5, 0.5), acc)
        assert -1e-12 <= v_ <= analyst((wp, -20), (0.5, 0.5), 1.0)[0] + 1e-12, "l14 screens[6] bounds on VOI"
assert abs(sum(max(x, 3) for x in range(1, 7)) / 6 - max(3.5, 3) - 0.5) < 1e-12, "l14 screens[7] die worth 0.5"
assert abs(6 / 25 * 150 - 36) < 1e-12, "l14 screens[7] seeing his cards worth 36"
pw = 0.24
weak = pw * 0.8 + (1 - pw) * 0.2
assert abs(weak - 43 / 125) < 1e-12 and abs(pw * 0.8 / weak - 24 / 43) < 1e-12 and abs((1 - pw) * 0.8 / (1 - weak) - 38 / 41) < 1e-12, "l14 screens[8] tell probabilities"
assert abs(0.192 * 150 - 0.152 * 50 - 21.2) < 1e-9 and 24 / 43 * 150 - 19 / 43 * 50 > 0 and 3 / 41 * 150 - 38 / 41 * 50 < 0, "l14 screens[8] tell worth 21.20"
assert abs(0.5 * 10 - 5) < 1e-12, "l14 quiz[2] seeing the coin worth 5"

# ---------- l15 Kelly and ruin ----------
g = lambda f, p=0.3, b=4: p * math.log(1 + b * f) + (1 - p) * math.log(1 - f)
fs = np.linspace(0, 0.4, 40001)
gs = np.array([g(f) for f in fs])
assert abs(fs[gs.argmax()] - 0.125) < 1e-4 and abs(gs.max() - 0.02817) < 1e-5, "l15 screens[0] Kelly 0.125, growth 0.02817"
assert abs(g(0.0625) - 0.02177) < 1e-5 and abs(g(0.25) - 0.00657) < 1e-5 and abs(g(0.3) + 0.0131) < 1e-4, "l15 screens[2], [4]"
root = fs[(gs[1:] < 0).argmax()]
assert abs(root - 0.268) < 0.002, "l15 screens[0] growth turns negative past about 0.268"
assert abs(g(0.0625) / g(0.125) - 0.77) < 0.01, "l15 screens[2] half Kelly keeps 77% of growth"
# long-run growth equals the mean log return: simulate 10^6 bets at f = 0.125 and at f = 0.3
wins = rng.random((20, 50000)) < 0.3
for f, exp in [(0.125, 0.02817), (0.3, -0.0131)]:
    lr = np.where(wins, np.log(1 + 4 * f), np.log(1 - f)).mean()
    assert abs(lr - exp) < 0.002, f"l15 simulated growth at f = {f}"
assert abs(0.3 ** 10 - 5.9e-6) < 1e-7, "l15 screens[1] survive ten all-ins"
kelly = lambda p, b: p - (1 - p) / b
assert kelly(0.25, 3) == 0 and abs(kelly(0.45, 2) - 0.175) < 1e-12 and abs(kelly(0.4, 3) - 0.2) < 1e-12 and abs(kelly(0.3, 3) - 1 / 15) < 1e-12, "l15 screens[5], [7], quiz[0], review-3 items[8]"
assert abs(g(0.175, 0.45, 2) - 0.02924) < 1e-5, "l15 screens[7] growth 0.02924"
assert all(g(f, 0.25, 3) < 0 for f in np.linspace(0.001, 0.5, 100)), "l15 screens[5] with no edge every stake shrinks the bankroll"
assert abs(g(0.125, 0.25, 4) - 0.0012) < 1e-4 and abs(g(0.0625, 0.25, 4) - 0.0074) < 1e-4, "l15 screens[8], homework-3 items[5]"
assert abs(kelly(0.25, 4) - 0.0625) < 1e-12 and abs(kelly(0.35, 4) - 0.1875) < 1e-12, "l15 screens[8] Kelly range"
ruin = lambda p, n: ((1 - p) / p) ** n
assert abs(ruin(0.55, 5) - 0.3666) < 5e-5 and abs(ruin(0.55, 10) - 0.1344) < 5e-5 and abs(ruin(0.55, 20) - 0.0181) < 5e-5, "l15 screens[3]"
assert abs(ruin(0.52, 15) - 0.3010) < 5e-5 and abs(ruin(0.6, 8) - 0.0390) < 5e-5 and abs(ruin(0.55, 15) - 0.0493) < 5e-5, "l15 screens[7], quiz[1], review-3 items[9]"
assert abs(math.exp(-2 * 0.05 * 1500 / 64) - 0.0960) < 5e-5 and abs(math.exp(-2 * 0.05 * 1000 / 64) - 0.2096) < 5e-5 and abs(math.exp(-2 * 0.05 * 2000 / 64) - 0.0439) < 5e-5, "l15 screens[7] poker ruin"
assert abs(math.sqrt(ruin(0.55, 20)) - ruin(0.55, 10)) < 1e-12, "homework-3 items[6] doubling the stake takes the square root"
# gambler's ruin by simulation: 10 stakes at 55%, 200000 walks of 2000 steps (ruin after 2000 steps is negligible)
N, steps = 200000, 2000
pos = np.full(N, 10)
alive = np.ones(N, bool)
for _ in range(steps):
    step = np.where(rng.random(N) < 0.55, 1, -1)
    pos = np.where(alive, pos + step, pos)
    alive &= pos > 0
assert abs((~alive).mean() - 0.1344) < 0.004, "l15 screens[3] simulated ruin with 10 stakes near 13.44%"


# the seeded walk (l15 screens[3].explain: "Seed 4 shows 46 of 300 broke"), replicating app/js/engine/sim.js mulberry32 and canvas/walk.js draws
def mulberry32(seed):
    a = seed & 0xFFFFFFFF

    def imul(x, y):
        return (x * y) & 0xFFFFFFFF

    def nxt():
        nonlocal a
        a = (a + 0x6D2B79F5) & 0xFFFFFFFF
        t = a
        t = imul(t ^ (t >> 15), t | 1)
        t ^= (t + imul(t ^ (t >> 7), t | 61)) & 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296

    return nxt


def walk_hits(seed=4, paths=300, steps=400, p=0.55, start=10):
    r = mulberry32((seed * 7919) & 0xFFFFFFFF)

    def gauss():
        u = 0
        while u <= 1e-12:
            u = r()
        r()  # the cosine draw

    hits = 0
    for _ in range(paths):
        u = []
        for _ in range(steps):
            u.append(r())
            gauss()
        pos = start
        for ui in u:
            pos += 1 if ui < p else -1
            if pos <= 0:
                hits += 1
                break
    return hits


assert walk_hits() == 46, "l15 screens[3].explain: seed 4 shows 46 of 300 broke"
print("game-theory L3 concepts: all checks passed")
