# mock-oa-quant-data: report

Brief: `docs/briefs/mocks.md`, section `## mock-oa-quant-data`. Build script: `docs/briefs/mocks-scripts/oa_quant_data_build.py`. (Written by the orchestrator from the author's hand-back; the author's Write call was refused by the harness.)

## Files
- `app/content/exams/mock-oa-quant-data.json`
- `app/content/data/qd/qd-prices.csv`, `qd-pair.csv`, `qd-signal.csv`
- `docs/briefs/mocks-scripts/oa_quant_data_build.py`

| File | Bytes | SHA-256 prefix |
| --- | --- | --- |
| `qd-prices.csv` | 17,550 | `075ba1d7e21c18f1` |
| `qd-pair.csv` | 15,613 | `31b8bee8e889386e` |
| `qd-signal.csv` | 31,659 | `9a44408ce52afff1` |

Hashes and sizes match the brief; all are under the 256 KB cap.

## Items
13 items in 120 minutes; pass 6 of 10 (paper 1) and 2 of 3 (paper 2), plus the `no-lookup` check.
- Paper 1 difficulties: 2 x2, 3 x5, 4 x2, 5 x1. Kinds: 6 numeric, 1 `parts` (Q6), 1 choice, 2 `multi`.
- Paper 2: three `code` items at difficulty 3, 4 and 5.
- `pace` sums to 2,280 s and 4,500 s. Q7 uses `unit: "%"` with answer 0.142.

## Numbers computed twice (Fractions, in the build script; each pair agreed)
- Q1 3.92; Q3 1.8; Q5 0.3467 (26/75); Q6 5.6 and 1.6; Q7 14.2% (variance 0.02016); Q8 0.3448 (10/29, checked on a 1/290 grid); Q10 500 (checked by a sum over N from 0 to 79).
- Q4: SSE never rose in 2,000 exact fits; adjusted R² fell in 1,259 of them (seed 3501). The brief's 1,285 came from another seed, so the explanation does not quote a count.
- Task 1: 773 rows; closes 258, 257, 258; volatilities 0.17608, 0.25817, 0.35772.
- Task 2: 458 windows; betas 0.8033, 1.3829; full sample 1.0877.
- Task 3: coefficients 0.000254, 0.002297, -0.00159; train R² 0.0836; out-of-sample R² 0.0577.
- The pure-Python second method read the decimal text for all three tasks.

## Pyodide 0.27.7 (numpy 2.0.2, pandas 2.2.3), scratch runner
- All three starters fail every test; all three references pass every test.
- Alternative right solutions pass: task 1 groupby-apply; task 2 polyfit and pandas rolling; task 3 normal equations.
- Every wrong version fails at least one test. Task 1: no repeat removal, return across tickers, `ddof=0`, no sort, blanks as zero. Task 2: keeps the errors, asset-only filter, window minus one. Task 3: unlagged, test-mean baseline, whole-sample fit, split before lagging.
- The three worked examples (tiny files written by `setup`) pass for the references and fail for the starters.
- No expected value differed between pandas 3.0.5 (brief) and 2.2.3.

## Brief corrections (noted in `docs/briefs/mocks.md`)
1. `skills` gained `rq-case`.
2. Task 2's "asset only" wrong version passed all 8 tests; a 9th hidden test (error in `mkt` only) was added.
3. The generator stays in `mocks-scripts/`, since content agents may not edit `app/tools/`.

## Validation and playthrough
- Validator: 0 errors (no warning from this exam).
- `--exam mock-oa-quant-data` green at 1280 and 390 px (`--mobile`): scored 13 of 13, passed. Screenshots of the start card, every item and the results checked at both widths: no overlap, no sideways scroll.

## Freshness, prerequisites, prep.json
- The only hits on this exam's function names and figures are in the exam itself.
- Prerequisites cited (nothing gated): `research-int` l1 to l5, l16 to l19; `numpy-pandas` l7 and l12; `regression` l12; `validation` l6.
- `prep.json`: no change proposed.

## Backlog
4 bullets under `Raised later (exam mock-oa-quant-data):` in `docs/BACKLOG-INBOX.md`.
