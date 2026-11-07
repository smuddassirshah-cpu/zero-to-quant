"""Checks that assert findings of review-perf-retrofit-1. Each FAIL line names a
finding and stays failing until the fix lands; exit 1 while any stands.
It also proves the expectations of the proposed new tests with the shipped solutions."""
import itertools
from harness import item, run, check, finish

def pass_without(rubric, core):
    """Tick sets that pass (>= 7, every required row ticked) with row `core` (0-based) unticked."""
    n = len(rubric)
    out = []
    for ticks in itertools.product((0, 1), repeat=n):
        if ticks[core]:
            continue
        if any(r.get('required') and not t for r, t in zip(rubric, ticks)):
            continue
        if sum(r['points'] for r, t in zip(rubric, ticks) if t) >= 7:
            out.append([k + 1 for k in range(n) if ticks[k]])
    return out

# BZ1-1: the piece must be pinned to an L (an in-line extra square makes an I piece).
_, bz1 = item('brainteasers', 'homework-1', 'hw9-l-pieces-6x10')
check('right angles' in bz1['widget']['prompt'], 'BZ1-1 prompt says the extra square is at right angles to the line')
# BZ1-2: a pass needs the proof of the 3 and 1 split (row 3).
p = pass_without(bz1['widget']['rubric'], 2)
check(not p, f'BZ1-2 no pass without row 3 (passing tick sets without it: {p})')

# RI2-1: each of the three named parts is needed for a pass.
_, ri2 = item('research-int', 'homework-2', 'h2-pca-aloud')
for core in (0, 1, 2):
    p = pass_without(ri2['widget']['rubric'], core)
    check(not p, f'RI2-1 no pass without row {core + 1} (passing tick sets: {p})')
check('standardised' in ri2['widget']['model'], 'RI2-2 model says the baskets are of standardised returns')

# CI4-1 and CI4-2.
_, ci4 = item('coding-int', 'homework-4', 'h4-pairs-aloud')
r3 = ci4['widget']['rubric'][2]['text']
check('$O(1)$ extra memory' not in r3, 'CI4-1 required row no longer gives an in-place sort O(1) extra memory')
rows_code = [k for k, r in enumerate(ci4['widget']['rubric']) if 'gives 5' in r['text'] or 'correct' in r['text']]
check(bool(rows_code) and all(not pass_without(ci4['widget']['rubric'], k) for k in rows_code),
      f'CI4-2 a row grades the typed code and no pass skips it (rows {rows_code})')

# CI3-1 and CI3-2: slips must be caught before the timing test.
_, ci3 = item('coding-int', 'homework-3', 'h3-notes-drive')
w = ci3['widget']
S = w['solution']
size_file = S.replace("        return 0 if chain is None else chain[-1].total",
                      "        return 0 if chain is None or chain[-1].text is not None else chain[-1].total")
mk = S.replace("    def mkdir(self, path):\n        self._make(self._names(path))",
               "    def mkdir(self, path):\n        names = self._names(path)\n        if names:\n            chain = self._make(names[:-1])\n            chain[-1].children[names[-1]] = _Node()")
last = len(w['tests'])
for tag, code in (('CI3-1 size of a file returns 0', size_file), ('CI3-2 mkdir replaces an existing folder', mk)):
    bad = [k + 1 for k, r in enumerate(run(code, w, w['tests'])) if not r[0]]
    check(bool(bad) and bad[0] < last, f'{tag}: first caught by a test before the timing test (fails {bad})')

# RI4-1: the same for research-int.
_, ri4 = item('research-int', 'homework-4', 'h4-quote-at')
w4 = ri4['widget']
S4 = w4['solution']
dedupe = S4.replace("    return out\n", "    return list(dict(zip(times, out)).values())\n")
firstlast = S4.replace(
    "        sums[t] = sums.get(t, 0.0) + p\n        counts[t] = counts.get(t, 0) + 1\n",
    "        if t in sums:\n            sums[t] = (first[t] + p)\n            counts[t] = 2\n        else:\n            first[t] = p\n            sums[t], counts[t] = p, 1\n").replace(
    "    sums, counts = {}, {}", "    sums, counts, first = {}, {}, {}")
last4 = len(w4['tests'])
for tag, code in (('RI4-1 repeated asked seconds answered once', dedupe), ('RI4-1 mean of first and last repeat only', firstlast)):
    bad = [k + 1 for k, r in enumerate(run(code, w4, w4['tests'])) if not r[0]]
    check(bool(bad) and bad[0] < last4, f'{tag}: first caught by a test before the timing test (fails {bad})')

# Proposed new expectations, run on the shipped solutions (these must hold now).
ns = {}
exec(S4, ns)
got = ns['quote_at']([(0, 100.0), (0, 101.0), (0, 105.0), (10, 110.0)], [5, 0, 5], 60)
print('proposed RI4 test:', got)
ns = {}
exec(S, ns)
exec(w['postlude'], ns)
print('proposed CI3 test 3:', ns['run_drive']([('write', '/r/a', 'abcdef'), ('write', '/r/a', 'xy'), ('size', '/r/a'), ('size', '/r'), ('size', '/'), ('write', '/r/a', ''), ('size', '/r'), ('read', '/r/a')]))
print('proposed CI3 test 5:', ns['run_drive']([('ls', '/nope'), ('read', '/nope'), ('size', '/nope'), ('mkdir', '/m'), ('read', '/m'), ('size', '/m'), ('ls', '/'), ('mv', '/nope', '/x'), ('ls', '/'), ('write', '/m/k', 'abc'), ('mkdir', '/m'), ('ls', '/m'), ('size', '/m')]))
for tag, code in (('size of a file', size_file), ('mkdir replaces', mk)):
    n2 = {}
    exec(code, n2); exec(w['postlude'], n2)
    a = n2['run_drive']([('write', '/r/a', 'abcdef'), ('write', '/r/a', 'xy'), ('size', '/r/a'), ('size', '/r'), ('size', '/'), ('write', '/r/a', ''), ('size', '/r'), ('read', '/r/a')])
    b = n2['run_drive']([('ls', '/nope'), ('read', '/nope'), ('size', '/nope'), ('mkdir', '/m'), ('read', '/m'), ('size', '/m'), ('ls', '/'), ('mv', '/nope', '/x'), ('ls', '/'), ('write', '/m/k', 'abc'), ('mkdir', '/m'), ('ls', '/m'), ('size', '/m')])
    print(f'  slip "{tag}" on proposed tests 3 and 5:', a, b)
for tag, code in (('dedupe', dedupe), ('first-last', firstlast)):
    n3 = {}
    exec(code, n3)
    print(f'  slip "{tag}" on proposed RI4 test:', n3['quote_at']([(0, 100.0), (0, 101.0), (0, 105.0), (10, 110.0)], [5, 0, 5], 60))
finish()
