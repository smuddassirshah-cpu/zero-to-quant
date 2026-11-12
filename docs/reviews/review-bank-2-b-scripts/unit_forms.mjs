#!/usr/bin/env node
/* What the real numeric parser makes of answers with a unit written around them (plain field, then a per cent field). */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';
const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../app');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; g.ZQ = {}; vm.createContext(g);
vm.runInContext(fs.readFileSync(path.join(APP, 'js/engine/grade.js'), 'utf8'), g);
const G = g.ZQ.grade;
for (const t of ['10 bp', '10bps', '10 basis points', '550 shares', '£1.732m', '1.732m', '1.732 million', '6 pounds', '£6.00', '4 hrs', '4h', '-1.75 %', '-1.75 per cent', '10 per cent', '20p', '55p', '40/9', '£40/9', '4 4/9', '1,190', '£1,288.55', '-24 %', '1.2743 dollars', '$1.2743'])
  console.log(JSON.stringify(t).padEnd(18), String(G.numValue(t, {})).padEnd(22), G.numValue(t, { unit: '%' }));
