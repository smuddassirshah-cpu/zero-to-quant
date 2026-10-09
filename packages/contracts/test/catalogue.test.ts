// docs/ARCHITECTURE.md 5.6 encoded as a test: each catalogue method's new home exists on the contract with
// the shape the table names, and the methods the host took over exist on neither the logic nor the view API.
import type { Answer } from '@zq/contracts/answer';
import type { ElementId, Json, Mark, Scope } from '@zq/contracts/base';
import type { BaseConfig, Target, WidgetLogic, WidgetState } from '@zq/contracts/widget';
import type { WidgetApi } from '@zq/contracts/widget-api';
import { expectTypeOf, test } from 'vitest';
import type { Words } from './types.ts';

type L = WidgetLogic<BaseConfig, Json, Json>;
type Api = WidgetApi<Json, Json>;
type S = WidgetState<Json, Json>;

test("where the catalogues' methods went (5.6)", () => {
  // getState, setState: api.state reads, api.change and api.commit write.
  expectTypeOf<Api['state']['value']>().toEqualTypeOf<S>();
  expectTypeOf<Api['change']>().parameter(0).toEqualTypeOf<(s: S) => S>();
  expectTypeOf<Api['commit']>().parameter(0).toEqualTypeOf<((s: S) => S) | undefined>();
  // ready(), answer(): logic.answer, non-null when ready. dirty(): logic.dirty.
  expectTypeOf<L['answer']>().returns.toEqualTypeOf<Answer | null>();
  expectTypeOf<L['dirty']>().returns.toEqualTypeOf<boolean>();
  // lock(on): api.locked. preview(patch): api.ghost. destroy(): the host's scope.
  expectTypeOf<Api['locked']['value']>().toEqualTypeOf<boolean>();
  expectTypeOf<Api['ghost']>().toEqualTypeOf<boolean>();
  expectTypeOf<Api['scope']>().toEqualTypeOf<Scope>();
  // mark and grade painting: logic.marks. showWhy(key): logic.recipes. reveal(): logic.solved. reset(): init.
  expectTypeOf<NonNullable<L['marks']>>().returns.toEqualTypeOf<Record<ElementId, Mark>>();
  expectTypeOf<NonNullable<L['solved']>>().returns.toEqualTypeOf<S>();
  expectTypeOf<L['init']>().returns.toEqualTypeOf<S>();
  expectTypeOf<L['targets']>().returns.toEqualTypeOf<Target[]>();
  // describe, targets, secret, tryable, tryValue, code, predicates and recipes keep their names on logic.
  expectTypeOf<Words<'describe targets secret tryable tryValue code predicates recipes'>>().toExtend<
    keyof L
  >();
  // The host owns the rest: none of these is on the logic or the view API.
  type Gone =
    | Words<'getState setState ready lock mark showGrade clearMarks clearGrade showWhy reveal reset ids'>
    | Words<'highlight annotate clearTutor preview snapshot on resize destroy configSchema generators'>;
  expectTypeOf<Extract<keyof L | keyof Api, Gone>>().toBeNever();
});
