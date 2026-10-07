import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import { main, readManifest, renderPage } from './page.ts';

const assets = { entry: 'assets/app.CEUOy4jd.js', stylesheet: 'assets/app.CfLytedv.css' };
const manifest = {
  'artifact.html': { file: assets.entry, name: 'app', src: 'artifact.html', isEntry: true },
  'style.css': { file: assets.stylesheet, src: 'style.css' },
};

const temps: string[] = [];
afterEach(() => {
  for (const dir of temps.splice(0)) rmSync(dir, { recursive: true, force: true });
});

describe('renderPage', () => {
  const page = renderPage(assets);

  it('writes the fragment in the order of ARCHITECTURE.md 6.2.2', () => {
    let at = 0;
    for (const part of [
      '<meta charset="utf-8">',
      '<title>Zero to Quant</title>',
      '<link rel="preconnect" href="https://fonts.googleapis.com">',
      '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
      'family=Archivo:wdth,wght@62..125,100..900&family=Besley:ital,wght@0,400..900;1,400..900&family=Source+Code+Pro',
      '<link rel="stylesheet" href="./assets/app.CfLytedv.css">',
      '<div id="app"></div>',
      '<script>',
      'window.__zqOld = true',
      '</script>',
      '<script>',
      'if (window.__zqOld) return;',
      "import('./assets/app.CEUOy4jd.js')",
      '</script>',
    ]) {
      const found = page.indexOf(part, at);
      expect(found, part).toBeGreaterThanOrEqual(0);
      at = found + part.length;
    }
    expect(page.startsWith('<meta charset="utf-8">')).toBe(true);
  });

  const [gate = '', bootstrap = ''] = page.split('</script>');

  it('gates old browsers in a script of its own, which never names import()', () => {
    expect(gate).toContain("typeof structuredClone === 'function'");
    expect(gate).toContain("typeof [].at === 'function'");
    expect(gate).toContain("CSS.supports('transition-timing-function', 'linear(0, 1)')");
    expect(gate).toContain("textContent = 'This browser is too old for Zero to Quant.'");
    expect(gate).not.toContain('import(');
  });

  it('bootstraps only past the gate and reports a failed start without an empty catch', () => {
    expect(bootstrap.indexOf('if (window.__zqOld) return;')).toBeLessThan(bootstrap.indexOf('import('));
    expect(bootstrap).toContain("textContent = 'Zero to Quant could not start. Reload to try again.'");
    expect(bootstrap).toContain('console.error(error)');
  });

  it('uses two classic scripts, no module script and no raw HTML sink', () => {
    expect(page.match(/<script>/g)).toHaveLength(2);
    expect(page.match(/<script/g)).toHaveLength(2);
    expect(page).not.toContain('type="module"');
    expect(page).not.toContain('innerHTML');
  });

  it.each([
    [{ ...assets, entry: 'assets/app.js"><script>alert(1)</script>' }],
    [{ ...assets, entry: '../secret/app.js' }],
    [{ ...assets, entry: 'https://example.com/app.js' }],
    [{ ...assets, entry: 'assets/sub/app.js' }],
    [{ ...assets, entry: assets.stylesheet }],
    [{ ...assets, stylesheet: assets.entry }],
    [{ ...assets, stylesheet: 'assets/app.css?x=1' }],
  ])('refuses a bad path: %j', (bad) => {
    expect(() => renderPage(bad)).toThrow(/^Refusing /);
  });
});

describe('readManifest', () => {
  it('finds the entry chunk and the stylesheet', () => {
    expect(readManifest(manifest)).toEqual(assets);
  });

  it.each([
    [null, /not an object/],
    [[], /not an object/],
    [{ 'style.css': manifest['style.css'] }, /found 0/],
    [{ ...manifest, other: { file: 'assets/o.js', isEntry: true } }, /found 2/],
    [{ a: { isEntry: true, file: 3 }, 'style.css': manifest['style.css'] }, /names no file/],
    [{ 'artifact.html': manifest['artifact.html'] }, /no style\.css/],
  ])('rejects %j', (bad, message) => {
    expect(() => readManifest(bad)).toThrow(message);
  });
});

describe('main', () => {
  function build(files: Record<string, string>): string {
    const root = mkdtempSync(join(tmpdir(), 'zq-page-'));
    temps.push(root);
    const dir = join(root, 'artifact');
    for (const [path, text] of Object.entries(files)) {
      mkdirSync(join(dir, path, '..'), { recursive: true });
      writeFileSync(join(dir, path), text);
    }
    return dir;
  }
  function run(argv: string[]): { code: number; lines: string[] } {
    const lines: string[] = [];
    return { code: main(argv, (line) => lines.push(line)), lines };
  }
  const withoutStylesheet = {
    'index.html': '<!doctype html><script type="module" src="../../assets/x.js"></script>',
    '.vite/manifest.json': JSON.stringify(manifest),
    [assets.entry]: '',
  };
  const complete = { ...withoutStylesheet, [assets.stylesheet]: '' };

  it('rewrites the page, moves the manifest beside the folder and removes .vite/', () => {
    const dir = build(complete);
    const { code, lines } = run([dir]);
    expect(code).toBe(0);
    expect(lines[0]).toMatch(/^page: wrote index\.html for assets\/app\.CEUOy4jd\.js/);
    expect(readFileSync(join(dir, 'index.html'), 'utf8')).toBe(renderPage(assets));
    expect(JSON.parse(readFileSync(`${dir}-manifest.json`, 'utf8'))).toEqual(manifest);
    expect(existsSync(join(dir, '.vite'))).toBe(false);
  });

  it('fails without a manifest, or when the manifest names a missing file', () => {
    expect(run([]).code).toBe(2);
    const bare = build({ 'index.html': '' });
    expect(run([bare])).toMatchObject({ code: 1, lines: [expect.stringMatching(/no Vite manifest/)] });
    const partial = build(withoutStylesheet);
    expect(run([partial])).toMatchObject({
      code: 1,
      lines: [expect.stringMatching(/names assets\/app\..*\.css/)],
    });
    expect(existsSync(join(partial, '.vite', 'manifest.json'))).toBe(true);
  });
});
