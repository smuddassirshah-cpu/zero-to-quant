// zq/no-nondeterminism (scope in eslint.config.js, ARCHITECTURE.md 10.4): code whose numbers are
// shown or graded gives the same bits on every engine and every run, so it reads no clock and no
// unseeded randomness; seeded draws come from @zq/mathcore's Philox (ARCHITECTURE.md decision 14).
// Decision notes:
// - Refused: `Date` and `Temporal` on any value use (`new Date(0)`, `Date.now`, `Date.UTC`, an
//   alias, `instanceof Date`), and `performance` on any value use too, since each of its members
//   reads the clock [our choice: 10.4 names `performance.now`]; `Math.random`,
//   `crypto.getRandomValues` and `crypto.randomUUID`. Type positions are fine (`d: Date`).
// - Each is found as a global by scope analysis (a local `Date` is fine), as a member or destructured
//   key of `globalThis`, `window` or `self`, and, where the type checker is available (`.ts`), on
//   anything typed `Math`, `Crypto`, `Performance`, `DateConstructor` or the global object: an alias,
//   a parameter, `g.Math` after `const g = globalThis`.
// - `Math`, `crypto` and the global objects are usable only through static members or a
//   destructuring with static keys and no rest, so the rule sees every member taken: `Math[k]`,
//   `Reflect.get(Math, k)`, `const M = Math`, `{ Math } = globalThis` and passing one on are refused.
// - Option `transcendental`, set for `content/generators/**` (CONTENT-FORMAT.md 5.3), also refuses
//   the Math functions ECMA-262 21.3.2 leaves implementation-approximated [recalled: the spec could
//   not be fetched from this session] and `**` on numbers (Number::exponentiate, the same), whose
//   last bit differs between engines; `dmath` replaces them. `sqrt`, `fround` and the rounding
//   functions are exact and pass, and so does `**` when an operand is a bigint (a literal, a
//   `BigInt()` call, or typed so). The option covers the whole generator module, not only `accept`,
//   `level` and `answer` as 5.3 words it: `build` must be byte-identical on every device (5.4),
//   `diagnoses` is compared point by point with the Python twin (5.6), and a per-function check would
//   miss the helpers and module constants those functions read [our choice, reported as a deviation].
// - Accepted residue, left to review and the cross-engine tests: a source received from code outside
//   the scope and used other than by a member or a call (`Reflect.construct(D, [])` for a parameter
//   `D: DateConstructor`); aliases of the global object in `.js`, which has no type checker; `Intl`
//   and the `toLocale*` methods (locale data differs between engines; 10.4 does not list them); Node's
//   `crypto` and `perf_hooks`, which zq/layering keeps out (mathcore and logic.ts import no npm or
//   builtin module).
import type { Rule, Scope } from 'eslint';
import {
  hasType,
  isGlobal,
  keyName,
  patternSource,
  propName,
  unwrap,
  type ESNode,
  type NodeOf,
} from '../util/ast.ts';

const CLOCKS = new Set(['Date', 'Temporal', 'performance']);
const RANDOM: ReadonlyMap<string, ReadonlySet<string>> = new Map([
  ['Math', new Set(['random'])],
  ['crypto', new Set(['getRandomValues', 'randomUUID'])],
]);
const KINDS = new Set([...CLOCKS, ...RANDOM.keys()]);
const GLOBAL_OBJECTS = new Set(['globalThis', 'window', 'self']);
const GUARDED = [...RANDOM.keys(), ...GLOBAL_OBJECTS];
const TRANSCENDENTAL = new Set(
  [
    'acos acosh asin asinh atan atan2 atanh cbrt cos cosh exp',
    'expm1 hypot log log10 log1p log2 pow sin sinh tan tanh',
  ].flatMap((line) => line.split(' ')),
);
// The type of each watched global, and the global it names; the global object's is `typeof globalThis`.
const TYPES: readonly (readonly [ReadonlySet<string>, string])[] = [
  [new Set(['Math']), 'Math'],
  [new Set(['Crypto']), 'crypto'],
  [new Set(['Performance']), 'performance'],
  [new Set(['DateConstructor']), 'Date'],
];
const TYPED = new Set(TYPES.flatMap(([types]) => [...types]));
const GLOBAL_TYPES = new Set(['globalThis', 'Window']);
const DATE_TYPES = new Set(['DateConstructor']);
// TypeScript's expression wrappers and an optional chain's end (`self?.Math`): `strip` removes them
// from an owner, `outermost` climbs them from a use.
const WRAPPERS = new Set([
  'TSAsExpression',
  'TSNonNullExpression',
  'TSSatisfiesExpression',
  'TSTypeAssertion',
  'ChainExpression',
]);

/** `node` without its wrappers: util/ast.ts's `unwrap`, and an optional chain's end too. */
function strip(node: ESNode): ESNode {
  let current = unwrap(node);
  while (current.type === 'ChainExpression') current = unwrap(current.expression);
  return current;
}

interface Checker {
  getBigIntType(): unknown;
  getNumberType(): unknown;
  isTypeAssignableTo(source: unknown, target: unknown): boolean;
}

/**
 * True when the type checker sees `node` as a bigint (a literal, a union of them): assignable to
 * `bigint` and not to `number`, so `any` and `never` do not pass. False without type information.
 */
function typedBigInt(sourceCode: Rule.RuleContext['sourceCode'], node: ESNode): boolean {
  const services = sourceCode.parserServices as
    { program?: { getTypeChecker(): Checker }; getTypeAtLocation?: (node: ESNode) => unknown } | undefined;
  if (!services?.program || !services.getTypeAtLocation) return false;
  const checker = services.program.getTypeChecker();
  const type = services.getTypeAtLocation(node);
  return (
    checker.isTypeAssignableTo(type, checker.getBigIntType()) &&
    !checker.isTypeAssignableTo(type, checker.getNumberType())
  );
}

/** `node` with the wrappers around it climbed (`Math as Math` for the `Math`). */
function outermost(node: Rule.Node): Rule.Node {
  let current = node;
  while (current.parent && WRAPPERS.has(current.parent.type)) current = current.parent;
  return current;
}

/**
 * True when a guarded value is used other than as the object of a member access (judged by
 * `member`, dynamic keys included) or as the source of an object pattern (judged per key).
 */
function escapes(node: Rule.Node): boolean {
  const use = outermost(node);
  const { parent } = use;
  if (parent?.type === 'MemberExpression' && parent.object === use) return false;
  if (parent?.type === 'VariableDeclarator' && parent.init === use) return parent.id.type !== 'ObjectPattern';
  if (parent?.type === 'AssignmentExpression' && parent.right === use)
    return parent.left.type !== 'ObjectPattern';
  return true;
}

const rule: Rule.RuleModule = {
  meta: {
    type: 'problem',
    docs: { description: 'Refuse clocks, unseeded randomness and, in generators, transcendental Math' },
    schema: [
      {
        type: 'object',
        properties: { transcendental: { type: 'boolean' } },
        additionalProperties: false,
      },
    ],
    messages: {
      clock: "'{{name}}' reads the clock, which deterministic code may not (ARCHITECTURE.md 10.4)",
      random:
        "'{{name}}' is not seeded: draw from @zq/mathcore's Philox by (seed, stream, index) (ARCHITECTURE.md 10.4)",
      transcendental:
        "'{{name}}' may differ between engines in the last bit: use @zq/mathcore's dmath (CONTENT-FORMAT.md 5.3)",
      escape:
        "'{{name}}' may be used here only through static members, so that each member taken is checked (ARCHITECTURE.md 10.4)",
    },
  },
  create(context) {
    const { sourceCode } = context;
    const transcendental =
      (context.options[0] as { transcendental?: boolean } | undefined)?.transcendental === true;
    const report = (node: ESNode, messageId: string, name: string) => {
      context.report({ node, messageId, data: { name } });
    };
    const globalObject = (node: ESNode) => {
      const target = strip(node);
      return (
        (target.type === 'Identifier' && GLOBAL_OBJECTS.has(target.name) && isGlobal(sourceCode, target)) ||
        hasType(sourceCode, target, GLOBAL_TYPES)
      );
    };
    // The watched global a node names syntactically: `Math`, `globalThis.Math`, `window['Date']`.
    const globalName = (node: ESNode): string | undefined => {
      const target = strip(node);
      const name =
        target.type === 'Identifier'
          ? isGlobal(sourceCode, target) && target.name
          : target.type === 'MemberExpression' && globalObject(target.object) && propName(target);
      return name && KINDS.has(name) ? name : undefined;
    };
    // How a global object is named in a report: as written (`self`, an alias `g`), or `globalThis`.
    const objectName = (node: ESNode) => {
      const target = strip(node);
      return target.type === 'Identifier' ? target.name : 'globalThis';
    };
    const typedKind = (node: ESNode): string | undefined =>
      hasType(sourceCode, node, TYPED)
        ? TYPES.find(([types]) => hasType(sourceCode, node, types))?.[1]
        : undefined;
    // `owner.name` (`name` undefined for a dynamic key or a rest), read by a member access or a pattern.
    const member = (node: ESNode, name: string | undefined, owner: ESNode) => {
      if (globalObject(owner)) {
        if (name === undefined) report(node, 'escape', objectName(owner));
        else if (CLOCKS.has(name)) report(node, 'clock', name);
        return;
      }
      const named = globalName(owner);
      const kind = named ?? typedKind(owner);
      // A clock named outright is reported where it is named: by `Program`, or as a global's member.
      if (kind === undefined || (named !== undefined && CLOCKS.has(named))) return;
      if (CLOCKS.has(kind)) report(node, 'clock', name === undefined ? kind : `${kind}.${name}`);
      else if (name === undefined) report(node, 'escape', kind);
      else if (RANDOM.get(kind)?.has(name)) report(node, 'random', `${kind}.${name}`);
      else if (transcendental && kind === 'Math' && TRANSCENDENTAL.has(name)) {
        report(node, 'transcendental', `Math.${name}`);
      }
    };
    const bigint = (node: ESNode): boolean => {
      const target = strip(node);
      if (target.type === 'Literal' && 'bigint' in target) return true;
      const { callee } = target.type === 'CallExpression' ? target : { callee: undefined };
      if (callee?.type === 'Identifier' && callee.name === 'BigInt' && isGlobal(sourceCode, callee))
        return true;
      return typedBigInt(sourceCode, target);
    };
    const power = (node: ESNode, left: ESNode, right: ESNode, operator: string) => {
      if (transcendental && !bigint(left) && !bigint(right)) report(node, 'transcendental', operator);
    };
    // A `DateConstructor` from elsewhere (a parameter) called or constructed without a member.
    const construct = (node: NodeOf<'CallExpression' | 'NewExpression'>) => {
      if (globalName(node.callee) === undefined && hasType(sourceCode, node.callee, DATE_TYPES)) {
        report(node, 'clock', 'Date');
      }
    };
    // Value references to a global nobody in this file declares; `typeof X` in a type is not one.
    const globalRefs = (name: string): Rule.Node[] => {
      const scope = sourceCode.scopeManager.globalScope;
      const variable = scope?.set.get(name);
      const refs: Scope.Reference[] = [
        ...(variable?.defs.length === 0 ? variable.references : []),
        ...(scope?.through.filter((ref) => ref.identifier.name === name) ?? []),
      ];
      return refs
        .filter((ref) => (ref as { isValueReference?: boolean }).isValueReference !== false)
        .map((ref) => ref.identifier as Rule.Node)
        .filter((id) => {
          const parent = id.parent?.type as string | undefined;
          return parent !== 'TSTypeQuery' && parent !== 'TSQualifiedName';
        });
    };

    return {
      Program() {
        for (const name of CLOCKS) for (const id of globalRefs(name)) report(id, 'clock', name);
        for (const name of GUARDED)
          for (const id of globalRefs(name)) if (escapes(id)) report(id, 'escape', name);
      },
      MemberExpression(node) {
        const name = propName(node);
        member(node, name, node.object);
        // `globalThis.Math` itself, taken as a value.
        if (name !== undefined && RANDOM.has(name) && globalObject(node.object) && escapes(node)) {
          report(node, 'escape', name);
        }
      },
      Property(node) {
        if (node.parent.type !== 'ObjectPattern') return;
        const owner = patternSource(node.parent) ?? node.parent;
        const name = keyName(node);
        if (name !== undefined && RANDOM.has(name) && globalObject(owner)) report(node, 'escape', name);
        else member(node, name, owner);
      },
      // A rest takes every key not named, so it is judged as a dynamic key.
      RestElement(node) {
        if (node.parent.type === 'ObjectPattern')
          member(node, undefined, patternSource(node.parent) ?? node.parent);
      },
      BinaryExpression(node) {
        if (node.operator === '**') power(node, node.left, node.right, '**');
      },
      AssignmentExpression(node) {
        if (node.operator === '**=') power(node, node.left, node.right, '**=');
      },
      CallExpression: construct,
      NewExpression: construct,
    };
  },
};

export default rule;
