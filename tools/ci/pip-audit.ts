/*
 * pip-audit over the Python lock (docs/PLAN.md 7.6). Usage: node tools/ci/pip-audit.ts
 * uv exports tools/py/uv.lock, every group included, as a hashed requirements file. pip-audit runs from the
 * lock's dev group alone (uv run --only-group dev, so the scientific stack is not installed to audit it) and
 * looks each exact version up in PyPI's advisory data without resolving it (--disable-pip); --strict fails on
 * a package it cannot audit. Its JSON report is judged as npm's is (audit.ts): "pypi" waivers in
 * tools/ci/audit-waivers.json match an advisory's id or alias, an expired waiver fails, an unused one is
 * reported. pip-audit has no severity, so every advisory counts.
 */
import { existsSync, mkdtempSync, readFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { evaluate, loadWaivers, today, type Advisory } from './audit.ts';
import { repoRoot, run as realRun, type Log, type Run } from './proc.ts';

export function exportArgs(project: string, out: string): string[] {
  return ['export', '--project', project, '--locked', '--all-groups', '--no-emit-project', '--quiet'].concat([
    '--format',
    'requirements-txt',
    '--output-file',
    out,
  ]);
}

export function auditArgs(project: string, requirements: string, report: string): string[] {
  return ['run', '--project', project, '--locked', '--only-group', 'dev', 'pip-audit', '--strict']
    .concat(['--progress-spinner', 'off', '--disable-pip', '--require-hashes', '-r', requirements])
    .concat(['--format', 'json', '--output', report]);
}

/** PEP 503 normalised project name, so `Typing_Extensions` and `typing-extensions` match. */
export const normalise = (name: string): string => name.toLowerCase().replace(/[-_.]+/g, '-');

const isRecord = (v: unknown): v is Record<string, unknown> => typeof v === 'object' && v !== null;
const strings = (v: unknown): string[] => (Array.isArray(v) ? v.filter((x) => typeof x === 'string') : []);

/** Advisories from pip-audit's JSON report; a skipped package fails, as --strict means it to. */
export function pipAdvisories(report: unknown): Advisory[] {
  if (!isRecord(report) || !Array.isArray(report.dependencies)) {
    throw new Error('pip-audit report has no dependencies list');
  }
  const found = new Map<string, Advisory>();
  for (const dep of report.dependencies.filter(isRecord)) {
    const name = normalise(String(dep.name));
    const skipped = dep.skip_reason;
    if (skipped !== undefined) {
      throw new Error(
        `pip-audit skipped ${name}: ${typeof skipped === 'string' ? skipped : JSON.stringify(skipped)}`,
      );
    }
    for (const v of (Array.isArray(dep.vulns) ? dep.vulns : []).filter(isRecord)) {
      const id = String(v.id);
      const fixes = strings(v.fix_versions).join(', ') || 'none';
      const title = `${String(dep.version)}, fixed in ${fixes}`;
      found.set(`${id} ${name}`, {
        id,
        aliases: strings(v.aliases),
        package: name,
        severity: 'unrated',
        title,
      });
    }
  }
  return [...found.values()];
}

export async function main(run: Run = realRun, root = repoRoot, log: Log = console.log): Promise<number> {
  const waivers = loadWaivers(root).map((w) =>
    w.ecosystem === 'pypi' ? { ...w, package: normalise(w.package) } : w,
  );
  const project = join(root, 'tools', 'py');
  const dir = mkdtempSync(join(tmpdir(), 'zq-pip-audit-'));
  try {
    const [requirements, report] = [join(dir, 'requirements.txt'), join(dir, 'report.json')];
    const exported = await run('uv', exportArgs(project, requirements), { cwd: root, capture: true });
    if (exported.missing) throw new Error('uv is not installed: see tools/py/uv-bootstrap.txt');
    if (exported.code !== 0) throw new Error(`uv export failed: ${exported.stderr.trim()}`);
    // pip-audit exits 1 whenever it finds an advisory, waived or not; the report decides.
    const audited = await run('uv', auditArgs(project, requirements, report), { cwd: root, capture: true });
    if (!existsSync(report)) throw new Error(`pip-audit wrote no report: ${audited.stderr.trim()}`);
    const advisories = pipAdvisories(JSON.parse(readFileSync(report, 'utf8')));
    const { failures, waived, unused } = evaluate(advisories, waivers, 'low', today(), 'pypi');
    for (const line of waived) log(`pip-audit: ${line}`);
    for (const id of unused) log(`pip-audit: waiver ${id} matches no advisory: remove it`);
    for (const line of failures) log(`pip-audit: ${line}`);
    log(`pip-audit: ${advisories.length} advisories, ${failures.length} failing`);
    return failures.length === 0 ? 0 : 1;
  } catch (error) {
    log(`pip-audit: ${error instanceof Error ? error.message : String(error)}`);
    return 1;
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

if (import.meta.main) process.exitCode = await main();
