# stat-learning level 4: performance task

- File `app/content/courses/stat-learning/homework-4.json`, item `h-kmeans`, index 6 (item 7 of 9). Kind `code` (Python, NumPy), difficulty 4, skill `sl-setup`, pace 1200 s, written with the level (no conversion).
- Objective matched (l17, verb rule "Build"): "Build a network with one hidden layer, follow one gradient step, and fit one with scikit-learn." The brief names k-means as the level's task, so the product proves l16's objective "Cluster data with $k$-means and with hierarchical clustering, and choose the number of groups" from a blank stub.
- Product: `kmeans(X, k, init, max_iter)`: the assign and update loop, the stop when an assignment repeats, the `max_iter` cap, an empty centre kept in place, ties to the lower index; returns labels, centres to 4 places and the inertia.
- Tests: 10 hidden, 1 example. The six shares from two starts (64; 58), one assignment only (25.6, 587.2), an empty centre (1, 10, 100; 2), a tie at 11, a 2-D point where Euclidean and Manhattan distance disagree, and the 60 scaled shares of `make_stocks(11)` from two starts, checked against `KMeans(init=<same rows>, n_init=1)` (inertia 14.1574). Nine planted slips each fail at least one test: no empty guard, one round, `max_iter` ignored, median, inertia about the old centres, plain distance in the inertia, ties upwards, Manhattan assignment, centres from before the last update.
- Overlapping screens: l16 screens[0] to [3] run the two steps by hand on the six shares; l16 screens[4] codes one step, `kmeans_step`, with the empty-centre and tie rules stated; review-4 `r-kmeans-2d` does one step in 2-D. New: the loop, the stopping rule, the `max_iter` cap, and agreement with scikit-learn from given starts.

## Gates

1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors. stat-learning L4 is a new level, not on `perf-pending.json`.
2. Voice, `VOICE_BASE=app/content/courses/stat-learning python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 explanations over three sentences.
3. Numbers script, `<venv>/bin/python docs/reports/stat-learning-4-perf-numbers.py`: exit 0. Fractions for 64, 58, 25.6 and 587.2; a hand loop for the empty centre; scikit-learn for 14.1574; solution 10 of 10, starter 0 of 10, every planted slip fails.
4. Playthrough, `node tools/playthrough.mjs --set stat-learning/homework-4 --local-cdn <pkgs>`, with and without `--mobile` (and `--tablet`): All passed, "1 performance starter fail". Shots read at 440 px.

Freshness: `node tools/fresh-check.mjs --file content/courses/stat-learning/homework-4.json`: 0 hits. Grep terms: `kmeans`, `kmeans_step`, `inertia`, `max_iter`, `n_init`, `25.6`, `587.2`, `14.16`. Backlog: no bullet for this item.
