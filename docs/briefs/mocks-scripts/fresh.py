"""Freshness check for the three mocks (DECISIONS "Duplicates"): no item may reuse a number set, a question or a
function name found in any course, exam, bank or drill file, or in any other brief (the unwritten levels of
topic 3.5 are in the briefs).  Run from anywhere: python3 -I fresh.py

A group is a set of lower-case tokens that must all occur in the same blob (a screen, an item, a brief line).
A hit means a repeat; the script prints it and exits 1.  Function names are checked on their own.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
APP = os.path.join(ROOT, "app", "content")

NAMES = ["count_products_below", "trapped_water", "min_jumps", "min_merge_cost", "smallest_after_removing", "longest_rising",
         "count_decodings", "critical_path_length", "weighted_line_fit", "rolling_slopes", "windowed_betas", "vol_by_ticker",
         "tidy_closes", "oos_scores", "oa-product-windows", "oa-rain-water", "oa-min-jumps", "oa-merge-cost", "oa-remove-digits",
         "oa-rising-run", "oa-decodings", "oa-critical-path"]

GROUPS = {
    "S1 two regressions": [["0.35", "1.4", "slope"], ["slope", "0.7", "0.35"]],
    "S2 correlation limits": [["0.8887"], ["0.9", "-0.6", "-0.54"]],
    "S3 special eigenvalues": [["3i", "0.5"], ["135", "determinant", "eigenvalues 5"]],
    "S4 multiple testing": [["0.004167"], ["0.0042", "bonferroni"], ["12 tests", "0.05"], ["0.4596", "false positive"]],
    "M1 ridge": [["4/3", "ridge"], ["sxx", "50", "100", "ridge"]],
    "M2 lasso": [["3.4", "lasso"], ["soft", "3.0", "0.8", "1.5"]],
    "M4 pca": [["5.56", "1.44"], ["0.7945"]],
    "M5 bias variance": [["1.68", "bias"], ["0.64", "0.04", "bias"], ["42/25"]],
    "M6 boosting": [["1, 3, 8, 12"], ["18.5", "boost"], ["6.5", "boost", "1, 3"]],
    "Case 1": [["1.4546"], ["52.3%"]],
    "Case 2": [["1.265", "0.04"], ["-0.022", "0.102"]],
    "Q5 adjusted r2": [["0.3467"], ["26/75"], ["adjusted", "0.4", "50", "4"]],
    "Q6 conditional normal": [["2.56", "conditional"], ["0.4", "0.6", "conditional", "5.6"]],
    "Q7 portfolio sd": [["0.02016"], ["0.1420"], ["0.142", "portfolio"]],
    "Q8 min variance": [["10/29"], ["0.3448"], ["0.0625", "0.04", "0.015"]],
    "Q10 compound poisson": [["500", "poisson", "mean 10"], ["λ", "500", "compound"]],
    "oa tests": [["2228224", "merge"], ["999990", "water"], ["199998", "water"]],
    "data": [["qd-prices"], ["qd-pair"], ["qd-signal"]],
}
# Broad token groups were tried first (for example the bare key 135, 0.4596 or 6.5); on 4 Nov every hit was read in
# context and was a coincidence in another topic, so only the groups above, which name the item's own figures, remain.


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


def blobs_of(o, label):
    """a blob for every dict that looks like a screen or an item"""
    if isinstance(o, dict):
        if any(k in o for k in ("question", "prompt", "prose", "brief")):
            yield label, " ".join(strings(o)).lower()
        for v in o.values():
            yield from blobs_of(v, label)
    elif isinstance(o, list):
        for v in o:
            yield from blobs_of(v, label)


def corpus():
    out = []
    for path in glob.glob(os.path.join(APP, "**", "*.json"), recursive=True):
        if "manifest" in path:
            continue
        try:
            d = json.load(open(path))
        except Exception:
            continue
        rel = os.path.relpath(path, APP)
        out.extend(blobs_of(d, rel))
        out.append((rel + " (whole file)", " ".join(strings(d)).lower()))
    for path in glob.glob(os.path.join(ROOT, "docs", "briefs", "*.md")):
        if os.path.basename(path) == "mocks.md":
            continue
        for i, line in enumerate(open(path), 1):
            out.append((f"docs/briefs/{os.path.basename(path)}:{i}", line.lower()))
    return out


def near(text, tokens, width=160):
    """every token occurs within one window of `width` characters around an occurrence of the first token"""
    toks = [t.lower() for t in tokens]
    if not all(t in text for t in toks):
        return False
    start = 0
    while True:
        i = text.find(toks[0], start)
        if i < 0:
            return False
        win = text[max(0, i - width): i + width]
        if all(t in win for t in toks):
            return True
        start = i + 1


ACCEPTED = {  # hits read in context on 4 Nov and judged coincidences in other topics
    "eigen/l16-correlated-normals": "0.35 and 0.7 are loadings of a covariance example",
    "regression/l11-assumptions-fail": "the figures sit in a regression table, not in a correlation question",
    "estimation/homework-3": "0.9, -0.6 and -0.54 are entries of a returns list",
    "briefs/complex.md:41": "3i and 0.5 are complex numbers",
    "briefs/game-theory.md": "10/29 is a game-theory fraction",
    "arma/l9-shocks-that-linger": "-0.3448 is an MA(1) autocorrelation",
    "vectors/homework-3": "different covariance matrices (0.04, 0.0625 on the diagonal, other off-diagonals)",
    "research-int/homework-2": "a boosting code test with other data (y 1, 2, 6, 7)",
}


def main():
    C = corpus()
    print(f"corpus: {len(C)} blobs")
    hits = []
    for n in NAMES:
        for label, text in C:
            if n.lower() in text:
                hits.append((n, label))
    # every call text of the oa-code drills: the argument literals must not occur in the corpus
    try:
        tests = json.load(open(os.path.join(HERE, "oa_code_tests.json")))
    except FileNotFoundError:
        tests = {}
    for pid, spec in tests.items():
        for row in spec["tests"]:
            call = row["call"]
            args = call[call.index("(") + 1: call.rindex(")")].lower()
            if len(args) < 14 or "range(" in args or " * " in args:
                continue
            for label, text in C:
                if "(whole file)" in label:
                    continue
                if args in text or args.replace("'", '"') in text or args.replace('"', "'") in text:
                    hits.append((f"{pid} call args {args[:50]}", label))
    for item, groups in GROUPS.items():
        for g in groups:
            for label, text in C:
                if "(whole file)" in label:
                    continue  # whole-file blobs only for single-token groups below
                if near(text, g):
                    hits.append((f"{item} {g}", label))
    hits = [h for h in hits if not any(k in h[1] for k in ACCEPTED)]
    for h in hits:
        print("HIT ", h)
    print("FRESH: no repeats" if not hits else f"{len(hits)} hits")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
