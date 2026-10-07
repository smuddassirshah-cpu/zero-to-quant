/*
 * Who applied visual-approved, and when (docs/PLAN.md 7.6; docs/DECISIONS.md G1).
 * Usage: node tools/ci/label-guard.ts <events.json> <owner-login> <check-suites.json>
 * Reads a pull request's issue events (`gh api --paginate --slurp`, so an array of pages, or a plain array) and
 * the check suites of its head commit, and passes only if the latest `labeled` event for the label was by the
 * owner, applied directly rather than through a GitHub App (performed_via_github_app set), after the head
 * commit's earliest check suite was created and after any force-push. GitHub sets a check suite's created_at
 * when the commit arrives, so the pusher cannot backdate it the way a commit date can be; no check suite, or
 * an unreadable time, fails. label-guard.yml also removes the label on every push and reopening.
 * Measured limit, 7 October 2026: the session platform's GitHub connection authenticates as the owner's own
 * account (smuddassirshah-cpu), so a label an agent applies through it may be indistinguishable from the owner's
 * own [unverified: whether its events carry performed_via_github_app]. The guard then refuses every other
 * account but cannot tell an agent from the owner, and the rule binds agents procedurally (CLAUDE.md hard rule 3).
 */
import { readFileSync } from 'node:fs';
import type { Log } from './proc.ts';

export const LABEL = 'visual-approved';

interface LabelEvent {
  readonly event: string;
  readonly created_at: string;
  readonly id: number;
  readonly actor: { readonly login: string } | null;
  readonly label?: { readonly name: string };
  readonly performed_via_github_app?: { readonly slug?: string } | null;
}

export function flatten(json: unknown): LabelEvent[] {
  if (!Array.isArray(json)) throw new Error('issue events must be a JSON array');
  const events: unknown[] = json.flatMap((page: unknown) =>
    Array.isArray(page) ? (page as unknown[]) : [page],
  );
  for (const e of events) {
    if (typeof e !== 'object' || e === null || !('event' in e) || !('created_at' in e)) {
      throw new Error('issue events: an entry lacks event or created_at');
    }
  }
  return events as LabelEvent[];
}

const byTime = (a: string, b: string) => Date.parse(a) - Date.parse(b);

/** The earliest created_at of `{ check_suites }` pages (slurped or one page); undefined when there is none. */
export function firstSuite(json: unknown): string | undefined {
  const pages: unknown[] = Array.isArray(json) ? json : [json];
  const times = pages.flatMap((page): unknown[] => {
    const suites: unknown =
      typeof page === 'object' && page !== null ? Reflect.get(page, 'check_suites') : [];
    if (!Array.isArray(suites)) return [];
    return (suites as unknown[]).map((s): unknown =>
      typeof s === 'object' && s !== null ? Reflect.get(s, 'created_at') : '',
    );
  });
  return times
    .filter((t): t is string => typeof t === 'string' && !Number.isNaN(Date.parse(t)))
    .sort(byTime)[0];
}

const last = (events: readonly LabelEvent[], keep: (e: LabelEvent) => boolean) =>
  events
    .filter(keep)
    .sort((a, b) => byTime(a.created_at, b.created_at) || a.id - b.id)
    .at(-1);

export function verdict(
  events: readonly LabelEvent[],
  owner: string,
  headSeen: string | undefined,
): { ok: boolean; reason: string } {
  const latest = last(events, (e) => e.event === 'labeled' && e.label?.name === LABEL);
  if (latest === undefined) return { ok: false, reason: `no labeled event for ${LABEL}` };
  const at = Date.parse(latest.created_at);
  if (headSeen === undefined || Number.isNaN(at)) {
    return {
      ok: false,
      reason: 'no check suite or label time: cannot tell the label came after the head commit',
    };
  }
  if (at <= Date.parse(headSeen)) {
    return {
      ok: false,
      reason: `${LABEL} was applied at ${latest.created_at}, before the head arrived at ${headSeen}`,
    };
  }
  const pushed = last(events, (e) => e.event === 'head_ref_force_pushed');
  if (pushed !== undefined && Date.parse(pushed.created_at) >= at) {
    return {
      ok: false,
      reason: `commits were force-pushed at ${pushed.created_at}, after ${LABEL} was applied`,
    };
  }
  const who = latest.actor?.login ?? '(unknown)';
  if (who.toLowerCase() !== owner.toLowerCase()) {
    return { ok: false, reason: `${LABEL} was applied by ${who}; only ${owner} may apply it` };
  }
  const app = latest.performed_via_github_app;
  if (app !== undefined && app !== null) {
    return {
      ok: false,
      reason: `${LABEL} was applied through the GitHub App ${app.slug ?? '?'}; ${owner} applies it directly`,
    };
  }
  return {
    ok: true,
    reason: `${LABEL} applied by ${owner} at ${latest.created_at}, after the head at ${headSeen}`,
  };
}

export function main(argv: readonly string[], log: Log = console.log): number {
  const [file, owner, suites] = argv;
  if (file === undefined || owner === undefined || suites === undefined) {
    log('usage: node tools/ci/label-guard.ts <events.json> <owner-login> <check-suites.json>');
    return 2;
  }
  const read = (path: string): unknown => JSON.parse(readFileSync(path, 'utf8'));
  const { ok, reason } = verdict(flatten(read(file)), owner, firstSuite(read(suites)));
  log(`label-guard: ${reason}`);
  return ok ? 0 : 1;
}

if (import.meta.main) process.exitCode = main(process.argv.slice(2));
