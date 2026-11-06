"""Build app/content/exams/mock-superday-strats.json (route A: closed forms and reference code).

Deterministic: random.Random(2611) orders the choice options only; every parameter is fixed below. Every key is
computed here once in closed form; superday_strats_check.py recomputes each by a second route and checks it at its path.
Code test expectations come from the reference solutions run in CPython (Python) and g++ (C++).
Run: python3 docs/briefs/mocks-scripts/superday_strats_build.py
"""
import json
import math
import os
import random
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from statistics import NormalDist

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from superday_lib import numeric, choice, fb, item, part, parts_item, longform, write  # noqa: E402

OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'mock-superday-strats.json')
rng = random.Random(2611)
N = NormalDist()
Phi = N.cdf

# ======================================================================== paper 1: probability
# P1 drift ruin: up 0.6, down 0.4, start 2 steps above the floor, stops 6 steps apart
p, q = F(3, 5), F(2, 5)
r_ = q / p
P_up = (1 - r_ ** 2) / (1 - r_ ** 6)
assert P_up == F(81, 133)
ET = (4 * P_up - 2 * (1 - P_up)) / (p - q)
assert ET == F(1100, 133)
P1 = parts_item(
    'p1-drift-ruin', 4, ['mc-walks'], ['ruin-with-drift', 'wald-identity'], 420, 'A walk with drift',
    'A price moves up £1 with chance 0.6 or down £1 with chance 0.4 at each step, independently. '
    'It starts at £50. You stop when it reaches £54 or £48.',
    [part('Find the probability that £54 comes before £48. Give four decimals.',
          numeric(0.6090, 0.0005, wr1 := [('fair', 0.3333, 0.0005, 'You used the fair-game answer, 2 steps out of 6. The drift makes the top more likely.'),
                                           ('one-step', 0.6, 0.0005, 'You gave the chance of one up step, not of reaching the top first.'),
                                           ('lower', 0.3910, 0.0005, 'You gave the chance of reaching £48 first.')],
                  placeholder='four decimals', accept='0.6090 (81/133, within 0.0005)'),
          fb('The ratio $q/p = 2/3$ in the ruin formula gives $81/133$.', 'Write the ruin formula with $r = q/p$, from 2 steps above the floor.', wr1),
          'With $r = q/p = 2/3$, $P = (1 - r^2)/(1 - r^6) = 81/133 \\approx 0.6090$. '
          'A linear solve over the five states between the stops gives the same value.'),
     part('What is the expected number of steps until you stop? Give two decimals.',
          numeric(8.27, 0.01, wr2 := [('fair-rule', 8, 0.01, 'You used the fair-game rule, 4 times 2. A drift shortens the walk.'),
                                      ('no-drift', 1.65, 0.01, 'You found the expected gain in pounds but did not divide by the drift of 0.2 a step.')],
                  placeholder='two decimals', accept='8.27 (1100/133, within 0.01)'),
          fb('Wald: expected gain over drift per step.', 'Find the expected end point, then divide by the average gain per step.', wr2),
          'The expected end point is $4P - 2(1 - P) = 220/133$ pounds above the start. '
          'Each step gains 0.2 on average, so $E[T] = (220/133)/0.2 = 1100/133 \\approx 8.27$. '
          'A linear solve for the expected steps from each state agrees.')])

# P2 orthant chance for correlation 0.5
rho = 0.5
orth = 0.25 + math.asin(rho) / (2 * math.pi)
assert abs(orth - 1 / 3) < 1e-15
P2 = item('p2-orthant', 4, ['rv-joint'], ['orthant-correlation'], 240, 'Both up',
          'Two daily returns are jointly normal with mean 0 and correlation 0.5. What is the chance that both are positive?',
          choice(rng, [('$1/3$', None),
                       ('$1/4$', 'You multiplied $1/2 \\times 1/2$, as if the two returns were independent.'),
                       ('$3/8$', 'You moved a straight line from $1/4$ at no correlation to $1/2$ at full correlation.'),
                       ('$1/6$', 'You used a correlation of $-0.5$, a sign slip in the arcsine.')]),
          fb('The arcsine rule: $1/4 + \\arcsin(\\rho)/(2\\pi)$.', 'Write one return as $\\rho X + \\sqrt{1 - \\rho^2} Z$ and look at angles.'),
          'The pair is a rotated standard normal, so the chance is an angle over $2\\pi$. '
          'That gives $1/4 + \\arcsin(0.5)/(2\\pi) = 1/4 + 1/12 = 1/3$. '
          'Integrating the joint density over the quadrant gives the same.')

# P3 first-to-last gap of four uniform arrivals in 60 minutes
n4 = 4
gap = F(60) * F(n4 - 1, n4 + 1)
assert gap == 36
P3 = item('p3-first-last-gap', 3, ['rv-expect'], ['range-of-uniforms'], 180, 'First to last',
          'Four orders arrive at independent uniform times in a 60-minute window. '
          'What is the expected time from the first arrival to the last, in minutes?',
          numeric(36, 0.05, wr3 := [('last-only', 48, 0.05, 'You gave the expected time of the last arrival, not its gap from the first.'),
                                    ('half', 30, 0.05, 'You took half the window. Even two arrivals are only a third of the window apart on average.'),
                                    ('three-quarters', 45, 0.05, 'You took $(n - 1)/n$ of the window. The right share is $(n - 1)/(n + 1)$.')],
                  placeholder='minutes', unit='min', accept='36 minutes'),
          fb('$E[\\max] - E[\\min] = 48 - 12$.', 'Find the expected last and first arrival times separately.', wr3),
          'The last of four uniform times has mean $\\tfrac45 \\times 60 = 48$, and the first has mean $\\tfrac15 \\times 60 = 12$. '
          'The gap is $36$ minutes, or $\\tfrac35$ of the window. '
          'Integrating $1 - x^4$ and $(1 - x)^4$ gives the same two means.')

# P4 Poisson thinning
lam, pc, cancels = 18, F(2, 3), 10
others = lam * (1 - pc)
assert others == 6
P4 = item('p4-poisson-thinning', 4, ['dl-discrete'], ['poisson-thinning'], 240, 'Cancels and the rest',
          'Messages reach a matching engine as a Poisson stream, 18 a second. Each is a cancel with chance $2/3$, independently. '
          'In one second you count 10 cancels. How many other messages do you expect in that second?',
          choice(rng, [('6', None),
                       ('8', 'You took the 10 cancels from the average of 18. The other messages do not depend on the cancels.'),
                       ('5', 'You scaled the 10 cancels by one other message per two cancels, as if the split were fixed.'),
                       ('18', 'You gave the rate of all messages, not of the others.')]),
          fb('Thinning splits a Poisson stream into independent streams.', 'Split the messages into a cancel stream and a stream of the rest.'),
          'Cancels and the rest are independent Poisson streams, at 12 and 6 a second. '
          'Seeing 10 cancels says nothing about the rest, so the answer is $18 \\times \\tfrac13 = 6$. '
          'Summing over the total count with the binomial split gives 6 too.')

# P5 expected larger of two correlated N(0, 2%^2) returns
sig, rho5 = 0.02, 0.5
emax = sig * math.sqrt((1 - rho5) / math.pi)
P5 = item('p5-max-of-two-normals', 4, ['rv-expect'], ['max-of-two-normals'], 240, 'The better of two days',
          'Two daily returns are jointly normal, each with mean 0 and standard deviation 2%, with correlation 0.5. '
          'What is the expected value of the larger one?',
          numeric(round(emax, 6), 0.00005, wr5 := [('no-correlation', 0.011284, 0.00005, 'You ignored the correlation and used $2\\%/\\sqrt{\\pi}$. A positive correlation pulls the two returns together.'),
                                                   ('abs-value', 0.015958, 0.00005, 'You gave $E|X| = \\sigma\\sqrt{2/\\pi}$ for one return. The larger of two is half of $E|X - Y|$.'),
                                                   ('zero', 0, 0.00005, 'You used symmetry on the larger one. The larger of two is above 0 on average.')],
                  placeholder='per cent, two decimals', unit='%', accept='0.80% ($\\sigma\\sqrt{(1 - \\rho)/\\pi} = 0.00798$)'),
          fb('$\\max(X, Y) = \\tfrac12(X + Y) + \\tfrac12|X - Y|$.', 'Write the larger as the mean plus half the gap.', wr5),
          'Write $\\max(X, Y) = \\tfrac12(X + Y) + \\tfrac12|X - Y|$. '
          'The gap $X - Y$ has standard deviation $2\\%\\sqrt{2(1 - 0.5)} = 2\\%$, so $E|X - Y| = 2\\%\\sqrt{2/\\pi}$. '
          'Then $E[\\max] = \\tfrac12 \\times 2\\% \\times \\sqrt{2/\\pi} = 2\\%\\sqrt{0.5/\\pi} \\approx 0.80\\%$.')

# ======================================================================== paper 2: pricing
# R1 at-the-money rule of thumb: S 250, vol 20%, T 0.25, r 0
S1, v1, T1 = 250, 0.2, 0.25
bs_atm = S1 * (2 * Phi(v1 * math.sqrt(T1) / 2) - 1)
thumb = 0.4 * S1 * v1 * math.sqrt(T1)
assert abs(bs_atm - 9.9695) < 1e-4 and abs(thumb - 10) < 1e-12
R1 = item('r1-atm-rule', 3, ['tp-bs'], ['atm-approximation'], 150, 'A call in your head',
          'A stock trades at £250 and pays no dividend, and rates are 0. An at-the-money call has three months to run. '
          'Its implied volatility is 20%. Estimate the call price to the nearest 10p.',
          numeric(9.97, 0.1, wr6 := [('full-year', 20, 0.1, 'You used a full year. Three months gives $\\sqrt{0.25} = 0.5$.'),
                                     ('used-T', 5, 0.1, 'You multiplied by $T = 0.25$, not by $\\sqrt{T} = 0.5$.')],
                  placeholder='pounds', unit='£', accept='£10.0 by the rule of thumb (£9.97 exactly), within 10p'),
          fb('$0.4\\,S\\sigma\\sqrt{T} = £10$.', 'Use the at-the-money rule $C \\approx 0.4\\,S\\sigma\\sqrt{T}$.', wr6),
          'The rule $C \\approx 0.4\\,S\\sigma\\sqrt{T}$ gives $0.4 \\times 250 \\times 0.2 \\times 0.5 = £10$. '
          'Black-Scholes with $r = 0$ gives $250\\,(2\\Phi(0.05) - 1) = £9.97$. '
          'The 0.4 is $1/\\sqrt{2\\pi}$ rounded.')

# R2 put-call parity arbitrage
C2, P2_, S2, K2, DF2 = F(720, 100), F(410, 100), 52, 50, F(98, 100)
rich = (C2 - P2_) - (S2 - K2 * DF2)
assert rich == F(1, 10) and K2 * DF2 == 49
R2 = item('r2-parity-arbitrage', 3, ['op-parity'], ['parity-arbitrage'], 240, 'A riskless profit',
          'A stock is at £52 and pays no dividend. One-year European options struck at £50 trade at £7.20 for the call and £4.10 for the put. '
          'The one-year discount factor is 0.98. Which trade locks in a riskless profit today?',
          choice(rng, [('Sell the call, buy the put and the stock, and borrow £49: £0.10 now', None),
                       ('Buy the call, sell the put, short the stock and lend £49: £0.10 now',
                        'You reversed the trade. Buying the rich side loses the £0.10.'),
                       ('No trade, because the call should cost more than the put when in the money',
                        'You compared the call with the put, not $C - P$ with $S - K \\times 0.98$.'),
                       ('Sell the call, buy the put and the stock, and borrow £50: £1.10 now',
                        'You borrowed the strike, not its present value. Repaying £50 a year later costs more than £50 today.')]),
          fb('$C - P = 3.10$ against $S - 0.98K = 3.00$.', 'Compare $C - P$ with $S$ minus the present value of the strike.'),
          'Parity says $C - P = S - 0.98 \\times 50 = 52 - 49 = £3.00$, but the market has $7.20 - 4.10 = £3.10$. '
          'So sell the call, buy the put and the stock, and borrow £49: cash today is $7.20 - 4.10 - 52 + 49 = £0.10$. '
          'At expiry the stock settles the options and repays the £50 owed, whatever the price.')

# R3 gamma and theta P&L of a hedged book
G3, TH3, dS3, n3 = F(4, 100), F(-40, 100), 5, 300
pnl3 = n3 * (F(1, 2) * G3 * dS3 ** 2 + TH3)
assert pnl3 == 30
R3 = item('r3-gamma-theta', 4, ['op-greeks'], ['gamma-theta-pnl'], 300, 'A hedged day',
          'You hold 300 calls, delta hedged. Each call has gamma 0.04 per pound and theta $-£0.40$ a day. '
          'Today the stock moves £5. Estimate the day’s P&L of the hedged book, in pounds.',
          numeric(30, 0.5, wr7 := [('no-theta', 150, 0.5, 'You left out the theta of $-£0.40$ a call.'),
                                   ('no-half', 180, 0.5, 'You used $\\Gamma (\\Delta S)^2$ without the half.'),
                                   ('theta-only', -120, 0.5, 'You counted the theta but not the gamma gain.')],
                  placeholder='pounds', unit='£', accept='£30'),
          fb('$\\tfrac12 \\Gamma (\\Delta S)^2 + \\Theta$ a call, times 300.', 'A hedged option earns $\\tfrac12 \\Gamma (\\Delta S)^2$ and pays its theta.', wr7),
          'Each call earns $\\tfrac12 \\times 0.04 \\times 5^2 = £0.50$ from gamma and pays £0.40 of theta. '
          'That is £0.10 a call, so £30 for 300. '
          'Repricing a quadratic value with that gamma and theta over the day gives £30 too.')

# R4 digital from a call spread
C99, C101 = F(540, 100), F(430, 100)
dig = (C99 - C101) / 2
assert dig == F(55, 100)
R4 = item('r4-digital-spread', 3, ['op-greeks', 'tp-bs'], ['digital-from-calls'], 240, 'A digital from calls',
          'Calls on one stock with one expiry trade at £5.40 for strike £99 and £4.30 for strike £101. '
          'Estimate the price of a digital call that pays £1 if the stock ends above £100.',
          numeric(0.55, 0.005, wr8 := [('no-width', 1.10, 0.005, 'You did not divide by the £2 between the strikes.'),
                                       ('digital-put', 0.45, 0.005, 'You gave $1 - 0.55$, the digital put with no discounting.')],
                  placeholder='pounds', unit='£', accept='£0.55'),
          fb('$(C(99) - C(101))/2$.', 'A digital is minus the slope of the call price in the strike.', wr8),
          'A call spread of 99 against 101, scaled by $1/2$, pays £1 above 101 and nothing below 99. '
          'So the digital is about $(5.40 - 4.30)/2 = £0.55$. '
          'This is $-\\partial C/\\partial K$ taken by a central difference.')

# R5 Monte Carlo error: 90,000 paths, payoff standard deviation 27, two standard errors
n5, sd5, half_target = 90000, 27, F(6, 100)
se5 = F(sd5) / math.isqrt(n5)
half5 = 2 * se5
need5 = (2 * F(sd5) / half_target) ** 2
assert se5 == F(9, 100) and half5 == F(18, 100) and need5 == 810000
R5 = parts_item(
    'r5-mc-error', 3, ['nm-mc'], ['mc-interval-paths'], 300, 'How many paths',
    'After 90,000 paths a Monte Carlo pricer reports £8.41. The discounted payoffs have sample standard deviation £27. '
    'Take a 95% interval as two standard errors either side.',
    [part('How wide is half of that interval, in pounds?',
          numeric(0.18, 0.0005, wr9 := [('one-se', 0.09, 0.0005, 'You gave one standard error. The interval reaches two either side.'),
                                        ('over-n', 0.0006, 0.00005, 'You divided by $n$, not by $\\sqrt{n}$.')],
                  placeholder='pounds', unit='£', accept='£0.18'),
          fb('$2 \\times 27/\\sqrt{90000} = 2 \\times 0.09$.', 'The standard error of a mean is the standard deviation over $\\sqrt{n}$.', wr9),
          'The price is a mean of 90,000 payoffs, so its standard error is $27/300 = £0.09$. '
          'Two of them give a half-width of £0.18, so the interval is £8.23 to £8.59.'),
     part('How many paths bring that half-width down to £0.06?',
          numeric(810000, 0.5, wr10 := [('linear', 270000, 0.5, 'You scaled the paths by 3. The error falls with $\\sqrt{n}$, so you need 9 times as many.'),
                                        ('no-square', 900, 0.5, 'You found $2 \\times 27/0.06$ but did not square it.')],
                  placeholder='paths', accept='810,000 paths'),
          fb('$(2 \\times 27/0.06)^2$.', 'Solve $2 \\times 27/\\sqrt{n} = 0.06$ for $n$.', wr10),
          'Solve $54/\\sqrt{n} = 0.06$: $\\sqrt{n} = 900$, so $n = 810{,}000$. '
          'That is 9 times 90,000, because a third of the error needs 9 times the paths.')])

# R6 Crank-Nicolson error at four times the steps
e100 = F(48, 10000)
e400 = e100 / 16
assert e400 == F(3, 10000)
R6 = item('r6-convergence-order', 3, ['nm-fd'], ['convergence-order'], 180, 'A finer grid',
          'A Crank-Nicolson pricer has error 0.0048 with 100 time steps and 100 price steps. '
          'Its error is second order in the step. Roughly what is the error with 400 of each?',
          choice(rng, [('0.0003', None),
                       ('0.0012', 'You assumed first order, so you divided by 4.'),
                       ('0.000075', 'You divided by 64, which is third order.'),
                       ('0.0024', 'You halved the error, as if the steps had only doubled.')]),
          fb('Second order: a step 4 times smaller cuts the error 16 times.', 'Square the ratio of the step sizes.'),
          'The step falls by 4, and a second-order error falls by $4^2 = 16$. '
          'So $0.0048/16 = 0.0003$. '
          'This holds once the steps are small enough for the leading term to dominate.')

# R7 longform: realised against implied
G7, S7, vr, vi, T7 = 0.07, 100, 0.25, 0.20, 1 / 12
pnl7 = 0.5 * G7 * S7 ** 2 * (vr ** 2 - vi ** 2) * T7
assert abs(pnl7 - 0.65625) < 1e-12
R7 = longform(
    'r7-realised-vs-implied', 5, ['op-greeks', 'tp-bs'], ['realised-vs-implied'], 900, 'Where the P&L comes from',
    'Answer aloud first. Then write your answer down, in 250 words or fewer.\n\n'
    'You buy a one-month at-the-money call at 20% implied volatility and delta hedge it daily. '
    'The stock then realises 25% volatility. Explain where your P&L comes from. '
    'Then estimate it for a call with the stock at £100. Rates are 0. Take gamma as constant at 0.07 per pound, about its Black-Scholes value. '
    'Take one month as $1/12$ of a year.',
    '*An example answer. Your own words are the real answer.*\n\n'
    'Each day the hedged call earns from gamma and pays theta. The gamma gain is $\\tfrac12 \\Gamma (\\Delta S)^2$. '
    'Theta is set by the implied volatility, so it costs $\\tfrac12 \\Gamma S^2 \\sigma_{imp}^2 \\Delta t$ a day.\n\n'
    'Over the month the P&L is about $\\tfrac12 \\Gamma S^2 (\\sigma_{real}^2 - \\sigma_{imp}^2) T$. '
    'Here that is $\\tfrac12 \\times 0.07 \\times 100^2 \\times (0.0625 - 0.04) \\times \\tfrac1{12}$. '
    'That is about £0.66 a call.\n\n'
    'When realised equals implied, the gain and the cost cancel on average. '
    'So I make money because realised volatility beat implied, whichever way the stock went.\n\n'
    'Two caveats. Gamma changes as the stock moves, so the result depends on the path. '
    'Daily hedging also adds noise around this average.',
    [(2, 'Splits the daily P&L into a gamma gain and a theta cost'),
     (2, 'Says theta is priced at the implied volatility, so the two cancel when realised equals implied'),
     (2, 'Gives $\\tfrac12 \\Gamma S^2 (\\sigma_{real}^2 - \\sigma_{imp}^2) T$, or the same in words'),
     (2, 'Estimates about £0.66 a call (£0.65 or £0.66 is fine)'),
     (1, 'Says the sign does not depend on the direction of the stock'),
     (1, 'Names one caveat: gamma moves with the path, or hedging is discrete')])

# ======================================================================== paper 3: stochastic calculus
# S1 (W + a t) e^{W - t/2} martingale: drift (a + 1) e^{W - t/2} = 0, so a = -1; then E[W_2 e^{W_2 - 1}] = 2
a_, e2 = -1, 2
S1i = parts_item(
    's1-exponential-correction', 4, ['it-calculus', 'it-martingale'], ['exponential-martingale'], 360, 'Correct an exponential',
    '$W_t$ is a standard Brownian motion. You want $(W_t + a\\,t)\\,e^{W_t - t/2}$ to be a martingale, with $a$ a constant.',
    [part('What must $a$ be?',
          numeric(a_, 0, wr11 := [('sign-slip', 1, 0, 'You solved $a - 1 = 0$. The drift is $(a + 1)e^{W_t - t/2}$, so the sign flips.'),
                                  ('zero', 0, 0, 'You set $a = 0$, taking $W_t e^{W_t - t/2}$ as a martingale. It has drift $e^{W_t - t/2}$.')],
                  placeholder='a whole number', accept='-1'),
          fb('The drift is $(a + 1)e^{W_t - t/2}$.', 'Apply the product rule with $d(e^{W_t - t/2}) = e^{W_t - t/2}\\,dW_t$ and set the drift to 0.', wr11),
          'Write $M = e^{W_t - t/2}$, so $dM = M\\,dW$. '
          'The product rule gives $d[(W + at)M] = M(dW + a\\,dt) + (W + at)M\\,dW + M\\,dt$. '
          'The $dt$ terms are $(a + 1)M\\,dt$, so $a = -1$.'),
     part('Use that martingale to find $E[W_2\\,e^{W_2 - 1}]$.',
          numeric(e2, 0.005, wr12 := [('independent', 0, 0.005, 'You treated $W_2$ and $e^{W_2 - 1}$ as independent, so the product has mean 0.'),
                                      ('no-compensator', 5.4366, 0.005, 'You left out the factor $e^{-1}$ and found $E[W_2\\,e^{W_2}] = 2e$.')],
                  placeholder='two decimals', accept='2 (within 0.005)'),
          fb('$E[(W_2 - 2)e^{W_2 - 1}] = 0$ and $E[e^{W_2 - 1}] = 1$.', 'A martingale started at 0 has mean 0. Split it into two expectations.', wr12),
          'The martingale $(W_t - t)e^{W_t - t/2}$ starts at 0, so $E[(W_2 - 2)e^{W_2 - 1}] = 0$. '
          'Hence $E[W_2 e^{W_2 - 1}] = 2E[e^{W_2 - 1}] = 2$, since $e^{W_t - t/2}$ has mean 1. '
          'Integrating against the normal density of $W_2$ gives the same.')])

# S2 median of GBM
S0g, mu, sg, Tg = 40, 0.10, 0.40, 2
med = S0g * math.exp((mu - sg ** 2 / 2) * Tg)
mean = S0g * math.exp(mu * Tg)
S2i = item('s2-gbm-median', 3, ['it-bm'], ['gbm-median'], 200, 'The middle outcome',
           'A stock follows geometric Brownian motion with drift 10% and volatility 40% a year. '
           'It is at £40 today. What is its median price in two years?',
           choice(rng, [(f'£{med:.2f}', None),
                        (f'£{mean:.2f}', 'You gave the mean, $40e^{0.2}$. The median takes off half the variance.'),
                        (f'£{S0g * math.exp((mu - sg ** 2) * Tg):.2f}', 'You took off the whole variance, $\\sigma^2$, not half of it.'),
                        (f'£{S0g * math.exp((mu - sg ** 2 / 2) * 1):.2f}', 'You used one year, not two.')]),
           fb('The median is $S_0 e^{(\\mu - \\sigma^2/2)T}$.', 'The log price is normal; its median is its mean.'),
           f'The log price is normal with mean $\\ln 40 + (0.10 - 0.08) \\times 2$, so the median is $40e^{{0.04}} = £{med:.2f}$. '
           f'The mean is larger, $40e^{{0.2}} = £{mean:.2f}$, because the distribution is skewed to the right.')
assert abs(med - 41.63) < 0.005 and abs(mean - 48.86) < 0.005

# S3 touch probability by reflection
a3, s3, T3 = 3, 2, 1
touch = 2 * (1 - Phi(a3 / (s3 * math.sqrt(T3))))
S3i = item('s3-touch', 4, ['it-bm'], ['reflection-touch'], 300, 'Touching a level',
           'A price follows Brownian motion with no drift and volatility £2 per square-root day. '
           'What is the chance it touches £3 above today\u2019s level within one day? Take $\\Phi(1.5) = 0.9332$. Give three decimals.',
           numeric(round(touch, 4), 0.001, wr13 := [('no-reflection', 0.0668, 0.0005, 'You gave the chance it ends above the level. Reflection doubles it.'),
                                                    ('stays-below', 0.8664, 0.0005, 'You gave the chance it never touches.')],
                   placeholder='three decimals', accept=f'{touch:.3f} (within 0.001)'),
           fb('$P(\\max \\ge a) = 2P(W_T \\ge a)$.', 'Use the reflection principle on the first touch.', wr13),
           f'By reflection, $P(\\max \\ge 3) = 2P(X_1 \\ge 3) = 2(1 - \\Phi(1.5)) = {touch:.3f}$. '
           'Integrating the density of the first touching time up to one day gives the same.')

# S4 longform: log contract
S04, r4, s4, T4 = 100, 0.02, 0.20, 1
Elog = math.log(S04) + (r4 - s4 ** 2 / 2) * T4
price4 = math.exp(-r4 * T4) * Elog
assert abs(price4 - 4.5140) < 5e-5
S4i = longform(
    's4-log-contract', 5, ['it-pricing', 'it-calculus'], ['log-contract'], 900, 'A log contract',
    'Answer aloud first. Then write your answer down, in 250 words or fewer.\n\n'
    'Under Black-Scholes with no dividends, price a contract that pays $\\ln S_T$ at time $T$. '
    'Use a spot of 100, a rate of 2%, volatility of 20% and one year to run. '
    'Then say why a desk links this contract to variance.',
    '*An example answer. Your own words are the real answer.*\n\n'
    'Under the pricing measure $dS = rS\\,dt + \\sigma S\\,dW$. '
    'It\u00f4\u2019s lemma on $\\ln S$ gives $d\\ln S = (r - \\tfrac12\\sigma^2)\\,dt + \\sigma\\,dW$. '
    'So $E[\\ln S_T] = \\ln S_0 + (r - \\tfrac12\\sigma^2)T$.\n\n'
    f'Here $r - \\tfrac12\\sigma^2 = 0.02 - 0.02 = 0$, so the expectation is $\\ln 100 = {Elog:.4f}$. '
    f'Discounting gives $e^{{-0.02}} \\times {Elog:.4f} = {price4:.4f}$.\n\n'
    'The same lemma gives the variance link. '
    'Rearranged, $\\int_0^T \\sigma^2\\,dt = 2\\int_0^T dS/S - 2\\ln(S_T/S_0)$. '
    'The first term is a delta hedge, and the second is a short position in log contracts. '
    'So log contracts plus a hedge replicate realised variance. '
    'That is how a variance swap is priced from a strip of options.',
    [(2, 'Applies It\u00f4\u2019s lemma to $\\ln S$ and gets the $-\\tfrac12\\sigma^2$ term'),
     (2, 'Uses the risk-neutral drift $r$ and states $E[\\ln S_T] = \\ln S_0 + (r - \\tfrac12\\sigma^2)T$'),
     (1, f'Discounts to about {price4:.2f}'),
     (2, 'Writes realised variance as $2\\int dS/S - 2\\ln(S_T/S_0)$'),
     (2, 'Names the $dS/S$ term as a delta hedge. Names the log term as a static position, priced from a strip of options'),
     (1, 'Gives the price before moving on to the variance link')])

# ======================================================================== paper 4: coding
CRR1 = """import math


def crr_value(S, K, T, r, sigma, n, call=True):
    if n < 1:
        raise ValueError("need at least one step")
    dt = T / n
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    p = (math.exp(r * dt) - d) / (u - d)
    if not 0 < p < 1:
        raise ValueError("no risk-neutral probability")
    disc = math.exp(-r * dt)
    sign = 1 if call else -1
    values = [max(sign * (S * u ** j * d ** (n - j) - K), 0.0) for j in range(n + 1)]
    for step in range(n - 1, -1, -1):
        values = [disc * (p * values[j + 1] + (1 - p) * values[j]) for j in range(step + 1)]
    return values[0]
"""
CRR2 = """import math


def crr_value(S, K, T, r, sigma, n, call=True, barrier=None):
    if n < 1:
        raise ValueError("need at least one step")
    dt = T / n
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    p = (math.exp(r * dt) - d) / (u - d)
    if not 0 < p < 1:
        raise ValueError("no risk-neutral probability")
    disc = math.exp(-r * dt)
    sign = 1 if call else -1

    def alive(price):
        return barrier is None or price > barrier

    values = []
    for j in range(n + 1):
        price = S * u ** j * d ** (n - j)
        values.append(max(sign * (price - K), 0.0) if alive(price) else 0.0)
    for step in range(n - 1, -1, -1):
        values = [disc * (p * values[j + 1] + (1 - p) * values[j]) if alive(S * u ** j * d ** (step - j)) else 0.0
                  for j in range(step + 1)]
    return values[0]
"""
START1 = """import math


def crr_value(S, K, T, r, sigma, n):
    # A European call on an n-step Cox-Ross-Rubinstein tree.
    # Add call=True (False prices a put) and the two input checks.
    dt = T / n
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    p = (math.exp(r * dt) - d) / (u - d)
    disc = math.exp(-r * dt)
    values = [max(S * u ** j * d ** (n - j) - K, 0.0) for j in range(n + 1)]
    for step in range(n - 1, -1, -1):
        values = [disc * (p * values[j + 1] + (1 - p) * values[j]) for j in range(step + 1)]
    return values[0]
"""
START2 = CRR1.replace('def crr_value(S, K, T, r, sigma, n, call=True):', 'def crr_value(S, K, T, r, sigma, n, call=True, barrier=None):\n    # TODO: worth 0 at every node at or below the barrier')

ns1, ns2 = {}, {}
exec(CRR1, ns1)
exec(CRR2, ns2)
calls1 = ['crr_value(100, 95, 0.5, 0.03, 0.25, 3)', 'crr_value(80, 90, 2, 0.01, 0.3, 50)', 'crr_value(100, 100, 1, 0.05, 0.2, 1000)',
          'crr_value(100, 105, 1, 0.04, 0.25, 10, call=False)', 'crr_value(60, 55, 0.75, 0.02, 0.35, 7, call=False)']
calls2 = ['crr_value(100, 100, 1, 0.05, 0.2, 50, barrier=105)', 'crr_value(100, 100, 1, 0.05, 0.2, 200, barrier=1)',
          'crr_value(100, 100, 1, 0.05, 0.2, 4, barrier=95)', 'crr_value(100, 95, 0.5, 0.03, 0.25, 12, barrier=92)',
          'crr_value(100, 100, 1, 0.05, 0.2, 400, barrier=95)', 'crr_value(80, 90, 2, 0.01, 0.3, 50, call=False, barrier=70)',
          'crr_value(100, 100, 1, 0.05, 0.2, 50, barrier=100)']
TOL = {'rel': 1e-9, 'abs': 1e-9}


def pytest_(call, ns):
    return {'call': call, 'expect': repr(float(eval(call, ns))), 'compare': 'isclose', 'tol': TOL}


tests1 = [pytest_(c, ns1) for c in calls1] + [
    {'call': 'crr_value(100, 100, 1, 0.05, 0.2, 0)', 'expect': 'ValueError', 'compare': 'raises'},
    {'call': 'crr_value(100, 100, 1, 0.5, 0.01, 1)', 'expect': 'ValueError', 'compare': 'raises'},
    {'call': 'crr_value(100, 100, 1, -0.5, 0.01, 1)', 'expect': 'ValueError', 'compare': 'raises'}]
tests2 = [pytest_(c, ns2) for c in calls2]
ex1 = [dict(tests1[i], expect=f'{float(tests1[i]["expect"]):.6f}') for i in (0, 3)]
ex2 = [dict(tests2[i], expect=f'{float(tests2[i]["expect"]):.6f}') for i in (2, 3)]
for e in ex1 + ex2:
    e['tol'] = {'abs': 5e-7}
C1 = parts_item(
    'c1-barrier-tree', 4, ['tp-multistep', 'cx-pricers'], ['barrier-tree', 'crr-tree'], 1320, 'A tree, then a barrier',
    'Extend a binomial tree pricer, then change it when the interviewer adds a barrier.',
    [part('Here is a working European call pricer on an `n`-step Cox-Ross-Rubinstein tree. '
          'Add `call=True`, so that `call=False` prices a put, which pays $\\max(K - S_T, 0)$. '
          'The risk-neutral up chance `p` must lie strictly between 0 and 1. '
          'Raise `ValueError` if `n` is below 1 or `p` is outside that range.',
          {'kind': 'code', 'language': 'python', 'starter': START1, 'examples': ex1, 'tests': tests1, 'solution': CRR1,
           'how': f'Submit runs {len(tests1)} hidden tests. Prices are accepted within a relative and absolute 1e-9.'},
          fb('Flip the sign inside the payoff for a put, and test `n` and `p` before stepping back.',
             'Only the last layer’s payoff changes for a put. Check `n` first, then compute `p` and test it.'),
          'A put pays $\\max(K - S, 0)$, so only the payoff at the last layer changes. '
          'Put-call parity holds exactly on the tree, $P = C - S + Ke^{-rT}$. '
          'With 1,000 steps the call is within a few pence of Black-Scholes.'),
     part('The interviewer adds a down-and-out barrier. Add `barrier=None`. '
          'The option is worth 0 at any node where the price is at or below `barrier`. That includes the start and the last layer.',
          {'kind': 'code', 'language': 'python', 'starter': START2, 'examples': ex2, 'tests': tests2, 'solution': CRR2,
           'how': f'Submit runs {len(tests1) + len(tests2)} hidden tests: the {len(tests1)} from part 1 and {len(tests2)} new ones. '
                  'Prices are accepted within a relative and absolute 1e-9.'},
          fb('Zero every node at or below the barrier as you step back.',
             'Check each node’s price against the barrier at every layer, the start included, not only at the end.'),
          'A dead node passes 0 to its parents, so every path that touches the barrier pays nothing. '
          'Checking only the last layer gives a European option with a cut payoff, not a barrier.'),
     part('As you raise `n`, your barrier price jumps up and down instead of settling. Why?',
          choice(rng, [('The barrier falls between node levels, which move with `n`', None),
                       ('Floating-point rounding builds up over the many steps',
                        'You blamed the arithmetic. Rounding moves prices by about 1e-12, and the jumps are far larger.'),
                       ('The risk-neutral $p$ leaves the range 0 to 1 for large `n`',
                        'You expected $p$ to fail. As `n` grows, $p$ tends to one half.'),
                       ('A barrier option has no limit as `n` grows',
                        'You expected no limit. The price tends to the continuous-barrier value, slowly.')]),
          fb('The tree’s effective barrier is the node level just below it.',
             'Look at where the barrier sits between the nodes of the tree.'),
          'The tree knocks out at the first node level at or below the barrier. '
          'That level moves as `n` changes, so the price saws. '
          'Choosing `n` so a node layer sits on the barrier fixes it.')])

# C2 C++ total-variance interpolation
VOL_SOL = '''#include <cmath>
#include <vector>

double vol_at(const std::vector<double>& T, const std::vector<double>& vols, double t) {
    const std::size_t n = T.size();
    for (std::size_t i = 1; i < n; ++i)
        if (vols[i] * vols[i] * T[i] < vols[i - 1] * vols[i - 1] * T[i - 1]) return -1.0;
    if (t <= T[0]) return vols[0];
    if (t >= T[n - 1]) return vols[n - 1];
    std::size_t i = 1;
    while (T[i] < t) ++i;
    const double w0 = vols[i - 1] * vols[i - 1] * T[i - 1];
    const double w1 = vols[i] * vols[i] * T[i];
    const double w = w0 + (w1 - w0) * (t - T[i - 1]) / (T[i] - T[i - 1]);
    return std::sqrt(w / t);
}
'''
VOL_START = '''#include <cmath>
#include <vector>

// A colleague's draft: it interpolates the vols themselves.
// Fix it: interpolate total variance, vol * vol * T,
// linearly in time, and return the vol that it implies.
// Before the first pillar keep its vol; after the last, likewise.
// Return -1.0 if any pillar's total variance is below the one before it
// (a calendar arbitrage), wherever t is. Equal is allowed.
double vol_at(const std::vector<double>& T, const std::vector<double>& vols, double t) {
    const std::size_t n = T.size();
    if (t <= T[0]) return vols[0];
    if (t >= T[n - 1]) return vols[n - 1];
    std::size_t i = 1;
    while (T[i] < t) ++i;
    return vols[i - 1] + (vols[i] - vols[i - 1]) * (t - T[i - 1]) / (T[i] - T[i - 1]);
}
'''
VOL_ARGS = [([0.25, 1.0], [0.2, 0.25], 0.5), ([0.25, 1.0], [0.2, 0.25], 1.0), ([0.25, 1.0], [0.2, 0.25], 0.1),
            ([0.25, 1.0], [0.2, 0.25], 3.0), ([0.5, 1.0], [0.3, 0.2], 0.75), ([0.25, 0.5, 1.0], [0.3, 0.26, 0.24], 0.75),
            ([0.25, 0.5, 1.0], [0.3, 0.2, 0.3], 0.1), ([1.0], [0.22], 0.5), ([0.5, 2.0], [0.4, 0.2], 1.0)]
TYPES = ['std::vector<double>', 'std::vector<double>', 'double']


def run_cpp(src, call):
    with tempfile.TemporaryDirectory() as td:
        open(os.path.join(td, 'm.cpp'), 'w').write(src + '\n#include <cstdio>\nint main() { std::printf("%.17g\\n", (double)(' + call + ')); }\n')
        subprocess.run(['g++', '-std=c++17', '-O1', os.path.join(td, 'm.cpp'), '-o', os.path.join(td, 'm')], check=True)
        return float(subprocess.run([os.path.join(td, 'm')], capture_output=True, text=True, check=True).stdout)


def cpp_lit(v):
    return '{' + ', '.join(repr(float(x)) for x in v) + '}' if isinstance(v, list) else repr(float(v))


vol_tests = []
for a in VOL_ARGS:
    got = run_cpp(VOL_SOL, 'vol_at(std::vector<double>' + cpp_lit(a[0]) + ', std::vector<double>' + cpp_lit(a[1]) + ', ' + cpp_lit(a[2]) + ')')
    vol_tests.append({'call': 'vol_at', 'args': [a[0], a[1], a[2]], 'types': TYPES, 'expect': got, 'compare': 'isclose', 'tol': {'rel': 1e-9, 'abs': 1e-12}})
assert abs(vol_tests[0]['expect'] - math.sqrt(0.055)) < 1e-15
C2i = item('c2-variance-interpolation', 4, ['cx-pricers', 'tp-bs'], ['variance-interpolation'], 1200, 'Fix the vol curve',
           prose='A desk quotes implied vols at a few maturities, the pillars. A colleague\u2019s C++ draft reads off the vol between them. '
           'It interpolates the vols linearly in time.',
           question='Fix `vol_at(T, vols, t)` in C++. Interpolate total variance, $\\sigma^2 T$, linearly in time, and return the vol it implies. '
           'Keep the end pillars\u2019 vols outside the range. Return -1.0 if any pillar\u2019s total variance is below the one before it, wherever `t` is. '
           'Equal total variances are allowed.',
           widget={'kind': 'code', 'language': 'cpp', 'starter': VOL_START, 'solution': VOL_SOL,
            'signature': 'double vol_at(const std::vector<double>&, const std::vector<double>&, double)',
            'examples': [dict(vol_tests[0], expect=round(vol_tests[0]['expect'], 6), tol={'abs': 5e-7}),
                         dict(vol_tests[4])],
            'tests': vol_tests,
            'how': f'Submit runs {len(vol_tests)} hidden tests. Vols are accepted within a relative 1e-9.'},
           feedback=fb('Interpolating $\\sigma^2 T$ keeps forward variance positive between pillars.',
              'Work with $w = \\sigma^2 T$ at each pillar, interpolate $w$, then return $\\sqrt{w/t}$.'),
           explain='Between 0.25 and 1 year the total variances are 0.01 and 0.0625. '
           'At half a year $w = 0.01 + 0.0525/3 = 0.0275$, so the vol is $\\sqrt{0.055} = 0.2345$, not the draft\u2019s 0.2167. '
           'A falling $w$ means a negative forward variance, which no model can produce.',
           )

# ======================================================================== paper 5: fit
F1 = longform(
    'f1-why-strats', 3, ['rk-behave'], ['why-strats'], 450, 'Why strats',
    'Answer aloud first. Then write your answer down, in 200 words or fewer.\n\n'
    'What draws you to a strats or desk quant seat, over trading or pure research?',
    '*An example answer. Your own words are the real answer.*\n\n'
    'I want to build the models a desk uses every day. '
    'Two things draw me. The work is maths turned into code that people rely on at once. '
    'And the feedback is direct: a trader tells you by lunch if a price is wrong.\n\n'
    'I tested this. In my project I priced barrier options three ways and found my tree was off by 2%. '
    'Tracking that down taught me more than the formula did.\n\n'
    'The hard part is the pressure of a live desk. I handle it by testing small pieces first.\n\n'
    'Research is slower to touch the business, and trading needs fast calls more than models. '
    'Strats sits where I am strongest.',
    [(1, 'Gives a one-sentence answer first'),
     (2, 'Two reasons tied to the daily work, such as models in use and fast feedback'),
     (3, 'One piece of their own evidence with a number or an outcome'),
     (2, 'Names something hard about the role and how they handle it'),
     (1, 'Says why strats rather than trading or research'),
     (1, 'About 90 seconds, and no line that would fit any firm, such as "I am passionate about markets"')])
F2 = longform(
    'f2-model-disagrees', 3, ['rk-behave'], ['model-versus-market'], 450, 'The trader disagrees',
    'Answer aloud first. Then write your answer down, in 200 words or fewer.\n\n'
    'A trader says your model\u2019s price is wrong because it disagrees with the market. Talk through how you respond.',
    '*An example answer. Your own words are the real answer.*\n\n'
    'I would start by taking it seriously, because the market is often right. '
    'I would ask which price, by how much, and since when.\n\n'
    'Then I would check the inputs before the model. Stale vols, a wrong dividend or a bad curve cause most gaps.\n\n'
    'If the inputs are right, I would ask what the market knows that the model leaves out. '
    'A smile, a jump or a funding cost are common answers.\n\n'
    'I would agree a fix and a date with the trader. Meanwhile I would mark the gap so nobody trades on it blindly.\n\n'
    'Once, my volatility fit was off at short dates. A trader spotted it, and we fixed the weighting together.',
    [(1, 'Opens by treating the trader\u2019s point as possibly right'),
     (2, 'Asks for specifics: which price, how far off and since when'),
     (2, 'Checks inputs, such as data, vols, dividends and curves, before the model'),
     (2, 'Names what the model may leave out, such as a smile or jumps'),
     (2, 'Agrees an action and a time with the trader, and flags the gap meanwhile'),
     (1, 'Speaks in the first person, under two minutes')])

# ======================================================================== the exam document
SCORE = {'right': 1, 'wrong': 0, 'blank': 0}
doc = {
    'id': 'mock-superday-strats',
    'name': 'Strats superday',
    'style': 'strats',
    'models': 'Reported, as of Nov 2026: strats final rounds at Goldman Sachs and Morgan Stanley, quant research at JP Morgan. '
              'Probability, coding, Greeks; stochastic calculus in older reports.',
    'description': 'This mock is built from reports of bank strats final rounds, as candidates described them by Nov 2026. '
                   'Goldman Sachs, Morgan Stanley and JP Morgan candidates report rounds like these. '
                   'There are five papers, each on its own clock. '
                   'They cover probability, derivatives pricing and risk, stochastic calculus, coding and fit. '
                   'Real rounds are spoken, so say each answer aloud before you type it. '
                   'Some questions have follow-ups that open one at a time. '
                   'No calculator and no search engine are allowed, except to run your code. '
                   'Orders and lengths differ by firm and office. '
                   'Two checks at the end ask for what the app cannot see.',
    'requires': ['markov/L5', 'options/L3', 'trees/L4', 'ito/L4', 'numerics/L4', 'cpp-pricing/L2'],
    'skills': {'mc-walks': 'Random walks and stopping', 'rv-joint': 'Correlated variables', 'rv-expect': 'Expected values',
               'dl-discrete': 'Poisson arrivals', 'tp-bs': 'Black-Scholes', 'op-parity': 'Parity and arbitrage',
               'op-greeks': 'Greeks and hedging', 'nm-mc': 'Monte Carlo error', 'nm-fd': 'Finite differences',
               'it-calculus': 'It\u00f4 calculus', 'it-martingale': 'Martingales', 'it-bm': 'Brownian motion',
               'it-pricing': 'Pricing by expectation', 'tp-multistep': 'Binomial trees', 'cx-pricers': 'Pricers in code',
               'rk-behave': 'Behavioural answers'},
    'parts': [
        {'kind': 'paper', 'id': 'probability', 'name': 'Probability', 'minutes': 30, 'scoring': SCORE, 'pass': 0.6,
         'items': [P1, P2, P3, P4, P5]},
        {'kind': 'paper', 'id': 'pricing', 'name': 'Derivatives pricing and risk', 'minutes': 45, 'scoring': SCORE, 'pass': 0.6,
         'items': [R1, R2, R3, R4, R5, R6, R7]},
        {'kind': 'paper', 'id': 'stochastic', 'name': 'Stochastic calculus', 'minutes': 30, 'scoring': SCORE, 'pass': 0.6,
         'items': [S1i, S2i, S3i, S4i]},
        {'kind': 'paper', 'id': 'coding', 'name': 'Coding', 'minutes': 45, 'scoring': SCORE, 'pass': 0.75, 'items': [C1, C2i]},
        {'kind': 'paper', 'id': 'fit', 'name': 'Fit and motivation', 'minutes': 15, 'scoring': SCORE, 'pass': 0.5, 'items': [F1, F2]},
        {'kind': 'check', 'id': 'derivation-aloud', 'name': 'I derived one result aloud to a listener, start to finish',
         'detail': 'Tick this only if someone heard every step and you read nothing from notes.'},
        {'kind': 'check', 'id': 'no-lookup', 'name': 'I used no calculator, search engine or notes',
         'detail': 'Tick this only if you sat all five papers without them, apart from running your code.'},
    ],
}
assert len(doc['models']) <= 200, len(doc['models'])
write(doc, OUT)
n_items = sum(len(p.get('items', [])) for p in doc['parts'])
print(f'wrote {os.path.relpath(OUT)}: {n_items} items, {sum(p.get("minutes", 0) for p in doc["parts"])} minutes')
for p in doc['parts']:
    for it in p.get('items', []):
        print(f'{p.get("id"):12} {it["id"]:28} d{it["difficulty"]} pace {it["pace"]}')
