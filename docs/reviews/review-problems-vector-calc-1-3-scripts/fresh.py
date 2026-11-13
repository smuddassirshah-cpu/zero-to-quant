"""Reader's reuse grep: normalised strings of app/content against key formulas of the three sets."""
import json, sys, os, re, glob
ROOT = sys.argv[1]  # app/content
def norm(s):
    s = s.replace('\\tfrac', '\\frac').replace('\\dfrac', '\\frac').replace('\\left', '').replace('\\right', '')
    s = s.replace('\\,', '').replace('\\ ', '').replace('\\;', '').replace('\\cdot', '*').replace('\\times', '*')
    return re.sub(r'\s+', '', s)
def strings(o, path=''):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from strings(v, path + '.' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from strings(v, path + '[%d]' % i)
PAT = {
 'P1': ['2x-y', 'x+2y', '3\\cost,3\\sint', 'x^2+y^2=9', '\\sqrt{50}', '9\\sqrt5', '3\\sqrt5', '(xy,x+y)', 't,t^3', '\\frac{29}{20}', '\\frac{7}{60}',
        '3x^2+y^2', 'x^3+xy^2', 'y^2+ky', '2xy+3x', 'xy^2+3xy', '2\\cost,5\\sint', '20\\pi', '20\\sin^2', 'bead', '(-1,7)', '5x^2+5y^2', 'y^2+3y'],
 'P2': ['y^3-4y', 'xy^2+2x', '[0,3]*[0,1]', '6-2y^2', 'cycloid', 't-\\sint', '1-\\cost', '\\frac{5\\pi}{2}', 'centroid', 'x^2+y,2xy', '(x^2+y', '\\frac{64}{3}', '\\frac{70}{3}',
        '(5,1)', '(4,5)', '2x-4y', '(0,0),(4,0)', '(4,0)', '-\\frac{y^2}{2}', 'plotofland', 'x_1y_2-x_2y_1', '3y^2+6', '8x-2x^2', 'wheel'],
 'P3': ['z=xy', 'x^2+y^2\\le3', '(y,x,5)', '\\frac{14\\pi}{3}', '\\frac{21\\pi}{2}', '(-y,-x,1)', '\\sqrt{1+x^2+y^2}', '\\sqrt{1+r^2}', '5-r^2', '[0,4]*[0,1]*[0,2]', '(xz,', 'z+2y+3', 'z=2-x',
        '-yz,xz', '28\\pi', '7-2x', '(3,-2y,2z)', '(1,0,1)', '2y-z^2', 'x+xz+3z', 'x^2+y^2=16', 'x^2+y^2\\le16', '16\\pi', '32\\pi', 'saddle', 'tank', 'roof', '\\frac{9\\pi}{2}',
        'x^2+y^2=4', 'x^2+y^2\\le4', 'slant', 'x^2+y^2\\le3'],
}
files = sorted(glob.glob(os.path.join(ROOT, '**', '*.json'), recursive=True))
want = sys.argv[2:]  # substrings of path to include
for lvl, pats in PAT.items():
    for p in pats:
        hits = []
        for f in files:
            rel = os.path.relpath(f, ROOT)
            if want and not any(w in rel for w in want):
                continue
            if 'vector-calc/problems-' in rel or rel == 'manifest.json':
                continue
            try:
                d = json.load(open(f))
            except Exception:
                continue
            for path, s in strings(d):
                n = norm(s)
                if norm(p) in n:
                    i = n.index(norm(p))
                    hits.append('%s %s: ...%s...' % (rel, path, n[max(0, i - 50):i + 70]))
        if hits:
            print('== %s  %r  %d hit(s)' % (lvl, p, len(hits)))
            for h in hits[:6]:
                print('    ' + h[:300])
