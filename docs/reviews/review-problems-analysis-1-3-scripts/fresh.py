"""Second read, analysis problems-1 to -3: reuse grep across app/content.

For each problem, its formulas, key numbers and distinctive nouns are searched (as plain substrings, with
LaTeX spacing removed) in every other content file. Hits are printed with the file; the reader judges them.
Run from the repo root: python3 docs/reviews/review-problems-analysis-1-3-scripts/fresh.py
"""
import glob
import os
import re

OWN = {os.path.normpath(f"app/content/courses/analysis/problems-{n}.json") for n in (1, 2, 3)}
NEEDLES = {
    "p-cube-root-twenty": ["x^3<20", "20q^3", "p^3-20", "21}{8}", "-979", "29.546875", "1.912109375", "2.625", "5q^3", "cube root of 20", "sqrt[3]{20}", "[2,3]", "15.45"],
    "p-climbing-fractions": ["5n-4}{n+1}", "9}{n+1}", "9}{\\\\varepsilon}", "2250", "2249", "4.996", "0.004"],
    "p-diagonal-fraction": ["0.70329", "0.18096", "0.42571", "0.96053", "0.33418", "0.55445", "100001", "55446", "0.5544"],
    "p-sum-law-band": ["6n+1}{2n+5}", "2n-2}{n+1}", "14}{2n+5}", "4}{n+1}", "137.5", "0.09914", "0.10005", "5\\\\pm0.1", "a_n+b_n-5"],
    "p-root-recursion": ["4a_n+21", "sqrt{41}", "6.403", "4L+21", "6000", "6.9997", "7-a_n"],
    "p-two-strands-cauchy": ["(-1)^n\\\\left(2-", "2-\\\\tfrac3n", "3.071", "3.196", "(-1)^n\\\\left(1+", "(-1)^n(1-"],
    "p-telescoping-tail": ["(n+1)(n+3)", "n^2+4n+7", "n^2+4n+3", "5}{12}", "0.0010005", "0.0009995", "n(n+2)", "N+2.5"],
    "p-alternating-quarters": ["n}{4^n}", "5}{1024}", "327}{2048}", "0.1597", "7}{16384", "4}{25}", "n}{2^n}", "n}{3^n}"],
    "p-cube-root-greedy": ["sqrt[3]{n}", "0.5718", "0.2063", "0.4237", "0.2697", "0.7937", "T=0.2", "sqrt{n}}"],
}


def squash(s):
    return re.sub(r"\s+", "", s)


files = sorted(glob.glob("app/content/**/*.json", recursive=True))
texts = {f: squash(open(f, encoding="utf-8").read()) for f in files if os.path.normpath(f) not in OWN and not f.endswith("manifest.json")}
for item, needles in NEEDLES.items():
    print(f"== {item}")
    for nd in needles:
        hits = [f.replace("app/content/", "") for f, t in texts.items() if squash(nd) in t]
        ana = [h for h in hits if "analysis/" in h or "topic-1.10" in h]
        print(f"  {nd!r:28} {len(hits):3} files; analysis and topic-1.10: {', '.join(ana) if ana else 'none'}")
