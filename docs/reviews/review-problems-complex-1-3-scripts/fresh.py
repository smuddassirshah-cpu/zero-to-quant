"""Freshness grep for complex problems-1 to -3: key numbers, expressions and nouns of each problem,
searched in every JSON file under app/content except the three sets themselves.
Whitespace is ignored on both sides. Hits are for reading by eye, not a verdict.
Run from the repo root: python3 docs/reviews/review-problems-complex-1-3-scripts/fresh.py"""
import glob
import json
import re

KEYS = {
    "p-parallel-branches": ["2 + 5i", "4 - 3i", "23 + 14i", "6 + 2i", "4.15", "18.125", "4.257", "2.819", "12.9", "impedance", "parallel"],
    "p-turning-frames": ["z^2 - 3z + 3", "3z + 3", "\\sqrt3\\,e^{i\\pi/6}", "-27", "729", "animation", "frame"],
    "p-four-lamps": ["81", "6561", "4.243", "3\\sqrt2", "3\\sqrt{2}", "lamp", "w^4 ="],
    "p-neutral-wire": ["12e^{2\\pi i/3}", "7e^{4\\pi i/3}", "10.392", "6\\sqrt3", "16.643", "phasor", "three-phase", "neutral"],
    "p-mesh-map": ["z^2 - 4z", "2.5 + 3i", "-12.75", "1 + 6i", "6.083", "80.5", "\\sqrt{37}", "0.0037", "mesh"],
    "p-plate-heat": ["2xy + 3x", "y^2 - x^2 + 3y", "3z - iz^2", "5 - 2i", "5.385", "\\sqrt{29}", "plate", "temperature"],
    "p-log-branches": ["4\\sqrt3", "-\\sqrt3 + i", "\\ln 8", "7\\pi}{6}", "5\\pi}{6}", "0.0729", "13.708", "0.125"],
    "p-modulus-plus-z": ["|z|^2 + z", "|z|^2", "x^2 + y^2 + x", "0.01i"],
    "p-traffic-island": ["3t + it^2", "3 + 2it", "9t + 2t^3", "5 + i", "(3 + i)", "2iA", "island", "\\bar z\\,dz"],
    "p-lighthouse-flashes": ["x^2 - 2x + 10", "x^2 + 9", "1 + 3i", "0.955", "1.047", "0.0498", "e^{-3}", "lighthouse", "\\frac{1}{6i}", "\\tfrac{1}{6i}"],
    "p-share-moments": ["£64", "0.03125", "0.01875", "66.61", "4664", "4665", "15.08", "2241", "\\varphi(-i)", "\\varphi(-2i)", "E[S_T^2]"],
    "p-print-stages": ["1 - 2iu", "2 - iu", "-8\\pi", "-25.13", "-24\\pi", "print", "\\varphi'(0)", "\\varphi''(0)"],
}
OWN = {f"app/content/courses/complex/problems-{n}.json" for n in (1, 2, 3)}


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


squash = lambda s: re.sub(r"\s+", "", s)
TEXT = {}
for path in glob.glob("app/content/**/*.json", recursive=True):
    if path in OWN or path.endswith("manifest.json"):
        continue
    try:
        TEXT[path] = squash(" ".join(strings(json.load(open(path)))))
    except Exception:
        pass

for prob, keys in KEYS.items():
    print("==", prob)
    for k in keys:
        kk = squash(k)
        num = re.fullmatch(r"-?[\d.]+", kk) is not None
        pat = re.compile((r"(?<![\d.])" if num else "") + re.escape(kk) + (r"(?![\d])" if num else ""))
        hits = sorted(p for p, t in TEXT.items() if pat.search(t))
        inc = [h.replace("app/content/", "") for h in hits if "/complex/" in h or "topic-1.11" in h]
        print(f"   {k!r:28} course+exam: {inc if inc else '-'}; elsewhere: {len(hits) - len(inc)} file(s)" + (" " + str([h.replace('app/content/', '') for h in hits if h.replace('app/content/', '') not in inc][:4]) if 0 < len(hits) - len(inc) <= 4 else ""))
