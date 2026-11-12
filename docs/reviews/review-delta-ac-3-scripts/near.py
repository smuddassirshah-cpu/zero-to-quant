"""Find the question that holds a numeric key or a wrong id, and print it compactly with its path.
   python docs/reviews/review-delta-ac-3-scripts/near.py <file under app/content, no .json> <number | wrong-id> [...]
   A number matches a widget whose answer equals it to 6 significant figures; a word matches a wrong[] id."""
import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from brief import show_part  # noqa: E402
from dump import load  # noqa: E402


def holders(d, path=""):
    """Yield (path, node, parent) for every node that owns a widget."""
    if isinstance(d, dict):
        if isinstance(d.get("widget"), dict):
            yield path, d
        for k, v in d.items():
            yield from holders(v, f"{path}.{k}" if path else k)
    elif isinstance(d, list):
        for i, v in enumerate(d):
            yield from holders(v, f"{path}[{i}]")


def parent_of(d, path):
    import re
    toks = re.findall(r"[A-Za-z_]+|\[\d+\]", path)
    # drop the trailing parts[n] / quiz[n] to reach the item
    if len(toks) >= 2 and toks[-2] in ("parts", "quiz"):
        toks = toks[:-2]
    else:
        return None
    for tok in toks:
        d = d[int(tok[1:-1])] if tok.startswith("[") else d[tok]
    return d


def matches(w, key):
    try:
        x = float(key)
    except ValueError:
        return any(e.get("id") == key for e in w.get("wrong", []))
    a = w.get("answer")
    return isinstance(a, (int, float)) and abs(a - x) <= 1e-6 * max(1, abs(x))


if __name__ == "__main__":
    d = load(sys.argv[1])
    for key in sys.argv[2:]:
        for path, node in holders(d):
            if matches(node["widget"], key):
                print("=" * 10, sys.argv[1], path, f"(match {key})")
                par = parent_of(d, path)
                for src in (par, node):
                    if src:
                        for k in ("id", "title", "prose", "text"):
                            if isinstance(src.get(k), str):
                                print(f" {k}:", src[k][:1500])
                show_part(node, path.rsplit(".", 1)[-1])
