"""Build app/content/exams/topic-1.11.json (topic 1.11, Complex numbers, vector calculus and differential equations:
complex, vector-calc and odes).

Route A for every key: the closed forms below. check_numbers.py recomputes each value by a second route and
asserts it at its path in the written file. Run from anywhere: python3 docs/briefs/exam-1.11-scripts/build.py
"""
import cmath
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-1.11.json')
E = math.e
PI = math.pi


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
# complex L1 (l1): division by the conjugate
z_div = (4 + 7j) / (2 - 3j)
assert abs(z_div - (-1 + 2j)) < 1e-12
items.append(item(
    "e-divide-conjugate", 2, ["cz-arith"], ["division"], 75, "A quotient in the form a + bi",
    "Take $z = \\dfrac{4 + 7i}{2 - 3i}$.",
    "Write $z$ in the form $a + bi$.",
    expr("-1+2i", ["-1+2i", "2i-1", "-1+2\\cdot i"],
         [("plus-one", "\\frac{29+26i}{13}"), ("times-bottom", "\\frac{29+2i}{13}")]),
    fb("Multiplying top and bottom by $2 + 3i$ gives $\\tfrac{-13 + 26i}{13} = -1 + 2i$.",
       "Multiply top and bottom by the conjugate of the bottom.",
       {"plus-one": "You took $i^2 = 1$. With $i^2 = -1$ the top is $8 - 21 + 26i = -13 + 26i$.",
        "times-bottom": "You multiplied by $2 - 3i$ itself. The conjugate $2 + 3i$ is what makes the bottom real."}),
    "The conjugate $2 + 3i$ makes the bottom $2^2 + 3^2 = 13$. "
    "The top is $(4 + 7i)(2 + 3i) = 8 + 26i + 21i^2 = -13 + 26i$. "
    "So $z = -1 + 2i$, and $(-1 + 2i)(2 - 3i) = 4 + 7i$ checks it."))

# complex L1 (l2): modulus and principal argument in the third quadrant
z_q = complex(-2 * math.sqrt(3), -2)
mod_q = abs(z_q)
arg_q = cmath.phase(z_q)
assert abs(mod_q - 4) < 1e-12 and abs(arg_q + 5 * PI / 6) < 1e-12
items.append(parts(
    "e-arg-quadrant", 2, ["cz-polar"], ["modulus-argument"], 90, "A point in the third quadrant",
    "Let $z = -2\\sqrt3 - 2i$.",
    "Two questions on the polar form of $z$.",
    [("What is $|z|$?",
      num(mod_q, 0.001, [("no-root", 16, 0.001)], label="|z|"),
      fb("$|z| = \\sqrt{12 + 4} = 4$.",
         "Take the square root of $x^2 + y^2$.",
         {"no-root": "You gave $|z|^2 = 16$. The modulus is its square root, 4."})),
     ("What is $\\operatorname{Arg} z$, in $(-\\pi, \\pi]$?",
      choice([
          opt("ok", "$-\\tfrac{5\\pi}{6}$", correct=True),
          opt("arctan", "$\\tfrac{\\pi}{6}$",
              "You took $\\arctan(y/x)$, which lands in the first quadrant. The point $(-2\\sqrt3, -2)$ is in the third."),
          opt("range", "$\\tfrac{7\\pi}{6}$",
              "You found the right direction but left $(-\\pi, \\pi]$. Subtract $2\\pi$."),
          opt("flip", "$\\tfrac{5\\pi}{6}$",
              "You flipped the sign. $\\tfrac{5\\pi}{6}$ points into the second quadrant, above the real axis.")]),
      fb("The point is below the negative real axis, $\\tfrac{\\pi}{6}$ short of $-\\pi$.",
         "Sketch the point first, then measure from the positive real axis."))],
    "$|z| = \\sqrt{(2\\sqrt3)^2 + 2^2} = 4$. "
    "The reference angle is $\\arctan\\tfrac{2}{2\\sqrt3} = \\tfrac{\\pi}{6}$, and the point is in the third quadrant. "
    "So $\\operatorname{Arg} z = -\\pi + \\tfrac{\\pi}{6} = -\\tfrac{5\\pi}{6}$."))

# vector-calc L1 (l2): mass of a straight wire
mass = 5 * (2 + 5)
items.append(item(
    "e-wire-mass", 2, ["vk-line"], ["scalar-line-integral"], 90, "The mass of a straight wire",
    "A wire runs straight from $(1, 0)$ to $(4, 4)$. Its density is $f(x, y) = 2x + y$.",
    "What is $\\int_C f\\,ds$, the mass of the wire?",
    num(mass, 0.001, [("no-speed", mass / 5, 0.001), ("far-end", 12 * 5, 0.001)], label="Mass"),
    fb("With $ds = 5\\,dt$, the mass is $\\int_0^1 (2 + 10t)\\,5\\,dt = 35$.",
       "Parametrise the segment, then multiply by $|\\mathbf r'(t)|$.",
       {"no-speed": "You left out $|\\mathbf r'(t)| = 5$, so you got 7. Each step $dt$ covers a length $5\\,dt$.",
        "far-end": "You used the density at the far end, 12, for the whole wire. It rises from 2 to 12, so integrate it."}),
    "Take $\\mathbf r(t) = (1 + 3t, 4t)$ for $0 \\le t \\le 1$, so $|\\mathbf r'(t)| = 5$. "
    "Then $f = 2 + 10t$, and $\\int_0^1 (2 + 10t)\\,5\\,dt = 5(2 + 5) = 35$. "
    "The mean density is 7, over a length of 5."))

# odes L1 (l5): a mean-reverting rate
kap, th, r0, tt = 0.25, 0.045, 0.07, 4
r_t = th + (r0 - th) * math.exp(-kap * tt)
r_sign = th - (r0 - th) * math.exp(-kap * tt)
r_not = th + (r0 - th) * math.exp(-kap)
items.append(item(
    "e-rate-pull", 2, ["de-first"], ["mean-reversion"], 75, "A rate pulled to its mean",
    "A short rate follows $r' = 0.25(0.045 - r)$ with $r(0) = 0.07$, time in years.",
    "What is $r(4)$? Give it as a decimal.",
    num(r(r_t), 0.00005, [("sign", r(r_sign), 0.00005), ("no-t", r(r_not), 0.00005)], placeholder="a decimal",
        label="r(4)", accept="0.0542, about 5.42%"),
    fb("The gap of 0.025 shrinks by $e^{-1}$, so $r(4) = 0.045 + 0.0092 = 0.0542$.",
       "Write $r(t) = \\theta + (r_0 - \\theta)e^{-\\kappa t}$.",
       {"sign": "You subtracted the gap. The rate starts above 0.045, so it stays above as the gap decays.",
        "no-t": "You used $e^{-\\kappa}$, one year of decay. Four years give $e^{-0.25 \\times 4} = e^{-1}$."}),
    "The gap $r - 0.045$ decays as $e^{-0.25t}$, so $r(t) = 0.045 + 0.025e^{-0.25t}$. "
    "At $t = 4$ the factor is $e^{-1} = 0.3679$. "
    "So $r(4) = 0.045 + 0.0092 = 0.0542$."))

# odes L2 (l7): distinct real roots
items.append(item(
    "e-char-roots", 2, ["de-second"], ["characteristic"], 75, "Two real roots",
    "Take $y'' - 2y' - 15y = 0$.",
    "Which is the general solution?",
    choice([
        opt("ok", "$c_1e^{5t} + c_2e^{-3t}$", correct=True),
        opt("flip", "$c_1e^{-5t} + c_2e^{3t}$",
            "You solved $r^2 + 2r - 15 = 0$, flipping the sign of the middle term."),
        opt("double", "$(c_1 + c_2t)e^{5t}$",
            "You treated the root as repeated. The roots 5 and $-3$ are distinct, so each gives its own exponential."),
        opt("complex", "$e^{t}(c_1\\cos\\sqrt{14}\\,t + c_2\\sin\\sqrt{14}\\,t)$",
            "You took $-15$ as $+15$. The discriminant is $4 + 60 = 64 > 0$, so the roots are real.")]),
    fb("$r^2 - 2r - 15 = (r - 5)(r + 3)$, so the roots are 5 and $-3$.",
       "Try $y = e^{rt}$ and solve the quadratic in $r$."),
    "Trying $e^{rt}$ gives $r^2 - 2r - 15 = 0$, with discriminant $4 + 60 = 64$. "
    "So $r = \\tfrac{2 \\pm 8}{2}$, that is 5 and $-3$. "
    "Two distinct real roots give $c_1e^{5t} + c_2e^{-3t}$."))

# odes L4 (l14): the shift rule
items.append(item(
    "e-laplace-shift", 2, ["de-laplace"], ["shift-rule"], 75, "A damped sine, transformed",
    "A payment stream pays at rate $f(t) = e^{-2t}\\sin 3t$.",
    "What is $F(s) = \\mathcal{L}\\{f\\}(s)$, for $s > -2$?",
    expr("\\frac{3}{(s+2)^2+9}", ["3/((s+2)^2+9)", "\\frac{3}{s^2+4s+13}", "3/(s^2+4s+13)"],
         [("shift-sign", "\\frac{3}{(s-2)^2+9}"), ("cosine-row", "\\frac{s+2}{(s+2)^2+9}")], keyboard="calculus"),
    fb("$\\mathcal{L}\\{\\sin 3t\\} = \\tfrac{3}{s^2 + 9}$, shifted from $s$ to $s + 2$.",
       "Transform $\\sin 3t$, then apply the shift rule.",
       {"shift-sign": "You shifted the wrong way. A factor $e^{at}$ replaces $s$ by $s - a$, and here $a = -2$.",
        "cosine-row": "You used the cosine row. The sine row has the frequency 3 on top, not $s$."}),
    "$\\mathcal{L}\\{\\sin 3t\\} = \\tfrac{3}{s^2 + 9}$. "
    "Multiplying by $e^{-2t}$ shifts $s$ to $s + 2$. "
    "So $F(s) = \\tfrac{3}{(s + 2)^2 + 9}$, defined for $s > -2$."))

# ================================================================ difficulty 3
# complex L1 (l4): fifth roots of -32
roots5 = [2 * cmath.exp(1j * (PI + 2 * PI * k) / 5) for k in range(5)]
assert all(abs(w ** 5 + 32) < 1e-9 for w in roots5)
items.append(item(
    "e-fifth-roots", 3, ["cz-polar"], ["nth-roots"], 120, "Fifth roots of a negative number",
    "We look for every $w$ with $w^5 = -32$.",
    "Which of these solve $w^5 = -32$? Select all that apply.",
    choice([
        opt("minus-two", "$-2$", correct=True),
        opt("pi-fifth", "$2e^{i\\pi/5}$", correct=True),
        opt("seven", "$2e^{7\\pi i/5}$", correct=True),
        opt("two", "$2$", "You solved $w^5 = 32$. $2^5 = 32$, not $-32$."),
        opt("zero-arg", "$2e^{2\\pi i/5}$",
            "You gave $-32$ argument 0. Then $(2e^{2\\pi i/5})^5 = 32e^{2\\pi i} = 32$."),
        opt("half-pi", "$2e^{i\\pi/10}$",
            "You gave $-32$ argument $\\tfrac{\\pi}{2}$. Then $(2e^{i\\pi/10})^5 = 32i$.")], kind="multi"),
    fb("$-32 = 32e^{i\\pi}$, so the roots are $2e^{i(\\pi + 2\\pi k)/5}$.",
       "Write $-32$ in polar form, then divide its argument by 5 and add steps of $\\tfrac{2\\pi}{5}$."),
    "$-32 = 32e^{i\\pi}$, so the roots are $2e^{i(\\pi + 2\\pi k)/5}$ for $k = 0, \\dots, 4$. "
    "Their arguments are $\\tfrac{\\pi}{5}, \\tfrac{3\\pi}{5}, \\pi, \\tfrac{7\\pi}{5}, \\tfrac{9\\pi}{5}$, spaced by $\\tfrac{2\\pi}{5}$. "
    "The root at $\\pi$ is $-2$."))

# complex L2 (l7): a harmonic conjugate
items.append(item(
    "e-harmonic-partner", 3, ["cz-functions"], ["harmonic-conjugate"], 150, "The other half of an analytic function",
    "Let $u(x, y) = e^x\\cos y + 2xy$. It is harmonic on the whole plane.",
    "Find $v(x, y)$ with $v(0, 0) = 0$ so that $f = u + iv$ is analytic.",
    expr("e^{x}\\sin(y)-x^2+y^2", ["e^x\\sin y-x^2+y^2", "e^x sin(y) - x^2 + y^2", "y^2-x^2+e^{x}\\sin(y)"],
         [("swap", "-e^{x}\\sin(y)+x^2-y^2"), ("no-g", "e^{x}\\sin(y)+y^2")], keyboard="calculus"),
    fb("$v_y = u_x$ gives $e^x\\sin y + y^2 + g(x)$, and $v_x = -u_y$ fixes $g(x) = -x^2$.",
       "Integrate $v_y = u_x$ in $y$, then match $v_x = -u_y$.",
       {"swap": "You used $u_y = v_x$. Cauchy-Riemann says $u_y = -v_x$, which flips the sign of $v$.",
        "no-g": "You stopped after $v_y = u_x$. Matching $v_x = -u_y = e^x\\sin y - 2x$ adds $-x^2$."}),
    "From $v_y = u_x = e^x\\cos y + 2y$ we get $v = e^x\\sin y + y^2 + g(x)$. "
    "Then $v_x = e^x\\sin y + g'(x)$ must equal $-u_y = e^x\\sin y - 2x$, so $g = -x^2$. "
    "So $f = e^z - iz^2$, analytic on the whole plane."))

# complex L2 (l8): the principal log of a square
z_l = complex(-1, math.sqrt(3))
im_log_sq = cmath.log(z_l * z_l).imag
twice_arg = 2 * cmath.phase(z_l)
items.append(parts(
    "e-log-square", 3, ["cz-functions", "cz-polar"], ["principal-log"], 150, "The log of a square",
    "Let $z = -1 + \\sqrt3\\,i$, so $\\operatorname{Arg} z = \\tfrac{2\\pi}{3}$ and $z^2 = -2 - 2\\sqrt3\\,i$.",
    "Two questions on $\\operatorname{Log}(z^2)$.",
    [("What is $\\operatorname{Im}\\operatorname{Log}(z^2)$? Give it to 3 decimal places.",
      num(r(im_log_sq, 4), 0.001, [("doubled", r(twice_arg, 4), 0.001)], label="Im Log(z²)"),
      fb("$\\operatorname{Arg}(z^2) = \\tfrac{4\\pi}{3} - 2\\pi = -\\tfrac{2\\pi}{3} \\approx -2.094$.",
         "Double the argument, then bring it back into $(-\\pi, \\pi]$.",
         {"doubled": "You doubled $\\operatorname{Arg} z$ to $\\tfrac{4\\pi}{3}$. That is outside $(-\\pi, \\pi]$, so subtract $2\\pi$."})),
     ("Which statement is true?",
      choice([
          opt("ok", "$\\operatorname{Log}(z^2) = 2\\operatorname{Log} z - 2\\pi i$", correct=True),
          opt("real-rule", "$\\operatorname{Log}(z^2) = 2\\operatorname{Log} z$, as for real logarithms",
              "You carried the real rule over. Doubling the argument leaves $(-\\pi, \\pi]$ here, so the two differ by $2\\pi i$."),
          opt("modulus", "$\\operatorname{Log}(z^2)$ and $2\\operatorname{Log} z$ have different real parts",
              "You blamed the modulus. Both real parts are $\\ln 4$; only the imaginary parts differ."),
          opt("undefined", "$\\operatorname{Log}(z^2)$ is undefined, since $z^2$ is in the third quadrant",
              "You confused a quadrant with the cut. $\\operatorname{Log}$ is defined at every $w \\ne 0$.")]),
      fb("The real parts agree, and the imaginary parts differ by $2\\pi$.",
         "Compare real parts and imaginary parts separately."))],
    "$2\\operatorname{Arg} z = \\tfrac{4\\pi}{3}$ lies outside $(-\\pi, \\pi]$, so $\\operatorname{Arg}(z^2) = -\\tfrac{2\\pi}{3}$. "
    "Both logarithms have real part $\\ln|z^2| = \\ln 4$. "
    "So $\\operatorname{Log}(z^2) = 2\\operatorname{Log} z - 2\\pi i$."))

# complex L3 (l9): the conjugate round a circle
rad = 2.5
c_conj = 2 * rad ** 2
items.append(item(
    "e-conjugate-circle", 3, ["cz-contour"], ["non-analytic-integral"], 120, "The conjugate round a circle",
    "Let $\\gamma$ be the circle $|z| = 2.5$, once anticlockwise.",
    "$\\oint_\\gamma \\bar z\\,dz = c\\pi i$. What is $c$?",
    num(c_conj, 0.01, [("cauchy", 0, 0.01), ("radius", 2 * rad, 0.01)], label="c"),
    fb("On the circle $\\bar z = \\tfrac{6.25}{z}$, so the integral is $6.25 \\times 2\\pi i = 12.5\\pi i$.",
       "Use $z\\bar z = |z|^2$ on the circle.",
       {"cauchy": "You used Cauchy's theorem. $\\bar z$ is analytic nowhere, so the theorem does not apply.",
        "radius": "You took $\\bar z = \\tfrac{r}{z}$, which gives 5. On the circle $\\bar z = \\tfrac{r^2}{z}$, with $r^2 = 6.25$."}),
    "On $|z| = 2.5$ we have $z\\bar z = 6.25$, so $\\bar z = \\tfrac{6.25}{z}$. "
    "Then $\\oint \\tfrac{6.25}{z}\\,dz = 6.25 \\times 2\\pi i = 12.5\\pi i$. "
    "Cauchy's theorem gives no help, since $\\bar z$ is not analytic."))

# complex L3 (l12): characteristic function of an independent sum
u0 = 0.8
cf = math.exp(-u0) * math.exp(-u0 ** 2 / 2)
cf_add = math.exp(-u0) + math.exp(-u0 ** 2 / 2)
cf_nohalf = math.exp(-u0) * math.exp(-u0 ** 2)
items.append(item(
    "e-cauchy-plus-normal", 3, ["cz-fourier"], ["cf-of-sum"], 120, "A Cauchy shock plus a normal one",
    "$X$ is standard Cauchy, with $\\varphi_X(u) = e^{-|u|}$. $Y \\sim N(0, 1)$ is independent of $X$.",
    "What is $\\varphi_{X+Y}(0.8)$? Give it to 4 decimal places.",
    num(r(cf, 4), 0.0005, [("added", r(cf_add, 4), 0.0005), ("no-half", r(cf_nohalf, 4), 0.0005)], label="φ(0.8)"),
    fb("$\\varphi_{X+Y}(0.8) = e^{-0.8}e^{-0.32} = e^{-1.12} = 0.3263$.",
       "For independent variables, characteristic functions multiply.",
       {"added": "You added the two functions and got 1.1755. Independent sums multiply them, and $|\\varphi| \\le 1$ always.",
        "no-half": "You used $e^{-u^2}$ for $N(0, 1)$, giving 0.2369. Its characteristic function is $e^{-u^2/2}$."}),
    "For independent $X$ and $Y$, $\\varphi_{X+Y} = \\varphi_X\\varphi_Y$. "
    "Here that is $e^{-|u|}e^{-u^2/2}$, so at $u = 0.8$ it is $e^{-0.8 - 0.32} = e^{-1.12} = 0.3263$. "
    "It is real, as both laws are symmetric about 0."))

# vector-calc L1 (l4): work from a potential
f_pot = lambda x, y: x * x * y + x * y ** 3 + y * y
work = f_pot(2, 1) - f_pot(1, 0)
items.append(parts(
    "e-potential-work", 3, ["vk-fields", "vk-line"], ["potential"], 150, "Work along a winding path",
    "Let $\\mathbf F = (2xy + y^3,\\ x^2 + 3xy^2 + 2y)$ on the whole plane. "
    "A particle moves along a winding path from $(1, 0)$ to $(2, 1)$.",
    "Two questions on the work $\\mathbf F$ does.",
    [("Which statement is true?",
      choice([
          opt("ok", "$P_y = Q_x = 2x + 3y^2$ on the plane, which is simply connected, so $\\mathbf F$ has a potential.",
              correct=True),
          opt("poly", "$\\mathbf F$ has a potential because its components are polynomials.",
              "You judged by the formula's type. $(-y, x)$ has polynomial components and no potential."),
          opt("winding", "The work depends on the path, since this path winds.",
              "You assumed winding changes the work. With a potential the work is $f(B) - f(A)$ on every path."),
          opt("wrong-test", "$P_x = Q_y$ is the test, and it fails, so there is no potential.",
              "You compared the wrong partials. The test is $P_y = Q_x$, and it holds here.")]),
      fb("The partials match on a simply connected region, so a potential exists.",
         "Compare $P_y$ with $Q_x$, and check the region.")),
     ("What work does $\\mathbf F$ do along the path?",
      num(work, 0.001, [("no-g", work - 1, 0.001)], label="Work"),
      fb("$f = x^2y + xy^3 + y^2$, so the work is $f(2, 1) - f(1, 0) = 7$.",
         "Find $f$ with $f_x = P$ and $f_y = Q$, then subtract its end values.",
         {"no-g": "You stopped at $x^2y + xy^3$ and got 6. Matching $f_y$ with $Q$ adds $g(y) = y^2$, worth 1 at $(2, 1)$."}))],
    "Integrating $P$ in $x$ gives $x^2y + xy^3 + g(y)$, and $f_y = Q$ forces $g'(y) = 2y$. "
    "So $f = x^2y + xy^3 + y^2$. "
    "The work is $f(2, 1) - f(1, 0) = 7 - 0 = 7$, on any piecewise smooth path."))

# vector-calc L2 (l6, l8): circulation and flux on one circle
curl_c, div_c, area = 3 - (-5), 2 + 1, 9
items.append(parts(
    "e-circulation-flux", 3, ["vk-theorems", "vk-fields"], ["green-two-forms"], 150, "Circulation and flux on one circle",
    "Let $\\mathbf F = (2x - 5y,\\ 3x + y)$, smooth on the whole plane. "
    "Let $C$ be the circle of radius 3 about the origin, anticlockwise.",
    "Two questions on $\\mathbf F$ round $C$.",
    [("The circulation $\\oint_C \\mathbf F \\cdot d\\mathbf r$ is $c\\pi$. What is $c$?",
      num(curl_c * area, 0, [("sign", -curl_c * area, 0), ("div", div_c * area, 0)], placeholder="a whole number", label="c"),
      fb("$Q_x - P_y = 8$ over an area of $9\\pi$ gives $72\\pi$.",
         "Use Green's theorem with the scalar curl.",
         {"sign": "You used $P_y - Q_x$. Green's theorem integrates $Q_x - P_y = 3 + 5 = 8$.",
          "div": "You integrated the divergence. That gives the flux, not the circulation."})),
     ("The outward flux $\\oint_C \\mathbf F \\cdot \\mathbf n\\,ds$ is $c\\pi$. What is $c$?",
      num(div_c * area, 0, [("curl", curl_c * area, 0), ("radius", div_c * 3, 0)], placeholder="a whole number", label="c"),
      fb("$P_x + Q_y = 3$ over an area of $9\\pi$ gives $27\\pi$.",
         "Use the flux form of Green's theorem, with the divergence.",
         {"curl": "You integrated the curl. Flux uses the divergence, $P_x + Q_y = 3$.",
          "radius": "You took the area as $3\\pi$, with $r$ not squared. The disc has area $9\\pi$."}))],
    "Green's theorem turns the circulation into $\\iint (Q_x - P_y)\\,dA = 8 \\times 9\\pi = 72\\pi$. "
    "The flux form gives $\\iint (P_x + Q_y)\\,dA = 3 \\times 9\\pi = 27\\pi$. "
    "Both need $\\mathbf F$ continuously differentiable on the closed disc, which holds here."))

# vector-calc L3 (l9): area of a tilted plane piece
ru, rv = (1, 0, 3), (0, 1, -1)
cr = (ru[1] * rv[2] - ru[2] * rv[1], ru[2] * rv[0] - ru[0] * rv[2], ru[0] * rv[1] - ru[1] * rv[0])
cr_len = math.sqrt(sum(c * c for c in cr))
s_area = 2 * cr_len
s_lengths = 2 * math.sqrt(10) * math.sqrt(2)
items.append(item(
    "e-tilted-patch", 3, ["vk-surface"], ["surface-area"], 120, "The area of a tilted patch",
    "The surface $S$ is $\\mathbf r(u, v) = (u,\\ v,\\ 3u - v)$ for $0 \\le u \\le 2$ and $0 \\le v \\le 1$.",
    "What is the area of $S$? Give it to 3 decimal places.",
    num(r(s_area, 4), 0.005, [("no-factor", 2, 0.005), ("lengths", r(s_lengths, 4), 0.005)], label="Area"),
    fb("$|\\mathbf r_u \\times \\mathbf r_v| = \\sqrt{11}$ on a rectangle of area 2, so the area is $2\\sqrt{11} = 6.633$.",
       "Find $\\mathbf r_u \\times \\mathbf r_v$ and its length.",
       {"no-factor": "You found the area of the parameter rectangle. Each cell is stretched by $\\sqrt{11}$.",
        "lengths": "You multiplied $|\\mathbf r_u| = \\sqrt{10}$ by $|\\mathbf r_v| = \\sqrt2$, giving 8.944. That needs right angles; use the cross product."}),
    "$\\mathbf r_u = (1, 0, 3)$ and $\\mathbf r_v = (0, 1, -1)$, so $\\mathbf r_u \\times \\mathbf r_v = (-3, 1, 1)$, of length $\\sqrt{11}$. "
    "The map is smooth and one-to-one, so the area is $\\sqrt{11} \\times 2 = 6.633$. "
    "Each cell of the rectangle grows by $\\sqrt{11} \\approx 3.317$."))

# vector-calc L3 (l11): outflow from a cube
flux_cube = 3 * (8 / 3) * 4
items.append(item(
    "e-cube-outflow", 3, ["vk-theorems", "vk-surface"], ["divergence-theorem"], 150, "Outflow from a cube",
    "Let $\\mathbf F = (xz^2,\\ yx^2,\\ zy^2)$, smooth everywhere. "
    "Let $S$ be the surface of the cube $[0, 2]^3$, with outward normal.",
    "What is the outward flux $\\oiint_S \\mathbf F \\cdot \\mathbf n\\,dS$?",
    num(flux_cube, 0.001, [("centre", 3 * 8, 0.001), ("one-term", flux_cube / 3, 0.001)], label="Flux"),
    fb("$\\nabla \\cdot \\mathbf F = x^2 + y^2 + z^2$, and its integral over the cube is 32.",
       "Use the divergence theorem, then integrate the divergence over the cube.",
       {"centre": "You multiplied the divergence at the centre, 3, by the volume 8. The divergence is not linear, so integrate it.",
        "one-term": "You integrated only $x^2$, giving $\\tfrac{32}{3}$. The divergence also has $y^2$ and $z^2$."}),
    "$\\nabla \\cdot \\mathbf F = z^2 + x^2 + y^2$, and $\\mathbf F$ is smooth on the closed cube, so the divergence theorem applies. "
    "Each square term integrates to $\\tfrac83 \\times 4 = \\tfrac{32}{3}$ over the cube. "
    "The flux is $3 \\times \\tfrac{32}{3} = 32$."))

# odes L1 (l3): integrating factor
y_if = 3 * math.exp(-1) + 2 * math.exp(-4)
y_add = 3 * math.exp(-1) + 2
y_nofit = 3 * math.exp(-1) + 5 * math.exp(-4)
items.append(item(
    "e-integrating-factor", 3, ["de-first"], ["integrating-factor"], 150, "A forced decay",
    "Take $y' + 4y = 9e^{-t}$ with $y(0) = 5$.",
    "What is $y(1)$? Give it to 3 decimal places.",
    num(r(y_if, 4), 0.0005, [("const-add", r(y_add, 4), 0.0005), ("no-fit", r(y_nofit, 4), 0.0005)], label="y(1)"),
    fb("$y = 3e^{-t} + 2e^{-4t}$, so $y(1) = 1.1403$.",
       "Multiply by $e^{4t}$, integrate, fit the constant, then divide.",
       {"const-add": "You added the constant after dividing by $\\mu$, giving 3.1036. It must be divided by $e^{4t}$ too.",
        "no-fit": "You set $C = y(0) = 5$, giving 1.1952. At $t = 0$, $y = 3 + C$, so $C = 2$."}),
    "Multiplying by $\\mu = e^{4t}$ gives $(e^{4t}y)' = 9e^{3t}$, so $e^{4t}y = 3e^{3t} + C$. "
    "Then $y = 3e^{-t} + Ce^{-4t}$, and $y(0) = 5$ gives $C = 2$. "
    "At $t = 1$, $y = 3e^{-1} + 2e^{-4} = 1.1403$."))

# odes L2 (l8): forcing that solves the homogeneous equation
A_res = 12 / (2 * 2 + 2)
items.append(item(
    "e-resonant-guess", 3, ["de-second"], ["undetermined-coefficients"], 150, "A guess that needs a t",
    "Take $y'' + 2y' - 8y = 12e^{2t}$. The guess $Ae^{2t}$ fails, since $e^{2t}$ solves the homogeneous equation.",
    "A particular solution is $y_p = Ate^{2t}$. What is $A$?",
    num(A_res, 0.001, [("deriv", 3, 0.001)], label="A"),
    fb("The $t$ terms cancel and leave $6Ae^{2t} = 12e^{2t}$, so $A = 2$.",
       "Differentiate $Ate^{2t}$ twice by the product rule, then substitute.",
       {"deriv": "You took $y_p'' = A(2 + 4t)e^{2t}$. Differentiating $(1 + 2t)e^{2t}$ gives $(4 + 4t)e^{2t}$."}),
    "With $y_p = Ate^{2t}$, $y_p' = A(1 + 2t)e^{2t}$ and $y_p'' = A(4 + 4t)e^{2t}$. "
    "Substituting, the $t$ terms cancel and leave $(4A + 2A)e^{2t} = 12e^{2t}$. "
    "So $A = 2$."))

# odes L2 (l9): damping past critical
b_crit = 2 * math.sqrt(16)
roots_b10 = sorted([(-10 + math.sqrt(100 - 64)) / 2, (-10 - math.sqrt(100 - 64)) / 2])
k_slow = -roots_b10[1]
items.append(parts(
    "e-damping-rate", 3, ["de-second"], ["damping"], 150, "More damping, slower decay",
    "Take $y'' + by' + 16y = 0$ with $b > 0$.",
    "Two questions on how the damping $b$ sets the decay.",
    [("What value of $b$ gives critical damping?",
      num(b_crit, 0.001, [("omega", 4, 0.001)], label="b"),
      fb("Critical damping is a double root: $b^2 = 4 \\times 16$, so $b = 8$.",
         "Set the discriminant of $r^2 + br + 16$ to 0."),
      ),
     ("At $b = 10$, the slower mode decays as $e^{-kt}$. What is $k$?",
      num(k_slow, 0.001, [("fast", 8, 0.001), ("half-b", 5, 0.001)], label="k"),
      fb("$r^2 + 10r + 16 = (r + 2)(r + 8)$, so the slow mode is $e^{-2t}$.",
         "Factorise $r^2 + 10r + 16$ and take the root nearer 0.",
         {"fast": "You took the fast root. The $e^{-8t}$ term dies first, so $e^{-2t}$ sets the pace.",
          "half-b": "You took $\\tfrac{b}{2}$. That is the decay rate only for $b \\le 8$; past critical the roots split."}))],
    "$r^2 + br + 16 = 0$ has a double root when $b^2 = 64$, so $b = 8$ and both modes decay as $e^{-4t}$. "
    "At $b = 10$ the roots are $-2$ and $-8$. "
    "The slow mode $e^{-2t}$ decays more slowly than at $b = 8$, so more damping is not always faster."))
items[-1]["parts"][0]["feedback"]["byKey"] = {
    "omega": "You set $b = \\omega_0 = 4$. Critical damping needs $b^2 = 4 \\times 16$, so $b = 2\\omega_0 = 8$."}

# odes L3 (l10): a saddle from its eigenvectors
c1, c2 = 2, 1
x1_half = c1 * 2 * math.exp(3 * 0.5) + c2 * 2 * math.exp(-0.5)
x1_swap = c1 * 2 * math.exp(-0.5) + c2 * 2 * math.exp(1.5)
x1_novec = c1 * math.exp(1.5) + c2 * math.exp(-0.5)
items.append(parts(
    "e-saddle-solution", 3, ["de-systems"], ["eigen-solution"], 150, "A solution from two eigenvectors",
    "Let $\\mathbf x' = \\mathbf A\\mathbf x$ with $\\mathbf A = \\begin{pmatrix}1&4\\\\1&1\\end{pmatrix}$ and $\\mathbf x(0) = (6, 1)$. "
    "The eigenvalues are 3 and $-1$, with eigenvectors $(2, 1)$ and $(2, -1)$.",
    "Two questions on $\\mathbf x(t)$.",
    [("Write $\\mathbf x(0) = c_1(2, 1) + c_2(2, -1)$. What is $c_1$?",
      num(c1, 0.001, [("swap", c2, 0.001)], label="c₁"),
      fb("$2c_1 + 2c_2 = 6$ and $c_1 - c_2 = 1$ give $c_1 = 2$.",
         "Solve the two equations for $c_1$ and $c_2$.",
         {"swap": "You gave $c_2 = 1$. Adding $c_1 + c_2 = 3$ to $c_1 - c_2 = 1$ gives $c_1 = 2$."})),
     ("What is $x_1(0.5)$, the first component at $t = 0.5$? Give it to 2 decimal places.",
      num(r(x1_half, 4), 0.005, [("swap-rates", r(x1_swap, 4), 0.005), ("no-vector", r(x1_novec, 4), 0.005)], label="x₁(0.5)"),
      fb("$x_1(t) = 4e^{3t} + 2e^{-t}$, so $x_1(0.5) = 19.14$.",
         "Build $\\mathbf x(t) = c_1e^{3t}(2, 1) + c_2e^{-t}(2, -1)$ and read the first entry.",
         {"swap-rates": "You paired $e^{3t}$ with the second eigenvector, giving 11.39. Each eigenvalue grows its own vector.",
          "no-vector": "You dropped the eigenvector entries, giving 9.57. Each term carries the first entry, 2."}))],
    "$2c_1 + 2c_2 = 6$ and $c_1 - c_2 = 1$ give $c_1 = 2$ and $c_2 = 1$. "
    "So $\\mathbf x(t) = 2e^{3t}(2, 1) + e^{-t}(2, -1)$. "
    "At $t = 0.5$, $x_1 = 4e^{1.5} + 2e^{-0.5} = 19.14$."))

# odes L3 (l11, l12): trace, determinant and the turn
items.append(item(
    "e-spiral-turn", 3, ["de-systems"], ["trace-determinant"], 120, "Which way it turns",
    "Let $\\mathbf x' = \\mathbf A\\mathbf x$ with $\\mathbf A = \\begin{pmatrix}-1&-4\\\\2&-3\\end{pmatrix}$.",
    "Which describes the origin?",
    choice([
        opt("ok", "A stable spiral, turning anticlockwise", correct=True),
        opt("clockwise", "A stable spiral, turning clockwise",
            "You guessed the turn. At $(1, 0)$ the velocity is $\\mathbf A(1, 0) = (-1, 2)$, upwards, so it turns anticlockwise."),
        opt("node", "A stable node",
            "You saw $\\tau < 0$ and $\\Delta > 0$ and stopped. $\\tau^2 - 4\\Delta = -28 < 0$ makes it a spiral."),
        opt("centre", "A centre",
            "A centre needs $\\tau = 0$. Here $\\tau = -4$, so paths spiral in."),
        opt("unstable", "An unstable spiral, turning anticlockwise",
            "You read the sign of $\\tau$ the wrong way. The real part is $\\tfrac{\\tau}{2} = -2 < 0$.")]),
    fb("$\\tau = -4$, $\\Delta = 11$ and $\\tau^2 - 4\\Delta = -28$: a stable spiral, turning anticlockwise.",
       "Find $\\tau$ and $\\Delta$, then read the turn from one velocity."),
    "$\\tau = -4$ and $\\Delta = 11$, so $\\tau^2 - 4\\Delta = -28 < 0$ and the eigenvalues are $-2 \\pm i\\sqrt7$. "
    "The real part is negative, so paths spiral in. "
    "At $(1, 0)$ the velocity is $(-1, 2)$, so the turn is anticlockwise."))

# odes L4 (l16): two Euler steps by hand
h = 0.25
y1 = 1 + h * (1 - 0 ** 2)
y2 = y1 + h * (y1 - 0.25 ** 2)
y_one = 1 + 0.5 * 1
y_stale = y1 + h * (y1 - 0)
y_exact = 0.25 + 1 + 2 - math.exp(0.5)
items.append(item(
    "e-euler-by-hand", 3, ["de-numeric"], ["euler-steps"], 120, "Two Euler steps",
    "Take $y' = y - t^2$ with $y(0) = 1$, and Euler's method with $h = 0.25$.",
    "What value does Euler give for $y(0.5)$, after two steps?",
    num(y2, 0.0005, [("one-step", y_one, 0.0005), ("stale-t", y_stale, 0.0005)], label="y₂"),
    fb("$y_1 = 1.25$ and $y_2 = 1.25 + 0.25(1.25 - 0.0625) = 1.546875$.",
       "Apply $y_{n+1} = y_n + hf(t_n, y_n)$ twice, updating $t$.",
       {"one-step": "You took one step of 0.5, giving 1.5. The question asks for two steps of 0.25.",
        "stale-t": "You kept $t = 0$ in the second slope, giving 1.5625. At the second step $t_1 = 0.25$."}),
    "Step one: $y_1 = 1 + 0.25(1 - 0) = 1.25$. "
    "Step two uses $t_1 = 0.25$: $y_2 = 1.25 + 0.25(1.25 - 0.0625) = 1.546875$. "
    "The exact value is $3.25 - e^{0.5} = 1.6013$, so the error is about 0.054."))

# ================================================================ difficulty 4
# complex L3 (l11): a real integral by residues
pole = complex(-3, 2)
res_up = 1 / (2 * pole + 6)
I_real = (2j * PI * res_up).real
items.append(parts(
    "e-upper-pole", 4, ["cz-contour"], ["real-integral"], 210, "A real integral from one pole",
    "We find $I = \\int_{-\\infty}^{\\infty} \\tfrac{dx}{x^2 + 6x + 13}$ by closing with the upper semicircle. "
    "The denominator has degree 2 above the numerator and no real zeros, so the arc's integral tends to 0.",
    "Two questions on the residue and the integral.",
    [("The residue at the pole in the upper half-plane is $ci$. What is $c$?",
      num(res_up.imag, 0.001, [("no-i", -res_up.imag, 0.001)], label="c"),
      fb("At $-3 + 2i$ the residue is $\\tfrac{1}{2z + 6} = \\tfrac{1}{4i} = -\\tfrac{i}{4}$.",
         "Use $\\tfrac{p(a)}{q'(a)}$ at the simple pole $-3 + 2i$.",
         {"no-i": "You wrote $\\tfrac{1}{4i}$ as $\\tfrac{i}{4}$. Multiplying top and bottom by $i$ gives $-\\tfrac{i}{4}$."})),
     ("What is $I$? Give it to 3 decimal places.",
      num(r(I_real, 4), 0.0005, [("both", 0, 0.0005), ("no-2pi", 0.25, 0.0005), ("lower", -r(I_real, 4), 0.0005)], label="I"),
      fb("$I = 2\\pi i \\cdot (-\\tfrac{i}{4}) = \\tfrac{\\pi}{2} \\approx 1.571$.",
         "Multiply the upper residue by $2\\pi i$.",
         {"both": "You added both residues. Only the pole inside the upper semicircle counts, at $-3 + 2i$.",
          "no-2pi": "You stopped at the residue. The integral is $2\\pi i$ times it.",
          "lower": "You used the lower pole $-3 - 2i$. Closing upwards encloses only $-3 + 2i$."}))],
    "The poles are $-3 \\pm 2i$, and only $-3 + 2i$ lies in the upper half-plane. "
    "There the residue is $\\tfrac{1}{2z + 6} = \\tfrac{1}{4i} = -\\tfrac{i}{4}$. "
    "So $I = 2\\pi i \\cdot (-\\tfrac{i}{4}) = \\tfrac{\\pi}{2}$, and completing the square to $(x + 3)^2 + 4$ confirms it."))

# complex L3 (l10): Cauchy's formula for a second derivative
c_cif = E
items.append(item(
    "e-third-power-pole", 4, ["cz-contour"], ["cauchy-formula"], 180, "A pole of order three",
    "Let $\\gamma$ be the circle $|z| = 2$, once anticlockwise. "
    "$e^z$ is analytic on and inside $\\gamma$, and the point 1 lies inside.",
    "$\\oint_\\gamma \\tfrac{e^z}{(z - 1)^3}\\,dz = c\\pi i$. What is $c$? Give it to 3 decimal places.",
    num(r(c_cif, 4), 0.0005, [("no-fact", r(2 * E, 4), 0.0005), ("three-fact", r(E / 3, 4), 0.0005)], label="c"),
    fb("$\\tfrac{2\\pi i}{2!}f''(1) = \\pi i e$, so $c = e \\approx 2.718$.",
       "Use Cauchy's formula for a derivative, with $k + 1 = 3$.",
       {"no-fact": "You left out the $k!$, giving $2e$. With $k = 2$, divide by $2! = 2$.",
        "three-fact": "You used $3!$, giving $\\tfrac{e}{3}$. The power 3 is $k + 1$, so $k = 2$ and $k! = 2$."}),
    "Cauchy's formula with $k = 2$ gives $\\oint \\tfrac{f(z)}{(z - 1)^3}\\,dz = \\tfrac{2\\pi i}{2!}f''(1)$. "
    "For $f = e^z$, $f''(1) = e$. "
    "So the integral is $\\pi i e$, and $c = e \\approx 2.7183$."))

# complex L3 (l13): why the call is damped
items.append(item(
    "e-damped-call", 4, ["cz-fourier"], ["damping-factor"], 180, "Why the call is damped",
    "In Fourier pricing with no dividends, the call price $C(k)$ at log strike $k$ is damped to $c(k) = e^{\\alpha k}C(k)$ before transforming.",
    "Why damp, and what does $\\alpha$ need?",
    choice([
        opt("ok", "$C(k) \\to S_0$ as $k \\to -\\infty$, so $C$ has no transform; $c$ has one for $\\alpha > 0$ with $E[S_T^{\\alpha + 1}]$ finite.",
            correct=True),
        opt("fitted", "$\\alpha$ is fitted to market prices, since the price changes with $\\alpha$.",
            "You treated $\\alpha$ as a model input. With $E[S_T^{\\alpha + 1}]$ finite, every $\\alpha > 0$ gives the same price."),
        opt("zero", "Any $\\alpha \\ge 0$ works, including $\\alpha = 0$.",
            "You allowed no damping. At $\\alpha = 0$, $c(k) = C(k)$ tends to $S_0$, so its transform does not exist."),
        opt("phi", "Damping is needed because $\\varphi$ may not exist.",
            "You mixed up the call and the law. $\\varphi(u) = E[e^{iuX}]$ exists for every $X$, since $|e^{iuX}| = 1$."),
        opt("moments", "Any $\\alpha > 0$ works, whatever the moments of $S_T$.",
            "You dropped the moment condition. The transform needs $E[S_T^{\\alpha + 1}] < \\infty$, so heavy right tails limit $\\alpha$.")]),
    fb("The left tail of $C$ needs killing, and the moment condition keeps the right tail in check.",
       "Ask what $C(k)$ does as the strike falls to 0."),
    "As $k \\to -\\infty$ the call tends to $S_0$, so $C(k)$ has no Fourier transform. "
    "The factor $e^{\\alpha k}$ with $\\alpha > 0$ kills that left tail. "
    "The transform also needs $E[S_T^{\\alpha + 1}]$ finite, and then the price does not depend on $\\alpha$."))

# vector-calc L3 (l12): Stokes on a hemisphere
items.append(parts(
    "e-hemisphere-curl", 4, ["vk-theorems", "vk-surface"], ["stokes"], 210, "The curl through a dome",
    "Let $\\mathbf F = (z - y,\\ x + z,\\ xy)$, smooth everywhere. "
    "$S$ is the upper half of the unit sphere with outward normal. "
    "Its boundary is the unit circle in $z = 0$, anticlockwise seen from above.",
    "Two questions on the flux of $\\nabla \\times \\mathbf F$.",
    [("What is $\\iint_S (\\nabla \\times \\mathbf F) \\cdot \\mathbf n\\,dS$? Give it to 3 decimal places.",
      num(r(2 * PI, 4), 0.001, [("closed", 0, 0.001), ("area", r(4 * PI, 4), 0.001)], label="Flux"),
      fb("By Stokes's theorem it equals $\\oint_C \\mathbf F \\cdot d\\mathbf r = 2\\pi \\approx 6.283$.",
         "Replace the flux of the curl by the circulation round the boundary."
         ,
         {"closed": "You used the rule for a closed surface. $S$ has a boundary, so Stokes's theorem gives the circulation round it.",
          "area": "You multiplied the curl's third entry, 2, by the dome's area $2\\pi$. On the dome the normal is not $\\mathbf k$."})),
     ("Close $S$ with the flat unit disc in $z = 0$, normal $-\\mathbf k$. What is the outward flux of $\\nabla \\times \\mathbf F$ through the closed surface?",
      num(0, 0.001, [("double", r(4 * PI, 4), 0.001)], label="Flux"),
      fb("The disc gives $-2\\pi$, which cancels the dome's $2\\pi$.",
         "Find the disc's flux with the outward normal $-\\mathbf k$."
         ,
         {"double": "You gave the disc the normal $+\\mathbf k$. Outward on the base is $-\\mathbf k$, which cancels the dome."}))],
    "Stokes's theorem turns the flux of the curl into $\\oint_C \\mathbf F \\cdot d\\mathbf r$. "
    "On $z = 0$ this is $\\oint -y\\,dx + x\\,dy = 2 \\times \\pi = 2\\pi$. "
    "A closed surface gives 0, since $\\nabla \\cdot (\\nabla \\times \\mathbf F) = 0$ and $\\mathbf F$ is smooth inside."))

# odes L3 (l13): linearising with crowding
x_eq, y_eq = 2, 1
J = [[4 - 2 * x_eq - 2 * y_eq, -2 * x_eq], [y_eq, x_eq - 2]]
detJ = J[0][0] * J[1][1] - J[0][1] * J[1][0]
trJ = J[0][0] + J[1][1]
items.append(parts(
    "e-crowded-prey", 4, ["de-systems"], ["linearise"], 240, "Prey that crowd",
    "Take $x' = x(4 - x - 2y)$ and $y' = y(x - 2)$, with $x, y > 0$.",
    "Three questions on the equilibrium with $x, y > 0$.",
    [("What is $y$ at that equilibrium?",
      num(y_eq, 0.001, [("crowd", 2, 0.001)], label="y"),
      fb("$y' = 0$ forces $x = 2$, and then $4 - 2 - 2y = 0$ gives $y = 1$.",
         "Use the second equation first."
         ,
         {"crowd": "You dropped $x$ from $4 - x - 2y = 0$. The second equation forces $x = 2$, so $y = 1$."})),
     ("What is $\\det\\mathbf J$ there?",
      num(detJ, 0.001, [("sign", -detJ, 0.001), ("trace", trJ, 0.001)], label="det J"),
      fb("$\\mathbf J = \\begin{pmatrix}-2&-4\\\\1&0\\end{pmatrix}$, so $\\det\\mathbf J = 0 + 4 = 4$.",
         "Differentiate each right-hand side in $x$ and in $y$, then evaluate at $(2, 1)$.",
         {"sign": "You computed $ad + bc$. The determinant is $(-2)(0) - (-4)(1) = 4$.",
          "trace": "You gave the trace, $-2$. The determinant is $ad - bc$."})),
     ("What does the linearisation tell us about the true system?",
      choice([
          opt("ok", "It is a stable spiral, and the true system spirals in near $(2, 1)$ too.", correct=True),
          opt("centre", "It is a centre, so nearby orbits close.",
              "You remembered predator and prey without crowding. Here $\\tau = -2 \\ne 0$, so it is not a centre."),
          opt("decides-nothing", "It is a stable spiral, but that decides nothing for the true system.",
              "That caution is for a centre or a zero eigenvalue. A spiral with nonzero real part carries over."),
          opt("saddle", "It is a saddle.",
              "A saddle needs $\\det\\mathbf J < 0$. Here it is 4.")]),
      fb("$\\tau = -2$ and $\\tau^2 - 4\\Delta = -12$: a stable spiral, which the true system shares.",
         "Classify by $\\tau$ and $\\Delta$, then ask whether the case is one we can trust."))],
    "$y' = 0$ with $y > 0$ needs $x = 2$, and then $x' = 0$ needs $y = 1$. "
    "There $\\tau = -2$, $\\Delta = 4$ and $\\tau^2 - 4\\Delta = -12$, so the eigenvalues are $-1 \\pm i\\sqrt3$. "
    "Their real part is not 0, so the spiral of the linearisation is trusted near $(2, 1)$."))

# odes L4 (l15): solving with the transform
y_lap = lambda t: 2 * math.exp(-t) - math.exp(-5 * t)
y_swap = lambda t: math.exp(-t) + 2 * math.exp(-5 * t)
items.append(parts(
    "e-laplace-rebound", 4, ["de-laplace"], ["laplace-ivp"], 270, "Starting values inside the transform",
    "Take $y'' + 6y' + 5y = 0$ with $y(0) = 1$ and $y'(0) = 3$. We solve it with the Laplace transform, $Y = \\mathcal{L}\\{y\\}$.",
    "Two questions on the solution.",
    [("Put the solution in order. Move the two flawed lines to Left out.",
      {"kind": "order", "lines": [
          line("k1", "Transform: $s^2Y - s - 3 + 6(sY - 1) + 5Y = 0$."),
          line("k2", "Collect: $(s^2 + 6s + 5)Y = s + 9$."),
          line("k3", "Factor: $Y = \\tfrac{s + 9}{(s + 1)(s + 5)}$."),
          line("k4", "Partial fractions: $Y = \\tfrac{2}{s + 1} - \\tfrac{1}{s + 5}$."),
          line("k5", "Invert by the table: $y = 2e^{-t} - e^{-5t}$."),
          line("e1", "Transform: $s^2Y - 3s - 1 + 6(sY - 1) + 5Y = 0$.",
               "You swapped the starting values. $\\mathcal{L}\\{y''\\} = s^2Y - sy(0) - y'(0)$, so $s$ goes with $y(0) = 1$."),
          line("e2", "Invert by the table: $y = 2e^{t} - e^{5t}$.",
               "You read the pole $s = -1$ as $e^{t}$. A term $\\tfrac{1}{s - p}$ inverts to $e^{pt}$, so $\\tfrac{1}{s + 1}$ gives $e^{-t}$.")],
       "answer": ["k1", "k2", "k3", "k4", "k5"], "distractors": ["e1", "e2"]},
      fb("Transform, collect, factor, split, invert: no constants are left to fit.",
         "Start from $\\mathcal{L}\\{y''\\} = s^2Y - sy(0) - y'(0)$.")),
     ("What is $y(1)$? Give it to 3 decimal places.",
      num(r(y_lap(1), 4), 0.0005, [("swapped", r(y_swap(1), 4), 0.0005)], label="y(1)"),
      fb("$y(1) = 2e^{-1} - e^{-5} = 0.7358 - 0.0067 = 0.7290$.",
         "Put $t = 1$ into $2e^{-t} - e^{-5t}$.",
         {"swapped": "You paired $s$ with $y'(0)$ in $\\mathcal{L}\\{y''\\}$, which gives $e^{-t} + 2e^{-5t}$ and 0.3814. The $s$ goes with $y(0)$."}))],
    "The derivative rules carry $y(0) = 1$ and $y'(0) = 3$ into the algebra, so no constants remain to fit. "
    "Cover-up gives 2 at $s = -1$ and $-1$ at $s = -5$. "
    "So $y = 2e^{-t} - e^{-5t}$, and $y(1) = 0.7358 - 0.0067 = 0.7290$."))

# ================================================================ difficulty 5
# complex L3 (l11): the semicircle argument
items.append(item(
    "e-semicircle-proof", 5, ["cz-contour"], ["semicircle-proof"], 360, "Why the arc vanishes",
    "Let $p$ and $q$ be polynomials with $\\deg q \\ge \\deg p + 2$, and let $q$ have no real zeros. "
    "We prove $\\int_{-\\infty}^{\\infty} \\tfrac{p(x)}{q(x)}\\,dx = 2\\pi i \\sum_{\\operatorname{Im} a > 0} \\operatorname{Res}_a \\tfrac pq$.",
    "Put the proof in order. Move the two flawed lines to Left out.",
    {"kind": "order", "lines": [
        line("k1", "Take $R$ larger than every $|a|$ with $q(a) = 0$. Let $\\gamma_R$ run along $[-R, R]$, then round the upper semicircle $C_R$."),
        line("k2", "Inside $\\gamma_R$, $\\tfrac pq$ is analytic except at the zeros of $q$ with $\\operatorname{Im} a > 0$, and all of them lie inside."),
        line("k3", "The residue theorem gives $\\int_{-R}^{R} \\tfrac pq\\,dx + \\int_{C_R} \\tfrac pq\\,dz = 2\\pi i \\sum \\operatorname{Res}_a \\tfrac pq$."),
        line("k4", "Since $\\deg q \\ge \\deg p + 2$, there is $M$ with $\\left|\\tfrac{p(z)}{q(z)}\\right| \\le \\tfrac{M}{R^2}$ on $C_R$ for large $R$."),
        line("k5", "The length bound gives $\\left|\\int_{C_R} \\tfrac pq\\,dz\\right| \\le \\pi R \\cdot \\tfrac{M}{R^2} = \\tfrac{\\pi M}{R} \\to 0$."),
        line("k6", "The same bound makes the real integral converge, so letting $R \\to \\infty$ proves the claim."),
        line("e1", "$\\int_{C_R} \\tfrac pq\\,dz = 0$, since $\\tfrac pq$ is analytic on $C_R$.",
             "Being analytic on a path does not make its integral 0. Cauchy's theorem needs a closed path with nothing singular inside."),
        line("e2", "Since $\\deg q \\ge \\deg p + 1$, $\\left|\\tfrac pq\\right| \\le \\tfrac MR$ on $C_R$, which is enough.",
             "One degree is not enough. The bound $\\pi R \\cdot \\tfrac MR = \\pi M$ does not tend to 0.")],
     "answer": ["k1", "k2", "k3", "k4", "k5", "k6"], "distractors": ["e1", "e2"]},
    fb("Close the path, apply the residue theorem, bound the arc by its length, then let $R$ grow.",
       "Close the path, apply the residue theorem, then bound the arc."),
    "On the half-disc the residue theorem holds for every large $R$. "
    "Two degrees of decay make the arc's integral at most $\\tfrac{\\pi M}{R}$, which tends to 0. "
    "Letting $R \\to \\infty$ leaves the real integral equal to $2\\pi i$ times the upper residues."))

# vector-calc L2 (l6): a vortex inside a square
circ_sq = 2 * PI
green_part = 3 * 16 - 0
items.append(parts(
    "e-vortex-square", 5, ["vk-theorems", "vk-fields"], ["green-with-hole"], 360, "A vortex inside a square",
    "Let $\\mathbf F = \\tfrac{(-y,\\ x)}{x^2 + y^2}$, defined for $(x, y) \\ne (0, 0)$. Away from the origin its scalar curl is 0. "
    "$S$ is the square with corners $(\\pm 2, \\pm 2)$, anticlockwise.",
    "Three questions on circulation round loops.",
    [("What is $\\oint_S \\mathbf F \\cdot d\\mathbf r$? Give it to 3 decimal places.",
      num(r(circ_sq, 4), 0.001, [("green", 0, 0.001)], label="Circulation"),
      fb("It equals the circulation round a small circle about 0, which is $2\\pi \\approx 6.283$.",
         "Apply Green's theorem between the square and a small circle about the origin.",
         {"green": "You applied Green's theorem across the origin. $\\mathbf F$ is undefined there, so the theorem does not apply on the square."})),
     ("Let $T$ be the circle of radius 1 about $(4, 1)$, anticlockwise. What is $\\oint_T \\mathbf F \\cdot d\\mathbf r$?",
      num(0, 0.001, [("always", r(circ_sq, 4), 0.001)], label="Circulation"),
      fb("The disc misses the origin, so $\\mathbf F$ is smooth on it and Green's theorem gives 0.",
         "Check whether the origin is inside $T$.",
         {"always": "You gave every loop $2\\pi$. The origin is $\\sqrt{17}$ from $(4, 1)$, outside $T$, so the answer is 0."})),
     ("Now take $\\mathbf G = \\mathbf F + (y^2,\\ 3x)$. What is $\\oint_S \\mathbf G \\cdot d\\mathbf r$? Give it to 2 decimal places.",
      num(r(green_part + circ_sq, 4), 0.005, [("no-vortex", green_part, 0.005), ("sign", r(circ_sq - green_part, 4), 0.005)],
          label="Circulation"),
      fb("The vortex gives $2\\pi$ and the smooth part gives 48, so the total is $48 + 2\\pi \\approx 54.28$.",
         "Split $\\mathbf G$ into the vortex and a smooth field.",
         {"no-vortex": "You dropped the vortex. Its $2\\pi$ adds to Green's term for the smooth part.",
          "sign": "You used $P_y - Q_x$ for the smooth part. Green's theorem integrates $Q_x - P_y = 3 - 2y$."}))],
    "Between the square and a small circle about 0 the curl is 0, so both circulations are $2\\pi$. "
    "A loop whose disc misses the origin gives 0. "
    "The smooth part $(y^2, 3x)$ has $Q_x - P_y = 3 - 2y$, which integrates to 48 over the square."))

# odes L4 (l16, l17): a stiff pull
lam = 80
h_eu = 2 / lam
h_rk = 2.7853 / lam
h_try = 0.03
amp = 1 - lam * h_try
items.append(parts(
    "e-stiff-steps", 5, ["de-numeric"], ["stiff-stability"], 360, "Step sizes on a stiff pull",
    "Take $y' = -80(y - \\cos t)$. Errors near the solution obey $e' = -80e$, the test equation with $\\lambda = 80$. "
    "RK4 is stable on that test equation when $0 < h\\lambda < 2.7853$.",
    "Three questions on the step size $h$.",
    [("What is the largest $h$ for which Euler is stable here?",
      num(h_eu, 0.0005, [("one-over", 1 / lam, 0.0005), ("rk4", r(h_rk, 4), 0.0005)], placeholder="a decimal", label="h"),
      fb("Euler multiplies errors by $1 - 80h$, which stays in $(-1, 1)$ for $h < 0.025$.",
         "Find when $|1 - 80h| < 1$.",
         {"one-over": "You took $h < \\tfrac{1}{\\lambda} = 0.0125$. The factor $1 - 80h$ stays inside $(-1, 1)$ up to $h = \\tfrac{2}{80}$.",
          "rk4": "That is RK4's limit. Euler's is $\\tfrac{2}{\\lambda} = 0.025$, which is smaller."})),
     ("What is the largest stable $h$ for RK4? Give it to 4 decimal places.",
      num(r(h_rk, 4), 0.0002, [("euler", h_eu, 0.0002), ("order", 4 * h_eu, 0.0002)], placeholder="a decimal", label="h"),
      fb("$h < \\tfrac{2.7853}{80} = 0.0348$.",
         "Divide RK4's interval end by $\\lambda$.",
         {"euler": "That is Euler's limit. RK4's interval reaches $h\\lambda = 2.7853$.",
          "order": "You scaled Euler's limit by the order 4, giving 0.1. The stability limit does not grow with the order like that."})),
     ("With $h = 0.03$, Euler multiplies each error by what factor per step?",
      num(r(amp, 6), 0.001, [("abs", r(-amp, 6), 0.001), ("no-one", r(-lam * h_try, 6), 0.001)], label="Factor"),
      fb("$1 - 80 \\times 0.03 = -1.4$, so errors flip sign and grow by 40% each step.",
         "Euler's factor on $e' = -\\lambda e$ is $1 - h\\lambda$.",
         {"abs": "You dropped the sign. $1 - 2.4 = -1.4$, so errors also flip each step.",
          "no-one": "You left out the 1. Euler's factor on $e' = -\\lambda e$ is $1 - h\\lambda$."}))],
    "On $e' = -80e$, Euler multiplies the error by $1 - 80h$ each step, so it is stable only for $h < 0.025$. "
    "At $h = 0.03$ that factor is $-1.4$, so errors flip sign and grow, while RK4 is still stable. "
    "RK4 is stable up to $h = 0.0348$; higher order raises the limit a little but does not remove it."))

order = {2: [], 3: [], 4: [], 5: []}
for it in items:
    order[it["difficulty"]].append(it)
exam = {
    "id": "topic-1.11", "topic": "1.11", "name": "Complex numbers, vector calculus and differential equations",
    "minutes": 100, "pass": 0.7,
    "skills": {"cz-arith": "Complex arithmetic", "cz-polar": "The polar form and Euler’s formula",
               "cz-functions": "Complex functions", "cz-contour": "Contour integrals and residues",
               "cz-fourier": "Fourier transforms",
               "vk-fields": "Vector fields", "vk-line": "Line integrals", "vk-surface": "Surface integrals",
               "vk-theorems": "Green, Stokes and divergence",
               "de-first": "First-order equations", "de-second": "Second-order linear equations",
               "de-systems": "Systems and stability", "de-laplace": "The Laplace transform",
               "de-numeric": "Numerical solution"},
    "items": order[2] + order[3] + order[4] + order[5],
}
with open(OUT, "w", encoding="utf8") as f:
    json.dump(exam, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("wrote", os.path.normpath(OUT), len(exam["items"]), "items, pace", sum(i["pace"] for i in exam["items"]), "s",
      {k: len(v) for k, v in order.items()})
