# Topic 3.1 exam: research papers

File: `app/content/exams/topic-3.1.json` (90 minutes, pass 0.7, 30 items, all nine skills of `momentum-rep` and `pairs-rep`). Scripts: `docs/briefs/exam-3.1-scripts/` (`build.py` route A, `check_numbers.py` route B, `fresh.py`).

## Result

- Ramp 6, 15, 6, 3 at difficulties 2 to 5; pace 4,605 s (77 min).
- By course and level: momentum-rep L1 5, L2 5, L3 5; pairs-rep L1 5, L2 5, L3 5 (l11 to l14).
- Coverage: every level has an item on a skill first met there, except pairs-rep L3. That level has no new skill, so it is covered through `pr-extend` and `pr-method`.
- Kinds: 13 numeric, 9 parts, 3 choice, 2 multi, 2 Python code, 1 longform (self-marked; every skill is also on an auto item).

## Gates

- Validator: 0 errors, no topic-3.1 warnings.
- Voice scan on a copy: 0 and 0.
- `check_numbers.py`: 244 of 244, exit 0. It covers every key, every `wrong`, every number in the prose and `check_wrongs`. Both code solutions pass in CPython, and both starters fail.
- Playthrough with `--local-cdn`: green with and without `--mobile`; screenshots checked.

## Freshness

Two clashes were changed: the survival inputs (37.5% was a pairs-rep l14 key) and the 16-cell chance (0.56 is in testing l9). Other hits are data arrays or unrelated.
