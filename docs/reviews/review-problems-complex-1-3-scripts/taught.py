"""Skim what the complex course teaches and sets, one line per screen or item.
Run from the repo root:
  python3 docs/reviews/review-problems-complex-1-3-scripts/taught.py <file-stem>... [--width n]
e.g. taught.py l1-square-root-of-minus-one review-1 homework-1 exam
"""
import json
import sys

args = [a for a in sys.argv[1:] if not a.startswith("--") and not a.isdigit()]
W = 170
if "--width" in sys.argv:
    W = int(sys.argv[sys.argv.index("--width") + 1])


def cut(s):
    s = " ".join(str(s).split())
    return s if len(s) <= W else s[:W] + "..."


def ans(w):
    if not isinstance(w, dict):
        return ""
    if w.get("kind") == "choice":
        c = [o.get("text") for o in w.get("options", []) if o.get("correct")]
        return "choice: " + cut(c[0] if c else "?")
    for k in ("answer", "answers", "solution"):
        if k in w:
            return f"{w.get('kind')}: " + cut(w[k])
    return str(w.get("kind"))


def item(tag, s):
    print(f"  {tag} [{s.get('type', s.get('id', ''))}] {cut(s.get('prose', ''))}")
    if s.get("question"):
        print(f"      Q: {cut(s['question'])}  => {ans(s.get('widget'))}")
    for st in s.get("steps", []) or []:
        if isinstance(st, dict):
            print(f"      step: {cut(st.get('question') or st.get('prose') or st.get('text') or '')}  => {ans(st.get('widget'))}")
    for i, p in enumerate(s.get("parts", []) or []):
        print(f"      part {i + 1}: {cut(p.get('question', ''))}  => {ans(p.get('widget'))}")


for a in args:
    path = "app/content/exams/topic-1.11.json" if a == "exam" else f"app/content/courses/complex/{a}.json"
    d = json.load(open(path))
    print("#" * 10, path, d.get("title", ""))
    for key in ("screens", "quiz", "items", "questions", "sections"):
        v = d.get(key)
        if isinstance(v, list):
            for i, s in enumerate(v):
                if isinstance(s, dict) and isinstance(s.get("items"), list):
                    for j, t in enumerate(s["items"]):
                        item(f"{key}[{i}].items[{j}]", t)
                elif isinstance(s, dict):
                    item(f"{key}[{i}]", s)
