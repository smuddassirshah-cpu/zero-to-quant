"""Expected values for the smaller large tests proposed for ci-k-bit-count (finding on the digit
recursion), and the check of the replacement first example proposed for ci-room-numbers.
usage: resize.py <drills dir>"""
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import checks  # noqa: E402

D = checks.load(sys.argv[1])
j = D['ci-k-bit-count']
e = {}
exec(j['solution'], e)
c11 = j['tests'][11]['call'].replace('range(2000)', 'range(400)')
c12 = j['tests'][12]['call'].replace('* 1000', '* 300')
assert c11 != j['tests'][11]['call'] and c12 != j['tests'][12]['call']
print('tests[11] with range(400):', eval(c11, e))
print('tests[12] with * 300:', eval(c12, e))
m = {}
exec(open(os.path.join(HERE, 'right.py')).read(), m)
r = {}
exec(m['CANDIDATES']['R_kbits_digit_dp'][1], r)
t = time.time()
assert eval(c11, r) == eval(c11, e) and eval(c12, r) == eval(c12, e)
print('digit recursion on both, natively: %.2f s' % (time.time() - t))
t = time.time()
eval(j['tests'][11]['call'], r)
eval(j['tests'][12]['call'], r)
print('digit recursion on today\'s tests[11] and [12], natively: %.2f s' % (time.time() - t))

j = D['ci-room-numbers']
e = {}
exec(j['solution'], e)
ex = ([[0, 28], [4, 9], [11, 40], [33, 50]], 2)
print('room example', ex, '->', e['room_numbers'](*ex), checks.b_room_numbers(*ex))
