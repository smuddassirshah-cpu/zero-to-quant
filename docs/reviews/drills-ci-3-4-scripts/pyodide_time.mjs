/* Time a Python script in Pyodide under node (V8, the engine Chromium uses).
   usage: node pyodide_time.mjs <pkgs>/pyodide-0.27.7/package <script.py>
   The script prints its own timings. */
import fs from 'node:fs';
import path from 'node:path';
const dir = path.resolve(process.argv[2]);
const { loadPyodide } = await import(path.join(dir, 'pyodide.mjs'));
const py = await loadPyodide({ indexURL: dir + '/' });
py.runPython(fs.readFileSync(process.argv[3], 'utf8'));
