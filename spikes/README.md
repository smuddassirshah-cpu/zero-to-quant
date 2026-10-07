# Platform spikes

Evidence for architecture decisions in `docs/PLAN.md`. Both pages were published as private artifacts and run on the owner's iPhone in the Claude app.

> **Status after the owner's publishing rule (7 October 2026, `docs/PLAN.md` revision 2, section 4.3).** The Artifact publishing tool requires the publishing session to read every file it did not write, and never publishes a file it cannot read. The Artifact therefore publishes only files generated from this repository's own sources, and no third-party code or binary. Both results below stand as measurements. Neither runtime they tested is adopted for the Artifact: Pyodide and MicroPython are third-party binaries. The web app (GitHub Pages or local), which is not published through the Artifact tool, runs Pyodide in its native layout; in the Artifact every Python, SQL and C++ drill hands off to the web app and returns by result code. Spike S1 (`docs/PLAN.md` stage 2, below) checks what the rule now depends on: an import map loading pinned CDN modules on the page and in a module worker, import-map integrity, MathML rendering, and the `db`, `sample` and `user` behaviours.

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

## s1 and s1-dbsize (spike S1, stage 2)

The probe of `docs/PLAN.md` stage 2: 44 checks in four modules, every one recording its raw evidence and answering pass, fail, info, inconclusive, error or skipped. `cdn` (7 checks) loads Preact 11.0.0, `@preact/signals`, `zod/mini`, KaTeX, ts-fsrs and fflate from jsDelivr through an import map with integrity, checks whether a wrong hash is refused, against a control, tries the cdnjs copies, runs a module worker importing by full URL, and loads the Preact 10.29.8 UMD fallback with integrity. `mathml` (7) renders the 40-formula specimen with KaTeX's MathML output, measures native layout from bounding boxes, binds the `TexSlots` sentinels and checks `\htmlData`. `platform` (19) covers the single list of stage 2 (c). `caps` (11) measures `user`, `permissions`, the `db` round trip and rule set (with a canary rule only a declared rule set can produce), a `meta/release` change reaching the open page after a republish, and `sample` (consent, limits, streaming, tiers, abort, page tools). `s1-dbsize` is the separate paced size probe: 192 KiB documents every 2 s up to 60 MiB, then it deletes them.

Every published file is our own code or data; third-party code loads at run time from the CDN. `s1/CONTRACT.md` is the brief every module follows and the publishing runbook. To rebuild and test locally (Node 22, the repository's `npm ci`, Chromium at `/opt/pw-browsers` or `ZQ_CHROMIUM`):

```
cd spikes/s1
node tools/fetch-npm.mjs      # the eight pinned tarballs, each checked against the registry's SHA-512
node tools/build.mjs --strict # dist/v1, dist/v2, dist/v3, dist/dbsize and dist/manifest.json
node tools/test.mjs           # 109 expectations against a fake window.claude, the CDN served from npm/
```

The build is deterministic: `dist/manifest.json` must equal the committed `s1/manifest.json` (SHA-256 `f7ea81f7...`), the ledger of what was published.

Published 7 October 2026 by the stage 2 session, from files it read in full: the probe at https://claude.ai/artifact/KfYB1yPs9DfKTakjZZrGFD (version `1791402675-43ad`; `db` with the six rules of `manifest.json`, `user` with the `profile` scope, `sample`) and the size probe at https://claude.ai/artifact/DF7mBFRaKCWkrXp14eRgXs (version `1791402685-14db`; `db`). Results on the owner's iPhone: pending; they go in `docs/DECISIONS.md` section 4.
