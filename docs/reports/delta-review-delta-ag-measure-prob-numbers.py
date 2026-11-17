#!/usr/bin/env python3
"""Delta read AG, measure-prob problem sets 1 to 3 (review-delta-ag-measure-prob).

Recomputes every key, every `wrong` value and every printed number of the four
re-authored problems, of p-no-double-four and of the parts the fix pass changed.
Imports no earlier script. Standard library only. Exits 0; a failing check
prints a FINDING line (the listed ones are findings of the review).
"""
import json, math, os, re
from fractions import Fraction as F
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..", "..", "app", "content", "courses", "measure-prob")
SETS = {n: json.load(open(os.path.join(BASE, f"problems-{n}.json"))) for n in (1, 2, 3)}
ITEM = {it["id"]: it for s in SETS.values() for it in s["items"]}

checks = 0
findings = []


def chk(name, cond, note=""):
    global checks
    checks += 1
    if not cond:
        findings.append(name)
        print(f"FINDING {name} {note}".rstrip())


def close(a, b, eps=1e-9):
    return abs(a - b) <= eps


def part(pid, k):
    return ITEM[pid]["parts"][k - 1]


def key(pid, k):
    return part(pid, k)["widget"]["answer"]


def wrong(pid, k, wid):
    for w in part(pid, k)["widget"]["wrong"]:
        if w["id"] == wid:
            return w["value"]
    raise KeyError((pid, k, wid))


def accepts(value, answer, tol):  # app/js/engine/widgets/_base.js
    return abs(value - answer) <= tol + 1e-12


def places_of(q):
    m = re.search(r"(\d) decimal places|to (\d) places|to (\d) decimal places", q)
    if m:
        return int(next(g for g in m.groups() if g))
    if "whole number" in q:
        return 0
    return None


def typed(x, p):
    return x if p is None else float(f"{x:.{p}f}")


def stored(v, exact):
    """A stored value is the exact one, or the exact one rounded to the decimals it is stored with."""
    d = len(repr(float(v)).split(".")[1])
    return close(v, exact, 6e-7) or (d >= 3 and close(v, round(exact, d), 1e-12))


def bands(pid, k, exact, wrongs_exact):
    """Key and slips typed at the places asked; ties; disjoint bands."""
    w = part(pid, k)["widget"]
    p = places_of(part(pid, k)["question"])
    ans, tol = w["answer"], w["tol"]["abs"]
    tag = f"{pid}.{k}"
    chk(f"{tag} key", stored(ans, exact), f"{ans} vs {exact}")
    chk(f"{tag} key typed at places", accepts(typed(exact, p), ans, tol))
    if p is not None:
        frac = abs(exact * 10 ** p - math.floor(exact * 10 ** p) - 0.5)
        chk(f"{tag} key not on a rounding tie", frac > 1e-6)
    ids = {x["id"]: x for x in w.get("wrong", [])}
    chk(f"{tag} wrong ids", set(ids) == set(wrongs_exact), f"{sorted(ids)} vs {sorted(wrongs_exact)}")
    for wid, val in wrongs_exact.items():
        x = ids[wid]
        chk(f"{tag} wrong {wid} value", stored(x["value"], val), f"{x['value']} vs {val}")
        t = typed(val, p)
        chk(f"{tag} wrong {wid} refused by key", not accepts(t, ans, tol) and not accepts(val, ans, tol))
        chk(f"{tag} wrong {wid} typed at places routed", accepts(t, x["value"], x["tol"]["abs"]))
        for oid, o in ids.items():
            if oid != wid:
                chk(f"{tag} bands {wid}/{oid} disjoint", abs(x["value"] - o["value"]) > x["tol"]["abs"] + o["tol"]["abs"])
        chk(f"{tag} band {wid} clear of key band", abs(x["value"] - ans) > x["tol"]["abs"] + tol)


def working(tag, value, pid, k):
    """A figure a learner gets from the printed working, typed at the places asked."""
    w = part(pid, k)["widget"]
    p = places_of(part(pid, k)["question"])
    chk(f"{tag} printed working taken by the band", accepts(typed(value, p), w["answer"], w["tol"]["abs"]),
        f"working gives {typed(value, p)}, key {w['answer']} +- {w['tol']['abs']}")


def tex_eval(tex, **env):
    s = tex.replace("\\cdot", "*").replace("\\left", "").replace("\\right", "")
    s = re.sub(r"\\sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
    s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
    s = re.sub(r"\^\{([^{}]*)\}", r"**(\1)", s).replace("^", "**")
    return eval(s, {"sqrt": math.sqrt}, env)


# ---------------------------------------------------------------- p-quote-ladder
P = "p-quote-ladder"
r = F(2, 5)
pN = lambda k: r ** k - r ** (k + 1)  # length of the band (0.4^(k+1), 0.4^k]
chk("ladder total", close(float(sum(pN(k) for k in range(300))), 1))
bands(P, 1, float(pN(2)), {"rung": 0.16, "next-rung": 0.064, "swap": 0.4 * 0.6 ** 2})
w2 = part(P, 2)["widget"]
for k in range(6):
    chk(f"ladder.2 key at k={k}", close(tex_eval(w2["answer"], k=k), float(pN(k))))
    for x, f in zip(w2["wrong"], (lambda k: 0.4 ** k, lambda k: 0.4 ** (k + 1), lambda k: 0.4 * 0.6 ** k)):
        chk(f"ladder.2 wrong {x['id']} at k={k}", close(tex_eval(x["tex"], k=k), f(k)) and (k == 1 or not close(f(k), float(pN(k)))))
third = sum(pN(3 * j) for j in range(200))
chk("ladder.3 series is 25/39", close(float(third), 25 / 39))
bands(P, 3, 25 / 39, {"no-zero": 25 / 39 - 0.6, "third": 1 / 3, "two-terms": float(pN(0) + pN(3))})
working("ladder.3 0.6/0.936", 0.6 / 0.936, P, 3)
# part 5 two ways: exact band algebra, then a midpoint grid on U with N found by search
exact5 = sum(r ** k - r ** k / 2 for k in range(300))
hits = n = 0
for i in range(400000):
    u = (i + 0.5) / 400000
    k = 0
    while 0.4 ** (k + 1) >= u:
        k += 1
    hits += 0.4 ** k <= 2 * u
    n += 1
chk("ladder.5 exact 5/6", close(float(exact5), 5 / 6))
chk("ladder.5 grid", abs(hits / n - 5 / 6) < 2e-4, f"{hits / n}")
bands(P, 5, 5 / 6, {"half-band": 0.5, "complement": 1 / 6})
chk("ladder.5 cut-off above each floor", all(0.5 * 0.4 ** k > 0.4 ** (k + 1) for k in range(40)))
chk("ladder.4 key option", [o["id"] for o in part(P, 4)["widget"]["options"] if o.get("correct")] == ["all-b"])
chk("ladder.4 {U<=0.5} cuts the band of N=0", 0.4 < 0.5 < 1)
why = {o["id"]: o.get("why", "") for o in part(P, 4)["widget"]["options"]}
chk("ladder.4 `countable` line says the sets are uncountable (each set of values is countable)",
    "those sets are uncountable" not in why["countable"], "finding 7")

# ------------------------------------------------------------ p-settlement-fails
P = "p-settlement-fails"
pm = lambda k: F(64, 100) * (k + 1) * F(1, 5) ** k
K = 400
chk("fails total", close(float(sum(pm(k) for k in range(K))), 1))
m_pen = float(sum(F(5, 4) ** k * pm(k) for k in range(K)))
EN = float(sum(k * pm(k) for k in range(K)))
EN2 = float(sum(k * k * pm(k) for k in range(K)))
chk("fails E[N] also as 2q/p of a negative binomial", close(EN, 2 * 0.2 / 0.8))
chk("fails Var(N) also as 2q/p^2", close(EN2 - EN ** 2, 2 * 0.2 / 0.64))
bands(P, 1, m_pen, {"jensen": 1.25 ** EN, "no-k": float(sum(F(64, 100) * F(1, 4) ** k for k in range(K)))})
chk("fails.1 256/225", close(m_pen, 256 / 225))
working("fails.1 0.64/0.5625", 0.64 / 0.5625, P, 1)
G = lambda s: sum(float(pm(k)) * s ** k for k in range(K))
for s in (0, 0.3, 0.9, 1.25, 3, 4.5):
    chk(f"fails.2 G({s})", close(G(s), 16 / (5 - s) ** 2, 1e-6 * max(1, G(s))))
for s in (0.2, 0.6, 0.95):
    d1 = sum(k * float(pm(k)) * s ** (k - 1) for k in range(1, K))
    d2 = sum(k * (k - 1) * float(pm(k)) * s ** (k - 2) for k in range(2, K))
    chk(f"fails.2 G'({s})", close(d1, 32 / (5 - s) ** 3, 1e-9))
    chk(f"fails.4 G''({s})", close(d2, 96 / (5 - s) ** 4, 1e-9))
chk("fails.2 N s^(N-1) rises in s for N >= 1", all(n * a ** (n - 1) <= n * b ** (n - 1) for n in range(1, 30) for a, b in ((0.1, 0.4), (0.4, 0.99))))
chk("fails.2 explain: 's^(N-1) rises with s' fails at N = 0 (s^-1 falls)",
    "For fixed $N$, $s^{N-1}$ rises with $s$" not in part(P, 2)["explain"]["text"], "finding 6")
dct = next(o for o in part(P, 2)["widget"]["options"] if o["id"] == "dct")
chk("fails.2 option `dct` is a true statement marked wrong (E[N] = 0.5 is finite, so Y = N does dominate)",
    dct["text"] != "Dominated convergence with $Y = N$, since $Ns^{N-1} \\le N$", "finding 9")
chk("fails.2 key option", [o["id"] for o in part(P, 2)["widget"]["options"] if o.get("correct")] == ["mct"])
bands(P, 3, EN, {"one": G(1), "at-zero": float(pm(1)), "square": 32 / 16})
chk("fails.3 32/125 is G'(0) = P(N = 1)", close(32 / 125, float(pm(1))))
bands(P, 4, EN2, {"falling": EN2 - EN, "variance": EN2 - EN ** 2, "mean-sq": EN ** 2})
chk("fails.4 96/256", close(96 / 256, EN2 - EN))
terms5 = [float(5 ** k * pm(k)) for k in range(30)]
chk("fails.5 terms are 0.64(k+1)", all(close(t, 0.64 * (k + 1)) for k, t in enumerate(terms5)))
chk("fails.5 key option", [o["id"] for o in part(P, 5)["widget"]["options"] if o.get("correct")] == ["inf"])
chk("fails.1 `jensen` line prints part 3's key E[N] = 0.5",
    "0.5" not in part(P, 1)["feedback"]["byKey"]["jensen"], "finding 2")
o5 = {o["id"]: o for o in part(P, 5)["widget"]["options"]}
chk("fails.5 retells l5 'Does every random variable have a mean?' (options and why lines)",
    not ("shrink" in o5 and "always has a mean in" in o5.get("undefined", {}).get("why", "")), "finding 4")
# the replacement part of finding 4: 6^N
chk("fix 4: terms of E[6^N] are 0.64(k+1)1.2^k and grow", all(close(float(6 ** k * pm(k)), 0.64 * (k + 1) * 1.2 ** k, 1e-9 * 1.2 ** k) for k in range(40)))
chk("fix 4: formula gives 16 at s = 6", close(16 / (5 - 6) ** 2, 16))
chk("fix 4: 6^0.5 is 2.45", f"{6 ** 0.5:.2f}" == "2.45")

# -------------------------------------------------------------------- p-boom-bust
P = "p-boom-bust"


def law(n):  # (value of M_n, chance) by number of up days
    return [(1.6 ** k * 0.4 ** (n - k), math.comb(n, k) / 2 ** n) for k in range(n + 1)]


for n in range(0, 12):
    chk(f"boom E[M_{n}] = 1", close(sum(v * p for v, p in law(n)), 1))
    chk(f"boom.1 E[sqrt M_{n}]", close(sum(math.sqrt(v) * p for v, p in law(n)), 0.9 ** (n / 2)))
w1 = part(P, 1)["widget"]
for n in (1, 2, 5):
    chk(f"boom.1 key at n={n}", close(tex_eval(w1["answer"], n=n), 0.9 ** (n / 2)))
    for x, f in zip(w1["wrong"], (lambda n: 0.8 ** n, lambda n: (math.sqrt(1.6) + math.sqrt(0.4)) ** n, lambda n: 0.9 ** n)):
        chk(f"boom.1 wrong {x['id']} at n={n}", close(tex_eval(x["tex"], n=n), f(n)) and not close(f(n), 0.9 ** (n / 2)))
chk("boom.1 3/sqrt(10) and sqrt(1.6*0.4)", close((math.sqrt(1.6) + math.sqrt(0.4)) / 2, 3 / math.sqrt(10)) and close(math.sqrt(1.6 * 0.4), 0.8))
chk("boom.2 indicator bound on the 5 values of M_4", all((v > 0.5) <= math.sqrt(v / 0.5) for v, _ in law(4)))
b2 = sum(math.sqrt(v) * p for v, p in law(4)) / math.sqrt(0.5)
bands(P, 2, b2, {"no-root": 0.81, "epsilon": 0.81 / 0.5, "markov-m": 1 / 0.5})
working("boom.2 0.81/0.7071", 0.81 / 0.7071, P, 2)
p3 = sum(1 for path in product((1.6, 0.4), repeat=4) if math.prod(path) > 0.5) / 16
bands(P, 3, p3, {"two-ups": 11 / 16, "all-up": 1 / 16, "three-only": 4 / 16})
chk("boom.3 0.4096, 1.6384, 0.0256*4^k", close(1.6 ** 2 * 0.4 ** 2, 0.4096) and close(1.6 ** 3 * 0.4, 1.6384) and all(close(v, 0.0256 * 4 ** k) for k, (v, _) in enumerate(law(4))))
chk("boom.3 exact chance below the bound of part 2", p3 <= b2)
tail = sum(0.9 ** (n / 2) / math.sqrt(0.01) for n in range(200, 6000))
chk("boom.4 closed form", close(tail, 10 * 0.9 ** 100 / (1 - math.sqrt(0.9)), 1e-12))
bands(P, 4, tail, {"one-day": 10 * 0.9 ** 100, "no-root": tail / 10, "epsilon": tail * 10})
working("boom.4 explain 10*0.9^100/(1-0.9487)", 10 * 0.9 ** 100 / (1 - 0.9487), P, 4)
if "\\tfrac{0.0000266}{0.0513}" in part(P, 4)["feedback"]["correct"]:  # finding 1
    working("boom.4 feedback.correct 10*0.0000266/0.0513", 10 * 0.0000266 / 0.0513, P, 4)
working("fix 1: 10*0.00002656/0.0513", 10 * 0.00002656 / 0.0513, P, 4)
chk("fix 1: 0.9^100 is 0.00002656 to 4 figures", f"{0.9 ** 100:.8f}" == "0.00002656")
chk("boom.4 bound sits above the exact chance on day 200", sum(p for v, p in law(200) if v > 0.01) <= 0.9 ** 100 * 10)
m10 = sum(v * v * p for v, p in law(10))
chk("boom.5 one-day factor 1.36", close((1.6 ** 2 + 0.4 ** 2) / 2, 1.36))
bands(P, 5, m10, {"mean-sq": 1, "added": 13.6, "one-day": 1.36})
chk("boom.5 1.36^10", close(m10, 1.36 ** 10, 1e-9))
chk("boom.5 'so M_n -> 0 almost surely' rests on the bound for 0.01 alone",
    "any $\\varepsilon" in part(P, 5)["question"] or "every $\\varepsilon" in part(P, 5)["question"], "finding 5")
for eps in (0.5, 1e-3, 1e-9):  # the bound for any epsilon does shrink with the start day
    chk(f"boom.5 tail bound for eps={eps} shrinks", 0.9 ** 2000 / (1 - math.sqrt(0.9)) / math.sqrt(eps) < 1e-80)

# ------------------------------------------------------------------ p-trial-stake
P = "p-trial-stake"
leaves = [  # (news path, chance, X)
    (("fail",), F(4, 10), 20),
    (("ok", "refused"), F(6, 10) * F(1, 4), 40),
    (("ok", "approved", "strong"), F(6, 10) * F(3, 4) * F(8, 10), 100),
    (("ok", "approved", "weak"), F(6, 10) * F(3, 4) * F(2, 10), 50),
]
chk("trial total", sum(p for _, p, _ in leaves) == 1)


def M(prefix):
    sel = [(p, x) for path, p, x in leaves if path[:len(prefix)] == prefix[:len(path)]]
    return sum(p * x for p, x in sel) / sum(p for p, _ in sel)


chk("trial M0", M(()) == F(109, 2))
chk("trial M1", M(("ok",)) == F(155, 2) and M(("fail",)) == 20)
chk("trial M2", M(("ok", "approved")) == 90 and M(("ok", "refused")) == 40)
chk("trial martingale at each node", M(()) == F(6, 10) * M(("ok",)) + F(4, 10) * 20
    and M(("ok",)) == F(3, 4) * 90 + F(1, 4) * 40 and M(("ok", "approved")) == F(8, 10) * 100 + F(2, 10) * 50)
bands(P, 1, 77.5, {"approved": 90, "no-refusal": 0.75 * 90, "unweighted": (100 + 50 + 40) / 3})
chk("trial.1 chances given a success", (F(3, 4) * F(8, 10), F(3, 4) * F(2, 10), F(1, 4)) == (F(6, 10), F(15, 100), F(1, 4)))


def stopped(rule):
    out = []
    for path, p, x in leaves:
        full = path + (path[-1],) * (3 - len(path))
        for n in range(0, 4):
            if n == 3 or rule(M(full[:n])):
                out.append((n, p, M(full[:n])))
                break
    return out


first = stopped(lambda m: m >= 80)
second = stopped(lambda m: m <= 45)
bands(P, 2, float(sum(p for n, p, _ in first if n == 2)), {"at-success": 0.6, "strong": 0.36, "approval": 0.75})
chk("trial.3 both rules have mean 54.5", sum(p * m for _, p, m in first) == F(109, 2) == sum(p * m for _, p, m in second))
chk("trial.3 neither rule stops at n = 0", all(n > 0 for n, _, _ in first + second))
chk("trial.3 second fund sells at 20 (n=1) or 40 (n=2) or holds", sorted((n, float(m)) for n, _, m in second) == [(1, 20.0), (2, 40.0), (3, 50.0), (3, 100.0)])
chk("trial.3 key option", [o["id"] for o in part(P, 3)["widget"]["options"] if o.get("correct")] == ["both"])
EMT2 = sum(p * m * m for _, p, m in first)
VX = sum(p * x * x for _, p, x in leaves) - F(109, 2) ** 2
chk("trial.4 E[M_T^2] = 4045 and 54.5^2", EMT2 == 4045 and F(109, 2) ** 2 == F(297025, 100))
bands(P, 4, float(EMT2 - F(109, 2) ** 2), {"hold": float(VX), "no-mean": 4045, "gap": float(VX - (EMT2 - F(109, 2) ** 2))})
lawT = {}
for _, p, m in first:
    lawT[m] = lawT.get(m, 0) + p
chk("trial.4 law of M_T", lawT == {20: F(4, 10), 40: F(15, 100), 90: F(45, 100)})
chk("trial.4 explain cites 'part 4' for the mean of part 3", "by part 4" not in part(P, 4)["explain"]["text"], "finding 3")
chk("trial.2/3 'day' used for a piece of news", "day" not in part(P, 2)["feedback"]["generic"] and "selling day" not in json.dumps(part(P, 3)), "finding 8")

# --------------------------------------------------------------- p-no-double-four
P = "p-no-double-four"
cnt = lambda n: sum(1 for s in product("0123456789", repeat=n) if "44" not in "".join(s))
a = {n: cnt(n) for n in (2, 3, 4, 5)}
chk("four counts", a == {2: 99, 3: 981, 4: 9720, 5: 96309})
chk("four recursion", a[4] == 9 * a[3] + 9 * a[2] and a[5] == 9 * a[4] + 9 * a[3])
chk("four 19 strings hold 44", 1000 - a[3] == 19)
bands(P, 1, 0.981, {"overlap": 0.98, "first-pair": 0.99})
bands(P, 2, 0.972, {"one-term": 0.8829, "square": 0.981 ** 2, "independent": 0.981 * 0.99})
chk("four.2 independent 0.97119", close(0.981 * 0.99, 0.97119))
x = next(w for w in part(P, 2)["widget"]["wrong"] if w["id"] == "independent")
chk("four.2 independent band as the reader gave it", x["tol"]["abs"] == 0.0003 and accepts(0.971, x["value"], 0.0003) and not accepts(0.972, x["value"], 0.0003))
chk("four.2 independent line as the reader gave it", part(P, 2)["feedback"]["byKey"]["independent"] ==
    "That is $0.981 \\times 0.99$. $D_3$ and the pair $d_3 d_4$ share the digit $d_3$, so their chances do not multiply. Use the recursion.")
bands(P, 3, 0.99 ** 100, {"all-places": 0.99 ** 199, "all-digits": 0.99 ** 200})
blob = json.dumps(ITEM[P], ensure_ascii=False)
chk("four no block 77 or digit 7 left", not re.search(r"77|digit other than 7|in a 7 |ending in a 7", blob))
chk("four 44 strings present", blob.count("44") >= 30 and "444" in blob and "0.1111" in blob)
# P(D_200) is larger than 0.99^199, so that figure is no upper bound
x0, x1 = 1.0, 0.99
for n in range(3, 201):
    x0, x1 = x1, 0.9 * x1 + 0.09 * x0
chk("four P(D_200) between 0.99^199 and 0.99^100", 0.99 ** 199 < x1 < 0.99 ** 100, f"{x1}")

# ------------------------------------------------------- fix-pass lines, 7 to 11
c = ITEM["p-compounding"]["parts"]
chk("fix 8 text", c[1]["question"] == "As in part 1, expand and use the moments of $R$ from the setting. Find $E[G_4]$. Give 4 decimal places.")
chk("fix 7 text", c[2]["feedback"]["byKey"]["no-abs"] == "That is $e^{0.125}$ alone. The formula also carries the factors 2 and $\\Phi(0.5) = 0.6915$.")
phi = 0.5 * math.erfc(-0.5 / math.sqrt(2))
chk("fix 7 numbers", f"{phi:.4f}" == "0.6915" and close(c[2]["widget"]["wrong"][0]["value"], round(math.exp(0.125), 4)) and f"{2 * math.exp(0.125) * 0.6915:.3f}" == "1.567")
chk("fix 7 part 3 no longer names E[e^R]", "E[e^R]" not in json.dumps(c[2]))
EG4 = 1 + 6 * 0.25 / 16 + 3 * 0.25 ** 2 / 256
chk("fix 8 key of the part", close(c[1]["widget"]["answer"], round(EG4, 4)))
m = ITEM["p-random-maturity"]["parts"][1]
chk("fix 9 texts", m["widget"]["options"][0]["text"] == "$Y = 4$: the quotient has size $Te^{-sT}$ for some $s \\ge 0$, at most $T \\le 4$"
    and m["feedback"]["correct"].startswith("By the mean value theorem each quotient has size $Te^{-sT}$"))
chk("fix 9 bound", all(abs((math.exp(-(r_ + h) * T) - math.exp(-r_ * T)) / h) <= T + 1e-12
                       for T in (0.5, 2, 4) for r_ in (0, 0.3, 0.9) for h in (0.1, 0.01, -0.05) if 0 <= r_ + h <= 1))
nf = ITEM["p-nested-forecasts"]["parts"][4]
pr = [0.1, 0.15, 0.25, 0.2, 0.2, 0.1]
xs = [-3, 1, 5, 2, 6, -4]
cond = lambda atoms: {i: sum(pr[j] * xs[j] for j in A) / sum(pr[j] for j in A) for A in atoms for i in A}
g, h = cond([(0,), (1, 2), (3, 4), (5,)]), cond([(0, 1, 2), (3, 4, 5)])
gap = sum(pr[i] * (g[i] - h[i]) ** 2 for i in range(6))
side = sum(pr[i] * (g[i] - h[i]) ** 2 for i in range(3))
chk("fix 10 numbers", close(gap, 8.5) and close(side, 3.38) and close(gap - side, 1.024 + 4.096) and close(nf["widget"]["wrong"][1]["value"], side))
chk("fix 10 text", nf["feedback"]["byKey"]["one-side"] == "That counts the scenarios $\\{1, 2, 3\\}$ only. The side $\\{4, 5, 6\\}$ adds $1.024 + 4.096$.")
tu = ITEM["p-two-ups-stop"]["parts"]
early = late = 0
for path in product((1, -1), repeat=4):
    s, stop = 0, None
    for n, st in enumerate(path, 1):
        s += st
        if n >= 2 and path[n - 2] == 1 and st == 1:
            stop = n
            break
    if stop and stop < 4:
        early += s / 16
    else:
        late += s / 16
chk("fix 11 numbers", close(early, 0.625) and close(late, -0.625) and close(tu[2]["widget"]["wrong"][0]["value"], 0.625))
chk("fix 11 text", tu[2]["feedback"]["byKey"]["early-only"] == "That counts only the paths that stop early. The paths that run to day 4 count too, and optional stopping gives the total at once.")
chk("fix 11 part 3 no longer prints part 5's working", "\\tfrac18" not in json.dumps(tu[2]))

print(f"{checks} checks, {len(findings)} FINDING line(s)")
