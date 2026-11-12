"""Print the learner-facing text of analysis lessons, reviews, homework and the topic exam, for reading.

Usage (repo root):
  python3 docs/reviews/review-problems-analysis-1-3-scripts/taught.py <file.json> [maxlen] [grep-regex]
With a regex only the matching lines are printed (used for the by-eye reuse read).
"""
import json
import re
import sys

SKIP = {"id", "kind", "layout", "keyboard", "placeholder", "skills", "course", "type"}


def walk(o, out, mx, key=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in SKIP:
                continue
            walk(v, out, mx, k)
    elif isinstance(o, list):
        for v in o:
            walk(v, out, mx, key)
    elif isinstance(o, str):
        s = o.replace("\n", " ")
        out.append(f"  [{key}] {s[:mx]}")
    elif isinstance(o, (int, float)) and key in ("answer", "value"):
        out.append(f"  [{key}] {o}")


if __name__ == "__main__":
    mx = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    rx = re.compile(sys.argv[3]) if len(sys.argv) > 3 else None
    out = []
    walk(json.load(open(sys.argv[1])), out, mx)
    for line in out:
        if rx is None or rx.search(line):
            print(line)
