"""Reuse greps of delta read AC-4 (DECISIONS, session AB): the settings and key numbers of every re-set item, searched
in every string and stored number of every content file but the item's own set. Hits are printed for reading and judged
in the review under "Verified"; nothing here fails.
   python docs/reviews/review-delta-ac-4-scripts/fresh.py"""
import os
import subprocess
import sys

G = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grepc.py")
RUNS = [
    ("proof re-sets, everywhere but the proof sets", ["--not", "proof/problems-", "--n", "5"],
     [r"parcel", r"heavy label", r"greenhouse", r"soil", r"[Jj]udges?\b", r"dancer", r"ferr(y|ies)", r"berth", r"cx - 4", r"4n - 4", r"f_c",
      r"-2x - 4", r"5j \+ 1", r"remainder 1 on division by 5", r"n\^2 \+ 2\b(?!n)", r"3k\^2 \+ 5k \+ 2", r"\(k \+ 1\)\(3k \+ 2\)", r"5jk",
      r"3\(3k\^2\)"]),
    ("proof re-sets, the same tasks in the proof course", ["--in", "proof/", "--not", "problems-", "--n", "6"],
     [r"leaves? remainder 1", r"j \+ 1\)\(\d?k \+ 1", r"\(a - b\) = 0", r"integers from 1 to", r"witness", r"out of 10|marks?\b", r"truth table",
      r"multiple of 3", r"f\(A \\cap B\)"]),
    ("proof re-sets, the two exams", ["--in", "exams/", "--n", "6"], [r"multiple of 3, then|remainder 1|berth|\(P \\lor Q\)"]),
    ("analysis re-keyed items", ["--n", "4"],
     [r"8n \+ 3\}\{2n \+ 5", r"3n - 1\}\{n \+ 1", r"17\}\{2n", r"2\.6875", r"\b2413\b", r"43\}\{16", r"cube root of 20", r"\\sqrt\[3\]\{20\}"]),
    ("analysis, the same tasks in the course", ["--in", "courses/analysis", "--not", "problems-", "--n", "5"], [r"cube root|x\^3 < |\\sqrt\[3\]", r"sum law"]),
    ("linear-maps re-stories", ["--not", "linear-maps/problems-", "--n", "4"],
     [r"robot", r"gearbox", r"gauge", r"kiosk", r"noon temp", r"takings", r"\(1, -1, 0, 1, -1\)", r"11x \+ 12y", r"\(57, 46\)"]),
    ("complex re-sets", ["--not", "complex/problems-", "--n", "4"],
     [r"-8 \+ 15i", r"\b2\.0608", r"4\.2224", r"0\.0588", r"0\.1274", r"2\|z\|\^2", r"z\^2 \+ 2\|z\|", r"3x\^2 \+ y\^2", r"2x\^2 - 2x \+ 13",
      r"e\^\{-5/2\}", r"0\.0821", r"1\.592", r"0\.7985", r"e\^\{-0\.225\}", r"\\varphi\(3\)", r"lighthouse"]),
    ("complex, the same tasks in the course and exams", ["--in", "courses/complex", "--not", "problems-", "--n", "6"],
     [r"\|z\|\^2", r"only at (\$z = 0\$|0|the origin)", r"e\^z = ", r"w\^i|i\^i", r"x\^2 [-+] \d*x \+ \d+\}"]),
]
for title, opts, pats in RUNS:
    print("=" * 8, title)
    sys.stdout.flush()
    subprocess.run([sys.executable, G, *opts, *pats], check=True)
