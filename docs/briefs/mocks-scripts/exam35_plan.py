"""Topic 3.5 exam plan: asserts the brief in docs/reports/exam-3.5.md is consistent, and prints its tables.

Run: python3 -I exam35_plan.py
Checks: 30 items; difficulty ramp 6, 15, 6, 3 (20%, 50%, 20%, 10%); every one of the 13 skills of the three courses is
tested; every level of every course is covered (by a skill first met in it, or by an item built on one of its own
lessons); item kinds count to 30; the paces fit the clock.
"""
import json, os, sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
COURSES = os.path.join(ROOT, "app", "content", "courses")

# (no, course, level, lesson, difficulty, skills, kind, pace, family tag, idea)
ITEMS = [
    (1, "research-int", 1, "l1-two-regressions", 2, ["rq-stats"], "numeric", 60, "two-regressions", "The two slopes of a pair of regressions give the correlation, and the duplicated-data follow-up in one number."),
    (2, "research-int", 1, "l2-correlation-limits", 3, ["rq-stats", "rq-linalg"], "numeric", 120, "correlation-limits", "The range of a third correlation from two others, by a positive semidefinite matrix."),
    (3, "research-int", 1, "l4-tests-in-words", 2, ["rq-stats"], "choice", 60, "p-value-meaning", "What a p-value, a power or a corrected threshold says, in plain words; each distractor a blurt."),
    (4, "research-int", 1, "l5-matrices-on-the-spot", 3, ["rq-linalg"], "numeric", 120, "special-eigenvalues", "A determinant or eigenvalue of a rank-one-plus-identity or projection matrix, by reasoning."),
    (5, "research-int", 2, "l7-ridge-against-lasso", 3, ["rq-ml"], "choice", 120, "ridge-lasso", "Which penalty zeroes a coefficient and why, with a feature-scale twist."),
    (6, "research-int", 2, "l9-pca-questions", 3, ["rq-ml", "rq-linalg"], "numeric", 120, "pca-share", "The variance share or loading of a component of a small covariance matrix."),
    (7, "research-int", 2, "l10-weak-signals", 4, ["rq-ml"], "multi", 210, "weak-signal-traps", "Which of six statements about a low signal-to-noise prediction hold (leakage, regime change, cost, sample size)."),
    (8, "research-int", 3, "l11-framing-the-question", 3, ["rq-case"], "order", 150, "case-steps", "Put the steps of an open prediction case in order; distractors are plausible wrong steps."),
    (9, "research-int", 3, "l13-baseline-first", 4, ["rq-case", "rq-ml"], "numeric", 180, "baseline-first", "The expected error of a persistence, a mean and a fitted forecast on a mean-reverting series."),
    (10, "research-int", 4, "l17-regression-by-group", 4, ["rq-data"], "code", 480, "group-fit", "A small Python function on data in the item's `prelude`: one fit per group with a guard for small groups."),
    (11, "research-int", 4, "l18-updating-a-fit", 5, ["rq-data", "rq-linalg", "rq-case"], "parts", 360, "online-fit", "Parts: update the sums when a row arrives, then when one leaves, then the cost or the stability trap."),
    (12, "coding-int", 1, "l1-merging-intervals", 2, ["ci-patterns"], "choice", 60, "pattern-pick", "Name the pattern a short problem statement needs (sweep, trie, monotonic deque, heap, XOR)."),
    (13, "coding-int", 1, "l3-window-maximum", 3, ["ci-patterns"], "numeric", 120, "deque-trace", "The number of pushes, pops or the answer after tracing a deque or a heap on a short list."),
    (14, "coding-int", 1, "l4-top-k", 3, ["ci-patterns"], "order", 150, "two-heaps", "Order the steps of a streaming median or top-k update; distractors skip the rebalance."),
    (15, "coding-int", 2, "l7-parsing-with-a-stack", 3, ["ci-strings"], "numeric", 120, "stack-parse", "The value of an expression with unary minus and truncating division, traced with a stack."),
    (16, "coding-int", 2, "l8-simulating-the-rules", 2, ["ci-strings", "ci-timed"], "numeric", 60, "rule-trace", "The state after a short list of rule steps, read from a statement as an assessment words it."),
    (17, "coding-int", 2, "l10-matching-engine", 3, ["ci-strings", "ci-design"], "choice", 120, "price-time", "Which resting orders fill, and in what order, when a crossing order arrives."),
    (18, "coding-int", 3, "l11-lru-cache", 3, ["ci-design"], "table", 150, "cache-state", "The order of keys in a least recently used cache after a list of gets and puts."),
    (19, "coding-int", 4, "l15-reading-an-assessment", 3, ["ci-timed"], "numeric", 120, "minutes-plan", "The most points in a time budget when each problem may be taken in full, in part or skipped."),
    (20, "coding-int", 4, "l16-edge-cases-first", 4, ["ci-timed"], "multi", 210, "edge-case-list", "Which inputs expose a planted bug in a short function (empty, single, repeated, boundary)."),
    (21, "coding-int", 3, "l14-rate-limiter", 4, ["ci-design", "ci-timed"], "code", 480, "event-window", "A small Python class or function counting events in a time window, with hidden tests of size and order."),
    (22, "systems", 1, "l1-latency-numbers", 2, ["sy-memory"], "numeric", 60, "latency-ladder", "A ratio or order of magnitude between two costs on the latency ladder."),
    (23, "systems", 1, "l2-caches", 3, ["sy-memory"], "numeric", 120, "cache-misses", "The count of cache misses for an access pattern and a line size."),
    (24, "systems", 1, "l4-object-layout", 3, ["sy-memory"], "tap-regions", 150, "struct-padding", "Tap the padding bytes of a struct on an array canvas, or the field that moves to shrink it."),
    (25, "systems", 1, "l3-virtual-memory", 3, ["sy-memory", "sy-os"], "choice", 120, "page-fault", "What happens, and what it costs, on a first touch of a page; a TLB miss against a page fault."),
    (26, "systems", 1, "l5-branches", 2, ["sy-memory", "sy-latency"], "numeric", 60, "branch-cost", "The cycles lost to mispredicted branches in a loop over sorted and unsorted data."),
    (27, "systems", 2, "l7-data-races", 3, ["sy-concurrency"], "multi", 150, "race-claims", "Which claims about a two-thread listing hold (a race, a lost update, a possible final value)."),
    (28, "systems", 3, "l13-tcp-and-udp", 4, ["sy-os", "sy-latency"], "choice", 180, "transport-pick", "TCP, UDP or multicast for orders and for market data, with the reason."),
    (29, "systems", 4, "l17-measuring-latency", 5, ["sy-latency"], "numeric", 300, "tail-percentile", "A percentile of a short latency list, and why the mean misleads."),
    (30, "systems", 4, "l16-ring-buffer", 5, ["sy-latency", "sy-concurrency"], "code", 600, "ring-index", "A C++ function on ring-buffer indices with a power-of-two mask, tested single-threaded."),
]
PAPER_MINUTES = 90
FIRST_MET = {  # skill first met in these levels (course.json skills per lesson and the briefs)
    "research-int": {1: ["rq-stats", "rq-linalg"], 2: ["rq-ml"], 3: ["rq-case"], 4: ["rq-data"]},
    "coding-int": {1: ["ci-patterns"], 2: ["ci-strings", "ci-timed", "ci-design"], 3: [], 4: []},
    "systems": {1: ["sy-memory", "sy-os", "sy-latency"], 2: ["sy-concurrency"], 3: [], 4: []},
}


def main():
    assert len(ITEMS) == 30
    ramp = Counter(i[4] for i in ITEMS)
    assert (ramp[2], ramp[3], ramp[4], ramp[5]) == (6, 15, 6, 3), ramp
    per_course = Counter(i[1] for i in ITEMS)
    kinds = Counter(i[6] for i in ITEMS)
    assert sum(kinds.values()) == 30
    skills = Counter(s for i in ITEMS for s in i[5])
    allskills = set()
    for c in FIRST_MET:
        d = json.load(open(os.path.join(COURSES, c, "course.json")))
        allskills |= set(d["skills"])
        lessons = {x for lv in d["levels"] for x in lv["lessons"]}
        for it in ITEMS:
            if it[1] == c:
                assert it[3] in lessons, (it[0], it[3])
                assert it[2] == next(lv["n"] for lv in d["levels"] if it[3] in lv["lessons"]), (it[0], "level")
    assert set(skills) == allskills and len(allskills) == 13, (set(skills) ^ allskills)
    # every level covered, by a first-met skill or by an item built on its own lesson
    rows = []
    for c, levels in FIRST_MET.items():
        for lv, first in levels.items():
            own = [i for i in ITEMS if i[1] == c and i[2] == lv]
            assert own, (c, lv)
            via = [i[0] for i in own if set(i[5]) & set(first)]
            if first:
                assert via, (c, lv)
            rows.append((c, lv, first, [i[0] for i in own], via))
    pace = sum(i[7] for i in ITEMS)
    assert pace <= PAPER_MINUTES * 60, pace
    print("ramp", dict(ramp), "courses", dict(per_course), "kinds", dict(kinds))
    print("skills", dict(sorted(skills.items())))
    print(f"pace {pace} s = {pace / 60:.1f} min of {PAPER_MINUTES}")
    for r in rows:
        print("level", r)
    out = ["| # | Course, lesson | Lvl | d | Skills | Kind | Pace | Family tag | Idea |", "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for i in ITEMS:
        out.append(f"| {i[0]} | {i[1]} {i[3].split('-')[0]} | {i[2]} | {i[4]} | {', '.join(i[5])} | {i[6]} | {i[7]} | `{i[8]}` | {i[9]} |")
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exam35_plan_table.md"), "w").write("\n".join(out) + "\n")
    print("PLAN OK")


if __name__ == "__main__":
    sys.exit(main())
