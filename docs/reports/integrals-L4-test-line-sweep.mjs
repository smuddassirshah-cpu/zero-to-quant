/* Audit integrals-4: feedback-line sweep of l16 screens[4] (midpoint) under the page Pyodide.
   Run from anywhere: node docs/reports/integrals-L4-test-line-sweep.mjs <absolute path to app> <local cdn pkgs>
   Prints, per submission, the key the page would give and pass (P), fail (F) or error (E) per hidden test. */
import fs from 'node:fs';
const root = process.argv[2], pkgs = process.argv[3];
const { makeRunner } = await import(root + '/tools/code-runner.mjs');
const d = JSON.parse(fs.readFileSync(root + '/content/courses/integrals/l16-infinite-height.json', 'utf8'));
const spec = d.screens[4].widget;
const head = 'import math\n\ndef midpoint(f, a, b, n):\n    h = (b - a) / n\n    total = 0.0\n';
const V = {
  solution: spec.solution, starter: spec.starter,
  left: head + '    for i in range(n):\n        total += f(a + i * h)\n    return h * total\n',
  right: head + '    for i in range(n):\n        total += f(a + (i + 1) * h)\n    return h * total\n',
  trapezium: head + '    for i in range(n):\n        total += (f(a + i * h) + f(a + (i + 1) * h)) / 2\n    return h * total\n',
  avg_ends_then_f: head + '    for i in range(n):\n        total += f((a + i * h + a + (i + 1) * h) / 2)\n    return h * total\n',
  range1n: head + '    for i in range(1, n + 1):\n        total += f(a + (i + 0.5) * h)\n    return h * total\n',
  range1n_minus_half: head + '    for i in range(1, n + 1):\n        total += f(a + (i - 0.5) * h)\n    return h * total\n',
  half_h_offset_only: head + '    for i in range(n):\n        total += f(i * h + h / 2)\n    return h * total\n',
  no_h: head + '    for i in range(n):\n        total += f(a + (i + 0.5) * h)\n    return total\n',
  int_div: 'import math\n\ndef midpoint(f, a, b, n):\n    h = (b - a) // n\n    total = 0.0\n    for i in range(n):\n        total += f(a + (i + 0.5) * h)\n    return h * total\n',
  simpson: head + '    for i in range(n):\n        l = a + i*h; r = l + h\n        total += (f(l) + 4*f((l+r)/2) + f(r)) / 6\n    return h * total\n',
  guard_left: head + '    for i in range(n):\n        x = a + i * h\n        if x == 0: x = 1e-12\n        total += f(x)\n    return h * total\n',
  syntax_error: head + '    for i in range(n)\n        total += f(a + (i + 0.5) * h)\n    return h * total\n',
};
const r = makeRunner({ pkgs, root, jobs: 1 });
for (const [k, src] of Object.entries(V)) {
  const g = await r.grade(spec, src, 'tests');
  console.log(k.padEnd(22), 'ok=' + g.ok, 'key=' + g.key, (g.rows || []).map((x) => (x.ok ? 'P' : x.error ? 'E' : 'F')).join(''), g.error ? String(g.error).split('\n').pop().slice(0, 80) : '');
}
await r.close();
