"""Recompute every Fluency answer and every named slip in the ratio sets from the drawn variable values alone.

Method 1 is the engine's own arithmetic (the set's `let` expressions, resolved by tools/fluency-sample.mjs --json).
Method 2 is this script: exact fractions (Python's Fraction) work each answer out again from the vars, by the
lesson's own method (1% first, the multiplier, change over original, divide by the multiplier, count the parts),
and rebuild each slip from what the learner would have done. For every draw it checks
  - the prompt states the amounts the vars describe, with money to two decimal places where the lesson does;
  - the engine's key equals the key worked out here, and the money key is a whole number of pence;
  - the slips offered are exactly those whose condition holds here, each equal to the slip worked out here,
    each outside the key's tolerance (allowing its own) and apart from the other slips.
Run:  <scratchpad>/venv/bin/python docs/reports/fluency-ratio-numbers.py   (exit 0 = pass; FLUENCY_N sets draws)
"""
import json, os, subprocess, sys
from fractions import Fraction as F
from math import gcd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

APP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app')
N = int(os.environ.get('FLUENCY_N', '200'))
lv = Level("ratio", 1)
count = 0


def check(ok, label):
    global count
    count += 1
    lv.claim(bool(ok), label)


def draws(ref, fam):
    out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', ref, '--family', fam, '--n', str(N), '--json'],
                         cwd=APP, capture_output=True, text=True, check=True).stdout
    return json.loads(out)['items']


def q(x):
    return F(x).limit_denominator(10 ** 9) if isinstance(x, float) else F(x)


def money(x):
    """Pounds to two decimal places, as the prompt writes them."""
    x = q(x)
    pence = x * 100
    check(pence.denominator == 1, f"amount {float(x)} is a whole number of pence")
    return f"{int(pence) // 100}.{int(pence) % 100:02d}"


def pct(x):
    """A percentage figure as the prompt writes it: 12, 0.5, 17.5."""
    x = q(x)
    return str(x.numerator) if x.denominator == 1 else f"{float(x):g}"


def item(it, prompt, key, slips, money_key=True):
    tag = f"{it['family']} seed {it['seed']}"
    check(it['prompt'] == prompt, f"{tag}: prompt {it['prompt']!r} is {prompt!r}")
    got = q(it['answer'])
    check(got == key, f"{tag}: key {it['answer']} equals {key}")
    if money_key:
        check((key * 100).denominator == 1, f"{tag}: key {float(key)} is a whole number of pence")
    tol = q((it.get('tol') or {}).get('abs', 0))
    ids = [w['id'] for w in it['wrong']]
    check(sorted(ids) == sorted(slips), f"{tag}: slips offered {ids} are {sorted(slips)}")
    vals = {}
    for w in it['wrong']:
        v = q(float(w['value']))
        wt = q((w.get('tol') or {}).get('abs', 0))
        vals[w['id']] = (v, wt)
        if w['id'] in slips:
            check(abs(v - slips[w['id']]) <= F(1, 10 ** 6), f"{tag}: slip {w['id']} = {float(v)} is {float(slips[w['id']])}")
        check(abs(v - key) > tol + wt, f"{tag}: slip {w['id']} lies outside the key's tolerance")
    vs = list(vals.items())
    for i in range(len(vs)):
        for j in range(i + 1, len(vs)):
            check(abs(vs[i][1][0] - vs[j][1][0]) > vs[i][1][1] + vs[j][1][1], f"{tag}: slips {vs[i][0]} and {vs[j][0]} apart")


def run(ref, fam, fn):
    for it in draws(ref, fam):
        V = {k: (q(x) if not isinstance(x, str) else x) for k, x in it['vars'].items()}
        fn(it, V)


# ---- l2-building-percentages: build from 1% --------------------------------------------------------
def l2_whole(it, V):
    p, amt = V['p'], V['amt']
    one = amt / 100
    key = p * one
    check(key == amt * p / 100, f"whole seed {it['seed']}: p lots of 1% is p% of the amount")
    slips = {'the-rest': amt - key}
    if abs(amt / p - key) > F(2, 100):
        slips['divided-by-p'] = amt / p
    item(it, f"What is {pct(p)}% of £{int(amt)}?", key, slips)


def l2_half(it, V):
    p, amt = V['p'], V['amt']
    check(p.denominator == 2, f"half seed {it['seed']}: the percentage has a half in it")
    key = (amt / 100) * p
    slips = {'tenths': amt * p / 10}
    if abs(amt / p - key) > F(2, 100):
        slips['divided-by-p'] = amt / p
    item(it, f"What is {pct(p)}% of £{int(amt)}?", key, slips)


# ---- l4-multipliers ----------------------------------------------------------------------------------
def l4_write(it, V):
    p = V['q'] / 2
    s = int(V['s'])
    key = 1 + s * p / 100
    check(F(100) * key == 100 + s * p, f"write seed {it['seed']}: the multiplier is the whole plus or minus the change")
    slips = {'opposite': 1 - s * p / 100}
    if p != 50:
        slips['change-only'] = p / 100
    if p < 10:
        slips['tenths'] = 1 + s * p / 10
    item(it, f"What multiplier {V['verb']} an amount by {pct(p)}%?", key, slips, money_key=False)


def l4_apply(it, V):
    amt, p, s = V['amt'], V['p'], int(V['s'])
    two_step = amt + s * amt * p / 100
    key = amt * (1 + s * p / 100)
    check(key == two_step, f"apply seed {it['seed']}: one multiplication equals the two-step change")
    slips = {'change-only': amt * p / 100, 'opposite': amt * (1 - s * p / 100)}
    if p < 10:
        slips['tenths'] = amt * (1 + s * p / 10)
    item(it, f"{V['verb']} £{money(amt)} by {int(p)}%, using one multiplication.", key, slips)


# ---- l5-rise-or-fall: change over original -----------------------------------------------------------
def l5_change(it, V):
    old, p, s = V['old'], V['p'], int(V['s'])
    new = old * (1 + s * p / 100)
    change = abs(new - old)
    key = change / old
    check(key == p / 100, f"change seed {it['seed']}: change over original is p%")
    slips = {'new-base': change / new}
    if s == 1 or p != 50:
        slips['ratio'] = new / old
    pounds = change / 100
    if all(abs(pounds - x) > F(2, 1000) for x in (key, new / old, change / new)):
        slips['pounds'] = pounds
    item(it, f"A share {V['verb']} from £{money(old)} to £{money(new)}. By what percentage did it {V['noun']}?", key, slips, money_key=False)


def l5_return(it, V):
    y, r = V['y'], V['r']
    t = y * (1 + r / 100)
    key = (t - y) / y
    slips = {'sign-flipped': -key}
    if abs(key - (t - y) / t) > F(1, 1000):
        slips['new-base'] = (t - y) / t
    item(it, f"A stock closes at £{money(y)} on Monday and at £{money(t)} on Tuesday. What is its daily return?", key, slips, money_key=False)


# ---- l6-before-the-discount: divide by the multiplier ------------------------------------------------
def l6_discount(it, V):
    orig, p = V['orig'], V['p']
    sale = orig * (1 - p / 100)
    key = sale / (1 - p / 100)
    check(key == orig, f"discount seed {it['seed']}: dividing by the multiplier gives the original")
    item(it, f"A {V['item']} costs £{money(sale)} after {int(p)}% off. What was its price before the discount?", key,
         {'added-back': sale * (1 + p / 100), 'divided-by-cut': sale / (p / 100)})


def l6_rise(it, V):
    orig, p = V['orig'], V['p']
    after = orig * (1 + p / 100)
    key = after / (1 + p / 100)
    item(it, f"After a {int(p)}% rise, a share is at £{money(after)}. What was its price before the rise?", key,
         {'took-off': after * (1 - p / 100), 'divided-by-rise': after / (p / 100)})


def l6_vat(it, V):
    net = V['net']
    gross = net * F(6, 5)
    key = gross - gross / F(6, 5)
    check(key == gross / 6, f"vat seed {it['seed']}: VAT is one sixth of the price with VAT")
    item(it, f"A {V['item']} costs £{money(gross)} including VAT at 20%. How much of that is VAT?", key,
         {'vat-of-total': gross / 5, 'price-before': net})


# ---- l9-sharing: count the parts, find one part --------------------------------------------------------
def l9_total(it, V):
    a, b, k, big = int(V['a']), int(V['b']), V['k'], int(V['big'])
    T = k * (a + b)
    one = T / (a + b)
    xp = max(a, b) if big else min(a, b)
    key = one * xp
    check(V['w'] == ('larger' if big else 'smaller'), f"total seed {it['seed']}: the word matches the share")
    slips = {'split-equally': T / 2}
    if xp > 1:
        slips['one-part'] = one
    if not big and 2 * min(a, b) != max(a, b):
        slips['ratio-as-fraction'] = T * F(min(a, b), max(a, b))
    item(it, f"Share £{int(T)} in the ratio {a} : {b}. How much is the {V['w']} share?", key, slips)


def l9_one(it, V):
    a, b, k = int(V['a']), int(V['b']), V['k']
    first = a * k
    one = first / a
    slips = {'gave-the-total': one * (a + b)}
    if b > a:
        slips['added-the-gap'] = first + b - a
    item(it, f"Money is shared in the ratio {a} : {b}, and the first share is £{int(first)}. How much is the second share?", one * b, slips)


def l9_three(it, V):
    a, b, c, k = int(V['a']), int(V['b']), int(V['c']), V['k']
    check(len({a, b, c}) == 3 and gcd(gcd(a, b), c) == 1, f"three seed {it['seed']}: distinct parts in lowest terms")
    T = k * (a + b + c)
    one = T / (a + b + c)
    item(it, f"Share £{int(T)} in the ratio {a} : {b} : {c}. How much is the largest share?", one * max(a, b, c),
         {'one-part': one, 'split-equally': T / 3})


def l9_diff(it, V):
    a, b, k = int(V['a']), int(V['b']), V['k']
    d = k * (b - a)
    one = d / (b - a)
    slips = {'one-part': one, 'larger-share': one * b}
    if b - a > 1:
        slips['gap-as-one-part'] = d * (a + b)
    item(it, f"Money is shared in the ratio {a} : {b}. The second share is £{int(d)} more than the first. What is the total?", one * (a + b), slips)


JOBS = [
    ('ratio/fluency-l2-building-percentages', 'whole-percent', l2_whole),
    ('ratio/fluency-l2-building-percentages', 'half-percent', l2_half),
    ('ratio/fluency-l4-multipliers', 'write-multiplier', l4_write),
    ('ratio/fluency-l4-multipliers', 'apply-multiplier', l4_apply),
    ('ratio/fluency-l5-rise-or-fall', 'percentage-change', l5_change),
    ('ratio/fluency-l5-rise-or-fall', 'daily-return', l5_return),
    ('ratio/fluency-l6-before-the-discount', 'undo-a-discount', l6_discount),
    ('ratio/fluency-l6-before-the-discount', 'undo-a-rise', l6_rise),
    ('ratio/fluency-l6-before-the-discount', 'vat-inside', l6_vat),
    ('ratio/fluency-l9-sharing', 'share-a-total', l9_total),
    ('ratio/fluency-l9-sharing', 'from-one-share', l9_one),
    ('ratio/fluency-l9-sharing', 'three-way', l9_three),
    ('ratio/fluency-l9-sharing', 'from-a-difference', l9_diff),
]

for ref, fam, fn in JOBS:
    run(ref, fam, fn)
print(f"{len(JOBS)} families, {N} draws each, {count} checks")
lv.report()
