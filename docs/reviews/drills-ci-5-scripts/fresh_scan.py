"""List the code tasks of coding-int, trees and contests that touch a graph idea,
so each pack 5 drill can be compared with them by eye.
usage: fresh_scan.py <app/content> [word ...]   (words: print 160 characters round each hit)"""
import glob
import re
import sys

root = sys.argv[1]
words = sys.argv[2:]
strong = {'island', 'flood', 'bipart', 'topolog', 'union', 'dijkstra', 'breadth', 'depot', 'wall',
          'voucher', 'coupon', 'ferry', 'clash', 'redundan', 'spare', 'cycle', 'checkpoint'}
kw = re.compile('|'.join(sorted(strong)), re.I)
for c in ('coding-int', 'trees', 'contests'):
    for f in sorted(glob.glob('%s/courses/%s/*.json' % (root, c))):
        s = open(f).read()
        if words:
            for w in words:
                for m in re.finditer(w, s, re.I):
                    print(f.split('courses/')[1], '|', s[max(0, m.start() - 80):m.start() + 160].replace('\\n', ' '))
            continue
        defs = sorted(set(re.findall(r'def (\w+)\(', s)))
        hits = sorted(set(m.group(0).lower() for m in kw.finditer(s)))
        if defs and hits:
            print(f.split('courses/')[1], defs[:10], hits)
