// Shows a widget with its holder's question, wrong entries, byKey lines. node showD.mjs <file> <path>
import fs from 'fs';
import { scan, at, upPath, toJS } from './jsonscan.mjs';
const [, , f, p] = process.argv;
const text = fs.readFileSync(f, 'utf8'), root = scan(text);
const w = toJS(text, at(root, p)), h = toJS(text, at(root, upPath(p)));
console.log('Q:', String(h.question || '').replace(/\s+/g, ' ').slice(0, 300));
console.log('prose:', String(h.prose || '').replace(/\s+/g, ' ').slice(0, 300));
console.log('W:', JSON.stringify({ kind: w.kind, answer: w.answer, tol: w.tol, unit: w.unit, accept: w.accept, form: w.form }));
for (const x of w.wrong || []) console.log(' wrong', JSON.stringify(x), '\n   byKey:', JSON.stringify(h.feedback?.byKey?.[x.id]));
console.log('F.correct:', JSON.stringify(h.feedback?.correct), '\nE:', JSON.stringify(h.explain?.text || '').slice(0, 500));
