import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import type { Waiver } from './audit.ts';
import { auditArgs, exportArgs, main, normalise, pipAdvisories } from './pip-audit.ts';
import type { Run } from './proc.ts';

const waiver: Waiver = {
  id: 'GHSA-6w46-j5rx-g56g',
  package: 'PyTest',
  ecosystem: 'pypi',
  reason: 'test',
  expires: '2999-01-01',
  decision: 'docs/DECISIONS.md A0',
};

// The shape of pip-audit 2.10.1's JSON report [measured], trimmed; the duplicate is pip-audit's own.
const vuln = { id: 'PYSEC-2026-1845', fix_versions: ['9.0.3'], aliases: [waiver.id, 'CVE-2025-71176'] };
const report = {
  dependencies: [
    { name: 'boolean-py', version: '5.0', vulns: [] },
    { name: 'pytest', version: '9.0.2', vulns: [vuln, vuln] },
  ],
  fixes: [],
};

const roots: string[] = [];
afterEach(() => {
  for (const dir of roots.splice(0)) rmSync(dir, { recursive: true, force: true });
});
const root = (waivers: unknown[]) => {
  const dir = mkdtempSync(join(tmpdir(), 'zq-pip-audit-test-'));
  roots.push(dir);
  mkdirSync(join(dir, 'tools', 'ci'), { recursive: true });
  writeFileSync(join(dir, 'tools', 'ci', 'audit-waivers.json'), JSON.stringify(waivers));
  return dir;
};

/** uv as a stand-in: export succeeds, then the audit writes `body` as its report (or nothing). */
const uv =
  (body: unknown, calls: string[][] = []): Run =>
  (cmd, args) => {
    calls.push([cmd, ...args]);
    const out = args[args.indexOf('--output') + 1];
    if (args[0] === 'run' && out !== undefined && body !== undefined)
      writeFileSync(out, JSON.stringify(body));
    return Promise.resolve({ code: args[0] === 'run' ? 1 : 0, stdout: '', stderr: 'boom', missing: false });
  };

describe('pip-audit', () => {
  it('exports the whole lock and audits it from the dev group alone, without resolving', () => {
    expect(exportArgs('p', 'r.txt')).toContain('--all-groups');
    const audit = auditArgs('p', 'r.txt', 'o.json');
    expect(audit.slice(0, 7)).toEqual([
      'run',
      '--project',
      'p',
      '--locked',
      '--only-group',
      'dev',
      'pip-audit',
    ]);
    expect(audit).toEqual(expect.arrayContaining(['--strict', '--disable-pip', '--require-hashes']));
    expect(audit.slice(-4)).toEqual(['--format', 'json', '--output', 'o.json']);
  });

  it('reads advisories once each, normalising names, and fails a skipped package', () => {
    expect(normalise('Typing_Extensions')).toBe('typing-extensions');
    expect(pipAdvisories(report)).toEqual([
      {
        id: vuln.id,
        aliases: vuln.aliases,
        package: 'pytest',
        severity: 'unrated',
        title: '9.0.2, fixed in 9.0.3',
      },
    ]);
    expect(() => pipAdvisories({})).toThrow(/no dependencies list/);
    expect(() => pipAdvisories({ dependencies: [{ name: 'x', skip_reason: 'not on PyPI' }] })).toThrow(
      /skipped x: not on PyPI/,
    );
  });

  it('waives by alias, reports a waiver that matches nothing, and fails an unwaived advisory', async () => {
    const lines: string[] = [];
    const log = (line: string) => lines.push(line);
    const calls: string[][] = [];
    expect(await main(uv(report, calls), root([waiver]), log)).toBe(0);
    expect(calls.map((c) => c[1])).toEqual(['export', 'run']);
    expect(lines[0]).toMatch(/PYSEC-2026-1845 in pytest: .* \(waived until 2999-01-01/);
    expect(await main(uv({ dependencies: [] }), root([waiver]), log)).toBe(0);
    expect(lines).toContain(
      'pip-audit: waiver GHSA-6w46-j5rx-g56g for pytest matches no advisory: remove it',
    );
    expect(await main(uv(report), root([]), log)).toBe(1);
    expect(lines.at(-1)).toBe('pip-audit: 1 advisories, 1 failing');
  });

  it('fails on an expired waiver, a missing uv, a failed export and a missing report', async () => {
    const lines: string[] = [];
    const log = (line: string) => lines.push(line);
    expect(await main(uv(report), root([{ ...waiver, expires: '2000-01-01' }]), log)).toBe(1);
    expect(lines).toContain(
      'pip-audit: waiver GHSA-6w46-j5rx-g56g for pytest expired on 2000-01-01 (docs/DECISIONS.md A0)',
    );
    const missing: Run = () => Promise.resolve({ code: 127, stdout: '', stderr: '', missing: true });
    expect(await main(missing, root([]), log)).toBe(1);
    expect(lines.at(-1)).toMatch(/uv is not installed/);
    const failed: Run = () =>
      Promise.resolve({ code: 2, stdout: '', stderr: 'lock out of date', missing: false });
    expect(await main(failed, root([]), log)).toBe(1);
    expect(lines.at(-1)).toBe('pip-audit: uv export failed: lock out of date');
    expect(await main(uv(undefined), root([]), log)).toBe(1);
    expect(lines.at(-1)).toBe('pip-audit: pip-audit wrote no report: boom');
  });
});
