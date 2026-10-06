# Platform spikes

Evidence for architecture decisions in `docs/PLAN.md`. Both pages were published as private artifacts and run on the owner's iPhone in the Claude app.

## artifact-probe

Checks WebAssembly (page and worker), fetching published `.json` and `.wasm` files, classic and blob workers, MicroPython with `ulab`, browser storage, service workers, and the `sample`, `db` and `user` capabilities.

Result, 6 October 2026, iPhone (iOS 18.7, Claude app): every check passed except service workers, which are absent. The AI tutor capability answered on the quick tier; page tools up to 16; no image input in that view.

## pyodide-in-artifact

The artifact host does not serve archives, and Pyodide expects its standard library and package wheels as zip files. `build.py` splits each archive into the types the host serves: text files into one JSON map per archive, WebAssembly side modules (`.so`) into `.wasm` files, and small binary data files (time-zone tables) as base64 inside the JSON map, the way a `data:` URI embeds an asset. `zq-py-worker.js` (a module worker) intercepts Pyodide's own requests for those archives and reassembles them in memory with a store-only zip writer, so Pyodide loads unchanged.

Inputs: the `pyodide` npm package (core) and the NumPy, pandas, python-dateutil, pytz and six wheels from the Pyodide 314.0.7 release on GitHub. Output: 69 files, 49 MB raw, about 13 MB gzipped.

Result in Chromium: Python 3.14.2 ready in 3.0 s, NumPy 2.4.6 and pandas 3.0.2 loaded by 8.5 s, drawdown computed correctly.

Result on the owner's iPhone (iOS 18.7, Claude app, 6 October 2026): Python 3.14.2 ready at 2.8 s, NumPy and pandas loaded at 5.1 s, the calculation done at 6.2 s, drawdown 0.25 correct. Full Python runs inside the artifact.
