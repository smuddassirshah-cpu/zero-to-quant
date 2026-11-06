"""Build app/content/exams/topic-3.1.json (topic 3.1, Research papers: momentum-rep and pairs-rep).

Route A for every key: the closed forms below. check_numbers.py recomputes each value by a second route and
asserts it at its path in the written file. Run from anywhere: python3 docs/briefs/exam-3.1-scripts/build.py
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-3.1.json')


def r(x, n=7):
    return round(x, n)


def fb(correct, generic, by_key=None):
    d = {"correct": correct, "generic": generic}
    if by_key:
        d["byKey"] = by_key
    return d


def num(answer, tol, wrong=(), unit=None, placeholder="a number", label="Answer", accept=None):
    w = {"kind": "numeric", "answer": answer, "tol": {"abs": tol}, "placeholder": placeholder, "label": label}
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
    return {"id": id, "difficulty": d, "skills": skills, "tags": tags, "pace": pace, "title": title,
            "prose": prose, "question": question, "widget": widget, "feedback": feedback,
            "explain": {"text": explain}}


def parts(id, d, skills, tags, pace, title, prose, question, ps, explain):
    return {"id": id, "difficulty": d, "skills": skills, "tags": tags, "pace": pace, "title": title,
            "prose": prose, "question": question,
            "parts": [{"question": q, "widget": w, "feedback": f} for q, w, f in ps],
            "explain": {"text": explain}}


items = []

# ---------------------------------------------------------------- difficulty 2
# M1 momentum-rep L1 (l3): the abstract's 12.01% a year back to a month
m1 = 1.1201 ** (1 / 12) - 1
items.append(item(
    "e-monthly-from-annual", 2, ["rm-paper"], ["compounding"], 60, "From a year back to a month",
    "Jegadeesh and Titman's abstract states a compounded excess return of 12.01% a year for the 6/6 strategy.",
    "What monthly return compounds to 12.01% a year? Give it in % to 2 decimal places.",
    num(r(m1), 0.00005, [("simple", r(0.1201 / 12), 0.00005)], unit="%", label="Monthly return",
        accept="1.1201^(1/12) - 1 = 0.95%"),
    fb("$(1.1201)^{1/12} - 1 = 0.95\\%$ a month, the paper's 6/6 figure.",
       "Take the twelfth root of 1.1201, then subtract 1.",
       {"simple": "You divided 12.01% by 12. Compounding needs the twelfth root, which gives a little less."}),
    "Monthly returns compound, so $(1 + r)^{12} = 1.1201$. The twelfth root gives $r = 0.95\\%$, the paper's 6/6 cell. "
    "Dividing by 12 gives 1.00%, too high because it ignores the growth on earlier gains."))

# P1 pairs-rep L1 (l3): number of pairs ranked
items.append(item(
    "e-pair-count", 2, ["pr-method"], ["pair-count"], 45, "How many pairs to rank",
    "A replication on another market has 140 shares that trade every day of the formation year.",
    "How many pairs does the distance method rank?",
    num(140 * 139 // 2, 0, [("ordered", 140 * 139, 0), ("square", 140 ** 2, 0)], placeholder="a whole number",
        label="Pairs"),
    fb("$140 \\times 139 / 2 = 9{,}730$ pairs.",
       "Each share pairs with every other share once.",
       {"ordered": "You counted (i, j) and (j, i) separately. Each pair counts once, so halve 19,460.",
        "square": "You took $140^2$. That pairs each share with itself and counts every pair twice."}),
    "Each share pairs with 139 others, and each pair is met from both ends. So the count is $140 \\times 139 / 2 = 9{,}730$."))

# M2 momentum-rep L1 (l1, l4): a testable target
items.append(item(
    "e-testable-claim", 2, ["rm-paper", "rm-data"], ["testable-claim"], 60, "A target you can test",
    "A testable claim names a universe, a period, a signal, a holding rule and a number.",
    "Which sentence is a target you could replicate?",
    choice([
        opt("full", "NYSE and AMEX, 1965 to 1989: 6-month winners minus losers, held 6 months, earn about 0.95% a month.", correct=True),
        opt("no-sample", "Past winners beat past losers by about 0.95% a month, which the paper finds significant in its main table.",
            "It gives a number but no universe and no period, so any later sample could claim to match it."),
        opt("no-number", "NYSE and AMEX shares, 1965 to 1989: past winners beat past losers over the next 6 months.",
            "It names the sample but gives no number, so any positive spread would pass."),
        opt("slogan", "Momentum works in US shares: past winners keep beating past losers, as the paper shows.",
            "It names no period, no holding rule and no number. Nothing could fail it.")]),
    fb("It names the universe, the period, the signal, the holding rule and the number.",
       "Check each sentence for all five parts."),
    "A target must fix every choice that could change the number. Without the universe or the period, any later sample could claim a match. "
    "Without the number, any positive spread would pass."))

# P10 pairs-rep L3 (l11, l15): survival share
items.append(item(
    "e-survival-share", 2, ["pr-extend"], ["survival-share"], 45, "How much survived",
    "A pairs replication earns 1.15% a month on committed capital before its pairs break, and 0.46% after.",
    "What share of the return survived? Give it in % to 1 decimal place.",
    num(r(0.46 / 1.15), 0.0005, [("lost", r(1 - 0.46 / 1.15), 0.0005), ("points", r(0.0115 - 0.0046), 0.00005)],
        unit="%", label="Share that survived", accept="0.46 / 1.15 = 40.0%"),
    fb("$0.46 / 1.15 = 40.0\\%$ survived.",
       "Divide the after figure by the before figure.",
       {"lost": "That is the share lost. The share that survived is after over before.",
        "points": "That is the fall in points a month. The question asks for a share of the before figure."}),
    "Survival is the after figure over the before figure: $0.46 / 1.15 = 40.0\\%$. "
    "The fall of 0.69 points a month is the part lost, not the share kept."))

# M11 momentum-rep L3 (l11): naive t on overlapping sums
items.append(item(
    "e-root-k", 2, ["rm-stats"], ["overlap-t"], 60, "A t statistic on overlapping returns",
    "A note reports overlapping 9-month returns, one a month, with a naive t of 6.30. The monthly returns are close to independent, and the sample is long.",
    "Roughly what t do the data support once the overlap is allowed for? Give 2 decimal places.",
    num(r(6.30 / 3), 0.05, [("by-k", r(6.30 / 9), 0.05), ("times", r(6.30 * 3), 0.05)], label="t statistic",
        accept="6.30 / 3 = 2.10"),
    fb("About $6.30 / \\sqrt 9 = 2.10$.",
       "Overlap makes the naive t too large. By how much?",
       {"by-k": "You divided by K. The variance of the mean is about K times too small, so the t is too large by $\\sqrt K$.",
        "times": "You multiplied. Overlap makes the naive t too large, not too small."}),
    "Overlapping K-month sums share months, so the variance of their mean is about K times the naive one. "
    "The naive t is then too large by about $\\sqrt K = 3$, and $6.30 / 3 = 2.10$."))

# M14 momentum-rep L3 (l14): crash mechanism
crash = (0.7 - 1.6) * 0.14
items.append(item(
    "e-crash-beta", 2, ["rm-extend"], ["crash-beta"], 60, "A rebound after a bear market",
    "After a two-year bear market, the winner leg of a momentum book has market beta 0.7. The loser leg, full of beaten-down shares, has beta 1.6. The market then rises 14% in a month.",
    "Roughly what does the beta term add to the winners-minus-losers return that month, in %?",
    num(r(crash), 0.0005, [("sign", r(-crash), 0.0005), ("sum", r(-(0.7 + 1.6) * 0.14), 0.0005)], unit="%",
        label="Beta term", accept="(0.7 - 1.6) × 14% = -12.6%"),
    fb("$(0.7 - 1.6) \\times 14\\% = -12.6\\%$.",
       "The book is long the winners and short the losers. Find its beta first.",
       {"sign": "You took the betas the wrong way round. The book is long W and short L, so the term is $(\\beta_W - \\beta_L)\\,m$.",
        "sum": "You added the two betas. The short leg's beta enters with a minus sign."}),
    "Long the winners and short the losers, the book's beta is $0.7 - 1.6 = -0.9$. A 14% rally then costs about $0.9 \\times 14\\% = 12.6\\%$. "
    "That is the crash mechanism: after a fall the losers rebound hardest."))

# ---------------------------------------------------------------- difficulty 3
# M3 momentum-rep L1 (l4): sixteen cells under the 2 se rule
p16 = 1 - (1 - 0.0455) ** 16
items.append(item(
    "e-sixteen-cells", 3, ["rm-paper", "rm-stats"], ["many-cells"], 90, "Sixteen cells, one rule",
    "You plan to reproduce all 16 cells of the J × K table. A cell fails when it lies more than 2 standard errors from the paper's. A correct cell then fails with chance 0.0455. Suppose your code is exactly right and the cells' errors are independent.",
    "What is the chance that at least one cell fails? Give 2 decimal places.",
    num(r(p16, 5), 0.005, [("added", r(16 * 0.0455, 4), 0.005), ("one", 0.0455, 0.005)], placeholder="a decimal", label="Probability",
        accept="1 - 0.9545^16 = 0.53"),
    fb("$1 - 0.9545^{16} = 0.53$.",
       "Find the chance that all 16 pass, then take it from 1.",
       {"added": "You added 16 chances of 0.0455. Chances of overlapping events do not add; use $1 - 0.9545^{16}$.",
        "one": "That is the chance for one cell. With 16 cells a miss somewhere is much more likely."}),
    "Each correct cell passes with chance 0.9545, so all 16 pass with chance $0.9545^{16} = 0.47$. "
    "At least one fails with chance $1 - 0.47 = 0.53$. So fix the targets and the rule in the plan, and expect a miss or two."))

# P2 pairs-rep L1 (l2, l3): SSD and sd by hand
A = [1, 1.04, 1.02, 1.07, 1.05]
B = [1, 1.01, 1.04, 1.03, 1.06]
sp = [a - b for a, b in zip(A, B)]
ssd = sum(x * x for x in sp)
mu = sum(sp) / 5
sd0 = math.sqrt(sum((x - mu) ** 2 for x in sp) / 5)
sd1 = math.sqrt(sum((x - mu) ** 2 for x in sp) / 4)
rms = math.sqrt(ssd / 5)
items.append(parts(
    "e-ssd-sd", 3, ["pr-method"], ["ssd-by-hand"], 150, "Distance and spread by hand",
    "Two normalised paths over five formation days. A is 1, 1.04, 1.02, 1.07, 1.05. B is 1, 1.01, 1.04, 1.03, 1.06.",
    "Two questions on the spread $A - B$.",
    [("What is the pair's distance, the sum of squared differences? Give 4 decimal places.",
      num(r(ssd), 0.00005, [("sum-then-square", r(sum(sp) ** 2), 0.00002), ("mean", r(ssd / 5), 0.00002)],
          placeholder="a decimal", label="SSD", accept="0.0030"),
      fb("$0.03^2 + 0.02^2 + 0.04^2 + 0.01^2 = 0.0030$.",
         "Square each day's gap, then add.",
         {"sum-then-square": "You added the gaps and then squared: $0.04^2 = 0.0016$. Square each gap first.",
          "mean": "You took the mean of the squares. Distance is their sum."})),
     ("What is the spread's standard deviation, dividing by n as `np.std` does? Give 4 decimal places.",
      num(r(sd0), 0.00006, [("ddof-one", r(sd1), 0.00006), ("no-mean", r(rms), 0.00006)],
          placeholder="a decimal", label="Standard deviation", accept="0.0232"),
      fb("The mean gap is 0.008, so the sd is $\\sqrt{0.0006 - 0.008^2} = 0.0232$.",
         "Take off the mean gap before squaring, and divide by 5.",
         {"ddof-one": "You divided by $n - 1 = 4$. `np.std` divides by n.",
          "no-mean": "You left the mean gap of 0.008 in. Take it off before squaring."}))],
    "The spread is 0, 0.03, $-0.02$, 0.04 and $-0.01$, so the distance is $0.0009 + 0.0004 + 0.0016 + 0.0001 = 0.0030$. "
    "Its mean is 0.008, so the variance is $0.0006 - 0.008^2 = 0.000536$. The sd is 0.0232, and the trigger is twice that."))

# M4 momentum-rep L1 (l4): lowest matching mean
se4 = 0.0630 / math.sqrt(300)
low = 0.0095 - 2 * se4
items.append(item(
    "e-lowest-match", 3, ["rm-paper", "rm-stats"], ["tolerance-rule"], 120, "The edge of the match",
    "Your plan says a cell matches when it lies within 2 standard errors of the paper's. The paper reports about 0.95% a month for 6/6. Your 6/6 series has sd 6.30% over 300 months.",
    "What is the lowest monthly mean that still counts as a match? Give it in % to 2 decimal places.",
    num(r(low), 0.00005, [("one-se", r(0.0095 - se4), 0.00005), ("over-n", r(0.0095 - 2 * 0.0630 / 300), 0.00005)],
        unit="%", label="Lowest matching mean", accept="0.95% - 2 × 6.30% / √300 = 0.22%"),
    fb("$0.95\\% - 2 \\times 6.30\\% / \\sqrt{300} = 0.22\\%$.",
       "Find the standard error $s/\\sqrt n$, then go 2 of them below 0.95%.",
       {"one-se": "You went 1 standard error below. The rule allows 2.",
        "over-n": "You divided the sd by n. The standard error divides by $\\sqrt n$."}),
    "The standard error is $6.30\\% / \\sqrt{300} = 0.364\\%$. Two of them is 0.73%, so any mean from 0.22% to 1.68% matches. "
    "That band is wide, which is why the rule is fixed before the table is seen."))

# P4 pairs-rep L1 (l4, l8): committed and employed
items.append(parts(
    "e-capital-split", 3, ["pr-returns"], ["committed-employed"], 120, "Two capital figures",
    "A cycle nominates 20 pairs and 16 of them open. Their round trips pay £0.88 in all over the six-month trading period.",
    "Two figures for the cycle.",
    [("What is the monthly committed return, by our convention of the six-month figure over 6? Give it in % to 2 decimal places.",
      num(r(0.88 / 20 / 6), 0.00005, [("employed", r(0.88 / 16 / 6), 0.00005), ("cycle", r(0.88 / 20), 0.00005)],
          unit="%", label="Monthly committed return", accept="0.88 / 20 / 6 = 0.73%"),
      fb("$0.88 / 20 = 4.4\\%$ a cycle, and $4.4\\% / 6 = 0.73\\%$ a month.",
         "Committed capital divides by every nominated pair.",
         {"employed": "You divided by the 16 pairs that opened. Committed capital counts all 20.",
          "cycle": "That is the six-month figure. Divide by 6 for the monthly one."})),
     ("What is the employed return over the whole cycle? Give it in % to 1 decimal place.",
      num(r(0.88 / 16), 0.0005, [("committed", r(0.88 / 20), 0.0005), ("legs", r(0.88 / 32), 0.0005)],
          unit="%", label="Employed return", accept="0.88 / 16 = 5.5%"),
      fb("$0.88 / 16 = 5.5\\%$.",
         "Employed capital divides by the pairs that opened.",
         {"committed": "You divided by all 20 nominated pairs. Employed capital counts only the 16 that opened.",
          "legs": "You divided by 32 legs. Returns are per pair, £1 a side."}))],
    "Committed capital counts every nominated pair: $0.88 / 20 = 4.4\\%$ a cycle, or 0.73% a month. "
    "Employed counts only the 16 that opened: $0.88 / 16 = 5.5\\%$. The ratio $5.5 / 4.4 = 1.25 = 20 / 16$ is a free check."))

# M5 momentum-rep L1 (l5): which log lines show a bug
items.append(item(
    "e-plan-checks", 3, ["rm-stats", "rm-paper"], ["replication-checks"], 120, "Reading a replication log",
    "A replication log prints one line per check. The plan says every cohort's weights sum to 0 and gross to 2. A shuffled panel should give a spread near 0.",
    "Select all that apply: which lines show a bug?",
    choice([
        opt("pass-weights", "Cohort 140: the weights sum to 0.0000 and gross to 2.0000.",
            "This passes. The cohort is £1 long and £1 short, at zero cost."),
        opt("long-heavy", "Cohort 141: weights sum to 0.0200 and gross to 2.0200.", correct=True),
        opt("pass-shuffle", "Shuffled panel, 6/6: 0.04% a month, t 0.15.",
            "A spread near 0 with a small t is what a shuffled panel should give."),
        opt("lookahead", "Shuffled panel, 6/6: 9.8% a month, t 31.", correct=True),
        opt("pass-planted", "Planted panel, 6/6: 1.02% a month, t 2.9.",
            "That is close to the planted size, so this check passes."),
        opt("half-book", "Cohort 150: weights sum to 0.0000 and gross to 1.0000.", correct=True)], kind="multi"),
    fb("Cohort 141, the 9.8% shuffled spread and cohort 150 fail. One leg is too big, the shuffle earns a fortune, and the book is half size.",
       "Compare each line with its rule: sum 0, gross 2, shuffled spread near 0."),
    "A sum of 0.02 with gross 2.02 means the long leg carries an extra weight. A shuffled panel has no momentum, so 9.8% a month points to look-ahead. "
    "A gross of 1 means each leg holds only half its size."))

# P5 pairs-rep L1 (l5): the employed over committed check
items.append(item(
    "e-ratio-check", 3, ["pr-returns", "pr-extend"], ["capital-check"], 75, "A check from algebra",
    "A replication log reports one cycle of the top 20: committed 6.0% and employed 5.0%. The cycle's total payoff is positive.",
    "What should you conclude?",
    choice([
        opt("bug", "There is a bug: with a positive total, employed over committed is k over n, at least 1.", correct=True),
        opt("losers", "Nothing is wrong: pairs that lost money pull employed below committed, as in any bad cycle.",
            "Losses lower both figures alike. Both divide the same total; only the denominators differ."),
        opt("trips", "Nothing is wrong: employed divides by round trips, which can outnumber the pairs.",
            "Employed divides by the pairs that opened, not by round trips."),
        opt("all-open", "There is a bug only if all 20 pairs opened.",
            "If all opened, the two figures would be equal. Employed below committed is impossible with a positive total.")]),
    fb("Employed over committed is $20 / n \\ge 1$ for a positive total, so 5.0% against 6.0% is a bug.",
       "Both figures divide the same total. Compare the denominators."),
    "Both figures divide the same total, by $k = 20$ and by the $n \\le 20$ pairs that opened. "
    "So employed over committed is $20 / n \\ge 1$ when the total is positive. A lower employed figure means the code divides by something else."))

# M6 momentum-rep L2 (l6): survivorship in the loser leg
true_l = (45 * 0.012 + 5 * -0.40) / 50
items.append(item(
    "e-dead-losers", 3, ["rm-data"], ["survivorship"], 120, "The shares a free source drops",
    "The loser decile of one cohort holds 50 shares. Next month 45 of them return 1.2% on average. The other 5 delist with a final return of $-40\\%$ each. All the winners survive.",
    "A free source drops the delisted shares and their final returns. By how many points does that understate the winners-minus-losers spread that month? Give 2 decimal places.",
    num(r(0.012 - true_l), 0.00005, [("over-45", r(0.012 - (45 * 0.012 + 5 * -0.40) / 45), 0.00005),
                                     ("dead-only", 0.04, 0.00005)],
        unit="%", label="Understatement in points", accept="1.2% - (-2.92%) = 4.12%"),
    fb("The true loser mean is $-2.92\\%$ against 1.2%, so the spread is understated by 4.12 points.",
       "Find the loser mean with the 5 dead shares, then compare it with 1.2%.",
       {"over-45": "You divided the full total by 45. All 50 shares were in the decile, so divide by 50.",
        "dead-only": "You took $5 \\times 40\\% / 50 = 4\\%$ and forgot the survivors' 1.2% that replaces it."}),
    "With the dead shares the loser mean is $(45 \\times 1.2\\% + 5 \\times (-40\\%)) / 50 = -2.92\\%$. "
    "Without them it is 1.2%, so the loser leg looks 4.12 points better. The book is short the losers, so the spread is understated by 4.12 points."))

# P6 pairs-rep L2 (l6, l7): one trade
pay = 1.010 / 0.960 - 0.998 / 1.011
items.append(parts(
    "e-one-trade", 3, ["pr-trading"], ["round-trip"], 150, "One trade, open to close",
    "A pair's formation spread has sd 0.022. On trading day 12 the normalised prices are $p_i = 1.011$ and $p_j = 0.960$. On day 40 they have crossed: $p_i = 0.998$ and $p_j = 1.010$.",
    "Two questions on this trade.",
    [("What does the desk do on day 12?",
      choice([
          opt("short-dear", "Sell £1 of i and buy £1 of j.", correct=True),
          opt("long-dear", "Buy £1 of i and sell £1 of j.",
              "That is long the dearer leg. Convergence would then lose money."),
          opt("inside", "Nothing: the spread is inside the 2 sd band.",
              "The spread is 0.051 and 2 sd is 0.044, so it is outside the band."),
          opt("units", "Sell £1 of i and buy £1.05 of j, to match the units.",
              "The rule puts £1 on each side. The units differ because the prices differ.")]),
      fb("The spread 0.051 is beyond $2 \\times 0.022 = 0.044$. Sell the dearer i and buy the cheaper j, £1 each.",
         "Compare the spread with 2 sd, then short the dearer leg.")),
     ("What is the round trip's payoff on £1 a side? Give 4 decimal places.",
      num(r(pay), 0.0001, [("wrong-side", r(-pay), 0.0001), ("price-gaps", r((1.010 - 0.960) - (0.998 - 1.011)), 0.0001)],
          placeholder="a decimal", label="Payoff", accept="1.010/0.960 - 0.998/1.011 = 0.0649"),
      fb("$1.010/0.960 - 0.998/1.011 = 0.0649$.",
         "The payoff is the long leg's return minus the short leg's.",
         {"wrong-side": "You have the sign of a trade long the dearer leg. The desk is short i, so the payoff is positive.",
          "price-gaps": "You added price changes. On £1 a side the payoff uses returns: divide by each entry price."}))],
    "The spread $1.011 - 0.960 = 0.051$ exceeds $2 \\times 0.022 = 0.044$, so the desk sells the dearer i and buys j. "
    "The payoff is $1.010/0.960 - 0.998/1.011 = 0.0521 + 0.0129 = 0.0649$. Both legs earn as the prices cross."))

# M8 momentum-rep L2 (l8, l9): month counts
T, J, K, skip = 360, 9, 4, 1
items.append(parts(
    "e-month-counts", 3, ["rm-portfolios"], ["month-count"], 120, "Counting the months",
    "A 9/4 strategy with a one-month skip runs on a panel of 360 months, numbered from 0.",
    "Two counts.",
    [("How many monthly returns does the overlapping composite give?",
      num(T - J - skip - K + 1, 0, [("no-warmup", T - J - skip, 0), ("no-skip", T - J - K + 1, 0)],
          placeholder="a whole number", label="Composite months"),
      fb("$360 - 9 - 1 - 4 + 1 = 347$.",
         "Find the month the first ranking is ready, then wait for K live cohorts.",
         {"no-warmup": "You counted from the first ranking, month 10. The composite needs 4 live cohorts, so it starts 3 months later.",
          "no-skip": "You left out the skip. The ranking window ends a month earlier, so the first cohort starts at month 10."})),
     ("How many returns would the non-overlapping design give, rebalancing the whole book every 4 months?",
      num((T - J - skip) // K, 0, [("all-months", T // K, 0), ("from-composite", (T - J - skip - K + 1) // K, 0)],
          placeholder="a whole number", label="Non-overlapping returns"),
      fb("$\\lfloor 350 / 4 \\rfloor = 87$ blocks.",
         "Blocks of 4 start once the first ranking is ready.",
         {"all-months": "You divided all 360 months by 4. The first 10 months only build the first ranking.",
          "from-composite": "You divided 347 by 4. The blocks start at month 10, not month 13."}))],
    "The first ranking needs $J + \\text{skip} = 10$ months, and the composite is full at month $10 + 4 - 1 = 13$. "
    "That leaves $360 - 9 - 1 - 4 + 1 = 347$ months. Blocks of 4 from month 10 number $\\lfloor 350 / 4 \\rfloor = 87$."))

# P8 pairs-rep L2 (l9): bounce share
items.append(item(
    "e-bounce-share", 3, ["pr-trading", "pr-returns"], ["bounce"], 120, "How much is bounce",
    "Monthly committed returns of a top-20 replication, on closes unless named. Same-day trades earn 1.18%. Same-day trades on mid prices earn 0.95%. With a one-day wait, closes earn 0.85%.",
    "What share of the same-day figure on closes is bid-ask bounce? Give it in % to 1 decimal place.",
    num(r(0.23 / 1.18), 0.0005, [("wait-gap", r(0.33 / 1.18), 0.0005), ("over-mids", r(0.23 / 0.95), 0.0005)],
        unit="%", label="Share that is bounce", accept="(1.18 - 0.95) / 1.18 = 19.5%"),
    fb("$(1.18 - 0.95) / 1.18 = 19.5\\%$.",
       "Mid prices carry no bounce. Compare the two same-day runs.",
       {"wait-gap": "You used the whole fall from waiting, 0.33 points. Part of it is a lost day of convergence, so use the mid-price run.",
        "over-mids": "You divided by the mid figure. The share is of the figure on closes, 1.18%."}),
    "Mid prices carry no bounce, so the bounce is $1.18 - 0.95 = 0.23$ points. That is $0.23 / 1.18 = 19.5\\%$ of the same-day figure. "
    "The wait costs 0.33 points, but 0.10 of that is a day of lost convergence."))

# M10 momentum-rep L2 (l10): gap in standard errors
se10 = 5.90 / math.sqrt(289)
items.append(item(
    "e-gap-in-se", 3, ["rm-stats"], ["gap-in-se"], 90, "A gap in standard errors",
    "Your 6/6 composite has mean 0.68% a month and sd 5.90% over 289 months. The paper reports about 0.95%. Your plan matches within 2 standard errors.",
    "How many standard errors apart are the two means? Give 2 decimal places.",
    num(r(0.27 / se10, 5), 0.005, [("over-sd", r(0.27 / 5.90, 5), 0.0005), ("over-n", r(0.27 / (5.90 / 289), 4), 0.005)],
        placeholder="a decimal", label="Gap in standard errors", accept="0.27 / (5.90 / 17) = 0.78"),
    fb("The standard error is $5.90 / 17 = 0.347$ points, so the gap is $0.27 / 0.347 = 0.78$ of them.",
       "Divide the gap by $s / \\sqrt n$.",
       {"over-sd": "You divided the gap by the sd. The yardstick for a mean is $s/\\sqrt n$.",
        "over-n": "You divided the sd by n. The standard error divides by $\\sqrt n = 17$."}),
    "The standard error is $5.90\\% / \\sqrt{289} = 5.90\\% / 17 = 0.347\\%$. The gap of 0.27 points is $0.27 / 0.347 = 0.78$ of them. "
    "That is inside the rule, and about what a new seed alone moves a cell."))

# P9 pairs-rep L2 (l10): which cell to lead with
items.append(item(
    "e-lead-cell", 3, ["pr-returns", "pr-extend"], ["conservative-cell"], 75, "The cell to lead with",
    "A first full run of the top 20 gives four monthly figures. Same day: 1.12% committed and 1.25% employed. With a one-day wait: 0.79% committed and 0.88% employed.",
    "Which figure should the write-up set beside the paper's headline?",
    choice([
        opt("wait-committed", "0.79%: committed capital with the one-day wait.", correct=True),
        opt("same-employed", "1.25%: employed capital on same-day trades.",
            "It carries the bounce and leaves out the pairs that never opened. It is the most flattering cell."),
        opt("wait-employed", "0.88%: employed capital with the one-day wait.",
            "Employed capital drops the nominated pairs that never traded. Committed capital counts the whole book."),
        opt("same-committed", "1.12%: committed capital on same-day trades, the paper's first rule.",
            "Same-day fills on closes book a bounce no desk could capture. The wait removes it.")]),
    fb("Lead with 0.79%: the whole book, with the bounce removed.",
       "Pick the figure a desk could earn on all the capital it set aside."),
    "Lead with the cell a desk could earn on its whole book: top 20, committed capital, one-day wait. "
    "The others add the bounce or drop the pairs that never opened. Report them beside it, not instead."))

# P11 pairs-rep L3 (l11): pooled convergence share
pooled = (36 + 22 + 15) / (48 + 40 + 32)
mean_sh = (36 / 48 + 22 / 40 + 15 / 32) / 3
items.append(parts(
    "e-convergence-pooled", 3, ["pr-extend"], ["convergence-share"], 150, "How often trades converge",
    "Three cycles after a break. Cycle 1 opens 48 trades and 36 close at a crossing. Cycle 2 opens 40 and 22 do. Cycle 3 opens 32 and 15 do.",
    "Two questions on convergence.",
    [("What is the convergence share, pooled over the trades of all three cycles? Give it in % to 1 decimal place.",
      num(r(pooled), 0.0005, [("mean-of-shares", r(mean_sh), 0.0005)], unit="%", label="Convergence share",
          accept="73 / 120 = 60.8%"),
      fb("$73 / 120 = 60.8\\%$.",
         "Add the converged trades and the opened trades, then divide.",
         {"mean-of-shares": "You averaged the three cycle shares. Pooling weights each trade equally, so divide 73 by 120."})),
     ("Before the break the pooled share was 78%. What does the fall point to?",
      choice([
          opt("broken", "More trades fail to converge, as when pairs stop co-moving.", correct=True),
          opt("crowding", "Crowding: rival desks close the gaps before we can trade them.",
              "Crowding shrinks the gaps and the gain per trade. The trades that do open still converge, so the share holds."),
          opt("bounce", "More bid-ask bounce in the later closing prices.",
              "Bounce moves the booked prices, not whether the spread crosses zero."),
          opt("fewer", "Fewer pairs reach 2 sd, so fewer trades open in each cycle.",
              "That lowers the count of trades, not the share of opened trades that converge.")]),
      fb("A falling convergence share is the mark of pairs that stopped co-moving.",
         "Ask what would make an opened trade fail to cross."))],
    "Pooled, $(36 + 22 + 15) / (48 + 40 + 32) = 73 / 120 = 60.8\\%$. The mean of the three cycle shares, 59.0%, weights a small cycle like a large one. "
    "A falling share means more trades end at the forced close, the mark of broken pairs."))

# P12 pairs-rep L3 (l12): chance passes
npairs = 120 * 119 // 2
items.append(item(
    "e-chance-passes", 3, ["pr-extend", "pr-method"], ["false-positives"], 75, "Passes by chance",
    "A researcher tests every pair of 120 shares for cointegration at the 1% level. Suppose no pair is cointegrated.",
    "How many pairs pass by chance, on average?",
    num(r(npairs * 0.01), 0.05, [("shares", r(120 * 0.01), 0.05), ("ordered", r(120 * 119 * 0.01), 0.05)],
        placeholder="a decimal", label="Expected passes", accept="7,140 × 0.01 = 71.4"),
    fb("$7{,}140 \\times 0.01 = 71.4$.",
       "Count the pairs, then multiply by the level.",
       {"shares": "You multiplied the 120 shares by 0.01. Each pair is a test, so count pairs.",
        "ordered": "You counted ordered pairs, 14,280. Each pair is tested once: 7,140."}),
    "There are $120 \\times 119 / 2 = 7{,}140$ pairs. Each passes by chance with probability 0.01, so 71.4 pass on average. "
    "A shortlist that long can hold no real pair at all."))

# P14 pairs-rep L3 (l14): cycles in sample under a lock
starts = list(range(0, 3024, 21))
in_s = [s for s in starts if s + 378 <= 1764]
items.append(item(
    "e-lock-count", 3, ["pr-extend"], ["held-out-lock"], 120, "Cycles before the lock",
    "Cycles start every 21 trading days from day 0. Each has 252 formation days, then 126 trading days. The held-out data begin on day 1,764 and stay locked.",
    "How many cycles use only days before 1,764?",
    num(len(in_s), 0, [("starts", len([s for s in starts if s < 1764]), 0),
                       ("formation", len([s for s in starts if s + 252 <= 1764]), 0)],
        placeholder="a whole number", label="In-sample cycles"),
    fb("Starts 0 to 1,386 qualify: $1{,}386 / 21 + 1 = 67$.",
       "A cycle from day s uses days s to $s + 377$.",
       {"starts": "You counted cycles that start before day 1,764. Most of the late ones trade on locked days.",
        "formation": "You counted cycles whose formation ends in time. Their trading days still fall after the lock."}),
    "A cycle from day s uses days s to $s + 377$, so it is in sample when $s + 378 \\le 1{,}764$, that is $s \\le 1{,}386$. "
    "The starts 0, 21, ..., 1,386 number $1{,}386 / 21 + 1 = 67$. A cycle that trades after the lock would leak held-out prices."))

# ---------------------------------------------------------------- difficulty 4
# M12 momentum-rep L3 (l11): Newey-West by hand
g0, g1, g2, n12, mean12 = 36.0, -3.0, 1.2, 240, 0.80
V = g0 + 2 * ((1 - 1 / 3) * g1 + (1 - 2 / 3) * g2)
t_nw = mean12 / math.sqrt(V / n12)
t_naive = mean12 / math.sqrt(g0 / n12)
t_unw = mean12 / math.sqrt((g0 + 2 * (g1 + g2)) / n12)
items.append(item(
    "e-nw-hand", 4, ["rm-stats"], ["newey-west"], 180, "Newey-West by hand",
    "A monthly spread has mean 0.80% over 240 months. In squared per cent, its variance is 36.0. Its autocovariances are $-3.0$ at lag 1 and 1.2 at lag 2. Use Newey-West with $L = 2$, weighting lag j by $1 - j/(L + 1)$.",
    "What is the Newey-West t statistic of the mean? Give 2 decimal places.",
    num(r(t_nw, 5), 0.005, [("naive", r(t_naive, 5), 0.002), ("unweighted", r(t_unw, 5), 0.002)],
        placeholder="a decimal", label="t statistic", accept="0.80 / √(32.8 / 240) = 2.16"),
    fb("$\\hat V = 36.0 + 2(\\tfrac23(-3.0) + \\tfrac13(1.2)) = 32.8$, so $t = 0.80 / \\sqrt{32.8/240} = 2.16$.",
       "Build $\\hat V = \\hat\\gamma_0 + 2\\sum_j w_j\\hat\\gamma_j$, then divide the mean by $\\sqrt{\\hat V / n}$.",
       {"naive": "You used the variance alone, lag 0. That is the naive t, 2.07.",
        "unweighted": "You added the autocovariances at full weight. Lag 1 gets $\\tfrac23$ and lag 2 gets $\\tfrac13$."}),
    "$\\hat V = 36.0 + 2(\\tfrac23(-3.0) + \\tfrac13(1.2)) = 36.0 - 3.2 = 32.8$. The standard error is $\\sqrt{32.8 / 240} = 0.370$, so $t = 0.80 / 0.370 = 2.16$. "
    "The negative lag-1 term lowers the variance, so the t rises above the naive 2.07."))

# P3 pairs-rep L1 (l1): what formation may use
items.append(item(
    "e-formation-only", 4, ["pr-method"], ["look-ahead"], 150, "What the desk knows",
    "A cycle forms pairs on days 1,000 to 1,251 and trades them on days 1,252 to 1,377.",
    "Select all that apply: which choices avoid look-ahead?",
    choice([
        opt("sd-form", "Measure each spread's sd over days 1,000 to 1,251.", correct=True),
        opt("normalise", "Normalise both prices to 1 on day 1,000 and carry them into trading.", correct=True),
        opt("rank-all", "Rank pairs by distance over days 1,000 to 1,377.",
            "Days 1,252 to 1,377 are trading days. Ranking on them uses prices the desk has not seen."),
        opt("sd-trade", "Measure the trigger sd over the trading days, while the spread is live.",
            "The trigger is fixed when formation ends. A trading-period sd uses future prices."),
        opt("open-first", "Open on day 1,252 if the spread already exceeds 2 sd.", correct=True),
        opt("pick-threshold", "Pick 1.5 or 2 sd by which paid more over days 1,252 to 1,377.",
            "That chooses the rule from the very profits it then reports.")], kind="multi"),
    fb("The formation sd, the day-1,000 normalisation and an opening on day 1,252 are all known in time.",
       "For each choice, ask which days it reads."),
    "Everything that chooses or measures is fixed by day 1,251: the normalisation, the ranking and the sd. "
    "The opening rule is a level test, so a gap already past 2 sd opens on day 1,252. A ranking, sd or threshold from trading days is look-ahead."))

# M13 momentum-rep L3 (l13, l15): after publication
se_d = math.sqrt(5.8 ** 2 / 288 + 6.6 ** 2 / 168)
t_d = (0.40 - 1.10) / se_d
items.append(parts(
    "e-after-pub", 4, ["rm-extend", "rm-stats"], ["post-publication"], 210, "After publication",
    "On an extension panel, take the 288 months before publication. There the 6/6 skip spread has mean 1.10% a month and sd 5.8%. After it, the mean is 0.40% and the sd 6.6% over 168 months.",
    "Two figures for the note.",
    [("What share of the effect survived? Give it in % to 1 decimal place.",
      num(r(0.40 / 1.10), 0.0005, [("lost", r(1 - 0.40 / 1.10), 0.0005), ("points", 0.007, 0.00005)],
          unit="%", label="Share that survived", accept="0.40 / 1.10 = 36.4%"),
      fb("$0.40 / 1.10 = 36.4\\%$.",
         "Divide the after mean by the before mean.",
         {"lost": "That is the share lost. The share that survived is after over before.",
          "points": "That is the fall in points a month. The question asks for a share."})),
     ("What is the t statistic of the difference, after minus before? Give 2 decimal places.",
      num(r(t_d, 5), 0.005, [("after-only", r(-0.70 / (6.6 / math.sqrt(168)), 5), 0.005),
                             ("no-n", r(-0.70 / math.sqrt(5.8 ** 2 + 6.6 ** 2), 5), 0.002)],
          placeholder="a decimal", label="t statistic", accept="-0.70 / 0.613 = -1.14"),
      fb("$-0.70 / \\sqrt{5.8^2/288 + 6.6^2/168} = -0.70 / 0.613 = -1.14$.",
         "The difference's standard error adds the two squared standard errors.",
         {"after-only": "You used the after period's standard error alone. Both means are estimates, so add both variances.",
          "no-n": "You added the two variances without dividing each by its months."}))],
    "Survival is $0.40 / 1.10 = 36.4\\%$. The difference's standard error is $\\sqrt{5.8^2/288 + 6.6^2/168} = 0.613$ points, so $t = -0.70 / 0.613 = -1.14$. "
    "The fall is large but not significant, so the note gives both."))

# P7 pairs-rep L2 (l9): break-even and net
trades = 4 * 1.8
items.append(parts(
    "e-break-even-net", 4, ["pr-trading", "pr-returns"], ["break-even"], 180, "What costs leave",
    "A pair earns 5.2% gross over a cycle from 1.8 round trips. Each round trip is four trades: an open and a close on both legs.",
    "Two questions on costs.",
    [("What cost per trade leaves the pair at break-even? Give it in % to 2 decimal places.",
      num(r(0.052 / trades), 0.00005, [("per-trip", r(0.052 / 1.8), 0.00005), ("once", r(0.052 / 4), 0.00005)],
          unit="%", label="Break-even cost per trade", accept="5.2% / 7.2 = 0.72%"),
      fb("$5.2\\% / (4 \\times 1.8) = 0.72\\%$ a trade.",
         "Count the trades first: four for each round trip.",
         {"per-trip": "You divided by the round trips. Each round trip is four trades.",
          "once": "You charged the four trades once per pair. The pair makes 1.8 round trips."})),
     ("At 0.25% per trade, what is the pair's net monthly figure, the cycle return over 6? Give it in % to 2 decimal places.",
      num(r((0.052 - trades * 0.0025) / 6), 0.00005, [("once", r((0.052 - 4 * 0.0025) / 6), 0.00005),
                                                      ("per-trip", r((0.052 - 1.8 * 0.0025) / 6), 0.00005)],
          unit="%", label="Net monthly return", accept="(5.2% - 7.2 × 0.25%) / 6 = 0.57%"),
      fb("$(5.2\\% - 7.2 \\times 0.25\\%) / 6 = 0.57\\%$ a month.",
         "Charge 0.25% on every one of the 7.2 trades, then divide by 6.",
         {"once": "You charged four trades in all. With 1.8 round trips there are 7.2.",
          "per-trip": "You charged 0.25% per round trip. It is per trade, four to a trip."}))],
    "The pair makes $4 \\times 1.8 = 7.2$ trades, so break-even is $5.2\\% / 7.2 = 0.72\\%$ a trade. "
    "At 0.25% the costs are $7.2 \\times 0.25\\% = 1.8\\%$, leaving 3.4% a cycle. Over 6 months that is 0.57% a month."))

# P13 pairs-rep L3 (l12): a hedge ratio that is not 1
L_now = 1.05 ** 1.8
items.append(parts(
    "e-hedge-ratio", 4, ["pr-method", "pr-extend"], ["hedge-ratio"], 180, "A hedge that is not 1 to 1",
    "Engle-Granger finds $\\ln L = 1.8 \\ln A + \\varepsilon$ with $\\varepsilon$ stationary. Both normalised prices start at 1. Over a month A rises to 1.05 while $\\varepsilon$ stays put.",
    "Two questions on what the distance method sees.",
    [("What is the normalised spread $L - A$ now? Give 4 decimal places.",
      num(r(L_now - 1.05), 0.0001, [("l-only", r(L_now - 1), 0.0001), ("one-to-one", 0, 0.0001)],
          placeholder="a decimal", label="Spread", accept="1.05^1.8 - 1.05 = 0.0418"),
      fb("$L = 1.05^{1.8} = 1.0918$, so $L - A = 0.0418$.",
         "With $\\varepsilon$ unchanged, $L = A^{1.8}$.",
         {"l-only": "You gave L's own move. The spread is $L - A$.",
          "one-to-one": "You assumed L moves 1 to 1 with A. The estimated slope is 1.8."})),
     ("The 1 to 1 spread had formation sd 0.015. What happens under the distance rule?",
      choice([
          opt("opens", "It opens, though L and A have kept their estimated relation.", correct=True),
          opt("shut", "It stays shut, because 0.0418 is inside 2 sd.",
              "Two sd is 0.030, and 0.0418 is beyond it."),
          opt("converges", "It opens, and the gap will close because $\\varepsilon$ is stationary.",
              "The 1 to 1 spread is not $\\varepsilon$. It drifts with A, so it need not close."),
          opt("long-l", "It opens long L, the dearer leg, and short A.",
              "The rule shorts the dearer leg. L at 1.0918 is the dearer one.")]),
      fb("0.0418 is beyond $2 \\times 0.015 = 0.030$, so distance opens on a gap Engle-Granger calls normal.",
         "Compare the spread with 2 sd, then ask whether the relation broke."))],
    "With $\\varepsilon$ unchanged, $L = 1.05^{1.8} = 1.0918$, so $L - A = 0.0418$, beyond $2 \\times 0.015$. "
    "Distance fixes a 1 to 1 hedge, so the drift in A reads as a divergence. Engle-Granger's residual has not moved at all."))

# Pcode pairs-rep L2 (l8): committed and employed from a list of round trips
items.append({
    "id": "e-capital-code", "difficulty": 4, "skills": ["pr-returns", "pr-trading"], "tags": ["capital-code"], "pace": 360,
    "title": "Capital from a list of trades",
    "prose": "One cycle's round trips arrive as `(pair, payoff)` tuples, one per round trip. A pair that reopens appears more than once. `k` pairs were nominated.",
    "question": "Write `cycle_capital(trades, k)` returning `(committed, employed)` over the cycle. Committed divides the total payoff by `k`. Employed divides it by the number of pairs that opened, and is 0.0 when none did.",
    "widget": {
        "kind": "code", "language": "python",
        "starter": "def cycle_capital(trades, k):\n    \"\"\"(committed, employed) returns of one cycle.\"\"\"\n    total = sum(p for _, p in trades)\n    return total / k, total / len(trades)\n",
        "solution": "def cycle_capital(trades, k):\n    total = sum(p for _, p in trades)\n    opened = len({pair for pair, _ in trades})\n    employed = total / opened if opened else 0.0\n    return total / k, employed\n",
        "prelude": "BOOK = [((2 * i, 2 * i + 1), round(0.01 * ((i * 7) % 5 - 1.5), 4)) for i in range(12)]\nBOOK += [((2 * i, 2 * i + 1), 0.006) for i in range(0, 12, 3)]\n",
        "examples": [
            {"call": "list(cycle_capital([((2, 3), 0.04), ((5, 8), -0.01)], 5))", "expect": "[0.006, 0.015]",
             "compare": "isclose", "tol": {"abs": 1e-12}}],
        "tests": [],
        "how": "Check runs 7 hidden tests. They hold reopened pairs, an empty cycle and a losing cycle. They also hold a flat trade and a book of 16 round trips. Each figure must match to $10^{-12}$."
    },
    "feedback": fb("Employed counts each pair that opened once, however often it reopened, and is 0.0 for an empty cycle.",
                   "Count distinct pairs, not round trips, and guard the empty cycle."),
    "explain": {"text": "Committed divides the total by every nominated pair, k. Employed divides by the distinct pairs in the list, so a reopened pair counts once. "
                        "With no trades both are 0.0, the paper's 0 over 0 rule."}})


def capital(trades, k):
    total = sum(p for _, p in trades)
    opened = len({pair for pair, _ in trades})
    return [total / k, total / opened if opened else 0.0]


BOOK = [((2 * i, 2 * i + 1), round(0.01 * ((i * 7) % 5 - 1.5), 4)) for i in range(12)]
BOOK += [((2 * i, 2 * i + 1), 0.006) for i in range(0, 12, 3)]
cap_cases = [
    ("list(cycle_capital([((2, 3), 0.03), ((2, 3), 0.02), ((4, 9), 0.01)], 4))", [((2, 3), 0.03), ((2, 3), 0.02), ((4, 9), 0.01)], 4),
    ("list(cycle_capital([], 20))", [], 20),
    ("list(cycle_capital([((1, 7), 0.01)] * 4, 1))", [((1, 7), 0.01)] * 4, 1),
    ("list(cycle_capital([((0, 1), -0.05), ((0, 1), 0.01), ((3, 4), 0.02)], 10))", [((0, 1), -0.05), ((0, 1), 0.01), ((3, 4), 0.02)], 10),
    ("list(cycle_capital([((6, 9), 0.0), ((2, 5), 0.03)], 20))", [((6, 9), 0.0), ((2, 5), 0.03)], 20),
    ("list(cycle_capital(BOOK, 20))", BOOK, 20),
]
cap_tests = [{"call": c, "expect": repr([round(x, 12) for x in capital(tr, k)]), "compare": "isclose", "tol": {"abs": 1e-12}}
             for c, tr, k in cap_cases]
cap_tests.append({"call": "len(cycle_capital([((2, 3), 0.01)], 5))", "expect": "2", "compare": "equal"})
items[-1]["widget"]["tests"] = cap_tests

# ---------------------------------------------------------------- difficulty 5
# M9 momentum-rep L2 (l9): what the skip swaps
ev = {1: -0.40, 2: 0.80, 3: 0.75, 4: 0.70, 13: -0.10}
d3 = (ev[4] - ev[1]) / 3 / 100
d12 = (ev[13] - ev[1]) / 12 / 100
items.append(parts(
    "e-skip-event", 5, ["rm-portfolios"], ["skip-month"], 240, "What the skip month swaps",
    "Event month h is the h-th month after a cohort's ranking window ends. In event month 1 a cohort's average spread is $-0.40\\%$. In months 2, 3 and 4 it is 0.80%, 0.75% and 0.70%. In month 13 it is $-0.10\\%$. In steady state a composite's mean is the average of the event months it holds.",
    "Two questions on what a one-month skip changes.",
    [("By how many points a month does the skip change the mean of the K = 3 strategy? Give 2 decimal places, with a sign.",
      num(r(d3), 0.00005, [("no-divide", r(d3 * 3), 0.00005), ("reversed", r(-d3), 0.00005)],
          unit="%", label="Change in points", accept="(0.70 - (-0.40)) / 3 = 0.37%"),
      fb("The hold moves from months 1 to 3 to months 2 to 4: $(0.70 + 0.40) / 3 = +0.37$ points.",
         "List the event months held with and without the skip.",
         {"no-divide": "You took month 4 minus month 1 but did not average. The swap is one month of three.",
          "reversed": "You have the sign backwards. The skip drops month 1, the reversal month, and adds month 4."})),
     ("By how many points a month does the skip change the mean of the K = 12 strategy? Give 3 decimal places, with a sign.",
      num(r(d12, 8), 0.000005, [("no-divide", r(d12 * 12, 8), 0.000005), ("reversed", r(-d12, 8), 0.000005)],
          unit="%", label="Change in points", accept="(-0.10 - (-0.40)) / 12 = 0.025%"),
      fb("The hold moves from months 1 to 12 to months 2 to 13: $(-0.10 + 0.40) / 12 = +0.025$ points.",
         "The skip swaps month 1 for month 13, one month of twelve.",
         {"no-divide": "You took month 13 minus month 1 but did not average. The swap is one month of twelve.",
          "reversed": "You have the sign backwards. Month 13 at $-0.10\\%$ replaces month 1 at $-0.40\\%$."}))],
    "The skip swaps event month 1 for month $K + 1$, so the mean moves by their difference over K. "
    "That is $1.10 / 3 = 0.37$ points for K = 3 and $0.30 / 12 = 0.025$ for K = 12. The swap is a third of a short hold but a twelfth of a long one."))

# Mcode momentum-rep L2 (l8): the JT composite from cohort returns
prelude_c = ("import math\n"
             "C3 = [[0.02, 0.01, -0.01], [0.03, 0.0, 0.02], [-0.01, 0.04, 0.01], [0.0, 0.02, 0.03], [0.05, -0.02, 0.0]]\n"
             "SAME = [[0.01, -0.02, 0.03, 0.005] for _ in range(7)]\n"
             "BIG = [[round(0.05 * math.sin(7 * s + 3 * h), 6) for h in range(6)] for s in range(40)]\n")
ns = {}
exec(prelude_c, ns)


def composite(c, K):
    return [sum(c[s][t - s] for s in range(t - K + 1, t + 1)) / K for t in range(K - 1, len(c))]


comp_cases = [
    ("jt_composite([[0.01, 0.02], [0.03, 0.04], [0.05, 0.06]], 2)", [[0.01, 0.02], [0.03, 0.04], [0.05, 0.06]], 2),
    ("jt_composite(C3, 3)", ns["C3"], 3),
    ("jt_composite(C3, 1)", [[row[0]] for row in ns["C3"]], 1),
    ("jt_composite(SAME, 4)", ns["SAME"], 4),
    ("jt_composite(BIG, 6)", ns["BIG"], 6),
]
comp_tests = []
for call, c, K in comp_cases:
    comp_tests.append({"call": call, "expect": repr([round(x, 12) for x in composite(c, K)]), "compare": "isclose",
                       "tol": {"abs": 1e-12}})
comp_tests[2]["call"] = "jt_composite([[row[0]] for row in C3], 1)"
comp_tests.append({"call": "jt_composite(C3[:2], 3)", "expect": "[]", "compare": "equal"})
comp_tests.append({"call": "jt_composite(C3[:3], 3)", "expect": repr([round(composite(ns['C3'][:3], 3)[0], 12)]),
                   "compare": "isclose", "tol": {"abs": 1e-12}})
comp_tests.append({"call": "len(jt_composite(BIG, 6))", "expect": str(len(composite(ns["BIG"], 6))), "compare": "equal"})
items.append({
    "id": "e-composite-code", "difficulty": 5, "skills": ["rm-portfolios"], "tags": ["composite-code"], "pace": 480,
    "title": "The overlapping composite",
    "prose": "A new cohort is ranked at the start of every month s and held for K months. `cohort_returns[s]` lists its K winners-minus-losers returns, in months s, s + 1, ..., s + K − 1.",
    "question": "Write `jt_composite(cohort_returns, K)`. Return one value for each month t from K − 1 to S − 1. Here S is the number of cohorts. Each value averages the month-t returns of the K live cohorts. Those are the cohorts ranked in months t − K + 1 to t.",
    "widget": {
        "kind": "code", "language": "python",
        "starter": "def jt_composite(cohort_returns, K):\n    \"\"\"The composite return in each month once K cohorts are live.\"\"\"\n    out = []\n    return out\n",
        "solution": "def jt_composite(cohort_returns, K):\n    out = []\n    for t in range(K - 1, len(cohort_returns)):\n        live = [cohort_returns[s][t - s] for s in range(t - K + 1, t + 1)]\n        out.append(sum(live) / K)\n    return out\n",
        "prelude": prelude_c,
        "examples": [comp_tests[0]],
        "tests": comp_tests,
        "how": "Check runs 8 hidden tests, with K from 1 to 6. They hold too few cohorts, exactly K cohorts, identical cohorts and 40 cohorts. Each list must match to $10^{-12}$."
    },
    "feedback": fb("Month t holds the cohorts ranked in months t − K + 1 to t. Each is in its holding month t − s, and the K are averaged.",
                   "Index each live cohort by how many months it has been held, then divide by K."),
    "explain": {"text": "Month t averages `cohort_returns[s][t - s]` over the K live cohorts, since cohort s is then in holding month $t - s$. "
                        "Averaging gives each cohort weight $1/K$; a sum would run K books at full size. The first full month is K − 1."}})

# M15 momentum-rep L3 (l15): the survival paragraph
items.append({
    "id": "e-survival-note", "difficulty": 5, "skills": ["rm-extend", "rm-paper"], "tags": ["replication-note"], "pace": 600,
    "title": "The survival paragraph",
    "kind": "longform",
    "prompt": "Your momentum replication gives these results on the seeded extension panel.\n\n"
              "- Before publication, 288 months: 6/6 with a skip earns 0.88% a month, t 2.6.\n"
              "- After publication, 168 months: 0.31% a month. The t of the difference is $-0.98$.\n"
              "- Costs: the book trades 0.60 per £1 a month, buys plus sells, at 25 bp per £1 traded.\n"
              "- The worst month after publication is a rebound after a bear market.\n\n"
              "Write the survival paragraph of the replication note, in five to eight sentences. "
              "Give the share that survived before and after costs. Say how sure we can be, and what the panel cannot show.",
    "model": "About a third of the effect survived on our panel. The 6/6 spread with a skip fell from 0.88% to 0.31% a month, so 35% survived. "
             "Costs are $0.60 \\times 25$ bp $= 0.15$ points a month. Net of them the spread fell from 0.73% to 0.16%, so about 22% survived. "
             "The fall is not significant: the t of the difference is $-0.98$. "
             "A 95% interval for the fall runs from about $-1.71$ to $+0.57$ points. It covers both no decline and the loss of the whole effect. "
             "The worst month after publication was a rebound after a bear market. Then the short loser leg carried the higher beta. "
             "The panel is seeded and plants its decline, so this tests our code, not the market. "
             "Real data would add survivorship, point-in-time universes and higher small-share costs.",
    "rubric": [
        {"points": 2, "text": "Gives the gross survival share, 0.31 / 0.88, about 35%"},
        {"points": 2, "text": "Charges 0.60 × 25 bp = 0.15 points a month and gives the net share, 0.16 / 0.73, about 22%"},
        {"points": 2, "text": "Says the fall is not significant (t −0.98), so the data cannot pin its size"},
        {"points": 1, "text": "Links the crash month to the loser leg's high beta after a fall"},
        {"points": 2, "text": "Says the seeded panel plants the effect, so the result tests the code, not markets"},
        {"points": 1, "text": "Keeps each number beside the method that produced it, in plain sentences"}]})

order = {2: [], 3: [], 4: [], 5: []}
for it in items:
    order[it["difficulty"]].append(it)
exam = {
    "id": "topic-3.1", "topic": "3.1", "name": "Research papers", "minutes": 90, "pass": 0.7,
    "skills": {"rm-paper": "Reading the paper", "rm-data": "Data and universe", "rm-portfolios": "Portfolio formation",
               "rm-stats": "Statistical evidence", "rm-extend": "Out-of-sample extension",
               "pr-method": "The distance method", "pr-trading": "Trading rules", "pr-returns": "Return calculation",
               "pr-extend": "Extension and critique"},
    "items": order[2] + order[3] + order[4] + order[5],
}
with open(OUT, "w", encoding="utf8") as f:
    json.dump(exam, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("wrote", os.path.normpath(OUT), len(exam["items"]), "items, pace", sum(i["pace"] for i in exam["items"]), "s")
