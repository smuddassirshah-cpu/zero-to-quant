/*
 * Licence allow-lists over package-lock.json (docs/PLAN.md 7.6). Usage: node tools/ci/licences.ts
 * - Shipped means reachable from a production root: the root's dependencies and optionalDependencies, and every
 *   workspace the root does not list in devDependencies (a workspace ships unless declared otherwise, so the
 *   default fails closed). Edges are dependencies, optionalDependencies and installed peerDependencies, resolved
 *   the way Node does, nearest node_modules first. npm's own `dev` flag is not used: it marks the peers of a
 *   development workspace (eslint for eslint-plugin-zq) as production. Everything else installed is development.
 * - SPDX expressions with OR, AND, WITH and parentheses; WITH adds an exception to a licence and is judged by the
 *   licence. A missing, unparsable or unknown licence fails unless tools/ci/licences.exceptions.json lists that
 *   exact name and version, with the reason and the docs/DECISIONS.md entry. An exception that matches nothing
 *   fails too, so the list cannot go stale. O(n) in lockfile entries.
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { repoRoot, type Log } from './proc.ts';

const SHIPPED = ['MIT', 'ISC', 'BSD-2-Clause', 'BSD-3-Clause', 'Apache-2.0', 'MPL-2.0', 'OFL-1.1'];
const DEVELOPMENT = [...SHIPPED, '0BSD', 'BlueOak-1.0.0', 'CC0-1.0', 'CC-BY-4.0', 'Python-2.0'];
export const ALLOWED = { shipped: new Set(SHIPPED), development: new Set(DEVELOPMENT) };

type Expr =
  { readonly id: string } | { readonly op: 'AND' | 'OR'; readonly left: Expr; readonly right: Expr };

export function parseSpdx(text: string): Expr {
  const tokens = text.match(/\(|\)|[^\s()]+/g) ?? [];
  let at = 0;
  const peek = () => tokens[at];
  const take = () => tokens[at++];
  const primary = (): Expr => {
    const token = take();
    if (token === '(') {
      const inner = or();
      if (take() !== ')') throw new Error(`unbalanced parentheses in "${text}"`);
      return inner;
    }
    if (token === undefined || token === ')' || /^(AND|OR|WITH)$/.test(token)) {
      throw new Error(`expected a licence in "${text}"`);
    }
    if (peek() === 'WITH') {
      take();
      const exception = take();
      if (exception === undefined || exception === '(' || exception === ')') {
        throw new Error(`expected an exception after WITH in "${text}"`);
      }
    }
    return { id: token };
  };
  const chain = (op: 'AND' | 'OR', next: () => Expr) => (): Expr => {
    let left = next();
    while (peek() === op) {
      take();
      left = { op, left, right: next() };
    }
    return left;
  };
  const and = chain('AND', primary);
  const or = chain('OR', and);
  const expr = or();
  if (at !== tokens.length) throw new Error(`unexpected "${tokens[at] ?? ''}" in "${text}"`);
  return expr;
}

export function satisfies(expr: Expr, allowed: ReadonlySet<string>): boolean {
  if ('id' in expr) return allowed.has(expr.id);
  const [l, r] = [satisfies(expr.left, allowed), satisfies(expr.right, allowed)];
  return expr.op === 'AND' ? l && r : l || r;
}

interface Entry {
  readonly version?: string;
  readonly license?: string;
  readonly link?: boolean;
  readonly resolved?: string;
  readonly dependencies?: Record<string, string>;
  readonly optionalDependencies?: Record<string, string>;
  readonly peerDependencies?: Record<string, string>;
  readonly devDependencies?: Record<string, string>;
}
export interface Installed {
  readonly key: string;
  readonly name: string;
  readonly version: string;
  readonly licence: string | undefined;
  readonly shipped: boolean;
}

const nameOf = (key: string) => key.slice(key.lastIndexOf('node_modules/') + 'node_modules/'.length);
const parentOf = (key: string) => {
  const i = key.lastIndexOf('/node_modules/');
  return i >= 0 ? key.slice(0, i) : '';
};

/** Every installed package with its shipped or development class. Links and workspace sources are ours. */
export function classify(lock: { readonly packages?: Record<string, Entry> }): Installed[] {
  const packages = lock.packages;
  if (packages?.[''] === undefined)
    throw new Error('package-lock.json has no packages[""]: lockfile v3 needed');
  const resolve = (from: string, dep: string): string | undefined => {
    for (let base = from; ; base = parentOf(base)) {
      const key = base === '' ? `node_modules/${dep}` : `${base}/node_modules/${dep}`;
      const entry = packages[key];
      if (entry !== undefined) return entry.link === true ? entry.resolved : key;
      if (base === '') return undefined;
    }
  };
  const root = packages[''];
  const dev = new Set(Object.keys(root.devDependencies ?? {}));
  const links = Object.entries(packages).filter(([, e]) => e.link === true);
  const roots = [
    ...Object.keys({ ...root.dependencies, ...root.optionalDependencies }),
    ...links.map(([key]) => nameOf(key)).filter((name) => !dev.has(name)),
  ];
  const shipped = new Set<string>();
  const queue = roots.flatMap((name) => resolve('', name) ?? []);
  for (let key = queue.pop(); key !== undefined; key = queue.pop()) {
    if (shipped.has(key)) continue;
    shipped.add(key);
    const entry = packages[key];
    for (const [deps, required] of [
      [entry?.dependencies, true],
      [entry?.optionalDependencies, false],
      [entry?.peerDependencies, false],
    ] as const) {
      for (const dep of Object.keys(deps ?? {})) {
        const target = resolve(key, dep);
        if (target !== undefined) queue.push(target);
        else if (required) throw new Error(`${key} depends on ${dep}, which the lockfile does not hold`);
      }
    }
  }
  return Object.entries(packages)
    .filter(([key, e]) => key.includes('node_modules/') && e.link !== true)
    .map(([key, e]) => ({
      key,
      name: nameOf(key),
      version: e.version ?? '?',
      licence: e.license,
      shipped: shipped.has(key),
    }));
}

export interface LicenceException {
  readonly name: string;
  readonly version: string;
  readonly licence: string;
  readonly reason: string;
  readonly decision: string;
}

export function parseExceptions(json: unknown): LicenceException[] {
  const fields = ['name', 'version', 'licence', 'reason', 'decision'] as const;
  if (!Array.isArray(json)) throw new Error('licences.exceptions.json must be an array');
  return json.map((item: unknown, i) => {
    const ok =
      typeof item === 'object' &&
      item !== null &&
      fields.every((f) => f in item && typeof (item as Record<string, unknown>)[f] === 'string');
    if (!ok) throw new Error(`licences.exceptions.json entry ${i} needs string ${fields.join(', ')}`);
    return item as LicenceException;
  });
}

export function check(installed: readonly Installed[], exceptions: readonly LicenceException[]) {
  const failures: string[] = [];
  const counts = { shipped: new Map<string, number>(), development: new Map<string, number>() };
  const used = new Set<LicenceException>();
  for (const pkg of installed) {
    const kind = pkg.shipped ? 'shipped' : 'development';
    const label = pkg.licence ?? '(none)';
    counts[kind].set(label, (counts[kind].get(label) ?? 0) + 1);
    let ok: boolean;
    try {
      ok = pkg.licence !== undefined && satisfies(parseSpdx(pkg.licence), ALLOWED[kind]);
    } catch (error) {
      failures.push(`${pkg.name}@${pkg.version}: ${error instanceof Error ? error.message : String(error)}`);
      continue;
    }
    if (ok) continue;
    const exception = exceptions.find((x) => x.name === pkg.name && x.version === pkg.version);
    if (exception !== undefined && (pkg.licence === undefined || pkg.licence === exception.licence)) {
      used.add(exception);
    } else {
      failures.push(`${pkg.name}@${pkg.version} (${pkg.key}): ${label} is not allowed for ${kind} packages`);
    }
  }
  for (const x of exceptions) {
    if (!used.has(x)) failures.push(`exception ${x.name}@${x.version} matches no failing package: remove it`);
  }
  return { failures, counts, excepted: [...used] };
}

export function main(root = repoRoot, log: Log = console.log): number {
  const lock = JSON.parse(readFileSync(join(root, 'package-lock.json'), 'utf8')) as Parameters<
    typeof classify
  >[0];
  const exceptionsFile = join(root, 'tools', 'ci', 'licences.exceptions.json');
  const exceptions = parseExceptions(JSON.parse(readFileSync(exceptionsFile, 'utf8')));
  const installed = classify(lock);
  const { failures, counts, excepted } = check(installed, exceptions);
  for (const kind of ['shipped', 'development'] as const) {
    const sorted = [...counts[kind]].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
    const total = sorted.reduce((sum, [, n]) => sum + n, 0);
    log(`licences: ${total} ${kind}${sorted.map(([l, n]) => `\n  ${l} ${n}`).join('')}`);
  }
  for (const x of excepted) log(`licences: exception ${x.name}@${x.version} (${x.licence}), ${x.decision}`);
  for (const failure of failures) log(`licences: ${failure}`);
  return failures.length === 0 ? 0 : 1;
}

if (import.meta.main) process.exitCode = main();
