"""Print the context of a regex in content files. Run from the repo root.
python ctx.py <regex> <glob under app/content> [max hits] [chars before] [chars after]"""
import glob
import re
import sys

pat = re.compile(sys.argv[1])
files = sorted(glob.glob("app/content/" + sys.argv[2], recursive=True))
mx = int(sys.argv[3]) if len(sys.argv) > 3 else 5
before = int(sys.argv[4]) if len(sys.argv) > 4 else 160
after = int(sys.argv[5]) if len(sys.argv) > 5 else 220
for f in files:
    s = open(f).read()
    n = 0
    for m in pat.finditer(s):
        n += 1
        if n > mx:
            break
        a, b = max(0, m.start() - before), min(len(s), m.end() + after)
        print(f"{f.replace('app/content/', '')}: ...{s[a:b]}...".replace("\n", " "))
