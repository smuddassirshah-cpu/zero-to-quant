import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { LABEL, flatten, main, verdict } from './label-guard.ts';

const OWNER = 'smuddassirshah-cpu';
const labeled = (
  login: string,
  at: string,
  id: number,
  name = LABEL,
  app: { slug: string } | null = null,
) => ({
  event: 'labeled',
  created_at: at,
  id,
  actor: { login },
  label: { name },
  performed_via_github_app: app,
});

describe('label guard', () => {
  it('passes when the owner applied the label last', () => {
    const events = [labeled('zq-bot', '2026-10-07T10:00:00Z', 1), labeled(OWNER, '2026-10-07T11:00:00Z', 2)];
    expect(verdict(events, 'Smuddassirshah-CPU').ok).toBe(true);
  });

  it('fails when another account applied it last, whatever the array order', () => {
    const events = [labeled('zq-bot', '2026-10-07T12:00:00Z', 3), labeled(OWNER, '2026-10-07T11:00:00Z', 2)];
    expect(verdict(events, OWNER)).toEqual({
      ok: false,
      reason: `${LABEL} was applied by zq-bot; only ${OWNER} may apply it`,
    });
  });

  it('breaks a tie on the timestamp by event id', () => {
    const at = '2026-10-07T12:00:00Z';
    expect(verdict([labeled('zq-bot', at, 5), labeled(OWNER, at, 4)], OWNER).ok).toBe(false);
  });

  it('fails a label applied through a GitHub App, even as the owner', () => {
    const events = [labeled(OWNER, '2026-10-07T12:00:00Z', 1, LABEL, { slug: 'claude' })];
    expect(verdict(events, OWNER).reason).toMatch(/through the GitHub App claude/);
  });

  it('fails without a labeled event for the label, and ignores other labels', () => {
    const events = [
      labeled(OWNER, '2026-10-07T12:00:00Z', 1, 'docs'),
      { ...labeled(OWNER, 'x', 2), event: 'unlabeled' },
    ];
    expect(verdict(events, OWNER)).toEqual({ ok: false, reason: `no labeled event for ${LABEL}` });
    expect(verdict([{ ...labeled('x', 'y', 1), actor: null }], OWNER).reason).toMatch(
      /applied by \(unknown\)/,
    );
  });

  it('reads slurped pages or a plain array, and rejects other shapes', () => {
    const e = labeled(OWNER, '2026-10-07T12:00:00Z', 1);
    expect(flatten([[e], [e]])).toHaveLength(2);
    expect(flatten([e])).toHaveLength(1);
    expect(() => flatten({})).toThrow(/JSON array/);
    expect(() => flatten([[{ id: 1 }]])).toThrow(/lacks event/);
  });

  it('runs from a file and the owner login', () => {
    const dir = mkdtempSync(join(tmpdir(), 'zq-label-guard-'));
    try {
      const file = join(dir, 'events.json');
      writeFileSync(file, JSON.stringify([[labeled('zq-bot', '2026-10-07T12:00:00Z', 1)]]));
      const lines: string[] = [];
      expect(main([file, OWNER], (line) => lines.push(line))).toBe(1);
      writeFileSync(file, JSON.stringify([[labeled(OWNER, '2026-10-07T12:00:00Z', 1)]]));
      expect(main([file, OWNER], (line) => lines.push(line))).toBe(0);
      expect(main([file], (line) => lines.push(line))).toBe(2);
      expect(lines[1]).toBe(`label-guard: ${LABEL} applied by ${OWNER} at 2026-10-07T12:00:00Z`);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });
});
