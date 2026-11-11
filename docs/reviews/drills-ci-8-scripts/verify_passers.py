"""For candidates that pass every hidden test: are they really wrong?
Compares each against the model on random inputs inside the constraints and
prints the smallest disagreeing input found (a test that would catch it).
usage: verify_passers.py <drills dir> <candidates file> label [label ...]"""
import copy
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checks  # noqa: E402

drills = checks.load(sys.argv[1])
env0 = {}
exec(open(sys.argv[2]).read(), env0)
C = env0['CANDIDATES']
for label in sys.argv[3:]:
    did, code, comment = C[label]
    j = drills[did]
    fn = j['fn']
    m, c = {}, {}
    exec(j['solution'], m)
    exec(code, c)
    rng = random.Random(11)
    best = None
    n_bad = 0
    N = 6000
    for it in range(N):
        args = checks.gens(rng, it % 3 == 2)[fn]()
        want = m[fn](*copy.deepcopy(args))
        try:
            got = c[fn](*copy.deepcopy(args))
        except Exception as e:  # noqa
            got = 'EXC %s' % type(e).__name__
        if got != want:
            n_bad += 1
            if best is None or len(repr(args)) < len(repr(best[0])):
                best = (args, want, got)
    print('%-40s %-20s wrong on %d of %d' % (label, did, n_bad, N))
    if best:
        print('     smallest:', repr(best[0])[:260], 'want', repr(best[1])[:90], 'got', repr(best[2])[:90])
