"""Build app/content/exams/topic-2.6.json (topic 2.6, Statistical modelling: the stat-models course, levels 1 to 4).

Route A for every key: the closed forms below (math and statistics.NormalDist only). check_numbers.py recomputes
each value by a second route (exact Fractions, sums over the pmf, brute-force ranks, simulation-free loops) and
asserts it at its path in the written file. Run from anywhere: python3 docs/briefs/exam-2.6-scripts/build.py
"""
import json
import math
import os
import statistics
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-2.6.json')
Z = NormalDist()


def r(x, n=6):
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


def cell(answer, tol, wrong=None):
    c = {"edit": True, "answer": answer, "tol": {"abs": tol}}
    if wrong:
        c["wrong"] = [{"id": i, "value": v, "tol": {"abs": t}} for i, v, t in wrong]
    return c


def chi2_sf(x, df):
    """Right tail of chi-square for df 1 and 2 (closed forms)."""
    if df == 1:
        return math.erfc(math.sqrt(x / 2))
    if df == 2:
        return math.exp(-x / 2)
    raise ValueError(df)


items = []

# ---------------------------------------------------------------- difficulty 2
# G1 L1 (l1): family and link for a positive time
items.append(item(
    "e-fill-time-family", 2, ["sm-glm"], ["family-link"], 60, "Time to fill",
    "A desk models the seconds until a resting limit order fills, against its queue position. Times are positive and right-skewed, and their spread grows with their mean.",
    "Which family and link suit this outcome?",
    choice([
        opt("gamma", "Gamma with a log link", correct=True),
        opt("poisson", "Poisson with a log link",
            "You matched \"positive and skewed\" to counts. Poisson is for whole-number counts, not continuous times."),
        opt("normal", "Normal with the identity link",
            "You kept the default. It allows negative times and gives every order the same variance."),
        opt("binomial", "Binomial with a logit link",
            "You picked the 0/1 family. Whether an order fills is binary, but how long it takes is not.")]),
    fb("Gamma has variance $\\phi\\mu^2$, so the spread grows with the mean, and the log link keeps $\\mu > 0$.",
       "Match the family to the outcome's values and its variance function."),
    "A time is continuous and positive. The Gamma family has variance function $\\mu^2$, so spread grows with the mean. "
    "The log link keeps every fitted mean positive."))

# G2 L1 (l2): a fitted probability of default
eta_pd = -4.2 + 6.0 * 0.5
pd = 1 / (1 + math.exp(-eta_pd))
items.append(item(
    "e-pd-at-leverage", 2, ["sm-glm"], ["logistic"], 60, "A fitted default probability",
    "A logistic PD model has $\\hat\\beta_0 = -4.2$ and $\\hat\\beta_1 = 6.0$ on leverage $L$.",
    "What is the fitted PD of a firm with $L = 0.5$? Give it in % to 2 decimal places.",
    num(r(pd), 0.00005, [("odds", r(math.exp(eta_pd)), 0.00005), ("sign", r(1 - pd), 0.00005)], unit="%",
        label="PD", accept="1 / (1 + e^{1.2}) = 23.15%"),
    fb("$\\eta = -4.2 + 6.0 \\times 0.5 = -1.2$, and $1/(1 + e^{1.2}) = 23.15\\%$.",
       "Work out $\\eta$, then apply the inverse logit $1/(1 + e^{-\\eta})$.",
       {"odds": "You stopped at the odds, $e^{-1.2} = 0.3012$. The probability is odds over 1 plus odds.",
        "sign": "You used $1/(1 + e^{-1.2}) = 76.85\\%$, the chance of no default. The sign of $\\eta$ flipped."}),
    "The linear predictor is $\\eta = -4.2 + 3.0 = -1.2$, the log odds. The odds are $e^{-1.2} = 0.3012$. "
    "So the PD is $0.3012 / 1.3012 = 23.15\\%$."))

# A1 L2 (l6, l7): F from sums of squares
F_a1 = (18 / 2) / (105 / 21)
items.append(item(
    "e-algo-f", 2, ["sm-anova"], ["f-statistic"], 60, "Three algorithms",
    "Three execution algorithms each worked 8 orders. The slippage ANOVA gives SSB = 18 and SSW = 105, in bps squared.",
    "What is $F$?",
    num(r(F_a1, 4), 0.005, [("ratio", r(18 / 105, 4), 0.005), ("total-df", r((18 / 2) / (105 / 23), 4), 0.005),
                             ("k-df", r((18 / 3) / (105 / 24), 4), 0.005)], label="F"),
    fb("MSB $= 18/2 = 9$ and MSW $= 105/21 = 5$, so $F = 1.8$.",
       "Divide each sum of squares by its degrees of freedom first.",
       {"ratio": "You divided SSB by SSW, giving 0.1714. Each needs its own degrees of freedom first.",
        "total-df": "You divided SSW by $N - 1 = 23$, giving 1.9714. Within groups the df is $N - k = 21$.",
        "k-df": "You used $k = 3$ and $N = 24$ as the df, giving 1.3714. They are $k - 1$ and $N - k$."}),
    "Between groups has $k - 1 = 2$ df, so MSB $= 9$. Within has $N - k = 24 - 3 = 21$ df, so MSW $= 5$. "
    "Their ratio is $F = 1.8$."))

# N1 L3 (l10): Mann-Whitney as a probability
items.append(item(
    "e-u-share", 2, ["sm-nonpar"], ["mann-whitney"], 45, "How often X wins",
    "Strategy X has 12 days and strategy Y has 15. Mann-Whitney gives $U_X = 99$: X won 99 of the day pairs.",
    "What is the estimated chance that a random X day beats a random Y day?",
    num(99 / 180, 0.0005, [("flipped", 1 - 99 / 180, 0.0005), ("sum", r(99 / 27, 4), 0.005)], label="Chance"),
    fb("$U_X / (mn) = 99 / 180 = 0.55$.",
       "Divide $U_X$ by the number of X-against-Y pairs.",
       {"flipped": "That is $1 - 0.55 = 0.45$, Y's chance. $U_X$ counts the pairs X wins.",
        "sum": "You divided by $12 + 15 = 27$, giving 3.6667. There are $12 \\times 15 = 180$ pairs."}),
    "Each of the 12 X days meets each of the 15 Y days, so there are 180 pairs. "
    "X won 99 of them, an estimate of $P(X > Y) = 0.55$."))

# B1 L4 (l14): beta-binomial update
items.append(item(
    "e-fill-posterior", 2, ["sm-bayes"], ["conjugate"], 60, "A new venue's fill rate",
    "A venue's fill rate $p$ has a Beta(4, 6) prior. The desk sends 50 orders and 18 fill.",
    "What is the posterior mean of $p$? Give 4 decimal places.",
    num(r(22 / 60, 4), 0.0005, [("data", 18 / 50, 0.0005), ("prior", 0.4, 0.0005), ("swapped", r(36 / 60, 4), 0.0005)],
        label="Posterior mean"),
    fb("The posterior is Beta(4 + 18, 6 + 32) = Beta(22, 38), with mean $22/60 = 0.3667$.",
       "Add the fills to the first parameter and the misses to the second.",
       {"data": "You gave the data share, $18/50 = 0.36$. The prior adds 4 fills and 6 misses.",
        "prior": "You gave the prior mean, $4/10 = 0.4$. Update it with the 18 fills and 32 misses.",
        "swapped": "You added the misses to the first parameter, giving Beta(36, 24) with mean 0.6. Fills go first."}),
    "Beta is conjugate to the binomial, so the counts add on. Beta(4, 6) with 18 fills and 32 misses gives Beta(22, 38). "
    "Its mean $22/60 = 0.3667$ sits between the prior's 0.4 and the data's 0.36."))

# ---------------------------------------------------------------- difficulty 3
# G3 L1 (l3): expected count with an offset
mu_g3 = 20 * math.exp(-0.9 + 0.045 * 18)
items.append(item(
    "e-trades-offset", 3, ["sm-glm"], ["poisson", "offset"], 90, "Trades in a 20-minute window",
    "A Poisson model of trade counts uses an offset: $\\ln E[Y] = \\ln t - 0.9 + 0.045v$. Here $t$ is the interval in minutes and $v$ the volatility in points.",
    "How many trades does it expect in a 20-minute interval at $v = 18$? Give 2 decimal places.",
    num(r(mu_g3, 4), 0.005, [("no-offset", r(mu_g3 / 20, 4), 0.005), ("times-log", r(math.log(20) * mu_g3 / 20, 4), 0.005)],
        label="Expected trades"),
    fb("$20 \\times e^{-0.9 + 0.81} = 20 \\times e^{-0.09} = 18.28$ trades.",
       "The offset multiplies the rate per minute by $t$.",
       {"no-offset": "You left out the offset, giving the rate per minute, 0.9139. Multiply by the 20 minutes.",
        "times-log": "You multiplied by $\\ln 20$, giving 2.74. The offset enters as $\\ln t$ on the log scale, so $t$ multiplies."}),
    "$-0.9 + 0.045 \\times 18 = -0.09$, so the rate is $e^{-0.09} = 0.9139$ trades a minute. "
    "The offset $\\ln 20$ adds to the log, so the count is $20 \\times 0.9139 = 18.28$."))

# G4 L1 (l4): a logistic working response
mu4 = 0.2
eta4 = math.log(mu4 / (1 - mu4))
W4 = mu4 * (1 - mu4)
z4 = eta4 + (0 - mu4) / W4
items.append(item(
    "e-working-response", 3, ["sm-glm"], ["irls"], 105, "One IRLS step",
    "In a logistic IRLS step, a firm that did not default ($y = 0$) has fitted $\\mu = 0.2$.",
    "What is its working response $z = \\eta + (y - \\mu)/W$? Give 4 decimal places.",
    num(r(z4, 4), 0.0005, [("no-weight", r(eta4 - mu4, 4), 0.0005), ("times-weight", r(eta4 - mu4 * W4, 4), 0.0005)],
        label="z"),
    fb("$\\eta = \\ln(0.2/0.8) = -1.3863$ and $W = 0.16$, so $z = -1.3863 - 1.25 = -2.6363$.",
       "Find $\\eta$ from $\\mu$, then $W = \\mu(1 - \\mu)$.",
       {"no-weight": "You added $y - \\mu$ without dividing by $W = 0.16$, giving $-1.5863$.",
        "times-weight": "You multiplied by $W$ instead of dividing, giving $-1.4183$."}),
    "The logit gives $\\eta = \\ln 0.25 = -1.3863$. The weight is $W = 0.2 \\times 0.8 = 0.16$. "
    "So $z = -1.3863 + (0 - 0.2)/0.16 = -2.6363$."))

# G5 L1 (l5): a likelihood-ratio test on two predictors
p_g5 = chi2_sf(412.6 - 405.1, 2)
items.append(item(
    "e-deviance-two", 3, ["sm-glm"], ["deviance"], 90, "Two new predictors",
    "Adding two predictors to a logistic PD model cuts its deviance from 412.6 to 405.1.",
    "What is the likelihood-ratio $p$-value? Give 4 decimal places.",
    num(r(p_g5, 4), 0.0005, [("one-df", r(chi2_sf(7.5, 1), 4), 0.0005)], label="p-value",
        accept="P(chi-square with 2 df > 7.5) = e^{-3.75} = 0.0235"),
    fb("The drop is 7.5 on 2 df, and $P(\\chi^2_2 > 7.5) = e^{-7.5/2} = 0.0235$.",
       "Refer the drop in deviance to $\\chi^2$ with one df per added coefficient.",
       {"one-df": "You used 1 df, giving 0.0062. Two added coefficients give 2 df."}),
    "The drop in deviance, $412.6 - 405.1 = 7.5$, is roughly $\\chi^2$ with 2 df. "
    "With 2 df the tail is $e^{-x/2}$, so $p = e^{-3.75} = 0.0235$."))

# A3 L2 (l8): orders per arm
z975, z80 = Z.inv_cdf(0.975), Z.inv_cdf(0.8)
n_a3 = 2 * (z975 + z80) ** 2 * 9 ** 2 / 2 ** 2
items.append(item(
    "e-orders-per-arm", 3, ["sm-anova"], ["power"], 90, "How many orders",
    "A desk will test a new algorithm against the old one. Shortfall has SD $\\sigma = 9$ bps, and the gain to detect is $\\delta = 2$ bps. The test is two-sided at 5% with 80% power.",
    "Using $n = 2(z_{0.975} + z_{0.8})^2\\sigma^2/\\delta^2$, how many orders per arm are needed, rounded up?",
    num(math.ceil(n_a3), 0, [("no-two", math.ceil(n_a3 / 2), 0),
                             ("one-sided", math.ceil(2 * (Z.inv_cdf(0.95) + z80) ** 2 * 81 / 4), 0)],
        placeholder="a whole number", label="Orders per arm"),
    fb("$2(1.9600 + 0.8416)^2 \\times 81/4 = 317.9$, so 318 orders per arm.",
       "Put $z_{0.975} = 1.9600$ and $z_{0.8} = 0.8416$ into the formula, then round up.",
       {"no-two": "You left out the factor 2, giving 159. Two arms each carry noise, which doubles the variance.",
        "one-sided": "You used $z_{0.95} = 1.6449$, a one-sided test, giving 251. The test is two-sided."}),
    "$(1.9600 + 0.8416)^2 = 7.8489$, and $2 \\times 7.8489 \\times 81 / 4 = 317.9$. "
    "Round up to 318, since 317 orders would fall just short of 80% power."))

# A7 L2 (l8): designs that avoid confounding
items.append(item(
    "e-design-confound", 3, ["sm-anova"], ["design"], 90, "Designs without confounding",
    "A desk wants to compare execution algorithms A and B on its parent orders.",
    "Which designs keep anything about the orders from following the algorithm? Select all that apply.",
    choice([
        opt("coin", "A coin flip assigns each parent order to A or B.", correct=True),
        opt("block", "Each stock-day sends one order to A and one to B, with a random choice of which goes first.", correct=True),
        opt("choose", "Traders pick the algorithm they think suits each order.",
            "You trusted judgement over chance. What traders see in an order then follows the algorithm."),
        opt("time", "A runs through January and B through February.",
            "You split by calendar. Markets change from month to month, so the month confounds the algorithm."),
        opt("size", "A works the large orders and B the small ones, so both get used.",
            "You split by size. Large orders cost more anyway, so size confounds the comparison.")], kind="multi"),
    fb("Randomising, alone or within stock-day blocks, leaves no order trait able to follow the algorithm.",
       "Ask whether anything other than chance decides which algorithm an order gets."),
    "A coin cannot see the order, so no trait can line up with the algorithm. Blocking on stock-day also cancels the shared level. "
    "Choice, the calendar and size each let a cost driver follow the algorithm."))

# N2 L3 (l10): U from the data
X = [0.4, 1.2, -0.3, 0.9]
Y = [0.1, -0.5, 0.6, 0.2, -0.1]
U_X = sum(1 for x in X for y in Y if x > y)
pooled = sorted(X + Y)
rank_sum = sum(pooled.index(x) + 1 for x in X)
items.append(item(
    "e-u-from-days", 3, ["sm-nonpar"], ["mann-whitney"], 120, "Counting the wins",
    "Daily returns in %. Strategy X: 0.4, 1.2, $-0.3$, 0.9. Strategy Y: 0.1, $-0.5$, 0.6, 0.2, $-0.1$.",
    "What is $U_X$, the number of (X day, Y day) pairs that X wins?",
    num(U_X, 0, [("rank-sum", rank_sum, 0), ("u-y", 4 * 5 - U_X, 0)], placeholder="a whole number", label="U_X"),
    fb("X's days win 4, 5, 1 and 5 pairs, so $U_X = 15$ of 20.",
       "For each X day, count the Y days below it.",
       {"rank-sum": "You gave X's rank sum, 25. Subtract $m(m + 1)/2 = 10$ to get $U_X$.",
        "u-y": "You counted the pairs Y wins, 5. $U_X$ counts X's wins."}),
    "0.4 beats four Y days, 1.2 and 0.9 beat all five, and $-0.3$ beats only $-0.5$. That is $4 + 5 + 1 + 5 = 15$. "
    "So $U_X / 20 = 0.75$ estimates $P(X > Y)$."))

# N3 L3 (l11): permutation p-value
items.append(item(
    "e-perm-p", 3, ["sm-nonpar"], ["permutation"], 75, "Reporting the shuffles",
    "A permutation test of a signal's edge runs $B = 999$ shuffles of the signal days. 12 shuffles give an edge at least as large as the real one.",
    "What $p$-value should be reported? Give 4 decimal places.",
    num(r((12 + 1) / (999 + 1), 4), 0.00005, [("raw", r(12 / 999, 6), 0.00005)], label="p-value"),
    fb("$(12 + 1)/(999 + 1) = 0.0130$.",
       "Count the real labelling as one of the arrangements.",
       {"raw": "You divided 12 by 999, giving 0.0120. Add the real data to both counts: $(c + 1)/(B + 1)$."}),
    "The observed labelling is one of the possible arrangements, so it joins both counts. "
    "That gives $(12 + 1)/(999 + 1) = 0.0130$, never below the floor $1/1000$."))

# N4 L3 (l12): Silverman's bandwidth
h_n4 = 0.9 * min(1.6, 1.75 / 1.34) * 250 ** (-0.2)
items.append(item(
    "e-silverman-250", 3, ["sm-nonpar"], ["kde"], 105, "A bandwidth for 250 days",
    "A year of 250 daily returns has SD 1.6% and IQR 1.75%. Silverman's rule is $h = 0.9\\min(s, \\text{IQR}/1.34)\\,n^{-1/5}$.",
    "What is $h$, in % to 4 decimal places?",
    num(r(h_n4, 4), 0.0005, [("used-s", r(0.9 * 1.6 * 250 ** (-0.2), 4), 0.0005), ("no-n", r(0.9 * 1.75 / 1.34, 4), 0.0005)],
        label="h, in %"),
    fb("$\\text{IQR}/1.34 = 1.3060$ is below 1.6, so $h = 0.9 \\times 1.3060 \\times 250^{-0.2} = 0.3896$.",
       "Take the smaller of $s$ and IQR/1.34, then scale by $n^{-1/5}$.",
       {"used-s": "You used $s = 1.6$, giving 0.4773. The rule takes the smaller spread, $1.3060$.",
        "no-n": "You left out $n^{-1/5} = 0.3314$, giving 1.1754. More data narrows the kernel."}),
    "$1.75/1.34 = 1.3060$, below $s = 1.6$, so the IQR sets the spread. $250^{-0.2} = 0.3314$. "
    "So $h = 0.9 \\times 1.3060 \\times 0.3314 = 0.3896$%."))

# N6 L2 (l9): the sign test with ties
p_n6 = 2 * sum(math.comb(18, k) for k in range(14, 19)) / 2 ** 18
p_n6_20 = 2 * sum(math.comb(20, k) for k in range(14, 21)) / 2 ** 20
items.append(item(
    "e-sign-test-ties", 3, ["sm-nonpar"], ["sign-test"], 105, "Twenty stock-days",
    "A paired execution test ran over 20 stock-days. B had the lower shortfall on 14, A on 4, and 2 were tied.",
    "What is the two-sided sign-test $p$-value? Give 4 decimal places.",
    num(r(p_n6, 4), 0.0005, [("one-sided", r(p_n6 / 2, 4), 0.0005), ("kept-ties", r(p_n6_20, 4), 0.0005)],
        label="p-value"),
    fb("Drop the 2 ties: $2P(X \\ge 14)$ for $X \\sim \\mathrm{Bin}(18, 0.5)$ is $2 \\times 4{,}048/262{,}144 = 0.0309$.",
       "Drop the ties, then double the binomial tail at 14 of 18.",
       {"one-sided": "You gave one tail, 0.0154. The question asks for two-sided, so double it.",
        "kept-ties": "You kept the ties as losses, 14 of 20, giving 0.1153. A tie favours neither side, so drop it."}),
    "Ties carry no sign, so 18 days remain. $P(X \\ge 14) = (3{,}060 + 816 + 153 + 18 + 1)/2^{18} = 0.0154$. "
    "Doubling for two sides gives 0.0309."))

# B2 L4 (l14): gamma-Poisson update
items.append(item(
    "e-default-rate", 3, ["sm-bayes"], ["conjugate"], 90, "A loan book's default rate",
    "A loan book's yearly default count is Poisson($\\lambda$). The prior is Gamma(3, rate 2). Five years bring 2, 0, 3, 1 and 1 defaults.",
    "What is the posterior mean of $\\lambda$? Give 4 decimal places.",
    num(r(10 / 7, 4), 0.0005, [("no-periods", 10 / 2, 0.0005), ("data", 7 / 5, 0.0005)], label="Posterior mean"),
    fb("The posterior is Gamma(3 + 7, rate 2 + 5) = Gamma(10, 7), with mean $10/7 = 1.4286$.",
       "Add the total count to the shape and the number of years to the rate.",
       {"no-periods": "You added the 7 defaults but not the 5 years, giving $10/2 = 5$. Each year adds 1 to the rate.",
        "data": "You gave the data mean, $7/5 = 1.4$. The prior adds 3 defaults over 2 years."}),
    "Gamma is conjugate to the Poisson: the shape gains the 7 defaults and the rate the 5 years. "
    "Gamma(10, 7) has mean $10/7 = 1.4286$, between the prior's 1.5 and the data's 1.4."))

# B3 L4 (l14): normal prior on alpha
post_b3 = (0 / 1.5 ** 2 + 8 / 3 ** 2) / (1 / 1.5 ** 2 + 1 / 3 ** 2)
items.append(item(
    "e-alpha-prior", 3, ["sm-bayes"], ["normal-normal"], 90, "A sceptical prior on alpha",
    "A new fund's alpha is estimated at 8% a year, with standard error 3%. The prior is $N(0, 1.5^2)$, in %.",
    "What is the posterior mean alpha, in %?",
    num(r(post_b3 / 100, 6), 0.0005, [("average", 0.04, 0.0005), ("inverted", r(8 * (4 / 9) / (5 / 9) / 100, 6), 0.0005)],
        unit="%", label="Posterior mean", accept="(8/9) / (4/9 + 1/9) = 1.6%"),
    fb("Precisions $4/9$ and $1/9$ add to $5/9$, so the mean is $(8/9)/(5/9) = 1.6\\%$.",
       "Weight each mean by its precision, one over its variance.",
       {"average": "You averaged 0 and 8 equally, giving 4%. The prior is four times as precise as the estimate.",
        "inverted": "You weighted by variance instead of precision, giving 6.4%. The noisier source must count less."}),
    "The prior has precision $1/1.5^2 = 4/9$ and the estimate $1/3^2 = 1/9$. The posterior mean is $(0 \\times 4/9 + 8 \\times 1/9)/(5/9) = 1.6\\%$. "
    "The precise prior pulls the noisy 8% most of the way to 0."))

# B5 L4 (l16): one Metropolis step on the log scale
ln_ratio = -15.1 - (-14.2)
accept5 = math.log(0.35) < ln_ratio
items.append(item(
    "e-metropolis-log", 3, ["sm-mcmc"], ["metropolis"], 90, "A step on the log scale",
    "A random-walk Metropolis chain sits at $x = 1.20$ and proposes $x' = 0.95$. The log posterior is $-14.2$ at 1.20 and $-15.1$ at 0.95. The uniform draw is $u = 0.35$.",
    "Where is the chain after this step?",
    num(0.95 if accept5 else 1.20, 0.001, [("reject", 1.20 if accept5 else 0.95, 0.001)], label="x after the step"),
    fb("$\\ln u = -1.0498 < -0.9$, so the proposal is accepted and the chain moves to 0.95.",
       "Compare $\\ln u$ with the difference of the log posteriors.",
       {"reject": "You rejected a worse proposal and stayed at 1.20. Metropolis still accepts it when $\\ln u$ is below $-0.9$, as here."}),
    "The log ratio is $-15.1 + 14.2 = -0.9$, a ratio of $e^{-0.9} = 0.4066$. Since $u = 0.35$ is below it, the chain moves to 0.95. "
    "Refusing every downhill move would leave the chain stuck at a mode."))

# B6 L4 (l17): effective sample size
ess6 = 6000 * (1 - 0.75) / (1 + 0.75)
items.append(item(
    "e-ess-sticky", 3, ["sm-mcmc"], ["ess"], 75, "What 6,000 draws are worth",
    "After burn-in a chain keeps 6,000 draws. It behaves like an AR(1) with $\\phi = 0.75$.",
    "What is its effective sample size by the AR(1) rule $n(1 - \\phi)/(1 + \\phi)$? Give 1 decimal place.",
    num(r(ess6, 2), 0.05, [("one-minus", 6000 * 0.25, 0.05), ("over-one-plus", r(6000 / 1.75, 2), 0.05)], label="ESS"),
    fb("$6{,}000 \\times 0.25/1.75 = 857.1$ draws' worth.",
       "Multiply by $1 - \\phi$ and divide by $1 + \\phi$.",
       {"one-minus": "You multiplied by $1 - \\phi$ but did not divide by $1 + \\phi = 1.75$, giving 1,500.",
        "over-one-plus": "You divided by $1 + \\phi$ but did not multiply by $1 - \\phi = 0.25$, giving 3,428.6."}),
    "Strong autocorrelation makes neighbouring draws repeat each other. $(1 - 0.75)/(1 + 0.75) = 0.1429$, so 6,000 draws act like 857.1 independent ones. "
    "Standard errors must use the 857.1, not the 6,000."))

# ---------------------------------------------------------------- difficulty 4
# A2 L2 (l6, l7): an ANOVA table from three brokers' orders
brokers = {"A": [2, 3, 3, 4], "B": [4, 5, 5, 6], "C": [5, 7, 8, 8]}
allv = [v for g in brokers.values() for v in g]
gm = sum(allv) / len(allv)
SSB = sum(len(g) * (sum(g) / len(g) - gm) ** 2 for g in brokers.values())
SSW = sum(sum((v - sum(g) / len(g)) ** 2 for v in g) for g in brokers.values())
SST = sum((v - gm) ** 2 for v in allv)
MSB, MSW = SSB / 2, SSW / 9
items.append(item(
    "e-broker-anova", 4, ["sm-anova"], ["anova-table"], 240, "Three brokers' slippage",
    "Slippage in bps on four orders each. Broker A: 2, 3, 3, 4. Broker B: 4, 5, 5, 6. Broker C: 5, 7, 8, 8.",
    "Fill the ANOVA table. Give MS within and $F$ to 4 decimal places.",
    {"kind": "table", "columns": ["Source", "SS", "df", "MS", "$F$"],
     "rows": [["Between brokers", cell(SSB, 0.005), "2", cell(MSB, 0.005), cell(r(MSB / MSW, 4), 0.005, [("ss-ratio", SSB / SSW, 0.005)])],
              ["Within brokers", cell(SSW, 0.005, [("total", SST, 0.005)]), "9", cell(r(MSW, 4), 0.0005, [("n-minus-one", r(SSW / 11, 4), 0.0005)]), ""]]},
    fb("Means 3, 5 and 7 around 5 give SSB = 32 and SSW = 10. So $F = 16 / 1.1111 = 14.4$.",
       "Find each broker's mean and the grand mean, then the two sums of squares.",
       {"ss-ratio": "You divided SSB by SSW, giving 3.2. Divide the mean squares instead.",
        "total": "You entered the total SS, 42. Within means each order's distance from its own broker's mean.",
        "n-minus-one": "You divided SSW by $N - 1 = 11$, giving 0.9091. Within has $N - k = 9$ df."}),
    "SSB $= 4[(3 - 5)^2 + 0 + (7 - 5)^2] = 32$ and SSW $= 2 + 2 + 6 = 10$; together they make SST = 42. "
    "MSB $= 16$ and MSW $= 10/9 = 1.1111$. So $F = 14.4$, far beyond the 5% cut of 4.2565."))

# N5 L3 (l13): median and scaled MAD with a takeover day
R5 = [-0.8, 0.3, 0.5, 0.2, -0.1, 0.9, 7.9]
med5 = statistics.median(R5)
mad5 = statistics.median([abs(x - med5) for x in R5])
items.append(parts(
    "e-takeover-week", 4, ["sm-nonpar"], ["robust"], 180, "A week with a takeover",
    "A stock's daily returns over seven days, in %: $-0.8$, 0.3, 0.5, 0.2, $-0.1$, 0.9 and 7.9. The 7.9 was a takeover bid.",
    "Two robust summaries.",
    [("What is the median daily return, in %?",
      num(med5, 0.005, [("mean", r(sum(R5) / 7, 4), 0.005)], label="Median"),
      fb("Sorted, the middle of seven values is the fourth: 0.3.",
         "Sort the seven returns and take the middle one.",
         {"mean": "You gave the mean, $8.9/7 = 1.2714$. The takeover day drags it; the median ignores it."})),
     ("What is the scaled MAD, $1.4826 \\times \\text{median}|r - \\text{median}|$? Give 4 decimal places.",
      num(r(1.4826 * mad5, 4), 0.0005, [("raw", mad5, 0.0005), ("sd", r(statistics.stdev(R5), 4), 0.0005)],
          label="Scaled MAD"),
      fb("The distances from 0.3 have median 0.4, so the scaled MAD is $1.4826 \\times 0.4 = 0.5930$.",
         "Take each distance from the median, find their median, then scale by 1.4826.",
         {"raw": "You stopped at the raw MAD, 0.4. Scaling by 1.4826 makes it comparable with an SD.",
          "sd": "You gave the sample SD, 2.9702. One takeover day inflates it."}))],
    "The median is the fourth of seven sorted values, 0.3, whatever the takeover day does. "
    "The distances from it have median 0.4, so the scaled MAD is 0.5930. The mean and SD, 1.2714 and 2.9702, are dragged by one day."))

# B4 L4 (l15): posterior predictive against plug-in
pred0 = (7 / 8) ** 10
plug0 = math.exp(-10 / 7)
items.append(parts(
    "e-no-defaults-next", 4, ["sm-bayes"], ["predictive"], 180, "A year with no defaults",
    "A loan book's default rate has posterior Gamma(10, rate 7). Next year's count is Poisson($\\lambda$). Its predictive is negative binomial, with $P(0) = \\left(\\tfrac{7}{8}\\right)^{10}$.",
    "Compare the predictive with plugging in the mean.",
    [("What is the predictive chance of no defaults next year? Give 4 decimal places.",
      num(r(pred0, 4), 0.0005, [("plug-in", r(plug0, 4), 0.0005)], label="P(no defaults)"),
      fb("$(7/8)^{10} = 0.2631$.",
         "Raise rate over rate plus 1 to the power of the shape.",
         {"plug-in": "You plugged in $\\lambda = 10/7$, giving $e^{-1.4286} = 0.2397$. That ignores the doubt about $\\lambda$."})),
     ("Why is the predictive chance above the plug-in's 0.2397?",
      choice([
          opt("doubt", "It averages over $\\lambda$, and low-$\\lambda$ draws make a quiet year more likely.", correct=True),
          opt("prior", "The prior pulls $\\lambda$ down, so the predictive mean is lower.",
              "You blamed the mean. Both use the same mean, $10/7$; the predictive adds spread."),
          opt("bias", "The plug-in is biased, so the predictive corrects its mean.",
              "You treated it as a bias. The plug-in has the right mean but too little spread."),
          opt("rounding", "It is rounding: the two agree to 2 decimal places.",
              "You dismissed the gap. 0.2631 against 0.2397 differ in the second decimal.")]),
      fb("Doubt about $\\lambda$ widens the predictive, which puts more weight in both tails, including 0.",
         "Ask what the predictive averages over that the plug-in fixes."))],
    "The plug-in fixes $\\lambda = 10/7$ and gives $e^{-1.4286} = 0.2397$. The predictive averages $e^{-\\lambda}$ over the posterior, giving 0.2631. "
    "Averaging over doubt fattens the tails, so a quiet year is more likely."))

# B8 L4 (l18): beta shrinkage of a hit rate
a8, b8 = 18, 22
w8 = 60 / (60 + a8 + b8)
items.append(parts(
    "e-hit-rate-shrink", 4, ["sm-hier", "sm-bayes"], ["shrinkage"], 180, "Shrinking a hit rate",
    "A desk's strategies share a population of hit rates fitted as Beta(18, 22), with mean 0.45 and $\\hat\\kappa = 40$. One strategy won 33 of its 60 trades.",
    "Shrink its hit rate towards the population.",
    [("What weight $n/(n + \\hat\\kappa)$ does its own record get?",
      num(w8, 0.0005, [("kappa", r(40 / 100, 4), 0.0005)], label="Weight"),
      fb("$60/(60 + 40) = 0.6$.",
         "Divide its trades by its trades plus $\\hat\\kappa$.",
         {"kappa": "You gave the population's weight, $40/100 = 0.4$. The record's weight is $n/(n + \\hat\\kappa)$."})),
     ("What is its shrunk hit rate? Give 4 decimal places.",
      num(r((a8 + 33) / (a8 + b8 + 60), 4), 0.0005, [("raw", 33 / 60, 0.0005), ("pop", 0.45, 0.0005)],
          label="Shrunk rate"),
      fb("$(18 + 33)/(40 + 60) = 0.51$, which is $0.45 + 0.6 \\times (0.55 - 0.45)$.",
         "Add the population's 18 wins and 22 losses to the record.",
         {"raw": "You gave the raw rate, $33/60 = 0.55$. Sixty trades still carry noise.",
          "pop": "You gave the population mean, 0.45. The record gets weight 0.6."}))],
    "The population acts like 40 earlier trades with 18 wins. So the shrunk rate is $51/100 = 0.51$. "
    "That moves the raw 0.55 four tenths of the way to 0.45."))

# Ncode L3 (l10): the Hodges-Lehmann estimate of a paired gain


def walsh_median(d):
    w = sorted((d[i] + d[j]) / 2 for i in range(len(d)) for j in range(i, len(d)))
    return statistics.median(w)


hl_cases = [
    ("[1.0, 2.0, 9.0]", [1.0, 2.0, 9.0]),
    ("[0.4, -0.2, 1.1, 0.3, 2.5]", [0.4, -0.2, 1.1, 0.3, 2.5]),
    ("[-1.2, 0.5, 0.8, 0.1, 2.9, 6.0]", [-1.2, 0.5, 0.8, 0.1, 2.9, 6.0]),
    ("GAINS", None),
    ("[3.0, 3.0, 3.0, 10.0, 10.0]", [3.0, 3.0, 3.0, 10.0, 10.0]),
    ("[-4.0, -0.5, 0.2]", [-4.0, -0.5, 0.2]),
    ("[0.0, 3.0, 4.0]", [0.0, 3.0, 4.0]),
]
prelude_hl = "GAINS = [round(0.8 + 1.5 * ((7 * i) % 11 - 5) / 5 + (6.0 if i % 4 == 0 else 0.0), 2) for i in range(40)]\n"
ns_hl = {}
exec(prelude_hl, ns_hl)
hl_tests = []
for call, d in hl_cases:
    dd = ns_hl["GAINS"] if d is None else d
    hl_tests.append({"call": f"walsh_median({call})", "expect": repr(round(walsh_median(dd), 12)), "compare": "isclose",
                     "tol": {"abs": 1e-9}})
items.append({
    "id": "e-walsh-median", "difficulty": 4, "skills": ["sm-nonpar"], "tags": ["hodges-lehmann"], "pace": 360,
    "title": "A robust paired gain",
    "prose": "A paired test gives `d`, the within-day shortfall saving of B over A in bps, one per stock-day. "
             "The Hodges-Lehmann estimate is the median of the Walsh averages $(d_i + d_j)/2$ over all $i \\le j$, each day with itself included.",
    "question": "Write `walsh_median(d)` returning that median. A list of $n$ days has $n(n + 1)/2$ Walsh averages.",
    "widget": {
        "kind": "code", "language": "python",
        "starter": "import statistics\n\n\ndef walsh_median(d):\n    \"\"\"Hodges-Lehmann estimate: the median of the Walsh averages.\"\"\"\n    return statistics.median(d)\n",
        "solution": "import statistics\n\n\ndef walsh_median(d):\n    n = len(d)\n    w = [(d[i] + d[j]) / 2 for i in range(n) for j in range(i, n)]\n    return statistics.median(w)\n",
        "prelude": prelude_hl,
        "examples": [{"call": "walsh_median([1.0, 3.0])", "expect": "2.0", "compare": "isclose", "tol": {"abs": 1e-9}}],
        "tests": hl_tests,
        "how": "Check runs 7 hidden tests. They hold skewed days, a tie, an even count of averages and 40 days with spikes. Each answer must match to $10^{-9}$."
    },
    "feedback": fb("Pair every day with itself and every later day, average each pair, and take the median of those.",
                   "Loop $j$ from $i$, not $i + 1$, so each day's own value counts once."),
    "explain": {"text": "The Walsh averages include $(d_i + d_i)/2 = d_i$, so $n$ days give $n(n + 1)/2$ of them. "
                        "Their median is the estimate that goes with the Wilcoxon signed-rank test. A spike moves few averages, so it barely shifts the median."}})

# ---------------------------------------------------------------- difficulty 5
# G6 L1 (l5): overdispersion and the quasi-Poisson test
phi6 = 588 / (200 - 4)
se_q = 0.028 * math.sqrt(phi6)
p_q = math.erfc((0.072 / se_q) / math.sqrt(2))
p_pois = math.erfc((0.072 / 0.028) / math.sqrt(2))
items.append(parts(
    "e-rejections-dispersion", 5, ["sm-glm"], ["overdispersion"], 300, "Rejected orders on volatile days",
    "A Poisson GLM of daily rejected orders has 4 coefficients and is fitted on 200 days. Its Pearson $\\chi^2$ is 588. "
    "The volatility coefficient is 0.072 with Poisson standard error 0.028.",
    "Check the dispersion, then test the coefficient again.",
    [("What is the estimated dispersion $\\hat\\phi = \\chi^2/(n - p)$?",
      num(r(phi6, 4), 0.005, [("n", r(588 / 200, 4), 0.005)], label="Dispersion"),
      fb("$588/(200 - 4) = 3.0$, three times the Poisson variance.",
         "Divide by the residual degrees of freedom, $n - p$.",
         {"n": "You divided by $n = 200$, giving 2.94. Four fitted coefficients use 4 df."})),
     ("What is the quasi-Poisson standard error of the coefficient? Give 4 decimal places.",
      num(r(se_q, 4), 0.0005, [("phi", r(0.028 * phi6, 4), 0.0005), ("divided", r(0.028 / math.sqrt(phi6), 4), 0.0005)],
          label="Standard error"),
      fb("$0.028 \\times \\sqrt{3} = 0.0485$.",
         "Scale the Poisson standard error by $\\sqrt{\\hat\\phi}$.",
         {"phi": "You multiplied by $\\hat\\phi = 3$, giving 0.084. Variances scale by $\\hat\\phi$, standard errors by its root.",
          "divided": "You divided by $\\sqrt{3}$, giving 0.0162. Overdispersion widens the errors."})),
     ("What is the two-sided $p$-value of the coefficient with that standard error? Give 4 decimal places.",
      num(r(p_q, 4), 0.0005, [("poisson", r(p_pois, 4), 0.0005)], label="p-value"),
      fb("$z = 0.072/0.0485 = 1.485$, so $p = 0.1376$: not significant at 5%.",
         "Divide the coefficient by its new standard error and take both tails of $N(0, 1)$.",
         {"poisson": "You kept the Poisson error, $z = 2.571$ and $p = 0.0101$. That trusts a variance three times too small."}))],
    "The Pearson ratio is 3.0, so the counts vary three times as much as Poisson allows. "
    "Standard errors grow by $\\sqrt{3}$, from 0.028 to 0.0485. The $p$-value rises from 0.0101 to 0.1376, and the signal is no longer significant."))

# Kcode L2 and L3 (l7, l10): ANOVA on ranks


def avg_ranks(values):
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return ranks


def kruskal_h(groups):
    flat = [v for g in groups for v in g]
    rk = avg_ranks(flat)
    n = len(flat)
    rbar = sum(rk) / n
    pos, ssb = 0, 0.0
    for g in groups:
        rg = rk[pos:pos + len(g)]
        pos += len(g)
        ssb += len(g) * (sum(rg) / len(g) - rbar) ** 2
    sst = sum((x - rbar) ** 2 for x in rk)
    return (n - 1) * ssb / sst


kw_cases = [
    ("[[1.0, 2.0], [3.0, 9.0]]", [[1.0, 2.0], [3.0, 9.0]]),
    ("[[2, 3, 3, 4], [4, 5, 5, 6], [5, 7, 8, 8]]", [[2, 3, 3, 4], [4, 5, 5, 6], [5, 7, 8, 8]]),
    ("[[0.5, 9.0, 1.2], [1.1, 0.7], [3.3, 2.8, 4.0, 2.9]]", [[0.5, 9.0, 1.2], [1.1, 0.7], [3.3, 2.8, 4.0, 2.9]]),
    ("[[1.0, 1.0, 2.0, 7.0], [1.0, 2.0, 2.0]]", [[1.0, 1.0, 2.0, 7.0], [1.0, 2.0, 2.0]]),
    ("SLIP", None),
    ("[[10.0, 20.0, 30.0], [1.0, 2.0, 3.0], [100.0, 200.0, 300.0]]", [[10.0, 20.0, 30.0], [1.0, 2.0, 3.0], [100.0, 200.0, 300.0]]),
]
prelude_kw = ("SLIP = [[round(1.5 + ((5 * i + 3 * g) % 13) / 4 + (12.0 if i == 4 else 0.0), 2) for i in range(10 + 2 * g)]\n"
              "        for g in range(3)]\n")
ns_kw = {}
exec(prelude_kw, ns_kw)
kw_tests = []
for call, g in kw_cases:
    gg = ns_kw["SLIP"] if g is None else g
    kw_tests.append({"call": f"kruskal_h({call})", "expect": repr(round(kruskal_h(gg), 12)), "compare": "isclose",
                     "tol": {"abs": 1e-9}})
kw_tests.append({"call": "kruskal_h([[1.0, 2.0], [3.0, 400.0]]) == kruskal_h([[1.0, 2.0], [3.0, 4.0]])", "expect": "True",
                 "compare": "equal"})
items.append({
    "id": "e-kruskal-h", "difficulty": 5, "skills": ["sm-nonpar", "sm-anova"], "tags": ["rank-anova"], "pace": 480,
    "title": "An ANOVA on ranks",
    "prose": "`groups` is a list of lists of slippages, one list per broker. A rank version of the one-way ANOVA "
             "ranks all orders together, from 1 for the smallest. Tied values share the average of their ranks.",
    "question": "Write `kruskal_h(groups)`. Rank the pooled orders, then return $H = (N - 1)\\,\\text{SSB}/\\text{SST}$ computed on the ranks. "
                "Here $N$ is the number of orders.",
    "widget": {
        "kind": "code", "language": "python",
        "starter": "def kruskal_h(groups):\n    \"\"\"H from the pooled ranks.\"\"\"\n"
                   "    flat = [v for g in groups for v in g]\n    n = len(flat)\n    mean = sum(flat) / n\n"
                   "    ssb = sum(len(g) * (sum(g) / len(g) - mean) ** 2 for g in groups)\n"
                   "    sst = sum((v - mean) ** 2 for v in flat)\n    return (n - 1) * ssb / sst\n",
        "solution": "def kruskal_h(groups):\n    flat = [v for g in groups for v in g]\n    n = len(flat)\n"
                    "    order = sorted(range(n), key=lambda i: flat[i])\n    ranks = [0.0] * n\n    i = 0\n"
                    "    while i < n:\n        j = i\n        while j + 1 < n and flat[order[j + 1]] == flat[order[i]]:\n            j += 1\n"
                    "        for k in range(i, j + 1):\n            ranks[order[k]] = (i + j) / 2 + 1\n        i = j + 1\n"
                    "    rbar = (n + 1) / 2\n    ssb, pos = 0.0, 0\n    for g in groups:\n        rg = ranks[pos:pos + len(g)]\n"
                    "        pos += len(g)\n        ssb += len(g) * (sum(rg) / len(g) - rbar) ** 2\n"
                    "    sst = sum((x - rbar) ** 2 for x in ranks)\n    return (n - 1) * ssb / sst\n",
        "prelude": prelude_kw,
        "examples": [{"call": "kruskal_h([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])", "expect": repr(round(kruskal_h([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]), 12)),
                      "compare": "isclose", "tol": {"abs": 1e-9}}],
        "tests": kw_tests,
        "how": "Check runs 7 hidden tests. They hold ties, unequal group sizes, a wild order, the ANOVA table's brokers and three groups of up to 14. Each $H$ must match to $10^{-9}$."
    },
    "feedback": fb("Ranks replace the slippages, ties share their average rank, and the ANOVA ratio is taken on the ranks.",
                   "Compute the ranks first, with tied values sharing the mean of their places, then the sums of squares."),
    "explain": {"text": "On ranks the grand mean is $(N + 1)/2$, and $(N - 1)\\,\\text{SSB}/\\text{SST}$ is the Kruskal-Wallis $H$ with its tie correction. "
                        "A wild order becomes just the top rank, so it cannot swamp SSB. Refer $H$ to $\\chi^2$ with $k - 1$ df."}})

order_d = {2: [], 3: [], 4: [], 5: []}
for it in items:
    order_d[it["difficulty"]].append(it)
exam = {
    "id": "topic-2.6", "topic": "2.6", "name": "Statistical modelling", "minutes": 75, "pass": 0.7,
    "skills": {"sm-glm": "Generalised linear models", "sm-anova": "Analysis of variance and design",
               "sm-nonpar": "Nonparametric methods", "sm-bayes": "Bayesian inference",
               "sm-mcmc": "Markov chain Monte Carlo", "sm-hier": "Hierarchical models"},
    "items": order_d[2] + order_d[3] + order_d[4] + order_d[5],
}
with open(OUT, "w", encoding="utf8") as f:
    json.dump(exam, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("wrote", os.path.normpath(OUT), len(exam["items"]), "items, pace", sum(i["pace"] for i in exam["items"]), "s")
