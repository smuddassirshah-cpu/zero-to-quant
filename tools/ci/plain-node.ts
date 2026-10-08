/*
 * Imports every module of every @zq/ workspace package in a plain Node process with no DOM globals
 * (docs/ARCHITECTURE.md 4.3: the shared packages run unchanged in Node and the browser, and a CI test
 * imports them this way). Usage: node tools/ci/plain-node.ts
 * Decision notes:
 * - A package's modules are what its `exports` map reaches: wildcard subpaths are expanded against the
 *   files on disk, so a module a later stage adds is imported without editing this file. Only string
 *   targets are read; a null or conditional target, whose precedence this tool does not model, is refused.
 * - Each module is imported by its bare specifier from the repository root, through the workspace link and
 *   the package's own `exports`, as a consumer resolves it.
 * - The child is plain Node: no NODE_OPTIONS (so no preloaded shim), Node 22's one browser-named global
 *   (`navigator`) switched off by its flag, and a check that no DOM global exists before the first import.
 *   A module that reads one at import time fails with a ReferenceError naming it.
 */
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join, sep } from 'node:path';
import { repoRoot, run as realRun, type Log, type Run } from './proc.ts';

type Exports = Readonly<Record<string, unknown>>;

const DOM_GLOBALS = [
  'window',
  'self',
  'document',
  'navigator',
  'location',
  'history',
  'localStorage',
  'sessionStorage',
  'indexedDB',
  'customElements',
  'requestAnimationFrame',
  'getComputedStyle',
  'Element',
  'HTMLElement',
  'Node',
];

// Runs in the child as an ES module; the specifiers arrive as arguments, never in the code string.
const CHILD = `
const present = ${JSON.stringify(DOM_GLOBALS)}.filter((name) => name in globalThis);
if (present.length > 0) {
  process.stderr.write('DOM globals are defined: ' + present.join(', ') + '\\n');
  process.exit(2);
}
for (const specifier of process.argv.slice(1)) {
  try {
    await import(specifier);
    process.stdout.write(specifier + '\\n');
  } catch (error) {
    process.stderr.write(specifier + ': ' + String(error) + '\\n');
    process.exitCode = 1;
  }
}
`;

/** Every specifier `name`'s exports map resolves to one of `files` (package-relative, `/`-separated), sorted. */
export function specifiers(name: string, exports: Exports, files: readonly string[]): string[] {
  const present = new Set(files);
  const byFile = new Map<string, string>();
  for (const [key, target] of Object.entries(exports)) {
    if (typeof target !== 'string' || !target.startsWith('./') || !key.startsWith('.')) {
      throw new Error(`${name}: export ${key} is not a string target inside the package`);
    }
    const parts = target.slice(2).split('*');
    if (parts.length !== key.split('*').length || parts.length > 2) {
      throw new Error(`${name}: export ${key} needs one '*' in both key and target, or none`);
    }
    const subpath = key.slice(1);
    const [prefix = '', suffix] = parts;
    if (suffix === undefined) {
      if (present.has(prefix) && !byFile.has(prefix)) byFile.set(prefix, name + subpath);
      continue;
    }
    for (const file of files) {
      const fits =
        file.length > prefix.length + suffix.length && file.startsWith(prefix) && file.endsWith(suffix);
      if (fits && !byFile.has(file)) {
        byFile.set(file, name + subpath.replace('*', file.slice(prefix.length, file.length - suffix.length)));
      }
    }
  }
  return [...byFile.values()].sort();
}

/** A package's files, package-relative; tests, declarations and nested node_modules are not modules. */
function moduleFiles(dir: string): string[] {
  return readdirSync(dir, { recursive: true, encoding: 'utf8' })
    .map((file) => file.split(sep).join('/'))
    .filter((file) => !file.startsWith('node_modules/') && !/\.(?:test|d)\.ts$/.test(file));
}

/** The specifiers of every `packages/*` whose name starts with `@zq/`. */
export function workspaceSpecifiers(root: string): string[] {
  const packages = join(root, 'packages');
  if (!existsSync(packages)) return [];
  return readdirSync(packages, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && existsSync(join(packages, entry.name, 'package.json')))
    .flatMap((entry) => {
      const dir = join(packages, entry.name);
      const manifest = JSON.parse(readFileSync(join(dir, 'package.json'), 'utf8')) as {
        name?: unknown;
        exports?: unknown;
      };
      if (typeof manifest.name !== 'string' || !manifest.name.startsWith('@zq/')) return [];
      if (typeof manifest.exports !== 'object' || manifest.exports === null) {
        throw new Error(`${manifest.name}: package.json has no exports map`);
      }
      return specifiers(manifest.name, manifest.exports as Exports, moduleFiles(dir));
    });
}

export async function main(root = repoRoot, run: Run = realRun, log: Log = console.log): Promise<number> {
  const specs = workspaceSpecifiers(root);
  if (specs.length === 0) {
    log('plain-node: no @zq/ package found');
    return 1;
  }
  const env = { ...process.env };
  delete env.NODE_OPTIONS;
  const args = ['--no-experimental-global-navigator', '--input-type=module', '-e', CHILD, '--', ...specs];
  const result = await run(process.execPath, args, { cwd: root, env, capture: true });
  for (const line of result.stderr.split('\n')) if (line !== '') log(`plain-node: ${line}`);
  const imported = result.stdout.split('\n').filter((line) => line !== '');
  log(`plain-node: ${imported.length} of ${specs.length} modules imported in plain Node`);
  return result.code === 0 && imported.length === specs.length ? 0 : 1;
}

if (import.meta.main) process.exitCode = await main();
