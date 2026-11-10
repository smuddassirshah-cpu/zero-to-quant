"""Print drills as a candidate and a reviewer read them.

usage: dump.py <drills dir> <slug> [<slug> ...] [--planted]
"""
import json
import sys

SHOWN = ("id", "fn", "difficulty", "pace", "pattern", "tags", "brief", "constraints", "hint",
         "examples", "tests", "how", "solution", "notes", "planted", "starter")


def cut(s, n=260):
    s = str(s)
    return s if len(s) <= n else s[:n] + " ...[%d]" % len(s)


for slug in sys.argv[2:]:
    if slug.startswith("--"):
        continue
    d = json.load(open("%s/ci-%s.json" % (sys.argv[1], slug)))
    print("=====", d["id"], "| fn", d["fn"], "| diff", d["difficulty"], "| pace", d.get("pace"),
          "| pattern", d.get("pattern"), "| tags", d["tags"], "| other", {k: d[k] for k in d if k not in SHOWN})
    print("BRIEF:", d["brief"])
    print("CONSTRAINTS:", *d["constraints"], sep="\n  - ")
    print("HINT:", d["hint"])
    print("STARTER:", cut(d["starter"], 200))
    for e in d["examples"]:
        print("EX:", cut(e["call"]), "=>", cut(e["expect"]), "| NOTE:", e.get("note"))
    for i, t in enumerate(d["tests"]):
        print("T%d:" % i, cut(t["call"]), "=>", cut(t["expect"], 120),
              "" if t.get("compare", "equal") == "equal" else t.get("compare"))
    print("HOW:", d["how"])
    print("NOTES:", *d["notes"], sep="\n  - ")
    print("SOLUTION:\n" + d["solution"])
    for p in d.get("planted", []):
        print("PLANTED slip:", p.get("slip"))
        if "--planted" in sys.argv:
            print(p.get("code") or p.get("solution") or p)
