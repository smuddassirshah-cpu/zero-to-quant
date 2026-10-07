// Release budgets per target (docs/ARCHITECTURE.md 6.2.3 and 6.2.5): `node tools/release/budgets.ts
// <web|artifact> <dir>` exits 1 and names the largest groups when a file or the release breaks one.
// Decision notes:
// - Artifact: only the host's served types. Archives, WebAssembly and fonts get messages of their own,
//   because each breaks a different rule (CLAUDE.md hard rule 1); a root `preflight.js` is reserved by
//   the host; anything under a dot-name is refused, since nothing hidden belongs in a release.
// - The host's 16 MB per text file is read as 16,000,000 bytes [our choice: the stricter reading].
// - Web: 25 MiB per file and 20,000 files are Cloudflare Pages' limits [recalled, unverified]. Source
//   maps stay CI artefacts, so they are listed as not deployed and left out of every count.
// - Symbolic links and special files fail on both targets: a link could publish what no build wrote.
// - One pass over the files, O(n); sorting the listing and the report's groups is O(n log n).
import { existsSync, readdirSync, statSync } from 'node:fs';
import { extname, join, relative, sep } from 'node:path';

export type Target = 'web' | 'artifact';

export interface FileEntry {
  readonly path: string;
  readonly size: number;
}

export interface Violation {
  readonly path: string;
  readonly message: string;
}

export const LIMITS = {
  artifact: { fileBytes: 16_000_000, files: 230, releaseBytes: 150_000_000 },
  web: { fileBytes: 25 * 1024 * 1024, files: 20_000, releaseBytes: Infinity },
} as const;

const SERVED = new Set(['.html', '.js', '.mjs', '.css', '.json', '.svg']);
const ARCHIVES = new Set(['.zip', '.tar', '.gz', '.tgz', '.br', '.zst', '.7z', '.rar', '.bz2', '.xz']);
const FONTS = new Set(['.woff', '.woff2', '.ttf', '.otf', '.eot']);
const RELEASE = '(release)';
const IRREGULAR = 'not a regular file: links are not published';
const USAGE = 'Usage: node tools/release/budgets.ts <web|artifact> <dir>';

const n = (value: number): string => value.toLocaleString('en-GB');
const plural = (count: number, noun: string): string => `${n(count)} ${noun}${count === 1 ? '' : 's'}`;

function artifactTypeRule(path: string): string | undefined {
  if (path.split('/').some((part) => part.startsWith('.'))) {
    return 'dotfile or dot-folder: nothing hidden is published (a leftover .vite/ manifest is the usual cause)';
  }
  if (path === 'preflight.js') {
    return 'a root preflight.js is reserved by the host, which runs it against open pages on every publish';
  }
  const ext = extname(path);
  if (SERVED.has(ext)) return undefined;
  const lower = ext.toLowerCase();
  if (ARCHIVES.has(lower)) return 'archive: the Artifact publishes no archives or other binaries';
  if (lower === '.wasm') return 'WebAssembly: the Artifact publishes no binaries; it belongs to the web app';
  if (FONTS.has(lower)) return 'font file: the Artifact takes fonts only from Google Fonts';
  return `${ext || 'no extension'}: the host serves only ${[...SERVED].join(' ')}`;
}

/** Splits off what the target never deploys: the web build's hidden source maps. */
export function partition(
  target: Target,
  files: readonly FileEntry[],
): { deployed: FileEntry[]; skipped: FileEntry[] } {
  const deployed: FileEntry[] = [];
  const skipped: FileEntry[] = [];
  for (const file of files) (target === 'web' && file.path.endsWith('.map') ? skipped : deployed).push(file);
  return { deployed, skipped };
}

export function checkBudgets(target: Target, files: readonly FileEntry[]): Violation[] {
  const limits = LIMITS[target];
  const { deployed } = partition(target, files);
  const violations: Violation[] = [];
  const fail = (path: string, message: string) => violations.push({ path, message });
  let bytes = 0;
  for (const { path, size } of deployed) {
    bytes += size;
    const type = target === 'artifact' ? artifactTypeRule(path) : undefined;
    if (type) fail(path, type);
    if (size > limits.fileBytes) {
      fail(path, `${n(size)} bytes is over the limit of ${n(limits.fileBytes)} per file`);
    }
  }
  if (deployed.length > limits.files) {
    fail(RELEASE, `${plural(deployed.length, 'file')} is over the limit of ${n(limits.files)}`);
  }
  if (bytes > limits.releaseBytes) {
    fail(RELEASE, `${n(bytes)} bytes is over the limit of ${n(limits.releaseBytes)}`);
  }
  return violations;
}

export const byFolder = (path: string): string => {
  const slash = path.indexOf('/');
  return slash === -1 ? '(root)' : `${path.slice(0, slash)}/`;
};

export const byExtension = (path: string): string => extname(path).toLowerCase() || '(none)';

export function largestGroups(
  files: readonly FileEntry[],
  keyOf: (path: string) => string,
  top = 5,
): { key: string; files: number; bytes: number }[] {
  const groups = new Map<string, { files: number; bytes: number }>();
  for (const file of files) {
    const key = keyOf(file.path);
    const group = groups.get(key) ?? { files: 0, bytes: 0 };
    group.files += 1;
    group.bytes += file.size;
    groups.set(key, group);
  }
  return [...groups]
    .map(([key, group]) => ({ key, ...group }))
    .sort((a, b) => b.bytes - a.bytes || a.key.localeCompare(b.key))
    .slice(0, top);
}

/** Every file under `dir`, with `/`-separated relative paths; links and special files apart. */
export function listFiles(dir: string): { files: FileEntry[]; irregular: string[] } {
  const files: FileEntry[] = [];
  const irregular: string[] = [];
  for (const entry of readdirSync(dir, { recursive: true, withFileTypes: true })) {
    if (entry.isDirectory()) continue;
    const full = join(entry.parentPath, entry.name);
    const path = relative(dir, full).split(sep).join('/');
    if (entry.isFile()) files.push({ path, size: statSync(full).size });
    else irregular.push(path);
  }
  files.sort((a, b) => (a.path < b.path ? -1 : 1));
  irregular.sort();
  return { files, irregular };
}

export function main(argv: readonly string[], print: (line: string) => void = console.log): number {
  const [target, dir] = argv;
  if (argv.length !== 2 || (target !== 'web' && target !== 'artifact') || dir === undefined) {
    print(USAGE);
    return 2;
  }
  if (!existsSync(dir) || !statSync(dir).isDirectory()) {
    print(`budgets: ${dir} is not a directory; build the ${target} target first`);
    return 2;
  }
  const { files, irregular } = listFiles(dir);
  const { deployed, skipped } = partition(target, files);
  const links = irregular.map((path) => ({ path, message: IRREGULAR }));
  const violations = [...links, ...checkBudgets(target, files)];
  const bytes = deployed.reduce((sum, file) => sum + file.size, 0);
  const maps = skipped.map((file) => file.path).join(', ');
  if (violations.length === 0) {
    const tail = maps ? `; not deployed: ${maps}` : '';
    print(`budgets ${target}: ${plural(deployed.length, 'file')}, ${n(bytes)} bytes, within budget${tail}`);
    return 0;
  }
  print(`budgets ${target}: ${plural(violations.length, 'violation')} in ${dir}`);
  for (const violation of violations) print(`  ${violation.path}: ${violation.message}`);
  for (const [label, keyOf] of [
    ['folder', byFolder],
    ['extension', byExtension],
  ] as const) {
    print(`Largest groups by ${label}:`);
    for (const group of largestGroups(deployed, keyOf)) {
      print(`  ${group.key}: ${plural(group.files, 'file')}, ${n(group.bytes)} bytes`);
    }
  }
  if (maps) print(`Not deployed: ${maps}`);
  return 1;
}

if (import.meta.main) process.exitCode = main(process.argv.slice(2));
