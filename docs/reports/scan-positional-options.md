# Scan: positional options, key length, uniform multi keys

Engine item 585 (validator warnings `[shuffled-position]`, `[key-length]`, `[multi-keys-uniform]`). Content not fixed. Counts from `node tools/validate.mjs`.

## [shuffled-position]: 14 hits

By folder: exams 1, homework 4, lesson 8, review 1

By course (or exam/bank folder):

- eigen: 2
- recruiting: 2
- algo-think: 1
- alpha: 1
- analysis: 1
- coding-int: 1
- convex: 1
- exams: 1
- git: 1
- mm-games: 1
- puzzles: 1
- py-found: 1

Full hit list:

- `content/courses/recruiting/l8-why-this-firm.json` `screens[1].widget.options[3].why`: "answer A"
- `content/courses/recruiting/l9-sitting-an-assessment.json` `screens[11].widget.options[1].why`: "top choice"
- `content/courses/py-found/l9-splitting-files.json` `quiz[1].feedback.generic`: "top one"
- `content/courses/git/l3-staging-area.json` `quiz[2].explain.text`: "top one"
- `content/courses/eigen/homework-4.json` `items[2].explain.text`: "(a)"
- `content/courses/eigen/homework-4.json` `items[2].feedback.correct`: "(a)"
- `content/courses/algo-think/l6-call-stack.json` `screens[4].hints[1].text`: "the one above"
- `content/courses/analysis/review-3.json` `items[5].explain.text`: "second option"
- `content/courses/alpha/l3-including-the-dead.json` `screens[10].hints[2].text`: "first option"
- `content/courses/convex/l4-recognising-convex-problems.json` `screens[2].feedback.correct`: "(c)"
- `content/courses/puzzles/homework-5.json` `items[4].widget.options[1].why`: "last answer"
- `content/courses/mm-games/l12-thinking-aloud.json` `screens[3].hints[2].text`: "first answer"
- `content/courses/coding-int/homework-4.json` `items[0].parts[1].widget.options[3].why`: "first answer"
- `content/exams/topic-0.7.json` `items[12].explain.text`: "second answer"

## [key-length]: 1658 hits

By folder: exams 16, homework 78, lesson 1393, review 171

By course (or exam/bank folder):

- analysis: 103
- momentum-rep: 63
- recruiting: 61
- stat-models: 61
- cpp: 56
- validation: 55
- coint: 52
- pairs-rep: 51
- alpha: 48
- linear-maps: 48
- convex: 45
- topology: 45
- opt-dash: 43
- contests: 41
- ensembles: 41
- backtest: 40
- garch: 37
- fin-ml: 36
- stat-learning: 36
- arma: 35
- numerics: 32
- algebra: 31
- pytest: 27
- cpp-pricing: 26
- plotting: 25
- trees: 22
- complex: 21
- micro: 21
- regression: 20
- algo-think: 18
- graphs-dp: 18
- limits: 18
- vector-calc: 18
- conditional: 17
- exams: 16
- git: 16
- ds: 15
- puzzles: 15
- py-found: 15
- terminal: 15
- functions: 14
- markov: 13
- odes: 13
- proof: 13
- eigen: 12
- multivar: 11
- random-vars: 11
- testing: 11
- first-python: 10
- integrals: 10
- mm-games: 10
- game-theory: 9
- sql: 9
- mental-pressure: 8
- numpy-pandas: 8
- taylor: 8
- estimation: 7
- least-squares: 7
- vectors: 7
- elimination: 6
- limits-thm: 6
- markets: 6
- quadratics: 6
- series: 6
- brainteasers: 5
- options: 5
- trig: 5
- equations: 4
- exp-log: 4
- counting-chance: 3
- number-sense: 3
- counting: 2
- mental: 1
- pdes: 1
- ratio: 1

## [multi-keys-uniform]: 0 hits

None.

## Fix pass

Shuffled-position: 14 hits, 6 fixed, 8 false positives (hits now 8, all listed below).

Fixed (named by content):

- `eigen/homework-4` `items[2].explain.text` and `items[2].feedback.correct`: "(a)", "(c)" now name the matrices by diagonal. Traces and determinants recomputed: (-3, 2), (-4, 5), det -8, det -1, trace 0.
- `analysis/review-3` `items[5].explain.text`: "the second option" now "comparison with $\sum |a_n|$".
- `alpha/l3-including-the-dead` `screens[10].hints[2].text`: "The first option" now "The sentence on delisted shares".
- `mm-games/l12-thinking-aloud` `screens[3].hints[2].text`: "The first answer" now "The answer that averages 3.5 per die".
- `exams/topic-0.7` `items[12].explain.text`: "The second answer" now "The answer about fast decisions".

False positives (no change):

- `recruiting/l8-why-this-firm` `screens[1].widget.options[3].why`: "answer A" is row A of the table on the previous screen.
- `recruiting/l9-sitting-an-assessment` `screens[11].widget.options[1].why`: "top choice" is the table label "Firm A, top choice".
- `py-found/l9-splitting-files` `quiz[1].feedback.generic`: "the top one" is the top pair of the count.
- `git/l3-staging-area` `quiz[2].explain.text`: "the top one" is the file in the top folder.
- `algo-think/l6-call-stack` `screens[4].hints[1].text`: "the one above" is the frame above in the call stack.
- `convex/l4-recognising-convex-problems` `screens[2].feedback.correct`: "(c)" is problem (c) in the table, not an option.
- `puzzles/homework-5` `items[4].widget.options[1].why`: "the last answer" is the answer to the previous puzzle.
- `coding-int/homework-4` `items[0].parts[1].widget.options[3].why`: "the first answer" is the result of the first call.
