/*
 * The platform adapters (docs/ARCHITECTURE.md 5.9): the only target-specific code. Engine, widgets, screens
 * and the tutor see these interfaces; src/platform implements them per target (stage 4), and
 * src/platform/types.ts re-exports them.
 * Decision notes:
 * - `ProgressStore` is in events.ts with the events it stores (ASSESSMENT.md 13.5). `TutorBackend` and the
 *   types it names are AI-TUTOR.md 6.1, 4.1 and 6.4, transcribed below, because `Platform.tutor` names it and
 *   this package may import no other (4.5); src/tutor/context/schema.ts keeps the validators (AI-TUTOR.md 11.1).
 *   `TutorErrorCode` is 6.4's table's code column, in its order: no paper writes the union.
 * - `CourseBundle`, `ItemBody`, `Glossary` and `NotebookCards` are @zq/content-schema's compiled outputs
 *   (5.9's note), which this package may not import (4.5), so they are opaque here until their home is
 *   decided: no value but one the platform returns is of the type.
 * - No DOM type, so @zq/compiler, which writes the `Manifest`, and the workers can read this module without the
 *   DOM lib: `Blob`, `File` and `AbortSignal` are Node globals too [measured: @types/node 22.20.5,
 *   test/node-libs.test.ts].
 * - `KeyValue.get` returns `Json`: 5.9's `get<T extends Json>(key): T | undefined` is an unchecked cast, which
 *   typescript-eslint's no-unnecessary-type-parameters refuses and no file may switch off (10.4), so the
 *   caller narrows what it reads [measured: ESLint 10.12.0].
 * - The listings keep their own layout (`prettier-ignore`); test/drift.test.ts compares every declaration.
 */
import type { ReadonlySignal, Signal } from '@preact/signals-core';
import type { ContentId, Json } from './base.ts';
import type { ProgressStore } from './events.ts';
import type { ClusterId } from './widget.ts';

declare const opaque: unique symbol;
type Opaque<Name extends string> = Readonly<{ [opaque]: Name }>;

export type CourseBundle = Opaque<'CourseBundle'>;
export type ItemBody = Opaque<'ItemBody'>;
export type Glossary = Opaque<'Glossary'>;
export type NotebookCards = Opaque<'NotebookCards'>;

export interface Platform {
  readonly target: 'artifact' | 'web' | 'test';
  readonly build: { app: string; content: string; commit: string };
  readonly content: ContentSource;
  readonly progress: ProgressStore; // ASSESSMENT.md 13.5, unchanged
  readonly drafts: DraftStore; // per-device lesson drafts; homework and papers use progress.draft (leased)
  readonly cache: BlobCache; // disposable: bundles, generator modules
  readonly kv: KeyValue;
  readonly tutor: TutorBackend | null; // AI-TUTOR.md 6.1; null when this view has no tutor
  readonly python: PythonRuntime; // web: Pyodide; Artifact: the handoff stub (revision 2)
  readonly sql: SqlRuntime; // web: SQLite; Artifact: the handoff stub
  readonly cpp: CppRuntime | null; // web only (programming decision 9); null in the Artifact, where C++ drills hand off
  readonly feedback: Feedback;
  readonly clock: Clock;
  readonly random: RandomSource;
  readonly files: FileSaver;
  readonly identity: Identity;
  readonly handoff: Handoff;
  readonly lifecycle: Lifecycle;
}

export interface ContentSource {
  manifest(): Manifest; // synchronous after boot, which fetches the file the page's <meta name="zq-manifest"> names (decision 30)
  course(id: ContentId): Promise<CourseBundle>; // by hash: cache, else fetch; validated once per hash in the data worker
  generators(id: ContentId): Promise<GeneratorModule>; // course id in; dynamic import of the topic's gen/<top>.<hash>.mjs (one module per topic)
  searchIndex(stage: 0 | 1 | 2 | 3): Promise<Json>;
  glossary(): Promise<Glossary>;
  notebook(): Promise<NotebookCards>;
  assetUrl(name: string): string;
  prefetch(id: ContentId): void; // idle priority
  keepOffline(id: ContentId, on: boolean): Promise<void>; // web: service worker cache; Artifact: resolves, no effect
  onChange(fn: () => void): () => void; // development hot reload only
}
// prettier-ignore
export interface Manifest {
  release: string; format: 1; app: string;
  courses: Record<ContentId, {
    bundle: string; gen?: string; bytes: number;
    clusters: ClusterId[];                                 // widget chunks the course needs
    python: PyPackage[];                                   // union of its drills' `needs`
    sql: boolean;
  }>;
  search: string[]; glossary: string; notebook: string; assets: Record<string, string>;
}
// prettier-ignore
export interface GeneratorModule {
  readonly v: Record<ContentId, number>;
  make(gen: ContentId, seed: number, level: 1 | 2 | 3 | 4 | 5, pool: 'practice' | 'exam'): ItemBody;   // content-format 5.4
  /** Bertie's practice picks (content-format 5.4, ai-tutor 2.11): a seeded point from the level's admissible, non-reserved index matching
   *  the partial assignment over the generator's `tutorParams`; null when nothing matches (the pick is dropped and counted). */
  makeWhere(gen: ContentId, partial: Record<string, Json>, seed: number, level: 1 | 2 | 3 | 4 | 5): ItemBody | null;
}

export interface BlobCache {
  // IndexedDB; least recently used beyond 300 MB or 60% of quota
  get(key: string): Promise<ArrayBuffer | null>;
  put(key: string, data: ArrayBuffer, kind: 'course' | 'gen' | 'search'): Promise<void>;
  evict(kind?: 'course' | 'gen' | 'search'): Promise<void>;
  usage(): Promise<{ bytes: number; quota: number | null }>;
}
// prettier-ignore
export interface DraftStore {                             // keys: 'lesson:<lsn id>@<rev>:<screen id>:<widget id>', so a new rev never meets an old draft
  get(key: string): Promise<Json | null>; put(key: string, value: Json): Promise<void>; drop(prefix: string): Promise<void>;
  mirror(key: string, value: Json): void;                 // Artifact: a synchronous sessionStorage copy at every commit, before the debounced put; get returns the newer copy, drop clears both (section 6.2.6; DECISIONS.md B22). A no-op on the web
}
export interface KeyValue {
  // small device-local values; synchronous reads from a mirror loaded at boot
  get(key: string): Json | undefined; // see the decision notes
  set(key: string, value: Json): void;
  secret(name: 'tutor-token'): Promise<string | null>; // IndexedDB only, never localStorage
  setSecret(name: 'tutor-token', value: string | null): Promise<void>;
}

export type PyPackage =
  'numpy' | 'pandas' | 'scipy' | 'statsmodels' | 'sklearn' | 'matplotlib' | 'pytest' | 'hypothesis'; // the content schema's Drill.needs enum, spelt identically; 'cvxpy' and 'highspy' join at the 2.0b wave (docs/PLAN.md 5.7)
// prettier-ignore
export interface PythonRuntime {
  readonly status: ReadonlySignal<
    | { k: 'cold' } | { k: 'loading'; step: string; done: number; total: number }
    | { k: 'ready'; packages: PyPackage[] } | { k: 'failed'; code: 'network' | 'integrity' | 'memory' | 'crashed' | 'unsupported' }>;
  available(packages: readonly PyPackage[]): { ok: true; downloadBytes: number } | { ok: false; reason: 'not-in-this-build' };   // downloadBytes: what is not yet cached; 0 means warm() needs no network
  warm(packages: readonly PyPackage[]): Promise<void>;     // idempotent; starts the worker and loads packages
  run(req: RunRequest, io: { signal: AbortSignal; onEvent(e: RunEvent): void }): Promise<RunResult>;
  terminate(): void;
}
export interface RunRequest {
  drill: ContentId;
  rev: number;
  mode: 'drill' | 'script' | 'pytest' | 'answer' | 'checker'; // content-format Drill.mode (sql and C++ use their own runtimes)
  files: Record<string, string>; // the learner's files
  support: Record<string, string>; // tests.py, zqtest.py, data files: from the course bundle
  entry?: string;
  tests: 'examples' | 'all';
  examples: string[];
  timeLimitMs: number; // per test (content-format: 5,000 by default)
  needs: readonly PyPackage[];
}
// prettier-ignore
export type RunEvent =
  | { k: 'stdout' | 'stderr'; text: string }               // at most 4,000 characters per stream (programming 2.4)
  | { k: 'test'; name: string; status: 'pass' | 'fail' | 'error' | 'timeout'; ms: number; hidden: boolean;
      input?: string; expected?: string; actual?: string; error?: { type: string; message: string; line?: number } };
// prettier-ignore
export interface RunResult { status: 'pass' | 'fail' | 'error' | 'timeout' | 'cancelled'; passed: number; total: number; firstFailure?: string; ms: number }
// prettier-ignore
export interface CppRuntime {                              // web only; present only if the 1.9 cpp-runner spike passes (programming 8); no Compiler Explorer route (docs/PLAN.md)
  readonly backend: 'clang-wasm';
  run(req: RunRequest & { language: 'cpp'; flags: string[] }, io: { signal: AbortSignal; onEvent(e: RunEvent): void }): Promise<RunResult>;
}
// prettier-ignore
export interface SqlRuntime {
  load(db: { name: string; sql: string }): Promise<void>;
  query(sql: string, o: { signal: AbortSignal; maxRows: 1000 }): Promise<{ columns: string[]; rows: Json[][]; plan?: string[] } | { error: string }>;
}

export type SoundName = 'correct' | 'not-yet' | 'complete' | 'streak' | 'tap' | 'snap';
export type HapticName = 'correct' | 'not-yet' | 'snap' | 'complete';
export interface Feedback {
  readonly soundOn: Signal<boolean>;
  readonly hapticsOn: Signal<boolean>;
  sound(name: SoundName): void; // Web Audio synthesis; peak about 12 dB below full scale
  haptic(name: HapticName): void; // navigator.vibrate where it exists (Android Chrome); a no-op elsewhere
  unlock(): void; // resumes the AudioContext on the first gesture
  suppress(on: boolean): void; // exams
}
// prettier-ignore
export interface Clock { now(): number; perf(): number; tz(): number } // tz: minutes east of UTC
// prettier-ignore
export interface RandomSource { deviceId(): string; seed(): number; nonce(bytes: number): string } // crypto.getRandomValues
// prettier-ignore
export interface FileSaver {
  save(name: string, mime: string, data: Blob | string): Promise<'saved' | 'unsupported' | 'cancelled' | 'failed'>;
  pick(accept: readonly string[]): Promise<File | null> | null;   // null: no file picker in this view, offer paste instead
}
// prettier-ignore
export interface Identity { viewerId(): Promise<string | null>; canWrite(): Promise<boolean | null> }
export interface Handoff {
  toWeb(route: string, payload?: Json): { href: string | null; copyText: string }; // href null where links cannot leave the Artifact
  receive(): Json | null; // web: the validated ?h= payload of the current route
}
export interface Lifecycle {
  readonly visible: ReadonlySignal<boolean>;
  readonly online: ReadonlySignal<boolean>;
  readonly writer: ReadonlySignal<'this-tab' | 'other-tab'>;
  takeWriter(): Promise<void>;
  persist(): Promise<boolean>; // navigator.storage.persist on the web
  reload(): void;
}

// The tutor's backend (AI-TUTOR.md 6.1), the request it sends (4.1) and its error codes (6.4).
// prettier-ignore
export type TutorErrorCode =
  | 'cancelled' | 'invalid_request' | 'transform_error' | 'queue_overflow' | 'prompt_too_large' | 'not_granted'
  | 'sampling_disabled' | 'not_declared' | 'capability_disabled' | 'capability_removed' | 'tools_unavailable'
  | 'images_unavailable' | 'image_rejected' | 'rate_limited' | 'session_expired' | 'refused' | 'empty_completion'
  | 'invalid_json' | 'upstream_error' | 'offline' | 'auth_failed' | 'budget_exhausted' | 'version_mismatch'
  | 'locked' | 'withheld';

export type Tier = 'quick' | 'default' | 'complex';
export type Effort = 'low' | 'medium' | 'high';
export type OutputKind = 'prose' | 'json' | 'jsonl';

export interface CallPlan {
  // from the mode table in section 6.5; never chosen by the model
  mode: TutorMode;
  tier: Tier; // Artifact
  effort: Effort; // web: top-level medium plus an effort message when not medium (decision 23)
  maxTokens: number; // web
  output: OutputKind;
  jsonSchema?: object; // output 'json'
  tools: ('getScreenState' | 'compute')[];
  cache: 'default' | 'off' | 'day'; // Artifact answer cache
}

export interface CallIO {
  onText(u: { text: string; delta: string }): void; // whole text so far and the new part, as sample
  onProgress(label: string): void; // "Reading the page", from inside tool execute
  signal: AbortSignal; // one controller per call
  tools: Record<string, (input: unknown, ctx: { signal: AbortSignal }) => Promise<unknown>>;
}

export interface RawResult {
  text: string;
  truncated: boolean;
  served: string; // 'quick' | 'default' | 'complex' | 'claude-opus-5-5' | a fallback model id
  usage?: { input: number; output: number; cacheRead: number; cacheWrite: number; usd: number };
}

// prettier-ignore
export interface TutorBackend {
  readonly kind: 'artifact' | 'web';
  probe(): Promise<{ available: boolean; reason?: TutorErrorCode; tools: boolean; images: boolean; maxPromptBytes: number }>;
  send(req: TutorRequest, plan: CallPlan, io: CallIO): Promise<RawResult>;   // rejects with TutorError, never throws synchronously
}

// prettier-ignore
export interface TutorError { code: TutorErrorCode; message: string; text?: string } // text: partial answer the page may keep

export type TutorMode =
  'hint' | 'why' | 'explain' | 'chat' | 'mark' | 'code_review' | 'recap' | 'diagnose' | 'practice';
export type Depth = 'new' | 'standard' | 'formal' | 'interview';
export type Rep = 'picture' | 'count' | 'algebra' | 'analogy' | 'simulation' | 'code';

export interface TutorRequest {
  v: 1;
  mode: TutorMode;
  depth: Depth; // from the chip or Settings; 'standard' by default
  lesson: LessonCtx; // stable for the whole lesson
  screen?: ScreenCtx; // absent for lesson-level recap and practice
  learner?: LearnerCtx; // learner-originated fields are escaped by the renderer
  hints?: HintCtx;
  misconceptions?: MisconceptionCtx;
  answer?: AnswerCtx; // absent when config tutor.answerKey = 'never' and status is sealed
  why?: { text: string; rep: Rep; useReps: Rep[]; avoidReps: Rep[]; previous: string[] };
  chat?: ChatCtx;
  marking?: MarkingCtx;
  code?: CodeCtx;
  session?: SessionCtx;
  practice?: PracticeCtx;
  avoid?: string[]; // Bertie's earlier lines, for "Say it differently"
}

export interface ChatCtx {
  turns: ChatTurn[]; // earlier turns of this thread, oldest first, at most 11
  message: string; // the new learner message; learner-originated
  summary?: string; // page-made summary when a fresh thread replaced a full one
}

export interface ChatTurn {
  role: 'learner' | 'bertie';
  text: string; // learner text, or Bertie's reply with the act line removed
  call?: string; // web, learner turns only: the call block the proxy rendered for that turn, verbatim
  sig?: string; // web: the proxy's HMAC over promptVersion, lesson id and call (decision 24)
}

export interface LessonCtx {
  id: string; // content id: 'lsn.cond.shrinking-sample-space'
  title: string;
  path: string; // display path, computed from position: '1.5 Probability > Conditional probability > Level 1 > Lesson 3'
  objectives: string[]; // from introduces and insight; at most 4
  covered: string[]; // earlier lesson titles in this course and the skills in uses and requires, at most 20
  notation: string; // the topic's notation card as text, at most 800 characters
  glossary: { term: string; def: string }[]; // terms introduced so far in the course, at most 20
  embargo: string[]; // glossary terms introduced later in the course, at most 60 (decision 28)
  screens: { n: number; title: string; keyIdea?: string }[]; // outline: title from tutor.focus; keyIdea from reason, only for finished screens
  references: { id: string; cite: string }[]; // curated reading for this lesson, at most 6
  cards: { id: string; title: string }[]; // Notebook cards available, at most 20
}

// prettier-ignore
export interface ScreenCtx {
  id: string; n: number; of: number;
  type: 'title' | 'explore' | 'problem' | 'ladder' | 'demonstrate' | 'trap' | 'generalise' | 'derive' | 'code' | 'summary';
  prose: string;                        // authored prompt prose, at most 1,500 characters
  question?: string;
  widgets: { id: string; type: string; label: string; brief: string; full?: string }[];   // describe(); full only where the recipe says
  focus: string;                        // authored tutor.focus: what this screen is for
  targets: { id: string; label: string }[];    // from targets(), at most 40; bare ids on one-widget screens, 'grid/cell:5,5' otherwise
  tryable: { control: string; label: string; range?: [number, number]; options?: string[] }[];
  notes?: string;                       // authored tutor.notes: where learners stall and what to ask
  reps?: Rep[];                         // authored tutor.reps
  avoid?: string[];                     // authored tutor.avoid: phrases Bertie must not use on this screen
}

export interface LearnerCtx {
  answer?: string; // current answer as displayed: '12', 'Option C: 1/6', 'cells (2,6) (3,5) (4,4)'
  checked: boolean; // whether answer has been checked in its current form
  attempts: { answer: string; verdict: 'not-yet' | 'correct'; misconception?: string; line?: string }[];
  log: string[]; // last 10 action summaries from the engine
  firstCheckDone: boolean; // in this lesson
  timeBucket: 'under-1-min' | '1-to-3-min' | 'over-3-min';
}

export interface HintCtx {
  seen: { rung: 1 | 2 | 3; label: 'Nudge' | 'Point' | 'Step'; text: string }[];
  next?: { rung: 1 | 2 | 3; label: 'Nudge' | 'Point' | 'Step'; text: string };
  canShowSolution: boolean; // two not-yet attempts on this screen
  solutionShown: boolean;
}

export interface MisconceptionCtx {
  screen: { id: string; belief: string }[]; // the screen's register: every mc named in its diagnose list, with the library's belief
  topic?: { id: string; belief: string }[]; // diagnose only: at most 15 library entries, filtered to the screen's skills
}

export interface AnswerCtx {
  status: 'sealed' | 'open';
  key: string; // the compiler's summary of the check: 'numeric, 11 exactly, whole number'
  solution?: string; // authored solution.line and solution.steps
  secrets?: string; // widget secret(): true parameters, planted leaks, hidden truths
  accepted?: string; // the learner-facing accepted-answer rule; only when status is 'open'
}

export interface MarkingCtx {
  item: { id: string; prompt: string; genre: 'proof' | 'derivation' | 'written' | 'results-note' };
  rubric: { id: string; text: string; marks: number; lines: string[] }[]; // 4 to 10 points totalling 10; lines: model-answer line ids
  model: string; // authored model answer, its lines labelled with their ids
  working: string; // learner-originated
}

// prettier-ignore
export interface CodeCtx {
  drill: { id: string; prompt: string; signature: string; examples: string };
  packages: string[];                   // the PyPackage values loaded for this attempt (Pyodide 314.0.7, web app only since revision 2)
  files: { name: string; numbered: string }[];    // learner-originated; '12| total += x'
  run?: { status: 'pass' | 'fail' | 'error' | 'timeout'; passed: number; total: number;
          firstFailure?: { name: string; input: string; expected: string; actual: string; hidden: boolean };
          error?: { type: string; message: string; line?: number; excerpt?: string } };
  submissions: number; failedSubmissions: number;
  solved: boolean; solutionUnlocked: boolean;
  reference?: string;                   // only when solutionUnlocked or solved
  reviewDepth?: 1 | 2 | 3 | 4 | 5;
}

// prettier-ignore
export interface SessionCtx {
  kind: 'lesson' | 'homework' | 'exam';
  screens: { n: number; title: string; result: 'first-try' | 'retry' | 'revealed' | 'explore'; hints: number; misconception?: string }[];
  quiz?: { score: number; of: number };
  minutes: number;                      // rounded to 5
  redoAdded: number;
  next?: string;
}

export interface PracticeCtx {
  count: number; // 3 to 5
  skills: { id: string; name: string; mastery: number; due: boolean }[];
  recentMisconceptions: string[];
  generators: { id: string; skill: string; desc: string; tutorParams: object; levels: number[] }[]; // at most 12; tutorParams: the dimensions Bertie may fix, with bounds
  recent: { generator: string; params: object }[]; // at most 10
}
