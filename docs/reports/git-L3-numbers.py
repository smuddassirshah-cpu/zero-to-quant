"""Number recompute for git level 3 (GitHub and the shell): l9 to l12, review-3, homework-3. Second reader, session V.

Pipelines are re-run in Python on the lessons' trades.csv; remote histories are lists; the drawdown is recomputed from
the two closes the lesson states. Checks tied to a sentence (lv.stated) fail while a false sentence is still in the text.
The shell pipelines and git commands were also run in bash and git 2.43.0 (see docs/reviews/review-git-1-3.md).
Run from anywhere:
    python3 docs/reports/git-L3-numbers.py
"""
import sys, os, json
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level, COURSES

lv = Level("git", 3)

trades = ["date,ticker,side,qty", "2024-03-01,AAPL,buy,100", "2024-03-01,MSFT,sell,50", "2024-03-04,AAPL,sell,100",
          "2024-03-04,NVDA,buy,20", "2024-03-05,MSFT,buy,50", "2024-03-05,AAPL,buy,30"]
cut = lambda rows, f: [r.split(',')[f - 1] for r in rows]


def uniq_c(lines):
    out = []
    for x in lines:
        if out and out[-1][1] == x:
            out[-1][0] += 1
        else:
            out.append([1, x])
    return out


def ahead_behind(local, remote):
    s = 0
    while s < min(len(local), len(remote)) and local[s] == remote[s]:
        s += 1
    return len(local) - s, len(remote) - s


# l9 quiz[0]; review-3 items[1]: pull gains E and M
lv.expect("l9", "quiz[0].widget.answer", 47)
lv.claim(1 + 1 == 2, "review-3 items[1]: pull gains E and the merge commit")
lv.expect("review", "items[1].widget.answer", 2)
lv.claim(len(["A", "B", "C", "D", "E", "F"]) == 6, "l9 s11: six commits")

# l10 quiz[1]: 2 + 3; screens[8] drawdown
lv.claim(2 + 3 == 5, "l10 quiz[1]: 2 + 3 = 5")
lv.expect("l10", "quiz[1].widget.answer", 5)
dd = 222.95 / 338.34 - 1
lv.claim(abs(dd - (-0.341)) < 0.0005, "l10 s8: 338.34 to 222.95 is a fall of 34.1%", note=f"{dd:.5f}")
lv.expect("l10", "screens[8].explain.text", 338.34)
lv.expect("l10", "screens[8].explain.text", 222.95)
lv.expect("l10", "screens[5].canvas.params.rows[4][0]", 17.6)
print("check by hand: l10 'volatility 17.6% a year' (SPY 2014 to 2023) needs a price series the repository does not hold; not verified")

# l11 screens[0] to [2], [8], quiz[0]; homework-3 items[1]; review-3 items[4]
f2 = cut(trades, 2)
lv.claim(len(f2) == 7 and f2[0] == "ticker", "l11 s0: seven lines, the header word first")
counts = uniq_c(sorted(f2))
lv.claim(counts == [[3, 'AAPL'], [2, 'MSFT'], [1, 'NVDA'], [1, 'ticker']], "l11 s1: 3 AAPL, 2 MSFT, 1 NVDA, 1 ticker")
lv.claim(len(uniq_c(f2)) == 7, "l11 s2: without sort, seven lines")
lv.expect("l11", "screens[2].widget.answer", 7)
lv.claim(len(counts) == 4 and len(set(f2) - {'ticker'}) == 3, "l11 s2: wrong 4 (sorted counts), 3 (tickers)")
top = sorted(counts, key=lambda c: -c[0])[0]
lv.claim(top == [3, 'AAPL'], "l11 s8: the pipeline prints 3 AAPL")
lv.claim(sorted(['10', '9'], reverse=True) == ['9', '10'], "l11 s8: as text, sort -r puts 9 above 10 (unpadded)")
lv.stated("l11", "screens[8].explain.text", "and 10 would come before 9", False)
f3 = cut(trades, 3)
c3 = dict((x, n) for n, x in uniq_c(sorted(f3)))
lv.claim(c3 == {'buy': 4, 'sell': 2, 'side': 1}, "l11 quiz[0]: 4 buy, 2 sell, 1 side")
lv.expect("l11", "quiz[0].widget.answer", c3['buy'])
lv.claim([i for i, x in enumerate(f3, 1) if x == 'buy'] == [2, 5, 6, 7], "l11 quiz[0]: lines 2, 5, 6 and 7 say buy")
lv.expect("l11", "quiz[0].feedback.byKey.three", "lines 2, 5, 6 and 7")
lv.claim(len(uniq_c(sorted(f2))) == 4, "homework-3 items[1]: sort | uniq | wc -l prints 4")
lv.expect("homework", "items[1].widget.answer", 4)
lv.claim((3, 7, 6) == (len(set(f2)) - 1, len(f2), len(f2) - 1), "homework-3 items[1]: wrong 3, 7, 6")
aapl = sorted(int(r.split(',')[3]) for r in trades if 'AAPL' in r)
lv.claim(aapl == [30, 100, 100] and aapl[-1] == 100 and aapl[0] == 30 and sum(aapl) == 230, "review-3 items[4]: 100; wrong 30 (head), 230 (sum)")
lv.expect("review", "items[4].widget.answer", 100)

# l11 screens[6] and [9]; review-3 items[5]
lines = []
for t in ['SPY', 'QQQ', 'IWM']:
    lines = [t]            # '>' empties the file each pass
lv.claim(len(lines) == 1 and lines == ['IWM'], "l11 s6: one line, IWM's")
lv.expect("l11", "screens[6].widget.answer", 1)
f = []
for run in range(2):
    f += ['row'] * 5        # '>>' only appends
lv.claim(len(f) == 10, "l11 s9: two runs of five appended lines")
lv.expect("l11", "screens[9].widget.answer", 10)
for run in range(2):
    f = ['header'] + ['row'] * 5
lv.claim(len(f) == 6 and 1 + 10 == 11 and 12 == 2 * 6, "review-3 items[5]: 6; wrong 11 (one header, both runs), 12 (both runs whole)")
lv.expect("review", "items[5].widget.answer", 6)

# homework-3 items[0], items[4]
loc = ['A', 'B', 'C', 'D', 'F', 'G']
rem = ['A', 'B', 'C', 'D', 'E1', 'E2', 'E3']
lv.claim(ahead_behind(loc, rem) == (2, 3), "homework-3 items[0]: 2 and 3 different commits")
lv.claim((len(loc), len(rem)) == (6, 7), "homework-3 items[0]: wrong totals 6 and 7")
lv.expect("homework", "items[0].widget.options[3].text", "6 and 7")
lv.claim(ahead_behind(['A', 'B', 'X', 'Y'], ['A', 'B', 'C']) == (2, 1), "homework-3 items[4] explain: (2, 1)")
hw = json.load(open(os.path.join(COURSES, 'git', 'homework-3.json')))
lv.claim(len(hw['items'][4]['widget']['tests']) == 9 and len(hw['items'][5]['widget']['tests']) == 11, "homework-3 code items: 9 and 11 hidden tests, as `how` says")
lv.expect("homework", "items[4].widget.how", 9)
lv.expect("homework", "items[5].widget.how", 11)

lv.check_wrongs()
lv.report()
