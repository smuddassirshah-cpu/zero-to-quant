"""Items of topic-3.2, part B: the measure-prob items M1 to M11 (plan numbers)."""
from helpers import *

M = {}

# ---------------------------------------------------------------- M1
M[1] = item(
    "e-atoms-three-sets", 2, ["mt-sigma"], ["sigma-count"], 60,
    title="Counting events from three generators",
    prose="Let $\\Omega = \\{1, 2, \\ldots, 9\\}$ and $A = \\{1, 2, 3, 4\\}$, $B = \\{3, 4, 5, 6\\}$, $C = \\{6, 7\\}$.",
    question="How many events does the sigma-algebra $\\sigma(A, B, C)$ contain?",
    widget=numeric(64, abs_=0, placeholder="a whole number", label="Number of events",
                   wrong=[("generators", 8, 0), ("power-set", 512, 0)], accept="64"),
    feedback=fb("The atoms are $\\{1,2\\}, \\{3,4\\}, \\{5\\}, \\{6\\}, \\{7\\}, \\{8,9\\}$. Six atoms give $2^6 = 64$ events.",
                "Split $\\Omega$ into atoms by membership of $A$, $B$ and $C$. Each event is a union of atoms.",
                {"generators": "You counted $2^3$, one choice for each generator. Complements and intersections make smaller atoms, and there are six.",
                 "power-set": "You counted $2^9$, the power set. The sigma-algebra cannot tell 1 from 2, or 8 from 9."}),
    explain="Points in the same sets of $A$, $B$, $C$ cannot be told apart. That leaves six atoms: 1 and 2, 3 and 4, 5, 6, 7, and 8 and 9. Each event is a union of atoms, so there are $2^6 = 64$.")

# ---------------------------------------------------------------- M3
M[3] = item(
    "e-tail-integral", 2, ["mt-integral"], ["tail-integral"], 75,
    title="A mean from the tail",
    prose="A non-negative random variable $X$ has $P(X > t) = 1$ for $t < 2$ and $P(X > t) = (2/t)^3$ for $t \\ge 2$.",
    question="What is $E[X]$?",
    widget=numeric(3, abs_=0, placeholder="a number", label="Mean",
                   wrong=[("no-flat-part", 1, 0), ("lost-half", 4, 0)], accept="3"),
    feedback=fb("$E[X] = \\int_0^\\infty P(X > t)\\,dt = 2 + \\int_2^\\infty 8t^{-3}\\,dt = 2 + 1 = 3$.",
                "Integrate the tail $P(X > t)$ from 0 to infinity, in two pieces.",
                {"no-flat-part": "You left out $\\int_0^2 1\\,dt = 2$. The tail equals 1 on $[0, 2)$, and that area counts.",
                 "lost-half": "You made $\\int_2^\\infty 8t^{-3}\\,dt$ equal 2. The antiderivative is $-4t^{-2}$, which gives 1."}),
    explain="For $X \\ge 0$, $E[X] = \\int_0^\\infty P(X > t)\\,dt$. The flat part gives $\\int_0^2 1\\,dt = 2$. The power tail gives $\\int_2^\\infty 8t^{-3}\\,dt = [-4t^{-2}]_2^\\infty = 1$.")

# ---------------------------------------------------------------- M10
M[10] = item(
    "e-die-reweight", 2, ["mt-change"], ["radon-nikodym-die"], 60,
    title="A second moment under a reweighted die",
    prose="A fair die has measure $P$, and $X$ is the face. A second measure $Q$ puts chances $(0.35, 0.25, 0.15, 0.10, 0.10, 0.05)$ on faces 1 to 6. The weight is $Z = \\tfrac{dQ}{dP}$, face by face.",
    question="What is $E_Q[X^2]$? Give one decimal place.",
    widget=numeric(8.6, abs_=0.01, placeholder="a decimal", label="Second moment",
                   wrong=[("no-weight", 15.17, 0.01), ("square-of-mean", 6.25, 0.01)], accept="8.6 within 0.01"),
    feedback=fb("$Z = 6Q = (2.1, 1.5, 0.9, 0.6, 0.6, 0.3)$ and $E_Q[X^2] = E_P[ZX^2] = \\tfrac16(2.1 + 6 + 8.1 + 9.6 + 15 + 10.8) = 8.6$.",
                "Weight each face by $Z$ under $P$, or add $Q(k)k^2$ over the faces.",
                {"no-weight": "You gave $E_P[X^2] = 91/6$. That ignores the weight $Z$. Under $Q$ low faces are likelier.",
                 "square-of-mean": "You squared $E_Q[X] = 2.5$. The mean of the square is larger than the square of the mean."}),
    explain="Each face has $Z(k) = Q(k)/P(k) = 6Q(k)$, so $Z = (2.1, 1.5, 0.9, 0.6, 0.6, 0.3)$ with mean 1. Then $E_Q[X^2] = E_P[ZX^2] = \\tfrac{51.6}{6} = 8.6$. Adding $Q(k)k^2$ directly gives the same.")

# ---------------------------------------------------------------- M2
M[2] = item(
    "e-sigma-families", 3, ["mt-sigma"], ["sigma-axioms"], 120,
    title="Which families are sigma-algebras",
    prose="Let $\\Omega = \\{a, b, c, d\\}$. Each family below contains $\\emptyset$ and $\\Omega$.",
    question="Select all that apply: which families are sigma-algebras on $\\Omega$?",
    widget=multi([
        ("f1", "$\\{\\emptyset, \\Omega, \\{a\\}, \\{b,c,d\\}\\}$", True, None),
        ("f2", "$\\{\\emptyset, \\Omega, \\{a\\}, \\{b\\}\\}$", False, "The complement of $\\{a\\}$ is $\\{b,c,d\\}$, which is missing."),
        ("f3", "$\\{\\emptyset, \\Omega, \\{a,b\\}, \\{c,d\\}, \\{a\\}, \\{b,c,d\\}\\}$", False, "It is closed under complements, but $\\{a\\} \\cup \\{c,d\\} = \\{a,c,d\\}$ is missing."),
        ("f4", "$\\{\\emptyset, \\Omega, \\{a,b\\}, \\{c,d\\}, \\{a,c\\}, \\{b,d\\}\\}$", False, "Closed under complements, but $\\{a,b\\} \\cap \\{a,c\\} = \\{a\\}$ is missing."),
        ("f5", "All 16 subsets of $\\Omega$", True, None),
        ("f6", "$\\{\\emptyset, \\Omega, \\{a,b\\}\\}$", False, "The complement of $\\{a,b\\}$ is $\\{c,d\\}$, which is missing."),
    ]),
    feedback=fb("Only the first family and the power set are closed under complements and unions.",
                "Test each family for complements first, then for unions of two of its sets."),
    explain="A sigma-algebra is closed under complements and countable unions. $\\{a\\}$ with $\\{b,c,d\\}$ passes, and so does the power set. The other four fail on a complement or a union.")

# ---------------------------------------------------------------- M5
M[5] = item(
    "e-var-of-condexp", 3, ["mt-condexp"], ["condexp-variance"], 120,
    title="The variance of a conditional mean",
    prose="A fair die shows $X$. The sigma-algebra $\\mathcal G$ is generated by the three sets $\\{1,2,3,4\\}$, $\\{5\\}$ and $\\{6\\}$.",
    question="What is $\\mathrm{Var}(E[X \\mid \\mathcal G])$? Give four decimal places.",
    widget=numeric(2.08333, abs_=0.0005, placeholder="a decimal", label="Variance",
                   wrong=[("within-block-mean", 0.8333, 0.0005), ("whole-variance", 2.9167, 0.0005)], accept="2.0833 within 0.0005"),
    feedback=fb("The block means are 2.5, 5 and 6 with chances $\\tfrac46, \\tfrac16, \\tfrac16$. Their variance about 3.5 is $\\tfrac{25}{12} = 2.0833$.",
                "Replace $X$ by its block mean, then take the variance of that three-valued variable.",
                {"within-block-mean": "You gave $E[\\mathrm{Var}(X \\mid \\mathcal G)] = \\tfrac56$, the other half of the split. The question asks for the variance of the means.",
                 "whole-variance": "You gave $\\mathrm{Var}(X) = \\tfrac{35}{12}$. Averaging inside blocks removes the within-block part."}),
    explain="$E[X \\mid \\mathcal G]$ takes the values 2.5, 5, 6 with chances $\\tfrac46, \\tfrac16, \\tfrac16$, and mean 3.5. Its variance is $\\tfrac46 \\cdot 1 + \\tfrac16 \\cdot 2.25 + \\tfrac16 \\cdot 6.25 = \\tfrac{25}{12}$. The rest of $\\tfrac{35}{12}$ is the within-block part $\\tfrac56$.")

# ---------------------------------------------------------------- M6
def yn(ans):
    return {"edit": True, "answer": ans, "accept": [ans[0]]}


M[6] = item(
    "e-adapted-predictable", 3, ["mt-condexp", "mt-martingale"], ["adapted-predictable"], 150,
    title="Adapted or predictable",
    prose="A fair coin walk has $S_n = \\xi_1 + \\cdots + \\xi_n$ with steps $\\xi_n = \\pm 1$ and $S_0 = 0$. A betting rule $H_n$ is adapted if known at time $n$. It is predictable if known at time $n - 1$.",
    question="Type yes or no in each cell.",
    widget={"kind": "table", "columns": ["Rule $H_n$", "Adapted", "Predictable"],
            "rows": [["$S_{n-1}$", yn("yes"), yn("yes")],
                     ["$S_n$", yn("yes"), yn("no")],
                     ["1 if $\\xi_{n+1} = +1$, else 0", yn("no"), yn("no")],
                     ["$\\max(S_0, \\ldots, S_{n-1})$", yn("yes"), yn("yes")],
                     ["$S_{n-1}\\,\\xi_n$", yn("yes"), yn("no")]]},
    feedback=fb("A rule built from $S_0, \\ldots, S_{n-1}$ is predictable. One that needs $\\xi_n$ is only adapted. One that needs $\\xi_{n+1}$ is neither.",
                "For each rule, name the last toss it needs. Compare that toss with $n - 1$ and $n$.",
                {"r0c1": "$S_{n-1}$ uses only tosses up to $n - 1$, so it is known at time $n$.",
                 "r0c2": "$S_{n-1}$ uses only tosses up to $n - 1$, so it is predictable.",
                 "r1c1": "$S_n$ uses toss $n$, which is known at time $n$. So it is adapted.",
                 "r1c2": "$S_n$ needs toss $n$, which is not known at time $n - 1$. It is not predictable.",
                 "r2c1": "The rule looks at toss $n + 1$, which is in the future at time $n$. It is not adapted.",
                 "r2c2": "A rule that is not even adapted cannot be predictable.",
                 "r3c1": "A running maximum up to $S_{n-1}$ is known by time $n$.",
                 "r3c2": "The maximum of $S_0, \\ldots, S_{n-1}$ is known at time $n - 1$, so it is predictable.",
                 "r4c1": "$S_{n-1}\\,\\xi_n$ uses tosses up to $n$, which are all known at time $n$. So it is adapted.",
                 "r4c2": "The factor $\\xi_n$ is toss $n$, which is unknown at time $n - 1$. So the rule is not predictable."}),
    explain="Predictable means measurable with respect to $\\mathcal F_{n-1}$, and adapted means measurable with respect to $\\mathcal F_n$. The rules $S_{n-1}$ and the running maximum use tosses up to $n - 1$. The rules $S_n$ and $S_{n-1}\\xi_n$ need toss $n$, and the look-ahead rule needs toss $n + 1$.")

# ---------------------------------------------------------------- M7
M[7] = item(
    "e-ruin-by-martingale", 3, ["mt-martingale"], ["ruin-martingale"], 150,
    title="Ruin on a biased walk",
    prose="A walk starts at 0 and steps $+1$ with chance 0.4 and $-1$ with chance 0.6. The process $M_n = 1.5^{S_n}$ is a martingale. The walk stops on first reaching $+3$ or $-2$.",
    question="What is the chance it stops at $+3$? Give four decimal places.",
    widget=numeric(0.18957, abs_=0.0005, placeholder="a decimal", label="Probability",
                   wrong=[("fair-walk", 0.4, 0.0005), ("ratio-inverted", 0.6398, 0.0005)], accept="0.1896 within 0.0005"),
    feedback=fb("Optional stopping gives $P \\cdot 1.5^3 + (1 - P) \\cdot 1.5^{-2} = 1$, so $P = 0.1896$.",
                "Check $E[1.5^{\\xi}] = 1$, then set $E[M_\\tau] = M_0 = 1$ and solve for $P$.",
                {"fair-walk": "You used the fair-walk answer $2/5$, which ignores the bias. The drift is downward, so the chance is lower.",
                 "ratio-inverted": "You used $1.5^{-S_n}$, the inverted odds ratio, which is not a martingale for these chances."}),
    explain="The step factor has mean $0.4 \\cdot 1.5 + 0.6/1.5 = 1$, so $M_n$ is a martingale. Stopping at $+3$ or $-2$ gives $P \\cdot 3.375 + (1 - P) \\cdot 0.4444 = 1$. Hence $P = 0.5556/2.9306 = 0.1896$.")

# ---------------------------------------------------------------- M9
M[9] = item(
    "e-is-weight", 3, ["mt-change"], ["importance-weight"], 90,
    title="One importance-sampling weight",
    prose="We estimate the tail of $P = N(0, 1)$ by drawing from $Q = N(2.5, 1)$. One draw lands at $x = 3.2$. The weight is $\\tfrac{dP}{dQ}(x) = \\tfrac{\\varphi(x)}{\\varphi(x - 2.5)}$.",
    question="What weight does this draw carry? Give four decimal places.",
    widget=numeric(0.007635, abs_=0.0001, placeholder="a decimal", label="Weight",
                   wrong=[("upside-down", 130.9, 0.5), ("no-half-theta-squared", 0.0003, 0.0001)], accept="0.0076 within 0.0001"),
    feedback=fb("$\\tfrac{dP}{dQ}(x) = e^{-\\theta x + \\theta^2/2} = e^{-8 + 3.125} = e^{-4.875} = 0.0076$.",
                "Divide the two densities: the constants cancel, leaving $e^{-\\theta x + \\theta^2/2}$.",
                {"upside-down": "You inverted the ratio, $e^{+4.875}$. A draw this far out is over-sampled, so its weight is below 1.",
                 "no-half-theta-squared": "You left out the $\\theta^2/2 = 3.125$ and got $e^{-8}$. Expanding $(x - \\theta)^2$ leaves that term."}),
    explain="The density ratio is $\\exp(-\\tfrac{x^2}{2} + \\tfrac{(x - \\theta)^2}{2}) = e^{-\\theta x + \\theta^2/2}$. At $\\theta = 2.5$ and $x = 3.2$ the exponent is $-8 + 3.125 = -4.875$. So the weight is 0.0076.")

# ---------------------------------------------------------------- M4
M[4] = item(
    "e-swap-limits", 4, ["mt-integral"], ["limit-swap"], 210,
    title="When the limit passes through the mean",
    prose="$U$ is uniform on $[0, 1]$. Each sequence $X_n$ below has an almost sure limit. Compare $E[X_n]$ as $n \\to \\infty$ with the mean of that limit.",
    question="Select all that apply: which sequences have $E[X_n] \\to E[\\lim X_n]$?",
    widget=multi([
        ("a", "$U^{1/n}$", True, None),
        ("b", "$n^2\\,\\mathbf 1_{\\{U < 1/n^2\\}}$", False, "Its mean is $n^2 \\cdot n^{-2} = 1$ for every $n$, but the limit is 0 almost surely. No integrable variable dominates it."),
        ("c", "$\\sqrt n\\,U^n$", True, None),
        ("d", "$ne^{-nU}$", False, "Its mean is $1 - e^{-n} \\to 1$, but $ne^{-nU} \\to 0$ for every $U > 0$. The mass piles up near $U = 0$."),
        ("e", "$\\min(n, 1/U)$", True, None),
    ]),
    feedback=fb("A, C and E: the swap holds. B and D put mass on a thin region near a point, and the limit loses it.",
                "For each one, find the mean and the limit, then compare."),
    explain="A and C have means $n/(n+1) \\to 1$ and $\\sqrt n/(n+1) \\to 0$, matching their limits 1 and 0. E increases to $1/U$, so monotone convergence gives an infinite mean on both sides. B and D have mean tending to 1 and limit 0.")

# ---------------------------------------------------------------- M11
M[11] = parts_item(
    "e-tree-price", 4, ["mt-change", "mt-martingale"], ["risk-neutral-tree"], 270,
    title="Pricing on a two-step tree",
    prose="A share has $S_0 = 60$. Each step it multiplies by $u = 1.24$ or $d = 0.84$, and cash grows by $1 + r = 1.05$ a step. The real-world chance of an up move is $p = 0.6$. A call struck at $K = 60$ expires after two steps.",
    question="Three follow-up questions.",
    parts=[
        dict(question="What is the risk-neutral chance $q$ of an up move? Give three decimal places.",
             widget=numeric(0.525, abs_=0.0005, placeholder="a decimal", label="q",
                            wrong=[("real-world-chance", 0.6, 0.0005), ("weights-swapped", 0.475, 0.0005)], accept="0.525 within 0.0005"),
             feedback=fb("$q = (1.05 - 0.84)/(1.24 - 0.84) = 0.525$.",
                         "Choose $q$ so that the discounted share is a martingale: $q \\cdot 74.4 + (1 - q) \\cdot 50.4 = 60 \\cdot 1.05$.",
                         {"real-world-chance": "You used the real-world 0.6. The pricing chance is set by $u$, $d$ and $r$ alone.",
                          "weights-swapped": "You swapped the weights, $(u - 1 - r)/(u - d)$. The up weight is $(1 + r - d)/(u - d)$."})),
        dict(question="What is the price of the call? Give three decimal places.",
             widget=numeric(9.19314, abs_=0.0006, placeholder="a decimal", label="Price",
                            wrong=[("real-world-weights", 11.619, 0.001), ("no-discounting", 10.135, 0.001)], accept="9.193 within 0.0006"),
             feedback=fb("The payoffs are 32.256, 2.496 and 0. So the price is $[q^2 \\cdot 32.256 + 2q(1 - q) \\cdot 2.496]/1.05^2 = 9.193$.",
                         "Weight the three payoffs with $q$, then discount two steps.",
                         {"real-world-weights": "You weighted with $p = 0.6$. The price uses $q$, not $p$.",
                          "no-discounting": "You took the $Q$-mean payoff, 10.135, and did not discount two steps by $1.05^2$."})),
        dict(question="Why does the real-world chance 0.6 not enter the price?",
             widget=choice([
                 ("a", "The price is a replication cost, so it cannot depend on $p$.", True, None),
                 ("b", "Discounting averages the chance 0.6 away over the two steps, so $p$ cancels out.", False,
                  "Discounting multiplies by $1.05^{-2}$, which has no link to $p$. Nothing cancels that way."),
                 ("c", "The chance 0.6 enters only through $q$, which is why $q$ sits below 0.6.", False,
                  "$q = 0.525$ is computed from $u$, $d$ and $r$ alone. The number 0.6 is not an input."),
                 ("d", "It matters for a call, but not for a put, by put-call parity.", False,
                  "A put is priced by replication too, so $p$ matters for neither. Parity only links the two prices."),
             ]),
             feedback=fb("A replicating portfolio costs the same whatever the real-world chances. The chance $q$ makes discounted prices martingales.",
                         "Ask what the price is: the cost of a portfolio that reproduces the payoff in every state."))],
    explain="Part a solves $q \\cdot 74.4 + (1 - q) \\cdot 50.4 = 63$. Part b is the $Q$-mean of the payoff, discounted. The real-world chance moves expected profit, but not the cost of replication.")

# ---------------------------------------------------------------- M8
M[8] = item(
    "e-variance-split", 5, ["mt-condexp"], ["variance-split"], 360,
    title="Variance splits in two",
    prose="Let $X$ be square-integrable and $\\mathcal G$ a sigma-algebra. Write $Y = E[X \\mid \\mathcal G]$ and $\\mu = E[X]$. We prove $\\mathrm{Var}(X) = E[\\mathrm{Var}(X \\mid \\mathcal G)] + \\mathrm{Var}(E[X \\mid \\mathcal G])$.",
    question="Put the proof in order. Move the two flawed lines to Left out.",
    widget=order([
        ("s1", "Write $X - \\mu = (X - Y) + (Y - \\mu)$.", None),
        ("s2", "Square and take expectations: two squares and a cross term.", None),
        ("s3", "Take out what is known, $Y - \\mu$. The cross term is $E[(Y - \\mu)\\,E[X - Y \\mid \\mathcal G]]$.", None),
        ("s4", "Since $E[X - Y \\mid \\mathcal G] = 0$, the cross term is 0.", None),
        ("s5", "As $E[Y] = \\mu$, $E[(Y - \\mu)^2] = \\mathrm{Var}(E[X \\mid \\mathcal G])$.", None),
        ("s6", "By the tower, $E[(X - Y)^2] = E[\\mathrm{Var}(X \\mid \\mathcal G)]$.", None),
        ("s7", "Add the two surviving terms to get the split.", None),
        ("d1", "The cross term is 0 because $X - Y$ and $Y - \\mu$ are independent.", "They are orthogonal, not independent. Orthogonality is what the zero conditional mean gives."),
        ("d2", "Take out $Y - \\mu$: the cross term is $(Y - \\mu)\\,E[X - Y]$.", "Taking out what is known leaves the conditional mean $E[X - Y \\mid \\mathcal G]$, not the plain mean, and the product stays inside $E$."),
    ], ["s1", "s2", "s3", "s4", "s5", "s6", "s7"], distractors=["d1", "d2"]),
    feedback=fb("The cross term dies by taking out what is known. The two squares are the two parts of the split. Lines 5 and 6 may swap.",
                "Split $X - \\mu$, square, remove the cross term, then identify the two squares."),
    explain="Writing $X - \\mu = (X - Y) + (Y - \\mu)$ and squaring gives three terms. The cross term vanishes because $E[X - Y \\mid \\mathcal G] = 0$. The squares are $E[\\mathrm{Var}(X \\mid \\mathcal G)]$ and $\\mathrm{Var}(E[X \\mid \\mathcal G])$.")
M[8]["widget"]["same"] = [["s5", "s6"]]

ITEMS = M
