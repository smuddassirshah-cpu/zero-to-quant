import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { findNames, forbidden, inScope, main, viteEnvProblems } from './env-names.ts';
import type { Run } from './proc.ts';

// Assembled at run time so this file does not itself carry a forbidden name.
const planted = ['VITE', 'ZQ', 'TUTOR', 'TOKEN'].join('_');
const sauce = ['VITE', 'ZQ', 'SECRET', 'SAUCE'].join('_');

describe('env names', () => {
  it.each([
    ['src/app/config.ts', true],
    ['.github/workflows/ci.yml', true],
    ['vite.config.ts', true],
    ['.env.example', true],
    ['proxy/.env.example', true],
    ['docs/PLAN.md', false],
    ['README.md', false],
    ['package-lock.json', false],
    ['content/a.yaml', false],
  ])('%s in scope: %s', (path, expected) => {
    expect(inScope(path)).toBe(expected);
  });

  it('finds every VITE_ name with its line and flags KEY, TOKEN and SECRET', () => {
    const text = `VITE_BASE=/\nconst a = import.meta.env.${planted};\nMY_VITE_X=1 ${sauce} VITE_\n`;
    const found = findNames('f.ts', text);
    expect(found.map((f) => `${f.line}:${f.name}`)).toEqual(['1:VITE_BASE', `2:${planted}`, `3:${sauce}`]);
    expect(forbidden(found).map((f) => f.name)).toEqual([planted, sauce]);
    const camel = ['VITE', 'tutorToken'].join('_');
    expect(forbidden(findNames('g.ts', `env.${camel}`)).map((f) => f.name)).toEqual([camel]);
  });

  it('allows only VITE_ reads through loadEnv and the default envPrefix', () => {
    expect(
      viteEnvProblems("const env = loadEnv(mode, repo, 'VITE_');\nenv.VITE_BASE; process.env.ZQ_X;"),
    ).toEqual([]);
    expect(viteEnvProblems("const all = loadEnv(mode, dir, '');\nall.PATH;")).toEqual([
      "loadEnv(mode, dir, '') reads non-VITE_ names",
      'all.PATH is a loadEnv read of a non-VITE_ name',
    ]);
    expect(viteEnvProblems("const e = loadEnv(m, d);\ne['HOME'];")).toEqual([
      'e.HOME is a loadEnv read of a non-VITE_ name',
    ]);
    expect(viteEnvProblems('const { VITE_BASE, HOME: h } = loadEnv(m, d);\n')).toEqual([
      'HOME is a loadEnv read of a non-VITE_ name',
    ]);
    expect(viteEnvProblems("export default { envPrefix: ['VITE_', 'APP_'] };")).toHaveLength(1);
  });

  it('scans tracked files in scope and fails on a planted name', async () => {
    const root = mkdtempSync(join(tmpdir(), 'zq-env-names-'));
    try {
      mkdirSync(join(root, 'src'));
      writeFileSync(join(root, 'src', 'a.ts'), `export const url = import.meta.env.${planted};\n`);
      writeFileSync(join(root, 'notes.md'), `${planted}\n`);
      writeFileSync(join(root, '.env.example'), 'VITE_BASE=/\n');
      const files = ['src/a.ts', 'notes.md', '.env.example', 'src/deleted.ts'];
      const git =
        (stdout: string, code = 0): Run =>
        () =>
          Promise.resolve({ code, stdout, stderr: 'no', missing: false });
      const lines: string[] = [];
      expect(await main(git(files.join('\0')), root, (line) => lines.push(line))).toBe(1);
      expect(lines).toEqual([
        `env-names: src/a.ts:1: ${planted} contains KEY, TOKEN or SECRET`,
        'env-names: 2 files, 2 VITE_ names, 1 failing',
      ]);
      writeFileSync(join(root, 'src', 'a.ts'), `\0binary ${planted}`);
      expect(await main(git(files.join('\0')), root, () => undefined)).toBe(0);
      writeFileSync(join(root, 'vite.config.ts'), "const env = loadEnv(mode, root, '');\n");
      expect(await main(git(files.join('\0')), root, (line) => lines.push(line))).toBe(1);
      expect(lines.at(-2)).toBe("env-names: vite.config.ts: loadEnv(mode, root, '') reads non-VITE_ names");
      await expect(main(git('', 128), root)).rejects.toThrow(/git ls-files failed/);
    } finally {
      rmSync(root, { recursive: true, force: true });
    }
  });
});
