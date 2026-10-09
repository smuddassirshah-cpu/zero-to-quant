/*
 * Answers, grades and show-why (docs/ARCHITECTURE.md 5.2). Widgets produce answers; graders
 * (content-format 7) read them. Widgets never parse or grade.
 * Decision notes:
 * - `Grade` is CONTENT-FORMAT.md 7.1's type with 5.2's amendment: `answerObjects` is filled by the host
 *   from `WidgetLogic.answerObjects`, and graders leave it empty, because only the widget knows its ids.
 * - `ShowStep` is the shape of CONTENT-FORMAT.md 3.2's zod `ShowStep`, the authored step a bundle carries
 *   and `Grade.diagnosis.show` returns; @zq/content-schema owns its validation (lengths, patterns, limits).
 *   The schema's `.strict()` is encoded as `?: never` on the other variant's keys, so a step that mixes a
 *   recipe with declarative fields fails to type, as it fails to parse. `args` is `Record<string, Json>`
 *   where the schema writes `z.unknown()`: a bundle is JSON, and recipes take `Record<string, Json>` (5.3).
 * - `CasService` is declared here, not in widget-api.ts where 5.3 lists it (that module re-exports it),
 *   so this module and base.ts name no DOM or Preact type and @zq/graders, which reads `GradeCtx`, can
 *   compile without the DOM lib, as B43 requires of the modules @zq/mathcore imports [our choice].
 */
import type { ContentId, ElementId, HighlightStyle, Json, LocalId, TokenList } from './base.ts';

export type Answer =
  | { type: 'choice'; ids: LocalId[] }
  | { type: 'numeric'; raw: string } // as typed; @zq/graders normalises and parses (content-format 7.2)
  | { type: 'expression'; latex: string }
  | { type: 'set'; ids: ElementId[] }
  | { type: 'interval'; raw: string } // '[3.35, 3.45)'; unions with 'U'
  | { type: 'ordering'; ids: LocalId[] }
  | { type: 'mapping'; pairs: [LocalId, LocalId][] }
  | { type: 'point'; pts: { id: ElementId; x: number; y: number; z?: number }[] }
  | { type: 'curve'; samples: [number, number][] } // at most 400 samples
  | { type: 'matrix'; entries: string[][] } // exact strings, parsed by graders
  | { type: 'distribution'; support: (number | string)[]; masses: string[] }
  | { type: 'state' } // graded by a predicate on the widget's own state
  | { type: 'output'; text: string }
  | { type: 'resultset'; columns: string[]; rows: Json[][] }
  | { type: 'code'; files: Record<string, string>; entry: string }
  | { type: 'long-form'; text: string }
  | { type: 'parts'; parts: Record<LocalId, Answer> };
export type AnswerType = Answer['type'];

/** LaTeX to MathJSON through the Compute Engine parser. */
export interface CasService {
  parse(latex: string): Json;
}

/** Supplied by the engine to @zq/graders for one grading call. */
export interface GradeCtx {
  predicate(name: string, args: Record<string, Json>): boolean; // bound to the answering widget's config and state
  cas(): Promise<CasService>; // lazy LaTeX to MathJSON (content-format decision 10)
  seed: number; // for probing points in expression checks
  locale: 'en-GB';
}

/** An authored show-why step (content-format 3.2): a widget recipe, or a declarative step the host expands. */
// prettier-ignore
export type ShowStep =
  | { widget: LocalId; recipe: string; args?: Record<string, Json>;    // recipe: '^[a-z][a-z0-9-]*$'
      set?: never; highlight?: never; annotate?: never; ms?: never }
  | { set?: Record<string, number | string>;                           // tween non-answer widget variables
      highlight?: ElementId[];                                         // at most 6, widget-prefixed: 'grid/cell:5,5'
      annotate?: { at: ElementId; text: string }[];                    // at most 3; text at most 80 characters
      ms?: number;                                                     // an integer from 300 to 1,200
      widget?: never; recipe?: never; args?: never };

/** CONTENT-FORMAT.md 7.1, amended by ARCHITECTURE.md 5.2. */
export interface Grade {
  verdict: 'correct' | 'not-yet' | 'nudge'; // 'nudge': unparseable or out of range; costs no attempt
  parts?: Record<LocalId, 'correct' | 'not-yet'>; // multi-part
  diagnosis?: { key?: LocalId; mc?: ContentId; slip?: true; line: TokenList; show?: ShowStep[] };
  nudge?: string; // "A probability lies between 0 and 1"
  accepted: TokenList; // the accepted-answer rule (content-format 7.9)
  normalised: unknown; // what was graded, for the attempt snapshot
  answerObjects: ElementId[]; // the only elements grading may recolour; the host fills it, graders leave it empty
}

/** What a widget recipe expands into: data the engine animates. Richer than authored ShowStep, still declarative. */
// prettier-ignore
export type MotionStep =
  | { k: 'set'; widget: LocalId; values: Record<string, number | string>; ms: number;
      ease: 'morph' | 'standard' | 'spring-snap' | 'spring-physical' }  // view state only (5.3)
  | { k: 'highlight'; ids: ElementId[]; style: HighlightStyle; times?: number; gapMs?: number }
  | { k: 'annotate'; at: ElementId; text: string }                     // at most 80 characters
  | { k: 'wait'; ms: number }
  | { k: 'together'; steps: MotionStep[] };
