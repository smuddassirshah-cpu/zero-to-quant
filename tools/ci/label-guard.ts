/*
 * Who applied visual-approved (docs/PLAN.md 7.6). Usage: node tools/ci/label-guard.ts <events.json> <owner-login>
 * Reads a pull request's issue events (`gh api --paginate --slurp`, so an array of pages, or a plain array) and
 * passes only if the latest `labeled` event for the label was by the owner, applied directly rather than
 * through a GitHub App (performed_via_github_app set): an agent acting through an installed App is refused
 * even when the App acts as the owner's account.
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

export function verdict(events: readonly LabelEvent[], owner: string): { ok: boolean; reason: string } {
  const latest = events
    .filter((e) => e.event === 'labeled' && e.label?.name === LABEL)
    .sort((a, b) => a.created_at.localeCompare(b.created_at) || a.id - b.id)
    .at(-1);
  if (latest === undefined) return { ok: false, reason: `no labeled event for ${LABEL}` };
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
  return { ok: true, reason: `${LABEL} applied by ${owner} at ${latest.created_at}` };
}

export function main(argv: readonly string[], log: Log = console.log): number {
  const [file, owner] = argv;
  if (file === undefined || owner === undefined) {
    log('usage: node tools/ci/label-guard.ts <events.json> <owner-login>');
    return 2;
  }
  const { ok, reason } = verdict(flatten(JSON.parse(readFileSync(file, 'utf8'))), owner);
  log(`label-guard: ${reason}`);
  return ok ? 0 : 1;
}

if (import.meta.main) process.exitCode = main(process.argv.slice(2));
