import { Linter } from 'eslint';
import fc from 'fast-check';
import tseslint from 'typescript-eslint';
import { expect, it } from 'vitest';
import rule from '../src/rules/no-nondeterminism.ts';
import { tester, TYPED, typed } from './tester.ts';

const error = (messageId: string, name: string) => ({ messageId, data: { name } });
const fails = (code: string, ...errors: [string, string][]) => ({
  code,
  errors: errors.map(([messageId, name]) => error(messageId, name)),
});
const GEN = [{ transcendental: true }];
const gen = (code: string, ...errors: [string, string][]) => ({ ...fails(code, ...errors), options: GEN });

tester.run('no-nondeterminism', rule, {
  valid: [
    'Math.floor(x) + Math.sqrt(y) + Math.PI',
    'const { floor, max } = Math',
    'const Date = makeClock(); Date.now()',
    'function f(Math) { return Math.random() }',
    'import { random } from "./rng.ts"; random()',
    'rng.random()',
    'const o = { random: 1, Date: 2, now() {} }',
    'x.performance.now()',
    'globalThis.structuredClone(x)',
    'function f(top) { return top.self.Math.random() }',
    'node.parent.window.Math.random(); tree.top.Date.now()',
    'let d: Date',
    'type N = typeof Date.now',
    'type M = typeof Math',
    'Math.exp(1) + Math.pow(2, 0.5) + 2 ** 0.5',
    { code: 'Math.sqrt(2) + Math.fround(x) + Math.round(x) + Math.hypotenuse', options: GEN },
    { code: '10n ** 3n + BigInt(n) ** k', options: GEN },
    { code: 'let n = 10n; n **= 2n', options: GEN },
    {
      code: 'let y = 0; y = Math.floor(1.5); const [...xs] = list; function f(...args) { return args }',
      options: GEN,
    },
  ],
  invalid: [
    fails('Math.random()', ['random', 'Math.random']),
    fails('const r = Math.random', ['random', 'Math.random']),
    fails('Math["random"]()', ['random', 'Math.random']),
    fails('Math?.random()', ['random', 'Math.random']),
    fails('(Math as Math).random()', ['random', 'Math.random']),
    fails('const M = Math!', ['escape', 'Math']),
    fails('const { random } = Math', ['random', 'Math.random']),
    fails('({ random: r } = Math)', ['random', 'Math.random']),
    fails('globalThis.Math.random()', ['random', 'Math.random']),
    fails('window["Math"].random()', ['random', 'Math.random']),
    fails('crypto.getRandomValues(a)', ['random', 'crypto.getRandomValues']),
    fails('self.crypto.randomUUID()', ['random', 'crypto.randomUUID']),
    fails('const { randomUUID } = crypto', ['random', 'crypto.randomUUID']),
    fails('crypto.subtle.generateKey(a, true, u)', ['random', 'crypto.subtle']),
    fails('const { subtle } = globalThis.crypto', ['random', 'crypto.subtle']),
    fails('process.hrtime.bigint()', ['host', 'process']),
    fails('const { uptime } = globalThis.process', ['host', 'process']),
    fails('Date.now()', ['clock', 'Date']),
    fails('new Date()', ['clock', 'Date']),
    fails('new Date(0)', ['clock', 'Date']),
    fails('const D = Date', ['clock', 'Date']),
    fails('x instanceof Date', ['clock', 'Date']),
    fails('globalThis.Date.now()', ['clock', 'Date']),
    fails('new window.Date()', ['clock', 'Date']),
    fails('const { Date: D } = globalThis', ['clock', 'Date']),
    fails('performance.now()', ['clock', 'performance']),
    fails('performance.timeOrigin', ['clock', 'performance']),
    fails('const p = self.performance', ['clock', 'performance']),
    fails('Temporal.Now.instant()', ['clock', 'Temporal']),
    // Without the DOM library the browser's globals are undeclared, and reached through the scope.
    {
      ...fails(
        'performance.now(); crypto.randomUUID()',
        ['clock', 'performance'],
        ['random', 'crypto.randomUUID'],
      ),
      languageOptions: { parserOptions: { lib: ['es2022'] } },
    },
    fails('Math[name]()', ['escape', 'Math']),
    fails('const M = Math', ['escape', 'Math']),
    fails('use(Math)', ['escape', 'Math']),
    fails('Reflect.get(Math, "random")', ['escape', 'Math']),
    fails('const { floor, ...rest } = Math', ['escape', 'Math']),
    fails('const { [k]: f } = Math', ['escape', 'Math']),
    fails('const c = crypto', ['escape', 'crypto']),
    fails('const M = globalThis.Math', ['escape', 'Math']),
    fails('const { Math: M } = globalThis', ['escape', 'Math']),
    fails('globalThis[k]', ['escape', 'globalThis']),
    fails('const g = globalThis', ['escape', 'globalThis']),
    fails('Reflect.get(window, "Date")', ['escape', 'window']),
    fails('const { ...all } = self', ['escape', 'self']),
    // A global object reached through its own members, as `.js` files see it without types.
    fails('const g = globalThis.globalThis', ['escape', 'globalThis']),
    fails('const { self: s } = globalThis; s.Math.random()', ['escape', 'self']),
    fails('const { globalThis: g } = globalThis', ['escape', 'globalThis']),
    fails('use(window?.top)', ['escape', 'top']),
    fails('const p = parent', ['escape', 'parent']),
    fails('globalThis.window[k]', ['escape', 'window']),
    fails('globalThis[k].self.Math.random()', ['escape', 'globalThis']),
    fails('globalThis.globalThis.Math.random()', ['random', 'Math.random']),
    fails('window.top.Math.random()', ['random', 'Math.random']),
    fails('self.self.crypto.getRandomValues(a)', ['random', 'crypto.getRandomValues']),
    fails('window.parent.performance.now()', ['clock', 'performance']),
    fails('opener.frames.Date.now()', ['clock', 'Date']),
    fails('global.Math.random()', ['random', 'Math.random']),
    fails('const { Math: M } = top.self', ['escape', 'Math']),
    gen('Math.exp(x)', ['transcendental', 'Math.exp']),
    gen('Math.pow(2, k)', ['transcendental', 'Math.pow']),
    gen('const { sin, cos } = Math', ['transcendental', 'Math.sin'], ['transcendental', 'Math.cos']),
    gen('globalThis.Math.log1p(x)', ['transcendental', 'Math.log1p']),
    gen('2 ** k', ['transcendental', '**']),
    gen('x **= 0.5', ['transcendental', '**=']),
    gen('Math.random() + Math.tanh(x)', ['random', 'Math.random'], ['transcendental', 'Math.tanh']),
    gen('globalThis.globalThis.Math.exp(1)', ['transcendental', 'Math.exp']),
  ],
});

// Every function of ECMA-262 21.3.2: the 22 its NOTE leaves implementation-approximated, less `random`,
// and the 14 exact ones [sourced: tc39/ecma262 spec.html at 6db9135].
const APPROXIMATED = [
  'acos acosh asin asinh atan atanh atan2 cbrt cos cosh exp',
  'expm1 hypot log log1p log2 log10 pow sin sinh tan tanh',
].flatMap((line) => line.split(' '));
const EXACT = 'abs ceil clz32 floor fround f16round imul max min round sign sqrt sumPrecise trunc'.split(' ');

it('lists 22 approximated and 14 exact Math functions', () => {
  expect([APPROXIMATED.length, EXACT.length]).toEqual([22, 14]);
});

tester.run('no-nondeterminism (each Math function)', rule, {
  valid: [
    ...EXACT.map((name) => ({ code: `Math.${name}(x)`, options: GEN })),
    ...APPROXIMATED.map((name) => `Math.${name}(x)`),
  ],
  invalid: APPROXIMATED.map((name) => gen(`Math.${name}(x)`, ['transcendental', `Math.${name}`])),
});

const typedFails = (code: string, ...errors: [string, string][]) => ({
  ...fails(code, ...errors),
  filename: TYPED,
});

typed.run('no-nondeterminism (typed)', rule, {
  valid: [
    { code: 'declare const d: Date; export const t = d.getTime();', filename: TYPED },
    { code: 'declare const rng: { random(): number }; export const r = rng.random();', filename: TYPED },
    { code: 'declare const n: bigint; export const c = n ** 3n;', filename: TYPED, options: GEN },
    {
      code: 'declare const n: 2n | 3n; declare const k: bigint; export const c = n ** k;',
      filename: TYPED,
      options: GEN,
    },
    { code: 'export const sq = (m: Math, x: number) => m.sqrt(x);', filename: TYPED, options: GEN },
    // A module's own Window, such as a rolling window, is not the platform's.
    {
      code: [
        'interface Window { top: number; bottom: number; parent: Window | null }',
        'export const height = (w: Window): number => w.top - w.bottom;',
        'export const up = (w: Window): Window | null => w.parent;',
      ].join('\n'),
      filename: TYPED,
    },
  ],
  invalid: [
    typedFails('export const r = (m: Math) => m.random();', ['random', 'Math.random']),
    typedFails('export const r = ({ random }: Math) => random();', ['random', 'Math.random']),
    typedFails('export const u = (c: Crypto) => c.randomUUID();', ['random', 'crypto.randomUUID']),
    typedFails('export const t = (p: Performance) => p.now();', ['clock', 'performance.now']),
    typedFails('export const t = (D: DateConstructor) => D.now();', ['clock', 'Date.now']),
    typedFails('export const t = (D: DateConstructor) => new D();', ['clock', 'Date']),
    typedFails('export const t = ({ ...rest }: DateConstructor) => rest;', ['clock', 'Date']),
    typedFails('export const t = (p: Performance, k: "now") => p[k]();', ['clock', 'performance']),
    typedFails('export const r = ({ ...rest }: Math) => rest;', ['escape', 'Math']),
    typedFails('export const t = ({ Date: D }: typeof globalThis) => D;', ['clock', 'Date']),
    typedFails('export const t = ({ ...rest }: typeof globalThis) => rest;', ['escape', 'globalThis']),
    typedFails('export const t = (D: DateConstructor) => D();', ['clock', 'Date']),
    typedFails(
      'const g = globalThis; export const t = g.Date.now();',
      ['escape', 'globalThis'],
      ['clock', 'Date'],
    ),
    typedFails('declare const g: typeof globalThis; export const r = g.Math.random();', [
      'random',
      'Math.random',
    ]),
    typedFails('declare const g: typeof globalThis; export const { Date: D } = g;', ['clock', 'Date']),
    typedFails('declare const g: typeof globalThis; export const v = g[k];', ['escape', 'g']),
    typedFails('const M = Math; export const r = M.random();', ['escape', 'Math'], ['random', 'Math.random']),
    typedFails(
      'const g = globalThis.globalThis; export const r = g.Math.random();',
      ['escape', 'globalThis'],
      ['random', 'Math.random'],
    ),
    typedFails(
      'const { self: s } = globalThis; export const t = s.Date.now();',
      ['escape', 'self'],
      ['clock', 'Date'],
    ),
    typedFails(
      "export const k = crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, ['encrypt']);",
      ['random', 'crypto.subtle'],
    ),
    typedFails(
      "declare const s: SubtleCrypto; export const k = s.generateKey('AES-GCM', true, ['encrypt']);",
      ['random', 'crypto.subtle.generateKey'],
    ),
    typedFails('export const k = ({ generateKey }: SubtleCrypto) => generateKey;', [
      'random',
      'crypto.subtle.generateKey',
    ]),
    typedFails('export const k = (s: SubtleCrypto, m: "digest") => s[m];', ['random', 'crypto.subtle']),
    typedFails('export const s = (c: Crypto) => c.subtle;', ['random', 'crypto.subtle']),
    typedFails(
      "declare const o: { subtle: SubtleCrypto }; export const k = o.subtle.generateKey('AES-GCM', true, []);",
      ['random', 'crypto.subtle.generateKey'],
    ),
    typedFails('export const t = process.uptime();', ['host', 'process']),
    // lib.dom's Window, and the same augmented by a module.
    typedFails('export const t = (w: Window) => w.top;', ['escape', 'top']),
    typedFails('export const r = (w: Window) => w.parent.Math.random();', ['random', 'Math.random']),
    typedFails('export const t = <W extends Window>(w: W) => w.top;', ['escape', 'top']),
    typedFails('declare global { interface Window { zq: number } }\nexport const t = (w: Window) => w.top;', [
      'escape',
      'top',
    ]),
    {
      ...typedFails('declare const n: number; export const c = n ** 2;', ['transcendental', '**']),
      options: GEN,
    },
    {
      ...typedFails('declare const n: bigint | number; export const c = n ** 2;', ['transcendental', '**']),
      options: GEN,
    },
    {
      ...typedFails('declare const n: any; export const c = n ** 2;', ['transcendental', '**']),
      options: GEN,
    },
    {
      ...typedFails('export const e = (m: Math, x: number) => m.exp(x);', ['transcendental', 'Math.exp']),
      options: GEN,
    },
  ],
});

// Every spelling of a watched member (owner, access form, enclosing code) gives exactly one report of
// its kind, and an exact Math member none, with and without the generator option.
const members = fc.constantFrom(
  { owner: 'Math', name: 'random', id: 'random', gen: 'random' },
  { owner: 'crypto', name: 'getRandomValues', id: 'random', gen: 'random' },
  { owner: 'crypto', name: 'randomUUID', id: 'random', gen: 'random' },
  ...['exp', 'log', 'pow', 'sin', 'atan2', 'hypot', 'cbrt'].map((name) => ({
    owner: 'Math',
    name,
    id: undefined,
    gen: 'transcendental',
  })),
  ...['floor', 'sqrt', 'abs', 'fround', 'imul', 'PI'].map((name) => ({
    owner: 'Math',
    name,
    id: undefined,
    gen: undefined,
  })),
);
const owners = fc.constantFrom(
  '$',
  'globalThis.$',
  "window['$']",
  'self?.$',
  '($ as typeof $)',
  'globalThis.self.$',
  "window.window['$']",
  'top?.parent.$',
  'global.$',
);
const forms = fc.constantFrom(
  (o: string, m: string) => `${o}.${m}`,
  (o: string, m: string) => `${o}['${m}']`,
  (o: string, m: string) => `${o}[\`${m}\`]`,
  (o: string, m: string) => `${o}?.['${m.slice(0, 1)}' + '${m.slice(1)}']`,
  (o: string, m: string) => `(() => { const { ${m}: x } = ${o}; return x; })()`,
);
const sites = fc.constantFrom(
  (e: string) => `export const v = ${e};`,
  (e: string) => `export function f() { return ${e}; }`,
  (e: string) => `export class C { m() { return ${e}; } }`,
);
const linter = new Linter({ configType: 'flat' });

it('reports each spelling of a watched member once, with its kind', () => {
  fc.assert(
    fc.property(members, owners, forms, sites, fc.boolean(), (member, owner, form, site, generator) => {
      const code = site(form(owner.replace('$', member.owner), member.name));
      const messages = linter.verify(
        code,
        {
          files: ['**/*.ts'],
          languageOptions: { parser: tseslint.parser },
          plugins: { zq: { rules: { 'no-nondeterminism': rule } } },
          rules: { 'zq/no-nondeterminism': ['error', { transcendental: generator }] },
        },
        'a.ts',
      );
      const expected = generator ? member.gen : member.id;
      expect(messages.map((m) => m.messageId)).toEqual(expected ? [expected] : []);
    }),
  );
});
