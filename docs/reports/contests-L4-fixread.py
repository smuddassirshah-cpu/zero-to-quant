"""Fix-pass read, contests level 4, round 1: checks on the text changed by commit c71901d3.

Run from the repo root with Python 3.13 (the venv): python docs/reports/contests-L4-fixread.py
Exit 0 when every check holds. Each check is tied to a JSON path in the `## Fix-pass read` table of
docs/reviews/audit-contests-4.md.

1. Code-widget feedback keys: the mistake each new or changed `feedback.byKey.test-N` line names is written
   as a submission and run against the widget's hidden tests in order, the way js/engine/widgets/code.js does
   (prelude and learner code loaded once into one namespace, then per test: setup, eval(call), compare with
   eval(expect); an exception in a test fails that test; key = test-(first failing index + 1)). Recursion limit
   3000 as in js/screens/drill-worker.js.
2. Numbers in the changed prose are recomputed (l14 screens 0, 4, 6, 11; homework item 0).
3. Sentences that cite "the curriculum" are matched against docs/curriculum.md.
4. Voice gates on every changed string: no exclamation mark, no em-dash, no sentence over 35 words, `explain`
   of at most three sentences.
"""
import json, math, os, random, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
CDIR = os.path.join(ROOT, 'app', 'content', 'courses', 'contests')
bad = 0


def check(name, ok, detail=''):
    global bad
    print(('ok   ' if ok else 'FAIL ') + name + ('' if ok else '  ' + str(detail)))
    if not ok:
        bad += 1


def load(f):
    with open(os.path.join(CDIR, f + '.json'), encoding='utf8') as fh:
        return json.load(fh)


L13, L14, L15, L16, HW = (load(f) for f in ('l13-virtual-contest', 'l14-which-first', 'l15-debugging-under-time', 'l16-upsolving', 'homework-4'))
DOCS = {'l13-virtual-contest': L13, 'l14-which-first': L14, 'l15-debugging-under-time': L15, 'l16-upsolving': L16, 'homework-4': HW}


# ---------- 1. the code widget's judge, in native Python ----------
def _same(x, y):
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_same(p, q) for p, q in zip(x, y))
    return bool(x == y)


def _close(x, y):
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_close(p, q) for p, q in zip(x, y))
    try:
        return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return x == y


def first_fail(widget, src):
    """1-based index of the first failing hidden test, 0 if all pass, -1 on a load error."""
    sys.setrecursionlimit(3000)
    ns = {'__name__': '__main__'}
    try:
        exec(widget.get('prelude', '') + '\n' + src, ns)
    except BaseException:
        return -1
    first = 0
    for i, t in enumerate(widget['tests']):
        ok = False
        try:
            if t.get('setup'):
                exec(t['setup'], ns)
            a = eval(t['call'], ns)
            e = eval(t['expect'], ns)
            ok = _close(a, e) if t.get('compare') == 'isclose' else _same(a, e)
        except BaseException:
            ok = False
        if not ok and not first:
            first = i + 1          # later tests still run, as on the page (module state carries on)
    return first


def key_check(label, widget, byKey, n, subs):
    check(f'{label}: byKey has test-{n}', f'test-{n}' in byKey)
    check(f'{label}: the solution passes every hidden test', first_fail(widget, widget['solution']) == 0)
    check(f'{label}: the starter does not pass', first_fail(widget, widget['starter']) != 0)
    for name, src in subs:
        got = first_fail(widget, src)
        check(f'{label}: "{name}" fails first at test {n}', got == n, f'first failure at {got}')


# l13 screens[3] test-5: `>=` in place of `>`
w = L13['screens'][3]
key_check('l13 s3 test-5', w['widget'], w['feedback']['byKey'], 5, [('>= on both sides', '''
def peaks(closes):
    count = 0
    for i in range(1, len(closes) - 1):
        if closes[i] >= closes[i - 1] and closes[i] >= closes[i + 1]:
            count += 1
    return count
''')])
check('l13 s3: test 5 is 2 2 2 2 and test 6 the plateau 1 3 3 1', w['widget']['tests'][4]['call'] == 'peaks([2, 2, 2, 2])' and w['widget']['tests'][5]['call'] == 'peaks([1, 3, 3, 1])')
codes = [s for s in L13['screens'] if s.get('widget', {}).get('kind') == 'code']
rates = [int(re.search(r'about (\d+)', s['prose']).group(1)) for s in codes]
check('l13 s2 option rating: code screens give ratings from about 800 to about 1500', rates and min(rates) == 800 and max(rates) == 1500, rates)
check('l13 s1: D has a note', any(l.startswith('Note:') for l in L13['screens'][1]['canvas']['controls'][0]['frames'][3]['lines']))

# l14 screens[4] test-2: the floor applied before the attempt cost, or not at all
w = L14['screens'][4]
key_check('l14 s4 test-2', w['widget'], w['feedback']['byKey'], 2, [
    ('floor before the attempt cost', 'def decayed_score(value, minute, wrong, per_minute, per_wrong, floor):\n    return max(floor * value, value - per_minute * minute) - per_wrong * wrong\n'),
    ('no floor', 'def decayed_score(value, minute, wrong, per_minute, per_wrong, floor):\n    return value - per_minute * minute - per_wrong * wrong\n')])
check('l14 s4 test-2 figures: 500 - 240 - 150 = 110 < 150', 500 - 2 * 120 - 50 * 3 == 110 and 0.3 * 500 == 150 and w['widget']['tests'][1]['call'] == 'decayed_score(500, 120, 3, 2, 50, 0.3)')

# l14 screens[5] test-5: a bare `if minute:`
w = L14['screens'][5]
key_check('l14 s5 test-5', w['widget'], w['feedback']['byKey'], 5, [('bare if minute', '''
def icpc_rank_key(results, per_wrong=20):
    solved, penalty = 0, 0
    for minute, wrong in results:
        if minute:
            solved += 1
            penalty += minute + per_wrong * wrong
    return (-solved, penalty)
''')])
check('l14 s5: test 5 is a solve at minute 0 after five rejections', w['widget']['tests'][4]['call'] == 'icpc_rank_key([(0, 5)])')

# l15 screens[5] test-3: a set outside solve_all, emptied between cases but not at the start of a call
w = L15['screens'][5]
key_check('l15 s5 test-3', w['widget'], w['feedback']['byKey'], 3, [('outside set, cleared only between cases', '''
seen = set()


def solve_all(text):
    data = text.split()
    t = int(data[0])
    pos = 1
    out = []
    for k in range(t):
        if k > 0:
            seen.clear()
        n = int(data[pos])
        pos += 1
        for s in data[pos:pos + n]:
            seen.add(s)
        pos += n
        out.append(len(seen))
    return out
''')])
check('l15 s5: the starter (set never emptied) fails first at test 2', first_fail(w['widget'], w['widget']['starter']) == 2)
check('l15 s5: test 3 starts with AAA alone', w['widget']['tests'][2]['call'].startswith("solve_all('3\\n1\\nAAA\\n"))

# l15 screens[9] test-3: lengths 1 and 2 only
w = L15['screens'][9]
key_check('l15 s9 test-3', w['widget'], w['feedback']['byKey'], 3, [('lengths 1 and 2 only', '''
def smallest_failing(fast, brute, gen, seed):
    for n in range(1, 3):
        case = stress(fast, brute, lambda rng: gen(rng, n), 200, seed)
        if case is not None:
            return case
    return None
''')])
check('l15 s9: test 3 needs three values', w['widget']['tests'][2]['expect'] == '[2, 1, 1]')
check('l15 s2: lesson 4 is the stress-testing lesson', os.path.exists(os.path.join(CDIR, 'l4-stress-testing.json')))

# l16 screens[5] test-1: sorted by count only
w = L16['screens'][5]
key_check('l16 s5 test-1', w['widget'], w['feedback']['byKey'], 1, [
    ('count only, stable', 'def mistakes_summary(log):\n    c = {}\n    for p, k in log:\n        c[k] = c.get(k, 0) + 1\n    return sorted(c.items(), key=lambda kv: -kv[1])\n'),
    ('Counter.most_common', 'from collections import Counter\n\ndef mistakes_summary(log):\n    return Counter(k for p, k in log).most_common()\n')])
exp = eval(w['widget']['tests'][0]['expect'])
check('l16 s5 test-1: greedy and misread tie at 2, greedy first', exp[1] == ('greedy without proof', 2) and exp[2] == ('misread a constraint', 2))

# homework items[0] test-2 (isolated desks) and the `how` line (a recursive DFS on test 7)
w = HW['items'][0]
key_check('hw item 0 test-2', w['widget'], w['feedback']['byKey'], 2, [('only desks that have a link are counted', '''
def desks_after_cut(n, links, cut):
    adj = {}
    for i, (a, b) in enumerate(links):
        if i != cut:
            adj.setdefault(a, []).append(b)
            adj.setdefault(b, []).append(a)
    seen, groups = set(), 0
    for s in adj:
        if s in seen:
            continue
        groups += 1
        seen.add(s)
        stack = [s]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
    return groups
''')])
check('hw item 0: a recursive DFS fails first at test 7 under the 3,000 limit', first_fail(w['widget'], '''
def desks_after_cut(n, links, cut):
    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(links):
        if i != cut:
            adj[a].append(b)
            adj[b].append(a)
    seen = [False] * n

    def go(u):
        seen[u] = True
        for v in adj[u]:
            if not seen[v]:
                go(v)
    groups = 0
    for s in range(n):
        if not seen[s]:
            groups += 1
            go(s)
    return groups
''') == 7)
with open(os.path.join(ROOT, 'app', 'js', 'screens', 'drill-worker.js'), encoding='utf8') as fh:
    check('hw item 0 how: the page sets a recursion limit of 3000', 'RECURSION_LIMIT = 3000' in fh.read())
check('hw item 0 how: the cut chain leaves a part of 100,001 desks, so a DFS from desk 0 nests 100,000 calls below the first', 200000 // 2 + 1 == 100001)
check('hw item 0 test-2: the answer is 3', w['widget']['tests'][1]['call'] == 'desks_after_cut(4, [(0, 1), (1, 2)], 1)' and w['widget']['tests'][1]['expect'] == '3')

# homework items[2] test-1: no sort
w = HW['items'][2]
key_check('hw item 2 test-1', w['widget'], w['feedback']['byKey'], 1, [('no sort', w['widget']['solution'].replace('xs = sorted(levels)', 'xs = list(levels)'))])
check('hw item 2: the unsorted submission really differs from the solution', 'xs = sorted(levels)' in w['widget']['solution'])

# ---------- 2. numbers ----------
rows = L14['screens'][0]['canvas']['params']['rows']
check('l14 s0: the table loses v/250 a minute', all(int(r[1].replace(',', '')) / 250 == int(r[3]) for r in rows))

E = lambda x: 1000 * (1 - math.exp(-x / 50)) + 800 * (1 - math.exp(-(60 - x) / 15))
xs = [i / 1000 for i in range(60001)]
xbest = max(xs, key=E)
check('l14 s6: all D about 699, all E about 785', round(E(60)) == 699 and round(E(0)) == 785, (E(60), E(0)))
check('l14 s6: best fixed split about 35 minutes, about 1,152 points', abs(xbest - 34.84) < 0.01 and round(E(xbest)) == 1152 and round(xbest) == 35, (xbest, E(xbest)))
wr = {x['id']: x['region']['x'] for x in L14['screens'][6]['widget']['wrong']}
check('l14 s6: "nearly the whole hour" and "almost no time" match the regions', wr['all'] == [50, 60] and wr['none'] == [0, 8])


def V(c, steps=20000):
    """Leave D when solved or at the cap c; D's solving time is exponential with mean 50, E's with mean 15."""
    h = c / steps
    f = lambda t: math.exp(-t / 50) / 50 * (1000 + 800 * (1 - math.exp(-(60 - t) / 15)))
    integral = sum(f((i + 0.5) * h) for i in range(steps)) * h if c > 0 else 0.0
    return integral + math.exp(-c / 50) * 800 * (1 - math.exp(-(60 - c) / 15))


cbest = max((i / 10 for i in range(601)), key=lambda c: V(c, 2000))
closed = 60 - 15 * math.log(800 / (15 * 20))      # dV/dc = e^(-c/50) (20 - (800/15) e^(-(60-c)/15)) = 0
check('l14 s6 explain: leaving D when solved, the best cap is near 45 minutes', abs(cbest - closed) < 0.11 and 44.5 < closed < 46, (cbest, closed))
rng = random.Random(7)


def sim(c, n=400000):
    tot = 0.0
    for _ in range(n):
        td = rng.expovariate(1 / 50)
        left = 60 - min(td, c)
        tot += (1000 if td <= c else 0) + (800 if rng.expovariate(1 / 15) <= left else 0)
    return tot / n


s35, s45 = sim(35), sim(45)
check('l14 s6 explain: simulation agrees with the integral, and a cap of 45 beats 35', abs(s35 - V(35)) < 4 and abs(s45 - V(45)) < 4 and V(45) - V(35) > 8 and s45 > s35, (s35, V(35), s45, V(45)))

tasks = {'rec': (2000, 20), 'hedge': (12000, 25), 'quote': (3000, 5)}
rate = {k: v / t for k, (v, t) in tasks.items()}
check('l14 s11: £600, £480 and £100 a minute', rate == {'rec': 100, 'hedge': 480, 'quote': 600})
check('l14 s11 explain: at 1% a minute the waits cost £600 and £750', 0.01 * 5 * 12000 == 600 and 0.01 * 25 * 3000 == 750 and 5 + 25 == 30)
from itertools import permutations
unique = True
for r in (0.001, 0.005, 0.01, 0.02, 0.03):
    for until in ('start', 'finish'):
        best = {}
        for order in permutations(tasks):
            clock = total = 0
            for k in order:
                v, t = tasks[k]
                wait = clock if until == 'start' else clock + t
                clock += t
                if clock <= 30:
                    total += v * (1 - r * wait)
            best[order[0]] = max(best.get(order[0], -1), total)
        top = sorted(best.values())
        unique = unique and max(best, key=best.get) == 'quote' and top[-1] > top[-2]
check('l14 s11: with a fixed share lost per minute of waiting, quote first is the unique best first task', unique)
opt = {o['id']: o for o in L14['screens'][11]['widget']['options']}
check('l14 s11: the key is the quote', opt['quote'].get('correct') is True and '480' in opt['hedge']['why'] and '100' in opt['rec']['why'])

check('l16 s1: 6 ways for five zeros, 19,999,700,001 for test 9', math.comb(4, 2) == 6 and math.comb(199999, 2) == 19999700001)
check('l16 s6: E is 700 above 1,200 and C, D are within 300', 1900 - 1200 == 700 and 1500 - 1200 == 300)

# ---------- 3. what the curriculum says ----------
with open(os.path.join(ROOT, 'docs', 'curriculum.md'), encoding='utf8') as fh:
    CUR = fh.read()
for name, needle in [
    ('1,400 as a fair first-year target', 'A rating of 1400 is a fair first-year target'),
    ('one contest a week after 100 problems', 'Start once you have 100 problems behind you and enter one contest a week'),
    ('rating shortlists mainly an Indian campus practice', 'rating-based shortlisting is mainly a feature of Indian campus hiring'),
    ('elsewhere: helps developer, little for trader or researcher', 'Elsewhere a rating helps developer applications and counts for little in trader or researcher interviews'),
    ('trader row', '| Trader | Probability, mental arithmetic, market-making and betting games |'),
    ('researcher row', '| Researcher | Probability, statistics, regression, machine learning, a data take-home |'),
    ('developer row', '| Developer | Algorithms, C++, systems design |'),
    ('a fresh LeetCode medium in 30 minutes', 'a fresh LeetCode medium finished in 30 minutes'),
    ('IMC Prosperity and Kaggle as additions', 'Kaggle competitions on the researcher track, firm-run trading competitions such as IMC Prosperity on the trader track'),
]:
    check('curriculum: ' + name, needle in CUR)
trow = L16['screens'][10]['canvas']['params']['rows']
check('l16 s10: the table rows are the three tracks', [r[0] for r in trow] == ['Developer', 'Trader', 'Researcher'] and 'market-making games' in trow[1][1] and 'take-home' in trow[2][1])

# ---------- 4. voice on every changed string ----------
CHANGED = {
    'l13-virtual-contest': ['screens[1].explain.text', 'screens[2].prose', 'screens[2].widget.options[3].why', 'screens[3].prose', 'screens[3].feedback.byKey.test-5', 'screens[3].explain.text'],
    'l14-which-first': ['screens[0].prose', 'screens[4].feedback.byKey.test-2', 'screens[5].feedback.byKey.test-5', 'screens[6].prose', 'screens[6].feedback.byKey.all', 'screens[6].feedback.byKey.none', 'screens[6].explain.text', 'screens[11].prose', 'screens[11].explain.text'],
    'l15-debugging-under-time': ['screens[0].prose', 'screens[2].explain.text', 'screens[5].feedback.byKey.test-3', 'screens[9].feedback.byKey.test-3', 'screens[10].explain.text', 'summary.ideas[0]'],
    'l16-upsolving': ['screens[0].hints[2].text', 'screens[1].prose', 'screens[5].feedback.byKey.test-1', 'screens[6].feedback.byKey.l4', 'screens[6].explain.text', 'screens[7].widget.options[1].why', 'screens[8].widget.options[2].why', 'screens[10].prose', 'screens[10].widget.options[1].why', 'screens[10].widget.options[2].why', 'screens[10].hints[2].text', 'screens[10].explain.text', 'summary.ideas[2]', 'quiz[3].question', 'quiz[3].widget.options[1].why', 'quiz[3].explain.text'],
    'homework-4': ['items[0].widget.how', 'items[0].feedback.byKey.test-2', 'items[2].feedback.byKey.test-1', 'items[5].prose', 'items[5].widget.options[2].why', 'items[5].widget.options[3].why', 'items[5].feedback.correct', 'items[5].explain.text', 'items[6].widget.model'],
}


def get(doc, path):
    o = doc
    for part in re.findall(r'[^.\[\]]+|\[\d+\]', path):
        o = o[int(part[1:-1])] if part.startswith('[') else o[part]
    return o


def sentences(text):
    t = re.sub(r'\$[^$]*\$|`[^`]*`', 'X', text)
    t = re.sub(r'\*\*[^*]*\.\*\*', 'X.', t)
    return [s for s in re.split(r'(?<=[.?])\s+|\n+', t) if s.strip()]


n_rows = 0
for f, paths in CHANGED.items():
    for p in paths:
        n_rows += 1
        s = get(DOCS[f], p)
        sent = sentences(s)
        longest = max(len(x.split()) for x in sent)
        ok = '!' not in s and '—' not in s and longest <= 35 and '$' not in re.sub(r'\$[^$]*\$', '', s)
        if p.endswith('explain.text'):
            ok = ok and len(sent) <= 3
        ok = ok and not re.search(r'\b(color|center|analyze|practice[sd]?\s+(?:about|market)|favor|behavior)\b', s)
        check(f'voice: {f} {p}', ok, (longest, len(sent)))
check('46 changed strings read', n_rows == 46, n_rows)

print('failures:', bad)
sys.exit(1 if bad else 0)
