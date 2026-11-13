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

## Fix pass

Fixer: Opus, 12 Nov 2026. Content strings only; no graded key, tolerance, `wrong[]` value or slip value changed.

| # | Status | Basis |
|---|---|---|
| 1 | fixed differently | Both functions read `bids[0]` first, so the hidden test `microprice([], ...)` fails at `bids[0]`, not `asks[0]`. New text: "Without the check, `bids[0]` or `asks[0]` on an empty list raises `IndexError`." |
| 2 | fixed differently | Avellaneda and Stoikov (2008): $r = s - q\gamma\sigma^2(T - t)$, so $\tau = T - t$ and the skew tends to 0 as $t \to T$. s7 prose as proposed; s10 sentence reworded to keep under 20 words: "Counting the night in $\tau$, the skew rule agrees: ..." plus "In the model itself $\tau$ stops at the close, so its skew fades as the close nears." Explanation stays at three sentences. |
| 3 | fixed | MiFIR Art. 5 volume cap (EU; kept, as a single cap, by the 2024 MiFIR review); UK removed the double volume cap; US Reg ATS has no volume cap. |
| 4 | fixed | Screen 0 sets the 16:30 closing auction, so "closing price" applies. LSE MIT201 closing-price hierarchy: uncross, else a VWAP of late continuous trades, else the last automated trade. All are earlier trades. |
| 5 | fixed | $E = h + c - p(2h + c)$, $dE/dp = -(2h + c)$, so +0.01 in $p$ cuts $E$ by $0.01(2h + c)$. |
| 6 | fixed differently | l11 as proposed. review-3 `full` slip (value 4 = full spread $2s$ with $s = 2$) now names the mistake: "You counted the full 4p spread. On average one trade earns at most the half-spread, 2p." Bound: $E[\text{profit}] = s - \alpha\delta \le s$. |
| 7 | fixed differently | Discrete check from the derive: min(buyers, sellers) is 700, 1,200, 1,000 at 500p, 501p, 502p; lines cross at $501 + 300/1{,}100 \approx 501.27$p; slider step is 1. New text: "Shares traded follow the lower of the two lines, peaking at 501p, just below where they cross." Also the correct option on the same screen now reads "near where the two lines cross" (key id unchanged). |
| 8 | fixed | Kyle (1985) names tightness, depth and resiliency; "a guide to how fast the book refills" keeps volume as a proxy, matching the lesson's own trap. |
| U1 l8 s6 explain | fixed (stated condition) | Tied to the lesson's own data: "Here, makers quote wide while unsure of the price after the open, then tight once volume is heavy." No general intraday claim remains. |
| U2 l8 summary ideas[2] | fixed differently | Auditor's hedge used "often"; new text scopes it to the lesson: "in this lesson's day the spread is wide after the open and tight before the close". |
| U3 l8 s8 prose | fixed | "for example 10%": the figure is now an example the screen then uses, not a market claim. |
| U4 l10 s8 explain | fixed differently | Rewritten as a hypothetical: "An options desk left short the share after a large client trade would skew its quotes the same way." No claim about what desks do. |
| U5 l11 s9 explain | fixed | "as fast as their systems allow" removes the unsourced timescale. |

Gates: validator 0 errors, 4531 warnings (unchanged), manifest unchanged; voice scan 35 on micro: 0 and 0; `micro-L1-3-r2-concepts.py`, `micro-3-perf-numbers.py` exit 0; `micro-L1-3-concepts.py` exit 0 once `sympy` is on the path (without it the script stops at `import sympy`, a pre-existing environment gap); playthrough desktop and `--mobile` green for l7, l8, l10, l11, l12, homework-1, review-3.

## Fix-pass read

Reader: fresh Fable reader, blind to the audit, its ledger and the fixer's notes. Range: `git diff 0adb8041~1 0adb8041 -- app/content/courses/micro/` (seven files, 16 changed strings; content identical at HEAD). Each row was read in its item, numbers recomputed from the item's data, and the one code claim run. External sources: the EU cap was confirmed by web search (ESMA statements on Regulation (EU) 2024/791); the LSE closing-price fallback by search snippets of LSE notices only, since `www.lseg.com` is not reachable from this session and the current MIT201 text was not fetched. Papers are cited from recall.

| # | File | JSON path | New text (short) | Verdict | Basis |
|---|---|---|---|---|---|
| 1 | homework-1.json | `h-expr.explain.text` | Raising the fill chance by 0.01 cuts the cost by $0.01(2h + c)$ | correct | $E = h + c - p(2h + c)$, so $E(p) - E(p + 0.01) = 0.01(2h + c)$; checked numerically on three random $(p, h, c)$. Agrees with key and `accept`. |
| 2 | l10-inventory.json | generalise (line 1034) `.prose` | Avellaneda-Stoikov turns that into our rule, with $\tau$ the time left in the trading session | correct | Avellaneda and Stoikov (2008), reservation price $r = s - q\gamma\sigma^2(T - t)$; here $A$ is their $\gamma$ and $\tau = T - t$. Key x4 follows from $\sigma^2$. |
| 3 | l10-inventory.json | calls item (line 1160) `.explain.text` | An options desk left short the share after a large client trade would skew its quotes the same way | imprecise | See finding 1. The screen's maker is short calls, not the share, and "its quotes" is unspecified: a desk short delta raises call quotes but lowers put quotes. |
| 4 | l10-inventory.json | close item (line 1472) `.explain.text` | Counting the night in $\tau$, the skew rule agrees: $\gamma$ is large... In the model itself $\tau$ stops at the close, so its skew fades | correct | $0.02 \times 2{,}000 \times £5 = £200$. Stated condition for the first claim; second is $\gamma = A\sigma^2(T - t) \to 0$ as $t \to T$ in Avellaneda and Stoikov (2008). Agrees with option `var` and the step hint. |
| 5 | l11-adverse-selection.json | line 773 option `four.why` | On average one trade earns at most the half-spread | correct | Item data: $0.2 \times (-8) + 0.8 \times 2 = 0$p; the uninformed term caps the mean at 2p. "On average" is needed, since one realised trade can earn more. £4.00 is 4p on 100 shares. |
| 6 | l11-adverse-selection.json | sweep item (line 1218) `.explain.text` | Makers... pull or move their quotes as fast as their systems allow | correct | No speed figure is now claimed. Quote cancellation after trades on other venues: van Kervel (2015), Review of Financial Studies 28(7); Budish, Cramton and Shim (2015), QJE. Cited from recall. |
| 7 | l12-venues.json | line 296 option `switch.text` | the most trade near where the two lines cross | correct | min of buyers and sellers at 499 to 503p is 300, 700, 1,200, 1,000, 600: peak at 501p; segments cross at 501.27p. |
| 8 | l12-venues.json | same item (line 328) `.explain.text` | Shares traded follow the lower of the two lines, peaking at 501p, just below where they cross | correct | Same recompute. At 501p sellers (1,200) still limit; crossing at $501 + 300/1100 = 501.27$p. Agrees with feedback and option `rises`. |
| 9 | l12-venues.json | no-overlap item (line 861) `.explain.text` | the orders stay unmatched, and the exchange takes the closing price from earlier trades | correct | Best buy 249p below best sell 251p, so zero matches. LSE fallback: VWAP of the last ten minutes of continuous trading, else last automated trade (LSE closing-price notices; current MIT201 not fetched). |
| 10 | l12-venues.json | dark item (line 1062) `feedback.byKey.unreg` | regulated venues with their own rules, and the EU caps their volume | correct | MiFIR Art. 5: double volume cap, replaced from October 2025 by a single 7% EU-wide cap on reference-price-waiver trading (Regulation (EU) 2024/791; ESMA statements). Limited to the EU, which is right: the UK dropped its cap. Agrees with option `unreg.why`. |
| 11 | l7-where-is-the-price.json | code item (line 1219) `.explain.text` | Without the check, `bids[0]` or `asks[0]` on an empty list raises `IndexError` | correct | Run: the hint's solution body without the guard raises `IndexError` on both one-sided test books. Agrees with `byKey.error`. |
| 12 | l8-liquidity.json | intraday item (line 787) `.explain.text` | Here, makers quote wide while unsure of the price after the open, then tight once volume is heavy | correct | $500{,}000 \times 12$ bp $= £600$, $\times 3.2$ bp $= £160$, gap £440. "Here" limits the story to the lesson's share; mechanism is Glosten and Milgrom (1985). |
| 13 | l8-liquidity.json | derive item (line 914) `.prose` | trade at most a fraction $p$ of daily volume $V$, for example 10% | correct | 10% is now an example, not a frequency claim. Participation-rate limits: Kissell, The Science of Algorithmic Trading and Portfolio Management (POV schedules). $D = X/(pV)$ unchanged. |
| 14 | l8-liquidity.json | `summary.ideas[0]` | volume (a guide to how fast the book refills) | correct | Hedged; agrees with the volume screen (line 402). Resiliency as the third dimension: Kyle (1985). |
| 15 | l8-liquidity.json | `summary.ideas[2]` | in this lesson's day the spread is wide after the open and tight before the close, and liquidity vanishes in a crisis | imprecise | See finding 2. First clause is the lesson's own data (12.0 bp falling to 3.2 bp). "Vanishes" is an unconditional absolute; the lesson's crisis screen shows a tenfold spread, not no market. |
| 16 | review-3.json | last item `feedback.byKey.full` | You counted the full 4p spread. On average one trade earns at most the half-spread, 2p. | correct | Item data: $0.3 \times (-8) + 0.7 \times 2 = -1$p $= s - \alpha\delta$; slip value 4 is $2s$. Agrees with key $-1$. |

Rows read: 16. Verdicts: 14 correct, 2 imprecise, 0 wrong, 0 misleading, 0 unverified.

### Findings

1. l10-inventory.json | calls item, `explain.text` (line 1160) | imprecise, minor | The new last sentence moves from the screen's position (short 2,000 calls) to a desk "short the share", and does not say which quotes it skews. A desk short delta raises its share and call quotes but lowers its put quotes, so "the same way" holds only for some of them. | The item's key is "raise both call quotes"; short calls are cut by buying calls. | Replace the last sentence with: `An options desk left short calls after a large client trade would skew its call quotes the same way.` Verified against the key (`up`) and the feedback line.
2. l8-liquidity.json | `summary.ideas[2]` (line 1170) | imprecise, minor | "liquidity vanishes in a crisis" is stated without condition. The lesson's own crisis screen (line 799) has makers who "widen their quotes or step away" and a spread that rose tenfold. | Lesson data; Nagel (2012), "Evaporating Liquidity", RFS, documents a sharp fall, not a universal disappearance. | Replace the idea with: `Liquidity changes: in this lesson's day the spread is wide after the open and tight before the close, and in a crisis liquidity can dry up. Size positions by the days needed to exit.`

Note, outside the diff: l8-liquidity.json `summary.formula.note` (line 1175) still reads "(often 0.1)" while the fixed prose at line 914 now says "for example 10%". For agreement, change to `(for example 0.1)`. Minor.

No `wrong` row, so nothing counts towards the convergence rule.

## Fix-pass follow-up

| # | File | JSON path | Status | Basis |
|---|---|---|---|---|
| F1 (row 3) | l10-inventory.json | calls item (transfer, "How do you move your call quotes") `explain.text`, last sentence | fixed differently | The screen's "you" already is the options maker, short 2,000 calls, so the auditor's "an options desk left short calls" restates the screen. New sentence states the transfer point inside the inventory model only, with no delta or put-quote claim: "The inventory rule from shares carries over: whatever instrument you are short, you raise both your quotes in it." Agrees with key `up` and `feedback.correct`. |
| F2 (row 15) | l8-liquidity.json | `summary.ideas[2]` | fixed differently | Replaced the unconditional "liquidity vanishes in a crisis" with the lesson's own crisis data: spread series 4 bp calm to 40 bp peak, 40/4 = 10, and 4 x 10 = 40, matching the screen's "rose tenfold" (line 799). Avoids importing a claim the lesson does not show. |
| F3 (note) | l8-liquidity.json | `summary.formula.note` | fixed | "(often 0.1)" to "(for example 0.1)", agreeing with the derive prose "for example 10%" (line 914). |

Gates: validator 0 errors (manifest unchanged); voice scan 35 on micro 0 and 0; micro-3-perf-numbers.py and micro-L1-3-r2-concepts.py exit 0; micro-L1-3-concepts.py fails before any check with a pre-existing `ModuleNotFoundError: No module named 'sympy'`, unrelated to these strings; playthrough of micro/l8-liquidity and micro/l10-inventory green, desktop and `--mobile`.
