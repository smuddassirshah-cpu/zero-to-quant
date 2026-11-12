"""Second read, proof problems-1 to -3: print chosen items whole, for the reuse comparison.
Usage (repo root): python3 docs/reviews/review-problems-proof-1-3-scripts/peek.py <file under app/content> <list key path, e.g. screens or items or parts.4.items> <index>... [--len n]"""
import json
import sys

args = sys.argv[1:]
n = 1800
if '--len' in args:
    i = args.index('--len'); n = int(args[i + 1]); del args[i:i + 2]
d = json.load(open('app/content/' + args[0]))
for k in args[1].split('.'):
    d = d[int(k)] if k.isdigit() else d[k]
for i in args[2:]:
    s = d[int(i)]
    keep = {k: s[k] for k in ('id', 'title', 'prose', 'question', 'widget', 'parts', 'feedback', 'explain') if k in s}
    print(f'[{i}]', json.dumps(keep, ensure_ascii=False)[:n])
    print()
