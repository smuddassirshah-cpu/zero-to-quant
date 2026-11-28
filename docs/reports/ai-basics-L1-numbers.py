"""Number check for ai-basics level 1 (l1 to l4, review-1, homework-1, problems-1).
Every count is found twice: method A counts agreements between a threshold rule and the labels, method B counts the
mistakes (false alarms plus misses) and subtracts from the total. Shares are checked as exact fractions. Every code
widget's hidden tests are checked twice: the expected value is recomputed by method B, and the widget's own solution
is run in CPython and must reproduce it, while the starter must fail at least one test.
Run: python3 docs/reports/ai-basics-L1-numbers.py   (exits 0 when every check passes)
"""
import os
import re
import sys
from fractions import Fraction as F

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("ai-basics", 1)


def right_a(t, xs, ys, strict=False):
    return sum(((x > t) if strict else (x >= t)) == bool(y) for x, y in zip(xs, ys))


def right_b(t, xs, ys, strict=False):
    false_alarm = sum(1 for x, y in zip(xs, ys) if ((x > t) if strict else (x >= t)) and y == 0)
    missed = sum(1 for x, y in zip(xs, ys) if not ((x > t) if strict else (x >= t)) and y == 1)
    return len(xs) - false_alarm - missed


def two(label, a, b):
    lv.claim(a == b, f'{label}: method A {a} = method B {b}')
    return a


def right(t, xs, ys, strict=False, label=''):
    return two(f'{label} t={t}', right_a(t, xs, ys, strict), right_b(t, xs, ys, strict))


def scr(f, title):
    doc = lv.files[[k for k in lv.files if k.startswith(f)][0]]
    for i, s in enumerate(doc['screens']):
        if s.get('title') == title:
            return f'screens[{i}]'
    raise KeyError(title)


def item(f, iid):
    doc = lv.files[[k for k in lv.files if k.startswith(f)][0]]
    for i, s in enumerate(doc['items']):
        if s.get('id') == iid:
            return f'items[{i}]'
    raise KeyError(iid)


def quiz(f, qid):
    doc = lv.files[[k for k in lv.files if k.startswith(f)][0]]
    for i, s in enumerate(doc['quiz']):
        if s.get('id') == qid:
            return f'quiz[{i}]'
    raise KeyError(qid)


def run_code(f, path):
    doc = lv.files[[k for k in lv.files if k.startswith(f)][0]]
    node = doc
    for part in path.replace(']', '').replace('[', '.').split('.'):
        node = node[int(part)] if part.isdigit() else node[part]
    w = node['widget']
    ok_all, starter_fails = True, False
    for src, want_pass in ((w['solution'], True), (w['starter'], False)):
        ns = {}
        exec(src, ns)
        for t in w['tests']:
            try:
                got = eval(t['call'], ns)
                exp = eval(t['expect'])
                ok = abs(got - exp) <= 1e-9 * max(1, abs(exp)) if t.get('compare') == 'isclose' else got == exp
            except Exception:
                ok = False
            if want_pass and not ok:
                ok_all = False
            if not want_pass and not ok:
                starter_fails = True
    lv.claim(ok_all, f'{f} {path}: solution passes every hidden test')
    lv.claim(starter_fails, f'{f} {path}: starter fails a hidden test')
    return w


# ---------------- the course data ----------------
TR = [0, 1, 1, 2, 3, 4, 5, 6, 7, 9]; SP = [0, 0, 0, 1, 0, 0, 1, 1, 1, 1]; FR = [0, 0, 1, 1, 0, 0, 0, 1, 0, 1]
TE = [0, 2, 4, 5, 8, 10]; TS = [0, 0, 1, 1, 1, 1]
counts = [right(t, TR, SP, label='course data') for t in range(11)]
lv.claim(counts == [5, 6, 8, 7, 8, 9, 8, 7, 6, 6, 5], f'course counts {counts}')
lv.claim(counts.count(9) == 1 and counts.index(9) == 5, 't = 5 is the unique best, 9 of 10')
for t, c in enumerate(counts):
    lv.expect('l3', scr('l3', 'Learning is choosing') + f'.canvas.state.values.{t}', c)
lv.expect('l3', scr('l3', 'Drag the threshold') + '.widget.answer', max(counts))
lv.expect('l3', scr('l3', 'Drag the threshold') + '.explain.text', 9)
lv.expect('l3', scr('l3', 'Learning is choosing') + '.widget.answer', float(F(9, 10)))
lv.expect('l3', scr('l3', 'Learning is choosing') + '.feedback.correct', 90)
lv.expect('l3', scr('l3', 'Count it by hand: t = 3') + '.widget.answer', counts[3])
lv.expect('l3', scr('l3', 'Count it by hand: t = 3') + '.feedback.correct', 7)
lv.expect('l3', scr('l3', 'Count it by hand: t = 6') + '.widget.answer', counts[6])
lv.expect('l3', scr('l3', 'Count it by hand: t = 6') + '.explain.text', 8)
lv.claim(right(3, TR, SP, strict=True) == 8, 'l3 slip: reading t = 3 as "more than 3" gives 8 (wrong id strict)')
lv.expect('l3', scr('l3', 'Count it by hand: t = 3') + '.widget.wrong[2].value', 8)
# the derived caption on the explore plane counts exactly method A for every t
cap = lv.files['l3-learning-a-rule']['screens'][0]['canvas']['derive']['caption']
expr = cap.split('{{')[-1].split('}}')[0]
terms = re.findall(r'\((\d+)<t\.x\?(\d):(\d)\)', expr)
lv.claim(len(terms) == 10, f'l3 explore caption has one term per email ({len(terms)})')
for t in range(11):
    val = sum(int(b) if int(x) < t else int(c) for x, b, c in terms)
    lv.claim(val == counts[t], f'l3 explore caption formula gives {val} at t = {t}')
# second feature: links >= 5 or says free
orr = sum(((l >= 5) or f == 1) == bool(s) for l, f, s in zip(TR, FR, SP))
orr_b = 10 - sum(1 for l, f, s in zip(TR, FR, SP) if ((l >= 5) or f == 1) != bool(s))
lv.claim(two('or rule', orr, orr_b) == 9, 'links >= 5 or free gets 9')
lv.expect('l3', scr('l3', 'A second feature') + '.widget.answer', 9)
# trap: t = 4 splits 5 and 5, scores 8; mean of links 3.8
lv.claim(sum(1 for x in TR if x < 4) == 5 and sum(1 for x in TR if x >= 4) == 5, 't = 4 puts five emails each side')
lv.claim(F(sum(TR), len(TR)) == F(38, 10), 'mean link count is 3.8')
lv.expect('l3', scr('l3', 'Half and half') + '.widget.options', 3.8)
lv.claim(counts[4] == 8 and counts[10] == 5, 't = 4 scores 8, t = 10 scores 5')
# tie inbox
TL = [0, 1, 2, 3, 4, 5]; TSP = [0, 0, 1, 0, 1, 1]
tc = [right(t, TL, TSP, label='tie inbox') for t in range(7)]
lv.claim(tc == [3, 4, 5, 4, 5, 4, 3], f'tie inbox counts {tc}: 2 and 4 tie at 5, 3 gets 4')
# desk transfer
SG = [0.2, 0.9, 0.4, 1.3, 0.7, 1.1, 0.1, 1.6]; UP = [0, 0, 1, 1, 0, 1, 0, 1]
dc = {c: right(c, SG, UP, strict=True, label='desk') for c in (0.5, 1.0, 1.5)}
lv.claim(dc == {0.5: 5, 1.0: 7, 1.5: 5}, f'desk cut-offs {dc}')
lv.expect('l3', scr('l3', "A desk's signal") + '.widget.options', 7)
lv.expect('l3', scr('l3', "A desk's signal") + '.explain.text', 7)
# l3 quiz
lv.claim(right(2, [0, 1, 3, 4, 6], [0, 0, 0, 1, 1]) == 4, 'q-count-t2: 4 right')
lv.expect('l3', quiz('l3', 'q-count-t2') + '.widget.answer', 4)
lv.claim(F(17, 20) == F(85, 100), 'q-accuracy 17/20 = 85%')
lv.expect('l3', quiz('l3', 'q-accuracy') + '.widget.answer', 0.85)
# l3 code
w = run_code('l3', scr('l3', 'Count in code'))
for tcase, (t, xs, ys) in zip(w['tests'], [(0, TR, SP), (5, TR, SP), (10, TR, SP), (3, TR, SP), (6, [2, 8, 5], [0, 1, 1]), (4, [4, 4, 1], [1, 0, 0])]):
    lv.claim(int(tcase['expect']) == right_b(t, xs, ys), f"count_correct test {tcase['call']} = {tcase['expect']} (method B)")
w = run_code('l3', scr('l3', 'Choose in code'))


def best_b(xs, ys, ts):
    sc = {t: right_b(t, xs, ys) for t in ts}
    m = max(sc.values())
    return min(t for t in ts if sc[t] == m)


for tcase, args in zip(w['tests'], [(TR, SP, range(11)), (TL, TSP, range(7)), (TL, TSP, range(7)), ([3], [1], range(5)), ([3], [0], range(5)), (TR, SP, [7, 3, 6])]):
    lv.claim(int(tcase['expect']) == best_b(*args), f"best_threshold test {tcase['call'][:40]} = {tcase['expect']} (method B)")

# ---------------- l1 ----------------
SIX = [(1, 6, 1), (0, 0, 0), (1, 1, 0), (0, 7, 1), (0, 1, 0), (0, 5, 1)]   # (says free, links, spam)
free_wrong = [i for i, (f, l, s) in enumerate(SIX) if (f == 1) != bool(s)]
lv.claim(free_wrong == [2, 3, 5], 'l1: "free" rule wrong on C, D, F')
lv.claim(lv.files['l1-rules-or-examples']['screens'][0]['widget']['answer'] == ['r2', 'r3', 'r5'], 'l1 hook answer rows C, D, F')
for name, pred, n in (("free", lambda f, l: f == 1, 3), ("links >= 1", lambda f, l: l >= 1, 2), ("links >= 5", lambda f, l: l >= 5, 0), ("links >= 8", lambda f, l: l >= 8, 3)):
    m = sum(1 for f, l, s in SIX if pred(f, l) != bool(s))
    lv.claim(m == n, f'l1 explore rule {name}: {m} mistakes')
frames = lv.files['l1-rules-or-examples']['screens'][1]['canvas']['controls'][0]['frames']
lv.claim([len(fr['highlight']['rows']) for fr in frames] == [3, 2, 0, 3], 'l1 explore frames mark 3, 2, 0, 3 mistakes')
lv.claim(sum(1 for x in [0, 2, 4, 6, 8] if (x >= 4) != (x in (6, 8))) == 1, 'l1 quiz: links >= 4 wrong on 1 of 0, 2, 4, 6, 8')
lv.expect('l1', quiz('l1', 'q-rule-mistakes') + '.widget.answer', 1)

# ---------------- l2 ----------------
lv.expect('l2', scr('l2', 'Features, labels, examples') + '.widget.answer', len(TR))
lv.expect('l2', scr('l2', 'Count the features') + '.widget.answer', 4 - 1)
lv.expect('l2', scr('l2', 'The pattern') + '.widget.answer', 6 - 1)
lv.expect('l2', quiz('l2', 'q-count-examples') + '.widget.answer', 48)

# ---------------- l4 ----------------
memo = {}
for l, s in zip(TR, SP):
    lv.claim(memo.get(l, s) == s, f'memoriser: link count {l} has one label')
    memo[l] = s
answered = [l for l in TE if l in memo]
memo_right = sum(1 for l, s in zip(TE, TS) if l in memo and memo[l] == s)
lv.claim(len(answered) == 4 and memo_right == 2, f'memoriser answers {len(answered)} test emails, {memo_right} right')
lv.claim(sum(1 for l, s in zip(TR, SP) if memo[l] == s) == 10, 'memoriser 10 of 10 on training')
rt = right(5, TE, TS, label='test set')
lv.claim(rt == 5, 'rule t = 5 gets 5 of 6 test emails')
lv.expect('l4', scr('l4', 'The memoriser meets new emails') + '.widget.answer', 4)
lv.expect('l4', scr('l4', 'Training and test') + '.widget.answer', 2)
lv.expect('l4', scr('l4', 'The test score') + '.widget.answer', round(float(F(5, 6)), 4))
lv.claim(abs(float(F(5, 6)) - 0.8333) < 0.0005, '5/6 within the band of 0.8333')
lv.expect('l4', scr('l4', 'The test score') + '.feedback.correct', 83.3)
lv.claim([right(t, TE, TS) for t in (3, 4)] == [6, 6], 'tuning on the test set: t = 3 and t = 4 get 6 of 6')
lv.claim(sum(1 for x in TE if x == 4) == 1, 'the six-email test set has one email with 4 links (the two-email test has none)')
lv.claim(F(18, 24) == F(3, 4), 'l4 quiz 18/24 = 75%')
lv.expect('l4', quiz('l4', 'q-test-share') + '.widget.answer', 0.75)

# ---------------- review-1 ----------------
lv.expect('review', item('review', 'r-count-t4') + '.widget.answer', right(4, [1, 2, 4, 6, 8], [0, 1, 0, 1, 1], label='r-count-t4'))
lv.claim(right_a(4, [1, 2, 4, 6, 8], [0, 1, 0, 1, 1], strict=True) == 4, 'r-count-t4 slip "strict" gives 4')
lv.expect('review', item('review', 'r-accuracy') + '.widget.answer', float(F(14, 16)))
lv.expect('review', item('review', 'r-memo-answers') + '.widget.answer', sum(1 for x in [1, 2, 7, 8] if x in [0, 1, 3, 4, 7]))
lv.expect('review', item('review', 'r-test-score') + '.widget.answer', float(F(right(4, [3, 4, 6, 9], [1, 1, 1, 0], label='r-test-score'), 4)))

# ---------------- homework-1 ----------------
w = run_code('homework', item('homework', 'h-accuracy'))
for tcase in w['tests']:
    args = eval(tcase['call'].replace('accuracy', ''))
    p, l = args
    lv.claim(abs(float(F(sum(1 for a, b in zip(p, l) if a == b), len(l))) - float(eval(tcase['expect']))) < 1e-12, f"accuracy test {tcase['call']}")
w = run_code('homework', item('homework', 'h-split'))
w = run_code('homework', item('homework', 'h-fit-score'))


def fit_b(tx, ty, sx, sy):
    t = best_b(tx, ty, range(11))
    return [t, right_b(t, sx, sy)]


for tcase in w['tests'][:4]:
    args = eval(tcase['call'][len('list(fit_and_score'):-1])
    lv.claim(fit_b(*args) == eval(tcase['expect']), f"fit_and_score test {tcase['call'][:50]} = {tcase['expect']} (method B)")
tie = [right(t, [0, 2, 4, 6], [0, 1, 0, 1], label='h-tie-count') for t in range(8)]
lv.claim(tie == [2, 3, 3, 2, 2, 3, 3, 2], f'h-tie-count counts {tie}')
lv.expect('homework', item('homework', 'h-tie-count') + '.widget.answer', tie.count(max(tie)))

# ---------------- problems-1 ----------------
PX = [0, 1, 2, 3, 4, 6, 7, 9]; PY = [0, 1, 0, 0, 1, 1, 0, 1]
pc = [right(t, PX, PY, label='loans') for t in range(11)]
lv.claim(pc[3] == 5 and max(pc) == 6 and pc.count(6) == 1 and pc.index(6) == 4, f'loans counts {pc}')
lv.expect('problems', 'items[0].parts[0].widget.answer', pc[3])
lv.claim(right_a(3, PX, PY, strict=True) == 6, 'loans slip strict at t = 3 gives 6')
lv.expect('problems', 'items[0].parts[0].widget.wrong[1].value', 6)
lv.expect('problems', 'items[0].parts[1].widget.answer', pc.index(max(pc)))
lv.expect('problems', 'items[0].parts[2].widget.answer', float(F(6, 8)))
lv.expect('problems', 'items[0].parts[3].widget.answer', float(F(right(4, [2, 5, 8, 10], [1, 1, 1, 0], label='loan test'), 4)))
lv.expect('problems', 'items[0].parts[4].widget.answer', sum(1 for x in [2, 5, 8, 10] if x in PX))
lv.expect('problems', 'items[1].parts[3].widget.answer', 5 - 2)
lv.expect('problems', 'items[1].parts[4].widget.answer', float(F(17, 20)))
SX = [0.1, 0.3, 0.4, 0.6, 0.7, 0.9, 1.0, 0.25, 0.55, 0.85]; SY = [0, 0, 1, 0, 1, 1, 1, 0, 1, 0]
QX = [0.15, 0.45, 0.65, 0.95, 0.35]; QY = [0, 1, 0, 1, 1]
tr = {c: right(c, SX, SY, strict=True, label='signal train') for c in (0.2, 0.5, 0.8)}
te = {c: right(c, QX, QY, strict=True, label='signal test') for c in (0.2, 0.5, 0.8)}
lv.claim(tr == {0.2: 6, 0.5: 7, 0.8: 6} and te == {0.2: 4, 0.5: 2, 0.8: 3}, f'signal train {tr} test {te}')
lv.claim(sum(1 for x in SX if x > 0.2) == 9, 'nine training days above 0.2 (slip "buys")')
lv.expect('problems', 'items[2].parts[0].widget.answer', tr[0.2])
lv.expect('problems', 'items[2].parts[1].widget.answer', 0.5)
lv.expect('problems', 'items[2].parts[2].widget.answer', float(F(te[0.5], 5)))
lv.expect('problems', 'items[2].parts[3].widget.answer', float(F(max(te.values()), 5)))
lv.expect('problems', 'items[2].parts[2].widget.wrong[0].value', float(F(tr[0.5], 10)))
lv.expect('problems', 'items[2].parts[3].widget.wrong[1].value', float(F(te[0.8], 5)))

lv.check_wrongs()
lv.report()
