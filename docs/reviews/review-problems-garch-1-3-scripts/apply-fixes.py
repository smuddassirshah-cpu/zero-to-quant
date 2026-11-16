"""Apply the replacement texts of review-problems-garch-1-3.md to a scratch copy of the content.

Usage: python3 apply-fixes.py <repo root> <scratch>/content ; then from app/:
  node tools/fresh-check.mjs --content <scratch>/content --file <scratch>/content/courses/garch/problems-<n>.json
The two re-author findings (1 and 27) are not applied here."""
import json, os, shutil, sys, re
ROOT = sys.argv[1]            # repo root
OUT = sys.argv[2]             # a scratch folder, never inside the repo
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, 'courses'))
shutil.copytree(os.path.join(ROOT, 'app/content/courses/garch'), os.path.join(OUT, 'courses/garch'))
shutil.copytree(os.path.join(ROOT, 'app/content/exams'), os.path.join(OUT, 'exams'))
for f in ('manifest.json',):
    p = os.path.join(ROOT, 'app/content', f)
    if os.path.exists(p): shutil.copy(p, os.path.join(OUT, f))
S = {n: json.load(open(os.path.join(OUT, f'courses/garch/problems-{n}.json'))) for n in (1, 2, 3)}
P = lambda n, i, j: S[n]['items'][i]['parts'][j - 1]
def wrong(p, wid, val=None, text=None):
    for x in p['widget']['wrong']:
        if x['id'] == wid and val is not None: x['value'] = val
    if text is not None: p['feedback']['byKey'][wid] = text
R = {}
# ---- set 1
p = P(1, 1, 1)
p['question'] = "How far from zero must a bar of this correlogram sit to count as significant at 5%? Give 4 decimal places."
wrong(p, 'no-root', text="That is $1.96/1200$. The standard error of a bar is $1/\\sqrt{1200}$, so the root is missing.")
p = P(1, 1, 4)
p['feedback']['correct'] = "$21.20/19.05 = \\sqrt{312.24/252} = 1.113$: the true figure is about 11% above the reported one."
p['explain']['text'] = "Both volatilities share the factor $1.2\\%$, so the ratio is $\\sqrt{312.24/252} = 1.113$. The 251 neighbouring pairs add 23.9% to the year's variance, and the report leaves all of it out."
p = P(1, 2, 3)
p['widget'].update(answer=0.28336, tol={'abs': 0.00011}, accept="28.34%: $\\sqrt{252} \\times 1.785\\%$.")
p['feedback']['correct'] = "$\\sqrt{252} \\times 1.785\\% = 15.8745 \\times 1.785\\% = 28.34\\%$ a year."
wrong(p, 'calendar', text="You scaled by $\\sqrt{365}$, which gives 34.10%. Markets are open on about 252 days a year, so the factor is $\\sqrt{252}$.")
p['explain']['text'] = "A year holds 252 trading days, so the daily $1.785\\%$ is scaled by $\\sqrt{252} = 15.8745$. That gives $28.34\\%$ a year. Eight days make this a very rough figure."
p = P(1, 3, 4)
p['question'] = "Keep $LM = (n - 1)R^2$ from part 3, $p = 0.05$ and the 75 follow-on days. Chance alone would make $0.05 \\times 75 = 3.75$ of them big. What is the smallest count above that which rejects at 5% ($\\chi^2_1$ critical value 3.841)? Give a whole number."
# ---- set 2
P(2, 0, 3)['widget']['answer'] = 1.65365
p = P(2, 1, 1)
wrong(p, 'omega', text="6.0 is the variance after a week with no move at all. An average week has $r^2 = V$, so $V = 6.0 + 0.35V$ sits higher.")
P(2, 1, 3)['question'] = "This week's 12% fall puts next week's variance at $6.0 + 0.35 \\times 144$, far above the level $V = 9.23$ %² of part 1. What variance does the model expect for the week after next, in %²? Use $E[r^2] = \\sigma^2$. Give 2 decimal places."
P(2, 1, 5)['feedback']['generic'] = "Not quite. Three terms: 0.7385, then $0.12 \\times 144$, then $0.80 \\times 9.2308$."
p = P(2, 2, 2)
p['feedback']['generic'] = "Not quite. Find the number of days $h$ after which $0.96^h$ of a shock is one half."
wrong(p, 'mean-age', text="25 is $1/(1 - 0.96)$, the mean age of a shock. Half of it has gone sooner, after $\\ln 0.5/\\ln 0.96$ days.")
wrong(p, 'half-mean', text="12.5 is half of the 25-day average age. The decay is geometric, so $h = \\ln 0.5/\\ln 0.96$.")
p['explain']['text'] = "A variance shock keeps the fraction $0.96^h$ of itself after $h$ days. Setting that to one half gives $h = \\ln 0.5/\\ln 0.96 = 16.98$ days. So half of any excess variance is gone in about three and a half weeks."
p = P(2, 2, 4)
p['question'] = "The lag-1 ACF then points to $\\alpha = 0.13$, so $\\beta = 0.83$. Today's variance is 2.89 %² and today's return is $+4.5\\%$. Using $\\omega = 0.1156$ from part 3, what is tomorrow's daily volatility? Give a percentage to 2 decimal places."
p['widget'].update(answer=0.022687, accept="2.27%: $\\sqrt{5.1468}$.")
wrong(p, 'variance', 0.051468, "That is the variance, 5.1468 %². A volatility is its root.")
wrong(p, 'no-square', 0.017605, "You used $0.13 \\times 4.5$ rather than $0.13 \\times 4.5^2$. The model reacts to the squared move.")
wrong(p, 'annual', 0.360138)
p['feedback']['correct'] = "$0.1156 + 0.13 \\times 20.25 + 0.83 \\times 2.89 = 0.1156 + 2.6325 + 2.3987 = 5.1468$ %², so $\\sigma = 2.27\\%$."
p['explain']['text'] = "The $+4.5\\%$ day adds $0.13 \\times 20.25 = 2.6325$ of news to the carried $0.83 \\times 2.89$. With $\\omega$ the total is 5.1468 %², a daily volatility of $2.27\\%$. That is 33% above the long-run $1.70\\%$; the excess variance halves in about 17 days."
it = S[2]['items'][3]
it['prose'] = it['prose'].replace("Every day after that moves exactly 0.5%.", "Every day after that moves exactly 0.4%.")
assert '0.4%' in it['prose']
p = P(2, 3, 1)
wrong(p, 'swapped', text="That is $0.05 \\times 1.21 + 0.95 \\times 36$. The 36 is one day's news and takes the small weight, 0.05.")
p['explain']['text'] = "The squared fall, 36, is 30 times the estimate, but it gets only 5% weight. That adds 1.8 to the 1.1495 carried over. The estimate ends at 2.9495 %², about 2.4 times where it stood."
p = P(2, 3, 3)
p['question'] = "The next day moves 0.4%. Using 2.9495 from part 1, what is the EWMA variance for the day after that, in %²? Give 4 decimal places."
p['widget']['answer'] = 2.81
wrong(p, 'no-news', 2.802, "You decayed 2.9495 by 0.95 and stopped. The quiet day still adds $0.05 \\times 0.16$.")
wrong(p, 'abs', 2.822, "You added $0.05 \\times 0.4$. The filter takes the square, 0.16.")
wrong(p, 'decimal', 0.000281, "You gave it in decimals. In %² it is 2.8100.")
p['feedback']['correct'] = "$0.95 \\times 2.9495 + 0.05 \\times 0.16 = 2.8020 + 0.0080 = 2.8100$ %²."
p['feedback']['generic'] = "Not quite. Decay 2.9495 by 0.95, then add 5% of $0.4^2 = 0.16$."
p['explain']['text'] = "A 0.4% day squares to 0.16, well below the estimate, so the EWMA falls. It keeps 95% of 2.9495 and adds 0.0080, giving 2.8100. ARCH, meanwhile, drops at once to $0.8 + 0.45 \\times 0.16 = 0.872$."
p = P(2, 3, 4)
p['question'] = "On quiet days the EWMA after $k$ of them is $0.16 + 0.95^k(2.9495 - 0.16)$, using part 1's 2.9495. ARCH stays at 0.872. After how many quiet days is the EWMA first below 0.872? Give a whole number."
p['widget']['answer'] = 27
wrong(p, 'round-down', 26, "After 26 days the EWMA is still about 0.90, above 0.872. Round $26.6$ up.")
wrong(p, 'no-floor', 24, "24 is the count if the share did not move at all. On 0.4% days the EWMA settles at 0.16, so the gap to cross is $0.872 - 0.16$.")
p['feedback']['correct'] = "$0.95^k < (0.872 - 0.16)/(2.9495 - 0.16) = 0.2552$ needs $k > \\ln 0.2552/\\ln 0.95 = 26.6$, so 27 days."
p['feedback']['generic'] = "Not quite. Solve $0.16 + 0.95^k \\times 2.7895 < 0.872$ for the smallest whole $k$."
p['explain']['text'] = "The EWMA is pulled towards the quiet days' 0.16, and its excess shrinks by 0.95 a day. It needs $0.95^k$ below 0.2552, which first happens at $k = 27$. ARCH forgets the fall in one day; the EWMA still remembers it after five weeks of calm."
# ---- set 3
P(3, 0, 1)['question'] = "The screen hides $\\phi = \\alpha + \\beta$. What value of it fits all three forecasts? Give 2 decimal places."
p = P(3, 0, 3)
p['feedback']['generic'] = "Not quite. Day 30 is 29 steps past tomorrow: find what is left of the 0.2, put it on top of 0.49, and root the total."
wrong(p, 'power-30', text="That has the 0.2 fading 30 times. The first forecast, 0.69, is tomorrow's, so day 30 is only 29 fades on: $0.93^{29}$.")
wrong(p, 'no-long-run', text="$\\sqrt{0.0244}$ is the root of the faded gap alone. The forecast variance is $0.49 + 0.0244$.")
p = P(3, 0, 4)
p['question'] = "The desk holds an £8m dollar-yen position. Using 0.7172% from part 3 and $z = 2.3263$, what 99% normal VaR does that day-30 forecast give? Give your answer to the nearest £."
wrong(p, 'z95', text="£94,378 is the 95% figure, from 1.6449. The desk reports at 99%, where the multiplier is 2.3263.")
p['explain']['text'] = "Tomorrow's VaR is £154,590, so the forecast path takes the figure down by 14% to £133,474 over the month. Most of tonight's extra risk has gone by then."
p = P(3, 1, 1)
p['feedback']['generic'] = "Not quite. Tomorrow's variance has three parts: 0.06, the news $0.06 \\times 16$ and the carried $0.91 \\times 2.25$. Root their sum."
wrong(p, 'no-omega', text="That is $0.96 + 2.0475$ alone. The constant 0.06 belongs in the sum too.")
wrong(p, 'variance', text="3.0675 is in %². The weight in part 2 needs a volatility in %, $\\sqrt{3.0675}$.")
p = P(3, 1, 2)
p['feedback']['generic'] = "Not quite. Put the forecast on a yearly footing first, $1.7514\\% \\times \\sqrt{252}$, then compare it with the 11% target and the 1.25 cap."
wrong(p, 'daily', text="$11/1.7514$ is 6.28, which the cap would cut to 1.25. The 11% is a yearly figure and 1.7514% a daily one.")
wrong(p, 'times-252', text="$1.7514\\% \\times 252$ is 441% a year. Volatility scales with $\\sqrt{252}$, which gives 27.80%.")
p['feedback']['correct'] = "$1.7514\\% \\times \\sqrt{252} = 27.803\\%$ a year. The target is 11%, so $w = 11/27.803 = 0.3956$, well short of 1.25."
wrong(P(3, 1, 3), 'z95', text="£170,951 is the 95% figure, from 1.6449. This VaR is at 99%: 2.3263.")
p = P(3, 1, 4)
p['question'] = "Months later the fund has refitted its GARCH, and in a quiet market the new fit forecasts 0.50% a day for tomorrow. With the same target and cap, what is the fund's 99% VaR for tomorrow? Give your answer to the nearest £100."
p['widget']['answer'] = 218090.63
wrong(p, 'no-cap', text="You used the uncapped weight 1.39, which gives the flat £241,800 again. The cap holds the weight at 1.25.")
wrong(p, 'cap-1', 174472.5)
p['feedback']['correct'] = "$0.50\\% \\times \\sqrt{252} = 7.94\\%$, so $11/7.94 = 1.39$ and the cap holds $w = 1.25$. The VaR is $2.3263 \\times 1.25 \\times 0.50\\%$ of £15m, £218,091."
p['explain']['text'] = "Below a forecast of $11/(1.25\\sqrt{252}) = 0.5543$% a day the cap binds, and the VaR falls with the forecast, here to £218,091. So the flat VaR holds only on nights the cap leaves alone."
it = S[3]['items'][2]
old = "A short loses when the share rises, so its losing tail is the right one."
assert old in it['prose']
it['prose'] = it['prose'].replace(old, "The desk is hurt by rises in the share, so its VaR is a quantile of the upper tail.")
p = P(3, 2, 1)
p['feedback']['generic'] = "Not quite. Write $383\\ln(1 - p) + 17\\ln p$ at $p = 0.025$ and again at $\\hat p = 17/400$; LR is twice the difference."
wrong(p, 'half', text="2.084 is the gap between the two scores. LR is double that, 4.168.")
p['explain']['text'] = "A correct model expects 10 breaches here, not 17. LR is 4.168, above 3.841, so Kupiec rejects at 5%, with a p-value of 0.041. Too many breaches mean the forecasts run low."
P(3, 2, 3)['widget']['tol'] = {'abs': 5}
p = P(3, 2, 4)
p['widget']['tol'] = {'abs': 5}
wrong(p, 'no-divide', text="£2,294 is the density times the vol and the position. The mean loss in the tail divides that by the tail's size, 0.025.")
for n in S:
    json.dump(S[n], open(os.path.join(OUT, f'courses/garch/problems-{n}.json'), 'w'), ensure_ascii=False, indent=2)
print('patched copy at', OUT)
