# Data for the AI strand: sources, licences and credit lines

Lessons name these files in a `code` or `trainer` widget's `data` map (`"names.txt": "content/data/ai/names.txt"`). The validator allows a data file up to 256 KB, so Tiny Shakespeare is a slice.

| File | What | Size | Licence | Credit line |
| --- | --- | --- | --- | --- |
| `names.txt` | 32,032 first names, one per line, lower case (the most common names in the US Social Security Administration's 2018 baby-names data) | 228,145 bytes | MIT, `LICENSE` of the makemore repository (Copyright (c) 2022 Andrej Karpathy), checked at https://github.com/karpathy/makemore | "Names list from Andrej Karpathy's makemore (MIT licence), drawn from US Social Security Administration baby-name data." |
| `tiny-shakespeare.txt` | The first 250,000 characters of Tiny Shakespeare (full text 1,115,394 characters, 65 distinct characters). The slice has 62 of the 65: it lacks `$`, `3` and `X`. All ASCII. Its vocabulary of 65 is taken from the full text: `tiny-shakespeare-vocab.json` lists them (sorted; newline is the JSON string `"\n"`), so a model sized for 65 matches the published figures | 250,000 bytes | The text is Shakespeare's, public domain. The file is the start of the char-rnn `data/tinyshakespeare/input.txt`. No licence file of the char-rnn repository could be read from the build sandbox (its API was blocked and `LICENSE` paths returned 404), so only the public-domain status of the text is asserted here, not the compilation's licence. | "Tiny Shakespeare, the text as distributed with Andrej Karpathy's char-rnn (first 250,000 characters); Shakespeare's plays are in the public domain." |

## Digits (not a file here)

`sklearn.datasets.load_digits()` ships inside the scikit-learn wheel, so it works offline in Pyodide (checked on scikit-learn 1.6.1: 1,797 samples of 8 by 8 images, `data.shape == (1797, 64)`; `import sklearn.datasets` takes about 3.6 s once, `load_digits()` 11 to 28 ms; `docs/reports/ai-timing-spike.md`). No data file is needed.

Licence: the UCI Machine Learning Repository's "Optical Recognition of Handwritten Digits" data set (the test set of NIST-derived preprocessed digits by E. Alpaydin and C. Kaynak), released under CC BY 4.0. Credit line: "Digits data: Alpaydin, E. and Kaynak, C., Optical Recognition of Handwritten Digits, UCI Machine Learning Repository, CC BY 4.0, as bundled with scikit-learn."

Put the credit line of every data set a lesson uses in that lesson's closing prose or a `how` line; the courses' voice rules apply (British English, no em-dashes).
