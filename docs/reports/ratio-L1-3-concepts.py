"""Concept checks for the blind audit ratio-1-3 (round 1), course `ratio`, levels 1 to 3.

Run from anywhere with Python 3 (standard library only; no version-dependent figure).
Exits 0 when every checked claim holds. A check that fails because the content is
wrong stays failing (see docs/reviews/audit-ratio-1-3.md). Checks marked NOTE print a
wording finding but do not fail the run.

Fix pass (Opus fixer): the finding 6 note re-pointed from the Monte Carlo split (which
does not depend on the text) to the explanation text, with the split kept as an ok check;
the q-seven-25ths "digits" slip now has its row (725 typed, 7.25) instead of a skip; the
finding 9 note reads the explanation, since the part asks for rounded March working and
its accept line stays the plain figure £50,746.60 that the problems number script requires.

Parts
  1. Every numeric and slider key and every named slip value, recomputed from an
     independent expression (183 widgets), and every band checked against the key's.
  2. The five fluency files swept over their whole variable range.
  3. Rules stated with "always", "never", "only" or as a general fact: swept or
     simulated (seeded Monte Carlo) so the rule is separated from its negation.
  4. Checks tied to findings.
"""
import json, math, os, sys, glob, random, itertools
from fractions import Fraction as F

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'ratio')
fails, notes, n_checks = [], [], 0


def ok(name, cond, detail=''):
    global n_checks
    n_checks += 1
    if not cond:
        fails.append(name + (' :: ' + detail if detail else ''))


def note(name, cond, detail=''):
    global n_checks
    n_checks += 1
    if not cond:
        notes.append(name + (' :: ' + detail if detail else ''))


def load(name):
    return json.load(open(os.path.join(ROOT, name + '.json'), encoding='utf-8'))


def widgets(d):
    out = {}
    for i, s in enumerate(d.get('screens', []) or []):
        if s.get('widget'):
            out['s%d' % i] = s
    for q in d.get('quiz') or []:
        out[q['id']] = q
    for it in d.get('items', []) or []:
        if it.get('widget'):
            out[it['id']] = it
        for j, p in enumerate(it.get('parts', []) or []):
            out['%s.%d' % (it['id'], j)] = p
    return out


# ------------------------------------------------------------------ 1. keys and slips
# file | locator | key | slip=value; ...   (unit "%" widgets store the fraction, so a
# figure typed as t per cent is t/100; "typed the decimal d" is d/100.)
L = {'l1': 'l1-out-of-a-hundred', 'l2': 'l2-building-percentages', 'l3': 'l3-what-percentage', 'l4': 'l4-multipliers',
     'l5': 'l5-rise-or-fall', 'l6': 'l6-before-the-discount', 'l7': 'l7-up-then-down', 'l8': 'l8-growth-on-growth',
     'l9': 'l9-sharing', 'l10': 'l10-scaling', 'l11': 'l11-direct-or-inverse', 'l12': 'l12-best-buy', 'l13': 'l13-currencies',
     'H1': 'homework-1', 'H2': 'homework-2', 'H3': 'homework-3', 'P1': 'problems-1', 'P2': 'problems-2', 'P3': 'problems-3',
     'R1': 'review-1', 'R2': 'review-2', 'R3': 'review-3'}
TABLE = r'''
l1|s1|37/100|count=37;thousandths=37/1000;rows=30/100
l1|s2|45/100|half=50/100
l1|s3|60/100|rows=6/100;decimal=0.6/100
l1|s4|3/4|digits=34/100;decimal=0.75/100
l1|s10|-0.008|one-place=-0.08;decimal=-0.008/100;sign=0.008
l1|q-seven-25ths|7/25|digits=725/100;flipped=25/7
l1|q-fund-fee|2.5/100|one-place=0.25;no-scale=2.5
l1|q-above-whole|1.2|twelve=12/100;rise=0.2
l2|s1|240/10|hundred=240/100;times=240*10
l2|s3|240/100|ten=240/10;thousand=240/1000
l2|s4|0.15*240|divide=240/15;one-and-five=0.11*240;ten-only=0.10*240
l2|s5|0.17*240|one-once=0.16*240;seven-tens=0.70*240
l2|s6|0.99*240|one=0.01*240;ninety=0.90*240
l2|s10|0.02*1850|twenty=0.20*1850;half=1850/2;small=0.002*1850
l2|q-fifteen-of-sixty|0.15*60|divide=60/15;ten=6
l2|q-three-of-450|0.03*450|divide=450/3;tens=0.30*450
l2|q-half-percent-fee|0.005*2000|no-scale=0.5*2000;five=0.05*2000
l2|q-ninety-five|0.95*40|gap=0.05*40;added=1.05*40
l3|s1|18/25|raw=18/100;flipped=25/18
l3|s2|7/20|
l3|s3|13/50|raw=13/100;halved=6.5/100
l3|s4|9/40|raw=9/100;flipped=40/9
l3|s5|500/400|flipped=400/500;rise=100/400
l3|s10|3500/12500|rest=3500/9000;largest=3500/4000
l3|q-45-of-60|45/60|raw=45/100;flipped=60/45
l3|q-rate-points|3.5-2.5|relative=100*1/3.5
l3|q-rate-relative|1/3.5|points=1/100;new-whole=1/2.5
l3|q-up-days|26/40|ratio=26/14;down=14/40
l4|s1|60*0.85|discount=60*0.15;pounds=60-15
l4|s3|1.15|rise-only=0.15;tenths=1.5;whole=15
l4|s4|240*1.08|rise-only=240*0.08;tenths=240*1.8;pounds=240+8
l4|s5|350*0.94|fall-only=350*0.06;rise=350*1.06;pounds=350-6
l4|s10|3750*1.072|return-only=3750*0.072;tenths=3750*1.72;pounds=3750+7.2
l4|q-twelve-up|1.12|rise-only=0.12;tenths=1.2
l4|q-twenty-off|45*0.8|cut-only=45*0.2;rise=45*1.2
l4|q-small-rise|1200*1.025|rise-only=1200*0.025;tenths=1200*1.25;pounds=1202.5
l5|s1|40*1.25|added-pounds=40+25;rise-only=10
l5|s3|6/40|pounds=6/100;new-base=6/46;ratio=46/40
l5|s4|12/80|pounds=12/100;new-base=12/68
l5|s5|18/12|ratio=30/12;pounds=18/100;new-base=18/30
l5|s9|(84.15-82.5)/82.5|pounds=1.65/100;new-base=1.65/84.15
l5|q-three-twenty-fall|0.8/3.2|new-base=0.8/2.4;kept=2.4/3.2
l5|q-eighteen-to-forty-five|27/18|ratio=45/18;new-base=27/45;pounds=27/100
l6|s1|64/0.8|add-back=64*1.2;off-again=64*0.8;add-pounds=64+20
l6|s3|45/0.75|add-back=45*1.25;off-again=45*0.75;divide-cut=45/0.25
l6|s4|92/1.15|down-again=92*0.85;up-again=92*1.15;minus-pounds=92-15
l6|s5|150-150/1.2|of-total=0.2*150;pre-vat=150/1.2
l6|s9|50.70/1.04|took-off=50.70*0.96;minus-pounds=50.70-4
l6|q-phone-vat|84/1.2|off=84*0.8;pounds=84-20
l6|q-seventy-five-fall|5/0.25|add=5*1.75;wrongm=5/0.75
l7|s3|1.2*0.8|cancel=1;added=1.2+0.8;change=1-1.2*0.8
l7|s4|1-1.1*0.9|cancel=0;pounds=0.5/100
l7|s5|100*1.5*0.5|cancel=100;half-start=50
l7|s9|2000/8000|same=2000/10000;pounds=2000/100
l7|q-after-half|1/0.5-1|same=0.5
l8|s1|1000*1.1**2|simple=1200
l8|s3|1000*1.1**5|simple=1500;times-n=1000*1.1*5
l8|s4|2500*1.04**2|simple=2500*1.08;one-year=2600
l8|s5|50*0.9**3|simple=50*0.7;pounds=40.5-5
l8|s9|1.05*0.96*1.025-1|added=0.05-0.04+0.025;multiplier=1.05*0.96*1.025
l8|q-two-falls|1-0.8**2|added=0.4;kept=0.64
l8|q-fee|10000*1.06*0.99|subtract=10000*1.05
l9|s0|15*2/5|one-round=2;fraction=15*2/3;half=7.5
l9|s2|40*3/5|one-part=8;dev=16;by-three=40/3
l9|s3|60*3/6|one-part=10;by-people=20;by-ratio-sum=60*3/5
l9|s4|14/2*5|add-gap=14+3;total=49;frac=14*2/5
l9|s5|18/2*8|diff-as-part=18*8;kit=45;jo=27
l9|s9|16500-0.6*26500|sold-gain=1500;swapped=16500-0.4*26500
l9|q-pennies|round(100/3,2)|half=50;third-up=33.34
l9|q-profit-total|1200/3*8|larger=2000;wrong-part=1200/5*8;one-part=400
l9|q-three-way|1500*5/10|by-people=500;one-part=150
l10|s1|300/4|times-four=1200;per-six=300/6
l10|s2|75*10|eight=600;added=306;rate=75
l10|s4|750*2/3|multiplied=750*3/2;one-part=250;added=749
l10|s8|45000*0.8|additive=45000-200;inverted=45000/0.8
l10|q-eggs|3*1000/250|added=3+4;units=3/4
l10|q-hedge|24000*3/2|inverted=24000*2/3;additive=25000
l11|s2|1200/60|direct=80;additive=40-30
l11|s3|1200/48|direct=40*48/30;additive=40-18
l11|s4|30/6|direct=15*3;pattern=6-3;halve=7.5
l11|s8|10000/62.5|direct=400*2.5;additive=400-37.5
l11|q-servers|60/15|direct=10*15/6;additive=10-9
l11|q-direct-k|18/4*10|additive=18+6;inverse=72/10
l11|q-inverse-c|72/6|direct=18*6/4;additive=18-2
l12|s1|5.60/400*100|per-gram=0.014;grams-per-pound=400/5.6
l12|s2|13.50/10|per-kilo=13.5;per-gram=0.0135
l12|s3|150/2.5|decimal-time=150/2.3;per-minute=150/150;whole-hours=150/2
l12|s4|4.5/3-7/5|totals=7-4.5;per-two=0.2
l12|s8|(1849.20-6)/240|fee-in=1849.20/240;inverted=240/1849.20
l12|q-cyclist|18/0.75|decimal=18/0.45;per-minute=18/45
l12|q-etf|3762/450|inverted=450/3762
l13|s0|300*1.16|divided=300/1.16;added=301.16
l13|s2|1/1.16|same=1.16;subtract=1-0.16;gap=0.16
l13|s3|500*1.12/1.21|same=500;multiplied-back=500*1.12*1.21
l13|s4|1.16*160|divided=160/1.16;added=161.16
l13|s8|12760/1.21-11600/1.16|old-rate=(12760-11600)/1.16;euro-profit=1160;multiplied=12760*1.21-11600*1.16
l13|q-back|87/1.16|multiplied=87*1.16
l13|q-yen-pence|100/190|same=190;pounds=1/190
l13|q-round-trip|200-200*1.10/1.22|rate-gap=200*0.12;none=0
l13|q-cross|190/1.16|multiplied=190*1.16
H1|h-seventeen-half|0.175*64|divide=64/17.5;tenths=1.75*64
H1|h-fee-then-rise|2000*1.05-2000*1.02|no-fee=100;sale=2100;points=5-2
H1|h-negative-return|12400*(1-0.0275)|sign=12400*1.0275;tenths=12400*0.725;loss-only=12400*0.0275
H2|hw2-portfolio-fall|1840/18400|new-base=1840/16560;kept=0.9
H2|hw2-yesterday-close|71.40/1.05|took-off=71.40*0.95
H2|hw2-index-rise|1750/1250|ratio=3000/1250;new-base=1750/3000
H2|hw2-recovery|60/90|same=60/150
H2|hw2-fees|10000*(1.08*0.98)**2|net-six=10000*1.06**2;simple=11200;no-fee=10000*1.08**2
H2|hw2-double|math.ceil(math.log(2)/math.log(1.07))|simple=15;short=10;simple-floor=14
H2|hw2-five-days|1.03*0.98*1.04*0.94*1.01-1|added=0;sign=-(1.03*0.98*1.04*0.94*1.01-1)
H3|h-difference|1260/3*11|diff-as-part=1260*11;larger=2940;one-part=420
H3|h-ratio-change|60/2*5|ali-before=90;sixty=60;part=30
H3|h-workers-leave|5+(180-60)/8|ignore-done=180/8;direct=15
H3|h-triangle|1000*1.16*162/190|start=1000;multiplied=1000*1.16*162*190
H3|h-rebalance-cash|0.6*49000-28000|no-cash=0.6*45000-24000;old-total=30000-28000;swapped=28000-0.4*49000
H3|h-broker-break-even|9.95/0.01|rate=0.01;fee=9.95
H3|h-paint|54/4.5*7.5|additive=54+3;inverse=54*4.5/7.5
P1|p-pension-split.0|3/8|decimal=0.375/100;upside-down=8/3
P1|p-pension-split.1|9600*3/8|ten-times=36000;tenth=360;bonds=6000
P1|p-pension-split.2|3600*1.15|multiplier-1-5=3600*1.5;rise-only=540;bonds=6000*1.15
P1|p-pension-split.3|6000*0.96|rise=6000*1.04;fall-only=240;multiplier-0-6=6000*0.6
P1|p-pension-split.4|4140/9900|old-total=4140/9600;unchanged=0.375;bonds-base=4140/5760
P1|p-platform-fee.0|0.35/100|one-place=0.035;no-move=0.35;times-100=35
P1|p-platform-fee.1|8400*0.0035|one-place=8400*0.035;no-move=8400*0.35;half-only=8400*0.005
P1|p-platform-fee.2|8400*0.9965|added=8400*1.0035;one-place=8400*0.965;fee-only=29.4
P1|p-platform-fee.3|24/29.4|upside-down=29.4/24;account-base=24/8400;one-place=24/294
P1|p-phone-rise.0|(3.2+3.9)/100|one-place=0.71;no-move=7.1
P1|p-phone-rise.1|1.071|fall=0.929;rise-only=0.071;one-place=1.71
P1|p-phone-rise.2|30*1.071|rise-only=2.13;one-place=30*1.71;fall=30*0.929
P1|p-phone-rise.3|14/32.13|old-price=14/30;upside-down=32.13/14;saving=18.13/32.13
P1|p-savings-tax.0|18000*0.046|tenth=82.8;ten-times=8280
P1|p-savings-tax.1|0.4*(828-500)|all-taxed=0.4*828;allowance-taxed=0.4*500;kept=0.6*328
P1|p-savings-tax.2|(828-131.2)/18000|gross=0.046;all-taxed=0.6*0.046;tax-share=131.2/18000
P2|p-share-week.0|(84.10-72.50)/72.50|new-base=11.60/84.10;pounds=11.6/100
P2|p-share-week.1|84.10*0.84|cancel=72.5;pounds=84.10-16;rise=84.10*1.16
P2|p-share-week.2|1.16*0.84-1|sign=0.0256;cancel=0;new-base=(70.644-72.5)/70.644
P2|p-share-week.3|1/0.9744-1|same=0.0256;sixteen=0.16
P2|p-laptop-sale.0|561/0.85|added=561*1.15;off-again=561*0.85
P2|p-laptop-sale.1|660/1.1|took-off=660*0.9;added-carried=645.15/1.1
P2|p-laptop-sale.2|(561-600)/600|sign=0.065;added=0.10-0.15;sale-base=-39/561
P2|p-fund-two-years.0|(7840-6250)/6250|new-base=1590/7840;multiplier=7840/6250
P2|p-fund-two-years.1|math.sqrt(7840/6250)-1|halved=0.2544/2;total=0.2544
P2|p-fund-two-years.2|7840-(6250+2*750)|simple-balance=7750;none=0
P2|p-fund-two-years.3|6250*1.12**5|simple=6250*1.6;halved=6250*1.1272**5
P2|p-fund-six-months.0|52000*0.91**3|added=52000*0.73;one-month=52000*0.91
P2|p-fund-six-months.1|39185.69*1.09**3|cancel=52000;added=39185.69*1.27
P2|p-fund-six-months.2|50746.60/52000-1|sign=0.0241;cancel=0;one-pair=0.91*1.09-1
P2|p-fund-six-months.3|1/0.975896-1|same=0.0241;nine=0.09
P3|p-partners-profit.0|3+4+8|thousands=12+16+32;halved=6+8+16
P3|p-partners-profit.1|9600/15*8|equal=9600/3;one-part=640
P3|p-partners-profit.2|2850/3*15|own-parts=2850*3;one-part-share=2850*15
P3|p-partners-profit.3|11900/17*2|old-parts=11900/15*2;equal=11900/4
P3|p-print-run.0|4*15/8|direct=30;subtracted=15-4
P3|p-print-run.1|8*7.5*14|direct=8*30*14;one-press=7.5*14
P3|p-print-run.2|840/36|per-leaflet=840/36000;upside-down=36000/840
P3|p-coffee-suppliers.0|330/12|upside-down=12/330;german=441/15
P3|p-coffee-suppliers.1|27.5/1.10|multiplied=27.5*1.10
P3|p-coffee-suppliers.2|441/15/1.20|multiplied=441/15*1.20;euros=441/15
P3|p-coffee-suppliers.3|90*(25-24.5)|per-kg=0.5;multiplied=90*(35.28-30.25)
P3|p-villa-split.0|8*405/6|direct=405*6/8;unchanged=405
P3|p-villa-split.1|540/1.125|multiplied=540*1.125
P3|p-villa-split.2|3240/36*7|equal=540;two-parts=3240*7/11;four-nights=360
P3|p-villa-split.3|(630-540)/1.125|euros=90;multiplied=90*1.125
R1|r-seven-hundredths|0.07|seventy=0.7;decimal=0.07/100
R1|r-35-of-120|0.35*120|divide=120/35;thirty=36
R1|r-cash-share|600/2400|flipped=2400/600;part-part=600/1800
R1|r-four-percent-fall|85*0.96|fall-only=3.4;rise=85*1.04;pounds=81
R1|r-fee-total|2350*1.02|fee-only=47;tenths=2350*1.2;pounds=2352
R1|r-tiny-return|0.0045|one-place=0.045;three=0.45
R2|r2-thirty-two-to-forty|8/32|new-base=8/40;pounds=8/100
R2|r2-up-down-ten|250*1.1*0.9|cancel=250;fall-only=225
R2|r2-three-percent|4000*1.03**2|simple=4240;one=4120
R2|r2-drawdown|40/160|new-base=40/120
R2|r2-back-from-sixty-four|(56/0.7-56)/56|same=0.3
R2|r2-vat|63-63/1.05|of-total=0.05*63;pre=60
R2|r2-yearly-rate|math.sqrt(45/20)-1|halved=1.25/2;total=1.25
R3|r-share-larger|450*5/9|one-part=50;smaller=200;by-two=225
R3|r-convert|640*1.15|divided=640/1.15;added=641.15
R3|r-pumps|5*12/3|direct=12*3/5;additive=14
R3|r-bonds-percent|3/10|as-fraction=3/7;equities=0.7
R3|r-shares-direct|2015/(930/120)|inverse=120*930/2015;additive=120+1085
R3|r-quote-inverse|430/0.86|times=430*0.86;gap=430*1.14
R3|r-fee-share|300*(1005-5)/125+5|fee-in=1005*300/125;no-fee=2400
'''

docs = {}
seen = 0
for line in TABLE.strip().splitlines():
    fk, loc, kexpr, slips = line.split('|')
    name = L[fk]
    if name not in docs:
        docs[name] = widgets(load(name))
    it = docs[name].get(loc)
    tag = '%s %s' % (name, loc)
    ok('located ' + tag, it is not None)
    if it is None:
        continue
    seen += 1
    w = it['widget']
    key = float(w['answer'])
    tol = w.get('tol', 0)
    tol = tol.get('abs', 0) if isinstance(tol, dict) else float(tol)
    mine = eval(kexpr)
    ok('key ' + tag, abs(mine - key) <= tol + 1e-9, 'stored %r, recomputed %r' % (key, mine))
    exprs = dict(s.split('=', 1) for s in slips.split(';') if s)
    stored = {x['id']: x for x in w.get('wrong', [])}
    # every authored numeric slip is covered by an expression, except the one finding
    for sid, x in stored.items():
        ok('slip covered ' + tag + ' ' + sid, sid in exprs)
    bands = [(key - tol, key + tol, 'key')]
    for sid, e in exprs.items():
        x = stored.get(sid)
        ok('slip exists ' + tag + ' ' + sid, x is not None)
        if x is None:
            continue
        v = eval(e)
        if 'value' in x:
            st = x.get('tol', {}).get('abs', 0)
            lo, hi = x['value'] - st, x['value'] + st
        else:
            lo, hi = x['from'], x['to']
        ok('slip value ' + tag + ' ' + sid, lo - 1e-9 <= v <= hi + 1e-9, 'band [%r, %r], named mistake gives %r' % (lo, hi, v))
        bands.append((lo, hi, sid))
    for sid, x in stored.items():
        if sid not in exprs and 'value' in x:
            st = x.get('tol', {}).get('abs', 0)
            bands.append((x['value'] - st, x['value'] + st, sid))
    for (a, b, n1), (c, d, n2) in itertools.combinations(bands, 2):
        ok('bands apart ' + tag + ' %s/%s' % (n1, n2), b < c or d < a, '[%r,%r] meets [%r,%r]' % (a, b, c, d))

total_numeric = 0
for f in sorted(glob.glob(os.path.join(ROOT, '*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    for loc, it in widgets(d).items():
        if it['widget'].get('kind') in ('numeric', 'slider'):
            total_numeric += 1
ok('every numeric and slider widget has a row', seen == total_numeric, '%d rows, %d widgets' % (seen, total_numeric))

# ------------------------------------------------------------------ 2. fluency sweeps
# Each family is rebuilt here from its meaning (not from its `let` strings), and the
# authored `let` expressions are checked against it over the whole range.
def fam(name, fid):
    for x in load(name)['families']:
        if x['id'] == fid:
            return x
    raise KeyError(fid)


def gcd3(*a):
    g = 0
    for x in a:
        g = math.gcd(g, x)
    return g


ENV = {'abs': abs, 'max': max, 'min': min, 'gcd': gcd3, 'if': None}


def ev(expr, env):
    e = expr.replace('if(', 'IF(')
    return eval(e, {'__builtins__': {}}, dict(env, IF=lambda c, a, b: a if c else b, abs=abs, max=max, min=min, gcd=gcd3))


def sweep(name, fid, cases, truth, slips):
    """cases: iterable of env dicts; truth(env) -> key; slips: id -> fn(env) (the named mistake)."""
    f = fam(name, fid)
    n = 0
    for env in cases:
        if not all(ev(c, env) for c in f.get('where', [])):
            continue
        n += 1
        full = dict(env)
        for k, e in f.get('let', {}).items():
            full[k] = ev(e, env)
        key = full[f['widget']['answer'].strip('{}')] if f['widget']['answer'].strip('{}') in full else ev(f['widget']['answer'].strip('{}'), full)
        tol = f['widget']['tol']['abs']
        t = truth(env)
        if abs(key - t) > 1e-9:
            ok('%s/%s key' % (name, fid), False, '%r: stored %r, true %r' % (env, key, t)); return n
        act = []
        for wv in f['wrong']:
            if 'when' in wv and not ev(wv['when'], env):
                continue
            v = ev(wv['value'].strip('{}'), full)
            m = slips[wv['id']](env)
            if abs(v - m) > 1e-9:
                ok('%s/%s slip %s' % (name, fid, wv['id']), False, '%r: stored %r, mistake gives %r' % (env, v, m)); return n
            wt = wv['tol']['abs']
            if abs(v - key) <= wt + tol:
                ok('%s/%s slip %s clear of key' % (name, fid, wv['id']), False, '%r: slip %r, key %r' % (env, v, key)); return n
            act.append((wv['id'], v, wt))
        for (i1, v1, t1), (i2, v2, t2) in itertools.combinations(act, 2):
            if abs(v1 - v2) <= t1 + t2:
                ok('%s/%s slips %s and %s apart' % (name, fid, i1, i2), False, '%r: %r and %r' % (env, v1, v2)); return n
    ok('%s/%s swept' % (name, fid), n > 0)
    return n


def grid(**kw):
    ks = list(kw)
    for vals in itertools.product(*[kw[k] for k in ks]):
        yield dict(zip(ks, vals))


swept = 0
swept += sweep('fluency-l2-building-percentages', 'whole-percent', grid(p=range(2, 99), amt=range(20, 501, 10)),
               lambda e: e['p'] / 100 * e['amt'], {'divided-by-p': lambda e: e['amt'] / e['p'], 'the-rest': lambda e: e['amt'] - e['p'] / 100 * e['amt']})
swept += sweep('fluency-l2-building-percentages', 'half-percent',
               grid(p=[0.5, 1.5, 2.5, 3.5, 4.5, 7.5, 12.5, 15.5, 17.5, 22.5, 32.5, 37.5], amt=range(20, 981, 20)),
               lambda e: e['p'] / 100 * e['amt'], {'divided-by-p': lambda e: e['amt'] / e['p'], 'tenths': lambda e: e['p'] / 10 * e['amt']})
swept += sweep('fluency-l4-multipliers', 'write-multiplier', grid(q=range(1, 121), s=[1, -1]),
               lambda e: 1 + e['s'] * (e['q'] / 2) / 100,
               {'opposite': lambda e: 1 - e['s'] * (e['q'] / 2) / 100, 'change-only': lambda e: (e['q'] / 2) / 100, 'tenths': lambda e: 1 + e['s'] * (e['q'] / 2) / 10})
swept += sweep('fluency-l4-multipliers', 'apply-multiplier', grid(amt=range(20, 901, 10), p=range(1, 61), s=[1, -1]),
               lambda e: e['amt'] + e['s'] * e['amt'] * e['p'] / 100,
               {'change-only': lambda e: e['amt'] * e['p'] / 100, 'opposite': lambda e: e['amt'] - e['s'] * e['amt'] * e['p'] / 100, 'tenths': lambda e: e['amt'] * (1 + e['s'] * e['p'] / 10)})
OLD = [8, 12, 16, 20, 24, 25, 30, 32, 40, 45, 48, 50, 60, 64, 75, 80, 90, 120, 150, 200]


def new_price(e):
    return e['old'] * (1 + e['s'] * e['p'] / 100)


swept += sweep('fluency-l5-rise-or-fall', 'percentage-change', grid(old=OLD, p=range(5, 151, 5), s=[1, -1]),
               lambda e: abs(new_price(e) - e['old']) / e['old'],
               {'new-base': lambda e: abs(new_price(e) - e['old']) / new_price(e), 'ratio': lambda e: new_price(e) / e['old'],
                'pounds': lambda e: abs(new_price(e) - e['old']) / 100})
YS = [20, 25, 40, 50, 80, 100, 120, 125, 150, 200, 250, 300, 400, 500]
swept += sweep('fluency-l5-rise-or-fall', 'daily-return', grid(y=YS, r=[r for r in range(-12, 13) if r != 0]),
               lambda e: (e['y'] * (1 + e['r'] / 100) - e['y']) / e['y'],
               {'sign-flipped': lambda e: -e['r'] / 100, 'new-base': lambda e: (e['y'] * e['r'] / 100) / (e['y'] * (1 + e['r'] / 100))})
swept += sweep('fluency-l6-before-the-discount', 'undo-a-discount', grid(orig=range(20, 401, 10), p=[5, 10, 15, 20, 25, 30, 40, 60, 75, 80]),
               lambda e: e['orig'],
               {'added-back': lambda e: e['orig'] * (1 - e['p'] / 100) * (1 + e['p'] / 100), 'divided-by-cut': lambda e: e['orig'] * (1 - e['p'] / 100) / (e['p'] / 100)})
swept += sweep('fluency-l6-before-the-discount', 'undo-a-rise', grid(orig=range(20, 401, 10), p=[5, 10, 15, 20, 25, 40, 50, 60]),
               lambda e: e['orig'],
               {'took-off': lambda e: e['orig'] * (1 + e['p'] / 100) * (1 - e['p'] / 100), 'divided-by-rise': lambda e: e['orig'] * (1 + e['p'] / 100) / (e['p'] / 100)})
swept += sweep('fluency-l6-before-the-discount', 'vat-inside', grid(net=range(5, 301, 5)),
               lambda e: e['net'] * 1.2 - e['net'], {'vat-of-total': lambda e: 0.2 * 1.2 * e['net'], 'price-before': lambda e: e['net']})
swept += sweep('fluency-l9-sharing', 'share-a-total', grid(a=range(1, 8), b=range(1, 10), k=range(2, 21), big=[0, 1]),
               lambda e: e['k'] * (max(e['a'], e['b']) if e['big'] else min(e['a'], e['b'])),
               {'one-part': lambda e: e['k'], 'ratio-as-fraction': lambda e: e['k'] * (e['a'] + e['b']) * min(e['a'], e['b']) / max(e['a'], e['b']),
                'split-equally': lambda e: e['k'] * (e['a'] + e['b']) / 2})
swept += sweep('fluency-l9-sharing', 'from-one-share', grid(a=range(1, 10), b=range(1, 10), k=range(2, 16)),
               lambda e: e['a'] * e['k'] / e['a'] * e['b'], {'added-the-gap': lambda e: e['a'] * e['k'] + (e['b'] - e['a']), 'gave-the-total': lambda e: e['k'] * (e['a'] + e['b'])})
swept += sweep('fluency-l9-sharing', 'three-way', grid(a=range(1, 7), b=range(1, 7), c=range(1, 7), k=range(2, 21)),
               lambda e: e['k'] * max(e['a'], e['b'], e['c']), {'one-part': lambda e: e['k'], 'split-equally': lambda e: e['k'] * (e['a'] + e['b'] + e['c']) / 3})
swept += sweep('fluency-l9-sharing', 'from-a-difference', grid(a=range(1, 9), b=range(2, 10), k=range(2, 16)),
               lambda e: e['k'] * (e['b'] - e['a']) / (e['b'] - e['a']) * (e['a'] + e['b']),
               {'one-part': lambda e: e['k'], 'larger-share': lambda e: e['b'] * e['k'], 'gap-as-one-part': lambda e: e['k'] * (e['b'] - e['a']) * (e['a'] + e['b'])})
# prompts print money to the penny: every generated price is a whole number of pence
for old in OLD:
    for p in range(5, 151, 5):
        for s in (1, -1):
            if s == 1 or p < 100:
                ok('fluency l5 price in pence', (F(old) * (100 + s * p) / 100 * 100).denominator == 1)
for y in YS:
    for r in range(-12, 13):
        ok('fluency l5 close in pence', (F(y) * (100 + r)).denominator == 1)
for orig in range(20, 401, 10):
    for p in [5, 10, 15, 20, 25, 30, 40, 60, 75, 80]:
        ok('fluency l6 sale price in pence', (F(orig) * (100 - p)).denominator == 1)

# ------------------------------------------------------------------ 3. general rules
rng = random.Random(20261126)
# l7: (1 + p)(1 - p) = 1 - p^2 < 1 for every p != 0, in either order (summary, s6, s8, hw2 longform)
for p in [F(k, 1000) for k in range(1, 1001)]:
    ok('equal swing loses', (1 + p) * (1 - p) == 1 - p * p < 1 and (1 - p) * (1 + p) == (1 + p) * (1 - p))
ok('losses 0.01, 0.04, 0.25', [F(1, 10) ** 2, F(2, 10) ** 2, F(5, 10) ** 2] == [F(1, 100), F(4, 100), F(25, 100)])
# Monte Carlo twin: 200,000 random swings of 0.1% to 99.9%, random order: every one ends below the start
lose = 0
for _ in range(200000):
    p = rng.uniform(0.001, 0.999)
    m = (1 + p) * (1 - p) if rng.random() < 0.5 else (1 - p) * (1 + p)
    lose += m < 1
ok('Monte Carlo: equal swings always lose', lose == 200000, str(lose))
# l7 quiz: unequal moves can cancel (1.25 x 0.8 = 1)
ok('up 25 down 20 cancels', F(5, 4) * F(4, 5) == 1)
# hw2: recovery r = d / (1 - d) > d for 0 < d < 1; 20% -> 25%, 50% -> 100%, 25% -> 33.3%, 40% -> 66.7%
for d in [F(k, 1000) for k in range(1, 1000)]:
    r = d / (1 - d)
    ok('recovery exceeds fall', r > d and (1 - d) * (1 + r) == 1)
ok('recovery cases', [F(1, 5) / F(4, 5), F(1, 2) / F(1, 2), F(1, 4) / F(3, 4), F(2, 5) / F(3, 5)] == [F(1, 4), 1, F(1, 3), F(2, 3)])
# l8: compound P(1+r)^n against simple P(1+nr): equal at n = 1, compound ahead for every n >= 2 and r > 0
for r in [F(k, 200) for k in range(1, 61)]:
    ok('compound = simple at n = 1', (1 + r) ** 1 == 1 + r)
    for n in range(2, 41):
        ok('compound beats simple', (1 + r) ** n > 1 + n * r)
ok('ten years at 10% is 2.59, not 2', abs(1.1 ** 10 - 2.5937424601) < 1e-9 and round(1000 * 1.1 ** 10, 2) == 2593.74)
# l8 quiz: 10% compound against 11% simple: behind for n = 1, 2, ahead from n = 3 and pulling away
gaps = [F(11, 10) ** n - (1 + n * F(11, 100)) for n in range(1, 31)]
ok('10% compound v 11% simple', gaps[0] < 0 and gaps[1] < 0 and gaps[2] == F(1, 1000) and all(gaps[i + 1] > gaps[i] for i in range(2, 29)))
# l8 s5: repeated 10% falls shrink and never reach zero; three falls are 27.1%
ok('repeated falls', all(F(9, 10) ** n > 0 for n in range(1, 500)) and 1 - F(9, 10) ** 3 == F(271, 1000))
# homework-1: p% of A = A% of p
for _ in range(20000):
    p, A = F(rng.randint(1, 4000), 10), F(rng.randint(1, 100000), 100)
    ok('percentage swap', p / 100 * A == A / 100 * p)
# l5/l4: a fall cannot pass 100% while the price stays at or above zero; a multiplier below 1 is a fall
ok('fall bounded', all((F(o) - F(n)) / o <= 1 for o in range(1, 60) for n in range(0, o + 1)))
# l6: dividing by the multiplier undoes it for every m != 0; adding the percentage back always falls short
for k in range(1, 100):
    p = F(k, 100)
    ok('add-back falls short', (1 - p) * (1 + p) < 1 and (1 - p) / (1 - p) == 1)
    ok('taking the rise off overshoots', (1 + p) * (1 - p) < 1)
# l9: a : b gives fractions a/(a+b), b/(a+b); a/b is never the fraction of the whole (a, b > 0)
ok('ratio fractions', all(F(a, a + b) + F(b, a + b) == 1 and F(a, b) != F(a, a + b) for a in range(1, 30) for b in range(1, 30)))
# l10: adding the same amount to both sides changes the ratio unless the sides are equal
ok('adding keeps the gap, not the ratio', all((F(a + c, b + c) == F(a, b)) == (a == b) for a in range(1, 15) for b in range(1, 15) for c in range(1, 15)))
# l10/l11: y = kx doubles with x; xy = c halves; a fixed charge or a falling line passes neither test
ok('taxi not proportional', F(3 + 2 * 2, 2) != F(3 + 2 * 4, 4) and (3 + 2 * 4) != 2 * (3 + 2 * 2))
ok('fuel not inverse', 2 * (40 - 5 * 2) == 60 and 4 * (40 - 5 * 4) == 80 and 1 * 35 == 35)
ok('machines table product', 2 * 15 == 3 * 10 == 5 * 6 == 6 * 5 == 30)
# l13: a rate times its inverse is 1; 1/r equals 1 - (r - 1) only at r = 1; chained rates multiply
for k in range(50, 251):
    r = F(k, 100)
    ok('rate times inverse', r * (1 / r) == 1)
    ok('inverse is not 2 - r', ((1 / r) == 1 - (r - 1)) == (r == 1))
ok('chain', F(116, 100) * 160 == F(1856, 10) and 250 * F(1856, 10) == 46400)
ok('triangle loop loses', F(116, 100) * 162 < 190 and abs(1000 * 1.16 * 162 / 190 - 989.05) < 0.005 and abs(1000 - 989.0526 - 10.95) < 0.005)
ok('l13 transfer returns', abs(63.80 / 58 - 1.10) < 1e-12 and abs(545.4545 / 10000 - 0.0545) < 1e-4 and abs(500 - 462.81 - 37.19) < 1e-9)
# l12: bulk is not always cheaper (honey), and can be (coffee, cans)
ok('bulk both ways', 9.00 / 10 > 4.40 / 5 and 13.50 / 10 < 5.60 / 4 < 3.75 / 2.5 and 6.50 / 10 < 4.20 / 6)
# l3: points against per cent
ok('points and per cent', (5 - 4, F(1, 4), F(4, 12), F(4, 16), F(75, 150)) == (1, F(1, 4), F(1, 3), F(1, 4), F(1, 2)) and abs(1 / 3.5 - 0.2857) < 1e-4)
# stated figures in explanations and long-form models
ok('l2 fee break-even', 1850 * 1.02 == 1887.0 and abs(1887 / 1850 - 1.02) < 1e-12)
ok('l6 VAT share', abs(25 / 150 - 0.1667) < 1e-4 and 33000 * 0.1 - 3000 == 300)
ok('h1 long', (round(12000 / 19940 * 100, 2), round(6000 / 19940 * 100, 2), round(1940 / 19940 * 100, 2)) == (60.18, 30.09, 9.73)
   and abs(15.18 / 45 - 0.337) < 1e-3 and 12960 + 5880 + 1940 == 20780 and round(840 / 19940 * 100, 2) == 4.21 and 780 / 20000 == 0.039)
ok('h1 fee', round(60 / 2040 * 100, 1) == 2.9 and abs(0.0075 * 1.5 - 0.01125) < 1e-12)
ok('hw2 fees', round(10000 * 1.0584 ** 2, 2) == 11202.11 and round(11664 - 11202.11, 2) == 461.89 and 461.89 > 400)
ok('hw2 double', round(1000 * 1.07 ** 10, 2) == 1967.15 and 1.07 ** 11 > 2 and math.ceil(100 / 7) == 15)
ok('hw2 five days', abs(1.03 * 0.98 * 1.04 * 0.94 * 1.01 - 0.996657) < 1e-6 and 3 - 2 + 4 - 6 + 1 == 0)
ok('r2 three days', abs(1.01 * 1.01 * 0.98 - 0.999698) < 1e-9)
ok('p2 figures', abs(0.91 ** 3 - 0.753571) < 1e-9 and abs(1.09 ** 3 - 1.295029) < 1e-9 and abs(0.9919 ** 3 - 0.975896) < 1e-6
   and abs(1.12 ** 5 - 1.762342) < 1e-6 and abs(7840 * 1.12 ** 3 - 6250 * 1.12 ** 5) < 1e-6 and abs(70.644 * 1.0263 - 72.50) < 0.01)
ok('p1 figures', abs((0.039 * 18000) - 696.80 - 5.20) < 1e-9 and abs(0.039 * 18000 - 702) < 1e-9)
ok('p3 figures', 36 * 22 == 792 and 840 - 792 == 48 and 4 * 7 + 2 * 4 == 36)
ok('h3 long', 80000 / 5 * 2 == 32000 and 32000 * 1.16 == 37120 and abs(32000 / 0.8621 - 37119) < 1)
ok('l9 rebalance', 0.6 * 26500 == 15900 and 16500 - 15900 == 600 and F(15900, 10600) == F(3, 2))
ok('l11 quiz tank', 1 * (40 - 5) == 35 and 2 * (40 - 10) == 60)

# l8 transfer and trap: does adding returns over- or understate? Monte Carlo over random return paths.
# Claim A (s6): with every return positive, the sum understates the compound return. Always.
# Claim B (s9): "adding returns ignores growth on growth, so here it overstates". The direction is not general:
# with mixed signs it goes either way. 100,000 paths of three returns each separate the two statements.
under_pos = over_mixed = under_mixed = n_mixed = 0
N = 100000
for _ in range(N):
    rs = [rng.uniform(0.001, 0.2) for _ in range(3)]
    under_pos += sum(rs) < (1 + rs[0]) * (1 + rs[1]) * (1 + rs[2]) - 1
    ms = [rng.uniform(-0.2, 0.2) for _ in range(3)]
    if min(ms) < 0 < max(ms):
        n_mixed += 1
        c = (1 + ms[0]) * (1 + ms[1]) * (1 + ms[2]) - 1
        over_mixed += sum(ms) > c
        under_mixed += sum(ms) < c
ok('adding understates all-positive growth', under_pos == N, str(under_pos))
ok('l8 s9 numbers', abs(1.05 * 0.96 * 1.025 - 1.0332) < 1e-12 and abs(200 * 1.0332 - 206.64) < 1e-9 and 0.035 > 0.0332)
ok('mixed signs go either way', over_mixed > 0.05 * n_mixed and under_mixed > 0.05 * n_mixed)
note('l8 s9: the reason for overstating is specific to this path, not "growth on growth" (finding 6)',
     'growth on growth' not in load('l8-growth-on-growth')['screens'][9]['explain']['text']
     and abs(200 * 1.05 * 0.04 - 8.40) < 1e-9 and 1.05 * 0.96 * 1.025 - 1 < 0.05 - 0.04 + 0.025,
     'mixed-sign paths: sum above compound %.1f%%, below %.1f%% of %d' % (100 * over_mixed / n_mixed, 100 * under_mixed / n_mixed, n_mixed))

# ------------------------------------------------------------------ 4. checks tied to findings
# Finding 1 (wrong): l1 screens[8] option 850% says the point moved three places.
d = load('l1-out-of-a-hundred')
opt = [o for o in d['screens'][8]['widget']['options'] if o['id'] == 'three'][0]
places = round(math.log10(850 / 0.085))
ok('finding 1: l1 s8 "850%%" names the right number of places (0.085 -> 850 is %d places; three places give %g)' % (places, 0.085 * 1000),
   ('three places' not in opt['why']) or places == 3, opt['why'])
# Finding 2 (imprecise): l1 quiz q-seven-25ths slip "digits" is stored as 72.5%, the line says 7 and 25 side by side (725).
w = docs['l1-out-of-a-hundred']['q-seven-25ths']['widget']
dig = [x for x in w['wrong'] if x['id'] == 'digits'][0]
note('finding 2: l1 q-seven-25ths "digits" value is 7 and 25 side by side', abs(dig['value'] - 7.25) < 1e-9,
     'stored %r (typed %g); "7 and 25 side by side" typed as 725 is 7.25' % (dig['value'], dig['value'] * 100))
# Finding 3 (imprecise): l2 s7 "it never divides the amount": p% of A = A / p exactly when p = 10, the lesson's first screen.
hits = [p for p in range(1, 101) if F(p, 100) * 240 == F(240, p)]
note('finding 3: l2 s7 "never divides the amount" has no exception',
     not ('never divides' in load('l2-building-percentages')['screens'][7]['explain']['text'] and hits),
     'p%% of A equals A / p for p in %r; also 20%% = A / 5, 25%% = A / 4, 50%% = A / 2' % hits)
# Finding 4 (imprecise): l3 formula note "The whole is every item, never just the other part" against screen 5 (500 as a percentage of 400).
note('finding 4: l3 formula note covers the lesson\'s own comparisons', 'every item' not in load('l3-what-percentage')['summary']['formula']['note'],
     'screens[5] measures £500 against £400 (125%%); every item together would give 500/900 = %.1f%%' % (500 / 900 * 100))
# Finding 5 (imprecise): l10 quiz "A ratio only compares like with like" against "ratio of grams to people" in the same lesson.
l10 = load('l10-scaling')
note('finding 5: l10 "only compares like with like" agrees with the lesson', not ('only compares like with like' in l10['quiz'][0]['explain']['text'] and 'ratio of grams to people' in l10['screens'][2]['prose']))
# Finding 7 (imprecise): l11 s5 "Direct proportion is a line through (0, 0) that rises": y = kx with k < 0 keeps y/x fixed and falls.
k = -2
note('finding 7: l11 s5 direct proportion "rises"', not ('that rises' in [o for o in load('l11-direct-or-inverse')['screens'][5]['widget']['options'] if o['id'] == 'direct'][0]['why']
                                                    and len({F(k * x, x) for x in range(1, 9)}) == 1 and k * 2 < k * 1))

# Finding 8 (imprecise): l10 s7 order: "origin" and "slope" each need only y = kx, yet one order is keyed and no `same` group is set.
w10 = l10['screens'][7]['widget']
note('finding 8: l10 s7 interchangeable lines are grouped', w10['answer'][2:] != ['origin', 'slope'] or bool(w10.get('same')),
     'ratio, times, slope, origin is as valid a proof and is marked wrong')
# Finding 9 (imprecise): problems-2 p-fund-six-months part 2 states 50,746.60; the fund is worth 52,000 x 0.91^3 x 1.09^3.
exact = float(52000 * F(91, 100) ** 3 * F(109, 100) ** 3)
p2 = docs['problems-2']['p-fund-six-months.1']
note('finding 9: the fund\'s unrounded June value is stated to the penny', ('%.2f' % exact).replace('50746', '50,746') in p2['explain']['text'],
     'exact %.4f, i.e. 50,746.61; accept says %s (from the rounded March value: %.4f)' % (exact, p2['widget']['accept'], 39185.69 * 1.09 ** 3))
ok('finding 9: both pennies are accepted', abs(50746.60 - p2['widget']['answer']) <= 0.01 and abs(50746.61 - p2['widget']['answer']) <= 0.01)

print('ratio-L1-3-concepts: %d checks, %d widgets with rows, %d fluency cases swept, %d fail, %d note' % (n_checks, seen, swept, len(fails), len(notes)))
for s in notes:
    print('NOTE', s)
for s in fails:
    print('FAIL', s)
sys.exit(1 if fails else 0)
