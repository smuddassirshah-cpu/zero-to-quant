# Report: markov level 5, "Martingales and stopping" (gap level, topic 1.5)

Brief: `docs/briefs/gap-markov-2.md`, `## Level 5`. Ids, names, objectives and skills as in `app/content/courses/markov/course.json`.

## Files written

| File | Screens / items | Quiz | Notes |
|---|---|---|---|
| `l17-fair-bets.json` | 12 screens | 4 | walk (hook, bias slider, drift overlay, roulette), tree (price, forecaster, Pólya, binary contract), series trap, order derive with distractor, code `next_mean` / `is_martingale` |
| `l18-hidden-martingales.json` | 10 screens | 4 | walk overlays `sq`, `ratio`, expr `S^2` and `(p / q) ^ S`, `showStopped`; order derive; code `one_step_drift` / `is_walk_martingale` |
| `l19-optional-stopping.json` | 12 screens | 4 | walk with `lower`/`upper` sliders, `showStopped`, expr overlays `x^2 - n`, `(q / p) ^ x`, `x - n * (2 * p - 1)`; bars (Wald); table check against first-step; code `ruin_by_stopping` / `wald_total` |
| `l20-when-stopping-fails.json` | 11 screens | 4 | walk with floor slider and `stopAt`; bars (doubling); walk `bankroll` overlay with `bet: "double"`; series transfer; code `doubling_ev` / `stop_when_up` |
| `l21-waiting-for-patterns.json` | 11 screens | 4 | walk `model: "markov"` (pattern automata, `values.tauMean`), graph automaton, gambler tables, order derive, multi (ABRACADABRA), code `pattern_wait` / `simulate_wait` |
| `l22-arrivals-fair-game.json` | 11 screens | 4 | series counting path (seeded), order derive, bars of trade sizes, trap on the variance, code `compound_moments` / `simulate_compound` |
| `review-5.json` | 10 items, difficulty 2 to 4 | | interleaves all six lessons |
| `homework-5.json` | 10 items, difficulty 3 to 5 (three at 5) | | code (`stop_when_up_exact`, d5), order (duration proof), longform (take-profit with no stop, 10-point rubric), exponential martingale (d5) |

## Validator

`node tools/validate.mjs`: 0 errors, 365 warnings. The only warning in my files: `l19` screen 8 (the two-routes table) is a problem screen without a canvas; the widget is itself a table. No errors from the `proof` files at the time of the last run.

## Playthrough (with `--local-cdn <scratchpad>/pkgs`)

- l17 ok, 16 checks, quiz 4/4; l18 ok, 14 checks, 4/4; l19 ok, 16 checks, 4/4; l20 ok, 15 checks, 4/4; l21 ok, 15 checks, 4/4; l22 ok, 15 checks, 4/4.
- `--set markov/review-5` ok, 10 of 10; `--set markov/homework-5` ok, 10 of 10, 45 of 45 marks.
- Screenshots at 1280 and 390 px (with `--why`) in `scratchpad/markov-5/shots`. Fixed after looking: tree node values written as "1/2" stacked over the pill (now ½, ¾, ⅓); graph edge labels as strings did not draw, and crowded at 390 px (numbers, or `show: "none"` with a caption); first-step equations stacked with `aligned`; l18 and l22 summary formulas and ideas shortened, because a long inline formula widened the whole ideas list past the phone column; walk widths shortened (l20 floor walk 1,000 steps, automaton walks 60 and 80).
- Code: every solution passes its tests in CPython and in the browser; every starter fails its suite (l19 and homework starters pass only the edge cases, 2 of 11 and 2 of 7). Slowest CPython case 0.08 s (compound simulation, 5,000 trials).

## Numbers and their two sources

Scripts: `scratchpad/markov-5/nums.py`, `nums2.py`, `nums3.py` (exact `fractions`), `codecheck.py`. Walk values read from the browser with `scratchpad/markov-5/probe.mjs` (`step().canvas.values()`), never from CPython.

- l17: £13 and £13 (average of 14 and 12; martingale mean). £13.20 ($0.6 \times 14 + 0.4 \times 12$; $13 + 2p - 1$). $M_{11}$ forecast 3 ($5.2 - 2.2$; $M_{10} = 5 - 2$). Price chance $\tfrac49$ (solve; check $\tfrac49 \cdot 1.25 + \tfrac59 \cdot 0.8 = 1$). Forecaster $\tfrac12, \tfrac34, \tfrac14$, then $1, \tfrac12, \tfrac12, 0$ (binomial counts; averages of children). Roulette $-\tfrac{1}{37} \approx -0.027$. Pólya: $\tfrac23$ next share; three-draw shares $\tfrac15..\tfrac45$ at $\tfrac14$ each, mean $\tfrac12$ (exact enumeration of the urn). Binary contract £20 ($0.6x + 28 = 40$; check). Quiz: $\tfrac13$, 1, 7.
- l18: 10 from $S_n = 3$; $0.96 = 4pq = 1 - 0.2^2$; factor 1 for $r = \tfrac23$; $E[r^{S_{10}}] = 1$ by binomial sum; flipped factor $\tfrac76 \approx 1.1667$ and $(\tfrac76)^{10} = 4.6716$ (power and binomial sum agree); £5,000. Explore (seed 11, 2,000 paths): averages 102.7 and 2.7 against exact 100 and 0 (sd of $S_{100}^2$ is $\sqrt{19800} \approx 141$, standard error about 3.2). Ratio screens (seed 3, 300 paths): 1.02 and 4.64. Quiz: $\tfrac37$, 0.75, 1.
- l19: from first-step exact Gaussian elimination and the martingale formulas, all equal: $(3,10,\tfrac12) \to \tfrac{3}{10}, 21$; 25 and 2,500; 6 from £2 of £5; $(2,4,\tfrac35) \to \tfrac{9}{13}, \tfrac{50}{13} \approx 3.846$; $(5,10,\tfrac25) \to \tfrac{32}{275} \approx 0.1164, \tfrac{211}{11}$; $(3,10,\tfrac35) \to \tfrac{41553}{58025}, \tfrac{48291}{2321}$; $p = 0.49$, £50 of £100: 0.1192 and 1,904.1. Still going after 200 steps from 3: 0.0000458; after 50: 0.0852 (DP). Wald 21 ($3.5 \times 6$; $5 \times 3 + 6$; `random.Random(1)` 200,000 games 21.03). Trader $\tfrac23$, 8 trades, £0. Browser: hook 97 of 300 reached £10, average $S_T$ 3.23, mean length 20.2; $p = 0.4$ screen average $S_T$ 1.17 (exact 1.164), power average 7.61 (exact 7.59); $p = 0.6$ mean length 3.87; trap (seed 6, 200 paths) 23 reached £100, average £11.75 (exact 11.92); square panel average 12.1 (SE 2.5) against 9. `wald_total(1, 2000) = 21.3755`, `wald_total(5, 10) = 22.6` (CPython; Pyodide matched).
- l20: $\tfrac{L}{L+1}$, $E[S_T] = 0$, $E[T] = L$ (9 and 99, ruin formulas after a shift). Fail chance in 100 steps $\binom{100}{50}/2^{100} = 0.0796$ (reflection and DP agree), conditional mean $-11.56$ ($-0.9204/0.0796$ and DP). Doubling: 0 for $d = 10$ and 6; $-0.3056$ (closed form and sum of branches; exact $-\tfrac{1469627475570375}{4808584372417849}$); $d = 7$: $-0.2052$. 200,000 fair cycles with `random.Random(1)`: +0.032, sd 31.5 (seed 2 gave $-0.034$; the planner's +0.068 came from another seed). Browser: floor $-9$, 276 of 300 reached +1, average $S_T$ 0.20, length 8.7; floor $-99$, length only 40 because of the heavy tail (stated on the screen); cap 100: 20 of 300 failed, average +0.07. Seeded `stop_when_up` values from CPython: (100, 3000, 1) 0.9193 and 0.0033; exact 0.9204 and 0.
- l21: waits H 2, HT 4, HH 6, HHT 8, HTH 10, HHH 14, HTHT 20, HHHH 30, HH at $\tfrac23$ 3.75, LLL at 0.4 24.375, LL 8.75, ABRACADABRA 3,670,344,487,444,778: casino rule and an exact first-step solve on the KMP automaton agree for every one. Seeded games (`random.Random(3)`, 20,000): 10.06 and 8.02. Browser automata: HHT 7.84, HTH 9.80. `simulate_wait('HTH', 0.5, 2000, 1) = 9.917`, `('HH', 2/3, 3000, 2) = 3.6853`. THT 10, HT at 0.6 4.1667.
- l22: path `random.Random(25)`, `expovariate(2)`: arrivals 0.237, 1.544, 2.471, 2.591, 3.618, 4.124, 4.146, so $N_3 = 4$. $E[N_5 \mid N_3 = 4] = 8$; $-2$ and $-2$; $E[(N_5 - 10)^2 \mid N_3 = 4] = 8$; $E[T_3] = 1.5$. $E[Y] = 210$, $E[Y^2] = 67{,}000$, $\mathrm{Var}(Y) = 22{,}900$; mean 4,200; variance 1,340,000 ($20 \times 67{,}000$ and $458{,}000 + 882{,}000$); sd 1,157.6; window 6,515; inventory 10 and 50, sd 7.07. `simulate_compound(..., 5000, 5) = (4181.26, 1337394.29)` (20,000 trials: 4,184.7 and 1,339,932; the planner's 1,339,865 differs in the variance divisor or the seed stream, not in the method).
- Review: $\tfrac{9}{11}$; $\tfrac{81}{202} \approx 0.4010$ (formula and first-step); 84; $-0.3686$ ($1 - 256 \times 0.52^8$, two forms); HTHH 18; HHH at 0.6 9.07; claims sd £12,247; $E[T_4] = 8$.
- Homework: $p = 0.55$ from £4 of £10: 0.6376 and 23.76 (formula and first-step solve agree exactly); chain $x = \tfrac13$, chance $\tfrac23$; $E[0.8^T] = \tfrac{8}{17}$ (exponential martingale and a first-step generating function); HTH at 0.6: $\tfrac{155}{18} \approx 8.6111$; insurer £192,000 and sd £36,661; `stop_when_up_exact`: $\tfrac12, \tfrac58, \tfrac{193}{256}, \tfrac{793}{1024}$, 100 steps $1 - \binom{100}{50}/2^{100}$ (DP and reflection agree), mean exactly 0; P&L limits 100 days; longform 0.9, 0, 9 trades.

No number failed its double check.

## Departures from the brief

- l17 hook uses a `table` widget for both forecasts on one screen; the name screen is a choice of which process is a martingale. The supermartingale screen uses red at a European wheel, as the brief says.
- l18 explore has no slider on `steps` (optional in the brief).
- l19: the brief's unfair-ruin ladder at $p = 0.49$ from £50 of £100 is the trap (a walk of 200 games over 8,000 steps); the ladder screen uses $p = 0.4$ from £5 of £10 so the chart is readable, and $\tfrac{32}{275}$ is also a code test. The walk's built-in `sq` and `ratio` overlays measure $S$ from the start, so screens with a start other than 0 use `expr` overlays in the position `x` (see backlog). The "highest point of the first 10 steps" trap is quiz item `q-peak`; the start-on-a-barrier edge case is quiz item `q-on-barrier`.
- l20: the bankroll overlay caps a bet at the bankroll (and `maxBet` when given); it does not restart a fresh £1,023 cycle after a ruin, so it shows a climb of about £1 a cycle and then a collapse, as the brief wanted, while the exact ten-bet cycle lives in the bars screens and the code. Edge case (bounded rule keeps a fair game fair) is quiz item `q-bounded`.
- l21: the first-step solve and the casino are separate screens; the edge case (H waits 2) is a quiz item; Penney's game gets one sentence in the trap's explanation.
- l22: the variance trap is a choice between 458,000, 882,000 and 1,340,000; the constant-size edge case is a quiz item.
- Table cells name their slips through cell-id `byKey` lines (`r0c1`), not `wrong[]` ids, because the validator rejects those keys (already in the inbox under proof level 1).

## course.json

No change proposed.

## Exam 1.5 (not edited, at the 30-item cap)

The level answers the existing `e-ruin-length` (6 bets from £2 with ends £0 and £5; l19 table and code). Items that could later join or replace exam items: an optional stopping ruin chance (`r-unfair-ruin`, $\tfrac{81}{202}$, or l19's $\tfrac{32}{275}$), a duration (`q-fair-12`, 32 bets), a pattern wait (`r-hthh`, 18, or `h-hth-biased`, 8.6111), a doubling expectation (`r-doubling-8`) and a compound Poisson spread (`r-claims-sd`).

## Seeds and conventions

Walk canvases: l17 seeds 4, 5, 9; l18 seeds 3, 6, 8, 11; l19 seeds 11, 6 (trap), 4; l20 seeds 2, 12; l21 seed 3. Python `random.Random(seed)` in every code screen with one documented draw per step (`rng.random()`, `rng.randint(1, 6)`, `rng.expovariate(rate)`, `rng.choices(sizes, weights=probs)[0]`). Exact answers are `Fraction`s compared with `compare: "fraction"` or tuple equality. Generators: `scratchpad/markov-5/l17.py` to `l22.py`, `review5.py`, `homework5.py`, with seeded browser values in `vals18.json` to `vals21.json`.
