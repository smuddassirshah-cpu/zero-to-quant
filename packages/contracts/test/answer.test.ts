// Compile-time tests of docs/ARCHITECTURE.md 5.2 with CONTENT-FORMAT.md 3.2 (ShowStep) and 7.1 (Grade).
import type { Answer, AnswerType, CasService, Grade, GradeCtx, MotionStep } from '@zq/contracts/answer';
import type { ShowStep } from '@zq/contracts/answer';
import type { ElementId, Json, TokenList } from '@zq/contracts/base';
import { describe, expectTypeOf, test } from 'vitest';
import type { OptionalKeys, RequiredKeys, Words } from './types.ts';

type Of<T extends AnswerType> = Extract<Answer, { type: T }>;

describe('answers, grades and show-why (5.2)', () => {
  test('one union for every widget: the 17 answer types of WIDGETS.md 1.3', () => {
    expectTypeOf<AnswerType>().toEqualTypeOf<
      | Words<'choice numeric expression set interval ordering mapping point curve matrix distribution'>
      | Words<'state output resultset code long-form parts'>
    >();
  });

  test('answers carry raw input for the graders to parse; parts nest them', () => {
    expectTypeOf<Of<'numeric'>>().toEqualTypeOf<{ type: 'numeric'; raw: string }>();
    expectTypeOf<Of<'matrix'>['entries']>().toEqualTypeOf<string[][]>();
    expectTypeOf<Of<'state'>>().toEqualTypeOf<{ type: 'state' }>();
    expectTypeOf<Of<'point'>['pts'][number]>().toEqualTypeOf<{
      id: ElementId;
      x: number;
      y: number;
      z?: number;
    }>();
    expectTypeOf<Of<'parts'>['parts']>().toEqualTypeOf<Record<string, Answer>>();
    expectTypeOf<{ type: 'numeric'; raw: number }>().not.toExtend<Answer>();
    expectTypeOf<{ type: 'probability'; raw: string }>().not.toExtend<Answer>();
  });

  test('GradeCtx binds predicates, a lazy CAS, a seed and the locale', () => {
    expectTypeOf<RequiredKeys<GradeCtx>>().toEqualTypeOf<'predicate' | 'cas' | 'seed' | 'locale'>();
    expectTypeOf<OptionalKeys<GradeCtx>>().toBeNever();
    expectTypeOf<GradeCtx['predicate']>().toEqualTypeOf<
      (name: string, args: Record<string, Json>) => boolean
    >();
    expectTypeOf<GradeCtx['cas']>().returns.resolves.toEqualTypeOf<CasService>();
    expectTypeOf<CasService['parse']>().returns.toEqualTypeOf<Json>();
    expectTypeOf<GradeCtx['locale']>().toEqualTypeOf<'en-GB'>();
  });

  test('Grade is content-format 7.1 with answerObjects filled by the host', () => {
    expectTypeOf<RequiredKeys<Grade>>().toEqualTypeOf<
      'verdict' | 'accepted' | 'normalised' | 'answerObjects'
    >();
    expectTypeOf<OptionalKeys<Grade>>().toEqualTypeOf<'parts' | 'diagnosis' | 'nudge'>();
    expectTypeOf<Grade['verdict']>().toEqualTypeOf<'correct' | 'not-yet' | 'nudge'>();
    expectTypeOf<Grade['parts']>().toEqualTypeOf<Record<string, 'correct' | 'not-yet'> | undefined>();
    expectTypeOf<NonNullable<Grade['diagnosis']>>().toEqualTypeOf<{
      key?: string;
      mc?: string;
      slip?: true;
      line: TokenList;
      show?: ShowStep[];
    }>();
    expectTypeOf<Grade['nudge']>().toEqualTypeOf<string | undefined>();
    expectTypeOf<Grade['answerObjects']>().toEqualTypeOf<ElementId[]>();
    expectTypeOf<Grade['normalised']>().toBeUnknown();
  });

  test('ShowStep is a recipe call or a declarative step, never both (content-format 3.2)', () => {
    expectTypeOf({ widget: 'grid', recipe: 'flash', args: { cells: ['cell:5,1'] } }).toExtend<ShowStep>();
    expectTypeOf({
      set: { zoom: 2, step: 'b' },
      highlight: ['grid/cell:4,4'],
      annotate: [{ at: 'grid/cell:5,5', text: 'counted twice' }],
      ms: 600,
    }).toExtend<ShowStep>();
    expectTypeOf<{ widget: string; recipe: string; highlight: string[] }>().not.toExtend<ShowStep>();
    expectTypeOf<{ widget: string; recipe: string; set: Record<string, number> }>().not.toExtend<ShowStep>();
    expectTypeOf<{ widget: string; set: Record<string, number> }>().not.toExtend<ShowStep>();
    expectTypeOf<{ widget: string; recipe: string; args: { f: () => void } }>().not.toExtend<ShowStep>();
  });

  test('MotionStep is what recipes expand into', () => {
    expectTypeOf<MotionStep['k']>().toEqualTypeOf<Words<'set highlight annotate wait together'>>();
    expectTypeOf<Extract<MotionStep, { k: 'set' }>['ease']>().toEqualTypeOf<
      Words<'morph standard spring-snap spring-physical'>
    >();
    expectTypeOf({
      k: 'together',
      steps: [
        { k: 'highlight', ids: ['cell:5,5'], style: 'flash', times: 2, gapMs: 200 },
        { k: 'annotate', at: 'cell:5,5', text: 'counted twice' },
        { k: 'wait', ms: 300 },
        { k: 'set', widget: 'grid', values: { zoom: 2 }, ms: 480, ease: 'morph' },
      ],
    } satisfies MotionStep).toExtend<MotionStep>();
  });
});
