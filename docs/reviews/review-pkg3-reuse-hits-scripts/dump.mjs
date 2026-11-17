// Side-by-side dump of the unwaived reuse hits. Run from app/:
//   node tools/same-course-reuse.mjs --all --all-exams --json > hits.json
//   node ../docs/reviews/review-pkg3-reuse-hits-scripts/dump.mjs hits.json [chars] [n,n,...] [full]
import fs from 'fs';
const h = JSON.parse(fs.readFileSync(process.argv[2]));
const lim = +process.argv[3] || 500; const only = process.argv[4]; const full = process.argv[5];
const get = (o, p) => p.split(/[.\[\]]+/).filter(Boolean).reduce((a, k) => a?.[k], o);
const ans = (w) => !w ? '' : w.kind === 'numeric' ? `num ${w.answer} tol=${JSON.stringify(w.tol)} wrong=${(w.wrong || []).map((x) => x.id + ':' + x.value).join(',')}` : w.options ? w.kind + ' ' + w.options.map((o) => (o.correct ? '*' : '') + o.text).join(' | ') : w.kind + ' ' + JSON.stringify(w).slice(0, 200);
const t = (s) => String(s ?? '').replace(/\s+/g, ' ').slice(0, lim);
let n = 0;
for (const x of h) {
  if (process.env.WAIVED ? !x.waived : x.waived) continue; n++;
  if (only && only !== 'all' && !only.split(',').includes(String(n))) continue;
  const d = JSON.parse(fs.readFileSync('content/' + x.file)); const it = get(d, x.item);
  console.log(`\n=== #${n} [${x.tag || 'gate'}/${x.kind}] ${x.file} ${it.id} part ${x.part} <- ${x.source} ${x.sourceId || ''}\n  EV: ${t(x.evidence)}`);
  console.log('  PS prose:', t(it.prose));
  const ps = x.part && !full ? [it.parts[x.part - 1]] : it.parts;
  for (const p of ps) console.log('  PS Q:', t(p.question), '\n  PS A:', t(ans(p.widget)), '\n  PS X:', t(p.explain?.text || p.feedback?.correct));
  const [sf, sp] = [x.source.split(':')[0], x.source.slice(x.source.indexOf(':') + 1)];
  const sd = JSON.parse(fs.readFileSync('content/' + sf)); const s = get(sd, sp) || {};
  console.log('  SRC:', t(s.title), '|', t(s.prose || s.text || s.body), '| Q:', t(s.question || s.prompt), '\n  SRC A:', t(ans(s.widget)), '\n  SRC X:', t(s.explain?.text || s.feedback?.correct));
  if (s.parts) for (const p of s.parts) console.log('   SRC part Q:', t(p.question), 'A:', t(ans(p.widget)));
  if (full || (!s.question && !s.prose && !s.parts)) console.log('  SRC raw:', JSON.stringify(s).slice(0, lim * 6));
}
console.log('unwaived', n);
