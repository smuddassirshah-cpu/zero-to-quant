#!/usr/bin/env node
/* Second read, ratio problems-1 to -3: what the engine's own grader does with each typed part.
   Loads app/js/engine/grade.js and calls numGrade (the call numeric.js makes). For each of the 46 numeric parts:
     the key grades correct, also with one more place, after a letter and "=", with a true minus sign and with its unit;
     the `accept` text (the form the part shows as accepted) grades correct;
     every wrong[] is refused on its own key and has a byKey line;
   then the reader's own strings (ROWS): T accepted, F refused on no wrong line, a wrong id = refused on that line,
   N = not read as a number (Check stays unavailable). A row with a note is one the reader holds to be a fault
   (FINDING, not a failure): the row states what the reader thinks should happen, and the engine does otherwise.

   node docs/reviews/review-problems-ratio-1-3-scripts/grade-probe.mjs [--all]      (from the repo root) */
import fs from 'node:fs';
import vm from 'node:vm';

const ALL = process.argv.includes('--all');
const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
g.window = g; g.globalThis = g; vm.createContext(g);
g.ZQ = { widgets: { register() {}, shuffle: (a) => a } };
vm.runInContext(fs.readFileSync('app/js/engine/grade.js', 'utf8'), g);
const G = g.ZQ.grade;
const num = (w, t) => { const r = G.numGrade(w, t); return { ok: !!r.ok, key: r.key || (r.detail && r.detail.value == null ? 'NOPARSE' : null) }; };

const T = true, F = false, N = 'NOPARSE';
const EDGE = 'the slip, rounded as the part asks, misses its own line';
const ROUTE = 'the change worked from the rounded price of the part before is refused';
const CUR = 'the answer with its currency written is not read';
const ROWS = {
  1: {
    'p-pension-split': {
      1: [['37.5', T], ['37.5%', T], ['37.50', T], ['3/8', 'decimal'], ['0.375', 'decimal'], ['266.67', 'upside-down'], ['266.7', 'upside-down'], ['38', F], ['37', F], ['62.5', F]],
      2: [['3600', T], ['3,600', T], ['£3,600', T], ['3600.00', T], ['6000', 'bonds'], ['360', 'tenth'], ['36000', 'ten-times'], ['3599', F], ['1200', F]],
      3: [['4140', T], ['4,140.00', T], ['5400', 'multiplier-1-5'], ['540', 'rise-only'], ['6900', 'bonds'], ['3060', F], ['4104', F]],
      4: [['5760', T], ['5,760', T], ['6240', 'rise'], ['240', 'fall-only'], ['3600', 'multiplier-0-6'], ['5670', F]],
      5: [['41.8', T], ['41.82', T], ['41.818', T], ['41.8%', T], ['42', F], ['41.9', T], ['41.7', F], ['43.1', 'old-total'], ['43.125', 'old-total'], ['43.13', 'old-total'], ['37.5', 'unchanged'], ['71.9', 'bonds-base'], ['71.875', 'bonds-base'], ['58.2', F], ['0.418', F]],
    },
    'p-platform-fee': {
      1: [['0.0035', T], ['.0035', T], ['0.00350', T], ['7/2000', T], ['0.035', 'one-place'], ['0.35', 'no-move'], ['35', 'times-100'], ['0.0035%', F], ['0.004', F], ['0.00035', F]],
      2: [['29.40', T], ['29.4', T], ['£29.40', T], ['29.39', T], ['29', F], ['294', 'one-place'], ['2940', 'no-move'], ['42', 'half-only'], ['2.94', F]],
      3: [['8370.60', T], ['8,370.60', T], ['8370.6', T], ['8429.40', 'added'], ['8106', 'one-place'], ['29.40', 'fee-only'], ['8371', F], ['5460', F]],
      4: [['82', T], ['81.6', T], ['81.63', T], ['82%', T], ['81', T], ['83', F], ['80', F], ['122', 'upside-down', EDGE], ['123', 'upside-down', EDGE], ['122.5', 'upside-down'], ['8', 'one-place', EDGE], ['8.2', 'one-place'], ['8.16', 'one-place'], ['0.29', 'account-base'], ['0.3', 'account-base'], ['0.82', F], ['18', F]],
    },
    'p-phone-rise': {
      1: [['0.071', T], ['.071', T], ['0.0710', T], ['0.71', 'one-place'], ['7.1', 'no-move'], ['7.1%', T], ['0.07', F], ['1.071', F], ['0.0071', F]],
      2: [['1.071', T], ['1.0710', T], ['0.929', 'fall'], ['0.071', 'rise-only'], ['1.71', 'one-place'], ['107.1%', T], ['1.07', F], ['107.1', F]],
      3: [['32.13', T], ['£32.13', T], ['32.130', T], ['2.13', 'rise-only'], ['51.30', 'one-place'], ['27.87', 'fall'], ['32.10', F], ['32', F], ['31.17', F]],
      4: [['37.3', T], ['37.35', T], ['37.348', T], ['37.4', T], ['37', F], ['40', 'old-price'], ['40.0', 'old-price'], ['267.75', 'upside-down'], ['267.8', 'upside-down', EDGE], ['267.7', 'upside-down', EDGE], ['62.7', 'saving', EDGE], ['62.65', 'saving'], ['62.6', 'saving', EDGE], ['0.373', F]],
    },
    'p-savings-tax': {
      1: [['828', T], ['828.00', T], ['£828', T], ['82.8', 'tenth'], ['82.80', 'tenth'], ['8280', 'ten-times'], ['8,280', 'ten-times'], ['720', F], ['18828', F]],
      2: [['131.20', T], ['131.2', T], ['£131.20', T], ['331.20', 'all-taxed'], ['200', 'allowance-taxed'], ['196.80', 'kept'], ['131', F], ['328', F]],
      3: [['3.87', T], ['3.871', T], ['3.8711', T], ['3.87%', T], ['3.88', T], ['3.86', F], ['3.9', F], ['4.6', 'gross'], ['4.60', 'gross'], ['2.76', 'all-taxed'], ['0.73', 'tax-share'], ['0.729', 'tax-share'], ['0.0387', F], ['696.80', F]],
    },
  },
  2: {
    'p-share-week': {
      1: [['16', T], ['16%', T], ['16.0', T], ['16.00', T], ['13.79', 'new-base'], ['13.8', 'new-base'], ['11.6', 'pounds'], ['11.60', 'pounds'], ['0.16', F], ['116', F], ['14', F]],
      2: [['70.64', T], ['£70.64', T], ['70.644', T], ['70.65', T], ['72.50', 'cancel'], ['68.10', 'pounds'], ['97.56', 'rise'], ['97.556', 'rise'], ['70.6', F], ['71', F], ['60.90', F]],
      3: [['-2.56', T], ['−2.56', T], ['-2.56%', T], ['-2.560', T], ['2.56', 'sign'], ['0', 'cancel'], ['-2.63', 'new-base'], ['-2.57', T, ROUTE], ['-2.6', F], ['-0.0256', F], ['97.44', F], ['-97.44', F]],
      4: [['2.63', T], ['2.627', T], ['2.6273', T], ['2.63%', T], ['2.62', T], ['2.64', F], ['2.56', 'same'], ['16', 'sixteen'], ['2.6', F], ['0.0263', F], ['102.63', F]],
    },
    'p-laptop-sale': {
      1: [['660', T], ['660.00', T], ['£660.00', T], ['645.15', 'added'], ['476.85', F], ['646.15', F]],
      2: [['600', T], ['600.00', T], ['594', 'took-off'], ['594.00', 'took-off'], ['586.50', 'added-carried'], ['726', F], ['510', F]],
      3: [['-6.5', T], ['−6.5', T], ['-6.5%', T], ['-6.50', T], ['6.5', 'sign'], ['-5', 'added'], ['-5.0', 'added'], ['-6.95', 'sale-base'], ['-7.0', 'sale-base', EDGE], ['-7', 'sale-base', EDGE], ['-6.9', 'sale-base', EDGE], ['-0.065', F], ['93.5', F], ['5', F]],
    },
    'p-fund-two-years': {
      1: [['25.44', T], ['25.44%', T], ['25.440', T], ['25.4', F], ['20.28', 'new-base'], ['20.3', F], ['125.44', 'multiplier'], ['0.2544', F], ['1590', F]],
      2: [['12', T], ['12%', T], ['12.0', T], ['12.72', 'halved'], ['12.7', 'halved'], ['25.44', 'total'], ['1.12', F], ['112', F], ['11', F]],
      3: [['90', T], ['£90', T], ['90.00', T], ['7750', 'simple-balance'], ['7,750', 'simple-balance'], ['0', 'none'], ['1500', F], ['1590', F], ['750', F]],
      4: [['11014.64', T], ['11,014.64', T], ['£11,014.64', T], ['11014.63', T], ['11014.6355', T], ['11014.65', F], ['11014.6', F], ['11015', F], ['10000', 'simple'], ['11373.26', 'halved'], ['13816.59', F], ['9834.50', F]],
    },
    'p-fund-six-months': {
      1: [['39185.69', T], ['39,185.69', T], ['£39,185.69', T], ['39185.692', T], ['39185.70', T], ['37960', 'added'], ['47320', 'one-month'], ['39185.7', T], ['39186', F], ['67341.51', F]],
      2: [['50746.60', T], ['50,746.60', T], ['50746.61', T], ['50746.6', T], ['50746.59', F], ['52000', 'cancel'], ['49765.83', 'added'], ['42712.40', F], ['50747', F]],
      3: [['-2.41', T], ['−2.41', T], ['-2.41%', T], ['-2.410', T], ['-2.4104', T], ['-2.4', F], ['2.41', 'sign'], ['0', 'cancel'], ['-0.81', 'one-pair'], ['-2.47', F], ['97.59', F]],
      4: [['2.47', T], ['2.470', T], ['2.4699', T], ['2.47%', T], ['2.46', T], ['2.48', F], ['2.41', 'same'], ['9', 'nine'], ['2.5', F], ['0.0247', F]],
    },
  },
  3: {
    'p-partners-profit': {
      1: [['12', T], ['12 parts', T], ['3:4:5', T, 'the part asks first for the ratio in simplest form; a learner who types it is not read, and nothing says only the count is wanted'], ['72', 'thousands'], ['36', 'halved'], ['3', F], ['6000', F], ['24', F]],
      2: [['4000', T], ['4,000', T], ['£4,000', T], ['3200', 'equal'], ['800', 'one-part'], ['2400', F], ['5000', F]],
      3: [['11400', T], ['11,400', T], ['8550', 'own-parts'], ['34200', 'one-part-share'], ['950', F], ['2850', F], ['7125', F]],
      4: [['1700', T], ['1,700', T], ['1983.33', 'old-parts'], ['1,983.33', 'old-parts'], ['1983', F], ['2975', 'equal'], ['850', F], ['5950', F]],
    },
    'p-print-run': {
      1: [['7.5', T], ['7.5 hours', T], ['7.50', T], ['7 1/2', T], ['15/2', T], ['19.2', 'direct'], ['9', 'subtracted'], ['7', F], ['8', F], ['7.3', F], ['450', F]],
      2: [['840', T], ['£840', T], ['840.00', T], ['2150.40', 'direct'], ['2,150.40', 'direct'], ['105', 'one-press'], ['1344', F], ['112', F]],
      3: [['23.33', T], ['£23.33', T], ['23.333', T], ['23.34', T], ['23.3', F], ['23', F], ['0.02', 'per-leaflet'], ['0.0233', 'per-leaflet'], ['0.023', 'per-leaflet'], ['42.86', 'upside-down'], ['2.33', F], ['233.33', F]],
    },
    'p-coffee-suppliers': {
      1: [['27.50', T], ['27.5', T], ['CHF 27.50', T, CUR], ['27.50 CHF', T], ['27.50 francs', T], ['0.04', 'upside-down'], ['0.036', 'upside-down'], ['29.40', 'german'], ['25', F], ['25.00', F], ['30.25', F]],
      2: [['25', T], ['25.00', T], ['£25.00', T], ['30.25', 'multiplied'], ['27.50', F], ['22.73', F]],
      3: [['24.50', T], ['24.5', T], ['£24.50', T], ['35.28', 'multiplied'], ['29.40', 'euros'], ['26.73', F], ['25', F]],
      4: [['45', T], ['45.00', T], ['£45.00', T], ['0.50', 'per-kg'], ['0.5', 'per-kg'], ['452.70', 'multiplied'], ['2250', F], ['2205', F], ['-45', F]],
    },
    'p-villa-split': {
      1: [['540', T], ['540.00', T], ['€540', T, CUR], ['540 euros', T], ['EUR 540', T, CUR], ['303.75', 'direct'], ['405', 'unchanged'], ['3240', F], ['480', F], ['1620', F]],
      2: [['480', T], ['480.00', T], ['£480.00', T], ['607.50', 'multiplied'], ['607.5', 'multiplied'], ['540', F], ['360', F]],
      3: [['630', T], ['630.00', T], ['€630', T, CUR], ['540', 'equal'], ['2061.82', 'two-parts'], ['360', 'four-nights'], ['90', F], ['560', F], ['2520', F]],
      4: [['80', T], ['80.00', T], ['£80.00', T], ['90', 'euros'], ['101.25', 'multiplied'], ['560', F], ['480', F]],
    },
  },
};

let checks = 0, fails = 0, findings = 0, nNum = 0, nRows = 0;
const say = (ok, note, msg) => { checks++; if (ok) { if (ALL) console.log('ok      ' + msg); return; } if (note) { findings++; console.log('FINDING ' + msg + '   [' + note + ']'); } else { fails++; console.log('FAIL    ' + msg); } };
for (const n of [1, 2, 3]) {
  const doc = JSON.parse(fs.readFileSync(`app/content/courses/ratio/problems-${n}.json`, 'utf8'));
  for (const it of doc.items) it.parts.forEach((p, i) => {
    const k = i + 1, w = p.widget, where = `${n} ${it.id} ${k}`;
    if (w.kind !== 'numeric') return;
    nNum++;
    const by = (p.feedback && p.feedback.byKey) || {};
    const pct = w.unit === '%';
    const a = String(pct ? +(w.answer * 100).toPrecision(10) : w.answer);
    say(num(w, a).ok, null, `${where}: key ${a} grades correct`);
    say(num(w, a.includes('.') ? a + '0' : a + '.0').ok, null, `${where}: key with one more place grades correct`);
    say(num(w, 'x = ' + a).ok, null, `${where}: key after a letter and = grades correct`);
    if (w.answer < 0) say(num(w, a.replace('-', '−')).ok, null, `${where}: key with a true minus sign grades correct`);
    if (w.unit) say(num(w, /^[£$€]$/.test(w.unit) ? w.unit + a : a + ' ' + w.unit).ok, null, `${where}: key with its unit ${w.unit} grades correct`);
    if (w.accept) say(num(w, w.accept).ok, null, `${where}: accept text "${w.accept}" grades correct`);
    for (const x of w.wrong || []) {
      const t = String(pct ? +(x.value * 100).toPrecision(10) : x.value);
      const r = num(w, t);
      say(!r.ok && r.key === x.id, null, `${where}: wrong "${x.id}" ${t} lands on its key (got ok=${r.ok} key=${r.key})`);
      say(!!by[x.id], null, `${where}: wrong "${x.id}" has a byKey line`);
    }
    const rows = ((ROWS[n] || {})[it.id] || {})[k];
    say(!!rows, null, `${where}: reader rows exist`);
    for (const [text, want, note] of rows || []) {
      nRows++;
      const r = num(w, text);
      const good = want === true ? r.ok : want === false ? (!r.ok && r.key === null) : (!r.ok && r.key === want);
      say(good, note, `${where}: "${text}" expected ${want === true ? 'accepted' : want === false ? 'refused, generic' : want}, got ${r.ok ? 'accepted' : r.key || 'refused, generic'}`);
    }
  });
}
console.log(`${nNum} numeric parts, ${checks} checks (${nRows} reader rows), ${fails} failures, ${findings} rows held to be faults`);
process.exit(fails ? 1 : 0);
