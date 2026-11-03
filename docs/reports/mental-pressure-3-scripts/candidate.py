"""The sample candidate's marked mock (random.Random(81)) over the seed-80 paper."""
import random
from fractions import Fraction as F
from mockgen import generate

SECONDS = {"addsub": (3, 6), "mul": (4, 8), "div": (4, 8), "dec": (4, 8), "frac": (6, 11), "pct": (4, 7), "seq": (5, 10)}
RIGHT = {"addsub": 0.95, "mul": 0.9, "div": 0.9, "dec": 0.85, "frac": 0.75, "pct": 0.9, "seq": 0.85}
LIMIT = 480


def candidate_log(seed=81, paper_seed=80):
    rng = random.Random(seed)
    paper = generate(paper_seed)
    log, clock = [], F(0)
    for i, (k, text, opts, ans, letter) in enumerate(paper, 1):
        lo, hi = SECONDS[k]
        secs = F(round(rng.uniform(lo, hi), 1)).limit_denominator(10)
        if rng.random() < 0.08:
            secs += F(round(rng.uniform(6, 14), 1)).limit_denominator(10)
        right = rng.random() < RIGHT[k]
        chosen = letter if right else rng.choice([L for L in "ABCD" if L != letter])
        if clock + secs > LIMIT:
            log.append(dict(q=i, kind=k, text=text, secs=None, mark="blank", chosen=None, letter=letter))
            continue
        clock += secs
        log.append(dict(q=i, kind=k, text=text, secs=secs, mark="right" if right else "wrong", chosen=chosen, letter=letter, clock=clock))
    return log


def sort_type(r):
    if r["mark"] == "wrong":
        return "S" if r["secs"] <= 6 else "M"
    if r["mark"] == "right" and r["secs"] > 12:
        return "T"
    return None


if __name__ == "__main__":
    log = candidate_log()
    for r in log:
        print(r["q"], r["kind"], r["text"], r["secs"] and float(r["secs"]), r["mark"], r.get("chosen"), r["letter"], sort_type(r), r.get("clock") and float(r["clock"]))
    R = sum(r["mark"] == "right" for r in log); W = sum(r["mark"] == "wrong" for r in log); B = sum(r["mark"] == "blank" for r in log)
    print("right", R, "wrong", W, "blank", B, "net", R - W)
    for b in range(4):
        blk = log[20 * b: 20 * b + 20]
        print("block", b + 1, sum(r["mark"] == "right" for r in blk), sum(r["mark"] == "wrong" for r in blk), sum(r["mark"] == "blank" for r in blk),
              float(sum(r["secs"] or 0 for r in blk)))
