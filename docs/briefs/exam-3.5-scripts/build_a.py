"""Items of topic-3.5, part A: the research-int items (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11).
build.py imports ITEMS_A, ITEMS_B, ITEMS_C and writes app/content/exams/topic-3.5.json.
"""
from helpers import *

I = {}

# ---------------------------------------------------------------- 1 two-regressions
I[1] = item(
    "e-two-slopes", 2, ["rq-stats"], ["two-regressions"], 60,
    title="Two regressions, one correlation",
    prose="A study fits two regressions on the same ten pairs of returns. Regressing $y$ on $x$ gives a slope of 0.75. Regressing $x$ on $y$ gives a slope of 0.27.",
    question="What is the correlation of $x$ and $y$?",
    widget=numeric(0.45, abs_=0.0005, placeholder="a decimal", label="Correlation",
                   wrong=[("r-squared", 0.2025, 0.0005), ("mean-slopes", 0.51, 0.0005), ("one-slope", 0.75, 0.0005)],
                   accept="0.45 within 0.0005"),
    feedback=fb("The slopes multiply to $r^2 = 0.2025$, so $r = 0.45$.",
                "Multiply the two slopes, then take the square root.",
                {"r-squared": "You stopped at the product of the slopes. That is $r^2$. Take its square root.",
                 "mean-slopes": "You averaged the slopes. The correlation is their geometric mean, not the arithmetic one.",
                 "one-slope": "You gave one slope. A slope equals $r$ only when both spreads are equal."}),
    explain="The two slopes multiply to $r^2$: $0.75 \\times 0.27 = 0.2025$. The square root, with the sign of the slopes, gives $r = 0.45$.")

# ---------------------------------------------------------------- 2 correlation-limits
I[2] = item(
    "e-third-correlation", 3, ["rq-stats", "rq-linalg"], ["correlation-limits"], 120,
    title="How high can the third correlation go",
    prose="Three assets, A, B and C. The correlation of A with B is 0.8. The correlation of B with C is $-0.5$.",
    question="What is the largest correlation that A and C can have? Give it to 3 decimal places.",
    widget=numeric(0.1196, abs_=0.0006, placeholder="a decimal", label="Largest correlation",
                   wrong=[("product", -0.4, 0.0006), ("half-width", 0.5196, 0.0006), ("floor", -0.9196, 0.0006)],
                   accept="0.120 within 0.0006"),
    feedback=fb("The range is $-0.4 \\pm 0.5196$, so the top is 0.1196.",
                "Use the product of the two correlations, then add the half-width from the determinant.",
                {"product": "You gave the centre of the range, $0.8 \\times (-0.5)$. Add the half-width to reach the top.",
                 "half-width": "You gave the half-width alone. Add it to the centre, $-0.4$.",
                 "floor": "You subtracted the half-width. That is the lowest value, not the highest."}),
    explain="The correlation matrix must be positive semidefinite, so its determinant is at least zero. That gives $\\rho_{AC} = \\rho_{AB}\\rho_{BC} \\pm \\sqrt{(1-\\rho_{AB}^2)(1-\\rho_{BC}^2)}$. Here it is $-0.4 \\pm 0.5196$, so the top is 0.1196.")

# ---------------------------------------------------------------- 3 corrected threshold
I[3] = item(
    "e-eight-looks", 2, ["rq-stats"], ["p-value-meaning"], 60,
    title="The best of eight signals",
    prose="You test eight candidate signals on the same history. The best has $p = 0.011$. You want the chance of any false positive across all eight to stay at 5%.",
    question="What do you say about the best signal?",
    widget=choice([
        ("a", "No. It must beat $0.05/8 = 0.00625$, and 0.011 does not.", True, None),
        ("b", "Yes. 0.011 is below 0.05, so it passes the test.", False,
         "You compared with 0.05 as if you had tried one signal. Eight looks need a stricter bar."),
        ("c", "No. There is only a 1.1% chance that the signal is real.", False,
         "You read $p$ as the chance the signal is real. It is the chance of a result this extreme if there is no effect."),
        ("d", "It cannot be judged until you see the other seven $p$-values.", False,
         "The Bonferroni bar depends only on how many tests you ran, not on the other results."),
    ]),
    feedback=fb("Each of eight tests must clear $0.05/8 = 0.00625$. The $p$ of 0.011 does not.",
                "Divide the 5% by the number of signals you tried."),
    explain="With eight looks, each test must beat $0.05/8 = 0.00625$ to keep the chance of any false positive at 5%. The best $p$ of 0.011 does not. The same test in another form: the corrected $p$ is $8 \\times 0.011 = 0.088$, above 0.05.")

# ---------------------------------------------------------------- 4 special eigenvalues
I[4] = item(
    "e-rank-one-det", 3, ["rq-linalg"], ["special-eigenvalues"], 120,
    title="A determinant without expanding",
    prose="Let $w = (1, 2, 2, 4)^\\top$ and $A = 2I + 3ww^\\top$, a 4 by 4 matrix.",
    question="What is $\\det A$?",
    widget=numeric(616, abs_=0, placeholder="a whole number", label="Determinant",
                   wrong=[("no-identity", 600, 0), ("all-fours", 1232, 0), ("one-eigenvalue", 77, 0)],
                   accept="616"),
    feedback=fb("The eigenvalues are 77, 2, 2 and 2, and their product is 616.",
                "Find the eigenvalue along $w$, then count the others.",
                {"no-identity": "You gave $8 \\times 75$. The eigenvalue along $w$ is $2 + 75 = 77$, since the $2I$ adds to it.",
                 "all-fours": "You used $2^4 \\times 77$. Only three eigenvalues equal 2. The fourth is 77.",
                 "one-eigenvalue": "You gave the largest eigenvalue. The determinant is the product of all four."}),
    explain="The matrix $ww^\\top$ has rank one, with eigenvalue $w^\\top w = 25$ along $w$ and 0 on the other three directions. So $A$ has eigenvalues $2 + 3 \\times 25 = 77$ and $2, 2, 2$. The determinant is $77 \\times 2^3 = 616$.")

# ---------------------------------------------------------------- 5 ridge and lasso as lambda grows
I[5] = item(
    "e-penalty-limit", 3, ["rq-ml"], ["ridge-lasso"], 120,
    title="Raise the penalty without limit",
    prose="A spread averages 40 ticks. You standardise four features. You fit a ridge and a lasso, each with a constant that the penalty leaves alone. Then you raise $\\lambda$ without limit.",
    question="What do the two models forecast in the end?",
    widget=choice([
        ("a", "40 for every row. The lasso gets there at a finite $\\lambda$. Ridge only approaches it.", True, None),
        ("b", "0 for every row, because a huge penalty sends every coefficient to zero.", False,
         "You penalised the constant too. Here it is left alone, so it keeps the target's average of 40."),
        ("c", "40 from ridge but 0 from the lasso, since only the lasso has exact zeros.", False,
         "Exact zeros apply to the slopes. The constant stays at 40 in both models."),
        ("d", "40 from the lasso, but ridge never gets near it, because its slopes stay non-zero.", False,
         "Ridge slopes stay non-zero but shrink towards zero, so its forecast tends to 40 without reaching it."),
    ]),
    feedback=fb("With the slopes gone, only the constant is left, and it equals the average of 40.",
                "Ask what each penalty does to the slopes, and what is left when they vanish."),
    explain="The constant is outside the penalty, so it settles at the target's mean, 40. The lasso sets every slope to exactly zero once $\\lambda$ passes a finite limit. Ridge slopes only shrink towards zero, so its forecast tends to 40 without reaching it.")

# ---------------------------------------------------------------- 6 pca share
I[6] = item(
    "e-first-component", 3, ["rq-ml", "rq-linalg"], ["pca-share"], 120,
    title="Share of the first component",
    prose="Two assets have the covariance matrix $\\Sigma = \\begin{pmatrix} 7 & 2 \\\\ 2 & 4 \\end{pmatrix}$, in squared per cent.",
    question="What share of the total variance does the first principal component carry?",
    widget=numeric(0.7273, abs_=0.0005, unit="%", placeholder="a percentage", label="Share of variance",
                   wrong=[("larger-asset", 0.6364, 0.0005), ("second-component", 0.2727, 0.0005), ("half", 0.5, 0.0005)],
                   accept="72.7% within 0.05"),
    feedback=fb("The eigenvalues are 8 and 3, so the first carries $8/11 = 72.7\\%$.",
                "Find the eigenvalues from the trace and the determinant, then divide the larger by the trace.",
                {"larger-asset": "You gave the larger asset's share of variance, $7/11$. The component mixes both assets and carries more.",
                 "second-component": "You gave the second component's share, $3/11$. The first carries the rest.",
                 "half": "You assumed two components split the variance evenly. The eigenvalues are 8 and 3."}),
    explain="The trace is 11 and the determinant is $7 \\times 4 - 2^2 = 24$, so $\\lambda^2 - 11\\lambda + 24 = 0$ and $\\lambda = 8$ or 3. The first component carries $8/11 = 72.7\\%$ of the variance.")

# ---------------------------------------------------------------- 7 weak signals (multi)
I[7] = item(
    "e-weak-signal-claims", 4, ["rq-ml"], ["weak-signal-traps"], 210,
    title="Claims about a weak signal",
    prose="A researcher tests a daily signal on a liquid futures contract. Its correlation with the next day's return is 0.04 over 2,500 days.",
    question="Select all that apply. Which of these statements hold?",
    widget=multi([
        ("a", "The $t$-statistic is about 2, so the evidence is borderline.", True, None),
        ("b", "A correlation of 0.02 would need about 10,000 days to reach the same $t$-statistic.", True, None),
        ("c", "A gross edge of 4 basis points a trade is lost to costs of 5 basis points a round trip.", True, None),
        ("d", "Doubling the sample halves the standard error of the correlation.", False,
         "You halved it. The standard error falls with $\\sqrt{n}$, so doubling the data cuts it by $\\sqrt{2}$ only."),
        ("e", "A 21-day centred moving average of price is a safe feature, since it is smooth.", False,
         "A centred window holds 10 future days. The feature uses information that does not exist at the forecast time."),
        ("f", "A signal that held from 2010 to 2015 will hold in the next five years, since markets are stable.", False,
         "You assumed the regime stays put. Relationships drift, so test on later data and expect some decay."),
    ]),
    feedback=fb("Statements a, b and c hold. The other three miss the square root, a leak and a regime change.",
                "Check each statement with a number, a timestamp or a later period."),
    explain="The $t$-statistic is about $r\\sqrt{n} = 0.04 \\times 50 = 2$, and halving $r$ needs four times the days, so 0.02 needs 10,000. Costs larger than the gross edge leave a loss. A centred window leaks the future, and a regime can change.")

# ---------------------------------------------------------------- 8 case steps (order)
I[8] = item(
    "e-weekly-hit-case", 3, ["rq-case"], ["case-steps"], 150,
    title="Beat the index next week",
    prose="An interviewer asks: \"Will a given stock beat the index next week?\" You answer with a case plan.",
    question="Put the steps in order. Leave out the two that do not belong.",
    widget=order([
        ("s1", "Define the label: the stock's return beats the index's over the next five days", None),
        ("s2", "Find the baseline hit rate by always guessing the more common label", None),
        ("s3", "Split by date, leaving a gap of five days between train and test", None),
        ("s4", "Build features known at each Friday's close", None),
        ("s5", "Fit a simple model and compare its hit rate with the baseline", None),
        ("s6", "Report the gap with an interval and the weeks where it fails", None),
        ("x1", "Shuffle the weeks so train and test look alike", "Shuffling puts later weeks in training, so the test score is better than the future will be."),
        ("x2", "Tune the model on the test weeks until it beats the baseline", "Tuning on the test weeks uses them up. The reported hit rate is then too high."),
    ], ["s1", "s2", "s3", "s4", "s5", "s6"], ["x1", "x2"]),
    feedback=fb("Define the label, set the baseline, split with a gap, build features, fit, then report.",
                "A label that looks five days ahead overlaps its neighbours, so the split needs a gap."),
    explain="The label looks five days ahead, so train and test weeks overlap unless a gap separates them. The baseline comes before any model, so the model has something to beat. Report the gap with its uncertainty.")

# ---------------------------------------------------------------- 9 baseline first
I[9] = item(
    "e-persistence-gain", 4, ["rq-case", "rq-ml"], ["baseline-first"], 180,
    title="Three forecasts of a mean-reverting spread",
    prose="A spread has mean 0, variance 4 and a day-to-day autocorrelation of 0.6. We compare three forecasts of tomorrow's value: today's value, the mean 0, and the fitted $0.6 \\times$ today's value.",
    question="By what percentage does the fitted forecast cut the mean squared error of the persistence forecast?",
    widget=numeric(0.2, abs_=0.0005, unit="%", placeholder="a percentage", label="Cut in mean squared error",
                   wrong=[("ratio", 0.8, 0.0005), ("against-mean", 0.36, 0.0005), ("one-minus-phi", 0.4, 0.0005)],
                   accept="20% within 0.05"),
    feedback=fb("Persistence has error 3.2 and the fit 2.56. The cut is $1 - 2.56/3.2 = 20\\%$.",
                "Find each mean squared error, then compare the fit with persistence, not with the mean.",
                {"ratio": "You gave the ratio of the errors, 80%. The cut is what is left over, $1 - 0.8$.",
                 "against-mean": "You compared the fit with the mean forecast, whose error is 4. The question asks about persistence.",
                 "one-minus-phi": "You gave $1 - 0.6$. The errors are $2 \\times 4 \\times 0.4$ and $4 \\times 0.64$, and their ratio sets the cut."}),
    explain="Persistence errs by $x_{t+1} - x_t$, with variance $2 \\times 4 \\times (1 - 0.6) = 3.2$. The fitted forecast errs with variance $4 \\times (1 - 0.6^2) = 2.56$. The cut is $1 - 2.56/3.2 = 20\\%$.")

# ---------------------------------------------------------------- 10 group fit (code, python)
SOL10 = '''import pandas as pd
import numpy as np

def costliest_desk(df, min_rows):
    best_name, best_slope = None, None
    for name in sorted(df['desk'].unique()):
        g = df[df['desk'] == name]
        if len(g) < min_rows or g['size'].nunique() < 2:
            continue
        slope = np.polyfit(g['size'], g['cost'], 1)[0]
        if best_slope is None or slope > best_slope:
            best_name, best_slope = name, slope
    return best_name
'''
START10 = '''import pandas as pd
import numpy as np

def costliest_desk(df, min_rows):
    """Desk with the largest slope of cost on size.
    Skip a desk with too few rows or one distinct size.
    Return None if no desk qualifies."""
    # Your code here
    return None
'''
PRE10 = '''import pandas as pd
import numpy as np

FILLS = pd.DataFrame({
    'desk': ['north'] * 4 + ['east'] * 5 + ['south'] * 3 + ['west'] * 4,
    'size': [1, 2, 3, 4, 10, 20, 30, 40, 50, 5, 6, 7, 2, 2, 2, 2],
    'cost': [3, 5, 8, 9, 4, 7, 8, 14, 15, 2, 9, 14, 2, 4, 9, 1],
})
'''
T10 = [
    ("costliest_desk(FILLS, 4)", "'north'", None),
    ("costliest_desk(FILLS, 3)", "'south'", None),
    ("costliest_desk(FILLS, 6)", "None", None),
    ("costliest_desk(FILLS.iloc[:0], 3)", "None", None),
    ("costliest_desk(FILLS[FILLS['desk'] == 'west'], 2)", "None", None),
    ("costliest_desk(pd.DataFrame({'desk': ['b', 'b', 'a', 'a'], 'size': [1, 3, 2, 6], 'cost': [9, 5, 9, -3]}), 2)", "'b'", None),
    ("costliest_desk(pd.DataFrame({'desk': ['y', 'x', 'y', 'x', 'y'], 'size': [1, 2, 3, 4, 5], 'cost': [1, 7, 3, 12, 5]}), 2)", "'x'", None),
]
I[10] = item(
    "e-costliest-desk", 4, ["rq-data"], ["group-fit"], 480,
    title="Which desk has the steepest impact",
    prose="A frame of fills has the columns `desk`, `size` (lots) and `cost` (£ of slippage). A desk's impact slope is the least-squares slope of `cost` on `size`. The frame `FILLS` is ready to try.",
    question="Write `costliest_desk(df, min_rows)`. It returns the name of the desk with the largest impact slope. Skip a desk with fewer than `min_rows` rows or only one distinct size. Return `None` if no desk qualifies.",
    widget=code_py(START10, SOL10, PRE10,
                   examples=[("costliest_desk(FILLS, 4)", "'north'")],
                   tests=T10,
                   how="Check runs 7 hidden tests. They try two `min_rows` limits and no qualifying desk. They also try an empty frame, one distinct size, all slopes negative and interleaved rows. Each answer must equal the expected name or `None`."),
    feedback=fb("Group by desk, guard the small and flat groups, then pick the largest slope.",
                "Run it on `FILLS` with `min_rows` 4 and then 3, and compare the two names."),
    explain="Fit each desk on its own. Skip a desk with too few rows or a single size, since that line is undefined. Keep the largest slope, even when every slope is negative.")

# ---------------------------------------------------------------- 11 online fit (parts)
I[11] = parts_item(
    "e-online-slope", 5, ["rq-data", "rq-linalg"], ["online-fit"], 360,
    title="A slope kept up to date",
    prose="A desk fits slippage $y$ (basis points) on order size $x$ (thousands of shares). Its window holds the last four orders: $(1, 3)$, $(2, 4)$, $(3, 7)$ and $(4, 8)$. It keeps the sums $n$, $\\sum x$, $\\sum y$, $\\sum x^2$ and $\\sum xy$, and the slope is $\\dfrac{n\\sum xy - \\sum x \\sum y}{n\\sum x^2 - (\\sum x)^2}$.",
    question="Three follow-ups on the same window.",
    parts=[
        dict(question="A fifth order, $(5, 12)$, arrives. What is the slope over all five?",
             widget=numeric(2.2, abs_=0.005, placeholder="a decimal", label="Slope after the arrival",
                            wrong=[("forgot-n", 2.8, 0.005), ("old-slope", 1.8, 0.005)], accept="2.2 within 0.005"),
             feedback=fb("The sums become $n = 5$, 15, 34, 55 and 124, so the slope is $(620 - 510)/(275 - 225) = 2.2$.",
                         "Add the new row to every sum, including $n$, before using the formula.",
                         {"forgot-n": "You kept $n = 4$ after adding the row. The count grows with the sums.",
                          "old-slope": "You gave the slope of the first four rows. Add $(5, 12)$ to every sum first."})),
        dict(question="Now the oldest order, $(1, 3)$, leaves the window. What is the slope of the last four?",
             widget=numeric(2.5, abs_=0.005, placeholder="a decimal", label="Slope after the departure",
                            wrong=[("added-again", 2.125, 0.005), ("not-removed", 2.2, 0.005)], accept="2.5 within 0.005"),
             feedback=fb("Subtract the row from every sum: $n = 4$, 14, 31, 54 and 121. The slope is $(484 - 434)/(216 - 196) = 2.5$.",
                         "Take the leaving row out of every sum, including $n$.",
                         {"added-again": "You added the leaving row a second time. A departure subtracts from every sum.",
                          "not-removed": "You kept the row in. That gives the five-row slope."})),
        dict(question="After a million updates the sums of squares are huge and nearly cancel in the denominator. What is the sound fix?",
             widget=choice([
                 ("a", "Keep sums of deviations from a running mean, so nothing large is subtracted.", True, None),
                 ("b", "Nothing: each removal exactly undoes its addition, so errors cancel.", False,
                  "Each addition and removal rounds on its own, so the errors build up instead of cancelling."),
                 ("c", "Refit from scratch on every update, since running sums cannot be trusted.", False,
                  "A refit costs a pass over the window each time. Centred sums keep the update at a few operations."),
                 ("d", "Use a longer integer for the sums, because the totals overflow.", False,
                  "The loss is rounding in the subtraction of two nearly equal floats, not overflow."),
             ]),
             feedback=fb("Centre the data. Sums of deviations avoid subtracting two huge, nearly equal numbers.",
                         "Ask what is subtracted in the denominator, and how large it is.")),
    ],
    explain="Adding a row adds to every sum and a departure subtracts from every sum. The slope formula then costs a few operations, not a pass over the window. With huge sums, centre the data first.")

ITEMS_A = I
