// Run a reader script in Pyodide 0.27.7 (NumPy 2.0.2, pandas 2.2.3, matplotlib 3.8.4) from the local pkgs folder.
// node pyo12.mjs <pkgs>/pyodide-0.27.7/package <script.py> [package ...]
// The worktree is mounted at /wt, so the script finds the item JSON as it does in CPython.
import path from 'path';
import { fileURLToPath } from 'url';
const [dir, script, ...pkgs] = process.argv.slice(2);
const here = path.dirname(fileURLToPath(import.meta.url));
const wt = path.resolve(here, '../../..');
const { loadPyodide } = await import(path.resolve(dir, 'pyodide.mjs'));
const py = await loadPyodide({ indexURL: path.resolve(dir) + '/' });
py.setStdout({ batched: (s) => console.log(s) });
py.setStderr({ batched: (s) => { if (!/Warning|warn\(/.test(s)) console.error(s); } });
await py.loadPackage(pkgs.length ? pkgs : ['numpy']);
py.FS.mkdirTree('/wt');
py.FS.mount(py.FS.filesystems.NODEFS, { root: wt }, '/wt');
const rel = path.relative(wt, path.resolve(script));
try {
  await py.runPythonAsync(`import runpy, os\nos.chdir('/tmp')\ntry:\n    runpy.run_path('/wt/${rel}', run_name='__main__')\nexcept SystemExit as e:\n    print('exit', e.code)\n`);
} catch (e) { console.error(String(e).slice(-2000)); process.exit(1); }
