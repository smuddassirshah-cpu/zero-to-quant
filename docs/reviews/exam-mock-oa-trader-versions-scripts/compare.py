"""Compare the reader's blind answers (recorded before the keys were read) with each file's key.

Usage: python compare.py <repo root>
"""
import json
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'

# Blind answers, written down from blind.py output before this script was run.
BLIND = {
    2: ['4', '2', '15', '169', '135', '26', '60', '12', '384', '94', '256', '7', '26', '1595', '221',
        r'\dfrac{2}{7}', r'\dfrac{5}{12}', r'\dfrac{1}{480}', r'\dfrac{3}{5}', r'\dfrac{27}{100}',
        r'\dfrac{1}{3}', r'\dfrac{21}{1000}', r'\dfrac{1}{10}', r'\dfrac{1}{150}', r'\dfrac{1}{5}',
        r'\dfrac{5}{16}', r'\dfrac{11}{32}', r'\dfrac{2}{3}', r'\dfrac{11}{18}', r'\dfrac{1}{2}',
        ['bo3', 'one', 'both'], ['sq02', 'one3', 'bo3w'], ['disc', 'w1', 'w5'], ['s5', 's3', 'near'],
        ['j3', 'j1', 'j5'], ['g7', 'g3', 'g1'],
        '600,000 to 610,000', '59 to 60', '2.001 to 2.002', '5.8 to 5.9'],
    3: ['0.123456', r'\tfrac{6}{13}', '121', '57', '42', '4', '68', '11', '441', '203', '83', '4', '8',
        '42', '46656',
        r'\dfrac{4}{9}', r'\dfrac{1}{6}', r'\dfrac{1}{4}', r'\dfrac{9}{2}', r'\dfrac{2}{9}',
        r'\dfrac{3}{11}', r'\dfrac{13}{32}', r'\dfrac{1}{10}', r'\dfrac{2}{21}', r'\dfrac{1}{12}',
        r'\dfrac{2}{5}', r'\dfrac{14}{27}', r'\dfrac{12}{7}', r'\dfrac{4}{7}', r'\dfrac{3}{2}',
        ['d12', 'edge', 'hh3'], ['adj', 'hhh5', 'rep'], ['hhh10', 'oct', 'd30'],
        ['hh6', 'dig1', 'dif1'], ['h3in7', 'd36', 'h4in12'], ['r2', 'r3', 'r4'],
        '142 to 143', '3.6 to 3.7', '2.9 to 3.0', '75,000 to 76,000'],
}

agree = 0
total = 0
for v in (2, 3):
    d = json.load(open(f'{ROOT}/app/content/exams/mock-oa-trader-{v}.json'))
    items = [it for p in d['parts'] if 'items' in p for it in p['items']]
    for it, mine in zip(items, BLIND[v]):
        w = it['widget']
        if w['kind'] == 'choice':
            key = [o['text'] for o in w['options'] if o.get('correct')]
            key = key[0].strip('$') if len(key) == 1 else key
        else:
            key = w['answer']
        total += 1
        ok = key == mine
        agree += ok
        if not ok:
            print(f'v{v} {it["id"]}: mine {mine} key {key}')
print(f'blind agreement {agree} of {total}')
