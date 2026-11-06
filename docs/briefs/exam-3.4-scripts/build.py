"""Build app/content/exams/topic-3.4.json (topic 3.4, Pure mathematics: algebra L1 to L4 and topology L1 to L3).

Route A for every key: the closed forms and small computations below. check_numbers.py recomputes each value by a
second route (brute force over the finite groups, rings and spaces, numerical maxima and integrals, iterates) and
asserts it at its path in the written file. Run from anywhere: python3 docs/briefs/exam-3.4-scripts/build.py
Notation follows the algebra and topology lessons: products read right to left, e for the identity, ord(g), |G|,
left cosets g + H, Z_n and Z_n^x, phi for a homomorphism (Euler's function named as such), closure overline{A},
interior A^circ, boundary partial A, tau for a topology, B(x, r), d_1, d_2, d_infty, a contraction T with constant q.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-3.4.json')


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


def line(id, text, why=None):
    d = {"id": id, "text": text}
    if why:
        d["why"] = why
    return d


def cell(answer, wrong=()):
    c = {"edit": True, "answer": answer, "tol": {"abs": 0}}
    if wrong:
        c["wrong"] = [{"id": i, "value": v, "tol": {"abs": 0}} for i, v in wrong]
    return c


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
# algebra L1 (l4) with L2 (l6): order of 15 in Z_36, then the index of <15>
n36, a15 = 36, 15
ord15 = n36 // math.gcd(a15, n36)
idx15 = n36 // ord15
items.append(parts(
    "e-order-fifteen", 2, ["ag-groups", "ag-cosets"], ["element-order"], 90, "The order of 15 modulo 36",
    r"Work in $\mathbb{Z}_{36}$ under addition. The order of $a$ is the least $k \ge 1$ with $ka \equiv 0 \pmod{36}$.",
    r"Two questions on $H = \langle 15 \rangle$.",
    [(r"What is $\operatorname{ord}(15)$ in $\mathbb{Z}_{36}$?",
      num(ord15, 0, [("gcd", math.gcd(a15, n36), 0), ("lcm", a15 * n36 // math.gcd(a15, n36), 0)],
          placeholder="a whole number", label="Order"),
      fb(r"$12 \times 15 = 180 = 5 \times 36$, and no smaller multiple of 15 is a multiple of 36.",
         r"Find the least $k$ with $36 \mid 15k$.",
         {"gcd": r"You gave $\gcd(15, 36) = 3$. The order is $\tfrac{36}{3} = 12$.",
          "lcm": r"You gave $\operatorname{lcm}(15, 36) = 180$, the first multiple of 15 that is $\equiv 0$. The order counts the copies: $180 = 12 \times 15$."})),
     (r"How many cosets $a + H$ does $H = \langle 15 \rangle$ have in $\mathbb{Z}_{36}$?",
      num(idx15, 0, [("order", ord15, 0)], placeholder="a whole number", label="Cosets"),
      fb(r"$|H| = 12$, so $[\mathbb{Z}_{36} : H] = \tfrac{36}{12} = 3$.",
         r"The cosets split $\mathbb{Z}_{36}$ into pieces of size $|H|$.",
         {"order": r"You gave $|H| = 12$, the size of each coset. The number of cosets is $\tfrac{36}{12}$."}))],
    r"$36 \mid 15k$ means $12 \mid 5k$, so $12 \mid k$, since $\gcd(5, 12) = 1$. "
    r"So $H = \langle 15 \rangle$ has 12 elements, the multiples of 3. "
    r"Its cosets $H$, $1 + H$ and $2 + H$ split the 36 residues into 3 pieces of 12."))

# algebra L2 (l8): order from a bottom row
sigma_row = [3, 5, 1, 2, 6, 4]
items.append(item(
    "e-cycles-bottom-row", 2, ["ag-perm"], ["permutation-order"], 60, "A permutation from its bottom row",
    r"A permutation $\sigma$ of $\{1, \dots, 6\}$ has bottom row $3, 5, 1, 2, 6, 4$. So $\sigma(1) = 3$, $\sigma(2) = 5$, and so on.",
    r"What is the order of $\sigma$?",
    num(4, 0, [("product", 8, 0), ("sum", 6, 0)], placeholder="a whole number", label="Order"),
    fb(r"$\sigma = (1\,3)(2\,5\,6\,4)$, and $\operatorname{lcm}(2, 4) = 4$.",
       r"Follow 1 until it returns, then start again at the first point not yet used.",
       {"product": r"You multiplied the cycle lengths, $2 \times 4 = 8$. The order is their lcm, 4.",
        "sum": r"You added the cycle lengths. That counts the points moved, not the order."}),
    r"Following each point gives $\sigma = (1\,3)(2\,5\,6\,4)$. "
    r"Disjoint cycles commute, so $\sigma^k = e$ exactly when both lengths divide $k$. "
    r"The least such $k$ is $\operatorname{lcm}(2, 4) = 4$."))

# algebra L4 (l14): zero divisors of Z_14
zd14 = [a for a in range(1, 14) if math.gcd(a, 14) > 1]
items.append(item(
    "e-zero-divisors-z14", 2, ["ag-rings"], ["zero-divisor"], 60, "Zero divisors modulo 14",
    r"A zero divisor is an $a \ne 0$ with $ab = 0$ for some $b \ne 0$. Work in the ring $\mathbb{Z}_{14}$.",
    r"How many zero divisors does $\mathbb{Z}_{14}$ have?",
    num(len(zd14), 0, [("evens", 6, 0), ("zero", len(zd14) + 1, 0)], placeholder="a whole number", label="Zero divisors"),
    fb(r"They are 2, 4, 6, 8, 10, 12 and 7: the non-zero $a$ with $\gcd(a, 14) > 1$.",
       r"Test $\gcd(a, 14)$ for each non-zero $a$.",
       {"evens": r"You counted the 6 even residues only. $7 \times 2 = 14 \equiv 0$, so 7 is one too.",
        "zero": r"You counted 0 as well, giving 8. A zero divisor must be non-zero."}),
    r"If $d = \gcd(a, 14) > 1$, then $a \cdot \tfrac{14}{d} \equiv 0$ with $\tfrac{14}{d} \ne 0$. "
    r"If $\gcd(a, 14) = 1$, then $a$ is a unit, and a unit is never a zero divisor. "
    r"So the 13 non-zero residues split into 6 units and 7 zero divisors."))

# topology L1 (l1): a distance with a jump is still a metric
items.append(item(
    "e-jump-metric", 2, ["tg-metric"], ["metric-axioms"], 60, "A distance with a jump",
    r"On $\mathbb{R}$ put $d(x, x) = 0$, and $d(x, y) = |x - y| + 1$ when $x \ne y$.",
    r"Is $d$ a metric?",
    choice([
        opt("ok", r"Yes: all three axioms hold, the triangle inequality included.", correct=True),
        opt("tri", r"No: the triangle inequality fails, since two hops add 1 twice.",
            r"You read the inequality the wrong way round. The two hops add 2 to the right side, and the left side gains only 1."),
        opt("zero", r"No: $d(x, x)$ should be 0, and the $+1$ spoils it.",
            r"You missed the first case. $d(x, x) = 0$ by definition, and the $+1$ applies only to distinct points."),
        opt("small", r"No: a metric needs $d(x, y) \to 0$ as $y \to x$.",
            r"You added a rule that is not an axiom. The discrete metric also jumps, and it is a metric.")]),
    fb(r"The $+1$ only ever helps the right side of the triangle inequality.",
       r"Check $d(x, x)$, symmetry, then the triangle inequality with $y$ equal to $x$, equal to $z$, or neither."),
    r"The first case gives $d(x, x) = 0$, and $d$ is symmetric and positive on distinct points. "
    r"For $x \ne z$, if $y$ equals $x$ or $z$ the triangle inequality is an equality. "
    r"Otherwise the right side is $|x - y| + |y - z| + 2 \ge |x - z| + 1 = d(x, z)$."))

# topology L1 (l4): a preimage under x^2 - 4x
fpre = lambda x: x * x - 4 * x
items.append(item(
    "e-preimage-quadratic", 2, ["tg-continuity"], ["preimage"], 60, "Pulling back an open interval",
    r"Let $f(x) = x^2 - 4x = (x - 2)^2 - 4$ on $\mathbb{R}$, and $V = (-3, 5)$, an open set.",
    r"What is $f^{-1}(V)$?",
    choice([
        opt("ok", r"$(-1, 1) \cup (3, 5)$", correct=True),
        opt("one-side", r"$(3, 5)$",
            r"You solved on one side of 2 only. Each $x$ in $(-1, 1)$ also has $f(x)$ in $(-3, 5)$."),
        opt("fill", r"$(-1, 5)$",
            r"You kept $f(x) < 5$ and dropped $f(x) > -3$. Points near 2 map below $-3$, as $f(2) = -4$."),
        opt("closed", r"$[-1, 1] \cup [3, 5]$",
            r"You kept the ends. $f(-1) = f(5) = 5$ and $f(1) = f(3) = -3$ are not in the open set $V$.")]),
    fb(r"$-3 < (x - 2)^2 - 4 < 5$ means $1 < |x - 2| < 3$: two open intervals.",
       r"Solve $1 < (x - 2)^2 < 9$ for $x$, on both sides of 2."),
    r"$f(x) \in (-3, 5)$ exactly when $1 < (x - 2)^2 < 9$, that is $1 < |x - 2| < 3$. "
    r"That is $(-1, 1) \cup (3, 5)$, a union of open intervals. "
    r"An open preimage of an open set is what continuity by open sets predicts."))

# topology L2 (l5): which family is a topology on four points
items.append(item(
    "e-four-point-topology", 2, ["tg-open"], ["topology-axioms"], 75, "A topology on four points",
    r"Take $X = \{1, 2, 3, 4\}$. A topology on $X$ holds $\varnothing$ and $X$, and is closed under unions and finite intersections.",
    r"Which family is a topology on $X$?",
    choice([
        opt("ok", r"$\{\varnothing, \{1\}, \{2\}, \{1, 2\}, \{1, 2, 3\}, X\}$", correct=True),
        opt("union", r"$\{\varnothing, \{1\}, \{2\}, \{1, 2, 3\}, X\}$",
            r"You checked intersections only. $\{1\} \cup \{2\} = \{1, 2\}$ is missing."),
        opt("inter", r"$\{\varnothing, \{1, 2\}, \{2, 3\}, \{1, 2, 3\}, X\}$",
            r"You checked unions only. $\{1, 2\} \cap \{2, 3\} = \{2\}$ is missing."),
        opt("whole", r"$\{\varnothing, \{1\}, \{1, 2\}, \{1, 2, 3\}\}$",
            r"You checked unions and intersections but not the whole space. $X$ itself must be open.")]),
    fb(r"It holds $\varnothing$ and $X$, and every union and intersection of two members is a member.",
       r"For each family, test every pair: its union and its intersection."),
    r"In $\{\varnothing, \{1\}, \{2\}, \{1, 2\}, \{1, 2, 3\}, X\}$, unions and intersections of pairs stay inside it. "
    r"The others miss $\{1, 2\}$, $\{2\}$ or $X$. "
    r"On a finite set pairs are enough, since longer unions and intersections build up from pairs."))

# ================================================================ difficulty 3
# algebra L1 (l3): an inverse by Euclid's algorithm
inv17 = pow(17, -1, 60)
items.append(item(
    "e-inverse-mod-60", 3, ["ag-groups"], ["modular-inverse"], 90, "An inverse modulo 60",
    r"$\gcd(17, 60) = 1$, so 17 is a unit modulo 60. Euclid's algorithm gives $60 = 3 \times 17 + 9$, $17 = 1 \times 9 + 8$ and $9 = 1 \times 8 + 1$.",
    r"What is $17^{-1} \bmod 60$, as a residue from 0 to 59?",
    num(inv17, 0, [("sign", 60 - inv17, 0), ("coef", 2, 0)], placeholder="a whole number", label="Inverse"),
    fb(r"$17 \times 53 = 901 = 15 \times 60 + 1$.",
       r"Run the steps backwards to write $1 = 60u + 17v$.",
       {"sign": r"You dropped the sign of $-7$. From $1 = 2 \times 60 - 7 \times 17$, the inverse is $-7 \equiv 53$.",
        "coef": r"You took the coefficient of 60 in $1 = 2 \times 60 - 7 \times 17$. The inverse is the coefficient of 17."}),
    r"Back-substituting gives $1 = 9 - 8 = 2 \times 9 - 17 = 2 \times 60 - 7 \times 17$. "
    r"So $-7 \times 17 \equiv 1$, and $-7 \equiv 53 \pmod{60}$. "
    r"The check $17 \times 53 = 901 = 15 \times 60 + 1$ confirms it."))

# algebra L1 (l4): orders and generators in Z_17^x
ord2_17 = next(k for k in range(1, 17) if pow(2, k, 17) == 1)
gens17 = sum(1 for k in range(1, 17) if math.gcd(k, 16) == 1)
items.append(parts(
    "e-units-mod-17", 3, ["ag-groups"], ["cyclic-generators"], 150, "Orders modulo 17",
    r"$\mathbb{Z}_{17}^{\times}$ is the group of the 16 non-zero residues modulo 17 under multiplication. It is cyclic.",
    r"Two questions on orders in $\mathbb{Z}_{17}^{\times}$.",
    [(r"What is $\operatorname{ord}(2)$ in $\mathbb{Z}_{17}^{\times}$?",
      num(ord2_17, 0, [("group", 16, 0), ("minus-one", 4, 0)], placeholder="a whole number", label="Order"),
      fb(r"$2^4 = 16 \equiv -1$, so $2^8 \equiv 1$, and no smaller power is 1.",
         r"List $2, 4, 8, 16, \ldots$ modulo 17 until you reach 1.",
         {"group": r"You took the order of the group, 16. An element's order only divides it: $2^8 = 256 = 15 \times 17 + 1$.",
          "minus-one": r"You stopped at $2^4 = 16$. That is $-1$, not 1, so square it once more."})),
     (r"How many elements of $\mathbb{Z}_{17}^{\times}$ generate it?",
      num(gens17, 0, [("all", 15, 0), ("primes", 6, 0)], placeholder="a whole number", label="Generators"),
      fb(r"A cyclic group of order 16 has Euler's $\varphi(16) = 8$ generators: the $g^k$ with $k$ odd.",
         r"In $\langle g \rangle$ of order 16, $g^k$ generates exactly when $\gcd(k, 16) = 1$.",
         {"all": r"You counted all 15 elements other than 1. A generator needs order 16, and 2 has order 8.",
          "primes": r"You counted the 6 prime residues. Being prime in $\mathbb{Z}$ does not fix the order: 2 has order 8."}))],
    r"$2^4 \equiv -1$ gives $\operatorname{ord}(2) = 8$, a divisor of 16. "
    r"With a generator $g$, $\operatorname{ord}(g^k) = \tfrac{16}{\gcd(k, 16)}$, so $g^k$ generates when $k$ is odd. "
    r"That gives Euler's $\varphi(16) = 8$ generators, among them 3."))

# algebra L2 (l9): which permutations are even
items.append(item(
    "e-even-or-odd", 3, ["ag-perm"], ["permutation-sign"], 120, "Even or odd",
    r"A permutation is even when it is a product of an even number of transpositions. A $k$-cycle is a product of $k - 1$ transpositions.",
    r"Which permutations of $\{1, \dots, 6\}$ are even? Select all that apply.",
    choice([
        opt("five", r"$(1\,2\,3\,4\,5)$", correct=True),
        opt("two-four", r"$(1\,2)(3\,4\,5\,6)$", correct=True),
        opt("four", r"$(1\,2\,3\,4)$",
            r"You called a 4-cycle even because 4 is even. It is 3 transpositions, so it is odd."),
        opt("three-pairs", r"$(1\,2)(3\,4)(5\,6)$",
            r"You saw pairs and called it even. It is 3 transpositions, which is odd."),
        opt("two-three", r"$(1\,4)(2\,5\,3)$",
            r"You took a 3-cycle times anything to be even. The 3-cycle is even, but the transposition makes the product odd.")],
        kind="multi"),
    fb(r"A $k$-cycle has sign $(-1)^{k-1}$, and signs multiply.",
       r"Count $k - 1$ transpositions for each $k$-cycle, then add."),
    r"$(1\,2\,3\,4\,5)$ uses 4 transpositions and $(1\,2)(3\,4\,5\,6)$ uses $1 + 3 = 4$, so both are even. "
    r"$(1\,2\,3\,4)$, $(1\,2)(3\,4)(5\,6)$ and $(1\,4)(2\,5\,3)$ each use 3. "
    r"An odd count gives an odd permutation."))

# algebra L2 (l8): a product, right to left, in a table
sig = {1: 3, 3: 5, 5: 1, 2: 4, 4: 2}           # (1 3 5)(2 4)
tau = {1: 5, 5: 1, 2: 3, 3: 4, 4: 2}           # (1 5)(2 3 4)
st = {k: sig[tau[k]] for k in range(1, 6)}     # do tau, then sigma
ts = {k: tau[sig[k]] for k in range(1, 6)}     # the slip: sigma first
rows = []
for k in range(1, 6):
    w = [(f"sigma-first-{k}", ts[k])] if ts[k] != st[k] else []
    rows.append([f"${k}$", cell(st[k], w)])
items.append(item(
    "e-product-table", 3, ["ag-perm"], ["composition"], 150, "A product of two permutations",
    r"In $S_5$ take $\sigma = (1\,3\,5)(2\,4)$ and $\tau = (1\,5)(2\,3\,4)$. Products read right to left: $\sigma\tau$ means do $\tau$, then $\sigma$.",
    r"Fill in $\sigma\tau(k)$ for each $k$.",
    {"kind": "table", "columns": ["$k$", r"$\sigma\tau(k)$"], "rows": rows},
    fb(r"$\sigma\tau = (2\,5\,3)$, with 1 and 4 fixed.",
       r"For each $k$, apply $\tau$ first, then apply $\sigma$ to the result.",
       {f"sigma-first-{k}": (f"You did $\\sigma$ first, which gives $\\tau\\sigma({k}) = {ts[k]}$. "
                             f"Do $\\tau$ first: $\\tau({k}) = {tau[k]}$, then $\\sigma({tau[k]}) = {st[k]}$.")
        for k in range(1, 6) if ts[k] != st[k]}),
    r"Doing $\tau$ then $\sigma$ sends $1 \to 5 \to 1$, $2 \to 3 \to 5$, $3 \to 4 \to 2$, $4 \to 2 \to 4$ and $5 \to 1 \to 3$. "
    r"So $\sigma\tau = (2\,5\,3)$, a 3-cycle. "
    r"Both factors are odd and the product is even, as signs multiply."))

# algebra L3 (l10, l12): kernel and image of x -> 2x from Z_18 to Z_12
ker = [x for x in range(18) if (2 * x) % 12 == 0]
im = sorted({(2 * x) % 12 for x in range(18)})
items.append(parts(
    "e-hom-z18-z12", 3, ["ag-hom"], ["kernel-image"], 150, "Doubling from 18 to 12",
    r"Define $\varphi : \mathbb{Z}_{18} \to \mathbb{Z}_{12}$ by $\varphi(x) = 2x \bmod 12$. It is well defined, since $2 \times 18 = 36 \equiv 0 \pmod{12}$, and it is a homomorphism.",
    r"Two questions on its kernel and image.",
    [(r"How many elements does $\ker\varphi$ have?",
      num(len(ker), 0, [("in-target", 2, 0), ("image", len(im), 0)], placeholder="a whole number", label="Kernel size"),
      fb(r"$2x \equiv 0 \pmod{12}$ means $6 \mid x$, so $\ker\varphi = \{0, 6, 12\}$.",
         r"Solve $2x \equiv 0 \pmod{12}$ for $x$ from 0 to 17.",
         {"in-target": r"You solved $2x \equiv 0$ for $x$ in $\mathbb{Z}_{12}$, giving 0 and 6. The kernel lives in $\mathbb{Z}_{18}$: 0, 6 and 12.",
          "image": r"You gave 6, the size of the image. The kernel is what maps to 0."})),
     (r"How many elements does $\operatorname{im}\varphi$ have?",
      num(len(im), 0, [("target-over", 12 // len(ker), 0), ("onto", 12, 0)], placeholder="a whole number", label="Image size"),
      fb(r"$\tfrac{18}{3} = 6$: the image is $\{0, 2, 4, 6, 8, 10\}$.",
         r"Use $G/\ker\varphi \cong \operatorname{im}\varphi$ and count.",
         {"target-over": r"You divided $|\mathbb{Z}_{12}|$ by the kernel's size, giving 4. The theorem divides the domain: $\tfrac{18}{3}$.",
          "onto": r"You assumed $\varphi$ is onto. Every value $2x \bmod 12$ is even, so odd residues are missed."}))],
    r"$\ker\varphi = \{0, 6, 12\}$, since $2x$ is a multiple of 12 exactly when $6 \mid x$. "
    r"By the first isomorphism theorem, $|\operatorname{im}\varphi| = \tfrac{18}{3} = 6$. "
    r"The image is the even residues, $\langle 2 \rangle$ in $\mathbb{Z}_{12}$."))

# algebra L3 (l11): the normal subgroup of S_4
items.append(item(
    "e-normal-in-s4", 3, ["ag-hom"], ["normal-subgroup"], 120, "A normal subgroup of S_4",
    r"In $S_n$, conjugation keeps cycle type: $\sigma(a\,b\,c\,d)\sigma^{-1} = (\sigma(a)\,\sigma(b)\,\sigma(c)\,\sigma(d))$, and likewise for every cycle.",
    r"Which subgroup of $S_4$ is normal?",
    choice([
        opt("ok", r"$V = \{e, (1\,2)(3\,4), (1\,3)(2\,4), (1\,4)(2\,3)\}$", correct=True),
        opt("four", r"$\{e, (1\,2\,3\,4), (1\,3)(2\,4), (1\,4\,3\,2)\}$",
            r"You took a cyclic subgroup of order 4 to be as good as $V$. Conjugating $(1\,2\,3\,4)$ by $(1\,2)$ gives $(2\,1\,3\,4)$, which is not in it."),
        opt("pair", r"$\{e, (1\,2)(3\,4)\}$",
            r"You conjugated only by elements that fix it. Conjugating by $(2\,3)$ gives $(1\,3)(2\,4)$, outside it."),
        opt("three", r"$\{e, (1\,2\,3), (1\,3\,2)\}$",
            r"You treated a subgroup of 3-cycles like the whole of $A_4$. Conjugating by $(3\,4)$ gives $(1\,2\,4)$, outside it.")]),
    fb(r"$V$ holds every product of two disjoint transpositions, so conjugation maps it to itself.",
       r"Conjugate a non-identity element of each subgroup by a transposition, and see if it stays."),
    r"Conjugation keeps cycle type, so a normal subgroup of $S_4$ must hold whole cycle types. "
    r"$V$ holds $e$ and all three products of two disjoint transpositions, so $gVg^{-1} = V$ for every $g$. "
    r"Each other subgroup holds only part of a cycle type, and one conjugation leaves it."))

# algebra L3 (l13): Euler's theorem modulo 14
p14 = pow(5, 100, 14)
items.append(item(
    "e-euler-mod-14", 3, ["ag-cosets", "ag-groups"], ["euler-theorem"], 120, "A large power modulo 14",
    r"$\gcd(5, 14) = 1$, and Euler's function gives $\varphi(14) = 6$, the order of $\mathbb{Z}_{14}^{\times}$.",
    r"What is $5^{100} \bmod 14$, as a residue from 0 to 13?",
    num(p14, 0, [("prime", pow(5, 100 % 13, 14), 0), ("mod-n", pow(5, 100 % 14, 14), 0)],
        placeholder="a whole number", label="Residue"),
    fb(r"$100 = 16 \times 6 + 4$, so $5^{100} \equiv 5^4 = 625 \equiv 9$.",
       r"Reduce the exponent modulo 6, then work out the small power.",
       {"prime": r"You used $5^{13} \equiv 1$ as if 14 were prime, which gives $5^9 \equiv 13$. Lagrange gives $5^6 \equiv 1$, since $|\mathbb{Z}_{14}^{\times}| = 6$.",
        "mod-n": r"You reduced the exponent modulo 14, which gives $5^2 = 25 \equiv 11$. Exponents reduce modulo the group's order, 6."}),
    r"By Lagrange, $g^{|G|} = e$ in the finite group $G = \mathbb{Z}_{14}^{\times}$, so $5^6 \equiv 1$. "
    r"Then $5^{100} = (5^6)^{16} \cdot 5^4 \equiv 625 = 44 \times 14 + 9 \equiv 9$. "
    r"That is Euler's theorem for $n = 14$."))

# algebra L4 (l17): a remainder over Z_7
fz7 = lambda x: (x ** 5 + 3 * x ** 2 + 2)
items.append(item(
    "e-remainder-z7", 3, ["ag-poly"], ["remainder-theorem"], 90, "A remainder over Z_7",
    r"Over the field $\mathbb{Z}_7$, divide $f(x) = x^5 + 3x^2 + 2$ by $x - 4$.",
    r"What is the remainder, as a residue from 0 to 6?",
    num(fz7(4) % 7, 0, [("minus-four", fz7(-4) % 7, 0), ("unreduced", fz7(4), 0)],
        placeholder="a whole number", label="Remainder"),
    fb(r"By the remainder theorem it is $f(4) = 4^5 + 3 \cdot 4^2 + 2 \equiv 2 + 6 + 2 \equiv 3$.",
       r"The remainder on dividing by $x - a$ is $f(a)$.",
       {"minus-four": r"You evaluated at $-4$, which gives 6. Dividing by $x - 4$ leaves $f(4)$.",
        "unreduced": r"You worked in $\mathbb{Z}$ and stopped at 1074. Reduce it modulo 7."}),
    r"Division by $x - 4$ leaves a constant $r$ with $f(x) = q(x)(x - 4) + r$. "
    r"Putting $x = 4$ gives $r = f(4)$. "
    r"Modulo 7, $4^2 \equiv 2$ and $4^3 \equiv 1$, so $f(4) \equiv 2 + 6 + 2 \equiv 3$."))

# algebra L4 (l17): irreducible over Z_3
items.append(item(
    "e-irreducible-z3", 3, ["ag-poly"], ["irreducibility"], 150, "Irreducible over Z_3",
    r"Work in $\mathbb{Z}_3[x]$. A polynomial of degree 2 or 3 over a field is reducible exactly when it has a root.",
    r"Which are irreducible over $\mathbb{Z}_3$? Select all that apply.",
    choice([
        opt("quad", r"$x^2 + x + 2$", correct=True),
        opt("cubic", r"$x^3 + 2x^2 + 1$", correct=True),
        opt("quartic", r"$x^4 + x^3 + x + 2$",
            r"You tested for roots, which settles degrees 2 and 3 only. This quartic is $(x^2 + 1)(x^2 + x + 2)$."),
        opt("root", r"$x^3 + x + 2$",
            r"You missed the root 2: $8 + 2 + 2 = 12 \equiv 0$. So $x - 2$ is a factor.")],
        kind="multi"),
    fb(r"$x^2 + x + 2$ and $x^3 + 2x^2 + 1$ have no root in $\mathbb{Z}_3$, and the root test decides degrees 2 and 3.",
       r"Evaluate each at 0, 1 and 2, and watch the degree."),
    r"At 0, 1 and 2, $x^2 + x + 2$ takes 2, 1, 2 and $x^3 + 2x^2 + 1$ takes 1, 1, 2: no roots. "
    r"$x^3 + x + 2$ vanishes at 2. "
    r"$x^4 + x^3 + x + 2$ has no root, yet it is $(x^2 + 1)(x^2 + x + 2)$: above degree 3 roots are not enough."))

# topology L1 (l3): the boundary of a half disc
items.append(item(
    "e-half-disc", 3, ["tg-open"], ["boundary"], 120, "The boundary of a half disc",
    r"In $\mathbb{R}^2$ with $d_2$, let $A = \{(x, y) : x^2 + y^2 < 1,\ y \ge 0\}$. It is the upper half of the open unit disc, with its flat edge kept.",
    r"What is $\partial A$?",
    choice([
        opt("ok", r"The arc $x^2 + y^2 = 1,\ y \ge 0$, together with the segment $[-1, 1] \times \{0\}$", correct=True),
        opt("arc", r"The arc $x^2 + y^2 = 1,\ y \ge 0$, only",
            r"You left out the flat edge because it lies in $A$. Boundary points may lie in the set: every ball round $(0, 0)$ meets $y < 0$."),
        opt("corners", r"The arc $x^2 + y^2 = 1,\ y > 0$, together with the segment $(-1, 1) \times \{0\}$",
            r"You dropped the corners $(\pm 1, 0)$. They lie in $\overline{A}$ but not in $A^\circ$, so they are boundary points."),
        opt("interior", r"$\{(x, y) : x^2 + y^2 < 1,\ y > 0\}$",
            r"That is $A^\circ$, the interior. The boundary is $\overline{A} \setminus A^\circ$.")]),
    fb(r"$\overline{A}$ is the closed half disc and $A^\circ$ is the open half with $y > 0$. Their difference is the arc and the closed diameter.",
       r"Find $\overline{A}$ and $A^\circ$, then take $\partial A = \overline{A} \setminus A^\circ$."),
    r"Every ball round a point with $y = 0$ meets $y < 0$, so no such point is interior. "
    r"The closure adds the arc $x^2 + y^2 = 1$, $y \ge 0$. "
    r"So $\partial A$ is that arc together with the segment from $(-1, 0)$ to $(1, 0)$."))

# topology L1 (l1): two metrics on functions
xpk = 1 / math.sqrt(3)
dinf = xpk - xpk ** 3
d1 = 0.5 - 0.25
items.append(parts(
    "e-two-function-metrics", 3, ["tg-metric"], ["function-metrics"], 150, "Two distances between functions",
    r"On the continuous functions on $[0, 1]$, take $d_\infty(f, g) = \max_x |f(x) - g(x)|$ and $d_1(f, g) = \int_0^1 |f(x) - g(x)|\,dx$. Let $f(x) = x$ and $g(x) = x^3$.",
    r"Two questions on the distance from $f$ to $g$.",
    [(r"What is $d_\infty(f, g)$? Give 4 decimal places.",
      num(r(dinf), 0.00005, [("ends", 0, 0.00005), ("midpoint", 0.375, 0.00005)], placeholder="a decimal",
          label="Sup distance", accept="2/(3√3) = 0.3849"),
      fb(r"$x - x^3$ peaks where $1 - 3x^2 = 0$, at $x = \tfrac{1}{\sqrt3}$, with value $\tfrac{2}{3\sqrt3} = 0.3849$.",
         r"Maximise $h(x) = x - x^3$ on $[0, 1]$.",
         {"ends": r"You compared at the ends, where $f$ and $g$ agree and the gap is 0. The gap peaks inside, at $x = \tfrac{1}{\sqrt3}$.",
          "midpoint": r"You took the gap at $x = \tfrac12$, which is 0.375. The maximum is where $1 - 3x^2 = 0$."})),
     (r"What is $d_1(f, g)$? Give 4 decimal places.",
      num(r(d1), 0.00005, [("square", r(8 / 105), 0.00005)], placeholder="a decimal", label="Integral distance"),
      fb(r"$\int_0^1 (x - x^3)\,dx = \tfrac12 - \tfrac14 = 0.25$.",
         r"Here $x - x^3 \ge 0$, so integrate it directly.",
         {"square": r"You integrated the squared gap, which gives $\tfrac{8}{105} = 0.0762$. $d_1$ integrates $|f - g|$ itself."}))],
    r"$h(x) = x - x^3$ is non-negative on $[0, 1]$, with $h'(x) = 1 - 3x^2$. "
    r"Its peak is $h(\tfrac{1}{\sqrt3}) = \tfrac{2}{3\sqrt3} = 0.3849$, and its integral is $\tfrac12 - \tfrac14 = 0.25$. "
    r"On an interval of length 1, $d_1 \le d_\infty$ always, and here $0.25 \le 0.3849$."))

# topology L2 (l7, l8): which pairs are homeomorphic
items.append(item(
    "e-homeomorphic-pairs", 3, ["tg-continuity", "tg-connected"], ["homeomorphism"], 150, "Same space or not",
    r"Each set is a subspace of $\mathbb{R}$. A homeomorphism is a continuous bijection with a continuous inverse, and it keeps connectedness and compactness.",
    r"Which pairs are homeomorphic? Select all that apply.",
    choice([
        opt("half-line", r"$(0, 1)$ and $(0, \infty)$", correct=True),
        opt("affine", r"$(0, 1)$ and $(3, 7)$", correct=True),
        opt("closed-half", r"$\mathbb{R}$ and $[0, \infty)$",
            r"You matched two unbounded sets. Removing 0 leaves $[0, \infty)$ connected, but removing any point splits $\mathbb{R}$."),
        opt("ends", r"$[0, 1]$ and $[0, 1)$",
            r"You matched intervals of the same length. $[0, 1]$ is compact and $[0, 1)$ is not."),
        opt("two-pieces", r"$(0, 1)$ and $(0, 1) \cup (2, 3)$",
            r"You matched two open sets. A homeomorphism would carry the connected $(0, 1)$ onto a disconnected set.")],
        kind="multi"),
    fb(r"$x \mapsto \tfrac{x}{1 - x}$ and $x \mapsto 3 + 4x$ are continuous bijections with continuous inverses.",
       r"Look for an invariant that differs: compactness, connectedness, or what is left after removing a point."),
    r"$x \mapsto \tfrac{x}{1 - x}$ maps $(0, 1)$ onto $(0, \infty)$ with inverse $y \mapsto \tfrac{y}{1 + y}$, and $x \mapsto 3 + 4x$ maps it onto $(3, 7)$. "
    r"$[0, 1]$ is compact and $[0, 1)$ is not, and $(0, 1) \cup (2, 3)$ is disconnected. "
    r"Removing 0 leaves $[0, \infty)$ connected, but removing any point splits $\mathbb{R}$."))

# topology L2 (l8): connected subsets of R
items.append(item(
    "e-connected-subsets", 3, ["tg-connected"], ["connected-sets"], 120, "Connected subsets of the line",
    r"Each set is a subspace of $\mathbb{R}$. A subset of $\mathbb{R}$ is connected exactly when it is an interval.",
    r"Which sets are connected? Select all that apply.",
    choice([
        opt("glued", r"$(-1, 0) \cup (0, 3)$",
            r"You saw two intervals that meet at 0. The point 0 is missing, so the set splits there."),
        opt("image", r"$f([0, 5])$, with $f$ continuous", correct=True),
        opt("rationals", r"$\mathbb{Q} \cap [0, 1]$",
            r"You saw no gaps between rationals. $\tfrac{\sqrt2}{2}$ is missing, and it splits the set into two open pieces."),
        opt("outside", r"$\{x : x^2 > 4\}$",
            r"You read one inequality as one interval. The set is $(-\infty, -2) \cup (2, \infty)$, two pieces."),
        opt("point", r"$[0, 1] \cup \{2\}$",
            r"You thought one point cannot split a set. $\{2\}$ is open in the subspace, and so is $[0, 1]$.")],
        kind="multi"),
    fb(r"A continuous image of the connected $[0, 5]$ is connected.",
       r"Ask whether each set is an interval: does it hold every point between two of its points?"),
    r"$f([0, 5])$ is connected because $[0, 5]$ is, and $(-1, 0) \cup (0, 3)$ misses 0. "
    r"The rationals miss $\tfrac{\sqrt2}{2}$, and $\{x : x^2 > 4\}$ misses $[-2, 2]$. "
    r"In $[0, 1] \cup \{2\}$ the point 2 is open on its own, which gives a separation."))

# topology L3 (l9, l10): compact subsets of the plane
items.append(item(
    "e-compact-subsets", 3, ["tg-compact"], ["compact-sets"], 120, "Compact subsets of the plane",
    r"Each set is a subset of $\mathbb{R}^2$ with $d_2$. By Heine-Borel in $\mathbb{R}^n$, a subset is compact exactly when it is closed and bounded.",
    r"Which sets are compact? Select all that apply.",
    choice([
        opt("circle", r"The unit circle $\{(x, y) : x^2 + y^2 = 1\}$", correct=True),
        opt("graph", r"The graph $\{(t, \sin t) : 0 \le t \le 2\pi\}$", correct=True),
        opt("square", r"The open square $(0, 1) \times (0, 1)$",
            r"You saw a bounded set and stopped. It is not closed: $(\tfrac1n, \tfrac1n)$ tends to $(0, 0)$, outside it."),
        opt("line", r"The line $\{(x, 2x) : x \in \mathbb{R}\}$",
            r"You saw a closed set and stopped. It is unbounded, and the balls $B(0, n)$ cover it with no finite subcover."),
        opt("points", r"$\{(\tfrac1n, 0) : n \ge 1\} \cup \{(0, 0)\}$", correct=True)],
        kind="multi"),
    fb(r"The circle, the graph and the points with their limit are closed and bounded.",
       r"Check each set for closed, then for bounded."),
    r"The circle is closed and bounded, and the graph is the image of the compact $[0, 2\pi]$ under $t \mapsto (t, \sin t)$. "
    r"The points $(\tfrac1n, 0)$ with their limit $(0, 0)$ are closed and bounded too. "
    r"The open square misses the limit $(0, 0)$ of $(\tfrac1n, \tfrac1n)$, and the line is unbounded."))

# topology L3 (l11): a log metric on (0, infinity)
items.append(item(
    "e-log-metric", 3, ["tg-complete"], ["completeness"], 120, "Complete under a log distance",
    r"On $X = (0, \infty)$ put $d(x, y) = |\ln x - \ln y|$. It is a metric, because $\ln$ is one-to-one.",
    r"Is $(X, d)$ complete?",
    choice([
        opt("ok", r"Yes: $\ln$ maps $(X, d)$ onto $\mathbb{R}$ keeping distances, and $\mathbb{R}$ is complete.", correct=True),
        opt("recip", r"No: $x_n = \tfrac1n$ is Cauchy, and its limit 0 is not in $X$.",
            r"You measured with $|x - y|$. Here $d(\tfrac1n, \tfrac1m) = |\ln m - \ln n|$, which does not shrink."),
        opt("closed", r"No: $(0, \infty)$ is not closed in $\mathbb{R}$.",
            r"You judged by the usual metric. Completeness depends on the metric, and this one stretches gaps near 0."),
        opt("bounded", r"No: $X$ is unbounded in $d$.",
            r"You linked completeness with boundedness. $\mathbb{R}$ is unbounded and complete.")]),
    fb(r"A $d$-Cauchy $(x_n)$ makes $(\ln x_n)$ Cauchy in $\mathbb{R}$, with a limit $L$. Then $x_n \to e^L$, a point of $X$.",
       r"Map each point by $\ln$ and see what $d$ becomes."),
    r"$d(x, y) = |\ln x - \ln y|$ makes $\ln$ a distance-keeping bijection from $X$ onto $\mathbb{R}$. "
    r"A $d$-Cauchy sequence has $\ln x_n \to L$, so $d(x_n, e^L) \to 0$, and $e^L > 0$ lies in $X$. "
    r"The sequence $\tfrac1n$ is not even Cauchy here."))

# ================================================================ difficulty 4
# algebra L4 (l15): which rings are fields
items.append(item(
    "e-which-fields", 4, ["ag-rings"], ["field-test"], 180, "Which rings are fields",
    r"A field is a commutative ring with $1 \ne 0$ in which every non-zero element has an inverse.",
    r"Which are fields? Select all that apply.",
    choice([
        opt("prime", r"$\mathbb{Z}_{103}$", correct=True),
        opt("root-three", r"$\mathbb{Q}(\sqrt3) = \{a + b\sqrt3 : a, b \in \mathbb{Q}\}$", correct=True),
        opt("composite", r"$\mathbb{Z}_{87}$",
            r"You took an odd number for a prime. $87 = 3 \times 29$, so 3 is a zero divisor."),
        opt("integers", r"$\mathbb{Z}$",
            r"You checked the ring axioms only. 2 has no inverse in $\mathbb{Z}$."),
        opt("matrices", r"The real $2 \times 2$ matrices",
            r"You saw that invertible matrices have inverses. The ring is not commutative, and $\begin{pmatrix}1&0\\0&0\end{pmatrix}$ has no inverse.")],
        kind="multi"),
    fb(r"103 is prime, and $(a + b\sqrt3)^{-1} = \tfrac{a - b\sqrt3}{a^2 - 3b^2}$ for $(a, b) \ne (0, 0)$.",
       r"For each ring, look for a non-zero element with no inverse, and check commutativity."),
    r"$\mathbb{Z}_n$ is a field exactly when $n$ is prime, so 103 passes and $87 = 3 \times 29$ fails. "
    r"In $\mathbb{Q}(\sqrt3)$, $a^2 - 3b^2 \ne 0$ unless $a = b = 0$, since $\sqrt3$ is irrational. "
    r"$\mathbb{Z}$ lacks $\tfrac12$, and the matrices are neither commutative nor free of zero divisors."))

# topology L3 (l10): a maximum on the circle exists, then find it
items.append(parts(
    "e-max-on-circle", 4, ["tg-compact", "tg-continuity"], ["extreme-value"], 180, "The best book on a risk budget",
    r"Positions $(x, y)$ in two assets must satisfy the risk budget $x^2 + y^2 = 1$. The expected P&L, in £ thousands, is $f(x, y) = x + 2y$.",
    r"Two questions on the best P&L.",
    [(r"Why must $f$ attain a largest value on the budget set?",
      choice([
          opt("ok", r"The circle is compact and $f$ is continuous, so $f$ of the circle is compact.", correct=True),
          opt("bounded", r"$f$ is bounded on the circle, since $|x + 2y| \le 3$ there.",
              r"You stopped at bounded. A bounded function need not attain its supremum: $x$ on $(0, 1)$ never reaches 1."),
          opt("linear", r"Every linear function has a maximum.",
              r"You forgot the domain. On all of $\mathbb{R}^2$, $x + 2y$ has no maximum."),
          opt("connected", r"The circle is connected, so $f$ takes every value between its extremes.",
              r"You used connectedness. It gives intermediate values, not a largest one.")]),
      fb(r"A continuous image of a compact set is compact, and a compact subset of $\mathbb{R}$ holds its supremum.",
         r"Ask which property of the circle survives a continuous map and forces a maximum.")),
     (r"What is the largest expected P&L, in £ thousands? Give 4 decimal places.",
      num(r(math.sqrt(5)), 0.00005, [("corner", 3, 0.00005), ("one-asset", 2, 0.00005)], placeholder="a decimal",
          label="Best P&L", accept="√5 = 2.2361"),
      fb(r"By Cauchy-Schwarz, $x + 2y \le \sqrt{1^2 + 2^2}\,\sqrt{x^2 + y^2} = \sqrt5$, with equality at $(\tfrac{1}{\sqrt5}, \tfrac{2}{\sqrt5})$.",
         r"Write $(x, y) = (\cos t, \sin t)$ and maximise $\cos t + 2\sin t$.",
         {"corner": r"You put $x = y = 1$, giving 3, which breaks the budget: $1^2 + 1^2 = 2$.",
          "one-asset": r"You put everything in the second asset. Mixing in some of the first does better."}))],
    r"The circle is compact and $f$ is continuous, so the maximum exists before we look for it. "
    r"Cauchy-Schwarz gives $x + 2y \le \sqrt5$, with equality at $(\tfrac{1}{\sqrt5}, \tfrac{2}{\sqrt5})$. "
    r"So the best P&L is $\sqrt5 = 2.2361$, about £2,236."))

# algebra L2 (l5): every subgroup of a cyclic group is cyclic
items.append(item(
    "e-cyclic-subgroups-proof", 4, ["ag-cosets"], ["subgroup-proof"], 240, "Subgroups of a cyclic group",
    r"Let $G = \langle g \rangle$ be cyclic, finite or infinite, and $H$ a subgroup with $H \ne \{e\}$. We prove $H$ is cyclic. Two lines are independent and may come in either order.",
    r"Put the proof in order. Move the two flawed lines to Left out.",
    {"kind": "order", "lines": [
        line("c1", r"$H$ holds some $g^k$ with $k \ne 0$, and so its inverse $g^{-k}$. So $H$ holds a positive power of $g$."),
        line("c2", r"Let $m$ be the least positive integer with $g^m \in H$."),
        line("c3", r"$H$ is closed under products and inverses, so $\langle g^m \rangle \subseteq H$."),
        line("c4", r"Take $h \in H$ and write $h = g^k$. Divide: $k = qm + r$ with $0 \le r < m$. Then $g^r = g^k(g^m)^{-q}$ is a product of elements of $H$, so $g^r \in H$."),
        line("c5", r"Since $m$ is least and $0 \le r < m$, $r = 0$. So $h = (g^m)^q$, and $H = \langle g^m \rangle$."),
        line("d1", r"By Lagrange, $|H|$ divides $|G|$, and a group whose order divides a cyclic group's order is cyclic.",
             r"Lagrange limits sizes, not structure, and $G$ may be infinite. $\{e, (1\,2)(3\,4), (1\,3)(2\,4), (1\,4)(2\,3)\}$ has order 4, as $\mathbb{Z}_4$ does, and is not cyclic."),
        line("d2", r"Let $m$ be the least integer with $g^m \in H$.",
             r"Without the word positive there is no least one: $H$ holds $g^{-m}$, $g^{-2m}$ and so on.")],
     "answer": ["c1", "c2", "c3", "c4", "c5"], "same": [["c3", "c4"]], "distractors": ["d1", "d2"]},
    fb(r"The least positive power of $g$ in $H$ generates $H$, by the division trick.",
       r"Choose the least positive power of $g$ in $H$, then divide any exponent by it."),
    r"A non-trivial $H$ holds a least positive power $g^m$, and closure gives $\langle g^m \rangle \subseteq H$. "
    r"Dividing any exponent $k$ by $m$ leaves $g^r \in H$ with $0 \le r < m$, so $r = 0$. "
    r"Hence $H = \langle g^m \rangle$, whatever the size of $G$."))

# topology L2 (l5, l7) with L1 (l4): where two maps into a Hausdorff space agree
items.append(item(
    "e-equaliser-closed", 4, ["tg-continuity", "tg-open"], ["hausdorff-proof"], 240, "Where two maps agree",
    r"Let $f, g : X \to Y$ be continuous maps of topological spaces, with $Y$ Hausdorff: distinct points have disjoint open sets round them. We prove $E = \{x : f(x) = g(x)\}$ is closed. Two lines may come in either order.",
    r"Put the proof in order. Move the two flawed lines to Left out.",
    {"kind": "order", "lines": [
        line("h1", r"We show $X \setminus E$ is open. Take $x$ with $f(x) \ne g(x)$."),
        line("h2", r"Since $Y$ is Hausdorff, pick disjoint open sets $U \ni f(x)$ and $V \ni g(x)$."),
        line("h3", r"$f^{-1}(U)$ is open in $X$, since $f$ is continuous."),
        line("h4", r"$g^{-1}(V)$ is open in $X$, since $g$ is continuous."),
        line("h5", r"So $W = f^{-1}(U) \cap g^{-1}(V)$ is open, as a finite intersection of open sets, and $x \in W$."),
        line("h6", r"For $w \in W$, $f(w) \in U$ and $g(w) \in V$. As $U \cap V = \varnothing$, $f(w) \ne g(w)$."),
        line("h7", r"So $W \subseteq X \setminus E$. Each point of $X \setminus E$ has such a $W$, so $X \setminus E$ is open and $E$ is closed."),
        line("d1", r"$f - g$ is continuous, and $E$ is the preimage of the closed set $\{0\}$.",
             r"You treated $Y$ as $\mathbb{R}$. A general space has no subtraction; Hausdorff is what separates $f(x)$ from $g(x)$."),
        line("d2", r"Pick an open $U$ with $f(x) \in U$ and $g(x) \notin U$. Then $W = f^{-1}(U)$ works.",
             r"You separated $f(x)$ only. A point $w$ of $f^{-1}(U)$ may still have $g(w) \in U$, so disjoint $U$ and $V$ are needed.")],
     "answer": ["h1", "h2", "h3", "h4", "h5", "h6", "h7"], "same": [["h3", "h4"]], "distractors": ["d1", "d2"]},
    fb(r"Disjoint open sets in $Y$ pull back to one open $W$ round $x$, on which $f$ and $g$ differ.",
       r"Show the complement is open: round each $x$ with $f(x) \ne g(x)$, find an open set where they still differ."),
    r"Hausdorff gives disjoint open $U \ni f(x)$ and $V \ni g(x)$. "
    r"Continuity makes $W = f^{-1}(U) \cap g^{-1}(V)$ an open set round $x$, and on it $f$ and $g$ land in disjoint sets. "
    r"So $X \setminus E$ is open; without Hausdorff, two maps from $\mathbb{R}$ to an indiscrete $\{a, b\}$ can agree on $(0, \infty)$ only."))

# algebra L3 (l12) with L2 (l7): possible image sizes
items.append(item(
    "e-image-sizes", 4, ["ag-hom", "ag-cosets"], ["first-isomorphism"], 180, "How big can the image be",
    r"Let $\varphi : G \to H$ be a homomorphism of finite groups with $|G| = 28$ and $|H| = 21$.",
    r"Which values are possible for $|\operatorname{im}\varphi|$, over all such $G$, $H$ and $\varphi$? Select all that apply.",
    choice([
        opt("one", "1", correct=True),
        opt("seven", "7", correct=True),
        opt("three", "3",
            r"You checked $3 \mid 21$ only. Since $\operatorname{im}\varphi \cong G/\ker\varphi$, its size divides 28 too."),
        opt("four", "4",
            r"You checked $4 \mid 28$ only. The image is a subgroup of $H$, so by Lagrange its size divides 21."),
        opt("onto", "21",
            r"You assumed $\varphi$ can be onto. That needs $21 \mid 28$, which fails.")],
        kind="multi"),
    fb(r"$|\operatorname{im}\varphi|$ divides both 28 and 21, so it divides 7.",
       r"The image is a subgroup of $H$, and it is a copy of a quotient of $G$."),
    r"By Lagrange $|\operatorname{im}\varphi|$ divides 21, and by $G/\ker\varphi \cong \operatorname{im}\varphi$ it divides 28. "
    r"So it divides $\gcd(28, 21) = 7$, which leaves 1 and 7. "
    r"The trivial map gives 1, and $x \mapsto 3x$ from $\mathbb{Z}_{28}$ to $\mathbb{Z}_{21}$ gives 7."))

# algebra L2 (l8): elements of order 3 in S_6
one3 = math.comb(6, 3) * 2
two3 = math.comb(6, 3) // 2 * 2 * 2
items.append(item(
    "e-order-three-s6", 4, ["ag-perm"], ["cycle-type-count"], 210, "Elements of order 3 in S_6",
    r"An element $\sigma \ne e$ of $S_6$ has order 3 exactly when each of its disjoint cycles has length 1 or 3.",
    r"How many elements of $S_6$ have order 3?",
    num(one3 + two3, 0, [("one-cycle", one3, 0), ("ordered", one3 + 2 * two3, 0)], placeholder="a whole number",
        label="Elements"),
    fb(r"There are $\binom63 \times 2 = 40$ single 3-cycles and $\tfrac12 \times 20 \times 2 \times 2 = 40$ products of two: 80 in all.",
       r"Count the single 3-cycles, then the products of two disjoint 3-cycles.",
       {"one-cycle": r"You counted the 40 single 3-cycles only. Products such as $(1\,2\,3)(4\,5\,6)$ also have order 3.",
        "ordered": r"You counted the two 3-cycles of a product in order, giving 120. $(1\,2\,3)(4\,5\,6) = (4\,5\,6)(1\,2\,3)$, so halve that part."}),
    r"A 3-cycle picks 3 of the 6 points in $\binom63 = 20$ ways and has 2 cyclic orders, giving 40. "
    r"Two disjoint 3-cycles split the 6 points into two triples in 10 ways, with 2 orders each, giving 40. "
    r"So 80 elements have order 3."))

# ================================================================ difficulty 5
# algebra L3 (l10, l12) with L1 (l4) and L4 (l17): squares modulo 11
sq11 = sorted({x * x % 11 for x in range(1, 11)})
items.append(parts(
    "e-squares-mod-11", 5, ["ag-hom", "ag-groups"], ["squaring-map"], 420, "Squares modulo 11",
    r"$G = \mathbb{Z}_{11}^{\times}$ is cyclic of order 10. Since $G$ is abelian, squaring, $\varphi(x) = x^2$, is a homomorphism $G \to G$.",
    r"Three questions on which elements are squares.",
    [(r"How many elements does $\ker\varphi$ have?",
      num(2, 0, [("one", 1, 0), ("image", len(sq11), 0)], placeholder="a whole number", label="Kernel size"),
      fb(r"$x^2 = 1$ means $(x - 1)(x + 1) = 0$, and a field has no zero divisors: $x = 1$ or $x = 10$.",
         r"Solve $x^2 \equiv 1 \pmod{11}$.",
         {"one": r"You kept only 1. $10^2 = 100 = 9 \times 11 + 1$, so $-1$ is in the kernel too.",
          "image": r"You gave 5, the size of the image. The kernel is the solutions of $x^2 = 1$."})),
     (r"How many non-zero residues modulo 11 are squares?",
      num(len(sq11), 0, [("onto", 10, 0), ("with-zero", len(sq11) + 1, 0)], placeholder="a whole number", label="Squares"),
      fb(r"$\operatorname{im}\varphi \cong G/\ker\varphi$ has $\tfrac{10}{2} = 5$ elements: 1, 3, 4, 5 and 9.",
         r"Use the first isomorphism theorem with the kernel you found.",
         {"onto": r"You assumed squaring is onto, giving 10. Its kernel has 2 elements, so it is two-to-one.",
          "with-zero": r"You counted 0 as well, giving 6. Among the non-zero residues there are 5 squares."})),
     (r"Now let $\psi(x) = x^5$. Each square $y = x^2$ has $\psi(y) = x^{10} = 1$, and $x^5 = 1$ has at most 5 roots in the field $\mathbb{Z}_{11}$. So the squares are exactly $\ker\psi$. Which of 2 and 3 is a square modulo 11?",
      choice([
          opt("three", "3 only", correct=True),
          opt("two", "2 only", r"You read $2^5 \equiv 10$ as a pass. Squares give exactly 1, and $10 \equiv -1$."),
          opt("both", "Both", r"You assumed every element is a square. Only 5 of the 10 are."),
          opt("neither", "Neither", r"You expected squares to look like squares in $\mathbb{Z}$. But $5^2 = 25 \equiv 3$.")]),
      fb(r"$3^5 = 243 = 22 \times 11 + 1$, so 3 is a square, and indeed $5^2 \equiv 3$. But $2^5 = 32 \equiv -1$.",
         r"Work out $2^5$ and $3^5$ modulo 11."))],
    r"The kernel of squaring is $\{1, 10\}$, the roots of $x^2 = 1$ in a field. "
    r"By the first isomorphism theorem the image has $\tfrac{10}{2} = 5$ elements. "
    r"Those squares are exactly where $x^5 = 1$, so 3 is a square and 2 is not."))

# topology L1 (l1) with L3 (l12, l13): a contraction of the plane in the largest-gap metric
Tp = lambda p: (math.sin(p[1]) / 3 + 2, math.cos(p[0]) / 4)
p0 = (2.0, 0.0)
ps = [p0]
for _ in range(80):
    ps.append(Tp(ps[-1]))
fix = ps[-1]
d10 = max(abs(ps[1][0] - p0[0]), abs(ps[1][1] - p0[1]))
q = 1 / 3
n_prior = next(n for n in range(200) if q ** n / (1 - q) * d10 < 1e-6)
n_noconst = next(n for n in range(200) if q ** n < 1e-6)
items.append(parts(
    "e-plane-contraction", 5, ["tg-complete", "tg-metric"], ["a-priori-bound"], 420, "A contraction of the plane",
    r"On $\mathbb{R}^2$ let $T(x, y) = (\tfrac13 \sin y + 2,\ \tfrac14 \cos x)$. $(\mathbb{R}^2, d_\infty)$ is complete. By the mean value theorem, the first coordinate of $T$ moves by at most $\tfrac13|y - y'|$. The second moves by at most $\tfrac14|x - x'|$.",
    r"Three questions on the contraction mapping theorem for $T$ in $d_\infty$.",
    [(r"What constant $q$ do these bounds give, so that $d_\infty(T(p), T(p')) \le q\,d_\infty(p, p')$? Give 4 decimal places.",
      num(r(q), 0.00005, [("sum", r(1 / 3 + 1 / 4), 0.00005), ("product", r(1 / 12), 0.00005)], placeholder="a decimal",
          label="q", accept="1/3 = 0.3333"),
      fb(r"Each coordinate gap is at most $\tfrac13 d_\infty(p, p')$, and $d_\infty$ takes the larger gap, so $q = \tfrac13$.",
         r"Bound each coordinate of $T(p) - T(p')$ by a multiple of $d_\infty(p, p')$, then take the larger.",
         {"sum": r"You added the constants, which gives 0.5833. $d_\infty$ takes the larger coordinate gap, so the constants combine by max.",
          "product": r"You multiplied the constants, which gives 0.0833. That is the rate over two steps of one coordinate, not one step of $T$."})),
     (r"From $p_0 = (2, 0)$, $p_1 = (2, \tfrac14 \cos 2) = (2, -0.1040)$. What is the smallest $n$ with $\tfrac{q^n}{1 - q}\,d_\infty(p_1, p_0) < 10^{-6}$, the a priori bound?",
      num(n_prior, 0, [("floor", n_prior - 1, 0), ("no-factor", n_noconst, 0)], placeholder="a whole number", label="n"),
      fb(r"$\tfrac{d_\infty(p_1, p_0)}{1 - q} = 1.5 \times 0.10404 = 0.1561$. Then $0.1561 \times 3^{-11} = 8.8 \times 10^{-7}$, while $n = 10$ gives $2.6 \times 10^{-6}$.",
         r"Solve $0.1561 \times 3^{-n} < 10^{-6}$ for the least whole $n$.",
         {"floor": r"You rounded down. At $n = 10$ the bound is $2.6 \times 10^{-6}$, still too big.",
          "no-factor": r"You dropped the factor $\tfrac{d_\infty(p_1, p_0)}{1 - q} = 0.1561$, which gives 13. The factor is below 1, so fewer steps are needed."})),
     (r"Iterate to the fixed point $p^* = T(p^*)$. What is its first coordinate? Give 4 decimal places.",
      num(r(fix[0]), 0.00005, [("one-step", 2, 0.00005)], placeholder="a decimal", label="First coordinate"),
      fb(r"$p^* = (1.9678, -0.0967)$: then $\tfrac13 \sin(-0.0967) + 2 = 1.9678$ and $\tfrac14 \cos 1.9678 = -0.0967$.",
         r"Apply $T$ repeatedly from $p_0$; each step cuts the error by at least a factor of 3.",
         {"one-step": r"You stopped at $p_1$, whose first coordinate is still 2. The second coordinate is now negative, which pulls the first below 2."}))],
    r"Each coordinate of $T(p) - T(p')$ is at most $\tfrac13 d_\infty(p, p')$, so $T$ is a contraction with $q = \tfrac13$ on a complete space. "
    r"The theorem gives one fixed point, and the a priori bound promises $10^{-6}$ by step 11. "
    r"The iterates settle at $p^* = (1.9678, -0.0967)$."))

# topology L3 (l12): a power of T that contracts (self-marked)
items.append({
    "id": "e-power-contraction-proof", "difficulty": 5, "skills": ["tg-complete"], "tags": ["contraction-proof"], "pace": 600,
    "title": "When a power of T contracts",
    "kind": "longform",
    "prompt": r"Let $(X, d)$ be a non-empty complete metric space and $T : X \to X$. Suppose that for some $k \ge 1$ the iterate $T^k = T \circ \cdots \circ T$ is a contraction."
              "\n\n"
              r"(a) Prove that $T$ has exactly one fixed point. You may quote the contraction mapping theorem."
              "\n\n"
              r"(b) Let $T(x) = e^{-x}$ on $X = [0, \infty)$. Show that $T$ is not a contraction, but $T^2$ is, with constant $q = \tfrac1e$."
              "\n\n"
              r"(c) Explain why the iterates $x_{n+1} = e^{-x_n}$ converge to the same point from every $x_0 \ge 0$."
              "\n\n"
              "Give a reason for every line.",
    "model": r"**(a)** $T^k$ is a contraction on a non-empty complete metric space. By the contraction mapping theorem it has exactly one fixed point $x^*$."
             "\n\n"
             r"*Existence.* $T^k(Tx^*) = T^{k+1}x^* = T(T^kx^*) = Tx^*$, so $Tx^*$ is also a fixed point of $T^k$. By uniqueness, $Tx^* = x^*$."
             "\n\n"
             r"*Uniqueness.* If $Ty = y$, then applying $T$ again $k - 1$ times gives $T^ky = y$. So $y$ is a fixed point of $T^k$, and $y = x^*$. $\blacksquare$"
             "\n\n"
             r"**(b)** $X = [0, \infty)$ is closed in $\mathbb{R}$, so it is complete, and $T$ maps $X$ into $(0, 1] \subseteq X$."
             "\n\n"
             r"$T$ is not a contraction. For $h > 0$, $\tfrac{|T(h) - T(0)|}{h} = \tfrac{1 - e^{-h}}{h}$, which tends to 1 as $h \to 0$. So no constant $q < 1$ works near 0."
             "\n\n"
             r"$T^2(x) = e^{-e^{-x}}$ has $(T^2)'(x) = e^{-e^{-x}}e^{-x}$. Put $u = e^{-x} \in (0, 1]$: the derivative is $ue^{-u}$."
             "\n\n"
             r"$\tfrac{d}{du}(ue^{-u}) = (1 - u)e^{-u} \ge 0$ on $(0, 1]$, so $ue^{-u} \le e^{-1}$. By the mean value theorem, $|T^2x - T^2y| \le \tfrac1e|x - y|$, with $\tfrac1e = 0.3679 < 1$."
             "\n\n"
             r"**(c)** By (a), $T$ has exactly one fixed point $x^*$, the root of $x = e^{-x}$, about 0.5671."
             "\n\n"
             r"The even iterates are $x_{2m} = (T^2)^m x_0$ and the odd ones are $x_{2m+1} = (T^2)^m x_1$. By the theorem for $T^2$, both tend to the fixed point of $T^2$, which is $x^*$."
             "\n\n"
             r"Both subsequences tend to $x^*$, so the whole sequence does, from every $x_0 \ge 0$.",
    "rubric": [
        {"points": 2, "text": r"Applies the contraction mapping theorem to $T^k$, naming completeness and non-emptiness, for a unique fixed point $x^*$"},
        {"points": 2, "text": r"Shows $Tx^*$ is fixed by $T^k$, since $T^k(Tx^*) = T(T^kx^*)$, and concludes $Tx^* = x^*$ by uniqueness"},
        {"points": 1, "text": r"Shows a fixed point of $T$ is fixed by $T^k$, so $T$ has at most one"},
        {"points": 2, "text": r"Shows $T$ is not a contraction, through slopes near 0 that tend to 1"},
        {"points": 2, "text": r"Bounds $|(T^2)'| = ue^{-u} \le \tfrac1e$ and uses the mean value theorem, noting $X$ is complete and $T(X) \subseteq X$"},
        {"points": 1, "text": r"Argues convergence from every $x_0$ through the even and odd iterates"}],
    "explain": {"text": r"A fixed point of $T^k$ is moved by $T$ to another fixed point of $T^k$, so uniqueness pins it. "
                        r"For $e^{-x}$ the slope near 0 is close to 1, but two steps shrink distances by $\tfrac1e$. "
                        r"So the theorem still gives one fixed point, about 0.5671, and convergence from every start."}})

order = {2: [], 3: [], 4: [], 5: []}
for it in items:
    order[it["difficulty"]].append(it)
exam = {
    "id": "topic-3.4", "topic": "3.4", "name": "Pure mathematics", "minutes": 100, "pass": 0.7,
    "skills": {"ag-groups": "Groups", "ag-cosets": "Subgroups and cosets", "ag-perm": "Permutations",
               "ag-hom": "Homomorphisms and quotients", "ag-rings": "Rings and fields",
               "ag-poly": "Polynomials over a field",
               "tg-metric": "Metric spaces", "tg-open": "Open sets and topologies", "tg-continuity": "Continuity",
               "tg-connected": "Connectedness", "tg-compact": "Compactness",
               "tg-complete": "Completeness and contraction"},
    "items": order[2] + order[3] + order[4] + order[5],
}
with open(OUT, "w", encoding="utf8") as f:
    json.dump(exam, f, indent=1, ensure_ascii=False)
    f.write("\n")
print("wrote", os.path.normpath(OUT), len(exam["items"]), "items, pace", sum(i["pace"] for i in exam["items"]), "s",
      {d: len(v) for d, v in order.items()})
