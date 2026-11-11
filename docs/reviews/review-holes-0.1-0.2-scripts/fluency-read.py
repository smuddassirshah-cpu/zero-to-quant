"""Second read of the nine level 4 Fluency sets (number-sense l15 to l19, quadratics l14 to l17).

For every draw in <dir> (made by draw.sh: 20 a family, seeds 7001 on) the answer is rebuilt from the PROMPT TEXT alone
(regex on the sentence the learner reads, then integer arithmetic or sympy), never from the draw's vars or lets, and
compared with the generated answer. Each wrong value is rebuilt from the slip its line describes. Extra checks: a wrong
value never equals the answer or another wrong value; shapes can exist (a slant side is longer than the height); the
value a learner gets with pi = 3.14 or 22/7, rounded as the prompt asks, lies inside the tolerance (review-number-sense-4
findings 3 and 20); oddities of wording (a coefficient 1 printed, "1 hours").

  <venv>/bin/python fluency-read.py <dir>        exit 0 when every check passes; NOTE lines are for the reader to judge
"""
import glob
import json
import math
import os
import re
import sys
from fractions import Fraction as Fr

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor

TR = standard_transformations + (implicit_multiplication_application, convert_xor)
checks = fails = 0
notes = []


def E(s):
    s = s.replace('\\left', '').replace('\\right', '').replace('{', '(').replace('}', ')').replace(' ', '')
    return parse_expr(s, transformations=TR)


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


def note(msg):
    notes.append(msg)


def nums(s):
    return [int(x.replace('{,}', '').replace(',', '')) for x in re.findall(r'\$(-?\d[\d{},]*)\$', s)]


def wr(it):
    return {w['id']: w.get('value', w.get('tex')) for w in it.get('wrong') or []}


def close(a, b, t=1e-6):
    return abs(float(a) - float(b)) <= t


def same(a, b):
    return sp.simplify(E(a) - E(b)) == 0 if isinstance(a, str) else sp.simplify(a - E(b)) == 0


def fracs(p):
    return re.findall(r'\\dfrac\{([^{}]*)\}\{([^{}]*)\}', p)


def rounded_pi(it, exact_over_pi, dp, where):
    """the value a learner gets with 3.14 and 22/7, rounded to dp places, must sit inside the band"""
    tol = it['tol']['abs']
    for name, pi in (('3.14', Fr(314, 100)), ('22/7', Fr(22, 7)), ('3.142', Fr(3142, 1000))):
        v = round(float(exact_over_pi * pi) + 1e-12, dp)
        ok(abs(v - it['answer']) <= tol + 1e-9, f"{where}: with pi = {name} the learner types {v}, outside {it['answer']:.4f} +/- {tol}")


def check(fam, it, where):
    p, a, w = it['prompt'], it.get('answer', it.get('answers')), wr(it)
    n = nums(p)
    # ---------------- number-sense l15
    if fam == 'count-factors':
        N = n[0]
        f = sp.factorint(N)
        ok(a == sp.divisor_count(N), f'{where}: answer')
        ok(a == sum(1 for d in range(1, N + 1) if N % d == 0), f'{where}: answer by counting')
        npo = math.prod(f.values())
        ok(w.get('pairs', (a + 1) // 2) == (a + 1) // 2, f'{where}: pairs')
        ok('pairs' in w or (a + 1) // 2 == npo, f'{where}: pairs dropped with no clash')
        ok(w['no-plus-one'] == npo, f'{where}: no-plus-one')
        if w['no-plus-one'] == 1:
            note(f"{where}: no-plus-one is 1 for {N} (every index is 1): 'You multiplied the indices' of a number with no index shown")
    elif fam == 'count-from-primes':
        body = re.search(r'does \$(.*?)\$ have', p).group(1)
        fs = [(int(b), int(e or 1)) for b, e in re.findall(r'(\d+)(?:\^(\d+))?', body)]
        N = math.prod(b ** e for b, e in fs)
        ok(all(sp.isprime(b) for b, _ in fs), f'{where}: bases prime')
        ok(a == sp.divisor_count(N), f'{where}: answer')
        ok(w['indices-multiplied'] == math.prod(e for _, e in fs), f'{where}: indices-multiplied')
        ok(w['indices-added'] == sum(e + 1 for _, e in fs), f'{where}: indices-added')
    elif fam == 'largest-prime':
        N = n[0]
        ok(a == max(sp.primefactors(N)), f'{where}: answer')
        ok(w['largest-factor'] == N // min(sp.primefactors(N)), f'{where}: largest-factor')
        ok(not sp.isprime(w['largest-factor']), f"{where}: 'not prime' said of {w['largest-factor']}")
    # ---------------- number-sense l16
    elif fam == 'hcf':
        ok(a == math.gcd(n[0], n[1]), f'{where}: answer')
        ok(w['lcm'] == math.lcm(n[0], n[1]), f'{where}: lcm')
        if a == 1 or a == min(n[:2]):
            note(f'{where}: HCF of {n[0]} and {n[1]} is {a} (trivial draw)')
    elif fam == 'lcm':
        ok(a == math.lcm(n[0], n[1]), f'{where}: answer')
        ok(w['product'] == n[0] * n[1] and w['hcf'] == math.gcd(n[0], n[1]), f'{where}: wrongs')
        if a == n[0] * n[1] or a == max(n[:2]):
            note(f'{where}: LCM of {n[0]} and {n[1]} is {a} (trivial draw)')
    elif fam == 'other-number':
        m, g, l = n[0], n[1], n[2]
        ok(Fr(g * l, m) == a, f'{where}: answer')
        cands = [x for x in range(1, l + 1) if math.gcd(m, x) == g and math.lcm(m, x) == l]
        ok(cands == [a], f'{where}: search gives {cands}')
        ok(w['product'] == g * l, f'{where}: product')
        ok(w['lcm-over-hcf'] in (l // g, Fr(l, m)), f"{where}: lcm-over-hcf {w['lcm-over-hcf']}")
        if a in (m, l, g):
            note(f'{where}: other number {a} equals {"the given number" if a == m else "the LCM" if a == l else "the HCF"} (given {m}, HCF {g}, LCM {l})')
    # ---------------- number-sense l17
    elif fam == 'triangle-area':
        b, s, h = n[:3]
        ok(close(a, b * h / 2), f'{where}: answer')
        ok(close(w['no-half'], b * h) and close(w.get('sloping-side', b * s / 2), b * s / 2), f'{where}: wrongs')
        ok('sloping-side' in w or b * s / 2 in (b * h, b * h / 2), f'{where}: sloping-side dropped with no clash')
        ok(s > h, f'{where}: sloping side {s} not longer than height {h}')
    elif fam == 'parallelogram-area':
        b, s, h = n[:3]
        ok(close(a, b * h), f'{where}: answer')
        ok(close(w['slant-side'], b * s) and close(w['halved'], b * h / 2), f'{where}: wrongs')
        ok(s > h, f'{where}: slant side {s} not longer than height {h}')
    elif fam == 'trapezium-area':
        x, c, h = n[:3]
        ok(close(a, (x + c) * h / 2), f'{where}: answer')
        ok(close(w['no-half'], (x + c) * h) and close(w['longer-side'], max(x, c) * h), f'{where}: wrongs')
    elif fam == 'l-shape-area':
        W, T, P, Q = n[:4]
        ok(a == W * T - P * Q, f'{where}: answer')
        ok(w['corner-kept'] == W * T and w['corner-added'] == W * T + P * Q, f'{where}: wrongs')
        ok((P < W and Q < T) or (P < T and Q < W), f'{where}: corner fits')
        if not (P < W and Q < T):
            note(f'{where}: the corner {P} by {Q} fits the {W} by {T} rectangle only when turned')
    # ---------------- number-sense l18
    elif fam == 'area-units':
        x = Fr(re.search(r'area of \$([\d.]+)\$ m', p).group(1))
        ok(a == x * 10000, f'{where}: answer')
        ok(Fr(str(w['length-only'])) == x * 100 and close(w['divided'], float(x) / 10000, 1e-12), f'{where}: wrongs')
    elif fam in ('circle-area', 'circumference'):
        word, m = re.search(r'has (radius|diameter) \$([\d.]+)\$', p).groups()
        m = Fr(m)
        r = m if word == 'radius' else m / 2
        if fam == 'circle-area':
            ok(close(a, math.pi * float(r) ** 2), f'{where}: answer')
            rounded_pi(it, r * r, 1, where)
            ok(close(w['circumference'], 2 * math.pi * float(r)), f'{where}: circumference')
            ok(close(w.get('diameter-squared', w.get('radius-not-halved', w.get('diameter', 0))), math.pi * float(2 * r) ** 2) or word == 'radius', f'{where}: diameter-squared')
            if word == 'radius':
                note(f"{where}: radius given; wrong ids {sorted(w)} values {[round(v, 2) for v in w.values()]} (pi r^2 = {math.pi * float(r) ** 2:.2f}, pi d^2 = {math.pi * float(2 * r) ** 2:.2f}, pi (r/2)^2 = {math.pi * float(r / 2) ** 2:.2f})")
        else:
            ok(close(a, 2 * math.pi * float(r)), f'{where}: answer')
            rounded_pi(it, 2 * r, 1, where)
            ar = math.pi * float(r) ** 2
            ok(close(w.get('area-rule', ar), ar), f'{where}: area-rule')
            ok('area-rule' in w or min(abs(ar - a), abs(ar - w['radius-diameter'])) <= 1, f'{where}: area-rule dropped with no clash')
            other = math.pi * float(r) if word == 'radius' else 2 * math.pi * float(m)
            ok(close(w['radius-diameter'], other), f"{where}: radius-diameter {w['radius-diameter']} against {other}")
        vals = sorted([a] + list(w.values()))
        ok(all(v2 - v1 > 0.5 for v1, v2 in zip(vals, vals[1:])), f'{where}: answer and wrong values closer than 0.5: {vals}')
    elif fam == 'speed-units':
        x, frm = re.search(r'Change \$([\d.]+)\$ (km an hour|metres a second)', p).groups()
        x = Fr(x)
        if frm == 'km an hour':
            t, back, mins = x * 1000 / 3600, x * 3600 / 1000, x * 1000 / 60
        else:
            t, back, mins = x * 3600 / 1000, x * 1000 / 3600, x * 60 / 1000
        ok(close(a, t, 1e-9), f'{where}: answer')
        ok(abs(round(float(t) + 1e-12, 1) - a) <= it['tol']['abs'] + 1e-9, f'{where}: the 1 d.p. value is in the band')
        ok(close(w['wrong-way'], back, 1e-6), f"{where}: wrong-way {w['wrong-way']} against {float(back)}")
        ok(close(w['minutes'], mins, 1e-6), f"{where}: minutes {w['minutes']} against {float(mins)}")
    # ---------------- number-sense l19
    elif fam == 'mean':
        v = n[:5]
        ok(Fr(sum(v), 5) == Fr(str(a)), f'{where}: answer')
        ok(Fr(str(w['divided-by-four'])) == Fr(sum(v), 4), f'{where}: divided-by-four')
        flips = [Fr(sum(v) - 2 * x, 5) for x in v if x < 0]
        ok(Fr(str(w['loss-added'])) in flips, f"{where}: loss-added {w['loss-added']} not in {flips}")
        if len(flips) > 1:
            note(f"{where}: two losses in the list {v}; loss-added flips one of them only")
    elif fam == 'median':
        v = n[:5]
        ok(a == sorted(v)[2], f'{where}: answer')
        ok(w['unsorted'] == v[2], f'{where}: unsorted')
        ok('mean' not in w or Fr(str(w['mean'])) == Fr(sum(v), 5), f'{where}: mean')
        ok('mean' in w or Fr(sum(v), 5) in (a, v[2]), f'{where}: mean dropped with no clash')
        ok(len(set(v)) == 5, f'{where}: repeated values {v}')
    elif fam == 'range':
        v = n[:5]
        ok(a == max(v) - min(v), f'{where}: answer')
        ok(w['first-last'] in (v[0] - v[4], v[4] - v[0]), f"{where}: first-last {w['first-last']} for {v}")
        ok(w['sign-lost'] == max(v) - abs(min(v)), f"{where}: sign-lost {w['sign-lost']} for {v}")
        if w['first-last'] < 0:
            note(f"{where}: first-last is negative ({w['first-last']}) for {v}")
    elif fam == 'table-mean':
        m = re.search(r'over \$(\d+)\$ (\w+): 0 in \$(\d+)\$ \w+, 1 in \$(\d+)\$, 2 in \$(\d+)\$, 3 in \$(\d+)\$ and 4 in \$(\d+)\$', p)
        N, f = int(m.group(1)), [int(m.group(i)) for i in range(3, 8)]
        tot = sum(i * x for i, x in enumerate(f))
        ok(sum(f) == N, f'{where}: counts add to {sum(f)}, prompt says {N}')
        ok(close(a, tot / N, 1e-9), f'{where}: answer')
        ok(abs(round(tot / N + 1e-12, 2) - a) <= it['tol']['abs'], f'{where}: 2 d.p. value in band')
        ok(close(w['values-only'], 2) and close(w['rows'], tot / 5), f'{where}: wrongs')
        if f[0] == 1:
            note(f'{where}: prompt reads "0 in $1$ {m.group(2)}" (plural after 1)')
        if 0 in f:
            note(f'{where}: a count of 0 in the table: {f}')
    # ---------------- quadratics l14
    elif fam == 'simplest-surd':
        N = int(re.search(r'\\sqrt\{(\d+)\}', p).group(1))
        k = max(j for j in range(1, N + 1) if N % (j * j) == 0)
        ok(a == k and k > 1, f'{where}: answer {a} against {k}')
        ok(sp.sqrt(N) == k * sp.sqrt(N // (k * k)), f'{where}: sympy')
        ok(w['square-not-root'] == k * k, f'{where}: square-not-root')
        if 'stopped-early' in w:
            j = w['stopped-early']
            ok(1 < j < k and N % (j * j) == 0, f'{where}: stopped-early {j}')
    elif fam == 'collect-surds':
        A, o, B, m = re.search(r'\\sqrt\{(\d+)\} ([+-]) \\sqrt\{(\d+)\}\$ to \$k\\sqrt\{(\d+)\}', p).groups()
        A, B, m = int(A), int(B), int(m)
        val = sp.sqrt(A) + sp.sqrt(B) if o == '+' else sp.sqrt(A) - sp.sqrt(B)
        ok(sp.simplify(val - a * sp.sqrt(m)) == 0, f'{where}: answer')
        ok(close(float(val), a * math.sqrt(m), 1e-9), f'{where}: answer in floating point')
        ok(sp.factorint(m) and all(e == 1 for e in sp.factorint(m).values()), f'{where}: {m} square-free')
        ok(w['no-roots'] == (A // m + B // m if o == '+' else A // m - B // m), f'{where}: no-roots')
        if a <= 0:
            note(f'{where}: k = {a} for sqrt({A}) {o} sqrt({B})')
        if A == m or B == m:
            note(f'{where}: one root is already simple: sqrt({A}) {o} sqrt({B})')
    elif fam == 'conjugate-bottom':
        P, o, Q = re.search(r'\{(\d+) ([+-]) \\sqrt\{(\d+)\}\}', p).groups()
        P, Q = int(P), int(Q)
        ok(a == P * P - Q, f'{where}: answer')
        ok(sp.expand((P + sp.sqrt(Q)) * (P - sp.sqrt(Q))) == a, f'{where}: sympy')
        ok(w['added'] == P * P + Q and w['squared-q'] == P * P - Q * Q, f'{where}: wrongs')
        co = re.search(r'bottom by \$(\d+) ([+-]) \\sqrt', p).group(2)
        ok(co != o, f'{where}: the conjugate has the same sign')
        if a <= 1:
            note(f'{where}: new bottom {a} for {P} {o} sqrt({Q}) ("What whole number")')
    # ---------------- quadratics l15
    elif fam == 'cancel-common-bracket':
        (top, bot), (_, den) = fracs(p)[:2]
        v = sorted(E(top).free_symbols, key=str)[0]
        want = sp.cancel(E(top) / E(bot) * E(den))
        ok(want.is_polynomial(v) and sp.expand(want - E(a)) == 0, f'{where}: answer {a} against {want}')
        g = sp.gcd(E(top), E(bot))
        ok(sp.expand(g - E(w['shared-bracket'])) == 0, f'{where}: shared-bracket')
        ok(sp.simplify(E(w['whole'].replace('\\frac', '').replace('}{', ')/(')) - E(a) / E(den)) == 0, f'{where}: whole')
        ok(sp.expand(E(w['sign-slip']) - E(a)) != 0, f'{where}: sign-slip differs')
        ok(sp.degree(g, v) == 1 and sp.gcd(E(a), E(den)) == 1, f'{where}: one bracket cancels and the result is in lowest terms')
    elif fam in ('multiply-and-cancel', 'divide-and-cancel'):
        (t1, b1), (t2, b2) = fracs(p)[:2]
        val = E(t1) / E(b1) * E(t2) / E(b2) if fam == 'multiply-and-cancel' else E(t1) / E(b1) / (E(t2) / E(b2))
        ok(sp.simplify(val - E(a)) == 0, f'{where}: answer {a} against {sp.factor(val)}')
        x0 = Fr(37, 10)
        v = sorted(E(a).free_symbols, key=str)[0]
        ok(close(val.subs(v, x0), E(a).subs(v, x0), 1e-9), f'{where}: answer at a point')
        for k, t in w.items():
            ok(sp.simplify(E(t) - E(a)) != 0, f'{where}: wrong {k} differs')
        if fam == 'multiply-and-cancel':
            lead = re.match(r'(-?\d*)\(', a)
            if not lead or lead.group(1) in ('', '1', '-'):
                note(f'{where}: "a number times one bracket" but the answer is {a}')
        ok(sp.cancel(val).is_polynomial(v), f'{where}: the result is a polynomial')
    # ---------------- quadratics l16
    elif fam in ('add-tops', 'subtract-tops'):
        (pp, d1), (qq, d2) = fracs(p)[:2]
        sgn = 1 if fam == 'add-tops' else -1
        top = sp.expand(E(pp) * E(d2) + sgn * E(qq) * E(d1))
        ok(sp.expand(top - E(a)) == 0, f'{where}: answer {a} against {top}')
        v = sorted(E(d1).free_symbols, key=str)[0]
        ok(sp.simplify(E(pp) / E(d1) + sgn * E(qq) / E(d2) - top / (E(d1) * E(d2))) == 0, f'{where}: the whole fraction')
        ok(sp.expand(E(w['own-bottoms']) - (E(pp) * E(d1) + sgn * E(qq) * E(d2))) == 0, f'{where}: own-bottoms')
        if fam == 'add-tops':
            ok(sp.expand(E(w['tops-added']) - (E(pp) + E(qq))) == 0, f'{where}: tops-added')
        else:
            lost = E(pp) * E(d2) - E(qq) * v + E(qq) * (E(d1) - v)
            ok(sp.expand(E(w['sign-lost']) - lost) == 0, f"{where}: sign-lost {w['sign-lost']} against {sp.expand(lost)}")
        named = re.search(r'over \$(.*?)\$', p).group(1)
        ok(sp.expand(E(named) - E(d1) * E(d2)) == 0, f'{where}: the named denominator')
        ok(E(d1) != E(d2), f'{where}: the two bottoms are the same')
        co = sp.Poly(top, v).all_coeffs()
        if len(co) < 2 or co[0] == 0 or (len(co) == 2 and co[1] == 0):
            note(f'{where}: the top is {top}')
        if math.gcd(*[int(c) for c in co]) > 1:
            note(f'{where}: the top {top} has a common factor; does the factorised form pass "simplified"?')
    elif fam == 'solve-two-roots':
        x = sp.Symbol('x')
        (aa, d1), (bb, d2) = fracs(p)[:2]
        sol = sp.solveset(sp.Eq(E(aa) / E(d1) + E(bb) / E(d2), 1), x, domain=sp.S.Reals)
        ok(set(sol) == set(a), f'{where}: answers {a} against {sol}')
        for r in a:
            ok(E(d1).subs(x, r) != 0 and E(d2).subs(x, r) != 0 and Fr(int(E(aa)), int(E(d1).subs(x, r))) + Fr(int(E(bb)), int(E(d2).subs(x, r))) == 1, f'{where}: root {r} by substitution')
        ok(set(int(t) for t in w['signs'].split(',')) == set(-r for r in a), f'{where}: signs')
        if set(-r for r in a) == set(a):
            note(f'{where}: roots {a}: the "signs" wrong entry equals the answer')
    elif fam == 'reject-root':
        x = sp.Symbol('x')
        (t1, d1), (t2, d2) = fracs(p)[:2]
        sol = sp.solveset(sp.Eq(E(t1) / E(d1), E(t2) / E(d2) + x), x, domain=sp.S.Reals)
        ok(set(sol) == {a}, f'{where}: answer {a} against {sol}')
        bad = sp.solve(E(d1), x)[0]
        ok(w['kept-bad'] == bad, f'{where}: kept-bad')
        cleared = sp.expand(E(t1) - E(t2) - x * E(d1))
        ok(set(sp.solve(cleared, x)) == {a, bad}, f'{where}: the cleared quadratic has roots {sp.solve(cleared, x)}')
        ok(w['sign'] == -a, f'{where}: sign')
        if re.search(r'\{-?1x\}', p) or t1.startswith('-'):
            note(f'{where}: prompt prints "{t1}" on top')
        if a == bad or -a == bad:
            note(f'{where}: answer {a}, rejected root {bad}: sign entry {w["sign"]} equals kept-bad' if -a == bad else f'{where}: double root')
    # ---------------- quadratics l17
    elif fam == 'remainder':
        x = sp.Symbol('x')
        poly, div = re.search(r'when \$(.*?)\$ is divided by \$\((.*?)\)\$', p).groups()
        q, r = sp.div(E(poly), E(div), x)
        ok(r == a, f'{where}: answer {a} against {r}')
        root = sp.solve(E(div), x)[0]
        ok(E(poly).subs(x, root) == a, f'{where}: by substitution')
        ok(w['sign'] == E(poly).subs(x, -root), f'{where}: sign')
        ok(w['no-constant'] == a - E(poly).subs(x, 0), f'{where}: no-constant')
        if a == 0:
            note(f'{where}: remainder 0')
    elif fam == 'find-k':
        x, k = sp.symbols('x k')
        div, poly = re.search(r'\$\((.*?)\)\$ is a factor of \$(.*?)\$', p).groups()
        poly = E(re.sub(r'\s+', '', poly))
        root = sp.solve(E(div), x)[0]
        ok(sp.solve(poly.subs(x, root), k) == [a], f'{where}: answer')
        ok(sp.rem(poly.subs(k, a), E(div), x) == 0, f'{where}: division leaves no remainder')
        sg = sp.solve(poly.subs(x, -root), k)[0]
        dropped = sp.solve(poly.subs(x, root) - k * root ** 2 + k * root, k)[0]
        ok('sign' not in w or close(sg, w['sign'], 1e-9), f'{where}: sign')
        ok('sign' in w or sg == a, f'{where}: sign dropped with no clash')
        ok('power-dropped' not in w or close(dropped, w['power-dropped'], 1e-9), f'{where}: power-dropped against {dropped}')
        ok('power-dropped' in w or dropped in (a, sg), f'{where}: power-dropped dropped with no clash')
        if 'sign' in w and sg.q != 1:
            note(f'{where}: the sign slip gives k = {sg}, not a whole number')
        if re.search(r'[+-]\s*1x', p) or '+-' in p or '+ -' in p or re.search(r'\+0|-0', p):
            note(f'{where}: prompt prints "{p}"')
    elif fam == 'quotient':
        poly, div = re.search(r'Divide \$(.*?)\$ by \$\((.*?)\)\$', p).groups()
        v = sorted(E(div).free_symbols, key=str)[0]
        q, r = sp.div(E(poly), E(div), v)
        ok(r == 0 and sp.expand(q - E(a)) == 0, f'{where}: answer {a} against {q} remainder {r}')
        root = sp.solve(E(div), v)[0]
        q2, r2 = sp.div(E(poly), v + root, v)
        ok(sp.expand(q2 - E(w['sign'])) == 0, f"{where}: sign {w['sign']} against {q2}")
        ok(sp.expand(E(w['constant-sign']) - (E(a) - 2 * E(a).subs(v, 0))) == 0, f'{where}: constant-sign')
        disc = sp.discriminant(q, v)
        if disc >= 0 and sp.sqrt(disc).is_integer:
            note(f'{where}: the quotient {q} factorises as {sp.factor(q)}; form "expanded" refuses the factorised quotient')
    elif fam == 'factorise-cubic':
        poly = re.search(r'Factorise \$(.*?)\$ fully', p).group(1)
        v = sorted(E(poly).free_symbols, key=str)[0]
        ok(sp.expand(E(poly) - E(a)) == 0, f'{where}: answer expands to the cubic')
        fl = sp.factor_list(E(poly))
        ok(all(sp.degree(f, v) == 1 for f, _ in fl[1]) and sum(e for _, e in fl[1]) == 3, f'{where}: three linear factors')
        ok(a.count('(') == 3 or '^' in a, f'{where}: the key shows three brackets')
        for key, t in w.items():
            ok(sp.expand(E(t) - E(poly)) != 0, f'{where}: wrong {key} differs')
        roots = sp.roots(E(poly), v)
        if any(m > 1 for m in roots.values()) or 0 in roots:
            note(f'{where}: roots {roots} for {poly}, key {a}')
    else:
        ok(False, f'{where}: family {fam} has no check')
    # ---------------- common to all
    vals = [a] if not isinstance(a, list) else []
    if it['kind'] == 'numeric' and not isinstance(a, list):
        ws = [float(x) for x in w.values() if not isinstance(x, str)]
        tol = (it.get('tol') or {}).get('abs', 0)
        ok(all(abs(x - a) > tol for x in ws), f'{where}: a wrong value sits on the answer: {a} {w}')
        ok(len(set(round(x, 9) for x in ws)) == len(ws), f'{where}: two wrong entries share a value: {w}')
    for wv in it.get('wrong') or []:
        for m in re.findall(r'\$(-?\d+(?:\.\d+)?)\$ is', wv['line'][:14]):
            if 'value' in wv and not isinstance(wv['value'], str) and not close(float(m), wv['value'], 0.051):
                ok(False, f"{where}: line of {wv['id']} opens with {m}, value is {wv['value']}")
    if re.search(r'\+\s*-|-\s*-\d|\b1[a-z]\b(?!\w)|\^1\b', re.sub(r'\\[a-z]+', '', p)):
        note(f'{where}: prompt typography: {p}')


d = sys.argv[1]
per = {}
for f in sorted(glob.glob(os.path.join(d, '*.json'))):
    doc = json.load(open(f))
    setid = os.path.basename(f).replace('.json', '')
    c0 = checks
    prompts = set()
    for i, it in enumerate(doc['items']):
        prompts.add(it['prompt'])
        try:
            check(it['family'], it, f"{setid} seed {it['seed']}")
        except Exception as ex:  # a prompt the reader's regex cannot read is itself worth a look
            ok(False, f"{setid} seed {it['seed']}: {type(ex).__name__} {ex} :: {it['prompt']}")
    per[setid] = (len(doc['items']), len(prompts), checks - c0)
for k, (n, u, c) in per.items():
    print(f'{k}: {n} draws, {u} distinct prompts, {c} checks')
seen = {}
for m in notes:
    key = re.sub(r'seed \d+', 'seed *', m)
    key = re.sub(r'-?\d+(\.\d+)?', '#', key)[:70]
    seen.setdefault(key, []).append(m)
print('\nNOTES (for the reader to judge):')
for key, ms in seen.items():
    print(f'  [{len(ms)}] {ms[0]}')
    if len(ms) > 1:
        print(f'        also: {ms[1]}')
print(f'\nfluency-read: {checks} checks, {fails} failures, {len(notes)} notes')
sys.exit(1 if fails else 0)
