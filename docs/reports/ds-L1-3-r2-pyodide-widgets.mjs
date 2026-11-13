// Round 2 audit of ds L1 to L3: runs every Python code widget under the local Pyodide build.
// Usage, from the repository root:
//   node docs/reports/ds-L1-3-r2-pyodide-widgets.mjs <pkgs dir holding pyodide-0.27.7>
// Prints one line per widget (solution passes all hidden tests, starter fails one) and exits 1 on any problem.
import fs from 'fs';
import path from 'path';
const PK = path.resolve(process.argv[2] || 'pkgs');
const { loadPyodide } = await import(path.join(PK, 'pyodide-0.27.7', 'package', 'pyodide.mjs'));
const DS = path.resolve('app/content/courses/ds') + '/';
const names = fs.readdirSync(DS).filter(f => /^(l([1-9]|1[0-3])-|review-[123]|homework-[123])/.test(f));
const items = [];
for (const f of names) {
  const d = JSON.parse(fs.readFileSync(DS + f));
  for (const k of ['screens', 'quiz', 'items']) (d[k] || []).forEach((it, i) => {
    if (it.widget && it.widget.kind === 'code') items.push({ name: `${f} ${k}[${i}]`, w: it.widget });
  });
}
const py = await loadPyodide();
py.globals.set('ITEMS', JSON.stringify(items));
const out = py.runPython(`
import json, time
def run(w, src):
    ns = {'__learner_source__': src}
    exec(w.get('prelude', ''), ns); exec(src, ns)
    res = []
    for t in w['tests']:
        try:
            if t.get('setup'): exec(t['setup'], ns)
            t0 = time.time()
            ok = eval(t['call'], ns) == eval(t['expect'], ns)
            res.append((ok, time.time() - t0))
        except BaseException:
            res.append((False, 0))
    return res
lines = []
bad = 0
for it in json.loads(ITEMS):
    w = it['w']
    s = run(w, w['solution']); st = run(w, w['starter'])
    okS = all(r[0] for r in s); okT = not all(r[0] for r in st)
    bad += (not okS) + (not okT)
    lines.append('%s: solution %s (slowest %.2fs), starter fails %s' % (it['name'], okS, max(r[1] for r in s), okT))
lines.append('widgets %d, problems %d' % (len(lines), bad))
'\\n'.join(lines)
`);
console.log(out);
process.exit(/problems 0$/.test(out.trim()) ? 0 : 1);
