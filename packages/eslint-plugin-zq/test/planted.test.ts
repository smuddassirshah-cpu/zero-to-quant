// Stage 1's definition of done: a planted violation of each lint rule fails; stage 3's: a planted
// `Math.random` in mathcore fails. Each file is written at a real path and linted with the
// repository's own eslint.config.js (the type-aware parser needs the files on disk). The two sink
// files pass only at their exempt paths, and the files outside a rule's reach pass.
// Hygiene: every planted file starts with MARKER. Stale planted files from a killed run are
// removed first; a file at a planted path without the marker is real, and the test refuses to
// run rather than touch it (the sink paths become real files at stages 23 and 59). Cleanup
// removes this run's files one by one and its directories only when empty, so a real file
// written meanwhile survives.
// ESLint's Node API runs in a child process (an argument list, no shell): there ESLint loads the
// config and the plugin itself, as `npx eslint` does, and that natively loaded copy of the plugin
// stays out of this run's coverage, which it would otherwise distort.
import { execFileSync } from 'node:child_process';
import {
  existsSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  rmdirSync,
  unlinkSync,
  writeFileSync,
} from 'node:fs';
import path from 'node:path';
import type { ESLint } from 'eslint';
import { beforeAll, describe, expect, it } from 'vitest';
import { REPO_ROOT } from '../src/util/paths.ts';

type Result = Pick<ESLint.LintResult, 'filePath' | 'messages'>;

const MARKER = '// zq-planted: written and removed by packages/eslint-plugin-zq/test/planted.test.ts';
const LINT = [
  "import { ESLint } from 'eslint';",
  'const [cwd, ...files] = process.argv.slice(1);',
  'const results = await new ESLint({ cwd }).lintFiles(files);',
  'process.stdout.write(JSON.stringify(results.map(({ filePath, messages }) => ({ filePath, messages }))));',
].join('\n');

const violations = [
  {
    rule: 'zq/no-empty-catch',
    file: 'tools/__planted_catch.ts',
    code: 'export function run(task: () => void): void {\n  try {\n    task();\n  } catch {\n    // ignored\n  }\n}\n',
    message: 'never swallowed',
  },
  {
    rule: 'zq/no-inner-html',
    file: 'src/app/__planted_html.ts',
    code: 'export function show(el: HTMLElement, html: string): void {\n  el.innerHTML = html;\n}\n',
    message: "'innerHTML' turns a string into markup",
  },
  {
    rule: 'zq/no-forbidden-apis',
    file: 'src/app/__planted_open.ts',
    code: "export function leave(): void {\n  window.open('https://example.com');\n}\n",
    message: "'window.open' is forbidden",
  },
  {
    rule: 'zq/no-colour-literals',
    file: 'src/app/__planted_colour.tsx',
    code: "export const ink = '#ff0000';\n",
    message: "'#ff0000' is a colour literal",
  },
  {
    rule: 'zq/no-forbidden-apis',
    file: 'src/app/__planted_open.mjs',
    code: "globalThis.open('https://example.com');\n",
    message: "'globalThis.open' is forbidden",
  },
  {
    rule: 'zq/no-colour-literals',
    file: 'src/app/__planted_colour.js',
    code: "export const ink = 'rgb(255, 0, 0)';\n",
    message: "'rgb(255, 0, 0)' is a colour literal",
  },
  {
    rule: 'zq/layering',
    file: 'src/engine/__planted_layering.ts',
    code: "export * from '../screens/today/View.tsx';\n",
    message: 'engine/ may not import src/screens/today/View.tsx',
  },
  {
    rule: 'zq/no-nondeterminism',
    file: 'packages/mathcore/src/__planted_random.ts',
    code: 'export function draw(): number {\n  return Math.random();\n}\n',
    message: "'Math.random' is not seeded",
  },
  {
    rule: 'zq/no-nondeterminism',
    file: 'src/widgets/__planted/logic.ts',
    code: 'export function stamp(): number {\n  return Date.now();\n}\n',
    message: "'Date' reads the clock",
  },
  {
    rule: 'zq/no-nondeterminism',
    file: 'content/generators/__planted_exp.mjs',
    code: 'export const grow = (x) => Math.exp(x);\n',
    message: "'Math.exp' may differ between engines",
  },
  {
    rule: 'zq/no-nondeterminism',
    file: 'content/generators/__planted_self.mjs',
    code: 'const g = globalThis.globalThis;\nexport const draw = () => g.Math.random();\n',
    message: "'globalThis' may be used here only through static members",
  },
  {
    rule: 'zq/no-nondeterminism',
    file: 'packages/mathcore/src/dmath__planted_cube.ts',
    code: 'export const cube = (x: number): number => x ** 3;\n',
    message: "'**' may differ between engines",
  },
  {
    rule: 'zq/no-nondeterminism',
    file: 'packages/gen-kit/src/__planted_exp.mjs',
    code: 'export const grow = (x) => Math.exp(x);\n',
    message: "'Math.exp' may differ between engines",
  },
];

// An inline directive does not switch a rule off: noInlineConfig reports the directive instead.
const disabled = {
  rule: 'zq/no-inner-html',
  file: 'src/app/__planted_disable.ts',
  code: 'export function show(el: HTMLElement, html: string): void {\n  el.innerHTML = html; // eslint-disable-line zq/no-inner-html\n}\n',
  message: "'innerHTML' turns a string into markup",
};

const sinks = [
  {
    file: 'src/engine/render/Tex.tsx',
    code: 'export function setTex(el: HTMLElement, html: string): void {\n  el.innerHTML = html;\n}\n',
  },
  {
    file: 'src/ui/bertie/markup.ts',
    code: "export function parseRig(svg: string): Document {\n  return new DOMParser().parseFromString(svg, 'image/svg+xml');\n}\n",
  },
];

// Outside zq/no-nondeterminism's reach: transcendental Math in mathcore outside dmath, a package's tests.
const clean = [
  {
    file: 'packages/mathcore/src/__planted_exp.ts',
    code: 'export const grow = (x: number): number => Math.exp(x);\n',
  },
  {
    file: 'packages/mathcore/test/__planted_clock.ts',
    code: 'export const elapsed = (start: number): number => performance.now() - start;\n',
  },
];

const planted = [...violations, disabled, ...sinks, ...clean];
const results = new Map<string, Result>();
const createdFiles: string[] = [];
const createdDirs: string[] = [];

const ours = (file: string) => readFileSync(file, 'utf8').startsWith(MARKER);

function clearStale(target: string): void {
  if (!existsSync(target)) return;
  if (!path.basename(target).startsWith('__planted_') && !ours(target)) {
    throw new Error(
      `${path.relative(REPO_ROOT, target)} is a real file; move its check off the planted test`,
    );
  }
  unlinkSync(target);
}

function plant(target: string, code: string): void {
  const missing: string[] = [];
  for (let dir = path.dirname(target); !existsSync(dir); dir = path.dirname(dir)) missing.unshift(dir);
  for (const dir of missing) {
    mkdirSync(dir);
    createdDirs.push(dir);
  }
  writeFileSync(target, `${MARKER}\n${code}`, { flag: 'wx' });
  createdFiles.push(target);
}

function cleanUp(): void {
  for (const file of createdFiles) if (existsSync(file) && ours(file)) unlinkSync(file);
  for (const dir of [...createdDirs].reverse()) if (readdirSync(dir).length === 0) rmdirSync(dir);
}

beforeAll(() => {
  const targets = planted.map(({ file, code }) => ({ target: path.join(REPO_ROOT, file), code }));
  for (const { target } of targets) clearStale(target);
  try {
    for (const { target, code } of targets) plant(target, code);
    const args = ['--input-type=module', '--eval', LINT, REPO_ROOT, ...targets.map(({ target }) => target)];
    const out = execFileSync(process.execPath, args, { cwd: REPO_ROOT, encoding: 'utf8', timeout: 90_000 });
    for (const result of JSON.parse(out) as Result[]) {
      results.set(path.relative(REPO_ROOT, result.filePath).split(path.sep).join('/'), result);
    }
  } finally {
    cleanUp();
  }
}, 120_000);

describe('planted violations', () => {
  it.each(violations)('$rule fails $file', ({ rule, file, message }) => {
    const messages = results.get(file)?.messages ?? [];
    expect(messages.map((m) => m.ruleId)).toEqual([rule]);
    expect(messages[0]?.message).toContain(message);
  });

  it('an inline disable neither silences zq/no-inner-html nor passes unreported', () => {
    const messages = results.get(disabled.file)?.messages ?? [];
    expect(messages.filter((m) => m.ruleId === disabled.rule).map((m) => m.message)).toEqual([
      expect.stringContaining(disabled.message),
    ]);
    expect(messages.some((m) => m.ruleId === null && m.message.includes("'noInlineConfig'"))).toBe(true);
  });

  it.each(sinks)('$file passes as a justified sink', ({ file }) => {
    expect(results.get(file)?.messages).toEqual([]);
  });

  it.each(clean)('$file passes outside the rule', ({ file }) => {
    expect(results.get(file)?.messages).toEqual([]);
  });

  it('removes every file and directory it created', () => {
    expect(createdFiles).toHaveLength(planted.length);
    for (const entry of [...createdFiles, ...createdDirs]) expect(existsSync(entry)).toBe(false);
  });
});
