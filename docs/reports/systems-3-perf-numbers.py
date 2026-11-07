"""systems level 3 performance task h3-process-aloud: every number in the
prompt, model, rubric and explain, computed twice.

Route A: per order, then times the order rate.
Route B: per second, event by event: count the calls, switches and
scheduler runs in one busy second and add their costs, from a small
event simulation of the pipe (write, wake, read, sleep) for 20,000 orders.
"""
import json, os, re, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'systems', 'homework-3.json')
item = next(i for i in json.load(open(HW))['items'] if i['id'] == 'h3-process-aloud')
W = item['widget']
text = W['prompt'] + W['model'] + json.dumps(W['rubric'], ensure_ascii=False) + item['explain']['text'] + json.dumps(W['followUps'])
text = text.replace('{,}', ',')
fails = []
def check(c, m):
    if not c:
        fails.append(m); print('FAIL', m)

call, switch, sched, rate = F(2, 10), F(2), F(1), 20_000

# ---- route A: per order ------------------------------------------------
calls = 2 * call
wake = switch + sched + switch
per = calls + wake
check(calls == F(4, 10), 'two calls 0.4 us')
check(wake == 5, 'wake 5 us')
check(per == F(54, 10), '5.4 us an order')
total_us = rate * per
check(total_us == 108_000, '108,000 us a second')
check(total_us / 1000 == 108, '108 ms')
check(round(float(total_us / 10**6) * 100) == 11, 'about 11% of a core')
check(round(float(rate * wake / total_us) * 100) == 93, 'wake is about 93%')
check(rate * wake / 1000 == 100, 'wake 100 ms of the 108')

# ---- route B: event count in one second ---------------------------------
events = {'syscall': 0, 'switch': 0, 'sched': 0}
sender_asleep = True
for _ in range(rate):
    events['syscall'] += 1            # strategy write
    if sender_asleep:
        events['sched'] += 1          # scheduler picks the woken sender
        events['switch'] += 1         # switch the sender in
        sender_asleep = False
    events['syscall'] += 1            # sender read returns the order
    # sender calls read again, finds the pipe empty and sleeps:
    events['switch'] += 1
    sender_asleep = True
# the read that blocks is the same call that later returns; count it once
us = events['syscall'] * F(2, 10) + events['switch'] * 2 + events['sched'] * 1
print('events in one second:', events, 'cost us:', float(us))
check(events == {'syscall': 40_000, 'switch': 40_000, 'sched': 20_000}, 'event counts')
check(us == 108_000, 'route B 108,000 us')
check(float(us) / 1e6 == 0.108, 'route B 10.8% of a core')

# ---- every figure in the text is accounted for -------------------------
for fig in ['20,000', '0.2 µs', '2 µs', '1 µs', '0.4', '5 µs', '5.4 µs', '108,000', '108 ms', '11%', '93', '100%']:
    check(fig in text, 'figure present: ' + fig)
nums = set(x.rstrip(',.') for x in re.findall(r'\d[\d,]*(?:\.\d+)?', text.replace('{,}', ',')))
# fix pass SY3-1: an order's own wait is the scheduler plus the switch back in, plus the two calls
check(F(1) + 2 == 3 and F(1) + 2 + F(4, 10) * 1 == F(34, 10), 'wait on the order path 3 us, 3.4 us with the calls')
known = {'3.4', '20,000', '0.2', '2', '1', '0.4', '5', '5.4', '108,000', '108', '11', '100', '93', '3'}
check(nums <= known, 'no unchecked figure: %s' % sorted(nums - known))
check(sum(r['points'] for r in W['rubric']) == 10, 'rubric sums to 10')
check(0 < sum(1 for r in W['rubric'] if r.get('required')) < len(W['rubric']), 'some rows required, not all')
check(15 <= W['seconds'] <= 1800 and 1 <= len(W['followUps']) <= 5, 'aloud shape')
print('FAILURES:', len(fails))
sys.exit(1 if fails else 0)
