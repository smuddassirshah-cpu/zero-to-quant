/*
 * The progress log (docs/ASSESSMENT.md 13.2) and the store both targets implement (13.5), which `Platform`
 * names (docs/ARCHITECTURE.md 5.9); built on by stage 9a's append queue and fold, and stage 69's stores.
 * Decision notes:
 * - `Envelope` and `ProgressStore` are 13.2's and 13.5's listings, exported; test/drift.test.ts compares them.
 * - 13.2 types no payload, and its table lists each kind's "main fields". A field the table writes as an
 *   identifier (in backticks) is typed: with the values it lists in brackets, or the shape it gives
 *   (`marks` as `[earned, max]`, `have` from 14.1). The name alone fixes a few more [inferred]: `ms` is
 *   milliseconds and `rev` a revision everywhere in the papers; `try`, `hints`, `xp` and `mp` are counts;
 *   `skills` are skill ids, the first a card's primary skill (5.3); `mc` is a misconception id. The rest are
 *   `Json` until stage 9a defines them. Fields given only in words (lesson id, attempt id, seeds) are left
 *   out: no paper names them. Optional only where a paper says the field is conditional: `mc`, `snap` (0.3's
 *   rule) and `perfect` (ARCHITECTURE.md 5.7.2 records it on `complete`).
 * - Nothing names the field that carries the kind, and `time` and `import` have their own `kind`, so it is
 *   `k`, as 5.7's `Phase` and `MotionStep` discriminate [our choice]. An event is flat: envelope, `k` and
 *   payload side by side [our choice].
 * - `Snapshot`, `DraftHandle` and `ImportReport` have no TypeScript definition in any paper (13.3, 13.4 and
 *   14.2 describe them in prose), so they are opaque: no value but one the store returns is of the type, and
 *   stages 9a, 69 and 70 define them.
 * - No DOM type: the data worker and Node tools read events. `Blob` is a Node global too [measured: @types/node
 *   22.20.5, test/node-libs.test.ts].
 */
import type { ContentId, Json } from './base.ts';

declare const opaque: unique symbol;
type Opaque<Name extends string> = Readonly<{ [opaque]: Name }>;

/** ASSESSMENT.md 13.2. */
export interface Envelope {
  id: string; // `${t.toString(36)}-${dev}-${seq.toString(36)}`: time-sortable, unique per device
  t: number; // device clock, epoch milliseconds
  tz: number; // minutes east of UTC at the event (study days, section 12.1)
  dev: string; // 8 random base-36 characters, generated at first run on this install
  seq: number; // per-device counter, strictly increasing
  rel: string; // content release (CONTENT-FORMAT.md 4.5)
  app: string; // app release
  v: 1; // event format version
}

/** 13.2's kinds, in its table's order. */
// prettier-ignore
export type EventKind = 'att' | 'lsn' | 'hw' | 'exam' | 'mark' | 'ment' | 'weekly' | 'out' | 'proj' | 'paste'
                      | 'time' | 'prior' | 'set' | 'plan' | 'import';

// prettier-ignore
export type AttemptContext = 'lesson' | 'quiz' | 'practice' | 'review' | 'redo' | 'homework' | 'exam' | 'check'
                           | 'placement' | 'weekly' | 'timed';

/** An event without its envelope (ARCHITECTURE.md 5.7.1): what the player records; the append queue adds the envelope. */
// prettier-ignore
export type EventDraft =
  | { k: 'att'; ctx: AttemptContext; ref: Json; try: number; ans: Json; verdict: Json; marks: [number, number]; ms: number;
      hints: number; skills: ContentId[]; d: Json; mc?: ContentId; snap?: Json; xp: number; mp: number }
  | { k: 'lsn'; rev: number; op: 'start' | 'screen' | 'complete'; perfect?: boolean }
  | { k: 'hw'; op: 'issue' | 'submit'; rev: number }
  | { k: 'exam'; op: 'start' | 'pause' | 'resume' | 'hidden' | 'section' | 'leave' | 'submit' }
  | { k: 'mark' }
  | { k: 'ment' }
  | { k: 'weekly'; op: 'assign' | 'rate' }
  | { k: 'out'; op: 'create' | 'edit' | 'delete' }
  | { k: 'proj'; op: 'create' | 'update' }
  | { k: 'paste' }
  | { k: 'time'; ctx: Json; ref: Json; ms: number; kind: 'solving' | 'reading' }
  | { k: 'prior' }
  | { k: 'set' }
  | { k: 'plan'; op: 'accept' | 'adjust' | 'override' }
  | { k: 'import'; have: Record<string, number> };

/** One logged event: the envelope with its kind and payload. */
export type Ev = Envelope & EventDraft;

export type Snapshot = Opaque<'Snapshot'>; // derived state with its basis (13.3)
export type DraftHandle = Opaque<'DraftHandle'>; // a leased draft of a homework set, a paper or long-form text (13.4, 13.7)
export type ImportReport = Opaque<'ImportReport'>; // what an import adds (14.2 step 3)

/** ASSESSMENT.md 13.5: both targets use one interface. */
export interface ProgressStore {
  append(events: Ev[]): Promise<void>; // durable locally on resolve; queued for the remote where one exists
  load(): Promise<{ snapshot?: Snapshot; events: Ev[] }>; // the newest snapshot and the events after its basis
  subscribe(onEvents: (evs: Ev[]) => void): () => void; // other devices' events (Artifact); a no-op on the web
  saveSnapshot(s: Snapshot): Promise<void>;
  draft(id: string): Promise<DraftHandle>; // lease-held on the Artifact
  exportAll(): Promise<Blob>; // full backup (section 14.1)
  exportSince(peer: 'artifact' | 'web'): Promise<Blob>; // sync file: events that peer has not acknowledged
  importFile(text: string): Promise<ImportReport>; // validated in the data worker (ARCHITECTURE.md decision 10)
}
