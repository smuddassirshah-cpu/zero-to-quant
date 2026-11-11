"""Small facts quoted in the review.
usage: misc_checks.py <drills dir>
1. ci-trace-count: the slow plant's time on the two large tests that expect 0, and
   the value of the replacement proposed in finding 12 (model and mine.py).
2. ci-hold-limit: the two calls recalled as published samples.
3. Stated numbers in notes, how and slips recomputed."""
import json
import math
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
D = sys.argv[1]
mine = {}
exec(open(os.path.join(HERE, 'mine.py')).read(), mine)


def drill(did):
    return json.load(open(os.path.join(D, did + '.json')))


j = drill('ci-trace-count')
env = {}
exec(j['solution'], env)
call = "trace_count([''.join('abc'[(i + 2 * j) % 3] for j in range(19)) for i in range(20)], 'abcab' * 12)"
print('proposed trace test:', eval(call, env), eval(call, {'trace_count': mine['trace_count']}))
slow = {}
exec(j['planted'][3]['code'], slow)
for i in (11, 12):
    t = time.time()
    r = eval(j['tests'][i]['call'], slow)
    print('trace tests[%d]: slow plant returns %r in %.3f s' % (i, r, time.time() - t))

h = drill('ci-hold-limit')
print('hold-limit examples[1]:', h['examples'][1]['call'], '=>', h['examples'][1]['expect'])
print('hold-limit tests[8]:', h['tests'][8]['call'], '=>', h['tests'][8]['expect'])

print('C(40, 20) =', math.comb(40, 20))
print('11! =', math.factorial(11), ' 11! - 2 * 10! =', math.factorial(11) - 2 * math.factorial(10))
print('digits of C(600, 300):', len(str(math.comb(600, 300))))
print('light-cargo table cells at most:', 80 * 30 + 1)
m = drill('ci-merged-tape')
p = {}
exec(m['planted'][1]['code'], p)
print('merged-tape planted[1] (no length check): tape too short', p['merge_ways']('ab', 'cd', 'acb'),
      '(right, 0); tape too long', p['merge_ways']('ab', 'c', 'acbb'), '(wrong, should be 0)')
