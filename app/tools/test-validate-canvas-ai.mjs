#!/usr/bin/env node
/* Scratch cases for the AI strand canvas keys (ENGINE-BACKLOG 1227 to 1229; docs/AUTHORING.md section 4).
   Copies tools/fixtures/mini-app (lib/validate-harness.mjs), swaps the canvas of one lesson screen and reads the report.
     graph:  valueLines (one or two { label, colour }), state.values2 (needs two lines, node ids exist), edgeWidth (true or { min, max, norm, sign })
     matrix: heat (true or { mode, range, legend, decimals }); a sequential heat with negative entries needs a range
     grid:   state.arrows (rows by cols list, or a cell-id map; directions up, down, left, right, none; lengths match rows and cols)
   Usage: node tools/test-validate-canvas-ai.mjs. Exit 0 pass, 1 failure. */
import fs from 'node:fs';
import { openHarness } from './lib/validate-harness.mjs';

const h = openHarness({ name: 'canvas-ai' });
const file = h.path('content/courses/algo-think/l1-counting-work.json');
const base = JSON.parse(fs.readFileSync(file, 'utf8'));
let fails = 0;
const say = (ok, name, detail = '') => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`); if (!ok) fails++; };
const run = (canvas) => {
  const d = JSON.parse(JSON.stringify(base));
  d.screens[0].canvas = canvas;
  fs.writeFileSync(file, JSON.stringify(d, null, 2));
  return h.validate(['--no-manifest']);
};
const mine = (r) => r.errors.filter((l) => /params\.(valueLines|edgeWidth|matrices\[\d+\]\.heat|edges)|state\.(values2?|arrows)/.test(l));

const GN = [{ id: 'a', label: 'a', x: 0.2, y: 0.5 }, { id: 'b', label: 'b', x: 0.8, y: 0.5 }];
const graph = (params, state = {}) => ({ kind: 'graph', params: { directed: true, nodes: GN, edges: [{ from: 'a', to: 'b', w: -0.5 }], ...params }, state });
const mat = (heat, rows = [[0.1, 0.9], [0.4, 0.2]]) => ({ kind: 'matrix', params: { matrices: [{ id: 'A', rows, heat }] }, state: {} });
const grid = (state, params = {}) => ({ kind: 'grid', params: { rows: 2, cols: 3, ...params }, state });

const GOOD = [
  ['graph two lines and edge width', graph({ valueLines: [{ label: 'v', colour: 2 }, { label: 'g', colour: 4 }], edgeWidth: { max: 6, sign: 'colour' } }, { values: { a: '1.2' }, values2: { b: '-0.3' } })],
  ['graph edgeWidth true, one line', graph({ edgeWidth: true, valueLines: [{ label: 'v' }] }, { values: { a: '1' } })],
  ['matrix heat true', mat(true)], ['matrix heat diverging with range', mat({ mode: 'div', range: [-1, 1], decimals: 1 }, [[-1, 0.5], [0.2, 1]])],
  ['matrix heat signed rows, mode auto', mat({ legend: false }, [[-1, 0.5], [0.2, 1]])],
  ['grid arrows 2D', grid({ arrows: [['up', 'down', 'left'], ['right', 'none', 'up']] })],
  ['grid arrows by id', grid({ arrows: { r1c1: 'up', r2c3: { dir: 'left', colour: 2 } } })],
];
for (const [name, c] of GOOD) { const r = run(c); say(mine(r).length === 0, `good: ${name}`, r.errors.slice(0, 3).join(' | ')); }

const BAD = [
  ['valueLines not a list', graph({ valueLines: { label: 'v' } }), 'params.valueLines'],
  ['valueLines three', graph({ valueLines: [{}, {}, {}] }), 'params.valueLines'],
  ['valueLines bad colour', graph({ valueLines: [{ label: 'v', colour: 9 }] }), 'params.valueLines'],
  ['values2 without a second line', graph({ valueLines: [{ label: 'v' }] }, { values2: { a: '1' } }), 'state.values2'],
  ['values2 unknown node', graph({ valueLines: [{}, {}] }, { values2: { z: '1' } }), 'state.values2.z'],
  ['values names unknown node', graph({ valueLines: [{}, {}] }, { values: { z: '1' } }), 'state.values.z'],
  ['edgeWidth text', graph({ edgeWidth: 'weight' }), 'params.edgeWidth'],
  ['edgeWidth bad sign', graph({ edgeWidth: { sign: 'red' } }), 'params.edgeWidth'],
  ['edgeWidth min above max', graph({ edgeWidth: { min: 8, max: 4 } }), 'params.edgeWidth'],
  ['edge weight text with edgeWidth', graph({ edgeWidth: true, edges: [{ from: 'a', to: 'b', w: 'heavy' }] }), 'params.edges[0].w'],
  ['heat text', mat('hot'), '.heat'], ['heat bad mode', mat({ mode: 'rainbow' }), '.heat.mode'], ['heat range reversed', mat({ range: [1, 0] }), '.heat.range'],
  ['heat range one number', mat({ range: [1] }), '.heat.range'], ['heat legend text', mat({ legend: 'yes' }), '.heat.legend'], ['heat decimals fraction', mat({ decimals: 1.5 }), '.heat.decimals'],
  ['heat seq with negatives and no range', mat({ mode: 'seq' }, [[-1, 1], [0, 1]]), '.heat.mode'],
  ['arrows too few rows', grid({ arrows: [['up', 'down', 'left']] }), 'state.arrows'],
  ['arrows too few columns', grid({ arrows: [['up', 'down'], ['up', 'down']] }), 'state.arrows'],
  ['arrows bad direction', grid({ arrows: [['up', 'down', 'north'], ['up', 'down', 'up']] }), 'state.arrows[0][2]'],
  ['arrows cell outside the grid', grid({ arrows: { r3c1: 'up' } }), 'state.arrows.r3c1'],
  ['arrows bad id', grid({ arrows: { A1: 'up' } }), 'state.arrows.A1'],
  ['arrows bad direction in a map', grid({ arrows: { r1c1: 'sideways' } }), 'state.arrows.r1c1'],
  ['arrows bad colour', grid({ arrows: { r1c1: { dir: 'up', colour: 7 } } }), 'state.arrows.r1c1'],
  ['arrows text', grid({ arrows: 'up' }), 'state.arrows'],
];
for (const [name, c, sub] of BAD) { const r = run(c); say(r.errors.some((l) => l.includes(sub)), `bad: ${name} names ${sub}`, r.errors.slice(0, 3).join(' | ')); }
h.close();
if (fails) { console.error(`test-validate-canvas-ai: ${fails} failed`); process.exit(1); }
console.log('test-validate-canvas-ai: all passed');
