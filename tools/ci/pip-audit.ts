/*
 * pip-audit over the Python lock (docs/PLAN.md 7.6). Usage: node tools/ci/pip-audit.ts
 * uv exports tools/py/uv.lock, every group included, as a hashed requirements file; pip-audit (the lock's dev
 * group) checks those exact versions against PyPI's advisory data without resolving or installing anything,
 * and --strict fails on a package it cannot audit. Unexpired "pypi" waivers in tools/ci/audit-waivers.json
 * become --ignore-vuln flags; an expired one fails the run.
 */
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { expired, loadWaivers, today, type Waiver } from './audit.ts';
import { repoRoot, run as realRun, type Log, type Run } from './proc.ts';

export function exportArgs(project: string, out: string): string[] {
  return ['export', '--project', project, '--locked', '--all-groups', '--no-emit-project', '--quiet'].concat([
    '--format',
    'requirements-txt',
    '--output-file',
    out,
  ]);
}

export function auditArgs(project: string, requirements: string, ignore: readonly string[]): string[] {
  return ['run', '--project', project, '--locked', 'pip-audit', '--strict', '--progress-spinner', 'off']
    .concat(['--disable-pip', '--require-hashes', '-r', requirements])
    .concat(ignore.flatMap((id) => ['--ignore-vuln', id]));
}

export function ignored(waivers: readonly Waiver[], day: string): string[] {
  return waivers.filter((w) => w.ecosystem === 'pypi' && w.expires >= day).map((w) => w.id);
}

export async function main(run: Run = realRun, root = repoRoot, log: Log = console.log): Promise<number> {
  const waivers = loadWaivers(root);
  const stale = expired(waivers, 'pypi', today());
  for (const line of stale) log(`pip-audit: ${line}`);
  if (stale.length > 0) return 1;
  const project = join(root, 'tools', 'py');
  const dir = mkdtempSync(join(tmpdir(), 'zq-pip-audit-'));
  try {
    const requirements = join(dir, 'requirements.txt');
    const exported = await run('uv', exportArgs(project, requirements), { cwd: root, capture: true });
    if (exported.missing) throw new Error('uv is not installed: see tools/py/uv-bootstrap.txt');
    if (exported.code !== 0) throw new Error(`uv export failed: ${exported.stderr.trim()}`);
    for (const id of ignored(waivers, today())) log(`pip-audit: ${id} waived (tools/ci/audit-waivers.json)`);
    return (await run('uv', auditArgs(project, requirements, ignored(waivers, today())), { cwd: root })).code;
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

if (import.meta.main) process.exitCode = await main();
