// Stage 1's definition of done: a planted violation of each lint rule fails. Each file is written
// at a real path, linted with the repository's own eslint.config.js (the type-aware parser needs
// the files on disk), and removed in a `finally` with any directory planting created, whatever
// the lint did. The two sink files pass only at their exempt paths, and are planted only when no
// such file exists yet.
// ESLint's Node API runs in a child process (an argument list, no shell): there ESLint loads the
// config and the plugin itself, as `npx eslint` does, and that natively loaded copy of the plugin
// stays out of this run's coverage, which it would otherwise distort.
import { execFileSync } from 'node:child_process';
import { existsSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import type { ESLint } from 'eslint';
import { beforeAll, describe, expect, it } from 'vitest';
import { REPO_ROOT } from '../src/util/paths.ts';

type Result = Pick<ESLint.LintResult, 'filePath' | 'messages'>;

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
];

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

const results = new Map<string, Result>();
const planted: string[] = [];

beforeAll(() => {
  try {
    for (const { file, code } of [...violations, ...sinks]) {
      const target = path.join(REPO_ROOT, file);
      if (existsSync(target)) continue;
      planted.push(mkdirSync(path.dirname(target), { recursive: true }) ?? target);
      writeFileSync(target, code, { flag: 'wx' });
    }
    const files = [...violations, ...sinks].map(({ file }) => path.join(REPO_ROOT, file));
    const args = ['--input-type=module', '--eval', LINT, REPO_ROOT, ...files];
    const out = execFileSync(process.execPath, args, { cwd: REPO_ROOT, encoding: 'utf8' });
    for (const result of JSON.parse(out) as Result[]) {
      results.set(path.relative(REPO_ROOT, result.filePath).split(path.sep).join('/'), result);
    }
  } finally {
    for (const entry of [...planted].reverse()) rmSync(entry, { recursive: true, force: true });
  }
}, 120_000);

describe('planted violations', () => {
  it.each(violations)('$rule fails $file', ({ rule, file, message }) => {
    const messages = results.get(file)?.messages ?? [];
    expect(messages.map((m) => m.ruleId)).toEqual([rule]);
    expect(messages[0]?.message).toContain(message);
  });

  it.each(sinks)('$file passes as a justified sink', ({ file }) => {
    expect(results.get(file)?.messages).toEqual([]);
  });

  it('leaves nothing behind', () => {
    expect(planted.length).toBeGreaterThan(0);
    for (const entry of planted) expect(existsSync(entry)).toBe(false);
  });
});
