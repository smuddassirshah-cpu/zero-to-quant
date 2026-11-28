# Topic 0.8 exam: AI from nothing

File: `app/content/exams/topic-0.8.json` (90 minutes, pass 0.7, 30 items). Scripts: `docs/briefs/exam-0.8-scripts/` (`build.py` route A, `check_numbers.py` route B).

## Result

- Ramp 6, 15, 6, 3 at difficulties 2 to 5 (20, 50, 20, 10%). Pace 4,860 s (81 min); the two code items take 10 minutes each.
- Skills, all ten: ab-models 3, ab-nudge 4, ab-neuron 5, ab-language 5, au-making 3, au-limits 2 (+3 shared), au-asking 2, au-checking 1 (+2 shared), au-risks 2, au-alignment 2.
- Exits: a neuron's output by hand (risk alarm, "at least two of three" bias); a bigram table built from a desk log and sampled; `fit_halving`, a 17-line nudging script with steps 1 to 0.125, and `sample_name`, a letter table with start and end marks.
- Kinds: 9 numeric, 10 choice, 1 multi, 8 parts, 2 Python code with 4 mutants each.

## Gates

- Validator 0 errors; no topic-0.8 warnings besides advisory long sentences.
- Voice scan 35: 0 over 35, 0 lesson ids, 0 doubled words, 0 long explanations.
- `check_numbers.py` (venv): 253 of 253, exit 0, every numeric slip included.
- `grade-all --code`: 0 failures. Playthrough green with and without `--mobile`; screenshots checked.
- `fresh-check`: 0 hits (13 advisory stock phrases).

No registration beyond `manifest.json`, which the validator rewrites.
