"""Build app/content/exams/topic-2.5.json (topic 2.5, Numerical methods and optimisation: convex and numerics).

Route A for every key: the closed forms below. check_numbers.py recomputes each value by a second route and
asserts it at its path in the written file. Run from anywhere: python3 docs/briefs/exam-2.5-scripts/build.py
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-2.5.json')


def r(x, n=6):
    return round(x, n)


def fb(correct, generic, by_key=None):
    d = {"correct": correct, "generic": generic}
    if by_key:
        d["byKey"] = by_key
    return d


def num(answer, tol, wrong=(), unit=None, placeholder="a number", label="Answer", accept=None, rel=False):
    t = {"rel": tol} if rel else {"abs": tol}
    w = {"kind": "numeric", "answer": answer, "tol": t, "placeholder": placeholder, "label": label}
    if unit:
        w["unit"] = unit
    if accept:
        w["accept"] = accept
    if wrong:
        w["wrong"] = [{"id": i, "value": v, "tol": ({"rel": tt} if rel else {"abs": tt})} for i, v, tt in wrong]
    return w


def expr(answer, accept, wrong=(), keyboard="algebra"):
    w = {"kind": "expression", "answer": answer, "accept": list(accept), "keyboard": keyboard}
    if wrong:
        w["wrong"] = [{"id": i, "tex": t} for i, t in wrong]
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


def line(id, text, why=None):
    d = {"id": id, "text": text}
    if why:
        d["why"] = why
    return d


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

# ================================================================ difficulty 2
# convex L2 (l6): the best corner of a small LP
corners = {(0, 0): 0, (4, 0): 12, (0, 4): 16, (2, 3): 18}
lp_best = max(corners.values())
items.append(item(
    "e-lp-corner", 2, ["cv-lp"], ["vertex"], 90, "The best corner",
    "Two strategies earn £3k and £4k per unit of size, $x$ and $y$. "
    "The limits are $x + 2y \\le 8$ for risk and $3x + 2y \\le 12$ for margin, with $x, y \\ge 0$.",
    "What is the largest total profit, in £ thousand?",
    num(lp_best, 0.001, [("axis-y", 16, 0.001), ("axis-x", 12, 0.001), ("infeasible", 24, 0.001)], label="Profit (£k)"),
    fb("The corner $(2, 3)$, where both limits bind, earns $6 + 12 = 18$.",
       "List the corners of the feasible region and price each.",
       {"axis-y": "You stopped at the corner $(0, 4)$, worth 16. Moving along the risk limit to $(2, 3)$ earns more.",
        "axis-x": "You stopped at the corner $(4, 0)$, worth 12. The corner $(2, 3)$ earns more.",
        "infeasible": "You used $(0, 6)$, which breaks the risk limit, since $0 + 12 > 8$."}),
    "The corners are $(0, 0)$, $(4, 0)$, $(0, 4)$ and $(2, 3)$, where $x + 2y = 8$ meets $3x + 2y = 12$. "
    "Their profits are 0, 12, 16 and 18. "
    "A linear objective on a bounded polygon is largest at a corner, so the best is 18."))

# convex L2 (l8): weak duality as a sandwich
items.append(item(
    "e-duality-sandwich", 2, ["cv-duality", "cv-lp"], ["weak-duality"], 75, "A plan and an offer",
    "For a maximising LP, a desk finds a feasible plan earning 8.4. "
    "It also finds a feasible point of the dual, whose cost is 9.6.",
    "What do these two numbers tell us about the optimal value $p^*$?",
    choice([
        opt("ok", "$8.4 \\le p^* \\le 9.6$", correct=True),
        opt("mid", "$p^* = 9$, halfway between",
            "You averaged the bounds. Weak duality traps $p^*$ between them but does not place it."),
        opt("flip", "$p^* \\le 8.4$ or $p^* \\ge 9.6$",
            "You turned the bounds round. A feasible plan is a floor for a maximum, and a dual cost is a ceiling."),
        opt("nothing", "Nothing, until both problems are solved",
            "You waited for the optima. Weak duality holds for every feasible pair, so these two already bound $p^*$.")]),
    fb("Any feasible plan earns at most any feasible dual cost, so $p^*$ lies in $[8.4, 9.6]$.",
       "Which number is a floor, and which a ceiling?"),
    "A feasible plan earns at most $p^*$, so $p^* \\ge 8.4$. "
    "Weak duality says every feasible dual point costs at least $p^*$, so $p^* \\le 9.6$. "
    "The gap of 1.2 bounds how far the plan can be from optimal."))

# convex L4 (l14): the largest stable step
items.append(item(
    "e-step-limit", 2, ["cv-descent"], ["step-size"], 75, "How big a step",
    "We minimise $f(\\mathbf x) = \\tfrac12\\mathbf x^T\\mathbf H\\mathbf x$ with $\\mathbf H = \\begin{pmatrix}6.45&6.05\\\\6.05&6.45\\end{pmatrix}$, "
    "whose eigenvalues are 0.4 and 12.5. Gradient descent uses a fixed step $s$.",
    "Below what value must $s$ lie for the iterates to converge from every start?",
    num(2 / 12.5, 0.0005, [("min", 2 / 0.4, 0.0005), ("one-step", 1 / 12.5, 0.0005), ("best", r(2 / 12.9, 4), 0.0005)],
        placeholder="a decimal", label="s"),
    fb("Each step multiplies the error along an eigenvector by $1 - s\\lambda$, so we need $s < \\tfrac{2}{12.5} = 0.16$.",
       "Ask when $|1 - s\\lambda| < 1$ for both eigenvalues.",
       {"min": "You used the smaller eigenvalue. The steep direction, $\\lambda = 12.5$, sets the limit.",
        "one-step": "That step, $\\tfrac{1}{\\lambda_{\\max}} = 0.08$, clears the steep direction at once. Larger steps still converge, up to 0.16.",
        "best": "That is the best fixed step, $\\tfrac{2}{\\lambda_{\\min} + \\lambda_{\\max}} = 0.155$. The question asks for the limit, 0.16."}),
    "Along each eigenvector the error is multiplied by $1 - s\\lambda$ every step. "
    "Both factors lie in $(-1, 1)$ exactly when $0 < s < \\tfrac{2}{\\lambda_{\\max}} = 0.16$. "
    "At $s = 0.16$ the steep factor is $-1$, and the error there swings for ever."))

# numerics L1 (l1): the gap between doubles
gap = 2.0 ** (21 - 52)
items.append(item(
    "e-double-gap", 2, ["nm-float"], ["spacing"], 90, "The gap between neighbours",
    "A double has 52 stored mantissa bits. Take $x = 3{,}000{,}000$, which lies between $2^{21}$ and $2^{22}$.",
    "What is the gap between $x$ and the next larger double? Give it to 3 significant figures.",
    num(gap, 0.001, [("at-one", 2.0 ** -52, 0.001), ("next-power", 2.0 ** (22 - 52), 0.001),
                     ("half-gap", 3e6 * 2.0 ** -53, 0.001)], placeholder="for example 1e-10", label="Gap", rel=True),
    fb("The gap is $2^{21 - 52} = 2^{-31} \\approx 4.66 \\times 10^{-10}$.",
       "The gap is $2^{-52}$ times the power of two at or below $x$.",
       {"at-one": "You gave the gap above 1. It doubles at each power of two, so near $2^{21}$ it is $2^{-31}$.",
        "next-power": "You used $2^{22}$. The gap is set by the power of two at or below $x$, which is $2^{21}$.",
        "half-gap": "You computed $xu$, a bound on the rounding error. The gap between neighbours is $2^{-31}$."}),
    "Between $2^{21}$ and $2^{22}$ the doubles are evenly spaced. "
    "The gap is $2^{21} \\times 2^{-52} = 2^{-31}$, which Python prints as 4.656612873077393e-10. "
    "So a price stored near three million can carry only about nine decimal places."))

# numerics L2 (l5): bisection steps
n_bis = math.ceil(math.log2(2 / 1e-6))
items.append(item(
    "e-bisection-count", 2, ["nm-roots"], ["bisection"], 75, "How many halvings",
    "Bisection starts on the bracket $[1, 3]$ and halves it each step.",
    "How many steps make the bracket narrower than $10^{-6}$?",
    num(n_bis, 0, [("floor", n_bis - 1, 0)], placeholder="a whole number", label="Steps"),
    fb("We need $2 / 2^n < 10^{-6}$, so $2^n > 2 \\times 10^6$ and $n = 21$.",
       "Solve $\\tfrac{2}{2^n} < 10^{-6}$ for the smallest whole $n$.",
       {"floor": "You rounded down. After 20 steps the width is $2 / 2^{20} \\approx 1.9 \\times 10^{-6}$, still too wide."}),
    "After $n$ steps the width is $2 / 2^n$. "
    "We need $2^n > 2 \\times 10^6$, and $2^{20} = 1{,}048{,}576$ is too small while $2^{21} = 2{,}097{,}152$ is enough. "
    "So 21 steps, whatever the function, as long as it is continuous with a sign change."))

# numerics L4 (l15): a Monte Carlo standard error
s_mc, n_mc = 12.3, 40000
se = s_mc / math.sqrt(n_mc)
items.append(item(
    "e-mc-error", 2, ["nm-mc"], ["standard-error"], 75, "A price with its error",
    "A Monte Carlo call price uses 40,000 paths. The payoffs have sample standard deviation £12.30.",
    "What is the standard error of the price, in pounds? Give it to 4 decimal places.",
    num(r(se, 4), 0.0001, [("by-n", r(s_mc / n_mc, 6), 0.00001), ("by-root-s", r(math.sqrt(s_mc) / math.sqrt(n_mc), 6), 0.0001)],
        unit="£", placeholder="a decimal", label="SE"),
    fb("$\\tfrac{12.30}{\\sqrt{40{,}000}} = \\tfrac{12.30}{200} = £0.0615$.",
       "Divide the standard deviation by $\\sqrt n$.",
       {"by-n": "You divided by $n$. The standard error falls like $\\tfrac{1}{\\sqrt n}$, so divide by 200.",
        "by-root-s": "You took the square root of the standard deviation too. Only $n$ goes under the root."}),
    "The standard error of a mean is $\\tfrac{s}{\\sqrt n}$. "
    "Here that is $\\tfrac{12.30}{200} = £0.0615$. "
    "Halving it would need four times as many paths."))

# ================================================================ difficulty 3
# convex L1 (l1): which sets are convex
items.append(item(
    "e-convex-sets", 3, ["cv-convex"], ["convex-sets"], 150, "Six sets in the plane",
    "Each set is a region of the $(x, y)$ plane.",
    "Which sets are convex? Select all that apply.",
    choice([
        opt("disc-half", "$\\{x^2 + y^2 \\le 4\\} \\cap \\{y \\ge x\\}$", correct=True),
        opt("one-branch", "$\\{xy \\ge 1,\\ x > 0\\}$", correct=True),
        opt("square", "$\\{\\max(|x|, |y|) \\le 1\\}$", correct=True),
        opt("two-branch", "$\\{xy \\ge 1\\}$",
            "You pictured one branch. $(1, 1)$ and $(-1, -1)$ are in the set, but their midpoint $(0, 0)$ is not."),
        opt("outside", "$\\{|x| \\ge 1\\}$",
            "You saw two half-planes and called the union convex. The midpoint of $(1, 0)$ and $(-1, 0)$ is outside."),
        opt("circle", "$\\{x^2 + y^2 = 1\\}$",
            "You took the circle for the disc. The chord from $(1, 0)$ to $(-1, 0)$ passes through the centre, which is not on the circle.")],
        kind="multi"),
    fb("An intersection of convex sets, the region above $\\tfrac1x$ for $x > 0$, and a square are convex.",
       "For each set, look for two points whose midpoint escapes."),
    "A half-plane and a disc are convex, so their intersection is. "
    "For $x > 0$ the set is $y \\ge \\tfrac1x$, above a convex function, and the square is a ball of the max norm. "
    "The two branches, the region $|x| \\ge 1$ and the circle each have a chord that leaves the set."))

# convex L1 (l2): the Hessian test
k_min = 9 / 4
items.append(item(
    "e-hessian-threshold", 3, ["cv-convex"], ["hessian-test"], 120, "When a quadratic bowls",
    "Let $f(x, y) = x^2 + 3xy + ky^2$.",
    "What is the smallest $k$ for which $f$ is convex on the whole plane?",
    num(k_min, 0.001, [("diagonal", 0, 0.001), ("coefficients", 9, 0.001), ("entry", 1.5, 0.001)], label="k"),
    fb("The Hessian $\\begin{pmatrix}2&3\\\\3&2k\\end{pmatrix}$ is positive semidefinite when $4k - 9 \\ge 0$, so $k \\ge 2.25$.",
       "Write the Hessian and ask when it is positive semidefinite.",
       {"diagonal": "You checked only the diagonal, $2k \\ge 0$. The determinant $4k - 9$ must be at least 0 too.",
        "coefficients": "You used the coefficients as the matrix, $\\begin{pmatrix}1&3\\\\3&k\\end{pmatrix}$. The Hessian of $x^2$ is 2, so the determinant is $4k - 9$.",
        "entry": "You required $2k \\ge 3$, comparing an entry with the off-diagonal. The test is the determinant, $4k \\ge 9$."}),
    "The Hessian is $\\begin{pmatrix}2&3\\\\3&2k\\end{pmatrix}$, constant over the plane. "
    "A symmetric 2 by 2 matrix is positive semidefinite when its diagonal and determinant are at least 0. "
    "Here that needs $4k - 9 \\ge 0$, so $k \\ge \\tfrac94 = 2.25$."))

# convex L2 (l7): linprog's default bounds
items.append(item(
    "e-linprog-bounds", 3, ["cv-lp"], ["linprog-bounds"], 120, "A short that never happens",
    "A long-short desk maximises $\\mathbf c^T\\mathbf x$ with `linprog(-c, A_ub=A, b_ub=b)`, passing no `bounds`. "
    "One asset has a negative expected return, yet the solver always gives it weight 0, never a short.",
    "Why?",
    choice([
        opt("ok", "With no `bounds`, `linprog` holds every weight at or above 0.", correct=True),
        opt("status", "`res.status` must be 2, so the problem is infeasible.",
            "You blamed feasibility. A weight of 0 is a feasible answer; the bounds simply forbid going below it."),
        opt("sign", "`linprog` maximises, so passing $-\\mathbf c$ flipped the objective.",
            "You reversed the sign rule. `linprog` minimises, so $-\\mathbf c$ is right for a maximum."),
        opt("slack", "A weight of 0 means its constraint row is slack.",
            "You mixed up weights and rows. Slack is the room left in a row of `A_ub`, not a weight.")]),
    fb("The default bounds $(0, \\infty)$ forbid every short.",
       "Ask what `linprog` assumes about each variable when no bounds are passed."),
    "Without `bounds`, `linprog` holds every variable in $[0, \\infty)$. "
    "So the best it can do with a losing asset is weight 0. "
    "A long-short problem must pass `bounds=(None, None)`, or a finite range per asset."))

# convex L3 (l9): the dual function
g = lambda lam: 3 * lam - lam ** 2 / 4
g_sign = lambda lam: -3 * lam - lam ** 2 / 4
items.append(parts(
    "e-dual-function", 3, ["cv-duality"], ["dual-function"], 180, "A floor from one multiplier",
    "Minimise $(x + 1)^2$ subject to $x \\ge 2$. Write the limit as $2 - x \\le 0$, with multiplier $\\lambda \\ge 0$.",
    "Two questions on the dual function $g(\\lambda) = \\min_x \\left[(x + 1)^2 + \\lambda(2 - x)\\right]$.",
    [("What is $g(2)$?",
      num(g(2), 0.001, [("p-star", 9, 0.001), ("sign", g_sign(2), 0.001)], label="g(2)"),
      fb("The minimiser is $x = \\tfrac{\\lambda}{2} - 1 = 0$, so $g(2) = 1 + 4 = 5$.",
         "Minimise over $x$ first: set the derivative in $x$ to 0.",
         {"p-star": "You gave the optimum, 9. $g(2)$ is only a floor below it.",
          "sign": "You priced the limit as $x - 2$, which gives $-7$. With $2 - x \\le 0$ the term is $\\lambda(2 - x)$."})),
     ("Which $\\lambda$ maximises $g$?",
      num(6, 0.001, [("p-star", 9, 0.001), ("no-half", 3, 0.001)], label="λ*"),
      fb("$g(\\lambda) = 3\\lambda - \\tfrac{\\lambda^2}{4}$ peaks at $\\lambda = 6$, where $g = 9 = p^*$.",
         "Differentiate $g(\\lambda) = 3\\lambda - \\tfrac{\\lambda^2}{4}$.",
         {"p-star": "You gave the best value, 9. The question asks for the multiplier that reaches it.",
          "no-half": "You solved $3 - \\lambda = 0$. The derivative of $\\tfrac{\\lambda^2}{4}$ is $\\tfrac{\\lambda}{2}$, so $\\lambda = 6$."}))],
    "Setting $2(x + 1) - \\lambda = 0$ gives $x = \\tfrac{\\lambda}{2} - 1$ and $g(\\lambda) = 3\\lambda - \\tfrac{\\lambda^2}{4}$. "
    "So $g(2) = 5$, a floor below $p^* = 9$. "
    "The problem is convex and $x = 3$ is strictly feasible, so the best floor $g(6) = 9$ meets $p^*$."))

# convex L3 (l12): SLSQP's inequality sign
items.append(item(
    "e-slsqp-sign", 3, ["cv-qp"], ["slsqp-constraint"], 120, "A variance cap for SLSQP",
    "We minimise a portfolio's tracking cost with `minimize(..., method='SLSQP', constraints=cons)`. "
    "The variance must be at most 0.02, where `S` is the covariance matrix.",
    "Which entry in `cons` states that limit?",
    choice([
        opt("ok", "`{'type': 'ineq', 'fun': lambda w: 0.02 - w @ S @ w}`", correct=True),
        opt("flip", "`{'type': 'ineq', 'fun': lambda w: w @ S @ w - 0.02}`",
            "You wrote the limit the wrong way round. SciPy's `ineq` means `fun(w) >= 0`, so this demands variance of at least 0.02."),
        opt("eq", "`{'type': 'eq', 'fun': lambda w: 0.02 - w @ S @ w}`",
            "You made it an equality. That forces variance to exactly 0.02, even when less risk is better."),
        opt("bool", "`{'type': 'ineq', 'fun': lambda w: w @ S @ w <= 0.02}`",
            "You returned a comparison. SLSQP needs a number whose sign it can follow, not `True` or `False`.")]),
    fb("SciPy's `ineq` means `fun(w) >= 0`, so the cap is $0.02 - \\mathbf w^T\\mathbf S\\mathbf w \\ge 0$.",
       "Rewrite the limit as something $\\ge 0$."),
    "SLSQP reads `'ineq'` as `fun(w) >= 0`. "
    "The cap $\\mathbf w^T\\mathbf S\\mathbf w \\le 0.02$ becomes $0.02 - \\mathbf w^T\\mathbf S\\mathbf w \\ge 0$. "
    "The reversed form would ask for at least 0.02 of variance."))

# convex L4 (l15): rate from the condition number
lmin, lmax = 0.5, 12
kap = lmax / lmin
rho = (kap - 1) / (kap + 1)
n_steps = math.ceil(math.log(1e6) / -math.log(rho))
rho_one = 1 - lmin / lmax
n_one = math.ceil(math.log(1e6) / -math.log(rho_one))
items.append(parts(
    "e-rate-from-kappa", 3, ["cv-descent"], ["linear-rate"], 150, "Steps from the condition number",
    "Gradient descent minimises a positive definite quadratic whose Hessian has eigenvalues 0.5 and 12. "
    "It uses the best fixed step, $s = \\tfrac{2}{\\lambda_{\\min} + \\lambda_{\\max}}$.",
    "Two questions on the rate.",
    [("By what factor $\\rho$ does the worst error shrink each step?",
      num(r(rho, 4), 0.0005, [("one-over", r(rho_one, 4), 0.0005)], label="ρ"),
      fb("$\\kappa = 24$, so $\\rho = \\tfrac{23}{25} = 0.92$.",
         "Use $\\rho = \\tfrac{\\kappa - 1}{\\kappa + 1}$ with $\\kappa = \\tfrac{\\lambda_{\\max}}{\\lambda_{\\min}}$.",
         {"one-over": "You used the step $\\tfrac{1}{\\lambda_{\\max}}$, whose factor is $1 - \\tfrac{1}{24} = 0.9583$. The best step gives 0.92."})),
     ("How many steps cut the error by a factor of $10^6$?",
      num(n_steps, 0, [("floor", n_steps - 1, 0), ("one-over", n_one, 0)], placeholder="a whole number", label="Steps"),
      fb("$\\tfrac{\\ln 10^6}{\\ln(25/23)} = 165.7$, so 166 steps.",
         "Solve $0.92^n \\le 10^{-6}$ for the smallest whole $n$.",
         {"floor": "You rounded 165.7 down. After 165 steps the factor is still above $10^{-6}$.",
          "one-over": "You used the factor 0.9583 of the step $\\tfrac{1}{\\lambda_{\\max}}$. That needs 325 steps, nearly twice as many."}))],
    "$\\kappa = \\tfrac{12}{0.5} = 24$, so the best fixed step shrinks the error by $\\rho = \\tfrac{23}{25} = 0.92$ a step. "
    "Then $n \\ge \\tfrac{\\ln 10^6}{\\ln(25/23)} = 165.7$, so 166 steps. "
    "The rule of thumb $\\tfrac{\\kappa}{2}\\ln 10^6 \\approx 166$ agrees."))

# convex L4 (l16): Newton for a minimum
x1 = 1 - (math.e - 3) / math.e
items.append(parts(
    "e-newton-minimise", 3, ["cv-descent"], ["newton-minimise"], 150, "Newton on a convex curve",
    "We minimise $f(x) = e^x - 3x$, which is strictly convex with minimum at $\\ln 3 \\approx 1.0986$. "
    "Newton's method starts at $x_0 = 1$.",
    "Two questions on the first steps.",
    [("What is $x_1$? Give it to 4 decimal places.",
      num(r(x1, 4), 0.00005, [("root-of-f", 0, 0.00005), ("descent", r(1 - (math.e - 3), 4), 0.00005)], label="x₁"),
      fb("$x_1 = 1 - \\tfrac{e - 3}{e} = \\tfrac{3}{e} = 1.1036$.",
         "Apply $x_{k+1} = x_k - \\tfrac{f'(x_k)}{f''(x_k)}$.",
         {"root-of-f": "You applied Newton to $f$, not to $f'$. That hunts for a root of $f$, not for the minimum.",
          "descent": "You took a gradient step with $s = 1$. Newton divides by $f''(1) = e$ as well."})),
     ("The error after one step is about 0.0050. About how big is it after the second step?",
      choice([
          opt("ok", "$1.3 \\times 10^{-5}$", correct=True),
          opt("linear", "$2.5 \\times 10^{-3}$",
              "You halved the error, as bisection would. Newton near a minimum with $f'' > 0$ roughly squares it."),
          opt("no-half", "$2.5 \\times 10^{-5}$",
              "You squared the error but dropped the factor $\\tfrac{f'''}{2f''} = \\tfrac12$ here."),
          opt("exact", "0, since Newton is exact in one step",
              "One step is exact only on a quadratic. $e^x - 3x$ is not one.")]),
      fb("The error is multiplied by about $\\tfrac{f'''}{2f''}e_1 = \\tfrac12 \\times 0.005$, giving $1.3 \\times 10^{-5}$.",
         "Use $e_{k+1} \\approx \\tfrac{f'''}{2f''}e_k^2$."))],
    "Newton for a minimum is the root finder applied to $f'(x) = e^x - 3$. "
    "From $x_0 = 1$ it gives $x_1 = \\tfrac3e = 1.1036$, an error of 0.0050. "
    "Since $\\tfrac{f'''}{2f''} = \\tfrac12$, the next error is about $\\tfrac12 \\times 0.005^2 \\approx 1.3 \\times 10^{-5}$."))

# numerics L1 (l2): a cancellation and its cure
big = 1e8
naive = math.sqrt(big * big + 1) - big
items.append(parts(
    "e-cancel-rewrite", 3, ["nm-float"], ["cancellation"], 150, "A difference that vanishes",
    "We need $f(x) = \\sqrt{x^2 + 1} - x$ at $x = 10^8$, in doubles. "
    "There $x^2 + 1 = 10^{16} + 1$, which is not a double and rounds to $10^{16}$.",
    "Two questions on computing $f(10^8)$.",
    [("What does the formula as written return?",
      num(naive, 1e-12, [("true", 5e-9, 1e-12)], placeholder="a number", label="f(10⁸)"),
      fb("$\\sqrt{10^{16}} - 10^8 = 0$ exactly.",
         "Round $x^2 + 1$ first, then take the root and subtract.",
         {"true": "That is the true value, about $\\tfrac{1}{2x}$. In doubles the $+1$ is lost, so the formula returns 0."})),
     ("Which form returns about $5 \\times 10^{-9}$, accurate to nearly every digit?",
      choice([
          opt("ok", "$\\dfrac{1}{\\sqrt{x^2 + 1} + x}$", correct=True),
          opt("as-written", "$\\dfrac{(x^2 + 1) - x^2}{\\sqrt{x^2 + 1} + x}$, evaluated as written",
              "You kept the subtraction on top. $(x^2 + 1) - x^2$ still rounds to 0 at $x = 10^8$."),
          opt("factor", "$x\\left(\\sqrt{1 + x^{-2}} - 1\\right)$",
              "You moved the cancellation inside. $1 + 10^{-16}$ rounds to 1, so the bracket is 0."),
          opt("square", "$\\sqrt{x^2 + 1 - 2x\\sqrt{x^2 + 1} + x^2}$",
              "You squared and rooted. The terms inside still cancel almost completely.")]),
      fb("Multiplying by the conjugate removes the subtraction: $\\tfrac{1}{2 \\times 10^8} = 5 \\times 10^{-9}$.",
         "Find a form with no subtraction of nearly equal numbers."))],
    "Near $10^{16}$ doubles are 2 apart, so $10^{16} + 1$ is a tie and rounds to the even $10^{16}$. "
    "The subtraction then cancels every digit and returns 0. "
    "The conjugate form $\\tfrac{1}{\\sqrt{x^2 + 1} + x}$ adds instead, and returns $5 \\times 10^{-9}$."))

# numerics L1 (l3): the condition number of a log
kap_ln = 1 / math.log(1.02)
items.append(item(
    "e-log-condition", 3, ["nm-stability"], ["condition-number"], 120, "How sensitive a log is",
    "We evaluate $f(x) = \\ln x$ at $x = 1.02$.",
    "What is the condition number $\\kappa = \\left|\\tfrac{xf'(x)}{f(x)}\\right|$ there? Give it to 2 decimal places.",
    num(r(kap_ln, 4), 0.01, [("slope", r(1 / 1.02, 4), 0.01), ("inverse", r(math.log(1.02), 4), 0.01)], label="κ"),
    fb("$\\kappa = \\tfrac{1}{|\\ln 1.02|} = 50.50$, so we lose about 1.7 digits.",
       "With $f' = \\tfrac1x$, the product $xf'(x)$ is 1.",
       {"slope": "You gave $|f'(x)|$. The condition number compares relative changes, so it is $\\left|\\tfrac{xf'}{f}\\right|$.",
        "inverse": "You inverted it. $\\kappa = \\tfrac{1}{\\ln 1.02}$, not $\\ln 1.02$."}),
    "Here $xf'(x) = 1$, so $\\kappa = \\tfrac{1}{|\\ln 1.02|} = 50.50$. "
    "A relative error in $x$ grows about 50 times in $\\ln x$, a loss of about $\\log_{10} 50.5 \\approx 1.7$ digits. "
    "This belongs to the problem: no algorithm for $\\ln x$ near 1 avoids it."))

# numerics L1 (l3, l4): well conditioned, badly computed
items.append(item(
    "e-log1p-blame", 3, ["nm-stability", "nm-float"], ["stability-vs-conditioning"], 120, "Whose fault is the error",
    "In doubles, `math.log(1 + 3e-12)` returns $3.0000446571375978 \\times 10^{-12}$. "
    "The true value is $2.9999999999955 \\times 10^{-12}$.",
    "Which explains the relative error of about $1.5 \\times 10^{-5}$?",
    choice([
        opt("ok", "Rounding $1 + x$ is the unstable step; the problem itself has $\\kappa \\approx 1$.", correct=True),
        opt("ill", "The problem is ill conditioned near 0, so no method can do better.",
            "You blamed the problem. Its condition number is about 1 here, and `math.log1p` gets every digit."),
        opt("log", "`math.log` is inaccurate near 1.",
            "You blamed `log`. It is correct to within $u$; the damage is done when $1 + x$ is rounded."),
        opt("float32", "The value was stored in single precision.",
            "You assumed a narrower type. Python floats are doubles; the loss comes from rounding $1 + x$.")]),
    fb("A well-conditioned problem met an unstable first step; `log1p` is the stable algorithm.",
       "Separate the problem's condition number from what the formula does."),
    "$\\ln(1 + x)$ at $x = 3 \\times 10^{-12}$ has $\\kappa = \\tfrac{x}{(1 + x)\\ln(1 + x)} \\approx 1$, so the problem is well conditioned. "
    "Storing $1 + x$ keeps only about five digits of $x$, since the gap between doubles near 1 is $2^{-52}$. "
    "`math.log1p` works on $x$ itself and gets every digit."))

# numerics L2 (l7): a quadratic through three points
items.append(item(
    "e-three-point-poly", 3, ["nm-roots"], ["interpolation"], 120, "A curve through three quotes",
    "A curve is quoted at three tenors: $(0, 1)$, $(1, 3)$ and $(4, 2)$, in years and per cent.",
    "The quadratic through the three points is evaluated at 2 years. What value does it give? Give it to 2 decimal places.",
    num(r(23 / 6, 4), 0.005, [("linear", r(8 / 3, 4), 0.001), ("two-points", 5, 0.001)], label="p(2)"),
    fb("The Lagrange weights at 2 are $-\\tfrac12$, $\\tfrac43$ and $\\tfrac16$, so $p(2) = -\\tfrac12 + 4 + \\tfrac13 = \\tfrac{23}{6}$.",
       "Write $p$ in Lagrange form and put $x = 2$.",
       {"linear": "You interpolated linearly between $(1, 3)$ and $(4, 2)$. The quadratic bends through all three points.",
        "two-points": "You extended the line through $(0, 1)$ and $(1, 3)$. The quadratic uses the third point too."}),
    "The Lagrange basis at $x = 2$ gives $L_0 = \\tfrac{(2 - 1)(2 - 4)}{(0 - 1)(0 - 4)} = -\\tfrac12$, $L_1 = \\tfrac{2 \\times (-2)}{1 \\times (-3)} = \\tfrac43$ and $L_2 = \\tfrac{2 \\times 1}{4 \\times 3} = \\tfrac16$. "
    "So $p(2) = 1 \\times (-\\tfrac12) + 3 \\times \\tfrac43 + 2 \\times \\tfrac16 = \\tfrac{23}{6} \\approx 3.8333$. "
    "The weights sum to 1, as they must."))

# numerics L3 (l9): Richardson for an order-3 method with the step cut to a third
items.append(item(
    "e-richardson-three", 3, ["nm-quadrature"], ["richardson"], 150, "Extrapolating from a third of the step",
    "A method has error about $Ch^3$ for small $h$. It returns $A$ with step $h$ and $B$ with step $\\tfrac h3$.",
    "Give the combination of $A$ and $B$ that cancels the $h^3$ term.",
    expr("\\frac{27B-A}{26}", ["(27B-A)/26", "B+\\frac{B-A}{26}", "B+(B-A)/26", "\\frac{27}{26}B-\\frac{1}{26}A"],
         [("halving", "\\frac{8B-A}{7}"), ("order-two", "\\frac{9B-A}{8}"), ("order-one", "\\frac{3B-A}{2}")]),
    fb("$A \\approx I + Ch^3$ and $B \\approx I + \\tfrac{Ch^3}{27}$, so $\\tfrac{27B - A}{26} \\approx I$.",
       "Write $A$ and $B$ with their error terms, then eliminate $Ch^3$.",
       {"halving": "Those are the weights for halving $h$. A third of the step divides $h^3$ by 27.",
        "order-two": "That cancels $h^2$. Here the error falls by 27, not 9.",
        "order-one": "That cancels an $h$ term. For $h^3$ the weights are $\\tfrac{27}{26}$ and $-\\tfrac{1}{26}$."}),
    "With $A = I + Ch^3$ and $B = I + \\tfrac{Ch^3}{27}$, we get $27B - A = 26I$. "
    "So $\\tfrac{27B - A}{26}$ removes the leading error. "
    "In general, steps $h$ and $\\tfrac hr$ with an order-$p$ error give $\\tfrac{r^pB - A}{r^p - 1}$."))

# numerics L3 (l10): two-point Gauss on a quartic over [-1, 5]
a_g = 1 / math.sqrt(3)
gauss = 3 * ((3 * a_g + 2) ** 4 + (2 - 3 * a_g) ** 4)
items.append(parts(
    "e-gauss-two-point", 3, ["nm-quadrature"], ["gauss-legendre"], 150, "Two nodes on a quartic",
    "The two-point Gauss-Legendre rule on $[-1, 1]$ has nodes $\\pm\\tfrac{1}{\\sqrt3}$ and weights 1. "
    "We apply it to $\\int_{-1}^{5} x^4\\,dx = 625.2$.",
    "Two questions on the rule.",
    [("What value does the mapped rule give? Give it to 2 decimal places.",
      num(r(gauss, 4), 0.005, [("no-scale", r(gauss / 3, 4), 0.005), ("full-width", r(gauss * 2, 4), 0.005)], label="Rule"),
      fb("The nodes map to $2 \\pm \\sqrt3$ with weights 3, giving $3 \\times 194 = 582$.",
         "Map with $x = 3t + 2$ and multiply by $\\tfrac{b - a}{2} = 3$.",
         {"no-scale": "You left out the factor $\\tfrac{b - a}{2} = 3$, giving 194.",
          "full-width": "You multiplied by $b - a = 6$. The factor is $\\tfrac{b - a}{2} = 3$."})),
     ("Why is the rule not exact here?",
      choice([
          opt("ok", "Two nodes are exact up to degree $2n - 1 = 3$, and $x^4$ has degree 4.", correct=True),
          opt("two-n", "Gauss is exact up to degree $2n = 4$, so a rounding error must have crept in.",
              "You counted one degree too many. $n$ nodes are exact up to degree $2n - 1$."),
          opt("interval", "Gauss rules work only on $[-1, 1]$.",
              "You forgot the map. A linear change of variable carries the rule to any $[a, b]$, degree for degree."),
          opt("smooth", "$x^4$ is not smooth enough for Gauss.",
              "You blamed smoothness. $x^4$ is a polynomial; it is just one degree too high for two nodes.")]),
      fb("Two nodes integrate cubics exactly, and $x^4$ is one degree higher.",
         "How high a degree can $n$ nodes integrate exactly?"))],
    "The map $x = 3t + 2$ sends the nodes $t = \\pm\\tfrac{1}{\\sqrt3}$ to $2 \\pm \\sqrt3$ and multiplies by 3. "
    "The rule gives 582 against 625.2, since two nodes are exact only to degree 3. "
    "Three nodes would be exact up to degree 5, so they would give 625.2."))

# numerics L4 (l13): the explicit scheme's time step, read from a price range
sig, rr = 0.25, 0.02
M_grid = round(300 / 2.5)
dtau = 1 / (sig ** 2 * M_grid ** 2 + rr)
N_steps = 2500
m_max = max(m for m in range(1, 1000) if sig ** 2 * m ** 2 + rr <= N_steps)
items.append(parts(
    "e-explicit-step", 3, ["nm-fd"], ["explicit-stability"], 150, "The explicit scheme's time step",
    "An explicit Black-Scholes grid has $\\sigma = 0.25$ and $r = 0.02$. "
    "It is stable while $\\Delta\\tau \\le \\tfrac{1}{\\sigma^2M^2 + r}$, with $M$ space steps.",
    "Two questions on the grid.",
    [("With $S_{\\max} = 300$ and $\\Delta S = 2.5$, what is the largest stable $\\Delta\\tau$? Give it to 6 decimal places.",
      num(r(dtau, 6), 0.0000005, [("no-m", r(1 / (sig ** 2 * 300 ** 2 + rr), 6), 0.0000005),
                                  ("no-square", r(1 / (sig * M_grid ** 2 + rr), 6), 0.0000005)],
          placeholder="a decimal", label="Δτ"),
      fb("$M = 120$, so $\\sigma^2M^2 + r = 900.02$ and $\\Delta\\tau \\le 0.001111$.",
         "Find $M$ from the price range, then compute $\\sigma^2M^2 + r$.",
         {"no-m": "You used $S_{\\max}$ as $M$. The grid has $M = 300/2.5 = 120$ steps.",
          "no-square": "You used $\\sigma$ for $\\sigma^2$. With $\\sigma^2 = 0.0625$ the bound is $\\tfrac{1}{900.02}$."})),
     ("A one-year option can afford $N = 2{,}500$ time steps. What is the largest $M$ the bound allows?",
      num(m_max, 0, [("round-up", 200, 0), ("no-square", math.floor(math.sqrt((N_steps - rr) / sig)), 0),
                     ("no-root", math.floor((N_steps - rr) / sig ** 2), 0)],
          placeholder="a whole number", label="M"),
      fb("$0.0625M^2 \\le 2{,}499.98$ needs $M \\le 199.9992$, so $M = 199$.",
         "Solve $\\sigma^2M^2 + r \\le 2{,}500$ for the largest whole $M$.",
         {"round-up": "At $M = 200$, $\\sigma^2M^2 + r = 2{,}500.02$, just over 2,500.",
          "no-square": "You used $\\sigma$ for $\\sigma^2$. Solve $0.0625M^2 \\le 2{,}499.98$.",
          "no-root": "You stopped at $M^2 \\le 39{,}999.68$. Take the square root."}))],
    "With $M = 120$, $\\sigma^2M^2 + r = 900.02$, so $\\Delta\\tau \\le 0.001111$. "
    "With $N = 2{,}500$ we need $0.0625M^2 \\le 2{,}499.98$, so $M = 199$. "
    "The steps grow with $M^2$, so a finer price grid soon costs far more steps."))

# numerics L4 (l16): a control variate
vy, vx, cov = 49.0, 9.0, 17.85
b_star = cov / vx
rho_c = cov / math.sqrt(vy * vx)
factor = 1 / (1 - rho_c ** 2)
items.append(parts(
    "e-control-variate", 3, ["nm-mc"], ["control-variate"], 150, "How much a control buys",
    "A payoff $Y$ has variance 49. A control $X$ with known mean has variance 9, and $\\text{Cov}(Y, X) = 17.85$.",
    "Two questions on the control-variate estimator $\\overline{Y - b(X - E[X])}$.",
    [("What is the best coefficient $b^*$? Give it to 4 decimal places.",
      num(r(b_star, 4), 0.0005, [("by-vy", r(cov / vy, 4), 0.0005), ("by-sd", r(cov / 3, 4), 0.0005)], label="b*"),
      fb("$b^* = \\tfrac{\\text{Cov}(Y, X)}{\\text{Var}(X)} = \\tfrac{17.85}{9} = 1.9833$.",
         "Regress $Y$ on $X$: divide the covariance by $\\text{Var}(X)$.",
         {"by-vy": "You divided by $\\text{Var}(Y)$. The slope of $Y$ on $X$ divides by $\\text{Var}(X) = 9$.",
          "by-sd": "You divided by the standard deviation of $X$. Divide by its variance, 9."})),
     ("By what factor does the control cut the variance? Give it to 2 decimal places.",
      num(r(factor, 4), 0.005, [("one-minus-rho", r(1 / (1 - rho_c), 4), 0.005), ("rho", r(1 / rho_c ** 2, 4), 0.005)],
          label="Factor"),
      fb("$\\rho = \\tfrac{17.85}{7 \\times 3} = 0.85$, so the factor is $\\tfrac{1}{1 - 0.7225} = 3.60$.",
         "Find $\\rho$, then use $\\tfrac{1}{1 - \\rho^2}$.",
         {"one-minus-rho": "You used $\\tfrac{1}{1 - \\rho} = 6.67$. The variance left is $\\text{Var}(Y)(1 - \\rho^2)$.",
          "rho": "You used $\\tfrac{1}{\\rho^2}$. The variance left is $\\text{Var}(Y)(1 - \\rho^2)$, a factor $\\tfrac{1}{1 - \\rho^2}$."}))],
    "$b^* = \\tfrac{17.85}{9} = 1.9833$, and $\\rho = \\tfrac{17.85}{\\sqrt{49 \\times 9}} = 0.85$. "
    "The best control leaves $\\text{Var}(Y)(1 - \\rho^2) = 49 \\times 0.2775 = 13.60$. "
    "That is a factor of 3.60, worth about 3.6 times as many paths."))

# ================================================================ difficulty 4
# convex L3 (l10, l13): KKT for a projection, and the shadow price
pt = (4, 1)
nrm = (1, 2)
exc = pt[0] + 2 * pt[1] - 3
lam_p = 2 * exc / 5
xstar = (pt[0] - exc / 5, pt[1] - 2 * exc / 5)
val0 = exc ** 2 / 5
val1 = (exc - 0.1) ** 2 / 5
items.append(parts(
    "e-projection-kkt", 4, ["cv-duality"], ["kkt-projection"], 240, "The nearest point on a budget",
    "Minimise $(x - 4)^2 + (y - 1)^2$ subject to $x + 2y \\le 3$. "
    "The objective is convex and the limit is affine, so KKT points are exactly the optima.",
    "Three questions on the optimum and its multiplier.",
    [("What is $x^*$?",
      num(xstar[0], 0.001, [("free", 4, 0.001), ("along-x", 4 - exc, 0.001)], label="x*"),
      fb("The point moves back along $(1, 2)$ by $\\tfrac35$ of it, to $(3.4, -0.2)$.",
         "Guess the limit is active, then solve stationarity with $x + 2y = 3$.",
         {"free": "You ignored the limit. $(4, 1)$ has $x + 2y = 6 > 3$, so the limit binds.",
          "along-x": "You moved only $x$, to $(1, 1)$. The nearest point moves along the normal $(1, 2)$."})),
     ("What is the multiplier $\\lambda$?",
      num(lam_p, 0.001, [("no-two", lam_p / 2, 0.001), ("sign", -lam_p, 0.001)], label="λ"),
      fb("$2(x - 4) + \\lambda = 0$ at $x = 3.4$ gives $\\lambda = 1.2$.",
         "Read $\\lambda$ from the $x$ row of stationarity.",
         {"no-two": "You dropped the 2 from the derivative of $(x - 4)^2$. It is $2(x - 4)$, so $\\lambda = 1.2$.",
          "sign": "A multiplier on a $\\le$ limit cannot be negative. $\\lambda = 1.2 > 0$ confirms the limit binds."})),
     ("The limit is relaxed to $x + 2y \\le 3.1$. What is the new optimal value? Give it to 3 decimal places.",
      num(r(val1, 4), 0.0005, [("predicted", r(val0 - lam_p * 0.1, 4), 0.0005), ("plus", r(val0 + lam_p * 0.1, 4), 0.0005)],
          label="Value"),
      fb("The gap is now 2.9, so the value is $\\tfrac{2.9^2}{5} = 1.682$.",
         "Recompute the distance with the gap $6 - 3.1 = 2.9$.",
         {"predicted": "That is the shadow-price estimate, $1.8 - 1.2 \\times 0.1$. The curved value gives 1.682.",
          "plus": "You moved the wrong way. Relaxing a binding limit lowers a minimum, by about $\\lambda \\times 0.1$."}))],
    "Stationarity reads $2(x - 4) + \\lambda = 0$ and $2(y - 1) + 2\\lambda = 0$; with $x + 2y = 3$ this gives $(3.4, -0.2)$ and $\\lambda = 1.2$. "
    "The best value is $0.6^2 + 1.2^2 = 1.8$, and the shadow price predicts $1.8 - 0.12 = 1.68$ after relaxing. "
    "The true value 1.682 is close, since the value is curved in the limit."))

# convex L3 (l11): long-only mean-variance by KKT
s2 = (0.01, 0.04, 0.09)
mret = (0.01, 0.06, 0.10)
mu_ = (2 * s2[2] * 0.5 - 2 * s2[1] * 0.5) / (mret[2] - mret[1])
lam_ = 2 * s2[1] * 0.5 - mu_ * mret[1]
nu1 = -lam_ - mu_ * mret[0]
items.append(parts(
    "e-long-only-kkt", 4, ["cv-qp", "cv-duality"], ["long-only-kkt"], 270, "A weight held at zero",
    "Three uncorrelated assets have variances 0.01, 0.04 and 0.09 and expected returns 0.01, 0.06 and 0.10. "
    "We minimise variance with full investment, return at least 0.08 and no shorts. "
    "KKT reads $2\\sigma_i^2w_i = \\lambda + \\mu m_i + \\nu_i$, with $\\mu, \\nu_i \\ge 0$ and $\\nu_iw_i = 0$. "
    "We test $\\mathbf w = (0, 0.5, 0.5)$.",
    "Three questions on the test.",
    [("What is $\\mu$?",
      num(mu_, 0.001, [("no-two", mu_ / 2, 0.001)], label="μ"),
      fb("Subtracting the rows for assets 2 and 3 gives $0.05 = 0.04\\mu$, so $\\mu = 1.25$.",
         "Subtract the stationarity rows of the two held assets.",
         {"no-two": "You dropped the 2 in $2\\sigma_i^2w_i$. The rows read 0.04 and 0.09, so $\\mu = 1.25$."})),
     ("What is $\\nu_1$?",
      num(nu1, 0.0005, [("sign", -nu1, 0.0005)], label="ν₁"),
      fb("$\\lambda = 0.04 - 0.075 = -0.035$, so $\\nu_1 = 0.035 - 0.0125 = 0.0225$.",
         "Find $\\lambda$ from asset 2's row, then solve asset 1's row with $w_1 = 0$.",
         {"sign": "You moved $\\lambda + \\mu m_1$ across with the wrong sign. $0 = \\lambda + \\mu m_1 + \\nu_1$ gives $\\nu_1 = 0.0225$."})),
     ("What do these numbers show?",
      choice([
          opt("ok", "Every condition holds, and the problem is convex, so $(0, 0.5, 0.5)$ is the global minimum.", correct=True),
          opt("buy", "$\\nu_1 > 0$, so asset 1 should be bought.",
              "You read the sign the wrong way. $\\nu_1 > 0$ means the floor at 0 is pushing up: asset 1 would be shorted if allowed."),
          opt("lambda", "$\\lambda < 0$, so the test fails.",
              "You put a sign condition on $\\lambda$. It prices an equality, so its sign is free."),
          opt("search", "It is a candidate only; we must still try every other set of zero weights.",
              "You doubted sufficiency. For a convex problem, a point meeting every KKT condition is optimal.")]),
      fb("Feasible, $\\mu \\ge 0$, $\\nu \\ge 0$ and complementary slackness all hold, and KKT suffices for a convex problem.",
         "Check each KKT condition, then recall what KKT means for a convex problem."))],
    "Rows 2 and 3 read $0.04 = \\lambda + 0.06\\mu$ and $0.09 = \\lambda + 0.10\\mu$, so $\\mu = 1.25$ and $\\lambda = -0.035$. "
    "Row 1 with $w_1 = 0$ gives $\\nu_1 = 0.0225 \\ge 0$, and the return is exactly 0.08 with $\\mu > 0$. "
    "The problem is convex with affine limits, so this KKT point is the global minimum."))

# convex L1 (l2): the maximum of convex functions is convex, ordered
items.append(item(
    "e-local-global-proof", 4, ["cv-convex"], ["max-convex-proof"], 270, "Why the worse of two convex losses is convex",
    "A desk's loss is the worse of two convex scenario losses, $h(\\mathbf x) = \\max(f(\\mathbf x), g(\\mathbf x))$. "
    "We prove $h$ is convex.",
    "Put the proof in order. Move the two flawed lines to Left out.",
    {"kind": "order", "lines": [
        line("k1", "Take $\\mathbf x$, $\\mathbf y$, $0 \\le \\theta \\le 1$ and $\\mathbf z = \\theta\\mathbf x + (1 - \\theta)\\mathbf y$."),
        line("k2", "Convexity of $f$ and of $g$ gives $f(\\mathbf z) \\le \\theta f(\\mathbf x) + (1 - \\theta)f(\\mathbf y)$ and the same for $g$."),
        line("k3", "Since $f \\le h$ and the weights are nonnegative, the bound on $f(\\mathbf z)$ is at most $\\theta h(\\mathbf x) + (1 - \\theta)h(\\mathbf y)$."),
        line("k4", "Since $g \\le h$ and the weights are nonnegative, the bound on $g(\\mathbf z)$ is at most $\\theta h(\\mathbf x) + (1 - \\theta)h(\\mathbf y)$."),
        line("k5", "So $h(\\mathbf z) = \\max(f(\\mathbf z), g(\\mathbf z)) \\le \\theta h(\\mathbf x) + (1 - \\theta)h(\\mathbf y)$, and $h$ is convex."),
        line("e1", "$h(\\mathbf z) = \\theta h(\\mathbf x) + (1 - \\theta)h(\\mathbf y)$, since $h$ is a maximum.",
             "A maximum need not be straight along the segment. The proof needs only $\\le$."),
        line("e2", "The same argument shows $\\min(f, g)$ is convex.",
             "A minimum can fail: $\\min(x^2, (x - 2)^2)$ has a bump at 1. There is no step like $f \\le h$ for it.")],
     "answer": ["k1", "k2", "k3", "k4", "k5"], "distractors": ["e1", "e2"], "same": [["k3", "k4"]]},
    fb("Bound each function by its chord, then by the chord of $h$, and take the larger.",
       "Bound $f(\\mathbf z)$ and $g(\\mathbf z)$ separately, then take the maximum."),
    "Each of $f$ and $g$ lies on or below its chord, and each is at most $h$ at both ends. "
    "So both sit below the chord of $h$, and so does their maximum. "
    "A minimum has no such step, which is why $\\min(f, g)$ can fail."))

# numerics L1 (l4): normal equations against QR, asked as the largest kappa each solver allows
u = 2.0 ** -53
tol_t = 1e-6
k_ne = math.sqrt(tol_t / u)
k_qr = tol_t / u
items.append(parts(
    "e-normal-equations", 4, ["nm-stability"], ["normal-equations"], 210, "Squaring the condition number",
    "A least-squares fit needs coefficients with relative error below $10^{-6}$. "
    "The fit is close, so its residual is small. A stable solver's error is about $\\kappa u$, for the $\\kappa$ of the matrix it works on. "
    "Doubles have $u = 2^{-53} \\approx 1.11 \\times 10^{-16}$.",
    "Three questions on the design matrix $\\mathbf A$.",
    [("Through the normal equations, what is the largest $\\kappa(\\mathbf A)$ that meets the target?",
      num(r(k_ne, 2), 0.01, [("qr", 9.007199e9, 0.01), ("eps", r(math.sqrt(tol_t / 2.0 ** -52), 2), 0.01)],
          placeholder="for example 50000", label="κ(A)", rel=True),
      fb("$\\kappa(\\mathbf A)^2u \\le 10^{-6}$ gives $\\kappa(\\mathbf A) \\le \\sqrt{9.0 \\times 10^9} \\approx 94{,}900$.",
         "The normal equations face $\\kappa(\\mathbf A)^2$. Solve $\\kappa(\\mathbf A)^2u \\le 10^{-6}$.",
         {"qr": "That is QR's limit, $\\tfrac{10^{-6}}{u}$. The normal equations face $\\kappa(\\mathbf A)^2$, so take the square root.",
          "eps": "You used $2^{-52}$, the gap above 1. The bound uses $u = 2^{-53}$."})),
     ("Through QR, what is the largest $\\kappa(\\mathbf A)$?",
      num(9.007199e9, 0.01, [("normal", r(k_ne, 2), 0.01), ("eps", 4.5036e9, 0.01)],
          placeholder="for example 1e9", label="κ(A)", rel=True),
      fb("$\\kappa(\\mathbf A)u \\le 10^{-6}$ gives $\\kappa(\\mathbf A) \\le 9.0 \\times 10^9$.",
         "QR works on $\\mathbf A$ itself. Solve $\\kappa(\\mathbf A)u \\le 10^{-6}$.",
         {"normal": "That is the normal equations' limit. QR works on $\\mathbf A$ itself, so $\\kappa(\\mathbf A)u \\le 10^{-6}$.",
          "eps": "You used $2^{-52}$. With $u = 2^{-53}$ the limit is $9.0 \\times 10^9$."})),
     ("Which solver keeps the error near $\\kappa(\\mathbf A)u$?",
      choice([
          opt("ok", "QR, or `np.linalg.lstsq`, which work on $\\mathbf A$ itself", correct=True),
          opt("cholesky", "Cholesky on $\\mathbf A^T\\mathbf A$, since it is stable",
              "You trusted a stable step on a squared problem. Cholesky is backward stable, but $\\kappa(\\mathbf A^T\\mathbf A)$ is already squared."),
          opt("inverse", "`np.linalg.inv(A.T @ A) @ A.T @ y`",
              "You formed $\\mathbf A^T\\mathbf A$ and inverted it. That keeps the squared $\\kappa$ and adds more rounding."),
          opt("float128", "Any method, if the data are first rounded to 6 digits",
              "You rounded the data. That adds error; it does not reduce $\\kappa$.")]),
      fb("QR and `lstsq` never form $\\mathbf A^T\\mathbf A$, so they keep $\\kappa(\\mathbf A)$.",
         "Which methods avoid forming $\\mathbf A^T\\mathbf A$?"))],
    "The normal equations face $\\kappa(\\mathbf A)^2$, so they meet $10^{-6}$ only up to $\\kappa(\\mathbf A) \\approx 94{,}900$. "
    "QR faces $\\kappa(\\mathbf A)$ and copes up to $9.0 \\times 10^9$. "
    "Squaring $\\kappa$ shrinks the usable range by a factor of about 95,000."))

# numerics L2 (l8): a natural spline by hand, two inner equations
M1 = -6.0
S_half = M1 * 0.5 ** 3 / 6 + (2 - M1 / 6) * 0.5
items.append(parts(
    "e-natural-spline", 4, ["nm-roots"], ["natural-spline"], 240, "A spline through four points",
    "A natural cubic spline passes through $(0, 0)$, $(1, 2)$, $(2, 1)$ and $(3, 3)$, so $M_0 = M_3 = 0$. "
    "With unit spacing the inner equations are $\\tfrac16M_{i-1} + \\tfrac23M_i + \\tfrac16M_{i+1} = (y_{i+1} - y_i) - (y_i - y_{i-1})$ for $i = 1, 2$.",
    "Two questions on the spline.",
    [("What is $M_1$, the second derivative at $x = 1$?",
      num(M1, 0.001, [("one-equation", -4.5, 0.001), ("sign", -M1, 0.001)], label="M₁"),
      fb("Times 6, the equations read $4M_1 + M_2 = -18$ and $M_1 + 4M_2 = 18$, so $M_1 = -6$ and $M_2 = 6$.",
         "Write both inner equations and solve them together.",
         {"one-equation": "You dropped $\\tfrac16M_2$ from the first equation. $M_2 = 6$ pulls $M_1$ further down.",
          "sign": "You took the slopes in the wrong order. The right sides are $-3$ and 3."})),
     ("What is the spline's value at $x = 0.5$? Give it to 4 decimal places.",
      num(r(S_half, 5), 0.00005, [("linear", 1.0, 0.00005), ("no-correction", r(M1 * 0.5 ** 3 / 6 + 2 * 0.5, 5), 0.00005),
                                  ("three-point", r(-4.5 * 0.5 ** 3 / 6 + (2 + 4.5 / 6) * 0.5, 5), 0.00005)],
          label="S(0.5)"),
      fb("On $[0, 1]$, $S(x) = -x^3 + 3x$, so $S(0.5) = 1.375$.",
         "Use $S(x) = \\tfrac{M_1x^3}{6} + \\left(y_1 - \\tfrac{M_1}{6}\\right)x$ on $[0, 1]$, as $M_0 = 0$ and $y_0 = 0$.",
         {"linear": "You joined the points with a straight line. The spline bends, with $S'' = -6$ at the knot.",
          "no-correction": "You left out the $-\\tfrac{M_1}{6}$ in the linear term, so $S(1) \\ne 2$. The term keeps the spline through the knot.",
          "three-point": "You used $M_1 = -4.5$ from one equation alone. The second equation changes it to $-6$."}))],
    "The two inner equations give $M_1 = -6$ and $M_2 = 6$. "
    "On $[0, 1]$ the spline is $\\tfrac{M_1x^3}{6} + (y_1 - \\tfrac{M_1}{6})x = -x^3 + 3x$, which passes through $(1, 2)$. "
    "At $x = 0.5$ it is $-0.125 + 1.5 = 1.375$."))

# numerics L1 (l1, l2): a stable log-sum-exp in Python
LSE_SOLUTION = (
    "import math\n\n"
    "def log_sum_exp(xs):\n"
    "    m = max(xs)\n"
    "    if m == -math.inf:\n"
    "        return -math.inf\n"
    "    return m + math.log(sum(math.exp(x - m) for x in xs))\n")
LSE_STARTER = (
    "import math\n\n"
    "def log_sum_exp(xs):\n"
    "    \"\"\"ln(e^x1 + ... + e^xn) for a non-empty list of floats.\"\"\"\n"
    "    return math.log(sum(math.exp(x) for x in xs))\n")
LSE_TESTS = [
    ("log_sum_exp([0.0, 0.0])", repr(math.log(2))),
    ("log_sum_exp([1000.0, 1000.0])", repr(1000 + math.log(2))),
    ("log_sum_exp([-1000.0, -1000.0])", repr(-1000 + math.log(2))),
    ("log_sum_exp([3.0])", "3.0"),
    ("log_sum_exp([800.0, 0.0])", "800.0"),
    ("log_sum_exp([0.0, 1500.0])", "1500.0"),
    ("log_sum_exp([710.0, 709.0, 708.0])", repr(710 + math.log(1 + math.exp(-1) + math.exp(-2)))),
    ("log_sum_exp([-745.0, -746.0])", repr(-745 + math.log(1 + math.exp(-1)))),
    ("log_sum_exp([1.0, 2.0, 3.0])", repr(3 + math.log(1 + math.exp(-1) + math.exp(-2)))),
]
items.append(item(
    "e-log-sum-exp", 4, ["nm-float", "nm-stability"], ["log-sum-exp"], 420, "Adding exponentials without overflow",
    "A regime model scores each of $n$ states with a log-likelihood $x_i$. The total log-likelihood is $\\ln \\sum_i e^{x_i}$. "
    "Doubles overflow above about $1.8 \\times 10^{308}$, so $e^{710}$ is too big, and $e^{-746}$ rounds to 0.",
    "Write `log_sum_exp(xs)` returning $\\ln \\sum_i e^{x_i}$ for a non-empty list. "
    "It must stay accurate when every $x_i$ is near 1000 or near $-1000$.",
    {"kind": "code", "language": "python", "starter": LSE_STARTER, "solution": LSE_SOLUTION,
     "examples": [{"call": "log_sum_exp([0.0, 0.0])", "expect": repr(math.log(2)), "compare": "isclose",
                   "tol": {"rel": 1e-12}}],
     "tests": [{"call": c, "expect": e, "compare": "isclose", "tol": {"rel": 1e-12}} for c, e in LSE_TESTS],
     "how": f"Check runs {len(LSE_TESTS)} hidden tests. They hold lists near 1000 and near $-1000$, a single entry and lists that mix sizes. "
            "Each answer must match to a relative $10^{-12}$."},
    fb("Shifting by the largest $x_i$ makes every exponential at most 1 and the largest exactly 1. So nothing overflows and the sum is at least 1.",
       "Pull the largest term out: $\\ln \\sum e^{x_i} = m + \\ln \\sum e^{x_i - m}$."),
    "With $m = \\max x_i$, the identity $\\ln \\sum e^{x_i} = m + \\ln \\sum e^{x_i - m}$ is exact. "
    "Every $e^{x_i - m}$ is at most 1 and one of them is 1, so the sum lies between 1 and $n$. "
    "No step overflows, and the logarithm never sees 0."))

# ================================================================ difficulty 5
# convex L4 (l17): certifying a solver's answer
fval = 3.02 ** 2 + 3 * 0.98 ** 2
gfun = lambda lam: 4 * lam - lam ** 2 / 3
g59 = gfun(5.9)
items.append(parts(
    "e-solver-certificate", 5, ["cv-duality", "cv-descent"], ["certificate"], 360, "How good is the solver's answer",
    "Minimise $x^2 + 3y^2$ subject to $x + y \\ge 4$. The problem is convex and Slater's condition holds. "
    "A solver reports $(x, y) = (3.02, 0.98)$ with multiplier $\\lambda = 5.9$. "
    "The dual function is $g(\\lambda) = 4\\lambda - \\tfrac{\\lambda^2}{3}$ for $\\lambda \\ge 0$.",
    "Three questions on what we can certify.",
    [("What is $g(5.9)$? Give it to 4 decimal places.",
      num(r(g59, 6), 0.00005, [("primal", r(fval, 6), 0.00005), ("optimum", 12, 0.00005)], label="g(5.9)"),
      fb("$4 \\times 5.9 - \\tfrac{34.81}{3} = 23.6 - 11.6033 = 11.9967$.",
         "Put $\\lambda = 5.9$ into $g$.",
         {"primal": "You gave the objective at the reported point, 12.0016. The dual function gives the floor.",
          "optimum": "You gave the true optimum, 12. The certificate must come from the reported $\\lambda$ alone."})),
     ("What is the duality gap $f(3.02, 0.98) - g(5.9)$? Give it to 4 decimal places.",
      num(r(fval - g59, 6), 0.00005, [("zero", 0, 0.00005), ("to-optimum", r(fval - 12, 6), 0.00005)], label="Gap"),
      fb("$f = 9.1204 + 2.8812 = 12.0016$, so the gap is $12.0016 - 11.9967 = 0.0049$.",
         "Evaluate the objective at the reported point, then subtract $g(5.9)$.",
         {"zero": "You assumed a reported optimum has no gap. The values differ by 0.0049.",
          "to-optimum": "You subtracted the true optimum, which we do not know in practice. The gap uses $g(5.9)$."})),
     ("What does the gap certify?",
      choice([
          opt("ok", "The reported point is feasible and its value is within 0.0049 of the optimum.", correct=True),
          opt("point", "The reported point is within 0.0049 of the optimal point.",
              "You read a value gap as a distance. The gap bounds $f - p^*$, not how far $(x, y)$ is from $(3, 1)$."),
          opt("nothing", "Nothing, since $\\lambda = 5.9$ is not the optimal multiplier.",
              "You required the best multiplier. Weak duality makes every $\\lambda \\ge 0$ give a valid floor."),
          opt("exact", "The point is optimal, since $x + y = 4$ exactly.",
              "Feasibility is one check of five. Stationarity fails slightly: $2x = 6.04$ but $\\lambda = 5.9$.")]),
      fb("$g(5.9) \\le p^* \\le f(3.02, 0.98)$, so the value is within 0.0049 of optimal.",
         "Which two numbers sandwich $p^*$?"))],
    "The point is feasible, since $3.02 + 0.98 = 4$, so $f = 12.0016$ is a ceiling on $p^*$. "
    "Any $\\lambda \\ge 0$ gives a floor, and $g(5.9) = 11.9967$. "
    "So the reported value is within 0.0049 of optimal; the true $p^* = 12$ lies in between."))

# numerics L4 (l13, l15, l17): an error budget across methods
P2, P1 = 7.9620, 7.9680
rich = (4 * P1 - P2) / 3
err1 = rich - P1
s_pay = 15.0
n_need = (s_pay / err1) ** 2
items.append(parts(
    "e-error-budget", 5, ["nm-fd", "nm-mc"], ["error-budget"], 360, "One price, two error budgets",
    "A grid prices a put at £7.9620 with $\\Delta S = 2$ and £7.9680 with $\\Delta S = 1$. "
    "Its error is about $C\\Delta S^2$, with $\\Delta\\tau$ scaled to match.",
    "Three questions on the errors.",
    [("What is the Richardson estimate of the true price? Give it to 4 decimal places.",
      num(r(rich, 6), 0.00005, [("mean", r((P1 + P2) / 2, 6), 0.00005), ("linear", r(2 * P1 - P2, 6), 0.00005)],
          unit="£", label="Price"),
      fb("$\\tfrac{4 \\times 7.9680 - 7.9620}{3} = £7.9700$.",
         "With error $\\propto \\Delta S^2$, halving $\\Delta S$ quarters it: use $\\tfrac{4P_1 - P_2}{3}$.",
         {"mean": "You averaged the two prices. The finer one is four times as accurate, so weight it more.",
          "linear": "You extrapolated as if the error were $\\propto \\Delta S$. It is $\\propto \\Delta S^2$, so use $\\tfrac{4P_1 - P_2}{3}$."})),
     ("About how big is the error of the $\\Delta S = 1$ price, in pounds? Give its size.",
      num(r(err1, 6), 0.00005, [("difference", r(P1 - P2, 6), 0.00005), ("signed", r(P1 - rich, 6), 0.00005)], unit="£", placeholder="a decimal", label="Error"),
      fb("$7.9700 - 7.9680 = £0.0020$, a third of the change between grids.",
         "Compare the finer price with the Richardson estimate.",
         {"difference": "You gave the change between grids, £0.0060. With error $\\propto \\Delta S^2$, the finer grid's error is a third of it.",
          "signed": "That is the signed error, grid minus estimate. Its size is £0.0020."})),
     ("Monte Carlo payoffs have standard deviation £15. How many paths give a standard error equal to that grid error?",
      num(round(n_need), 1, [("no-square", round(s_pay / err1), 1), ("grid-change", round((s_pay / (P1 - P2)) ** 2), 1)],
          placeholder="a whole number", label="Paths"),
      fb("$\\left(\\tfrac{15}{0.0020}\\right)^2 = 7{,}500^2 = 56{,}250{,}000$ paths.",
         "Solve $\\tfrac{15}{\\sqrt n} = 0.0020$ for $n$.",
         {"no-square": "You stopped at $\\tfrac{15}{0.0020} = 7{,}500$. That is $\\sqrt n$; square it.",
          "grid-change": "You matched the change between grids, £0.0060. The grid error is £0.0020, which needs nine times as many paths."}))],
    "With error $C\\Delta S^2$, the two prices give $C = -0.0020$ and a limit of £7.9700. "
    "So the finer grid is out by about £0.0020. "
    "Matching that with Monte Carlo needs $(15/0.002)^2 = 56{,}250{,}000$ paths, since its error falls only like $n^{-1/2}$."))

# numerics L3 (l12): stiff decay, implicit and trapezoidal
lam_s, h_s = 200, 0.04
z = h_s * lam_s
imp = 1 / (1 + z)
trap = (1 - z / 2) / (1 + z / 2)
n_trap = math.ceil(math.log(1e8) / -math.log(abs(trap)))
n_imp = math.ceil(math.log(1e8) / -math.log(imp))
items.append(parts(
    "e-stiff-implicit", 5, ["nm-quadrature", "nm-stability"], ["stiff-factors"], 330, "Damping a fast mode",
    "Errors in a stiff model decay as $e' = -200e$. We take steps of $h = 0.04$, so $h\\lambda = 8$ with $\\lambda = 200$.",
    "Three questions on what each method does to the error per step.",
    [("What factor does implicit Euler apply each step? Give it to 4 decimal places.",
      num(r(imp, 4), 0.0005, [("explicit", 1 - z, 0.0005), ("inverse-z", r(1 / z, 4), 0.0005)], label="Factor"),
      fb("Implicit Euler gives $\\tfrac{1}{1 + h\\lambda} = \\tfrac19 = 0.1111$.",
         "Solve $e_{n+1} = e_n - h\\lambda e_{n+1}$ for $e_{n+1}$.",
         {"explicit": "That is explicit Euler's factor, $1 - h\\lambda = -7$. Implicit Euler divides instead.",
          "inverse-z": "You dropped the 1. The factor is $\\tfrac{1}{1 + h\\lambda} = \\tfrac19$."})),
     ("How many trapezoidal steps cut the fast mode by a factor of $10^8$?",
      num(n_trap, 0, [("floor", n_trap - 1, 0), ("implicit", n_imp, 0)], placeholder="a whole number", label="Steps"),
      fb("The factor is $\\tfrac{1 - 4}{1 + 4} = -0.6$, and $\\tfrac{\\ln 10^8}{\\ln(1/0.6)} = 36.06$, so 37 steps.",
         "Find the trapezoidal factor, then solve $0.6^n \\le 10^{-8}$.",
         {"floor": "After 36 steps $0.6^{36} \\approx 1.03 \\times 10^{-8}$, still above $10^{-8}$.",
          "implicit": "That is implicit Euler's count, with factor $\\tfrac19$. The trapezoidal factor is $-0.6$."})),
     ("Which statement is true for this stiff mode?",
      choice([
          opt("ok", "Both are stable, but only implicit Euler damps the fast mode quickly.", correct=True),
          opt("trap-best", "The trapezoidal rule damps it fastest, since it is second order.",
              "You equated order with damping. Its factor here is $-0.6$, against 0.11 for implicit Euler."),
          opt("explicit-ok", "Explicit Euler is fine at $h = 0.04$, since the model is smooth.",
              "You looked at the smooth solution. The fast mode sets the limit, $h < 0.01$, and the factor here is $-7$."),
          opt("unstable", "Implicit Euler is unstable for $h\\lambda > 2$.",
              "That limit is explicit Euler's. Implicit Euler's factor $\\tfrac{1}{1 + h\\lambda}$ is below 1 for every $h > 0$.")]),
      fb("Implicit Euler cuts the error ninefold a step; the trapezoidal rule flips it and keeps 60% of it.",
         "Compare the sizes and signs of the two factors."))],
    "Implicit Euler multiplies the error by $\\tfrac19$ and needs 9 steps to cut it by $10^8$. "
    "The trapezoidal factor is $-0.6$, so it needs 37, and the factor tends to $-1$ as $h\\lambda$ grows. "
    "Both are stable for every $h > 0$, but only implicit Euler kills a fast mode at once."))

order = {2: [], 3: [], 4: [], 5: []}
for it in items:
    order[it["difficulty"]].append(it)
pace = sum(i["pace"] for i in items)
exam = {
    "id": "topic-2.5", "topic": "2.5", "name": "Numerical methods and optimisation",
    "minutes": 110, "pass": 0.7,
    "skills": {"cv-convex": "Convex sets and functions", "cv-lp": "Linear programming", "cv-duality": "Duality and KKT",
               "cv-qp": "Quadratic programmes", "cv-descent": "Gradient descent and Newton",
               "nm-float": "Floating point", "nm-stability": "Conditioning and stability",
               "nm-roots": "Root finding and interpolation", "nm-quadrature": "Quadrature and ODE solvers",
               "nm-fd": "Finite differences", "nm-mc": "Monte Carlo"},
    "items": order[2] + order[3] + order[4] + order[5],
}
with open(OUT, "w", encoding="utf8") as f:
    json.dump(exam, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("wrote", os.path.normpath(OUT), len(exam["items"]), "items, pace", pace, "s", {k: len(v) for k, v in order.items()})
