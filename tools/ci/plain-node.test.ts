import { mkdirSync, mkdtempSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import fc from 'fast-check';
import { afterEach, describe, expect, it } from 'vitest';
import { main, specifiers, workspaceSpecifiers } from './plain-node.ts';
import { repoRoot } from './proc.ts';

const WORKSPACE = { '.': './src/index.ts', './*': './src/*.ts' };

const temps: string[] = [];
afterEach(() => {
  for (const dir of temps.splice(0)) rmSync(dir, { recursive: true, force: true });
});

/** A repository root holding one linked workspace package, as npm lays it out. */
function plantPackage(name: string, files: Readonly<Record<string, string>>): string {
  const root = mkdtempSync(join(tmpdir(), 'zq-plain-node-'));
  temps.push(root);
  const dir = join(root, 'packages', 'planted');
  mkdirSync(join(dir, 'src'), { recursive: true });
  writeFileSync(join(dir, 'package.json'), JSON.stringify({ name, type: 'module', exports: WORKSPACE }));
  for (const [file, text] of Object.entries(files)) writeFileSync(join(dir, file), text);
  mkdirSync(join(root, 'node_modules', '@zq'), { recursive: true });
  symlinkSync(join('..', '..', 'packages', 'planted'), join(root, 'node_modules', '@zq', 'planted'), 'dir');
  return root;
}

describe('specifiers', () => {
  it('maps the entry and every wildcard module once, and nothing outside the targets', () => {
    const files = [
      'package.json',
      'src/index.ts',
      'src/rng.ts',
      'src/stats/normal.ts',
      'src/notes.md',
      'test/a.ts',
    ];
    expect(specifiers('@zq/m', WORKSPACE, files)).toEqual(['@zq/m', '@zq/m/rng', '@zq/m/stats/normal']);
  });

  it('reads exact subpaths and keeps the first key that reaches a file', () => {
    const exports = { './a': './lib/a.js', './b': './lib/missing.js', './*': './lib/*.js' };
    expect(specifiers('@zq/x', exports, ['lib/a.js', 'lib/c.js'])).toEqual(['@zq/x/a', '@zq/x/c']);
  });

  it.each([
    [{ '.': null }, 'is not a string target'],
    [{ '.': { import: './src/index.ts' } }, 'is not a string target'],
    [{ '.': '../outside.ts' }, 'is not a string target'],
    [{ src: './src/index.ts' }, 'is not a string target'],
    [{ '.': './src/*.ts' }, "needs one '*'"],
    [{ './*/*': './src/*/*.ts' }, "needs one '*'"],
  ])('refuses %j', (exports, message) => {
    expect(() => specifiers('@zq/x', exports, ['src/index.ts'])).toThrow(message);
  });

  it('gives each module under a wildcard exactly one specifier that names it, in any file order', () => {
    const stem = fc.stringMatching(/^[a-z][a-z0-9-]{0,7}(?:\/[a-z][a-z0-9-]{0,7})?$/);
    fc.assert(
      fc.property(fc.uniqueArray(stem, { maxLength: 12 }), fc.boolean(), (stems, withIndex) => {
        const modules = stems.filter((s) => s !== 'index').map((s) => `src/${s}.ts`);
        const files = [...modules, ...(withIndex ? ['src/index.ts'] : []), 'README.md', 'src/data.json'];
        const expected = modules.map((file) => `@zq/p/${file.slice(4, -3)}`);
        if (withIndex) expected.push('@zq/p');
        expected.sort();
        expect(specifiers('@zq/p', WORKSPACE, files)).toEqual(expected);
        expect(specifiers('@zq/p', WORKSPACE, [...files].reverse())).toEqual(expected);
      }),
    );
  });
});

describe('plain Node import of the workspace packages', () => {
  it('lists every @zq/ package module and skips other workspaces', () => {
    const specs = workspaceSpecifiers(repoRoot);
    expect(specs).toContain('@zq/contracts');
    expect(specs).toContain('@zq/mathcore');
    expect(specs.every((s) => s.startsWith('@zq/'))).toBe(true);
  });

  it('imports @zq/contracts and @zq/mathcore with no DOM globals', async () => {
    const lines: string[] = [];
    expect(await main(repoRoot, undefined, (line) => lines.push(line))).toBe(0);
    const count = workspaceSpecifiers(repoRoot).length;
    expect(lines).toEqual([`plain-node: ${count} of ${count} modules imported in plain Node`]);
  }, 30_000);

  it('fails a module that reads a DOM global or navigator at import time, naming it', async () => {
    const root = plantPackage('@zq/planted', {
      'src/index.ts': 'export const ok: number = 1;\n',
      'src/dom.ts': 'export const title: string = document.title;\n',
      'src/nav.ts': 'export const agent: string = navigator.userAgent;\n',
    });
    const lines: string[] = [];
    expect(await main(root, undefined, (line) => lines.push(line))).toBe(1);
    expect(lines.join('\n')).toMatch(/@zq\/planted\/dom: ReferenceError: document is not defined/);
    expect(lines.join('\n')).toMatch(/@zq\/planted\/nav: ReferenceError: navigator is not defined/);
    expect(lines.at(-1)).toBe('plain-node: 1 of 3 modules imported in plain Node');
  }, 30_000);

  it('fails when there is no @zq/ package, or one has no exports map', async () => {
    const empty = mkdtempSync(join(tmpdir(), 'zq-plain-node-'));
    temps.push(empty);
    const lines: string[] = [];
    expect(await main(empty, undefined, (line) => lines.push(line))).toBe(1);
    expect(lines).toEqual(['plain-node: no @zq/ package found']);
    const bare = plantPackage('@zq/bare', { 'src/index.ts': 'export {};\n' });
    writeFileSync(join(bare, 'packages', 'planted', 'package.json'), JSON.stringify({ name: '@zq/bare' }));
    expect(() => workspaceSpecifiers(bare)).toThrow('@zq/bare: package.json has no exports map');
    const other = plantPackage('eslint-plugin-other', { 'src/index.ts': 'export {};\n' });
    expect(workspaceSpecifiers(other)).toEqual([]);
  });
});
