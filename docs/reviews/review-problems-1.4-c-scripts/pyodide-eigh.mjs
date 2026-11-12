#!/usr/bin/env node
/* Second read, eigen problems-3 p-crab-sizes part 3: what `np.linalg.eigh` returns for the crab covariance matrix in the app's own
   Python (Pyodide 0.27.7 from the local pkgs folder).

   node docs/reviews/review-problems-1.4-c-scripts/pyodide-eigh.mjs <pkgs>/pyodide-0.27.7/<folder holding pyodide.js> */
import { createRequire } from 'node:module';
import path from 'node:path';

const dir = path.resolve(process.argv[2]);
const require = createRequire(import.meta.url);
const { loadPyodide } = require(path.join(dir, 'pyodide.js'));
const py = await loadPyodide({ indexURL: dir + '/' });
await py.loadPackage('numpy');
console.log(py.runPython(`
import numpy as np
S = np.cov([68, 74, 60, 46, 52], [59, 42, 40, 38, 21])
vals, vecs = np.linalg.eigh(S)
"NumPy " + str(np.__version__) + ": S = " + str(S.tolist()) + ", vals = " + str(vals) + ", vecs = " + str(vecs.round(6).tolist())
`));
