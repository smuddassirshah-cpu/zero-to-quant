"""Writes app/content/exams/mock-superday-research.json.

Run from anywhere:  python3 -I research_exam.py <path to the exam json to write>
Every keyed number is recomputed here from scratch, as a Fraction, by a second method that differs from the one in
research_mocks.py (which holds the first method and ends ALL AGREE).  The coding references are run against the hidden
tests, the starters are run and must fail, and the voice rules are checked on every learner-facing string.
Standard library only.
"""
import json, math, os, re, sys, itertools
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import research_mocks as RM  # first method, the reference coding functions and the exact checkers

OUT = sys.argv[1]
FAIL = []


def agree(label, a, b, tol=0):
    if abs(a - b) > tol:
        FAIL.append(label)
        print("FAIL", label, a, b)
    else:
        print("OK  ", label, float(a), float(b))


# ---------------------------------------------------------------------------------------------- numbers, second pass
# S1: two regressions.  Build (r, sx, sy) from the slopes, then rebuild the slopes; duplicate a sample for the SE ratio.
b_yx, b_xy = F(7, 20), F(7, 5)
r2 = b_yx * b_xy
agree("S1 r^2 = 0.49", r2, F(49, 100))
r = F(7, 10)
assert r * r == r2
agree("S1 sy/sx from slope and r", b_yx / r, F(1, 2))
agree("S1 sy/sx from the other slope", r / b_xy, F(1, 2))
agree("S1 r from averaging (wrong 0.875)", (b_yx + b_xy) / 2, F(7, 8))
ratio = math.sqrt(38 / 78)
agree("S1 SE ratio sqrt(38/78)", ratio, math.sqrt(38 / 39) / math.sqrt(2), 1e-12)
assert round(1 - ratio, 2) == 0.30 and round(1 - 1 / math.sqrt(2), 2) == 0.29
# S2
a, b = F(9, 10), F(-3, 5)
top = float(a * b) + math.sqrt(float((1 - a * a) * (1 - b * b)))
det = lambda x: F(1) - a * a - b * b - x * x + 2 * a * b * x
best = max(F(i, 10000) for i in range(-10000, 10001) if det(F(i, 10000)) >= 0)
agree("S2 upper limit -0.1913", top, float(best), 1e-4)
assert round(top, 3) == -0.191
low = float(a * b) - math.sqrt(float((1 - a * a) * (1 - b * b)))
assert round(low, 3) == -0.889
# S3
M = [[F(7, 2) if i == j else F(1, 2) for j in range(4)] for i in range(4)]
perm = lambda p: (-1) ** sum(1 for i in range(4) for j in range(i + 1, 4) if p[i] > p[j])
leib = sum(perm(p) * math.prod(M[i][p[i]] for i in range(4)) for p in itertools.permutations(range(4)))
agree("S3 determinant by the Leibniz sum", leib, F(135))
assert 3 ** 4 == 81 and 5 ** 4 == 625 and 5 * 3 == 15
# S4
p_any = 1 - F(19, 20) ** 12
agree("S4 p1", p_any, sum(math.comb(12, k) * F(1, 20) ** k * F(19, 20) ** (12 - k) for k in range(1, 13)))
assert round(float(p_any), 4) == 0.4596 and round(float(F(19, 20) ** 12), 4) == 0.5404
agree("S4 p2 0.05/12", F(1, 20) / 12, F(5, 1200))
assert round(1 / 240, 5) == 0.00417 and F(6, 1000) > F(1, 240)
# M1
Sxx, Sxy, lam = F(50), F(100), F(25)
agree("M1 ridge", Sxy / (Sxx + lam), min((F(i, 300) for i in range(901)), key=lambda t: Sxx * t * t - 2 * Sxy * t + lam * t * t))
assert round(float(F(4, 3)), 4) == 1.3333 and round(2 / 26, 4) == 0.0769
# M2
co = [F(3), F(4, 5), F(-3, 2), F(3, 10)]
soft = [max(abs(c) - 1, F(0)) for c in co]
agree("M2 sum of soft thresholds", sum(soft), F(5, 2))
assert sum(abs(c) for c in co) == F(28, 5) and sum(abs(c - (1 if c > 0 else -1)) for c in co) == F(17, 5)
# M4
tr, dt = 7, 8
l1 = (tr + math.sqrt(tr * tr - 4 * dt)) / 2
agree("M4 share", l1 / tr, 0.7945, 5e-5)
assert round(4 / 7, 4) == 0.5714
# M5
agree("M5 A", F(1, 4) + F(1, 4) + 1, F(3, 2))
agree("M5 B", F(1, 25) + F(16, 25) + 1, F(42, 25))
assert F(1, 2) + F(1, 4) + 1 == F(7, 4) and F(1, 4) + F(1, 4) == F(1, 2)
assert F(1, 5) + F(16, 25) + 1 == F(46, 25) and F(1, 25) + F(16, 25) == F(17, 25)
# M6
ys = [1, 3, 8, 12]
mean = F(sum(ys), 4)
res = [y - mean for y in ys]
sse = lambda seg: sum((v - sum(seg) / len(seg)) ** 2 for v in seg)
splits = [sse(res[:k]) + sse(res[k:]) for k in (1, 2, 3)]
assert [float(round(s, 1)) for s in splits] == [40.7, 10.0, 26.0] and splits.index(min(splits)) == 1
pred = [mean + F(1, 2) * F(-4)] * 2 + [mean + F(1, 2) * F(4)] * 2
agree("M6 MSE", sum((y - p) ** 2 for y, p in zip(ys, pred)) / 4, F(13, 2))
# cases
z = 0.023 / math.sqrt(0.25 / 1000)
agree("Case A z", z, 1.4546, 1e-4)
agree("Case A p", 2 * 0.5 * math.erfc(z / math.sqrt(2)), 0.1458, 1e-4)
t = 0.04 * math.sqrt(998) / math.sqrt(1 - 0.0016)
agree("Case B t", t, 1.2646, 1e-4)
half = 1.96 / math.sqrt(997)
lo, hi = math.tanh(math.atanh(0.04) - half), math.tanh(math.atanh(0.04) + half)
assert round(lo, 3) == -0.022 and round(hi, 3) == 0.102

# ---------------------------------------------------------------------------------------------- builders
def money(s):
    return s


def num(answer, tol, wrong, accept, placeholder="a number"):
    return {"kind": "numeric", "answer": answer, "tol": {"abs": tol}, "placeholder": placeholder, "label": "Your answer",
            "wrong": [{"id": w[0], "value": w[1], "tol": {"abs": w[2]}} for w in wrong], "accept": accept}


def choice(key, distractors):
    opts = [{"id": "a", "text": key, "correct": True}]
    for k, (text, why) in zip("bcd", distractors):
        opts.append({"id": k, "text": text, "why": why})
    return {"kind": "choice", "layout": "stack", "shuffle": True, "label": "Answer options", "options": opts}


def fb(correct, generic, bykey=None):
    d = {"correct": correct, "generic": generic}
    if bykey:
        d["byKey"] = bykey
    return d


def codew(starter, examples, tests, how, solution):
    return {"kind": "code", "language": "python", "starter": starter, "examples": [{"call": c, "expect": e, "compare": "isclose"} for c, e in examples],
            "tests": tests, "how": how, "solution": solution}


def numeric_item(iid, diff, skills, tag, pace, title, question, widget, feedback, explain):
    return {"id": iid, "difficulty": diff, "skills": skills, "tags": [tag], "pace": pace, "title": title, "question": question,
            "widget": widget, "feedback": feedback, "explain": {"text": explain}}


def part(question, widget, feedback, explain):
    return {"question": question, "widget": widget, "feedback": feedback, "explain": {"text": explain}}


def parts_item(iid, diff, skills, tag, pace, title, prose, parts):
    return {"id": iid, "difficulty": diff, "skills": skills, "tags": [tag], "pace": pace, "title": title, "prose": prose, "parts": parts}


# ---------------------------------------------------------------------------------------------- paper 1
s1 = parts_item("s1-two-regressions", 3, ["rq-stats"], "two-regressions", 420, "Two regressions",
    "Regressing $y$ on $x$ over 40 rows gives a slope of 0.35. Regressing $x$ on $y$ over the same rows gives a slope of 1.4.", [
    part("What is the correlation of $x$ and $y$? Both slopes are positive.",
         num(0.7, 0.0005, [("r-squared", 0.49, 0.0005), ("averaged", 0.875, 0.0005)], "0.7 (within 0.0005)"),
         fb("The two slopes multiply to $r^2$, so $r = \\sqrt{0.49}$.", "The product of the two slopes is a familiar quantity. Take its root.",
            {"r-squared": "You gave $r^2$. The product of the slopes is $r^2$, so take its square root.",
             "averaged": "You averaged the slopes. They multiply to $r^2$ and do not average to $r$."}),
         "The slopes are $r s_y/s_x$ and $r s_x/s_y$, so their product is $r^2 = 0.35 \\times 1.4 = 0.49$ and $r = 0.7$. Check: a standard deviation ratio of 2 gives slopes $0.7/2$ and $0.7 \\times 2$."),
    part("What is $s_y / s_x$, the ratio of the standard deviation of $y$ to that of $x$?",
         num(0.5, 0.0005, [("flipped", 2.0, 0.001), ("slope", 0.35, 0.0005)], "0.5 (within 0.0005)"),
         fb("The slope of $y$ on $x$ is $r s_y/s_x$, so divide 0.35 by 0.7.", "Write the slope of $y$ on $x$ in terms of $r$ and the two spreads.",
            {"flipped": "You took $x$ over $y$. The slope of $y$ on $x$ has $s_y$ on top.",
             "slope": "You gave the slope. Divide it by $r = 0.7$ to reach the ratio of spreads."}),
         "The slope of $y$ on $x$ is $r s_y/s_x$, so $s_y/s_x = 0.35/0.7 = 0.5$. Check: $r/1.4 = 0.7/1.4 = 0.5$."),
    part("You stack a copy of every row beneath the data, so $n$ goes from 40 to 80. What happens to the slope and its standard error?",
         choice("The slope stays the same and its standard error is about 30% smaller.",
                [("The slope and the standard error both stay the same.", "You expected copies to change nothing. The formula counts 80 rows, so the error shrinks."),
                 ("The slope stays the same and its standard error is about 50% smaller.", "You halved it. The error falls with the square root of $n$, so doubling $n$ cuts it by about 30%."),
                 ("The slope halves and its standard error stays the same.", "You split the slope between the two copies. Copies lie on the same points, so the line does not move.")]),
         fb("Copies leave the line alone and make the formula over-confident.", "Ask what each sum in the slope does when every row appears twice."),
         "Every sum doubles, so the line does not move. The error scales as $\\sqrt{38/78} = 0.70$, about 30% smaller, although the copies add no new evidence. An explicit duplicated sample gives the same ratio.")])

s2 = numeric_item("s2-correlation-limits", 4, ["rq-stats", "rq-linalg"], "correlation-limits", 300, "Correlations that must fit together",
    "Assets A and B have correlation 0.9. Assets B and C have correlation $-0.6$. What is the largest possible correlation of A and C? Give three decimals.",
    num(-0.1913, 0.0005, [("centre", -0.54, 0.001), ("sign", 0.191, 0.0005), ("bottom", -0.889, 0.001)], "-0.191 (within 0.0005)", "three decimals"),
    fb("The determinant bound gives $ab + \\sqrt{(1-a^2)(1-b^2)}$.", "A correlation matrix must have a determinant of at least 0. Solve that for the third correlation.",
       {"centre": "You gave the centre of the range, $ab$. The largest value adds the square-root term.",
        "sign": "You flipped the sign. A and C cannot be positively correlated here.",
        "bottom": "You gave the other end of the range. The largest value adds the root, not subtracts it."}),
    "The determinant of the correlation matrix must be at least 0. That bounds the third correlation by $ab \\pm \\sqrt{(1-a^2)(1-b^2)} = -0.54 \\pm 0.3487$. The top is $-0.1913$, and a grid search on the exact determinant agrees.")

s3 = numeric_item("s3-special-eigenvalues", 3, ["rq-linalg"], "special-eigenvalues", 240, "A matrix with a pattern",
    "A 4 by 4 matrix has 3.5 on the diagonal and 0.5 in every other place. What is its determinant?",
    num(135, 0, [("threes", 81, 0), ("fives", 625, 0), ("distinct", 15, 0)], "135 exactly", "a whole number"),
    fb("Write it as $3I + 0.5J$ and multiply the eigenvalues 5, 3, 3, 3.", "Split the matrix into a multiple of the identity and a multiple of the all-ones matrix.",
       {"threes": "You used the eigenvalue 3 for all four directions. The all-ones direction has eigenvalue 5.",
        "fives": "You used the eigenvalue 5 four times. Only the all-ones direction has it.",
        "distinct": "You counted each distinct eigenvalue once. The eigenvalue 3 appears three times."}),
    "Write the matrix as $3I + 0.5J$, where $J$ is all ones. $J$ has eigenvalues 4, 0, 0, 0, so the matrix has eigenvalues 5, 3, 3, 3. The determinant is $5 \\times 27 = 135$, and exact elimination agrees.")

s4 = parts_item("s4-multiple-testing", 4, ["rq-stats"], "multiple-testing", 480, "Twelve signals",
    "You test 12 independent signals. None has a real effect. Each test uses a 5% significance level.", [
    part("What is the chance that at least one test gives a false positive? Give a decimal.",
         num(0.4596, 0.0005, [("added", 0.6, 0.001), ("one-test", 0.05, 0.0005), ("none", 0.5404, 0.0005)], "0.4596 (within 0.0005)", "a decimal"),
         fb("Find the chance that all 12 stay quiet, then subtract it from 1.", "It is easier to find the chance of no false positive first."
            ),
         "Each test stays quiet with chance 0.95, so all 12 do with $0.95^{12} = 0.5404$. The chance of at least one false positive is $1 - 0.5404 = 0.4596$. Summing the binomial terms from 1 to 12 gives the same."),
    part("What cut-off does the Bonferroni rule give for each test, to hold the family-wise level at 5%? Give a decimal.",
         num(0.00417, 0.00005, [("single", 0.05, 0.0005), ("times", 0.6, 0.001)], "0.00417 (within 0.00005)", "a decimal"),
         fb("Bonferroni divides the 5% level by the number of tests.", "The rule shares the family-wise level out across the tests.",
            {"single": "You gave the single-test cut-off. With 12 tests each one needs a lower bar.",
             "times": "You multiplied by 12. Bonferroni divides, so the cut-off falls."}),
         "Bonferroni divides the family-wise level by the number of tests: $0.05/12 = 0.00417$. Check: 12 tests at that cut-off add to at most 5%."),
    part("The smallest of the 12 p-values is 0.006. What do you conclude?",
         choice("Not significant, because 0.006 is above the cut-off of 0.0042.",
                [("Significant, because 0.006 is below 0.05.", "You used the single-test cut-off. With 12 tests the cut-off falls to 0.0042."),
                 ("Significant, because 0.006 is below $12 \\times 0.05$.", "You multiplied the cut-off by 12. Bonferroni divides it."),
                 ("Not significant, because 12 tests can never show a real effect.", "You ruled out any real effect. A true effect can still clear the lower cut-off.")]),
         fb("Compare 0.006 with $0.05/12 = 0.0042$.", "Compare the smallest p-value with the Bonferroni cut-off, not with 0.05."),
         "The cut-off is $0.05/12 = 0.0042$, and 0.006 is above it. So the smallest p-value does not clear the family-wise bar. A fresh sample is the honest next step.")])
# the first part has no byKey for 'added' and so on: add them
s4["parts"][0]["feedback"]["byKey"] = {
    "added": "You added $12 \\times 5\\%$. Chances of overlapping events do not simply add.",
    "one-test": "You gave the chance for one test. There are 12 chances to be wrong.",
    "none": "You gave the chance that no test is a false positive. Subtract it from 1."}

# ---------------------------------------------------------------------------------------------- paper 2
m1 = numeric_item("m1-ridge-shrinkage", 3, ["rq-ml"], "ridge-shrinkage", 210, "A ridge slope",
    "One centred predictor has $S_{xx} = 50$ and $S_{xy} = 100$. Ridge minimises the squared error plus $\\lambda \\beta^2$. What is the ridge slope with $\\lambda = 25$?",
    num(1.3333, 0.001, [("least-squares", 2.0, 0.001), ("halved", 1.0, 0.001), ("one-plus", 0.0769, 0.0005)], "1.3333 (within 0.001)", "a number"),
    fb("The ridge slope is $S_{xy}/(S_{xx} + \\lambda)$.", "Set the derivative of the penalised sum of squares to zero.",
       {"least-squares": "You gave the least-squares slope. The penalty pulls it towards zero.",
        "halved": "You halved the slope. The shrinkage depends on $\\lambda$ against $S_{xx}$, not a fixed half.",
        "one-plus": "You divided by $1 + 25$. The penalty adds to $S_{xx}$ in the denominator."}),
    "Setting the derivative of $\\sum (y - \\beta x)^2 + 25\\beta^2$ to zero gives $\\beta = S_{xy}/(S_{xx} + 25) = 100/75 = 1.3333$. A grid search over $\\beta$ finds the same minimum. The penalty shrinks the least-squares slope of 2.0 towards zero.")

m2 = numeric_item("m2-lasso-threshold", 3, ["rq-ml"], "lasso-threshold", 210, "Lasso on an orthonormal design",
    "The columns of $X$ are orthonormal. The least-squares coefficients are 3.0, 0.8, $-1.5$ and 0.3. The lasso minimises $\\tfrac12 \\lVert y - X\\beta \\rVert^2 + \\lambda \\lVert \\beta \\rVert_1$ with $\\lambda = 1$. What is the sum of the absolute lasso coefficients?",
    num(2.5, 0.0005, [("no-shrink", 5.6, 0.001), ("no-floor", 3.4, 0.001)], "2.5 (within 0.0005)", "a number"),
    fb("Each coefficient moves 1 towards zero and stops at zero.", "With orthonormal columns the problem splits into one variable at a time.",
       {"no-shrink": "You summed the least-squares coefficients. The penalty shrinks each one.",
        "no-floor": "You shrank every coefficient by 1 without stopping at zero. A coefficient smaller than 1 becomes 0."}),
    "With orthonormal columns each coefficient is soft-thresholded: it moves 1 towards zero and stops at zero. That gives 2.0, 0, $-0.5$ and 0, so the sum of absolute values is 2.5. Minimising each one-variable objective on a grid gives the same.")

m4 = numeric_item("m4-pca-share", 3, ["rq-ml", "rq-linalg"], "pca-share", 270, "Variance on the first component",
    "A covariance matrix has rows $(4, 2)$ and $(2, 3)$. What share of the total variance lies on the first principal component?",
    num(0.7945, 0.0005, [("first-variable", 0.5714, 0.001), ("equal", 0.5, 0.001)], "0.7945 (within 0.0005)", "a decimal"),
    fb("The share is the largest eigenvalue over the trace.", "Find the eigenvalues from the trace and the determinant.",
       {"first-variable": "You gave the first variable's share, $4/7$. Principal components mix the variables.",
        "equal": "You assumed an equal split. The correlation puts most of the variance on one direction."}),
    "The eigenvalues satisfy $\\lambda^2 - 7\\lambda + 8 = 0$, so $\\lambda_1 = (7 + \\sqrt{17})/2 = 5.5616$. The trace is 7, so the share is $5.5616/7 = 0.7945$. Power iteration gives the same.")

m3 = {"id": "m3-leakage", "difficulty": 4, "skills": ["rq-ml", "rq-case"], "tags": ["leakage"], "pace": 270, "title": "A score that is too good",
    "question": "You standardise every feature with the mean and standard deviation of the whole sample, then split by time. The test score is too good. Why?",
    "widget": choice("The scaler saw the test rows, so the future leaked in.",
        [("Standardising always raises the $R^2$ of a model.", "You treated scaling as a gain. It changes units, not information."),
         ("A split by time always favours the model over a random split.", "You blamed the split. A later test set is the honest set-up for a forecast."),
         ("The model is too simple to overfit the training rows.", "You blamed simplicity. A simple model does not explain a score that is too good.")]),
    "feedback": fb("The scaler was fitted on rows it should not have seen.", "Ask which rows each step of the pipeline was allowed to see."),
    "explain": {"text": "The mean and standard deviation used the test rows, so every training row carries a trace of the future. Fit the scaler on the training rows only, then apply it to the test rows. The time split was right and the scaling step was not."}}

m5 = parts_item("m5-bias-variance", 4, ["rq-ml"], "bias-variance", 420, "Two models",
    "Expected squared error is the bias squared plus the variance plus the noise variance. The noise variance is 1.0 for both models.", [
    part("Model A has bias 0.5 and variance 0.25. What is its expected squared error?",
         num(1.5, 0.005, [("unsquared", 1.75, 0.005), ("no-noise", 0.5, 0.005)], "1.5 (within 0.005)"),
         fb("Square the bias, then add the variance and the noise.", "Three terms add: bias squared, variance and noise.",
            {"unsquared": "You added the bias without squaring it. The bias enters as a square.",
             "no-noise": "You left out the noise variance. It is part of the error that no model removes."}),
         "Bias squared is $0.5^2 = 0.25$. Add the variance 0.25 and the noise 1.0 to get 1.5. Building the three terms separately gives the same."),
    part("Model B has bias 0.2 and variance 0.64. What is its expected squared error?",
         num(1.68, 0.005, [("unsquared", 1.84, 0.005), ("no-noise", 0.68, 0.005)], "1.68 (within 0.005)"),
         fb("Square the bias, then add the variance and the noise.", "Three terms add: bias squared, variance and noise.",
            {"unsquared": "You added the bias without squaring it. The bias enters as a square.",
             "no-noise": "You left out the noise variance. It is part of the error that no model removes."}),
         "Bias squared is $0.2^2 = 0.04$. Add 0.64 and 1.0 to get 1.68."),
    part("Model B has the lower bias but the higher error. Which change lowers its error most?",
         choice("More data or a stronger penalty, to cut its variance.",
                [("More features, to cut its bias further.", "You attacked the bias. It is already 0.04 of the 1.68, so there is little to gain."),
                 ("A weaker penalty, to fit the training rows more closely.", "You raised the variance. It is already the largest part you can change."),
                 ("Nothing, because the noise sets the error.", "You treated all the error as noise. The variance of 0.64 can still be cut.")]),
         fb("The variance is the part to cut.", "Compare how much of the error each term holds."),
         "Model B's reducible error is 0.04 of bias and 0.64 of variance. Cut the variance: more data averages it away, and a stronger penalty trades a little bias for less variance.")])

m6 = numeric_item("m6-boosting-round", 4, ["rq-ml"], "boosting-round", 360, "One boosting round",
    "Four training targets are 1, 3, 8 and 12, at positions 1, 2, 3 and 4. Boosting starts from their mean. One stump is fitted to the residuals, splitting the positions in two to minimise squared error. Its values are added at learning rate 0.5. What is the training mean squared error after this round?",
    num(6.5, 0.0005, [("before", 18.5, 0.005), ("full-step", 2.5, 0.0005)], "6.5 (within 0.0005)", "a number"),
    fb("Find the best split of the residuals, add half the stump, then average the squared errors.", "Start from the residuals around the mean of 6.",
       {"before": "You gave the error before any round. The stump has not been added.",
        "full-step": "You added the whole stump. The learning rate 0.5 adds only half of it."}),
    "The mean is 6, so the residuals are $-5, -3, 2, 6$. Splitting after the second point leaves a residual sum of squares of 10. The other splits leave 40.7 and 26. The stump adds $\\pm 2$ at rate 0.5, so the errors are $-3, -1, 0, 4$ and the mean square is $26/4 = 6.5$.")

# ---------------------------------------------------------------------------------------------- paper 3: code
T = {"rel": 1e-9, "abs": 1e-9}
def ct(call, expect, compare="isclose", tol=None, budget=None):
    d = {"call": call, "expect": expect, "compare": compare}
    if compare == "isclose":
        d["tol"] = tol or T
    if budget:
        d["budget"] = budget
    return d
def rt(call):
    return {"call": call, "compare": "raises", "expect": "ValueError"}

wlf = RM.weighted_line_fit
CALL = lambda c, fn=wlf: eval(c, {"weighted_line_fit": fn})
t1_calls = ["weighted_line_fit([1, 2, 3, 4], [2, 3, 5, 4])", "weighted_line_fit([0, 10], [100, 200])", "weighted_line_fit([3, 1, 2], [30, 10, 25])",
            "weighted_line_fit(list(range(100000)), [3 * i + 7 for i in range(100000)])",
            "weighted_line_fit([1e8 + 3, 1e8 + 4, 1e8 + 5, 1e8 + 6], [2, 5, 4, 8])"]
t1_raise = ["weighted_line_fit([5, 5, 5], [1, 2, 3])", "weighted_line_fit([1], [2])", "weighted_line_fit([1, 2, 3], [4, 5])"]
t2_calls = ["weighted_line_fit([1, 2, 3, 4], [2, 3, 5, 4], [1, 1, 1, 1])", "weighted_line_fit([0, 1, 2], [1, 3, 2], [1, 1, 4])",
            "weighted_line_fit([1, 2, 3], [2, 4, 7], [0.5, 1.0, 2.0])", "weighted_line_fit([0, 10], [5, 7], [1, 1000])"]
t2_raise = ["weighted_line_fit([1, 2, 3], [2, 4, 7], [1, 1])"]
exp = {}
for c in t1_calls + t2_calls:
    got, second = CALL(c), CALL(c, RM.weighted_line_fit_exact)
    assert RM.lists_close(got, second), c
    exp[c] = got
# expected values written as the exact decimal where there is one
exp["weighted_line_fit([1e8 + 3, 1e8 + 4, 1e8 + 5, 1e8 + 6], [2, 5, 4, 8])"] = [1.7, -170000002.9]
exp["weighted_line_fit([0, 10], [100, 200])"] = [10.0, 100.0]
assert RM.lists_close(CALL(t1_calls[4]), exp[t1_calls[4]]) and RM.lists_close(CALL(t1_calls[1]), exp[t1_calls[1]])
fmt = lambda v: "[" + ", ".join(repr(float(x)) for x in v) + "]"

sol1 = '''def weighted_line_fit(xs, ys):
    n = len(xs)
    if n != len(ys) or n < 2:
        raise ValueError("need matching lists of at least two points")
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        raise ValueError("all x values are equal")
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx
    return [slope, my - slope * mx]
'''
sol2 = '''def weighted_line_fit(xs, ys, weights=None):
    n = len(xs)
    if n != len(ys) or (weights is not None and len(weights) != n) or n < 2:
        raise ValueError("need matching lists of at least two points")
    w = weights if weights is not None else [1.0] * n
    sw = sum(w)
    mx = sum(wi * x for wi, x in zip(w, xs)) / sw
    my = sum(wi * y for wi, y in zip(w, ys)) / sw
    sxx = sum(wi * (x - mx) ** 2 for wi, x in zip(w, xs))
    if sxx == 0:
        raise ValueError("all x values are equal")
    sxy = sum(wi * (x - mx) * (y - my) for wi, x, y in zip(w, xs, ys))
    slope = sxy / sxx
    return [slope, my - slope * mx]
'''
start1 = 'def weighted_line_fit(xs, ys):\n    """Return [slope, intercept] of the least-squares line."""\n    ...\n'
start2 = sol1.replace("def weighted_line_fit", "def weighted_line_fit")

tests1 = [ct(c, fmt(exp[c])) for c in t1_calls] + [rt(c) for c in t1_raise]
tests2 = [ct(c, fmt(exp[c])) for c in t2_calls] + [rt(c) for c in t2_raise]
assert len(tests1) == 8 and len(tests2) == 5

# harness: run a code against the tests (call/expect/compare) in-process, to check solutions pass and starters fail
def run_tests(src, tests):
    ns = {}
    try:
        exec(src, ns)
    except Exception:
        return 0
    ok = 0
    for t in tests:
        try:
            if t["compare"] == "raises":
                try:
                    eval(t["call"], ns)
                except ValueError:
                    ok += 1
                continue
            got, want = eval(t["call"], ns), eval(t["expect"])
            if t["compare"] == "equal":
                ok += got == want
            else:
                tol = t["tol"]
                rel, ab = tol.get("rel", 0), tol.get("abs", 0)
                gl = got if isinstance(got, list) else [got]
                wl = want if isinstance(want, list) else [want]
                ok += len(gl) == len(wl) and all(abs(g - w) <= max(rel * max(abs(g), abs(w)), ab) for g, w in zip(gl, wl))
        except Exception:
            pass
    return ok

assert run_tests(sol1, tests1) == 8, "sol1"
assert run_tests(sol2, tests1 + tests2) == 13, "sol2"
assert run_tests(start1, tests1) <= 3, run_tests(start1, tests1)  # only the three raises could pass by accident; none do for `...`
assert run_tests(start2, tests2) == 0
# the textbook sums fail the shifted-data test (the denominator is exactly 0.0)
naive_src = 'def weighted_line_fit(xs, ys):\n    n = len(xs)\n    if n != len(ys) or n < 2:\n        raise ValueError\n    sx, sy = sum(xs), sum(ys)\n    sxx = sum(x * x for x in xs)\n    sxy = sum(x * y for x, y in zip(xs, ys))\n    d = n * sxx - sx * sx\n    if d == 0:\n        raise ValueError\n    s = (n * sxy - sx * sy) / d\n    return [s, (sy - s * sx) / n]\n'
assert run_tests(naive_src, tests1) < 8 and run_tests(naive_src, [tests1[4]]) == 0

c1 = parts_item("c1-fit-line", 4, ["rq-data", "rq-stats"], "fit-line-weights", 1500, "Fit a line, then change it",
    "You write the least-squares line through some points. Then the interviewer adds a requirement.", [
    part("Write `weighted_line_fit(xs, ys)`. It returns `[slope, intercept]` of the least-squares line. Raise `ValueError` for fewer than two points, lists of different lengths, or all `xs` equal.",
         codew(start1, [(t1_calls[0], fmt(exp[t1_calls[0]])), (t1_calls[2], fmt(exp[t1_calls[2]]))], tests1,
               "Submit runs 8 hidden tests. Answers are accepted when each number is within 1e-9, relative or absolute. One test uses very large x values.", sol1),
         fb("All eight tests pass, including the shifted data.", "A hidden test failed. Check the large-x test: centre the data before you sum."),
         "Centre the points on their means before summing, so the large shift cancels. The textbook sums subtract two huge, nearly equal numbers and lose every digit. An exact Fraction solve gives the same line."),
    part("The interviewer says some points are measured more precisely. Add a third argument, `weights`, one positive number per point, and fit by weighted least squares. Keep every earlier behaviour.",
         codew(start2.replace("def weighted_line_fit(xs, ys):", "def weighted_line_fit(xs, ys):"), [(t2_calls[1], fmt(exp[t2_calls[1]]))], tests2,
               "Submit runs your part 1 tests and 5 more, 13 in all. Answers are accepted when each number is within 1e-9, relative or absolute.", sol2),
         fb("All thirteen tests pass.", "A hidden test failed. Use weighted means, and raise ValueError when weights and points differ in number."),
         "Replace each mean with a weighted mean, and weight each squared deviation. With equal weights the code reduces to part 1. The exact normal equations on Fractions give the same line."),
    part("A point's noise standard deviation is $\\sigma_i$. Which weights give the best fit?",
         choice("$w_i = 1/\\sigma_i^2$, the inverse of the noise variance.",
                [("$w_i = 1/\\sigma_i$, the inverse of the noise standard deviation.", "You used the standard deviation, not the variance."),
                 ("$w_i = \\sigma_i^2$, the noise variance itself.", "You gave the noisiest points the most weight."),
                 ("$w_i = 1$ for every point.", "You ignored what you know about the noise. Equal weights suit equal noise only.")]),
         fb("Weight each point by the inverse of its noise variance.", "Ask which points should count for more."),
         "The best linear unbiased fit weights each point by $1/\\sigma_i^2$. A point twice as noisy counts a quarter as much. Equal weights are best only when every $\\sigma_i$ is the same.")])

# C2 rolling slopes
rs = RM.rolling_slopes
rs_small = ["rolling_slopes([1, 2, 3, 4, 5], [2, 4, 5, 4, 5], 3)", "rolling_slopes([1, 2, 3], [2, 4, 7], 3)", "rolling_slopes([1, 2, 3], [2, 4, 7], 4)",
            "rolling_slopes([0, 1, 2, 3], [5, 5, 5, 5], 2)", "rolling_slopes([4, 2, 9, 1, 7, 3], [8, 1, 6, 2, 9, 5], 2)",
            "[s is None for s in rolling_slopes([1, 1, 1, 2, 3], [1, 2, 3, 4, 9], 3)]", "len(rolling_slopes(list(range(10)), list(range(10)), 10))"]
tests_rs = []
for c in rs_small:
    got = eval(c, {"rolling_slopes": rs})
    slow = eval(c, {"rolling_slopes": lambda a, b, w: [None if v is None else float(v) for v in RM.rolling_slow(a, b, w)]})
    if isinstance(got, list) and got and not isinstance(got[0], bool):
        assert RM.lists_close(got, slow)
        tests_rs.append(ct(c, "[" + ", ".join(repr(float(v)) for v in got) + "]"))
    elif isinstance(got, list) and got and isinstance(got[0], bool):
        assert got == slow
        tests_rs.append(ct(c, repr(got), "equal"))
    else:
        assert got == slow
        tests_rs.append(ct(c, repr(got), "equal"))
c_big = "sum(rolling_slopes([i % 10 for i in range(200000)], [(i * i) % 97 for i in range(200000)], 1000))"
big = eval(c_big, {"rolling_slopes": rs})
XS, YS = [i % 10 for i in range(200000)], [(i * i) % 97 for i in range(200000)]
tot = F(0); sx = sy = sxx = sxy = 0
for i in range(200000):  # exact total from integer window sums
    sx += XS[i]; sy += YS[i]; sxx += XS[i] ** 2; sxy += XS[i] * YS[i]
    if i >= 1000:
        j = i - 1000; sx -= XS[j]; sy -= YS[j]; sxx -= XS[j] ** 2; sxy -= XS[j] * YS[j]
    if i >= 999:
        tot += F(1000 * sxy - sx * sy, 1000 * sxx - sx * sx)
agree("C2 total of 199,001 slopes", big, float(tot), abs(big) * 1e-12)
tests_rs.append(ct(c_big, repr(big), budget=3000))
A = list(range(200000))
c9 = "rolling_slopes(list(range(200000)), [2 * i + 1 for i in range(200000)], 50000)[-1]"
assert abs(eval(c9, {"rolling_slopes": rs}) - 2.0) < 1e-9
tests_rs.append(ct(c9, "2.0", tol={"rel": 1e-6}, budget=3000))
c10 = "len(rolling_slopes(list(range(200000)), [i % 7 for i in range(200000)], 50000))"
assert eval(c10, {"rolling_slopes": rs}) == 150001
tests_rs.append(ct(c10, "150001", "equal", budget=3000))
assert len(tests_rs) == 10

sol_rs = '''def rolling_slopes(xs, ys, w):
    sx = sy = sxx = sxy = 0
    out = []
    for i in range(len(xs)):
        sx += xs[i]
        sy += ys[i]
        sxx += xs[i] * xs[i]
        sxy += xs[i] * ys[i]
        if i >= w:
            j = i - w
            sx -= xs[j]
            sy -= ys[j]
            sxx -= xs[j] * xs[j]
            sxy -= xs[j] * ys[j]
        if i >= w - 1:
            den = w * sxx - sx * sx
            out.append(None if den == 0 else (w * sxy - sx * sy) / den)
    return out
'''
start_rs = 'def rolling_slopes(xs, ys, w):\n    """Slope of ys on xs over each full window of w points."""\n    ...\n'
# the small tests pass with the solution; the starter fails all of them
assert run_tests(sol_rs, tests_rs[:7]) == 7
assert run_tests(start_rs, tests_rs) == 0
c2 = {"id": "c2-rolling-slope", "difficulty": 4, "skills": ["rq-data"], "tags": ["rolling-slope"], "pace": 1200, "title": "A rolling slope",
      "question": "Write `rolling_slopes(xs, ys, w)`. It returns a list: the least-squares slope of `ys` on `xs` over each window of `w` neighbouring points. Use full windows only, in order. `w` is at least 2. If every `xs` value in a window is equal, that slope is `None`. The inputs reach 200,000 points.",
      "widget": codew(start_rs, [(rs_small[0], tests_rs[0]["expect"]), (rs_small[1], tests_rs[1]["expect"])], tests_rs,
                      "Submit runs 10 hidden tests, the last three on 200,000 points. Answers are accepted when each number is within 1e-9, relative or absolute.", sol_rs),
      "feedback": fb("All ten tests pass, including the large windows.", "A hidden test failed. Recomputing each window from scratch is too slow on 200,000 points; update running sums instead."),
      "explain": {"text": "Keep running sums of $x$, $y$, $x^2$ and $xy$, add the new point and subtract the one that leaves. Each slope is then $(w S_{xy} - S_x S_y)/(w S_{xx} - S_x^2)$ in constant time. Whole-number sums stay exact, and exact Fractions on every 4,000th window agree."}}

# ---------------------------------------------------------------------------------------------- paper 4: longform
MODEL_NOTE = "*An example answer. Your own words are the real answer.*\n\n"
case_a = {"id": "k1-open-case-framing", "difficulty": 4, "skills": ["rq-case", "rq-stats"], "tags": ["open-case-hit-rate"], "pace": 1200, "title": "Is 523 skill",
    "kind": "longform",
    "prompt": "Say your answer aloud first, then type it in at most 250 words.\n\nAn interviewer says: predict whether an index future rises tomorrow. You test a model on 1,000 days and it calls the direction right on 523 of them. A coin gets 500. Frame the problem, then say whether 523 is evidence of skill.",
    "model": MODEL_NOTE + "I would frame it first. The target is the sign of tomorrow's return on the future. The horizon is one day, and the loss is a wrong call. I might weight it by the size of the move.\n\nA coin gets 50%, so the baseline is 500 of 1,000. The model beats it by 2.3 points. The standard error of a hit rate is $\\sqrt{0.25/1000} = 1.58$ points, so $z$ is about 1.45. The two-sided $p$-value is about 0.15. On its own, 523 is not evidence of skill.\n\nI would add one honest limit. If I tried many models, the best of them looks better than it is. Costs matter too, and so does whether the test days came after the training days.\n\nNext I would fix the model and run it on a fresh 1,000 days. I would drop it if it does not beat 53%, about two standard errors over a coin.",
    "rubric": [{"points": 2, "text": "States the target, the horizon and the loss"}, {"points": 1, "text": "Names the coin baseline as 50%"},
               {"points": 2, "text": "Gives the standard error of 1.58 points and $z$ of about 1.45"}, {"points": 2, "text": "Gives $p$ of about 0.15 and says 523 is not significant on its own"},
               {"points": 2, "text": "Names one honest limit, such as models tried, costs, or test days after training days"}, {"points": 1, "text": "Gives a next step with a stopping rule"}]}
case_b = {"id": "k2-open-case-signal", "difficulty": 5, "skills": ["rq-case", "rq-stats"], "tags": ["open-case-signal"], "pace": 1500, "title": "Small but real",
    "kind": "longform",
    "prompt": "Say your answer aloud first, then type it in at most 250 words.\n\nYour signal has correlation 0.04 with next-day return over 1,000 days. A colleague says it is small but real, because the t-statistic is over one. Respond, and say what you would do next.",
    "model": MODEL_NOTE + "The signal explains $R^2 = 0.16\\%$ of the variance of next-day returns. The t-statistic is $0.04\\sqrt{998}/\\sqrt{1 - 0.0016} = 1.27$. That is above one but below 2, so it is not significant at the usual 5% level.\n\nA 95% interval for the correlation, from the Fisher transform, runs from $-0.02$ to $0.10$. It spans zero, so small but real is not yet supported.\n\nA small true correlation can still matter at scale. Whether it pays depends on costs and turnover, so I would test those early.\n\nFirst I would check the timing: the signal may use only data known before the return starts. Then I would extend the sample or test another market. If the interval still spans zero after twice the days, I would drop it.",
    "rubric": [{"points": 1, "text": "Gives $R^2$ of 0.16%"}, {"points": 2, "text": "Gives $t$ of 1.27, below 2, so not significant"},
               {"points": 2, "text": "Says the interval spans zero, about $-0.02$ to $0.10$"},
               {"points": 2, "text": "Says a small true correlation can matter at scale, but costs and turnover decide it"},
               {"points": 1, "text": "Checks time order and leakage before trusting it"}, {"points": 2, "text": "Makes a decision and names a next test, such as a longer sample or another market"}]}
for cs in (case_a, case_b):
    assert sum(r["points"] for r in cs["rubric"]) == 10

# ---------------------------------------------------------------------------------------------- the exam
DRAW = {"from": "bank/probability", "tags": ["bayes-in-a-minute", "estimating-n", "exceeding-one", "expected-distance", "indicator-tricks", "largest-of-several",
        "random-chords", "semicircle", "broken-stick", "urns", "hats", "waiting-for-hh", "when-to-stop", "every-coupon", "meeting", "given-the-total"],
        "difficulty": [3, 5], "n": 4}
SC = {"right": 1, "wrong": 0, "blank": 0}
exam = {
    "id": "mock-superday-research", "name": "Research superday", "style": "research",
    "models": "Reported, as of Nov 2026: quant research final rounds at Two Sigma, Citadel and JP Morgan: probability and statistics, machine learning, coding, and an open prediction case.",
    "description": "This is the reported shape of a quant research final-round day, as candidates described it by Nov 2026. There are four papers, each on its own clock. They cover probability and statistics, machine learning, coding, and an open case. Real rounds are spoken, so say each answer aloud before you type it. Some questions have follow-ups that open one at a time. Four of the probability questions are drawn afresh each time you sit. No calculator and no search engine are allowed. Orders and lengths differ by firm and office. Two checks at the end ask for what the app cannot see.",
    "skills": {"rq-stats": "Statistics questions", "rq-linalg": "Linear algebra questions", "rq-ml": "Machine learning questions", "rq-case": "The open case", "rq-data": "Data tasks"},
    "parts": [
        {"kind": "paper", "id": "stats", "name": "Probability and statistics", "minutes": 45, "scoring": SC, "pass": 0.6, "items": [s1, s2, s3, s4], "draw": [DRAW]},
        {"kind": "paper", "id": "ml", "name": "Machine learning", "minutes": 30, "scoring": SC, "pass": 0.65, "items": [m1, m2, m4, m3, m5, m6]},
        {"kind": "paper", "id": "coding", "name": "Coding", "minutes": 45, "scoring": SC, "pass": 0.5, "items": [c1, c2]},
        {"kind": "paper", "id": "case", "name": "The open case", "minutes": 45, "scoring": SC, "pass": 0.5, "items": [case_a, case_b]},
        {"kind": "check", "id": "story-aloud", "name": "I told one behavioural story aloud in under two minutes, with a result", "detail": "Tick this only if you timed it and named an outcome."},
        {"kind": "check", "id": "no-lookup", "name": "I used no search engine and no notes", "detail": "Tick this only if you sat all four papers without either."},
    ]}

# ---------------------------------------------------------------------------------------------- self-checks
import voice as V  # noqa: E402  (copied beside this script)


def strings(o, path=""):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in ("starter", "solution", "call", "expect", "setup", "id", "kind", "layout", "label", "placeholder", "language", "compare", "unit", "style"):
                continue
            yield from strings(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from strings(v, path + f"[{i}]")


bad = []
for path, s in strings(exam):
    V.check_text(path, s, bad)
# choice keys not visibly longer than the longest distractor
def walk(o):
    if isinstance(o, dict):
        if o.get("kind") == "choice":
            opts = o["options"]
            key = [x for x in opts if x.get("correct")][0]["text"]
            longest = max(len(x["text"]) for x in opts if not x.get("correct"))
            print("choice key", len(key), "longest distractor", longest)
            if len(key) > longest:
                bad.append(("choice", f"key longer than every distractor: {key[:50]}"))
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
walk(exam)
if bad:
    print("VOICE PROBLEMS"); [print(" ", b) for b in bad]
    FAIL.append("voice")
json.dump(exam, open(OUT, "w"), indent=2, ensure_ascii=False)
open(OUT, "a").write("\n")
print("WROTE", OUT)
print("EXAM CHECKS FAILED: " + ", ".join(FAIL) if FAIL else "EXAM CHECKS OK")
raise SystemExit(1 if FAIL else 0)
