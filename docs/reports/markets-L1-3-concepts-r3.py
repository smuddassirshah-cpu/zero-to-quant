#!/usr/bin/env python3
"""Blind concept audit, markets levels 1 to 3, round 3 (audit-markets-1-3-r3).
Recomputes every graded key, every slip whose feedback names a mistake, and the stated numbers,
straight from the content JSON. Exits 0 when the content is right; a check that fails because
the content is wrong stays failing (see docs/reviews/audit-markets-1-3-r3.md).
Run: python docs/reports/markets-L1-3-concepts-r3.py   (any working directory; NumPy needed)."""
import json, math, os, sys
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'markets')
_cache = {}
def J(f):
    if f not in _cache: _cache[f] = json.load(open(os.path.join(ROOT, f + '.json')))
    return _cache[f]
def W(f, loc):
    d = J(f); kind, i = loc[0], int(loc[1:])
    arr = {'s': d.get('screens'), 'q': d.get('quiz'), 'i': d.get('items')}[kind]
    return arr[i]['widget']
fails, n = [], 0
def dec(x):
    s = repr(float(x)); return len(s.split('.')[1]) if '.' in s and 'e' not in s else 0
def chk(label, got, want, tol=None):
    global n; n += 1
    if tol is None: tol = 0.5 * 10 ** -dec(got)
    if not abs(got - want) <= tol + 1e-12: fails.append(f"{label}: content {got}, recomputed {want:.6f}")
def key(f, loc, want, tol=None): chk(f"{f} {loc} key", W(f, loc)['answer'], want, tol)
def slip(f, loc, sid, want, tol=None):
    w = W(f, loc); v = [x for x in w['wrong'] if x['id'] == sid]
    if not v: fails.append(f"{f} {loc}: no slip {sid}"); return
    chk(f"{f} {loc} slip {sid}", v[0]['value'], want, tol)
def cell(f, loc, r, c, want, tol=None): chk(f"{f} {loc} r{r}c{c}", W(f, loc)['rows'][r][c]['answer'], want, tol)
def opt_true(f, loc, oid):
    global n; n += 1
    o = [x for x in W(f, loc)['options'] if x.get('correct')]
    if [x['id'] for x in o] != [oid]: fails.append(f"{f} {loc}: correct option {[x['id'] for x in o]} != {oid}")
def stated(label, got, want, tol): chk('stated ' + label, got, want, tol)
def ann(n_, r): return (1 - (1 + r) ** -n_) / r
def bond(c, y, T, F=100, f=1):
    return c / f * ann(T * f, y / f) + F / (1 + y / f) ** (T * f)
def bisect(fn, lo, hi):
    for _ in range(200):
        mid = (lo + hi) / 2
        if fn(mid) > 0: lo = mid
        else: hi = mid
    return (lo + hi) / 2

# ---------------- L1 ----------------
f = 'l1-interest-on-interest'
key(f,'s0', 1000*1.05**10 - 1500); slip(f,'s0','balance',1000*1.05**10); slip(f,'s0','simple-int',500); slip(f,'s0','comp-int',1000*1.05**10-1000)
stated('l1 gap at 20y', 653.30, 1000*1.05**20 - 2000, 0.005)
key(f,'s1',52.5); slip(f,'s1','original',50); slip(f,'s1','total',102.5); slip(f,'s1','balance',1102.5)
cell(f,'s2',1,2,52.5); cell(f,'s2',1,3,1102.5); cell(f,'s2',2,1,1102.5); cell(f,'s2',2,2,1102.5*.05,1e-9); cell(f,'s2',2,3,1000*1.05**3,1e-9)
assert 1000*1.05**14 < 2000 < 1000*1.05**15; key(f,'s3',15); slip(f,'s3','simple',20); slip(f,'s3','rule72',72/5)
stated('l1 y14', 1979.93, 1000*1.05**14, .005); stated('l1 y15', 2078.93, 1000*1.05**15, .005); stated('l1 ln2/ln1.05', 14.21, math.log(2)/math.log(1.05), .005)
opt_true(f,'s4','right'); stated('l1 -5% 10y', 598.74, 1000*.95**10, .005)
key(f,'s5',2000*1.06**5); slip(f,'s5','simple',2600); slip(f,'s5','times',2000*1.06*5); slip(f,'s5','once',2120); slip(f,'s5','interest',2000*1.06**5-2000)
opt_true(f,'s6','right')
key(f,'s7',math.log(2)/math.log(1.2),6e-3); slip(f,'s7','simple',5); slip(f,'s7','rule72',3.6); slip(f,'s7','savings',math.log(2)/math.log(1.04))
key(f,'s8',1.01**12-1,6e-5); slip(f,'s8','twelve',.12); slip(f,'s8','month',.01); stated('l1 11268.25',11268.25,10000*1.01**12,.005)
key(f,'q0',1000*.98**10); slip(f,'q0','simple',800); slip(f,'q0','grew',1000*1.02**10)
key(f,'q1',72/8); slip(f,'q1','simple',100/8); stated('l1 9.01',9.01,math.log(2)/math.log(1.08),.005)
opt_true(f,'q2','b'); stated('l1 B', 5604.41, 1000*1.09**20, .005); stated('l1 B-A', 2604.41, 1000*1.09**20-3000, .005)
key(f,'q3',500*1.04**3-500); slip(f,'q3','simple',60); slip(f,'q3','balance',500*1.04**3)

f = 'l2-present-value'
opt_true(f,'s0','today'); stated('l2 900 grows', 1041.86, 900*1.05**3, .005)
w = W(f,'s1'); assert abs(w['answer'] - ((1000/750)**(1/3)-1)) <= w['tol']['abs'] and abs(0.10 - w['answer']) <= w['tol']['abs'], 'l2 s1 tol'
slip(f,'s1','simple',(1000/750-1)/3,5e-5); slip(f,'s1','split',.25/3,5e-5); stated('l2 751.31',751.31,1000/1.1**3,.005)
key(f,'s2',1000/1.05**3); slip(f,'s2','once',1000/1.05); slip(f,'s2','simple',1000/1.15); slip(f,'s2','minus',850); slip(f,'s2','grow',1000*1.05**3)
pv3 = 400/1.05+500/1.05**2+600/1.05**3
cell(f,'s3',1,2,1.05**-2,1e-6); cell(f,'s3',1,3,500/1.05**2); cell(f,'s3',2,2,1.05**-3,1e-6); cell(f,'s3',2,3,600/1.05**3); cell(f,'s3',3,3,pv3)
key(f,'s4',250+pv3); slip(f,'s4','once',250/1.05+1352.77); slip(f,'s4','ignored',pv3); slip(f,'s4','plain',1750)
key(f,'s5',30/.04); slip(f,'s5','pct',30/4); slip(f,'s5','due',780); slip(f,'s5','once',30/1.04); slip(f,'s5','times',30*.04)
key(f,'s6',5000/1.06**3); slip(f,'s6','simple',5000/1.18); slip(f,'s6','once',5000/1.06); slip(f,'s6','minus',5000*.82); slip(f,'s6','grow',5000*1.06**3)
stated('l2 trader gap',39.19,5000/1.18-5000/1.06**3,.005)
opt_true(f,'s7','right'); stated('l2 DF10',.6139,1.05**-10,5e-5)
key(f,'s8',500/1.07**2); slip(f,'s8','simple',500/1.14); slip(f,'s8','once',500/1.07); slip(f,'s8','minus',430); slip(f,'s8','grow',500*1.07**2)
opt_true(f,'s9','right'); stated('l2 lottery',679516.32,50000*ann(20,.04),.005); stated('l2 once',961538.46,1e6/1.04,.005); stated('l2 last',456386.95,1e6/1.04**20,.005)
key(f,'q0',10000/1.05); slip(f,'q0','minus',9500); slip(f,'q0','grow',10500)
key(f,'q1',1000/1.03**10-1000/1.06**10); slip(f,'q1','simple',1000/1.3-1000/1.6); slip(f,'q1','pv6',1000/1.06**10)
key(f,'q2',400); slip(f,'q2','pct',4); slip(f,'q2','due',412)
opt_true(f,'q3','right'); stated('l2 658.16',658.16,800/1.05**4,.005); stated('l2 overprice 8.50',8.50,800/1.2-800/1.05**4,.006)

f = 'l3-comparing-rates'
opt_true(f,'s0','b'); stated('l3 B',1126.83,1000*1.01**12,.005)
opt_true(f,'s1','right'); m = np.arange(1,2000); e = (1+.12/m)**m-1
assert np.all(np.diff(e) > 0) and np.all(np.diff(np.diff(e)) < 0) and e[-1] < math.exp(.12)-1
key(f,'s2',1.02**4-1,5e-5); cell(f,'s3',0,3,1000*1.03**2); cell(f,'s3',1,3,1000*1.005**12); cell(f,'s3',2,3,1000*(1+.06/365)**365)
stated('l3 15p',0.15,1000*(1+.06/365)**365-1000*1.005**12,.005)
key(f,'s4',math.exp(.12)-1,5e-5); slip(f,'s4','quad',.12+.0072,5e-5); slip(f,'s4','monthly',1.01**12-1,5e-6)
stated('l3 daily 12.747',12.747,100*((1+.12/365)**365-1),5e-4); assert 100*(math.exp(.12)-(1+.12/365)**365) < .003
opt_true(f,'s5','one'); key(f,'s6',1.12**(1/12)-1,5e-6)
opt_true(f,'s7','right'); stated('l3 AER',4.91,100*(1.004**12-1),.005); stated('l3 cont',4.92,100*(math.exp(.048)-1),.005)
opt_true(f,'s8','y'); stated('l3 124.38',124.38,200000*((1+.059/12)**12-1-.06),.005)
key(f,'s9',20000*((1+.045/365)**365-1)); slip(f,'s9','simple',900); slip(f,'s9','cont',20000*(math.exp(.045)-1)); slip(f,'s9','balance',20000*(1+.045/365)**365)
key(f,'q0',1.015**12-1,5e-6); opt_true(f,'q1','a'); assert 1.0125**4-1 < .051
key(f,'q2',math.exp(.03)-1,5e-6); key(f,'q3',4*(1.1**.25-1),5e-6); slip(f,'q3','quarter',1.1**.25-1,5e-6); stated('l3 10.38',10.38,100*(1.025**4-1),.005)

f = 'l4-npv'
npv = lambda r, fl: sum(c/(1+r)**t for t, c in enumerate(fl))
opt_true(f,'s0','no'); stated('l4 954.55',954.55,550/1.1+550/1.21,.005)
key(f,'s1',100); irr1 = bisect(lambda r: npv(r,[-1000,550,550]),0,1); assert .06 < irr1 < .07
for r_ in (1,2,3): cell(f,'s2',r_,3,2000/1.08**r_)
cell(f,'s2',4,3,npv(.08,[-5000,2000,2000,2000]))
irr2 = bisect(lambda r: npv(r,[-5000,2000,2000,2000]),0,1); w = W(f,'s3'); chk('l4 s3 irr',w['answer'],irr2,5e-4)
A = [-1000,0,0,1331]; B = [-1000,800,300,100]; opt_true(f,'s4','right')
for lab,v,want in (('A4',183.25,npv(.04,A)),('B4',135.50,npv(.04,B)),('A8',56.59,npv(.08,A)),('B8',77.33,npv(.08,B))): stated('l4 '+lab,v,want,.005)
x = bisect(lambda r: npv(r,A)-npv(r,B),0,.15); stated('l4 cross 6.7',6.7,100*x,.05)
rs = np.linspace(0,1,100001); d = np.array([npv(r,A)-npv(r,B) for r in rs]); assert (np.diff(np.sign(d)) != 0).sum() == 1
key(f,'s5',300*ann(4,.07)-1100); slip(f,'s5','undisc',100); slip(f,'s5','no-cost',300*ann(4,.07)); slip(f,'s5','once',1200/1.07-1100); slip(f,'s5','last',1200/1.07**4-1100); slip(f,'s5','sign',1100-300*ann(4,.07))
opt_true(f,'s6','right')
for t in W(f,'s7')['tests']:
    chk('l4 code '+t['call'], float(t['expect']), eval(t['call'],{'npv':npv}), 1e-9)
bf = [-95,4,4,104]; key(f,'s8',npv(.05,bf)); slip(f,'s8','undisc',17); slip(f,'s8','no-cost',npv(.05,bf)+95); slip(f,'s8','no-principal',npv(.05,[-95,4,4,4]))
stated('l4 bond irr',5.87,100*bisect(lambda r: npv(r,bf),0,1),.005)
ff = [-130000,50000,50000,50000]; key(f,'s9',npv(.07,ff)); slip(f,'s9','undisc',20000); slip(f,'s9','no-cost',npv(.07,ff)+130000); slip(f,'s9','at8',npv(.08,ff))
stated('l4 feed irr',7.51,100*bisect(lambda r: npv(r,ff),0,1),.005)
key(f,'q0',npv(.05,[-200,120,120])); slip(f,'q0','undisc',40); slip(f,'q0','no-cost',npv(.05,[0,120,120]))
opt_true(f,'q1','right'); key(f,'q2',100); opt_true(f,'q3','right'); stated('l4 interp',.0923,.08+.02*40/65,5e-5)

# ---------------- L2 ----------------
f = 'l5-pricing-a-bond'
P5 = bond(4,.05,5); key(f,'s1',P5); slip(f,'s1','no-discount',120); slip(f,'s1','last-only',104/1.05**5); slip(f,'s1','coupons-only',4*ann(5,.05))
cell(f,'s2',2,2,1.05**-3,1e-6); cell(f,'s2',2,3,4/1.05**3,5e-5); cell(f,'s2',4,2,1.05**-5,1e-6); cell(f,'s2',4,3,104/1.05**5,5e-5); cell(f,'s2',5,3,P5,5e-5)
key(f,'s3',bond(4,.05,5,f=2)); slip(f,'s3','annual',P5); slip(f,'s3','full-coupon',4*ann(10,.025)+100/1.025**10); slip(f,'s3','full-rate',2*ann(10,.05)+100/1.05**10); slip(f,'s3','five-periods',2*ann(5,.025)+100/1.025**5)
stated('l5 equiv annual bond', bond(4,.05,5,f=2), 4.05*ann(5,1.025**2-1)+100/1.025**10, 1e-9)
key(f,'s4',.04); key(f,'s5',100/1.05**5); slip(f,'s5','with-coupon',104/1.05**5); slip(f,'s5','simple',100/1.25)
opt_true(f,'s6','right'); opt_true(f,'s7','right'); stated('l5 102.72',102.72,bond(6,.05,3),.005); stated('l5 swapped',97.33,bond(5,.06,3),.005)
bp = lambda face,coupon,years,yld: sum(face*coupon/(1+yld)**t for t in range(1,years+1)) + face/(1+yld)**years
for t in W(f,'s9')['tests']: chk('l5 code '+t['call'], float(t['expect']), eval(t['call'],{'bond_price':bp}), 1e-9)
key(f,'s10',98.5*100+100); slip(f,'s10','clean',9850); slip(f,'s10','per-pound',985000); slip(f,'s10','whole-coupon',10050); slip(f,'s10','full-year',10250)
opt_true(f,'q0','right'); stated('l5 q0 principal',86.38,100/1.05**3,.005); stated('l5 q0 coupons',13.62,5*ann(3,.05),.005)
key(f,'q1',bond(6,.04,2)); slip(f,'q1','undiscounted',112); slip(f,'q1','principal',100/1.04**2)
key(f,'q2',100/1.05**10); slip(f,'q2','simple',100/1.5); slip(f,'q2','ten-off',50)
key(f,'q3',bond(6,.04,2,f=2)); slip(f,'q3','annual',bond(6,.04,2)); slip(f,'q3','full-coupon',6*ann(4,.02)+100/1.02**4); slip(f,'q3','two-periods',3*ann(2,.02)+100/1.02**2)

f = 'l6-yield'
opt_true(f,'s0','above'); key(f,'s1',104/1.06**5); slip(f,'s1','at-five',104/1.05**5); slip(f,'s1','price',bond(4,.06,5))
y92 = bisect(lambda y: bond(4,y,5)-92,.001,1); key(f,'s2',y92,5e-4); slip(f,'s2','current',4/92,5e-5); stated('l6 5.894',5.894,100*y92,5e-4)
stated('l6 5.85',92.18,bond(4,.0585,5),.005); stated('l6 5.90',91.97,bond(4,.059,5),.005)
for lab,v,y in (('6',91.58,.06),('5.5',93.59,.055),('5.75',92.58,.0575),('5.875',92.07,.05875)): stated('l6 bis '+lab,v,bond(4,y,5),.005)
lo,hi = 4.,8.; rows = W(f,'s3')['rows']
for r_ in range(1,4):
    mid = (lo+hi)/2
    if bond(4,mid/100,5) > 92: lo = mid
    else: hi = mid
    for c,v in ((0,lo),(1,hi),(2,(lo+hi)/2)):
        if isinstance(rows[r_][c],dict): chk(f'l6 s3 r{r_}c{c}',rows[r_][c]['answer'],v,1e-9)
assert 4/2**20 < 4e-6
def dP(y): return -sum(t*c/(1+y)**(t+1) for t,c in enumerate([0,4,4,4,4,104]))
newton3 = {}
for y0 in (.04,.05,.06,.08):
    y = y0
    for _ in range(3): y -= (bond(4,y,5)-92)/dP(y)
    newton3[y0] = abs(y-y92)*100
assert all(v < 4e-6 for v in newton3.values()), newton3   # "Newton gets there in three steps", from either end of the bracket
D = -dP(.05)/P5; stated('l6 D',4.40,D,.005); key(f,'s4',4.40*95.67*.01,.006); slip(f,'s4','no-price',4.4); slip(f,'s4','true',P5-bond(4,.06,5))
conv = sum(t*(t+1)*c/(1.05)**(t+2) for t,c in enumerate([0,4,4,4,4,104]))/P5; stated('l6 convexity',24.47,conv,.005)
p2a,p2b,p10a,p10b = bond(4,.05,2),bond(4,.06,2),bond(4,.05,10),bond(4,.06,10)
for lab,v,want in (('2y5',98.14,p2a),('2y6',96.33,p2b),('10y5',92.28,p10a),('10y6',85.28,p10b)): stated('l6 '+lab,v,want,.005)
cell(f,'s5',0,3,100*(p2b/p2a-1),.005); cell(f,'s5',1,3,100*(p10b/p10a-1),.005)
# FINDING 1: the step hint prints "-7.00/92.28 = -7.58%"; that quotient is -7.586, which is -7.59 to two places.
hint = J(f)['screens'][5]['hints'][2]['text']; n += 1
if '-7.00/92.28 = -7.58' in hint: fails.append(f"l6-yield s5 hint prints -7.00/92.28 = -7.58%; that quotient is {100*(-7.00/92.28):.3f}%, so -7.59% to two places")
def moddur(c,y,T):
    if not c: return T/(1+y)
    cf=[0]+[c]*(T-1)+[100+c]; return sum(t*x/(1+y)**(t+1) for t,x in enumerate(cf))/bond(c,y,T)
stated('l6 D10',7.96,moddur(4,.05,10),.005); stated('l6 D2',1.87,moddur(4,.05,2),.005)
key(f,'s6',5/1.05,.005); slip(f,'s6','times',5.25); opt_true(f,'s7','right'); stated('l6 fall',4.10,P5-bond(4,.06,5),.005)
key(f,'s8',4/95.67,5e-5); slip(f,'s8','inverse',4.33/95.67,5e-5)
opt_true(f,'s9','zero10'); ds = {'zero10':10/1.05,'coupon10':moddur(8,.05,10),'short':moddur(4,.05,2),'zero2':2/1.05}
assert max(ds,key=ds.get)=='zero10' and ds['zero2'] < 2 and ds['short'] < 2
key(f,'s10',440000); slip(f,'s10','tenth',44000); slip(f,'s10','no-pct',44e6); slip(f,'s10','one-pct',1e5); stated('l6 428058',428058,1e7*(1-bond(4,.06,5)/P5),1)
opt_true(f,'s11','right'); opt_true(f,'q0','right'); key(f,'q1',7*102*.005); slip(f,'q1','no-price',3.5); slip(f,'q1','full-pct',7.14); slip(f,'q1','fraction',.035)
key(f,'q2',6/105,5e-5); opt_true(f,'q3','right'); stated('l6 84.03',84.03,bond(4,.08,5),.005); stated('l6 12.2',12.2,100*(1-bond(4,.08,5)/P5),.05); stated('l6 tangent',83.04,P5+dP(.05)*.03,.005)

f = 'l7-shares'
key(f,'s0',50000); slip(f,'s0','one-share',.5); key(f,'s1',.2); cell(f,'s2',0,1,5.2*400); cell(f,'s2',1,1,100*.13/5.2); cell(f,'s2',2,1,5.2/.4)
key(f,'s3',2080); slip(f,'s3','share-of-debt',2080+50e6*400/400e6); opt_true(f,'s4','right')
key(f,'s5',2/(.08-.03)); slip(f,'s5','no-growth',25); slip(f,'s5','ten',40*(1-(1.03/1.08)**10),.005); slip(f,'s5','plus',2/.11); stated('l7 150y',39.97,40*(1-(1.03/1.08)**150),.005)
key(f,'s7',2/.07); slip(f,'s7','no-growth',20); slip(f,'s7','plus',2/.13); opt_true(f,'s8','right'); stated('l7 1.85',1.85,2/1.08,.005); opt_true(f,'s9','right')
cell(f,'s10',0,1,3.45*1200); cell(f,'s10',1,1,100*124.2/4140); cell(f,'s10',2,1,4140/276)
key(f,'s11',23/5); slip(f,'s11','average',4); key(f,'q0',2.1); opt_true(f,'q1','right'); key(f,'q2',30); slip(f,'q2','no-growth',1.5/.09); slip(f,'q2','plus',1.5/.13)
key(f,'q3',.03); slip(f,'q3','earnings',2.5/40); slip(f,'q3','payout',1.2/2.5)

f = 'l8-measuring-returns'
key(f,'s0',.09); slip(f,'s0','price-only',.06); slip(f,'s0','div-only',.03); slip(f,'s0','pounds',.045)
key(f,'s1',1.2*.9*1.05-1); slip(f,'s1','added',.15); slip(f,'s1','average',.05)
cell(f,'s2',1,4,100*(40.42+1.29-43)/43,.005); cell(f,'s2',2,4,100*(44.06+1.21-40.42)/40.42,.005)
key(f,'s3',1.134**(1/3)-1,5e-5); slip(f,'s3','divide',.134/3,5e-5); key(f,'s4',math.log(1.134),5e-5)
opt_true(f,'s5','right'); stated('l8 -13.4',-13.4,100*(.75**.5-1),.05)
key(f,'s6',1.0075**12-1,5e-5); stated('l8 26.82',26.82,100*(1.02**12-1),.005); opt_true(f,'s7','right')
key(f,'s8',.05/.12,5e-5); slip(f,'s8','no-rf',.75); slip(f,'s8','inverse',2.4)
g = 1.12*.92*1.15; cell(f,'s9',0,1,100*(g-1),.005); cell(f,'s9',1,1,100*(g**(1/3)-1),.005); cell(f,'s9',2,1,19/3,.005)
def annualised(returns):
    growth = 1.0
    for r in returns: growth *= 1 + r
    return growth ** (1/len(returns)) - 1
for t in W(f,'s10')['tests']: chk('l8 code '+t['call'], float(t['expect']), eval(t['call'],{'annualised':annualised}), 1e-12)
opt_true(f,'s11','right'); key(f,'q0',.08); key(f,'q1',1.6105**.2-1,5e-5); slip(f,'q1','divide',.6105/5,5e-5); key(f,'q2',math.exp(.04)-1,5e-5); opt_true(f,'q3','right'); stated('l8 10.03',10.03,100*(1.008**12-1),.005)

# ---------------- L3 ----------------
f = 'l9-agreeing-today'
key(f,'s0',30); opt_true(f,'s1','loss'); key(f,'s2',-30)
for r_,s in enumerate((170,200,215,240)): cell(f,'s3',r_,1,s-200); cell(f,'s3',r_,2,200-s)
opt_true(f,'s4','nothing'); opt_true(f,'s6','forty'); key(f,'s7',200); key(f,'s8',1e6*.82-1e6*(.82-.79)); slip(f,'s8','added',850000)
opt_true(f,'s9','call'); S = np.linspace(80,120,401); assert np.allclose((S-100)+np.maximum(100-S,0), np.maximum(S-100,0))
key(f,'q0',-7.5); key(f,'q1',-3000); key(f,'q2',1000*540-1000*(540-600)); slip(f,'q2','sign',480000); opt_true(f,'q3','right')

f = 'l10-cost-of-carry'
key(f,'s0',105); opt_true(f,'s1','flat'); key(f,'s2',105); slip(f,'s2','discounted',100/1.05)
cell(f,'s3',0,2,-105); cell(f,'s3',2,2,108); cell(f,'s3',3,1,0); cell(f,'s3',3,2,3); opt_true(f,'s4','reverse'); opt_true(f,'s5','fair')
stated('l10 cont',105.13,100*math.exp(.05),.005)
Fd = (100-2/1.05**.5)*1.05; key(f,'s7',Fd,.006); slip(f,'s7','not-grown',103); slip(f,'s7','not-disc',98*1.05); slip(f,'s7','added',107)
stated('l10 alt',Fd,105-2*1.05**.5,1e-9); stated('l10 2.05',2.05,2*1.05**.5,.005)
key(f,'s8',1.25*1.05/1.04,6e-4); slip(f,'s8','inverted',1.25*1.04/1.05,5e-5); w = W(f,'s8'); assert abs(1.2625-w['answer']) <= w['tol']['abs']
key(f,'s9',8000*.99,5); w = W(f,'s9'); assert abs(8000*1.04/1.05-w['answer']) <= w['tol']['abs']; slip(f,'s9','ignored',8320); slip(f,'s9','added',8720)
key(f,'q0',50*1.04**2); slip(f,'q0','simple',54); slip(f,'q0','one-year',52); opt_true(f,'q1','carry'); key(f,'q2',2000*1.05+10)
stated('l10 gold, Hull (S0+U)(1+r)', 2110, (2000+10/1.05)*1.05, 1e-9); opt_true(f,'q3','same')

f = 'l11-margin'
def run_margin(prices, n_, pv, init, maint, topup='initial'):
    bal = init*abs(n_); calls = []; bals = []
    for a,b in zip(prices, prices[1:]):
        bal += n_*pv*(b-a); bals.append(bal)
        call = ((init if topup=='initial' else maint)*abs(n_) - bal) if bal < maint*abs(n_) else 0
        calls.append(call); bal += call
    return calls, bals
key(f,'s0',-400); slip(f,'s0','tick',-200)
px = [8000,7960,7900,7830,7830,7880]
calls,bals = run_margin(px,1,10,6000,4500); assert calls == [0,0,1700,0,0] and bals == [5600,5000,4300,6000,6500]
key(f,'s2',1700); slip(f,'s2','maint',200); slip(f,'s2','loss',700)
rows = W(f,'s3')['rows']
for r_ in range(1,5):
    for c,v in ((2,10*(px[r_+1]-px[r_])),(3,bals[r_]),(4,calls[r_])): chk(f'l11 s3 r{r_}c{c}',rows[r_][c]['answer'],v,1e-9)
key(f,'s4',6000+1700); slip(f,'s4','day',6700)
calls,bals = run_margin([8000,7930,7840,7900,7880],1,10,6000,4500); key(f,'s5',sum(calls)); assert bals[1]==4400 and 6000-1200==4800; slip(f,'s5','maint',100); slip(f,'s5','loss',1200)
opt_true(f,'s6','credit'); key(f,'s7',0); slip(f,'s7','stuck',7990-8010)
calls,_ = run_margin([8010,8260],-10,10,6000,4500); key(f,'s8',calls[0]); slip(f,'s8','maint',45000-35000); slip(f,'s8','one',2500); assert abs(800000*250/8010-25000) < 100
key(f,'q0',-600); key(f,'q1',0); key(f,'q2',1800); slip(f,'q2','maint',300); opt_true(f,'q3','zero')

f = 'l12-selling-what-you-do-not-own'
key(f,'s0',8); opt_true(f,'s1','p0'); opt_true(f,'s2','you')
cell(f,'s3',1,1,-50000*.03*.25); cell(f,'s3',2,1,-600); cell(f,'s3',3,1,-42000); cell(f,'s3',4,1,50000-375-600-42000)
key(f,'s4',1000*(50-65)-975); slip(f,'s4','no-costs',-15000); slip(f,'s4','costs-helped',-15000+975)
key(f,'s5',100); opt_true(f,'s6','right'); key(f,'s7',6); slip(f,'s7','inverted',2/12,5e-5); slip(f,'s7','product',24); slip(f,'s7','diff',10)
key(f,'s8',-8000+12000); slip(f,'s8','both-long',-20000); slip(f,'s8','sign',-4000)
key(f,'s9',100000-150000-2000); slip(f,'s9','no-fee',-50000)
key(f,'q0',985); slip(f,'q0','plus',1015); opt_true(f,'q1','none'); key(f,'q2',-550); slip(f,'q2','no-div',-50); slip(f,'q2','div-gain',450); key(f,'q3',12000)

f = 'l13-leverage'
RE = lambda L,ra,r: L*ra-(L-1)*r
key(f,'s0',RE(2,.1,.05)); slip(f,'s0','no-int',.2); slip(f,'s0','int-all',.05); opt_true(f,'s1','pivot')
for L in (1,2,3.5,5): assert abs(RE(L,.05,.05)-.05) < 1e-12
stated('l13 L4 up',.25,RE(4,.1,.05),1e-9); stated('l13 L4 down',-.55,RE(4,-.1,.05),1e-9)
key(f,'s2',3); slip(f,'s2','borrowed',2); key(f,'s3',RE(2,-.3,.05)); slip(f,'s3','no-int',-.6); slip(f,'s3','int-helps',-.55)
assert abs(W(f,'s4')['points'][0]['target']['x'] + 1/4) < 1e-12
key(f,'s5',RE(3,.08,.05)); slip(f,'s5','no-int',.24); slip(f,'s5','int-once',.19); slip(f,'s5','int-three',.09); stated('l13 -34',-.34,RE(3,-.08,.05),1e-9)
key(f,'s7',10000/.75); slip(f,'s7','orig',10000+.25*20000); slip(f,'s7','zero',10000); slip(f,'s7','pct',10000/.8)
key(f,'s8',(.2*300000+200000*.06*.25)/100000); slip(f,'s8','no-int',.6); slip(f,'s8','year',.72); stated('l13 further 15%',15,100*37000/240000,.5)
key(f,'s9',3); slip(f,'s9','net',.6); slip(f,'s9','long',1.8)
key(f,'q0',.07); key(f,'q1',1.0); key(f,'q2',RE(2,.12,.04)); slip(f,'q2','double-int',.16); opt_true(f,'q3','fifth')

# ---------------- reviews and homework ----------------
f = 'review-1'
key(f,'i0',5000*1.03**6); slip(f,'i0','simple',5900); slip(f,'i0','interest',5000*1.03**6-5000)
key(f,'i1',2500/1.06**4); slip(f,'i1','simple',2500/1.24); slip(f,'i1','once',2500/1.06)
key(f,'i2',1.0075**12-1,5e-6); key(f,'i3',300*ann(3,.06)-800); slip(f,'i3','undisc',100); slip(f,'i3','no-cost',300*ann(3,.06))
opt_true(f,'i4','right'); stated('r1 11.90',11.90,math.log(2)/math.log(1.06),.005)
key(f,'i5',10000/1.005**24); slip(f,'i5','annual',10000/1.06**2); slip(f,'i5','simple',10000/1.12)
key(f,'i6',1.08**.25-1,5e-6); opt_true(f,'i7','right')
A=[-2000,0,2600]; B=[-2000,1300,1200]
for lab,v,want in (('A5',358.28,npv(.05,A)),('B5',326.53,npv(.05,B)),('A10',148.76,npv(.1,A)),('B10',173.55,npv(.1,B))): stated('r1 '+lab,v,want,.005)
stated('r1 cross',7.7,100*bisect(lambda r: npv(r,A)-npv(r,B),0,.5),.05)
key(f,'i8',1500); slip(f,'i8','due',1545); stated('r1 4%',1125,45/.04,1e-9)

f = 'homework-1'
key(f,'i0',3000*1.018**24); slip(f,'i0','simple',3000*(1+.018*24)); slip(f,'i0','annual',3000*1.216**2); slip(f,'i0','interest',3000*1.018**24-3000); stated('h1 EAR',23.87,100*(1.018**12-1),.005)
v = 1000/1.05+2000/1.05**3+3000/1.05**5; key(f,'i1',v); slip(f,'i1','plain',6000); slip(f,'i1','all-five',6000/1.05**5); slip(f,'i1','all-three',6000/1.05**3)
aers = {'monthly':(1+.046/12)**12-1,'annual':.047,'cont':math.exp(.0455)-1,'right':(1+.0465/4)**4-1}; assert max(aers,key=aers.get)=='right'; opt_true(f,'i2','right')
for v_,k in ((4.698,'monthly'),(4.700,'annual'),(4.655,'cont'),(4.732,'right')): stated('h1 AER '+k,v_,100*aers[k],5e-4)
stated('h1 4.89',.0489,12*(1.05**(1/12)-1),5e-5)
def irr(fl): return bisect(lambda r: npv(r,fl),0,1)
for t in W(f,'i5')['tests']: chk('h1 irr '+t['call'][:40], float(t['expect']), eval(t['call'],{'irr':irr,'round':round}), 1e-9)
assert 2**-33 > 1e-10 > 2**-34
u = (550+math.sqrt(550**2+4*1000*550))/2000; key(f,'i6',u-1,5e-6); slip(f,'i6','simple',.1/1.5,5e-5); slip(f,'i6','u',u,5e-6); slip(f,'i6','neg',(550-math.sqrt(550**2+4*1000*550))/2000-1,5e-6)
for lab,v_,want in (('4%',611564.69,45000*ann(20,.04)),('5%',560799.47,45000*ann(20,.05)),('4.2%',600875.25,45000*ann(20,.042)),('4.3%',595634.83,45000*ann(20,.043)),('last',20537.41,45000/1.04**20)): stated('h1 pension '+lab,v_,want,.005)
stated('h1 breakeven',4.22,100*bisect(lambda r: 45000*ann(20,r)-600000,.001,.2),.005)

f = 'review-2'
key(f,'i0',bond(5,.06,3,f=2)); slip(f,'i0','annual',bond(5,.06,3))
# FINDING 2: the named mistake, £5 every six months at 3% a period, gives 110.8344, so 110.83 to the penny; the file holds 110.84.
slip(f,'i0','full-coupon',5*ann(6,.03)+100/1.03**6)
slip(f,'i0','full-rate',2.5*ann(6,.06)+100/1.06**6)
opt_true(f,'i1','right'); stated('r2 D 2y8%',1.84,moddur(8,.05,2),.005); stated('r2 D zero2',1.90,2/1.05,.005); assert moddur(8,.05,2) < 2/1.05 < moddur(8,.05,10) < 10/1.05
opt_true(f,'i2','right'); key(f,'i3',.1); slip(f,'i3','divide',.105); opt_true(f,'i4','right'); stated('r2 94.00',94.00,bond(3,.04,7),.005)
key(f,'i5',6.2*5e6*.0025); slip(f,'i5','full-point',310000); slip(f,'i5','quarter',7750); key(f,'i6',2.5/50+.02); slip(f,'i6','minus',.03)
opt_true(f,'i7','right'); stated('r2 98.17',98.17,bond(5,.06,2),.005); stated('r2 97.27',97.27,bond(5,.065,2),.005); stated('r2 ytm',6.09,100*bisect(lambda y: bond(5,y,2)-98,.001,1),.005)
key(f,'i8',.5); slip(f,'i8','raw',.11/.16,5e-5); slip(f,'i8','inverse',2)

f = 'homework-2'
key(f,'i0',bond(3,.04,7),.005); slip(f,'i0','principal',100/1.04**7)
y97 = bisect(lambda y: bond(5,y,3)-97,.001,1); key(f,'i1',y97,5e-5); slip(f,'i1','current',5/97,5e-5); stated('h2 97.33',97.33,bond(5,.06,3),.005); stated('h2 96.03',96.03,bond(5,.065,3),.005)
def ytm(price, face, coupon, years): return bisect(lambda y: bp(face,coupon,years,y)-price,0,1)
for t in W(f,'i3')['tests']: chk('h2 ytm '+t['call'], float(t['expect']), eval(t['call'],{'ytm':ytm,'round':round}), 1e-9)
key(f,'i4',38/7); slip(f,'i4','average',5); key(f,'i5',.08-1.8/60); slip(f,'i5','plus',.11)
key(f,'i6',1.1**(1/3)-1,5e-5); slip(f,'i6','divide',.1/3,5e-5)
p4 = bond(4,.06,4); key(f,'i7',(p4+4-P5)/P5,5e-5); slip(f,'i7','unchanged',(bond(4,.05,4)+4-P5)/P5,5e-5); slip(f,'i7','no-coupon',(p4-P5)/P5,5e-5); slip(f,'i7','five-year',(bond(4,.06,5)+4-P5)/P5,5e-5)
pb = bond(5,.06,4); stated('h2 96.5349',96.5349,pb,5e-5); sl = sum(t*c/1.06**(t+1) for t,c in enumerate([0,5,5,5,105])); stated('h2 slope',338.58,sl,.005); stated('h2 D',3.51,sl/pb,.005)
stated('h2 94.86',94.86,bond(5,.065,4),.005); stated('h2 hold',6.00,100*((bond(5,.06,3)+5)/pb-1),.005); stated('h2 42.86',42.86,3/.07,.005); stated('h2 16.7',16.7,1/.06,.05)

f = 'review-3'
key(f,'i0',-15); key(f,'i1',80*1.03**2); slip(f,'i1','simple',84.8); slip(f,'i1','one',82.4); key(f,'i2',110-105); slip(f,'i2','pv',5/1.05)
calls,_ = run_margin([8000,7800],3,10,6000,4500); key(f,'i3',calls[0]); slip(f,'i3','maint',13500-12000); slip(f,'i3','one',2000)
key(f,'i4',300*(15-18)-20); slip(f,'i4','fee-helped',-880); key(f,'i5',RE(4,-.1,.05)); slip(f,'i5','int-once',-.45)
assert sorted(o['id'] for o in W(f,'i6')['options'] if o.get('correct')) == ['short-fwd','short-share']
Fd2 = (60-1.5/1.04**.25)*1.04; key(f,'i7',Fd2); slip(f,'i7','ignored',62.4); slip(f,'i7','not-grown',62.4-1.5); slip(f,'i7','not-disc',58.5*1.04); stated('r3 alt',Fd2,62.4-1.5*1.04**.75,1e-9)
key(f,'i8',18000/.7); slip(f,'i8','orig',18000+9000); slip(f,'i8','of-loan',18000*1.3); stated('r3 14.3',14.3,100*(1-18000/.7/30000),.05)

f = 'homework-3'
key(f,'i0',2e6*.83+2e6*(.85-.83)); slip(f,'i0','sign',1620000); key(f,'i2',104-Fd,.006); slip(f,'i2','no-div',-1); slip(f,'i2','not-grown',1)
hp = [8000,7900,7820,7850,7700,7640]; calls,bals = run_margin(hp,2,10,6000,4500); key(f,'i3',sum(calls)); assert bals == [10000,8400,12600,9600,8400] and min(bals) > 4500
slip(f,'i3','one',calls[1]); slip(f,'i3','maint',sum(run_margin(hp,2,10,6000,4500,'maint')[0])); assert 20*(8000-7640) == 7200
def margin_calls(prices, contracts, point_value, initial, maintenance): return run_margin(prices,contracts,point_value,initial,maintenance)[0]
for t in W(f,'i4')['tests']:
    got = eval(t['call'],{'margin_calls':margin_calls}); want = eval(t['expect']); n += 1
    if not (len(got)==len(want) and all(math.isclose(a,b,abs_tol=1e-9) for a,b in zip(got,want))): fails.append('h3 margin '+t['call'])
key(f,'i5',-6000-1000-180); slip(f,'i5','div-income',-5180); key(f,'i6',1/9,5e-5); slip(f,'i6','eq-quarter',.25/3,5e-5)
key(f,'i7',10000/65000,5e-5); slip(f,'i7','no-growth',.2)
stated('h3 642',642,600*1.05+12,1e-9); stated('h3 arb',18,660-630-12,1e-9)
up = (64-1.2*1.07**-.5)*1.07; lo_ = (64-1.2*1.03**-.5)*1.03-.5
for lab,v_,want in (('upper',67.2387,up),('upper alt',67.2621,64*1.07-1.2*1.03**.5),('lower',64.2021,lo_),('lower alt',64.1787,64*1.03-1.2*1.07**.5-.5),('one rate',65.9704,(64-1.2*1.05**-.5)*1.05),('opt',.5613,67.8-up)): stated('h3 two-rate '+lab,v_,want,5e-5)
assert lo_ < (64-1.2*1.05**-.5)*1.05 < up

# ---------------- empirical claims: Monte Carlo ----------------
rng = np.random.default_rng(20261126)
# (a) l8 summary trap: the arithmetic average of yearly returns is never below the annualised return, and exceeds it when returns vary
R = rng.normal(.06,.18,(200000,3)).clip(-.95); am = R.mean(1); gm = np.prod(1+R,1)**(1/3)-1
assert np.all(am >= gm-1e-12) and (am-gm).mean() > .01
# (b) l8 s11: Sharpe 0.42 against 0.40 cannot be told apart from a few years of data (5 years, 20,000 pairs of funds)
a = rng.normal(.09,.12,(20000,5)); b = rng.normal(.12,.20,(20000,5))
sa = (a.mean(1)-.04)/a.std(1,ddof=1); sb = (b.mean(1)-.04)/b.std(1,ddof=1); pwin = (sa > sb).mean(); assert .45 < pwin < .56, pwin
# (c) l13 q1: leverage makes a 50% loss of equity far more likely (yearly asset return N(6%, 18%), borrowing at 4%)
ra = rng.normal(.06,.18,1000000); p1 = (ra <= -.5).mean(); p3 = (RE(3,ra,.04) <= -.5).mean(); assert p3 > 50*max(p1,1e-6) and p3 > .10, (p1,p3)
# (d) l13 s8: volatility scales with L
assert abs(np.std(RE(3,ra,.04))/np.std(ra)-3) < 1e-9
# (e) l1: the rule of 72 runs short at 20%, long at 5%, and is close near 8%
assert 72/20 < math.log(2)/math.log(1.2) and 72/5 > math.log(2)/math.log(1.05) and abs(72/8-math.log(2)/math.log(1.08)) < .01

print(f"{n} checks, {len(fails)} failed; Newton error after 3 steps (percentage points): {newton3}; P(A's Sharpe > B's over 5 years) = {pwin:.3f}; P(lose half) L=1 {p1:.2e}, L=3 {p3:.3f}")
for x in fails: print('FAIL', x)
sys.exit(1 if fails else 0)
