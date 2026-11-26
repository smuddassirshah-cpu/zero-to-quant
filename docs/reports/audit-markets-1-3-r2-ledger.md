# Claim ledger: markets levels 1 to 3, blind audit round 2

Commit audited: 7bc79413. Audit: `docs/reviews/audit-markets-1-3-r2.md`. Script: `docs/reports/markets-L1-3-concepts-r2.py`.

Stage 1 course, full ledger: one row for each definition, rule, convention, graded key, wrong option, slip, hint, feedback line and explanation. Every row was read against the source named; every number in it was recomputed, by hand or in the script. Hull section numbers are from the 10th edition (the 11th renumbers chapter 4: measuring rates is §4.4, duration §4.10).

Rows: 2440. Verdicts: correct 2431, imprecise 7, wrong 2, misleading 0, unverified 0.


## l1-interest-on-interest

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `summary.ideas[0]` | Simple interest pays on the original deposit only. Compound interest pays on the whole balance, earlier inter… | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `summary.ideas[1]` | Compounding multiplies by $1 + r$ each period, so $P$ grows to $P(1 + r)^n$ after $n$ periods. | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `summary.ideas[2]` | Interest on interest is the gap: zero after one period, then widening fast. The rule of 72 estimates the doub… | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `summary.formula` | Compound growth: P(1 + r)^n; Enter the rate as a decimal: 5% is $r = 0.05$. | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `summary.trap` | Adding the rate $n$ times, $P(1 + rn)$, is simple interest. Compounding multiplies by $1 + r$, $n$ times. | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[0].prose` | Two accounts each take £1,000.00 at 5% a year. The simple account pays £50.00 a year, 5% of the original depo… | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[0].canvas.derive` | formulas: values.simple=1000 * (1 + 0.05 * n); values.comp=1000 * pow(1 + 0.05, n) | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[0].widget.answer` | key 128.89 £: £128.89: £1,628.89 − £1,500.00. | correct | Recomputed; right under the convention the item states |
| `screens[0].feedback.byKey.same` | slip 0: You expected equal balances because both pay 5%. Look at the bars at 10 years: they differ. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.balance` | slip 1628.89: That is the compound balance. Take away the simple balance, £1,500.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.simple-int` | slip 500: £500.00 is the simple account's interest. The question asks for the gap between the two balances. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.comp-int` | slip 628.89: £628.89 is the compound account's interest. Take away the simple account's £500.00 of interest. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].hints[0]` | Set the slider to 10 and read both bars. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[1]` | The labels on the bars give the two balances. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[2]` | Subtract: £1,628.89 − £1,500.00. | correct | Derivation or arithmetic step, checked |
| `screens[0].feedback.correct` | The compound account is £128.89 ahead after 10 years. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[0].feedback.generic` | Not quite right. Read both balances at 10 years, then subtract. | correct | Derivation or arithmetic step, checked |
| `screens[0].explain.text` | At 10 years the bars read £1,500.00 and £1,628.89, a gap of £128.89. At 1 year they were equal. The gap widen… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[1].prose` | Look inside the compound account. Year 1 pays 5% of £1,000.00, which is £50.00. So year 2 starts with £1,050.… | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[1].canvas.params.rows` | table: [["1", "£1,000.00", "£50.00"], ["2", "£1,050.00", "?"]] | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[1].widget.answer` | key 52.5 £: £52.50: 5% of £1,050.00. | correct | Recomputed; right under the convention the item states |
| `screens[1].feedback.byKey.original` | slip 50: You paid 5% on the original £1,000.00, as the simple account does. The compound account pays on £1,0… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].feedback.byKey.total` | slip 102.5: £102.50 is the interest over both years. The question asks for year 2 alone. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].feedback.byKey.balance` | slip 1102.5: £1,102.50 is the balance at the end of year 2. Take away the £1,050.00 it started with. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].hints[0]` | Interest is 5% of the balance at the start of the year. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[1]` | Year 2 starts with £1,050.00. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[2]` | $0.05 \times 1050 = 52.50$. | correct | Derivation or arithmetic step, checked |
| `screens[1].feedback.correct` | £52.50: 5% of £1,050.00. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[1].feedback.generic` | Not quite right. Take 5% of the balance at the start of year 2. | correct | Derivation or arithmetic step, checked |
| `screens[1].explain.text` | Year 2 pays £52.50, which is £2.50 more than year 1. That £2.50 is 5% of the £50.00 earned in year 1. The acc… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[2].prose` | Paying interest on the whole balance, earlier interest included, is **compound interest**. Paying only on the… | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[2].canvas.state` | plotted values: {"y0": 1000, "y1": 1050, "y2": 0, "y3": 0} | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[2].widget.rows[1][2]` | cell key 52.5; Year 2 interest is 5% of £1,050.00, not of £1,000.00. | correct | Recomputed; right under the convention the item states |
| `screens[2].widget.rows[1][3]` | cell key 1102.5; Year 2 ends at its start, £1,050.00, plus its interest. | correct | Recomputed; right under the convention the item states |
| `screens[2].widget.rows[2][1]` | cell key 1102.5; Year 3 starts where year 2 ended: copy the year 2 end balance. | correct | Recomputed; right under the convention the item states |
| `screens[2].widget.rows[2][2]` | cell key 55.125; Year 3 interest is 5% of the year 3 starting balance, £1,102.50. | correct | Recomputed; right under the convention the item states |
| `screens[2].widget.rows[2][3]` | cell key 1157.625; Year 3 ends at its start plus its interest. | correct | Recomputed; right under the convention the item states |
| `screens[2].hints[0]` | Each year's interest is 5% of that year's starting balance. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[1]` | Year 3 starts where year 2 ended. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[2]` | Year 2: £52.50, ending at £1,102.50. Year 3: 5% of £1,102.50 is £55.13, ending at £1,157.63. | correct | Derivation or arithmetic step, checked |
| `screens[2].feedback.correct` | Each year multiplied the balance by 1.05: £1,157.63 after 3 years. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[2].feedback.generic` | Not quite right. Start each year from the end of the year before, then add 5% of it. | correct | Derivation or arithmetic step, checked |
| `screens[2].explain.text` | Each row multiplied the balance by 1.05, so $1000 \times 1.05^3 = 1157.63$. Simple interest gives £1,150.00 a… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[3].prose` | Back to the two accounts, now beside a bar at £2,000.00. How long does each take to double the deposit? | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[3].canvas.derive` | formulas: values.simple=1000 * (1 + 0.05 * n); values.comp=1000 * pow(1 + 0.05, n); values.target=2000 | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[3].widget.answer` | key 15 : Year 15: £2,078.93. Year 14 is £1,979.93. | correct | Recomputed; right under the convention the item states |
| `screens[3].feedback.byKey.simple` | slip 20: 20 years is when the simple account doubles: £50.00 a year for 20 years. The compound account gets t… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].feedback.byKey.under` | slip 14: After 14 years the account holds £1,979.93, just short of £2,000.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].feedback.byKey.rule72` | slip 14.4: 14.4 is a quick estimate of the doubling time. The question asks for the first whole year past £2,… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].hints[0]` | Watch the compound bar against the Double bar. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[1]` | Try 14 and 15 years. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[2]` | After 14 years it holds £1,979.93; after 15 years, £2,078.93. | correct | Derivation or arithmetic step, checked |
| `screens[3].feedback.correct` | Year 15. Year 14 leaves it at £1,979.93, just short. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[3].feedback.generic` | Not quite right. Find the first year where the compound bar is above the Double bar. | correct | Derivation or arithmetic step, checked |
| `screens[3].explain.text` | Exactly, doubling takes $\dfrac{\ln 2}{\ln 1.05} = 14.21$ years. Traders estimate it with the **rule of 72**:… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[4].prose` | Now you control the rate too, including negative rates. Try several rates, and look at the bars after exactly… | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[4].canvas.derive` | formulas: values.simple=1000 * (1 + r * n); values.comp=1000 * pow(1 + r, n) | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[4].widget.options[right]` | key: In year 1 there is no earlier interest to earn interest | correct | Recomputed; right under the convention the item states |
| `screens[4].widget.options[rate].why` | wrong option 'Both accounts use the same rate': They use the same rate at 10 years too, and differ there. Som… | correct | Checked false under the item's premises; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[4].widget.options[less].why` | wrong option 'The compound account pays less in its first year': Set 1 year: the bars are level, not lower. B… | correct | Checked false under the item's premises; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[4].widget.options[rounding].why` | wrong option 'Rounding hides a small gap after one year': Nothing is rounded away. $1000(1 + r)^1$ and $1000(… | correct | Checked false under the item's premises; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[4].hints[0]` | What does each account pay interest on during year 1? | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[1]` | In year 1 both pay on the £1,000.00 deposit. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[2]` | $(1 + r)^1 = 1 + r \times 1$, so the two formulas agree at one year. | correct | Derivation or arithmetic step, checked |
| `screens[4].feedback.correct` | Interest on interest needs some interest to exist first. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[4].feedback.generic` | Not quite right. Ask what each account pays interest on during year 1. | correct | Derivation or arithmetic step, checked |
| `screens[4].explain.text` | In year 1 both accounts pay on the same £1,000.00, so $(1 + r)^1 = 1 + r$. The gap opens in year 2. At −5% fo… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[5].prose` | A fund grows £2,000.00 at 6% a year, compounded yearly, for 5 years. A colleague works out the final balance … | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[5].canvas.params.rows` | table: [["Colleague: add 6% five times", "£2,600.00"], ["Compound: multiply by 1.06 five times", "?"]] | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[5].widget.answer` | key 2676.45 £: £2,676.45: $2000 \times 1.06^5$. | correct | Recomputed; right under the convention the item states |
| `screens[5].feedback.byKey.simple` | slip 2600: You multiplied by $1 + 0.06 \times 5$, adding the rate five times. That is simple interest. Compou… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.times` | slip 10600: You multiplied by 1.06 and then by 5. The 5 belongs in the power: $1.06^5$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.once` | slip 2120: £2,120.00 is one year of growth. The fund compounds for five. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.interest` | slip 676.45: £676.45 is the interest alone. Add the £2,000.00 deposit. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].hints[0]` | Compounding multiplies by 1.06 each year. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[1]` | Five years means five factors of 1.06. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[2]` | $2000 \times 1.06^5 = 2000 \times 1.338226 = 2676.45$. | correct | Derivation or arithmetic step, checked |
| `screens[5].feedback.correct` | £2,676.45. The colleague's sum misses £76.45. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[5].feedback.generic` | Not quite right. Multiply by 1.06 once for each year. | correct | Derivation or arithmetic step, checked |
| `screens[5].explain.text` | Compounding multiplies by 1.06 once a year: $2000 \times 1.06^5 = 2676.45$. The colleague's $1 + 0.06 \times … | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[6].prose` | Each year you multiplied by $1 + r$. After $n$ years a deposit $P$ becomes $$P(1 + r)^n \ \text{compound}, \q… | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[6].widget.options[right]` | key: $P(1 + r)^n - P(1 + rn)$ | correct | Recomputed; right under the convention the item states |
| `screens[6].widget.options[all].why` | wrong option '$P(1 + r)^n - P$': That is all the compound interest, the simple part included. Take away the s… | correct | Checked false under the item's premises; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[6].widget.options[simple].why` | wrong option '$Prn$': That is the simple interest. Interest on interest is what compounding adds on top of it. | correct | Checked false under the item's premises; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[6].widget.options[balance].why` | wrong option '$P(1 + r)^n$': That is the whole compound balance, deposit included. | correct | Checked false under the item's premises; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[6].hints[0]` | Interest on interest was the gap between the two bars. | correct | Derivation or arithmetic step, checked |
| `screens[6].feedback.correct` | The gap between the bars, written as a formula. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[6].feedback.generic` | Not quite right. Interest on interest was the gap between the compound and the simple balance. | correct | Derivation or arithmetic step, checked |
| `screens[6].explain.text` | The gap between the bars was the compound balance minus the simple one. For £1,000.00 at 5% over 10 years it … | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[7].prose` | You hold £1,000.00 in savings at 4% a year. You also owe £1,000.00 on a credit card at 20% a year, compounded… | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[7].canvas.derive` | formulas: values.save=1000 * pow(1.04, n); values.card=1000 * pow(1.2, n) | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[7].widget.answer` | key 3.8018 : 3.80 years: $\ln 2 / \ln 1.2$. | correct | Recomputed; right under the convention the item states |
| `screens[7].feedback.byKey.simple` | slip 5: You added £200.00 a year, which takes 5 years. The debt compounds, so it doubles sooner. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].feedback.byKey.rule72` | slip 3.6: 3.6 is the rule of 72, $72 \div 20$. It runs short at high rates. Solve $1.2^n = 2$ exactly. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].feedback.byKey.savings` | slip 17.67: 17.67 years is the savings account at 4%. The card charges 20%. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].hints[0]` | Solve $1.2^n = 2$ for $n$. | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[1]` | Take logs of both sides: $n \ln 1.2 = \ln 2$. | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[2]` | $n = \ln 2 / \ln 1.2 = 0.6931 / 0.1823 = 3.80$. | correct | Derivation or arithmetic step, checked |
| `screens[7].feedback.correct` | 3.80 years. The savings need 17.67 years to double. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[7].feedback.generic` | Not quite right. Solve $1.2^n = 2$ with logs. | correct | Derivation or arithmetic step, checked |
| `screens[7].explain.text` | $n = \dfrac{\ln 2}{\ln 1.2} = 3.80$ years, while the savings need $\dfrac{\ln 2}{\ln 1.04} = 17.67$. The rule… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[8].prose` | A strategy's backtest returns 1% every month for a year, with gains reinvested. It starts with £10,000.00. Th… | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[8].canvas.params.rows` | table: [["1", "£10,100.00"], ["2", "£10,201.00"], ["3", "£10,303.01"], ["…", "…"], ["12", "?"]] | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[8].widget.answer` | key 0.126825 %: 12.68%: $1.01^{12} - 1 = 0.1268$. | correct | Recomputed; right under the convention the item states |
| `screens[8].feedback.byKey.twelve` | slip 0.12: You added 1% twelve times. Each month's gain also earns returns in the months after it. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.month` | slip 0.01: 1% is one month. The question asks for the whole year. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].hints[0]` | Twelve months means twelve factors of 1.01. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[1]` | Find $1.01^{12}$, then take away 1. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[2]` | $1.01^{12} = 1.126825$, a return of 12.68%. | correct | Derivation or arithmetic step, checked |
| `screens[8].feedback.correct` | 12.68% a year, not 12%. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `screens[8].feedback.generic` | Not quite right. Multiply by 1.01 twelve times, then take away 1. | correct | Derivation or arithmetic step, checked |
| `screens[8].explain.text` | $1.01^{12} - 1 = 0.1268$, so the strategy made 12.68% on the year, ending at £11,268.25. Adding up monthly re… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `quiz[0].prose` | A fund loses 2% a year, compounded, for 10 years. It starts with £1,000.00. | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `quiz[0].widget.answer` | key 817.07 £: £817.07: $1000 \times 0.98^{10}$. | correct | Recomputed; right under the convention the item states |
| `quiz[0].feedback.byKey.simple` | slip 800: You took 2% of the original £1,000.00 each year. Each loss is 2% of a smaller balance. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.byKey.grew` | slip 1218.99: You grew the fund by 2% a year. A loss multiplies by 0.98, not 1.02. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.correct` | £817.07: each year multiplies by 0.98. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `quiz[0].feedback.generic` | Not quite right. A 2% loss multiplies by $1 - 0.02 = 0.98$ each year. | correct | Derivation or arithmetic step, checked |
| `quiz[0].explain.text` | A negative rate shrinks the balance: $1000 \times 0.98^{10} = 817.07$. Simple losses would leave £800.00. Com… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `quiz[1].prose` | Money earns 8% a year, compounded yearly. | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `quiz[1].widget.answer` | key 9 : 9 years: $72 \div 8$. The exact answer is 9.01 years. | correct | Recomputed; right under the convention the item states |
| `quiz[1].feedback.byKey.simple` | slip 12.5: 12.5 years is simple interest: $100 \div 8$. Compounding doubles sooner. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[1].feedback.correct` | $72 \div 8 = 9$ years, close to the exact 9.01. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `quiz[1].feedback.generic` | Not quite right. Divide 72 by the rate in per cent. | correct | Derivation or arithmetic step, checked |
| `quiz[1].explain.text` | The rule of 72 gives $72 \div 8 = 9$ years. Exactly, $\ln 2 / \ln 1.08 = 9.01$ years. The rule is close for r… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `quiz[2].prose` | Account A pays 10% a year simple interest. Account B pays 9% a year, compounded yearly. Each holds £1,000.00 … | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `quiz[2].widget.options[a].why` | wrong option 'A, because 10% beats 9%': You compared the rates alone. A ends at £3,000.00, but B compounds to… | correct | Checked false under the item's premises; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `quiz[2].widget.options[b]` | key: B, by £2,604.41 | correct | Recomputed; right under the convention the item states |
| `quiz[2].widget.options[same].why` | wrong option 'They end level': They are not level: A ends at £3,000.00 and B at £5,604.41. | correct | Checked false under the item's premises; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `quiz[2].widget.options[b-small].why` | wrong option 'B, by £200.00': You took the 1% gap in rates as simple interest over 20 years: £200.00. Compoun… | correct | Checked false under the item's premises; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `quiz[2].feedback.correct` | B ends at £5,604.41 against A's £3,000.00. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `quiz[2].feedback.generic` | Not quite right. Work out both balances after 20 years. | correct | Derivation or arithmetic step, checked |
| `quiz[2].explain.text` | A ends at $1000(1 + 0.1 \times 20) = 3000$. B ends at $1000 \times 1.09^{20} = 5604.41$. Over long horizons c… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `quiz[3].prose` | £500.00 is deposited at 4% a year, compounded yearly, for 3 years. | correct | BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `quiz[3].widget.answer` | key 62.43 £: £62.43: $500 \times 1.04^3 - 500$. | correct | Recomputed; right under the convention the item states |
| `quiz[3].feedback.byKey.simple` | slip 60: £60.00 is simple interest, £20.00 a year. Compounding adds interest on interest. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[3].feedback.byKey.balance` | slip 562.43: £562.43 is the balance. Take away the £500.00 deposit to leave the interest. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[3].feedback.correct` | £62.43, of which £2.43 is interest on interest. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |
| `quiz[3].feedback.generic` | Not quite right. Find the balance after 3 years, then take away the deposit. | correct | Derivation or arithmetic step, checked |
| `quiz[3].explain.text` | The balance is $500 \times 1.04^3 = 562.43$, so the interest is £62.43. Simple interest would be £60.00. The … | correct | Recomputed in the concepts script or by hand; BMA ch. 2 (compound interest); Hull 10e §4.2; derivation $P(1+r)^n$ |

## l2-present-value

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `summary.ideas[0]` | Money today beats the same money later, because it can earn interest meanwhile. | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `summary.ideas[1]` | Discounting is compounding run backwards: divide by $1 + r$ once for each year of waiting. | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `summary.ideas[2]` | A stream of cash flows is worth the sum of their present values. A perpetuity is worth $C/r$. | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `summary.formula` | Present value: PV = \dfrac{C}{(1 + r)^n}; At $n = 0$ the factor is 1: cash in hand is not discounted. | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `summary.trap` | Dividing by $1 + rn$, or by $1 + r$ just once, overprices cash that is several years away. | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[0].prose` | A client owes you £1,000.00, payable in 3 years. She offers £900.00 today instead. You can earn 5% a year, co… | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[0].widget.options[today]` | key: £900.00 today | correct | Recomputed; right under the convention the item states |
| `screens[0].widget.options[later].why` | wrong option '£1,000.00 in 3 years': You compared the two amounts as they stand. Invested at 5%, the £900.00 … | correct | Checked false under the item's premises; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[0].widget.options[same].why` | wrong option 'They are worth the same': You treated 5% as making up the £100.00 exactly. Three years of 5% on… | correct | Checked false under the item's premises; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[0].hints[0]` | What would £900.00 grow to by year 3? | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[1]` | Grow the £900.00 forward to year 3 and compare there. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[2]` | $900 \times 1.05^3 = 1041.86$, which beats £1,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[0].feedback.correct` | £900.00 today grows to £1,041.86 by year 3. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[0].feedback.generic` | Not quite right. Grow the £900.00 to year 3, then compare. | correct | Derivation or arithmetic step, checked |
| `screens[0].explain.text` | Invested at 5%, the £900.00 becomes $900 \times 1.05^3 = 1041.86$ by year 3. That beats the £1,000.00 on offe… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[1].prose` | Now turn it round. What is £1,000.00 in 3 years worth today? Each year back divides by $1 + r$, undoing a yea… | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[1].canvas.derive` | formulas: now.label={{money(1000 / pow(1 + r, 3))}} | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[1].widget.answer` | key 0.1006 %: About 10%: at 10% the value today is £751.31. Exactly, $(1000/750)^{1/3} - 1 = 0.1006$. | correct | Recomputed; right under the convention the item states |
| `screens[1].feedback.byKey.five` | slip 0.05: At 5% the value today is £863.84. A higher rate pushes it further down. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].feedback.byKey.simple` | slip 0.1111: That solves $1000 / (1 + 3r) = 750$, discounting with simple interest. Each year back divides by… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].feedback.byKey.split` | slip 0.0833: You took 25% off and split it over 3 years. Discounting divides by $1 + r$ each year instead. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].hints[0]` | Raise the rate and watch the label at Today. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[1]` | The value today passes £750.00 close to 10%. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[2]` | Exactly, $(1000/750)^{1/3} - 1 = 0.1006$, about 10%. | correct | Derivation or arithmetic step, checked |
| `screens[1].feedback.correct` | At 10% the value today is £751.31. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[1].feedback.generic` | Not quite right. Slide until the Today label reads close to £750.00. | correct | Derivation or arithmetic step, checked |
| `screens[1].explain.text` | At 10%, $1000 / 1.1^3 = 751.31$. A higher rate divides by more for each year back, so the value today falls. … | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[2].prose` | The value today of a future cash flow is its **present value**. Finding it is called **discounting**: compoun… | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[2].widget.answer` | key 863.84 £: £863.84: $1000 / 1.05^3$. | correct | Recomputed; right under the convention the item states |
| `screens[2].feedback.byKey.once` | slip 952.38: You divided by 1.05 once. The cash is 3 years away, so divide three times. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].feedback.byKey.simple` | slip 869.57: You divided by $1 + 0.05 \times 3 = 1.15$, simple interest run backwards. Divide by $1.05^3$ ins… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].feedback.byKey.minus` | slip 850: You took 15% off £1,000.00. Discounting divides; it does not subtract. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].feedback.byKey.grow` | slip 1157.63: You grew the £1,000.00 forward. Present value goes back in time. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].hints[0]` | Divide by 1.05 once for each year. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[1]` | Three arrows, so three divisions. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[2]` | $1000 / 1.05^3 = 1000 / 1.157625 = 863.84$. | correct | Derivation or arithmetic step, checked |
| `screens[2].feedback.correct` | £863.84 grows back to £1,000.00 in 3 years. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[2].feedback.generic` | Not quite right. Divide by 1.05 once for each of the 3 years. | correct | Derivation or arithmetic step, checked |
| `screens[2].explain.text` | Three steps back give $1000 / 1.05^3 = 863.84$. Check it forwards: $863.84 \times 1.05^3 = 1000.00$. The numb… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[3].prose` | A business will pay you £400.00, £500.00 and £600.00 at the ends of the next three years. The rate is 5%. Dis… | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[3].widget.rows[1][2]` | cell key 0.907029; The year 2 factor is $1/1.05^2 = 0.9070$: two years back. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[1][3]` | cell key 453.51; Multiply £500.00 by the year 2 factor. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[2][2]` | cell key 0.863838; The year 3 factor is $1/1.05^3 = 0.8638$: three years back. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[2][3]` | cell key 518.3; Multiply £600.00 by the year 3 factor. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[3][3]` | cell key 1352.77; Add the three present values, not the cash flows themselves. | correct | Recomputed; right under the convention the item states |
| `screens[3].hints[0]` | Year 2 divides by $1.05^2$; year 3 by $1.05^3$. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[1]` | The year 3 factor is the one you found on the last screen. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[2]` | Factors 0.9070 and 0.8638. Present values £453.51 and £518.30. Total £1,352.77. | correct | Derivation or arithmetic step, checked |
| `screens[3].feedback.correct` | The stream is worth £1,352.77 today, not £1,500.00. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[3].feedback.generic` | Not quite right. Multiply each cash flow by its own discount factor, then add. | correct | Derivation or arithmetic step, checked |
| `screens[3].explain.text` | Each cash flow got its own factor, smaller the later it comes. The present values add to £1,352.77, which is … | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[4].prose` | The business adds £250.00 paid today, at $t = 0$, on top of the three later cash flows. Those three are still… | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[4].widget.answer` | key 1602.77 £: £1,602.77: $250 + 1352.77$. | correct | Recomputed; right under the convention the item states |
| `screens[4].feedback.byKey.once` | slip 1590.87: You divided today's £250.00 by 1.05. It waits zero years, and $1.05^0 = 1$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].feedback.byKey.ignored` | slip 1352.77: You left out the £250.00 paid today. It counts in full. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].feedback.byKey.plain` | slip 1750: £1,750.00 adds the cash flows without discounting. Only the £250.00 is free of discounting. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].hints[0]` | How many years must the £250.00 wait? | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[1]` | At $t = 0$ the discount factor is $1/1.05^0$. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[2]` | $1.05^0 = 1$, so the £250.00 counts in full: $250 + 1352.77 = 1602.77$. | correct | Derivation or arithmetic step, checked |
| `screens[4].feedback.correct` | £1,602.77: cash paid today is not discounted. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[4].feedback.generic` | Not quite right. Discount each cash flow for its own wait. The £250.00 waits zero years. | correct | Derivation or arithmetic step, checked |
| `screens[4].explain.text` | With $n = 0$ the factor is $1/(1 + r)^0 = 1$, so the present value equals the cash flow. Cash in hand needs n… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[5].prose` | Some promises never end. A **perpetuity** pays £30.00 at the end of every year, for ever. The rate is 4%. In … | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[5].canvas.state` | plotted values: {"t1": 28.8462, "t2": 27.7367, "t3": 26.6699, "t4": 25.6441, "t5": 24.6578, "t6": 23.7094, "t… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[5].widget.answer` | key 750 £: £750.00: $30 / 0.04$. | correct | Recomputed; right under the convention the item states |
| `screens[5].feedback.byKey.pct` | slip 7.5: You divided by 4 instead of 0.04. The rate goes in as a decimal. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.due` | slip 780: £780.00 adds a payment today. The first payment comes in a year. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.once` | slip 28.85: That is the first payment's present value alone. Every later payment adds to it. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.times` | slip 1.2: You multiplied by the rate. The value is the payment divided by the rate. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].hints[0]` | Sum $\dfrac{30}{1.04} + \dfrac{30}{1.04^2} + \dots$ as a geometric series. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[1]` | First term $a = 30/1.04$, ratio $q = 1/1.04$, sum $a/(1 - q)$. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[2]` | $\dfrac{30/1.04}{0.04/1.04} = \dfrac{30}{0.04} = 750$. | correct | Derivation or arithmetic step, checked |
| `screens[5].feedback.correct` | £750.00, which is $C/r$. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[5].feedback.generic` | Not quite right. Add the endless geometric series with $\tfrac{a}{1 - q}$. | correct | Derivation or arithmetic step, checked |
| `screens[5].explain.text` | The sum is $\dfrac{C}{r} = \dfrac{30}{0.04} = 750$. An endless stream has a finite price because far-off paym… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[6].prose` | A bond will repay £5,000.00 in 3 years. The rate is 6% a year, compounded. A trader prices it today as $5000 … | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[6].widget.answer` | key 4198.1 £: £4,198.10: $5000 / 1.06^3$. | correct | Recomputed; right under the convention the item states |
| `screens[6].feedback.byKey.simple` | slip 4237.29: You divided by $1 + 0.06 \times 3 = 1.18$, the trader's shortcut. Three compounded years back d… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[6].feedback.byKey.once` | slip 4716.98: You discounted once, as if the cash came in a year. It is 3 years away. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[6].feedback.byKey.minus` | slip 4100: You took 18% off the £5,000.00. Discounting divides by the growth factor. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[6].feedback.byKey.grow` | slip 5955.08: You grew the £5,000.00 forward three years. Present value goes back. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[6].hints[0]` | Three years back means dividing by 1.06 three times. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[1]` | Find $1.06^3$ first. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[2]` | $5000 / 1.06^3 = 5000 / 1.191016 = 4198.10$. | correct | Derivation or arithmetic step, checked |
| `screens[6].feedback.correct` | £4,198.10, which is £39.19 below the trader's price. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[6].feedback.generic` | Not quite right. Divide by $1.06^3$, the growth over three compounded years. | correct | Derivation or arithmetic step, checked |
| `screens[6].explain.text` | Three years at 6% compound to $1.06^3 = 1.1910$, not 1.18. So $5000 / 1.1910 = 4198.10$. The trader's price i… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[7].prose` | You divided by $1 + r$ once for each year of waiting. A cash flow $C$ paid in $n$ years has $$PV = \frac{C}{(… | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[7].widget.options[right]` | key: $0.6139$ | correct | Recomputed; right under the convention the item states |
| `screens[7].widget.options[simple].why` | wrong option '$0.6667$': You used $1/(1 + 0.05 \times 10)$, simple interest. Discount by $1.05^{10}$ instead. | correct | Checked false under the item's premises; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[7].widget.options[one].why` | wrong option '$0.9524$': That is the one-year factor, $1/1.05$. Ten years needs the tenth power. | correct | Checked false under the item's premises; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[7].widget.options[grow].why` | wrong option '$1.6289$': That is $1.05^{10}$, the growth factor. Discounting divides by it. | correct | Checked false under the item's premises; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[7].hints[0]` | The factor is $1/(1 + r)^n$ with $n = 10$. | correct | Derivation or arithmetic step, checked |
| `screens[7].feedback.correct` | $1/1.05^{10} = 0.6139$: £1.00 in 10 years is worth £0.61 today. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[7].feedback.generic` | Not quite right. Work out $1/1.05^{10}$. | correct | Derivation or arithmetic step, checked |
| `screens[7].explain.text` | The factor is $1/1.05^{10} = 1/1.628895 = 0.6139$. So £1.00 due in 10 years is worth about £0.61 today. Every… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[8].prose` | A share is expected to pay a £500.00 special dividend in 2 years. Investors want 7% a year for waiting. | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[8].widget.answer` | key 436.72 £: £436.72: $500 / 1.07^2$. | correct | Recomputed; right under the convention the item states |
| `screens[8].feedback.byKey.simple` | slip 438.6: You divided by $1 + 0.07 \times 2 = 1.14$. Two compounded years back divide by $1.07^2 = 1.1449$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.once` | slip 467.29: You discounted for one year. The dividend is two years away. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.minus` | slip 430: You took 14% off. Discounting divides by $1.07^2$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.grow` | slip 572.45: You grew the dividend forward. We want its value today. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].hints[0]` | The dividend is 2 years away. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[1]` | Divide by $1.07^2$. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[2]` | $500 / 1.07^2 = 500 / 1.1449 = 436.72$. | correct | Derivation or arithmetic step, checked |
| `screens[8].feedback.correct` | £436.72 today. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[8].feedback.generic` | Not quite right. Divide £500.00 by $1.07^2$. | correct | Derivation or arithmetic step, checked |
| `screens[8].explain.text` | $500 / 1.07^2 = 436.72$. A buyer who pays more than that for the dividend alone earns less than 7% a year. A … | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[9].prose` | A lottery advertises a £1,000,000.00 jackpot. It pays £50,000.00 a year for 20 years, the first in a year. Mo… | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[9].canvas.state` | plotted values: {"t1": 48076.92, "t2": 46227.81, "t3": 44449.82, "t4": 42740.21, "t5": 41096.36, "t6": 39515.… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[9].widget.options[face].why` | wrong option '£1,000,000.00': You added the payments without discounting. Every payment after today is worth … | correct | Checked false under the item's premises; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[9].widget.options[once].why` | wrong option '£961,538.46': You discounted the whole £1,000,000.00 by one year. Later payments wait up to 20 … | correct | Checked false under the item's premises; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[9].widget.options[right]` | key: £679,516.32 | correct | Recomputed; right under the convention the item states |
| `screens[9].widget.options[last].why` | wrong option '£456,386.95': You discounted the whole sum by 20 years. Only the last payment waits that long. | correct | Checked false under the item's premises; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[9].hints[0]` | Each payment is discounted for its own wait. | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[1]` | The 20 present values form a geometric series with ratio $1/1.04$. | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[2]` | $50000 \times \dfrac{1 - 1.04^{-20}}{0.04} = 50000 \times 13.5903 = 679516.32$. | correct | Derivation or arithmetic step, checked |
| `screens[9].feedback.correct` | £679,516.32: about two thirds of the headline. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `screens[9].feedback.generic` | Not quite right. Discount each £50,000.00 for its own wait, then add. | correct | Derivation or arithmetic step, checked |
| `screens[9].explain.text` | The bars add to $50000 \times \frac{1 - 1.04^{-20}}{0.04} = 679516.32$. The value is about a third below the … | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `quiz[0].prose` | A customer owes you £10,000.00, due in 1 year. They offer to pay now. Your money earns 5% a year. | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `quiz[0].widget.answer` | key 9523.81 £: £9,523.81: $10000 / 1.05$. | correct | Recomputed; right under the convention the item states |
| `quiz[0].feedback.byKey.minus` | slip 9500: You took 5% off. £9,500.00 grows to only £9,975.00. Divide by 1.05 instead. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.byKey.grow` | slip 10500: You grew the invoice forward a year. Paying early is worth less, not more. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.correct` | £9,523.81 grows to £10,000.00 in a year. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `quiz[0].feedback.generic` | Not quite right. Find the sum that grows to £10,000.00 in a year at 5%. | correct | Derivation or arithmetic step, checked |
| `quiz[0].explain.text` | The fair amount is $10000 / 1.05 = 9523.81$. Taking 5% off, £9,500.00, would cost you £23.81. Discounts for e… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `quiz[1].prose` | £1,000.00 is due in 10 years. Interest rates rise from 3% to 6%. | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `quiz[1].widget.answer` | key 185.7 £: £185.70: from £744.09 to £558.39. | correct | Recomputed; right under the convention the item states |
| `quiz[1].feedback.byKey.simple` | slip 144.23: You discounted with simple interest, $1000/(1 + 10r)$. Compound back with $(1 + r)^{10}$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[1].feedback.byKey.pv6` | slip 558.39: £558.39 is the new present value. The question asks how far it fell from £744.09. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[1].feedback.correct` | It falls from £744.09 to £558.39, by £185.70. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `quiz[1].feedback.generic` | Not quite right. Work out $1000/1.03^{10}$ and $1000/1.06^{10}$, then subtract. | correct | Derivation or arithmetic step, checked |
| `quiz[1].explain.text` | At 3%, $1000/1.03^{10} = 744.09$; at 6%, $1000/1.06^{10} = 558.39$. Doubling the rate cut the present value b… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `quiz[2].prose` | A perpetuity pays £12.00 at the end of every year, for ever. The rate is 3%. | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `quiz[2].widget.answer` | key 400 £: £400.00: $12 / 0.03$. | correct | Recomputed; right under the convention the item states |
| `quiz[2].feedback.byKey.pct` | slip 4: You divided by 3, not 0.03. The rate goes in as a decimal. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.byKey.due` | slip 412: That adds a payment today. The first payment is a year away. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.correct` | $12 / 0.03 = 400$. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `quiz[2].feedback.generic` | Not quite right. A perpetuity is worth $C/r$. | correct | Derivation or arithmetic step, checked |
| `quiz[2].explain.text` | A perpetuity is worth $C/r = 12/0.03 = 400$. Each year's payment is 3% of £400.00, which is why the sum match… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `quiz[3].prose` | £800.00 will be paid in 4 years. The rate is 5% a year, compounded. | correct | BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `quiz[3].widget.options[simple].why` | wrong option '£666.67': You divided by $1 + 0.05 \times 4 = 1.2$, simple interest. Divide by $1.05^4 = 1.2155… | correct | Checked false under the item's premises; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `quiz[3].widget.options[right]` | key: £658.16 | correct | Recomputed; right under the convention the item states |
| `quiz[3].widget.options[once].why` | wrong option '£761.90': You discounted for one year. The payment is four years away. | correct | Checked false under the item's premises; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `quiz[3].widget.options[minus].why` | wrong option '£640.00': You took 20% off. Discounting divides by the growth factor. | correct | Checked false under the item's premises; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `quiz[3].feedback.correct` | $800 / 1.05^4 = 658.16$. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |
| `quiz[3].feedback.generic` | Not quite right. Divide by $1.05^4$. | correct | Derivation or arithmetic step, checked |
| `quiz[3].explain.text` | Four compounded years give $1.05^4 = 1.215506$. So $800 / 1.215506 = 658.16$. Simple discounting would overpr… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 §2.1–2.2 (present value, perpetuity, annuity); geometric series |

## l3-comparing-rates

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `summary.ideas[0]` | A nominal rate says how much is credited a year; the effective rate says how much the money actually grows in… | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `summary.ideas[1]` | Credited $m$ times a year, $r$ nominal is $(1 + \tfrac{r}{m})^m - 1$ effective, rising towards $e^r - 1$ as $… | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `summary.ideas[2]` | Compare rates only as effective rates. With one credit a year, nominal and effective agree. | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `summary.formula` | Effective annual rate: r_{\text{eff}} = \left(1 + \dfrac{r}{m}\right)^m - 1; Continuously compounded: $r_{\te… | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `summary.trap` | Dividing an annual rate by 12 gives a nominal monthly rate. The effective monthly rate is $(1 + r_{\text{eff}… | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[0].prose` | Two banks quote for a one-year deposit of £1,000.00. Bank A pays 12.6% once, at the end of the year. Bank B p… | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[0].canvas.params.rows` | table: [["A", "12.6% a year", "once, at year end"], ["B", "12% a year", "1% each month"]] | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[0].widget.options[a].why` | wrong option 'Bank A': You compared the quoted numbers, 12.6 against 12. Bank B's monthly credits earn intere… | correct | Checked false under the item's premises; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[0].widget.options[b]` | key: Bank B | correct | Recomputed; right under the convention the item states |
| `screens[0].widget.options[same].why` | wrong option 'They pay the same': They differ by 83p. Bank B multiplies by 1.01 twelve times, which is 1.1268… | correct | Checked false under the item's premises; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[0].hints[0]` | Work out each bank's balance after a year. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[1]` | Bank B multiplies by 1.01 twelve times. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[2]` | A: £1,126.00. B: $1000 \times 1.01^{12} = 1126.83$. | correct | Derivation or arithmetic step, checked |
| `screens[0].feedback.correct` | Bank B pays £1,126.83, which is 83p more than bank A. | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[0].feedback.generic` | Not quite right. Work out both balances before you decide. | correct | Derivation or arithmetic step, checked |
| `screens[0].explain.text` | Bank B's monthly 1% compounds: $1.01^{12} = 1.1268$. So B pays 12.68% over the year, beating A's 12.6%. The h… | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[1].prose` | A rate of 12% a year can be credited in $m$ equal parts of $\tfrac{0.12}{m}$. Over a year, £1.00 then grows t… | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[1].canvas.derive` | formulas: P.x=m; P.y=pow(1 + r / m, m) - 1 | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[1].widget.options[right]` | key: It rises more and more slowly, and stays below the dashed line | correct | Recomputed; right under the convention the item states |
| `screens[1].widget.options[steady].why` | wrong option 'It rises by about the same amount at each step': You read only the first steps. From 1 to 2 it … | correct | Checked false under the item's premises; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[1].widget.options[forever].why` | wrong option 'It keeps growing without limit': Each credit is smaller as $m$ grows. The rate settles under th… | correct | Checked false under the item's premises; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[1].widget.options[falls].why` | wrong option 'It rises, then falls back towards 12%': More credits never lose: each one adds interest on inte… | correct | Checked false under the item's premises; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[1].hints[0]` | Compare the step from 1 to 2 with the step from 51 to 52. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[1]` | Look at the dashed line. | correct | Derivation or arithmetic step, checked |
| `screens[1].feedback.correct` | It climbs towards the dashed line and never crosses it. | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[1].feedback.generic` | Not quite right. Compare the early steps with the late ones, and watch the dashed line. | correct | Derivation or arithmetic step, checked |
| `screens[1].explain.text` | From $m = 1$ to 2 the rate jumps from 12% to 12.36%. From 51 to 52 it barely moves. It settles on the dashed … | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[2].prose` | The quoted 12% is the **nominal** annual rate. The growth over a whole year, here 12.68% for monthly credits,… | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[2].canvas.params.functions` | curves: (1 + r/x)^x - 1; exp(r) - 1 | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[2].widget.answer` | key 0.082432 %: 8.24%: $1.02^4 - 1 = 0.0824$. | correct | Recomputed; right under the convention the item states |
| `screens[2].feedback.byKey.nominal` | slip 0.08: 8% is the nominal rate. Quarterly credits earn interest within the year, so the effective rate is … | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].feedback.byKey.quarter` | slip 0.02: 2% is one quarter's credit. The effective rate covers the whole year. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].hints[0]` | Each quarter pays $0.08 / 4 = 0.02$. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[1]` | Four quarters multiply by $1.02^4$. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[2]` | $1.02^4 - 1 = 0.0824$, so 8.24%. | correct | Derivation or arithmetic step, checked |
| `screens[2].feedback.correct` | 8.24% effective, from 8% nominal. | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[2].feedback.generic` | Not quite right. Multiply by 1.02 four times, then take away 1. | correct | Derivation or arithmetic step, checked |
| `screens[2].explain.text` | Four quarterly credits of 2% give $1.02^4 = 1.0824$. So the effective rate is 8.24%, above the 8% nominal. Th… | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[3].prose` | One nominal rate, 6%, credited three ways. For each, find what £1,000.00 becomes after a year. | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[3].canvas.params.functions` | curves: (1 + r/x)^x - 1; exp(r) - 1 | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[3].widget.rows[0][3]` | cell key 1060.9; Twice a year: $1000 \times 1.03^2$. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[1][3]` | cell key 1061.68; Monthly: $1000 \times 1.005^{12}$. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[2][3]` | cell key 1061.83; Daily: 365 credits of $\tfrac{0.06}{365}$ each, so $1000(1 + \tfrac{0.06}{365})^{365}$. | correct | Recomputed; right under the convention the item states |
| `screens[3].hints[0]` | Each row multiplies by $1 + \tfrac{0.06}{m}$, $m$ times. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[1]` | Twice a year is $1000 \times 1.03^2$. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[2]` | $1.03^2 = 1.0609$, $1.005^{12} = 1.061678$ and $(1 + \tfrac{0.06}{365})^{365} = 1.061831$. | correct | Derivation or arithmetic step, checked |
| `screens[3].feedback.correct` | 6.09%, 6.17% and 6.18% effective. | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[3].feedback.generic` | Not quite right. Multiply £1,000.00 by $1 + \tfrac{0.06}{m}$, $m$ times, for each row. | correct | Derivation or arithmetic step, checked |
| `screens[3].explain.text` | The effective rates are 6.09%, 6.17% and 6.18%. Going from monthly to daily adds only 15p on £1,000.00. More … | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[4].prose` | Let $m$ grow without limit. In Exponentials and Logarithms you found $(1 + \tfrac{r}{m})^m \to e^r$: **contin… | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[4].canvas.derive` | formulas: P.x=m; P.y=pow(1 + r / m, m) - 1 | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[4].widget.answer` | key 0.127497 %: 12.75%: $e^{0.12} - 1 = 0.1275$. | correct | Recomputed; right under the convention the item states |
| `screens[4].feedback.byKey.nominal` | slip 0.12: 12% is the nominal rate. Continuous credits add the most interest on interest. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].feedback.byKey.quad` | slip 0.1272: You stopped the series after $\tfrac{r^2}{2}$. The $\tfrac{r^3}{6}$ term adds another 0.03 point… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].feedback.byKey.monthly` | slip 0.126825: 12.68% is monthly compounding. Continuous compounding goes further, to the dashed line. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].hints[0]` | The year's growth factor is $e^{0.12}$. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[1]` | Take away 1 from the factor. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[2]` | $e^{0.12} = 1.127497$, so the effective rate is 12.75%. | correct | Derivation or arithmetic step, checked |
| `screens[4].feedback.correct` | 12.75%, the ceiling for 12% nominal. | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[4].feedback.generic` | Not quite right. Work out $e^{0.12}$, then take away 1. | correct | Derivation or arithmetic step, checked |
| `screens[4].explain.text` | $e^{0.12} - 1 = 0.1275$, the ceiling for a 12% nominal rate. The series gives $0.12 + 0.0072 + 0.000288 = 0.1… | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[5].prose` | Back to 12% nominal. Slide $m$ again and compare P with 12%. | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[5].canvas.derive` | formulas: P.x=m; P.y=pow(1 + r / m, m) - 1 | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[5].widget.options[one]` | key: $m = 1$ | correct | Recomputed; right under the convention the item states |
| `screens[5].widget.options[twelve].why` | wrong option '$m = 12$': At $m = 12$ the effective rate is 12.68%. Monthly credits earn interest within the y… | correct | Checked false under the item's premises; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[5].widget.options[never].why` | wrong option 'No value of $m$': Slide to $m = 1$: one credit at year end gives exactly 12%. | correct | Checked false under the item's premises; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[5].widget.options[cont].why` | wrong option 'Continuous compounding': Continuous compounding gives 12.75%, the highest of all. | correct | Checked false under the item's premises; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[5].hints[0]` | When is there no interest within the year to compound? | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[1]` | Slide $m$ all the way left. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[2]` | At $m = 1$: $(1 + 0.12)^1 - 1 = 0.12$. | correct | Derivation or arithmetic step, checked |
| `screens[5].feedback.correct` | One credit a year leaves nothing to compound within the year. | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[5].feedback.generic` | Not quite right. Slide $m$ down to its smallest value and read P. | correct | Derivation or arithmetic step, checked |
| `screens[5].explain.text` | With one credit a year there is no earlier interest to compound, so nominal and effective agree. This is the … | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[6].prose` | A fund's report says it returned 12% effective over the year. An analyst wants the steady monthly return that… | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[6].canvas.params.rows` | table: [["1% (the analyst's)", "12.68%"], ["?", "12.00%"]] | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[6].widget.answer` | key 0.0094888 %: 0.949%: $1.12^{1/12} - 1 = 0.00949$. | correct | Recomputed; right under the convention the item states |
| `screens[6].feedback.byKey.div` | slip 0.01: You divided 12% by 12. A monthly 1% compounds to 12.68%, too much. Take the twelfth root of 1.12 i… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[6].feedback.byKey.nominal` | slip 0.12: 12% is the whole year. The question asks for one month. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[6].hints[0]` | We need $(1 + x)^{12} = 1.12$. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[1]` | Take the twelfth root of 1.12. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[2]` | $1.12^{1/12} = 1.009489$, so 0.949% a month. | correct | Derivation or arithmetic step, checked |
| `screens[6].feedback.correct` | 0.949% a month compounds to 12.00% a year. | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[6].feedback.generic` | Not quite right. Solve $(1 + x)^{12} = 1.12$ for $x$. | correct | Derivation or arithmetic step, checked |
| `screens[6].explain.text` | We need $(1 + x)^{12} = 1.12$, so $x = 1.12^{1/12} - 1 = 0.00949$. A monthly 1% would compound to 12.68%. Div… | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[7].prose` | You raised one period's growth to the number of periods. For a nominal rate $r$ credited $m$ times a year, $$… | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[7].widget.options[right]` | key: 4.91% | correct | Recomputed; right under the convention the item states |
| `screens[7].widget.options[nominal].why` | wrong option '4.80%': That is the nominal rate. The AER includes the interest on interest from monthly credit… | correct | Checked false under the item's premises; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[7].widget.options[month].why` | wrong option '0.40%': That is one month's credit, $0.048 / 12$. The AER covers the whole year. | correct | Checked false under the item's premises; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[7].widget.options[cont].why` | wrong option '4.92%': That is $e^{0.048} - 1$, continuous compounding. Monthly credits give slightly less: $1… | correct | Checked false under the item's premises; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[7].hints[0]` | Each month credits $0.048 / 12 = 0.004$. | correct | Derivation or arithmetic step, checked |
| `screens[7].feedback.correct` | $1.004^{12} - 1 = 0.0491$, so the AER is 4.91%. | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[7].feedback.generic` | Not quite right. Compound $1.004$ over 12 months, then take away 1. | correct | Derivation or arithmetic step, checked |
| `screens[7].explain.text` | Each month credits 0.4%, and $1.004^{12} - 1 = 0.0491$. So the account must quote an AER of 4.91%. The AER le… | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[8].prose` | Two lenders offer the same £200,000.00 mortgage with no fees. Lender X charges 5.9% a year, compounded monthl… | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[8].canvas.params.rows` | table: [["X", "5.9%", "monthly", "?"], ["Y", "6.0%", "annually", "?"]] | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[8].widget.options[x].why` | wrong option 'X, because 5.9% is below 6.0%': You compared the nominal rates directly. Monthly compounding li… | correct | Checked false under the item's premises; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[8].widget.options[y]` | key: Y | correct | Recomputed; right under the convention the item states |
| `screens[8].widget.options[same].why` | wrong option 'They cost the same': They differ: X is 6.06% effective, Y is 6.00%. | correct | Checked false under the item's premises; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[8].hints[0]` | Turn both quotes into effective rates. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[1]` | Y is compounded annually, so its effective rate is 6.00%. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[2]` | X: $(1 + \tfrac{0.059}{12})^{12} - 1 = 0.0606$. | correct | Derivation or arithmetic step, checked |
| `screens[8].feedback.correct` | Y costs 6.00% effective; X costs 6.06%. | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[8].feedback.generic` | Not quite right. Compare the effective rates, not the nominal ones. | correct | Derivation or arithmetic step, checked |
| `screens[8].explain.text` | X's effective rate is 6.06%, above Y's 6.00%. On £200,000.00 that is about £124.38 more in a year's interest,… | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[9].prose` | Your broker pays 4.5% nominal on idle cash, credited daily over 365 days. You leave £20,000.00 there for a ye… | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[9].canvas.params.rows` | table: [["365-day (your broker)", "$0.045 / 365$"], ["360-day (dollar and euro money markets)", "$0.045 / 360… | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[9].widget.answer` | key 920.5 £: £920.50: $20000((1 + \tfrac{0.045}{365})^{365} - 1)$. | correct | Recomputed; right under the convention the item states |
| `screens[9].feedback.byKey.simple` | slip 900: £900.00 is 4.5% with no compounding. Daily credits earn interest too. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[9].feedback.byKey.cont` | slip 920.56: That is continuous compounding, 6p more. The broker credits daily. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[9].feedback.byKey.balance` | slip 20920.5: That is the balance. Take away the £20,000.00 to leave the interest. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[9].hints[0]` | The year's factor is $(1 + \tfrac{0.045}{365})^{365}$. | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[1]` | That factor is 1.046025. | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[2]` | $20000 \times 0.046025 = 920.50$. | correct | Derivation or arithmetic step, checked |
| `screens[9].feedback.correct` | £920.50 of interest: 4.60% effective. | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `screens[9].feedback.generic` | Not quite right. Compound daily for 365 days, then take away the £20,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[9].explain.text` | Daily credits turn 4.5% nominal into 4.60% effective, so £920.50 rather than £900.00. Continuous compounding … | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `quiz[0].prose` | A store card charges 1.5% a month, compounded monthly. | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `quiz[0].widget.answer` | key 0.195618 %: 19.56%: $1.015^{12} - 1$. | correct | Recomputed; right under the convention the item states |
| `quiz[0].feedback.byKey.simple` | slip 0.18: You multiplied 1.5% by 12. Each month's charge is also charged on later. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.correct` | $1.015^{12} - 1 = 0.1956$, so 19.56%. | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `quiz[0].feedback.generic` | Not quite right. Compound 1.015 over 12 months, then take away 1. | correct | Derivation or arithmetic step, checked |
| `quiz[0].explain.text` | Twelve monthly charges compound: $1.015^{12} = 1.1956$. So the card costs 19.56% a year, not 18%. A UK card's… | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `quiz[1].prose` | A saver can choose 5% compounded quarterly or 5.1% compounded annually. | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `quiz[1].widget.options[q].why` | wrong option '5% quarterly': You trusted the compounding to win. $1.0125^4 - 1 = 0.0509$, which is 5.09%, bel… | correct | Checked false under the item's premises; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `quiz[1].widget.options[a]` | key: 5.1% annually | correct | Recomputed; right under the convention the item states |
| `quiz[1].widget.options[same].why` | wrong option 'They pay the same': They differ: 5.09% against 5.10%. | correct | Checked false under the item's premises; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `quiz[1].feedback.correct` | 5.10% beats 5.09% effective. | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `quiz[1].feedback.generic` | Not quite right. Turn 5% quarterly into an effective rate. | correct | Derivation or arithmetic step, checked |
| `quiz[1].explain.text` | Quarterly 5% is $1.0125^4 - 1 = 0.0509$ effective. That is just below 5.1% paid once. Compounding helps, but … | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `quiz[2].prose` | A deposit earns 3% a year, compounded continuously. | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `quiz[2].widget.answer` | key 0.030455 %: 3.05%: $e^{0.03} - 1$. | correct | Recomputed; right under the convention the item states |
| `quiz[2].feedback.byKey.nominal` | slip 0.03: 3% is the nominal rate. Continuous compounding adds a little interest on interest. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.correct` | $e^{0.03} - 1 = 0.0305$. | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `quiz[2].feedback.generic` | Not quite right. The year's factor is $e^{0.03}$. | correct | Derivation or arithmetic step, checked |
| `quiz[2].explain.text` | One year multiplies by $e^{0.03} = 1.030455$. So the effective rate is 3.05%. At low rates the gap is small: … | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `quiz[3].prose` | A client wants an effective rate of exactly 10% a year, credited quarterly. | correct | Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `quiz[3].widget.answer` | key 0.096455 %: 9.65%: $4(1.1^{1/4} - 1)$. | correct | Recomputed; right under the convention the item states |
| `quiz[3].feedback.byKey.same` | slip 0.1: 10% nominal credited quarterly compounds to 10.38%. The nominal rate must be lower. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[3].feedback.byKey.quarter` | slip 0.024114: That is the quarterly rate, 2.41%. A nominal annual rate is four times it. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[3].feedback.correct` | $4(1.1^{1/4} - 1) = 0.0965$. | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |
| `quiz[3].feedback.generic` | Not quite right. Find the quarterly rate with $(1 + x)^4 = 1.1$, then multiply by 4. | correct | Derivation or arithmetic step, checked |
| `quiz[3].explain.text` | The quarterly rate solves $(1 + x)^4 = 1.1$: $x = 1.1^{1/4} - 1 = 0.02411$. The nominal rate is four times th… | correct | Recomputed in the concepts script or by hand; Hull 10e §4.2 (compounding frequency, continuous compounding), §6.1 (day counts) |

## l4-npv

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `summary.ideas[0]` | The NPV adds every cash flow's present value, the outlay counted as a negative cash flow today. | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `summary.ideas[1]` | Accept a project when its NPV is positive. The rate that makes the NPV zero is the IRR. | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `summary.ideas[2]` | For an outlay followed by inflows, NPV falls as the rate rises, and two streams can rank differently at diffe… | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `summary.formula` | Net present value: NPV(r) = \sum_{t=0}^{T} \dfrac{C_t}{(1 + r)^t}; $C_0$ is the outlay, usually negative, and… | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `summary.trap` | Summing cash flows without discounting, or ranking NPVs computed at different rates. | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[0].prose` | A project costs £1,000.00 today. It pays back £550.00 in 1 year and £550.00 in 2 years. Money left elsewhere … | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[0].widget.options[yes].why` | wrong option 'Yes: it pays back £100.00 more than it costs': You added £1,100.00 back against £1,000.00 out. … | correct | Checked false under the item's premises; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[0].widget.options[no]` | key: No: what it pays back is worth less than £1,000.00 today | correct | Recomputed; right under the convention the item states |
| `screens[0].widget.options[cant].why` | wrong option 'There is no way to tell': We can tell: discount each payment at 10%, then compare with the £1,0… | correct | Checked false under the item's premises; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[0].hints[0]` | What is each payment worth today at 10%? | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[1]` | Discount the year 1 payment once and the year 2 payment twice. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[2]` | $\tfrac{550}{1.1} + \tfrac{550}{1.1^2} = 500 + 454.55 = 954.55$. | correct | Derivation or arithmetic step, checked |
| `screens[0].feedback.correct` | The payments are worth £954.55 today, below the £1,000.00 cost. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[0].feedback.generic` | Not quite right. Value both payments today, then compare with the cost. | correct | Derivation or arithmetic step, checked |
| `screens[0].explain.text` | Today the payments are worth $\tfrac{550}{1.1} + \tfrac{550}{1.1^2} = 500 + 454.55 = 954.55$. That is £45.45 … | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[1].prose` | Count the cost as a negative cash flow, then add every present value. Slide the rate and watch the total, P. | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[1].canvas.derive` | formulas: P.x=r; P.y=-1000 + 550 / pow(1 + r, 1) + 550 / pow(1 + r, 2) | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[1].widget.answer` | key 100 £: £100.00: $-1000 + 550 + 550$. | correct | Recomputed; right under the convention the item states |
| `screens[1].feedback.byKey.no-cost` | slip 1100: You left out the £1,000.00 cost. It counts as a negative cash flow. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].feedback.byKey.ten` | slip -45.45: That is the total at 10%. Slide the rate down to 0%. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].hints[0]` | Slide the rate all the way left. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[1]` | At 0% nothing is discounted. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[2]` | $-1000 + 550 + 550 = 100$. | correct | Derivation or arithmetic step, checked |
| `screens[1].feedback.correct` | At 0% the total is the plain sum, £100.00. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[1].feedback.generic` | Not quite right. Set the rate to 0% and read the caption. | correct | Derivation or arithmetic step, checked |
| `screens[1].explain.text` | At 0% the total is the plain sum, $-1000 + 550 + 550 = 100$. Every higher rate pulls it down. It crosses zero… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[2].prose` | That total is the **net present value**, or NPV: every present value added, the cost counted as negative. A d… | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[2].canvas.params.functions` | curves: -5000 + 2000/(1+x)^1 + 2000/(1+x)^2 + 2000/(1+x)^3 | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[2].widget.rows[1][3]` | cell key 1851.85; Year 1: $2000 \times 0.925926$. | correct | Recomputed; right under the convention the item states |
| `screens[2].widget.rows[2][3]` | cell key 1714.68; Year 2: $2000 \times 0.857339$. | correct | Recomputed; right under the convention the item states |
| `screens[2].widget.rows[3][3]` | cell key 1587.66; Year 3: $2000 \times 0.793832$. | correct | Recomputed; right under the convention the item states |
| `screens[2].widget.rows[4][3]` | cell key 154.19; Add all four present values. The −£5,000.00 is one of them. | correct | Recomputed; right under the convention the item states |
| `screens[2].hints[0]` | Multiply each cash flow by its factor. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[1]` | The NPV adds all four present values, including −£5,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[2]` | £1,851.85, £1,714.68 and £1,587.66 add to £5,154.19. Take away £5,000.00: NPV £154.19. | correct | Derivation or arithmetic step, checked |
| `screens[2].feedback.correct` | NPV £154.19: positive, so the model beats leaving the money at 8%. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[2].feedback.generic` | Not quite right. Multiply each cash flow by its factor, then add all four, the cost included. | correct | Derivation or arithmetic step, checked |
| `screens[2].explain.text` | The savings are worth £5,154.19 today, so the NPV is £154.19. A positive NPV means the project beats the 8% a… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[3].prose` | The NPV depends on the rate. Here is the desk's model again, with its NPV plotted against the rate. | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[3].canvas.derive` | formulas: P.x=r; P.y=-5000 + 2000 / pow(1 + r, 1) + 2000 / pow(1 + r, 2) + 2000 / pow(1 + r, 3) | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[3].widget.answer` | key 0.097 ± 0.0015 | correct | Recomputed; right under the convention the item states |
| `screens[3].feedback.byKey.low` | At that rate the NPV is still above zero. Move right. | correct | Checked false under the item's premises; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[3].feedback.byKey.high` | The NPV is below zero there. Move left. | correct | Checked false under the item's premises; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[3].hints[0]` | Watch P cross the horizontal line at zero. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[1]` | At 8% the NPV is £154.19, still positive. Go higher. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[2]` | The NPV reaches zero at about 9.7%. | correct | Derivation or arithmetic step, checked |
| `screens[3].feedback.correct` | About 9.70%: there the savings are worth exactly £5,000.00. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[3].feedback.generic` | Not quite right. Move the slider until P sits on the zero line. | correct | Derivation or arithmetic step, checked |
| `screens[3].explain.text` | The NPV hits zero at about 9.70%. That rate is the **internal rate of return**, or IRR. We solve for it numer… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[4].prose` | Two projects each cost £1,000.00. A pays £1,331.00 in year 3. B pays £800.00, £300.00 and £100.00 over years … | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[4].canvas.derive` | formulas: PA.x=r; PA.y=-1000 + 0 / pow(1 + r, 1) + 0 / pow(1 + r, 2) + 1331 / pow(1 + r, 3); PB.x=r; PB.y=-10… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[4].widget.options[right]` | key: A wins at 4%, B wins at 8% | correct | Recomputed; right under the convention the item states |
| `screens[4].widget.options[a].why` | wrong option 'A wins at every rate, because it pays more in total': Its £1,331.00 comes last, so discounting … | correct | Checked false under the item's premises; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[4].widget.options[b].why` | wrong option 'B wins at every rate, because it pays sooner': At 4%, A's NPV is £183.25 against B's £135.50. L… | correct | Checked false under the item's premises; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[4].widget.options[tie].why` | wrong option 'They tie at every rate': The curves cross only once, near 6.7%. Elsewhere one is above the othe… | correct | Checked false under the item's premises; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[4].hints[0]` | Set 4%, then 8%, and read both NPVs. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[1]` | The curves cross between 6% and 7%. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[2]` | At 4%: A £183.25, B £135.50. At 8%: A £56.59, B £77.33. | correct | Derivation or arithmetic step, checked |
| `screens[4].feedback.correct` | The ranking flips where the curves cross, near 6.7%. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[4].feedback.generic` | Not quite right. Read both NPVs at 4% and at 8%. | correct | Derivation or arithmetic step, checked |
| `screens[4].explain.text` | The curves cross near 6.7%. Below it, A's larger total wins; above it, B's earlier cash wins. A ranking by NP… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[5].prose` | A deal pays £300.00 at the end of each of the next 4 years, for £1,100.00 today. Your other investments earn … | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[5].widget.answer` | key -83.84 £: −£83.84: $300 \times 3.3872 - 1100$. | correct | Recomputed; right under the convention the item states |
| `screens[5].feedback.byKey.undisc` | slip 100: You added the cash without discounting, as the colleague did. Each £300.00 is worth less the later … | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.no-cost` | slip 1016.16: £1,016.16 is the value of the payments. Take away the £1,100.00 cost. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.once` | slip 21.5: You discounted all £1,200.00 by one year. The later payments wait longer. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.last` | slip -184.53: You discounted all £1,200.00 by four years. Only the last payment waits that long. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.sign` | slip 83.84: The payments are worth £1,016.16 today, less than the £1,100.00 paid, so the NPV is below zero. A… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].hints[0]` | Discount each £300.00 for its own wait. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[1]` | The four factors at 7% add to 3.3872. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[2]` | $300 \times 3.3872 = 1016.16$, and $1016.16 - 1100 = -83.84$. | correct | Derivation or arithmetic step, checked |
| `screens[5].feedback.correct` | NPV −£83.84: the deal loses value at 7%. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[5].feedback.generic` | Not quite right. Discount each payment for its own wait, add them, then take away £1,100.00. | correct | Derivation or arithmetic step, checked |
| `screens[5].explain.text` | The payments are worth $300(\tfrac{1}{1.07} + \tfrac{1}{1.07^2} + \tfrac{1}{1.07^3} + \tfrac{1}{1.07^4}) = 10… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[6].prose` | You discounted each cash flow for its own wait and added, the outlay included. With $C_t$ paid at time $t$, $… | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[6].widget.options[right]` | key: $C_0$, the outlay, not discounted | correct | Recomputed; right under the convention the item states |
| `screens[6].widget.options[disc].why` | wrong option '$\dfrac{C_0}{1 + r}$': You discounted the outlay by a year. It is paid today, and $(1 + r)^0 = … | correct | Checked false under the item's premises; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[6].widget.options[none].why` | wrong option 'There is none: the outlay is left out': Leaving the outlay out gives the value of what comes ba… | correct | Checked false under the item's premises; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[6].hints[0]` | What is $(1 + r)^0$? | correct | Derivation or arithmetic step, checked |
| `screens[6].feedback.correct` | $\frac{C_0}{(1 + r)^0} = C_0$: the outlay counts in full. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[6].feedback.generic` | Not quite right. Put $t = 0$ into $\frac{C_t}{(1 + r)^t}$. | correct | Derivation or arithmetic step, checked |
| `screens[6].explain.text` | At $t = 0$ the factor is $(1 + r)^0 = 1$, so the term is $C_0$ itself. For the desk's model, $C_0 = -5000$. A… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[7].prose` | The desk wants NPV as a function. `flows[0]` is paid today, `flows[1]` in a year, and so on. The rate is a de… | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[7].widget.solution` | solution passes the hidden tests; starter fails; tests: 8 | correct | Solution and starter graded under Pyodide 0.27.7 (grade-all --code); natural wrong codings rejected |
| `screens[7].feedback.byKey.error` | Your code stopped with an error. Check that the `...` is replaced. | imprecise | Finding 5: Pyodide run: an unreplaced `...` is keyed test-1, never error; error is given only when the code does not load |
| `screens[7].hints[0]` | Each term is `cash` divided by $(1 + r)^t$. | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[1]` | `enumerate` gives `t = 0` for the first cash flow, so it is not discounted. | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[2]` | Replace `...` with `cash / (1 + rate) ** t`. | correct | Derivation or arithmetic step, checked |
| `screens[7].feedback.correct` | One line of discounting covers every stream. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[7].feedback.generic` | Some tests failed. Each term should be `cash / (1 + rate) ** t`. | correct | Derivation or arithmetic step, checked |
| `screens[7].explain.text` | The loop discounts each cash flow for its own wait, $t$ years. Because `t` starts at 0, the outlay is not dis… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[8].prose` | A bond costs £95.00. It pays £4.00 at the end of each year for 3 years, and £100.00 back with the last paymen… | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[8].widget.answer` | key 2.28 £: £2.28: $\tfrac{4}{1.05} + \tfrac{4}{1.05^2} + \tfrac{104}{1.05^3} - 95$. | correct | Recomputed; right under the convention the item states |
| `screens[8].feedback.byKey.undisc` | slip 17: You added the cash without discounting. Each payment is worth less the later it comes. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.no-cost` | slip 97.28: £97.28 is the value of the payments. Take away the £95.00 price. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.no-principal` | slip -84.11: You left out the £100.00 repaid in year 3. The last cash flow is £104.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].hints[0]` | The last cash flow is £104.00: a coupon plus the £100.00. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[1]` | The three payments are worth £97.28 today. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[2]` | $3.81 + 3.63 + 89.84 = 97.28$, and $97.28 - 95 = 2.28$. | correct | Derivation or arithmetic step, checked |
| `screens[8].feedback.correct` | NPV £2.28: buy, because the bond returns more than 5%. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[8].feedback.generic` | Not quite right. Discount £4.00, £4.00 and £104.00 for 1, 2 and 3 years, then take away £95.00. | correct | Derivation or arithmetic step, checked |
| `screens[8].explain.text` | The payments are worth £97.28 today, £2.28 more than the price. So buying at £95.00 earns more than 5%: its I… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[9].prose` | A trading desk can buy a faster data feed for £130,000.00 today. It should cut slippage by £50,000.00 a year … | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[9].canvas.state` | plotted values: {"y0": -130000, "y1": 50000, "y2": 50000, "y3": 50000} | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[9].widget.answer` | key 1215.8 £: £1,215.80: $50000 \times 2.624316 - 130000$. | correct | Recomputed; right under the convention the item states |
| `screens[9].feedback.byKey.undisc` | slip 20000: You added the cash without discounting. Three years of savings are worth less than £150,000.00 to… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[9].feedback.byKey.no-cost` | slip 131215.8: That is the value of the savings. Take away the £130,000.00 cost. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[9].feedback.byKey.at8` | slip -1145.15: That is the NPV at 8%. The firm's rate is 7%. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[9].hints[0]` | Discount each £50,000.00 for its own wait. | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[1]` | The three factors at 7% add to 2.624316. | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[2]` | $50000 \times 2.624316 = 131215.80$, minus £130,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[9].feedback.correct` | NPV £1,215.80: buy, but only just. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `screens[9].feedback.generic` | Not quite right. Discount each year's saving at 7%, add them, then take away the cost. | correct | Derivation or arithmetic step, checked |
| `screens[9].explain.text` | The savings are worth £131,215.80 today, so the NPV is £1,215.80. The IRR is 7.51%, so at 8% the answer flips… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[0].prose` | A project costs £200.00 today and pays £120.00 at the end of each of the next 2 years. The rate is 5%. | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[0].widget.answer` | key 23.13 £: £23.13: $\tfrac{120}{1.05} + \tfrac{120}{1.05^2} - 200$. | correct | Recomputed; right under the convention the item states |
| `quiz[0].feedback.byKey.undisc` | slip 40: You added the cash without discounting. Later payments are worth less today. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.byKey.no-cost` | slip 223.13: That is the value of the payments. Take away the £200.00 cost. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.correct` | £114.29 + £108.84 − £200.00 = £23.13. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[0].feedback.generic` | Not quite right. Discount both payments, add them, then take away £200.00. | correct | Derivation or arithmetic step, checked |
| `quiz[0].explain.text` | The payments are worth $114.29 + 108.84 = 223.13$ today. Take away the £200.00 outlay: NPV £23.13. Positive, … | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[1].prose` | An analyst reports project A's NPV as £50.00 at 9%, and project B's as £70.00 at 6%. Each is an outlay today … | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[1].widget.options[b].why` | wrong option 'B is better: its NPV is higher': You compared NPVs taken at different rates. B's NPV at 9% woul… | correct | Checked false under the item's premises; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[1].widget.options[a].why` | wrong option 'A is better: it was tested at the higher rate': The rate is not a score. A higher rate lowers t… | correct | Checked false under the item's premises; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[1].widget.options[right]` | key: Nothing yet: compute both at the same rate | correct | Recomputed; right under the convention the item states |
| `quiz[1].feedback.correct` | Rank projects only by NPVs at one shared rate. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[1].feedback.generic` | Not quite right. Ask whether the two NPVs are measured the same way. | correct | Derivation or arithmetic step, checked |
| `quiz[1].explain.text` | An NPV changes with the rate, so the two numbers are not comparable. Recompute both at the rate that fits the… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[2].prose` | A stream is −£500.00 today, then £200.00 at the end of each of the next 3 years. | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[2].widget.answer` | key 100 £: £100.00: $-500 + 200 + 200 + 200$. | correct | Recomputed; right under the convention the item states |
| `quiz[2].feedback.byKey.no-cost` | slip 600: You left out the −£500.00 paid today. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.correct` | At 0% the NPV is the plain sum. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[2].feedback.generic` | Not quite right. At 0% every factor is 1. | correct | Derivation or arithmetic step, checked |
| `quiz[2].explain.text` | At $r = 0$ every factor $(1 + 0)^{-t}$ is 1. So the NPV is the plain sum: $-500 + 600 = 100$. Any positive ra… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[3].prose` | A project has an outlay today and inflows later. Its NPV is £40.00 at 8% and −£25.00 at 10%. | correct | BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[3].widget.options[below].why` | wrong option 'Below 8%': Below 8% the NPV is even higher than £40.00, so it cannot be zero there. | correct | Checked false under the item's premises; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[3].widget.options[right]` | key: Between 8% and 10% | correct | Recomputed; right under the convention the item states |
| `quiz[3].widget.options[above].why` | wrong option 'Above 10%': Above 10% the NPV falls further below −£25.00. | correct | Checked false under the item's premises; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[3].widget.options[none].why` | wrong option 'It has none': The NPV changes sign between 8% and 10%, so it passes through zero. | correct | Checked false under the item's premises; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[3].feedback.correct` | The NPV changes sign between 8% and 10%. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |
| `quiz[3].feedback.generic` | Not quite right. The IRR is where the NPV crosses zero. | correct | Derivation or arithmetic step, checked |
| `quiz[3].explain.text` | For an outlay followed by inflows, NPV falls as the rate rises: here from £40.00 at 8% to −£25.00 at 10%. So … | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and ch. 5 §5.3 (NPV rule, IRR and its pitfalls); derivative of NPV in $r$ |

## l5-pricing-a-bond

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `summary.ideas[0]` | A bond's cash flows are fixed: a coupon each period and the face value at maturity. | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `summary.ideas[1]` | Its price is the present value of every cash flow at the yield. Half-yearly: halve the coupon and the yield, … | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `summary.ideas[2]` | Yield equal to the coupon rate gives par. Below it the bond trades at a premium; above it, at a discount. | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `summary.formula` | Bond price: P = \sum_{t=1}^{T} \frac{C}{(1+y)^t} + \frac{F}{(1+y)^T}; The coupons sum to $\tfrac{C}{y}\left(1… | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `summary.trap` | Discount the face value as well as the coupons, and discount at the yield, never the coupon rate. | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[0].prose` | You lend £100 by buying a bond. It pays you 4% of the £100, so £4, at the end of each year for 5 years. At th… | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[0].widget.answer` | key p1,p2,p3,p4,p5 | correct | Recomputed; right under the convention the item states |
| `screens[0].feedback.byKey.end-only` | You tapped only year 5, as if the bond were a deposit paid out at the end. It also pays £4 every year. | correct | Checked false under the item's premises; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[0].feedback.byKey.today` | You tapped today as well. Today you pay for the bond; it pays you nothing yet. | correct | Checked false under the item's premises; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[0].feedback.byKey.p0` | You tapped today. Today you pay for the bond; it pays you nothing yet. | correct | Checked false under the item's premises; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[0].hints[0]` | A coupon arrives at the end of every year, not only the last. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[1]` | Today, at 0, money goes the other way: you pay. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[2]` | Tap years 1, 2, 3, 4 and 5. | correct | Derivation or arithmetic step, checked |
| `screens[0].feedback.correct` | Five payments: £4 at years 1 to 4, and £104 at year 5. | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[0].feedback.generic` | Not quite right. The bond pays £4 every year end, and the £100 comes back with the last £4. | correct | Derivation or arithmetic step, checked |
| `screens[0].explain.text` | The bond pays £4 at the end of years 1 to 4. Year 5 brings £4 plus the £100: £104. Today is the only date whe… | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[1].prose` | Each bar is one payment, worth less today the later it comes. You could earn a rate elsewhere instead, so eac… | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[1].canvas.derive` | formulas: values.t1=4 / pow(1 + yld, 1); values.t2=4 / pow(1 + yld, 2); values.t3=4 / pow(1 + yld, 3); values… | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[1].widget.answer` | key 95.67 £: £95.67, to the penny (exact: 95.6705). | correct | Recomputed; right under the convention the item states |
| `screens[1].feedback.byKey.no-discount` | slip 120: That is the total at 0%: you added the payments without discounting them. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].feedback.byKey.par` | slip 100: £100 is what you lent, not what the payments are worth at 5%. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].feedback.byKey.last-only` | slip 81.49: That is the year-5 bar alone. Add the four coupon bars too. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].feedback.byKey.coupons-only` | slip 17.32: That is the five £4 coupons alone. Add the £100 face at year 5. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].hints[0]` | The caption adds the five bars for you. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[1]` | Drag the rate to 5.00%. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[2]` | At 5% the caption reads £95.67. | correct | Derivation or arithmetic step, checked |
| `screens[1].feedback.correct` | £95.67. Every payment is fixed, so a 5% rate makes each one worth less today. | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[1].feedback.generic` | Not quite right. Move the rate to 5% and read the total in the caption. | correct | Derivation or arithmetic step, checked |
| `screens[1].explain.text` | At 5% the bars are £3.81, £3.63, £3.46, £3.29 and £81.49. They add to £95.67. The year-5 payment is most of t… | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[2].prose` | You just priced a bond. The £100 is its **face value**, the £4 a year its **coupon**, and year 5 its **maturi… | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[2].canvas.derive` | formulas: values.t1=4 / pow(1 + yld, 1); values.t2=4 / pow(1 + yld, 2); values.t3=4 / pow(1 + yld, 3); values… | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[2].widget.rows[2][2]` | cell key 0.863838; Year 3's factor is $1/1.05^3$. You may have used a different power. | correct | Recomputed; right under the convention the item states |
| `screens[2].widget.rows[2][3]` | cell key 3.4554; | correct | Recomputed; right under the convention the item states |
| `screens[2].widget.rows[4][2]` | cell key 0.783526; | correct | Recomputed; right under the convention the item states |
| `screens[2].widget.rows[4][3]` | cell key 81.4867; Year 5 pays £104, the last coupon and the face value together. Multiply 104 by its factor. | correct | Recomputed; right under the convention the item states |
| `screens[2].widget.rows[5][3]` | cell key 95.6705; Add all five present values, including the large one at year 5. | correct | Recomputed; right under the convention the item states |
| `screens[2].hints[0]` | A discount factor is $1/1.05^t$: divide 1 by 1.05 three times for year 3. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[1]` | Year 5 pays £104: the last coupon and the face value together. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[2]` | $1/1.05^3 = 0.8638$, so $4 \times 0.8638 = 3.4554$. $1/1.05^5 = 0.7835$, so $104 \times 0.7835 = 81.49$. The … | correct | Derivation or arithmetic step, checked |
| `screens[2].feedback.correct` | The present values add to £95.67, the price you found on the bars. | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[2].feedback.generic` | Not quite right. Each discount factor is $1/1.05^t$, and each present value is the cash flow times it. | correct | Derivation or arithmetic step, checked |
| `screens[2].explain.text` | Year 3: $4 \times 0.8638 = 3.4554$. Year 5: $104 \times 0.7835 = 81.4867$. The five present values add to $95… | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[3].prose` | Most bonds, including UK government bonds, pay coupons half-yearly. This 4% bond pays £2 every six months, an… | imprecise | Finding 4: euro-area government bonds and most eurobonds pay yearly (Fabozzi ch. 1; Hull 10e §4.4 footnote on conventions); rest correct, recomputed |
| `screens[3].canvas.state` | plotted values: {"h1": 2, "h2": 2, "h3": 2, "h4": 2, "h5": 2, "h6": 2, "h7": 2, "h8": 2, "h9": 2, "h10": 102} | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[3].widget.answer` | key 95.62 £: £95.62 (exact: 95.6240). Discount ten £2 coupons and the £100 at 2.5% a period. | correct | Recomputed; right under the convention the item states |
| `screens[3].feedback.byKey.annual` | slip 95.67: That is the annual-coupon price. Here the coupons come half-yearly, so the schedule changes. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].feedback.byKey.full-coupon` | slip 113.13: You paid £4 every six months. Halve the coupon too: £2 a period. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].feedback.byKey.full-rate` | slip 76.83: You discounted at 5% every six months. Halve the yield too: 2.5% a period. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].feedback.byKey.five-periods` | slip 97.68: You halved the coupon and the yield but kept 5 periods. Five years of halves is 10 periods. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].hints[0]` | Halve the coupon and the yield, and double the number of periods. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[1]` | Ten periods of 2.5%: the last payment is $102/1.025^{10}$. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[2]` | $2 \times \dfrac{1 - 1.025^{-10}}{0.025} + \dfrac{100}{1.025^{10}} = 17.50 + 78.12 = 95.62$. | correct | Derivation or arithmetic step, checked |
| `screens[3].feedback.correct` | £95.62: ten coupons of £2 and the face value, each discounted at 2.5% a period. | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[3].feedback.generic` | Not quite right. Use £2 coupons, 2.5% a period and 10 periods. | correct | Derivation or arithmetic step, checked |
| `screens[3].explain.text` | With half-yearly coupons we use £2, 2.5% and 10 periods. The coupons are worth £17.50 and the face £78.12, so… | correct | Recomputed: £2 half-yearly at 2.5% equals £4.05 yearly at 5.0625% exactly (script) |
| `screens[4].prose` | Back to annual coupons. Move the yield and watch the total in the caption. A bond priced above £100 is at a *… | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[4].canvas.derive` | formulas: values.t1=4 / pow(1 + yld, 1); values.t2=4 / pow(1 + yld, 2); values.t3=4 / pow(1 + yld, 3); values… | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[4].widget.answer` | key 0.04 %: 4%, the coupon rate. | correct | Recomputed; right under the convention the item states |
| `screens[4].feedback.byKey.start` | slip 0.05: At 5% the price is £95.67, a discount. Lower the yield. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].feedback.byKey.zero` | slip 0.0: At 0% nothing is discounted and the price is £120. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].hints[0]` | At 5% the price is below £100. Which way must the yield move? | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[1]` | Lower yields raise the price. Try the coupon rate. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[2]` | At 4% the caption reads £100.00. | correct | Derivation or arithmetic step, checked |
| `screens[4].feedback.correct` | 4%. A bond whose yield equals its coupon rate is priced at par, its face value. | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[4].feedback.generic` | Not quite right. Move the yield until the caption reads £100.00. | correct | Derivation or arithmetic step, checked |
| `screens[4].explain.text` | At 4% each £4 coupon exactly pays the 4% you could earn on £100 elsewhere. So the bond is worth its face, £10… | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[5].prose` | A **zero-coupon bond** pays no coupons. This one pays only £100 at year 5. Its yield is 5%. | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[5].canvas.state` | plotted values: {"t1": 0, "t2": 0, "t3": 0, "t4": 0, "t5": 100} | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[5].widget.answer` | key 78.35 £: £78.35 (exact: 78.3526), $100/1.05^5$. | correct | Recomputed; right under the convention the item states |
| `screens[5].feedback.byKey.no-discount` | slip 100: You priced it at face value. The £100 is five years away, so it is worth less today. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.coupon-bond` | slip 95.67: That is the 4% coupon bond. This bond pays no coupons. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.with-coupon` | slip 81.49: You discounted £104. A zero pays £100 alone. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.simple` | slip 80: You divided by $1 + 5 \times 0.05$. Discounting compounds: divide by $1.05^5$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].hints[0]` | There is one payment to discount. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[1]` | It is five years away. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[2]` | $100/1.05^5 = 100 \times 0.7835 = 78.35$. | correct | Derivation or arithmetic step, checked |
| `screens[5].feedback.correct` | £78.35. A zero-coupon bond is one discounted cash flow. | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[5].feedback.generic` | Not quite right. Discount the single £100 back five years at 5%. | correct | Derivation or arithmetic step, checked |
| `screens[5].explain.text` | The only cash flow is £100 at year 5, so the price is $100/1.05^5 = \text{£}78.35$. The gap to £100 is the ze… | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[6].prose` | Four colleagues price the 5-year 4% bond at a 5% yield. They get £17.32, £100.00, £95.67 and £120.00. | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[6].canvas.state` | plotted values: {"t1": 4, "t2": 4, "t3": 4, "t4": 4, "t5": 104} | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[6].widget.options[coupons].why` | wrong option '£17.32': You discounted the £4 coupons and left out the £100 at year 5. The face value is a cas… | correct | Checked false under the item's premises; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[6].widget.options[coupon-rate].why` | wrong option '£100.00': You discounted at 4%, the coupon rate. The coupon sets the cash flows; the yield disc… | correct | Checked false under the item's premises; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[6].widget.options[right]` | key: £95.67 | correct | Recomputed; right under the convention the item states |
| `screens[6].widget.options[undiscounted].why` | wrong option '£120.00': You added the cash flows without discounting. Later money is worth less today. | correct | Checked false under the item's premises; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[6].feedback.byKey.coupons` | You discounted the coupons and dropped the £100 at year 5. It is most of the bond's value. | correct | Checked false under the item's premises; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[6].feedback.byKey.coupon-rate` | You discounted at the coupon rate. That gives £100 whatever the market yield is. | correct | Checked false under the item's premises; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[6].hints[0]` | Which rate discounts the cash flows: the coupon rate or the yield? | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[1]` | Every payment counts, including the £100 at year 5. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[2]` | Discount all five payments at 5%: the total is £95.67. | correct | Derivation or arithmetic step, checked |
| `screens[6].feedback.correct` | £95.67: all five payments, each discounted at the 5% yield. | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[6].feedback.generic` | Not quite right. Discount every cash flow, the face value included, at the yield. | correct | Derivation or arithmetic step, checked |
| `screens[6].explain.text` | The coupon rate fixes the cash flows at £4 a year; the 5% yield discounts them. The £100 at year 5 must be di… | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[7].prose` | You discounted each coupon $C$ and the face $F$ at the yield $y$: $$P = \sum_{t=1}^{T} \frac{C}{(1+y)^t} + \f… | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[7].widget.options[par].why` | wrong option '£100.00': You treated it as a par bond. Its coupon, 6%, is above its 5% yield, so it is at a pr… | correct | Checked false under the item's premises; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[7].widget.options[right]` | key: £102.72 | correct | Recomputed; right under the convention the item states |
| `screens[7].widget.options[swapped].why` | wrong option '£97.33': You swapped them: that is a 5% coupon at a 6% yield. | correct | Checked false under the item's premises; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[7].widget.options[undiscounted].why` | wrong option '£118.00': You added the cash flows without discounting. | correct | Checked false under the item's premises; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[7].feedback.correct` | £102.72: $\tfrac{6}{1.05} + \tfrac{6}{1.05^2} + \tfrac{106}{1.05^3}$, a premium. | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[7].feedback.generic` | Not quite right. Discount £6, £6 and £106 at 5%. | correct | Derivation or arithmetic step, checked |
| `screens[7].explain.text` | $\tfrac{6}{1.05} + \tfrac{6}{1.05^2} + \tfrac{106}{1.05^3} = 5.71 + 5.44 + 91.57 = 102.72$. The coupon beats … | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[8].prose` | Adding $T$ discounted coupons one by one is slow for a 30-year bond. The coupons form a geometric series. Wri… | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[8].widget.lines[s1]` | $P = C(v + v^2 + \dots + v^T) + F v^T$, writing each factor as a power of $v$ | correct | Derivation or arithmetic step, checked |
| `screens[8].widget.lines[s2]` | $v + v^2 + \dots + v^T = v\,\dfrac{1 - v^T}{1 - v}$, a geometric series with first term $v$ and ratio $v$ | correct | Derivation or arithmetic step, checked |
| `screens[8].widget.lines[s3]` | $1 - v = \dfrac{y}{1+y}$, so $\dfrac{v}{1 - v} = \dfrac{1}{y}$, by algebra on $v = \dfrac{1}{1+y}$ | correct | Derivation or arithmetic step, checked |
| `screens[8].widget.lines[s4]` | $P = \dfrac{C}{y}\left(1 - v^T\right) + F v^T$, substituting into the first line | correct | Derivation or arithmetic step, checked |
| `screens[8].widget.lines[s5]` | $P = 80(1 - 0.7835) + 78.35 = 17.32 + 78.35 = 95.67$, a check with $C = 4$, $y = 0.05$, $T = 5$ | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[0]` | Start by writing the price with powers of $v$. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[1]` | The sum of the coupons' factors is a geometric series. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[2]` | Sum the series, simplify $v/(1-v)$, substitute, then check with the 5-year bond. | correct | Derivation or arithmetic step, checked |
| `screens[8].feedback.correct` | The coupons are worth $\tfrac{C}{y}(1 - v^T)$, and the face adds $Fv^T$. | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[8].feedback.generic` | Not quite right. Write the price with $v$ first, then sum the series, then simplify. | correct | Derivation or arithmetic step, checked |
| `screens[8].explain.text` | The coupon factors $v, v^2, \dots, v^T$ form the geometric series from the Sequences and Series course. Summi… | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[9].prose` | A desk prices hundreds of bonds a day. Write the pricer once. Coupons are annual, `coupon` is a rate such as … | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[9].widget.solution` | solution passes the hidden tests; starter fails; tests: 8 | correct | Solution and starter graded under Pyodide 0.27.7 (grade-all --code); natural wrong codings rejected |
| `screens[9].feedback.byKey.error` | Your code stopped with an error. Check that both `...` are replaced. | imprecise | Finding 5: Pyodide run: an unreplaced `...` is keyed test-1, never error |
| `screens[9].feedback.byKey.test-1` | The 5-year 4% bond at a 5% yield should give 95.67. Discount every coupon and the face at `yld`: each coupon … | correct | Pyodide run: coupon-rate discounting, face left out, face undiscounted, coupon not times face all fail test 1 first |
| `screens[9].feedback.byKey.test-2` | A bond whose yield equals its coupon should price at par, 100. Check that both lines discount at `yld`, not a… | correct | Pyodide run: a fixed 1.05 in both lines, in the coupon line, or in the face line each fails test 2 first |
| `screens[9].feedback.byKey.test-3` | A 10-year zero-coupon bond at 5% should give $100/1.05^{10} = 61.39$. Check that the face is discounted over … | correct | Pyodide run: face over a fixed 5 years fails test 3 first |
| `screens[9].hints[0]` | Each year pays `face * coupon`, discounted by `(1 + yld) ** t`. | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[1]` | After the loop, add the face value, discounted over `years` years. | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[2]` | Inside the loop: `face * coupon / (1 + yld) ** t`. After it: `face / (1 + yld) ** years`. | correct | Derivation or arithmetic step, checked |
| `screens[9].feedback.correct` | The loop discounts each coupon, and the last line adds the face value. | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[9].feedback.generic` | Some tests failed. Discount every coupon at the yield, then add the discounted face value. | correct | Derivation or arithmetic step, checked |
| `screens[9].explain.text` | The loop adds $C/(1+y)^t$ for each year, and the face adds $F/(1+y)^T$. Two tests are the checks from this le… | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[10].prose` | UK government bonds, **gilts**, are quoted per £100 of face value, called nominal. A 4% gilt is quoted at 98.… | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[10].canvas.params.rows` | table: [["Quote per £100 nominal", "98.50"], ["Coupon", "4% a year, paid half-yearly"], ["You buy", "£10,000 … | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[10].widget.answer` | key 9950 £: £9,950: £9,850 for the bond plus £100 of accrued interest. | correct | Recomputed; right under the convention the item states |
| `screens[10].feedback.byKey.clean` | slip 9850: That is the quoted price alone. You also owe the seller the interest earned since the last coupon. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[10].feedback.byKey.per-pound` | slip 985000: You multiplied 98.50 by 10,000. The quote is per £100, so multiply by 100. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[10].feedback.byKey.whole-coupon` | slip 10050: You added a whole half-year coupon. Only half the period has passed, so add half of it. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[10].feedback.byKey.full-year` | slip 10250: You added a whole year's coupon. Only a quarter of a year's interest has built up. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[10].hints[0]` | The quote is per £100, so scale it to £10,000 first. | correct | Derivation or arithmetic step, checked |
| `screens[10].hints[1]` | A full half-year coupon on £10,000 is £200. Half the period has passed. | correct | Derivation or arithmetic step, checked |
| `screens[10].hints[2]` | $98.50 \times 100 = 9{,}850$, plus half of £200, £100: £9,950. | correct | Derivation or arithmetic step, checked |
| `screens[10].feedback.correct` | £9,950: the quoted price plus half a coupon. | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `screens[10].feedback.generic` | Not quite right. Scale the quote to £10,000, then add the coupon earned since the last payment. | correct | Derivation or arithmetic step, checked |
| `screens[10].explain.text` | The quote, the **clean price**, gives $98.50 \times 100 = \text{£}9{,}850$. Half a period has passed, so the … | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `quiz[0].prose` | A 3-year bond pays a 5% annual coupon on £100 face. Its yield is 5%. | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `quiz[0].widget.options[right]` | key: £100.00 | correct | Recomputed; right under the convention the item states |
| `quiz[0].widget.options[undiscounted].why` | wrong option '£115.00': You added the cash flows without discounting them. | correct | Checked false under the item's premises; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `quiz[0].widget.options[principal].why` | wrong option '£86.38': You discounted the £100 and dropped the coupons. | correct | Checked false under the item's premises; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `quiz[0].widget.options[coupons].why` | wrong option '£13.62': You discounted the coupons and dropped the £100. | correct | Checked false under the item's premises; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `quiz[0].feedback.correct` | £100.00. The yield equals the coupon rate, so the bond is at par. | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `quiz[0].feedback.generic` | Not quite right. Compare the yield with the coupon rate. | correct | Derivation or arithmetic step, checked |
| `quiz[0].explain.text` | Each £5 coupon pays exactly the 5% you could earn elsewhere on £100. So the bond is worth its face value. Che… | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `quiz[1].prose` | A 2-year bond pays a 6% annual coupon on £100 face. Its yield is 4%. | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `quiz[1].widget.answer` | key 103.77 £: £103.77 (exact: 103.7722). | correct | Recomputed; right under the convention the item states |
| `quiz[1].feedback.byKey.undiscounted` | slip 112: You added £6 and £106 without discounting. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[1].feedback.byKey.coupon-rate` | slip 100: You discounted at the 6% coupon rate. Discount at the 4% yield. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[1].feedback.byKey.principal` | slip 92.46: You discounted the £100 and dropped both coupons. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[1].feedback.correct` | £103.77, a premium: the coupon beats the yield. | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `quiz[1].feedback.generic` | Not quite right. Discount £6 at year 1 and £106 at year 2, both at 4%. | correct | Derivation or arithmetic step, checked |
| `quiz[1].explain.text` | $\tfrac{6}{1.04} + \tfrac{106}{1.04^2} = 5.77 + 98.00 = 103.77$. The 6% coupon is above the 4% yield, so the … | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `quiz[2].prose` | A 10-year zero-coupon bond pays £100 at maturity. Its yield is 5%. | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `quiz[2].widget.answer` | key 61.39 £: £61.39 (exact: 61.3913). | correct | Recomputed; right under the convention the item states |
| `quiz[2].feedback.byKey.no-discount` | slip 100: You priced it at face. The £100 is ten years away. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.byKey.simple` | slip 66.67: You divided by $1 + 10 \times 0.05$. Interest compounds, so divide by $1.05^{10}$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.byKey.ten-off` | slip 50: You took 5% of £100 off each year. Discounting divides by 1.05 each year instead. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.correct` | £61.39: one cash flow, $100/1.05^{10}$. | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `quiz[2].feedback.generic` | Not quite right. Divide £100 by $1.05^{10}$. | correct | Derivation or arithmetic step, checked |
| `quiz[2].explain.text` | A zero-coupon bond is a single cash flow. Its price is $100/1.05^{10} = 100/1.6289 = \text{£}61.39$. | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `quiz[3].prose` | A 2-year bond pays a 6% coupon on £100 face, half-yearly. Its yield is 4% a year, compounded half-yearly. | correct | Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `quiz[3].widget.answer` | key 103.81 £: £103.81 (exact: 103.8077). | correct | Recomputed; right under the convention the item states |
| `quiz[3].feedback.byKey.annual` | slip 103.77: That treats the coupons as annual. Here they are £3 every six months. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[3].feedback.byKey.full-coupon` | slip 115.23: You paid £6 every six months. Halve the coupon too. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[3].feedback.byKey.two-periods` | slip 101.94: You halved the coupon and the yield but kept 2 periods. Two years of halves is 4 periods. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[3].feedback.correct` | £103.81: four coupons of £3 and the face, each at 2% a period. | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |
| `quiz[3].feedback.generic` | Not quite right. Use £3 coupons, 2% a period and 4 periods. | correct | Derivation or arithmetic step, checked |
| `quiz[3].explain.text` | Halve the coupon and yield and double the periods: £3, 2%, 4 periods. $3 \times \tfrac{1 - 1.02^{-4}}{0.02} +… | correct | Recomputed in the concepts script or by hand; Fabozzi, Bond Markets, ch. 2 (pricing); Hull 10e §4.4; BKM ch. 14 §14.1–14.2 (accrued interest) |

## l6-yield

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `summary.ideas[0]` | The yield to maturity is the one rate that makes the present value of the cash flows equal the price. Bisecti… | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `summary.ideas[1]` | The cash flows are fixed, so a higher yield discounts them harder: price falls as yield rises, along a curve … | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `summary.ideas[2]` | Modified duration is the slope per pound: $\Delta P \approx -D\,P\,\Delta y$. Longer maturity and lower coupo… | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `summary.formula` | Price change from duration: \Delta P \approx -D\,P\,\Delta y; Good for small moves; for large ones the curve'… | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `summary.trap` | A higher yield is not good news for a holder: it means the bond's price has fallen. | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[0].prose` | The 5-year 4% bond was priced at £95.67 when its yield was 5%. Today it trades at £92.00. Its cash flows have… | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[0].canvas.state` | plotted values: {"t1": 4, "t2": 4, "t3": 4, "t4": 4, "t5": 104} | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[0].widget.options[above]` | key: Above 5% | correct | Recomputed; right under the convention the item states |
| `screens[0].widget.options[below].why` | wrong option 'Below 5%': You read a lower price as a lower yield. Paying less for the same cash flows earns y… | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[0].widget.options[same].why` | wrong option 'Still 5%': You treated the yield as fixed when the bond was issued. The yield is set by today's… | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[0].widget.options[coupon].why` | wrong option 'Exactly 4%, the coupon rate': The coupon rate is fixed at 4%; the yield is not. At 4% the price… | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[0].feedback.byKey.below` | You read a lower price as a lower yield. Paying less for the same cash flows earns you more on each pound. | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[0].hints[0]` | At 5% the cash flows are worth £95.67. You now pay less for them. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[1]` | Paying less for the same money later means a higher return. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[2]` | A lower price means a higher yield: above 5%. | correct | Derivation or arithmetic step, checked |
| `screens[0].feedback.correct` | Above 5%. Paying less for the same cash flows is a higher return. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[0].feedback.generic` | Not quite right. You pay less today for exactly the same payments later. | correct | Derivation or arithmetic step, checked |
| `screens[0].explain.text` | At 5% the cash flows are worth £95.67, more than the £92.00 asked. Only a higher rate discounts them down to … | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[1].prose` | Each bar is one cash flow's value today. Move the yield from 5% to 6% and watch the bars. | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[1].canvas.derive` | formulas: values.t1=4 / pow(1 + yld, 1); values.t2=4 / pow(1 + yld, 2); values.t3=4 / pow(1 + yld, 3); values… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[1].widget.answer` | key 77.71 £: £77.71 (exact: 77.7148), $104/1.06^5$. | correct | Recomputed; right under the convention the item states |
| `screens[1].feedback.byKey.at-five` | slip 81.49: That is its value at 5%. Move the yield to 6%. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].feedback.byKey.undiscounted` | slip 104: That is the payment itself. Its value today is the payment discounted at 6%. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].feedback.byKey.price` | slip 91.58: That is the whole bond at 6%. You want the Year 5 bar alone. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].hints[0]` | Set the yield to 6% and read the Year 5 bar. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[1]` | The bar is $104/1.06^5$. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[2]` | $1.06^5 = 1.3382$, and $104/1.3382 = 77.71$. | correct | Derivation or arithmetic step, checked |
| `screens[1].feedback.correct` | £77.71, down from £81.49 at 5%. The same £104, divided by a bigger number. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[1].feedback.generic` | Not quite right. Move the yield to 6% and read the Year 5 bar. | correct | Derivation or arithmetic step, checked |
| `screens[1].explain.text` | The cash flows are fixed, so a higher yield divides each one by a larger number. Every bar shrinks, the far o… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[2].prose` | The curve is the bond's price at every yield. Move the yield and watch the price. The dashed line is £92.00. | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[2].canvas.derive` | formulas: C.x=yld * 100; C.y=4/(1+yld) + 4/pow(1+yld,2) + 4/pow(1+yld,3) + 4/pow(1+yld,4) + 104/pow(1+yld,5) | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[2].widget.answer` | key 0.059 %: 5.9% (exact: 5.894%). | correct | Recomputed; right under the convention the item states |
| `screens[2].feedback.byKey.same` | slip 0.05: At 5% the price is £95.67. Raise the yield to bring the price down. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].feedback.byKey.current` | slip 0.0435: That is the coupon over the price, $4/92$. The yield also counts the £100 at maturity. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].feedback.byKey.lower` | slip 0.041: You moved the yield down, and the price went up. Move it the other way. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].hints[0]` | The price must fall from £95.67 to £92.00. Which way does the yield go? | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[1]` | Watch the dot cross the dashed line. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[2]` | Between 5.85% (£92.18) and 5.90% (£91.97): about 5.9%. | correct | Derivation or arithmetic step, checked |
| `screens[2].feedback.correct` | About 5.9%. The price fell, so the yield rose. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[2].feedback.generic` | Not quite right. Move the yield until the caption reads about £92.00. | correct | Derivation or arithmetic step, checked |
| `screens[2].explain.text` | At 5.85% the price is £92.18, and at 5.90% it is £91.97. So £92.00 needs a yield of about 5.89%. Along the cu… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[3].prose` | You found the bond's **yield to maturity**: the one rate that makes the present value equal the price. Softwa… | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[3].canvas.params.functions` | curves: 4/(1+x/100) + 4/(1+x/100)^2 + 4/(1+x/100)^3 + 4/(1+x/100)^4 + 104/(1+x/100)^5 | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[3].widget.rows[1][1]` | cell key 6; At 6% the price, £91.58, is below £92.00. The yield must be below 6%, so 6% is the new high. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[1][2]` | cell key 5; | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[2][0]` | cell key 5; At 5% the price, £95.67, is above £92.00. The yield must be above 5%, so 5% is the new low. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[2][2]` | cell key 5.5; | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[3][0]` | cell key 5.5; At 5.5% the price, £93.59, is still above £92.00. So 5.5% is the new low. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[3][2]` | cell key 5.75; | correct | Recomputed; right under the convention the item states |
| `screens[3].hints[0]` | If the price at the midpoint is below £92.00, the yield is below the midpoint. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[1]` | At 6% the price is £91.58, too low, so 6% becomes the high end. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[2]` | Row 2: 4 to 6, midpoint 5. At £95.67 the price is too high, so row 3 is 5 to 6, midpoint 5.5. Then 5.5 to 6, … | correct | Derivation or arithmetic step, checked |
| `screens[3].feedback.correct` | Each row halves the interval. After five rows the yield is pinned between 5.875% and 6%. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[3].feedback.generic` | Not quite right. Compare each midpoint's price with £92.00 to decide which half to keep. | correct | Derivation or arithmetic step, checked |
| `screens[3].explain.text` | A price above £92.00 means the yield is higher than the midpoint, so the low end moves up. A price below mean… | correct | $4/2^{20}=3.8\times10^{-6}$ points; Newton run from 4%, 6% and 8% reaches it in three steps (script) |
| `screens[4].prose` | In Limits and Derivatives you found this bond's **modified duration**, $D = 4.40$, from the tangent's slope. … | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[4].canvas.params.functions` | curves: 4/(1+x/100) + 4/(1+x/100)^2 + 4/(1+x/100)^3 + 4/(1+x/100)^4 + 104/(1+x/100)^5; 95.6705 - 4.2098*(x - … | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[4].widget.answer` | key 4.21 £: £4.21: $4.40 \times 95.67 \times 0.01$. The true fall is £4.10. | correct | Recomputed; right under the convention the item states |
| `screens[4].feedback.byKey.no-price` | slip 4.4: You took the duration as pounds. It is a percentage: 4.40% of £95.67. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].feedback.byKey.pct` | slip 0.044: That is the fraction of the price lost, 4.4%. Multiply by £95.67 for pounds. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].feedback.byKey.true` | slip 4.1: That is the true fall, from the curve. The tangent gives a little more. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].hints[0]` | Duration is a percentage of the price per unit of yield. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[1]` | $\Delta y = 0.01$ and $P = 95.67$. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[2]` | $4.40 \times 95.67 \times 0.01 = 4.21$. | correct | Derivation or arithmetic step, checked |
| `screens[4].feedback.correct` | £4.21. The true fall, from the curve, is £4.10. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[4].feedback.generic` | Not quite right. Multiply $D$, the price and $\Delta y$. | correct | Derivation or arithmetic step, checked |
| `screens[4].explain.text` | The tangent says $4.40 \times 95.67 \times 0.01 = \text{£}4.21$. The curve bends up, so the true fall is smal… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[5].prose` | Two 4% bonds, one with 2 years left and one with 10. Both yield 5%, and yields rise to 6%. | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[5].canvas.params.functions` | curves: 4/(1+x/100) + 104/(1+x/100)^2; 400/x*(1 - (1+x/100)^(-10)) + 100/(1+x/100)^10 | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[5].widget.rows[0][3]` | cell key -1.84; For the 2-year bond, divide $96.33 - 98.14$ by 98.14. Prices fell, so the change is negative. | correct | Recomputed; right under the convention the item states |
| `screens[5].widget.rows[1][3]` | cell key -7.58; For the 10-year bond, divide $85.28 - 92.28$ by 92.28. Prices fell, so the change is negative. | correct | Recomputed; right under the convention the item states |
| `screens[5].hints[0]` | Change is (new − old) / old, as a percentage. Prices fell, so it is negative. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[1]` | 2-year: $(96.33 - 98.14)/98.14$. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[2]` | 2-year: $-1.81/98.14 = -1.84\%$. 10-year: $-7.00/92.28 = -7.58\%$. | correct | Derivation or arithmetic step, checked |
| `screens[5].feedback.correct` | The 10-year bond loses about four times as much: 7.58% against 1.84%. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[5].feedback.generic` | Not quite right. Divide each change in price by the price at 5%. | correct | Derivation or arithmetic step, checked |
| `screens[5].explain.text` | The 2-year bond falls 1.84% and the 10-year 7.58%. The 10-year's cash flows are further away, so a higher yie… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[6].prose` | A zero-coupon bond's value all arrives at maturity $T$. So its **Macaulay duration**, the average time of its… | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[6].canvas.params.functions` | curves: 100/(1+x/100)^5; 4/(1+x/100) + 4/(1+x/100)^2 + 4/(1+x/100)^3 + 4/(1+x/100)^4 + 104/(1+x/100)^5 | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[6].widget.answer` | key 4.76 : 4.76: $5/1.05 = 4.7619$. | correct | Recomputed; right under the convention the item states |
| `screens[6].feedback.byKey.macaulay` | slip 5: 5 is the Macaulay duration. Divide by $1 + y$ for the modified duration. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[6].feedback.byKey.coupon` | slip 4.4: 4.40 is the 4% coupon bond. The zero has no early cash flows to pull its duration down. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[6].feedback.byKey.times` | slip 5.25: You multiplied by 1.05. Divide instead. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[6].hints[0]` | Its Macaulay duration is its maturity, 5 years. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[1]` | Modified duration is Macaulay duration divided by $1 + y$. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[2]` | $5/1.05 = 4.76$. | correct | Derivation or arithmetic step, checked |
| `screens[6].feedback.correct` | 4.76, more than the coupon bond's 4.40. With no coupons, all the value waits until year 5. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[6].feedback.generic` | Not quite right. Divide the maturity by 1.05. | correct | Derivation or arithmetic step, checked |
| `screens[6].explain.text` | $D = 5/1.05 = 4.76$, against 4.40 for the 4% bond of the same maturity. Coupons return money early and shorte… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[7].prose` | You bought the 5-year 4% bond for £95.67 at a 5% yield. Overnight, yields rise to 6%. A friend says you are b… | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[7].canvas.params.functions` | curves: 4/(1+x/100) + 4/(1+x/100)^2 + 4/(1+x/100)^3 + 4/(1+x/100)^4 + 104/(1+x/100)^5 | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[7].widget.options[better].why` | wrong option 'You are better off: it now yields 6%': You read the higher yield as a gain to you. The 6% goes … | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[7].widget.options[right]` | key: It is worth £4.10 less: £91.58 | correct | Recomputed; right under the convention the item states |
| `screens[7].widget.options[fixed].why` | wrong option 'Nothing: its coupons and face value are fixed': The cash flows are fixed, but their value today… | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[7].widget.options[gain].why` | wrong option 'It is worth £4.33 more: £100.00': That is a fall in yields, to 4%. Yields rose, so the price fe… | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[7].feedback.byKey.better` | You read the higher yield as a gain to you. The 6% goes to whoever buys at today's lower price. | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[7].feedback.byKey.fixed` | The cash flows are fixed, but their value today is not. At 6% they are worth £4.10 less. | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[7].hints[0]` | Read the price at 6% on the curve. | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[1]` | Your bond's cash flows are now discounted at 6%. | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[2]` | At 6% the price is £91.58, down £4.10. | correct | Derivation or arithmetic step, checked |
| `screens[7].feedback.correct` | £4.10 down. A new buyer earns 6% from £91.58; you have already lost the difference. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[7].feedback.generic` | Not quite right. Price your bond's fixed cash flows at the new 6% yield. | correct | Derivation or arithmetic step, checked |
| `screens[7].explain.text` | Your cash flows are fixed, so a 6% yield prices them at £91.58. You have lost £4.10 today. Held to maturity, … | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[8].prose` | Quotes often show the **current yield** too: the annual coupon divided by the price. It ignores the gain or l… | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[8].canvas.params.rows` | table: [["Annual coupon", "£4.00"], ["Price", "£95.67"], ["Face value at maturity", "£100.00"], ["Yield to ma… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[8].widget.answer` | key 0.0418 %: 4.18%: $4/95.67 = 0.0418$. | correct | Recomputed; right under the convention the item states |
| `screens[8].feedback.byKey.ytm` | slip 0.05: That is the yield to maturity, which also counts the £4.33 rise to £100 at the end. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.coupon` | slip 0.04: That is the coupon over the face value. Divide by the price instead. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.inverse` | slip 0.0453: That is the £4.33 pull to £100 over the price. The current yield uses the coupon. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].hints[0]` | Divide the coupon by the price. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[1]` | Use £4.00 and £95.67. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[2]` | $4/95.67 = 0.0418$, or 4.18%. | correct | Derivation or arithmetic step, checked |
| `screens[8].feedback.correct` | 4.18%, below the 5% yield to maturity. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[8].feedback.generic` | Not quite right. Divide the £4 coupon by the £95.67 price. | correct | Derivation or arithmetic step, checked |
| `screens[8].explain.text` | The current yield is $4/95.67 = 4.18\%$. The yield to maturity, 5%, also counts the £4.33 the bond gains on i… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[9].prose` | Price is a falling curve in the yield, and it bends upwards. For a small move, $$\Delta P \approx -D\,P\,\Del… | correct | BKM §16.1 rules 2–4, checked numerically for coupons 0–12 and T 2–30 at 5%; the maturity rule can fail only for deep-discount bonds, outside the item's cases |
| `screens[9].widget.options[zero10]` | key: A 10-year zero-coupon bond | correct | Recomputed; right under the convention the item states |
| `screens[9].widget.options[coupon10].why` | wrong option 'A 10-year bond with an 8% coupon': Its large coupons return money early, which shortens its dur… | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[9].widget.options[short].why` | wrong option 'A 2-year bond with a 4% coupon': Its cash flows are close, so they are discounted over few year… | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[9].widget.options[zero2].why` | wrong option 'A 2-year zero-coupon bond': No coupons helps, but 2 years is short. Its duration is under 2. | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[9].feedback.correct` | The 10-year zero: the longest maturity and no coupons. Its modified duration is $10/1.05 = 9.52$. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[9].feedback.generic` | Not quite right. Look for the latest cash flows. | correct | Derivation or arithmetic step, checked |
| `screens[9].explain.text` | The 10-year zero has all its value at year 10, so $D = 10/1.05 = 9.52$. The 8% 10-year bond's coupons pull it… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[10].prose` | You run a £10 million bond portfolio with a modified duration of 4.4. The central bank surprises the market, … | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[10].canvas.params.rows` | table: [["Market value", "£10,000,000"], ["Modified duration", "4.4"], ["Yield change", "+1.00%"]] | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[10].widget.answer` | key 440000 £: About £440,000: $4.4 \times 10{,}000{,}000 \times 0.01$. | correct | Recomputed; right under the convention the item states |
| `screens[10].feedback.byKey.tenth` | slip 44000: You used a 0.1% move. One percentage point is $\Delta y = 0.01$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[10].feedback.byKey.no-pct` | slip 44000000: You multiplied by 1 instead of 0.01. A 1% move is $\Delta y = 0.01$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[10].feedback.byKey.one-pct` | slip 100000: You took 1% of the value. Duration multiplies that: 4.4 times as much. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[10].hints[0]` | Use $\Delta P \approx -D\,P\,\Delta y$. | correct | Derivation or arithmetic step, checked |
| `screens[10].hints[1]` | $\Delta y = 0.01$ and $P = \text{£}10{,}000{,}000$. | correct | Derivation or arithmetic step, checked |
| `screens[10].hints[2]` | $4.4 \times 10{,}000{,}000 \times 0.01 = 440{,}000$. | correct | Derivation or arithmetic step, checked |
| `screens[10].feedback.correct` | About £440,000, or 4.4% of the portfolio. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[10].feedback.generic` | Not quite right. Multiply the duration, the value and the yield change as a decimal. | correct | Derivation or arithmetic step, checked |
| `screens[10].explain.text` | $4.4 \times \text{£}10{,}000{,}000 \times 0.01 = \text{£}440{,}000$. Convexity makes the true loss a little s… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[11].prose` | In 2022 central banks raised interest rates fast to fight inflation, and bond yields jumped. A broad index of… | correct | Bloomberg US Aggregate total return 2022: −13.0%, the worst calendar year since its 1976 inception |
| `screens[11].widget.options[right]` | key: Higher yields discounted the same fixed cash flows harder, so prices fell | correct | Recomputed; right under the convention the item states |
| `screens[11].widget.options[default].why` | wrong option 'Many of the bonds defaulted and stopped paying': You looked for missed payments. Almost every b… | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[11].widget.options[coupons].why` | wrong option 'The bonds cut their coupons when rates rose': A bond's coupon is fixed when it is issued. Risin… | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[11].widget.options[better].why` | wrong option 'Nothing real: higher yields made the bonds better': You read the higher yield as good news for … | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[11].hints[0]` | What happens to a bond's price when its yield rises? | correct | Derivation or arithmetic step, checked |
| `screens[11].hints[1]` | Duration links a yield change to a price change. | correct | Derivation or arithmetic step, checked |
| `screens[11].hints[2]` | Fixed cash flows discounted at higher yields are worth less: prices fell. | correct | Derivation or arithmetic step, checked |
| `screens[11].feedback.correct` | Yields up, prices down. Funds holding long bonds, with high durations, fell most. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `screens[11].feedback.generic` | Not quite right. Think about what a rise in yield does to a fixed cash flow's value today. | correct | Derivation or arithmetic step, checked |
| `screens[11].explain.text` | Rising yields cut the present value of every fixed coupon and face value. With durations of about six years, … | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `quiz[0].prose` | A bond's yield falls from 6% to 5%. Nothing else changes. | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `quiz[0].widget.options[right]` | key: It rises | correct | Recomputed; right under the convention the item states |
| `quiz[0].widget.options[falls].why` | wrong option 'It falls': You moved price and yield together. A lower yield discounts the same cash flows less… | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `quiz[0].widget.options[same].why` | wrong option 'It stays the same: the coupons are fixed': The cash flows are fixed, but their value today depe… | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `quiz[0].feedback.correct` | It rises. Price and yield move opposite ways. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `quiz[0].feedback.generic` | Not quite right. A lower yield divides each cash flow by a smaller number. | correct | Derivation or arithmetic step, checked |
| `quiz[0].explain.text` | Each cash flow is divided by $(1+y)^t$. A smaller $y$ makes every divisor smaller, so every present value, an… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `quiz[1].prose` | A bond is priced at £102.00 with a modified duration of 7.0. Its yield rises by 0.5 percentage points. | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `quiz[1].widget.answer` | key 3.57 £: £3.57: $7.0 \times 102 \times 0.005$. | correct | Recomputed; right under the convention the item states |
| `quiz[1].feedback.byKey.no-price` | slip 3.5: That is the percentage, 3.5. Multiply it by the £102 price. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[1].feedback.byKey.full-pct` | slip 7.14: You used a 1-point move. Half a point is $\Delta y = 0.005$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[1].feedback.byKey.fraction` | slip 0.035: That is the fraction of the price, 0.035. Multiply by £102. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[1].feedback.correct` | £3.57, or 3.5% of the price. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `quiz[1].feedback.generic` | Not quite right. Multiply duration, price and $\Delta y = 0.005$. | correct | Derivation or arithmetic step, checked |
| `quiz[1].explain.text` | $\Delta P \approx -D\,P\,\Delta y = -7.0 \times 102 \times 0.005 = -3.57$. The price falls about £3.57. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `quiz[2].prose` | A bond pays a £6 annual coupon and is priced at £105.00. Its yield to maturity is 4.9%. | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `quiz[2].widget.answer` | key 0.0571 %: 5.71%: $6/105$. | correct | Recomputed; right under the convention the item states |
| `quiz[2].feedback.byKey.coupon` | slip 0.06: That is the coupon over the face value. Divide by the £105 price. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.byKey.ytm` | slip 0.049: That is the yield to maturity. The current yield is the coupon over the price. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.correct` | 5.71%. Here it is above the yield to maturity, because the bond loses £5 on its way to £100. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `quiz[2].feedback.generic` | Not quite right. Divide the coupon by the price. | correct | Derivation or arithmetic step, checked |
| `quiz[2].explain.text` | $6/105 = 5.71\%$. A premium bond falls to £100 by maturity, so its yield to maturity, 4.9%, is below its curr… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `quiz[3].prose` | The 5-year 4% bond, at £95.67 with modified duration 4.40, sees yields jump from 5% to 8%. Duration alone pre… | correct | Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `quiz[3].widget.options[right]` | key: Smaller, about 12.2%, because the price curve bends up | correct | Recomputed; right under the convention the item states |
| `quiz[3].widget.options[same].why` | wrong option 'The same, 13.2%: duration gives the change': You treated the curve as a straight line. Over 3 p… | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `quiz[3].widget.options[bigger].why` | wrong option 'Bigger, because large moves hurt more than duration says': You expected the bend to add to the … | correct | Checked false under the item's premises; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `quiz[3].feedback.correct` | The true price is £84.03, a fall of 12.2%. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |
| `quiz[3].feedback.generic` | Not quite right. Does the curve lie above or below its tangent? | correct | Derivation or arithmetic step, checked |
| `quiz[3].explain.text` | The true price at 8% is £84.03, a 12.2% fall; the tangent gives £83.04. The curve bends up, so a straight lin… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 3–4 (yield measures, duration, convexity); Hull 10e §4.8–4.9; BKM ch. 16 §16.1 |

## l7-shares

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `summary.ideas[0]` | A share is a claim on a slice of a company's profits and assets. Losses stop at what you paid. | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `summary.ideas[1]` | Market cap is price times shares; dividend yield is $D/P$; P/E is price over earnings per share. Compare P/E,… | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `summary.ideas[2]` | A share is worth its future payouts discounted: $P = D/(r - g)$ for steady growth with $g < r$. A higher requ… | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `summary.formula` | Dividend discount model: P = \dfrac{D}{r - g}; $D$ is next year's dividend. Valid only for $g < r$. | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `summary.trap` | A £2 share is not cheaper than a £50 share. Compare price to earnings. | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[0].prose` | A company is split into 10 million equal shares. You own 100,000 of them. This year it made a profit of £5 mi… | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[0].canvas.params.rows` | table: [["Shares in issue", "10,000,000"], ["Your shares", "100,000"], ["Profit this year", "£5,000,000"]] | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[0].widget.answer` | key 50000 £: £50,000: 1% of the shares, so 1% of the profit. | correct | Recomputed; right under the convention the item states |
| `screens[0].feedback.byKey.one-share` | slip 0.5: That is the profit for one share, £0.50. You hold 100,000 of them. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.tenth` | slip 500000: You took 10%. 100,000 out of 10 million is 1%. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.hundredth` | slip 5000: You took 0.1%. 100,000 out of 10 million is 1%. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].hints[0]` | What fraction of all the shares do you own? | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[1]` | $100{,}000 / 10{,}000{,}000 = 1\%$. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[2]` | 1% of £5,000,000 is £50,000. | correct | Derivation or arithmetic step, checked |
| `screens[0].feedback.correct` | £50,000. You own 1% of the company, so 1% of its profit is yours. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[0].feedback.generic` | Not quite right. Find your fraction of the shares, then take that fraction of the profit. | correct | Derivation or arithmetic step, checked |
| `screens[0].explain.text` | You hold $100{,}000 / 10{,}000{,}000 = 1\%$ of the shares. A share is a claim on a slice of the company's pro… | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[1].prose` | The board decides how much of the £5 million to pay out to shareholders. The rest stays in the company to fun… | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[1].canvas.derive` | formulas: values.paid=5 * payout; values.kept=5 * (1 - payout) | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[1].widget.answer` | key 0.2 £: £0.20: £2 million over 10 million shares. | correct | Recomputed; right under the convention the item states |
| `screens[1].feedback.byKey.eps` | slip 0.5: That is the whole profit per share, £0.50. Only 40% of it is paid out. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].feedback.byKey.kept` | slip 0.3: That is the part kept, per share. You want the part paid out. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].feedback.byKey.millions` | slip 2: £2 million is the total paid. Divide it among 10 million shares. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].hints[0]` | At 40%, £2 million is paid out in total. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[1]` | Share it equally among 10 million shares. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[2]` | $2{,}000{,}000 / 10{,}000{,}000 = \text{£}0.20$. | correct | Derivation or arithmetic step, checked |
| `screens[1].feedback.correct` | £0.20 a share. That payment is the **dividend**. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[1].feedback.generic` | Not quite right. Divide the amount paid out by the number of shares. | correct | Derivation or arithmetic step, checked |
| `screens[1].explain.text` | 40% of £5 million is £2 million, so each share gets a **dividend** of £0.20. The £3 million kept is **retaine… | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[2].prose` | Price times shares is the **market capitalisation**: what the market says all the shares are worth. Dividend … | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[2].canvas.params.rows` | table: [["Share price", "£5.20"], ["Shares in issue", "400 million"], ["Dividend per share", "£0.13"], ["Earn… | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[2].widget.rows[0][1]` | cell key 2080; Market cap is the share price times the shares in issue: $5.20 \times 400$. | correct | Recomputed; right under the convention the item states |
| `screens[2].widget.rows[1][1]` | cell key 2.5; Dividend yield is the dividend divided by the price: $0.13/5.20$, as a percentage. | correct | Recomputed; right under the convention the item states |
| `screens[2].widget.rows[2][1]` | cell key 13; P/E is the price divided by the earnings per share: $5.20/0.40$. | correct | Recomputed; right under the convention the item states |
| `screens[2].hints[0]` | Each measure is one multiplication or division. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[1]` | Market cap is $5.20 \times 400$ million. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[2]` | $5.20 \times 400 = 2{,}080$. $0.13/5.20 = 2.5\%$. $5.20/0.40 = 13$. | correct | Derivation or arithmetic step, checked |
| `screens[2].feedback.correct` | £2,080 million, 2.5% and 13. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[2].feedback.generic` | Not quite right. Market cap is price times shares; the other two divide by the price or into it. | correct | Derivation or arithmetic step, checked |
| `screens[2].explain.text` | $5.20 \times 400\text{m} = \text{£}2{,}080\text{m}$. The dividend yield is $0.13/5.20 = 2.5\%$. A P/E of 13 m… | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[3].prose` | You paid £2,080 for 400 shares. The company collapses, owing its lenders £50 million more than everything it … | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[3].canvas.params.rows` | table: [["You paid", "£2,080"], ["Your shares", "400 of 400 million"], ["Debts above assets", "£50,000,000"]] | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[3].widget.answer` | key 2080 £: £2,080, what you paid. | correct | Recomputed; right under the convention the item states |
| `screens[3].feedback.byKey.share-of-debt` | slip 2130: You added your share of the shortfall, £50. Shareholders do not owe the company's debts. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].feedback.byKey.debt` | slip 50000000: The £50 million is owed by the company, not by its owners. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].feedback.byKey.nothing` | slip 0: Shareholders are paid last. With debts above assets, the shares are worth nothing, so you lose what y… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].hints[0]` | Can the lenders come to you for the shortfall? | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[1]` | Shareholders are not liable for the company's debts. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[2]` | You lose the £2,080 you paid, and no more. | correct | Derivation or arithmetic step, checked |
| `screens[3].feedback.correct` | £2,080. Your shares can fall to zero, but no further. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[3].feedback.generic` | Not quite right. The company's debts are not yours. | correct | Derivation or arithmetic step, checked |
| `screens[3].explain.text` | This is **limited liability**: an owner's loss is capped at what they paid for the shares. Lenders are paid f… | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[4].prose` | Two companies in the same industry. A friend wants share A because it costs only £2.00. | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[4].canvas.params.rows` | table: [["Price", "£2.00", "£50.00"], ["Earnings per share", "£0.10", "£5.00"]] | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[4].widget.options[a].why` | wrong option 'Share A': You compared the prices per share. A share of A is a much smaller slice: compare pric… | correct | Checked false under the item's premises; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[4].widget.options[right]` | key: Share B | correct | Recomputed; right under the convention the item states |
| `screens[4].widget.options[same].why` | wrong option 'Neither: both are fairly priced': You may have assumed the market prices both the same. Their P… | correct | Checked false under the item's premises; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[4].widget.options[cant].why` | wrong option 'They cannot be compared': They can: P/E puts both on the same basis, pounds paid per pound of p… | correct | Checked false under the item's premises; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[4].feedback.byKey.a` | You compared the prices per share. A share of A is a much smaller slice of its company: its P/E is 20. | correct | Checked false under the item's premises; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[4].hints[0]` | A low price can just mean a small slice of the company. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[1]` | Divide each price by its earnings per share. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[2]` | A: $2.00/0.10 = 20$. B: $50.00/5.00 = 10$. Lower P/E is cheaper. | correct | Derivation or arithmetic step, checked |
| `screens[4].feedback.correct` | Share B: a P/E of 10 against 20. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[4].feedback.generic` | Not quite right. Compare price to earnings, not price alone. | correct | Derivation or arithmetic step, checked |
| `screens[4].explain.text` | A costs $2.00/0.10 = 20$ times earnings, B only $50.00/5.00 = 10$ times. The price of one share says nothing … | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[5].prose` | A share will pay £2.00 next year, growing 3% a year after that. Investors want an 8% return. The curve adds u… | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[5].canvas.derive` | formulas: C.x=N; C.y=40*(1 - pow(1.03/1.08, N)) | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[5].widget.answer` | key 40 £: £40.00. | correct | Recomputed; right under the convention the item states |
| `screens[5].feedback.byKey.no-growth` | slip 25: That is $2/0.08$, which ignores the 3% growth. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.ten` | slip 15.1: That counts only the first 10 dividends. They carry on for ever. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.plus` | slip 18.18: That is $2/(0.08 + 0.03)$. Growth makes the share worth more, not less. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].hints[0]` | Move $N$ far to the right. Does the total keep growing? | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[1]` | Each new dividend adds less than the one before: its value shrinks by $1.03/1.08$. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[2]` | The total levels off at £40.00. | correct | Derivation or arithmetic step, checked |
| `screens[5].feedback.correct` | £40.00. Infinitely many dividends, but a finite value. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[5].feedback.generic` | Not quite right. Push $N$ to 150 and see where the total levels off. | correct | Derivation or arithmetic step, checked |
| `screens[5].explain.text` | Each dividend is worth $1.03/1.08 = 0.954$ times the one before it, today. The values shrink, so the total se… | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[6].prose` | Call next year's dividend $D$, its growth rate $g$ and the required return $r$. Each dividend is $1 + g$ time… | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[6].widget.lines[s1]` | $P = \dfrac{D}{1+r} + \dfrac{D(1+g)}{(1+r)^2} + \dfrac{D(1+g)^2}{(1+r)^3} + \dots$, discounting every dividend | correct | Derivation or arithmetic step, checked |
| `screens[6].widget.lines[s2]` | A geometric series with first term $a = \dfrac{D}{1+r}$ and ratio $q = \dfrac{1+g}{1+r}$, dividing each term … | correct | Derivation or arithmetic step, checked |
| `screens[6].widget.lines[s3]` | When $g < r$, $0 < q < 1$, so the series converges to $\dfrac{a}{1 - q}$ | correct | Derivation or arithmetic step, checked |
| `screens[6].widget.lines[s4]` | $1 - q = \dfrac{(1+r) - (1+g)}{1+r} = \dfrac{r - g}{1+r}$, over a common denominator | correct | Derivation or arithmetic step, checked |
| `screens[6].widget.lines[s5]` | $P = \dfrac{D}{1+r} \cdot \dfrac{1+r}{r - g} = \dfrac{D}{r - g}$, dividing $a$ by $1 - q$ | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[0]` | Write the price as a sum first. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[1]` | Find the ratio between neighbouring terms. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[2]` | Sum, ratio, convergence, simplify $1 - q$, divide. | correct | Derivation or arithmetic step, checked |
| `screens[6].feedback.correct` | $P = D/(r - g)$: here $2.00/(0.08 - 0.03) = \text{£}40.00$. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[6].feedback.generic` | Not quite right. Start from the sum, name its ratio, then use the infinite geometric sum. | correct | Derivation or arithmetic step, checked |
| `screens[6].explain.text` | This is the infinite geometric sum from the Sequences and Series course: $a/(1 - q)$ with $q = (1+g)/(1+r)$. … | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[7].prose` | Nothing about the company changes, but interest rates rise and investors now want 10% a year from this share.… | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[7].canvas.params.functions` | curves: 200/(x - 3) | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[7].widget.answer` | key 28.57 £: £28.57: $2.00/(0.10 - 0.03)$. | correct | Recomputed; right under the convention the item states |
| `screens[7].feedback.byKey.same` | slip 40: The dividends are unchanged, but they are now discounted at 10%. The price falls. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].feedback.byKey.no-growth` | slip 20: That is $2/0.10$, which ignores the 3% growth. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].feedback.byKey.plus` | slip 15.38: That adds $g$ to $r$. Growth is subtracted: $r - g$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].hints[0]` | Only $r$ changes in $P = D/(r - g)$. | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[1]` | $r - g = 0.10 - 0.03 = 0.07$. | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[2]` | $2.00/0.07 = 28.57$. | correct | Derivation or arithmetic step, checked |
| `screens[7].feedback.correct` | £28.57, down 29%, with no change in the company. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[7].feedback.generic` | Not quite right. Use $D = 2.00$, $r = 0.10$ and $g = 0.03$. | correct | Derivation or arithmetic step, checked |
| `screens[7].explain.text` | $2.00/0.07 = \text{£}28.57$, a 29% fall. A share price moves with the cash flows investors expect and the rat… | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[8].prose` | Move the growth rate $g$ towards the 8% required return. The curve is $P = 2/(r - g)$, drawn for $r > g$. | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[8].canvas.derive` | formulas: | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[8].widget.options[right]` | key: It gives no answer: the dividends' values never shrink, so the sum has no limit | correct | Recomputed; right under the convention the item states |
| `screens[8].widget.options[zero].why` | wrong option 'Nothing, because $r - g = 0$': You read dividing by zero as giving zero. The terms do not shrin… | correct | Checked false under the item's premises; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[8].widget.options[buy].why` | wrong option 'An infinite amount, so it is worth buying at any price': You trusted the formula outside its ra… | correct | Checked false under the item's premises; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[8].widget.options[ignore].why` | wrong option '£25.00, using $2/0.08$': You dropped the growth. With $g = r$ every term is $2/1.08$, the same … | correct | Checked false under the item's premises; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[8].hints[0]` | At $g = r$, what is the ratio $q = (1+g)/(1+r)$? | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[1]` | $q = 1$, so every dividend is worth the same today. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[2]` | A sum of infinitely many equal terms has no limit: the model breaks. | correct | Derivation or arithmetic step, checked |
| `screens[8].feedback.correct` | The model needs $g < r$. At $g \ge r$ the series diverges. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[8].feedback.generic` | Not quite right. Find the ratio between neighbouring terms when $g = r$. | correct | Derivation or arithmetic step, checked |
| `screens[8].explain.text` | With $g = r$ the ratio is $q = 1$: every dividend is worth £1.85 today, for ever. The sum has no limit, and f… | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[9].prose` | Market cap $= P \times N$, dividend yield $= D/P$, P/E $= P/\text{EPS}$. A share is worth its future payouts,… | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[9].widget.options[right]` | key: The value today of the cash it will return later, as dividends or buybacks | correct | Recomputed; right under the convention the item states |
| `screens[9].widget.options[zero].why` | wrong option 'Nothing: with $D = 0$ the model gives $P = 0$': You set every future payout to zero. Cash can c… | correct | Checked false under the item's premises; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[9].widget.options[book].why` | wrong option 'Exactly its assets minus its debts': That is the book value. The price also counts the profit t… | correct | Checked false under the item's premises; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[9].feedback.correct` | Payouts can start later or take another form. The share is worth them, discounted. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[9].feedback.generic` | Not quite right. Ask what cash the owners will get, and when. | correct | Derivation or arithmetic step, checked |
| `screens[9].explain.text` | A **buyback** returns cash by buying shares from those who want to sell. A young firm reinvesting at high ret… | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[10].prose` | An analyst screens a UK retailer. Its shares trade at £3.45. Fill in the measures a screen shows. | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[10].canvas.params.rows` | table: [["Share price", "£3.45"], ["Shares in issue", "1,200 million"], ["Profit after tax", "£276 million"],… | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[10].widget.rows[0][1]` | cell key 4140; Market cap is $3.45 \times 1{,}200$ million. | correct | Recomputed; right under the convention the item states |
| `screens[10].widget.rows[1][1]` | cell key 3.0; Dividend yield is total dividends over market cap: $124.2/4{,}140$. | correct | Recomputed; right under the convention the item states |
| `screens[10].widget.rows[2][1]` | cell key 15; P/E is market cap over total profit: $4{,}140/276$. | correct | Recomputed; right under the convention the item states |
| `screens[10].hints[0]` | Totals work as well as per-share figures: divide total by total. | correct | Derivation or arithmetic step, checked |
| `screens[10].hints[1]` | Market cap is $3.45 \times 1{,}200$ million. | correct | Derivation or arithmetic step, checked |
| `screens[10].hints[2]` | Market cap £4,140m. Dividend yield $124.2/4{,}140 = 3.0\%$. P/E $4{,}140/276 = 15$. | correct | Derivation or arithmetic step, checked |
| `screens[10].feedback.correct` | £4,140 million, 3.0% and 15. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[10].feedback.generic` | Not quite right. Find the market cap first; the other two divide by it or into it. | correct | Derivation or arithmetic step, checked |
| `screens[10].explain.text` | Market cap is $3.45 \times 1{,}200\text{m} = \text{£}4{,}140\text{m}$. Total over total, the dividend yield i… | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[11].prose` | A company's shares trade at £5.00. To raise cash it offers a **rights issue**: one new share at £3.00 for eve… | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[11].canvas.params.rows` | table: [["Four old shares at £5.00", "£20.00"], ["Cash paid for one new share", "£3.00"], ["Shares afterwards… | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[11].widget.answer` | key 4.6 £: £4.60: $(20 + 3)/5$. | correct | Recomputed; right under the convention the item states |
| `screens[11].feedback.byKey.unchanged` | slip 5: New shares sold at £3.00 bring in less than £5.00 each, so the average price falls. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[11].feedback.byKey.average` | slip 4: You averaged £5.00 and £3.00. There are four old shares for each new one. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[11].hints[0]` | No value is created or lost: add up what the holder has. | correct | Derivation or arithmetic step, checked |
| `screens[11].hints[1]` | Four shares worth £20.00, plus £3.00 of new cash, now spread over 5 shares. | correct | Derivation or arithmetic step, checked |
| `screens[11].hints[2]` | $(20 + 3)/5 = \text{£}4.60$. | correct | Derivation or arithmetic step, checked |
| `screens[11].feedback.correct` | £4.60. The holder's total, £23.00, is unchanged by the issue. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `screens[11].feedback.generic` | Not quite right. Add the old shares' value and the new cash, then divide by 5. | correct | Derivation or arithmetic step, checked |
| `screens[11].explain.text` | Before: £20.00 of shares plus £3.00 of cash, £23.00. After: 5 shares worth £23.00, so £4.60 each. A share spl… | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `quiz[0].prose` | A company has 250 million shares in issue, trading at £8.40. | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `quiz[0].widget.answer` | key 2.1 billion: £2.1 billion. | correct | Recomputed; right under the convention the item states |
| `quiz[0].feedback.byKey.millions` | slip 2100: That is the answer in millions. Give it in billions: 2,100 million is 2.1 billion. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.byKey.per-share` | slip 8.4: That is one share's price. Multiply by 250 million shares. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.correct` | £2.1 billion. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `quiz[0].feedback.generic` | Not quite right. Multiply the price by the number of shares. | correct | Derivation or arithmetic step, checked |
| `quiz[0].explain.text` | $8.40 \times 250\text{m} = \text{£}2{,}100\text{m} = \text{£}2.1\text{bn}$. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `quiz[1].prose` | You hold 150 shares at £80.00. The company does a 2-for-1 share split. | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `quiz[1].widget.options[right]` | key: £12,000: 300 shares at £40.00 | correct | Recomputed; right under the convention the item states |
| `quiz[1].widget.options[double].why` | wrong option '£24,000: 300 shares at £80.00': You doubled the shares but kept the price. Each new share is ha… | correct | Checked false under the item's premises; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `quiz[1].widget.options[half].why` | wrong option '£6,000: 150 shares at £40.00': You halved the price but kept 150 shares. You now hold 300. | correct | Checked false under the item's premises; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `quiz[1].feedback.correct` | £12,000, as before. A split slices the same company more thinly. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `quiz[1].feedback.generic` | Not quite right. A split changes the count and the price, not the value. | correct | Derivation or arithmetic step, checked |
| `quiz[1].explain.text` | Each share becomes two, so you hold 300, and each is worth half, £40.00. $300 \times 40 = \text{£}12{,}000 = … | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `quiz[2].prose` | A share will pay a £1.50 dividend next year, growing 4% a year for ever. Investors require 9% a year. | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `quiz[2].widget.answer` | key 30 £: £30.00: $1.50/(0.09 - 0.04)$. | correct | Recomputed; right under the convention the item states |
| `quiz[2].feedback.byKey.no-growth` | slip 16.67: That is $1.50/0.09$, ignoring growth. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.byKey.plus` | slip 11.54: That adds $g$ to $r$. Subtract it. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.correct` | £30.00. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `quiz[2].feedback.generic` | Not quite right. Use $P = D/(r - g)$. | correct | Derivation or arithmetic step, checked |
| `quiz[2].explain.text` | $P = 1.50/(0.09 - 0.04) = 1.50/0.05 = \text{£}30.00$. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `quiz[3].prose` | A share trades at £40.00 and pays a dividend of £1.20 a year. Its earnings per share are £2.50. | correct | BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `quiz[3].widget.answer` | key 0.03 %: 3%: $1.20/40$. | correct | Recomputed; right under the convention the item states |
| `quiz[3].feedback.byKey.earnings` | slip 0.0625: That is earnings over price, $2.50/40$. Use the dividend. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[3].feedback.byKey.payout` | slip 0.48: That is dividend over earnings, the payout ratio. Divide by the price. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[3].feedback.correct` | 3%. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |
| `quiz[3].feedback.generic` | Not quite right. Divide the dividend by the price. | correct | Derivation or arithmetic step, checked |
| `quiz[3].explain.text` | $1.20/40.00 = 0.03$, a 3% dividend yield. The P/E is $40/2.50 = 16$. | correct | Recomputed in the concepts script or by hand; BKM ch. 18 §18.3–18.4 (dividend discount model, P/E); BMA ch. 4 |

## l8-measuring-returns

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `summary.ideas[0]` | Total return counts income: $R = (P_1 + D - P_0)/P_0$. | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `summary.ideas[1]` | Returns compound: multiply growth factors $1 + R$, and annualise with $(1 + R)^{1/T} - 1$. Log returns add. | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `summary.ideas[2]` | Excess return is the return above the risk-free rate; the Sharpe ratio divides it by volatility. | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `summary.formula` | Annualised return: (1 + R)^{1/T} - 1; $R$ is the total return over $T$ years. Never divide $R$ by $T$, or mul… | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `summary.trap` | +50% then −50% is −25%, not 0%. Averaging yearly returns overstates growth. | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[0].prose` | You bought a share for £50.00. Halfway through the year it paid a dividend of £1.50, and the price dropped as… | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[0].canvas.state` | plotted values: [[50, 50.8, 51.5, 50.9, 52.2, 53.0, 51.6, 51.9, 52.4, 51.8, 52.7, 53.4, 53.0]] | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[0].widget.answer` | key 0.09 %: 9%: $(53.00 + 1.50 - 50.00)/50.00$. | correct | Recomputed; right under the convention the item states |
| `screens[0].feedback.byKey.price-only` | slip 0.06: That is the price change alone. The £1.50 dividend is part of what you made. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.div-only` | slip 0.03: That is the dividend alone. The price also rose £3.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.pounds` | slip 0.045: You typed £4.50 as a percentage. Divide £4.50 by the £50.00 you paid. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].hints[0]` | You gained from the price and from the cash paid to you. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[1]` | Price gain £3.00, dividend £1.50. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[2]` | $(3.00 + 1.50)/50.00 = 0.09$. | correct | Derivation or arithmetic step, checked |
| `screens[0].feedback.correct` | 9%: £4.50 on £50.00. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[0].feedback.generic` | Not quite right. Add the price gain and the dividend, then divide by what you paid. | correct | Derivation or arithmetic step, checked |
| `screens[0].explain.text` | You gained £3.00 on the price and received £1.50 in cash. That is £4.50 on £50.00, or 9%. Leaving out the div… | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[1].prose` | £100 is invested for three years. Each slider sets one year's return. Watch the bars, and compare the total w… | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[1].canvas.derive` | formulas: values.y0=100; values.y1=100 * (1 + r1); values.y2=100 * (1 + r1) * (1 + r2); values.y3=100 * (1 + … | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[1].widget.answer` | key 0.134 %: 13.4%: $1.20 \times 0.90 \times 1.05 = 1.134$. | correct | Recomputed; right under the convention the item states |
| `screens[1].feedback.byKey.added` | slip 0.15: You added the three returns. The 10% loss came off £120, not £100, so returns compound. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].feedback.byKey.average` | slip 0.05: That is the average of the three. You want the total over all three years. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[1].hints[0]` | Each year's return applies to the value at the start of that year. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[1]` | Multiply the growth factors: $1.20 \times 0.90 \times 1.05$. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[2]` | $1.20 \times 0.90 = 1.08$, and $1.08 \times 1.05 = 1.134$: 13.4%. | correct | Derivation or arithmetic step, checked |
| `screens[1].feedback.correct` | 13.4%, not the 15% the returns add to. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[1].feedback.generic` | Not quite right. Set the three sliders and read the total in the caption. | correct | Derivation or arithmetic step, checked |
| `screens[1].explain.text` | £100 becomes £120, then £108, then £113.40: a total of 13.4%. The returns add to 15% because adding ignores t… | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[2].prose` | You just found a **total return**: price change plus income, over the starting price. $$R = \frac{P_1 + D - P… | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[2].canvas.state` | plotted values: [[40.0, 43.0, 40.42, 44.06]] | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[2].widget.rows[1][4]` | cell key -3.0; Year 2 lost £2.58 on the price but paid £1.29: $(40.42 + 1.29 - 43.00)/43.00 = -3\%$. | correct | Recomputed; right under the convention the item states |
| `screens[2].widget.rows[2][4]` | cell key 12.0; Year 3: $(44.06 + 1.21 - 40.42)/40.42$. Divide by the start price, 40.42. | correct | Recomputed; right under the convention the item states |
| `screens[2].hints[0]` | Year 2: the price fell, but a dividend was paid. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[1]` | Year 2: $(40.42 + 1.29 - 43.00)/43.00$. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[2]` | Year 2: $-1.29/43.00 = -3.00\%$. Year 3: $4.85/40.42 = 12.00\%$. | correct | Derivation or arithmetic step, checked |
| `screens[2].feedback.correct` | −3.00% and 12.00%. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[2].feedback.generic` | Not quite right. Add the dividend to the end price, subtract the start price, divide by the start price. | correct | Derivation or arithmetic step, checked |
| `screens[2].explain.text` | Year 2: the price fell £2.58, the dividend paid £1.29, so $-1.29/43.00 = -3.00\%$. Year 3: $(3.64 + 1.21)/40.… | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[3].prose` | Back to £100 growing to £113.40 over three years. The dashed line grows at the same rate every year and ends … | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[3].canvas.state` | plotted values: [[100, 120, 108, 113.4], [100.0, 104.28, 108.74, 113.4]] | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[3].widget.answer` | key 0.0428 %: 4.28%: $1.134^{1/3} - 1$. | correct | Recomputed; right under the convention the item states |
| `screens[3].feedback.byKey.divide` | slip 0.0447: You divided 13.4% by 3. That ignores compounding: $1.0447^3 = 1.140$, too much. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].feedback.byKey.average` | slip 0.05: That is the arithmetic average of the three returns. It overstates the steady rate. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].feedback.byKey.total` | slip 0.134: | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].hints[0]` | A steady rate $a$ for three years multiplies by $(1 + a)^3$. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[1]` | Solve $(1 + a)^3 = 1.134$. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[2]` | $a = 1.134^{1/3} - 1 = 0.0428$. | correct | Derivation or arithmetic step, checked |
| `screens[3].feedback.correct` | 4.28% a year: $1.0428^3 = 1.134$. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[3].feedback.generic` | Not quite right. Take the cube root of 1.134, then subtract 1. | correct | Derivation or arithmetic step, checked |
| `screens[3].explain.text` | We need $(1 + a)^3 = 1.134$, so $a = 1.134^{1/3} - 1 = 4.28\%$. Over $T$ years the annualised return is $(1 +… | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[4].prose` | The **log return** of a year is $\ln(1 + R)$. In the Series and Approximation course you saw it is close to $… | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[4].canvas.state` | plotted values: [[100, 120, 108, 113.4]] | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[4].widget.answer` | key 0.1258 : 0.1258: $\ln 1.2 + \ln 0.9 + \ln 1.05 = \ln 1.134$. | correct | Recomputed; right under the convention the item states |
| `screens[4].feedback.byKey.simple` | slip 0.15: You added the simple returns. Take $\ln(1 + R)$ of each first. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].feedback.byKey.pct` | slip 12.58: Give it as a decimal: 0.1258, not 12.58. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].hints[0]` | Find $\ln 1.20$, $\ln 0.90$ and $\ln 1.05$. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[1]` | They are 0.1823, −0.1054 and 0.0488. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[2]` | $0.1823 - 0.1054 + 0.0488 = 0.1258$. | correct | Derivation or arithmetic step, checked |
| `screens[4].feedback.correct` | 0.1258, which is $\ln 1.134$: log returns add up to the log of the total. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[4].feedback.generic` | Not quite right. Take the natural log of each $1 + R$, then add. | correct | Derivation or arithmetic step, checked |
| `screens[4].explain.text` | $\ln 1.2 + \ln 0.9 + \ln 1.05 = \ln(1.2 \times 0.9 \times 1.05) = \ln 1.134 = 0.1258$. Logs turn the product … | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[5].prose` | A fund makes +50% one year and −50% the next. Its brochure says it averaged 0% a year. | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[5].canvas.state` | plotted values: [[100, 150, 75]] | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[5].widget.options[flat].why` | wrong option 'It is still £100: the average return is 0%': You averaged the yearly returns. The 50% loss came… | correct | Checked false under the item's premises; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[5].widget.options[right]` | key: It fell to £75: a total return of −25% | correct | Recomputed; right under the convention the item states |
| `screens[5].widget.options[zero].why` | wrong option 'It fell to £0: the losses wiped it out': A −50% year halves the value; it takes −100% to reach … | correct | Checked false under the item's premises; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[5].widget.options[up].why` | wrong option 'It grew to £125': You applied the −50% to the original £100 and kept the +50% on top. Each year… | wrong | Finding 2: the named mistake gives £100 ($100-50+50$), not the option's £125. Script check fails |
| `screens[5].feedback.byKey.flat` | You averaged the yearly returns. The 50% loss came off £150, so it removed £75. | correct | Checked false under the item's premises; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[5].hints[0]` | Apply each year to the value at the start of that year. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[1]` | £100 grows to £150. Then it halves. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[2]` | $100 \times 1.5 \times 0.5 = 75$: −25% in total. | correct | Derivation or arithmetic step, checked |
| `screens[5].feedback.correct` | £75: $1.5 \times 0.5 = 0.75$. The annualised return is −13.4% a year. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[5].feedback.generic` | Not quite right. Multiply the growth factors, $1.5$ and $0.5$. | correct | Derivation or arithmetic step, checked |
| `screens[5].explain.text` | £100 grows to £150, and halving £150 leaves £75: a total of −25%. The arithmetic average, 0%, would only fit … | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[6].prose` | A fund gains exactly 0.75% every month for a year. Its factsheet must quote a yearly return. | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[6].canvas.state` | plotted values: [[100.0, 100.75, 101.51, 102.27, 103.03, 103.81, 104.59, 105.37, 106.16, 106.96, 107.76, 108.… | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[6].widget.answer` | key 0.0938 %: 9.38%: $1.0075^{12} - 1$. | correct | Recomputed; right under the convention the item states |
| `screens[6].feedback.byKey.times12` | slip 0.09: You multiplied the monthly return by 12. That ignores the return earned on earlier returns. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[6].feedback.byKey.simple` | slip 0.0075: That is one month. Compound it over twelve. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[6].hints[0]` | Each month's 0.75% applies to a slightly larger sum. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[1]` | Twelve growth factors of 1.0075. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[2]` | $1.0075^{12} = 1.0938$: 9.38%. | correct | Derivation or arithmetic step, checked |
| `screens[6].feedback.correct` | 9.38%, more than $12 \times 0.75\% = 9\%$. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[6].feedback.generic` | Not quite right. Compound the monthly factor twelve times. | correct | Derivation or arithmetic step, checked |
| `screens[6].explain.text` | $1.0075^{12} - 1 = 9.38\%$. Multiplying by 12 gives 9%, missing the interest on interest. The gap grows with … | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[7].prose` | Growth factors multiply: over $T$ years the total is $1 + R = (1 + R_1)(1 + R_2)\cdots(1 + R_T)$, and $$\text… | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[7].widget.options[right]` | key: −100%: everything is lost | correct | Recomputed; right under the convention the item states |
| `screens[7].widget.options[sum].why` | wrong option '+240%, the four returns added': You added the returns. The −100% year multiplies the value by 0. | correct | Checked false under the item's premises; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[7].widget.options[avg].why` | wrong option '+60% a year on average': You averaged them. A factor of 0 makes the product 0, whatever else ha… | correct | Checked false under the item's premises; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[7].widget.options[recover].why` | wrong option '+200%: the last year recovers it': 200% of nothing is nothing. Once the value is £0, no return … | correct | Checked false under the item's premises; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[7].feedback.correct` | −100%. One factor of 0 makes the whole product 0. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[7].feedback.generic` | Not quite right. Multiply the four growth factors. | correct | Derivation or arithmetic step, checked |
| `screens[7].explain.text` | The factors are 1.8, 1.6, 0 and 3, and their product is 0. A return of −100% is total loss, and nothing compo… | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[8].prose` | Cash in a bank earns the **risk-free rate**, here 4% a year. The **excess return** is what a fund earns above… | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[8].canvas.params.rows` | table: [["Average yearly return", "9%"], ["Risk-free rate", "4%"], ["Volatility", "12%"]] | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[8].widget.answer` | key 0.4167 : 0.42: $(0.09 - 0.04)/0.12$. | correct | Recomputed; right under the convention the item states |
| `screens[8].feedback.byKey.no-rf` | slip 0.75: You divided the whole 9% by the volatility. Subtract the 4% risk-free rate first. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.excess` | slip 0.05: That is the excess return, 5%. Divide it by the 12% volatility. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.inverse` | slip 2.4: You divided the volatility by the excess return. It is the other way up. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].hints[0]` | Subtract the risk-free rate first. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[1]` | The excess return is $9\% - 4\% = 5\%$. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[2]` | $0.05/0.12 = 0.42$. | correct | Derivation or arithmetic step, checked |
| `screens[8].feedback.correct` | 0.42: 5% of excess return for 12% of volatility. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[8].feedback.generic` | Not quite right. Divide the excess return by the volatility. | correct | Derivation or arithmetic step, checked |
| `screens[8].explain.text` | $(0.09 - 0.04)/0.12 = 0.42$. It measures excess return per unit of risk. The Distributions and Limit Theorems… | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[9].prose` | A fund's factsheet shows yearly returns of 12%, −8% and 15%. You check its headline numbers. | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[9].canvas.state` | plotted values: [[100, 112, 103.04, 118.5]] | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[9].widget.rows[0][1]` | cell key 18.5; Multiply the growth factors 1.12, 0.92 and 1.15, then subtract 1. | correct | Recomputed; right under the convention the item states |
| `screens[9].widget.rows[1][1]` | cell key 5.82; Take the cube root of 1.18496, then subtract 1. | correct | Recomputed; right under the convention the item states |
| `screens[9].widget.rows[2][1]` | cell key 6.33; Add 12, −8 and 15, and divide by 3. | correct | Recomputed; right under the convention the item states |
| `screens[9].hints[0]` | Multiply the growth factors for the total. | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[1]` | $1.12 \times 0.92 \times 1.15 = 1.18496$. | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[2]` | Total 18.50%. Annualised $1.18496^{1/3} - 1 = 5.82\%$. Average $(12 - 8 + 15)/3 = 6.33\%$. | correct | Derivation or arithmetic step, checked |
| `screens[9].feedback.correct` | 18.50% in total, 5.82% a year annualised, and a 6.33% average. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[9].feedback.generic` | Not quite right. Compound the returns for the total, then take the cube root of the growth factor. | correct | Derivation or arithmetic step, checked |
| `screens[9].explain.text` | $1.12 \times 0.92 \times 1.15 = 1.18496$, an 18.50% total. Annualised, $1.18496^{1/3} - 1 = 5.82\%$. A factsh… | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[10].prose` | A backtest produces a list of yearly returns as decimals. Write the function the report calls for its headlin… | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[10].widget.solution` | solution passes the hidden tests; starter fails; tests: 8 | correct | Solution and starter graded under Pyodide 0.27.7 (grade-all --code); natural wrong codings rejected |
| `screens[10].feedback.byKey.error` | Your code stopped with an error. Check that both `...` are replaced. | imprecise | Finding 5: Pyodide run: an unreplaced `...` is keyed test-1, never error |
| `screens[10].feedback.byKey.test-1` | For 12%, −8% and 15% the answer is $1.18496^{1/3} - 1 = 0.0582$, not the 6.33% average. Compound, then take t… | correct | Pyodide run: mean, total/T, total, and root without −1 all fail test 1 first |
| `screens[10].feedback.byKey.test-2` | For +50% then −50% the answer is $0.75^{1/2} - 1 = -0.134$. Check that the root uses `len(returns)`, here 2. | correct | Pyodide run: root fixed at 3 (two codings) fails test 2 first |
| `screens[10].feedback.byKey.test-6` | A −100% year makes the growth 0, so the answer is −1. `math.log(0)` fails there: multiply the growth factors … | correct | Pyodide run: `math.log` and `math.log1p` codings raise at test 6 first (a NumPy log coding returns −1 and passes, correctly) |
| `screens[10].hints[0]` | Multiply the growth factors $1 + R$ together. | correct | Derivation or arithmetic step, checked |
| `screens[10].hints[1]` | With $T$ years, take the $T$-th root: `** (1 / len(returns))`. | correct | Derivation or arithmetic step, checked |
| `screens[10].hints[2]` | `growth *= 1 + r`, then `return growth ** (1 / len(returns)) - 1`. | correct | Derivation or arithmetic step, checked |
| `screens[10].feedback.correct` | Compound, take the root, subtract 1. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[10].feedback.generic` | Some tests failed. Multiply the growth factors, take the $T$-th root, then subtract 1. | correct | Derivation or arithmetic step, checked |
| `screens[10].explain.text` | The loop builds $(1 + R_1)\cdots(1 + R_T)$, and the root spreads it evenly over $T$ years. One test has a −10… | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[11].prose` | You must pick one of two funds. The risk-free rate is 4%. Fund B has the higher return. | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[11].canvas.params.rows` | table: [["Average yearly return", "9%", "12%"], ["Volatility", "12%", "20%"]] | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[11].widget.options[right]` | key: Fund A: Sharpe ratio 0.42 against 0.40 | correct | Recomputed; right under the convention the item states |
| `screens[11].widget.options[b].why` | wrong option 'Fund B: it returns 12%': You compared raw returns. B takes far more risk to get them. | correct | Checked false under the item's premises; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[11].widget.options[raw].why` | wrong option 'Fund A: 0.75 against 0.60': You divided the raw returns by volatility. Subtract the 4% risk-fre… | correct | Checked false under the item's premises; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[11].widget.options[same].why` | wrong option 'They are the same': Their Sharpe ratios are close, 0.42 and 0.40, but not equal. | correct | Checked false under the item's premises; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[11].feedback.byKey.b` | You compared raw returns. Per unit of risk, B earns a little less. | correct | Checked false under the item's premises; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[11].feedback.byKey.raw` | You left out the risk-free rate. The ratio uses excess return. | correct | Checked false under the item's premises; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[11].hints[0]` | Compute each Sharpe ratio. | correct | Derivation or arithmetic step, checked |
| `screens[11].hints[1]` | A: $(9 - 4)/12$. B: $(12 - 4)/20$. | correct | Derivation or arithmetic step, checked |
| `screens[11].hints[2]` | A: 0.42. B: 0.40. A is slightly better per unit of risk. | correct | Derivation or arithmetic step, checked |
| `screens[11].feedback.correct` | Fund A, just: 0.42 against 0.40. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `screens[11].feedback.generic` | Not quite right. Subtract the risk-free rate, then divide by the volatility. | correct | Derivation or arithmetic step, checked |
| `screens[11].explain.text` | A: $(0.09 - 0.04)/0.12 = 0.42$. B: $(0.12 - 0.04)/0.20 = 0.40$. The gap is tiny, and a few years of data coul… | correct | Recomputed; Monte Carlo, 200,000 five-year records: B ranks above A in 49% (script) |
| `quiz[0].prose` | You buy a share for £20.00, receive a £0.60 dividend, and sell it a year later for £21.00. | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `quiz[0].widget.answer` | key 0.08 %: 8%: $(21.00 + 0.60 - 20.00)/20.00$. | correct | Recomputed; right under the convention the item states |
| `quiz[0].feedback.byKey.price` | slip 0.05: That is the price change alone. Add the £0.60 dividend. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.byKey.div` | slip 0.03: That is the dividend yield alone. Add the price gain. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.correct` | 8%. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `quiz[0].feedback.generic` | Not quite right. Add the dividend to the price gain, then divide by £20.00. | correct | Derivation or arithmetic step, checked |
| `quiz[0].explain.text` | $(21.00 + 0.60 - 20.00)/20.00 = 1.60/20.00 = 8\%$. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `quiz[1].prose` | A fund returned 61.05% in total over five years. | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `quiz[1].widget.answer` | key 0.1 %: 10%: $1.6105^{1/5} - 1$. | correct | Recomputed; right under the convention the item states |
| `quiz[1].feedback.byKey.divide` | slip 0.1221: You divided by 5. That ignores compounding. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[1].feedback.correct` | 10% a year: $1.1^5 = 1.6105$. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `quiz[1].feedback.generic` | Not quite right. Take the fifth root of 1.6105. | correct | Derivation or arithmetic step, checked |
| `quiz[1].explain.text` | $1.6105^{1/5} = 1.10$, so 10% a year. Dividing 61.05% by 5 gives 12.21%, too high. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `quiz[2].prose` | A share's monthly log returns are 0.02, −0.01 and 0.03. | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `quiz[2].widget.answer` | key 0.0408 %: 4.08%: $e^{0.04} - 1$. | correct | Recomputed; right under the convention the item states |
| `quiz[2].feedback.byKey.sum` | slip 0.04: 0.04 is the total log return. Convert it: $e^{0.04} - 1$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.correct` | 4.08%. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `quiz[2].feedback.generic` | Not quite right. Add the log returns, then convert with $e^x - 1$. | correct | Derivation or arithmetic step, checked |
| `quiz[2].explain.text` | Log returns add: $0.02 - 0.01 + 0.03 = 0.04$. The simple return is $e^{0.04} - 1 = 4.08\%$. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `quiz[3].prose` | A strategy makes 0.8% every month. | correct | BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `quiz[3].widget.options[right]` | key: 10.03% | correct | Recomputed; right under the convention the item states |
| `quiz[3].widget.options[times].why` | wrong option '9.60%': You multiplied 0.8% by 12. Monthly returns compound. | correct | Checked false under the item's premises; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `quiz[3].widget.options[one].why` | wrong option '0.80%': That is one month. | correct | Checked false under the item's premises; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `quiz[3].feedback.correct` | $1.008^{12} - 1 = 10.03\%$. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |
| `quiz[3].feedback.generic` | Not quite right. Compound the monthly factor twelve times. | correct | Derivation or arithmetic step, checked |
| `quiz[3].explain.text` | $1.008^{12} = 1.1003$, so 10.03% a year, not $12 \times 0.8\% = 9.6\%$. | correct | Recomputed in the concepts script or by hand; BKM ch. 5 (holding-period return, arithmetic and geometric averages, Sharpe ratio) |

## l9-agreeing-today

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `summary.ideas[0]` | A forward fixes today the price $F$ of a trade on a later date. No money changes hands until then. | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `summary.ideas[1]` | At delivery the long gets $S_T - F$ and the short $F - S_T$: straight lines through $F$, with no floor. | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `summary.ideas[2]` | A forward on something you already hold, or must buy, fixes its price and cancels your exposure. | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `summary.formula` | Forward payoff at delivery: \text{long: } S_T - F, \qquad \text{short: } F - S_T; Both sides are bound. The t… | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `summary.trap` | A forward is not an option. Its payoff keeps falling below $F$; a floor at zero would need a right to walk aw… | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[0].prose` | A baker agrees today to buy one tonne of wheat from a miller in six months, at £200.00. No money changes hand… | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[0].widget.answer` | key 30 £: £30.00: wheat worth £230.00 bought for £200.00 | correct | Recomputed; right under the convention the item states |
| `screens[0].feedback.byKey.whole` | slip 230: You counted the whole wheat price. The baker still pays £200.00, so only the difference is a gain. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.paid` | slip -30: You subtracted the wrong way round. Paying £200.00 for wheat worth £230.00 is a gain. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.none` | slip 0: You valued the deal by what changed hands today. By delivery day the fixed price has become a bargain. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.price` | slip 200: That is what the baker pays, not what the deal is worth. Wheat worth £230.00 arrives for £200.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].hints[0]` | What could the baker do with the wheat the moment it arrives? | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[1]` | The baker pays £200.00 and receives wheat the market values at £230.00. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[2]` | Sell it at once: $230 - 200 = 30$. | correct | Derivation or arithmetic step, checked |
| `screens[0].feedback.correct` | The baker pays £200.00 for wheat worth £230.00: a gain of £30.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[0].feedback.generic` | Not quite right. Compare what the wheat is worth with what the baker pays for it. | correct | Derivation or arithmetic step, checked |
| `screens[0].explain.text` | The baker pays £200.00 for wheat worth £230.00, a gain of £30.00. The bold line shows that gain at every whea… | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[1].prose` | Slide the wheat price at delivery and watch the dot on the bold line. Its label shows what the agreement is w… | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[1].widget.options[loss]` | key: −£30.00: the baker must still pay £200.00 for wheat worth £170.00 | correct | Recomputed; right under the convention the item states |
| `screens[1].widget.options[floor].why` | wrong option '£0.00: the baker walks away and buys at the market': You treated the agreement as an option. Th… | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[1].widget.options[size].why` | wrong option '£30.00: the price moved £30.00': You took the size of the move and dropped its sign. Paying £20… | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[1].feedback.correct` | Below £200.00 the baker overpays, so the payoff is negative. | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[1].feedback.generic` | Not quite right. Slide the price to £170.00 and read the label on the dot. | correct | Derivation or arithmetic step, checked |
| `screens[1].explain.text` | At £170.00 the baker pays £200.00 for wheat worth £170.00, a loss of £30.00. The line keeps falling below £20… | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[2].prose` | This agreement is a **forward contract**. The fixed price is the **forward price** $F$, paid on the **deliver… | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[2].widget.answer` | key -30 £: −£30.00 | correct | Recomputed; right under the convention the item states |
| `screens[2].feedback.byKey.copied` | slip 30: You gave the miller the baker's payoff. The miller sells £230.00 of wheat for £200.00, which loses £… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].feedback.byKey.zero` | slip 0: You assumed the seller just collects the fixed price, so nothing is lost. The miller could have sold … | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].feedback.byKey.price` | slip 200: That is the cash the miller receives. The payoff compares it with the £230.00 the wheat is worth. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].hints[0]` | Could the miller have sold the wheat for more elsewhere? | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[1]` | The miller hands over wheat worth £230.00 and receives £200.00. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[2]` | $200 - 230 = -30$. | correct | Derivation or arithmetic step, checked |
| `screens[2].feedback.correct` | The miller sells £230.00 of wheat for £200.00: $F - S_T = -30$. | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[2].feedback.generic` | Not quite right. Compare what the miller receives with what the wheat is worth. | correct | Derivation or arithmetic step, checked |
| `screens[2].explain.text` | The miller hands over wheat worth £230.00 for £200.00, so the payoff is $F - S_T = 200 - 230 = -30$. The mill… | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[3].prose` | The forward price is $F = \text{£}200.00$. Fill in both sides' payoffs at delivery for four wheat prices. Use… | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[3].widget.rows[0][1]` | cell key -30; At £170.00 the long pays £200.00 for wheat worth £170.00. That is a loss, so the entry is negat… | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[0][2]` | cell key 30; At £170.00 the short sells for £200.00 wheat worth only £170.00: a gain. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[1][1]` | cell key 0; At $S_T = F$ the long pays exactly what the wheat is worth. Neither side gains. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[1][2]` | cell key 0; At $S_T = F$ the short receives exactly what the wheat is worth. Neither side gains. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[2][1]` | cell key 15; At £215.00 the long buys for £200.00 wheat worth £215.00. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[2][2]` | cell key -15; At £215.00 the short gives up wheat worth £215.00 for £200.00. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[3][1]` | cell key 40; At £240.00 the long buys for £200.00 wheat worth £240.00. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[3][2]` | cell key -40; At £240.00 the short gives up wheat worth £240.00 for £200.00. | correct | Recomputed; right under the convention the item states |
| `screens[3].hints[0]` | For each price, ask who would rather have traded at the market. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[1]` | At £200.00 the wheat is worth exactly what is paid for it. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[2]` | Long: $-30, 0, 15, 40$. Short: the same numbers with the sign flipped. | correct | Derivation or arithmetic step, checked |
| `screens[3].feedback.correct` | Long: −30, 0, 15, 40. Short: 30, 0, −15, −40. | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[3].feedback.generic` | Not quite right. The long gets $S_T - 200$, the short $200 - S_T$, losses negative. | correct | Derivation or arithmetic step, checked |
| `screens[3].explain.text` | Each row adds to zero: what the long gains, the short loses. At £200.00 both payoffs are 0, the edge where th… | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[4].prose` | Back to signing day. The baker and the miller agree $F = \text{£}200.00$ for delivery in six months. Wheat tr… | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[4].widget.options[nothing]` | key: £0.00 | correct | Recomputed; right under the convention the item states |
| `screens[4].widget.options[pays-f].why` | wrong option '£200.00': You paid the forward price today. $F$ is paid on the delivery date, when the wheat ar… | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[4].widget.options[spot].why` | wrong option '£195.00': You bought the wheat at today's price. Nobody buys wheat today; they fix the price of… | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[4].widget.options[premium].why` | wrong option 'A small fee, like an option premium': You treated the forward as an option. Both sides are boun… | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[4].feedback.byKey.pays-f` | You paid the forward price today. $F$ is paid on the delivery date, in exchange for the wheat. | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[4].feedback.byKey.premium` | You treated the forward as an option. A forward gives no choice, so there is nothing to pay for. | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[4].hints[0]` | When does the wheat change hands? | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[1]` | The £200.00 is paid in exchange for the wheat. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[2]` | Signing creates two promises and moves no cash. Everything happens on the delivery date. | correct | Derivation or arithmetic step, checked |
| `screens[4].feedback.correct` | Nothing changes hands until delivery. | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[4].feedback.generic` | Not quite right. Ask what is exchanged on signing day, and what on delivery day. | correct | Derivation or arithmetic step, checked |
| `screens[4].explain.text` | A forward costs nothing to enter: each side takes on an obligation, and neither pays the other. The £200.00 m… | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[5].prose` | Now draw the baker's payoff yourself. The forward price is £200.00. Drag each blue point up or down to the pa… | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[5].widget.target` | key curve x - 200 | correct | Recomputed; right under the convention the item states |
| `screens[5].feedback.byKey.floor` | You drew a floor at zero, as for a call. The baker must buy at £200.00 even when wheat is cheaper, so the lin… | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[5].feedback.byKey.short` | You drew the miller's side. The baker gains when wheat rises. | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[5].hints[0]` | What is the payoff at £160.00? Below the forward price, the baker still has to buy. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[1]` | At £200.00 the payoff is 0, and it changes by £1.00 for each £1.00 of wheat price. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[2]` | The points sit at −40, −20, 0, 20 and 40: one straight line through £200.00. | correct | Derivation or arithmetic step, checked |
| `screens[5].feedback.correct` | A straight line through £200.00, falling below zero on the left. | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[5].feedback.generic` | Not quite right. At each point, work out $S_T - 200$, including below £200.00. | correct | Derivation or arithmetic step, checked |
| `screens[5].explain.text` | The forward payoff is the straight line $S_T - 200$, negative below £200.00. A floor at zero would need a rig… | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[6].prose` | You found the payoffs price by price. For a forward with price $F$, at delivery: $$\text{long: } S_T - F, \qq… | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[6].widget.options[forty]` | key: £40.00 | correct | Recomputed; right under the convention the item states |
| `screens[6].widget.options[sixty].why` | wrong option '£60.00': You solved $F - S_T = -10$, the short's payoff. For the long, $S_T - 50 = -10$. | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[6].widget.options[never].why` | wrong option 'Never: it cannot pay less than £0.00': You gave the forward a floor. Only an option has one. | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[6].feedback.correct` | $S_T - 50 = -10$ gives $S_T = 40$. | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[6].feedback.generic` | Not quite right. Set the long's payoff $S_T - 50$ equal to $-10$. | correct | Derivation or arithmetic step, checked |
| `screens[6].explain.text` | The long pays $S_T - 50$, which equals $-10$ when $S_T = 40$. Below the forward price the long loses one for … | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[7].prose` | A farmer will harvest one tonne of wheat in six months. To fix her selling price she goes short a forward at … | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[7].widget.answer` | key 200 £: £200.00 at every price | correct | Recomputed; right under the convention the item states |
| `screens[7].feedback.byKey.spot` | slip 175: That is the crop alone at £175.00. Add the short forward, which pays $200 - 175 = 25$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].feedback.byKey.fwd` | slip 25: That is the forward alone. She also holds the crop, worth £175.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].feedback.byKey.zero` | slip 0: The forward cancels the risk, not the value. She still sells a tonne of wheat. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].hints[0]` | Add the two pieces at one price, say £175.00. | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[1]` | At £175.00 the crop is worth £175.00 and the short forward pays $200 - 175 = 25$. | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[2]` | $S_T + (200 - S_T) = 200$ at every price. | correct | Derivation or arithmetic step, checked |
| `screens[7].feedback.correct` | $S_T + (200 - S_T) = 200$: £200.00 whatever wheat does. | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[7].feedback.generic` | Not quite right. Add the crop's value and the short forward's payoff. | correct | Derivation or arithmetic step, checked |
| `screens[7].explain.text` | The crop is worth $S_T$ and the short forward pays $200 - S_T$, so together they are worth £200.00. The bold … | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[8].prose` | A UK importer must pay a US supplier 1,000,000 US dollars in three months. A bank offers a three-month forwar… | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[8].widget.answer` | key 790000 £: £790,000.00, the forward rate times the amount | correct | Recomputed; right under the convention the item states |
| `screens[8].feedback.byKey.spot` | slip 820000: That is the cost without the forward. The forward pays £30,000.00, which brings the cost down. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.payoff` | slip 30000: That is the forward's payoff alone. The importer still has to buy 1,000,000 dollars. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.added` | slip 850000: You added the payoff as a cost. The forward pays the importer when the dollar rises. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].hints[0]` | Price the dollars at the market first, then add what the forward pays. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[1]` | The forward pays $(0.82 - 0.79) \times 1{,}000{,}000$ pounds. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[2]` | Dollars cost £820,000.00; the forward pays £30,000.00; the net is £790,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[8].feedback.correct` | £820,000.00 at the market, less the forward's £30,000.00: £790,000.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[8].feedback.generic` | Not quite right. Buy the dollars at £0.8200, then subtract the forward's payoff. | correct | Derivation or arithmetic step, checked |
| `screens[8].explain.text` | At the market the dollars cost £820,000.00, and the forward pays $(0.82 - 0.79) \times 1{,}000{,}000 = \text{… | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[9].prose` | A trader is long a forward on a share at $F = \text{£}100.00$. She also buys a put struck at £100.00, expirin… | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[9].widget.options[call]` | key: A call struck at £100.00 | correct | Recomputed; right under the convention the item states |
| `screens[9].widget.options[share].why` | wrong option 'The share itself': You kept the forward's slope everywhere. Below £100.00 the put's gain cancel… | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[9].widget.options[short-put].why` | wrong option 'A short put struck at £100.00': A short put loses below the strike and is flat above it. This p… | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[9].widget.options[lower-fwd].why` | wrong option 'A forward at £90.00': Moving the forward price keeps a straight line. This pair has a kink at £… | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[9].feedback.byKey.share` | You kept the forward's slope everywhere. Below £100.00 the put's gain cancels the forward's loss. | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[9].hints[0]` | Read the bold line below £100.00 and above it. | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[1]` | Below £100.00 the put pays $100 - S_T$ and the forward pays $S_T - 100$. | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[2]` | Below £100.00 the two cancel to 0. Above, only the forward pays: $S_T - 100$. Which contract pays $\max(S_T -… | correct | Derivation or arithmetic step, checked |
| `screens[9].feedback.correct` | Flat at 0 below £100.00 and $S_T - 100$ above: a call. | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `screens[9].feedback.generic` | Not quite right. Work out the total payoff at £90.00 and at £110.00. | correct | Derivation or arithmetic step, checked |
| `screens[9].explain.text` | Below £100.00 the put pays $100 - S_T$ and the forward $S_T - 100$: together 0. Above, only the forward pays,… | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `quiz[0].prose` | You are long a forward on a share at $F = \text{£}80.00$. On the delivery date the share trades at £72.50. | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `quiz[0].widget.answer` | key -7.5 £: −£7.50 | correct | Recomputed; right under the convention the item states |
| `quiz[0].feedback.byKey.sign` | slip 7.5: You took $F - S_T$, the short's payoff. You must buy at £80.00 a share worth £72.50. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.byKey.floor` | slip 0: You gave the forward a floor. You are bound to buy, so the loss stands. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.byKey.price` | slip -80: You counted the whole forward price as lost. You also receive the share, worth £72.50. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.correct` | $72.50 - 80.00 = -7.50$. | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `quiz[0].feedback.generic` | Not quite right. The long's payoff is $S_T - F$. | correct | Derivation or arithmetic step, checked |
| `quiz[0].explain.text` | You pay £80.00 for a share worth £72.50, so the payoff is $S_T - F = -7.50$. There is no option to walk away. | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `quiz[1].prose` | A fund is short a forward on 500 shares at £40.00 a share. On the delivery date the share trades at £46.00. | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `quiz[1].widget.answer` | key -3000 £: −£3,000.00 | correct | Recomputed; right under the convention the item states |
| `quiz[1].feedback.byKey.sign` | slip 3000: You used the long's payoff. The fund sells at £40.00 shares worth £46.00, which loses. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[1].feedback.byKey.per` | slip -6: That is the payoff per share. The forward covers 500 shares. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[1].feedback.correct` | $500 \times (40 - 46) = -3{,}000$. | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `quiz[1].feedback.generic` | Not quite right. Find the short's payoff per share, $F - S_T$, then multiply by 500. | correct | Derivation or arithmetic step, checked |
| `quiz[1].explain.text` | Per share the short gets $F - S_T = 40 - 46 = -6$. On 500 shares that is −£3,000.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `quiz[2].prose` | An airline goes long a forward on 1,000 tonnes of jet fuel at £600.00 a tonne. At delivery fuel trades at £54… | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `quiz[2].widget.answer` | key 600000 £: £600,000.00 | correct | Recomputed; right under the convention the item states |
| `quiz[2].feedback.byKey.spot` | slip 540000: That ignores the forward. It loses $1{,}000 \times (540 - 600) = -60{,}000$, which the airline p… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.byKey.payoff` | slip -60000: That is the forward's payoff alone. The airline still buys 1,000 tonnes of fuel. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.byKey.sign` | slip 480000: You subtracted the forward's loss. A loss adds to what the airline pays. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.correct` | £540,000.00 at the market plus the forward's £60,000.00 loss: £600,000.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `quiz[2].feedback.generic` | Not quite right. Add the market cost and the forward's loss. | correct | Derivation or arithmetic step, checked |
| `quiz[2].explain.text` | The fuel costs £540,000.00 at the market, and the forward loses £60,000.00. In total the airline pays £600,00… | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `quiz[3].prose` | Two firms sign a one-year forward on a share at $F = \text{£}25.00$. | correct | Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `quiz[3].widget.options[right]` | key: No money changes hands, and both firms are bound to trade in a year | correct | Recomputed; right under the convention the item states |
| `quiz[3].widget.options[long-pays].why` | wrong option 'The buyer pays £25.00 now and receives the share in a year': You paid the forward price at sign… | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `quiz[3].widget.options[option].why` | wrong option 'The buyer may walk away in a year if the share is below £25.00': You gave the buyer a choice. T… | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `quiz[3].widget.options[seller-pays].why` | wrong option 'The seller pays the buyer a fee for the obligation': You priced the promise as if one side were… | correct | Checked false under the item's premises; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `quiz[3].feedback.correct` | A forward is two promises and no cash today. | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |
| `quiz[3].feedback.generic` | Not quite right. Ask what a forward obliges each side to do, and when. | correct | Derivation or arithmetic step, checked |
| `quiz[3].explain.text` | Signing a forward creates an obligation on both sides and moves no money. In a year the buyer pays £25.00 and… | correct | Recomputed in the concepts script or by hand; Hull 10e §1.3 (forward contracts and payoffs), §1.5 (options against forwards) |

## l10-cost-of-carry

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `summary.ideas[0]` | Borrowing to buy the share now delivers it later for $S_0(1 + r)^T$. Any other forward price is free money. | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `summary.ideas[1]` | Too high: borrow, buy and sell forward. Too low: sell a borrowed share, lend the cash and buy forward. | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `summary.ideas[2]` | Income from holding (dividends) lowers the forward; costs of holding (storage) raise it. Forecasts play no pa… | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `summary.formula` | Forward price by cost of carry: F = \left(S_0 - PV(\text{income})\right)(1 + r)^T; With no income, $F = S_0(1… | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `summary.trap` | The forward price is not the expected future price. It is what replicating the forward costs: the share plus … | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[0].prose` | You will need one share in a year. It costs £100.00 today, and you can borrow at 5% a year. **Plan A:** borro… | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[0].canvas.params.rows` | table: [["Borrow at 5%", "100.00", "?"], ["Buy the share", "-100.00", "hold the share"], ["Net cash", "0.00",… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[0].widget.answer` | key 105 £: £105.00 | correct | Recomputed; right under the convention the item states |
| `screens[0].feedback.byKey.no-interest` | slip 100: You repaid only what you borrowed. The lender charges 5% for the year. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.interest` | slip 5: That is the interest alone. The £100.00 itself is repaid too. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.forward` | slip 95: You took the interest off. Borrowing costs you interest; it does not earn it. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].hints[0]` | The lender wants the £100.00 back, and something for the year. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[1]` | A year at 5% adds $0.05 \times 100$. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[2]` | $100 \times 1.05 = 105$. | correct | Derivation or arithmetic step, checked |
| `screens[0].feedback.correct` | $100 \times 1.05 = 105$: you repay £105.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[0].feedback.generic` | Not quite right. Repay the £100.00 plus a year's interest at 5%. | correct | Derivation or arithmetic step, checked |
| `screens[0].explain.text` | You repay $100 \times 1.05 = \text{£}105.00$. So Plan A gets you the share in a year for £105.00, fixed today… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[1].prose` | Plan A fixes today what the share costs you later: the loan repayment. Slide the rate $r$ and the time $T$, a… | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[1].canvas.derive` | formulas: P.y=100 * pow(1 + r, P.x) | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[1].widget.options[flat]` | key: £100.00 for every $T$: free borrowing makes holding the share cost nothing | correct | Recomputed; right under the convention the item states |
| `screens[1].widget.options[time].why` | wrong option 'More than £100.00, and more the longer you wait': You charged for time itself. With $r = 0$ the… | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[1].widget.options[less].why` | wrong option 'Less than £100.00, because money later is worth less': You discounted the price. Plan A repays … | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[1].feedback.correct` | At $r = 0$ the line is flat at £100.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[1].feedback.generic` | Not quite right. Slide the rate to 0% and read the caption at a few times. | correct | Derivation or arithmetic step, checked |
| `screens[1].explain.text` | At 0% the loan repays exactly £100.00 however long you hold the share. Raise the rate and the curve bends upw… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[2].prose` | **Plan B:** go long a one-year forward on the share at price $F$. It costs nothing today, and in a year you p… | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[2].widget.answer` | key 105 £: £105.00 | correct | Recomputed; right under the convention the item states |
| `screens[2].feedback.byKey.spot` | slip 100: You priced the forward at today's share price. Plan A shows that holding the share for a year costs… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].feedback.byKey.interest` | slip 5: That is the interest alone. The forward pays for the whole share. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].feedback.byKey.discounted` | slip 95.24: You discounted £100.00 instead of growing it. $F$ is paid in a year, so it carries the interest. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].hints[0]` | Both plans cost nothing today and end with one share in a year. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[1]` | Plan A pays £105.00 in a year for the share; Plan B pays $F$. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[2]` | If the payments differ, everyone picks the cheaper plan. They match when $F = 105$. | correct | Derivation or arithmetic step, checked |
| `screens[2].feedback.correct` | $F = 105$: both plans pay £105.00 in a year for the share. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[2].feedback.generic` | Not quite right. Compare what each plan pays in a year. | correct | Derivation or arithmetic step, checked |
| `screens[2].explain.text` | Two plans that end in the same place, and cost the same today, must pay the same later. So $F = 105$, the **n… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[3].prose` | A dealer quotes the one-year forward at £108.00, above the £105.00 that Plan A costs. Borrow £100.00, buy the… | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[3].widget.rows[0][2]` | cell key -105; You repaid only what you borrowed, or forgot the sign. You pay out $100 \times 1.05 = 105$. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[2][2]` | cell key 108; Selling forward at £108.00 brings in £108.00 when you deliver the share. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[3][1]` | cell key 0; Today you borrow £100.00 and spend it all on the share: the net is £0.00. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[3][2]` | cell key 3; Add the year's column: $-105 + 108$. | correct | Recomputed; right under the convention the item states |
| `screens[3].hints[0]` | In a year you repay the loan and deliver the share to the dealer. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[1]` | The loan repays $100 \times 1.05$; the dealer pays £108.00 for the share. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[2]` | Today: $100 - 100 + 0 = 0$. In a year: $-105 + 108 = 3$. | correct | Derivation or arithmetic step, checked |
| `screens[3].feedback.correct` | Nothing today, £3.00 for certain in a year. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[3].feedback.generic` | Not quite right. Add each column, with money paid out as negative. | correct | Derivation or arithmetic step, checked |
| `screens[3].explain.text` | You put in nothing today and collect £3.00 in a year, whatever the share does. That is an **arbitrage**: borr… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[4].prose` | Another dealer quotes the forward at £102.00, below Plan A's £105.00. You can sell a borrowed share today and… | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[4].widget.options[reverse]` | key: Buy the forward, sell a borrowed share for £100.00, and lend the £100.00 at 5% | correct | Recomputed; right under the convention the item states |
| `screens[4].widget.options[carry].why` | wrong option 'Sell the forward, and buy the share with borrowed cash': That is the trade for a forward that i… | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[4].widget.options[bet].why` | wrong option 'Buy the forward and wait': That is a bet on the share, not an arbitrage. If it ends below £102.… | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[4].widget.options[share].why` | wrong option 'Buy the share today and hold it': That is Plan A, which costs £105.00. It does not use the chea… | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[4].feedback.byKey.carry` | You ran the trade for a forward that is too dear. Here the forward is the cheap side, so you buy it. | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[4].feedback.byKey.bet` | Buying the forward alone is exposed to the share price. An arbitrage needs the offsetting share sale. | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[4].hints[0]` | The forward is cheap, so you want to be the buyer. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[1]` | Buying forward gives you a share in a year. Whom could you hand it to? | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[2]` | Sell a borrowed share now and lend the £100.00: it grows to £105.00. Pay £102.00 for the forward's share and … | correct | Derivation or arithmetic step, checked |
| `screens[4].feedback.correct` | The lending grows to £105.00; the share costs £102.00; you keep £3.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[4].feedback.generic` | Not quite right. Buy what is cheap, the forward, and sell what is dear, the share. | correct | Derivation or arithmetic step, checked |
| `screens[4].explain.text` | The borrowed share sells for £100.00, which grows to £105.00 in the bank. The forward delivers a share for £1… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[5].prose` | Analysts expect the share, now £100.00, to be worth £112.00 in a year. The rate is still 5%. A colleague pric… | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[5].widget.options[fair]` | key: £105.00 | correct | Recomputed; right under the convention the item states |
| `screens[5].widget.options[forecast].why` | wrong option '£112.00': You priced the forward at the forecast. Plan A delivers the share for £105.00 whateve… | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[5].widget.options[spot].why` | wrong option '£100.00': You forgot the financing. Holding the share for a year costs £5.00 of interest. | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[5].widget.options[both].why` | wrong option '£117.60': You grew the forecast by the rate, $112 \times 1.05$. The forecast plays no part. | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[5].feedback.byKey.forecast` | You priced the forward at the forecast. At £112.00 you could borrow, buy and sell forward for a sure £7.00. | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[5].hints[0]` | What would you do if the forward were £112.00? | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[1]` | Plan A gets the share in a year for £105.00, with no forecast needed. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[2]` | At £112.00 you would borrow, buy and sell forward for £7.00 of free money. So $F = 105$. | correct | Derivation or arithmetic step, checked |
| `screens[5].feedback.correct` | £105.00, from the cost of carry alone. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[5].feedback.generic` | Not quite right. Ask what replicating the forward costs. | correct | Derivation or arithmetic step, checked |
| `screens[5].explain.text` | At £112.00 you would borrow £100.00, buy the share and sell it forward, locking in £7.00. Everyone would, unt… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[6].prose` | Now in general, with no dividends. Strategy 1: buy the share today for $S_0$. Strategy 2: go long the forward… | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[6].widget.lines[o1]` | At $T$ both strategies hold one share: in strategy 2 the loan repays $F$, which pays for the forward's share | correct | Derivation or arithmetic step, checked |
| `screens[6].widget.lines[o2]` | Equal payoffs at $T$ need equal costs today, or buying one strategy and selling the other is free money | correct | Derivation or arithmetic step, checked |
| `screens[6].widget.lines[o3]` | $S_0 = \dfrac{F}{(1 + r)^T}$, the cost today of each strategy | correct | Derivation or arithmetic step, checked |
| `screens[6].widget.lines[o4]` | $F = S_0 (1 + r)^T$, multiplying both sides by $(1 + r)^T$ | correct | Derivation or arithmetic step, checked |
| `screens[6].feedback.byKey.o3` | The equation of costs needs the no-arbitrage reason first: equal payoffs at $T$. | correct | Derivation or arithmetic step, checked |
| `screens[6].feedback.byKey.o4` | Solving for $F$ comes last, once the costs are set equal. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[0]` | Start from what each strategy holds on the delivery date. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[1]` | The no-arbitrage step turns equal payoffs into equal costs. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[2]` | Payoffs match, so costs match: $S_0 = F/(1 + r)^T$. Then solve for $F$. | correct | Derivation or arithmetic step, checked |
| `screens[6].feedback.correct` | Same payoff, same cost, then solve for $F$. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[6].feedback.generic` | Not quite right. Compare the payoffs first, then the costs, then rearrange. | correct | Derivation or arithmetic step, checked |
| `screens[6].explain.text` | With $S_0 = 100$, $r = 0.05$ and $T = 1$ this gives $F = 105$, your Plan A. With continuous compounding the s… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[7].prose` | Now the share pays a £2.00 dividend in six months. Whoever holds the share gets it; the forward's buyer does … | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[7].widget.answer` | key 102.95 £: £102.95: $(100 - 2/1.05^{0.5}) \times 1.05$ | correct | Recomputed; right under the convention the item states |
| `screens[7].feedback.byKey.ignored` | slip 105: You left out the dividend. Holding the share earns £2.00 that the forward's buyer never sees. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].feedback.byKey.not-grown` | slip 103: You took £2.00 off £105.00. The dividend arrives at six months and earns interest until the year's … | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].feedback.byKey.not-disc` | slip 102.9: You took the full £2.00 off today's price. It arrives in six months, so today it is worth only £1… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].feedback.byKey.added` | slip 107: You added the dividend. It is income to the holder, so it lowers the cost of carry. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].hints[0]` | The dividend makes holding the share cheaper. What is it worth today? | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[1]` | Today the dividend is worth $\dfrac{2}{1.05^{0.5}} = 1.95$. | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[2]` | Take that off the share and grow the rest: $(100 - 1.95) \times 1.05 = 102.95$. | correct | Derivation or arithmetic step, checked |
| `screens[7].feedback.correct` | $(100 - 1.952) \times 1.05 = 102.95$. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[7].feedback.generic` | Not quite right. Take the dividend's present value off the share price, then grow for a year. | correct | Derivation or arithmetic step, checked |
| `screens[7].explain.text` | The dividend is worth $\tfrac{2}{1.05^{0.5}} = \text{£}1.95$ today, so $F = (100 - 1.95) \times 1.05 = \text{… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[8].prose` | One pound buys 1.2500 US dollars today. A year's deposit earns 4% in pounds and 5% in dollars. A bank sets th… | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[8].canvas.params.rows` | table: [["Keep pounds at 4%", "£1.00", "£1.04"], ["Change to dollars at 5%", "1.2500 dollars", "1.3125 dollar… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[8].widget.answer` | key 1.262 : 1.2620, from $1.3125 / 1.04$ (1.2625 by the shortcut $1.25 \times (1 + 0.05 - 0.04)$) | correct | Recomputed; right under the convention the item states |
| `screens[8].feedback.byKey.inverted` | slip 1.2381: You swapped the two rates, $1.25 \times 1.04 / 1.05$. The dollar deposit earns more, so a pound … | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.spot` | slip 1.25: That is today's rate. The two deposits grow at different rates, so the forward differs. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.dollars` | slip 1.3125: That is the dollars in a year from £1.00. Divide by the £1.04 the pound route gives. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].hints[0]` | In a year, £1.04 must swap at the forward rate for the 1.3125 dollars. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[1]` | The forward rate is dollars per pound: dollars in a year over pounds in a year. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[2]` | $F = \dfrac{1.3125}{1.04} = 1.2620$. | correct | Derivation or arithmetic step, checked |
| `screens[8].feedback.correct` | $1.3125 / 1.04 = 1.2620$ dollars per pound. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[8].feedback.generic` | Not quite right. Divide the dollars in a year by the pounds in a year. | correct | Derivation or arithmetic step, checked |
| `screens[8].explain.text` | £1.00 grows to £1.04, or to 1.3125 dollars. They must swap at the forward rate, so $F = \tfrac{1.3125}{1.04} … | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[9].prose` | An equity index stands at 8,000 points. Borrowing costs 4% a year, and the index's shares pay dividends of 5%… | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[9].widget.answer` | key 7920 : 7,920, from $8000 \times (1 + 0.04 - 0.05)$; 7,924 by $8000 \times 1.04/1.05$ | correct | Recomputed; right under the convention the item states |
| `screens[9].feedback.byKey.ignored` | slip 8320: You charged the interest but left out the dividends. The holder earns 5% back. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[9].feedback.byKey.spot` | slip 8000: That would need the interest and the dividends to cancel. Here the dividends are larger. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[9].feedback.byKey.added` | slip 8720: You added the dividends to the interest. Dividends are income to the holder, so they lower the for… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[9].hints[0]` | Is the net cost of carrying the index positive or negative? | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[1]` | It costs 4% and earns 5%: a net carry of −1%. | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[2]` | $8000 \times (1 + 0.04 - 0.05) = 7{,}920$. | correct | Derivation or arithmetic step, checked |
| `screens[9].feedback.correct` | About 7,920: below today's level. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `screens[9].feedback.generic` | Not quite right. Net the interest against the dividend yield, then apply it for a year. | correct | Derivation or arithmetic step, checked |
| `screens[9].explain.text` | Carrying the index costs 4% and earns 5%, a net carry of −1%. So $F \approx S_0(1 + r - y)^T = 8000 \times 0.… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[0].prose` | A share costs £50.00. The rate is 4% a year, compounded yearly, and the share pays no dividends. | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[0].widget.answer` | key 54.08 £: £54.08 | correct | Recomputed; right under the convention the item states |
| `quiz[0].feedback.byKey.simple` | slip 54: You used simple interest, $50 \times 1.08$. The loan compounds, so the second year earns interest on… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.byKey.one-year` | slip 52: That is the one-year forward. The delivery is two years away. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.byKey.spot` | slip 50: You forgot the financing. Holding the share for two years costs interest. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.correct` | $50 \times 1.04^2 = 54.08$. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[0].feedback.generic` | Not quite right. Grow £50.00 at 4% for two years. | correct | Derivation or arithmetic step, checked |
| `quiz[0].explain.text` | Borrowing £50.00 for two years at 4% repays $50 \times 1.04^2 = \text{£}54.08$. That is the cost of Plan A, s… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[1].prose` | A forward on a share is quoted above $S_0(1 + r)^T$. The share pays no dividends. | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[1].widget.options[carry]` | key: Borrow, buy the share, and sell the forward | correct | Recomputed; right under the convention the item states |
| `quiz[1].widget.options[reverse].why` | wrong option 'Sell a borrowed share, lend the cash, and buy the forward': That is the trade for a forward tha… | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[1].widget.options[short].why` | wrong option 'Sell the forward and wait': That is a bet that the share falls. Without the share in hand, a ri… | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[1].widget.options[nothing].why` | wrong option 'None: the forward reflects what the market expects': You priced the forward by expectations. It… | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[1].feedback.correct` | Cash and carry: you deliver a share that cost $S_0(1 + r)^T$ for the higher quote. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[1].feedback.generic` | Not quite right. Sell what is dear, the forward, and buy what is cheap, the share. | correct | Derivation or arithmetic step, checked |
| `quiz[1].explain.text` | Borrowing to buy the share costs $S_0(1 + r)^T$ at delivery. Selling it forward above that locks in the diffe… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[2].prose` | Gold costs £2,000.00 an ounce today. The rate is 5% a year. Storing an ounce for a year costs £10.00, paid at… | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[2].widget.answer` | key 2110 £: £2,110.00 | correct | Recomputed; right under the convention the item states |
| `quiz[2].feedback.byKey.no-storage` | slip 2100: You left out the storage. Holding gold costs £10.00 more, so the forward is higher. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.byKey.minus` | slip 2090: You treated storage as income. It is a cost of holding, so it raises the forward. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.byKey.spot` | slip 2000: You forgot the financing and the storage. Holding gold for a year costs both. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.correct` | $2000 \times 1.05 + 10 = 2{,}110$. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[2].feedback.generic` | Not quite right. Add the interest and the storage cost of holding gold for a year. | correct | Derivation or arithmetic step, checked |
| `quiz[2].explain.text` | Plan A borrows £2,000.00, repaying £2,100.00, and pays £10.00 to store the gold. Delivering gold in a year th… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[3].prose` | A share trades at £80.00. The interest rate is 0%, and the share pays no dividends. | correct | Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[3].widget.options[same]` | key: £80.00 | correct | Recomputed; right under the convention the item states |
| `quiz[3].widget.options[grown].why` | wrong option 'More than £80.00': You charged for time. At 0% borrowing £80.00 for three years repays exactly … | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[3].widget.options[less].why` | wrong option 'Less than £80.00': You discounted the price. A lower forward would need income from holding the… | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[3].widget.options[unknown].why` | wrong option 'It depends on where the share is expected to go': You priced the forward by a forecast. It is p… | correct | Checked false under the item's premises; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[3].feedback.correct` | With nothing to pay and nothing earned, $F = S_0$. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |
| `quiz[3].feedback.generic` | Not quite right. Work out what Plan A costs at a 0% rate. | correct | Derivation or arithmetic step, checked |
| `quiz[3].explain.text` | $F = 80 \times (1 + 0)^3 = 80$. Carrying the share costs nothing, so the forward equals today's price. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.4–5.6 (forward price, known income, known yield), §5.10 (currencies), §5.11 (storage), §5.14 |

## l11-margin

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `summary.ideas[0]` | A future is a forward traded on an exchange and settled every evening: each day's gain or loss moves in cash. | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `summary.ideas[1]` | A margin call comes when the balance closes below the maintenance margin, and it restores the initial margin. | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `summary.ideas[2]` | Daily settlement limits what anyone can owe to about a day's move. The future converges to spot at expiry. | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `summary.formula` | Marking to market: B_t = B_{t-1} + n\,m\,(F_t - F_{t-1}); Below maintenance, pay in up to the initial margin. | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `summary.trap` | Settle every evening, not once at the end. A call due on a bad day is not cancelled by later gains. | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[0].prose` | A **futures contract** is a forward traded on an exchange. You go long one index future at 8,000 points. Each… | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[0].canvas.state` | plotted values: [[8000, 7960, null, null, null, null]] | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[0].widget.answer` | key -400 £: −£400.00: 40 points at £10.00 | correct | Recomputed; right under the convention the item states |
| `screens[0].feedback.byKey.sign` | slip 400: You are long, so a fall is a loss. Use a negative number. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.points` | slip -40: That is the move in points. Each point is worth £10.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.tick` | slip -200: You valued each point at £5.00. That is one tick, half a point. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].hints[0]` | How many points did the future move, and which way? | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[1]` | It fell from 8,000 to 7,960: 40 points against you. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[2]` | $-40 \times \text{£}10.00 = -\text{£}400.00$. | correct | Derivation or arithmetic step, checked |
| `screens[0].feedback.correct` | A 40-point fall at £10.00 a point: −£400.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[0].feedback.generic` | Not quite right. Multiply the change in points by £10.00 a point. | correct | Derivation or arithmetic step, checked |
| `screens[0].explain.text` | The future fell 40 points, and you are long, so you lose $40 \times 10 = \text{£}400.00$. Unlike a forward, a… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[1].prose` | To trade, you leave £6,000.00 with the exchange. Each evening it adds your gain or takes your loss. If the ba… | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[1].canvas.state` | plotted values: [[6000, 5600, 5000, 4300, 6000, 6500]] | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[1].widget.answer` | key d3 | correct | Recomputed; right under the convention the item states |
| `screens[1].feedback.byKey.d1` | Day 1 closes at £5,600.00. That is below the £6,000.00 you started with, but above £4,500.00. | correct | Checked false under the item's premises; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[1].feedback.byKey.d2` | Day 2 closes at £5,000.00, still above £4,500.00. | correct | Checked false under the item's premises; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[1].feedback.byKey.d4` | Day 4 is back at £6,000.00: that jump is your top-up after day 3. | correct | Checked false under the item's premises; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[1].feedback.byKey.d5` | Day 5 closes at £6,500.00, above both lines. | correct | Checked false under the item's premises; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[1].hints[0]` | Find the dashed line at £4,500.00. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[1]` | Only one evening closes under that line. | correct | Derivation or arithmetic step, checked |
| `screens[1].hints[2]` | Day 3 closes at £4,300.00, below £4,500.00. | correct | Derivation or arithmetic step, checked |
| `screens[1].feedback.correct` | Day 3: the balance closes at £4,300.00, below £4,500.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[1].feedback.generic` | Not quite right. Look for the evening the balance closes below £4,500.00, not below £6,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[1].explain.text` | Days 1 and 2 dip below £6,000.00, but the rule is the £4,500.00 line. Day 3 closes at £4,300.00, so you pay i… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[2].prose` | The £6,000.00 is the **initial margin**; £4,500.00 is the **maintenance margin**. Settling gains and losses e… | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[2].canvas.state` | plotted values: [[6000, 5600, 5000, 4300, 6000, 6500]] | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[2].widget.answer` | key 1700 £: £1,700.00 | correct | Recomputed; right under the convention the item states |
| `screens[2].feedback.byKey.maint` | slip 200: You topped up to the maintenance level. A call restores the initial margin, £6,000.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].feedback.byKey.whole` | slip 6000: You paid the whole initial margin again. The £4,300.00 is still yours; you only fill the gap. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].feedback.byKey.loss` | slip 700: That is day 3's loss. The call fills the gap from £4,300.00 up to £6,000.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].hints[0]` | A margin call restores the balance to one of the two lines. Which one? | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[1]` | The call tops the account up to the initial margin, £6,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[2]` | $6{,}000 - 4{,}300 = 1{,}700$. | correct | Derivation or arithmetic step, checked |
| `screens[2].feedback.correct` | $6{,}000 - 4{,}300 = 1{,}700$: back to the initial margin. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[2].feedback.generic` | Not quite right. Top the balance up to the initial margin. | correct | Derivation or arithmetic step, checked |
| `screens[2].explain.text` | The call is $6{,}000 - 4{,}300 = \text{£}1{,}700.00$, back up to the initial margin. The trigger is the maint… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[3].prose` | Now build the account yourself, one contract at £10.00 a point. Balance means after the evening's settlement,… | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[3].canvas.state` | plotted values: [[8000, 7960, 7900, 7830, 7830, 7880]] | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[3].widget.rows[1][2]` | cell key -600; Day 2 moves from 7,960 to 7,900: 60 points down, at £10.00 a point. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[1][3]` | cell key 5000; Start from day 1's £5,600.00 and take off day 2's loss. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[1][4]` | cell key 0; | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[2][2]` | cell key -700; | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[2][3]` | cell key 4300; | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[2][4]` | cell key 1700; Day 3 closes at £4,300.00, below £4,500.00. Top it up to £6,000.00. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[3][2]` | cell key 0; The price did not move on day 4, so nothing is settled. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[3][3]` | cell key 6000; Day 4 starts at £6,000.00 after your £1,700.00 top-up. With no price change, it stays there. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[3][4]` | cell key 0; | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[4][2]` | cell key 500; | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[4][3]` | cell key 6500; Day 5 starts from £6,000.00, not from £4,300.00: the top-up is in the account. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[4][4]` | cell key 0; | correct | Recomputed; right under the convention the item states |
| `screens[3].hints[0]` | Each day: points moved times £10.00, added to the last balance plus any top-up. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[1]` | Day 3 is the first balance below £4,500.00. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[2]` | Gains: −600, −700, 0, 500. Balances: 5,000, 4,300, 6,000, 6,500. One call: £1,700.00 after day 3. | correct | Derivation or arithmetic step, checked |
| `screens[3].feedback.correct` | One call, £1,700.00 after day 3; the week ends at £6,500.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[3].feedback.generic` | Not quite right. Work one row at a time, and check each balance against £4,500.00. | correct | Derivation or arithmetic step, checked |
| `screens[3].explain.text` | The losses of days 2 and 3 take the balance to £4,300.00, and the call restores £6,000.00. Day 4 has no price… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[4].prose` | Someone is short the contract you bought. Their account also starts at £6,000.00, with the same margin rules.… | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[4].canvas.state` | plotted values: [[8000, 7960, 7900, 7830, 7830, 7880]] | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[4].widget.answer` | key 7700 £: £7,700.00 | correct | Recomputed; right under the convention the item states |
| `screens[4].feedback.byKey.copied` | slip 4300: You gave the short your balance. A fall that hurts the long helps the short. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].feedback.byKey.start` | slip 6000: The short's account is marked to market too. Each evening it receives your loss. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].feedback.byKey.day` | slip 6700: That counts only day 3's gain. Add all three days. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].hints[0]` | Your loss is the short's gain. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[1]` | Over three days you lost $400 + 600 + 700$. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[2]` | $6{,}000 + 1{,}700 = 7{,}700$. | correct | Derivation or arithmetic step, checked |
| `screens[4].feedback.correct` | The short gained your £1,700.00: £7,700.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[4].feedback.generic` | Not quite right. Add your three losses to the short's £6,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[4].explain.text` | The short gains what you lose: £1,700.00 over three days, so £7,700.00. Your call money went, through the exc… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[5].prose` | A new week, the same rules: initial £6,000.00, maintenance £4,500.00. The future settles at 7,930, 7,840, 7,9… | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[5].canvas.state` | plotted values: [[8000, 7930, 7840, 7900, 7880]] | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[5].widget.answer` | key 1600 £: £1,600.00, after day 2 | correct | Recomputed; right under the convention the item states |
| `screens[5].feedback.byKey.end` | slip 0: You settled the week in one go, as the colleague did. Futures settle every evening, and day 2 closed … | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.maint` | slip 100: You topped up only to the maintenance level. A call restores the initial margin, £6,000.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.loss` | slip 1200: That is the week's net loss. The call depends on the balance on the worst evening. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.two` | slip 1700: Day 1 loses 70 points, £700.00, and day 2 loses 90, £900.00. Check day 2's balance again. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].hints[0]` | Settle the account evening by evening, not once at the end. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[1]` | After day 2 the balance is $6{,}000 - 700 - 900$. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[2]` | Day 2 closes at £4,400.00, below £4,500.00: a call of £1,600.00. Days 3 and 4 never drop below again. | correct | Derivation or arithmetic step, checked |
| `screens[5].feedback.correct` | Day 2 closes at £4,400.00, so the long pays £1,600.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[5].feedback.generic` | Not quite right. Work out the balance each evening and check it against £4,500.00. | correct | Derivation or arithmetic step, checked |
| `screens[5].explain.text` | Day 1 takes £700.00, leaving £5,300.00. Day 2 takes £900.00, leaving £4,400.00, below £4,500.00: a call for £… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[6].prose` | You settled each evening. For $n$ contracts at $m$ pounds a point, with settlement prices $F_t$: $$G_t = n\,m… | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[6].widget.options[credit]` | key: So no one can owe more than about one day's move, and a default costs little | correct | Recomputed; right under the convention the item states |
| `screens[6].widget.options[sooner].why` | wrong option 'To pay winners their profits sooner': Profits arriving sooner is a side effect. The point is th… | correct | Checked false under the item's premises; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[6].widget.options[price].why` | wrong option 'To keep the futures price equal to the spot price': Settlement moves cash; it does not set the … | correct | Checked false under the item's premises; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[6].widget.options[fees].why` | wrong option 'To charge a fee every day': Settlement is not a fee. The cash goes from one side's account to t… | correct | Checked false under the item's premises; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[6].feedback.correct` | Daily settlement caps what any side can owe at about one day's loss. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[6].feedback.generic` | Not quite right. Think about a forward whose loser owes a year of losses on one day. | correct | Derivation or arithmetic step, checked |
| `screens[6].explain.text` | A forward's loser may owe a year of losses on the delivery date, and might not pay. Daily settlement collects… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[7].prose` | The **basis** is the spot price minus the futures price. Four weeks before expiry the index is at 7,990 and t… | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[7].canvas.state` | plotted values: [[7990, 7985, 8005, 7995, 8012], [8010, 8000, 8015, 8000, 8012]] | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[7].widget.answer` | key 0 : 0 | correct | Recomputed; right under the convention the item states |
| `screens[7].feedback.byKey.stuck` | slip -20: That is today's basis, $7{,}990 - 8{,}010$. It shrinks as expiry nears. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].feedback.byKey.sign` | slip 20: The basis is spot minus future, and at expiry the two are equal. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].hints[0]` | What price does the future settle at on its last day? | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[1]` | At expiry the future is set from the index itself. | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[2]` | Spot minus a future equal to spot is 0. | correct | Derivation or arithmetic step, checked |
| `screens[7].feedback.correct` | The two meet at expiry: a basis of 0. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[7].feedback.generic` | Not quite right. On the last day the future settles at the index level. | correct | Derivation or arithmetic step, checked |
| `screens[7].explain.text` | Before expiry the gap is the cost of carry, and it shrinks as the time left shrinks. At expiry the future set… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[8].prose` | A pension fund holds £800,000.00 of shares that track the index. It hedges with a short position in 10 future… | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[8].canvas.state` | plotted values: [[8000, 8020, 8010, 8260]] | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[8].widget.answer` | key 25000 £: £25,000.00 | correct | Recomputed; right under the convention the item states |
| `screens[8].feedback.byKey.offset` | slip 0: The shares did gain about as much, but that gain is not cash. The margin call must be paid in cash, t… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.maint` | slip 10000: You topped up to the maintenance level. A call restores the initial margin, £60,000.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.one` | slip 2500: That is one contract's loss. The fund is short 10. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].hints[0]` | The fund is short, so a rally is a loss on the futures. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[1]` | The loss is $10 \times 250 \times \text{£}10.00$, taken from £60,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[2]` | The balance falls to £35,000.00, below £45,000.00: top up to £60,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[8].feedback.correct` | A £25,000.00 loss leaves £35,000.00, so the call is £25,000.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `screens[8].feedback.generic` | Not quite right. Find the futures loss, the new balance, and the gap to £60,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[8].explain.text` | The futures lose $10 \times 250 \times 10 = \text{£}25{,}000.00$, leaving £35,000.00, so the fund pays £25,00… | correct | Recomputed; Hull 10e Business Snapshot 3.2 (Metallgesellschaft, loss of 1.33 billion dollars) |
| `quiz[0].prose` | You are long 2 futures at £10.00 a point. Today's settlement price falls from 7,500 to 7,470. | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `quiz[0].widget.answer` | key -600 £: −£600.00 | correct | Recomputed; right under the convention the item states |
| `quiz[0].feedback.byKey.one` | slip -300: That is one contract. You hold 2. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.byKey.sign` | slip 600: You are long and the price fell, so it is a loss. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.byKey.points` | slip -30: That is the move in points. Multiply by £10.00 and by 2 contracts. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.correct` | $2 \times 10 \times (7{,}470 - 7{,}500) = -600$. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `quiz[0].feedback.generic` | Not quite right. Multiply contracts, pounds a point and the change in points. | correct | Derivation or arithmetic step, checked |
| `quiz[0].explain.text` | Each contract loses 30 points at £10.00, which is £300.00, and you hold 2. The account is debited £600.00 ton… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `quiz[1].prose` | Your initial margin is £6,000.00 and the maintenance margin £4,500.00. Your balance is £5,000.00. Tonight you… | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `quiz[1].widget.answer` | key 0 £: £0.00: £4,700.00 is above £4,500.00 | correct | Recomputed; right under the convention the item states |
| `quiz[1].feedback.byKey.initial` | slip 1300: You compared the balance with the initial margin. The call comes only below £4,500.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[1].feedback.byKey.loss` | slip 300: The loss is settled from your balance. A call comes only when the balance closes below maintenance. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[1].feedback.correct` | £4,700.00 is above the maintenance line: no call. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `quiz[1].feedback.generic` | Not quite right. Compare the new balance with the maintenance margin. | correct | Derivation or arithmetic step, checked |
| `quiz[1].explain.text` | The balance falls to £4,700.00, still above £4,500.00. No call is made; the margin between the two lines abso… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `quiz[2].prose` | Same rules: initial £6,000.00, maintenance £4,500.00. Your balance is £4,600.00, and tonight you lose £400.00. | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `quiz[2].widget.answer` | key 1800 £: £1,800.00 | correct | Recomputed; right under the convention the item states |
| `quiz[2].feedback.byKey.maint` | slip 300: You topped up to the maintenance line. A call restores the initial margin. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.byKey.loss` | slip 400: That replaces tonight's loss only. The call fills the whole gap to £6,000.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.byKey.none` | slip 0: £4,200.00 is below £4,500.00, so a call is due. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.correct` | $6{,}000 - 4{,}200 = 1{,}800$. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `quiz[2].feedback.generic` | Not quite right. Find the new balance, then the gap up to the initial margin. | correct | Derivation or arithmetic step, checked |
| `quiz[2].explain.text` | The balance closes at £4,200.00, below £4,500.00. You pay $6{,}000 - 4{,}200 = \text{£}1{,}800.00$ to restore… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `quiz[3].prose` | A month before expiry an index future trades 25 points above the index. | correct | Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `quiz[3].widget.options[zero]` | key: It shrinks to zero: the future settles at the index | correct | Recomputed; right under the convention the item states |
| `quiz[3].widget.options[stays].why` | wrong option 'It stays at 25 points': You kept today's gap. It is the cost of carry for a month, and that cos… | correct | Checked false under the item's premises; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `quiz[3].widget.options[grows].why` | wrong option 'It grows as traders bet on the index': Bets move both prices. At expiry the future is defined b… | correct | Checked false under the item's premises; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `quiz[3].widget.options[any].why` | wrong option 'It could end anywhere': At expiry the future and the index are the same thing, so arbitrage clo… | correct | Checked false under the item's premises; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `quiz[3].feedback.correct` | Convergence: the basis is 0 at expiry. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |
| `quiz[3].feedback.generic` | Not quite right. Ask how the future's final settlement price is set. | correct | Derivation or arithmetic step, checked |
| `quiz[3].explain.text` | The gap reflects the carry over the time left, which falls to nothing at expiry. The future's last settlement… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.3–2.4 (convergence, daily settlement and margins), §3.3 (basis), Business Snapshot 3.2 |

## l12-selling-what-you-do-not-own

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `summary.ideas[0]` | A short sale borrows a share, sells it, buys it back later and returns it: profit $P_0 - P_1$ less costs. | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `summary.ideas[1]` | The short pays the stock loan fee and every dividend the lender would have had. | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `summary.ideas[2]` | The best case is the share going to zero, a profit of $P_0 - C$. The loss has no limit, and recalls and squee… | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `summary.formula` | Short sale profit: \text{profit} = P_0 - P_1 - C; $C$ is the fee plus the dividends paid to the lender. | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `summary.trap` | The most a short can lose is not the sale price. The share can rise without limit, and you must buy it back. | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[0].prose` | You expect a share now at £50.00 to fall. You borrow one share from a broker and sell it for £50.00. A month … | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[0].widget.answer` | key 8 £: £8.00 | correct | Recomputed; right under the convention the item states |
| `screens[0].feedback.byKey.sign` | slip -8: You subtracted the wrong way round. Selling high and buying back low is a gain. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.buy` | slip 42: That is what you paid to buy back. Your profit is what you sold for minus that. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.sale` | slip 50: That is the cash from the sale. You still had to buy a share back to return it. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].hints[0]` | You received cash first and paid cash later. Which was more? | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[1]` | You sold for £50.00 and bought back for £42.00. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[2]` | $50 - 42 = 8$. | correct | Derivation or arithmetic step, checked |
| `screens[0].feedback.correct` | Sold at £50.00, bought back at £42.00: £8.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[0].feedback.generic` | Not quite right. Take what you paid to buy back from what you sold for. | correct | Derivation or arithmetic step, checked |
| `screens[0].explain.text` | You sold first at £50.00 and bought back later at £42.00, keeping £8.00. The line slopes down: you gain £1.00… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[1].prose` | Slide the buy-back price across the whole range, from £0.00 to £120.00. Watch the dot's label. Where does the… | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[1].widget.options[p0]` | key: £50.00, if the share goes to zero | correct | Recomputed; right under the convention the item states |
| `screens[1].widget.options[unlimited].why` | wrong option 'No limit: the further the share falls, the more you make': You mirrored the long's gains. A pri… | correct | Checked false under the item's premises; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[1].widget.options[eight].why` | wrong option '£8.00': That was one outcome. Slide the price to £0.00 and read the label. | correct | Checked false under the item's premises; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[1].feedback.correct` | At £0.00 you keep the whole £50.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[1].feedback.generic` | Not quite right. Slide the price to £0.00 and read the profit. | correct | Derivation or arithmetic step, checked |
| `screens[1].explain.text` | If the company fails and the share goes to £0.00, you buy back for nothing and keep the £50.00. That is the m… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[2].prose` | This is a **short sale**. Buying back is **covering** the short. The broker lends you the share for a **stock… | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[2].canvas.params.rows` | table: [["Lender", "a promise: one share back, and its dividends"], ["You", "£50.00 cash and a debt of one sh… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[2].widget.options[you]` | key: You do | correct | Recomputed; right under the convention the item states |
| `screens[2].widget.options[company].why` | wrong option 'The company does': The company pays whoever holds the share now: the buyer you sold to. The len… | correct | Checked false under the item's premises; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[2].widget.options[buyer].why` | wrong option 'The buyer does': The buyer owns the share outright and keeps the dividend. The buyer owes the l… | correct | Checked false under the item's premises; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[2].widget.options[nobody].why` | wrong option 'Nobody: the lender gave up the share': The lender only lent the share, and expects every divide… | correct | Checked false under the item's premises; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[2].feedback.byKey.company` | You assumed the company pays the lender. It pays only the holder, the buyer, so the lender's dividend comes f… | correct | Checked false under the item's premises; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[2].hints[0]` | The company pays one dividend per share. Who holds the share now? | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[1]` | The buyer holds it and receives the company's dividend. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[2]` | The lender still expects a dividend, and only you owe the lender anything. | correct | Derivation or arithmetic step, checked |
| `screens[2].feedback.correct` | You pay the dividend to the lender, out of your own pocket. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[2].feedback.generic` | Not quite right. Follow the share: who holds it, and who is owed? | correct | Derivation or arithmetic step, checked |
| `screens[2].explain.text` | The company pays the buyer, who now holds the share. The lender still expects its £0.60, and you owe it. So y… | correct | Hull 10e §5.2: the short pays dividends to the lender; the ex-dividend drop offsets it (BKM ch. 3 §3.9) |
| `screens[3].prose` | You short 1,000 shares at £50.00 for three months, then cover at £42.00. The stock loan fee is 3% a year on t… | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[3].widget.rows[1][1]` | cell key -375; The fee is 3% a year, but you are short for only a quarter: $50{,}000 \times 0.03 \times 0.25$. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[2][1]` | cell key -600; You owe the lender the dividend on all 1,000 shares: $1{,}000 \times \text{£}0.60$, paid out. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[3][1]` | cell key -42000; Buying back 1,000 shares at £42.00 costs £42,000.00, paid out. | correct | Recomputed; right under the convention the item states |
| `screens[3].widget.rows[4][1]` | cell key 7025; Add the column. Did you forget the dividend you pay the lender? | correct | Recomputed; right under the convention the item states |
| `screens[3].hints[0]` | The fee is a yearly rate charged for a quarter of a year. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[1]` | Fee: $50{,}000 \times 0.03 \times 0.25$. Dividend: $1{,}000 \times 0.60$. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[2]` | Fee −375, dividend −600, buy-back −42,000. Profit $50{,}000 - 375 - 600 - 42{,}000 = 7{,}025$. | correct | Derivation or arithmetic step, checked |
| `screens[3].feedback.correct` | £8,000.00 from the price, less £975.00 of costs: £7,025.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[3].feedback.generic` | Not quite right. Fill each cost, then add the column. | correct | Derivation or arithmetic step, checked |
| `screens[3].explain.text` | The fall earns $1{,}000 \times (50 - 42) = \text{£}8{,}000.00$. The fee takes £375.00 and the dividend £600.0… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[4].prose` | Same trade, same £375.00 fee and £600.00 of dividends. This time the share rises to £65.00 before you cover. | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[4].widget.answer` | key -15975 £: −£15,975.00 | correct | Recomputed; right under the convention the item states |
| `screens[4].feedback.byKey.no-costs` | slip -15000: You left out the fee and the dividend. They are due whatever the share does. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].feedback.byKey.costs-helped` | slip -14025: You took the costs off the loss. Costs always make a short worse. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].feedback.byKey.sign` | slip 15975: The share rose against you, so this is a loss: use a negative number. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[4].hints[0]` | Start from the price move, then take off the costs. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[1]` | The price move costs $1{,}000 \times (65 - 50) = 15{,}000$. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[2]` | $-15{,}000 - 375 - 600 = -15{,}975$. | correct | Derivation or arithmetic step, checked |
| `screens[4].feedback.correct` | $-15{,}000 - 975 = -15{,}975$. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[4].feedback.generic` | Not quite right. The price move loses money, and the costs add to the loss. | correct | Derivation or arithmetic step, checked |
| `screens[4].explain.text` | Buying back at £65.00 costs £15,000.00 more than the sale raised. The fee and the dividend add £975.00 to the… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[5].prose` | A colleague says a short mirrors buying. A buyer can lose at most £50.00 a share, so the colleague says you c… | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[5].widget.answer` | key 100 £: £100.00 | correct | Recomputed; right under the convention the item states |
| `screens[5].feedback.byKey.capped` | slip 50: You capped the loss at the sale price, as for a long. A short must buy back at any price, so the los… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.whole` | slip 150: You counted the whole buy-back price. The £50.00 from the sale offsets part of it. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.signed` | slip -100: The question asks for the size of the loss, as a positive number. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].hints[0]` | What must you pay to return the share? | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[1]` | You sold at £50.00 and must buy back at £150.00. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[2]` | $150 - 50 = 100$: the loss is £100.00, twice what the sale raised. | correct | Derivation or arithmetic step, checked |
| `screens[5].feedback.correct` | You buy back at £150.00 what you sold at £50.00: a £100.00 loss. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[5].feedback.generic` | Not quite right. The loss is the buy-back price minus the sale price. | correct | Derivation or arithmetic step, checked |
| `screens[5].explain.text` | You must buy back at £150.00 a share you sold for £50.00: a loss of £100.00. A price has no ceiling, so the l… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[6].prose` | You sold at $P_0$, covered at $P_1$, and paid fees and dividends $C$: $$\text{profit} = P_0 - P_1 - C.$$ The … | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[6].widget.options[right]` | key: −£6.50 | correct | Recomputed; right under the convention the item states |
| `screens[6].widget.options[helped].why` | wrong option '−£5.50': You took the costs off the loss. Costs always count against you: $30 - 36 - 0.5$. | correct | Checked false under the item's premises; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[6].widget.options[sign].why` | wrong option '£6.50': You subtracted the wrong way round. Covering above the sale price is a loss. | correct | Checked false under the item's premises; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[6].feedback.correct` | $30 - 36 - 0.50 = -6.50$. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[6].feedback.generic` | Not quite right. Put the numbers into $P_0 - P_1 - C$. | correct | Derivation or arithmetic step, checked |
| `screens[6].explain.text` | $P_0 - P_1 - C = 30 - 36 - 0.50 = -6.50$. The price move costs £6.00 and the costs add £0.50. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[7].prose` | Before you short, your broker must **locate** a share to borrow, and the lender can **recall** it at any time… | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[7].canvas.state` | plotted values: {"si": 12, "vol": 2} | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[7].widget.answer` | key 6 days: 6 days | correct | Recomputed; right under the convention the item states |
| `screens[7].feedback.byKey.inverted` | slip 0.1667: You divided volume by short interest. Days to cover is short interest over daily volume. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].feedback.byKey.product` | slip 24: You multiplied. The shorts need 12 million shares at 2 million a day. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].feedback.byKey.diff` | slip 10: You subtracted. Divide the short interest by the daily volume. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].hints[0]` | Every short must buy back 12 million shares in total. | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[1]` | The market trades about 2 million a day. | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[2]` | $12 / 2 = 6$ days. | correct | Derivation or arithmetic step, checked |
| `screens[7].feedback.correct` | $12 / 2 = 6$ days to cover. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[7].feedback.generic` | Not quite right. Divide the shares sold short by the shares traded a day. | correct | Derivation or arithmetic step, checked |
| `screens[7].explain.text` | Shorts would need about 6 days of the market's whole volume to cover. If the price jumps, their rush to buy p… | correct | Hull §5.2; days to cover 12/2. GameStop: short interest about 140% of float (SEC staff report, Oct 2021); close 17.25 on 4 Jan to 347.51 on 27 Jan 2021, so more than tenfold |
| `screens[8].prose` | A **pairs trade**: long £100,000.00 of one bank's shares, short £100,000.00 of a rival's. Bad news hits the w… | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[8].canvas.params.rows` | table: [["Long bank A", "100,000.00", "-8%"], ["Short bank B", "-100,000.00", "-12%"], ["Net exposure", "0.00… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[8].widget.answer` | key 4000 £: £4,000.00 | correct | Recomputed; right under the convention the item states |
| `screens[8].feedback.byKey.both-long` | slip -20000: You treated both legs as long. The short leg gains when bank B falls. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.sign` | slip -4000: You swapped the legs. The short is in bank B, which fell further. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.zero` | slip 0: Zero net exposure cancels the sector's common move, not the gap between the two shares. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].hints[0]` | Work out each leg's profit separately. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[1]` | The long loses 8% of £100,000.00; the short gains 12% of £100,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[2]` | $-8{,}000 + 12{,}000 = 4{,}000$. | correct | Derivation or arithmetic step, checked |
| `screens[8].feedback.correct` | The long loses £8,000.00, the short gains £12,000.00: £4,000.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[8].feedback.generic` | Not quite right. A short gains when its share falls. | correct | Derivation or arithmetic step, checked |
| `screens[8].explain.text` | The long loses £8,000.00 and the short gains £12,000.00, so the pair makes £4,000.00. With zero net exposure,… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[9].prose` | A fund shorts 1,000 shares at £100.00, £100,000.00 in all. The stock is hard to borrow, and the fee for the p… | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[9].widget.answer` | key -52000 £: −£52,000.00 | correct | Recomputed; right under the convention the item states |
| `screens[9].feedback.byKey.no-fee` | slip -50000: You left out the £2,000.00 fee. It is due whatever the share does. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[9].feedback.byKey.whole` | slip -150000: You counted the whole buy-back as lost. The £100,000.00 from the sale pays for most of it. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[9].feedback.byKey.capped` | slip -100000: You capped the loss at the sale value. The loss is set by the buy-back price, which has no ceil… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[9].feedback.byKey.sign` | slip 52000: The share rose against the short, so this is a loss. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[9].hints[0]` | The fund sold for £100,000.00. What does buying back cost? | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[1]` | Buying back 1,000 shares at £150.00 costs £150,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[2]` | $100{,}000 - 150{,}000 - 2{,}000 = -52{,}000$. | correct | Derivation or arithmetic step, checked |
| `screens[9].feedback.correct` | A £50,000.00 loss on the price plus the £2,000.00 fee. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `screens[9].feedback.generic` | Not quite right. Sale proceeds minus the buy-back cost minus the fee. | correct | Derivation or arithmetic step, checked |
| `screens[9].explain.text` | Covering costs £150,000.00 against £100,000.00 raised, a £50,000.00 loss, and the fee adds £2,000.00. The rec… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `quiz[0].prose` | You short 200 shares at £25.00 and cover at £20.00. The stock loan fee for the period is £15.00, and no divid… | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `quiz[0].widget.answer` | key 985 £: £985.00 | correct | Recomputed; right under the convention the item states |
| `quiz[0].feedback.byKey.no-fee` | slip 1000: You left out the £15.00 fee. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.byKey.per` | slip 5: That is the gain per share. You shorted 200. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.byKey.plus` | slip 1015: You added the fee. It is a cost of borrowing the shares. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.correct` | $200 \times 5 - 15 = 985$. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `quiz[0].feedback.generic` | Not quite right. Find the gain on the price, then take off the fee. | correct | Derivation or arithmetic step, checked |
| `quiz[0].explain.text` | The price fall earns $200 \times (25 - 20) = \text{£}1{,}000.00$, and the fee takes £15.00. The profit is £98… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `quiz[1].prose` | You short a share at £40.00. | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `quiz[1].widget.options[none]` | key: There is no limit | correct | Recomputed; right under the convention the item states |
| `quiz[1].widget.options[forty].why` | wrong option '£40.00': You treated the short like a purchase. A buyer can lose £40.00 at most; you must buy b… | correct | Checked false under the item's premises; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `quiz[1].widget.options[eighty].why` | wrong option '£80.00, if the share doubles': Doubling is one outcome. The share can rise further, and your lo… | correct | Checked false under the item's premises; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `quiz[1].widget.options[fees].why` | wrong option 'Only the stock loan fee': The fee is a cost, but the main risk is the price rising. | correct | Checked false under the item's premises; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `quiz[1].feedback.correct` | A share's price has no ceiling, so neither has the loss. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `quiz[1].feedback.generic` | Not quite right. Ask what you pay to buy back if the share keeps rising. | correct | Derivation or arithmetic step, checked |
| `quiz[1].explain.text` | The loss is the buy-back price minus £40.00, plus costs. The buy-back price can rise without limit, so the lo… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `quiz[2].prose` | You short 500 shares at £40.00. While you are short the company pays a £1.00 dividend per share. The fee is £… | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `quiz[2].widget.answer` | key -550 £: −£550.00 | correct | Recomputed; right under the convention the item states |
| `quiz[2].feedback.byKey.no-div` | slip -50: You forgot the dividend. You owe the lender £1.00 on each of the 500 shares. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.byKey.div-gain` | slip 450: You treated the dividend as income. The buyer receives it; you pay the lender the same amount. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.byKey.zero` | slip 0: The price is unchanged, but the fee and the dividend are still due. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.byKey.sign` | slip 550: You pay £500.00 of dividends and the £50.00 fee while the price earns nothing, so the profit is −£5… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.correct` | No price gain, minus £500.00 of dividends and £50.00 of fee. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `quiz[2].feedback.generic` | Not quite right. The price did not move, so only the costs remain. | correct | Derivation or arithmetic step, checked |
| `quiz[2].explain.text` | The price is where you sold it, so the move earns nothing. You pay the lender $500 \times \text{£}1.00 = \tex… | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `quiz[3].prose` | You short 1,000 shares at £12.00, with no fees or dividends. The company fails and its shares become worthles… | correct | Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `quiz[3].widget.answer` | key 12000 £: £12,000.00 | correct | Recomputed; right under the convention the item states |
| `quiz[3].feedback.byKey.per` | slip 12: That is per share. You shorted 1,000. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[3].feedback.byKey.double` | slip 24000: You can keep only what the sale raised. The share cannot go below £0.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[3].feedback.byKey.zero` | slip 0: A worthless share is the short's best case: buying back costs nothing. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[3].feedback.correct` | You keep the whole £12,000.00 from the sale. | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |
| `quiz[3].feedback.generic` | Not quite right. Buying back at £0.00 costs nothing. | correct | Derivation or arithmetic step, checked |
| `quiz[3].explain.text` | You sold for £12,000.00 and buy back for nothing. That is the most a short can make: the sale value $P_0$ on … | correct | Recomputed in the concepts script or by hand; Hull 10e §5.2 (short selling); BKM ch. 3 §3.9 |

## l13-leverage

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `summary.ideas[0]` | Leverage $L$ is position over equity. Borrowing $(L - 1)$ times your equity multiplies every return by $L$ an… | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `summary.ideas[1]` | Gains and losses scale alike, and the interest is due either way. Volatility scales with $L$ too. | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `summary.ideas[2]` | A fall of $1/L$ wipes out the equity; a maintenance margin forces a sale before that. | imprecise | Finding 3: true only with no interest; from $R_E=-1$, the fall is $(1-(L-1)r)/L$ |
| `summary.formula` | Return on equity: R_E = L R_A - (L - 1) r; At $L = 1$ it is $R_A$. Every line passes through $(r, r)$. | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `summary.trap` | Leverage is not more return. It is a steeper line: bigger losses as well as gains, less the interest on the b… | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[0].prose` | You have £10,000.00. You borrow another £10,000.00 at 5% a year and buy £20,000.00 of shares. A year later th… | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[0].canvas.state` | plotted values: {"pos": 20000, "loan": 10000, "eq": 10000} | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[0].widget.answer` | key 0.15 %: 15% | correct | Recomputed; right under the convention the item states |
| `screens[0].feedback.byKey.unlev` | slip 0.1: That is the shares' return. Half of the £20,000.00 was borrowed, so your own money did better. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.no-int` | slip 0.2: You doubled the shares' return but forgot the £500.00 interest on the loan. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].feedback.byKey.int-all` | slip 0.05: You subtracted the 5% rate from the 10% return. The interest is paid on the borrowed half only, an… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[0].hints[0]` | Work out what the shares are worth and what you owe a year later. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[1]` | Shares: £22,000.00. Loan with interest: £10,500.00. | correct | Derivation or arithmetic step, checked |
| `screens[0].hints[2]` | You keep $22{,}000 - 10{,}500 = 11{,}500$, a gain of £1,500.00 on £10,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[0].feedback.correct` | £11,500.00 back on £10,000.00: 15%. | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[0].feedback.generic` | Not quite right. Take the loan and its interest off the shares' value, then compare with £10,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[0].explain.text` | The shares are worth £22,000.00 and you owe £10,500.00, leaving £11,500.00: a 15% return. You earned 10% on £… | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[1].prose` | The solid line is your return for every return on the shares, borrowing at 5%. The dashed line is buying with… | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[1].canvas.derive` | formulas: P.y=L * 0.1 - (L - 1) * r | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[1].widget.options[pivot]` | key: It steepens, turning about the point where the shares earn the 5% you pay | correct | Recomputed; right under the convention the item states |
| `screens[1].widget.options[up].why` | wrong option 'It moves up: more return at every share return': You looked only at the right-hand side. Left o… | correct | Checked false under the item's premises; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[1].widget.options[parallel].why` | wrong option 'It stays parallel to the dashed line': The slope is the leverage. Each 1% on the shares moves y… | correct | Checked false under the item's premises; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[1].widget.options[flat].why` | wrong option 'It flattens': You read the slider backwards. Higher leverage makes your equity swing more, so t… | correct | Checked false under the item's premises; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[1].feedback.correct` | Steeper, about the point $(0.05, 0.05)$. | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[1].feedback.generic` | Not quite right. Compare the caption's two numbers at $L = 1$ and at $L = 5$. | correct | Derivation or arithmetic step, checked |
| `screens[1].explain.text` | At $L = 4$, a 10% rise gives 25%, but a 10% fall gives −55%. Every line passes through $(0.05, 0.05)$: when t… | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[2].prose` | **Leverage** $L$ is the position divided by your own money, your **equity**. Your £20,000.00 of shares on £10… | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[2].canvas.params.functions` | curves: x; L*x - (L-1)*r | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[2].widget.answer` | key 3 : 3 | correct | Recomputed; right under the convention the item states |
| `screens[2].feedback.byKey.borrowed` | slip 2: You divided the borrowing, £100,000.00, by the equity. Leverage uses the whole position. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].feedback.byKey.inverted` | slip 0.3333: You divided equity by the position. Leverage is position over equity. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].feedback.byKey.loan` | slip 100000: That is the amount borrowed. Leverage is a ratio: position over equity. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[2].hints[0]` | Leverage compares the position with the equity, not with the loan. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[1]` | Position £150,000.00, equity £50,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[2].hints[2]` | $L = 150{,}000 / 50{,}000 = 3$. | correct | Derivation or arithmetic step, checked |
| `screens[2].feedback.correct` | $150{,}000 / 50{,}000 = 3$. | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[2].feedback.generic` | Not quite right. Divide the position by the equity. | correct | Derivation or arithmetic step, checked |
| `screens[2].explain.text` | $L = \tfrac{150{,}000}{50{,}000} = 3$, with $(L - 1) \times 50{,}000 = \text{£}100{,}000.00$ borrowed. Each 1… | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[3].prose` | Back to $L = 2$, borrowing at 5% a year. This year the shares fall 30%. | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[3].canvas.params.functions` | curves: x; L*x - (L-1)*r | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[3].widget.answer` | key -0.65 %: −65% | correct | Recomputed; right under the convention the item states |
| `screens[3].feedback.byKey.no-int` | slip -0.6: You doubled the fall but forgot the interest. The loan charges 5% whatever the shares do. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].feedback.byKey.unlev` | slip -0.3: That is the shares' fall. On borrowed money your equity takes twice the hit. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].feedback.byKey.int-helps` | slip -0.55: You added the interest back. Interest is a cost, so it deepens the loss. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].feedback.byKey.sign` | slip 0.65: £3,500.00 is left of your £10,000.00, so your equity has fallen by 65%. A positive 65% books the l… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[3].hints[0]` | The position loses twice the shares' fall. What else do you owe? | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[1]` | The position loses 60% of your equity, and the interest is 5% of your equity. | correct | Derivation or arithmetic step, checked |
| `screens[3].hints[2]` | $2 \times (-0.30) - 1 \times 0.05 = -0.65$. | correct | Derivation or arithmetic step, checked |
| `screens[3].feedback.correct` | $2 \times (-0.30) - 0.05 = -0.65$: you lose 65%. | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[3].feedback.generic` | Not quite right. Double the fall, then pay the interest on the borrowed half. | correct | Derivation or arithmetic step, checked |
| `screens[3].explain.text` | £20,000.00 of shares falls to £14,000.00, and you owe £10,500.00. That leaves £3,500.00 of your £10,000.00: −… | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[4].prose` | Now $L = 4$, and to keep things simple the loan charges no interest. Your equity is gone when $R_E = -1$, the… | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[4].canvas.derive` | formulas: | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[4].widget.points` | key {"on": "eq", "x": -0.25} | correct | Recomputed; right under the convention the item states |
| `screens[4].feedback.byKey.full` | You waited for the asset to lose everything. With $L = 4$ your equity is gone long before. | correct | Checked false under the item's premises; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[4].feedback.byKey.three-quarters` | You took $1 - 1/L$. The fall that wipes you out is $1/L$, a quarter. | correct | Checked false under the item's premises; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[4].feedback.byKey.P` | The point is not yet where the solid line crosses $R_E = -1$. | correct | Checked false under the item's premises; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[4].hints[0]` | Each 1% the asset falls costs your equity 4%. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[1]` | You need $4 \times R_A = -1$. | correct | Derivation or arithmetic step, checked |
| `screens[4].hints[2]` | $R_A = -\tfrac{1}{4} = -0.25$: drag to −25%. | correct | Derivation or arithmetic step, checked |
| `screens[4].feedback.correct` | A 25% fall, $1/L$, wipes out the equity. | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[4].feedback.generic` | Not quite right. Find where the solid line meets the dashed line. | correct | Derivation or arithmetic step, checked |
| `screens[4].explain.text` | At $L = 4$ each 1% the asset falls costs your equity 4%, so a 25% fall costs 100%. In general a fall of $\tfr… | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[5].prose` | A fund holds an index at 3 times its equity, borrowing the rest at 5% a year. The index returns 8% this year.… | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[5].canvas.params.functions` | curves: x; L*x - (L-1)*r | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[5].widget.answer` | key 0.14 %: 14% | correct | Recomputed; right under the convention the item states |
| `screens[5].feedback.byKey.no-int` | slip 0.24: You tripled the index return and stopped. The fund borrowed twice its equity and pays 5% on it: 10… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.int-once` | slip 0.19: You charged interest on one unit of equity. The fund borrowed two. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].feedback.byKey.int-three` | slip 0.09: You charged interest on the whole position. The fund's own third is not borrowed. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[5].hints[0]` | For each £1.00 of equity, how much does the fund borrow? | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[1]` | It borrows £2.00 for each £1.00, and pays 5% on all of it. | correct | Derivation or arithmetic step, checked |
| `screens[5].hints[2]` | $3 \times 0.08 - 2 \times 0.05 = 0.14$. | correct | Derivation or arithmetic step, checked |
| `screens[5].feedback.correct` | $3 \times 0.08 - 2 \times 0.05 = 0.14$: 14%, not 24%. | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[5].feedback.generic` | Not quite right. Triple the index return, then pay interest on the borrowing. | correct | Derivation or arithmetic step, checked |
| `screens[5].explain.text` | $R_E = 3 \times 0.08 - 2 \times 0.05 = 0.14$. Had the index fallen 8%, the fund would lose $0.24 + 0.10 = 0.3… | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[6].prose` | Now in general. You put in equity $E$ and hold a position $L$ times as large. The position returns $R_A$, and… | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[6].widget.lines[d1]` | The position is $LE$, so you borrow $(L - 1)E$: leverage is position over equity | correct | Derivation or arithmetic step, checked |
| `screens[6].widget.lines[d2]` | At the end the position is worth $LE(1 + R_A)$ and you owe $(L - 1)E(1 + r)$: the asset's return and the loan… | correct | Derivation or arithmetic step, checked |
| `screens[6].widget.lines[d3]` | Your equity is then $LE(1 + R_A) - (L - 1)E(1 + r)$: what is left after repaying | correct | Derivation or arithmetic step, checked |
| `screens[6].widget.lines[d4]` | $R_E = L(1 + R_A) - (L - 1)(1 + r) - 1$: divide by $E$ and subtract 1 | correct | Derivation or arithmetic step, checked |
| `screens[6].widget.lines[d5]` | $R_E = L R_A - (L - 1) r$: the constants cancel, since $L - (L - 1) - 1 = 0$ | correct | Derivation or arithmetic step, checked |
| `screens[6].feedback.byKey.d4` | The return needs the end equity first: the line that subtracts the loan. | correct | Derivation or arithmetic step, checked |
| `screens[6].feedback.byKey.d5` | The simple form comes last, after dividing by $E$. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[0]` | Start from how much you borrow. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[1]` | Value everything at the end before you turn it into a return. | correct | Derivation or arithmetic step, checked |
| `screens[6].hints[2]` | Borrowing, end values, equity left, divide by $E$, simplify. | correct | Derivation or arithmetic step, checked |
| `screens[6].feedback.correct` | Borrowing, end values, equity, return, simplify. | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[6].feedback.generic` | Not quite right. Build the end-of-period equity before dividing by $E$. | correct | Derivation or arithmetic step, checked |
| `screens[6].explain.text` | Check with the first screen: $L = 2$, $R_A = 0.10$, $r = 0.05$ gives $0.20 - 0.05 = 0.15$. The slope in $R_A$… | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[7].prose` | You buy £20,000.00 of shares with £10,000.00 of your own and a £10,000.00 **margin loan** from your broker. T… | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[7].widget.answer` | key 13333.33 £: £13,333.33: $10{,}000 / 0.75$ | correct | Recomputed; right under the convention the item states |
| `screens[7].feedback.byKey.orig` | slip 15000: You took 25% of the original £20,000.00. The rule uses the position's value now, $V$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].feedback.byKey.zero` | slip 10000: That is where your equity reaches zero. The broker steps in earlier, at 25%. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].feedback.byKey.pct` | slip 12500: You set the loan equal to 80% of the position. The loan is 75% of it at the trigger. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[7].hints[0]` | Your equity is the position's value minus the £10,000.00 loan. | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[1]` | The rule is $V - 10{,}000 \ge 0.25\,V$. | correct | Derivation or arithmetic step, checked |
| `screens[7].hints[2]` | $0.75\,V = 10{,}000$, so $V = 13{,}333.33$. | correct | Derivation or arithmetic step, checked |
| `screens[7].feedback.correct` | $V - 10{,}000 = 0.25V$ gives $V = 13{,}333.33$. | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[7].feedback.generic` | Not quite right. Write equity as $V - 10{,}000$ and set it equal to 25% of $V$. | correct | Derivation or arithmetic step, checked |
| `screens[7].explain.text` | Equity is $V - 10{,}000$, and the rule needs $V - 10{,}000 \ge 0.25V$, so $V \ge 13{,}333.33$. That is a fall… | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[8].prose` | A £100,000.00 account holds £300,000.00 of shares: 3 times leverage, with £200,000.00 borrowed at 6% a year. … | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[8].canvas.params.functions` | curves: x; L*x - (L-1)*r | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[8].widget.answer` | key 0.63 %: 63%: £60,000.00 lost and £3,000.00 of interest | correct | Recomputed; right under the convention the item states |
| `screens[8].feedback.byKey.no-int` | slip 0.6: You tripled the fall but forgot three months of interest on £200,000.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.unlev` | slip 0.2: That is the market's fall. The account holds three times its equity. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].feedback.byKey.year` | slip 0.72: You charged a whole year's interest. The period is three months. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[8].hints[0]` | Find the loss on the shares and the interest for three months. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[1]` | Shares lose $0.2 \times 300{,}000$; interest is $200{,}000 \times 0.06 \times 0.25$. | correct | Derivation or arithmetic step, checked |
| `screens[8].hints[2]` | $60{,}000 + 3{,}000 = 63{,}000$ off £100,000.00: 63%. | correct | Derivation or arithmetic step, checked |
| `screens[8].feedback.correct` | £63,000.00 off £100,000.00: equity falls 63%. | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[8].feedback.generic` | Not quite right. Add the share loss and three months' interest, then compare with £100,000.00. | correct | Derivation or arithmetic step, checked |
| `screens[8].explain.text` | The shares lose $0.2 \times 300{,}000 = \text{£}60{,}000.00$ and interest costs £3,000.00, leaving £37,000.00… | correct | Recomputed; sd of $R_E$ at $L=3$ is 0.45 in simulation; $37{,}000/240{,}000=15.4\%$ |
| `screens[9].prose` | A hedge fund has £100m of capital. It holds £180m of shares long and £120m short. Its **gross exposure** adds… | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[9].canvas.state` | plotted values: {"cap": 100, "long": 180, "short": 120} | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[9].widget.answer` | key 3 : 3: £300m over £100m | correct | Recomputed; right under the convention the item states |
| `screens[9].feedback.byKey.net` | slip 0.6: That is net leverage, $\tfrac{180 - 120}{100}$. Gross adds the two sides. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[9].feedback.byKey.long` | slip 1.8: You counted only the long side. A short position can lose money too. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[9].feedback.byKey.total` | slip 300: That is gross exposure in millions. Divide by the £100m of capital. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `screens[9].hints[0]` | Gross exposure counts both sides as positive. | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[1]` | Gross is $180 + 120$ million. | correct | Derivation or arithmetic step, checked |
| `screens[9].hints[2]` | $300 / 100 = 3$. | correct | Derivation or arithmetic step, checked |
| `screens[9].feedback.correct` | $\tfrac{180 + 120}{100} = 3$. | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `screens[9].feedback.generic` | Not quite right. Add the long and the short side, then divide by capital. | correct | Derivation or arithmetic step, checked |
| `screens[9].explain.text` | Gross exposure is £300m, three times capital; net is £60m, 0.6 times. Net says which way the fund leans on th… | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `quiz[0].prose` | You buy shares with your own money only, so $L = 1$. The shares return 7% in a year, and the borrowing rate i… | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `quiz[0].widget.answer` | key 0.07 %: 7% | correct | Recomputed; right under the convention the item states |
| `quiz[0].feedback.byKey.minus` | slip 0.02: You charged interest. At $L = 1$ you borrow nothing, so no interest is due. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.byKey.plus` | slip 0.12: You added the rate. The rate matters only on borrowed money, and there is none. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[0].feedback.correct` | At $L = 1$, $R_E = R_A = 7\%$. | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `quiz[0].feedback.generic` | Not quite right. With $L = 1$ nothing is borrowed. | correct | Derivation or arithmetic step, checked |
| `quiz[0].explain.text` | $R_E = 1 \times 0.07 - 0 \times 0.05 = 0.07$. Unlevered, your return is the asset's return. | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `quiz[1].prose` | A leveraged account loses 50% of its equity in a bad year. | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `quiz[1].widget.answer` | key 1.0 %: 100% | correct | Recomputed; right under the convention the item states |
| `quiz[1].feedback.byKey.same` | slip 0.5: A 50% gain on £50.00 is only £25.00, back to £75.00. The gain is on a smaller base. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[1].feedback.byKey.quarter` | slip 0.25: That would take £50.00 to £62.50. You need to double it. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[1].feedback.correct` | Half the money must double: a 100% gain. | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `quiz[1].feedback.generic` | Not quite right. Start from £100.00, lose half, and find the gain back to £100.00. | correct | Derivation or arithmetic step, checked |
| `quiz[1].explain.text` | £100.00 falls to £50.00, and only a 100% gain returns it to £100.00. In log returns the two are symmetric: $\… | correct | Derivation; Monte Carlo, 1,000,000 years at 15% volatility: P(lose half) 0.00007 at L=1 against 0.088 at L=3 (script) |
| `quiz[2].prose` | A position has $L = 2$, borrowing at 4% a year. The asset returns 12% in the year. | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `quiz[2].widget.answer` | key 0.2 %: 20% | correct | Recomputed; right under the convention the item states |
| `quiz[2].feedback.byKey.no-int` | slip 0.24: You doubled the return and forgot the interest on the borrowed half. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.byKey.double-int` | slip 0.16: You charged interest on the whole position. Only half is borrowed. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.byKey.unlev` | slip 0.12: That is the asset's return. With $L = 2$ your equity moves twice as much. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `quiz[2].feedback.correct` | $2 \times 0.12 - 1 \times 0.04 = 0.20$. | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `quiz[2].feedback.generic` | Not quite right. Use $R_E = L R_A - (L - 1) r$. | correct | Derivation or arithmetic step, checked |
| `quiz[2].explain.text` | $R_E = 2 \times 0.12 - 1 \times 0.04 = 0.20$. You earn 12% on twice your money and pay 4% on the borrowed hal… | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `quiz[3].prose` | A position has $L = 5$. Ignore interest. | correct | BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `quiz[3].widget.options[fifth]` | key: 20% | correct | Recomputed; right under the convention the item states |
| `quiz[3].widget.options[half].why` | wrong option '50%': You may have halved. With $L = 5$ each 1% on the asset is 5% on equity, so 20% is enough. | correct | Checked false under the item's premises; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `quiz[3].widget.options[eighty].why` | wrong option '80%': You took $1 - 1/L$. The equity is gone after a fall of $1/L$. | correct | Checked false under the item's premises; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `quiz[3].widget.options[all].why` | wrong option '100%': That is the unlevered case. Borrowed money brings the wipe-out much closer. | correct | Checked false under the item's premises; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `quiz[3].feedback.correct` | $1/L = 1/5$: a 20% fall. | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |
| `quiz[3].feedback.generic` | Not quite right. Find the fall that, times 5, is 100%. | correct | Derivation or arithmetic step, checked |
| `quiz[3].explain.text` | Each 1% on the asset moves the equity 5%. A 20% fall costs $5 \times 20\% = 100\%$ of the equity. | correct | Recomputed in the concepts script or by hand; BKM ch. 3 §3.8–3.9 (buying on margin, short margin); derivation of $R_E = LR_A-(L-1)r$ |

## review-1

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | £5,000.00 is invested at 3% a year, compounded yearly, for 6 years. | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[0].widget.answer` | key 5970.26 £: £5,970.26: $5000 \times 1.03^6$. | correct | Recomputed; right under the convention the item states |
| `items[0].feedback.byKey.simple` | slip 5900: £5,900.00 adds 3% of £5,000.00 six times: simple interest. Each year's 3% is on a larger balance. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[0].feedback.byKey.interest` | slip 970.26: That is the interest alone. Add the £5,000.00 invested. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[0].feedback.correct` | $5000 \times 1.03^6 = 5970.26$. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[0].feedback.generic` | Not quite right. Multiply by 1.03 once for each of the 6 years. | correct | Derivation or arithmetic step, checked |
| `items[0].explain.text` | Six years multiply by $1.03^6 = 1.194052$. So £5,000.00 becomes £5,970.26. Simple interest would give £5,900.… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[1].prose` | A payment of £2,500.00 is due in 4 years. The rate is 6% a year, compounded. | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[1].widget.answer` | key 1980.23 £: £1,980.23: $2500 / 1.06^4$. | correct | Recomputed; right under the convention the item states |
| `items[1].feedback.byKey.simple` | slip 2016.13: You divided by $1 + 0.06 \times 4 = 1.24$. Four compounded years back divide by $1.06^4 = 1.262… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[1].feedback.byKey.once` | slip 2358.49: You discounted for one year. The payment is four years away. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[1].feedback.correct` | $2500 / 1.06^4 = 1980.23$. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[1].feedback.generic` | Not quite right. Divide by $1.06^4$. | correct | Derivation or arithmetic step, checked |
| `items[1].explain.text` | Four years back divide by $1.06^4 = 1.262477$. So £2,500.00 in 4 years is worth £1,980.23 today. Check: $1980… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[2].prose` | A loan charges 9% a year nominal, compounded monthly. | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[2].widget.answer` | key 0.093807 %: 9.38%: $(1 + \tfrac{0.09}{12})^{12} - 1$. | correct | Recomputed; right under the convention the item states |
| `items[2].feedback.byKey.nominal` | slip 0.09: 9% is the nominal rate. Monthly compounding charges interest on interest within the year. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[2].feedback.byKey.month` | slip 0.0075: 0.75% is one month's charge. The effective rate covers the year. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[2].feedback.correct` | $1.0075^{12} - 1 = 0.0938$, so 9.38%. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[2].feedback.generic` | Not quite right. Compound $1 + \tfrac{0.09}{12}$ over 12 months, then take away 1. | correct | Derivation or arithmetic step, checked |
| `items[2].explain.text` | Each month charges $0.09/12 = 0.0075$. Twelve months give $1.0075^{12} = 1.0938$. So the loan costs 9.38% eff… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[3].prose` | A project costs £800.00 today and pays £300.00 at the end of each of the next 3 years. The rate is 6%. | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[3].widget.answer` | key 1.9 £: £1.90: $300(\tfrac{1}{1.06} + \tfrac{1}{1.06^2} + \tfrac{1}{1.06^3}) - 800$. | correct | Recomputed; right under the convention the item states |
| `items[3].feedback.byKey.undisc` | slip 100: You added the cash without discounting. Each £300.00 is worth less the later it comes. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[3].feedback.byKey.no-cost` | slip 801.9: That is the value of the payments. Take away the £800.00 cost. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[3].feedback.correct` | NPV £1.90: positive, but only just. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[3].feedback.generic` | Not quite right. Discount each £300.00, add them, then take away £800.00. | correct | Derivation or arithmetic step, checked |
| `items[3].explain.text` | The three payments are worth £283.02, £267.00 and £251.89 today, £801.90 in all. Take away £800.00: NPV £1.90… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[4].prose` | An index fund is expected to grow 6% a year, compounded. | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[4].widget.options[right]` | key: About 12 years | correct | Recomputed; right under the convention the item states |
| `items[4].widget.options[simple].why` | wrong option 'About 16.7 years': That is simple growth, $100 \div 6$. Compounding doubles sooner. | correct | Checked false under the item's premises; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[4].widget.options[six].why` | wrong option 'About 6 years': You read the rate as the doubling time. Divide 72 by 6. | correct | Checked false under the item's premises; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[4].widget.options[half].why` | wrong option 'About 3 years': Doubling at 6% a year takes much longer. Divide 72 by 6. | correct | Checked false under the item's premises; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[4].feedback.correct` | $72 \div 6 = 12$ years, close to the exact 11.90. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[4].feedback.generic` | Not quite right. Use the rule of 72. | correct | Derivation or arithmetic step, checked |
| `items[4].explain.text` | The rule of 72 gives $72 \div 6 = 12$ years. Exactly, $\ln 2 / \ln 1.06 = 11.90$ years. Simple growth would t… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[5].prose` | £10,000.00 is due in 2 years. The discount rate is 6% a year nominal, compounded monthly. | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[5].widget.answer` | key 8871.86 £: £8,871.86: $10000 / 1.005^{24}$. | correct | Recomputed; right under the convention the item states |
| `items[5].feedback.byKey.annual` | slip 8899.96: You discounted at 6% compounded yearly. Monthly compounding means 24 steps of $1.005$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[5].feedback.byKey.simple` | slip 8928.57: You divided by $1 + 0.06 \times 2 = 1.12$, simple interest. Compound back over 24 months. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[5].feedback.correct` | $10000 / 1.005^{24} = 8871.86$. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[5].feedback.generic` | Not quite right. Discount by $1.005$ for each of the 24 months. | correct | Derivation or arithmetic step, checked |
| `items[5].explain.text` | Each month back divides by $1 + \tfrac{0.06}{12} = 1.005$, and there are 24 months. So $10000 / 1.005^{24} = … | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[6].prose` | A fund targets 8% a year effective. Its manager wants the matching quarterly return. | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[6].widget.answer` | key 0.019427 %: 1.94%: $1.08^{1/4} - 1$. | correct | Recomputed; right under the convention the item states |
| `items[6].feedback.byKey.div` | slip 0.02: You divided 8% by 4. Four quarters of 2% compound to 8.24%, too much. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[6].feedback.correct` | $1.08^{1/4} - 1 = 0.0194$. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[6].feedback.generic` | Not quite right. Solve $(1 + x)^4 = 1.08$. | correct | Derivation or arithmetic step, checked |
| `items[6].explain.text` | We need $(1 + x)^4 = 1.08$, so $x = 1.08^{1/4} - 1 = 0.0194$. Dividing by 4 gives 2%, which compounds to 8.24… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].prose` | Projects A and B each cost £2,000.00. A pays £2,600.00 in year 2. B pays £1,300.00 in year 1 and £1,200.00 in… | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].widget.options[right]` | key: A has the higher NPV at 5%, B at 10% | correct | Recomputed; right under the convention the item states |
| `items[7].widget.options[a].why` | wrong option 'A wins at both rates, because it pays £100.00 more in total': At 10%, A's NPV is £148.76 and B'… | correct | Checked false under the item's premises; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].widget.options[b].why` | wrong option 'B wins at both rates, because it pays sooner': At 5%, A's NPV is £358.28 and B's £326.53. At lo… | correct | Checked false under the item's premises; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].widget.options[same].why` | wrong option 'They rank the same at every rate': The ranking flips near 7.7%, where the two NPVs are equal. | correct | Checked false under the item's premises; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].feedback.correct` | A wins at 5%, B at 10%: the ranking flips near 7.7%. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].feedback.generic` | Not quite right. Work out both NPVs at 5% and at 10%. | correct | Derivation or arithmetic step, checked |
| `items[7].explain.text` | At 5%: A £358.28, B £326.53. At 10%: A £148.76, B £173.55. The NPVs are equal at about 7.7%, so the rate deci… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[8].prose` | A preference share pays £45.00 at the end of every year, for ever. Investors want 3% a year. | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[8].widget.answer` | key 1500 £: £1,500.00: $45 / 0.03$. | correct | Recomputed; right under the convention the item states |
| `items[8].feedback.byKey.pct` | slip 15: You divided by 3, not 0.03. The rate goes in as a decimal. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[8].feedback.byKey.due` | slip 1545: That adds a payment today. The first is a year away. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[8].feedback.correct` | $45 / 0.03 = 1500$. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[8].feedback.generic` | Not quite right. A perpetuity is worth $C/r$. | correct | Derivation or arithmetic step, checked |
| `items[8].explain.text` | A payment for ever is a perpetuity, worth $C/r = 45/0.03 = 1500$. Each year's £45.00 is exactly 3% of £1,500.… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |

## review-2

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | A 3-year bond pays a 5% coupon on £100 face, half-yearly. Its yield is 6% a year, compounded half-yearly. | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[0].widget.answer` | key 97.29 £: £97.29 (exact: 97.2914). | correct | Recomputed; right under the convention the item states |
| `items[0].feedback.byKey.annual` | slip 97.33: That treats the coupons as annual. Halve the coupon and yield, and use 6 periods. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[0].feedback.byKey.full-coupon` | slip 110.84: You paid £5 every six months. Halve the coupon too. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[0].feedback.byKey.full-rate` | slip 82.79: You discounted at 6% every six months. Halve the yield too. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[0].feedback.correct` | £97.29: six £2.50 coupons and the face, at 3% a period. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[0].feedback.generic` | Not quite right. Use £2.50 coupons, 3% a period and 6 periods. | correct | Derivation or arithmetic step, checked |
| `items[0].explain.text` | Halve the coupon and the yield, double the periods: £2.50, 3%, 6 periods. $2.50 \times \tfrac{1 - 1.03^{-6}}{… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[1].prose` | Four bonds all yield 5%. | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[1].widget.options[right]` | key: A 2-year bond with an 8% coupon | correct | Recomputed; right under the convention the item states |
| `items[1].widget.options[zero2].why` | wrong option 'A 2-year zero-coupon bond': No coupons means all the value waits until year 2: a longer duratio… | correct | Checked false under the item's premises; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[1].widget.options[c10].why` | wrong option 'A 10-year bond with an 8% coupon': Its cash flows run ten years out, so a yield change bites ov… | correct | Checked false under the item's premises; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[1].widget.options[z10].why` | wrong option 'A 10-year zero-coupon bond': That is the most sensitive: all its value sits at year 10. | correct | Checked false under the item's premises; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[1].feedback.correct` | Short maturity and high coupon: the earliest cash flows, the smallest duration. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[1].feedback.generic` | Not quite right. Look for the cash flows that arrive soonest. | correct | Derivation or arithmetic step, checked |
| `items[1].explain.text` | Duration is the present-value-weighted time of the cash flows. The 2-year 8% bond returns the most money soon… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[2].prose` | Share X trades at £12.00 with earnings per share of £0.80. Share Y trades at £3.00 with earnings per share of… | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[2].widget.options[right]` | key: Y, with a P/E of 10 | correct | Recomputed; right under the convention the item states |
| `items[2].widget.options[x].why` | wrong option 'X, with a P/E of 15': X's P/E is 15, higher than Y's. A higher P/E means paying more per pound … | correct | Checked false under the item's premises; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[2].widget.options[price].why` | wrong option 'Y, because £3.00 is less than £12.00': Right share, wrong reason. A low price per share means n… | correct | Checked false under the item's premises; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[2].widget.options[inverse].why` | wrong option 'X, with earnings of 6.7% of its price': Y earns 10% of its price, more than X's 6.7%. | correct | Checked false under the item's premises; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[2].feedback.byKey.price` | Right share, wrong reason. Compare P/E, not price. | correct | Checked false under the item's premises; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[2].feedback.correct` | Y: $3.00/0.30 = 10$, against $12.00/0.80 = 15$. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[2].feedback.generic` | Not quite right. Divide each price by its earnings per share. | correct | Derivation or arithmetic step, checked |
| `items[2].explain.text` | X has a P/E of $12.00/0.80 = 15$ and Y of $3.00/0.30 = 10$. Y costs less per pound of profit. The share price… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[3].prose` | An investment grew by 21% in total over two years. | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[3].widget.answer` | key 0.1 %: 10%: $1.21^{1/2} - 1$. | correct | Recomputed; right under the convention the item states |
| `items[3].feedback.byKey.divide` | slip 0.105: You halved 21%. Compounding means $1.105^2 = 1.221$, too much. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[3].feedback.byKey.total` | slip 0.21: That is the total. Spread it over two years. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[3].feedback.correct` | 10% a year: $1.1^2 = 1.21$. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[3].feedback.generic` | Not quite right. Take the square root of 1.21. | correct | Derivation or arithmetic step, checked |
| `items[3].explain.text` | $(1.21)^{1/2} - 1 = 0.10$. Halving the total gives 10.5%, which ignores the return on the first year's return. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[4].prose` | A 7-year bond pays a 3% annual coupon on £100 face. Its yield is 4%. | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[4].widget.options[right]` | key: Below £100, at a discount | correct | Recomputed; right under the convention the item states |
| `items[4].widget.options[premium].why` | wrong option 'Above £100, at a premium': You read a higher yield as a higher price. A yield above the coupon … | correct | Checked false under the item's premises; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[4].widget.options[par].why` | wrong option 'At £100, at par': Par needs the yield to equal the coupon rate. Here 4% is above 3%. | correct | Checked false under the item's premises; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[4].feedback.correct` | At a discount: £94.00. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[4].feedback.generic` | Not quite right. Compare the coupon rate with the yield. | correct | Derivation or arithmetic step, checked |
| `items[4].explain.text` | The coupon, 3%, is below the 4% yield, so the bond must be cheap enough to make up the difference. Its price … | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[5].prose` | A £5 million bond portfolio has a modified duration of 6.2. Yields rise by 0.25 percentage points. | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[5].widget.answer` | key 77500 £: About £77,500: $6.2 \times 5{,}000{,}000 \times 0.0025$. | correct | Recomputed; right under the convention the item states |
| `items[5].feedback.byKey.full-point` | slip 310000: You used a 1-point move. A quarter point is $\Delta y = 0.0025$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[5].feedback.byKey.quarter` | slip 7750: You used 0.025%. A quarter of a percentage point is 0.0025 as a decimal. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[5].feedback.correct` | About £77,500. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[5].feedback.generic` | Not quite right. Use $\Delta P \approx -D\,P\,\Delta y$ with $\Delta y = 0.0025$. | correct | Derivation or arithmetic step, checked |
| `items[5].explain.text` | $6.2 \times \text{£}5{,}000{,}000 \times 0.0025 = \text{£}77{,}500$. Convexity makes the true loss slightly s… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[6].prose` | A share trades at £50.00. Its next dividend is £2.50, and analysts expect 2% growth a year for ever. | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[6].widget.answer` | key 0.07 %: 7%: $r = D/P + g = 0.05 + 0.02$. | correct | Recomputed; right under the convention the item states |
| `items[6].feedback.byKey.yield-only` | slip 0.05: That is the dividend yield alone. Add the growth rate. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[6].feedback.byKey.minus` | slip 0.03: You subtracted the growth. $r = D/P + g$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[6].feedback.correct` | 7%: a 5% dividend yield plus 2% growth. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[6].feedback.generic` | Not quite right. Rearrange $P = D/(r - g)$ for $r$. | correct | Derivation or arithmetic step, checked |
| `items[6].explain.text` | From $P = D/(r - g)$, $r - g = D/P = 2.50/50 = 0.05$. So $r = 0.05 + 0.02 = 7\%$: income plus growth. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[7].prose` | A 2-year bond pays a 5% annual coupon on £100 face and trades at £98.00. At 6% it would be worth £98.17; at 6… | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[7].widget.options[right]` | key: Between 6% and 6.5% | correct | Recomputed; right under the convention the item states |
| `items[7].widget.options[below].why` | wrong option 'Between 5% and 6%': At 6% the price, £98.17, is still above £98.00. The yield is above 6%. | correct | Checked false under the item's premises; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[7].widget.options[above].why` | wrong option 'Above 6.5%': At 6.5% the price, £97.27, is below £98.00. The yield is below 6.5%. | correct | Checked false under the item's premises; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[7].widget.options[coupon].why` | wrong option 'Exactly 5%': At 5% the bond is at par, £100. It trades below par. | correct | Checked false under the item's premises; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[7].feedback.correct` | Between 6% and 6.5%: the price crosses £98.00 there. The yield is 6.09%. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[7].feedback.generic` | Not quite right. Find the two prices either side of £98.00. | correct | Derivation or arithmetic step, checked |
| `items[7].explain.text` | £98.17 at 6% is too high and £97.27 at 6.5% too low, so the yield lies between. Bisection would next try 6.25… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].prose` | A fund returned 11% a year with a volatility of 16%. The risk-free rate is 3%. | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].widget.answer` | key 0.5 : 0.50: $(0.11 - 0.03)/0.16$. | correct | Recomputed; right under the convention the item states |
| `items[8].feedback.byKey.raw` | slip 0.6875: You left out the risk-free rate. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[8].feedback.byKey.inverse` | slip 2: That is volatility over excess return. Flip it. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[8].feedback.correct` | 0.50. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].feedback.generic` | Not quite right. Divide the excess return by the volatility. | correct | Derivation or arithmetic step, checked |
| `items[8].explain.text` | Excess return $0.11 - 0.03 = 0.08$, over volatility 0.16, gives 0.50. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |

## review-3

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | A grain trader is short a forward on one tonne of wheat at $F = \text{£}120.00$. At delivery wheat trades at … | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[0].widget.answer` | key -15 £: −£15.00 | correct | Recomputed; right under the convention the item states |
| `items[0].feedback.byKey.long` | slip 15: You used the long's payoff. The short must sell wheat worth £135.00 for £120.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[0].feedback.byKey.floor` | slip 0: You gave the forward a floor. The short is bound to deliver, so the loss stands. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[0].feedback.correct` | $F - S_T = 120 - 135 = -15$. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[0].feedback.generic` | Not quite right. The short's payoff is $F - S_T$. | correct | Derivation or arithmetic step, checked |
| `items[0].explain.text` | The short delivers wheat worth £135.00 and receives £120.00, a payoff of −£15.00. The long gains exactly that. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[1].prose` | A share trades at £80.00 and pays no dividends. The rate is 3% a year, compounded yearly. | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[1].widget.answer` | key 84.87 £: £84.87 | correct | Recomputed; right under the convention the item states |
| `items[1].feedback.byKey.simple` | slip 84.8: You used simple interest, $80 \times 1.06$. The financing compounds. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[1].feedback.byKey.one` | slip 82.4: That is the one-year forward. Delivery is in two years. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[1].feedback.byKey.spot` | slip 80: You left out the cost of carry. Holding the share for two years costs interest. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[1].feedback.correct` | $80 \times 1.03^2 = 84.87$. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[1].feedback.generic` | Not quite right. Grow £80.00 at 3% for two years. | correct | Derivation or arithmetic step, checked |
| `items[1].explain.text` | Borrowing £80.00 for two years repays $80 \times 1.03^2 = \text{£}84.872$. That is what delivering the share … | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[2].prose` | A share trades at £100.00 with no dividends, and the one-year rate is 5%. A dealer quotes the one-year forwar… | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[2].widget.answer` | key 5 £: £5.00 | correct | Recomputed; right under the convention the item states |
| `items[2].feedback.byKey.vs-spot` | slip 10: You compared the quote with today's price. Buying the share needs a loan that grows to £105.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[2].feedback.byKey.pv` | slip 4.76: That is the profit's value today. The question asks what you receive at delivery. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[2].feedback.correct` | Deliver for £110.00 a share that costs £105.00 to carry: £5.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[2].feedback.generic` | Not quite right. Borrow, buy and sell forward; compare the £110.00 with what the loan repays. | correct | Derivation or arithmetic step, checked |
| `items[2].explain.text` | Borrow £100.00, buy the share, sell it forward at £110.00. At delivery you receive £110.00 and repay £105.00,… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[3].prose` | You are long 3 index futures at £10.00 a point. The initial margin is £6,000.00 a contract and the maintenanc… | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[3].widget.answer` | key 6000 £: £6,000.00 | correct | Recomputed; right under the convention the item states |
| `items[3].feedback.byKey.maint` | slip 1500: You topped up to the maintenance level, £13,500.00. A call restores the initial margin, £18,000.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[3].feedback.byKey.one` | slip 2000: That is one contract's loss. You hold 3. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[3].feedback.byKey.none` | slip 0: £12,000.00 is below 3 times £4,500.00, so a call is due. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[3].feedback.correct` | £6,000.00 lost leaves £12,000.00, below £13,500.00: a call of £6,000.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[3].feedback.generic` | Not quite right. Find the loss on all 3 contracts, the new balance, and the gap to the initial margin. | correct | Derivation or arithmetic step, checked |
| `items[3].explain.text` | The loss is $3 \times 200 \times 10 = \text{£}6{,}000.00$, leaving £12,000.00. That is below the £13,500.00 m… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[4].prose` | You short 300 shares at £15.00 and cover at £18.00. The stock loan fee is £20.00, and no dividend is paid. | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[4].widget.answer` | key -920 £: −£920.00 | correct | Recomputed; right under the convention the item states |
| `items[4].feedback.byKey.no-fee` | slip -900: You left out the £20.00 fee. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[4].feedback.byKey.fee-helped` | slip -880: You took the fee off the loss. A fee always makes the result worse. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[4].feedback.byKey.sign` | slip 920: The share rose against your short, so this is a loss. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[4].feedback.correct` | $300 \times (15 - 18) - 20 = -920$. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[4].feedback.generic` | Not quite right. Use $P_0 - P_1 - C$ per trade. | correct | Derivation or arithmetic step, checked |
| `items[4].explain.text` | Covering at £18.00 costs £3.00 a share more than the sale raised: £900.00 on 300 shares. With the £20.00 fee … | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[5].prose` | A position has leverage $L = 4$, borrowing at 5% a year. Over the year the asset returns −10%. | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[5].widget.answer` | key -0.55 %: −55% | correct | Recomputed; right under the convention the item states |
| `items[5].feedback.byKey.no-int` | slip -0.4: You scaled the fall but forgot the interest on three units of borrowing. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[5].feedback.byKey.int-once` | slip -0.45: You charged interest on one unit. With $L = 4$ you borrow three times your equity. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[5].feedback.byKey.unlev` | slip -0.1: That is the asset's return. Your equity moves four times as much. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[5].feedback.byKey.sign` | slip 0.55: R_E = 4 × (−0.10) − 3 × 0.05, and both terms are negative: −0.40 and −0.15. A positive 55% books t… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[5].feedback.correct` | $4 \times (-0.10) - 3 \times 0.05 = -0.55$. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[5].feedback.generic` | Not quite right. Use $R_E = L R_A - (L - 1) r$. | correct | Derivation or arithmetic step, checked |
| `items[5].explain.text` | $R_E = 4 \times (-0.10) - 3 \times 0.05 = -0.55$. The 10% fall costs 40% of equity, and the interest another … | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[6].prose` | Four positions, each held to the delivery or expiry date. Ignore any premium paid. | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[6].widget.options[short-fwd]` | key: A short forward | correct | Recomputed; right under the convention the item states |
| `items[6].widget.options[short-share]` | key: A short sale of a share | correct | Recomputed; right under the convention the item states |
| `items[6].widget.options[long-fwd].why` | wrong option 'A long forward': A long forward loses at most $F$, if the asset goes to zero. | correct | Checked false under the item's premises; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[6].widget.options[long-call].why` | wrong option 'A long call': A long call's payoff never falls below zero; the most you lose is the premium. | correct | Checked false under the item's premises; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[6].feedback.correct` | The short forward and the short sale both lose as the price rises, without limit. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[6].feedback.generic` | Not quite right. Ask which positions lose when the price rises, and whether prices have a ceiling. | correct | Derivation or arithmetic step, checked |
| `items[6].explain.text` | Both short positions lose £1.00 for each £1.00 the price rises, and prices have no ceiling. A long forward's … | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[7].prose` | A share trades at £60.00. It pays a £1.50 dividend in three months. The rate is 4% a year, compounded yearly. | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[7].widget.answer` | key 60.86 £: £60.86: $(60 - 1.5/1.04^{0.25}) \times 1.04$ | correct | Recomputed; right under the convention the item states |
| `items[7].feedback.byKey.ignored` | slip 62.4: You left out the dividend. The holder receives £1.50 that the forward's buyer does not. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[7].feedback.byKey.not-grown` | slip 60.9: You took £1.50 off £62.40. Received at three months, it earns interest for nine more: £1.545. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[7].feedback.byKey.not-disc` | slip 60.84: You took the full £1.50 off today's price. Paid in three months, it is worth £1.485 today. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[7].feedback.correct` | $(60 - 1.485) \times 1.04 = 60.86$. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[7].feedback.generic` | Not quite right. Take the dividend's present value off £60.00, then grow for a year. | correct | Derivation or arithmetic step, checked |
| `items[7].explain.text` | $PV(D) = \tfrac{1.50}{1.04^{0.25}} = \text{£}1.485$, so $F = (60 - 1.485) \times 1.04 = \text{£}60.86$. Equiv… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[8].prose` | You hold £30,000.00 of shares bought with £12,000.00 of your own money and an £18,000.00 margin loan. The bro… | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[8].widget.answer` | key 25714.29 £: £25,714.29: $18{,}000 / 0.7$ | correct | Recomputed; right under the convention the item states |
| `items[8].feedback.byKey.orig` | slip 27000: You took 30% of the original £30,000.00 as the trigger for your equity. The rule uses the value n… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[8].feedback.byKey.zero` | slip 18000: That is where your equity is gone. The broker calls earlier, at 30%. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[8].feedback.byKey.of-loan` | slip 23400: You measured 30% of the loan. The rule is 30% of the position's value, $V$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[8].feedback.correct` | $V - 18{,}000 = 0.3V$ gives $V = 25{,}714.29$. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[8].feedback.generic` | Not quite right. Write equity as $V - 18{,}000$ and set it equal to 30% of $V$. | correct | Derivation or arithmetic step, checked |
| `items[8].explain.text` | Equity is $V - 18{,}000$; the rule needs $V - 18{,}000 \ge 0.3V$, so $V \ge \tfrac{18{,}000}{0.7} = 25{,}714.… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |

## homework-1

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | A store card balance of £3,000.00 is left unpaid. The card charges 1.8% a month, compounded monthly. | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[0].widget.answer` | key 4603.29 £: £4,603.29: $3000 \times 1.018^{24}$. | correct | Recomputed; right under the convention the item states |
| `items[0].feedback.byKey.simple` | slip 4296: You charged 1.8% of £3,000.00 each month: simple interest. Each month's charge is on a bigger bala… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[0].feedback.byKey.annual` | slip 4435.97: You compounded 21.6% a year. The card compounds monthly, so use $1.018^{24}$. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[0].feedback.byKey.interest` | slip 1603.29: That is the interest alone. Add the £3,000.00 balance. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[0].feedback.correct` | $3000 \times 1.018^{24} = 4603.29$. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[0].feedback.generic` | Not quite right. Multiply by 1.018 once for each of the 24 months. | correct | Derivation or arithmetic step, checked |
| `items[0].explain.text` | Twenty-four monthly charges compound to $1.018^{24} = 1.534429$. So £3,000.00 becomes £4,603.29. The effectiv… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[1].prose` | A contract pays £1,000.00 in 1 year, £2,000.00 in 3 years and £3,000.00 in 5 years. The rate is 5% a year, co… | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[1].widget.answer` | key 5030.63 £: £5,030.63: $\tfrac{1000}{1.05} + \tfrac{2000}{1.05^3} + \tfrac{3000}{1.05^5}$. | correct | Recomputed; right under the convention the item states |
| `items[1].feedback.byKey.plain` | slip 6000: You added the payments without discounting. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[1].feedback.byKey.all-five` | slip 4701.16: You discounted all £6,000.00 by five years. The first two payments come sooner. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[1].feedback.byKey.all-three` | slip 5183.03: You discounted all £6,000.00 by three years, the middle date. Each payment needs its own wait. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[1].feedback.correct` | £952.38 + £1,727.68 + £2,350.58 = £5,030.63. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[1].feedback.generic` | Not quite right. Discount each payment for its own wait, then add. | correct | Derivation or arithmetic step, checked |
| `items[1].explain.text` | The present values are $952.38$, $1727.68$ and $2350.58$. They add to £5,030.63. Discounting each payment sep… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[2].prose` | Four savings accounts quote nominal rates with different crediting. | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[2].widget.options[monthly].why` | wrong option '4.60% credited monthly': Its AER is $(1 + \tfrac{0.046}{12})^{12} - 1 = 0.04698$, or 4.698%. Cl… | correct | Checked false under the item's premises; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[2].widget.options[annual].why` | wrong option '4.70% credited once a year': Its AER is 4.70%. The quarterly account compounds a higher rate, r… | correct | Checked false under the item's premises; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[2].widget.options[cont].why` | wrong option '4.55% compounded continuously': You trusted continuous compounding to win. $e^{0.0455} - 1 = 0.… | correct | Checked false under the item's premises; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[2].widget.options[right]` | key: 4.65% credited quarterly | correct | Recomputed; right under the convention the item states |
| `items[2].feedback.correct` | $(1 + \tfrac{0.0465}{4})^4 - 1 = 0.0473$: an AER of 4.73%, the highest. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[2].feedback.generic` | Not quite right. Turn each quote into an effective rate before you compare. | correct | Derivation or arithmetic step, checked |
| `items[2].explain.text` | The AERs are 4.698%, 4.700%, 4.655% and 4.732%. The quarterly account wins although its nominal rate is not t… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[3].prose` | An account must pay an AER of $a$, credited monthly. Derive the nominal annual rate $r$ it should quote. | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[3].widget.lines[s1]` | $\left(1 + \tfrac{r}{12}\right)^{12} = 1 + a$: twelve monthly credits must give the year's growth | correct | Derivation or arithmetic step, checked |
| `items[3].widget.lines[s2]` | $1 + \tfrac{r}{12} = (1 + a)^{1/12}$: take the twelfth root of both sides | correct | Derivation or arithmetic step, checked |
| `items[3].widget.lines[s3]` | $\tfrac{r}{12} = (1 + a)^{1/12} - 1$: subtract 1 from both sides | correct | Derivation or arithmetic step, checked |
| `items[3].widget.lines[s4]` | $r = 12\left((1 + a)^{1/12} - 1\right)$: multiply both sides by 12 | correct | Derivation or arithmetic step, checked |
| `items[3].widget.lines[s5]` | For $a = 0.05$: $r = 12(1.05^{1/12} - 1) = 0.0489$, so quote 4.89% | correct | Derivation or arithmetic step, checked |
| `items[3].feedback.byKey.s2` | The root needs an equation to act on. State the growth equation first. | correct | Derivation or arithmetic step, checked |
| `items[3].feedback.byKey.s4` | Multiply by 12 only once $\tfrac{r}{12}$ stands alone. | correct | Derivation or arithmetic step, checked |
| `items[3].feedback.byKey.s5` | The number comes last, once the formula is found. | correct | Derivation or arithmetic step, checked |
| `items[3].feedback.correct` | Undo each operation in reverse: the power, then the 1, then the 12. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[3].feedback.generic` | Not quite right. Start from the equation that says both rates give the same year's growth. | correct | Derivation or arithmetic step, checked |
| `items[3].explain.text` | Matching a year's growth gives $(1 + \tfrac{r}{12})^{12} = 1 + a$. Undoing the power, the 1 and the 12 in tur… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[4].prose` | A cash flow $C$ is paid in $n$ years. The rate is $r$ a year nominal, compounded $m$ times a year. | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[4].widget.answer` | key \frac{C}{(1+\frac{r}{m})^{mn}} | correct | Recomputed; right under the convention the item states |
| `items[4].feedback.byKey.annual` | wrong form \frac{C}{(1+r)^{n}}: That compounds once a year. With $m$ credits a year, each period's rate is $\… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[4].feedback.byKey.power-n` | wrong form \frac{C}{(1+\frac{r}{m})^{n}}: You used the period rate but only $n$ periods. There are $m$ period… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[4].feedback.byKey.simple` | wrong form \frac{C}{1+rn}: That is simple discounting. Divide by the compounded growth instead. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[4].feedback.correct` | $mn$ periods back, each dividing by $1 + \tfrac{r}{m}$. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[4].feedback.generic` | Not quite right. Count the compounding periods in $n$ years, and the rate for each one. | correct | Derivation or arithmetic step, checked |
| `items[4].explain.text` | There are $mn$ periods, each growing money by $1 + \tfrac{r}{m}$. Discounting divides by all of them: $PV = C… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[5].prose` | Write `irr(flows)`, the rate where the NPV is zero. Assume `flows[0]` is negative and the rest are not, so th… | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[5].widget.solution` | solution passes the hidden tests; starter fails; tests: 10 | correct | Solution and starter graded under Pyodide 0.27.7 (grade-all --code); natural wrong codings rejected |
| `items[5].feedback.byKey.error` | Your code stopped with an error, or ran too long. Check that the loop changes `lo` or `hi` every time. | imprecise | Finding 5: Pyodide run: a loop that never ends is stopped per case and keyed test-1, never error |
| `items[5].feedback.correct` | Each step keeps the half of the bracket where the NPV changes sign. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[5].feedback.generic` | Some tests failed. A positive NPV at `mid` means the IRR is higher, so move `lo` up; otherwise move `hi` down. | correct | Derivation or arithmetic step, checked |
| `items[5].explain.text` | A positive NPV at `mid` means the rate is still too low, so the IRR lies in the upper half. Each step halves … | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[6].prose` | A project costs £1,000.00 today and pays £550.00 at the end of each of the next 2 years. Write $u = 1 + r$, s… | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[6].widget.answer` | key 0.065965 %: 6.60%: $u = \tfrac{550 + \sqrt{550^2 + 4 \times 1000 \times 550}}{2000} = 1.0660$. | correct | Recomputed; right under the convention the item states |
| `items[6].feedback.byKey.simple` | slip 0.0667: 6.67% solves $1000(1 + 2r) = 1100$, a simple-interest return. Compounding needs the quadratic. | wrong | Finding 1: $1000(1+2r)=1100$ gives $r=0.05$; 0.0667 is $0.10/1.5$. Script check fails |
| `items[6].feedback.byKey.u` | slip 1.065965: That is $u = 1 + r$. Take away 1 to get the rate. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[6].feedback.byKey.neg` | slip -1.515965: That comes from the negative root, $u = -0.5160$. A growth factor must be positive. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[6].feedback.correct` | $u = 1.0660$, so the IRR is 6.60%. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[6].feedback.generic` | Not quite right. Multiply through by $u^2$ to get $1000u^2 - 550u - 550 = 0$, then use the formula. | correct | Derivation or arithmetic step, checked |
| `items[6].explain.text` | Multiplying by $u^2$ gives $1000u^2 - 550u - 550 = 0$. The positive root is $u = \tfrac{550 + \sqrt{2502500}}… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].prompt` | A retiring trader can take £600,000.00 now. The other offer is £45,000.00 a year for 20 years, the first in o… | correct | BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].model[0]` | **(a) Values today.** The income is a 20-year stream of £45,000.00, so its present value is $$45000 \times \f… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].model[1]` | **(b) Break-even rate.** The offers are equal when the factor is $600000 / 45000 = 13.3333$. At 4.2% the stre… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].model[2]` | **(c) Recommendation.** If the trader could invest the lump sum at less than 4.2% a year, the income is worth… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].model[3]` | **(d) The £900,000.00 error.** Adding $20 \times 45000$ ignores when the money arrives. Each payment must be … | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].model[4]` | **(e) Different rates.** An NPV depends on the rate, so two values computed at different rates are not compar… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].rubric[0]` | Writes the stream's present value as a discounted sum or annuity formula, with each payment discounted for it… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].rubric[1]` | Computes £611,564.69 at 4% and £560,799.47 at 5%, within £1.00. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].rubric[2]` | Finds the break-even rate as about 4.2%, by trial or bisection, and names it as an IRR. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].rubric[3]` | Recommends conditionally on the achievable rate, and names at least one risk outside the NPV (longevity, defa… | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].rubric[4]` | Explains that £900,000.00 sums undiscounted cash flows. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |
| `items[7].rubric[5]` | Explains that NPVs at different rates cannot be compared, and that one shared rate must be used. | correct | Recomputed in the concepts script or by hand; BMA ch. 2 and 5; Hull 10e §4.2 |

## homework-2

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | A 7-year bond pays a 3% annual coupon on £100 face. Its yield is 4%. | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[0].widget.answer` | key 94.0 £: £94.00 (exact: 93.9979). | correct | Recomputed; right under the convention the item states |
| `items[0].feedback.byKey.coupon-rate` | slip 100: You discounted at the coupon rate. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[0].feedback.byKey.principal` | slip 75.99: You discounted the face and dropped the coupons. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[0].feedback.correct` | £94.00, a discount. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[0].feedback.generic` | Not quite right. Use the shortcut: $\tfrac{C}{y}(1 - v^T) + Fv^T$. | correct | Derivation or arithmetic step, checked |
| `items[0].explain.text` | $v^7 = 1/1.04^7 = 0.7599$. Coupons: $\tfrac{3}{0.04}(1 - 0.7599) = 18.01$; face: $75.99$. Price £94.00. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[1].prose` | A 3-year bond pays a 5% annual coupon on £100 face and trades at £97.00. | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[1].widget.answer` | key 0.0612 %: 6.12% (exact: 6.1249%). | correct | Recomputed; right under the convention the item states |
| `items[1].feedback.byKey.current` | slip 0.0515: That is the current yield, $5/97$. It ignores the £3 gain to par. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[1].feedback.byKey.coupon` | slip 0.05: At 5% the price is £100. It trades below par, so the yield is higher. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[1].feedback.correct` | 6.12%. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[1].feedback.generic` | Not quite right. Bisect between 6% and 6.5%: price each midpoint and compare with £97.00. | correct | Derivation or arithmetic step, checked |
| `items[1].explain.text` | At 6% the price is £97.33 and at 6.5% £96.03, so the yield is in between. Bisecting further gives 6.1249%. Ch… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[2].prose` | Show that a bond whose yield equals its coupon rate $c$ is priced at its face value $F$. Write $v = 1/(1+y)$. | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[2].widget.lines[s1]` | $P = \dfrac{C}{y}\left(1 - v^T\right) + F v^T$, the price with the coupons summed as a geometric series | correct | Derivation or arithmetic step, checked |
| `items[2].widget.lines[s2]` | $C = cF$, since the coupon is the coupon rate times the face | correct | Derivation or arithmetic step, checked |
| `items[2].widget.lines[s3]` | With $y = c$: $\dfrac{C}{y} = \dfrac{cF}{c} = F$ | correct | Derivation or arithmetic step, checked |
| `items[2].widget.lines[s4]` | $P = F\left(1 - v^T\right) + F v^T$, substituting into the first line | correct | Derivation or arithmetic step, checked |
| `items[2].widget.lines[s5]` | $P = F$, because the $F v^T$ terms cancel | correct | Derivation or arithmetic step, checked |
| `items[2].feedback.correct` | At $y = c$ the coupons are worth exactly $F(1 - v^T)$, and the face supplies the rest. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[2].feedback.generic` | Not quite right. Start from the price formula, then substitute $C = cF$ and $y = c$. | correct | Derivation or arithmetic step, checked |
| `items[2].explain.text` | With $y = c$, the coupons are worth $F(1 - v^T)$ and the face $Fv^T$. They add to $F$ for every maturity $T$.… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[3].prose` | Write a yield solver for annual-coupon bonds. `bond_price` is given. Bisect on `[0, 1]`: the price falls as t… | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[3].widget.solution` | solution passes the hidden tests; starter fails; tests: 8 | correct | Solution and starter graded under Pyodide 0.27.7 (grade-all --code); natural wrong codings rejected |
| `items[3].feedback.byKey.error` | Your code stopped with an error. Replace the `...` with a comparison. | imprecise | Finding 5: Pyodide run: `if ...:` runs (Ellipsis is true) and is keyed test-1, never error |
| `items[3].feedback.byKey.test-1` | Check the direction: if the price at `mid` is too high, the yield must be above `mid`. | correct | Pyodide run: reversed comparison (two codings) and comparison with face fail test 1 first |
| `items[3].feedback.correct` | A price above the target means the yield is higher than the midpoint, so the low end moves up. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[3].feedback.generic` | Some tests failed. Compare the price at `mid` with the target price. | correct | Derivation or arithmetic step, checked |
| `items[3].explain.text` | If `bond_price(..., mid)` exceeds the target, `mid` is too low a yield, so the low end moves up. A hundred ha… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[4].prose` | A share trades at £6.00. The company offers two new shares at £4.00 for every five held, and all holders take… | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[4].widget.answer` | key 5.43 £: £5.43 (exact: 5.4286), $(5 \times 6 + 2 \times 4)/7$. | correct | Recomputed; right under the convention the item states |
| `items[4].feedback.byKey.unchanged` | slip 6: Shares sold below £6.00 pull the average price down. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[4].feedback.byKey.average` | slip 5: You averaged £6 and £4. There are five old shares for every two new ones. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[4].feedback.correct` | £5.43. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[4].feedback.generic` | Not quite right. Add the value of five old shares and the cash for two new ones, then divide by 7. | correct | Derivation or arithmetic step, checked |
| `items[4].explain.text` | Five old shares are worth £30.00, and two new ones bring £8.00 of cash. That £38.00 is spread over 7 shares: … | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[5].prose` | A share trades at £60.00. Its next dividend is £1.80, and investors require 8% a year. | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[5].widget.answer` | key 0.05 %: 5%: $g = r - D/P = 0.08 - 0.03$. | correct | Recomputed; right under the convention the item states |
| `items[5].feedback.byKey.plus` | slip 0.11: You added the dividend yield to $r$. Growth is $r$ minus the yield. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[5].feedback.byKey.yield` | slip 0.03: That is the dividend yield, $D/P$. Growth is what is left of $r$ after it. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[5].feedback.correct` | 5%. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[5].feedback.generic` | Not quite right. Rearrange $P = D/(r - g)$ for $g$. | correct | Derivation or arithmetic step, checked |
| `items[5].explain.text` | $r - g = D/P = 1.80/60 = 0.03$, so $g = 0.08 - 0.03 = 5\%$. The price is a bet on 5% growth for ever. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[6].prose` | A fund returned +25%, −20% and +10% in three years. Its manager quotes the 5% arithmetic average. | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[6].widget.answer` | key 0.0323 %: 3.23%: $1.1^{1/3} - 1$, where $1.25 \times 0.8 \times 1.1 = 1.1$. | correct | Recomputed; right under the convention the item states |
| `items[6].feedback.byKey.average` | slip 0.05: That is the arithmetic average the manager quotes. Compound instead. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[6].feedback.byKey.total` | slip 0.1: That is the total return. Annualise it. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[6].feedback.byKey.divide` | slip 0.0333: You divided 10% by 3. Take the cube root of 1.1 instead. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[6].feedback.correct` | 3.23% a year: a 10% total over three years. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[6].feedback.generic` | Not quite right. Multiply the growth factors, then take the cube root. | correct | Derivation or arithmetic step, checked |
| `items[6].explain.text` | $1.25 \times 0.80 \times 1.10 = 1.10$, a 10% total. Annualised, $1.1^{1/3} - 1 = 3.23\%$. The 5% average over… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[7].prose` | You buy the 5-year 4% annual bond for £95.67 at a 5% yield. One year later you receive the £4 coupon, and yie… | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[7].widget.answer` | key 0.0146 %: 1.46%: $(93.07 + 4 - 95.67)/95.67$. | correct | Recomputed; right under the convention the item states |
| `items[7].feedback.byKey.unchanged` | slip 0.05: That would be the return had yields stayed at 5%. They rose, so the price fell. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[7].feedback.byKey.no-coupon` | slip -0.0272: You left out the £4 coupon. Total return includes income. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[7].feedback.byKey.five-year` | slip -0.001: You priced 5 years at 6%. One year has passed, so 4 remain. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[7].feedback.correct` | 1.46%: the coupon is mostly eaten by the fall in price. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[7].feedback.generic` | Not quite right. Price the remaining 4 years at 6%, add the coupon, and divide the gain by £95.67. | correct | Derivation or arithmetic step, checked |
| `items[7].explain.text` | With 4 years left at 6%, the bond is worth £93.07. You gain $93.07 + 4 - 95.67 = 1.40$, or 1.46%. Had yields … | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].prompt` | A 4-year bond pays a 5% annual coupon on £100 face. Its yield is 6%. (a) Find its price. (b) Find its current… | correct | Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].model[0]` | **(a) Price.** Discount each cash flow at 6%: $$\begin{aligned} P &= \frac{5}{1.06} + \frac{5}{1.06^2} + \fra… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].model[1]` | **(b) Current yield.** $5/96.53 = 5.18\%$. It is below the 6% yield to maturity, which also counts the £3.47 … | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].model[2]` | **(c) Duration and a 0.5-point rise.** The slope is $P'(y) = -\sum t\,c_t/(1+y)^{t+1} = -(4.4500 + 8.3962 + 1… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].model[3]` | **(d) Holding for a year.** If yields stay at 6%, after one year the bond has 3 years left and is worth $$\fr… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].model[4]` | **(e) The share.** $P = D/(r - g) = 3/(0.08 - 0.02) = \text{£}50.00$. At $r = 9\%$, $P = 3/0.07 = \text{£}42.… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].model[5]` | **(f) Why both fall, and why the share falls more.** Both are present values of fixed or forecast cash flows,… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].rubric[0]` | Prices the bond at £96.53 by discounting all four cash flows, face value included, at 6%. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].rubric[1]` | Gives the current yield 5.18% and explains that the yield to maturity also counts the rise to par. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].rubric[2]` | Finds $D = 3.51$ from the slope, estimates a fall of about £1.69, and finds the true price £94.86. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].rubric[3]` | States that the true fall is smaller than the tangent's because the price curve bends up. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].rubric[4]` | Prices the 3-year bond at £97.33 after a year and finds a total return of 6.00%, including the coupon. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].rubric[5]` | Values the share at £50.00 and £42.86 with $D/(r - g)$, a 14.3% fall. | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |
| `items[8].rubric[6]` | Explains that both prices are present values that fall as rates rise. The share's distant, growing cash flows… | correct | Recomputed in the concepts script or by hand; Fabozzi ch. 2–4; Hull 10e §4.4, §4.8; BKM ch. 5, 14, 16, 18 |

## homework-3

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | A UK exporter will receive 2,000,000 euros from a customer in six months. It goes short a six-month forward a… | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[0].widget.answer` | key 1700000 £: £1,700,000.00: $2{,}000{,}000 \times 0.85$ | correct | Recomputed; right under the convention the item states |
| `items[0].feedback.byKey.spot` | slip 1660000: That ignores the forward. A short forward pays $F - S_T = 0.02$ pounds per euro. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[0].feedback.byKey.payoff` | slip 40000: That is the forward's payoff alone. The exporter still sells 2,000,000 euros. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[0].feedback.byKey.sign` | slip 1620000: You subtracted the forward's payoff. The euro fell, so the short forward gains. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[0].feedback.correct` | £1,660,000.00 at the market plus the forward's £40,000.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[0].feedback.generic` | Not quite right. Sell the euros at the market, then add the short forward's payoff. | correct | Derivation or arithmetic step, checked |
| `items[0].explain.text` | The euros fetch $2{,}000{,}000 \times 0.83 = \text{£}1{,}660{,}000.00$, and the short forward pays $2{,}000{,… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[1].prose` | A share at $S_0$ pays one dividend $D$ at time $t < T$. Rates are $r$ a year, compounded yearly, and $PV(D) =… | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[1].widget.lines[o1]` | Strategy 1: buy the share for $S_0$ and borrow $PV(D)$ against the dividend: net cost today $S_0 - PV(D)$ | correct | Derivation or arithmetic step, checked |
| `items[1].widget.lines[o2]` | At $t$ the dividend $D$ repays that loan exactly, so at $T$ strategy 1 holds one share and owes nothing | correct | Derivation or arithmetic step, checked |
| `items[1].widget.lines[o3]` | Strategy 2: go long the forward and lend $F(1 + r)^{-T}$ today; at $T$ the loan pays $F$ for the share | correct | Derivation or arithmetic step, checked |
| `items[1].widget.lines[o4]` | Both end with one share at $T$, so with no arbitrage they cost the same: $F(1 + r)^{-T} = S_0 - PV(D)$ | correct | Derivation or arithmetic step, checked |
| `items[1].widget.lines[o5]` | $F = \left(S_0 - PV(D)\right)(1 + r)^T$, multiplying both sides by $(1 + r)^T$ | correct | Derivation or arithmetic step, checked |
| `items[1].feedback.byKey.o4` | Equal costs need both strategies laid out first, with the same holding at $T$. | correct | Derivation or arithmetic step, checked |
| `items[1].feedback.byKey.o5` | Solving for $F$ comes last. | correct | Derivation or arithmetic step, checked |
| `items[1].feedback.correct` | Two strategies, the same share at $T$, the same cost today, then solve. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[1].feedback.generic` | Not quite right. Build each strategy and its payoff before setting the costs equal. | correct | Derivation or arithmetic step, checked |
| `items[1].explain.text` | The dividend is income only the holder receives, so it is sold off today as $PV(D)$. With $S_0 = 100$, $D = 2… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[2].prose` | A share trades at £100.00 and pays a £2.00 dividend in six months. The rate is 5% a year, compounded yearly. … | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[2].widget.answer` | key 1.05 £: £1.05: $104 - 102.95$ | correct | Recomputed; right under the convention the item states |
| `items[2].feedback.byKey.no-div` | slip -1: You compared £104.00 with £105.00 and ignored the dividend. Holding the share earns £2.00, so carryi… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[2].feedback.byKey.vs-spot` | slip 4: You compared the quote with today's price. Carrying the share costs interest, less the dividend. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[2].feedback.byKey.not-grown` | slip 1: You used £103.00 as the fair price. The dividend, reinvested from six months, grows to £2.05. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[2].feedback.correct` | The fair price is £102.95, so selling forward at £104.00 locks in £1.05. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[2].feedback.generic` | Not quite right. Find the no-arbitrage forward with the dividend, then compare with £104.00. | correct | Derivation or arithmetic step, checked |
| `items[2].explain.text` | Borrow £100.00, buy the share and sell it forward at £104.00. The £2.00 dividend, invested from six months, g… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[3].prose` | You are long 2 index futures at £10.00 a point. The initial margin is £6,000.00 a contract and the maintenanc… | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[3].widget.answer` | key 7200 £: £7,200.00: £3,600.00 after day 2 and after day 5 | correct | Recomputed; right under the convention the item states |
| `items[3].feedback.byKey.end` | slip 0: You checked the 2-contract balance against £4,500.00, one contract's maintenance. It never falls that… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[3].feedback.byKey.one` | slip 3600: You found the first call. Day 5 closes at £8,400.00, below £9,000.00 again. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[3].feedback.byKey.maint` | slip 4200: You topped up to the maintenance level each time. A call restores the initial £12,000.00. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[3].feedback.correct` | Two calls of £3,600.00: after days 2 and 5. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[3].feedback.generic` | Not quite right. Settle each evening for 2 contracts, and check each balance against £9,000.00. | correct | Derivation or arithmetic step, checked |
| `items[3].explain.text` | The balance runs £10,000.00, £8,400.00 (call £3,600.00), £12,600.00, £9,600.00 and £8,400.00 (call £3,600.00)… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[4].prose` | Write `margin_calls(prices, contracts, point_value, initial, maintenance)`. `prices` are daily settlement pri… | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[4].widget.solution` | solution passes the hidden tests; starter fails; tests: 10 | correct | Solution and starter graded under Pyodide 0.27.7 (grade-all --code); natural wrong codings rejected |
| `items[4].feedback.correct` | Your simulator settles every evening and restores the initial margin on each call. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[4].feedback.generic` | Not quite right. Check the failing tests. Start at `initial` times the number of contracts, and add each call… | correct | Derivation or arithmetic step, checked |
| `items[4].explain.text` | Start with `initial * abs(contracts)` and each day add the signed gain, `contracts * point_value * (now - pre… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[5].prose` | A fund shorts 2,000 shares at £30.00 and covers at £33.00. While it is short the company pays a £0.50 dividen… | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[5].widget.answer` | key -7180 £: −£7,180.00 | correct | Recomputed; right under the convention the item states |
| `items[5].feedback.byKey.no-div` | slip -6180: You forgot the dividend. The fund owes the lender £0.50 on each of 2,000 shares. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[5].feedback.byKey.div-income` | slip -5180: You treated the dividend as income. The buyer receives it; the short pays it to the lender. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[5].feedback.byKey.no-costs` | slip -6000: That is the price loss alone. The dividend and the fee add to it. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[5].feedback.byKey.sign` | slip 7180: The price move costs £6,000.00, the dividends £1,000.00 and the fee £180.00, and all three are los… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[5].feedback.correct` | $-6{,}000 - 1{,}000 - 180 = -7{,}180$. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[5].feedback.generic` | Not quite right. Add the price loss, the dividend owed to the lender and the fee. | correct | Derivation or arithmetic step, checked |
| `items[5].explain.text` | The price move costs $2{,}000 \times 3 = \text{£}6{,}000.00$. The fund also pays the lender £1,000.00 of divi… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[6].prose` | You hold shares worth 3 times your equity, $L = 3$, with the rest on a margin loan. The broker's maintenance … | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[6].widget.answer` | key 0.1111 %: 11.11%, a fall of one ninth | correct | Recomputed; right under the convention the item states |
| `items[6].feedback.byKey.wipe` | slip 0.3333: That is the fall that wipes out the equity, $1/L$. The broker calls well before. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[6].feedback.byKey.quarter` | slip 0.25: You read 25% as the fall allowed. It is a floor on equity as a share of the position. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[6].feedback.byKey.eq-quarter` | slip 0.0833: You let equity fall by a quarter, a 25% loss of equity. The rule compares equity with the positi… | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[6].feedback.correct` | $V = \tfrac{8}{3}E$ against a start of $3E$: a fall of $\tfrac{1}{9} = 11.11\%$. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[6].feedback.generic` | Not quite right. With equity $E$, the loan is $2E$. Solve $V - 2E = 0.25V$. | correct | Derivation or arithmetic step, checked |
| `items[6].explain.text` | With equity $E$ the loan is $2E$. The rule $V - 2E \ge 0.25V$ gives $V \ge \tfrac{8}{3}E$, against $3E$ at th… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[7].prose` | A trader shorts £50,000.00 of a share. The broker holds the £50,000.00 of sale proceeds plus £25,000.00 of th… | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[7].widget.answer` | key 0.1538 %: 15.38%: $10{,}000 / 65{,}000$ | correct | Recomputed; right under the convention the item states |
| `items[7].feedback.byKey.wipe` | slip 0.5: That is where the equity is gone: a 50% rise. The broker calls sooner. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[7].feedback.byKey.thirty` | slip 0.3: You read the 30% rule as the rise allowed. It is a floor on equity relative to the shares owed. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[7].feedback.byKey.no-growth` | slip 0.2: You held the 30% to the original £50,000.00. As the share rises, the shares owed grow too. | correct | The named mistake recomputed to this value; not a valid answer under any convention the item allows |
| `items[7].feedback.correct` | $25{,}000 - 50{,}000x = 0.3 \times 50{,}000(1 + x)$ gives $x = 15.38\%$. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[7].feedback.generic` | Not quite right. Write the shares owed as $50{,}000(1 + x)$ and the equity as $75{,}000$ minus that. | correct | Derivation or arithmetic step, checked |
| `items[7].explain.text` | After a rise $x$ the shares owed are worth $50{,}000(1 + x)$ and the equity is $25{,}000 - 50{,}000x$. The ru… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[8].prompt` | An airline must buy 10,000 tonnes of jet fuel in one year. Fuel costs £600.00 a tonne today. The rate is 5% a… | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[8].model[0]` | **1. The forward price.** One way to own fuel in a year is to buy it today and store it. Buying today costs £… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[8].model[1]` | **2. Payoffs at delivery.** The airline is long 10,000 tonnes at £642.00. - Fuel at £570.00: payoff $10{,}000… | correct | Hull 10e §5.11: for a consumption commodity cost of carry gives only an upper bound; $600\times1.05+12$ |
| `items[8].model[2]` | Either way the fuel costs $10{,}000 \times 642 = \text{£}6{,}420{,}000.00$: the forward fixes the price, givi… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[8].model[3]` | **3. Futures instead.** With futures the same £720,000.00 loss is paid in cash, day by day, as fuel falls. Ea… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[8].model[4]` | **4. A quote of £660.00.** The forward is £18.00 too dear. Sell it forward at £660.00, borrow £600.00 a tonne… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[8].rubric[0]` | Derives $F = 600 \times 1.05 + 12 = \text{£}642.00$ from a buy-and-store strategy. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[8].rubric[1]` | Says storage raises the forward because it is a cost of holding. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[8].rubric[2]` | Gives the payoffs −£720,000.00 at £570.00 and +£580,000.00 at £700.00. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[8].rubric[3]` | Shows the total cost is £6,420,000.00 in both cases. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[8].rubric[4]` | Explains that futures losses are paid in cash daily, with margin calls when the balance closes below maintena… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[8].rubric[5]` | Explains the mismatch: the physical saving arrives later. So the airline needs cash or may be forced to close… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[8].rubric[6]` | Describes selling forward at £660.00, borrowing to buy and store fuel, and finds £18.00 a tonne. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[9].prompt` | A share trades at £64.00 today. It pays one dividend of £1.20 a share in six months. You want the price of a … | correct | Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[9].model[0]` | Write $S_0 = 64$, $D = 1.20$ paid at $t = 0.5$, delivery at $T = 1$, $r_b = 0.07$ for borrowing and $r_d = 0.… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[9].model[1]` | **1. The upper bound: cash and carry.** Sell the forward at $F$ and buy the share with two loans at 7%. - *To… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[9].model[2]` | So any quote above 67.2387 is money from nothing, and no arbitrage needs $$\begin{aligned} F &\le \left(S_0 -… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[9].model[3]` | **2. The lower bound: reverse cash and carry.** Buy the forward at $F$, sell a borrowed share for £64.00 and … | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[9].model[4]` | So any quote below 64.2021 is money from nothing, and no arbitrage needs $$\begin{aligned} F &\ge \left(S_0 -… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[9].model[5]` | With two rates and a fee, no arbitrage fixes a band, not a price: from £64.20 to £67.24. Inside it each plan … | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[9].model[6]` | **3. One rate and no fee.** Put $r_b = r_d = r$ and the fee at 0. Both bounds become $$F = \left(S_0 - D(1 + … | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[9].model[7]` | **Optional: a quote of £67.80.** It is above the upper bound, so run cash and carry: sell forward at £67.80, … | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[9].rubric[0]` | Part 1: shows that any quote above $\left(S_0 - D(1.07)^{-0.5}\right) \times 1.07$, about £67.24, gives a ris… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[9].rubric[1]` | Part 2: shows that any quote below $\left(S_0 - D(1.03)^{-0.5}\right) \times 1.03 - 0.50$, about £64.20, give… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[9].rubric[2]` | Part 3: shows that with one rate $r$ and no fee both bounds equal $\left(S_0 - D(1 + r)^{-t}\right)(1 + r)^T$… | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
| `items[9].rubric[3]` | Optional part: names cash and carry for a quote of £67.80 and finds a profit of about £0.56 a share. | correct | Recomputed in the concepts script or by hand; Hull 10e §2.4, §5.2, §5.4–5.6, §5.11; BKM ch. 3 §3.8–3.9 |
