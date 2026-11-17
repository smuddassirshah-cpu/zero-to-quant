# Engine pass 8 part A: hits of the new rules on the 149 problem sets

Generated from `node tools/validate.mjs` at the HEAD this report is filed with (0 errors). A reader triages this list next. Every rule below ships as a warning except `[percent-unit]`, which has 0 hits and is an error. Evidence is the validator's own message.

| rule | level | hits |
|---|---|---|
| `[working-band]` | warning | 2 |
| `[rounding-tie]` | warning | 2 |
| `[table-source]` | warning | 6 |
| `[percent-unit]` | error | 0 |
| `[wide-wrong-tol]` | warning | 10 |
| `[escaped-apostrophe]` | warning | 1 |

## [working-band] (2)

### content/courses/coint/problems-1.json

- `items[2].parts[3]`: explain.text ends at 1104.4, 1104 at the asked places, outside the key 1105 band +-1e-9: a learner who follows the working is marked wrong

### content/courses/stat-learning/problems-1.json

- `items[3].parts[3]`: explain.text ends at 1.44, outside the key 1.476 band +-0.0005: a learner who follows the working is marked wrong

## [rounding-tie] (2)

### content/courses/trig/problems-1.json

- `items[1].parts[3].wrong[2]`: wrong "half" (0.5) is exactly on a rounding tie at 0 decimal places; its band +-0.0005 takes neither rounding (0, 1)
- `items[3].parts[2].wrong[2]`: wrong "ratio-tan" (0.75) is exactly on a rounding tie at 1 decimal place; its band +-0.0005 takes neither rounding (0.7, 0.8)

## [table-source] (6)

### content/courses/arma/problems-3.json

- `items[2].parts[2]`: the part needs a tail area, quantile or table value (P(Z) but neither the stem nor the question gives it or names its source: state the value, or say where to read it (a table to 4 places, software)
- `items[2].parts[3]`: the part needs a tail area, quantile or table value (P(Z) but neither the stem nor the question gives it or names its source: state the value, or say where to read it (a table to 4 places, software)

### content/courses/fin-ml/problems-3.json

- `items[1].parts[1]`: the part needs a tail area, quantile or table value (\Phi^{-1}() but neither the stem nor the question gives it or names its source: state the value, or say where to read it (a table to 4 places, software)
- `items[1].parts[3]`: the part needs a tail area, quantile or table value (\Phi() but neither the stem nor the question gives it or names its source: state the value, or say where to read it (a table to 4 places, software)
- `items[2].parts[3]`: the part needs a tail area, quantile or table value (\Phi() but neither the stem nor the question gives it or names its source: state the value, or say where to read it (a table to 4 places, software)

### content/courses/garch/problems-1.json

- `items[0].parts[1]`: the part needs a tail area, quantile or table value (\Phi() but neither the stem nor the question gives it or names its source: state the value, or say where to read it (a table to 4 places, software)

## [percent-unit] (0)

No hits.

## [wide-wrong-tol] (10)

### content/courses/estimation/problems-3.json

- `items[1].parts[1].wrong[3]`: wrong "decimal" (0.00086667) has a band of +-0.005, wider than its own value: unrelated answers land in it

### content/courses/garch/problems-2.json

- `items[1].parts[0].wrong[3]`: wrong "decimal" (0.00092308) has a band of +-0.005, wider than its own value: unrelated answers land in it
- `items[1].parts[2].wrong[3]`: wrong "decimal" (0.002574) has a band of +-0.005, wider than its own value: unrelated answers land in it
- `items[1].parts[4].wrong[3]`: wrong "decimal" (0.00254031) has a band of +-0.005, wider than its own value: unrelated answers land in it
- `items[2].parts[2].wrong[2]`: wrong "decimal" (0.00001156) has a band of +-0.00005, wider than its own value: unrelated answers land in it

### content/courses/garch/problems-3.json

- `items[0].parts[1].wrong[2]`: wrong "decimal" (0.000049) has a band of +-0.005, wider than its own value: unrelated answers land in it
- `items[3].parts[0].wrong[3]`: wrong "decimal" (0.00433484) has a band of +-0.005, wider than its own value: unrelated answers land in it
- `items[3].parts[2].wrong[3]`: wrong "decimal" (0.00294742) has a band of +-0.005, wider than its own value: unrelated answers land in it

### content/courses/numerics/problems-1.json

- `items[2].parts[1].wrong[1]`: wrong "no-kappa" (0.004657) has a band of +-0.005, wider than its own value: unrelated answers land in it

### content/courses/trig/problems-2.json

- `items[0].parts[1].wrong[0]`: wrong "wrong-way" (0.0393) has a band of +-0.05, wider than its own value: unrelated answers land in it

## [escaped-apostrophe] (1)

### content/courses/elimination/problems-1.json

- `items[1].parts[1].question`: a backslash before an apostrophe ("Monday\'s orde") shows on screen: write the apostrophe alone

