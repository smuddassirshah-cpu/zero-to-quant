"""Reuse and stale-number greps for the renumbered items of delta read AC-3.
   Run from the repo root:  python docs/reviews/review-delta-ac-3-scripts/fresh.py [--show]

   REUSE: the new numbers and settings of each renumbered item, searched in every string of every file under
   app/content (DECISIONS session AB). Hits in the item's own file are dropped. Hits are printed for reading;
   nothing here fails.
   STALE: the old numbers of each renumbered item (from the Fix pass sections), searched in the item as it stands.
   A hit is printed as STALE and counted; each one is judged in the review."""
import glob
import json
import re
import sys

SHOW = "--show" in sys.argv


def strings(d, path=""):
    if isinstance(d, str):
        yield path, d
    elif isinstance(d, dict):
        for k, v in d.items():
            yield from strings(v, f"{path}.{k}" if path else k)
    elif isinstance(d, list):
        for i, v in enumerate(d):
            yield from strings(v, f"{path}[{i}]")


def numbers_too(d, path=""):
    """Strings and numbers, numbers as text."""
    if isinstance(d, (str, int, float)) and not isinstance(d, bool):
        yield path, str(d)
    elif isinstance(d, dict):
        for k, v in d.items():
            yield from numbers_too(v, f"{path}.{k}" if path else k)
    elif isinstance(d, list):
        for i, v in enumerate(d):
            yield from numbers_too(v, f"{path}[{i}]")


FILES = sorted(glob.glob("app/content/**/*.json", recursive=True))
DOCS = {}
for f in FILES:
    if f.endswith("manifest.json"):
        continue
    try:
        DOCS[f] = json.load(open(f))
    except Exception:
        pass

# (label, own file, [regex ...]) : every regex is searched in every string of every other file
REUSE = [
    ("ratio p-partners-profit", "app/content/courses/ratio/problems-3.json", [
        r"3 : 4 : 8", r"3:4:8", r"12\{?,\}?000 : 16", r"5\{?,\}?120", r"14\{?,\}?250", r"42\{?,\}?750", r"1\{?,\}?586\.67",
        r"11\{?,\}?900", r"9\{?,\}?600 \\div 15", r"2\{?,\}?850"]),
    ("ratio p-print-run", "app/content/courses/ratio/problems-3.json", [
        r"36\{?,\}?000 leaflets", r"[Ff]our (identical )?(presses|machines|printers|pumps|workers)[^.]{0,40}15 hours", r"4 \\times 15 = 60",
        r"60 \\div 8 = 7\.5", r"press-hours", r"3\{?,\}?360"]),
    ("ratio p-phone-rise p4", "app/content/courses/ratio/problems-1.json", [
        r"SIM-only", r"14(\.00)? \\div 32\.13", r"43\.6\\?%", r"0\.4357", r"18\.13"]),
    ("eigen p-machine-stops", "app/content/courses/eigen/problems-4.json", [
        r"-0\.1 & 0\.4 \\\\ 0\.1 & -0\.4", r"-0\.4 & 0\.1 \\\\ 0\.4 & -0\.1", r"\(0\.8, 0\.2\)", r"\(0\.2, 0\.8\)", r"0\.2 \+ 0\.8e\^\{-0\.5",
        r"\\ln 80", r"e\^\{-2\.5\}"]),
    ("eigen p-linked-lagoons", "app/content/courses/eigen/problems-4.json", [
        r"1 & 0 \\\\ 1 & 1", r"1 & 0 \\\\ -1 & 1", r"-2 & 2 \\\\ 0 & -5", r"-2 & 2 \\\\ -2 & -3", r"-4 & 2 \\\\ 1 & -3"]),
    ("number-sense p-rye-loaves", "app/content/courses/number-sense/problems-1.json", [
        r"\\t?frac\{5\}\{6\} \\div \\t?frac\{1\}\{5\}", r"\\t?frac\{25\}\{6\}", r"4\\t?frac\{1\}\{6\}", r"\\t?frac\{1\}\{30\}", r"\\t?frac\{19\}\{30\}",
        r"\\t?frac\{25\}\{30\} - \\t?frac\{24\}\{30\}"]),
    ("number-sense p-cube-tub", "app/content/courses/number-sense/problems-3.json", [
        r"2\{?,\}?169", r"\b441\b", r"2\{?,\}?025", r"12\^3", r"1\{?,\}?728", r"2\{?,\}?197", r"21\^2", r"\\sqrt\{441\}"]),
    ("number-sense p-garden-beds p1", "app/content/courses/number-sense/problems-1.json", [
        r"20 (equal )?beds", r"quarter of 20", r"20 \\div 4 = 5"]),
]

print("REUSE (hits outside the item's own file)")
for label, own, pats in REUSE:
    for pat in pats:
        rx = re.compile(pat)
        hits = []
        for f, d in DOCS.items():
            if f == own:
                continue
            for path, s in strings(d):
                m = rx.search(s)
                if m:
                    hits.append((f, path, s[max(0, m.start() - 60):m.end() + 60].replace("\n", " ")))
        print(f"  {label:32s} /{pat}/ : {len(hits)} hit(s) in {len({h[0] for h in hits})} file(s)")
        for f, path, ctx in hits[: (40 if SHOW else 6)]:
            print(f"      {f.replace('app/content/', '')} {path}: ...{ctx}...")


def item(f, pid):
    for it in DOCS[f]["items"]:
        if it["id"] == pid:
            return it
    raise KeyError(pid)


# old numbers that must be gone from the item as it stands (strings and stored numbers)
STALE = [
    ("app/content/courses/ratio/problems-1.json", "p-phone-rise", [
        r"12\.00", r"37\.3", r"0\.3735", r"0\.373\b", r"20\.13", r"2\.6775", r"267\.", r"0\.6265", r"62\.6", r"\b40\\?%"]),
    ("app/content/courses/ratio/problems-3.json", "p-partners-profit", [
        r"18\{?,\}?000", r"24\{?,\}?000", r"30\{?,\}?000", r"(?<![0-9])6\{?,\}?000", r"3 : 4 : 5", r"\b12(?!\{?,\}?000)\b", r"\b72\b", r"\b36\b",
        r"\b800\b", r"4\{?,\}?000(?! divides)(?!,)(?! is)", r"11\{?,\}?400", r"34\{?,\}?200", r"1\{?,\}?700", r"1\{?,\}?983", r"\b5 parts", r"\b9 : 12"]),
    ("app/content/courses/ratio/problems-3.json", "p-print-run", [
        r"[Ff]ive", r"\b5 presses", r"12 hours", r"5 \\times 12", r"19\.2", r"2\{?,\}?150", r"\b3 hours", r"3 more", r"\b9\b"]),
    ("app/content/courses/eigen/problems-4.json", "p-machine-stops", [
        r"0\.75", r"0\.25", r"-0\.8\b", r"0\.6\b", r"\b3 hours", r"-2\.4", r"0\.318", r"5\.40?\b", r"\\ln 75", r"0\.773", r"0\.068", r"0\.374",
        r"0\.587", r"4\.02", r"5\.76", r"7\.20?\b", r"3\.45", r"\(3, 1\)", r"\(1, 3\)", r"0\.15\b", r"0\.0907", r"4\.317", r"-0\.2\b"]),
    ("app/content/courses/eigen/problems-4.json", "p-linked-lagoons", [
        r"1 & 1 \\\\ 0 & 1", r"1 & -1 \\\\ 0 & 1", r"\(4, -1\)", r"\(3, -1\)", r"\(3, 2\)", r"w_1 = "]),
    ("app/content/courses/number-sense/problems-1.json", "p-garden-beds", [
        r"one-fifth", r"\b50\b", r"two fifths of 20", r"20 \\div 5 \\times 2 = 8\$ beds\. That"]),
    ("app/content/courses/number-sense/problems-1.json", "p-rye-loaves", [
        r"frac\{1\}\{4\}", r"quarter", r"3\\t?frac\{1\}\{3\}", r"frac\{10\}\{3\}", r"frac\{1\}\{12\}", r"frac\{1\}\{10\}", r"twelfths", r"frac\{7\}\{12\}",
        r"3\.3333", r"0\.0833", r"0\.2083", r"0\.5833", r"0\.0694", r"\b0\.7\b", r"\b0\.3\b", r"\b0\.1\b", r"\b3 loaves", r"\b3 whole"]),
    ("app/content/courses/number-sense/problems-3.json", "p-cube-tub", [
        r"1\{?,\}?500", r"1\{?,\}?331", r"(?<![,}0-9])169\b", r"\b11\b", r"\b38\b", r"\b500\b", r"1\{?,\}?379", r"-228", r"1\{?,\}?467", r"84\.5", r"42\.25",
        r"13\^2", r"11\^3", r"\\sqrt\{169\}"]),
]

print("\nSTALE (old numbers still in the item)")
stale = 0
for f, pid, pats in STALE:
    it = item(f, pid)
    for pat in pats:
        rx = re.compile(pat)
        for path, s in numbers_too(it):
            m = rx.search(s)
            if m:
                stale += 1
                print(f"  STALE {pid} {path}: /{pat}/ in ...{s[max(0, m.start() - 70):m.end() + 50]}...")
print(f"fresh: {stale} STALE hit(s), each judged in the review")
