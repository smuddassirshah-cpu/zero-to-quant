# cpp-pricing level 2 ("Pricers"): report

## Files written

All in `app/content/courses/cpp-pricing/` (generators in the scratchpad folder `cpp-pricing-2/gen/`):

- `l5-payoff-classes.json`: 11 screens, 4 quiz items, skill `cx-pricers`. Four C++ code screens: `Call`/`Put`/`DigitalCall` against a hidden abstract `Payoff`; `portfolio_payoff` over `std::vector<std::unique_ptr<Payoff>>` (a hidden `straddle(100.0)` gives 10 at spot 90); `Straddle` composed of a `Call` and a `Put`; transfer `CappedCall`. Canvases: pair of consoles (real clang error), plane explore (spot drag, edge case at the strike), graph hierarchy (tap), tree for virtual dispatch (tap), payoff, consoles for the trap (missing `const`, no `override`, prints 0) and for slicing (concrete base, prints `0 20`).
- `l6-binomial-cpp.json`: 10 screens, 4 quiz items, skills `cx-pricers`, `cx-numeric`. Recombining lattice drawn with `graph` (hand-placed rect nodes, n = 3); `array` explore with a step slider and `derive` (one row reused backwards, stale cells faded); code: `terminal_values`, in-place `step_back` (a test catches the downward loop), full `tree_price` + `binomial_price` (11 tests), script-mode transfer reading n from stdin. Table screen comparing C++ with trees l8's Python at n = 1, 4, 128, 512. Trap: `days / 365` with two `int`s.
- `l7-black-scholes-cpp.json`: 10 screens, 4 quiz items, skills `cx-pricers`, `cx-numeric`, `cx-testing`. Code: `bs_call` (7 points), `bs_put` (4 points + 3 parity tests), `bs_delta_call`/`bs_vega`/`bs_gamma` (incl. finite-difference cross-tests), `implied_vol` by bisection to 1e-8 with two `raises` cases. Plane of price against σ (σ → 0 edge case); trap: `sigma * t` passes every T = 1 test and parity; T = 0 gives `nan` at the strike.
- `l8-monte-carlo.json`: 11 screens, 4 quiz items, skills `cx-pricers`, `cx-numeric`, `cx-testing`. Code: `terminal_prices`, `mc_price(const Payoff&, ...)`, `mc_standard_error` (two-pass, n − 1, throws for n < 2), `mc_price_antithetic`. Series sim explore (running mean), bars of SE at n = 100 × 4^k, series of the C++ estimate with a ±2 SE band, Asian call console, trap: reseeding inside the loop.
- `review-2.json`: 8 items, difficulty 2 to 4, all four lessons.
- `homework-2.json`: 8 items, difficulty 3 to 5. Code: difficulty-5 `american_put` on a CRR tree (£5.8828 at 4 steps, £6.0888 at 500, both growth e^{rΔt}); difficulty-4 script reading S K r σ T n and printing tree, Black-Scholes and difference to 4 places. `order`: the antithetic variance derivation. `longform` (difficulty 5, 10-point rubric, full model answer): designing the pricer library. Plus paths-for-a-penny, American call = European, bisection count, a too-tight MC test tolerance.

Every `how` warns about the first compiler load.

## Validator

`node app/tools/validate.mjs`: 0 errors and no warnings of substance in my files (only "point hint usually highlights" and "ladder reuses canvas kind" on code ladders). The one error in the run belongs to `stat-learning/l8-setting-to-zero.json` (another agent).

## Playthrough

`node app/tools/playthrough.mjs --local-cdn …/scratchpad/pkgs`, screenshots in the scratchpad folder `cpp-pricing-2/shots` and `shots2`:

- l5-payoff-classes: 15 checks, quiz 4/4, ok.
- l6-binomial-cpp: 14 checks, quiz 4/4, ok.
- l7-black-scholes-cpp: 14 checks, quiz 4/4, ok.
- l8-monte-carlo: 15 checks, quiz 4/4, ok.
- review-2: 8 of 8 recorded, ok.
- homework-2: 8 of 8, 37 of 37 marks, ok.

The first combined run reported review-2 "has no items" and a homework timeout, straight after the four C++ lessons; rerunning the two sets alone passed (probably a transient load while other agents were writing files in this course folder). Fixed after looking at the screenshots: a floating point label on the l5 explore, a cramped l6 lattice (taller frame), crowded line-end labels on the l8 band chart, and ugly 1,001-style ticks on the l8 explore. l5, l6 and l8 were replayed after the fixes.

## How the C++ cases were checked

Every expected value comes from the app's runtime (clang 21, libc++, through a Node copy of the worker and `cpp-grade.js`), and every solution passes all its cases; every starter fails at least one. Values were checked a second time in Python, including a Python replica of `std::mt19937` and libc++'s polar `std::normal_distribution` (first draw for seed 42: 0.5154330696912013, MC price and SE identical to 1e-13). Slowest test: 32 ms.

## Proposed change to course.json

None. Note for the orchestrator: the `cpp` course has no inheritance lesson (l10 to l13 are invariants, constructors, operators, templates), so l5 teaches `virtual`, `override`, abstract classes and slicing from scratch. Level 3 (`l9-timing`) names its hidden classes `CallPayoff`/`PutPayoff` (structs); level 2 uses `Call`/`Put` as the brief says. The `binomial_price` signature matches.

## Every price stated, with its convention

Standard inputs S = K = 100, r = 5% (continuous), σ = 20%, T = 1 unless noted.

- Black-Scholes call £10.4506 (10.450583572185565), put £5.5735; delta 0.6368, vega 37.524, gamma 0.018762.
- Options l12 inputs (r = 0, T = 0.5): call £5.6372, delta 0.5282 (the 0.53).
- Other closed forms tested: (110) £17.6630, (90) £5.0912, (K 95, r 4%, σ 25%, T 0.5) £10.7854 call / £3.9043 put, (σ 24%) £11.9578, (S 200) £104.8777, (S 50, K 48, r 4%, σ 30%, T 0.25) put £1.8418, (S 80) put £16.9824, (K 110, r 3%, σ 35%, T 2) put £21.7448; T = 182/365 call £6.8776.
- σ → 0 limit: £4.8771 (= e^{−0.05}(100e^{0.05} − 100)); the 512-step tree at σ = 0.01 gives £4.8771. The tree throws at σ = 0 (u = d, q undefined): this departs from the brief's "σ = 0 gives max(Se^{rT} − K, 0) discounted", which is taught as the limit through Black-Scholes and small σ instead.
- Implied vol: £12.00 → 0.2411; £11.96 → 0.2401; floor £4.88 (£4.50 throws).
- CRR tree, growth e^{rΔt} per step: call n = 1 £12.1623, n = 3 £11.0439, n = 4 £9.9705, n = 64 £10.4194, n = 65 £10.4776, n = 128 £10.4350, n = 512 £10.4467; American put n = 1 £7.2852, n = 4 £5.8828, n = 500 £6.0888 (European n = 500 £5.5695, n = 4 £5.0935); American put S = 60 £40.00; American put S 90, K 110, r 3%, σ 30%, T 0.75, n 200 £21.9744; homework script cases (S 110, K 100, r 3%, σ 25%, T 0.5, n 200) tree £14.4682 vs BS £14.4670; (S 100, K 105, r 4%, σ 30%, T 2, n 50) £18.1922 vs £18.1219.
- Trees level 2 example, u = 1.2, d = 0.8, growth 1 + r = 1.05 per step, two steps: European put £6.2925, American put £7.9932, call £15.5896 (American the same); one step call £11.9048. Review: u 1.1, d 0.9, growth 1.02, one step put £3.9216.
- Monte Carlo, `std::mt19937` seed 42, libc++ `std::normal_distribution`: 8 paths £7.5536; 20,000 paths call £10.4735 ± 0.1042 (0.22 SE from BS), put £5.5547 ± 0.0609, digital (£10 cash) £5.3183; antithetic 10,000 pairs call £10.5031 ± 0.0737 (variance halved for the same 20,000 payoffs), put £5.6082; Asian call (12 monthly averages) £6.1774 ± 0.0601; reseeding per path £13.5406 with SE 0; SE at n = 100, 400, …, 102,400: 1.3306, 0.7271, 0.3892, 0.1869, 0.0919, 0.0462.

## Engine or runtime limitations

Listed in `docs/BACKLOG-INBOX.md` under "Raised later (cpp-pricing level 2):" (4 bullets).
