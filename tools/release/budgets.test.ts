import { spawnSync } from 'node:child_process';
import { cpSync, existsSync, mkdirSync, mkdtempSync, rmSync, symlinkSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { afterEach, describe, expect, it } from 'vitest';
import { byExtension, byFolder, checkBudgets, largestGroups, main, type FileEntry } from './budgets.ts';

const CLI = fileURLToPath(new URL('./budgets.ts', import.meta.url));
const BUILT = fileURLToPath(new URL('../../dist/artifact', import.meta.url));
const app: FileEntry[] = [
  { path: 'index.html', size: 1_000 },
  { path: 'assets/app.abc123.js', size: 90_000 },
  { path: 'assets/app.abc123.css', size: 40_000 },
  { path: 'content/course/numwork.abc.json', size: 2_000_000 },
  { path: 'content/gen/prob.abc.mjs', size: 30_000 },
  { path: 'content/assets/curve.abc.svg', size: 8_000 },
];
const messages = (target: 'web' | 'artifact', files: FileEntry[]) =>
  checkBudgets(target, files).map((v) => `${v.path}: ${v.message}`);
const files = (count: number, size: number, name = 'content/c') =>
  Array.from({ length: count }, (_, i) => ({ path: `${name}${i}.json`, size }));

const temps: string[] = [];
function tempDir(): string {
  const dir = mkdtempSync(join(tmpdir(), 'zq-budgets-'));
  temps.push(dir);
  return dir;
}
afterEach(() => {
  for (const dir of temps.splice(0)) rmSync(dir, { recursive: true, force: true });
});

describe('checkBudgets, artifact', () => {
  it.each([
    ['content/course/bundle.zip', /^content\/course\/bundle\.zip: archive/],
    ['assets/app.js.gz', /: archive/],
    ['py/pyodide.asm.wasm', /: WebAssembly/],
    ['preflight.js', /^preflight\.js: a root preflight\.js is reserved/],
    ['fonts/KaTeX_Main.woff2', /: font file/],
    ['.vite/manifest.json', /^\.vite\/manifest\.json: dotfile or dot-folder/],
    ['assets/.DS_Store', /: dotfile or dot-folder/],
    ['notes.txt', /^notes\.txt: \.txt: the host serves only \.html \.js \.mjs \.css \.json \.svg$/],
    ['LICENSE', /: no extension: the host serves only/],
    ['assets/app.JS', /: \.JS: the host serves only/],
  ])('fails a planted %s', (path, expected) => {
    const found = messages('artifact', [...app, { path, size: 10 }]);
    expect(found).toHaveLength(1);
    expect(found[0]).toMatch(expected);
  });

  it('passes the served types, a preflight.js below the root and a file of exactly 16,000,000 bytes', () => {
    const extra = [
      { path: 'content/preflight.js', size: 10 },
      { path: 'content/big.json', size: 16_000_000 },
    ];
    expect(checkBudgets('artifact', [...app, ...extra])).toEqual([]);
  });

  it('fails a 17 MB file, and reports type and size apart', () => {
    expect(messages('artifact', [{ path: 'content/big.json', size: 17_000_000 }])).toEqual([
      'content/big.json: 17,000,000 bytes is over the limit of 16,000,000 per file',
    ]);
    expect(messages('artifact', [{ path: 'py.zip', size: 20_000_000 }])).toHaveLength(2);
  });

  it('fails a release over 230 files or 150,000,000 bytes', () => {
    expect(checkBudgets('artifact', files(230, 1))).toEqual([]);
    expect(messages('artifact', files(231, 1))).toEqual(['(release): 231 files is over the limit of 230']);
    expect(messages('artifact', files(10, 15_000_001))).toEqual([
      '(release): 150,000,010 bytes is over the limit of 150,000,000',
    ]);
  });
});

describe('checkBudgets, web', () => {
  it('accepts any type and leaves source maps out of every count', () => {
    const maps = files(20_000, 30_000_000, 'assets/c').map((f) => ({ ...f, path: `${f.path}.map` }));
    expect(checkBudgets('web', [...app, { path: 'py/pyodide.asm.wasm', size: 9_000_000 }, ...maps])).toEqual(
      [],
    );
  });

  it('fails a file over 25 MiB and more than 20,000 files', () => {
    expect(messages('web', [{ path: 'py/big.whl', size: 26_214_401 }])).toEqual([
      'py/big.whl: 26,214,401 bytes is over the limit of 26,214,400 per file',
    ]);
    expect(messages('web', files(20_001, 1))).toEqual([
      '(release): 20,001 files is over the limit of 20,000',
    ]);
  });
});

describe('largestGroups', () => {
  it('groups by top-level folder and by extension, largest first', () => {
    expect(largestGroups(app, byFolder)).toEqual([
      { key: 'content/', files: 3, bytes: 2_038_000 },
      { key: 'assets/', files: 2, bytes: 130_000 },
      { key: '(root)', files: 1, bytes: 1_000 },
    ]);
    expect(largestGroups([...app, { path: 'LICENSE', size: 1 }], byExtension, 2)).toEqual([
      { key: '.json', files: 1, bytes: 2_000_000 },
      { key: '.js', files: 1, bytes: 90_000 },
    ]);
    expect(byExtension('LICENSE')).toBe('(none)');
  });
});

describe('main', () => {
  function run(argv: string[]): { code: number; lines: string[] } {
    const lines: string[] = [];
    const code = main(argv, (line) => lines.push(line));
    return { code, lines };
  }

  it('rejects bad arguments and a missing folder', () => {
    expect(run([]).code).toBe(2);
    expect(run(['site', 'dist/web']).lines).toEqual([
      'Usage: node tools/release/budgets.ts <web|artifact> <dir>',
    ]);
    expect(run(['web', join(tempDir(), 'absent')]).code).toBe(2);
  });

  it('prints a one-line summary within budget, naming what is not deployed', () => {
    const dir = tempDir();
    writeFileSync(join(dir, 'index.html'), 'abcd');
    writeFileSync(join(dir, 'app.js.map'), 'map');
    expect(run(['web', dir])).toEqual({
      code: 0,
      lines: ['budgets web: 1 file, 4 bytes, within budget; not deployed: app.js.map'],
    });
  });

  it('prints every violation, links included, and the largest groups, then fails', () => {
    const dir = tempDir();
    mkdirSync(join(dir, 'assets'));
    writeFileSync(join(dir, 'index.html'), 'abcd');
    writeFileSync(join(dir, 'assets', 'app.js'), 'ab');
    writeFileSync(join(dir, 'preflight.js'), 'a');
    writeFileSync(join(dir, 'app.js.map'), 'map');
    symlinkSync(join(dir, 'index.html'), join(dir, 'page.html'));
    expect(run(['artifact', dir])).toEqual({
      code: 1,
      lines: [
        `budgets artifact: 3 violations in ${dir}`,
        '  page.html: not a regular file: links are not published',
        '  app.js.map: .map: the host serves only .html .js .mjs .css .json .svg',
        '  preflight.js: a root preflight.js is reserved by the host, which runs it against open pages on every publish',
        'Largest groups by folder:',
        '  (root): 3 files, 8 bytes',
        '  assets/: 1 file, 2 bytes',
        'Largest groups by extension:',
        '  .html: 1 file, 4 bytes',
        '  .js: 2 files, 3 bytes',
        '  .map: 1 file, 3 bytes',
      ],
    });
    expect(run(['web', dir]).lines.at(-1)).toBe('Not deployed: app.js.map');
    expect(run(['web', join(dir, 'assets')]).lines).toEqual(['budgets web: 1 file, 2 bytes, within budget']);
  });
});

// Stage 1's definition of done: each planted file fails the CLI against a copy of the real build.
describe('the CLI against a copy of dist/artifact', () => {
  const built = existsSync(join(BUILT, 'index.html'));
  const title = built
    ? 'fails a planted .zip, .wasm, preflight.js and 17 MB file'
    : 'skipped: dist/artifact is absent; run npm run build:artifact first (CI builds before testing)';
  it.skipIf(!built)(title, () => {
    const dir = tempDir();
    cpSync(BUILT, dir, { recursive: true });
    const cli = () => spawnSync(process.execPath, [CLI, 'artifact', dir], { encoding: 'utf8' });
    expect(cli().status, 'the unplanted copy must pass: build it with npm run build:artifact').toBe(0);
    for (const [path, size, reason] of [
      ['content/bundle.zip', 10, 'archive'],
      ['assets/sqlite.wasm', 10, 'WebAssembly'],
      ['preflight.js', 10, 'reserved by the host'],
      ['content/big.json', 17_000_000, '17,000,000 bytes is over the limit'],
    ] as const) {
      const file = join(dir, path);
      mkdirSync(join(file, '..'), { recursive: true });
      writeFileSync(file, Buffer.alloc(size, 0x20));
      try {
        const result = cli();
        expect(result.status, path).toBe(1);
        expect(result.stdout).toContain(`  ${path}: `);
        expect(result.stdout).toContain(reason);
      } finally {
        rmSync(file);
      }
    }
  });
});
