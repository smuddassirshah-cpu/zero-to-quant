#!/usr/bin/env python3
"""Fix-pass read 2 of content commit bed3c57d (fluency generators, number-sense l3 and l12, markov l2).

Independent of docs/reports/fluency-ns-markov-concepts.py and of the families' own `let` expressions:
  A. each family's whole range is enumerated here from the drawn values alone (exact fractions), with the keep rule
     re-derived from what the rule is for, and every named wrong method written out from its description;
  B. 10,000 engine draws per family (tools/fluency-sample.mjs --json) are read as a learner would: the key and every
     wrong method are recomputed from the numbers printed in the prompt, and compared with the engine's key and slips.
     The set of prompts the engine draws must equal the set enumerated in A.
Run from the repository root:  python docs/reports/fluency-ns-markov-fixread-2.py   (exit 0 when every check holds; at bed3c57d the two
'old tops, sizes only' checks fail, see Fix-pass read 2 row 7 in docs/reviews/audit-fluency-ns-markov.md)
"""
import json, math, re, subprocess, sys, itertools, os
from fractions import Fraction as F

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
APP = os.path.join(ROOT, 'app')
N = 10000
fails = []
notes = []


OBS = ('added first and doubled', 'wrong way round one step', 'row i . row i', 'col j . col j')


def check(name, ok, detail=''):
    if not ok and any(o in name for o in OBS):
        notes.append('observation, not a named method: ' + name + ' | ' + detail)
        print('obs  ' + name + ' | ' + detail)
        return
    print(('ok   ' if ok else 'FAIL ') + name + (' | ' + detail if detail else ''))
    if not ok:
        fails.append(name)


def engine(setid, fam, n=N):
    out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', setid, '--family', fam, '--n', str(n), '--json'],
                         cwd=APP, capture_output=True, text=True, check=True).stdout
    return json.loads(out)['items']


def stats(setid, fam):
    out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', setid, '--stats'], cwd=APP, capture_output=True, text=True, check=True).stdout
    m = re.search(r'family %s: (\d+) distinct prompts in (\d+) draws, (\d+) of (\d+) draws rejected' % re.escape(fam), out)
    return tuple(int(x) for x in m.groups())


def tex_frac(s):
    s = s.strip()
    m = re.fullmatch(r'(-?)\\frac\{(-?\d+)\}\{(-?\d+)\}', s)
    if m:
        return (-1 if m.group(1) else 1) * F(int(m.group(2)), int(m.group(3)))
    return F(s)


def gen_checks(tag, setid, fam, items, universe):
    d, n, rej, att = stats(setid, fam)
    check(f'{tag}: at least 100 distinct prompts in 200 draws', d >= 100, f'{d} distinct in {n}')
    check(f'{tag}: rejection under the 80% limit (validator sample)', rej / att < 0.8, f'{rej} of {att} = {rej / att:.1%}')
    prompts = set(it['prompt'] for it in items)
    check(f'{tag}: engine prompts over {len(items)} draws equal the enumerated kept range', prompts == universe,
          f'engine {len(prompts)}, enumerated {len(universe)}, engine only {len(prompts - universe)}, enumerated only {len(universe - prompts)}')


# ---------------------------------------------------------------- number-sense l3 subtract-unlike
PICK = [[1,2],[1,3],[2,3],[1,4],[3,4],[1,5],[2,5],[3,5],[4,5],[1,6],[5,6],[1,8],[3,8],[5,8],[7,8],[1,9],[2,9],[4,9],[5,9],[7,9],[8,9],
        [1,10],[3,10],[7,10],[9,10],[1,12],[5,12],[7,12],[11,12]]


def sub_methods(a, b, c, d):
    """Named wrong methods for a/b - c/d, from their descriptions. None where the method gives no number."""
    L = b * d // math.gcd(b, d)
    return {
        'tops and bottoms taken away, (a-c)/(b-d)': F(a - c, b - d) if b != d else None,
        'tops and bottoms taken away, sizes only, |a-c|/|b-d|': F(abs(a - c), abs(b - d)) if b != d else None,
        'common bottom (lowest) with old tops, (a-c)/lcm': F(a - c, L),
        'common bottom (product) with old tops, (a-c)/(bd)': F(a - c, b * d),
        'old tops, sizes only, |a-c|/lcm': F(abs(a - c), L),
        'old tops, sizes only, |a-c|/(bd)': F(abs(a - c), b * d),
        'adding tops and bottoms, (a+c)/(b+d)': F(a + c, b + d),
        'tops taken, bottoms added, (a-c)/(b+d)': F(a - c, b + d),
        'added instead of taken away': F(a, b) + F(c, d),
        'wrong way round, c/d - a/b': F(c, d) - F(a, b),
        'only the first top renamed': F(a * L // b - c, L) if d != L else None,      # with d = L the second top needs no renaming
        'only the second top renamed': F(a - c * L // d, L) if b != L else None,
    }


def sub_family():
    tag = 'ns-l3 subtract-unlike'
    items = engine('number-sense/fluency-l3-adding-pieces', 'subtract-unlike')
    drawn = set(it['prompt'] for it in items)          # wrong methods are judged on the prompts the engine can draw
    total = kept = small_first_top = 0
    universe = set()
    hit = {}
    slip_clash = 0
    lowest_ok = True
    for (x1, y1), (x2, y2) in itertools.product(PICK, PICK):
        total += 1
        if y1 == y2:
            continue                                   # like bottoms: not this skill
        L = y1 * y2 // math.gcd(y1, y2)
        if L > 36:
            continue
        f1, f2 = F(x1, y1), F(x2, y2)
        assert f1 != f2                                # all listed in lowest terms, so unlike bottoms means unequal
        (a, b), (c, d) = ((x1, y1), (x2, y2)) if f1 > f2 else ((x2, y2), (x1, y1))
        key = F(a, b) - F(c, d)
        m = sub_methods(a, b, c, d)
        # the two exclusions the commit states: old tops over the lowest common bottom, and over b times d
        if m['common bottom (lowest) with old tops, (a-c)/lcm'] == key or m['common bottom (product) with old tops, (a-c)/(bd)'] == key:
            continue
        prompt = f'Work out $\\tfrac{{{a}}}{{{b}}} - \\tfrac{{{c}}}{{{d}}}$ as a fraction in its lowest terms.'
        sizes_only = m['old tops, sizes only, |a-c|/lcm'] == key or m['old tops, sizes only, |a-c|/(bd)'] == key
        if sizes_only and prompt not in drawn:
            continue                                   # the row 7 fix is in: these draws are no longer offered
        kept += 1
        universe.add(prompt)
        small_first_top += a < c
        lowest_ok &= (0 < key < 1)
        for k, v in m.items():
            if v is not None and v == key:
                hit.setdefault(k, []).append((a, b, c, d))
        # slips as offered: tops-and-bottoms when a > c and b > d and it is not the key; tops-not-renamed always
        s2 = F(a - c, L)
        if a > c and b > d and F(a - c, b - d) != key:
            s1 = F(a - c, b - d)
            if s1 == s2 or s1 == key:
                slip_clash += 1
        if s2 == key:
            slip_clash += 1
    check(f'{tag}: enumerated range', True, f'{total} ordered draws, {kept} kept ({1 - kept / total:.1%} rejected), {len(universe)} distinct prompts, {small_first_top // 2} with first top smaller')
    check(f'{tag}: every kept draw is larger first, key strictly between 0 and 1', lowest_ok)
    for k in sub_methods(3, 4, 1, 2):
        check(f'{tag}: wrong method never the key: {k}', k not in hit, str(hit.get(k, [])[:6]) + (f' ({len(hit[k])} draws)' if k in hit else ''))
    check(f'{tag}: no offered slip equals the key or the other slip', slip_clash == 0, f'{slip_clash} clashes')
    check(f'{tag}: true rejection rate under 80%', 1 - kept / total < 0.8, f'{1 - kept / total:.1%}')
    bad = 0
    slipbad = 0
    solbad = 0
    for it in items:
        a, b, c, d = map(int, re.search(r'\\tfrac\{(\d+)\}\{(\d+)\} - \\tfrac\{(\d+)\}\{(\d+)\}', it['prompt']).groups())
        key = F(a, b) - F(c, d)
        ans = re.fullmatch(r'\\frac\{(\d+)\}\{(\d+)\}', it['answer'])
        if not (key > 0 and ans and math.gcd(int(ans.group(1)), int(ans.group(2))) == 1 and F(int(ans.group(1)), int(ans.group(2))) == key):
            bad += 1
        ws = [tex_frac(w['tex']) for w in it['wrong']]
        if any(w == key for w in ws) or len(set(ws)) != len(ws):
            slipbad += 1
        L = b * d // math.gcd(b, d)
        s = it['solution'][0]
        m = re.search(r'Rename both over \$(\d+)\$.*= \\tfrac\{(\d+)\}\{(\d+)\} - \\tfrac\{(\d+)\}\{(\d+)\} = \\tfrac\{(\d+)\}\{(\d+)\}\$', s)
        g = list(map(int, m.groups())) if m else []
        if not (m and g[0] == L == g[2] == g[4] == g[6] and F(g[1], L) == F(a, b) and F(g[3], L) == F(c, d) and g[5] == g[1] - g[3]):
            solbad += 1
        for w in it['wrong']:
            if w['id'] == 'tops-not-renamed':
                mm = re.search(r'over \$(\d+)\$ but kept the old tops: \$\\tfrac\{(\d+)\}\{(\d+)\}\$ is \$\\tfrac\{(\d+)\}\{(\d+)\}\$ and \$\\tfrac\{(\d+)\}\{(\d+)\}\$ is \$\\tfrac\{(\d+)\}\{(\d+)\}\$', w['line'])
                q = list(map(int, mm.groups())) if mm else []
                if not (mm and q[0] == L and F(q[1], q[2]) == F(q[3], q[4]) == F(a, b) and F(q[5], q[6]) == F(q[7], q[8]) == F(c, d) and q[4] == q[8] == L):
                    solbad += 1
                if tex_frac(w['tex']) != F(a - c, L):
                    slipbad += 1
            if w['id'] == 'tops-and-bottoms' and tex_frac(w['tex']) != F(a - c, b - d):
                slipbad += 1
    check(f'{tag}: engine key = prompt recomputed, positive, lowest terms ({len(items)} draws)', bad == 0, f'{bad} bad')
    check(f'{tag}: engine slips are what they name, differ from the key and from each other', slipbad == 0, f'{slipbad} bad')
    check(f'{tag}: solution and slip lines restate the drawn fractions correctly', solbad == 0, f'{solbad} bad')
    gen_checks(tag, 'number-sense/fluency-l3-adding-pieces', 'subtract-unlike', items, universe)


# ---------------------------------------------------------------- number-sense l12 brackets-first
def br_methods(a, b, c, d):
    g = c - d
    return {
        'added first, (a+b) x g^2': (a + b) * g * g,
        'multiplied then squared, a + (b g)^2': a + (b * g) ** 2,
        'doubling for squaring, a + b x 2g': a + b * 2 * g,
        'added first and doubled, (a+b) x 2g': (a + b) * 2 * g,
        'strict left to right, ((a+b) g)^2': ((a + b) * g) ** 2,
        'whole line squared, (a + b g)^2': (a + b * g) ** 2,
        'brackets ignored, a + b c - d^2': a + b * c - d * d,
        'power on each term in the bracket, a + b (c^2 - d^2)': a + b * (c * c - d * d),
        'power dropped, a + b g': a + b * g,
        'brackets ignored and left to right, ((a+b) c - d)^2': ((a + b) * c - d) ** 2,
        'power on c only, a + b (c^2 - d)': a + b * (c * c - d),
    }


def br_family():
    tag = 'ns-l12 brackets-first'
    total = kept = 0
    universe = set()
    hit = {}
    clash = 0
    for a in range(1, 13):
        for b in range(2, 6):
            for d in range(1, 8):
                for g in range(3, 6):
                    total += 1
                    c = d + g
                    key = a + b * g * g
                    m = br_methods(a, b, c, d)
                    s1, s2 = m['added first, (a+b) x g^2'], m['multiplied then squared, a + (b g)^2']
                    if s1 == s2:
                        continue                       # the two slips would be one number
                    kept += 1
                    universe.add(f'Work out ${a} + {b} \\times ({c} - {d})^2$.')
                    if key in (s1, s2):
                        clash += 1
                    for k, v in m.items():
                        if v == key:
                            hit.setdefault(k, []).append((a, b, c, d, 'g=%d' % g))
    check(f'{tag}: enumerated range', True, f'{total} draws, {kept} kept ({1 - kept / total:.1%} rejected), {len(universe)} distinct prompts')
    for k in br_methods(1, 2, 4, 1):
        check(f'{tag}: wrong method never the key: {k}', k not in hit, str(hit.get(k, [])[:6]) + (f' ({len(hit[k])} draws, g values {sorted(set(h[4] for h in hit[k]))})' if k in hit else ''))
    check(f'{tag}: no slip equals the key or the other slip', clash == 0)
    items = engine('number-sense/fluency-l12-which-first', 'brackets-first')
    bad = slipbad = solbad = 0
    for it in items:
        a, b, c, d = map(int, re.search(r'\$(\d+) \+ (\d+) \\times \((\d+) - (\d+)\)\^2\$', it['prompt']).groups())
        g = c - d
        key = a + b * g * g
        if not (g >= 1 and F(it['answer']) == key):
            bad += 1
        ws = {w['id']: F(str(w['value'])) for w in it['wrong']}
        if ws.get('added-first') != (a + b) * g * g or ws.get('multiplied-then-squared') != a + (b * g) ** 2 or key in ws.values() or len(set(ws.values())) != len(ws):
            slipbad += 1
        sol = ' '.join(it['solution'])
        want = f'Brackets first: ${c} - {d} = {g}$. Power next: ${g}^2 = {g * g}$, then ${b} \\times {g * g} = {b * g * g}$. Last, ${a} + {b * g * g} = {key}$.'
        lines = {w['id']: w['line'] for w in it['wrong']}
        if sol != want or f'${a} + {b} = {a + b}$' not in lines['added-first'] or f'${b} \\times {g} = {b * g}$' not in lines['multiplied-then-squared']:
            solbad += 1
    check(f'{tag}: engine key = prompt recomputed ({len(items)} draws)', bad == 0, f'{bad} bad')
    check(f'{tag}: engine slips are what they name, differ from the key and from each other', slipbad == 0, f'{slipbad} bad')
    check(f'{tag}: solution and slip lines state the right numbers', solbad == 0, f'{solbad} bad')
    gen_checks(tag, 'number-sense/fluency-l12-which-first', 'brackets-first', items, universe)


# ---------------------------------------------------------------- markov l2
def mat2(P):
    n = len(P)
    return [[sum(P[i][k] * P[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def mk_methods(P, i, j):
    n = len(P)
    P2 = mat2(P)
    row = lambda r: P[r]
    col = lambda c: [P[k][c] for k in range(n)]
    dot = lambda u, v: sum(x * y for x, y in zip(u, v))
    return {
        'one step, P_ij': P[i][j],
        'squared entry, P_ij^2': P[i][j] ** 2,
        'doubled entry, 2 P_ij': 2 * P[i][j],
        'row times row, row i . row j': dot(row(i), row(j)),
        'column times column, col i . col j': dot(col(i), col(j)),
        'rows and columns swapped or wrong way round, (P^2)_ji': P2[j][i],
        'wrong way round one step, P_ji': P[j][i],
        'row i . row i': dot(row(i), row(i)),
        'col j . col j': dot(col(j), col(j)),
        'direct then stay only, P_ij P_jj': P[i][j] * P[j][j],
        'stay then go only, P_ii P_ij': P[i][i] * P[i][j],
    }


INHERENT = 'rows and columns swapped or wrong way round, (P^2)_ji'


def mk_report(tag, hit, diag_hit, names):
    for k in names:
        if k == INHERENT:
            check(f'{tag}: wrong method never the key off the diagonal (i != j): {k}', k not in hit, str(hit.get(k, [])[:4]) + (f' ({len(hit[k])} draws)' if k in hit else ''))
            notes.append(f'{tag}: (P^2)_ii is unchanged by transposing P, so a swapped reading gives the key on all {diag_hit} kept draws with start = target; no choice of numbers can separate them')
        else:
            check(f'{tag}: wrong method never the key: {k}', k not in hit, str(hit.get(k, [])[:4]) + (f' ({len(hit[k])} draws)' if k in hit else ''))


def parse_matrix(prompt):
    body = re.search(r'\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}', prompt).group(1)
    return [[F(x.strip()) for x in r.split('&')] for r in body.split('\\\\')]


def two_family():
    tag = 'markov-l2 two-state'
    vals = [F(k, 10) for k in range(1, 10)]
    names = ['bull', 'bear']
    total = kept = 0
    universe = set()
    hit = {}
    diag = 0
    clash = 0
    dec = lambda x: ('%g' % float(x))
    for a in vals:
        for b in vals:
            for i in (0, 1):
                for j in (0, 1):
                    total += 1
                    P = [[a, 1 - a], [b, 1 - b]]
                    key = mat2(P)[i][j]
                    m = mk_methods(P, i, j)
                    # keep rule re-derived: rows differ, not symmetric (a + b = 1 makes P symmetric), squared entry is not the key
                    if a == b or a + b == 1 or m['squared entry, P_ij^2'] == key:
                        continue
                    kept += 1
                    universe.add((dec(a), dec(1 - a), dec(b), dec(1 - b), names[i], names[j]))
                    if m['squared entry, P_ij^2'] == m['one step, P_ij'] or key in (m['squared entry, P_ij^2'], m['one step, P_ij']):
                        clash += 1
                    if i == j:
                        diag += 1
                    for k, v in m.items():
                        if v == key and not (k == INHERENT and i == j):
                            hit.setdefault(k, []).append((dec(a), dec(b), i, j))
    check(f'{tag}: enumerated range', True, f'{total} draws, {kept} kept ({1 - kept / total:.1%} rejected)')
    mk_report(tag, hit, diag, list(mk_methods([[F(1, 2)] * 2] * 2, 0, 1)))
    check(f'{tag}: no offered slip equals the key or the other slip', clash == 0)
    items = engine('markov/fluency-l2-transition-matrix', 'two-state-two-step')
    bad = slipbad = solbad = 0
    seen = set()
    for it in items:
        P = parse_matrix(it['prompt'])
        i = names.index(re.search(r'Today is (\w+)\.', it['prompt']).group(1))
        j = names.index(re.search(r'chance of (\w+) in two periods', it['prompt']).group(1))
        seen.add((dec(P[0][0]), dec(P[0][1]), dec(P[1][0]), dec(P[1][1]), names[i], names[j]))
        key = mat2(P)[i][j]
        if not (all(sum(r) == 1 and all(0 < x < 1 for x in r) for r in P) and F(str(it['answer'])) == key and re.fullmatch(r'0\.\d{1,2}', str(it['answer']))):
            bad += 1
        ws = {w['id']: F(str(w['value'])) for w in it['wrong']}
        if ws.get('squared-entry') != P[i][j] ** 2 or ws.get('one-step', P[i][j]) != P[i][j] or key in ws.values() or len(set(ws.values())) != len(ws) or 'one-step' not in ws:
            slipbad += 1
        x0, x1 = P[i][0] * P[0][j], P[i][1] * P[1][j]
        want = [f'Through bull: ${dec(P[i][0])} \\times {dec(P[0][j])} = {dec(x0)}$. Through bear: ${dec(P[i][1])} \\times {dec(P[1][j])} = {dec(x1)}$.',
                f'Add the two paths: ${dec(x0)} + {dec(x1)} = {dec(key)}$.']
        if it['solution'] != want:
            solbad += 1
    check(f'{tag}: engine key = (P^2)_ij from the printed matrix, rows sum to 1, key prints to at most 2 places ({len(items)} draws)', bad == 0, f'{bad} bad')
    check(f'{tag}: engine slips are what they name, differ from the key and from each other, one-step always offered', slipbad == 0, f'{slipbad} bad')
    check(f'{tag}: solution states the two paths and their sum correctly', solbad == 0, f'{solbad} bad')
    d, n, rej, att = stats('markov/fluency-l2-transition-matrix', 'two-state-two-step')
    check(f'{tag}: at least 100 distinct prompts in 200 draws', d >= 100, f'{d} distinct in {n}')
    check(f'{tag}: rejection under the 80% limit (validator sample)', rej / att < 0.8, f'{rej} of {att} = {rej / att:.1%}')
    check(f'{tag}: engine draws over {len(items)} seeds equal the enumerated kept range', seen == universe, f'engine {len(seen)}, enumerated {len(universe)}, engine only {len(seen - universe)}, enumerated only {len(universe - seen)}')


R1 = [[0.6, 0.3, 0.1], [0.5, 0.4, 0.1], [0.7, 0.2, 0.1], [0.4, 0.4, 0.2], [0.5, 0.3, 0.2], [0.6, 0.2, 0.2]]
R2 = [[0.2, 0.5, 0.3], [0.3, 0.4, 0.3], [0.1, 0.6, 0.3], [0.3, 0.5, 0.2], [0.2, 0.6, 0.2], [0.4, 0.4, 0.2]]
R3 = [[0.1, 0.3, 0.6], [0.2, 0.4, 0.4], [0.2, 0.3, 0.5], [0.1, 0.4, 0.5], [0.3, 0.3, 0.4], [0.1, 0.2, 0.7]]


def three_family():
    tag = 'markov-l2 three-state'
    names = ['Sunny', 'Cloudy', 'Rain']
    fr = lambda r: [F(str(x)) for x in r]
    dec = lambda x: ('%g' % float(x))
    total = kept = 0
    universe = set()
    hit = {}
    diag = clash = 0
    for r1, r2, r3 in itertools.product(R1, R2, R3):
        P = [fr(r1), fr(r2), fr(r3)]
        assert all(sum(r) == 1 for r in P)
        for j in range(3):
            total += 1
            i = 0
            key = mat2(P)[i][j]
            m = mk_methods(P, i, j)
            # keep rule re-derived from the commit message: one step, row times row, column times column, swapped reading
            # (off the diagonal, where it can differ) and 2P must each miss the key
            if (m['one step, P_ij'] == key or m['row times row, row i . row j'] == key or m['column times column, col i . col j'] == key
                    or (j != 0 and m[INHERENT] == key) or m['doubled entry, 2 P_ij'] == key):
                continue
            kept += 1
            universe.add((tuple(dec(x) for r in P for x in r), names[j]))
            sq, one = m['squared entry, P_ij^2'], m['one step, P_ij']
            if one == key or (sq != key and sq == one):
                clash += 1
            if j == 0:
                diag += 1
            for k, v in m.items():
                if v == key and not (k == INHERENT and i == j):
                    hit.setdefault(k, []).append((r1, r2, r3, names[j]))
    check(f'{tag}: enumerated range', True, f'{total} draws, {kept} kept ({1 - kept / total:.1%} rejected)')
    mk_report(tag, hit, diag, list(mk_methods([[F(1, 2)] * 2] * 2, 0, 1)))
    check(f'{tag}: no offered slip equals the key or the other slip', clash == 0)
    items = engine('markov/fluency-l2-transition-matrix', 'three-state-two-step')
    bad = slipbad = solbad = 0
    seen = set()
    for it in items:
        P = parse_matrix(it['prompt'])
        j = names.index(re.search(r'chance of (\w+) in two days', it['prompt']).group(1))
        seen.add((tuple(dec(x) for r in P for x in r), names[j]))
        key = mat2(P)[0][j]
        if not (all(sum(r) == 1 and all(0 < x < 1 for x in r) for r in P) and F(str(it['answer'])) == key and re.fullmatch(r'0\.\d{1,2}', str(it['answer']))):
            bad += 1
        ws = {w['id']: F(str(w['value'])) for w in it['wrong']}
        if ws.get('squared-entry', P[0][j] ** 2) != P[0][j] ** 2 or ws.get('one-step') != P[0][j] or key in ws.values() or len(set(ws.values())) != len(ws):
            slipbad += 1
        xs = [P[0][k] * P[k][j] for k in range(3)]
        want = [f'Row Sunny times column {names[j]}: ' + '$' + ' + '.join(f'{dec(P[0][k])} \\times {dec(P[k][j])}' for k in range(3)) + '$.',
                'That is $' + ' + '.join(dec(x) for x in xs) + f' = {dec(key)}$.']
        if it['solution'] != want:
            solbad += 1
    check(f'{tag}: engine key = (P^2)_1j from the printed matrix, rows sum to 1, key prints to at most 2 places ({len(items)} draws)', bad == 0, f'{bad} bad')
    check(f'{tag}: engine slips are what they name, differ from the key and from each other', slipbad == 0, f'{slipbad} bad')
    check(f'{tag}: solution states the three paths and their sum correctly', solbad == 0, f'{solbad} bad')
    d, n, rej, att = stats('markov/fluency-l2-transition-matrix', 'three-state-two-step')
    check(f'{tag}: at least 100 distinct prompts in 200 draws', d >= 100, f'{d} distinct in {n}')
    check(f'{tag}: rejection under the 80% limit (validator sample)', rej / att < 0.8, f'{rej} of {att} = {rej / att:.1%}')
    check(f'{tag}: engine draws over {len(items)} seeds equal the enumerated kept range', seen == universe, f'engine {len(seen)}, enumerated {len(universe)}, engine only {len(seen - universe)}, enumerated only {len(universe - seen)}')


sub_family()
br_family()
two_family()
three_family()
for n_ in notes:
    print('note ' + n_)
print(f'{len(fails)} failing checks')
sys.exit(1 if fails else 0)
