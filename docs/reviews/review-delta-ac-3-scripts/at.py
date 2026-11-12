"""Compact view of the node at an index path. Run from the repo root:
   python docs/reviews/review-delta-ac-3-scripts/at.py <file under app/content, no .json> <path> [<path> ...]
   A path is like items[7].parts[0] or screens[5]. A node with parts prints every part, or one with .parts[n]."""
import json
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from brief import show_part  # noqa: E402
from dump import load  # noqa: E402


def walk(d, path):
    for tok in re.findall(r"[A-Za-z_]+|\[\d+\]", path):
        d = d[int(tok[1:-1])] if tok.startswith("[") else d[tok]
    return d


def show(node, tag):
    if "prose" in node and "parts" in node:
        print(" PROSE:", node["prose"])
    if "parts" in node:
        for i, p in enumerate(node["parts"]):
            show_part(p, f"{tag}.parts[{i}]")
    elif "quiz" in node and "widget" not in node:
        for i, p in enumerate(node["quiz"]):
            show_part(p, f"{tag}.quiz[{i}]")
    else:
        for k in ("title", "text", "body"):
            if isinstance(node.get(k), str):
                print(f" {k}:", node[k][:1200])
        show_part(node, tag)
        rest = {k: v for k, v in node.items() if k not in ("widget", "feedback", "explain", "question", "prompt", "prose", "title", "text", "body", "hint", "hints")}
        if rest:
            print("   other:", json.dumps(rest, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    d = load(sys.argv[1])
    for p in sys.argv[2:]:
        print("=" * 10, sys.argv[1], p)
        show(walk(d, p), p)
