"""grep the freshness index. Usage: g.py <index.tsv> <max per pattern> <width> pattern [pattern ...]  (regex, case-blind)"""
import re, sys
lines = open(sys.argv[1]).read().split('\n')
n, w = int(sys.argv[2]), int(sys.argv[3])
for p in sys.argv[4:]:
    hits = [l for l in lines if re.search(p, l, re.I)]
    print(f'=== {p}  ({len(hits)} hits)')
    for l in hits[:n]:
        print('  ', l[:w])
