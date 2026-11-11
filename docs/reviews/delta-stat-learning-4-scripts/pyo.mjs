// Delta read, stat-learning L4: run one of this folder's Python files inside the local Pyodide 0.27.7 build
// (the app's runtime), with the level's seven content files copied to /content.
// Usage (from the repo root): node docs/reviews/delta-stat-learning-4-scripts/pyo.mjs <scratchpad>/pkgs <file.py> [args]
import { pathToFileURL, fileURLToPath } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';
const here = path.dirname(fileURLToPath(import.meta.url));
const dir = path.join(process.argv[2], 'pyodide-0.27.7', 'package') + path.sep;
const { loadPyodide } = await import(pathToFileURL(dir + 'pyodide.mjs').href);
const py = await loadPyodide({ indexURL: dir });
await py.loadPackage(['numpy', 'scipy', 'scikit-learn'], { messageCallback: () => {} });
const src = path.join(here, '..', '..', '..', 'app', 'content', 'courses', 'stat-learning');
py.FS.mkdir('/content');
for (const f of fs.readdirSync(src)) if (/^(l1[5-9]-.*|review-4|homework-4)\.json$/.test(f)) py.FS.writeFile('/content/' + f, fs.readFileSync(path.join(src, f)));
const code = fs.readFileSync(path.join(here, process.argv[3]), 'utf8');
py.globals.set('ARGV', py.toPy([process.argv[3], '/content', ...process.argv.slice(4)]));
py.runPython('import sys\nsys.argv = list(ARGV)\n__name__ = "pyodide"');
py.runPython(code);
