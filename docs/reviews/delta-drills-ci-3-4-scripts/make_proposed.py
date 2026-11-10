"""Compute the expect of every test proposed in the delta review, by the model and by mine.py, and write proposed_tests.json.
From the repo root: <venv python> docs/reviews/delta-drills-ci-3-4-scripts/make_proposed.py"""
import json, os, importlib.util
S = os.path.dirname(os.path.abspath(__file__)) + '/'
spec = importlib.util.spec_from_file_location('mine', S + 'mine.py'); mine = importlib.util.module_from_spec(spec); spec.loader.exec_module(mine)
P = {
 'ci-ring-lookup': [
  "find_in_ring([1000000000, -1000000000], [-1000000000, 1000000000, -999999999, 0])",
  "(lambda r: (len(r), sum(r), r.count(-1)))(find_in_ring([10000 * ((i + 61729) % 100000) for i in range(100000)], [(i * 104729) % 1000000000 for i in range(100000)]))"],
 'ci-tick-ranges': [
  "solve_tick_ranges('4 4\\n0 0 1000000000000 1000000000000\\n0 1000000000000 999999999999 1\\n')",
  "(lambda r: (r.count('\\n'), sum(map(int, r.split()))))(solve_tick_ranges('100000 100000\\n' + ' '.join(str(10000000 * (i // 2)) for i in range(100000)) + '\\n' + ' '.join(str(i * 7919) for i in range(100000)) + '\\n'))"],
 'ci-live-median': [
  "(lambda out: (len(out), out.count('-'), sum(int(t) for t in out if t != '-'), out[-3:]))(solve_live_median('400000\\n' + '\\n'.join('+ %d' % (i * 7919 % 1000003 + 1) if i < 300000 else '- %d' % ((i - 300000) * 3 * 7919 % 1000003 + 1) for i in range(400000)) + '\\n').split())",
  "(lambda out: (len(out), out.count('-'), sum(int(t) for t in out if t != '-'), out[-3:]))(solve_live_median('200000\\n' + '\\n'.join('- %d' % ((i - 2) * 37 % 1000 + 1) if i % 3 == 2 else '+ %d' % (i * 37 % 1000 + 1) for i in range(200000)) + '\\n').split())"],
 'ci-ready-blocks': [
  "earliest_ready_day([7, 2, 9, 4, 4, 6], 1, 3)",
  "earliest_ready_day([7, 2, 9, 4, 4, 6], 2, 2)",
  "earliest_ready_day([7, 2, 9, 4, 4, 6], 2, 4)"],
 'ci-price-ramp': [
  "widest_ramp([8, 8, 7, 2, 8, 5, 1, 4, 2])",
  "widest_ramp(list(range(199999, 0, -1)) + [100000])"],
 'ci-right-edge-view': [
  "right_edge_view((4, (9, (2, None, (7, None, None)), None), (1, None, None)))"],
 'ci-funded-projects': [
  "funded_projects(1, 2, [[4, 6], [1, 2], [0, 3], [3, 1]])"],
 'ci-relay-masts': [
  "min_longest_gap([0] + [(i * i * 31) % 9973 + 10000 * i for i in range(1, 100000)], 5000000)"],
 'ci-cell-formula': [
  "formula_value('SUM(2,MAX(' * 49999 + '-3' + '))' * 49999)"],
}
out = {}
for did, calls in P.items():
    d = json.load(open('app/content/drills/%s.json' % did)); fn = d['fn']; ns = {}; exec(d['solution'], ns)
    out[did] = []
    for c in calls:
        a = eval(c, {fn: ns[fn]}); b = eval(c, {fn: getattr(mine, fn)})
        assert a == b, (did, a, b)
        out[did].append({'call': c, 'expect': repr(a), 'compare': 'equal'})
        print(did, repr(a))
json.dump(out, open(S + 'proposed_tests.json', 'w'), indent=1)
