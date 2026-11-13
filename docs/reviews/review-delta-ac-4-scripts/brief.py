"""Compact view of items: one line per field. Run from the repo root:
   python docs/reviews/review-delta-ac-4-scripts/brief.py <file under app/content, no .json> <id> [<id> ...]"""
import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from dump import find, load  # noqa: E402


def show_widget(w, ind="   "):
    if w is None:
        return
    keys = {k: v for k, v in w.items() if k not in ("wrong", "options")}
    print(ind + "W", json.dumps(keys, ensure_ascii=False))
    for x in w.get("wrong", []):
        print(ind + "  wrong", json.dumps(x, ensure_ascii=False))
    for o in w.get("options", []):
        print(ind + "  opt", json.dumps(o, ensure_ascii=False))


def show_part(p, tag):
    print(f" [{tag}] Q:", p.get("question") or p.get("prompt") or p.get("prose"))
    show_widget(p.get("widget"))
    fb = p.get("feedback") or {}
    for k, v in fb.items():
        if isinstance(v, dict):
            for kk, vv in v.items():
                print(f"   fb.{k}.{kk}:", vv)
        else:
            print(f"   fb.{k}:", v)
    for k in ("explain", "hint", "hints"):
        if k in p:
            print(f"   {k}:", json.dumps(p[k], ensure_ascii=False))


if __name__ == "__main__":
    d = load(sys.argv[1])
    for pid in sys.argv[2:]:
        it = find(d, pid)
        print("=" * 10, sys.argv[1], pid)
        if it.get("prose"):
            print(" PROSE:", it["prose"])
        if "parts" in it:
            for i, p in enumerate(it["parts"], 1):
                show_part(p, i)
        else:
            show_part(it, "-")
