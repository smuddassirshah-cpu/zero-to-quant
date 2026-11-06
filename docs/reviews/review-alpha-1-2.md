# Alpha levels 1 and 2 (Universe; Signals): second-reader findings

Scope: `app/content/courses/alpha/` l1 to l8, `review-1.json`, `review-2.json`, `homework-1.json`, `homework-2.json`. Continuity skim of l9 to l16 (first screens, every cross-reference from L1 and L2 to levels 3 and 4).

Method: the panel was rebuilt from l1's prelude (the brief's `make_panel()`, seed 2310) and the brief's checks reproduced (235,497 cells, 15 splits, rebuild error 5.2e-16, 0.1128 and 0.1301, momentum IC 0.0325, t 2.64, 47 dates). Every stated number, graded key and `wrong[]` value was recomputed, mostly by direct code with the lesson solutions as a second route: universes, split adjustment, total returns, the survivorship and momentum studies, every rank IC, autocorrelation, clip count, sector mean, neutralising residual and rolling beta. Every claim was read against the data ("six largest", "every row", "join on their 60th day", "both sum only days that exist"). Every code widget was run in CPython (NumPy 2.5.3, pandas 3.0.5): all 19 solutions pass every hidden test and example, and every starter fails at least one. Prose about code behaviour was run too (centred windows, `stack`, rolling sums at the tail, `shift` directions).

Tool results:
- `python3 docs/reports/alpha-L1-numbers.py` (new): exit 1, 275 of 289. The 14 failing checks are findings 1 to 4, 7 to 10 and 13, plus the two `%` checks for findings 5 and 6; they stay failing until the fix pass. The script reads review-1 `items[2]`, `items[7]` and homework-1 `items[3]` both as they stand and as the fixes below rewrite them.
- `python3 docs/reports/alpha-L2-numbers.py` (new): exit 1, 168 of 170. The 2 failing checks are findings 11 and 12. It reads review-2 `items[8]` and homework-2 `items[6]` both ways too. 22 "check by hand" lines, each read; all fine (the slips are stated in other units).
- Code: 19 of 19 widgets OK (`/tmp/.../read-alpha-1-2/harness.py`).
- `cd app && node tools/validate.mjs`: 0 errors. L1 and L2 have no hits for the five new rules (`[shuffle-false]`, `[float-example]`, `[wrong-band]`, `[float-artefact]`, `[math-thousands-comma]`). They have 24 `[key-length]` warnings (finding 25 takes the three worst) and 37 advisory `O2-long-sentence` (20 words). Seven `O2-explain-answer` were each read; none blocks, since l1 `screens[1]` says "Twenty". Two `O2-no-slip` and two "unit % key above 1" are findings 5 and 6. The three l8 warnings are as the author reported.
- `VOICE_BASE=app/content/courses/alpha python3 docs/reviews/voice-scan.py 35`: 0 explanations over three sentences in the course. Nine sentences over 35 words are in L1 and L2, all in `how` lines (finding 24). There are no exclamation marks, no em-dashes in prose and no American spellings.
- Playthrough, `--local-cdn`: all 12 files passed without `--mobile`. They passed again with `--mobile --shots --why`. Lessons l1 to l4 had 15 checks each and l5 to l8 had 14, with every quiz 4/4. review-1 and review-2 recorded 9 of 9; homework-1 and homework-2 marked 7 of 7, 33 of 33. I read a sample of 440 px screenshots (l1 s1 series, l2 s7 table, l3 s5 boxes, l7 s1 number line, l8 s4 scatter) and found no layout faults.

Format: `N. file | JSON path | severity | problem | evidence | exact fix`. Severities: wrong, misleading, voice, layout, continuity.

## Findings

1. l2-splits-and-dividends.json | `screens[7].prose` | wrong | "The six largest drops among them are shown" is false. | The 20 death days are the 20 largest raw drops (−93.52% to −54.87%). The table shows deaths ranked 1st, 2nd and 19th (S007, S120, S024) and splits ranked 21st to 23rd (S089, S002, S016). | Replace the sentence with "Six of them are shown, with the split ratio of each day."

2. l2-splits-and-dividends.json | `screens[10].explain.text` | wrong | "Our panel has 14 split days that would trip it, each with its split record" contradicts the rule. The rule holds only drops with no split or delisting record, so no split day trips it. | Of the 34 drops below −40%, 14 have a split ratio of 2 and 20 are the share's last listed day. | Replace the last sentence with "Our panel has 34 such drops and none trips it: 14 carry a split record and 20 a delisting."

3. l3-including-the-dead.json | `screens[6].explain.text` | wrong | "three deaths in 30 shares weigh more than 20 in 200" is false: both are 10% of the names. The gap is larger on `small` because its deaths come in 300 days, not 1,260. | Deaths per share-year: small $3/30/(300/252) = 0.084$; full $20/200/5 = 0.02$. | Replace the first sentence with "On `small` the gap is larger, 8.26% against 16.54%: its 3 deaths in 30 shares come in 300 days, not 1,260."

4. l3-including-the-dead.json | `screens[8].explain.text` | wrong | "The filled panel keeps 200 shares in every row" is false. Late listings are still NaN before they list, so only 647 of the 1,260 filled rows hold 200 shares. | Count of rows with 200 non-NaN values in the zero-filled panel. | Replace the first sentence with "The filled panel keeps each dead share in every row after its death, so dead ones dilute each day's average and sit in the universe."

5. l3-including-the-dead.json | `quiz[1].widget.wrong[1]`; `quiz[1].feedback.byKey` | wrong | With `unit: "%"` the learner types per cent, so the slip "10 × 0.6 = 6" arrives as 0.06. The value 6 is reached only by typing 600, and `big` has no `byKey` line. | AUTHORING `numeric`: "with `%` the learner types 16.7 and the engine compares 0.167". | Set `wrong[1]` to `{ "id": "big", "value": 0.06, "tol": { "abs": 0.001 } }` and add `"big": "You multiplied the 10 deaths by the 60% loss. Divide by the 500 shares first: $(10/500) \\times 0.6 = 1.2\\%$."`

6. review-1.json | `items[2]` | wrong | The item has the same slip as finding 5: `total` is 4.8, which a learner reaches only by typing 480, and it has no `byKey` line. It also repeats l3 `quiz[1]`'s setup (N shares, k deaths a year, a mean loss). | 6 × 0.8 = 4.8 typed in a % field is 0.048. | Rewrite the item to give deaths over a period:
   - prose: "A universe of 250 shares lost 40 shares to delisting over 5 years, with an average last-day return of −75%."
   - `widget`: `"answer": 0.024`, `"tol": { "abs": 0.0005 }`, `"accept": "2.4%: $(8/250) \\times 0.75$."`, `"wrong": [{ "id": "ratio", "value": 0.032, "tol": { "abs": 0.0005 } }, { "id": "total", "value": 0.12, "tol": { "abs": 0.0005 } }]`
   - `feedback.correct`: "About 2.4% a year."
   - `feedback.generic`: "Not quite right. Find the deaths a year, divide by the shares, then multiply by the average loss."
   - `feedback.byKey`: `"ratio": "That is $k/N$ alone. Multiply by the 75% loss."`, `"total": "You used all 40 deaths. The bias is per year: 8 deaths a year."`
   - `explain.text`: "Forty deaths in 5 years is 8 a year, 3.2% of the universe, each with a 75% loss. Dropping them adds about $0.032 \\times 0.75 = 2.4\\%$ a year."

7. homework-1.json | `items[4].widget.wrong[1]`; `items[4].feedback.byKey.forty` | wrong | The `forty` line says "You left out the 60% loss", but leaving out the loss gives $0.024 \times 400 = 9.6$, not 40. No natural slip gives 40. | $k = 0.024 \times 400 / 0.6 = 16$; without the $/0.6$ the count is 9.6. | Set `wrong[1]` to `{ "id": "forty", "value": 9.6, "tol": { "abs": 0.3 } }` and `byKey.forty` to "You left out the 60% loss: $0.024 \\times 400 = 9.6$ is the count at a 100% loss. Divide by 0.6 as well."

8. homework-1.json | `items[5].explain.text` | wrong | The explanation names choices by place ("Lines a and b ... c and d"), and the choices shuffle. Its last sentence is also false. Both right lines blank the last 21 rows, as `forward_returns` does. They also give NaN for any window with a missing day, where `forward_returns` compounds the days that exist. | `L.rolling(21).sum().shift(-21)`: the last 21 rows are NaN, and 800 cells before them are NaN where `forward_returns(ret, 21)` has a value (deaths inside the window). | "A forward window must start on $t + 1$. The two right lines cover $t + 1$ to $t + 21$; the two others that look ahead include day $t$. Both right lines also give NaN for a window with a missing day, so a death inside it is lost; `forward_returns` compounds the days that exist."

9. homework-1.json | `items[6].widget.model`, `items[6].widget.rubric[2].text`, `items[6].explain.text` | wrong | The model holds two errors.
   - It says "20 shares listed late and join on their 60th trading day". S073 trades £3.33m a day and never passes the filter.
   - Bias 3 quotes the "today's 180" study (20.68% against 18.66%, spread 11.02% against 11.88%) as the result of keeping "full histories only". That universe also drops the late listings: it leaves 160 shares, raises both fifths and widens the spread. The rubric and the explanation repeat "spread down".

   Evidence (160 shares listed on every day): top fifth 21.40%, bottom fifth 8.43%, spread 12.97%, against 18.66%, 6.78% and 11.88% for everyone. Exact fix:
   - model, the Bias 3 paragraph: "**Bias 3: full histories only.** This drops every share that died, with its delisting loss, and every late listing. On `make_panel()` it keeps 160 shares and raises both fifths: the top from 18.66% to 21.40% a year, the bottom from 6.78% to 8.43%. So the spread moves from 11.88% to 12.97%. Deaths there are random; in real markets they cluster among past losers, so dropping them flatters the bottom fifth most and can shrink the spread."
   - model, the data paragraph: replace "20 shares listed late and join on their 60th trading day." with "20 shares listed late: 19 join on their 60th trading day, and S073, at £3.3m a day, never passes the filter."
   - `rubric[2].text`: "Full histories only: survivorship bias from dropping the dead and the late listings; every fifth's return pushed up (the top by about 2.7 points here), with the spread's direction unclear (up 1.1 points on this panel, down when deaths cluster among losers)"
   - `explain.text`: "Each bias has a mechanism and pushes the mean return one way, but none has a safe direction for the spread. That is why the honest response is a rerun with a data paragraph a reviewer can check, not a corrected number."

10. l4-returns-panel.json | `screens[8].prose`; `screens[8].canvas.params.lines[3]`, `[4]`; `screens[8].feedback.byKey.good`; `screens[8].explain.text` | wrong | The stated ICs do not reproduce. Weekly dates 5, 10, ... up to the last date where `forward_returns(ret, 5)` exists give 250 dates, not 249. On them version a gives −0.0242 (t −4.54) and version b gives +0.1694 (t 32.45). Momentum's leak is 0.0356, not 0.0366. I tried other date sets: starts 0 to 10 give b from 0.1613 to 0.1725, and none gives 0.1697 together with −0.0243. | `alpha-L1-numbers.py` prints all three routes. Momentum uses 47 monthly dates against `forward_returns(ret, 21)` (0.0334), and its leak uses `(1 + ret).rolling(21)` product `.shift(-20)`. | Exact fix:
   - prose: "On 250 weekly dates the rank IC (lesson 9) is −0.0242 with one version and +0.1694 with the other: a t statistic of 32."
   - `lines[3]`: `"IC with a: -0.0242   t = -4.5"`
   - `lines[4]`: `"IC with b:  0.1694   t = 32.5"`
   - `byKey.good`: "The true IC is −0.0242: past winners slightly reverse. The +0.17 comes from sharing day $t$."
   - `explain.text`: replace "0.0334 against 0.0366" with "0.0334 against 0.0356".

11. l6-reversal-signal.json | `quiz[3].explain.text` | wrong | "Half went in the first three days" is false: $0.8^3 = 0.512$ is left, so 48.8% went. | The half-life is 3.1 days (lesson screen 1). | Replace the last sentence with "About half went in the first three days: $0.8^3 = 0.51$ is left."

12. l5-momentum-signal.json | `screens[7].explain.text` | wrong | "S019's sum of 0.2942" is $\ln 1.342$ from the rounded 34.2%. The sum of S019's 231 log returns is 0.2941 (0.29413). | `np.log1p(ret['S019']).iloc[1008:1239].sum()`. | Replace "0.2942" with "0.2941".

13. l1-choosing-a-universe.json | `screens[2].feedback.byKey.r2` | misleading | "It listed 58 days ago" is off by one. C lists on row 30 and 3 May is row 87, so it listed 57 days ago and has traded 58 days, as the table and hint 2 say. | `toy_panel`: `listed.iloc[:30, 2] = False`. | "You kept C. It has traded only 58 days, so it has no 60-day average yet."

14. l4-returns-panel.json | `screens[5].prose`; `screens[5].explain.text` | misleading | The prose and the console say `stack()` drops NaN cells, and the explanation then says it keeps them. Both are true of different pandas versions, but neither sentence says which. `to_long` also uses `melt`, not `stack`. | In pandas 2.2.3 (the app's Pyodide) `ret.stack()` drops NaN; in pandas 3.0.5 it returns 252,000 rows. | Prose: replace "and drops NaN cells" with "and, in the pandas here (2.2), drops NaN cells". Explain, last sentence: "pandas 3 keeps NaN cells in `stack()`, so `to_long` drops them itself rather than relying on it."

15. review-1.json | `items[8].explain.text` | misleading | "A whole-sample mean would have admitted the share long before" depends on how long each volume regime lasts. With "a long time" at £1m, a whole-sample mean can stay below £5m. | £1m for 500 days and £10m for 100 days averages £2.5m. | Replace the last sentence with "A whole-sample mean would instead judge it on days at £10m that had not happened yet."

16. homework-2.json | `items[2].explain.text` | misleading | "so the final scores have mean 0 and sd 1 on every date" ignores the clip at ±3, which the last step applies. | `cs_zscore` clips 690 of 191,497 momentum values (l7 `screens[7]`). | Replace the last sentence with "Neutralise, then z-score, so the final scores have mean 0 and sd 1 on every date before the clip."

17. l5-momentum-signal.json | `screens[6].prose` | continuity | Level 2 reports momentum's IC as 0.0325. Level 1 (l3 `screens[3]`, l4 `screens[8]`) and level 3 (l9) report 0.0334, and nothing in L2 says why. L2's forward return is the summed log return, which drops a window with a death; l4 taught that a death compounds into the window. l9 explains the gap (0.0325 against 0.0334). L2 side should change. | `alpha-L2-numbers.py`: 0.0325 with the summed log forward return; `alpha-L1-numbers.py`: 0.0334 with `forward_returns`. | Append to the prose: "Here next month's return is the summed log return, which drops a window with a death; with lesson 4's `forward_returns` the same IC is 0.0334."

18. l6-reversal-signal.json | `screens[9].explain.text` | continuity | "Everyone else uses it to time trades they would make anyway, which level 4 prices" points at the wrong thing. l14 prices a stand-alone reversal book's turnover and break-even cost, not the timing use. | l14 `screens` prose: "Lesson 6's reversal signal, as rank weights, rebalanced daily, weekly or monthly." | "Everyone else uses it to time trades they would make anyway. Level 4 prices the stand-alone book's costs."

19. review-1.json | `items[7]` | continuity | The item repeats l4 `screens[4]` exactly: Z gains +2% and then loses −60% on its last day (−0.592). | l4 `screens[4].prose`: "+2%, then −60% on its last day". | Rewrite with fresh numbers:
   - prose: "Edge case. On row $t$ a study holds three shares equally for five days. X returns +4% and Y −2% over the window. Z returns +3% and then −50% on its last day, and has no later returns."
   - `widget`: `"answer": -0.155`, `"accept": "−15.5%: $(0.04 - 0.02 - 0.485)/3$."`, `"wrong": [{ "id": "drop", "value": 0.01, "tol": { "abs": 0.0002 } }, { "id": "last", "value": -0.16, "tol": { "abs": 0.0002 } }]`
   - `feedback.correct`: "−15.5%: Z's death is inside the window."
   - `feedback.byKey`: `"drop": "You dropped Z because its window has NaN. Its holder still lost 48.5%."`, `"last": "You used −50% for Z. It gained 3% first: $1.03 \\times 0.50 - 1 = -0.485$."`
   - `explain.text`: "Z's forward return compounds to its death: $1.03 \\times 0.50 - 1 = -0.485$. Averaged with +4% and −2% it gives −15.5%. Dropping Z would report +1%."

20. review-2.json | `items[8]` | continuity | The item repeats l6 `screens[8]` (a decay factor, find the half-life) and `screens[1]`. | l6 `screens[8].question`: "decays by a factor of 0.9 a day. What is its half-life in days?" | Ask the inverse:
   - prose: "In another market an overshoot loses half of itself every 2 days."
   - question: "What share of an overshoot is left after one day?"
   - `widget`: `"answer": 0.7071`, `"tol": { "abs": 0.002 }`, `"unit": "%"`, `"accept": "70.7%: $\\phi^2 = 0.5$ gives $\\phi = \\sqrt{0.5} = 0.7071$"`, `"wrong": [{ "id": "lin", "value": 0.75, "tol": { "abs": 0.002 } }]`
   - `feedback.correct`: "Correct. $\\sqrt{0.5} = 0.7071$, so 70.7% is left after a day."
   - `feedback.generic`: "Not quite. Solve $\\phi^2 = 0.5$."
   - `feedback.byKey.lin`: "You took 25 points off a day. The decay is a fixed share of what is left: $\\phi^2 = 0.5$."
   - `explain.text`: "$\\phi^2 = 0.5$ gives $\\phi = \\sqrt{0.5} = 0.7071$, and $\\ln 0.5 / \\ln 0.7071 = 2$ days. A fade this fast suits a shorter reversal window than five days."

21. homework-2.json | `items[6]` | continuity | The item asks for a number that l5 `screens[5].explain.text` already states: "It first gets a score 220 trading days after its first return". | Same rule, same answer. | Change the rule to 150 returns:
   - prose: "A share lists and has its first daily return on day $L$. A colleague's rule needs 150 returns in the window $t - 251$ to $t - 21$."
   - `widget`: `"answer": 170`, `"accept": "170: we need $t - 21 - L + 1 \\ge 150$"`, `"wrong": [{ "id": "two", "value": 150, "tol": { "abs": 0 } }, { "id": "off", "value": 171, "tol": { "abs": 0 } }, { "id": "full", "value": 252, "tol": { "abs": 0 } }]`
   - `feedback.correct`: "Correct. At $t = L + 170$ the window holds days $L$ to $L + 149$."
   - `feedback.byKey.full`: "That would need the full 231 returns plus the skip. The rule asks for 150."
   - `explain.text`: "Returns from $L$ to $t - 21$ number $t - 21 - L + 1$. Setting that to 150 gives $t = L + 170$, 50 days sooner than our rule of 200. Until then the share is listed but unranked."

22. homework-1.json | `items[3]` | continuity | The item repeats review-1 `items[5]`: a split and a dividend per new share on the same day, find the total return (0). | review-1 `items[5]`: £150, two for one, £0.75, £74.25. | Ask for the dividend instead:
   - prose: "A share closes at £96. The next day it splits three for one and closes at £31.60."
   - question: "What cash dividend per new share that day would make the holder's total return exactly 0, in £?"
   - `widget`: `"answer": 0.40`, `"tol": { "abs": 0.005 }`, `"unit": "£"`, `"label": "Dividend per new share (£)"`, `"accept": "£0.40: $3 \\times (31.60 + D)/96 = 1$ gives $D = 32 - 31.60$."`, `"wrong": [{ "id": "old", "value": 1.20, "tol": { "abs": 0.005 } }, { "id": "raw", "value": 64.40, "tol": { "abs": 0.005 } }]`
   - `feedback.correct`: "£0.40: three shares at £31.60 plus £1.20 cash is £96."
   - `feedback.generic`: "Not quite right. One old share at £96 is three new shares at £32 each."
   - `feedback.byKey`: `"old": "£1.20 is the cash on the three new shares together. Per new share it is £0.40."`, `"raw": "You ignored the split. The holder has three shares, so the gap is $96/3 - 31.60$."`
   - `explain.text`: "Before the split one share is worth £96, or £32 for each of the three new shares. At £31.60 each, a dividend of £0.40 per new share fills the gap. Any other dividend moves the total return away from 0."

23. homework-1.json, review-1.json, review-2.json | freshness note, no change | continuity | These items rework a lesson setup with new numbers: review-1 `items[0]` (l1 `quiz[1]`), `items[1]` (l2 `quiz[3]`) and `items[3]` (l4 `quiz[1]`); review-2 `items[2]` (l7 `screens[3]` and `quiz[1]`) and `items[3]` (l8 `quiz[1]`); homework-1 `items[5]` (review-1 `items[6]` at $h = 21$, but its two right lines are new). As retrieval practice they are acceptable. | `fresh-check.mjs` could not run on course sets (Engine below), so this was a hand grep. | None required. If the fixer has time, apply finding 22's pattern to review-1 `items[1]` (ask for the ratio from the two closes).

24. l2, l4, l5, l8, homework-1, homework-2 | nine `how` lines | voice | These first sentences run over 35 words (36 to 65; `voice-scan.py 35`). | Voice scan output. | Replace only the sentence quoted (the "NaN prints as ..." and "The first run loads ..." sentences stay):
   - homework-1 `items[0].widget.how`: "Check runs 8 hidden tests on a six-day hand panel with `window=2`: a split (A), a late listing (B), a death at −80% (C) and an illiquid share (D). It repeats that panel with a daily volume frame, then runs `small` with the default 60-day window (nothing kept in the first 60 rows, the count kept, the mean return a year)."
   - homework-2 `items[0].widget.how`: "Check runs 9 hidden tests. Some use hand-made shares with betas 2, 0.5 and a late listing at 1.5, and some compare estimated with true betas on `make_panel(30, 600, 5)` (correlation above 0.7, mean error to 4 places). A spy changes returns from row 400 and checks the betas on row 399 do not move. The rest check the neutralised signal on monthly dates: no beta or sector left, sds to 4 places."
   - l2 `screens[5].widget.how`: "Check runs 6 hidden tests: a hand frame with one split in each share, a share with two splits, a late listing (NaN before it lists, compared as −1) and the column names. The last two compare with `adj_close` on `make_panel(30, 300, 5)` and on `make_panel()`: the largest error must be below 1e-9."
   - l2 `screens[6].widget.how`: "Check runs 6 hidden tests: the five-day table from this lesson, its first row, and a split and a dividend on the same day. On `small` they then check the largest error against `ret`, the count of first days left NaN (one per share) and the mean return."
   - l4 `screens[6].widget.how`: "Check runs 8 hidden tests: share B with $h = 1$ and 5, the death inside the window, `ValueError` for $h = 0$, and agreement with a slow loop on `small` (values and NaN). A spy rewrites every return up to row 100 (rows from 100 on must not move), and the last test checks the empty tail for $h = 21$."
   - l4 `screens[7].widget.how`: "Check runs 7 hidden tests: the frame shown (rows, columns and index), the shape of `small` in long form and no NaN values. The rest check its first rows as ISO dates and a round trip back to wide form with `pivot`."
   - l5 `screens[4].widget.how`: "Check runs 8 hidden tests: two hand-made shares, the NaN rows before 200 returns exist, and short windows passed as arguments. A spy changes the last returns and checks the signal before them does not move, and the rest use `make_panel(30, 300, 5)`, already defined."
   - l8 `screens[3].widget.how`: "Check runs 6 hidden tests: the table's frame and a sector Series in a different order from the columns. The rest use momentum from `make_panel(30, 300, 5)`, already defined with `momentum_12_1`: each sector sums to 0 on every date and NaN stays NaN."
   - l8 `screens[5].widget.how`: "Check runs 8 hidden tests: an eight-share date, a date with too few shares, and residuals that sum to 0 against beta and within every sector to 9 places. The rest check seeded values on `make_panel(30, 300, 5)` momentum, already defined."

25. l8-neutralising.json `quiz[3]`, l7-ranks-and-z.json `quiz[2]`, l2-splits-and-dividends.json `screens[10]` | `widget.options` (key) | voice | In these three, the key alone carries an explanation and is 3 to 7 times the length of the distractors, so length gives it away (advisory rule 586; the other 21 `[key-length]` hits are milder). | l8 key 93 characters against 14; l7 108 against 30; l2 109 against 49. | Exact fix:
   - l8 `quiz[3]` option `nan`: "NaN for every share". The explanation already gives the reason.
   - l7 `quiz[2]` option `dates`: "Dates mix, so the book's balance swings with the market".
   - l2 `screens[10]` option `flag`: "Hold any unexplained drop below −40% for a check".

## Continuity

Notation and conventions in l9 to l16 match L1 and L2: wide date-by-share frames, NaN outside the universe, `forward_returns` from $t + 1$, rank scores on $[-0.5, 0.5]$, $\sqrt{252}$ Sharpe, the panel's half spread. These cross-references hold: l4 "rank IC (lesson 9)"; l7 "Level 3 measures a signal by its rank IC"; l5 "Level 4 builds the drawdown figure" (l16 `max_drawdown`); l5 and l8 "Level 4 measures the market exposure" and "checks the book's exposures" (l13 "Dollar neutral is not beta neutral"); l4 "Level 4's research note lists it" (l16); l2 "keeps raw and adjusted prices both" (l16, yfinance `auto_adjust`); homework-2 "another variant tried, which level 4 counts" (l15 deflation); l6 and review-2 "Level 4 measures that turnover" (l14). The two that fail are findings 17 and 18, both on the L2 side. l9's first screens build on l5's momentum and l4's `forward_returns` without re-teaching them.

## Engine

- `fresh-check.mjs --file content/courses/alpha/review-1.json --as exams` throws ENOENT: `scanCode` opens `content/exams/review-1.json`. The same call on `homework-2.json` ran past 120 s and was stopped. This adds a symptom to the existing inbox bullet (garch review, engine 4). Freshness for these sets was therefore checked by hand grep (finding 23).
- `numbers_lib.py`: a path key with a hyphen (`feedback.byKey.test-3`) cannot be addressed. `_PART` stops at `-` and reports `no key "test"`, so a script must read the whole `byKey` object instead. Wanted: allow `[\w-]` in a key.
