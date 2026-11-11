"""How deep can a remembered recursion go on the drill page before Python stops?
Rewrites two drills in a COPY of app/: the tests become one input per depth, in
rising order, and the model solution becomes the lru_cache recursion. The page
skips every test after the first error, so "the model solution passes X of Y"
from planted-check on the copy gives the first depth that fails.

usage: depth_probe.py <copy of app>
then:  ZQ_APP_DIR=<copy> node tools/planted-check.mjs --drill ci-merged-tape --drill ci-mirror-pieces --local-cdn <pkgs>
Depths: merged tape 2k frames for k = 100, 125, ..., 300 (tests 0 to 8);
mirror pieces n frames (each with a generator frame inside) for n = 100, 150, ..., 400 (tests 0 to 6)."""
import json
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
app = os.path.abspath(sys.argv[1])
assert app != os.path.abspath(os.path.join(here, '..', '..', '..', 'app')), 'use a copy'
c = {}
for name in ('wrong2.py',):
    e = {}
    exec(open(os.path.join(here, name)).read(), e)
    c.update(e['CANDIDATES'])


def rewrite(did, label, calls):
    f = os.path.join(app, 'content', 'drills', did + '.json')
    d = json.load(open(f))
    env = {}
    exec(d['solution'], env)
    d['tests'] = [{'call': call, 'expect': repr(eval(call, env)), 'compare': 'equal'} for call in calls]
    d['solution'] = c[label][1].strip() + '\n'
    d['planted'] = [{'code': d['starter'], 'slip': 'starter'}]
    json.dump(d, open(f, 'w'), indent=2)
    print(did, len(d['tests']), 'tests')


rewrite('ci-merged-tape', 'merge_memo_recursion',
        ["merge_ways('a' * %d, 'a' * %d, 'a' * %d)" % (k, k, 2 * k) for k in range(100, 301, 25)])
rewrite('ci-mirror-pieces', 'pieces_memo_recursion',
        ["solve_mirror_pieces('1\\n' + 'abc' * %d + 'a')" % (n // 3) for n in range(100, 401, 50)])
