// Full view of the widgets behind one tag, with their holders' question, feedback and explain. node ext2.mjs <tag> [substring]
import fs from 'fs';
import { scan, at, upPath, prop, toJS } from './jsonscan.mjs';
const tag = process.argv[2], sub = process.argv[3] || '';
const lines = fs.readFileSync(process.argv[4] || '/tmp/v2.txt', 'utf8').split('\n').filter(l => l.includes('[' + tag + ']') && l.includes(sub));
for (const l of lines) {
  const m = l.match(/^warning (\S+)\s+(\S+): \[/); if (!m) continue;
  const text = fs.readFileSync(m[1], 'utf8'), root = scan(text);
  const w = toJS(text, at(root, m[2]));
  const holder = toJS(text, at(root, upPath(m[2])));
  console.log('=== ' + m[1].replace('content/', '') + ' ' + m[2]);
  console.log(' Q:', String(holder.question || '').replace(/\s+/g, ' ').slice(0, 300));
  console.log(' W:', JSON.stringify({ answer: w.answer, tol: w.tol, unit: w.unit, accept: w.accept, wrong: (w.wrong || []).map(x => `${x.id}=${x.value}+-${JSON.stringify(x.tol)}`) }));
  console.log(' F:', JSON.stringify(holder.feedback?.correct || '').slice(0, 300));
  console.log(' E:', JSON.stringify(holder.explain?.text || '').slice(0, 450));
}
