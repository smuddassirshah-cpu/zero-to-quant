"""Shares over 200 draws (seeds 9001 on) for the fluency findings: how often a draw is trivial, negative, or of a shape
the grader refuses. Reads <dir>/{hcf,lcm,other,conj,quot,add,sub,cf}.json made with fluency-sample --n 200 --json.
  python3 shares.py <dir>"""
import json
import math
import re
import sys

d = sys.argv[1]


def items(name):
    return json.load(open(f'{d}/{name}.json'))['items']


def nums(s):
    return [int(x) for x in re.findall(r'\$(-?\d+)\$', s)]


h = items('hcf')
print('hcf: HCF equals the smaller number in', sum(1 for i in h if i['answer'] == min(nums(i['prompt'])[:2])), 'of', len(h), '; HCF is 1 in', sum(1 for i in h if i['answer'] == 1))
l = items('lcm')
print('lcm: LCM equals the larger number in', sum(1 for i in l if i['answer'] == max(nums(i['prompt'])[:2])), 'of', len(l), '; LCM is the product in', sum(1 for i in l if i['answer'] == math.prod(nums(i['prompt'])[:2])))
o = items('other')
print('other-number: answer equals the LCM in', sum(1 for i in o if i['answer'] == nums(i['prompt'])[2]), 'of', len(o), '; equals the HCF in', sum(1 for i in o if i['answer'] == nums(i['prompt'])[1]), '; given number equals the HCF in', sum(1 for i in o if nums(i['prompt'])[0] == nums(i['prompt'])[1]))
c = items('conj')
print('conjugate-bottom: new bottom below 0 in', sum(1 for i in c if i['answer'] < 0), 'of', len(c), '; equal to 1 in', sum(1 for i in c if i['answer'] == 1))
q = items('quot')
fac = 0
for i in q:
    m = re.match(r'^[a-z]\^2([+-]\d*)?[a-z]?([+-]\d+)$', i['answer'])
    co = re.findall(r'[+-]?\d*', i['answer'])
    b = i['vars']['p']
    cc = i['vars']['q']
    disc = b * b - 4 * cc
    if disc >= 0 and math.isqrt(disc) ** 2 == disc:
        fac += 1
print('quotient: the quotient factorises over the whole numbers in', fac, 'of', len(q))
for name in ('add', 'sub'):
    a = items(name)
    n = 0
    for i in a:
        v = i['vars']
        m, c0 = (v['p'] + v['q'], v['p'] * v['b'] + v['q'] * v['a']) if name == 'add' else (v['p'] - v['q'], v['p'] * v['b'] - v['q'] * v['a'])
        if math.gcd(m, c0) > 1:
            n += 1
    print(f'{name}-tops: the top has a common whole-number factor in', n, 'of', len(a))
cf = items('cf')
print('count-factors: no-plus-one value is 1 in', sum(1 for i in cf if any(w['id'] == 'no-plus-one' and w['value'] == 1 for w in i['wrong'])), 'of', len(cf))
