"""Number recompute for git level 1 (Commits): l1 to l4, review-1, homework-1. Second reader, session V.

Every graded key, every numeric wrong[] value and the counts stated in prose, hints, feedback and explanations are
recomputed here from small models (commit lists, staged sets, diff hunks). Checks tied to a sentence (lv.stated) fail
while a false sentence is still in the text and pass once the fix rewords it. The git behaviour behind each model was
also run in throwaway repositories with git 2.43.0 (see docs/reviews/review-git-1-3.md). Run from anywhere:
    python3 docs/reports/git-L1-numbers.py
Failing checks on the current content are findings in docs/reviews/review-git-1-3.md.
"""
import sys, os, re, json, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level, COURSES

lv = Level("git", 1)


def commits_made(steps):
    """Each step is 'add', 'save' or 'commit'. A commit succeeds only when something is staged."""
    staged, made = False, 0
    for s in steps:
        if s == 'add':
            staged = True
        elif s == 'commit' and staged:
            made, staged = made + 1, False
    return made


def hunk(lines):
    """lines: list of (mark, text). Returns (old count, new count) as a @@ header counts them."""
    old = sum(1 for m, _ in lines if m in ' -')
    new = sum(1 for m, _ in lines if m in ' +')
    return old, new


# l1 screens[2]: the first broken snapshot
vals = [0.04, 0.04, 0.05, 0.05, -3.1, -3.1]
first_bad = next(i for i, v in enumerate(vals, 1) if v < 0)
lv.claim(first_bad == 5, "l1 s2: snapshot 5 is the first broken one")
lv.expect("l1", "screens[2].widget.answer", "m5")
lv.expect("l1", "screens[2].hints[2].text", 5)
lv.expect("l1", "screens[2].feedback.byKey.m4", 0.05)
lv.expect("l1", "screens[2].feedback.byKey.m1", 0.04)
lv.expect("l1", "screens[1].prose", -3.10, fmt="−3.10%")

# l1 screens[6]: last good 2, broken 6: suspects 3..6; testing 4 splits them 2 and 2
sus = list(range(2 + 1, 6 + 1))
lv.claim(sus == [3, 4, 5, 6], "l1 s6: suspects are 3, 4, 5, 6")
lv.claim(len([c for c in sus if c <= 4]) == len([c for c in sus if c > 4]) == 2, "l1 s6: running commit 4 splits the suspects in two")

# l1 screens[9]: the jump commit and the cost drop
rows = [("a13f5e2", None), ("2f0c6d8", 0.62), ("71ad3be", 0.48), ("e52f9c1", 2.91), ("4b8d0a3", 2.91), ("9c1e2f7", 2.91)]
jump = next(h for h, s in rows if s == 2.91)
lv.claim(jump == "e52f9c1", "l1 s9: the Sharpe ratio first reads 2.91 at e52f9c1")
lv.expect("l1", "screens[9].hints[2].text", 0.48)
lv.expect("l1", "screens[9].feedback.byKey.r2c0", 0.62)
lv.expect("l1", "screens[9].feedback.correct", 2.91)

# l1 quiz[0]: commit, five saves, commit
steps = ['add', 'commit'] + ['save'] * 5 + ['add', 'commit']
lv.claim(commits_made(steps) == 2, "l1 quiz[0]: two snapshots")
lv.expect("l1", "quiz[0].widget.answer", 2)
lv.claim(5 + 2 == 7 and 5 + 1 == 6, "l1 quiz[0]: wrong values 7 (saves and commits), 6 (saves and one commit)")
lv.expect("l1", "quiz[0].widget.wrong[0].value", 7)
lv.expect("l1", "quiz[0].widget.wrong[2].value", 6)
lv.claim(5 - 1 == 4, "l1 quiz[0] explain: of five saves, four are lost and the fifth is committed")
lv.expect("l1", "quiz[0].explain.text", "four saves")

# l2 quiz[2]: add, commit, commit
lv.claim(commits_made(['add', 'commit', 'commit']) == 1, "l2 quiz[2]: one new commit")
lv.expect("l2", "quiz[2].widget.answer", 1)

# l3 screens[9]
lv.expect("l3", "screens[9].prose", 1.10)
lv.expect("l3", "screens[9].prose", 0.40)

# l4 screens[3], screens[4], quiz[1]: hunk headers
s3 = [(' ', 'signal'), ('-', 'shift'), ('+', 'noshift'), (' ', 'pnl')]
lv.claim(hunk(s3) == (3, 3), "l4 s3: @@ -12,3 +12,3 @@ counts the lines shown")
lv.expect("l4", "screens[3].canvas.params.rows[0][1]", "@@ -12,3 +12,3 @@")
s4 = [('-', 'r20'), ('+', 'r50'), (' ', 'position')]
lv.claim(hunk(s4) == (2, 2), "l4 s4: @@ -12,2 +12,2 @@ counts the lines shown")
lv.claim(sum(1 for m, _ in s4 if m == '-') == 1, "l4 s4: one line edited")
lv.expect("l4", "screens[4].widget.answer", 1)
lv.claim(len([m for m, _ in s4 if m != ' ']) == 2 and len(s4) == 3, "l4 s4: wrong values 2 (marked lines) and 3 (all lines)")
q1 = [(' ', 'window'), ('-', 'fee5'), ('+', 'fee10'), ('+', 'slip'), (' ', 'start')]
lv.claim(hunk(q1) == (3, 4), "l4 quiz[1]: @@ -3,3 +3,4 @@")
lv.expect("l4", "quiz[1].widget.answer", hunk(q1)[1])
lv.claim(len(q1) == 5, "l4 quiz[1]: wrong 5 counts every line, the minus line included")
lv.expect("l4", "quiz[1].explain.text", "2 + 2 = 4")

# review-1 items[0] (finding 31): good on 1, broken on 16: suspects 2..16 (15). Each run keeps at most ceil(n/2).
n, steps_, seq = 15, 0, [15]
while n > 1:
    n, steps_ = math.ceil(n / 2), steps_ + 1
    seq.append(n)
lv.claim(len(range(2, 16 + 1)) == 15, "review-1 items[0]: 15 suspects, commits 2 to 16")
lv.claim(seq == [15, 8, 4, 2, 1] and steps_ == 4 == math.ceil(math.log2(15)), "review-1 items[0]: 15, 8, 4, 2, 1 is four runs")
lv.expect("review", "items[0].widget.answer", 4)
lv.expect("review", "items[0].explain.text", "15, 8, 4, 2, 1")
lv.expect("review", "items[0].widget.wrong[0].value", 15)
lv.claim(len(range(2, 15 + 1)) == 14, "review-1 items[0]: wrong 'between' counts commits 2 to 15, 14")
lv.expect("review", "items[0].widget.wrong[1].value", 14)

# review-1 items[5] (finding 32): the staged hunk has 3 old and 3 new lines, and the key is not the longest option
r5 = [(' ', 'prices'), ('-', 'w20'), ('+', 'w60'), (' ', 'signal')]
lv.claim(hunk(r5) == (3, 3), "review-1 items[5]: @@ -4,3 +4,3 @@")
lv.expect("review", "items[5].prose", "@@ -4,3 +4,3 @@")
opts5 = get_opts = json.load(open(os.path.join(COURSES, 'git', 'review-1.json')))['items'][5]['widget']['options']
lens5 = {o['id']: len(o['text']) for o in opts5}
lv.claim(lens5['good'] == 45 and lens5['more'] == 38 and lens5['good'] > lens5['more'], "review-1 items[5]: key 45 characters against 38", note=str(lens5))

# review-1 items[3]: the hunk and the cost
r3 = [(' ', 'pnl'), ('-', 'old'), ('+', 'cost'), ('+', 'pnl2'), (' ', 'equity')]
lv.claim(hunk(r3) == (3, 4), "review-1 items[3]: @@ -20,3 +20,4 @@")
lv.claim(round(0.0005 * 1e4) == 5 and round(0.0010 * 1e4) == 10, "review-1 items[3]: 0.0005 is 5 bp, 0.0010 is 10 bp")
lv.expect("review", "items[3].explain.text", "5 bp to 10 bp")

# review-1 items[7] (finding 33): add a b, restore --staged b, commit One, commit Two, add b, commit Three
def commits_sets(steps):
    staged, made, log = set(), 0, []
    for op, arg in steps:
        if op == 'add':
            staged |= set(arg)
        elif op == 'unstage':
            staged -= set(arg)
        elif op == 'commit':
            if staged:
                made += 1
                log.append((arg, sorted(staged)))
                staged = set()
            else:
                log.append((arg, None))
    return made, log


made7, log7 = commits_sets([('add', 'ab'), ('unstage', 'b'), ('commit', 'One'), ('commit', 'Two'), ('add', 'b'), ('commit', 'Three')])
lv.claim(made7 == 2, "review-1 items[7]: two new commits")
lv.claim(log7 == [('One', ['a']), ('Two', None), ('Three', ['b'])], "review-1 items[7]: One takes a.py, Two is refused, Three takes b.py")
lv.expect("review", "items[7].widget.answer", 2)

# homework-1 items[2]: init, add, A, save, B, add, C, checkout A -- file (stages it), D
lv.claim(commits_made(['add', 'commit', 'save', 'commit', 'add', 'commit', 'add', 'commit']) == 3, "homework-1 items[2]: A, C and D")
lv.expect("homework", "items[2].widget.answer", 3)

# homework-1 items[4]: log newest first, read upwards
log = [("d93a1f0", 2.40), ("7be22c5", 2.40), ("41f0e8a", 2.40), ("c08d7b3", 0.70), ("5a91e44", 0.85)]
up = list(reversed(log))
first = next(h for h, s in up if s == 2.40)
lv.claim(first == "41f0e8a", "homework-1 items[4]: 41f0e8a is the first 2.40 in time order")
lv.expect("homework", "items[4].explain.text", 0.85)
lv.expect("homework", "items[4].explain.text", 0.70, fmt="0.70")
lv.stated("homework", "items[4].canvas.params.rows[0][0]", "HEAD →", False)   # git prints "HEAD -> main" (finding 3, fixed)
lv.claim_text("homework", "items[4].canvas.params.rows[0][0]", "(HEAD -> main)", "(HEAD -> main)" in lv.text("homework", "items[4].canvas.params.rows[0][0]"), "homework-1 items[4]: HEAD -> main with an ASCII arrow")

# homework-1 items[6]: the code item's stated test count
hw = json.load(open(os.path.join(COURSES, 'git', 'homework-1.json')))
lv.claim(len(hw['items'][6]['widget']['tests']) == 11, "homework-1 items[6]: 11 hidden tests, as `how` says")
lv.expect("homework", "items[6].widget.how", 11)

# Course-wide: a hash names one commit, so it must carry one message (finding: l4 reuses l1's hashes)
msgs = {}
for f in sorted(os.listdir(os.path.join(COURSES, 'git'))):
    if not f.endswith('.json') or f == 'course.json':
        continue
    d = json.load(open(os.path.join(COURSES, 'git', f)))
    def rows_of(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k == 'rows' and isinstance(v, list):
                    yield v
                yield from rows_of(v)
        elif isinstance(x, list):
            for v in x:
                yield from rows_of(v)
    for rows in rows_of(d):
        for r in rows:
            cells = r if isinstance(r, list) else [r]
            line = ' '.join(str(c) for c in cells)
            m = re.match(r'^([0-9a-f]{7})\s+(?:\([^)]*\)\s*)?(.+)$', line)
            if m and re.search(r'\d', m.group(1)):
                msg = re.sub(r'\s+[-–\d.]+$', '', m.group(2)).strip()
                msgs.setdefault(m.group(1), set()).add(msg)
clash = {h: s for h, s in msgs.items() if len(s) > 1}
lv.claim(not clash, "every hash in the course names one commit message", note='; '.join(f"{h}: {sorted(s)}" for h, s in sorted(clash.items())))

lv.check_wrongs()
lv.report()
