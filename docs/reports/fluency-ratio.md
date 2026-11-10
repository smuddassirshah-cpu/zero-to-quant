# Fluency: ratio (docs/briefs/fluency.md, second wave, agent 1, topic 0.1)

Five sets, thirteen families. Money is £, in prompts to two decimal places where the lesson writes it so (l4, l5, l6) and in whole pounds where it does not (l2, l9). Amounts in prompts stay under £1,000, so no thousands comma is needed; percentages are whole or end in a half.

## Lessons chosen

- l2-building-percentages: a percentage of an amount, built from 1%, is the rote core of the topic.
- l4-multipliers: writing and using the multiplier for a rise or fall is one move with fresh numbers.
- l5-rise-or-fall: percentage change over the original value, and a signed daily return, is a fixed recipe with a famous slip (the new base).
- l6-before-the-discount: undoing a change by dividing by its multiplier, VAT included, needs repetition to beat the add-it-back slip.
- l9-sharing: sharing in a ratio by counting parts, from a total, a share or a difference, is a procedure.

Considered and left out: l1 (moving between fractions, decimals and percentages: procedural, left out to keep ten sets; the conversion is the first step of l4 and l5); l3 (one amount as a percentage of another: procedural, left out for ten; its part over whole is the same division as l5's change over original); l7 (equal moves up and down do not cancel: an idea); l8 (compound growth: the powers need a calculator); l10 (scaling: the unit rate is procedural, but simplest form needs a typed ratio $a : b$, and no `form` reads one; raised); l11 (direct or inverse: a judgement); l12 (best buy: a comparison); l13 (currencies: four-decimal rates and a calculator).

| set | family | distinct prompts in 200 | `form` | slips |
| --- | --- | --- | --- | --- |
| fluency-l2-building-percentages | whole-percent | 198 | (numeric, £) | divided-by-p, the-rest |
| | half-percent | 172 | (numeric, £) | divided-by-p, tenths |
| fluency-l4-multipliers | write-multiplier | 103 | (numeric) | opposite, change-only, tenths (under 10%) |
| | apply-multiplier | 199 | (numeric, £) | change-only, opposite, tenths (under 10%) |
| fluency-l5-rise-or-fall | percentage-change | 184 | (numeric, %) | new-base, ratio, pounds |
| | daily-return | 146 | (numeric, %) | sign-flipped, new-base (where it is more than 0.1 points away) |
| fluency-l6-before-the-discount | undo-a-discount | 195 | (numeric, £) | added-back, divided-by-cut |
| | undo-a-rise | 149 | (numeric, £) | took-off, divided-by-rise |
| | vat-inside | 163 | (numeric, £) | vat-of-total, price-before |
| fluency-l9-sharing | share-a-total | 184 | (numeric, £) | one-part, ratio-as-fraction (smaller share), split-equally |
| | from-one-share | 177 | (numeric, £) | added-the-gap, gave-the-total |
| | three-way | 195 | (numeric, £) | one-part, split-equally |
| | from-a-difference | 161 | (numeric, £) | one-part, larger-share, gap-as-one-part |

Notes. Percentage keys use `unit: "%"` with the key as the fraction and `accept` "{p}%", as section 3 asks. Rises in l5 go to 150%, as in the lesson; `over100` is not a field a Fluency numeric takes, and no warning fires without it. The words and signs ("rises", 1, "rise") are drawn together as tuples.

## Checks
1. `docs/reports/fluency-ratio-numbers.py` (Fraction, 200 draws a family, 27,572 checks): rebuilds each prompt as text from the vars (money to the penny) and compares it; works each key again by the lesson's method (1% first, the multiplier, change over original, divide by the multiplier, one part times the parts); checks money keys are whole pence; rebuilds each slip, checks the slips offered are exactly those whose condition holds, and that each lies outside the key's tolerance plus its own and apart from the others. Exit 0. A mutation run (a key shifted by £1) failed as it should.
2. Validator: 0 errors; no warning on these files. `test-fluency.mjs --local-cdn`: 300, 300, 300, 304 and 308 passed, all green.
3. Playthrough `--fluency` of all five sets, desktop and `--mobile`: green. Screenshots of l5 (item, wrong chip, end card, 440 px and desktop) read: no layout fault.
4. Voice scan 35 on the course folder: 0 and 0.
5. I read 20 drawn items of every family as a learner would, and scanned 200 of each for the faults in the brief, a "£-" and float tails: no hits (one hit, $0.055$ for 5.5%, is the true multiplier). Fixed on reading: "one 17th" in a line, a "ratio" slip equal to the key at a 50% fall, and a "ratio as a fraction" slip equal to "split equally" for $1 : 2$.

## Engine limits (inbox)
- No `form` for a ratio in simplest form, so l10 has no set.
- No thousands separator among the formats: `{x:dp2}` writes £1271.00 where the lessons write £1,271.00. Prompts stay under £1,000; a key over £1,000 (apply-multiplier) shows the plain form in `accept` and the working.
