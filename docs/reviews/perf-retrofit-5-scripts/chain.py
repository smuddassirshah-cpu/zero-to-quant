"""Gated prerequisite chain of a level (transitive, gate: false edges skipped; a lesson ref adds only that lesson),
then a case-insensitive grep of every lesson, review and homework in the chain for each term.
Usage: python chain.py course/L<n> term [term ...]   (the level's own earlier levels are included)."""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
C = ROOT / "app" / "content" / "courses"

def course(c):
    return json.loads((C / c / "course.json").read_text())

def files_of(c, n):
    lv = next(l for l in course(c)["levels"] if l["n"] == n)
    return [f"{c}/{x}.json" for x in lv["lessons"] + [lv["review"], lv["homework"]]]

def chain(c, n, seen=None):
    seen = seen if seen is not None else {}
    if (c, n) in seen: return seen
    seen[(c, n)] = files_of(c, n)
    for k in range(1, n):  # earlier levels of the same course
        chain(c, k, seen)
    lv = next(l for l in course(c)["levels"] if l["n"] == n)
    for r in lv.get("requires", []):
        ref, gate = (r, True) if isinstance(r, str) else (r["ref"], r.get("gate", True))
        if not gate: continue
        m = re.match(r"([\w-]+)/L(\d+)(?:/(.+))?$", ref)
        if m and m.group(3):
            seen.setdefault((m.group(1), "lesson:" + m.group(3)), [f"{m.group(1)}/{m.group(3)}.json"])
        elif m:
            chain(m.group(1), int(m.group(2)), seen)
        else:
            parts = ref.split("/")
            seen.setdefault(tuple(parts), [ref + ".json"])
    return seen

if __name__ == "__main__":
    c, n = sys.argv[1].split("/L"); n = int(n)
    ch = chain(c, n)
    print("chain:", sorted(f"{a}/{b}" for a, b in ch))
    for term in sys.argv[2:]:
        hits = []
        for fs in ch.values():
            for f in fs:
                p = C / f
                if p.exists() and re.search(term, p.read_text(), re.I):
                    hits.append(f)
        print(f"{term!r}: {len(hits)} files {sorted(hits)[:12]}")
