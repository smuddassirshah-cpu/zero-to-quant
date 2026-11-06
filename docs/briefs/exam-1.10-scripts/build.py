"""Build app/content/exams/topic-1.10.json (topic 1.10, Analysis and proof-based linear algebra: analysis and linear-maps).

Route A for every key: the closed forms below. check_numbers.py recomputes each value by a second route and
asserts it at its path in the written file. Run from anywhere: python3 docs/briefs/exam-1.10-scripts/build.py
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-1.10.json')


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
# analysis L1 (l2): a supremum that is not a maximum
items.append(item(
    "e-sup-rising", 2, ["an-reals"], ["supremum"], 60, "A supremum from outside",
    "Let $A = \\left\\{ \\tfrac{2n + 1}{n + 4} : n \\ge 1 \\right\\}$. Its first terms are $\\tfrac35$, $\\tfrac56$, 1 and $\\tfrac98$.",
    "Which statement about $\\sup A$ is true?",
    choice([
        opt("ok", "$\\sup A = 2$, and $A$ has no largest element.", correct=True),
        opt("max", "$\\sup A = 2$, and 2 is the largest element of $A$.",
            "You treated the limit as a term. Each term is $2 - \\tfrac{7}{n + 4}$, which is below 2."),
        opt("first", "$\\sup A = \\tfrac35$, the first term.",
            "You took the first term. The terms rise, so $\\tfrac35$ is the infimum."),
        opt("none", "$A$ has no supremum, since no term reaches 2.",
            "You required the supremum to be attained. Completeness gives $\\sup A = 2$ whether or not 2 is in $A$.")]),
    fb("Every term is $2 - \\tfrac{7}{n + 4} < 2$, and the terms come within any $\\varepsilon$ of 2.",
       "Write each term as 2 minus something positive."),
    "Each term is $2 - \\tfrac{7}{n + 4}$, so 2 is an upper bound that no term reaches. "
    "For $\\varepsilon > 0$, any $n > \\tfrac{7}{\\varepsilon}$ gives a term above $2 - \\varepsilon$, so nothing smaller bounds $A$. "
    "The supremum is 2, and it is not a maximum."))

# analysis L1 (l5): the diagonal rule with 4s and 5s
diag_rows = ["5544", "4454", "4545", "5555"]
x_digits = "".join("4" if diag_rows[k][k] == "5" else "5" for k in range(4))
x_val = float("0." + x_digits)
copied = float("0." + "".join(diag_rows[k][k] for k in range(4)))
row1 = float("0." + "".join("4" if c == "5" else "5" for c in diag_rows[0]))
items.append(item(
    "e-diagonal-digits", 2, ["an-reals"], ["diagonal-argument"], 60, "A number missing from the list",
    "A list of numbers in $(0, 1)$ begins $x_1 = 0.5544\\ldots$, $x_2 = 0.4454\\ldots$, $x_3 = 0.4545\\ldots$ and $x_4 = 0.5555\\ldots$. "
    "We build $x$ by the diagonal rule. Digit $k$ of $x$ is 4 when digit $k$ of $x_k$ is 5, and 5 otherwise.",
    "What are the first four decimal places of $x$? Type them as a decimal, cut off after the fourth place.",
    num(x_val, 0.00004, [("copied", copied, 0.00004), ("row", row1, 0.00004)], placeholder="0.dddd", label="x",
        accept="0.4554, the first four places"),
    fb("The diagonal digits are 5, 4, 4, 5, so $x = 0.4554\\ldots$.",
       "Read digit $k$ of $x_k$ only, then swap it.",
       {"copied": "You copied the diagonal digits. Each must be changed, so that $x$ differs from every $x_k$.",
        "row": "You changed the digits of $x_1$. The rule reads digit $k$ of the $k$-th number."}),
    "Digit $k$ of $x_k$ gives 5, 4, 4, 5 down the diagonal, so $x$ begins $0.4554$. "
    "It differs from each $x_k$ at digit $k$, so it is not on the list. "
    "Using only 4s and 5s avoids two names for one number, such as $0.4999\\ldots = 0.5$."))

# analysis L3 (l11): telescoping with a gap of three
tel = (1 + 1 / 2 + 1 / 3) / 3
items.append(item(
    "e-telescope-gap-three", 2, ["an-series"], ["telescoping"], 75, "Terms that cancel three apart",
    "Partial fractions give $\\tfrac{1}{n(n + 3)} = \\tfrac13\\left(\\tfrac{1}{n} - \\tfrac{1}{n + 3}\\right)$.",
    "What is $\\sum_{n=1}^{\\infty} \\tfrac{1}{n(n + 3)}$? Give 4 decimal places.",
    num(r(tel), 0.00005, [("no-third", r(3 * tel), 0.00005), ("one-term", r(1 / 3), 0.00005)],
        placeholder="a decimal", label="Sum", accept="11/18 = 0.6111"),
    fb("$\\tfrac13\\left(1 + \\tfrac12 + \\tfrac13\\right) = \\tfrac{11}{18} = 0.6111$.",
       "Write out $S_n$ and see which terms survive.",
       {"no-third": "You dropped the factor $\\tfrac13$ from the partial fractions, which gives 1.8333.",
        "one-term": "You kept only $\\tfrac13 \\times 1 = 0.3333$. The shift is three places, so $\\tfrac12$ and $\\tfrac13$ survive too."}),
    "In $S_n$ each $\\tfrac{1}{k}$ cancels three places later, leaving $\\tfrac13\\left(1 + \\tfrac12 + \\tfrac13 - \\tfrac{1}{n + 1} - \\tfrac{1}{n + 2} - \\tfrac{1}{n + 3}\\right)$. "
    "As $n \\to \\infty$ the last three terms vanish. The sum is $\\tfrac{11}{18} = 0.6111$."))

# analysis L4 (l16): bisection on [0, 3]
halv = math.ceil(math.log2(3 / 0.001))
items.append(item(
    "e-halvings-width", 2, ["an-continuity"], ["bisection-count"], 60, "How many halvings",
    "A continuous $f$ has $f(0) < 0 < f(3)$, so it has a root in $[0, 3]$. Bisection halves the bracket at each step.",
    "How many halvings bring the bracket's width below 0.001?",
    num(halv, 0, [("unit-width", math.ceil(math.log2(1 / 0.001)), 0), ("floor", halv - 1, 0)],
        placeholder="a whole number", label="Halvings"),
    fb("$\\tfrac{3}{2^{12}} = 0.00073$, while $\\tfrac{3}{2^{11}} = 0.0015$.",
       "After $n$ halvings the width is $\\tfrac{3}{2^n}$.",
       {"unit-width": "You started from width 1, which needs only 10. The bracket is $[0, 3]$, so you need $2^n > 3000$.",
        "floor": "You rounded $\\log_2 3000 \\approx 11.55$ down. After 11 halvings the width is 0.0015, still too wide."}),
    "The width after $n$ halvings is $\\tfrac{3}{2^n}$, so we need $2^n > 3000$. "
    "$2^{11} = 2048$ is too small and $2^{12} = 4096$ is enough. So 12 halvings."))

# linear-maps L3 (l13): one Gram-Schmidt step
gv1, gv2 = (1, -2, 2), (3, 0, 3)
gdot = sum(x * y for x, y in zip(gv1, gv2))
gnn = sum(x * x for x in gv1)
gcoef = gdot / gnn
gf = [y - gcoef * x for x, y in zip(gv1, gv2)]
g_key = math.sqrt(sum(x * x for x in gf))
g_root = math.sqrt(sum((y - gdot / math.sqrt(gnn) * x) ** 2 for x, y in zip(gv1, gv2)))
g_nosub = math.sqrt(sum(y * y for y in gv2))
items.append(item(
    "e-gram-schmidt-step", 2, ["lx-inner"], ["gram-schmidt"], 60, "One Gram-Schmidt step",
    "In $\\mathbb{R}^3$ with the dot product, take $\\mathbf{v}_1 = (1, -2, 2)$ and $\\mathbf{v}_2 = (3, 0, 3)$.",
    "Gram-Schmidt replaces $\\mathbf{v}_2$ by $\\mathbf{f}_2 = \\mathbf{v}_2 - \\tfrac{\\langle \\mathbf{v}_2, \\mathbf{v}_1 \\rangle}{\\langle \\mathbf{v}_1, \\mathbf{v}_1 \\rangle}\\mathbf{v}_1$. "
    "What is $\\|\\mathbf{f}_2\\|$? Give 2 decimal places.",
    num(r(g_key), 0.005, [("root-norm", r(g_root), 0.005), ("no-sub", r(g_nosub), 0.005)], placeholder="a decimal",
        label="Length"),
    fb("The coefficient is $\\tfrac99 = 1$, so $\\mathbf{f}_2 = (2, 2, 1)$ and $\\|\\mathbf{f}_2\\| = 3$.",
       "Subtract the part of $\\mathbf{v}_2$ along $\\mathbf{v}_1$, then take the length.",
       {"root-norm": "You divided by $\\|\\mathbf{v}_1\\| = 3$, not by $\\langle \\mathbf{v}_1, \\mathbf{v}_1 \\rangle = 9$, and got 6.71.",
        "no-sub": "That is $\\|\\mathbf{v}_2\\| = \\sqrt{18}$. Subtract the part along $\\mathbf{v}_1$ first."}),
    "The coefficient is $\\tfrac99 = 1$, so $\\mathbf{f}_2 = (2, 2, 1)$. "
    "It is orthogonal to $\\mathbf{v}_1$, since $2 - 4 + 2 = 0$. "
    "Its length is $\\sqrt{4 + 4 + 1} = 3$."))

# linear-maps L1 (l2): a subspace of R^3
items.append(item(
    "e-subspace-r3", 2, ["lx-spaces"], ["subspace-test"], 60, "Which set is a subspace",
    "A subspace contains $\\mathbf{0}$ and is closed under addition and scalar multiplication.",
    "Which subset of $\\mathbb{R}^3$ is a subspace?",
    choice([
        opt("ok", "$\\{\\mathbf{x} : x_1 = 2x_3\\}$", correct=True),
        opt("product", "$\\{\\mathbf{x} : x_1x_2 = 0\\}$",
            "You checked $\\mathbf{0}$ and multiples. Sums fail: $(1, 0, 0) + (0, 1, 0)$ has $x_1x_2 = 1$."),
        opt("affine", "$\\{\\mathbf{x} : x_1 + x_2 = 1\\}$",
            "You saw a plane and stopped. This plane misses $\\mathbf{0}$, so it is not a subspace."),
        opt("half", "$\\{\\mathbf{x} : x_1 \\ge 0\\}$",
            "You checked sums only. Multiplying $(1, 0, 0)$ by $-1$ leaves the set.")]),
    fb("It holds $\\mathbf{0}$, and $x_1 = 2x_3$ survives sums and multiples.",
       "Test $\\mathbf{0}$, a sum and a multiple for each set."),
    "The condition $x_1 - 2x_3 = 0$ is linear, so it keeps $\\mathbf{0}$, sums and multiples. "
    "The product condition fails for sums, the shifted plane misses $\\mathbf{0}$, and the half-space fails for $-1$. "
    "One failed test is enough to rule a set out."))

# ================================================================ difficulty 3
# analysis L1 (l4): a fraction between 0.47 and 0.495
a_, b_ = 0.47, 0.495
n_den = 41          # smallest whole n above 1 / (b - a) = 40
m_num = math.floor(n_den * a_) + 1
items.append(parts(
    "e-rational-between", 3, ["an-reals"], ["density"], 120, "A fraction in a narrow gap",
    "Take $a = 0.47$ and $b = 0.495$. The density proof picks a whole $n > \\tfrac{1}{b - a}$ and $m = \\lfloor na \\rfloor + 1$. Then $a < \\tfrac{m}{n} < b$.",
    "Two questions on the fraction the proof builds.",
    [("What is the smallest $n$ the proof allows?",
      num(n_den, 0, [("at-bound", 40, 0)], placeholder="a whole number", label="n"),
      fb("$\\tfrac{1}{0.025} = 40$, and $n$ must be strictly larger, so $n = 41$.",
         "Compute $\\tfrac{1}{b - a}$ first.",
         {"at-bound": "You took $n = \\tfrac{1}{b - a} = 40$. The proof needs $n$ strictly above it, so that $nb - na > 1$."})),
     ("What is $m$?",
      num(m_num, 0, [("no-plus", m_num - 1, 0)], placeholder="a whole number", label="m"),
      fb("$41 \\times 0.47 = 19.27$, so $m = 20$ and $\\tfrac{20}{41} = 0.4878$.",
         "Compute $na$, then take the floor and add 1.",
         {"no-plus": "You took $\\lfloor na \\rfloor = 19$. Then $\\tfrac{19}{41} = 0.4634$ lies below $a$, so add 1."}))],
    "Here $b - a = 0.025$, so $n = 41$ and $na = 19.27$. "
    "Then $m = 20$, and $0.47 < \\tfrac{20}{41} = 0.4878 < 0.495$. "
    "The strict $nb - na > 1$ is what keeps $\\tfrac{m}{n}$ below $b$."))

# analysis L2 (l6): epsilon and N for a quotient
eps = 0.02
thr = 5 / (2 * eps) + 0.5
N_q = math.floor(thr) + 1
items.append(parts(
    "e-n-for-quotient", 3, ["an-sequences"], ["epsilon-n"], 150, "An N for a quotient",
    "Let $a_n = \\tfrac{4n + 3}{2n - 1}$, which tends to 2. For $n \\ge 1$, $|a_n - 2| = \\tfrac{5}{2n - 1}$.",
    "Two questions on the $N$ for a given $\\varepsilon$.",
    [("$|a_n - 2| < \\varepsilon$ exactly when $n$ is greater than what? Give it in terms of $\\varepsilon$.",
      expr("\\frac{5}{2\\varepsilon}+\\frac{1}{2}",
           ["5/(2\\varepsilon)+1/2", "(5+\\varepsilon)/(2\\varepsilon)", "(5/\\varepsilon+1)/2"],
           [("minus", "\\frac{5}{2\\varepsilon}-\\frac{1}{2}"), ("no-half", "\\frac{5}{\\varepsilon}+1")]),
      fb("$2n - 1 > \\tfrac{5}{\\varepsilon}$ gives $n > \\tfrac{5}{2\\varepsilon} + \\tfrac12$.",
         "Solve $\\tfrac{5}{2n - 1} < \\varepsilon$ for $n$.",
         {"minus": "You moved the $-1$ the wrong way. From $2n - 1 > \\tfrac{5}{\\varepsilon}$, add 1, then halve.",
          "no-half": "That bounds $2n$, not $n$. Halve it."})),
     ("What is the smallest $N$ that works for $\\varepsilon = 0.02$?",
      num(N_q, 0, [("floor", N_q - 1, 0), ("no-half", math.floor(5 / eps + 1) + 1, 0)], placeholder="a whole number",
          label="N"),
      fb("$\\tfrac{5}{0.04} + \\tfrac12 = 125.5$, so $N = 126$.",
         "Put $\\varepsilon = 0.02$ into the threshold, then take the next whole number.",
         {"floor": "You rounded 125.5 down. At $n = 125$, $\\tfrac{5}{249} \\approx 0.0201$, just outside the band.",
          "no-half": "You did not halve. $2n > 251$ gives $n > 125.5$, not $n > 251$."}))],
    "$|a_n - 2| = \\tfrac{5}{2n - 1} < \\varepsilon$ exactly when $n > \\tfrac{5}{2\\varepsilon} + \\tfrac12$. "
    "For $\\varepsilon = 0.02$ that is $n > 125.5$, so $N = 126$. "
    "Every later $n$ works too, since $\\tfrac{5}{2n - 1}$ falls."))

# analysis L2 (l8): a square-root recursion
a2 = math.sqrt(3 * 1 + 10)
a3 = math.sqrt(3 * a2 + 10)
items.append(parts(
    "e-root-recursion", 3, ["an-sequences"], ["recursive-limit"], 150, "A recursion with a square root",
    f"Let $a_1 = 1$ and $a_{{n+1}} = \\sqrt{{3a_n + 10}}$. The first terms are 1, {a2:.3f} and {a3:.3f}.",
    "Two questions on the limit of $(a_n)$.",
    [("What must the proof establish before it solves $L = \\sqrt{3L + 10}$?",
      choice([
          opt("ok", "That $(a_n)$ rises and is bounded above", correct=True),
          opt("root", "That $L = 5$ solves the limit equation",
              "You solved before knowing a limit exists. A root of $L = f(L)$ says nothing about a divergent sequence."),
          opt("steps", "That the steps $a_{n+1} - a_n$ tend to 0",
              "You relied on shrinking steps. They do not force convergence, as the harmonic sums show."),
          opt("positive", "That every term $a_n$ is positive",
              "You checked one bound only. Positivity helps choose the root but gives no limit.")]),
      fb("Monotone and bounded gives a limit $L$. Only then may we pass to the limit in the recursion.",
         "What does the monotone convergence theorem need?")),
     ("What is $\\lim a_n$?",
      num(5, 0.001, [("neg-root", -2, 0.001)], label="Limit"),
      fb("$L^2 = 3L + 10$ gives $L = 5$ or $L = -2$, and $L \\ge 1$.",
         "Square $L = \\sqrt{3L + 10}$ and solve.",
         {"neg-root": "You kept the root $-2$ of $L^2 - 3L - 10 = 0$. Every $a_n$ is at least 1, so $L \\ge 1$."}))],
    "If $a_n < 5$ then $3a_n + 10 < 25$, so $a_{n+1} < 5$. Also $a_{n+1} > a_n$ exactly when $(a_n - 5)(a_n + 2) < 0$. "
    "So the sequence rises below 5 and converges, and its limit solves $L^2 - 3L - 10 = 0$ with $L \\ge 1$, so $L = 5$."))

# analysis L3 (l12, l11): which series converge
items.append(item(
    "e-which-converge", 3, ["an-series"], ["convergence-tests"], 150, "Five series, three tests",
    "Each series runs over $n \\ge 1$.",
    "Which series converge? Select all that apply.",
    choice([
        opt("ratio", "$\\sum \\tfrac{n^3}{2^n}$", correct=True),
        opt("comp", "$\\sum \\tfrac{\\cos^2 n}{n^{3/2}}$", correct=True),
        opt("root-n", "$\\sum \\tfrac{1}{\\sqrt n}$",
            "You saw the terms tend to 0. That is not enough: this is a $p$-series with $p = \\tfrac12 \\le 1$."),
        opt("term", "$\\sum \\tfrac{2n}{5n + 1}$",
            "You saw terms that stay below $\\tfrac25$. Bounded terms are not enough: they tend to $\\tfrac25$, not 0, so it diverges."),
        opt("early", "$\\sum \\tfrac{(n + 1)!}{4^n}$",
            "You judged by the first ratios, which are at most 1. The ratio is $\\tfrac{n + 2}{4}$, which grows without bound.")],
        kind="multi"),
    fb("The ratio test settles $\\tfrac{n^3}{2^n}$, and comparison with $\\tfrac{1}{n^{3/2}}$ settles the cosine series.",
       "Try the term test first, then compare or take ratios."),
    "For $\\tfrac{n^3}{2^n}$ the ratio tends to $\\tfrac12$, and $0 \\le \\tfrac{\\cos^2 n}{n^{3/2}} \\le \\tfrac{1}{n^{3/2}}$ with $p = \\tfrac32 > 1$. "
    "The terms $\\tfrac{2n}{5n + 1}$ tend to $\\tfrac25$, and $\\sum \\tfrac{1}{\\sqrt n}$ has $p \\le 1$. "
    "The factorial series has ratio $\\tfrac{n + 2}{4} \\to \\infty$."))

# analysis L4 (l15): epsilon and delta for x^3 at 2
K = 3 ** 2 + 2 * 3 + 4
d_key = min(1, 0.38 / K)
items.append(parts(
    "e-cube-delta", 3, ["an-continuity"], ["epsilon-delta"], 150, "A delta for the cube",
    "We prove $f(x) = x^3$ continuous at 2. Factor $|x^3 - 8| = |x - 2|\\,|x^2 + 2x + 4|$ and cap $\\delta \\le 1$, so $1 < x < 3$.",
    "Two questions on the $\\delta$.",
    [("What is the least $K$ with $|x^2 + 2x + 4| < K$ for every $x$ in $(1, 3)$?",
      num(K, 0, [("at-a", 2 ** 2 + 2 * 2 + 4, 0), ("at-left", 1 + 2 + 4, 0)], placeholder="a whole number", label="K"),
      fb("The factor rises on $(1, 3)$, from 7 towards $9 + 6 + 4 = 19$.",
         "The factor increases for $x > 0$. Where is it largest?",
         {"at-a": "You evaluated at $x = 2$ and got 12. The bound must hold across $(1, 3)$, where the factor rises towards 19.",
          "at-left": "You took the left end, where the factor is 7. It rises on $(1, 3)$, so its supremum is at $x = 3$."})),
     ("With $\\delta = \\min(1, \\tfrac{\\varepsilon}{K})$, what is $\\delta$ for $\\varepsilon = 0.38$?",
      num(r(d_key), 0.00005, [("at-a", r(0.38 / 12), 0.0005), ("max", 1, 0.00005)], placeholder="a decimal",
          label="delta"),
      fb("$\\min(1, \\tfrac{0.38}{19}) = 0.02$.",
         "Divide $\\varepsilon$ by $K$, then compare with 1.",
         {"at-a": "You divided by 12, the value at $x = 2$, and got 0.0317. Divide by the bound 19.",
          "max": "You took the larger of the two. Both caps must hold, so take the smaller."}))],
    "With $\\delta \\le 1$ we have $1 < x < 3$, so $|x^2 + 2x + 4| < 19$. "
    "Then $|x^3 - 8| < 19\\delta \\le \\varepsilon$ when $\\delta = \\min(1, \\tfrac{\\varepsilon}{19})$. "
    "For $\\varepsilon = 0.38$ that is 0.02."))

# analysis L4 (l18): the mean value theorem on x^4 + x
c_mvt = 2 ** (1 / 3)
items.append(parts(
    "e-mvt-quartic", 3, ["an-calculus"], ["mean-value"], 150, "The mean value theorem at work",
    "Let $f(x) = x^4 + x$ on $[0, 2]$. It is differentiable, with $f'(x) = 4x^3 + 1$.",
    "Two questions from the mean value theorem.",
    [("Find the $c \\in (0, 2)$ with $f'(c) = \\tfrac{f(2) - f(0)}{2}$. Give 4 decimal places.",
      num(r(c_mvt), 0.00005, [("mid", 1, 0.00005), ("no-root", 2, 0.00005)], placeholder="a decimal", label="c",
          accept="cube root of 2 = 1.2599"),
      fb("The mean slope is $\\tfrac{18}{2} = 9$, so $4c^3 = 8$ and $c = \\sqrt[3]{2} = 1.2599$.",
         "Compute the mean slope, then solve $4c^3 + 1$ equal to it.",
         {"mid": "You took the midpoint of the interval. Solve $4c^3 + 1 = 9$ instead.",
          "no-root": "That is $c^3 = 2$. Take the cube root."})),
     ("The theorem gives $|f(x) - f(y)| \\le M|x - y|$ on $[0, 2]$ with $M = \\sup |f'|$. What is that $M$?",
      num(4 * 2 ** 3 + 1, 0, [("mean-slope", 9, 0), ("no-plus", 32, 0)], placeholder="a whole number", label="M"),
      fb("$f'$ rises on $[0, 2]$ to $f'(2) = 33$.",
         "Where is $4x^3 + 1$ largest on $[0, 2]$?",
         {"mean-slope": "You used the mean slope, 9. The bound needs the largest $|f'|$ on the interval.",
          "no-plus": "You dropped the $+1$ in $f'$. $f'(2) = 32 + 1$."}))],
    "The mean slope is $\\tfrac{18 - 0}{2} = 9$, and $4c^3 + 1 = 9$ gives $c = \\sqrt[3]{2} = 1.2599$. "
    "For $x \\ne y$ in $[0, 2]$ the theorem gives $f(x) - f(y) = f'(\\xi)(x - y)$ with $\\xi$ between them. "
    "So $M = \\sup |f'| = 33$ works."))

# analysis L5 (l20): upper and lower sums of x^3 on [0, 2]
U4 = 0.5 * sum((k * 0.5) ** 3 for k in range(1, 5))
L4 = 0.5 * sum((k * 0.5) ** 3 for k in range(0, 4))
M4 = 0.5 * sum(((k + 0.5) * 0.5) ** 3 for k in range(0, 4))
items.append(parts(
    "e-upper-sum-square", 3, ["an-calculus"], ["upper-lower-sums"], 150, "Upper and lower sums",
    "Split $[0, 2]$ into $n$ equal pieces and let $f(x) = x^3$. On each piece $f$ rises, so its supremum is at the right end.",
    "Two questions on the upper and lower sums.",
    [("What is $U(f, P)$ for $n = 4$? Give 2 decimal places.",
      num(U4, 0.005, [("lower", L4, 0.005), ("mid", M4, 0.005)], placeholder="a decimal", label="U"),
      fb("$0.5(0.125 + 1 + 3.375 + 8) = 6.25$.",
         "Multiply the width 0.5 by the sum of $f$ at the right ends.",
         {"lower": "You used left ends. That is the lower sum $L$; $U$ takes the supremum on each piece.",
          "mid": "You used midpoints. That is a Riemann sum, not the upper sum."})),
     ("$U - L$ telescopes to $\\big(f(2) - f(0)\\big)\\tfrac{2}{n}$. What is the smallest $n$ with $U - L < 0.01$?",
      num(1601, 0, [("at-bound", 1600, 0), ("no-width", 801, 0)], placeholder="a whole number", label="n"),
      fb("$\\tfrac{16}{n} < 0.01$ needs $n > 1600$, so $n = 1601$.",
         "Simplify $U - L$ to a constant over $n$.",
         {"at-bound": "At $n = 1600$, $U - L = 0.01$ exactly. The gap must be strictly below.",
          "no-width": "You used width $\\tfrac1n$. The pieces have width $\\tfrac2n$, so $U - L = \\tfrac{16}{n}$."}))],
    "With width $\\tfrac12$, $U = \\tfrac12(0.125 + 1 + 3.375 + 8) = 6.25$ and $L = 2.25$. "
    "In general the terms telescope, so $U - L = \\tfrac{16}{n}$. That is below 0.01 from $n = 1601$."))

# analysis L5 (l21): FTC with both limits moving
ftc = 3 * 2 ** 2 / (1 + 2 ** 6) - 1 / (1 + 2 ** 2)
items.append(item(
    "e-ftc-both-limits", 3, ["an-calculus"], ["ftc-chain"], 120, "Both limits move",
    "Let $F(x) = \\int_x^{x^3} \\tfrac{dt}{1 + t^2}$ for $x > 0$.",
    "What is $F'(2)$? Give 4 decimal places.",
    num(r(ftc), 0.00005, [("no-chain", r(1 / 65 - 1 / 5), 0.00005), ("upper-only", r(12 / 65), 0.00005)],
        placeholder="a decimal", label="F'(2)", accept="12/65 - 1/5 = -1/65 = -0.0154"),
    fb("$\\tfrac{12}{65} - \\tfrac15 = -\\tfrac{1}{65} = -0.0154$.",
       "Split at a fixed point and apply the fundamental theorem to each piece.",
       {"no-chain": "You left out the chain rule and got $-0.1846$. The upper limit $x^3$ brings a factor $3x^2$.",
        "upper-only": "You dropped the lower limit and got 0.1846. It moves too, and contributes $-\\tfrac{1}{1 + x^2}$."}),
    "Write $F(x) = G(x^3) - G(x)$ with $G(u) = \\int_0^u \\tfrac{dt}{1 + t^2}$, so $G'(u) = \\tfrac{1}{1 + u^2}$ by part one. "
    "Then $F'(x) = \\tfrac{3x^2}{1 + x^6} - \\tfrac{1}{1 + x^2}$. "
    "At 2 that is $\\tfrac{12}{65} - \\tfrac15 = -\\tfrac{1}{65} = -0.0154$."))

# analysis L5 (l23): closed sets
items.append(item(
    "e-closed-sets", 3, ["an-metric"], ["closed-sets"], 150, "Which sets keep their limits",
    "A set is closed when it keeps the limit of every convergent sequence of its points.",
    "Which subsets of $\\mathbb{R}$ are closed? Select all that apply.",
    choice([
        opt("z", "$\\mathbb{Z}$", correct=True),
        opt("powers", "$\\{2^{-n} : n \\ge 0\\} \\cup \\{0\\}$", correct=True),
        opt("meet", "$\\bigcap_{n \\ge 1} \\left(-\\tfrac1n, 1 + \\tfrac1n\\right)$", correct=True),
        opt("half", "$(0, 1]$", "You checked the end 1. The points $\\tfrac1n$ tend to 0, which is missing."),
        opt("union", "$\\bigcup_{n \\ge 1} \\left[\\tfrac1n, 1\\right]$",
            "You assumed unions of closed sets are closed. This one is $(0, 1]$, which misses 0."),
        opt("rat", "$\\mathbb{Q} \\cap [0, 1]$",
            "You saw the closed interval. Rationals can tend to $\\tfrac{\\sqrt2}{2}$, which is missing.")],
        kind="multi"),
    fb("$\\mathbb{Z}$ keeps its limits, the powers keep 0, and the intersection is $[0, 1]$.",
       "For each set, look for a sequence whose limit escapes."),
    "A convergent sequence of integers is eventually constant, and $2^{-n} \\to 0$ with 0 kept. "
    "The intersection of the open intervals is $[0, 1]$, which is closed. "
    "The other three each miss a limit: 0, 0 and an irrational."))

# linear-maps L1 (l4): coordinates in a new basis
items.append(item(
    "e-coords-new-basis", 3, ["lx-spaces"], ["coordinates"], 120, "Coordinates in a new basis",
    "In $\\mathcal{P}_2(\\mathbb{R})$ take the basis $\\mathcal{B} = (1 + x,\\ x + x^2,\\ x^2)$.",
    "What is $[3 + 2x + 5x^2]_{\\mathcal{B}}$?",
    expr("(3, -1, 6)", ["(3,-1,6)", "[3, -1, 6]"], [("std", "(3, 2, 5)"), ("rev", "(6, -1, 3)")]),
    fb("$3(1 + x) - (x + x^2) + 6x^2 = 3 + 2x + 5x^2$.",
       "Match the constant, then the $x$, then the $x^2$ coefficient.",
       {"std": "Those are the coordinates in $(1, x, x^2)$. Solve for the weights on $\\mathcal{B}$.",
        "rev": "You listed the weights backwards. The first entry goes with $1 + x$.",
        "length": "Give three weights, one for each basis vector."}),
    "Write $a(1 + x) + b(x + x^2) + cx^2$ and match coefficients. "
    "The constant gives $a = 3$, then $a + b = 2$ gives $b = -1$, then $b + c = 5$ gives $c = 6$. "
    "The weights are unique because $\\mathcal{B}$ is a basis."))

# linear-maps L2 (l7): rank-nullity for A - A^T
items.append(parts(
    "e-antisym-map", 3, ["lx-maps"], ["rank-nullity-count"], 150, "Rank-nullity on matrices",
    "Let $V$ be the space of real $4 \\times 4$ matrices, of dimension 16. Define $T\\mathbf{A} = \\mathbf{A} - \\mathbf{A}^T$.",
    "Two questions on rank-nullity for $T$.",
    [("What is $\\dim \\ker T$?",
      num(4 * 5 // 2, 0, [("skew", 4 * 3 // 2, 0), ("diag", 4, 0)], placeholder="a whole number", label="Dimension"),
      fb("The kernel is the symmetric matrices: 4 diagonal entries and 6 above the diagonal.",
         "Solve $\\mathbf{A} - \\mathbf{A}^T = \\mathbf{0}$ and count the free entries.",
         {"skew": "That counts the antisymmetric matrices, which form the image. The kernel is where $\\mathbf{A} = \\mathbf{A}^T$.",
          "diag": "You counted the 4 diagonal entries only. Every symmetric matrix is in the kernel, and those need 10 numbers."})),
     ("What is $\\dim \\operatorname{im} T$?",
      num(16 - 10, 0, [("full", 16, 0)], placeholder="a whole number", label="Dimension"),
      fb("$16 - 10 = 6$, the antisymmetric matrices.",
         "Use rank-nullity with the kernel you found.",
         {"full": "You assumed $T$ is onto. Rank-nullity leaves $16 - 10$."}))],
    "$T\\mathbf{A} = \\mathbf{0}$ exactly when $\\mathbf{A}$ is symmetric, a space of dimension $4 + 6 = 10$. "
    "Rank-nullity gives $\\dim \\operatorname{im} T = 16 - 10 = 6$. "
    "That matches the antisymmetric matrices, fixed by their 6 entries above the diagonal."))

# linear-maps L2 (l8): the matrix of a map on P_2
items.append(item(
    "e-matrix-of-map", 3, ["lx-maps"], ["matrix-of-map"], 120, "A map written as a matrix",
    "Define $T : \\mathcal{P}_2(\\mathbb{R}) \\to \\mathcal{P}_2(\\mathbb{R})$ by $Tp = p' + p(0)\\,x^2$. Use the basis $(1, x, x^2)$ for inputs and outputs.",
    "What is the matrix of $T$?",
    expr("\\begin{pmatrix}0&1&0\\\\0&0&2\\\\1&0&0\\end{pmatrix}", ["[[0, 1, 0], [0, 0, 2], [1, 0, 0]]"],
         [("rows", "\\begin{pmatrix}0&0&1\\\\1&0&0\\\\0&2&0\\end{pmatrix}"),
          ("no-eval", "\\begin{pmatrix}0&1&0\\\\0&0&2\\\\0&0&0\\end{pmatrix}")]),
    fb("$T1 = x^2$, $Tx = 1$ and $Tx^2 = 2x$ give the three columns.",
       "Apply $T$ to each basis vector and write the result in coordinates.",
       {"rows": "You wrote each image as a row. Column $k$ holds the coordinates of $T$ applied to basis vector $k$.",
        "no-eval": "You left out $p(0)\\,x^2$. The constant 1 has $p(0) = 1$, so $T1 = x^2$."}),
    "$T1 = 0 + x^2$, $Tx = 1 + 0$ and $Tx^2 = 2x + 0$. "
    "Their coordinates $(0, 0, 1)$, $(1, 0, 0)$ and $(0, 2, 0)$ are the columns. "
    "Columns, not rows, so that $[T][p] = [Tp]$."))

# linear-maps L3 (l10): a dual basis and a dual map
items.append(parts(
    "e-dual-basis-pair", 3, ["lx-dual"], ["dual-basis"], 150, "A dual basis and a dual map",
    "In $\\mathbb{R}^2$ take the basis $\\mathbf{v}_1 = (2, 1)$, $\\mathbf{v}_2 = (3, 2)$. Its dual basis has $\\varphi_j(\\mathbf{v}_k) = 1$ when $j = k$ and 0 otherwise.",
    "Two questions on the dual basis.",
    [("Find $\\varphi_1(x, y)$.",
      expr("2x-3y", ["2x - 3y"], [("col", "2x-y"), ("self", "2x+y")]),
      fb("$\\varphi_1(2, 1) = 1$ and $\\varphi_1(3, 2) = 0$.",
         "Solve $\\varphi_1(\\mathbf{v}_1) = 1$ and $\\varphi_1(\\mathbf{v}_2) = 0$ for the two weights.",
         {"col": "You read a column of $\\mathbf{B}^{-1}$. The dual basis is its rows.",
          "self": "You used $\\mathbf{v}_1$ as the weights. Then $\\varphi_1(\\mathbf{v}_1) = 5$, not 1."})),
     ("Let $T(x, y) = (x + y,\\ 2x - y)$. Find $(T'\\varphi_1)(x, y)$.",
      expr("-4x+5y", ["5y-4x", "-4x + 5y"], [("unapplied", "2x-3y"), ("transpose", "-x+7y")]),
      fb("$2(x + y) - 3(2x - y) = -4x + 5y$.",
         "Substitute $T(x, y)$ into $\\varphi_1$.",
         {"unapplied": "You returned $\\varphi_1$. The dual map composes: $T'\\varphi_1 = \\varphi_1 \\circ T$.",
          "transpose": "You applied the transpose of $T$ to $(x, y)$. Apply $T$ itself, then $\\varphi_1$."}))],
    "The rows of $\\mathbf{B}^{-1} = \\begin{pmatrix}2&-3\\\\-1&2\\end{pmatrix}$ are the dual basis, so $\\varphi_1(x, y) = 2x - 3y$. "
    "Then $T'\\varphi_1 = \\varphi_1 \\circ T$ gives $2(x + y) - 3(2x - y) = -4x + 5y$. "
    "In the dual bases the matrix of $T'$ is the transpose of the matrix of $T$."))

# linear-maps L4 (l16): self-adjoint for a weighted inner product
items.append(item(
    "e-weighted-adjoint", 3, ["lx-spectral", "lx-inner"], ["self-adjoint"], 150, "Self-adjoint for which inner product",
    "On $\\mathbb{R}^2$ use $\\langle \\mathbf{x}, \\mathbf{y} \\rangle = 3x_1y_1 + x_2y_2$, which is $\\mathbf{x}^T\\mathbf{W}\\mathbf{y}$ with $\\mathbf{W} = \\operatorname{diag}(3, 1)$.",
    "Which matrix gives an operator that is self-adjoint for this inner product?",
    choice([
        opt("ok", "$\\begin{pmatrix}1&1\\\\3&2\\end{pmatrix}$", correct=True),
        opt("sym", "$\\begin{pmatrix}1&3\\\\3&2\\end{pmatrix}$",
            "You chose the symmetric matrix. That is the test for the dot product; here $\\mathbf{W}\\mathbf{T}$ must be symmetric."),
        opt("tw", "$\\begin{pmatrix}1&3\\\\1&2\\end{pmatrix}$",
            "You made $\\mathbf{T}\\mathbf{W}$ symmetric. The condition is $\\mathbf{T}^T\\mathbf{W} = \\mathbf{W}\\mathbf{T}$, so $\\mathbf{W}\\mathbf{T}$ must be."),
        opt("real", "$\\begin{pmatrix}2&1\\\\0&5\\end{pmatrix}$",
            "You relied on its real eigenvalues, 2 and 5. Real eigenvalues alone do not make an operator self-adjoint.")]),
    fb("$\\mathbf{W}\\mathbf{T} = \\begin{pmatrix}3&3\\\\3&2\\end{pmatrix}$ is symmetric.",
       "Write $\\langle \\mathbf{T}\\mathbf{x}, \\mathbf{y} \\rangle = \\langle \\mathbf{x}, \\mathbf{T}\\mathbf{y} \\rangle$ with $\\mathbf{W}$ and compare."),
    "Self-adjoint means $\\mathbf{x}^T\\mathbf{T}^T\\mathbf{W}\\mathbf{y} = \\mathbf{x}^T\\mathbf{W}\\mathbf{T}\\mathbf{y}$ for all $\\mathbf{x}, \\mathbf{y}$. "
    "So $\\mathbf{W}\\mathbf{T}$ must be symmetric, and only $\\begin{pmatrix}1&1\\\\3&2\\end{pmatrix}$ gives that. "
    "The adjoint depends on the inner product, not on the matrix alone."))

# linear-maps L4 (l19): Jordan blocks from kernel dimensions
items.append(item(
    "e-jordan-from-kernels", 3, ["lx-jordan"], ["jordan-blocks"], 120, "Blocks from kernel dimensions",
    "An operator $T$ on $\\mathbb{C}^5$ has the single eigenvalue $-1$. The dimensions of $\\ker(T + I)^k$ for $k = 1, 2, 3, 4$ are 2, 4, 5 and 5.",
    "What are its Jordan blocks?",
    choice([
        opt("ok", "One block of size 3 and one of size 2", correct=True),
        opt("diffs", "Blocks of sizes 2, 2 and 1",
            "You read the jumps 2, 2, 1 as sizes. They count the blocks of size at least 1, 2 and 3."),
        opt("one", "One block of size 5",
            "You used the algebraic multiplicity alone. $\\dim \\ker(T + I) = 2$ says there are two blocks."),
        opt("four", "One block of size 4 and one of size 1",
            "You read $\\dim \\ker(T + I)^2 = 4$ as a block size. Two blocks have size at least 2, so neither has size 1.")]),
    fb("Two blocks have size at least 2, and one has size at least 3.",
       "The jump $d_k - d_{k-1}$ counts the blocks of size at least $k$."),
    "The jumps are $2 - 0 = 2$, $4 - 2 = 2$ and $5 - 4 = 1$. "
    "So two blocks have size at least 2, and one has size at least 3. The sizes are 3 and 2, totalling 5."))

# ================================================================ difficulty 4
# analysis L4 (l19): a moving peak that shrinks
items.append(parts(
    "e-uniform-peak", 4, ["an-continuity"], ["uniform-convergence"], 210, "A peak that shrinks",
    "Let $f_n(x) = \\tfrac{x}{1 + nx^2}$ on $[0, \\infty)$. Each $f_n(x) \\to 0$, and $f_n'(x) = 0$ at $x = \\tfrac{1}{\\sqrt n}$.",
    "Two questions on whether the convergence is uniform.",
    [("What is $\\sup_{x \\ge 0} f_n(x)$? Give it in terms of $n$.",
      expr("\\frac{1}{2\\sqrt{n}}", ["1/(2\\sqrt{n})", "\\frac{\\sqrt{n}}{2n}"],
           [("one", "\\frac{1}{1+n}"), ("no-half", "\\frac{1}{\\sqrt{n}}")]),
      fb("$f_n(\\tfrac{1}{\\sqrt n}) = \\tfrac{1/\\sqrt n}{2} = \\tfrac{1}{2\\sqrt n}$.",
         "Evaluate $f_n$ at its critical point.",
         {"one": "You evaluated at $x = 1$. The peak is at $x = \\tfrac{1}{\\sqrt n}$.",
          "no-half": "You dropped the denominator. At the peak $1 + nx^2 = 2$."})),
     ("What is the smallest $n$ with $\\sup f_n < 0.01$?",
      num(2501, 0, [("at-bound", 2500, 0), ("no-square", 51, 0)], placeholder="a whole number", label="n"),
      fb("$\\tfrac{1}{2\\sqrt n} < 0.01$ needs $\\sqrt n > 50$, so $n = 2501$.",
         "Solve $\\tfrac{1}{2\\sqrt n} < 0.01$ for $n$.",
         {"at-bound": "At $n = 2500$ the supremum is exactly 0.01. It must be strictly below.",
          "no-square": "You stopped at $\\sqrt n > 50$, giving 51. Square it: $n > 2500$."}))],
    "The peak is $f_n(\\tfrac{1}{\\sqrt n}) = \\tfrac{1}{2\\sqrt n}$, and it tends to 0. "
    "One $n$ then serves every $x$, so the convergence is uniform. "
    "The supremum falls below 0.01 from $n = 2501$."))

# analysis L5 (l24): compact sets are bounded, in any metric space
items.append(item(
    "e-compact-bounded", 4, ["an-metric"], ["compactness-proof"], 210, "Compact sets are bounded",
    "Let $(X, d)$ be a metric space and $K \\subseteq X$ compact: every sequence in $K$ has a subsequence converging in $K$. We prove $K$ is bounded.",
    "Put the proof in order. Move the two flawed lines to Left out.",
    {"kind": "order", "lines": [
        line("c1", "Suppose $K$ is not bounded, and fix a point $p \\in X$."),
        line("c2", "No ball $B(p, n)$ contains $K$, so for each $n$ pick $x_n \\in K$ with $d(x_n, p) \\ge n$."),
        line("c3", "By compactness, a subsequence $x_{n_k}$ converges to some $x \\in K$."),
        line("c4", "By the triangle inequality, $d(x_{n_k}, p) \\le d(x_{n_k}, x) + d(x, p)$, which is bounded in $k$."),
        line("c5", "But $d(x_{n_k}, p) \\ge n_k \\ge k$ for every $k$. This contradiction shows $K$ is bounded."),
        line("d1", "Every sequence in $K$ converges, so $(x_n)$ is bounded.",
             "Compactness gives a convergent subsequence, not convergence of the whole sequence."),
        line("d2", "Since $d(x_n, p) \\ge n$, no subsequence can converge, because $(x_n)$ diverges.",
             "A divergent sequence can have a convergent subsequence. Here the triangle inequality is what rules one out.")],
     "answer": ["c1", "c2", "c3", "c4", "c5"], "distractors": ["d1", "d2"]},
    fb("Unboundedness builds a sequence that runs off, and compactness then gives a subsequence that cannot.",
       "Assume the opposite, build a sequence that escapes, then apply compactness."),
    "Assuming $K$ unbounded gives points $x_n$ with $d(x_n, p) \\ge n$. "
    "Compactness gives a subsequence converging to $x \\in K$, and the triangle inequality bounds its distances from $p$. "
    "That clashes with $d(x_{n_k}, p) \\ge k$, so $K$ is bounded."))

# linear-maps L2 (l6, l7) with L1 (l2): an idempotent splits the space
items.append(item(
    "e-idempotent-split", 4, ["lx-maps", "lx-spaces"], ["projection-proof"], 210, "A projection splits the space",
    "Let $T \\in \\mathcal{L}(V)$ with $T^2 = T$. We prove $V = \\ker T \\oplus \\operatorname{im} T$.",
    "Put the proof in order. Move the two flawed lines to Left out.",
    {"kind": "order", "lines": [
        line("s1", "Take $\\mathbf{v} \\in V$ and write $\\mathbf{v} = (\\mathbf{v} - T\\mathbf{v}) + T\\mathbf{v}$."),
        line("s2", "$T(\\mathbf{v} - T\\mathbf{v}) = T\\mathbf{v} - T^2\\mathbf{v} = \\mathbf{0}$, so $\\mathbf{v} - T\\mathbf{v} \\in \\ker T$."),
        line("s3", "$T\\mathbf{v} \\in \\operatorname{im} T$, so $V = \\ker T + \\operatorname{im} T$."),
        line("s4", "Now let $\\mathbf{w} \\in \\ker T \\cap \\operatorname{im} T$, say $\\mathbf{w} = T\\mathbf{u}$."),
        line("s5", "Then $\\mathbf{w} = T\\mathbf{u} = T^2\\mathbf{u} = T\\mathbf{w} = \\mathbf{0}$, since $\\mathbf{w} \\in \\ker T$."),
        line("s6", "So $\\ker T \\cap \\operatorname{im} T = \\{\\mathbf{0}\\}$, and the sum is direct."),
        line("d1", "Rank-nullity gives $\\dim \\ker T + \\dim \\operatorname{im} T = \\dim V$, and that alone makes the sum direct.",
             "Dimensions can add up with an overlap. For $N(x, y) = (y, 0)$ the kernel and the image are the same line."),
        line("d2", "$T^2 = T$ gives $T(T - I) = 0$, so $T = 0$ or $T = I$.",
             "Operators can multiply to 0 with neither factor 0. A projection onto a line is neither.")],
     "answer": ["s1", "s2", "s3", "s4", "s5", "s6"], "distractors": ["d1", "d2"]},
    fb("The split $\\mathbf{v} = (\\mathbf{v} - T\\mathbf{v}) + T\\mathbf{v}$ gives the sum, and $T^2 = T$ kills the overlap.",
       "First show that every vector splits, then show the overlap is $\\{\\mathbf{0}\\}$."),
    "Every $\\mathbf{v}$ is $(\\mathbf{v} - T\\mathbf{v}) + T\\mathbf{v}$, a kernel vector plus an image vector. "
    "A vector $T\\mathbf{u}$ in the kernel has $T\\mathbf{u} = T^2\\mathbf{u} = \\mathbf{0}$, so the overlap is $\\{\\mathbf{0}\\}$. "
    "Rank-nullity alone cannot give this, since a nilpotent map's kernel and image can overlap."))

# linear-maps L3 (l11, l14): a least-squares hedge as a projection
vr, vm, cv = 0.0010, 0.0005, 0.0004
beta = cv / vm
res_sd = math.sqrt(vr - beta ** 2 * vm)
items.append(parts(
    "e-hedge-residual", 4, ["lx-inner"], ["projection-hedge"], 210, "A hedge as a projection",
    "Zero-mean monthly returns form an inner product space with $\\langle X, Y \\rangle = \\mathrm{Cov}(X, Y)$. "
    "A stock $R$ has $\\mathrm{Var}(R) = 0.0010$ and the market $M$ has $\\mathrm{Var}(M) = 0.0005$. Their covariance is 0.0004.",
    "Two questions on the least-squares hedge, the projection of $R$ onto the span of $M$.",
    [("How many units of $M$ does the projection hold?",
      num(r(beta), 0.0005, [("reverse", r(cv / vr), 0.0005), ("corr", r(cv / math.sqrt(vr * vm)), 0.0005)],
          placeholder="a decimal", label="Units of M"),
      fb("$\\tfrac{0.0004}{0.0005} = 0.8$.",
         "The projection onto one vector is $\\tfrac{\\langle R, M \\rangle}{\\langle M, M \\rangle}M$.",
         {"reverse": "You divided by $\\mathrm{Var}(R)$ and got 0.4. Projecting onto $M$ divides by $\\langle M, M \\rangle$.",
          "corr": "That is the correlation, 0.566. The coefficient is $\\tfrac{\\langle R, M \\rangle}{\\langle M, M \\rangle}$."})),
     ("What is the standard deviation of the hedged residual $R - 0.8M$, in %? Give 2 decimal places.",
      num(r(res_sd), 0.00005, [("sub-cov", r(math.sqrt(vr - cv)), 0.00005),
                                ("sub-sd", r(math.sqrt(vr) - beta * math.sqrt(vm)), 0.00005)],
          unit="%", label="Residual sd", accept="sqrt(0.00068) = 2.61%"),
      fb("$0.0010 - 0.8^2 \\times 0.0005 = 0.00068$, and $\\sqrt{0.00068} = 2.61\\%$.",
         "The residual is orthogonal to $M$, so variances split by Pythagoras.",
         {"sub-cov": "You subtracted the covariance and got 2.45%. Pythagoras takes away the projection's squared norm, $0.8^2 \\times 0.0005$.",
          "sub-sd": "You subtracted standard deviations and got 1.37%. Norms do not subtract; squared norms do, by Pythagoras."}))],
    "The projection is $0.8M$, since $\\tfrac{0.0004}{0.0005} = 0.8$. "
    "The residual is orthogonal to $M$, so $\\mathrm{Var}(R) = 0.8^2 \\times 0.0005 + \\mathrm{Var}(R - 0.8M)$. "
    "That leaves 0.00068, a standard deviation of 2.61%."))

# linear-maps L4 (l17): a power through the spectral theorem
l1_, l2_ = 8, 3
entry6 = round(0.4 * (l1_ ** 6 - l2_ ** 6))
items.append(parts(
    "e-symmetric-power", 4, ["lx-spectral"], ["spectral-power"], 240, "A sixth power without multiplying",
    "Let $\\mathbf{A} = \\begin{pmatrix}7&2\\\\2&4\\end{pmatrix}$. Its unit eigenvectors are $\\mathbf{q}_1 = \\tfrac{1}{\\sqrt5}(2, 1)$ and $\\mathbf{q}_2 = \\tfrac{1}{\\sqrt5}(1, -2)$.",
    "Two questions using $\\mathbf{A} = \\mathbf{Q}\\boldsymbol{\\Lambda}\\mathbf{Q}^T$.",
    [("What is the largest eigenvalue of $\\mathbf{A}$?",
      num(l1_, 0, [("trace", 11, 0), ("entry", 7, 0)], placeholder="a whole number", label="Eigenvalue"),
      fb("$\\mathbf{A}(2, 1) = (16, 8) = 8(2, 1)$.",
         "Apply $\\mathbf{A}$ to each eigenvector.",
         {"trace": "That is the trace, 11, the sum of both eigenvalues. Apply $\\mathbf{A}$ to $(2, 1)$.",
          "entry": "You took the largest entry, 7. Apply $\\mathbf{A}$ to $(2, 1)$: it gives $(16, 8)$."})),
     ("What is the top-right entry of $\\mathbf{A}^6$?",
      num(entry6, 0, [("no-small", r(0.4 * l1_ ** 6), 0.05), ("entrywise", 2 ** 6, 0), ("plus", r(0.4 * (l1_ ** 6 + l2_ ** 6)), 0.05)],
          placeholder="a whole number", label="Entry"),
      fb("$\\tfrac25(8^6 - 3^6) = \\tfrac25 \\times 261{,}415 = 104{,}566$.",
         "Write $\\mathbf{A}^6 = 8^6\\mathbf{q}_1\\mathbf{q}_1^T + 3^6\\mathbf{q}_2\\mathbf{q}_2^T$ and read the top-right entries.",
         {"no-small": "You dropped the term for eigenvalue 3, which gives 104,857.6. It adds $3^6 \\times (-\\tfrac25)$.",
          "entrywise": "You raised the entry 2 to the sixth power, 64. Powers act on the eigenvalues, not the entries.",
          "plus": "You lost a sign and got 105,149.2. The second eigenvector gives the product $1 \\times (-2)$, so its term is negative."}))],
    "$\\mathbf{A}^6 = \\mathbf{Q}\\boldsymbol{\\Lambda}^6\\mathbf{Q}^T = 8^6\\mathbf{q}_1\\mathbf{q}_1^T + 3^6\\mathbf{q}_2\\mathbf{q}_2^T$. "
    "The top-right entries of $\\mathbf{q}_1\\mathbf{q}_1^T$ and $\\mathbf{q}_2\\mathbf{q}_2^T$ are $\\tfrac25$ and $-\\tfrac25$. "
    "So the entry is $\\tfrac25(262{,}144 - 729) = 104{,}566$."))

# linear-maps L4 (l18): a Jordan chain makes the response rise
lam = 0.85
resp = [t * lam ** (t - 1) for t in range(1, 60)]
t_peak = 1 + resp.index(max(resp))
tpow = max(t * lam ** t for t in range(1, 60))
items.append(parts(
    "e-chain-response", 4, ["lx-jordan"], ["jordan-response"], 240, "A shock that grows before it fades",
    "A two-variable model steps $\\mathbf{x}_{t+1} = \\mathbf{J}\\mathbf{x}_t$ with the Jordan block $\\mathbf{J} = \\begin{pmatrix}0.85&1\\\\0&0.85\\end{pmatrix}$. "
    "A shock $\\mathbf{x}_0 = (0, 1)$ hits the second variable.",
    "Two questions on the first variable's response.",
    [("Which is the top-right entry of $\\mathbf{J}^t$?",
      choice([
          opt("ok", "$t\\,(0.85)^{t-1}$", correct=True),
          opt("diag", "$(0.85)^t$", "You powered the diagonal only. The 1 above it feeds in a new term at every step."),
          opt("tpow", "$t\\,(0.85)^t$",
              "You counted one power too many. In $(0.85I + N)^t$ with $N^2 = 0$, the $N$ term is $t(0.85)^{t-1}N$."),
          opt("one", "1, at every $t$", "You powered the entries one by one. Matrix powers mix the entries.")]),
      fb("Since $N^2 = 0$, the binomial theorem gives $(0.85I + N)^t = 0.85^tI + t\\,0.85^{t-1}N$.",
         "Write $\\mathbf{J} = 0.85I + N$ and expand.")),
     ("What is the largest value the first variable reaches? Give 3 decimal places.",
      num(r(max(resp)), 0.0005, [("tpow", r(tpow), 0.0005), ("decay", 1, 0.0005)], placeholder="a decimal",
          label="Peak", accept="6 × 0.85^5 = 2.662"),
      fb("$t(0.85)^{t-1}$ rises while $t < 5.67$, so the peak is at $t = 6$, where it is 2.662.",
         "Compare neighbours: the ratio is $0.85\\tfrac{t + 1}{t}$.",
         {"tpow": "You used $t(0.85)^t$, which peaks at 2.263. The response is $t(0.85)^{t-1}$.",
          "decay": "You assumed an eigenvalue below 1 means a steady decay from 1. The chain makes the response rise first."}))],
    "The first variable is $x_t = t(0.85)^{t-1}$, and neighbours compare by $\\tfrac{x_{t+1}}{x_t} = 0.85\\tfrac{t + 1}{t}$. "
    "That ratio is above 1 exactly when $t < 5.67$. "
    "So the peak is $x_6 = 6(0.85)^5 = 2.662$, well above the shock of 1."))

# ================================================================ difficulty 5
# analysis L3 (l14): three positives then one negative
new_sum = math.log(2) + 0.5 * math.log(3)
items.append(parts(
    "e-three-one-rearrange", 5, ["an-series"], ["rearrangement"], 420, "Three up, one down",
    "Reorder $\\sum \\tfrac{(-1)^{n+1}}{n} = \\ln 2$ as three positive terms, then one negative: $1 + \\tfrac13 + \\tfrac15 - \\tfrac12 + \\tfrac17 + \\tfrac19 + \\tfrac{1}{11} - \\tfrac14 + \\cdots$. "
    "Use $H_n = 1 + \\tfrac12 + \\cdots + \\tfrac1n = \\ln n + \\gamma + o(1)$.",
    "Two questions on the new sum.",
    [("After $m$ blocks the positive terms used are $1, \\tfrac13, \\ldots, \\tfrac{1}{6m - 1}$. What is their sum?",
      choice([
          opt("ok", "$H_{6m} - \\tfrac12 H_{3m}$", correct=True),
          opt("all", "$H_{6m} - H_{3m}$",
              "You removed $H_{3m}$ for the even terms. They are $\\tfrac12 + \\tfrac14 + \\cdots + \\tfrac{1}{6m}$, which is $\\tfrac12 H_{3m}$."),
          opt("half", "$\\tfrac12 H_{6m}$",
              "You assumed the odd terms are half of all terms. They are $H_{6m}$ minus the even ones."),
          opt("three", "$H_{3m}$",
              "You took the first $3m$ reciprocals. The odd ones run to $\\tfrac{1}{6m - 1}$.")]),
      fb("The even reciprocals up to $\\tfrac{1}{6m}$ sum to $\\tfrac12 H_{3m}$; take them from $H_{6m}$.",
         "The odd reciprocals are all the reciprocals minus the even ones.")),
     ("The negatives used are $\\tfrac12 + \\cdots + \\tfrac{1}{2m} = \\tfrac12 H_m$. What is the new sum? Give 4 decimal places.",
      num(r(new_sum), 0.0001, [("same", r(math.log(2)), 0.00005), ("two-one", r(1.5 * math.log(2)), 0.00005)],
          placeholder="a decimal", label="Sum", accept="ln 2 + (1/2) ln 3 = 1.2425"),
      fb("$\\ln 6m - \\tfrac12 \\ln 3m - \\tfrac12 \\ln m \\to \\ln 2 + \\tfrac12 \\ln 3 = 1.2425$.",
         "Replace each $H$ by $\\ln n + \\gamma$; the $\\gamma$ terms cancel.",
         {"same": "You kept the old sum. Rearranging a conditionally convergent series can change it.",
          "two-one": "That is $\\tfrac32 \\ln 2 = 1.0397$, the two-then-one order. Here three positives come per negative."}))],
    "After $m$ blocks the sum is $H_{6m} - \\tfrac12 H_{3m} - \\tfrac12 H_m$. "
    "The $\\gamma$ terms cancel, and the logs give $\\ln 6 - \\tfrac12 \\ln 3 = \\ln 2 + \\tfrac12 \\ln 3 = 1.2425$. "
    "Inside a block the partial sums move by terms tending to 0, so the series has this sum."))

# analysis L2 (l10) with L4 (l15): a contraction converges to a fixed point
items.append(item(
    "e-contraction-proof", 5, ["an-sequences", "an-continuity"], ["contraction-proof"], 420, "A contraction has a fixed point",
    "Let $f : [a, b] \\to [a, b]$ satisfy $|f(x) - f(y)| \\le k|x - y|$ with $0 \\le k < 1$. "
    "Pick $x_0 \\in [a, b]$ and set $x_{n+1} = f(x_n)$. We prove $(x_n)$ converges to a point $L$ with $f(L) = L$.",
    "Put the proof in order. Move the two flawed lines to Left out.",
    {"kind": "order", "lines": [
        line("k1", "By induction, $|x_{n+1} - x_n| \\le k^n|x_1 - x_0|$."),
        line("k2", "For $m > n$, the triangle inequality and the geometric sum give $|x_m - x_n| \\le \\tfrac{k^n}{1 - k}|x_1 - x_0|$."),
        line("k3", "Since $k^n \\to 0$, that bound is below any $\\varepsilon > 0$ for large $n$, so $(x_n)$ is Cauchy."),
        line("k4", "Cauchy sequences in $\\mathbb{R}$ converge, so $x_n \\to L$, and $L \\in [a, b]$ since $a \\le x_n \\le b$."),
        line("k5", "$|f(x_n) - f(L)| \\le k|x_n - L|$, so $f(x_n) \\to f(L)$."),
        line("k6", "But $f(x_n) = x_{n+1} \\to L$, so $f(L) = L$ by uniqueness of limits."),
        line("e1", "Since $|x_{n+1} - x_n| \\to 0$, the sequence is Cauchy.",
             "Shrinking steps are not enough: the harmonic sums have steps tending to 0 and diverge. The bound on all later gaps is what makes it Cauchy."),
        line("e2", "The iterates are monotone and bounded, so they converge.",
             "Nothing makes them monotone. For $f(x) = 1 - \\tfrac x2$ on $[0, 1]$ they jump from side to side.")],
     "answer": ["k1", "k2", "k3", "k4", "k5", "k6"], "distractors": ["e1", "e2"]},
    fb("The geometric bound makes the iterates Cauchy, completeness gives the limit, and continuity makes it fixed.",
       "Bound the steps, then all later gaps, then use completeness and continuity."),
    "The steps shrink geometrically, so every gap beyond $n$ is at most $\\tfrac{k^n}{1 - k}|x_1 - x_0|$. "
    "That makes $(x_n)$ Cauchy, and completeness of $\\mathbb{R}$ gives a limit in $[a, b]$. "
    "Continuity of $f$ then turns $x_{n+1} = f(x_n)$ into $L = f(L)$."))

# linear-maps L4 (l17): the top eigenvalue is the largest quadratic form (self-marked)
items.append({
    "id": "e-rayleigh-proof", "difficulty": 5, "skills": ["lx-spectral"], "tags": ["rayleigh-proof"], "pace": 600,
    "title": "The largest variance of a unit-norm portfolio",
    "kind": "longform",
    "prompt": "Let $\\mathbf{A}$ be a real symmetric $n \\times n$ matrix with eigenvalues $\\lambda_1 \\ge \\lambda_2 \\ge \\cdots \\ge \\lambda_n$.\n\n"
              "(a) Prove that $\\mathbf{x}^T\\mathbf{A}\\mathbf{x} \\le \\lambda_1$ for every unit vector $\\mathbf{x}$, with equality at a unit eigenvector for $\\lambda_1$.\n\n"
              "(b) A covariance matrix $\\boldsymbol{\\Sigma}$ has eigenvalues 0.04, 0.01 and 0.005. "
              "What is the largest value of $\\mathbf{w}^T\\boldsymbol{\\Sigma}\\mathbf{w}$ over weight vectors with $\\|\\mathbf{w}\\| = 1$?\n\n"
              "Give a reason for every line.",
    "model": "**(a)** $\\mathbf{A}$ is real and symmetric. By the spectral theorem it has an orthonormal basis of eigenvectors $\\mathbf{q}_1, \\dots, \\mathbf{q}_n$ with $\\mathbf{A}\\mathbf{q}_i = \\lambda_i\\mathbf{q}_i$.\n\n"
             "Write a unit vector as $\\mathbf{x} = \\sum_i c_i\\mathbf{q}_i$ with $c_i = \\langle \\mathbf{x}, \\mathbf{q}_i \\rangle$. "
             "By Pythagoras for an orthonormal list, $\\sum_i c_i^2 = \\|\\mathbf{x}\\|^2 = 1$.\n\n"
             "By linearity, $\\mathbf{A}\\mathbf{x} = \\sum_i \\lambda_i c_i\\mathbf{q}_i$. "
             "So $\\mathbf{x}^T\\mathbf{A}\\mathbf{x} = \\sum_{i,j} c_j\\lambda_i c_i\\,\\mathbf{q}_j^T\\mathbf{q}_i = \\sum_i \\lambda_i c_i^2$. "
             "The cross terms vanish because $\\mathbf{q}_j^T\\mathbf{q}_i = 0$ for $i \\ne j$.\n\n"
             "Each $\\lambda_i \\le \\lambda_1$ and each $c_i^2 \\ge 0$, so $\\sum_i \\lambda_i c_i^2 \\le \\lambda_1 \\sum_i c_i^2 = \\lambda_1$.\n\n"
             "At $\\mathbf{x} = \\mathbf{q}_1$ we have $c_1 = 1$ and every other $c_i = 0$, so $\\mathbf{x}^T\\mathbf{A}\\mathbf{x} = \\lambda_1$. "
             "The bound is attained. $\\blacksquare$\n\n"
             "The same steps with $\\lambda_i \\ge \\lambda_n$ show that the least value is $\\lambda_n$.\n\n"
             "**(b)** A covariance matrix is symmetric, so (a) applies. "
             "The largest value is the top eigenvalue, 0.04, along its eigenvector. That is a standard deviation of 20%.",
    "rubric": [
        {"points": 2, "text": "Invokes the spectral theorem for an orthonormal eigenbasis, naming symmetry as the reason (another complete route also earns rows 1 to 3)"},
        {"points": 2, "text": "Expands $\\mathbf{x}$ in that basis and shows $\\sum c_i^2 = 1$ by orthonormality"},
        {"points": 2, "text": "Shows $\\mathbf{x}^T\\mathbf{A}\\mathbf{x} = \\sum \\lambda_i c_i^2$, with the cross terms vanishing"},
        {"points": 2, "text": "Bounds the sum by $\\lambda_1$ using $c_i^2 \\ge 0$ and $\\sum c_i^2 = 1$"},
        {"points": 1, "text": "Shows equality at a unit eigenvector for $\\lambda_1$"},
        {"points": 1, "text": "Gives 0.04 in (b) and says why (a) applies to a covariance matrix"}],
    "explain": {"text": "In an orthonormal eigenbasis, $\\mathbf{x}^T\\mathbf{A}\\mathbf{x}$ becomes $\\sum \\lambda_i c_i^2$, an average of the eigenvalues with weights summing to 1. "
                        "Such an average is at most the largest eigenvalue. "
                        "So the top eigenvalue of a covariance matrix is the largest variance of a unit-norm portfolio."}})

order = {2: [], 3: [], 4: [], 5: []}
for it in items:
    order[it["difficulty"]].append(it)
exam = {
    "id": "topic-1.10", "topic": "1.10", "name": "Analysis and proof-based linear algebra", "minutes": 100, "pass": 0.7,
    "skills": {"an-reals": "The real numbers", "an-sequences": "Sequences and limits", "an-series": "Series",
               "an-continuity": "Continuity", "an-calculus": "Derivatives and integrals proved",
               "an-metric": "Metric spaces",
               "lx-spaces": "Abstract vector spaces", "lx-maps": "Linear maps", "lx-dual": "Duality",
               "lx-inner": "Inner product spaces", "lx-spectral": "The spectral theorem",
               "lx-jordan": "Operators and the Jordan form"},
    "items": order[2] + order[3] + order[4] + order[5],
}
with open(OUT, "w", encoding="utf8") as f:
    json.dump(exam, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("wrote", os.path.normpath(OUT), len(exam["items"]), "items, pace", sum(i["pace"] for i in exam["items"]), "s")
