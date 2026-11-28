# nn-train level 4 (Experiments you can trust): second-reader findings

Scope: `app/content/courses/nn-train/` l13-one-seed-one-draw, l14-ablations, l15-training-log, l16-paired-seeds, review-4, homework-4, problems-4; `app/content/data/ai/nt_ops_l4.py` and `nn-train-seeds.json`; at `afabe1db`.
Method, no browser: `docs/reports/nn-train-L4-numbers.py` run through `tools/run-number-scripts.mjs --only nn-train-L4` and directly with `ZQ_NUMBERS_STRICT=1 --verbose` at default threads, and with `--write` in a scratch copy of `app/` (default and single BLAS threads) to compare the rewritten seeds file with the shipped one; every `claim(..., covers=...)` searched for coverage by fiat, all four `literal()` marks read (the script has four, not ten) and ten `covers` claims read against their conditions; every statistic recomputed from `nn-train-seeds.json` with SciPy 1.x and statsmodels (paired and Welch $t$, $p$, intervals, the sign and Wilcoxon tests, correlations, every ablation effect with its own paired $t$, the per-seed interaction, exact noncentral-$t$ power beside the normal formula, $1 - 0.95^k$, Bonferroni cut-offs); `nt_ops_l4.t_cdf` and `t_quantile` probed at extreme quantiles against `scipy.stats.t`; every hand figure in the review, homework and problem set recomputed from its printed inputs; each `wrong[]` value evaluated against the engine's own `numGrade` (node, `js/engine/grade.js`) with the slip worked from the numbers the screen prints; `grade-all.mjs --file <f> --code --local-cdn <pkgs>` on each of the seven files alone; 51 reviewer solutions graded in Pyodide as `mutants` (appendix); per-case times against the page's limits; `voice-scan.py 35` on the course, plus scans for em-dashes, exclamation marks and American spellings; every `wrong[]` id and wrong option checked for a `byKey` line; hint highlight ids checked against the canvas READMEs.
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, gap or teaching issue; note = style or small polish.

Counts: 1 error, 9 warnings, 15 notes. No module error; the number script recomputes everything (no coverage by fiat). Wrong solutions: 51 tried, 5 of them correct alternatives (accepted, as they should be), 3 of the other 46 survive.

The statistics hold up: every paired test, $p$-value, interval, seed count and correction the level states is right to its printed places. The faults are in labelling (the interaction's sign), in what an interval or a power figure is said to cover, and in slips whose `byKey` lines a learner working from the printed numbers cannot reach.

## Module and data (nt_ops_l4.py, nn-train-seeds.json)

- app/content/data/ai/nt_ops_l4.py | `t_quantile` | note | Bisection runs on $[-10^4, 10^4]$ and returns the bound silently when the quantile lies outside it: `t_quantile(0.99999, 1)` gives 9999.99 against SciPy's 31,831. Only $n = 2$ seeds with a very deep Bonferroni level reaches it, but `ml-int` and `ai-papers` will reuse the function. | Widen the bracket by doubling until `t_cdf(hi, df) > q`, or raise `ValueError` when the bound is hit.
- app/content/data/ai/nn-train-seeds.json | whole file | note | A `--write` on this machine reproduces the file to $5.2 \times 10^{-9}$ relative (301 of the 390 final losses differ in the last digits; every curve point is identical), the same at one BLAS thread, so the file is not byte-identical to a rewrite. The script compares at $10^{-6}$, and every figure the lessons state is fixed to 4 places or fewer. | None; recorded for the next reader.

## Number script (nn-train-L4-numbers.py)

CI runner: 1 of 1 passed (20 s). Direct, strict, default threads: 422 of 422 checks, 0 uncovered, 4 literals (0.005 the lowered rate, 0.1 the wall seconds, $10^{-7}$ a tolerance, 500 a quiz step count: each a stated setting). No `claim(True, ...)`: every covered number comes from a two-route `agree` or a recomputed condition (read: the narrow net's 0.42 and 0.2, the sample log's 0.47 and 0.043, 2.262, 2.571, step 150, the rates, the 0.073 line, the range ratio, the squared-deviation sums, the five-pair sums). Route B's hand backward matches `train_run` to $10^{-9}$ on all 12 configurations, and retraining all 130 runs matches the file.

- docs/reports/nn-train-L4-numbers.py | `check_wrongs` and the slips | note | Each slip's value is worked from the unrounded data, not from the numbers the screen prints, so several `wrong[]` bands miss the learner's slip (the l16 and problems-4 warning below). The 31 "check by hand" lines list the byKey texts but not whether each slip is reachable. | Work each slip from the printed inputs (the item's own rounded $\bar d$, $s_d$, quantile) and assert the band contains it; raise as an engine item for `numbers_lib` (a `slip(..., inputs=printed)` form).
- docs/reports/nn-train-L4-numbers.py | `power_n` | note | Route B for `runs_needed` is a search on the same normal approximation, so the "formula and a power search agree" in the report checks the arithmetic, not the power: the paired $t$ test at 7 seeds has power 0.69 (see the l16 screens[10] warning). | Add a noncentral-$t$ power at the returned $n$ (SciPy `nct`) and print it beside the claim.

## l13-one-seed-one-draw

- app/content/courses/nn-train/l13-one-seed-one-draw.json | quiz[0] | note | The exact sd is 0.03651 and the band is $0.037 \pm 0.0005$, so a learner who keeps four places (0.0365) is in by $10^{-5}$. It is accepted (checked in `numGrade`), so this is a margin, not a fault. | Widen to `abs: 0.0006` if the item is edited.

## l14-ablations

- app/content/courses/nn-train/l14-ablations.json | screens[4] explain | error | "The difference, -0.057, is the **interaction**". By the lesson's own formula on screens[8], $I = (L_{11} - L_{01}) - (L_{10} - L_{00}) = (0.022 - 0.086) - (0.084 - 0.205) = +0.057$; the code screen's test 4 expects $+0.0566$ for this very table; review-4 items[7] calls the same kind of overlap $+0.03$; and quiz[2] reads a negative $I$ as "the two help more together", the opposite of this screen's "overlap". The learner meets the term with the wrong sign, and `ai-papers` L3 builds its interaction on this one. | "Adam changes the loss by $-0.121$ without layer norm and by $-0.064$ with it. The **interaction** is $I = -0.064 - (-0.121) = 0.057$: positive, because the two changes overlap. So the two directions of ablation can measure a change differently." On screens[8] add after the display: "$L_{ab}$ is the mean loss with change A off (0) or on (1) and change B off or on."
- app/content/courses/nn-train/l14-ablations.json | screens[7] question, key and byKey `sign` | warning | Two sign conventions meet on one screen. screens[2] defines "the effect of a change" as (loss without it) minus (loss of the full set-up), and the explain here says the remove-one ablation "credits it with 0.050". The question asks for "the wider layer's effect on the loss when dropout is on" and keys $-0.05$ (with minus without), so a learner who applies the lesson's definition types $+0.050$ and is told "the effect on the loss is negative". | Ask: "Dropout is on. Adding the wider layer changes the loss by how much? Give 3 decimal places, with its sign." and change byKey `sign` to "That is the removal effect, without minus with; the question asks with minus without."
- app/content/courses/nn-train/l14-ablations.json | screens[4] explain; screens[6] explain | warning | "So the two directions of ablation can rank a change differently" rests on point estimates: added to the baseline, Adam gains 0.121 and layer norm 0.119, a gap the seeds cannot resolve (paired $t = -0.05$, $p = 0.96$). The lesson's own trap is ranking on noise. screens[6]'s "Over ten seeds layer norm matters more" is fairer but the paired difference of the two removals is only just significant ($t = 2.32$, $p = 0.046$). | screens[4]: end with "So the two directions can measure a change differently: Adam is worth 0.121 added to the baseline and 0.058 removed from the full set-up." screens[6] explain: "Over ten seeds layer norm's removal costs more on average, 0.111 against 0.058."
- app/content/courses/nn-train/l14-ablations.json | screens[7] prose | note | The supposed table gives means only, while quiz[1] teaches that "an effect counts only against its seed spread" (the L4 report's backlog bullet says the table is made up, and the prose says "Suppose"). | Add a spread: "...both 0.240, each difference with an sd of about 0.01 across the ten seeds."

## l15-training-log

- app/content/courses/nn-train/l15-training-log.json | screens[8] prelude `variant` | note | `[...][-keep_losses:]` with `keep_losses=0` is `[0:]`, so test 8's `variant(..., keep_losses=0)` keeps all 50 loss events. The expected list (no "no loss curve") matches what the call does, so grading is right, but the call reads as "no losses" and a learner who sees it in a failing test will expect "no loss curve". The `[...][:0]` term is always empty. | `log["events"] = ([e for e in log["events"] if e["kind"] == "loss"][-keep_losses:] if keep_losses else []) + [e for e in log["events"] if e["kind"] != "loss"]`, and test 8 expects `['missing data', 'missing config', 'no loss curve']`; or drop `keep_losses=0` from test 8.
- app/content/courses/nn-train/l15-training-log.json | screens[4] prose | note | "Karpathy's *A Recipe for Training Neural Networks*, in four steps": the recipe has six stages (become one with the data; the end-to-end skeleton and dumb baselines; overfit; regularise; tune; squeeze out the juice), and "overfit one batch" is a check inside the second. The four are the brief's condensation. | "...in four of its steps:" and keep the rest.
- app/content/courses/nn-train/l15-training-log.json | screens[3] explain | note | "a different split moves the loss as much as a different seed": across ten seeds of each, the split sd is 0.029 against the training seed's 0.046. | "nearly as much as a different seed (sd 0.029 against 0.046)".
- app/content/courses/nn-train/l15-training-log.json | screens[6] prose | note | The key says "The first test score chose a change", but the prose says only that the rate "was then lowered". | "After reading the step-150 test loss, the team lowered the rate from 0.01 to 0.005..."

## l16-paired-seeds

- app/content/courses/nn-train/l16-paired-seeds.json | screens[2], [5], [8]; problems-4.json items[0] parts[2], parts[3] | `wrong[]` bands | warning | Ten slip bands miss the slip worked from the numbers the screen prints, so the learner gets the generic line (each checked in `numGrade`). screens[2] ($\bar d = -0.0206$, $s_d = 0.0180$): `sign` 3.62 against $3.63 \pm 0.005$, `nosqrt` $-1.14$ against $-1.15 \pm 0.005$, `se` $-3.43$ against $-3.44 \pm 0.005$: none of the three lines can show. screens[5]: `lower` $-0.0335$ against $-0.0334 \pm 0.00005$, `z` $-0.0094$ against $-0.0095$, `nosqrt` 0.0201 against 0.0200, `sign` 0.0077 against 0.0078: none of the four can show. screens[8]: `sign` 2.23 against $2.22 \pm 0.005$. problems-4 parts[2] (with $s_d = 0.0068$ as the part says): `sign` 4.39 against 4.37, `nosqrt` $-1.79$ against $-1.78$; parts[3]: `z` $-0.0068$ against $-0.0067 \pm 0.00005$, `sign` 0.0051 against 0.0050. | Centre each band between the printed-input and unrounded values and widen to cover both: screens[2] `sign` 3.625 ± 0.012, `nosqrt` -1.145 ± 0.008, `se` -3.437 ± 0.008; screens[5] `lower` -0.03345 ± 0.0001, `z` -0.00945 ± 0.0001, `nosqrt` 0.0201 ± 0.0001, `sign` 0.00775 ± 0.0001; screens[8] `sign` 2.225 ± 0.012; problems-4 parts[2] `sign` 4.38 ± 0.025, `nosqrt` -1.788 ± 0.01; parts[3] `z` -0.00675 ± 0.0001, `sign` 0.00505 ± 0.0001. None overlaps its answer band.
- app/content/courses/nn-train/l16-paired-seeds.json | screens[2] hint 2, explain and feedback.correct; screens[4] hint 2; screens[5] hint 2 and feedback.correct; problems-4.json items[0] parts[2] feedback.correct and explain | warning | Worked figures that do not follow from the printed inputs: "$0.0180/\sqrt{10} = 0.00568$" (0.00569), "$t = -0.0206/(0.0180/\sqrt{10}) = -3.63$" (gives $-3.62$), "$\sqrt{(0.0457^2 + 0.0439^2)/10} = 0.0201$" (0.0200), "That is 0.0128" for $2.262 \times 0.0180/\sqrt{10}$ (0.0129), and in problems-4 "$0.0068/\sqrt 6 = 0.00279$" (0.00278) and "$t = -0.0122/(0.0068/\sqrt 6) = -4.37$" (gives $-4.39$). Each stated result comes from the unrounded data; a learner checking their own arithmetic finds the course out by one in the last place, or by 0.02 in $t$. | Either print the inputs to one more place ($s_d = 0.01796$, problems-4 $s_d = 0.00682$) or state the result the printed inputs give and add "(−3.63 from the unrounded runs)" where the key keeps the unrounded value.
- app/content/courses/nn-train/l16-paired-seeds.json | screens[10] feedback.correct | warning | "a 0.02 gain needs 7 seeds; with batches not fixed, 24". Those are the normal approximation's answers; the paired $t$ test at 7 seeds has power 0.69, not 0.80, and needs 9 (exact noncentral $t$; 24 seeds give 0.77 and 26 are needed). homework-4 h4-seeds says it right ("runs a little low for so few seeds, so add one or two"), so the lesson and the homework disagree, and `ml-int` L3 will plan seeds from this screen. | "All pass. For our pairs ($s_d = 0.0180$) the formula asks for 7 seeds for a 0.02 gain, and 24 with batches not fixed. At so few seeds it runs low: the $t$ test needs about 9 and 26."
- app/content/courses/nn-train/l16-paired-seeds.json | screens[11] explain | warning | The committee sentence ("version 2 raised out-of-sample Sharpe by 0.12, with a 95% interval of 0.04 to 0.20") presents a seed-only interval as the uncertainty of the gain. Both versions were scored on one out-of-sample period, so the interval says nothing about the noise of that period's Sharpe, which `testing` l11 measures and which is the committee's real question. l13 screens[4] made exactly this point for splits. | Third sentence: "It covers seed noise only: both versions saw one test period, whose own noise (`testing` l11) it leaves out." Sentence: "on 8 shared seeds and one test period, version 2 raised ...".
- app/content/courses/nn-train/l16-paired-seeds.json | screens[5] explain; screens[7] option `paired`; homework-4.json items[7] explain; problems-4.json items[0] parts[4] option `q` and explain | warning | "on these seeds B's rate lowers the loss by between 0.008 and 0.033" (and "B is better on these seeds", "better on these seeds, by a little", "On these six seeds Q lowers the loss"). On these seeds the mean difference is simply $-0.0206$; the interval is a statement about the mean over new seeds, on this split and data. The wording reads the interval as a description of the sample, the misreading `ml-int` and `ai-papers` L3 will need gone. | "for new seeds on this split, B's rate lowers the mean loss by between 0.008 and 0.033"; option: "...$p = 0.0055$: across seeds, B is better on this split"; homework: "the new set-up is better on average across seeds, by a little"; problems-4: "Across seeds on this split Q lowers the loss; the whole 95% interval is below 0" and explain "so the gain holds for new seeds on this split".
- app/content/courses/nn-train/l16-paired-seeds.json | screens[3] | note | Five pairs give $t = -2.72$ on 4 degrees of freedom, $p = 0.053$, short of 5%, against $p = 0.0055$ with all ten. The screen stops at $t$, so the learner never sees what five seeds cost. | Feedback.correct: "...$t = -2.72$ on 4 degrees of freedom, $p = 0.053$: five pairs fall just short where ten were clear."
- app/content/courses/nn-train/l16-paired-seeds.json | screens[6] prose and explain | note | The twenty rates are each tested against one baseline, so the tests share the baseline's runs and are positively correlated, not independent; then $1 - 0.95^{20}$ is an upper bound on the false-win chance. The prose says "Suppose ... independent", which is fair, but the scenario contradicts it. The Bonferroni sentence restates `testing` l10 without citing it. | Explain: "...0.642. Tests against one shared baseline are not quite independent, so the true chance is a little lower. A Bonferroni correction (`testing` l10) tests each at $0.05/20 = 0.0025$."

## review-4

- app/content/courses/nn-train/review-4.json | items[7] prose | note | "Four runs of a net over the same seeds: plain, 0.44; ..." names four runs where it means four set-ups, each averaged over the seeds. | "Four set-ups of a net, each averaged over the same seeds: plain, 0.44; ..."

## homework-4

- app/content/courses/nn-train/homework-4.json | items[0] `experiment_report` tests | warning | A Bonferroni count taken from the configs present in `results` (less the baseline) instead of from `changes` passes every hidden test (appendix, homework-4 W1): in every test but 5 the results hold exactly the baseline and the changes, and in test 5 the eleven configs on split 0 move no verdict. This is the "wrong count" slip the task exists to catch. | Add a test with extra configs in the results that are not asked about: `experiment_report(EDGE + [r for r in plant(5, {"y": 0.0, "z": 0.0, "w": 0.0, "v": 0.0}) if r["config"] != "base"], "base", ["x"])["x"]["survives"]` expecting `True` (Bonferroni over one change); the slip gives `False`.
- app/content/courses/nn-train/homework-4.json | items[0] tests 4 and 8 | note | `plant(5, {"y": 0.0, ...})` reads as four null effects, but its base is dropped and the four are paired with EDGE's base, whose level differs: their mean differences are about $-0.104$ and all four survive. The tests check only x's verdict, which is right under Bonferroni whatever the others are, so grading is sound; but the "borderline effect among nulls" the code suggests is a borderline effect among four strong ones (Holm's step-down, a valid procedure, would let x through). | Build the four companions on EDGE's base (`plant` with EDGE's seed, or `effects` measured from it), or rename them in the setup line to say they are real effects.
- app/content/courses/nn-train/homework-4.json | items[1] `log_diff` tests | note | A field set to `None` in one log and absent from the other is a difference by the starter's rule ("a field in one log only counts as differing") and the explain, but no test has that pair, so reading an absent field as `None` passes (appendix, homework-4 items[1] W3). | Add `L7 = copy.deepcopy(LOG1); L7["code"] = None; L8 = copy.deepcopy(LOG1); del L8["code"]`, call `log_diff(L7, L8)`, expect `['code']`.

## problems-4

- app/content/courses/nn-train/problems-4.json | items[2] parts[3] | warning | The key says "The test set was scored five times, so it helped choose the reported run", but the prose says the team reported seed 2's 0.131, the lowest validation loss, and no test score is reported. Choosing by validation and then scoring the test set is the right procedure; the bias the key names exists only if the test scores drove the choice. | Question: "The team's log shows they scored the test set after each of the five runs and reported the run with the best test score. Which fault matters most for that reported test score?"

## Automated checks (no finding)

- `grade-all.mjs --file <f> --code --local-cdn <pkgs>`, each of the seven files alone: 0 failures; 9 Python code widgets run; every starter fails test 1 and every authored mutant fails its named test. No code feedback in the level has `byKey` `test-N` lines (each code screen has only `correct` and `generic`), so there is no `test-N` line to show or miss.
- Per-case time against the page's limit (two runs, the slower kept): the slowest is l15 screens[9] test 3 (the zero net, 200 Adam steps) at 182 ms against 38 s (209x); every other case is over 400x. Threshold tests: the 200-step batch ends at 0.00041 against a bar of 0.01 (24x), the zero net sits at exactly $\ln 2$ (the batch holds four points of each class, so every gradient is 0) against a bar of 0.6.
- Statistics recomputed from `nn-train-seeds.json`: A 0.10846 (sd 0.045714), B 0.08786 (0.043941); $\bar d = -0.020600$, $s_d = 0.017957$, $t = -3.628$, $p = 0.00550$, interval $-0.03345$ to $-0.00775$; Welch $t = -1.027$ on 17.97 df, $p = 0.318$; B lower on 10 of 10 (sign test $p = 0.002$); correlations 0.921 and 0.653; other batches $\bar d = -0.02437$, $s_d = 0.03464$, $t = -2.225$, $p = 0.0532$, interval $-0.0491$ to $0.0004$; five pairs (to 3 places) $-0.0258$, 0.02123, $-2.717$; removal effects 0.05775 (sd 0.06631, $t = 2.75$, $p = 0.022$), 0.11123 (0.04681, $t = 7.51$), $-0.02361$ (0.01455, $t = -5.13$, lower on 9 of 10); Bonferroni cut-off for three changes $t_{0.99167, 9} = 2.933$, so Adam's removal misses it as homework test 5 expects; interaction 0.0567 (per-seed $p = 0.043$); seed 6 effects 0.2374 and 0.1177; split-seed sd 0.02893; narrow net eight-seed sum 0.91536, mean 0.11442, all ten 0.17573; $1 - 0.95^{20} = 0.6415$, $1 - 0.95^{10} = 0.4013$; Sharpe interval 0.0364 to 0.2036; 6.36, 23.49 and 17.66 seeds by the normal formula.
- Every hand figure in review-4, homework-4 and problems-4 recomputed from its printed inputs: 0.0224, $-3.50$ ($s_d = 0.010488$), 20, 0.0157 and 0.0443, 0.03, 18 and 14, 0.00625 and 0.00556, $-0.0016$ and $-0.0144$, $-0.0122$, 0.0068 (sum of squares 0.000233), $-0.0050$, 0.040 and 0.0071, $-0.04$, 50 and 80, 0.143, 0.0094 (0.000350), 1.28. The longform rubric sums to 10.
- Teaching claims checked and sound: separate seed streams leave the batches alone when dropout is switched off (and `Generator.spawn` gives the same children, accepted); se $= s/\sqrt n$ and "quadrupling the seeds halves it"; $0.006\sqrt 2$ for two independent single runs; the bimodal advice (failure rate plus the mean of the rest, with "a failure rate of 0.2 is itself rough"); remove-one plus add-one with three changes is all 8 mixes; fresh dropout masks add noise without bias, so the paired test stays valid and weaker; Bonferroni holds "whatever the dependence"; the 95% interval kept beside a corrected verdict, said in the explain; B beating A on all ten seeds disclosed against the brief's nine.
- `voice-scan.py 35` on the course: 0 sentences over 35 words (7,920 scanned), 0 explanations over three sentences, 0 lesson ids in code spans, 0 doubled words. No em-dashes, no exclamation marks outside code, no American spellings in prose. Every `wrong[]` id and every wrong option has a `byKey` line. Hint highlight ids resolve (table `r{i}` and `r{i}c{j}` zero-based, console `l{i}` one-based, bars `x{label}`). The two percentage items (l16 screens[6], quiz[2]) carry `unit: "%"`, so 64.2 and 40.1 are accepted.

## Appendix: wrong solutions

Each widget's model solution was edited into a wrong one and graded as a `mutant` in Pyodide by `grade-all.mjs --code` (scratch copies in the scratchpad's `rv-nt4/wrong-json`, nothing committed). "fails Tn" is the first hidden test it fails. The first line of each widget checks that the model solution, with the starter's comment lines kept, still passes. Builder: the scratchpad's `rv-nt4/wrongs.py` and `mkwrong.py`.

### l13-one-seed-one-draw screens[7] `seed_summary` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. statistics.stdev for the sd (a correct alternative): **passes** (accepted, as it should be).

```python
import statistics


def seed_summary(results):
    return (statistics.fmean(results), statistics.stdev(results), min(results), max(results))
```
- W2. NumPy with ddof=1 (a correct alternative): **passes** (accepted, as it should be).

```python
import numpy as np


def seed_summary(results):
    x = np.array(results)
    return (float(x.mean()), float(x.std(ddof=1)), float(x.min()), float(x.max()))
```
- W3. reports the standard error s/sqrt(n) as the sd: **fails T1**.

```python
def seed_summary(results):
    n = len(results)
    mean = sum(results) / n
    var = sum((x - mean) ** 2 for x in results) / (n - 1)
    return (mean, (var / n) ** 0.5, min(results), max(results))
```
- W4. reports the best seed as the centre: **fails T1**.

```python
def seed_summary(results):
    n = len(results)
    mean = sum(results) / n
    var = sum((x - mean) ** 2 for x in results) / (n - 1)
    return (min(results), var ** 0.5, min(results), max(results))
```
- W5. sorts the input in place to read the lowest and highest: **fails T5**.

```python
def seed_summary(results):
    n = len(results)
    mean = sum(results) / n
    var = sum((x - mean) ** 2 for x in results) / (n - 1)
    results.sort()
    return (mean, var ** 0.5, results[0], results[-1])
```
- W6. divides the mean by n - 1 as well: **fails T1**.

```python
def seed_summary(results):
    n = len(results)
    mean = sum(results) / (n - 1)
    var = sum((x - mean) ** 2 for x in results) / (n - 1)
    return (mean, var ** 0.5, min(results), max(results))
```

### l13-one-seed-one-draw screens[8] `set_all_seeds` (5 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. Generator.spawn from default_rng(seed) (a correct alternative): **passes** (accepted, as it should be).

```python
import numpy as np


def set_all_seeds(seed):
    return tuple(np.random.default_rng(seed).spawn(3))
```
- W2. three generators seeded seed, seed + 1, seed + 2: **fails T1**.

```python
import numpy as np


def set_all_seeds(seed):
    return tuple(np.random.default_rng(seed + k) for k in range(3))
```
- W3. children seeded by generate_state instead of passed to default_rng: **fails T1**.

```python
import numpy as np


def set_all_seeds(seed):
    children = np.random.SeedSequence(seed).spawn(3)
    return tuple(np.random.default_rng(int(c.generate_state(1)[0])) for c in children)
```
- W4. the seed itself for the weights, two spawned children for the rest: **fails T1**.

```python
import numpy as np


def set_all_seeds(seed):
    children = np.random.SeedSequence(seed).spawn(2)
    return (np.random.default_rng(seed),) + tuple(np.random.default_rng(c) for c in children)
```

### l14-ablations screens[9] `ablation_table` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. sd from the two rows' own sds (unpaired), mean of the differences right: **fails T1**.

```python
def ablation_table(runs, full, removed):
    base = {r["seed"]: r["val"] for r in runs if r["config"] == full}
    fb = list(base.values())
    mf = sum(fb) / len(fb)
    vf = sum((x - mf) ** 2 for x in fb) / (len(fb) - 1)
    table = {}
    for change, name in removed.items():
        row = [r["val"] for r in runs if r["config"] == name]
        mr = sum(row) / len(row)
        vr = sum((x - mr) ** 2 for x in row) / (len(row) - 1)
        table[change] = (mr - mf, (vr + vf) ** 0.5)
    return table


def interaction(t):
    a_alone = t[1][0] - t[0][0]
    a_with_b = t[1][1] - t[0][1]
    return (a_alone, a_with_b, a_with_b - a_alone)
```
- W2. sd of the differences divides by n: **fails T1**.

```python
def ablation_table(runs, full, removed):
    base = {r["seed"]: r["val"] for r in runs if r["config"] == full}
    table = {}
    for change, name in removed.items():
        diffs = [r["val"] - base[r["seed"]] for r in runs if r["config"] == name and r["seed"] in base]
        n = len(diffs)
        mean = sum(diffs) / n
        table[change] = (mean, (sum((d - mean) ** 2 for d in diffs) / n) ** 0.5)
    return table


def interaction(t):
    a_alone = t[1][0] - t[0][0]
    a_with_b = t[1][1] - t[0][1]
    return (a_alone, a_with_b, a_with_b - a_alone)
```
- W3. interaction as with-B-off minus with-B-on (sign flipped): **fails T4**.

```python
def ablation_table(runs, full, removed):
    base = {r["seed"]: r["val"] for r in runs if r["config"] == full}
    table = {}
    for change, name in removed.items():
        diffs = [r["val"] - base[r["seed"]] for r in runs if r["config"] == name and r["seed"] in base]
        n = len(diffs)
        mean = sum(diffs) / n
        sd = (sum((d - mean) ** 2 for d in diffs) / (n - 1)) ** 0.5
        table[change] = (mean, sd)
    return table


def interaction(t):
    a_alone = t[1][0] - t[0][0]
    a_with_b = t[1][1] - t[0][1]
    return (a_alone, a_with_b, a_alone - a_with_b)
```
- W4. interaction indexed t[b][a] (B's effects; the difference is the same): **fails T4**.

```python
def ablation_table(runs, full, removed):
    base = {r["seed"]: r["val"] for r in runs if r["config"] == full}
    table = {}
    for change, name in removed.items():
        diffs = [r["val"] - base[r["seed"]] for r in runs if r["config"] == name and r["seed"] in base]
        n = len(diffs)
        mean = sum(diffs) / n
        sd = (sum((d - mean) ** 2 for d in diffs) / (n - 1)) ** 0.5
        table[change] = (mean, sd)
    return table


def interaction(t):
    b_alone = t[0][1] - t[0][0]
    b_with_a = t[1][1] - t[1][0]
    return (b_alone, b_with_a, b_with_a - b_alone)
```
- W5. effects against the first row in the list, not the full set-up (two changes per row): **fails T1**.

```python
def ablation_table(runs, full, removed):
    first = runs[0]["config"]
    base = {r["seed"]: r["val"] for r in runs if r["config"] == first}
    table = {}
    for change, name in removed.items():
        diffs = [r["val"] - base[r["seed"]] for r in runs if r["config"] == name and r["seed"] in base]
        n = len(diffs)
        mean = sum(diffs) / n
        sd = (sum((d - mean) ** 2 for d in diffs) / (n - 1)) ** 0.5
        table[change] = (mean, sd)
    return table


def interaction(t):
    a_alone = t[1][0] - t[0][0]
    a_with_b = t[1][1] - t[0][1]
    return (a_alone, a_with_b, a_with_b - a_alone)
```
- W6. one seed per row: the seed-0 difference with sd 0: **fails T1**.

```python
def ablation_table(runs, full, removed):
    base = {r["seed"]: r["val"] for r in runs if r["config"] == full}
    table = {}
    for change, name in removed.items():
        r0 = min((r for r in runs if r["config"] == name), key=lambda r: r["seed"])
        table[change] = (r0["val"] - base[r0["seed"]], 0.0)
    return table


def interaction(t):
    a_alone = t[1][0] - t[0][0]
    a_with_b = t[1][1] - t[0][1]
    return (a_alone, a_with_b, a_with_b - a_alone)
```

### l15-training-log screens[8] `audit_log` (8 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. no loss curve only when there are no loss events at all: **fails T5**.

```python
REQUIRED = ["code", "data", "split_seed", "seed", "config"]


def audit_log(log):
    problems = []
    for field in REQUIRED:
        if log.get(field) is None:
            problems.append("missing " + field)
    events = log.get("events", [])
    if sum(e["kind"] == "loss" for e in events) == 0:
        problems.append("no loss curve")
    tests = sum(e["kind"] == "test" for e in events)
    if tests > 1:
        problems.append(f"test scored {tests} times")
    for e in events:
        if e["kind"] == "set":
            problems.append(f"changed {e['key']} at step {e['step']}")
        if e["kind"] == "resume" and "from" not in e:
            problems.append(f"resume at step {e['step']} without a checkpoint")
    return problems
```
- W2. missing fields in alphabetical order: **fails T8**.

```python
REQUIRED = ["code", "data", "split_seed", "seed", "config"]


def audit_log(log):
    problems = []
    for field in sorted(REQUIRED):
        if log.get(field) is None:
            problems.append("missing " + field)
    events = log.get("events", [])
    if sum(e["kind"] == "loss" for e in events) < 2:
        problems.append("no loss curve")
    tests = sum(e["kind"] == "test" for e in events)
    if tests > 1:
        problems.append(f"test scored {tests} times")
    for e in events:
        if e["kind"] == "set":
            problems.append(f"changed {e['key']} at step {e['step']}")
        if e["kind"] == "resume" and "from" not in e:
            problems.append(f"resume at step {e['step']} without a checkpoint")
    return problems
```
- W3. every resume flagged, checkpoint or not: **fails T6**.

```python
REQUIRED = ["code", "data", "split_seed", "seed", "config"]


def audit_log(log):
    problems = []
    for field in REQUIRED:
        if log.get(field) is None:
            problems.append("missing " + field)
    events = log.get("events", [])
    if sum(e["kind"] == "loss" for e in events) < 2:
        problems.append("no loss curve")
    tests = sum(e["kind"] == "test" for e in events)
    if tests > 1:
        problems.append(f"test scored {tests} times")
    for e in events:
        if e["kind"] == "set":
            problems.append(f"changed {e['key']} at step {e['step']}")
        if e["kind"] == "resume":
            problems.append(f"resume at step {e['step']} without a checkpoint")
    return problems
```
- W4. set events listed before the test count: **fails T7**.

```python
REQUIRED = ["code", "data", "split_seed", "seed", "config"]


def audit_log(log):
    problems = []
    for field in REQUIRED:
        if log.get(field) is None:
            problems.append("missing " + field)
    events = log.get("events", [])
    if sum(e["kind"] == "loss" for e in events) < 2:
        problems.append("no loss curve")
    for e in events:
        if e["kind"] == "set":
            problems.append(f"changed {e['key']} at step {e['step']}")
        if e["kind"] == "resume" and "from" not in e:
            problems.append(f"resume at step {e['step']} without a checkpoint")
    tests = sum(e["kind"] == "test" for e in events)
    if tests > 1:
        problems.append(f"test scored {tests} times")
    return problems
```
- W5. a resume with "from": None counted as having no checkpoint (e.get; a correct reading of the comment): **passes** (accepted, as it should be).

```python
REQUIRED = ["code", "data", "split_seed", "seed", "config"]


def audit_log(log):
    problems = []
    for field in REQUIRED:
        if log.get(field) is None:
            problems.append("missing " + field)
    events = log.get("events", [])
    if sum(e["kind"] == "loss" for e in events) < 2:
        problems.append("no loss curve")
    tests = sum(e["kind"] == "test" for e in events)
    if tests > 1:
        problems.append(f"test scored {tests} times")
    for e in events:
        if e["kind"] == "set":
            problems.append(f"changed {e['key']} at step {e['step']}")
        if e["kind"] == "resume" and e.get("from") is None:
            problems.append(f"resume at step {e['step']} without a checkpoint")
    return problems
```

### l15-training-log screens[9] `overfit_one_batch` (5 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. plain SGD instead of Adam: **fails T1**.

```python
import numpy as np
from nt_ops_l1 import loss_and_grads, full_loss, adam_step


def overfit_one_batch(make_net, batch, steps, lr):
    Xb, yb = batch
    params = make_net()
    for t in range(1, steps + 1):
        _, grads = loss_and_grads(params, Xb, yb)
        params = [p - lr * g for p, g in zip(params, grads)]
    return full_loss(params, Xb, yb)
```
- W2. the rate ignored (always 0.01): **fails T5**.

```python
import numpy as np
from nt_ops_l1 import loss_and_grads, full_loss, adam_step


def overfit_one_batch(make_net, batch, steps, lr):
    Xb, yb = batch
    params = make_net()
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    for t in range(1, steps + 1):
        _, grads = loss_and_grads(params, Xb, yb)
        params, m, v = adam_step(params, grads, m, v, t, 0.01)
    return full_loss(params, Xb, yb)
```
- W3. one step fewer (range(1, steps)): **fails T1**.

```python
import numpy as np
from nt_ops_l1 import loss_and_grads, full_loss, adam_step


def overfit_one_batch(make_net, batch, steps, lr):
    Xb, yb = batch
    params = make_net()
    m = [np.zeros_like(p) for p in params]
    v = [np.zeros_like(p) for p in params]
    for t in range(1, steps):
        _, grads = loss_and_grads(params, Xb, yb)
        params, m, v = adam_step(params, grads, m, v, t, lr)
    return full_loss(params, Xb, yb)
```
- W4. Adam moments kept at module level across calls: **fails T5**.

```python
import numpy as np
from nt_ops_l1 import loss_and_grads, full_loss, adam_step


STATE = {}


def overfit_one_batch(make_net, batch, steps, lr):
    Xb, yb = batch
    params = make_net()
    if "m" not in STATE:
        STATE["m"] = [np.zeros_like(p) for p in params]
        STATE["v"] = [np.zeros_like(p) for p in params]
    for t in range(1, steps + 1):
        _, grads = loss_and_grads(params, Xb, yb)
        params, STATE["m"], STATE["v"] = adam_step(params, grads, STATE["m"], STATE["v"], t, lr)
    return full_loss(params, Xb, yb)
```

### l16-paired-seeds screens[9] `paired_t` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. Welch's unpaired test, with Welch's degrees of freedom for the interval: **fails T1**.

```python
import math
from nt_ops_l4 import t_quantile


def paired_t(a, b):
    n, k = len(a), len(b)
    ma, mb = sum(a) / n, sum(b) / k
    va = sum((x - ma) ** 2 for x in a) / (n - 1)
    vb = sum((x - mb) ** 2 for x in b) / (k - 1)
    se = math.sqrt(va / n + vb / k)
    df = (va / n + vb / k) ** 2 / ((va / n) ** 2 / (n - 1) + (vb / k) ** 2 / (k - 1))
    mean = mb - ma
    half = t_quantile(0.975, df) * se
    return (mean, mean / se, (mean - half, mean + half))


def compare_configs(runs, a, b, split=0):
    ra = {r["seed"]: r["val"] for r in runs if r["config"] == a and r["split_seed"] == split}
    rb = {r["seed"]: r["val"] for r in runs if r["config"] == b and r["split_seed"] == split}
    seeds = sorted(set(ra) & set(rb))
    xa, xb = [ra[s] for s in seeds], [rb[s] for s in seeds]
    mean, t, ci = paired_t(xa, xb)
    wins = sum(y < x for x, y in zip(xa, xb))
    return {"n": len(seeds), "mean_diff": mean, "t": t, "ci": list(ci), "wins": wins}
```
- W2. se of the mean difference from the two means' standard errors, df n - 1: **fails T1**.

```python
import math
from nt_ops_l4 import t_quantile


def paired_t(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    sea = math.sqrt(sum((x - ma) ** 2 for x in a) / (n - 1) / n)
    seb = math.sqrt(sum((x - mb) ** 2 for x in b) / (n - 1) / n)
    se = math.sqrt(sea ** 2 + seb ** 2)
    mean = mb - ma
    half = t_quantile(0.975, n - 1) * se
    return (mean, mean / se, (mean - half, mean + half))


def compare_configs(runs, a, b, split=0):
    ra = {r["seed"]: r["val"] for r in runs if r["config"] == a and r["split_seed"] == split}
    rb = {r["seed"]: r["val"] for r in runs if r["config"] == b and r["split_seed"] == split}
    seeds = sorted(set(ra) & set(rb))
    xa, xb = [ra[s] for s in seeds], [rb[s] for s in seeds]
    mean, t, ci = paired_t(xa, xb)
    wins = sum(y < x for x, y in zip(xa, xb))
    return {"n": len(seeds), "mean_diff": mean, "t": t, "ci": list(ci), "wins": wins}
```
- W3. interval with z = 1.96 at small n (NormalDist): **fails T1**.

```python
import math
from statistics import NormalDist
from nt_ops_l4 import t_quantile


def paired_t(a, b):
    d = [y - x for x, y in zip(a, b)]
    n = len(d)
    mean = sum(d) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1))
    se = sd / math.sqrt(n)
    half = NormalDist().inv_cdf(0.975) * se
    return (mean, mean / se, (mean - half, mean + half))


def compare_configs(runs, a, b, split=0):
    ra = {r["seed"]: r["val"] for r in runs if r["config"] == a and r["split_seed"] == split}
    rb = {r["seed"]: r["val"] for r in runs if r["config"] == b and r["split_seed"] == split}
    seeds = sorted(set(ra) & set(rb))
    xa, xb = [ra[s] for s in seeds], [rb[s] for s in seeds]
    mean, t, ci = paired_t(xa, xb)
    wins = sum(y < x for x, y in zip(xa, xb))
    return {"n": len(seeds), "mean_diff": mean, "t": t, "ci": list(ci), "wins": wins}
```
- W4. interval on n degrees of freedom: **fails T1**.

```python
import math
from nt_ops_l4 import t_quantile


def paired_t(a, b):
    d = [y - x for x, y in zip(a, b)]
    n = len(d)
    mean = sum(d) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1))
    se = sd / math.sqrt(n)
    half = t_quantile(0.975, n) * se
    return (mean, mean / se, (mean - half, mean + half))


def compare_configs(runs, a, b, split=0):
    ra = {r["seed"]: r["val"] for r in runs if r["config"] == a and r["split_seed"] == split}
    rb = {r["seed"]: r["val"] for r in runs if r["config"] == b and r["split_seed"] == split}
    seeds = sorted(set(ra) & set(rb))
    xa, xb = [ra[s] for s in seeds], [rb[s] for s in seeds]
    mean, t, ci = paired_t(xa, xb)
    wins = sum(y < x for x, y in zip(xa, xb))
    return {"n": len(seeds), "mean_diff": mean, "t": t, "ci": list(ci), "wins": wins}
```
- W5. a 90% interval (t_quantile(0.95, n - 1)): **fails T1**.

```python
import math
from nt_ops_l4 import t_quantile


def paired_t(a, b):
    d = [y - x for x, y in zip(a, b)]
    n = len(d)
    mean = sum(d) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1))
    se = sd / math.sqrt(n)
    half = t_quantile(0.95, n - 1) * se
    return (mean, mean / se, (mean - half, mean + half))


def compare_configs(runs, a, b, split=0):
    ra = {r["seed"]: r["val"] for r in runs if r["config"] == a and r["split_seed"] == split}
    rb = {r["seed"]: r["val"] for r in runs if r["config"] == b and r["split_seed"] == split}
    seeds = sorted(set(ra) & set(rb))
    xa, xb = [ra[s] for s in seeds], [rb[s] for s in seeds]
    mean, t, ci = paired_t(xa, xb)
    wins = sum(y < x for x, y in zip(xa, xb))
    return {"n": len(seeds), "mean_diff": mean, "t": t, "ci": list(ci), "wins": wins}
```
- W6. compare_configs ignores the split seed: **fails T3**.

```python
import math
from nt_ops_l4 import t_quantile


def paired_t(a, b):
    d = [y - x for x, y in zip(a, b)]
    n = len(d)
    mean = sum(d) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1))
    se = sd / math.sqrt(n)
    half = t_quantile(0.975, n - 1) * se
    return (mean, mean / se, (mean - half, mean + half))


def compare_configs(runs, a, b, split=0):
    ra = {r["seed"]: r["val"] for r in runs if r["config"] == a}
    rb = {r["seed"]: r["val"] for r in runs if r["config"] == b}
    seeds = sorted(set(ra) & set(rb))
    xa, xb = [ra[s] for s in seeds], [rb[s] for s in seeds]
    mean, t, ci = paired_t(xa, xb)
    wins = sum(y < x for x, y in zip(xa, xb))
    return {"n": len(seeds), "mean_diff": mean, "t": t, "ci": list(ci), "wins": wins}
```
- W7. wins counted where a is lower: **fails T3**.

```python
import math
from nt_ops_l4 import t_quantile


def paired_t(a, b):
    d = [y - x for x, y in zip(a, b)]
    n = len(d)
    mean = sum(d) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1))
    se = sd / math.sqrt(n)
    half = t_quantile(0.975, n - 1) * se
    return (mean, mean / se, (mean - half, mean + half))


def compare_configs(runs, a, b, split=0):
    ra = {r["seed"]: r["val"] for r in runs if r["config"] == a and r["split_seed"] == split}
    rb = {r["seed"]: r["val"] for r in runs if r["config"] == b and r["split_seed"] == split}
    seeds = sorted(set(ra) & set(rb))
    xa, xb = [ra[s] for s in seeds], [rb[s] for s in seeds]
    mean, t, ci = paired_t(xa, xb)
    wins = sum(x < y for x, y in zip(xa, xb))
    return {"n": len(seeds), "mean_diff": mean, "t": t, "ci": list(ci), "wins": wins}
```
- W8. the best seed of each set-up reported as the difference: **fails T3**.

```python
import math
from nt_ops_l4 import t_quantile


def paired_t(a, b):
    d = [y - x for x, y in zip(a, b)]
    n = len(d)
    mean = sum(d) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1))
    se = sd / math.sqrt(n)
    half = t_quantile(0.975, n - 1) * se
    return (mean, mean / se, (mean - half, mean + half))


def compare_configs(runs, a, b, split=0):
    ra = {r["seed"]: r["val"] for r in runs if r["config"] == a and r["split_seed"] == split}
    rb = {r["seed"]: r["val"] for r in runs if r["config"] == b and r["split_seed"] == split}
    seeds = sorted(set(ra) & set(rb))
    xa, xb = [ra[s] for s in seeds], [rb[s] for s in seeds]
    _, t, ci = paired_t(xa, xb)
    wins = sum(y < x for x, y in zip(xa, xb))
    return {"n": len(seeds), "mean_diff": min(xb) - min(xa), "t": t, "ci": list(ci), "wins": wins}
```

### l16-paired-seeds screens[10] `runs_needed` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. int(n) + 1 instead of the ceiling: **SURVIVES** (wrong only when n is an exact whole number, which floats almost never give; no fix needed).

```python
from statistics import NormalDist


def runs_needed(sd_d, delta, alpha=0.05, power=0.8):
    z = NormalDist().inv_cdf
    n = ((z(1 - alpha / 2) + z(power)) * sd_d / delta) ** 2
    return int(n) + 1
```
- W2. z of 1 - power (the wrong tail): **fails T1**.

```python
import math
from statistics import NormalDist


def runs_needed(sd_d, delta, alpha=0.05, power=0.8):
    z = NormalDist().inv_cdf
    n = ((z(1 - alpha / 2) + z(1 - power)) * sd_d / delta) ** 2
    return math.ceil(n)
```
- W3. treats the pairs as unpaired (sd times root 2): **fails T1**.

```python
import math
from statistics import NormalDist


def runs_needed(sd_d, delta, alpha=0.05, power=0.8):
    z = NormalDist().inv_cdf
    n = ((z(1 - alpha / 2) + z(power)) * sd_d * math.sqrt(2) / delta) ** 2
    return math.ceil(n)
```
- W4. adds two seeds to the normal answer, as homework h4-seeds advises: **fails T1**.

```python
import math
from statistics import NormalDist


def runs_needed(sd_d, delta, alpha=0.05, power=0.8):
    z = NormalDist().inv_cdf
    n = math.ceil(((z(1 - alpha / 2) + z(power)) * sd_d / delta) ** 2)
    return n + 2
```

### homework-4 items[0] `experiment_report` (8 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. Bonferroni over the configs in the results less one, not over the changes asked: **SURVIVES** (see homework-4 items[0] warning).

```python
import math
from nt_ops_l4 import t_quantile


def experiment_report(results, baseline, changes):
    base = {r["seed"]: r["val"] for r in results if r["config"] == baseline}
    m = len({r["config"] for r in results}) - 1
    out = {}
    for c in changes:
        d = [r["val"] - base[r["seed"]] for r in results if r["config"] == c and r["seed"] in base]
        n = len(d)
        mean = sum(d) / n
        se = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1)) / math.sqrt(n)
        half = t_quantile(0.975, n - 1) * se
        crit = t_quantile(1 - 0.05 / (2 * m), n - 1)
        out[c] = {"mean_diff": mean, "ci": [mean - half, mean + half], "survives": abs(mean / se) > crit}
    return out
```
- W2. Bonferroni over the seeds (n): **fails T3**.

```python
import math
from nt_ops_l4 import t_quantile


def experiment_report(results, baseline, changes):
    base = {r["seed"]: r["val"] for r in results if r["config"] == baseline}
    m = None
    out = {}
    for c in changes:
        d = [r["val"] - base[r["seed"]] for r in results if r["config"] == c and r["seed"] in base]
        n = len(d)
        m = n
        mean = sum(d) / n
        se = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1)) / math.sqrt(n)
        half = t_quantile(0.975, n - 1) * se
        crit = t_quantile(1 - 0.05 / (2 * m), n - 1)
        out[c] = {"mean_diff": mean, "ci": [mean - half, mean + half], "survives": abs(mean / se) > crit}
    return out
```
- W3. Bonferroni counting the baseline as a test (m + 1): **fails T3**.

```python
import math
from nt_ops_l4 import t_quantile


def experiment_report(results, baseline, changes):
    base = {r["seed"]: r["val"] for r in results if r["config"] == baseline}
    m = len(changes) + 1
    out = {}
    for c in changes:
        d = [r["val"] - base[r["seed"]] for r in results if r["config"] == c and r["seed"] in base]
        n = len(d)
        mean = sum(d) / n
        se = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1)) / math.sqrt(n)
        half = t_quantile(0.975, n - 1) * se
        crit = t_quantile(1 - 0.05 / (2 * m), n - 1)
        out[c] = {"mean_diff": mean, "ci": [mean - half, mean + half], "survives": abs(mean / se) > crit}
    return out
```
- W4. Bonferroni with the normal quantile: **fails T4**.

```python
import math
from statistics import NormalDist
from nt_ops_l4 import t_quantile


def experiment_report(results, baseline, changes):
    base = {r["seed"]: r["val"] for r in results if r["config"] == baseline}
    m = len(changes)
    out = {}
    for c in changes:
        d = [r["val"] - base[r["seed"]] for r in results if r["config"] == c and r["seed"] in base]
        n = len(d)
        mean = sum(d) / n
        se = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1)) / math.sqrt(n)
        half = t_quantile(0.975, n - 1) * se
        crit = NormalDist().inv_cdf(1 - 0.05 / (2 * m))
        out[c] = {"mean_diff": mean, "ci": [mean - half, mean + half], "survives": abs(mean / se) > crit}
    return out
```
- W5. Holm's step-down instead of Bonferroni: **fails T4**.

```python
import math
from nt_ops_l4 import t_quantile, t_cdf


def experiment_report(results, baseline, changes):
    base = {r["seed"]: r["val"] for r in results if r["config"] == baseline}
    m = len(changes)
    out, pv = {}, {}
    for c in changes:
        d = [r["val"] - base[r["seed"]] for r in results if r["config"] == c and r["seed"] in base]
        n = len(d)
        mean = sum(d) / n
        se = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1)) / math.sqrt(n)
        half = t_quantile(0.975, n - 1) * se
        pv[c] = 2 * (1 - t_cdf(abs(mean / se), n - 1))
        out[c] = {"mean_diff": mean, "ci": [mean - half, mean + half], "survives": False}
    for k, c in enumerate(sorted(changes, key=lambda c: pv[c])):
        if pv[c] >= 0.05 / (m - k):
            break
        out[c]["survives"] = True
    return out
```
- W6. unpaired (Welch) standard error for each change: **fails T1**.

```python
import math
from nt_ops_l4 import t_quantile


def experiment_report(results, baseline, changes):
    b = [r["val"] for r in results if r["config"] == baseline]
    mb = sum(b) / len(b)
    vb = sum((x - mb) ** 2 for x in b) / (len(b) - 1)
    m = len(changes)
    out = {}
    for c in changes:
        x = [r["val"] for r in results if r["config"] == c]
        n = len(x)
        mx = sum(x) / n
        vx = sum((v - mx) ** 2 for v in x) / (n - 1)
        se = math.sqrt(vx / n + vb / len(b))
        mean = mx - mb
        half = t_quantile(0.975, n - 1) * se
        crit = t_quantile(1 - 0.05 / (2 * m), n - 1)
        out[c] = {"mean_diff": mean, "ci": [mean - half, mean + half], "survives": abs(mean / se) > crit}
    return out
```
- W7. verdict from the uncorrected 95% interval excluding 0: **fails T4**.

```python
import math
from nt_ops_l4 import t_quantile


def experiment_report(results, baseline, changes):
    base = {r["seed"]: r["val"] for r in results if r["config"] == baseline}
    m = 1
    out = {}
    for c in changes:
        d = [r["val"] - base[r["seed"]] for r in results if r["config"] == c and r["seed"] in base]
        n = len(d)
        mean = sum(d) / n
        se = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1)) / math.sqrt(n)
        half = t_quantile(0.975, n - 1) * se
        crit = t_quantile(1 - 0.05 / (2 * m), n - 1)
        out[c] = {"mean_diff": mean, "ci": [mean - half, mean + half], "survives": abs(mean / se) > crit}
    return out
```
- W8. the interval with z = 1.96, Bonferroni right: **fails T1**.

```python
import math
from nt_ops_l4 import t_quantile


def experiment_report(results, baseline, changes):
    base = {r["seed"]: r["val"] for r in results if r["config"] == baseline}
    m = len(changes)
    out = {}
    for c in changes:
        d = [r["val"] - base[r["seed"]] for r in results if r["config"] == c and r["seed"] in base]
        n = len(d)
        mean = sum(d) / n
        se = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1)) / math.sqrt(n)
        half = 1.96 * se
        crit = t_quantile(1 - 0.05 / (2 * m), n - 1)
        out[c] = {"mean_diff": mean, "ci": [mean - half, mean + half], "survives": abs(mean / se) > crit}
    return out
```
- W9. the best seed of each config differenced: **fails T1**.

```python
import math
from nt_ops_l4 import t_quantile


def experiment_report(results, baseline, changes):
    base = {r["seed"]: r["val"] for r in results if r["config"] == baseline}
    m = len(changes)
    out = {}
    for c in changes:
        d = [r["val"] - base[r["seed"]] for r in results if r["config"] == c and r["seed"] in base]
        n = len(d)
        mean = sum(d) / n
        se = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1)) / math.sqrt(n)
        half = t_quantile(0.975, n - 1) * se
        crit = t_quantile(1 - 0.05 / (2 * m), n - 1)
        best = min(r["val"] for r in results if r["config"] == c) - min(base.values())
        out[c] = {"mean_diff": best, "ci": [mean - half, mean + half], "survives": abs(mean / se) > crit}
    return out
```
- W10. |t| >= the cut-off instead of > (harmless): **passes** (accepted, as it should be).

```python
import math
from nt_ops_l4 import t_quantile


def experiment_report(results, baseline, changes):
    base = {r["seed"]: r["val"] for r in results if r["config"] == baseline}
    m = len(changes)
    out = {}
    for c in changes:
        d = [r["val"] - base[r["seed"]] for r in results if r["config"] == c and r["seed"] in base]
        n = len(d)
        mean = sum(d) / n
        se = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1)) / math.sqrt(n)
        half = t_quantile(0.975, n - 1) * se
        crit = t_quantile(1 - 0.05 / (2 * m), n - 1)
        out[c] = {"mean_diff": mean, "ci": [mean - half, mean + half], "survives": abs(mean / se) >= crit}
    return out
```

### homework-4 items[1] `log_diff` (6 hidden tests)

- Model solution with the starter's comment lines kept inside the function: **passes**.
- W1. nested keys compared only over the first log's keys: **fails T5**.

```python
def log_diff(log_a, log_b):
    out = []
    for k in set(log_a) | set(log_b):
        if k in ("run", "events"):
            continue
        a, b = log_a.get(k, "<missing>"), log_b.get(k, "<missing>")
        if isinstance(a, dict) and isinstance(b, dict):
            for j in a:
                if a.get(j) != b.get(j, "<missing>"):
                    out.append(k + "." + j)
        elif a != b:
            out.append(k)
    return sorted(out)
```
- W2. top-level keys of the first log only: **fails T4**.

```python
def log_diff(log_a, log_b):
    out = []
    for k in log_a:
        if k in ("run", "events"):
            continue
        a, b = log_a.get(k, "<missing>"), log_b.get(k, "<missing>")
        if isinstance(a, dict) and isinstance(b, dict):
            for j in set(a) | set(b):
                if a.get(j, "<missing>") != b.get(j, "<missing>"):
                    out.append(k + "." + j)
        elif a != b:
            out.append(k)
    return sorted(out)
```
- W3. a missing field read as None, so absent equals None: **SURVIVES** (see homework-4 items[1] note).

```python
def log_diff(log_a, log_b):
    out = []
    for k in set(log_a) | set(log_b):
        if k in ("run", "events"):
            continue
        a, b = log_a.get(k), log_b.get(k)
        if isinstance(a, dict) and isinstance(b, dict):
            for j in set(a) | set(b):
                if a.get(j) != b.get(j):
                    out.append(k + "." + j)
        elif a != b:
            out.append(k)
    return sorted(out)
```
- W4. unsorted output: **fails T3**.

```python
def log_diff(log_a, log_b):
    out = []
    for k in log_b:
        if k in ("run", "events"):
            continue
        a, b = log_a.get(k, "<missing>"), log_b.get(k, "<missing>")
        if isinstance(a, dict) and isinstance(b, dict):
            for j in set(a) | set(b):
                if a.get(j, "<missing>") != b.get(j, "<missing>"):
                    out.append(k + "." + j)
        elif a != b:
            out.append(k)
    for k in log_a:
        if k not in log_b and k not in ("run", "events"):
            out.append(k)
    return out
```

## Fix pass

Counts: 23 fixed, 2 declined, 0 deferred (25 findings: 1 error, 9 warnings, 15 notes; the survivor list and the script notes are counted with the findings they belong to). Validator 0 errors with no `[ai-mutants]` or `[source-ban]` warning on nn-train files; voice scan 0 and 0; number script 505 of 505 (CI runner and direct strict), 0 uncovered; `grade-all.mjs --file <f> --code` 0 failures on all six edited files; playthrough green with and without `--mobile` on l14, l15, l16, homework-4, review-4 and problems-4. Graded answers changed: none (hidden-test expectations are unchanged, two tests added; `wrong[]` bands moved only as listed).

1. nt_ops_l4.py `t_quantile` bracket (note): declined. Not an error in the module as the level uses it (seeds 2 to 12, Bonferroni levels to 0.99999 at most are within $\pm 10^4$ except $n = 2$ at a very deep level), and the module is hashed by the number script and shared by later levels. Raised for the engine owner: widen the bracket or raise when the bound is hit before `ml-int` reuses it.
2. nn-train-seeds.json rewrite reproducibility (note): no change by the finding's own wording. The script compares at $10^{-6}$ and every stated figure is to 4 places or fewer.
3. Script `check_wrongs` and the slips (note): fixed. `lv.slip(...)` now works each of the ten slips from the printed inputs and from the unrounded runs; both routes must land in the slip band and outside the key band.
4. Script `power_n` (note): fixed. Added the exact noncentral-$t$ power (`nct_power`) and a search for the seeds the $t$ test needs: power 0.69 at 7, 9 needed for our pairs, 26 for other batches (24 give 0.77), each recomputed before it is written.
5. l13 quiz[0] margin (note): declined. The finding itself says it is a margin and not a fault ("if the item is edited"); the item is not edited, and 0.0365 is accepted.
6. l14 screens[4] interaction sign (error): fixed. The explain now reads "$I = -0.064 - (-0.121) = 0.057$: positive". I recomputed $(0.022 - 0.086) - (0.084 - 0.205) = +0.0567$. The script checks the screen's text: it must say `= 0.057` and must contain no negative 0.057.
7. l14 screens[7] two sign conventions (warning): fixed. The question asks what adding the wider layer changes, with its sign; byKey `sign` says that is the removal effect, without minus with.
8. l14 screens[4] and [6] ranking on point estimates (warning): fixed. screens[4] ends with "0.121 added to the baseline and 0.058 removed from the full set-up"; screens[6] says layer norm's removal costs more on average, 0.111 against 0.058. Both figures are recomputed in the script.
9. l14 screens[7] means without a spread (note): fixed, "an sd of about 0.01 across the ten seeds". Also screens[8] now defines $L_{ab}$, as the first finding proposed.
10. l15 screens[8] `keep_losses=0` (note): fixed in the prelude (`losses[len(losses) - keep_losses:]`, so 0 keeps none) and test 8 no longer passes `keep_losses=0`, so its expected list and the model solution are unchanged and no mutant's first failing test moves.
11. l15 screens[4] "four steps" (note): fixed, "in four of its steps".
12. l15 screens[3] "as much as" (note): fixed, "nearly as much as a different seed (sd 0.029 against 0.046)".
13. l15 screens[6] first test score chose a change (note): fixed in the prose.
14. l16 ten slip bands (warning): fixed. The five bands of screens[2] and [5] and the rest now use the centres and widths proposed, rechecked against both routes by `lv.slip` (screens[2] sign 3.625 +- 0.012, nosqrt -1.145 +- 0.008, se -3.437 +- 0.008; screens[5] lower -0.03345, z -0.00945, sign 0.00775 each +- 0.0001, nosqrt 0.02006 +- 0.00012; screens[8] sign 2.225 +- 0.012; problems-4 parts[2] sign 4.38 +- 0.025, nosqrt -1.788 +- 0.01, parts[3] z -0.00675 and sign 0.00505 each +- 0.0001). None meets its key band.
15. l16 and problems-4 worked figures that do not follow from the printed inputs (warning): fixed by stating what the printed inputs give and what the unrounded runs give: 0.00569, $-3.62$ and $-3.63$; 0.0129, $-0.0077$ and $-0.0078$; 0.0109 for the screens[8] hint; problems-4 0.00278, $-4.39$ and $-4.37$, upper end $-0.0051$ and $-0.0050$. The keys stay as they were and still accept both.
16. l16 screens[10] "needs 7 seeds" (warning): fixed. The text says the formula asks for 7 and 24, "at so few seeds it runs low: the $t$ test needs about 9 and 26". Recomputed with SciPy `nct`: power 0.691 at 7, 0.830 at 9; 0.774 at 24, 0.809 at 26.
17. l16 screens[11] committee interval (warning): fixed. "on 8 shared seeds and one test period", and "It covers seed noise only: both versions saw one test period, whose own noise (`testing` l11) it leaves out."
18. l16 "on these seeds" readings of an interval (warning): fixed in l16 screens[5] and [7], homework-4 items[7] and problems-4 items[0] parts[4] (option, feedback and explain): the claims are now about new seeds on this split.
19. l16 screens[3] five pairs (note): fixed, "$p = 0.053$: five pairs fall just short where ten were clear" (recomputed 0.0532 on 4 df).
20. l16 screens[6] independence (note): fixed. The explain says tests against one shared baseline are not quite independent, so the true chance is a little lower, and cites `testing` l10 for Bonferroni.
21. review-4 items[7] "four runs" (note): fixed, "Four set-ups of a net, each averaged over the same seeds".
22. homework-4 items[0] Bonferroni count from the configs in the results (warning, surviving wrong solution W1): fixed. New hidden test 9 hands `experiment_report` unasked configs beside the borderline effect (expects `True`, Bonferroni over one change); the slip gives `False`. Added as a `mutant` (test 9). `how` says 9 tests.
23. homework-4 items[0] tests 4 and 8 companions (note): fixed. `nulls(names)` builds four genuine null configs on EDGE's own base, so the "borderline effect among nulls" is one; x's verdict is unchanged.
24. homework-4 items[1] absent versus None (note, surviving wrong solution W3): fixed. Test 7 compares a log with `code` set to `None` against one without it, expecting `['code']`; added as a `mutant` (test 7). `how` says 7 tests.
25. problems-4 items[2] parts[3] (warning): fixed. The question now says the test set was scored after each of the five runs and the run with the best test score was reported.

Surviving wrong solution W1 of `runs_needed` (`int(n) + 1`): declined as the review concluded. It differs from the ceiling only when $n$ is an exact whole number, which needs the two quantiles to give an exact square in floating point. A test built on that would also reject correct variants (`-z(alpha / 2)`) by one unit in the last place.
