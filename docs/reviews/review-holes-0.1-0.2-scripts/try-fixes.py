"""Writes patched COPIES of four fluency sets into <out dir> with the fixes of findings 15 to 21 applied, so the reader
can draw from them with `node app/tools/fluency-sample.mjs --file <copy> --family <id> --stats`. Content is not touched.
  python3 try-fixes.py <out dir>"""
import json
import os
import sys

out = sys.argv[1]
os.makedirs(out, exist_ok=True)


def patch(path, fn):
    d = json.load(open(path))
    for f in d['families']:
        fn(f)
    dest = os.path.join(out, os.path.basename(path))
    json.dump(d, open(dest, 'w'), ensure_ascii=False, indent=1)
    print('wrote', dest)


def l19(f):
    if f['id'] == 'table-mean':
        f['prompt'] = '{tcap} {one}, counted over ${n}$ {unit}: ${f0}$ {unit} had 0, ${f1}$ had 1, ${f2}$ had 2, ${f3}$ had 3 and ${f4}$ had 4. Find the mean number of {thing} {one}, to 2 decimal places.'


def q17(f):
    if f['id'] == 'quotient':
        f['prompt'] = 'Divide ${poly(v; 1, b2, b1, b0)}$ by $({v}{na:+})$. Give the quotient multiplied out.'


def q16(f):
    if f['id'] in ('add-tops', 'subtract-tops'):
        f['prompt'] = f['prompt'].replace('Type the top, simplified.', 'Type the top, simplified, with no brackets.')
        f['wrong'].append({'id': 'whole', 'tex': '\\frac{{{poly(v; m, c0)}}}{{({v}{a:+})({v}{b:+})}}', 'line': 'That is the whole fraction. Type only the top.'})


def q14(f):
    if f['id'] == 'conjugate-bottom':
        f['where'] = f.get('where', []) + ['p*p > q']


def n16(f):
    if f['id'] == 'other-number':
        f['where'] = f.get('where', []) + ['a > 1']


def n15(f):
    if f['id'] == 'count-factors':
        for w in f['wrong']:
            if w['id'] == 'no-plus-one':
                w['when'] = 'mul > 1'


Q, N = 'app/content/courses/quadratics/', 'app/content/courses/number-sense/'
patch(N + 'fluency-l19-one-number-for-many.json', l19)
patch(Q + 'fluency-l17-dividing-polynomials.json', q17)
patch(Q + 'fluency-l16-adding-and-solving.json', q16)
patch(Q + 'fluency-l14-roots-that-stay.json', q14)
patch(N + 'fluency-l16-shared-factors.json', n16)
patch(N + 'fluency-l15-building-blocks.json', n15)
