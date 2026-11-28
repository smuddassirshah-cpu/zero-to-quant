# info level 1: performance task

- `homework-1.json` item 6 of 8, `h-huffman-code`. Kind `code`, difficulty 5, pace 1500 s.
- Matched objective (l3): "Build a Huffman code and compare its average length with the entropy." The verb "Build" matches the rule, so the task is `code`.
- Product: `huffman_code(probs)` from a one-line stub, returning one bit string per symbol in the order of `probs`; a single symbol gets `["0"]` (stated in the prose).
- 11 hidden tests, 1 example. A hidden postlude defines `_prefix_ok`, `_avg_ok` (against Huffman's average by the sum of merged weights, to 1e-9), `_kraft_ok` and `_bits_ok`. Five distributions: one with ties (0.3, 0.3, 0.2, 0.1, 0.1), one of 8 symbols, one out of order, two symbols, and a single symbol. Tests never compare word lengths, because ties may be broken either way.
- Overlapping screens: l3 screens 5 to 7 and 11 (Huffman's merges and `huffman_lengths`). New in the task: the words themselves (a 0 or 1 put in front at each merge), the single-symbol case and an 8-symbol source.

Gates:
1. Validator: `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. Voice: `VOICE_BASE=app/content/courses/info python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 lesson ids in code spans.
3. Numbers script: `<venv>/bin/python docs/reports/info-L1-numbers.py` exits 0; it runs the model solution on all 12 cases in CPython and checks the starter fails.
4. Playthrough: `node tools/playthrough.mjs --set info/homework-1 --mobile --local-cdn <pkgs>`: passed at 1280 and 440, the starter fails and the solution passes in Pyodide.
