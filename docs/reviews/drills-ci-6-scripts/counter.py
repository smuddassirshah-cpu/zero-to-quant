"""For candidates of wrong.py: search small random inputs (the generators of
checks.py) for the shortest input where the candidate and the model disagree.
usage: counter.py <drills dir> <label> [<label> ...]   (no label: every candidate not marked right)"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import checks  # noqa: E402

drills = checks.load(sys.argv[1])
w = {}
exec(open(os.path.join(HERE, 'wrong.py')).read(), w)
labels = sys.argv[2:] or [k for k in w['CANDIDATES'] if '(right)' not in k]
for label in labels:
    did, code, _ = w['CANDIDATES'][label]
    j = drills[did]
    fn = j['fn']
    model, cand = {}, {}
    exec(j['solution'], model)
    exec(code, cand)
    gen = getattr(checks, 'g_' + fn)
    best = None
    n = 0
    for _ in range(20000):
        args = gen(False)
        want = model[fn](*copy.deepcopy(args))
        try:
            got = cand[fn](*copy.deepcopy(args))
        except Exception as e:  # noqa
            got = type(e).__name__
        if got != want:
            n += 1
            if best is None or len(repr(args)) < len(repr(best[0])):
                best = (args, want, got)
    print('%-55s %d of 20000 differ; shortest %r' % (label, n, best))
