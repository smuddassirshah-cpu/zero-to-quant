# Concept audit, round 2: micro L1 to L3

Auditor: Fable, blind. No earlier review, audit, author report, ledger or concepts script for this course was opened before the ledger and findings below were committed (WIP commit named in the overlap section). Date 12 Nov 2026. Stage 1, full ledger depth.

Scope: `app/content/courses/micro/` l1 to l12, review-1 to review-3, homework-1 to homework-3 (18 files).

Ledger: `docs/reports/audit-micro-1-3-r2-ledger.md`, 308 rows: 294 `correct`, 0 `wrong`, 9 `imprecise`, 0 `misleading`, 5 `unverified`.

Concepts script: `docs/reports/micro-L1-3-r2-concepts.py` (CPython 3.13.18, standard library), 36 checks, exit 0.

## Method

- Every graded key, `wrong[]` value, slip feedback, table cell and option was recomputed by hand from the item's own data. The course has no number script for L1 and L2, so the concepts script also recomputes the main L1 and L2 keys from the JSON canvases (walks of each book, spreads, the l4 fill-chance model, the l6 curve and series, l8 books).
- Every slip tolerance window was compared with the key's window; none overlap.
- Empirical claims were simulated: the microprice against the mid as a predictor in a one-tick book (two queue models), the sign of the imbalance, inventory with and without a skew, Glosten-Milgrom posteriors after one, two and three buys, the tilted-noise quotes of homework-3, the timing-risk figure of homework-2, and the optima $1/k$ and $\alpha\delta + 1/k$.
- All eight code items were run in CPython: every solution passes all hidden tests and every starter fails. The l11 seeded test values reproduce exactly.
- Market and industry remarks were each matched to a named source or marked `unverified`.

## Findings

No `wrong` finding. Eight `imprecise` findings, all `minor`.

1. `l7-where-is-the-price.json` | `screens[9].explain.text` | imprecise, minor | The third sentence says "Dividing would then crash or mislead." With an empty side nothing is divided: without the guard the function stops at `asks[0]`. | Evidence: `[][0]` raises `IndexError` (script INFO line); the item's own `feedback.byKey.error` says "An empty list has no `[0]`". | Fix: replace the third sentence with: "Without the check, `asks[0]` on an empty list raises `IndexError`."

2. `l10-inventory.json` | `screens[7].prose` and `screens[10].explain.text` | imprecise, minor | The lesson credits $\gamma = A\sigma^2\tau$ to Avellaneda and Stoikov and then says a long $\tau$ makes the maker "shed inventory hard into the close". In that model $\tau$ is the time left in the session, $T - t$, so the skew fades to zero at the close. The lesson's reading (the night counts in $\tau$) is sound for a desk, but a learner would misstate the named model. | Basis: Avellaneda and Stoikov (2008), reservation price $r = s - q\gamma\sigma^2(T - t)$. | Fix, `screens[7].prose`: replace "The Avellaneda-Stoikov model turns that into exactly our rule:" with "The Avellaneda-Stoikov model turns that into our rule, with $\tau$ the time left in the trading session:". Fix, `screens[10].explain.text`: replace the second sentence with: "With the night counted in $\tau$, the skew rule says the same: $\gamma$ is large, so you shed inventory hard into the close. In the model itself $\tau$ stops at the close, so its skew fades as the close nears."

3. `l12-venues.json` | `screens[7].feedback.byKey.unreg` | imprecise, minor | "Dark pools are regulated venues with their own rules and volume caps." Volume caps are an EU rule. The UK removed its double volume cap and the US has none. The option's `why` on the same screen says it correctly ("The EU also caps dark volume"). | Basis: MiFIR Art. 5 (EU volume cap); Financial Services and Markets Act 2023 (UK removal). | Fix: "You assumed hidden means unregulated. Dark pools are regulated venues with their own rules, and the EU caps their volume."

4. `l12-venues.json` | `screens[5].explain.text` | imprecise, minor | "the orders simply stay in the book" leaves two things unsaid: unmatched orders stay only until they expire, and the share still gets a closing price. The summary trap says the close is the uncross price, so a learner is left with no close for this share. | Basis: LSE *Guide to the Trading System* (MIT201), closing price hierarchy: uncross price, else a volume-weighted price of late continuous trades, else the last automated trade. | Fix: replace the last sentence with: "That is the edge case: the orders stay unmatched, and the exchange takes the closing price from earlier trades."

5. `homework-1.json` | `items[6].explain.text` | imprecise, minor | "Each extra point of fill chance cuts the cost by $2h + c$." The slope is $-(2h + c)$ per unit of $p$. A "point" of chance reads as 0.01, which cuts the cost by $0.01(2h + c)$. | Basis: $E = h + c - p(2h + c)$, so $dE/dp = -(2h + c)$. | Fix: "Raising the fill chance by 0.01 cuts the cost by $0.01(2h + c)$."

6. `l11-adverse-selection.json` | `screens[5].widget.options[3].why` (id `four`); `review-3.json` | `items[8].feedback.byKey.full` | imprecise, minor | "One trade earns at most the half-spread." This lesson measures profit at the true value, and there a single sale at 502p of a share worth 490p earns 12p. The bound holds for the average. | Basis: $E[\text{profit} \mid \text{buy}] = s - \alpha\delta \le s$; per trade the profit is $s \pm \delta$ for an uninformed buyer. | Fix, both places: replace the sentence with "On average one trade earns at most the half-spread."

7. `l12-venues.json` | `screens[1].explain.text` | imprecise, minor | "it peaks where they cross, at 501p." The plotted lines cross between 501p and 502p. | Evidence: buyers fall 1,500 to 1,000 and sellers rise 1,200 to 1,800 from 501p to 502p, so they meet at $501 + 300/1{,}100 \approx 501.3$p. | Fix: replace the second sentence with: "The traded amount is the lower of the two lines, so it peaks at 501p, the whole penny beside their crossing."

8. `l8-liquidity.json` | `summary.ideas[0]` | imprecise, minor | "volume (how fast the book refills)" equates volume with refill speed. The standard third dimension is resiliency; volume is a proxy for it, and this lesson's own trap shows volume alone can mislead. | Basis: Kyle (1985), tightness, depth and resiliency. | Fix: "Liquidity has three dimensions: spread (the cost of a small trade), depth (what a large one meets) and volume (a guide to how fast the book refills)."

## Unverified market remarks

These five ledger rows are `unverified`: plausible, but I could not tie them to a named source. None changes a graded answer. A hedge is offered for each; the fixer may instead add a source.

- `l8-liquidity.json` | `screens[6].explain.text` and `summary.ideas[2]` | The chart is the lesson's own data, so the prose that describes it is fine. The general statement "wide after the open, tight before the close" is unsourced, and older NYSE studies found spreads widening again at the close (McInish and Wood 1992). Hedge for the summary: "Liquidity changes through the day, often wide after the open, and it vanishes in a crisis."
- `l8-liquidity.json` | `screens[8].prose` | "often 10%". Hedge: "for example 10%".
- `l10-inventory.json` | `screens[8].explain.text` | "Options desks skew this way after every large client trade". Hedge: "Options desks skew this way after a large client trade".
- `l11-adverse-selection.json` | `screens[9].explain.text` | "within microseconds". Hedge: "Makers watch for sweeps and pull or move their quotes as fast as their systems allow."

## Notes that are not findings

- `l6` uses $c\,\sigma\sqrt{Q/V}$ as the average cost per share (Grinold and Kahn's convention). Some papers use the same formula for the peak price move, with the average cost about two thirds of it. With $c$ described as "near 1" and fitted, the lesson's usage is defensible; no change proposed.
- `l7` screen 3 says openly that the microprice (£100.133) overshoots the mid's next value (£100.125) in a four-tick spread, and the summary limits the prediction claim to a one-tick book. The simulation supports that scoped claim.
- `l9` screen 3 says once that $s$ changes meaning from the whole spread to the half-spread. Good.

## Gates

- Validator (`node tools/validate.mjs`, from `app/`): 0 errors, 4531 warnings; `content/manifest.json` unchanged.
- Number script `docs/reports/micro-3-perf-numbers.py` (run, not opened): exit 0. The course has no `micro-L*-numbers.py`.
- `node tools/grade-all.mjs --file ... --local-cdn <pkgs>`: review-1 (8 widgets), review-2 (9), review-3 (9), homework-1 (6), homework-2 (6), homework-3 (5): 0 failures each, exit 0.
- Concepts script: exit 0.
- Code items (own CPython run): l2 9/9, l6 12/12, l7 10/10, l9 9/9, l11 8/8, homework-1 9/9, homework-2 10/10, homework-3 9/9; starters fail (l7's starter passes only its two `None` tests).

## Overlap with earlier reads

Read after the ledger and findings were committed (WIP commit `709c32ad`): `docs/reviews/review-1.7.md` (micro part and its fix pass), `docs/reviews/audit-micro-1-3.md` (round 1 audit, fix pass, fix-pass read and its follow-up) and the micro lines of `docs/reviews/review-perf-retrofit-12.md`.

Earlier conceptual findings: review-1.7 raised 12, the round 1 audit 20, its fix-pass read 4, and the performance retrofit read 2: 38 in all. All were fixed before this read, so this audit read the fixed text and could re-find one only where a fix left a residue.

| | count | which |
|---|---|---|
| Found by this audit only | 7 | findings 1, 2, 4, 5, 6, 7, 8 |
| Found by an earlier read only | 37 | review-1.7: 11; round 1 audit: 20; round 1 fix-pass read: 4; perf retrofit 12: 2 |
| Found by both | 1 | finding 3: review-1.7 raised the UK's removal of the dark volume cap on l12 screens[7]; its fix corrected the option's `why` and left the `byKey` line |

New `wrong` findings that no earlier read found: **0**. This audit has no `wrong` finding at all; all eight findings are `imprecise` and `minor`.

Notes on agreement and difference.

- Finding 2 (Avellaneda-Stoikov $\tau$). The round 1 audit lists "the skew rule $m = V - \gamma q$ with $\gamma = A\sigma^2\tau$ against Avellaneda and Stoikov" under checked and clean. The formula is right; the point here is the meaning of $\tau$ and the "into the close" sentence, which round 1 did not raise.
- l8 screens[8] "often 10%". My blind verdict is `unverified`. The round 1 fix-pass read passed the same sentence citing Kissell and Glantz, *Optimal Trading Strategies*, on participation-rate limits. I have not checked that source for the 10% figure; the hedge "for example 10%" removes the question either way.
- l7 summary and quiz[3] (round 1 finding 11 and fix-pass findings F1, F2). The fixed text scopes the prediction claim to a one-tick book and to the mid just after its next move. My simulation, written blind, tests exactly that claim and supports it (squared error 0.55 and 0.59 against 1.00 in half-ticks squared).
- The round 1 keys changed by its fix pass (l6 quiz[0] to 20.0233, homework-1 `h-bp`, `h-sell-walk`, homework-3 `old-k`) all recompute correctly here.

Convergence: at most one new `wrong` per three levels is allowed; this round found none. The fix pass for the eight minor findings and its fix-pass read remain.
