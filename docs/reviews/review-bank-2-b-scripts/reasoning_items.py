"""Second reader, bank part 2 (b): run the code shown in every reasoning-about-code and C++ reading item of coding-1 to 4,
and compare with the key, the wrong values and the figures in the feedback. The Python is taken from the item's own prose
(the fenced block), so a change to the item is seen. C++ is compiled with g++ -std=c++20 when one is present.
Exit 0 when every item agrees."""
import io, json, os, re, shutil, subprocess, sys, tempfile, contextlib

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content', 'bank')
ITEMS = {}
for n in (1, 2, 3, 4):
    for it in json.load(open(os.path.join(ROOT, f'coding-{n}.json')))['items']:
        if it['widget']['kind'] != 'code':
            ITEMS[it['id']] = it
fails = []
seen = set()
checks = 0


def block(iid, lang='python', which=0):
    return re.findall(r'```' + lang + r'\n(.*?)```', ITEMS[iid]['prose'], flags=re.S)[which]


def run(iid, extra=''):
    ns = {}
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        exec(block(iid) + '\n' + extra, ns)
    return ns, out.getvalue().strip()


def ok(iid, cond, what):
    global checks
    checks += 1
    seen.add(iid)
    if not cond:
        fails.append(f'{iid}: {what}')


def key(iid):
    w = ITEMS[iid]['widget']
    if w['kind'] == 'numeric':
        return w['answer']
    return [o['text'] for o in w['options'] if o.get('correct')][0]


def wrongs(iid):
    return {x['id']: x['value'] for x in ITEMS[iid]['widget'].get('wrong', [])}


# ---- coding-1
ns, _ = run('pf-types-round-half-even', '')
v = eval(block('pf-types-round-half-even'))
ok('pf-types-round-half-even', v == key('pf-types-round-half-even') == 4 and [round(0.5), round(1.5), round(2.5)] == [0, 2, 2], f'value {v}')
ok('pf-types-round-half-even', wrongs('pf-types-round-half-even') == {'half-up': 1 + 2 + 3, 'half-down': 0 + 1 + 2}, 'wrong values')
ns, _ = run('pf-functions-default-list')
ok('pf-functions-default-list', ns['total'] == key('pf-functions-default-list') == 6, f"total {ns['total']}")
ok('pf-functions-default-list', wrongs('pf-functions-default-list') == {'fresh-list': 3, 'three-each': 9}, 'wrong values')
# complexity: count the inner steps at n = 1,024 and at 2,048
def steps(n):
    c = 0
    for i in range(n):
        j = 1
        while j < n:
            j *= 2
            c += 1
    return c
ok('complexity-read-doubling-inner', steps(1024) == 10240 and steps(2048) == 2048 * 11 and key('complexity-read-doubling-inner') == '$O(n \\log n)$', f'steps {steps(1024)}')
ok('complexity-read-doubling-inner', block('complexity-read-doubling-inner').strip() == 'for i in range(n):\n    j = 1\n    while j < n:\n        j *= 2', 'the block is the loop counted here')
ns, _ = run('at-complexity-tripling-loop')
ok('at-complexity-tripling-loop', ns['count'] == key('at-complexity-tripling-loop') == 7 and ns['i'] == 2187, f"count {ns['count']}")
ok('at-complexity-tripling-loop', wrongs('at-complexity-tripling-loop') == {'stopped-early': 6, 'divided': 1000 // 3}, 'wrong values')
ns, _ = run('pf-types-backward-slice')
ok('pf-types-backward-slice', ns['total'] == key('pf-types-backward-slice') == 15 and ns['xs'][7:2:-2] == [7, 5, 3], f"total {ns['total']}")
ok('pf-types-backward-slice', wrongs('pf-types-backward-slice') == {'step-one': sum(ns['xs'][7:2:-1]), 'ends-swapped': 6 + 4 + 2}, 'wrong values')
ns = {}
exec(block('integer-division-toward-zero', 'python'), ns)
ok('integer-division-toward-zero', (ns['q'], ns['r']) == (-4, 1) and key('integer-division-toward-zero') == 'C++: -3 and -1. Python: -4 and 1.', 'Python half')

# ---- coding-2
ns, _ = run('pf-collections-first-of-ties')
ok('pf-collections-first-of-ties', ns['best'] == 'to' and key('pf-collections-first-of-ties') == '`"to"`' and ns['d'] == {'to': 2, 'be': 2, 'or': 1, 'not': 1}, f"best {ns['best']}")
ns, _ = run('pf-functions-late-binding')
ok('pf-functions-late-binding', ns['total'] == key('pf-functions-late-binding') == 36, f"total {ns['total']}")
ok('pf-functions-late-binding', wrongs('pf-functions-late-binding') == {'bound-early': 10 + 11 + 12, 'ignored-i': 30}, 'wrong values')
calls = {'n': 0, 'leaf': 0}
src = block('at-recursion-count-the-calls')
ns = {}
exec(src, ns)
orig = ns['f']
def counted(n):
    calls['n'] += 1
    if n <= 1:
        calls['leaf'] += 1
    return orig(n)
ns['f'] = counted
val = counted(12)
ok('at-recursion-count-the-calls', calls['n'] == key('at-recursion-count-the-calls') == 13 and calls['leaf'] == 7 and val == 7, f'calls {calls}')
ok('at-recursion-count-the-calls', wrongs('at-recursion-count-the-calls') == {'gave-value': val, 'no-first': 12}, 'wrong values')
# list membership: count the comparisons for 20,000 different ids
ok('ds-hashing-list-membership', sum(range(20000)) == 199990000 and '199{,}990{,}000' in ITEMS['ds-hashing-list-membership']['explain']['text'], 'comparison count')
ids = list(range(300)) + [5, 7]
ns = {'ids': ids}
exec(block('ds-hashing-list-membership'), ns)
seen_set, rep = set(), 0
for x in ids:
    if x in seen_set:
        rep += 1
    else:
        seen_set.add(x)
ok('ds-hashing-list-membership', ns['repeats'] == rep == 2 and key('ds-hashing-list-membership').startswith('Make `seen` a set'), 'set version gives the same count')
_, out = run('pf-idioms-spent-generator')
ok('pf-idioms-spent-generator', out == '14 0' and key('pf-idioms-spent-generator') == '`14 0`', f'printed {out}')
ns = {}
exec(block('copy-vs-move-vector-copy', 'python'), ns)
ok('copy-vs-move-vector-copy', (len(ns['v']), len(ns['w'])) == (4, 4) and key('copy-vs-move-vector-copy') == 'C++: 3 and 4. Python: 4 and 4.', 'Python half')

# ---- coding-3
_, out = run('pf-idioms-stable-ties')
ok('pf-idioms-stable-ties', out == "['c', 'b', 'a']" == key('pf-idioms-stable-ties'), f'printed {out}')
# stuck loop: trace with a step cap, and the two claims in the distractors' lines
def find_trace(xs, x, test, lo_step, cap=50):
    lo, hi = 0, len(xs)
    tr = []
    while test(lo, hi) and len(tr) < cap:
        mid = (lo + hi) // 2
        tr.append((lo, hi, mid))
        if xs[mid] < x:
            lo = lo_step(mid)
        else:
            hi = mid
    return tr, lo, hi
tr, lo, hi = find_trace([1, 3, 5, 7], 6, lambda a, b: a < b, lambda m: m)
ok('at-search-stuck-loop', len(tr) == 50 and tr[:3] == [(0, 4, 2), (2, 4, 3), (2, 3, 2)] and (lo, hi) == (2, 3) and key('at-search-stuck-loop').startswith('It never ends'), f'trace {tr[:4]}')
tr2, lo2, _ = find_trace([1, 3, 5, 7], 6, lambda a, b: a <= b, lambda m: m)
ok('at-search-stuck-loop', len(tr2) == 50 and lo2 == 2, 'with lo <= hi the loop still sticks at lo 2')
tr3, lo3, hi3 = find_trace([1, 3, 5, 7], 6, lambda a, b: a < b, lambda m: m + 1)
ok('at-search-stuck-loop', len(tr3) < 50 and lo3 == hi3 == 3, 'lo = mid + 1 ends, at index 3')
ok('at-search-stuck-loop', 'def find(xs, x):' in block('at-search-stuck-loop') and 'lo = mid\n' in block('at-search-stuck-loop'), 'block is the loop traced')
_, out = run('ds-stacks-push-pop-trace')
ok('ds-stacks-push-pop-trace', out == '14' and key('ds-stacks-push-pop-trace') == 14, f'printed {out}')
ok('ds-stacks-push-pop-trace', wrongs('ds-stacks-push-pop-trace') == {'from-front': 3 + 5 + 2, 'every-value': 3 + 5 + 2 + 7, 'two-pops': 5 + 7}, 'wrong values')
_, out = run('gd-dp-table-size')
ok('gd-dp-table-size', out == '70' and key('gd-dp-table-size') == 70, f'printed {out}')
ok('gd-dp-table-size', wrongs('gd-dp-table-size') == {'no-empty-prefix': 6 * 9, 'added-lengths': 15, 'added-padded': 17}, 'wrong values')
try:
    _, out = run('np-broadcast-column-plus-row')
    ok('np-broadcast-column-plus-row', out == '324' and key('np-broadcast-column-plus-row') == 324, f'printed {out}')
except ModuleNotFoundError:
    a, b = [1, 2, 3], [10, 20, 30, 40]
    ok('np-broadcast-column-plus-row', sum(x + y for x in a for y in b) == 324 == key('np-broadcast-column-plus-row'), 'no numpy here: outer sum')
    print('note: numpy not installed for this interpreter; the outer sum was used in its place')
ok('np-broadcast-column-plus-row', wrongs('np-broadcast-column-plus-row') == {'added-sums': 6 + 100, 'swapped-counts': 3 * 6 + 4 * 100, 'paired-by-position': 11 + 22 + 33}, 'wrong values')

# ---- coding-4
_, out = run('pf-classes-shared-class-list')
ok('pf-classes-shared-class-list', out == '2' and key('pf-classes-shared-class-list') == 2, f'printed {out}')
ok('pf-classes-shared-class-list', wrongs('pf-classes-shared-class-list') == {'own-list': 1, 'copied-list': 0}, 'wrong values')
ns, out = run('ds-trees-heap-trace')
ok('ds-trees-heap-trace', out == '6' and key('ds-trees-heap-trace') == 6 and (ns['a'], ns['b'], ns['h'][0]) == (1, 2, 3), f'printed {out}')
ok('ds-trees-heap-trace', wrongs('ds-trees-heap-trace') == {'pushed-value': 1 + 4 + 2, 'old-top': 1 + 2 + 2}, 'wrong values')
_, out = run('bit-lowest-and-count')
ok('bit-lowest-and-count', out == '7' and key('bit-lowest-and-count') == 7 and bin(44) == '0b101100', f'printed {out}')
ok('bit-lowest-and-count', wrongs('bit-lowest-and-count') == {'bit-index': 2 + 3, 'highest-bit': 32 + 3}, 'wrong values')
ns = {}
exec(block('edge-case-list-median-test'), ns)
import statistics
res = {}
for opt in ITEMS['edge-case-list-median-test']['widget']['options']:
    xs = eval(opt['text'].strip('`'))
    try:
        got = ns['median'](xs)
        res[opt['text']] = 'wrong' if got != statistics.median(xs) else 'right'
    except IndexError:
        res[opt['text']] = 'raises'
ok('edge-case-list-median-test', res == {'`[4, 1, 3, 2]`': 'wrong', '`[]`': 'raises', '`[5]`': 'right', '`[3, 1, 2]`': 'right'} and key('edge-case-list-median-test') == '`[4, 1, 3, 2]`', f'{res}')
ok('edge-case-list-median-test', ns['median']([4, 1, 3, 2]) == 3 and statistics.median([4, 1, 3, 2]) == 2.5, 'returns 3, median 2.5')
ns, _ = run('gd-traversal-depth-first-order')
ok('gd-traversal-depth-first-order', ', '.join(ns['seen']) == key('gd-traversal-depth-first-order') == 'A, B, D, F, C, E', f"seen {ns['seen']}")

# ---- C++ reading items
CPP = r'''
#include <climits>
#include <vector>
#include <cstdio>
struct B { char name() const { return 'B'; } };
struct D : B { char name() const { return 'D'; } };
struct VB { virtual char name() const { return 'B'; } virtual ~VB() = default; };
struct VD : VB { char name() const override { return 'D'; } };
static_assert(-7 / 2 == -3 && -7 % 2 == -1, "integer-division-toward-zero");
static_assert(0u - 1 == 4294967295u && sizeof(unsigned) == 4, "defined-vs-undefined-wraparound x");
int main() {
    std::vector<int> v{1, 2, 3};
    auto w = v;
    w.push_back(4);
    D d; const B& r = d; char c = r.name();
    VD vd; const VB& vr = vd;
    unsigned u = 0; auto x = u - 1;
    std::printf("%zu %zu %c %c %u\n", v.size(), w.size(), c, vr.name(), x);
}
'''
UB = '#include <climits>\nconstexpr int y = INT_MAX + 1;\nint main() { return y; }\n'
gxx = shutil.which('g++') or shutil.which('clang++')
cpp_ids = ['integer-division-toward-zero', 'copy-vs-move-vector-copy', 'virtual-dispatch-missing-virtual', 'defined-vs-undefined-wraparound']
if gxx:
    d = tempfile.mkdtemp()
    open(os.path.join(d, 'a.cpp'), 'w').write(CPP)
    open(os.path.join(d, 'ub.cpp'), 'w').write(UB)
    r = subprocess.run([gxx, '-std=c++20', '-o', os.path.join(d, 'a'), os.path.join(d, 'a.cpp')], capture_output=True, text=True)
    out = subprocess.run([os.path.join(d, 'a')], capture_output=True, text=True).stdout.strip() if r.returncode == 0 else r.stderr[:300]
    for i in cpp_ids:
        ok(i, out == '3 4 B D 4294967295', f'C++ run printed {out!r}')
    r2 = subprocess.run([gxx, '-std=c++20', '-fsyntax-only', os.path.join(d, 'ub.cpp')], capture_output=True, text=True)
    ok('defined-vs-undefined-wraparound', r2.returncode != 0 and 'overflow' in r2.stderr, 'INT_MAX + 1 is rejected in a constant expression')
    ok('virtual-dispatch-missing-virtual', key('virtual-dispatch-missing-virtual') == "The character 'B'", 'key')
    ok('defined-vs-undefined-wraparound', key('defined-vs-undefined-wraparound') == 'Only x, which is 4,294,967,295', 'key')
else:
    print('WARNING: no C++ compiler found; the four C++ halves were not run')
    for i in cpp_ids:
        seen.add(i)

missing = [i for i in ITEMS if i not in seen]
if missing:
    fails.append('not run: ' + ', '.join(missing))
print(f'{len(ITEMS)} reasoning and reading items, {checks} checks, {len(fails)} failed')
for f in fails:
    print('FAIL', f)
sys.exit(1 if fails else 0)
