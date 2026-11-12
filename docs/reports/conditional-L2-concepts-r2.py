"""Round 2 concept audit, course `conditional`, level 2 (l7 to l12, review-2,
homework-2 with its performance task, problems-2, fluency-l7-turning-around).
Run from the repo root:
    python3 docs/reports/conditional-L2-concepts-r2.py
Bayes results are recomputed three ways where it matters: the path formula,
the odds form, and a seeded Monte Carlo run. Exits 0 on correct content.
Checks expected to FAIL on the content as audited (they are findings):
  finding 1: l12 screens[3] explain says the 8-sided die "lost a little" when
             its chance rose from 1/3 to 3/7;
  finding 2: l11 screens[8] tree leaves are conditional rates that add to 2,
             and the `joint` slip feedback calls 0.49 the joint chance (0.245).
"""
from conditional_concepts_r2_lib import *

ltp = lambda ws, ps: sum(a * b for a, b in zip(ws, ps))
ln = math.log


def mc_bayes(prior, hit, false, n, seed):
    def t(r):
        h = r.random() < prior
        e = r.random() < (hit if h else false)
        return e, h
    return mc_cond(t, n, seed)


# ---------------- l7 turning the condition around ----------------
L = 'l7-turning-around'
trees(L)
v = get(L, 'screens[1].canvas.params.values')
ok('l7 venn totals 100', v == {'A': 2, 'AB': 8, 'B': 18, 'none': 72} and sum(v.values()) == 100)
ill, pos = v['A'] + v['AB'], v['B'] + v['AB']
A(L, 'screens[1]', F(8, ill), whole=F(8, 100), pos=F(8, pos), **{'ill-share': F(ill, 100)})
TAP(L, 'screens[2]', ['AB', 'B'])
A(L, 'screens[3]', F(8, pos), inverse=F(8, ill), whole=F(8, 100), well=F(18, pos))
A(L, 'screens[4]', 0.1 * 0.8, added=0.9, sens=0.8, base=0.1)
A(L, 'screens[5]', ltp([0.1, 0.9], [0.8, 0.2]), average=0.5, **{'ill-only': 0.08, 'add-rates': 1.0})
C(L, 'screens[6]', 'right')
ok('l7 s6 0.08/0.26', close(bayes(0.1, 0.8, 0.2), 8 / 26, 1e-12))
C(L, 'screens[7]', 'right', bayes(F(2, 10), F(9, 10), F(3, 10)), inverse=0.9, joint=0.18, prior=0.2)
ORD(L, 'screens[8]', ['d1', 'd2', 'd3', 'd4'])
S(L, 'screens[8].widget.lines[3].text', 'which is not 0')
up = bayes(0.55, 0.8, 0.3)
A(L, 'screens[9]', up, inverse=0.8, joint=0.44, prior=0.55, fires=0.575)
m = mc_bayes(0.55, 0.8, 0.3, 400000, 71)
ok(f'l7 MC up given signal {m:.4f} vs {up:.4f}', abs(m - up) < 0.004)
# summary idea 3: with P(A and B) > 0 the two conditionals agree exactly when P(A) = P(B)
rng = random.Random(9)
good = True
for _ in range(3000):
    pab = rng.uniform(0.01, 0.3)
    pa = pab + rng.uniform(0, 0.3)
    pbb = pab + rng.uniform(0, 0.3)
    good &= (abs(pab / pa - pab / pbb) < 1e-12) == (abs(pa - pbb) < 1e-12)
S(L, 'summary.ideas', 'the two directions agree exactly when $P(A) = P(B)$', good)
face = [(r, s) for r in range(13) for s in range(4)]
C(L, 'quiz[0]', 'right', cond(face, lambda c: c[0] == 12, lambda c: c[0] >= 10), one=1, deck=F(4, 52), suit=F(1, 4))
A(L, 'quiz[1]', 0.6 * 0.3 / 0.4, inverse=0.6, joint=0.18, upside=0.6 * 0.4 / 0.3)
C(L, 'quiz[2]', 'right', 0.6 * 0.25 / 0.25, complement=0.4, half=0.6 * 0.25)
C(L, 'quiz[3]', 'right')

# ---------------- l8 base rates ----------------
L = 'l8-base-rates'
trees(L)
post = lambda b: bayes(b, 0.9, 0.05)
C(L, 'screens[0]', 'right')
ok('l8 hook about 15%', abs(post(0.01) - 0.15) < 0.01)
S(L, 'screens[0].explain.text', 'over five times bigger', 0.0495 / 0.009 > 5)
C(L, 'screens[1]', 'right')
ok('l8 s1 crosses 0.5 between 5% and 6%', post(0.05) < 0.5 < post(0.06) and abs(0.05 / 0.95 - 0.0526) < 1e-3)
S(L, 'screens[1].hints[2].text', 'At 5% the right bar reads 0.49. At 6% it reads 0.53',
  round(post(0.05), 2) == 0.49 and round(post(0.06), 2) == 0.53)
S(L, 'screens[1].widget.options[2].why', 'near 0.89', round(post(0.30), 2) == 0.89)
S(L, 'screens[1].widget.options[3].why', 'about 0.95', round(post(0.50), 2) == 0.95)
A(L, 'screens[2]', 0.01 * 0.9 + 0.99 * 0.05, unweighted=0.009 + 0.05, rates=0.95, **{'ill-only': 0.009})
A(L, 'screens[3]', post(0.01), inverse=0.9, joint=0.009, base=0.01)
S(L, 'screens[3].explain.text', 'fifteenfold', 15 <= post(0.01) / 0.01 < 16)
A(L, 'screens[4]', 1 - post(0.01), joint=0.0495, **{'fp-rate': 0.05, 'true-share': post(0.01)})
A(L, 'screens[5]', post(0.5), hit=0.9, base=0.5)
ok('l8 s5 base rate cancels at 50%', abs(post(0.5) - 0.9 / 0.95) < 1e-12)
C(L, 'screens[6]', 'right')
S(L, 'screens[6].feedback.byKey.same', "clinic A's positives are 85% false and clinic B's only 11%",
  round(1 - post(0.01), 2) == 0.85 and round(1 - post(0.30), 2) == 0.11)
S(L, 'screens[6].explain.text', r'0.27 / 0.305 \approx 0.89', round(post(0.3), 2) == 0.89)
C(L, 'screens[7]', 'right')
# "much rarer than the false-positive rate makes most positives false": b << f  =>  posterior < 1/2
bad = 0
for b in [i / 1000 for i in range(1, 60)]:
    for f_ in [i / 100 for i in range(1, 60)]:
        for h in (0.5, 0.9, 1.0):
            if b <= f_ / 2 and bayes(b, h, f_) >= 0.5:
                bad += 1
ok('l8 claim: base rate at most half the false-positive rate gives posterior below 1/2', bad == 0)
A(L, 'screens[8]', bayes(0.002, 0.95, 0.01), inverse=0.95, joint=0.0019, spec=0.99)
A(L, 'screens[9]', bayes(0.05, 0.9, 0.1), inverse=0.9, joint=0.045, base=0.05, luck=0.1)
A(L, 'quiz[0]', bayes(0.05, 0.6, 0.1), inverse=0.6, joint=0.03, base=0.05)
C(L, 'quiz[1]', 'right')
S(L, 'quiz[1].explain.text', 'about 4.3 times', abs(post(0.10) / post(0.01) - 4.33) < 0.05 and post(0.10) / post(0.01) < 10)
A(L, 'quiz[2]', bayes(0.5, 0.8, 0.2), base=0.5, joint=0.4)
A(L, 'quiz[3]', bayes(0.02, 1.0, 0.02), perfect=1.0, spec=0.98, base=0.02)
m = mc_bayes(0.01, 0.9, 0.05, 3000000, 81)
ok(f'l8 MC condition given positive {m:.4f} vs {post(0.01):.4f}', abs(m - post(0.01)) < 0.004)

# ---------------- l9 natural frequencies ----------------
L = 'l9-natural-frequencies'
trees(L)
cells = get(L, 'screens[0].canvas.params.cells')
plus = [f'r{i + 1}c{j + 1}' for i, row in enumerate(cells) for j, c in enumerate(row) if c == '+']
top = [p for p in plus if p.startswith('r1c')]
TAP(L, 'screens[0]', plus)
ok('l9 grid 8 true positives, 9 false', len(top) == 8 and len(plus) == 17)
A(L, 'screens[1]', F(len(top), len(plus)), inverse=F(8, 10), everyone=F(8, 100), base=F(10, 100))
A(L, 'screens[2]', 0.05 * 990, hit=0.9 * 990, negatives=0.95 * 990, cond=9)
A(L, 'screens[3]', 9 + 50, healthy=50, cond=9, everyone=1000)
w = get(L, 'screens[4].widget')
ok('l9 s4 accepts both 9/59 and the exact 9/58.5', close(9 / 59, w['answer'], w['tol']['abs']) and close(9 / 58.5, w['answer'], w['tol']['abs']))
A(L, 'screens[4]', 9 / 59, inverse=0.9, everyone=0.009, base=0.01)
A(L, 'screens[5]', 90 + 495, everyone=90 + 500, healthy=495, cond=90)
S(L, 'screens[5].explain.text', r'\tfrac{90}{585} = \tfrac{2}{13}', F(90, 585) == F(2, 13) == F(9, 1000) / F(585, 10000))
C(L, 'screens[6]', 'right', F(240, 268), everyone=F(240, 280), inverse=0.8, joint=F(240, 1000))
C(L, 'screens[7]', 'right')
ORD(L, 'screens[8]', ['s1', 's2', 's3', 's4', 's5'])
g = get(L, 'screens[9].canvas.params.cells')
sig_top = sum(1 for c in g[0] if c == 'S') * 10
sig_rest = sum(1 for row in g[1:] for c in row if c == 'S') * 10
ok('l9 s9 grid: 140 trend signals, 80 others, 200 trend days', (sig_top, sig_rest, len(g[0]) * 10, sum(len(r) for r in g) * 10) == (140, 80, 200, 1000))
A(L, 'screens[9]', F(sig_top, sig_top + sig_rest), inverse=F(sig_top, 200), everyone=F(140, 140 + 100), joint=F(140, 1000), base=F(200, 1000))
S(L, 'screens[9].explain.text', 'a 70% detection rate and a 10% false-alarm rate', (F(sig_top, 200), F(sig_rest, 800)) == (F(7, 10), F(1, 10)))
A(L, 'quiz[0]', 0.8 * 50 + 0.1 * 950, everyone=40 + 100, defaulters=40, others=95)
A(L, 'quiz[1]', F(40, 135), inverse=0.8, everyone=0.04, base=0.05)
C(L, 'quiz[2]', 'right', 1, hit=F(2, 3), everyone=F(20, 1000), base=F(30, 1000))
C(L, 'quiz[3]', 'right')

# ---------------- l10 odds form ----------------
L = 'l10-odds-form'
trees(L)
A(L, 'screens[0]', 49.5 / 9, before=99, flipped=9 / 49.5, prob=9 / 58.5)
A(L, 'screens[1]', from_odds(F(10, 55)), flip=1 - from_odds(F(10, 55)), **{'odds-as-p': F(10, 55)})
ok('l10 s2 1/5.5 = 18/99', F(10, 55) == F(18, 99))
A(L, 'screens[2]', F(18, 99) / F(1, 99), probs=F(2, 13) / F(1, 100), hit=0.9, drop=99 - 5.5)
ok('l10 s2 LR 18 = 0.9 / 0.05 and odds form matches Bayes', abs(0.9 / 0.05 - 18) < 1e-9 and abs(from_odds(odds(0.01) * 18) - bayes(0.01, 0.9, 0.05)) < 1e-12)
C(L, 'screens[3]', 'right')
lab = {x['text']: x['x'] for x in get(L, 'screens[3].canvas.params.labels')}
ok('l10 s3 log-odds labels', all(abs(lab[t] - ln(a / b)) < 1e-4 for t, a, b in [('1:99', 1, 99), ('1:9', 1, 9), ('1:4', 1, 4), ('1:1', 1, 1), ('4:1', 4, 1), ('9:1', 9, 1)]))
pts = get(L, 'screens[3].canvas.state.points')
ok('l10 s3 after point', abs(pts[1]['x'] - (ln(1 / 99) + ln(18))) < 1e-4)
A(L, 'screens[4]', from_odds(F(1, 4) * 6), probs=0.2 * 6, prior=0.2, **{'lr-odds': from_odds(F(6))})
A(L, 'screens[5]', from_odds(odds(F(55, 100)) * 1), hit=0.3, joint=0.55 * 0.3, sum=0.55 + 0.3)
ok('l10 s5 LR 1 leaves Bayes at the prior', abs(bayes(0.55, 0.3, 0.3) - 0.55) < 1e-12)
A(L, 'screens[6]', from_odds(odds(F(1, 10)) * 3), probs=0.3, prior=0.1, **{'lr-post': from_odds(F(3))})
ORD(L, 'screens[7]', ['o1', 'o2', 'o3', 'o4'])
n = 0
o = F(1, 4)
while o < 1:
    o *= F(3, 2)
    n += 1
A(L, 'screens[8]', n, added=1, half=2, **{'round-down': 3})
S(L, 'screens[8].widget.accept', 'Three give odds of $0.84$; four give $1.27$', round(0.25 * 1.5 ** 3, 2) == 0.84 and round(0.25 * 1.5 ** 4, 2) == 1.27)
S(L, 'screens[8].explain.text', r'\approx 3.42', abs(ln(4) / ln(1.5) - 3.42) < 0.005)
S(L, 'screens[8].prose', 'Whether or not a trend has begun, each signal fires independently of the others')
A(L, 'quiz[0]', from_odds(F(3)), against=F(1, 4), third=F(1, 3))
A(L, 'quiz[1]', from_odds(odds(F(1, 2)) * 4), probs=2.0, **{'lr-as-p': F(1, 4)})
C(L, 'quiz[2]', 'right')
S(L, 'quiz[2].explain.text', 'about 0.17', F(1, 50) * 10 == F(1, 5) and round(float(from_odds(F(1, 5))), 2) == 0.17)
A(L, 'quiz[3]', from_odds(F(1) * F(1, 4)), probs=0.5 / 4, **{'lr-as-p': 0.25})
# Monte Carlo: posterior odds = LR x prior odds (leak with LR 6 on a 20% prior)
m = mc_bayes(0.2, 0.6, 0.1, 500000, 101)
ok(f'l10 MC odds update {m:.4f} vs 0.6', abs(m - 0.6) < 0.004)

# ---------------- l11 updating twice ----------------
L = 'l11-updating-twice'
trees(L)
p1 = bayes(F(1, 100), F(9, 10), F(1, 20))
p2 = bayes(p1, F(9, 10), F(1, 20))
ok('l11 chain', p1 == F(2, 13) and p2 == F(36, 47))
A(L, 'screens[0]', p2, stuck=p1, hit=0.9, joint=p1 * F(9, 10))
S(L, 'screens[0].prose', 'errs independently of the first, both with and without the condition')
C(L, 'screens[1]', 'right')
ok('l11 s1 line points', abs(get(L, 'screens[1].canvas.state.points')[2]['x'] - (ln(1 / 99) + 2 * ln(18))) < 2e-4)
A(L, 'screens[2]', F(1, 99) * 18 * 18, added=F(36, 99), once=F(18, 99), lr=324)
ok('l11 s2 odds 324/99 is p2', from_odds(F(324, 99)) == p2)
lrn = F(1, 10) / F(95, 100)
pn = from_odds(F(1, 99) * 18 * lrn)
ok('l11 s3 4/213', lrn == F(2, 19) and pn == F(4, 213))
A(L, 'screens[3]', pn, base=0.01, ignored=p1, miss=0.1)
S(L, 'screens[3].feedback.byKey.base', 'multiply to about 1.9', abs(18 * float(lrn) - 1.9) < 0.01)
ec = get(L, 'screens[3].explain.canvas')
ok('l11 s3 line positions', abs(ec['points']['p2']['x'] - ln(4 / 209)) < 2e-4)
C(L, 'screens[4]', 'right')
ok('l11 s4 line positions', abs(get(L, 'screens[4].explain.canvas.points.p1.x') - ln(F(1, 99) * lrn)) < 2e-4)
A(L, 'screens[5]', F(81, 100) / F(25, 10000), once=18, added=36, diff=0.81 / 0.05)
C(L, 'screens[6]', 'right', None, **{'old-prior': p1, 'no-prior': 0.81, 'squared': float(p1) ** 2})
S(L, 'screens[6].widget.options[1].text', '$0.766$', round(float(p2), 3) == 0.766)
ORD(L, 'screens[7]', ['c1', 'c2', 'c3', 'c4'])
two_calls = bayes(F(1, 2), F(49, 100), F(9, 100))
A(L, 'screens[8]', two_calls, one=0.7, joint=F(1, 2) * F(49, 100), likelihood=0.49, either=1 - 0.09)
ok('l11 s8 odds route', from_odds(F(7, 3) ** 2) == two_calls == F(49, 58))
# FINDING 2 (wrong): trees(L) above fails on this screen's leaves. They show the
# conditional rates 0.49, 0.51, 0.09, 0.91 (which add to 2), not the path chances
# 0.245, 0.255, 0.045, 0.455. The slip feedback then calls 0.49 the joint chance.
fbj = get(L, 'screens[8].feedback.byKey.joint')
ok('l11 screens[8].feedback.byKey.joint calls 0.49 "up with both calls up, out of everything"; the joint chance is 0.245',
   not ('out of everything' in fbj and abs(0.5 * 0.49 - next(w['value'] for w in get(L, 'screens[8].widget.wrong') if w['id'] == 'joint')) > 1e-9))
C(L, 'screens[9]', 'right', from_odds(F(7, 3)), double=two_calls, none=0.5, more=0.91)
S(L, 'summary.formula.note', 'err independently given $H$ and given $\\neg H$')
A(L, 'quiz[0]', from_odds(odds(F(1, 5)) * 6), probs=1.2, **{'first-only': from_odds(odds(F(1, 5)) * 2), 'second-only': from_odds(odds(F(1, 5)) * 3)})
C(L, 'quiz[1]', 'right', from_odds(odds(F(3, 10)) * 4 * F(1, 4)))
C(L, 'quiz[2]', 'right')


# Monte Carlo: two conditionally independent positives; then a copied second call
def two_pos(r):
    h = r.random() < 0.01
    q = 0.9 if h else 0.05
    return (r.random() < q and r.random() < q), h


m = mc_cond(two_pos, 6000000, 111)
ok(f'l11 MC two positives {m:.3f} vs {float(p2):.3f}', abs(m - float(p2)) < 0.02)


def copy(r):
    upd = r.random() < 0.5
    a = upd if r.random() < 0.7 else (not upd)
    return a, upd      # B copies A, so "both say up" is the event "A says up"


m = mc_cond(copy, 400000, 112)
ok(f'l11 MC copied call {m:.4f} vs 0.7', abs(m - 0.7) < 0.004)


def pos_neg(r):
    h = r.random() < 0.01
    q = 0.9 if h else 0.05
    return (r.random() < q and not (r.random() < q)), h


m = mc_cond(pos_neg, 6000000, 113)
ok(f'l11 MC positive then negative {m:.4f} vs {float(pn):.4f}', abs(m - float(pn)) < 0.002)

# ---------------- l12 many hypotheses ----------------
L = 'l12-many-hypotheses'
pri = [F(1, 3)] * 3
lik5 = [F(0), F(1, 6), F(1, 8)]
lik3 = [F(1, 4), F(1, 6), F(1, 8)]
post5 = posterior(pri, lik5)
C(L, 'screens[0]', 'right')
ok('l12 s0 6-sided die most likely', post5.index(max(post5)) == 1)
TB(L, 'screens[1]', {(0, 2): lik5[0], (1, 2): lik5[1], (2, 2): lik5[2]})
S(L, 'screens[1].explain.text', r'\tfrac{7}{24}', sum(lik5) == F(7, 24))
TB(L, 'screens[2]', {(i, 3): pri[i] * lik5[i] for i in range(3)})
S(L, 'screens[2].explain.text', r'\tfrac{7}{72}', sum(a * b for a, b in zip(pri, lik5)) == F(7, 72))
A(L, 'screens[3]', post5[1], raw=F(1, 18), prior=F(1, 3), lik=F(1, 6))
S(L, 'screens[3].explain.text', r'0, $\tfrac{4}{7}$ and $\tfrac{3}{7}$', post5 == [0, F(4, 7), F(3, 7)])
# FINDING 1 (wrong): the 8-sided die went from 1/3 to 3/7, so it gained
txt = get(L, 'screens[3].explain.text')
ok('l12 screens[3].explain.text says the 8-sided die "lost a little" but its chance rose from 1/3 to 3/7',
   not ('8-sided die lost' in txt and post5[2] > pri[2]))
post53 = posterior(post5, lik3)
A(L, 'screens[4]', post53[1], stale=post5[1], raw=post5[1] * lik3[1], **{'old-prior': posterior(pri, lik3)[1]})
S(L, 'screens[4].feedback.correct', r'\tfrac{25}{168}', sum(a * b for a, b in zip(post5, lik3)) == F(25, 168))
S(L, 'screens[4].explain.text', '0.64 against 0.36', post53 == [0, F(16, 25), F(9, 25)])
C(L, 'screens[5]', 'right', post53[0], quarter=F(1, 4), third=F(1, 3))
ok('l12 s5: a 3 has the same 1/4 chance as every other face of the 4-sided die', len({F(1, 4) for _ in range(4)}) == 1)
cp = posterior([0.6, 0.2, 0.2], [0.5, 0.8, 0.2])
A(L, 'screens[6]', cp[1], raw=0.16, lik=0.8, prior=0.2, **{'lik-norm': 0.8 / 1.5})
C(L, 'screens[7]', 'right')
S(L, 'screens[7].prose', 'cannot overlap and whose priors add to 1')
rp = posterior([0.6, 0.3, 0.1], [0.05, 0.15, 0.6])
TB(L, 'screens[8]', {(0, 3): rp[0], (1, 3): rp[1], (2, 3): rp[2]})
S(L, 'screens[8].feedback.byKey.r2c3', 'If you got 0.75', abs(0.6 / (0.05 + 0.15 + 0.6) - 0.75) < 1e-9)
mp = posterior([0.5, 0.3, 0.2], [0.012, 0.03, 0.045])
A(L, 'screens[9]', mp[0], prior=0.5, raw=0.006, **{'lik-norm': 0.012 / 0.087})
mg = posterior([0.1, 0.6, 0.3], [0.8, 0.5, 0.3])
A(L, 'quiz[0]', mg[0], raw=0.08, prior=0.1, **{'lik-norm': 0.8 / 1.6})
C(L, 'quiz[1]', 'right')
ok('l12 cromwell: prior 0 stays 0', posterior([F(0), F(1)], [F(10), F(1)])[0] == 0)
A(L, 'quiz[2]', 0.12 / 0.2, raw=0.12, third=1 / 3)
C(L, 'quiz[3]', 'right')


# Monte Carlo: three dice, a 5 then a 3
def dice(r):
    s = r.choice([4, 6, 8])
    return (r.randint(1, s) == 5 and r.randint(1, s) == 3), s == 6


m = mc_cond(dice, 3000000, 121)
ok(f'l12 MC 6-sided after 5 then 3: {m:.3f} vs 0.64', abs(m - 0.64) < 0.01)
m = mc_cond(lambda r: (lambda s: (r.randint(1, s) == 5, s == 8))(r.choice([4, 6, 8])), 2000000, 122)
ok(f'l12 MC 8-sided after a 5: {m:.3f} vs 3/7 (above the prior 1/3)', abs(m - 3 / 7) < 0.01 and m > 1 / 3)

# ---------------- review-2 ----------------
L = 'review-2'
v = get(L, 'items[0].canvas.params.values')
ok('review-2 venn', v == {'A': 10, 'AB': 30, 'B': 50, 'none': 110} and sum(v.values()) == 200)
A(L, 'items[0]', F(30, 80), inverse=F(30, 40), all=F(30, 200))
ins = bayes(0.005, 0.98, 0.02)
A(L, 'items[1]', ins, inverse=0.98, base=0.005, joint=0.0049)
S(L, 'items[1].explain.text', 'about 80% of flags are false', abs(1 - ins - 0.80) < 0.01)
A(L, 'items[2]', 0.75 * 400 + 0.05 * 9600, everyone=300 + 500, fraud=300, genuine=480)
S(L, 'items[2].explain.text', r'\approx 0.38', round(300 / 780, 2) == 0.38)
A(L, 'items[3]', 0.45 / 0.15, diff=0.30, flip=0.15 / 0.45)
A(L, 'items[4]', from_odds(odds(F(1, 4)) * 4), probs=1.0, prior=0.25, **{'lr-odds': from_odds(F(4))})
A(L, 'items[5]', from_odds(odds(F(1, 10)) * 9), probs=0.9, one=from_odds(odds(F(1, 10)) * 3), added=from_odds(odds(F(1, 10)) * 6))
tc = posterior([F(1, 2), F(1, 4), F(1, 4)], [F(1, 4), F(9, 16), F(1)])
A(L, 'items[6]', tc[2], raw=0.25, **{'lik-norm': 1 / (0.25 + 0.5625 + 1), 'one-flip': posterior([F(1, 2), F(1, 4), F(1, 4)], [F(1, 2), F(3, 4), F(1)])[2]})
ok('review-2 16/33', tc[2] == F(16, 33))
C(L, 'items[7]', 'right')
A(L, 'items[8]', bayes(0.5, 0.7, 0.1), hit=0.7, base=0.5, joint=0.35)

# ---------------- homework-2 ----------------
L = 'homework-2'
an = bayes(0.02, 0.85, 0.03)
A(L, 'items[0]', an, inverse=0.85, joint=0.017, base=0.02)
S(L, 'items[0].explain.text', 'Under 37%', an < 0.37)
A(L, 'items[1]', 1 / odds(F(1, 100)), probs=50, half=49.5)
o2 = odds(F(5, 100)) * (F(95, 100) / F(10, 100)) * (F(20, 100) / F(98, 100))
A(L, 'items[2]', from_odds(o2), prior=0.05, **{'a-only': from_odds(odds(F(5, 100)) * F(19, 2)), 'b-pos': from_odds(odds(F(5, 100)) * F(19, 2) * 40)})
ok('homework-2 h-two-tests 5/54', from_odds(o2) == F(5, 54) and o2 == F(5, 49))
fd = posterior([F(4, 10), F(3, 10), F(2, 10), F(1, 10)], [F(0), F(1, 6), F(1, 8), F(1, 12)])
TB(L, 'items[3]', {(i, 2): fd[i] for i in range(4)})
S(L, 'items[3].feedback.byKey.r2c2', r'If you got $\tfrac{1}{3}$', F(1, 8) / (F(1, 6) + F(1, 8) + F(1, 12)) == F(1, 3))
ORD(L, 'items[4]', ['s1', 's2', 's3', 's4'])
# explain: posterior >= 1/2 exactly when f/h <= b/(1-b)
good = True
rng = random.Random(4)
for _ in range(4000):
    b, h, f_ = rng.uniform(0.001, 0.6), rng.uniform(0.05, 1), rng.uniform(0.001, 0.6)
    good &= (bayes(b, h, f_) >= 0.5) == (f_ / h <= b / (1 - b))
    good &= abs(bayes(b, h, f_) - 1 / (1 + (f_ / h) * ((1 - b) / b))) < 1e-12
S(L, 'items[4].explain.text', r'at most $\tfrac{b}{1 - b}$', good)
bt = from_odds(odds(F(10, 200)) * 16 * 16)
A(L, 'items[5]', bt, one=from_odds(odds(F(10, 200)) * 16), probs=0.64, **{'no-prior': from_odds(F(256))})
S(L, 'items[5].explain.text', 'about 6.4 real and 0.475 noise', (10 * 0.64, 190 * 0.05 * 0.05) == (6.4, 0.47500000000000003) or abs(190 * 0.0025 - 0.475) < 1e-12)
S(L, 'items[5].feedback.byKey.one', '8 real of 17.5 passes', abs(10 * 0.8 + 190 * 0.05 - 17.5) < 1e-12)
mod = get(L, 'items[6].model')
n = 1
while from_odds(F(18) ** n / 99) <= F(95, 100):
    n += 1
ok('homework-2 long (c) n = 3', n == 3 and '$n = 3$' in mod and r'\approx 2.61' in mod and abs(ln(1881) / ln(18) - 2.61) < 0.005)
ok('homework-2 long (c) checks', abs(float(from_odds(F(324, 99))) - 0.766) < 5e-4 and abs(float(from_odds(F(5832, 99))) - 0.983) < 5e-4)
ok('homework-2 long rubric total', sum(r['points'] for r in get(L, 'items[6].rubric')) == 10)
C(L, 'items[7]', 'right')
A(L, 'items[8]', from_odds(odds(F(6, 10)) * F(1, 3)), probs=0.2, prior=0.6, **{'wrong-way': from_odds(odds(F(6, 10)) * 3)})
# performance task: two filters on a price feed
b, hJ, fJ, hV, fV = F(2, 100), F(9, 10), F(6, 100), F(7, 10), F(3, 100)
pBJ = bayes(b, hJ, fJ)
pBJV = b * hJ * hV / (b * hJ * hV + (1 - b) * fJ * fV)
pBJV4 = b * hJ * hV / (b * hJ * hV + (1 - b) * fV)
ok('perf task part 3', pBJ == F(15, 64) and pBJV == F(50, 57))
ok('perf task odds check 1/49 x 15 x 70/3 = 50/7', odds(b) * (hJ / fJ) * (hV / fV) == F(50, 7))
ok('perf task part 4', pBJV4 == F(3, 10) and odds(pBJ) * (hV / (fV / fJ)) == F(3, 7) and fV <= fJ)
pm = get(L, 'items[9].model')
for frag in [r'\frac{15}{64}', r'\frac{50}{57}', r'\frac{3}{10}', '0.0768', '0.001764', '0.014364', '0.0294', r'\tfrac{0.7}{0.5} = 1.4']:
    ok(f'perf task model shows {frag}', frag in pm)
rub = get(L, 'items[9].rubric')
ok('perf task rubric 10 points, four required', sum(r['points'] for r in rub) == 10 and sum(1 for r in rub if r.get('required')) == 4)


def filters(shared):
    def t(r):
        bad = r.random() < 0.02
        if bad:
            j, v_ = r.random() < 0.9, r.random() < 0.7
        elif shared:
            j = r.random() < 0.06
            v_ = j and r.random() < 0.5        # V only with J, and P(V | good) = 0.03
        else:
            j, v_ = r.random() < 0.06, r.random() < 0.03
        return (j and v_), bad
    return t


m = mc_cond(filters(False), 4000000, 131)
ok(f'perf MC independent filters {m:.3f} vs 50/57', abs(m - 50 / 57) < 0.01)
m = mc_cond(filters(True), 4000000, 132)
ok(f'perf MC shared stale quote {m:.3f} vs 0.3', abs(m - 0.3) < 0.01)

# ---------------- problems-2 ----------------
L = 'problems-2'
I = 'items[0].parts'
A(L, I + '[0]', 5000 * 0.08 * 0.45, **{'all-targets': 400, 'rate-on-all': 2250})
A(L, I + '[1]', 180 + 4600 * 0.06, **{'false-on-all': 180 + 300, 'others-only': 276})
A(L, I + '[2]', F(180, 456), inverse=0.45, **{'count-slip': F(180, 480), 'over-false': F(180, 276)})
bstar = F(6, 100) / (F(45, 100) + F(6, 100))
ok('problems-2 break-even base rate', bayes(bstar, F(45, 100), F(6, 100)) == F(1, 2))
A(L, I + '[3]', bstar, half=0.5, **{'no-complement': 0.06 / 0.45, 'rate-gap': 0.39})
I = 'items[1].parts'
o0 = odds(F(15, 100))
A(L, I + '[0]', o0, probability=0.15, reversed=1 / o0)
A(L, I + '[1]', o0 * 3, **{'prob-times': 0.45, 'inverse-lr': o0 / 3, 'rate-gap': o0 + F(4, 10)})
A(L, I + '[2]', from_odds(o0 * 3 * 6), odds=o0 * 18, **{'ratio-sum': from_odds(o0 * 9), 'prob-slip': from_odds(odds(F(45, 100)) * 6)})
k = 0
o = o0 * 18
while from_odds(o) < F(95, 100):
    o *= 3
    k += 1
A(L, I + '[3]', k, ninety=1, **{'prob-as-odds': 0})
S(L, I + '[3].feedback.byKey.ninety', 'about 0.905', round(float(from_odds(o0 * 54)), 3) == 0.905)
C(L, I + '[4]', 'not-independent')
I = 'items[2].parts'
pr, lk = [F(5, 10), F(3, 10), F(2, 10)], [F(3, 10), F(5, 10), F(8, 10)]
f1 = ltp(pr, lk)
A(L, I + '[0]', f1, average=sum(lk) / 3, **{'aggressive-only': 0.16})
q1 = posterior(pr, lk)
A(L, I + '[1]', q1[2], likelihood=0.8, **{'not-normalised': 0.16, 'average-slip': F(16, 100) / (sum(lk) / 3)})
q2 = posterior(q1, lk)
A(L, I + '[2]', q2[2], once=q1[2], **{'not-normalised': q1[2] * F(8, 10)})
ok('problems-2 posteriors after two fills', q2 == [F(45, 248), F(75, 248), F(128, 248)])
A(L, I + '[3]', ltp(q2, lk), equal=sum(lk) / 3, **{'prior-weights': f1, 'most-likely': 0.8})
I = 'items[3].parts'
pa = F(2, 100) * F(95, 100) + F(98, 100) * F(4, 100)
A(L, I + '[0]', pa, **{'errors-only': 0.019, 'rates-added': 0.99, 'false-on-all': 0.019 + 0.04})
ea = bayes(F(2, 100), F(95, 100), F(4, 100))
A(L, I + '[1]', ea, inverse=0.95, specificity=0.96, **{'false-slip': 0.019 / 0.059})
eb = from_odds(odds(ea) * 70)
A(L, I + '[2]', eb, odds=odds(ea) * 70, product=ea * F(7, 10), **{'skipped-a': from_odds(odds(F(2, 100)) * 70)})
A(L, I + '[3]', 980000 * 0.04 * 0.01, **{'a-only': 39200, 'all-prints': 400})
A(L, I + '[4]', F(392, 13300 + 392), **{'over-all': F(392, 1000000), 'over-errors': F(392, 13300), 'error-share': eb})
ok('problems-2 parts 3 and 5 agree', abs(float(1 - eb) - 392 / 13692) < 1e-12)


def broker(r):
    kind = r.choices([0, 1, 2], [0.5, 0.3, 0.2])[0]
    q = [0.3, 0.5, 0.8][kind]
    return (r.random() < q and r.random() < q), r.random() < q


m = mc_cond(broker, 1500000, 141)
ok(f'problems-2 MC third fill given two fills {m:.4f} vs 0.6185', abs(m - float(ltp(q2, lk))) < 0.004)

# ---------------- fluency-l7 ----------------
L = 'fluency-l7-turning-around'
fam = {f['id']: f for f in get(L, 'families')}
ok('fluency weights', [f['weight'] for f in get(L, 'families')] == [1, 2, 1])
rng = random.Random(77)
good = True
for _ in range(4000):          # from-counts: key, slips and the where-clause separate them
    tot_ = rng.choice([100, 200, 400])
    a, c, b_ = rng.randint(5, 30), rng.randint(1, 9), rng.randint(3, 40)
    if b_ == c:
        continue
    key, fwd, joint = F(a, a + b_), F(a, a + c), F(a, tot_)
    good &= key != fwd and key != joint and a + c <= tot_ and b_ <= tot_ - (a + c)
ok('fluency from-counts: population is consistent and slips never equal the key', good)
ok('fluency from-counts formulas', fam['from-counts']['let']['key'] == 'a/(a + b)' and fam['from-counts']['let']['fwd'] == 'a/(a + c)'
   and fam['from-counts']['let']['joint'] == 'a/tot' and fam['from-counts']['where'] == ['b != c'])
good = True
for pp in fam['from-rates']['vars']['pp']['pick']:
    for s in range(60, 96, 5):
        for f_ in range(5, 31, 5):
            env = {'pp': pp, 's': s, 'f': f_, 'abs': abs}
            key = eval(fam['from-rates']['let']['key'], env)
            good &= abs(key - float(bayes(F(pp, 100), F(s, 100), F(f_, 100)))) < 1e-12
            nof = eval(fam['from-rates']['let']['nof'], env)
            good &= abs(nof - (pp * s / 10000) / (pp * s / 10000 + f_ / 100)) < 1e-12
ok('fluency from-rates key is Bayes on every draw', good)
good = True
for pp in fam['every-positive-path']['vars']['pp']['pick']:
    for s in range(60, 96, 5):
        for f_ in range(5, 41, 5):
            env = {'pp': pp, 's': s, 'f': f_}
            key = eval(fam['every-positive-path']['let']['key'], env)
            good &= abs(key - (pp / 100 * s / 100 + (1 - pp / 100) * f_ / 100)) < 1e-12
            good &= abs(key - eval(fam['every-positive-path']['let']['unw'], env)) > 1e-9
            good &= abs(key - eval(fam['every-positive-path']['let']['j'], env)) > 1e-9
ok('fluency every-positive-path key is total probability; slips differ from it', good)

done()
