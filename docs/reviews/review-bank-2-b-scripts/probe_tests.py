"""Probes for proposed extra hidden tests: each proposed call must pass my solution and the model, and fail the candidate
that slipped through. Run after code_harness.py. Prints one line per proposal; exit 1 if a proposal does not do its job."""
import importlib, json, os, sys
import code_harness as H

ROOT = H.ROOT
PROPOSED = {
    # item id: [(candidate name that passes today, proposed test dict)]
    'ds-arrays-sign-changes': [('zero-as-a-loss', {'call': 'sign_changes([1, 0, 2, 0, -3])', 'expect': '1'}),
                               ('zero-as-a-loss', {'call': 'sign_changes([0, 5, -1])', 'expect': '1'})],
    'edge-case-list-to-pence': [('returns-float', {'call': 'type(to_pence("£0.29")).__name__', 'expect': "'int'"})],
    'ds-pointers-merge-ticks': [('pop-front-in-place', {'setup': 'a = [(1, 1.0), (3, 1.0)]; b = [(2, 2.0)]', 'call': '(merge_ticks(a, b), a, b)', 'expect': '([(1, 1.0), (2, 2.0), (3, 1.0)], [(1, 1.0), (3, 1.0)], [(2, 2.0)])'}),
                                ('extends-a-in-place', {'setup': 'a = [(1, 1.0), (3, 1.0)]; b = [(2, 2.0)]', 'call': '(merge_ticks(a, b), a, b)', 'expect': '([(1, 1.0), (2, 2.0), (3, 1.0)], [(1, 1.0), (3, 1.0)], [(2, 2.0)])'})],
    'gd-dp-walk-above-zero': [('float-ballot', {'call': 'nonneg_walk_counts(60)[2]', 'expect': '10729649537134605'})],
    'pf-idioms-trend-direction': [('first-and-last-pairs', {'call': 'trend([1, 5, 3, 4, 6])', 'expect': '0'}),
                                  ('first-pair-sets-direction', {'call': 'trend([1, 2, 2, 3])', 'expect': '0'})],
    'at-search-count-in-range': [('bisect-then-walk', {'setup': 'xs = list(range(0, 2000000, 2))', 'call': 'sum(count_in_range(xs, k, 10**7) for k in range(0, 600, 2))', 'expect': '299955150', 'budget': 0})],
    'pf-idioms-count-above-mean': [('truncated-mean', {'call': 'above_mean([-1, -2])', 'expect': '1'}),
                                   ('truncated-mean', {'call': 'above_mean([-4, -1, -1, -1])', 'expect': '3'})],
    'ds-arrays-local-peaks': [('wraps-at-index-zero', {'call': 'local_peaks([5, 1, 2])', 'expect': '[]'}),
                              ('wraps-at-index-zero', {'call': 'local_peaks([9, 1, 9, 3])', 'expect': '[2]'})],
    'at-search-smallest-n': [('float-mid', {'call': 'rows_needed(999999912498231751)', 'expect': '1414213501'})],
    'at-greedy-orders-to-fill': [('remove-max-in-place', {'setup': 'sizes = [1] * 30000', 'call': 'orders_to_fill(sizes, 30000)', 'expect': '30000'})],
}


def main():
    bad = 0
    for n in (1, 2, 3, 4):
        items = {it['id']: it for it in json.load(open(os.path.join(ROOT, f'coding-{n}.json')))['items'] if it['widget']['kind'] == 'code'}
        try:
            cands = importlib.import_module(f'cands_{n}').CANDS
        except ModuleNotFoundError:
            continue
        for iid, props in PROPOSED.items():
            if iid not in items:
                continue
            w = items[iid]['widget']
            by = {nm: src for nm, _, src in cands[iid]['wrong']}
            for nm, case in props:
                m = H.run(w['solution'], [case])[0]
                mine = H.run(cands[iid]['mine'], [case])[0]
                c = H.run(by[nm], [case])[0] if nm in by else (None, 0, 'no such candidate')
                ok = m[0] and mine[0] and c[0] is False
                bad += not ok
                print(f'{"ok  " if ok else "BAD "} {iid}: {case["call"][:70]} => {case["expect"][:50]} | model {m[0]} ({m[1]:.2f} s), mine {mine[0]}, {nm} {c[0]} ({c[2][:40]}, {c[1]:.2f} s)')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
