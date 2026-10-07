/*
 * No secret-looking VITE_ names (docs/PLAN.md 7.1, ARCHITECTURE.md 11.4). Usage: node tools/ci/env-names.ts
 * Vite inlines every VITE_ variable into the bundle, so a name containing KEY, TOKEN or SECRET fails, taken
 * literally as the plan words it. Scope: tracked files under the code directories, every root file but prose
 * and the lockfile, and every .env*.example anywhere. One pass over each file.
 */
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { repoRoot, run as realRun, type Log, type Run } from './proc.ts';

const DIRS = ['src/', 'tools/', 'packages/', 'proxy/', 'tests/', '.github/'];
const ROOT_SKIPPED = /^(?:.*\.md|LICENSE|package-lock\.json)$/;
const NAME = /\bVITE_[A-Z0-9_]+/g;
const FORBIDDEN = /KEY|TOKEN|SECRET/;

export function inScope(path: string): boolean {
  if (DIRS.some((dir) => path.startsWith(dir))) return true;
  if (/(?:^|\/)\.env[^/]*\.example$/.test(path)) return true;
  return !path.includes('/') && !ROOT_SKIPPED.test(path);
}

export interface Finding {
  readonly path: string;
  readonly line: number;
  readonly name: string;
}

export function findNames(path: string, text: string): Finding[] {
  return text
    .split('\n')
    .flatMap((line, i) => [...line.matchAll(NAME)].map((m) => ({ path, line: i + 1, name: m[0] })));
}

export const forbidden = (findings: readonly Finding[]): Finding[] =>
  findings.filter((f) => FORBIDDEN.test(f.name));

export async function main(run: Run = realRun, root = repoRoot, log: Log = console.log): Promise<number> {
  const listed = await run('git', ['ls-files', '-z'], { cwd: root, capture: true });
  if (listed.code !== 0) throw new Error(`git ls-files failed: ${listed.stderr.trim()}`);
  const paths = listed.stdout.split('\0').filter((p) => p !== '' && inScope(p) && existsSync(join(root, p)));
  const findings = paths.flatMap((p) => {
    const text = readFileSync(join(root, p), 'utf8');
    return text.includes('\0') ? [] : findNames(p, text);
  });
  const bad = forbidden(findings);
  for (const f of bad) log(`env-names: ${f.path}:${f.line}: ${f.name} contains KEY, TOKEN or SECRET`);
  const names = new Set(findings.map((f) => f.name));
  log(`env-names: ${paths.length} files, ${names.size} VITE_ names, ${bad.length} forbidden`);
  return bad.length === 0 ? 0 : 1;
}

if (import.meta.main) process.exitCode = await main();
