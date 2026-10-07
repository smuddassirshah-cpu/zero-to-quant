import { mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { describe, expect, it } from 'vitest';
import { LABEL, firstSuite, flatten, main, verdict } from './label-guard.ts';

const OWNER = 'smuddassirshah-cpu';
// The head commit's earliest check suite: every label below is applied after it unless a test says otherwise.
const HEAD = '2026-10-07T09:00:00Z';
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
  it('passes when the owner applied the label last, after the head commit arrived', () => {
    const events = [labeled('zq-bot', '2026-10-07T10:00:00Z', 1), labeled(OWNER, '2026-10-07T11:00:00Z', 2)];
    expect(verdict(events, 'Smuddassirshah-CPU', HEAD).ok).toBe(true);
  });

  it('fails when another account applied it last, whatever the array order', () => {
    const events = [labeled('zq-bot', '2026-10-07T12:00:00Z', 3), labeled(OWNER, '2026-10-07T11:00:00Z', 2)];
    expect(verdict(events, OWNER, HEAD)).toEqual({
      ok: false,
      reason: `${LABEL} was applied by zq-bot; only ${OWNER} may apply it`,
    });
  });

  it('breaks a tie on the timestamp by event id', () => {
    const at = '2026-10-07T12:00:00Z';
    expect(verdict([labeled('zq-bot', at, 5), labeled(OWNER, at, 4)], OWNER, HEAD).ok).toBe(false);
  });

  it('fails a label from before the head commit arrived, at the same second, or with no check suite', () => {
    const label = [labeled(OWNER, '2026-10-07T12:00:00Z', 1)];
    expect(verdict(label, OWNER, '2026-10-07T12:30:00Z').reason).toMatch(/before the head arrived at/);
    expect(verdict(label, OWNER, '2026-10-07T12:00:00Z').ok).toBe(false);
    expect(verdict(label, OWNER, undefined).reason).toMatch(/^no check suite or label time/);
    expect(verdict([labeled(OWNER, 'not a time', 1)], OWNER, HEAD).ok).toBe(false);
  });

  it('fails a label that a later force-push made stale', () => {
    const push = { event: 'head_ref_force_pushed', created_at: '2026-10-07T13:00:00Z', id: 9, actor: null };
    const label = labeled(OWNER, '2026-10-07T12:00:00Z', 1);
    expect(verdict([label, push], OWNER, HEAD).reason).toMatch(/force-pushed at 2026-10-07T13:00:00Z/);
    expect(verdict([push, labeled(OWNER, '2026-10-07T14:00:00Z', 10)], OWNER, HEAD).ok).toBe(true);
  });

  it('fails a label applied through a GitHub App, even as the owner', () => {
    const events = [labeled(OWNER, '2026-10-07T12:00:00Z', 1, LABEL, { slug: 'claude' })];
    expect(verdict(events, OWNER, HEAD).reason).toMatch(/through the GitHub App claude/);
  });

  it('fails without a labeled event for the label, and ignores other labels', () => {
    const events = [
      labeled(OWNER, '2026-10-07T12:00:00Z', 1, 'docs'),
      { ...labeled(OWNER, 'x', 2), event: 'unlabeled' },
    ];
    expect(verdict(events, OWNER, HEAD)).toEqual({ ok: false, reason: `no labeled event for ${LABEL}` });
    const anonymous = [{ ...labeled('x', '2026-10-07T12:00:00Z', 1), actor: null }];
    expect(verdict(anonymous, OWNER, HEAD).reason).toMatch(/applied by \(unknown\)/);
  });

  it('reads slurped pages or a plain array, and rejects other shapes', () => {
    const e = labeled(OWNER, '2026-10-07T12:00:00Z', 1);
    expect(flatten([[e], [e]])).toHaveLength(2);
    expect(flatten([e])).toHaveLength(1);
    expect(() => flatten({})).toThrow(/JSON array/);
    expect(() => flatten([[{ id: 1 }]])).toThrow(/lacks event/);
  });

  it('takes the earliest check suite from slurped pages or one page', () => {
    const page = (...times: unknown[]) => ({
      total_count: times.length,
      check_suites: times.map((t) => ({ created_at: t })),
    });
    expect(firstSuite([page('2026-10-07T10:00:00Z', 'junk'), page('2026-10-07T09:00:00Z')])).toBe(
      '2026-10-07T09:00:00Z',
    );
    expect(firstSuite(page('2026-10-07T10:00:00Z'))).toBe('2026-10-07T10:00:00Z');
    expect(firstSuite([page()])).toBeUndefined();
    expect(firstSuite([null, { check_suites: 'x' }, page(7)])).toBeUndefined();
  });

  it('runs from the two files and the owner login', () => {
    const dir = mkdtempSync(join(tmpdir(), 'zq-label-guard-'));
    try {
      const [events, suites] = [join(dir, 'events.json'), join(dir, 'suites.json')];
      writeFileSync(suites, JSON.stringify([{ check_suites: [{ created_at: HEAD }] }]));
      writeFileSync(events, JSON.stringify([[labeled('zq-bot', '2026-10-07T12:00:00Z', 1)]]));
      const lines: string[] = [];
      const log = (line: string) => lines.push(line);
      expect(main([events, OWNER, suites], log)).toBe(1);
      writeFileSync(events, JSON.stringify([[labeled(OWNER, '2026-10-07T12:00:00Z', 1)]]));
      expect(main([events, OWNER, suites], log)).toBe(0);
      expect(main([events, OWNER], log)).toBe(2);
      expect(lines[1]).toBe(
        `label-guard: ${LABEL} applied by ${OWNER} at 2026-10-07T12:00:00Z, after the head at ${HEAD}`,
      );
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });
});
