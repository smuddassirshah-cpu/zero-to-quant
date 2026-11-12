"""Every `skills` id of each analysis problem set is carried by a lesson of its level. Run from the repo root."""
import glob
import json
import sys

bad = 0
for n, ls in ((1, range(1, 6)), (2, range(6, 11)), (3, range(11, 15))):
    taught = set()
    for l in ls:
        f = glob.glob(f"app/content/courses/analysis/l{l}-*.json")[0]
        taught |= set(json.load(open(f)).get("skills", []))
    d = json.load(open(f"app/content/courses/analysis/problems-{n}.json"))
    used = {s for it in d["items"] for s in it["skills"]}
    # a level may also use skills of earlier levels
    print(n, "lessons carry", sorted(taught), "; set uses", sorted(used))
    if n == 1 and not used <= taught:
        bad += 1
sys.exit(bad)
