/*
 * Shared primitives (docs/ARCHITECTURE.md 5.1), transcribed.
 * Decision notes:
 * - `hash32` (5.1) is a function, so it lives in @zq/mathcore with the Philox generator; this module carries
 *   only the `Rng` and `SeedSource` contracts that generator implements.
 * - No DOM-only type, so @zq/mathcore, which imports `Rng` and `SeedSource` from here, compiles without the
 *   DOM lib (docs/DECISIONS.md B43; test/node-libs.test.ts checks it). AbortSignal, EventTarget and Event
 *   are Node globals too, but AddEventListenerOptions is not [measured: @types/node 22.20.5 declares it
 *   module-local], so `listen` spells out its members, which are lib.dom's exactly (capture, once, passive,
 *   signal), where 5.1 names the DOM type.
 * - `effect`'s callback returns a cleanup or `undefined`, where 5.1 writes `void | (() => void)`:
 *   typescript-eslint's no-invalid-void-type refuses `void` in a union and no file may switch a rule off
 *   (10.4). An inline callback with no `return` still types; a function declared `(): void` needs a
 *   wrapping arrow [measured: tsc 6.0.3].
 */

export type Json = null | boolean | number | string | Json[] | { [key: string]: Json };
export type ContentId = string; // 'lsn.cond.shrinking-sample-space' (content-format 4.1)
export type LocalId = string; // 'shade', 'grid', 'd': unique inside its parent
export type ElementId = string; // 'cell:5,3'; on a screen with several widgets the host prefixes the widget id: 'grid/cell:5,3'
export type Mark = 'correct' | 'not-yet' | 'kept' | 'reveal'; // grading styles (widgets-stage0 1.5)
export type HighlightStyle = 'ring' | 'wash' | 'flash'; // tutor and hint "Point" styles

/** Compiled ZQ Markdown (content-format 2.4). The compiler emits it; the engine's Prose renderer is its only reader. */
export type Token =
  | ['t', string] // text
  | ['b' | 'i', Token[]] // bold, italic
  | ['c', string] // inline code
  | ['m' | 'M', string] // inline and display maths (KaTeX source)
  | ['l', ContentId, Token[]] // link to a glossary term, lesson, card or item
  | ['v', string] // template value path (content-format 3.6)
  | ['if', string, Token[], Token[]] // one level of condition
  | ['p'] // paragraph break
  | ['ul', Token[][]]; // list (summary ideas, solution steps, model answers)
export type TokenList = Token[];

/** Owns every timer, frame callback, listener, effect and abort in one screen or widget. */
export interface Scope {
  readonly signal: AbortSignal; // aborts on dispose
  readonly disposed: boolean;
  later(fn: () => void, ms: number): () => void; // returns a cancel function
  every(fn: () => void, ms: number): () => void;
  frame(fn: (t: number) => void): () => void; // one animation frame
  loop(fn: (t: number, dt: number) => boolean): () => void; // runs each frame while fn returns true
  listen(
    target: EventTarget,
    type: string,
    fn: (e: Event) => void,
    opts?: { capture?: boolean; once?: boolean; passive?: boolean; signal?: AbortSignal },
  ): void;
  effect(fn: () => (() => void) | undefined): void; // a signals effect disposed with the scope; fn may return its cleanup
  own(dispose: () => void): void; // anything else (observers, workers)
  child(): Scope; // disposed with its parent
  dispose(): void; // idempotent
}

/** Counter-based Philox4x32-10 (@zq/mathcore/rng). Draw k of stream s is a pure function of (seed, s, k). */
export interface Rng {
  next(): number; // uniform on [0, 1) with 53 random bits; advances the counter
  at(index: number): number; // the draw at an index, without advancing
  int(lo: number, hi: number): number; // inclusive, unbiased by rejection on 32-bit words
  normal(): number; // Box-Muller from two draws
  fork(stream: string): Rng; // an independent stream
}

/** A lesson screen's seed is hash32(lessonId, screenId) unless the widget config sets `seed`; an item's comes from its generator draw (5.1). */
export interface SeedSource {
  readonly seed: number;
  rng(stream: string): Rng;
}
