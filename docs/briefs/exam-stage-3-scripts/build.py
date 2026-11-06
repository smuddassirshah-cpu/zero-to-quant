"""Build app/content/exams/stage-3.json, the Stage 3 exit test (topics 3.1, 3.3 and 3.5; 3.2 and 3.4 are optional).

Route A for every key: closed forms, exact Fractions and the reference solution below. check_numbers.py recomputes each
value by a second route (enumeration, numerical integration, exact binomial sums, simulation) and asserts it at its
path in the written file. Run: python3 docs/briefs/exam-stage-3-scripts/build.py
"""
import json
import math
import os
from fractions import Fraction as F
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'stage-3.json')
N = NormalDist()


def r(x, n=6):
    return round(float(x), n)


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


def choice(options):
    return {"kind": "choice", "layout": "stack", "shuffle": True, "options": options}


def multi(options):
    return {"kind": "multi", "layout": "stack", "shuffle": True, "options": options}


def opt(id, text, why=None, correct=False):
    o = {"id": id, "text": text}
    if correct:
        o["correct"] = True
    if why:
        o["why"] = why
    return o


def line(id, text, why=None):
    d = {"id": id, "text": text}
    if why:
        d["why"] = why
    return d


def item(id, d, skills, tags, pace, title, prose, question, widget, feedback, explain):
    it = {"id": id, "difficulty": d, "skills": skills, "tags": tags, "pace": pace, "title": title}
    if prose:
        it["prose"] = prose
    it.update({"question": question, "widget": widget, "feedback": feedback, "explain": {"text": explain}})
    return it


def parts(id, d, skills, tags, pace, title, prose, question, ps, explain):
    return {"id": id, "difficulty": d, "skills": skills, "tags": tags, "pace": pace, "title": title,
            "prose": prose, "question": question, "parts": [{"question": q, "widget": w, "feedback": f} for q, w, f in ps],
            "explain": {"text": explain}}


def why_map(options):
    return {o["id"]: o["why"] for o in options if "why" in o}


A, C = [], []

# ======================================================================== Paper A: probability and expected value
# A1 conditioning on an even product
a1 = F(9, 27)
A.append(item("a-even-product", 2, ["pz-conditioning"], ["dice-condition"], 75, "An even product",
    "Two fair dice are rolled. You are told only that the product of the faces is even.",
    "What is the chance that their sum is even? Give a fraction or 4 decimal places.",
    num(r(a1), 0.0005, [("ignored-news", 0.5, 0.0005), ("whole-table", r(F(9, 36)), 0.0005)],
        placeholder="fraction or decimal", accept="Any form equal to 1/3, or 0.3333 ± 0.0005"),
    fb("Nine of the 27 rolls with an even product have an even sum.", "List the rolls the news leaves, then count those with an even sum.",
       {"ignored-news": "You gave the chance before the news. An even product rules out every odd-odd roll.",
        "whole-table": "You counted the 9 even-even rolls out of all 36. Divide by the 27 rolls with an even product."}),
    "An even product rules out the 9 odd-odd rolls, leaving 27. Given that, the sum is even only when both faces are even: 9 rolls. "
    "So the chance is $\\tfrac{9}{27} = \\tfrac13$."))

# A2 a roll that repeats the one before
a2 = 1 + 6
A.append(item("a-repeat-roll", 2, ["pz-expectation"], ["repeat-wait"], 75, "Until a roll repeats",
    "Roll a fair die again and again. Stop at the first roll that shows the same face as the roll before it.",
    "How many rolls do you expect to make, counting the last one?",
    num(a2, 0, [("no-first", 6, 0), ("one-pair", 36, 0)]),
    fb("One roll to start, then a wait of 6 on average.", "The first roll cannot match. After it, what is the chance each roll matches the one before?",
       {"no-first": "You counted the wait for a match but not the first roll, which has nothing to match.",
        "one-pair": "You waited for one fixed pair of faces. Any face will do, as long as it equals the one before."}),
    f"The first roll cannot match. After it, each roll matches the one before with chance $\\tfrac16$, whatever came earlier. "
    f"So we expect $1 + 6 = {a2}$ rolls."))

# A3 a watch that ends on two busy hours in a row (a two-state chain)
a3, b3 = 0.2, 0.5                      # chance of busy after a quiet hour; of busy after a busy hour
a3n = (1 + a3) / (a3 * b3)
a3w = a3 * b3 / (1 - a3 * (1 - b3))
A.append(parts("a-lead-by-two", 3, ["pz-recursion"], ["regime-chain"], 180, "Two busy hours",
    "A venue's order flow is quiet or busy each hour. After a quiet hour, the next is busy with chance 0.2. "
    "After a busy hour, the next is busy again with chance 0.5. The venue is quiet now.",
    "Two questions on the hours to come.",
    [("You watch until two busy hours come in a row. How many hours do you expect to watch, counting the last? Give a whole number.",
      num(r(a3n), 0, [("first-busy", r(1 / a3), 0), ("fresh-tries", r(1 / (a3 * b3)), 0)]),
      fb("From a quiet hour the wait is 12, and from a busy hour it is 7.",
         "Write the expected wait after a quiet hour and after a busy hour, each in terms of the other.",
         {"first-busy": "You counted the wait for the first busy hour. A second must follow it at once.",
          "fresh-tries": "You took one over $0.2 \\times 0.5$, as if each hour began a fresh try. A failed try leaves you busy or quiet, so track which."})),
     ("Count the quiet hour just gone. What is the chance that two busy hours in a row come before two quiet hours in a row? Give 4 decimal places.",
      num(r(a3w), 0.0005, [("next-busy", a3, 0.0005), ("one-route", a3 * b3, 0.0005)]),
      fb("From a quiet hour the race is won only through a busy one.",
         "Let $w$ be the winning chance after a quiet hour and after a busy hour, and link the two.",
         {"next-busy": "You gave the chance that the next hour is busy. A second busy hour must still follow.",
          "one-route": "You counted busy then busy only. After busy then quiet the race is still open."}))],
    f"Let $E_Q$ and $E_B$ be the expected hours still to watch after a quiet hour and after a busy hour. "
    f"Then $E_Q = 1 + 0.8E_Q + 0.2E_B$ and $E_B = 1 + 0.5E_Q$, so $E_Q = {a3n:.0f}$. "
    f"For the race, $w_Q = 0.2w_B$ and $w_B = 0.5 + 0.5w_Q$, so $w_Q = \\tfrac{{1}}{{9}} \\approx {a3w:.4f}$."))

# A4 two people side by side at a round table
a4 = F(2, 9)
o4 = [opt("a", "$\\tfrac{2}{9}$", correct=True),
      opt("b", "$\\tfrac{1}{5}$", "You counted 2 neighbouring seats out of 10. The first head takes a seat, so 9 are left."),
      opt("c", "$\\tfrac{1}{9}$", "You counted one neighbouring seat. At a round table everyone has two neighbours."),
      opt("d", "$\\tfrac{1}{45}$", "You fixed both heads in one pair of seats. The first head may sit anywhere.")]
A.append(item("a-round-table", 3, ["pz-symmetry"], ["seating-symmetry"], 90, "Side by side",
    "Ten traders, two of them desk heads, take the ten seats of a round table in a random order.",
    "What is the chance that the two desk heads sit next to each other?",
    choice(o4),
    fb("Seat the first head, then place the second.", "Wherever the first head sits, how many seats are left, and how many touch hers?",
       why_map(o4)),
    "Seat the first head anywhere; by symmetry her seat does not matter. The second head is then equally likely to take any of the 9 other seats. "
    "Two of those touch the first head's seat, so the chance is $\\tfrac29$."))

# A5 a point past the diagonal and inside the circle
a5 = math.pi / 2 - 1
A.append(item("a-uniform-product", 3, ["pz-geometry"], ["area-in-square"], 150, "Past the diagonal",
    "A point $(X, Y)$ is chosen uniformly in the unit square, and you are told that $X + Y > 1$.",
    "What is the chance that $X^2 + Y^2 < 1$? Give 4 decimal places.",
    num(r(a5), 0.0005, [("ignored-news", r(math.pi / 4), 0.0005), ("not-divided", r(math.pi / 4 - 0.5), 0.0005)]),
    fb("A sliver of area $\\tfrac{\\pi}{4} - \\tfrac{1}{2}$ out of a triangle of area $\\tfrac{1}{2}$.",
       "The news keeps the triangle above the diagonal. How much of the quarter disc lies there?",
       {"ignored-news": "You gave the chance of landing in the quarter disc. The news cuts the square to the triangle above the diagonal.",
        "not-divided": "You found the area of the part inside the circle. Divide by the triangle's area, one half."}),
    f"Given $X + Y > 1$, the point is uniform on a triangle of area $\\tfrac{{1}}{{2}}$. "
    f"The part inside the circle is the quarter disc, area $\\tfrac{{\\pi}}{{4}}$, less the lower triangle of area $\\tfrac{{1}}{{2}}$. "
    f"So the chance is $(\\tfrac{{\\pi}}{{4}} - \\tfrac{{1}}{{2}}) / \\tfrac{{1}}{{2}} = \\tfrac{{\\pi}}{{2}} - 1 \\approx {a5:.4f}$."))

# A6 a two-by-two game with no saddle point
M6 = [[2, -1], [-3, 4]]
p6 = (M6[1][1] - M6[1][0]) / (M6[0][0] - M6[1][0] - M6[0][1] + M6[1][1])
v6 = p6 * M6[0][0] + (1 - p6) * M6[1][0]
q6 = (M6[1][1] - M6[0][1]) / (M6[0][0] - M6[0][1] - M6[1][0] + M6[1][1])
half6 = min(0.5 * M6[0][0] + 0.5 * M6[1][0], 0.5 * M6[0][1] + 0.5 * M6[1][1])
A.append(parts("a-quote-game", 3, ["gm-mixed"], ["two-by-two-mixed"], 180, "A mix of two quotes",
    "A market maker plays a repeated game with an arbitrageur. Each round she quotes tight or wide, and he trades or waits. "
    "Her gain per round, in £, is his loss:\n\n| | Trade | Wait |\n|---|---|---|\n| Tight | 2 | −1 |\n| Wide | −3 | 4 |",
    "Two questions on her best mix.",
    [("With what chance should she quote tight, so that his choice does not matter? Give 1 decimal place.",
      num(r(p6), 0.05, [("his-mix", r(q6), 0.02), ("pure-tight", 1, 0.02)]),
      fb("Make his two choices cost him the same.", "Write her average gain against Trade and against Wait, as functions of her tight share $p$.",
         {"his-mix": "You made her indifferent, which fixes his mix. Her mix must make his two choices pay the same.",
          "pure-tight": "You chose her best row against Trade. A pure quote is read and exploited."})),
     ("At that mix, what does she gain per round on average, in £? Give 1 decimal place.",
      num(r(v6), 0.05, [("pure-maximin", -1, 0.02), ("half-half", r(half6), 0.02)], unit="£"),
      fb("The same gain against either reply.", "Put her mix into either column.",
         {"pure-maximin": "You gave the most she can guarantee with one pure quote. Mixing raises it.",
          "half-half": "You mixed half and half. Then he trades, and she loses £0.50 a round."}))],
    f"Against Trade her tight share $p$ earns $2p - 3(1 - p)$; against Wait it earns $-p + 4(1 - p)$. "
    f"Setting them equal gives $10p = 7$, so $p = {p6:.1f}$. She then gains $2(0.7) - 3(0.3) = £{v6:.2f}$ a round whatever he does."))

# A7 a parent order that must land exactly on 5 lots
p7 = [1.0, 0.6]
for n_ in range(2, 6):
    p7.append(0.6 * p7[n_ - 1] + 0.4 * p7[n_ - 2])
a7 = p7[5]
A.append(item("a-six-or-nine", 3, ["pz-recursion"], ["landing-on-a-total"], 150, "Exactly five lots",
    "A parent order is worked in slices. Each slice fills 1 lot with chance 0.6 or 2 lots with chance 0.4, independently. "
    "After each slice, the lots filled so far are totalled.",
    "What is the chance that the total is exactly 5 lots after some slice? Give 4 decimal places.",
    num(r(a7), 0.0005, [("one-route", r(0.6 ** 5), 0.0005), ("tick-four", r(p7[4]), 0.0005), ("long-run", r(1 / 1.4), 0.0005)]),
    fb("Land on 5 from 4 by one lot, or from 3 by two.", "The last slice came from 4 lots or from 3. Build the chances up from 1 lot.",
       {"one-route": "You counted five single-lot slices only. Slices of 2 lots can land on 5 as well.",
        "tick-four": "You gave the chance of landing on 4 lots. Take one more step of the recursion.",
        "long-run": "You gave the long-run chance, one over the mean slice of 1.4 lots. At 5 lots it has not quite settled."}),
    f"The last slice to land on $n$ lots came from $n - 1$ or $n - 2$, so $p_n = 0.6p_{{n-1}} + 0.4p_{{n-2}}$. "
    f"With $p_0 = 1$ and $p_1 = 0.6$ this gives {p7[2]:.2f}, {p7[3]:.3f}, {p7[4]:.4f} and {p7[5]:.5f}. "
    f"So the chance of landing on 5 lots is about {a7:.4f}."))

# A8 wins before the third loss
a8 = 3 * 0.75 / 0.25
A.append(item("a-third-loss", 3, ["pz-expectation"], ["wins-before-losses"], 120, "Wins before the third loss",
    "A trader takes one bet a day. Each bet wins with chance 0.75, independently. She stops for the month after her third losing bet.",
    "How many winning bets do you expect before she stops?",
    num(a8, 0.01, [("all-bets", 3 / 0.25, 0.01), ("first-loss", 0.75 / 0.25, 0.01)]),
    fb("Three runs of wins, each with mean 3.", "Split the bets at each loss. How many wins come before one loss, on average?",
       {"all-bets": "You counted every bet, the three losses too. Only the wins are asked for.",
        "first-loss": "You counted the wins before the first loss only. She stops at the third."}),
    f"Before each loss comes a run of wins with mean $\\tfrac{{0.75}}{{0.25}} = 3$. Three losses means three such runs. "
    f"So we expect $3 \\times 3 = {a8:.0f}$ winning bets."))

# A9 an all-pay auction
v9 = 0.8
a9 = v9 ** 2 / 2
A.append(item("a-all-pay", 4, ["gm-auction"], ["all-pay-auction"], 210, "Everyone pays",
    "Two firms bid for a licence in an all-pay auction. Each pays its own bid, and only the higher bid wins. "
    "Each firm's value is private and uniform from £0 to £1 million. Both use the same increasing bidding rule.",
    "In equilibrium, what does a firm with value £0.8 million bid, in £ millions? Give 2 decimal places.",
    num(r(a9), 0.005, [("first-price", 0.4, 0.002), ("truthful", 0.8, 0.002)], unit="£m"),
    fb("The rule is $b(v) = v^2/2$.", "Bid as if your value were $w$: you win with chance $w$ and always pay $b(w)$.",
       {"first-price": "You used the first-price bid $v/2$. Here a loser pays too, so bids are lower.",
        "truthful": "You bid your value, as in a second-price auction. In an all-pay auction that loses money on every defeat."}),
    f"Bidding as if your value were $w$ wins with chance $w$ and costs $b(w)$ for sure, so you maximise $vw - b(w)$. "
    f"At $w = v$ the first-order condition gives $b'(v) = v$, so $b(v) = v^2/2$. At $v = 0.8$ the bid is £{a9:.2f} million."))

# A10 a skewed bet that is rarely ahead
n10, p10, win10, lose10 = 8, 0.3, 3, 1
pmf = [math.comb(n10, k) * p10 ** k * (1 - p10) ** (n10 - k) for k in range(n10 + 1)]
need10 = next(k for k in range(n10 + 1) if win10 * k - lose10 * (n10 - k) > 0)
a10 = sum(pmf[need10:])
level10 = sum(pmf[need10 - 1:])
four10 = sum(pmf[need10 + 1:])
A.append(item("a-edge-hundred", 4, ["pz-games"], ["edge-and-luck"], 180, "Skewed bets",
    "A strategy takes 8 independent bets. Each wins £3 with chance 0.3 and otherwise loses £1.",
    "What is the chance that she finishes ahead overall? Give 4 decimal places.",
    num(r(a10), 0.0005, [("level-counts", r(level10), 0.0005), ("four-wins", r(four10), 0.0005)]),
    fb("Three wins or more, since $3k - (8 - k) > 0$ needs $k \\ge 3$.",
       "Turn the profit into a count of wins, find the fewest that leave her ahead, then add that tail.",
       {"level-counts": "You counted finishing level as ahead. Two wins leave her exactly even, so ahead needs three.",
        "four-wins": "You asked for four wins. Three wins give $9 - 5 = £4$, which is already ahead."}),
    f"With $k$ wins her profit is $3k - (8 - k) = 4k - 8$, so she is ahead when $k \\ge 3$. "
    f"The chances of 0, 1 and 2 wins are {pmf[0]:.4f}, {pmf[1]:.4f} and {pmf[2]:.4f}. "
    f"So she is ahead with chance about {a10:.4f}, though each bet has a positive edge of £0.20."))

# A11 which broker is it: a posterior and then a prediction
pc11, hit_c, hit_s = F(2, 5), F(9, 10), F(3, 5)
lc11, ls11 = hit_c ** 2 * (1 - hit_c), hit_s ** 2 * (1 - hit_s)
wc11, ws11 = pc11 * lc11, (1 - pc11) * ls11
post_c11 = wc11 / (wc11 + ws11)
a11 = post_c11 * hit_c + (1 - post_c11) * hit_s
prior11 = pc11 * hit_c + (1 - pc11) * hit_s
A.append(item("a-two-flags", 4, ["pz-conditioning"], ["broker-type"], 180, "Which broker is it?",
    "A desk is sent one broker for the day. The broker is careful with chance 0.4 and sloppy with chance 0.6. "
    "A careful broker fills each order at the quoted price with chance 0.9, a sloppy one with chance 0.6. "
    "Given the broker, orders fill independently. Today's first three orders were filled, filled, not filled.",
    "What is the chance that the fourth order is filled? Give 4 decimal places.",
    num(r(a11), 0.0005, [("ignored-orders", r(prior11), 0.0005), ("sample-rate", r(F(2, 3)), 0.0005), ("who-careful", r(post_c11), 0.0005)]),
    fb("Update the broker's type on all three orders, then weigh each type's fill chance.",
       "Weigh a careful broker and a sloppy one by the chance of filled, filled, not filled.",
       {"ignored-orders": "You used the prior mix of brokers. The three orders tell you more about who it is.",
        "sample-rate": "You used the fill rate of the three orders. The broker's type, not the sample, sets the next chance.",
        "who-careful": "You gave the chance that the broker is careful. The question asks about the next fill."}),
    f"Filled, filled, not filled has chance $0.9^2 \\times 0.1 = {float(lc11):.3f}$ for a careful broker and $0.6^2 \\times 0.4 = {float(ls11):.3f}$ for a sloppy one. "
    f"With the priors the weights are {float(wc11):.4f} and {float(ws11):.4f}, so the broker is careful with chance $\\tfrac{{3}}{{11}}$. "
    f"The next order fills with chance $\\tfrac{{3}}{{11}}(0.9) + \\tfrac{{8}}{{11}}(0.6) = \\tfrac{{15}}{{22}} \\approx {float(a11):.4f}$."))

# A12 a buyer who may know
xs = range(1, 101)
prior12 = sum(xs) / 100
p_inf_buy = sum(1 for x in xs if x > 55) / 100
mean_inf_buy = sum(x for x in xs if x > 55) / sum(1 for x in xs if x > 55)
w_noise, w_inf = 0.5 * 0.5, 0.5 * p_inf_buy
pbuy12 = w_noise + w_inf
post12 = (w_noise * prior12 + w_inf * mean_inf_buy) / pbuy12
pnl12 = 55 - post12
even12 = (prior12 + mean_inf_buy) / 2
A.append(parts("a-informed-buyer", 5, ["mg-update"], ["adverse-selection"], 300, "A buyer who may know",
    "The interviewer picks a whole number $X$ from 1 to 100, each equally likely. You quote 45 bid, 55 ask on $X$. "
    "Half the time the trader knows $X$: he buys if $X > 55$, sells if $X < 45$, and otherwise does nothing. "
    "Otherwise he does not know $X$, and buys or sells with chance one half each.",
    "Three questions on one trade.",
    [("What is the chance that the trader buys from you? Give 3 decimal places.",
      num(r(pbuy12), 0.0005, [("noise-only", 0.5, 0.0005), ("informed-only", r(p_inf_buy), 0.0005)]),
      fb("Add the noise buys and the informed buys.", "Weight each kind of trader by one half.",
         {"noise-only": "You gave the noise trader's chance alone. Half the time the trader is informed.",
          "informed-only": "You gave the informed trader's chance alone. Half the time the trader buys at random."})),
     ("He buys at 55. What is your new fair value for $X$? Give 2 decimal places.",
      num(r(post12), 0.005, [("all-informed", mean_inf_buy, 0.002), ("no-update", prior12, 0.002), ("equal-weights", r(even12), 0.002)]),
      fb("A buy is news, but only partly.", "Weigh the noise buys, with mean 50.5, against the informed buys, with mean 78.",
         {"all-informed": "You treated every buyer as informed. Half the buyers trade at random and carry no news.",
          "no-update": "You kept the prior. A buy is likelier when $X$ is high, so it moves fair value up.",
          "equal-weights": "You weighted the two kinds of buyer equally. Their weights are 0.25 and 0.225."})),
     ("On average, what is that one sale at 55 worth to you, in points? Give 2 decimal places.",
      num(r(pnl12), 0.005, [("sign", r(-pnl12), 0.005), ("prior-value", 55 - prior12, 0.002)]),
      fb("Sale price minus the new fair value.", "You sold at 55 something now worth your new fair value.",
         {"sign": "You gave the loss as a gain. You sold at 55 something now worth more.",
          "prior-value": "You valued the sale against the prior 50.5. The buy itself is news."}))],
    f"Buys come from noise with weight $0.25$ and from informed traders with weight $0.5 \\times 0.45 = 0.225$. "
    f"So $E[X \\mid \\text{{buy}}] = (0.25 \\times 50.5 + 0.225 \\times 78) / 0.475 \\approx {post12:.2f}$. The sale at 55 then loses about {-pnl12:.2f} on average."))

# ======================================================================== Paper C: research papers (3.1)
# C1 backfill
o1 = [opt("a", "Backfill bias: the early records were chosen for being good.", correct=True),
      opt("b", "Survivorship bias: funds that closed have dropped out of the data.", "You named the bias from funds that close. Here funds join with a chosen past."),
      opt("c", "Look-ahead bias: returns are known before they happen.", "You named a timing leak. No trade here uses data from the future."),
      opt("d", "Data snooping: many rules were tried on one sample.", "You named a search over many rules. No rule was searched here.")]
C.append(item("r-backfill", 2, ["rm-data"], ["backfill-bias"], 90, "A history that arrives late",
    "A hedge fund database lets a fund start reporting whenever it likes. A fund that joins also loads its past returns. "
    "Funds tend to join after a good year.",
    "Which bias does this put in the database's average return?",
    choice(o1),
    fb("The loaded history was chosen after the fact.", "Ask which funds choose to join, and when.", why_map(o1)),
    "A fund that joins after a good run brings that run with it. So the database's early years look better than a typical fund's record. "
    "A fix is to drop each fund's returns from before its join date."))

# C2 weights that see the month they trade
o2 = [opt("a", "The weights use month $t$'s return to trade month $t$.", correct=True),
      opt("b", "A 6-month window is too short to rank on.", "You questioned the window. Jegadeesh and Titman rank on 3 to 12 months; the bug is timing."),
      opt("c", "Summed returns should be compounded first.", "You looked at sums against products. That moves a few ranks, not 6% a month."),
      opt("d", "The loser leg should be dropped, since shorting losers is costly.", "You changed the design. Dropping losers does not explain 6% a month.")]
C.append(item("r-same-month", 2, ["rm-portfolios"], ["look-ahead-code"], 90, "Six per cent a month",
    "A colleague's momentum backtest earns 6% a month. `ret` holds monthly returns, one row a month. `rank_weights` "
    "sets +1 on winners and −1 on losers in each row.\n\n```python\nw = rank_weights(ret.rolling(6).sum())\npnl = (w * ret).sum(axis=1)\n```",
    "What is wrong?",
    choice(o2),
    fb("Row $t$ of the weights already knows month $t$.", "Check which months row $t$ of the rolling sum contains.", why_map(o2)),
    "Row $t$ of the rolling sum includes month $t$, and `pnl` multiplies it by month $t$ again. The book earns the returns it ranked on, which is look-ahead. "
    "Use `w.shift(1)`, so month $t$ trades on weights set at the end of month $t - 1$."))

# C3 funds that close
alive3, dead3, ra3, rd3 = 160, 40, 9.0, -15.0
true3 = (alive3 * ra3 + dead3 * rd3) / (alive3 + dead3)
c3 = ra3 - true3
C.append(item("r-closed-funds", 2, ["rm-data"], ["survivorship-funds"], 90, "Only the funds still open",
    "A database follows 200 funds through one year. 40 close during the year, with an average return of −15% up to closing. "
    "The 160 that survive average 9%. The database keeps only the funds still open at the year end.",
    "By how many percentage points does it overstate the average fund's return? Give 1 decimal place.",
    num(r(c3), 0.05, [("true-mean", r(true3), 0.02), ("equal-groups", r(ra3 - (ra3 + rd3) / 2), 0.02)]),
    fb("Survivors' 9% against a true 4.2%.", "Weight the two groups by their numbers of funds, then compare with 9%.",
       {"true-mean": "You gave the true average. The question asks for the gap from the reported 9%.",
        "equal-groups": "You averaged the two groups equally. Weight them by 160 and 40 funds."}),
    f"The true average weights both groups: $0.8 \\times 9\\% + 0.2 \\times (-15\\%) = {true3:.1f}\\%$. The database reports the survivors' 9%. "
    f"So it overstates by $9 - {true3:.1f} = {c3:.1f}$ points."))

# C4 Fama and French's June rule
o4c = [opt("a", "The year ending March 2014", correct=True),
       opt("b", "The year ending March 2015", "You took the latest year end. March 2015 falls in calendar 2015, and June may be too soon for those accounts."),
       opt("c", "The year ending December 2014", "You used a calendar year. This firm's years end in March."),
       opt("d", "The year ending March 2016", "You used accounts from after June 2015. That is look-ahead.")]
C.append(item("r-june-book", 3, ["rm-paper"], ["point-in-time-accounts"], 120, "Book equity in June",
    "Fama and French (1993) form portfolios at the end of June of year $t$. They use book equity from the fiscal year ending in calendar year $t - 1$. "
    "A firm's fiscal year ends in March.",
    "You form portfolios at the end of June 2015 by their rule. Which year's book equity does the firm contribute?",
    choice(o4c),
    fb("The fiscal year ending in calendar 2014.", "Find calendar year $t - 1$, then the firm's year end inside it.", why_map(o4c)),
    "Here $t - 1 = 2014$, and the firm's fiscal year in 2014 ends in March. The rule leaves at least six months between a year end and its use. "
    "That gap makes sure the accounts were public by June 2015."))

# C5 which choices leak
o5 = [opt("a", "Scale 2009 returns by each share's volatility over 1990 to 2024.", correct=True),
      opt("b", "Pick the holding period with the best Sharpe ratio over 1990 to 2024.", correct=True),
      opt("c", "Use book equity for fiscal years ending December 2009.", correct=True),
      opt("d", "Choose pairs by their distance over 2009 only.", "You flagged a formation window. All of 2009 was known by January 2010."),
      opt("e", "Use book equity from fiscal years ending in 2008.", "You flagged old accounts. Fiscal 2008 accounts were public by 2010."),
      opt("f", "Report results for 2010 to 2024 from signals set each month on past data.", "You flagged the reporting window. Results may run to 2024 if each signal used only earlier data.")]
C.append(item("r-which-leak", 3, ["rm-extend", "pr-method"], ["look-ahead-plan"], 150, "What January 2010 knew",
    "A replication plan lists six choices for a test that starts trading in January 2010.",
    "Select all that apply: which choices use information that was not available in January 2010?",
    multi(o5),
    fb("Three choices use data not public in January 2010.", "For each choice, find the latest date whose data it needs."),
    "The full-sample volatility, the holding period from 1990 to 2024 and the December 2009 accounts all use the future. "
    "Accounts for a December year end are not public until about March. "
    "The 2009 pairs window, the 2008 accounts and a report to 2024 on past signals are all safe."))

# C6 the order of an out-of-sample test
C.append(item("r-pairs-oos-order", 3, ["pr-extend"], ["held-out-test"], 150, "A test on later years",
    "Gatev, Goetzmann and Rouwenhorst (2006) report pairs returns to 2002. You plan to test their method on 2003 to 2024.",
    "Put the steps in order. Leave out the two that do not belong.",
    {"kind": "order",
     "lines": [line("p1", "Write down the paper's rules: 12 months of formation, 6 of trading, open at 2 sd."),
               line("p2", "Reproduce the paper's main table on its own years."),
               line("p3", "Freeze the code and the rules in a tagged commit."),
               line("p4", "Run the frozen code once on 2003 to 2024."),
               line("p5", "Report what share of the paper's return survived."),
               line("x1", "Tune the opening threshold on 2003 to 2024 until it matches the paper.",
                    "You tuned on the held-out years. Then they no longer test anything."),
               line("x2", "Drop the years in which the method lost money.",
                    "You removed the bad years. That hides what the test should show.")],
     "answer": ["p1", "p2", "p3", "p4", "p5"], "distractors": ["x1", "x2"]},
    fb("Fix, match, freeze, run once, report.", "The held-out years may be used only once, after the code is frozen.",
       {"x1": "You tuned on the held-out years. Then they no longer test anything.",
        "x2": "You removed the bad years. That hides what the test should show.",
        "left-out": "You left out a step that belongs. Rules, match, freeze, run and report are all needed."}),
    "Fix the rules first and prove the code by matching the paper. Freeze it, then spend the held-out years once. "
    "Tuning on them, or dropping years, turns the test back into a fit."))

# C7 the cost that wipes out a momentum book
g7, t7 = 0.011, 1.4
c7 = g7 / t7
C.append(item("r-turnover-cost", 3, ["rm-portfolios"], ["break-even-cost"], 150, "What costs leave",
    "A momentum book earns 1.1% a month before costs, per £1 long and £1 short. Each month it buys and sells shares worth £1.40 in all.",
    "What cost per £1 traded wipes out the return? Give it in % to 2 decimal places.",
    num(r(c7, 8), 0.00005, [("twice", r(g7 / (2 * t7), 8), 0.00005), ("no-turnover", g7, 0.00002)], unit="%",
        accept=f"0.79%: 1.1% / 1.4 ≈ {c7 * 100:.2f}%"),
    fb("Costs fall on the £1.40 traded each month.", "Set the monthly cost, £1.40 times the rate, equal to the 1.1% earned.",
       {"twice": "You charged each trade twice. The £1.40 already counts buys and sells.",
        "no-turnover": "You charged costs on the position, not on what is traded. Only the £1.40 traded pays."}),
    f"Costs are charged on what is traded: $1.4c$ a month. They wipe out the 1.1% when $1.4c = 1.1\\%$. "
    f"So $c = 1.1\\% / 1.4 \\approx {c7 * 100:.2f}\\%$ per £1 traded."))

# C8 a factor against the bar of 3
m8, s8, n8 = 0.45, 3.1, 360
t8 = m8 / (s8 / math.sqrt(n8))
o8 = [opt("a", "It clears 2 but not 3, so call it unproven.", correct=True),
      opt("b", "It clears 2, so it is a real factor.", "You used the single-test bar of 2. After hundreds of factors were tried, 3 is safer."),
      opt("c", "It fails 3, so the factor has no effect.", "You read a miss as proof of zero. A $t$ of 2.75 is weak evidence, not none."),
      opt("d", "Annualise first, since $t$ grows with the horizon.", "You changed units. A $t$ statistic is the same in monthly or annual terms.")]
C.append(parts("r-t-bar", 3, ["rm-stats"], ["factor-t-bar"], 150, "A bar of three",
    "A new factor earns 0.45% a month, with sd 3.1%, over 360 months. The months are close to independent.",
    "Two questions on the evidence.",
    [("What is its $t$ statistic? Give 2 decimal places.",
      num(r(t8), 0.005, [("no-root", r(m8 / s8), 0.005), ("years", r(m8 / (s8 / math.sqrt(30))), 0.005)]),
      fb("Mean over its standard error.", "Divide the sd by $\\sqrt{360}$, then divide the mean by that.",
         {"no-root": "You divided by the sd, not the standard error. Divide the sd by $\\sqrt{360}$ first.",
          "years": "You counted years, not months. There are 360 monthly returns."})),
     ("Harvey, Liu and Zhu (2016) say a new factor should clear $t = 3$. What should the note say?",
      choice(o8),
      fb("Promising, not proven.", "Compare the $t$ with both bars.", why_map(o8)))],
    f"The standard error is $3.1 / \\sqrt{{360}} \\approx {s8 / math.sqrt(n8):.3f}$, so $t \\approx {t8:.2f}$. "
    "That clears 2 but not the bar of 3 that Harvey, Liu and Zhu set for new factors. The note should call it promising but unproven."))

# C9 one small share in an equal-weighted decile
caps9, rets9 = [5.0] * 9 + [0.05], [0.01] * 9 + [0.60]
ew9 = sum(rets9) / len(rets9)
vw9 = sum(c * x for c, x in zip(caps9, rets9)) / sum(caps9)
C.append(parts("r-small-share", 3, ["rm-portfolios"], ["weighting-scheme"], 150, "One small share",
    "In one month a loser decile holds ten shares. Nine are worth £5 billion each and return 1%. "
    "The tenth is worth £0.05 billion and returns 60%.",
    "Two figures for the month.",
    [("What is the decile's equal-weighted return? Give it in % to 1 decimal place.",
      num(r(ew9, 8), 0.0005, [("big-only", 0.01, 0.0002), ("value-weighted", r(vw9, 8), 0.0004)], unit="%", accept=f"6.9%: (9 × 1% + 60%) / 10 = {ew9 * 100:.1f}%"),
      fb("Each share counts one tenth.", "Average the ten returns, each with weight one tenth.",
         {"big-only": "You gave the nine large shares alone. The tenth share counts one tenth too.",
          "value-weighted": "You weighted by size. Equal weights give the small share a tenth of the decile."})),
     ("What is its value-weighted return? Give it in % to 2 decimal places.",
      num(r(vw9, 8), 0.00005, [("equal-weighted", r(ew9, 8), 0.00002), ("big-only", 0.01, 0.00002)], unit="%", accept=f"1.07%: 0.48 / 45.05 ≈ {vw9 * 100:.2f}%"),
      fb("Weights by size: £45 billion against £0.05 billion.", "Weight each return by the share's value, then divide by the decile's total value.",
         {"equal-weighted": "You gave each share a tenth. Weight by value instead.",
          "big-only": "You left the small share out. It still adds $0.05 \\times 60\\%$ to the total."}))],
    f"Equal weights give $(9 \\times 1\\% + 60\\%) / 10 = {ew9 * 100:.1f}\\%$. Value weights give $(45 \\times 1\\% + 0.05 \\times 60\\%) / 45.05 \\approx {vw9 * 100:.2f}\\%$. "
    "One tiny share drives the equal-weighted figure, so a replication reports both weightings."))

# C10 the sentence for the note
k10 = 0.21 / 0.84
o10 = [opt("a", "A quarter of the effect survived, too little to tell from zero.", correct=True),
       opt("b", "Three quarters of the effect survived publication.", "You gave the share lost, $1 - 0.25$. The share kept is $0.21 / 0.84$."),
       opt("c", "The effect vanished after publication, so it was never really there.", "You read a weak $t$ as proof. The in-sample match also stands."),
       opt("d", "The effect survived, since 0.21% is still positive.", "You ignored the noise. With $t = 0.7$, 0.21% cannot be told from zero.")]
C.append(item("r-note-sentence", 3, ["rm-extend"], ["survival-note"], 150, "One plain sentence",
    "Your replication of a value strategy matches the paper on its years: 0.84% a month, $t = 3.2$. "
    "On the 15 years since publication it earns 0.21% a month, $t = 0.7$.",
    "Which sentence belongs in the note?",
    choice(o10),
    fb("A quarter kept, and within noise of zero.", "Divide the later mean by the earlier one, then read the later $t$.", why_map(o10)),
    f"The kept share is $0.21 / 0.84 = {k10:.0%}$. With $t = 0.7$ the later mean is within noise of zero. ".replace('%', '\\%')
    + "A plain note says both, without calling the effect gone or intact."))

# C12 a pairs strategy against a reversal factor
r12, b12, f12 = 0.0090, 0.35, 0.0140
c12 = r12 - b12 * f12
C.append(item("r-factor-alpha", 3, ["pr-extend"], ["factor-alpha"], 150, "Is it just reversal?",
    "A pairs strategy earns 0.90% a month. Regressed on a short-term reversal factor, its beta is 0.35. "
    "The factor earns 1.40% a month over the same years.",
    "What is the pairs strategy's alpha, in % a month? Give 2 decimal places.",
    num(r(c12, 8), 0.00005, [("whole-factor", r(r12 - f12, 8), 0.00002), ("scaled-own", r(r12 * (1 - b12), 8), 0.00006)], unit="%",
        accept=f"0.41%: 0.90% − 0.35 × 1.40% = {c12 * 100:.2f}%"),
    fb("Subtract beta times the factor's return.", "Find how much of the 0.90% the factor explains, then take it away.",
       {"whole-factor": "You subtracted the whole factor return. Only the beta share, $0.35 \\times 1.40\\%$, is explained.",
        "scaled-own": "You scaled the strategy's own return by the beta. Alpha subtracts beta times the factor's return."}),
    f"The factor explains $0.35 \\times 1.40\\% = {b12 * f12 * 100:.2f}\\%$ a month. What is left is the alpha, $0.90\\% - 0.49\\% = {c12 * 100:.2f}\\%$. "
    "So a little over half the return is reversal exposure."))

# C11 the best of twenty variants with no edge
k11, yrs11 = 20, 5
p11 = 1 - N.cdf(1 / (1 / math.sqrt(yrs11)))
c11 = 1 - (1 - p11) ** k11
C.append(item("r-best-of-twenty", 4, ["rm-stats"], ["best-of-many"], 210, "The best of twenty",
    "You try 20 independent variants of a rule on 5 years of data. None has any edge. "
    "Each variant's annual Sharpe ratio estimate is then normal, with mean 0 and sd $1/\\sqrt{5}$.",
    "What is the chance that the best of the 20 shows a Sharpe ratio above 1? Give 2 decimal places.",
    num(r(c11), 0.005, [("one-variant", r(p11), 0.005), ("added-chances", r(k11 * p11), 0.005)]),
    fb("One minus the chance that all 20 stay below 1.", "Find the chance one variant beats 1, then the chance that none of the 20 does.",
       {"one-variant": "You gave the chance for one variant. The best of 20 has 20 tries at it.",
        "added-chances": "You added the 20 chances, which counts overlaps twice. Use $1 - (1 - p)^{20}$."}),
    f"One variant beats 1 with chance $1 - \\Phi(\\sqrt5) \\approx {p11:.4f}$. All 20 stay below with $(1 - {p11:.4f})^{{20}} \\approx {(1 - p11) ** k11:.3f}$. "
    f"So the best clears 1 with chance about {c11:.2f}, though no variant has an edge."))

# C16 the false share among factors that pass
null16, real16, mu16 = 200, 100, 3.5
pass_null2, pass_real2 = null16 * (1 - N.cdf(2)), real16 * N.cdf(mu16 - 2)
pass_null3, pass_real3 = null16 * (1 - N.cdf(3)), real16 * N.cdf(mu16 - 3)
c16a = pass_null2 / (pass_null2 + pass_real2)
c16b = pass_null3 / (pass_null3 + pass_real3)
C.append(parts("r-false-share", 4, ["rm-stats"], ["false-discoveries"], 240, "False factors among the passes",
    "Suppose 300 candidate factors are tested. 200 have no effect. The other 100 are real, each with an expected $t$ of 3.5. "
    "Treat each $t$ as normal with sd 1. A factor passes when its $t$ is above the bar.",
    "Two questions on the false share.",
    [("With a bar of $t > 2$, what share of the factors that pass are false? Give 4 decimal places.",
      num(r(c16a), 0.0005, [("over-tested", r(pass_null2 / 300), 0.0002), ("null-rate", r(1 - N.cdf(2)), 0.0002)]),
      fb("4.55 false passes against 93.32 real ones.", "Count the expected null passes and real passes, then take the false share.",
         {"over-tested": "You divided by all 300 tested. Divide by the number that pass.",
          "null-rate": "You gave the chance that one null factor passes. The share also needs the real passes."})),
     ("With a bar of $t > 3$, what is that share? Give 4 decimal places.",
      num(r(c16b), 0.00005, [("null-rate", r(1 - N.cdf(3)), 0.00006), ("over-tested", r(pass_null3 / 300), 0.00002)]),
      fb("0.27 false passes against 69.15 real ones.", "Repeat the count with the bar at 3.",
         {"null-rate": "You gave the chance that one null factor passes. The share also needs the real passes.",
          "over-tested": "You divided by all 300 tested. Divide by the number that pass."}))],
    f"At $t > 2$, $200 \\times {1 - N.cdf(2):.5f} \\approx {pass_null2:.2f}$ null factors pass beside $100 \\times \\Phi(1.5) \\approx {pass_real2:.2f}$ real ones, a false share of {c16a:.4f}. "
    f"At $t > 3$ the nulls fall to {pass_null3:.2f} and the real ones to {pass_real3:.2f}, a share of {c16b:.4f}. "
    "The higher bar costs a quarter of the real factors but almost removes the false ones."))

# C13 a point-in-time join in Python
R13 = [("AAA", "2014-12-31", "2015-03-20", 10.0), ("AAA", "2015-12-31", "2016-03-18", 12.0),
       ("BBB", "2015-03-31", "2015-06-25", 5.0), ("BBB", "2015-03-31", "2015-09-10", 4.5),
       ("CCC", "2015-12-31", "2016-04-30", 7.0)]
D13 = [("DDD", "2015-12-31", "2016-02-01", 3.0), ("DDD", "2014-12-31", "2016-02-10", 2.0)]
SOL13 = ("def as_of(reports, date):\n    best = {}\n    for ticker, period_end, published, value in reports:\n"
         "        if published > date:\n            continue\n        key = (period_end, published)\n"
         "        if ticker not in best or key > best[ticker][0]:\n            best[ticker] = (key, value)\n"
         "    return {t: v for t, (k, v) in best.items()}\n")
ns13 = {}
exec(SOL13, ns13)
as_of = ns13["as_of"]
SET13 = "R = " + repr(R13)
SETD13 = "D = " + repr(D13)
calls13 = [(SET13, "as_of(R, '2015-06-30')", as_of(R13, '2015-06-30')),
           (SET13, "as_of(R, '2015-12-31')", as_of(R13, '2015-12-31')),
           (SET13, "as_of(R, '2016-03-18')", as_of(R13, '2016-03-18')),
           (SET13, "as_of(R, '2014-01-01')", as_of(R13, '2014-01-01')),
           (SET13, "as_of(R, '2016-12-31')", as_of(R13, '2016-12-31')),
           (SET13, "as_of(list(reversed(R)), '2015-12-31')", as_of(list(reversed(R13)), '2015-12-31')),
           (SETD13, "as_of(D, '2016-03-01')", as_of(D13, '2016-03-01'))]
tests13 = [{"setup": s, "call": c, "expect": repr(v), "compare": "equal"} for s, c, v in calls13]
C.append(item("r-as-of-code", 4, ["rm-data"], ["point-in-time-join"], 900, "What the desk could see",
    "A point-in-time join stops a backtest from using accounts before they were public. Each report is a tuple "
    "`(ticker, period_end, published, value)` with ISO date strings such as `'2015-03-20'`. A later report may restate an earlier period.",
    "Write `as_of(reports, date)`, a dict from ticker to the value known on `date`. Use only reports published on or before `date`. "
    "Per ticker, take the latest `period_end`, and for a restated period the latest `published`. Leave out tickers with nothing published yet.",
    {"kind": "code", "language": "python",
     "starter": "def as_of(reports, date):\n    # reports: list of (ticker, period_end, published, value)\n    ...\n",
     "solution": SOL13, "examples": [{"setup": tests13[0]["setup"], "call": tests13[0]["call"], "expect": tests13[0]["expect"]}],
     "tests": tests13,
     "how": "Check runs 7 hidden tests. Each compares your dict with the expected one exactly."},
    fb("Filter on the publication date, then keep the latest period per ticker.", "Some tests failed. Open the first one that failed below the editor.",
       {"error": "Your code stopped with an error. Read the first line of the message under the editor.",
        "test-1": "Test 1 asks for 30 June 2015. AAA's 2015 accounts and CCC's came out in 2016, so leave them out.",
        "test-2": "Test 2 asks for 31 December 2015. BBB's restatement, published in September, replaces its June figure.",
        "test-3": "Test 3 is the day AAA's 2015 accounts come out. On or before `date` includes that day.",
        "test-6": "Test 6 gives the reports in reverse order. Compare the dates; do not rely on the list order.",
        "test-7": "Test 7 restates an old period after a newer one is out. The latest `period_end` still wins."}),
    "Filter on `published <= date` first: that is the look-ahead guard. Then keep, per ticker, the largest `(period_end, published)` pair. "
    "ISO date strings sort in date order, so plain string comparison works."))

# C15 how strong an out-of-sample test is
t15, n15, keep15, m15 = 4.0, 240, 0.5, 120
c15a = t15 * keep15 * math.sqrt(m15 / n15)
c15b = 1 - N.cdf(2 - c15a)
c15c = n15 * (2 / (t15 * keep15)) ** 2
C.append(parts("r-oos-power", 5, ["rm-extend"], ["out-of-sample-power"], 360, "A fair test after publication",
    "A paper reports $t = 4.0$ for a strategy over 240 months. Suppose half its mean return survives publication, with the same volatility. "
    "You will test it on the 120 months since.",
    "Three questions on the test.",
    [("What $t$ statistic do you expect out of sample? Give 2 decimal places.",
      num(r(c15a), 0.005, [("halved-only", 2.0, 0.002), ("full-mean", r(t15 * math.sqrt(m15 / n15)), 0.002)]),
      fb("Half the mean, and a standard error $\\sqrt2$ times larger.", "$t$ scales with the mean and with the square root of the months.",
         {"halved-only": "You halved the mean but kept 240 months. With 120 months the standard error is $\\sqrt2$ times larger.",
          "full-mean": "You shortened the sample but kept the full mean. Only half the mean survives."})),
     ("Treat the out-of-sample $t$ as normal with that mean and sd 1. What is the chance that it exceeds 2? Give 2 decimal places.",
      num(r(c15b), 0.005, [("nothing-survived", r(1 - N.cdf(2)), 0.005), ("below-two", r(N.cdf(2 - c15a)), 0.002)]),
      fb("$1 - \\Phi(2 - 1.41)$.", "Standardise 2 against the expected $t$ from the first part.",
         {"nothing-survived": "You used a mean of 0, as if nothing survived. Centre on 1.41.",
          "below-two": "You gave the chance that $t$ falls below 2. The question asks for above."})),
     ("How many months would give an expected out-of-sample $t$ of 2?",
      num(r(c15c), 0, [("same-t", r(n15 * (t15 / (t15 * keep15)) ** 2), 0), ("doubled", 2 * n15, 0)]),
      fb("Solve $2\\sqrt{n/240} = 2$.", "With half the mean, the expected $t$ is $2\\sqrt{n/240}$.",
         {"same-t": "You aimed for the paper's $t$ of 4. A $t$ of 2 needs a quarter of those months.",
          "doubled": "You doubled the months for half the mean. $t$ grows with $\\sqrt n$, so check the square."}))],
    f"Halving the mean halves $t$, and half the months divides it by $\\sqrt2$: $4 \\times 0.5 / \\sqrt2 \\approx {c15a:.2f}$. "
    f"So $t$ tops 2 only about {c15b:.0%} of the time, though half the effect is real. ".replace('%', '\\%')
    + f"An expected $t$ of 2 needs {c15c:.0f} months."))

# ======================================================================== the exam document
CHECKS = [
    ("zhou-probability", "80% of the probability chapter in Zhou solved cold",
     "Zhou's A Practical Guide to Quantitative Finance Interviews, the probability chapter. Work every problem without the solutions, "
     "under a clock, then mark yourself. Count a problem only if your first answer was right."),
    ("zetamac-50", "A Zetamac score of 50 or more",
     "Default Zetamac settings, 120 seconds, typed answers. Use your best score from the last week, on Zetamac or the Today warm-up, which uses the same settings. Paper B is the same pace with options to pick."),
    ("mock-interviews", "Ten mock interviews done aloud, at least three with a stranger",
     "Each one is a full interview, spoken aloud with someone marking your reasoning. For a research role, one is an open case worked aloud "
     "in 45 minutes. For a developer role, one is a feed handler design you defend aloud."),
    ("replication-github", "One replication on GitHub, with an out-of-sample extension and a note on what survived",
     "Reproduce the main table of one classic paper, then run the frozen code on the years since publication. "
     "The repository holds the code, the data steps and a plain note on how much of the effect survived."),
]


def minutes(items, factor, extra=0):
    return int(math.ceil(factor * (sum(it["pace"] for it in items) + extra) / 60 / 5) * 5)


DRAW_A = [{"from": "bank/probability", "tags": ["waiting-for-hh", "betting-on-sequences", "ruin-in-interviews"], "difficulty": [3, 5], "n": 1},
          {"from": "bank/probability", "tags": ["when-to-stop", "who-wins", "duels"], "difficulty": [3, 5], "n": 1},
          {"from": "bank/probability", "tags": ["broken-stick", "semicircle", "random-chords", "meeting"], "difficulty": [3, 5], "n": 1},
          {"from": "bank/probability", "tags": ["exceeding-one", "expected-distance", "largest-of-several", "buffon"], "difficulty": [3, 5], "n": 1},
          {"from": "bank/probability", "tags": ["kelly", "when-to-hedge", "doubling-up"], "difficulty": [3, 5], "n": 1},
          {"from": "bank/probability", "tags": ["fair-from-biased", "cards-and-colours"], "difficulty": [3, 5], "n": 1},
          {"from": "bank/brainteasers", "difficulty": [3, 4], "n": 1},
          {"from": "bank/market-making", "difficulty": [3, 4], "n": 1}]
DRAW_D = [{"from": "drills/oa", "difficulty": 3, "n": 1},
          {"from": "drills/ci", "tags": ["pair-gaps", "digit-sum-pairs", "split-points"], "difficulty": 3, "n": 1}]
ARITH = {"generator": "arith", "n": 80, "options": 4, "difficulty": 3, "skills": ["mp-speed"]}
doc = {
    "id": "stage-3", "stage": 3, "name": "Stage 3 exit test",
    "description": "The exit test for Advanced, in four papers and four checks. "
                   "The papers cover probability, games and markets at interview pace, mental arithmetic, research papers and two coding problems. "
                   "The checks cover Zhou's probability chapter, Zetamac, your mock interviews and your replication. "
                   "Topics 3.2 and 3.4 are optional, so they sit in their own topic exams instead.",
    "parts": [
        {"kind": "paper", "id": "probability", "name": "Paper A: probability, games and markets at interview pace",
         "minutes": minutes(A, 1.0, 6 * 180 + 180 + 120), "pass": 0.8, "items": A, "draw": DRAW_A},
        {"kind": "paper", "id": "arithmetic", "name": "Paper B: mental arithmetic at Zetamac pace",
         "minutes": 2, "scoring": {"right": 1, "wrong": -1, "blank": 0}, "passNet": 50, "navigation": "forward", "skip": False,
         "items": [ARITH]},
        {"kind": "paper", "id": "research", "name": "Paper C: research papers and their traps",
         "minutes": minutes(C, 1.25), "pass": 0.7, "items": C},
        {"kind": "paper", "id": "coding", "name": "Paper D: two medium coding problems in an hour",
         "minutes": 60, "pass": 1, "items": [], "draw": DRAW_D},
    ] + [{"kind": "check", "id": i, "name": n, "detail": dt} for i, n, dt in CHECKS],
}

if __name__ == '__main__':
    with open(OUT, 'w', encoding='utf8') as f:
        json.dump(doc, f, ensure_ascii=False, indent=1)
        f.write('\n')
    for p in doc["parts"]:
        if p["kind"] == "paper":
            ds = [it.get("difficulty") for it in p["items"] if "generator" not in it]
            print(p["id"], len(p["items"]), "entries +", sum(d_["n"] for d_ in p.get("draw", [])), "drawn,",
                  p["minutes"], "min, ramp", [ds.count(k) for k in (2, 3, 4, 5)])
    print("wrote", os.path.relpath(OUT))
