# Claim ledger: exp-log levels 1 to 3 (audit round 1)

Stage 0 depth (docs/briefs/concept-audit.md): definitions, rules, always/never claims, conventions, and every graded key, wrong option and slip. Commit audited: 461a68d2. Script: `docs/reports/exp-log-L1-3-concepts.py`. Sources: Gelfand and Shen, *Algebra*; a standard A-level pure mathematics text; Rudin, *Principles of Mathematical Analysis* (3.31, e as a limit); Hull, *Options, Futures and Other Derivatives* (ch. 4 compounding, ch. 15 volatility); Tsay, *Analysis of Financial Time Series* (sec. 1.1 returns).

Rows: 1102. Verdicts: correct 1089, imprecise 9, misleading 3, wrong 1, unverified 0.

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l1-doubling | screens[2].prose | n twos multiplied is 2^n; 2 is the base, n the power or index | correct | Gelfand and Shen, Algebra, sec. 20 (powers); definition |
| l1-doubling | screens[4].explain | 2^0 = 1: zero doublings leave the start untouched | correct | Gelfand and Shen sec. 21 (a^0 = 1 keeps a^m a^n = a^(m+n)) |
| l1-doubling | screens[7].prose | a x 2^n after n doublings; steady addition gives a + dn; repeated multiplication by one factor is exponential… | correct | definition; A-level pure (exponential models) |
| l1-doubling | screens[8].explain | doubling the time squares the growth factor: 2^10 = 2^5 x 2^5 | correct | index law a^(2n) = (a^n)^2 |
| l1-doubling | summary.trap | half the final amount is one doubling back, not half the time | correct | 2^(n-1) = 2^n / 2 |
| l1-doubling | quiz[q-race].explain | doubling passes 100 a step at step 10 (B also leads at step 0, 1 against 0; A leads steps 1 to 9) | correct | concepts script: first step after 0 with 2^k > 100k is 10 |
| l1-doubling | screens[0].options[a] | Pot A | correct | wrong option, wrong under every convention: You carried on the first three days. A leads early, but B's daily gain doubles while A's stays at £… |
| l1-doubling | screens[0].options[b] (key) | Pot B | correct | derivation: Pot B ends with £1,024.00 against pot A's £101.00. |
| l1-doubling | screens[0].options[same] | About the same | correct | wrong option, wrong under every convention: You expected the two to even out. By day 10, B holds about ten times as much as A. |
| l1-doubling | screens[1].widget.answer | key 6 | correct | recomputed: Day 6: B holds £64.00, A holds £61.00. |
| l1-doubling | screens[1].wrong[day5] | slip 5 | correct | slip reproduced: On day 5, B holds £32.00 and A holds £51.00. B is still behind. |
| l1-doubling | screens[1].wrong[day7] | slip 7 | correct | slip reproduced: B is ahead on day 7, but it already got ahead a day earlier. Check day 6. |
| l1-doubling | screens[1].wrong[day4] | slip 4 | correct | slip reproduced: On day 4, B holds £16.00 and A holds £41.00. B is well behind. |
| l1-doubling | screens[2].options[pow] (key) | $2^6$ | correct | derivation: $2^6 = 64$: six doublings of £1.00. |
| l1-doubling | screens[2].options[times] | $2 \times 6$ | correct | wrong option, wrong under every convention: You multiplied 2 by 6 once, which gives 12. Six doublings multiply by 2 six times over. |
| l1-doubling | screens[2].options[swap] | $6^2$ | correct | wrong option, wrong under every convention: You swapped the base and the power. $6^2 = 6 \times 6 = 36$. |
| l1-doubling | screens[2].options[off] | $2^5$ | correct | wrong option, wrong under every convention: You counted from day 1. Day 0 holds £1.00 before any doubling, so day 6 is six doublings. |
| l1-doubling | screens[3].widget.answer | key 128 | correct | recomputed: £128.00, which is $2^7$. |
| l1-doubling | screens[3].wrong[plus2] | slip 65.5..66.5 | correct | slip reproduced: You added 2 to £64.00. Doubling multiplies by 2, so £64.00 becomes £128.00. |
| l1-doubling | screens[3].wrong[potA] | slip 73.5..74.5 | correct | slip reproduced: You added £10.00, which is pot A's rule. Pot B doubles: £64.00 becomes £128.00. |
| l1-doubling | screens[4].widget.answer | key 1 | correct | recomputed: $2^0 = 1$: no doubling yet. |
| l1-doubling | screens[4].wrong[zero] | slip 0 | correct | slip reproduced: You read a power of 0 as a value of 0. Zero doublings change nothing, so the pot still holds £1.00. |
| l1-doubling | screens[4].wrong[two] | slip 2 | correct | slip reproduced: You doubled once. Day 0 comes before the first doubling. |
| l1-doubling | screens[5].widget.answer | key 80 | correct | recomputed: $5 \times 2^4 = 5 \times 16 = 80$. |
| l1-doubling | screens[5].wrong[base10] | slip 10000 | correct | slip reproduced: You worked out $(5 \times 2)^4 = 10^4$. Only the 2 is raised to the power; the 5 multiplies once. |
| l1-doubling | screens[5].wrong[plus] | slip 21 | correct | slip reproduced: You added the £5.00 start to $2^4 = 16$. The start is multiplied: £5.00 doubled four times. |
| l1-doubling | screens[5].wrong[three] | slip 40 | correct | slip reproduced: That is day 3. Day 4 doubles it once more. |
| l1-doubling | screens[6].options[d15] | Day 15 | correct | wrong option, wrong under every convention: You halved the 30 days. Halving the cover means undoing one doubling, so it is one day back. |
| l1-doubling | screens[6].options[d29] (key) | Day 29 | correct | derivation: Day 29: one doubling short of full. |
| l1-doubling | screens[6].options[d28] | Day 28 | correct | wrong option, wrong under every convention: Day 28 is two doublings back from full, so the pond is a quarter covered then. |
| l1-doubling | screens[7].options[lin] (key) | $1 + 10n$ | correct | derivation: Adding gives $1 + 10n$; doubling gives $2^n$. |
| l1-doubling | screens[7].options[pow10] | $1 \times 10^n$ | correct | wrong option, wrong under every convention: You multiplied by 10 each day. Pot A adds £10.00 a day, so the tens pile up as $10n$. |
| l1-doubling | screens[7].options[potb] | $1 \times 2^n$ | correct | wrong option, wrong under every convention: That is pot B's rule. Pot A never doubles; it adds the same £10.00 each day. |
| l1-doubling | screens[8].widget.answer | order s1 > s2 > s3 > s4 | correct | each line follows from the one before; The second five days multiply by 32 again. |
| l1-doubling | screens[9].widget.answer | key 1024 | correct | recomputed: $2^{10} = 1024$: ten doublings after the first £1.00. |
| l1-doubling | screens[9].wrong[eleven] | slip 2048 | correct | slip reproduced: You doubled eleven times. Bet 1 is already £1.00, so bet 11 comes after ten doublings. |
| l1-doubling | screens[9].wrong[nine] | slip 512 | correct | slip reproduced: You stopped one doubling short. Bet 10 stakes £512.00 and bet 11 doubles it. |
| l1-doubling | screens[9].wrong[times] | slip 20 | correct | slip reproduced: You multiplied 2 by 10. Ten doublings multiply by 2 ten times: $2^{10}$. |
| l1-doubling | quiz[q-three-four].widget.answer | key 81 | correct | recomputed: $3 \times 3 \times 3 \times 3 = 81$. |
| l1-doubling | quiz[q-three-four].wrong[times] | slip 12 | correct | slip reproduced: You multiplied 3 by 4. The power 4 means four 3s multiplied. |
| l1-doubling | quiz[q-three-four].wrong[swap] | slip 64 | correct | slip reproduced: You worked out $4^3$. The base is 3 and the power is 4. |
| l1-doubling | quiz[q-ten-days].options[sq] (key) | 1,024 times | correct | derivation: $32 \times 32 = 1024$. |
| l1-doubling | quiz[q-ten-days].options[dbl] | 64 times | correct | wrong option, wrong under every convention: You doubled the 32 because the time doubled. The second five years multiply by 32 again. |
| l1-doubling | quiz[q-ten-days].options[add] | 42 times | correct | wrong option, wrong under every convention: You added one per extra year. Each extra year doubles the value. |
| l1-doubling | quiz[q-race].options[b] (key) | Plan B | correct | derivation: $2^{20} = 1{,}048{,}576$ against 2,000. |
| l1-doubling | quiz[q-race].options[a] | Plan A | correct | wrong option, wrong under every convention: You judged by the early steps, where A leads. After 20 steps A reaches 2,000, while B reaches $2^{2… |
| l1-doubling | quiz[q-race].options[tie] | They are equal | correct | wrong option, wrong under every convention: You expected the plans to meet and stay level. Once B gets ahead, its lead grows every step. |
| l1-doubling | quiz[q-seven-zero].widget.answer | key 1 | correct | recomputed: $7^0 = 1$: no factors of 7 at all. |
| l1-doubling | quiz[q-seven-zero].wrong[zero] | slip 0 | correct | slip reproduced: You read a power of 0 as a value of 0. Multiplying by no 7s leaves 1. |
| l1-doubling | quiz[q-seven-zero].wrong[seven] | slip 7 | correct | slip reproduced: You used one factor of 7. A power of 0 uses none. |
| l2-growth-factors | screens[2].prose | growth factor = 1 + rate; +10% is 1.1, -10% is 0.9 | correct | A-level pure, percentage multipliers |
| l2-growth-factors | screens[3].explain | every fall between 0% and 100% gives a factor between 0 and 1: decay | correct | 0 < 1 - r < 1 for 0 < r < 1 |
| l2-growth-factors | screens[5].explain | 100% fall has factor 0; only factors above 0 give growth or decay | correct | derivation: V g^n = 0 for g = 0 |
| l2-growth-factors | screens[6].explain | decay by a factor never reaches zero | correct | g^n > 0 for g > 0, all n |
| l2-growth-factors | screens[7].prose | V_n = V_0 (1 + r)^n with r negative for a fall; g > 1 grows, 0 < g < 1 decays, g = 1 stays | correct | compound growth formula; A-level pure (geometric sequences) |
| l2-growth-factors | screens[9].feedback.byKey.gain2 | second ten years gain 1,024.41 (difference of the displayed balances; exact 1,024.40) | correct | concepts script; penny difference from rounding only |
| l2-growth-factors | summary.ideas[2] | percentage changes do not add; each acts on the value it meets | correct | 1.1 x 0.9 = 0.99 |
| l2-growth-factors | screens[0].widget.answer | key 99 | correct | recomputed: £99.00: the fall is 10% of £110.00. |
| l2-growth-factors | screens[0].wrong[back] | slip 99.75..100.25 | correct | slip reproduced: You took £10.00 off, which is 10% of £100.00. Tuesday's fall is 10% of £110.00, which is £11.00. |
| l2-growth-factors | screens[1].widget.answer | key 1 | correct | recomputed: Multiplying by 1 leaves £100.00 each day. |
| l2-growth-factors | screens[1].wrong[zero] | slip 0 | correct | slip reproduced: You thought of no change as adding 0. These numbers multiply, and multiplying by 0 wipes the value … |
| l2-growth-factors | screens[2].widget.answer | key 1.05 | correct | recomputed: $1 + 0.05 = 1.05$. |
| l2-growth-factors | screens[2].wrong[rate] | slip 0.05 | correct | slip reproduced: You wrote the rate, 0.05. Multiplying by 0.05 keeps only 5% of the fund. The factor keeps the whole… |
| l2-growth-factors | screens[2].wrong[five] | slip 5 | correct | slip reproduced: You used the 5 from 5% as the factor. Multiplying by 5 is a 400% rise. |
| l2-growth-factors | screens[2].wrong[half] | slip 1.5 | correct | slip reproduced: You read 5% as 0.5. 5% is 0.05, so the factor is 1.05. |
| l2-growth-factors | screens[3].widget.answer | key 0.85 | correct | recomputed: $1 - 0.15 = 0.85$: 85% is left. |
| l2-growth-factors | screens[3].wrong[lost] | slip 0.15 | correct | slip reproduced: You wrote the part that is lost. The factor is the part that stays: $1 - 0.15$. |
| l2-growth-factors | screens[3].wrong[plus] | slip 1.15 | correct | slip reproduced: You added the 15%. A fall subtracts: $1 - 0.15 = 0.85$. |
| l2-growth-factors | screens[4].widget.answer | key 1024 | correct | recomputed: $2000 \times 0.8^3 = 1024$. |
| l2-growth-factors | screens[4].wrong[sum] | slip 800 | correct | slip reproduced: You took 60% off in one go: three lots of 20% of £2,000.00. Each fall is 20% of a smaller value. |
| l2-growth-factors | screens[4].wrong[two] | slip 1280 | correct | slip reproduced: That is after two years. Apply 0.8 once more. |
| l2-growth-factors | screens[4].wrong[rate] | slip 16 | correct | slip reproduced: You multiplied by 0.2, the part lost, each year. The factor is the part kept, 0.8. |
| l2-growth-factors | screens[5].widget.answer | key 2 | correct | recomputed: $1 + 1 = 2$: a 100% rise doubles. |
| l2-growth-factors | screens[5].wrong[one] | slip 1 | correct | slip reproduced: You turned 100% into 1 and stopped. The factor keeps the original too: $1 + 1 = 2$. |
| l2-growth-factors | screens[5].wrong[hundred] | slip 100 | correct | slip reproduced: You used 100 as the factor. Multiplying by 100 is a 9,900% rise. |
| l2-growth-factors | screens[6].options[zero] | £0.00 | correct | wrong option, wrong under every convention: You added ten 10% falls to make 100%. Each fall is 10% of a smaller price, so it never reaches zero. |
| l2-growth-factors | screens[6].options[penny] | Less than 1p | correct | wrong option, wrong under every convention: You multiplied by 0.1 each day, the part lost. The part that stays is 0.9. |
| l2-growth-factors | screens[6].options[right] (key) | £34.87 | correct | derivation: $100 \times 0.9^{10} \approx 34.87$. |
| l2-growth-factors | screens[6].options[once] | £90.00 | correct | wrong option, wrong under every convention: You applied one fall. The price falls on each of the ten days. |
| l2-growth-factors | screens[7].options[right] (key) | $0.96$ | correct | derivation: $g = 1 - 0.04 = 0.96$. |
| l2-growth-factors | screens[7].options[sign] | $1.04$ | correct | wrong option, wrong under every convention: You added the 4%. A fall makes $r$ negative: $1 - 0.04$. |
| l2-growth-factors | screens[7].options[rate] | $0.04$ | correct | wrong option, wrong under every convention: You wrote the part lost. The factor is the part kept. |
| l2-growth-factors | screens[7].options[tenth] | $0.6$ | correct | wrong option, wrong under every convention: You read 4% as 0.4. 4% is 0.04, so the factor is 0.96. |
| l2-growth-factors | screens[8].widget.answer | order s0 > s1 > s2 > sn | correct | each line follows from the one before; Each step adds one more factor of $g$. |
| l2-growth-factors | screens[9].widget.answer | key 2653.3 | correct | recomputed: $1000 \times 1.05^{20} \approx 2653.30$. |
| l2-growth-factors | screens[9].wrong[simple] | slip 2000 | correct | slip reproduced: You added £50.00 a year for 20 years. Each year's 5% is of a bigger balance, so the gains grow. |
| l2-growth-factors | screens[9].wrong[times] | slip 21000 | correct | slip reproduced: You multiplied 1.05 by 20. The factor is applied 20 times over: $1.05^{20}$. |
| l2-growth-factors | screens[9].wrong[double10] | slip 3257.78 | correct | slip reproduced: You doubled the year 10 value because the time doubled. The second 10 years multiply by 1.6289 agai… |
| l2-growth-factors | screens[9].wrong[gain2] | slip 2257.78 | correct | slip reproduced: You doubled the first 10 years' gain. The second 10 years earn 5% on a bigger balance, so they gain… |
| l2-growth-factors | quiz[q-twelve].widget.answer | key 1.12 | correct | recomputed: $1 + 0.12 = 1.12$. |
| l2-growth-factors | quiz[q-twelve].wrong[rate] | slip 0.12 | correct | slip reproduced: You wrote the rate. The factor keeps the whole salary too: 1.12. |
| l2-growth-factors | quiz[q-twelve].wrong[twelve] | slip 12 | correct | slip reproduced: You used 12 as the factor. 12% is 0.12. |
| l2-growth-factors | quiz[q-car].widget.answer | key 14450 | correct | recomputed: $20000 \times 0.85^2 = 14450$. |
| l2-growth-factors | quiz[q-car].wrong[sum] | slip 14000 | correct | slip reproduced: You took 30% off in one go. The second year's 15% is of £17,000.00, not £20,000.00. |
| l2-growth-factors | quiz[q-car].wrong[one] | slip 17000 | correct | slip reproduced: That is after one year. Apply 0.85 again. |
| l2-growth-factors | quiz[q-up-down].options[flat] (key) | Back where it started | correct | derivation: $1.25 \times 0.8 = 1$: back where it started. |
| l2-growth-factors | quiz[q-up-down].options[up] | 5% up | correct | wrong option, wrong under every convention: You added +25% and −20%. The factors multiply: $1.25 \times 0.8 = 1$. |
| l2-growth-factors | quiz[q-up-down].options[down] | Below where it started | correct | wrong option, wrong under every convention: You expected a fall after a rise to leave a loss, as equal swings do. Here $1.25 \times 0.8 = 1$ ex… |
| l2-growth-factors | quiz[q-which-decay].options[d] (key) | $0.98$ | correct | derivation: 0.98 keeps 98% each day: a 2% decay. |
| l2-growth-factors | quiz[q-which-decay].options[g] | $1.02$ | correct | wrong option, wrong under every convention: Multiplying by 1.02 adds 2% a day. That is growth. |
| l2-growth-factors | quiz[q-which-decay].options[one] | $1$ | correct | wrong option, wrong under every convention: Multiplying by 1 leaves the value unchanged. It neither grows nor decays. |
| l2-growth-factors | quiz[q-which-decay].options[two] | $2$ | correct | wrong option, wrong under every convention: Multiplying by 2 doubles the value each day. |
| l3-strange-powers | screens[2].prose | a^(-n) = 1 / a^n, forced by a^m a^n = a^(m+n) | correct | Gelfand and Shen sec. 21-22 (negative powers) |
| l3-strange-powers | screens[3].explain | a half power is a square root (9^(1/2) = 3) | correct | Gelfand and Shen sec. 62 (rational powers) |
| l3-strange-powers | screens[6].explain | growth by powers is never a straight line between the dots | correct | strict convexity of a^x for a not 1 |
| l3-strange-powers | screens[7].prose | for a > 0: a^0 = 1, a^(-n) = 1/a^n, a^(1/n) = nth root, a^(m/n) = (nth root)^m | correct | A-level pure index laws; the domain a > 0 is stated, so negative bases with fractional powers are excluded |
| l3-strange-powers | screens[8].explain | a^(1/2) is the positive root, since powers of a positive base are positive | correct | convention of the principal root; b = (a^(1/4))^2 >= 0 |
| l3-strange-powers | quiz[q-half-neg].explain | a negative power of a number below 1 gives a number above 1 | imprecise | true for 0 < a < 1 only: (-2)^(-1) = -0.5 < 1 and 0^(-1) is undefined. Finding 7 |
| l3-strange-powers | summary.formula.note | for a > 0; the bottom of the fraction picks the root, a minus means one over | correct | as screens[7] |
| l3-strange-powers | screens[0].widget.answer | key 0.5 | correct | recomputed: Halving 1 gives $\tfrac{1}{2}$. |
| l3-strange-powers | screens[0].wrong[neg] | slip -2 | correct | slip reproduced: You put a minus sign on the 2. Each step down halves, so the value goes from 1 to a half. |
| l3-strange-powers | screens[0].wrong[zero] | slip 0 | correct | slip reproduced: You expected the values to hit zero after 1. Halving 1 gives 0.5, not 0. |
| l3-strange-powers | screens[0].wrong[negone] | slip -1 | correct | slip reproduced: You copied the power into the value column. The value halves at each step: 1 becomes 0.5. |
| l3-strange-powers | screens[1].widget.answer | key 0.125 | correct | recomputed: $2^{-3} = \tfrac{1}{8} = 0.125$. |
| l3-strange-powers | screens[1].wrong[neg8] | slip -8 | correct | slip reproduced: You made $2^3$ negative. A negative power undoes doublings by halving, so the value stays positive. |
| l3-strange-powers | screens[1].wrong[neg6] | slip -6 | correct | slip reproduced: You multiplied 2 by −3. The power counts halvings here: three of them. |
| l3-strange-powers | screens[1].wrong[zero] | slip 0 | correct | slip reproduced: You expected the dots to reach zero. Halving never gets to 0; the dots only creep towards it. |
| l3-strange-powers | screens[2].options[right] (key) | $\dfrac{1}{25}$ | correct | derivation: $5^{-2} = \dfrac{1}{5^2} = \dfrac{1}{25}$. |
| l3-strange-powers | screens[2].options[neg] | $-25$ | correct | wrong option, wrong under every convention: You made the answer negative. The minus in the power means divide, not a negative value. |
| l3-strange-powers | screens[2].options[times] | $-10$ | correct | wrong option, wrong under every convention: You multiplied 5 by −2. A power is not a product with the base. |
| l3-strange-powers | screens[2].options[tenth] | $\dfrac{1}{10}$ | correct | wrong option, wrong under every convention: You put $5 \times 2$ underneath. The 2 means $5 \times 5$ underneath: $\tfrac{1}{25}$. |
| l3-strange-powers | screens[3].widget.answer | key 3 | correct | recomputed: $9^{1/2} = 3$, because $3 \times 3 = 9$. |
| l3-strange-powers | screens[3].wrong[half] | slip 4.5 | correct | slip reproduced: You halved 9. Half a power is half the multiplying: the factor that, used twice, gives 9. |
| l3-strange-powers | screens[3].wrong[mid] | slip 5 | correct | slip reproduced: You took the midpoint of 1 and 9. Powers multiply, so the halfway value is the factor 3, not the av… |
| l3-strange-powers | screens[4].widget.answer | key 2 | correct | recomputed: $8^{1/3} = 2$, because $2^3 = 8$. |
| l3-strange-powers | screens[4].wrong[third] | slip 2.6667 | correct | slip reproduced: You divided 8 by 3. A third of a power is the factor that, used three times, gives 8. |
| l3-strange-powers | screens[4].wrong[sq] | slip 2.8284 | correct | slip reproduced: You took the square root. That needs two equal steps; here there are three. |
| l3-strange-powers | screens[5].widget.answer | key 0.25 | correct | recomputed: $16^{-1/2} = \dfrac{1}{\sqrt{16}} = \dfrac{1}{4}$. |
| l3-strange-powers | screens[5].wrong[neg] | slip -4 | correct | slip reproduced: You made the root negative. The minus in the power means one over: $\tfrac{1}{4}$. |
| l3-strange-powers | screens[5].wrong[dropped] | slip 4 | correct | slip reproduced: You took the square root but dropped the minus. The minus then puts it underneath: $\tfrac{1}{4}$. |
| l3-strange-powers | screens[5].wrong[negeight] | slip -8 | correct | slip reproduced: You multiplied 16 by $-\tfrac{1}{2}$. Powers are not products with the base. |
| l3-strange-powers | screens[6].options[avg] | $1.5$, the height of M | correct | wrong option, wrong under every convention: You averaged 1 and 2 along the ruler. Powers multiply: two equal half-steps must multiply 1 up to 2. |
| l3-strange-powers | screens[6].options[prod] | $1$ | correct | wrong option, wrong under every convention: You multiplied 2 by $\tfrac{1}{2}$. A power is not a product with the base. |
| l3-strange-powers | screens[6].options[right] (key) | About $1.414$ | correct | derivation: $2^{1/2} = \sqrt{2} \approx 1.414$. |
| l3-strange-powers | screens[6].options[recip] | $0.5$ | correct | wrong option, wrong under every convention: That is $2^{-1}$. A half power is a root, not a reciprocal. |
| l3-strange-powers | screens[7].options[right] (key) | $9$ | correct | derivation: $27^{2/3} = (\sqrt[3]{27})^2 = 3^2 = 9$. |
| l3-strange-powers | screens[7].options[times] | $18$ | correct | wrong option, wrong under every convention: You multiplied 27 by $\tfrac{2}{3}$. Take the cube root, 3, then square it. |
| l3-strange-powers | screens[7].options[root] | $3$ | correct | wrong option, wrong under every convention: You took the cube root and stopped. The 2 on top squares it: $3^2 = 9$. |
| l3-strange-powers | screens[7].options[recip] | $\dfrac{1}{9}$ | correct | wrong option, wrong under every convention: You turned it upside down, but there is no minus sign in the power. |
| l3-strange-powers | screens[8].widget.answer | order s1 > s2 > s3 > s4 > s5 | correct | each line follows from the one before; The law forces $b^2 = a$. |
| l3-strange-powers | screens[9].widget.answer | key 1.1 | correct | recomputed: $\sqrt{1.21} = 1.1$: 10% a year. |
| l3-strange-powers | screens[9].wrong[halved] | slip 1.105 | correct | slip reproduced: You split the 21% gain into 10.5% a year. Two years of that give $1.105^2 \approx 1.221$, too much. |
| l3-strange-powers | screens[9].wrong[half] | slip 0.605 | correct | slip reproduced: You halved the two-year factor. Two years multiply, so take the square root, not half. |
| l3-strange-powers | screens[9].wrong[total] | slip 1.21 | correct | slip reproduced: That is the factor for both years together. Each year applies its own factor. |
| l3-strange-powers | quiz[q-ten-neg].widget.answer | key 0.01 | correct | recomputed: $10^{-2} = \tfrac{1}{100} = 0.01$. |
| l3-strange-powers | quiz[q-ten-neg].wrong[neg] | slip -100 | correct | slip reproduced: You made $10^2$ negative. The minus in the power means one over: $\tfrac{1}{100}$. |
| l3-strange-powers | quiz[q-ten-neg].wrong[times] | slip -20 | correct | slip reproduced: You multiplied 10 by −2. Powers are not products with the base. |
| l3-strange-powers | quiz[q-root-25].widget.answer | key 5 | correct | recomputed: $5 \times 5 = 25$. |
| l3-strange-powers | quiz[q-root-25].wrong[half] | slip 12.5 | correct | slip reproduced: You halved 25. A half power is a square root: $\sqrt{25} = 5$. |
| l3-strange-powers | quiz[q-half-neg].options[right] (key) | $2$ | correct | derivation: One over $\tfrac{1}{2}$ is 2. |
| l3-strange-powers | quiz[q-half-neg].options[neg] | $-\tfrac{1}{2}$ | correct | wrong option, wrong under every convention: You made it negative. A power of −1 turns the number upside down. |
| l3-strange-powers | quiz[q-half-neg].options[same] | $\tfrac{1}{2}$ | correct | wrong option, wrong under every convention: You ignored the minus. One over $\tfrac{1}{2}$ is 2. |
| l3-strange-powers | quiz[q-eight-two-thirds].widget.answer | key 4 | correct | recomputed: $(\sqrt[3]{8})^2 = 2^2 = 4$. |
| l3-strange-powers | quiz[q-eight-two-thirds].wrong[times] | slip 5.3333 | correct | slip reproduced: You multiplied 8 by $\tfrac{2}{3}$. The 3 picks a cube root and the 2 squares it. |
| l3-strange-powers | quiz[q-eight-two-thirds].wrong[root] | slip 2 | correct | slip reproduced: You took the cube root and stopped. Square it too. |
| l4-exponential-curves | screens[0].explain | x-axis is an asymptote of y = 2^x; height positive for every x | correct | A-level pure, graph of a^x |
| l4-exponential-curves | screens[1].explain | every curve y = a^x passes through (0, 1) (slider a from 0.2 to 3) | correct | a^0 = 1 for a > 0 |
| l4-exponential-curves | screens[2].prose | a > 1 exponential growth, 0 < a < 1 exponential decay | correct | definition |
| l4-exponential-curves | screens[3].explain | 0.5^x = 2^(-x): decay curves mirror growth curves in the y-axis | correct | (1/a)^x = a^(-x) |
| l4-exponential-curves | screens[4].explain | a steady rate gives a constant doubling time | correct | a^(x+h) = a^x a^h, derived on screens[8] |
| l4-exponential-curves | screens[5].explain | half-life about 6.6 days; selling a fixed fraction never fully closes | correct | ln 0.5 / ln 0.9 = 6.58 |
| l4-exponential-curves | screens[6].explain | exponential growth beats every line eventually, however steep | correct | a^x / x -> infinity for a > 1 (Rudin 3.20(d) or A-level) |
| l4-exponential-curves | screens[7].prose | for a > 0, a not 1: through (0, 1), x-axis an asymptote, each step h multiplies y by a^h | correct | index law |
| l4-exponential-curves | screens[10].prose | rule of 72: divide 72 by the yearly rate in percent; an estimate (1.08^9 = 1.999) | correct | rate form stated (yearly, percent), called an estimate; ln 2 / ln(1+r) |
| l4-exponential-curves | screens[10].explain | without compounding doubling takes 100/6 = 16.7 years | correct | simple interest 1 + rt = 2 |
| l4-exponential-curves | quiz[q-eventually].explain | 1.01^x passes 1000x at x = 1,424 | correct | concepts script, first integer crossing |
| l4-exponential-curves | screens[0].options[never] (key) | It gets closer to 0 but never reaches it | correct | derivation: The height halves at each step left, so it never reaches 0. |
| l4-exponential-curves | screens[0].options[hits] | It reaches 0 at some negative $x$ | correct | wrong option, wrong under every convention: You pictured the curve meeting the axis. Each step left halves the height, and halving never gives … |
| l4-exponential-curves | screens[0].options[below] | It drops below 0 | correct | wrong option, wrong under every convention: You expected negative powers to give negative heights. $2^{-1} = 0.5$ is still positive. |
| l4-exponential-curves | screens[1].options[zero-one] (key) | $(0, 1)$ | correct | derivation: Every curve passes through $(0, 1)$, because $a^0 = 1$. |
| l4-exponential-curves | screens[1].options[origin] | $(0, 0)$ | correct | wrong option, wrong under every convention: You expected the curve to start at the origin. At $x = 0$ the height is $a^0 = 1$, never 0. |
| l4-exponential-curves | screens[1].options[one-one] | $(1, 1)$ | correct | wrong option, wrong under every convention: Only the flat curve with $a = 1$ passes there. At $x = 1$ the height is $a$, which moves with the s… |
| l4-exponential-curves | screens[2].widget.answer | key 4 | correct | recomputed: $0.5^{-2} = \dfrac{1}{0.5^2} = \dfrac{1}{0.25} = 4$. |
| l4-exponential-curves | screens[2].wrong[pos] | slip 0.25 | correct | slip reproduced: You worked out $0.5^2$. The power is −2, so the height is one over that: 4. |
| l4-exponential-curves | screens[2].wrong[times] | slip -1 | correct | slip reproduced: You multiplied 0.5 by −2. The height is a power, and powers of 0.5 stay positive. |
| l4-exponential-curves | screens[3].widget.points | target [-3, 8] | correct | recomputed: $0.5^{-3} = 2^3 = 8$. |
| l4-exponential-curves | screens[3].wrong[same] | region {"x": [2.5, 3.5], "y": [7, 9]} | correct | region is clear of the target band; You put D on P. That point is on $2^x$; at $x = 3$, $0.5^3 = 0.125$. |
| l4-exponential-curves | screens[3].wrong[low] | region {"x": [2.5, 3.5], "y": [-0.5, 1]} | correct | region is clear of the target band; That is $0.5^3 = 0.125$, the right height for $x = 3$, but the question asks for height 8. |
| l4-exponential-curves | screens[4].widget.answer | key 8 | correct | recomputed: 8 years: every doubling takes the same time. |
| l4-exponential-curves | screens[4].wrong[perpound] | slip 32 | correct | slip reproduced: You gave each pound gained the same time. Growth here is by a factor, and £4,000.00 doubles as fast… |
| l4-exponential-curves | screens[4].wrong[fromstart] | slip 24 | correct | slip reproduced: That is the year it reaches £8,000.00, counted from the start. The question starts the clock at P. |
| l4-exponential-curves | screens[5].widget.answer | key 7 | correct | recomputed: Day 7: about 4,783 shares left. |
| l4-exponential-curves | screens[5].wrong[linear] | slip 5 | correct | slip reproduced: You sold 1,000 shares a day, 10% of the start. Each sale is 10% of what is left, so it shrinks. |
| l4-exponential-curves | screens[5].wrong[six] | slip 6 | correct | slip reproduced: After 6 days 5,314 shares are left, still just over half. |
| l4-exponential-curves | screens[6].options[never] | Yes, the curve never catches the line | correct | wrong option, wrong under every convention: You judged the race by the early steps. The line adds 100 a step, but the curve doubles, and doubli… |
| l4-exponential-curves | screens[6].options[right] (key) | No, the curve overtakes it between $x = 9$ and $x = 10$ | correct | derivation: $2^{10} = 1024$ beats $100 \times 10 = 1000$. |
| l4-exponential-curves | screens[6].options[seven] | No, the curve overtakes it between $x = 6$ and $x = 7$ | correct | wrong option, wrong under every convention: At $x = 7$ the curve is 128 and the line is 700. Check both values at each step. |
| l4-exponential-curves | screens[6].options[back] | No, but the line pulls back ahead later | correct | wrong option, wrong under every convention: You expected the lead to swap back. Once the curve's step-gain passes 100, its lead only grows. |
| l4-exponential-curves | screens[7].options[right] (key) | It passes through $(0, 1)$ and falls towards 0 without reaching it | correct | derivation: $(0, 1)$, then decay towards the asymptote. |
| l4-exponential-curves | screens[7].options[zero] | It falls from $(0, 1)$ and reaches 0 at $x = 5$ | correct | wrong option, wrong under every convention: You took off 0.2 per step, five times. Each step multiplies by 0.8, which never gives 0. |
| l4-exponential-curves | screens[7].options[int] | It passes through $(0, 0.8)$ and falls towards 0 | correct | wrong option, wrong under every convention: At $x = 0$ the power is 0, and $0.8^0 = 1$. |
| l4-exponential-curves | screens[8].widget.answer | order s1 > s2 > s3 > s4 | correct | each line follows from the one before; The factor $a^h$ does not depend on $x$. |
| l4-exponential-curves | screens[9].widget.answer | key 18166.97 | correct | recomputed: $10000 \times 1.01^{60} \approx 18166.97$. |
| l4-exponential-curves | screens[9].wrong[flat] | slip 16000 | correct | slip reproduced: That is strategy B. A's 1% is of a growing balance, so its monthly gain grows. |
| l4-exponential-curves | screens[9].wrong[yearly] | slip 17623.42 | correct | slip reproduced: You turned 1% a month into 12% a year. Monthly compounding gives a little more: $1.01^{12} \approx … |
| l4-exponential-curves | screens[9].wrong[times] | slip 606000 | correct | slip reproduced: You multiplied by 1.01 and by 60: $10000 \times 1.01 \times 60 = 606000$. The factor is applied 60 … |
| l4-exponential-curves | screens[10].widget.answer | key 2012.2 | correct | recomputed: $1000 \times 1.06^{12} \approx 2012.20$: very close to double. |
| l4-exponential-curves | screens[10].wrong[simple] | slip 1720 | correct | slip reproduced: You added £60.00 a year. That is simple interest, which takes 16.7 years to double. Compounding tak… |
| l4-exponential-curves | screens[10].wrong[exact] | slip 2000 | correct | slip reproduced: You took the rule as exact. It is an estimate: $1.06^{12} \approx 2.012$, just over double. |
| l4-exponential-curves | quiz[q-intercept].widget.answer | key 1 | correct | recomputed: $5^0 = 1$. |
| l4-exponential-curves | quiz[q-intercept].wrong[five] | slip 5 | correct | slip reproduced: You used $x = 1$. The y-axis is where $x = 0$, and $5^0 = 1$. |
| l4-exponential-curves | quiz[q-intercept].wrong[zero] | slip 0 | correct | slip reproduced: You expected the curve to start at the origin. $5^0 = 1$, not 0. |
| l4-exponential-curves | quiz[q-never-zero].options[no] (key) | No: $3^x$ is positive for every $x$ | correct | derivation: The x-axis is an asymptote: never reached. |
| l4-exponential-curves | quiz[q-never-zero].options[neg] | Yes, a large negative $x$ | correct | wrong option, wrong under every convention: You followed the curve towards the axis. It gets as close as you like, but $3^{-n} = \tfrac{1}{3^n}… |
| l4-exponential-curves | quiz[q-never-zero].options[zero] | Yes, $x = 0$ | correct | wrong option, wrong under every convention: $3^0 = 1$, not 0. |
| l4-exponential-curves | quiz[q-halving].widget.answer | key 1000 | correct | recomputed: Three halvings: 8,000, 4,000, 2,000, 1,000. |
| l4-exponential-curves | quiz[q-halving].wrong[third] | slip 2667 | correct | slip reproduced: You divided by 3 for three half-lives. Each half-life halves: divide by $2^3 = 8$. |
| l4-exponential-curves | quiz[q-halving].wrong[two] | slip 2000 | correct | slip reproduced: That is after 8 days, two halvings. 12 days is three. |
| l4-exponential-curves | quiz[q-halving].wrong[linear] | slip 0 | correct | slip reproduced: You took 4,000 shares off each half-life. Each halving removes half of what is left. |
| l4-exponential-curves | quiz[q-eventually].options[exp] (key) | $1.01^x$ | correct | derivation: Exponential growth beats any line eventually. |
| l4-exponential-curves | quiz[q-eventually].options[lin] | $1000x$ | correct | wrong option, wrong under every convention: You judged by the size of the numbers in the rules. Any growth factor above 1 beats any line in the… |
| l4-exponential-curves | quiz[q-eventually].options[tie] | They stay roughly equal | correct | wrong option, wrong under every convention: You expected the two to settle level. Once the curve gains more than 1,000 a step, the gap only wid… |
| review-1 | items[r-two-eight].widget.answer | key 256 | correct | recomputed: $2^8 = 256$. |
| review-1 | items[r-two-eight].wrong[times] | slip 16 | correct | slip reproduced: You multiplied 2 by 8. Eight doublings multiply by 2 eight times over. |
| review-1 | items[r-two-eight].wrong[swap] | slip 64 | correct | slip reproduced: You worked out $8^2$. The base is 2 and the power is 8. |
| review-1 | items[r-two-eight].wrong[seven] | slip 128 | correct | slip reproduced: You stopped one doubling short. Day 0 holds £1.00, so day 8 is eight doublings. |
| review-1 | items[r-fall-seven].widget.answer | key 0.93 | correct | recomputed: $1 - 0.07 = 0.93$. |
| review-1 | items[r-fall-seven].wrong[rate] | slip 0.07 | correct | slip reproduced: You wrote the part lost. The factor is the part kept: $1 - 0.07$. |
| review-1 | items[r-fall-seven].wrong[plus] | slip 1.07 | correct | slip reproduced: You added the 7%. A fall subtracts. |
| review-1 | items[r-fall-seven].wrong[tenth] | slip 0.3 | correct | slip reproduced: You read 7% as 0.7. 7% is 0.07. |
| review-1 | items[r-four-neg].widget.answer | key 0.25 | correct | recomputed: $4^{-1} = \tfrac{1}{4}$. |
| review-1 | items[r-four-neg].wrong[neg] | slip -4 | correct | slip reproduced: You made the 4 negative. The minus in the power means one over: $\tfrac{1}{4}$. |
| review-1 | items[r-four-neg].wrong[tenth] | slip 0.4 | correct | slip reproduced: You turned 4 into 0.4. One over 4 is 0.25. |
| review-1 | items[r-quarter-curve].widget.answer | key 4 | correct | recomputed: $0.25^{-1} = \dfrac{1}{0.25} = 4$. |
| review-1 | items[r-quarter-curve].wrong[same] | slip 0.25 | correct | slip reproduced: You used $x = 1$. At $x = -1$ the power is negative, so the height is one over 0.25. |
| review-1 | items[r-quarter-curve].wrong[neg] | slip -0.25 | correct | slip reproduced: You made the height negative. Exponential curves stay above the x-axis. |
| review-1 | items[r-savings].widget.answer | key 624.32 | correct | recomputed: $5000 \times 1.04^3 - 5000 = 624.32$. |
| review-1 | items[r-savings].wrong[simple] | slip 600 | correct | slip reproduced: You added £200.00 a year. Each year's 4% is of a bigger balance, so the interest grows. |
| review-1 | items[r-savings].wrong[balance] | slip 5624.32 | correct | slip reproduced: That is the balance. The interest is the balance minus the £5,000.00 he put in. |
| review-1 | items[r-savings].wrong[two] | slip 408 | correct | slip reproduced: That is two years of interest. Apply 1.04 once more: £5,624.32 in all. |
| review-1 | items[r-three-fifths].widget.answer | key 8 | correct | recomputed: $(\sqrt[5]{32})^3 = 2^3 = 8$. |
| review-1 | items[r-three-fifths].wrong[times] | slip 19.2 | correct | slip reproduced: You multiplied 32 by $\tfrac{3}{5}$. The 5 picks a fifth root and the 3 cubes it. |
| review-1 | items[r-three-fifths].wrong[root] | slip 2 | correct | slip reproduced: You took the fifth root and stopped. Cube it too. |
| review-1 | items[r-tripling].widget.answer | key 6 | correct | recomputed: 6 years: every tripling takes the same time. |
| review-1 | items[r-tripling].wrong[linear] | slip 18 | correct | slip reproduced: You gave each pound the same time: £20.00 per 6 years. Growth here is by a factor, and £30.00 tripl… |
| review-1 | items[r-tripling].wrong[total] | slip 12 | correct | slip reproduced: That counts from the start. The question asks for more years after £30.00. |
| review-1 | items[r-million].options[million] (key) | About a million times | correct | derivation: $2^{20} = 2^{10} \times 2^{10} \approx 1000 \times 1000$. |
| review-1 | items[r-million].options[twothousand] | About 2,000 times | correct | wrong option, wrong under every convention: You doubled the thousand because the doublings doubled. The second ten multiply by about a thousand… |
| review-1 | items[r-million].options[tenthousand] | About 10,000 times | correct | wrong option, wrong under every convention: You multiplied the thousand by 10. Twenty doublings are two blocks of ten: a thousand times a thous… |
| review-1 | items[r-losing-strategy].widget.answer | key 35 | correct | recomputed: $0.98^{35} \approx 0.493$. |
| review-1 | items[r-losing-strategy].wrong[linear] | slip 25 | correct | slip reproduced: You lost 2% of the start each day: 25 days to lose half. Each loss is 2% of what is left, so it tak… |
| review-1 | items[r-losing-strategy].wrong[close] | slip 34 | correct | slip reproduced: After 34 days $0.98^{34} \approx 0.503$ is left, still just over half. |
| review-1 | items[r-years-ago].widget.answer | key 8 | correct | recomputed: $27 \times 1.5^{-3} = \dfrac{27}{3.375} = 8$. |
| review-1 | items[r-years-ago].wrong[divlin] | slip 6 | correct | slip reproduced: You divided by $1.5 \times 3$. Three years back divide by 1.5 three times: by $1.5^3 = 3.375$. |
| review-1 | items[r-years-ago].wrong[forward] | slip 91.13 | correct | slip reproduced: You went forward 3 years. Back in time uses the power −3. |
| review-1 | items[r-years-ago].wrong[subtract] | slip 3.375 | correct | slip reproduced: You took 50% off for each year back: $27 \times 0.5^3 = 3.375$. Undoing a 50% rise divides by 1.5, … |
| homework-1 | items[h-long-compound].model | V_n = 5000 x 1.05^n; 8,144.47; 13,266.49; simple 10,000.00; rule of 72 gives 14.4, true crossing between year… | correct | concepts script |
| homework-1 | items[h-derive-beats-flat] | A gains 100 x 1.01^(n-1) in month n, more than 100 from month 2 | correct | 1.01^(n-1) > 1 for n >= 2 |
| homework-1 | items[h-write-rule].widget.answer | key 2500\cdot1.06^{n} | correct | derivation: $2500 \times 1.06^n$. |
| homework-1 | items[h-write-rule].wrong[rate] | slip 2500\cdot0.06^{n} | correct | not equivalent to the key; You raised the rate, 0.06, to the power. The factor is $1 + 0.06 = 1.06$. |
| homework-1 | items[h-write-rule].wrong[simple] | slip 2500(1+0.06n) | correct | not equivalent to the key; That is simple interest: £150.00 added each year. Compounding multiplies by 1.06 each year. |
| homework-1 | items[h-write-rule].wrong[times] | slip 2500\cdot1.06n | correct | not equivalent to the key; You multiplied 1.06 by $n$. The factor is applied $n$ times, so it is a power. |
| homework-1 | items[h-rule-72-check].widget.answer | key 1.99 | correct | recomputed: $1.09^8 \approx 1.99$: very nearly double. |
| homework-1 | items[h-rule-72-check].wrong[simple] | slip 1.72 | correct | slip reproduced: You added 9% eight times: $1 + 8 \times 0.09$. Compounding multiplies by 1.09 eight times. |
| homework-1 | items[h-rule-72-check].wrong[exact] | slip 2 | correct | slip reproduced: The rule is an estimate. Work out $1.09^8$ itself; it is just under 2. |
| homework-1 | items[h-monthly-rate].widget.answer | key 0.01 (unit %) | correct | recomputed: $1.1268^{1/12} \approx 1.0100$: 1.00% a month. |
| homework-1 | items[h-monthly-rate].wrong[divide] | slip 0.010567 | correct | slip reproduced: You divided 12.68% by 12. Monthly factors multiply, so take the twelfth root of 1.1268. |
| homework-1 | items[h-unwind-twenty].widget.answer | key 4 | correct | recomputed: $0.8^4 = 0.4096$. |
| homework-1 | items[h-unwind-twenty].wrong[three] | slip 3 | correct | slip reproduced: After 3 days $0.8^3 = 0.512$ is left, just over half. Each sale is 20% of what remains, not of the … |
| homework-1 | items[h-derive-beats-flat].widget.answer | order s1 > s2 > s3 > s4 > s5 | correct | each line follows from the one before; A's monthly gain grows; B's stays fixed. |
| homework-1 | items[h-biggest].options[exp] (key) | $2^x$ | correct | derivation: $2^{30} = 1073741824$. |
| homework-1 | items[h-biggest].options[lin] | $1000x$ | correct | wrong option, wrong under every convention: You trusted the big coefficient. $1000 \times 30 = 30000$, but $2^{30}$ is over a billion. |
| homework-1 | items[h-biggest].options[cube] | $x^3$ | correct | wrong option, wrong under every convention: $30^3 = 27000$. A fixed power of $x$ grows far slower than $2^x$. |
| homework-1 | items[h-biggest].options[sq] | $30^2$ | correct | wrong option, wrong under every convention: That is 900, the smallest here. |
| homework-1 | items[h-overtake].widget.answer | key 78 | correct | recomputed: Month 78: £21,730.37 against £21,700.00. |
| homework-1 | items[h-overtake].wrong[gain] | slip 41 | correct | slip reproduced: You found when A's monthly gain first passes £150.00, when its balance passes £15,000.00. A is stil… |
| homework-1 | items[h-overtake].wrong[gain40] | slip 40 | correct | slip reproduced: You found roughly when A's monthly gain reaches £150.00. A is still behind in total, after many mon… |
| homework-1 | items[h-overtake].wrong[before] | slip 77 | correct | slip reproduced: At month 77 A holds £21,515.22 and B £21,550.00. A is still £34.78 behind. |
| problems-1 | items[p-yeast-culture].parts[0].widget.answer | key 3000\cdot2^{n} | correct | derivation: Each hour multiplies by 2, so $n$ hours multiply by $2^n$: $N = 3000 \times 2^n$. |
| problems-1 | items[p-yeast-culture].parts[0].wrong[base-times] | slip 6000^{n} | correct | not equivalent to the key; You raised $3000 \times 2$ to the power. Only the 2 is repeated, so the rule is $3000 \times 2^n$. |
| problems-1 | items[p-yeast-culture].parts[0].wrong[added] | slip 3000+2^{n} | correct | not equivalent to the key; After one hour that gives 3,002 cells, not 6,000. Doubling multiplies the whole culture: $3000 \tim… |
| problems-1 | items[p-yeast-culture].parts[0].wrong[steady] | slip 6000n | correct | not equivalent to the key; That adds 6,000 cells every hour, which is steady growth. Doubling multiplies by 2 each hour: $3000… |
| problems-1 | items[p-yeast-culture].parts[1].widget.answer | key 750 | correct | recomputed: $2^{-2} = \tfrac{1}{4}$, so $3000 \times \tfrac{1}{4} = 750$ cells. |
| problems-1 | items[p-yeast-culture].parts[1].wrong[negative] | slip -12000 | correct | slip reproduced: A negative power is not a negative number. $2^{-2} = \tfrac{1}{2^2} = \tfrac{1}{4}$, so there were … |
| problems-1 | items[p-yeast-culture].parts[1].wrong[one-hour] | slip 1500 | correct | slip reproduced: 1,500 is the count at 11 am, one hour back. Two hours back halves twice: 750. |
| problems-1 | items[p-yeast-culture].parts[1].wrong[forwards] | slip 12000 | correct | slip reproduced: 12,000 is the count at 2 pm, two hours after noon. Going back in time halves: $3000 \times 2^{-2} =… |
| problems-1 | items[p-yeast-culture].parts[2].widget.answer | key 4242.64 | correct | recomputed: $2^{1/2} = \sqrt{2} \approx 1.4142$, so there are $3000 \times 1.4142 \approx 4243$ cells. |
| problems-1 | items[p-yeast-culture].parts[2].wrong[halfway] | slip 4500 | correct | slip reproduced: 4,500 is halfway between 3,000 and 6,000. Halfway in time is not halfway in size: $2^{1/2} \approx … |
| problems-1 | items[p-yeast-culture].parts[2].wrong[times-half] | slip 3000 | correct | slip reproduced: You read $2^{1/2}$ as $2 \times \tfrac{1}{2} = 1$. It is the square root of 2, about 1.414. |
| problems-1 | items[p-yeast-culture].parts[2].wrong[halved] | slip 1500 | correct | slip reproduced: You read $2^{1/2}$ as $\tfrac{1}{2}$. A power of $\tfrac{1}{2}$ is a square root, so the culture gr… |
| problems-1 | items[p-yeast-culture].parts[2].wrong[base-times] | slip 77.46 | correct | slip reproduced: That is $6000^{1/2}$, from the rule $6000^n$. With $3000 \times 2^n$ only the 2 takes the power: $3… |
| problems-1 | items[p-yeast-culture].parts[3].widget.answer | key 2.5 | correct | recomputed: $\dfrac{3000 \times 2^{1/2}}{3000 \times 2^{-2}} = 2^{1/2 - (-2)} = 2^{2.5}$, so $k = 2.5$. |
| problems-1 | items[p-yeast-culture].parts[3].wrong[added-powers] | slip -1.5 | correct | slip reproduced: You added the powers. Dividing subtracts them: $\tfrac{1}{2} - (-2) = 2.5$. |
| problems-1 | items[p-yeast-culture].parts[3].wrong[divided-powers] | slip -0.25 | correct | slip reproduced: You divided one power by the other. Dividing powers of the same base subtracts them: $\tfrac{1}{2} … |
| problems-1 | items[p-yeast-culture].parts[3].wrong[ratio] | slip 5.657 | correct | slip reproduced: That is the factor itself, $2^{2.5} \approx 5.657$. The question asks for the power $k$. |
| problems-1 | items[p-laptop-value].parts[0].widget.answer | key 0.75 | correct | recomputed: Losing 25% keeps 75% of the value: $1 - 0.25 = 0.75$. |
| problems-1 | items[p-laptop-value].parts[0].wrong[loss] | slip 0.25 | correct | slip reproduced: 0.25 is the part that is lost. The factor is the part kept: $1 - 0.25 = 0.75$. |
| problems-1 | items[p-laptop-value].parts[0].wrong[rise] | slip 1.25 | correct | slip reproduced: 1.25 is the factor for a 25% rise. A fall keeps less than the whole: 0.75. |
| problems-1 | items[p-laptop-value].parts[1].widget.answer | key 675 | correct | recomputed: $1200 \times 0.75^2 = 1200 \times 0.5625 = 675$, so £675. |
| problems-1 | items[p-laptop-value].parts[1].wrong[steady] | slip 600 | correct | slip reproduced: You took £300, a quarter of the price paid, off each year. The second year's loss is a quarter of £… |
| problems-1 | items[p-laptop-value].parts[1].wrong[one-year] | slip 900 | correct | slip reproduced: £900 is the value after 1 year. Multiply by 0.75 again for the second year. |
| problems-1 | items[p-laptop-value].parts[1].wrong[loss-factor] | slip 75 | correct | slip reproduced: That uses the factor 0.25. The value keeps 0.75 each year: $1200 \times 0.75^2 = 675$. |
| problems-1 | items[p-laptop-value].parts[1].wrong[rise-factor] | slip 1875 | correct | slip reproduced: That uses 1.25, a rise. The laptop loses value: $1200 \times 0.75^2 = 675$. |
| problems-1 | items[p-laptop-value].parts[2].widget.answer | key 379.6875 | correct | recomputed: $675 \times 0.5625 = 379.6875$, which is £379.69. |
| problems-1 | items[p-laptop-value].parts[2].wrong[steady] | slip 150 | correct | slip reproduced: You took off the same £525 as in the first 2 years. Each 2 years multiplies by 0.5625, so the losse… |
| problems-1 | items[p-laptop-value].parts[2].wrong[one-year] | slip 506.25 | correct | slip reproduced: £506.25 is the value after 3 years. Two more years from year 2 multiply by $0.75^2$. |
| problems-1 | items[p-laptop-value].parts[2].wrong[halved] | slip 337.5 | correct | slip reproduced: Halving would be a factor of 0.5. The 2-year factor is 0.5625, a little more. |
| problems-1 | items[p-laptop-value].parts[3].widget.answer | key 0.683594 (unit %) | correct | recomputed: $\tfrac{1200 - 379.69}{1200} \approx 0.6836$, a loss of 68.36%. |
| problems-1 | items[p-laptop-value].parts[3].wrong[added] | slip 1.0 | correct | slip reproduced: Four losses of 25% do not add to 100%. Each 25% comes off a smaller value, so the laptop keeps $0.7… |
| problems-1 | items[p-laptop-value].parts[3].wrong[kept] | slip 0.3164 | correct | slip reproduced: 31.64% is the part of the price that is left. The loss is the rest: $100\% - 31.64\% = 68.36\%$. |
| problems-1 | items[p-laptop-value].parts[3].wrong[one-short] | slip 0.5781 | correct | slip reproduced: 57.81% is the loss after 3 years. After 4 years the value is £379.69. |
| problems-1 | items[p-laptop-value].parts[3].wrong[decimal] | slip 0.006836 | correct | slip reproduced: In this box, 0.6836 reads as 0.6836%. Type the percentage, 68.36. |
| problems-1 | items[p-rare-coin].parts[0].widget.answer | key 2.460375 | correct | recomputed: $3936.60 \div 1600 = 2.460375$. |
| problems-1 | items[p-rare-coin].parts[0].wrong[inverted] | slip 0.406442 | correct | slip reproduced: 0.406442 is £1,600 over £3,936.60, the factor back in time. Forward over the three years it is $393… |
| problems-1 | items[p-rare-coin].parts[0].wrong[rise] | slip 1.460375 | correct | slip reproduced: 1.460375 is only the gain on £1,600. Add back the whole £1,600, which is 1, to get 2.460375. |
| problems-1 | items[p-rare-coin].parts[1].widget.answer | key 1.35 | correct | recomputed: $g = 2.460375^{1/3} = \sqrt[3]{2.460375} = 1.35$. |
| problems-1 | items[p-rare-coin].parts[1].wrong[thirded-factor] | slip 0.820125 | correct | slip reproduced: 0.820125 is 2.460375 divided by 3. Three yearly factors multiply, not add, so $g = \sqrt[3]{2.46037… |
| problems-1 | items[p-rare-coin].parts[1].wrong[thirded-rise] | slip 1.486792 | correct | slip reproduced: That shares the 146.0375% gain equally over three years. Each year's gain also acts on the gains be… |
| problems-1 | items[p-rare-coin].parts[1].wrong[square-root] | slip 1.568558 | correct | slip reproduced: 1.568558 is a square root, which fits two years. Three years need the cube root: $\sqrt[3]{2.460375… |
| problems-1 | items[p-rare-coin].parts[2].widget.answer | key 0.35 (unit %) | correct | recomputed: $1.35 - 1 = 0.35$, a rise of 35% a year. |
| problems-1 | items[p-rare-coin].parts[2].wrong[factor] | slip 1.35 | correct | slip reproduced: 135% is the yearly factor itself. The rise is what sits above 1: $1.35 - 1 = 0.35$, or 35%. |
| problems-1 | items[p-rare-coin].parts[2].wrong[thirded-rise] | slip 0.486792 | correct | slip reproduced: 48.68% is a third of the three-year gain. With the yearly factor 1.35 the rise is 35%. |
| problems-1 | items[p-rare-coin].parts[2].wrong[decimal] | slip 0.0035 | correct | slip reproduced: This box reads 0.35 as 0.35%. Enter 35 for 35%. |
| problems-1 | items[p-rare-coin].parts[3].widget.answer | key 2509.69 | correct | recomputed: 18 months ago is 1.5 years after the £1,600 price, so the coin was worth $1600 \times 1.35^{1.5} \a… |
| problems-1 | items[p-rare-coin].parts[3].wrong[mid-value] | slip 2768.3 | correct | slip reproduced: £2,768.30 is the mean of £1,600 and £3,936.60. Equal times give equal factors, not equal sums: $160… |
| problems-1 | items[p-rare-coin].parts[3].wrong[simple] | slip 2440 | correct | slip reproduced: £2,440 adds 1.5 lots of 35% of £1,600. Each year's rise compounds, so use $1600 \times 1.35^{1.5}$. |
| problems-1 | items[p-rare-coin].parts[3].wrong[two-years-ago] | slip 2160 | correct | slip reproduced: £2,160 was the price two years ago. 18 months ago is half a year later: $2160 \times 1.35^{1/2} \ap… |
| problems-1 | items[p-rare-coin].parts[3].wrong[one-year-ago] | slip 2916 | correct | slip reproduced: £2,916 was the price one year ago. 18 months ago is half a year earlier: $2916 \times 1.35^{-1/2} \… |
| problems-1 | items[p-rare-coin].parts[3].wrong[forward] | slip 6174.79 | correct | slip reproduced: £6,174.79 is the price 18 months after today, not before. Counted from the £1,600 price, the date i… |
| problems-1 | items[p-rare-coin].parts[3].wrong[carried] | slip 2900.65 | correct | slip reproduced: That grows £1,600 by a yearly factor of 1.486792. The yearly factor is 1.35: $1600 \times 1.35^{1.5… |
| problems-1 | items[p-curve-point].parts[0].widget.answer | key 4 | correct | recomputed: $a^3 = 64$, so $a = 64^{1/3} = 4$. |
| problems-1 | items[p-curve-point].parts[0].wrong[divided] | slip 21.33 | correct | slip reproduced: You divided 64 by 3. The 3 is a power, so take the cube root: $64^{1/3} = 4$. |
| problems-1 | items[p-curve-point].parts[0].wrong[square-root] | slip 8 | correct | slip reproduced: 8 is the square root of 64. The power is 3, so take the cube root: 4. |
| problems-1 | items[p-curve-point].parts[1].widget.answer | key 0.5 | correct | recomputed: $4^{1/2} = \sqrt{4} = 2$, so a step of 0.5 doubles the height. |
| problems-1 | items[p-curve-point].parts[1].wrong[factor] | slip 2 | correct | slip reproduced: 2 is the factor the height is multiplied by. The question asks for the step $h$ with $4^h = 2$. |
| problems-1 | items[p-curve-point].parts[1].wrong[quarter] | slip 0.25 | correct | slip reproduced: $4^{0.25} = \sqrt{2} \approx 1.414$, so a step of 0.25 does not double. $4^{0.5} = 2$ does. |
| problems-1 | items[p-curve-point].parts[1].wrong[one] | slip 1 | correct | slip reproduced: A step of 1 multiplies by 4, which is two doublings. Half that step doubles: 0.5. |
| problems-1 | items[p-curve-point].parts[2].widget.answer | key 5.5 | correct | recomputed: $2048 \div 64 = 32 = 2^5$: five doublings of 0.5 each, so $x = 3 + 2.5 = 5.5$. |
| problems-1 | items[p-curve-point].parts[2].wrong[step-one] | slip 8 | correct | slip reproduced: You moved 1 for each doubling. Each doubling needs a step of only 0.5, so five doublings move 2.5. |
| problems-1 | items[p-curve-point].parts[2].wrong[counted-ratio] | slip 19 | correct | slip reproduced: You moved once for each of the 32. The ratio 32 is $2^5$, five doublings. |
| problems-1 | items[p-curve-point].parts[2].wrong[distance-only] | slip 2.5 | correct | slip reproduced: 2.5 is the distance moved. Start from $x = 3$: $3 + 2.5 = 5.5$. |
| problems-1 | items[p-curve-point].parts[2].wrong[step-two] | slip 13 | correct | slip reproduced: That moves 2 for each doubling, using the factor as the step. The step is 0.5: $x = 3 + 2.5 = 5.5$. |
| problems-1 | items[p-curve-point].parts[3].widget.answer | key -5.5 | correct | recomputed: $\left(\tfrac{1}{4}\right)^x = 4^{-x}$, so $4^{-x} = 2048$ needs $-x = 5.5$, and $x = -5.5$. |
| problems-1 | items[p-curve-point].parts[3].wrong[no-flip] | slip 5.5 | correct | slip reproduced: At $x = 5.5$ the decay curve is tiny: $4^{-5.5} = \tfrac{1}{2048}$. The mirror point is on the othe… |
| problems-1 | items[p-curve-point].parts[3].wrong[reciprocal] | slip 0.1818 | correct | slip reproduced: You turned 5.5 into $\tfrac{1}{5.5}$. The mirror in the y-axis changes the sign of $x$: $-5.5$. |
| fluency-l3-strange-powers | families[negative-power].widget.answer | work out a negative power: key {key} | correct | every draw in the whole variable range recomputed (concepts script sweep) |
| fluency-l3-strange-powers | families[negative-power].wrong[dropped-minus] | {big}: You dropped the minus: ${a}^{{-{n}}}$ is one over ${an}$, not ${an}$ itself. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l3-strange-powers | families[negative-power].wrong[times-the-power] | {times}: You multiplied {a} by ${-n}$: a power is not a product with the base. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l3-strange-powers | families[fractional-power].widget.answer | work out a fractional power: key {key} | correct | every draw in the whole variable range recomputed (concepts script sweep) |
| fluency-l3-strange-powers | families[fractional-power].wrong[times-the-power] | {times}: You multiplied {a} by the power: a fraction in the power takes a root, not a share of {a}. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l3-strange-powers | families[fractional-power].wrong[flipped] | {flip}: Check the sign of the power: a minus means one over, and no minus means no flip. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l3-strange-powers | families[laws-then-evaluate].widget.answer | use the index laws, then evaluate: key {key} | correct | every draw in the whole variable range recomputed (concepts script sweep) |
| fluency-l3-strange-powers | families[laws-then-evaluate].wrong[added-the-bottom] | {added}: Dividing subtracts powers: take away ${p}$, do not add it. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l3-strange-powers | families[laws-then-evaluate].wrong[multiplied-the-top] | {multiplied}: Multiplying adds powers: ${m} + {n:()} = {t}$, not ${m} \times {n:()}$. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l3-strange-powers | families[power-of-a-power].widget.answer | write a power of a power as one power: key {key} | correct | every draw in the whole variable range recomputed (concepts script sweep) |
| fluency-l3-strange-powers | families[power-of-a-power].wrong[added-the-powers] | {added}: A power of a power multiplies: $\left({v}^{{{m}}}\right)^{{{n}}} = {v}^{{{mn}}}$. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l3-strange-powers | families[power-of-a-power].wrong[sign-of-divide] | {plus}: Dividing subtracts powers: take away ${p}$, do not add it. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| l5-how-many-doublings | screens[2].prose | log_2 1024 = 10 because 2^10 = 1024: the logarithm is the power needed | correct | Gelfand and Shen (logarithm as inverse of the power); A-level pure definition |
| l5-how-many-doublings | screens[3].explain | graph of log_2 x is 2^x mirrored in y = x | correct | inverse functions, A-level pure |
| l5-how-many-doublings | screens[4].explain | numbers between 0 and 1 have negative logs (base 2), log_2 1 = 0, 0 has no log | correct | base 2 > 1 in context |
| l5-how-many-doublings | screens[4].options.none.why | only 0 and negative numbers have no log | correct | real logarithm, domain x > 0 |
| l5-how-many-doublings | screens[7].prose | log_b x = y means b^y = x; b positive and not 1; x positive | correct | A-level pure definition with full domain |
| l5-how-many-doublings | screens[8] | 2^(log_2 x) = x for every positive x | correct | definition |
| l5-how-many-doublings | summary.formula.note | needs b > 0, b not 1, x > 0. Numbers below 1 have negative logs | imprecise | second sentence is true only for b > 1 (and 0 < x < 1): log_(1/2)(1/8) = 3. Finding 6 |
| l5-how-many-doublings | quiz[q-log-one].explain | log_b 1 = 0 for every base | correct | b^0 = 1 |
| l5-how-many-doublings | quiz[q-log4-2].explain | swapping base and number gives the reciprocal log | correct | log_a b x log_b a = 1 |
| l5-how-many-doublings | screens[0].widget.answer | key 10 | correct | recomputed: Ten doublings: $2^{10} = 1024$. |
| l5-how-many-doublings | screens[0].wrong[stop-early] | slip 9 | correct | slip reproduced: Nine doublings reach £512.00. One more doubling is needed. |
| l5-how-many-doublings | screens[0].wrong[count-start] | slip 11 | correct | slip reproduced: You counted the starting row as a round. Round 0 is the £1.00 you began with. |
| l5-how-many-doublings | screens[0].wrong[halved] | slip 512 | correct | slip reproduced: You halved £1,024.00. We want how many times we double, not what we double from. |
| l5-how-many-doublings | screens[1].options[ans] (key) | 6 and 7 | correct | derivation: £64.00 after 6 and £128.00 after 7, so the crossing lies between. |
| l5-how-many-doublings | screens[1].options[half] | 50 and 51 | correct | wrong option, wrong under every convention: You halved £100.00. Fifty doublings would make far more than £100.00; drag P to 7 and it already re… |
| l5-how-many-doublings | screens[1].options[zeros] | 2 and 3 | correct | wrong option, wrong under every convention: You counted the zeros in 100. That counts steps of ×10, not ×2. Drag P to 3: it reads £8.00. |
| l5-how-many-doublings | screens[1].options[late] | 7 and 8 | correct | wrong option, wrong under every convention: After 7 doublings the stake is £128.00, already past £100.00. Drag P to 6: it reads £64.00. |
| l5-how-many-doublings | screens[2].widget.answer | key 5 | correct | recomputed: $\log_2 32 = 5$, because $2^5 = 32$. |
| l5-how-many-doublings | screens[2].wrong[divided] | slip 16 | correct | slip reproduced: You divided 32 by 2. The log counts how many 2s multiply to make 32. |
| l5-how-many-doublings | screens[2].wrong[count-terms] | slip 6 | correct | slip reproduced: You counted 1, 2, 4, 8, 16 and 32 as six. The 1 is the start, not a doubling. |
| l5-how-many-doublings | screens[3].widget.points | target [8, 3] | correct | recomputed: $(8, 3)$ says: reaching 8 takes 3 doublings. |
| l5-how-many-doublings | screens[3].wrong[same] | region {"x": [2.6, 3.4], "y": [7.6, 8.4]} | correct | region is clear of the target band; You left Q on the original point. The swap puts 8 across and 3 up. |
| l5-how-many-doublings | screens[3].wrong[flip-y] | region {"x": [7.6, 8.4], "y": [7.6, 8.4]} | correct | region is clear of the target band; You kept 8 as the height. After the swap the height is the count, 3. |
| l5-how-many-doublings | screens[4].options[ans] (key) | $-3$ | correct | derivation: $2^{-3} = \tfrac{1}{8}$, so $\log_2 \tfrac{1}{8} = -3$. |
| l5-how-many-doublings | screens[4].options[pos] | $3$ | correct | wrong option, wrong under every convention: You found $\log_2 8$. Reaching $\tfrac{1}{8}$ takes three halvings, which are three steps left of 0. |
| l5-how-many-doublings | screens[4].options[recip] | $\tfrac{1}{3}$ | correct | wrong option, wrong under every convention: You turned the answer for 8 upside down. $2^{1/3}$ is about 1.26, not $\tfrac{1}{8}$. |
| l5-how-many-doublings | screens[4].options[none] | It does not exist | correct | wrong option, wrong under every convention: Only 0 and negative numbers have no log. $2^{-3} = \tfrac{1}{8}$, so this one exists. |
| l5-how-many-doublings | screens[5].options[ans] (key) | 12 and 13 | correct | derivation: $2^{12} < 5000 < 2^{13}$, so the log is between 12 and 13. |
| l5-how-many-doublings | screens[5].options[digits] | 3 and 4 | correct | wrong option, wrong under every convention: You counted the digits of 5,000. Digits count steps of ×10, not doublings. |
| l5-how-many-doublings | screens[5].options[low] | 11 and 12 | correct | wrong option, wrong under every convention: $2^{12} = 4096$ is still below 5,000, so the log is above 12. |
| l5-how-many-doublings | screens[5].options[half] | 2,500 and 2,501 | correct | wrong option, wrong under every convention: You halved 5,000. A log counts doublings; it does not divide. |
| l5-how-many-doublings | screens[6].options[ans] (key) | 6 | correct | derivation: $2^6 = 64$, so $\log_2 64 = 6$. |
| l5-how-many-doublings | screens[6].options[div] | 32 | correct | wrong option, wrong under every convention: You divided 64 by 2. The log asks how many 2s multiply to make 64, and $2^{32}$ is over four billio… |
| l5-how-many-doublings | screens[6].options[root] | 8 | correct | wrong option, wrong under every convention: You found the number whose square is 64. That is $\sqrt{64}$; the log asks for the power on 2. |
| l5-how-many-doublings | screens[6].options[double] | 128 | correct | wrong option, wrong under every convention: You doubled 64. The log counts the doublings up to 64; it does not add one more. |
| l5-how-many-doublings | screens[7].options[ans] (key) | $5^3 = 125$ | correct | derivation: The base carries the power, and the log is that power. |
| l5-how-many-doublings | screens[7].options[swap] | $3^5 = 125$ | correct | wrong option, wrong under every convention: You swapped the base and the power. $3^5 = 243$. |
| l5-how-many-doublings | screens[7].options[wrong-base] | $125^3 = 5$ | correct | wrong option, wrong under every convention: You raised the wrong number. The base 5 carries the power. |
| l5-how-many-doublings | screens[7].options[div] | $125 \div 5 = 3$ | correct | wrong option, wrong under every convention: You divided. $125 \div 5 = 25$, and the log counts factors of 5. |
| l5-how-many-doublings | screens[8].widget.answer | order name > mean > sub > check | correct | each line follows from the one before; Name, rewrite, substitute, check. |
| l5-how-many-doublings | screens[9].widget.answer | key 7 | correct | recomputed: Seven halvings: £1,000.00 ÷ 128 = £7.81. |
| l5-how-many-doublings | screens[9].wrong[equal] | slip 6 | correct | slip reproduced: After 6 halvings the position is worth £15.63, still above £10.00. |
| l5-how-many-doublings | screens[9].wrong[ratio] | slip 100 | correct | slip reproduced: You divided £1,000.00 by £10.00 and stopped. 100 is the factor to undo; count the halvings that mak… |
| l5-how-many-doublings | screens[9].wrong[half] | slip 50 | correct | slip reproduced: You halved 100. The log counts halvings; it does not divide by 2. |
| l5-how-many-doublings | quiz[q-log3-81].widget.answer | key 4 | correct | recomputed: $3^4 = 81$. |
| l5-how-many-doublings | quiz[q-log3-81].wrong[divided] | slip 27 | correct | slip reproduced: You divided 81 by 3. The log counts how many 3s multiply to make 81. |
| l5-how-many-doublings | quiz[q-log3-81].wrong[root] | slip 9 | correct | slip reproduced: You found $\sqrt{81}$. The log is the power on 3. |
| l5-how-many-doublings | quiz[q-log-one].options[ans] (key) | 0 | correct | derivation: $7^0 = 1$, so $\log_7 1 = 0$. |
| l5-how-many-doublings | quiz[q-log-one].options[one] | 1 | correct | wrong option, wrong under every convention: You took the log of 1 to be 1. But $7^1 = 7$; making 1 takes no factors of 7. |
| l5-how-many-doublings | quiz[q-log-one].options[seven] | 7 | correct | wrong option, wrong under every convention: You gave the base. $\log_7 7 = 1$, and $\log_7 1$ asks for the power that makes 1. |
| l5-how-many-doublings | quiz[q-log-one].options[none] | It does not exist | correct | wrong option, wrong under every convention: $7^0 = 1$, so the power exists: it is 0. |
| l5-how-many-doublings | quiz[q-between].options[ans] (key) | 5 and 6 | correct | derivation: $2^5 = 32 < 50 < 64 = 2^6$. |
| l5-how-many-doublings | quiz[q-between].options[digits] | 1 and 2 | correct | wrong option, wrong under every convention: You counted the digits of 50. That is the base-10 count, not doublings. |
| l5-how-many-doublings | quiz[q-between].options[half] | 25 and 26 | correct | wrong option, wrong under every convention: You halved 50. A log counts doublings. |
| l5-how-many-doublings | quiz[q-between].options[high] | 6 and 7 | correct | wrong option, wrong under every convention: $2^6 = 64$ is already past 50, so the log is below 6. |
| l5-how-many-doublings | quiz[q-log4-2].options[ans] (key) | $\tfrac{1}{2}$ | correct | derivation: $4^{1/2} = \sqrt{4} = 2$. |
| l5-how-many-doublings | quiz[q-log4-2].options[swap] | $2$ | correct | wrong option, wrong under every convention: You found $\log_2 4$. Here the base is 4, and 2 is smaller than 4. |
| l5-how-many-doublings | quiz[q-log4-2].options[neg] | $-2$ | correct | wrong option, wrong under every convention: A negative power makes a number below 1. 2 is above 1, so the power is positive. |
| l5-how-many-doublings | quiz[q-log4-2].options[half] | $\tfrac{1}{4}$ | correct | wrong option, wrong under every convention: $4^{1/4} = \sqrt{2} \approx 1.41$, not 2. |
| l6-products-into-sums | screens[1].explain | distance on the ruler is log_2; adding distances multiplies numbers (slide rule) | correct | product law |
| l6-products-into-sums | screens[7].prose | log_b(xy) = log_b x + log_b y; log_b(x/y) = log_b x - log_b y; log_b(x^k) = k log_b x, positive x and y | correct | A-level pure laws of logarithms |
| l6-products-into-sums | screens[6].explain | there is no law for the log of a sum | correct | counterexample log_2(4+4) = 3, not 4 |
| l6-products-into-sums | screens[8] | proof of the product law from b^m b^n = b^(m+n) | correct | standard proof |
| l6-products-into-sums | summary.trap | log(a + b) is not log a + log b | correct | as above |
| l6-products-into-sums | screens[0].widget.answer | tap ['r12c1'] | correct | recomputed: $32 \times 128 = 4096$: row 5 plus row 7 is row 12. |
| l6-products-into-sums | screens[0].feedback.byKey.r12c0 | wrong tap r12c0 | correct | slip reproduced: You tapped the power, 12. The product is the amount in that row. |
| l6-products-into-sums | screens[0].feedback.byKey.r11c1 | wrong tap r11c1 | correct | slip reproduced: That is 2,048, one row short. 32 is $2^5$ and 128 is $2^7$: add 5 and 7. |
| l6-products-into-sums | screens[0].feedback.byKey.r10c1 | wrong tap r10c1 | correct | slip reproduced: 1,024 is $2^{10}$. Check the powers: 32 is $2^5$ and 128 is $2^7$. |
| l6-products-into-sums | screens[0].feedback.byKey.r8c1 | wrong tap r8c1 | correct | slip reproduced: 256 is $128 \times 2$, one doubling of 128. Multiplying by 32 is five doublings: row 7 plus 5. |
| l6-products-into-sums | screens[0].feedback.byKey.r2c1 | wrong tap r2c1 | correct | slip reproduced: 4 is $2^{7 - 5}$. Multiplying adds the powers, $5 + 7$; it does not take one from the other. |
| l6-products-into-sums | screens[1].options[ans] (key) | Multiplies it by 8 | correct | derivation: Three doublings: $\times 8$ wherever you start. |
| l6-products-into-sums | screens[1].options[add8] | Adds 8 | correct | wrong option, wrong under every convention: Slide A to 4: A reads 16 and B reads 128. That is 112 more, but 8 times as much. |
| l6-products-into-sums | screens[1].options[add3] | Adds 3 | correct | wrong option, wrong under every convention: The steps add 3 to the power, not to the number. From 4 to 32 is far more than 3. |
| l6-products-into-sums | screens[1].options[times3] | Multiplies it by 3 | correct | wrong option, wrong under every convention: Each step doubles, so 3 steps double three times: $2 \times 2 \times 2 = 8$. |
| l6-products-into-sums | screens[2].widget.answer | key 8 | correct | recomputed: Five 2s, then three more: eight. |
| l6-products-into-sums | screens[2].wrong[mult] | slip 15 | correct | slip reproduced: You multiplied 5 by 3. Putting the strings side by side adds them: five 2s, then three more. |
| l6-products-into-sums | screens[2].wrong[added-numbers] | slip 40 | correct | slip reproduced: You added 32 and 8. Count factors of 2 instead. |
| l6-products-into-sums | screens[2].wrong[sub] | slip 2 | correct | slip reproduced: You subtracted the counts. Multiplying joins the two strings, so the counts add. |
| l6-products-into-sums | screens[2].wrong[product] | slip 256 | correct | slip reproduced: That is the product, $2^8 = 256$. We asked for the number of 2s in it. |
| l6-products-into-sums | screens[3].widget.answer | key 5 | correct | recomputed: $8 - 3 = 5$ factors of 2 survive. |
| l6-products-into-sums | screens[3].wrong[number] | slip 32 | correct | slip reproduced: You found $\tfrac{256}{8} = 32$ itself. The log is its count of 2s. |
| l6-products-into-sums | screens[3].wrong[added] | slip 11 | correct | slip reproduced: You added the logs. Dividing cancels factors, so subtract: $8 - 3$. |
| l6-products-into-sums | screens[3].wrong[divided-logs] | slip 2.667 | correct | slip reproduced: You divided the logs, $8 \div 3$. Dividing the numbers subtracts their logs; it does not divide the… |
| l6-products-into-sums | screens[4].widget.answer | key 12 | correct | recomputed: Four groups of three 2s: twelve. |
| l6-products-into-sums | screens[4].wrong[added] | slip 7 | correct | slip reproduced: You added 3 and 4. There are four groups of three 2s, so multiply: $4 \times 3$. |
| l6-products-into-sums | screens[4].wrong[power-of-log] | slip 81 | correct | slip reproduced: You worked out $3^4$. The power 4 counts copies of 8, so it multiplies the log. |
| l6-products-into-sums | screens[4].wrong[number] | slip 4096 | correct | slip reproduced: That is $8^4$ itself. Its log counts the 2s inside it. |
| l6-products-into-sums | screens[5].widget.answer | key 3.585 | correct | recomputed: $\log_2 12 = 2 + 1.585 = 3.585$. |
| l6-products-into-sums | screens[5].wrong[mult-logs] | slip 3.17 | correct | slip reproduced: You multiplied $\log_2 4$ by $\log_2 3$. A product inside the log becomes a sum: $2 + 1.585$. |
| l6-products-into-sums | screens[5].wrong[power] | slip 6.34 | correct | slip reproduced: You worked out $4 \times 1.585$, which is $\log_2 3^4 = \log_2 81$. But 12 is $4 \times 3$, not $3^… |
| l6-products-into-sums | screens[6].options[ans] (key) | 3 | correct | derivation: $4 + 4 = 8$, and $\log_2 8 = 3$. |
| l6-products-into-sums | screens[6].options[split] | 4 | correct | wrong option, wrong under every convention: You split the log over a sum. $\log_2 4 + \log_2 4$ is $\log_2(4 \times 4) = \log_2 16$, which is 4. |
| l6-products-into-sums | screens[6].options[number] | 8 | correct | wrong option, wrong under every convention: That is $4 + 4$ itself. Its log counts the 2s in 8. |
| l6-products-into-sums | screens[6].options[one] | 2 | correct | wrong option, wrong under every convention: You took the log of one 4 and dropped the other. |
| l6-products-into-sums | screens[7].options[ans] (key) | $3\log_b x - \log_b y$ | correct | derivation: Quotient law, then power law. |
| l6-products-into-sums | screens[7].options[divide] | $\dfrac{3\log_b x}{\log_b y}$ | correct | wrong option, wrong under every convention: You divided the logs. Dividing the numbers subtracts their logs. |
| l6-products-into-sums | screens[7].options[inside] | $\log_b 3x - \log_b y$ | correct | wrong option, wrong under every convention: The power 3 multiplies the log of $x$; it does not go inside as $3x$. |
| l6-products-into-sums | screens[7].options[both] | $3(\log_b x - \log_b y)$ | correct | wrong option, wrong under every convention: The 3 belongs to $x$ only. $y$ is not cubed. |
| l6-products-into-sums | screens[8].widget.answer | order name > mean > index > back > sub | correct | each line follows from the one before; Each line uses only the one before it and a law you know. |
| l6-products-into-sums | screens[9].widget.answer | key 2p+3q | correct | derivation: $\log_b(x^2 y^3) = 2p + 3q$. |
| l6-products-into-sums | screens[9].wrong[mult] | slip 6pq | correct | not equivalent to the key; You multiplied everything together. A product inside the log becomes a sum outside. |
| l6-products-into-sums | screens[9].wrong[inside] | slip p^2+q^3 | correct | not equivalent to the key; You kept the powers as powers. The power law turns $\log_b x^2$ into $2p$, not $p^2$. |
| l6-products-into-sums | screens[10].widget.answer | key 0.585 | correct | recomputed: $0.5850 - 0.3219 + 0.3219 = 0.5850$. |
| l6-products-into-sums | screens[10].wrong[sign] | slip 1.2288 | correct | slip reproduced: You added the fall as if it were a gain. A factor below 1 has a negative log. |
| l6-products-into-sums | screens[10].wrong[mult-logs] | slip -0.0606 | correct | slip reproduced: You multiplied the logs. Multiplying factors adds their logs. |
| l6-products-into-sums | screens[10].wrong[add-factors] | slip 3.55 | correct | slip reproduced: You added the growth factors. Factors multiply, and it is their logs that add. |
| l6-products-into-sums | quiz[q-log2-40].widget.answer | key 5.322 | correct | recomputed: $40 = 8 \times 5$, so $3 + 2.322$. |
| l6-products-into-sums | quiz[q-log2-40].wrong[mult] | slip 6.966 | correct | slip reproduced: You multiplied $\log_2 8$ by $\log_2 5$. A product inside the log becomes a sum. |
| l6-products-into-sums | quiz[q-quotient].options[ans] (key) | 3 | correct | derivation: $5 - 2 = 3$. |
| l6-products-into-sums | quiz[q-quotient].options[div] | 2.5 | correct | wrong option, wrong under every convention: You divided the logs, $5 \div 2$. Dividing the numbers subtracts their logs. |
| l6-products-into-sums | quiz[q-quotient].options[number] | 27 | correct | wrong option, wrong under every convention: That is the quotient itself. Its log is 3. |
| l6-products-into-sums | quiz[q-quotient].options[add] | 7 | correct | wrong option, wrong under every convention: You added the logs. Dividing subtracts them. |
| l6-products-into-sums | quiz[q-tidy].options[ans] (key) | $\log_b x$ | correct | derivation: $2\log_b x - \log_b x = \log_b x$. |
| l6-products-into-sums | quiz[q-tidy].options[sum-inside] | $\log_b \left(x^2 + \tfrac{1}{x}\right)$ | correct | wrong option, wrong under every convention: That puts the sum inside the log. Adding logs multiplies the numbers: $x^2 \cdot \tfrac{1}{x} = x$. |
| l6-products-into-sums | quiz[q-tidy].options[prod] | $3\log_b x$ | correct | wrong option, wrong under every convention: You added the powers 2 and 1. But $\tfrac{1}{x} = x^{-1}$, so the multipliers are 2 and −1. |
| l6-products-into-sums | quiz[q-tidy].options[zero] | $0$ | correct | wrong option, wrong under every convention: The two terms do not cancel: one is $2\log_b x$ and the other is $-\log_b x$. |
| l6-products-into-sums | quiz[q-true-law].options[ans] (key) | $\log_b(xy) = \log_b x + \log_b y$ | correct | derivation: That is the product law. |
| l6-products-into-sums | quiz[q-true-law].options[sum] | $\log_b(x + y) = \log_b x + \log_b y$ | correct | wrong option, wrong under every convention: Adding logs multiplies the numbers, so the right side is $\log_b(xy)$, not the log of a sum. |
| l6-products-into-sums | quiz[q-true-law].options[quot] | $\log_b \tfrac{x}{y} = \dfrac{\log_b x}{\log_b y}$ | correct | wrong option, wrong under every convention: Dividing the numbers subtracts the logs; it does not divide them. |
| l6-products-into-sums | quiz[q-true-law].options[power] | $\log_b(x^k) = (\log_b x)^k$ | correct | wrong option, wrong under every convention: The power comes out in front as a multiplier, not as a power of the log. |
| l7-changing-base | screens[2].prose | log with no base means log_10 (convention of the course); log 2 = 0.301 | correct | A-level convention; stated where it first matters and repeated in the summary; l10 adds that Python math.log is ln |
| l7-changing-base | screens[4].explain | numbers below 1 have negative logs (base 10 ruler), 0 never appears | correct | base 10 > 1 in context |
| l7-changing-base | screens[7].prose | log_b x = log x / log b; any base on top and bottom if the same | correct | change of base; proof on screens[8] |
| l7-changing-base | screens[8].explain | the rule fails only for base 1, since log 1 = 0 | correct | derivation |
| l7-changing-base | screens[9].explain | on a log chart equal moves are equal percentages | correct | log(kx) - log x = log k |
| l7-changing-base | summary.trap | a quotient of logs is not the log of a quotient | correct | log 8 / log 2 = 3, log 4 = 0.602 |
| l7-changing-base | screens[0].widget.answer | key 3 | correct | recomputed: ×1,000 is three tenfold steps. |
| l7-changing-base | screens[0].wrong[ratio] | slip 1000 | correct | slip reproduced: You found the ratio, ×1,000. Count how many 10s multiply to make it. |
| l7-changing-base | screens[0].wrong[diff] | slip 99900 | correct | slip reproduced: You subtracted. This ruler measures ratios, not differences. |
| l7-changing-base | screens[0].wrong[from-one] | slip 5 | correct | slip reproduced: You counted from 1. The index started at 100, two steps along already. |
| l7-changing-base | screens[1].options[ans] (key) | About 0.30 | correct | derivation: At 0.30 the ruler reads 2.00. |
| l7-changing-base | screens[1].options[linear] | About 0.11 | correct | wrong option, wrong under every convention: You placed 2 a ninth of the way from 1 to 10, as on an ordinary ruler. Slide P to 0.11: it reads 1.… |
| l7-changing-base | screens[1].options[fifth] | About 0.20 | correct | wrong option, wrong under every convention: 2 is a fifth of 10, but slide P to 0.20: it reads 1.58. |
| l7-changing-base | screens[1].options[half] | About 0.50 | correct | wrong option, wrong under every convention: Halfway reads 3.16, the number that times itself makes 10. 2 comes sooner. |
| l7-changing-base | screens[2].widget.answer | key 1.301 | correct | recomputed: $\log 20 = 0.301 + 1 = 1.301$. |
| l7-changing-base | screens[2].wrong[times10] | slip 3.01 | correct | slip reproduced: You multiplied $\log 2$ by 10. Multiplying the number by 10 adds one step: $0.301 + 1$. |
| l7-changing-base | screens[2].wrong[digits] | slip 2 | correct | slip reproduced: You counted the digits of 20. Digits give the whole steps; 20 sits part-way between 10 and 100. |
| l7-changing-base | screens[2].wrong[double] | slip 0.602 | correct | slip reproduced: That is $\log 4$, twice $\log 2$. But 20 is $2 \times 10$, not $2 \times 2$. |
| l7-changing-base | screens[3].widget.answer | tap ['c6'] | correct | recomputed: 2 to 6 is ×3, the same gap as 1 to 3. |
| l7-changing-base | screens[3].feedback.byKey.c4 | wrong tap c4 | correct | slip reproduced: 4 is 2 more than 2, as 3 is 2 more than 1. This ruler measures ratios: 3 is 1 times 3, so look for … |
| l7-changing-base | screens[3].feedback.byKey.c5 | wrong tap c5 | correct | slip reproduced: 5 is 2.5 times 2. The gap from 1 to 3 is a ratio of 3. |
| l7-changing-base | screens[3].feedback.byKey.c8 | wrong tap c8 | correct | slip reproduced: 8 is 4 times 2, a longer gap than 1 to 3. |
| l7-changing-base | screens[4].widget.points | target -0.301 | correct | recomputed: $\log 0.5 = -0.301$. |
| l7-changing-base | screens[4].wrong[same-side] | region {"x": [0.25, 0.35]} | correct | region is clear of the target band; You put 0.5 where 2 is. Halving moves left of 1, so 0.5 sits 0.301 to the left. |
| l7-changing-base | screens[4].wrong[halfway] | region {"x": [-0.55, -0.45]} | correct | region is clear of the target band; You put 0.5 halfway to 0.1, as on an ordinary ruler. On this ruler halfway reads 0.32. |
| l7-changing-base | screens[5].widget.answer | key 19.93 | correct | recomputed: $6 \div 0.301 \approx 19.9$ doublings. |
| l7-changing-base | screens[5].wrong[mult] | slip 1.806 | correct | slip reproduced: You multiplied 6 by 0.301. Each doubling is a short hop, so it takes more of them than steps: divid… |
| l7-changing-base | screens[5].wrong[tens] | slip 6 | correct | slip reproduced: That is the count of tenfold steps, $\log 1{,}000{,}000$. Each tenfold step holds about 3.3 doublin… |
| l7-changing-base | screens[5].wrong[half] | slip 500000 | correct | slip reproduced: You halved a million. A log counts doublings; it does not divide. |
| l7-changing-base | screens[6].options[ans] (key) | 3 | correct | derivation: $0.903 \div 0.301 = 3$, and $2^3 = 8$. |
| l7-changing-base | screens[6].options[quot] | 0.602 | correct | wrong option, wrong under every convention: You took the log of $8 \div 2$. Dividing two logs is not the log of a quotient; $\log 8 - \log 2$ i… |
| l7-changing-base | screens[6].options[top] | 0.903 | correct | wrong option, wrong under every convention: That is $\log 8$ on its own. Divide it by $\log 2 = 0.301$. |
| l7-changing-base | screens[6].options[numbers] | 4 | correct | wrong option, wrong under every convention: You divided 8 by 2 and stopped. The rule divides the logs. |
| l7-changing-base | screens[7].options[ans] (key) | $\dfrac{\log 200}{\log 5}$ | correct | derivation: $\log_5 200 = \dfrac{\log 200}{\log 5} \approx 3.29$. |
| l7-changing-base | screens[7].options[flip] | $\dfrac{\log 5}{\log 200}$ | correct | wrong option, wrong under every convention: You put the base on top. Divide by the size of one unit, $\log 5$. |
| l7-changing-base | screens[7].options[quot] | $\log \dfrac{200}{5}$ | correct | wrong option, wrong under every convention: That is $\log 40$. The rule divides two logs, not the numbers. |
| l7-changing-base | screens[7].options[mult] | $\log 200 \times \log 5$ | correct | wrong option, wrong under every convention: Converting to a new unit means dividing by its size, not multiplying. |
| l7-changing-base | screens[8].widget.answer | order name > mean > take > power > divide | correct | each line follows from the one before; Each line follows from the one before. |
| l7-changing-base | screens[9].widget.answer | key 15 | correct | recomputed: £12.00 × 1.25 = £15.00: both moves are +25%. |
| l7-changing-base | screens[9].wrong[added] | slip 17 | correct | slip reproduced: You added £5.00. Equal heights on a log chart are equal ratios: ×1.25. |
| l7-changing-base | screens[9].wrong[diff-log] | slip 12.1 | correct | slip reproduced: You added the height, 0.097, to the price. Add it to $\log 12$ instead, then undo the log. |
| l7-changing-base | quiz[q-log-hundredth].widget.answer | key -2 | correct | recomputed: $10^{-2} = 0.01$. |
| l7-changing-base | quiz[q-log-hundredth].wrong[sign] | slip 2 | correct | slip reproduced: You dropped the sign. 0.01 is below 1, so its log is negative. |
| l7-changing-base | quiz[q-log-hundredth].wrong[value] | slip 0.01 | correct | slip reproduced: That is the number itself. Its log is the power on 10. |
| l7-changing-base | quiz[q-log2-3].widget.answer | key 1.585 | correct | recomputed: $0.477 \div 0.301 \approx 1.58$. |
| l7-changing-base | quiz[q-log2-3].wrong[flip] | slip 0.631 | correct | slip reproduced: You divided $\log 2$ by $\log 3$. The base's log goes on the bottom. |
| l7-changing-base | quiz[q-log2-3].wrong[quot] | slip 0.176 | correct | slip reproduced: That is $\log 1.5 = \log \tfrac{3}{2}$. The rule divides the logs. |
| l7-changing-base | quiz[q-log-chart].options[ans] (key) | £8.00 to £12.00 | correct | derivation: £8.00 to £12.00 is ×1.5, like £50.00 to £75.00. |
| l7-changing-base | quiz[q-log-chart].options[pounds] | £100.00 to £125.00 | correct | wrong option, wrong under every convention: That is the same £25.00 rise, but only +25%. Equal heights need equal ratios: ×1.5. |
| l7-changing-base | quiz[q-log-chart].options[pounds2] | £30.00 to £55.00 | correct | wrong option, wrong under every convention: You copied the £25.00 rise. From £30.00 that is +83%, far more than +50%. |
| l7-changing-base | quiz[q-log-chart].options[next] | £75.00 to £100.00 | correct | wrong option, wrong under every convention: That is ×1.33, a smaller ratio than ×1.5. |
| l7-changing-base | quiz[q-log9-27].options[ans] (key) | $1.5$ | correct | derivation: $9^{1.5} = 27$. |
| l7-changing-base | quiz[q-log9-27].options[quot] | $3$ | correct | wrong option, wrong under every convention: You worked out $27 \div 9$. The rule divides the logs: $\tfrac{\log 27}{\log 9}$. |
| l7-changing-base | quiz[q-log9-27].options[flip] | $0.667$ | correct | wrong option, wrong under every convention: You put the base on top. Divide by $\log 9$, the unit. |
| l7-changing-base | quiz[q-log9-27].options[log-quot] | $0.477$ | correct | wrong option, wrong under every convention: That is $\log 3 = \log \tfrac{27}{9}$, the log of a quotient. |
| l8-solving-for-the-power | screens[5].explain | 2^x = -4 has no solution; log(-4) does not exist | correct | real exponential is positive; real log domain x > 0 |
| l8-solving-for-the-power | screens[7].prose | a^x = b gives x = log b / log a; needs a > 0, a not 1, b > 0 | correct | A-level pure; domain stated |
| l8-solving-for-the-power | screens[4].explain | taking logs straight away also works, since log 300 - log 200 = log 1.5 | correct | product law (compare Finding 2: three slip lines say the opposite) |
| l8-solving-for-the-power | screens[8] | doubling time n = log 2 / log(1 + r), independent of P; log(1 + r) > 0 since r > 0 | correct | derivation; hypothesis r > 0 stated |
| l8-solving-for-the-power | screens[0].widget.answer | key 5 | correct | recomputed: Year 4 gives £732.05 and year 5 gives £805.26. |
| l8-solving-for-the-power | screens[0].wrong[simple] | slip 6 | correct | slip reproduced: Six years of £50.00 reach exactly £800.00, which is simple interest. Compounding adds 10% of the ne… |
| l8-solving-for-the-power | screens[0].wrong[short] | slip 4 | correct | slip reproduced: After 4 years the balance is £732.05, still short of £800.00. |
| l8-solving-for-the-power | screens[0].wrong[seven] | slip 7 | correct | slip reproduced: You added £50.00 a year, which is simple interest: it passes £800.00 in year 7. The interest grows … |
| l8-solving-for-the-power | screens[1].options[ans] (key) | About 4.9 years | correct | derivation: At 4.9 years the balance is about £798; at 5.0 it is £805.26. |
| l8-solving-for-the-power | screens[1].options[simple] | About 6 years | correct | wrong option, wrong under every convention: That is simple interest, £50.00 a year. Compound growth adds more each year, so it arrives sooner. |
| l8-solving-for-the-power | screens[1].options[ratio] | About 1.6 years | correct | wrong option, wrong under every convention: You divided £800.00 by £500.00. That 1.6 is the growth needed, not the time. |
| l8-solving-for-the-power | screens[1].options[early] | About 3 years | correct | wrong option, wrong under every convention: Slide to 3: the balance is £665.50, still well short. |
| l8-solving-for-the-power | screens[2].widget.answer | key 4.93 | correct | recomputed: $n = \dfrac{0.2041}{0.0414} \approx 4.93$ years. |
| l8-solving-for-the-power | screens[2].wrong[flip] | slip 0.203 | correct | slip reproduced: You divided $\log 1.1$ by $\log 1.6$. The unknown's partner, $\log 1.1$, goes on the bottom. |
| l8-solving-for-the-power | screens[2].wrong[mult] | slip 0.0084 | correct | slip reproduced: You multiplied the logs. $n$ is multiplied by $\log 1.1$, so divide to free it. |
| l8-solving-for-the-power | screens[2].wrong[sub] | slip 0.1627 | correct | slip reproduced: You subtracted the logs. That is $\log \tfrac{1.6}{1.1}$, a different number. |
| l8-solving-for-the-power | screens[3].widget.answer | key 3.561 | correct | recomputed: $x = \dfrac{\log 50}{\log 3} \approx 3.56$. |
| l8-solving-for-the-power | screens[3].wrong[div] | slip 16.67 | correct | slip reproduced: You divided 50 by 3. The 3 is raised to the power $x$; it does not multiply it. |
| l8-solving-for-the-power | screens[3].wrong[flip] | slip 0.281 | correct | slip reproduced: You put $\log 50$ on the bottom. Divide by $\log 3$, the number multiplying $x$. |
| l8-solving-for-the-power | screens[3].wrong[log-quot] | slip 1.222 | correct | slip reproduced: That is $\log \tfrac{50}{3}$. Divide the two logs rather than the two numbers. |
| l8-solving-for-the-power | screens[4].widget.states | target state n = \dfrac{\log 1.5}{\log 1.05} \approx 8.31 | correct | every state checked as an equation equivalent to the start (dead ends marked with a why); $n = \dfrac{\log 1.5}{\log 1.05} \approx 8.31$ years. |
| l8-solving-for-the-power | screens[5].options[ans] (key) | There is no solution | correct | derivation: Every power of 2 is positive, so $2^x = -4$ has no solution. |
| l8-solving-for-the-power | screens[5].options[neg] | $x = -2$ | correct | wrong option, wrong under every convention: $2^{-2} = \tfrac{1}{4}$, which is still positive. |
| l8-solving-for-the-power | screens[5].options[pos] | $x = 2$ | correct | wrong option, wrong under every convention: $2^2 = 4$, not $-4$. |
| l8-solving-for-the-power | screens[5].options[formula] | $x = \dfrac{\log(-4)}{\log 2}$ | correct | wrong option, wrong under every convention: $\log(-4)$ does not exist: no power of 10 is negative. |
| l8-solving-for-the-power | screens[6].options[ans] (key) | 4.93 | correct | derivation: $1.1^n = 1.6$ gives $n \approx 4.93$, as the slider showed. |
| l8-solving-for-the-power | screens[6].options[merge] | 1.06 | correct | wrong option, wrong under every convention: You merged 500 and 1.1 into 550. The power belongs to 1.1 alone, so divide by 500 first. |
| l8-solving-for-the-power | screens[6].options[drop] | 70.14 | correct | wrong option, wrong under every convention: You solved $1.1^n = 800$ and left out the 500. Divide by 500 first: $1.1^n = 1.6$. |
| l8-solving-for-the-power | screens[6].options[simple] | 6.00 | correct | wrong option, wrong under every convention: That is simple interest, £50.00 a year. The balance compounds. |
| l8-solving-for-the-power | screens[7].options[ans] (key) | Divide both sides by 3 | correct | derivation: Then $2^x = 16$, so $x = 4$. |
| l8-solving-for-the-power | screens[7].options[merge] | Take logs: $x \log 6 = \log 48$ | correct | wrong option, wrong under every convention: That treats $3 \times 2$ as the base. Only 2 carries the power. |
| l8-solving-for-the-power | screens[7].options[div2] | Divide both sides by 2 | correct | wrong option, wrong under every convention: The 2 carries the power, so dividing by it does not free $x$. |
| l8-solving-for-the-power | screens[7].options[root] | Take the cube root of both sides | correct | wrong option, wrong under every convention: The 3 multiplies; it is not a power. Divide by it. |
| l8-solving-for-the-power | screens[8].widget.answer | order set > cancel > logs > power > solve | correct | each line follows from the one before; The starting amount cancels, so the doubling time depends only on $r$. |
| l8-solving-for-the-power | screens[9].widget.answer | key 10.24 | correct | recomputed: $n = \dfrac{\log 2}{\log 1.07} \approx 10.24$ years. |
| l8-solving-for-the-power | screens[9].wrong[simple] | slip 14.29 | correct | slip reproduced: That is simple interest: £70.00 a year takes 14.29 years to add £1,000.00. Compounding is faster. |
| l8-solving-for-the-power | screens[9].wrong[div-rate] | slip 28.57 | correct | slip reproduced: You divided 2 by 0.07. The 1.07 is raised to a power, so take logs. |
| l8-solving-for-the-power | screens[9].wrong[div-base] | slip 1.87 | correct | slip reproduced: You divided 2 by 1.07. That undoes one year of growth, not $n$ of them. |
| l8-solving-for-the-power | screens[9].wrong[flip] | slip 0.098 | correct | slip reproduced: You divided $\log 1.07$ by $\log 2$. The log of the growth factor goes on the bottom. |
| l8-solving-for-the-power | quiz[q-2x-12].widget.answer | key 3.585 | correct | recomputed: $x = \dfrac{\log 12}{\log 2} \approx 3.58$. |
| l8-solving-for-the-power | quiz[q-2x-12].wrong[div] | slip 6 | correct | slip reproduced: You divided 12 by 2. The 2 carries the power $x$. |
| l8-solving-for-the-power | quiz[q-2x-12].wrong[flip] | slip 0.279 | correct | slip reproduced: You put $\log 12$ on the bottom. Divide by $\log 2$. |
| l8-solving-for-the-power | quiz[q-coefficient].widget.answer | key 4 | correct | recomputed: $1.5^n = 5.0625 = 1.5^4$. |
| l8-solving-for-the-power | quiz[q-coefficient].wrong[merge] | slip 1.297 | correct | slip reproduced: You merged 40 and 1.5 into 60. Only 1.5 carries the power. |
| l8-solving-for-the-power | quiz[q-halvings].widget.answer | key 8 | correct | recomputed: $2^8 = 256 > 250$, so 8 halvings: £9.77. |
| l8-solving-for-the-power | quiz[q-halvings].wrong[short] | slip 7 | correct | slip reproduced: After 7 halvings it is worth £19.53, still above £10.00. |
| l8-solving-for-the-power | quiz[q-halvings].wrong[ratio] | slip 250 | correct | slip reproduced: 250 is the factor to undo. Count the halvings that make it. |
| l8-solving-for-the-power | quiz[q-decay].widget.answer | key 3.106 | correct | recomputed: $n = \dfrac{\log 0.5}{\log 0.8} \approx 3.11$ months. |
| l8-solving-for-the-power | quiz[q-decay].wrong[sign] | slip -3.106 | correct | slip reproduced: You lost a minus sign. Both logs are negative, so their quotient is positive. |
| l8-solving-for-the-power | quiz[q-decay].wrong[flip] | slip 0.322 | correct | slip reproduced: You put $\log 0.5$ on the bottom. Divide by $\log 0.8$, the log of the growth factor. |
| review-2 | items[r-log2-128].widget.answer | key 7 | correct | recomputed: $2^7 = 128$. |
| review-2 | items[r-log2-128].wrong[divided] | slip 64 | correct | slip reproduced: You divided 128 by 2. The log counts how many 2s multiply to make 128. |
| review-2 | items[r-log2-128].wrong[count-terms] | slip 8 | correct | slip reproduced: You counted 1, 2, 4, ..., 128 as eight numbers. The 1 is the start, not a doubling. |
| review-2 | items[r-product].widget.answer | key 5 | correct | recomputed: $2 + 3 = 5$. |
| review-2 | items[r-product].wrong[mult] | slip 6 | correct | slip reproduced: You multiplied the logs, $2 \times 3$. A product inside the log becomes a sum. |
| review-2 | items[r-product].wrong[number] | slip 243 | correct | slip reproduced: That is $9 \times 27$ itself. Its log counts the 3s. |
| review-2 | items[r-between-3].widget.answer | key 5 | correct | recomputed: $3^4 = 81 < 200 < 243 = 3^5$, so hour 5. |
| review-2 | items[r-between-3].wrong[low] | slip 4 | correct | slip reproduced: After 4 hours there are $3^4 = 81$ cells, still under 200. |
| review-2 | items[r-between-3].wrong[third] | slip 67 | correct | slip reproduced: You divided 200 by 3. A log counts factors of 3. |
| review-2 | items[r-between-3].wrong[digits] | slip 3 | correct | slip reproduced: You counted the digits of 200. That is the base-10 count, not powers of 3. |
| review-2 | items[r-change-base].widget.answer | key 2.161 | correct | recomputed: $1.301 \div 0.602 \approx 2.16$. |
| review-2 | items[r-change-base].wrong[flip] | slip 0.463 | correct | slip reproduced: You divided $\log 4$ by $\log 20$. The base's log goes on the bottom. |
| review-2 | items[r-change-base].wrong[quot] | slip 0.699 | correct | slip reproduced: That is $\log 5 = \log \tfrac{20}{4}$. A quotient of logs is not the log of a quotient. |
| review-2 | items[r-sum-trap].options[ans] (key) | None of these, in general | correct | derivation: There is no law for the log of a sum. |
| review-2 | items[r-sum-trap].options[sum] | $\log a + \log b$ | correct | wrong option, wrong under every convention: That is $\log(ab)$. With $a = b = 1$ it gives 0, but $\log 2 \approx 0.301$. |
| review-2 | items[r-sum-trap].options[prod] | $\log a \times \log b$ | correct | wrong option, wrong under every convention: With $a = b = 10$ it gives 1, but $\log 20 \approx 1.301$. |
| review-2 | items[r-sum-trap].options[ab] | $\log(ab)$ | correct | wrong option, wrong under every convention: That equals $\log a + \log b$. It matches $\log(a + b)$ only when $ab = a + b$, as at $a = b = 2$. … |
| review-2 | items[r-solve].widget.answer | key 6.026 | correct | recomputed: $n = \dfrac{\log 3}{\log 1.2} \approx 6.03$. |
| review-2 | items[r-solve].wrong[div] | slip 2.5 | correct | slip reproduced: You divided 3 by 1.2. The 1.2 is raised to the power $n$. |
| review-2 | items[r-solve].wrong[flip] | slip 0.166 | correct | slip reproduced: You put $\log 3$ on the bottom. Divide by $\log 1.2$. |
| review-2 | items[r-fund-target].widget.answer | key 9 | correct | recomputed: $n > \dfrac{\log 1.6}{\log 1.06} \approx 8.07$, so 9 years. |
| review-2 | items[r-fund-target].wrong[short] | slip 8 | correct | slip reproduced: After 8 years the fund is worth £7,969.24, just short of £8,000.00. |
| review-2 | items[r-fund-target].wrong[simple] | slip 10 | correct | slip reproduced: That is simple interest: £300.00 a year for 10 years. Compounding gets there sooner. |
| review-2 | items[r-decibel].widget.answer | key 100 | correct | recomputed: $10^{20/10} = 100$. |
| review-2 | items[r-decibel].wrong[diff] | slip 20 | correct | slip reproduced: You subtracted the readings and stopped. A gap of 20 is two tenfold steps, since each step is 10 un… |
| review-2 | items[r-decibel].wrong[ratio] | slip 1.465 | correct | slip reproduced: You divided the readings. On a log scale the gap matters, not the ratio of readings. |
| review-2 | items[r-decibel].wrong[tenpow] | slip 1e+20 | correct | slip reproduced: You raised 10 to the gap of 20. The scale has a factor 10 in front, so divide the gap by 10 first. |
| homework-2 | items[h-drawdown].explain | dividing by a negative log flips the inequality | correct | log 0.85 < 0 |
| homework-2 | items[h-long-doubling].model | T(7%) = 10.24, year 11 balance 2,104.85; T(14%) = 5.29, not 5.12, because log 1.14 is not 2 log 1.07 | correct | concepts script |
| homework-2 | items[h-power-law-order] | proof of the power law from (b^m)^k = b^(mk) | correct | standard proof |
| homework-2 | items[h-log8-2].widget.answer | key 0.3333 | correct | recomputed: $8^{1/3} = 2$. |
| homework-2 | items[h-log8-2].wrong[swap] | slip 3 | correct | slip reproduced: You found $\log_2 8$. Here 8 is the base, and 2 is smaller than 8. |
| homework-2 | items[h-log8-2].wrong[div] | slip 4 | correct | slip reproduced: You divided 8 by 2. The log is a power on 8. |
| homework-2 | items[h-expression].widget.answer | key 3p-\frac{q}{2} | correct | derivation: $3p - \tfrac{1}{2}q$. |
| homework-2 | items[h-expression].wrong[root-inside] | slip 3p-\sqrt{q} | correct | not equivalent to the key; You took the root of the log. $\sqrt{y} = y^{1/2}$, so the power law gives $\tfrac{1}{2}q$. |
| homework-2 | items[h-expression].wrong[divide] | slip \frac{3p}{q/2} | correct | not equivalent to the key; You divided the logs. A quotient inside the log becomes a difference. |
| homework-2 | items[h-expression].wrong[no-half] | slip 3p-q | correct | not equivalent to the key; You dropped the square root. $\sqrt{y}$ is $y^{1/2}$, so its log is $\tfrac{1}{2}q$. |
| homework-2 | items[h-log-chart-fall].widget.answer | key 18 | correct | recomputed: £24.00 × 0.75 = £18.00: both fell 25%. |
| homework-2 | items[h-log-chart-fall].wrong[pounds] | slip 4 | correct | slip reproduced: You took away the same £20.00. From £24.00 that would be a fall of 83%, not 25%. |
| homework-2 | items[h-log-chart-fall].wrong[same-end] | slip 60 | correct | slip reproduced: Equal heights do not mean equal end prices. Copy the ratio: ×0.75. |
| homework-2 | items[h-drawdown].widget.answer | key 9 | correct | recomputed: $n > \dfrac{\log 0.25}{\log 0.85} \approx 8.53$, so 9 months. |
| homework-2 | items[h-drawdown].wrong[simple] | slip 6 | correct | slip reproduced: You took £1,800.00 off each month. Each loss is 15% of what is left, so the losses shrink. |
| homework-2 | items[h-drawdown].wrong[short] | slip 8 | correct | slip reproduced: After 8 months the capital is £3,269.89, still above £3,000.00. |
| homework-2 | items[h-drawdown].wrong[raw] | slip 8.53 | correct | slip reproduced: That is the exact solution, 8.53. Months come whole, so the first month below is the next one. |
| homework-2 | items[h-select-forms].options[cb10] (key) | $\dfrac{\log 50}{\log 2}$ | correct | derivation: Any base works for the change of base rule, and the laws split 50 as $2 \times 5^2$. |
| homework-2 | items[h-select-forms].options[cb3] (key) | $\dfrac{\log_3 50}{\log_3 2}$ | correct | derivation: Any base works for the change of base rule, and the laws split 50 as $2 \times 5^2$. |
| homework-2 | items[h-select-forms].options[split] (key) | $1 + \log_2 25$ | correct | derivation: Any base works for the change of base rule, and the laws split 50 as $2 \times 5^2$. |
| homework-2 | items[h-select-forms].options[power] (key) | $1 + 2\log_2 5$ | correct | derivation: Any base works for the change of base rule, and the laws split 50 as $2 \times 5^2$. |
| homework-2 | items[h-select-forms].options[quot] | $\log 25$ | correct | wrong option, wrong under every convention: That is $\log \tfrac{50}{2}$, about 1.398. A quotient of logs is not the log of a quotient. |
| homework-2 | items[h-select-forms].options[ratio] | $\dfrac{50}{2}$ | correct | wrong option, wrong under every convention: That divides the numbers, giving 25. The rule divides their logs. |
| homework-2 | items[h-power-law-order].widget.answer | order name > mean > raise > read > sub | correct | each line follows from the one before; Name, rewrite as a power, use the index law, read the log, substitute. |
| homework-2 | items[h-overtake].widget.answer | key 17 | correct | recomputed: $n > \dfrac{\log 2.5}{\log(1.09 / 1.03)} \approx 16.18$, so 17 years. |
| homework-2 | items[h-overtake].wrong[short] | slip 16 | correct | slip reproduced: After 16 years A is worth £1,588.12 and B £1,604.71. A is still behind. |
| homework-2 | items[h-overtake].wrong[raw] | slip 16.18 | correct | slip reproduced: That is the exact crossing, 16.18. The first whole year after it is 17. |
| problems-2 | items[p-fault-search].prose | halving search needs the smallest whole k with 2^k >= N | correct | binary search bound ceil(log_2 N) |
| problems-2 | items[p-fault-search].parts[0].widget.answer | key 11 | correct | recomputed: $2^{11} = 2048$, so $\log_2 2048 = 11$ checks. |
| problems-2 | items[p-fault-search].parts[0].wrong[halved] | slip 1024 | correct | slip reproduced: 1,024 is the number left after one check. The checks count the halvings: $\log_2 2048 = 11$. |
| problems-2 | items[p-fault-search].parts[0].wrong[off-by-one] | slip 10 | correct | slip reproduced: $2^{10} = 1024$, which is only half the batch. You need $2^{11} = 2048$. |
| problems-2 | items[p-fault-search].parts[1].widget.answer | key 16 | correct | recomputed: $\log_2(32 \times 2048) = \log_2 32 + \log_2 2048 = 5 + 11 = 16$. |
| problems-2 | items[p-fault-search].parts[1].wrong[multiplied-logs] | slip 55 | correct | slip reproduced: You multiplied the logs, $5 \times 11$. A product of numbers adds the logs: $5 + 11 = 16$. |
| problems-2 | items[p-fault-search].parts[1].wrong[times-batches] | slip 352 | correct | slip reproduced: You searched each batch in turn, 32 lots of 11 checks. Halving the whole day at once needs only $5 … |
| problems-2 | items[p-fault-search].parts[1].wrong[added-count] | slip 43 | correct | slip reproduced: You added 32 to 11. Add the logs instead: $\log_2 32 = 5$, so $5 + 11 = 16$. |
| problems-2 | items[p-fault-search].parts[1].wrong[carried] | slip 15 | correct | slip reproduced: That uses 10 checks for a batch. A batch of $2^{11}$ trades needs 11, so the day needs $5 + 11 = 16… |
| problems-2 | items[p-fault-search].parts[2].widget.answer | key 19 | correct | recomputed: $\log_2 327{,}680 = 16 + \log_2 5$, which is between 18 and 19. Since $2^{19} = 524{,}288$ covers t… |
| problems-2 | items[p-fault-search].parts[2].wrong[rounded-down] | slip 18 | correct | slip reproduced: $2^{18} = 262{,}144$, fewer than the week's trades. 18 checks leave some trades unsearched, so you … |
| problems-2 | items[p-fault-search].parts[2].wrong[added-five] | slip 21 | correct | slip reproduced: You added 5 for the 5 days. Add $\log_2 5$, which is between 2 and 3, not 5. |
| problems-2 | items[p-fault-search].parts[2].wrong[times-five] | slip 80 | correct | slip reproduced: You multiplied the 16 checks by 5. A product of numbers adds logs: $16 + \log_2 5$. |
| problems-2 | items[p-forty-doublings].parts[0].widget.answer | key 12.0412 | correct | recomputed: By the power law, $\log(2^{40}) = 40 \log 2 \approx 40 \times 0.30103 = 12.0412$. |
| problems-2 | items[p-forty-doublings].parts[0].wrong[swapped] | slip 3.2041 | correct | slip reproduced: That is $\log(40^2)$. Here the base is 2 and the power is 40: $40 \log 2$. |
| problems-2 | items[p-forty-doublings].parts[0].wrong[added] | slip 40.301 | correct | slip reproduced: You added 40 to $\log 2$. A power multiplies the log: $40 \times 0.30103$. |
| problems-2 | items[p-forty-doublings].parts[1].widget.answer | key 12 | correct | recomputed: $12 < 12.0412 < 13$, so $10^{12} < 2^{40} < 10^{13}$ and $n = 12$. |
| problems-2 | items[p-forty-doublings].parts[1].wrong[rounded-up] | slip 13 | correct | slip reproduced: 13 is the upper end. $10^{13}$ has log 13, above 12.0412, so $2^{40}$ lies below it. |
| problems-2 | items[p-forty-doublings].parts[1].wrong[power] | slip 40 | correct | slip reproduced: 40 is the number of doublings. The log 12.0412 counts tenfold steps. |
| problems-2 | items[p-forty-doublings].parts[1].wrong[carried] | slip 3 | correct | slip reproduced: That uses a log of 3.2041, from $40^2$. With $\log(2^{40}) = 12.0412$, $n = 12$. |
| problems-2 | items[p-forty-doublings].parts[2].widget.answer | key 1.0995 | correct | recomputed: $2^{40} = 10^{0.0412} \times 10^{12}$, so $m = 10^{0.0412} \approx 1.10$. |
| problems-2 | items[p-forty-doublings].parts[2].wrong[fraction-part] | slip 0.0412 | correct | slip reproduced: 0.0412 is $\log m$, not $m$. Undo the log: $m = 10^{0.0412} \approx 1.10$. |
| problems-2 | items[p-forty-doublings].parts[2].wrong[one-plus] | slip 1.0412 | correct | slip reproduced: You took $m$ as $1 + 0.0412$. Undo the log instead: $m = 10^{0.0412} \approx 1.10$. |
| problems-2 | items[p-forty-doublings].parts[3].widget.answer | key 14 | correct | recomputed: The money must grow by a factor of $\tfrac{10^{16}}{1.10 \times 10^{12}} \approx 9091$. $\tfrac{\lo… |
| problems-2 | items[p-forty-doublings].parts[3].wrong[rounded-down] | slip 13 | correct | slip reproduced: Thirteen more doublings multiply by 8192, short of the 9091 needed. A fourteenth is needed. |
| problems-2 | items[p-forty-doublings].parts[3].wrong[tenfold-steps] | slip 4 | correct | slip reproduced: About 4 is the gap in tenfold steps, $\log 9091 \approx 3.96$. Each doubling is only 0.30103 of a s… |
| problems-2 | items[p-forty-doublings].parts[3].wrong[total] | slip 54 | correct | slip reproduced: 54 counts every doubling from £1. The question asks for the doublings after the first 40. |
| problems-2 | items[p-drawdown-recovery].parts[0].widget.answer | key 32000 | correct | recomputed: $50{,}000 \times 0.8^2 = 50{,}000 \times 0.64 = 32{,}000$, so £32,000. |
| problems-2 | items[p-drawdown-recovery].parts[0].wrong[added-falls] | slip 30000 | correct | slip reproduced: You took 40% off at once. The second fall is 20% of £40,000, not of £50,000. |
| problems-2 | items[p-drawdown-recovery].parts[0].wrong[one-fall] | slip 40000 | correct | slip reproduced: £40,000 is the value after one fall. The second multiplies by 0.8 again. |
| problems-2 | items[p-drawdown-recovery].parts[1].widget.answer | key 0.5625 (unit %) | correct | recomputed: $\tfrac{50{,}000}{32{,}000} = 1.5625$, a gain of 56.25%. |
| problems-2 | items[p-drawdown-recovery].parts[1].wrong[two-twenties] | slip 0.4 | correct | slip reproduced: Two gains of 20% would only reach $32{,}000 \times 1.2^2 = 46{,}080$ pounds. A gain is measured fro… |
| problems-2 | items[p-drawdown-recovery].parts[1].wrong[the-loss] | slip 0.36 | correct | slip reproduced: 36% is the loss, measured from £50,000. The gain back is measured from £32,000, so it is larger. |
| problems-2 | items[p-drawdown-recovery].parts[1].wrong[factor] | slip 1.5625 | correct | slip reproduced: 156.25% is the whole factor 1.5625 as a percentage. The gain is the part above 1: 56.25%. |
| problems-2 | items[p-drawdown-recovery].parts[1].wrong[carried] | slip 0.6667 | correct | slip reproduced: That starts from £30,000. From £32,000 the gain needed is $\tfrac{50{,}000}{32{,}000} - 1 = 56.25\%… |
| problems-2 | items[p-drawdown-recovery].parts[1].wrong[decimal] | slip 0.005625 | correct | slip reproduced: In this box, 0.5625 reads as 0.5625%. Type the percentage, 56.25. |
| problems-2 | items[p-drawdown-recovery].parts[2].widget.answer | key 4.2764 | correct | recomputed: $n \log 1.11 = 2 \log 1.25$, so $n \approx \tfrac{2 \times 0.09691}{0.04532} \approx 4.28$ months. |
| problems-2 | items[p-drawdown-recovery].parts[2].wrong[no-power] | slip 2.14 | correct | slip reproduced: You used $\log 1.25$ once. The power law makes $\log(1.25^2) = 2 \log 1.25$. |
| problems-2 | items[p-drawdown-recovery].parts[2].wrong[inverted] | slip 0.23 | correct | slip reproduced: You divided $\log 1.11$ by $2\log 1.25$. Solve $n \log 1.11 = 2\log 1.25$ for $n$ by dividing by $\… |
| problems-2 | items[p-drawdown-recovery].parts[2].wrong[simple] | slip 5.11 | correct | slip reproduced: That shares 56.25% out as 11% a month with no compounding. Each month's 11% grows on the last, so i… |
| problems-2 | items[p-drawdown-recovery].parts[2].wrong[carried] | slip 3.22 | correct | slip reproduced: That solves $1.11^n = 1.4$, from a 40% gain. The factor needed is 1.5625. |
| problems-2 | items[p-drawdown-recovery].parts[2].wrong[divided-numbers] | slip 1.41 | correct | slip reproduced: You divided 1.5625 by 1.11. The power $n$ comes down only after taking logs. |
| problems-2 | items[p-drawdown-recovery].parts[3].widget.answer | key 5 | correct | recomputed: After 4 months it holds about £48,578, still short. After 5 months it holds about £53,922, so 5 mon… |
| problems-2 | items[p-drawdown-recovery].parts[3].wrong[rounded-down] | slip 4 | correct | slip reproduced: After 4 months it holds $32{,}000 \times 1.11^4 \approx 48{,}578$ pounds, still below £50,000. |
| problems-2 | items[p-drawdown-recovery].parts[3].wrong[with-falls] | slip 7 | correct | slip reproduced: 7 counts the two months of falls as well. The question asks for months of growth only. |
| problems-2 | items[p-app-users].parts[0].widget.answer | key 2000\cdot1.3^{n} | correct | derivation: Each month multiplies by $1 + 0.3 = 1.3$: $U = 2000 \times 1.3^n$. |
| problems-2 | items[p-app-users].parts[0].wrong[rate-only] | slip 2000\cdot0.3^{n} | correct | not equivalent to the key; 0.3 is the rise alone, and $0.3^n$ shrinks. The factor keeps the whole too: 1.3. |
| problems-2 | items[p-app-users].parts[0].wrong[joined] | slip 2600^{n} | correct | not equivalent to the key; You raised $2000 \times 1.3$ to the power. Only the 1.3 is repeated: $2000 \times 1.3^n$. |
| problems-2 | items[p-app-users].parts[0].wrong[steady] | slip 2000+600n | correct | not equivalent to the key; That adds 600 users each month, 30% of the first 2,000. The 30% acts on the users there now, so it … |
| problems-2 | items[p-app-users].parts[1].options[ratio] (key) | $\dfrac{\log 25}{\log 1.3}$ | correct | derivation: Change of base: $\log_{1.3} 25 = \tfrac{\log 25}{\log 1.3}$, in any one base. |
| problems-2 | items[p-app-users].parts[1].options[quotient] | $\log \dfrac{25}{1.3}$ | correct | wrong option, wrong under every convention: That is the log of a quotient, about 1.284. Change of base divides one log by the other. |
| problems-2 | items[p-app-users].parts[1].options[difference] | $\log 25 - \log 1.3$ | correct | wrong option, wrong under every convention: Subtracting logs gives $\log \tfrac{25}{1.3} \approx 1.284$. Change of base divides the logs. |
| problems-2 | items[p-app-users].parts[1].options[numbers] | $\dfrac{25}{1.3}$ | correct | wrong option, wrong under every convention: That divides the numbers and gives about 19.23, but $1.3^{19.23}$ is far above 25. |
| problems-2 | items[p-app-users].parts[2].widget.answer | key 12.2687 | correct | recomputed: $n \log 1.3 = \log 25$, so $n = \tfrac{\log 25}{\log 1.3} \approx \tfrac{1.3979}{0.1139} \approx 12… |
| problems-2 | items[p-app-users].parts[2].wrong[joined] | slip 1.38 | correct | slip reproduced: That solves $2600^n = 50{,}000$. The equation to solve is $1.3^n = 25$. |
| problems-2 | items[p-app-users].parts[2].wrong[divided] | slip 19.23 | correct | slip reproduced: You divided 25 by 1.3. Take logs first, then divide the logs: $\tfrac{\log 25}{\log 1.3}$. |
| problems-2 | items[p-app-users].parts[2].wrong[rate-only] | slip -2.67 | correct | slip reproduced: That uses $\log 0.3$, which is negative. The factor is 1.3. |
| problems-2 | items[p-app-users].parts[2].wrong[simple] | slip 80 | correct | slip reproduced: That adds a fixed 600 users a month: $2000 + 600n = 50{,}000$ at $n = 80$. The rise compounds, so i… |
| problems-2 | items[p-app-users].parts[3].widget.answer | key 13 | correct | recomputed: After 12 months it has $2000 \times 1.3^{12} \approx 46{,}596$ users, short of 50,000. After 13 mon… |
| problems-2 | items[p-app-users].parts[3].wrong[rounded-down] | slip 12 | correct | slip reproduced: After 12 months the app has about 46,596 users, still below 50,000. It passes 50,000 during month 1… |
| problems-2 | items[p-app-users].parts[3].wrong[joined] | slip 2 | correct | slip reproduced: That rounds up 1.38, from $2600^n$. The app needs about 12.27 months. |
| fluency-l6-products-into-sums | families[split-a-product].widget.answer | split the log of a product: key {m}p+{n}q | correct | every draw in the whole variable range recomputed (concepts script sweep) |
| fluency-l6-products-into-sums | families[split-a-product].wrong[powers-left-behind] | p+q: You left the powers behind: the power law brings each one down in front. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l6-products-into-sums | families[split-a-product].wrong[multiplied-the-logs] | {mn}pq: A product inside the log becomes a sum of logs, not a product. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l6-products-into-sums | families[split-a-quotient].widget.answer | split the log of a quotient: key {m}p-{n}q | correct | every draw in the whole variable range recomputed (concepts script sweep) |
| fluency-l6-products-into-sums | families[split-a-quotient].wrong[added-for-divide] | {m}p+{n}q: Dividing inside the log subtracts the logs: the $y$ term takes a minus. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l6-products-into-sums | families[split-a-quotient].wrong[divided-the-logs] | \frac{{{m}p}}{{{n}q}}: A quotient inside the log becomes a difference of logs, not a quotient of them. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l6-products-into-sums | families[combine-a-sum].widget.answer | combine a sum of logs: key {n} | correct | every draw in the whole variable range recomputed (concepts script sweep) |
| fluency-l6-products-into-sums | families[combine-a-sum].wrong[log-of-the-sum] | {ofsum}: You added {x} and {y} inside one log: adding logs multiplies the numbers inside. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l6-products-into-sums | families[combine-a-sum].wrong[multiplied-the-logs] | {times}: You multiplied the two logs: the product law turns a sum of logs into the log of a product. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l6-products-into-sums | families[combine-a-difference].widget.answer | combine a difference of logs: key {n} | correct | every draw in the whole variable range recomputed (concepts script sweep) |
| fluency-l6-products-into-sums | families[combine-a-difference].wrong[divided-the-logs] | {divided}: You divided one log by the other: the quotient law turns a difference of logs into the log of a qu… | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l6-products-into-sums | families[combine-a-difference].wrong[subtracted-inside] | {inside}: You took {c} from {top} inside the log: subtracting logs divides the numbers inside. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l8-solving-for-the-power | families[exact-power].widget.answer | solve for the power exactly: key \frac{{\log {b}}}{{\log {a}}} | correct | every draw in the whole variable range recomputed (concepts script sweep) |
| fluency-l8-solving-for-the-power | families[exact-power].wrong[upside-down] | \frac{{\log {a}}}{{\log {b}}}: That is upside down: $\log {b}$, the log of the answer side, goes on top. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l8-solving-for-the-power | families[exact-power].wrong[divided-the-numbers] | {b/a:frac}: You divided {b} by {a}: take logs first, then divide the logs. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l8-solving-for-the-power | families[power-to-3-sf].widget.answer | solve for the power to 3 significant figures: key {round(r, 6)} | correct | every draw in the whole variable range recomputed (concepts script sweep) |
| fluency-l8-solving-for-the-power | families[power-to-3-sf].wrong[upside-down] | {round(flip, 6)}: That is upside down: $\log {b}$, the log of the answer side, goes on top. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l8-solving-for-the-power | families[power-to-3-sf].wrong[divided-the-numbers] | {ratio}: You divided {b} by {a}: take logs first, then divide the logs. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l8-solving-for-the-power | families[power-alone-first].widget.answer | get the power alone, then solve: key {n} | correct | every draw in the whole variable range recomputed (concepts script sweep) |
| fluency-l8-solving-for-the-power | families[power-alone-first].wrong[stopped-early] | {an}: That is ${a}^{v}$: one more step finds the power ${v}$ itself. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l8-solving-for-the-power | families[power-alone-first].wrong[joined-the-base] | {round(joined, 6)}: ${c} \times {a}^{v}$ is not ${ca}^{v}$: divide by {c} first. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l8-solving-for-the-power | families[money-target].widget.answer | get the power alone, then solve to 3 significant figures: key {round(r, 6)} | correct | every draw in the whole variable range recomputed (concepts script sweep) |
| fluency-l8-solving-for-the-power | families[money-target].wrong[joined-the-base] | {round(joined, 6)}: ${p} \times {g}^{v}$ is not $({p} \times {g})^{v}$: divide by {p} first. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l8-solving-for-the-power | families[money-target].wrong[logs-too-soon] | {round(early, 6)}: You took logs before getting the power alone: divide by {p} first. | misleading | value is ln(target)/ln(g) or ln(target)/k: the start amount was dropped. Taking logs first, done correctly, gives the key (l8 screens[4]). Finding 2 |
| l9-compounding-more-often | screens[2] | (1 + 1/n)^n rises more and more slowly and stays under e | correct | Rudin 3.31 (monotone, bounded by e); concepts script n = 1..5000 |
| l9-compounding-more-often | screens[2].explain.canvas.points[P].y | P at n = 52 has height 2.6916 | wrong | (1 + 1/52)^52 = 2.6926 (concepts script). The text beside it, 2.69, is right. Finding 1 |
| l9-compounding-more-often | screens[3].prose | e = 2.71828..., never ends or repeats (irrational); e is the limit of (1 + 1/n)^n | correct | Rudin 3.31-3.32 |
| l9-compounding-more-often | screens[4].explain | a rate r compounded without limit multiplies by e^r each year | correct | lim (1 + r/n)^n = e^r |
| l9-compounding-more-often | screens[7].prose | (1 + r/n)^(nt) -> e^(rt); A = P e^(rt); r as a decimal, t in years | correct | Hull, ch. 4 (continuous compounding) |
| l9-compounding-more-often | screens[6].explain | 6% continuous is worth 6.18% a year; compare e^r with 1 + r | correct | e^0.06 - 1 = 0.0618 |
| l9-compounding-more-often | screens[8] | derivation with m = n/r: ((1 + 1/m)^m)^r -> e^r (as written for r > 0; the negative-rate quiz item uses the r… | correct | standard substitution |
| l9-compounding-more-often | screens[9].prose | the once-a-year equivalent of a rate is what UK banks call the AER | correct | UK savings convention (annual equivalent rate) |
| l9-compounding-more-often | summary.trap | continuous compounding does not always beat a higher rate paid once | correct | e^0.06 < 1.062 |
| l9-compounding-more-often | screens[1].options[less] | Less than £2.25 | correct | wrong option, wrong under every convention: You expected tiny payments to add up to less. Each one earns interest on all the interest before it… |
| l9-compounding-more-often | screens[1].options[right] (key) | Between £2.25 and £3.00 | correct | derivation: The total creeps up, but it never reaches £3.00. |
| l9-compounding-more-often | screens[1].options[mid] | Between £3.00 and £100.00 | correct | wrong option, wrong under every convention: You expected the extra growth to keep piling up. Each payment shrinks as the number of payments gro… |
| l9-compounding-more-often | screens[1].options[huge] | More than £1,000,000.00 | correct | wrong option, wrong under every convention: You treated 31 million payments as 31 million chances to grow a lot. Each one is only a 31-milliont… |
| l9-compounding-more-often | screens[2].options[right] (key) | It rises more and more slowly, and stays under the dashed line | correct | derivation: The gains shrink as $n$ grows, and the curve hugs the dashed line. |
| l9-compounding-more-often | screens[2].options[steady] | It rises by about the same amount at each step | correct | wrong option, wrong under every convention: You read the first few steps only. From 1 to 2 it gains 25p; from 51 to 52 it gains far less than 1… |
| l9-compounding-more-often | screens[2].options[falls] | It rises, then falls back | correct | wrong option, wrong under every convention: You may have read the flattening as a fall. Every extra payment adds a little; the value never drop… |
| l9-compounding-more-often | screens[2].options[stops] | It stops changing after $n = 12$ | correct | wrong option, wrong under every convention: It still changes after 12, just by less. At 12 it is £2.61 and at 52 it is £2.69. |
| l9-compounding-more-often | screens[3].rows[2][1] | key 2.4414 | correct | recomputed: 2.4414 and 2.6130: the climb slows as it nears $e$. |
| l9-compounding-more-often | screens[3].rows[3][1] | key 2.613 | correct | recomputed: 2.4414 and 2.6130: the climb slows as it nears $e$. |
| l9-compounding-more-often | screens[4].options[right] (key) | $100e^{0.1}$, about £110.52 | correct | derivation: At 10%, compounding without limit gives a factor of $e^{0.1} = 1.1052$. |
| l9-compounding-more-often | screens[4].options[e] | $100e$, about £271.83 | correct | wrong option, wrong under every convention: You used the 100% limit. The rate is now 10%, so the bars stay near £110, nowhere near £271. |
| l9-compounding-more-often | screens[4].options[times] | $100 \times 0.1e$, about £27.18 | correct | wrong option, wrong under every convention: You multiplied $e$ by the rate. That is less than the £100.00 you started with. |
| l9-compounding-more-often | screens[4].options[once] | $100 \times 1.1$, exactly £110.00 | correct | wrong option, wrong under every convention: That is one payment a year, the first bar. The other bars are already above it. |
| l9-compounding-more-often | screens[5].widget.answer | key 1648.72 | correct | recomputed: $1000e^{0.05 \times 10} = 1000e^{0.5} = 1648.72$. |
| l9-compounding-more-often | screens[5].wrong[yearly] | slip 1628.89 | correct | slip reproduced: That is $1000 \times 1.05^{10}$, paid once a year. Continuous compounding pays a little more. |
| l9-compounding-more-often | screens[5].wrong[one-year] | slip 1051.27 | correct | slip reproduced: You applied one year only. Ten years multiply by $e^{0.05}$ ten times. |
| l9-compounding-more-often | screens[5].wrong[times-ten] | slip 10512.71 | correct | slip reproduced: You multiplied by 10 instead of compounding for 10 years. The years multiply the power, not the ans… |
| l9-compounding-more-often | screens[5].wrong[simple] | slip 1500 | correct | slip reproduced: That adds 5% of £1,000.00 each year, with no interest on interest. |
| l9-compounding-more-often | screens[6].options[a] | A, because continuous compounding always beats paying once | correct | wrong option, wrong under every convention: You let the compounding decide on its own. $10000e^{0.06} = 10618.37$, so A pays £10,618.37, less t… |
| l9-compounding-more-often | screens[6].options[b] (key) | B | correct | derivation: B pays £10,620.00 and A pays £10,618.37. |
| l9-compounding-more-often | screens[6].options[same] | They pay the same | correct | wrong option, wrong under every convention: You treated 6% continuous as worth 6.2% a year. $e^{0.06} = 1.0618$, so it is worth 6.18% a year. |
| l9-compounding-more-often | screens[7].options[right] (key) | $r = 0.04$ | correct | derivation: The rate goes in as a decimal. |
| l9-compounding-more-often | screens[7].options[four] | $r = 4$ | correct | wrong option, wrong under every convention: You typed the percentage. $e^{4}$ is about 54.6, so each year would multiply the money by 54.6. |
| l9-compounding-more-often | screens[7].options[factor] | $r = 1.04$ | correct | wrong option, wrong under every convention: You used the yearly growth factor. In $e^{rt}$ the rate goes in alone; the factor comes out as $e^{… |
| l9-compounding-more-often | screens[8].widget.answer | order s1 > s2 > s3 > s4 > s5 | correct | each line follows from the one before; The bracket becomes the one from the table, raised to the power $r$. |
| l9-compounding-more-often | screens[9].widget.answer | key 0.05127 (unit %) | correct | recomputed: $e^{0.05} - 1 = 0.0513$, so 5.13% paid once a year. |
| l9-compounding-more-often | screens[9].wrong[same] | slip 0.05 | correct | slip reproduced: You kept 5.00%. Continuous compounding earns interest on interest, so the yearly rate is a little h… |
| l9-compounding-more-often | screens[9].wrong[times-e] | slip 0.1359 | correct | slip reproduced: You multiplied 0.05 by $e$. The rate goes in the power: $e^{0.05}$. |
| l9-compounding-more-often | quiz[q-continuous-three].widget.answer | key 2818.74 | correct | recomputed: $2500e^{0.04 \times 3} = 2500e^{0.12} = 2818.74$. |
| l9-compounding-more-often | quiz[q-continuous-three].wrong[yearly] | slip 2812.16 | correct | slip reproduced: That is $2500 \times 1.04^3$, paid once a year. Continuous compounding pays a little more. |
| l9-compounding-more-often | quiz[q-continuous-three].wrong[one-year] | slip 2602.03 | correct | slip reproduced: You used one year. Three years make the power $0.04 \times 3 = 0.12$. |
| l9-compounding-more-often | quiz[q-thousand-parts].options[right] (key) | 2.717 | correct | derivation: It is 2.71692, just under $e$. |
| l9-compounding-more-often | quiz[q-thousand-parts].options[tiny] | 1.001 | correct | wrong option, wrong under every convention: You took one part as the whole year. There are 1,000 of them, each multiplying by 1.001. |
| l9-compounding-more-often | quiz[q-thousand-parts].options[two] | 2.000 | correct | wrong option, wrong under every convention: You expected splitting to change nothing. Interest on interest lifts it above 2. |
| l9-compounding-more-often | quiz[q-thousand-parts].options[big] | Over 1,000 | correct | wrong option, wrong under every convention: You saw a large power and expected a large answer. The base is barely above 1. |
| l9-compounding-more-often | quiz[q-negative-rate].widget.answer | key 4950.25 | correct | recomputed: $5000e^{-0.005 \times 2} = 5000e^{-0.01} = 4950.25$. |
| l9-compounding-more-often | quiz[q-negative-rate].wrong[sign] | slip 5050.25 | correct | slip reproduced: You dropped the minus sign. A negative rate shrinks the deposit. |
| l9-compounding-more-often | quiz[q-negative-rate].wrong[simple] | slip 4950.0 | correct | slip reproduced: You took 0.5% off twice, as simple interest. Continuous compounding takes it off a shrinking balanc… |
| l9-compounding-more-often | quiz[q-quarterly-or-continuous].options[x] (key) | Bank X | correct | derivation: X: $1.02^4 = 1.0824$. Y: $e^{0.079} = 1.0822$. |
| l9-compounding-more-often | quiz[q-quarterly-or-continuous].options[y] | Bank Y | correct | wrong option, wrong under every convention: You let continuous compounding win by default. $e^{0.079} = 1.0822$, below X's $1.02^4 = 1.0824$. |
| l9-compounding-more-often | quiz[q-quarterly-or-continuous].options[same] | They are the same | correct | wrong option, wrong under every convention: You expected the extra compounding to make up the 0.1% exactly. Work out both factors to four place… |
| l10-natural-log | screens[2].explain | gradient of e^x equals its height; that is why e is the natural base | correct | d/dx e^x = e^x |
| l10-natural-log | screens[3].prose | ln x = log_e x; calculators have separate ln and log keys; Python math.log is ln | correct | convention stated: log is base 10 in this course, ln is base e |
| l10-natural-log | screens[3].explain | any number to the power 0 is 1 | imprecise | 0^0 is not defined (Gelfand and Shen define a^0 = 1 for a not 0). Finding 7 |
| l10-natural-log | screens[4].explain | ln x negative for 0 < x < 1, undefined for x <= 0 | correct | real ln, domain x > 0 |
| l10-natural-log | screens[8].prose | e^(ln y) = y, ln(e^x) = x, ln(ab) = ln a + ln b, ln(a^k) = k ln a, b^x = e^(x ln b) | correct | A-level pure |
| l10-natural-log | screens[9] | b^x = e^(x ln b) for any b > 0 | correct | derivation |
| l10-natural-log | screens[10].explain | rates desks quote zero-coupon yields this way (continuously compounded) | imprecise | Hull ch. 4: continuous compounding is the convention of pricing models; market quotes use annual or semi-annual compounding or money-market bases. Finding 3 |
| l10-natural-log | screens[1].widget.points | target [1.609, 5] | correct | recomputed: P sits at about 1.61 years. |
| l10-natural-log | screens[1].wrong[x-five] | region {"x": [2.3, 2.5], "y": [0, 10]} | correct | region is clear of the target band; You moved P to the right-hand edge. The value is £5.00 well before then, at about 1.61 years. |
| l10-natural-log | screens[2].options[right] (key) | The gradient always equals the height | correct | derivation: At every point, gradient and height match. |
| l10-natural-log | screens[2].options[one] | The gradient is always 1 | correct | wrong option, wrong under every convention: That holds only at $x = 0$, where the height is also 1. At $x = 2$ the gradient is 7.39. |
| l10-natural-log | screens[2].options[times-e] | The gradient is the height times $e$ | correct | wrong option, wrong under every convention: Check one point: at $x = 1$ the height is 2.72 and the gradient is 2.72, not 7.39. |
| l10-natural-log | screens[2].options[bigger] | The gradient is bigger than the height, by more and more | correct | wrong option, wrong under every convention: Read both numbers at $x = 2$: the height is 7.39 and the gradient is 7.39. They match. |
| l10-natural-log | screens[3].widget.answer | key 0 | correct | recomputed: $e^0 = 1$, so $\ln 1 = 0$. |
| l10-natural-log | screens[3].wrong[one] | slip 1 | correct | slip reproduced: You gave the number itself. $e^1 = 2.718$, not 1, so $\ln 1$ is not 1. |
| l10-natural-log | screens[3].wrong[e] | slip 2.718 | correct | slip reproduced: You worked forwards, $e^1 = 2.718$. The log runs backwards: which power gives 1? |
| l10-natural-log | screens[4].options[right] (key) | Numbers between 0 and 1 | correct | derivation: Between 0 and 1, $\ln x$ is negative. |
| l10-natural-log | screens[4].options[neg] | Negative numbers | correct | wrong option, wrong under every convention: You expected negative in, negative out. But $e^x$ is never negative, so no power of $e$ gives $-2$:… |
| l10-natural-log | screens[4].options[above] | Numbers above 1 | correct | wrong option, wrong under every convention: Above 1 the curve sits above the axis. $\ln e = 1$, for example. |
| l10-natural-log | screens[4].options[never] | None: $\ln x$ is never negative | correct | wrong option, wrong under every convention: Point A says otherwise: $e^{-1} = 0.368$, so $\ln 0.368 = -1$. |
| l10-natural-log | screens[5].rows[0][1] | key 1.7918 | correct | recomputed: 1.7918, 2.0794 and 0.4055. |
| l10-natural-log | screens[5].rows[1][1] | key 2.0794 | correct | recomputed: 1.7918, 2.0794 and 0.4055. |
| l10-natural-log | screens[5].rows[2][1] | key 0.4055 | correct | recomputed: 1.7918, 2.0794 and 0.4055. |
| l10-natural-log | screens[6].widget.states | target state t = \dfrac{\ln 1.5}{0.04} \approx 10.14 | correct | every state checked as an equation equivalent to the start (dead ends marked with a why); $t = \dfrac{\ln 1.5}{0.04} \approx 10.14$ years. |
| l10-natural-log | screens[7].options[right] (key) | $100e^{1.0986t}$ | imprecise | the item asks for the same growth; e^1.0986 = 2.99996 and e^0.6931 = 1.99996, equal only to 4 dp. Finding 5 |
| l10-natural-log | screens[7].options[three] | $100e^{3t}$ | correct | wrong option, wrong under every convention: You put the yearly factor in the power. $e^3$ is about 20.1, so that grows twentyfold a year. |
| l10-natural-log | screens[7].options[none] | None: an $e$-power always grows slower than $3^t$ | correct | wrong option, wrong under every convention: You compared the bases only. The number in the power sets the speed, and $e^{1.0986} = 3$. |
| l10-natural-log | screens[7].options[front] | $300e^{t}$ | correct | wrong option, wrong under every convention: You moved the 3 out in front. That starts at 300 and multiplies by 2.72 a year, not 3. |
| l10-natural-log | screens[8].options[right] (key) | $0.7$ | correct | derivation: ln undoes $e$ and leaves the power, 0.7. |
| l10-natural-log | screens[8].options[exp] | $e^{0.7}$ | correct | wrong option, wrong under every convention: You applied $e$ again instead of undoing it. ln strips the $e$ off and leaves the power. |
| l10-natural-log | screens[8].options[rate] | $0.07$ | correct | wrong option, wrong under every convention: You kept the rate but dropped the 10. The whole power, $0.07 \times 10$, comes out. |
| l10-natural-log | screens[9].widget.answer | order d1 > d2 > d3 > d4 | correct | each line follows from the one before; Any positive base is $e$ to the power of its log. |
| l10-natural-log | screens[10].widget.answer | key 0.04 (unit %) | correct | recomputed: $r = \tfrac{1}{2}\ln\tfrac{100}{92.31} = 0.0400$, so 4.00%. |
| l10-natural-log | screens[10].wrong[simple] | slip 0.04165 | correct | slip reproduced: You split the 8.33% gain evenly over two years. That ignores compounding; ln gives the continuous r… |
| l10-natural-log | screens[10].wrong[no-half] | slip 0.08 | correct | slip reproduced: That is $2r$, the rate for both years together. Halve it for a yearly rate. |
| l10-natural-log | screens[10].wrong[yearly] | slip 0.04082 | correct | slip reproduced: That is $\sqrt{1.08331} - 1$, the rate paid once a year. The continuous rate is a little lower. |
| l10-natural-log | quiz[q-solve-twenty].widget.answer | key 2.9957 | correct | recomputed: $x = \ln 20 = 3.00$. |
| l10-natural-log | quiz[q-solve-twenty].wrong[divide] | slip 7.358 | correct | slip reproduced: You divided 20 by $e$. The $e$ is a base, so undo it with ln. |
| l10-natural-log | quiz[q-solve-twenty].wrong[ten] | slip 1.301 | correct | slip reproduced: You used the base-10 log. $10^{1.301} = 20$, but here the base is $e$. |
| l10-natural-log | quiz[q-log-difference].options[right] (key) | $\ln 25$ | correct | derivation: $\ln 50 - \ln 2 = \ln \tfrac{50}{2} = \ln 25$. |
| l10-natural-log | quiz[q-log-difference].options[minus] | $\ln 48$ | correct | wrong option, wrong under every convention: You subtracted inside the log. A difference of logs is the log of a quotient. |
| l10-natural-log | quiz[q-log-difference].options[ratio] | $\dfrac{\ln 50}{\ln 2}$ | correct | wrong option, wrong under every convention: You divided the logs themselves. The division happens inside: $\ln \tfrac{50}{2}$. |
| l10-natural-log | quiz[q-log-difference].options[times] | $\ln 100$ | correct | wrong option, wrong under every convention: You multiplied. Adding logs multiplies; subtracting divides. |
| l10-natural-log | quiz[q-reach-ten-thousand].widget.answer | key 15.27 | correct | recomputed: $t = \tfrac{\ln 2.5}{0.06} = 15.27$ years. |
| l10-natural-log | quiz[q-reach-ten-thousand].wrong[simple] | slip 25 | correct | slip reproduced: You worked as if 6% of £4,000.00 is added each year. Continuous growth compounds, so it gets there … |
| l10-natural-log | quiz[q-reach-ten-thousand].wrong[ln-gain] | slip 145.0 | correct | slip reproduced: You took the log of the £6,000.00 gain. Use the ratio of values, $\tfrac{10000}{4000} = 2.5$. |
| l10-natural-log | quiz[q-two-as-e].options[right] (key) | $e^{0.6931t}$ | imprecise | the item asks for the same growth; e^1.0986 = 2.99996 and e^0.6931 = 1.99996, equal only to 4 dp. Finding 5 |
| l10-natural-log | quiz[q-two-as-e].options[two] | $e^{2t}$ | correct | wrong option, wrong under every convention: You put the factor 2 in the power. $e^2 = 7.39$, so that grows more than sevenfold a year. |
| l10-natural-log | quiz[q-two-as-e].options[front] | $2e^t$ | correct | wrong option, wrong under every convention: You moved the 2 to the front. That doubles once, then grows by 2.72 a year. |
| l10-natural-log | quiz[q-two-as-e].options[half] | $e^{t/2}$ | correct | wrong option, wrong under every convention: You halved instead of taking a log. $e^{0.5} = 1.65$, not 2. |
| l11-log-returns | screens[3].prose | log return = ln(P1 / P0) | correct | Tsay, Analysis of Financial Time Series, sec. 1.1 (continuously compounded return) |
| l11-log-returns | screens[1].explain | simple returns multiply: 1.1 x 0.9 = 0.99 | correct | Tsay sec. 1.1 (multi-period simple return) |
| l11-log-returns | screens[5].explain | the log return is always a little below the simple return when the price rises | correct | ln(1 + r) < r for r not 0 (concepts script) |
| l11-log-returns | screens[6] | a total loss has simple return -100% and no finite log return | correct | ln 0 undefined, ln x -> -infinity |
| l11-log-returns | screens[7].prose | ln(1 + r) is about r for small moves only | correct | Taylor: ln(1 + r) = r - r^2/2 + ... |
| l11-log-returns | screens[8].prose | log returns add to ln(P_n / P_0); simple returns compound as a product | correct | Tsay sec. 1.1; telescoping proof on screens[9] |
| l11-log-returns | screens[10].explain | risk systems store log returns because a period total is a sum | correct | Tsay sec. 1.1 (additivity over time is the stated advantage) |
| l11-log-returns | summary.formula.note | back to a simple return: r = e^l - 1 | correct | inverse of l = ln(1 + r) |
| l11-log-returns | screens[1].widget.answer | key -0.01 (unit %) | correct | recomputed: The share ends £1.00 down: −1%. |
| l11-log-returns | screens[1].wrong[cancel] | slip 0 | correct | slip reproduced: You added the two returns. The 10% fall is taken from £110.00, so it removes £11.00, not £10.00. |
| l11-log-returns | screens[1].wrong[double] | slip -0.02 | correct | slip reproduced: That is twice too much. £100.00 to £99.00 is −1%. |
| l11-log-returns | screens[1].wrong[sign] | slip 0.01 | correct | slip reproduced: 1.1 × 0.9 is 0.99, which is below 1, so the share lost money. A return of +1% books the loss as a g… |
| l11-log-returns | screens[2].options[log] (key) | The sum of the $\ln$ values | correct | derivation: The ln sum is always 0.1906, which is $\ln 1.21$. |
| l11-log-returns | screens[2].options[simple] | The sum of the simple returns | correct | wrong option, wrong under every convention: Watch it as you drag: at £110 the simple sum is 0.2000, at £140 it is 0.2643. It moves. |
| l11-log-returns | screens[2].options[both] | Both sums | correct | wrong option, wrong under every convention: Only one of them holds still. Drag to £80 and compare: the simple sum jumps to 0.3125. |
| l11-log-returns | screens[2].options[neither] | Neither sum | correct | wrong option, wrong under every convention: Look again at the ln sum: it reads 0.1906 wherever the middle point sits. |
| l11-log-returns | screens[3].widget.answer | key 0.0488 | correct | recomputed: $\ln \tfrac{52.50}{50.00} = \ln 1.05 = 0.0488$. |
| l11-log-returns | screens[3].wrong[simple] | slip 0.05 | correct | slip reproduced: That is the simple return, 5%. The log return is $\ln 1.05$, a little smaller. |
| l11-log-returns | screens[3].wrong[diff] | slip 2.5 | correct | slip reproduced: You found the change in pounds. A return compares the prices by dividing. |
| l11-log-returns | screens[3].wrong[lnp] | slip 3.9608 | correct | slip reproduced: You took ln of the new price alone. Divide by the old price first. |
| l11-log-returns | screens[4].widget.answer | key 0.038 | correct | recomputed: All the middle closes cancel: $\ln\tfrac{83.10}{80.00} = 0.0380$. |
| l11-log-returns | screens[4].wrong[simple] | slip 0.03875 | correct | slip reproduced: That is the simple return over the four days, 3.875%. The sum of log returns is $\ln 1.03875$. |
| l11-log-returns | screens[4].wrong[price] | slip 3.1 | correct | slip reproduced: That is the change in pounds. Log returns compare prices by ratio. |
| l11-log-returns | screens[5].widget.answer | key 0.08329 (unit %) | correct | recomputed: $e^{0.08} - 1 = 0.0833$, so 8.33%. |
| l11-log-returns | screens[5].wrong[same] | slip 0.08 | correct | slip reproduced: You read the log return as the percentage. $e^{0.08} = 1.0833$, so the share rose 8.33%. |
| l11-log-returns | screens[5].wrong[ln] | slip 0.07696 | correct | slip reproduced: You took ln of 1.08. To go back from a log return, use $e$. |
| l11-log-returns | screens[6].options[none] (key) | It has no finite value | correct | derivation: $\ln 0$ does not exist: the log return falls without limit. |
| l11-log-returns | screens[6].options[minus-one] | $-1$ | correct | wrong option, wrong under every convention: You used the simple return, $-100\%$. The log return is $\ln \tfrac{0}{20} = \ln 0$, and ln is not … |
| l11-log-returns | screens[6].options[zero] | $0$ | correct | wrong option, wrong under every convention: A log return of 0 means the price did not change. Here it went to nothing. |
| l11-log-returns | screens[6].options[ln20] | $-\ln 20 = -3.00$ | correct | wrong option, wrong under every convention: You found $\ln \tfrac{1}{20}$, a fall to £1.00. The ratio here is 0, not $\tfrac{1}{20}$. |
| l11-log-returns | screens[7].options[right] (key) | $0.4055$ | correct | derivation: $\ln 1.5 = 0.4055$, well below 0.50. |
| l11-log-returns | screens[7].options[approx] | $0.50$ | correct | wrong option, wrong under every convention: You used the small-move shortcut $\ln(1 + r) \approx r$. At $r = 0.5$ the curve is well below the d… |
| l11-log-returns | screens[7].options[ln2] | $0.6931$ | correct | wrong option, wrong under every convention: That is $\ln 2$, the log return of a 100% rise. A 50% rise multiplies by 1.5. |
| l11-log-returns | screens[7].options[ten] | $0.1761$ | correct | wrong option, wrong under every convention: That is the base-10 log of 1.5. Log returns use ln. |
| l11-log-returns | screens[8].options[right] (key) | $e^{-0.03} = 0.9704$ | correct | derivation: The ratio is $e^{-0.03} = 0.9704$, a fall of 2.96%. |
| l11-log-returns | screens[8].options[simple] | $1 - 0.03 = 0.97$ exactly | correct | wrong option, wrong under every convention: You treated the log return as a simple return. Turn it back with $e$. |
| l11-log-returns | screens[8].options[ln] | $\ln 0.97$ | correct | wrong option, wrong under every convention: You applied ln again. The sum is already a log; undo it with $e$. |
| l11-log-returns | screens[9].widget.answer | order d1 > d2 > d3 > d4 | correct | each line follows from the one before; The product law turns the sum into one log, and the middle price cancels. |
| l11-log-returns | screens[10].widget.answer | key 1024802.59 | correct | recomputed: $1000000e^{0.0245} = 1024802.59$. |
| l11-log-returns | screens[10].wrong[simple] | slip 1024500 | correct | slip reproduced: You used 0.0245 as a simple return. It is a log return, so the ratio is $e^{0.0245}$, which is £302… |
| l11-log-returns | quiz[q-small-fall].widget.answer | key -0.0513 | correct | recomputed: $\ln\tfrac{38}{40} = \ln 0.95 = -0.0513$. |
| l11-log-returns | quiz[q-small-fall].wrong[simple] | slip -0.05 | correct | slip reproduced: That is the simple return, −5%. The log return of a fall is a little more negative. |
| l11-log-returns | quiz[q-small-fall].wrong[pounds] | slip -2 | correct | slip reproduced: That is the change in pounds. Divide the prices instead. |
| l11-log-returns | quiz[q-small-fall].wrong[sign] | slip 0.0513 | correct | slip reproduced: The price falls, so the ratio 0.95 is below 1 and its log is negative. 0.0513 books the fall as a g… |
| l11-log-returns | quiz[q-three-days].options[right] (key) | $0.04$ | correct | derivation: $0.02 - 0.01 + 0.03 = 0.04$. |
| l11-log-returns | quiz[q-three-days].options[compound] | $0.0401$ | correct | wrong option, wrong under every convention: You multiplied $1.02 \times 0.99 \times 1.03$. That is how simple returns combine; log returns just… |
| l11-log-returns | quiz[q-three-days].options[mean] | $0.0133$ | correct | wrong option, wrong under every convention: You averaged them. The total over three days is the sum. |
| l11-log-returns | quiz[q-three-days].options[product] | $-0.000006$ | correct | wrong option, wrong under every convention: You multiplied the returns themselves. Log returns add. |
| l11-log-returns | quiz[q-up-down-twenty].widget.answer | key -0.0408 | correct | recomputed: $\ln 1.2 + \ln 0.8 = 0.1823 - 0.2231 = -0.0408$. |
| l11-log-returns | quiz[q-up-down-twenty].wrong[cancel] | slip 0 | correct | slip reproduced: You let $+20\%$ and $-20\%$ cancel. Their log returns are 0.1823 and −0.2231, which do not. |
| l11-log-returns | quiz[q-up-down-twenty].wrong[simple] | slip -0.04 | correct | slip reproduced: That is the simple two-day return, −4%. The log return is $\ln 0.96$. |
| l11-log-returns | quiz[q-up-down-twenty].wrong[sign] | slip 0.0408 | correct | slip reproduced: ln 1.2 + ln 0.8 is 0.1823 − 0.2231, and the loss is the larger. 0.0408 takes the subtraction the wr… |
| l11-log-returns | quiz[q-year-log].widget.answer | key 0.28403 (unit %) | correct | recomputed: $e^{0.25} - 1 = 0.2840$, so 28.40%. |
| l11-log-returns | quiz[q-year-log].wrong[same] | slip 0.25 | correct | slip reproduced: You read the log return as the simple return. For a move this size they differ by more than 3%. |
| l11-log-returns | quiz[q-year-log].wrong[ln] | slip 0.22314 | correct | slip reproduced: You took ln of 1.25. Going back from a log return uses $e$. |
| l12-doubling-time | screens[3].prose | doubling time T solves e^(kT) = 2: T = ln 2 / k | correct | derivation; continuous rate form stated |
| l12-doubling-time | screens[2] | rate in percent x doubling time is about 69.3 for a continuous rate; 72 is a rounded rule for yearly payments | correct | 100 ln 2 = 69.3 |
| l12-doubling-time | screens[4].explain | half-life has the same formula as the doubling time | correct | ln(1/2) = -ln 2 |
| l12-doubling-time | screens[5].prose | paid once a year T = ln 2 / ln(1 + r); rule of 72 estimates it as 72 / rate in percent | correct | rate form (yearly, percent) and approximate status both stated |
| l12-doubling-time | screens[5].explain | rule of 72 almost exact near 8%, a year long at 2%, short at 24%; error crosses zero near 8% | correct | concepts script: zero between 7.5% and 8.5% |
| l12-doubling-time | screens[6].feedback.byKey.zero | exponential decay never reaches zero | correct | e^(-kt) > 0 |
| l12-doubling-time | screens[7].prose | T = ln 2 / k, about 69.3 / rate in %; yearly T = ln 2 / ln(1 + r), which the rule of 72 approximates | correct | as above |
| l12-doubling-time | screens[9].explain | execution desks quote unwind speed this way | imprecise | no source found; execution schedules are quoted as participation rates or horizons (Almgren and Chriss 2000). Finding 3 |
| l12-doubling-time | screens[1].widget.points | target [9.9, 2.0] | correct | recomputed: The money doubles after about 9.9 years. |
| l12-doubling-time | screens[2].options[right] (key) | About 69, whatever the rate | correct | derivation: Rate × time is always 69.3. |
| l12-doubling-time | screens[2].options[72] | About 72, whatever the rate | correct | wrong option, wrong under every convention: Check one: at 4% the time is 17.33 years, and $4 \times 17.33 = 69.3$. The 72 is a rounded rule for… |
| l12-doubling-time | screens[2].options[grows] | A bigger number at higher rates | correct | wrong option, wrong under every convention: Try 2% and 12%: $2 \times 34.66 = 69.3$ and $12 \times 5.776 = 69.3$. The product holds still. |
| l12-doubling-time | screens[2].options[100] | About 100 | correct | wrong option, wrong under every convention: You may be thinking of simple interest, which doubles when rate × years = 100. Compounding gets the… |
| l12-doubling-time | screens[3].widget.answer | key 13.86 | correct | recomputed: $T = \tfrac{\ln 2}{0.05} = 13.86$ years. |
| l12-doubling-time | screens[3].wrong[simple] | slip 20 | correct | slip reproduced: That is how long simple interest takes: 5% of the start, 20 times. Compounding doubles sooner. |
| l12-doubling-time | screens[3].wrong[72] | slip 14.4 | correct | slip reproduced: That is the rule of 72, an estimate for yearly payments. Continuous compounding uses $\ln 2 = 0.693… |
| l12-doubling-time | screens[3].wrong[pct] | slip 0.1386 | correct | slip reproduced: You divided by 5 instead of 0.05. The rate goes in as a decimal. |
| l12-doubling-time | screens[4].widget.answer | key 23.1 | correct | recomputed: $t = \tfrac{\ln 2}{0.03} = 23.10$ years. |
| l12-doubling-time | screens[4].wrong[linear] | slip 16.67 | correct | slip reproduced: You took 3% of the original £1,000.00 off every year. Each year loses 3% of a smaller amount, so ha… |
| l12-doubling-time | screens[4].wrong[72] | slip 24 | correct | slip reproduced: That is $72 \div 3$, the yearly rule of thumb. The continuous answer uses 69.3. |
| l12-doubling-time | screens[5].rows[0][2] | key 35.0 | correct | recomputed: 35.00, 9.01 and 3.22 years. |
| l12-doubling-time | screens[5].rows[1][2] | key 9.01 | correct | recomputed: 35.00, 9.01 and 3.22 years. |
| l12-doubling-time | screens[5].rows[2][2] | key 3.22 | correct | recomputed: 35.00, 9.01 and 3.22 years. |
| l12-doubling-time | screens[6].options[zero] | None of it | correct | wrong option, wrong under every convention: You treated the decay as a straight line: half gone in 5 years, so all gone in 10. Each 5 years rem… |
| l12-doubling-time | screens[6].options[quarter] (key) | A quarter | correct | derivation: Two half-lives leave $\tfrac{1}{4}$. |
| l12-doubling-time | screens[6].options[half] | Still a half | correct | wrong option, wrong under every convention: You read the half-life as a floor. The value keeps shrinking; the next 5 years halve it again. |
| l12-doubling-time | screens[7].options[right] (key) | 19.80 years | correct | derivation: $\tfrac{0.6931}{0.035} = 19.80$ years. |
| l12-doubling-time | screens[7].options[simple] | 28.57 years | correct | wrong option, wrong under every convention: That is $100 \div 3.5$, the simple-interest time. Compounding doubles sooner. |
| l12-doubling-time | screens[7].options[72] | 20.57 years | correct | wrong option, wrong under every convention: That is $72 \div 3.5$, the yearly rule. For continuous growth use 69.3. |
| l12-doubling-time | screens[7].options[pct] | 0.20 years | correct | wrong option, wrong under every convention: You divided by 3.5 rather than 0.035. |
| l12-doubling-time | screens[8].widget.answer | order d1 > d2 > d3 > d4 > d5 | correct | each line follows from the one before; Doubling, cancel, take ln, divide. |
| l12-doubling-time | screens[9].widget.answer | key 4.62 | correct | recomputed: $\tfrac{\ln 2}{0.15} = 4.62$ trading days. |
| l12-doubling-time | screens[9].wrong[linear] | slip 3.33 | correct | slip reproduced: You sold 15% of the original each day. The desk sells at a continuous rate on what is left, so halv… |
| l12-doubling-time | screens[9].wrong[72] | slip 4.8 | correct | slip reproduced: That is $72 \div 15$. For continuous decay use $\ln 2$, which gives 69.3. |
| l12-doubling-time | screens[9].wrong[pct] | slip 0.0462 | correct | slip reproduced: You divided by 15 instead of 0.15. |
| l12-doubling-time | quiz[q-ten-percent].widget.answer | key 6.93 | correct | recomputed: $\tfrac{\ln 2}{0.1} = 6.93$ years. |
| l12-doubling-time | quiz[q-ten-percent].wrong[72] | slip 7.2 | correct | slip reproduced: That is the rule of 72. Continuous growth gives $\tfrac{\ln 2}{0.1} = 6.93$. |
| l12-doubling-time | quiz[q-ten-percent].wrong[simple] | slip 10 | correct | slip reproduced: That is the simple-interest time. Compounding doubles sooner. |
| l12-doubling-time | quiz[q-signal-decay].options[right] (key) | $\tfrac{1}{8}$ | correct | derivation: Three half-lives: $(\tfrac{1}{2})^3 = \tfrac{1}{8}$. |
| l12-doubling-time | quiz[q-signal-decay].options[zero] | $0$ | correct | wrong option, wrong under every convention: You let it fall in a straight line. Each 3 days halves what is left, so it never reaches zero. |
| l12-doubling-time | quiz[q-signal-decay].options[third] | $\tfrac{1}{3}$ | correct | wrong option, wrong under every convention: You divided 3 by 9. Count half-lives instead: 9 days is three of them. |
| l12-doubling-time | quiz[q-signal-decay].options[sixth] | $\tfrac{1}{6}$ | correct | wrong option, wrong under every convention: You put $2 \times 3$ underneath. Three halvings multiply: $(\tfrac{1}{2})^3 = \tfrac{1}{8}$. |
| l12-doubling-time | quiz[q-rate-from-doubling].widget.answer | key 0.05776 (unit %) | correct | recomputed: $k = \tfrac{\ln 2}{12} = 0.0578$, so 5.78%. |
| l12-doubling-time | quiz[q-rate-from-doubling].wrong[72] | slip 0.06 | correct | slip reproduced: That is $72 \div 12$, the yearly rule. Continuous compounding uses $\ln 2$. |
| l12-doubling-time | quiz[q-rate-from-doubling].wrong[simple] | slip 0.08333 | correct | slip reproduced: That is $100 \div 12$, the simple-interest rate. Compounding needs less. |
| l12-doubling-time | quiz[q-one-percent].widget.answer | key 69.66 | correct | recomputed: $\tfrac{\ln 2}{\ln 1.01} = 69.66$ years. |
| l12-doubling-time | quiz[q-one-percent].wrong[72] | slip 72 | correct | slip reproduced: That is the rule's estimate. At 1% it runs more than 2 years long. |
| l12-doubling-time | quiz[q-one-percent].wrong[cont] | slip 69.31 | correct | slip reproduced: That is the continuous answer, $\tfrac{\ln 2}{0.01}$. Paid once a year, divide by $\ln 1.01 = 0.009… |
| l13-log-scale | screens[3].prose | a log scale chart plots ln of the price with gridlines labelled in prices; base 10 draws the same picture, on… | correct | log_10 x = ln x / ln 10 |
| l13-log-scale | screens[7].prose | a rise of h multiplies the price by e^h; P = P0 e^(kt) plots as a straight line of gradient k | correct | ln P = ln P0 + kt |
| l13-log-scale | screens[8] | derivation of ln P = ln P0 + kt | correct | product law |
| l13-log-scale | summary.trap | halfway between 200 and 400 on a log axis is 282.84 | correct | geometric mean |
| l13-log-scale | quiz[q-steeper] | the steeper line (larger gradient) grew by the larger percentage | correct | gradient of ln P is the continuous rate |
| l13-log-scale | screens[1].options[same] (key) | At the same rate | correct | derivation: Both stretches multiply the price by 2.01. |
| l13-log-scale | screens[1].options[late] | Years 15 to 20 | correct | wrong option, wrong under every convention: You read the size of the rise in pounds. £82.30 is a bigger rise than £10.11, but each is a doublin… |
| l13-log-scale | screens[1].options[early] | Years 0 to 5 | correct | wrong option, wrong under every convention: You may have felt the early years were the real growth. Both stretches multiply the price by 2.01. |
| l13-log-scale | screens[2].options[same] (key) | It stays the same height | correct | derivation: Every five-year rise has the same height. |
| l13-log-scale | screens[2].options[grows] | It gets taller later on | correct | wrong option, wrong under every convention: That was true of the ordinary chart. Here the height is ln of the price, and each rise is 0.70 wher… |
| l13-log-scale | screens[2].options[shrinks] | It gets shorter later on | correct | wrong option, wrong under every convention: Look at the rise at year 0 and at year 15: both span the same height. |
| l13-log-scale | screens[3].widget.answer | key 100 | correct | recomputed: M is £100.00: £50.00 doubled once. |
| l13-log-scale | screens[3].wrong[mid] | slip 125 | correct | slip reproduced: You took the midpoint in pounds. On a log scale, halfway up splits the ratio 4 into $2 \times 2$, s… |
| l13-log-scale | screens[4].options[same] (key) | Both rises are the same height | correct | derivation: Both rise by $\ln 1.5 = 0.41$. |
| l13-log-scale | screens[4].options[b] | Share B's rise, £100.00 to £150.00 | correct | wrong option, wrong under every convention: You compared the pound amounts: £50.00 against £10.00. A log scale measures ratios, and both are 1.… |
| l13-log-scale | screens[4].options[a] | Share A's rise, £20.00 to £30.00 | correct | wrong option, wrong under every convention: You may have expected small prices to stretch out. Both multiply by 1.5, so both rise by $\ln 1.5$. |
| l13-log-scale | screens[5].widget.answer | key 141.42 | correct | recomputed: N is $100\sqrt{2} = 141.42$. |
| l13-log-scale | screens[5].wrong[mid] | slip 150 | correct | slip reproduced: You took the midpoint in pounds. Halfway up on a log scale is the ratio $\sqrt{2}$ from each end, s… |
| l13-log-scale | screens[6].widget.points | target [5, 5.7038] | correct | recomputed: £300.00 sits a little above halfway, 58% of the way from £200 to £400. |
| l13-log-scale | screens[6].wrong[halfway] | region {"x": [4, 6], "y": [5.615, 5.675]} | correct | region is clear of the target band; You placed P halfway between £200 and £400, as on a pound axis. Halfway up on a log scale is £282.8… |
| l13-log-scale | screens[7].options[right] (key) | It grew by the same percentage each year | correct | derivation: A straight line on a log scale is steady percentage growth. |
| l13-log-scale | screens[7].options[pounds] | It gained the same number of pounds each year | correct | wrong option, wrong under every convention: That is what a straight line means on an ordinary axis. On a log scale, straight means a steady rat… |
| l13-log-scale | screens[7].options[flat] | Its price hardly changed | correct | wrong option, wrong under every convention: A flat line would mean that. A rising straight line means steady percentage growth. |
| l13-log-scale | screens[8].widget.answer | order d1 > d2 > d3 > d4 | correct | each line follows from the one before; $\ln P = \ln P_0 + kt$: intercept $\ln P_0$, gradient $k$. |
| l13-log-scale | screens[9].widget.answer | key 0.13863 (unit %) | correct | recomputed: $k = \tfrac{\ln 4}{10} = 0.1386$, so 13.86% a year. |
| l13-log-scale | screens[9].wrong[simple] | slip 0.3 | correct | slip reproduced: You spread the 300% gain evenly over 10 years. Growth compounds; the gradient of the log chart is $… |
| l13-log-scale | screens[9].wrong[yearly] | slip 0.1487 | correct | slip reproduced: That is $4^{0.1} - 1$, the rate paid once a year. The gradient of the chart is the continuous rate. |
| l13-log-scale | screens[9].wrong[log10] | slip 0.06021 | correct | slip reproduced: You used the base-10 log. The chart's height is ln, so use $\ln 4$. |
| l13-log-scale | quiz[q-equal-heights].options[right] (key) | 20% | correct | derivation: Equal heights are equal percentage moves: 20%. |
| l13-log-scale | quiz[q-equal-heights].options[more] | More than 20%, since the price was higher | correct | wrong option, wrong under every convention: You treated height as pounds. On a log scale equal heights are equal percentages. |
| l13-log-scale | quiz[q-equal-heights].options[less] | Less than 20% | correct | wrong option, wrong under every convention: Equal heights mean equal ratios, whatever the price level. |
| l13-log-scale | quiz[q-halfway-ten].widget.answer | key 31.62 | correct | recomputed: $10\sqrt{10} = 31.62$. |
| l13-log-scale | quiz[q-halfway-ten].wrong[mid] | slip 55 | correct | slip reproduced: You took the midpoint in pounds. Halfway up on a log scale is the ratio $\sqrt{10} = 3.162$ from £1… |
| l13-log-scale | quiz[q-slope-rate].widget.answer | key 0.34657 (unit %) | correct | recomputed: $\tfrac{\ln 4}{4} = 0.3466$, so 34.66%. |
| l13-log-scale | quiz[q-slope-rate].wrong[simple] | slip 0.75 | correct | slip reproduced: You spread the 300% gain over 4 years. The gradient of a log chart is $\tfrac{\ln 4}{4}$. |
| l13-log-scale | quiz[q-slope-rate].wrong[yearly] | slip 0.41421 | correct | slip reproduced: That is $4^{1/4} - 1$, the rate paid once a year. The gradient gives the continuous rate. |
| l13-log-scale | quiz[q-steeper].options[right] (key) | A grew by a larger percentage | correct | derivation: Steeper on a log scale means a faster percentage rate. |
| l13-log-scale | quiz[q-steeper].options[pounds] | A gained more pounds | correct | wrong option, wrong under every convention: A cheap share can be steeper while gaining fewer pounds. Gradient on a log scale is a growth rate. |
| l13-log-scale | quiz[q-steeper].options[price] | A has the higher price | correct | wrong option, wrong under every convention: Height on the chart gives price, but steepness gives growth. A low line can be the steeper one. |
| review-3 | items[r-continuous-eight].widget.answer | key 37.92 | correct | recomputed: A holds $6000e^{0.28} = 7938.78$ and B $6000 \times 1.035^8 = 7900.85$: about £37.92 more. |
| review-3 | items[r-continuous-eight].wrong[cont] | slip 7938.78 | correct | slip reproduced: That is account A's value. Subtract account B's, $6000 \times 1.035^8 = 7900.85$. |
| review-3 | items[r-continuous-eight].wrong[simple] | slip 258.78 | correct | slip reproduced: You took account B as simple interest, £7,680.00. B compounds once a year: $6000 \times 1.035^8$. |
| review-3 | items[r-solve-three-x].widget.answer | key 1.2296 | correct | recomputed: $3x = \ln 40 = 3.6889$, so $x = 1.2296$. |
| review-3 | items[r-solve-three-x].wrong[inside] | slip 2.5903 | correct | slip reproduced: You divided 40 by 3 before taking ln. The 3 multiplies $x$ in the power, so divide after taking ln. |
| review-3 | items[r-solve-three-x].wrong[no-third] | slip 3.6889 | correct | slip reproduced: That is $3x$. Divide by 3 to find $x$. |
| review-3 | items[r-log-path].widget.answer | key 0.2231 | correct | recomputed: The middle closes cancel: $\ln\tfrac{80}{64} = 0.2231$. |
| review-3 | items[r-log-path].wrong[simple] | slip 0.25 | correct | slip reproduced: That is the simple return over the three days, 25%. The log return is $\ln 1.25$. |
| review-3 | items[r-log-path].wrong[pounds] | slip 16 | correct | slip reproduced: That is the change in pounds. Log returns compare prices by ratio. |
| review-3 | items[r-signal-half-life].widget.answer | key 3.47 | correct | recomputed: $\tfrac{\ln 2}{0.2} = 3.47$ days. |
| review-3 | items[r-signal-half-life].wrong[linear] | slip 2.5 | correct | slip reproduced: You let it lose 0.2 of its starting power each day. It decays at a continuous rate on what is left,… |
| review-3 | items[r-signal-half-life].wrong[72] | slip 3.6 | correct | slip reproduced: That is $72 \div 20$. For continuous decay use $\ln 2 = 0.693$. |
| review-3 | items[r-log-midpoint].widget.answer | key 40 | correct | recomputed: £40.00: a quarter of the ratio 16 is $16^{1/4} = 2$. |
| review-3 | items[r-log-midpoint].wrong[mid] | slip 95 | correct | slip reproduced: You went a quarter of the way in pounds: $20 + \tfrac{1}{4} \times 300 = 95$. On a log scale a quar… |
| review-3 | items[r-quote-compare].options[x] (key) | Bank X | correct | derivation: X multiplies by $e^{0.05} = 1.05127$, Y by 1.05100. |
| review-3 | items[r-quote-compare].options[y] | Bank Y | correct | wrong option, wrong under every convention: You let the higher headline rate win. $e^{0.05} = 1.05127$, a little above Y's 1.051. |
| review-3 | items[r-quote-compare].options[same] | They pay the same | correct | wrong option, wrong under every convention: Work out both factors to five places: 1.05127 and 1.05100. |
| review-3 | items[r-crash-log].widget.answer | key -0.5108 | correct | recomputed: $\ln 0.6 = -0.5108$. |
| review-3 | items[r-crash-log].wrong[approx] | slip -0.4 | correct | slip reproduced: You used $\ln(1 + r) \approx r$. For a 40% fall it is far off: $\ln 0.6 = -0.51$. |
| review-3 | items[r-crash-log].wrong[wrong-ratio] | slip -0.9163 | correct | slip reproduced: You took ln of 0.4, the part lost. The price ratio is what is left, 0.6. |
| review-3 | items[r-crash-log].wrong[sign] | slip 0.5108 | correct | slip reproduced: The ratio 0.6 is below 1, so its log is negative. 0.5108 books the fall as a gain. |
| review-3 | items[r-fund-rate].widget.answer | key 0.08245 (unit %) | correct | recomputed: $k = \tfrac{1}{6}\ln\tfrac{410000}{250000} = 0.0824$, so 8.24%. |
| review-3 | items[r-fund-rate].wrong[simple] | slip 0.10667 | correct | slip reproduced: You split the 64% gain evenly over 6 years. Compounding needs a lower rate. |
| review-3 | items[r-fund-rate].wrong[yearly] | slip 0.08594 | correct | slip reproduced: That is $1.64^{1/6} - 1$, the rate paid once a year. The continuous rate is $\tfrac{\ln 1.64}{6}$. |
| review-3 | items[r-steeper-share].options[a] (key) | A's line | correct | derivation: A rose $\ln 4 = 1.39$, B rose $\ln 3 = 1.10$. |
| review-3 | items[r-steeper-share].options[b] | B's line | correct | wrong option, wrong under every convention: You compared pounds: B gained £200.00 and A only £15.00. The log scale compares ratios, 4 against 3. |
| review-3 | items[r-steeper-share].options[same] | They are equally steep | correct | wrong option, wrong under every convention: The ratios differ: A multiplied by 4 and B by 3. |
| homework-3 | items[h-annual-vol].prose | independent daily log returns of sd 1.2%: yearly sd = 0.012 sqrt(252); variances of independent terms add; ab… | correct | Hull ch. 15 (volatility scales with sqrt of time); Monte Carlo in concepts script, 40,000 years, normal and t5 |
| homework-3 | items[h-annual-vol].explain | this works because log returns add; simple returns compound and do not | correct | Monte Carlo in concepts script |
| homework-3 | items[h-unwind-rate].explain | the desk sells 23.10% of what it still holds per day, continuously | imprecise | k = 0.2310 is an instantaneous rate; over one day it sells 1 - e^(-0.2310) = 20.6%. Finding 4 |
| homework-3 | items[h-rule-of-72] | T = ln 2 / ln(1 + r), about 0.693 / r for small r; 72 replaces 69.3 because ln(1 + r) < r at typical rates | correct | derivation |
| homework-3 | items[h-two-bonds].prose | traders compare yields on a continuous basis | imprecise | like-for-like compounding is what is compared; continuous is the model convention (Hull ch. 4), not the market quote. Finding 3 |
| homework-3 | items[h-long-monthly-pnl].model | six log returns sum to 0.13294; simple 14.22%; sum of simple returns 16%; doubling 31.28 months; 26.59% conti… | correct | concepts script |
| homework-3 | items[h-bond-yield].widget.answer | key 810.58 | correct | recomputed: $1000e^{-0.042 \times 5} = 1000e^{-0.21} = 810.58$. |
| homework-3 | items[h-bond-yield].wrong[yearly] | slip 814.07 | correct | slip reproduced: That is $\tfrac{1000}{1.042^5}$, a yield paid once a year. The quote is continuous: divide by $e^{0… |
| homework-3 | items[h-bond-yield].wrong[simple] | slip 826.45 | correct | slip reproduced: You discounted 21% as simple interest, $\tfrac{1000}{1.21}$. Continuous discounting divides by $e^{… |
| homework-3 | items[h-bond-yield].wrong[no-five] | slip 958.87 | correct | slip reproduced: You discounted one year only. Five years make the power $0.042 \times 5 = 0.21$. |
| homework-3 | items[h-eight-days].widget.answer | key 46.14 | correct | recomputed: The log returns add to 0.025, and $45e^{0.025} = 46.14$. |
| homework-3 | items[h-eight-days].wrong[simple] | slip 46.125 | correct | slip reproduced: You treated the total 0.025 as a simple return. It is a log return, so the ratio is $e^{0.025} = 1.… |
| homework-3 | items[h-eight-days].wrong[mean] | slip 45.14 | correct | slip reproduced: You averaged the log returns. Over eight days they add, so use the total, 0.025. |
| homework-3 | items[h-annual-vol].widget.answer | key 0.19049 (unit %) | correct | recomputed: $0.012 \times \sqrt{252} = 0.1905$, so 19.05%. |
| homework-3 | items[h-annual-vol].wrong[times] | slip 3.024 | correct | slip reproduced: You multiplied the standard deviation by 252. Variances add, so the variance is $252 \times 0.012^2… |
| homework-3 | items[h-annual-vol].wrong[compound] | slip 19.2064 | correct | slip reproduced: You compounded the volatility like a return. A standard deviation is not a growth rate. |
| homework-3 | items[h-annual-vol].wrong[365] | slip 0.22926 | correct | slip reproduced: You used calendar days. Markets trade on about 252 days a year. |
| homework-3 | items[h-unwind-rate].widget.answer | key 0.231 | correct | recomputed: $k = \tfrac{\ln 2}{3} = 0.2310$ per day. |
| homework-3 | items[h-unwind-rate].wrong[linear] | slip 0.1667 | correct | slip reproduced: You split the half evenly over 3 days. The desk sells a share of what is left, so it needs a higher… |
| homework-3 | items[h-unwind-rate].wrong[72] | slip 0.24 | correct | slip reproduced: That is $72 \div 3$ as a decimal. Continuous decay uses $\ln 2 = 0.693$. |
| homework-3 | items[h-rule-of-72].widget.answer | order a > b > c > d > e | correct | each line follows from the one before; Exact formula first, then the small-$r$ shortcut, then the calibration to 72. |
| homework-3 | items[h-exact-time].widget.answer | key \frac{\ln 4}{0.08} | correct | derivation: $t = \dfrac{\ln 4}{0.08} = 12.5\ln 4 \approx 17.33$ years. |
| homework-3 | items[h-exact-time].wrong[no-divide] | slip \ln 4 | correct | not equivalent to the key; That is $0.08t$. Divide by 0.08 to find $t$. |
| homework-3 | items[h-exact-time].wrong[ln-thousand] | slip \frac{\ln 1000}{0.08} | misleading | ln 1000 / 0.08 comes from dropping the 250, not from taking ln first: ln 250 + 0.08t = ln 1000 gives the key. Finding 2 |
| homework-3 | items[h-exact-time].wrong[pct] | slip \frac{\ln 4}{8} | correct | not equivalent to the key; You used 8 for 8%. The rate goes in as a decimal: divide by 0.08. |
| homework-3 | items[h-crash-month].widget.answer | key -0.0943 | correct | recomputed: $\ln 0.7 + \ln 1.3 = -0.3567 + 0.2624 = -0.0943$. |
| homework-3 | items[h-crash-month].wrong[cancel] | slip 0 | correct | slip reproduced: You used the small-move shortcut on 30% moves. $\ln 0.7 = -0.357$ and $\ln 1.3 = 0.262$ do not canc… |
| homework-3 | items[h-crash-month].wrong[simple] | slip -0.09 | correct | slip reproduced: That is the simple two-month return, $0.7 \times 1.3 - 1 = -0.09$. The log return is $\ln 0.91$. |
| homework-3 | items[h-crash-month].wrong[sign] | slip 0.0943 | correct | slip reproduced: ln 0.7 + ln 1.3 is −0.3567 + 0.2624, and the loss is the larger. A positive 0.0943 would say the sh… |
| homework-3 | items[h-log-read].widget.answer | key 199.53 | correct | recomputed: $100 \times 10^{0.3} = 199.53$. |
| homework-3 | items[h-log-read].wrong[linear] | slip 370 | correct | slip reproduced: You went 30% of the way in pounds, $100 + 0.3 \times 900$. On a log scale you go 30% of the way in … |
| homework-3 | items[h-log-read].wrong[thirty] | slip 130 | correct | slip reproduced: You added 30% to £100.00. The step to £1,000 multiplies by 10; P multiplies by $10^{0.3}$. |
| homework-3 | items[h-two-bonds].widget.answer | key 5.1 | correct | recomputed: A: $\tfrac{1}{3}\ln\tfrac{100}{88} = 0.04261$. B: $\ln 1.043 = 0.04210$. The gap is 5.1 basis point… |
| homework-3 | items[h-two-bonds].wrong[yearly] | slip 5.32 | correct | slip reproduced: You compared yearly-paid yields, 4.353% against 4.30%, a gap of 5.3 basis points. The question asks… |
| homework-3 | items[h-two-bonds].wrong[raw] | slip -3.9 | correct | slip reproduced: You compared A's continuous yield with B's quoted 4.30% without converting. Convert B: $\ln 1.043 =… |
| problems-3 | items[p-monthly-deposit].parts[2].question | growth at continuous rate r for t years has log return rt | correct | ln(e^(rt)) = rt |
| problems-3 | items[p-savings-doubling].parts[0].widget.answer | key 2400e^{0.055t} | correct | derivation: Continuous compounding at rate $r$ multiplies by $e^{rt}$: $A = 2400e^{0.055t}$. |
| problems-3 | items[p-savings-doubling].parts[0].wrong[percent] | slip 2400e^{5.5t} | correct | not equivalent to the key; The rate goes in as a decimal: 5.5% is 0.055, not 5.5. |
| problems-3 | items[p-savings-doubling].parts[0].wrong[yearly] | slip 2400\cdot1.055^{t} | correct | not equivalent to the key; $1.055^t$ pays the 5.5% once a year. Paid continuously, each year multiplies by $e^{0.055}$. |
| problems-3 | items[p-savings-doubling].parts[0].wrong[factor] | slip 2400e^{1.055t} | correct | not equivalent to the key; $e^{1.055t}$ uses the yearly factor as the rate. The rate is $r = 0.055$. |
| problems-3 | items[p-savings-doubling].parts[1].widget.answer | key 12.6027 | correct | recomputed: $e^{0.055T} = 2$ gives $0.055T = \ln 2$, so $T = \tfrac{0.6931}{0.055} \approx 12.60$ years. |
| problems-3 | items[p-savings-doubling].parts[1].wrong[rule-72] | slip 13.09 | correct | slip reproduced: 13.09 is the rule of 72, made for interest paid once a year. For continuous growth, $T = \tfrac{\ln… |
| problems-3 | items[p-savings-doubling].parts[1].wrong[yearly] | slip 12.95 | correct | slip reproduced: $\tfrac{\ln 2}{\ln 1.055}$ is the doubling time for 5.5% paid once a year. Paid continuously, $T = … |
| problems-3 | items[p-savings-doubling].parts[1].wrong[percent] | slip 0.13 | correct | slip reproduced: You divided by 5.5. The rate is 0.055 as a decimal. |
| problems-3 | items[p-savings-doubling].parts[1].wrong[factor] | slip 36.36 | correct | slip reproduced: You divided 2 by the rate. Take ln first: $0.055T = \ln 2$. |
| problems-3 | items[p-savings-doubling].parts[2].widget.answer | key 37.808 | correct | recomputed: $19{,}200 \div 2400 = 8 = 2^3$, three doublings: $3 \times 12.60 = 37.80$ years. |
| problems-3 | items[p-savings-doubling].parts[2].wrong[eight-times] | slip 100.82 | correct | slip reproduced: You multiplied the doubling time by 8. A factor of 8 is three doublings, $2^3$, so $3 \times 12.60$. |
| problems-3 | items[p-savings-doubling].parts[2].wrong[four] | slip 50.41 | correct | slip reproduced: Four doublings would give $2400 \times 16 = 38{,}400$ pounds. £19,200 is three doublings. |
| problems-3 | items[p-savings-doubling].parts[2].wrong[two] | slip 25.21 | correct | slip reproduced: Two doublings reach only £9,600. One more reaches £19,200. |
| problems-3 | items[p-savings-doubling].parts[3].widget.answer | key 6787.48 | correct | recomputed: 18.90 years is 1.5 doubling times, so the balance is $2400 \times 2^{1.5} \approx 6788$ pounds. |
| problems-3 | items[p-savings-doubling].parts[3].wrong[halfway-pounds] | slip 10800 | correct | slip reproduced: £10,800 is halfway between £2,400 and £19,200. The balance grows faster later, so halfway in time i… |
| problems-3 | items[p-savings-doubling].parts[3].wrong[midpoint] | slip 7200 | correct | slip reproduced: £7,200 is halfway between £4,800 and £9,600. Half a doubling multiplies by $\sqrt{2} \approx 1.414$… |
| problems-3 | items[p-savings-doubling].parts[3].wrong[years] | slip 2606.4 | correct | slip reproduced: That uses 1.5 years. Halfway is 18.90 years, which is 1.5 doubling times. |
| problems-3 | items[p-weekly-target].parts[0].widget.answer | key 0.043 | correct | recomputed: Log returns add: $0.030 - 0.012 + 0.045 - 0.020 = 0.043$. |
| problems-3 | items[p-weekly-target].parts[0].wrong[signs] | slip 0.107 | correct | slip reproduced: You added the falls as rises. The $-0.012$ and $-0.020$ take away. |
| problems-3 | items[p-weekly-target].parts[0].wrong[averaged] | slip 0.01075 | correct | slip reproduced: That is the average daily log return. The week's log return is the sum. |
| problems-3 | items[p-weekly-target].parts[1].widget.answer | key 41.7575 | correct | recomputed: $P = 40e^{0.043} \approx 40 \times 1.04394 = 41.76$ pounds. |
| problems-3 | items[p-weekly-target].parts[1].wrong[one-plus] | slip 41.72 | correct | slip reproduced: That treats 0.043 as a simple return, $40 \times 1.043$. A log return is undone with $e$: $40e^{0.0… |
| problems-3 | items[p-weekly-target].parts[1].wrong[added] | slip 40.04 | correct | slip reproduced: You added 0.043 pounds. A log return measures a ratio: $\tfrac{P}{40} = e^{0.043}$. |
| problems-3 | items[p-weekly-target].parts[1].wrong[carried] | slip 44.52 | correct | slip reproduced: That uses 0.107, with the falls added as rises. With a log return of 0.043, the close is $40e^{0.04… |
| problems-3 | items[p-weekly-target].parts[2].widget.answer | key 0.074724 | correct | recomputed: $\ln \tfrac{45}{41.76} \approx 0.0747$. |
| problems-3 | items[p-weekly-target].parts[2].wrong[simple] | slip 0.0776 | correct | slip reproduced: 0.0776 is the simple return, $\tfrac{45 - 41.76}{41.76}$. The log return is $\ln \tfrac{45}{41.76}$… |
| problems-3 | items[p-weekly-target].parts[2].wrong[from-monday] | slip 0.1178 | correct | slip reproduced: 0.1178 is the log return from Monday's £40.00. The week has already supplied 0.043 of it. |
| problems-3 | items[p-weekly-target].parts[2].wrong[inverted] | slip -0.0747 | correct | slip reproduced: That is $\ln \tfrac{41.76}{45}$, a fall. The price must rise, so the log return is positive. |
| problems-3 | items[p-weekly-target].parts[2].wrong[difference] | slip 3.24 | correct | slip reproduced: £3.24 is the gap in pounds. A log return is ln of the ratio. |
| problems-3 | items[p-weekly-target].parts[3].widget.answer | key 0.0249 | correct | recomputed: Log returns add, so each week needs $0.0747 \div 3 = 0.0249$. |
| problems-3 | items[p-weekly-target].parts[3].wrong[cube-root] | slip 0.4212 | correct | slip reproduced: You took the cube root of 0.0747. Log returns add, so divide by 3. |
| problems-3 | items[p-weekly-target].parts[3].wrong[times-three] | slip 0.2241 | correct | slip reproduced: You multiplied by 3. The three weeks share the 0.0747 between them. |
| problems-3 | items[p-weekly-target].parts[3].wrong[carried] | slip 0.0259 | correct | slip reproduced: That shares out 0.0776, the simple return. The log return needed is 0.0747. |
| problems-3 | items[p-weekly-target].parts[4].widget.answer | key 0.025213 (unit %) | correct | recomputed: $e^{0.0249} - 1 \approx 0.0252$, a simple return of 2.52% a week. |
| problems-3 | items[p-weekly-target].parts[4].wrong[log-as-simple] | slip 0.0249 | correct | slip reproduced: 2.49% is the log return written as a percentage. The simple return is $e^{0.0249} - 1$, a little la… |
| problems-3 | items[p-weekly-target].parts[4].wrong[simple-split] | slip 0.0259 | correct | slip reproduced: That splits the simple return of 7.76% into three. Simple returns compound, so each week needs less… |
| problems-3 | items[p-weekly-target].parts[4].wrong[decimal] | slip 0.000252 | correct | slip reproduced: In this box, 0.0252 reads as 0.0252%. Type the percentage, 2.52. |
| problems-3 | items[p-weekly-target].parts[4].wrong[e-power] | slip 1.0252 | correct | slip reproduced: 102.52% is the whole weekly factor $e^{0.0249}$. The simple return is the part above 1: 2.52%. |
| problems-3 | items[p-log-chart-line].parts[0].widget.answer | key 0.274653 (unit %) | correct | recomputed: $k = \tfrac{\ln(135/15)}{8} = \tfrac{\ln 9}{8} \approx 0.2747$, so 27.47% a year. |
| problems-3 | items[p-log-chart-line].parts[0].wrong[simple-total] | slip 1.0 | correct | slip reproduced: 100% a year shares the rise in pounds over 8 years. The chart's height is $\ln P$, so use $\ln 9$. |
| problems-3 | items[p-log-chart-line].parts[0].wrong[ratio-over-years] | slip 1.125 | correct | slip reproduced: You divided the factor 9 by 8 years. Take ln of the factor first: $\tfrac{\ln 9}{8}$. |
| problems-3 | items[p-log-chart-line].parts[0].wrong[yearly-factor] | slip 0.3161 | correct | slip reproduced: 31.61% is the rate paid once a year, $9^{1/8} - 1$. The gradient of $\ln P$ is the continuous rate,… |
| problems-3 | items[p-log-chart-line].parts[0].wrong[log10] | slip 0.1193 | correct | slip reproduced: That uses base-10 logs. The continuous rate comes from ln: $\tfrac{\ln 9}{8}$. |
| problems-3 | items[p-log-chart-line].parts[0].wrong[decimal] | slip 0.0027465 | correct | slip reproduced: In this box, 0.2747 reads as 0.2747%. Type the percentage, 27.47. |
| problems-3 | items[p-log-chart-line].parts[1].widget.answer | key 2.52372 | correct | recomputed: $T = \tfrac{\ln 2}{k} \approx \tfrac{0.6931}{0.2747} \approx 2.52$ years. |
| problems-3 | items[p-log-chart-line].parts[1].wrong[rule-72] | slip 2.62 | correct | slip reproduced: 2.62 is the rule of 72. For a continuous rate, $T = \tfrac{\ln 2}{k}$. |
| problems-3 | items[p-log-chart-line].parts[1].wrong[inverse] | slip 3.64 | correct | slip reproduced: $\tfrac{1}{k}$ leaves out the $\ln 2$. Doubling needs $kT = \ln 2$. |
| problems-3 | items[p-log-chart-line].parts[1].wrong[percent] | slip 0.03 | correct | slip reproduced: You divided by 27.47. Use the rate as a decimal, 0.2747. |
| problems-3 | items[p-log-chart-line].parts[1].wrong[tripling] | slip 4 | correct | slip reproduced: 4 years is the tripling time, $\tfrac{\ln 3}{k}$. Doubling needs $\ln 2$. |
| problems-3 | items[p-log-chart-line].parts[2].widget.answer | key 45 | correct | recomputed: 4 years is $\tfrac{4}{2.52} \approx 1.59$ doublings, and $15 \times 2^{1.59} \approx 45$ pounds. |
| problems-3 | items[p-log-chart-line].parts[2].wrong[pounds-midpoint] | slip 75 | correct | slip reproduced: £75 is halfway between £15 and £135 in pounds. The line is straight in $\ln P$, so the price grows … |
| problems-3 | items[p-log-chart-line].parts[2].wrong[whole-doublings] | slip 30 | correct | slip reproduced: £30 counts only one whole doubling. 4 years hold about 1.59 doublings: $15 \times 2^{1.59}$. |
| problems-3 | items[p-log-chart-line].parts[2].wrong[rounded-up] | slip 60 | correct | slip reproduced: £60 rounds 1.59 doublings up to 2. Keep the fraction: $15 \times 2^{1.59} \approx 45$. |
| problems-3 | items[p-log-chart-line].parts[3].widget.answer | key 6 | correct | recomputed: $\tfrac{\ln(45/15)}{\ln(135/15)} = \tfrac{\ln 3}{\ln 9} = \tfrac{1}{2}$, so it sits 6 cm up. |
| problems-3 | items[p-log-chart-line].parts[3].wrong[pounds] | slip 3 | correct | slip reproduced: 3 cm places £45 a quarter of the way up in pounds. On a log chart, height measures ratios: 15 to 45… |
| problems-3 | items[p-log-chart-line].parts[3].wrong[ratio] | slip 4 | correct | slip reproduced: You took 45 as a share of 135. Heights measure ratios from the £15 level: $\ln 3$ out of $\ln 9$. |
| problems-3 | items[p-monthly-deposit].parts[0].widget.answer | key 1.04907 | correct | recomputed: $1.004^{12} \approx 1.0491$. |
| problems-3 | items[p-monthly-deposit].parts[0].wrong[once] | slip 1.048 | correct | slip reproduced: 1.048 pays the 4.8% once. Paid monthly, the interest earns interest, so the factor is $1.004^{12}$. |
| problems-3 | items[p-monthly-deposit].parts[0].wrong[continuous] | slip 1.0492 | correct | slip reproduced: That is $e^{0.048}$, for continuous compounding. Monthly payments give $1.004^{12}$, a little less. |
| problems-3 | items[p-monthly-deposit].parts[0].wrong[whole-rate] | slip 1.7552 | correct | slip reproduced: That adds the whole 4.8% every month. Each month adds $\tfrac{4.8\%}{12} = 0.4\%$. |
| problems-3 | items[p-monthly-deposit].parts[1].widget.answer | key 0.047904 (unit %) | correct | recomputed: $\ln 1.0491 \approx 0.0479$, a continuous rate of 4.79%. |
| problems-3 | items[p-monthly-deposit].parts[1].wrong[quoted] | slip 0.048 | correct | slip reproduced: 4.80% continuous would give $e^{0.048} \approx 1.0492$, a little too much. Solve $e^{r} = 1.0491$: … |
| problems-3 | items[p-monthly-deposit].parts[1].wrong[factor-rate] | slip 0.0491 | correct | slip reproduced: 4.91% is the yearly rate paid once, $1.0491 - 1$. The continuous rate is $\ln 1.0491$, a little low… |
| problems-3 | items[p-monthly-deposit].parts[1].wrong[decimal] | slip 0.000479 | correct | slip reproduced: In this box, 0.0479 reads as 0.0479%. Type the percentage, 4.79. |
| problems-3 | items[p-monthly-deposit].parts[1].wrong[log10] | slip 0.0208 | correct | slip reproduced: That uses the base-10 log. Continuous rates come from ln. |
| problems-3 | items[p-monthly-deposit].parts[2].widget.answer | key 0.239521 | correct | recomputed: Each year's log return is 0.0479, and log returns add: $5 \times 0.0479 = 0.2395$. |
| problems-3 | items[p-monthly-deposit].parts[2].wrong[quoted] | slip 0.24 | correct | slip reproduced: That uses 4.8%, the rate paid monthly. The log return per year is 4.79%. |
| problems-3 | items[p-monthly-deposit].parts[2].wrong[simple] | slip 0.2707 | correct | slip reproduced: 0.2708 is the 5-year simple return, $1.0491^5 - 1$. The log return is the sum of the yearly log ret… |
| problems-3 | items[p-monthly-deposit].parts[2].wrong[one-year] | slip 0.0479 | correct | slip reproduced: 0.0479 is one year's log return. Five years add five of them. |
| problems-3 | items[p-monthly-deposit].parts[3].widget.answer | key 7623.84 | correct | recomputed: $6000e^{0.2395} \approx 7623.68$, so about £7,624. |
| problems-3 | items[p-monthly-deposit].parts[3].wrong[one-plus] | slip 7437 | correct | slip reproduced: That treats 0.2395 as a simple return, $6000 \times 1.2395$. Undo a log return with $e$: $6000e^{0.… |
| problems-3 | items[p-monthly-deposit].parts[3].wrong[quoted] | slip 7627.49 | correct | slip reproduced: That uses 4.8% continuously for 5 years. The account pays monthly, which matches 4.79% continuously. |
| problems-3 | items[p-monthly-deposit].parts[3].wrong[simple-interest] | slip 7440 | correct | slip reproduced: That adds 4.8% of £6,000 each year, with no interest on interest. |
| fluency-l10-natural-log | families[exact-with-ln].widget.answer | solve with e and ln, exactly: key \frac{{\ln {b}}}{{{k}}} | correct | every draw in the whole variable range recomputed (concepts script sweep) |
| fluency-l10-natural-log | families[exact-with-ln].wrong[multiplied-by-k] | {k}\ln {b}: Taking $\ln$ gives ${k}{v} = \ln {b}$: divide by {k}, do not multiply. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l10-natural-log | families[exact-with-ln].wrong[divided-inside] | \ln({b/k:frac}): Take $\ln$ first, then divide: ${k}{v} = \ln {b}$, so the {k} divides $\ln {b}$, not {b}. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l10-natural-log | families[continuous-growth].widget.answer | solve a continuous growth problem: key {round(years, 6)} | correct | every draw in the whole variable range recomputed (concepts script sweep) |
| fluency-l10-natural-log | families[continuous-growth].wrong[logs-too-soon] | {round(early, 6)}: Divide by {p} before taking $\ln$: $e^{{{k}t}} = {q}$. | misleading | value is ln(target)/ln(g) or ln(target)/k: the start amount was dropped. Taking logs first, done correctly, gives the key (l8 screens[4]). Finding 2 |
| fluency-l10-natural-log | families[continuous-growth].wrong[rate-as-whole-number] | {round(whole, 6)}: The rate in the power is ${k}$, not {r}: {r}% is ${k}$. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l10-natural-log | families[ln-from-two-values].widget.answer | use the log laws with ln: key {key} | correct | every draw in the whole variable range recomputed (concepts script sweep) |
| fluency-l10-natural-log | families[ln-from-two-values].wrong[powers-left-behind] | {flat}: The power law brings each power down in front of its log. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l10-natural-log | families[ln-from-two-values].wrong[swapped-the-values] | {swapped}: You swapped the two values: $\ln {f} = {lf:dp4}$ and $\ln {g} = {lg:dp4}$. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l10-natural-log | families[any-base-as-e].widget.answer | write a power of any base with e: key {round(lb, 8)} | correct | every draw in the whole variable range recomputed (concepts script sweep) |
| fluency-l10-natural-log | families[any-base-as-e].wrong[used-log] | {round(common, 8)}: That is $\log {b}$, base 10: the power of $e$ needs $\ln {b}$. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
| fluency-l10-natural-log | families[any-base-as-e].wrong[one-over] | {round(flip, 8)}: That is $\frac{{1}}{{\ln {b}}}$: ${b} = e^{{\ln {b}}}$, so $k = \ln {b}$. | correct | slip value differs from the key by more than both bands in every draw (concepts script sweep) |
