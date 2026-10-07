# Platform spikes

Evidence for architecture decisions in `docs/PLAN.md`. Both pages were published as private artifacts and run on the owner's iPhone in the Claude app.

> **Status after the owner's publishing rule (7 October 2026, `docs/PLAN.md` revision 2, section 4.3).** The Artifact publishing tool requires the publishing session to read every file it did not write, and never publishes a file it cannot read. The Artifact therefore publishes only files generated from this repository's own sources, and no third-party code or binary. Both results below stand as measurements. Neither runtime they tested is adopted for the Artifact: Pyodide and MicroPython are third-party binaries. The web app (GitHub Pages or local), which is not published through the Artifact tool, runs Pyodide in its native layout; in the Artifact every Python, SQL and C++ drill hands off to the web app and returns by result code. The next spike, S1 (`docs/PLAN.md` stage 2), checks what the rule now depends on: an import map loading pinned CDN modules on the page and in a module worker, import-map integrity, MathML rendering, and the `db`, `sample` and `user` behaviours.

## artifact-probe

Checks WebAssembly (page and worker), fetching published `.json` and `.wasm` files, classic and blob workers, MicroPython with `ulab`, browser storage, service workers, and the `sample`, `db` and `user` capabilities.

Result, 6 October 2026, iPhone (iOS 18.7, Claude app): every check passed except service workers, which are absent. The AI tutor capability answered on the quick tier; page tools up to 16; no image input in that view.

Status: the capability, storage and worker results are used by the plan. The WebAssembly and MicroPython results are a record only: under the publishing rule the Artifact publishes no `.wasm` and no MicroPython build.

## pyodide-in-artifact

**Measured; not adopted.** The layout below ran Pyodide inside an Artifact, but it publishes Pyodide's own binaries and repackaged wheel contents, which the publishing rule excludes. Draft 1 of `docs/PLAN.md` had refined it into JSON parts of each wheel's compressed members (`docs/ARCHITECTURE.md` 6.3.3, also kept as a record, and `tools/pysplit`, now removed).

The artifact host does not serve archives, and Pyodide expects its standard library and package wheels as zip files. `build.py` splits each archive into the types the host serves: text files into one JSON map per archive, WebAssembly side modules (`.so`) into `.wasm` files, and small binary data files (time-zone tables) as base64 inside the JSON map, the way a `data:` URI embeds an asset. `zq-py-worker.js` (a module worker) intercepts Pyodide's own requests for those archives and reassembles them in memory with a store-only zip writer, so Pyodide loads unchanged.

Inputs: the `pyodide` npm package (core) and the NumPy, pandas, python-dateutil, pytz and six wheels from the Pyodide 314.0.7 release on GitHub. Output: 69 files, 49 MB raw, about 13 MB gzipped.

Result in Chromium: Python 3.14.2 ready in 3.0 s, NumPy 2.4.6 and pandas 3.0.2 loaded by 8.5 s, drawdown computed correctly.

Result on the owner's iPhone (iOS 18.7, Claude app, 6 October 2026): Python 3.14.2 ready at 2.8 s, NumPy and pandas loaded at 5.1 s, the calculation done at 6.2 s, drawdown 0.25 correct. Full Python ran inside the artifact. The timings remain the plan's reference for Pyodide on that phone; the web app's timings are measured again at `docs/PLAN.md` stage 25.
