"""Number recompute for git level 2 (Branches): l5 to l8, review-2, homework-2. Second reader, session V.

Commit graphs are modelled as parent maps; "contains" is reachability, a merge is a fast-forward when the receiving
tip is an ancestor of the other. Every graded key, numeric wrong[] value and stated count is recomputed. Checks tied to a
sentence (lv.stated) fail while a false sentence is still in the text. The git behaviour behind each model was also run
with git 2.43.0 (see docs/reviews/review-git-1-3.md). Run from anywhere:
    python3 docs/reports/git-L2-numbers.py
"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level, COURSES

lv = Level("git", 2)


def reach(parents, tip):
    seen, todo = set(), [tip]
    while todo:
        c = todo.pop()
        if c not in seen:
            seen.add(c)
            todo.extend(parents[c])
    return seen


def chain(n, prefix='c'):
    return {f"{prefix}{i}": ([f"{prefix}{i-1}"] if i > 1 else []) for i in range(1, n + 1)}


def merge(parents, cur, other, name='m'):
    """Return (new parents, new tip of cur, commits added to cur's history)."""
    before = reach(parents, cur)
    if other in before:
        return parents, cur, 0
    if cur in reach(parents, other):
        return parents, other, len(reach(parents, other) - before)
    p = dict(parents); p[name] = [cur, other]
    return p, name, len(reach(p, name) - before)


def tilde(parents, tip, k):
    for _ in range(k):
        tip = parents[tip][0]
    return tip


# l5 quiz[0]: main at c3, two commits on fast-ma
p = chain(3); p.update({'f1': ['c3'], 'f2': ['f1']})
lv.claim(len(reach(p, 'c3')) == 3, "l5 quiz[0]: main contains 3")
lv.expect("l5", "quiz[0].widget.answer", 3)
lv.claim(len(reach(p, 'f2')) == 5, "l5 quiz[0]: wrong 5 counts fast-ma's history")
lv.expect("l5", "quiz[0].widget.wrong[0].value", 5)
# l5 screens[3]: main at c4 contains c1..c4; experiment at c6 contains six
p = chain(6)
lv.claim(reach(p, 'c4') == {'c1', 'c2', 'c3', 'c4'} and len(reach(p, 'c6')) == 6, "l5 s3: main c1..c4, experiment all six")
# l5 screens[5] and quiz[2]: a loose ref is 40 hex digits and a newline
lv.claim(40 + 1 == 41, "l5 s5, quiz[2]: a loose SHA-1 ref file is 41 bytes (packed after git gc; see the review)")

# l6 screens[0]: fast-forward; screens[1]: sliding to c5 loses c3; screens[2]: merge commit contains all six
p = {'c1': [], 'c2': ['c1'], 'c3': ['c2'], 'c4': ['c3']}
_, tip, added = merge(p, 'c2', 'c4')
lv.claim(tip == 'c4' and added == 2, "l6 s0: fast-forward main from c2 to c4")
p = {'c1': [], 'c2': ['c1'], 'c3': ['c2'], 'c4': ['c2'], 'c5': ['c4']}
lv.claim(reach(p, 'c5') == {'c1', 'c2', 'c4', 'c5'}, "l6 s1: c5 reaches c1, c2, c4, c5 and not c3")
p2, tip, added = merge(p, 'c3', 'c5')
lv.claim(tip == 'm' and len(reach(p2, 'm')) == 6, "l6 s2: m contains all six")
lv.claim(merge(p2, 'm', 'c5')[2] == 0, "l6 s3: merging again adds nothing (Already up to date.)")
# l6 screens[8]: main 4 commits, branch 3, one fix on main, merge
p = chain(4); p.update({'f': ['c4'], 'b1': ['c4'], 'b2': ['b1'], 'b3': ['b2']})
p2, tip, _ = merge(p, 'f', 'b3')
n = len(reach(p2, tip))
lv.claim(n == 9, "l6 s8: 4 + 1 + 3 + 1 = 9")
lv.expect("l6", "screens[8].widget.answer", n)
lv.claim(n - 1 == 8, "l6 s8: wrong 8 leaves out the merge commit")
lv.claim(4 + 1 + 1 == 6, "l6 s8: wrong 6 counts the branch as one commit")
lv.claim(4 + 3 == 7 and 9 - 7 == 2, "l6 s8: wrong 7 is 4 + 3, so it leaves out both the fix and the merge commit")
lv.stated("l6", "screens[8].feedback.byKey.branch-only", "You left out the colleague's fix or the merge commit", False)
# l6 quiz[0]: fast-forward adds 2; quiz[3]: two parents
p = chain(3); p.update({'k1': ['c3'], 'k2': ['k1']})
lv.claim(merge(p, 'c3', 'k2')[2] == 2, "l6 quiz[0]: a fast-forward gains 2")
lv.expect("l6", "quiz[0].widget.answer", 2)
lv.expect("l6", "quiz[3].widget.answer", 2)

# l7 screens[1]: 7 lines, 3 markers, 4 lines of code
lines = ['ticker = "SPY"', '<<<<<<< HEAD', 'lookback = 30', '=======', 'lookback = 60', '>>>>>>> experiment', 'cost_bps = 5']
markers = [l for l in lines if l.startswith(('<<<<<<<', '=======', '>>>>>>>'))]
lv.claim(len(markers) == 3 and len(lines) - len(markers) == 4, "l7 s1: three marker lines, four lines you wrote")
lv.expect("l7", "screens[1].prose", "four of these lines")
# l7 quiz[1]: 2 dividers, 6 marker lines, 4 halves
lv.claim((2, 2 * 3, 2 * 2) == (2, 6, 4), "l7 quiz[1]: 2 conflicts, 6 marker lines, 4 halves")
lv.expect("l7", "quiz[1].widget.answer", 2)
lv.expect("l7", "quiz[1].widget.wrong[0].value", 6)
lv.expect("l7", "quiz[1].widget.wrong[1].value", 4)
# l7 screens[5] and review-2 items[5]: edits clash when the line ranges touch (no unchanged line between)
clash = lambda a, b: abs(a - b) <= 1
lv.claim(not clash(1, 3), "l7 s5: lines 1 and 3 merge cleanly")
lv.claim(clash(3, 3) and clash(3, 4) and not clash(2, 5), "review-2 items[5]: 3/3 and 3/4 clash; 2/5 merge cleanly")
lv.claim(clash(2, 3), "l7 s8: lookback (line 2) and cost_bps (line 3) touch, so one conflict")

# l8: HEAD~k
p = chain(5)
lv.claim(tilde(p, 'c5', 2) == 'c3' and tilde(p, 'c5', 1) == 'c4', "l8 s3: HEAD~2 from c5 is c3")
p = chain(7)
lv.claim(tilde(p, 'c7', 3) == 'c4' and tilde(p, 'c7', 2) == 'c5' and tilde(p, 'c7', 4) == 'c3', "l8 quiz[0]: HEAD~3 from c7 is c4")
# l8 quiz[2]: revert adds one commit
lv.claim(4 + 1 == 5, "l8 quiz[2]: 4 + 1 = 5")
lv.expect("l8", "quiz[2].widget.answer", 5)
lv.expect("l8", "quiz[2].feedback.correct", "4 + 1")

# review-2 items[1], items[2], items[3], items[4]
p = chain(6)
lv.claim(len(reach(p, 'c3')) == 3, "review-2 items[1]: main contains 3")
lv.expect("review", "items[1].widget.answer", 3)
p = {'c1': [], 'c2': ['c1'], 'c3': ['c2'], 'c4': ['c3'], 'c5': ['c2'], 'c6': ['c5']}
p2, tip, _ = merge(p, 'c4', 'c6')
lv.claim(tip == 'm' and p2['m'] == ['c4', 'c6'], "review-2 items[2]: merge commit with parents c4 and c6")
lv.claim(len(['41c09d8', '0be7c55', 'c2a91f4']) == 3, "review-2 items[3]: three commits in the right-hand lane")
lv.expect("review", "items[3].widget.answer", 3)
lv.claim(3 + 1 == 4 and 6 == len(['7f3e1a2', '41c09d8', '0be7c55', 'c2a91f4', '9d6b310', '5e8a0c1']), "review-2 items[3]: wrong 4 adds the merge, 6 counts every star")
lv.claim(2 + 3 == 5, "review-2 items[4]: '5, the two added'")
# review-2 items[7]: carry at c3, main at c4; ff carry, reset main
p = chain(4)
_, tip, _ = merge(p, 'c3', 'c4')
lv.claim(tip == 'c4' and tilde(p, 'c4', 1) == 'c3', "review-2 items[7]: carry fast-forwards to c4, main resets to c3")

# homework-2 items[1]: main 6, signal-a 2 and signal-b 3 from main's tip; merge a then b
p = chain(6); p.update({'a1': ['c6'], 'a2': ['a1'], 'b1': ['c6'], 'b2': ['b1'], 'b3': ['b2']})
p2, tip, _ = merge(p, 'c6', 'a2')
lv.claim(tip == 'a2', "homework-2 items[1]: the first merge is a fast-forward")
p3, tip, _ = merge(p2, 'a2', 'b3')
n = len(reach(p3, tip))
lv.claim(n == 12, "homework-2 items[1]: 6 + 2 + 3 + 1 = 12")
lv.expect("homework", "items[1].widget.answer", n)
lv.claim((n + 1, n - 1, 6 + 3) == (13, 11, 9), "homework-2 items[1]: wrong 13 (two merges), 11 (no merge), 9 (one branch)")
lv.expect("homework", "items[1].explain.text", 8)
# homework-2 code items: stated test counts
hw = json.load(open(os.path.join(COURSES, 'git', 'homework-2.json')))
lv.claim(len(hw['items'][4]['widget']['tests']) == 8 and len(hw['items'][5]['widget']['tests']) == 8, "homework-2 items[4] and [5]: 8 hidden tests each, as `how` says")
lv.expect("homework", "items[4].widget.how", 8)
lv.expect("homework", "items[5].widget.how", 8)
lv.claim(len(reach(chain(500), 'c500')) == 500, "homework-2 items[4] test 7: 500 commits")

lv.check_wrongs()
lv.report()
