"""Items of topic-3.2, part A: the ito items I1 to I11 (plan numbers)."""
from helpers import *

I = {}


def expr(answer, accept=None, wrong=None, integers=None):
    w = {"kind": "expression", "answer": answer, "keyboard": "algebra"}
    if accept:
        w["accept"] = accept
    if wrong:
        w["wrong"] = [{"id": i, "tex": t} for i, t in wrong]
    if integers:
        w["integers"] = integers
    return w


# ---------------------------------------------------------------- I1
I[1] = item(
    "e-var-two-times", 2, ["it-bm"], ["brownian-covariance"], 60,
    title="A signed combination of two times",
    prose="$W$ is a standard Brownian motion.",
    question="What is $\\mathrm{Var}(2W_3 - W_7)$?",
    widget=numeric(7, abs_=0, placeholder="a number", label="Variance",
                   wrong=[("no-covariance", 19, 0), ("plus-cross-term", 31, 0)], accept="7"),
    feedback=fb("Write $W_7 = W_3 + D$ with $D \\sim N(0, 4)$ independent of $W_3$. Then $2W_3 - W_7 = W_3 - D$, with variance $3 + 4 = 7$.",
                "Split $W_7$ into $W_3$ plus an independent increment, then add the variances.",
                {"no-covariance": "You added $4 \\cdot 3 + 7$ and dropped the covariance term. $W_3$ and $W_7$ share the first three years.",
                 "plus-cross-term": "You added the cross term where it must be subtracted. The coefficients are $2$ and $-1$, so the cross term is $-2 \\cdot 2 \\cdot 1 \\cdot 3$."}),
    explain="The variance is $4 \\cdot 3 + 7 - 2 \\cdot 2 \\cdot 1 \\cdot \\min(3, 7) = 7$. Splitting $W_7 = W_3 + D$ gives the same in one line: $W_3 - D$ has variance $3 + 4$.")

# ---------------------------------------------------------------- I3
I[3] = item(
    "e-qv-drift", 2, ["it-calculus", "it-bm"], ["quadratic-variation"], 60,
    title="Noise plus drift",
    prose="$W$ is a standard Brownian motion and $X_t = 3W_t - 2t$.",
    question="What is the quadratic variation $[X]_5$ of $X$ over $[0, 5]$?",
    widget=numeric(45, abs_=0, placeholder="a number", label="Quadratic variation", wrong=[("drift-counted", 65, 0), ("sigma-t", 15, 0)], accept="45"),
    feedback=fb("Only the noise counts: $[X]_5 = 3^2 \\cdot 5 = 45$.",
                "Square the coefficient of $W$ and multiply by the length of the interval.",
                {"drift-counted": "You added $2^2 \\cdot 5$ for the drift. The drift has finite variation, so its squared steps vanish.",
                 "sigma-t": "You used $3 \\cdot 5$. The quadratic variation of $\\sigma W$ is $\\sigma^2 t$, with the square."}),
    explain="The drift term has squared steps of order $dt^2$, which add up to nothing. The noise term gives $(3\\,dW)^2 = 9\\,dt$. Over five years that is 45.")

# ---------------------------------------------------------------- I2
I[2] = item(
    "e-gbm-below", 3, ["it-bm"], ["gbm-below"], 120,
    title="The chance a price ends below 70",
    prose="A share follows geometric Brownian motion with $S_0 = 80$, drift $\\mu = 6\\%$ and volatility $\\sigma = 30\\%$ a year.",
    question="What is $P(S_2 < 70)$ after two years? Give four decimal places.",
    widget=numeric(0.34995, abs_=0.0005, placeholder="a decimal", label="Probability",
                   wrong=[("no-ito-term", 0.2751, 0.0005), ("sigma-not-root-t", 0.2928, 0.0005)], accept="0.3500 within 0.0005"),
    feedback=fb("$\\ln S_2$ is normal with mean $\\ln 80 + 0.03$ and sd $0.3\\sqrt2$. So $z = -0.3855$ and the chance is 0.3500.",
                "Take logs: the drift of $\\ln S$ is $\\mu - \\sigma^2/2$, and the sd over two years is $\\sigma\\sqrt{T}$.",
                {"no-ito-term": "You used $\\mu$ as the drift of $\\ln S$. Itô's lemma takes off $\\sigma^2/2$, which is 4.5% a year here.",
                 "sigma-not-root-t": "You used $\\sigma$ as the sd over two years. It is $\\sigma\\sqrt{T} = 0.4243$."}),
    explain="$\\ln S_2$ has mean $\\ln 80 + (0.06 - 0.045) \\cdot 2$ and sd $0.3\\sqrt2 = 0.4243$. The standardised barrier is $z = (\\ln(70/80) - 0.03)/0.4243 = -0.3855$. So $P = \\Phi(-0.3855) = 0.3500$.")

# ---------------------------------------------------------------- I4
I[4] = item(
    "e-drift-t2w2", 3, ["it-calculus"], ["ito-drift"], 90,
    title="The drift of $t^2W_t^2$",
    prose="Let $X_t = t^2W_t^2$, so $dX_t = a\\,dt + b\\,dW_t$. Write $w$ for $W_t$.",
    question="Give the $dt$ coefficient $a$ as an expression in $t$ and $w$.",
    widget=expr("2tw^2+t^2", accept=["t^2+2tw^2", "2tw^2 + t^2"], wrong=[("no-ito-term", "2tw^2"), ("forgot-half", "2tw^2+2t^2")]),
    feedback=fb("With $f(t, x) = t^2x^2$, $a = f_t + \\tfrac12 f_{xx} = 2tx^2 + t^2$.",
                "Use $a = f_t + \\tfrac12 f_{xx}$ with $f(t, x) = t^2x^2$.",
                {"no-ito-term": "You kept $f_t$ and dropped the Itô term $\\tfrac12 f_{xx}$, which is $t^2$ here.",
                 "forgot-half": "You added $f_{xx} = 2t^2$ in full. The Itô term has a half in front, so it is $t^2$."}),
    explain="Here $f_t = 2tx^2$ and $f_{xx} = 2t^2$. The drift is $f_t + \\tfrac12 f_{xx} = 2tw^2 + t^2$. The noise coefficient is $f_x = 2t^2w$.")

# ---------------------------------------------------------------- I5
I[5] = item(
    "e-pick-martingales", 3, ["it-martingale", "it-calculus"], ["martingale-test"], 150,
    title="Which of these are martingales",
    prose="$W$ is a standard Brownian motion. Test each process for zero drift.",
    question="Select all that apply: which processes are martingales?",
    widget=multi([
        ("a", "$e^{0.8W_t - 0.32t}$", True, None),
        ("b", "$e^{0.8W_t - 0.64t}$", False, "Its drift is $(-0.64 + 0.32)$ times the process, which is not zero. The exponent needs $-\\tfrac12 \\cdot 0.8^2 t = -0.32t$."),
        ("c", "$e^{-t/2}\\cosh W_t$", True, None),
        ("d", "$W_t^2 - 2t + \\int_0^t W_s\\,dW_s$", False, "Its drift is $1 - 2 = -1$, because the Itô integral adds none. The right process is $W_t^2 - t$."),
        ("e", "$W_t^3 - 3\\int_0^t W_s\\,ds$", True, None),
        ("f", "$W_t^4 - 6tW_t^2 + 6t^2$", False, "Its drift is $6t$, not zero. The constant that cancels the drift is $3t^2$, not $6t^2$."),
    ]),
    feedback=fb("A, C and E have zero drift. B, D and F do not.",
                "Apply $f_t + \\tfrac12 f_{xx}$ to each, and use $d(W^3) = 3W^2\\,dW + 3W\\,dt$ for the last."),
    explain="A has drift $(-0.32 + 0.32)$ times itself, and C has $-\\tfrac12 f + \\tfrac12 f = 0$. For E, $d(W^3) = 3W^2\\,dW + 3W\\,dt$, so subtracting $3W\\,dt$ leaves $3W^2\\,dW$. B, D and F leave a drift.")

# ---------------------------------------------------------------- I6
I[6] = item(
    "e-theta-from-pde", 3, ["it-pricing"], ["bs-balance"], 120,
    title="Theta from the Black-Scholes equation",
    prose="A call has $S = 70$, $K = 65$, $r = 4\\%$, $\\sigma = 30\\%$ and $T = 0.75$ years. Its price is $V = 10.8791$, its delta is $\\Delta = 0.70216$ and its gamma is $\\Gamma = 0.019056$.",
    question="Use the Black-Scholes equation to find $\\Theta = \\partial V/\\partial t$ per year. Give it to 2 decimal places.",
    widget=numeric(-5.73, abs_=0.02, placeholder="a number", label="Theta per year",
                   wrong=[("no-half", -9.93, 0.02), ("sign-of-delta-term", -1.80, 0.02)], accept="-5.73 within 0.02"),
    feedback=fb("$\\Theta = rV - rS\\Delta - \\tfrac12\\sigma^2S^2\\Gamma = 0.4352 - 1.9660 - 4.2018 = -5.73$.",
                "Rearrange $\\Theta + rS\\Delta + \\tfrac12\\sigma^2S^2\\Gamma = rV$.",
                {"no-half": "You left the half off the gamma term. It is $\\tfrac12\\sigma^2S^2\\Gamma = 4.2018$, not 8.4037.",
                 "sign-of-delta-term": "You added $rS\\Delta$. Moving it across the equation makes it $-rS\\Delta = -1.9660$."}),
    explain="The equation is $\\Theta + rS\\Delta + \\tfrac12\\sigma^2S^2\\Gamma = rV$. Here $rV = 0.4352$, $rS\\Delta = 1.9660$ and $\\tfrac12\\sigma^2S^2\\Gamma = 4.2018$. So $\\Theta = 0.4352 - 1.9660 - 4.2018 = -5.73$.")

# ---------------------------------------------------------------- I10
I[10] = parts_item(
    "e-moment-and-isometry", 3, ["it-calculus"], ["moments"], 240,
    title="A mixed moment and an Itô integral",
    prose="$W$ is a standard Brownian motion.",
    question="Two follow-up questions on moments.",
    parts=[
        dict(question="What is $E[W_2 W_5^3]$?",
             widget=numeric(30, abs_=0, placeholder="a number", label="Moment",
                            wrong=[("odd-power-zero", 0, 0), ("one-pairing", 10, 0)], accept="30"),
             feedback=fb("Write $W_5 = W_2 + D$ with $D \\sim N(0, 3)$. Then $E[W_2 W_5^3] = E[W_2^4] + 3E[W_2^2]E[D^2] = 12 + 18 = 30$.",
                         "Split $W_5$ at time 2, expand the cube and keep the terms with even powers.",
                         {"odd-power-zero": "You called it zero because the total power is odd. Total power 4 is even: $W_2 \\cdot W_5^3$ has four factors.",
                          "one-pairing": "You took $E[W_2 W_5] \\cdot E[W_5^2] = 2 \\cdot 5$. Wick pairing has three pairings of four factors, not one."})),
        dict(question="What is $\\mathrm{Var}\\int_0^{2.5} e^{W_t - t/2}\\,dW_t$? Give four decimal places.",
             widget=numeric(11.18249, abs_=0.0005, placeholder="a decimal", label="Variance",
                            wrong=[("martingale-mean", 2.5, 0.0005), ("no-lower-limit", 12.1825, 0.0005)], accept="11.1825 within 0.0005"),
             feedback=fb("By the isometry the variance is $\\int_0^{2.5} E[e^{2W_t - t}]\\,dt = \\int_0^{2.5} e^t\\,dt = e^{2.5} - 1 = 11.1825$.",
                         "Square the integrand, take the mean, then integrate over $t$.",
                         {"martingale-mean": "You used $E[e^{W_t - t/2}] = 1$. The isometry needs the mean of the square, which is $e^t$.",
                          "no-lower-limit": "You gave $e^{2.5}$. The integral $\\int_0^{2.5} e^t\\,dt$ is $e^{2.5} - 1$."}))],
    explain="Part a splits $W_5$ into $W_2$ and an independent increment of variance 3. Part b uses the Itô isometry, with $E[e^{2W_t - t}] = e^t$ because $e^{2W_t - 2t}$ is a martingale.")

# ---------------------------------------------------------------- I7
I[7] = item(
    "e-daily-touch", 4, ["it-pricing"], ["barrier-touch"], 210,
    title="A barrier checked once a day",
    prose="A log price is driftless Brownian motion with $\\sigma = 25\\%$ a year over $T = 0.5$ years, checked on 126 days ($\\Delta t = 1/252$). The barrier sits 0.06 above the start, in log terms.",
    question="What is the chance the barrier is hit on a daily check? Use the continuous formula with the barrier shifted by $0.5826\\sigma\\sqrt{\\Delta t}$. Give three decimal places.",
    widget=numeric(0.6956, abs_=0.004, placeholder="a decimal", label="Probability",
                   wrong=[("continuous-monitoring", 0.734, 0.004), ("no-factor-two", 0.348, 0.004)], accept="0.696 within 0.004"),
    feedback=fb("The shifted barrier is $0.06 + 0.00917 = 0.06917$. Then $2(1 - \\Phi(0.06917/0.17678)) = 0.696$.",
                "Move the barrier up by the shift, then use the reflection principle: twice the normal tail.",
                {"continuous-monitoring": "You used the barrier 0.06 with no shift. Daily checks miss some touches, so the shifted barrier is higher.",
                 "no-factor-two": "You gave one normal tail. The reflection principle doubles it: $P(\\max > b) = 2P(W_T > b)$."}),
    explain="The shift is $0.5826 \\cdot 0.25 \\cdot \\sqrt{1/252} = 0.00917$, so the barrier is 0.06917. The sd over the period is $0.25\\sqrt{0.5} = 0.17678$. Then $2(1 - \\Phi(0.3913)) = 0.696$.")

# ---------------------------------------------------------------- I8
I[8] = parts_item(
    "e-exit-drift", 4, ["it-bm", "it-martingale"], ["exit-time"], 240,
    title="Exit with a downward drift",
    prose="$X_t = -0.3t + 0.9W_t$ starts at 0 and stops the first time it reaches $+1$ or $-2$.",
    question="Two follow-up questions on the exit.",
    parts=[
        dict(question="What is the chance that $X$ reaches $+1$ before $-2$? Give four decimal places.",
             widget=numeric(0.41317, abs_=0.0005, placeholder="a decimal", label="Probability",
                            wrong=[("driftless", 0.6667, 0.0005), ("no-sigma-squared", 0.4595, 0.0005)], accept="0.4132 within 0.0005"),
             feedback=fb("With $c = 2\\mu/\\sigma^2 = -0.7407$, stopping $e^{-cX_t}$ gives $Pe^{-c} + (1 - P)e^{2c} = 1$, so $P = 0.4132$.",
                         "Stop the martingale $e^{-cX_t}$ with $c = 2\\mu/\\sigma^2$ and solve for $P$.",
                         {"driftless": "You used the driftless answer $2/3$. The negative drift pushes $X$ towards $-2$, so $P$ is lower.",
                          "no-sigma-squared": "You used $c = 2\\mu = -0.6$ and left $\\sigma^2$ out. The exponent is $2\\mu/\\sigma^2 = -0.7407$."})),
        dict(question="What is the mean exit time $E[\\tau]$? Give four decimal places.",
             widget=numeric(2.535, abs_=0.0005, placeholder="a decimal", label="Mean exit time",
                            wrong=[("driftless", 2.0, 0.0005), ("not-divided-by-mu", -0.7605, 0.0005)], accept="2.5350 within 0.0005"),
             feedback=fb("$E[X_\\tau] = P - 2(1 - P) = -0.7605$, and $E[X_\\tau] = \\mu E[\\tau]$, so $E[\\tau] = 2.5350$.",
                         "Wald gives $E[X_\\tau] = \\mu E[\\tau]$. Find $E[X_\\tau]$ from $P$ first.",
                         {"driftless": "You used the driftless $ab = 2$. With a drift, divide $E[X_\\tau]$ by $\\mu$.",
                          "not-divided-by-mu": "You stopped at $E[X_\\tau] = -0.7605$. Divide by $\\mu = -0.3$ to get the time."}))],
    explain="Part a stops $e^{-cX_t}$, which is a martingale for $c = 2\\mu/\\sigma^2$. Part b uses $X_t - \\mu t$, a martingale, so $E[X_\\tau] = \\mu E[\\tau]$. Both use $P = 0.41317$.")

# ---------------------------------------------------------------- I9
I[9] = item(
    "e-sixth-repair", 4, ["it-martingale", "it-calculus"], ["martingale-repair"], 180,
    title="Repair $W_t^6$",
    prose="Choose $a$, $b$ and $c$ so that $M_t = W_t^6 + a\\,tW_t^4 + b\\,t^2W_t^2 + c\\,t^3$ is a martingale. Write $w$ for $W_t$.",
    question="Write $M_t$ in full, as an expression in $t$ and $w$.",
    widget=expr("w^6-15tw^4+45t^2w^2-15t^3",
                accept=["w^6-15t w^4+45t^2 w^2-15t^3", "w^6 - 15*t*w^4 + 45*t^2*w^2 - 15*t^3"],
                wrong=[("no-constant", "w^6-15tw^4+45t^2w^2"), ("all-plus", "w^6+15tw^4+45t^2w^2+15t^3")]),
    feedback=fb("Setting the drift to zero gives $a = -15$, $b = 45$ and $c = -15$.",
                "Find the drift $f_t + \\tfrac12 f_{xx}$ and choose $a$, $b$, $c$ so each power of $w$ cancels.",
                {"no-constant": "Without the $t^3$ term the drift is $45t^2$, not zero. The constant $c = -15$ cancels it.",
                 "all-plus": "Every sign is plus, so the $w^4$ terms add instead of cancelling. The coefficients alternate: $-15$, $+45$, $-15$."}),
    explain="The drift is $(a + 15)w^4 + (6a + 2b)tw^2 + (b + 3c)t^2$. Each bracket must vanish, so $a = -15$, $b = 45$ and $c = -15$.")

# ---------------------------------------------------------------- I11
I[11] = parts_item(
    "e-cubed-claim", 5, ["it-pricing"], ["quick-pricing"], 300,
    title="A cubic payoff",
    prose="A share follows $dS = rS\\,dt + \\sigma S\\,dW$ under the pricing measure, with $S_0 = 2$, $r = 3\\%$ and $\\sigma = 40\\%$. A claim pays $S_T^m$ at $T = 2$ years. Its price is $S_0^m e^{cT}$ with $c = r(m - 1) + \\tfrac12\\sigma^2 m(m - 1)$.",
    question="Two follow-up questions.",
    parts=[
        dict(question="What is the price of the claim that pays $S_T^3$? Give four decimal places.",
             widget=numeric(23.5574, abs_=0.0005, placeholder="a decimal", label="Price",
                            wrong=[("no-discounting", 25.0141, 0.0005), ("no-convexity", 5.5814, 0.0005)], accept="23.5574 within 0.0005"),
             feedback=fb("Here $c = 0.03 \\cdot 2 + 0.08 \\cdot 6 = 0.54$, so the price is $2^3 e^{0.54 \\cdot 2} = 8e^{1.08} = 23.5574$.",
                         "Take $E[S_T^3]$ under the pricing measure, then discount by $e^{-rT}$.",
                         {"no-discounting": "You did not discount. $E[S_T^3] = 25.0141$, and the price is $e^{-0.06}$ times that.",
                          "no-convexity": "You dropped the convexity term $\\tfrac12 n^2\\sigma^2 T = 1.44$ in the exponent. A cube of a lognormal grows faster."})),
        dict(question="Find the power $m \\ne 1$ whose price never changes with time. Give three decimal places.",
             widget=numeric(-0.375, abs_=0.0005, placeholder="a decimal", label="Power m",
                            wrong=[("sign", 0.375, 0.0005), ("sigma-not-squared", -0.15, 0.0005)], accept="-0.375 within 0.0005"),
             feedback=fb("Set $c = 0$: $r + \\tfrac12\\sigma^2 m = 0$, so $m = -2r/\\sigma^2 = -0.375$.",
                         "Set $c = 0$ and divide out the factor $m - 1$.",
                         {"sign": "You gave $+0.375$. The factor is $r + \\tfrac12\\sigma^2 m = 0$, which needs $m$ negative.",
                          "sigma-not-squared": "You used $-2r/\\sigma = -0.15$. The equation has $\\sigma^2 = 0.16$."}))],
    explain="Part a is $e^{-rT}E[S_T^3]$ with the lognormal moment. Part b sets $c = 0$, so $r(m-1) + \\tfrac12\\sigma^2m(m-1) = 0$ and either $m = 1$ or $m = -2r/\\sigma^2$.")

ITEMS = I
