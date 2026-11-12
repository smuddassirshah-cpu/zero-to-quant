// Lists the widgets behind one validator tag: node ext.mjs <tag> (run from app/, reads /tmp/v.txt)
import fs from 'fs';
const tag = process.argv[2];
const lines = fs.readFileSync('/tmp/v.txt', 'utf8').split('\n').filter(l => l.includes('[' + tag + ']'));
let n = 0;
for (const l of lines) {
  const m = l.match(/^warning (\S+)\s+(\S+): \[/);
  if (!m) continue;
  const [, f, p] = m;
  const j = JSON.parse(fs.readFileSync(f, 'utf8'));
  let o = j, parent = null;
  const toks = [...p.matchAll(/([A-Za-z_]+)|\[(\d+)\]/g)];
  const path = [];
  for (const t of toks) { path.push(o); o = t[1] !== undefined ? o?.[t[1]] : o?.[+t[2]]; }
  const w = o;
  // question: nearest ancestor with a question field
  let q = '';
  for (let i = path.length - 1; i >= 0; i--) { const a = path[i]; if (a && typeof a === 'object' && a.question) { q = a.question; break; } if (a && a.prompt) { q = a.prompt; break; } }
  if (w && w.question) q = w.question;
  console.log(`=== #${++n} ${f.replace('content/', '')} ${p}`);
  console.log(' Q:', String(q).replace(/\s+/g, ' ').slice(0, 420));
  console.log(' ', JSON.stringify({ answer: w?.answer, tol: w?.tol, unit: w?.unit, label: w?.label, wrong: w?.wrong?.map(x => `${x.id}=${x.value}`) }));
}
