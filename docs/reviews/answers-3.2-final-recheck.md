# Answers recheck: topic 3.2 fix passes, exam fix pass and per cent fix (final)

Scope: the "Changed keys" lists in `review-ito.md`, `review-measure-prob.md`, `review-pdes.md` and `review-exam-3.2.md`, and the 46 widgets of `fix-pct-keys.md`. Branch base: e6562af. Every value recomputed independently (mpmath at 30 digits, SciPy, exact fractions or a second route); scripts in the scratchpad `rc-final/`. No content edited. Greps for every old value (`b4`, `e4`, `c5`, `1246076` as a key, `driftless` as a wrong id in part 2, `130.9`, `0.0003`, `1/U`) found no stale use.

## Verdict: 2 mismatches

1. ERROR, `courses/garch/homework-2.json` items[3] `h-year-later` (a per cent widget).
2. ERROR (logic of an order key), `courses/ito/homework-4.json` items[0] `h-stopping` (`same`).

## ito

- l16 `q-cube`: 10^6 e^0.22 = 1,246,076.7306 (exponent 2r + 3 sigma^2 = 0.10 + 0.12, and -0.05 + 0.09 + 0.18 = 0.22). Key 1246077 tol 1: OK. `jensen` 10^6 e^0.10 = 1,105,170.92 and `no-discount` 10^6 e^0.27 = 1,309,964.45, both tol 1: OK. Accept, feedback and explain agree.
- l3 s4 order: b1 and b2 each need only the setup; b3 needs both (fourth moment and the mean squared); b5 needs b3. Valid orders: b1 b2 b3 b5 and b2 b1 b3 b5, exactly what `same [[b1, b2]]` accepts. OK.
- l6 s2 order: e2 and e3 each need only e1; e5 needs both. Valid: e1 e2 e3 e5 and e1 e3 e2 e5, exactly `same [[e2, e3]]`. OK.
- homework-4 `h-stopping` `same [[o2, o3]]`: ERROR. o3 passes to the limit by bounded convergence, which needs tau finite almost surely, and that is what o2 proves. Also o3 and o4 cite "line 1" and "line 2" by position, so after a swap "line 2" is the P line. `answers-3.2-ito-4.md` (error 2) already found the same dependency and removed a `same`; this one reintroduces it. Fix: delete `"same": [["o2", "o3"]]` and the question sentence "The finiteness line and the line for P may swap." Only o1 o2 o3 o4 is valid.
- l13 s2 table: drifts at t = 1, W = 2: W^2 + t gives 1 + 1 = 2; e^(4W - 8t) gives -8f + 8f = 0; W^3 - 3tW gives -3x + 3x = 0; W^4 gives 6x^2 = 24. Martingale no, yes, yes, no. `accept` y and n added to the matching cells (table.js reads `accept` arrays for text cells). Feedback figures (3, 1, 48) checked. OK.
- l2 s8: `normal` ("each X_t ~ N(0, t)") is true, given by the question; `zero` X_0 = 0 true; `cont` true; independence fails since X_2 - X_1 = (sqrt 2 - 1)Z is a multiple of X_1, Cov(X_1, X_2) = sqrt 2, not min(1, 2) = 1. Only `indep` keyed. OK.

## measure-prob

- l3 s7: 3 x 1% = 3%, key 0.03 tol 1e-5; `indep` 1 - 0.99^3 = 0.029701. OK.
- l3 `q-union`: 4 x 0.5% = 2%, key 0.02; `indep` 1 - 0.995^4 = 0.0198505 (stored 0.01985, tol 1e-5 holds). OK.
- review-1 `r-union`: 5 x 0.8% = 4%, key 0.04; `indep` 1 - 0.992^5 = 0.0393651 (stored 0.039365). OK.
- l11 s8: 250 x 1% = 250 points = 2.5 as a fraction; `zero` 0, `one` 0.01 (typed 1), `half` 1.25 (typed 125), all exact in floating point after the /100. OK.
- review-3 `r-cube`: with S_{n+1} = S + X, X = +1 or -1, a: E = S^3 + 3S - 3(n + 1)S = S^3 - 3nS, a martingale (key). b: drift 3S, not. c: E = S^3 - n - 1, drift 3S - 1, not. New d `S_n^2 + S_n`: E = S^2 + 1 + S, drift +1, NOT a martingale. The old proposal `S_n^2 - n + S_n` has E = S^2 + 1 - (n + 1) + S = itself, a martingale, so rejecting it was right. OK.
- l4 `q-expu`: P(-ln U > 2) = e^-2 = 0.135335, key 0.1353 tol 0.0005. `half` 0.5 is P(X > ln 2), correct. OK.
- l3 s5 order: c1 (pieces), c2 (union is A), c3 (additivity needs both), c4 ("that sum", partial sums), c6. One valid order and one keyed. OK.
- l12 s3 order: b2, b3, b4 is a chain (b3 uses b2's expression, b4 finishes b3). b1 folded into b4. OK.
- homework-1 `h-long` part 2: sum over k >= 50 of 1/k^2 = 0.0202013 (also 1/49.5 = 0.020202). "about 0.0202" OK.

## pdes (option texts only, no graded change)

l11 s5 and `q-drift` (12% drift, S = K = 100, r = 5%, sigma = 20%: discounted payoff 15.5261, BS 10.4506, ratio 1.4857, "49% too high" and "about £15.53" hold), l9 s0, l12 s6 `kink` and `unstable` (CN factor at lambda = 200 is (1 - 2 lambda)/(1 + 2 lambda) = -399/401 = -0.9950; CN is stable at any step, so "unstable" stays wrong), l5 `q-const`, review-1 `ends`: each has the same single correct id and the same meaning. OK.

## exam topic-3.2

- `e-swap-limits`: a U^(1/n): E = n/(n + 1) tends to 1 = limit, true. c sqrt(n) U^n: E = sqrt(n)/(n + 1) tends to 0 = limit, true. e min(n, U^(-1/2)): E = 1/n + 2 - 2/n = 2 - 1/n tends to 2 = E[U^(-1/2)], true (monotone). b n^2 1{U < n^-2}: E = 1, limit 0, false. d n e^(-nU): E = 1 - e^-n, limit 0, false. True set is exactly a, c, e. OK.
- `e-is-weight`: weight e^(-8 + 3.125) = e^-4.875 = 0.0076351 (also phi(3.2)/phi(0.7) = 0.0076351). `upside-down` e^4.875 = 130.974 (stored 130.97, tol 0.5); `no-half-theta-squared` e^-8 = 0.00033546 (stored 0.000335, tol 0.0001). OK.
- `e-exit-drift` part 2: c = 2(-0.3)/0.81 = -0.7407, P = 0.413167 (scale-function route agrees), E[X_tau] = -0.76050, E[tau] = 2.53500. `standard-bm` 2.0 = ab. `wrong` id and `byKey` key both `standard-bm`. OK.
- `e-variance-split`: s1, s2, s3, s4 are forced; s5 and s6 each need only s4; s7 needs both. Valid orders: s5 s6 and s6 s5 only, exactly `same [[s5, s6]]`. Reworded s5 and s6 read correctly in either order; d1 and d2 remain wrong with the stated reasons. OK.

## Per cent fix (46 widgets)

Systematic check against the pre-fix commit (29b1d7e^): for all 46, new answer x 100 = old answer; every `wrong` value x 100 = old value with the same id; every absolute tol x 100 = old tol; `accept` text unchanged; unit `%`. One difference, as documented: garch review-2 items[1] tol 0.003 to 0.00005 (accepted 1.48 sits 0.00003 from 0.014832, inside). The leading number of every `accept` lies within tol of key x 100 for all 46.
Independent recomputation (all keys equal the figure the prompt asks for, at the stated precision):
garch hw1 [1] 20/sqrt(52) = 2.7735, with wrong 20/sqrt(252) = 1.2599 and 20/52 = 0.385; hw2 [0] sqrt(1.5 x 252) = 19.442; l4 s2 15.106, quiz 14.422; l5 s1 1 - 0.94^20 = 0.7099, s10 2.2566, quiz 0.2626; l6 s2 2.2361, s11 5.7966; l8 s2 15.875, s3 14.963, s6 24.695, quiz 23.812; review-1 23.812; review-2 [1] 1.4832, [7] 15.87, [9] 22.450; pytest hw3 386/1024 = 0.37695, l10 1/32 and 1/16, l11 25% and 40%, l12 19/21 = 0.9048 and 34/40, l9 82/80 - 1 = 2.5%, review-3 17/25; py-found hw4 2.5 sqrt(52) = 18.028, l13 25%, l14 -2%, l15 19.049 and 12.700, review-4 15%, 22.450 and 4.7375; ensembles leaf means 21 and 17; topic-2.2 [1] sqrt(0.02 + 0.07 x 5.76 + 0.91 x 1.6) = 1.3708, [11] sqrt(1 + 0.97^10 x 1.5) = 1.4513; opt-dash hw4 18.385; pdes l7 0.17898/2 = 8.949%; eigen -2.25; systems 1000/2500 = 40%; validation 7.0351/5.8928 - 1 = 19.38%. All OK except one.

- `courses/garch/homework-2.json` items[3] `h-year-later`: ERROR. 0.995^252 = 0.282759 (0.995^251 = 0.28418, so 0.2834 is neither). Key 0.2834 tol 0.0005 rejects a typed 28.28 or 28.27 (0.2828 is 0.0006 away), and the accept line states a false equality. Fix: `answer` 0.2828 (tol 0.0005 stays) and `accept` "28.3%: $0.995^{252} = 0.2828$." (`explain` already says 0.283). The error predates the per cent fix (old key 28.34); the same figure is not used as a key elsewhere (garch l1 line 14658 is chart data, not checked here).

## Counts

Rechecked: ito 6, measure-prob 9, pdes 6 option texts, exam 4, per cent 46: 71 widgets. Mismatches 2: homework-4 `h-stopping` `same` (worst for a learner: a correct-looking order is accepted that uses an unproved step, and the positional "line 2" breaks) and garch homework-2 `h-year-later` (a correct typed answer 28.28 is rejected).
