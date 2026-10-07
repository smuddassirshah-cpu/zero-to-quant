// Spike S1: recreates npm/, the local CDN mirror that tools/build.mjs hashes and tools/test.mjs serves.
//
// Decision notes:
// - The tarballs come from the npm registry with `npm pack`, run with an argument list (no shell), and each
//   must match the SHA-512 below, the registry's own dist.integrity [measured 7 October 2026]; a mismatch
//   deletes the tarball and stops. The mirror is never committed and never published.
// - Existing unpacked folders are left alone, so a second run only fills gaps.

import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const NPM = path.join(ROOT, 'npm');

const TARBALLS = [
  ['preact@11.0.0', 'preact-11.0.0', 'sha512-LRTLKuSe6VYPhvBDjwFaX+nuZnpsw6IN2GSboisAvhGsncylBmrbDCERhgKDn6yP2mAwbGvsB5OVyTe33M8gBg=='],
  ['preact@10.29.8', 'preact-10.29.8', 'sha512-ej2aVZ+vZ8WO7tvlQWRM9N63A0KzF9q4mWJfDUHgYaIofWY9hu74QdnQrjoPMmZi2/nZ5gN0bJCQF49xQqx09Q=='],
  ['@preact/signals@2.11.3', 'preact-signals-2.11.3', 'sha512-mttwFM98G/JiriTgMwU+UWygL6sfVmYEiNcPSKkUnv4PxPpZhmP2ugGC4qi360+ZIHyQ8NY05bfJT3b4RUIGlw=='],
  ['@preact/signals-core@1.14.4', 'preact-signals-core-1.14.4', 'sha512-HNB6HYeYKhQbJ1aKl+YRjrS4+QWHLKX6qKoUsfS/m0vqzsVaEBiZiaKbG/e+NKk2ch5ALQr/ihWaMHxiCuuWHA=='],
  ['zod@4.6.5', 'zod-4.6.5', 'sha512-v5l/aFXZQeai4awLbOpSoHecE9UiMrnfx75tEXLjNonXVARxQ5mOeipTjROUchszUNCqnE+hqAMujRsRHsut2Q=='],
  ['katex@0.19.0', 'katex-0.19.0', 'sha512-v6Tznz3zJ7u3niRCoDTsumM2+HA2XXcCu+WAacCeHD2z3p9A9Ks987o5FzfTGBN0e8A0vjEgIDvLbICrXpdw/Q=='],
  ['ts-fsrs@5.4.2', 'ts-fsrs-5.4.2', 'sha512-z4qop4pzTcyTzuJ566d9EaX/4bZZzhYfeaPImfVr+xcYT65c5oBgFDijUhCE/D+C78eaolHIhKRZ04/RwF+v2g=='],
  ['fflate@0.8.3', 'fflate-0.8.3', 'sha512-tbZNuJrLwGUp3zshBtdy4W+ORxZuIh8a5ilyIEQDC5rY1f3U20JMry0Ll3WBzU58EZKsEuJFXhb5gwv8CsPvgA=='],
];

function run(cmd, args) {
  const r = spawnSync(cmd, args, { encoding: 'utf8' });
  if (r.status !== 0) throw new Error(`${cmd} ${args.join(' ')} failed: ${r.error?.message ?? r.stderr.trim()}`);
  return r.stdout;
}

fs.mkdirSync(NPM, { recursive: true });
for (const [spec, name, integrity] of TARBALLS) {
  const dir = path.join(NPM, name);
  if (fs.existsSync(path.join(dir, 'package', 'package.json'))) {
    console.log(`${spec}: already unpacked`);
    continue;
  }
  const tgz = path.join(NPM, `${name}.tgz`);
  if (!fs.existsSync(tgz)) run('npm', ['pack', spec, '--pack-destination', NPM, '--silent']);
  const got = `sha512-${createHash('sha512').update(fs.readFileSync(tgz)).digest('base64')}`;
  if (got !== integrity) {
    fs.rmSync(tgz);
    throw new Error(`${spec}: the tarball's SHA-512 is ${got}, not ${integrity}; it was deleted`);
  }
  fs.mkdirSync(dir, { recursive: true });
  run('tar', ['-xzf', tgz, '-C', dir]);
  console.log(`${spec}: verified and unpacked`);
}
