// Compile-time tests of docs/ARCHITECTURE.md 5.9 and 5.11 with the papers' types they name: ASSESSMENT.md 13.2 and
// 13.5 (events.ts), AI-TUTOR.md 4.1, 6.1 and 6.4. test/drift.test.ts pins the transcription; these pin meaning.
import type { Json } from '@zq/contracts/base';
import type {
  DraftHandle,
  Ev,
  EventDraft,
  EventKind,
  ImportReport,
  ProgressStore,
} from '@zq/contracts/events';
import type { Snapshot } from '@zq/contracts/events';
import type * as p from '@zq/contracts/platform';
import type { TexService } from '@zq/contracts/render';
import { describe, expectTypeOf, test } from 'vitest';
import type { Words } from './types.ts';

type Of<K extends EventKind> = Extract<EventDraft, { k: K }>;

describe('platform adapters (5.9)', () => {
  test('Platform carries every adapter; only the tutor and C++ may be absent', () => {
    expectTypeOf<keyof p.Platform>().toEqualTypeOf<
      | Words<'target build content progress drafts cache kv tutor python sql cpp'>
      | Words<'feedback clock random files identity handoff lifecycle'>
    >();
    expectTypeOf<p.Platform['progress']>().toEqualTypeOf<ProgressStore>();
    expectTypeOf<p.Platform['tutor']>().toEqualTypeOf<p.TutorBackend | null>();
    expectTypeOf<p.Platform['cpp']>().toEqualTypeOf<p.CppRuntime | null>();
    expectTypeOf<p.Platform['python']>().toEqualTypeOf<p.PythonRuntime>(); // the Artifact's is the handoff stub
  });

  test("content-schema's outputs are opaque: no value but one the platform returns has the type", () => {
    expectTypeOf<Record<string, never>>().not.toExtend<p.CourseBundle>();
    expectTypeOf<p.CourseBundle>().not.toExtend<p.ItemBody>();
    expectTypeOf<p.Glossary>().not.toExtend<p.NotebookCards>();
    expectTypeOf<p.ContentSource['course']>().returns.resolves.toEqualTypeOf<p.CourseBundle>();
  });

  test('runtimes: Python packages are Drill.needs, availability comes first, SQL caps its rows', () => {
    expectTypeOf<p.PyPackage>().toEqualTypeOf<
      Words<'numpy pandas scipy statsmodels sklearn matplotlib pytest hypothesis'>
    >();
    expectTypeOf<ReturnType<p.PythonRuntime['available']>>().toEqualTypeOf<
      { ok: true; downloadBytes: number } | { ok: false; reason: 'not-in-this-build' }
    >();
    expectTypeOf<p.SqlRuntime['query']>()
      .parameter(1)
      .toEqualTypeOf<{ signal: AbortSignal; maxRows: 1000 }>();
    expectTypeOf<p.RunResult['status']>().toEqualTypeOf<Words<'pass fail error timeout cancelled'>>();
  });

  test('the tutor token is kept only as a named secret; other values read back as Json', () => {
    expectTypeOf<p.KeyValue['get']>().toEqualTypeOf<(key: string) => Json | undefined>();
    expectTypeOf<p.KeyValue['secret']>().parameter(0).toEqualTypeOf<'tutor-token'>();
    expectTypeOf<p.KeyValue['setSecret']>().parameters.toEqualTypeOf<
      [name: 'tutor-token', value: string | null]
    >();
  });

  test("the tutor's backend sends one TutorRequest under a CallPlan; errors carry 6.4's codes", () => {
    expectTypeOf<p.TutorBackend['send']>().parameters.toEqualTypeOf<
      [req: p.TutorRequest, plan: p.CallPlan, io: p.CallIO]
    >();
    expectTypeOf<p.TutorMode>().toEqualTypeOf<
      Words<'hint why explain chat mark code_review recap diagnose practice'>
    >();
    expectTypeOf<p.TutorErrorCode>().toEqualTypeOf<
      | Words<'cancelled invalid_request transform_error queue_overflow prompt_too_large not_granted'>
      | Words<'sampling_disabled not_declared capability_disabled capability_removed tools_unavailable'>
      | Words<'images_unavailable image_rejected rate_limited session_expired refused empty_completion'>
      | Words<'invalid_json upstream_error offline auth_failed budget_exhausted version_mismatch locked withheld'>
    >();
    expectTypeOf<p.TutorError['code']>().toEqualTypeOf<p.TutorErrorCode>();
    expectTypeOf<NonNullable<p.TutorRequest['answer']>['status']>().toEqualTypeOf<'sealed' | 'open'>();
  });

  test('TexService renders authored maths by default, untrusted text on request (5.11, B33)', () => {
    expectTypeOf<keyof TexService>().toEqualTypeOf<Words<'ready load html'>>();
    expectTypeOf<TexService['html']>().parameter(2).toEqualTypeOf<'authored' | 'untrusted' | undefined>();
  });
});

describe('the progress log (ASSESSMENT.md 13.2, 13.5)', () => {
  test("the table's kinds, one draft per kind", () => {
    expectTypeOf<EventKind>().toEqualTypeOf<
      Words<'att lsn hw exam mark ment weekly out proj paste time prior set plan import'>
    >();
    expectTypeOf<EventDraft['k']>().toEqualTypeOf<EventKind>();
    expectTypeOf<Of<'att'>['ctx']>().toEqualTypeOf<
      Words<'lesson quiz practice review redo homework exam check placement weekly timed'>
    >();
    expectTypeOf<Of<'att'>['marks']>().toEqualTypeOf<[number, number]>();
    expectTypeOf<Of<'exam'>['op']>().toEqualTypeOf<Words<'start pause resume hidden section leave submit'>>();
    expectTypeOf<Of<'import'>['have']>().toEqualTypeOf<Record<string, number>>();
    expectTypeOf<{ k: 'lsn'; rev: number; op: 'finish' }>().not.toExtend<EventDraft>();
  });

  test('an event is flat: the envelope beside its kind and payload; drafts are JSON, events are not', () => {
    const envelope = {
      id: 'm0-abcdefgh-1',
      t: 0,
      tz: 60,
      dev: 'abcdefgh',
      seq: 1,
      rel: 'r1',
      app: 'a1',
      v: 1,
    } as const;
    expectTypeOf({ ...envelope, k: 'lsn', rev: 3, op: 'complete', perfect: true } as const).toExtend<Ev>();
    expectTypeOf({ ...envelope, v: 2, k: 'mark' } as const).not.toExtend<Ev>();
    expectTypeOf<EventDraft>().toExtend<Json>();
    expectTypeOf<Ev>().not.toExtend<Json>(); // 13.2's Envelope is an interface (see the report)
  });

  test('the store: snapshots, drafts and import reports are opaque until their stages define them', () => {
    expectTypeOf<Record<string, never>>().not.toExtend<Snapshot>();
    expectTypeOf<Snapshot>().not.toExtend<DraftHandle>();
    expectTypeOf<DraftHandle>().not.toExtend<ImportReport>();
    expectTypeOf<ProgressStore['load']>().returns.resolves.toEqualTypeOf<{
      snapshot?: Snapshot;
      events: Ev[];
    }>();
    expectTypeOf<ProgressStore['exportAll']>().returns.resolves.toEqualTypeOf<Blob>();
  });
});
